# RWB-S5-E4033-CON Rent a held asset to a third party - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4033-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the rental step of rwb-asset, split from RWB-E4-033. It fixes the two read operations on `/api/recovery/asset/v1` (DP-13), the rental element and its closed lists including `RENTED`, the consumed rwb-payment, rwb-case, rwb-comms and rwb-source-data rows, the decision-record element of DP-03, the tables and the fakes, and declares no published and no consumed event. The rental element has no physical column set, the consumed operation names are unpublished and ATS has no specification (GAP-2966; ASM-4862, ASM-4863, ASM-4865); the read path carries the ACE asset business key while `asset` is keyed by a record identifier (GAP-2966; ASM-4867); no approval record exists for a Draft baseline and no source fixes a deprecation window or fake retention (GAP-2966; ASM-4868, ASM-4869). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the rental step of rwb-asset — the two asset reads on `/api/recovery/asset/v1`, the rental element with its closed lists, the consumed rwb-payment, rwb-case, rwb-comms and rwb-source-data rows, the decision-record element, the tables and the fakes**, so that **the app story, the two screens and the wave 3 harness build against one fixed, testable contract on Day 1, and a term, a list value, a mandate field or an answer shape can never drift between rwb-asset, rwb-payment, rwb-case and rwb-comms without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy rental of RWB-E4-033 crossed four boundaries at once: an officer screen, the case route state, the auto-debit and the arrears notice. The target splits them — rwb-case owns the case and its route states, rwb-decision the approval and the rule package, rwb-payment the mandate and the money, rwb-comms the notice, and rwb-asset the asset, its holding status and the decision record — so each boundary is now a contract another team builds against, and each is fixed before the app story starts.

The baseline fixes the naming the checks require: schema `rwb_asset`, login rwb-asset, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset`. It records that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition and every foreign fact is consumed on its owner's contract only.

Three points are carried as a gap and assumptions rather than decided quietly: the rental terms have no physical column set and the consumed operation names and ATS have no source (GAP-2966; ASM-4862, ASM-4863, ASM-4865), the read path carries the ACE asset business key while the table is keyed by a record identifier (GAP-2966; ASM-4867), and the baseline sits in Draft with no approval record and no stated deprecation window (GAP-2966; ASM-4868, ASM-4869).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- Ownership is taken from the Ownership Map only: `asset_sale` and `listing` are S5's, `recovery_case`, `assignment`, `task` and `timer` are P3's, `proceeds` is P8's, `decision_log_entry`, `rule_row` and `approval` are P7's, `notice` and `template` are P6's, and every `v_ace_*` view is P1's. The `asset` row has no Ownership Map row and is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 (GAP-2966; ASM-4867).
- The consumed rows are published with their fakes, so each names a real owner document; they are not in the contract-dependency row, which is None, and the absence is recorded (GAP-2966; ASM-4863).
- The DISPOSAL package with R-DIS-25 and R-DIS-63 is governed in rwb-decision (P7); this baseline names it and declares none of it.
- The `asset` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The baseline sits in Draft under D-RCV-60 with no approval record, and no source fixes the deprecation window of a field or the retention of a fake (GAP-2966; ASM-4868, ASM-4869).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this step: the two reads with their elements, filters, rights and error responses.
2. Fix the rental element — asset reference, tenant reference, rental start date, term, rent, currency, payment method and auto-debit reference — with its types, required flags and the list each property is declared against.
3. Record the closed vocabulary of `LOV-HOLDING` with `RENTED` and of `LOV-ASSET-TYPE`, and the rule that no list value is a constant of the code.
4. Fix the consumed rows: the rwb-payment auto-debit request and answer, the rwb-case state read and move answer, the rwb-comms notice request and the rwb-source-data asset read, marking every name and field the sources do not give with the placeholder.
5. Record the decision-record element of DP-03, written before the asset row changes, and the naming baseline with its prohibitions: no `v_ace_*` path, no `recovery_case` property, no foreign schema, no monolith base, no Schedule and no event.
6. Publish the contract tables of §12 and the fakes of 12.8.
7. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence tests and the fake drift test.
8. Tag the baseline and hand it to RWB-S5-E4033-APP, the two screens and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or response body fails schema validation | The schema lint fails the build; a deployed service answers 400 with the envelope | MSG-GEN-001 | AC1, AC4 |
| X2 | A property is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A consumed row carries a name or field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake derives from the published document | None | AC3 |
| X4 | A value outside `LOV-HOLDING`, `LOV-ASSET-TYPE` or `LOV-SEGMENT` appears | The vocabulary test fails the build | None | AC2 |
| X5 | A fake drifts from the document | The drift test fails and the merge is blocked | None | AC5 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a payment amount or an approval row | The review fails the baseline and the boundary test fails the build | None | AC3, AC5 |
| X7 | The document declares a published event, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC5 |
| X8 | The rights of an operation are not the ones TSD S5 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts only |
| Negotiable | The property names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic and the queue are fixed by the architecture |
| Valuable | Unblocks the app story, the two screens and the wave 3 harness on Day 1, and the four owner teams the same day |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the rental step of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of asset_sale and listing is S5, of recovery_case, task and timer is P3, of proceeds is P8, of decision_log_entry, rule_row and approval is P7, of notice and template is P6 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The document validates and a change within major version 1 is additive (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema and the additive rule of the platform
    Then it validates with no error
    Then every change within major version 1 adds a property or an optional field and removes, renames and retypes nothing
    Then a removed, renamed or retyped property fails the contract test and needs a new major version

  Scenario: AC2 The rental element and its closed lists are fixed (new, D-RCV-60)
    Given the rental section of the baseline
    When it is compared with TSD S5 T3.1, TSD S5 T3.2 and the FSD S5 A2.24 field catalog
    Then the Rental element declares the asset reference, the tenant reference, the rental start date, the rental term, the rent, the rent currency, the payment method and the auto-debit reference
    Then the asset reference and the tenant reference are required and the other six properties are optional
    Then the Rental element is declared additively on the Asset element of the two reads
    Then holding_status is declared against LOV-HOLDING with HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED, and RENTED is a value the element may carry
    Then asset_type is declared against LOV-ASSET-TYPE with its six values and from_segment against LOV-SEGMENT
    Then no posting, balance, instalment schedule or arrears value is declared on the element

  Scenario: AC3 The consumed rows are declared with their owners and their placeholders (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the rwb-payment, rwb-case, rwb-comms and rwb-source-data contracts
    Then the auto-debit request is consumed from P8 rwb-payment with the case reference, the asset reference, the rental term and the rent amount as inputs and a mandate reference as its answer
    Then the operation name and the request shape of that row are Not specified in the source documents (GAP-2966; ASM-4863) and the row carries the placeholder
    Then the row declares no posting, balance, receipt, instalment or arrears state, which stay with rwb-payment
    Then the case state read and the case-move answer are consumed from P3 rwb-case with ROUTE_WITH_APPROVER, the route rental and the move RENTAL_ACTIVE it accepts, and the move name is Not specified in the source documents (GAP-2966; ASM-4863)
    Then the asset read is consumed from P1 rwb-source-data with the ACE asset business key, the asset reference, the asset type and the freshness stamp, and its operation name is Not specified in the source documents (GAP-2966; ASM-4863, ASM-4867)
    Then the arrears notice request is consumed from P6 rwb-comms on POST /cases/{caseId}/notices with the case reference and the notice type and no personal data
    Then the document declares no recovery_case, task or timer property and no write of a case row from rwb-asset, and no v_ace_* path or property, and the boundary test fails a build that adds one
    Then each call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access and error sections of the baseline
    When they are compared with TSD S5 T-A.1, T6.1 and the platform envelope
    Then both reads declare Asset and disposal right R with the scope applied, and no operation of this baseline declares C, U or D
    Then RW-SALEOFF holds CRUA, RW-NPAMGR and RW-ENFORCE hold CRU and every other role of TSD S5 T6.1 holds R
    Then the answers 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 are declared with one envelope and one message ID per condition
    Then a repeated request with the same Idempotency-Key describes no second effect, and neither read declares the header
    Then MSG-P7-003 is declared as the answer of the decision-record element and MSG-S5-001 and MSG-S5-002 are carried with no path that raises them

  Scenario: AC5 The decision-record element and the seven fakes answer the document, and no event is declared (new, D-RCV-60)
    Given the decision section, the fakes and the naming section of the baseline
    When each is compared with the library schema, the operation or the element it serves, and the nine sub-tables of section 12
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the rule ID, the package version, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the asset row changes, and a failed write leaves the asset unchanged with MSG-P7-003
    Then the fakes answer the case state and move, the auto-debit and its mandate reference, the notice, the ACE asset fact by business key, the DISPOSAL package, a healthy and a stopped decision chain, and the merged screen read
    Then the drift test compares every fake with the document and fails the build on any difference
    Then the schema is rwb_asset, the base is /api/recovery/asset/v1, the topic is rwb.asset.events.v1 with its retry and .dlt topics, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the owned tables are asset and the library objects decision_record and idempotency_key, and every other table and view is named as another owner's
    Then the document declares no published event, no consumed event, no second topic, no Schedule and no monolith base, and the absence tests fail a build that adds one
```

These five criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E4033-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The asset and its holding status are rwb-asset's, and the contract declares their fields, lists and required flags on the `asset` and `Rental` elements only | Architecture v5 slide 41; TSD S5 T3.1 and T3.2; ASM-4867 |
| BR2 | The decision record is declared as an element written before the asset row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S5 T2; legacy RWB-E4-033 AC1 and AC3 |
| BR3 | The ACE asset fact stays with rwb-source-data: the contract declares the read as consumed and declares no `v_ace_*` property | DP-05; Architecture v5 slide 29; GAP-2966 |
| BR4 | The case move is answered and not written: the contract declares the state read and the answer and no `recovery_case`, `task` or `timer` property | Ownership Map (P3); GAP-2966 |
| BR5 | The money stays with rwb-payment: the contract declares the mandate request and its reference and no amount, receipt, instalment or arrears state | Architecture v5 slide 41; FSD P8 A2.9; GAP-2966 |
| BR6 | This step publishes no event and consumes none: `AssetTakenOn` and `AssetSold` stay the two event names of the service and neither is declared here | Architecture v5 slide 19 OUT; Template and Rules §R4 |
| BR7 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; TSD S5 T-A.2 |
| BR8 | The vocabulary is closed: `LOV-HOLDING`, `LOV-ASSET-TYPE` and `LOV-SEGMENT` are published as enumerations, `RENTED` is one of them, and no list value is a constant of the code | TSD S5 T3.2; FSD S5 BR-S5-024 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules §R7.2 (s17) |
| BR10 | One REST base, one topic, one queue and one login per service, and the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR12 | The rule rows of R-DIS-25 and R-DIS-63 and the reference data of the lists are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; GAP-2966 |
| BR13 | ATS is an external system with no interface specification in TSD S5 T5.1: named as a system of the rule row and never declared as an operation, a topic or a fake | R-DIS-25 of Business Rules and Routing Logic v4; TSD S5 T5.1; ASM-4865 |

### 9. State transitions

The lifecycle of this document, not of an asset:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The reads, the rental element, the lists, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the harness and the four owner teams accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC5 fail | In review |
| Draft | No approval recorded | The run continues in Draft under D-RCV-60 and the missing approval is recorded | Draft |

The holding-status machine the document describes is the app story's: `LOV-HOLDING` is HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED; this baseline fixes the vocabulary and the value `RENTED` and moves no asset.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the correction of the Ownership Map rows the baseline consumes, including the missing `asset` row and the business-key path |
| Consuming teams (the app story, the two screens, the wave 3 harness and the owners of rwb-payment, rwb-case, rwb-comms, rwb-source-data, rwb-decision, rwb-access and the platform libraries) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses without redefining |
| Data steward | Confirms that no personal data field is declared in an answer, an element, a notice request or a fake |

The per-service login behind the security scheme is named "the rwb-asset login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Asset element | The columns of DF-COL-028 to DF-COL-042 as the existing asset reads declare them: `id`, `case_id`, `collateral_id`, `asset_ref`, `asset_code`, `asset_type`, `transfer_in_type`, `from_segment`, `transfer_in_date`, `book_value`, `auction_purchase_price`, `repossessed_date`, `stock_date`, `holding_status` and `holding_cost_to_date` |
| Rental element | `asset_ref` and `tenant_ref` required; `rental_start_date`, `rental_term_months`, `rent_amount`, `rent_currency`, `payment_method` and `auto_debit_ref` optional; declared additively on the Asset element and backed by no physical column set in TSD S5 T3.1 (GAP-2966; ASM-4862) |
| Lists | `LOV-HOLDING` with HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED; `LOV-ASSET-TYPE` with its six values; `LOV-SEGMENT` with its three values, published as enumerations and read at their version |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the asset row changes (DP-03) |
| ACE asset fact | DF-ACE-208 to DF-ACE-219 of `v_ace_npa_asset` in P1, read only through the owner's contract and never written, copied or joined here |
| Not declared here | `recovery_case`, `task` and `timer` (P3), `proceeds` (P8), `notice` and `template` (P6), `decision_log_entry`, `rule_row` and `approval` (P7), `listing` and `asset_sale` (this service's later stories) and every other `v_ace_*` view (P1) |
| Consumed names with no source | The operation names of the auto-debit request, the case-move answer and the rwb-source-data asset read, and the ATS interface: Not specified in the source documents (GAP-2966; ASM-4863, ASM-4865) |
| Key with no source | The read path carries the ACE asset business key while `asset` is keyed by a record identifier and carries `asset_ref` and no business-key column (GAP-2966; ASM-4867) |

The field-level types, lengths and required flags of the added rental element are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of AC1. **No new table, no new column and no migration** is declared.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated by page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetKey}` | Asset out, with its holding status and its Rental element (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |

The two operations answer 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of §14. The operation IDs are those of TSD S5 T-A.1, the paths are those of the target base, and the path parameter is the ACE asset business key of API Specification v4, re-read against the record key of TSD S5 T3.1 under ASM-4867 (GAP-2966). No operation writes the rental: the rental is a workflow step, so an operation that writes the rental terms is Not specified in the source documents (GAP-2966; ASM-4862). API-S5-003 `POST /assets/{assetId}/valuations` is rwb-valuation's under the Ownership Map ruling on the valuation operation, and API-S5-004 and API-S5-005 belong to the pricing and auction stories of this service; none of the three is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The auto-debit request (operation name Not specified in the source documents (GAP-2966; ASM-4863)) | `/api/recovery/payment/v1` | P8 rwb-payment | The mandate of the case and the asset for the rental term, answered by a mandate reference; no amount held here; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state `ROUTE_WITH_APPROVER`, its route `rental` and the case reference; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2966; ASM-4863)) | `/api/recovery/case/v1` | P3 rwb-case | The move `RENTAL_ACTIVE` with the rule ID and its version; on the workflow boundary the stage outcome the parent applies; faked |
| `POST /cases/{caseId}/notices` | `/api/recovery/comms/v1` | P6 rwb-comms | The arrears notice the legacy arrears follow-up implies, with the case reference and the notice type; faked |
| The ACE asset read (operation name Not specified in the source documents (GAP-2966; ASM-4863)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE asset business key, the asset reference, the asset type and the freshness stamp behind the asset row; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are class C dependencies in fact while the plan's C row is None, and the absence is recorded as GAP-2966 with ASM-4863.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset exactly two event names, `AssetTakenOn` and `AssetSold`, and neither is the rental: the step writes no outbox row and publishes nothing. The two names stay with RWB-S5-E3019-APP and the sale stories of this service, and this baseline names them as the catalogue's and not as an element of this step.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives the service `JudgmentRecorded`, `AuctionResult`, `ProceedsMatched` and `PartnerResultSubmitted`, and none is the rental approval, which reaches the stage as a signal from the parent `CaseWorkflow`. This baseline declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC5 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | The stage that hosts the rental step; its signals and its outcome for the parent are declared, not built |
| `rentHeldAsset` | Activity, the one rental step | `rwb-asset` | The case and the approved route in; the rule ID with its version, the asset reference, the debit reference, the notice and the case move out |

No child workflow for the case, the approval or the money exists in this service. The activity name is a target design choice and the trigger is the arrival of the approved route for a case in `ROUTE_WITH_APPROVER`, because the FSD declares no background event (FSD S5 A2.24.4.4). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the approved route and the case signal; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| asset | S5 (`rwb_asset`) | The held asset, its holding status, its fields and its lists; the table the two reads answer from and the row the rental terms extend |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated approval and the answer it holds |

`recovery_case`, `assignment`, `task` and `timer` (P3), `proceeds` (P8), `notice` and `template` (P6), `decision_log_entry`, `rule_row` and `approval` (P7), `listing` and `asset_sale` (later stories of this service) and every `v_ace_*` view (P1) are not owned here; the baseline names them only as an answer of their owner or a later story's table, and no foreign key leaves the schema (DP-01). `outbox_event` exists in the schema from the library and this baseline declares no row in it.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | The state `ROUTE_WITH_APPROVER` of case `RC-2026-000521` with route `rental`; the states `RENTAL_ACTIVE` and `ASSET_HELD`; an accepted and a refused move | AC3, AC5 |
| rwb-payment auto-debit fake | The auto-debit set for case `RC-2026-000521` with its mandate reference; a refused mandate; no answer beyond 2 s | AC3, AC5 |
| rwb-source-data asset fake | The ACE asset fact of asset `AST-2026-000521` by its business key with the freshness stamp; a stale product with its date; no answer beyond 2 s | AC3, AC5 |
| rwb-comms notice fake | The arrears notice accepted with its notice reference, and a refused request | AC3, AC4 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-25 and R-DIS-63 | AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000521`, with the asset and its rental terms read once | AC1, AC5 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the auto-debit request, the case-move answer and the rwb-source-data read carry the placeholder until their owners confirm them (GAP-2966; ASM-4863). ATS has no fake, because it has no interface specification and no operation of it is declared (BR13).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The two asset reads; the auto-debit request, the case state read and move answer, the notice request and the ACE asset read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event is declared; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `AssetDisposalWorkflow` and `rentHeldAsset` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no asset, no case, no balance and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and seven fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on any other owner's schema. DP-13 moves the base and nothing else. DP-19 sits behind SCR-21 and SCR-22, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, and the step needs none because it publishes no event (BR6).

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml`, the `Asset`, `AssetPage` and `Rental` elements, the vocabulary of the three lists as published enumerations, the contract README rows for the five consumed rows with their placeholders, and the seven WireMock mapping sets. The pattern table adds two H rows, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, which the plan's build list carries; the five consumed rows are C dependencies in fact and not in the metadata row (GAP-2966; ASM-4863).

**Build steps**

1. Write the two reads and validate the additive rule of AC1 in the pipeline.
2. Write the `Rental` element of AC2 additively on the `Asset` element, with its required flags, the three lists and the placeholder where a type is unstated.
3. Record the five consumed rows of AC3 with their owners and placeholders.
4. Record the rights and the error envelope of AC4.
5. Record the decision-record element of AC5, validate it against the library schema and publish the seven fakes with the drift test.
6. Record the naming baseline and the boundary of AC5, tag the baseline and collect the consumer sign-off.

**Done when.** The document validates in the pipeline, the four new contract tests pass, the fakes answer every consumed path and the drift test is green, the absence tests for a `v_ace_*` read, a `recovery_case` write, a published event, a consumed event, a second topic and a Schedule are green, and the app story, the two screens and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set. It names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation (VR-S5-024-1) | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the asset row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S5-001 and MSG-S5-002 are carried because they are in the message set of the feature. The freshness stamp of the rwb-source-data answer is declared as a field of the consumed row, and the stale-data check and its message belong to the owner of the data product.

### 15. Screens and states

The contract serves SCR-21 Asset list (loading, list) and SCR-22 Asset record (take-on, held, listed, sold) through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its holding status and its rental terms, rwb-case for the case and its route state, rwb-source-data for the ACE asset fact, rwb-valuation for the valuation references and rwb-payment for the debit; this baseline fixes the rwb-asset answers only, and the route specification and the field list belong to RWB-PLT-N001-CON.

The legacy screen table names four states of SCR-22 and no rented state, while `LOV-HOLDING` carries `RENTED`: the baseline declares the value and leaves the rendering to the screen owner, and the difference is recorded (GAP-2966; ASM-4869). The refusal, not-recorded and invalid states of the app story read the messages of §14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-033-01 | AC2, AC5 | Contract | The rental element and the decision-record element of case `RC-2026-000521`; the contract half answers the element, its lists and the record shape |
| TC-E4-033-02 | AC2, AC3 | Contract | Case `RC-2026-000521` at `ROUTE_WITH_APPROVER` with route `rental`; the contract half answers the rental element, the mandate reference and the `RENTAL_ACTIVE` move shape |
| TC-E4-033-03 | AC4, AC5 | Contract | A stopped decision-record chain; the contract half answers the MSG-P7-003 path and the record element |
| TC-E4-033-04 | AC4 | Contract | A role without the Asset and disposal right; the contract half answers the 403 with MSG-P4-002 and the rights of the two reads |
| TC-E4-033-05 | AC4, AC5 | Contract | A malformed request and an absent required term; the contract half answers the 400 and the 422 of the envelope, and the absence tests |
| TC-S5-E4033-CON-01 | AC1 | Contract | The document validates; the base, the two operations, the filters and the additive rule are present, and a removed or renamed property fails |
| TC-S5-E4033-CON-02 | AC2 | Contract | The `Rental` element validates with its eight properties, its two required flags and the three closed lists, and `RENTED` is accepted |
| TC-S5-E4033-CON-03 | AC3 | Contract | The five consumed rows with their placeholders; the no-`v_ace_*` and no-`recovery_case` boundary; the 2 s budget and the breaker |
| TC-S5-E4033-CON-04 | AC4, AC5 | Contract | The rights and the six message answers; the seven fakes match the document and a drifted fake fails the build; the no-event, no-second-topic and no-Schedule absence tests |

The five legacy cases are the legacy cases of RWB-E4-033 in their legacy order, carried as the contract half: their Covers column names the criterion that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E4033-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S5-E4033-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the route condition, the states, the `RENTED` value, the term limits and the arrears value stay data, reference data or the rule package, never a schema default or a branch of the code.
- No personal data in a schema, an example, a notice request or a fake: identifiers, codes, amounts, dates and a rule version only; the tenant reference is an identifier of the arrangement and every example is synthetic.
- ACE data only through the owner's contract or the `v_ace_*` views: the document declares no `v_ace_*` path, no `v_ace_*` property, no case row write and no ACE table read (BR3, BR4).
- The money stays with rwb-payment: the document declares a mandate request and its reference and no posting, balance, instalment, receipt or arrears state (BR5).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No event is published or consumed by this step and no third event name is added to the service; the absence tests fail a build that declares one (BR6).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element and no invented interface is reintroduced: no monolith base, no Quartz row, no shared job table, no Schedule and no ATS operation without a specification (ASM-4865).
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S5-010 | A transfer to the asset management company, a buy-back and a rental each follow a recorded approval (FSD S5 requirements served; Business Requirements Program v4; BR-030 of Epics 3 to 8 BRD v1); the split plan carries no requirement id for this slice (GAP-2966; ASM-4866) | The `Rental` element, the two reads and the five consumed rows | TC-E4-033-01, TC-E4-033-02, TC-S5-E4033-CON-01, TC-S5-E4033-CON-02 |
| ADR-014 | Schema and login per service | `rwb_asset`, the rwb-asset login and no foreign schema | TC-S5-E4033-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-S5-E4033-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the change | TC-S5-E4033-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-033, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S5-E4033-APP; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the four new contract cases TC-S5-E4033-CON-01 to -04 |
| Feature and screens | FEAT-AST-24, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-25 from the Business Rules and Routing Logic v4, governed in rwb-decision; R-DIS-63 named as the later tenant-default step |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the two reads, the R-DIS-25 evaluation, the decision record, the rental terms, the holding status, the mandate and notice requests and the move answer: RWB-S5-E4033-APP.
- The case of record, its route states, `task`, `timer` and `assignment`, the parent `CaseWorkflow` and the move operation name: rwb-case (P3) (GAP-2966); the approval path, the rule package, the rule rows and the decision ledger: rwb-decision (P7).
- The auto-debit, the receipt, the instalments, the arrears follow-up and the rental_arrears value: rwb-payment (P8) under FEAT-PAY-09 (GAP-2966); the arrears notice, its template and its delivery: rwb-comms (P6).
- The ACE NPA asset, customer and account facts and the freshness of the data product: rwb-source-data (P1) (ASM-4867).
- ATS and its interface: an external system with no specification in TSD S5 T5.1, tracked and not declared here (ASM-4865).
- The correction of the Ownership Map rows the baseline consumes, including the missing `asset` row and the business-key path: the solution architect (GAP-2966; ASM-4867).
- The holding-age clock, the provision steps and the monthly cost of carry: RWB-S5-E3023-APP; the return of the asset to the holding on a tenant default (R-DIS-63): a later step of this service.
- The deed in lieu buy-back rental of the customer's own asset: rwb-treatment (S2) and rwb-payment (P8), a different route set (R-DIL-32, R-DIL-34).
- The listing, the floor price and the auction rounds: the pricing and auction stories of this service (API-S5-004, API-S5-005).
- The gateway-bff composite route and the field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories; the cross-service journey: the wave 3 harness; the deployment, its flag and its runbook: the operations story of this legacy key.
