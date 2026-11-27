"""Rulings workbook for the build-readiness pipeline (sandbox prototype, D-RCV-60).

Two steps around one Excel workbook that a person fills in:

  capture  Collect every open item of one pipeline run into a rulings workbook, one row per item:
           script gaps and assumptions (1-check), held and wording-only fixes (2-fixes), Decision Log
           rows, open register gaps and assumptions the stories cite or should cite, and, where a model
           review was run (--review <dir>), its readiness items, AC review, missing ACs, open questions,
           story defects, gaps and assumptions. Rows the scripts can already fix carry their fix IDs.

  apply    Read the filled workbook and turn each decision into work:
             Accept proposed   the ready fix is kept (or built, for a held line)
             Use my value      replace 'Current text' with 'Your value or wording' in 'File'
             Accept / Reject assumption, Not an issue, Deferred   register status only, no document edit
           Rows that need new wording (an AC, a rule, a rewritten sentence with no exact current text)
           go to needs_wording.jsonl for the model pass; nothing is invented. The fixes are applied as
           next-version copies (apply_fixes.py) and the produced stories are checked again (detcheck.py).
           Register status changes are written as proposals (register_updates.*): only step D1 changes
           the registers (AGENTS.md rule 7).

Usage:
  python -I rulings.py capture --root <ROOT> --run <pipeline out> [--review <dir> ...]
                               [--registers cited|all|none] --out <rulings-v1.xlsx>
  python -I rulings.py apply   --root <ROOT> --run <pipeline out> --rulings <filled.xlsx> --out <dir>
                               [--jobs 8] [--wp RUL] [--date "26 November 2026"] [--dry-run]
Writes only the given --out (outside ROOT for apply). Never overwrites a file.
"""
import argparse, json, re, subprocess, sys, time
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rwbsrc  # noqa: E402

TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
CELL_MAX = 32000

COLS = ["Ruling ID", "Kind", "Item ID", "Story", "Severity", "Check", "Title", "Detail", "Evidence",
        "Owner role", "Pipeline status", "Proposed fix", "File", "Current text", "Decision",
        "Your value or wording", "Decided by (role)", "Ruling source", "Notes", "Fix IDs"]
EDITABLE = ["File", "Current text", "Decision", "Your value or wording", "Decided by (role)", "Ruling source",
            "Notes"]
DECISIONS = ["Accept proposed", "Use my value", "Accept assumption", "Reject assumption", "Not an issue",
             "Deferred"]
REG_STATUS = {"Accept proposed": "Resolved", "Use my value": "Resolved", "Accept assumption": "Confirmed",
              "Reject assumption": "Rejected", "Not an issue": "Closed (not an issue)"}
SEV_ORDER = {"P1": 0, "P2": 1, "P3": 2}
KIND_ORDER = ["Script gap", "Model gap", "Readiness item", "AC review", "Missing AC", "Open question",
              "Story defect", "Held line", "Decision Log", "Script assumption", "Model assumption",
              "Register gap", "Register assumption"]


def load(p):
    p = Path(p)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def clip(s):
    s = "" if s is None else str(s)
    return s if len(s) <= CELL_MAX else s[:CELL_MAX - 40] + " ... [cut; full text in the source]"


def rel_to_root(root, p):
    p = Path(p)
    try:
        return p.resolve().relative_to(root).as_posix()
    except ValueError:
        return str(p)


# ---------------------------------------------------------------- capture
class Capture:
    def __init__(self, root, run, reviews, registers):
        self.root, self.run, self.reviews, self.reg_mode = root, run, reviews, registers
        self.items = OrderedDict()   # item id -> row dict
        self.src = rwbsrc.Sources(root, run / "_cache")

    def add(self, iid, **kw):
        if iid in self.items:  # one row per item: merge the stories that raise it
            r = self.items[iid]
            st = [s for s in r["Story"].split("; ") if s]
            for s in kw.get("Story", "").split("; "):
                if s and s not in st:
                    st.append(s)
            r["Story"] = "; ".join(st)
            return r
        r = {c: "" for c in COLS}
        r.update(kw)
        r["Item ID"] = iid
        self.items[iid] = r
        return r

    def script_rows(self):
        disp = {d["id"]: d for d in load(self.run / "2-fixes/stories/disposition.jsonl")}
        sfix = load(self.run / "2-fixes/stories/fixes.jsonl")
        held = load(self.run / "2-fixes/stories/held.jsonl")
        x20_by_story = {}
        for f in sfix:
            m = re.match(r"X20 (\S+)$", f.get("finding", ""))
            if m:
                x20_by_story.setdefault(m.group(1), []).append("S-" + f["fix_id"])
        held_by_story = Counter(h["story"] for h in held)
        for g in load(self.run / "1-check/gaps.jsonl"):
            d = disp.get(g["id"])
            if d:
                status = {"FIXED": "Fixed by script", "PARTLY FIXED": "Partly fixed", "HELD": "Held",
                          "WORDING": "Needs wording"}.get(d["status"], d["status"])
                fixes = sorted({"S-" + x for x in d.get("fixes", [])})
                note = d.get("detail", "")
            elif g.get("check") == "X20" and not disp:
                fixes = x20_by_story.get(g.get("story", ""), [])
                h = held_by_story.get(g.get("story", ""), 0)
                status = ("Partly fixed" if fixes and h else "Fixed by script" if fixes else
                          "Held" if h else "Open")
                note = f"{len(fixes)} line fix(es); {h} line(s) held (see Held line rows)" if fixes or h else ""
            else:
                status, fixes, note = "Open", [], ""
            self.add(g["id"], Kind="Script gap", Story=g.get("story", ""), Severity=g.get("severity", ""),
                     Check=g.get("check", ""), Title=g.get("title", ""), Detail=g.get("description", ""),
                     Evidence=g.get("evidence", ""), **{"Owner role": g.get("owner_role", ""),
                     "Pipeline status": status, "Proposed fix": g.get("proposed", ""),
                     "Fix IDs": ", ".join(fixes), "Notes": note,
                     "Decision": "Accept proposed" if status in ("Fixed by script", "Partly fixed") else ""})
        for a in load(self.run / "1-check/assumptions.jsonl"):
            self.add(a["id"], Kind="Script assumption", Story=a.get("story", ""), Severity="",
                     Check="", Title=a.get("text", ""), Detail=a.get("why", ""), Evidence=a.get("read", ""),
                     **{"Owner role": "", "Pipeline status": "Open",
                        "Proposed fix": a.get("confirm", ""), "Notes": f"gap {a.get('gap', '')}; applied in "
                                                                       f"{a.get('applied_in', '')}"})
        by_line = OrderedDict()  # one row per held line: a line held for two pairs is one ruling
        for i, h in enumerate(held, 1):
            by_line.setdefault((h["file"], h["line"]), []).append((i, h))
        for (file, line), hs in by_line.items():
            h = hs[0][1]
            pairs = "; ".join(f"{a} -> {b}" for _, x in hs for a, b in x.get("pairs", []))
            self.add(f"HELD-{h['story']}-L{line}", Kind="Held line", Story=h["story"], Severity="P3", Check="X20",
                     Title=f"Version reference held: {pairs}",
                     Detail="; ".join(dict.fromkeys(x.get("reason", "") for _, x in hs)), Evidence="",
                     **{"Owner role": "Business analyst", "Pipeline status": "Held",
                        "Proposed fix": f"Replace {pairs} on line {line}", "File": file,
                        "Current text": h.get("text", ""), "Fix IDs": ", ".join(f"held:{i}" for i, _ in hs)})

    def declog_rows(self):
        dfix = load(self.run / "2-fixes/declog/fixes.jsonl")
        for g in load(self.run / "2-fixes/declog/gaps.jsonl"):
            fixes = ["D-" + f["fix_id"] for f in dfix if g["id"] in f.get("finding", "")]
            self.add(g["id"], Kind="Decision Log", Story=g.get("story", ""), Severity=g.get("severity", ""),
                     Check=g.get("check", ""), Title=g.get("title", ""), Detail=g.get("description", ""),
                     Evidence=g.get("evidence", ""), **{"Owner role": g.get("owner_role", ""),
                     "Pipeline status": "Fixed by script" if fixes else "Open",
                     "Proposed fix": g.get("proposed", ""), "Fix IDs": ", ".join(fixes),
                     "Decision": "Accept proposed" if fixes else ""})

    def register_rows(self):
        if self.reg_mode == "none":
            return
        gaps, asms = self.src.register("gapreg"), self.src.register("asmreg")
        report = {}
        rp = self.run / "1-check/report.json"
        if rp.exists():
            report = json.loads(rp.read_text(encoding="utf-8")).get("stories", {})
        want = OrderedDict()  # register id -> (stories, why)
        if self.reg_mode == "all":
            for i in list(gaps) + list(asms):
                want[i] = ([], "open in the register")
        for key, s in report.items():
            ids = []
            try:
                ids = re.findall(r"\b(?:GAP|ASM)-\d{4}\b", Path(s["file"]).read_text(encoding="utf-8",
                                                                                     errors="replace"))
            except OSError:
                pass
            for i in dict.fromkeys(ids):
                want.setdefault(i, ([], "cited by the story"))[0].append(key)
            for u in s.get("uncited_register_gaps", []):
                i = u.split(" ", 1)[0]
                want.setdefault(i, ([], "open, names this story's legacy key or objects, not cited"))[0].append(key)
            for dl in s.get("open_dl", []):
                for i in re.findall(r"ASM-\d{4}", dl):
                    want.setdefault(i, ([], f"assumption of open decision {dl.split(' ', 1)[0]}"))[0].append(key)
        for i, (stories, why) in want.items():
            if i.startswith("GAP-"):
                r = gaps.get(i)
                if not r or r.get("Status", "Open") not in ("Open", ""):
                    continue
                self.add(i, Kind="Register gap", Story="; ".join(stories), Severity=r.get("Severity", ""),
                         Check="", Title=r.get("Title", ""), Detail=r.get("Description", ""),
                         Evidence=r.get("Evidence", ""), **{"Owner role": r.get("Owner role", ""),
                         "Pipeline status": "Open (register)", "Proposed fix": r.get("Proposed resolution", ""),
                         "Notes": why})
            else:
                r = asms.get(i)
                if not r or r.get("Status", "Unconfirmed") not in ("Unconfirmed", ""):
                    continue
                self.add(i, Kind="Register assumption", Story="; ".join(stories), Severity="", Check="",
                         Title=r.get("Assumption", ""), Detail=r.get("Why", ""), Evidence=r.get("What was read", ""),
                         **{"Owner role": "", "Pipeline status": "Unconfirmed (register)",
                            "Proposed fix": r.get("How to confirm", ""),
                            "Notes": f"{why}; impact if wrong: {r.get('Impact if wrong', '')}"})

    # ---- model review
    @staticmethod
    def review_blocks(text):
        """Yield (section number, heading, header, rows) for each table, and ('5', heading, None, (id, title,
        gherkin)) for each bold 'ACn' paragraph followed by a gherkin block."""
        sec, head, block, lines = "", "", [], text.splitlines()
        i = 0
        def table(b):
            rows = [r for r in (rwbsrc.split_row(l) for l in b) if r is not None]
            rows = [r for r in rows if not all(re.fullmatch(r":?-{3,}:?", c or "---") for c in r)]
            return (rows[0], rows[1:]) if rows else (None, [])
        while i < len(lines):
            l = lines[i]
            if l.lstrip().startswith("|"):
                block.append(l)
                i += 1
                continue
            if block:
                h, rows = table(block)
                if h:
                    yield sec, head, h, rows
                block = []
            m = re.match(r"^(#{2,4})\s+(.*)", l)
            if m:
                head = m.group(2).strip()
                mr = re.match(r"R(\d)", head)
                if mr and len(m.group(1)) == 2:
                    sec = mr.group(1)
            mb = re.match(r"^\*\*(AC\d+)\s*[—–-]\s*(.*?)\*\*(.*)", l)
            if sec == "5" and mb:
                j = i + 1
                while j < len(lines) and not lines[j].startswith("```"):
                    j += 1
                k = j + 1
                while k < len(lines) and not lines[k].startswith("```"):
                    k += 1
                if j < len(lines):
                    yield sec, head, None, (mb.group(1), mb.group(2) + mb.group(3), "\n".join(lines[j + 1:k]))
                    i = k + 1
                    continue
            i += 1
        if block:
            h, rows = table(block)
            if h:
                yield sec, head, h, rows

    def review_rows(self, rdir):
        rdir = Path(rdir)
        cg_story = {}
        for f in sorted((rdir / "review").glob("*.md")):
            story = f.stem
            text = f.read_text(encoding="utf-8", errors="replace")
            for cg in re.findall(r"CG-[\w-]+?-\d{3}\b", text):
                cg_story.setdefault(cg, [])
                if story not in cg_story[cg]:
                    cg_story[cg].append(story)
            for sec, head, hdr, rows in self.review_blocks(text):
                if hdr is None:  # bold missing-AC paragraph
                    ac, title, g = rows
                    self.add(f"NEWAC-{story}-{ac}", Kind="Missing AC", Story=story, Severity="", Check="R5",
                             Title=f"{ac} {title}".strip(), Detail="", Evidence="",
                             **{"Pipeline status": "Needs wording", "Proposed fix": g})
                    continue
                d = lambda r: dict(zip(hdr, r + [""] * (len(hdr) - len(r))))
                col = lambda row, *names: next((row[h] for h in hdr if any(n in h for n in names) and row.get(h)), "")
                for r in rows:
                    row = d(r)
                    first = r[0] if r else ""
                    if sec == "2" and "Result" in " ".join(hdr):
                        res = col(row, "Result")
                        if res.strip("* ").lower().startswith("pass"):
                            continue
                        self.add(f"DOR-{story}-{first}", Kind="Readiness item", Story=story,
                                 Severity="P1" if res.strip("* ").lower().startswith("fail") else "P2", Check="R2",
                                 Title=f"Definition of Ready item {first} {col(row, 'Item')}: {res}",
                                 Detail=col(row, "Evidence"), Evidence="",
                                 **{"Pipeline status": "Open", "Notes": f"gaps: {col(row, 'Gap')}"})
                    elif sec == "3" and first.startswith("DEF-"):
                        fixed = col(row, "Fixed", "fix")
                        if fixed.strip("* ").lower().startswith("yes"):
                            continue
                        self.add(re.match(r"DEF-\d+", first).group(0), Kind="Story defect", Story=story, Severity="", Check="R3",
                                 Title=col(row, "contradicts", "Defect"), Detail=fixed, Evidence="",
                                 **{"Pipeline status": "Open", "Notes": f"step {col(row, 'Section', 'Step')}"})
                    elif sec == "4" and first.startswith("AC"):
                        ac = first.split()[0]
                        self.add(f"ACR-{story}-{ac}", Kind="AC review", Story=story, Severity="", Check="R4",
                                 Title=f"{first}", Detail=col(row, "Problem"), Evidence="",
                                 **{"Pipeline status": "Needs wording",
                                    "Proposed fix": col(row, "Improved").replace("<br>", "\n")})
                    elif sec == "5" and first.startswith("AC"):
                        self.add(f"NEWAC-{story}-{first}", Kind="Missing AC", Story=story, Severity="",
                                 Check="R5", Title=f"{first}: {col(row, 'Covers')}",
                                 Detail=f"proposed test: {col(row, 'TC')}", Evidence="",
                                 **{"Pipeline status": "Needs wording",
                                    "Proposed fix": col(row, "Gherkin").replace("<br>", "\n")})
                    elif sec == "6" and first and "Question" in hdr:
                        blocks = col(row, "Blocks")
                        self.add(f"Q-{story}-{first}", Kind="Open question", Story=story,
                                 Severity="P1" if blocks.lower().startswith("yes") else "P2", Check="R6",
                                 Title=col(row, "Question"), Detail="", Evidence=col(row, "Links"),
                                 **{"Owner role": col(row, "Owner"), "Pipeline status": "Open",
                                    "Notes": f"blocks build: {blocks}"})
        for g in load(rdir / "gaps.jsonl"):
            self.add(g["id"], Kind="Model gap", Story="; ".join(cg_story.get(g["id"], [])),
                     Severity=g.get("severity", ""), Check="model", Title=g.get("title", ""),
                     Detail=g.get("description", ""), Evidence=g.get("evidence", ""),
                     **{"Owner role": g.get("owner_role", ""), "Pipeline status": "Open",
                        "Proposed fix": g.get("proposed", "")})
        for a in load(rdir / "assumptions.jsonl"):
            self.add(a["id"], Kind="Model assumption", Story="; ".join(cg_story.get(a.get("gap", ""), [])),
                     Severity="", Check="model", Title=a.get("text", ""), Detail=a.get("why", ""),
                     Evidence=a.get("read", ""), **{"Pipeline status": "Open", "Proposed fix": a.get("confirm", ""),
                                                    "Notes": f"gap {a.get('gap', '')}; applied in "
                                                             f"{a.get('applied_in', '')}"})

    def build(self):
        self.script_rows()
        self.declog_rows()
        for r in self.reviews:
            self.review_rows(r)
        self.register_rows()
        rows = list(self.items.values())
        ko = {k: i for i, k in enumerate(KIND_ORDER)}
        rows.sort(key=lambda r: (SEV_ORDER.get(r["Severity"], 3), ko.get(r["Kind"], 99), r["Story"], r["Item ID"]))
        for n, r in enumerate(rows, 1):
            r["Ruling ID"] = f"R-{n:05d}"
        return rows


def write_workbook(rows, out, meta):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
    wb = openpyxl.Workbook()
    rm = wb.active
    rm.title = "Read me"
    text = [
        "Recovery Workbench rulings workbook. Decision D-RCV-60.",
        f"Tool: {TOOL}.",
        f"Captured from pipeline run: {meta['run']}" + (f"; model reviews: {meta['reviews']}" if meta['reviews'] else
                                                       "; no model review (script items and registers only)"),
        "",
        "How to fill it in (sheet Rulings, the yellow columns only):",
        "1. Decision: pick one value from the list. Leave it empty if you have not decided; an empty row is skipped.",
        "   Accept proposed   - keep the fix the scripts prepared, or the proposed resolution as the wording to use.",
        "   Use my value      - put the value or wording in 'Your value or wording'. For an exact edit also give",
        "                       'File' (ROOT-relative) and 'Current text' (copied character for character).",
        "   Accept assumption / Reject assumption - for assumption rows.",
        "   Not an issue      - closes the item; a prepared fix for it is dropped.",
        "   Deferred          - stays open; a prepared fix for it is dropped this round.",
        "2. Decided by (role): a role, never a person's name (AGENTS.md rule 4).",
        "3. Ruling source: where the answer comes from (document, decision ID, workshop and date).",
        "4. Do not change the Ruling ID, Item ID or Fix IDs columns; apply matches rows on them.",
        "",
        "Rows that need new wording (missing ACs, AC rewrites, rules) are not invented by the scripts: apply",
        "lists them in needs_wording.jsonl for the model pass, with your value.",
        "Register gaps and assumptions are listed for a ruling; their status change is a proposal for step D1.",
    ]
    for i, t in enumerate(text, 1):
        rm.cell(row=i, column=1, value=t)
    rm.column_dimensions["A"].width = 120
    ws = wb.create_sheet("Rulings")
    ws.append(COLS)
    for r in rows:
        ws.append([clip(r[c]) for c in COLS])
    bold, yellow = Font(bold=True), PatternFill("solid", fgColor="FFF2CC")
    widths = {"Ruling ID": 10, "Kind": 16, "Item ID": 24, "Story": 22, "Severity": 8, "Check": 7, "Title": 50,
              "Detail": 60, "Evidence": 40, "Owner role": 18, "Pipeline status": 16, "Proposed fix": 50,
              "File": 40, "Current text": 40, "Decision": 18, "Your value or wording": 50,
              "Decided by (role)": 20, "Ruling source": 30, "Notes": 30, "Fix IDs": 20}
    from openpyxl.utils import get_column_letter
    for i, c in enumerate(COLS, 1):
        cell = ws.cell(row=1, column=i)
        cell.font = bold
        if c in EDITABLE:
            cell.fill = yellow
        ws.column_dimensions[get_column_letter(i)].width = widths.get(c, 20)
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLS))}{len(rows) + 1}"
    dv = DataValidation(type="list", formula1='"' + ",".join(DECISIONS) + '"', allow_blank=True)
    dcol = get_column_letter(COLS.index("Decision") + 1)
    dv.add(f"{dcol}2:{dcol}{max(len(rows) + 1, 2)}")
    ws.add_data_validation(dv)
    sm = wb.create_sheet("Summary")
    sm.append(["Kind", "P1", "P2", "P3", "Other", "Total", "Ready fix", "Needs wording"])
    for k in KIND_ORDER:
        ks = [r for r in rows if r["Kind"] == k]
        if not ks:
            continue
        c = Counter(r["Severity"] if r["Severity"] in SEV_ORDER else "Other" for r in ks)
        sm.append([k, c["P1"], c["P2"], c["P3"], c["Other"], len(ks),
                   sum(1 for r in ks if r["Fix IDs"]), sum(1 for r in ks if r["Pipeline status"] == "Needs wording")])
    sm.append(["All", *[sum(1 for r in rows if (r["Severity"] if r["Severity"] in SEV_ORDER else "Other") == s)
                        for s in ("P1", "P2", "P3", "Other")], len(rows),
               sum(1 for r in rows if r["Fix IDs"]), sum(1 for r in rows if r["Pipeline status"] == "Needs wording")])
    for c in sm[1]:
        c.font = bold
    sm.column_dimensions["A"].width = 22
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)


def cmd_capture(a):
    root, run, out = Path(a.root).resolve(), Path(a.run).resolve(), Path(a.out).resolve()
    if out.exists():
        sys.exit(f"{out} exists (never overwrite; use the next version)")
    if not (run / "1-check/gaps.jsonl").exists():
        sys.exit(f"{run} is not a pipeline run folder (no 1-check/gaps.jsonl)")
    cap = Capture(root, run, [Path(r).resolve() for r in a.review], a.registers)
    rows = cap.build()
    write_workbook(rows, out, {"run": str(run), "reviews": ", ".join(a.review)})
    c = Counter(r["Kind"] for r in rows)
    print(f"{len(rows)} items -> {out}: " + ", ".join(f"{k} {c[k]}" for k in KIND_ORDER if c[k]))
    return 0


# ---------------------------------------------------------------- apply
def read_rulings(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    if "Rulings" not in wb.sheetnames:
        sys.exit("no sheet Rulings in the workbook")
    it = wb["Rulings"].iter_rows(values_only=True)
    hdr = [str(h or "") for h in next(it)]
    missing = [c for c in ("Ruling ID", "Item ID", "Decision", "Fix IDs") if c not in hdr]
    if missing:
        sys.exit(f"Rulings sheet lacks columns {missing}")
    rows = []
    for v in it:
        r = {h: ("" if x is None else str(x)) for h, x in zip(hdr, v)}
        if r.get("Ruling ID"):
            rows.append(r)
    return rows


def run_step(step, args, log):
    t0 = time.time()
    r = subprocess.run([sys.executable, "-I", str(HERE / step), *map(str, args)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    last = (r.stdout.strip().splitlines() or [""])[-1]
    log.append(f"{step}: rc {r.returncode}, {time.time() - t0:.1f} s: {last}")
    print(log[-1], flush=True)
    if r.returncode not in (0, 1):
        sys.exit(f"{step} failed (rc {r.returncode}):\n{r.stderr[-2000:]}")
    return r


def cmd_apply(a):
    from apply_fixes import apply_text, FixError
    root, run, out = Path(a.root).resolve(), Path(a.run).resolve(), Path(a.out).resolve()
    if out == root or root in out.parents:
        sys.exit("--out must be outside ROOT (sandbox only)")
    if out.exists() and any(out.iterdir()):
        sys.exit(f"--out {out} is not empty (never overwrite a run)")
    rows = read_rulings(a.rulings)
    merged = {f["fix_id"]: f for f in load(run / "3-merged/fixes.jsonl")}
    held = load(run / "2-fixes/stories/held.jsonl")
    log, problems = [], []
    out.mkdir(parents=True, exist_ok=True)
    # 1. check the rulings
    ok_rows = []
    for r in rows:
        d = r.get("Decision", "").strip()
        if not d:
            continue
        why = []
        if d not in DECISIONS:
            why.append(f"decision {d!r} is not one of the list")
        if d == "Use my value" and not r.get("Your value or wording", "").strip():
            why.append("'Use my value' with no value")
        if d in ("Accept assumption", "Reject assumption") and "assumption" not in r.get("Kind", "").lower():
            why.append(f"'{d}' on a {r.get('Kind', '')} row")
        if not r.get("Decided by (role)", "").strip() and not (d == "Accept proposed" and r.get("Fix IDs")):
            why.append("no 'Decided by (role)'")
        if why:
            problems.append({"ruling": r["Ruling ID"], "item": r["Item ID"], "problem": "; ".join(why),
                             "treated_as": "Deferred"})
            r["Decision"] = "Deferred"
        ok_rows.append(r)
    # 2. fixes
    keep_auto, drop_auto = set(), set()
    ruling_fixes, wording, reg = [], [], []
    story_idx = None
    for r in ok_rows:
        d, ids = r["Decision"], [x.strip() for x in r.get("Fix IDs", "").split(",") if x.strip()]
        auto = [x for x in ids if x in merged]
        if d == "Accept proposed":
            keep_auto.update(auto)
            hs = [held[int(x[5:]) - 1] for x in ids if x.startswith("held:")]
            if hs:
                ruling_fixes.append((r, {"fix_id": f"R-{r['Ruling ID']}", "finding": r["Item ID"],
                                         "file": hs[0]["file"], "op": "held-line", "line": hs[0]["line"],
                                         "pairs": [p for h in hs for p in h["pairs"]],
                                         "source": r.get("Ruling source", "")}))
            if not ids:
                wording.append(r)
        else:
            drop_auto.update(auto)
        if d == "Use my value":
            f, cur = r.get("File", "").strip(), r.get("Current text", "")
            if not f and r.get("Story", "") and "; " not in r["Story"] and cur:
                if story_idx is None:
                    story_idx = rwbsrc.Sources(root, run / "_cache").story_index()
                p = story_idx.get(r["Story"])
                f = rel_to_root(root, p) if p else ""
            if f and cur:
                ruling_fixes.append((r, {"fix_id": f"R-{r['Ruling ID']}", "finding": r["Item ID"], "file": f,
                                         "op": "replace", "old": cur, "new": r["Your value or wording"],
                                         "count": max(1, (root / f).read_text(encoding="utf-8").count(cur))
                                         if (root / f).suffix == ".md" and (root / f).exists() else 1,
                                         "source": r.get("Ruling source", "")}))
            else:
                wording.append(r)
        if d in REG_STATUS or d == "Deferred":
            reg.append(r)
    conflict = keep_auto & drop_auto
    keep_auto -= drop_auto
    for x in sorted(conflict):
        problems.append({"ruling": "", "item": x, "problem": "one row accepts this fix and another drops it",
                         "treated_as": "dropped"})
    # unlinked fixes (version stamps, change-log cells) follow the other fixes of their file
    linked = {x.strip() for r in rows for x in r.get("Fix IDs", "").split(",") if x.strip()}
    kept_files = {merged[x]["file"] for x in keep_auto}
    final = [f for k, f in merged.items() if k in keep_auto or (k not in linked and f["file"] in kept_files)]
    # held lines -> exact replace of the current line
    built, failed = [], set()
    for r, fx in ruling_fixes:
        if fx["op"] == "held-line":
            try:
                lines = (root / fx["file"]).read_text(encoding="utf-8").split("\n")
                old = lines[fx["line"] - 1]
                new = old
                for p_old, p_new in fx["pairs"]:
                    new = new.replace(p_old, p_new)
                if new == old:
                    raise ValueError("the pair is no longer on that line")
                fx = {k: v for k, v in fx.items() if k not in ("line", "pairs")}
                fx.update(op="replace", old=old, new=new, count=sum(1 for l in lines if l == old))
            except (OSError, IndexError, ValueError) as e:
                failed.add(r["Ruling ID"])
                problems.append({"ruling": r["Ruling ID"], "item": r["Item ID"], "problem": f"held line: {e}",
                                 "treated_as": "not applied"})
                continue
        built.append((r, fx))
    # pre-check every ruling text fix on top of the automatic fixes of its file
    work = {}
    for f in final:
        if f["op"] in ("replace", "delete_line", "insert_after"):
            t = work.get(f["file"])
            if t is None:
                t = (root / f["file"]).read_text(encoding="utf-8")
            try:
                work[f["file"]] = apply_text(t, f)
            except FixError as e:  # apply_fixes reports it FAILED for the whole file
                problems.append({"ruling": "", "item": f["fix_id"], "problem": f"prepared fix no longer applies: {e}",
                                 "treated_as": "FAILED in apply"})
    for r, fx in built:
        p = root / fx["file"]
        if p.suffix.lower() != ".md" or not p.exists():
            problems.append({"ruling": r["Ruling ID"], "item": r["Item ID"],
                             "problem": f"file is not a markdown file in ROOT: {fx['file']}",
                             "treated_as": "needs wording"})
            wording.append(r)
            continue
        t = work.get(fx["file"]) or p.read_text(encoding="utf-8")
        try:
            work[fx["file"]] = apply_text(t, fx)
            final.append(fx)
        except FixError as e:
            failed.add(r["Ruling ID"])
            problems.append({"ruling": r["Ruling ID"], "item": r["Item ID"],
                             "problem": f"current text does not match {fx['file']} after the automatic fixes: {e}",
                             "treated_as": "not applied; copy 'Current text' again, character for character"})
    (out / "2-fixes").mkdir(parents=True)
    with (out / "2-fixes/fixes.jsonl").open("w", encoding="utf-8") as fh:
        for f in final:
            fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    with (out / "2-fixes/needs_wording.jsonl").open("w", encoding="utf-8") as fh:
        for r in wording:
            fh.write(json.dumps({"ruling": r["Ruling ID"], "item": r["Item ID"], "kind": r.get("Kind", ""),
                                 "story": r.get("Story", ""), "title": r.get("Title", ""),
                                 "decision": r["Decision"], "value": r.get("Your value or wording", ""),
                                 "proposed": r.get("Proposed fix", ""), "decided_by": r.get("Decided by (role)", ""),
                                 "source": r.get("Ruling source", "")}, ensure_ascii=False) + "\n")
    (out / "1-rulings-check.jsonl").write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in problems),
                                               encoding="utf-8")
    # 3. apply and 4. re-check
    rc_rows = None
    res = []
    if final:
        run_step("apply_fixes.py", ["--root", root, "--fixes", out / "2-fixes/fixes.jsonl", "--out", out / "3-applied",
                                    "--date", a.date, "--note", "fixes from the rulings workbook",
                                    *(["--dry-run"] if a.dry_run else [])], log)
        res = load(out / "3-applied/apply_result.jsonl")
        produced = {r["file"]: out / "3-applied" / Path(r["file"]).parent / r["to"] for r in res
                    if r["status"] == "APPLIED"}
        stories = sorted(str(p) for p in produced.values() if p.suffix == ".md" and rwbsrc.story_key_from_name(p.name))
        if stories and not a.dry_run:
            overrides = [f"{k}={produced[v]}" for k, v in rwbsrc.SOURCES.items() if v in produced]
            lst = out / "4-recheck/stories.txt"
            lst.parent.mkdir(parents=True, exist_ok=True)
            lst.write_text("\n".join(stories) + "\n", encoding="utf-8")
            run_step("detcheck.py", ["--root", root, "--cache", run / "_cache", "--out", out / "4-recheck/stories",
                                     "--wp", f"{a.wp}-RE", "--story-list", lst, "--jobs", a.jobs,
                                     *[x for o in overrides for x in ("--source", o)]], log)
            rc_rows = load(out / "4-recheck/stories/gaps.jsonl")
    # register status proposals, from what was actually applied
    status_of = {x["fix_id"]: x["status"] for x in res}
    wset = {r["Ruling ID"] for r in wording}
    kept = {f["fix_id"] for f in final}
    sc = Counter()
    with (out / "2-fixes/register_updates.jsonl").open("w", encoding="utf-8") as fh:
        for r in reg:
            d = r["Decision"]
            if d == "Deferred":
                st = "Open (deferred)"
            elif d in ("Accept assumption", "Reject assumption", "Not an issue"):
                st = REG_STATUS[d]
            elif r["Ruling ID"] in failed:
                st = "Open (ruling not applied: see 1-rulings-check.jsonl)"
            elif r["Ruling ID"] in wset:
                st = "Ruled; wording pending (model pass)"
            else:
                ids = [x.strip() for x in r.get("Fix IDs", "").split(",") if x.strip() in kept]
                ids += [f"R-{r['Ruling ID']}"] if f"R-{r['Ruling ID']}" in kept else []
                if not ids:
                    st = "Open (no fix kept)"
                elif a.dry_run:
                    st = "Resolved (dry run, not applied)"
                elif all(status_of.get(x) == "APPLIED" for x in ids):
                    st = "Partly resolved" if r.get("Pipeline status") == "Partly fixed" else "Resolved"
                else:
                    st = "Open (fix FAILED in apply: see 3-applied/apply_log.md)"
            sc[st.split(" (")[0].split(";")[0]] += 1
            fh.write(json.dumps({"item": r["Item ID"], "kind": r.get("Kind", ""), "new_status": st,
                                 "ruling": r["Ruling ID"], "decided_by": r.get("Decided by (role)", ""),
                                 "source": r.get("Ruling source", ""), "value": r.get("Your value or wording", ""),
                                 "note": "proposal for step D1; the register is not edited here"},
                                ensure_ascii=False) + "\n")
    # summary
    dc = Counter(r["Decision"] for r in ok_rows)
    applied = sum(r["status"] == "APPLIED" for r in res)
    lines = [f"# Rulings apply ({a.wp})", "", f"Tool: {TOOL}. Decision D-RCV-60. Rulings: {a.rulings}. "
             f"Run: {run}.{' Dry run.' if a.dry_run else ''}", "",
             "| Step | Result |", "|---|---|",
             f"| Rulings read | {len(rows)} rows; {len(ok_rows)} decided: "
             + ", ".join(f"{k} {v}" for k, v in sorted(dc.items())) + " |",
             f"| Rulings problems | {len(problems)} (1-rulings-check.jsonl) |",
             f"| Fixes | {len(final)} ({len([f for f in final if not f['fix_id'].startswith('R-')])} prepared by the "
             f"scripts, {len([f for f in final if f['fix_id'].startswith('R-')])} from your values) |",
             f"| Needs wording (model pass) | {len(wording)} (2-fixes/needs_wording.jsonl) |",
             f"| Status proposals | {len(reg)}: " + ", ".join(f"{k} {v}" for k, v in sorted(sc.items()))
             + " (2-fixes/register_updates.jsonl, for step D1) |",
             f"| Applied | {applied} of {len(res)} fixes over {len({r['file'] for r in res})} files |"]
    if rc_rows is not None:
        lines.append(f"| Re-check of the produced stories | {len(rc_rows)} rows |")
    if problems:
        lines += ["", "## Rulings problems", "", "| Ruling | Item | Problem | Treated as |", "|---|---|---|---|"]
        lines += [f"| {p['ruling']} | {p['item']} | {p['problem'][:200]} | {p['treated_as']} |" for p in problems]
    lines += ["", "## Log", ""] + [f"- {l}" for l in log]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"done -> {out / 'summary.md'}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("capture")
    c.add_argument("--root", required=True)
    c.add_argument("--run", required=True)
    c.add_argument("--review", action="append", default=[])
    c.add_argument("--registers", choices=["cited", "all", "none"], default="cited")
    c.add_argument("--out", required=True)
    p = sub.add_parser("apply")
    p.add_argument("--root", required=True)
    p.add_argument("--run", required=True)
    p.add_argument("--rulings", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--jobs", type=int, default=1)
    p.add_argument("--wp", default="RUL")
    p.add_argument("--date", default="26 November 2026")
    p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    return cmd_capture(a) if a.cmd == "capture" else cmd_apply(a)


if __name__ == "__main__":
    sys.exit(main())
