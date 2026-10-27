# Render log.txt from so_fetch.py as the inline SVG chart used in web/index.html.
# Usage: python3 so_chart.py log.txt > chart.svg
import sys
# Reads log.txt lines "series year month count"; emits an inline SVG line chart.
pts = []
for line in open(sys.argv[1]):
    k, y, m, c = line.split()
    if k == 'all' and c != 'None':
        pts.append((int(y) + (int(m) - 1) / 12, int(c)))
W, H = 1000, 290
L, R, T, B = 60, 70, 18, 34
x0, x1 = 2009, 2026.9
ymax = 200000
X = lambda x: L + (x - x0) / (x1 - x0) * (W - L - R)
Y = lambda y: T + (1 - y / ymax) * (H - T - B)
o = [f'<svg class=chart viewBox="0 0 {W} {H}" role=img aria-labelledby=so-title so-desc>']
o.append('<title id=so-title>New Stack Overflow questions per month, 2009–2026</title>')
o.append('<desc id=so-desc>Peaks at about 197,000 in April 2016, slides to about 106,000 by October 2022, then collapses after ChatGPT to about 1,200 in July 2026.</desc>')
for v in range(0, ymax + 1, 50000):
    o.append(f'<line class=grid x1={L} x2={W-R} y1={Y(v):.1f} y2={Y(v):.1f} />')
    o.append(f'<text class=tick x={L-8} y={Y(v)+5:.1f} text-anchor=end>{v//1000}k</text>')
for yr in range(2010, 2027, 2):
    o.append(f'<text class=tick x={X(yr):.1f} y={H-8} text-anchor=middle>{yr}</text>')
for xv, label, dy in [(2022 + 10.97/12, 'ChatGPT', 0), (2025 + 1/12, 'Coding agents', 22)]:
    o.append(f'<line class=event x1={X(xv):.1f} x2={X(xv):.1f} y1={T} y2={H-B} />')
    o.append(f'<text class=event-label x={X(xv)+6:.1f} y={T+14+dy}>{label}</text>')
d = ' '.join(f'{"M" if i == 0 else "L"}{X(x):.1f},{Y(y):.1f}' for i, (x, y) in enumerate(pts))
o.append(f'<path class=line d="{d}" />')
peak = max(pts, key=lambda p: p[1]); last = pts[-1]
for (x, y), txt, anchor, dx, dyy in [(peak, f'{peak[1]:,}', 'start', 8, -6), (last, f'{last[1]:,}', 'end', -2, -12)]:
    o.append(f'<circle class=dot cx={X(x):.1f} cy={Y(y):.1f} r=5 />')
    o.append(f'<text class=value x={X(x)+dx:.1f} y={Y(y)+dyy:.1f} text-anchor={anchor}>{txt}</text>')
o.append('</svg>')
print('\n'.join(o))
