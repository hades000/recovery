# RWB-S4-E5020-CON Record an enforcement deferral with its reason - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5020-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5020-CON-16) |
| Contract version | v1 (path suffix `/v1` on `/api/recovery/litigation/v1`) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the enforcement-deferral step of rwb-litigation, split from RWB-E5-020. It fixes the two operations on `/api/recovery/litigation/v1` with their schemas, the deferral element (`deferral_reason`, `deferral_review_date`), the stage vocabulary of the LITIGATION machine, the case read and the case answer with the queue placement, the rule package read of rwb-decision, the decision-record element of DP-03, the durable review-date timer of `LitigationWorkflow`, the error set and the fakes. The reason code list has no source (GAP-2828; ASM-4681); the three consumed contracts carry no dependency row (GAP-2829; ASM-4682); R-LIT-44 is named here as the judgment step of RWB-S4-E5016-APP and is not re-declared (GAP-2830; ASM-4683); the review date is a timer and not the monolith scheduler (GAP-2831; ASM-4684). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5020-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the enforcement-deferral step of rwb-litigation — the two operations with their schemas, the deferral and review-date elements, the stage vocabulary, the case read and case answer with the queue placement, the rule package read, the decision-record element, the durable review-date timer, the error set and the fakes**, so that **the app story, the enforcement workspace and the wave 3 harness build against one fixed, testable surface on Day 1, and a reason code, a review date or an answer shape can never drift between rwb-litigation and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (ADR-020). The legacy deferral crossed five boundaries in one process: the legal action row, the case row, the queue and assignment rows, the task row and the decision log entry. The target splits them: the action stays here, the case and its queue, assignment and task move to rwb-case, the rule rows move to rwb-decision and the record moves to the library of DP-03. Each boundary is now something another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It records that this service holds no `v_ace_*` grant, so DP-05 is declared as a prohibition.

Four points are carried as gaps and assumptions rather than decided quietly: the reason code list and the deferral storage have no source (GAP-2828), the three consumed contracts carry no dependency row (GAP-2829), R-LIT-44 is named by two legacy keys and is declared once (GAP-2830), and the monolith scheduler behind the review date has no target equivalent (GAP-2831).

### 3. Preconditions

- The service template and the naming library are available (`RWB-PLT-TPL`, `RWB-PLT-E1047-CON`), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the idempotency rule and the pagination convention are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `legal_action` and `hearing` are S4's, `recovery_case`, `queue`, `assignment` and `task` are P3's, `rule_row` and `decision_log_entry` are P7's, `document` is P5's and the payment rows are P8's. This document never declares another service's operation as provided.
- The three consumed owner contracts are named as documents and built against their fakes: rwb-case for the case read and the case answer with the queue placement, and rwb-decision for the rule package. No source read for this key names their operations, so all three rows carry the placeholder (GAP-2829; ASM-4682).
- The LITIGATION rule package with R-LIT-55 and R-LIT-44 and its D7 route set are governed in rwb-decision; this baseline consumes them and declares neither (GAP-2828; ASM-4681).
- The deferral reason, its code list and the review-date rule are reference values whose content no source gives for this key; the element names are those of R-LIT-55 (GAP-2828; ASM-4681).
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract description of the step: its two provided operations, its consumed facts, its own durable timer and decision record, and its error conditions.
2. Fix the schemas `LegalActionUpdate` and `LegalAction` over DF-LEG-001 to DF-LEG-014 with the deferral element of R-LIT-55.
3. Fix the two operations on the base of DP-13 with their rights, their errors and the repeat rule.
4. Fix the case read and the case answer of rwb-case: the stage state, the move, the queue placement, the role, the review date, the rule ID and the package version.
5. Fix the rule package read of rwb-decision and the decision-record element of DP-03, written before anything changes.
6. Fix the durable review-date timer of `LitigationWorkflow` and the return to `ENFORCEMENT_DECISION` under R-LIT-56.
7. Record the no-column declaration and the prohibition on a duplicate judgment contract of R-LIT-44.
8. Publish the contract tables of section 12 and the five contract fakes.
9. Add the contract tests: schemas, vocabularies, error envelope, rights, placeholders, the absence of a third operation, of an event, of a Schedule, of a deferral column and of a `v_ace_*` read, and the drift between a fake and the document.
10. Tag the baseline and hand it to `RWB-S4-E5020-APP`, SCR-20 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body of a request or of an answer fails schema validation | The build fails on the schema lint; a deployed service answers 400 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A consumed or answered field list is not given by any source | The row carries the placeholder, the gap and the assumption, and the fake derives from the published document | None | AC3, AC4 |
| X5 | A state name, a stage name or a message outside its vocabulary appears in the document or an example | The vocabulary test fails the build | None | AC1 |
| X6 | The document declares a third operation, an event, a Schedule, a deferral column, a `timer` row or a second judgment contract | The absence test of AC8 fails the build | None | AC6, AC8 |
| X7 | A written `recovery_case`, `queue`, `assignment` or `task` property, or a rule property, appears | The boundary test fails; the review rejects the baseline | None | AC3, AC4 |
| X8 | The same deferral is described twice with the same reference and review date | The document describes the stored answer and no second effect | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the Ownership Map and the published owner documents only |
| Negotiable | The element names beyond the ones the sources give, the examples and the fake fixtures are settled in the baseline review; the operations, the vocabularies, the base, the topic and the queue are fixed |
| Valuable | Unblocks `RWB-S4-E5020-APP`, SCR-20 and the wave 3 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One contract document with its AsyncAPI absence note, nine contract tables, five fakes and four contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the enforcement-deferral step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of recovery_case, queue, assignment and task is P3 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The deferral element, the action schema and the vocabularies are fixed (new, D-RCV-60)
    Given the schema section of the baseline
    When it is compared with DF-LEG-001 to DF-LEG-014 of TSD S4 T3.1 and with T3.2
    Then LegalAction is declared with id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no, red_case_no, court_name, claim_amount, filed_date, judgment_date, judgment_amount, lit_status and status
    Then LegalActionUpdate is declared with the deferral element: deferral_reason and deferral_review_date, both required, as R-LIT-55 names them
    Then the stage vocabulary is declared with exactly ENFORCEMENT_DECISION and DEFERRAL_RECORDED for this step, and the return state ENFORCEMENT_DECISION of R-LIT-56
    Then LOV-LEGAL-STATUS is declared with exactly OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN and no deferred or deferral-reason value is added to it
    Then the reason code list is declared as a versioned reference value whose content is Not specified in the source documents (GAP-2828; ASM-4681)

  Scenario: AC2 The two provided operations, their rights and their errors are declared (new, D-RCV-60)
    Given the operation section of the baseline
    When it is compared with TSD S4 T-A.1, T-A.2 and T6.1
    Then PATCH /legal-actions/{legalActionId} is declared with Litigation right U, LegalActionUpdate in and LegalAction out (API-S4-004)
    Then GET /legal-actions/{legalActionId} is declared with Litigation right R and LegalAction out, its action type, its status and its court facts included (API-S4-003)
    Then each operation carries its error set of 401, 403, 404, 409, 422 and 503 as T-A.2 gives it, one envelope and one message ID per condition
    Then no third operation is declared beyond these two, the legal-action create of API-S4-002, the hearing create of API-S4-005 and the notice approve of API-S4-001, which belong to the sibling stories
    Then a repeated PATCH with the same deferral reference and review date is described as answering the stored result and no second effect

  Scenario: AC3 The case read, the case answer and the queue placement are declared (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case, queue, assignment and task
    Then the read is declared with the stage state, which must be ENFORCEMENT_DECISION for R-LIT-55
    Then the answer is declared with the stage outcome DEFERRAL_RECORDED, the rule ID, the package version and the review date
    Then the queue placement is declared with the queue code, the team, the owner role RW-ENFORCE and the task request, and the return to ENFORCEMENT_DECISION when the timer fires
    Then the document declares no recovery_case property, no queue property, no assignment property and no task property of its own
    Then the operation names are Not specified in the source documents (GAP-2829; ASM-4682) and both rows carry the placeholder

  Scenario: AC4 The rule package read and the decision-record element are declared (new, D-RCV-60)
    Given the rule and decision sections of the baseline
    When they are compared with the LITIGATION route set and the local library of DP-03
    Then the package is declared as consumed from P7 rwb-decision with R-LIT-55, R-LIT-44 and its version in force
    Then one decision record is declared per deferral with the case reference, the legal action reference, the rule ID, the package version, the deferral reason, the review date, the inputs reference and the stage outcome
    Then the record is declared as written through the library before anything changes, and a stopped chain leaves the stage and the case unchanged with MSG-P7-003
    Then the operation name is Not specified in the source documents (GAP-2829; ASM-4682)

  Scenario: AC5 The review date is declared as a durable timer of LitigationWorkflow (new, D-RCV-60)
    Given the timer section of the baseline
    When it is compared with the ownership rows (Jobs 0, Workflows 1) and the state transitions of TSD S4 T4
    Then the review date of R-LIT-55 is declared as one durable timer of LitigationWorkflow on queue rwb-litigation
    Then the fire of the timer is declared to answer the case move back to ENFORCEMENT_DECISION under R-LIT-56
    Then the document declares no timer row, no Temporal Schedule, no Quartz row, no shared job table and no use of the Workbench scheduler named by the rule
    Then a deviation is declared to pause no review date, because a legal deadline is never paused
    Then the second-deferral routing of R-LIT-57 is left to rwb-writeoff and is not declared here

  Scenario: AC6 The deferral is declared as a no-column fact and the judgment contract is not duplicated (new, D-RCV-60)
    Given the data section of the baseline
    When it is compared with DF-LEG-001 to DF-LEG-014 and with the legacy criterion AC3
    Then deferral_reason and deferral_review_date are declared as inputs and decision-record facts with no column and no list value
    Then no column of legal_action is declared as written by the deferral, and the status is declared unchanged
    Then R-LIT-44 and the judgment write are named as the contract of RWB-S4-E5016-APP and no second judgment element, operation or write is declared here (GAP-2830; ASM-4683)
    Then no ACE table, ACE view or cross-schema join appears in the document or in a fake
    Then the legacy criterion AC3 of the judgment write is proved here as a regression through the same contract, and the boundary is declared in the absence test of AC8

  Scenario: AC7 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the case fake answers the stage state "ENFORCEMENT_DECISION", another state, an accepted move DEFERRAL_RECORDED with the queue placement for RW-ENFORCE, and a refused move
    Then the rule-package fake answers the LITIGATION package with R-LIT-55 and R-LIT-44 and a second version
    Then the decision-record stub answers a healthy chain and a stopped chain, the composite route fake answers the merged SCR-20 enforcement-decision and deferred models, and the partner-portal fake answers the firm's entry under PT-LAWFIRM
    Then no answer exceeds 2 s and the drift test fails the build on any difference with the document

  Scenario: AC8 The naming baseline, the table ownership and the absence tests are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema and the login are rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as this service's are legal_action, hearing, decision_record and idempotency_key, and recovery_case, queue, assignment, task, rule_row, decision_log_entry, document and the payment rows are named as other owners'
    Then the document declares no event published, no event consumed, no Schedule and no v_ace_* read, and the absence test fails a build that adds one

  Scenario: AC9 Each business rule of section 8 is declared or prohibited as the section states (new, D-RCV-60)
    Given the business rules table of section 8
    When each of BR1 to BR11 is compared with its source column
    Then each rule is declared or prohibited as the table states
    Then the rules that are architecture constraints are proved by the absence tests of AC8 and the additive-version check, not by a second criterion

  Scenario: AC10 A retried or timed-out activity answers the stored result and no second effect (new, D-RCV-60)
    Given the operations and the review-date timer of the baseline
    When an activity is retried or reaches its timeout
    Then the retry is declared to answer the stored result with no second effect, as AC2 states for a repeated PATCH
    Then the timeout value is Not specified in the source documents (NEWAC-RWB-S4-E5020-CON-AC10)
```

The ten criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by `RWB-S4-E5020-APP`, which owns the four legacy criteria AC1 to AC4 word for word, and they declare no judgment contract, because R-LIT-44 is RWB-S4-E5016-CON's surface (GAP-2830; ASM-4683).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The enforcement-deferral step of the litigation journey is rwb-litigation's, and the contract declares its operations, its vocabularies, its timer, its record and the facts it consumes and nothing else | Context pack ownership rows; FSD S4 A2.20 |
| BR2 | The legal action is this service's and is reached on the two operations of TSD S4 T-A.1 only | Context pack ownership rows; TSD S4 T3.1, T-A.1 |
| BR3 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-020 AC1 and AC4 |
| BR4 | The case, its stage state, the queue, the assignment and the task stay with rwb-case: the contract declares the read, the answer and the queue placement and declares no such property | Context pack ownership rows; TSD S4 T5.2; GAP-2829 |
| BR5 | The two rules are governed in rwb-decision and are named here, never declared here; R-LIT-44 is the judgment contract of RWB-S4-E5016-CON and is not re-declared | GAP-2828, GAP-2830; ASM-4683 |
| BR6 | The deferral reason and the review date are inputs and record facts; no column and no list value is declared for them, and the status list keeps its six values | TSD S4 T3.1, T3.2; GAP-2828 |
| BR7 | No ACE view and no ACE table is read: the service holds no `v_ace_*` grant | DP-05 applied as a prohibition |
| BR8 | No personal data in a fact, an answer, an example or a fake: references, dates, codes and a rule version only | Template and Rules §R7.2 (s17) |
| BR9 | One base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A change is additive within major version 1; a breaking change is a new major version | Architecture v5 backward-compatibility rule |
| BR11 | The review date is a durable timer of `LitigationWorkflow`; the Workbench scheduler named by R-LIT-55 has no target equivalent and no Schedule is declared | GAP-2831; ASM-4684 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the three consumed facts, the timer, the record and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-20, the wave 3 harness and the rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a vocabulary value or an operation changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a third operation, an event, a Schedule, a deferral column or a `v_ace_*` read | In review |

The state machine of the case is the app story's own, from TSD S4 T4 and the Business Rules and Routing Logic v4: `ENFORCEMENT_DECISION` to `DEFERRAL_RECORDED` under R-LIT-55, and `DEFERRAL_RECORDED` to `ENFORCEMENT_DECISION` under R-LIT-56 when the review date is reached. The stage of `LitigationWorkflow` is this service's and the state is written by rwb-case on this baseline's answer shape.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the contract document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and a correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, SCR-20, the wave 3 harness and the owners of rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the idempotency rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in a fact, an answer, an example or a fake |

The per-service login behind the security scheme is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

The rights check on both operations is the rwb-access authorise check (DP-08); its name and its call shape are Not specified in the source documents (DOR-RWB-S4-E5020-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Legal action element | Not specified in the source documents (DOR-RWB-S4-E5020-CON-7) | `legal_action` of `rwb_litigation`, DF-LEG-001 to DF-LEG-014: id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no, red_case_no, court_name, claim_amount, filed_date, judgment_date, judgment_amount, lit_status, status |
| Deferral element | Not specified in the source documents (DOR-RWB-S4-E5020-CON-7) | `deferral_reason` and `deferral_review_date`, both required by R-LIT-55; inputs and record facts only, no column (GAP-2828; ASM-4681) |
| Stage vocabulary | Not specified in the source documents (DOR-RWB-S4-E5020-CON-7) | `ENFORCEMENT_DECISION`, `DEFERRAL_RECORDED` and the return state `ENFORCEMENT_DECISION` of R-LIT-56 |
| Case answer | Not specified in the source documents (DOR-RWB-S4-E5020-CON-7) | The stage state, the stage outcome, the queue code, the team, the role `RW-ENFORCE`, the task request, the rule ID and the package version, all P3's |
| Decision record | Not specified in the source documents (DOR-RWB-S4-E5020-CON-7) | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) |
| Rule rows | Not specified in the source documents (DOR-RWB-S4-E5020-CON-7) | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, read as the package in force (GAP-2828) |
| Timer | Not specified in the source documents (DOR-RWB-S4-E5020-CON-7) | The review date as one durable timer of `LitigationWorkflow`; no column, no Schedule, no job row (GAP-2831; ASM-4684) |
| Reference data | Not specified in the source documents (DOR-RWB-S4-E5020-CON-7) | Lists and parameters read: the reason code list has no source (GAP-2828; ASM-4681); the parameter names and the reference-data contract (DP-06, DP-07) are Not specified in the source documents (DOR-RWB-S4-E5020-CON-20) |
| Not written here | Not specified in the source documents (DOR-RWB-S4-E5020-CON-7) | `recovery_case`, `queue`, `assignment` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), the payment rows (P8), every `v_ace_*` view (P1) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the stage vocabulary of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story, and in particular no column for the reason or the review date (BR6).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Errors |
|---|---|---|---|---|
| PATCH | `/legal-actions/{legalActionId}` | Record the deferral or another enforcement step (API-S4-004) | Litigation U | 401, 403, 404, 409, 422, 503; no idempotency header |
| GET | `/legal-actions/{legalActionId}` | Read the action with its type, its status and its court facts (API-S4-003) | Litigation R | 401, 403, 404, 503 |

Base `/api/recovery/litigation/v1`. The two rows are the whole surface of this step; `POST /cases/{caseId}/legal-actions` (API-S4-002), `POST /legal-actions/{legalActionId}/hearings` (API-S4-005) and `POST /notices/{noticeId}/approve` (API-S4-001) stay with the sibling stories of this service, and a third operation here fails the review and the absence test (BR2; AC2, AC8).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `Not specified in the source documents (GAP-2829; ASM-4682)` | `/api/recovery/case/v1` | P3 rwb-case | The stage state of the case, which must be `ENFORCEMENT_DECISION` for R-LIT-55; faked |
| The stage answer of `CaseWorkflow` (`Not specified in the source documents (GAP-2829; ASM-4682)`) | rwb-case (P3) | P3 rwb-case | The stage outcome `DEFERRAL_RECORDED`, the return to `ENFORCEMENT_DECISION`, the queue code, the team, the role `RW-ENFORCE`, the review date, the rule ID and the package version; faked |
| `Not specified in the source documents (GAP-2829; ASM-4682)` | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version with R-LIT-55 and R-LIT-44; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All three are C dependencies in fact and not in the metadata row, and the absence is recorded as GAP-2829 with ASM-4682.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. This baseline declares no event, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. `DEFER_RECORDED` is an event of the state machine in the Business Rules and Routing Logic v4, not a Kafka subscription: the service holds no consumer group and no inbox, and every fact arrives on the contracts of 12.2 or as a signal of the workflow (GAP-2829; ASM-4682).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new | `rwb-litigation` | The stage that hosts the step; its signals and its outcome for the parent are declared, not built; it holds the review-date timer |
| `recordEnforcementDeferral` | Activity | `rwb-litigation` | The deferral element in; the decision record, the rule ID with its version, the stage move and the case answer with the queue placement out |
| `armReviewDate` | Activity | `rwb-litigation` | The review date in; one durable timer out, and on the fire the case move back to `ENFORCEMENT_DECISION` |

The activity and signal names are target design choices and are fixed by no source. No activity is registered by this story.

Workflow ID form: Not specified in the source documents (CG-ALL-9530). Start trigger per Temporal Catalog v1: Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02). Start or signalWithStart and duplicate-start policy: Not specified in the source documents (CG-ALL-9530).

#### 12.6 Schedules

None. The review date of R-LIT-55 is a durable timer of `LitigationWorkflow`. This baseline declares no Temporal Schedule, no Quartz row, no `timer` row, no shared job table and no batch window, and no Job of the batch catalogue is owned or moved here (GAP-2831; ASM-4684).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read only for this step; no business column is contracted as written and the status is unchanged |
| hearing | S4 (`rwb_litigation`) | This service's, not read by this step |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked record of the deferral (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of a repeated deferral |

`recovery_case`, `queue`, `assignment` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5) and the payment rows (P8) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case fake | The stage state `ENFORCEMENT_DECISION` and another state, an accepted move `DEFERRAL_RECORDED` with the queue placement for `RW-ENFORCE`, the return to `ENFORCEMENT_DECISION` and a refused move; no answer beyond 2 s | AC3, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-55 and R-LIT-44, and a second version | AC4, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain that answers MSG-P7-003 | AC4, AC7 |
| gateway-bff composite route fake | The merged SCR-20 model in the enforcement-decision state and in the deferred state for case `RC-2026-000820` | AC7 |
| Partner-portal entry fake | The firm's deferral entry under PT-LAWFIRM through the PATCH operation, and a refused entry for an action outside the firm's scope | AC2, AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the three consumed rows and the reason code list are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2828, GAP-2829).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The action update and the action read; the case read, the case stage answer with the queue placement and the rule package read; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 2 activities declared, 0 registered, 1 durable timer | `LitigationWorkflow`, `recordEnforcementDeferral`, `armReviewDate` and the review date; no Schedule |
| File | None | No file is read or written by this step |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no action and no case. What it publishes is one contract description, one AsyncAPI absence note that declares no event, nine contract tables and five fakes.

**Deliverables.** The contract document `contracts/rwb-litigation-enforcement-deferral.v1.yaml` with the two schemas and the stage vocabulary as published reference values, the operation descriptions with their rights and errors, the timer element of `LitigationWorkflow`, the contract README rows with their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: the document declares no `v_ace_*` read and no ACE grant, because rwb-litigation holds neither. DP-01 is declared because the document names only its own schema. DP-09, DP-10 and DP-14 are outside the pattern set, which is why 12.3 and 12.4 declare no event and 12.6 declares no Schedule (GAP-2831; ASM-4684).

**Build steps**

1. Write the two schemas, the deferral element and the stage vocabulary of AC1 as published reference values and validate them in the pipeline.
2. Write the two operation descriptions of AC2 with their rights, their errors and the repeat rule.
3. Write the case read, the stage answer and the queue placement of AC3 with their placeholders.
4. Write the rule package read and the decision-record element of AC4.
5. Write the timer element and the return under R-LIT-56 of AC5, and validate them against the workflow contract.
6. Write the no-column declarations and the judgment-contract boundary of AC6 with their absence tests.
7. Publish the five fakes of AC7 and the drift test.
8. Record the naming baseline and the absence tests of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The contract tests pass, the vocabulary is published as reference values, the five fakes answer every consumed path and the drift test is green, and the absence tests block a third operation, an event, a Schedule, a deferral column, a `timer` row and a `v_ace_*` read.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key; it names a missing item of the pack, which is the pack story's path | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key; it names the expiry of the claim, which the case read reports | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a fact or an answer is absent or invalid, which is VR-S4-020-1 of the FSD | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and their text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-20 Enforcement workspace in its enforcement-decision and deferred reading, through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the action and its deferral and rwb-case for the stage state and the queue; this baseline fixes the rwb-litigation side only, and the composite route specification and the screen field list belong to `RWB-PLT-N001-CON`. The legacy state list of SCR-20 carries no deferred state and no source gives a field list for the reason or the review date, so the deferred reading is declared here and the absence is recorded (GAP-2832; ASM-4685). The deferred reading shows the reason, the review date and the rule version; its field list and merge order belong to `RWB-PLT-N001-CON`. The states empty, loading, error and no access of SCR-20 are not in the screen specification and are Not specified in the source documents (CG-ALL-9534). The refusal and not-recorded states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-020-01 | AC1, AC2 | Contract | The contract half of "Record an enforcement deferral with its reason": the deferral element, the action schema and the two operations answer the document |
| TC-E5-020-02 | AC1, AC4 | Contract | The contract half of "Rule R-LIT-55": the two required elements and their record are declared, and no column is declared for them |
| TC-E5-020-03 | AC6 | Contract | The contract half of "Rule R-LIT-44": the judgment contract is named as RWB-S4-E5016-CON and nothing of it is re-declared here |
| TC-E5-020-04 | AC4 | Contract | The contract half of "Not recorded": a stopped decision-record chain answers MSG-P7-003 and describes no change |
| TC-E5-020-05 | AC2 (access path) | Contract | A role without the Litigation right is refused with MSG-P4-002 on both operations |
| TC-E5-020-06 | AC6 (source boundary) | Contract | Every ACE row is refused by the boundary test and no deferral column is declared |
| TC-S4-E5020-CON-01 | AC1, AC2 | Contract | The two schemas, the stage vocabulary, the two operations, their rights and their error sets validate; no third operation is declared |
| TC-S4-E5020-CON-02 | AC3, AC4 | Contract | The case read, the stage answer with the queue placement and the rule package read each carry their placeholder, one hop with a 2 s budget |
| TC-S4-E5020-CON-03 | AC5, AC6 | Contract | The review-date timer, the return under R-LIT-56, the no-column declaration and the ACE prohibition validate; no Schedule, no `timer` row and no `v_ace_*` read is declared |
| TC-S4-E5020-CON-04 | AC7, AC8 | Contract | The five fakes match the document and a drifted fake fails the build; the absence tests for a third operation, an event, a Schedule, a deferral column and a `v_ace_*` read |
| TC-S4-E5020-CON-05 | AC6 | Contract | Boundary of the owned tables: the tables of §12.7 are the only ones declared as owned, `legal_action` is read with no business column contracted, and no table outside that list is declared |
| TC-S4-E5020-CON-06 | BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 | Contract | Each rule of §8 is declared or prohibited as §8 states |
| TC-S4-E5020-CON-07 | AC9 | Contract | Each rule BR1 to BR11 of §8 is declared or prohibited as §8 states, and the architecture constraints are proved by the absence tests of AC8 |
| TC-S4-E5020-CON-08 | AC10 | Contract | A retried or timed-out activity answers the stored result with no second effect; the timeout is Not specified in the source documents (NEWAC-RWB-S4-E5020-CON-AC10) |

The six legacy cases are the legacy cases of RWB-E5-020 in their legacy order, carried as the contract half: their Covers column names the criteria of this story that fix the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by `RWB-S4-E5020-APP`. The legacy level maps to `Contract` here because the artefact under test is the contract. The eight cases `TC-S4-E5020-CON-01` to `-08` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the review-date rule, the route set, the LOV values and the message texts stay reference rows, never schema defaults or enumeration members of the code.
- No personal data in a fact, an answer, an example or a fake: references, dates, codes and a rule version only; every example is synthetic.
- The case stays with rwb-case: the document declares no `recovery_case`, `queue`, `assignment` or `task` property and no write of any of them (BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on ACE, and the boundary test fails a build that adds one (DP-05, BR7).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or operation as its own fails the review (DP-13, DP-14, BR9).
- No third operation, no event, no Schedule, no Quartz row, no `timer` row and no deferral column: the absence tests of AC8 fail a build that declares one (BR2, BR6, BR11).
- No second judgment contract: R-LIT-44 and its element stay in RWB-S4-E5016-CON, and a duplicate here fails the review (BR5; GAP-2830).
- The error envelope, the idempotency rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement (FSD S4 Requirements served); the legacy master carries no requirement ID for this key, so this is a mapping of FEAT-LIT-20 under L3 process 08 Litigation (GAP-2833; ASM-4686) | The deferral element, the case answer with the queue placement and the two operations | TC-E5-020-01, TC-E5-020-02, TC-S4-E5020-CON-01 |
| R-LIT-55, R-LIT-44 | The deferral with a coded reason and a review date, and the judgment for the bank | The rule package read, the record element and the stage answer | TC-E5-020-01, TC-E5-020-02, TC-E5-020-03, TC-S4-E5020-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows and the two provided operations | TC-S4-E5020-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-020, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by `RWB-S4-E5020-APP`; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases |
| Feature and screens | FEAT-LIT-20, SCR-20 Enforcement workspace and SCR-19 Litigation workspace |
| Rules | R-LIT-55 and R-LIT-44, named and governed in rwb-decision (GAP-2828) |
| Judgment surface | RWB-S4-E5016-CON and RWB-S4-E5016-APP, which own R-LIT-44 and the judgment write (GAP-2830) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the step, the evaluation of R-LIT-55, the decision record, the stage move, the timer and the case answer: `RWB-S4-E5020-APP`.
- The judgment element, the judgment write and its operation surface: `RWB-S4-E5016-CON` and `RWB-S4-E5016-APP` (GAP-2830; ASM-4683).
- The case of record, the stage state, the parent `CaseWorkflow`, the queue, the assignment and the task rows: rwb-case (P3) (GAP-2829; ASM-4682).
- The authoring, testing, approval and versioning of the LITIGATION package and of R-LIT-55 and R-LIT-44, and the reason code list itself: rwb-decision (P7) and the reference-data owner of rwb-case (GAP-2828; ASM-4681).
- The return on the review date under R-LIT-56 as a separate behaviour, and the second deferral that routes the case to write-off under R-LIT-57: the timer continuation of the app story and rwb-writeoff (S7) (GAP-2831; ASM-4684).
- The asset trace, the writ, the seizure, the auction and the payment match: the enforcement stories of this service, rwb-asset (S5) and rwb-payment (P8).
- The rights, roles, scope and masking data themselves, the screen field list, the merge order of SCR-20 and the deferred screen state: rwb-access (P4), RWB-PLT-N001-CON and GAP-2832 (ASM-4685).
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
