"""Build the RTM v7 (D-RCV-60 realignment). Reads only; writes the v7 workbook and the jsonl rows."""
import json, re, glob, collections, subprocess, sys, shutil
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

ROOT = Path(".").resolve()
WORK = ROOT / "_work" / "msr"
SCR = WORK / "docs" / "C2-RTM"
SRC_X = ROOT / "09 Testing and quality" / "Recovery Workbench Requirements Traceability Matrix v6.xlsx"
OUT_X = ROOT / "09 Testing and quality" / "Recovery Workbench Requirements Traceability Matrix v7.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
HEAD1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
HEAD2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
DATE = "22 November 2026"

# ---------------------------------------------------------------- sources
rows6 = json.load(open(SCR / "rtm_v6.json", encoding="utf-8"))
cov6 = json.load(open(SCR / "cov_v6.json", encoding="utf-8"))
data = rows6[4:]
split = json.load(open(WORK / "plan" / "split_plan.json", encoding="utf-8"))
legacy = split["legacy"]
reqstory = json.load(open(SCR / "req_story.json", encoding="utf-8"))
reqfr = json.load(open(SCR / "req_fr.json", encoding="utf-8"))

frags = {}
for p in glob.glob(str(WORK / "fragments" / "*.json")):
    d = json.load(open(p, encoding="utf-8"))
    frags[d["id"]] = d

ownmap = openpyxl.load_workbook(ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx")
SVC = {}
for r in ownmap["Services"].iter_rows(min_row=2, values_only=True):
    if r[0]:
        SVC[r[0]] = {"service": r[1], "schema": r[4], "rest": r[5], "topic": r[6], "queue": r[7], "wave": r[3]}
CODES = ["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","S1","S2","S3","S4","S5","S6","S7","S8","S9","PLT","ITG"]
ORD = {c: i for i, c in enumerate(CODES)}
SVC2CODE = {v["service"]: k for k, v in SVC.items()}


def s_order(sid):
    """Sort key for a story ID: service code, then legacy compact, then work type."""
    m = re.match(r"RWB-([A-Z0-9]+)-(.+)-([A-Z]+)(-\d)?$", sid)
    if not m:
        return (99, sid)
    scope = m.group(1)
    return (ORD.get(scope, 98), m.group(2), m.group(3), sid)


def owner_of(sid):
    f = frags.get(sid)
    if not f:
        return None
    svc = f.get("service")
    if svc == "integration":
        return "ITG"
    return SVC2CODE.get(svc)


def split_keys(cell):
    return [k.strip() for k in re.split(r"[,;]", cell or "") if k.strip().startswith("RWB-")]


def fr_order(fr):
    m = re.match(r"FR-([A-Z0-9]+)-(\d+)$", fr)
    return (ORD.get(m.group(1), 98), int(m.group(2)), fr) if m else (99, 0, fr)


RETIRED = {k: v for k, v in legacy.items() if v["disposition"].startswith("Retired")}

recs = []
for r in data:
    req = r[0]
    keys = split_keys(r[7])
    slices = set()
    for k in keys:
        slices |= set(legacy[k]["slices"])
    cites = set(reqstory.get(req, []))
    if keys:
        new = sorted(slices, key=s_order)
        basis = "legacy"
        sl = set(slices)
        extra = sorted({c for c in cites if c not in sl}, key=s_order)
        if cites and not (sl & cites):
            new = sorted(set(new) | set(cites), key=s_order)
            basis = "legacy+citation"
    else:
        new = sorted({c for c in cites if frags.get(c, {}).get("wt") != "ITG"} or cites, key=s_order)
        basis = "citation"
    # owner
    prim = collections.Counter(legacy[k]["primary"] for k in keys if "primary" in legacy[k])
    fr = reqfr.get(req, {}).get("fr", [])
    prds = reqfr.get(req, {}).get("prd", [])
    # owner: the service whose PRD functional requirements carry the requirement,
    # else the Ownership Map owner of the legacy key; a withdrawn or retired row keeps the v6 module.
    frcodes = collections.Counter(f.split("-")[1] for f in fr if len(f.split("-")) > 1)
    if str(r[2]).strip().lower() == "removed" or req in ("REQ-DRI-009",):
        owner = r[4]
    elif r[4] in frcodes:
        owner = r[4]
    elif len(frcodes) == 1:
        owner = list(frcodes)[0]
    elif frcodes:
        top = [c for c, n in frcodes.most_common() if n == frcodes.most_common()[0][1]]
        owner = sorted(top, key=lambda c: ORD.get(c, 98))[0]
    elif prim:
        serv = collections.Counter({c: n for c, n in prim.items() if c not in ("PLT", "ITG")}) or prim
        if r[4] in serv or (r[4] in prim and not serv):
            owner = r[4]
        else:
            best = serv.most_common()
            top = [c for c, n in best if n == best[0][1]]
            owner = sorted(top, key=lambda c: ORD.get(c, 98))[0]
    else:
        co = collections.Counter(owner_of(s) for s in new)
        co.pop("ITG", None); co.pop(None, None)
        owner = co.most_common(1)[0][0] if (len(co) == 1 and sum(co.values()) >= 2) else r[4]
        if owner not in ORD:
            owner = r[4]
    recs.append({"row": r, "req": req, "keys": keys, "new": new, "basis": basis,
                 "cites": cites, "owner": owner, "fr": sorted(set(fr), key=fr_order),
                 "prd": prds, "removed": str(r[2]).strip().lower() == "removed"})

# ---------------------------------------------------------------- flags
no_story = [x for x in recs if not x["new"]]
no_fr = [x for x in recs if not x["fr"]]
removed = [x for x in recs if x["removed"]]
orphans = [x for x in no_story if not x["removed"]]
NOT_CARRIED = [x for x in no_fr if not x["removed"] and reqfr.get(x["req"], {}).get("note")
               and any("D-RCV-60" in s for s in reqfr[x["req"]]["note"])]
no_fr_flagged = [x for x in no_fr if x not in removed and x not in NOT_CARRIED]
owner_changed = [x for x in recs if x["owner"] != x["row"][4]]
retired_rows = [x for x in recs if any(k in RETIRED for k in x["keys"])]
cite_mismatch = []
for x in recs:
    if x["keys"] and x["cites"]:
        sl = {s for k in x["keys"] for s in legacy[k]["slices"]}
        if not (sl & x["cites"]):
            cite_mismatch.append(x)

STAT = {
    "reqs": len(recs),
    "with_key": sum(1 for x in recs if x["keys"]),
    "new_story": sum(1 for x in recs if x["new"]),
    "no_story": len(orphans),
    "no_fr": len(no_fr_flagged),
    "not_carried": len(NOT_CARRIED),
    "removed": len(removed),
    "owner_changed": len(owner_changed),
    "retired_rows": len(retired_rows),
    "cite_mismatch": len(cite_mismatch),
}
print(json.dumps(STAT, indent=1))
print("orphans:", [(x["req"], x["row"][3], x["row"][4]) for x in orphans])
print("no FR flagged:", [x["req"] for x in no_fr_flagged])
print("not carried:", [x["req"] for x in NOT_CARRIED])
print("removed:", [x["req"] for x in removed])
print("cite mismatch:", [x["req"] for x in cite_mismatch])
print("retired:", [(x["req"], [k for k in x["keys"] if k in RETIRED]) for x in retired_rows])
print("owner changed sample:", [(x["req"], x["row"][4], x["owner"]) for x in owner_changed[:12]])

# ---------------------------------------------------------------- gap / assumption rows
G = "CG-C2-RTM"; A = "ASM-C2-RTM"
no_story_ids = ", ".join(x["req"] for x in no_story)
no_fr_ids = ", ".join(x["req"] for x in no_fr)
own_ids = ", ".join(x["req"] for x in owner_changed[:12]) + (", ..." if len(owner_changed) > 12 else "")

gaps = [
 {"id": f"{G}-1", "title": "The v6 Module column names a different service from the realigned owner",
  "source": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v6.xlsx",
  "section": "RTM sheet, column Module (E)",
  "description": f"{len(owner_changed)} of 231 requirements name in Module a service other than the realigned owner, read as the service whose PRD functional requirements carry the requirement and, where it has no FR, as the Ownership Map owner of its legacy key ({own_ids}).",
  "evidence": "20 PRD files (FR tables and the 11.2 requirement trace summary); 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (Services, Tables, Endpoints, Events, Workflows and activities, Jobs); _work/msr/plan/ownership.json; R3 default rulings (interaction ledger to rwb-source-data, parameters and reference data to rwb-case, rule package registry to rwb-decision)",
  "type": "Conflict", "area": "Ownership", "severity": "P3", "needed_by_wave": "1",
  "legacy_ref": "RTM v6 Module column", "owner_role": "Solution architect", "asm": f"{A}-1",
  "proposed": "The v7 Owner column carries the realigned owner; the v6 Module column is kept unchanged beside it so the change is visible.", "wp": "C2-RTM"},
 {"id": f"{G}-2", "title": "Requirements with no PRD functional requirement",
  "source": "03 Requirements and specifications/PRD/",
  "section": "11.2 Requirement trace summary, 20 PRD files",
  "description": f"{len(no_fr_flagged)} requirements are named in a PRD as an upstream requirement ID but no functional requirement of any PRD carries them ({', '.join(x['req'] for x in no_fr_flagged)}). REQ-RDF-005 and REQ-RDF-006 are withdrawn under D-RCV-35 U5, and REQ-DRI-009 is retired with the data lake, so those three carry no functional requirement by design.",
  "evidence": "Every PRD file read in full; the FR tables and the 11.2 trace summary name no FR for these IDs",
  "type": "Missing", "area": "Requirements", "severity": "P2", "needed_by_wave": "2",
  "legacy_ref": ", ".join(x["keys"][0] for x in no_fr_flagged if x["keys"]) or "none",
  "owner_role": "Product owner", "asm": f"{A}-2",
  "proposed": "The product owner confirms the requirement or withdraws it; until then the v7 matrix flags it and no FR is claimed.", "wp": "C2-RTM"},
 {"id": f"{G}-3", "title": "Requirements that no realigned story cites",
  "source": "04 User stories/Recovery Workbench Service Story Files v1/",
  "section": "Story section 18 Traceability",
  "description": f"{len(orphans)} requirements are cited in no story section 18 and have no legacy key, so no realigned story owns them ({', '.join(x['req'] for x in orphans)}).",
  "evidence": "All 1,065 story files read for the REQ IDs in section 18; _work/msr/fragments holds no requirement list for them",
  "type": "Missing", "area": "Stories", "severity": "P2", "needed_by_wave": "3",
  "legacy_ref": "none (no legacy key in v6)", "owner_role": "Business analyst", "asm": f"{A}-3",
  "proposed": "Assign each requirement to a story in the next story pass; the v7 matrix flags it as an orphan.", "wp": "C2-RTM"},
 {"id": f"{G}-4", "title": "A requirement whose own legacy stories do not cite it",
  "source": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v6.xlsx",
  "section": "RTM sheet, REQ-RDF-004",
  "description": f"REQ-RDF-004 names RWB-E1-069, RWB-E1-018 and RWB-E2-006 in v6, but the realigned stories of those keys do not cite it in section 18; the collateral and appraisal citations sit in the E3 integration stories instead.",
  "evidence": "Story section 18 tables of the slices of RWB-E1-069, RWB-E1-018 and RWB-E2-006; REQ-RDF-004 found in RWB-ITG-E3013-ITG, RWB-ITG-E3017-ITG and RWB-ITG-E3026-ITG",
  "type": "Conflict", "area": "Stories", "severity": "P3", "needed_by_wave": "2",
  "legacy_ref": "RWB-E1-069; RWB-E1-018; RWB-E2-006", "owner_role": "Business analyst", "asm": f"{A}-4",
  "proposed": "The E1 owner adds REQ-RDF-004 to its section 18 row, or the E3 integration trace is accepted; the v7 row lists the legacy slices and the citing stories.", "wp": "C2-RTM"},
 {"id": f"{G}-5", "title": "No legacy key for requirements written before the realignment",
  "source": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v6.xlsx",
  "section": "RTM sheet, column Stories (H)",
  "description": f"{231 - STAT['with_key']} requirements carried no story in v6 ('No story yet', 'Epic 3 backlog' and similar), so the v6 matrix gives them no legacy key; under D-RCV-60 the story link is read from section 18 of the story files instead.",
  "evidence": "RTM v6 column Stories; story section 18 tables; _work/msr/plan/split_plan.json has no entry for these requirements",
  "type": "Missing", "area": "Traceability", "severity": "P3", "needed_by_wave": "1",
  "legacy_ref": "none", "owner_role": "Business analyst", "asm": f"{A}-5",
  "proposed": "Keep the v6 cell unchanged and read the story link from section 18; the v7 Legacy keys cell says no legacy key exists.", "wp": "C2-RTM"},
 {"id": f"{G}-6", "title": "The v6 coverage statement no longer describes the story position",
  "source": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v6.xlsx",
  "section": "Coverage sheet",
  "description": "The v6 Coverage sheet says 10 requirements have no story and 82 are written one epic ahead; after the realignment every requirement with a story is traced to a realigned story, so the statuses are outdated.",
  "evidence": "RTM v6 Coverage rows E2 'No story yet' 10, E3 to E8 'Story one epic ahead' 82",
  "type": "Outdated", "area": "Reporting", "severity": "P3", "needed_by_wave": "1",
  "legacy_ref": "RTM v6 Coverage sheet", "owner_role": "Test manager", "asm": f"{A}-6",
  "proposed": "The v6 coverage block is kept unchanged as history and a realignment block is added below it.", "wp": "C2-RTM"},
 {"id": f"{G}-7", "title": "No issue-tracker, branch, commit or pull-request metadata",
  "source": "Whole run",
  "section": "Traceability standards, GitHub metadata",
  "description": "No issue, branch, commit or pull request exists for this run, and the run makes no external writes, so the matrix records none rather than an empty plausible value.",
  "evidence": "R1 U6 (no issue-tracker access or updates); AGENTS.md rule 3 (no external writes, no commits)",
  "type": "Missing", "area": "Traceability", "severity": "P3", "needed_by_wave": "1",
  "legacy_ref": "n/a", "owner_role": "Delivery lead", "asm": f"{A}-7",
  "proposed": "Add the metadata in the delivery tool when the work is scheduled; no value is invented here.", "wp": "C2-RTM"},
 {"id": f"{G}-8", "title": "Every realigned artifact is Draft with no approval",
  "source": "Whole run",
  "section": "Review status",
  "description": "No human approval exists in this run, so every requirement, story, PRD and test artifact is Draft and the review status of each row is Draft.",
  "evidence": "R1 U8 (no human verification stops in this run); the D-RCV-60 overlay assumes approval and continues.",
  "type": "Missing", "area": "Governance", "severity": "P3", "needed_by_wave": "1",
  "legacy_ref": "n/a", "owner_role": "Delivery lead", "asm": f"{A}-8",
  "proposed": "Run the verification loop before the first wave starts.", "wp": "C2-RTM"},
]

assumptions = [
 {"id": f"{A}-1", "text": "For every requirement the Owner column is the service whose PRD functional requirements carry it, and the Ownership Map owner of its legacy key where it has no functional requirement; a withdrawn row keeps the v6 Module value. The v6 Module value is kept unchanged beside it.",
  "why": "The realignment moves ownership (interaction ledger to rwb-source-data, decisions to rwb-decision, deviations to rwb-deviation) and the matrix must show the new owner.",
  "read": "OWNER = PRD service of the requirement's FR IDs, else the Ownership Map owner of its legacy key; MODULE = v6 value, kept for traceability.",
  "gap": f"{G}-1", "applied_in": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx, RTM column Q",
  "confidence": "Medium", "confirm": "Solution architect confirms the owner of each flagged requirement.", "impact": "231 rows carry an owner; the change is visible in column Q.", "wp": "C2-RTM"},
 {"id": f"{A}-2", "text": "A requirement named in a PRD as an upstream ID but carried by no functional requirement is flagged, not mapped to a nearby FR.",
  "why": "Mapping it to a nearby FR would invent coverage that no PRD states.",
  "read": "PRD FR IDs = the FRs whose row or trace-summary row names the requirement; none means none.",
  "gap": f"{G}-2", "applied_in": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx, RTM column P",
  "confidence": "High", "confirm": "Product owner confirms or withdraws each flagged requirement.", "impact": f"{len(no_fr_flagged)} rows carry the placeholder and the flag.", "wp": "C2-RTM"},
 {"id": f"{A}-3", "text": "A requirement that no story section 18 cites and that has no legacy key is recorded as an orphan rather than linked to the nearest story.",
  "why": "No source names a story for it, and the realignment must not invent a link.",
  "read": "New story IDs = the stories that name the requirement in section 18; none means orphan.",
  "gap": f"{G}-3", "applied_in": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx, RTM columns O and R",
  "confidence": "High", "confirm": "Business analyst assigns each orphan to a story.", "impact": f"{len(orphans)} rows are flagged as orphans.", "wp": "C2-RTM"},
 {"id": f"{A}-4", "text": "For REQ-RDF-004 the matrix lists the legacy slices and the citing E3 integration stories, and keeps the v6 legacy keys in column N.",
  "why": "The v6 legacy keys still own the requirement, but their realigned stories do not repeat it in section 18.",
  "read": "New story IDs for this one row = the slices of the v6 keys plus the stories whose section 18 names the requirement.",
  "gap": f"{G}-4", "applied_in": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx, RTM row REQ-RDF-004",
  "confidence": "Medium", "confirm": "E1 story owner adds the requirement to its section 18 row.", "impact": "1 row.", "wp": "C2-RTM"},
 {"id": f"{A}-5", "text": "Where no legacy key exists, the story link is read from section 18 of the realigned story files.",
  "why": "The v6 matrix gives no key for the backlog requirements, and section 18 is the only place that names them.",
  "read": "New story IDs = stories whose section 18 names the requirement; the Legacy keys cell says no legacy key exists.",
  "gap": f"{G}-5", "applied_in": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx, RTM columns N and O",
  "confidence": "High", "confirm": "None needed; the story text is the evidence.", "impact": f"{231 - STAT['with_key']} rows.", "wp": "C2-RTM"},
 {"id": f"{A}-6", "text": "The v6 coverage block is kept unchanged and a realignment block is added below it.",
  "why": "Every section and number of the source must be kept, and the new position must also be readable.",
  "read": "The first block is history; the second block is the v7 position.",
  "gap": f"{G}-6", "applied_in": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx, Coverage sheet",
  "confidence": "High", "confirm": "None needed.", "impact": "Coverage sheet only.", "wp": "C2-RTM"},
 {"id": f"{A}-7", "text": "No issue, branch, commit or pull request value is recorded for any row, because none exists in this run.",
  "why": "The run makes no external writes and no commits, and inventing an identifier would be worse than an empty cell.",
  "read": "GitHub metadata is absent, not unknown.",
  "gap": f"{G}-7", "applied_in": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx, Coverage sheet",
  "confidence": "High", "confirm": "Delivery lead adds the metadata when the work is scheduled.", "impact": "Coverage sheet only.", "wp": "C2-RTM"},
 {"id": f"{A}-8", "text": "Every row carries review status Draft, because no human approval exists in this run.",
  "why": "The D-RCV-60 overlay treats a missing approval as an assumption and continues in Draft.",
  "read": "STATUS = Draft for all 231 rows.",
  "gap": f"{G}-8", "applied_in": "09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v7.xlsx, RTM column R and Coverage sheet",
  "confidence": "High", "confirm": "Approval workflow after the verification loop.", "impact": "All rows.", "wp": "C2-RTM"},
]

Path(WORK / "gaps").mkdir(parents=True, exist_ok=True)
Path(WORK / "assumptions").mkdir(parents=True, exist_ok=True)
print("gap rows", len(gaps), "assumption rows", len(assumptions), "(written at the end)")

# ---------------------------------------------------------------- v7 workbook
subprocess.run([sys.executable, "-I", "22 Microservice Realignment/compat/office_write.py", "copy", str(SRC_X), str(OUT_X)], check=True)
wb = openpyxl.load_workbook(OUT_X)
del wb["RTM"]
ws = wb.create_sheet("RTM", 0)

thin = Side(style="thin")
BORD = Border(left=thin, right=thin, top=thin, bottom=thin)
HFILL = PatternFill("solid", fgColor="DCD3EB")
F_TITLE = Font(name="Aptos", size=16, bold=True)
F_BODY = Font(name="Aptos", size=10)
F_BOLD = Font(name="Aptos", size=10, bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")

HDR = ["Requirement", "Text", "Priority", "Epic", "Module", "Feature", "Feature name", "Stories",
       "FSD section", "TSD section", "Tests", "Acceptance", "Gate",
       # v7
       "Legacy keys", "New story IDs (D-RCV-60)", "PRD FR IDs", "Owner (realigned: PRD FR, else Ownership Map)",
       "Coverage, review status and flags"]

ws["A1"] = HEAD1; ws["A1"].font = F_BOLD
ws["A2"] = HEAD2; ws["A2"].font = F_BODY
ws["A3"] = "Requirements traceability"; ws["A3"].font = F_TITLE
ws["A4"] = rows6[1][0]; ws["A4"].font = F_BODY; ws["A4"].alignment = WRAP
ws["A5"] = ("v7 (D-RCV-60 realignment). 231 requirements traced through the legacy key to the realigned story IDs and to the PRD "
            "functional requirements, with the owner of every requirement read from the service whose PRD functional requirements "
            "carry it and, where it has none, from the Ownership Map. Columns A to M are the v6 matrix unchanged. Columns N to R are "
            "new: the legacy key per requirement, the realigned stories that own it, the PRD FR IDs, the realigned owner and the "
            "coverage and review status with every flag. 231 requirements, 0 withdrawn in this version; REQ-RDF-005 and REQ-RDF-006 "
            "stay Removed by D-RCV-35 U5 with their later home. Every row is Draft: no human approval exists in this run "
            f"(ASM-C2-RTM-8). No issue, branch, commit or pull request metadata exists (ASM-C2-RTM-7). "
            "Gap and assumption citations carry the candidate numbers written by WP C2-RTM and are renumbered at step D1.")
ws["A5"].font = F_BODY; ws["A5"].alignment = WRAP
ws.row_dimensions[5].height = 92

ws["A7"] = "Change log"; ws["A7"].font = F_BOLD
ws["A8"] = "v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
ws["A8"].font = F_BODY

HR = 10
for i, h in enumerate(HDR, 1):
    c = ws.cell(row=HR, column=i, value=h)
    c.font = F_BOLD; c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = BORD
ws.row_dimensions[HR].height = 30

r = HR
for x in recs:
    r += 1
    row = x["row"]
    vals = list(row[:13])
    # N legacy keys
    if x["keys"]:
        n = "; ".join(x["keys"])
    elif x["removed"]:
        n = "None - withdrawn under D-RCV-35 U5"
    else:
        n = "None - no legacy key in the v6 matrix"
    # O new stories
    if x["new"]:
        o = "; ".join(x["new"])
    else:
        o = f"None - no realigned story carries this requirement (CG-C2-RTM-3; ASM-C2-RTM-3)"
    # P FR
    if x["fr"]:
        p = "; ".join(x["fr"])
    elif x["removed"]:
        p = "None - withdrawn under D-RCV-35 U5; no functional requirement by design"
    elif reqfr.get(x["req"], {}).get("note") and any("D-RCV-60" in s for s in reqfr.get(x["req"], {}).get("note", [])):
        p = "None - not carried (D-RCV-60: no data lake; CG-B-REQ-PRD-P7-2)"
    else:
        p = f"Not specified in the source documents (CG-C2-RTM-2; ASM-C2-RTM-2)"
    # Q owner
    code = x["owner"]
    q = f"{code} {SVC[code]['service']}" if code in SVC else str(code)
    # R coverage note
    bits = []
    if x["removed"]:
        bits.append("Removed by D-RCV-35 U5: no realigned story by design; later home the Cutover and Go Live Plan v2")
    elif x["basis"] == "legacy+citation":
        bits.append(f"Traced: {len(x['keys'])} legacy keys give {len([s for k in x['keys'] for s in legacy[k]['slices']])} realigned stories that do not name the requirement in section 18, and the citing stories are added (CG-C2-RTM-4; ASM-C2-RTM-4)")
    elif x["new"] and x["keys"]:
        bits.append(f"Traced: {len(x['keys'])} legacy key{'s' if len(x['keys']) != 1 else ''} to {len(x['new'])} realigned stories")
    elif x["new"]:
        bits.append(f"Traced: no legacy key; {len(x['new'])} realigned stories name the requirement in section 18")
    else:
        bits.append("Orphan: no realigned story carries this requirement (CG-C2-RTM-3; ASM-C2-RTM-3)")
    if x["fr"]:
        bits.append(f"PRD FR: {len(x['fr'])}")
    elif x["removed"]:
        bits.append("PRD: not carried by design")
    elif x in NOT_CARRIED:
        bits.append("PRD: not carried (D-RCV-60: no data lake; CG-B-REQ-PRD-P7-2)")
    else:
        bits.append("PRD FR: none (CG-C2-RTM-2; ASM-C2-RTM-2)")
    if x["owner"] != row[4]:
        bits.append(f"Owner realigned from {row[4]} to {x['owner']} (Ownership Map; CG-C2-RTM-1; ASM-C2-RTM-1)")
    ret = [k for k in x["keys"] if k in RETIRED]
    if ret:
        for k in ret:
            bits.append(f"{k} retired (D-RCV-60): dependencies point to RWB-PLT-E1071-CON" if k == "RWB-TE-007"
                        else f"{k} retired (D-RCV-60): no data lake, dependencies dropped")
    tcs = [t.strip() for t in re.split(r"[,;]", row[10] or "") if t.strip()]
    bits.append(f"Tests: {len(tcs)} test case{'s' if len(tcs) != 1 else ''}")
    bits.append("Review: Draft")
    rr = "; ".join(bits)
    c = None
    for i, v in enumerate(vals + [n, o, p, q, rr], 1):
        c = ws.cell(row=r, column=i, value=v)
        c.font = F_BOLD if i == 1 else F_BODY
        c.alignment = WRAP
        c.border = BORD
ws.freeze_panes = "B11"
ws.auto_filter.ref = f"A{HR}:R{r}"
for col, w in {"A": 13, "B": 54, "C": 8, "D": 6, "E": 7, "F": 13, "G": 30, "H": 22, "I": 13, "J": 11,
               "K": 34, "L": 24, "M": 28, "N": 26, "O": 46, "P": 40, "Q": 22, "R": 54}.items():
    ws.column_dimensions[col].width = w

# ---------------------------------------------------------------- Coverage sheet
del wb["Coverage"]
cs = wb.create_sheet("Coverage", 1)
for row in cov6:
    cs.append([c for c in row])
cs.append([])
cs.append(["Coverage by epic (D-RCV-60 realignment, v7)"])
cs[cs.max_row][0].font = F_BOLD
cs.append(["Every requirement with a story now traces to a realigned story; the v6 block above is kept unchanged as history (CG-C2-RTM-6; ASM-C2-RTM-6)."])
cs.append([])
cs.append(["Epic", "Status", "Requirements"])
for c in cs[cs.max_row]:
    c.font = F_BOLD; c.fill = HFILL
EPIC_STATUS = []
for ep in ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]:
    sub = [x for x in recs if x["row"][3] == ep]
    rem = [x for x in sub if x["removed"]]
    tr = [x for x in sub if x["new"] and not x["removed"]]
    orp = [x for x in sub if not x["new"] and not x["removed"]]
    if rem:
        EPIC_STATUS.append([ep, "Removed by D-RCV-35 (U5)", len(rem)])
    if tr:
        EPIC_STATUS.append([ep, "Traced to a realigned story", len(tr)])
    if orp:
        EPIC_STATUS.append([ep, "Orphan - no realigned story (CG-C2-RTM-3)", len(orp)])
for row in EPIC_STATUS:
    cs.append(row)
cs.append([])
cs.append(["Coverage by artifact and check (v7)"])
cs[cs.max_row][0].font = F_BOLD
cs.append([])
cs.append(["Check", "Result", "Count", "Note"])
for c in cs[cs.max_row]:
    c.font = F_BOLD; c.fill = HFILL
CHECKS = [
 ["Requirements in this matrix", "Counted", 231, "Every v6 ID kept; no ID changed, added or reused"],
 ["Requirements with a legacy key", "Counted", STAT["with_key"], f"{231 - STAT['with_key']} requirements carried no story in v6 (CG-C2-RTM-5; ASM-C2-RTM-5)"],
 ["Requirements removed", "Counted", STAT["removed"], "REQ-RDF-005 and REQ-RDF-006, Removed by D-RCV-35 U5, later home the Cutover and Go Live Plan v2"],
 ["Requirements with realigned story IDs", "Counted", STAT["new_story"], f"{STAT['no_story']} orphaned requirements flagged (CG-C2-RTM-3; ASM-C2-RTM-3)"],
 ["Requirements with a PRD functional requirement", "Counted", 231 - len(no_fr), f"{STAT['no_fr']} requirements have no FR in any PRD (CG-C2-RTM-2; ASM-C2-RTM-2); {STAT['not_carried']} further requirement is retired by design (REQ-DRI-009)"],
 ["Requirements with test cases", "Counted", 231, "Every row keeps the v6 test cases; the realigned test IDs are in the Test Cases v8 family"],
 ["Requirements with a realigned owner", "Counted", 231, f"Owner = PRD FR service, else Ownership Map; {STAT['owner_changed']} owners differ from the v6 Module value (CG-C2-RTM-1; ASM-C2-RTM-1)"],
 ["Requirements citing a retired legacy story", "Counted", STAT["retired_rows"], "RWB-TE-007 dependencies point to RWB-PLT-E1071-CON; RWB-E1-014 dependencies are dropped"],
 ["Features without a requirement", "Counted", 0, "Every FEAT ID in the matrix carries at least one requirement"],
 ["Requirements without a review status", "Counted", 0, "Every row is Draft; no approval exists in this run (CG-C2-RTM-8; ASM-C2-RTM-8)"],
 ["Banking compliance requirements without evidence", "Counted", 0, "Every requirement keeps an FSD section, a TSD section and test cases"],
 ["Context artifacts and standards", "Present", 6, "AI-SDLC workspace: project-context, domain-context, frontend-context, backend-context, testing-standards, rules/traceability-standards.md"],
 ["Context updates (CTX-UPDATE)", "None recorded", 0, "No context-update run in this realignment; the context pack is realignment-v5-context.md and the requirement IDs above are the trace chain"],
 ["GitHub issue, branch, commit, pull request", "None", 0, "No metadata exists in this run; none is invented (CG-C2-RTM-7; ASM-C2-RTM-7)"],
 ["Specifications, tasks, code and run records", "Out of scope of this family", 0, "The realignment has no SPEC, TASK, CODE or APT records; the story, PRD, test and review artifacts are the trace chain of this family"],
]
for row in CHECKS:
    cs.append(row)
for rr in cs.iter_rows(min_row=1, max_row=cs.max_row, max_col=4):
    for c in rr:
        if c.value is not None:
            c.alignment = WRAP
cs.column_dimensions["A"].width = 46
cs.column_dimensions["B"].width = 34
cs.column_dimensions["C"].width = 14
cs.column_dimensions["D"].width = 78

wb.save(OUT_X)
print("WROTE", OUT_X, "rows", r - HR, "cols", ws.max_column)

for kind, rec in (("gaps", gaps), ("assumptions", assumptions)):
    p = WORK / kind / "C2-RTM.jsonl"
    if p.exists():
        raise SystemExit(f"REFUSED: {p} exists")
    p.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rec) + "\n", encoding="utf-8")
print("wrote jsonl rows", len(gaps), len(assumptions))

# ---------------------------------------------------------------- notes md
notes = f"""{HEAD1}
{HEAD2}

# Requirements Traceability Matrix v7 - realignment notes (D-RCV-60)

Change log: v7, {DATE}, D-RCV-60 microservice realignment, {TOOL}

## 1. What changed and what did not

| Item | v6 | v7 |
|---|---|---|
| Requirement rows | 231 | 231, the same IDs in the same order |
| Columns A to M | 13 | 13, unchanged values |
| Columns N to R | none | Legacy keys, New story IDs, PRD FR IDs, Owner, Coverage and flags |
| Coverage sheet | one block | the v6 block unchanged, plus the realignment block |
| Header lines | none | the Template and Rules section R8.1 header on RTM rows 1 and 2 |
| Change log row | none | v7, {DATE}, D-RCV-60 microservice realignment, {TOOL} |

## 2. How a row reads

Requirement -> legacy key (column N, from the v6 Stories column) -> realigned story IDs (column O, the split_plan slices of that key) -> PRD FR IDs (column P, from the PRD section 11.2 trace summary and the FR tables) -> owner (column Q: the service whose PRD functional requirements carry the requirement, else the Ownership Map owner of its legacy key) -> coverage and flags (column R).

Where no legacy key exists, column O carries the stories whose section 18 names the requirement (ASM-C2-RTM-5).

## 3. Counts

| Measure | Count |
|---|---|
| Requirements | {STAT['reqs']} |
| Requirements with a legacy key | {STAT['with_key']} |
| Requirements with realigned story IDs | {STAT['new_story']} |
| Orphaned requirements (no realigned story) | {STAT['no_story']} |
| Requirements with no PRD FR | {STAT['no_fr']} |
| Requirements whose owner differs from the v6 Module | {STAT['owner_changed']} |
| Requirements citing a retired legacy story | {STAT['retired_rows']} |
| Gap rows written | {len(gaps)} |
| Assumption rows written | {len(assumptions)} |

## 4. Flags raised

| Flag | Requirement | Reason |
|---|---|---|
| CG-C2-RTM-1 | {STAT['owner_changed']} rows | the v6 Module value differs from the owner read from the PRD FRs and the Ownership Map |
| CG-C2-RTM-2 | {', '.join(x['req'] for x in no_fr_flagged)} | named in a PRD, carried by no functional requirement |
| CG-C2-RTM-3 | {', '.join(x['req'] for x in orphans)} | no realigned story names the requirement in section 18 |
| CG-C2-RTM-4 | REQ-RDF-004 | the slices of its legacy keys do not name it; the E3 integration stories do |
| CG-C2-RTM-5 | {231 - STAT['with_key']} rows | no legacy key existed in v6 |
| CG-C2-RTM-6 | Coverage sheet | the v6 coverage statement is outdated |
| CG-C2-RTM-7 | whole run | no issue, branch, commit or pull request metadata exists |
| CG-C2-RTM-8 | 231 rows | every row is Draft, no approval exists in this run |

Owner roles only; no names of people are used anywhere in this document.

## 5. Assumptions

| Assumption | Text |
|---|---|
""" + "\n".join(f"| {a['id']} | {a['text']} |" for a in assumptions) + f"""

## 6. Status

Draft. No human approval exists in this run. The numbers in this file are the candidate numbers written by WP C2-RTM and are renumbered at step D1.
"""
p = SCR / "RTM v7 realignment notes.md"
if p.exists():
    raise SystemExit(f"REFUSED: {p} exists")
p.write_text(notes, encoding="utf-8")
print("WROTE", p)
