# RWB-S4-E5016-CON Record the judgment - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5016-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the judgment step of rwb-litigation, split from RWB-E5-016. It fixes the two operations on `/api/recovery/litigation/v1` with their schemas, the judgment element and the appeal-window element, the action status vocabulary, the case read and the case-move answer with the enforcement task request of rwb-case, the rule package read of rwb-decision, the decision-record element of DP-03, the durable-timer element of `LitigationWorkflow`, the error set and the fakes. The judgment type, the dismissal and the appeal window have no column (GAP-2811; ASM-4651); the `v_ace_lawsuit` read of the feature extract has no grant in this service (GAP-2812; ASM-4655). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the judgment step of rwb-litigation — the two operations with their schemas, the judgment and appeal-window elements, the action status vocabulary, the case read and case-move answer with the enforcement task request, the rule package read, the decision-record element, the durable-timer element, the error set and the fakes**, so that **the app story, the two workspaces and the wave 3 harness build against one fixed, testable surface on Day 1 and a judgment date, an amount, a judgment type or an answer shape can never drift between rwb-litigation, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (ADR-020). The legacy step crossed four boundaries in one process: the legal action row, the case row, the task row and the decision log entry. The target splits them: the action and its court facts stay here, the case and its route state and the enforcement task move to rwb-case, the rule answer and its record move to the library of DP-03 and the governed rule rows of rwb-decision. Each boundary is now something another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It records that this service holds no `v_ace_*` grant, so DP-05 is declared as a prohibition and the `v_ace_lawsuit` read of the feature extract appears on no row.

Three points are carried as gaps and assumptions rather than decided quietly: the judgment type, the dismissal and the appeal window have no column or list value (GAP-2811), the trigger and the ACE lawsuit read have no single source (GAP-2812), and the legacy key carries no requirement id (GAP-2813).

### 3. Preconditions

- The service template and the naming library are available (`RWB-PLT-TPL`, `RWB-PLT-E1047-CON`), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the idempotency rule and the pagination convention are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `legal_action` and `hearing` are S4's, `recovery_case` and `task` are P3's, `rule_row` and `decision_log_entry` are P7's, `treatment` is S2's, `document` is P5's and the payment rows are P8's. This document never declares another service's operation as provided.
- The three consumed owner contracts are named as documents and built against their fakes: rwb-case for the case read and the case-move answer with the task request, and rwb-decision for the rule package. No source read for this key names their operations, so all three rows carry the placeholder (GAP-2812; ASM-4653).
- The LITIGATION rule package with R-LIT-44 and R-LIT-45 and its D7 route set are governed in rwb-decision; this baseline consumes them and declares none of them (GAP-2812; ASM-4653).
- The judgment type values, the appeal window end and every LOV value are reference values whose content no source gives for this key beyond the words `full`, `partial`, `default` and `dismissed` of the two rules (GAP-2811; ASM-4651).
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract description of the step: its two provided operations, its three consumed facts, its own durable timer and decision record, and its error conditions.
2. Fix the schemas `LegalActionUpdate` and `LegalAction` over DF-LEG-001 to DF-LEG-014 with the judgment element, and the appeal-window element of R-LIT-45.
3. Fix the two operations on the base of DP-13 with their rights, their errors and their idempotency rule.
4. Fix the case read and the case-move answer of rwb-case: the route state, the move, the enforcement task request, the rule ID and the package version.
5. Fix the rule package read of rwb-decision and the decision-record element of DP-03, written before anything changes.
6. Fix the durable-timer element of `LitigationWorkflow` and the appeal window it holds.
7. Record the `v_ace_lawsuit` prohibition and the absence of a judgment-type or appeal-window column.
8. Publish the contract tables of section 12 and the five contract fakes.
9. Add the contract tests: schemas, vocabularies, error envelope, rights, placeholders, the absence of a third operation, of an event, of a Schedule and of a `v_ace_*` read, and the drift between a fake and the document.
10. Tag the baseline and hand it to `RWB-S4-E5016-APP`, SCR-19, SCR-20 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body of a request or of an answer fails schema validation | The build fails on the schema lint; a deployed service answers 400 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A consumed or answered field list is not given by any source | The row carries the placeholder, the gap and the assumption, and the fake derives from the published document | None | AC4, AC5 |
| X5 | A judgment type, an action status or a hearing outcome outside its vocabulary appears in the document or an example | The vocabulary test fails the build | None | AC1 |
| X6 | The document declares a third operation, an event, a Schedule, a judgment-type column or a `v_ace_*` read | The absence test of AC8 fails the build | None | AC8 |
| X7 | A written `recovery_case` property, a `task` property or a rule property appears | The boundary test fails; the review rejects the baseline | None | AC3, AC6 |
| X8 | The same judgment is described twice with the same reference and date | The document describes the stored answer and no second effect | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the Ownership Map and the published owner documents only |
| Negotiable | The element names beyond the ones the sources give, the examples and the fake fixtures are settled in the baseline review; the operations, the vocabularies, the base, the topic and the queue are fixed |
| Valuable | Unblocks `RWB-S4-E5016-APP`, SCR-19, SCR-20 and the wave 3 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One contract document with its AsyncAPI absence note, nine contract tables, five fakes and four contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the judgment step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of recovery_case and task is P3 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The judgment element, the action schema and the vocabularies are fixed (new, D-RCV-60)
    Given the schema section of the baseline
    When it is compared with DF-LEG-001 to DF-LEG-014 of TSD S4 T3.1 and with T3.2
    Then LegalAction is declared with id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no, red_case_no, court_name, claim_amount, filed_date, judgment_date, judgment_amount, lit_status and status
    Then LegalActionUpdate is declared with the judgment element: judgment_type, judgment_date, judgment_amount, red_case_no and appeal_window_ends
    Then judgment_type is declared with exactly full, partial, default and dismissed, as R-LIT-44 and R-LIT-45 name them
    Then LOV-LEGAL-STATUS is declared with exactly OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN and no dismissed or appeal value is added to it
    Then every vocabulary is published as a versioned reference value and none is an enumeration member of a schema or a constant of the code

  Scenario: AC2 The two provided operations, their rights and their errors are declared (new, D-RCV-60)
    Given the operation section of the baseline
    When it is compared with TSD S4 T-A.1, T-A.2 and T6.1
    Then PATCH /legal-actions/{legalActionId} is declared with Litigation right U, LegalActionUpdate in and LegalAction out (API-S4-004)
    Then GET /legal-actions/{legalActionId} is declared with Litigation right R and LegalAction out, hearing and judgment included (API-S4-003)
    Then each operation carries its error set of 401, 403, 404, 409, 422 and 503 as T-A.2 gives it, one envelope and one message ID per condition
    Then no third operation is declared beyond these two, the legal-action create of API-S4-002, the hearing create of API-S4-005 and the notice approve of API-S4-001, which belong to the sibling stories
    Then a repeated PATCH with the same judgment reference is described as answering the stored result and no second effect

  Scenario: AC3 The case read, the case-move answer and the enforcement task request are declared (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case and task
    Then the read is declared with the route state, which must be IN_HEARING for R-LIT-44 and R-LIT-45
    Then the answer is declared with the stage outcome JUDGMENT_RECORDED or JUDGMENT_DISMISSED, the rule ID and the package version
    Then the enforcement task request is declared with the task code, the owner role RW-ENFORCE, the due date and the rule ID
    Then the document declares no recovery_case property, no route-state column and no task property of its own
    Then the operation names are Not specified in the source documents (GAP-2812; ASM-4653) and both rows carry the placeholder

  Scenario: AC4 The rule package read and the decision-record element are declared (new, D-RCV-60)
    Given the rule and decision sections of the baseline
    When they are compared with the LITIGATION route set and the local library of DP-03
    Then the package is declared as consumed from P7 rwb-decision with R-LIT-44, R-LIT-45 and its version in force
    Then one decision record is declared per outcome with the case reference, the legal action reference, the rule ID, the package version, the judgment type, the judgment date, the judgment amount, the inputs reference and the stage outcome
    Then the record is declared as written through the library before anything changes, and a stopped chain leaves the action and the case unchanged with MSG-P7-003
    Then the operation name is Not specified in the source documents (GAP-2812; ASM-4653)

  Scenario: AC5 The appeal window is declared as a durable timer of LitigationWorkflow (new, D-RCV-60)
    Given the timer section of the baseline
    When it is compared with the ownership rows (Jobs 0, Workflows 1) and the state transitions of TSD S4 T4
    Then the appeal window of R-LIT-45 is declared as one durable timer of LitigationWorkflow on queue rwb-litigation
    Then the document declares no timer row, no Temporal Schedule, no Quartz row and no shared job table
    Then the window end is declared as a versioned reference value whose content is Not specified in the source documents (GAP-2811; ASM-4652)
    Then the declaration states that a deviation pauses no appeal window, because a legal deadline is never paused

  Scenario: AC6 The judgment, the dismissal and the ACE lawsuit read are declared as no-column facts (new, D-RCV-60)
    Given the data section of the baseline
    When it is compared with DF-LEG-001 to DF-LEG-014 and with the feature extract of FEAT-LIT-16
    Then judgment_date, judgment_amount and red_case_no are declared as columns of legal_action and no other judgment column is declared
    Then judgment_type, the dismissal and the appeal window end are declared as inputs and decision-record facts with no column and no list value
    Then the status write is declared to JUDGMENT on both paths and no write to ENFORCING is described
    Then the v_ace_lawsuit read named by the feature extract is declared as a prohibition, because this service holds no v_ace_* grant (GAP-2812; ASM-4655)
    Then no ACE table, ACE view or cross-schema join appears in the document or in a fake

  Scenario: AC7 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the case fake answers the route state "IN_HEARING", another state, and an accepted and a refused stage outcome with the enforcement task created for RW-ENFORCE
    Then the rule-package fake answers the LITIGATION package with R-LIT-44 and R-LIT-45 and a second version
    Then the decision-record stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged SCR-19 judgment model and SCR-20 requested model
    Then no answer exceeds 2 s and the drift test fails the build on any difference with the document

  Scenario: AC8 The naming baseline, the table ownership and the absence tests are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema and the login are rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as this service's are legal_action and hearing, and recovery_case, task, rule_row, decision_log_entry, treatment, document and the payment rows are named as other owners'
    Then the document declares no event published, no event consumed, no Schedule and no v_ace_* read, and the absence test fails a build that adds one
```

The eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by `RWB-S4-E5016-APP`, which owns the four legacy criteria AC1 to AC4 word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The judgment step of the litigation journey is rwb-litigation's, and the contract declares its operations, its vocabularies, its timer, its record and the facts it consumes and nothing else | Context pack ownership rows; FSD S4 A2.16 |
| BR2 | The legal action is this service's and is reached on the two operations of TSD S4 T-A.1 only | Context pack ownership rows; TSD S4 T3.1, T-A.1 |
| BR3 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-016 AC1 and AC4 |
| BR4 | The case, its route state and the enforcement task stay with rwb-case: the contract declares the read, the answer and the task request and declares no such property | Context pack ownership rows; TSD S4 T5.2; GAP-2811 |
| BR5 | The two rules are governed in rwb-decision and are named here, never declared here | GAP-2812; ASM-4653 |
| BR6 | The judgment type, the dismissal and the appeal window are inputs, a stage and a durable timer; no column and no list value is declared for them | TSD S4 T3.1, T3.2, T4; GAP-2811 |
| BR7 | No ACE view and no ACE table is read: the service holds no `v_ace_*` grant and the judgment arrives on the LIT interface and the partner portal | DP-05 applied as a prohibition; GAP-2812 |
| BR8 | No personal data in a fact, an answer, an example or a fake: references, dates, codes, amounts and a rule version only | Template and Rules §R7.2 (s17) |
| BR9 | One base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A change is additive within major version 1; a breaking change is a new major version | Architecture v5 backward-compatibility rule |
| BR11 | A staging judgment value is a state of the stage and a fact of the record; `LOV-LEGAL-STATUS` keeps its six values | TSD S4 T3.2; GAP-2811 |

### 9. State transitions

The lifecycle of this document, not of a judgment:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the three consumed facts, the timer, the record and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a vocabulary value or an operation changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a third operation, an event, a Schedule, a judgment column or a `v_ace_*` read | In review |

The state machine of the case is the app story's own, from TSD S4 T4: `IN_HEARING` to `JUDGMENT_RECORDED` under R-LIT-44, `IN_HEARING` to `JUDGMENT_DISMISSED` under R-LIT-45, and `JUDGMENT_DISMISSED` to `APPEAL_DECISION` under R-LIT-46. The state itself is written by rwb-case on this baseline's answer shape; the stage of `LitigationWorkflow` is this service's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the contract document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and a correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, SCR-19, SCR-20, the wave 3 harness and the owners of rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the idempotency rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in a fact, an answer, an example or a fake |

The per-service login behind the security scheme is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Legal action element | `legal_action` of `rwb_litigation`, DF-LEG-001 to DF-LEG-014: id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no, red_case_no, court_name, claim_amount, filed_date, judgment_date, judgment_amount, lit_status, status |
| Judgment element | `judgment_type` with exactly `full`, `partial`, `default` and `dismissed`; `judgment_date` (DF-LEG-011), `judgment_amount` (DF-LEG-012) and `red_case_no` (DF-LEG-007) as columns; the type is an input and a record fact only (GAP-2811; ASM-4651) |
| Appeal-window element | The window end of R-LIT-45, as a durable timer value; it has no column and its content is Not specified in the source documents (GAP-2811; ASM-4652) |
| Hearing element | `hearing` of `rwb_litigation`, DF-LEG-024 to DF-LEG-029, read by the app story as the hearing the judgment closes |
| Case answer | The route state, the stage outcome, the enforcement task request, the rule ID and the package version, all P3's |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) |
| Rule rows | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, read as the package in force (GAP-2812) |
| Not written here | `recovery_case` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `treatment` (S2), `document` (P5), the payment rows (P8), every `v_ace_*` view (P1) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabularies of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story, and in particular no column for the judgment type, the dismissal or the appeal window (BR6).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Errors |
|---|---|---|---|---|
| PATCH | `/legal-actions/{legalActionId}` | Record the judgment, the dismissal or another legal-action step (API-S4-004) | Litigation U | 401, 403, 404, 409, 422, 503; no idempotency header |
| GET | `/legal-actions/{legalActionId}` | Read the action with its hearings and its judgment (API-S4-003) | Litigation R | 401, 403, 404, 503 |

Base `/api/recovery/litigation/v1`. The two rows are the whole surface of this step; `POST /cases/{caseId}/legal-actions` (API-S4-002), `POST /legal-actions/{legalActionId}/hearings` (API-S4-005) and `POST /notices/{noticeId}/approve` (API-S4-001) stay with the sibling stories of this service, and a third operation here fails the review and the absence test (BR2; AC2, AC8).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `Not specified in the source documents (GAP-2812; ASM-4653)` | `/api/recovery/case/v1` | P3 rwb-case | The route state of the case, which must be `IN_HEARING` for both rules; faked |
| The stage answer of `CaseWorkflow` (`Not specified in the source documents (GAP-2812; ASM-4653)`) | rwb-case (P3) | P3 rwb-case | The stage outcome `JUDGMENT_RECORDED` or `JUDGMENT_DISMISSED`, the rule ID, the package version and the enforcement task request for RW-ENFORCE; faked |
| `Not specified in the source documents (GAP-2812; ASM-4653)` | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version with R-LIT-44 and R-LIT-45; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All three are C dependencies in fact and not in the metadata row, and the absence is recorded as GAP-2812 with ASM-4653.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. This baseline declares no event, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. `JUDGMENT_FOR_THE_BANK` and `JUDGMENT_AGAINST_THE_BANK` are events of the state machine in the Business Rules and Routing Logic v4, not Kafka subscriptions: the service holds no consumer group and no inbox, and every fact arrives on the contracts of 12.2 or as a signal of the workflow (GAP-2812; ASM-4654).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the step; its signals and its outcome for the parent are declared, not built; it holds the appeal-window timer |
| `recordJudgment` | Activity | `rwb-litigation` | The judgment element in; the action columns, the decision record, the rule ID with its version and the case move with the task request out |
| `armAppealWindow` | Activity | `rwb-litigation` | The dismissal and the window end in; the dismissal fact, the decision record, the case move and one durable timer out |

The activity and signal names are target design choices and are fixed by no source. No activity is registered by this story.

#### 12.6 Schedules

None. The appeal window of R-LIT-45 is a durable timer of `LitigationWorkflow`. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch window, and no Job of Architecture v5 is owned or moved here (GAP-2811; ASM-4652).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read and updated; `judgment_date`, `judgment_amount`, `red_case_no` and `status` are the written columns |
| hearing | S4 (`rwb_litigation`) | Read only, as the hearing the judgment closes |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked record of the judgment or the dismissal (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of a repeated judgment |

`recovery_case` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `treatment` (S2), `document` (P5) and the payment rows (P8) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case fake | The route state `IN_HEARING` and another state, and an accepted and a refused stage outcome carrying the enforcement task request for RW-ENFORCE; no answer beyond 2 s | AC3, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-44 and R-LIT-45, and a second version | AC4, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain that answers MSG-P7-003 | AC4, AC7 |
| gateway-bff composite route fake | The merged SCR-19 model in the judgment state and the SCR-20 model in the requested state for case `RC-2026-000716` | AC7 |
| Partner-portal entry fake | The firm's judgment entry under PT-LAWFIRM through the PATCH operation, and a refused entry for an action outside the firm's scope | AC2, AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the three consumed rows, the appeal window end and the judgment type vocabulary beyond the four values of the two rules are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2811, GAP-2812).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The action update and the action read; the case read, the case stage answer with the task request and the rule package read; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 2 activities declared, 0 registered, 1 durable timer | `LitigationWorkflow`, `recordJudgment`, `armAppealWindow` and the appeal window; no Schedule |
| File | None | No file is read or written by this step |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no action, no case and no task. What it publishes is one contract description, one AsyncAPI absence note that declares no event, nine contract tables and five fakes.

**Deliverables.** The contract document `contracts/rwb-litigation-judgment.v1.yaml` with the two schemas and the four vocabularies as published reference values, the operation descriptions with their rights and errors, the timer element of `LitigationWorkflow`, the contract README rows with their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: the document declares no `v_ace_*` read and no ACE grant, because rwb-litigation holds neither and the `v_ace_lawsuit` read of the feature extract has no home here (GAP-2812; ASM-4655). DP-04, DP-06 and DP-07 are outside the pattern set although the step reads rule rows and reference values; those reads are on the owners' contracts and carry no dependency row. DP-09 and DP-14 are not in the set either, which is why 12.3 and 12.4 declare no event.

**Build steps**

1. Write the two schemas, the judgment element and the four vocabularies of AC1 as published reference values and validate them in the pipeline.
2. Write the two operation descriptions of AC2 with their rights, their errors and the repeat rule.
3. Write the case read, the stage answer and the task request of AC3 with their placeholders.
4. Write the rule package read and the decision-record element of AC4.
5. Write the timer element of AC5 and validate it against the workflow contract.
6. Write the no-column declarations and the `v_ace_lawsuit` prohibition of AC6 with their absence tests.
7. Publish the five fakes of AC7 and the drift test.
8. Record the naming baseline and the absence tests of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The contract tests pass, the vocabularies are published as reference values, the five fakes answer every consumed path and the drift test is green, and the absence tests block a third operation, an event, a Schedule, a judgment-type column and a `v_ace_*` read.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key; it names a missing item of the pack, which is the pack story's path | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key; it names the expiry of the claim, which the case read reports | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a fact or an answer is absent or invalid | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The source product of a consumed read is stale after a late or failed ACE batch, which is VR-S4-016-1 of the FSD; the check is the owner's | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs are contract elements and their text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its judgment state and SCR-20 Enforcement workspace in its requested state, through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the action and its judgment, rwb-case for the route state and the enforcement task and rwb-decision for nothing on screen; this baseline fixes the rwb-litigation side only, and the composite route specification and the screen field list belong to `RWB-PLT-N001-CON`. The refusal, not-recorded and refused states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-016-01 | AC1, AC2 | Contract | The contract half of "Record the judgment": the judgment element, the action schema and the two operations answer the document |
| TC-E5-016-02 | AC4 | Contract | The contract half of "Not recorded": a stopped decision-record chain answers MSG-P7-003 and describes no change |
| TC-E5-016-03 | AC3 | Contract | The contract half of "Rule R-LIT-45": the dismissal and the appeal-window element are declared and the window is a durable timer |
| TC-E5-016-04 | AC4 (forced failure) | Contract | A forced decision-record write failure is described as changing nothing, and the fake proves the stopped chain |
| TC-E5-016-05 | AC2 (access path) | Contract | A role without the Litigation right is refused with MSG-P4-002 on both operations |
| TC-E5-016-06 | AC6 (source boundary) | Contract | The `v_ace_lawsuit` read and every ACE row are refused by the boundary test, and no judgment-type column is declared |
| TC-S4-E5016-CON-01 | AC1, AC2 | Contract | The two schemas, the four vocabularies, the two operations, their rights and their error sets validate; no third operation is declared |
| TC-S4-E5016-CON-02 | AC3, AC4 | Contract | The case read, the stage answer with the task request and the rule package read each carry their placeholder, one hop with a 2 s budget |
| TC-S4-E5016-CON-03 | AC5, AC6 | Contract | The appeal-window timer, the no-column declaration and the ACE prohibition validate; no Schedule, no timer row and no `v_ace_*` read is declared |
| TC-S4-E5016-CON-04 | AC7, AC8 | Contract | The five fakes match the document and a drifted fake fails the build; the absence tests for a third operation, an event, a Schedule, a judgment column and a `v_ace_*` read |

The six legacy cases are the legacy cases of RWB-E5-016 in their legacy order, carried as the contract half: their Covers column names the criteria of this story that fix the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by `RWB-S4-E5016-APP`. The legacy level maps to `Contract` here because the artefact under test is the contract. The four cases `TC-S4-E5016-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the 5 working days, the appeal window end, the LOV values and the message texts stay reference rows, never schema defaults or enumeration members of the code.
- No personal data in a fact, an answer, an example or a fake: references, dates, codes, amounts and a rule version only; every example is synthetic.
- The case stays with rwb-case: the document declares no `recovery_case`, route-state or `task` property and no write of any of them (BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on ACE, and the boundary test fails a build that adds one (DP-05, BR7).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or operation as its own fails the review (DP-13, DP-14, BR9).
- No third operation, no event, no Schedule, no Quartz row and no judgment-type column: the absence tests of AC8 fail a build that declares one (BR2, BR6).
- The error envelope, the idempotency rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement (FSD S4 Requirements served); the legacy master and TSD S4 T8 carry no requirement ID for this key (GAP-2813; ASM-4656) | The judgment element, the case-move answer with the task request and the two operations | TC-E5-016-01, TC-E5-016-02, TC-S4-E5016-CON-01 |
| R-LIT-44, R-LIT-45 | Judgment for the bank and judgment against the bank | The rule package read, the record element and the stage answer | TC-E5-016-01, TC-E5-016-03, TC-S4-E5016-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows and the two provided operations | TC-S4-E5016-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-016, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by `RWB-S4-E5016-APP`; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases |
| Feature and screens | FEAT-LIT-16, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-44 and R-LIT-45, named and governed in rwb-decision (GAP-2812) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the step, the evaluation of the two rules, the decision record, the column updates, the timer and the stage answer: `RWB-S4-E5016-APP`.
- The case of record, its route state, `CaseWorkflow` and the enforcement task row: rwb-case (P3) and its slice of this legacy key (GAP-2811).
- The authoring, testing, approval and versioning of the LITIGATION package, of R-LIT-44 and R-LIT-45 and of the appeal window value: rwb-decision (P7) and the reference-data owner (GAP-2811).
- The LIT lawsuit read, the ACE views and the partner portal's own contract: rwb-integration (P2), rwb-source-data (P1) and rwb-partner (S9) (GAP-2812).
- The pack, the notice, the firm instruction, the filing, the hearings and the prescription warning, and the three sibling operations of this service: the sibling stories of S4, rwb-document (P5) and rwb-comms (P6).
- The appeal after a dismissal (R-LIT-46 to R-LIT-49) and the enforcement after the judgment (R-LIT-50 to R-LIT-70): RWB-S4-E5014-APP and the enforcement stories of this service.
- The rights, roles, scope and masking data, and the composite route and screen field list of SCR-19 and SCR-20: rwb-access (P4) and `RWB-PLT-N001-CON`.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this key.
