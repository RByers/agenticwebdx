# Fetch monthly new-question counts from the public Stack Exchange API.
# Usage: python3 so_fetch.py > log.txt  (lines: series year month count)
import json, time, urllib.request, gzip, calendar, sys
out = {}
def count(y, m, tag=None):
    s = calendar.timegm((y, m, 1, 0, 0, 0))
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    e = calendar.timegm((ny, nm, 1, 0, 0, 0))
    url = f"https://api.stackexchange.com/2.3/questions?site=stackoverflow&fromdate={s}&todate={e}&filter=total"
    if tag: url += f"&tagged={tag}"
    for i in range(4):
        try:
            r = urllib.request.urlopen(url, timeout=60).read()
            try: r = gzip.decompress(r)
            except OSError: pass
            d = json.loads(r)
            if 'total' in d: return d['total']
            print(d, file=sys.stderr); time.sleep(5)
        except Exception as ex:
            print(ex, file=sys.stderr); time.sleep(5)
for tag in [None, 'javascript', 'css']:
    key = tag or 'all'
    out[key] = {}
    for y in range(2009, 2027):
        for m in (1, 4, 7, 10):
            if (y, m) > (2026, 9) or (y, m) < (2009, 1): continue
            if tag == 'css' and m not in (1, 7): continue
            c = count(y, m, tag)
            out[key][f"{y}-{m:02d}"] = c
            print(key, y, m, c, flush=True)
            time.sleep(0.3)
json.dump(out, open('so.json', 'w'), indent=1)
