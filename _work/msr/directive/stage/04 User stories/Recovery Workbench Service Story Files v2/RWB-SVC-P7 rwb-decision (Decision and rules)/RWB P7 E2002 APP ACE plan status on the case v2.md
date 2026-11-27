# RWB-P7-E2002-APP ACE plan status on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P7-R |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2002-CON, version v1 (the /v1 path) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-DRI-013, REQ-CHO-002) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-decision slice of RWB-E2-002, answering which version of package `RESTRUCTURE` is in force for a business date with its state, checksum and rows `R-RES-29`, `R-RES-30`, `R-RES-31` and `R-LIT-02`, and collecting the route moves a broken plan causes into one hash-chained ledger entry per case, business date and rule identity, carrying the rule, the version `RES-2026.12`, the ACE plan status and its date, the final call, the actions and the actor, read back with `chainVerified`. The plan read, the stored status, the route move, the task, the timer, the rights and the scope check stay outside this service. Secondary slice: it owns no legacy criterion. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 26 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN), a team manager (RW-TEAMMGR) and an internal auditor (RW-AUDIT)**, I want **the RESTRUCTURE version that was in force on a business date, with its checksum and the rows that decide a plan, and one hash-chained record of every route move a broken plan caused, with the rule, the version, the ACE plan status and its date**, so that **a plan that broke and the route the case took can be explained from one read the next morning, and no service can evaluate a rule version this service never promoted**.

Inside `rwb-decision`, schema `rwb_decision`, base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1`, queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`:

- The registry: `rule_package`, `rule_package_version` and `rule_row` hold package `RESTRUCTURE`, version `RES-2026.12` in force with its checksum and rows `R-RES-29`, `R-RES-30`, `R-RES-31` and `R-LIT-02`. The version answer names only a version in force; the evaluation runs in the service that owns the package (DP-04, ADR-017), so no rule, working memory or agenda lives here.
- The records: `rwb.decision.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1`, key `caseId`, carries the moves `CURE_PERIOD_EXPIRED` by `R-RES-29` and `R-RES-30` and `TREATMENT_BROKEN` by `R-LIT-02`, and is consumed idempotently into `decision_log_entry`, append only and hash-chained.
- The read: `GET /decision-log` answers the moves of a case with `chainVerified` on every entry; an entry whose link does not hold is named and never hidden. JOB-14 at 02:00 checks the chain of the business date, so a `chainVerified` value is the result of a run.

The legacy facts are unchanged: case `RW-2026-000310`, synthetic account `A-0310`, plan `TDR-SYN-0310`; version `RES-2026.12`; plan statuses `CREATED`, `APPROVED`, `BOOKED`, `BROKEN` with `SUSPENDED` the unknown code; route states `PLAN_CURE_PERIOD`, `PLAN_BROKEN`, `BACK_TO_ROUTE_DECISION`, `RESTRUCTURE_BARRED`, `LIT_ROUTE_APPROVED`, `NOTICE_GENERATED`; the 5 working days of `timer_spec`; the 2 second timeout and the batch of 500; `restructure.max_breaks` = 2. None of them is a column of this schema: the plan facts travel inside the record and the entry.

### 2. Business rationale

The legacy story promised that a case with a live plan is never treated as if it had none, that a broken plan returns to its owner the next morning, and that the rule and the version behind the move are on the record. In the target those promises sit in four services: rwb-integration reads the plan, rwb-case stores the status, evaluates the package and moves the route state with its task and timer, rwb-access holds the rights, and this service holds the authority and the proof.

Both mechanisms here fail silently when they are wrong. Rule governance is central and evaluation local (ADR-017, DP-04): a version never promoted, or an artifact whose bytes no longer match its checksum, would still be evaluated and the case would still look decided by a rule. The record is no longer one table and one writer: each service writes a local record in its transaction and announces it on `rwb.decision-record.v1` (ADR-022, DP-03), and this service collects it. A move can complete with no entry and no error, and an auditor would find a plan that broke with nothing to explain it.

This story closes both gaps: only a version in force is answered, with the checksum the caller verifies before it evaluates, and a broken plan leaves one chained entry with the rule, the version, the plan status and its date, the final call, the actions and the actor. It meets REQ-DRI-013 and REQ-CHO-002 on the rule-version and record side and serves NFR-033 and NFR-035. It is this service's part only: the plan read is rwb-integration's (RWB-P2-E2002-APP, RWB-P2-E2002-CON), the stored status, the route move, the task and the timer are rwb-case's (RWB-P3-E2002-APP), the rights and the scope check are rwb-access's, and authoring, approval and promotion are RWB-P3-E2042-APP's and RWB-P7-E1073-APP's.

### 3. Preconditions

- RWB-P2-E2002-CON is published: `GET /api/recovery/integration/v1/cases/{caseId}/plan-status` with `planRef`, `accountNo`, `status`, `statusDate`, `live` and `messageCode`, its refusals and its fake (DP-11, DP-13). This story calls it at display time and holds no copy of the plan.
- The `rwb_decision` baseline exists from the service template: schema, tables, outbox and inbox objects of DP-09, base, topic, queue and chart.
- `decision_log_entry` carries `chain_seq`, `prev_hash`, `entry_hash` and `corrects_entry_id`, the chain lock, the canonical form and the append-only trigger, and the service login holds INSERT and SELECT only (RWB-P7-E1008-APP). Its name is Not specified in the source documents (GAP-2469; ASM-4099).
- RWB-PLT-E1027-CON is published: the record shape, the `rwb.decision.DecisionRecorded.v1` envelope on `rwb.decision-record.v1`, the idempotency key and the transaction rule, with its fake.
- Version `RES-2026.12` is loaded, tested and approved with its checksum, its valid-from date and an approver who is not its author, and its four rows each carry `action_text`, `owner_role` and `timer_spec` (RWB-P3-E2042-APP, RWB-P7-E1073-APP). This story reads and answers that version and loads none of it.
- The version-state list and LOV-DECISION are in force and read as reference data (DP-07); no list value is written in code.
- The workflow kit and namespace `rwb-recovery` are provisioned, so the 02:00 check runs as a Schedule on queue `rwb-decision` (DP-10, RWB-P7-E1008-APP).
- The synthetic facts exist: plan `APPROVED` dated 2026-12-10, then `BROKEN` dated 2026-12-14, then no status, then `SUSPENDED`; business dates 2026-12-10 to 2026-12-16; `restructure.max_breaks` = 2. Readers hold Decision log R (TSD P7 T6.1); DP-08 is not in this slice's pattern set, so the story adds no guard.
- No build dependency: it builds against the published contract fake and the registry rows of RWB-P7-E1073-APP and starts on Day 1 in its lane (§R5.7).

### 4. Flow

1. Version `RES-2026.12` is in force from 2026-12-01 with its checksum in `rule_package_version` and rows `R-RES-29`, `R-RES-30`, `R-RES-31` and `R-LIT-02`.
2. On 2026-12-15 the plan-status step of rwb-case finds plan `TDR-SYN-0310` broken with date 2026-12-14, evaluates the version it fetched from this registry and moves the route state through `PLAN_BROKEN` to `BACK_TO_ROUTE_DECISION` in one transaction with its local record and outbox row (RWB-P3-E2002-APP).
3. A caller asks `GET /admin/rule-packages/RESTRUCTURE/versions`; the answer names `RES-2026.12` as the one version in force with its state, valid-from date, checksum and row count, and names no other as in force.
4. rwb-case publishes `rwb.decision.DecisionRecorded.v1` with decision code, final call `CURE_PERIOD_EXPIRED`, rule ID `R-RES-29`, rule version `RES-2026.12`, inputs reference, actions with `R-RES-30` and the state reached, and the actor.
5. `PlanStatusRecordIngest` consumes it through the inbox, deduplicating on the event identifier and again on the case, business date and rule identity.
6. `PlanStatusRecordMapper` checks the required fields and maps the record to the field groups of the ledger.
7. `MoveRecordAppender` appends one `decision_log_entry` with the rule, the version, the inputs snapshot holding `BROKEN` dated 2026-12-14, the actions holding `R-RES-30`, `PLAN_BROKEN` and `BACK_TO_ROUTE_DECISION`, the actor, the decided time and the chain columns. The status, the route state and the task stay in `rwb_case`.
8. The litigation move `TREATMENT_BROKEN` from `LIT_ROUTE_APPROVED` to `NOTICE_GENERATED` gets its own entry on its own date. A repeat appends nothing and answers the first id; a move that never happened, because the status did not change, the read timed out or no version was in force, leaves none.
9. `PlanStatusDecisionReader` answers `GET /decision-log` in `chain_seq` order with `chainVerified`, may show today's plan status beside an entry from the rwb-integration contract within 2 s, and never rewrites the entry.
10. At 02:00 JOB-14 verifies the chain of the business date, names the first break and answers `chainVerified` false from that entry on.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A version that is not in force is asked for | Refused; no rows; the answer names the package, the version and its state | None | AC2 |
| X2 | The artifact no longer matches its checksum | Refused; no rows; one incident; the state is unchanged | None | AC2 |
| X3 | The ledger cannot take the append | The append is refused and the read answers no partial page; the record waits in the producer's outbox and the ingest catches up | MSG-P7-003 | AC4, AC5 |
| X4 | The same record or the same step arrives twice | One entry for the case, date and rule identity; the first id is answered and the repeat counted | None | AC4 |
| X5 | A rule ID without a version, or an unknown decision code | Refused with the field named, nothing appended, dead-lettered after the last retry | MSG-P7-009 | AC4 |
| X6 | The chain does not hold for an entry on the page | `chainVerified` false, the page carries the warning, one incident to Compliance; the entry is never hidden | MSG-P7-012 | AC5, AC6 |
| X7 | No version in force on the business date | The owning service stops with `NoPackageInForce`; nothing is answered as in force and nothing is appended | MSG-P3-027 | AC2, AC4 |
| X8 | A role without Decision log R, or a case outside scope | Refused; nothing returned and nothing written | MSG-P4-002, MSG-P4-003 | AC5 |

A version that is not in force is never a default. The plan-side exceptions of the legacy story, the status ACE cannot give, the unknown code, the timeout and the batch of 500, belong to rwb-integration and rwb-case and are proved by RWB-P2-E2002-APP and RWB-P3-E2002-APP.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the rwb-integration contract fake, the envelope of RWB-PLT-E1027-CON, the `rwb_decision` baseline and the registry rows of RWB-P7-E1073-APP; the other platform rows are the ones the patterns add (§13) |
| Negotiable | Nothing business is fixed: package codes, rule IDs, version labels, route states and maximum breaks are rows of the package or values of rwb-case |
| Valuable | One read explains every move a broken plan caused, and no caller can evaluate a version that was not promoted or whose checksum does not match |
| Estimable | One consumer, one mapper, one appender, one reader, one version answer |
| Small | One sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test on the record and registry fixtures |

### 7. Acceptance criteria

```gherkin
Feature: ACE plan status on the case, the RESTRUCTURE version in force and the record of the route moves

  Background:
    Given open case "RW-2026-000310" with synthetic account "A-0310"
    Given the ACE common module stub holds plan "TDR-SYN-0310" for "A-0310"
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02
    Given the business date is 2026-12-15

  Scenario: AC1 The version in force is answered with its state and its checksum (new, D-RCV-60)
    Given version "RES-2026.12" is IN_FORCE from 2026-12-01 with the checksum of its artifact held
    When a caller asks GET /api/recovery/decision/v1/admin/rule-packages/RESTRUCTURE/versions
    Then the answer names "RES-2026.12" as the one version in force on 2026-12-15 with its state, its valid-from date and its checksum
    Then no other version of the package is named as in force for that date
    Then no rule is evaluated, no working memory is opened and no rule result is returned by this service

  Scenario: AC2 Any other state, and an artifact that no longer matches its checksum, is refused (new, D-RCV-60)
    Given version "RES-2026.13" is APPROVED and not in force on 2026-12-15
    When a caller asks for the versions of the package on that date
    Then "RES-2026.13" is not named as in force, no row of it is served, and any answer that names it names its state APPROVED
    Given the artifact of "RES-2026.12" is altered so its checksum no longer matches the recorded one
    When the same caller asks for the versions of the package on 2026-12-15
    Then the call is refused with the state named and no rows served
    Then one incident is raised for the version, its state is unchanged and no other version is served in its place

  Scenario: AC3 The plan-status move of a broken plan leaves one entry with its rule and its version (new, D-RCV-60)
    Given the case is in route state "PLAN_CURE_PERIOD" with break count 0
    Given plan "TDR-SYN-0310" has status "BROKEN" in ACE with status date 2026-12-14
    When the plan-status step announces rwb.decision.DecisionRecorded.v1 with rule ID "R-RES-29", rule version "RES-2026.12", final call "CURE_PERIOD_EXPIRED" and actions carrying "R-RES-30" and "BACK_TO_ROUTE_DECISION"
    Then one decision_log_entry exists for case "RW-2026-000310" and business date 2026-12-15 with rule_id "R-RES-29", rule_version "RES-2026.12" and final_call "CURE_PERIOD_EXPIRED"
    Then its inputs snapshot holds plan status "BROKEN" dated 2026-12-14, route state "PLAN_CURE_PERIOD" and break count 0
    Then it carries the actor, the decided time, chain_seq, prev_hash and entry_hash, and this service writes no case row, plan column, route-state column or timer

  Scenario: AC4 The litigation move has its own entry, a repeat adds none and a move that never happened leaves none (new, D-RCV-60)
    Given a seed of the case is in route state "LIT_ROUTE_APPROVED" with prior route R2 on 2026-12-16
    When the move is announced with rule ID "R-LIT-02", rule version "RES-2026.12", final call "TREATMENT_BROKEN" and actions carrying "NOTICE_GENERATED"
    Then one decision_log_entry exists for the case and 2026-12-16 with rule_id "R-LIT-02" and final_call "TREATMENT_BROKEN"
    Given the same record is delivered again with the same idempotency key
    Then the count for the case and 2026-12-16 stays one and the first entry's id is answered
    Given the status did not change, or the ACE read timed out, or no version was in force on 2026-12-15
    Then no entry is written for that case and date and the ledger of the date is unchanged
    Given a record with rule ID "R-RES-29" and an empty rule version
    Then it is refused with MSG-P7-009 naming "ruleVersion" and dead-lettered after the last retry

  Scenario: AC5 The read explains the moves of a case, with chainVerified on every entry (new, D-RCV-60)
    Given the entries of the case for 2026-12-15 and 2026-12-16 exist and the link of the second does not hold
    Given the rwb-integration contract mock returns plan status "BOOKED" with date 2026-12-01 and live false
    When a reader holding Decision log R calls GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000310&from=2026-12-15&to=2026-12-16
    Then the page returns both entries in chain order with rule_id, rule_version, final_call, decided_at, the actions and chainVerified
    Then the mock's plan status is shown beside them with its date 2026-12-01 and rewrites no entry
    Then the entry whose link does not hold answers chainVerified false, is not dropped and is named by MSG-P7-012
    Then a role without Decision log R is refused with MSG-P4-002 and a case outside scope answers 404 with MSG-P4-003

  Scenario: AC6 The 02:00 chain check covers the entries of the business date (new, D-RCV-60)
    Given the entries of 2026-12-15 form a chain from chain_seq 1 to 40 and the entry at chain_seq 17 was altered outside the service
    When JOB-14 runs at 02:00 on 2026-12-16
    Then the run stops at that entry and names its id, and one incident is raised with MSG-P7-008 naming the date and the entry
    Then every entry of the date from that one on answers chainVerified false and the seal of the date is not written

  Scenario: AC7 A provided operation answers 401 without a valid credential and 403 without the right (new, D-RCV-60)
    Given the decision log read GET /api/recovery/decision/v1/decision-log is provided for case "RW-2026-000310"
    When a caller with no valid credential calls it
    Then the answer is 401 and no entry is returned
    When a caller without Decision log R calls it for that case
    Then the answer is 403 and no entry is returned

  Scenario: AC8 A consumed call that fails or does not answer writes no entry (new, D-RCV-60)
    Given the plan-status step reads plan "TDR-SYN-0310" for "A-0310" through a consumed call
    When the consumed call fails with an error answer
    Then no decision_log_entry is written for case "RW-2026-000310" and business date 2026-12-15 and the ledger of the date is unchanged
    When the consumed call does not answer
    Then no decision_log_entry is written for case "RW-2026-000310" and business date 2026-12-15 and the ledger of the date is unchanged
```

These six criteria are new and test only this deliverable. They own no legacy criterion: the nine of RWB-E2-002 stay with the primary slices, the ACE read and the stored status with RWB-P2-E2002-APP, the status on the case, the route move, the task and the timer with RWB-P3-E2002-APP, the rights with RWB-P4-E2002-APP, and the cross-service proof with RWB-ITG-E2002-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a version in force for the business date is answered, with its state, valid-from date, checksum and rows; no older, superseded or unchecked version fills a gap | DP-04; ADR-017; NFR-034 |
| BR2 | The move a broken plan causes is recorded once, one entry per case, business date and rule identity, with the rule and the package version the owning service evaluated | REQ-DRI-013; REQ-CHO-002; legacy AC2, BR10 |
| BR3 | The entry carries `rule_id`, `rule_version`, the inputs snapshot with the ACE plan status and its date, the final call, the actions with the second rule and the state reached, and the actor | FSD P7 A2.2, A2.3; TSD P7 T3.1 |
| BR4 | An entry is append only and hash-chained; a correction is a new entry naming the one it corrects | FSD P7 AC-P7-001-01; RWB-P7-E1008-APP |
| BR5 | A decision whose record cannot be written does not proceed: the local record and the move are one transaction in the owning service, and an unavailable ledger answers no partial page | Principle 5; R-UNI-39; legacy BR8 |
| BR6 | A repeat appends nothing and is counted; a move that never happened leaves no entry | R-UNI-40; legacy BR9, BR11 |
| BR7 | A version not in force, or an artifact whose checksum does not recompute, is refused with the state named and no rows; a missing version is `NoPackageInForce` in the owning service, never a default move | R-UNI-41; legacy BR11; MSG-P3-027 |
| BR8 | The read names the rule and its version for every move, and a break in the chain is shown with `chainVerified` false and named, never hidden | NFR-033, NFR-035; MSG-P7-012 |
| BR9 | The chain of a business date is checked at 02:00, which is the only reason a `chainVerified` value is trusted for that date | NFR-035; RWB-P7-E1008-APP |
| BR10 | The plan status, its date, the route state, the queue, the task, the timer and the rights are other services' values; this service holds the version, the checksum and the record | DP-01; DP-03; legacy AC7, AC8 |

BR1 runs in the version answer. BR2, BR3, BR6 and BR10 run in the ingest, the mapper and the appender, where the dedupe key decides whether an entry is appended and the plan facts are copied as they arrive. BR4 and BR5 run in the schema and the append: the trigger refuses an UPDATE and a DELETE, and the append is one transaction with the chain lock. BR7 runs at the boundary, before any row is read. BR8 and BR9 run in the reader and the 02:00 check.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | a record for a case, date and rule identity | No entry exists | One `decision_log_entry` at the next `chain_seq` |
| Appended | the same record or move again | The idempotency key repeats | No change; the first id is answered and the repeat counted |
| Appended | the same case and date, a different move | The rule identity differs | A further entry for that date |
| APPROVED | the 00:01 promotion on the valid-from date (RWB-P7-E1073-APP) | The load checks passed and approver is not author | `IN_FORCE`; the version before it becomes `SUPERSEDED` |
| LOADED, APPROVED, SUPERSEDED, ROLLED_BACK, REFUSED | a version answer | The version is not in force | Refused, state named, no rows |
| IN_FORCE | a version answer | The checksum recomputes to the recorded one | Answered; anything else refuses and raises one incident |
| Chained | the 02:00 check | A link does not hold | That entry and every later one answer `chainVerified` false, one incident, no seal |

The case state machine is not this service's (TSD P7 T4): rwb-case owns the case status, the route state, the plan status, the queue, the task and the timer. This story records the move that reaches a route state and sets none: `PLAN_CURE_PERIOD` while the cure period runs, `PLAN_BROKEN` and `BACK_TO_ROUTE_DECISION` by `R-RES-29` and `R-RES-30`, `RESTRUCTURE_BARRED` at the second break under `restructure.max_breaks` = 2, `NOTICE_GENERATED` from `LIT_ROUTE_APPROVED` by `R-LIT-02`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-decision service identity, schema `rwb_decision`, own login (DP-02) | Appends the entry, answers the version and serves the read; the login name is Not specified in the source documents (GAP-2469; ASM-4099) |
| SY-DECLOG, decision log writer and the record library of DP-03 | Publishes the record from the owning service; holds no grant on `rwb_decision` |
| SY-RULES, rules component | Evaluates the package in its own service on the version answered here; never on its behalf here |
| RW-CASEOWN, RW-RESTRUCT | Read the moves and plan facts of cases in scope (Decision log R, scope applied) |
| RW-TEAMMGR, RW-AUDIT, RW-COMPLY | Read the ledger with its chain state for a team, an audit or a review (Decision log R) |
| RW-RISK, RW-COE | Approve and author the versions through RWB-P7-E1073-APP and RWB-P3-E2042-APP; this story answers the version and records the move |
| RW-PLATADM | Operates the Schedule and reads the incidents of a refused version and of a chain break |
| rwb-integration (P2), rwb-case (P3), rwb-access (P4) | Own the plan read, the case, the move and the rights; this service calls the plan read at display time and reads no table of theirs |

The authorisation decision is the POST /authorise check of rwb-access under DP-08: every read and every action of this service asks it before it runs, and the roles of section 10 are the rights that check answers; the story holds no role row. Refusals are 403 with MSG-P4-002, 404 with MSG-P4-003 and 503 with MSG-P7-003.

### 11. Data

| BR Field ID | Table in rwb_decision | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write |
| DF-DEC-002 | decision_log_entry | case_id (a value of the record, no foreign key into `rwb_case`) | Write |
| DF-DEC-003 | decision_log_entry | decision_code (a value of LOV-DECISION) | Write |
| DF-DEC-004, DF-DEC-005 | decision_log_entry | rule_id ("R-RES-29" or "R-LIT-02"), rule_version ("RES-2026.12") | Write |
| DF-DEC-008 | decision_log_entry | inputs_ref, naming the snapshot with the plan status and its date | Write |
| DF-DEC-012 | decision_log_entry | final_call ("CURE_PERIOD_EXPIRED" or "TREATMENT_BROKEN") | Write |
| DF-DEC-014 | decision_log_entry | actions (second rule, intermediate state, state reached, plan reference, plan status and date) | Write |
| DF-DEC-015 | decision_log_entry | outcome | Write |
| DF-DEC-016, DF-DEC-030 | decision_log_entry | decided_at, actor_user_id | Write |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | decision_log_entry | prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key (case, business date and rule identity) | Write |
| DF-REF-274 to DF-REF-278 | rule_package | all fields | Read |
| DF-REF-279, 281, 282, 286, 287 | rule_package_version | id, version_label, status, valid_from, valid_to | Read; the state is written only by RWB-P7-E1073-APP |
| DF-REF-284, DF-REF-285 | rule_package_version | drl_source, checksum | Read |
| DF-REF-002, 003, 008, 010, 011, 296, 298 | rule_row | rule_id, rule_version, action_text, owner_role, timer_spec, package_version_id, outputs | Read |
| Not specified in the source documents (GAP-2469; ASM-4099) | rule_package_version | the artifact reference answered with the checksum | Read |
| outbox_event, processed_event, idempotency_key | objects of DP-09 | all fields | Write |

Field IDs are those of the Logical Data Model and TSD P7 T3.1. `decision_log_entry.case_id` is the only case value here: no plan reference, status, route-state, product-group or amount column exists and no foreign key points into another schema (DP-01). The plan facts travel inside the inputs snapshot and the actions payload; the physical shape of that snapshot is Not specified in the source documents (GAP-2469; ASM-4099). `recovery_case`, `case_account`, `task` and `timer` are rwb-case's and `treatment` is rwb-treatment's.

### 12. Contract

Base `/api/recovery/decision/v1` (DP-13), topic `rwb.decision.events.v1` (DP-14), queue `rwb-decision`, schema `rwb_decision`, Java package as §1.

#### 12.1 REST operations provided

| Method | Path | Purpose | Authorization |
|---|---|---|---|
| GET | `/admin/rule-packages/{packageCode}/versions` | The versions of `RESTRUCTURE` for a business date: the one in force with its state, valid-from date, checksum and row count, and any other version with its state only; no rows of a version not in force | Decision log R; a model-owner service identity for the checksum |
| GET | `/decision-log` | The moves of a case or a date range: query `caseId`, `from`, `to`, `page`, `size`; each item carries `rule_id`, `rule_version`, `final_call`, `decided_at`, the actions and `chainVerified`, and the page carries MSG-P7-012 on a broken link | Decision log, right R, scope applied |

The first is the registry read the Ownership Map attributes to this service; API-P7-006 of TSD appendix T-A is the decision-log query, and the entry read and the audit export are RWB-P7-E2005-APP's. Field names beyond those named, the page size (50 by default) and the artifact field are Not specified in the source documents (GAP-2469; ASM-4099, ASM-4100).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/integration/v1/cases/{caseId}/plan-status` | rwb-integration (P2), under RWB-P2-E2002-CON | Today's plan status beside an entry, so a reader can tell a plan that has moved since the decision from one that has not; the entry is never rewritten from it | One hop, 2 s (DP-11) |

The answer carries `planRef`, `accountNo`, `status`, `statusDate`, `live` and `messageCode`; a stored value answers `live` false with MSG-P2-008 and its date, and an unavailable ACE answers 503 with MSG-GEN-006. Both are rwb-integration's and are shown as they arrive.

#### 12.3 Events published

None. The promotion announcement on `rwb.decision.events.v1` is written by RWB-P7-E1073-APP in the transaction that moves a version to `IN_FORCE`, so no caller can fetch a version whose promotion was never announced; this story answers with the label and checksum that announcement names. Its payload field names are Not specified in the source documents (GAP-2469; ASM-4101).

#### 12.4 Events consumed

| Event | Topic | From | Used for | Owner |
|---|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | `rwb.decision-record.v1` | All 19 services; the moves of this key from rwb-case | The append of `decision_log_entry`: decision code, final call, rule and version, inputs reference, actions and actor | rwb-decision (P7) |

Consumed through an inbox that deduplicates on the event identifier and again on the case, business date and rule identity, with the retry and dead-letter topics of DP-09. The envelope is RWB-PLT-E1027-CON's; how the business date travels and the field names of the plan facts in the actions are Not specified in the source documents (GAP-2469; ASM-4101).

#### 12.5 Workflows and activities

None added; the ingest is a consumer and the appender runs in its transaction. The one it depends on is another story's:

| Name | Kind | Queue | Owner |
|---|---|---|---|
| DecisionChainCheckWorkflow and its `sendComplianceNotice` activity | Workflow and activity, JOB-14 | `rwb-decision` | RWB-P7-E1008-APP |

#### 12.6 Schedules

| Job | When | Queue | Mechanism |
|---|---|---|---|
| JOB-14 Hash-chain check | 02:00 daily, Asia/Bangkok | `rwb-decision` | Temporal Schedule starting DecisionChainCheckWorkflow (DP-10). The Schedule is RWB-P7-E1008-APP's; this story asserts the moves of a business date are inside the range it verifies |

None else; the daily plan-status step of the legacy story is an event-started run in rwb-case, not a Schedule here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `decision_log_entry` | P7 (rwb_decision) | Ledger entry of a move and of every other decision announced here; append only and hash-chained |
| `rule_package`, `rule_package_version`, `rule_row` | P7 (rwb_decision) | Registry, versions and parsed rows; read here, written by the authoring, promotion and rollback stories |
| `rule_test_case` | P7 (rwb_decision) | Read in this story's tests only; written by the authoring story |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |

`recovery_case`, `case_account`, `task` and `timer` are P3's, `treatment` is S2's and `approval` stays with the approval stories of this service; this story owns none of them and reads none of them.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration contract fake (RWB-P2-E2002-CON) | The plan-status read | `APPROVED` dated 2026-12-10; `BROKEN` dated 2026-12-14; no status with `live` false and MSG-P2-008 dated 2026-12-01; `SUSPENDED`; an answer beyond 2 s with MSG-GEN-006; MSG-P4-002 and MSG-P4-003 |
| DecisionRecorded fixture (RWB-PLT-E1027-CON) | The consumed envelope | One move for 2026-12-15 naming `R-RES-29` and `RES-2026.12` with `R-RES-30` in its actions; one litigation move for 2026-12-16; a duplicate of each; a record without a rule version; decision code `D99` |
| Registry fixture (RWB-P7-E1073-APP) | `rule_package_version` and `rule_row` | `RES-2026.12` in force with a matching checksum; `RES-2026.13` approved and not in force; a superseded version; an artifact that no longer matches |
| Ledger fixture | `decision_log_entry` | A chain of forty entries for 2026-12-15 with chain_seq 17 altered; an empty ledger for a date whose step did not run |
| gateway-bff composite route (DP-19) | One answer for the decision log screen | The entries page with the case header beside it; the path and merge order are Not specified in the source documents (GAP-2469; ASM-4102) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The version answer and the decision-log page provided; the plan-status read consumed at display, one hop within 2 s |
| Kafka | None published, 1 consumed | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`; the promotion announcement is RWB-P7-E1073-APP's |
| Temporal | None created | JOB-14 is observed on queue `rwb-decision` and is RWB-P7-E1008-APP's |
| File | None | The daily seal and its write-once storage stay with RWB-P7-E1008-APP |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, modules `planstatusrecord` and `restructureversion`.

| Component | Type | Responsibility |
|---|---|---|
| PlanStatusRecordIngest | Consumer | Consumes the record through the inbox; deduplicates on the event and on the case, date and rule identity |
| PlanStatusRecordMapper | Service | Required fields, the two refusals, and the mapping to the field groups of the entry |
| MoveRecordAppender | Service | Appends one entry with `chain_seq`, `prev_hash` and `entry_hash` in one transaction; answers the first id on a repeat |
| PlanStatusDecisionReader | Service | The read by case or date range, `chainVerified`, MSG-P7-012, and today's status from the rwb-integration contract at display |
| RestructureVersionAnswer | Service | The one version in force for the date with state, valid-from, checksum and row count; any other with its state only; no evaluation |

**Database and migrations.** Writes `decision_log_entry` only and reads `rule_package`, `rule_package_version` and `rule_row`. Index `(case_id, decided_at)`, a unique key on the idempotency key of case, date and rule identity, and a unique key on `rule_package_version (package_id, version_label)`. Per-service Flyway of DP-15: `V2002_1__plan_status_record.sql` adds the indexes and no case, plan or route column; no row is seeded.

**Configuration.** No business value: package codes, rule IDs, version labels, route states and maximum breaks are rows of the package or values of rwb-case, and the version-state list and LOV-DECISION are read as reference data (DP-07). Two settings only, the page size and the ingest retry count, neither fixed by a source in the read set (GAP-2469; ASM-4100).

**Build steps.** (1) The version answer with the state check and the checksum, tests AC1 and AC2. (2) The ingest and mapper against the fixture, AC3 and AC4. (3) The appender with the chain columns and the repeat path, AC3 and AC4. (4) The reader with the filters, `chainVerified` and the refusals, AC5. (5) The JOB-14 coverage assertion over a seeded chain, and the schema assertion that `rwb_decision` holds no case, plan or route column, AC6.

| DP | Pattern applied | Dependency added |
|---|---|---|
| DP-01 | Own schema `rwb_decision`; no other service's tables | none |
| DP-03 | Local record in the owning service and the shared topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | Embedded Drools per service; package and versions from this registry, evaluation in the owner | H RWB-PLT-E1072-CON; C RWB-P7-E1073-APP |
| DP-05 | ACE data only through the owner's contract or own `v_ace_*`; none read here | none |
| DP-06 | Parameters through the rwb-case contract (`restructure.max_breaks`) | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data and lists through the rwb-case contract | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Outbox and inbox library, CloudEvents, per-service topic | H RWB-PLT-TE006-CON |
| DP-10 | Temporal Schedule instead of Quartz for JOB-14 | H RWB-PLT-E1071-CON |
| DP-11 | The plan-status read as a REST contract with a mock, one hop, 2 s | none (C from the legacy dependency) |
| DP-13 | Base `/api/recovery/decision/v1` | none |
| DP-15 | Per-service Flyway in `rwb_decision` | H RWB-PLT-E1044-CON |
| DP-19 | gateway-bff composite route for the decision log screen | H RWB-PLT-N001-CON |

This slice adds no build dependency of its own (metadata "Depends on (build)" = None) and builds against the baseline, the RWB-P2-E2002-CON fake and the registry rows of RWB-P7-E1073-APP. The platform H rows and C rows above are the ones the patterns add; they are held by the platform, contract and registry stories and are not repeated in the metadata rows, which name the one contract dependency of the key (GAP-2470; ASM-4103). DP-04 is the point of the slice: the registry is central, the evaluation local, and the working memory and budget stay in the owning service. DP-05, DP-06 and DP-07 are prohibitions: no ACE view, no parameter and no list value in code. DP-19 is the composite route behind the screen.

**Done when.** The tests in §16 pass, the contract tests of RWB-P2-E2002-CON and RWB-PLT-E1027-CON stay green, and a SIT week shows the move of 2026-12-15 recorded once with `R-RES-29` and `RES-2026.12`, the litigation move of 2026-12-16 recorded once with `R-LIT-02`, a repeat adding no entry, a page that names a broken link and hides no entry, and the version answer naming only the version in force with its checksum.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The ledger cannot take the append or answer the read | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |
| MSG-P7-012 | An entry on the page does not match the chain | Entry {entryId} does not match the decision log chain. Do not rely on it until Compliance has reviewed it. |
| MSG-P7-008 | The 02:00 check of a date finds a break | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P3-027 | No version in force on the business date | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P4-002 | A role without the Decision log right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A case outside the caller's scope | This case is not in your scope. |
| MSG-P2-008 | Not specified in the source documents (DOR-RWB-P7-E2002-APP-9) | Shown as rwb-integration sends it. |
| MSG-GEN-006 | Not specified in the source documents (DOR-RWB-P7-E2002-APP-9) | Shown as rwb-integration sends it. |

MSG-P7-009 goes to the log and the incident, never to a customer; its {field} is `ruleVersion` or `decisionCode`. For MSG-P3-027 the {table} is the package code "RESTRUCTURE" and the {check} is "no package in force"; no case fact is named. Every error is an RFC 9457 problem response; the reads answer 401, 403, 404 and 503 with MSG-P7-003. A refused version answer names the package, the version and its state, carries no rows and has no message identifier of its own (GAP-2469; ASM-4101). MSG-P2-008 and MSG-GEN-006 are rwb-integration's and shown as they arrive. This story owns no screen: SCR-03 and SCR-14 are rwb-case's (P3); their states are listed in section 15 as the sources give them.

### 15. Screens and states

No new screen. The plan-status section of SCR-38 Decision log query shows, for a case or a date range, the entries in chain order with the rule and its version, the final call, the plan reference, the plan status and its date, the state reached, the decided time and `chainVerified`. States are Loading, Results, Empty ("No decisions match this search.") and Error with MSG-P7-003. Screen Specifications v1 gives only Loading for SCR-38; Empty, Error and no access are Not specified in the source documents (CG-ALL-7051). A broken link puts MSG-P7-012 at the top and leaves every entry in place; a reader without Decision log R sees the refusal. The header beside the entries, the SCR-03 plan-status panel and the SCR-14 broken state are rwb-case's. SCR-03 states: Loading (Screen Specifications v1); empty, error and no access are Not specified in the source documents (CG-ALL-7049). SCR-14 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-7050). The screen is one gateway answer through the composite route (DP-19), which calls this service for the entries and rwb-case for the header; its path and merge order are Not specified in the source documents (GAP-2469; ASM-4102). No screen of this story writes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-002-01 | Legacy AC1 (BR1, BR2, BR6, BR10); status and move are P2's and P3's; BR1, AC1: the day's evaluation cites `RES-2026.12` and that version is answered with its checksum | End to end | ACE stub plan TDR-SYN-0310 APPROVED |
| TC-E2-002-02 | Legacy AC2 (BR4, BR5, BR10); BR2, BR3, AC3: one entry naming `R-RES-29` and `RES-2026.12` with `R-RES-30` and `BACK_TO_ROUTE_DECISION` | End to end | Case in PLAN_CURE_PERIOD; plan BROKEN |
| TC-E2-002-03 | Legacy AC3 (BR7); stored status is P3's, ACE answer P2's; BR6, AC4: an unchanged status writes no entry | End to end | ACE stub returns no plan |
| TC-E2-002-04 | Legacy AC4; BR6, AC4: a read that timed out writes no entry and the ledger catches up with no loss | NFR | ACE stub delayed 3 seconds |
| TC-E2-002-05 | Legacy AC5 (BR3); the unknown code is P3's exception; BR6, AC4: `SUSPENDED` writes no entry | End to end | ACE stub returns SUSPENDED |
| TC-E2-002-06 | Legacy AC6 (BR9); BR6, AC4: the repeat appends nothing and adds one to the repeat count | End to end | Step run twice on 2026-12-15 |
| TC-E2-002-07 | Legacy AC7 (BR8); the local record is P3's; BR5, AC4: a record that never arrives leaves no entry here and is caught up when it does | End to end | Decision log store stopped |
| TC-E2-002-08 | Legacy AC8; the scope check is P4's; BR8, AC5: 404 with MSG-P4-003 and no entry returned | End to end | Scope Own; another owner's case |
| TC-E2-002-09 | Legacy AC9, legacy BR11; BR7, AC2: no version in force names none and serves no rows | Contract | No RESTRUCTURE version in force on 2026-12-15 |
| TC-E2-002-10 | The legacy Access criterion (legacy X7); the right is P4's; BR8, AC5: a role without Decision log R is refused with MSG-P4-002 | Component | RW-REFADM calls GET /decision-log for a case in scope |
| TC-E2-002-11 | Legacy Principle 5 (legacy BR8); BR5, AC4: the move and its entry are one transaction, so a failed append leaves nothing | NFR | Append forced to fail on the R-RES-29 move |
| TC-E2-002-12 | Boundary of the tables of section 12.7 (ASM-3438) | Component | Edge rows of each table in section 12.7 |
| TC-E2-002-13 | AC7: a call with no valid credential answers 401 and a call without Decision log R answers 403 | Component | Not specified in the source documents (NEWAC-RWB-P7-E2002-APP-AC10) |
| TC-E2-002-14 | AC8: a consumed call that fails or does not answer writes no entry | NFR | Not specified in the source documents (NEWAC-RWB-P7-E2002-APP-AC11) |

Every legacy test case of RWB-E2-002 appears once. System maps to End to end, Access to Component and Resilience to NFR; the no-version case is Contract because its assertion here is the version refusal. The `-ITG` copies belong to RWB-ITG-E2002-ITG. `RES-2026.13` and the chain of forty entries are synthetic, built on the pattern of `RES-2026.12`.

### 17. Guardrails

- No business value in code: package codes, rule IDs, version labels, status codes, route states, the event map and the maximum breaks are rows of the package, values of rwb-case or reference data. No rule form, label, status code or route state appears in this service's Java.
- No personal data in events, workflow inputs, logs or tests: an entry carries a case identifier, a rule identity, the plan reference and actor identifiers, never a name, address, identity number or account number. Test data is synthetic.
- No cross-schema read (DP-01): no `rwb_case`, `rwb_treatment` or other service's table is read and no foreign key points into one.
- ACE data only through the owner's contract: the plan comes from the rwb-integration operation; no `v_ace_*` view and no ACE table is read.
- No rule engine here: no KieBase, no working memory and no evaluation on queue `rwb-decision`.
- A version is answered only while in force and only with a matching checksum; no older, superseded or unchecked version fills a gap.
- An entry is never corrected in place: a correction is a new entry naming the one it corrects, and the trigger refuses an UPDATE and a DELETE.
- No topic or event name is typed in code (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module, with the rule and the version on the record | Program 5.2; Epic 2 3.2 | FEAT-CHO-02, FEAT-DRI-02, FEAT-DRI-03 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39, R-UNI-40 | TC-E2-002-01, TC-E2-002-04, TC-E2-002-06, TC-E2-002-07 |
| REQ-CHO-002 | Plan status change visible on the case, with the move explained | Program 5.3; Epic 2 3.2 | FEAT-CHO-02, FEAT-DRI-01, FEAT-DRI-07 | 7.3 Negotiate settlement or deed in lieu | R-RES-29, R-RES-30, R-RES-31, R-LIT-02 | TC-E2-002-02, TC-E2-002-03, TC-E2-002-05, TC-E2-002-08, TC-E2-002-09, TC-E2-002-12 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E2-002; contract RWB-P2-E2002-CON; baseline `rwb_decision` | Metadata; sections 1, 3, 12 |
| Version `RES-2026.12` with rows `R-RES-29`, `R-RES-30`, `R-RES-31`, `R-LIT-02` (legacy BR10) | Sections 1, 3, 7 (AC1, AC3), 8 (BR1, BR2), 11, 12 |
| Rule ID and version on every entry (legacy AC2, BR10) | Sections 7 (AC3, AC4), 8 (BR2, BR3), 11 |
| Plan statuses and the unknown `SUSPENDED` (legacy BR3, AC3, AC5) | Sections 1, 3, 5 |
| Route states of legacy section 9 and `restructure.max_breaks` = 2 | Sections 1, 9 |
| Append only and hash-chained (legacy BR8) | Sections 8 (BR4, BR5), 9, 17 |
| No version in force is a refusal (legacy AC9, BR11) | Sections 5, 7 (AC2), 8 (BR7), 14 |
| Messages MSG-P7-003, 008, 009, 012, MSG-P3-027, MSG-P4-002, 003 | Section 14, exception paths |
| Field IDs DF-DEC-001 to 031 and DF-REF-002 to 298 | Section 11 |
| Legacy test cases TC-E2-002-01 to 11; synthetic case, plan and dates | Section 16 |
| The other slices of RWB-E2-002 | Sections 2, 5, 19 |

### 19. Out of scope

- The ACE plan read, the live answer, the batch of 500, the 2 second timeout and the status ACE cannot give: rwb-integration (RWB-P2-E2002-APP, RWB-P2-E2002-CON).
- The stored plan status with its date, the route state, the task and the durable timer: rwb-case (RWB-P3-E2002-APP).
- The plan-status panel, the broken-plan state of the treatment record and the case header: rwb-case (RWB-P3-E2002-APP, RWB-P3-E2004-APP) and rwb-treatment (RWB-S2-E2004-APP).
- The rights, the scope check and the refusal of an out-of-scope case: rwb-access (RWB-P4-E2002-APP).
- Authoring, load checks, four-eyes approval, effective dating, the promotion step and the rollback: RWB-P3-E2042-APP and RWB-P7-E1073-APP.
- The append-only table, the trigger, the chain lock, the verifier, the daily seal and the JOB-14 workflow: RWB-P7-E1008-APP.
- The generic ledger ingest, JOB-13, the record library and the reads of other decisions: RWB-P7-E1027-APP.
- The entry read `GET /decision-log/{entryId}`, the audit query screen, its filters, paging and export: RWB-P7-E2005-APP and legacy RWB-E2-005.
- The other packages of the phase 1 set and the route sets of Epics 3 to 7.
- The end-to-end proof across the four services and the registry: RWB-ITG-E2002-ITG.
- The schema baseline, topic and queue provisioning, the chart, dashboards and runbook of this service.
