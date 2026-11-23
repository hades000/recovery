# RWB-S5-E3025-CON Maintain a held property - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3025-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the held-property step of rwb-asset, split from RWB-E3-025. It fixes the asset read and the cost write on `/api/recovery/asset/v1` (DP-13), the cost element and its closed list, the work-order instruction towards rwb-partner, the case-move answer of rwb-case, the consumed rwb-source-data data-product row, the decision-record element of DP-03, the fakes and the absence tests. DP-09 is not in the pattern set of this key although the step writes an outbox row, and the plan gives no C row although the step cannot run without three published contracts (GAP-2862, GAP-2863, GAP-2867, GAP-2868; ASM-4747, ASM-4750, ASM-4752, ASM-4753, ASM-4755). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the held-property step of rwb-asset — the asset read and the cost write on `/api/recovery/asset/v1`, the cost element with its closed list, the work-order instruction, the case-move answer, the consumed rwb-source-data row, the decision-record element, the tables and the fakes**, so that **the app story, the two screens and the wave 2 harness build against one fixed, testable contract on Day 1 and a cost field, a list value, an instruction property or an answer shape can never drift between rwb-asset, rwb-source-data, rwb-case and rwb-partner without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy held-property step crossed four boundaries at once: the officer screen, the ACE asset fact read through `v_ace_npa_asset`, the decision log and the case state. The target splits them: rwb-source-data owns the ACE asset fact, rwb-case owns the case and its route states, rwb-partner owns the vendor and the portal instruction, rwb-decision governs the DISPOSAL rules, and rwb-asset owns the asset record, the cost and the decision record. Each boundary is a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset` (Template and Rules §R4; _work/msr/context/S5.md). It records that the step publishes no event, because the catalogue gives the service EV-22 only and EV-22 is the take-on step's.

Four points are carried as gaps and assumptions rather than decided quietly: no source names the cost operation, its element, its closed list or its answer (GAP-2862, GAP-2867; ASM-4747, ASM-4748), no source names the vendor instruction or the partner operation (GAP-2863; ASM-4750), the legacy AC2 and the FSD attach the bid-in-round rule R-DIS-37 to a cost feature (GAP-2864; ASM-4751), and the connection matrix shows subscribes cells that no source names while the plan carries no C row (GAP-2868; ASM-4755).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `asset_sale` and `listing` are S5's, `recovery_case` and `timer` are P3's, `document` is P5's, `proceeds` is P8's, `partner_instruction` is S9's, `decision_log_entry` and `rule_row` are P7's. This document declares no other service's table or operation as its own.
- The rwb-source-data data-product contract of DP06 Collateral and assets, the rwb-case state and move answer and the rwb-partner instruction contract are published with their fakes, so the consumed rows name a real owner document; they are not in the contract-dependency row, which is None, and the absence is recorded (GAP-2862, GAP-2863, GAP-2868).
- The outbox and inbox library `RWB-PLT-TE006-CON` of DP-09 is the platform dependency of the outbox row the step writes; the pattern set of this key does not carry DP-09, and this baseline keeps the metadata row as the plan states it (GAP-2868; ASM-4755).
- The DISPOSAL package and its rows for R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `asset` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive OpenAPI 3.1 document of rwb-asset for this step: the asset read with its request and answer, the cost write with its element, its rights and its error responses.
2. Fix the cost element: its properties, their types, their required flags, and the closed list of the kind.
3. Declare the consumed rows: the rwb-source-data data-product read with its freshness stamp, the rwb-case state read and move answer, and the rwb-partner instruction with its answer, marking with the placeholder every field no source gives.
4. Record the work-order element and its lifecycle keys as the partner instruction's data, and the durable timer of R-DIS-11 as the workflow's, not the document's.
5. Record the decision-record element of DP-03, written before the asset row changes.
6. Record the closed vocabulary, the naming baseline and the rule that no list value is a constant of the code.
7. Publish the contract tables of section 12 and the six fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the absence of a published event, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-S5-E3025-APP, the two screens and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or a response body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake derives from the published document | None | AC3, AC4 |
| X5 | A kind outside the closed list, or a list value used as a code constant, appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view or a `recovery_case` row | The boundary test fails the build and the review fails the baseline | None | AC7 |
| X7 | The document declares a published event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation are not the ones the permission table declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-source-data, rwb-case and rwb-partner only |
| Negotiable | The element names, the example values and the fake fixtures are settled in the baseline review; the operations, the list, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S5-E3025-APP, the two screens and the wave 2 harness on Day 1, and the rwb-partner and rwb-case teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, six fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the held-property step of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of asset_sale and listing is S5, of recovery_case and timer is P3, of partner_instruction is S9 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The asset read and the cost write are declared on the asset base with their shapes and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /assets/{assetId} with an Asset answer of status 200 and the cost write on the same asset path with a HoldingCost request and an Asset answer of status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then the read declares the path parameter assetId, and the write declares the path parameter assetId and the Idempotency-Key header
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then the change is additive within major version 1, and a removed or renamed property fails the contract test

  Scenario: AC2 The cost element and its closed list are fixed (new, D-RCV-60)
    Given the HoldingCost element of the baseline
    When it is compared with TSD S5 T3.1, T3.2 and the legacy sentence of RWB-E3-025 AC1
    Then HoldingCost declares the kind, the amount, the currency, the invoice date, the vendor reference and the work-order reference of the cost
    Then kind is declared against the closed list LOV-HOLDING-COST with the values MAINTENANCE, INSURANCE and CUSTODY, published as a reference-data enumeration and never as a code constant
    Then amount and kind are required and the other four properties are optional, and the amount is declared with two decimals and a currency
    Then no property is added for a document, a photograph, a bank account, a payee or a posting step, and those facts are referenced as documents and payments of their owners
    Then the response Asset element carries holding_status of LOV-HOLDING with the value HELD and holding_cost_to_date of DF-COL-042, and no other asset property is redefined by this baseline

  Scenario: AC3 The work-order instruction and the case-move answer are declared against their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with rwb-partner as the owner of partner_instruction and rwb-case as the owner of recovery_case, and with the Business Rules and Routing Logic v4 rows R-DIS-10, R-DIS-11 and R-DIS-12
    Then the work order is declared as a partner instruction consumed from S9 rwb-partner, with the case reference, the asset reference, the vendor, the instruction type, the requested scope and the invoice, and with the answer accepted, refused or pending
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state and the move WORK_ORDER_OPEN, ASSET_HELD or BID_RECEIVED carrying the rule ID and its version
    Then the operation names of the instruction and of the case-move answer are Not specified in the source documents (GAP-2862, GAP-2863; ASM-4750, ASM-4753) and the rows carry the placeholder
    Then the document declares no partner_instruction property, no recovery_case property, no case row write and no vendor row write from rwb-asset
    Then the instruction is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The consumed rwb-source-data row is declared and the ACE fact stays there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the rwb-source-data data-product contract and the naming rules of the context pack
    Then the read of DP06 Collateral and assets is declared as consumed from P1 rwb-source-data, with the asset reference, asset code, asset type, transfer-in type, segment, book value, repossessed date and the freshness stamp of the data product
    Then the operation name of the row is Not specified in the source documents (GAP-2862; ASM-4747) and the row carries the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property and no grant on any rwb_* schema of another owner, and the boundary test fails a build that adds one
    Then the call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The rights, the idempotency rule and the error envelope are fixed (new, D-RCV-60)
    Given the access sections of the baseline
    When they are compared with the legacy permission table of RWB-E3-025 and with TSD S5 T6.1
    Then the read declares Asset and disposal right R and the write declares right C with the scope applied
    Then RW-ENFORCE, RW-SALEOFF, RW-NPAMGR and SY-DATALOAD hold C with the scope, and every other role of TSD S5 T6.1 holds R only
    Then a repeated write with the same Idempotency-Key describes no second cost, no second instruction and no second case move, and the read declares no header
    Then the seven answers of AC1 each carry one message ID of section 14, and 403 carries MSG-P4-002 and 422 carries MSG-GEN-001

  Scenario: AC6 The decision-record element and the six fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the rule ID, the package version in force, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the asset row changes, and a failed write leaves the asset unchanged with MSG-P7-003
    Then the rwb-source-data fake answers the ACE asset fact of asset "AST-2026-000512" for case "RC-2026-000512" with its freshness stamp, a stale product and no answer beyond 2 s
    Then the rwb-case fake answers the states ASSET_HELD, WORK_ORDER_OPEN and ROUND_OPEN, an accepted move and a refused move, and the rwb-partner fake answers the work order accepted, refused and pending and a bid reported on the open round
    Then the rwb-decision fake answers the DISPOSAL package at its version with R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37, and the decision-record stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is published (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the tables named as owned are asset and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, document, proceeds, partner_instruction, decision_log_entry, rule_row, listing, asset_sale and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the baseline declares no published event, no consumed event, no second topic and no Schedule, because the catalogue gives the service EV-22 only and that event is the take-on step's (GAP-2868; ASM-4755)
    Then the absence test fails a build that adds an event, a second topic or a Schedule, and the review records the outbox library row as an absent H dependency
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E3025-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The asset and its holding cost are rwb-asset's, and the contract declares their fields and required flags on the Asset element and on the cost element only | TSD S5 T3.1 and T3.2; _work/msr/context/S5.md |
| BR2 | The decision record is declared as an element written before the asset row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S5 T2; legacy AC1 and AC3 |
| BR3 | The ACE asset, collateral and score facts stay with rwb-source-data: the contract declares the data-product read as consumed, no `v_ace_*` property and no ACE table read of rwb-asset | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2862 |
| BR4 | The case move is answered and not written, and the work order leaves as a partner instruction: the contract declares both as consumed and declares no `recovery_case` property and no vendor row | Business Rules and Routing Logic v4 rows R-DIS-10 to R-DIS-12; GAP-2863 |
| BR5 | The cost kind is a closed list of three values published as reference data; no kind, amount, threshold, vendor or term is a schema default or a code constant | BR-S5-007; FSD S5 A2.7.3.1; GAP-2867; ASM-4748 |
| BR6 | A write declares the `Idempotency-Key` and stores its answer; a read declares none | Architecture v5 slide 11; TSD S5 T-A.2 |
| BR7 | The baseline declares one REST base, one topic, one queue and one login, and never another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR8 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules §R7.2 (s17) |
| BR10 | The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR11 | The rule rows of R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37 and the reference data of the lists are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; GAP-2864; ASM-4751 |

### 9. State transitions

The lifecycle of this document, not of an asset:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The read, the write, the element, the list, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 2 harness and the rwb-source-data, rwb-case and rwb-partner owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new optional cost field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC4 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a published event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's: R-DIS-10 moves `ASSET_HELD` to `WORK_ORDER_OPEN`, R-DIS-11 returns it to `ASSET_HELD` and R-DIS-12 keeps it open, and this baseline fixes the move names and the answer shapes and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows this baseline consumes |
| Consuming teams (the app story, the two screens, the wave 2 harness and the owners of rwb-source-data, rwb-case, rwb-partner, rwb-decision, rwb-access and rwb-payment) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library, the partner instruction kit and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-asset login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Asset element and its answer | The read answers from `asset`: DF-COL-028 to DF-COL-042, with `holding_status` of `LOV-HOLDING` and `holding_cost_to_date` of DF-COL-042 carrying the cost |
| Cost element | The kind of `LOV-HOLDING-COST`, the amount, the currency, the invoice date, the vendor reference and the work-order reference; the kind and the amount required (GAP-2867; ASM-4748, ASM-4749) |
| Work-order instruction | The case reference, the asset reference, the vendor, the instruction type, the requested scope and the invoice, with the accepted, refused and pending answer (GAP-2863; ASM-4750) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the asset row changes (DP-03) |
| ACE asset fact | DF-ACE-208 to DF-ACE-219 of `v_ace_npa_asset` and the collateral and score facts in P1, read only through the owner's data product and never written, copied or joined here |
| Not declared here | `recovery_case` and `timer` (P3), `document` and the custody of documents (P5), `proceeds` (P8), `partner_instruction` (S9), `decision_log_entry` and `rule_row` (P7), `listing` and `asset_sale` (S5, the pricing and auction stories') |
| Consumed fields with no source | The operation names of the three consumed rows and the cost element name: Not specified in the source documents (GAP-2862, GAP-2863, GAP-2867; ASM-4747, ASM-4750) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the closed list of AC2 and the optionality rule of BR8. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets/{assetId}` | Asset of status 200 out, with its holding status, holding cost to date, valuations, costs and listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |
| POST | The cost write, operation name Not specified in the source documents (GAP-2862; ASM-4747) | HoldingCost in, Asset of status 200 out with the new `holding_cost_to_date` and the work-order reference | Asset and disposal, right C, scope applied | `Idempotency-Key` required |

The two operations answer 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The operation IDs of the read are those of TSD S5 T-A.1 and its path is the target base, not the monolith form. API-S5-001, API-S5-003, API-S5-004 and API-S5-005 belong to the stock, valuation, pricing and round steps of this service, and API-S5-003 is rwb-valuation's under ASM-0043; none of the four is declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2862; ASM-4747)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE asset fact of the case with its freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the case reference of the step; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2862; ASM-4753)) | rwb-case (P3) | P3 rwb-case | The move `WORK_ORDER_OPEN`, `ASSET_HELD` or `BID_RECEIVED` with the rule ID and its version; faked |
| The work-order instruction and its answer (operation name Not specified in the source documents (GAP-2863; ASM-4750)) | rwb-partner (S9), through the partner gateway | S9 rwb-partner | The partner instruction to the property services vendor and its accepted, refused or pending answer; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are class C in fact while the plan's C row is empty, and the absence is recorded (GAP-2862, GAP-2863).

#### 12.3 Events published

None. Architecture v5 and the context pack give the service EV-22 `AssetTakenOn`, which the take-on step publishes, and no catalogue event covers a holding cost or a work-order state; this baseline therefore declares no published event and the absence test of AC7 fails a build that adds one (GAP-2868; ASM-4755).

#### 12.4 Events consumed

None declared by this step. The S5 row of the connection matrix shows subscribes cells towards S4, S9 and P8, and no source names the events or their data for a held-property cost, so this baseline declares no consumer group, no subscription and no inbox of its own, and the vendor answer arrives on the partner instruction of 12.2 (GAP-2868; ASM-4755).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | The stage that hosts the held-property step; its signals, its durable timer and its outcome for the parent are declared, not built |
| `recordHoldingCost` | Activity (design name), the cost step | `rwb-asset` | The cost element and the rule ID with its package version in; the asset update, the decision record and the instruction out |
| `raiseWorkOrder` | Activity (design name) through the L3 partner instruction kit | `rwb-asset` | The partner instruction of 12.2 and its answer; the 3-working-day timer of R-DIS-11 |

The two activity names are design names with no source (GAP-2863). No child workflow for the case and none for the money exists in this service, and no activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the officer action and from the vendor answer, the FSD S5 A2.7.4.4 declares no background event, and this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `asset` | S5 (`rwb_asset`) | The held asset, its `holding_status` and its `holding_cost_to_date`; the table the two operations answer from |
| `decision_record` | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| `idempotency_key` | PLT library, created in `rwb_asset` | The key of a repeated cost request and the answer it holds |
| `outbox_event` | PLT library, created in `rwb_asset` | The relay row of the step's transaction (DP-09) |

`recovery_case` and `timer` (P3), `document` (P5), `proceeds` (P8), `partner_instruction` (S9), `decision_log_entry` and `rule_row` (P7), `listing` and `asset_sale` (S5, later stories') and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The ACE asset fact of asset `AST-2026-000512` for case `RC-2026-000512` with its collateral, segment, book value and freshness stamp; a stale product; no answer beyond 2 s; an unreadable answer | AC4, AC6 |
| rwb-case state and move fake | The states `ASSET_HELD`, `WORK_ORDER_OPEN` and `ROUND_OPEN` of case `RC-2026-000512`; an accepted move and a refused move | AC3, AC5, AC6 |
| rwb-partner instruction fake | The work order accepted with its instruction reference, refused, and still pending; a bid reported on the open round | AC3, AC6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37; a package out of force | AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000512` | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The cost element, the vendor instruction and the operation names are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2862, GAP-2863, GAP-2867; ASM-4747, ASM-4750).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The asset read and the cost write on `/api/recovery/asset/v1`; the rwb-source-data data-product read, the rwb-case state read, the case-move answer and the rwb-partner instruction; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `AssetDisposalWorkflow`, `recordHoldingCost` and `raiseWorkOrder` on `rwb-asset`; one durable timer; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no asset, no case, no invoice and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment, nine contract tables and six fakes.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml`, the `Asset`, `AssetPage` and `HoldingCost` elements, the closed list of the cost kind as a published enumeration, the contract README rows for the four consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/asset/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on any other owner's schema, because rwb-asset holds none (GAP-2862; ASM-4752). DP-13 moves the base and nothing else. DP-19 is behind SCR-21 and SCR-22, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, which is why the outbox library is recorded as an absent H row rather than declared (GAP-2868; ASM-4755).

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON` that the plan's build list for this key already carries, and it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the outbox row needs. The four consumed rows are C dependencies in fact and not in the metadata row (GAP-2862, GAP-2863, GAP-2868).

**Build steps**

1. Write the read and the write and validate the additive rule of AC1 in the pipeline.
2. Write the `HoldingCost` element, its six properties and its closed list of AC2.
3. Record the instruction and the case-move rows of AC3 with their owners, their budget and their placeholders.
4. Record the consumed rwb-source-data row of AC4 with its freshness stamp and its placeholder.
5. Record the rights, the `Idempotency-Key` rule and the error envelope of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema, then publish the six fakes and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the five new contract tests pass, the fakes answer every consumed path, the drift test is green, and the app story, the two screens and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it (GAP-2865) | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it (GAP-2865) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the asset row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added. The two price messages are carried because they are in the message set of this feature, and the surfaces that raise them belong to the pricing and re-appraisal stories (GAP-2865).

### 15. Screens and states

The contract serves SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its take-on, held, listed and sold states, all through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its holding status and its cost to date, rwb-case for the case and its route state, rwb-source-data for the ACE asset fact and rwb-partner for the vendor and the instruction; this baseline fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to `RWB-PLT-N001-CON`. The refusal, not-recorded and stale-data states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-025-01 | AC1, AC2 | Contract | Held asset `AST-2026-000512` of case `RC-2026-000512`; the contract half answers the read, the write, the cost element and its closed list |
| TC-E3-025-02 | AC1, AC3 | Contract | A bid reported on the open round of `RC-2026-000512`; the contract half answers the round outcome and the `BID_RECEIVED` move shape |
| TC-E3-025-03 | AC1, AC6 | Contract | The policy and the routing instances of the DISPOSAL package; the contract half answers the rule inputs and the decision-record element |
| TC-E3-025-04 | AC5 | Contract | A role without the Asset and disposal right and a malformed body; the contract half answers the 403 with MSG-P4-002 and the 422 of the envelope |
| TC-E3-025-05 | AC6, AC7 | Contract | The decision-record stub stopped and a stale data product; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S5-E3025-CON-01 | AC1 | Contract | The document validates; the read, the write, the base, the path parameters and the seven error answers are present |
| TC-S5-E3025-CON-02 | AC2 | Contract | The `HoldingCost` element validates with its six properties, its two required flags and the closed list of three values |
| TC-S5-E3025-CON-03 | AC3, AC4 | Contract | The four consumed rows and their placeholders; the instruction answer and the case-move answer match the document |
| TC-S5-E3025-CON-04 | AC5, AC6, AC7 | Contract | The rights of the two operations, the `Idempotency-Key` rule, the six fakes and the drift test, the no-publication, no-`v_ace_*` and no-`recovery_case` boundaries |

The five legacy cases are the legacy cases of RWB-E3-025 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E3025-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S5-E3025-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the cost kinds, the three-day term, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; every example is synthetic.
- The ACE asset fact stays with rwb-source-data and the case with rwb-case: the document declares no `v_ace_*` path, no `recovery_case` property, no case row write and no ACE table read (BR3, BR4).
- The money stays with rwb-payment and the vendor with rwb-partner: the document declares no posting, no balance, no bank account, no payee and no vendor row.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No element without a catalogue row: an event, a second topic or a Schedule fails the absence test of AC7.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the partner instruction kit come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| FEAT-AST-07 (requirement id Not specified in the source documents (GAP-2866; ASM-4756)) | Records maintenance, insurance and custody costs against the asset; the contract fixes the element, the list and the consumed rows on which the record is built (FSD S5 A2.7; Epics 3 to 8 Specification v3) | The `HoldingCost` element, the closed list and the four consumed rows | TC-E3-025-01, TC-S5-E3025-CON-01, TC-S5-E3025-CON-02 |
| BR-S5-007 | No value a business person may change is written in code | The closed list as a published enumeration | TC-S5-E3025-CON-02 |
| R-DIS-10, R-DIS-11, R-DIS-12 | The work order to the property services vendor, its acceptance and its refusal | The instruction element and the case-move answer | TC-S5-E3025-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S5-E3025-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-025, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S5-E3025-APP; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the four new contract cases TC-S5-E3025-CON-01 to -04 |
| Feature and screens | FEAT-AST-07, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-019, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the read and the write, the evaluation of R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37, the decision record, the `asset` row and the case move: RWB-S5-E3025-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked.
- The ACE NPA asset, collateral and score facts and the freshness of the data product: rwb-source-data (P1).
- The vendor, its fee schedule, the portal and the partner instruction itself: rwb-partner (S9) and the partner gateway.
- The holding-age clock, the provision steps and the monthly cost of carry: the holding stories of this service, with the posting in rwb-payment (P8).
- The valuations of the asset: rwb-valuation (S1) under API-S5-003 and ASM-0043.
- The listing, the floor price and the auction rounds: the pricing and auction stories of this service, API-S5-004 and API-S5-005.
- The custody of the documents themselves: rwb-document (P5).
- The authoring, testing, approval and versioning of the DISPOSAL package and of the four rule rows: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: `RWB-PLT-N001-CON` and the edge stories.
- The event catalogue change that a later reporting need may require: the platform event stories, not this baseline.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
