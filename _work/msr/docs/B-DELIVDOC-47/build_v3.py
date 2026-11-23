# Build the v3 deck: keep slides 2-6 word for word, add header lines to slide 1,
# and append one run-book slide set. Scratch only; never touches the source.
import copy
from pptx import Presentation
from pptx.util import Inches, Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

DST = r"11 Delivery and operations/Recovery Workbench Run Operating Model v3.pptx"
PURPLE = RGBColor(0x4E, 0x29, 0x7F)
HEAD_FILL = RGBColor(0xDC, 0xD3, 0xEB)
GREY = RGBColor(0x59, 0x59, 0x59)
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

prs = Presentation(DST)
TEMPLATE = prs.slides[1]  # slide 2 carries the design elements


def clone_design(slide, num, title):
    for sh in TEMPLATE.shapes:
        if sh.has_table:
            continue
        if sh.shape_type == 19:  # table
            continue
        el = copy.deepcopy(sh._element)
        slide.shapes._spTree.append(el)
    for sh in slide.shapes:
        if sh.name == "TextBox 1":
            sh.text_frame.paragraphs[0].runs[0].text = title
        elif sh.name == "TextBox 3":
            sh.text_frame.paragraphs[0].runs[0].text = str(num)


def cell_border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        for e in tcPr.findall(qn(tag)):
            tcPr.remove(e)
    for tag in ("a:lnL", "a:lnR", "a:lnT"):
        el = etree.SubElement(tcPr, qn(tag))
        el.set("w", "0")
        etree.SubElement(el, qn("a:noFill"))
    el = etree.SubElement(tcPr, qn("a:lnB"))
    el.set("w", "9525")
    el.set("cap", "flat")
    solid = etree.SubElement(el, qn("a:solidFill"))
    etree.SubElement(solid, qn("a:srgbClr")).set("val", "C8C8C8")
    etree.SubElement(el, qn("a:prstDash")).set("val", "solid")


def _row_height(cells, widths, pt):
    """Estimate the height one row needs, so the table is neither cramped nor empty."""
    import math
    best = 0.0
    for c, val in enumerate(cells):
        usable = max(0.4, widths[c] - 0.15)
        cpi = 15.0 * 8.0 / pt
        lines = 0
        for part in str(val).split("\n"):
            lines += max(1, math.ceil(len(part) / max(1.0, usable * cpi)))
        best = max(best, lines * pt * 1.30 / 72.0 + 0.11)
    return best


def add_table(slide, rows, widths, left=0.45, top=1.12, bottom=6.45, header_pt=9.5, body_pt=8.0):
    nr, nc = len(rows), len(rows[0])
    pt = body_pt
    while pt > 6.5:
        heights = [max(0.26, _row_height(rows[0], widths, header_pt))]
        heights += [max(0.3, _row_height(rows[r], widths, pt)) for r in range(1, nr)]
        if sum(heights) <= bottom - top:
            break
        pt -= 0.5
    height = sum(heights)
    gf = slide.shapes.add_table(nr, nc, Inches(left), Inches(top), Inches(sum(widths)), Inches(height))
    tbl = gf.table
    tbl._tbl.tblPr.set("firstRow", "0")
    tbl._tbl.tblPr.set("bandRow", "0")
    style = tbl._tbl.tblPr.find(qn("a:tableStyleId"))
    if style is None:
        style = etree.SubElement(tbl._tbl.tblPr, qn("a:tableStyleId"))
    style.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"
    for i, w in enumerate(widths):
        tbl.columns[i].width = Inches(w)
    for r in range(nr):
        tbl.rows[r].height = Inches(heights[r])
    for r in range(nr):
        for c in range(nc):
            cell = tbl.cell(r, c)
            cell.margin_left = Emu(72000)
            cell.margin_right = Emu(54000)
            cell.margin_top = Emu(32000)
            cell.margin_bottom = Emu(32000)
            cell.vertical_anchor = MSO_ANCHOR.TOP
            cell_border(cell)
            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = HEAD_FILL
            else:
                cell.fill.background()
            tf = cell.text_frame
            tf.word_wrap = True
            parts = str(rows[r][c]).split("\n")
            for i, part in enumerate(parts):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                run = p.add_run()
                run.text = part
                f = run.font
                f.name = "Aptos"
                f.size = Pt(header_pt if r == 0 else pt)
                f.bold = r == 0
                f.color.rgb = PURPLE if r == 0 else RGBColor(0, 0, 0)
    return gf


def add_note(slide, text, top=6.62, size=8.5):
    box = slide.shapes.add_textbox(Inches(0.45), Inches(top), Inches(12.4), Inches(0.34))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run.font.color.rgb = GREY
    return box


def add_bullets(slide, items, top=1.2, size=13.5):
    box = slide.shapes.add_textbox(Inches(0.55), Inches(top), Inches(12.2), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        lead, rest = item
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = lead + " "
        r1.font.name = "Aptos"
        r1.font.size = Pt(size)
        r1.font.bold = True
        r1.font.color.rgb = PURPLE
        r2 = p.add_run()
        r2.text = rest
        r2.font.name = "Aptos"
        r2.font.size = Pt(size)
        r2.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    return box


# ---------------------------------------------------------------- slide 1
cover = prs.slides[0]
head = cover.shapes.add_textbox(Inches(0.62), Inches(0.08), Inches(10.2), Inches(0.42))
tf = head.text_frame
tf.word_wrap = False
p = tf.paragraphs[0]
r = p.add_run()
r.text = "SCB Collections and Recovery. Henka Group, 22 November 2026."
r.font.name = "Aptos"
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(0xD8, 0xCE, 0xEA)
p2 = tf.add_paragraph()
r2 = p2.add_run()
r2.text = "(C) Siam Commercial Bank and Henka Pte Ltd"
r2.font.name = "Aptos"
r2.font.size = Pt(9)
r2.font.color.rgb = RGBColor(0xD8, 0xCE, 0xEA)
sp = head._element
cover.shapes._spTree.remove(sp)
cover.shapes._spTree.insert(2, sp)

foot = cover.shapes.add_textbox(Inches(0.62), Inches(6.62), Inches(12.0), Inches(0.3))
fr = foot.text_frame.paragraphs[0].add_run()
fr.text = "3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
fr.font.name = "Aptos"
fr.font.size = Pt(9)
fr.font.color.rgb = RGBColor(0xCF, 0xC4, 0xE4)

# ---------------------------------------------------------------- new slides
LAYOUT = [l for l in prs.slide_layouts if l.name == "Blank"][0]
SERV_NOTE = ("Owner: the service code in the Ownership Map v1; the team is a suggestion only, "
             "any team may pick up this story (U3; DL46). Service owner for the run: Not specified "
             "in the source documents (CG-B-DELIVDOC-47-1; ASM-B-DELIVDOC-47-1).")

spec = []

spec.append(dict(
    n=7, title="What changed in version 3", kind="table",
    widths=[0.85, 2.15, 2.45, 2.55, 4.4],
    rows=[
        ["Version", "Date", "Decision", "Tool", "What changed"],
        ["3", "22 November 2026", "D-RCV-60 microservice realignment",
         "T3 Code / OpenCode / DeepSeek v4.1 Flash",
         "One run book page per service for the 19 services (slides 8 to 17); every owner from the "
         "Ownership Map v1; decisions DL44 to DL49 added; the five version 2 slides of tiers, "
         "service levels, hours, escalation and DL02 kept word for word; release dates unchanged "
         "and tentative (DL48)."],
        ["2", "28 October 2026 (the date on the source cover)",
         "Not stated in the source documents (CG-B-DELIVDOC-47-5; ASM-B-DELIVDOC-47-5)",
         "Not stated in the source documents (CG-B-DELIVDOC-47-5; ASM-B-DELIVDOC-47-5)",
         "The source deck: tiers, service levels, hours and shifts, escalation and the DL02 "
         "decision, kept on slides 2 to 6."],
    ],
    note=("The source has no change log, so no row before version 2 is reconstructed "
          "(CG-B-DELIVDOC-47-5; ASM-B-DELIVDOC-47-5). Status: Draft; no approval is recorded in "
          "this run (U8; CG-B-DELIVDOC-47-7; ASM-B-DELIVDOC-47-7).")))

spec.append(dict(
    n=8, title="The service shape: what a run book covers", kind="bullets",
    items=[
        ("Nineteen services.", "P1 to P10 platform, S1 to S9 route. Each one has its own schema and "
         "login, the REST base /api/recovery/<short>/v1, the topic rwb.<short>.events.v1 with its retry "
         "and .dlt topics, and the task queue rwb-<short> (Template and Rules R4)."),
        ("Waves.", "1 for P1 to P7, P9 and P10; 2 for P8, S2, S5 and S8; 3 for S1, S3, S4 and S6; 4 "
         "for S7 and S9 (Ownership Map v1, Services sheet)."),
        ("Service template.", "Every service comes from it: own schema and login, outbox and inbox, a "
         "Temporal worker, a local decision record and DecisionRecorded, OpenTelemetry (Architecture "
         "v5 slide 20)."),
        ("Shared pieces.", "Not counted in the 19: gateway-bff with the Redis session, the partner "
         "gateway in the DMZ, Kafka, Temporal in namespace rwb-recovery, Airflow and observability "
         "(Architecture v5 slide 20 note)."),
        ("One page per service.", "what it runs, what to look at first, who owns it and where it "
         "escalates. The source deck has none, so version 3 adds the pages on slides 10 to 13 "
         "(CG-B-DELIVDOC-47-6; ASM-B-DELIVDOC-47-6)."),
        ("Owner.", "the service code in the Ownership Map v1; the team is a suggestion only, TechX "
         "unless a DB, INF, OPS or ITG story names another owner (U3; Template and Rules R5.3; DL46)."),
    ]))

spec.append(dict(
    n=9, title="Run book per service: the eight steps", kind="table",
    widths=[0.62, 2.55, 5.2, 3.98],
    rows=[
        ["Step", "Do", "Look at", "Stop when"],
        ["1", "Open the service's page and confirm health",
         "GET /health and GET /metrics on the service; the service dashboard",
         "health green and the error rate back to its normal band"],
        ["2", "Confirm the worker polls its own queue",
         "Temporal UI, namespace rwb-recovery, queue rwb-<short>; the KEDA backlog",
         "the backlog falls and the workers scale"],
        ["3", "Clear the topic",
         "the retry topics at 1 min, 10 min and 1 h, then the .dlt topic with an alert; the replay tool",
         "no message in the .dlt topic and the alert closed"],
        ["4", "Confirm events left the outbox",
         "the outbox table in the service's schema; DecisionRecorded on rwb.decision-record.v1",
         "the outbox empty and the 5-minute ledger target met"],
        ["5", "Check the service's Schedules",
         "the service's Schedules in Temporal; the times are on its run book page",
         "each Schedule ran at its time"],
        ["6", "Check the decision record",
         "the local decision record, hash-linked, in the service's schema; the central ledger in P7 rwb-decision",
         "the chain check passes and no gap alert is open"],
        ["7", "Check the calls it depends on",
         "contract dependencies (C) never block; integration dependencies (I) only on ITG stories (Template and Rules R5.4)",
         "the caller's circuit breaker is closed"],
        ["8", "Record and escalate",
         "severity from slide 3; escalation from slide 5 and slide 17; owner from slide 15",
         "the ticket closes with the restore time met"],
    ],
    note=("The alert thresholds and the per-service dashboard: Not specified in the source documents "
          "(CG-B-DELIVDOC-47-3; ASM-B-DELIVDOC-47-3). The desk uses the four severity bands on slide 3 "
          "until they are stated."),
    header_pt=10.0, body_pt=11.0))

P_ROWS_1 = [
    ["Service", "Wave and owner", "Schema, queue and topic", "What runs", "First check"],
    ["P1 rwb-source-data\nSource data", "Wave 1\nP1; TechX",
     "rwb_source_data\nqueue rwb-source-data\nrwb.source-data.events.v1",
     "AceIngestCheck, reconciliation; listEligibleAccounts, snapshot(page); the 30 v_ace_* views",
     "GET /freshness; the 05:30 AceDataLate alarm; the Airflow DAG's last task; the fallback poll of "
     "the ACE batch record"],
    ["P2 rwb-integration\nIntegration and files", "Wave 1\nP2; TechX",
     "rwb_integration\nqueue rwb-integration\nrwb.integration.events.v1",
     "deliverFile(manifest), receiveFile; the WIN file at 16:00; the buyer files per lot",
     "GET /interface-runs; POST /interface-runs/{id}/retry; FileFailed and the 16:00 window"],
    ["P3 rwb-case\nCase and workflow", "Wave 1\nP3; TechX",
     "rwb_case\nqueue rwb-case\nrwb.case.events.v1",
     "CaseWorkflow, one per case; DailyCaseRun (Schedule and AceDataReady); allocate, transfer, rebalance",
     "DailyCaseRun finished; CaseAllocationFailed; the CaseWorkflow count in Temporal UI"],
    ["P4 rwb-access\nAccess and authority", "Wave 1\nP4; TechX",
     "rwb_access\nqueue rwb-access\nrwb.access.events.v1",
     "POST /authorise with the cached answer; the six-monthly access review Schedule",
     "POST /authorise answers; the cache refresh on AccessPolicyChanged and DoaLimitChanged"],
    ["P5 rwb-document\nDocument hub", "Wave 1\nP5; TechX",
     "rwb_document\nqueue rwb-document\nrwb.document.events.v1",
     "DocumentIntakeWorkflow (OCR, classify, extract); the retention Schedule; Azure Blob WORM",
     "DocumentStored without DocumentFieldsExtracted; Blob write errors; the retention run"],
]

P_ROWS_2 = [
    ["Service", "Wave and owner", "Schema, queue and topic", "What runs", "First check"],
    ["P6 rwb-comms\nCommunications", "Wave 1\nP6; TechX",
     "rwb_comms\nqueue rwb-comms\nrwb.comms.events.v1",
     "NoticeDispatchWorkflow; the letter generated in P5; WIN letters through P2; ACE Common SMS and LINE",
     "NoticeDispatched without NoticeDelivered; the ACE Common notification path; the WIN letter file"],
    ["P7 rwb-decision\nDecision centre and log", "Wave 1\nP7; TechX",
     "rwb_decision\nqueue rwb-decision\nrwb.decision.events.v1",
     "ApprovalWorkflow; rule promote 00:01; chain check 02:00; the daily ledger seal to WORM",
     "ledger completeness against the 5-minute target; the 02:00 chain check; RulePackageInForce after 00:01"],
    ["P8 rwb-payment\nPayments and posting", "Wave 2\nP8; TechX",
     "rwb_payment\nqueue rwb-payment\nrwb.payment.events.v1",
     "matchPayments, confirmBookings, postProceeds (saga step); the posting file to P2",
     "payments matched for the business date; PaymentMissed; the posting file delivered"],
    ["P9 rwb-reporting\nReporting", "Wave 1\nP9; TechX",
     "rwb_reporting\nqueue rwb-reporting\nrwb.reporting.events.v1",
     "measures at 01:30 (Schedule); buildRegulatoryExtract; snapshot(page) from P1",
     "measures finished at 01:30 and ReportPublished; the regulatory extract file; projection lag on Kafka"],
    ["P10 rwb-agent\nAgent runtime", "Wave 1\nP10; TechX",
     "rwb_agent\nqueue rwb-agent\nrwb.agent.events.v1",
     "AgentRunWorkflow, 60 s and then the rule result; the tool gateway read-only calls; the Enterprise AI endpoint",
     "AgentRunCompleted rate and the 60 s fallback; the Enterprise AI endpoint; switch rwb-agent off if it misbehaves"],
]

S_ROWS_1 = [
    ["Service", "Wave and owner", "Schema, queue and topic", "What runs", "First check"],
    ["S1 rwb-valuation\nValuation and route", "Wave 3\nS1; TechX",
     "rwb_valuation\nqueue rwb-valuation\nrwb.valuation.events.v1",
     "RouteDecisionWorkflow, a child of the case; the route agent; the approval child",
     "RouteDecided for the day's cases; RulePackageInForce picked up; collateral and appraisal reads from P1"],
    ["S2 rwb-treatment\nTDR, settlement, DIL", "Wave 2\nS2; TechX",
     "rwb_treatment\nqueue rwb-treatment\nrwb.treatment.events.v1",
     "TreatmentWorkflow; the settlement and DIL sagas; the restructure calculator through Nexus",
     "TreatmentApproved and TreatmentClosed; the plan timers; the Nexus call into ace-collection"],
    ["S3 rwb-guarantee\nGuarantees", "Wave 3\nS3; TechX",
     "rwb_guarantee\nqueue rwb-guarantee\nrwb.guarantee.events.v1",
     "GuaranteeClaimWorkflow; the guarantor notice child; the approval child",
     "GuaranteeClaimFiled without GuaranteeClaimSettled; NoticeDelivered missing; the workflow age"],
    ["S4 rwb-litigation\nLitigation and enforcement", "Wave 3\nS4; TechX",
     "rwb_litigation\nqueue rwb-litigation\nrwb.litigation.events.v1",
     "LitigationWorkflow, years and continues-as-new; the law firm instruction; the demand notice child",
     "instruction SLAs on rwb-partner; hearings without PartnerResultSubmitted; the continue-as-new run"],
    ["S5 rwb-asset\nAssets and auction", "Wave 2\nS5; TechX",
     "rwb_asset\nqueue rwb-asset\nrwb.asset.events.v1",
     "AssetDisposalWorkflow; the monthly re-appraisal (Schedule); the auction vendor instruction",
     "the monthly re-appraisal Schedule; AuctionResult; AssetSold without ProceedsMatched"],
]

S_ROWS_2 = [
    ["Service", "Wave and owner", "Schema, queue and topic", "What runs", "First check"],
    ["S6 rwb-debtsale\nDebt sale", "Wave 3\nS6; TechX",
     "rwb_debtsale\nqueue rwb-debtsale\nrwb.debtsale.events.v1",
     "DebtSaleWorkflow, a saga with the transfer as pivot; the data room pack; the buyer file through P2",
     "LotAwarded without AccountsTransferred; the buyer file delivery; the saga's pivot step"],
    ["S7 rwb-writeoff\nWrite-off and recovery", "Wave 4\nS7; TechX",
     "rwb_writeoff\nqueue rwb-writeoff\nrwb.writeoff.events.v1",
     "WriteOffWorkflow; the scan on the 3rd working day (Schedule); the committee approval child",
     "the 3rd-working-day scan ran; WriteOffApproved; posting held until the central ledger confirms"],
    ["S8 rwb-deviation\nDeviation handling", "Wave 2\nS8; TechX",
     "rwb_deviation\nqueue rwb-deviation\nrwb.deviation.events.v1",
     "DeviationWorkflow, a child of the case; X1 to X7 screening; the screening agent run",
     "DeviationRaised without DeviationCleared; the paused stage timer; the screening agent run"],
    ["S9 rwb-partner\nPartner management", "Wave 4\nS9; TechX",
     "rwb_partner\nqueue rwb-partner\nrwb.partner.events.v1",
     "InstructionWorkflow with SLA timers; issueInstruction, recordResult; the partner portal on FAPI 2.0",
     "instruction SLA timers; PartnerResultSubmitted; the partner gateway and MFA"],
]

for n, title, rows in [
    (10, "Run book per service: platform P1 to P5", P_ROWS_1),
    (11, "Run book per service: platform P6 to P10", P_ROWS_2),
    (12, "Run book per service: route S1 to S5", S_ROWS_1),
    (13, "Run book per service: route S6 to S9", S_ROWS_2),
]:
    spec.append(dict(n=n, title=title, kind="table", rows=rows,
                     widths=[2.0, 1.55, 2.95, 2.75, 3.15], note=SERV_NOTE,
                     header_pt=10.0, body_pt=11.0))

spec.append(dict(
    n=14, title="Run book for the shared platform", kind="table",
    widths=[2.5, 2.4, 5.0, 2.5],
    rows=[
        ["Piece", "Who runs it", "What to check", "Escalate to"],
        ["gateway-bff with the Redis session", "platform (PLT); SCB IT",
         "one hop and the 2 s timeout per service; the session store; a breaker per service",
         "SCB IT incident manager"],
        ["Partner gateway (DMZ)", "platform (PLT); SCB IT",
         "FAPI 2.0; the partner client certificates; MFA", "SCB IT incident manager"],
        ["Kafka", "the bank and ACE platform team",
         "consumer lag per group; the retry topics; the .dlt alerts; the replay tool", "ACE team"],
        ["Temporal", "platform (PLT)",
         "namespace rwb-recovery; the queue backlog; JOB-21, the stuck workflow scan every 5 min",
         "platform team"],
        ["ACE PostgreSQL", "ACE DBA",
         "one login per schema; the capped pools per service; per-schema monitoring", "ACE team"],
        ["Airflow", "the bank platform; SCB IT",
         "the ACE ingestion DAG; POST /business-days/{date}/ready; the SLA alerts at 05:30 and 07:00",
         "data lead"],
        ["Observability", "platform (PLT); SCB IT",
         "one trace across the services; ACE PII logs to the SOC; per-service metrics", "SCB IT"],
    ],
    note=("Escalation follows slide 5. The rota for the shared pieces: Not specified in the source "
          "documents (CG-B-DELIVDOC-47-4; ASM-B-DELIVDOC-47-4)."),
    header_pt=10.0, body_pt=10.5))

spec.append(dict(
    n=15, title="Who owns what: the Ownership Map owners", kind="table",
    widths=[3.7, 5.2, 3.5],
    rows=[
        ["Area", "Owner", "Stated in"],
        ["Services, tables, endpoints, events, workflows and jobs",
         "the service code P1 to P10 and S1 to S9", "Ownership Map v1, Services and Tables sheets"],
        ["Parameters and reference data (E1-042, E1-043)", "P3 rwb-case", "R3 default ruling"],
        ["Case list API", "P3 rwb-case", "R3 default ruling"],
        ["Rule package registry", "P7 rwb-decision", "R3 default ruling"],
        ["Interaction ledger", "P1 rwb-source-data", "R3 default ruling"],
        ["Feature flags",
         "the platform library (PLT); the admin paths served by P2 rwb-integration",
         "R3 default ruling; Ownership Map v1 Rulings"],
        ["Outbox, inbox and idempotency tables",
         "the platform library, created in every service schema", "Ownership Map v1 Rulings"],
        ["Service owner for the run",
         "Not specified in the source documents (CG-B-DELIVDOC-47-1; ASM-B-DELIVDOC-47-1)",
         "gap in this version"],
        ["Tier 1, tier 2 and tier 3 roles per service",
         "Not specified in the source documents (CG-B-DELIVDOC-47-2; ASM-B-DELIVDOC-47-2)",
         "gap in this version"],
    ],
    note=("Each owner above is the owner recorded in the Ownership Map v1 or in the R3 default "
          "rulings; no owner is invented in this deck."),
    header_pt=10.0, body_pt=10.5))

spec.append(dict(
    n=16, title="Hours, rota and on call, per service", kind="table",
    widths=[2.3, 4.8, 5.3],
    rows=[
        ["Item", "Design kept from version 2", "Per service in version 3"],
        ["Business hours", "08:00 to 20:00 on business days; tier 1 and tier 2 on duty",
         "the service's suggested owner is on duty for its own page, slides 10 to 13"],
        ["Early shift",
         "05:00 to 08:00 on business days: data steward on call for the loads and the morning chain",
         "P1 rwb-source-data first, then P3 rwb-case (DailyCaseRun), then the route services in play"],
        ["Outside hours", "SCB IT on call for severity 1; platform administrator on call by rota",
         "one rota page per service: Not specified in the source documents (CG-B-DELIVDOC-47-4; ASM-B-DELIVDOC-47-4)"],
        ["Release weekends", "ACE team and the squads on call for the change window",
         "the service's wave, 1 to 4, as printed on its page"],
    ],
    note=("The four rows of version 2 are kept; the right-hand column is the only change, so that a "
          "page exists for each of the 19 services."),
    header_pt=10.0, body_pt=11.0))

spec.append(dict(
    n=17, title="Escalation, per service", kind="table",
    widths=[3.2, 6.3, 2.9],
    rows=[
        ["Issue", "Goes to", "When"],
        ["Severity 1", "the service's suggested owner, then the application owner and the SCB IT incident manager", "at once"],
        ["Missed restore time", "Head of the Chief Debt Recovery Management Office", "at the restore time"],
        ["Data load late", "the P1 rwb-source-data owner, then the data steward, then the data lead", "07:00, then 09:00"],
        ["Agent behaving wrongly",
         "the P10 rwb-agent owner, then the risk and model risk officer; the autonomy level is lowered", "at once"],
        ["Decision record gap", "the P7 rwb-decision owner; the 5-minute completeness alert and the chain check", "at once"],
        ["Stuck workflow", "the platform team; JOB-21, the visibility query every 5 minutes", "at once"],
    ],
    note=("The first four rows are those of version 2, with the service owner inserted for the 19 "
          "services; the last two rows are new for the target architecture."),
    header_pt=10.0, body_pt=11.0))

spec.append(dict(
    n=18, title="Decisions added in version 3", kind="table",
    widths=[1.3, 4.2, 6.9],
    rows=[
        ["ID", "Decision", "Answer used until decided"],
        ["D-RCV-60", "Adopt Architecture v5 and realign the documents and stories",
         "19 services inside ACE, one schema and login per service; applied in this version"],
        ["DL44", "Adopt Architecture v5", "Architecture v5 is the top source on the R3 precedence list"],
        ["DL45", "Service epics plus business-epic tags",
         "one epic per service (19), plus 7 platform and 5 integration epics"],
        ["DL46", "Soft ownership by team type",
         "the owner is a suggestion only; any team may pick up this story"],
        ["DL47", "Epic 1 preservation rule",
         "a built or in-build Epic 1 story keeps its base ID; the change is a delta story"],
        ["DL48", "Dates unchanged and tentative", "every release date is unchanged and marked (tentative)"],
        ["DL49", "Gap and assumption registers", "gaps and assumptions are recorded per document in folder 23"],
    ],
    note=("DL02 of slide 6 is unchanged and still open. D-RCV-60 and DL44 to DL49 are the new "
          "decisions of this realignment."),
    header_pt=10.0, body_pt=11.0))

spec.append(dict(
    n=19, title="Change log", kind="table",
    widths=[1.2, 2.3, 5.6, 3.3],
    rows=[
        ["Version", "Date", "Change", "Tool"],
        ["3", "22 November 2026",
         "D-RCV-60 microservice realignment: one run book page per service (slides 8 to 17), every "
         "owner from the Ownership Map v1, decisions DL44 to DL49; every version 2 slide kept",
         "T3 Code / OpenCode / DeepSeek v4.1 Flash"],
        ["2", "28 October 2026", "the source deck; it records no change log and no tool line",
         "Not stated in the source documents (CG-B-DELIVDOC-47-5; ASM-B-DELIVDOC-47-5)"],
    ],
    note=('Change-log row: "3, 22 November 2026, D-RCV-60 microservice realignment, '
          'T3 Code / OpenCode / DeepSeek v4.1 Flash". Status: Draft.'),
    header_pt=10.0, body_pt=11.0))

for s in spec:
    slide = prs.slides.add_slide(LAYOUT)
    clone_design(slide, s["n"], s["title"])
    if s["kind"] == "table":
        add_table(slide, s["rows"], s["widths"],
                  header_pt=s.get("header_pt", 9.0), body_pt=s.get("body_pt", 8.5))
    else:
        add_bullets(slide, s["items"])
    if s.get("note"):
        add_note(slide, s["note"])

prs.save(DST)
print("WROTE", DST, "slides:", len(prs.slides))
