SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench architecture decision records

## Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench architecture decision records |
| Version | 4 |
| Status | Draft |
| Date | 16 November 2026 |
| Owner | Solution architect |
| Decision | D-RCV-60 |
| Change | v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

## Index

| ID | Decision | Status | Date |
|---|---|---|---|
| ADR-001 | Build the Workbench as a module of ACE | Accepted | 27 October 2026 |
| ADR-002 | Structure ACE as a modular monolith with common, collection and recovery modules | Superseded by ADR-013 | 27 October 2026 |
| ADR-003 | Run the case workflow in code, in CMMN 1.1 terms, with no workflow engine | Superseded by ADR-011 | 27 October 2026 |
| ADR-004 | Hold every rule as versioned data and evaluate it with a decision table component | Superseded by ADR-012 | 20 October 2026 |
| ADR-005 | Take data through COLLINS and file loads, and call no system of record directly | Superseded by ADR-010 | 27 October 2026 |
| ADR-006 | One ACE front end with a recovery module folder | Proposed | 28 October 2026 |
| ADR-007 | Build the document hub in the Workbench as the system of record for recovery documents | Accepted | 26 October 2026 |
| ADR-008 | Trunk based development with feature flags | Accepted | 27 October 2026 |
| ADR-009 | An append-only, hash-chained decision log that blocks an action it cannot record | Superseded by ADR-022 | 28 October 2026 |
| ADR-010 | Read source data from the ACE database through read-only views | Accepted | 15 November 2026 |
| ADR-011 | Run case workflows on Temporal, with case data in the ACE database | Accepted | 16 November 2026 |
| ADR-012 | Evaluate rules with embedded Drools from versioned rule packages | Accepted | 16 November 2026 |
| ADR-013 | Run Recovery as 19 services inside ACE | Proposed | 22 November 2026 |
| ADR-014 | One schema and one login per service in the ACE PostgreSQL database | Proposed | 22 November 2026 |
| ADR-015 | Kafka business-event topics with outbox, inbox and CloudEvents | Proposed | 22 November 2026 |
| ADR-016 | A reusable Temporal layer, and Temporal Schedules in place of Quartz | Proposed | 22 November 2026 |
| ADR-017 | Embedded Drools in each service, with the rule registry in rwb-decision | Proposed | 22 November 2026 |
| ADR-018 | No data lake; rwb-reporting builds its read model from events | Proposed | 22 November 2026 |
| ADR-019 | Edge: gateway-bff for staff and a partner gateway for partners | Proposed | 22 November 2026 |
| ADR-020 | Contract-first REST, one hop, 2 second timeout | Proposed | 22 November 2026 |
| ADR-021 | Per-service Flyway and migration ownership | Proposed | 22 November 2026 |
| ADR-022 | A local decision record plus a central ledger | Proposed | 22 November 2026 |
| ADR-023 | Observability per service | Proposed | 22 November 2026 |

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

Superseded by ADR-013 on 22 November 2026. Recovery stays inside ACE, and recovery-core is split along its module lines into 19 services, one per module P1–P10 and S1–S9, each with its own schema, login, topic, task queue and release (ADR-013, ADR-014). This section is kept as the record of what was decided on 27 October 2026.

- Status: Superseded by ADR-013
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

Superseded by ADR-022 on 22 November 2026. Each service writes the decision record in its own schema in the same transaction as the state change, hash-linked to the previous record, and publishes it to `rwb.decision-record.v1`; rwb-decision collects it into the central ledger, and only irreversible steps wait for the ledger acknowledgement. This section is kept as the record of what was decided on 28 October 2026.

- Status: Superseded by ADR-022
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

Amended by ADR-016 on 22 November 2026: the Temporal layer is shared with ACE in five layers under a versioned workflow kit, one task queue per service replaces the three fixed queues, the case is a parent workflow with a child for each stage under Continue-As-New, and Temporal Schedules in the owning service replace the Quartz jobs from Epic 3. This section is kept as the record of what was decided on 16 November 2026.

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

Amended by ADR-017 on 22 November 2026: rule governance, the package versions and the registry stay central in rwb-decision (P7), and each service that owns a decision loads its own approved model and evaluates it in an activity, with no shared rule server on the hot path. This section is kept as the record of what was decided on 16 November 2026.

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

---

## ADR-013 Run Recovery as 19 services inside ACE

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-60; DL44 (adopt Architecture v5); supersedes ADR-002

### Context and problem

ADR-002 held ACE together as a modular monolith: a common module, a collection module and a recovery module in one deployable and one repository, with boundaries checked at build time. Architecture v5 keeps Recovery inside ACE but cuts recovery-core along its module lines, so that each business module becomes a service with its own release, contract, schema, topic and task queue. A capability such as the document hub, communications or the decision center can then be reused or replaced by another workbench without untangling a shared core.

The question is how many deployable units Recovery has, where they run, and what boundary replaces the module folder boundary of ADR-002.

### Decision drivers

- A capability that can be reused, released, scaled or replaced alone (Architecture v5 slides 4 and 36)
- Ownership that matches the business modules in the functional specifications, one service per module P1–P10 and S1–S9
- Failure isolation: one route service down does not stop the other routes, the case list or payments (slide 34)
- Recovery stays on the platform ACE already runs: the same AKS cluster and App Gateway, the ACE Common shared services and the ACE PostgreSQL database (slides 2, 7 and 8)
- Boundaries that are checked in the build, which is the principle ADR-002 set
- Epic 1 work already built or in build is not changed unless it must be (U2)

### Options considered

1. 19 services inside ACE, one per module, each with its own schema, login, contract, topic and task queue
2. The modular monolith of ADR-002: one deployable with common, collection and recovery modules by folder
3. 19 services on a separate recovery platform, outside ACE

### Decision

Option 1. Recovery runs as 19 services inside the ACE platform, one per module, plus the shared platform parts that are not services of the 19: gateway-bff with its Redis session, the shared Temporal layer, the Kafka business-event topics, the bank Airflow scheduler at the edges and OpenTelemetry observability.

| Code | Service | Wave |
|---|---|---|
| P1 | rwb-source-data | 1 |
| P2 | rwb-integration | 1 |
| P3 | rwb-case | 1 |
| P4 | rwb-access | 1 |
| P5 | rwb-document | 1 |
| P6 | rwb-comms | 1 |
| P7 | rwb-decision | 1 |
| P8 | rwb-payment | 2 |
| P9 | rwb-reporting | 1 |
| P10 | rwb-agent | 1 |
| S1 | rwb-valuation | 3 |
| S2 | rwb-treatment | 2 |
| S3 | rwb-guarantee | 3 |
| S4 | rwb-litigation | 3 |
| S5 | rwb-asset | 2 |
| S6 | rwb-debtsale | 3 |
| S7 | rwb-writeoff | 4 |
| S8 | rwb-deviation | 2 |
| S9 | rwb-partner | 4 |

- Each service has one short name and derives everything from it: schema `rwb_<short>`, one database login, REST base `/api/recovery/<short>/v1`, topic `rwb.<short>.events.v1` with retry and `.dlt` topics, event names `rwb.<short>.<Event>.v1`, Temporal task queue `rwb-<short>`, Java package `th.co.scb.ace.workbench.recovery.<short without hyphen>` and epic `RWB-SVC-<code>`.
- Each service is an api deployment and a worker deployment. The api tier is small and fixed at two copies; the worker tier scales with the queue backlog and may scale to zero for bursty work such as OCR and agent runs.
- The boundary is data and contract, not folder: a service writes only its own schema, reaches another service only through its published REST contract, its Kafka topic or its Temporal activity contract, and holds the other service's IDs rather than its rows. A boundary test fails the build on any cross-schema reference (ADR-014, ADR-020).
- Recovery stays a module of ACE. ADR-001 stands: the same sign-in, the same audit and PII logging, the same case view, the same restructure calculator, the same notification path, and one copy of source data read through the views of ADR-010.
- Services arrive in waves with the epics that need them: nine in Wave 1, four in Wave 2, four in Wave 3 and two in Wave 4. Nothing is built twice, and a service is created when its first epic starts.
- Epic 1 keeps what it has built or in build (U2). The split of the single recovery schema of RWB-E1-001 into the `rwb_*` schemas is new work, carried by RWB-PLT-NF06-DB and the per-service database stories, and is recorded in the Change Register.

### Consequences

- Good: a capability can be reused or replaced alone. Another workbench can call or deploy rwb-document, rwb-comms or rwb-decision without taking the rest of Recovery.
- Good: each service has its own release, contract, schema, topic and queue, so a change in one does not hold another's release.
- Good: a failure is contained. Litigation down pauses litigation; its work waits on its queue and topic offset, and the other 18 services keep running.
- Good: the module boundary of ADR-002 survives as a checked schema and contract boundary, which is stronger than a folder.
- Bad: 19 services are about 38 small deployments at rest in four environments, with one Helm chart and one pipeline template to keep the cost per service low.
- Bad: ownership and contracts become the coordination cost: 19 contracts, 19 schemas and 19 release trains, and a cross-service change is a contract change, not a code edit.
- Bad: the Epic 1 scope grows by the platform work (template, Helms, schemas, topics) before the first case workflow brings a case benefit.

---

## ADR-014 One schema and one login per service in the ACE PostgreSQL database

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka; the ACE team and the database administrator for the server, the schemas, the logins and the grants
- Decision log: D-RCV-60; DL44 (adopt Architecture v5)

### Context and problem

ADR-002 said each module owns its tables. ADR-010 said source data stays in one copy in the ACE database and is read through `recovery.v_ace_*` views. With 19 services in one database, ownership has to be enforced by something the runtime cannot bypass, or the services will couple through tables. The options are a database per service, one schema for everything, or one schema and one login per service on the ACE server.

### Decision drivers

- Ownership that the database enforces, not only code review
- No second database server for SCB IT to run, back up and approve
- ACE protected from Recovery: a connection cap and a statement timeout per login
- A schema that can move to its own server later without a code change
- The 30 views of ADR-010 kept as the one path to ACE data

### Options considered

1. One schema and one login per service in the ACE PostgreSQL database, no cross-schema access
2. A database per service
3. One schema per module group, or the single recovery schema of the monolith

### Decision

Option 1. The ACE PostgreSQL server holds the ACE schemas, the `recovery` schema with the 30 read-only views, and 19 Recovery schemas `rwb_<short>`, one login each.

- Each login owns its own schema and holds no grant on any other schema. A read or write outside its own schema fails in the catalog, not in code review.
- Only `rwb_source_data` holds SELECT on `recovery.v_ace_*`. A grant of those views to another login is refused, and the views themselves stay SELECT only (ADR-010).
- No cross-schema join, view or foreign key. A service holds the other service's IDs and asks the owner through its contract. A boundary test in every build fails on a cross-schema reference.
- Each login goes through its own PgBouncer pool with a connection cap and a statement timeout, so Recovery cannot starve ACE. Heavy reporting runs from the projections in `rwb_reporting`, not from the ACE tables.
- The Workbench keeps its four extension tables in `rwb_source_data` (party_ext, contact_point_ext, account_ext, valuation_ext). It adds no table and no column to an ACE schema; every ACE-side addition is raised once with the ACE team under RWB-ACE-001.
- Temporal keeps its persistence in its own database, with no grant either way: `temporal_svc` has no grant on the ACE database and `recovery_svc` has no grant on the Temporal databases.
- The physical schema is delivered per service: 19 `rwb_<name>.sql` files plus `recovery_views.sql` and a README, so each service's DDL and its Flyway sequence are the same artefact.

### Consequences

- Good: ownership is enforced by grants. A service cannot read another service's tables even by mistake.
- Good: one server to run, back up and approve, which is the position ADR-010 already took.
- Good: a busy service is capped at its own pool, so a runaway report cannot slow ACE or the other services.
- Good: a schema can move to its own server later by changing its connection string, with no code change.
- Bad: 19 logins, 19 schemas and 19 migration sequences are configuration to keep in step across four environments.
- Bad: there is no referential integrity across services. An orphan ID is a data-quality incident and a reconciliation job, not a foreign key error.
- Bad: the connection budget has to be added up per environment and reviewed, because the caps multiply by 19 services and their worker pools.

---

## ADR-015 Kafka business-event topics with outbox, inbox and CloudEvents

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka; Enterprise Architecture and the ACE platform team for the Kafka platform
- Decision log: D-RCV-60; DL44 (adopt Architecture v5)

### Context and problem

The Workbench writes an outbox in the same transaction as its change, but there is no event bus: the outbox is delivered to consumers inside one deployable. With 19 services, a fact one service records has to reach the services that react to it, and each of them has to be able to rebuild its own view from history. The options are the bank Kafka platform that ACE already runs for PII logging, a managed Azure equivalent, or no broker.

### Decision drivers

- A fact that many services react to, without the producer knowing them
- Order per case, so a case's events arrive in the order they were written
- Replay, so a new or repurposed service rebuilds its view from history
- No new platform and no new outsourcing assessment where possible (FPG 19/2559 context)
- Personal data kept out of events (PDPA)

### Options considered

1. Apache Kafka on the bank platform ACE already runs, with dedicated Recovery topics and ACLs; Azure Event Hubs Premium through its Kafka endpoint as the fallback
2. Azure Service Bus Premium
3. No broker: the outbox and in-process application events only

### Decision

Option 1. Recovery has its own business-event topics on the Kafka platform ACE already uses, separate from the PII logging topics and with their own ACLs, quotas and schema subjects.

- One topic per service, `rwb.<short>.events.v1`, with retry topics at 1 minute, 10 minutes and 1 hour, then a `.dlt` topic with an alert and a replay tool.
- 12 partitions, replication factor 3, 7-day retention, record key `caseId`, so one case's events keep their order. One consumer group per service.
- Envelope is CloudEvents 1.0 in Kafka binary mode (`ce_*` headers) with a W3C `traceparent` header. Payloads are JSON, validated against a JSON Schema registry with BACKWARD compatibility, and described by an AsyncAPI 3.0 document per topic.
- The producer writes the event to its own outbox in the same transaction as the state change; the outbox relay publishes with an idempotent producer and `acks=all`, and marks it sent (JOB-11). If Kafka is unavailable, events wait in the outbox and nothing is lost.
- Each consumer records `ce_id` in its own inbox table `processed_event`, in the same transaction as its own change, so a redelivered event has no second effect.
- Events carry IDs and business facts only, never personal data. A consumer that needs personal data asks the owning service through its contract.
- The shared topic `rwb.decision-record.v1` carries DecisionRecorded from all 19 services to rwb-decision (ADR-022). It is the one topic not owned by a single service.
- Events announce facts; they are not commands. A step another service must perform is a Temporal activity or child workflow (ADR-016), and a person waiting for an answer is REST (ADR-020).
- `rwb-case` does not act on an event directly: its case router turns the event into a signal on the CaseWorkflow.

### Consequences

- Good: the producer does not know its consumers, so a new listener is a new consumer group and no producer change.
- Good: replay lets a service rebuild its view, which is what makes a service reusable and replaceable.
- Good: ACE already operates Kafka, so the platform and the outsourcing position are known, and the same client code runs on Event Hubs if the bank needs it.
- Bad: an event estate is new operational surface: topic ACLs, schema subjects, consumer lag, retry and dead-letter handling, and a replay tool.
- Bad: the effect is eventually consistent. A screen that must show the consequence of an event reads the consumer's own projection and accepts the delay.
- Bad: the platform decision is not yet confirmed by Enterprise Architecture and the ACE platform team (GAP-0092). Until it is, the outbox holds the events and the topics stay unbuilt.

---

## ADR-016 A reusable Temporal layer, and Temporal Schedules in place of Quartz

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka; the platform team for the Temporal cluster and the workflow kit
- Decision log: D-RCV-60; DL44 (adopt Architecture v5); amends ADR-011

### Context and problem

ADR-011 accepted Temporal, self-hosted, one cluster per environment, one workflow per case with the ID `case-{caseId}`, three task queues and one namespace, with Quartz and Spring Batch keeping every Epic 1 and Epic 2 job behind the `TimerScheduler` port. Architecture v5 redraws the same engine as a platform that another workbench can reuse: one cluster per environment shared with ACE, a namespace per workbench, a versioned workflow kit, one task queue per service, and a case that is a parent workflow with a child per stage. It also moves scheduled work off the shared Quartz tables and into a Temporal Schedule in the owning service, with the bank Airflow scheduler at the edges.

The question is what is owned once by the platform and what each service team owns, and where scheduled work runs.

### Decision drivers

- A layer another workbench can reuse in four steps: a namespace, the kit, the existing service contracts, and only its own domain workflows
- One queue per service, so a service is reusable through its queue and contract, not its code
- Cases that run for years without hitting the history limit
- A schedule in the service that owns the job, rather than a shared job table
- Epic 1 and Epic 2 not blocked on the engine (T2)

### Options considered

1. A five-layer Temporal platform: cluster, namespaces, workflow kit and activity contracts owned once by the platform team, domain workflows owned by each service team; Schedules in the owning service
2. One cluster and one namespace per service, as ADR-011 shaped it for a single deployable
3. Keep Quartz and Spring Batch for scheduled work, with Temporal only for the case lifecycle

### Decision

Option 1. Temporal is a platform in five layers. Recovery owns the top two, the platform team owns the rest.

- L1 cluster: one per environment on the ACE AKS cluster, with its own persistence database, UI, metrics and codec server. Version 1.30 or later, because Nexus and Worker Versioning are needed, on the pinned release SCB IT approves at build.
- L2 namespaces: `ace-collection` for ACE and `rwb-recovery` for Recovery, and a namespace per workbench after that. Each namespace has its own retention, quotas, certificates and codec keys. A new workbench is a new namespace, not a new cluster.
- L3 workflow kit: a versioned library of generic templates with no business terms in their interfaces — Approval with maker-checker and the delegation-of-authority lookup as a parameter, Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job and Partner instruction. Owned by the platform team, semantic versioning, and ACE can use it too.
- L4 activity contracts: every service publishes a contract jar with typed activity interfaces on its own queue `rwb-<short>`, plus Nexus endpoints for callers in another namespace, such as `restructure.calculate` in `ace-collection`.
- L5 domain workflows: CaseWorkflow in rwb-case and the stage workflows in the services that own them — RouteDecisionWorkflow, TreatmentWorkflow, GuaranteeClaimWorkflow, LitigationWorkflow, AssetDisposalWorkflow, DebtSaleWorkflow, WriteOffWorkflow, DeviationWorkflow and DocumentIntakeWorkflow, with ApprovalWorkflow, NoticeDispatchWorkflow, InstructionWorkflow, AgentRunWorkflow and PlatformSmokeWorkflow built from the kit template and owned by the service that runs them.
- One workflow per case, `CaseWorkflow`, with workflow ID `case-{caseId}` as the parent from entry to closure, and one child workflow per stage started on the owner's queue. Children use parent close policy ABANDON, so a stage survives the parent's Continue-As-New.
- Continue-As-New at every stage end and at least every 28 days, which keeps a run far below the history limit of 51,200 events or 50 MB.
- Workflow code is deterministic: clock, random and I/O live in activities only. Payloads pass through the codec (AES-GCM, keys in Key Vault per namespace), and the codec server lets authorised staff read payloads in the UI. Worker Versioning is used for safe upgrades.
- Workers run in each service's worker deployment, poll only their own queue and are scaled by KEDA on backlog, down to zero for bursty work. The stuck-workflow scan (JOB-21) and the daily smoke workflow (JOB-22) run on the platform.
- Scheduled work moves to a Temporal Schedule in the service that owns the job, with overlap policy SKIP and a catch-up window: rule promotion at 00:01 (JOB-20), measures at 01:30 (JOB-15), hash-chain check at 02:00 (JOB-14), smoke workflow at 06:00 (JOB-22), rebalancing at 06:30 (JOB-06), write-off scan on the third working day (JOB-16), retention on the first Sunday (JOB-17), the access review list (JOB-18) and re-appraisal (JOB-19). The ACE shared Quartz tables are no longer used by Recovery, JOB-05 and TimerDue retire, and the `timer` row stays only as the screen projection behind the timers tab, with the clock itself a durable Temporal timer in CaseWorkflow.
- The bank Airflow scheduler sits at the edges, not inside Recovery: it runs the ACE ingestion DAG, tells rwb-source-data the business date is ready (POST /v1/business-days/{date}/ready, answered 202 and idempotent on the date), opens the WIN and debt-buyer file windows, triggers report extracts and runs one-off bulk work. It calls service APIs only and never reads or writes an `rwb_*` schema. While ACE ingestion is still on Control-M, rwb-source-data polls the ACE batch record as the fallback.
- Epics 1 and 2 keep Quartz and Spring Batch behind the `TimerScheduler` port and the feature flag `rwb.p3.temporal`, as ADR-011 recorded (T2). The Schedules above are the target from the epic in which the owning service lands.

### Consequences

- Good: the bottom four layers are owned and paid for once, so a new workbench gets a namespace and the kit and writes only its own domain workflows.
- Good: one queue per service makes a service reusable through its contract, and a stage scales and releases with the service that owns it.
- Good: Continue-As-New and ABANDON let a case run for years across stages, restarts, deploys and upgrades.
- Good: a schedule lives next to the job it runs, so there is no shared job table and no cross-service job ownership.
- Good: Epics 1 and 2 are not blocked on the engine, because the port and the flag stay as ADR-011 set them.
- Bad: the platform team owns cluster operations, four environments, server and SDK upgrades, certificate rotation, the kit's semantic versioning and on-call, which is a standing cost for the platform and not for one project.
- Bad: upgrading to 1.30 or later is a Wave 0 prerequisite, because Nexus and Worker Versioning do not exist on 1.28.1 (GAP-0091).
- Bad: every service team must keep its workflow code deterministic and versioned, and a non-deterministic change is a release defect gated by the replay test.
- Bad: the bank Airflow position and the ownership of the DAGs are still to agree, so the edge of the design carries an open point.

---

## ADR-017 Embedded Drools in each service, with the rule registry in rwb-decision

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-60; DL44 (adopt Architecture v5); amends D-RCV-36 T1 and T2; amends ADR-012

### Context and problem

ADR-012 embedded Drools in the recovery module, held every package as a `rule_package_version` row with its workbook, generated DRL and checksum, kept `rule_row` as the queryable catalog, and evaluated only inside a Temporal activity. That fits one deployable. With 19 services, a rule model has exactly one owning service, and every other service needs the same governance without a shared rule server on a hot path.

The amendment to T1 and T2 of D-RCV-36 is recorded here by reference to the mapping in Template and Rules §R8.4; the Change Register text itself is Not specified in the source documents (GAP-0090; ASM-0152).

### Decision drivers

- Governance in one place: authoring, tests, four-eyes approval, effective dating and the audit of every version
- Evaluation in the service that owns the decision, inside its activity, under 300 ms
- No shared rule server on the hot path, and no second release path for a rule change
- Every answer names the rule and the model version that produced it
- A service that cannot load a new model keeps the last good one

### Options considered

1. Governance central in rwb-decision (P7), an embedded Drools engine in each owning service, and a local copy of the approved model
2. A central rules service that every decision calls over REST or Temporal
3. Rules compiled into each service's release

### Decision

Option 1. Drools stays embedded, with the KIE runtime libraries only (`drools-engine`, `drools-mvel`, `drools-decisiontables`, `drools-xml-support`); there is no KIE Server, no Business Central and no KJAR in Maven. Governance is central in rwb-decision; evaluation is local in the one service that owns the model.

- rwb-decision owns the registry: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case`, with the workbook in Blob, the generated DRL, the SHA-256 checksum, the valid-from date and the approver. RW-COE authors, RW-RISK approves, and the author cannot approve.
- A version is checked on upload: compile, schema, overlap, unreachable row, default row, at least 50 scenarios and a dry run. A version that fails is refused whole. Version states are LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED.
- JOB-20, a Temporal Schedule in rwb-decision, promotes a version at 00:01 and publishes RulePackageInForce on `rwb.decision.events.v1`. Each owning service fetches the model, verifies the checksum, swaps it in atomically and keeps the last good model if the new one fails to load. The KieBase cache holds one entry per package version, capped at 20, and is never recompiled per call. Rollback is one call.
- Evaluation happens only inside an activity of the owning service — `EvaluateRules` and `RecordAndApply` in its L4 contract — never in workflow code, so workflows stay deterministic and a replay reuses the recorded result.
- First match decides. RuleSet is the package code, each row is a rule whose NAME is the rule ID, rows share one activation-group, salience follows row order, and the default row is last. The `RuleResult` carries the package code, the package version, the rule ID and its outputs.
- `rule_row` stays the parsed, queryable catalog that stories read action text, owner role, timer spec and target queue from, by rule ID and version. A story never parses the workbook.
- The owning service writes the rule ID and the model version into its decision record, which is the record ADR-022 collects into the central ledger.
- Packages are owned one each. The Phase 1 packages stay ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER, RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH, the UNIVERSAL package arrives in Epic 3, and the route packages of S1–S9 arrive with their services.
- The target is OMG DMN 1.6 decision models, converted table by table on the same Drools runtime, so there is no big-bang conversion and an XLS table and a DMN model can be in force side by side.

### Consequences

- Good: a rule change is still data, not a release, and it is tested, approved, dated and rolled back in one call.
- Good: there is no shared rule server on the hot path, so a rule evaluation cannot fail because another service is down, and no request crosses a service boundary to decide.
- Good: one owner per model means one place to ask why an answer changed, and the answer carries the model version that produced it.
- Good: a service that cannot load a new model keeps working on the last good one, and the failure is a load event rather than a case error.
- Bad: the registry is a dependency for every service that evaluates a rule, so rwb-decision is on the path of a rule change even though it is not on the path of a rule evaluation.
- Bad: 19 copies of the Drools library have to be upgraded together with the runtime and checked against the stored DRL of every in-force package.
- Bad: a model that compiles and passes 50 scenarios can still be wrong, so the dry run over open cases and the Risk approval carry the weight.
- Bad: RW-COE needs XLS decision-table skills now and DMN modelling skills at the target, and the template reduces but does not remove that change.

---

## ADR-018 No data lake; rwb-reporting builds its read model from events

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-60; DL44 (adopt Architecture v5); supersedes the data lake position of ADR-009

### Context and problem

Today the design copies the decision log to the data lake (E1-014), keeps a lake copy watermark and raises INT-19 and INT-20 for the lake and the Power BI feed. Architecture v5 removes the connection to the data lake, removes INT-19 and INT-20, and gives the reporting measures to rwb-reporting (P9) as a read model built from the business events, with its own schema and its own extract job.

The question is where reporting reads from, and what happens to the copies that only the lake consumed.

### Decision drivers

- One fewer estate to build, run and secure, and no second copy of the decision log
- Reporting that cannot slow ACE, because it never reads the ACE tables or another service's schema
- A read model that can be rebuilt from history
- The regulatory extracts still produced on time, from a source the bank can audit
- A source that a report needs but no service publishes must be visible, not hidden

### Options considered

1. No data lake: rwb-reporting builds its own projections and snapshots from the Kafka business events
2. Keep the lake and the Power BI feed, and copy as today
3. Reporting reads the service schemas directly

### Decision

Option 1. Recovery has no connection to the data lake and no Power BI feed. rwb-reporting (P9) is the read model.

- rwb-reporting consumes the business events and the DecisionRecorded stream into its own projections in `rwb_reporting`: measures, snapshots, the steering dashboard and the regulatory reports.
- JOB-15 runs the reporting extract at 01:30 as a Temporal Schedule in rwb-reporting, with a rerun for any business date and backfills; the bank Airflow scheduler may trigger the same API (POST /reports/{id}/run). Heavy reporting reads `rwb_reporting` only.
- INT-19 and INT-20 are removed from the interface inventory. E1-014 (decision log copy to the data lake) is retired and dependencies on it are dropped.
- `lake_copy_watermark` has no target: the P1 database story drops it. Analysis of the decision log reads the central ledger in rwb-decision (ADR-022), not a lake copy.
- Power BI, if it is used, is fed from rwb-reporting's published output, not from a lake and not from a service schema.
- A report that needs data no service publishes is a gap, not a licence to read a schema: it is raised as a missing data product rather than a direct query.

### Consequences

- Good: one less estate, and no second copy of the audit record that could disagree with the ledger.
- Good: reporting cannot starve ACE or a case screen, because it reads its own schema through its own capped login.
- Good: the read model can be rebuilt by replaying the topics, which is what makes a projection trustworthy.
- Bad: a report is as fresh as the last event consumed and the last snapshot, not as fresh as a source table.
- Bad: a lake-only source has no path at all, so a report that depended on one is blocked until a service publishes the fact.
- Bad: 19 services must publish the events a report needs, which is a demand on every service's contract rather than a query someone writes later.

---

## ADR-019 Edge: gateway-bff for staff and a partner gateway for partners

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-60; DL44 (adopt Architecture v5); ADR-006 stands for the front end

### Context and problem

ADR-006 keeps one ACE front end with a recovery module folder, and the staff sign-in comes from ACE. With 19 services behind the screens, something has to be the single entry for a browser and to compose a screen from more than one service without letting call chains grow. Partners are outside the bank and need a different security profile.

The question is what sits at the edge, and what it is allowed to do.

### Decision drivers

- One entry for staff screens, one sign-in, one session
- A screen that needs two services costs one round trip of two parallel calls, not a chain
- Zero trust: every call encrypted and identified in both directions
- FAPI 2.0 for partner access, in a separate DMZ gateway
- ACE's own front end and sign-in unchanged (ADR-001, ADR-006)

### Options considered

1. gateway-bff for staff and a separate partner gateway for partners, both in front of the owning services
2. The App Gateway routes the browser straight to each service
3. A single gateway for staff and partners

### Decision

Option 1. Staff reach a shared App Gateway with WAF, which sends `/` and `/api/*` to ACE and `/recovery/*` and `/api/recovery/*` to gateway-bff. Partners reach a separate partner gateway in the DMZ, which fronts rwb-partner.

- gateway-bff is a Spring Cloud Gateway with the session in Redis. It signs the user in through ACE Common (Entra ID), keeps an opaque session cookie with a 15-minute idle timeout and issues a short-lived user JWT to the owner service.
- gateway-bff makes one hop to the owning service, and for a composite screen it makes a few parallel calls with a 2 second timeout and a circuit breaker per service. It never calls a service that then calls another.
- Redis holds sessions only, never business data. No screen state and no case data are cached there.
- gateway-bff turns ApprovalRequested and TimerBreached into an inbox push for the officer. Partners do not use it.
- The partner gateway applies FAPI 2.0: sender-constrained tokens, pushed authorisation requests, strong client authentication and MFA, and a penetration test before launch. It fronts rwb-partner only; a partner never reaches another service.
- Every call is encrypted and mutually authenticated, and each service still authorises the resource it serves. The gateway is not the place where authorisation happens.
- ACE's own screens and its shared case view are unchanged: ACE calls `GET /case-summary/{id}` on rwb-case for the shared case view.

### Consequences

- Good: one place for staff sign-in, session and route, and one place for the partner security profile, which is what Audit and the bank's WAF expect.
- Good: a composite screen is a bounded fan-out of one hop each, so a slow service adds latency to its own tab and not to the screen.
- Good: the partner edge can be assessed, pentested and changed without touching staff access.
- Bad: gateway-bff is a shared runtime that every staff screen depends on, so it needs its own availability, scaling and release discipline.
- Bad: two edges to secure, monitor and certificate-rotate, with two different token profiles to keep current.
- Bad: the gateway is a tempting place to put logic; every rule that lands there is a rule outside the owning service and outside its decision record.

---

## ADR-020 Contract-first REST, one hop, 2 second timeout

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-60; DL44 (adopt Architecture v5)

### Context and problem

With 19 services, the calls between them and from the screens are the design. If a service can call another in the middle of a business step, the call graph becomes a monolith with network failures, and a screen waits for the slowest link in a chain. The design needs a small set of call types with fixed rules, and a contract that exists before the code.

The question is what a REST call is allowed to be, and how a caller builds against a service that is not written yet.

### Decision drivers

- A person waiting for an answer gets an answer in a known budget
- No call chains, so latency and failure do not multiply
- A contract a caller can build against before the owner's code exists
- Idempotent commands, because a retry is normal and a duplicate is not
- One trace across the call, the event and the workflow

### Options considered

1. Contract-first REST, one hop, 2 second timeout, with a fixed choice of call type
2. Free REST between services, with call chains allowed
3. No synchronous calls: everything through events or workflows

### Decision

Option 1. REST is for a person waiting, and it is one hop.

- Every service publishes its contracts before its code: OpenAPI 3.1 for REST with `/v1` in the path under `/api/recovery/<short>/v1`, AsyncAPI 3.0 per topic, and a contract jar with the typed activity interfaces. Contract tests run in every build on both sides, and a published fake stands in for a service that is not built.
- Depth is one: browser to gateway-bff to the owner, or a cached reference read. A second hop is a defect; trace analysis flags call depth above one.
- Timeout is 2 seconds. A GET may retry once with jitter. Each downstream gets a Resilience4j circuit breaker and a bulkhead, so one slow service cannot consume the caller's threads.
- Every POST carries an Idempotency-Key, and the stored response is returned on a repeat.
- Errors are RFC 9457 problem details. Success and failure are typed, and a non-retryable failure is named as such.
- The call type is chosen by four questions in order: a person waiting is REST; a fact others may react to is an event; a step another service must perform with a result is a Temporal activity or child workflow; bulk data or a party outside the bank is a file through rwb-integration. ACE data is asked of rwb-source-data, in REST for a screen and as an activity in a workflow.
- Rejected in review: REST from one service to another inside a business step, events used as commands, a service reading another service's schema, and a workflow calling REST directly from workflow code.
- The three call types stay separate: events announce, Temporal commands, REST answers people.

### Consequences

- Good: latency has a ceiling per screen, and a slow service degrades its own tab.
- Good: a caller can start on day one against a contract and its fake, so contract dependencies never block a build.
- Good: idempotency and typed errors make a retry safe, which matters because retries happen at every layer.
- Bad: a use case that genuinely needs three synchronous reads in a row has to become a workflow or a projection, which is more design work than a method call.
- Bad: 19 contracts plus gateway-bff and the partner gateway are artefacts to version, review and test in both directions.
- Bad: the depth-one rule needs trace sampling and a review habit, or it decays into a chain that nobody notices until a peak.

---

## ADR-021 Per-service Flyway and migration ownership

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka
- Decision log: D-RCV-60; DL44 (adopt Architecture v5)

### Context and problem

The monolith has one migration sequence in one recovery schema, with a V0001 baseline and 92 tables. RWB-E1-001 is in build, so the baseline is kept as built (U2). With 19 schemas and 19 logins, the question is who owns the migration that creates and changes a schema, and how the built baseline becomes 19 schemas without editing what is built.

### Decision drivers

- A service owns the DDL of its own schema, and no one else's
- A release of one service does not need a release of another
- The built migration is kept, because Epic 1 work is not rewritten (U2)
- A schema can move to its own server later, so its DDL must be self-contained
- The split is visible as new work, not as an edit to history

### Options considered

1. One Flyway sequence per service in its own schema, in the service's own pipeline; the monolith baseline kept as built and the split shipped as new work
2. One shared migration sequence for all 19 schemas
3. No versioned migrations: schema managed by hand per environment

### Decision

Option 1. Each service owns a Flyway sequence in its own schema, run by its own pipeline.

- The sequence lives with the service, starts from that service's baseline, and holds only objects in that service's schema. A migration that names another schema fails the boundary test as well as the grant.
- The built V0001 baseline and the 92-table migration of RWB-E1-001 are kept unchanged. The split into `rwb_*` schemas is new work: RWB-PLT-NF06-DB for the schema and login estate, plus the per-service database story for each service's DDL. The Change Register records it.
- The 30 `recovery.v_ace_*` views ship in two migrations under the ACE team's ownership, per ADR-010: 16 views with RWB-E1-069 as the next free sequence after the baseline, and 14 views with RWB-ACE-001. `recovery_views.sql` is the artefact.
- The four extension tables of ADR-010 (party_ext, contact_point_ext, account_ext, valuation_ext) migrate in `rwb_source_data`, keyed by ACE business keys and with no foreign key into an ACE schema.
- Each service runs its migrations with its own login, and the login holds the schema privileges the migration needs and nothing on another schema.
- Migration tests run in the service pipeline against a throwaway database: forward from empty, forward from the previous release, and a check that the resulting schema matches the expected object list.
- A data movement that spans services is not one script. It is a backfill through the owner's contract, sequenced with the Build Sequence, and it is visible as such.

### Consequences

- Good: a service releases its schema change with its own code, and no one else's release train is involved.
- Good: the DDL of a schema can move to its own server, because it is self-contained and names nothing outside itself.
- Good: the built Epic 1 migration is not rewritten, so the as-built record and the tests that read it stay valid.
- Bad: 19 sequences in four environments are 76 migration targets to order and observe at cutover, so the cutover needs a sequencing plan rather than a single run.
- Bad: there is no cross-schema ordering guarantee, so a change that needs data from another service waits on an event or a backfill, not on a migration.
- Bad: a defect in the split of the baseline is found late, because the baseline itself is untouchable and the correction has to be a new migration per service.

---

## ADR-022 A local decision record plus a central ledger

- Status: Proposed
- Date: 22 November 2026
- Deciders: the solution architect with Risk and Internal Audit; SCB IT, the ACE team, TechX and Henka for the implementation
- Decision log: D-RCV-60; DL44 (adopt Architecture v5); supersedes ADR-009

### Context and problem

ADR-009 wrote one append-only, hash-chained log in the ACE database inside every action, and a failed write blocked the action. That works for one deployable with one schema. With 19 services, a synchronous central write inside every action becomes a distributed transaction across a network, and a ledger outage becomes an outage of every action.

Architecture v5 keeps the guarantees that matter — every decision traceable, the chain tamper-evident, an auditor able to search one place — and moves the write to the service that makes the decision.

### Decision drivers

- A decision record written in the same transaction as the change it explains
- No distributed transaction on the hot path, and no dependency on a remote ledger for an ordinary action
- A central place to search, with the rule version and the approver
- A chain that shows a gap or an edit
- Irreversible steps that still wait for the ledger

### Options considered

1. A local decision record in each service's schema, hash-linked and published, with a central ledger in rwb-decision
2. The synchronous central log of ADR-009
3. Application logs searched after the event

### Decision

Option 1. Each service records locally, and rwb-decision keeps the central ledger.

- Each of the 19 services writes its decision record in its own schema, in the same transaction as the state change, hash-linked to its own previous record, with these fields: `chain_seq`, `inputsRef`, `ruleId`, `ruleVersion`, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `actions`, `outcome`, `decidedAt`, `prev_hash` and `entry_hash`.
- The same transaction writes the outbox row. The relay publishes DecisionRecorded on `rwb.decision-record.v1`, and rwb-decision consumes it idempotently into the central ledger with a 5-minute completeness target.
- A gap in `chain_seq` raises an alert, and the chain is checked every day by JOB-14 at 02:00, a Temporal Schedule in rwb-decision. JOB-13 is continuous ingest, not an overnight copy.
- The ledger hash is anchored daily to write-once storage: the ledger seal is an immutable file, so a later change to a row is detectable even with database access.
- Strict mode applies at the points of no return only: debt transfer, write-off, auction sale and title transfer wait for the central ledger to acknowledge the record before the step executes. Every other action carries on at full speed.
- `decision_log_entry` stays in rwb-decision with its columns, and `rule_id` and `rule_version` keep carrying the rule name and the package version label. Analysis and audit read the ledger; there is no lake copy (ADR-018).
- A correction is a further entry naming the original. Nothing is updated in place, and nothing is deleted.
- The ledger model needs Risk and Internal Audit sign-off before it is in force.

### Consequences

- Good: an ordinary action costs one local transaction and an outbox row, so a ledger outage does not stop the Workbench.
- Good: the record is written with the change it explains, so the two cannot disagree.
- Good: an auditor has one place to search, with the rule version, the approver and the daily anchor, and a chain check that runs itself.
- Good: an irreversible step still waits for the acknowledgement, so the control survives at the points where it matters.
- Bad: completeness is eventual, up to the 5-minute target, so a report that must be exact has to wait for the ledger and say so.
- Bad: strict mode puts the central ledger on the critical path of four irreversible steps, which makes rwb-decision an availability dependency for them.
- Bad: the change from ADR-009 needs Risk and Internal Audit sign-off, and an unauthorised change to the record is now a database-level control in 19 schemas rather than in one.

---

## ADR-023 Observability per service

- Status: Proposed
- Date: 22 November 2026
- Deciders: SCB IT, the ACE team, TechX and Henka; the platform team for the observability stack
- Decision log: D-RCV-60; DL44 (adopt Architecture v5)

### Context and problem

With 19 services, a case journey crosses REST calls, Kafka topics and Temporal activities. A support call that starts with "the case is stuck" has to be answered from one trace, and an operator has to see which queue, topic or provider is behind before a user notices. The observability design also carries the audit and PII path and the stuck-workflow signal.

The question is what every service emits, what is aggregated where, and what is alerted on.

### Decision drivers

- One trace across REST, Kafka and Temporal (OpenTelemetry, W3C Trace Context)
- The health of a queue, a topic and an outbox visible before a user is affected
- Personal data kept out of logs and traces
- Failure containment that can be seen: one service down and the other 18 running
- A service template that makes all of this the default, not a per-team project

### Options considered

1. Observability per service from the service template, collected into one bank stack, with per-service and per-platform alerts
2. One central agent per environment with application logs only
3. Metrics per service with no distributed tracing

### Decision

Option 1. Every service is instrumented from the template, and the platform collects it.

- Every service emits OpenTelemetry traces, metrics and logs. The trace context is propagated on REST (`traceparent`), on Kafka through the CloudEvents headers, and through Temporal activity and workflow headers, so one case journey is one trace.
- Every service exposes `/health` and `/metrics` for the platform, and the api and worker deployments are separate, so a worker backlog does not hide in the api health.
- Alerts cover the signals that precede a user-visible failure: Temporal task-queue backlog and stuck workflows (JOB-21), Kafka consumer lag and `.dlt` depth, outbox age, retry-topic depth, rule model load failures, circuit-breaker open state, and the daily hash-chain result (JOB-14).
- There is one dashboard per service and one per journey, and the journey view shows the step the case is waiting on and the service that owns it.
- Audit and personal data access logs go through ACE Common's PII path to the SOC, as ADR-001 set. Personal data never appears in an application log, a trace attribute or a metric label, and payload inspection goes through the codec server on a break-glass session.
- Database observability is per login: pool saturation, connection count against the cap and statement timeouts, per schema, so one service cannot be diagnosed as the database.
- Service targets are the NFR v3 targets: screen response under 2 seconds at p95, rule evaluation under 300 ms, the AI agent answered within 60 seconds or the rule result used, and 99.9% availability in business hours. RPO and RTO are Not specified in the source documents (GAP-0093; ASM-0155).
- The daily smoke workflow (JOB-22) exercises a journey end to end at 06:00 and alerts on failure, which is the signal that the platform, not one service, is broken.

### Consequences

- Good: one trace answers the support question, and the journey view names the service the case is waiting on.
- Good: queue, topic and outbox signals are alerted before a user is affected, which is the difference between a contained failure and an incident.
- Good: the template makes instrumentation the default, so a new service is observable on its first deploy.
- Bad: 19 services in four environments multiply the dashboards, alerts and metric volume, and alert noise becomes the main operational risk.
- Bad: propagating trace context through Kafka and Temporal needs discipline in the template and a test, or the trace stops at the first hop.
- Bad: RPO and RTO are not set, so the availability target cannot be tested against a recovery objective until the NFR specification names one.
