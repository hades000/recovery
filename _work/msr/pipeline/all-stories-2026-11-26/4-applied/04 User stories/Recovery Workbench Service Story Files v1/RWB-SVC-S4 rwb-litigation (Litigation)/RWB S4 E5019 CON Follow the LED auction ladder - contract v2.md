# RWB-S4-E5019-CON Follow the LED auction ladder - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5019-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-019 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the LED auction ladder of rwb-litigation, split from RWB-E5-019. It fixes the three operations on `/api/recovery/litigation/v1` with their schemas, the auction element and the four ladder rounds, the action status vocabulary, the case read and the case-move answer with the enforcement task request of rwb-case, the rule package read of rwb-decision, the decision-record element of DP-03, the next-auction-date element of `LitigationWorkflow`, the error set and the six fakes. The ladder round, the price basis, the official value, the round result, the bid amount and the auction date have no column (GAP-2827; ASM-4673, ASM-4679); the three consumed owner operations are named by no source (GAP-2827; ASM-4653); this service holds no `v_ace_*` grant (GAP-2827; ASM-4677). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5019-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the LED auction ladder of rwb-litigation — the three operations with their schemas, the auction element with its four rounds, the action type and status vocabularies, the case read and case-move answer with the enforcement task request, the rule package read, the decision-record element, the next-auction-date element, the error set and the six fakes**, so that **the app story, the two workspaces and the wave 3 harness build against one fixed, testable surface on Day 1 and a round, a price basis, an official value or an answer shape can never drift between rwb-litigation, rwb-case and rwb-decision without a failing build**.

This is the contract slice of legacy RWB-E5-019. It owns the published surface of the ladder step and nothing of its behaviour; the three legacy acceptance criteria stay with `RWB-S4-E5019-APP` (GAP-2827; ASM-4673).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (ADR-020). The legacy step crossed four boundaries in one process: the legal action row, the case row, the task row and the decision log entry. In the target the action and its court facts stay here, the case and its route state and the enforcement task move to rwb-case, the rule answer stays in the LITIGATION package of rwb-decision and the record is the library of DP-03. Each boundary is now something another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with its retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It records that this service publishes and consumes no event and registers no Schedule, and that it holds no `v_ace_*` grant, so DP-05 and DP-10 are stated as prohibitions.

Three points are carried as gaps and assumptions rather than decided quietly: the auction facts have no column and the ladder states are stages, not list values (GAP-2827; ASM-4673); the trigger of the step and the three consumed operations have no single source (GAP-2827; ASM-4674, ASM-4653); and the legacy key carries no requirement id (GAP-2827; ASM-4675).

### 3. Preconditions

- The service template and the naming library are available (`RWB-PLT-TPL`, `RWB-PLT-E1047-CON`), so the base, the topic, the queue and the event names follow the platform rule and not a local choice.
- The platform error envelope, the idempotency rule and the pagination convention are the platform baseline; where this document narrows them it does so explicitly.
- Ownership is taken from the context pack and the Ownership Map only: `legal_action` and `hearing` are S4's; `recovery_case`, `task` and `assignment` are P3's; `rule_row` and `decision_log_entry` are P7's; the proceeds and ledger rows are P8's; `document` is P5's. This document never declares another service's operation as provided.
- The three consumed owner contracts are named as documents and built against their fakes: rwb-case for the case read and the case-move answer with the task request, and rwb-decision for the rule package. No source read for this key names their operations, so all three rows carry the placeholder (GAP-2827; ASM-4653).
- The LITIGATION rule package with R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67 at its version and the D7 route set are governed in rwb-decision; this baseline consumes them and declares none of them (GAP-2827; ASM-4653).
- The four price bases of official value, the 2 and 5 working days of R-LIT-65 and R-LIT-67 and every list value are reference values of the package and of reference data; no source gives them a column and this baseline declares no content for them beyond the four round rules (GAP-2827; ASM-4679).
- `legal_action` (DF-LEG-001 to DF-LEG-014) and `hearing` (DF-LEG-024 to DF-LEG-029) arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No approval is available in this run: the FSD and the TSD of this module are In review, so the baseline is published at status Draft and tagged when its own contract tests pass (GAP-2827; ASM-4676, ASM-4680).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract description of the step: its three provided operations, its three consumed facts, its own record and its own durable timer, and its error conditions.
2. Fix the schemas `LegalActionRequest`, `LegalActionUpdate` and `LegalAction` over DF-LEG-001 to DF-LEG-014 with the auction element, and the round element with its four rounds.
3. Fix the three operations on the base of DP-13 with their rights, their errors and their idempotency rule.
4. Fix the case read and the case-move answer of rwb-case: the route state, the three moves, the enforcement task request, the rule ID and the package version.
5. Fix the rule package read of rwb-decision and the decision-record element of DP-03, written before anything changes.
6. Fix the next-auction-date element of `LitigationWorkflow` and the four rounds it steps through.
7. Record the no-column declarations, the `v_ace_*` prohibition and the absence of an event, a Schedule and a third-party write.
8. Publish the nine contract tables of section 12 and the six contract fakes.
9. Add the contract tests: schemas, vocabularies, error envelope, rights, placeholders, the absence tests, and the drift between a fake and the document.
10. Tag the baseline and hand it to `RWB-S4-E5019-APP`, SCR-19, SCR-20 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body of a request or of an answer fails schema validation | The build fails on the schema lint; a deployed service answers 400 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A consumed or answered field list is not given by any source | The row carries the placeholder, the gap and the assumption, and the fake derives from the published document | None | AC3, AC4 |
| X5 | A round outside 1 to 4, a price basis outside the four bases of official value, or an action type or status outside its vocabulary appears in the document or an example | The vocabulary test fails the build | None | AC1, AC5 |
| X6 | The document declares a fourth operation, an event, a Schedule, an auction column or a `v_ace_*` read | The absence test of AC8 fails the build | None | AC6, AC8 |
| X7 | A `recovery_case` property, a `task` property, a proceeds property or a rule property is declared as this service's | The boundary test fails; the review rejects the baseline | None | AC3, AC4, AC6 |
| X8 | The same round is described twice with the same reference, round and date | The document describes the stored answer and no second effect | None | AC2 |

X1 to X6 are the contract-level paths of the legacy step, X7 is the DP-01 boundary and X8 is the repeat rule the app story builds to. The four price bases, the day counts and the D7 route set are values in force, so none is a schema default (GAP-2827; ASM-4679).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the Ownership Map and the published owner documents only |
| Negotiable | The element names beyond the ones the sources give, the examples and the fake fixtures are settled in the baseline review; the operations, the vocabularies, the base, the topic and the queue are fixed |
| Valuable | Unblocks `RWB-S4-E5019-APP`, SCR-19, SCR-20 and the wave 3 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One contract document with its AsyncAPI absence note, nine contract tables, six fakes and four contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the LED auction ladder of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of recovery_case and task is P3 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The auction element, the action schemas and the vocabularies are fixed (new, D-RCV-60)
    Given the schema section of the baseline
    When it is compared with DF-LEG-001 to DF-LEG-014 of TSD S4 T3.1 and with T3.2
    Then LegalAction is declared with id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no, red_case_no, court_name, claim_amount, filed_date, judgment_date, judgment_amount, lit_status and status
    Then LegalActionRequest and LegalActionUpdate are declared with the auction element: auction_round, auction_price_basis, official_value, round_result, bid_amount, auction_date and led_reference
    Then auction_round is declared with exactly 1, 2, 3 and 4 and auction_price_basis with exactly 100, 90, 80 and 70 percent of official value, as R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67 name them
    Then LOV-LEGAL-TYPE is declared with exactly NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION and LED_AUCTION and LOV-LEGAL-STATUS with exactly OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN
    Then every vocabulary is published as a versioned reference value and none is an enumeration member of a schema or a constant of the code

  Scenario: AC2 The three provided operations, their rights and their errors are declared (new, D-RCV-60)
    Given the operation section of the baseline
    When it is compared with TSD S4 T-A.1, T-A.2 and T6.1
    Then POST /cases/{caseId}/legal-actions is declared with Litigation right C, LegalActionRequest in and LegalAction out at 201 (API-S4-002)
    Then PATCH /legal-actions/{legalActionId} is declared with Litigation right U, LegalActionUpdate in and LegalAction out (API-S4-004)
    Then GET /legal-actions/{legalActionId} is declared with Litigation right R and LegalAction out, its court facts and its judgment included (API-S4-003)
    Then each operation carries its error set of 400, 401, 403, 404, 409, 422 and 503 as T-A.2 gives it, one envelope and one message ID per condition
    Then no fourth operation is declared beyond these three, the hearing create of API-S4-005 and the notice approve of API-S4-001, which belong to the sibling stories
    Then a repeated round with the same case, action, round and reference is described as answering the stored result and no second effect

  Scenario: AC3 The case read, the case-move answer and the enforcement task request are declared (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case, assignment and task
    Then the read is declared with the route state, which must be WRIT_AND_SEIZURE for R-LIT-63 and LED_AUCTION for R-LIT-65, R-LIT-66 and R-LIT-67
    Then the answer is declared with the stage outcome LED_AUCTION, PROCEEDS_MATCHED or NO_BID_AT_70, the rule ID and the package version
    Then the enforcement task request of R-LIT-67 is declared with the task code, the owner role RW-ENFORCE, the due date from the 5 working days and the rule ID
    Then the document declares no recovery_case property, no route-state column, no assignment property and no task property of its own
    Then the operation names are Not specified in the source documents (GAP-2827; ASM-4653) and both rows carry the placeholder

  Scenario: AC4 The rule package read and the decision-record element are declared (new, D-RCV-60)
    Given the rule and decision sections of the baseline
    When they are compared with the LITIGATION route set and the local library of DP-03
    Then the package is declared as consumed from P7 rwb-decision with R-LIT-63, R-LIT-65, R-LIT-66, R-LIT-67 and its version in force
    Then one decision record is declared per ladder step with the case reference, the legal action reference, the rule ID, the package version, the round, the price basis, the official value, the round result, the bid amount, the auction date, the inputs reference and the stage outcome
    Then the record is declared as written through the library before anything changes, and a stopped chain leaves the action and the case unchanged with MSG-P7-003
    Then the operation name is Not specified in the source documents (GAP-2827; ASM-4653)

  Scenario: AC5 The next auction date and the four rounds are declared as a durable timer and a package value (new, D-RCV-60)
    Given the timer and ladder sections of the baseline
    When they are compared with the ownership rows (Jobs 0, Workflows 1) and the state transitions of TSD S4 T4
    Then the next auction date of R-LIT-66 is declared as one durable timer of LitigationWorkflow on queue rwb-litigation
    Then the document declares no timer row, no Temporal Schedule, no Quartz row and no shared job table
    Then the four price bases and the 2 and 5 working days of R-LIT-65 and R-LIT-67 are declared as values of the package in force and not as schema defaults or code constants
    Then the declaration states that the ladder states LED_AUCTION, PROCEEDS_MATCHED and NO_BID_AT_70 are stages of the workflow and no value is added to LOV-LEGAL-STATUS to express one

  Scenario: AC6 The auction facts with no column and the ACE prohibition are declared (new, D-RCV-60)
    Given the data section of the baseline
    When it is compared with DF-LEG-001 to DF-LEG-014 and DF-LEG-024 to DF-LEG-029
    Then the action columns declared for writing are action_type and status with the standard record columns, and no auction column is declared
    Then the round, the price basis, the official value, the round result, the bid amount and the auction date are declared as inputs and decision-record facts with no column
    Then the v_ace_batch_status read of VR-S4-019-1 is declared as the owner's (P1) and as a prohibition here, because this service holds no v_ace_* grant (GAP-2827; ASM-4677)
    Then no ACE table, ACE view or cross-schema join appears in the document or in a fake, and no recovery_case, task, assignment, rule_row, decision_log_entry, proceeds or ledger write is declared

  Scenario: AC7 The six contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the case read fake answers the route state "WRIT_AND_SEIZURE" and "LED_AUCTION", another state, and an answer beyond 2 s
    Then the case-move fake answers the moves "LED_AUCTION", "PROCEEDS_MATCHED" and "NO_BID_AT_70" accepted with the enforcement task created for RW-ENFORCE, and a move refused because the case is not in the state the rule expects
    Then the rule-package fake answers the LITIGATION package with the four rules and a second version, the decision-record stub answers a healthy chain and a stopped chain, the composite route fake answers the merged SCR-20 and SCR-19 models and the partner-portal entry fake answers an accepted and a refused round entry under PT-LAWFIRM
    Then no answer exceeds 2 s and the drift test fails the build on any difference with the document

  Scenario: AC8 The naming baseline, the table ownership and the absence tests are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema and the login are rwb_litigation, the base is /api/recovery/litigation/v1, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as this service's are legal_action and hearing, and recovery_case, task, assignment, rule_row, decision_log_entry, document and the payment rows are named as other owners'
    Then the document declares no event published, no event consumed, no Schedule and no v_ace_* read, and the absence test fails a build that adds one
```

The eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by `RWB-S4-E5019-APP`, which owns the three legacy criteria AC1 to AC3 word for word and copies none of them here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The LED auction step is rwb-litigation's, and the contract declares its operations, its vocabularies, its timer, its record and the facts it consumes and nothing else | Context pack ownership rows; FSD S4 A2.19; TSD S4 T4 |
| BR2 | The legal action is this service's and is reached on the three operations of TSD S4 T-A.1 for this step only | Context pack ownership rows; TSD S4 T3.1, T-A.1 |
| BR3 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-019 AC1 and AC3 |
| BR4 | The case, its route state, the assignment and the enforcement task stay with rwb-case: the contract declares the read, the answer and the task request and declares no such property | Context pack ownership rows; TSD S4 T5.2; GAP-2827 |
| BR5 | The four ladder rules are governed in rwb-decision and are named here, never declared here | GAP-2827; ASM-4653 |
| BR6 | The round, the price basis, the official value, the round result, the bid amount and the auction date are inputs and record facts; no column and no list value is declared for them, and the ladder states are stages | TSD S4 T3.1, T3.2, T4; GAP-2827; ASM-4673 |
| BR7 | No ACE view and no ACE table is read: the service holds no `v_ace_*` grant and the LED and LIT facts arrive on the partner portal and on the LIT interface | DP-05 applied as a prohibition; GAP-2827; ASM-4677 |
| BR8 | No personal data in a fact, an answer, an example or a fake: references, dates, codes, percentages, amounts and a rule version only | Template and Rules §R7.2 (s17); TSD S4 T6.2 |
| BR9 | One base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A change is additive within major version 1; a breaking change is a new major version | Architecture v5 backward-compatibility rule |
| BR11 | The proceeds of a sold round are never a property here: R-LIT-65 declares the move `PROCEEDS_MATCHED` and the money is P8's and the proceeds story's | Context pack ownership rows; FSD S4 A2.22; GAP-2827; ASM-4678 |

### 9. State transitions

The lifecycle of this document, not of the ladder:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the three consumed facts, the auction element, the timer, the record and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| In review | Contract tests pass and no sign-off is available in this run | The baseline is tagged at status Draft and the sign-off is collected in the verification loop | Baselined (Draft) |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a vocabulary value or an operation changes, or a round or a price basis changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a fourth operation, an event, a Schedule, an auction column or a `v_ace_*` read | In review |

The ladder itself keeps the state machine of TSD S4 T4: `WRIT_AND_SEIZURE` to `LED_AUCTION` under R-LIT-63, `LED_AUCTION` to `LED_AUCTION` under R-LIT-66, `LED_AUCTION` to `PROCEEDS_MATCHED` under R-LIT-65 and `LED_AUCTION` to `NO_BID_AT_70` under R-LIT-67. The stage is written here; the case route state is rwb-case's on this baseline's answer shape (BR4; GAP-2827; ASM-4673).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the contract document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and a correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, SCR-19, SCR-20, the wave 3 harness and the owners of rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the idempotency rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in a fact, an answer, an example or a fake |

The per-service login behind the security scheme is named "the rwb-litigation login (DP-02)" and is not part of this baseline. No sign-off is available in this run, so the baseline is tagged by its own passing contract tests (GAP-2827; ASM-4680).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Legal action element | `legal_action` of `rwb_litigation`, DF-LEG-001 to DF-LEG-014: id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no, red_case_no, court_name, claim_amount, filed_date, judgment_date, judgment_amount, lit_status, status |
| Auction element | `auction_round` (1 to 4), `auction_price_basis` (100, 90, 80 or 70 percent of official value), `official_value`, `round_result` (sold or no bid), `bid_amount`, `auction_date` and `led_reference`: inputs of the operation and facts of the record only, with no column and no list value (GAP-2827; ASM-4673, ASM-4679) |
| Action type and status | `LOV-LEGAL-TYPE` incl. `LED_AUCTION`; `LOV-LEGAL-STATUS` as declared in AC1, where the ladder states are stages of the workflow and not list values |
| Hearing element | `hearing` of `rwb_litigation`, DF-LEG-024 to DF-LEG-029, read by the app story as the judgment hearing the enforcement follows |
| Case answer | The route state, the stage outcome, the enforcement task request, the rule ID and the package version, all P3's |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) |
| Rule rows | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, read as the package in force (GAP-2827; ASM-4653) |
| Not written here | `recovery_case`, `assignment` and `task` (P3), `rule_row` and `decision_log_entry` (P7), the proceeds and ledger rows (P8), `document` (P5), every `v_ace_*` view (P1) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabularies of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared, and in particular no column for the round, the price basis, the official value, the round result, the bid amount or the auction date (BR6).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Access | Errors |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | Open the legal action, the LED auction action at round 1 included (API-S4-002) | Litigation C | 401, 403, 404, 409, 422, 503; idempotency key required |
| PATCH | `/legal-actions/{legalActionId}` | Record a round of the ladder, its result and the next step (API-S4-004) | Litigation U | 401, 403, 404, 409, 422, 503; no idempotency header |
| GET | `/legal-actions/{legalActionId}` | Read the action with its court facts, its judgment and its status (API-S4-003) | Litigation R | 401, 403, 404, 503 |

Base `/api/recovery/litigation/v1` (DP-13). The three rows are the whole surface of this step; `POST /legal-actions/{legalActionId}/hearings` (API-S4-005) and `POST /notices/{noticeId}/approve` (API-S4-001) stay with the sibling stories of this service, and a fourth operation here fails the review and the absence test (BR2; AC2, AC8). 400 for a malformed request is carried on top of the T-A.2 sets because the auction element is validated before the rule fires.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `Not specified in the source documents (GAP-2827; ASM-4653)` | `/api/recovery/case/v1` | P3 rwb-case | The route state of the case, which must be `WRIT_AND_SEIZURE` or `LED_AUCTION` as the four rules expect; faked |
| The stage answer of `CaseWorkflow` (`Not specified in the source documents (GAP-2827; ASM-4653)`) | rwb-case (P3) | P3 rwb-case | The stage outcome `LED_AUCTION`, `PROCEEDS_MATCHED` or `NO_BID_AT_70`, the rule ID, the package version and the enforcement task request for RW-ENFORCE; faked |
| `Not specified in the source documents (GAP-2827; ASM-4653)` | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version with R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All three are C dependencies in fact and not in the metadata row, whose contract-dependency cell is None, and the absence is recorded as GAP-2827 with ASM-4653.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. This baseline declares no event, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. `SEIZURE_EXECUTED`, `ROUND_SOLD`, `ROUND_NO_BID` and `LADDER_EXHAUSTED` are events of the state machine in the Business Rules and Routing Logic v4, not Kafka subscriptions: the service holds no consumer group and no inbox, and every fact arrives on the contracts of 12.2 or as a signal of the workflow (GAP-2827; ASM-4674).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the step; its signals and its outcome for the parent are declared, not built; it holds the next-auction-date timer |
| `openLedAuction` | Activity | `rwb-litigation` | The seizure result in; the action, the record, the stage `LED_AUCTION` and the case-move answer out |
| `recordAuctionRound` | Activity | `rwb-litigation` | The round element in; the round fact, the record, the action update, the next auction date and the move `PROCEEDS_MATCHED` out |
| `closeUnsoldLadder` | Activity | `rwb-litigation` | The fourth no-bid round in; the unsold fact, the record, the move `NO_BID_AT_70` and the enforcement task request out |

The activity and signal names are target design choices and are fixed by no source. No activity is registered and no workflow is deployed by this story (GAP-2827; ASM-4674).

#### 12.6 Schedules

None. The next auction date of R-LIT-66 is a durable timer of `LitigationWorkflow`, read from the LED's date for the round. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch window, and no Job of the batch catalogue is owned or moved here (GAP-2827; ASM-4674).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read and written; `action_type` and `status` with the standard record columns are the written columns, and no auction column exists (BR6) |
| hearing | S4 (`rwb_litigation`) | Read only, as the judgment hearing the enforcement follows |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked record of each ladder step (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of a repeated round and the answer it holds |

`recovery_case`, `assignment` and `task` (P3), `rule_row` and `decision_log_entry` (P7), the proceeds and ledger rows (P8) and `document` (P5) are not owned by this baseline; it names them only as an answer, a rule version or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case read fake | The route state `WRIT_AND_SEIZURE` and `LED_AUCTION`, another state, and no answer beyond 2 s | AC3, AC7 |
| rwb-case case-move fake | The moves `LED_AUCTION`, `PROCEEDS_MATCHED` and `NO_BID_AT_70` accepted with the enforcement task created for RW-ENFORCE, and a move refused because the case is not in the state the rule expects | AC3, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67, and a second version | AC4, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain that answers MSG-P7-003 | AC4, AC7 |
| gateway-bff composite route fake | The merged SCR-20 model in the seized and auctioned states and the SCR-19 model in the judgment state for case `RC-2026-000719` | AC7 |
| Partner-portal entry fake | The Legal Execution Department's and the firm's round entry under `PT-LAWFIRM` through the PATCH operation, and a refused entry for an action outside the entry's scope | AC2, AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the three consumed rows, the element names of the auction element and the day counts behind the due date are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2827; ASM-4653, ASM-4679).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The action create, the action update and the action read on `/api/recovery/litigation/v1`; the case read, the case stage answer with the task request and the rule package read; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 3 activities declared, 0 registered, 1 durable timer | `LitigationWorkflow`, `openLedAuction`, `recordAuctionRound`, `closeUnsoldLadder` and the next auction date; no Schedule |
| File | None | No file is read or written by this step; the LED and LIT data arrives on the portal and the P2 contract |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no action, no case and no task. What it publishes is one contract description, one AsyncAPI absence note that declares no event, nine contract tables and six fakes.

**Deliverables.** The contract document `contracts/rwb-litigation-led-auction.v1.yaml` with the three schemas and the three vocabularies as published reference values, the operation descriptions with their rights and errors, the timer element of `LitigationWorkflow`, the contract README rows with their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: the document declares no `v_ace_*` read and no ACE grant, because rwb-litigation holds neither and the `v_ace_batch_status` check of VR-S4-019-1 is P1's (GAP-2827; ASM-4677). DP-10 is a prohibition too, since the next auction date is a workflow timer. DP-04, DP-06 and DP-07 are outside the pattern set although the step reads the rule package and reference values; those reads are on the owners' contracts and carry no dependency row. DP-09 and DP-14 are not in the set either, which is why 12.3 and 12.4 declare no event.

**Build steps**

1. Write the three schemas, the auction element and the three vocabularies of AC1 as published reference values and validate them in the pipeline.
2. Write the three operation descriptions of AC2 with their rights, their errors and the repeat rule.
3. Write the case read, the stage answer and the task request of AC3 with their placeholders.
4. Write the rule package read and the decision-record element of AC4.
5. Write the timer and ladder declarations of AC5 and validate them against the workflow contract.
6. Write the no-column declarations and the ACE prohibition of AC6 with their absence tests.
7. Publish the six fakes of AC7 and the drift test.
8. Record the naming baseline and the absence tests of AC8, then tag the baseline at status Draft and collect the consumer sign-off in the verification loop.

**Done when.** The contract tests pass, the vocabularies are published as reference values, the six fakes answer every consumed path and the drift test is green, and the absence tests block a fourth operation, an event, a Schedule, an auction column and a `v_ace_*` read.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key; it names a missing item of the pack, which is the pack story's path | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key; it names the expiry of the claim, which the prescription path of this service reports | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of the auction element or of an answer is absent or invalid | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The source product of a consumed read is stale after a late or failed ACE batch, which is VR-S4-019-1 of the FSD; the check is the owner's | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs are contract elements and their text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-20 Enforcement workspace in its requested, seized, auctioned and closed states and SCR-19 Litigation workspace in its judgment state, through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the action, its status and the round, rwb-case for the route state and the enforcement task and rwb-decision for nothing on screen; this baseline fixes the rwb-litigation side only, and the composite route specification and the screen field list belong to `RWB-PLT-N001-CON`. The not-recorded and refused states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-019-01 | AC1, AC2, AC5 | Contract | The contract half of "Follow the LED auction ladder": the auction element, the three operations and the four rounds answer the document |
| TC-E5-019-02 | AC3, AC5 | Contract | The contract half of "Rule R-LIT-67": the move `NO_BID_AT_70`, the task request for RW-ENFORCE and the exhausted ladder are declared |
| TC-E5-019-03 | AC4 | Contract | The contract half of "Not recorded": a stopped decision-record chain answers MSG-P7-003 and describes no change |
| TC-E5-019-04 | AC2 (access path) | Contract | A role without the Litigation right is refused with MSG-P4-002 on the three operations |
| TC-E5-019-05 | AC4 (forced failure) | Contract | A forced decision-record write failure is described as changing nothing, and the fake proves the stopped chain |
| TC-S4-E5019-CON-01 | AC1, AC2 | Contract | The three schemas, the three vocabularies, the three operations, their rights and their error sets validate; no fourth operation is declared |
| TC-S4-E5019-CON-02 | AC3, AC4 | Contract | The case read, the stage answer with the task request and the rule package read each carry their placeholder, one hop with a 2 s budget |
| TC-S4-E5019-CON-03 | AC5, AC6 | Contract | The next-auction-date timer, the no-column declaration and the ACE prohibition validate; no Schedule, no timer row and no `v_ace_*` read is declared |
| TC-S4-E5019-CON-04 | AC7, AC8 | Contract | The six fakes match the document and a drifted fake fails the build; the absence tests for a fourth operation, an event, a Schedule, an auction column and a `v_ace_*` read |

The five legacy cases are the legacy cases of RWB-E5-019 in their legacy order, carried as the contract half: their Covers column names the criteria of this story that fix the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by `RWB-S4-E5019-APP`. The legacy level maps to `Contract` here because the artefact under test is the contract. The four cases `TC-S4-E5019-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the four price bases, the 2 and 5 working days, the LOV values and the message texts stay reference rows of the package and of reference data, never schema defaults or enumeration members of the code.
- No personal data in a fact, an answer, an example or a fake: references, dates, codes, percentages, amounts and a rule version only; every example is synthetic.
- The case stays with rwb-case: the document declares no `recovery_case`, route-state, `assignment` or `task` property and no write of any of them (BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on ACE, and the boundary test fails a build that adds one (DP-05, BR7).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or operation as its own fails the review (DP-13, DP-14, BR9).
- No fourth operation, no event, no Schedule, no Quartz row and no auction column: the absence tests of AC8 fail a build that declares one (BR2, BR6).
- The money stays with rwb-payment: the document declares no proceeds, ledger or balance property and only the move `PROCEEDS_MATCHED` (BR11).
- The error envelope, the idempotency rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement (FSD S4 Requirements served); the legacy master and TSD S4 T8 carry no requirement ID for this key (GAP-2827; ASM-4675) | The auction element, the case-move answer with the task request and the three operations | TC-E5-019-01, TC-E5-019-02, TC-S4-E5019-CON-01 |
| R-LIT-63, R-LIT-65, R-LIT-66, R-LIT-67 | The opening, sold, stepping and exhausted steps of the LED ladder | The rule package read, the record element, the timer element and the stage answer | TC-E5-019-01, TC-E5-019-02, TC-S4-E5019-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows and the three provided operations | TC-S4-E5019-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-019, disposition Split (rework) |
| Legacy criteria | AC1 to AC3, owned word for word by `RWB-S4-E5019-APP`; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the four new contract cases |
| Feature and screens | FEAT-LIT-19, SCR-20 Enforcement workspace and SCR-19 Litigation workspace |
| Rules | R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67, named and governed in rwb-decision (GAP-2827) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the step, the evaluation of the four rules, the decision record, the action create and update, the timer and the stage answer: `RWB-S4-E5019-APP`.
- The case of record, its route state, `CaseWorkflow`, the assignment and the enforcement task row: rwb-case (P3) and its slice of this legacy key (GAP-2827; ASM-4673).
- The authoring, testing, approval and versioning of the LITIGATION package, of the four rules and of the four price bases: rwb-decision (P7) and the reference-data owner (GAP-2827; ASM-4653).
- The matching and posting of the sale proceeds under R-LIT-65, which the baseline declares only as the move `PROCEEDS_MATCHED`: `RWB-S4-E5022-APP` and rwb-payment (P8) (ASM-4678).
- The LED portal, the LIT interface, the partner portal's own contract and the ACE views: rwb-integration (P2), rwb-partner (S9) and rwb-source-data (P1) (GAP-2827; ASM-4677).
- The writ, the seizure and the obstruction (R-LIT-54, R-LIT-64) and the enforcement deferral, the bankruptcy petition and the write-off routing: the sibling stories of S4 and rwb-writeoff (S7).
- The notice, the pack, the firm instruction, the filing, the hearings and the prescription warning, and the two sibling operations of this service: the sibling stories of S4, rwb-document (P5) and rwb-comms (P6).
- The rights, roles, scope and masking data, and the composite route and screen field list of SCR-19 and SCR-20: rwb-access (P4) and `RWB-PLT-N001-CON`.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this key.
