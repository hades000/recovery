"""Checks C01-C20 for the D-RCV-53 realignment. Read-only except the report files."""
import argparse, csv, json, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "compat"))
from common import ROOT, R22, WORK, SERVICES, ID_RE, LEGACY_RE, sha256, read_json, read_jsonl, decision

DEC = decision()
RETIRED = (f"Retired ({DEC})", "Already retired")

META_ROWS = ["Story key", "Work type", "Suggested owner", "Service", "Service epic", "Wave", "Business epic", "Release",
             "Legacy key", "Legacy disposition", "Build status", "Patterns applied", "Parallel lane", "Ready to start",
             "Depends on (build)", "Contract dependencies", "Integration dependencies", "External dependencies", "PRD reference", "Status"]
SECTIONS = ["Story", "Business rationale", "Preconditions", "Flow", "Exception paths", "INVEST check", "Acceptance criteria",
            "Business rules", "State transitions", "Authority", "Data", "Contract", "Solution plan", "Validation and messages",
            "Screens and states", "Test cases", "Guardrails", "Traceability", "Out of scope"]
SHORTS = {s["short"] for s in SERVICES}
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
JIRA_OK = {"Recovery Workbench Jira Impact and Follow-up v1.md"}
STAGES = {"B": ["C02", "C03", "C04", "C05", "C06", "C07", "C08", "C12", "C13", "C14", "C15", "C16", "C17", "C20"],
          "C": ["C09", "C10", "C11", "C12", "C13", "C19"], "D": ["C01", "C12", "C13", "C17", "C19", "C20"]}
QUICK = ["C02", "C03", "C05", "C12", "C13", "C18"]

def _t(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")

def _plan():
    return read_json(WORK / "plan" / "split_plan.json", {"slices": [], "legacy": {}})

def _stories(files):
    return [Path(f) for f in files if Path(f).suffix == ".md" and re.match(r"^RWB ", Path(f).name)]

def _frags():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (WORK / "fragments").glob("*.json")}

def _res(fails, warn=False):
    return ("PASS", []) if not fails else (("WARN" if warn else "FAIL"), fails[:200])

def c01(files=None):
    base = read_json(WORK / "plan" / "baseline.json", {}) or {}
    bad = [k for k, h in base.items() if not (ROOT / k).exists() or sha256(ROOT / k) != h]
    return _res([f"changed or missing: {k}" for k in bad])

def c02(files):
    fails = []
    for p in _stories(files):
        t = _t(p); m = re.match(r"^# (\S+)", t)
        if not m or not ID_RE.match(m.group(1)):
            fails.append(f"{p.name}: title line must start with a valid story ID")
        rows = re.findall(r"^\|\s*([^|]+?)\s*\|", t.split("### 1.", 1)[0], re.M)
        got = [r for r in rows if r in META_ROWS]
        if got != META_ROWS:
            fails.append(f"{p.name}: metadata rows missing or out of order: {[r for r in META_ROWS if r not in got][:5]}")
    return _res(fails)

def c03(files):
    fails = []
    for p in _stories(files):
        heads = re.findall(r"^### (\d+)\. (.+?)\s*$", _t(p), re.M)
        if [h[1] for h in heads[:19]] != SECTIONS or [int(h[0]) for h in heads[:19]] != list(range(1, 20)):
            fails.append(f"{p.name}: the 19 section headings are not complete and in order")
    return _res(fails)

def c04(files=None):
    return _res([f"missing story file: {x['file']}" for x in _plan()["slices"] if not (ROOT / x["file"]).exists()])

def c05(files):
    fails = []
    for p in _stories(files):
        for line in _t(p).splitlines():
            if re.match(r"^\s*Scenario:\s*AC\d+", line) and not re.search(rf"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, {re.escape(DEC)})\)", line):
                fails.append(f"{p.name}: AC line without origin tag: {line.strip()[:80]}")
    return _res(fails)

def c06(files=None):
    s = {x["id"]: x for x in _plan()["slices"]}; fails = []
    for i, f in _frags().items():
        for h in f.get("H", []):
            t = s.get(h)
            if not t or not (t["wt"] == "CON" or t["scope"] == s.get(i, {}).get("scope")):
                fails.append(f"{i}: H dependency {h} is not same-service or a contract")
        if f.get("I") and f.get("wt") != "ITG":
            fails.append(f"{i}: I dependencies allowed only on ITG stories")
    return _res(fails)

def c07(files=None):
    import networkx as nx
    s = {x["id"]: x for x in _plan()["slices"]}; g = nx.DiGraph()
    for i, f in _frags().items():
        if f.get("wt") != "CON":
            g.add_node(i)
            for h in f.get("H", []):
                if s.get(h, {}).get("wt") != "CON":
                    g.add_edge(h, i)
    if not nx.is_directed_acyclic_graph(g):
        return _res(["dependency cycle in fragments"])
    return _res([f"lane deeper than 4: {' -> '.join(p)}" for c in nx.weakly_connected_components(g)
                 for p in [nx.dag_longest_path(g.subgraph(c))] if len(p) > 4])

def c08(files=None):
    teams = {f.get("owner") for f in _frags().values() if f.get("ready") == "Day 1"}
    return _res([f"no Day-1 story for team type {t}" for t in ("TechX", "ACE", "INFRA", "DEVOPS", "QA") if t not in teams])

def c09(files=None):
    plan = _plan(); fails = []
    for k, v in plan["legacy"].items():
        if v["disposition"] in RETIRED:
            continue
        if not v["slices"]:
            fails.append(f"{k}: no new story")
    idx = {r["key"]: r for r in read_json(WORK / "plan" / "legacy_index.json", [])}
    for x in plan["slices"]:
        if x.get("preserved") and (ROOT / x["file"]).exists():
            t = _t(ROOT / x["file"])
            if "As built (monolith)" not in t:
                fails.append(f"{x['id']}: preserved story lacks the 'As built (monolith)' heading")
    return _res(fails)

def c10(files=None):
    plan = _plan(); idx = {r["key"]: r for r in read_json(WORK / "plan" / "legacy_index.json", [])}
    owned = {}
    for f in _frags().values():
        for a in f.get("acs", []):
            owned.setdefault(f.get("legacy"), set()).add(a.get("id") if isinstance(a, dict) else a)
    fails = []
    for k, v in plan["legacy"].items():
        if v["disposition"] in RETIRED or k not in idx:
            continue
        miss = [a for a in idx[k]["acs"] if a not in owned.get(k, set())]
        if miss:
            fails.append(f"{k}: legacy ACs not owned by any new story: {miss}")
    return _res(fails)

def c11(files=None):
    idx = read_json(WORK / "plan" / "legacy_index.json", []); plan = _plan()
    seen = set()
    for x in plan["slices"]:
        p = ROOT / x["file"]
        if p.exists():
            seen.update(re.findall(r"\bTC-[A-Z0-9]+-\d{3}-\d{2}\b", _t(p)))
    fails = [f"{r['key']}: legacy TC {t} not in any new story" for r in idx
             if plan["legacy"].get(r["key"], {}).get("disposition", "").startswith(("Retired", "Already")) is False for t in r["tcs"] if t not in seen]
    return _res(fails, warn=True)

def _names():
    names = set()
    for p in ROOT.glob("21*/**/*"):
        if p.suffix.lower() == ".csv":
            with open(p, encoding="utf-8", errors="ignore", newline="") as f:
                for row in csv.DictReader(f):
                    for k, v in row.items():
                        if k and re.search(r"(?i)assignee|reporter|creator|watcher|author|updated by", k) and v and " " in v.strip():
                            names.add(v.strip().lower())
        elif p.suffix.lower() == ".json":
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            names.update(n.lower() for n in re.findall(r'"displayName"\s*:\s*"([^"@]+ [^"@]+)"', txt))
    return names

def c12(files, names=None):
    names = _names() if names is None else names; fails = []
    email = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
    for p in files:
        p = Path(p)
        if p.suffix.lower() not in (".md", ".json", ".yaml", ".sql", ".txt") or not p.exists():
            continue
        for n, line in enumerate(_t(p).splitlines(), 1):
            low = line.lower()
            if any(nm in low for nm in names):
                fails.append(f"{p.name}:{n}: person name from the deny-list")
            if email.search(line) and "example" not in low and "noreply" not in low:
                fails.append(f"{p.name}:{n}: email address")
    return _res(fails)

def c13(files):
    fails, warns = [], []
    for p in files:
        p = Path(p)
        if p.name in JIRA_OK or p.suffix.lower() not in (".md", ".json", ".yaml", ".txt") or not p.exists():
            continue
        t = _t(p)
        if re.search(r"(?i)\bjira\b|atlassian\.net", t):
            if "As built (monolith)" in t:
                warns.append(f"{p.name}: issue-tracker reference inside a word-for-word preserved copy")
            else:
                fails.append(f"{p.name}: refers to the issue tracker")
    res = _res(fails)
    if warns:
        return ("WARN" if res[0] == "PASS" else res[0], (res[1] + warns)[:200])
    return res

def c14(files):
    fails = []
    for p in files:
        p = Path(p)
        if p.suffix == ".md" and p.exists() and not p.name.startswith("RWB ") and "_work" not in p.parts:
            head = "\n".join(_t(p).splitlines()[:6])
            if "SCB Collections and Recovery. Henka Group," not in head:
                fails.append(f"{p.name}: header lines (Template and Rules §R8.1) missing")
    return _res(fails)

def c15(files=None):
    s = {x["id"]: x for x in _plan()["slices"]}; fails = []
    for i, f in _frags().items():
        rel = s.get(i, {}).get("release", "")
        if rel and rel not in str(f.get("release", "")):
            fails.append(f"{i}: release date changed ({f.get('release')} vs {rel})")
        p = ROOT / s.get(i, {}).get("file", "")
        if rel and p.exists() and "(tentative)" not in _t(p):
            fails.append(f"{i}: release not marked (tentative)")
    return _res(fails)

def c16(files):
    fails = []
    for p in _stories(files):
        t = _t(p)
        for rx, grp in [(r"\brwb\.([a-z-]+)\.events\.v1\b", 1), (r"/api/recovery/([a-z-]+)/v1\b", 1), (r"\bqueue rwb-([a-z-]+)\b", 1)]:
            for m in re.finditer(rx, t):
                if m.group(grp) not in SHORTS:
                    fails.append(f"{p.name}: unknown service name '{m.group(grp)}' in {m.group(0)}")
        if re.search(r"/api/recovery/v1/", t) and "As built (monolith)" not in t:
            fails.append(f"{p.name}: old monolith API base outside the as-built section")
    return _res(fails)

def c17(files=None):
    req_g = {"id", "title", "description", "type", "severity"}; req_a = {"id", "text", "why"}
    ids, fails = set(), []
    for kind, req in (("gaps", req_g), ("assumptions", req_a)):
        for p in (WORK / kind).glob("*.jsonl"):
            for r in read_jsonl(p):
                miss = req - set(k for k, v in r.items() if v not in (None, ""))
                if miss:
                    fails.append(f"{p.name}: {r.get('id')} missing {sorted(miss)}")
                ids.add(r.get("id"))
    cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
    for p in files or []:
        p = Path(p)
        if p.suffix in (".md", ".json") and p.exists():
            for c in set(cite.findall(_t(p))):
                if c not in ids:
                    fails.append(f"{p.name}: cites {c} but no jsonl row has that id")
    return _res(fails)

def _wp_writes(wp):
    t = _t(WORK / "wp" / f"{wp}.md")
    blk = t.split("Write only:", 1)[1].split("\nDo", 1)[0] if "Write only:" in t else ""
    return [l[2:].split(" (")[0].strip() for l in blk.splitlines() if l.startswith("- ")]

def c18(files, wp=None):
    if not wp:
        return ("PASS", [])
    allowed = _wp_writes(wp); log = WORK / "editlog" / f"{wp}.md"; fails = []
    if log.exists():
        for m in re.findall(r"(?m)^\s*[-*]\s+`?([^`\n]+?\.(?:md|json|jsonl|xlsx|docx|pptx|yaml|sql|svg|excalidraw))`?\s*$", _t(log)):
            if not any(m.replace("\\", "/").startswith(a.rstrip("/")) for a in allowed):
                fails.append(f"{wp}: wrote outside 'Write only': {m}")
    masters = read_json(WORK / "plan" / "legacy_hashes.json", {}) or {}
    for k, h in masters.items():
        p = ROOT / "04 User stories" / k if not k.startswith("04 ") else ROOT / k
        if p.exists() and sha256(p) != h:
            fails.append(f"legacy file changed: {k}")
    return _res(fails)

def c19(files=None):
    fails = []
    for q in sorted((WORK / "wp").glob("queue-*.json")):
        for item in json.loads(q.read_text(encoding="utf-8")):
            for e in item.get("expect", []):
                p = ROOT / e
                if not p.exists():
                    fails.append(f"{item['wp']}: planned output missing: {e}")
                elif p.suffix == ".md" and "editlog" not in e and "fragments" not in e and DEC not in _t(p):
                    fails.append(f"{item['wp']}: {p.name} has no {DEC} change-log row")
    return _res(fails)

def c20(files=None):
    fails = []
    for p in (WORK / "editlog").glob("*.md"):
        if TOOL not in _t(p):
            fails.append(f"{p.name}: tool line missing")
    for p in files or []:
        p = Path(p)
        if p.suffix in (".md", ".json") and p.exists() and re.search(r"Co-Authored-By: Claude|Generated with \[Claude Code\]", _t(p)):
            fails.append(f"{p.name}: wrong tool attribution")
    return _res(fails)

ALL = {f"C{n:02d}": globals()[f"c{n:02d}"] for n in range(1, 21)}

def outputs(stage=None):
    files = []
    for q in sorted((WORK / "wp").glob("queue-*.json")):
        if stage and q.stem != f"queue-{stage}":
            continue
        for item in json.loads(q.read_text(encoding="utf-8")):
            for e in item.get("expect", []):
                p = ROOT / e
                files += [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else ([p] if p.exists() else [])
    if stage in (None, "B"):
        files += [ROOT / x["file"] for x in _plan()["slices"] if (ROOT / x["file"]).exists()]
    return sorted(set(files))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--wp"); ap.add_argument("--quick", action="store_true")
    ap.add_argument("--stage", choices=["B", "C", "D"]); ap.add_argument("--full", action="store_true"); a = ap.parse_args()
    if a.wp:
        files = [ROOT / w for w in _wp_writes(a.wp)]
        files = [f for p in files for f in ([x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]) if f.exists()]
        names, mode = QUICK, f"wp-{a.wp}"
    elif a.stage:
        files, names, mode = outputs(a.stage), STAGES[a.stage], f"stage-{a.stage}"
    else:
        files, names, mode = outputs(), list(ALL), "full"
    res = {}
    for n in names:
        try:
            res[n] = ALL[n](files, wp=a.wp) if n == "C18" else ALL[n](files)
        except Exception as e:
            res[n] = ("FAIL", [f"check crashed: {type(e).__name__}: {e}"])
    ts = time.strftime("%Y%m%d-%H%M%S"); rep = R22 / "checks" / "reports"; rep.mkdir(parents=True, exist_ok=True)
    lines = [f"# Check report {mode} {ts}\n", "| Check | Result | Findings |", "|---|---|---|"]
    lines += [f"| {n} | {r[0]} | {len(r[1])} |" for n, r in res.items()]
    for n, r in res.items():
        if r[1]:
            lines += [f"\n## {n} {r[0]}\n"] + [f"- {x}" for x in r[1]]
    (rep / f"{mode}-{ts}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (rep / f"{mode}-{ts}.json").write_text(json.dumps({n: {"result": r[0], "findings": r[1]} for n, r in res.items()}, indent=1), encoding="utf-8")
    for n, r in res.items():
        print(n, r[0], len(r[1]))
    sys.exit(1 if any(r[0] == "FAIL" for r in res.values()) else 0)

if __name__ == "__main__":
    main()
