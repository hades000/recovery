Recovery Workbench

ACE architecture decision

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench ACE architecture decision |
| Version | 3 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | Architecture decision record, ISO/IEC/IEEE 42010 |


# 1. The decision

The Recovery Workbench is built inside ACE, the bank's collection workbench, as its recovery module. The case workflow runs in code, described in CMMN 1.1 terms, with no workflow engine. ACE ingests the source data, including SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, the COLLINS scores, the SCBPDM product, NLEADS, EasyApp and Entra ID group mapping. The Workbench runs no inbound load: it reads the data through read-only views (ADR-010).

| Question | Decision | Status | Decision log |
|---|---|---|---|
| Where is the Workbench built? | Inside ACE: one service, one repository, one front end | Agreed | DT07 |
| How is the code structured? | Modular monolith: common, collection and recovery modules by folder, with boundaries checked at build time | Agreed | DT08 |
| How does the case workflow run? | In code, with case, stage, task and timer state held as rows in the ACE database. No Temporal | Agreed | DT09 |
| Which case language is shared? | CMMN 1.1: case, stage, task, milestone, sentry | Agreed | DT10 |
| How do rules change? | Every rule, limit, timer and route is a versioned data row evaluated by a decision table component | Agreed | DT02 |
| How does data arrive? | ACE ingestion: SVAF, CCMS, AMIS, RPS, LIT, WIN, GL, COLLINS scores, SCBPDM product, NLEADS, EasyApp and Entra ID group mapping land in the ACE database. No Workbench load. The recovery module reads them through recovery.v_ace_* views | Agreed | D-RCV-35; ADR-010 |
| How is the front end split? | One ACE front end with a recovery module folder | Proposed | DL07 |
| How do squads merge and release? | Trunk based development with feature flags. A flag that is off returns the previous code path | Agreed | DT11 |


# 2. Where the Workbench is built

A recovery case starts at 90 days past due, when collection hands it over. ACE already runs sign-in with Entra ID and the bank IAM, access control, audit, PII and SOC logging, a case view and the restructure calculator, and it passed the bank's new application standard and penetration test when it went live in October 2026.

| Option | For | Against | Cost and time | Verdict |
|---|---|---|---|---|
| 1. Recovery module of ACE | One case view for staff who work collection and recovery; sign-in, audit and logging reused; no integration between collection and recovery | Squads share one repository and one release | Lowest: no new platform to certify | Chosen |
| 2. Separate recovery application on the ACE pattern | Independent releases | Two case views; sign-in, audit and logging rebuilt; an interface between collection and recovery | New application approval and penetration test | Not chosen |
| 3. Separate application on its own platform | Free choice of technology | All of option 2, plus a second platform for SCB IT to run | Highest | Not chosen |


# 3. How the case workflow runs

A recovery case lives for months or years and mostly waits on people, partners and courts. 366 of the 448 routing rules move a case to a state that a person or a partner owns. The workflow must change while cases are open, when a Bank of Thailand rule or a policy adds a step, and it must still hold cases that started under the old version.

## 3.1 Options compared

| Criterion | 1. Programmatic in ACE | 2. Temporal for everything | 3. Programmatic cases, Temporal for automation tasks | 4. BPMN engine (Flowable) |
|---|---|---|---|---|
| Long human waits (weeks to years) | A wait is a row with a state and a due date | Held as a running workflow execution for the life of the case | Cases as rows; Temporal only for short tasks | Held as a process instance |
| Changing the flow while cases are open | A handler change is an ordinary release; open cases keep their rule version as data | Workflow code must stay deterministic; each change needs a version branch kept for as long as the oldest open case, which for litigation can be ten years | As option 1 for cases; Temporal versioning only for short tasks | Process versions migrate through the engine's migration tools |
| Reporting and audit | SQL on the case tables; the decision log records each rule version | Case history is in Temporal's event history, outside the case tables | As option 1 | Engine history tables |
| Running and storage | No new runtime | One more runtime; history grows with every step, and retention clean-up must skip workflows still open | Two models to run and a bridge between them | One more engine to run |
| Automated chains with other systems | Retry and compensation built with Spring Batch and the outbox | Built in: retries, sagas, resume after failure | Built in for the automated parts | Service tasks in the engine |
| Skills in the teams | Spring Boot, already used by ACE and TechX | Known to TechX; new to the ACE code base | Both teams know both | New to both |
| Effort for Epics 1 and 2 | Lowest | Highest | Higher than option 1 | Higher than option 1 |
| Verdict | Chosen | Not chosen | Not now; can be added for a task under a separate decision | Not chosen |


## 3.2 Why the programmatic option

- Recovery is case management with long human waits. Rows and due dates hold these waits with nothing to replay.

- The flow changes often. With rules as data rows, a threshold or a route changes on its effective date without a release, and open cases keep the version they were decided under.

- The bank runs no extra runtime, and case reporting stays in SQL.

- The ACE team and TechX both build in Spring Boot today.

## 3.3 When Temporal can be added

Temporal suits a self-contained automation task: no human step, a known end within days, called through an API and returning its result to the case. Because the case is described in CMMN terms behind one case interface, such a task can run on Temporal later without changing the case model. Adding it needs its own decision record with the task named.

## 3.4 What the build uses instead

- Case, stage, task, milestone and timer state as rows in the ACE database

- Quartz for schedules and timers; Spring Batch for automated chains

- A transactional outbox for application events between modules

- A decision table component that evaluates the 448 routing rules, hit policy Unique, in 10 route sets

- An append-only decision log written before every action; a failed write stops the action

# 4. How the code is structured

| Option | For | Against | Cost and time | Verdict |
|---|---|---|---|---|
| 1. Modular monolith by folder | One deployment and one database; each module owns its tables; boundaries tested at build time | Boundary tests and code owners needed before the squads start (DL37) | Low: folders and checks in the existing service | Chosen |
| 2. Separate services per team | Independent deployment | Network calls between modules, separate databases, more to run and secure | High | Not chosen |
| 3. One code base with no module boundaries | Nothing to set up | One team's change breaks another's; the service becomes hard to change | Low now, high later | Not chosen |


Until the ACE team has moved ACE to the modular monolith, TechX builds the recovery module in its own package (DL05). A module reads only its own tables and reaches another module through its published interface or an application event. There is one exception, and it is written down rather than left to judgement: the recovery module reads source data through recovery.v_ace_* views, which read the public ACE tables. It holds no direct read of a public table, no write to it and no foreign key into it, because ACE cascades deletes on account (ADR-010).

# 5. How data arrives

| Option | For | Against | Cost and time | Verdict |
|---|---|---|---|---|
| 1. ACE ingestion, read through read-only views | One way in, run by the team that already ingests the data; one set of checks; no change to legacy systems; one copy of every record | The Workbench waits for the ACE additions (DL43); the data is as fresh as ACE holds it, end of day for COLLINS | Lowest: no inbound load to build or run | Chosen |
| 2. COLLINS daily batch plus Workbench file loads | The Workbench controls its own load and its own checks | A second copy of every record, kept in step by hand; a load, data quality and tracker estate to build and run | High | Not chosen; superseded by ADR-010 |
| 3. Real-time interfaces to each system of record | Same-day data | New interfaces into legacy systems; each one an enhancement request | High | Not chosen |
| 4. Events for every source | Same-day data with loose coupling | Sources do not publish events today | High | Not chosen |


Every source in scope arrives through ACE's ingestion. ACE holds account, payment, customer, address, phone, email, relation, collateral, asset, collections action, assignment, bucket, product and branch data today. SVAF appraisals, CCMS collateral detail, AMIS and RPS repossessed and purchased assets, LIT litigation and hearings, WIN proof of delivery, GL write-off postings, the COLLINS scores, the SCBPDM product holding, NLEADS credit decisions, EasyApp signature requests and Entra ID group mapping are added under RWB-ACE-001 (DL43).

The recovery module owns the case and the extension tables; ACE owns the source data. Four tiers: 22 Tier 1 ACE tables read through 16 views; 14 Tier 2 ACE tables and 12 columns, raised in RWB-ACE-001, read through 14 views; 4 Workbench extension tables keyed by ACE business keys; and 88 Workbench tables that stay. The Workbench schema is 92 tables, and the dictionary holds 122 objects and 1,366 fields in place of 108 and 1,256.

Same-day needs are named under DL06: the case transfer from EFS, a payment received and a legal event. The Workbench no longer meets them with its own feed. They depend on what ACE ingests, and the age of the data is visible on every view.

# 6. How squads merge and release

Two TechX squads and the collection squad release from one repository. Branches merge into main at least once a working day. Unfinished work sits behind a feature flag; a flag that is off returns the previous code path, so a change that fails SIT or UAT is switched off and the release goes ahead. Untested code is not merged. Each squad merges into its own module through code owners, and the ACE team owns the common module and the release decision (DL04).

# 7. Consequences

| Area | What follows |
|---|---|
| Security | Sign-in, the bank IAM, access control, audit, PII and SOC logging come from ACE |
| Staff | One case view across collection and recovery |
| Release | One release train with collection; merge ownership and flags matter (DL04) |
| Data | ACE owns the source data and the Workbench owns the case: 92 tables and 30 views, and 1,366 dictionary fields, in place of 108 tables and 1,256 fields. Source data is read through read-only views, so there is one copy of every record and no inbound load (ADR-010). The Workbench cannot start before the ACE additions land (DL43) |
| Build | Retry and compensation for automated chains are built in Spring Batch with the outbox |
| Partners | Partner access from outside the bank needs an architecture change with one to three months of lead time (DL03) |


# 8. Open points

| ID | Question | Proposed answer | Owner | Due |
|---|---|---|---|---|
| DL03 | Who raises the architecture change for partner access from outside the bank | The Workbench team or the ACE team, raised in November | K. Book with the architecture team | 29 October 2026 |
| DL04 | Who merges between squads and decides when a change holds the release | Each squad through code owners; the ACE team for the common module and the release | K. Book | 29 October 2026 |
| DL05 | Who creates the recovery module in ACE | TechX in its own package from 2 November, then the ACE team applies the boundaries | K. Pipat | 29 October 2026 |
| DL06 | Which interfaces need same-day data | Option A (daily batch through COLLINS) superseded by D-RCV-35. Same-day triggers stay named; they depend on what ACE ingests | K. Book with K. Pipat | 30 October 2026 |
| DL07 | How the ACE front end is split | One front end with a recovery folder from 2 November | K. Pipat | 31 October 2026 |
| DL37 | When code owners and the browser test runner are in place | Code owners before 2 November; browser runner before the first SIT run | K. Book | 6 November 2026 |
| DL43 | Does the ACE team accept the RWB-ACE-001 scope and its dates | Accept the 14 tables, 12 columns and 80 fields, delivered by 21 November 2026 | ACE team lead | 21 November 2026 |


# 9. Approval

| Role | Approves | Status |
|---|---|---|
| SCB CTO | The decision as a whole | To approve |
| SCB IT architecture | Sections 2 to 5 | To approve |
| ACE team lead | Sections 3, 4 and 6 | Agreed |
| TechX delivery lead | Sections 3, 4 and 6 | Agreed |
| Henka solution architect | The decision as a whole | Agreed |

