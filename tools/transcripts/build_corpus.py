import json,glob,os,re,collections,sys
root=sys.argv[1]
ev=collections.defaultdict(dict)
def walk_events(obj):
    if isinstance(obj,dict):
        d=obj.get('ccr',obj)
        if isinstance(d,dict) and isinstance(d.get('data'),list):
            for e in d['data']: yield e
def parse(path):
    s=open(path,errors='replace').read()
    i=s.find('{'); j=s.rfind('}')
    if i<0: return
    try:
        yield from walk_events(json.loads(s[i:j+1])); return
    except Exception: pass
    for line in s.splitlines():
        line=line.strip()
        if line.startswith('{'):
            try: o=json.loads(line)
            except Exception: continue
            if 'data' in o or 'ccr' in o: yield from walk_events(o)
            else: yield o
def render_content(c):
    out=[]
    if isinstance(c,str): return [c]
    for b in c or []:
        if not isinstance(b,dict): continue
        t=b.get('type')
        if t=='text': out.append(b.get('text',''))
        elif t=='tool_use': out.append('[TOOL_USE '+b.get('name','')+'] '+json.dumps(b.get('input'))[:20000])
        elif t=='tool_result':
            cc=b.get('content')
            if isinstance(cc,list): cc='\n'.join(x.get('text','') for x in cc if isinstance(x,dict))
            out.append('[TOOL_RESULT] '+str(cc)[:20000])
        elif t=='thinking': out.append('[THINKING] '+b.get('thinking',''))
    return out
files=[p for p in glob.glob(root+'/transcripts/*/*') if os.path.isfile(p)]
bad=0
for p in files:
    got=False
    for e in parse(p) or []:
        for role in ('user','assistant'):
            if role in e:
                m=e[role]; inner=m.get('internal_anthropic_catchall',m)
                sid=inner.get('session_id') or ''
                sid='session_'+sid.split('_',1)[1] if '_' in sid else os.path.basename(os.path.dirname(p))
                uuid=m.get('uuid') or inner.get('uuid')
                msg=inner.get('message',{})
                txt='\n'.join(render_content(msg.get('content')))
                ev[sid][uuid]=(e.get('created_at',''),role,txt)
                got=True
    if not got: bad+=1
n=0
for sid,d in ev.items():
    with open(f'{root}/corpus/{sid}.txt','w') as f:
        for uuid,(t,role,txt) in sorted(d.items(),key=lambda x:x[1][0]):
            f.write(f'\n=== {t} {role} {uuid}\n{txt}\n')
    n+=1
print('sessions',n,'files',len(files),'unparsed',bad)
