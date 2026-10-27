# Render web/data/stackoverflow-questions.csv as the inline SVG chart used in
# web/index.html. Each series is shown as a % of its own peak month.
# Usage: python3 so_chart.py web/data/stackoverflow-questions.csv > chart.svg
import csv, sys
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
SERIES = [('all', 'All questions', 'so-all'),
          ('javascript', '[javascript]', 'so-js'),
          ('css', '[css]', 'so-css')]
data = {k: [] for k, _, _ in SERIES}
for row in csv.DictReader(open(sys.argv[1])):
    if row['series'] in data and row['questions'] not in ('', 'None'):
        y, m = map(int, row['month'].split('-'))
        data[row['series']].append((y + (m - 1) / 12, int(row['questions']), f'{MONTHS[m-1]} {y}'))
W, H = 1000, 290
L, R, T, B = 60, 70, 18, 34
x0, x1 = 2009, 2026.9
X = lambda x: L + (x - x0) / (x1 - x0) * (W - L - R)
Y = lambda pct: T + (1 - pct / 100) * (H - T - B)
peaks = {k: max(pts, key=lambda p: p[1]) for k, pts in data.items()}
o = [f'<svg class=chart viewBox="0 0 {W} {H}" role=img aria-labelledby=so-title so-desc>']
o.append('<title id=so-title>New Stack Overflow questions per month, 2009–2026, as % of each series’ peak</title>')
desc = '; '.join(f'{name} peaked at {peaks[k][1]:,} in {peaks[k][2]} and fell to '
                 f'{data[k][-1][1]:,} ({100 * data[k][-1][1] / peaks[k][1]:.1f}% of peak) by {data[k][-1][2]}'
                 for k, name, _ in SERIES)
o.append(f'<desc id=so-desc>{desc}. The slow decline began around 2017 and became a collapse after ChatGPT.</desc>')
for v in range(0, 101, 25):
    o.append(f'<line class=grid x1={L} x2={W-R} y1={Y(v):.1f} y2={Y(v):.1f} />')
    o.append(f'<text class=tick x={L-8} y={Y(v)+5:.1f} text-anchor=end>{v}%</text>')
for yr in range(2010, 2027, 2):
    o.append(f'<text class=tick x={X(yr):.1f} y={H-8} text-anchor=middle>{yr}</text>')
for xv, label, dy in [(2022 + 10.97/12, 'ChatGPT', 0), (2025 + 1/12, 'Coding agents', 22)]:
    o.append(f'<line class=event x1={X(xv):.1f} x2={X(xv):.1f} y1={T} y2={H-B} />')
    o.append(f'<text class=event-label x={X(xv)+6:.1f} y={T+14+dy}>{label}</text>')
# Draw "all" last so the headline series sits on top.
for k, _, cls in reversed(SERIES):
    pk = peaks[k][1]
    d = ' '.join(f'{"M" if i == 0 else "L"}{X(x):.1f},{Y(100 * c / pk):.1f}'
                 for i, (x, c, _) in enumerate(data[k]))
    o.append(f'<path class="line {cls}" d="{d}" />')
for k, _, cls in reversed(SERIES):
    x = peaks[k][0]
    o.append(f'<circle class="dot {cls}" cx={X(x):.1f} cy={Y(100):.1f} r=5 />')
o.append('</svg>')
print('\n'.join(o))
# Legend (paste above the SVG): series name and its peak.
print('<!-- legend: ' + ' | '.join(f'{name}: peak {peaks[k][1]:,} ({peaks[k][2]})'
                                   for k, name, _ in SERIES) + ' -->', file=sys.stderr)
