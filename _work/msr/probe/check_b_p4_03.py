import json, re, sys
from pathlib import Path

ROOT = Path(".").resolve()
WORK = ROOT / "_work" / "msr"
plan = json.load(open(WORK / "plan" / "split_plan.json", encoding="utf-8"))
slices = {s["id"]: s for s in plan["slices"]}
KEY = ["AD007", "AD008", "AD009", "AD010", "AD011"]
WTS = ["APP", "CON"]

# 1. jsonl
ids = set()
for kind in ("gaps", "assumptions"):
    p = WORK / kind / "B-P4-03.jsonl"
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(kind, "rows", len(rows), "unique", len({r["id"] for r in rows}))
    ids |= {r["id"] for r in rows}
    req = {"id", "title", "description", "type", "severity"} if kind == "gaps" else {"id", "text", "why"}
    for r in rows:
        miss = req - {k for k, v in r.items() if v not in (None, "")}
        if miss:
            print("  MISSING", r["id"], miss)

# 2. citations
cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
bad = {}
files = []
for k in KEY:
    for wt in WTS:
        f = ROOT / slices[f"RWB-P4-{k}-{wt}"]["file"]
        files.append(f)
        # fragment
        frag = WORK / "fragments" / f"RWB-P4-{k}-{wt}.json"
        files.append(frag)
for f in files:
    if not f.exists():
        print("MISSING FILE", f); continue
    for c in set(cite.findall(f.read_text(encoding="utf-8"))):
        if c not in ids:
            bad.setdefault(c, []).append(f.name)
print("unresolved citations:", len(bad))
for c, v in sorted(bad.items()):
    print("  ", c, v[:2])

# 3. fragments vs plan
for k in KEY:
    for wt in WTS:
        sid = f"RWB-P4-{k}-{wt}"
        frag = json.load(open(WORK / "fragments" / f"{sid}.json", encoding="utf-8"))
        s = slices[sid]
        for key, want in (("epic", s["epic"]), ("service", s["service"]), ("wt", s["wt"]), ("lane", s["lane"]),
                          ("ready", s["ready"]), ("business_epic", s["business_epic"]), ("wave", s["wave"]),
                          ("legacy", s["legacy"]), ("disposition", s["disposition"]), ("file", s["file"])):
            if str(frag.get(key)) != str(want):
                print("FRAG MISMATCH", sid, key, frag.get(key), "want", want)
        if s["release"] not in str(frag.get("release", "")):
            print("FRAG RELEASE", sid, frag.get("release"))
        for key, want in (("H", s["H"]), ("C", s["C"]), ("I", s["I"]), ("X", s["X"])):
            if frag.get(key) != want:
                print("FRAG DEP MISMATCH", sid, key, frag.get(key), "want", want)
        if frag.get("owner") != "TechX":
            print("FRAG OWNER", sid, frag.get("owner"))

# 4. story metadata
META = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
        "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
        "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies",
        "PRD reference", "Status"]
for k in KEY:
    for wt in WTS:
        sid = f"RWB-P4-{k}-{wt}"
        f = ROOT / slices[sid]["file"]
        t = f.read_text(encoding="utf-8")
        head = t.split("### 1.", 1)[0]
        rows = dict(re.findall(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$", head, re.M))
        got = [r for r in re.findall(r"^\|\s*([^|]+?)\s*\|", head, re.M) if r in META]
        if got != META:
            print("META ORDER", sid, got)
        s = slices[sid]
        checks = {
            "Story key": sid,
            "Suggested owner": "TechX (suggested; any team may pick up this story)",
            "Service": s["service"], "Service epic": s["epic"], "Wave": str(s["wave"]),
            "Business epic": s["business_epic"], "Legacy key": s["legacy"],
            "Legacy disposition": s["disposition"], "Build status": s["build_status"],
            "Parallel lane": s["lane"], "Ready to start": s["ready"],
            "PRD reference": "Pending (C1)", "Status": "Draft (realignment v1)",
        }
        for key, want in checks.items():
            if rows.get(key, "") != want:
                print("META VALUE", sid, key, repr(rows.get(key)), "want", repr(want))
        rel = rows.get("Release", "")
        if not rel.startswith(s["release"]) or "(tentative)" not in rel:
            print("META RELEASE", sid, rel)
        pats = ", ".join(s["patterns"])
        if rows.get("Patterns applied") != pats:
            print("META PATTERNS", sid, rows.get("Patterns applied"), "want", pats)
        h = ", ".join(s["H"]) if s["H"] else "None"
        if rows.get("Depends on (build)") != h:
            print("META H", sid, rows.get("Depends on (build)"), "want", h)
        c = ", ".join(s["C"]) if s["C"] else "None"
        if rows.get("Contract dependencies") != c:
            print("META C", sid, rows.get("Contract dependencies"), "want", c)
        if not t.startswith(f"# {sid} "):
            print("TITLE", sid, t.splitlines()[0])

# 5. forbidden
for f in files:
    if f.suffix != ".md":
        continue
    t = f.read_text(encoding="utf-8")
    low = t.lower()
    if "jira" in low or "atlassian.net" in low:
        print("TRACKER WORD", f.name)
    if "/api/recovery/v1/" in t and "As built (monolith)" not in t:
        print("OLD BASE", f.name)
    if re.search(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", t):
        print("EMAIL", f.name)
    for n in range(1, 20):
        if not re.search(rf"^### {n}\. ", t, re.M):
            print("SECTION MISSING", f.name, n)
            break
print("done")
