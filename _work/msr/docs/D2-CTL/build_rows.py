"""Build the Document Control Sheet v13 rows for Document set v15 (D-RCV-60).

Reads the source control sheet row table (src_rows.json, produced by probe.py)
and the tree, and writes rows.json (11 columns, in control-sheet order) plus a
manifest for the edit log. Nothing outside _work/msr/docs/D2-CTL is written.
"""
import json, re
from pathlib import Path

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
SCRATCH = ROOT / "_work/msr/docs/D2-CTL"
DEC = "D-RCV-60"
LABEL = "Document set v15"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

src = json.loads((SCRATCH / "src_rows.json").read_text(encoding="utf-8"))
by_doc = {}
for r in src:
    by_doc[str(r[3]).strip().lower()] = r

SERVICES = [
    ("P1", "rwb-source-data"), ("P2", "rwb-integration"), ("P3", "rwb-case"), ("P4", "rwb-access"),
    ("P5", "rwb-document"), ("P6", "rwb-comms"), ("P7", "rwb-decision"), ("P8", "rwb-payment"),
    ("P9", "rwb-reporting"), ("P10", "rwb-agent"), ("S1", "rwb-valuation"), ("S2", "rwb-treatment"),
    ("S3", "rwb-guarantee"), ("S4", "rwb-litigation"), ("S5", "rwb-asset"), ("S6", "rwb-debtsale"),
    ("S7", "rwb-writeoff"), ("S8", "rwb-deviation"), ("S9", "rwb-partner"),
]

EPICS = [
    ("RWB-PLT-TPL", "Service template and repositories"), ("RWB-PLT-LIB", "Shared libraries"),
    ("RWB-PLT-WF", "Temporal workflow platform"), ("RWB-PLT-DB", "ACE DB schemas and logins"),
    ("RWB-PLT-EVT", "Kafka event platform"), ("RWB-PLT-EDGE", "Edge and gateway"),
    ("RWB-PLT-OBS", "Observability"),
    ("RWB-SVC-P1", "rwb-source-data (Source data)"), ("RWB-SVC-P2", "rwb-integration (Integration)"),
    ("RWB-SVC-P3", "rwb-case (Case and workflow)"), ("RWB-SVC-P4", "rwb-access (Access and authority)"),
    ("RWB-SVC-P5", "rwb-document (Document)"), ("RWB-SVC-P6", "rwb-comms (Communications)"),
    ("RWB-SVC-P7", "rwb-decision (Decision and rules)"), ("RWB-SVC-P8", "rwb-payment (Payment)"),
    ("RWB-SVC-P9", "rwb-reporting (Reporting)"), ("RWB-SVC-P10", "rwb-agent (Agent)"),
    ("RWB-SVC-S1", "rwb-valuation (Valuation and route)"), ("RWB-SVC-S2", "rwb-treatment (Treatment and offer)"),
    ("RWB-SVC-S3", "rwb-guarantee (Guarantee)"), ("RWB-SVC-S4", "rwb-litigation (Litigation)"),
    ("RWB-SVC-S5", "rwb-asset (Asset)"), ("RWB-SVC-S6", "rwb-debtsale (Debt sale)"),
    ("RWB-SVC-S7", "rwb-writeoff (Write-off)"), ("RWB-SVC-S8", "rwb-deviation (Deviation)"),
    ("RWB-SVC-S9", "rwb-partner (Partner)"),
    ("RWB-ITG-W1", "Wave 1 integration"), ("RWB-ITG-W2", "Wave 2 integration"),
    ("RWB-ITG-W3", "Wave 3 integration"), ("RWB-ITG-W4", "Wave 4 integration"),
    ("RWB-ITG-NFR", "Non-functional integration"),
]

NEWROWS = []


def add_family(source_doc, files, note, owner=None, status=None, present=True):
    """Row that continues an existing document family: priority, layer, owner
    roles are copied from the source row, as Template and Rules R8.2 asks."""
    k = source_doc.strip().lower()
    if k not in by_doc:
        raise SystemExit(f"no source row for family: {source_doc}")
    r = by_doc[k]
    comment = f"{LABEL}. {DEC} microservice realignment: {note}."
    if owner:
        comment += f" Owner: {owner} (Ownership Map)."
    if not present:
        comment += " Row is carried in this sheet for the file the realignment issues; when this sheet was written that file was not yet in the tree (CG-D2-CTL-4)."
    review = status or "Not started"
    NEWROWS.append([None, r[1], r[2], r[3], files, r[5], r[6], None, review, None, comment])


def add_new(document, files, priority, layer, reviewed, signed, note, owner=None, present=True):
    comment = f"{LABEL}. {DEC} microservice realignment: {note}."
    if owner:
        comment += f" Owner: {owner} (Ownership Map)."
    if not present:
        comment += " Row is carried in this sheet for the file the realignment issues; when this sheet was written that file was not yet in the tree (CG-D2-CTL-4)."
    NEWROWS.append([None, priority, layer, document, files, reviewed, signed, None, "Not started", None, comment])


def exists(rel):
    return (ROOT / rel).exists()


def count(rel):
    p = ROOT / rel
    return len([x for x in p.rglob("*") if x.is_file()]) if p.is_dir() else (1 if p.exists() else 0)


REQ_REV = "SCB business leads; TechX for build detail"
REQ_SIGN = "SCB business lead"
TECH_REV = "SCB IT architecture, ACE team, TechX"
TECH_SIGN = "SCB IT architecture"
CTRL_REV = "Recovery tech lead, solution architect, SCB IT"
CTRL_SIGN = "SCB sponsor"
BACK_REV = "TechX squads; SCB business leads for acceptance criteria"
BACK_SIGN = "SCB product owner"
DEL_REV = "Program manager, SCB IT"
DEL_SIGN = "SCB sponsor"
QA_REV = "TechX QA, SCB business testers"
QA_SIGN = "SCB QA lead"

# ---- 01 Decisions and governance
add_family("Decision log", "Recovery Workbench Decision Log v11.xlsx",
           "adds decision D-RCV-60 and DL44 to DL49, and marks D-RCV-36 T1 and T2 amended")

# ---- 02 Business architecture and process
add_family("Case and workflow model", "Recovery Workbench Case and Workflow Model v6.xlsx",
           "CaseWorkflow parent with a child workflow per stage (DP-12)", "P3 rwb-case")
add_family("Feature list", "Recovery Workbench Feature List v5.xlsx",
           "adds the Service and Service epic columns")
add_family("Users, roles and permissions", "Recovery Workbench Users Roles and Permissions v5.xlsx",
           "authorise contract of rwb-access (DP-08)", "P4 rwb-access")

# ---- 03 Requirements and specifications
add_family("Business requirements, program",
           "Recovery Workbench Business Requirements Program v5.md, Recovery Workbench Business Requirements Program v5.docx",
           "BR IDs stable, business content unchanged, new section 'Delivery model' and a BR to service epic to business epic trace table")
add_family("Business requirements, Epic 1",
           "Recovery Workbench Business Requirements Epic 1 v5.md, Recovery Workbench Business Requirements Epic 1 v5.docx",
           "BR IDs stable, business content unchanged, new section 'Delivery model' and the trace table")
add_family("Business requirements, Epic 2",
           "Recovery Workbench Business Requirements Epic 2 v3.md, Recovery Workbench Business Requirements Epic 2 v3.docx",
           "BR IDs stable, business content unchanged, new section 'Delivery model' and the trace table")
add_new("Business requirements, Epics 3 to 8",
        "Recovery Workbench Business Requirements Epics 3 to 8 v1.md, Recovery Workbench Business Requirements Epics 3 to 8 v1.docx",
        "2. Business sign-off", "Requirements", REQ_REV, REQ_SIGN,
        "new v1 BRD for Epics 3 to 8, filling the business gaps of the thin stories; every missing value is a gap row and an assumption row")
add_family("Non-functional specification", "Recovery Workbench Non Functional Specification v4.docx",
           "2 s timeout, one-hop REST, and gaps for RPO and RTO")
add_family("Functional specification per module",
           f"Recovery Workbench Functional Specifications by Module v7/ ({count('03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7')} files: 19 module specifications, each at its next version)",
           "adds only a Service line and a v5 note per module; the module set is the 19 services, no module for the platform")

for code, svc in SERVICES:
    name = f"Recovery Workbench PRD {code} {svc} v1.md"
    add_new(f"Product requirements, {code} {svc}", name, "2. Business sign-off", "Requirements",
            REQ_REV, REQ_SIGN,
            f"new v1 PRD for {svc} with CAP-, FR-, NFR- and AC- IDs, FR-{code}-nnn mapped to the FSD requirements, release slicing by wave",
            f"{code} {svc}")
add_new("Product requirements, PLT Platform", "Recovery Workbench PRD PLT Platform v1.md",
        "2. Business sign-off", "Requirements", REQ_REV, REQ_SIGN,
        "new v1 PRD for the platform: service template, shared libraries, workflow kit, event platform, edge, observability",
        "PLT platform")

# ---- 04 User stories
add_family("User stories, Epic 1", "Recovery Workbench User Stories Epic 1 v10.md",
           "story master rebuilt on the service story files, with the Epic 1 stories preserved and the delta stories added (U2)")
add_family("User stories, Epic 2", "Recovery Workbench User Stories Epic 2 v8.md",
           "story master rebuilt on the service story files")
add_family("User stories, Epics 3 to 8", "Recovery Workbench User Stories Epics 3 to 8 v4.md",
           "story master rebuilt on the service story files")
add_family("Technical enabler stories", "Recovery Workbench Technical Enabler Stories v8.md",
           "the platform and integration stories of the realignment")
add_family("Administration stories", "Recovery Workbench Administration Stories v4.md",
           "re-pointed to the owning services")
add_family("ACE team stories", "Recovery Workbench ACE Team Stories v2.md",
           "ACE DB work moved to the per-service DB stories")
add_family("Data migration stories", "Recovery Workbench Data Migration Stories v4.md",
           "migration per schema (DP-15)")
add_family("Story defects, Epic 1, Epic 2 and the enablers",
           "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v5.xlsx",
           "each open defect mapped to the realigned story IDs")
add_family("User story, worked example", "Recovery Workbench User Story Worked Example v7.md",
           "worked example rewritten to the 19-section template (Template and Rules R7)")
add_family("Acceptance criteria glossary", "Recovery Workbench Acceptance Criteria Glossary v2.xlsx",
           "adds the origin tag, the contract-mock Given and the -ITG copies")
add_family("How to read the acceptance criteria", "Recovery Workbench How To Read The Acceptance Criteria v2.docx",
           "explains slices and origin tags in English and Thai")
add_family("Build notes, Epic 1", "Recovery Workbench Build Notes Epic 1 v7.md",
           "per service and lane")
add_family("Build notes, Epic 2", "Recovery Workbench Build Notes Epic 2 v4.md",
           "per service and lane")
add_family("Build notes, technical enablers", "Recovery Workbench Build Notes Technical Enablers v3.md",
           "per platform epic and integration wave")
add_new("Service story catalog", "Recovery Workbench Service Story Catalog v1.xlsx",
        "1. Build start", "Backlog", BACK_REV, BACK_SIGN,
        "new v1 catalog of 31 epics and 1034 stories, per epic, lane, work type and wave")
add_new("Service epics", "Recovery Workbench Service Epics v1.md",
        "1. Build start", "Backlog", BACK_REV, BACK_SIGN,
        "new v1 epic overview: 7 platform, 19 service and 5 integration epics with scope, wave, owner, lanes and Day-1 stories")
base = "04 User stories/Recovery Workbench Service Story Files v1"
for code, name in EPICS:
    rel = f"{base}/{code} {name}"
    add_new(f"Service story files, {code} {name}",
            f"Recovery Workbench Service Story Files v1/{code} {name}/ ({count(rel)} files)",
            "1. Build start", "Backlog", BACK_REV, BACK_SIGN,
            f"{count(rel)} story files for {code}, each to the 19-section template")

# ---- 05 Technical architecture
add_family("ACE architecture decision", "Recovery Workbench ACE Architecture Decision v4.docx",
           "19 services inside ACE, superseding the single-service decision")
add_family("Architecture decision records", "Recovery Workbench Architecture Decision Records v4.md",
           "ADR-013 to ADR-023 added; ADR-002 and ADR-009 superseded, ADR-011 and ADR-012 amended")
add_family("Target architecture, all eight epics", "Recovery Workbench Target Architecture v7.pptx",
           "Arch v5 target: 19 services, Kafka, Temporal layer, edge, no data lake")
add_family("Technical specification per module",
           f"Recovery Workbench Technical Specifications by Module v6/ ({count('05 Technical architecture/Recovery Workbench Technical Specifications by Module v6')} files: 19 module specifications, each at its next version)",
           "adds a T0 Service section per module and rewrites T5.2 as contracts")
add_family("Interface specifications", "Recovery Workbench Interface Specifications v4.xlsx",
           "INT-19 and INT-20 removed (no data lake); per-service owners")
add_family("Environment and deployment design", "Recovery Workbench Environment and Deployment Design v5.docx",
           "per-service deployments; environment names are a gap")
add_family("Workflow engine design", "Recovery Workbench Workflow Engine Design v4.docx",
           "workflow kit, a child workflow per stage, Schedules replace Quartz")
add_family("Rules engine design", "Recovery Workbench Rules Engine Design v4.docx",
           "embedded Drools per service, rule registry in rwb-decision", "P7 rwb-decision")
add_family("Security and access design", "Recovery Workbench Security and Access Design v5.docx",
           "login per service, workload identity, authorise contract", "P4 rwb-access")
add_family("Observability and monitoring design", "Recovery Workbench Observability and Monitoring Design v4.docx",
           "per-service dashboards and alerts")
add_family("Error handling and resilience standard", "Recovery Workbench Error Handling and Resilience Standard v4.docx",
           "2 s timeout, one REST hop, retry and .dlt rules")
add_family("Availability, performance and recovery design", "Recovery Workbench Availability Performance and Recovery Design v3.docx",
           "per-service targets; RPO and RTO are a gap")
add_family("Audit and logging design", "Recovery Workbench Audit and Logging Design v3.docx",
           "local decision record plus the central ledger (DP-03)")
add_family("Document management design", "Recovery Workbench Document Management Design v3.docx",
           "owned by rwb-document", "P5 rwb-document")
add_family("Notification and correspondence design", "Recovery Workbench Notification and Correspondence Design v3.docx",
           "owned by rwb-comms", "P6 rwb-comms")
add_family("Information flow", "Recovery Workbench Information Flow v6.pptx",
           "flows between the 19 services")
add_family("System disposition and integration inventory", "Recovery Workbench System Disposition and Integration Inventory v4.xlsx",
           "adds the Service column")
add_new("Service catalog",
        "Recovery Workbench Service Catalog v1.md, Recovery Workbench Service Catalog v1.xlsx",
        "1. Build start", "Technical", TECH_REV, TECH_SIGN,
        "new v1 catalog of the 19 services with schema, REST base, topic, task queue, resources and call types (Arch v5 slides 13-20)")
add_new("Service template specification", "Recovery Workbench Service Template Specification v1.md",
        "1. Build start", "Technical", TECH_REV, TECH_SIGN,
        "new v1 specification of the service template every service starts from")
add_family("API specification",
           f"Recovery Workbench API Specification v5/ ({count('05 Technical architecture/Recovery Workbench API Specification v5')} files: 19 service contracts, gateway-bff, index, 20 AsyncAPI files)",
           "split into one contract per service plus gateway-bff and an index; each operation in exactly one file")
add_family("Event and messaging design", "Recovery Workbench Event and Messaging Design v5.xlsx",
           "19 service topics plus rwb.decision-record.v1, retry and .dlt topics, outbox and inbox, CloudEvents")
add_new("Kafka topic and event catalog", "Recovery Workbench Kafka Topic and Event Catalog v1.xlsx",
        "1. Build start", "Technical", TECH_REV, TECH_SIGN,
        "new v1 catalog of every topic and event with the producing and consuming service (Ownership Map Events sheet)")
add_family("Batch and scheduling design", "Recovery Workbench Batch and Scheduling Design v5.xlsx",
           "Quartz retired; each job becomes a Temporal Schedule or an event-started workflow (DP-10)")
add_new("Temporal workflow and activity catalog", "Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx",
        "1. Build start", "Technical", TECH_REV, TECH_SIGN,
        "new v1 catalog of every workflow, activity and schedule with the owning service (Ownership Map Workflows and Jobs sheets)")
add_new("Service contract catalog",
        "Recovery Workbench Service Contract Catalog v1.md, Recovery Workbench Service Contract Catalog v1.xlsx",
        "1. Build start", "Technical", TECH_REV, TECH_SIGN,
        "new v1 catalog of the contracts between the services with the v5 slide 13 call-type matrix")

# ---- 06 Data
add_family("Conceptual data model", "Recovery Workbench Conceptual Data Model v7.xlsx",
           "adds the owning service per entity")
add_family("Source to target mapping", "Recovery Workbench Source to Target Mapping v5.xlsx",
           "target schema rwb_<name> (DP-01)")
add_family("Reference data and lists of values", "Recovery Workbench Reference Data and Lists of Values v5.xlsx",
           "reference-data starter; shared lists through the rwb-case contract (DP-07)", "P3 rwb-case")
add_family("Data ownership and stewardship", "Recovery Workbench Data Ownership and Stewardship v4.xlsx",
           "owner service per data set")
add_family("Data migration approach", "Recovery Workbench Data Migration Approach v4.docx",
           "migration per schema (DP-15)")
add_family("Party and customer master data design", "Recovery Workbench Party and Customer Master Data Design v4.xlsx",
           "read only through the rwb-source-data contract (DP-05)", "P1 rwb-source-data")
add_family("Reporting and analytics data model", "Recovery Workbench Reporting and Analytics Data Model v4.xlsx",
           "no data lake; reporting read model from events (DP-17)", "P9 rwb-reporting")
add_family("Data classification and personal data inventory", "Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx",
           "no PII in events, workflow inputs or logs")
add_family("Data quality and reconciliation rules", "Recovery Workbench Data Quality and Reconciliation Rules v4.xlsx",
           "per-service reconciliation")
add_family("Volume and scale forecast", "Recovery Workbench Volume and Scale Forecast v4.xlsx",
           "per-service volumes, topics and queues")
add_family("Logical data model and data dictionary", "Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx",
           "owning service and rwb_<name> schema per table")
add_family("Entity relationship diagram", "Recovery Workbench Entity Relationship Diagram v6.md",
           "owning service per entity and the foreign-key cuts of the Ownership Map")
add_family("Physical schema",
           f"Recovery Workbench Physical Schema v7/ ({count('06 Data/Recovery Workbench Physical Schema v7')} files: 19 rwb_<name>.sql files, recovery_views.sql, README.md)",
           "one schema per service; the built monolith migration is kept; foreign-key cuts from the Ownership Map")

# ---- 08 AI and agents
add_family("AI and agent architecture", "Recovery Workbench AI and Agent Architecture v3.pptx",
           "rwb-agent service, AgentRunWorkflow child, 60 s fallback", "P10 rwb-agent")
add_family("Model integration design", "Recovery Workbench Model Integration Design v3.docx",
           "model calls only from rwb-agent activities", "P10 rwb-agent")
add_family("Agent catalog and specifications", "Recovery Workbench Agent Catalog and Specifications v3.xlsx",
           "owning service per agent", "P10 rwb-agent")

# ---- 09 Testing and quality
add_family("Test strategy", "Recovery Workbench Test Strategy v3.docx",
           "contract tests, component tests with mocks, ITG per wave")
add_family("Non-functional test plan", "Recovery Workbench Non Functional Test Plan v3.docx",
           "per-service and journey non-functional tests")
add_family("Test data plan", "Recovery Workbench Test Data Plan v4.docx",
           "synthetic data per schema and contract mocks")
add_family("Definition of ready and definition of done", "Recovery Workbench Definition of Ready and Done v4.docx",
           "Ready means the contract is published; Done means the contract and boundary tests are green")
add_new("Integration test plan", "Recovery Workbench Integration Test Plan v1.docx",
        "1. Build start", "Quality", QA_REV, QA_SIGN,
        "new v1 plan for the RWB-ITG-W1 to W4 and RWB-ITG-NFR epics with the RWB-ITG-W1J01-ITG harness")
add_family("Requirements traceability matrix", "Recovery Workbench Requirements Traceability Matrix v7.xlsx",
           "every requirement to legacy key to new story IDs to PRD FR IDs")
add_family("Test cases", "Recovery Workbench Test Cases v8.xlsx",
           "adds the Story, Service and Level columns and the -ITG copies")
add_family("Regression suite", "Recovery Workbench Regression Suite v7.xlsx",
           "re-pointed to the realigned story IDs")

# ---- 10 Policy, controls and compliance
add_family("Controls catalog", "Recovery Workbench Controls Catalog v4.xlsx",
           "control owner service per control")
add_family("Records retention and archiving", "Recovery Workbench Records Retention and Archiving v3.docx",
           "retention per schema")
add_family("Personal data protection design", "Recovery Workbench Personal Data Protection Design v3.docx",
           "PII boundaries per service and in events")
add_family("Regulatory requirements map", "Recovery Workbench Regulatory Requirements Map v3.xlsx",
           "regulation to service")

# ---- 11 Delivery and operations
add_family("Build sequence, Epic 1 and Epic 2", "Recovery Workbench Build Sequence Epic 1 and Epic 2 v7.xlsx",
           "by service and lane, Day-1 work first")
add_new("Day-1 work allocation", "Recovery Workbench Day-1 Work Allocation v1.xlsx",
        "1. Build start", "Delivery", DEL_REV, DEL_SIGN,
        "new v1 allocation of Day-1 work per team type, from the service story catalog (U3: owner is a suggestion only)")
add_family("Dependency map", "Recovery Workbench Dependency Map v5.xlsx",
           "H, C, I and X dependency classes")
add_family("Engineering practices", "Recovery Workbench Engineering Practices v6.docx",
           "repository per service, contract-first, per-service Flyway")
add_family("Release plan", "Recovery Workbench Release Plan v5.xlsx",
           "waves inside the eight-month horizon; dates unchanged and tentative")
add_family("Resource plan and team structure", "Recovery Workbench Resource Plan and Team Structure v3.xlsx",
           "suggested ownership by team type; no names")
add_family("Risks, assumptions, issues and dependencies", "Recovery Workbench Risks Assumptions Issues and Dependencies v5.xlsx",
           "realignment risks R1 to R9, and a pointer to the Assumptions Register")
add_family("Cutover and go-live plan", "Recovery Workbench Cutover and Go Live Plan v4.docx",
           "cutover per wave")
add_family("Run operating model", "Recovery Workbench Run Operating Model v3.pptx",
           "run book per service")
add_family("Story build order", "Recovery Workbench Story Build Order v4.docx",
           "lanes and Ready to start")

# ---- 12 Project communication
add_family("Document index", "Recovery Workbench Document Index v14.md",
           "new sections 'Microservice realignment' and 'Document gaps', listing every new file",
           present=exists("12 Project communication/Recovery Workbench Document Index v14.md"))
add_family("Document control sheet",
           "Recovery Workbench Document Control Sheet v13.xlsx",
           "this sheet: one row per new file, labelled Document set v15")
add_family("Project hub for the squads", "Recovery Workbench Project Hub v15.html",
           "links to the new files, labelled Document set v15",
           present=exists("12 Project communication/Recovery Workbench Project Hub v15.html"))
add_family("Team start pack", "Recovery Workbench Team Start Pack v3.pptx",
           "Day-1 work allocation per team type; no names",
           present=exists("12 Project communication/Recovery Workbench Team Start Pack v3.pptx"))
add_family("Executive presentation, CTO", "Recovery Workbench Executive Presentation CTO v4.pptx",
           "diagram-led slides: services, waves, Day-1 work, gaps",
           present=exists("12 Project communication/Recovery Workbench Executive Presentation CTO v4.pptx"))
add_family("Project overview", "Recovery Workbench Project Overview v5.pptx",
           "realignment summary")

# ---- 16 Story diagrams
add_new("Service epic diagrams", f"Recovery Workbench Service Epic Diagrams v1/ ({count('16 Story diagrams/Recovery Workbench Service Epic Diagrams v1')} files: one .excalidraw and one .svg per epic, 31 epics)",
        "3. Supporting", "Technical", TECH_REV, TECH_SIGN,
        "new v1 diagram per epic: story boxes by work type, wave bands, lanes and H, REST, Kafka, Temporal and I edges (Template and Rules R8.8)")

# ---- 22 Microservice Realignment (run material)
add_new("Microservice change register", "22 Microservice Realignment/Recovery Workbench Microservice Change Register v1.md",
        "1. Build start", "Control", CTRL_REV, CTRL_SIGN,
        "the change each document family and each legacy key takes")
add_new("Microservice ownership map", "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx",
        "1. Build start", "Control", CTRL_REV, CTRL_SIGN,
        "owning service for every table, endpoint, event, workflow and job")
add_new("Microservice story template and rules", "22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md",
        "1. Build start", "Control", CTRL_REV, CTRL_SIGN,
        "the story template and the split, dependency and Day-1 rules")
add_new("Microservice realignment tracker", "22 Microservice Realignment/Recovery Workbench Microservice Realignment Tracker v1.xlsx",
        "1. Build start", "Delivery", DEL_REV, DEL_SIGN,
        "the work package tracker")
add_new("Issue-tracker impact and follow-up", "22 Microservice Realignment/Recovery Workbench Jira Impact and Follow-up v1.md",
        "3. Supporting", "Control", CTRL_REV, CTRL_SIGN,
        "the tracker impacts that are not applied in this run (U6)")
add_new("Architecture v5 text extract", "22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md",
        "3. Supporting", "Control", CTRL_REV, CTRL_SIGN,
        "the extracted text of the Arch v5 source")
add_new("Temporal and Drools design text extract", "22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md",
        "3. Supporting", "Control", CTRL_REV, CTRL_SIGN,
        "the extracted text of the Temporal and Drools Detailed Design v1")
add_new("Microservice architecture by epic and story",
        "22 Microservice Realignment/Recovery Workbench Microservice Architecture by Epic and Story v1.excalidraw, 22 Microservice Realignment/Recovery Workbench Microservice Architecture by Epic and Story v1.svg",
        "3. Supporting", "Technical", TECH_REV, TECH_SIGN,
        "the diagram by epic and story")
for w in (1, 2, 3, 4):
    add_new(f"Wave {w} architecture",
            f"22 Microservice Realignment/Recovery Workbench Wave {w} Architecture v1.excalidraw, 22 Microservice Realignment/Recovery Workbench Wave {w} Architecture v1.svg",
            "3. Supporting", "Technical", TECH_REV, TECH_SIGN,
            f"the wave {w} service and dependency diagram")

# ---- 23 Document Gaps
add_new("Gap register",
        "23 Document Gaps/Recovery Workbench Gap Register v1.md, 23 Document Gaps/Recovery Workbench Gap Register v1.xlsx",
        "3. Supporting", "Control", CTRL_REV, CTRL_SIGN,
        "new v1 register of every gap, numbered GAP-nnnn in step D1")
add_new("Assumptions register",
        "23 Document Gaps/Recovery Workbench Assumptions Register v1.md, 23 Document Gaps/Recovery Workbench Assumptions Register v1.xlsx",
        "3. Supporting", "Control", CTRL_REV, CTRL_SIGN,
        "new v1 register of every assumption, numbered ASM-nnnn in step D1")

# number and sanity-check the rows
start = 135
for i, r in enumerate(NEWROWS):
    r[0] = start + i

report = {"rows": len(NEWROWS), "first": start, "last": start + len(NEWROWS) - 1}
missing = []
for r in NEWROWS:
    for part in re.split(r",\s+(?=Recovery Workbench|22 Microservice|23 Document)", str(r[4])):
        p = part.split(" (")[0].strip()
        if p.startswith("Recovery Workbench Service Story Files") or p.startswith("Recovery Workbench Service Epic Diagrams"):
            continue
        if (ROOT / p).exists():
            continue
        for folder in ("01 Decisions and governance", "02 Business architecture and process",
                       "03 Requirements and specifications", "03 Requirements and specifications/PRD",
                       "04 User stories", "05 Technical architecture",
                       "06 Data", "08 AI and agents", "09 Testing and quality", "10 Policy, controls and compliance",
                       "11 Delivery and operations", "12 Project communication", "16 Story diagrams",
                       "22 Microservice Realignment", "23 Document Gaps"):
            if (ROOT / folder / p).exists():
                break
        else:
            missing.append(p)
report["missing_files"] = sorted(set(missing))

(SCRATCH / "rows.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in NEWROWS) + "\n", encoding="utf-8")
(SCRATCH / "rows_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print(json.dumps(report, indent=1))
