"""Stage C assembler: the only writer of master files (AGENTS.md rule 7)."""
import collections, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, STORIES, SERVICES, OWNER, WT_NAME, header, next_version, read_json, write_json, add_gap, reset_cands, decision
from xlsx_write import write_book
import legacy_index as li
from split_plan import EPIC_NAMES, OUT_DIR

DEC = decision()
TOOL = f"Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision {DEC}."
F3 = "03 Requirements and specifications"

def fr_map(prd_text):
    m = {}
    for line in prd_text.splitlines():
        fr = re.findall(r"\bFR-(?:P10|P[1-9]|S[1-9]|PLT)-\d{3}\b", line)
        if fr:
            for r in re.findall(r"\bREQ-[A-Z]+-\d{3}\b", line):
                m.setdefault(r, [])
                for f in fr:
                    if f not in m[r]:
                        m[r].append(f)
    return m

def prd_value(path, reqs, m):
    frs = sorted({f for r in reqs for f in m.get(r, [])})
    return f"{path} ({', '.join(frs)})" if frs else f"{path} (no FR mapped to {', '.join(reqs) or 'no REQ IDs'})"

def demote(t):
    return re.sub(r"(?m)^(#{1,4}) ", lambda x: "#" * (len(x.group(1)) + 2) + " ", t)

def _prd_path(scope):
    s = next((x for x in SERVICES if x["code"] == scope), None)
    name = f"Recovery Workbench PRD {s['code']} {s['service']} v1.md" if s else "Recovery Workbench PRD PLT Platform v1.md"
    return f"{F3}/PRD/{name}"

def prd_refs(plan):
    reset_cands("C1"); cache = {}; done = 0
    for x in plan["slices"]:
        rel = _prd_path(x["scope"] if x["scope"] != "ITG" else "PLT")
        if rel not in cache:
            p = ROOT / rel
            cache[rel] = fr_map(p.read_text(encoding="utf-8", errors="replace")) if p.exists() else None
        m = cache[rel]
        if m is None:
            val = f"Not specified in the source documents ({add_gap('C1', f'PRD missing: {rel}', 'PRD WP did not produce the file', severity='P2', area='Requirements')})"
        else:
            val = prd_value(rel, x.get("reqs", []), m)
        sp = ROOT / x["file"]; fp = WORK / "fragments" / f"{x['id']}.json"
        if sp.exists():
            t = sp.read_text(encoding="utf-8")
            nt = re.sub(r"(?m)^\|\s*PRD reference\s*\|[^\n]*\|\s*$", f"| PRD reference | {val} |", t, count=1)
            if nt != t:
                sp.write_text(nt, encoding="utf-8"); done += 1
        if fp.exists():
            f = json.loads(fp.read_text(encoding="utf-8")); f["prd_ref"] = val; write_json(fp, f)
    print("C1 PRD references written:", done)

MASTER_STEMS = [("Recovery Workbench User Stories Epic 1", "E1"), ("Recovery Workbench User Stories Epic 2", "E2"),
                ("Recovery Workbench User Stories Epics 3 to 8", "E3-8"), ("Recovery Workbench Technical Enabler Stories", "TE"),
                ("Recovery Workbench Administration Stories", "AD"), ("Recovery Workbench Data Migration Stories", "DM"),
                ("Recovery Workbench ACE Team Stories", "ACE")]

def masters(plan, idx):
    s = {x["id"]: x for x in plan["slices"]}
    for stem, grp in MASTER_STEMS:
        n = next_version(STORIES, stem); out = STORIES / f"{stem} v{n}.md"
        if out.exists():
            print("KEPT", out.name); continue
        t = [f"# {stem} v{n}\n", header(), TOOL,
             f"\nRealigned to the 19-service architecture (Arch v5). Each legacy story below lists its new linked stories; the full text of each new story follows. Release dates are tentative and unchanged.\n"]
        for r in [r for r in idx if r["group"] == grp]:
            lg = plan["legacy"].get(r["key"], {"disposition": "Not found", "slices": []})
            t += [f"\n## {r['key']} {r['title']}\n", f"Legacy disposition: {lg['disposition']}.\n",
                  "| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |", "|---|---|---|---|---|---|"]
            for sid in lg["slices"]:
                x = s[sid]
                t.append(f"| {sid} | {WT_NAME[x['wt']]} | {x['epic']} | {x.get('lane')} | {x['ready']} | {OWNER[x['owner']]} |")
            for sid in lg["slices"]:
                p = ROOT / s[sid]["file"]
                t.append("\n" + (demote(p.read_text(encoding="utf-8")) if p.exists() else f"### {sid}\n\nNot written (see the Tracker WP status).\n"))
        out.write_text("\n".join(t) + "\n", encoding="utf-8"); print("WROTE", out.name)

def catalogue(plan, frags):
    epics = collections.defaultdict(list)
    for x in plan["slices"]:
        epics[x["epic"]].append(x)
    deps = [[x["id"], c, k] for x in plan["slices"] for k in ("H", "C", "I", "X") for c in x[k]]
    write_book(STORIES / "Recovery Workbench Service Story Catalog v1.xlsx", {
        "Epics": (["Epic", "Name", "Stories", "Lanes", "Day-1 stories", "Wave"],
                  [[e, EPIC_NAMES.get(e, e), len(v), len({x.get("lane") for x in v}), sum(1 for x in v if x["ready"] == "Day 1"), min(x["wave"] for x in v)] for e, v in sorted(epics.items())]),
        "Stories": (["Story", "Title", "Work type", "Suggested owner", "Service", "Epic", "Wave", "Business epic", "Release", "Legacy", "Disposition", "Lane", "Ready", "PRD", "File"],
                    [[x["id"], x["title"], WT_NAME[x["wt"]], OWNER[x["owner"]], x["service"], x["epic"], x["wave"], x["business_epic"],
                      (x["release"] + " (tentative)") if x["release"] else "", x["legacy"], x["disposition"], x.get("lane"), x["ready"],
                      frags.get(x["id"], {}).get("prd_ref", ""), x["file"]] for x in plan["slices"]]),
        "Legacy map": (["Legacy key", "Disposition", "New stories"], [[k, v["disposition"], v["slices"]] for k, v in sorted(plan["legacy"].items())]),
        "Dependencies": (["Story", "Depends on", "Class"], deps),
        "Contracts": (["Story", "Operations provided", "Operations consumed", "Events published", "Events consumed", "Workflows"],
                      [[i, f.get("ops_provided"), f.get("ops_consumed"), f.get("events_published"), f.get("events_consumed"), f.get("workflows")] for i, f in sorted(frags.items())]),
    }, read_me=header() + "\nRecovery Workbench Service Story Catalog v1. " + TOOL)
    print("WROTE Service Story Catalog v1.xlsx")

def overviews(plan):
    by = collections.defaultdict(list)
    for x in plan["slices"]:
        by[x["epic"]].append(x)
    for e, v in sorted(by.items()):
        p = ROOT / OUT_DIR / f"{e} {EPIC_NAMES[e]}" / f"{e} Epic Overview v1.md"
        if p.exists():
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        lanes = collections.defaultdict(list)
        for x in v:
            lanes[x.get("lane")].append(x)
        t = [f"# {e} {EPIC_NAMES[e]} - Epic Overview v1\n", header(), TOOL,
             f"\nWave {min(x['wave'] for x in v)}. Stories: {len(v)}. Ownership is suggested only; any team may pick up any story.\n",
             "## Suggested owners\n", "| Team type | Stories |", "|---|---|"]
        t += [f"| {OWNER[o]} | {n} |" for o, n in sorted(collections.Counter(x["owner"] for x in v).items())]
        t += ["\n## Day-1 stories\n"] + [f"- {x['id']} {x['title']}" for x in v if x["ready"] == "Day 1"]
        t += ["\n## Lanes\n", "| Lane | Stories | Ready to start |", "|---|---|---|"]
        t += [f"| {l} | {', '.join(x['id'] for x in xs)} | {'; '.join(sorted({x['ready'] for x in xs}))} |" for l, xs in sorted(lanes.items(), key=lambda kv: str(kv[0]))]
        p.write_text("\n".join(t) + "\n", encoding="utf-8")
    print("WROTE", len(by), "epic overviews")

def day1(plan):
    out = ROOT / "11 Delivery and operations" / "Recovery Workbench Day-1 Work Allocation v1.xlsx"
    sheets = {}
    for team in ("TechX", "ACE", "INFRA", "DEVOPS", "QA"):
        rows = [[x["id"], x["title"], WT_NAME[x["wt"]], x["epic"], x.get("lane"), x["file"]] for x in plan["slices"] if x["owner"] == team and x["ready"] == "Day 1"]
        sheets[team] = (["Story", "Title", "Work type", "Epic", "Lane", "File"], rows)
    write_book(out, sheets, read_me=header() + "\nDay-1 Work Allocation v1. Suggested owners by team type only; no names. " + TOOL)
    print("WROTE Day-1 Work Allocation v1.xlsx")

def main():
    plan = read_json(WORK / "plan" / "split_plan.json"); idx = read_json(WORK / "plan" / "legacy_index.json")
    prd_refs(plan)
    frags = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (WORK / "fragments").glob("*.json")}
    masters(plan, idx); catalogue(plan, frags); overviews(plan); day1(plan)
    print("C OK")

if __name__ == "__main__":
    main()
