"""Build Recovery Workbench Team Start Pack v3 from the v2 copy.

The v2 deck was copied to v3 with compat/office_write.py copy; this script only
changes the copy. It adds the read-me slide at position 2, renumbers the page
number box of every numbered slide to its position, and adds six Day-1 slides at
15 to 20 in the deck's own visual grammar (Aptos, 4E297F titles, the 1.25 pt
rule, the 595959 page number box and table style {5940675A-B579-460E-94D1-54222C63F5DA}
with the DCD3EB header fill).
"""
import math
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

ROOT = Path(__file__).resolve().parents[4]
DECK = ROOT / "12 Project communication" / "Recovery Workbench Team Start Pack v3.pptx"

PURPLE = "4E297F"
HEAD_FILL = "DCD3EB"
BLACK = "000000"
GREY = "595959"
BODY = "1F1F1F"

LEFT = 566928
WIDTH = 11064240
TOP = 1051560
BOTTOM = 5600000
NOTE_TOP = 5960000
STYLE_ID = "{5940675A-B579-460E-94D1-54222C63F5DA}"

HEADER1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
HEADER2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
CHANGE = ("Change log: 3, 22 November 2026, D-RCV-60 microservice realignment, "
          "T3 Code / OpenCode / DeepSeek v4.1 Flash. The row it follows is "
          "2, 28 October 2026, the issued deck.")

DECKS = []


def rgb(hexstr):
    return RGBColor.from_string(hexstr)


def set_font(run, size, bold=False, color=BLACK):
    f = run.font
    f.name = "Aptos"
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = rgb(color)
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set("typeface", "Aptos")


def clone(slide, el, text=None):
    e = deepcopy(el)
    cNvPr = e.find(".//" + qn("p:cNvPr"))
    cNvPr.set("id", str(slide.shapes._next_shape_id))
    slide.shapes._spTree.append(e)
    shape = slide.shapes[-1]
    if text is not None:
        shape.text_frame.paragraphs[0].runs[0].text = text
    return shape


def set_style(tbl):
    tblPr = tbl._tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    for el in tblPr.findall(qn("a:tableStyleId")):
        tblPr.remove(el)
    el = tblPr.makeelement(qn("a:tableStyleId"), {})
    el.text = STYLE_ID
    tblPr.append(el)


def lines_needed(text, col_width, size):
    usable = col_width - 72000 - 54000
    char = size * 12700 * 0.52
    per_line = max(8, int(usable // char))
    total = 0
    for part in str(text).split("\n"):
        total += max(1, math.ceil(len(part) / per_line))
    return total


def add_table(slide, data, widths, top, size=None, min_row=330000, bottom=BOTTOM):
    rows, cols = len(data), len(data[0])
    if size is None:
        for cand in (13.5, 13, 12.5, 12, 11.5, 11, 10.5, 10, 9.5, 9):
            heights = []
            for r in data:
                n = max(lines_needed(v, widths[i], cand) for i, v in enumerate(r))
                heights.append(max(min_row, int(n * cand * 12700 * 1.55) + 90000))
            if top + sum(heights) <= bottom:
                size, row_h = cand, heights
                break
        else:
            raise SystemExit("no font size fits the table area")
    else:
        row_h = []
        for r in data:
            n = max(lines_needed(v, widths[i], size) for i, v in enumerate(r))
            row_h.append(max(min_row, int(n * size * 12700 * 1.55) + 90000))
        if top + sum(row_h) > bottom:
            raise SystemExit(f"table overflows at {size} pt: {top + sum(row_h)}")
    gf = slide.shapes.add_table(rows, cols, Emu(LEFT), Emu(top), Emu(sum(widths)),
                               Emu(sum(row_h)))
    tbl = gf.table
    set_style(tbl)
    for i, w in enumerate(widths):
        tbl.columns[i].width = Emu(w)
    for r, row in enumerate(data):
        tbl.rows[r].height = Emu(row_h[r])
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.margin_left = Emu(72000)
            cell.margin_right = Emu(54000)
            cell.margin_top = Emu(45000)
            cell.margin_bottom = Emu(45000)
            cell.vertical_anchor = MSO_ANCHOR.TOP
            tf = cell.text_frame
            tf.word_wrap = True
            for li, part in enumerate(str(val).split("\n")):
                p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
                run = p.add_run()
                run.text = part
                set_font(run, size, bold=(r == 0 or c == 0),
                         color=(PURPLE if r == 0 else BLACK))
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(HEAD_FILL if r == 0 else "FFFFFF")
    return top + sum(row_h)


def add_note(slide, text, top, size=10.5, width=WIDTH):
    top = min(top, 6020000)
    box = slide.shapes.add_textbox(Emu(LEFT), Emu(top), Emu(width), Emu(300000))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    set_font(run, size, color=GREY)
    return box


class Deck:
    def __init__(self):
        self.prs = Presentation(DECK)
        src = self.prs.slides[2]  # source slide 3, a numbered slide
        self.t_title = src.shapes[0]._element
        self.t_rule = src.shapes[1]._element
        self.t_num = src.shapes[2]._element
        # the release column of the release table is marked tentative (rule 10)
        for sh in self.prs.slides[3].shapes:
            if sh.has_table:
                cell = sh.table.cell(0, 1)
                if cell.text.strip() == "Release":
                    cell.text_frame.paragraphs[0].runs[0].text = "Release (tentative)"
        self.slides = []

    def new(self, title):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        clone(slide, self.t_title, title)
        clone(slide, self.t_rule)
        clone(slide, self.t_num, "0")
        self.slides.append(slide)
        return slide

    def move_to_second(self):
        # move the slide just added (the read-me) to position 2
        lst = self.prs.slides._sldIdLst
        ids = list(lst)
        lst.remove(ids[-1])
        lst.insert(1, ids[-1])

    def finish(self):
        # page number = position
        for pos, slide in enumerate(self.prs.slides, 1):
            for sh in slide.shapes:
                if (sh.has_text_frame and sh.left is not None and sh.left > 10500000
                        and sh.top is not None and sh.top > 6000000):
                    t = sh.text_frame.text.strip()
                    if t.isdigit() and sh.text_frame.paragraphs[0].runs:
                        sh.text_frame.paragraphs[0].runs[0].text = str(pos)
        cp = self.prs.core_properties
        cp.author = "Henka Group"
        cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
        cp.title = "Recovery Workbench Team Start Pack v3"
        cp.subject = "SCB Collections and Recovery"
        cp.comments = ("D-RCV-60 microservice realignment. Release dates are tentative. "
                       "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.")
        cp.revision = 3
        cp.modified = datetime(2026, 11, 22, 0, 0, 0)
        self.prs.save(DECK)
        print("WROTE", DECK, "slides", len(self.prs.slides))


def readme(deck):
    slide = deck.new("Read me: the change in this version")
    deck.move_to_second()
    box = slide.shapes.add_textbox(Emu(LEFT), Emu(TOP), Emu(WIDTH), Emu(520000))
    tf = box.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = HEADER1
    p2 = tf.add_paragraph()
    p2.text = HEADER2
    for p in (tf.paragraphs[0], p2):
        set_font(p.runs[0], 12, color=BODY)
        p.space_after = Pt(2)
    log = slide.shapes.add_textbox(Emu(LEFT), Emu(1610000), Emu(WIDTH), Emu(420000))
    ltf = log.text_frame
    ltf.word_wrap = True
    ltf.paragraphs[0].text = CHANGE
    set_font(ltf.paragraphs[0].runs[0], 10.5, color=GREY)
    data = [
        ["Item", "In this version"],
        ["Kept word for word",
         "Slides 3 to 14 are the thirteen slides of version 2, with every table, ID, "
         "number, module code and date; the release column is marked (tentative) and "
         "the page number moved."],
        ["The change",
         "The Day-1 work allocation by team type, on slides 15 to 20: 939 of the "
         "1034 stories can start on Day 1, and every team type has Day-1 work "
         "(Rules R5.7 rule 6)."],
        ["Owner rule",
         "Every owner is a team type, a service or a platform epic of the Microservice "
         "Ownership Map v1; a suggestion only, any team may pick up this story."],
        ["Dates",
         "Unchanged from version 2 and tentative; the monthly release is the only date "
         "the business sees (ASM-D2-TSP-10)."],
        ["Status",
         "Draft; no approval is recorded for this version (ASM-D2-TSP-9)."],
    ]
    bottom = add_table(slide, data, [2600000, 8464240], 2130000, bottom=5600000)
    add_note(slide, "Slides 15 to 20 are new. Every later slide of the deck is the "
                    "version 2 slide of the same content.", bottom + 120000, 10)


def s15(deck):
    slide = deck.new("Day-1 work by team type")
    data = [
        ["Team type", "Day-1 stories", "Work types", "What starts on Day 1"],
        ["TechX", "846", "CON 288, APP 418, ITG 140",
         "The contract story of every service and platform, in CG-W0 to CG-W4, and "
         "the app and integration stories that build against them"],
        ["ACE team", "11", "DB 11",
         "The 19 rwb_* schemas and logins, the PgBouncer pools and migrator role, the "
         "read-only ACE views, and the DB stories of P1, P3, P4 and P7"],
        ["SCB IT infrastructure", "18", "INF 18",
         "Kafka topics and ACLs, the Temporal namespace and codec key, Redis, the "
         "partner gateway, the schema registry, blob and Key Vault, the OCR and intake "
         "pipelines"],
        ["DevOps team", "57", "OPS 57",
         "The repository, pipeline and Helm template, dashboards and alerts, "
         "environments, secrets, quality gates, migration tooling and run books"],
        ["QA team", "7", "ITG 7",
         "The contract-test harness and synthetic data, the four wave journeys, the "
         "performance harness and the accessibility tests"],
        ["Total", "939", "",
         "Of the 1034 stories in the plan; every team type has Day-1 work "
         "(Rules R5.7 rule 6)"],
    ]
    bottom = add_table(slide, data, [1700000, 900000, 1600000, 6864240], TOP)
    add_note(slide,
             "Every row is a suggestion only: any team may pick up this story. Day 1 is "
             "computed from the build edges (Rules R5.7 rule 8), so a story whose only "
             "build edges are contract stories is Day 1. Counts: the Day-1 Work "
             "Allocation v1, built from the plan (ASM-D2-TSP-4, ASM-D2-TSP-5).",
             bottom + int((bottom - TOP) * 0.09) + 130000, 10)


def s16(deck):
    slide = deck.new("Contract first: 288 contract stories, all Day 1")
    data = [
        ["Contract group", "Contract stories", "Service epics",
         "What the group gives"],
        ["CG-W0", "17", "RWB-PLT-LIB 8, RWB-PLT-WF 7, RWB-PLT-TPL 1, RWB-PLT-EDGE 1",
         "The platform interfaces every service builds against: template, libraries, "
         "workflow kit, edge route"],
        ["CG-W1", "44", "Nine service epics, led by RWB-SVC-P3 12, RWB-SVC-P1 9 and "
                        "RWB-SVC-P5 7",
         "The contracts of the wave 1 services, ahead of their app stories"],
        ["CG-W2", "64", "Twelve service epics, led by RWB-SVC-S2 18, RWB-SVC-S5 11 and "
                        "RWB-SVC-P3 8",
         "The contracts of the wave 2 services, ahead of their app stories"],
        ["CG-W3", "71", "Seven service epics, led by RWB-SVC-S4 22, RWB-SVC-S5 14 and "
                        "RWB-SVC-S1 12",
         "The contracts of the wave 3 services, ahead of their app stories"],
        ["CG-W4", "92", "Ten service epics, led by RWB-SVC-P4 30, RWB-SVC-S7 16 and "
                        "RWB-SVC-S9 16",
         "The contracts of the wave 4 services, ahead of their app stories"],
        ["Total", "288", "",
         "Every contract story ships an interface and a fake, so a C dependency never "
         "blocks a build"],
    ]
    bottom = add_table(slide, data, [1250000, 1350000, 5600000, 2864240], TOP)
    add_note(slide,
             "A contract story has no build dependency and is always Day 1 "
             "(Rules R5.7 rule 1). One contract group is shared by every epic of its "
             "wave.", bottom + int((bottom - TOP) * 0.09) + 130000, 10)


PLATFORM = [
    ["RWB-PLT-N001-CON", "gateway-bff route contract", "Contract", "TechX",
     "RWB-PLT-EDGE"],
    ["RWB-PLT-N009-CON", "RFC 9457 problem and Idempotency-Key helpers - interface and fake",
     "Contract", "TechX", "RWB-PLT-LIB"],
    ["RWB-PLT-N010-CON", "Workflow kit templates - interface and fake", "Contract",
     "TechX", "RWB-PLT-WF"],
    ["RWB-PLT-N011-DB", "PgBouncer pools, migrator role and grant check", "ACE DB",
     "ACE team", "RWB-PLT-DB"],
    ["RWB-PLT-NF06-DB", "Create the 19 rwb_* schemas and logins", "ACE DB",
     "ACE team", "RWB-PLT-DB"],
    ["RWB-PLT-N002-INF", "Kafka topics, retry and dead-letter topics and ACLs",
     "Infrastructure", "SCB IT infrastructure", "RWB-PLT-EVT"],
    ["RWB-PLT-N003-INF", "Temporal namespace rwb-recovery and codec key",
     "Infrastructure", "SCB IT infrastructure", "RWB-PLT-WF"],
    ["RWB-PLT-N004-OPS", "Service pipeline template and Helm chart", "DevOps",
     "DevOps team", "RWB-PLT-TPL"],
    ["RWB-PLT-N005-OPS", "Platform dashboards and alerts baseline", "DevOps",
     "DevOps team", "RWB-PLT-OBS"],
    ["RWB-ITG-W1J01-ITG", "Contract-test harness and synthetic test data", "Integration",
     "QA team", "RWB-ITG-W1"],
]


def s17(deck):
    slide = deck.new("The platform work that gives every team type a Day 1")
    data = [["Story", "Title", "Work type", "Team type", "Epic"]] + PLATFORM
    bottom = add_table(slide, data, [2400000, 3750000, 1350000, 2100000, 1464240], TOP)
    add_note(slide,
             "N001 to N012 are the twelve platform stories; NF-01 to NF-08 are the "
             "platform stories moved from Epic 1; W1J01 is the integration harness. "
             "With them, every team type has Day-1 work before any service story is "
             "pulled (Rules R5.7 rule 6).", bottom + int((bottom - TOP) * 0.09) + 130000, 10)


def s18(deck):
    slide = deck.new("What each team type pulls first")
    data = [
        ["Team type", "The first Day-1 stories"],
        ["TechX",
         "RWB-PLT-N001-CON, RWB-PLT-N009-CON, RWB-PLT-N010-CON (CG-W0)\n"
         "RWB-P1-E1002-CON (case list), RWB-P2-E1007-CON (integration adapters), "
         "RWB-P3-E1018-CON (case record), all CG-W1"],
        ["ACE team",
         "RWB-PLT-NF06-DB (the 19 rwb_* schemas and logins), RWB-PLT-N011-DB "
         "(PgBouncer, migrator role and grants)\n"
         "RWB-P1-ACE001-DB (ACE DB additions), RWB-P1-E1069-DB (read-only ACE views)"],
        ["SCB IT infrastructure",
         "RWB-PLT-N002-INF (Kafka topics and ACLs), RWB-PLT-N003-INF (Temporal "
         "namespace)\n"
         "RWB-PLT-N006-INF (Redis), RWB-PLT-N007-INF (partner gateway in the DMZ)"],
        ["DevOps team",
         "RWB-PLT-NF01-OPS (repository and pipeline baseline), RWB-PLT-N004-OPS "
         "(pipeline template and Helm chart)\n"
         "RWB-PLT-NF04-OPS (secrets and configuration), RWB-PLT-N005-OPS (dashboards "
         "and alerts)"],
        ["QA team",
         "RWB-ITG-W1J01-ITG (contract-test harness and synthetic data), "
         "RWB-ITG-TE009-ITG (performance harness)\n"
         "RWB-ITG-TE010-ITG (browser and accessibility tests), RWB-ITG-W1J02-ITG "
         "(wave 1 journey)"],
    ]
    bottom = add_table(slide, data, [1900000, 9164240], TOP)
    add_note(slide,
             "These are examples from the first rows of the Day-1 Work Allocation v1, "
             "not a priority order; the order is set at the board. The tables of the "
             "first month are read by team type (ASM-D2-TSP-7).",
             bottom + int((bottom - TOP) * 0.09) + 130000, 10)


def s19(deck):
    slide = deck.new("How a team uses this pack")
    data = [
        ["Step", "What the team does"],
        ["1", "Find your team type on slide 15. The count is the Day-1 work that team "
              "type may pull, not a target"],
        ["2", "Pull a contract story first: every contract story sits in CG-W0 to CG-W4 "
              "and has no build dependency (Rules R5.7 rule 1)"],
        ["3", "Build an app story against the published contract and its fake; a C "
              "dependency never blocks the build (Rules R5.5 DP-11, R5.7 rule 2)"],
        ["4", "Wait only for an H dependency in your own lane, or for a platform "
              "contract story (Rules R5.7 rule 3)"],
        ["5", "Keep integration dependencies on the integration stories; an I "
              "dependency sits nowhere else (Rules R5.7 rule 4)"],
        ["6", "Read Ready to start on the story: if it names an in-lane story, that "
              "story comes first (Rules R5.7 rule 8)"],
    ]
    bottom = add_table(slide, data, [700000, 10364240], TOP)
    add_note(slide,
             "The full list is the Day-1 Work Allocation v1; the story text, the "
             "contract and the tests are in the Service Story Catalog v1 files, and the "
             "epics and lanes are in the Service Epics v1. Day 1 is defined by Rules "
             "R5.7 (ASM-D2-TSP-6).", bottom + int((bottom - TOP) * 0.09) + 130000, 10)


def s20(deck):
    slide = deck.new("What is still open")
    data = [
        ["CG and ASM", "What is open", "Owner role", "Proposed reading"],
        ["CG-D2-TSP-1\nASM-D2-TSP-1",
         "The kept slides say one service, one repository and one front end; this run "
         "delivers 19 services",
         "Solution architect",
         "Read the kept line as the ACE module; the 19 services are on slides 15 to 18"],
        ["CG-D2-TSP-2\nASM-D2-TSP-2",
         "The first-items slide depends on RWB-E1-004 and RWB-E1-012, which are already "
         "cancelled",
         "Delivery lead",
         "Pull from the Day-1 Work Allocation v1, not from that slide"],
        ["CG-D2-TSP-3\nASM-D2-TSP-3", "Eight epic releases, E1 to E8, and no wave",
         "Programme manager", "E1 to E8 are EP01 to EP08; waves come from Rules R5.6"],
        ["CG-D2-TSP-4\nASM-D2-TSP-4",
         "No source document gives the Day-1 count per team type", "Delivery lead",
         "The counts are those of the Day-1 Work Allocation v1"],
        ["CG-D2-TSP-5\nASM-D2-TSP-5", "The deck names no team type", "Delivery lead",
         "The five team types are those of Rules R5.3"],
        ["CG-D2-TSP-6\nASM-D2-TSP-6", "The deck has no Day 1, lane or contract group",
         "Tech lead", "Day 1 is defined by Rules R5.7 and shown on slides 15 to 19"],
        ["CG-D2-TSP-7\nASM-D2-TSP-7",
         "The first month is planned by role and by week", "Business analyst",
         "A role is read as the team type that fills it; the dates stay as issued"],
        ["CG-D2-TSP-8\nASM-D2-TSP-8",
         "The Epic 1 and 2 slide says 13 technical enabler stories; the platform adds "
         "12 stories, 8 NF stories and a harness",
         "Solution architect", "The 13 stay as issued; the added work is on slide 17"],
    ]
    bottom = add_table(slide, data, [2400000, 4550000, 1900000, 2214240], TOP,
                       min_row=300000)
    add_note(slide,
             "The full text of every point, with its evidence and a proposed answer, is "
             "in the Gap Register v1 and the Assumptions Register v1.",
             bottom + 120000, 9.5)


if __name__ == "__main__":
    deck = Deck()
    readme(deck)
    s15(deck)
    s16(deck)
    s17(deck)
    s18(deck)
    s19(deck)
    s20(deck)
    deck.finish()
