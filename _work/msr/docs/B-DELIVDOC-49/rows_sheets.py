"""Builds the rows JSON for the three realignment sheets of Resource Plan v3 (scratch, B-DELIVDOC-49)."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
P = "CG-B-DELIVDOC-49-{}".format
A = "ASM-B-DELIVDOC-49-{}".format
PH = lambda n: f"Not specified in the source documents ({P(n)}; {A(n)})"

# ---------------------------------------------------------------- sheet 2
TECHX = "TechX (suggested; any team may pick up this story)"
ACE = "ACE team (suggested; any team may pick up this story)"
INFRA = "SCB IT infrastructure (suggested; any team may pick up this story)"
DEVOPS = "DevOps team (suggested; any team may pick up this story)"
QA_ONLY = "QA team (suggested; any team may pick up this story)"
ITG = "TechX (suggested; any team may pick up this story). Harness and NFR stories: " + QA_ONLY

own = [
    ["Suggested ownership by team type"],
    ["One suggested owner per work type. The phrase is a suggestion only: any team may pick up the story (DL46; Template and "
     "Rules R5.3). Owners are team types and service codes; no person is named (AGENTS.md rule 4)."],
    ["Work type", "Name", "Suggested owner (fixed phrase)", "What the owner holds in the 19-service shape",
     "Day-1 work (Template and Rules R5.7 rule 6)", "Source"],
    ["CON", "Contract", TECHX,
     "The service's REST, event and activity contracts, published with their fakes before any application work starts; the "
     "contract group CG-W<wave>",
     "Yes. A CON story has no build dependency and is always Day 1 (R5.7 rule 1); every service has at least one CON story "
     "(R5.7 rule 7)", "Architecture v5 slide 11; Template and Rules R5.3, R5.4, R5.7"],
    ["APP", "App development", TECHX,
     "The service's domain workflows and activities on task queue rwb-<short>, in its own schema, against the CON stories and "
     "their fakes",
     "No. The app story waits only on same-service CON work; a C dependency never blocks (R5.7 rule 2)",
     "Template and Rules R5.3, R5.4, R5.7"],
    ["DB", "ACE DB", ACE,
     "The schema rwb_<short>, its own login, the V0001 baseline and the Flyway sequence, the grants, and the outbox, inbox and "
     "idempotency tables created in that schema",
     "Yes. RWB-PLT-NF06-DB and the per-service DB stories carry the split of the single recovery schema (R6)",
     "Template and Rules R4, R6, DP-02, DP-09, DP-15; Ownership Map v1 Tables sheet"],
    ["INF", "Infrastructure", INFRA,
     "The AKS namespace, Kafka topics with their ACLs and quotas, the Temporal namespace quotas, certificates and codec keys, "
     "and the network path to ACE",
     "Yes, by R5.7 rule 6 every team type has Day-1 work. The source plan records no full-time equivalent for this team type "
     f"({P(6)}; {A(6)})", "Architecture v5 slides 21 and 23; Template and Rules R5.3, R5.7"],
    ["OPS", "DevOps", DEVOPS,
     "The service pipeline from the template, one Helm chart, the golden pipeline, KEDA scaling of the workers, the outbox relay "
     "and the observability hooks",
     "Yes. RWB-PLT-TPL, RWB-PLT-EVT and RWB-PLT-OBS are the Day-1 work. The source plan records no full-time equivalent for this "
     f"team type ({P(5)}; {A(5)})", "Architecture v5 slides 20 and 23; Template and Rules R5.1, R5.3, R5.7"],
    ["ITG", "Integration", ITG,
     "The cross-service journeys on the integration wave epics, and the NFR stories; the harness copies of a test case end -ITG",
     "Yes. The integration harness story W1J01 and the platform stories N001 to N012 make sure of it (R5.7 rule 6)",
     "Template and Rules R5.3, R5.5 (DP-11), R5.7, R7.2 s16"],
    [],
    ["Artefact ownership: who holds what in the 19-service shape"],
    ["Artefact or decision", "Owner (Ownership Map v1 or default ruling)", "Source"],
    ["Service template and repositories (RWB-PLT-TPL)", "Platform team, with the DevOps team for the pipeline",
     "Architecture v5 slide 20; Template and Rules R5.1"],
    ["Shared libraries (RWB-PLT-LIB)", "Platform team", "Template and Rules R5.1; DP-03, DP-09, DP-14"],
    ["Temporal cluster, namespace rwb-recovery and the workflow kit (L1 to L3)", "platform team: one owner for the four reusable layers",
     "Temporal and Drools Design slide 23"],
    ["Domain workflows and service activity contracts (L4 and L5)", "each service team, on task queue rwb-<short>",
     "Temporal and Drools Design slides 23 and 24; Template and Rules R4"],
    ["Kafka topics, ACLs and quotas (RWB-PLT-EVT)", "SCB IT infrastructure with the platform team", "Architecture v5 slide 21"],
    ["Edge: gateway-bff and the partner gateway (RWB-PLT-EDGE)", "Platform team with SCB IT security and the architecture team",
     "Architecture v5 slide 20; Template and Rules R5.1"],
    ["Observability (RWB-PLT-OBS)", "Platform team with the DevOps team", "Template and Rules R5.1; Architecture v5 slide 49"],
    ["Feature flags", "platform library", "Template and Rules R3 default ruling; Ownership Map v1 Tables sheet"],
    ["Outbox, inbox and idempotency tables (outbox_event, processed_event, idempotency_key)",
     "PLT library; the copy in each schema is created by that service's DB story",
     "Ownership Map v1 Tables sheet and ruling ASM-A6-tables-8; DP-09"],
    ["Rule package registry, rule package versions, rule rows and rule test cases",
     "P7 rwb-decision, with the business authoring the decision tables",
     "Ownership Map v1 Tables sheet and ruling ASM-A6-tables-3; Architecture v5 slide 27"],
    ["Rule evaluation inside a service", "the owning service, through the embedded Drools kit (DP-04)",
     "Template and Rules DP-04; Architecture v5 slide 27"],
    ["Parameters and reference data (E1-042, E1-043)", "P3 rwb-case",
     "Template and Rules R3 default ruling; Ownership Map v1 (parameter_catalog, parameter_value, reference_row)"],
    ["Case list API", "P3 rwb-case", "Template and Rules R3 default ruling; Ownership Map v1 (case_list_row ruling)"],
    ["Interaction ledger", "P1 rwb-source-data",
     "Template and Rules R3 default ruling and DP-18; Ownership Map v1 (interaction, efs_ledger_outcome)"],
    ["ACE data and the 30 read-only recovery.v_ace_* views", "P1 rwb-source-data only",
     "Architecture v5 slide 45 (ADR-010); DP-05"],
    ["DoA limits (delegation_limit)", "P4 rwb-access", "Ownership Map v1 Tables sheet and ruling ASM-A6-tables-4"],
    ["Case, CMMN state, queues, tasks, allocation and timers", "P3 rwb-case", "Ownership Map v1 Tables sheet; Architecture v5 slide 41"],
    ["Approvals and the central decision ledger", "P7 rwb-decision",
     "Ownership Map v1 Tables sheet (approval, decision_log_entry); Architecture v5 slide 27"],
    ["Service schema rwb_<short> and service login", "ACE team, through the service's DB story",
     "Template and Rules R4, R5.3; Architecture v5 slide 45"],
]

# ---------------------------------------------------------------- sheet 3
ONE = "Recovery squad 1"
TWO = "Recovery squad 2"

services = [
    # code, service, name, wave, source module, squad, slices, legacy
    ("P1", "rwb-source-data", "Source data", 1, "Data engine", ONE, 62, 30),
    ("P2", "rwb-integration", "Integration", 1,
     f"No module is named for this service in the Structure sheet ({P(3)}; {A(3)})", PH(3), 27, 10),
    ("P3", "rwb-case", "Case and workflow", 1, "Case and workflow", ONE, 84, 21),
    ("P4", "rwb-access", "Access and authority", 1, "Access", ONE, 111, 35),
    ("P5", "rwb-document", "Document", 1, "Document hub", TWO, 52, 17),
    ("P6", "rwb-comms", "Communications", 1, "Communications", TWO, 48, 16),
    ("P7", "rwb-decision", "Decision and rules", 1,
     "Rules component (squad 1) and decision center and log (squad 2)", f"{TWO} (decision center and log); the rules kit is {ONE}",
     52, 5),
    ("P8", "rwb-payment", "Payment", 2,
     f"No module is named for this service in the Structure sheet ({P(3)}; {A(3)})", PH(3), 21, 11),
    ("P9", "rwb-reporting", "Reporting", 1,
     f"No module is named for this service in the Structure sheet ({P(3)}; {A(3)})", PH(3), 12, 5),
    ("P10", "rwb-agent", "Agent", 1,
     f"No module is named for this service in the Structure sheet ({P(3)}; {A(3)})", PH(3), 40, 18),
    ("S1", "rwb-valuation", "Valuation and route", 3, "Valuation and route", ONE, 24, 12),
    ("S2", "rwb-treatment", "Treatment and offer", 2, "Settlement", TWO, 47, 18),
    ("S3", "rwb-guarantee", "Guarantee", 3,
     f"No module is named for this service in the Structure sheet ({P(3)}; {A(3)})", PH(3), 17, 8),
    ("S4", "rwb-litigation", "Litigation", 3, "Litigation", TWO, 45, 22),
    ("S5", "rwb-asset", "Asset", 2, "Assets and auction", ONE, 51, 25),
    ("S6", "rwb-debtsale", "Debt sale", 3, "Debt sale", TWO, 30, 16),
    ("S7", "rwb-writeoff", "Write-off", 4, "Write-off", TWO, 32, 16),
    ("S8", "rwb-deviation", "Deviation", 2, "Deviations", ONE, 31, 10),
    ("S9", "rwb-partner", "Partner", 4,
     f"No module is named for this service in the Structure sheet ({P(3)}; {A(3)})", PH(3), 36, 16),
]

svc = [
    ["The 19 services, their wave and the squad that carries their source module"],
    ["Service codes, waves, schemas and queues from the Ownership Map v1 Services sheet and Architecture v5 slide 41. Source "
     "module and squad from the version 2 Structure sheet. Short team names are used; the fixed phrase of Template and Rules "
     "R5.3 is on the Ownership by team type sheet and applies to every row. Story volume from the plan: 1,034 slices for 358 "
     "legacy stories, 939 of the slices Day 1."],
    ["Code", "Service", "Name", "Wave", "Source module (Structure sheet)", "Squad", "CON", "APP", "DB", "INF", "OPS", "ITG",
     "Story slices (plan)", "Legacy stories (plan)"],
]
for code, name, title, wave, module, squad, sl, lg in services:
    svc.append([code, name, title, wave, module, squad, "TechX",
                "TechX", "ACE team", "SCB IT infrastructure", "DevOps team",
                "TechX; harness and NFR stories QA team", sl, lg])
svc += [
    ["PLT", "platform epics", "Platform: RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, "
     "RWB-PLT-OBS", 0,
     f"No module is named for the platform epics in the Structure sheet ({P(4)}; {A(4)})", PH(4),
     "TechX", "TechX", "ACE team", "SCB IT infrastructure", "DevOps team", "TechX", 65, 26],
    ["ITG", "integration epics", "Integration: RWB-ITG-W1 to RWB-ITG-W4 and RWB-ITG-NFR", "1 to 4",
     f"No module is named for the integration epics in the Structure sheet ({P(3)}; {A(3)})", PH(3),
     "TechX", "TechX", "ACE team", "SCB IT infrastructure", "DevOps team",
     "TechX; harness and NFR stories QA team", 147, 2],
    ["Total", "", "", "", "", "", "", "", "", "", "", "", 1034, 358],
    [],
    ["How to read this sheet"],
    ["- Wave is the service wave of the Ownership Map v1 Services sheet (Architecture v5). A story whose business-epic wave is "
     "earlier than its service wave keeps the earlier wave (Template and Rules R5.6)."],
    ["- The source module and the squad are the words of the version 2 Structure sheet: squad 1 carries the data engine, case and "
     "workflow, rules component, access, valuation and route, assets and auction and deviations; squad 2 carries the document hub, "
     "communications, decision center and log, settlement, litigation, debt sale and write-off."],
    [f"- rwb-decision (P7) appears in both module lists: the decision center and log is squad 2, the rules component is the "
     f"embedded Drools kit that squad 1 builds for every service ({P(2)}; {A(2)})."],
    [f"- The six services with no module in the Structure sheet carry the R9 placeholder for the squad, and the squad is agreed "
     f"at the first daily review as the Structure sheet says ({P(3)}; {A(3)})."],
    ["- Story slices and legacy stories are counts of the plan, not new estimates. Legacy stories count the stories whose "
     "primary service is the row; story slices count every planned story in the row's scope, including the slices of a legacy "
     "story whose primary service is another. They show the size of the work each service puts on its squad, not the number of "
     "people it needs."],
]

# ---------------------------------------------------------------- sheet 4
teams = [
    ["Team types and the resources this plan records"],
    ["Full-time equivalents from the People by month sheet, where the Total row sums the 20 role rows. Shared teams are not "
     "counted, as the version 2 note on that sheet says. The team types and their phrases are Template and Rules R5.3."],
    ["Team type", "Suggested owner phrase", "Rows that staff it in version 2", "Full-time equivalents at the Total row",
     "What the realignment asks of it", "Source"],
    ["TechX", TECHX,
     "Recovery squad 1 (6) and Recovery squad 2 (6): one tech lead, three back end developers, one front end developer and one "
     "QA engineer in each", 12,
     "CON and APP stories for 19 services in waves 0 to 4: 1,034 slices, 939 of them Day 1",
     "Version 2 Team and People by month; Template and Rules R5.3, R5.7"],
    ["ACE team", ACE, "ACE team release owner (1) and the shared common module developers (not counted)", 1,
     "19 schemas and logins in ACE PostgreSQL, one Flyway baseline per service, the ACE contract and the release decision",
     "Version 2 Team and People by month; Template and Rules R4, R6"],
    ["SCB IT infrastructure", INFRA,
     "No row. The supporting teams of the Structure sheet (SCB IT security, architecture team) are recorded as shared only",
     PH(6), "The AKS namespace, the Kafka topics with ACLs and quotas, the Temporal namespace quotas, keys and certificates",
     "Version 2 Structure; Template and Rules R5.3; Architecture v5 slide 21"],
    ["DevOps team", DEVOPS, f"No row ({P(5)}; {A(5)})", 0,
     "The service pipeline from the template, one Helm chart, KEDA scaling, the outbox relay and worker deployments, "
     "observability", "Template and Rules R5.1; Architecture v5 slides 20 and 23"],
    ["QA team", QA_ONLY,
     "The QA engineer role in both squads: 2 of the 12 TechX full-time equivalents; no separate QA row",
     "2 (inside the 12 TechX, not counted twice)",
     "The integration harness stories W1J01 and the NFR stories; contract, event and journey tests",
     "Version 2 Team and People by month; Template and Rules R5.3; Architecture v5 slide 46"],
    ["Program roles", "No team type in Template and Rules R5.3",
     "Product owner, program manager, business architect, solution architect, three business analysts, business lead, IT lead and "
     "application owner (9 rows)", 9.5,
     "Sets the order of work, takes decisions, signs designs, runs the sponsor reviews; serves all 19 services",
     "Version 2 Team and People by month"],
    ["Data, business and reference data roles", "No team type in Template and Rules R5.3",
     "Two data engineers, four business testers and one reference data administrator (3 rows)", 7,
     "Loads and masked test data, UAT scripts, rule and limit loads",
     "Version 2 Team and People by month"],
    ["Total on the People by month sheet", "", "The 20 role rows of the People by month sheet", 29.5, "",
     "Version 2 People by month Total row"],
    [],
    ["What this plan does not staff"],
    ["Item", "Position in version 3", "Source"],
    ["Wave 0 platform epics", f"No team, no full-time equivalent and no accountable role in version 2 ({P(4)}; {A(4)})",
     "Version 2 Team and Structure; Template and Rules R5.1"],
    ["Six services (P2, P8, P9, P10, S3, S9)", f"No module and no squad in version 2 ({P(3)}; {A(3)})",
     "Version 2 Structure; Ownership Map v1 Services sheet"],
    ["Squad to service split", f"Version 2 names fourteen modules for 2 squads and 19 services; the split is agreed at the first daily "
     f"review ({P(2)}; {A(2)})", "Version 2 Structure"],
    ["Shared Epic 2 items (DL30)", f"Kept with the Collection squad as version 2 says; not identified per service "
     f"({P(10)}; {A(10)})", "Version 2 Team and Structure"],
    ["Quality assurance capacity", f"Two QA engineers inside TechX, no separate QA team line ({P(7)}; {A(7)})",
     "Version 2 Team; Template and Rules R5.3"],
    ["Named team basis for the counts", f"The TechX counts follow the assumed squad shape until the named team is confirmed "
     f"(DL36), which predates the 19-service shape ({P(8)}; {A(8)})", "Version 2 Team note"],
    ["Approval of this plan", f"No approval is recorded, so the plan is issued as Draft ({P(11)}; {A(11)})",
     "AGENTS.md rule 9 (a missing approval is recorded as an assumption and the work continues in Draft)"],
]

for name, rows in (("rows_ownership.json", own), ("rows_services.json", svc), ("rows_teams.json", teams)):
    (OUT / name).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(name, len(rows))
