"""Verify the B-P3-04 story metadata and TC ownership against the WP JSON lines. Read-only."""
import io, json, re

WP = "_work/msr/wp/B-P3-04.md"
OWN = {
    "TechX": "TechX (suggested; any team may pick up this story)",
    "DEVOPS": "DevOps team (suggested; any team may pick up this story)",
    "INFRA": "SCB IT infrastructure (suggested; any team may pick up this story)",
}
WT = {"APP": "App development", "CON": "Contract", "INF": "Infrastructure", "OPS": "DevOps"}

wp = io.open(WP, encoding="utf-8").read()
rows = [json.loads(line) for line in wp.splitlines() if line.startswith('{"id"')]
bad = 0
for r in rows:
    sid = r["id"]
    if not sid.startswith("RWB-P3-E20"):
        continue
    text = io.open(r["file"], encoding="utf-8").read()
    head = text.split("### 1.", 1)[0]
    meta = {m.group(1).strip(): m.group(2).strip()
            for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$", head, re.M)}
    exp = {
        "Story key": sid,
        "Work type": f"{r['wt']} ({WT[r['wt']]})",
        "Suggested owner": OWN[r["owner"]],
        "Service": "rwb-case",
        "Service epic": "RWB-SVC-P3",
        "Wave": str(r["wave"]),
        "Business epic": r["business_epic"],
        "Release": r["release"] + " (tentative)",
        "Legacy key": r["legacy"],
        "Legacy disposition": r["disposition"],
        "Build status": r["build_status"],
        "Patterns applied": ", ".join(r["patterns"]),
        "Parallel lane": r["lane"],
        "Ready to start": r["ready"],
        "Depends on (build)": ", ".join(r["H"]) or "None",
        "Contract dependencies": ", ".join(r["C"]) or "None",
        "Integration dependencies": ", ".join(r["I"]) or "None",
        "External dependencies": ", ".join(r["X"]) or "None",
        "PRD reference": "Pending (C1)",
        "Status": "Draft (realignment v1)",
    }
    diff = {k: (meta.get(k), v) for k, v in exp.items() if meta.get(k) != v}
    bad += bool(diff)
    print(sid, "meta", "OK" if not diff else diff)
    sec = text.split("### 16. Test cases", 1)[1].split("### 17.", 1)[0]
    tcs = re.findall(r"^\|\s*(TC-[A-Za-z0-9-]+)\s*\|", sec, re.M)
    if r["wt"] == "APP":
        miss = [x for x in r["tcs_legacy"] if x not in tcs]
        print("   APP tcs", len(tcs), "missing legacy", miss)
        bad += bool(miss)
    else:
        legacy = [x for x in tcs if re.match(r"TC-E[12]-", x)]
        print("   ", r["wt"], "tcs", len(tcs), "legacy ids present", legacy)
print("BAD", bad)
