"""B-TECH-15: build Recovery Workbench Information Flow v6 from the v5 copy.

The v5 deck is never edited: office_write.py copy makes v6, and this script only
adds slides to the copy, moves the read-me slide to position 2 and renumbers the
page footers. Source slides keep every shape, word, ID, number and date.
"""
import copy, math, sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

LEFT, TOTAL_W = 566928, 11064240
TBL_TOP, TBL_BOTTOM = 1097280, 5700000
NOTE_TOP, NOTE_H = 5700000, 560000
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


def set_one_run(shape_obj, text):
    tf = shape_obj.text_frame
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    runs = tf.paragraphs[0].runs
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    if runs:
        runs[0].text = text
    else:  # pragma: no cover - every donor has a run
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
    for size in (12, 11, 10, 9.5, 9, 8.5, 8, 7.5):
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
                                Emu(TOTAL_W), Emu(total))
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
    print(f"{label}: {len(rows)} rows, {size} pt, height {total} EMU")
    return size, total


# ---------------------------------------------------------------- slide shapes
TITLE, RULE, FOOT, NOTE = "TextBox 1", "Connector 2", "TextBox 3", "TextBox 5"


def new_table_slide(prs, donor, title, rows, widths, note, label, number_holder):
    s = clone_part(prs, donor, {TITLE, RULE, FOOT, NOTE})
    set_one_run(shape(s, TITLE), title)
    add_table(s, rows, widths, label)
    nb = shape(s, NOTE)
    move_box(nb, LEFT, NOTE_TOP, TOTAL_W, NOTE_H)
    set_one_run(nb, note)
    size_note = 14 if est_lines(note, TOTAL_W, 14) <= 2 else (12 if est_lines(note, TOTAL_W, 12) <= 3 else 11)
    if size_note != 14:
        for p in nb.text_frame.paragraphs:
            for r in p.runs:
                r.font.size = Pt(size_note)
    print(f"{label}: note {size_note} pt, {est_lines(note, TOTAL_W, size_note)} lines")
    number_holder.append(s)
    return s


def new_text_slide(prs, donor, title, paras, label, number_holder):
    s = clone_part(prs, donor, {TITLE, RULE, FOOT})
    set_one_run(shape(s, TITLE), title)
    box = clone_part_shape(s, donor, NOTE)
    move_box(box, LEFT, TBL_TOP, TOTAL_W, NOTE_TOP - TBL_TOP - 120000)
    tf = box.text_frame
    tf.clear()
    total = 0
    for i, (text, size, bold, colour) in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.0
        p.space_after = Pt(6)
        r = p.add_run()
        r.text = text
        r.font.size, r.font.bold, r.font.name = Pt(size), bold, "Aptos"
        r.font.color.rgb = RGBColor.from_string(colour)
        lines = est_lines(text, TOTAL_W, size)
        total += lines * size * 1.30 / 72.0 * C_EMU + 6 * 12700
    print(f"{label}: {len(paras)} paragraphs, height {int(total)} EMU "
          f"(box {NOTE_TOP - TBL_TOP - 120000})")
    if total > NOTE_TOP - TBL_TOP - 160000:
        print(f"WARNING {label}: text {int(total)} too tall")
    number_holder.append(s)
    return s


def clone_part_shape(slide, donor, name):
    src = shape(donor, name)
    el = copy.deepcopy(src._element)
    slide.shapes._spTree.append(el)
    return slide.shapes[-1]


# ---------------------------------------------------------------- content
def read_me_paras():
    return [
        ("SCB Collections and Recovery. Henka Group, 22 November 2026.", 14, True, PURPLE),
        ("(C) Siam Commercial Bank and Henka Pte Ltd", 14, True, PURPLE),
        ("Change log: 6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / "
         "DeepSeek v4.1 Flash. It follows 5, 15 November 2026, the issued deck (the title slide and "
         "slides 3 to 12 of this version).", 12, False, NOTE_C),
        ("What changes: only the flows between services. Where version 5 says 'the Workbench', 'the "
         "Workbench module' or names a module, version 6 names the service that owns the flow in the "
         "Microservice Ownership Map v1. No flow, ID, number or date of version 5 is removed "
         "(ASM-B-TECH-15-1).", 12, False, NOTE_C),
        ("What is added: slides 13 to 22. 13 is the change table; 14 and 15 give the information each of the 19 "
         "services owns; 16 and 17 the events that carry it; 18 follows one payment end to end; 19 gives the five "
         "call types; 20 the shared platform; 21 the owner of each fallback; 22 what stays open.", 12, False, NOTE_C),
        ("Owners: every owner is a service code P1 to P10 or S1 to S9 of the Ownership Map, a platform "
         "epic (RWB-PLT-*), or a party outside the 19 services (ACE Common, WIN, NSS, LINE OA, "
         "partners, debt buyers). No owner is a team type or a person (ASM-B-TECH-15-14). The wave of "
         "a flow is the wave of the service that owns it (ASM-B-TECH-15-15).", 12, False, NOTE_C),
        ("Dates: version 5 carries no release date. The document dates (15 November 2026 on the title "
         "slide, 22 November 2026 here) are kept as issued, and every release date in the programme is "
         "tentative (U7, DL48; ASM-B-TECH-15-13).", 12, False, NOTE_C),
        ("Decisions: D-RCV-60; ADR-013 to ADR-023; DL44 to DL49. Where a value is not in the source "
         "documents this deck writes 'Not specified in the source documents' and cites the Gap Register "
         "row and the Assumptions Register row, as in (CG-B-TECH-15-1; ASM-B-TECH-15-4).", 12, False, NOTE_C),
        ("Status: Draft. No approval is recorded for this version (ASM-B-TECH-15-2). The title slide "
         "stays first and this slide second, so every slide of version 5 keeps its content and its "
         "order (ASM-B-TECH-15-3).", 12, False, NOTE_C),
    ]


CHANGE_ROWS = [
    ["Version 5 says (source slide)", "Version 6", "Owner", "Decision"],
    ["Reads the 30 views; writes in the ACE database (2, 3)",
     "P1 alone reads the views; 19 rwb_* schemas, one login each, no cross-schema read",
     "P1; 19 services", "ADR-010, ADR-014, DP-01, DP-02"],
    ["One module holds case, rules, log, documents, partners (2)",
     "P3 case · P7 decision · P5 document · S9 partner", "P3, P7, P5, S9", "ADR-013"],
    ["Kafka only for personal data access logging (3)",
     "Plus 19 topics rwb.<short>.events.v1 and the shared rwb.decision-record.v1",
     "each service", "ADR-015, DP-09"],
    ["O04, O05: daily batch to the data lake (6)",
     "No data lake: P9 projects from events; the O05 model-learning path stays open",
     "P9", "ADR-018, DP-17"],
    ["O02: registered mail, file from the Workbench (6)",
     "P6 writes the notice; P2 delivers the daily file (JOB-10, INT-14)", "P6, P2", "DP-16"],
    ["O03: SMS and LINE through the ACE notification path (6)",
     "Same path, one caller", "P6", "ADR-019"],
    ["I13, O06: partner results and instructions (5, 6)",
     "Partner portal and partner gateway, one owner", "S9", "ADR-019"],
    ["I14: documents arrive at the document hub (5)",
     "Blob with WORM, one owner", "P5", "ADR-014"],
    ["I15: the guarantee officer enters quota and deadlines (5)",
     "Entered on the claim that owns them", "S3", "ADR-013"],
    ["I16: users and roles, group-to-role, iam_group (5)",
     "P4 holds roles, scope, masking and DoA; P1 reads the view; sign-in stays ACE Common",
     "P4, P1", "DP-08, DP-05"],
    ["O08: audit, PII and SOC events (6)",
     "Unchanged: every service writes through ACE Common", "each service", "ADR-023"],
    ["The Workbench is the only system carrying the case identifier (11)",
     "P3 owns caseId: the key of every event and the workflow ID", "P3", "ADR-011, DP-12"],
]

PLATFORM_ROWS = [
    ["Code", "Service and topic", "Wave", "Information it takes in", "Information it sends out"],
    ["P1", "rwb-source-data\nrwb.source-data.events.v1", "1",
     "The 30 recovery.v_ace_* views, read only; the ACE batch record; the business date from Airflow",
     "GET /customers/{id}, /accounts/{id}, /freshness; AceDataReady, AceDataLate; the ledger"],
    ["P2", "rwb-integration\nrwb.integration.events.v1", "1",
     "deliverFile and receiveFile tasks; the Airflow windows for WIN (16:00) and the buyer files",
     "FileDelivered, FileFailed; the WIN file (INT-14); the encrypted buyer file (INT-25)"],
    ["P3", "rwb-case\nrwb.case.events.v1", "1",
     "Every case event; AceDataReady; RulePackageInForce; the CaseWorkflow parent",
     "CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged, TimerBreached"],
    ["P4", "rwb-access\nrwb.access.events.v1", "1",
     "POST /authorise from every service; ACE Common sign-in and group-to-role",
     "AccessPolicyChanged, DoaLimitChanged; the DoA table and masking policies, cached"],
    ["P5", "rwb-document\nrwb.document.events.v1", "1",
     "POST /documents; AgentRunCompleted for classification; DocumentIntakeWorkflow",
     "DocumentStored, DocumentFieldsExtracted; the file in Blob with WORM"],
    ["P6", "rwb-comms\nrwb.comms.events.v1", "1",
     "POST /notices; DeviationRaised/Cleared, TreatmentApproved, PaymentMissed, CaseStateChanged",
     "NoticeGenerated, NoticeDispatched, NoticeDelivered; SMS and LINE through ACE Common"],
    ["P7", "rwb-decision\nrwb.decision.events.v1", "1",
     "DecisionRecorded from all 19; NoticeGenerated; AgentRunCompleted; ApprovalWorkflow",
     "ApprovalRequested, ApprovalDecided, RulePackageInForce; the central ledger and its WORM seal"],
    ["P8", "rwb-payment\nrwb.payment.events.v1", "2",
     "AceDataReady; TreatmentApproved, LotAwarded, AssetSold, WriteOffApproved",
     "TreatmentBooked, PaymentMissed, ProceedsMatched; the posting file through P2"],
    ["P9", "rwb-reporting\nrwb.reporting.events.v1", "1",
     "Every business event as a projection; DecisionRecorded; the measures Schedule at 01:30",
     "ReportPublished; the regulatory extract through P2; the read model that replaces the lake"],
    ["P10", "rwb-agent\nrwb.agent.events.v1", "1",
     "DocumentStored and CaseCreated; AgentRunWorkflow: 60 s, then a rule result",
     "AgentRunCompleted; case facts through P1, extracted fields through P5"],
]

STAGE_ROWS = [
    ["Code", "Service and topic", "Wave", "Information it takes in", "Information it sends out"],
    ["S1", "rwb-valuation\nrwb.valuation.events.v1", "3",
     "RulePackageInForce; the RouteDecisionWorkflow child; collateral and appraisals through P1",
     "RouteDecided"],
    ["S2", "rwb-treatment\nrwb.treatment.events.v1", "2",
     "TreatmentBooked, PaymentMissed, DeviationRaised; the TreatmentWorkflow sagas",
     "TreatmentApproved, TreatmentClosed; the restructure calculation through Nexus to ACE Common"],
    ["S3", "rwb-guarantee\nrwb.guarantee.events.v1", "3",
     "NoticeDelivered, ProceedsMatched; the quota and claim deadlines entered on the claim (I15)",
     "GuaranteeClaimFiled, GuaranteeClaimSettled; the guarantor notice through P6"],
    ["S4", "rwb-litigation\nrwb.litigation.events.v1", "3",
     "NoticeDelivered, PartnerResultSubmitted; LitigationWorkflow with Continue-As-New",
     "LawsuitFiled, JudgmentRecorded, AuctionResult; instructions to law firms through S9"],
    ["S5", "rwb-asset\nrwb.asset.events.v1", "2",
     "JudgmentRecorded, AuctionResult, ProceedsMatched; the monthly re-appraisal",
     "AssetTakenOn, AssetSold; instructions to auction vendors through S9"],
    ["S6", "rwb-debtsale\nrwb.debtsale.events.v1", "3",
     "ProceedsMatched; the data room pack from P5; the DebtSaleWorkflow saga",
     "LotAwarded, AccountsTransferred; the buyer file through P2 (INT-25)"],
    ["S7", "rwb-writeoff\nrwb.writeoff.events.v1", "4",
     "AceDataReady for the GL posting (I12 through P1); ProceedsMatched; WriteOffWorkflow",
     "WriteOffApproved"],
    ["S8", "rwb-deviation\nrwb.deviation.events.v1", "2",
     "CaseCreated, AceDataReady (deceased and bankrupt flags), AgentRunCompleted",
     "DeviationRaised, DeviationCleared; party flags through P1"],
    ["S9", "rwb-partner\nrwb.partner.events.v1", "4",
     "The partner portal /partner/v1/* through the partner gateway (FAPI 2.0); instruction tasks",
     "InstructionIssued, PartnerResultSubmitted; partner uploads into P5"],
]

EVENT_ROWS_1 = [
    ["Event", "Producer", "Consumers", "Topic"],
    ["AceDataReady", "P1", "P3, P8, S8, S7", "rwb.source-data.events.v1"],
    ["AceDataLate", "P1", "alerts, gateway-bff banner", "rwb.source-data.events.v1"],
    ["CaseCreated", "P3", "P10, S8, P9", "rwb.case.events.v1"],
    ["CaseStateChanged", "P3", "P6, P9", "rwb.case.events.v1"],
    ["DeviationRaised", "S8", "P3, P6, S2", "rwb.deviation.events.v1"],
    ["DeviationCleared", "S8", "P3, P6", "rwb.deviation.events.v1"],
    ["DocumentStored", "P5", "P10, P3", "rwb.document.events.v1"],
    ["DocumentFieldsExtracted", "P5", "P3", "rwb.document.events.v1"],
    ["PartnerResultSubmitted", "S9", "S4, S5, P3", "rwb.partner.events.v1"],
    ["RulePackageInForce", "P7", "P3, S1, S2, P8", "rwb.decision.events.v1"],
]

EVENT_ROWS_2 = [
    ["Event", "Producer", "Consumers", "Topic"],
    ["TreatmentApproved", "S2", "P6, P8", "rwb.treatment.events.v1"],
    ["TreatmentBooked", "P8", "P3, S2", "rwb.payment.events.v1"],
    ["PaymentMissed", "P8", "P3, S2, P6", "rwb.payment.events.v1"],
    ["ProceedsMatched", "P8", "P3, S5, S6, S7, S3", "rwb.payment.events.v1"],
    ["NoticeGenerated", "P6", "P7", "rwb.comms.events.v1"],
    ["NoticeDispatched", "P6", "P9", "rwb.comms.events.v1"],
    ["NoticeDelivered", "P6", "S4, S3, P3", "rwb.comms.events.v1"],
    ["WriteOffApproved", "S7", "P3, P8, P9", "rwb.writeoff.events.v1"],
    ["DecisionRecorded", "all 19", "P7 (the ledger), P9", "rwb.decision-record.v1"],
]

PATH_ROWS = [
    ["Step", "Where", "What happens", "Call type"],
    ["1", "ACE ingestion", "Posts the day's payments and closes the business date (I02); outside the 19 services", "Batch"],
    ["2", "P1 rwb-source-data", "Reads v_ace_payment and v_ace_batch_status and publishes AceDataReady", "Event"],
    ["3", "P3 rwb-case", "DailyCaseRun starts on AceDataReady (JOB-02) and allocates by 07:00 (JOB-03)", "Workflow"],
    ["4", "P8 rwb-payment", "matchPayments finds no payment for the case (JOB-07)", "Activity"],
    ["5", "P8 rwb-payment", "Writes PaymentMissed to its outbox in the same transaction as the state change", "Event"],
    ["6", "P3 rwb-case", "The case router dedupes in its inbox and signals the CaseWorkflow", "Signal"],
    ["7", "S2 rwb-treatment", "The running TreatmentWorkflow evaluates R-RES-27 and starts the 30-day cure period",
     "Activity, timer"],
    ["8", "S2 rwb-treatment", "RecordAndApply writes the decision record, the state and the outbox in one transaction",
     "Activity"],
    ["9", "P7 rwb-decision", "Collects DecisionRecorded into the ledger within 5 minutes; P9 projects it", "Event"],
]

CALL_ROWS = [
    ["Call type", "What travels", "Who owns the path", "Contract and limit", "Never"],
    ["REST", "A person waits: a screen read, or one command",
     "gateway-bff asks the owner, one hop",
     "OpenAPI 3.1, /v1 in the path; 2 s; GET retried once; a breaker per downstream",
     "A call chain deeper than one hop"],
    ["Kafka event", "A fact others may react to; IDs and facts, no personal data",
     "The producer, on its own topic",
     "AsyncAPI 3.0, CloudEvents 1.0 binary; retry 1 min, 10 min, 1 h, then .dlt",
     "Personal data in an event; an event used as a command"],
    ["Temporal", "A step in another service, or a long process",
     "The service that owns the workflow or activity, queue rwb-<short>",
     "A typed interface in a contract jar; workflow ID = the business key",
     "I/O or personal data in workflow code"],
    ["File", "Bulk data, or a party outside the bank", "P2 rwb-integration",
     "A manifest with fileId, sha256 and record count; a SAS link, one file, 15 minutes",
     "Data inside the message"],
    ["SQL view", "ACE source data, read only", "P1 rwb-source-data, the only reader",
     "The 30 recovery.v_ace_* views; 5 s statement timeout; read-only login",
     "Another service reading the views or the tables"],
]

PLATFORM2_ROWS = [
    ["Part", "Owner", "What it holds", "Where this deck uses it"],
    ["gateway-bff and Redis", "Shared platform, not a row of the Ownership Map (CG-B-TECH-15-1; ASM-B-TECH-15-4)",
     "The session, the short-lived user JWT, at most a few parallel calls per screen",
     "Every screen read (source slide 10)"],
    ["Kafka", "The bank's Kafka platform; one topic and ACL per service",
     "19 topics rwb.<short>.events.v1 and the shared rwb.decision-record.v1", "Every event on slides 16 and 17"],
    ["Temporal", "The platform workflow kit; one queue per service",
     "Namespace rwb-recovery, queue rwb-<short>, the CaseWorkflow and the stage children",
     "The workflows and timers of slides 8, 9 and 18"],
    ["Airflow", "The bank's scheduler (replaces Control-M)",
     "The ACE ingestion DAG, the business-date hand-off, the WIN and buyer file windows, the extract",
     "JOB-02, 04, 07, 08, 10, 15"],
    ["Blob with WORM", "P5 rwb-document", "Every file and its retention, 2.8 TB by 2031", "I14, O07"],
    ["The 30 recovery.v_ace_* views", "P1 rwb-source-data",
     "The only read path out of ACE source data; read-only login", "I01 to I12, I16"],
    ["ACE Common", "The ACE team, outside the 19 services",
     "Sign-in, audit and PII logging, the shared case view, the restructure calculator, notifications",
     "I16, O03, O08, and the DoA limits of P4"],
]

FALLBACK_ROWS = [
    ["When (source slide 8)", "Owner", "What it sends", "What the user sees"],
    ["An ACE source is late", "P1", "AceDataLate at the cut-off; the data product marked stale",
     "The age of the data on every screen that uses it"],
    ["ACE refuses a feed", "P1", "The last complete business date, read through v_ace_batch_status",
     "The same, with the product marked stale"],
    ["A weekly or monthly source is late", "P1", "AceDataLate one business day after the ACE batch was due",
     "The age of the data on the case"],
    ["A decision input is older than its age limit", "S1, S2, S4, S5, S7", "A held task naming the input and its age",
     "Which input is out of date and how to refresh it"],
    ["A score is missing for an account", "S1", "A route decision without the score; P7 records the missing input",
     "No score, and the reason"],
    ["A booking is not seen on the next ACE business date", "P8",
     "A task to the officer who recorded the booking; the case stays waiting", "The booking marked as not confirmed"],
    ["An outbound file is not acknowledged", "P2",
     "A retry; after the third failure FileFailed and a task to the owning team", "The notice marked as not sent"],
]

OPEN_ROWS = [
    ["What is open", "Placeholder and assumption", "Owner role"],
    ["The owner of gateway-bff, the Redis session and the App Gateway route; the Map has no row",
     "CG-B-TECH-15-1; ASM-B-TECH-15-4", "Platform team, RWB-PLT-EDGE"],
    ["The model-learning batch (O05) has no path now that the data lake is removed",
     "CG-B-TECH-15-2; ASM-B-TECH-15-5", "Reporting and the model owner"],
    ["Source slide 8 reads ace_batch_run, a table; ADR-010 allows the 30 views only",
     "CG-B-TECH-15-3; ASM-B-TECH-15-6", "P1 rwb-source-data"],
    ["Which services read the interaction ledger, and how", "CG-B-TECH-15-4; ASM-B-TECH-15-7", "P1 rwb-source-data"],
    ["Which service records a partner result, S9 or the dated data product of P1",
     "CG-B-TECH-15-5; ASM-B-TECH-15-8", "S9 rwb-partner"],
    ["Users and roles: sign-in, group-to-role and the iam_group view", "CG-B-TECH-15-6; ASM-B-TECH-15-9",
     "P4 rwb-access"],
    ["Who builds SMS and LINE dispatch (DL30 stays open)", "CG-B-TECH-15-7; ASM-B-TECH-15-10", "P6 rwb-comms"],
    ["The WIN file window JOB-10 is written by two services", "CG-B-TECH-15-8; ASM-B-TECH-15-11", "P6 and P2"],
    ["Two Kafka roles: PII logging and the 19 business topics", "CG-B-TECH-15-9; ASM-B-TECH-15-12",
     "Solution architect"],
]


def main(path):
    prs = Presentation(path)
    donor = prs.slides[3]          # source slide 4: title, rule, footer, table, note
    holder = []

    new_text_slide(prs, donor, "Version 6: the change log and how to read this deck",
                   read_me_paras(), "read-me", holder)
    new_table_slide(prs, donor, "What the realignment changes in the information flow", CHANGE_ROWS,
                    [3400000, 4300000, 1200000, 2164240],
                    "Version 5 is kept word for word; this table is the reading key. Every row is a flow of the "
                    "source deck and every owner is a row of the Ownership Map v1. Slide 22 lists the nine points "
                    "the source does not close.",
                    "change", holder)
    new_table_slide(prs, donor, "The ten platform services and the information they own", PLATFORM_ROWS,
                    [620000, 2200000, 560000, 3700000, 3984240],
                    "In and out per service, transcribed from the Architecture v5 service contracts (slides 14 to 20); "
                    "the topic is the service's own, rwb.<short>.events.v1 (ASM-B-TECH-15-16). Wave: Rules R4 and "
                    "Architecture v5 slide 38 (ASM-B-TECH-15-15).",
                    "platform", holder)
    new_table_slide(prs, donor, "The nine stage services and the information they own", STAGE_ROWS,
                    [620000, 2200000, 560000, 3700000, 3984240],
                    "The stage services run as children of the CaseWorkflow on their own queue, rwb-<short>. No service "
                    "reads another service's tables (DP-01); ACE data comes through P1's contract or the service's own "
                    "ACE views (DP-05).",
                    "stage", holder)
    new_table_slide(prs, donor, "The events that carry the information, and their owners 1/2", EVENT_ROWS_1,
                    [2600000, 1400000, 3300000, 3764240],
                    "Every event carries IDs and facts, never personal data; the key is caseId; the producer writes its "
                    "outbox in the same transaction (DP-09, ADR-015). These ten are the facts of the data, the case "
                    "and the platforms.",
                    "events1", holder)
    new_table_slide(prs, donor, "The events that carry the information, and their owners 2/2", EVENT_ROWS_2,
                    [2600000, 1400000, 3300000, 3764240],
                    "These nine are the working facts of a case. Architecture v5 slides 42 and 43 carry the full "
                    "catalogue of 30 events; the source slides of this deck use only the rows on slides 16 and 17.",
                    "events2", holder)
    new_table_slide(prs, donor, "One payment's path: from ACE to the ledger, service by service", PATH_ROWS,
                    [700000, 2400000, 6300000, 1664240],
                    "Architecture v5 slide 22 and the Temporal and Drools design slide 14 carry the same path for "
                    "PaymentMissed; every other fact in this deck travels the same way, and only the owner and the "
                    "event change (ASM-B-TECH-15-1).",
                    "path", holder)
    new_table_slide(prs, donor, "Five call types, and the owner of each path", CALL_ROWS,
                    [1100000, 2600000, 2400000, 3200000, 1764240],
                    "The five call types and their limits are Architecture v5 slides 11 and 12; the owner of each path "
                    "is a row of the Ownership Map v1. Events announce, Temporal commands, REST answers people.",
                    "calls", holder)
    new_table_slide(prs, donor, "The shared platform: what is not one of the 19 services", PLATFORM2_ROWS,
                    [2400000, 2700000, 3600000, 2364240],
                    "These parts are named by the source slides but are not rows of the 19-service table; each flow "
                    "that crosses them is named on the source slide that uses it.",
                    "shared", holder)
    new_table_slide(prs, donor, "The owner of each fallback when a flow does not arrive", FALLBACK_ROWS,
                    [3000000, 1400000, 4100000, 2564240],
                    "The seven rows are source slide 8; only the owner is added. The decision to raise a task, a timer "
                    "or a state change stays in the service that owns the case stage.",
                    "fallback", holder)
    new_table_slide(prs, donor, "What this version leaves open", OPEN_ROWS,
                    [5000000, 3600000, 2464240],
                    "These nine points are the ones this version cannot close from the source documents; each is a row "
                    "of the Gap Register and the Assumptions Register. The open decision-log rows of source slide 11 "
                    "(DL06, DL30, DL43) stay open and are not repeated here.",
                    "open", holder)

    # read-me slide goes second: title slide of version 5 stays first
    lst = prs.slides._sldIdLst
    ids = list(lst)
    lst.remove(ids[-11])
    lst.insert(1, ids[-11])

    # page footers follow the position, so no number repeats
    for n, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.name == FOOT and sh.has_text_frame and sh.text_frame.text.strip().isdigit():
                set_one_run(sh, str(n))

    cp = prs.core_properties
    cp.author = "Henka Group"
    cp.last_modified_by = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
    cp.title = "Recovery Workbench Information Flow v6"
    cp.revision = 6
    import datetime
    cp.modified = datetime.datetime(2026, 11, 22, 9, 0, 0)
    cp.created = datetime.datetime(2026, 11, 22, 9, 0, 0)
    prs.save(path)
    print("SLIDES", len(prs.slides._sldIdLst))


if __name__ == "__main__":
    main(sys.argv[1])
