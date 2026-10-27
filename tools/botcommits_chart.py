# Render AI-attributed commits as a share of public GitHub push events
# from botcommits.dev's data.json (https://botcommits.dev/data.json).
# Usage: python3 botcommits_chart.py data.json > chart.svg
import json, sys
d = json.load(open(sys.argv[1]))
pts = [(m, d['total6'][i] / d['pushes'][m] * 100)
       for i, m in enumerate(d['labels']) if not d['partial'][i] and d['pushes'].get(m)]
W, H = 1000, 230
L, R, T, B = 60, 90, 18, 34
ymax = 20
X = lambda i: L + i / (len(pts) - 1) * (W - L - R)
Y = lambda v: T + (1 - v / ymax) * (H - T - B)
o = [f'<svg class=chart viewBox="0 0 {W} {H}" role=img aria-labelledby=bc-title bc-desc>',
     '<title id=bc-title>AI-attributed commits as a share of public GitHub push events, Jan 2025 to Jul 2026</title>',
     f'<desc id=bc-desc>Near zero until mid-2025, rising steeply from about 2% in December 2025 to about 15% in April 2026, then flattening at {pts[-1][1]:.1f}% in {pts[-1][0]}.</desc>']
for v in range(0, ymax + 1, 5):
    o.append(f'<line class=grid x1={L} x2={W-R} y1={Y(v):.1f} y2={Y(v):.1f} />')
    o.append(f'<text class=tick x={L-8} y={Y(v)+6:.1f} text-anchor=end>{v}%</text>')
for i, (m, _) in enumerate(pts):
    y, mo = m.split('-')
    if mo in ('01', '04', '07', '10'):
        lab = ['Jan', 'Apr', 'Jul', 'Oct'][int(mo) // 3] + (f' {y}' if mo == '01' else '')
        o.append(f'<text class=tick x={X(i):.1f} y={H-8} text-anchor=middle>{lab}</text>')
d_ = ' '.join(f'{"M" if i == 0 else "L"}{X(i):.1f},{Y(v):.1f}' for i, (_, v) in enumerate(pts))
o.append(f'<path class=line d="{d_}" />')
for i, (m, v) in enumerate(pts):
    if m in ('2025-12', '2026-04') or i == len(pts) - 1:
        o.append(f'<circle class=dot cx={X(i):.1f} cy={Y(v):.1f} r=5 />')
        dx, anchor = (10, 'start') if i == len(pts) - 1 else (-10, 'end')
        o.append(f'<text class=value x={X(i)+dx:.1f} y={Y(v)+6:.1f} text-anchor={anchor}>{v:.1f}%</text>')
o.append('</svg>')
print('\n'.join(o))
