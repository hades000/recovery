<!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v1.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `05 Technical architecture/Recovery Workbench Architecture Decision Records v1.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench architecture decision records

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| ID | Decision | Status | Date |
|---|---|---|---|
| ADR-001 | Build the Workbench as a module of ACE | Accepted | 27 October 2026 |
| ADR-002 | Structure ACE as a modular monolith with common, collection and recovery modules | Accepted | 27 October 2026 |
| ADR-003 | Run the case workflow in code, in CMMN 1.1 terms, with no workflow engine | Accepted | 27 October 2026 |
| ADR-004 | Hold every rule as versioned data and evaluate it with a decision table component | Accepted | 20 October 2026 |
| ADR-005 | Take data through COLLINS and file loads, and call no system of record directly | Accepted | 27 October 2026 |
| ADR-006 | One ACE front end with a recovery module folder | Proposed | 28 October 2026 |
| ADR-007 | Build the document hub in the Workbench as the system of record for recovery documents | Accepted | 26 October 2026 |
| ADR-008 | Trunk based development with feature flags | Accepted | 27 October 2026 |
| ADR-009 | An append-only, hash-chained decision log that blocks an action it cannot record | Proposed | 28 October 2026 |

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
- Bad: the recovery and collection squads share one repository and one release, so merge ownership and release discipline matter (ADR-008, DL04).
- Bad: recovery takes ACE's data position: end of day data through COLLINS, with no real-time feed today (ADR-005).

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

- Status: Accepted
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

- Status: Accepted
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

- Status: Accepted
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
