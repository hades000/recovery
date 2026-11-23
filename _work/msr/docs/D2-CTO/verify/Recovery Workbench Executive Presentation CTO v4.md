## Slide 1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd
Recovery Workbench: 19 services inside ACE
Version 4, microservice realignment (D-RCV-60)
Executive presentation for the CTO

Change log: v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash
Release dates are kept as issued and are tentative (R1 U7, DL48).

SCB

## Slide 2

Change log and what this version adds

| Version | Date | Change | Tool |
|---|---|---|---|
| v3 | 28 October 2026 | Executive presentation for the CTO: architecture and build, as issued | — |
| v4 | 22 November 2026 | Services, waves, Day-1 work and gaps added; decisions ADR-013 to ADR-023 and DL44 to DL49 applied; version 3 content kept on slides 13 to 19 | T3 Code / OpenCode / DeepSeek v4.1 Flash |


v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash

•  Version 4 is diagram-led on four questions: which services, in which wave, what can start on Day 1, and which gaps remain.
•  Every source section, ID, count and date of version 3 is kept; release dates stay as issued and are tentative (R1 U7, DL48).
•  Sources: Architecture v5 (slides 13 to 20 and 41 to 44), the Temporal and Drools design v1, Ownership Map v1, Template and Rules v1 and the split plan.

2

## Slide 3

What this version changes in the deck

Statements on the version 3 slides are kept word for word. Where the realignment changes an answer, the decision that changes it is named here (R3 precedence: Architecture v5 first).

| Version 3 slide | Statement in version 3 | After D-RCV-60 | Decision |
|---|---|---|---|
| 2 | Build on ACE: one service, one repository, one front end | 19 services inside ACE, one repository and one epic per service; ACE sign-in, IAM, audit, PII and SOC logs reused | ADR-013, DL44 |
| 2 | Programmatic workflow: no Temporal | CaseWorkflow with a child workflow per stage on one shared, reusable Temporal layer; Schedules replace Quartz | ADR-016, DL44 |
| 3 | PostgreSQL with the recovery schema: 108 entities, 1,256 fields, 14 data products | One rwb_<name> schema and login per service in the ACE database; never read another service's tables | ADR-014, ADR-021 |
| 2 | Data through COLLINS: daily batch into the ACE database | Kept: ACE data arrives as before and is read through rwb-source-data's contract or the service's own v_ace_* views | ADR-014 |
| 5 | Out: reporting to the data lake | No data lake: rwb-reporting builds its read model from events | ADR-018 |
| 6 | Two TechX recovery squads, one repository | Kept as a suggestion only: ownership is soft by team type and any team may pick up a story | DL45, DL46 |
| 7 | DL03, DL05, DL06, DL07, DL11, DL12, DL21 and DL27 are open | IDs and dates kept; DL05 is restated for 19 services: one repository per service from the service template | ADR-013, DL44 |


3

## Slide 4

Realignment at a glance: the wave bands

•  19 services, one epic each (RWB-SVC-P1 to RWB-SVC-S9), plus 7 platform epics (RWB-PLT-TPL, -LIB, -WF, -DB, -EVT, -EDGE, -OBS) and 5 integration epics (RWB-ITG-W1 to W4 and -NFR).
•  Legacy stories by wave: 73 in Wave 1, 72 in Wave 2, 76 in Wave 3, 110 in Wave 4, 8 in the platform and NF band, 19 new and integration keys.
•  Diagram of record: Recovery Workbench Microservice Architecture by Epic and Story v1, and Wave 1 to Wave 4 Architecture v1 (folder 22).

Wave 0
platform and NF
7 platform epics

PLT-TPL
template and repositories

PLT-LIB
shared libraries

PLT-WF
Temporal workflow kit

PLT-DB
ACE DB schemas and logins

PLT-EVT
Kafka event platform

PLT-EDGE
edge and gateway

PLT-OBS
observability

Wave 1
9 services
EP01

P1
rwb-source-data

P2
rwb-integration

P3
rwb-case

P4
rwb-access

P5
rwb-document

P6
rwb-comms

P7
rwb-decision

P9
rwb-reporting

P10
rwb-agent

Wave 2
4 services
EP02, EP03

P8
rwb-payment

S2
rwb-treatment

S5
rwb-asset

S8
rwb-deviation

Wave 3
4 services
EP04, EP05

S1
rwb-valuation

S3
rwb-guarantee

S4
rwb-litigation

S6
rwb-debtsale

Wave 4
2 services
EP06 to EP08

S7
rwb-writeoff

S9
rwb-partner

4

## Slide 5

The ten platform services: 9 in Wave 1, 1 in Wave 2

| Code | Service | Wave | Service epic | Owns (Architecture v5 slide 41) |
|---|---|---|---|---|
| P1 | rwb-source-data | 1 | RWB-SVC-P1 | ACE view contract, extension tables, freshness, reconciliation |
| P2 | rwb-integration | 1 | RWB-SVC-P2 | interface config, file runs, outbound items, ACE integration paths |
| P3 | rwb-case | 1 | RWB-SVC-P3 | case, CMMN state, queues, tasks, allocation, timers |
| P4 | rwb-access | 1 | RWB-SVC-P4 | roles as data, scope, masking policy, DoA table, access log |
| P5 | rwb-document | 1 | RWB-SVC-P5 | metadata, custody, OCR text and fields, signatures, retention |
| P6 | rwb-comms | 1 | RWB-SVC-P6 | notices, templates, merge fields, proof of delivery |
| P7 | rwb-decision | 1 | RWB-SVC-P7 | approvals, central decision ledger, DMN model registry |
| P8 | rwb-payment | 2 | RWB-SVC-P8 | payment and proceeds matching, fees, bookings, posting files |
| P9 | rwb-reporting | 1 | RWB-SVC-P9 | measures, snapshots, steering dashboard, regulatory reports |
| P10 | rwb-agent | 1 | RWB-SVC-P10 | agent policies, prompts, runs, guardrails, evaluations |


Every service: schema rwb_<short> with its own login, REST base /api/recovery/<short>/v1 behind gateway-bff, topic rwb.<short>.events.v1 with retry and .dlt, task queue rwb-<short> in namespace rwb-recovery (R4).

5

## Slide 6

The nine stage services: Waves 2 to 4

| Code | Service | Wave | Service epic | Owns (Architecture v5 slide 41) |
|---|---|---|---|---|
| S1 | rwb-valuation | 3 | RWB-SVC-S1 | valuations, D6 route decision, route agent output |
| S2 | rwb-treatment | 2 | RWB-SVC-S2 | treatments, contracts, settlement and deed-in-lieu agreements, plan timers |
| S3 | rwb-guarantee | 3 | RWB-SVC-S3 | TCG and insurance claims, guarantor notices and pursuit |
| S4 | rwb-litigation | 3 | RWB-SVC-S4 | legal actions, hearings, judgments, enforcement, LED auction ladder |
| S5 | rwb-asset | 2 | RWB-SVC-S5 | assets taken on, holding, floor price, listings, auction rounds |
| S6 | rwb-debtsale | 3 | RWB-SVC-S6 | lots, data room, buyer terms, bids, award, transfer |
| S7 | rwb-writeoff | 4 | RWB-SVC-S7 | eligibility, committee, posting, recovery after charge-off |
| S8 | rwb-deviation | 2 | RWB-SVC-S8 | X1-X7 screening, pause, handling, return |
| S9 | rwb-partner | 4 | RWB-SVC-S9 | panel, partner users, instructions, results, fees, scorecards |


Rules run inside the owning service (embedded Drools) with the rule package registry in rwb-decision; decision records are written locally and sealed centrally (DP-03, DP-04).

6

## Slide 7

Wave plan: 5 bands, 19 services, one programme

| Wave | Services in the wave | Count | Business epic (R5.6) | Platform or integration epic |
|---|---|---|---|---|
| 0 | none: the platform, the shared libraries and the edge | 0 | platform and non-functional | RWB-PLT-TPL, -LIB, -WF, -DB, -EVT, -EDGE, -OBS and RWB-ITG-NFR |
| 1 | P1, P2, P3, P4, P5, P6, P7, P9, P10 | 9 | EP01 | RWB-ITG-W1 |
| 2 | P8, S2, S5, S8 | 4 | EP02, EP03 | RWB-ITG-W2 |
| 3 | S1, S3, S4, S6 | 4 | EP04, EP05 | RWB-ITG-W3 |
| 4 | S7, S9 | 2 | EP06, EP07, EP08 | RWB-ITG-W4 |


Release dates by wave: Not specified in the source documents (CG-D2-CTO-1; ASM-D2-CTO-3). Every release date is kept as issued and is tentative (R1 U7, DL48).

•  A story whose business-epic wave is earlier than its service wave keeps the business-epic wave (R5.6).
•  Wave 0 does not wait for Wave 1: the service template, the workflow kit, the event platform and the edge contract are Day 1 work for every team type (R5.7).

7

## Slide 8

Day-1 work: 939 of 1,034 story slices can start on Day 1

| Team type (suggested owner) | Work types (R5.3) | Day-1 position |
|---|---|---|
| TechX | CON, APP, ITG | At least one CON story per service, and every CON story is Day 1 (R5.7.1, R5.7.7); the new platform stories N001 to N012 are Day 1 |
| ACE team | DB | Day 1 by rule R5.7.6: every team type has Day-1 work; only H dependencies, and a platform CON story is Day 1 itself |
| SCB IT infrastructure | INF | Day 1 by rule R5.7.6 |
| DevOps team | OPS | Day 1 by rule R5.7.6; the new platform stories N001 to N012 carry it |
| QA team | ITG harness and NFR | The integration harness W1J01 is Day 1 (R5.7.6) |


1,034
story slices in the split plan

939
ready on Day 1

510
parallel lanes, at most 4 deep

5
team types with Day-1 work

C dependencies never block a build: a story builds against the published contract and its fake (R5.7.2). A lane is a connected group of non-CON stories linked by H, at most 4 deep (R5.7.5).

8

## Slide 9

Ownership: soft, by team type (Ownership Map v1)

| Ownership Map v1 sheet | Rows | What it fixes for the CTO |
|---|---|---|
| Services | 19 | code, service, wave, schema, REST base, topic and task queue for each service |
| Tables | 93 | the one service that owns each table; no table is read by another service |
| Endpoints | 156 | the owner of every REST operation |
| Events | 30 | the producer of every event; consumers read only through their own inbox |
| Workflows and activities | 15 | the service that owns each workflow or activity |
| Jobs | 22 | the owner and the replacement mechanism: a Temporal Schedule or an event-started workflow, no shared Quartz tables |
| Rulings | 71 | the default ruling where the sources are silent |


•  Default rulings (R3): parameters and reference data, and the case list API, to P3 rwb-case; the rule package registry to P7 rwb-decision; the interaction ledger to P1 rwb-source-data; feature flags to the platform library.
•  Owners are suggestions only: any team may pick up a story (R1 U3, DL46). No person is named anywhere.

9

## Slide 10

Gaps and assumptions that matter to the CTO

| Candidate gap | What is missing or in conflict | Type | Severity | Handling |
|---|---|---|---|---|
| CG-D2-CTO-1 | Release dates are not stated per wave in the sources; story releases are per story only | Missing | P2 | Left as a placeholder on the wave slide; dates stay tentative (R1 U7, DL48) |
| CG-D2-CTO-2 | The version 3 slides describe the monolith (one service, no Temporal, a data lake); Architecture v5 says 19 services, Temporal and no data lake | Conflict | P3 | Version 3 slides kept; the "what this version changes" slide maps each statement to its decision |
| CG-D2-CTO-3 | No accountable team per service: ownership is soft, by work type (R1 U3) | Missing | P3 | Service owners shown as the service code of the Ownership Map plus the suggested work-type owner |
| CG-D2-CTO-4 | 19 legacy keys in the split plan carry no wave value (new and integration keys) | Ambiguous | P3 | Wave taken from the service or the integration epic (R4, R5.1) |


Candidate rows are numbered GAP-nnnn and ASM-nnnn at step D1 and land in the Gap Register and the Assumptions Register (folder 23, Template and Rules R9). Severity: P1 blocks a wave start, P2 blocks a story's Done, P3 is documentation only.

10

## Slide 11

Where to read more

•  Architecture: Recovery Workbench Architecture v5 Text Extract v1 and the Temporal and Drools Design Text Extract v1 (folder 22).
•  Ownership: Recovery Workbench Microservice Ownership Map v1, 19 services, 93 tables, 156 endpoints, 30 events, 15 workflows and activities, 22 jobs.
•  Delivery: the service story set (358 legacy stories into 1,034 slices), the Service Story Catalog v1, the Day-1 Work Allocation v1 and the Service Epics v1.
•  Decisions and registers: ADR-013 to ADR-023, Decision Log rows DL44 to DL49, the Change Register v1, and the Gap Register and Assumptions Register (folder 23).
•  Diagrams: Recovery Workbench Microservice Architecture by Epic and Story v1, and Wave 1 to Wave 4 Architecture v1.

11

## Slide 12

Version 3 content, kept unchanged

•  Slides 13 to 19 are the version 3 slides of 28 October 2026, kept word for word (R8.2 versioning; CG-D2-CTO-2).
•  They describe the monolith that was current in October 2026: one service, one repository, programmatic workflow and a data lake.
•  Where a statement there differs from the section above, this section and its decision win (R3 precedence, Architecture v5 first).

12

## Slide 13

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION
Recovery Workbench: architecture and build

Executive presentation for the CTO. Henka Group, 28 October 2026
(C) Siam Commercial Bank and Henka Pte Ltd

## Slide 14

Architecture decisions taken

14

| Decision | What it means |
|---|---|
| Build on ACE (DT07) | One service, one repository, one front end; reuse of ACE sign-in, IAM, audit, PII and SOC logs |
| Modular monolith (DT08) | Collection, recovery and common modules by folder; boundaries checked at build time |
| Programmatic workflow (DT09) | Case, stage and task state in the database; CMMN 1.1 terms; no Temporal |
| Data through COLLINS (DT12) | Daily batch into the ACE database; file loads for CCMS, SVAF, AMIS, RPS, WIN and GL |
| Trunk based with flags (DT11) | Untested code is not merged; any change can be switched off |
| Document hub (DT06) | The recovery module is the system of record for recovery documents |


## Slide 15

The architecture on one page

15

| Layer | Design |
|---|---|
| Front end | React on Vite with Radix in the ACE front end; recovery screens in the recovery module folder |
| Service | Spring Boot ACE service; recovery module with ten platform and nine stage modules |
| Data | PostgreSQL with the recovery schema: 108 entities, 1,256 fields, 14 data products; Blob storage with a write-once container |
| Rules | 448 rules in ten route sets as DMN decision tables; versioned data |
| Integration | COLLINS batch, file loads, outbox with retry; 144 REST endpoints in OpenAPI 3.1 |
| AI | 12 agents through one orchestrator and tool gateway; 10 bank models from COLLINS; fallback to rules |
| Security | Entra ID, role, capability, scope and masking on every request; decision log hash chained |


## Slide 16

Data

16

|  | Data product | System of record | How it arrives | Freshness |
|---|---|---|---|---|
| DP01 | Account and arrears | Core bank (ALS) | COLLINS daily batch | End of day; in the Workbench the next morning |
| DP02 | Customer and party | SCBPDM and core bank | COLLINS daily batch | End of day; in the Workbench the next morning |
| DP03 | Case and ownership | Recovery Workbench | Held in the Workbench | As it changes |
| DP04 | Treatment and offers | Recovery Workbench; restructure plans in ACE | Held in the Workbench | As it changes |
| DP05 | Contact and promises | EFS before day 90; the Workbench after | COLLINS daily batch from EFS; held in the Workbench | End of day for EFS history; as it changes after |
| DP06 | Collateral and assets | CCMS, SVAF, AMIS, RPS | File load until a batch feed exists | Weekly or monthly today |
| DP07 | Legal events and cases | LIT for court records; the Workbench for instructions | COLLINS daily batch for litigation status; held in the Workbench | End of day for LIT status |


## Slide 17

Integration

17

| Route | What | How often |
|---|---|---|
| In through COLLINS | Accounts, payments, customers, collections history, litigation status, scores | Daily |
| In by file | Collateral, appraisals, assets, repossessions, proofs of delivery, postings | Weekly or monthly |
| Out | Notices to WIN; SMS and LINE through ACE; reporting to the data lake | Daily or as sent |
| Partners | Partner portal through the external gateway (DL03) | As entered |


## Slide 18

Build approach

18

| Item | Approach |
|---|---|
| Squads | Two TechX recovery squads with the ACE team and the collection squad in one repository |
| Flow | Kanban; monthly releases; SIT and UAT one week each |
| Quality | Nine pipeline gates; rule table tests for every row; regression suite on every release |
| AI-assisted development | Coding tool under DL32; AI first-pass review on every pull request |
| Specifications | FSD and TSD per module; Epics 1 and 2 at development detail; Epics 3 to 8 at architecture, API and integration detail |


## Slide 19

Technical decisions needed

19

|  | Decision | Recommended answer |
|---|---|---|
| DL03 | How partners reach the partner portal from outside the bank | Raise the external gateway change in November; partners keep current channels until then |
| DL05 | Who creates the recovery module in ACE | TechX builds in its own package from 2 November; the ACE team applies the boundaries |
| DL06 | Which interfaces need real-time data | Daily batch; same-day triggers named now: EFS hand-over, payment received, legal event |
| DL07 | How the front end is split into modules | One front end with a recovery module folder |
| DL11 | Non-functional target values | ACE values where ACE has them; proposed values for the rest |
| DL12 | Which legacy systems are kept | Keep the systems in the integration inventory, with what the Workbench reads from each |
| DL21 | Which systems carry the case identifier | The Workbench and WIN carry the case number in Epics 1 and 2 |
| DL27 | Storage, backup, legal hold and e-discovery for the document hub | ACE storage pattern with a write-once container and the bank backup |

