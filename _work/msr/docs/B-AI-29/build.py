"""B-AI-29: build Recovery Workbench AI and Agent Architecture v3 from the v2 copy.

The v2 deck is never edited: office_write.py copy made v3, and this script only
adds slides to the copy, moves the read-me slide to position 2 and renumbers the
page footers. Source slides keep every shape, word, ID, number and date.
"""
import copy, math, sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

LEFT, TOTAL_W = 566928, 11064240
TBL_TOP, TBL_BOTTOM = 1051560, 5600000
NOTE_TOP, NOTE_H = 5640000, 640000
PURPLE, HEAD_FILL, BODY_C, NOTE_C = "4E297F", "DCD3EB", "000000", "1F1F1F"
A_NS = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
C_EMU = 914400.0


# ---------------------------------------------------------------- shapes
def blank_layout(prs):
    for lay in prs.slide_layouts:
        if lay.name == "Blank":
            return lay
    return prs.slide_layouts[6]


def clone_part(prs, donor, names):
    s = prs.slides.add_slide(blank_layout(prs))
    bg = donor._element.cSld.find(qn("p:bg"))
    if bg is not None:
        s._element.cSld.insert(0, copy.deepcopy(bg))
    for sh in donor.shapes:
        if sh.name in names:
            s.shapes._spTree.append(copy.deepcopy(sh._element))
    return s


def shape(slide, name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise SystemExit(f"shape {name} not found")


def clone_part_shape(slide, donor, name):
    el = copy.deepcopy(shape(donor, name)._element)
    slide.shapes._spTree.append(el)
    return slide.shapes[-1]


def set_one_run(shape_obj, text):
    tf = shape_obj.text_frame
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    runs = tf.paragraphs[0].runs
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    if runs:
        runs[0].text = text
    else:  # pragma: no cover
        tf.paragraphs[0].text = text


def move_box(shape_obj, left, top, width, height):
    shape_obj.left, shape_obj.top = Emu(int(left)), Emu(int(top))
    shape_obj.width, shape_obj.height = Emu(int(width)), Emu(int(height))


# ---------------------------------------------------------------- table
def _borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        for el in tcPr.findall(qn(tag)):
            tcPr.remove(el)
    no = '<a:%s %s w="0"><a:noFill/></a:%s>'
    bot = ('<a:lnB %s w="9525" cap="flat" cmpd="sng"><a:solidFill>'
           '<a:srgbClr val="C8C8C8"/></a:solidFill><a:prstDash val="solid"/></a:lnB>')
    for tag, xml in (("a:lnB", bot % A_NS), ("a:lnT", no % ("lnT", A_NS, "lnT")),
                     ("a:lnR", no % ("lnR", A_NS, "lnR")), ("a:lnL", no % ("lnL", A_NS, "lnL"))):
        tcPr.insert(0, parse_xml(xml))


def set_cell(cell, text, size, header=False, bold=False):
    cell.margin_left, cell.margin_right = Emu(72000), Emu(54000)
    cell.margin_top, cell.margin_bottom = Emu(36000), Emu(36000)
    cell.vertical_anchor = MSO_ANCHOR.TOP
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor.from_string(HEAD_FILL if header else "FFFFFF")
    tf = cell.text_frame
    tf.clear()
    for i, line in enumerate(str(text).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.0
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        for j, chunk in enumerate(line.split("**")):
            if not chunk:
                continue
            r = p.add_run()
            r.text = chunk
            f = r.font
            f.size = Pt(size)
            f.bold = header or bold or (j % 2 == 1)
            f.name = "Aptos"
            f.color.rgb = RGBColor.from_string(PURPLE if header else BODY_C)
    _borders(cell)


def est_lines(text, width_emu, size):
    cpl = max(6, int((width_emu / C_EMU) * 72.0 / (0.50 * size)))
    return sum(max(1, math.ceil(len(part) / cpl))
               for part in str(text).replace("**", "").split("\n"))


def fit_size(rows, widths, avail):
    total = 0
    for size in (12, 11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5):
        total = 0
        for i, row in enumerate(rows):
            lines = max(est_lines(c, widths[j], size) for j, c in enumerate(row))
            total += max(lines * size * 1.30 / 72.0 * C_EMU + 2 * 36000 + 12000,
                         300000 if i == 0 else 235000)
        if total <= avail:
            return size, total
    return 7.5, total


def add_table(slide, rows, widths, label):
    assert abs(sum(widths) - TOTAL_W) <= 2000, (label, sum(widths))
    size, total = fit_size(rows, widths, TBL_BOTTOM - TBL_TOP)
    if total > TBL_BOTTOM - TBL_TOP:
        print(f"WARNING {label}: table {total} > available {TBL_BOTTOM - TBL_TOP}")
    gf = slide.shapes.add_table(len(rows), len(rows[0]), Emu(LEFT), Emu(TBL_TOP),
                                Emu(TOTAL_W), Emu(int(total)))
    tbl = gf._element.graphic.graphicData.tbl
    tblPr = tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is None:
        sid = parse_xml(f'<a:tableStyleId {A_NS}>{{5940675A-B579-460E-94D1-54222C63F5DA}}</a:tableStyleId>')
        tblPr.append(sid)
    sid.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"
    table = gf.table
    for j, w in enumerate(widths):
        table.columns[j].width = Emu(w)
    for i, row in enumerate(rows):
        lines = max(est_lines(c, widths[j], size) for j, c in enumerate(row))
        h = max(lines * size * 1.30 / 72.0 * C_EMU + 2 * 36000 + 12000,
                300000 if i == 0 else 235000)
        table.rows[i].height = Emu(int(h))
        for j, text in enumerate(row):
            set_cell(table.cell(i, j), text, size, header=(i == 0), bold=(j == 0 and i > 0))
    gf.height = Emu(int(total))
    print(f"{label}: {len(rows)} rows, {size} pt, height {total} EMU (avail {TBL_BOTTOM - TBL_TOP})")


# ---------------------------------------------------------------- slides
TITLE, RULE, FOOT, NOTE = "TextBox 1", "Connector 2", "TextBox 3", "TextBox 5"


def table_slide(prs, donor, note_donor, title, rows, widths, note, label):
    s = clone_part(prs, donor, {TITLE, RULE, FOOT})
    set_one_run(shape(s, TITLE), title)
    add_table(s, rows, widths, label)
    if note:
        nb = clone_part_shape(s, note_donor, NOTE)
        move_box(nb, LEFT, NOTE_TOP, TOTAL_W, NOTE_H)
        set_one_run(nb, note)
        size = 14 if est_lines(note, TOTAL_W, 14) <= 2 else (12 if est_lines(note, TOTAL_W, 12) <= 3 else 11)
        if size != 14:
            for p in nb.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(size)
        print(f"{label}: note {size} pt, {est_lines(note, TOTAL_W, size)} lines")
    return s


def text_slide(prs, donor, title, paras, label):
    s = clone_part(prs, donor, {TITLE, RULE, FOOT})
    set_one_run(shape(s, TITLE), title)
    box = clone_part_shape(s, donor, NOTE)
    move_box(box, LEFT, TBL_TOP, TOTAL_W, NOTE_TOP - TBL_TOP - 60000)
    tf = box.text_frame
    tf.word_wrap = True
    avail = NOTE_TOP - TBL_TOP - 120000

    def build(size):
        tf.clear()
        total = 0
        for i, (text, body_size, bold, colour) in enumerate(paras):
            sz = size if body_size else size
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.line_spacing = 1.0
            p.space_after = Pt(6)
            r = p.add_run()
            r.text = text
            r.font.size, r.font.bold, r.font.name = Pt(sz), bold, "Aptos"
            r.font.color.rgb = RGBColor.from_string(colour)
            total += est_lines(text, TOTAL_W, sz) * sz * 1.30 / 72.0 * C_EMU + 6 * 12700
        return total

    size = 12
    total = build(size)
    while total > avail and size > 9:
        size -= 0.5
        total = build(size)
    print(f"{label}: {len(paras)} paragraphs at {size} pt, height {int(total)} EMU (avail {avail})")
    if total > avail:
        print(f"WARNING {label}: text {int(total)} too tall")
    return s


# ---------------------------------------------------------------- content
def read_me():
    H, B = 14, 11.5
    return [
        ("SCB Collections and Recovery. Henka Group, 22 November 2026.", H, True, PURPLE),
        ("(C) Siam Commercial Bank and Henka Pte Ltd", H, True, PURPLE),
        ("Change log: 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / "
         "DeepSeek v4.1 Flash. It follows 2, 28 October 2026, the issued deck (the title slide and "
         "slides 3 to 12 of this version).", B, False, NOTE_C),
        ("What changes: only where the agent platform lives. Version 2 gives the Workbench an orchestrator, a tool "
         "gateway, a guardrail checker, a prompt store and a model endpoint. Version 3 gives all of them to one "
         "service, rwb-agent (P10) of the Ownership Map v1, and gives every other agent step to the service that owns "
         "the decision. No section, ID, number or date of version 2 is removed (ASM-B-AI-29-1).", B, False, NOTE_C),
        ("What is added: slides 13 to 21. 13 the change table; 14 the rwb-agent contract; 15 the six parts of source "
         "slide 5 inside the service; 16 AgentRunWorkflow step by step; 17 the 60-second rule; 18 the twelve agents "
         "and the service that starts each run; 19 the guardrails and where each is enforced; 20 autonomy and "
         "governance; 21 what stays open.", B, False, NOTE_C),
        ("Owners: every owner is a service code P1 to P10 or S1 to S9 of the Ownership Map, a platform epic "
         "(RWB-PLT-*), or a party outside the 19 services (ACE Common, Enterprise AI, COLLINS). No owner is a team "
         "type or a person (ASM-B-AI-29-5); the agent runtime is P10 rwb-agent (ASM-B-AI-29-6).", B, False, NOTE_C),
        ("Dates: version 2 carries no release date. Its document date (28 October 2026, title slide) is kept as "
         "issued, and every release date in the programme is tentative (U7, DL48; ASM-B-AI-29-4).", B, False, NOTE_C),
        ("Decisions: D-RCV-60; ADR-013 to ADR-023; DL44 to DL49. Where a value is not in the source documents this "
         "deck writes 'Not specified in the source documents' and cites the Gap Register row and the Assumptions "
         "Register row, as in (CG-B-AI-29-3; ASM-B-AI-29-10).", B, False, NOTE_C),
        ("Status: Draft. No approval is recorded for this version (ASM-B-AI-29-2). The title slide stays first and "
         "this slide second, so every slide of version 2 keeps its content and its order (ASM-B-AI-29-3).",
         B, False, NOTE_C),
    ]


CHANGE_ROWS = [
    ["Version 2 says (source slide)", "Version 3", "Owner, decision and assumption"],
    ["An orchestrator, a tool gateway, a guardrail checker, a versioned prompt and policy store and an evaluation "
     "harness sit beside the model; no agent holds a credential (5, 8)",
     "All six are components of rwb-agent; a tool call is a REST call on the owner's contract, one hop, 2 s",
     "P10 and the tool's owner · ADR-013, ADR-014, ADR-020, DP-01, DP-11 (ASM-B-AI-29-6)"],
    ["The model endpoint is 'a private endpoint in the SCB tenant' (DL33; 5, 11)",
     "The Enterprise AI private endpoint INT-23, called by rwb-agent only",
     "P10 · CG-B-AI-29-2; ASM-B-AI-29-15"],
    ["If the agent does not answer within 60 seconds, the rule result is used and the fallback is recorded (8; DL11)",
     "AgentRunWorkflow on queue rwb-agent with a 60 s timer; the caller's rule result stands",
     "P10 and the caller · ADR-016, DP-10 (CG-B-AI-29-8)"],
    ["Every agent proposal and action is written to the decision log on the same terms as a person's (8)",
     "A local decision record in rwb_agent, then DecisionRecorded; P7 keeps the ledger",
     "P10, P7 · DP-03, ADR-022 (ASM-B-AI-29-11)"],
    ["Twelve agents run in the Workbench; three of them run as children of a case (4, 6)",
     "Each run is an AgentRunWorkflow child, started by the service that owns the stage decision",
     "P5, S8, S1 to S7, P8 · DP-12 (CG-B-AI-29-3)"],
    ["The models run in COLLINS and ACE, and the Workbench reads their output from the daily load (7)",
     "P1 alone reads the ACE views; rwb-agent reads the same products as a tool through P1",
     "P1, P10 · ADR-010, DP-05 (CG-B-AI-29-9)"],
    ["Autonomy steps from shadow to L4 on measured results, and the committee, Model Risk, the centre of excellence, "
     "the Enterprise AI team and audit govern the agents (9, 10)",
     "Unchanged; the level is policy data in rwb_agent and the six who govern sit outside the 19 services",
     "P10, P7 · DP-04 (ASM-B-AI-29-13, ASM-B-AI-29-17)"],
]

CONTRACT_ROWS = [
    ["Contract element", "rwb-agent (P10)", "Source"],
    ["Service",
     "rwb-agent, wave 1, schema rwb_agent, one login, package th.co.scb.ace.workbench.recovery.agent",
     "Ownership Map v1; Rules R4"],
    ["REST base", "/api/recovery/agent/v1: GET /agent-runs/{id}, GET/POST /agent-policies (admin)",
     "Ownership Map v1; slide 16"],
    ["REST consumed", "P1 rwb-source-data: read case facts (tool) · P5 rwb-document: read extracted fields (tool)",
     "Slide 16"],
    ["Outside call", "Enterprise AI private endpoint (INT-23), HTTPS; no other caller, no credential in the agent",
     "Slides 7, 8 and 16"],
    ["Events consumed", "DocumentStored (intake) · CaseCreated (screening)", "Slide 16; rows 01 and 16"],
    ["Events published", "AgentRunCompleted on rwb.agent.events.v1, consumed by P7, P5 and S8",
     "Slides 16 and 43 (row 28)"],
    ["Temporal", "AgentRunWorkflow on task queue rwb-agent in namespace rwb-recovery: 60 s, then rule result",
     "Slide 16; Ownership Map v1"],
    ["Tables owned", "rwb_agent: agent policies, prompts, runs, guardrails, evaluations", "Slides 16 and 41"],
    ["Not owned", "The screen that calls GET /agent-runs/{id} is a gateway-bff composite route (DP-19)",
     "CG-B-AI-29-10"],
]

COMPONENT_ROWS = [
    ["Component (source slide 5)", "What it is inside rwb-agent", "Call type", "Owner"],
    ["Orchestrator",
     "AgentRunWorkflow: finds the step, the agent and its autonomy level, and holds the run to its 60 s",
     "Temporal workflow", "P10"],
    ["Tool gateway",
     "The only outbound path: one REST call on the owner's published contract for each read; the gateway holds the "
     "workload identity, the agent holds no credential",
     "REST, one hop, 2 s", "P10; P1 and P5 as the tools"],
    ["Guardrail checker",
     "An activity after the model answer: schema check, allowed actions and confidence floor, before any output is used",
     "Temporal activity", "P10"],
    ["Prompt and policy store",
     "The agent policies and prompts tables in rwb_agent, versioned so any run can be reproduced",
     "DB read, own schema", "P10"],
    ["Evaluation harness",
     "Labelled sets and their scores in the evaluations table; scored before a version or a level is used",
     "Batch, offline", "P10; Model Risk validates"],
    ["Model endpoint",
     "One HTTPS call per run to the Enterprise AI private endpoint (INT-23); no other service calls it",
     "HTTPS private endpoint", "P10; Enterprise AI team runs it"],
]

WORKFLOW_ROWS = [
    ["Step", "Where", "What happens", "Call type"],
    ["1", "P5, S8 or the stage owner", "DocumentStored, CaseCreated or a REST request names the agent and the case",
     "Event or REST"],
    ["2", "P10 rwb-agent",
     "AgentRunWorkflow starts on queue rwb-agent; the caller holds the child handle and passes caseId, step and run",
     "Temporal child"],
    ["3", "P10 rwb-agent",
     "The policy of the step is read: agent, autonomy level, prompt version, allowed actions, confidence floor",
     "DB read"],
    ["4", "P10 rwb-agent",
     "The tool gateway reads only the fields the step needs: case facts through P1, extracted fields through P5",
     "REST, one hop, 2 s"],
    ["5", "P10 rwb-agent", "The model is called on the Enterprise AI private endpoint (INT-23) with the versioned prompt",
     "HTTPS"],
    ["6", "P10 rwb-agent",
     "The guardrail checker tests the answer against its schema, the allowed actions and the floor", "Activity"],
    ["7", "P10 rwb-agent",
     "The 60 s timer; if it fires, the rule result of the step is used and the fallback is written (R-UNI-32)",
     "Temporal timer"],
    ["8", "P10 rwb-agent",
     "The run, the versions, the output and the fallback are written to rwb_agent, with the local decision record",
     "DB write and outbox"],
    ["9", "P10 rwb-agent", "AgentRunCompleted is published; the stage owner applies the outcome to its decision",
     "Event"],
    ["10", "P7 rwb-decision", "Collects DecisionRecorded into the central ledger within five minutes", "Event"],
]

FALLBACK_ROWS = [
    ["When", "What happens", "Recorded where", "Owner"],
    ["No answer within 60 s (source slide 8; DL11)",
     "The timer of AgentRunWorkflow fires; the rule result of the step is used and the case does not wait",
     "The run row in rwb_agent, with the reason", "P10 and the stage owner"],
    ["The answer fails its schema check",
     "The answer is not used; the rule result stands and the failure is written",
     "The run row in rwb_agent", "P10"],
    ["The answer proposes an action outside the allowed list",
     "The action is refused; where the level is advised the proposal goes to a person with its reasons",
     "The run row, and the person's task", "P10 and the stage owner"],
    ["The confidence is below the floor",
     "The output goes to a person and the rule result is used meanwhile (source slide 8)",
     "The run row, and the person's task", "P10 and the stage owner"],
    ["The model endpoint does not answer (INT-23)",
     "The run ends as a fallback; the rule result stands; the outage is counted in the measures",
     "The run row and the P10 measures", "P10"],
    ["Which rule supplies the result (twelve agents)",
     "R-UNI-32 names the route and pricing agents only; for the other ten the package and version are not in a source",
     "Not specified in the source documents (CG-B-AI-29-6; ASM-B-AI-29-7)", "P7 rwb-decision"],
]

AGENT_ROWS = [
    ["Agent (source slide 6)", "Started by (service and workflow)", "First in", "Source"],
    ["Intake agent", "P5 rwb-document, DocumentIntakeWorkflow (classify / extract run)", "E2", "Slide 16"],
    ["Screening agent", "S8 rwb-deviation, DeviationWorkflow (screening agent run)", "E2", "Slide 15"],
    ["Settlement and restructure agent", "S2 rwb-treatment, TreatmentWorkflow", "E3", "ASM-B-AI-29-10"],
    ["Valuation agent", "S1 rwb-valuation, RouteDecisionWorkflow", "E3", "ASM-B-AI-29-10"],
    ["Pricing agent", "S5 rwb-asset, AssetDisposalWorkflow", "E3", "ASM-B-AI-29-10"],
    ["Route agent", "S1 rwb-valuation, RouteDecisionWorkflow (child: route agent)", "E4", "Slide 18"],
    ["Guarantee claim agent", "S3 rwb-guarantee, GuaranteeClaimWorkflow", "E4", "ASM-B-AI-29-10"],
    ["Reconciliation agent", "P8 rwb-payment, matchPayments", "E4", "ASM-B-AI-29-10"],
    ["Legal document agent", "S4 rwb-litigation, LitigationWorkflow", "E5", "ASM-B-AI-29-10"],
    ["Debt sale agent", "S6 rwb-debtsale, DebtSaleWorkflow", "E5", "ASM-B-AI-29-10"],
    ["Write-off agent", "S7 rwb-writeoff, WriteOffWorkflow", "E6", "ASM-B-AI-29-10"],
    ["Tracing agent", "S8 rwb-deviation (X6 lost contact)", "E7", "ASM-B-AI-29-10"],
]

GUARDRAIL_ROWS = [
    ["Guardrail (source slide 8)", "Where it is enforced in version 3", "Owner"],
    ["Tool gateway",
     "A REST call on the owner's contract only (P1, P5, INT-23); the identity is the workload identity of rwb-agent",
     "P10; P1 and P5"],
    ["Allowed actions",
     "A column of the policy row in rwb_agent, checked after the answer and before the action is proposed",
     "P10"],
    ["Schema check", "The guardrail activity, before any output is used by the stage owner", "P10"],
    ["Confidence floor",
     "A column of the policy row; below it the output goes to a person and the rule result is used", "P10"],
    ["Fallback", "The 60 s timer of AgentRunWorkflow; the fallback is written to the run row",
     "P10 and the stage owner"],
    ["No personal data in prompts beyond need",
     "Field-level reads through P1 and P5; masking policy from P4; the PDPA lint runs in the evaluation harness",
     "P10; P4"],
    ["Versioned prompts and policies",
     "Every run row records the prompt, policy, model and agent versions; a version is never overwritten", "P10"],
    ["Decision log",
     "The local decision record in rwb_agent, then DecisionRecorded on rwb.decision-record.v1; P7 keeps the ledger",
     "P10; P7"],
]

AUTONOMY_ROWS = [
    ["Level (source slide 9)", "Who acts in version 3", "Where the level is held", "What is measured before the next step"],
    ["Shadow", "P10 runs the agent beside the rule; the output is logged and not shown",
     "Policy row in rwb_agent", "Agreement with the rule and with people's decisions on a labeled set"],
    ["L1 recommend", "P10 proposes; a person decides; the stage owner records the decision",
     "Policy row in rwb_agent", "Acceptance rate, override reasons, outcome against the rule"],
    ["L2 act in a band", "P10 acts inside the band a person set; the stage owner applies it and a person reviews a sample",
     "Policy row in rwb_agent", "Sample error rate, exception rate, outcome measures"],
    ["L3 act across the decision", "P10 acts across the decision; people review by exception",
     "Policy row in rwb_agent", "Outcome measures by route and product; complaints"],
    ["L4 act and close", "P10 acts and closes; people monitor the measures",
     "Policy row in rwb_agent", "Outcome measures; model risk review"],
]

OPEN_ROWS = [
    ["What is open", "Placeholder and assumption", "Owner role"],
    ["The autonomy levels let an agent act; Architecture v5 says a person approves",
     "CG-B-AI-29-1; ASM-B-AI-29-18", "Strategy and model committee"],
    ["The endpoint of DL33, its tenant, region and version", "CG-B-AI-29-2; ASM-B-AI-29-15",
     "Enterprise AI team and solution architect"],
    ["Nine of the twelve agents have no service row that starts the run",
     "CG-B-AI-29-3; ASM-B-AI-29-10", "Solution architect"],
    ["The tool gateway: a P10 component or a shared one", "CG-B-AI-29-4; ASM-B-AI-29-8", "P10 rwb-agent"],
    ["Who holds the AgentRunWorkflow handle and the parent-child link",
     "CG-B-AI-29-5; ASM-B-AI-29-9", "P10 rwb-agent"],
    ["The rule result of a fallback, for ten of the twelve agents",
     "CG-B-AI-29-6; ASM-B-AI-29-7", "P7 rwb-decision"],
    ["Who may change a prompt or a policy, and with what approval",
     "CG-B-AI-29-7; ASM-B-AI-29-13", "Centre of excellence and P10"],
    ["Whether the 60 s covers the whole run or the model call",
     "CG-B-AI-29-8; ASM-B-AI-29-7", "P10 rwb-agent"],
    ["Model output on the daily load: P1's contract or a direct read",
     "CG-B-AI-29-9; ASM-B-AI-29-16", "P1 rwb-source-data"],
    ["The run screen and its gateway-bff route", "CG-B-AI-29-10; ASM-B-AI-29-12",
     "Platform architect"],
]


def main(path):
    prs = Presentation(path)
    donor = prs.slides[5]       # source slide 6: title, rule, footer, table
    note_donor = prs.slides[6]  # source slide 7: the note text box
    added = []

    added.append(text_slide(prs, note_donor, "Version 3: the change log and how to read this deck",
                            read_me(), "read-me"))
    added.append(table_slide(
        prs, donor, note_donor, "What the realignment changes in the agent architecture", CHANGE_ROWS,
        [4100000, 4600000, 2364240],
        "Version 2 is kept word for word; this table is the reading key. Every row names an owner of the Ownership "
        "Map v1, and every open point is on slide 21.", "change"))
    added.append(table_slide(
        prs, donor, note_donor, "rwb-agent (P10): the contract of the agent runtime", CONTRACT_ROWS,
        [1900000, 6700000, 2464240],
        "Transcribed from the Architecture v5 service contract on slide 16 and the Ownership Map v1. The topic, the "
        "queue, the schema and the login are the service's own (Rules R4).", "contract"))
    added.append(table_slide(
        prs, donor, note_donor, "Inside rwb-agent: the six parts of slide 5, placed", COMPONENT_ROWS,
        [2100000, 6200000, 1300000, 1464240],
        "The six parts of source slide 5 are components of one deployable, not separate services (ASM-B-AI-29-6). A "
        "tool call is a REST call on the owner's contract (ADR-020; ASM-B-AI-29-8), and the labelled sets of the "
        "harness are the evaluations table (ASM-B-AI-29-14).", "components"))
    added.append(table_slide(
        prs, donor, note_donor, "AgentRunWorkflow: one agent run, step by step", WORKFLOW_ROWS,
        [560000, 1900000, 6910000, 1694240],
        "One run, from the event that starts it to the ledger. The 60 s of step 7 is the timer of the workflow "
        "(CG-B-AI-29-8; ASM-B-AI-29-7); the parent-child link is ASM-B-AI-29-9.", "workflow"))
    added.append(table_slide(
        prs, donor, note_donor, "The 60-second rule, and what the caller does then", FALLBACK_ROWS,
        [2500000, 4700000, 2200000, 1664240],
        "The rule is uniform in the sources: 60 s, then the rule result, and the fallback is recorded (source slide "
        "8; Architecture v5 slide 16). Only R-UNI-32 names a rule, and only for two agents.", "fallback"))
    added.append(table_slide(
        prs, donor, note_donor, "The twelve agents and the service that starts each run", AGENT_ROWS,
        [2900000, 5620000, 780000, 1764240],
        "Rows 1, 2 and 6 are drawn on a service contract of Architecture v5; the other nine follow the stage owner "
        "(CG-B-AI-29-3; ASM-B-AI-29-10). AgentRunCompleted returns to the service that started the run, which applies "
        "the outcome. The live and shadow epics are those of source slide 6 and do not change.",
        "agents"))
    added.append(table_slide(
        prs, donor, note_donor, "The guardrails, and where each one is enforced", GUARDRAIL_ROWS,
        [2600000, 6800000, 1664240],
        "The eight rows are source slide 8; only the place is added. The policy, prompt and floor live in rwb_agent, "
        "the masking policy in P4 and the ledger in P7.", "guardrails"))
    added.append(table_slide(
        prs, donor, note_donor, "Autonomy: who acts at each level, and where it is held", AUTONOMY_ROWS,
        [2100000, 4400000, 2000000, 2564240],
        "The five levels and their measures are source slide 9, unchanged. The level is configuration, not code "
        "(ASM-B-AI-29-17); every step up is still approved by the strategy and model committee with Model Risk "
        "(source slide 10; ASM-B-AI-29-13).", "autonomy"))
    added.append(table_slide(
        prs, donor, note_donor, "What this version leaves open", OPEN_ROWS,
        [5600000, 3400000, 2064240],
        "These ten points are the ones this version cannot close from the source documents; each is a row of the Gap "
        "Register and the Assumptions Register. The open decisions of source slide 11 (DL33, DL11, DL26) stay open "
        "and are read as slides 13, 16 and 19 do.", "open"))

    # read-me slide goes second: the title slide of version 2 stays first
    lst = prs.slides._sldIdLst
    ids = list(lst)
    lst.remove(ids[-10])
    lst.insert(1, ids[-10])

    # page footers follow the position, so no number repeats
    for n, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.name == FOOT and sh.has_text_frame and sh.text_frame.text.strip().isdigit():
                set_one_run(sh, str(n))

    cp = prs.core_properties
    cp.author = "Henka Group"
    cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
    cp.title = "Recovery Workbench AI and Agent Architecture v3"
    cp.revision = 3
    import datetime
    cp.modified = datetime.datetime(2026, 11, 22, 9, 0, 0)
    cp.created = datetime.datetime(2026, 11, 22, 9, 0, 0)
    prs.save(path)
    print("SLIDES", len(prs.slides._sldIdLst))


if __name__ == "__main__":
    main(sys.argv[1])
