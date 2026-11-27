# RWB-P7-E2004-APP Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: new rwb-decision story, the decision and rules slice of RWB-E2-004. It holds the RESTRUCTURE catalogue rows the plan timers read and the plan-timer decisions in the central ledger; the treatment entity, the case route state, the timer and the DP04 product stay with their owners. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2004-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 36 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E2004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not set; the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P7-S |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2004-CON |
| Contract version | v1 (the /v1 path of the REST operations in section 12.1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CHO-006, REQ-CHO-007, REQ-RDF-014, REQ-CWC-011) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **centre of excellence analyst (RW-COE)** who owns the rule package, and as an **internal auditor (RW-AUDIT)** who reads the log, I want **the catalogue rows of R-RES-25 and R-RES-27 of package RESTRUCTURE served from `rwb_decision` by rule ID and package version, and the plan-timer decisions of a case held as hash-chained entries of the central ledger**, so that **every plan timer a case runs can be explained from the row and the version that made it, no service reads this service's tables to find the timer specification, and no plan timer runs under a version that was never in force**.

Inside `rwb-decision` this is the decision and rules slice of the legacy key: base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1`, shared topic `rwb.decision-record.v1`, queue `rwb-decision`, schema `rwb_decision`, Java package `th.co.scb.ace.workbench.recovery.decision` (DP-13, DP-14, DP-01).

Three things are built here. The first is the catalogue read: one rule row of package RESTRUCTURE is answered at one package version with its action text, owner role, timer specification, target queue code and outputs, so the plan step of rwb-case applies the timer row it was given and never reads `rule_row`. The second is the version gate: a row is served only at a version that is IN_FORCE on the business date, and a business date with no version in force is a refusal, never a default. The third is the ledger: the plan-timer decisions of the case arrive as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and become one hash-chained `decision_log_entry` per case and business date, carrying rule ID "R-RES-25" or "R-RES-27" and version "RES-2026.12" (DP-03, DP-09).

What is deliberately not here is the evaluation. The KieBase, the first-match semantics and the 300 ms budget stay in the embedded kit of the owning service (DP-04, ADR-017); this service holds no evaluator, no working memory and no agenda, and it serves rows, states and ledger entries. The treatment row and its lifecycle are rwb-treatment's; the case route state, the task, the timer record and the plan-timer step that consumes `rwb.treatment.TreatmentApproved.v1` and `rwb.payment.PaymentMissed.v1` are rwb-case's (RWB-P3-E2004-APP); the DP04 extract is rwb-source-data's.

The legacy facts are unchanged: package RESTRUCTURE version "RES-2026.12" carries rows R-RES-25 and R-RES-27, the plan moves the case to PLAN_RUNNING and a missed installment starts the cure period in PLAN_CURE_PERIOD, the case status stays IN_PROGRESS through both moves, and an entry of the log cannot be altered once it is written.

### 2. Business rationale

Legacy RWB-E2-004 promised that every approved plan has a record and a clock, and that each plan decision names the rule and the package version that made it, so the plan can be explained afterwards. In the target that promise is spread across services: the treatment and its terms are rwb-treatment's, the route state and the timer are rwb-case's, and the authority of the rule and the proof of the decision are this service's.

Both mechanisms changed in the same way, and each fails quietly. A rule is no longer a table read from a shared schema: governance is central here and the evaluation is local in the one service that owns the model, so the owning service reads the row it applied through the catalogue answer and holds no grant on `rwb_decision` (DP-04, ADR-017). The decision log is no longer one table written by one writer: each service writes a local record in its own transaction and announces it, and the central ledger here collects it (DP-03, ADR-022). A plan can therefore run a timer with no row that explains it, or leave a ledger that names a version this service never had in force, and the case still looks correct on the screen.

This story closes both gaps for package RESTRUCTURE and its two plan rules. One catalogue read serves the row at the version the evaluation returned, so the timer specification the plan step applies is the approved one and cannot be an older, a superseded or an unchecked one. One ledger collection turns the two plan decisions of a case into entries that name the rule and version "RES-2026.12", carry the treatment identifier and the target route state, and cannot be edited afterwards, so an auditor reads why a plan timer exists without asking four services for it.

It meets REQ-CHO-006, REQ-CHO-007 and REQ-RDF-014 on the record and registry side, and REQ-CWC-011 on the warning the plan rows carry. The treatment entity, its terms, its booking and its outcome stay with rwb-treatment; the plan-timer step, the route state and the timer stay with rwb-case; the DP04 product stays with rwb-source-data; the cross-service proof of the plan journey is the wave 2 harness of RWB-ITG-E2004-ITG.

### 3. Preconditions

- RWB-P3-E2004-CON is published: the timers read, the case read with its route state, the shape of `rwb.case.CaseStateChanged.v1` and `rwb.decision-record.DecisionRecorded.v1`, and its fakes (DP-11). This story builds against that baseline and its fake.
- The `rwb_decision` baseline is in place from the service template: the schema, `decision_log_entry`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the outbox and inbox objects of DP-09, and the append-only trigger and chain columns of RWB-P7-E1008-APP.
- RWB-PLT-E1027-CON is published: the record shape, the envelope on `rwb.decision-record.v1`, the idempotency key and the transaction rule. How the business date travels in that envelope, and the field names that carry the treatment identifier, the timer specification identifier and the target state, are Not specified in the source documents (GAP-2473; ASM-4105).
- Package RESTRUCTURE is loaded, tested and approved with version "RES-2026.12" and rows R-RES-25 and R-RES-27, each carrying its action text, owner role, timer specification, target queue code and outputs (RWB-P7-E2042-APP, RWB-P7-E1073-APP). This story serves, gates and records that version; it loads none of it.
- LOV-DECISION and the version-state list LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED are in force and are read through the reference-data contract of DP-07; no list value is written in this service's code.
- The synthetic facts of the tests: case "RW-2026-000201" with product group "MORTGAGE", status "IN_PROGRESS" and route state "BOOKED_IN_ALS_NLEADS"; entry "DLE-9001" recording the approval of a restructure at level "L4" by user "U-APR-01"; CURE_PERIOD_DAYS of 30 calendar days and `plan.warn-days` of 3; a TDR plan of 36 installments, offer amount 850000.00 baht and first due date 2026-12-31; case "RW-2026-000202" in route state "WITH_FCR_OFFICER"; case "RW-2026-000203" with status "CLOSED"; and the business date 2026-12-01.
- A caller of the catalogue read holds a model-owner service identity, and a reader of the ledger holds Decision log R (TSD P7 T6.1). The authorisation answer is the cached permission decision the template holds from rwb-access; DP-08 is not in this slice's pattern set and this story adds no guard of its own.

### 4. Flow

1. Package RESTRUCTURE version "RES-2026.12" is IN_FORCE from its valid-from date, with rows R-RES-25 and R-RES-27 and their catalogue columns.
2. The plan-timer step of rwb-case consumes `rwb.treatment.TreatmentApproved.v1` for case "RW-2026-000201" and evaluates R-RES-25 in its own embedded kit; on a missed installment it evaluates R-RES-27 the same way.
3. The owning service reads the applied row: `GET /api/recovery/decision/v1/rule-catalog/R-RES-25?packageVersion=RES-2026.12` answers the action text, owner role, timer specification, target queue code and outputs of the row at that version, and nothing else.
4. rwb-decision answers only when "RES-2026.12" is IN_FORCE on the business date of the call; otherwise the answer names the package code, the version label and its state, or MSG-P3-027 when no version is in force, and no row is served.
5. The owning service writes the local decision record, the new route state, the timer and the outbox row in one transaction in `rwb_case`, so `rwb.decision.DecisionRecorded.v1` leaves on `rwb.decision-record.v1` keyed by the case ID with decision code, final call, rule ID "R-RES-25", rule version "RES-2026.12", inputs reference, actions and actor.
6. rwb-decision: `PlanTimerRecordIngest` consumes the record through the inbox, deduplicating on the event identifier and again on the case and the business date, and hands it to `PlanTimerRecordValidator`.
7. rwb-decision: `LedgerAppender` appends one `decision_log_entry` with the decision code and final call the record names, `rule_id` "R-RES-25", `rule_version` "RES-2026.12", the inputs snapshot naming the treatment identifier, the treatment type, the first due date 2026-12-31 and 36 installments, the actor and the decided time, and an actions payload holding the timer specification identifier and the target state "PLAN_RUNNING"; the chain columns come from the ledger's chain.
8. rwb-decision: the R-RES-27 record of business date 2027-01-01 arrives the same way and is appended the same way, with the target state "PLAN_CURE_PERIOD"; the two plan decisions of one case never share an entry and never overwrite one.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A rule ID is requested at a version that is not IN_FORCE | Refused; the answer names the package code, the version label and its state, and serves no row | MSG-P3-027 naming the version state | AC2 |
| X2 | No version of the package is IN_FORCE on the business date | Refused with the package code and the business date only; the owning service stops the step before it touches a case | MSG-P3-027 with {check} "no package in force" | AC2 |
| X3 | A record carries a rule ID and an empty rule version, or a decision code outside LOV-DECISION | Refused; nothing appended; one incident raised with the case ID and the missing field | MSG-P7-009 naming the field | AC3 |
| X4 | The same record arrives twice, or the plan step repeats for a date | One entry for the case and the business date; the first entry ID is answered and the repeat is counted | None | AC4 |
| X5 | The ledger store cannot take the append | Nothing appended, `chain_seq` not consumed, the record waits in the producer's outbox, the caller is answered and one incident is raised | MSG-P7-003 | AC5 |
| X6 | A row requested at a version whose stored artifact does not match its SHA-256 | Refused by the registry before the catalogue answer; no row served; one incident for the version | None | AC6 |

A version that is not in force is never a default: where nothing is servable the owning service stops the plan step with NoPackageInForce and this service serves no older, superseded or unchecked row in its place. The retired timer path is not an exception either: no five-minute check and no timer-due event is built or restored here (GAP-2476; ASM-4110).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the `rwb_decision` baseline, the registry rows of RWB-P7-E2042-APP, the envelope of RWB-PLT-E1027-CON and the fake of RWB-P3-E2004-CON; it evaluates no rule and calls no service except the list read of DP-07 |
| Negotiable | Nothing business is fixed in code: the package code, the rule rows, the version, the timer specifications, the cure period and the warning days are rows and parameters of their owners |
| Valuable | No plan timer runs under a row this service never approved, and every plan decision of a case is one entry that names the rule and the version |
| Estimable | One read, one ingest, one validator, one appender and one gate |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Each criterion in section 7 is one automated test against the registry fixture, the record fixture and the list fake, with a controlled clock |

### 7. Acceptance criteria

```gherkin
Feature: Treatment entity and plan timers data model, the RESTRUCTURE catalogue and the plan-timer ledger

  Background:
    Given the business date is 2026-12-01
    Given case "RW-2026-000201" with product group "MORTGAGE", status "IN_PROGRESS" and route state "BOOKED_IN_ALS_NLEADS"
    Given decision log entry "DLE-9001" records the approval of a restructure at level "L4" by user "U-APR-01"
    Given CURE_PERIOD_DAYS for "MORTGAGE" is 30 calendar days and plan.warn-days is 3
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-25 and R-RES-27

  Scenario: AC1 The rows of R-RES-25 and R-RES-27 are served by rule ID and package version (new, D-RCV-60)
    Given the rwb-case contract mock returns the evaluation answer that names package "RESTRUCTURE" and version "RES-2026.12"
    When the plan-timer step of rwb-case calls GET /api/recovery/decision/v1/rule-catalog/R-RES-25?packageVersion=RES-2026.12
    Then the answer holds rule_id "R-RES-25", rule_version "RES-2026.12", drools_rule_name, rule_table, row_order, action_text, owner_role, timer_spec, target_queue_code and outputs
    Then the row R-RES-27 is answered the same way at version "RES-2026.12"
    Then the answer holds no DRL source, no workbook and no evaluation
    Then the shape of the answer beyond that field set is Not specified in the source documents (GAP-2473; ASM-4104)

  Scenario: AC2 Only a version in force is served, and no version in force is never a default (new, D-RCV-60)
    Given version "RES-2026.11" of package "RESTRUCTURE" is SUPERSEDED
    When the plan-timer step calls GET /api/recovery/decision/v1/rule-catalog/R-RES-25?packageVersion=RES-2026.11
    Then the call is refused and no catalogue row is served
    Then the refusal names package "RESTRUCTURE", version "RES-2026.11" and its state
    When no version of "RESTRUCTURE" is in force on the business date
    Then the call is refused with MSG-P3-027 whose {check} is "no package in force" and whose {detail} names the package code and the business date only
    Then no older, superseded or unchecked version is served in its place

  Scenario: AC3 The R-RES-25 record becomes one hash-chained entry for the case and the business date (new, D-RCV-60)
    Given the plan-timer step of rwb-case writes its local decision record for case "RW-2026-000201" on business date 2026-12-01 with rule "R-RES-25", version "RES-2026.12" and the final call it took
    Given its inputs snapshot names treatment "TRT-0001", treatment type "RESTRUCTURE", first due date 2026-12-31 and 36 installments, and its actions payload names the timer spec of the row and the target state "PLAN_RUNNING"
    When rwb.decision.DecisionRecorded.v1 for it arrives on rwb.decision-record.v1 keyed by case "RW-2026-000201"
    Then one decision_log_entry exists with rule_id "R-RES-25", rule_version "RES-2026.12", the decision code and final call the record names, the inputs snapshot, the actions payload, the actor "SY-CASEWF" and decided_at
    Then the entry carries chain_seq, prev_hash and entry_hash, and a later entry links to its entry_hash
    Then rwb_decision holds no timer, no treatment and no case attribute column beyond case_id

  Scenario: AC4 The R-RES-27 record is a further entry, and a repeat adds none (new, D-RCV-60)
    Given the R-RES-25 entry of AC3 exists for case "RW-2026-000201" and business date 2026-12-01
    When the same record arrives again with the same idempotency key
    Then exactly one entry exists for the case and the business date, the first entry ID is answered and the repeat is counted for R-UNI-40
    When the R-RES-27 record arrives for business date 2027-01-01 with rule "R-RES-27", version "RES-2026.12" and the actions payload naming the cure-period timer spec and the target state "PLAN_CURE_PERIOD"
    Then one further decision_log_entry exists with rule_id "R-RES-27" and rule_version "RES-2026.12"
    Then the rule version on the first entry stays "RES-2026.12" and is not rewritten

  Scenario: AC5 A decision whose record cannot be written does not proceed (new, D-RCV-60)
    Given the ledger store is unavailable
    When the R-RES-25 record for case "RW-2026-000201" arrives
    Then no decision_log_entry is written, chain_seq is not consumed and no partial row exists
    Then the record waits in the producer's outbox and one incident is raised to the platform administrator queue
    Then the caller is answered MSG-P7-003 and the entry count for the case stays zero

  Scenario: AC6 No rule is evaluated here and no other service reads these tables (new, D-RCV-60)
    Given the rwb_decision baseline with decision_log_entry, rule_package, rule_package_version, rule_row and rule_test_case
    When the boundary test compiles a class of this service that holds a KieBase, a working memory or an agenda
    Then the build fails
    When a component of another service opens a connection to rwb_decision
    Then the build fails and that service's login is refused the grant
    Then the plan timer is a durable timer of the workflow kit in rwb-case, TimerDue has no topic and JOB-05 has no schedule, and this service registers no Quartz job, publishes no timer-due event and schedules no timer check (GAP-2476; ASM-4110)

  Scenario: AC7 An error answer of a provided operation carries status 401, 403 or 404 (new, D-RCV-60)
    When a call to a provided operation carries no valid credential
    Then the answer has status 401
    When a call carries a valid credential that lacks the right for the operation
    Then the answer has status 403
    When the 404 trigger is Not specified in the source documents (NEWAC-RWB-P7-E2004-APP-AC15)
    Then the answer has status 404
```

The seven criteria are new and test only this deliverable: the catalogue rows and the version gate, and the plan-timer entries of the central ledger. The legacy criteria of RWB-E2-004 are owned elsewhere and are not restated: the treatment write and its refusals, the plan-timer step, the route state, the timer and the cure period are RWB-P3-E2004-APP's and rwb-treatment's, the DP04 product is rwb-source-data's, and the cross-service proof is RWB-ITG-E2004-ITG's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The ledger, the registry, the rule rows and the scenarios are `rwb-decision`'s; no other service reads `rwb_decision`, and this service reads no other service's table | Arch v5 slides 14 and 41; DP-01; default ruling on the rule package registry |
| BR2 | A row is served by rule ID and package version with its action text, owner role, timer specification, target queue code and outputs, and nothing of the evaluation travels with it | legacy BR10; D-RCV-36 T5 to T7; RWB-P3-E2004-CON consumed set |
| BR3 | A row is served only at a version IN_FORCE on the business date, and the answer carries the version label and its state | legacy BR12; R-UNI-41; D-RCV-36 T7 |
| BR4 | No rule is evaluated here: the evaluator, the first-match semantics and the 300 ms budget stay in the owning service | DP-04; ADR-017; legacy section 12 |
| BR5 | The plan decisions R-RES-25 and R-RES-27 are collected into one hash-chained `decision_log_entry` per case and business date, carrying the rule ID, the package version, the inputs snapshot, the final call, the actions and the actor | ADR-022; DP-03; FSD P7 A2.3 (GAP-2473; ASM-4105) |
| BR6 | An entry is append only and hash-chained: nothing updates or deletes it, and a correction is a new entry naming the one it corrects | FSD P7 AC-P7-001-01 and AC-ALT-P7-001-01; DF-DEC-017, DF-DEC-018, DF-DEC-028, DF-DEC-029 |
| BR7 | A decision whose record cannot be written does not proceed: nothing moves in the owning service and the ledger stays empty | legacy BR6; Principle 5; R-UNI-39; CTL-06; MSG-P7-003 |
| BR8 | A plan decision is recorded once for a case and a business date: a repeated event gives one entry and the repeat is counted | legacy BR7; R-UNI-40; DF-DEC-031 |
| BR9 | No business value is code: the cure period, the warning days, the rule rows, the version label and the timer specifications are rows and parameters of their owners | legacy BR5; DP-06, DP-07 |
| BR10 | The plan timer is a durable timer of the workflow kit inside the workflow that owns the wait; the five-minute check and the timer-due event are retired and this service replaces them with nothing | DP-10; Arch v5 slides 42 and 44; ADR-016 (GAP-2476; ASM-4110) |
| BR11 | An entry carries identifiers and facts only: the case identifier, the treatment identifier, the rule identity, the package version, the timer specification identifier and the target state, and no name, address, identity number or account number | legacy section 17; Arch v5 slide 42 note |

How the rules hold in `rwb-decision`: BR1 runs in the absence of a foreign key into another schema and in the boundary test of AC6. BR2 runs in `RuleCatalogQuery`, which maps `rule_row` into the answer and reads no `drl_source` and no workbook. BR3 runs in `RuleVersionGate`, which reads the state of the version through the registry before any row is mapped. BR4 is what the service does not contain: no evaluator, no working memory and no agenda on this queue. BR5 and BR8 run in the mapper and in the unique key on the case and the business date, so a second delivery finds the first entry. BR6 runs in the schema, where the append-only trigger refuses an UPDATE and a DELETE. BR7 runs in the order of the owning service's transaction, which is why a failed record leaves nothing moved. BR9 is the reason no period, warning day, rule ID, version label or timer specification appears in this service's Java. BR10 is the target ruling this slice states. BR11 runs in the mapper and in the log pattern of the service.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | an accepted record for a case and a business date | No entry exists for the pair | One `decision_log_entry` at the next `chain_seq`, with the rule ID, the version and the final call of the record |
| Appended | the same case and business date again | The idempotency key repeats | No change; the first entry ID is answered and the repeat counted |
| IN_FORCE | a catalogue request | The version in force carries the requested rule row | The row is served, with the version label and the row's catalogue columns |
| SUPERSEDED, LOADED, APPROVED, ROLLED_BACK or REFUSED | a catalogue request | The version is not in force | Refused, the state named in the answer, no row served |
| No version in force | a catalogue request | The business date has no version of the package in force | Refused with MSG-P3-027; nothing served and no default version used |

The case state machine is not this service's: rwb-case owns the case status, the route state, the task and the timer, and this slice changes no case state. The moves to PLAN_RUNNING and PLAN_CURE_PERIOD are the owning service's and are recorded here only as the target state in the actions payload of the entry that explains them. The six version states are named by the Temporal and Drools design; the load, the checks, the approval and the rollback that move a version between them are RWB-P7-E2042-APP's and RWB-P7-E1073-APP's, and this story owns only the gate that refuses anything not in force.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-decision service identity (SY-DECLOG) | Appends the ledger entry, serves the catalogue row at the version in force, and refuses a version that is not in force |
| SY-CASEWF, the plan-timer step of rwb-case | Reads the catalogue row through the contract, writes its local record in `rwb_case` in its own transaction and announces it; holds no grant on `rwb_decision` |
| RW-COE, centre of excellence analyst | Reads the package, its rows and its versions (Rules and parameters R) |
| RW-AUDIT, internal auditor; RW-COMPLY, Compliance and PDPA officer | Read the plan decisions of a case and their chain state (Decision log R) |
| RW-CASEOWN, case owner; RW-TEAMMGR, team manager | Read the plan decisions of their own cases in scope (Decision log R) |
| RW-RISK, risk and model risk officer | Approves each version through RWB-P7-E2042-APP; this story gates on the approval and records the decisions that use it |

The authorisation answer is the cached permission decision the template holds from rwb-access; DP-08 applies to the REST operations of section 12.1, so each read calls the rwb-access authorise check before it answers; the check's name is Not specified in the source documents (DOR-RWB-P7-E2004-APP-6). The refusals are 403 with MSG-P4-002 for a role without the right and 503 with MSG-P7-003 when the ledger cannot take the append. The role codes are rows of the role model in `rwb_access` and are not fixed in code.

### 11. Data

| BR Field ID | Table in rwb_decision | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write |
| DF-DEC-002 | decision_log_entry | case_id, a value the record carries, with no foreign key into `rwb_case` | Write |
| DF-DEC-003 | decision_log_entry | decision_code, a value of LOV-DECISION carried by the record | Write |
| DF-DEC-004, DF-DEC-005 | decision_log_entry | rule_id ("R-RES-25", "R-RES-27"), rule_version ("RES-2026.12") | Write |
| DF-DEC-008 | decision_log_entry | inputs_ref, the snapshot naming the treatment identifier, the treatment type, the first due date and the installment count | Write |
| DF-DEC-012, DF-DEC-014 | decision_log_entry | final_call, and actions holding the timer spec identifier and the target state | Write |
| DF-DEC-016, DF-DEC-030 | decision_log_entry | decided_at, actor_user_id, a service identity where a service wrote the entry (GAP-2473; ASM-4107) | Write |
| DF-DEC-017, DF-DEC-018, DF-DEC-028, DF-DEC-029 | decision_log_entry | prev_hash, entry_hash, chain_seq, corrects_entry_id | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key, the case and the business date as the record carries them | Write |
| DF-REF-002, DF-REF-003, DF-REF-296, DF-REF-297 | rule_row | rule_id, rule_version, package_version_id, drools_rule_name | Read, served in the catalogue answer |
| DF-REF-008, DF-REF-010, DF-REF-011, DF-REF-298 | rule_row | action_text, owner_role, timer_spec, outputs | Read, served as the catalogue projection |
| DF-REF-052, DF-REF-053, DF-REF-054 | rule_row | rule_table, row_order, target_queue_code | Read, served with the row |
| DF-REF-274 to DF-REF-278 | rule_package | id, package_code, title, owner_role, hit_policy | Read |
| DF-REF-279 to DF-REF-294 | rule_package_version | id, package_id, version_label, status, valid_from, valid_to, checksum and the rest, read through the version gate | Read |
| Not specified in the source documents (GAP-2473; ASM-4104) | rule_row, rule_package_version | the physical types, lengths and nullability beyond the field set above, and the wire shape of the catalogue answer | Read |

Field IDs are those of the Logical Data Model and Data Dictionary v9. `decision_log_entry.case_id` is the only case value in `rwb_decision`: no case number, product group, route state, amount, queue code or owner name column exists, and no foreign key points into another schema (DP-01). The treatment row in `rwb_treatment` is S2's and `recovery_case`, `timer` and `task` in `rwb_case` are P3's; this service holds none of them and reads the timer through no path at all, because the timer is shown from the rwb-case contract by the screen that needs it.

### 12. Contract

The base is `/api/recovery/decision/v1` (DP-13), the topic is `rwb.decision.events.v1` (DP-14), the shared topic is `rwb.decision-record.v1`, the queue is `rwb-decision`, the schema is `rwb_decision` and the Java package is `th.co.scb.ace.workbench.recovery.decision`.

#### 12.1 REST operations provided

| Method | Path | Purpose | Authorization |
|---|---|---|---|
| GET | `/rule-catalog/{ruleId}` with the query `packageVersion` | Serve one rule row of a package at one package version: rule ID, rule version, the Drools rule name, the table, the row order, the action text, the owner role, the timer specification, the target queue code and the outputs; refused unless the version is IN_FORCE on the business date | A model-owner service identity, or Rules and parameters R for a person |

The path is the one RWB-P3-E2004-CON consumes for R-RES-25 and R-RES-27 and the one the legacy `RuleCatalog.row(ruleId, packageVersion)` answers on the monolith. The Ownership Map attributes no row to it and attributes `GET /decision-log/{entryId}` to this service, which RWB-P7-E2005-APP serves; this story therefore declares one path and adds no second read (GAP-2474; ASM-4108). The shape of the answer beyond the field set above is Not specified in the source documents (GAP-2473; ASM-4104).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | rwb-case (P3), under RWB-P3-E1043-CON | LOV-DECISION and the version-state list, read by the validator and never copied into code (DP-07) | One hop, 2 s (DP-11) |

#### 12.3 Events published

None. The version-in-force announcement `rwb.decision.RulePackageInForce.v1` (event 30) belongs to the promotion and registry stories RWB-P7-E2042-APP and RWB-P7-E1073-APP; this story serves the version the announcement refreshes and publishes nothing of its own.

#### 12.4 Events consumed

| Event | Topic | From | Owner service | Used for |
|---|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | `rwb.decision-record.v1` (shared) | All 19 services; the plan-timer records of this story from rwb-case | rwb-decision (RWB-SVC-P7) | The append of `decision_log_entry`: decision code, final call, rule ID "R-RES-25" or "R-RES-27", rule version "RES-2026.12", inputs reference, actions and actor |

Consumed through an inbox that deduplicates on the event identifier and again on the case and the business date, with the retry and dead-letter topics of DP-09. The envelope is the one RWB-PLT-E1027-CON fixes; how the business date and the treatment identifier, the timer specification identifier and the target state are carried in it is Not specified in the source documents (GAP-2473; ASM-4105).

#### 12.5 Workflows and activities

None. The ingest is a listener on the queue `rwb-decision` with no workflow of its own; the daily chain check of the ledger is RWB-P7-E1008-APP's and the promotion of a version is the registry stories'.

#### 12.6 Schedules

None. This story registers no Schedule, no cron entry and no job name. The five-minute timer check JOB-05 and the timer-due event it raised are retired with the Quartz scheduler, and the plan timer is a durable timer of the workflow kit inside the workflow that owns the wait (DP-10; Arch v5 slides 42 and 44; GAP-2476; ASM-4110).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `decision_log_entry` | P7 (rwb_decision) | The ledger entry of a plan-timer decision and of every other decision announced to this service |
| `rule_package`, `rule_package_version` | P7 (rwb_decision) | The registry and its versions; read only here, through the gate |
| `rule_row`, `rule_test_case` | P7 (rwb_decision) | The catalogue and the scenarios of each version; the rows are read and served, the scenarios are not read |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |

`treatment` in `rwb_treatment` is S2 rwb-treatment's, and `recovery_case`, `timer`, `task` and `queue` in `rwb_case` are P3 rwb-case's; `dp_treatment`, `data_product` and `data_product_load` in `rwb_source_data` are P1's. None of them is read or written here (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| DecisionRecorded fixture (RWB-PLT-E1027-CON) | The consumed envelope | An accepted R-RES-25 record for 2026-12-01 and an R-RES-27 record for 2027-01-01, each with its inputs snapshot, actions and actor; a duplicate key; a record with an empty rule version; a decision code outside LOV-DECISION |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | `GET /api/recovery/case/v1/admin/lists/{listCode}` | LOV-DECISION, the version-state list LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED, and a code outside the list to prove the refusal |
| Registry fixture (RWB-P7-E2042-APP) | `rule_package`, `rule_package_version`, `rule_row` | `RES-2026.12` IN_FORCE with rows R-RES-25 and R-RES-27 and their catalogue columns, `RES-2026.11` SUPERSEDED, a version whose artifact no longer matches its SHA-256, and a date with no version in force |
| rwb-case contract fixture (RWB-P3-E2004-CON) | The published baseline | The timers and case answers and the two event envelopes, used to prove that the caller reads the catalogue row and never a timer record |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | `GET /rule-catalog/{ruleId}?packageVersion=`; `GET /admin/lists/{listCode}` for the two lists, one hop within 2 s |
| Kafka | 0 published, 1 consumed | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed by the case ID |
| Temporal | None | No workflow, no activity and no Schedule; the ingest is a listener on queue `rwb-decision` |
| File | None | No file is read or written; the workbook and the DRL stay with the registry stories |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no build dependency of its own, and the platform H rows and the C rows above are the dependencies the patterns add, held by the platform and contract stories rather than repeated in the metadata rows (GAP-2475; ASM-4109). DP-01, DP-13 and DP-15 are the target shape itself: the schema, the base and the per-service migration, which here adds one index on `rule_row (rule_id, package_version_id)` and one on `decision_log_entry (case_id, idempotency_key)` and no column carrying a case attribute. DP-03 is the record path: the owning service writes its local record with its state change, the shared topic carries it, and the ledger here collects it, with no shared table and no call into rwb-case. DP-04 is the point of the slice: governance and the catalogue are central here and the evaluation is local there, so this service serves rows and holds no KieBase, and its C row RWB-P7-E1073-CON is this service's own rule-package contract story. DP-05, DP-06 and DP-07 are prohibitions and statements: no ACE view is read, no parameter is read in this slice, and no cure period, warning day, list value or version state is written in code. DP-09 and DP-14 are the mechanism: the inbox dedupe on the record and the topic names supplied by the naming library. DP-10 is the ruling this story states rather than builds: the timer is a durable timer of the workflow kit, so this service registers no Schedule and the five-minute check is retired. DP-11 is the one 2 s hop from the plan step to the catalogue and the one for the list read. DP-19 is the gateway-bff composite route behind the screens that show the rows and the entries.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E2004-CON and RWB-PLT-E1027-CON stay green, and a SIT week shows every catalogue call answered only at a version in force with its timer specification and outputs and refused otherwise, one hash-chained entry per case and business date for R-RES-25 and R-RES-27 naming rule and version "RES-2026.12" with the treatment identifier and the target route state, no second entry for a replayed record, and no timer, evaluator or Quartz job anywhere in this service.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | The requested version is not in force, or the business date has no version in force | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P7-009 | A record is refused for a missing or invalid field | Not specified in the source documents (GAP-2473; ASM-4106) |
| MSG-P7-003 | The ledger cannot take the append | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role holds no right for the action | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" when the business date has no version in force and "version state" when the requested version is not in force; {table} is Not specified in the source documents (CG-ALL-7055); the package code and version label are not shown, and no case fact is named. MSG-P7-009 is written to the service log and the incident and is never shown to a customer; its {field} value is "ruleVersion" or "decisionCode" (GAP-2473; ASM-4106). For MSG-P4-002 the {action} value is "read the catalogue row". Every error is an RFC 9457 problem response with `messageId` and `detail` filled, and the reads answer 401 without a session, 403 for a role without the right and 503 with MSG-P7-003 when the ledger cannot take the append.

The other refusals of the legacy key keep their identifiers with the stories that own them and are not restated here: MSG-GEN-001 and MSG-GEN-003 for the treatment write and its dates, MSG-P3-005 for a case that is closed or not in the state the rule expects, MSG-P1-001 for a stale treatment data product, and MSG-P3-003 for the warning raised inside the warning period.

### 15. Screens and states

No new screen. The catalogue row is read by the plan-timer step of rwb-case, not by a person, and the rows and versions of a package are administered on SCR-39 Rules and parameters under RWB-P7-E2042-APP. States of SCR-39: empty, loading, error and no access are Not specified in the source documents (CG-ALL-7062). The plan decisions of a case are read on SCR-38 Decision log query under RWB-P7-E2005-APP, where the entries of this ledger appear with their rule, version and chain verdict; this story fills that read. States of SCR-38: loading, as Screen Specifications v1 section SCR-38 gives it; empty, error and no access are Not specified in the source documents (CG-ALL-7061). The gateway-bff composite route behind both screens is DP-19 and is built by RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-004-01 | AC1, BR2 (legacy AC1, BR1) | Component | Restructure, 36 installments, 850000.00 baht, entry DLE-9001 |
| TC-E2-004-02 | AC1, AC3, BR2, BR3, BR10 (legacy AC2, BR3, BR5, BR10, BR11) | Component | First due date 2026-12-31; clock moved past expiry |
| TC-E2-004-03 | Legacy AC3, BR8; the DP04 extract is rwb-source-data's | Component | Ten treatments over three products, two booked |
| TC-E2-004-04 | AC2, BR3 (legacy AC4, BR2) | Contract | Restructure with no first due date |
| TC-E2-004-05 | AC3, BR5 (legacy AC5, BR1) | Component | Unknown decision log entry DLE-0000 |
| TC-E2-004-06 | Legacy AC6, BR2; the date refusal is rwb-treatment's | Contract | First due date one day before the proposal |
| TC-E2-004-07 | Legacy AC7, BR9; run by RWB-P3-E2004-APP; the exception queue is rwb-case's | Component | Case in route state WITH_FCR_OFFICER |
| TC-E2-004-08 | AC4, BR8 (legacy AC8, BR7) | Component | Same TreatmentApproved event twice |
| TC-E2-004-09 | AC5, BR7 (legacy AC9, BR6) | Component | Decision log store stopped in the test container |
| TC-E2-004-10 | Legacy AC10; run by Not specified in the source documents (CG-ALL-7058), the rwb-source-data story; the extract and its stale flag are rwb-source-data's | Component | JOB-15 forced to fail on 2026-12-02 |
| TC-E2-004-11 | Legacy AC11; run by Not specified in the source documents (CG-ALL-7058), the rwb-case story; the closed-case refusal is rwb-case's | Component | Closed case |
| TC-E2-004-12 | AC4, BR5 (legacy AC12, BR4, BR10) | Component | PaymentMissed for due date 2026-12-31 |
| TC-E2-004-13 | AC2, BR3 (legacy AC13, BR12) | Component | No RESTRUCTURE version in force on 2026-12-01 |
| TC-E2-004-14 | AC6, BR10 (legacy AC14, BR11) | Component | A component that inserts into the timer table without TimerScheduler |
| TC-E2-004-15 | AC1, MSG-P4-002 (legacy Access) | Component | RW-PHONECOL, which holds no Rules and parameters right, reads the catalogue row and is refused |
| TC-E2-004-16 | AC5, BR7 (legacy Principle 5) | NFR | Decision log store stopped at the append; no entry, no state change |
| TC-E2-004-17 | Section 12.7 table boundary; DP-01 | Component | Not specified in the source documents (DOR-RWB-P7-E2004-APP-12) |
| TC-E2-004-18 | AC7 (new; no legacy counterpart) | Component | Not specified in the source documents (NEWAC-RWB-P7-E2004-APP-AC15) |

The sixteen legacy cases keep the identifiers of RWB-E2-004, TC-E2-004-17 is added in this story with no legacy counterpart, and the Level column applies the mapping of this run: the legacy System level becomes Component for a single-service test against a container with a controlled clock, Access becomes Component, and Resilience becomes NFR. Each Covers text names the legacy criterion it descends from beside the criterion of this slice, so a reader can see that the treatment, the timer, the case state and the product are asserted in their owning stories and the row, the version and the entry are asserted here. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the cure period of 30 calendar days, the `plan.warn-days` value of 3, the package code, the rows R-RES-25 and R-RES-27, the version "RES-2026.12" and the timer specifications are rows and parameters of their owners, and none of them appears in this service's Java.
- No personal data in events, workflow inputs, logs or tests: an entry carries a case identifier, a treatment identifier, a rule identity, a package version, a timer specification identifier and a target state, and no name, address, identity number or account number is written or logged. Test data uses synthetic keys.
- No cross-schema read (DP-01): `rwb_decision` reads no `rwb_case` and no `rwb_treatment` table and holds no foreign key into one, and the boundary test fails the build on a cross-schema reference.
- ACE data only through the owner's contract or `v_ace_*` views, and this service reads neither: the facts behind a row or an entry come from the registry and the record.
- No rule engine here: no KieBase, no working memory and no evaluation on this queue, so the first-match semantics stay in the owning service (DP-04, ADR-017).
- An entry is append only and is written before the state it explains: the append-only trigger refuses an UPDATE and a DELETE, a correction is a new entry naming the one it corrects, and nothing moves in the owning service when its record cannot be written.
- The retired path is never restored: no Quartz job, no job catalogue row, no five-minute timer check and no timer-due event is built here.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25; BR2 | TC-E2-004-01, TC-E2-004-04, TC-E2-004-05, TC-E2-004-06, TC-E2-004-11, TC-E2-004-15 |
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25, R-RES-27, R-UNI-39, R-UNI-40; BR4, BR5, BR7, BR10 | TC-E2-004-02, TC-E2-004-07, TC-E2-004-08, TC-E2-004-09, TC-E2-004-12, TC-E2-004-13, TC-E2-004-14, TC-E2-004-16 |
| REQ-RDF-014 | Stage 2 data products for plans and treatments exist before the first treatment | Business Requirements Epic 2, section 4; Program, section 5.1 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | None; BR1 | TC-E2-004-03, TC-E2-004-10 |
| REQ-CWC-011 | Service levels, warnings and escalation as data; a breach does not move the case | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-13 | 06 Take over and own the case | BR9 | TC-E2-004-02, TC-E2-004-12 |

The three requirements the legacy story tabulates keep their legacy BRD section and requirement text. REQ-CWC-011 is tabulated because the legacy warning rule names it and the plan rows carry the warning; its section, feature and rule text are those of the Epic 1 requirement and no requirement ID is added. This story traces all four on the catalogue and ledger side only.

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E2-004; story RWB-P7-E2004-APP; contract RWB-P3-E2004-CON; `rwb_decision` baseline | Metadata; sections 1, 3, 12 |
| Package RESTRUCTURE, rows R-RES-25 and R-RES-27, version "RES-2026.12" (legacy BR10, AC2, AC12, AC13) | Sections 1, 3, 7 (AC1, AC2), 8 (BR2, BR3), 11 |
| The catalogue columns action text, owner role, timer specification, target queue code and outputs (legacy BR10; DF-REF-008 to DF-REF-011, DF-REF-054, DF-REF-298) | Sections 1, 7 (AC1), 8 (BR2), 11, 12.1 |
| The ledger entry, the rule ID and the package version (legacy BR6, BR10, BR12; AC2, AC9, AC12, AC13) | Sections 7 (AC3 to AC5), 8 (BR5 to BR8), 9, 11, 12.4 |
| Append only and hash-chained (FSD P7 AC-P7-001-01 and AC-ALT-P7-001-01) | Sections 7 (AC3), 8 (BR6), 9, 17 |
| The retired five-minute timer check and the durable plan timer (Arch v5 slides 42 and 44; DP-10) | Sections 1, 5, 8 (BR10), 12.6, 17; recorded as GAP-2476 |
| Synthetic values: cases "RW-2026-000201" to "RW-2026-000203"; entries "DLE-9001" and "DLE-0000"; level "L4"; "U-APR-01"; 36 installments; 850000.00 baht; first due date 2026-12-31; CURE_PERIOD_DAYS 30; `plan.warn-days` 3; business date 2026-12-01 | Sections 3, 7, 16 |
| MSG-P3-027, MSG-P7-003, MSG-P7-009, MSG-P4-002 | Section 14, exception paths |
| Field IDs DF-DEC-001 to DF-DEC-031; DF-REF-002 to DF-REF-011, DF-REF-052 to DF-REF-054, DF-REF-274 to DF-REF-298 | Section 11 |
| Legacy test cases TC-E2-004-01 to TC-E2-004-16 | Section 16 |
| The other slices of RWB-E2-004 | Sections 2, 19 |

### 19. Out of scope

- The treatment entity, its terms, its booking, its outcome and its lifecycle: rwb-treatment.
- The plan-timer step, the case route state PLAN_RUNNING and PLAN_CURE_PERIOD, the task, the timer record and the durable timer of the workflow kit that holds the wait: rwb-case (RWB-P3-E2004-APP).
- The embedded Drools evaluation itself: RuleEvaluator, the first-match semantics, the KieBase cache and the 300 ms budget stay in the owning service (DP-04, ADR-017, RWB-PLT-E1072-CON).
- The load, the checks, the four-eyes approval, the promotion and the rollback of package RESTRUCTURE and its rows: RWB-P7-E2042-APP and RWB-P7-E1073-APP; this story serves, gates and records, and loads nothing.
- The version-in-force announcement and the cache refresh it triggers: the registry and promotion stories.
- The daily chain check of the ledger, the entry read and the audit export: RWB-P7-E1008-APP, RWB-P7-E1027-APP and RWB-P7-E2005-APP.
- The DP04 treatment data product and its extract: rwb-source-data.
- Payment matching that raises PaymentMissed (P8), the booking confirmation of RWB-E2-007, and broken plan handling after the cure period (R-RES-29 to R-RES-32).
- The cross-service proof of the plan journey: the wave 2 harness of RWB-ITG-E2004-ITG.
- Platform deployment, the gateway-bff composite route (RWB-PLT-N001-CON), the durable-timer behaviour of the workflow kit (RWB-PLT-E1071-CON) and the platform configuration of Kafka, Temporal and observability.
