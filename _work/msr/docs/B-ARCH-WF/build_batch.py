"""Build Batch and Scheduling Design v5 from the copy of v4. Never touches the source."""
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
P = ROOT / "05 Technical architecture" / "Recovery Workbench Batch and Scheduling Design v5.xlsx"

NAVY = PatternFill("solid", fgColor="1F3864")
HEAD = dict(font=Font(bold=True, color="FFFFFF"), fill=NAVY,
            alignment=Alignment(wrap_text=True, vertical="top"))

PL_SCHED = "Not specified in the source documents (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8)"
PL_P8 = "Not specified in the source documents (CG-B-ARCH-WF-3; ASM-B-ARCH-WF-6)"
PL_WF = "Not specified in the source documents (CG-B-ARCH-WF-4; ASM-B-ARCH-WF-7)"

# (Owner service, Mechanism, Workflow or Schedule, Task queue, Note, Source)
JOBS = {
    "JOB-01": ("P1 rwb-source-data", "none (retired)", "-", "-",
               "Retired under D-RCV-35. ACE ingests the COLLINS feed; the Workbench reads the result through the rwb-source-data ACE view contract (v_ace_account, v_ace_payment). No new story.",
               "Ownership Map v1, sheet Jobs, JOB-01; Architecture v5 slide 41"),
    "JOB-02": ("P3 rwb-case", "event-started workflow", "DailyCaseRun (started by AceDataReady)", "rwb-case",
               "Case creation for accounts at 90 days past due. Architecture v5 slide 14 also names a Schedule beside AceDataReady; the Schedule is a documented fallback and is not configured (CG-B-ARCH-WF-5; ASM-B-ARCH-WF-11).",
               "Architecture v5 slides 14, 31 and 44; Temporal and Drools design slide 14"),
    "JOB-03": ("P3 rwb-case", "event-started workflow step", "DailyCaseRun step (activity allocate)", "rwb-case",
               "Allocation completes by 07:00 in the same DailyCaseRun; there is no separate Schedule for JOB-03.",
               "Architecture v5 slides 14 and 44; Batch v4 JOB-03"),
    "JOB-04": ("P1 rwb-source-data", "event-started workflow", "AceIngestCheck then reconciliation", "rwb-source-data",
               "Freshness check then reconciliation of accounts at 90 days past due against open cases. The activities of both workflows are not named in any source (CG-B-ARCH-WF-4; ASM-B-ARCH-WF-7).",
               "Architecture v5 slides 15 and 44; Ownership Map v1, sheet Jobs, JOB-04"),
    "JOB-05": ("PLT platform", "none (retired)", "-", "-",
               "The 5-minute timer check is retired: durable timers live inside each workflow. D-RCV-36 T2 keeps the TimerScheduler port for Epic 1 and Epic 2 only (CG-A6-flows-5; ASM-A6-flows-6).",
               "Architecture v5 slide 44; Temporal and Drools design slides 8 and 13"),
    "JOB-06": ("P3 rwb-case", "Temporal Schedule", "Schedule rebalancing", "rwb-case",
               "Moves cases from owners above the cap or absent. The workflow or activity the Schedule starts is not named (CG-B-ARCH-WF-4; ASM-B-ARCH-WF-7); the Schedule ID is not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8).",
               "Architecture v5 slides 14 and 44; Batch v4 JOB-06"),
    "JOB-07": ("P8 rwb-payment", "event-started workflow",
               "Event-started payment run, workflow name " + PL_P8 + "; activity matchPayments", "rwb-payment",
               "Started by AceDataReady. The hosting workflow has no name in any source (CG-B-ARCH-WF-3; ASM-B-ARCH-WF-6).",
               "Architecture v5 slides 17 and 44; Temporal and Drools design slide 14"),
    "JOB-08": ("P8 rwb-payment", "event-started workflow",
               "Event-started payment run, workflow name " + PL_P8 + "; activity confirmBookings", "rwb-payment",
               "Started by AceDataReady. Matches approved treatments to bookings in the ACE account view through the rwb-source-data contract (CG-B-ARCH-WF-3; ASM-B-ARCH-WF-6).",
               "Architecture v5 slides 17 and 44; Batch v4 JOB-08"),
    "JOB-09": ("P1 rwb-source-data", "none (retired)", "-", "-",
               "Retired under D-RCV-35. ACE ingests the CCMS, SVAF, RPS, WIN, AMIS and GL files; the Workbench reads them through the v_ace_* views owned by rwb-source-data. No new story.",
               "Ownership Map v1, sheet Jobs, JOB-09; Architecture v5 slide 41"),
    "JOB-10": ("P6 rwb-comms", "Temporal Schedule", "Schedule WIN notices, then deliverFile in rwb-integration", "rwb-comms",
               "rwb-comms owns the notice, the 16:00 window and the Schedule; rwb-integration performs deliverFile and the bank's Airflow opens the WIN file window. Schedule ID not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8) (CG-A6-flows-6; ASM-A6-flows-8).",
               "Architecture v5 slides 17, 31, 32 and 44; Batch v4 JOB-10"),
    "JOB-11": ("PLT platform", "none (no Schedule)", "-", "-",
               "Outbox relay to Kafka in every service, part of the service template and the shared libraries; each service runs its own relay, so there is no Schedule (ASM-A6-flows-9).",
               "Architecture v5 slides 20 and 44"),
    "JOB-12": ("P5 rwb-document", "event-started workflow", "DocumentIntakeWorkflow (KEDA workers)", "rwb-document",
               "Every 15 minutes in business hours becomes an event plus KEDA workers on the queue, not a Schedule; OCR, classify and extract are steps of the workflow.",
               "Architecture v5 slides 16 and 44; Temporal and Drools design slide 12"),
    "JOB-13": ("P7 rwb-decision", "none (no Schedule)", "-", "-",
               "Continuous DecisionRecorded ingest from Kafka in rwb-decision; the nightly copy to the data lake is removed with the data lake, so JOB-13 has no nightly run (CG-A6-flows-7; ASM-A6-flows-10).",
               "Architecture v5 slide 44; plan DP-17"),
    "JOB-14": ("P7 rwb-decision", "Temporal Schedule", "Schedule chain check", "rwb-decision",
               "Checks the hash chain of the central ledger at 02:00. The activity is not named (CG-B-ARCH-WF-4; ASM-B-ARCH-WF-7); the Schedule ID is not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8).",
               "Architecture v5 slides 14 and 44; Temporal and Drools design slide 16"),
    "JOB-15": ("P9 rwb-reporting", "Airflow trigger", "buildRegulatoryExtract activity through POST /reports/{id}/run", "rwb-reporting",
               "The bank's Airflow triggers the extract at 01:30 and re-runs any business date; rwb-reporting builds it from its own projections with no data lake. Architecture v5 slides 15 and 31 also describe a 01:30 Schedule (CG-A6-flows-8; ASM-A6-flows-11).",
               "Architecture v5 slides 15, 31, 32 and 44; plan DP-17"),
    "JOB-16": ("S7 rwb-writeoff", "Temporal Schedule", "Schedule write-off scan, then WriteOffWorkflow", "rwb-writeoff",
               "Runs on the third working day after AceDataReady; a cron expression cannot express the working-day gate, so the workflow checks AceDataReady before it scans (CG-A6-flows-9; ASM-A6-flows-12) (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8).",
               "Architecture v5 slides 20 and 44; Temporal and Drools design slide 23"),
    "JOB-17": ("P5 rwb-document", "Temporal Schedule", "Schedule retention", "rwb-document",
               "Lists records past retention for review on the first Sunday of the month. The workflow or activity is not named (CG-B-ARCH-WF-4; ASM-B-ARCH-WF-7); the Schedule ID is not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8).",
               "Architecture v5 slides 16 and 44"),
    "JOB-18": ("P4 rwb-access", "Temporal Schedule", "Schedule access review list", "rwb-access",
               "Produces role holder lists for recertification every six months. The workflow or activity is not named (CG-B-ARCH-WF-4; ASM-B-ARCH-WF-7); the Schedule ID is not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8).",
               "Architecture v5 slides 14 and 44"),
    "JOB-19": ("S5 rwb-asset", "Temporal Schedule", "Schedule re-appraisal", "rwb-asset",
               "Raises re-appraisal orders for assets due, monthly. The workflow or activity is not named (CG-B-ARCH-WF-4; ASM-B-ARCH-WF-7); the Schedule ID is not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8).",
               "Architecture v5 slides 19 and 44; Temporal and Drools design slide 21"),
    "JOB-20": ("P7 rwb-decision", "Temporal Schedule", "Schedule rule promote, publishes RulePackageInForce", "rwb-decision",
               "Moves APPROVED rule package versions with today's valid-from date to IN_FORCE and the previous version to SUPERSEDED at 00:01. The activity is not named (CG-B-ARCH-WF-4); the Schedule ID is not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8).",
               "Architecture v5 slides 14 and 44; Temporal and Drools design slide 15"),
    "JOB-21": ("PLT platform", "Temporal Schedule", "Schedule stuck workflow scan", "rwb-platform",
               "Visibility query over namespace rwb-recovery every 5 minutes, then an alert; no zero is published. Task queue rwb-platform has no service row (CG-B-ARCH-WF-6; ASM-B-ARCH-WF-12); the Schedule ID is not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8).",
               "Architecture v5 slide 44; Batch v4 JOB-21; Temporal and Drools design slide 28"),
    "JOB-22": ("PLT platform", "Temporal Schedule", "Schedule smoke workflow, then PlatformSmokeWorkflow", "rwb-platform",
               "Starts PlatformSmokeWorkflow as platform-smoke-{yyyymmdd} at 06:00. Task queue rwb-platform has no service row (CG-B-ARCH-WF-6; ASM-B-ARCH-WF-12); the Schedule ID is not specified (CG-B-ARCH-WF-1; ASM-B-ARCH-WF-8).",
               "Architecture v5 slide 44; Batch v4 JOB-22; Temporal and Drools design slide 31"),
}

# Schedule and event map: Job, Owner, Mechanism, Schedule or workflow, Schedule ID, Queue, Trigger, Overlap, Source
MAP = [
    ("JOB-01", "P1 rwb-source-data", "none (retired)", "-", "-", "-", "Retired - D-RCV-35", "-", "Ownership Map v1, sheet Jobs"),
    ("JOB-02", "P3 rwb-case", "event-started workflow", "DailyCaseRun", "-", "rwb-case", "AceDataReady (Airflow signals the business date, ~04:30)", "-", "Architecture v5 slides 31 and 44"),
    ("JOB-03", "P3 rwb-case", "event-started workflow step", "DailyCaseRun step: allocate", "-", "rwb-case", "After JOB-02, by 07:00", "-", "Architecture v5 slide 44"),
    ("JOB-04", "P1 rwb-source-data", "event-started workflow", "AceIngestCheck then reconciliation", "-", "rwb-source-data", "AceDataReady", "-", "Architecture v5 slides 15 and 44"),
    ("JOB-05", "PLT platform", "none (retired)", "-", "-", "-", "Retired: durable timers inside each workflow", "-", "Architecture v5 slide 44"),
    ("JOB-06", "P3 rwb-case", "Temporal Schedule", "Schedule rebalancing", PL_SCHED, "rwb-case", "Daily 06:30", "SKIP, catch-up window", "Architecture v5 slides 14 and 44"),
    ("JOB-07", "P8 rwb-payment", "event-started workflow", "Payment run, activity matchPayments", "-", "rwb-payment", "AceDataReady, after JOB-02", "-", "Architecture v5 slide 44; Temporal design slide 14"),
    ("JOB-08", "P8 rwb-payment", "event-started workflow", "Payment run, activity confirmBookings", "-", "rwb-payment", "AceDataReady, after JOB-02", "-", "Architecture v5 slide 44"),
    ("JOB-09", "P1 rwb-source-data", "none (retired)", "-", "-", "-", "Retired - D-RCV-35", "-", "Ownership Map v1, sheet Jobs"),
    ("JOB-10", "P6 rwb-comms", "Temporal Schedule", "Schedule WIN notices, then deliverFile", PL_SCHED, "rwb-comms", "Daily 16:00; Airflow opens the file window", "SKIP, catch-up window", "Architecture v5 slides 31 and 44"),
    ("JOB-11", "PLT platform", "none (no Schedule)", "Outbox relay in every service", "-", "each rwb-<short>", "Every minute, inside each service", "-", "Architecture v5 slides 20 and 44"),
    ("JOB-12", "P5 rwb-document", "event-started workflow", "DocumentIntakeWorkflow", "-", "rwb-document", "Scanner folder, SFTP or mailbox event; every 15 minutes in business hours", "KEDA scales workers on backlog", "Architecture v5 slides 16 and 44"),
    ("JOB-13", "P7 rwb-decision", "none (no Schedule)", "Continuous DecisionRecorded ingest", "-", "rwb-decision", "Continuous, from Kafka", "-", "Architecture v5 slide 44; plan DP-17"),
    ("JOB-14", "P7 rwb-decision", "Temporal Schedule", "Schedule chain check", PL_SCHED, "rwb-decision", "Daily 02:00", "SKIP, catch-up window", "Architecture v5 slides 14 and 44"),
    ("JOB-15", "P9 rwb-reporting", "Airflow trigger", "buildRegulatoryExtract, POST /reports/{id}/run", "-", "rwb-reporting", "Daily 01:30, re-runnable by business date", "-", "Architecture v5 slides 32 and 44"),
    ("JOB-16", "S7 rwb-writeoff", "Temporal Schedule", "Schedule write-off scan, then WriteOffWorkflow", PL_SCHED, "rwb-writeoff", "Monthly, 3rd working day, gated on AceDataReady", "SKIP, catch-up window", "Architecture v5 slides 20 and 44"),
    ("JOB-17", "P5 rwb-document", "Temporal Schedule", "Schedule retention", PL_SCHED, "rwb-document", "Monthly, 1st Sunday", "SKIP, catch-up window", "Architecture v5 slides 16 and 44"),
    ("JOB-18", "P4 rwb-access", "Temporal Schedule", "Schedule access review list", PL_SCHED, "rwb-access", "Every six months", "SKIP, catch-up window", "Architecture v5 slides 14 and 44"),
    ("JOB-19", "S5 rwb-asset", "Temporal Schedule", "Schedule re-appraisal", PL_SCHED, "rwb-asset", "Monthly", "SKIP, catch-up window", "Architecture v5 slides 19 and 44"),
    ("JOB-20", "P7 rwb-decision", "Temporal Schedule", "Schedule rule promote, publishes RulePackageInForce", PL_SCHED, "rwb-decision", "Daily 00:01", "SKIP, catch-up window", "Architecture v5 slides 14 and 44"),
    ("JOB-21", "PLT platform", "Temporal Schedule", "Schedule stuck workflow scan", PL_SCHED, "rwb-platform", "Every 5 minutes", "SKIP, catch-up window", "Architecture v5 slides 44; Batch v4 JOB-21"),
    ("JOB-22", "PLT platform", "Temporal Schedule", "Schedule smoke workflow, then PlatformSmokeWorkflow", PL_SCHED, "rwb-platform", "Daily 06:00", "SKIP, catch-up window", "Architecture v5 slide 44; Batch v4 JOB-22"),
]

TIMELINE = [
    [None],
    ["v5 realignment (D-RCV-60). The same working day, with the mechanism of each job. Times are Asia/Bangkok and every clock time is the v4 time carried unchanged."],
    ["Time (v5)", "Jobs (v5)", "Mechanism (v5)"],
    ["On AceDataReady (Airflow signals the business date, ~04:30; AceDataLate alarm 05:30)",
     "JOB-02 case creation, then JOB-04 reconciliation, JOB-07 payment matching and JOB-08 booking confirmation",
     "Event-started workflows on rwb-case, rwb-source-data and rwb-payment"],
    ["00:01", "JOB-20 rule package effective date", "Temporal Schedule in rwb-decision"],
    ["Every 5 minutes", "JOB-21 stuck workflow scan", "Temporal Schedule in rwb-platform"],
    ["06:00", "JOB-22 platform smoke trigger, platform-smoke-{yyyymmdd} on rwb-platform", "Temporal Schedule in rwb-platform"],
    ["06:30", "JOB-06 rebalancing", "Temporal Schedule in rwb-case"],
    ["by 07:00", "JOB-03 morning allocation complete", "DailyCaseRun step in rwb-case"],
    ["16:00", "JOB-10 WIN notices", "Temporal Schedule in rwb-comms; Airflow opens the file window; deliverFile in rwb-integration"],
    ["01:30", "JOB-15 reporting extract", "Airflow trigger on rwb-reporting, activity buildRegulatoryExtract"],
    ["02:00", "JOB-14 hash-chain check", "Temporal Schedule in rwb-decision"],
    ["continuous", "JOB-13 decision-log ingest", "Kafka ingest in rwb-decision; no nightly copy"],
    ["every minute", "JOB-11 outbox sender", "Outbox relay inside every service"],
    ["every 15 minutes in business hours", "JOB-12 document intake", "Event plus KEDA workers in rwb-document"],
    ["monthly, 3rd working day", "JOB-16 write-off scan", "Temporal Schedule in rwb-writeoff, gated on AceDataReady"],
    ["monthly, 1st Sunday", "JOB-17 retention job", "Temporal Schedule in rwb-document"],
    ["every six months", "JOB-18 access review list", "Temporal Schedule in rwb-access"],
    ["monthly", "JOB-19 re-appraisal cycle", "Temporal Schedule in rwb-asset"],
    ["The v4 row '01:00 to 02:00 | JOB-13, JOB-15, JOB-14' is kept above for comparison. In v5 JOB-13 is continuous, JOB-15 runs at 01:30 from Airflow and JOB-14 at 02:00 (CG-A6-flows-7, CG-A6-flows-8; ASM-B-ARCH-WF-9)."],
]

READ_ME = [
    "SCB Collections and Recovery. Henka Group, 22 November 2026.",
    "(C) Siam Commercial Bank and Henka Pte Ltd",
    "",
    "Recovery Workbench Batch and Scheduling Design v5 (D-RCV-60). Next version of Recovery Workbench Batch and Scheduling Design v4.",
    "Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.",
    "",
    "Change log",
    "v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash",
    "v4, 16 November 2026, D-RCV-36. Carried unchanged from the source.",
    "",
    "What v5 changes",
    "1. Quartz is retired. No job runs on Quartz or Spring Batch and the ACE qrtz_* and batch_* tables are no longer used (ADR-016; Template and Rules section R5.5 DP-10). Each of the 20 live jobs is a Temporal Schedule or an event-started workflow in the service that owns it.",
    "2. Every job has one owner service from the Recovery Workbench Microservice Ownership Map v1, in column I of the Jobs sheet, with the source in column N. The v4 owner role is kept in column G so the business role is not lost.",
    "3. The Jobs sheet keeps every v4 row, ID, job name, time, dependency, failure rule, owner role and TimerScheduler value unchanged in columns A to H. Only the two description rows (2 and 3) and the two headers G4 and H4 state the v5 wording; every other v4 cell is untouched.",
    "4. A v5 block is added below the v4 Daily timeline, and the new sheet Schedule and event map gives the mechanism, the Schedule ID, the task queue, the trigger and the overlap policy of every job.",
    "5. Nothing is invented. A value the sources do not give carries the placeholder of Template and Rules section R9 and a gap and assumption row.",
    "",
    "Counts",
    "Jobs: 22 rows, as in v4. Retired: JOB-01 and JOB-09 (D-RCV-35). Live: 20. Temporal Schedules: 10 (JOB-06, JOB-10, JOB-14, JOB-16, JOB-17, JOB-18, JOB-19, JOB-20, JOB-21, JOB-22). Event-started work: 6 (JOB-02, JOB-03 as a DailyCaseRun step, JOB-04, JOB-07, JOB-08, JOB-12). Airflow trigger: 1 (JOB-15). No Schedule and no workflow: 3 (JOB-05 durable timers, JOB-11 outbox relay, JOB-13 continuous ingest).",
    "Owners: P1 rwb-source-data JOB-01, JOB-04, JOB-09; P3 rwb-case JOB-02, JOB-03, JOB-06; P4 rwb-access JOB-18; P5 rwb-document JOB-12, JOB-17; P6 rwb-comms JOB-10; P7 rwb-decision JOB-13, JOB-14, JOB-20; P8 rwb-payment JOB-07, JOB-08; P9 rwb-reporting JOB-15; S5 rwb-asset JOB-19; S7 rwb-writeoff JOB-16; PLT platform JOB-05, JOB-11, JOB-21, JOB-22.",
    "",
    "Status",
    "Draft. No approval is recorded for this version (ASM-B-ARCH-WF-1).",
    "Release dates: this document states none. Every date carried from v4 is unchanged and every release date in a related document stays (tentative).",
    "",
    "Sources and precedence",
    "Precedence follows Template and Rules section R3 (R-PREC): Architecture v5 slides 41 to 44, then the Recovery Temporal and Drools Detailed Design v1, then the Architecture v5 narrative slides, then the Decision Log and the ADRs. Batch and Scheduling Design v4 is the document being realigned.",
    "Short forms used in the sheets: Arch v5 = Recovery Workbench Architecture v5 Text Extract v1; Temporal design = Recovery Workbench Temporal and Drools Design Text Extract v1; Batch v4 = Recovery Workbench Batch and Scheduling Design v4; Ownership Map = Recovery Workbench Microservice Ownership Map v1.",
    "Architecture v5 slide 44 (A4 job map) is the job-to-mechanism source. Architecture v5 slide 31 gives the order of the overnight chain. The Temporal design slides 11 to 32 give the task queues, the workflow model and the platform rules. The Ownership Map sheet Jobs gives the owner of every job.",
    "",
    "Gaps cited in this document",
    "CG-B-ARCH-WF-1 Schedule identifiers and calendars; CG-B-ARCH-WF-3 the event-started payment workflow of JOB-07 and JOB-08; CG-B-ARCH-WF-4 the work started by six Schedules and three workflows; CG-B-ARCH-WF-5 DailyCaseRun as Schedule and event; CG-B-ARCH-WF-6 the rwb-platform task queue; CG-A6-flows-5 timer check; CG-A6-flows-6 WIN notices; CG-A6-flows-7 decision-log copy; CG-A6-flows-8 reporting extract; CG-A6-flows-9 write-off scan. Assumptions: ASM-B-ARCH-WF-1 to ASM-B-ARCH-WF-13 and ASM-A6-flows-6, 8, 10, 11 and 12.",
    "",
    "Related documents",
    "Recovery Workbench Temporal Workflow and Activity Catalog v1, in this folder, lists every workflow, activity, Schedule and task queue that this design refers to.",
]


def main():
    wb = openpyxl.load_workbook(P)

    # 1. Read me first
    rm = wb.create_sheet("Read me", 0)
    for line in READ_ME:
        rm.append([line])
    rm.column_dimensions["A"].width = 130
    for r in rm.iter_rows(min_row=1, max_row=len(READ_ME), max_col=1):
        for c in r:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for n in (1, 2, 4, 7, 8, 11, 18, 22, 25, 27, 31, 35, 37):
        if n <= len(READ_ME):
            rm.cell(row=n, column=1).font = Font(bold=True)
    rm.cell(row=1, column=1).font = Font(bold=True, size=13)
    rm.cell(row=1, column=1).alignment = Alignment(wrap_text=False)
    rm.cell(row=2, column=1).alignment = Alignment(wrap_text=False)

    # 2. Jobs sheet
    ws = wb["Jobs"]
    ws["A2"] = ("22 jobs are listed; JOB-01 and JOB-09 are retired under D-RCV-35 and the other 20 run in the service that owns them, "
                "as a Temporal Schedule or an event-started workflow, with no Quartz and no ACE qrtz_* or batch_* tables (v5, D-RCV-60; ADR-016). "
                "Times are Asia/Bangkok. The data jobs start on AceDataReady, the ACE batch-complete record. JOB-20 to JOB-22 were added under D-RCV-36. "
                "The TimerScheduler column keeps the v4 answer for traceability: from v5 the timer check (JOB-05) is retired and durable timers live inside each workflow. "
                "Columns A to H are the v4 text; columns I to N are the v5 realignment.")
    ws["A3"] = "Version 5, 22 November 2026. D-RCV-60. Previous: Version 4, 16 November 2026. D-RCV-36."
    for ref in ("A2", "A3"):
        ws[ref].alignment = Alignment(wrap_text=True, vertical="top")

    ws["G4"] = "Owner (v4 role)"
    ws["H4"] = "TimerScheduler (v4)"
    for col, head in zip("IJKLMN", ["Owner service (v5)", "Mechanism (v5)", "Workflow or Schedule (v5)",
                                   "Task queue (v5)", "Note (v5)", "Source (v5)"]):
        ws[f"{col}4"] = head
        ws[f"{col}4"].font = HEAD["font"]; ws[f"{col}4"].fill = HEAD["fill"]; ws[f"{col}4"].alignment = HEAD["alignment"]

    seen = 0
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row, max_col=1):
        job = row[0].value
        if not job or job not in JOBS:
            continue
        seen += 1
        for col, val in zip("IJKLMN", JOBS[job]):
            c = ws[f"{col}{row[0].row}"]
            c.value = val
            c.alignment = Alignment(wrap_text=True, vertical="top")
    assert seen == 22, seen

    widths = {"A": 9, "B": 30, "C": 55, "D": 32, "E": 26, "F": 34, "G": 18, "H": 18,
              "I": 13, "J": 18, "K": 40, "L": 18, "M": 55, "N": 42}
    for k, v in widths.items():
        ws.column_dimensions[k].width = v
    for r in ws.iter_rows(min_row=1, max_row=4, max_col=14):
        for c in r:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:N{ws.max_row}"

    # 3. Daily timeline: keep v4 rows, append the v5 block
    dt = wb["Daily timeline"]
    for r in TIMELINE:
        dt.append(r)
    start = 13
    dt.column_dimensions["A"].width = 62
    dt.column_dimensions["B"].width = 60
    dt.column_dimensions["C"].width = 60
    for r in dt.iter_rows(min_row=start + 1, max_row=start + 1, max_col=1):
        for c in r:
            c.font = Font(bold=True)
            c.alignment = Alignment(wrap_text=True, vertical="top")
    hdr = start + 2
    for c in dt[hdr]:
        c.font = HEAD["font"]; c.fill = HEAD["fill"]; c.alignment = HEAD["alignment"]
    for row in dt.iter_rows(min_row=start, max_row=dt.max_row, max_col=3):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    # 4. New sheet: Schedule and event map
    if "Schedule and event map" in wb.sheetnames:
        del wb["Schedule and event map"]
    sm = wb.create_sheet("Schedule and event map")
    head = ["Job", "Owner service (v5)", "Mechanism (v5)", "Schedule or workflow (v5)", "Schedule ID (v5)",
            "Task queue (v5)", "Trigger (v5)", "Overlap and catch-up (v5)", "Source (v5)"]
    sm.append(head)
    for c in sm[1]:
        c.font = HEAD["font"]; c.fill = HEAD["fill"]; c.alignment = HEAD["alignment"]
    for r in MAP:
        sm.append(list(r))
    for k, v in zip("ABCDEFGHI", [9, 18, 22, 45, 42, 18, 45, 22, 40]):
        sm.column_dimensions[k].width = v
    for row in sm.iter_rows(min_row=2, max_row=sm.max_row, max_col=9):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    sm.freeze_panes = "A2"
    sm.auto_filter.ref = f"A1:I{sm.max_row}"

    # 5. Document properties: no personal name anywhere
    wb.properties.creator = "SCB Collections and Recovery"
    wb.properties.lastModifiedBy = "SCB Collections and Recovery"
    wb.properties.title = "Recovery Workbench Batch and Scheduling Design v5"
    wb.properties.subject = "D-RCV-60 microservice realignment"
    wb.save(P)
    print("SAVED", P, "sheets:", wb.sheetnames)


if __name__ == "__main__":
    main()
