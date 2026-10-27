# Fetch every feature entry from the public chromestatus.com API and write a
# CSV with one row per entry, plus a summary of counts to stderr.
# Usage: python3 tools/chromestatus_fetch.py > web/data/chromestatus-features.csv
# The API returns at most 1000 entries per request, so this pages with `start`.
# Responses start with the XSSI guard ")]}'" which is stripped before parsing.
import collections, csv, json, sys, urllib.request

API = "https://chromestatus.com/api/v0/features?num=1000&start={}"

def page(start):
    raw = urllib.request.urlopen(API.format(start), timeout=120).read().decode()
    return json.loads(raw[raw.index("\n") + 1:] if raw.startswith(")]}'") else raw)

features, start = [], 0
while True:
    d = page(start)
    features += d["features"]
    start += len(d["features"])
    if not d["features"] or start >= d["total_count"]:
        break
assert len({f["id"] for f in features}) == len(features)

w = csv.writer(sys.stdout)
w.writerow(["id", "name", "feature_type", "chrome_status", "chrome_desktop_milestone",
            "created", "spec_link"])
for f in sorted(features, key=lambda f: f["id"]):
    c = f["browsers"]["chrome"]
    w.writerow([f["id"], f["name"], f["feature_type"], c["status"]["text"],
                c.get("desktop") or "", f.get("created") or "", f.get("spec_link") or ""])

print(f"total entries: {len(features)} (API total_count {d['total_count']})", file=sys.stderr)
for k, v in collections.Counter(f["browsers"]["chrome"]["status"]["text"] for f in features).most_common():
    print(f"status\t{k}\t{v}", file=sys.stderr)
for k, v in collections.Counter(f["feature_type"] for f in features).most_common():
    print(f"type\t{k}\t{v}", file=sys.stderr)
