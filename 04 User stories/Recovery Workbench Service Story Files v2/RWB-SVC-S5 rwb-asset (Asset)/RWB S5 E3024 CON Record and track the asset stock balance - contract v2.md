# RWB-S5-E3024-CON Record and track the asset stock balance - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3024-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Contract version | v1 (base `/api/recovery/asset/v1`) |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | Three consumed rows of section 12: rwb-source-data data-product read, rwb-case state and move rows, rwb-access role matrix (GAP-2861) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the asset stock balance of rwb-asset, split from RWB-E3-024. It fixes the two reads on `/api/recovery/asset/v1` (DP-13) with the `AssetStockBalance` element, the confirmation operation and its `StockBalanceConfirmation` request, the owner-role and as-at fields, the consumed rwb-source-data and rwb-case rows, the decision-record element of DP-03, the tables, the fakes and the absence tests. The confirmation has no operation in any source and the figure has no object in the TSD, so both are carried as placeholders with their assumptions (GAP-2861; ASM-4743). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3024-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 16 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the asset stock balance of rwb-asset — the two reads on `/api/recovery/asset/v1`, the `AssetStockBalance` element with its owner and as-at fields, the confirmation request and answer, the consumed rwb-source-data and rwb-case rows, the decision-record element, the tables and the fakes**, so that **the app story, the two screens, the reporting reader and the wave 2 harness build against one fixed, testable contract on Day 1 and a count, a total, an owner role, a list value or an answer shape can never drift between rwb-asset, rwb-source-data, rwb-case and rwb-access without a failing build**.

This is the contract slice of legacy RWB-E3-024. It owns the surface and nothing behind it: the three operations, the two elements, the closed vocabulary, the consumed rows, the error set, the fakes and the absence tests. It owns none of the legacy criteria, which stay word for word with RWB-S5-E3024-APP, and it writes no code, no migration and no table. The empty, error and no-access states of SCR-21, and the empty, loading, error and no-access states of SCR-22, are not declared by this contract: Not specified in the source documents (DOR-RWB-S5-E3024-CON-10).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy feature of RWB-E3-024 read the ACE NPA asset, the ACE account and the case across the `recovery` schema in one query, with the stock balance owned by no one. The target splits the boundaries: rwb-source-data owns the ACE asset and account facts, rwb-case owns the case and its route states, rwb-access owns the role matrix, and rwb-asset owns the `asset` rows and the balance computed from them. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the balance element and its grouping, the vocabulary of `LOV-HOLDING`, `LOV-SEGMENT`, `LOV-ASSET-TYPE` and `LOV-TRANSFER-IN`, the confirmation request, the fact the rwb-source-data contract answers, the case state of rwb-case, the owner role of the access matrix and the record of the decision.

The baseline also fixes the naming the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset` (Architecture v5 slide 19 notes). It records that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition and the ACE fact is consumed on the owner's contract only.

Three points are carried as gaps and assumptions rather than decided quietly: no source names a write operation for the confirmation, so its path is a placeholder (GAP-2861; ASM-4743); no source says which figure the number is, so the count with the two totals is the default (GAP-2861; ASM-4744); and the TSD declares no balance object, so the figure is a computed answer and not a table (GAP-2861; ASM-4745).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the element names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `listing` and `asset_sale` are S5's, `recovery_case` and `assignment` are P3's, `proceeds` is P8's, `document` is P5's, `decision_log_entry` and `rule_row` are P7's. This document never declares another service's table or operation as its own, and it records that `asset` has no Ownership Map row while Architecture v5 slides 19 and 41 and TSD S5 T3.1 give it to S5 (GAP-2861; ASM-4745).
- The rwb-source-data data-product contract of DP06 Collateral and assets and the rwb-case state row are published with their fakes, so the consumed rows name a real owner document; they are not in this story's contract-dependency row, which is None (GAP-2861; ASM-4746).
- The rwb-access role matrix publishes the role codes RW-NPAMGR and RW-HEADNPA with their Asset and disposal rights and scopes, so the owner field of the answer resolves to a role and never to a person (GAP-2861; ASM-4744).
- The DISPOSAL rule package and its rule rows for R-DIS-01, R-DIS-02 and R-DIS-03 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `asset` and `listing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this feature: the two reads with their filters, rights and error responses, and the confirmation with its request, its answer and its idempotency.
2. Fix the `AssetStockBalance` element: the figure is the count of `asset` rows with the book-value total and the holding-cost-to-date total per `holding_status`, for a scope of `LOV-SEGMENT` and an as-at date, computed from `rwb_asset` and stored in no table; the owner role code and its scope are Not specified in the source documents (GAP-2860); with the record reference and the package version.
3. Fix the `StockBalanceConfirmation` request: the scope, the as-at date and the officer reference, with its required flags.
4. Fix the consumed rows: the rwb-source-data data-product read with its freshness stamp, and the rwb-case state and move rows, marking every field the sources do not give with the placeholder.
5. Record the decision-record element of DP-03, written before the figure is confirmed.
6. Record the closed vocabulary of the four lists, the naming baseline and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read, of a `recovery_case` write and of a balance table, the drift between a fake and the document, and the absence of an event.
9. Tag the baseline and hand it to RWB-S5-E3024-APP, the two screens, the reporting reader and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or a response body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC3 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | A consumed row or a designed element has fields the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-HOLDING`, `LOV-SEGMENT`, `LOV-ASSET-TYPE` or `LOV-TRANSFER-IN` appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` or `assignment` property, a `rule_row` or a balance table | The review fails the baseline; the boundary test fails the build | None | AC5 |
| X7 | The document declares an event, a second topic or a Schedule | The absence test fails the build | None | AC5 |
| X8 | The rights of an operation are not the ones TSD S5 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published contracts of rwb-source-data, rwb-case and rwb-access only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S5-E3024-APP, the two screens, the reporting reader and the wave 2 harness on Day 1 |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the asset stock balance of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing and asset_sale is S5, of recovery_case and assignment is P3, of decision_log_entry and rule_row is P7 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two asset reads are declared on the asset base with their shapes and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /assets with an AssetPage answer of status 200 that carries the AssetStockBalance element, and GET /assets/{assetId} with an Asset answer of status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then the list declares the filters type, status, region, page and size, and the single read declares the path parameter assetId
    Then the answers 400, 401, 403, 404, 422 and 503 are declared with one envelope and one message ID per condition, and neither read declares an Idempotency-Key
    Then no other asset operation of the monolith base is declared provided, and POST /assets/{assetId}/valuations, POST /assets/{assetId}/listings and POST /listings/{listingId}/rounds are named as other owners' and not declared here

  Scenario: AC2 The balance element, its owner and its closed lists are fixed (new, D-RCV-60)
    Given the balance section of the baseline
    When it is compared with TSD S5 T3.1 and T3.2 and FSD S5 A2.6.3
    Then the AssetStockBalance element declares the scope, the as-at date, the owner role, the per-holding_status count, the book-value total, the holding-cost total, the record reference and the rule ID with its version
    Then holding_status is declared against LOV-HOLDING with the values HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED, and the scope is declared against LOV-SEGMENT with the values RETAIL, SSME and CORPORATE
    Then the asset fields the balance shows are declared against LOV-ASSET-TYPE and LOV-TRANSFER-IN with the values of TSD S5 T3.2
    Then the owner is a role code of the rwb-access matrix and the element declares no person name, no user identifier, no address and no contact value
    Then the element declares no stored balance table and no second figure that could differ from the count and the two totals

  Scenario: AC3 The confirmation is declared with its request, its rights and its placeholder path (new, D-RCV-60)
    Given the confirmation section of the baseline
    When it is compared with TSD S5 T-A.1, TSD S5 T6.1 and FSD S5 A2.6.2
    Then one confirmation operation is declared on rwb-asset as a POST, with the StockBalanceConfirmation request and the AssetStockBalance answer carrying the record reference
    Then its path is Not specified in the source documents (GAP-2861; ASM-4743) and the row carries the placeholder
    Then the request declares the scope, the as-at date and the officer reference as required, and no amount, price or approval limit as a default
    Then the operation declares Asset and disposal right C with the scope applied, RW-NPAMGR holding CRU and RW-HEADNPA holding RA as TSD S5 T6.1 gives them
    Then the operation declares the Idempotency-Key header and describes one record and one answer for a repeated key, and the answers 400, 401, 403, 404, 409, 422 and 503
    Then no figure of the answer is a business value of the document: the count and the totals are described as computed from the asset rows

  Scenario: AC4 The consumed rows and the rights are declared and the ACE fact stays with rwb-source-data (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with the rwb-source-data data product, rwb-case and Architecture v5 slides 13, 29, 37 and 45
    Then the read of DP06 Collateral and assets is declared as consumed from P1 rwb-source-data with the asset reference, asset code, asset type, transfer-in type, segment, taken-on date, book value and the freshness stamp
    Then the operation name of that row is Not specified in the source documents (GAP-2861; ASM-4746) and the row carries the placeholder
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, and the document declares no recovery_case property, no assignment property and no write of a case row from rwb-asset
    Then the document declares no v_ace_* path, no v_ace_* property and no grant on any rwb_* schema of another owner, and the boundary test fails a build that adds one
    Then each consumed call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The decision-record element, the seven fakes, the naming baseline and the absence tests are fixed (new, D-RCV-60)
    Given the decision section, the fakes and the naming section of the baseline
    When the nine sub-tables of section 12 are reviewed
    Then one decision record is declared per confirmed figure with the scope, the as-at date, the count, the two totals, the owner role, the rule ID, the package version in force, the inputs reference, the outcome and the decided-at time, written before the figure is confirmed
    Then the rwb-source-data fake answers the ACE asset fact of "AST-2026-000524" with its dates and book value, a stale product with its date and no answer beyond 2 s
    Then the rwb-case fake answers the states ASSET_PENDING_TAKE_ON, ASSET_ON_BOOKS and ASSET_HELD and an accepted and a refused move, and the rwb-access fake answers RW-NPAMGR, RW-HEADNPA and a role without the right
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff route fake answers the merged SCR-21 and SCR-22 answer
    Then the drift test compares every fake with the document and fails the build on any difference
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the document declares no event, no second topic, no Schedule and no balance table, and the absence test fails a build that adds one
```

These five criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E3024-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

```gherkin
Scenario: AC6 The balance and the decision record are declared as the contract requires (new, D-RCV-60)
    Given the baseline document
    Then the balance is declared as a computed element of rwb-asset's own asset rows only, with the scope and the as-at date
    And the decision record is declared as an element written before the figure is confirmed, and a failed write changes nothing

Scenario: AC7 The consumed and answered parts are declared without a write (new, D-RCV-60)
    Given the baseline document
    Then the ACE asset fact is declared as consumed through the owner's data product, with no v_ace_* property
    And the case move is declared as an answer, with no recovery_case or assignment property and no case row write
    And only operations owned by rwb-asset are listed, and a consumed operation is described as consumed and faked

Scenario: AC8 The owner, the verbs and the data rules follow the contract (new, D-RCV-60)
    Given the baseline document
    Then the owner of the balance is a role code with a scope, never a person, a user identifier or a name
    And a POST declares the Idempotency-Key and stores its answer, and a GET declares none
    And no personal data field is declared, one REST base, one topic, one queue and one login are named, and a schema change is additive within major version 1

Scenario: AC9 The vocabulary is closed and no event is declared (new, D-RCV-60)
    Given the baseline document
    Then LOV-HOLDING, LOV-SEGMENT, LOV-ASSET-TYPE and LOV-TRANSFER-IN are published as enumerated values
    And no event is declared by this baseline
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The balance is declared as a computed element of this service's own `asset` rows in schema `rwb_asset` and of no other owner's data: the count, the book-value total and the holding-cost total per `holding_status`, with the scope and the as-at date. The holding record is keyed by the ACE asset key with no foreign key and no copied ACE column | TSD S5 T3.1 and T3.2; Architecture v5 slide 41; DP-01; ASM-4745 |
| BR2 | The decision record is declared as an element written before the figure is confirmed, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S5 T2; legacy RWB-E3-024 AC1 and AC4 |
| BR3 | The ACE asset fact stays with rwb-source-data: the contract declares the data-product read as consumed, declares no `v_ace_*` property and describes no ACE table read of rwb-asset | DP-05; Architecture v5 slides 29, 37 and 45; ASM-4746 |
| BR4 | The case move is answered and not written: the contract declares the state read and the answer, and declares no `recovery_case` or `assignment` property and no case row write | Ownership Map (recovery_case and assignment owner P3) |
| BR5 | The owner of the balance is a role code of the access matrix, with a scope, and never a person, a user identifier or a name | FSD S5 A2.6.3.3; TSD S5 T6.1; Template and Rules §R7.2 (s17) |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; TSD S5 T-A.2 |
| BR7 | The vocabulary is closed: `LOV-HOLDING`, `LOV-SEGMENT`, `LOV-ASSET-TYPE` and `LOV-TRANSFER-IN` are published as enumerated values and no list value is a constant of the code | TSD S5 T3.2; FSD S5 BR-S5-006 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules §R7.2 (s17) |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes |
| BR11 | The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR12 | No event is declared: the balance changes on the read after a take-on, and the topic `rwb.asset.events.v1` carries the take-on and sale events of the sibling stories only | Architecture v5 slide 19 OUT; ASM-4745 |

Coverage: BR1 and BR2 by AC6; BR3, BR4 and BR11 by AC7; BR5, BR6, BR8, BR9 and BR10 by AC8; BR7 and BR12 by AC9. Each AC is tested by the test case with the same number in section 16 (TC-S5-E3024-CON-06 to -09).

### 9. State transitions

The lifecycle of this document, not of an asset or of a figure:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the balance element, the confirmation, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the reporting reader, the wave 2 harness and the rwb-source-data, rwb-case and rwb-access owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new filter or an optional balance grouping | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a list value changes, or the confirmation path is fixed and differs from the placeholder | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC4 and AC5 fail: a `v_ace_*` view, a `recovery_case` property, an event, a second topic, a Schedule or a balance table | In review |

The figure states the document describes are the app story's: live, shown and confirmed, with the confirmed figure kept as its as-at figure after a take-on. This baseline fixes the vocabulary and the shape and confirms no figure.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the fixing of the confirmation path and the correction of the Ownership Map rows the baseline consumes, including the missing `asset` row |
| Consuming teams (the app story, the two screens, the reporting reader, the wave 2 harness and the owners of rwb-source-data, rwb-case, rwb-access, rwb-decision and rwb-reporting) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake, and that the owner field is a role and not a person |

The per-service login behind the security scheme of the document is named "the rwb-asset login (DP-02)" and is not part of this baseline.

Each REST operation is authorised by the rwb-access authorise check (DP-08) before it runs; this baseline names that check and does not implement it.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Balance element | Not specified in the source documents (DOR-RWB-S5-E3024-CON-7) | `scope` (`LOV-SEGMENT`), `asAtDate`, `ownerRole`, `count`, `bookValueTotal`, `holdingCostTotal` per `holding_status`, `recordRef`, `ruleId`, `ruleVersion` — GAP-2861; ASM-4745 |
| Confirmation request | Not specified in the source documents (DOR-RWB-S5-E3024-CON-7) | `StockBalanceConfirmation`: `scope`, `asAtDate`, `officerRef`; all three required; no amount, price or limit as a default |
| Asset element | Not specified in the source documents (DOR-RWB-S5-E3024-CON-7) | The columns of DF-COL-028 to DF-COL-042 that the read shows: `id`, `case_id`, `asset_ref`, `asset_code`, `asset_type`, `transfer_in_type`, `from_segment`, `transfer_in_date`, `repossessed_date`, `stock_date`, `book_value`, `holding_status`, `holding_cost_to_date` |
| Lists | Not specified in the source documents (DOR-RWB-S5-E3024-CON-7) | `LOV-HOLDING`, `LOV-SEGMENT`, `LOV-ASSET-TYPE` and `LOV-TRANSFER-IN`, published as enumerations and read as reference data at their version under the reference-data contract (DP-06, DP-07); the parameters read with them: Not specified in the source documents (DOR-RWB-S5-E3024-CON-20) |
| Decision record | Not specified in the source documents (DOR-RWB-S5-E3024-CON-7) | DF-DEC-001 to DF-DEC-018 through the local library, written before the figure is confirmed (DP-03) |
| ACE asset fact | Not specified in the source documents (DOR-RWB-S5-E3024-CON-7) | DF-ACE-208 to DF-ACE-219 of `v_ace_npa_asset` in P1, read only through the owner's data product and never written, copied or joined here |
| Not declared here | Not specified in the source documents (DOR-RWB-S5-E3024-CON-7) | `recovery_case` and `assignment` (P3), `proceeds` (P8), `document` (P5), `decision_log_entry` and `rule_row` (P7), `asset_sale` (S5, the sale stories'), and the `v_ace_*` views (P1) |
| Consumed fields with no source | Not specified in the source documents (DOR-RWB-S5-E3024-CON-7) | The operation names of the rwb-source-data read and the confirmation path: Not specified in the source documents (GAP-2861; ASM-4743, ASM-4746) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story, and no balance table exists in any source (GAP-2861; ASM-4745).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, carrying the `AssetStockBalance` element, filtered by type, status, region, page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its holding status, book value, cost to date and listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |
| POST | Not specified in the source documents (GAP-2861; ASM-4743) | `StockBalanceConfirmation` in, `AssetStockBalance` out with its record reference | Asset and disposal, right C, scope applied | `Idempotency-Key` header |

The operations answer 400, 401, 403 with MSG-P4-002, 404, 409 for a repeated confirmation without the key, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The two read operation IDs are those of TSD S5 T-A.1 and the paths are those of the target base, not the monolith form. API-S5-003 `POST /assets/{assetId}/valuations` is rwb-valuation's under the Ownership Map ruling ASM-0043, and API-S5-004 and API-S5-005 belong to the pricing and auction stories of this service; `GET /assets/{assetKey}` is the key read of the same list and is not declared here. The confirmation has no operation in the FSD endpoint list, the TSD inventory or the Ownership Map, which is why its path is a placeholder (GAP-2861; ASM-4743).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2861; ASM-4746)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE NPA asset fact of the displayed asset: asset reference, asset code, asset type, transfer-in type, segment, taken-on date, book value and the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the account link of the asset row; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2861; ASM-4746)) | rwb-case (P3) | P3 rwb-case | The move `ASSET_ON_BOOKS` with the rule ID and its version, applied by the parent `CaseWorkflow` on the sibling's outcome; declared here as consumed for the two take-on criteria of the app story; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2861 with ASM-4746.

#### 12.3 Events published

None. The balance is a computed answer of this service's own rows and the confirmation writes a decision record; Architecture v5 slide 19 OUT gives `rwb.asset.events.v1` to `AssetTakenOn` and `AssetSold`, which belong to the take-on and sale stories. This baseline declares no event, no event name of its own and no outbox row, and the absence test of AC5 fails a build that adds one (BR12).

#### 12.4 Events consumed

None. The balance needs no message: it is read on demand and recomputed from the rows. This baseline therefore declares no consumer group, no subscription and no inbox, and no Kafka call of this feature (BR12).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` | The stage that hosts the confirmation step; its signals and its outcome are declared by the sibling story, not redefined here |
| `confirmStockBalance` | Activity, the one confirmation step | `rwb-asset` | In: the scope, the as-at date and the officer reference. Out: the confirmed `AssetStockBalance`, the record reference and the rule version |

No child workflow and no activity is registered by this story. The activity name is a target design choice and the confirmation is a human task of the officer, so it runs on the officer's action and not on a timer; the read is a query and is not a workflow step. The workflow ID form and the start rule (start or signalWithStart, duplicate-start policy) of `AssetDisposalWorkflow` are Not specified in the source documents (CG-ALL-9784).

#### 12.6 Schedules

None. The baseline declares no Temporal Schedule, no Quartz row and no shared job table, and no Job of Architecture v5 slide 44 is owned or moved here. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| asset | S5 (`rwb_asset`) | The taken-on assets the balance counts: the columns of §11, read only by this feature |
| listing | S5 (`rwb_asset`) | The listing and its sale status shown next to a listed asset; read only |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the confirmed figure (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated confirmation and the answer it holds |

`recovery_case` and `assignment` (P3), `proceeds` (P8), `document` (P5), `decision_log_entry` and `rule_row` (P7), `asset_sale` (S5, the sale stories') and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table. No balance table is declared by any source, and a baseline that adds one fails the boundary test (GAP-2861; ASM-4745).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The ACE NPA asset `AST-2026-000524` with transfer-in date `2026-11-20` and book value `4500000.00`; a stale product with its date; no answer beyond 2 s; an unreadable answer | AC4, AC5 |
| rwb-case state and move fake | The states `ASSET_PENDING_TAKE_ON`, `ASSET_ON_BOOKS` and `ASSET_HELD` of case `RC-2026-000524`; an accepted move and a refused move | AC4, AC5 |
| rwb-access role fake | RW-NPAMGR with CRU, RW-HEADNPA with RA and a role without the right, each with its scope | AC2, AC3, AC5 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-01, R-DIS-02 and R-DIS-03 | AC2, AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000524` | AC1, AC5 |
| Asset-row fixture set | Three `asset` rows of the same scope in `HELD`, `LISTED` and `SOLD` with their book values and costs, producing one count and two totals per status | AC2 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data read, of the case-move answer and of the confirmation are derived from the published documents or designed here and carry the placeholder until their owners confirm them (GAP-2861; ASM-4743, ASM-4746).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The balance, the asset and the confirmation on `/api/recovery/asset/v1`; the rwb-source-data data-product read, the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event is declared by this baseline |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `AssetDisposalWorkflow` and `confirmStockBalance` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no asset, no case and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and seven fakes.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml`, the `AssetStockBalance`, `StockBalanceConfirmation` and `Asset` elements, the vocabulary of the four lists as published enumerations, the contract README rows for the consumed rows and the confirmation path with their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on any other owner's schema, because rwb-asset holds none (Architecture v5 slides 29, 37 and 45; ASM-4746). DP-13 moves the base and nothing else. DP-19 is behind SCR-21 and SCR-22, whose screen model is the edge contract's. DP-03 is the element rule of the confirmation.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the plan already carries for this key and no other; the three consumed rows are C dependencies in fact and not in the metadata row (GAP-2861; ASM-4746), and no event library is added because no event is declared.

**Build steps**

1. Write the two reads and validate the additive rule of AC1 in the pipeline.
2. Write the `AssetStockBalance` element, its owner and as-at fields and its four lists of AC2 with the placeholder where a type is unstated.
3. Write the `StockBalanceConfirmation` request and the confirmation operation of AC3 with its path placeholder, its rights and its idempotency.
4. Record the consumed rwb-source-data and rwb-case rows of AC4 with their owner, budget, freshness stamp and placeholder.
5. Record the decision-record element of AC5 and validate it against the library schema.
6. Publish the seven fakes of AC5 and the drift test.
7. Record the naming baseline and the boundary of AC5, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the four contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the two screens, the reporting reader and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the confirmation is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares, or the scope excludes the segment | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the figure is confirmed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of the displayed asset is stale after a late or failed batch (VR-S5-006-1); the check is the owner's and this service holds no ACE batch status read | {product} is from {date}. Today's load has not arrived. |
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no operation of this baseline raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no operation of this baseline raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |

The six message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of the feature, and the check itself belongs to rwb-source-data (GAP-2861; ASM-4746).

### 15. Screens and states

The contract serves SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its take-on, held, listed and sold states, all through the gateway-bff composite route (DP-19). The SCR-21 empty, error and no-access states are Not specified in the source documents (CG-ALL-9788); the SCR-22 empty, loading, error and no-access states are Not specified in the source documents (CG-ALL-9789). The route calls rwb-asset for the balance and the asset, rwb-case for the case and its route state and rwb-source-data for the ACE asset fact; this baseline fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The figure states of the app story — live, shown, confirmed, refused, not recorded, invalid and unavailable — read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-024-01 | AC1, AC2 | Contract | Asset `AST-2026-000524` of case `RC-2026-000524`; the contract half answers the list with the balance element and the single read |
| TC-E3-024-02 | AC2, AC4 | Contract | The RPS repossession result of the vehicle and the case state `ASSET_PENDING_TAKE_ON`; the contract half answers the consumed rows and the holding-status vocabulary |
| TC-E3-024-03 | AC2, AC4 | Contract | The AMIS deed in lieu transfer with its opening book value; the contract half answers the segment scope and the two totals |
| TC-E3-024-04 | AC3, AC5 | Contract | A repeated confirmation with the same `Idempotency-Key` and a malformed request; the contract half answers one record, the 409 and the 422 envelope |
| TC-E3-024-05 | AC3 | Contract | RW-NPAMGR holds CRU and RW-HEADNPA holds RA; the contract half answers the right of the confirmation |
| TC-E3-024-06 | AC5 | Contract | The decision-record stub stopped and the absence tests; the contract half answers the MSG-P7-003 path and declares no event, no second topic and no balance table |
| TC-S5-E3024-CON-01 | AC1 | Contract | The document validates; the two reads, the base, the filters and the error answers are present |
| TC-S5-E3024-CON-02 | AC2 | Contract | The `AssetStockBalance` element validates with its fields, its owner role and the four closed lists |
| TC-S5-E3024-CON-03 | AC3 | Contract | The confirmation request validates with its three required fields, its idempotency and its placeholder path |
| TC-S5-E3024-CON-04 | AC4, AC5 | Contract | The consumed rows and their placeholders; the seven fakes match the document and a drifted fake fails the build; the no-`v_ace_*`, no-`recovery_case` and no-balance-table boundary |
| TC-S5-E3024-CON-05 | AC5 | Contract | The boundary of the four tables of §12.7 (asset, listing, decision_record, idempotency_key): these are the only tables declared, and a baseline that adds a balance table fails |
| TC-S5-E3024-CON-06 | AC6 | Contract | The computed balance element of the own asset rows and the decision-record element written before the figure; a failed write changes nothing |
| TC-S5-E3024-CON-07 | AC7 | Contract | The consumed ACE fact, the case-move answer with no case write, and the list of owned operations only; no `v_ace_*` and no `recovery_case` property |
| TC-S5-E3024-CON-08 | AC8 | Contract | The owner role with its scope, the POST and GET key rules, the personal-data check and the single base, topic, queue and login; the additive schema rule |
| TC-S5-E3024-CON-09 | AC9 | Contract | The four closed lists as enumerated values and the no-event declaration; no event on `rwb.asset.events.v1` is declared by this baseline |

The six legacy cases are the legacy cases of RWB-E3-024 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E3024-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The nine cases `TC-S5-E3024-CON-01` to `-09` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the lists, the rule rows, the segment scopes and the one-working-day targets stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only, and the owner field is a role code and never a person; every example is synthetic.
- The ACE asset fact stays with rwb-source-data and the case with rwb-case: the document declares no `v_ace_*` path, no `recovery_case` or `assignment` property, no case row write and no ACE table read (BR3, BR4).
- The money stays with rwb-payment and the sale status with the sale stories: the document declares no posting, no balance amount of rwb-payment and no price.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (BR11).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row, a shared job table or a balance table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| Not specified in the source documents (GAP-2861; ASM-4745) | No requirement ID is mapped to FEAT-AST-06 in TSD S5 T8 and the split plan carries none for this slice; the contract fixes the fields, the owner and the consumed rows on which the balance is built, and the legacy requirement it serves is RWB-E3-024 | The `AssetStockBalance` element, the confirmation and the three consumed rows | TC-E3-024-01, TC-E3-024-04, TC-S5-E3024-CON-01, TC-S5-E3024-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S5-E3024-CON-04 |
| ADR-022 | Local decision record plus central ledger | The decision-record element of the confirmation | TC-E3-024-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-024, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S5-E3024-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S5-E3024-CON-01 to -04 |
| Feature and screens | FEAT-AST-06, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-01, R-DIS-02 and R-DIS-03, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two reads, the balance computation, the owner resolution and the confirmation record: RWB-S5-E3024-APP.
- The creation of the `asset` row under R-DIS-01, R-DIS-02 and R-DIS-03: RWB-S5-E3019-APP, RWB-S5-E3020-APP and RWB-S5-E3021-APP.
- The case of record, its route states, its assignment and the parent `CaseWorkflow`: rwb-case (P3), whose state this baseline declares as consumed and faked.
- The ACE NPA asset, collateral and account facts and the freshness of the data product: rwb-source-data (P1) (GAP-2861; ASM-4746).
- The role matrix, the scopes and the masking rules: rwb-access (P4), whose role codes this baseline names.
- The holding-age clock and the cost of carry that feeds `holding_cost_to_date`: RWB-S5-E3023-APP, with the posting in rwb-payment (P8).
- The authoring, testing, approval and versioning of the DISPOSAL package and of the rule rows: rwb-decision (P7).
- The valuations of the asset: rwb-valuation (S1) under API-S5-003 and ASM-0043.
- The listing, the floor price and the auction rounds: the pricing and auction stories of this service, API-S5-004 and API-S5-005.
- The reporting projection of the stock balance: rwb-reporting (P9), which reads the operation and receives no event from this baseline.
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
