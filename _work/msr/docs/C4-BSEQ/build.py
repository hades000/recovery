"""Build Build Sequence v7 from the v6 copy (scratch only, never touches the source)."""
import json
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
OUT = ROOT / "_work" / "msr" / "docs" / "C4-BSEQ"
DST = ROOT / "11 Delivery and operations" / "Recovery Workbench Build Sequence Epic 1 and Epic 2 v7.xlsx"

DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
HL = "SCB Collections and Recovery. Henka Group, 22 November 2026."
HL2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
CHANGE = f"v7, 22 November 2026, {DEC} microservice realignment, {TOOL}"
PH = "Not specified in the source documents (CG-C4-BSEQ-1; ASM-C4-BSEQ-6)"

data = json.loads((OUT / "mapping.json").read_text(encoding="utf-8"))
items = data["items"]
plt = data["plt"]

SVC = {
    "P1": ("rwb-source-data", "Source data", 1), "P2": ("rwb-integration", "Integration", 1),
    "P3": ("rwb-case", "Case and workflow", 1), "P4": ("rwb-access", "Access and authority", 1),
    "P5": ("rwb-document", "Document", 1), "P6": ("rwb-comms", "Communications", 1),
    "P7": ("rwb-decision", "Decision and rules", 1), "P8": ("rwb-payment", "Payment", 2),
    "P9": ("rwb-reporting", "Reporting", 1), "P10": ("rwb-agent", "Agent", 1),
    "S1": ("rwb-valuation", "Valuation and route", 3), "S2": ("rwb-treatment", "Treatment and offer", 2),
    "S3": ("rwb-guarantee", "Guarantee", 3), "S4": ("rwb-litigation", "Litigation", 3),
    "S5": ("rwb-asset", "Asset", 2), "S6": ("rwb-debtsale", "Debt sale", 3),
    "S7": ("rwb-writeoff", "Write-off", 4), "S8": ("rwb-deviation", "Deviation", 2),
    "S9": ("rwb-partner", "Partner", 4),
}
SHORT2CODE = {v[0]: k for k, v in SVC.items()}
SHORT2CODE["platform"] = "PLT"
SHORT2CODE["integration"] = "ITG"
WT_OWNER = {"CON": "TechX", "APP": "TechX", "ITG": "TechX", "DB": "ACE team",
            "INF": "SCB IT infrastructure", "OPS": "DevOps team"}
WT_FULL = {"CON": "TechX (suggested; any team may pick up this story)",
           "APP": "TechX (suggested; any team may pick up this story)",
           "ITG": "TechX (suggested; any team may pick up this story); harness and NFR stories: QA team (suggested; any team may pick up this story)",
           "DB": "ACE team (suggested; any team may pick up this story)",
           "INF": "SCB IT infrastructure (suggested; any team may pick up this story)",
           "OPS": "DevOps team (suggested; any team may pick up this story)"}
WINDOWS = ["Window 1", "Window 2", "Window 3", "Window 4", "Epic 3"]
EPIC_ORDER = ["RWB-PLT-TPL", "RWB-PLT-LIB", "RWB-PLT-DB", "RWB-PLT-EVT", "RWB-PLT-EDGE", "RWB-PLT-WF", "RWB-PLT-OBS"]
WT_ORDER = {"CON": 0, "APP": 1, "DB": 2, "INF": 3, "OPS": 4, "ITG": 5}
WT2CODE = {"Contract": "CON", "App development": "APP", "ACE DB": "DB",
           "Infrastructure": "INF", "DevOps": "OPS", "Integration": "ITG"}


def wcode(name):
    return WT2CODE.get(name, name)


def svc_label(short):
    code = SHORT2CODE.get(short, short)
    if code == "PLT":
        return "PLT platform"
    if code == "ITG":
        return "ITG integration"
    return f"{code} {SVC[code][0]}"


def svc_line(short):
    code = SHORT2CODE.get(short, short)
    if code in ("PLT", "ITG"):
        return svc_label(short)
    return f"{code} {SVC[code][0]} ({SVC[code][1]})"


# ---------- row planning ----------
def dep_keys(it):
    s = str(it["dep"] or "")
    return [k.strip() for k in s.split(",") if k.strip().startswith("RWB-")]


order = []
for w in WINDOWS:
    pool = [i for i in items if i["window"] == w]
    keys = {i["key"] for i in pool}
    done = set()
    while pool:
        free = [i for i in pool if all(d not in keys or d in done for d in dep_keys(i))]
        if not free:
            free = pool
        free.sort(key=lambda i: (0 if i["con"] else 1, i["order"]))
        pick = free[0]
        order.append(pick)
        done.add(pick["key"])
        pool.remove(pick)
for n, it in enumerate(order, 1):
    it["ord7"] = n

for it in items:
    if not it["slices"]:
        it["con_txt"] = "None (retired in " + DEC + ", Template and Rules §R6)"
        it["del_txt"] = "No new story"
        it["svc_txt"] = "None (retired)"
        it["lane_txt"] = "None"
        it["own_txt"] = "None (not pulled)"
        it["ready_txt"] = "Not pulled"
        continue
    if it["con"]:
        it["con_txt"] = "; ".join(c["id"] for c in it["con"])
    else:
        pref = [s for s in it["del"] if SHORT2CODE[s["svc"]] not in ("ITG", "PLT")] or it["del"]
        s0 = pref[0]
        code = SHORT2CODE[s0["svc"]]
        w = 0 if code == "PLT" else (SVC[code][2] if code in SVC else s0["wave"])
        grp = "the platform contract group CG-W0" if code == "PLT" else \
            f"the {svc_line(s0['svc'])} contract group CG-W{w}" if code in SVC else \
            f"the service contract groups of wave {w}"
        it["con_txt"] = f"None; build against {grp}"
    it["del_txt"] = "; ".join(s["id"] for s in it["del"]) if it["del"] else "None"
    svcs, lanes, owns = [], [], []
    for s in it["slices"]:
        if svc_line(s["svc"]) not in svcs:
            svcs.append(svc_line(s["svc"]))
        if s["lane"] not in lanes:
            lanes.append(s["lane"])
        o = str(s["owner"]).split(" (suggested")[0].strip()
        if o not in owns:
            owns.append(o)
    it["svc_txt"] = "; ".join(svcs)
    it["lane_txt"] = "; ".join(lanes)
    it["own_txt"] = "; ".join(owns)
    ready = [s["ready"] for s in it["del"]] or [s["ready"] for s in it["slices"]]
    distinct = sorted(set(ready))
    pick = "Day 1" if "Day 1" in distinct else min(distinct, key=len)
    it["ready_txt"] = pick if len(distinct) == 1 else f"{pick} (earliest of {len(distinct)} lane starts)"

wb = openpyxl.load_workbook(DST)


def style_header(ws, row, ncol, fill="1F3864"):
    for c in range(1, ncol + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(wrap_text=True, vertical="top")


def title(ws, text, row, bold=True, size=12):
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = Font(bold=bold, size=size)
    return cell


def note(ws, text, row, italic=True):
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = Font(italic=italic, size=9)
    cell.alignment = Alignment(wrap_text=True, vertical="top")
    return cell


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


# ---------- Read me ----------
rm = wb.create_sheet("Read me", 0)
title(rm, HL, 1, size=10)
rm.cell(row=2, column=1, value=HL2).font = Font(size=10)
rm.cell(row=4, column=1, value=f"Recovery Workbench Build Sequence Epic 1 and Epic 2 v7. Tool: {TOOL}. Decision {DEC}.").font = Font(bold=True, size=12)
rm.cell(row=6, column=1, value="Item")
rm.cell(row=6, column=2, value="Detail")
style_header(rm, 6, 2)
body = [
    ("What this workbook is",
     "The pull order for the Epic 1 and Epic 2 work, re-cut for the 19 services of Architecture v5: Day-1 contract and platform work first, then each service's lane in wave order. Every v6 item, ID, number and date is kept."),
    ("Source version", "Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx (v6, 16 November 2026), copied and extended. No v6 file is edited."),
    ("Scope", "The 115 v6 items, each mapped to the new stories of its legacy key (Template and Rules §R5.2). The 115 items become 530 new stories: 441 by a service and 89 integration stories."),
    ("Day-1 block", "65 platform stories (wave 0) and the wave 1 and wave 2 contract groups CG-W1 (44 stories) and CG-W2 (64 stories) are pulled before item 1 of the Sequence sheet (sheet 'Day 1 first', Template and Rules §R5.7.1 and §R5.7.6)."),
    ("Pull order", "After that block, the 115 items are pulled in Order (v7): window by window, dependency-safe (Pull rule 1), and inside each window the items whose contract story exists come first. Order (v6) is kept on every row, so a v6 number can still be quoted."),
    ("Contract first", "Contract work on every row is Day 1 (§R5.7.1), so each window opens with its contract stories and then its lanes. An APP story builds against the published contract and its fake; a C dependency never blocks (§R5.7.2). 27 items have no contract story of their own and build against their service contract group, named on the row."),
    ("Owner", "Owners are the work-type owners of Template and Rules §R5.3, in the spelling of the Microservice Ownership Map v1 (sheet 'Owners (v7)'). No names of people anywhere."),
    ("Source precedence", "Architecture v5 catalogue slides (13 to 20, 41 to 44) first, then the Temporal and Drools Detailed Design v1, then the Architecture v5 narrative (Template and Rules §R3). Owners and tables per the Microservice Ownership Map v1."),
    ("Release dates", "The Release column keeps the v6 edition label (E1, E2, E3). The two-week window dates are copied unchanged from v6. Every release date is marked (tentative) and no date is changed (Template and Rules §R1 U7)."),
    ("How to read", "Module (v6) is the monolith module of the v6 row. Service (v7) and Lane (v7) are the owner service and the lane of the new stories, from the Service Story Catalog v1. Ready to start (v7) takes the earliest lane start and says how many lane starts the row has."),
    ("Placeholders", "A value the sources do not give is written 'Not specified in the source documents (CG-C4-BSEQ-n; ASM-C4-BSEQ-n)'. The rows are in the Gap Register and the Assumptions Register."),
    ("Status", "Draft. Both v6 and v7 carry no recorded approval, so the next version continues in Draft (Template and Rules §R1 U8)."),
    ("Change log", CHANGE),
]
r = 7
for k, v in body:
    rm.cell(row=r, column=1, value=k).font = Font(bold=True, size=10)
    c = rm.cell(row=r, column=2, value=v)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = Font(size=10)
    r += 1
widths(rm, {"A": 22, "B": 118})
for r in range(1, r):
    rm.row_dimensions[r].height = None
rm.cell(row=4, column=1).alignment = Alignment(wrap_text=True)

# ---------- Sequence ----------
ws = wb["Sequence"]
ws.cell(row=1, column=1, value="The order the Epic 1 and Epic 2 work is pulled, by service and lane, Day 1 first").font = Font(bold=True, size=12)
ws["A2"] = ("115 items. Delivery runs as Kanban (DT04): items are pulled in this order as capacity frees up. The two-week windows are the sponsor review points, not sprint boundaries. "
            "RWB-ACE-001, the ACE team's schema delivery, gates window 1 and is not pulled by either squad. v6, 16 November 2026. "
            "v7, 22 November 2026: the 115 items keep their IDs, numbers and dates; each is remapped to its new stories by service and lane (Template and Rules §R5), and Order (v7) re-cuts the pull order dependency-safe, with the items that have a contract story first in each window (§R5.7) after the Day-1 block of the sheet 'Day 1 first'.")
ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws["A2"].font = Font(size=9, italic=True)
ws.row_dimensions[2].height = 46
hdrs = ["Order (v7)", "Order (v6)", "Key", "Title", "Module (v6)", "Type", "Priority",
        "Depends on (v6)", "Review window", "Dates", "Release", "Critical path",
        "Contract story (v7)", "Delivery stories (v7)", "Service(s) (v7)", "Lane(s) (v7)",
        "Owner(s) (v7)", "Ready to start (v7)"]
for c, h in enumerate(hdrs, 1):
    ws.cell(row=4, column=c, value=h)
style_header(ws, 4, len(hdrs))
ws.row_dimensions[4].height = 34
# clear the old body, then write the mapped rows in v7 order
for r in range(5, 5 + 200):
    for c in range(1, 13):
        ws.cell(row=r, column=c).value = None
for r, it in enumerate(sorted(items, key=lambda i: i["ord7"]), 5):
    vals = [it["ord7"], it["order"], it["key"], it["title"], it["module"], it["type"], it["priority"],
            it["dep"], it["window"], it["dates"], it["release"], it["cp"],
            it["con_txt"], it["del_txt"], it["svc_txt"], it["lane_txt"], it["own_txt"], it["ready_txt"]]
    for c, v in enumerate(vals, 1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
widths(ws, {"A": 8, "B": 8, "C": 14, "D": 46, "E": 9, "F": 11, "G": 8, "H": 30, "I": 12, "J": 14,
            "K": 8, "L": 9, "M": 30, "N": 46, "O": 28, "P": 26, "Q": 22, "R": 28})
ws.freeze_panes = "C5"
last = 4 + len(items)

# ---------- Day 1 first ----------
d1 = wb.create_sheet("Day 1 first", wb.sheetnames.index("Sequence") + 1)
title(d1, "Day 1 first: the wave-0 platform, then the contract groups of waves 1 and 2", 1)
note(d1, ("Every CON story is Day 1 and sits in contract group CG-W<wave> (Template and Rules §R5.7.1); the platform stories N001 to N012 and W1J01 make sure every team type has Day 1 work (§R5.7.6). "
          "Pull this block before item 1 of the Sequence sheet, then pull the Sequence sheet in Order (v7). v7, 22 November 2026."), 2)
d1.row_dimensions[2].height = 40
dh = ["Pull order (Day 1)", "Group", "Wave", "Story (v7)", "Title", "Work type", "Suggested owner",
      "Service (v7)", "Lane (v7)", "Ready to start", "Release", "Maps from (v6)"]
for c, h in enumerate(dh, 1):
    d1.cell(row=4, column=c, value=h)
style_header(d1, 4, len(dh))

r = 5
n = 0


def phase(row, text):
    cell = d1.cell(row=row, column=1, value=text)
    cell.font = Font(bold=True, size=10, color="1F3864")
    return row + 1


con_w1 = []
all_plt = sorted(plt, key=lambda p: (EPIC_ORDER.index(p["Epic"]) if p["Epic"] in EPIC_ORDER else 9,
                                     WT_ORDER.get(wcode(p["Work type"]), 9), p["Story"]))

wr = openpyxl.load_workbook(ROOT / "04 User stories" / "Recovery Workbench Service Story Catalog v1.xlsx",
                            read_only=True, data_only=True)
sr = list(wr["Stories"].iter_rows(values_only=True))
hdr = list(sr[0])
cats = [dict(zip(hdr, x)) for x in sr[1:]]
wr.close()


def legacy_label(p):
    leg = str(p["Legacy"])
    if leg in ("N001", "N002", "N003", "N004", "N005", "N006", "N007", "N008", "N009", "N010",
               "N011", "N012"):
        return f"New story ({leg})"
    if leg.startswith("NF-"):
        return "RWB-" + leg
    return leg


def emit2(rows, group):
    global r, n
    r = phase(r, group)
    for p in rows:
        n += 1
        vals = [n, group.split(" - ")[0], p["Wave"], p["Story"], p["Title"], p["Work type"],
                p["Suggested owner"], svc_line(p["Service"]), p["Lane"], p["Ready"],
                p["Release"] if p["Release"] not in (None, "") else PH, legacy_label(p)]
        for c, v in enumerate(vals, 1):
            cell = d1.cell(row=r, column=c, value=v)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1


emit2(all_plt, "Phase 0 - platform, wave 0 (before Window 1)")
emit2(sorted([c for c in cats if c["Lane"] == "CG-W1"], key=lambda c: (c["Service"], c["Story"])),
      "Phase 1 - wave 1 contract group CG-W1")
emit2(sorted([c for c in cats if c["Lane"] == "CG-W2"], key=lambda c: (c["Service"], c["Story"])),
      "Phase 2 - wave 2 contract group CG-W2")
note(d1, ("Then pull the Epic 1 and Epic 2 items in the 'Sequence' sheet in Order (v7): each window's contract stories are already published in this block, so the delivery stories of that window build against them and their fakes. "
          "Wave 3 and wave 4 contract groups (CG-W3, CG-W4) belong to Epics 4 to 8 and are outside this workbook."), r)
d1.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
widths(d1, {"A": 10, "B": 16, "C": 6, "D": 24, "E": 52, "F": 15, "G": 34, "H": 26, "I": 12, "J": 26, "K": 26, "L": 22})
d1.freeze_panes = "D5"

# ---------- By window ----------
bw = wb["By window"]
bw["A2"] = (str(bw["A2"].value) + " v7, 22 November 2026: the item counts of v6 are unchanged; the three new columns give the story count after the service split, "
            "the contract stories that are pulled on Day 1, and the items whose legacy key has no contract story of its own.")
bw["A2"].alignment = Alignment(wrap_text=True, vertical="top")
bw["A2"].font = Font(size=9, italic=True)
bw.row_dimensions[2].height = 46
for c, h in [(5, "Stories after the split (v7)"), (6, "Contract stories (Day 1)"),
             (7, "Items with no contract story of their own")]:
    bw.cell(row=4, column=c, value=h)
style_header(bw, 4, 7)
for rr in range(5, 10):
    w = bw.cell(row=rr, column=1).value
    its = [i for i in items if i["window"] == w]
    sl = [s for i in its for s in i["slices"]]
    bw.cell(row=rr, column=5, value=len(sl))
    bw.cell(row=rr, column=6, value=sum(1 for s in sl if s["wt"] == "Contract"))
    bw.cell(row=rr, column=7, value=sum(1 for i in its if not i["con"]))
tot = [s for i in items for s in i["slices"]]
bw.cell(row=10, column=5, value=len(tot))
bw.cell(row=10, column=6, value=sum(1 for s in tot if s["wt"] == "Contract"))
bw.cell(row=10, column=7, value=sum(1 for i in items if not i["con"]))
widths(bw, {"A": 12, "B": 16, "C": 8, "D": 8, "E": 18, "F": 16, "G": 22})

# ---------- By service and lane ----------
bs = wb.create_sheet("By service and lane", wb.sheetnames.index("Critical path"))
title(bs, "Items by service and lane after the split", 1)
note(bs, ("One v6 item becomes one story per service and lane that owns part of it, so the service rows add to more than the 115 items (same rule as the v6 module sheet). "
          "Service and lane come from the Service Story Catalog v1; owner from the Microservice Ownership Map v1 and Template and Rules §R5.3. v7, 22 November 2026."), 2)
bs.row_dimensions[2].height = 34
sh = ["Code", "Service", "Wave", "Window 1", "Window 2", "Window 3", "Window 4", "Epic 3",
      "Stories (v7)", "Contract stories", "Integration stories", "Lanes", "Day-1 stories",
      "Suggested owner (contract work)"]
for c, h in enumerate(sh, 1):
    bs.cell(row=4, column=c, value=h)
style_header(bs, 4, len(sh))

tab = defaultdict(Counter)
for it in items:
    for s in it["slices"]:
        code = SHORT2CODE[s["svc"]]
        tab[code][it["window"]] += 1
        tab[code]["tot"] += 1
        tab[code]["con"] += 1 if s["wt"] == "Contract" else 0
        tab[code]["itg"] += 1 if s["wt"] == "Integration" else 0
        tab[code]["day1"] += 1 if s["ready"] == "Day 1" else 0
        tab[code]["lane:" + str(s["lane"])] += 1

r = 5
all_codes = [f"P{n}" for n in range(1, 11)] + [f"S{n}" for n in range(1, 10)] + ["PLT", "ITG"]
for code in all_codes:
    d = tab.get(code) or Counter()
    name = (SVC[code][0] + f" ({SVC[code][1]})") if code in SVC else (
        "rwb-platform (platform)" if code == "PLT" else "rwb-integration (integration waves)")
    vals = [code, name, SVC[code][2] if code in SVC else 0] + [d[w] for w in WINDOWS] + \
           [d["tot"], d["con"], d["itg"], len([k for k in d if k.startswith("lane:")]), d["day1"],
            "TechX (suggested; any team may pick up this story)"]
    for c, v in enumerate(vals, 1):
        bs.cell(row=r, column=c, value=v).alignment = Alignment(wrap_text=True, vertical="top")
    r += 1
vals = ["Total", "", ""] + [sum((tab.get(c) or Counter())[w] for c in all_codes) for w in WINDOWS] + \
       [sum((tab.get(c) or Counter())["tot"] for c in all_codes), sum((tab.get(c) or Counter())["con"] for c in all_codes),
        sum((tab.get(c) or Counter())["itg"] for c in all_codes),
        sum(len([k for k in (tab.get(c) or Counter()) if k.startswith("lane:")]) for c in all_codes),
        sum((tab.get(c) or Counter())["day1"] for c in all_codes), ""]
for c, v in enumerate(vals, 1):
    cell = bs.cell(row=r, column=c, value=v)
    cell.font = Font(bold=True)
note(bs, ("S1, S6 and S7 carry no part of the 115 Epic 1 and Epic 2 items: rwb-valuation, rwb-debtsale and rwb-writeoff arrive in wave 3 and wave 4 (Architecture v5 slide 38). "
          "PLT carries the platform stories an item splits into; ITG carries its integration stories."), r + 1)
bs.cell(row=r + 1, column=1).alignment = Alignment(wrap_text=True, vertical="top")
bs.cell(row=r + 3, column=1, value="Lanes with more than one story (v7)").font = Font(bold=True, size=10)
lh = ["Code", "Lane", "Stories", "Windows", "Story IDs"]
for c, h in enumerate(lh, 1):
    bs.cell(row=r + 4, column=c, value=h)
style_header(bs, r + 4, len(lh))
lanes = defaultdict(list)
for it in items:
    for s in it["slices"]:
        if s["wt"] == "Contract":
            continue
        lanes[(SHORT2CODE[s["svc"]], s["lane"])].append((it["window"], s["id"]))
rr = r + 5
for (code, lane), lst in sorted(lanes.items(), key=lambda x: (-len(x[1]), x[0])):
    if len(lst) < 2:
        continue
    wins = ", ".join(sorted({w for w, _ in lst}, key=WINDOWS.index))
    vals = [code, lane, len(lst), wins, "; ".join(sorted(i for _, i in lst))]
    for c, v in enumerate(vals, 1):
        bs.cell(row=rr, column=c, value=v).alignment = Alignment(wrap_text=True, vertical="top")
    rr += 1
note(bs, ("Every other lane holds one story, so it needs no separate row: it is the lane shown on its own row of the Sequence sheet. "
          "CG-W0, CG-W1 and CG-W2 are the contract groups and are pulled in the 'Day 1 first' sheet."), rr + 1)
bs.cell(row=rr + 1, column=1).alignment = Alignment(wrap_text=True)
widths(bs, {"A": 8, "B": 34, "C": 7, "D": 9, "E": 9, "F": 9, "G": 9, "H": 8, "I": 10, "J": 12,
            "K": 14, "L": 8, "M": 10, "N": 34})

# ---------- Critical path ----------
cp = wb["Critical path"]
cp["A2"] = (str(cp["A2"].value) + " v7, 22 November 2026: each step keeps its v6 window and its gating note; the three new columns give the story, service and lane that carry the step in the 19-service design.")
cp["A2"].alignment = Alignment(wrap_text=True, vertical="top")
cp["A2"].font = Font(size=9, italic=True)
cp.row_dimensions[2].height = 46
for c, h in [(7, "Story (v7)"), (8, "Service (v7)"), (9, "Lane (v7)")]:
    cp.cell(row=4, column=c, value=h)
style_header(cp, 4, 9)
leg = json.loads((ROOT / "_work" / "msr" / "plan" / "split_plan.json").read_text(encoding="utf-8"))["legacy"]
cats_by = {c["Story"]: c for c in cats}
for rr in range(5, 5 + 17):
    key = cp.cell(row=rr, column=2).value
    v = leg.get(key)
    if not v:
        continue
    ids = v["slices"]
    cons = [s for s in ids if cats_by[s]["Work type"] == "Contract"]
    shows = cons + [s for s in ids if cats_by[s]["Work type"] != "Contract"]
    cp.cell(row=rr, column=7, value="; ".join(shows))
    cp.cell(row=rr, column=8, value="; ".join(dict.fromkeys(svc_label(cats_by[s]["Service"]) for s in shows)))
    cp.cell(row=rr, column=9, value="; ".join(dict.fromkeys(str(cats_by[s]["Lane"]) for s in shows)))
    for c in (7, 8, 9):
        cp.cell(row=rr, column=c).alignment = Alignment(wrap_text=True, vertical="top")
note(cp, ("v7, 22 November 2026: RWB-ACE-001 is the ACE team's delivery and is carried as RWB-P1-ACE001-DB (ACE DB); the 21 November date and DL43 are unchanged. "
          "RWB-E1-070 to RWB-E1-073 sit in the wave-0 platform block (sheet 'Day 1 first') as CON stories and in the Sequence rows as delivery stories, so the four configuration steps still come before RWB-E1-018."), 23)
cp.cell(row=23, column=1).alignment = Alignment(wrap_text=True)
widths(cp, {"A": 6, "B": 14, "C": 48, "D": 8, "E": 10, "F": 34, "G": 46, "H": 32, "I": 22})

# ---------- By module ----------
bm = wb["By module"]
bm.cell(row=16, column=1, value=("v7, 22 November 2026: the module counts of v6 stand, because one v6 item is still one row of the Sequence sheet. "
                                 "The service counts after the split are in the sheet 'By service and lane'.")).font = Font(size=9, italic=True)
bm.cell(row=16, column=1).alignment = Alignment(wrap_text=True, vertical="top")

# ---------- Pull rules ----------
pr = wb["Pull rules"]
pr["A2"] = "Applies to both recovery squads. v7, 22 November 2026: rules 1 to 6 stand; rules 7 to 12 add the microservice realignment."
pr["A2"].alignment = Alignment(wrap_text=True, vertical="top")
pr["A2"].font = Font(size=9, italic=True)
extra = [
    ("7", "Pull wave-0 platform and contract work first: the stories in the sheet 'Day 1 first' come before item 1 of the Sequence sheet (Template and Rules §R5.7.1 and §R5.7.6)"),
    ("8", "Build each delivery story against its contract story and the contract fake; a C dependency (another service's contract) never blocks, an H dependency does (Template and Rules §R5.4 and §R5.7.2)"),
    ("9", "An H dependency points only to the same service or to a platform contract story; a lane is one connected group of non-CON stories with depth at most 4 (Template and Rules §R5.7.3 and §R5.7.5)"),
    ("10", "A service is created in its Architecture v5 wave (wave 1 for P1 to P7, P9 and P10; wave 2 for P8, S2, S5 and S8; wave 3 for S1, S3, S4 and S6; wave 4 for S7 and S9), and a story whose business-epic wave is earlier keeps that earlier wave (Template and Rules §R5.6)"),
    ("11", "Only an ITG story carries an I dependency, so the cross-service behaviour is proven on the integration stories and their harness, not on a service lane (Template and Rules §R5.4 and §R5.7.4)"),
    ("12", "Release dates are unchanged and tentative; the issue tracker is not used in this run, and a change to a built item waits for its delta story (Template and Rules §R1 U2, U6 and U7)"),
]
r = 11
for a, b in extra:
    pr.cell(row=r, column=1, value=a)
    cell = pr.cell(row=r, column=2, value=b)
    cell.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1
widths(pr, {"A": 8, "B": 120})

# ---------- Owners (v7) ----------
ow = wb.create_sheet("Owners (v7)", wb.sheetnames.index("Change log") if "Change log" in wb.sheetnames else len(wb.sheetnames))
title(ow, "Owners and the Ownership Map extract used in this workbook", 1)
note(ow, ("Work-type owners are the fixed phrases of Template and Rules §R5.3 and are a suggestion only: any team may pick up the story. "
          "Service rows are the Microservice Ownership Map v1 (sheet 'Services'). No names of people. v7, 22 November 2026."), 2)
hd = ["Item", "Value"]
for c, h in enumerate(hd, 1):
    ow.cell(row=4, column=c, value=h)
style_header(ow, 4, 2)
r = 5
for k in ["CON", "APP", "DB", "INF", "OPS"]:
    ow.cell(row=r, column=1, value=f"{k} ({ {'CON': 'Contract', 'APP': 'App development', 'DB': 'ACE DB', 'INF': 'Infrastructure', 'OPS': 'DevOps'}[k] })").font = Font(bold=True)
    ow.cell(row=r, column=2, value=WT_FULL[k]).alignment = Alignment(wrap_text=True, vertical="top")
    r += 1
ow.cell(row=r, column=1, value="ITG (Integration)").font = Font(bold=True)
ow.cell(row=r, column=2, value=WT_FULL["ITG"]).alignment = Alignment(wrap_text=True, vertical="top")
r += 2
ow.cell(row=r, column=1, value="Ownership Map default rulings (Template and Rules §R3)").font = Font(bold=True, size=10)
r += 1
for k, v in [("Parameters and reference data (E1-042, E1-043)", "P3 rwb-case, contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON"),
             ("Case list API", "P3 rwb-case"),
             ("Rule package registry", "P7 rwb-decision"),
             ("Interaction ledger", "P1 rwb-source-data"),
             ("Feature flags", "Platform library (RWB-PLT-E1047-CON)")]:
    ow.cell(row=r, column=1, value=k).alignment = Alignment(wrap_text=True, vertical="top")
    ow.cell(row=r, column=2, value=v).alignment = Alignment(wrap_text=True, vertical="top")
    r += 1
r += 1
ow.cell(row=r, column=1, value="Service map (Microservice Ownership Map v1)").font = Font(bold=True, size=10)
r += 1
for c, h in enumerate(["Code", "Service", "Name", "Wave", "Schema", "REST base", "Topic", "Task queue"], 1):
    ow.cell(row=r, column=c, value=h)
style_header(ow, r, 8)
r += 1
for code in sorted(SVC, key=lambda c: (c.startswith("S"), len(c), c)):
    short, name, wave = SVC[code]
    vals = [code, short, name, wave, "rwb_" + short.replace("-", "_"), f"/api/recovery/{short}/v1",
            f"rwb.{short}.events.v1", f"rwb-{short}"]
    for c, v in enumerate(vals, 1):
        ow.cell(row=r, column=c, value=v)
    r += 1
ow.cell(row=r, column=1, value="PLT")
ow.cell(row=r, column=2, value="platform (7 platform epics, wave 0)")
ow.cell(row=r, column=4, value=0)
r += 1
ow.cell(row=r, column=1, value="ITG")
ow.cell(row=r, column=2, value="integration (4 wave epics plus NFR)")
ow.cell(row=r, column=4, value=0)
widths(ow, {"A": 34, "B": 40, "C": 24, "D": 6, "E": 22, "F": 30, "G": 30, "H": 20})

# ---------- Change log ----------
cl = wb.create_sheet("Change log")
title(cl, "Change log", 1)
cl.cell(row=2, column=1, value=HL).font = Font(size=9)
cl.cell(row=3, column=1, value=HL2).font = Font(size=9)
ch = ["Version", "Date", "Change", "Tool"]
for c, h in enumerate(ch, 1):
    cl.cell(row=5, column=c, value=h)
style_header(cl, 5, 4)
rows = [
    ("v6", "16 November 2026", "Source version: 115 Epic 1 and Epic 2 items, five review windows, 17 critical-path steps. Copied unchanged.", "(source)"),
    ("v7", "22 November 2026", "D-RCV-60 microservice realignment: every item mapped to its new stories by service and lane; pull order rebuilt so contract work and the wave-0 platform come first; new sheets 'Day 1 first', 'By service and lane', 'Owners (v7)', 'Read me' and this log; three new columns on 'By window'; three new columns on 'Critical path'; rules 7 to 12 on 'Pull rules'.", TOOL),
    ("v7", "22 November 2026", "Release dates copied unchanged and marked (tentative); the Release column keeps the v6 edition label E1, E2 or E3.", TOOL),
    ("v7", "22 November 2026", "Retired items RWB-E1-014 and RWB-TE-007 keep their rows and are not pulled (Template and Rules §R6).", TOOL),
    ("v7", "22 November 2026", CHANGE, TOOL),
]
r = 6
for row in rows:
    for c, v in enumerate(row, 1):
        cell = cl.cell(row=r, column=c, value=v)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1
widths(cl, {"A": 9, "B": 18, "C": 110, "D": 44})

# order the sheets
want = ["Read me", "Sequence", "Day 1 first", "By window", "By service and lane", "Critical path",
        "By module", "Pull rules", "Owners (v7)", "Change log"]
wb._sheets = [wb[n] for n in want] + [s for s in wb._sheets if s.title not in want]
wb.active = 0
wb.save(DST)
print("WROTE", DST)
print("sequence rows", len(items), "day1 rows", n)
