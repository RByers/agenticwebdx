#!/usr/bin/env python3
"""Turn the transcript-mining outputs into CSVs for web/data/.

Usage: to_csv.py <workdir> <outdir>
  <workdir>/findings/*.jsonl  pass-1 records (session + incident)
  <workdir>/freq/*.json       pass-2 per-pattern frequency results
Writes agent-session-incidents.csv and agent-session-patterns.csv.
Verbatim transcript quotes ("evidence", "quotes") are deliberately left out.
"""
import csv, glob, json, sys

work, out = sys.argv[1], sys.argv[2]

incidents = []
for f in sorted(glob.glob(f"{work}/findings/*.jsonl")):
    for line in open(f):
        if line.strip():
            r = json.loads(line)
            if r.get("type") == "incident":
                incidents.append(r)

cols = ["session_id", "project", "api", "category", "pattern", "summary",
        "cost_estimate", "discovered_by", "severity", "slide_potential", "design_lesson"]
with open(f"{out}/agent-session-incidents.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(cols)
    for r in sorted(incidents, key=lambda r: (r.get("project", ""), r.get("api", ""), r["session_id"])):
        w.writerow([str(r.get(c, "")) for c in cols])

pats = []
for f in sorted(glob.glob(f"{work}/freq/*.json")):
    pats += json.load(open(f))["patterns"]
pats.sort(key=lambda p: int(p["id"][1:]))
with open(f"{out}/agent-session-patterns.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "name", "episodes", "sessions", "zpcrweb_episodes", "meshcore_web_episodes",
                "found_by_user", "found_by_agent", "found_by_test",
                "cost_median", "cost_worst", "total_cost_estimate", "confidence", "sessions_list"])
    for p in pats:
        bp, fb = p.get("by_project", {}), p.get("found_by", {})
        w.writerow([p["id"], p["name"], p.get("episodes"), p.get("sessions"),
                    bp.get("zpcrweb"), bp.get("meshcore-web"),
                    fb.get("user"), fb.get("agent"), fb.get("test"),
                    p.get("cost_median"), p.get("cost_worst"), p.get("total_cost_estimate"),
                    p.get("confidence"),
                    " ".join(s["session_id"] for s in p.get("session_list", []))])
print(len(incidents), "incidents,", len(pats), "patterns")
