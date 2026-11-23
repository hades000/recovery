# RWB-S4-E5022-CON Match enforcement proceeds to the case - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5022-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the enforcement-matching step of rwb-litigation, split from RWB-E5-022. It fixes the three legal-action operations on `/api/recovery/litigation/v1` (DP-13), the `ENFORCEMENT`, `LED_AUCTION` and `CIVIL_CASE` action types and the match outcome fields of `legal_action`, the match and close shapes, the `Idempotency-Key` rule and the error envelope, the consumed money fact of rwb-payment (P8) and the case-move answer of rwb-case, and the decision-record element of DP-03. The money is matched and posted by rwb-payment and never by this contract (GAP-1891; ASM-3106); `ProceedsMatched` does not list rwb-litigation as a consumer (GAP-1892; ASM-3107); the operation names and the round facts have no source specification and are carried with the placeholder (GAP-1896; ASM-3111). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the enforcement-matching step of rwb-litigation — the three legal-action operations on `/api/recovery/litigation/v1`, the `ENFORCEMENT`, `LED_AUCTION` and `CIVIL_CASE` action types and the match outcome fields of `legal_action`, the request and answer shapes of the match and close steps, the `Idempotency-Key` rule, the error envelope and the rights, the consumed payment and proceeds fact of rwb-payment, the case-move answer of rwb-case, the decision-record element, the tables and the fakes**, so that **the app story, the screens and the tests of this legacy key build against one fixed, testable contract on Day 1 and an action type, an outcome field, a status value or an answer shape can never drift between rwb-litigation, rwb-payment and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-022 crossed three boundaries at once: an officer screen, a payment and proceeds fact, and a case state. The target splits them: the money is matched and posted by rwb-payment (P8), the case of record and its route states stay with rwb-case (P3), and the enforcement legal action, the enforcement step and the LED auction ladder entry stay with rwb-litigation (S4). Each boundary is now a contract that another team builds against, so each has to be fixed before the app story starts: the action types of `LOV-LEGAL-TYPE`, the four outcome fields of `legal_action`, the shape of the close, the fact the P8 contract answers, the case-move answer and the record of the decision.

The baseline also fixes the naming that the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation` (Architecture v5 slide 41 notes). It records that rwb-litigation holds no `v_ace_*` grant and no grant on `rwb_payment` (Architecture v5 slide 29), so DP-05 is declared as a prohibition and the payment fact is consumed on the owner's contract only. It records that `ProceedsMatched` does not list rwb-litigation as a consumer, so this contract declares no consumed event and the fact arrives synchronously.

Three points are carried as gaps and assumptions rather than decided quietly: the plan gives the two consumed contracts of rwb-payment no C row (GAP-1891), the trigger of the step has no source specification because the legacy story says it runs unattended while the FSD declares no background event (GAP-1893), and the rule rows of R-LIT-51, R-LIT-65 and R-LIT-70 with the round result and the percentage of official value have no field list anywhere (GAP-1895, GAP-1896).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `legal_action` and `hearing` are S4's, `proceeds` is P8's, `recovery_case` is P3's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's. This document never declares another service's operation as provided.
- `RWB-P8-E4044-CON` "Match auction and enforcement proceeds" and `RWB-P8-E4049-CON` "Apply proceeds to the case balance" are published, so the two consumed rows of 12.2 name a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-1891; ASM-3106).
- The case-move answer of rwb-case is fixed here as a shape only; no source names a published operation that moves a case state on behalf of a stage, and the name is Not specified in the source documents (GAP-1891; ASM-3106).
- The LITIGATION rule package, its rule rows for R-LIT-51, R-LIT-65 and R-LIT-70 and its D7 approval limit are governed in rwb-decision (P7); this baseline names them and declares none of them (GAP-1895; ASM-3110).
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-litigation for this step: the three operations with their request and answer elements, the action types, the outcome fields, the rights and the six error responses.
2. Fix the shape of the close: the `LegalActionUpdate` element, the status value `CLOSED` of `LOV-LEGAL-STATUS`, the rule ID and the package version, and the answer that carries the match outcome.
3. Fix the consumed money fact of the two P8 contracts and mark the fields the sources do not give with the placeholder.
4. Fix the case-move answer of rwb-case: the move, the rule ID, the version and the decided-at time, with no case row read or written here.
5. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, written before the legal action changes.
6. Record the closed vocabulary of the action types and the action status, and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the five contract fakes.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `proceeds` or `recovery_case` write, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-S4-E5022-APP, the screens and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | The consumed money fact or the case-move answer has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-LEGAL-TYPE` or `LOV-LEGAL-STATUS` appears in the document or in an example | The vocabulary test fails the build | None | AC1, AC8 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `proceeds` row or a `recovery_case` row | The review fails the baseline; the boundary test fails the build | None | AC8 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC2, AC5 |
| X8 | The rights of an operation are not the ones TSD S4 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-payment and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the action types, the status values, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S4-E5022-APP, the two screens and the wave 3 harness on Day 1, and the rwb-payment and rwb-case teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, five fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the enforcement-matching step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of proceeds is P8 and of recovery_case is P3
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The three legal-action operations are declared with the enforcement and auction action types and the outcome fields (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-litigation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/legal-actions with the LegalAction answer of status 201, GET /legal-actions/{legalActionId} with the LegalAction answer of status 200 and PATCH /legal-actions/{legalActionId} with the LegalAction answer of status 200, all under the base /api/recovery/litigation/v1 and owned by rwb-litigation
    Then action_type is declared against LOV-LEGAL-TYPE with the values NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION and LED_AUCTION, and the three action types of this step are ENFORCEMENT, LED_AUCTION and CIVIL_CASE
    Then status is declared against LOV-LEGAL-STATUS with the values OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN, and the close writes CLOSED
    Then the match outcome is carried on the existing columns claim_amount, judgment_date, judgment_amount and status, and no property is added to the LegalAction element for a round result, an official value or a case state
    Then every other property of the element is copied from the baseline of the legal action and is not redefined here

  Scenario: AC2 The request and answer shapes of the match and close steps are fixed (new, D-RCV-60)
    Given the match and close sections of the baseline
    When they are compared with the enforcement step of RWB-S4-E5022-APP
    Then the close step is PATCH /legal-actions/{legalActionId} with a LegalActionUpdate that carries the status CLOSED, the rule ID, the package version in force, the case reference and the outcome code
    Then its answer is a LegalAction that carries the same status, the rule ID, the package version and the decided-at time, and no case state
    Then the match step answers a case-move element that carries the case reference, the move CASE_CLOSED or PROCEEDS_MATCHED, the rule ID, the package version and the decided-at time
    Then the POST declares the Idempotency-Key header and its stored answer, and the GET and the PATCH declare none
    Then the field names of LegalActionUpdate and of the case-move element that no source gives are Not specified in the source documents (GAP-1896; ASM-3111) and the document marks them so

  Scenario: AC3 The consumed money fact of rwb-payment is declared and the money stays there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with RWB-P8-E4044-CON and RWB-P8-E4049-CON
    Then the match of auction and enforcement proceeds is declared as consumed from P8 rwb-payment, with the case reference, the proceeds or payment reference, the amount, the value date, the source LED or firm and, for an auction, the round result and the percentage of official value
    Then the application of the proceeds to the case balance is declared as consumed from P8 rwb-payment, and its posting reference is named as P8's
    Then the operation names of the two rows are Not specified in the source documents (GAP-1896; ASM-3111) and the rows carry the placeholder
    Then the round result, the percentage of official value and the proceeds source code are not added to legal_action, and the document declares no proceeds property
    Then every call on the two rows is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The case-move answer is declared and the case row is never written here (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case and of the route states
    Then the case move is declared as an answer to rwb-case with the move CASE_CLOSED or PROCEEDS_MATCHED, the rule ID, the package version and the decided-at time
    Then the document declares no recovery_case property, no case route-state column and no write of a case row from rwb-litigation
    Then the answer carries the stage outcome that the parent CaseWorkflow applies, and the operation name of a REST case-move call for another caller is Not specified in the source documents (GAP-1891; ASM-3106)
    Then the states JUDGMENT_RECORDED, LED_AUCTION, PROCEEDS_MATCHED and CASE_CLOSED are named as the case of record's and are read from its answer only

  Scenario: AC5 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S4 T-A.1 and T-A.2 and with TSD S4 T6.1
    Then the operations answer 400 for a malformed request, 401, 403 with MSG-P4-002, 404, 409 on a closed, withdrawn or wrong-type action, 422 with MSG-GEN-001 and 503 when a downstream does not answer, each with one envelope and one message ID per condition
    Then POST /cases/{caseId}/legal-actions declares Litigation right C, GET /legal-actions/{legalActionId} declares Litigation right R and PATCH /legal-actions/{legalActionId} declares Litigation right U, each with the scope applied
    Then RW-ENFORCE holds Litigation CRU, RW-LITOFF holds CRUA, RW-LEGAL and RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R
    Then a repeated POST with the same Idempotency-Key returns the stored answer and describes no second effect

  Scenario: AC6 The decision-record element is declared and written before the change (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the local decision-record library of DP-03
    Then one decision record is declared per rule outcome with the case reference, the legal action reference, the rule ID, the package version in force, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the legal action changes, and a failed write leaves the action unchanged with MSG-P7-003
    Then the document declares no event of its own for the record and no second topic for this capability
    Then the record carries IDs, codes, dates, amounts and a rule version only

  Scenario: AC7 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-payment match fake answers the matched payment of 2026-12-09 for case "RC-2026-000702", the round sold at 90 percent of official value for action "LA-2026-000702", a fact that does not cover the balance and costs, and no answer beyond 2 s
    Then the rwb-payment apply fake answers the proceeds applied to the balance with its posting reference and a refused apply
    Then the rwb-case fake answers the case states JUDGMENT_RECORDED, LED_AUCTION and PROCEEDS_MATCHED and an accepted and a refused case move
    Then the rwb-decision rule-package fake answers the LITIGATION package at its version with R-LIT-51, R-LIT-65 and R-LIT-70 and one approval answer
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline and the no-v_ace_ boundary are fixed and no cross-schema read is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as owned are legal_action and the library objects decision_record and idempotency_key, and recovery_case, proceeds, decision_log_entry, rule_row, document and hearing are named as other owners' or another story's and are consumed only through their contracts
    Then the document declares no read of a v_ace_* view and no grant on rwb_payment or any other rwb_* schema, and the boundary test fails a build that adds one
    Then the document declares no event published, no event consumed and no Schedule for this step, and the absence test fails a build that adds one
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5022-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The enforcement legal action, the enforcement step and the LED auction ladder entry are rwb-litigation's, and the contract declares their action types, status values and outcome fields on `legal_action` only | Architecture v5 slide 41; Ownership Map (legal_action and hearing owner S4); TSD S4 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the legal action changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-022 AC1 and AC4 |
| BR3 | The money stays with rwb-payment: the contract declares the match and the apply as consumed, declares no `proceeds` property, and describes no posting and no balance change of rwb-litigation | Ownership Map (proceeds owner P8); Architecture v5 slide 17; GAP-1891 |
| BR4 | The case move is answered and not written: the contract declares the answer that carries `CASE_CLOSED` or `PROCEEDS_MATCHED` and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); Architecture v5 slide 41; GAP-1891 |
| BR5 | No ACE view and no ACE table is read: the payment facts are consumed on the owner's contract, and the service holds no `v_ace_*` grant | DP-05; Architecture v5 slides 29 and 41 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET and a PATCH declare none | Architecture v5 slide 11; TSD S4 T-A.2 |
| BR7 | The vocabulary is closed: `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` are published as enumerated values and no state name or list value is a constant of the code | TSD S4 T3.2; BR-S4-022 (FSD S4 A2.22.3.1) |
| BR8 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, list values and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR11 | The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR12 | The rule rows of R-LIT-51, R-LIT-65 and R-LIT-70 and the D7 approval limit are governed in rwb-decision and named here, never declared here | GAP-1895; ASM-3110; Business Rules and Routing Logic v4 |

### 9. State transitions

The lifecycle of this document, not of a legal action:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the vocabulary, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-payment, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or an action type or status value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a `v_ace_*` view, a `proceeds` or `recovery_case` property, a second topic or a Schedule | In review |

The status machine of `legal_action` that the document describes is the app story's: `LOV-LEGAL-STATUS` is OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN, and this baseline fixes the vocabulary and the close to `CLOSED` and moves no action.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, the screens, the wave 3 harness and the owners of rwb-payment, rwb-case, rwb-decision, rwb-access and rwb-source-data) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| LegalAction element | The columns of DF-LEG-001 to DF-LEG-014: `id`, `case_id`, `law_firm_id`, `action_type`, `lawsuit_no`, `black_case_no`, `red_case_no`, `court_name`, `claim_amount`, `filed_date`, `judgment_date`, `judgment_amount`, `lit_status` and `status` |
| Match outcome | Carried on `claim_amount` (DF-LEG-009), `judgment_date` (DF-LEG-011), `judgment_amount` (DF-LEG-012) and `status` (DF-LEG-014); no property is added |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the action changes (DP-03) |
| Proceeds | DF-FIN-001 to DF-FIN-009 of `proceeds` in `rwb_payment`, read only through the P8 owner and never written, copied or joined here |
| ACE account and payment facts | DF-ACE-001 to DF-ACE-054, not read: this service holds no `v_ace_*` grant (DP-05) |
| Not written here | `recovery_case` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7); the notes of the three are answers or rule versions of their owners |
| Round facts | The round result, the percentage of official value and the proceeds source code of the P8 answer: Not specified in the source documents (GAP-1896; ASM-3111) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required; the answer is stored |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its judgment facts and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |
| PATCH | `/legal-actions/{legalActionId}` | LegalActionUpdate in, LegalAction out with the match outcome (API-S4-004) | Litigation, right U, scope applied | Not applicable |

The three operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S4 T-A.1; the paths are those of the target base and not the monolith form. API-S4-005 `POST /legal-actions/{legalActionId}/hearings` and API-S4-001 `POST /notices/{noticeId}/approve` belong to the hearing and notice stories of this service and are not declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The match operation of `RWB-P8-E4044-CON` (operation name Not specified in the source documents (GAP-1896; ASM-3111)) | `/api/recovery/payment/v1` | P8 rwb-payment | The matched payment or auction proceeds of the case: the case reference, the proceeds or payment reference, the amount, the value date, the source LED or firm and, for an auction, the round result and the percentage of official value; faked |
| The apply operation of `RWB-P8-E4049-CON` (operation name Not specified in the source documents (GAP-1896; ASM-3111)) | `/api/recovery/payment/v1` | P8 rwb-payment | The application of the proceeds to the case balance with its posting reference; the row, the posting and the balance are P8's, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-1891; ASM-3106)) | rwb-case (P3) | P3 rwb-case | The move of the case of record to `CASE_CLOSED` or `PROCEEDS_MATCHED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The two P8 rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-1891 with ASM-3106.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its three catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result. This baseline declares none of them, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service.

#### 12.4 Events consumed

None. `ProceedsMatched` is event 25 of `rwb.payment.events.v1`, produced by rwb-payment, and its consumers are rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee; rwb-litigation is not one of them, and the S4 IN row of Architecture v5 slide 19 lists only `NoticeDelivered` and `PartnerResultSubmitted` (GAP-1892; ASM-3107). The money therefore arrives on the P8 contract of 12.2 and the case state on the rwb-case answer; this baseline declares no consumer group, no subscription and no inbox of its own, and the trigger of the step is a workflow step rather than an event (GAP-1893; ASM-3108).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the enforcement-matching step; its signals and its outcome for the parent are declared, not built |
| `matchEnforcementOutcome` | Activity, the one enforcement-matching step | `rwb-litigation` | The case and the legal action in; the rule ID with its package version, the action of the rule and the case move out |

`matchPayments` and `postProceeds` are rwb-payment's activities on queue `rwb-payment` and are declared here as another owner's, never as this service's; no child workflow for the money exists in this service. The activity name is a target design choice and the trigger of the step is read as the arrival of the P8 fact for a case with an open enforcement or LED auction action, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-1893; ASM-3108). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the arrival of the money fact and from the case signal the parent forwards; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The action, its action type, its judgment facts and its status; the table the three operations read and the close writes |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated POST and the answer it holds |

`recovery_case` (P3), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7), `document` (P5) and `hearing` (S4, the sibling stories') are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment match fake (`RWB-P8-E4044-CON`) | The matched payment of 2026-12-09 for case `RC-2026-000702`; the round sold at 90 percent of official value for action `LA-2026-000702`; a fact that does not cover the balance and costs; no answer beyond 2 s | AC1, AC2, AC3, AC7 |
| rwb-payment apply fake (`RWB-P8-E4049-CON`) | The proceeds applied to the balance with its posting reference; a refused apply | AC3, AC7 |
| rwb-case case-move fake | The case states `JUDGMENT_RECORDED`, `LED_AUCTION` and `PROCEEDS_MATCHED`; an accepted move and a refused move | AC2, AC4, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-51, R-LIT-65 and R-LIT-70, and one approval answer | AC6, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6, AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the two P8 rows, the round facts and the case-move answer are derived from the published documents and carry the placeholder until their owners confirm them (GAP-1896, GAP-1891; ASM-3111, ASM-3106).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The create, read and patch of the legal action on `/api/recovery/litigation/v1`; the match and apply of `RWB-P8-E4044-CON` and `RWB-P8-E4049-CON`, and the case-move answer; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `LitigationWorkflow` and `matchEnforcementOutcome` on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no legal action, no case, no balance and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment that declares no event, eleven contract tables and five fakes.

**Deliverables.** The additive document `openapi/rwb-litigation-v1.yaml` for this step, the `LegalActionUpdate` and case-move elements, the vocabulary of `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` as published enumerations, the contract README rows for the consumed rows and their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` read and no grant on `rwb_payment`, because rwb-litigation holds neither (Architecture v5 slides 29 and 41; GAP-1897; ASM-3112). DP-13 moves the base and nothing else. DP-19 is behind SCR-19 and SCR-20, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None; this baseline builds against their fakes until those platform contract stories publish. The two P8 contracts are C dependencies in fact and not in the metadata row (GAP-1891; ASM-3106).

**Build steps**

1. Write the three operations and validate the additive rule of AC1 in the pipeline.
2. Write the `LegalActionUpdate` and case-move elements of AC2 with the placeholder on the fields the sources do not give.
3. Record the two P8 consumed rows of AC3 with their owner, their budget and their placeholders.
4. Record the case-move answer of AC4 and the absence test for a `recovery_case` property.
5. Record the error envelope, the rights and the `Idempotency-Key` rule of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the five fakes of AC7 and the drift test.
8. Record the naming baseline and the boundary of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the eight contract tests pass, the five fakes answer every consumed path and the drift test is green, and the app story, the screens and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-022-1 of the FSD; the check is the owner's and this service holds no ACE batch status read | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and no path of this service raises it (GAP-1897; ASM-3112).

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its pack, instructed, filed, hearing and judgment states and SCR-20 Enforcement workspace in its requested, seized, auctioned and closed states, all through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the legal action and its match outcome, rwb-case for the case and its route state and rwb-payment for the money and the posting; this baseline fixes the rwb-litigation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal and failure states the app story shows — not recorded, refused, stale data — read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-022-01 | AC1, AC2 | Contract | The matched payment of 2026-12-09 for case `RC-2026-000702`; the contract half answers the three operations, the action types, the outcome fields and the close shape |
| TC-E5-022-02 | AC2, AC5 | Contract | Action `LA-2026-000702` at `ENFORCING`; the contract half answers the close to `CLOSED` with the rule ID and the version, and the `Idempotency-Key` of the POST |
| TC-E5-022-03 | AC2, AC3 | Contract | The round sold at 90 percent of official value for action `LA-2026-000702`; the contract half answers the two P8 consumed rows and the placeholders |
| TC-E5-022-04 | AC5, AC8 | Contract | A role without the Litigation right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E5-022-05 | AC5, AC6 | Contract | RW-ENFORCE holds CRU and RW-LITOFF holds CRUA; the contract half answers the rights of AC5 and the decision-record element of AC6 |
| TC-E5-022-06 | AC6, AC7 | Contract | The decision-record stub stopped and a fact that does not cover the balance and costs; the contract half answers the MSG-P7-003 path and the fakes of AC7 |
| TC-S4-E5022-CON-01 | AC1 | Contract | The document validates; the three operations, the base, the six action types, the six status values and the four outcome fields are present, and no round or case property is added |
| TC-S4-E5022-CON-02 | AC2, AC5 | Contract | The `LegalActionUpdate` and case-move elements validate; the `Idempotency-Key` rule and the seven error responses with one message ID per condition |
| TC-S4-E5022-CON-03 | AC3, AC4 | Contract | The two P8 consumed rows and the case-move answer validate with their placeholder fields marked and one hop with a 2 s budget |
| TC-S4-E5022-CON-04 | AC6, AC7, AC8 | Contract | The decision-record element validates against the library schema; the five fakes match the document and a drifted fake fails the build; the absence test for a `v_ace_*` read, a `proceeds` or `recovery_case` property, a second topic and a Schedule |

The six legacy cases are the legacy cases of RWB-E5-022 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5022-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S4-E5022-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the ladder percentages, the balance and costs test, the D7 limit, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, list values and a rule version only; every example is synthetic.
- The money stays with rwb-payment and the case with rwb-case: the document declares no `proceeds` property, no `recovery_case` property, no posting and no case row write (BR3, BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on `rwb_payment` or any other `rwb_*` schema, and the boundary test fails a build that adds one (DP-05).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-litigation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence test of AC8 fails a build that declares a `v_ace_*` read, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-010 | Proceeds from enforcement are matched to the case and posted; the contract fixes the enforcement action, the close and the consumed money fact on which the rule is evaluated (FSD S4 requirements served; Business Requirements Program v4); the legacy story master carries no requirement ID (GAP-1894; ASM-3109) | The three operations, the vocabulary, the two P8 consumed rows and the case-move answer | TC-E5-022-01, TC-E5-022-03, TC-S4-E5022-CON-01, TC-S4-E5022-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S4-E5022-CON-02, TC-S4-E5022-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-022, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S4-E5022-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S4-E5022-CON-01 to -04 |
| Feature and screens | FEAT-LIT-22, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-51, R-LIT-65 and R-LIT-70, named from the Business Rules and Routing Logic v4 and governed in rwb-decision (GAP-1895) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the three operations, the evaluation of R-LIT-51, R-LIT-65 and R-LIT-70, the decision record, the close and the case-move answer: RWB-S4-E5022-APP.
- The matching of the payment or the proceeds and the application to the balance, the posting and the balance change: rwb-payment (P8), `RWB-P8-E4044-CON` and `RWB-P8-E4049-CON`. **The money is matched and posted by rwb-payment, and no part of this baseline moves it** (GAP-1891; ASM-3106).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose case-move answer this baseline declares as consumed and faked.
- The creation of the legal action and its pack, the hearing calendar, the filing and the judgment: the sibling stories of this service, including `RWB-S4-E5021-APP`.
- The authoring, testing, approval and versioning of the LITIGATION package and of the rule rows of R-LIT-51, R-LIT-65 and R-LIT-70, and the D7 approval limit: rwb-decision (P7) (GAP-1895; ASM-3110).
- The ACE account, payment and batch facts, the freshness of the data product and the interaction ledger: rwb-source-data (P1).
- The document of the closed enforcement file, its custody and its retention: rwb-document (P5).
- The gateway-bff composite route and the screen field list of SCR-19 and SCR-20: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
