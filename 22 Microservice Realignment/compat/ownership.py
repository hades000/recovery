"""Ownership Map: skeleton from the sources -> 3 agent WPs decide owners by R-PREC -> merge + validate + xlsx."""
import argparse, collections, json, re, sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R22, WORK, SERVICES, latest_path, read_json, write_json, header, append_jsonl, decision
from xlsx_write import write_book

DEC = decision()

CODES = [s["code"] for s in SERVICES] + ["PLT"]
DEFAULT_RULINGS = [  # R-PREC default rulings (Appendix R §R3); each is also an assumption
    ("parameters and reference data (E1-042, E1-043)", "P3"), ("case list API", "P3"),
    ("rule package registry", "P7"), ("interaction ledger", "P1"), ("feature flags", "PLT")]

def _sql_tables():
    p = latest_path(ROOT / "06 Data", "Recovery Workbench Physical Schema", ".sql")
    if p is None:
        d = latest_path(ROOT / "06 Data", "Recovery Workbench Physical Schema", "dir")
        p = next(iter(sorted(d.rglob("*.sql")))) if d else None
    txt = p.read_text(encoding="utf-8", errors="ignore") if p else ""
    return sorted(set(re.findall(r"(?i)create\s+table\s+(?:if\s+not\s+exists\s+)?(?:\"?recovery\"?\.)?\"?(\w+)\"?", txt))), (str(p.relative_to(ROOT)) if p else None)

def _api_ops():
    ops = []
    for p in sorted(ROOT.joinpath("05 Technical architecture").rglob("*.yaml")):
        if "API Specification" not in str(p):
            continue
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8", errors="ignore")) or {}
        except Exception:
            continue
        for path, item in (d.get("paths") or {}).items():
            for m, op in (item or {}).items():
                if isinstance(op, dict) and m.lower() in ("get", "post", "put", "patch", "delete"):
                    ops.append({"method": m.upper(), "path": path, "operationId": op.get("operationId"),
                                "x_module": op.get("x-module") or item.get("x-module"), "file": str(p.relative_to(ROOT))})
    return ops

def _ids(rx):
    found = collections.Counter()
    for p in (WORK / "extract").rglob("*.md"):
        found.update(re.findall(rx, p.read_text(encoding="utf-8", errors="ignore")))
    return sorted(found)

def skeleton():
    tables, schema_file = _sql_tables()
    idx = read_json(WORK / "plan" / "legacy_index.json", [])
    hint = collections.defaultdict(collections.Counter)
    masters = {}
    for r in idx:
        if not r.get("master") or not r.get("module"):
            continue
        if r["master"] not in masters:
            masters[r["master"]] = (ROOT / "04 User stories" / r["master"]).read_text(encoding="utf-8", errors="ignore")
    text_by_module = collections.defaultdict(str)
    for r in idx:
        if r.get("master") and r.get("module"):
            t = masters[r["master"]]; i = t.find(r["key"]); text_by_module[r["module"]] += t[i:i + r["chars"]]
    for t in tables:
        rx = re.compile(r"\b" + re.escape(t) + r"\b")
        for mod, txt in text_by_module.items():
            n = len(rx.findall(txt))
            if n:
                hint[t][mod] = n
    sk = {"schema_file": schema_file,
          "tables": [{"table": t, "hint": dict(hint[t].most_common(3))} for t in tables],
          "api": _api_ops(), "events": _ids(r"\bEV-\d{2,3}\b"), "jobs": _ids(r"\bJOB-\d{2,3}\b"),
          "workflows": _ids(r"\b[A-Z][A-Za-z]+Workflow\b"), "rulings": DEFAULT_RULINGS}
    write_json(WORK / "plan" / "ownership_skeleton.json", sk)
    print(f"SKELETON tables={len(tables)} api_ops={len(sk['api'])} events={len(sk['events'])} jobs={len(sk['jobs'])} workflows={len(sk['workflows'])}")

WP_TEXT = """# WP A6-{part} — Ownership Map part: {part}
Tool rules: AGENTS.md (root) rules 1-14. Agent: aisdlc-msr-worker. fanout: 0
Read only:
- _work/msr/plan/ownership_skeleton.json (section "{key}")
- 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (catalogue slides 14-20 and 41-44 win over narrative slides)
- 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
- _work/msr/extract/ (FSD v6 and TSD v5 module files, Event and Messaging, Batch and Scheduling, Physical Schema)
- The R-PREC precedence and default rulings in 2026-11-22-recovery-microservice-realignment-implementation-plan.md Appendix R §R3
Write only: _work/msr/plan/ownership_part_{part}.json ; _work/msr/gaps/A6-{part}.jsonl ; _work/msr/assumptions/A6-{part}.jsonl ; _work/msr/editlog/A6-{part}.md
Do: for EVERY item in the skeleton section, choose exactly one owner from {codes}. Use R-PREC order. The "hint" counts are which legacy module stories mention the table (a hint, not a rule).
Output JSON: {{"{key}": [{{"id": "<table | METHOD path | EV-nn | JOB-nn | Workflow>", "owner": "<code>", "basis": "<source file + slide/section>", "ruling": "<text or empty>", "asm": "<ASM-A6-{part}-n or empty>"}}]}}
Every ruling (two sources disagree) also gets a gap row (type Conflict, severity P2) and an assumption row.
Jobs: also give "replacement": "Temporal Schedule <name> in <service>" or "event-started workflow" (v5 slide 44); Quartz is retired.
Finish: every skeleton item appears once in your output. Write the edit log with tool line T3 Code / OpenCode / DeepSeek v4.1 Flash.
"""

def wps():
    parts = {"tables": "tables", "api": "api", "flows": "events, jobs, workflows"}
    q = []
    for part, key in parts.items():
        f = WORK / "wp" / f"A6-{part}.md"
        f.write_text(WP_TEXT.format(part=part, key=key, codes=", ".join(CODES)), encoding="utf-8")
        q.append({"wp": f"A6-{part}", "agent": "aisdlc-msr-worker", "file": str(f.relative_to(ROOT)), "fanout": False,
                  "expect": [f"_work/msr/plan/ownership_part_{part}.json"]})
    write_json(WORK / "wp" / "queue-A6.json", q)
    print("WPS A6 written: 3")

def merge():
    sk = read_json(WORK / "plan" / "ownership_skeleton.json")
    om = {"tables": {}, "api": {}, "events": {}, "jobs": {}, "workflows": {}, "rulings": []}
    for part in ("tables", "api", "flows"):
        d = read_json(WORK / "plan" / f"ownership_part_{part}.json", {}) or {}
        for key, rows in d.items():
            for r in rows if isinstance(rows, list) else []:
                k = key if key in om else ("events" if str(r.get("id", "")).startswith("EV-") else "jobs" if str(r.get("id", "")).startswith("JOB-") else "workflows")
                om[k][r["id"]] = r
                if r.get("ruling"):
                    om["rulings"].append([r["id"], r["owner"], r["ruling"], r.get("asm", "")])
    bad = []
    for t in sk["tables"]:
        o = om["tables"].get(t["table"], {}).get("owner")
        if o not in CODES:
            hint = max(t["hint"], key=t["hint"].get) if t["hint"] else "P3"
            om["tables"][t["table"]] = {"id": t["table"], "owner": hint, "basis": "fallback: most frequent legacy module", "ruling": "", "asm": "ASM-A6-fallback"}
            bad.append(t["table"])
    if bad:
        append_jsonl(WORK / "assumptions" / "A6-merge.jsonl", {"id": "ASM-A6-merge-1", "text": f"{len(bad)} tables had no agent owner; owner set to the most frequent legacy module: {', '.join(bad[:40])}", "why": "agent output missing", "read": "ownership_skeleton.json", "confidence": "Low"})
    for name, owner in DEFAULT_RULINGS:
        om["rulings"].append([name, owner, "R-PREC default ruling", "ASM-seed"])
    write_json(WORK / "plan" / "ownership.json", om)
    fk = fk_cuts(om)
    s = {s_["code"]: s_ for s_ in SERVICES}
    write_book(R22 / "Recovery Workbench Microservice Ownership Map v1.xlsx", {
        "Services": (["Code", "Service", "Name", "Wave", "Schema", "REST base", "Topic", "Queue"], [[x["code"], x["service"], x["name"], x["wave"], x["schema"], x["base"], x["topic"], x["queue"]] for x in SERVICES]),
        "Tables": (["Table", "Owner", "Schema", "Basis", "Ruling", "Assumption"], [[k, v["owner"], s[v["owner"]]["schema"] if v["owner"] in s else "platform", v.get("basis"), v.get("ruling"), v.get("asm")] for k, v in sorted(om["tables"].items())]),
        "FK cuts": (["From table", "From owner", "To table", "To owner", "Becomes"], fk),
        "Endpoints": (["Operation", "Owner", "Basis", "Ruling"], [[k, v["owner"], v.get("basis"), v.get("ruling")] for k, v in sorted(om["api"].items())]),
        "Events": (["Event", "Owner", "Basis", "Ruling"], [[k, v["owner"], v.get("basis"), v.get("ruling")] for k, v in sorted(om["events"].items())]),
        "Workflows and activities": (["Workflow", "Owner", "Basis"], [[k, v["owner"], v.get("basis")] for k, v in sorted(om["workflows"].items())]),
        "Jobs": (["Job", "Owner", "Replacement", "Basis"], [[k, v["owner"], v.get("replacement"), v.get("basis")] for k, v in sorted(om["jobs"].items())]),
        "Parameters": (["Item", "Owner", "Note"], [["parameters", "P3", "rwb-case contract RWB-P3-E1042-CON"], ["reference data", "P3", "rwb-case contract RWB-P3-E1043-CON"]]),
        "Rulings": (["Item", "Owner", "Ruling", "Assumption"], om["rulings"]),
    }, read_me=header() + f"\nRecovery Workbench Microservice Ownership Map v1 ({DEC}). Generated by compat/ownership.py merge.\nTool: T3 Code / OpenCode / DeepSeek v4.1 Flash.")
    print(f"MERGE OK tables={len(om['tables'])} api={len(om['api'])} events={len(om['events'])} jobs={len(om['jobs'])} fallback={len(bad)} fk_cuts={len(fk)}")

def fk_cuts(om):
    sk = read_json(WORK / "plan" / "ownership_skeleton.json")
    p = ROOT / sk["schema_file"] if sk.get("schema_file") else None
    txt = p.read_text(encoding="utf-8", errors="ignore") if p and p.exists() else ""
    rows = []
    for m in re.finditer(r"(?is)create\s+table\s+(?:if\s+not\s+exists\s+)?(?:\"?recovery\"?\.)?\"?(\w+)\"?\s*\((.*?)\n\);", txt):
        src = m.group(1)
        for tgt in re.findall(r"(?i)references\s+(?:\"?recovery\"?\.)?\"?(\w+)", m.group(2)):
            a = om["tables"].get(src, {}).get("owner"); b = om["tables"].get(tgt, {}).get("owner")
            if a and b and a != b:
                rows.append([src, a, tgt, b, "plain uuid column; integrity through the owner's contract"])
    return rows

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["skeleton", "wps", "merge"]); a = ap.parse_args()
    {"skeleton": skeleton, "wps": wps, "merge": merge}[a.cmd]()
