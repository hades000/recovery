SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench PRD P3 rwb-case v1

Product requirements for the case and workflow service of the Recovery Workbench, covering case creation, case state, queues, allocation, timers, reference data and the case screens, delivered in the nineteen-service realignment under D-RCV-60.

## 1. Document control and change log

| Item | Detail |
|---|---|
| Document | Recovery Workbench PRD P3 rwb-case |
| Title | Product requirements for P3 rwb-case (case and workflow) |
| Description | What the case and workflow service must do, for which roles, under which non-functional limits and in which release slice; derived from the program and epic business requirements and the P3 functional specification, and realigned to Architecture v5 and D-RCV-60 |
| Version | 1 |
| Status | Draft |
| Date | 22 November 2026 |
| Module | P3 Case and workflow (business module 5.3 of the program BRD) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Delivery wave | 1 |
| Decision | D-RCV-60 microservice realignment; ADR-013 to ADR-023 |
| BRD (business baseline) | 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx (version 5, 22 November 2026); 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v5.docx (version 5); 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.docx (version 3); 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx (version 1) |
| Delivery model | BRD Program v5 §10 and §11 (service epic, wave, business epic and requirement trace per service); Epic 1 v5 §8 and §9; Epic 2 v3 §8 and §9 |
| Functional source | 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P3 Case and workflow v4.md (document version 3, 15 November 2026) |
| Architecture baseline | 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md; 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md |
| Rules applied | 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md, §R1, §R3, §R5, §R8, §R9 |
| Ownership | 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx, read as _work/msr/plan/ownership.json |
| Owners (roles only) | Business lead (business owner); Product owner (product decisions); Solution architect (non-functional and contracts); Business analyst, P3 (documentation) |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |

**Change log.**

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | First version; D-RCV-60 microservice realignment from the program and epic BRDs and FSD P3 | T3 Code / OpenCode / DeepSeek v4.1 Flash |

Change-log row, as required by Template and Rules §R8.1: 1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.

**How this document is built.**

- It is one of the 20 service PRDs required by Template and Rules §R8.5 (19 services plus Platform). It is scoped to P3 rwb-case; another service's requirement is named only as a dependency (ASM-2683).
- Every functional requirement carries a CAP ID, the business requirement ID from the BRD, the feature, rule and acceptance-criteria codes from the FSD P3, and a MoSCoW priority. The FSD P3 carries no requirement identifier of its own, so the BRD REQ ID is the requirement key (GAP-1552; ASM-2682).
- PRD identifiers use the module infix and are new: CAP-P3-nnn, FR-P3-nnn, NFR-P3-nnn, AC-P3-nnn. FSD acceptance criteria are cited as AC-P3-nnn-nn (FSD) (ASM-2681).
- The document states requirements, not solution design. Where a v5 architecture constraint is confirmed (service boundaries, contracts, event names, workflow model, schema ownership) it is stated as a constraint on the requirement, not as a design.
- Every release date is copied unchanged and marked (tentative) (Template and Rules §U7; ASM-2684).
- This revision is issued as Draft: no Product Owner or FDA decision is evidenced on the BRD or the FSD (GAP-1550; ASM-2680).

## 2. Product overview and relationship to ACE

### 2.1 What the service is

rwb-case is the case and workflow service of the Recovery Workbench. It owns the recovery case, the case state, the queues and their membership, the assignment of work, the tasks, the timers and the case screens. It is one of 19 services inside the ACE platform, delivered in wave 1 (Architecture v5 slide 41).

| Attribute | Value |
|---|---|
| Service | rwb-case |
| Business module | P3 Case and workflow |
| Wave | 1 (Architecture v5 slide 41) |
| Schema | rwb_case (one schema and one login per service) |
| Contract base | /api/recovery/case/v1 (Template and Rules §R4) |
| Events published | topic rwb.case.events.v1 |
| Task queue | rwb-case, in namespace rwb-recovery |
| Java package | th.co.scb.ace.workbench.recovery.case |
| Service epic | RWB-SVC-P3 |

### 2.2 What is new in this service

1. **A recovery case as a first-class object.** One case per customer and product, with its accounts and parties linked by ACE business key and no foreign key into ACE (REQ-CWC-003).
2. **An explicit case state model.** Stage, status, route and deviation flags, one state at a time, every move made by rule (REQ-CWC-005).
3. **Reference data as the source of every business value.** Roles, teams, queues, capacity, service levels, legal periods, exclusion rules, allocation and transfer rules, parameters and lists of values (REQ-CWC-006, REQ-DRI-010, REQ-DRI-011).
4. **Allocation, assignment and transfer by rule,** with an overflow queue and a daily rebalance, so no case is allocated by hand as a matter of course (REQ-CWC-007 to REQ-CWC-010, REQ-CWC-015).
5. **A service level clock, escalation and a prescription clock** held apart from each other, so a breach escalates without moving the case and a legal date never pauses (REQ-CWC-011, REQ-CWC-012).
6. **A next action on every open case,** produced from the routing rule that moved the case (REQ-WKM-012 to REQ-WKM-016).
7. **A queue write interface for a model or an agent,** under the same permission checks as a person and behind a dated flag (REQ-CWC-017 to REQ-CWC-020).
8. **A case workflow instance per case** on the shared Temporal cluster, as the parent of a child workflow per stage (Architecture v5 slides 22 to 25; Temporal and Drools design slide 13).

### 2.3 What is reused from ACE and from other services

| Capability | Verdict | Reused from | What rwb-case does |
|---|---|---|---|
| Sign-in, access check and permission decision | Reuse | ACE sign-in through gateway-bff and the authorise contract of rwb-access (P4) | Calls the contract; holds no role table of its own beyond the queue and team structure it owns |
| Audit and personal-data access logging | Reuse | ACE PII logging path through rwb-access and the decision record path of rwb-decision (P7) | Emits the record; does not build a second audit store |
| Source data: account, customer, contact, relations, collateral, collections history, plan, payment | Reuse | ACE database, read only, through the contract of rwb-source-data (P1); Arch v5 slide 45 gives the read of the recovery.v_ace_* views to rwb-source-data only | Holds the business key that links to the ACE record; copies no source record (GAP-1549; ASM-2686) |
| ACE batch business date and completion | Reuse | The ACE batch record, read through rwb-source-data, which raises AceDataReady | Starts case creation and the daily run on AceDataReady; reads no batch record itself |
| Notification path, documents, decision log, reporting | Reuse | rwb-comms (P6), rwb-document (P5), rwb-decision (P7), rwb-reporting (P9) | Publishes the business event; the owner service acts |
| Rule registry, rule packages and rule test cases | Reuse | rwb-decision (P7) owns the registry; the service runs a local evaluated copy of the package (Template and Rules DP-04) | Loads and evaluates the package copy, records the rule ID and version it used |
| Workflow runtime | Reuse | The shared Temporal cluster and the platform workflow kit (RWB-PLT-WF) | Runs CaseWorkflow and the daily case run; holds no scheduler of its own |
| Interaction ledger | Reuse | rwb-source-data (P1) owns the ledger (Template and Rules §R3 default ruling, DP-18) | Writes and reads interactions through the P1 contract; keeps no second ledger |
| Delegation of authority | Reuse | rwb-access (P4) owns the DoA table | Consumes the limit decision; holds no limit of its own |
| Feature flags | Reuse | Platform library (Template and Rules §R3 default ruling) | Declares its flags with an owner and a removal date |

### 2.4 Relationship to the Epic 1 work already in build

The case list, the case record view, allocation, transfer, timers and prescription dates were built or are in build as one module of a single application. Under D-RCV-60 the same behaviour is delivered by rwb-case as a separate service with its own schema and contract. The preserved stories keep their content; the microservice change is carried by the contract story and the delta stories of the service epic (Template and Rules §R6). This PRD states the service's product requirements only; it does not restate the as-built behaviour of the monolith.

The Epic 1 trace records two requirements of this module as kept as built with a delta (RWB-E1-042 and RWB-E1-043) and one as moved unchanged (RWB-E1-045); the built code does not change until a delta story is picked up (BRD Epic 1 v5 §9; Template and Rules §R6).

### 2.5 Delivery model

Taken from BRD Program v5 §10, which adds the delivery structure without changing a requirement ID, its text, its priority or its business owner.

| Item | Value |
|---|---|
| Service epic | RWB-SVC-P3 |
| Wave the service is created in | 1 |
| Business epics this service serves | EP01, EP02, EP07 (BRD Program v5 §10.2) |
| Requirement rows assigned to this service | 48: REQ-CWC-001 to REQ-CWC-020, REQ-CHO-001 to REQ-CHO-010, REQ-WKM-001 to REQ-WKM-016 (to EP07 for REQ-WKM-010), REQ-DRI-010 and REQ-DRI-011 (BRD Program v5 §11) |
| Contract first | The contract is published before the build starts and a contract story is Day 1; no build waits on another service being built (BRD Program v5 §10.4; ADR-020) |
| One hop, two seconds | The service is called once from gateway-bff, with a two second timeout, and reads no other service's schema (BRD Program v5 §10.4; ADR-014, ADR-020) |
| Shared items it owns | Parameters and reference data, and the case list API and screen; the daily case list row stays with P1 (BRD Program v5 §10.5) |
| Shared items it consumes | The rule package registry (P7), the interaction ledger (P1), the delegation of authority table (P4), the feature flags and the outbox, inbox and idempotency tables (platform library) (BRD Program v5 §10.5) |

## 3. Personas and roles

Roles are named by role only. No individual is named anywhere in this document.

| Persona | Who they are | What they do on rwb-case | Source |
|---|---|---|---|
| Case owner | The person who holds a case from day 90 to close and answers for its outcome | Works their queue, reads the case record, sees the next action and the timers, records the outcome of the action | BRD Epic 1 §2; FSD P3 role tables |
| Team manager | The lead of a team of case owners | Sees every queue in the team, transfers and reassigns with a reason, watches ageing, breaches and caseload, receives the escalation | BRD Epic 1 §2 and Epic 2 §2; FSD P3 A2.39, A2.40, A2.41 |
| Restructuring officer (FCR) | The officer who prepares a plan for credit approval | Works the treatment and plan tasks that the case raises, submits the credit pack, reads the booking confirmation | BRD Epic 2 §2; FSD P3 A2.33, A2.34 |
| Litigation officer | The officer who instructs and follows legal action | Reads the case and its timers, holds and transfers the case, records the legal event that a transfer rule reacts to | BRD Epic 1 §2; FSD P3 A2.10 |
| Legal counsel | The role that owns legal periods and legal document standards | Owns the legal periods reference data that sets prescription dates | BRD §5.3 REQ-CWC-012 |
| Center of excellence analyst | The role that owns the rules and the parameters | Loads a rule version, runs the dry run, rolls back, reads the change report | BRD §5.3 REQ-CWC-013 to REQ-CWC-016; FSD P3 A2.14 to A2.16 |
| Reference data administrator | The role that owns the versioned tables | Loads reference data with valid from and valid to, author and approver | BRD §5.2 REQ-DRI-011 |
| Product head (Mortgage, HP, SSME) | The business owner of a product line | Approves the product parameters and the limits that the case reads | BRD §5.3 REQ-CWC-011; FSD P3 A2.25 |
| Platform administrator | The role that owns the flags and the run books | Sets a feature flag with its removal date, works a failed job from its run book | BRD §6.4 NFR-026; FSD P3 A2.26 |
| Compliance and PDPA officer | The role that owns masking and retention | Reviews the classification, the masking by role and the retention class of each record | BRD §6.5 NFR-031, §6.7 NFR-039 |
| Internal audit | The audit role | Queries the decision log and the rule change report for a case or a population | BRD §5.3 REQ-DRI-012 |
| Data steward and data product owner | The role that owns data quality and freshness | Reads the freshness state on the case list and works a reconciliation break | BRD §6.3 NFR-014, NFR-018 |
| Tribe lead | The programme business lead | Reads the steering measures that the case data feeds | BRD §5.3 REQ-WKM-009 |
| Analytical model or agent (non-human actor) | A model or an agent acting under a service identity | Places a case on a queue through the queue write interface, under the same permission checks as a person | BRD §5.3 REQ-CWC-017, REQ-CWC-018; FSD P3 A2.52 |
| Unattended system actor | The service itself on a Timer schedule or an event | Creates cases, allocates, rebalances, evaluates timers, escalates | FSD P3 A2.1, A2.17, A2.13 |

**Role classes carried by the program BRD.** 37 bank user roles, 7 partner user roles, 4 customer party roles and 6 non-human actor roles (BRD §3). Of these, the bank roles and the non-human actors above operate this service; no partner or customer party role operates rwb-case directly in this service's scope.

## 4. User journeys

Each journey states the current step list and the target step list. The current state is taken from the FSD P3 background: cases are run from team spreadsheets and ownership and deadlines are agreed by email (FSD P3 A1.3).

### 4.1 Case entry at 90 days past due

| # | Current | Target |
|---|---|---|
| 1 | A team downloads the days-past-due list from the core bank extract each morning | The ACE batch for the business date completes and rwb-source-data raises AceDataReady |
| 2 | An officer filters the list for 90 or more days past due in a spreadsheet | The service takes the eligible population and applies the entry rule for 90 days past due (REQ-CWC-001, REQ-CHO-004) |
| 3 | An officer checks by hand for deceased, fraud, bankruptcy, an active plan and an open dispute | The exclusion rules run as data and the reason and rule version are recorded (REQ-CWC-004) |
| 4 | An officer opens a new row and types a case reference and the accounts | A case number in the form RW-YYYY-NNNNNN is issued once and the accounts and parties are linked by business key (REQ-CWC-002, REQ-CWC-003) |
| 5 | The officer asks a team lead who should hold the case | The allocation and assignment rules place the case in a queue and give it one owner by 07:00 (REQ-CWC-007 to REQ-CWC-009) |
| 6 | The officer emails the case reference to the owner | The owner sees the case in their queue with its next action and its service level (REQ-CWC-011, REQ-WKM-001, REQ-WKM-012) |

### 4.2 A case owner starts the working day

| # | Current | Target |
|---|---|---|
| 1 | The owner opens several spreadsheets and asks colleagues what is urgent | The owner opens their queue, filtered by stage, route, status and age, sorted by service level (REQ-WKM-001, REQ-WKM-002) |
| 2 | The owner guesses which case is nearest a deadline | Every row shows its age in state and its breach flag (REQ-WKM-005, REQ-CWC-011) |
| 3 | The owner opens four systems to learn the case history | The case record view shows accounts, parties, stage, owner, clocks, deviations, documents, decisions and the timeline (REQ-OCC-007, REQ-OCC-008) |
| 4 | The owner works out what the case needs next | The next action states what has to happen, who owns it and the date it is due (REQ-WKM-012 to REQ-WKM-014) |

### 4.3 A service level is about to be breached

| # | Current | Target |
|---|---|---|
| 1 | Nobody notices until the customer complains or the case is reviewed | The stage clock starts on entry to every state from the timer table (REQ-CWC-011) |
| 2 | A team lead chases by email | The warning threshold and the breach escalate to the role named in the table, and the case does not move (REQ-CWC-011, REQ-WKM-004) |
| 3 | The escalation is lost in the mailbox | The escalation state, to whom it went and when are visible on the case (REQ-WKM-005) |

### 4.4 A hand-off between people or teams

| # | Current | Target |
|---|---|---|
| 1 | The owner emails the team lead and asks for a case to move | The owner or the lead transfers the case with a reason code from the agreed list (REQ-WKM-003) |
| 2 | The lead replies and the case is copied by hand | The transfer rules check the move and the state and the clocks are kept (REQ-CWC-010, REQ-WKM-007) |
| 3 | The new owner learns about it days later | The new owner sees the case in their queue at once and the transfer is on the case history with its reason (REQ-WKM-008) |

### 4.5 A rule or parameter change

| # | Current | Target |
|---|---|---|
| 1 | The business asks for a change of a limit, a timer or a rule | The analyst changes a versioned parameter or reference row, or loads a rule version through the validated template (REQ-DRI-010, REQ-DRI-011, REQ-CWC-013) |
| 2 | A developer changes code and a release is scheduled | Validation runs on schema, overlaps, unreachable rows, a missing default and the test cases, and a dry run runs against live cases (REQ-CWC-014) |
| 3 | The change is recorded in a ticket and a change note | The version, the author, the approver and the effect are recorded, and every decision records the version it used (REQ-CWC-013, REQ-CWC-016) |
| 4 | Rolling back means another release | Rollback returns the engine to the previous version by one call (REQ-CWC-013) |
| 5 | Audit reconstructs the change from memory | The rule change report lists who changed what, when, under which version and with what effect (REQ-CWC-016) |

### 4.6 A model or an agent places a case on a queue (target only)

| # | Current | Target |
|---|---|---|
| 1 | A daily score arrives in a file and a person re-keys the priority | The model places the case on a queue with the score, the priority and the reason (REQ-CWC-017) |
| 2 | Nobody can tell where the priority came from | The write passes the same permission checks as a person, runs under a service identity and is logged with the model version (REQ-CWC-018) |
| 3 | — | The placement sits in the same queue and the same order as rule-allocated work, so the person works one list (REQ-CWC-020) |

### 4.7 The case closes (later increment)

| # | Current | Target |
|---|---|---|
| 1 | A closed case stays in the working list indefinitely | The case closes once its retention period has run and no action is open (NFR-031; GAP-1554) |
| 2 | Nobody can say what was kept and for how long | The record class and its retention rule are visible and the closure is recorded (NFR-031; GAP-1555) |

## 5. Capabilities and features

### 5.1 Capability table

MoSCoW follows the BRD priority of the requirements behind the capability: Must = the epic cannot release without it, Should = planned in the epic, Could = taken if capacity allows.

| CAP | Capability | What it delivers | BR (REQ) | MoSCoW | Wave | FR |
|---|---|---|---|---|---|---|
| CAP-P3-001 | Case creation and entry at 90 days past due | One case per customer and product, created by rule from the eligible population once the ACE batch is complete, with a case number issued once and accounts and parties linked by business key | REQ-CWC-001, REQ-CWC-002, REQ-CWC-003, REQ-CHO-004 | Must | 1 | FR-P3-001 to FR-P3-003, FR-P3-005, FR-P3-006, FR-P3-035 |
| CAP-P3-002 | Exclusion rules as data | Deceased, fraud, bankruptcy, an active plan and an open dispute block case creation, with the reason and the rule version recorded | REQ-CWC-004 | Must | 1 | FR-P3-004 |
| CAP-P3-003 | Case state model | Stage, status within stage, route and deviation flags; one state at a time; every move by rule | REQ-CWC-005 | Must | 1 | FR-P3-007 |
| CAP-P3-004 | Roles, teams, queues and capacity as data | The organisation and its capacity held as versioned reference data and changed without a code release | REQ-CWC-006, REQ-ACA-002 | Must | 1 | FR-P3-008 |
| CAP-P3-005 | Allocation and assignment by rule | Every new case placed in a queue and given one owner by rule, with a capacity cap and an overflow queue | REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 | Must | 1 | FR-P3-009 to FR-P3-011 |
| CAP-P3-006 | Transfer rules and manual transfer | Cases move on the named triggers by rule, or by an authorised user with a reason code, and the state and clocks are kept | REQ-CWC-010, REQ-WKM-003 | Must | 1 and 2 | FR-P3-012, FR-P3-013 |
| CAP-P3-007 | Service levels, timers, escalation and prescription dates | A clock per queue and status from the timer table, a warning and an escalation to the named role, and a prescription date that never pauses; a deviation pauses the stage clock only | REQ-CWC-011, REQ-CWC-012, REQ-DVH-002, REQ-DVH-006, REQ-WKM-004, REQ-WKM-005 | Must | 1 and 2 | FR-P3-014 to FR-P3-016, FR-P3-022 |
| CAP-P3-008 | Daily rebalancing and queue measures | Unassigned and over-capacity cases move overnight before the working day, and queue depth, ageing, spread and breaches are published and reconcile to the case list | REQ-CWC-015, REQ-WKM-006, REQ-WKM-007 | Must | 1 | FR-P3-017, FR-P3-018 |
| CAP-P3-009 | Case list and case record view | One list and one record view per case, with queue, owner, stage, status, age, clocks, history and documents, and the account columns read from the source contract | REQ-RDF-007, REQ-OCC-007, REQ-OCC-008, REQ-WKM-001, REQ-WKM-002, REQ-WKM-005, REQ-WKM-008, REQ-WKM-011 | Must | 1 and 2 | FR-P3-019 to FR-P3-021 |
| CAP-P3-010 | Next action on every open case | What has to happen, who owns it and the date it is due, produced from the rule that moved the case, escalated when overdue, reported when absent | REQ-WKM-012 to REQ-WKM-016 | Must | 2 | FR-P3-023 |
| CAP-P3-011 | Queue write from a model or an agent | A placement from a non-human caller under the same permission checks, under a service identity, logged with the model version, behind a dated flag, in the same queue order | REQ-CWC-017 to REQ-CWC-020, REQ-ACA-010 | Must | 2 | FR-P3-024 |
| CAP-P3-012 | Parameter catalog and configuration service | Every limit, threshold, timer and name a versioned row with an owner and a used-by record; no business value in code | REQ-DRI-010, REQ-CWC-011 | Must | 1 | FR-P3-025 |
| CAP-P3-013 | Reference data service | Every reference table served with its version, valid from and valid to, author and approver | REQ-DRI-011, REQ-CWC-006 | Must | 1 | FR-P3-026 |
| CAP-P3-014 | Rule version authoring, validation, rollback and change report | A validated template load, a dry run, a version stamp, a one-call rollback and a recorded change history | REQ-CWC-013, REQ-CWC-014 | Must | 1 and 2 | FR-P3-027 to FR-P3-029 |
| CAP-P3-015 | Workflow event log and decision record | Every state change, allocation, transfer and timer written as an event with its rule ID and version, and a decision record sealed centrally | REQ-CWC-016 | Must | 1 | FR-P3-030 |
| CAP-P3-016 | Workflow administration interface | A programmatic way to move, reassign and correct a case with a reason code, before the screens exist | REQ-WKM-003, REQ-CWC-005 | Must | 1 | FR-P3-031 |
| CAP-P3-017 | Hand-over from collections and plan status | The case carries the contact and promise history of the account before day 90 and the ACE plan status, and is current the morning after a change | REQ-CHO-001, REQ-CHO-002, REQ-CHO-003, REQ-CHO-005, REQ-DRI-013 | Must | 2 | FR-P3-032 |
| CAP-P3-018 | Treatment record, plan timers, credit pack and booking confirmation | A treatment record for every offer, timers from the record, the credit pack for the approval system, and the booking confirmed from the next business date's account data | REQ-CHO-006, REQ-CHO-007, REQ-CHO-008, REQ-RDF-014 | Must | 2 | FR-P3-033, FR-P3-034 |
| CAP-P3-019 | Decision log query for audit | The decision history of a case or a population with its inputs, versions, approver and final call, read through the decision service contract | REQ-DRI-012 | Must | 2 | FR-P3-036 |
| CAP-P3-020 | Release control and go-live readiness | Dated feature flags, the release checklist, training and readiness for the release | REQ-CWC-019 (flag), BR-P3-026, BR-P3-049 | Should | 2 | FR-P3-037 |
| CAP-P3-021 | Measures for the steering dashboard and reporting | Case, queue, ageing, breach and turnaround measures published from the case record for the reporting service's dashboard and the baseline | REQ-WKM-006, REQ-WKM-009 | Must | 2 | FR-P3-040 |
| CAP-P3-022 | Case closure after the retention period | The case moves to closed once its retention class has run and no action is open, with the closure recorded; the closure rule, the reason and the approver stay with rwb-writeoff | NFR-031, REQ-S7-008 | Must | 4 | FR-P3-038 |
| CAP-P3-023 | Capacity view | Inflow by product, bucket and region against available capacity | REQ-WKM-010 | Could | 4 (EP07) (GAP-1553) | FR-P3-039 |
| CAP-P3-024 | Payment and outcome exception on the case | The payment matched to the plan, the settlement or the fee is visible on the case, and an unmatched payment appears as an exception for the case owner, read from the payment service | REQ-CHO-009 | Must | 2 | FR-P3-041 |

### 5.2 Feature inventory carried from the FSD P3

The FSD P3 holds 52 features (FEAT-CWC-01 to FEAT-CWC-29, FEAT-CHO-01 to FEAT-CHO-11, FEAT-WKM-01 to FEAT-WKM-12). Each is placed by this PRD as follows.

| FSD feature | Feature name | CAP | Note |
|---|---|---|---|
| FEAT-CWC-01 | Generate the case ID | CAP-P3-001 | — |
| FEAT-CWC-02 | Create one case per customer and product | CAP-P3-001 | Also the anchor for the merge requirement (GAP-1561) |
| FEAT-CWC-03 | Hold the case state in the ACE database | CAP-P3-003 | The state is held in the service's own schema, not in a shared table (Template and Rules DP-01) |
| FEAT-CWC-04 | Apply the entry rule at 90 days past due | CAP-P3-001 | — |
| FEAT-CWC-05 | Apply the exclusion rules as data | CAP-P3-002 | — |
| FEAT-CWC-06 | Hold roles, teams and queues as data | CAP-P3-004 | — |
| FEAT-CWC-07 | Run the allocation rule table | CAP-P3-005 | — |
| FEAT-CWC-08 | Run the assignment engine by load and continuity | CAP-P3-005 | — |
| FEAT-CWC-09 | Send a case to the overflow queue when no rule matches | CAP-P3-005 | — |
| FEAT-CWC-10 | Run the transfer rule table and engine | CAP-P3-006 | — |
| FEAT-CWC-11 | Set service levels and stage timers | CAP-P3-007 | The clock is a durable timer in the case workflow; the timer row is the projection the screen reads (ASM-0078 in the ownership map) |
| FEAT-CWC-12 | Set and track prescription dates | CAP-P3-007 | — |
| FEAT-CWC-13 | Escalate a breached timer to the named point | CAP-P3-007 | — |
| FEAT-CWC-14 | Load a rule version with validation | CAP-P3-014 | The registry is rwb-decision's (DP-04); the service loads and evaluates its copy |
| FEAT-CWC-15 | Roll back a rule version | CAP-P3-014 | — |
| FEAT-CWC-16 | Report every rule change for audit | CAP-P3-014 | — |
| FEAT-CWC-17 | Rebalance queues daily | CAP-P3-008 | — |
| FEAT-CWC-18 | Publish queue measures | CAP-P3-008 | — |
| FEAT-CWC-19 | Show queue and owner on the case list | CAP-P3-009 | — |
| FEAT-CWC-20 | Expose the workflow admin API | CAP-P3-016 | — |
| FEAT-CWC-21 | Log every workflow event | CAP-P3-015 | — |
| FEAT-CWC-22 | Hold the parameter catalog and configuration service | CAP-P3-012 | — |
| FEAT-CWC-23 | Run the reference data service with versioned tables | CAP-P3-013 | — |
| FEAT-CWC-24 | Run versioned migrations with parameterized schema names | CAP-P3-013 | Delivered as a platform capability (RWB-PLT-DB); the service consumes it |
| FEAT-CWC-25 | Set product parameters without a code change | CAP-P3-012 | — |
| FEAT-CWC-26 | Control module release with dated feature flags | CAP-P3-020 | The flag service is the platform library's; the service declares its flags |
| FEAT-CHO-01 | Take the case hand-over from EFS with full history | CAP-P3-017 | The history is read through the source contract, not loaded |
| FEAT-CHO-02 | Read the ACE plan status | CAP-P3-017 | — |
| FEAT-CHO-03 | Read customer facts from ACE | CAP-P3-017 | Through the source contract (GAP-1549) |
| FEAT-CHO-04 | Create a case the morning after it reaches 90 days past due | CAP-P3-001 | — |
| FEAT-CHO-05 | Hold case creation when the ACE batch is late | CAP-P3-001 | — |
| FEAT-CHO-06 | Hold the treatment entity and plan timers | CAP-P3-018 | — |
| FEAT-CHO-07 | Prepare the credit approval pack for NLEADS | CAP-P3-018 | — |
| FEAT-CHO-08 | Confirm booked terms from the ACE account data | CAP-P3-018 | — |
| FEAT-CHO-09 | Build the stage 2 data products | CAP-P3-018 | The products are built in the data service; the case provides the source facts (REQ-RDF-014) |
| FEAT-CHO-10 | Automate the EFS file load (removed) | — | Removed by D-RCV-35; ACE ingests EFS. No requirement is carried |
| FEAT-CHO-11 | Query the decision log for audit | CAP-P3-019 | Read through the decision service contract |
| FEAT-WKM-01 | Show my queue with filters and ageing | CAP-P3-009 | — |
| FEAT-WKM-02 | Show team queues | CAP-P3-009 | — |
| FEAT-WKM-03 | Transfer a case manually with a reason | CAP-P3-006 | — |
| FEAT-WKM-04 | Reassign a case to another owner | CAP-P3-006 | — |
| FEAT-WKM-05 | Show timers and the service level on the case | CAP-P3-007 | — |
| FEAT-WKM-06 | Show the deviation flag on the case | CAP-P3-007 | — |
| FEAT-WKM-07 | Show escalation state on the case | CAP-P3-007 | — |
| FEAT-WKM-08 | Show the full case record view with the history timeline | CAP-P3-009 | — |
| FEAT-WKM-09 | Show queue history on the case | CAP-P3-009 | — |
| FEAT-WKM-10 | Reallocate when an owner is unavailable | CAP-P3-008 | — |
| FEAT-WKM-11 | Reallocate when the caseload cap is breached | CAP-P3-008 | — |
| FEAT-WKM-12 | Run the Epic 2 release checklist and go-live readiness | CAP-P3-020 | — |
| FEAT-CWC-27 | Show the next action and its due date on a case | CAP-P3-010 | — |
| FEAT-CWC-28 | Set the next action from the routing rules | CAP-P3-010 | — |
| FEAT-CWC-29 | Accept a queue placement from a model or an agent | CAP-P3-011 | Flag off until a consumer is approved (GAP-1560) |

**Not carried from the FSD P3.** FEAT-CHO-10 (automated EFS file load) is removed by D-RCV-35 and has no requirement here. A2.49 (Epic 2 release checklist) is carried as CAP-P3-020.

### 5.3 Requirements coverage check

The BRD trace (Program v5 §11) assigns 48 live requirement rows to RWB-SVC-P3: the 20 REQ-CWC, the 10 REQ-CHO and the 16 REQ-WKM rows of module 5.3, plus REQ-DRI-010 and REQ-DRI-011 from module 5.2. All 48 are covered by a capability.

| Requirement group | Rows | Covered by |
|---|---|---|
| REQ-CWC-001 to REQ-CWC-020 | 20 | CAP-P3-001 to CAP-P3-016, CAP-P3-020 |
| REQ-CHO-001 to REQ-CHO-010 | 10 | CAP-P3-001, CAP-P3-017, CAP-P3-018, CAP-P3-024 |
| REQ-WKM-001 to REQ-WKM-016 | 16 | CAP-P3-006, CAP-P3-009 to CAP-P3-011, CAP-P3-021, CAP-P3-023 |
| REQ-DRI-010, REQ-DRI-011 | 2 | CAP-P3-012, CAP-P3-013 |

**Coverage gaps.** One requirement has no story behind it: REQ-WKM-010 (capacity view, Could, EP07) is assigned to this service by the BRD trace but has no P3 slice in the wave plan (GAP-1553). No other requirement assigned to this service is without a capability.

**Delivered across two services.** Two requirements need a second half in another service's PRD: REQ-CHO-009 (payment matching, half held by rwb-payment; GAP-1563) and REQ-S7-008 (case closure, half held by rwb-writeoff; GAP-1554).

## 6. Functional requirements

Priorities are the BRD priorities of the requirement behind the FR. "Wave" is the release slice of §10; a second wave in brackets names the slice that completes the requirement.

| FR | Requirement | CAP | BR (REQ) | FSD reference | MoSCoW | Wave |
|---|---|---|---|---|---|---|
| FR-P3-001 | The service issues a case number in the form RW-YYYY-NNNNNN when a case is created, once and never reused, and the same number appears on every letter and document produced for the case. | CAP-P3-001 | REQ-CWC-002 | FEAT-CWC-01; BR-P3-001; AC-P3-001-01 (FSD) | Must | 1 |
| FR-P3-002 | The service creates one case for every account that reaches 90 or more days past due and is not excluded, from the eligible population of the completed ACE business date, and creates no case before the ACE batch for that business date is complete. | CAP-P3-001 | REQ-CWC-001, REQ-CHO-004 | FEAT-CWC-04, FEAT-CHO-04; BR-P3-004, BR-P3-030; AC-P3-004-01 (FSD) | Must | 1 |
| FR-P3-003 | One case covers one customer and one product; every account and party of that customer and product is linked to the case by its business key, with no foreign key into ACE, and the total outstanding at entry is the sum of the linked account balances. | CAP-P3-001 | REQ-CWC-003 | FEAT-CWC-02; BR-P3-002; AC-P3-002-01 (FSD) | Must | 1 |
| FR-P3-004 | The exclusion rules for deceased, fraud, bankruptcy, an active restructure plan and an open dispute are held as data and applied at creation; a blocked account gets no case and an exclusion record that carries the account, the reason, the rule ID and the rule version. | CAP-P3-002 | REQ-CWC-004 | FEAT-CWC-05; BR-P3-005; AC-P3-005-01 (FSD) | Must | 1 |
| FR-P3-005 | Case creation is idempotent: a repeated run for the same business date creates no second case and issues no second case number for the same account. | CAP-P3-001 | REQ-CWC-001 | FEAT-CWC-04; BR-P3-004; AC-EXC-P3-001-01 (FSD) | Must | 1 |
| FR-P3-006 | When the ACE batch for a business date is not complete, case creation does not start for that date, the last complete business date stays in use, the gap is visible on the case list and the alert goes to the data steward; creation starts when the batch-complete event for that date arrives. | CAP-P3-001 | REQ-CWC-001 | FEAT-CHO-05; BR-P3-031; AC-P3-031-01 (FSD) | Must | 1 |
| FR-P3-007 | A case holds exactly one state at a time, built from the stage, the status within the stage, the route and the deviation flags, and every state change is made by a rule and recorded with the rule ID and the rule version; an internal or administrative correction is made only through the administration interface with a reason code. | CAP-P3-003 | REQ-CWC-005 | FEAT-CWC-03; BR-P3-003; AC-P3-003-01 (FSD) | Must | 1 |
| FR-P3-008 | Roles, teams, queues, queue membership, the caseload cap and the capacity per queue are held as versioned reference data with valid from, valid to, author and approver, and a change takes effect without a code release. | CAP-P3-004 | REQ-CWC-006, REQ-ACA-002 | FEAT-CWC-06; BR-P3-006; AC-P3-006-01 (FSD) | Must | 1 |
| FR-P3-009 | The allocation rule table reads product, region, exposure band, stage, route, deviation flag, customer segment and collateral type, applies the first matching row and always has a default row; the queue of a new case is decided by that table and not by a person. | CAP-P3-005 | REQ-CWC-007, REQ-CWC-008 | FEAT-CWC-07; BR-P3-007; AC-P3-007-01 (FSD) | Must | 1 |
| FR-P3-010 | The assignment engine gives each allocated case exactly one owner, by round robin, lowest load or a named owner for continuity, respects the caseload cap and uses the overflow queue when no rule matches. | CAP-P3-005 | REQ-CWC-009 | FEAT-CWC-08; BR-P3-008; AC-P3-008-01 (FSD) | Must | 1 |
| FR-P3-011 | No case is left without a queue and an owner: when no allocation rule matches, the case goes to the overflow queue, the allocation-failure event is published and a task is raised for the team manager. | CAP-P3-005 | REQ-CWC-007, REQ-CWC-009 | FEAT-CWC-09; BR-P3-009; AC-P3-009-01 (FSD) | Must | 1 |
| FR-P3-012 | Cases move between queues and roles by the transfer rule table on stage change, route decision, timer expiry, deviation raised or cleared, approval needed, document received, payment missed and manual request with a reason code, and every move records the rule ID and the rule version that caused it. | CAP-P3-006 | REQ-CWC-010, REQ-CWC-016 | FEAT-CWC-10; BR-P3-010; AC-P3-010-01 (FSD) | Must | 1 |
| FR-P3-013 | An authorised user moves a case to another queue or reassigns it to another owner only with a reason code from the agreed list; the transfer rules are checked, the state and the clocks are kept and the move is on the case history. | CAP-P3-006 | REQ-WKM-003, REQ-WKM-007 | FEAT-WKM-03, FEAT-WKM-04; BR-P3-040, BR-P3-041; AC-P3-040-01 (FSD) | Must | 1 (interface), 2 (screen) |
| FR-P3-014 | A service level per queue and status, with warning and breach thresholds and an escalation target, is held as data; the clock starts when the case enters a state from the timer table and the current due date is visible on the case. | CAP-P3-007 | REQ-CWC-011 | FEAT-CWC-11; BR-P3-011; AC-P3-011-01 (FSD) | Must | 1 |
| FR-P3-015 | A warning or a breach escalates to the role named in the timer table, publishes the timer-breach event and does not move the case; a breach is never silent. | CAP-P3-007 | REQ-CWC-011, REQ-WKM-004 | FEAT-CWC-13; BR-P3-013; AC-P3-013-01 (FSD) | Must | 1 |
| FR-P3-016 | The prescription date is set at case creation from the legal periods reference table, is visible at all times, and never pauses for a deviation, a hold or a transfer. | CAP-P3-007 | REQ-CWC-012 | FEAT-CWC-12; BR-P3-012; AC-P3-012-01 (FSD) | Must | 1 |
| FR-P3-017 | The daily rebalance moves unassigned cases and over-capacity cases to another owner inside the team before the working day starts, keeps the state and the clocks and records the reason. | CAP-P3-008 | REQ-CWC-015, REQ-WKM-007 | FEAT-CWC-17, FEAT-WKM-10, FEAT-WKM-11; BR-P3-017, BR-P3-047, BR-P3-048; AC-P3-017-01 (FSD) | Must | 1 |
| FR-P3-018 | Queue depth, ageing, the spread across owners and the count of service level breaches are calculated from the case record and published for the case list and for reporting, and reconcile to the case list without unexplained variance. | CAP-P3-008 | REQ-CWC-015, REQ-WKM-006 | FEAT-CWC-18; BR-P3-018; AC-P3-018-01 (FSD) | Must | 1 |
| FR-P3-019 | The case list shows every case in the user's scope with the case number, account, product, stage, status, route, owner, queue, age in state, breach flag, balance and days past due; the account columns come from the source-data contract by business key; the list can be filtered by queue, team, stage, route, status and age and exported, and work allocated to a partner appears in the same queue view as internal work. | CAP-P3-009 | REQ-RDF-007, REQ-WKM-001, REQ-WKM-002, REQ-WKM-011 | FEAT-CWC-19, FEAT-WKM-01, FEAT-WKM-02; BR-P3-019, BR-P3-038, BR-P3-039; AC-P3-019-01 (FSD) | Must | 1 (list), 2 (filters, export, team queues) |
| FR-P3-020 | The case record view shows the case number, the accounts and parties, arrears, owner, queue, stage, status, route, the timers with their due dates, the prescription date, the contact history, the documents and the decisions on one screen, read only in this slice, and loads within the response target for a case with 50 documents. | CAP-P3-009 | REQ-OCC-007, REQ-WKM-005 | FEAT-WKM-05, FEAT-WKM-08; BR-P3-042, BR-P3-045; AC-P3-045-01 (FSD) | Must | 1 |
| FR-P3-021 | The case record view carries a history timeline of every state change, transfer, contact, document and decision in time order, with filters, and shows the queue and transfer history with the reason for each move. | CAP-P3-009 | REQ-OCC-008, REQ-WKM-008, REQ-WKM-014 | FEAT-WKM-08, FEAT-WKM-09; BR-P3-045, BR-P3-046; AC-P3-046-01 (FSD) | Must | 2 |
| FR-P3-022 | An open deviation is visible on the case record view and in every queue view with its owner and its start date, pauses the stage clock, keeps the prescription clock running and does not replace the case state. | CAP-P3-007 | REQ-DVH-002, REQ-DVH-006, REQ-WKM-005 | FEAT-WKM-06; BR-P3-043; AC-P3-043-01 (FSD) | Must | 2 |
| FR-P3-023 | Every open case carries one next action (what has to happen, who owns it, the date it is due), taken from the rule that moved the case into its current state and not entered by hand as a matter of course; it is visible on the case and in every queue view; an overdue next action raises the same escalation as a service level breach without moving the case; a case with no next action is reported as an exception. | CAP-P3-010 | REQ-WKM-012, REQ-WKM-013, REQ-WKM-014, REQ-WKM-015, REQ-WKM-016 | FEAT-CWC-27, FEAT-CWC-28; BR-P3-050, BR-P3-051; AC-P3-050-01 (FSD) | Must | 2 |
| FR-P3-024 | A caller that is not a person may place a case on a queue with the case, the score, the priority and the reason; the queue's allocation, caseload and permission rules still apply, the caller runs under a service identity, the placement is refused for an unapproved caller or a closed case, and the placement is logged with the caller and the model version; the interface ships behind a feature flag with a removal date and the placement sits in the same queue order as rule-allocated work. | CAP-P3-011 | REQ-CWC-017, REQ-CWC-018, REQ-CWC-019, REQ-CWC-020, REQ-ACA-010 | FEAT-CWC-29; BR-P3-052; AC-P3-052-01 (FSD) | Must | 2 |
| FR-P3-025 | Every limit, threshold, timer, name and rule switch a business person may change is a versioned parameter row with a type, a default, an owner, the environments it applies to and where it is used; no such value is written in code, and a change takes effect without a release. | CAP-P3-012 | REQ-DRI-010, REQ-CWC-011 | FEAT-CWC-22, FEAT-CWC-25; BR-P3-022, BR-P3-025; AC-P3-022-01 (FSD) | Must | 1 |
| FR-P3-026 | Every reference table is served to the engines with its version, valid from and valid to, author and approver, so that a decision can record which version it used. | CAP-P3-013 | REQ-DRI-011, REQ-CWC-006 | FEAT-CWC-23; BR-P3-023; AC-P3-023-01 (FSD) | Must | 1 |
| FR-P3-027 | A rule version is loaded through a validated template that checks the schema, overlapping rows, unreachable rows, a missing default and a set of test cases, and runs a dry run against live cases before it takes effect; a failed check blocks the load. | CAP-P3-014 | REQ-CWC-013, REQ-CWC-014 | FEAT-CWC-14; BR-P3-014; AC-P3-014-01 (FSD) | Must | 1 |
| FR-P3-028 | A rule version is rolled back to the previous version by one call, and every decision keeps the version that was in force when it was taken. | CAP-P3-014 | REQ-CWC-013 | FEAT-CWC-15; BR-P3-015; AC-P3-015-01 (FSD) | Must | 1 |
| FR-P3-029 | A rule change report states who changed what, when, under which version and with what effect, for audit. | CAP-P3-014 | REQ-CWC-013 | FEAT-CWC-16; BR-P3-016; AC-P3-016-01 (FSD) | Must | 2 |
| FR-P3-030 | Every state change, allocation, assignment, transfer and timer is written as an event with the rule ID and the rule version that caused it, and a decision record reaches the central ledger through the decision service; nothing moves unless the record and the state commit together. | CAP-P3-015 | REQ-CWC-016 | FEAT-CWC-21; BR-P3-021; AC-P3-021-01 (FSD) | Must | 1 |
| FR-P3-031 | An administration interface moves, reassigns and corrects a case with a reason code before any screen exists, applies the same rules as the screens and records the caller and the reason. | CAP-P3-016 | REQ-WKM-003, REQ-CWC-005 | FEAT-CWC-20; BR-P3-020; AC-P3-020-01 (FSD) | Must | 1 |
| FR-P3-032 | The case carries the contact and promise history of the account before day 90 and the ACE plan status, both read through the source-data contract, is created or updated so that it is current the morning after the account changes, and the Workbench is the system of record for case state after hand-over. | CAP-P3-017 | REQ-CHO-001, REQ-CHO-002, REQ-CHO-003, REQ-CHO-005, REQ-DRI-013 | FEAT-CHO-01, FEAT-CHO-02, FEAT-CHO-03; BR-P3-027, BR-P3-028, BR-P3-029; AC-P3-027-01 (FSD) | Must | 2 |
| FR-P3-033 | A treatment record exists for every offer made to a customer, holding its type, terms, approval and outcome; plan timers run from the treatment record, and a missed payment raises an event; the stage 2 data products for contracts, plans and treatments are supplied from the case data before the first treatment goes live. | CAP-P3-018 | REQ-CHO-006, REQ-CHO-007, REQ-RDF-014 | FEAT-CHO-06, FEAT-CHO-09; BR-P3-032, BR-P3-035; AC-P3-032-01 (FSD) | Must | 2 |
| FR-P3-034 | A plan submitted for credit approval and the terms booked in the core system are recorded on the case; the booking is confirmed from the next business date's account data through the source-data contract, and a missing booking raises a task. | CAP-P3-018 | REQ-CHO-008 | FEAT-CHO-07, FEAT-CHO-08; BR-P3-033, BR-P3-034; AC-P3-033-01 (FSD) | Must | 2 |
| FR-P3-035 | A duplicate case for the same customer and product merges into the earlier case, carrying its documents and its decision log, and the merged case can no longer receive work. | CAP-P3-001 | REQ-CHO-010 | FEAT-CWC-02; BR-P3-002; no FSD acceptance criterion (GAP-1561) | Should | 2 |
| FR-P3-036 | Audit queries the decision history of a case, a decision, a period or an approver, and receives the inputs, the versions, the approver and the final call, read through the decision service contract. | CAP-P3-019 | REQ-DRI-012 | FEAT-CHO-11; BR-P3-037; AC-P3-037-01 (FSD) | Must | 2 |
| FR-P3-037 | Every feature flag the service uses carries an owner, the environments it applies to and the date it must be removed, and the release is not declared ready until the release checklist, the training and the readiness items for the release are complete. | CAP-P3-020 | REQ-CWC-019 (flag), BR-P3-026, BR-P3-049 | FEAT-CWC-26, FEAT-WKM-12; AC-P3-026-01 (FSD) | Should | 2 |
| FR-P3-038 | The case moves to closed once its retention class has run and no action is open; the closure records the record class, the date, the reason and the rule applied, the case leaves the working list without losing its history, and a reopening needs a written rule, a reason and an approver supplied by the write-off service. | CAP-P3-022 | NFR-031, REQ-S7-008 | FEAT-WOF-13; BR-057 and RULE-022 in the Epics 3 to 8 BRD (GAP-1554, GAP-1555) | Must | 4 |
| FR-P3-039 | A capacity view shows inflow by product, bucket and region against the available capacity of each queue and team. | CAP-P3-023 | REQ-WKM-010 | No FSD feature (GAP-1553) | Could | 4 |
| FR-P3-040 | Case, queue, ageing, breach and turnaround measures are published from the case record for the steering dashboard and the baseline, and reconcile to the case list; the dashboard itself is built by the reporting service. | CAP-P3-021 | REQ-WKM-006, REQ-WKM-009 | FEAT-CWC-18; BR-P3-018; AC-P3-018-01 (FSD) | Must | 2 |
| FR-P3-041 | For every case the payment matched to the plan, the settlement or the fee is visible on the case, and a payment that matches nothing is listed as an exception for the case owner with the data it arrived with; the matching outcome is read from the payment service and the matching rule is not held here. | CAP-P3-024 | REQ-CHO-009 | FEAT-CHO-06 (plan timers), no matching feature in FSD P3 (GAP-1563) | Must | 2 |

### 6.1 Out of scope for this service

1. Collections work before day 90, decisions D1 to D4, dialer and messaging channels, core bank booking, restructure affordability calculation, partner systems and changes to bank policy (BRD §1.2). These are reached through the interfaces of the owning service or of ACE.
2. The interaction ledger, the document store, the decision log store, the rule registry, the notification path and the delegation of authority table. Each is owned by another service and read or written through its contract.
3. The read of the ACE database. The service holds no view, no copy and no staging table (GAP-1549; ASM-2686).
4. The screens of another service and the reporting dashboards. This service supplies the data and the measures.

## 7. Non-functional requirements

Each NFR carries the program NFR it derives from. Where the program target is open, the row says so and no value is invented.

### 7.1 Performance and capacity

| NFR | Requirement | Target | Source | Status |
|---|---|---|---|---|
| NFR-P3-001 | The case store holds one case per customer and product for every account at 90 or more days past due across Mortgage, Hire Purchase and SSME. | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts a month | BRD NFR-001 | Proposed from the volume forecast |
| NFR-P3-002 | The service supports the peak number of staff users signed on at once. | About 370 staff online in the busiest hour, of 914 named users | BRD NFR-002 | Proposed from the volume forecast |
| NFR-P3-003 | A screen of this service responds within its target under normal load. | Under 2 seconds | BRD NFR-008 | Proposed |
| NFR-P3-004 | The case record view loads for a case with 50 documents. | Under 2 seconds | BRD NFR-009 | Proposed |
| NFR-P3-005 | A rule evaluation at a routing decision completes inside the user's wait. | Under 300 milliseconds per rule evaluation at the 95th percentile | BRD NFR-011 | Proposed, DL11 |
| NFR-P3-006 | A search across cases returns within its target. | Under 3 seconds across cases | BRD NFR-012 | Proposed, DL11 |
| NFR-P3-007 | The case list is available on the latest completed ACE business date and states that business date and the load time behind it. | Available by 07:00 | BRD NFR-013 | Proposed, DL43 |
| NFR-P3-008 | A missing, failed or late ACE batch is visible on the case list and alerts the data steward; the service runs no load window, catch-up job or staging table of its own. | Visible at the start of day on the ACE business date; no Workbench load | BRD NFR-014, NFR-015 | Proposed, DL43 |
| NFR-P3-009 | The case list reconciles to the ACE account data daily. | No unexplained variance; tolerance per data product under DL25 | BRD NFR-018 | Proposed, DL25 |
| NFR-P3-010 | The daily rebalancing completes before the working day starts. | Complete by 07:00 | BRD NFR-019 | Proposed, DL11 |

### 7.2 Availability, resilience and recovery

| NFR | Requirement | Target | Source | Status |
|---|---|---|---|---|
| NFR-P3-011 | The service is available during business hours. | 99.9 percent in business hours | BRD NFR-020 | Proposed |
| NFR-P3-012 | The service is available outside business hours, when the daily run and the timers run. | 99.5 percent outside business hours, excluding the change window | BRD NFR-021 | Proposed, DL11 |
| NFR-P3-013 | The recovery point and recovery time objectives of the case store and its event stream are the ACE objectives. | The ACE recovery point objective and the ACE recovery time objective (value not set) | BRD NFR-022, NFR-023 | Open, DL11 (GAP-1556; ASM-2687) |
| NFR-P3-014 | An outage of a model or an agent falls back to the rule result and the case still routes. | Fallback always on | BRD NFR-024 | Proposed |
| NFR-P3-015 | A production release rolls back by redeploying the previous tag. | Rollback by previous tag | BRD NFR-027 | Proposed |

### 7.3 Auditability and traceability

| NFR | Requirement | Target | Source | Status |
|---|---|---|---|---|
| NFR-P3-016 | Every decision taken through this service is reproducible from the log, including the rule, model, agent and prompt versions and the inputs used. | Every decision reproducible | BRD NFR-033 | Proposed |
| NFR-P3-017 | Every action carries the rule version applied and the approver who allowed it. | Every action | BRD NFR-034 | Proposed |
| NFR-P3-018 | The decision log hash chain is checked daily and a break is reported to Compliance the same day. | Daily check, same-day report | BRD NFR-035 | Proposed |
| NFR-P3-019 | A model or agent write to a queue is logged with the model or agent version, on the same terms as a decision taken by a person. | Every write | BRD NFR-078 | Proposed |
| NFR-P3-020 | Business measures per decision are produced from the decision log and not from a separate count. | From the log | BRD NFR-065 | Proposed |

### 7.4 Security, privacy and compliance

| NFR | Requirement | Target | Source | Status |
|---|---|---|---|---|
| NFR-P3-021 | Party identifiers are masked at rest in the case store and on every screen and every agent call, by role. | Masked at rest and in use | BRD NFR-039 | Proposed |
| NFR-P3-022 | Each screen and each agent receives only the personal data it needs. | Data minimisation per screen and per agent | BRD NFR-040 | Proposed |
| NFR-P3-023 | Every read of the case store is logged. | Every read | BRD NFR-042 | Proposed |
| NFR-P3-024 | No production data is used in the development environment, and the user acceptance environment uses masked copies. | Synthetic in development, masked in user acceptance | BRD NFR-045 | Proposed |
| NFR-P3-025 | Every data product of this service carries a data classification, and the classification sets its handling. | Classification scheme to be applied | BRD NFR-047 | Open, DL26 (ASM-2688) |
| NFR-P3-026 | Staff authenticate with single sign-on and multi-factor authentication; agents run under service identities and are subject to the same role checks as people. | Entra ID single sign-on with multi-factor; service identities | BRD NFR-049, NFR-051 | Proposed |
| NFR-P3-027 | Secrets are held in the key store and never in code, configuration files or prompts; data is encrypted at rest and in transit. | No secrets in code or prompts; encrypted | BRD NFR-052, NFR-053 | Proposed |
| NFR-P3-028 | Workbench data, including the case store, stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | BRD NFR-046 | Proposed |
| NFR-P3-029 | Case records carry a retention and archive rule by record class, and a case closes after its retention period. | Period not set | BRD NFR-031 | Open, DL26 (GAP-1555; ASM-2694) |
| NFR-P3-030 | A party or legal hold stops deletion and expiry for the case it covers, for as long as it is in place. | Hold overrides retention | BRD NFR-072 | Proposed |

### 7.5 Usability, language and devices

| NFR | Requirement | Target | Source | Status |
|---|---|---|---|---|
| NFR-P3-031 | Screen labels, validation messages and error messages are available in Thai and in English. | Every screen, label and message in Thai and English | BRD NFR-059 | Proposed, DL10 |
| NFR-P3-032 | Screens meet the bank's accessibility standard. | WCAG 2.1 level AA for every screen | BRD NFR-060 | Proposed, DL11 (GAP-1556) |
| NFR-P3-033 | Screens work on the browsers and versions the bank supports. | The current and previous major versions of Microsoft Edge and Google Chrome | BRD NFR-061 | Proposed, DL11 |

### 7.6 Observability and operations

| NFR | Requirement | Target | Source | Status |
|---|---|---|---|---|
| NFR-P3-034 | Logs, traces and metrics are produced across the case workflow, the rule evaluation and the case router. | Across all three | BRD NFR-064 | Proposed |
| NFR-P3-035 | Every scheduled job and event-started run of this service has a run book, monitoring and an alert to the operations channel, and a failing run alerts a named owner. | Alert within 15 minutes to the named owner | BRD NFR-067, NFR-068 | Proposed, DL11 |

### 7.7 NFR coverage note

Every program NFR that names this service's behaviour is carried above. The program NFRs that belong to another service (document intake, notification, ledger, reporting extract) are not restated (ASM-2683).

## 8. Data requirements

The service owns 15 entities in its own schema; the list is the ownership map's P3 table set. No entity is shared with another service, and no link to an ACE record is a foreign key.

**Classification** is proposed per entity from its content, pending the DL26 scheme (BRD NFR-047; GAP-1555; ASM-2688). **Retention** is stated as the variable that sets it; no period is set in the sources (BRD NFR-031; ASM-2694).

| Entity | Key fields | Classification (proposed) | Source of the values | Retention |
|---|---|---|---|---|
| Recovery case | Case number (RW-YYYY-NNNNNN), primary person key, product, stage, status, route, entry date, service level state, prescription date, freshness date of the source data used | [PII] for the person key; [SENSITIVE_FINANCIAL] for arrears, exposure and balance totals | Created by the service; person and product facts from the source-data contract | Set by record class under DL26 |
| Case to account link | Case number, account key, primary account flag, balance at entry | [SENSITIVE_FINANCIAL] | Source-data contract; the key is held locally | Follows the case |
| Case to party link | Case number, person key, role (borrower, guarantor, co-borrower), contact key | [PII] | Source-data contract; the key and role are held locally | Follows the case |
| Case entry exclusion | Account key, exclusion reason, rule ID, rule version, business date | [SENSITIVE_FINANCIAL] | Created by the service at case creation | Follows the case |
| Assignment | Case number, queue, owner role, assignment date, rule ID, rule version, reason | [CONFIDENTIAL] | Created by the service | Follows the case |
| Queue | Queue code, name, team, role, product scope, region scope, capacity, overflow flag, status | [CONFIDENTIAL] | Reference data | Versioned; old versions retained for the audit of the decisions that used them |
| Queue member | Queue code, role, capacity share, valid from, valid to | [CONFIDENTIAL] | Reference data | Versioned, as above |
| Queue measure | Queue code, business date, depth, ageing bucket, spread across owners, breach count | [CONFIDENTIAL] | Calculated by the service | Set by record class under DL26 |
| Task | Task ID, case number, action, owner role, due date, state, source rule ID | [CONFIDENTIAL] | Created by the service | Follows the case |
| Timer | Timer ID, case number, queue, state, start time, due time, warning time, escalation role, state | [CONFIDENTIAL] | Created by the service; the clock is a durable timer in the workflow, this entity is the screen projection | Follows the case |
| Parameter catalog entry | Parameter code, name, type, default, owner, environments, used by, status | [CONFIDENTIAL] | Loaded through the configuration interface | Versioned history retained for audit |
| Parameter value | Parameter code, environment, value, version, author, approver, valid from, valid to | [CONFIDENTIAL] | Loaded through the configuration interface | Versioned history retained for audit |
| Reference data row | Table code, row code, attributes, valid from, valid to, author, approver, version | [CONFIDENTIAL] | Loaded through the reference-data interface | Versioned history retained for audit |
| Reference data version | Table code, version, status (draft, verified, in force, rolled back), author, approver, effective date | [CONFIDENTIAL] | Loaded through the reference-data interface | Versioned history retained for audit |
| List of values | List code, value code, label in Thai and English, order, valid from, valid to | [PUBLIC] (codes and labels only, no personal or financial content) | Loaded through the reference-data interface | Versioned, as above |

### 8.1 Data the service reads and does not hold

| Data | Held by | How this service reads it |
|---|---|---|
| Account, customer, contact, relation, collateral, collections history, plan, payment, credit decision, batch status | ACE database, read only through rwb-source-data (P1) | Through the source-data contract, with the ACE business key held locally (GAP-1549; ASM-2686) |
| Interaction ledger of the case | rwb-source-data (P1) | Through the ledger read contract of P1 (Template and Rules §R3 default ruling, DP-18) |
| Decision records and the rule registry | rwb-decision (P7) | Through the decision contract and the decision-record topic |
| Delegation of authority limits, roles and masking policy | rwb-access (P4) | Through the authorise contract |
| Documents and their metadata | rwb-document (P5) | Through the document contract and the document events |

### 8.2 Data quality and referential integrity

1. Every business key on a case entity resolves to a record in the source contract; a key with no record is reported, not silently kept (BRD NFR-018, REQ-RDF-007).
2. The case list reconciles to the ACE account data daily, and every break carries a reason visible to the data product owner (BRD NFR-018).
3. Every case entity records the freshness date of the source data it was built from (BRD NFR-013, NFR-014).
4. No personal data is written to an event, a workflow input or a log (Template and Rules §R7.2 guardrails; BRD NFR-040).

## 9. Integration points

The service's own contract is HTTP REST under /api/recovery/case/v1, its topic is rwb.case.events.v1 and its Temporal task queue is rwb-case in namespace rwb-recovery (Template and Rules §R4; Architecture v5 slide 41). Protocol and owner are known; the operation-level contract is published by the service contract work and is not restated here.

| Peer | Direction | What crosses | Protocol | Owner | Note |
|---|---|---|---|---|---|
| rwb-source-data (P1) | Inbound | Eligible accounts for the business date, account and customer facts, freshness and the business-date-ready trigger | REST and Kafka (AceDataReady) | P1 | The only read path to ACE data (GAP-1549; ASM-2686) |
| rwb-source-data (P1) | Inbound and outbound | Interaction ledger entries for the case, and the case timeline read | REST | P1 | The ledger is P1's under the default ruling; this service writes and reads through its contract |
| rwb-access (P4) | Inbound | Authorisation decision for a user or a service identity, and the delegation limit for an approval | REST, cached in the service | P4 | No role or limit table of its own |
| rwb-decision (P7) | Outbound | Decision record for every state change, allocation, transfer and timer | Kafka, topic rwb.decision-record.v1 | P7 | The record is written locally with the state and sealed centrally by P7 (Template and Rules DP-03, DP-22) |
| rwb-decision (P7) | Inbound | Rule package in force for the packages this service evaluates | Kafka and REST | P7 | The registry is P7's; the service holds the evaluated copy (DP-04) |
| rwb-deviation (S8) | Inbound | Deviation raised and deviation cleared | Kafka, topic rwb.deviation.events.v1 | S8 | Pauses and resumes the stage clock and does not replace the state |
| rwb-valuation (S1) | Inbound | Route decided | Kafka, topic rwb.valuation.events.v1 | S1 | Moves the case by the transfer rules; starts the stage child workflow |
| rwb-payment (P8) | Inbound | Payment missed, treatment booked, proceeds matched | Kafka, topic rwb.payment.events.v1 | P8 | Signals the case workflow through the case router |
| rwb-treatment (S2) | Inbound | Treatment closed and the stage outcome | Kafka, topic rwb.treatment.events.v1 | S2 | Closes the stage child and moves the case |
| rwb-asset (S5), rwb-debtsale (S6), rwb-writeoff (S7) | Inbound | Asset taken on, asset sold, lot awarded, accounts transferred, write-off approved | Kafka, the owner's topic | S5, S6, S7 | Moves the case and closes the route |
| rwb-guarantee (S3) | Inbound | Guarantee claim outcome | Kafka, topic rwb.guarantee.events.v1 | S3 | Closes the stage child |
| rwb-litigation (S4) | Inbound | Judgment recorded, auction result | Kafka, topic rwb.litigation.events.v1 | S4 | Closes the stage child |
| rwb-partner (S9) | Inbound | Partner result submitted | Kafka, topic rwb.partner.events.v1 | S9 | Moves the case by the transfer rules |
| rwb-document (P5) | Inbound | Document stored, document fields extracted | Kafka, topic rwb.document.events.v1 | P5 | Moves the case when a document arrives; the case shows the document |
| rwb-comms (P6) | Inbound | Notice delivered | Kafka, topic rwb.comms.events.v1 | P6 | Moves the case when the transfer rule names a delivery |
| rwb-agent (P10) | Outbound and inbound | Case created for screening, and a queue placement from a model or an agent | Kafka and REST | P10 | The placement is behind the dated flag (GAP-1560) |
| rwb-reporting (P9) | Outbound | Case and queue events for the projections and the measures | Kafka | P9 | One-way; the service does not call the report |
| gateway-bff | Inbound | Screen composition and the case summary that the shared ACE case view reads | REST | Platform edge (RWB-PLT-EDGE) | One hop from the edge; the service is called in parallel with the source-data service |
| ACE sign-in and the ACE notification path | Outbound, indirect | Sign-in and group-to-role, and the notification channel | Through rwb-access and rwb-comms | ACE common module | The service calls neither directly |

**Open integration questions.** The Tier 2 ACE additions are behind a flag (DL43, GAP-1557). The team that owns the list and reference-load interface paths is recorded as P3 under the default ruling, against the API specification (GAP-1558; ASM-2689). The operation-level contract for each row is an open question in §12.

## 10. Release slicing proposal

Slices follow the wave map of Template and Rules §R5.6, the wave and release table of BRD Program v5 §10.3 and the release plan of BRD Program v5 §8. Every date is tentative (Template and Rules §U7; ASM-2684).

| Wave | Business epics in the wave | Release (tentative) |
|---|---|---|
| 0 | Platform and non-functional | Before EP01, November 2026 |
| 1 | EP01 | 30 November 2026 |
| 2 | EP02, EP03 | 31 December 2026 and 31 January 2027 |
| 3 | EP04, EP05 | 28 February 2027 and 31 March 2027 |
| 4 | EP06, EP07, EP08 | 30 April 2027, 31 May 2027 and 30 June 2027 |

### 10.1 Wave 1 — EP01, 30 November 2026 (tentative)

**Theme.** Foundation 1: one case for every account at 90 days past due, one list, one record view, allocation and transfer by rule, timers and prescription dates, and the reference data that makes the rules changeable.

| CAP | Capability | Why it is in the first slice |
|---|---|---|
| CAP-P3-001 | Case creation and entry at 90 days past due | Nothing else exists without a case; the epic release is measured on the reconciled case list |
| CAP-P3-002 | Exclusion rules as data | A case created for an excluded account is a conduct and data defect from day one |
| CAP-P3-003 | Case state model | The state is the anchor of the list, the timers and the transfer rules |
| CAP-P3-004 | Roles, teams, queues and capacity as data | Allocation, transfer and the escalation targets all read it |
| CAP-P3-005 | Allocation and assignment by rule | The epic outcome is "nobody allocates cases by hand" |
| CAP-P3-006 | Transfer rules and manual transfer | Hand-offs are the second source of manual work after allocation |
| CAP-P3-007 | Service levels, timers, escalation and prescription dates | The epic outcome is "no case waits past its limit unseen" |
| CAP-P3-008 | Daily rebalancing and queue measures | Keeps the queues balanced and visible without a screen for it |
| CAP-P3-009 | Case list and case record view (read only) | The two screens the epic releases |
| CAP-P3-012 | Parameter catalog and configuration service | Every later rule and timer depends on a value that is not in code |
| CAP-P3-013 | Reference data service | The same, for the tables the engines read |
| CAP-P3-014 | Rule version authoring, validation and rollback | A rule change must reach production without a code release from the first release |
| CAP-P3-015 | Workflow event log and decision record | Every allocation and transfer must be reconstructable from the first release |
| CAP-P3-016 | Workflow administration interface | Lets the operations team correct a case before the workflow screens exist |

**Wave 1 FRs.** FR-P3-001 to FR-P3-020, FR-P3-025 to FR-P3-028, FR-P3-030 and FR-P3-031, with the interface part of FR-P3-013 and the list part of FR-P3-019.

**Wave 1 conditions.** The features that read the ACE Tier 2 additions stay behind their dated feature flags until DL43 is answered (GAP-1557; ASM-2690). RPO and RTO are not baselined until DL11 is answered (NFR-P3-013).

### 10.2 Wave 2 — EP02 (31 December 2026) and EP03 (31 January 2027), tentative

**Theme.** Foundation 2: one owner and a timer on every case, the full history on one screen, the next action, the hand-over from collections, the treatment record, the payment and outcome exception, and the model or agent queue write.

| CAP | Capability | Why it is in the second slice |
|---|---|---|
| CAP-P3-010 | Next action on every open case | The epic outcome is that a case owner never has to work out what a case needs |
| CAP-P3-011 | Queue write from a model or an agent | Analytical output must reach a queue the day it is made; built dark behind the dated flag |
| CAP-P3-017 | Hand-over from collections and plan status | The case must carry what happened before day 90 before a route decision can be trusted |
| CAP-P3-018 | Treatment record, plan timers, credit pack and booking confirmation | Epic 2 opens the treatment path; every plan needs a record and a confirmed booking |
| CAP-P3-019 | Decision log query for audit | The first audit cycle after the first release needs a query, not a report request |
| CAP-P3-020 | Release control and go-live readiness | The dated flag rule and the release checklist come into force with the second release |
| CAP-P3-021 | Measures for the steering dashboard | The steering dashboard is released with this epic and reads these measures |
| CAP-P3-024 | Payment and outcome exception on the case | A plan that is not being paid is the first thing a case owner must see; the matching itself arrives from rwb-payment (GAP-1563) |

**Wave 2 FRs (EP02).** FR-P3-021 to FR-P3-024, FR-P3-029, FR-P3-032 to FR-P3-037, FR-P3-040 and FR-P3-041, with the screen part of FR-P3-013 and the filters, export and team queue part of FR-P3-019.

**EP03 delivery item in this window.** Check encumbrance and eligibility before negotiation (slice RWB-P3-E3013-APP, planned 31 January 2027). It carries no requirement row (GAP-1562) and the split plan labels it wave 3 against an EP03 release date in the wave 2 window (GAP-1559).

**Wave 2 condition.** The queue write interface is switched on only when a consumer is approved (GAP-1560; ASM-2692).

### 10.3 Wave 3 — EP04 (28 February 2027) and EP05 (31 March 2027), tentative

| Item | Slice | Note |
|---|---|---|
| Record proof of delivery on a notice | RWB-P3-E5002-APP, planned 31 March 2027 | Carries no requirement row (GAP-1562); the notice itself belongs to rwb-comms |

No new capability is introduced in wave 3 beyond this delivery item, because the route, guarantee, litigation and debt sale capabilities of EP04 and EP05 belong to the stage services and reach this service as events.

### 10.4 Wave 4 — EP06 (30 April 2027), EP07 (31 May 2027) and EP08 (30 June 2027), tentative

| CAP | Capability | Slice | Note |
|---|---|---|---|
| CAP-P3-022 | Case closure after the retention period | RWB-P3-E6025-APP, planned 30 April 2027 | Needs the record classes from DL26 (GAP-1555) and the split with rwb-writeoff, which holds the closure rule and the reopening approval (GAP-1554) |
| CAP-P3-023 | Capacity view | No slice | REQ-WKM-010 is a Could for EP07 and the BRD trace assigns it to this service, but no P3 story exists (GAP-1553) |
| — | Route the write-off population to the committee and schedule it | RWB-P3-E6017-APP, planned 30 April 2027 | Carries no requirement row (GAP-1562); the committee decision stays with rwb-writeoff |
| — | Data quality and reconciliation console | RWB-P3-AD019-APP, planned 30 June 2027 | Carries no requirement row (GAP-1562); the reconciliation duty belongs to rwb-source-data |

### 10.5 Slicing rationale

1. The first slice carries everything a case needs to exist, be owned, be measured and be corrected, because the EP01 outcome is a single trusted case list and no manual allocation.
2. The second slice carries everything a person needs on the case to act without asking, because the EP02 outcome is one owner, one timer and one history on one screen.
3. Nothing in the first two slices depends on the Tier 2 ACE additions being accepted; where it does, the feature is flag-gated (GAP-1557).
4. The wave 3 and wave 4 items are either delivery items whose requirements are thin (REQ-S7-008, NFR-031) or absent (GAP-1562), so they do not change the product baseline of the first two waves.
5. The wave of a slice is the wave of its business epic (BRD Program v5 §10.3), which is why the EP03, EP05, EP06 and EP08 items fall where they do.

## 11. Acceptance criteria and validation evidence

Each criterion is testable as written. The evidence column names the artefact that proves it; the test cases themselves belong to the backlog and test design stages.

| AC | Requirement | Criterion | Source | Evidence |
|---|---|---|---|---|
| AC-P3-001 | FR-P3-001 | Given an account reaching 90 days past due with no exclusion and the last case number issued in 2026 being RW-2026-000122, when the entry rule runs, then the case number RW-2026-000123 is issued once, the same number is printed on every letter and document of the case, and the number is never issued again | AC-P3-001-01 (FSD) | Component test on the number sequence; contract test on the retrieval of the number |
| AC-P3-002 | FR-P3-002, FR-P3-006 | Given the ACE batch for business date 2026-12-02 is not complete, when the daily run fires, then no case is created for that date, the case list shows the last complete business date with the stale state, the data steward is alerted, and the cases for 2026-12-02 are created when the batch-complete event for that date arrives | AC-EXC-P3-001-02 (FSD); NFR-P3-007, NFR-P3-008 | Integration test against a simulated batch-complete event; alert check |
| AC-P3-003 | FR-P3-003 | Given a customer with two hire purchase accounts at 95 days past due, when the entry rule runs, then one case exists for that customer and product with both accounts linked by account key, the borrower is linked by person key, and the total outstanding at entry is the sum of the two balances | AC-ALT-P3-001-02 (FSD) | Component test; data check on the case and its links |
| AC-P3-004 | FR-P3-004 | Given an account at 92 days past due with the plan flag set, when the entry rule runs, then no case is created and one exclusion record exists with the account key, the reason, the exclusion rule ID and the rule version in force | AC-ALT-P3-001-01 (FSD) | Component test; exclusion register query |
| AC-P3-005 | FR-P3-005 | Given a case was created for an account on 2026-12-01, when the run repeats for 2026-12-01, then the account has one case link and no second case number is issued | AC-EXC-P3-001-01 (FSD) | Component test on a repeated run |
| AC-P3-006 | FR-P3-007 | Given a case in one state, when it moves, then exactly one state is in force after the move, the previous state is on the history, and the move records the rule ID and the rule version that caused it | AC-P3-003-01 (FSD) | Component test; decision record check |
| AC-P3-007 | FR-P3-008 | Given a new queue and a new caseload cap in the reference data, when the reference load is verified and put in force, then the new queue and cap are used by the next allocation with no release, and the previous version stays readable | AC-P3-006-01 (FSD) | Reference load test; allocation test |
| AC-P3-008 | FR-P3-009, FR-P3-010 | Given the case creation run has completed, when the morning allocation run finishes before 07:00, then every new case has one queue and one owner, no case is above the caseload cap, and the assignment of each case states the rule and version used | AC-P3-007-01 (FSD); NFR-P3-010 | End-to-end run on a dated data set; queue measure check |
| AC-P3-009 | FR-P3-011 | Given a new case whose product and region match no allocation row except the default, when the allocation run finishes, then the case is in the overflow queue, the allocation-failure event is published and a task exists for the team manager | AC-P3-009-01 (FSD) | Component test; event contract test |
| AC-P3-010 | FR-P3-012 | Given a case in a stage, when the route is decided, then the case moves to the queue and role the transfer rule names, the reason is recorded, and the rule ID and version are on the decision record and on the case history | AC-P3-010-01 (FSD) | Component test; history check |
| AC-P3-011 | FR-P3-013 | Given an authorised user and a reason code from the agreed list, when the user transfers a case, then the case moves, the state and the clocks are unchanged and the reason is on the history; when the reason code is absent, the transfer is refused and nothing changes | AC-P3-040-01 (FSD) | UI and contract test; negative test |
| AC-P3-012 | FR-P3-014 | Given the timer table for a queue and status, when a case enters the state, then the clock starts, the due date and the warning date match the table, and the due date is visible on the case | AC-P3-011-01 (FSD) | Component test; timer projection check |
| AC-P3-013 | FR-P3-015 | Given a case whose breaching timer fires, when the timer runs, then the escalation goes to the role named in the table, the breach event is published and the case is in the same state as before | AC-P3-013-01 (FSD) | Component test; negative state check |
| AC-P3-014 | FR-P3-016 | Given a legal period in the reference data, when the case is created, then the prescription date is set from it and the date does not change when a deviation opens or the case is transferred | AC-P3-012-01 (FSD) | Component test; clock test with a deviation |
| AC-P3-015 | FR-P3-017 | Given an owner above the caseload cap and an unassigned case, when the daily rebalance runs, then the case moves to an owner inside the team, the state and the clocks are kept, the rebalance completes by 07:00 and the reason is on the case | AC-P3-017-01 (FSD); NFR-P3-010 | End-to-end run; timing check |
| AC-P3-016 | FR-P3-018 | Given the case list and the queue measures for the same business date, when both are read, then the depth, ageing and breach count per queue agree and any difference is explained by a recorded reason | AC-P3-018-01 (FSD) | Reconciliation check |
| AC-P3-017 | FR-P3-019 | Given a team manager, when the case list is opened, then each row shows case number, account, product, stage, status, route, owner, queue, age in state, breach flag and days past due, the account columns match the source-data contract, and the list can be filtered and exported | AC-P3-019-01 (FSD), AC-P3-039-01 (FSD) | UI test; contract test on the account columns |
| AC-P3-018 | FR-P3-020 | Given a case with 50 documents, when the case record view is opened, then it shows the case number, accounts, parties, arrears, owner, queue, stage, status, route, the timers with due dates, the prescription date, the contact history, the documents and the decisions, in read-only state, and it loads under 2 seconds | AC-P3-045-01 (FSD); NFR-P3-004 | Performance test; UI test |
| AC-P3-019 | FR-P3-021 | Given a case with state changes, transfers, contacts, documents and decisions, when the timeline is read, then every item is present, in time order, and can be filtered; the queue history shows each move with its reason | AC-P3-046-01 (FSD) | UI test on a seeded case |
| AC-P3-020 | FR-P3-022 | Given an open deviation on a case, when the case record view and every queue view are read, then the deviation is visible with its owner and start date, the stage clock is paused, the prescription clock has kept running and the case state has not changed | AC-P3-043-01 (FSD) | Component test; clock test |
| AC-P3-021 | FR-P3-023 | Given an open case, when it is read, then it carries one next action with an owner and a due date produced by the rule that moved it; when the due date passes, the escalation fires and the case does not move; when a case has no next action, it appears as an exception; a next action is not entered by hand as a matter of course | AC-P3-050-01 (FSD); REQ-WKM-013, REQ-WKM-016 | Component test; exception report check |
| AC-P3-022 | FR-P3-024 | Given an unapproved caller, when it places a case on a queue, then the answer is a rejection and nothing changes; given a closed case, the answer is a conflict and nothing changes; given an approved caller under a service identity, the placement is accepted and the decision record holds the caller, the model version, the score, the priority and the reason | AC-P3-052-01 (FSD), AC-EXC-P3-052-01 (FSD), AC-EXC-P3-052-02 (FSD) | Contract tests; decision record check |
| AC-P3-023 | FR-P3-025, FR-P3-026 | Given a parameter or a reference row changed through the validated load, when the next decision is taken, then it uses the new value and records the version, and no release was needed | AC-P3-022-01 (FSD), AC-P3-023-01 (FSD) | Reference load test; decision record check |
| AC-P3-024 | FR-P3-027 | Given a rule version with an overlapping row, an unreachable row or a missing default, when it is loaded, then the load is refused with the failing check named and the version in force is unchanged; a dry run against live cases is produced before a valid version takes effect | AC-P3-014-01 (FSD) | Load test per failure class; dry-run report check |
| AC-P3-025 | FR-P3-028 | Given two rule versions in force in turn, when a rollback is requested, then the previous version is in force again in one call, and decisions taken before the rollback still record the version they used | AC-P3-015-01 (FSD) | Component test; audit check |
| AC-P3-026 | FR-P3-030 | Given an allocation, a transfer and a timer breach, when each happens, then an event with the rule ID and version is published, a decision record exists locally and in the central ledger, and a failure to record leaves nothing changed | AC-P3-021-01 (FSD); NFR-P3-016, NFR-P3-018 | Event contract test; failure injection test |
| AC-P3-027 | FR-P3-031 | Given an administration caller with a reason code, when a case is moved, reassigned or corrected, then the same rules apply as on a screen, the caller and the reason are recorded, and a call without a reason code is refused | AC-P3-020-01 (FSD) | Contract test; negative test |
| AC-P3-028 | FR-P3-032 | Given an account that reaches 90 days past due on the previous business date, when the case is read the next morning, then the case carries the contact and promise history of the account and the ACE plan status, and the case is current for that business date | AC-P3-027-01 (FSD) | Integration test with a dated data set |
| AC-P3-029 | FR-P3-033, FR-P3-034 | Given a plan submitted for approval and booked terms that are absent from the next business date's account data, when the booking confirmation runs, then a task is raised for the officer and the absence is visible on the case | AC-P3-033-01 (FSD), AC-P3-034-01 (FSD) | Component test; task check |
| AC-P3-030 | FR-P3-035 | Given a second case for the same customer and product, when the merge runs, then the earlier case survives with the documents and the decision log of both, and the merged case can no longer receive work | No FSD criterion (GAP-1561) | Component test; data check on documents and decisions |
| AC-P3-031 | FR-P3-036 | Given an internal audit request by case, decision, period or approver, when it is made, then the decision history is returned with inputs, versions, approver and final call, read through the decision service contract | AC-P3-037-01 (FSD) | Contract test on a seeded population |
| AC-P3-032 | FR-P3-037 | Given a flag in use, when the flag register is read, then the flag carries an owner, its environments and the date it must be removed, and the release is not marked ready until the checklist is complete | AC-P3-026-01 (FSD); REQ-CWC-019 | Flag register check; release checklist |
| AC-P3-033 | FR-P3-038 | Given a case whose retention class has run and which has no open action, when the closure runs, then the case moves to closed, the record class, the reason and the rule are recorded, the case leaves the working list with its history intact, and a reopening is refused without a written rule, a reason and an approver | NFR-P3-029; REQ-S7-008; GAP-1555 | Component test on a dated data set; negative test on reopening |
| AC-P3-034 | NFR-P3-021, NFR-P3-022 | Given a user role, when the case record and the queue views are read, then personal identifiers are masked as the role requires and only the personal data the screen needs is returned | BRD NFR-039, NFR-040; REQ-ACA-005 | Security test per role; response inspection |
| AC-P3-035 | NFR-P3-024 | Given the development and user acceptance environments, when their data is inspected, then the development environment holds no production data and the user acceptance environment holds masked copies | BRD NFR-045 | Environment data audit |
| AC-P3-036 | NFR-P3-031, NFR-P3-032 | Given a screen of this service, when it is read in Thai and in English, then every label, validation message and error message is present in both, and the screen meets the accessibility standard | BRD NFR-059, NFR-060 | Localisation and accessibility test |
| AC-P3-037 | FR-P3-041 | Given a case with a plan, a settlement and a fee, when a payment matched to the plan and a payment that matches nothing are read, then the matched payment is visible against the plan on the case, the unmatched payment appears as an exception for the case owner with the data it arrived with, and no matching rule is applied in this service | REQ-CHO-009; GAP-1563 | Contract test with a matched and an unmatched payment; exception list check |

### 11.1 Validation evidence by stage

| Evidence | What it proves | Produced by |
|---|---|---|
| Component and contract test results | FR behaviour at the service boundary, including the negative cases | Build stage of the service epic |
| Integration test results on a dated data set with simulated ACE batch events | The freshness, hand-over and reconciliation behaviour | Integration stage, with the P1 and P9 harnesses |
| Performance test results at the volumes of NFR-P3-001 and NFR-P3-002 | Response and rule-evaluation targets | Non-functional test stage |
| Decision record and event samples | NFR-P3-016 to NFR-P3-020 | Audit stage, checked with Compliance |
| Reference load, dry-run and rollback records | FR-P3-027, FR-P3-028 and the rule governance of the center of excellence | Change record of the rule load |
| Flag register and release checklist | FR-P3-037 and the dated flag rule | Release record |
| Environment data audit | NFR-P3-024 | Pre-release control |
| Role-based masking test | NFR-P3-021, NFR-P3-022 | Security review |

## 12. Open questions

**Carried from the BRD and the program decisions.** These are open in the source documents and are not answered here. The program decisions keep their DL numbers; the open question the Epics 3 to 8 BRD raises on retention and masking is carried as Q-012 there and as OQ-P3-005 and OQ-P3-006 here.

| ID | Question | Owner role | Carried from |
|---|---|---|---|
| OQ-P3-001 | Does the ACE team accept the RWB-ACE-001 scope (14 tables, 12 columns, 80 source fields) and its dates, so the Tier 2 features can leave their flags? | ACE team lead | DL43; GAP-1557 |
| OQ-P3-002 | What are the recovery point and recovery time objectives for the case store and its event stream? | IT lead with Operational risk | DL11; NFR-P3-013 |
| OQ-P3-003 | What is the maximum time a case may stay in each state before it escalates, and who is the escalation target per queue? | Business lead | DL22 |
| OQ-P3-004 | What is the most cases one person may hold, and how is a queue ordered within a priority class? | Product owner | DL23 |
| OQ-P3-005 | How long is each case record class kept, and what is archived at closure? | Compliance | DL26; Q-012 (Epics 3 to 8 v1); GAP-1555 |
| OQ-P3-006 | Which fields are masked for which role on the case list and the case record view? | Compliance with security | DL26; Q-012 (Epics 3 to 8 v1); NFR-P3-021 |
| OQ-P3-007 | What is the Thai name for each field, label and message on the case screens? | Business lead with Legal and Compliance | DL10 |
| OQ-P3-008 | Does a case enter at 90 or 91 days past due, and is the entry rule one number for every product? | Business lead | DL16; REQ-CHO-004 |
| OQ-P3-009 | Which interfaces need same-day data, given that the case list and the hand-over run on the completed ACE batch? | Solution architect | DL06; NFR-P3-007 |

**Raised by this PRD.** Each is recorded as a candidate gap or assumption in the registers.

| ID | Question | Owner role | Register |
|---|---|---|---|
| OQ-P3-010 | Does P3 read ACE data through the source-data contract, as Arch v5 requires, or through the views as FSD P3 A1.5 states? | Solution architect | GAP-1549; ASM-2686 |
| OQ-P3-011 | What does a closed case keep: the full record, a summary or a handle to an archive, and who may read a closed case? | Compliance | GAP-1554; GAP-1555; NFR-P3-029 |
| OQ-P3-012 | Who owns the five list and reference-load interface paths, P3 by the default ruling or P4 by the API specification? | Solution architect | GAP-1558; ASM-2689 |
| OQ-P3-013 | Which model or agent is approved to write to a queue, and what is the removal date of that flag? | AI product owner | GAP-1560; ASM-2692 |
| OQ-P3-014 | How does a duplicate case merge behave across documents and the decision log, and who may trigger it? | Case owner | GAP-1561; ASM-2691 |
| OQ-P3-015 | Is the capacity view (REQ-WKM-010) built in wave 4 for EP07, or retired? It has a requirement row and no story | Capacity and workforce planner | GAP-1553; ASM-2693 |
| OQ-P3-016 | Should the EP03 encumbrance slice carry the wave 2 label, given that BRD Program v5 releases EP03 on 31 January 2027? | Program manager | GAP-1559 |
| OQ-P3-017 | What requirement backs the proof-of-delivery slice, the committee routing slice and the reconciliation console? | Product owner | GAP-1562; ASM-2695 |
| OQ-P3-018 | Is the PRD approved by the Product Owner and the FDA, and on which date? | Product owner; FDA | GAP-1550; ASM-2680 |
| OQ-P3-019 | Which document version is authoritative for P3, given the file name and the document control block disagree? | Business analyst, P3 | GAP-1551 |
| OQ-P3-020 | Which half of REQ-CHO-009 does each service own: the matching rule in rwb-payment or the exception on the case here? | Solution architect | GAP-1563; ASM-2696 |
| OQ-P3-021 | Which half of REQ-S7-008 does each service own: the closure rule, the reason and the approver in rwb-writeoff or the case state change here? | Solution architect | GAP-1554; ASM-2685 |

## 13. Approval

This table is left empty. The PRD is Draft and no approval has been recorded (ASM-2680).

| Role | Decision | Date |
|---|---|---|
| Product Owner | | |
| FDA | | |
