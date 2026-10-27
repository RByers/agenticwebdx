# Fetch monthly npm download counts from the public npm registry API.
# Usage: python3 tools/npm_downloads.py > web/data/npm-downloads.csv
# Output columns: package,month,downloads (calendar-month totals, Sep 2023 to Sep 2026).
# Uses https://api.npmjs.org/downloads/range/<start>:<end>/<package> (daily counts,
# max 18 months per request) and sums the days of each month.
import json, sys, time, urllib.parse, urllib.request
from collections import defaultdict

PACKAGES = [
    # shadcn/ui stack and its companions (the CLI was renamed shadcn-ui -> shadcn in Jul 2024)
    'shadcn', 'shadcn-ui', 'lucide-react', 'class-variance-authority', 'tailwind-merge',
    '@radix-ui/react-dialog', 'tailwindcss',
    # JS stand-ins for features the platform now has (anchor positioning)
    '@floating-ui/dom',
    # frameworks and build tools
    'react', 'next', 'vite', 'preact', 'vue', 'svelte', '@angular/core', 'lit', 'jquery',
    # other React-stack picks
    'zustand', 'react-hook-form', 'framer-motion', 'motion',
    # baselines that nobody picks for UI
    'lodash', 'express', 'typescript',
]
CHUNKS = [('2023-09-01', '2024-08-31'), ('2024-09-01', '2025-08-31'),
          ('2025-09-01', '2026-09-30')]

def fetch(pkg, start, end):
    url = (f"https://api.npmjs.org/downloads/range/{start}:{end}/"
           + urllib.parse.quote(pkg, safe='@'))
    for _ in range(4):
        try:
            return json.loads(urllib.request.urlopen(url, timeout=60).read())['downloads']
        except Exception as ex:
            print(pkg, ex, file=sys.stderr); time.sleep(5)
    raise SystemExit(f"failed: {pkg} {start}:{end}")

print('package,month,downloads')
for pkg in PACKAGES:
    months = defaultdict(int)
    for start, end in CHUNKS:
        for d in fetch(pkg, start, end):
            months[d['day'][:7]] += d['downloads']
        time.sleep(0.5)
    for m in sorted(months):
        print(f"{pkg},{m},{months[m]}", flush=True)
