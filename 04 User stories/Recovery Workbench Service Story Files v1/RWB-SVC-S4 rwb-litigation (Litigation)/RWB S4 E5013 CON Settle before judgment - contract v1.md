# RWB-S4-E5013-CON Settle before judgment - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-013 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the settlement-before-judgment step of rwb-litigation, split from RWB-E5-013. It fixes the two legal-action operations on `/api/recovery/litigation/v1` (DP-13), the settlement request and answer elements, the `CIVIL_CASE` action type and the `FILED` status the hold keeps, the consumed proposal of rwb-agent, the approval of rwb-decision, the booking of rwb-treatment and the case-move answer of rwb-case, the `Idempotency-Key` rule, the error envelope, the rights and the decision-record element of DP-03. The hold adds no list value and no column, and the action is never set to `WITHDRAWN` here; the four consumed rows carry no C row in the plan and no operation name in any source (GAP-2798, GAP-2799, GAP-2800; ASM-4635 to ASM-4640). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the settlement-before-judgment step of rwb-litigation — the two legal-action operations on `/api/recovery/litigation/v1`, the settlement request and answer elements, the `CIVIL_CASE` action type and the `FILED` status the hold keeps, the consumed proposal, approval, booking and case-move rows, the `Idempotency-Key` rule, the error envelope and the rights, the decision-record element, the tables and the fakes**, so that **the app story, SCR-19 and the tests of this legacy key build against one fixed, testable contract on Day 1 and a state name, a list value, an element name or an answer shape can never drift between rwb-litigation, rwb-agent, rwb-decision, rwb-treatment and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-013 crossed four boundaries at once: an officer screen with an agent proposal, a delegated-authority approval, a treatment and a case state. The target splits them: the proposal is rwb-agent's (P10), the approval and the D7.4 limit are rwb-decision's (P7), the treatment is rwb-treatment's (S2), the case of record is rwb-case's (P3), and the litigation stage, the legal action and the decision record stay with rwb-litigation (S4). Each boundary is a contract another team builds against, so each has to be fixed before the app story starts: the action type and status vocabulary, the settlement elements, the shape of the hold, the facts the four consumed rows answer and the record of the decision.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation` (context pack, service and naming rules). It records that rwb-litigation owns two tables, `legal_action` and `hearing`, five REST operations and one workflow, and no event and no job at all (context pack, ownership rows), so this baseline declares no event and no Schedule.

Two points are carried as gaps and assumptions rather than decided quietly: **the hold**, because `LOV-LEGAL-STATUS` has no held value and no source gives a hold column, so the hold is a stage state of `LitigationWorkflow` and the action keeps `FILED` (GAP-2799; ASM-4638); and **the approver**, because the approver named by the limit is a delegated-authority approver of the DoA matrix and not a Litigation role row, so the approval is consumed from rwb-decision and no right is widened here (GAP-2800; ASM-4639).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `legal_action` and `hearing` are S4's, `treatment` is S2's, `recovery_case` is P3's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's. This document never declares another service's operation as provided.
- The four consumed rows of 12.2 name four owners whose contracts are published; none of the four is in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2798; ASM-4635).
- The operation names and the element lists of the four consumed rows are Not specified in the source documents (GAP-2798; ASM-4636): the TSD S4 T5.2 names the published Java interfaces P3, P7, P4, P5 and P6 with no operation, and T-A.1 lists five S4 operations only.
- The LITIGATION package, its rule rows for R-LIT-36, R-LIT-37 and R-LIT-38 and the D7.4 limit are governed in rwb-decision (P7); this baseline names them and declares none of them (GAP-2799; ASM-4639).
- The `legal_action` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-litigation for this step: the two operations with their request and answer elements, the action type and status vocabulary, the rights and the six error responses.
2. Fix the settlement elements: the request that carries the proposal, its cost and its effect, the approver named by the limit and the offer reference, and the answer that carries the stage, the rule ID, the package version and the decided-at time.
3. Fix the hold: the stage value `LITIGATION_HELD`, the action status `FILED` it leaves unchanged, and the explicit statement that this step never writes `WITHDRAWN`.
4. Fix the four consumed rows and mark the fields the sources do not give with the placeholder.
5. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, written before the stage changes.
6. Record the closed vocabulary and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the six contract fakes.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `treatment`, `recovery_case` or `rule_row` property, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-S4-E5013-APP, SCR-19 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC6 |
| X5 | A value outside `LOV-LEGAL-TYPE` or `LOV-LEGAL-STATUS` appears, or a held value is added | The vocabulary test fails the build | None | AC1, AC7 |
| X6 | The document declares another service's operation as provided, a `treatment` row, a `recovery_case` row or a `rule_row` property | The review fails the baseline; the boundary test fails the build | None | AC7 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC2, AC4 |
| X8 | The rights of an operation are not the ones TSD S4 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-agent, rwb-decision, rwb-treatment and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the vocabulary, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S4-E5013-APP, SCR-19 and the wave 3 harness on Day 1, and the rwb-treatment and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, six fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the settlement-before-judgment step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of treatment is S2 and of recovery_case is P3
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two legal-action operations are declared with the civil-case action type and no held status value (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions with the LegalAction answer of status 201 and GET /legal-actions/{legalActionId} with the LegalAction answer of status 200, both under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then action_type is declared against LOV-LEGAL-TYPE with the values NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION and LED_AUCTION, and the action of this step is CIVIL_CASE
    Then status is declared against LOV-LEGAL-STATUS with the values OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN, and the step reads FILED and writes no status at all
    Then no held value is added to LOV-LEGAL-STATUS and no property is added to the LegalAction element for a hold, an offer or a settlement amount
    Then every other property of the element is copied from the baseline of the legal action and is not redefined here

  Scenario: AC2 The settlement request and answer elements and the hold are fixed (new, D-RCV-60)
    Given the settlement sections of the baseline
    When they are compared with the settlement step of RWB-S4-E5013-APP
    Then the request element carries the case reference, the legal action reference, the offer reference, the proposed amount, the cost and the effect of the proposal, the approver named by the limit and the rule ID with the package version in force
    Then the answer element carries the stage SETTLEMENT_OFFERED_AT_COURT, LITIGATION_HELD or IN_HEARING, the action status FILED unchanged, the treatment reference where the settlement is booked, the rule ID, the package version and the decided-at time
    Then the document states that the step never writes WITHDRAWN and that the withdrawal on a completed settlement is another story's
    Then the POST declares the Idempotency-Key header and its stored answer, and the GET declares none
    Then the field names the sources do not give are Not specified in the source documents (GAP-2799; ASM-4636) and the document marks them so

  Scenario: AC3 The four consumed rows are declared and their effects stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership rows and with the contracts of P10, P7, S2 and P3
    Then the proposal with its cost and its effect is declared as consumed from P10 rwb-agent, with the case reference, the step, the cost, the effect and the package version
    Then the approver named by the limit and the approval or rejection with its reason are declared as consumed from P7 rwb-decision, and the limit itself is named as P7's
    Then the booking of the approved settlement is declared as consumed from S2 rwb-treatment, with the case reference, the legal action reference, the approved amount and the treatment reference it answers, and the document declares no treatment plan, document or posting
    Then the case move is declared as consumed and answered with rwb-case, with the move, the rule ID, the package version and the decided-at time, and the document declares no recovery_case property
    Then the operation names of the four rows are Not specified in the source documents (GAP-2798; ASM-4635) and the rows carry the placeholder
    Then every call on the four rows is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S4 T-A.1 and T-A.2 and with TSD S4 T6.1
    Then the operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404, 409 on a closed, withdrawn or wrong-stage action, 422 with MSG-GEN-001 and 503 when a downstream does not answer, each with one envelope and one message ID per condition
    Then POST /cases/{caseId}/legal-actions declares Litigation right C and GET /legal-actions/{legalActionId} declares Litigation right R, each with the scope applied
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, RW-HEADLIT and RW-PRODHEAD and RW-LEGAL hold RA, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R
    Then no right is added for the approval, because the approver is a delegated-authority approver of the DoA matrix and not a Litigation role (GAP-2800; ASM-4639)
    Then a repeated POST with the same Idempotency-Key returns the stored answer and describes no second effect

  Scenario: AC5 The decision-record element is declared and written before the stage changes (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the local decision-record library of DP-03
    Then one decision record is declared per rule outcome with the case reference, the legal action reference, the rule ID, the package version in force, the inputs reference, the outcome and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the stage changes, and a failed write leaves the stage unchanged with MSG-P7-003
    Then the document declares no event of its own for the record and no second topic for this capability
    Then the record carries IDs, codes, dates, amounts and a rule version only

  Scenario: AC6 The six contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-agent proposal fake answers the step with its cost and its effect for case "RC-2026-000713" and an answer beyond 2 s
    Then the rwb-decision approval fake answers the approver at D7.4, an approval inside the limit, a committee approval above it and a rejection with a reason
    Then the rwb-treatment booking fake answers the treatment booked for case "RC-2026-000713" with its treatment reference, and a booking refused
    Then the rwb-case fake answers the case states IN_HEARING and SETTLEMENT_OFFERED_AT_COURT and the moves SETTLEMENT_OFFERED_AT_COURT, LITIGATION_HELD and IN_HEARING, with one move refused
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the ownership boundary are fixed and nothing else is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as owned are legal_action and the library objects decision_record and idempotency_key, and treatment, recovery_case, rule_row, decision_log_entry, document and hearing are named as other owners' or another story's and are consumed only through their contracts
    Then the document declares no event published, no event consumed and no Schedule for this step, and the absence test fails a build that adds one
    Then the document declares no read of a v_ace_* view and no grant on rwb_treatment, rwb_case or rwb_decision, and the boundary test fails a build that adds one
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5013-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The settlement step, the stage states `IN_HEARING`, `SETTLEMENT_OFFERED_AT_COURT` and `LITIGATION_HELD`, and the legal action are rwb-litigation's; the contract declares their vocabulary and their shapes on `legal_action` only | FSD S4 A2.13; TSD S4 T4; Ownership Map (legal_action and hearing owner S4) |
| BR2 | The decision record is declared as an element written before the stage changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-013 AC1 and AC4 |
| BR3 | The treatment stays with rwb-treatment: the contract declares the booking as consumed, declares no `treatment` property and describes no plan, document or posting | Ownership Map (treatment owner S2); TSD S4 T5.2; GAP-2798 |
| BR4 | The case move is answered and not written: the contract declares the answer that carries the move and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); GAP-2798 |
| BR5 | The hold adds no list value and no column: `LOV-LEGAL-STATUS` is published unchanged, the action keeps `FILED` and the step never writes `WITHDRAWN` | TSD S4 T3.2; R-LIT-37 and R-LIT-39; GAP-2799 |
| BR6 | The approver and the limit are rwb-decision's: the contract declares the approval as consumed and widens no Litigation right for it | GAP-2800; ASM-4639; context pack slide 3 notes (DoA Matrix v2) |
| BR7 | The proposal is the agent's: the contract declares it as consumed and fixes no cost, no effect and no model call of its own | FSD S4 A2.13.3.1 (R-LIT-36); GAP-2798 |
| BR8 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | TSD S4 T-A.2 |
| BR9 | The vocabulary is closed: `LOV-LEGAL-TYPE`, `LOV-LEGAL-STATUS`, `LOV-HEARING` and `LOV-HEARING-OUTCOME` are published as enumerated values and no state name or list value is a constant of the code | TSD S4 T3.2; BR-S4-013 (FSD S4 A2.13.3.1) |
| BR10 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, list values and a rule version only | Template and Rules v1 §R7.2 (s17) |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version; the document lists only operations owned by rwb-litigation | Architecture v5 notes; Ownership Map; DP-11 |

### 9. State transitions

The lifecycle of this document, not of a legal action:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the settlement elements, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-19, the wave 3 harness and the rwb-agent, rwb-decision, rwb-treatment and rwb-case owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC7 fails: a `treatment` or `recovery_case` property, a held list value, a second topic or a Schedule | In review |

The stage machine of `LitigationWorkflow` that the document describes is the app story's: `IN_HEARING` → `SETTLEMENT_OFFERED_AT_COURT` under R-LIT-36, → `LITIGATION_HELD` under R-LIT-37 or back to `IN_HEARING` under R-LIT-38, and this baseline fixes the vocabulary and the shapes and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, SCR-19, the wave 3 harness and the owners of rwb-agent, rwb-decision, rwb-treatment, rwb-case, rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-litigation login (DP-02)" and is not part of this baseline. No approver of the DoA matrix is a party to this document: the approval arrives as a consumed answer (BR6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| LegalAction element | The columns of DF-LEG-001 to DF-LEG-014: `id`, `case_id`, `law_firm_id`, `action_type`, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status` and `status` |
| Settlement request | The case reference, the legal action reference, the offer reference, the proposed amount, the cost and the effect of the proposal, the approver named by the limit and the rule ID with the package version: the field names Not specified in the source documents (GAP-2799; ASM-4636) |
| Hold | The stage value `LITIGATION_HELD` and the unchanged action status `FILED`; no column, no list value and no property is added (GAP-2799; ASM-4638) |
| Treatment | DF-TRT-001 to DF-TRT-014 of `treatment` in `rwb_treatment`, read only through the S2 booking answer and never written, copied or joined here |
| Case | DF-CAS-001 to DF-CAS-023 of `recovery_case` in `rwb_case`, answered by P3 with the move and never written here |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the stage changes (DP-03) |
| Rules | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, consumed through the package in force; R-LIT-36 to R-LIT-38 and the D7.4 limit are governed there (GAP-2799) |
| Not written here | `hearing` (S4, the sibling stories'), `document` (P5), `decision_log_entry` and `rule_row` (P7) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC1 and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required; the answer is stored |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its court facts and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The two operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S4 T-A.1; the paths are those of the target base and not the monolith form. API-S4-004 `PATCH /legal-actions/{legalActionId}` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` belong to the sibling stories that record the filing, the judgment, the enforcement step and the hearing, and API-S4-001 `POST /notices/{noticeId}/approve` belongs to the notice story; none of the three is declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The proposal operation of P10 (operation name Not specified in the source documents (GAP-2798; ASM-4636)) | `/api/recovery/agent/v1` | P10 rwb-agent | The step proposed with its cost and its effect for a case before judgment; read, never computed here; faked |
| The approval operation of P7 (operation name Not specified in the source documents (GAP-2798; ASM-4636)) | `/api/recovery/decision/v1` | P7 rwb-decision | The approver the DoA matrix names at D7.4 and the approval or the rejection with its reason; the limit and the approver are P7's; faked |
| The booking operation of S2 (operation name Not specified in the source documents (GAP-2798; ASM-4636)) | `/api/recovery/treatment/v1` | S2 rwb-treatment | The booking of the treatment for the approved settlement and the treatment reference it answers; the row, the plan and the posting are S2's; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2798; ASM-4635)) | rwb-case (P3) | P3 rwb-case | The move `SETTLEMENT_OFFERED_AT_COURT`, `LITIGATION_HELD` or `IN_HEARING` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2798 with ASM-4635 and ASM-4636. The base of each consumed row is the owner's and is named here only to show that it is not this service's.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service list no event at all (context pack, ownership rows). DP-09 is not in the pattern set of this key: this baseline declares no event, adds no outbox row and widens no topic, and the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service. A settlement booked by S2 is S2's event on S2's topic.

#### 12.4 Events consumed

None. The ownership rows list no consumed event either, so the proposal arrives as a signal of `LitigationWorkflow` and the three answers arrive on their owners' contracts of 12.2 (GAP-2799; ASM-4637). This baseline declares no consumer group, no subscription and no inbox of its own, and the absence test of AC7 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the settlement step; its signals, its 3 and 2 working-day timers and its outcome for the parent are declared, not built |
| `routeSettlementOffer` | Activity, the routing step | `rwb-litigation` | The case, the legal action and the proposal in; the rule ID with its package version, the approver and the case move out |
| `applySettlementHold` | Activity, the booking and hold step | `rwb-litigation` | The approval answer in; the treatment reference, the hold, the decision record and the case move out |

No model call and no treatment activity exist in this service: the proposal is P10's answer and the treatment is S2's row. The activity names are target design choices and the trigger of the step is read as a proposal signal, because the legacy story says the user acts on the screen while R-LIT-36 names the customer or the firm as the source (GAP-2799; ASM-4637). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the proposal signal and the approval answer; the 3 and 2 working-day task timers of R-LIT-36 and R-LIT-37 are durable timers of the workflow. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and the ownership rows of this service list no job.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The filed civil-case action, its court facts and its status; read by the two operations and **not written** on the settlement path (BR5) |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated POST and the answer it holds |

`treatment` (S2), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5) and `hearing` (S4, the sibling stories') are not owned by this baseline; it names them only as answers or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-agent proposal fake | The step with its cost and its effect for case `RC-2026-000713`; an answer beyond 2 s | AC3, AC6 |
| rwb-decision approval fake | The approver at `D7.4`; an approval inside the limit, a committee approval above it and a rejection with a reason | AC3, AC6 |
| rwb-treatment booking fake | The treatment booked for case `RC-2026-000713` with its treatment reference; a booking refused | AC3, AC6 |
| rwb-case case-move fake | The case states `IN_HEARING` and `SETTLEMENT_OFFERED_AT_COURT`; the moves `SETTLEMENT_OFFERED_AT_COURT`, `LITIGATION_HELD` and `IN_HEARING` accepted, and one refused | AC2, AC3, AC6 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-36, R-LIT-37 and R-LIT-38, and one approval answer | AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names and the element lists of the four consumed rows are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2798, GAP-2799; ASM-4635, ASM-4636).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The create and read of the legal action on `/api/recovery/litigation/v1`; the proposal, the approval, the booking and the case-move answer; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `LitigationWorkflow`, `routeSettlementOffer` and `applySettlementHold` on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no legal action, no case, no treatment and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment that declares no event, nine contract tables and six fakes.

**Deliverables.** The additive document `openapi/rwb-litigation-v1.yaml` for this step, the settlement request and answer elements, the vocabulary of `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` as published enumerations with no held value, the contract README rows for the four consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-13 moves the base and nothing else. DP-03 is declared as the element and the transaction rule, not as a build. DP-19 is behind SCR-19, whose screen model is the edge contract's. DP-09 and DP-20 are not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4 and why the agent proposal is a consumed row rather than a baseline of this service.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None; this baseline builds against their fakes until those platform contract stories publish. The four consumed rows are C dependencies in fact and not in the metadata row (GAP-2798; ASM-4635).

**Build steps**

1. Write the two operations and validate the additive rule of AC1 in the pipeline.
2. Write the settlement request and answer elements of AC2 with the placeholder on the fields the sources do not give, and the statement that no held value and no column is added.
3. Record the four consumed rows of AC3 with their owner, their budget and their placeholders.
4. Record the error envelope, the rights and the `Idempotency-Key` rule of AC4, including the absence of a right for the approval.
5. Record the decision-record element of AC5 and validate it against the library schema.
6. Publish the six fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the six fakes answer every consumed path and the drift test is green, and the app story, SCR-19 and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription story of this service, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the stage changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The FSD validation rules VR-S4-013-1 and VR-S4-013-2 name the pack and the prescription messages and belong to the pack and prescription stories of this service.

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its pack, instructed, filed, hearing and judgment states through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the legal action and the stage outcome, rwb-case for the case and its route state, rwb-treatment for the treatment and rwb-decision for the approval; this baseline fixes the rwb-litigation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The states this step adds — offered at court, held, rejected, not recorded, refused — read the messages of section 14 on the same route. The legacy screen table also names SCR-18 Notice approval, whose states generated, approved, sent, delivered and unserved carry no settlement state; it is carried read-only as the notice context and fixes nothing here (GAP-2800; ASM-4640).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-013-01 | AC1, AC2 | Contract | Case `RC-2026-000713` and action `LA-2026-000713`; the contract half answers the two operations, the `CIVIL_CASE` action type, the `FILED` status and the settlement elements |
| TC-E5-013-02 | AC2, AC3 | Contract | The approver at `D7.4` and the proposal of the agent; the contract half answers the request and answer elements and the agent and approval consumed rows |
| TC-E5-013-03 | AC2, AC3 | Contract | An approved settlement inside the limit and a treatment booked by S2; the contract half answers the booking row, the hold and the case move to `LITIGATION_HELD` |
| TC-E5-013-04 | AC4, AC5 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element of AC5 |
| TC-E5-013-05 | AC4, AC7 | Contract | A role without the Litigation right and a malformed request; the contract half answers the 403 with MSG-P4-002, the 400 of the envelope and the absence of a right for the approval |
| TC-E5-013-06 | AC5, AC6 | Contract | A forced decision-record failure and a drifted fake; the contract half answers the stopped chain and fails the build on the drift |
| TC-S4-E5013-CON-01 | AC1, AC2 | Contract | The document validates; the two operations, the base, the six action types, the six status values, the settlement elements and the unchanged `FILED` status are present, and no held value or hold property is added |
| TC-S4-E5013-CON-02 | AC2, AC4 | Contract | The settlement request and answer elements validate; the `Idempotency-Key` rule and the seven error responses with one message ID per condition |
| TC-S4-E5013-CON-03 | AC3 | Contract | The four consumed rows validate with their owner, their placeholder fields and one hop with a 2 s budget |
| TC-S4-E5013-CON-04 | AC5, AC6, AC7 | Contract | The record element validates against the library schema; the six fakes match the document and a drifted fake fails the build; the absence test for a `treatment` or `recovery_case` property, a held list value, a second topic and a Schedule |

The six legacy cases are the legacy cases of RWB-E5-013 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5013-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S4-E5013-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the D7.4 limit, the 3 and 2 working-day timers, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, list values and a rule version only; every example is synthetic.
- The treatment stays with rwb-treatment and the case with rwb-case: the document declares no `treatment` property, no `recovery_case` property, no plan and no case row write (BR3, BR4).
- The hold adds nothing to the vocabulary: `LOV-LEGAL-STATUS` is published unchanged, no held value is invented, and the step never writes `WITHDRAWN` (BR5).
- The approver is not a Litigation right: the approval is consumed from rwb-decision and no right is added to the capability area for it (BR6).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on `rwb_treatment`, `rwb_case` or `rwb_decision`, and the boundary test fails a build that adds one.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence test of AC7 fails a build that declares an event, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-006 | Settlement before judgment, an appeal and fee payment each need approval inside the delegation; the contract fixes the settlement elements, the approval consumed row and the hold on which the rule is evaluated (FSD S4 Requirements served); the legacy story master carries no requirement id | The two operations, the settlement elements, the approval and booking consumed rows and the hold | TC-E5-013-01, TC-E5-013-02, TC-S4-E5013-CON-01, TC-S4-E5013-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S4-E5013-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-013, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S4-E5013-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S4-E5013-CON-01 to -04 |
| Feature and screens | FEAT-LIT-13, SCR-19 Litigation workspace and SCR-18 Notice approval (read-only context) |
| Rules | R-LIT-36, R-LIT-37 and R-LIT-38, named from the Business Rules and Routing Logic v4 and governed in rwb-decision (GAP-2799) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two operations, the evaluation of R-LIT-36, R-LIT-37 and R-LIT-38, the decision record, the hold and the case-move answer: RWB-S4-E5013-APP.
- The proposal with its cost and its effect and the model that produces it: rwb-agent (P10), whose contract this baseline declares as consumed and faked (GAP-2798).
- The DoA matrix, the D7.4 limit, the approver and the approval: rwb-decision (P7), whose contract this baseline declares as consumed and faked (GAP-2800; ASM-4639).
- The booking of the treatment, its plan, its documents, its posting and its completion: rwb-treatment (S2), `RWB-S4-E5013-APP`'s consumed contract. **The treatment is booked by rwb-treatment, and no part of this baseline books it** (GAP-2798; ASM-4635).
- The case of record, its route state and the parent `CaseWorkflow`: rwb-case (P3), whose case-move answer this baseline declares as consumed and faked.
- The creation of the legal action and its pack, the filing, the hearing calendar and the judgment: the sibling stories of this service.
- The authoring, testing, approval and versioning of the LITIGATION package and of the rule rows of R-LIT-36, R-LIT-37 and R-LIT-38, and the D7.4 limit: rwb-decision (P7) (GAP-2799; ASM-4639).
- The ACE account and batch facts and the interaction ledger: rwb-source-data (P1); this feature needs none of them.
- The documents of the settled file, their custody and their retention: rwb-document (P5).
- The gateway-bff composite route and the screen field list of SCR-19 and SCR-18: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
