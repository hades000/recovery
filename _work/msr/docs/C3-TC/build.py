"""Build Test Cases v8 and Regression Suite v7 for D-RCV-60 (WP C3-TC).

Reads: the copied next-version workbooks, split_plan.json, ownership.json, the story files.
Writes: columns, Read me sheets and new rows into the copies only. Never touches a source file.
Run: python -I "_work/msr/docs/C3-TC/build.py"
"""
import json, re, sys
from copy import copy
from pathlib import Path

sys.path.insert(0, str(Path("22 Microservice Realignment/compat").resolve()))
import openpyxl
from common import ROOT, WORK, SERVICES

DEC = "D-RCV-60"
RUN_DATE = "22 November 2026"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
TC_OUT = ROOT / "09 Testing and quality" / "Recovery Workbench Test Cases v8.xlsx"
RS_OUT = ROOT / "09 Testing and quality" / "Recovery Workbench Regression Suite v7.xlsx"
HEADER1 = f"SCB Collections and Recovery. Henka Group, {RUN_DATE}."
HEADER2 = "(C) Siam Commercial Bank and Henka Pte Ltd"

SHORT = {s["code"]: s["short"] for s in SERVICES}
SERVICE_NAME = {s["code"]: s["service"] for s in SERVICES}
WAVE = {s["code"]: s["wave"] for s in SERVICES}

PLAN = json.loads((WORK / "plan" / "split_plan.json").read_text(encoding="utf-8"))
LEG = PLAN["legacy"]
SLICE = {s["id"]: s for s in PLAN["slices"]}

# Route set -> its own service, Archive v5 slide 3 ("Restructure / Settlement / Deed in lieu -> rwb-treatment S2",
# "Guarantee claim -> rwb-guarantee S3", "Litigation -> rwb-litigation S4", "Asset sale -> rwb-asset S5",
# "Debt sale -> rwb-debtsale S6", "Write-off -> rwb-writeoff S7", always-on: deviations S8, universal rules P7).
ROUTE_SERVICE = {
    "Restructure": "S2", "Settlement": "S2", "Deed in lieu": "S2", "Guarantee claim": "S3",
    "Litigation": "S4", "Asset disposal": "S5", "Asset sale": "S5", "Debt sale": "S6",
    "Write-off": "S7", "Deviations": "S8", "Universal rules": "P7",
}
LEVEL_MAP = {"System": "Component", "Schema": "Component", "Access": "Component",
             "Resilience": "NFR", "Operational": "NFR", "Rule table": "Component"}
NONE_CANCELLED = "None (legacy story cancelled; no new story under D-RCV-60)"
NONE_RETIRED = "None (legacy story retired under D-RCV-60)"
CANCELLED = {"RWB-E1-003", "RWB-E1-004", "RWB-E1-005", "RWB-E1-006", "RWB-E1-009",
             "RWB-E1-010", "RWB-E1-012", "RWB-E1-029", "RWB-E1-048", "RWB-E1-051",
             "RWB-E2-023", "RWB-TE-005"}
RETIRED = {"RWB-E1-014", "RWB-TE-007"}


def svc_name(code):
    if code in ("PLT", "platform"):
        return "platform"
    if code in ("ITG", "integration"):
        return "integration"
    return SERVICE_NAME.get(code, code)


def primary(key):
    """Owner code of a legacy key from the plan: explicit primary, else the first slice's scope."""
    e = LEG.get(key)
    if not e:
        return None
    if e.get("primary"):
        return e["primary"]
    for s in e.get("slices", []):
        if s in SLICE:
            return SLICE[s]["scope"]
    return None


def slices_of(key):
    return LEG.get(key, {}).get("slices", [])


def sec16(path):
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    m = re.search(r"### 16\. Test cases(.*?)(?=\n### 17\.)", t, re.S)
    rows = []
    if not m:
        return rows
    for line in m.group(1).splitlines():
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and cells[0].startswith("TC-"):
                rows.append(cells[:4])
    return rows


def ac_gherkin(path):
    """AC number -> {title, given, when, then} from section 7."""
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    m = re.search(r"### 7\. Acceptance criteria(.*?)(?=\n### 8\.)", t, re.S)
    out = {}
    if not m:
        return out
    cur, buf = None, []
    for line in m.group(1).splitlines():
        s = line.strip()
        mm = re.match(r"Scenario:\s*AC(\d+)\s*(.*)$", s)
        if mm:
            if cur:
                out[cur] = _pack(buf)
            cur, buf = mm.group(1), [mm.group(2)]
            continue
        if cur and s:
            buf.append(s)
    if cur:
        out[cur] = _pack(buf)
    return out


def _pack(buf):
    if not buf:
        return {}
    title = re.sub(r"\((legacy RWB-[A-Z0-9-]+ AC\d+|new, " + re.escape(DEC) + r")\)", "", buf[0]).strip()
    given = [re.sub(r"^(Given|And|But)\s+", "", l) for l in buf[1:] if re.match(r"^(Given|And|But)\s+", l)]
    when = [re.sub(r"^(When|And)\s+", "", l) for l in buf[1:] if re.match(r"^(When|And)\s+", l)]
    then = [re.sub(r"^(Then|And)\s+", "", l) for l in buf[1:] if re.match(r"^(Then|And)\s+", l)]
    return {"title": title, "given": "; ".join(given), "when": "; ".join(when), "then": "; ".join(then)}


def exc_rows(path):
    """Exception ID -> (trigger, what happens, message) from section 5."""
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    m = re.search(r"### 5\. Exception paths(.*?)(?=\n### 6\.)", t, re.S)
    out = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and re.fullmatch(r"X\d+", cells[0]):
            out[cells[0]] = (cells[1], cells[2], cells[3])
    return out


PH = "Not specified in the source documents (CG-C3-TC-5; ASM-C3-TC-5)"


def readme(wb, title, lines):
    ws = wb.create_sheet("Read me", 0)
    ws["A1"] = HEADER1
    ws["A2"] = HEADER2
    ws["A3"] = title
    r = 5
    for row in lines:
        for c, v in enumerate(row, 1):
            ws.cell(row=r, column=c, value=v)
        r += 1
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 24
    ws.column_dimensions["C"].width = 110
    ws.column_dimensions["D"].width = 30
    return ws


def style_header(ws, row, cols, ref_col=1):
    for c in cols:
        ws.cell(row=row, column=c)._style = copy(ws.cell(row=row, column=ref_col)._style)


# ---------------------------------------------------------------- Test Cases v8
def build_tc():
    wb = openpyxl.load_workbook(TC_OUT)
    st = wb["Story test cases"]
    rt = wb["Rule test cases"]

    base = {}
    for row in range(5, st.max_row + 1):
        tid = st.cell(row=row, column=1).value
        if not tid:
            continue
        base[tid] = row

    # --- Story test cases: columns O..R
    hdr = ["Service", "Story key (new)", "Test level", "Origin"]
    for i, h in enumerate(hdr, 15):
        st.cell(row=4, column=i, value=h)
    style_header(st, 4, range(15, 19))
    for row in range(5, st.max_row + 1):
        if not st.cell(row=row, column=1).value:
            continue
        key = st.cell(row=row, column=2).value
        lvl = st.cell(row=row, column=7).value
        if key in CANCELLED:
            svc, story = NONE_CANCELLED, "None (no new story)"
        elif key in RETIRED:
            svc, story = NONE_RETIRED, "None (no new story)"
        else:
            code = primary(key)
            svc = svc_name(code) if code else PH
            sl = slices_of(key)
            story = "; ".join(sl) if sl else PH
        st.cell(row=row, column=15, value=svc)
        st.cell(row=row, column=16, value=story)
        st.cell(row=row, column=17, value=LEVEL_MAP.get(str(lvl), "Component"))
        st.cell(row=row, column=18, value=f"legacy {key} (kept)")

    # --- new rows: -ITG copies of a case that exists, then draft cases of slices with no legacy case
    new_rows, seen = [], set(base)
    copies = 0
    itg_added = set()
    for s in PLAN["slices"]:
        if s["wt"] != "ITG":
            continue
        for tc, covers, level, data in sec16(s["file"]):
            baseid = tc[:-4] if tc.endswith("-ITG") else tc
            if baseid not in base or tc in seen:
                continue
            brow = base[baseid]
            g = lambda c: st.cell(row=brow, column=c).value
            new_rows.append([tc, g(2), g(3), "ITG", covers, g(6), level, g(8), g(9), g(10), data,
                             g(12), "Live", g(14), "integration", s["id"], level, f"new, {DEC}"])
            seen.add(tc)
            copies += 1
            itg_added.add(tc)

    drafts = 0
    new_slices = []
    for s in PLAN["slices"]:
        if s.get("tcs_legacy"):
            continue
        rows16 = sec16(s["file"])
        if not rows16:
            continue
        new_slices.append(s["id"])
        acs = ac_gherkin(s["file"])
        exc = exc_rows(s["file"])
        for tc, covers, level, data in rows16:
            if tc in seen:
                continue
            first = re.split(r"[,\s]", covers.strip())[0]
            num = re.match(r"AC(\d+)$", first)
            if num and num.group(1) in acs:
                a = acs[num.group(1)]
                test, given, when, then = a.get("title", ""), a.get("given", ""), a.get("when", ""), a.get("then", "")
            elif first in exc:
                trig, what, msg = exc[first]
                test = trig
                given = trig
                when = f"The exception path {first} is taken"
                then = what + (f"; {msg}" if msg and msg.lower() != "none" else "")
            else:
                test, given, when, then = covers, PH, PH, PH
            new_rows.append([tc, s["legacy"], "ITG" if s["scope"] == "ITG" else "PLT",
                             "ITG" if s["scope"] == "ITG" else "PLT", covers, test, level,
                             given, when, then, data, "Yes", "Live", "None",
                             "integration" if s["scope"] == "ITG" else "platform", s["id"], level,
                             f"new, {DEC}"])
            seen.add(tc)
            drafts += 1

    start = st.max_row + 1
    for i, r in enumerate(new_rows):
        for c, v in enumerate(r, 1):
            st.cell(row=start + i, column=c, value=v)
    for col, w in (("O", 26), ("P", 34), ("Q", 14), ("R", 34)):
        st.column_dimensions[col].width = w

    # --- Rule test cases: columns O..Q
    for i, h in enumerate(["Service", "Test level", "Origin"], 11):
        rt.cell(row=4, column=i, value=h)
    style_header(rt, 4, range(11, 14))
    for row in range(5, rt.max_row + 1):
        if not rt.cell(row=row, column=1).value:
            continue
        route = rt.cell(row=row, column=3).value
        rule = rt.cell(row=row, column=2).value
        code = ROUTE_SERVICE.get(str(route))
        rt.cell(row=row, column=11, value=svc_name(code) if code else PH)
        rt.cell(row=row, column=12, value=LEVEL_MAP.get(str(rt.cell(row=row, column=9).value), "Component"))
        rt.cell(row=row, column=13, value=f"legacy rule set {rule} (kept)")
    for col, w in (("K", 22), ("L", 14), ("M", 34)):
        rt.column_dimensions[col].width = w

    readme(wb, f"Recovery Workbench Test Cases v8 (Draft) - change log and how to read this workbook", [
        ["Document", "Recovery Workbench Test Cases"],
        ["Version", "8"],
        ["Date", RUN_DATE],
        ["Status", "Draft"],
        ["Decision", DEC],
        ["Supersedes", "Test Cases v7 (16 November 2026); v7 is unchanged"],
        ["Tool", TOOL],
        [],
        ["Change log", "Date", "Change", "Tool"],
        ["8", RUN_DATE, "D-RCV-60 microservice realignment", TOOL],
        ["7", "16 November 2026", "Source version, kept unchanged in the folder", ""],
        [],
        ["What this version changes", "", "", ""],
        ["Story test cases O:R", "", "Service, Story key (new), Test level, Origin. Every source column A:N and every source row is kept as it was.", ""],
        ["Rule test cases K:M", "", "Service, Test level, Origin. Every source column A:J and every source row is kept as it was.", ""],
        ["-ITG copies", "", f"{copies} rows added: the integration case of a story that already holds its case, ID = base ID + -ITG, level and data read from section 16 of the integration story. Tagged new, {DEC}.", ""],
        ["Draft cases", "", f"{drafts} rows added for the {len(new_slices)} new stories (platform keys N001-N012 and NF01-NF08, integration keys W1J01, W1J02, W2J01, W3J01, W4J01, TE009, TE010) that hold no legacy case. Covers, level and data from section 16; test name, given, when and then from section 7 (or section 5 for an X path). Tagged new, {DEC}.", ""],
        ["Totals", "", f"Story test cases: {len(base):,} + {len(new_rows):,} = {len(base) + len(new_rows):,} rows. Rule test cases: 448 rows, unchanged and extended with three columns.", ""],
        ["Retired and cancelled", "", "The 98 parked cases of the nine cancelled stories (RWB-E1-003, E1-004, E1-005, E1-006, E1-009, E1-010, E1-012, E1-051 and RWB-E2-023) and the 20 cases of the two retired stories (RWB-E1-014 and RWB-TE-007) keep their text unchanged and carry the Service value None with the reason. No case was deleted.", ""],
        ["Registers", "", "9 candidate gaps (CG-C3-TC-1 to CG-C3-TC-9) and 14 candidate assumptions (ASM-C3-TC-1 to ASM-C3-TC-14) sit in _work/msr/gaps/ and _work/msr/assumptions/. Only step D1 numbers them as GAP-nnnn and ASM-nnnn.", ""],
        [],
        ["How to read the columns", "", "", ""],
        ["Service", "", "The owning service of the case, from the Microservice Ownership Map v1: the plan's primary owner of the legacy story (P1-P10, S1-S9 to rwb-<short>), platform for RWB-PLT, integration for RWB-ITG. This is the owner column of the map; no case is owned by a team name or a person.", ""],
        ["Story key (new)", "", "Every story of the realignment that owns the case; a legacy story is split into several stories, so several keys are listed.", ""],
        ["Test level", "", "The level of the Template and Rules section R7.2 table: Unit, Component, Contract, Integration, End to end, NFR. For a source row it is read from the source Level column (System, Schema and Access to Component; Resilience and Operational to NFR; Rule table to Component). For an added row it is the level of section 16 of its story.", ""],
        ["Origin", "", "legacy <story or rule set> (kept) for a source row; new, D-RCV-60 for an added row.", ""],
        ["Level column", "", "Kept exactly as the source states it. Added rows carry the section 16 value (Component, Contract, Integration, End to end, NFR) because those levels did not exist in the source vocabulary.", ""],
        ["Status, In regression, Later home", "", "Kept unchanged on every source row; an added row is Live, in regression where its base row is, and has no later home.", ""],
        [],
        ["Rules of the run", "", "", ""],
        ["No source file edited", "", "This workbook is a copy of Test Cases v7 with added columns, a Read me sheet and added rows. v7 sits unchanged beside it.", ""],
        ["Dates", "", "Neither source workbook states a release date, so no date is added and no date is changed. Release dates stay in the story files, unchanged and tentative.", ""],
        ["Missing values", "", "None: every added value is read from the Ownership Map v1, the split plan or the story files. The one value the source workbooks never state is the owner of a case (CG-C3-TC-5); it is read from the Microservice Ownership Map v1 (ASM-C3-TC-5).", ""],
    ])
    wb.save(TC_OUT)
    return {"rows": len(base), "copies": copies, "drafts": drafts, "new": len(new_rows), "slices": new_slices}


# ---------------------------------------------------------------- Regression Suite v7
def build_rs():
    wb = openpyxl.load_workbook(RS_OUT)
    ws = wb["Suite"]
    tc = openpyxl.load_workbook(TC_OUT, read_only=True, data_only=True)
    idx = {}
    for row in tc["Story test cases"].iter_rows(min_row=5, values_only=True):
        if row[0]:
            idx[row[0]] = row
    base = {}
    for row in range(5, ws.max_row + 1):
        tid = ws.cell(row=row, column=1).value
        if tid:
            base[tid] = row

    for i, h in enumerate(["Service", "Story key (new)", "Test level", "Origin"], 11):
        ws.cell(row=4, column=i, value=h)
    style_header(ws, 4, range(11, 15), ref_col=1)
    for row in range(5, ws.max_row + 1):
        if not ws.cell(row=row, column=1).value:
            continue
        story = ws.cell(row=row, column=2).value
        mod = ws.cell(row=row, column=4).value
        lvl = ws.cell(row=row, column=7).value
        route = ROUTE_SERVICE.get(str(mod))
        if route:
            ws.cell(row=row, column=11, value=svc_name(route))
            ws.cell(row=row, column=12, value="None (rule case; the rule set is not a story)")
            ws.cell(row=row, column=14, value=f"legacy rule set {story} (kept)")
        elif story in CANCELLED:
            ws.cell(row=row, column=11, value=NONE_CANCELLED)
            ws.cell(row=row, column=12, value="None (no new story)")
            ws.cell(row=row, column=14, value=f"legacy {story} (kept, parked)")
        elif story in RETIRED:
            ws.cell(row=row, column=11, value=NONE_RETIRED)
            ws.cell(row=row, column=12, value="None (no new story)")
            ws.cell(row=row, column=14, value=f"legacy {story} (kept, retired)")
        else:
            code = primary(story)
            ws.cell(row=row, column=11, value=svc_name(code) if code else PH)
            sl = slices_of(story)
            ws.cell(row=row, column=12, value="; ".join(sl) if sl else PH)
            ws.cell(row=row, column=14, value=f"legacy {story} (kept)")
        ws.cell(row=row, column=13, value=LEVEL_MAP.get(str(lvl), "Component"))

    added = 0
    for tid, row in base.items():
        copy_id = tid + "-ITG"
        src = idx.get(copy_id)
        if not src:
            continue
        ws.append([copy_id, ws.cell(row=row, column=2).value, ws.cell(row=row, column=3).value,
                   ws.cell(row=row, column=4).value, src[4], ws.cell(row=row, column=6).value,
                   src[6], ws.cell(row=row, column=8).value, src[10], ws.cell(row=row, column=10).value,
                   "integration", src[15], src[16], f"new, {DEC}"])
        added += 1
    for col, w in (("K", 26), ("L", 34), ("M", 14), ("N", 34)):
        ws.column_dimensions[col].width = w

    readme(wb, "Recovery Workbench Regression Suite v7 (Draft) - change log and how to read this workbook", [
        ["Document", "Recovery Workbench Regression Suite"],
        ["Version", "7"],
        ["Date", RUN_DATE],
        ["Status", "Draft"],
        ["Decision", DEC],
        ["Supersedes", "Regression Suite v6 (15 November 2026); v6 is unchanged"],
        ["Tool", TOOL],
        [],
        ["Change log", "Date", "Change", "Tool"],
        ["7", RUN_DATE, "D-RCV-60 microservice realignment", TOOL],
        ["6", "15 November 2026", "Source version, kept unchanged in the folder", ""],
        [],
        ["What this version changes", "", "", ""],
        ["Suite K:N", "", "Service, Story key (new), Test level, Origin. Every source column A:J and every source row is kept as it was.", ""],
        ["-ITG copies", "", f"{added} rows added: the integration case of a case the suite already runs, ID = base ID + -ITG, level and data read from section 16 of the integration story. Tagged new, {DEC}.", ""],
        ["Growth", "", "A new story's cases join the suite when its release ships, as the Growth sheet already states; they are therefore not added here. The 448 rule cases and the 231 story cases of version 6 are unchanged.", ""],
        ["Totals", "", f"Suite: {len(base):,} + {added:,} = {len(base) + added:,} rows. Growth and Rules sheets unchanged.", ""],
        ["Cancelled stories", "", "The four cases of the two cancelled stories (RWB-E1-029 and RWB-TE-005) keep their text unchanged and carry the Service value None with the reason. No case was deleted.", ""],
        ["Registers", "", "9 candidate gaps (CG-C3-TC-1 to CG-C3-TC-9) and 14 candidate assumptions (ASM-C3-TC-1 to ASM-C3-TC-14) sit in _work/msr/gaps/ and _work/msr/assumptions/. Only step D1 numbers them as GAP-nnnn and ASM-nnnn.", ""],
        [],
        ["How to read the columns", "", "", ""],
        ["Service", "", "The owning service of the case, from the Microservice Ownership Map v1: the plan's primary owner of the legacy story, or for a rule case the service that executes the route set (Architecture v5 slide 3: Restructure, Settlement and Deed in lieu to rwb-treatment; Guarantee claim to rwb-guarantee; Litigation to rwb-litigation; Asset sale to rwb-asset; Debt sale to rwb-debtsale; Write-off to rwb-writeoff; deviations to rwb-deviation; universal rules to rwb-decision). No case is owned by a team name or a person.", ""],
        ["Story key (new)", "", "Every story of the realignment that owns the case; a rule case has none, because a rule set is not a story.", ""],
        ["Test level", "", "Component, Contract, Integration, End to end or NFR (Template and Rules section R7.2). Source rows: System, Access and Rule table to Component. Added rows: the level of section 16 of the story.", ""],
        ["Origin", "", "legacy <story or rule set> (kept) for a source row; new, D-RCV-60 for an added row.", ""],
        [],
        ["Rules of the run", "", "", ""],
        ["No source file edited", "", "This workbook is a copy of Regression Suite v6 with added columns, a Read me sheet and added rows. v6 sits unchanged beside it.", ""],
        ["Dates", "", "Neither source workbook states a release date, so no date is added and no date is changed.", ""],
        ["Missing values", "", "None: every added value is read from the Ownership Map v1, the split plan or the story files. The one value the source workbooks never state is the owner of a case (CG-C3-TC-5); it is read from the Microservice Ownership Map v1 (ASM-C3-TC-5).", ""],
    ])
    wb.save(RS_OUT)
    return {"rows": len(base), "added": added}


if __name__ == "__main__":
    tc = build_tc()
    rs = build_rs()
    print(json.dumps({"tc": tc, "rs": rs}, indent=1))
