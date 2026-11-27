# RWB-S4-E5011-CON Track hearings, deadlines and fees - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5011-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5011-CON-16); the squad sizes it at refinement |
| Contract version | v1, base `/api/recovery/litigation/v1` |
| Depends on (build) | None |
| Contract dependencies | Workflow kit contract for the durable timers of `LitigationWorkflow` (Not specified in the source documents (GAP-2789)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Requirement trace | Not specified in the source documents (GAP-2792) until the PRD allocates requirement IDs; the hearing lead time, the D7.4 spend limit and the prescription horizon are held as versioned reference or rule rows, Not specified in the source documents (GAP-2792) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the hearings, deadlines and fees step of rwb-litigation, split from RWB-E5-011. It fixes the three operations on `/api/recovery/litigation/v1` with their schemas, the two hearing vocabularies, the fee read of rwb-payment, the case read and stage answer of rwb-case, the rule package read of rwb-decision, the decision-record element of DP-03, the durable-timer element of `LitigationWorkflow`, the error set and the fakes. The fee has no home in this service and no named operation (GAP-2788; ASM-4626); the deadline is a workflow timer and not the `timer` row (GAP-2789; ASM-4627). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5011-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the hearings, deadlines and fees step of rwb-litigation — the three operations with their schemas, the two hearing vocabularies, the shape of the fee read from rwb-payment, the case read and stage answer of rwb-case, the rule package read of rwb-decision, the decision-record element, the durable-timer element, the error set and the fakes**, so that **the app story, the two workspaces and the wave 3 harness build against one fixed, testable surface on Day 1 and a hearing date, a deadline, a fee or an answer shape can never drift between rwb-litigation, rwb-payment, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (ADR-020). The legacy step crossed four boundaries in one process: the case row, a `timer` row, the decision log entry and the rule row. The target splits them: the hearing and its dates stay here, the case and its clock move to rwb-case, the rule answer and its record move to the library of DP-03 and the governed rule rows of rwb-decision, and the fee moves to rwb-payment. Each boundary is now something another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It records that this service holds no `v_ace_*` grant, so DP-05 is declared as a prohibition and no ACE read appears on any row.

Three points are carried as gaps and assumptions rather than decided quietly: the fee has no table and no named operation on rwb-payment (GAP-2788), the deadline is fixed by no value and its row belongs to rwb-case (GAP-2789), and the rule package read and the reference values carry no dependency row (GAP-2790, GAP-2792).

### 3. Preconditions

- The service template and the naming library are available (`RWB-PLT-TPL`, `RWB-PLT-E1047-CON`), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the idempotency rule and the pagination convention are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `hearing` and `legal_action` are S4's, `recovery_case`, `timer` and `task` are P3's, `rule_row` and `decision_log_entry` are P7's, `notice` and `document` are P6's and P5's. This document never declares another service's operation as provided.
- The three consumed owner contracts are named as documents and built against their fakes: rwb-payment for the fee and the spend, rwb-case for the case and the stage answer, rwb-decision for the rule package. No source read for this key names their operations, so all three rows carry the placeholder (GAP-2788, GAP-2790, GAP-2791; ASM-4626, ASM-4628, ASM-4629).
- The LITIGATION rule package with R-LIT-33 to R-LIT-35 and R-LIT-41 to R-LIT-43 and its D7 route set are governed in rwb-decision; this baseline consumes them and declares none of them (GAP-2790; ASM-4628).
- The hearing lead time, the spend limit, the label of D7.4 and every LOV value are reference values whose content no source gives for this key (GAP-2792; ASM-4630).
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract description of the step: its three provided operations, its three consumed facts, its own durable timers and decision record, and its error conditions.
2. Fix the schemas `HearingRequest`, `Hearing` and `LegalActionUpdate` over DF-LEG-024 to DF-LEG-029 and the two vocabularies LOV-HEARING and LOV-HEARING-OUTCOME.
3. Fix the three operations on the base of DP-13 with their rights, their errors and the `Idempotency-Key` rule.
4. Fix the fee read of rwb-payment, mark its operation and its field list with the placeholder, and record that this service posts nothing.
5. Fix the case read and the stage answer of rwb-case: the route state, the prescription date, the move, the case timer and the officer task.
6. Fix the rule package read of rwb-decision and the decision-record element of DP-03, written before anything changes.
7. Fix the durable-timer element of `LitigationWorkflow` and the two clocks it holds: the sitting date and the re-armed next date.
8. Publish the contract tables of section 12 and the five contract fakes.
9. Add the contract tests: schemas, vocabularies, error envelope, rights, placeholders, the absence of a fourth operation, of an event, of a Schedule and of a `v_ace_*` read, and the drift between a fake and the document.
10. Tag the baseline and hand it to `RWB-S4-E5011-APP`, SCR-19, SCR-20 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body of a request or of an answer fails schema validation | The build fails on the schema lint; a deployed service answers 400 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A consumed or answered field list is not given by any source | The row carries the placeholder, the gap and the assumption, and the fake derives from the published document | None | AC3, AC4, AC5 |
| X5 | A hearing type or an outcome outside its vocabulary appears in the document or an example | The vocabulary test fails the build | None | AC1 |
| X6 | The document declares a fourth operation, an event, a Schedule or a `v_ace_*` read | The absence test of AC8 fails the build | None | AC8 |
| X7 | A written fee, a `recovery_case` property or a `timer` property appears | The boundary test fails; the review rejects the baseline | None | AC3, AC4, AC6 |
| X8 | The same hearing is posted twice with the same reference and date | The step answers with the stored answer and describes no second effect | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the Ownership Map and the published owner documents only |
| Negotiable | The element names beyond the ones the sources give, the examples and the fake fixtures are settled in the baseline review; the operations, the vocabularies, the base, the topic and the queue are fixed |
| Valuable | Unblocks `RWB-S4-E5011-APP`, SCR-19, SCR-20 and the wave 3 harness on Day 1, and the rwb-payment, rwb-case and rwb-decision teams on the same day |
| Estimable | One contract document with its AsyncAPI absence note, nine contract tables, five fakes and four contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the hearings, deadlines and fees step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of hearing and legal_action is S4, of recovery_case, timer and task is P3, of rule_row is P7 and of the fee is P8
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The three hearing schemas and the two vocabularies are fixed (new, D-RCV-60)
    Given the schema section of the baseline
    When it is compared with DF-LEG-024 to DF-LEG-029 of TSD S4 T3.1 and with T3.2
    Then HearingRequest is declared with the legal action reference, the hearing date and the hearing type
    Then Hearing is declared with id, legal_action_id, hearing_date, hearing_type, outcome and next_date
    Then LegalActionUpdate is declared with the outcome and the next date of a sitting
    Then LOV-HEARING is declared with exactly FIRST_HEARING, WITNESS, JUDGMENT_READING and MEDIATION, and LOV-HEARING-OUTCOME with exactly HELD, ADJOURNED, SETTLED and JUDGMENT
    Then both vocabularies are published as versioned reference values and neither is an enumeration member of a schema or a constant of the code

  Scenario: AC2 The three provided operations, their rights and their errors are declared (new, D-RCV-60)
    Given the operation section of the baseline
    When it is compared with TSD S4 T-A.1, T-A.2 and T6.1
    Then POST /legal-actions/{legalActionId}/hearings is declared with Litigation right U, HearingRequest in, Hearing out and an Idempotency-Key header
    Then GET /legal-actions/{legalActionId} is declared with Litigation right R and LegalAction out, hearings included
    Then PATCH /legal-actions/{legalActionId} is declared with Litigation right U, LegalActionUpdate in, LegalAction out and an Idempotency-Key header
    Then each operation carries its error set of 401, 403, 404, 409, 422 and 503 as T-A.2 gives it, one envelope and one message ID per condition
    Then no fourth operation is declared beyond these three, the legal-action create of API-S4-002 and the notice approve of API-S4-001, which belong to the sibling stories

  Scenario: AC3 The fee read of rwb-payment is declared and never written here (new, D-RCV-60)
    Given the fee section of the baseline
    When it is compared with the ownership rows of S4 and with TSD S4 T3.1
    Then the accrued fee, its spend deadline, its value date and its approval state are declared as consumed from P8 rwb-payment
    Then the operation name and the field list are Not specified in the source documents (GAP-2788; ASM-4626) and the row carries the placeholder
    Then the document declares no fee property as owned, no posting and no balance, and names no column of legal_action or hearing as a fee
    Then the call is one hop with a 2 s budget and a breaker, and a failed read leaves the calendar answer intact

  Scenario: AC4 The case read and the stage answer of rwb-case are declared (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case, timer and task
    Then the read is declared with the route state, which must be IN_HEARING for R-LIT-34 and R-LIT-35, and the prescription date
    Then the answer is declared with the stage outcome, the case timer, the officer task, the rule ID and the package version
    Then the document declares no recovery_case property, no route-state column, no timer row and no task row of its own
    Then the operation names are Not specified in the source documents (GAP-2791; ASM-4629) and both rows carry the placeholder

  Scenario: AC5 The rule package read and the decision-record element are declared (new, D-RCV-60)
    Given the rule and decision sections of the baseline
    When they are compared with the LITIGATION route set and the local library of DP-03
    Then the package is declared as consumed from P7 rwb-decision with R-LIT-33, R-LIT-34, R-LIT-35, R-LIT-41, R-LIT-42 and R-LIT-43 and its version in force
    Then one decision record is declared per outcome with the case reference, the legal action reference, the rule ID, the package version, the inputs reference, the hearing or spend fact and the stage outcome
    Then the record is declared as written through the library before anything changes, and a stopped chain leaves the hearing and the case unchanged with MSG-P7-003
    Then the operation name is Not specified in the source documents (GAP-2790; ASM-4628)

  Scenario: AC6 The deadline is declared as a durable timer of LitigationWorkflow (new, D-RCV-60)
    Given the timer section of the baseline
    When it is compared with the ownership rows (Jobs 0, Workflows 1) and the state transitions of TSD S4 T4
    Then the sitting date and the re-armed next date are declared as durable timers of LitigationWorkflow on queue rwb-litigation
    Then the document declares no timer row, no Temporal Schedule, no Quartz row and no shared job table
    Then the deadline values are declared as versioned reference rows whose content is Not specified in the source documents (GAP-2789; ASM-4627)
    Then the declaration states that a deviation pauses these timers and never the prescription clock

  Scenario: AC7 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the fee fake answers the accrued fee and the spend deadline of case "RC-2026-001211" with the approval states PENDING, APPROVED and REJECTED, and no answer beyond 2 s
    Then the case fake answers the route state "IN_HEARING", another state, the prescription date and an accepted and a refused stage outcome
    Then the rule-package fake answers the LITIGATION package with the six rules and a second version
    Then the decision-record stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged SCR-19 and SCR-20 model
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline, the table ownership and the absence tests are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema and the login are rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as this service's are hearing and legal_action, and recovery_case, timer, task, rule_row, decision_log_entry, notice, document and the fee rows are named as other owners'
    Then the document declares no event published, no event consumed, no Schedule and no v_ace_* read, and the absence test fails a build that adds one

  Scenario: AC9 Each business rule of section 8 is answered and owned by the document (new, D-RCV-60)
    Given the business rules BR1 to BR11 of section 8
    When each rule is compared with the document and with its named owner
    Then each of BR1 to BR11 is answered by the document with its owner named
    Then no rule is declared outside its owner, and an architecture constraint among them is answered by a guardrail or boundary test

  Scenario: AC10 A retried or timed-out call changes nothing and repeats no write (new, D-RCV-60)
    Given a consumed read of rwb-payment, rwb-case or rwb-decision, or a write of this service, is retried or times out
    When the retry and the timeout are compared with the operation section of the baseline
    Then a timed-out read leaves the calendar answer intact and a timed-out write changes nothing
    Then a retried write carries the Idempotency-Key of AC2 and is applied once
    Then the retry count and the timeout value are Not specified in the source documents (NEWAC-RWB-S4-E5011-CON-AC10)
```

The ten criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by `RWB-S4-E5011-APP`, which owns the two legacy criteria AC1 and AC2 word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The hearings, deadlines and fees step of the litigation journey is rwb-litigation's, and the contract declares its operations, its vocabularies, its timers, its record and the facts it consumes and nothing else | Context pack ownership rows; FSD S4 A2.11 |
| BR2 | The hearing row is this service's and is reached on the three operations of TSD S4 T-A.1 only | Context pack ownership rows; TSD S4 T3.1, T-A.1 |
| BR3 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-011 AC1 and AC2 |
| BR4 | The case, its route state, its clock and its tasks stay with rwb-case: the contract declares the read and the answer and declares no such property | Context pack ownership rows; TSD S4 T5.2; GAP-2791 |
| BR5 | The fee, the posting and the balance stay with rwb-payment: the contract declares the accrual as read and describes no write | Context pack slide 4 (P8 Payments and posting); GAP-2788 |
| BR6 | The six rules are governed in rwb-decision and are named here, never declared here | GAP-2790; ASM-4628 |
| BR7 | A hearing date is a durable workflow timer; no Schedule, no Quartz row and no shared job table is declared | Context pack ownership rows (Jobs 0); GAP-2789 |
| BR8 | No personal data in a fact, an answer, an example or a fake: references, dates, codes and a rule version only | Template and Rules §R7.2 (s17) |
| BR9 | One base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A change is additive within major version 1; a breaking change is a new major version | Architecture v5 backward-compatibility rule |
| BR11 | No ACE view and no ACE table is read: the service holds no `v_ace_*` grant and the proof of any ACE fact arrives on its owner's contract | DP-05 applied as a prohibition |

### 9. State transitions

The lifecycle of this document, not of a hearing:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the three consumed facts, the timers, the record and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-payment, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a vocabulary value or an operation changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a fourth operation, an event, a Schedule or a `v_ace_*` read | In review |

The state machine of the case is the app story's own, from TSD S4 T4: `FILED_IN_COURT` to `IN_HEARING` under R-LIT-33, `HEARING_ADJOURNED` under R-LIT-34, back to `IN_HEARING` under R-LIT-35, and the spend states `LEGAL_SPEND_APPROVAL` under R-LIT-41 to R-LIT-43. The state itself is written by rwb-case on this baseline's answer shape.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the contract document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and a correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, SCR-19, SCR-20, the wave 3 harness and the owners of rwb-payment, rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the idempotency rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in a fact, an answer, an example or a fake |

The per-service login behind the security scheme is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

Every operation's authorisation check is the rwb-access authorise check (DP-08); this baseline names it and declares no authorisation rule of its own.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Hearing element | `hearing` of `rwb_litigation`, DF-LEG-024 to DF-LEG-029: id, legal_action_id, hearing_date, hearing_type, outcome, next_date | Not specified in the source documents (DOR-RWB-S4-E5011-CON-7) |
| Legal action element | The reference, the status, the court fields and `lit_status` of `legal_action`, DF-LEG-001 to DF-LEG-014; read and updated on the two action operations | Not specified in the source documents (DOR-RWB-S4-E5011-CON-7) |
| Fee element | The accrued fee, the spend deadline, the value date and the approval state, read from P8; the field list is Not specified in the source documents (GAP-2788; ASM-4626) | Not specified in the source documents (DOR-RWB-S4-E5011-CON-7) |
| Case answer | The route state, the prescription date, the stage outcome, the case timer, the officer task, the rule ID and the package version, all P3's | Not specified in the source documents (DOR-RWB-S4-E5011-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) | Not specified in the source documents (DOR-RWB-S4-E5011-CON-7) |
| Timer | The durable timers of `LitigationWorkflow`: the sitting date and the next date; the `timer` row DF-WRK-027 to DF-WRK-036 is P3's and is not declared here (GAP-2789; ASM-4627) | Not specified in the source documents (DOR-RWB-S4-E5011-CON-7) |
| Rule rows | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, read as the package in force through the rule package read of rwb-decision (DP-04); the LOV vocabularies and the deadline values ride the reference-data read of rwb-case (DP-06, DP-07); the dependency rows for DP-04, DP-06 and DP-07 are added centrally if the plan is revised (GAP-2790) | Not specified in the source documents (DOR-RWB-S4-E5011-CON-7) |
| Not written here | `recovery_case`, `timer` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `notice` (P6), `document` (P5), the fee rows (P8), every `v_ace_*` view (P1) | Not specified in the source documents (DOR-RWB-S4-E5011-CON-7) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabularies of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

Reference data: the list read is the rule package of rwb-decision (DF-REF-001 to DF-REF-015, GAP-2790); the reference-data contract is DP-06 and DP-07, and this step names no parameter key.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Errors |
|---|---|---|---|---|
| POST | `/legal-actions/{legalActionId}/hearings` | Add a hearing date (API-S4-005) | Litigation U | 401, 403, 404, 422, 503; `Idempotency-Key` required |
| GET | `/legal-actions/{legalActionId}` | Read the action with its hearings (API-S4-003) | Litigation R | 401, 403, 404, 503 |
| PATCH | `/legal-actions/{legalActionId}` | Record the outcome and the next date (API-S4-004) | Litigation U | 401, 403, 404, 409, 422, 503; `Idempotency-Key` required |

Base `/api/recovery/litigation/v1`. The three rows are the whole surface of this step; `POST /cases/{caseId}/legal-actions` (API-S4-002) and `POST /notices/{noticeId}/approve` (API-S4-001) stay with the sibling stories of this service, and a fourth operation here fails the review and the absence test (BR2; AC2, AC8).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `Not specified in the source documents (GAP-2788; ASM-4626)` | `/api/recovery/payment/v1` | P8 rwb-payment | The accrued fee, the spend deadline, the value date and the approval state; faked |
| `Not specified in the source documents (GAP-2791; ASM-4629)` | `/api/recovery/case/v1` | P3 rwb-case | The route state and the prescription date; faked |
| The stage answer of `CaseWorkflow` (`Not specified in the source documents (GAP-2791; ASM-4629)`) | rwb-case (P3) | P3 rwb-case | The stage outcome, the case timer, the officer task, the rule ID and the package version; faked |
| `Not specified in the source documents (GAP-2790; ASM-4628)` | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version with the six rules; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All four are C dependencies in fact and not in the metadata row, and the absence is recorded as GAP-2788, GAP-2790 and GAP-2791.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. This baseline declares no event, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. `HEARING_SCHEDULED`, `HEARING_ADJOURNED`, `NEW_DATE_SET`, `FEE_DUE`, `FEE_APPROVED` and `FEE_REJECTED` are the event names of the state machine in the Business Rules and Routing Logic v4, not Kafka subscriptions: the service holds no consumer group and no inbox, and every fact arrives on the contracts of 12.2 (GAP-2791; ASM-4629).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new | `rwb-litigation` | The stage that hosts the step; its signals (trigger Not specified in the source documents (GAP-2791)), and its outcome for the parent are declared, not built; it holds the two durable timers |
| `recordHearing` | Activity | `rwb-litigation` | The hearing in; the decision record, the rule ID with its version and the deadline out |
| `armHearingDeadline` | Activity | `rwb-litigation` | The hearing date or the next date in; one durable timer armed and its fact out |
| `recordSpendDecision` | Activity | `rwb-litigation` | The fee and its approval state in; the decision record and the approved fact out |

The activity and signal names are target design choices and are fixed by no source. No activity is registered by this story.

Workflow ID form: Not specified in the source documents (CG-ALL-9261). Start rule: LitigationWorkflow starts on Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02), per the Temporal Catalog v1 Workflows row; duplicate-start policy: Not specified in the source documents (CG-ALL-9261).

#### 12.6 Schedules

None. The two clocks of the step are durable timers of `LitigationWorkflow`: the sitting date and the re-armed next date. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch window, and no Job of Architecture v5 is owned or moved here (GAP-2789; ASM-4627).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| hearing | S4 (`rwb_litigation`) | Created, read and updated by this step |
| legal_action | S4 (`rwb_litigation`) | Read for status and court fields; `lit_status` and `filed_date` read only |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked record of every hearing and spend decision (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of a repeated create or update |

`recovery_case`, `timer` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `notice` (P6), `document` (P5) and the fee rows (P8) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment fee fake | The accrued fee and the spend deadline of case `RC-2026-001211` with the value date and the approval states `PENDING`, `APPROVED` and `REJECTED`; no amount is fixed by a source (GAP-2788) | AC3, AC7 |
| rwb-case fake | The route state `IN_HEARING` and another state, the prescription date, and an accepted and a refused stage outcome with the case timer and the officer task | AC4, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version with the six rules, and a second version | AC5, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain that answers MSG-P7-003 | AC5, AC7 |
| gateway-bff composite route fake | The merged SCR-19 and SCR-20 model for case `RC-2026-001211` | AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows, the fee field list, the deadline values and the prescription warning horizon are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2788, GAP-2789, GAP-2790, GAP-2791).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | The hearing create, the action read and the action update; the fee read, the case read, the case stage answer and the rule package read; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 3 activities declared, 0 registered, 2 durable timers | `LitigationWorkflow`, `recordHearing`, `armHearingDeadline`, `recordSpendDecision`, the sitting date and the next date; no Schedule |
| File | None | No file is read or written by this step |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no hearing, no case and no fee. What it publishes is one contract description, one AsyncAPI absence note that declares no event, nine contract tables and five fakes.

**Deliverables.** The contract document `contracts/rwb-litigation-hearing.v1.yaml` with the three schemas and the two vocabularies as published reference values, the operation descriptions with their rights and errors, the timer element of `LitigationWorkflow`, the contract README rows with their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: the document declares no `v_ace_*` read and no ACE grant, because rwb-litigation holds neither. DP-04, DP-06 and DP-07 are outside the pattern set although the step reads rule rows and reference values; those reads are on the owners' contracts and carry no dependency row (GAP-2790, GAP-2792). DP-09 and DP-14 are not in the set either, which is why 12.3 and 12.4 declare no event.

**Build steps**

1. Write the three schemas and the two vocabularies of AC1 as published reference values and validate them in the pipeline.
2. Write the three operation descriptions of AC2 with their rights, their errors and the idempotency rule.
3. Write the fee row of AC3 with its placeholder and the absence test for a fee write.
4. Write the case read and the stage answer of AC4 with their placeholders.
5. Write the rule package read and the decision-record element of AC5.
6. Write the timer element of AC6 and validate it against the workflow contract.
7. Publish the five fakes of AC7 and the drift test.
8. Record the naming baseline and the absence tests of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The contract tests pass, the vocabularies are published as reference values, the five fakes answer every consumed path and the drift test is green, and the absence tests block a fourth operation, an event, a Schedule and a `v_ace_*` read.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key; it names a missing item of the pack, which is the pack story's path | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key; it names the expiry of the claim, which the case read reports | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a fact or an answer is absent or invalid | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The source product of a consumed read is stale after a late or failed ACE batch, which is VR-S4-011-1 of the FSD; the check is the owner's | {product} is from {date}. Today's load has not arrived. |

The six message IDs are contract elements and their text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its hearing state and SCR-20 Enforcement workspace in its requested and seized states, through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the calendar, rwb-payment for the accrual and rwb-case for the route state; this baseline fixes the rwb-litigation side only, and the composite route specification and the screen field list belong to `RWB-PLT-N001-CON`. SCR-19 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-9267). SCR-20 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-9268). The refusal, stale-marker and timer-held states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-011-01 | AC1, AC2, AC6 | Contract | The contract half of "Track hearings, deadlines and fees": the three schemas, the two vocabularies, the three operations and the two durable timers answer the document |
| TC-E5-011-02 | AC5 | Contract | The contract half of "Not recorded": a stopped decision-record chain answers MSG-P7-003 and describes no change |
| TC-E5-011-03 | AC2 (access path) | Contract | A role without the Litigation right is refused with MSG-P4-002 on each of the three operations |
| TC-E5-011-04 | AC5 (forced failure) | Contract | A forced decision-record write failure is described as changing nothing, and the fake proves the stopped chain |
| TC-S4-E5011-CON-01 | AC1, AC2 | Contract | The schemas, the two vocabularies, the three operations, their rights and their error sets validate; no fourth operation is declared |
| TC-S4-E5011-CON-02 | AC3, AC4 | Contract | The fee row with its placeholder, the case read and the stage answer with theirs, each one hop with a 2 s budget |
| TC-S4-E5011-CON-03 | AC5, AC6 | Contract | The rule package read, the decision-record element and the two durable timers validate; no Schedule and no timer row is declared |
| TC-S4-E5011-CON-04 | AC7, AC8 | Contract | The five fakes match the document and a drifted fake fails the build; the absence tests for a fourth operation, an event, a Schedule and a `v_ace_*` read |
| TC-S4-E5011-CON-05 | AC1, AC2 | Contract | Boundary of the four tables of section 12.7: each table is declared with its owner and contracted use, and no table, column or foreign key outside the owner list is declared |
| TC-S4-E5011-CON-06 | BR1 to BR11 | Contract | Each business rule of section 8 is answered by the document, its owner is named, and no rule is declared outside its owner |
| TC-S4-E5011-CON-07 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-S4-E5011-CON-AC9) |
| TC-S4-E5011-CON-08 | AC10 | Contract | Not specified in the source documents (NEWAC-RWB-S4-E5011-CON-AC10) |

The four legacy cases are the legacy cases of RWB-E5-011 in their legacy order, carried as the contract half: their Covers column names the criteria of this story that fix the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by `RWB-S4-E5011-APP`. The legacy level maps to `Contract` here because the artefact under test is the contract. The four cases `TC-S4-E5011-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the hearing lead time, the spend limit, the LOV values and the message texts stay reference rows, never schema defaults or enumeration members of the code.
- No personal data in a fact, an answer, an example or a fake: references, dates, codes and a rule version only; every example is synthetic.
- The case stays with rwb-case and the money with rwb-payment: the document declares no `recovery_case`, `timer`, `task` or fee property and no write of any of them (BR4, BR5).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on ACE, and the boundary test fails a build that adds one (DP-05).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or operation as its own fails the review (DP-13, DP-14, BR9).
- No fourth operation, no event, no Schedule and no Quartz row: the absence tests of AC8 fail a build that declares one (BR2, BR7).
- The error envelope, the idempotency rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| FEAT-LIT-11 | Track hearings, deadlines and fees (FSD S4 A2.11); the legacy master and TSD S4 T8 carry no requirement ID for this key (GAP-2792; ASM-4630) | The three hearing schemas, the three operations, the timers and the consumed facts | TC-E5-011-01, TC-S4-E5011-CON-01, TC-S4-E5011-CON-03 |
| R-LIT-33 to R-LIT-35 | Hearing scheduled, adjourned and re-dated | The rule package read and the stage answer | TC-E5-011-01, TC-S4-E5011-CON-02 |
| R-LIT-41 to R-LIT-43 | Fee due, approved and rejected | The fee read and the spend decision element | TC-S4-E5011-CON-02, TC-S4-E5011-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows and the three provided operations | TC-S4-E5011-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-011, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned word for word by `RWB-S4-E5011-APP`; this baseline copies none of them |
| Test cases | The four legacy cases as the contract half, and the four new contract cases |
| Feature and screens | FEAT-LIT-11, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-33, R-LIT-34, R-LIT-35, R-LIT-41, R-LIT-42 and R-LIT-43, named and governed in rwb-decision (GAP-2790) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the step, the evaluation of the six rules, the decision record, the timers and the stage answer: `RWB-S4-E5011-APP`.
- The case of record, its route states, `CaseWorkflow`, the case timer and the officer task: rwb-case (P3) and its slice of this legacy key (GAP-2791).
- The fee row, the posting, the balance and the payment match: rwb-payment (P8) (GAP-2788).
- The authoring, testing, approval and versioning of the LITIGATION package and of the six rule rows: rwb-decision (P7) (GAP-2790).
- The hearing lead time, the spend limit and the prescription warning horizon: the reference-data owner of rwb-case and the business owner of S4 (GAP-2792).
- The pack, the notice, the firm instruction and the judgment, and the two sibling operations of this service: the sibling stories of S4, rwb-document (P5), rwb-comms (P6) and rwb-partner (S9).
- The rights, roles, scope and masking data, and the composite route and screen field list of SCR-19 and SCR-20: rwb-access (P4) and `RWB-PLT-N001-CON`.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this key.
