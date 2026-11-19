<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench architecture decision records

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| ID | Decision | Status | Date |
|---|---|---|---|
| ADR-001 | Build the Workbench as a module of ACE | Accepted | 27 October 2026 |
| ADR-002 | Structure ACE as a modular monolith with common, collection and recovery modules | Accepted | 27 October 2026 |
| ADR-003 | Run the case workflow in code, in CMMN 1.1 terms, with no workflow engine | Superseded by ADR-011 | 27 October 2026 |
| ADR-004 | Hold every rule as versioned data and evaluate it with a decision table component | Superseded by ADR-012 | 20 October 2026 |
| ADR-005 | Take data through COLLINS and file loads, and call no system of record directly | Superseded by ADR-010 | 27 October 2026 |
| ADR-006 | One ACE front end with a recovery module folder | Proposed | 28 October 2026 |
| ADR-007 | Build the document hub in the Workbench as the system of record for recovery documents | Accepted | 26 October 2026 |
| ADR-008 | Trunk based development with feature flags | Accepted | 27 October 2026 |
| ADR-009 | An append-only, hash-chained decision log that blocks an action it cannot record | Proposed | 28 October 2026 |
| ADR-010 | Read source data from the ACE database through read-only views | Accepted | 15 November 2026 |
| ADR-011 | Run case workflows on Temporal, with case data in the ACE database | Accepted | 16 November 2026 |
| ADR-012 | Evaluate rules with embedded Drools from versioned rule packages | Accepted | 16 November 2026 |

---

## ADR-001 Build the Workbench as a module of ACE

- Status: Accepted
- Date: 27 October 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: DT07

### Context and problem

Recovery needs a case system from day 90 to close. ACE is the bank's collection engine and already runs sign-in, access control, audit and personal data logging, a case view and the restructure calculator. Building recovery as a separate application would give staff who work both collection and recovery two systems and two case views, and the bank two platforms to run.

### Decision drivers

- One case view for collection and recovery staff
- Reuse of what ACE already runs in production
- No integration cost between collection and recovery
- One platform for SCB IT to operate and secure

### Options considered

1. A module of ACE: one service, one repository, one front end
2. A separate recovery application on the ACE infrastructure pattern
3. A separate recovery application on its own platform

### Decision

Option 1. The Workbench is the recovery module of ACE.

### Consequences

- Good: sign-in, the bank IAM, access control, audit, PII and SOC logging come from ACE.
- Good: one case view across collection and recovery.
- Good: recovery takes ACE's data position, which is now an asset rather than a constraint: one copy of the source data, ingested by ACE and read through read-only views (ADR-010).
- Bad: the recovery and collection squads share one repository and one release, so merge ownership and release discipline matter (ADR-008, DL04).

---

## ADR-002 Structure ACE as a modular monolith

- Status: Accepted
- Date: 27 October 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: DT08; module creation DL05

### Context and problem

Three teams build in one service: the ACE team, the collection squad and the TechX recovery squads. Without boundaries, a change in one team's code breaks another's, and the service becomes hard to change.

### Decision drivers

- Squads can change their own module without coordinating every change
- One deployable service
- Boundaries that are checked, not agreed

### Options considered

1. Modular monolith: common, collection and recovery modules by folder, boundaries checked at build time
2. Separate services per team
3. One codebase with no module boundaries

### Decision

Option 1. Each module owns its tables and is reached only through its published interface or an application event. A boundary test fails the build on any violation.

### Consequences

- Good: one deployment and one database, with clear ownership of code and tables.
- Good: a recovery component the collection module needs can move to the common module by agreement.
- Bad: the boundary test and code owners must be in place before the squads start (DL37).

---

## ADR-003 Run the case workflow in code, with no workflow engine

Superseded by ADR-011 on 16 November 2026. The Workbench runs the case lifecycle on Temporal from Epic 3, and case data stays in the ACE database recovery schema. This section is kept as the record of what was decided on 27 October 2026.

- Status: Superseded by ADR-011
- Date: 27 October 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: DT09, DT10

### Context and problem

A recovery case lives for months or years and mostly waits on people, partners and courts. 366 of the 448 routing rules move a case to a state that a person or a partner owns. The case model has 10 stages, 30 milestones, 150 tasks, 53 event listeners and 448 sentries. The question is whether a workflow engine such as Temporal holds the case, or the case is held as data and moved by code.

### Decision drivers

- Long human waits, which a workflow engine holds poorly
- Cases that outlive several releases, so in-flight versioning matters
- One case language shared with the collection module
- Skills the ACE team and TechX already have

### Options considered

1. Case state as rows in the ACE database, moved by code, timers on Quartz, automated chains on Spring Batch with an outbox
2. Temporal, with one workflow execution per case
3. A commercial case management engine

### Decision

Option 1. The case is modeled in CMMN 1.1 terms. Case, stage, task and timer state are rows. A wait of weeks is a row with a state and a stored due date. Temporal is not used; adding it later for a self-contained automation task needs its own decision record.

### Consequences

- Good: no extra runtime for SCB to operate; a change to a handler is an ordinary release; state does not replay.
- Good: case terms mean the same in both modules.
- Bad: retry and compensation for automated chains are built with Spring Batch and an outbox.

---

## ADR-004 Hold every rule as versioned data

Superseded by ADR-012 on 16 November 2026. Rules are still versioned data, now authored as Drools XLS decision-table workbooks and evaluated by embedded Drools. This section is kept as the record of what was decided on 20 October 2026.

- Status: Superseded by ADR-012
- Date: 20 October 2026
- Deciders: SCB core team with Henka
- Decision log: DT02; Epic 1 rule scope DL24

### Context and problem

Thresholds, limits, routes, timers and templates change often. If they are written in code, every change needs a release, and the business waits a month to move a number. ACE has rule based logic in code and no rules engine.

### Decision drivers

- A business change without a code release
- An audit trail of which rule version decided each case
- Open cases kept on the version they were decided under

### Options considered

1. Rules as versioned rows, evaluated by a decision table component in the recovery module
2. A commercial or open source rules engine
3. Rules in Java code

### Decision

Option 1. Every rule, limit, threshold, template, name, queue, role, timer and route is a data row with a version, valid from and valid to dates, an approver and a test case, changed through a validated load. Each route set is a decision table with hit policy Unique. Code holds the behavior; data holds the choices.

### Consequences

- Good: a threshold moves on its effective date with no release, and rolls back the same way.
- Good: the decision log records the rule ID and version for every move.
- Bad: the evaluator, the load checks and the rule table tests are built by the squads.

---

## ADR-005 Take data through COLLINS and file loads

Superseded by ADR-010 on 15 November 2026. The Workbench no longer loads source data: ACE ingests it, and the recovery module reads it through read-only `recovery.v_ace_*` views. This section is kept as the record of what was decided on 27 October 2026.

- Status: Superseded by ADR-010
- Date: 27 October 2026
- Deciders: SCB IT and the ACE team
- Decision log: DT12; real-time needs DL06; legacy scope DL12

### Context and problem

The Workbench needs account, customer, collections, litigation, collateral, valuation and asset data. ACE takes its data through COLLINS by end of day batch. Collateral, appraisals and assets are not in COLLINS today.

### Decision drivers

- One way in for data, with checks
- No new direct interfaces to legacy systems
- A known age for every input to a decision

### Options considered

1. COLLINS daily batch, plus file loads for sources COLLINS does not carry
2. Direct real-time interfaces to each system of record
3. Events for every source

### Decision

Option 1. No component calls a system of record directly. Each load is checked for business date, structure, control totals, keys and references, and is refused whole if it fails. Every loaded record carries its business date.

### Consequences

- Good: one path in, one set of checks, no legacy enhancement.
- Bad: decisions use end of day data, and collateral, appraisals and assets arrive weekly or monthly. Same-day needs are named under DL06.

---

## ADR-006 One ACE front end with a recovery module folder

- Status: Proposed
- Date: 28 October 2026
- Deciders: the ACE team
- Decision log: DL07

### Context and problem

ACE has one React front end. The recovery screens can live in a module folder of that front end, or the front end can be split into a workspace of modules.

### Decision drivers

- Squads work from 2 November
- One look and one sign-in for staff
- Types generated from the back end

### Options considered

1. One ACE front end with a recovery module folder
2. A workspace of front end modules with NX
3. A separate recovery front end

### Decision

Option 1 from 2 November. A move to option 2 is the ACE team's choice and does not change the recovery screens.

### Consequences

- Good: no wait for a front end restructure.
- Bad: code owners per folder are needed to keep squads out of each other's screens (DL37).

---

## ADR-007 Build the document hub in the Workbench

- Status: Accepted
- Date: 26 October 2026
- Deciders: CTO
- Decision log: DT06; storage pattern DL27; document types DL19

### Context and problem

Recovery runs on documents: contracts, notices, proofs of delivery, court papers, appraisals and titles. The choice was to index documents held in another store or to hold them in the Workbench.

### Decision drivers

- Documents found by case, type and date without manual filing
- Legal documents that cannot be altered
- Custody of originals tracked

### Options considered

1. A document hub built in the Workbench as the system of record
2. An index over an existing document store

### Decision

Option 1. Documents are stored in Blob storage with a write-once container for legal types, indexed by case, type, date and extracted fields, with retention classes and custody tracking.

### Consequences

- Good: one place for every recovery document, linked to its case.
- Bad: storage, backup, legal hold and e-discovery are in scope (DL27).

---

## ADR-008 Trunk based development with feature flags

- Status: Accepted
- Date: 27 October 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: DT11; merge owner DL04

### Context and problem

Two squads release monthly from one repository. One squad's unfinished or failed change must not hold the other's release.

### Options considered

1. Trunk based development with short branches and feature flags
2. Long-lived squad branches merged before each release

### Decision

Option 1. Branches merge into main at least once a working day. Unfinished work is behind a flag. A flag that is off returns the previous code path. Untested code is not merged.

### Consequences

- Good: a change that fails SIT or UAT is switched off and the release goes ahead.
- Bad: flags must be listed, owned and removed after release.

---

## ADR-009 An append-only decision log that blocks an action it cannot record

- Status: Proposed
- Date: 28 October 2026
- Deciders: the solution architect with Risk and Internal Audit

### Context and problem

Every recovery decision must be traceable for audit, testing and learning: the inputs, the rule and model versions, the recommendation, the approver, the actions and the outcome.

### Options considered

1. An append-only, hash-chained log in the ACE database, written before the action, with a failed write blocking the action
2. Application logs searched after the event

### Decision

Option 1. A correction is a further entry naming the original. Analysis reads a copy in the data lake, not the live log.

### Consequences

- Good: an auditor can test that every action carries a rule version and an approver.
- Bad: the decision log write is in the path of every action and must be fast and available. Retention is set by Compliance (DL26).

---

## ADR-010 Read source data from the ACE database through read-only views

- Status: Accepted
- Date: 15 November 2026
- Deciders: the recovery tech lead with the data architect; the ACE team lead for RWB-ACE-001 and DL43
- Decision log: D-RCV-35 (U1 to U4); supersedes ADR-005

### Context and problem

The design built a second copy of account, customer, payment, party, contact, collateral, valuation, asset, collections, product and score data in the recovery schema, and filled it with eleven copy tables and nine load tables. ACE already ingests those records and owns them. Two copies of one account row disagree over time, and the Workbench maintains the copy that nothing else reads. The question is where source data lives and how the recovery module reaches it.

### Decision drivers

- One copy of source data, held by the team that already ingests it
- No inbound interface or second load estate for the Workbench to build and run
- A boundary the database enforces, not only code review
- Case history that a change in a source system cannot delete

### Options considered

1. Read source data from the ACE database through `recovery.v_ace_*` views, SELECT only
2. Keep the copy tables in the recovery schema and load them (ADR-005)
3. Read the ACE `public` tables directly from the recovery module

### Decision

Option 1. The recovery module reads source data from the ACE database through `recovery.v_ace_*` views. It does not load, copy or transform source data. The views are SELECT only and owned by a dedicated role that holds SELECT on the ACE tables; the recovery service identity holds SELECT on the views and on nothing else, so a direct read of a `public` table fails in the catalog.

- 30 views in two migrations: 16 over ACE tables that exist today, shipped with RWB-E1-069 as the next free sequence after the V0001 baseline; 14 over the Tier 2 additions, shipped the week RWB-ACE-001 lands. Until then the features that need them stay behind their flags.
- The ACE team owns every table and column the views read, raised once in RWB-ACE-001. The Workbench owns only its four extension tables, keyed by ACE business keys.
- No foreign key from a `recovery` table into `public`, because ACE uses ON DELETE CASCADE on `account`. A link to a source record is a business-key column with no foreign key.

### Consequences

- Good: one copy of source data. There is no Workbench copy to reconcile, correct or retire.
- Good: no inbound load, data quality or tracker estate to build and run; 20 tables leave the schema.
- Good: the view list is the contract between the two teams, so a change to a source column is an ACE change with a named owner.
- Bad: the Workbench cannot start before the ACE additions land (DL43).
- Bad: there is no tokenization at load, so masking moves into the views and to E1-037 at the API, and every read of personal data is audited.
- Bad: a view that reads a changed ACE column breaks at deploy, so the view conformance test runs in the pipeline.

---

## ADR-011 Run case workflows on Temporal, with case data in the ACE database

- Status: Accepted
- Date: 16 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-36; supersedes ADR-003

### Context and problem

A recovery case lives for months or years and mostly waits on people, partners and courts. 366 of the 448 routing rules move a case to a state that a person or a partner owns. The case model has 10 stages, 30 milestones, 150 tasks, 53 event listeners and 448 sentries.

ADR-003 held case, stage, task and timer state as rows and moved it with code. The waits, retries and automated chains are built by hand: rows in `timer`, JOB-05 to check them, Spring Batch chains and an outbox. Each of those is code the squads maintain, and a case that waits six months is a row someone must keep sweeping. The question is whether a workflow engine runs the case lifecycle, and where the case of record lives.

### Decision drivers

- Timers that fire once, months later, across a deploy, a restart and an upgrade
- Retries and compensation for multi-step automated chains without hand-built Batch and outbox code
- A case of record that no workflow history can delete or contradict
- A platform SCB IT can run inside ACE, on the ACE AKS clusters, with the ACE sign-in, audit and personal data controls
- Cases in flight that survive a change to workflow code
- One case language shared with the collection module (DT10)

### Options considered

1. Temporal, hybrid: Temporal runs the case lifecycle, and case data stays in the ACE database recovery schema
2. Temporal holding the case state in its own persistence
3. Keep the code approach: case state as rows, Quartz timers, Spring Batch chains and an outbox (ADR-003)

### Decision

Option 1. Temporal runs the case lifecycle from Epic 3, one workflow per case, with the workflow ID `case-{caseId}`. Durable timers, retries and automated multi-step chains are workflow and activity behaviour. The clusters are self-hosted on the shared ACE AKS clusters in the ACE namespace: one cluster per environment (DEV, SIT, UAT, PROD), deployed with the official Temporal Helm chart, on the pinned release SCB IT approves at build.

- Case data stays the system of record in the ACE database recovery schema. Temporal holds no case of record. A workflow history can expire or be archived without losing a case, and the case record view, the decision log and the reports read the rows they read today.
- The engine's own tables (`temporal`, `temporal_visibility`) are outside the Physical Schema, owned by role `temporal_svc`, and have no grant on the ACE database. `recovery_svc` has no grant on the Temporal databases.
- Namespace `rwb-recovery` per cluster. Task queues `rwb-case` for case workflows, `rwb-integration` for multi-step outbound chains and `rwb-platform` for smoke and health workflows.
- Search attributes are `CaseId`, `Stage`, `ProductGroup` and `QueueCode`, all Keyword and none personal. Payloads are encrypted by `PdpaPayloadCodec`, so history holds no clear personal data. Closed workflows are retained 30 days and archived to Blob in E2-039.
- The Web UI sits behind Entra ID OIDC: RW-PLATADM operate, RW-AUDIT read, RW-SECADM decode through the codec server on a break-glass session. mTLS runs between worker, frontend and internal services.
- Quartz and Spring Batch keep every Epic 1 and Epic 2 job. JOB-05 runs behind the `TimerScheduler` port, so Epic 3 swaps in a Temporal implementation without changing a caller (T2). Temporal Schedules are not used in Epics 1 and 2.
- Workflow code is deterministic. Clock, random and I/O live in activities only. The worker polls through the Spring Boot starter under `SY-CASEWF`, and the feature flag `rwb.p3.temporal` starts or stops it.

### Consequences

- Good: durable timers, retries and multi-step chains replace hand-built timer, Batch and outbox machinery for the case lifecycle.
- Good: the case of record stays in the recovery schema, where the case engine, the decision log and the reports already read it.
- Good: one workflow per case gives replay, visibility and a stuck-workflow signal that a timer table cannot give.
- Good: the platform is a Helm release on clusters SCB IT already runs, with the ACE namespace, sign-in and audit controls.
- Good: the `TimerScheduler` port lets Epic 3 replace the Quartz implementation without a caller change, so Epics 1 and 2 are not blocked on the engine.
- Bad: SCB IT takes a new operational load: cluster operations, server and SDK upgrades, backup and restore of two databases, certificate rotation and on-call for four environments.
- Bad: the Epic 1 date is under pressure. The platform (E1-070) and the worker (E1-071) land in Epic 1 before the first case workflow in Epic 3, so Epic 1 carries the platform cost and the date risk without the case benefit.
- Bad: workflow code must be deterministic and versioned. A change is gated by the replay test (E2-040), old builds finish old workflows, and a non-deterministic change is a release defect, not a code review comment.
- Bad: two persistence estates with their own backup, restore, access and monitoring paths, and a second place a personal data incident can start.

---

## ADR-012 Evaluate rules with embedded Drools from versioned rule packages

- Status: Accepted
- Date: 16 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-36; supersedes ADR-004

### Context and problem

Thresholds, limits, routes, timers and templates change often. If they are written in code, every change needs a release, and the business waits a month to move a number. ADR-004 held every rule as a versioned row, evaluated by a decision-table component built in the recovery module. That component is code the squads maintain: the parser, the checks, the test runner, the dry run and the rollback. Each new shape of condition or output is a change to it, and a rule author is limited to the shapes the component was built for.

Drools is approved as an embedded library. The question is how rules are authored, evaluated and versioned, and whether a rules engine runs beside the Workbench or inside it.

### Decision drivers

- A business change without a code release
- An audit trail of which rule version decided each case
- Open cases kept on the version they were decided under
- One evaluator for the engines, the tests and the dry run, so a passed test means the same result in production
- No new server to operate and no new release path
- Rules as versioned data, the principle ADR-004 set

### Options considered

1. Embedded Drools, with XLS decision-table workbooks held as versioned data in the database
2. Drools rules shipped as code, built into the release
3. A separate KIE server or Business Central, with KJARs deployed to it

### Decision

Option 1. Drools is embedded in the recovery module with the KIE runtime libraries only: `drools-engine`, `drools-mvel`, `drools-decisiontables` and `drools-xml-support`. There is no KIE Server, no Business Central and no KJAR in Maven.

- RW-COE authors each package as an Excel workbook in Drools XLS decision-table format. On upload the workbook is compiled to a KieBase, checked, and run against its scenarios and a dry run. It is stored as a `rule_package_version` row with the workbook in Blob, the generated DRL and a checksum.
- RW-RISK approves. The author cannot approve. The version is in force from its valid-from date, and rollback is one call. A rule change needs no release.
- First match is kept. Each decision table has RuleSet = package code, each row is a rule whose NAME is the rule ID, rows share one activation-group, and salience follows row order, so exactly one row decides. The default row is last.
- `rule_row` stays as the rule catalog: the parsed, queryable copy of each row, linked to its package version, with `outputs` jsonb. Stories read action text, owner role, timer spec and target queue from the catalog by rule ID and version, not from the package source.
- Evaluation happens only inside a Temporal activity from Epic 3. The package version is chosen at evaluation time, returned in the `RuleResult` and written to the decision log. `decision_log_entry.rule_id` and `rule_version` keep their columns and now carry the Drools rule name and the package version label.
- `payment_match_rule` is dropped. Payment matching is package PAYMENT_MATCH, with match type, tolerance, window, grace and partial floor as decision-table columns.
- The R-UNI-xx rules that Epic 1 cites stay coded and are cited by ID in Phase 1. They move into a UNIVERSAL package in Epic 3.

### Consequences

- Good: a threshold, route or timer moves on its effective date with no release, and rolls back the same way.
- Good: the decision log records the rule ID and the package version for every move, in the columns that already exist.
- Good: one evaluator serves the engines, the scenarios, the dry run and the build gate, so a scenario that passes proves the production path.
- Good: rules stay versioned data, which is ADR-004's principle, now with a standard authoring format and a compiler that checks it.
- Good: no KIE Server, no Business Central and no KJAR to operate or deploy. The engine is a library in the same service.
- Bad: RW-COE must be trained in XLS decision-table authoring: RuleSet and RuleTable rows, condition and action columns, salience from row order, the default row and the Tests tab. The template reduces the risk but does not remove the skill change.
- Bad: the Drools library is a dependency the squads must upgrade: a pinned version per release, a compatibility check against `drl_source` in every stored package, and a regression run of every in-force package's scenarios on every build.
- Bad: a package that compiles can still be wrong. The checks and the scenarios catch less than a code review, so the dry run over open cases and the Risk approval carry more weight.
- Bad: the package store, the checksum and the Blob reference are new data the Workbench owns, and a corrupt or missing DRL refuses the version at load into the cache until it is fixed.
