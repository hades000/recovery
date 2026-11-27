"""Tests for rulings.py (capture and apply) on a small synthetic ROOT. Run: python -I test_rulings.py"""
import json, shutil, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rulings  # noqa: E402

STORY = "04 User stories/Demo/Demo story v1.md"   # name does not match a story key: no re-check runs
TEXT = ("# Demo story v1\n\n**Change log.** D-RCV-60, 22 November 2026: first version.\n\n"
        "BR1 uses Physical Schema v6 for the index.\n"
        "BR2 keys on primary_customer_id.\n"
        "BR3 old wording here.\n")


def jl(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


class RulingsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root, self.run = self.tmp / "root", self.tmp / "run"
        (self.root / STORY).parent.mkdir(parents=True)
        (self.root / STORY).write_text(TEXT, encoding="utf-8")
        for k in ("gapreg", "asmreg"):
            p = self.root / rulings.rwbsrc.TEXT[k]
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("", encoding="utf-8")
        g = lambda i, **kw: {"id": i, "title": f"title {i}", "severity": "P2", "check": "X1", "story": "DEMO",
                             "description": "d", "evidence": "e", "owner_role": "Business analyst",
                             "proposed": "p", **kw}
        jl(self.run / "1-check/gaps.jsonl", [g("CG-1"), g("CG-2"), g("CG-3")])
        jl(self.run / "1-check/assumptions.jsonl", [{"id": "ASM-X-1", "text": "t", "story": "DEMO", "gap": "CG-3"}])
        jl(self.run / "2-fixes/stories/disposition.jsonl", [
            {"id": "CG-1", "status": "FIXED", "fixes": ["F-001"]},
            {"id": "CG-2", "status": "FIXED", "fixes": ["F-002"]},
            {"id": "CG-3", "status": "HELD", "fixes": [], "detail": "needs a ruling"}])
        jl(self.run / "2-fixes/stories/held.jsonl", [
            {"story": "DEMO", "file": STORY, "line": 5, "text": "BR1 uses Physical Schema v6 for the index.",
             "reason": "no v7 file", "pairs": [["Physical Schema v6", "Physical Schema v7"]]}])
        jl(self.run / "3-merged/fixes.jsonl", [
            {"fix_id": "S-F-001", "finding": "CG-1", "file": STORY, "op": "replace", "old": "old wording",
             "new": "new wording"},
            {"fix_id": "S-F-002", "finding": "CG-2", "file": STORY, "op": "replace", "old": "BR2 keys",
             "new": "BR2 joins"}])

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def capture(self):
        out = self.tmp / "rulings-v1.xlsx"
        rulings.main(["capture", "--root", str(self.root), "--run", str(self.run), "--out", str(out)])
        return out

    def fill(self, path, decisions):
        import openpyxl
        wb = openpyxl.load_workbook(path)
        ws = wb["Rulings"]
        ci = {c.value: i + 1 for i, c in enumerate(ws[1])}
        for r in range(2, ws.max_row + 1):
            d = decisions.get(ws.cell(r, ci["Item ID"]).value)
            for k, v in (d or {}).items():
                ws.cell(r, ci[k], value=v)
        p = self.tmp / "filled.xlsx"
        wb.save(p)
        return p

    def apply(self, filled):
        out = self.tmp / "apply"
        rulings.main(["apply", "--root", str(self.root), "--run", str(self.run), "--rulings", str(filled),
                      "--out", str(out)])
        return out

    def test_capture_rows_and_prefill(self):
        rows = rulings.read_rulings(self.capture())
        by = {r["Item ID"]: r for r in rows}
        self.assertEqual(set(by), {"CG-1", "CG-2", "CG-3", "ASM-X-1", "HELD-DEMO-L5"})
        self.assertEqual(by["CG-1"]["Decision"], "Accept proposed")
        self.assertEqual(by["CG-1"]["Fix IDs"], "S-F-001")
        self.assertEqual(by["CG-3"]["Decision"], "")
        self.assertEqual(by["HELD-DEMO-L5"]["Fix IDs"], "held:1")

    def test_capture_never_overwrites(self):
        out = self.capture()
        with self.assertRaises(SystemExit):
            rulings.main(["capture", "--root", str(self.root), "--run", str(self.run), "--out", str(out)])

    def test_apply_decisions(self):
        role = "Decided by (role)"
        filled = self.fill(self.capture(), {
            "CG-2": {"Decision": "Not an issue", role: "Solution architect"},           # drops S-F-002
            "HELD-DEMO-L5": {"Decision": "Accept proposed", role: "Data architect"},   # builds the held fix
            "CG-3": {"Decision": "Use my value", role: "Data architect", "File": STORY,
                     "Current text": "primary_customer_id", "Your value or wording": "primary_person_key"},
            "ASM-X-1": {"Decision": "Accept assumption", role: "Business analyst"}})
        out = self.apply(filled)
        new = (out / "3-applied/04 User stories/Demo/Demo story v2.md").read_text(encoding="utf-8")
        self.assertIn("new wording", new)              # CG-1 kept (prefilled)
        self.assertIn("BR2 keys", new)                 # CG-2 dropped
        self.assertIn("Physical Schema v7", new)       # held line accepted
        self.assertIn("primary_person_key", new)       # your value
        self.assertIn("Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.", new)
        self.assertEqual((self.root / STORY).read_text(encoding="utf-8"), TEXT)  # ROOT untouched
        st = {r["item"]: r["new_status"] for r in rulings.load(out / "2-fixes/register_updates.jsonl")}
        self.assertEqual(st, {"CG-1": "Resolved", "CG-2": "Closed (not an issue)", "CG-3": "Resolved",
                              "HELD-DEMO-L5": "Resolved", "ASM-X-1": "Confirmed"})

    def test_bad_rows_are_reported_not_guessed(self):
        role = "Decided by (role)"
        filled = self.fill(self.capture(), {
            "CG-3": {"Decision": "Use my value", role: "QA", "File": STORY, "Current text": "not in the file",
                     "Your value or wording": "x"},
            "ASM-X-1": {"Decision": "Use my value", role: "QA"},                     # no value
            "CG-2": {"Decision": "Use my value", role: "QA", "Your value or wording": "joins on the key"}})
        out = self.apply(filled)
        probs = {p["item"]: p for p in rulings.load(out / "1-rulings-check.jsonl")}
        self.assertIn("CG-3", probs)
        self.assertIn("ASM-X-1", probs)
        st = {r["item"]: r["new_status"] for r in rulings.load(out / "2-fixes/register_updates.jsonl")}
        self.assertTrue(st["CG-3"].startswith("Open (ruling not applied"))
        self.assertEqual(st["CG-2"], "Ruled; wording pending (model pass)")
        wording = rulings.load(out / "2-fixes/needs_wording.jsonl")
        self.assertEqual([w["item"] for w in wording], ["CG-2"])
        new = (out / "3-applied/04 User stories/Demo/Demo story v2.md").read_text(encoding="utf-8")
        self.assertIn("BR2 keys", new)                 # the prepared CG-2 fix was replaced by the ruling, not applied

    def test_review_parsing(self):
        md = ("## R2. Definition of ready\n\n| # | Item | Result | Evidence | Gap |\n|---|---|---|---|---|\n"
              "| 1 | Story | Pass | ok | - |\n| 5 | States | Fail | bad | CG-9 |\n\n"
              "## R5. Missing acceptance criteria\n\n**AC7 — 409 carries its message (proposed).** text\n"
              "```gherkin\nScenario: AC7\n  Given x\n```\n\n"
              "## R6. Open questions\n\n| # | Question | Owner role | Blocks build | Links |\n|---|---|---|---|---|\n"
              "| Q1 | Which one? | Solution architect | Yes | CG-9 |\n")
        rdir = self.tmp / "review"
        (rdir / "review").mkdir(parents=True)
        (rdir / "review/RWB-X-1-APP.md").write_text(md, encoding="utf-8")
        cap = rulings.Capture(self.root, self.run, [rdir], "none")
        cap.review_rows(rdir)
        ids = set(cap.items)
        self.assertEqual(ids, {"DOR-RWB-X-1-APP-5", "NEWAC-RWB-X-1-APP-AC7", "Q-RWB-X-1-APP-Q1"})
        self.assertIn("Given x", cap.items["NEWAC-RWB-X-1-APP-AC7"]["Proposed fix"])
        self.assertEqual(cap.items["Q-RWB-X-1-APP-Q1"]["Severity"], "P1")


if __name__ == "__main__":
    unittest.main()
