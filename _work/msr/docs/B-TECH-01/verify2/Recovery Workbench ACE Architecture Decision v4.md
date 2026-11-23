SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

# ACE architecture decision

| Item | Detail |
|---|---|
| Document | Recovery Workbench ACE architecture decision |
| Version | 4 |
| Date | 22 November 2026 |
| Supersedes | Version 3, 15 November 2026 |
| Prepared by | Henka Group |
| Structure | Architecture decision record, ISO/IEC/IEEE 42010 |
| Decision | D-RCV-60: adopt Architecture v5 and realign the documents and stories |
| Status | Draft |
| Change | 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |


# 1. The decision

The Recovery Workbench is built inside ACE, the bank's collection workbench, as its recovery module. The module is delivered as 19 services inside ACE, one per business module, from one service template and the shared libraries: one repository, one pipeline, one schema and one login per service, and one ACE front end whose screens are composed by gateway-bff (ADR-013, ADR-014, ADR-019). The case workflow runs on Temporal, described in CMMN 1.1 terms: one parent CaseWorkflow per case with a child workflow per stage, and case, stage, task and milestone state held as rows in the rwb_case schema (ADR-011, ADR-016). ACE ingests the source data, including SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, the COLLINS scores, the SCBPDM product, NLEADS, EasyApp and Entra ID group mapping. The Workbench runs no inbound load: it reads the data through read-only views (ADR-010), and only rwb-source-data holds those views.

| Question | Decision | Status | Decision log |
|---|---|---|---|
| Where is the Workbench built? | Inside ACE: 19 services, one per business module, one repository and one pipeline per service, one front end | Proposed | DT07; ADR-013 |
| How is the code structured? | One service per module from one service template and the shared libraries: one schema and one login per service, and boundaries checked at build time | Proposed | DT08; ADR-013, ADR-014 |
| How does the case workflow run? | On Temporal: a parent CaseWorkflow per case with a child workflow per stage, and case, stage, task and timer state held as rows in the rwb_case schema. This replaces the version 3 ruling that the case runs in code with no workflow engine | Proposed | DT09; ADR-011, ADR-016 |
| Which case language is shared? | CMMN 1.1: case, stage, task, milestone, sentry | Agreed | DT10 |
| How do rules change? | Every rule, limit, timer and route is a versioned rule package, governed in rwb-decision and evaluated by embedded Drools in the service that owns the decision | Proposed | DT02; ADR-012, ADR-017 |
| How does data arrive? | ACE ingestion: SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS scores, SCBPDM product, NLEADS, EasyApp and Entra ID group mapping land in the ACE database. No Workbench load. Only rwb-source-data reads them, through recovery.v_ace_* views | Agreed | D-RCV-35; ADR-010, ADR-014 |
| How is the front end split? | One ACE front end with a recovery module folder, and composite screens composed by gateway-bff | Proposed | DL07; ADR-006, ADR-019 |
| How do squads merge and release? | Trunk based development with feature flags. A flag that is off returns the previous code path | Agreed | DT11; ADR-021 |


The four rows whose decision changes (DT07, DT08, DT09 and DT02) carry Proposed, the status of the record that replaces them: ADR-013, ADR-014, ADR-016 and ADR-017 are Proposed at 22 November 2026. DL07 was Proposed in version 3 and keeps that status. No approval of version 4 is recorded, so this document is issued as Draft (CG-B-TECH-01-2; ASM-B-TECH-01-2).

## 1.1 Decisions added or amended by this version

| Record | Decision | Effect in this document |
|---|---|---|
| ADR-013 | Run Recovery as 19 services inside ACE | Sections 1, 2 and 4; supersedes ADR-002, the single-service decision |
| ADR-014 | One schema and one login per service in the ACE PostgreSQL database | Sections 3.4, 5 and 7 |
| ADR-015 | Kafka business-event topics with outbox, inbox and CloudEvents | Sections 3.4, 5 and 7 |
| ADR-016 | A reusable Temporal layer, and Temporal Schedules in place of Quartz | Sections 3 and 6; amends ADR-011 |
| ADR-017 | Embedded Drools in each service, with the rule registry in rwb-decision | Sections 1, 3.4 and 7; amends D-RCV-36 T1 and T2 and amends ADR-012 |
| ADR-018 | No data lake; rwb-reporting builds its read model from events | Sections 3.4 and 7 |
| ADR-019 | Edge: gateway-bff for staff and a partner gateway for partners | Sections 1, 2 and 7 |
| ADR-020 | Contract-first REST, one hop, 2 second timeout | Sections 4 and 6 |
| ADR-021 | Per-service Flyway and migration ownership | Sections 5, 6 and 7 |
| ADR-022 | A local decision record plus a central ledger | Sections 3.4 and 5 |
| ADR-023 | Observability per service | Section 7 |


The decision log records D-RCV-60 and DL44 (adopt Architecture v5). DL45 to DL49 cover the story set issued with this version: service epics with business-epic tags, soft ownership by team type, the Epic 1 preservation rule, dates unchanged and tentative, and the gap and assumption registers.

# 2. Where the Workbench is built

A recovery case starts at 90 days past due, when collection hands it over. ACE already runs sign-in with Entra ID and the bank IAM, access control, audit, PII and SOC logging, a case view and the restructure calculator, and it passed the bank's new application standard and penetration test when it went live in October 2026.

| Option | For | Against | Cost and time | Verdict |
|---|---|---|---|---|
| 1. 19 services inside ACE, as the recovery module of ACE | One case view for staff who work collection and recovery; sign-in, audit and logging reused; no integration between collection and recovery; each business module is a service with its own release, contract, schema, topic and task queue (ADR-013) | Nineteen services to run and secure, and nineteen contracts to keep; squads share one release train | Lowest: no new platform to certify; one service template and one pipeline per service | Chosen |
| 2. Separate recovery application on the ACE pattern | Independent releases | Two case views; sign-in, audit and logging rebuilt; an interface between collection and recovery | New application approval and penetration test | Not chosen |
| 3. Separate application on its own platform | Free choice of technology | All of option 2, plus a second platform for SCB IT to run | Highest | Not chosen |


Version 3 chose one service, one repository and one front end (ADR-002). This version supersedes that record: the Workbench stays a module of ACE, and the module is cut along its business modules into the 19 services of Architecture v5, one per module P1 to P10 and S1 to S9 (ADR-013). The reasons for staying inside ACE do not change: one case view, and the sign-in, audit and logging of ACE reused rather than rebuilt.

Epic 1 keeps what it has built or has in build (U2). The split of the single recovery schema of RWB-E1-001 into the rwb_* schemas is new work, carried by RWB-PLT-NF06-DB and the per-service database stories, and it is recorded in the Change Register.

# 3. How the case workflow runs

A recovery case lives for months or years and mostly waits on people, partners and courts. 366 of the 448 routing rules move a case to a state that a person or a partner owns. The workflow must change while cases are open, when a Bank of Thailand rule or a policy adds a step, and it must still hold cases that started under the old version.

## 3.1 Options compared

| Criterion | 1. Programmatic in ACE | 2. Temporal for everything | 3. Programmatic cases, Temporal runs the case | 4. BPMN engine (Flowable) |
|---|---|---|---|---|
| Long human waits (weeks to years) | A wait is a row with a state and a due date | Held as a running workflow execution for the life of the case | Cases as rows; a wait is a Temporal durable timer | Held as a process instance |
| Changing the flow while cases are open | A handler change is an ordinary release; open cases keep their rule version as data | Workflow code must stay deterministic; each change needs a version branch kept for as long as the oldest open case, which for litigation can be ten years | As option 1 for the case state; each stage is a child workflow, and a change is a new version carried by Continue-As-New | Process versions migrate through the engine's migration tools |
| Reporting and audit | SQL on the case tables; the decision log records each rule version | Case history is in Temporal's event history, outside the case tables | As option 1 | Engine history tables |
| Running and storage | No new runtime | One more runtime; history grows with every step, and retention clean-up must skip workflows still open | Two models to run and a bridge between them | One more engine to run |
| Automated chains with other systems | Retry and compensation built with Spring Batch and the outbox | Built in: retries, sagas, resume after failure | Built in for the automated parts | Service tasks in the engine |
| Skills in the teams | Spring Boot, already used by ACE and TechX | Known to TechX; new to the ACE code base | Both teams know both | New to both |
| Effort for Epics 1 and 2 | Lowest | Highest | Higher than option 1 | Higher than option 1 |
| Verdict | Kept for the case state | Not chosen | Chosen (ADR-011, ADR-016) | Not chosen |


The cells of option 3 are rewritten for this version, because version 3 recorded the option as "not now" and no source restates the cells (CG-B-TECH-01-3; ASM-B-TECH-01-3).

## 3.2 Why the programmatic option

- Recovery is case management with long human waits. The case state is a row and the wait is a durable timer, so a wait of a year costs one timer rather than a replay of the flow.

- The flow changes often. With rules as data rows, a threshold or a route changes on its effective date without a release, and open cases keep the version they were decided under. A stage that changes is a new child workflow version, and Continue-As-New keeps the case history bounded.

- The bank runs one shared Temporal cluster, reused by every workbench, and case reporting stays in SQL.

- The ACE team and TechX both build in Spring Boot today.

## 3.3 When Temporal can be added

Temporal suits a self-contained automation task: no human step, a known end within days, called through an API and returning its result to the case. It also runs the case itself, because the case is described in CMMN terms behind one case interface, so the case model did not change when the engine arrived: one parent CaseWorkflow per case, a child workflow per stage, and a task queue per service in the namespace rwb-recovery (ADR-011, ADR-016). Temporal holds no case of record: case data stays in the rwb_case schema (T1). Adding a task needs its own decision record with the task named.

## 3.4 What the build uses instead

- Case, stage, task, milestone and timer state as rows in the rwb_case schema of the ACE database, owned by P3 rwb-case

- Temporal for the case lifecycle: a parent CaseWorkflow per case with a child workflow per stage, durable timers, and a Temporal Schedule or an event-started workflow in place of every Quartz job in the owning service (ADR-016). The bank's Airflow scheduler keeps the cross-system edges, for discussion

- A transactional outbox and an inbox in every service, and business events on Kafka as CloudEvents with a topic per service (ADR-015)

- Embedded Drools in the owning service, evaluating versioned rule packages that rwb-decision governs: the 448 routing rules, hit policy Unique, in 10 route sets (ADR-017)

- A decision record written in the same transaction as the action, held locally in the service's own schema and sealed in the central ledger in rwb-decision; the points of no return wait for the ledger to acknowledge the record (ADR-022)

- No data lake: rwb-reporting builds its measures and regulatory extracts from the events (ADR-018)

# 4. How the code is structured

| Option | For | Against | Cost and time | Verdict |
|---|---|---|---|---|
| 1. 19 services by module, from one service template | Independent deployment per module; each module owns its tables in its own schema; boundaries checked at build time against the contract | Nineteen services, schemas and contracts to keep in step; contract-first discipline before the squads start (DL37) | Low per service: one service template, one Helm chart, one pipeline and shared libraries | Chosen |
| 2. Separate services per team | Independent deployment | Network calls between modules, separate databases, more to run and secure | High | Not chosen: the services follow the 19 business modules, not the teams |
| 3. One code base with no module boundaries | Nothing to set up | One team's change breaks another's; the service becomes hard to change | Low now, high later | Not chosen |


Each service reads only its own tables and reaches another service through its published contract or an application event (ADR-014, ADR-020). There are two exceptions, and they are written down rather than left to judgement: rwb-source-data reads source data through recovery.v_ace_* views, which read the public ACE tables (ADR-010); and rwb-treatment calls the ACE restructure calculator through a Temporal Nexus operation. No other service holds a direct read of a public ACE table, no write to it and no foreign key into it, because ACE cascades deletes on account (ADR-010).

The boundary is checked in the build: a cross-schema reference, a call that is not contract-first, or a call chain longer than one hop fails it. Every service is built from the same template, which carries the api and worker deployments, the outbox relay, the inbox, the Temporal worker and codec, OpenTelemetry and the contract tests.

# 5. How data arrives

| Option | For | Against | Cost and time | Verdict |
|---|---|---|---|---|
| 1. ACE ingestion, read through read-only views | One way in, run by the team that already ingests the data; one set of checks; no change to legacy systems; one copy of every record | The Workbench waits for the ACE additions (DL43); the data is as fresh as ACE holds it, end of day for COLLINS | Lowest: no inbound load to build or run | Chosen |
| 2. COLLINS daily batch plus Workbench file loads | The Workbench controls its own load and its own checks | A second copy of every record, kept in step by hand; a load, data quality and tracker estate to build and run | High | Not chosen; superseded by ADR-010 |
| 3. Real-time interfaces to each system of record | Same-day data | New interfaces into legacy systems; each one an enhancement request | High | Not chosen |
| 4. Events for every source | Same-day data with loose coupling | Sources do not publish events today | High | Not chosen |


Every source in scope arrives through ACE's ingestion. ACE holds account, payment, customer, address, phone, email, relation, collateral, asset, collections action, assignment, bucket, product and branch data today. SVAF appraisals, CCMS collateral detail, AMIS and RPS repossessed and purchased assets, LIT litigation and hearings, WIN proof of delivery, GL write-off postings, the COLLINS scores, the SCBPDM product holding, NLEADS credit decisions, EasyApp signature requests and Entra ID group mapping are added under RWB-ACE-001 (DL43).

The services own the case and the extension tables; ACE owns the source data. Four tiers: 22 Tier 1 ACE tables read through 16 views; 14 Tier 2 ACE tables and 12 columns, raised in RWB-ACE-001, read through 14 views; 4 Workbench extension tables keyed by ACE business keys; and 88 Workbench tables that stay. The Workbench holds 92 tables across its 19 schemas, and the dictionary holds 122 objects and 1,366 fields in place of 108 and 1,256. The 30 views sit in the recovery schema and are granted to rwb-source-data alone (ADR-010, ADR-014).

Same-day needs are named under DL06: the case transfer from EFS, a payment received and a legal event. The Workbench no longer meets them with its own feed. They depend on what ACE ingests, and the age of the data is visible on every view.

## 5.1 Schema and login per service

| Code | Service | Schema | Wave | What it owns |
|---|---|---|---|---|
| P1 | rwb-source-data | rwb_source_data | 1 | ACE view contract, extension tables, freshness, reconciliation |
| P2 | rwb-integration | rwb_integration | 1 | interface config, file runs, outbound items, ACE integration paths |
| P3 | rwb-case | rwb_case | 1 | case, CMMN state, queues, tasks, allocation, timers |
| P4 | rwb-access | rwb_access | 1 | Recovery roles as data, scope, masking policy, DoA table, access log |
| P5 | rwb-document | rwb_document | 1 | metadata, custody, OCR text and fields, signatures, retention |
| P6 | rwb-comms | rwb_comms | 1 | notices, templates, merge fields, proof of delivery |
| P7 | rwb-decision | rwb_decision | 1 | approvals, central decision ledger, DMN model registry |
| P8 | rwb-payment | rwb_payment | 2 | payment and proceeds matching, fees, bookings, posting files |
| P9 | rwb-reporting | rwb_reporting | 1 | measures, snapshots, steering dashboard, regulatory reports |
| P10 | rwb-agent | rwb_agent | 1 | agent policies, prompts, runs, guardrails, evaluations |
| S1 | rwb-valuation | rwb_valuation | 3 | valuations, D6 route decision, route agent output |
| S2 | rwb-treatment | rwb_treatment | 2 | treatments, contracts, settlement and deed-in-lieu agreements, plan timers |
| S3 | rwb-guarantee | rwb_guarantee | 3 | TCG and insurance claims, guarantor notices and pursuit |
| S4 | rwb-litigation | rwb_litigation | 3 | legal actions, hearings, judgments, enforcement, LED auction ladder |
| S5 | rwb-asset | rwb_asset | 2 | assets taken on, holding, floor price, listings, auction rounds |
| S6 | rwb-debtsale | rwb_debtsale | 3 | lots, data room, buyer terms, bids, award, transfer |
| S7 | rwb-writeoff | rwb_writeoff | 4 | eligibility, committee, posting, recovery after charge-off |
| S8 | rwb-deviation | rwb_deviation | 2 | X1-X7 screening, pause, handling, return |
| S9 | rwb-partner | rwb_partner | 4 | panel, partner users, instructions, results, fees, scorecards |


The owner of every table, operation, event, job and workflow is fixed in the Microservice Ownership Map v1, and the per-service table counts follow from it; the source documents do not state them (CG-B-TECH-01-6; ASM-B-TECH-01-6).

## 5.2 Migration and schema ownership

Every schema is delivered as its own SQL file with its own Flyway sequence: 19 rwb_<name>.sql files, plus recovery_views.sql for the 30 views and a README (ADR-021). No service runs another service's migration. The four extension tables party_ext, contact_point_ext, account_ext and valuation_ext stay in rwb_source_data, and the Workbench adds no table and no column to an ACE schema.

# 6. How squads merge and release

Two TechX squads and the collection squad release the 19 services. Each service has its own repository, pipeline and Flyway sequence, all built from one service template and the shared libraries (ADR-013, ADR-021). Branches merge into main at least once a working day. Unfinished work sits behind a feature flag; a flag that is off returns the previous code path, so a change that fails SIT or UAT is switched off and the release goes ahead. Untested code is not merged. Each service merges through code owners, and the ACE team owns the common module and the release decision (DL04). One release train is shared with collection, and a service that is not ready stays behind its flag. The number of squads for 19 services is not restated in any source (CG-B-TECH-01-5; ASM-B-TECH-01-5).

# 7. Consequences

| Area | What follows |
|---|---|
| Security | Sign-in, the bank IAM, access control, audit, PII and SOC logging come from ACE, and rwb-access is the authorise contract and the guard library for the 19 services (ADR-013) |
| Staff | One case view across collection and recovery, composed for the screens by gateway-bff (ADR-019) |
| Release | One release train with collection; nineteen pipelines, one per service, with its own Flyway sequence and merge ownership (DL04, ADR-021) |
| Data | ACE owns the source data and the Workbench owns the case: 92 tables and 30 views, and 1,366 dictionary fields, in place of 108 tables and 1,256 fields. The 92 tables sit in 19 schemas with one login each, and only rwb-source-data reads the ACE views (ADR-014). Source data is read through read-only views, so there is one copy of every record and no inbound load (ADR-010). The Workbench cannot start before the ACE additions land (DL43) |
| Build | Retry and compensation come from Temporal for the case lifecycle and the sagas, and from the outbox for events; each service has an outbox relay and an inbox (ADR-015, ADR-016) |
| Rules | Embedded Drools in the owning service, rule packages governed in rwb-decision, and every answer naming the rule and the package version (ADR-017) |
| Reporting | No data lake: rwb-reporting projects the measures and the regulatory extracts from the events (ADR-018) |
| Observability | Traces, metrics and logs from every service on one OpenTelemetry pipeline, and a health and metrics endpoint per service (ADR-023) |
| Partners | Partner access from outside the bank needs an architecture change with one to three months of lead time (DL03), and it arrives through the partner gateway in the DMZ, which fronts rwb-partner only (ADR-019) |


# 8. Open points

| ID | Question | Proposed answer | Owner | Due |
|---|---|---|---|---|
| DL03 | Who raises the architecture change for partner access from outside the bank | The Workbench team or the ACE team, raised in November | Not specified in the source documents (CG-B-TECH-01-1; ASM-B-TECH-01-1); with the architecture team | 29 October 2026 |
| DL04 | Who merges between squads and decides when a change holds the release | Each service through code owners; the ACE team for the common module and the release | Not specified in the source documents (CG-B-TECH-01-1; ASM-B-TECH-01-1) | 29 October 2026 |
| DL05 | Who creates the recovery module in ACE | TechX creates the 19 services from the service template in its own packages from 2 November, then the ACE team applies the boundaries | Not specified in the source documents (CG-B-TECH-01-1; ASM-B-TECH-01-1) | 29 October 2026 |
| DL06 | Which interfaces need same-day data | Option A (daily batch through COLLINS) superseded by D-RCV-35. Same-day triggers stay named; they depend on what ACE ingests | Not specified in the source documents (CG-B-TECH-01-1; ASM-B-TECH-01-1) | 30 October 2026 |
| DL07 | How the ACE front end is split | One front end with a recovery folder from 2 November, and composite screens composed by gateway-bff (ADR-019) | Not specified in the source documents (CG-B-TECH-01-1; ASM-B-TECH-01-1) | 31 October 2026 |
| DL37 | When code owners and the browser test runner are in place | Code owners before 2 November; browser runner before the first SIT run | Not specified in the source documents (CG-B-TECH-01-1; ASM-B-TECH-01-1) | 6 November 2026 |
| DL43 | Does the ACE team accept the RWB-ACE-001 scope and its dates | Accept the 14 tables, 12 columns and 80 fields, delivered by 21 November 2026 | ACE team lead | 21 November 2026 |


The Owner column of DL03 to DL07 and DL37 carries the placeholder of Template and Rules R9 because the source names individuals; the role each holds is not stated in the source (CG-B-TECH-01-1; ASM-B-TECH-01-1). Every due date and every number is copied unchanged.

# 9. Approval

| Role | Approves | Status |
|---|---|---|
| SCB CTO | The decision as a whole | To approve |
| SCB IT architecture | Sections 2 to 5 | To approve |
| ACE team lead | Sections 3, 4 and 6 | Agreed |
| TechX delivery lead | Sections 3, 4 and 6 | Agreed |
| Henka solution architect | The decision as a whole | Agreed |


The statuses are those of version 3, copied unchanged. Version 4 was issued under D-RCV-60 without a new approval round (CG-B-TECH-01-2; ASM-B-TECH-01-2).

# 10. Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 4 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |


Version 4 keeps every section, ID, number and date of version 3, and changes only what the realignment needs:

- The decision becomes 19 services inside ACE, one per business module, with one schema, one login, one repository and one pipeline each (ADR-013, ADR-014). ADR-013 supersedes ADR-002, the single-service decision; section 2 says so.

- The case lifecycle moves onto Temporal, one parent CaseWorkflow per case with a child workflow per stage, and Schedules in place of Quartz (ADR-011, ADR-016). The version 3 ruling that the case runs in code with no workflow engine is replaced; the CMMN case model and the row-based case state stay.

- Rules become embedded Drools in the owning service with the registry in rwb-decision (ADR-012, ADR-017), and the decision record becomes local plus a central ledger (ADR-022).

- Section 5 gains the schema and login table for the 19 services (ADR-014) and per-service migration ownership (ADR-021); section 7 gains the rules, reporting and observability consequences (ADR-017, ADR-018, ADR-023).

- The Owner column of sections 8 and 9 is roles only, and the rows that named an individual carry the Template and Rules R9 placeholder (CG-B-TECH-01-1; ASM-B-TECH-01-1).
