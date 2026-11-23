# RWB-S6-E6005-CON Award the lot and test the price - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6005-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the award step of rwb-debtsale, split from RWB-E6-005. It fixes API-S6-003 `POST /debt-sale-lots/{lotId}/award` on base `/api/recovery/debtsale/v1` (DP-13) with its `AwardRequest`, its `DecisionLogEntry` answer, its error set and its `Idempotency-Key`; the `rwb.debtsale.LotAwarded.v1` event on `rwb.debtsale.events.v1`; the consumed rwb-case state and move rows, the rwb-decision package and approval rows, the rwb-access DoA limit and the rwb-source-data score (DP-05); the decision-record element of DP-03; the rights, the tables, the fakes and the absence tests. The plan's C row is empty although four services are consumed, DP-09 is absent although the step publishes, and no S6 extract exists for the module (GAP-2990, GAP-2991, GAP-2992; ASM-4938, ASM-4939, ASM-3171). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the award step of rwb-debtsale — API-S6-003 and its `AwardRequest` and `DecisionLogEntry`, the `LotAwarded` event, the consumed rwb-case, rwb-decision, rwb-access and rwb-source-data rows, the decision-record element, the rights, the tables and the fakes**, so that **the app story, the award screen and the wave 4 harness build against one fixed, testable contract on Day 1 and an award field, an event field, a consumed shape or a list value can never drift without a failing build**.

The baseline is deliberately narrow: it declares one write of this service and describes the four boundaries the award crosses. It declares no lot read, no data-room operation and no schedule.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy award of RWB-E6-005 crossed four boundaries at once: an officer screen, the decision log, a model score and a case state, all inside one process and one `recovery` schema. The target splits them: rwb-decision owns the rule package, the approval chain and the ledger; rwb-access owns the DoA table; rwb-source-data owns the ACE views and the score; rwb-case owns the case and its route states; rwb-debtsale owns the lot and its award columns. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the award request and its answer, the `LotAwarded` payload, the rule and approval rows, the DoA row, the case state and move, the score shape and the decision record.

The baseline also fixes the naming the checks require: schema `rwb_debtsale`, login `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (Template and Rules §R4). It records that rwb-debtsale holds no grant on `rwb_decision`, `rwb_access`, `rwb_case` or `rwb_source_data`, so those are consumed on their owners' contracts only.

Three points are carried as gaps and assumptions rather than decided quietly: the plan's C row is empty while four services are consumed and some consumed operations have no published name (GAP-2990), DP-09 and its outbox library are absent while the step publishes `LotAwarded` (GAP-2991), and the legacy key's rule and award boundaries span three sibling stories (GAP-2994).

The wave and the date are the plan's and the legacy epic's: this key is EP06 and therefore wave 4 with release 30 April 2027, while rwb-debtsale is created in wave 3, so one service delivers in two waves and the date is copied unchanged and marked tentative (GAP-2993; ASM-4940).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `approval`, `decision_log_entry` and `rule_row` are P7's, `delegation_limit` is P4's, `recovery_case` is P3's, the score data product and the `v_ace_*` views are P1's, `document` is P5's, `notice` is P6's, `proceeds` is P8's. This document never declares another service's table or operation as its own.
- The rwb-case, rwb-decision, rwb-access and rwb-source-data contracts are published with their fakes, so the consumed rows name a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2990; ASM-4938).
- The DS rule package and its rows for R-DS-19, R-DS-20 and R-DS-04 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `debt_sale_lot` and `debt_sale_account` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The lot read API-S6-002 belongs to RWB-S6-E6001-APP and the data-room operations to RWB-S6-E5026-APP; none is declared here.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-debtsale for this step: the award operation with its path parameter, its request, its answer and its error responses.
2. Fix the `AwardRequest` element: the winning buyer reference, the buyer class and the award decision reference, with the values drawn from the lot columns and the decision record and no amount invented.
3. Fix the `DecisionLogEntry` answer as the local decision-record element of DP-03: rule ID, rule version, model version, inputs reference, outcome, decided-at.
4. Fix the `LotAwarded` event: its name, its topic, its CloudEvents envelope, its payload and its two consumers, with no personal data.
5. Fix the consumed rows: the rwb-case state read and move answer, the rwb-decision package read and approval chain, the rwb-access DoA limit and the rwb-source-data score, marking the names the sources do not publish with the placeholder.
6. Record the rights of the award operation and its scope.
7. Publish the contract tables of section 12, the tables of section 11 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the element shapes, the error envelope, the rights, the drift between a fake and the document, the event payload and the boundary.
9. Tag the baseline and hand it to RWB-S6-E6005-APP, the award screen and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or response body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC7 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC6 |
| X5 | A value outside `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-SEGMENT` or `LOV-PUTBACK` appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation, an approval or ledger row, a DoA row or a `recovery_case` row | The review fails the baseline; the boundary test fails the build | None | AC7 |
| X7 | The document declares a second event, a second topic, a Schedule or a Quartz row | The absence test fails the build | None | AC4, AC7 |
| X8 | The rights of the operation are not the ones TSD S6 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-case, rwb-decision, rwb-access and rwb-source-data only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operation, the event, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S6-E6005-APP, the award screen and the wave 4 harness on Day 1, and the four consuming services on the same day |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the award step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of approval and rule_row is P7, of delegation_limit is P4, of recovery_case is P3 and of the score data product is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The award operation is declared on the debtsale base with its shape, its errors and its idempotency (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-debtsale is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /debt-sale-lots/{lotId}/award with an AwardRequest body and a DecisionLogEntry answer of status 200, under the base /api/recovery/debtsale/v1 and owned by rwb-debtsale
    Then the operation declares the path parameter lotId and the Idempotency-Key header
    Then the answers 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then the document declares no lot read, no lot creation and no data-room operation, and names API-S6-002, API-S6-001 and API-S6-004 as sibling stories' (GAP-2994; ASM-4941)

  Scenario: AC2 The AwardRequest and the DecisionLogEntry answer carry the award fields and the closed lists (new, D-RCV-60)
    Given the request and the answer sections of the baseline
    When they are compared with TSD S6 T-A.2 and T3.1 and T3.2
    Then the AwardRequest declares the path lotId, buyer_partner_id of DF-SAL-025, buyer_class of DF-SAL-026 and the decision reference, and declares no amount, because no column or field for the bid or the award price exists (GAP-2995; ASM-4942)
    Then buyer_class is declared against LOV-BUYER-CLASS with the values AMC and NON_AMC, and the lot values read by the step are declared against LOV-SEGMENT, LOV-LOT-STATUS and LOV-PUTBACK
    Then the DecisionLogEntry answer declares the fields of DF-DEC-001 to DF-DEC-018: rule ID, rule version, model version, inputs reference, outcome and decided-at
    Then the answer is the local decision-record element of DP-03, not a P7 ledger row, and the document says so
    Then the document records that the field names beyond the path parameter and the two lot columns are Not specified in the source documents (GAP-2995; ASM-4942)

  Scenario: AC3 The consumed rwb-case, rwb-decision, rwb-access and rwb-source-data rows are declared (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the context pack, the Ownership Map and the owner documents
    Then the case state read is declared as consumed from P3 rwb-case on the GET /cases/{caseId} family, and the case-move answer with AWARD_PENDING and BID_BELOW_RESERVE is declared with its operation name Not specified in the source documents (GAP-2990; ASM-4938)
    Then the DS rule package read with R-DS-19, R-DS-20 and R-DS-04 and the approval chain of GET /approvals and POST /approvals/{approvalId}/approve, /return, /refuse are declared as consumed from P7
    Then the DoA limit is declared as consumed from P4 rwb-access on GET /doa-limits, with the level, the measure and the limit the award is tested against
    Then the score and its model version are declared as consumed from P1 rwb-source-data on its contract, with no v_ace_* view and no ACE table read by rwb-debtsale (DP-05)
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The LotAwarded event is declared on the service topic with its payload and no personal data (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with TSD S6 T5.3, Architecture v5 slide 43 and the context pack connection matrix
    Then the event is declared as rwb.debtsale.LotAwarded.v1 (EV-23, LotAwarded) on the topic rwb.debtsale.events.v1, with its retry and .dlt topics and the CloudEvents envelope
    Then the payload declares the lot id, lot_no, the case reference, buyer_partner_id, buyer_class, the decision reference, the rule ID with its package version and the awarded-at time, and no name, contact value or identity number
    Then the event is written from the outbox in the same transaction as the lot update
    Then the document names rwb-payment and rwb-reporting as the consumers and records that DP-09 and RWB-PLT-TE006-CON are absent from the plan (GAP-2991; ASM-4939)
    Then the document declares no consumed event and names ProceedsMatched as the settlement story's

  Scenario: AC5 The rights, the scope and the approval limit are fixed on the award operation (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S6 T-A.1 and T6.1 and the legacy permission rows
    Then the award declares Debt sale right A with the scope applied, and RW-DEBTSALE holds CRUA, RW-PRODHEAD and RW-HEADASL hold RA
    Then the document records the legacy A right holders as RW-DEBTSALE, RW-PRODHEAD and RW-HEADASL and gives PT-BUYER and PT-RAMC no right on the operation
    Then the document declares the award tested against the rwb-access DoA limit and approved on the P7 chain where the limit requires it, and declares no approval operation and no approval row of this service
    Then a repeated request with the same Idempotency-Key describes no second effect (GAP-2990; ASM-4938)

  Scenario: AC6 The decision-record element and the fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per award outcome with the case reference, the lot reference, the bid reference, the rule ID, the package version, the model version, the DoA level, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the lot row changes, and a failed write leaves the lot unchanged with MSG-P7-003
    Then the rwb-case fake answers BIDS_RECEIVED and an accepted and a refused move; the rwb-decision fake answers the package with R-DS-19, R-DS-20 and R-DS-04 and a chain inside and outside the limit
    Then the rwb-access fake answers the DoA limit of the level and a limit below the award, and the rwb-source-data fake answers the score with its model version and as-of date
    Then the rwb-debtsale fake answers the award of LOT-2027-000041 with its buyer and its decision record
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline, the tables and the boundary are fixed and no Schedule is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the base is /api/recovery/debtsale/v1, the topic is rwb.debtsale.events.v1, the queue is rwb-debtsale and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then the tables named as owned are debt_sale_lot, debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and approval, decision_log_entry, rule_row, delegation_limit, recovery_case, document, notice, proceeds, the score data product and every v_ace_* view are named as other owners' and consumed only through their contracts
    Then the document declares no Schedule, no Quartz row and no shared job table, and the absence test fails a build that adds one
    Then the document records that the plan's C row is empty although four services are consumed, that no S6 extract exists so FSD S6 v3 and TSD S6 v2 stand in, and that the release is 30 April 2027 (tentative) (GAP-2990, GAP-2992, GAP-2993; ASM-4938, ASM-3171, ASM-4940)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6005-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot, its buyer columns and its award behaviour are rwb-debtsale's, and the contract declares their fields, their lists and their flags on the `AwardRequest` and the answer only | Architecture v5 slide 41; TSD S6 T3.1 and T3.2; context pack Ownership rows |
| BR2 | The decision record is declared as an element written before the lot row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy RWB-E6-005 AC1 and AC4 |
| BR3 | The rule package, the approval chain and the ledger stay with rwb-decision, and the DoA table with rwb-access: the contract declares them as consumed and declares no `approval` row, no ledger row and no `delegation_limit` property | Context pack; GAP-2990 |
| BR4 | The model score is consumed from rwb-source-data and the contract declares no `v_ace_*` path, no ACE table and no view grant of rwb-debtsale | DP-05; GAP-2995 |
| BR5 | `LotAwarded` is the only event of this step, on the service topic, with no personal data and with rwb-payment and rwb-reporting as consumers | TSD S6 T5.3; context pack slide 13; GAP-2991 |
| BR6 | The vocabulary is closed: `LOV-BUYER-CLASS`, `LOV-LOT-STATUS`, `LOV-SEGMENT` and `LOV-PUTBACK` are published as enumerated values and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-009 |
| BR7 | No personal data in a schema, an example, an event or a fake: identifiers, codes, amounts, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR8 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR9 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR10 | The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR11 | The cap, the reserve rule and the DoA limits are values in force in the DS package and the P4 table, named here and declared nowhere here | Business Rules and Routing Logic v4; GAP-2990 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the event, the consumed rows, the rights and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the award screen, the wave 4 harness and the four owner teams accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The boundary or absence test fails: a sibling operation, an approval row, a `recovery_case` property, a `v_ace_*` path, a second event or a Schedule | In review |

The route machine the document describes is the app story's and rwb-case's: `BIDS_RECEIVED`, `AWARD_PENDING` and `BID_BELOW_RESERVE` are case route states, and `LOV-LOT-STATUS` is BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED. This baseline fixes both vocabularies, declares no value for the award in the lot list, and moves no lot and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, the award screen, the wave 4 harness and the owners of rwb-case, rwb-decision, rwb-access and rwb-source-data) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the outbox library and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an event, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-debtsale login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Award request | The path lotId, `buyer_partner_id` (DF-SAL-025) and `buyer_class` (DF-SAL-026), the decision reference and the `Idempotency-Key` header; no amount, because no bid or award-price field exists (GAP-2995) |
| Decision answer | `DecisionLogEntry` of DF-DEC-001 to DF-DEC-018 through the local library, written before the lot row changes (DP-03) |
| Lot element | The columns of DF-SAL-020 to DF-SAL-030, of which this step reads all and writes two |
| Account element | The columns of DF-SAL-031 to DF-SAL-037, read as the accounts of the lot |
| Lists | `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK`, published as enumerations and read as reference data at their version |
| Event payload | Lot id, lot_no, case reference, buyer_partner_id, buyer_class, decision reference, rule ID with its version, awarded-at; no personal data |
| Consumed shapes | The case state and move of P3, the package and approval rows of P7, the `delegation_limit` row of P4 and the score data product of P1, each declared as consumed and faked |
| Not declared here | `approval`, `decision_log_entry` and `rule_row` (P7), `delegation_limit` (P4), `recovery_case` and `timer` (P3), the score data product and the `v_ace_*` views (P1), `document` (P5), `notice` (P6), `proceeds` (P8), and the sibling operations API-S6-001, API-S6-002, API-S6-004 and API-S6-005 |
| Consumed fields with no source | The operation name of the package read, the score read and the case-move answer, and the field IDs of the score data product: Not specified in the source documents (GAP-2990, GAP-2995; ASM-4938, ASM-4942) |

**No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/debt-sale-lots/{lotId}/award` | `AwardRequest` in, `DecisionLogEntry` of status 200 out (API-S6-003) | Debt sale, right A, scope applied | `Idempotency-Key` header |

The operation answers 401, 403 with MSG-P4-002, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation ID is API-S6-003 of TSD S6 T-A.1 and the path is that of the target base, not the monolith form. `POST /debt-sale-lots` (API-S6-001) is the lot-building story's, `GET /debt-sale-lots/{lotId}` (API-S6-002) is RWB-S6-E6001-APP's, and the data-room operations (API-S6-004 and API-S6-005) are RWB-S6-E5026-APP's; none is declared by this baseline (GAP-2994; ASM-4941).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state `BIDS_RECEIVED` and the case reference; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2990; ASM-4938)) | rwb-case (P3) | P3 rwb-case | The move `AWARD_PENDING` or `BID_BELOW_RESERVE` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The read of the DS rule package version in force (operation name Not specified in the source documents (GAP-2990; ASM-4938)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows of R-DS-19, R-DS-20 and R-DS-04 with the 54 percent cap; faked |
| `GET /approvals` and `POST /approvals/{approvalId}/approve`, `/return`, `/refuse` | `/api/recovery/decision/v1` | P7 rwb-decision | The approval chain started above the DoA limit and its answer; faked |
| `GET /doa-limits` | `/api/recovery/access/v1` | P4 rwb-access | The `delegation_limit` row of the officer's level, which the award is tested against; faked |
| The read of the model score and its model version (operation name Not specified in the source documents (GAP-2990; ASM-4938)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The score and estimate of the lot's accounts with their as-of date and model version; faked; field IDs Not specified in the source documents (GAP-2995; ASM-4942) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-2990; ASM-4938).

#### 12.3 Events published

| Event | Topic | Envelope | Documented payload |
|---|---|---|---|
| `rwb.debtsale.LotAwarded.v1` (EV-23, LotAwarded) | `rwb.debtsale.events.v1`, with its retry and `.dlt` topics | CloudEvents, from the outbox in the same transaction as the lot update | Lot id, lot_no, case reference, buyer_partner_id, buyer_class, decision reference, rule ID with its package version, awarded-at; consumers rwb-payment and rwb-reporting |

The producer is declared and not built by this story. DP-09 and its outbox library are absent from the plan's pattern set, and the absence is recorded (GAP-2991; ASM-4939).

#### 12.4 Events consumed

None. The S6 row of the connection matrix listens to rwb-payment (`ProceedsMatched`), the settlement fact of RWB-S6-E6011-APP's step. This baseline declares no consumer group, no subscription and no inbox of its own, and the absence test of AC4 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per case per stage, the saga child of `CaseWorkflow`, pivot = transfer | `rwb-debtsale` in namespace `rwb-recovery` | The stage that hosts the award branch; its input, signals and outcome for the parent are declared, not built |
| The award branch of `DebtSaleWorkflow` | Workflow branch | `rwb-debtsale` | The step from the closed bidding window to the award outcome: the price test, the DoA test, the optional approval, the record and the stage outcome |
| `ApprovalWorkflow` | Child workflow, the kit's Approval template, owned and run by rwb-decision, started on its queue where the limit requires it | `rwb-decision` (P7) | The maker-checker chain with the DoA lookup as a parameter |
| `testAwardPrice` | Activity | `rwb-debtsale` | The lot, the bids and the package in; the rule ID with its version, the price-test outcome and the DoA test out |
| `recordAward` | Activity | `rwb-debtsale` | The two lot columns, the decision record, the outbox row and the case move out, in one transaction |

The activity names are target design choices and no activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the bidding-window close and the approval answer; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its reserve, its buyer columns and its status; the table the award writes and the answer reads |
| debt_sale_account | S6 (`rwb_debtsale`) | The accounts of the lot; read for the price test and the answer |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the award outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated award and the outcome it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The outbox row of `LotAwarded`, written in the same transaction as the lot update |

`approval`, `decision_log_entry` and `rule_row` (P7), `delegation_limit` (P4), `recovery_case` and `timer` (P3), the score data product and every `v_ace_*` view (P1), `document` (P5), `notice` (P6) and `proceeds` (P8) are not owned by this baseline; it names them only as answers or rule versions of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | The state `BIDS_RECEIVED` of case `RC-2027-000611`, the moves `AWARD_PENDING` and `BID_BELOW_RESERVE` accepted, and a refused move | AC3, AC6 |
| rwb-decision rule-package fake | The DS package at its version with R-DS-19, R-DS-20 and R-DS-04 and the 54 percent cap | AC3, AC6 |
| rwb-decision approval-chain fake | A chain decided inside the limit, one decided outside it, and no answer beyond 2 s | AC3, AC6 |
| rwb-access DoA fake | The `delegation_limit` rows that let the officer award, and a limit below the award | AC3, AC5, AC6 |
| rwb-source-data score fake | The score and estimate of the lot's accounts with their model version and as-of date | AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC6 |
| rwb-debtsale award fake | The award of `LOT-2027-000041` with its buyer, its decision record and its event payload | AC1, AC2, AC6 |
| gateway-bff composite route fake | The merged SCR-26 answer for lot `LOT-2027-000041` | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished operation names and the score field IDs are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2990, GAP-2995; ASM-4938, ASM-4942).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | The award write on `/api/recovery/debtsale/v1`; the rwb-case state read and move answer, the rwb-decision package and approval rows, the rwb-access DoA read and the rwb-source-data score read; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.debtsale.LotAwarded.v1` on `rwb.debtsale.events.v1`; no consumed event |
| Temporal | 1 workflow, 1 branch, 2 activities and 1 conditional child workflow declared, 0 registered | `DebtSaleWorkflow` and its award branch, `testAwardPrice` and `recordAward` on `rwb-debtsale`, and the P7 `ApprovalWorkflow` child on `rwb-decision`; no Schedule |
| File | None | No file is read, built or delivered here; the tape and the data room pack are the data-room stories' |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no lot, no case, no approval and no rule package. What it publishes is one OpenAPI 3.1 document, one event schema, nine contract tables, the rights of the award and eight fakes.

**Deliverables.** The additive document `openapi/rwb-debtsale-v1.yaml` with the award operation, the `AwardRequest` and `DecisionLogEntry` elements, the `LotAwarded` schema, the vocabulary of the four lists as published enumerations, the contract README rows for the six consumed rows and their placeholders, and the eight WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before the lot row changes, on the shared `rwb.decision-record.v1`. DP-05 replaces the legacy `v_ace_score` read with the score data product. DP-13 moves the base and nothing else. DP-19 is behind SCR-26, whose screen model is the edge contract's, and this baseline fixes the rwb-debtsale answer only. DP-09 is absent although the step publishes, and the absence is recorded (GAP-2991).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. The six consumed rows are C dependencies in fact and not in the metadata row, and the approval chain adds a Temporal dependency on the P7 queue that no row expresses (GAP-2990; ASM-4938).

**Build steps**

1. Write the award operation and validate the additive rule of AC1, with the sibling operations declared as another story's.
2. Write the `AwardRequest`, the `DecisionLogEntry` and their lists of AC2, with the missing price field and the element names recorded.
3. Record the six consumed rows of AC3 with their owners, their budget and the placeholders.
4. Publish the `LotAwarded` schema and its no-personal-data test of AC4.
5. Record the rights and the approval limit of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the eight fakes of AC6 and the drift test.
8. Record the naming baseline, the tables and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the award screen and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the exclusion path of RWB-S6-E5023-APP, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation (VR-S6-009-1) | Enter {field}. |
| MSG-P4-002 | The role lacks the Debt sale A right the award declares, and a role without the approval right of the chain tries the act | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S6-001 is carried because it is in the message set of this feature, and the check itself belongs to the exclusion story of this service.

### 15. Screens and states

The contract serves SCR-26 Award in its open and closed states through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot, its reserve, its bids and its award decision, rwb-decision for the approval chain and the decision record, and rwb-case for the case and its route state; this baseline fixes the rwb-debtsale answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal, below-reserve, held-for-approval and not-recorded states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-005-01 | AC1, AC2 | Contract | The lot `LOT-2027-000041` of case `RC-2027-000611`; the contract half answers the award operation, the `AwardRequest` and the `DecisionLogEntry` shape |
| TC-E6-005-02 | AC3 | Contract | The case state and move, the package and approval rows, the DoA limit and the score; the contract half answers each consumed shape |
| TC-E6-005-03 | AC3, AC4 | Contract | The R-DS-04 row and the `LOT_WITH_COMMITTEE` shape, and the `LotAwarded` payload with no personal data |
| TC-E6-005-04 | AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element |
| TC-E6-005-05 | AC5 | Contract | A role without the Debt sale A right; the contract half answers 403 with MSG-P4-002 and the rights of the award |
| TC-E6-005-06 | AC4, AC7 | Contract | A forced record failure and a forbidden element; the contract half answers the event absence and the boundary tests |
| TC-S6-E6005-CON-01 | AC1 | Contract | The document validates; the award operation, its path, its header and its six error answers are present, and no sibling operation is declared |
| TC-S6-E6005-CON-02 | AC2 | Contract | The `AwardRequest` and the `DecisionLogEntry` validate with their fields, their required flags and the four closed lists |
| TC-S6-E6005-CON-03 | AC3 | Contract | The six consumed rows and their placeholders; the no-`approval`, no-`delegation_limit`, no-`recovery_case` and no-`v_ace_*` boundary |
| TC-S6-E6005-CON-04 | AC4 | Contract | The `LotAwarded` schema, its envelope, its consumers and the no-personal-data test |
| TC-S6-E6005-CON-05 | AC5 | Contract | RW-DEBTSALE holds CRUA and RW-PRODHEAD and RW-HEADASL hold RA; the partner roles hold no right |
| TC-S6-E6005-CON-06 | AC6 | Contract | The eight fakes match the document and a drifted fake fails the build |
| TC-S6-E6005-CON-07 | AC7 | Contract | The naming baseline; the absence test for a second event, a second topic, a Schedule and a Quartz row; the boundary test |

The six legacy cases are the legacy cases of RWB-E6-005 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6005-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S6-E6005-CON-01` to `-07` are new. The full test is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the 54 percent cap, the reserve rule, the 45-day target, the DoA limits, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example, an event or a fake: identifiers, codes, amounts, dates and a rule version only, and every example is synthetic.
- The rule package, the approval chain and the ledger stay with rwb-decision, the DoA table with rwb-access, the score with rwb-source-data and the case with rwb-case: the document declares no property or row of any of them (BR3, BR4).
- The sibling operations stay with their stories: the document declares no lot read, no lot creation and no data-room operation (BR10).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a second event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the outbox library and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-006 | The award of a lot is approved and recorded with the price achieved against the reserve (Must, E6; FSD S6); TSD S6 T8 maps REQ-S6-006 to FEAT-DBS-05 while the FSD gives the award as FEAT-DBS-09, and the difference is recorded (GAP-2994; ASM-4941) | The award operation, the `AwardRequest`, the `DecisionLogEntry` and the six consumed rows | TC-E6-005-01, TC-E6-005-02, TC-S6-E6005-CON-01, TC-S6-E6005-CON-02 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-S6-E6005-CON-07 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `LotAwarded` schema and its outbox rule | TC-S6-E6005-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-S6-E6005-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and the ledger entry of P7 | TC-S6-E6005-CON-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-005, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S6-E6005-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the seven new contract cases TC-S6-E6005-CON-01 to -07 |
| Feature and screens | FEAT-DBS-09, SCR-26 Award and SCR-25 Lot builder |
| Rules | R-DS-19, R-DS-20, R-DS-04 and R-DS-23, from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |
| Source text | FSD S6 Debt sale v3 A2.9; TSD S6 Debt sale v2 T3.1, T3.2, T4, T5.3, T6.1 and T-A; legacy RWB-E6-005 |

### 19. Out of scope

- The behaviour behind the award operation, the evaluation of R-DS-19 and R-DS-20, the DoA test, the record, the lot columns, the event and the case-move answer: RWB-S6-E6005-APP.
- The lot read API-S6-002 and the committee approval: RWB-S6-E6001-APP; the lot build, the agent estimate and API-S6-001: RWB-S6-E5024-APP.
- The sale agreement, the customer notices, R-DS-23 and the move to `LOT_AWARDED`: RWB-S6-E6006-APP.
- The data room read and bid operations API-S6-004 and API-S6-005: RWB-S6-E5026-APP; the buyer qualification: RWB-S6-E6002-APP.
- The rule package, the approval chain, the approver's act, the decision log entry and its versioning: rwb-decision (P7) (GAP-2990).
- The DoA table and its limits: rwb-access (P4) (GAP-2990).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked.
- The model score, the score data product and the `v_ace_*` views: rwb-source-data (P1) (GAP-2995).
- The transfer of the awarded data to the buyer: RWB-S6-E6007-APP; the settlement and `ProceedsMatched`: RWB-S6-E6011-APP (P8).
- The document, its custody and its retention: rwb-document (P5); the notices: rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-26: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
