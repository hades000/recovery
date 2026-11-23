SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench document index

Every asset in the document set at its current version, who reads it and the file that holds it. Functional and technical specifications are one file per module, in the two specification archives. The ACE DB alignment section carries the controlling change for the 15 November 2026 re-base, recorded as D-RCV-35. The Decisions section carries decision D-RCV-36 of 16 November 2026 and the two records that hold it.

Version 14 carries the microservice realignment of 22 November 2026, recorded as D-RCV-60: 19 services inside ACE, one per business module, with 7 platform epics and 5 integration epics, and every document shown at the version it holds after the realignment. Release dates are unchanged and tentative (U7; DL48). The Microservice realignment section lists every file the realignment added or moved to a new version; the Document gaps section lists what the files cannot show.

## Microservice realignment

Read by: Sponsors, programme manager, solution architects, tech leads, data steward, squads.

Decision D-RCV-60 of 22 November 2026 adopts Architecture v5. Recovery stays inside ACE and is split into 19 services, one per business module P1 to P10 and S1 to S9; each service has its own deployment, schema rwb_<name>, login, REST base /api/recovery/<short>/v1, topic rwb.<short>.events.v1 with retry and dead-letter topics, Temporal task queue rwb-<short> and epic RWB-SVC-<code>. Seven platform epics RWB-PLT-* build the template, the libraries, the workflow platform, the database, the event platform, the edge and observability; four wave integration epics RWB-ITG-W1 to W4 and RWB-ITG-NFR test them. Every story also carries its business epic EP01 to EP08 as a tag, and the 19 do not replace the eight.

The realignment holds 1,034 story files in 31 epic folders, one for every legacy key in the split plan: 358 legacy keys, 822 service stories, 65 platform stories and 147 integration stories. 939 stories are ready on Day 1, across the five team types TechX, ACE, SCB IT infrastructure, DevOps and QA (R5.3, R5.7), in 510 parallel lanes. Epic 1 work already built keeps its base ID and its text, and the microservice change sits in separate delta stories (U2; R6).

### The 19 services

Every value in this table is copied character for character from the Services sheet of the Ownership Map, which is also the owner of each row: the code in the first column owns the service, the schema, the REST base, the topic and the queue.

| Code | Service | Name | Wave | Schema | REST base | Topic | Task queue | Epic |
|---|---|---|---|---|---|---|---|---|
| P1 | rwb-source-data | Source data | 1 | rwb_source_data | /api/recovery/source-data/v1 | rwb.source-data.events.v1 | rwb-source-data | RWB-SVC-P1 |
| P2 | rwb-integration | Integration | 1 | rwb_integration | /api/recovery/integration/v1 | rwb.integration.events.v1 | rwb-integration | RWB-SVC-P2 |
| P3 | rwb-case | Case and workflow | 1 | rwb_case | /api/recovery/case/v1 | rwb.case.events.v1 | rwb-case | RWB-SVC-P3 |
| P4 | rwb-access | Access and authority | 1 | rwb_access | /api/recovery/access/v1 | rwb.access.events.v1 | rwb-access | RWB-SVC-P4 |
| P5 | rwb-document | Document | 1 | rwb_document | /api/recovery/document/v1 | rwb.document.events.v1 | rwb-document | RWB-SVC-P5 |
| P6 | rwb-comms | Communications | 1 | rwb_comms | /api/recovery/comms/v1 | rwb.comms.events.v1 | rwb-comms | RWB-SVC-P6 |
| P7 | rwb-decision | Decision and rules | 1 | rwb_decision | /api/recovery/decision/v1 | rwb.decision.events.v1 | rwb-decision | RWB-SVC-P7 |
| P8 | rwb-payment | Payment | 2 | rwb_payment | /api/recovery/payment/v1 | rwb.payment.events.v1 | rwb-payment | RWB-SVC-P8 |
| P9 | rwb-reporting | Reporting | 1 | rwb_reporting | /api/recovery/reporting/v1 | rwb.reporting.events.v1 | rwb-reporting | RWB-SVC-P9 |
| P10 | rwb-agent | Agent | 1 | rwb_agent | /api/recovery/agent/v1 | rwb.agent.events.v1 | rwb-agent | RWB-SVC-P10 |
| S1 | rwb-valuation | Valuation and route | 3 | rwb_valuation | /api/recovery/valuation/v1 | rwb.valuation.events.v1 | rwb-valuation | RWB-SVC-S1 |
| S2 | rwb-treatment | Treatment and offer | 2 | rwb_treatment | /api/recovery/treatment/v1 | rwb.treatment.events.v1 | rwb-treatment | RWB-SVC-S2 |
| S3 | rwb-guarantee | Guarantee | 3 | rwb_guarantee | /api/recovery/guarantee/v1 | rwb.guarantee.events.v1 | rwb-guarantee | RWB-SVC-S3 |
| S4 | rwb-litigation | Litigation | 3 | rwb_litigation | /api/recovery/litigation/v1 | rwb.litigation.events.v1 | rwb-litigation | RWB-SVC-S4 |
| S5 | rwb-asset | Asset | 2 | rwb_asset | /api/recovery/asset/v1 | rwb.asset.events.v1 | rwb-asset | RWB-SVC-S5 |
| S6 | rwb-debtsale | Debt sale | 3 | rwb_debtsale | /api/recovery/debtsale/v1 | rwb.debtsale.events.v1 | rwb-debtsale | RWB-SVC-S6 |
| S7 | rwb-writeoff | Write-off | 4 | rwb_writeoff | /api/recovery/writeoff/v1 | rwb.writeoff.events.v1 | rwb-writeoff | RWB-SVC-S7 |
| S8 | rwb-deviation | Deviation | 2 | rwb_deviation | /api/recovery/deviation/v1 | rwb.deviation.events.v1 | rwb-deviation | RWB-SVC-S8 |
| S9 | rwb-partner | Partner | 4 | rwb_partner | /api/recovery/partner/v1 | rwb.partner.events.v1 | rwb-partner | RWB-SVC-S9 |

### The story sets

One folder per epic, under 04 User stories\Recovery Workbench Service Story Files v1. The suggested owner of every story inside a folder follows its work type (R5.3); the folder itself belongs to the service or platform epic in its name.

| Epic folder | Story files |
|---|---|
| RWB-PLT-TPL Service template and repositories | 19 |
| RWB-PLT-LIB Shared libraries | 18 |
| RWB-PLT-WF Temporal workflow platform | 16 |
| RWB-PLT-DB ACE DB schemas and logins | 2 |
| RWB-PLT-EVT Kafka event platform | 3 |
| RWB-PLT-EDGE Edge and gateway | 5 |
| RWB-PLT-OBS Observability | 2 |
| RWB-SVC-P1 rwb-source-data (Source data) | 62 |
| RWB-SVC-P2 rwb-integration (Integration) | 27 |
| RWB-SVC-P3 rwb-case (Case and workflow) | 84 |
| RWB-SVC-P4 rwb-access (Access and authority) | 111 |
| RWB-SVC-P5 rwb-document (Document) | 52 |
| RWB-SVC-P6 rwb-comms (Communications) | 48 |
| RWB-SVC-P7 rwb-decision (Decision and rules) | 52 |
| RWB-SVC-P8 rwb-payment (Payment) | 21 |
| RWB-SVC-P9 rwb-reporting (Reporting) | 12 |
| RWB-SVC-P10 rwb-agent (Agent) | 40 |
| RWB-SVC-S1 rwb-valuation (Valuation and route) | 24 |
| RWB-SVC-S2 rwb-treatment (Treatment and offer) | 47 |
| RWB-SVC-S3 rwb-guarantee (Guarantee) | 17 |
| RWB-SVC-S4 rwb-litigation (Litigation) | 45 |
| RWB-SVC-S5 rwb-asset (Asset) | 51 |
| RWB-SVC-S6 rwb-debtsale (Debt sale) | 30 |
| RWB-SVC-S7 rwb-writeoff (Write-off) | 32 |
| RWB-SVC-S8 rwb-deviation (Deviation) | 31 |
| RWB-SVC-S9 rwb-partner (Partner) | 36 |
| RWB-ITG-W1 Wave 1 integration | 52 |
| RWB-ITG-W2 Wave 2 integration | 43 |
| RWB-ITG-W3 Wave 3 integration | 9 |
| RWB-ITG-W4 Wave 4 integration | 41 |
| RWB-ITG-NFR Non-functional integration | 2 |
| Total | 1,034 |

### Every new and next version

One row per document whose files were added or moved to a new version in this realignment. The # is the document number used in the sections below, so the two can be read together. A row that names two or three files keeps the older file where only one format was rebuilt; the Document gaps section says which.

| # | Document | Files at this version |
|---|---|---|
| 2 | Decision log | Recovery Workbench Decision Log v11.xlsx |
| 135 | Microservice change register | Recovery Workbench Microservice Change Register v1.md |
| 3 | Engineering practices | Recovery Workbench Engineering Practices v6.docx |
| 40 | Release plan | Recovery Workbench Release Plan v5.xlsx, Recovery Workbench Release Plan v4.pptx |
| 41 | Dependency map | Recovery Workbench Dependency Map v5.xlsx |
| 42 | Resource plan and team structure | Recovery Workbench Resource Plan and Team Structure v3.xlsx |
| 53 | Build sequence, Epic 1 and Epic 2 | Recovery Workbench Build Sequence Epic 1 and Epic 2 v7.xlsx |
| 123 | Story build order | Recovery Workbench Story Build Order v4.docx |
| 67 | Risks, assumptions, issues and dependencies | Recovery Workbench Risks Assumptions Issues and Dependencies v5.xlsx |
| 104 | Cutover and go-live plan | Recovery Workbench Cutover and Go Live Plan v4.docx |
| 105 | Run operating model | Recovery Workbench Run Operating Model v2.docx, Recovery Workbench Run Operating Model v3.pptx |
| 56 | AI and agent architecture | Recovery Workbench AI and Agent Architecture v2.docx, Recovery Workbench AI and Agent Architecture v3.pptx |
| 82 | Agent catalog and specifications | Recovery Workbench Agent Catalog and Specifications v2.md, Recovery Workbench Agent Catalog and Specifications v3.xlsx |
| 86 | Model integration design | Recovery Workbench Model Integration Design v3.docx |
| 8 | Case and workflow model | Recovery Workbench Case and Workflow Model v5.html, Recovery Workbench Case and Workflow Model v6.xlsx |
| 16 | Users, roles and permissions | Recovery Workbench Users Roles and Permissions v5.xlsx |
| 24 | Feature list | Recovery Workbench Feature List v5.xlsx |
| 9 | Conceptual data model | Recovery Workbench Conceptual Data Model v6.pptx, Recovery Workbench Conceptual Data Model v7.xlsx |
| 11 | Logical data model and data dictionary | Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx |
| 12 | Entity relationship diagram | Recovery Workbench Entity Relationship Diagram v6.md |
| 26 | Physical schema | Recovery Workbench Physical Schema v7 folder: 19 files, one per service schema, plus recovery_views.sql and README.md |
| 27 | Volume and scale forecast | Recovery Workbench Volume and Scale Forecast v3.pptx, Recovery Workbench Volume and Scale Forecast v4.xlsx |
| 32 | Data classification and personal data inventory | Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx |
| 38 | Reference data and lists of values | Recovery Workbench Reference Data and Lists of Values v5.xlsx |
| 46 | Source to target mapping | Recovery Workbench Source to Target Mapping v5.xlsx |
| 60 | Data ownership and stewardship | Recovery Workbench Data Ownership and Stewardship v4.xlsx |
| 61 | Data quality and reconciliation rules | Recovery Workbench Data Quality and Reconciliation Rules v4.xlsx |
| 65 | Party and customer master data design | Recovery Workbench Party and Customer Master Data Design v3.docx, Recovery Workbench Party and Customer Master Data Design v4.xlsx |
| 89 | Reporting and analytics data model | Recovery Workbench Reporting and Analytics Data Model v4.xlsx |
| 99 | Data migration approach | Recovery Workbench Data Migration Approach v4.docx |
| 10 | Information flow | Recovery Workbench Information Flow v6.pptx |
| 14 | Target architecture, all eight epics | Recovery Workbench Target Architecture v6.docx, Recovery Workbench Target Architecture v7.pptx |
| 20 | Architecture decision records | Recovery Workbench Architecture Decision Records v4.md |
| 25 | System disposition and integration inventory | Recovery Workbench System Disposition and Integration Inventory v4.xlsx |
| 34 | Environment and deployment design | Recovery Workbench Environment and Deployment Design v5.docx |
| 36 | Interface specifications | Recovery Workbench Interface Specifications v3.md, Recovery Workbench Interface Specifications v4.xlsx |
| 45 | Security and access design | Recovery Workbench Security and Access Design v5.docx |
| 57 | API specification | Recovery Workbench API Specification v5 folder: index.yaml, gateway-bff.yaml, 19 service files rwb-access.yaml to rwb-writeoff.yaml, 20 AsyncAPI files; Recovery Workbench API Specification v4.html |
| 63 | Event and messaging design | Recovery Workbench Event and Messaging Design v4.md, Recovery Workbench Event and Messaging Design v5.xlsx |
| 68 | Rules engine design | Recovery Workbench Rules Engine Design v4.docx |
| 71 | Workflow engine design | Recovery Workbench Workflow Engine Design v4.docx |
| 72 | Audit and logging design | Recovery Workbench Audit and Logging Design v3.docx |
| 74 | Batch and scheduling design | Recovery Workbench Batch and Scheduling Design v4.docx, Recovery Workbench Batch and Scheduling Design v5.xlsx |
| 76 | Document management design | Recovery Workbench Document Management Design v3.docx |
| 77 | Error handling and resilience standard | Recovery Workbench Error Handling and Resilience Standard v4.docx |
| 79 | Notification and correspondence design | Recovery Workbench Notification and Correspondence Design v3.docx |
| 83 | Availability, performance and recovery design | Recovery Workbench Availability Performance and Recovery Design v3.docx |
| 87 | Observability and monitoring design | Recovery Workbench Observability and Monitoring Design v4.docx |
| 92 | Technical specification per module | Recovery Workbench Technical Specifications by Module v6 folder: 19 module files |
| 113 | ACE architecture decision | Recovery Workbench ACE Architecture Decision v4.docx |
| 136 | Service catalog | Recovery Workbench Service Catalog v1.md, Recovery Workbench Service Catalog v1.xlsx |
| 137 | Service template specification | Recovery Workbench Service Template Specification v1.md |
| 138 | Service contract catalog | Recovery Workbench Service Contract Catalog v1.md, Recovery Workbench Service Contract Catalog v1.xlsx |
| 139 | Kafka topic and event catalog | Recovery Workbench Kafka Topic and Event Catalog v1.xlsx |
| 140 | Temporal workflow and activity catalog | Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx |
| 13 | Project overview | Recovery Workbench Project Overview v4.docx, Recovery Workbench Project Overview v5.pptx |
| 54 | Team start pack | Recovery Workbench Team Start Pack v2.html, Recovery Workbench Team Start Pack v3.pptx |
| 108 | Executive presentation, CTO | Recovery Workbench Executive Presentation CTO v4.pptx |
| 110 | Document index | Recovery Workbench Document Index v14.md |
| 114 | Document control sheet | Recovery Workbench Document Control Sheet v13.xlsx |
| 116 | Project hub for the squads | 12 Project communication\Recovery Workbench Project Hub v15.html, 14 Story Updates\Recovery Workbench Project Hub v17.html |
| 17 | User story, worked example | Recovery Workbench User Story Worked Example v7.md |
| 49 | Administration stories | Recovery Workbench Administration Stories v4.md, Recovery Workbench Administration Stories v3.xlsx |
| 51 | Technical enabler stories | Recovery Workbench Technical Enabler Stories v8.md, Recovery Workbench Technical Enabler Stories v7.xlsx |
| 52 | User stories, Epic 1 | Recovery Workbench Service Story Files v1 folder, Recovery Workbench User Stories Epic 1 v10.md, Recovery Workbench User Stories Epic 1 v9.xlsx, Recovery Workbench User Stories Epic 1 Story Files v7.zip |
| 55 | User stories, Epic 2 | Recovery Workbench Service Story Files v1 folder, Recovery Workbench User Stories Epic 2 v8.md, Recovery Workbench User Stories Epic 2 v7.xlsx, Recovery Workbench User Stories Epic 2 Story Files v5.zip |
| 130 | ACE team stories | Recovery Workbench ACE Team Stories v2.md, Recovery Workbench ACE Team Stories v1.xlsx |
| 101 | Data migration stories | Recovery Workbench Data Migration Stories v4.md, Recovery Workbench Data Migration Stories v3.xlsx |
| 109 | User stories, Epics 3 to 8 | Recovery Workbench User Stories Epics 3 to 8 v4.md, Recovery Workbench User Stories Epics 3 to 8 v3.xlsx |
| 117 | How to read the acceptance criteria | Recovery Workbench How To Read The Acceptance Criteria v2.docx |
| 118 | Acceptance criteria glossary | Recovery Workbench Acceptance Criteria Glossary v2.xlsx |
| 119 | Build notes, Epic 1 | Recovery Workbench Build Notes Epic 1 v7.md |
| 120 | Build notes, Epic 2 | Recovery Workbench Build Notes Epic 2 v4.md |
| 122 | Build notes, technical enablers | Recovery Workbench Build Notes Technical Enablers v3.md |
| 121 | Story defects | Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v5.xlsx |
| 144 | Service story files, all epics | Recovery Workbench Service Story Files v1 folder: 1,034 story files and 31 epic overviews |
| 145 | Service epics | Recovery Workbench Service Epics v1.md |
| 146 | Day-1 work allocation | Recovery Workbench Day-1 Work Allocation v1.xlsx |
| 147 | Service story catalog | Recovery Workbench Service Story Catalog v1.xlsx |
| 18 | Definition of ready and definition of done | Recovery Workbench Definition of Ready and Done v4.docx |
| 69 | Test strategy | Recovery Workbench Test Strategy v3.docx |
| 95 | Non-functional test plan | Recovery Workbench Non Functional Test Plan v3.docx |
| 96 | Test cases | Recovery Workbench Test Cases v8.xlsx |
| 97 | Requirements traceability matrix | Recovery Workbench Requirements Traceability Matrix v7.xlsx |
| 98 | Test data plan | Recovery Workbench Test Data Plan v4.docx |
| 102 | Regression suite | Recovery Workbench Regression Suite v7.xlsx |
| 141 | Integration test plan | Recovery Workbench Integration Test Plan v1.docx |
| 28 | Business requirements, program | Recovery Workbench Business Requirements Program v5.docx, Recovery Workbench Business Requirements Program v5.md |
| 29 | Business requirements, Epic 1 | Recovery Workbench Business Requirements Epic 1 v5.docx, Recovery Workbench Business Requirements Epic 1 v5.md |
| 30 | Business requirements, Epic 2 | Recovery Workbench Business Requirements Epic 2 v3.docx, Recovery Workbench Business Requirements Epic 2 v3.md |
| 50 | Non-functional specification | Recovery Workbench Non Functional Specification v4.docx |
| 78 | Functional specification per module | Recovery Workbench Functional Specifications by Module v7 folder: 19 module files |
| 142 | Business requirements, Epics 3 to 8 | Recovery Workbench Business Requirements Epics 3 to 8 v1.docx, Recovery Workbench Business Requirements Epics 3 to 8 v1.md |
| 143 | PRDs, one per service and Platform | 20 files in 03 Requirements and specifications\PRD: PRD P1 rwb-source-data v1.md to PRD S9 rwb-partner v1.md (19 service files) and PRD PLT Platform v1.md |
| 39 | Regulatory requirements map | Recovery Workbench Regulatory Requirements Map v3.xlsx |
| 59 | Controls catalog | Recovery Workbench Controls Catalog v4.xlsx |
| 66 | Personal data protection design | Recovery Workbench Personal Data Protection Design v3.docx |
| 88 | Records retention and archiving | Recovery Workbench Records Retention and Archiving v3.docx |

### Run material in folder 22

The realignment itself, its registers and its diagrams are assets of the document set too. They sit in 22 Microservice Realignment and carry D-RCV-60.

| File | What it is |
|---|---|
| Recovery Workbench Architecture v5 Text Extract v1.md | The text of the Architecture v5 deck, slide by slide. The first source in the precedence order (R3). |
| Recovery Workbench Temporal and Drools Design Text Extract v1.md | The text of the Temporal and Drools detailed design deck. The second source in the precedence order (R3). |
| Recovery Workbench Microservice Ownership Map v1.xlsx | The owner of every table, endpoint, event, workflow, job and ruling, with its basis. The owner table of this run. |
| Recovery Workbench Microservice Story Template and Rules v1.md | The decisions U1 to U10, the source precedence, the service naming, the owner table, the dependency classes, the decoupling patterns, the template and the gap rules. |
| Recovery Workbench Microservice Change Register v1.md | The change record of the realignment: what moved, which stories were disposed how, and the open points. |
| Recovery Workbench Microservice Realignment Tracker v1.xlsx | The working list: documents, stories, decisions and defects with their status. |
| Issue-tracker impact and follow-up v1 | The issue-tracker impact of the realignment, held in one file in this folder and nowhere else (U6). |
| Recovery Workbench Microservice Architecture by Epic and Story v1.excalidraw, Recovery Workbench Microservice Architecture by Epic and Story v1.svg | The large diagram for developers and architects: wave bands, epic frames, lanes and story boxes, by work type (U10). |
| Recovery Workbench Wave 1 Architecture v1.excalidraw, Recovery Workbench Wave 1 Architecture v1.svg | The same diagram cut to wave 1. |
| Recovery Workbench Wave 2 Architecture v1.excalidraw, Recovery Workbench Wave 2 Architecture v1.svg | The same diagram cut to wave 2. |
| Recovery Workbench Wave 3 Architecture v1.excalidraw, Recovery Workbench Wave 3 Architecture v1.svg | The same diagram cut to wave 3. |
| Recovery Workbench Wave 4 Architecture v1.excalidraw, Recovery Workbench Wave 4 Architecture v1.svg | The same diagram cut to wave 4. |
| aisdlc/ | The AI-SDLC context and the BRD and PRD builder inputs used to produce the requirements of R8.5 (U9). |

## Decisions

Read by: Sponsors, product owner, decision owners.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 1 | Admin and access model | Whether access is granted centrally or by the application owner, who the application owner is, and the authority levels. | NIST RBAC | Recovery Workbench Admin and Access Model v5.docx |
| 2 | Decision log | Every open decision with the question, the options, the owner, the date needed and what it blocks. | Henka excel rules | Recovery Workbench Decision Log v11.xlsx |
| 131 | Specification rulings, RWB-E1-001 | The four source conflicts found in RWB-E1-001 and the ruling on each, re-based on Physical Schema v6 and D-RCV-35: the counts and the systems of record move to ACE, the rulings are unchanged. | Henka word rules | Recovery Workbench RWB-E1-001 Specification Rulings v2.md |
| 132 | Pre-build rulings, RWB-E1-001 | The same four conflicts ruled as a best-answer set before anything is built, with the paste-ready seed, view SQL and edit schedule held in the specification rulings. | Henka word rules | Recovery Workbench RWB-E1-001 Pre-Build Rulings v2.md |
| 133 | Temporal and Drools change register | The ten decisions T1 to T10 of D-RCV-36, the target runtime, the story dispositions, the file edit list and the phase 2 scope. | Henka writing rules | Recovery Workbench Temporal and Drools Change Register v1.md |
| 134 | Rule story retirements | The three rule stories retired by D-RCV-36, their new homes, the cancelled increments and their full original text as an appendix. | Henka writing rules | Recovery Workbench Rule Story Retirements v1.md |
| 135 | Microservice change register | The decision record for D-RCV-60: the 19-service structure, the disposition of every legacy story, the document edit plan and the open points. The controlling document for this realignment. | MADR | Recovery Workbench Microservice Change Register v1.md |

## Delivery

Read by: Program manager, sponsors, SCB IT.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 3 | Engineering practices | The agreed practices: branching, merging, code review, tests, feature flags, pipeline gates and who owns the merge. | Henka word rules | Recovery Workbench Engineering Practices v6.docx |
| 19 | Ways of working and governance | The daily and weekly cadence, who attends, what each forum decides, and how a decision is recorded. | Henka word rules | Recovery Workbench Ways of Working and Governance v3.docx, Recovery Workbench Ways of Working and Governance v3.pptx |
| 40 | Release plan | The eight epics across eight months, what each release contains, and the gates between them. | Henka slide rules | Recovery Workbench Release Plan v5.xlsx, Recovery Workbench Release Plan v4.pptx |
| 41 | Dependency map | Every dependency on the ACE team, the collection squad, the architecture team, data engineering and the partners, with the date each is needed. | Henka excel rules | Recovery Workbench Dependency Map v5.xlsx |
| 42 | Resource plan and team structure | Who is on the squads, from which organization, for how long, and what each person is accountable for. | Henka excel rules | Recovery Workbench Resource Plan and Team Structure v3.xlsx |
| 53 | Build sequence, Epic 1 and Epic 2 | Stories in pull order with their dependencies, the review windows and the critical path. | Henka excel rules | Recovery Workbench Build Sequence Epic 1 and Epic 2 v7.xlsx |
| 123 | Story build order | The order the stories are built in, with the window each falls in, what each one waits for and the critical path through them. | Henka word rules | Recovery Workbench Story Build Order v4.docx |
| 67 | Risks, assumptions, issues and dependencies | Each one with an owner, a date and the action being taken. | Henka excel rules | Recovery Workbench Risks Assumptions Issues and Dependencies v5.xlsx |
| 103 | Benefit tracking plan | Each benefit with its baseline, its measure, the source of the number, who publishes it and how often. | Henka excel rules | Recovery Workbench Benefit Tracking Plan v2.xlsx |
| 104 | Cutover and go-live plan | The sequence, the rehearsal, the rollback, and who decides to go. | Henka word rules | Recovery Workbench Cutover and Go Live Plan v4.docx |
| 105 | Run operating model | The teams, shifts, service levels, escalation and support tiers that run the Workbench after go-live. | Henka slide rules | Recovery Workbench Run Operating Model v2.docx, Recovery Workbench Run Operating Model v3.pptx |
| 106 | Training and change plan | Who needs to learn what, when, how they are trained, and how readiness is measured. | Henka word rules | Recovery Workbench Training and Change Plan v2.docx, Recovery Workbench Training and Change Plan v2.pptx |

## AI

Read by: Enterprise AI team, Risk and Model Risk, center of excellence.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 4 | AI assisted development approach | How the squads use AI to build: the standards file, the story file, the review step and the quality gates. | Henka word rules | Recovery Workbench AI Assisted Development Approach v1.md, Recovery Workbench AI Assisted Development Approach v3.pptx |
| 56 | AI and agent architecture | Where decisions are automated, where a model advises a person, and where a person decides alone. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench AI and Agent Architecture v2.docx, Recovery Workbench AI and Agent Architecture v3.pptx |
| 82 | Agent catalog and specifications | Each agent: what it watches, what it does, what it may decide alone, what it escalates, and how it is measured. | Henka excel rules | Recovery Workbench Agent Catalog and Specifications v2.md, Recovery Workbench Agent Catalog and Specifications v3.xlsx |
| 86 | Model integration design | Which models are called, with what inputs, how the output is used, and how a model is changed without a release. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Model Integration Design v3.docx |
| 93 | AI decision governance | How an automated decision is recorded, explained, reviewed, challenged and reversed. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench AI Decision Governance v2.docx |

## Business

Read by: Business lead, product heads, process owners, analysts.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 5 | Process architecture | L1 and L2 definitions and the L3 processes, numbered and named. | APQC process classification | Recovery Workbench Process Architecture v3.xlsx, Recovery Workbench Process Architecture v4.pptx |
| 6 | Business architecture | Capabilities, the processes under each, the decisions taken, the partners and the organization that runs it. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Business Architecture v4.pptx |
| 7 | Business rules and routing logic | Every rule that moves a case: event, condition, action, owner, timer, from state and to state, with the completeness checks. | Decision Model and Notation 1.4 | Recovery Workbench Business Rules and Routing Logic v4.html, Recovery Workbench Business Rules and Routing Logic v4.xlsx |
| 8 | Case and workflow model | The stages, milestones, tasks, event listeners and sentries, with the state machine and the case file items. | CMMN 1.1 | Recovery Workbench Case and Workflow Model v5.html, Recovery Workbench Case and Workflow Model v6.xlsx |
| 15 | Target operating model | The future state organization, the work split, spans and layers, and what changes from today. | Henka slide rules | Recovery Workbench Target Operating Model v3.pptx |
| 16 | Users, roles and permissions | Every role, bank, partner, customer and non-human, with the permission per role, the access request and grant flow, and single sign-on mapping. | NIST RBAC | Recovery Workbench Users Roles and Permissions v5.xlsx |
| 21 | Business glossary | Every business term with one definition, the Thai equivalent, and the object or field it maps to. | Domain driven design | Recovery Workbench Business Glossary v3.xlsx |
| 22 | Detailed process flows | Every step in every journey across the actor and system lanes, with the rules that enter and leave each step. | BPMN 2.0 | Recovery Workbench Detailed Process Flows v4.html, Recovery Workbench Detailed Process Flows v4.xlsx |
| 23 | Deviation and exception catalog | Every deviation type: what raises it, what it suspends, who handles it, and how the case returns. | CMMN 1.1 | Recovery Workbench Deviation and Exception Catalog v3.xlsx |
| 24 | Feature list | Every feature in the product, by module, split user, administration and system. | Henka excel rules | Recovery Workbench Feature List v5.xlsx |
| 31 | Case journeys | One page per route: how a case moves from entry to closure. | Henka slide rules | Recovery Workbench Case Journeys v3.pptx |
| 33 | Delegation of authority matrix | Every approval and its limit by role, amount and product, with the substitute when the holder is absent. | NIST RBAC | Recovery Workbench Delegation of Authority Matrix v2.xlsx |
| 43 | Role to system access matrix | Every role against every system, each intersection marked read, write, read and write, or no access, covering bank, partner, customer and non-human roles. | NIST RBAC | Recovery Workbench Role to System Access Matrix v3.xlsx |
| 48 | User journeys | One page per role, bank, partner, customer and administration: the work the person does, the screens they use, how they get access and what they do when something goes wrong. | Henka slide rules | Recovery Workbench User Journeys v2.pptx |
| 58 | Business measures and targets | Every measure with its definition, formula, source, owner and target by quarter. | Henka excel rules | Recovery Workbench Business Measures and Targets v2.xlsx |
| 64 | Partner operating model | How law firms, collection agencies, auction vendors, valuers, buyers and the asset management companies are placed, instructed, paid and measured. | Henka slide rules | Recovery Workbench Partner Operating Model v2.docx, Recovery Workbench Partner Operating Model v2.pptx |
| 115 | Process map | The recovery process as one picture, from first missed payment to close, with the owner of each step. | Henka slide rules | Recovery Workbench Process Map v1.html |

## Data

Read by: Data steward, data engineering, squads.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 9 | Conceptual data model | The subject areas and the data products, and what each one holds. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Conceptual Data Model v6.pptx, Recovery Workbench Conceptual Data Model v7.xlsx |
| 11 | Logical data model and data dictionary | Every entity with every field: name, type, length, mandatory, default, list of values, key, and the ACE table and column each external field is read from. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx |
| 12 | Entity relationship diagram | The entities and their relationships with cardinality, grouped by data product. | IDEF1X notation | Recovery Workbench Entity Relationship Diagram v6.md |
| 26 | Physical schema | Create statements with indexes, constraints, the four extension tables, the ACE views and seed reference data, for Postgres. | ISO/IEC/IEEE 29148 | Recovery Workbench Physical Schema v7 folder: 19 files, one per service schema, plus recovery_views.sql and README.md |
| 27 | Volume and scale forecast | Cases, accounts, documents, interactions, decisions and events by product and stage, with the monthly and five year projection and the concurrent user load. Each figure carries its assumption, its source and the effect if the assumption moves. | ISO/IEC 25010 | Recovery Workbench Volume and Scale Forecast v3.pptx, Recovery Workbench Volume and Scale Forecast v4.xlsx |
| 32 | Data classification and personal data inventory | Every field classified by sensitivity, with the personal data fields named, the ACE column that holds each one and the handling rule, including the masking in the views. | Thai PDPA | Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx |
| 38 | Reference data and lists of values | Every code list with its values, meanings, owner and change process. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Reference Data and Lists of Values v5.xlsx |
| 46 | Source to target mapping | Every Workbench view field mapped from the ACE column that holds it, with the source system ACE ingests from, the transform in the view and the refresh. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Source to Target Mapping v5.xlsx |
| 60 | Data ownership and stewardship | Who owns each data product, who may change it, and how a change is requested. | Henka excel rules | Recovery Workbench Data Ownership and Stewardship v4.xlsx |
| 61 | Data quality and reconciliation rules | What is reconciled to ACE, the tolerance, and what happens when a check fails. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Data Quality and Reconciliation Rules v4.xlsx |
| 65 | Party and customer master data design | How one customer, guarantor or partner is identified across systems, and how duplicates are resolved. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Party and Customer Master Data Design v3.docx, Recovery Workbench Party and Customer Master Data Design v4.xlsx |
| 89 | Reporting and analytics data model | The measures, dimensions and refresh for management reporting, and where each number comes from. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Reporting and Analytics Data Model v4.xlsx |
| 99 | Data migration approach | Which history is already in ACE, what still moves, what happens to cases in flight, and whether there is a parallel run. | Henka word rules | Recovery Workbench Data Migration Approach v4.docx |

## ACE DB alignment

Read by: Data architect, ACE team, recovery tech lead, data engineering.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 124 | ACE DB alignment change register | The decision record for the re-base on the ACE database: decisions U1 to U5 as D-RCV-35, the document edit plan, the story disposition and the defects found. The controlling document for the pack. | MADR | Recovery Workbench ACE DB Alignment Change Register v1.md |
| 125 | ACE data tier map | The frozen table and column map: which ACE tables are read as they are, which the ACE team adds, which extension tables the Workbench owns, which tables leave, and every re-keyed foreign key. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench ACE Data Tier Map v1.md |
| 126 | ACE field gap list | All 133 external fields with their disposition, the 80 fields the ACE team must add, mapped to table and column, with the reconciliation of the counts. | Henka excel rules | Recovery Workbench ACE Field Gap List v1.xlsx |
| 127 | ACE source views | The 30 read-only v_ace_* view definitions, the helper functions, the grants and the conformance test, in two sections: one over ACE tables that exist today, one over the ACE additions. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench ACE Source Views v1.sql |
| 128 | ACE schema DDL and extract | The 62 ACE tables as runnable PostgreSQL DDL, generated from the ACE workbook, with a 547-row extract, one row per ACE column, for grep and agent use. | ISO/IEC/IEEE 29148 | ACE Schema PostgreSQL v1.sql, ACE Schema Extract v1.csv, ACE-data-schema_20261104.xlsx |
| 129 | ACE DB alignment tracker | The working list for the alignment: 82 documents with size, wave, owner and status, 334 stories with their disposition, the 9 decisions and the 4 defects. | Henka excel rules | Recovery Workbench ACE DB Alignment Tracker v1.xlsx |

## Technical

Read by: TechX squads, ACE team, solution architect.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 10 | Information flow | Where each piece of information comes from, how ACE ingests it, how the Workbench reads it through a view, how often, and what happens when it does not arrive. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Information Flow v6.pptx |
| 14 | Target architecture, all eight epics | The architecture on ACE: modular monolith, one service, one repository, one front end, the case workflow layer, and what each epic adds. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Target Architecture v6.docx, Recovery Workbench Target Architecture v7.pptx |
| 20 | Architecture decision records | One page per decision taken, including ADR-011 (Temporal) and ADR-012 (embedded Drools); ADR-003 and ADR-004 are superseded. | MADR | Recovery Workbench Architecture Decision Records v4.md |
| 25 | System disposition and integration inventory | Every system recovery uses today, whether ACE already ingests it and who owns that ingestion, what happens to each and when, and every interface with its route, direction and frequency. | OpenAPI 3.1, AsyncAPI 3.0 | Recovery Workbench System Disposition and Integration Inventory v4.xlsx |
| 34 | Environment and deployment design | The environments, the namespaces, the pipeline, the feature flag approach, the branching model and the release path. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Environment and Deployment Design v5.docx |
| 36 | Interface specifications | Per interface: approach, trigger, payload fields, frequency, volume, error handling, retry and owner, with the inbound interfaces owned by ACE and the outbound by the Workbench. | OpenAPI 3.1, AsyncAPI 3.0 | Recovery Workbench Interface Specifications v3.md, Recovery Workbench Interface Specifications v4.xlsx |
| 45 | Security and access design | Single sign-on, identity and access management, the permission check, personal data masking and the session rules. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Security and Access Design v5.docx |
| 57 | API specification | Every endpoint: method, path, request, response, error codes and authorization. | OpenAPI 3.1 | Recovery Workbench API Specification v5 folder: index.yaml, gateway-bff.yaml, 19 service files rwb-access.yaml to rwb-writeoff.yaml, 20 AsyncAPI files; Recovery Workbench API Specification v4.html |
| 63 | Event and messaging design | Every event the Workbench publishes and consumes, the payload, the order guarantee and the duplicate handling. | AsyncAPI 3.0 | Recovery Workbench Event and Messaging Design v4.md, Recovery Workbench Event and Messaging Design v5.xlsx |
| 68 | Rules engine design | How rules are authored as Drools XLS packages, versioned, tested, approved, made effective, rolled back and recorded. | Decision Model and Notation 1.4 | Recovery Workbench Rules Engine Design v4.docx |
| 71 | Workflow engine design | How the case model maps to Temporal, how a case moves, how timers run in Epics 1-2 and 3+, determinism and replay. | CMMN 1.1 | Recovery Workbench Workflow Engine Design v4.docx |
| 72 | Audit and logging design | What is logged, in what form, where it is held, who can read it, and how an action is traced end to end. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Audit and Logging Design v3.docx |
| 74 | Batch and scheduling design | Every scheduled job: what it does, when it runs against the ACE batch-complete record, what it depends on, and what happens when it fails or runs late. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Batch and Scheduling Design v4.docx, Recovery Workbench Batch and Scheduling Design v5.xlsx |
| 76 | Document management design | Storage, indexing, extraction, attachment to a case, versions, physical originals and custody. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Document Management Design v3.docx |
| 77 | Error handling and resilience standard | How every failure is caught, retried, reported and recovered, and what the user sees meanwhile. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Error Handling and Resilience Standard v4.docx |
| 79 | Notification and correspondence design | How letters, messages and alerts are generated, approved, sent, tracked and proved. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Notification and Correspondence Design v3.docx |
| 83 | Availability, performance and recovery design | The service levels, the scaling approach, the backup and the recovery time and point objectives. | ISO/IEC 25010 | Recovery Workbench Availability Performance and Recovery Design v3.docx |
| 87 | Observability and monitoring design | What is measured, what raises an alert, who receives it, and the dashboards that show the system is healthy. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Observability and Monitoring Design v4.docx |
| 92 | Technical specification per module | Components, data model, state machine, interfaces, access control and API endpoints, one per module. | Bank TSD template | Recovery Workbench Technical Specifications by Module v6 folder: 19 module files |
| 113 | ACE architecture decision | The decision to build the Workbench inside ACE, with the workflow, structure and data options compared. | ISO/IEC/IEEE 42010 | Recovery Workbench ACE Architecture Decision v4.docx |
| 136 | Service catalog | The 19 services with their resources, REST operations, events, workflows, naming, waves and call types, one row per service. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Service Catalog v1.md, Recovery Workbench Service Catalog v1.xlsx |
| 137 | Service template specification | The one shape every service is built from: schema and login, REST base, topic, task queue, library set, pipeline and definition of done. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Service Template Specification v1.md |
| 138 | Service contract catalog | Every contract between services: REST operations, events, Temporal contracts and jobs, with the contract pairs, the resources owned and the conformance check. | OpenAPI 3.1, AsyncAPI 3.0 | Recovery Workbench Service Contract Catalog v1.md, Recovery Workbench Service Contract Catalog v1.xlsx |
| 139 | Kafka topic and event catalog | Every topic, retry topic and dead-letter topic, every event with its envelope, the outbox and inbox tables, the access rules and the delivery rules. | AsyncAPI 3.0 | Recovery Workbench Kafka Topic and Event Catalog v1.xlsx |
| 140 | Temporal workflow and activity catalog | Every workflow, activity and Schedule, the task queues and namespaces, the platform rules and the open points. | CMMN 1.1 | Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx |

## Communication

Read by: Sponsors, executives, all teams.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 13 | Project overview | What the Workbench is, the problem it solves, what changes, the plan and the benefits, for any audience in ten minutes. | Henka slide rules | Recovery Workbench Project Overview v4.docx, Recovery Workbench Project Overview v5.pptx |
| 37 | Recovery Workbench project deck | The full account: today, the target, the process, the architecture, the data, the eight epics, the organization and the plan. | Henka slide rules | Recovery Workbench Project Deck v3.pptx |
| 47 | Stakeholder map and communication plan | Who needs to know what, how often, through which forum, and who tells them. | Henka excel rules | Recovery Workbench Stakeholder Map and Communication Plan v3.xlsx |
| 54 | Team start pack | What the Workbench is, how the work runs, and what each role does in the first month. | Henka slide rules | Recovery Workbench Team Start Pack v2.html, Recovery Workbench Team Start Pack v3.pptx |
| 70 | Weekly status pack | Progress against the plan, what is blocked, what is decided and what is needed, in one page per workstream. | Henka slide rules | Recovery Workbench Weekly Status Pack v2.pptx |
| 107 | Executive presentation, CEO | The outcome, the plan, the benefits and the decisions needed. | Henka slide rules | Recovery Workbench Executive Presentation CEO v2.pptx |
| 108 | Executive presentation, CTO | The architecture, the data, the integration and the build approach. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Executive Presentation CTO v4.pptx |
| 110 | Document index | Every asset, who reads it, and where it is. | Henka word rules | Recovery Workbench Document Index v14.md |
| 114 | Document control sheet | Every document with its upload priority, reviewer, sign-off owner and status. | Henka excel rules | Recovery Workbench Document Control Sheet v13.xlsx |
| 116 | Project hub for the squads | Every story, build note, code, term and original file in one page that works with no network and no sign-in. Version 17 applies the ACE re-base of 15 November 2026 and D-RCV-36 of 16 November 2026: 331 live stories, Temporal and Drools in the stack, the 30 recovery.v_ace_* views and the retired rule stories recorded. The workbench adds a developer action plan to every story, a simple acceptance-criteria table with its covering test cases, and build-sequence story order. | Henka writing rules | 12 Project communication\Recovery Workbench Project Hub v15.html, 14 Story Updates\Recovery Workbench Project Hub v17.html |

## Backlog

Read by: Squads, analysts, product owner.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 17 | User story, worked example | One story in the agreed format, as the template the three parties lock for the next releases. | Connextra form, INVEST, Gherkin | Recovery Workbench User Story Worked Example v7.md |
| 49 | Administration stories | User and role administration, reference data, rule versions, queue and timer configuration, interface monitoring and the audit log. | Connextra form, INVEST, Gherkin | Recovery Workbench Administration Stories v4.md, Recovery Workbench Administration Stories v3.xlsx |
| 51 | Technical enabler stories | Stories with no business user that the Epic 1 and Epic 2 stories build on, in the same format. | Connextra form, INVEST, Gherkin | Recovery Workbench Technical Enabler Stories v8.md, Recovery Workbench Technical Enabler Stories v7.xlsx |
| 52 | User stories, Epic 1 | Every Epic 1 story for build: requirement IDs, business rationale, preconditions, flow, exception paths, acceptance criteria, rules, data with field IDs, contract, solution plan, messages, screens, tests and traceability. One file, a workbook and one file per story. | Connextra form, INVEST, Gherkin | Recovery Workbench Service Story Files v1 folder, Recovery Workbench User Stories Epic 1 v10.md, Recovery Workbench User Stories Epic 1 v9.xlsx, Recovery Workbench User Stories Epic 1 Story Files v7.zip |
| 55 | User stories, Epic 2 | The same for Epic 2, with the three agent stories that go live in Epic 3. | Connextra form, INVEST, Gherkin | Recovery Workbench Service Story Files v1 folder, Recovery Workbench User Stories Epic 2 v8.md, Recovery Workbench User Stories Epic 2 v7.xlsx, Recovery Workbench User Stories Epic 2 Story Files v5.zip |
| 130 | ACE team stories | RWB-ACE-001, the one story the ACE team builds: the 14 new tables, the 12 new columns and the 80-row field appendix, with acceptance criteria on population, freshness and reversibility. | Connextra form, INVEST, Gherkin | Recovery Workbench ACE Team Stories v2.md, Recovery Workbench ACE Team Stories v1.xlsx |
| 101 | Data migration stories | Reconcile the ACE data behind each data product, validate it, cut over and prove it, one story per data product. | Connextra form, INVEST, Gherkin | Recovery Workbench Data Migration Stories v4.md, Recovery Workbench Data Migration Stories v3.xlsx |
| 109 | User stories, Epics 3 to 8 | Step by step detail for each epic, written one epic ahead of its build month. | Connextra form, INVEST, Gherkin | Recovery Workbench User Stories Epics 3 to 8 v4.md, Recovery Workbench User Stories Epics 3 to 8 v3.xlsx |
| 117 | How to read the acceptance criteria | How a Given, When, Then line is read, what each keyword means, and the twelve patterns the criteria use, written for a reader whose first language is not English. | Gherkin | Recovery Workbench How To Read The Acceptance Criteria v2.docx |
| 118 | Acceptance criteria glossary | Every term and code that appears in the acceptance criteria, with its meaning in English and Thai. | Henka excel rules | Recovery Workbench Acceptance Criteria Glossary v2.xlsx |
| 119 | Build notes, Epic 1 | Every flow step of every Epic 1 story written out in full: who acts, what runs on its own, and what has to be built. | Henka writing rules | Recovery Workbench Build Notes Epic 1 v7.md |
| 120 | Build notes, Epic 2 | Every flow step of every Epic 2 story written out in full, in the same form as the Epic 1 notes. | Henka writing rules | Recovery Workbench Build Notes Epic 2 v4.md |
| 122 | Build notes, technical enablers | Every flow step of the 12 technical enabler stories written out in full. | Henka writing rules | Recovery Workbench Build Notes Technical Enablers v3.md |
| 121 | Story defects | Every contradiction found inside a story by reading each flow step against the rest of that story, with its status and who rules on it. | Henka excel rules | Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v5.xlsx |
| 144 | Service story files, all epics | Every story of the 31 service, platform and integration epics in the 19-section template, one file per story, with an epic overview in each folder. | Connextra form, INVEST, Gherkin | Recovery Workbench Service Story Files v1 folder: 1,034 story files and 31 epic overviews |
| 145 | Service epics | The 31 epics: their service, wave, story count, work-type split and the stories they hold. | Connextra form, INVEST, Gherkin | Recovery Workbench Service Epics v1.md |
| 146 | Day-1 work allocation | The Day-1 work of each team type, story by story, with the contract it builds against. | Henka excel rules | Recovery Workbench Day-1 Work Allocation v1.xlsx |
| 147 | Service story catalog | Every story with its lane, wave, release, suggested owner, dependencies and contract, filtered every way the squads need. | Henka excel rules | Recovery Workbench Service Story Catalog v1.xlsx |

## Quality

Read by: QA engineers, business testers.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 18 | Definition of ready and definition of done | What a story carries before it is built, and what is true before it is accepted. | Henka word rules | Recovery Workbench Definition of Ready and Done v4.docx |
| 69 | Test strategy | The levels, the environments, the entry and exit criteria, the data, and who tests what. | ISO/IEC/IEEE 29119 | Recovery Workbench Test Strategy v3.docx |
| 84 | Defect management process | How a defect is raised, graded, assigned, fixed, retested and closed, and the severity definitions. | Henka word rules | Recovery Workbench Defect Management Process v2.docx |
| 95 | Non-functional test plan | How performance, load, resilience, security and penetration testing are run, and the pass marks. | ISO/IEC/IEEE 29119 | Recovery Workbench Non Functional Test Plan v3.docx |
| 96 | Test cases | Cases from the stories and the routing rules, with expected results and traceability. | ISO/IEC/IEEE 29119 | Recovery Workbench Test Cases v8.xlsx |
| 97 | Requirements traceability matrix | Requirement to feature to story to specification section to test, with priority and acceptance criteria. | Bank RTM template | Recovery Workbench Requirements Traceability Matrix v7.xlsx |
| 98 | Test data plan | The data each test needs, where it comes from, and how personal data is handled. | ISO/IEC/IEEE 29119 | Recovery Workbench Test Data Plan v4.docx |
| 100 | User acceptance test plan and scripts | What the business tests, in what order, with the script for each case and the sign-off. | ISO/IEC/IEEE 29119 | Recovery Workbench User Acceptance Test Plan v2.docx, Recovery Workbench User Acceptance Test Scripts v2.xlsx |
| 102 | Regression suite | The cases that run on every release, and how the suite grows as modules are added. | ISO/IEC/IEEE 29119 | Recovery Workbench Regression Suite v7.xlsx |
| 141 | Integration test plan | How the wave integration suites are run: the harness RWB-ITG-W1J01, the environments, the entry and exit criteria and the pass marks. | ISO/IEC/IEEE 29119 | Recovery Workbench Integration Test Plan v1.docx |

## Requirements

Read by: Squads, analysts, QA engineers.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 28 | Business requirements, program | Scope, outcomes, the process architecture, the requirements and the non-functional requirements across all eight epics. | ISO/IEC/IEEE 29148 | Recovery Workbench Business Requirements Program v5.docx, Recovery Workbench Business Requirements Program v5.md |
| 29 | Business requirements, Epic 1 | The requirements at development detail, with the user benefit and the support needed from users. | ISO/IEC/IEEE 29148 | Recovery Workbench Business Requirements Epic 1 v5.docx, Recovery Workbench Business Requirements Epic 1 v5.md |
| 30 | Business requirements, Epic 2 | The requirements at development detail, with the user benefit and the support needed from users. | ISO/IEC/IEEE 29148 | Recovery Workbench Business Requirements Epic 2 v3.docx, Recovery Workbench Business Requirements Epic 2 v3.md |
| 50 | Non-functional specification | Targets with a measure and a test for each, with volumes, concurrency, growth and external partner access. | ISO/IEC 25010 | Recovery Workbench Non Functional Specification v4.docx |
| 78 | Functional specification per module | What each module does: screens, fields, business rules, validation, messages and the process steps it serves. | Bank FSD template | Recovery Workbench Functional Specifications by Module v7 folder: 19 module files |
| 85 | Epics 3 to 8 at specification level | Each remaining epic at architecture, API and integration detail. | ISO/IEC/IEEE 29148 | Recovery Workbench Epics 3 to 8 Specification v3.docx, Recovery Workbench Epics 3 to 8 Specification v3.xlsx |
| 90 | Reporting and management information requirements | Every report and dashboard: who reads it, what decision it supports, the measures on it and the refresh. | ISO/IEC/IEEE 29148 | Recovery Workbench Reporting and Management Information Requirements v2.docx, Recovery Workbench Reporting and Management Information Requirements v2.xlsx |
| 111 | Lean BRD, Epic 1 | The business scope of Epic 1 for sign-off: problem and outcome, scope, rules, process ownership, constraints, dependencies and success measures. | ISO/IEC/IEEE 29148 | Recovery Workbench Lean BRD Epic 1 v3.docx |
| 112 | Lean BRD, Epic 2 | The business scope of Epic 2 for sign-off: problem and outcome, scope, rules, process ownership, constraints, dependencies and success measures. | ISO/IEC/IEEE 29148 | Recovery Workbench Lean BRD Epic 2 v2.docx |
| 142 | Business requirements, Epics 3 to 8 | The business scope of each of Epics 3 to 8 for sign-off, in the same form as the Epic 1 and Epic 2 BRDs. | ISO/IEC/IEEE 29148 | Recovery Workbench Business Requirements Epics 3 to 8 v1.docx, Recovery Workbench Business Requirements Epics 3 to 8 v1.md |
| 143 | PRDs, one per service and Platform | The product requirements of each service: scope, contract, data, state, rules, acceptance and traceability, one file per service plus Platform. | ISO/IEC/IEEE 29148 | 20 files in 03 Requirements and specifications\PRD: PRD P1 rwb-source-data v1.md to PRD S9 rwb-partner v1.md (19 service files) and PRD PLT Platform v1.md |

## Experience

Read by: Front end developers, analysts, business testers.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 35 | Error and message standard | The wording pattern for every error, warning and confirmation, in Thai and English, with the rules that raise each one. | Henka word rules | Recovery Workbench Error and Message Standard v4.docx |
| 44 | Screen inventory and navigation | Every screen, who reaches it, from where, and what it is for. | Henka excel rules | Recovery Workbench Screen Inventory and Navigation v2.xlsx |
| 62 | Design system and component library | The components, states, spacing, type and color the screens are built from. | Bank web standards | Recovery Workbench Design System and Component Library v1.html |
| 75 | Content and label standard | Every label, heading, button and help text in Thai and English, matched to the business glossary. | Domain driven design | Recovery Workbench Content and Label Standard v2.xlsx |
| 80 | Screen specifications | Each screen with its fields, states, validation and messages, attached to the stories that build it. | Connextra form, INVEST, Gherkin | Recovery Workbench Screen Specifications v1.html, Recovery Workbench Screen Specifications v1.md |
| 81 | Accessibility standard | The level the screens meet, the rules that follow from it, and how each screen is checked. | WCAG 2.2 AA | Recovery Workbench Accessibility Standard v2.docx |
| 91 | Screen prototype | Working screens for the developers and the business to use before the build. | Bank web standards | Recovery Workbench Screen Prototype v1.html |
| 94 | Customer and partner correspondence templates | Every letter, notice and message sent outside the bank, with the fields that fill it and the approval it needs. | Henka word rules | Recovery Workbench Customer and Partner Correspondence Templates v2.docx |

## Policy

Read by: Compliance, Risk, internal audit, Legal.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 39 | Regulatory requirements map | Each regulatory obligation mapped to the process step, the rule and the control that satisfies it. | ISO/IEC/IEEE 29148 | Recovery Workbench Regulatory Requirements Map v3.xlsx |
| 59 | Controls catalog | Every control point on the process: what it checks, who performs it, the evidence it produces and how it is tested. | Henka excel rules | Recovery Workbench Controls Catalog v4.xlsx |
| 66 | Personal data protection design | What personal data is held, the lawful basis, consent, masking, access, retention and the subject rights path. | Thai PDPA | Recovery Workbench Personal Data Protection Design v3.docx |
| 73 | Audit findings response map | Each open audit finding mapped to the change in the Workbench that closes it. | Henka excel rules | Recovery Workbench Audit Findings Response Map v2.xlsx |
| 88 | Records retention and archiving | How long each record and document is held, where it moves, and when it is destroyed. | Thai PDPA, bank policy | Recovery Workbench Records Retention and Archiving v3.docx |

## Document gaps

Read by: Programme manager, document owners, squads.

What the files of this set cannot show, at the version recorded above. Each row is a candidate gap: step D1 numbers them in the Gap Register and the Assumptions Register in folder 23, and the candidate rows of this work package sit in _work/msr/gaps/D2-IDX.jsonl and _work/msr/assumptions/D2-IDX.jsonl. No row blocks a wave start.

| Gap | What the index cannot show | Type | Severity | Owner role | How the index handles it |
|---|---|---|---|---|---|
| CG-D2-IDX-1 | The story master workbooks are not at the new version. The seven story masters were assembled as Markdown only: User Stories Epic 1 v10.md, User Stories Epic 2 v8.md, User Stories Epics 3 to 8 v4.md, Administration Stories v4.md, Technical Enabler Stories v8.md, ACE Team Stories v2.md and Data Migration Stories v4.md. Their workbooks stay at v9, v7, v3, v3, v7, v1 and v3. | Missing | P3 | Product owner | The index lists the Markdown at its new version and the workbook at the version found; the two are not read as one pair. |
| CG-D2-IDX-2 | Some document families advanced in one format only. Batch and Scheduling Design (docx v4, xlsx v5), Event and Messaging Design (md v4, xlsx v5), Interface Specifications (md v3, xlsx v4), Release Plan (pptx v4, xlsx v5), Run Operating Model (docx v2, pptx v3), Agent Catalog (md v2, xlsx v3), Process Architecture (xlsx v3, pptx v4), Case and Workflow Model (html v5, xlsx v6), Conceptual Data Model (pptx v6, xlsx v7) and Volume and Scale Forecast (pptx v3, xlsx v4) each hold two versions in one family. | Ambiguous | P3 | TechX | The index lists both files with their own version, so no reader takes the older one for the current text. |
| CG-D2-IDX-3 | The specifications are folders without an archive. Technical Specifications by Module v6, Functional Specifications by Module v7 and Physical Schema v7 exist as folders of module files; the source set carried the first two as .zip archives (v5.zip and v6.zip) and the physical schema as one .sql file (v6.sql). | Missing | P3 | TechX | The index names the folder and its contents instead of an archive that does not exist. |
| CG-D2-IDX-4 | The API specification has no single-file rendering at v5. API Specification v5 is a folder of index.yaml, gateway-bff.yaml, 19 service files and 20 AsyncAPI files. The last single-file HTML rendering is API Specification v4.html. | Missing | P3 | TechX | The index lists the v5 folder and keeps v4.html named as the previous rendering. |
| CG-D2-IDX-5 | The entity relationship diagram is Markdown only at v6. Entity Relationship Diagram v6.md exists; the HTML and PDF renderings stay at v5. | Missing | P3 | Data steward | The index lists v6.md and does not present the v5 rendering as current. |
| CG-D2-IDX-6 | The realignment tracker is at v1. The run material list in R8.3 names a tracker v2; only Microservice Realignment Tracker v1.xlsx is in folder 22. | Missing | P3 | Programme manager | The index lists v1 as it stands. |
| CG-D2-IDX-7 | The run summary is not in folder 22. The run material list in R8.3 names a Run Summary v1; no such file is in folder 22 at this version. | Missing | P3 | Programme manager | The index lists the run material that exists and records this one as a gap. |
| CG-D2-IDX-8 | Documents outside the realignment keep their previous version. Business Rules and Routing Logic v4, Detailed Process Flows v4, Screen Inventory and Navigation v2, Error and Message Standard v4 and the other Experience documents were not rebuilt under D-RCV-60. The index records the version the files hold. | Outdated | P3 | Business lead | The index shows the version on disk; it does not claim the document matches the 19-service target. |
| CG-D2-IDX-9 | The project hub carries two version-15 files. Project Hub v15.html was issued into 12 Project communication by this run, and 14 Story Updates already holds Project Hub v15.html of 12 November 2026, v16.html and v17.html. The same version number therefore names two different files in two folders. | ID collision | P3 | Programme manager | The index lists both files with their folders and gives the highest version, v17, as the current project hub. |

The assumptions behind these rows and behind the version numbers in this file are ASM-D2-IDX-1 to ASM-D2-IDX-11.

## Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 14 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| 13 | 16 November 2026 | Document set at version 13, carrying D-RCV-35 and D-RCV-36 | Source row |

Change-log row: 14, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
