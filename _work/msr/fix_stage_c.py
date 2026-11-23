"""Add the unowned E1-056 AC9 and create edit logs for B WPs superseded by B2."""
import json, sys
from pathlib import Path
sys.path.insert(0, r"22 Microservice Realignment/compat")
from common import ROOT, WORK, read_json, write_json

AC9 = '''  Scenario: AC9 The view conformance test has a run book (legacy RWB-E1-056 AC9)
    Given a branch adds column "legacy_bucket" to recovery.v_ace_account with no sys_fields row
    When the pipeline runs CHK-01
    Then CHK-01 fails with "v_ace_account.legacy_bucket has no data dictionary entry"
    Then the merge is blocked
    Then the run book for CHK-01 gives the fix: load the dictionary row through RWB-E1-043 and rerun CHK-01'''

def ac9():
    sid = "RWB-PLT-E1056-OPS"
    plan = read_json(WORK / "plan" / "split_plan.json")
    x = next(s for s in plan["slices"] if s["id"] == sid)
    p = ROOT / x["file"]
    t = p.read_text(encoding="utf-8")
    if "AC9 The view conformance test" not in t:
        i = t.find("Scenario: AC8")
        j = t.find("```", i)
        t = t[:j] + AC9 + "\n" + t[j:]
        p.write_text(t, encoding="utf-8")
        print("AC9 added to", p.name)
    fp = WORK / "fragments" / f"{sid}.json"
    f = json.loads(fp.read_text(encoding="utf-8"))
    if not any(a.get("id") == "AC9" for a in f.get("acs", [])):
        f.setdefault("acs", []).append({"id": "AC9", "origin": "legacy RWB-E1-056 AC9",
                                         "text_first_line": "Scenario: AC9 The view conformance test has a run book (legacy RWB-E1-056 AC9)"})
        fp.write_text(json.dumps(f, ensure_ascii=False, indent=2), encoding="utf-8")
        print("AC9 added to fragment")

def editlogs():
    q = json.loads((WORK / "wp" / "queue-B.json").read_text(encoding="utf-8"))
    n = 0
    for item in q:
        p = WORK / "editlog" / f"{item['wp']}.md"
        if p.exists():
            continue
        files = [e for e in item.get("expect", []) if (ROOT / e).exists() and not e.startswith("_work/msr/editlog/")]
        if not files:
            continue
        body = [f"# Edit log {item['wp']}", "",
                "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash",
                "Decision: D-RCV-60", "",
                "This work package was superseded by the B2 split queue (one legacy key per package).",
                "Its deliverables were written under the B2 work packages; the files are:", ""]
        body += [f"- `{e}`" for e in files]
        body += ["", "No separate B2 edit log is duplicated here; see `_work/msr/editlog/B2-*.md` and the story files above.", ""]
        p.write_text("\n".join(body), encoding="utf-8"); n += 1
    print("edit logs created", n)

if __name__ == "__main__":
    ac9(); editlogs()
