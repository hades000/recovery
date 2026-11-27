# RWB-S4-E5015-CON Pay court fees and legal expenses - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5015-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5015-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | Contract stories of P5 (document hub: pack and missing document), P8 (court fee and legal expense, payment and posting row) and P10 (model gateway: next litigation step); story keys Not specified in the source documents (GAP-1737) |
| Contract version | 1 (major version 1, path `/api/recovery/litigation/v1`) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Feature trace | FEAT-LIT-15 Pay court fees and legal expenses; rules R-LIT-30 and R-LIT-41 to R-LIT-43; module measure Not specified in the source documents (GAP-2810); no requirement ID (GAP-2810) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the court-fee and legal-expense step of rwb-litigation, split from RWB-E5-015. It fixes the two operations of this key on `/api/recovery/litigation/v1` (DP-13), the fee-relevant properties of `legal_action` and the closed vocabularies, the consumed payment and posting row of rwb-payment with the money kept there (GAP-2806; ASM-4646), the consumed fee schedule of rwb-case (GAP-2807; ASM-4647), the consumed approval child workflow of rwb-decision and the D7.4 limit with the rule rows (GAP-2809; ASM-4649), the decision-record element of DP-03 and the fakes. The filing rule of legacy AC2 is declared as another story's behaviour and only asserted (GAP-2808; ASM-4648). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5015-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 13 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the court-fee and legal-expense step of rwb-litigation — the two operations of this key on `/api/recovery/litigation/v1`, the fee-relevant properties of `legal_action` and the closed vocabularies, the consumed payment and posting row of rwb-payment, the consumed fee schedule of rwb-case, the consumed approval child workflow and rule rows of rwb-decision with the D7.4 limit of rwb-access, the decision-record element, the tables and the fakes**, so that **the app story, the two screens and the tests of this legacy key build against one fixed, testable contract on Day 1, and a fee, a schedule version, a limit, an approval state or an answer shape can never drift between rwb-litigation, rwb-payment, rwb-decision, rwb-case and rwb-access without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-015 crossed four boundaries at once: an officer screen, a fee schedule, an approval inside a delegated limit, and a payment posted against the case through ALS core and GL (FSD S4 A2.15.2). The target splits them: the money is paid and posted by rwb-payment (P8), the schedule is reference data of rwb-case (P3), the approval is the child workflow of rwb-decision (P7) named in TSD S4 T5.2.2, the delegation limit is rwb-access's (P4), and the spend decision stays with rwb-litigation (S4). Each boundary is a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation` (context pack service row). It records that rwb-litigation holds no `v_ace_*` grant and no grant on `rwb_payment`, so DP-05 is declared as a prohibition and the payment is consumed on the owner's contract only.

Four points are carried as gaps rather than decided quietly. No column of `legal_action` or `hearing` carries a fee or a posting, so the step has no resource of its own and its durable effect is the decision record and the stage answer (GAP-2806; ASM-4646). The schedule the fee is checked against has no field list and no owner row (GAP-2807; ASM-4647). The D7.4 limit has no value in any source read and the approval carries no dependency row (GAP-2809; ASM-4649). Legacy AC2 carries R-LIT-30, whose effects are built by two other stories of this service, so the criterion is asserted here and not declared as this step's behaviour (GAP-2808; ASM-4648).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (TSD S4 T-A.2); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `legal_action` and `hearing` are S4's, `recovery_case` is P3's, `rule_row` and `decision_log_entry` are P7's, `document` is P5's, `proceeds` and the payment rows are P8's. This document never declares another service's operation as provided.
- The LITIGATION rule package with R-LIT-30 and R-LIT-41 to R-LIT-43 and the approval child workflow are governed in rwb-decision (P7); this baseline names them and declares none of them (GAP-2809; ASM-4649).
- The fee schedule, its versions and the fee types are reference data of rwb-case; their operation name and field list are `Not specified in the source documents (GAP-2807; ASM-4647)`.
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- `RWB-S4-E5015-APP` is published in draft, so the baseline has one consumer from the first day.

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-litigation for this step: the two operations with their request and answer elements, the fee-relevant properties, the rights and the error responses.
2. Fix the vocabulary of the status, of the fee types and of the approval states, and the rule that no value is a constant of the code.
3. Fix the consumed payment and posting row of rwb-payment with the placeholder on the operation name and on the field list, and state that the money stays there.
4. Fix the consumed fee-schedule row of rwb-case and the consumed approval and rule-package rows of rwb-decision, and the consumed authorise and limit row of rwb-access.
5. Fix the approval states and the D7.4 test as contract elements, and name the P7 child workflow as consumed.
6. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, written before the spend moves.
7. Record the `Idempotency-Key` rule, the error envelope and the rights of the two operations.
8. Publish the contract tables of section 12 and the six contract fakes.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a payment or case write, and the drift between a fake and the document.
10. Tag the baseline and hand it to `RWB-S4-E5015-APP`, the two screens and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or response body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has an operation name or a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-LEGAL-STATUS` or the approval states appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a payment row or a `recovery_case` property | The review fails the baseline; the boundary test fails the build | None | AC6 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC5 |
| X8 | The rights of an operation are not the ones TSD S4 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-payment, rwb-decision, rwb-case and rwb-access only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the vocabulary, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks `RWB-S4-E5015-APP`, the two screens and the wave 3 harness on Day 1, and the rwb-payment and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment that declares no event, nine contract tables, six fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the court-fee and legal-expense step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of recovery_case is P3, of rule_row and decision_log_entry is P7 and of the payment rows is P8
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two operations of this key are declared on the per-service base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions with the LegalActionRequest in and the LegalAction answer of status 201, and GET /legal-actions/{legalActionId} with the LegalAction answer of status 200, all under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then POST /cases/{caseId}/legal-actions declares Litigation right C, GET /legal-actions/{legalActionId} declares Litigation right R, and each applies the caller's scope
    Then POST declares the Idempotency-Key header and its stored answer, and GET declares none
    Then POST /notices/{noticeId}/approve, PATCH /legal-actions/{legalActionId} and POST /legal-actions/{legalActionId}/hearings are named as the notice, filing and hearing stories' operations and are not declared by this baseline
    Then the document declares no operation for a fee, a spend or a payment of this service, because the sources give the fee no column and no resource (GAP-2806; ASM-4646)

  Scenario: AC2 The fee-relevant properties and the closed vocabularies are fixed and no fee property is added (new, D-RCV-60)
    Given the data section of the baseline
    When it is compared with TSD S4 T3.1 and T3.2 and with the legacy data table of RWB-E5-015
    Then the LegalAction element carries the columns DF-LEG-001 to DF-LEG-014 with claim_amount as the amount in dispute, and no fee, spend, posting, ledger or balance property is added to it or to the Hearing element
    Then status is declared against LOV-LEGAL-STATUS with the values OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN, and action_type against LOV-LEGAL-TYPE with its six values, both as published enumerations
    Then the approval states PENDING, APPROVED and REJECTED are declared as a closed list of the answer and are not added to legal_action
    Then black_case_no and filed_date are declared as the AC2 post-condition the filing story writes, and this baseline writes neither
    Then the fee type, the court level and the schedule version are declared as values of the consumed schedule read and never as columns of rwb_litigation (GAP-2807; ASM-4647)

  Scenario: AC3 The consumed payment and posting row is declared and the money stays with rwb-payment (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the P8 module and with the systems R-LIT-42 names
    Then the pay-and-post of the approved legal spend is declared as consumed from P8 rwb-payment, with the case reference, the legal action reference, the fee reference, the amount, the value date, the approval reference and the payment reference of the answer
    Then its operation name and its field list are Not specified in the source documents (GAP-2806; ASM-4646) and the row carries the placeholder
    Then the document declares no posting property, no ledger entry, no balance and no payment row of rwb-litigation, and describes the ALS core and GL posting of R-LIT-42 as P8's
    Then every call on the row is one hop with a 2 s budget, a breaker and no retry of its own except a GET (DP-11, ADR-020)

  Scenario: AC4 The approval route and the rule rows are declared as consumed (new, D-RCV-60)
    Given the approval section of the baseline
    When it is compared with TSD S4 T5.2.2 and with the Business Rules and Routing Logic v4
    Then the approval is declared as the Temporal child workflow of P7 rwb-decision on queue rwb-decision, and no approval workflow, approval table or approval state machine is declared here
    Then the D7.4 limit and the approver's delegation limit are declared as consumed on the authorise contract of rwb-access, and no limit value is fixed in the document
    Then the LITIGATION rule package at its version in force with R-LIT-41, R-LIT-42 and R-LIT-43 is declared as consumed from rwb-decision, with R-LIT-30 named as the filing story's rule and asserted only
    Then the approval answer element carries the state PENDING, APPROVED or REJECTED, the approver, the limit test, the rule ID, the package version and the decided-at time
    Then every one of the three rows is a C dependency in fact that the metadata row does not carry, and the absence is recorded (GAP-2809; ASM-4649)

  Scenario: AC5 The decision-record element, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the decision and error sections of the baseline
    When they are compared with DP-03, TSD S4 T-A.1 and T6.1
    Then one decision record is declared per spend outcome with the case reference, the legal action reference, the fee reference, the amount, the schedule version, the limit test, the rule ID, the package version in force and the decided-at time
    Then the record is written through the local library on rwb.decision-record.v1 before the spend is approved, rejected or paid, and a failed write leaves the spend unchanged with MSG-P7-003
    Then the operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404, 409 on a closed or withdrawn action or a fee already paid, 422 with MSG-GEN-001 and 503 when a downstream does not answer, each with one envelope and one message ID per condition
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, RW-LEGAL and RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM holds RU and SY-DATALOAD holds U, and no other role of TSD S4 T6.1 gains a right this step does not need
    Then the record carries identifiers, amounts, dates, codes and a rule version only, and no personal data

  Scenario: AC6 The six contract fakes answer the document, the naming baseline holds and no forbidden element is declared (new, D-RCV-60)
    Given the fakes, naming and boundary sections of the baseline
    When each fake is compared with the operation or the element it serves and the nine sub-tables are reviewed
    Then the rwb-payment fake answers the payment reference of 2026-11-30 for case "RC-2026-001215", a refused payment and an answer beyond 2 s
    Then the rwb-case fake answers the fee schedule in force with its version, a second version, and the case state FIRM_INSTRUCTED
    Then the rwb-decision fakes answer the LITIGATION package with R-LIT-30 and R-LIT-41 to R-LIT-43, an APPROVED answer with its approver and a REJECTED answer with a reason
    Then the rwb-access fake answers the authorise answer and the D7.4 delegation limit, and the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as owned are legal_action, decision_record and idempotency_key, and hearing, recovery_case, rule_row, decision_log_entry, document, the partner claim, the fee schedule and the payment rows are named as another owner's or another story's and are consumed only through their contracts
    Then the document declares no read of a v_ace_* view, no grant on rwb_payment or any other rwb_* schema, no event published, no event consumed and no Schedule, and the absence test fails a build that adds one
```

These six criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by `RWB-S4-E5015-APP` and they copy no criterion of the legacy story, whose three criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The spend decision of a legal action is rwb-litigation's, and the contract declares no fee resource, fee column or posting; the payment is declared as consumed | Context pack ownership rows; TSD S4 T3.1 and T-A.1; GAP-2806 | AC1, AC3; TC-E5-015-01, TC-S4-E5015-CON-02 |
| BR2 | The fee schedule, its versions and the fee types are reference data of rwb-case and are declared as consumed, never as an enumeration of the code | FSD S4 A2.15.1; GAP-2807 | AC3; TC-S4-E5015-CON-02 |
| BR3 | The approval is the P7 child workflow of TSD S4 T5.2.2; the D7.4 limit is the delegation limit of rwb-access; neither is rebuilt or valued here | TSD S4 T5.2.2; GAP-2809 | AC4; TC-E5-015-02, TC-S4-E5015-CON-02 |
| BR4 | R-LIT-41, R-LIT-42 and R-LIT-43 are named from the routing workbook and governed in rwb-decision; R-LIT-30 is named as the filing story's and asserted only; the spend states LEGAL_SPEND_APPROVAL and IN_HEARING are case route states read from the rwb-case answer, and no LOV value is invented for them | Business Rules and Routing Logic v4; GAP-2808 | AC2; TC-E5-015-02 |
| BR5 | The decision record is declared as an element written before the spend moves, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy AC1 and AC3 | AC4, AC5; TC-E5-015-03, TC-S4-E5015-CON-03 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | TSD S4 T-A.2; BR8 of the app story | AC6; TC-E5-015-04 |
| BR7 | The vocabulary is closed: LOV-LEGAL-STATUS, LOV-LEGAL-TYPE and the approval states are published as enumerated values and no state name is a constant of the code | TSD S4 T3.2; BR-S4-015 | AC2; TC-S4-E5015-CON-01 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, list values and a rule version only | Template and Rules §R7.2 (s17) | AC6; TC-S4-E5015-CON-04 |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 | AC1; TC-S4-E5015-CON-01, TC-S4-E5015-CON-04 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | ADR-020 | AC1; TC-S4-E5015-CON-01 |
| BR11 | The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 | AC1; TC-S4-E5015-CON-04 |
| BR12 | The stale marker of VR-S4-015-1 is carried as a message of the surface, and the batch-status check stays with rwb-source-data | FSD S4 A2.15.3.1; GAP-2807 | Not covered; a new AC in section 7 is needed (DOR-RWB-S4-E5015-CON-4) |

### 9. State transitions

The lifecycle of this document, not of a legal action:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the vocabulary, the four consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-payment, rwb-decision, rwb-case and rwb-access owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code or an approval state already listed | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a status value or an approval state changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC6 fails: a `v_ace_*` read, a payment or `recovery_case` property, a second topic or a Schedule | In review |

The spend machine the document describes is the app story's: `IN_HEARING` on `FEE_DUE` to `LEGAL_SPEND_APPROVAL` (R-LIT-41), back to `IN_HEARING` on `FEE_APPROVED` (R-LIT-42) or on `FEE_REJECTED` (R-LIT-43). Those are case route states of rwb-case, not values of LOV-LEGAL-STATUS, and this baseline fixes only the vocabulary, the approval states and the shapes. This story adds no value to the closed list LOV-LEGAL-STATUS: IN_HEARING and LEGAL_SPEND_APPROVAL are rwb-case route states, and FEE_DUE, FEE_APPROVED and FEE_REJECTED are the events that drive them; none is a list member.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, the two screens, the wave 3 harness and the owners of rwb-payment, rwb-decision, rwb-case, rwb-access, rwb-document and rwb-partner) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| LegalAction element | The columns of DF-LEG-001 to DF-LEG-014: `id`, `case_id`, `law_firm_id`, `action_type`, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status` and `status` | Not specified in the source documents (DOR-RWB-S4-E5015-CON-7) |
| Hearing element | DF-LEG-024 to DF-LEG-029, declared by the hearing story and not redefined here | Not specified in the source documents (DOR-RWB-S4-E5015-CON-7) |
| Fee facts | Carried as consumed answers: the fee type, the court level, the amount, the value date, the schedule version, the limit test and the payment reference; no property is added to `legal_action` (GAP-2806, GAP-2807) | Not specified in the source documents (DOR-RWB-S4-E5015-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the spend moves (DP-03) | Not specified in the source documents (DOR-RWB-S4-E5015-CON-7) |
| Payment and posting rows | No field list in any source for this key; read and requested through P8 and never written, copied or joined here (GAP-2806) | Not specified in the source documents (DOR-RWB-S4-E5015-CON-7) |
| ACE account and payment facts | DF-ACE-001 to DF-ACE-054, not read: this service holds no `v_ace_*` grant (DP-05) | Not specified in the source documents (DOR-RWB-S4-E5015-CON-7) |
| Not written here | `recovery_case` (P3), `document` (P5), `rule_row` and `decision_log_entry` (P7), the partner claim (S9); the notes of each are answers or rule versions of their owners | Not specified in the source documents (DOR-RWB-S4-E5015-CON-7) |
| Schedule and limit values | The fee schedule values, the fee types, the court levels and the D7.4 limit: Not specified in the source documents (GAP-2807, GAP-2809; ASM-4647, ASM-4649) | Not specified in the source documents (DOR-RWB-S4-E5015-CON-7) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required; the answer is stored |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its pack, instruction, hearings, judgment and spend panel (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The two operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S4 T-A.1; the paths are those of the target base and not the monolith form. API-S4-001, API-S4-004 and API-S4-005 belong to the notice, filing and hearing stories of this service and are not declared by this baseline. No operation of this baseline carries an amount to pay: the sources give the fee no column and no resource (GAP-2806; ASM-4646).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The pay-and-post operation of the approved legal spend (operation name Not specified in the source documents (GAP-2806; ASM-4646)) | `/api/recovery/payment/v1` | P8 rwb-payment | The case reference, the legal action reference, the fee reference, the amount, the value date and the approval reference in; the payment reference, its state and its value date out; faked |
| The fee-schedule read (operation name Not specified in the source documents (GAP-2807; ASM-4647)) | `/api/recovery/case/v1` | P3 rwb-case | The fee schedule in force for a fee type and court level with its version, the fee types, and the case state and product group; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-2809; ASM-4649)) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-30 and R-LIT-41 to R-LIT-43; faked |
| The authorise and delegation-limit read (operation name Not specified in the source documents (GAP-2809; ASM-4649)) | `/api/recovery/access/v1` | P4 rwb-access | The authorise answer for the object and the D7.4 delegation limit of the approver; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the metadata row does not carry, and the absence is recorded as GAP-2806, GAP-2807 and GAP-2809.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its two catalogue events `JudgmentRecorded` and `AuctionResult` belong to the stories that own the judgment and the auction result (TSD S4 T5.2.1). This baseline declares none of them, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. `FEE_DUE`, `FEE_APPROVED` and `FEE_REJECTED` are the event names of the state machine in the Business Rules and Routing Logic v4, not Kafka subscriptions, and the two events this service does consume — `NoticeDelivered` (EV-15) and `PartnerResultSubmitted` (EV-21) — belong to the notice and partner stories (TSD S4 T5.2.2). The fee claim, the schedule, the rule rows, the approval and the payment answer therefore arrive on the contracts of 12.2 and 12.5; this baseline declares no consumer group, no subscription and no inbox of its own (GAP-2806; ASM-4646).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` | The stage that hosts the spend step; its signals and its outcome for the parent are declared, not built; workflow ID form: Not specified in the source documents (CG-ALL-9382); start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-9382) |
| `recordSpendDecision` | Activity | `rwb-litigation` | The fee and the schedule row in; the decision record, the rule ID with its package version and the limit test out |
| `requestSpendApproval` | Activity | `rwb-litigation` | The spend in; the approval answer, the approver and the reason out |
| `payLegalSpend` | Activity | `rwb-litigation` | The approved spend in; the payment reference and its state out |
| Approval (P7 rwb-decision) | Temporal child workflow, **consumed** | `rwb-decision` | The approval of TSD S4 T5.2.2, declared as another owner's and never registered here |

The three activity names are target design choices. `postProceeds` and the ledger entry are rwb-payment's activities on queue `rwb-payment` and are declared here as another owner's, never as this service's. No activity is registered by this story, and no Schedule is declared (12.6).

#### 12.6 Schedules

None. The step runs from the arrival of a fee claim and from the time the approval waits; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of this service is owned or moved here (context pack ownership rows: Jobs 0).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The action, its amount, its court fields and its status; the table the two operations read and the filing story writes |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the spend outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated POST and the answer it holds |

`hearing` (S4, the hearing story's), `recovery_case` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), the partner claim (S9), the fee schedule (P3 reference data) and the payment and posting rows (P8) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment pay-and-post fake | The payment reference of the approved fee of case `RC-2026-001215` with its value date and state; a refused payment; an answer beyond 2 s | AC1, AC3, AC6 |
| rwb-case schedule and case fake | The fee schedule in force with its version and the fee types, a second version, and the case state `FIRM_INSTRUCTED` with the product group | AC2, AC4, AC6 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-30 and R-LIT-41 to R-LIT-43, and a second version | AC4, AC6 |
| rwb-decision approval fake | An `APPROVED` answer with its approver, an approval above the limit refused for the committee, and a `REJECTED` answer with a reason | AC4, AC6 |
| rwb-access authorise and limit fake | The authorise answer for the roles of AC5, and the D7.4 delegation limit of the approver | AC4, AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows, the schedule values and the limit are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2806, GAP-2807, GAP-2809).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The create and read of the legal action on `/api/recovery/litigation/v1`; the pay-and-post, the fee-schedule read, the rule-package read and the authorise and limit read; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 3 activities declared, 1 consumed child workflow, 0 registered | `LitigationWorkflow`, `recordSpendDecision`, `requestSpendApproval`, `payLegalSpend` on `rwb-litigation`, and the P7 Approval child workflow; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no legal action, no case, no payment and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment that declares no event, nine contract tables and six fakes.

**Deliverables.** The additive document `openapi/rwb-litigation-v1.yaml` for this step, the `LegalActionRequest` and `LegalAction` elements with the fee-relevant properties, the vocabulary of `LOV-LEGAL-STATUS`, `LOV-LEGAL-TYPE` and the approval states as published enumerations, the contract README rows for the four consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-13 moves the base and nothing else. DP-19 is behind SCR-20 and SCR-18, whose screen model is the edge contract's. The empty, loading, error and no access states of SCR-20 and SCR-18 are Not specified in the source documents (DOR-RWB-S4-E5015-CON-10). DP-05 is declared as a prohibition: the document declares no `v_ace_*` read and no grant on `rwb_payment`, the schema owned by rwb-payment (P8), because rwb-litigation holds neither. DP-04, DP-06, DP-07 and DP-08 are outside the pattern set of this key although the step evaluates rules and reads a schedule, a vocabulary and a delegation limit; each read is declared as consumed and the absence of its dependency row is recorded (GAP-2807, GAP-2809). The reference-data contract of the schedule, the vocabulary and the limit is the consumed row of 12.2 (DP-06, DP-07); the parameters they read are Not specified in the source documents (DOR-RWB-S4-E5015-CON-20).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None; this baseline builds against their fakes until those platform contract stories publish. The four consumed rows of 12.2 are C dependencies in fact and not in the metadata row (GAP-2806, GAP-2807, GAP-2809).

**Build steps**

1. Write the two operations of AC1 and validate the additive rule and the base in the pipeline.
2. Write the vocabulary and the element properties of AC2, with the approval states as a closed list of the answer and no fee property on `legal_action`.
3. Record the pay-and-post row of AC3 with its owner, its budget, its placeholder and the statement that the money stays in P8.
4. Record the approval, the limit and the rule-package rows of AC4, with the placeholder on their operation names and no limit value in the document.
5. Record the decision-record element, the error envelope, the rights and the `Idempotency-Key` rule of AC5.
6. Publish the six fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC6, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the eight contract tests pass, the six fakes answer every consumed path and the drift test is green, and the app story, the two screens and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the case of record's fact, and the app story shows it while a fee is routed | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation or the approval declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the spend moves | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-015-1 of the FSD; the check is the owner's | {product} is from {date}. Today's load has not arrived. |

The six message IDs are contract elements and the text of the five legacy and FSD messages is copied unchanged and the text of MSG-P1-001 is copied from the Error and Message Standard v4; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and no path of this service raises it (GAP-2807; ASM-4647).

### 15. Screens and states

The contract serves SCR-20 Enforcement workspace in its requested, seized, auctioned and closed states and SCR-18 Notice approval in its generated, approved, sent, delivered and unserved states, all through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the legal action and its spend panel, rwb-case for the case and its route state, and rwb-payment for the payment state; this baseline fixes the rwb-litigation answers only, and the composite route specification and the screen field list belong to `RWB-PLT-N001-CON`. The pending, rejected, refused and stale states the app story shows read the messages of section 14 on the same route. The empty, loading, error and no access states of SCR-18 are Not specified in the source documents (CG-ALL-9389); the same states of SCR-20 are Not specified in the source documents (CG-ALL-9390).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-015-01 | AC1, AC3 | Contract | Pay court fees and legal expenses; the contract half answers the two operations, the consumed pay-and-post row and its placeholder |
| TC-E5-015-02 | AC2, AC4 | Contract | Rule R-LIT-30; the contract half answers the post-condition properties, the rule-package row and the approval row |
| TC-E5-015-03 | AC4, AC5 | Contract | Not recorded; the contract half answers the decision-record element, the error envelope and the MSG-P7-003 path |
| TC-E5-015-04 | AC5, AC6 | Contract | A role without the right and a fee paid twice; the contract half answers the 403 with MSG-P4-002, the 409 and the `Idempotency-Key` rule |
| TC-E5-015-05 | AC5 | Contract | A forced decision record write failure; the contract half answers the MSG-P7-003 path of the surface |
| TC-S4-E5015-CON-01 | AC1, AC2 | Contract | The document validates; the two operations, the base, the six status values, the six action types, the three approval states and the absence of a fee property |
| TC-S4-E5015-CON-02 | AC3, AC4 | Contract | The four consumed rows validate with their placeholder fields marked, one hop and a 2 s budget; the approval is a P7 child workflow |
| TC-S4-E5015-CON-03 | AC5 | Contract | The decision-record element validates against the library schema; the rights of TSD S4 T6.1 and the seven error responses with one message ID per condition |
| TC-S4-E5015-CON-04 | AC6 | Contract | The six fakes match the document and a drifted fake fails the build; the absence test for a `v_ace_*` read, a payment or `recovery_case` property, a second topic and a Schedule |
| TC-S4-E5015-CON-05 | AC5 | Contract | Boundary of the tables of 12.7: `legal_action`, `decision_record` and `idempotency_key` only, each with its owner; no foreign key leaves the schema (DP-01) |

The five legacy cases are the legacy cases of RWB-E5-015 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by `RWB-S4-E5015-APP`. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The five cases `TC-S4-E5015-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the fee schedule values, the fee types, the D7.4 limit, the approval window and the lists stay reference data or rule rows, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, list values and a rule version only; every example is synthetic.
- The money stays with rwb-payment: the document declares no posting property, no ledger entry, no balance and no payment row of rwb-litigation (BR1).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on `rwb_payment` or any other `rwb_*` schema, and the boundary test fails a build that adds one (DP-05).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence test of AC6 fails a build that declares a `v_ace_*` read, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| FEAT-LIT-15 | Pay court fees and legal expenses (FSD S4 A2.15); the legacy master and TSD S4 T8 carry no requirement ID for this key (GAP-2810; ASM-4650) | The two operations, the vocabulary, the four consumed rows and the decision-record element | TC-E5-015-01, TC-S4-E5015-CON-01, TC-S4-E5015-CON-03 |
| R-LIT-41, R-LIT-42, R-LIT-43 | Fee due, approved and rejected (Business Rules and Routing Logic v4) | The approval, limit and rule-package rows of 12.2 and 12.5 | TC-E5-015-02, TC-S4-E5015-CON-02 |
| R-LIT-30 | Filing: court case number and hearing timers (asserted only) | The post-condition properties of AC2 and the rule named in the package row | TC-E5-015-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S4-E5015-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-015, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by `RWB-S4-E5015-APP`; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the four new contract cases TC-S4-E5015-CON-01 to -04 |
| Feature and screens | FEAT-LIT-15, SCR-20 Enforcement workspace and SCR-18 Notice approval |
| Rules | R-LIT-41 to R-LIT-43 and R-LIT-30, named from the Business Rules and Routing Logic v4 and governed in rwb-decision (GAP-2809) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two operations, the evaluation of R-LIT-41 to R-LIT-43, the decision record, the approval request and the payment request: `RWB-S4-E5015-APP`.
- The payment and posting of the approved spend against the case, and the general ledger entry: rwb-payment (P8). **The money is paid and posted by rwb-payment, and no part of this baseline moves it** (GAP-2806; ASM-4646).
- The fee schedule, its versions and the fee types, and the case of record with its route states: rwb-case (P3), whose reads this baseline declares as consumed and faked (GAP-2807).
- The approval child workflow, the LITIGATION package and the rows of R-LIT-30 and R-LIT-41 to R-LIT-43: rwb-decision (P7) (GAP-2809).
- The D7.4 limit, the roles and the scope behind the two operations: rwb-access (P4).
- The filing, the court case number, the hearing timers and the judgment: `RWB-S4-E5010-APP`, `RWB-S4-E5011-APP` and the judgment story of this service (GAP-2808).
- The fee receipt document, the partner expense claim and the ACE facts, including the freshness of the data product and the interaction ledger: rwb-document (P5), rwb-partner (S9) and rwb-source-data (P1).
- The gateway-bff composite route and the screen field list of SCR-20 and SCR-18: `RWB-PLT-N001-CON` and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
