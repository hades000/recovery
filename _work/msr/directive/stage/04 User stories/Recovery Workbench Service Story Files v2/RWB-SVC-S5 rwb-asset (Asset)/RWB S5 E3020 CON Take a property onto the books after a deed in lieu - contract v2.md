# RWB-S5-E3020-CON Take a property onto the books after a deed in lieu - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3020-CON |
| Work type | CON |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S5-E3020-CON-16) |
| Contract version | v1 (path `/api/recovery/asset/v1`, event `rwb.asset.AssetTakenOn.v1`); finer version Not specified in the source documents (DOR-RWB-S5-E3020-CON-23) |
| Depends on (build) | None |
| Contract dependencies | RWB-S2-E3012-CON (rwb-treatment transfer read); rwb-source-data (asset, collateral and score reads; source field names, business key and freshness response to be confirmed with P1 before wave 2 system test) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped; traces to REQ-S5-001 of the Business Requirements Program v4; the split plan allocates no requirement id to RWB-E3-020 (GAP-2845)) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the deed in lieu take-on step of rwb-asset, split from RWB-E3-020. It fixes the two asset reads on `/api/recovery/asset/v1` (DP-13), the `asset` element and its closed lists, the `AssetTakenOn` envelope on `rwb.asset.events.v1`, the consumed rwb-treatment, rwb-source-data and rwb-case rows with their placeholders, the decision-record element of DP-03, the tables and the fakes. The rwb-treatment and rwb-source-data rows are class C dependencies that the plan's contract row does not carry (GAP-2840; ASM-4705; GAP-2842; ASM-4707), the case-move answer has no published operation (GAP-2844; ASM-4709), the plan's pattern set omits DP-09 although event 22 exists (GAP-2843; ASM-4708) and the Ownership Map carries no `asset` row (GAP-2841; ASM-4706). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3020-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 14 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the deed in lieu take-on step of rwb-asset — the two asset reads, the `asset` element with its closed lists, the `AssetTakenOn` envelope, the consumed rwb-treatment, rwb-source-data and rwb-case rows, the decision-record element, the tables and the fakes**, so that **the app story, the two screens and the wave 2 harness build against one fixed and testable contract on Day 1, and an asset property, a list value, an event property or an answer shape cannot drift between rwb-asset, rwb-treatment, rwb-source-data, rwb-case and rwb-payment without a failing build**.

The baseline fixes the naming the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and package `th.co.scb.ace.workbench.recovery.asset`. It declares that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is a prohibition and the ACE facts are consumed on the owner's contract only. It decides no business outcome: the criteria of RWB-E3-020 stay with RWB-S5-E3020-APP.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy take-on of RWB-E3-020 crossed four boundaries at once: an officer screen, the ACE NPA asset record, a case state and the decision log. The target splits them: rwb-treatment owns the agreement and its registered transfer, rwb-source-data owns the ACE facts, rwb-case owns the case and its route states, and rwb-asset owns the asset record and the take-on event. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the `asset` properties of the take-on, the values of `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN` and `LOV-HOLDING`, the `AssetTakenOn` envelope, the transfer the rwb-treatment contract answers, the ACE fact of the data product, the case state and move, and the record of the decision.

The baseline is also the only place where the placeholders live: three consumed rows have no published operation name, one table has no Ownership Map row, and the outbox library is absent from the pattern set. Each is carried as a gap and an assumption rather than settled quietly, so the app story and the harness see one documented surface and the register sees each missing value once.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, topic, queue and event names follow the platform rule.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; this document narrows them only where it says so.
- Ownership is taken from the Ownership Map and the context pack only: `listing` and `asset_sale` are S5's; `recovery_case` and `assignment` are P3's; `treatment` is S2's; `proceeds` is P8's; `document` is P5's; `notice` is P6's; `decision_log_entry` and `rule_row` are P7's; every `v_ace_*` view is P1's. `asset` has no Ownership Map row and is read as S5's from TSD S5 T3.1 and Architecture v5 slides 19 and 41 (GAP-2841; ASM-4706).
- `RWB-S2-E3012-CON`, the DP06 Collateral and assets contract of rwb-source-data and the rwb-case state and move rows are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None (GAP-2840, -4, -6; ASM-4705, -4, -6).
- The outbox and inbox library `RWB-PLT-TE006-CON` of DP-09 is the platform dependency of the published event; the pattern set of this key does not carry it and this baseline keeps the metadata as the plan states it (GAP-2843; ASM-4708).
- The DISPOSAL rule package with R-DIS-01, R-DIS-02 and R-DIS-03 is governed in rwb-decision (P7); this baseline names the rules and declares none of them.
- The `asset` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (§R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this step: the two reads with their answers, filters, rights and error responses.
2. Fix the `asset` element as this service's own record in schema rwb_asset, keyed by the ACE asset key with no foreign key and no copied ACE column; the ACE asset stays read-only through the source-data contract. Its columns are DF-COL-028 to DF-COL-042, with their types, required flags and the list each is declared against.
3. Fix the `AssetTakenOn` envelope on `rwb.asset.events.v1`: the CloudEvents attributes, the data properties of the take-on and the ban on personal data. The event is written in the same transaction as the row through the outbox library RWB-PLT-TE006-CON (DP-09, platform dependency of the published event; GAP-2843).
4. Fix the consumed rows: the rwb-treatment transfer read of RWB-S2-E3012-CON, built against its published document and fake from Day 1; the DP06 Collateral and assets data-product read of rwb-source-data with its freshness stamp, carrying the asset reference, asset code, asset type, segment, taken-on date, book value and collateral reference; and the rwb-case state read and move answer as the stage outcome of the child workflow with the rule ID and its version, each with the placeholder Not specified in the source documents (GAP-2842; GAP-2844) where no source names the operation.
5. Record the decision-record element, written before the asset row changes (DP-03).
6. Record the closed vocabulary of the lists, the naming baseline and the rule that no value is a constant of the code.
7. Publish the contract tables of §12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the error envelope, the absence of a `v_ace_*` read and of a case write, drift between a fake and the document, and the absence of a consumed event.
9. Tag the baseline and hand it to RWB-S5-E3020-APP, the two screens and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or response body fails schema validation | The schema lint fails the build; a deployed service answers 400 or 500 with the envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A fake drifts from the document | The drift test fails the build and blocks the merge | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption; the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT` or `LOV-HOLDING` appears | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, or a `v_ace_*` view, a `recovery_case` property or a `treatment` property | The review fails the baseline; the boundary test fails the build | None | AC5 |
| X7 | The document declares a consumed event, a second topic, a Schedule or a Quartz row | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation differ from TSD S5 T-A.1 | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner documents of rwb-treatment, rwb-source-data and rwb-case only |
| Negotiable | Element names beyond the ones the sources give, example values and fake fixtures are settled in the baseline review; the operations, lists, base, topic and queue are fixed |
| Valuable | Unblocks RWB-S5-E3020-APP, the two screens, the wave 2 harness and the rwb-treatment, rwb-source-data, rwb-case and rwb-payment teams on Day 1 |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, six fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the deed in lieu take-on step of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing and asset_sale is S5, of recovery_case is P3, of treatment is S2 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two asset reads are declared on the asset base with their shapes and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /assets with an AssetPage answer of status 200 and GET /assets/{assetId} with an Asset answer of status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then the list declares the filters type, status, region, page and size, and the single read declares the path parameter assetId
    Then the answers 400, 401, 403, 404, 422 and 503 are declared with one envelope and one message ID per condition, and neither read declares an Idempotency-Key
    Then the key-based read, the creation of a listing and the round of a listing are declared as other stories' and not by this baseline

  Scenario: AC2 The asset element and its closed lists are fixed for the take-on (new, D-RCV-60)
    Given the asset section of the baseline
    When it is compared with TSD S5 T3.1 and T3.2
    Then the Asset element declares the properties of DF-COL-028 to DF-COL-042: id, case_id, collateral_id, asset_ref, asset_code, asset_type, transfer_in_type, from_segment, transfer_in_date, book_value, auction_purchase_price, repossessed_date, stock_date, holding_status and holding_cost_to_date
    Then asset_type is declared against LOV-ASSET-TYPE with the values DETACHED_HOUSE, TOWNHOUSE, CONDOMINIUM, LAND, COMMERCIAL_BUILDING and VEHICLE
    Then transfer_in_type is declared against LOV-TRANSFER-IN with the values AUCTION_PURCHASE, DEED_IN_LIEU and REPOSSESSION, and DEED_IN_LIEU is the value of this step
    Then from_segment is declared against LOV-SEGMENT and holding_status against LOV-HOLDING with the values HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED
    Then id, asset_ref, asset_type, transfer_in_type, transfer_in_date, book_value and holding_status are required and the other properties optional
    Then no property is added for a condition, a photograph, a location or a provision step, and those facts are referenced as documents and valuations of their owners

  Scenario: AC3 The AssetTakenOn event is declared with its envelope and its prohibitions (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with the event catalogue and the service topic
    Then AssetTakenOn is declared on the topic rwb.asset.events.v1 with the event name rwb.asset.AssetTakenOn.v1, produced by rwb-asset, with rwb-case and rwb-payment as its only consumers
    Then its data carries the case reference, the asset reference, the asset type, the transfer-in type, the taken-on date and the rule ID with its version, and no amount, balance or posting fact
    Then the envelope is CloudEvents and the topic declares its retry and .dlt topics
    Then a schema test fails any personal data property in the event or its examples
    Then no second event, no second topic and no Schedule is declared by this baseline

  Scenario: AC4 The consumed transfer row is declared and the agreement stays with rwb-treatment (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with RWB-S2-E3012-CON and the treatment contract
    Then the registered transfer read is declared as consumed from S2 rwb-treatment, with the case reference, the agreement reference, the property reference, the registered transfer date, the opening book value and the reversal state
    Then the operation name of the row is Not specified in the source documents (GAP-2840; ASM-4705) and the row carries the placeholder
    Then the document declares no treatment property, no settlement figure and no registration step of this service
    Then the call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The ACE, case and access sections are fixed and no table of another owner is declared (new, D-RCV-60)
    Given the consumed rows, the access section and the data section of the baseline
    When they are compared with the data-product contract, rwb-case and TSD S5 T-A.1 and T6.1
    Then the read of DP06 Collateral and assets is declared as consumed from P1 rwb-source-data with the asset reference, asset code, asset type, transfer-in type, segment, taken-on date, book value, collateral reference and the freshness stamp
    Then the operation name of that row is Not specified in the source documents (GAP-2842; ASM-4707) and the case-move answer carries its own placeholder (GAP-2844; ASM-4709)
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property and no grant on any rwb_* schema of another owner
    Then both reads declare Asset and disposal right R with the scope applied, and a repeated request with the same Idempotency-Key describes no second effect
    Then the tables named as owned are asset and asset_sale and listing of S5 with the library objects, and the ownership of asset is recorded as read from TSD S5 T3.1 while the Ownership Map names no row (GAP-2841; ASM-4706)

  Scenario: AC6 The decision-record element and the six fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or element it serves
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the agreement reference, the rule ID, the package version in force, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on rwb.decision-record.v1 before the asset row changes, and a failed write leaves the asset unchanged with MSG-P7-003
    Then the rwb-treatment fake answers a registered transfer, a transfer not registered, a reversal and no answer beyond 2 s
    Then the rwb-source-data fake answers the ACE asset and collateral facts, a stale product and no answer beyond 2 s, and the rwb-case fake answers the two route states and an accepted and a refused move
    Then the decision-record stub answers a healthy chain and a stopped chain, and the outbox stub answers a relayed AssetTakenOn and a relay that retries
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is consumed (new, D-RCV-60)
    Given the naming and event sections of the baseline
    When the nine contract sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the package is th.co.scb.ace.workbench.recovery.asset
    Then the document declares no consumed event, no second topic, no Schedule and no Quartz row, and the absence test fails a build that adds one
    Then the consumed rows name their owners from the Ownership Map and the context pack, and no row is declared as provided by rwb-asset
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome of RWB-S5-E3020-APP and they copy no legacy criterion; the four legacy criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The asset record is rwb-asset's, and the contract declares its properties, lists and required flags on the `asset` element only | TSD S5 T3.1 and T3.2; ASM-4706 |
| BR2 | The decision record is declared as an element written before the asset row changes, through the local library; a failed write changes nothing | DP-03; TSD S5 T2 |
| BR3 | The agreement stays with rwb-treatment: its read is declared as consumed with a placeholder, and no treatment property is declared | GAP-2840 |
| BR4 | The ACE facts stay with rwb-source-data: the data-product read is declared as consumed and no `v_ace_*` property or ACE table read is described | DP-05; GAP-2842 |
| BR5 | The case move is answered and not written: the state read and the answer are declared, and no `recovery_case` property | GAP-2844 |
| BR6 | The event is declared once: `AssetTakenOn` on `rwb.asset.events.v1` with rwb-case and rwb-payment as its only consumers | GAP-2843 |
| BR7 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | TSD S5 T-A.2 |
| BR8 | The vocabulary is closed: the four lists are published as enumerations and no list value is a constant of the code | TSD S5 T3.2; FSD S5 BR-S5-002 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | §R7.2 s17 |
| BR10 | One base, one topic, one queue and one login per service; no document names another service's base or topic as its own | DP-13, DP-14 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | ADR-020 |
| BR12 | The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided | DP-11; Ownership Map |

Coverage of each rule by a criterion and a test case: BR1 and BR8 by AC2 (TC-E3-020-01, TC-S5-E3020-CON-02); BR2 by AC6 (TC-E3-020-04, TC-S5-E3020-CON-05); BR3, BR4, BR5 and BR9 by AC4 (TC-E3-020-02, TC-S5-E3020-CON-04); BR6 by AC3 (TC-E3-020-06, TC-S5-E3020-CON-03); BR7, BR10, BR11 and BR12 by AC1 (TC-E3-020-01, TC-S5-E3020-CON-01).

### 9. State transitions

The lifecycle of this document, not of an asset:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the element, the lists, the event, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the screens, the harness and the rwb-treatment, rwb-source-data, rwb-case and rwb-payment owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property, a filter or an optional field is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake, or a forbidden element | A contract test fails: a `v_ace_*` view, a case property, a consumed event or a Schedule | In review |

The holding-status machine the document describes belongs to the app story: `LOV-HOLDING` is HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED, and this baseline fixes the vocabulary and the take-on value `HELD` and moves no asset.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the missing `asset` row |
| Consuming teams (the app story, the screens, the harness and the owners of rwb-treatment, rwb-source-data, rwb-case, rwb-decision, rwb-access and rwb-payment) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-asset login (DP-02)" and is not part of this baseline.

The rwb-access authorise check (DP-08) gates every operation of this baseline before it acts; its operation name is Not specified in the source documents (DOR-RWB-S5-E3020-CON-6).

### 11. Data

The baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Asset element | The columns of DF-COL-028 to DF-COL-042, from `id` to `holding_cost_to_date` |
| Required flags | `id`, `asset_ref`, `asset_type`, `transfer_in_type`, `transfer_in_date`, `book_value` and `holding_status` required; the other eight optional |
| Lists | `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT` and `LOV-HOLDING`, published as enumerations and read at their version |
| Reference data | The four lists are read at their version under DP-06 and DP-07; the parameters read are Not specified in the source documents (DOR-RWB-S5-E3020-CON-20) |
| Event data | Case reference, asset reference, asset type, transfer-in type, taken-on date and the rule ID with its version |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) |
| ACE fact | DF-ACE-208 to DF-ACE-219 of `v_ace_npa_asset` in P1, read only through the owner's data product and never copied or joined here |
| Not declared here | `recovery_case` and `assignment` (P3), `treatment` (S2), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7) |
| Fields with no source | The operation names of the transfer read, the data-product read and the case-move answer carry the placeholder (GAP-2840, -4, -6) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the additive rule of BR11. **No new table, no new column and no migration** is declared here.

BR Field IDs: the Asset element and the Required flags take DF-COL-028 to DF-COL-042; the Decision record takes DF-DEC-001 to DF-DEC-018; the ACE fact takes DF-ACE-208 to DF-ACE-219; Event data, Lists, Reference data, Not declared here and Fields with no source take Not specified in the source documents (DOR-RWB-S5-E3020-CON-7).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated by page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetId}` | Asset of status 200 out, with title, condition, valuations, costs and listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |

The two operations answer 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of §14. The key-based read of the asset, the creation of a listing on the asset reference and on the asset id, and the round of a listing are the pricing and listing stories' and are not declared here.

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use in the baseline |
|---|---|---|---|
| The transfer read of `RWB-S2-E3012-CON` (operation name Not specified in the source documents (GAP-2840; ASM-4705)) | `/api/recovery/treatment/v1` | S2 rwb-treatment | The registered deed in lieu transfer: case, agreement and property references, registered date, opening book value and the reversal state; faked |
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2842; ASM-4707)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE NPA asset and collateral facts with the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the account link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2844; ASM-4709)) | rwb-case (P3) | P3 rwb-case | `ASSET_ON_BOOKS` with the rule and its version; the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The rows are contract dependencies of class C that the plan's contract row does not carry, and the absence is recorded as GAP-2840, -4 and -6.

#### 12.3 Events published

| Event | Topic | Documented data | Consumers |
|---|---|---|---|
| `AssetTakenOn` (`rwb.asset.AssetTakenOn.v1`) | `rwb.asset.events.v1`, with `.retry` and `.dlt` | Case, asset reference, asset type, transfer-in type, taken-on date and the rule ID with its version; CloudEvents envelope; no personal data | rwb-case and rwb-payment, and no other consumer |

`AssetSold` is the second event of the service and belongs to the sale stories; this baseline declares it as the catalogue's and not as an element of this step. The outbox that relays `AssetTakenOn` is the DP-09 library, which the pattern set does not carry (GAP-2843; ASM-4708).

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none is a deed in lieu transfer; the S2 contract answers it synchronously. This baseline declares no consumer group, no subscription and no inbox of its own, and the absence test of AC7 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` | The stage that hosts the take-on step; its signals and its outcome for the parent are declared, not built |
| `takeOnAsset` | Activity, the one take-on step | `rwb-asset` | The case and the registered transfer in; the rule with its version, the asset reference, the event and the case move out |

Workflow ID form: Not specified in the source documents (CG-ALL-9649). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-9649).

No child workflow for the case, the agreement or the money exists in this service. The activity name is a target design choice; the trigger is read as the arrival of the registered transfer for a case in `ASSET_PENDING_TAKE_ON`, because the FSD declares no background event for the feature (FSD S5 A2.2.4.4). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the registered transfer and the case signal. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| asset | S5 (`rwb_asset`); read as S5 from TSD S5 T3.1 and Architecture v5 slides 19 and 41 while the Ownership Map names no row (GAP-2841; ASM-4706) | The taken-on property, its fields, its lists and its holding status; the table the two reads answer from |
| asset_sale | S5 (`rwb_asset`), Ownership Map | The sale of an asset; not declared by this step |
| listing | S5 (`rwb_asset`), Ownership Map | The offered asset with its prices and rounds; not declared by this step |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated fact and the answer it holds |
| outbox_event | PLT library, created in `rwb_asset` | The `AssetTakenOn` row relayed to `rwb.asset.events.v1` (DP-09) |

`recovery_case` and `assignment` (P3), `treatment` (S2), `proceeds` (P8), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are not owned here; the baseline names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-treatment transfer fake (`RWB-S2-E3012-CON`) | A registered transfer with its date and opening book value; a transfer not registered; a reversal; no answer beyond 2 s | AC4, AC6 |
| rwb-source-data data-product fake | The ACE NPA asset and collateral facts; a stale product with its date; no answer beyond 2 s | AC5, AC6 |
| rwb-case state and move fake | `ASSET_PENDING_TAKE_ON` and `ASSET_ON_BOOKS`; an accepted and a refused move | AC5, AC6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version with R-DIS-01, R-DIS-02 and R-DIS-03 | AC6 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| Outbox relay stub (`RWB-PLT-TE006-CON`) | A relayed `AssetTakenOn` and a relay that fails and retries | AC3, AC6 |

The fakes are test-only and are replaced by the real services in SIT; the operation names of the transfer read, the data-product read and the move answer are derived from the published documents and carry the placeholder until their owners confirm them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two asset reads on `/api/recovery/asset/v1`; the transfer read, the data-product read, the case state read and the move answer; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `AssetTakenOn` on `rwb.asset.events.v1`; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `AssetDisposalWorkflow` and `takeOnAsset` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no asset, no case and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment, the nine contract tables and six fakes.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml` with the `Asset` and `AssetPage` elements; the `AssetTakenOn` envelope in `asyncapi/rwb-asset-v1.yaml`; the four lists as published enumerations; the contract README rows for the consumed rows and their placeholders; the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: the document declares no `v_ace_*` path, property or grant (GAP-2842; ASM-4707). DP-13 moves the base and nothing else. DP-19 is behind SCR-21 and SCR-22, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, which is why the outbox library is recorded as an absent H row rather than declared (GAP-2843; ASM-4708).

**Dependencies the tables add and the plan does not hold.** The pattern table adds two H rows that the plan already carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, and it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the published event needs. The four consumed rows are C dependencies in fact and not in the metadata row (GAP-2840, -4, -6; ASM-4705, -4, -6).

**Build steps**

1. Write the two reads and validate the additive rule of AC1 in the pipeline.
2. Write the `Asset` element, its required flags and its four lists of AC2.
3. Write the `AssetTakenOn` envelope and the AsyncAPI fragment of AC3, with the no-personal-data and no-second-event tests.
4. Record the consumed rwb-treatment row of AC4 with its owner, budget, reversal state and placeholder.
5. Record the rwb-source-data and rwb-case rows, the rights and the error envelope of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the six fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the four new contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the two screens and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set. It names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | A role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the asset row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the case is stale after a late or failed batch (VR-S5-002-1); the check is the owner's and this service holds no ACE batch read | {product} is from {date}. Today's load has not arrived. |

The six IDs are contract elements and the text is the legacy and FSD wording, copied unchanged, except MSG-P1-001 as the next sentence states. The wording of MSG-P1-001 is copied from Error and Message Standard v4 (DOR-RWB-S5-E3020-CON-9). MSG-P1-001 is carried because it is in the message set of this feature, while the check itself belongs to rwb-source-data (GAP-2842; ASM-4707).

### 15. Screens and states

The contract serves SCR-21 Asset list in its loading and list states (empty, error and no access: Not specified in the source documents (CG-ALL-9653)) and SCR-22 Asset record in its take-on, held, listed and sold states (empty, loading, error and no access: Not specified in the source documents (CG-ALL-9654)) through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset and its holding status, rwb-case for the case and its route state, rwb-source-data for the ACE fact and rwb-valuation for the valuation references; this baseline fixes the rwb-asset answers only, and the route and the screen field list belong to RWB-PLT-N001-CON. The refusal, not-recorded and stale-data states the app story shows read the messages of §14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-020-01 | AC1, AC2 | Contract | The contract half of the take-on case: the two reads, the `Asset` element and its lists |
| TC-E3-020-02 | AC2, AC4 | Contract | A mocked registered transfer; the contract half answers the asset properties and the consumed transfer row |
| TC-E3-020-03 | AC4, AC5 | Contract | The sibling vehicle route's fact; the contract half fixes the same element and the same consumed rows |
| TC-E3-020-04 | AC6 | Contract | The decision-record stub stopped; the contract half declares the MSG-P7-003 path and the failure element |
| TC-E3-020-05 | AC5 | Contract | A role without the Asset and disposal right; the 403 with MSG-P4-002 and the rights of the two reads |
| TC-E3-020-06 | AC3, AC7 | Contract | A forced record failure and a stale product; the contract half fixes the envelope and the absence tests |
| TC-S5-E3020-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the filters and the six error answers are present |
| TC-S5-E3020-CON-02 | AC2 | Contract | The `Asset` element validates with its fifteen properties, seven required flags and four closed lists |
| TC-S5-E3020-CON-03 | AC3, AC7 | Contract | The `AssetTakenOn` envelope validates against CloudEvents and the catalogue; the absence test for a consumed event, a second topic and a Schedule |
| TC-S5-E3020-CON-04 | AC4, AC5, AC6 | Contract | The four consumed rows and their placeholders; the six fakes match the document and a drifted fake fails the build; the no-`v_ace_*` and no-case boundary |
| TC-S5-E3020-CON-05 | AC3, AC6 | Contract | Boundary of the six tables of §12.7: the three rwb_asset tables and the three PLT library tables; no table outside the list is created |

The six legacy cases are those of RWB-E3-020 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, and the business outcome of each is proved by RWB-S5-E3020-APP. The legacy level `System` maps to `Contract` because the artefact under test is the contract. The five `TC-S5-E3020-CON-` cases are new for this baseline. AC3 is asserted here only as a regression at the take-on boundary; R-DIS-02 is built once, in RWB-S5-E3020-APP (GAP-2940). The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same IDs; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the condition codes, the book value rule, the lists and the rule rows stay data, reference data or the rule package, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only, and every example is synthetic.
- The agreement stays with rwb-treatment and the ACE facts with rwb-source-data: the document declares no `treatment` property, no `v_ace_*` path and no ACE table read (BR3, BR4).
- The case stays with rwb-case and the money with rwb-payment: the document declares no `recovery_case` property, no posting and no balance.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (DP-11, BR12).
- No retired element is reintroduced: the absence tests fail a build that declares a consumed event, a second topic, a Schedule or a Quartz row.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S5-001 | Every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step (Business Requirements Program v5); the plan allocates no id for this slice (GAP-2845; ASM-4710) | The `Asset` element, the `AssetTakenOn` envelope and the four consumed rows | TC-E3-020-01, TC-S5-E3020-CON-01, TC-S5-E3020-CON-02 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `AssetTakenOn` envelope and the outbox row | TC-S5-E3020-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S5-E3020-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-020, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S5-E3020-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and TC-S5-E3020-CON-01 to -04 |
| Feature and screens | FEAT-AST-02, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-02, with R-DIS-01 and R-DIS-03 named, from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the two reads, the evaluation of R-DIS-02, the decision record, the `asset` row, the event and the case-move answer: RWB-S5-E3020-APP.
- The agreement, its settlement figures, the registration and its reversal: rwb-treatment (S2), whose read this baseline declares as consumed and faked (GAP-2840).
- The Land Office registration: an officer step with no service owner (GAP-2846; ASM-4711).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3) (GAP-2844).
- The ACE NPA asset and collateral facts and the freshness of the data product: rwb-source-data (P1) (GAP-2842).
- The vehicle repossession and LED auction take-on routes: RWB-S5-E3019-CON and RWB-S5-E3021-CON.
- The holding-age clock, the provision steps and the monthly cost of carry: RWB-S5-E3023-APP, with the posting in rwb-payment (P8).
- The valuations of the asset, the listing, the floor price and the auction rounds: rwb-valuation (S1) and the pricing and listing stories of this service.
- The authoring and versioning of the DISPOSAL package and its rule rows: rwb-decision (P7).
- The composite route and the screen field list: RWB-PLT-N001-CON. The cross-service journey: the wave 2 harness. The deployment, the flag and the runbook: the operations story of this legacy key.
