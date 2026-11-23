# RWB-S5-E3020-APP Take a property onto the books after a deed in lieu

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3020-APP |
| Work type | APP |
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
| Parallel lane | L-S5-C |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E3020-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-020 split out for rwb-asset. The four legacy criteria are kept word for word with their origin tag; the take-on runs as one step of `AssetDisposalWorkflow` on task queue `rwb-asset`, reads the completed deed in lieu transfer on the rwb-treatment contract with a placeholder name (GAP-2840; ASM-4705), evaluates R-DIS-02, creates the `asset` row in `rwb_asset` with the opening book value, records the decision through the local library before the row changes (DP-03), answers the case move `ASSET_ON_BOOKS` to rwb-case (GAP-2844; ASM-4709) and publishes `AssetTakenOn` from the outbox (event 22) on the pattern set's absent DP-09 library (GAP-2843; ASM-4708). The ACE facts arrive on the rwb-source-data data product because rwb-asset holds no `v_ace_*` grant (GAP-2842; ASM-4707); the base becomes `/api/recovery/asset/v1` (DP-13) and SCR-21 and SCR-22 read through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **the Workbench to create the asset record when a deed in lieu transfer completes and to record the decision with the rule version that produced it**, so that **a property taken in satisfaction of a debt enters the NPA stock on the day the transfer registers, with a book value the books can carry**.

This story owns:

- the four legacy criteria of RWB-E3-020, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- the take-on step of `AssetDisposalWorkflow` on `rwb-asset` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` (Temporal and Drools Design slides 12 and 13);
- the evaluation of R-DIS-02 on the registered transfer, with the DISPOSAL package version in force; R-DIS-01 and R-DIS-03 are tabled in §8 as the sibling routes' rules;
- the `asset` row in `rwb_asset` with the columns DF-COL-028 to DF-COL-042, `transfer_in_type` = `DEED_IN_LIEU` and `book_value` carrying the opening book value;
- the local decision record written before the row changes (DP-03), the `AssetTakenOn` outbox row (event 22) and the case-move answer;
- the two reads behind SCR-21 and SCR-22 on `/api/recovery/asset/v1` through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shapes and the fakes, which are RWB-S5-E3020-CON; the deed in lieu agreement, its settlement figures and the registration, which are rwb-treatment's (S2); the case and its route states, which are rwb-case's (P3); the ACE NPA asset and collateral facts, which are rwb-source-data's (P1); the Land Office step, the holding clocks, the money and the deployment, which are the officer, RWB-S5-E3023-APP, rwb-payment (P8) and the operations story of this key.

### 2. Business rationale

The FSD keeps the legacy objective and metric unchanged: the NPA sales cycle is measured on the decision log and the Workbench records, reviewed monthly, and moves from 1,486 days to a target of 1,095 days (FSD S5 A2.2.1). The program requirement behind it is REQ-S5-001, "Every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step" (Business Requirements Program v4); the split plan carries no requirement id for this slice (GAP-2845; ASM-4710).

What D-RCV-60 changes is who owns the agreement, the asset record and the case. In the monolith the take-on wrote the asset row, the case stage and the decision log row in one schema and one process. In the target:

- **the agreement is rwb-treatment's (S2).** The registered transfer arrives on its contract, one hop with a 2 s budget; that row is a C dependency in fact that the plan's C row does not carry (GAP-2840; ASM-4705).
- **the asset record is this service's.** `asset` is S5's record in `rwb_asset` (TSD S5 T3.1; Architecture v5 slides 19 and 41) although the Ownership Map table list names only `listing` and `asset_sale` (GAP-2841; ASM-4706).
- **the ACE facts are rwb-source-data's (P1).** The legacy data names `v_ace_npa_asset` and `v_ace_collateral`; only rwb-source-data reads the 30 `v_ace_*` views, so DP-05 applies as a prohibition (GAP-2842; ASM-4707).
- **the case is rwb-case's (P3).** This story answers the move to `ASSET_ON_BOOKS` with the rule and its version and writes no case row (GAP-2844; ASM-4709).
- **the decision is recorded first**, through the local decision-record library, which is what legacy AC1 states and legacy AC4 tests.
- **the event leaves from the outbox** on `rwb.asset.events.v1`, with rwb-case and rwb-payment as its consumers.

No business value moves: the lists `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN` and `LOV-HOLDING`, the one-working-day target of R-DIS-02 and the book value rule are reference data and rule rows read with their version, never constants of the build.

### 3. Preconditions

- RWB-S5-E3020-CON is published: the two reads, the `asset` element, the `AssetTakenOn` envelope, the consumed rows, the error set and the fakes are baselined.
- `RWB-S2-E3012-CON` "Run a deed in lieu to ownership transfer" is published with its fake, so the registered transfer can be read on Day 1 (GAP-2840; ASM-4705).
- The rwb-source-data data-product contract of DP06 Collateral and assets is available with its fake; its operation name is Not specified in the source documents (GAP-2842; ASM-4707).
- The rwb-case state read and the case-move answer are available for the fake; no source names a published move operation (GAP-2844; ASM-4709).
- RWB-PLT-E1027-CON is published with its writer fake: the record is written in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-22 reach this service through the composite route, one hop each (DP-19).
- `asset` exists in `rwb_asset` from the DB story of the service, with the columns of DF-COL-028 to DF-COL-042 and the standard record columns of TSD S5 T3.0; this story adds no table, no column and no migration.
- The DISPOSAL rule package is in force at its version with R-DIS-01, R-DIS-02 and R-DIS-03; it is authored and approved in rwb-decision (P7) and loaded on `RulePackageInForce`.
- The service runs as its own login on `rwb_asset` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a boundary test that reaches one fails the build (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the baseline is tagged by RWB-S5-E3020-CON when its tests pass.

### 4. Flow

1. The deed in lieu agreement of the case reaches its registered transfer in rwb-treatment; the agreement, its figures, the registration and any reversal stay there (FSD S5 A2.2.2).
2. The take-on step of `AssetDisposalWorkflow` on `rwb-asset` receives the fact for a case in `ASSET_PENDING_TAKE_ON` and reads the registered transfer on the S2 contract: case reference, agreement reference, property reference, transfer registered date and the agreed opening book value (GAP-2840; ASM-4705).
3. The step reads the ACE NPA asset and collateral facts of the case on the rwb-source-data data product: asset reference, asset code, asset type, segment, taken-on date and collateral reference (GAP-2842; ASM-4707).
4. The step reads the case state on the rwb-case contract to confirm `ASSET_PENDING_TAKE_ON` (GAP-2844; ASM-4709).
5. `AssetTakeOnEvaluator` loads the DISPOSAL package version in force and evaluates R-DIS-02 on the fact. Where no rule fires, the step changes nothing and reports the reason to the parent.
6. `AssetDecisionRecordWriter` writes one decision record through the local library, **before any change**: case, asset and agreement references, rule ID with its version, inputs reference, outcome and case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
7. `AssetTakeOnWriter` inserts the `asset` row in one `rwb_asset` transaction with the record, the outbox row and the idempotency row: `id`, `case_id`, `collateral_id`, `asset_ref`, `asset_code`, `asset_type` (a property value of `LOV-ASSET-TYPE`), `transfer_in_type` = `DEED_IN_LIEU`, `from_segment`, `transfer_in_date` (the registered date), `book_value` (the opening book value), `auction_purchase_price` empty, `stock_date`, `holding_status` = `HELD`.
8. The outbox writer publishes `AssetTakenOn` on `rwb.asset.events.v1` in the same transaction: case, asset reference, asset type, transfer-in type, taken-on date and rule version, with no personal data.
9. `CaseMoveAnswer` answers rwb-case with `ASSET_ON_BOOKS`, the rule ID, the version and the decided-at time; rwb-case writes the case row and the route state.
10. A repeated fact for the same case, agreement and transfer date writes nothing, publishes no second event and sends no second answer; the repeat is counted.
11. Where S2 reports a reversal, the step records the reversal and answers no move; no `asset` row is deleted.
12. SCR-21 and SCR-22 read the asset, its holding status and its book value from this service through the composite route, read only, next to the case state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing is written: no asset row, no event, no case-move answer | MSG-P7-003 | AC4, TC-E3-020-04, TC-E3-020-06 |
| X2 | The role lacks the Asset and disposal right of the operation | 403 before any read or write; nothing changes | MSG-P4-002 | AC1, TC-E3-020-05 |
| X3 | The case is not in `ASSET_PENDING_TAKE_ON` | 409 and nothing is written; the take-on is not re-evaluated | None | AC2, AC3 |
| X4 | S2 reports the transfer as not registered, or reports a reversal | Nothing is written and no move is answered; the reason goes to the parent | None | AC2 |
| X5 | An S2, rwb-source-data or rwb-case call does not answer inside 2 s, or its breaker is open | The step retries on the workflow schedule; nothing is written; the caller sees 503 with the platform error envelope | None | AC1, AC3 |
| X6 | The ACE data product is stale after a late or failed batch | The step holds, writes nothing and shows the data date; it resumes on the next fresh answer | MSG-P1-001 | AC1, AC3 |
| X7 | A row already exists for the case and the asset reference | One row, one event, one answer; the repeat is counted | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, another service's schema or a `recovery_case` row | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | §17, BR3, BR5 |

X1 to X4 are the legacy exception paths carried onto the split; X5 to X7 come from the target call types and the take-on fact; X8 is the DP-01 and DP-05 boundary. The one-working-day target of R-DIS-02 is a value in force, not a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3020-CON, the S2, rwb-source-data and rwb-case fakes and the decision-record stub, on its own schema |
| Negotiable | The activity name, the decision code and the stage-outcome shape are this story's choice; the rules, messages, screens, reads and `asset` columns are fixed |
| Valuable | A property taken in satisfaction of a debt is on the books at its agreed book value on the day the transfer registers |
| Estimable | One workflow step, one evaluator, one record write, one row insert, one event, one answer, three clients and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic case, agreement and ACE asset facts through the fakes, plus the access and failed-record paths |

### 7. Acceptance criteria

```gherkin
Feature: Take a property onto the books after a deed in lieu

  Background:
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-01, R-DIS-02 and R-DIS-03
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Take a property onto the books after a deed in lieu (legacy RWB-E3-020 AC1)
    Given the rwb-treatment contract mock returns the registered deed in lieu transfer of the case
    Given the rwb-source-data contract mock returns the ACE NPA asset and collateral facts of the case
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then creates the asset record when a deed in lieu transfer completes
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-02 (legacy RWB-E3-020 AC2)
    Given the rwb-treatment contract mock returns the registered deed in lieu transfer with the opening book value
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON"
    Given a case in state ASSET_PENDING_TAKE_ON
    When dil transfer registered
    Then create the asset record from AMIS with the opening book value
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC3 Rule R-DIS-01 (legacy RWB-E3-020 AC3)
    Given the rwb-source-data contract mock returns the repossession result with the statutory notice proved
    Given the rwb-case contract mock returns the case state "ASSET_PENDING_TAKE_ON"
    Given a case in state ASSET_PENDING_TAKE_ON
    When repossession completed
    Then create the asset record from RPS with condition, photographs and location
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded (legacy RWB-E3-020 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria word for word with their origin tag added and nothing else changed: the repeated `Then`, `its trigger arrives`, `dil transfer registered`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 carry the `Given the <service> contract mock returns <x>` lines, which are the only additions. AC3 is the vehicle criterion that RWB-E3-020 also carries: it is kept verbatim and its behaviour belongs to RWB-S5-E3019-APP (GAP-2839; ASM-4704).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-02 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | DIL_TRANSFER_REGISTERED | asset_type = property and transfer registered | Create the asset record from AMIS with the opening book value | ASSET_ON_BOOKS | Sale officer | AMIS, the Land Office | 1 working day |

The row is copied character for character from the Business Rules and Routing Logic v4. Its owner column is a business role and not a service: the case move is written by rwb-case on this story's answer and the asset row is written here. R-DIS-01 and R-DIS-03 are the other two take-on routes of the same step: R-DIS-01 belongs to RWB-S5-E3019-APP and R-DIS-03 to RWB-S5-E3021-APP, and the AMIS and Land Office systems of the row are reached through rwb-treatment and rwb-source-data, never directly.

| ID | Rule | Source |
|---|---|---|
| BR1 | The `asset` record is this service's: reference, types, dates, book value and holding status are columns of `asset` in `rwb_asset` | TSD S5 T3.1; Architecture v5 slides 19 and 41; ASM-4706 |
| BR2 | The decision is recorded before the row changes, with the rule ID and package version in force; a failed write changes nothing | DP-03; TSD S5 T2; legacy AC1 and AC4 |
| BR3 | The agreement stays with rwb-treatment: this story writes no `treatment` row and takes the registered transfer on the S2 contract only | Architecture v5 slide 41; GAP-2840 |
| BR4 | The ACE asset and collateral facts stay with rwb-source-data: no `v_ace_*` view and no ACE table is read here | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2842 |
| BR5 | The case move is answered and not written: `recovery_case` is rwb-case's | GAP-2844 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id`, `collateral_id` and the agreement reference are other services' identifiers | DP-01; TSD S5 T3.3 |
| BR7 | Every value a business person may change is reference data or a rule row read with its version: asset types, `DEED_IN_LIEU`, segments, holding status and the book value rule | TSD S5 T3.2; FSD S5 BR-S5-002; legacy Guardrails |
| BR8 | One event per confirmed take-on, written in the same transaction as the row, carrying identifiers, codes, dates and the rule version only | Architecture v5 slide 19 OUT; GAP-2843 |
| BR9 | The same fact twice, or the same `Idempotency-Key` twice, writes once, publishes once and answers once | TSD S5 T-A.2 |
| BR10 | No person name, address, contact value or identity number enters `rwb_asset`, the record, a log or an event | §R7.2 s17; Architecture v5 slide 42 notes |

### 9. State transitions

The case route state is rwb-case's: this story answers the move and the parent applies it (BR5). What it owns is the holding status of the asset and the state of the step.

| From (`asset.holding_status`) | Event | Condition | To |
|---|---|---|---|
| None, no row | The registered transfer under R-DIS-02 | asset_type = property and transfer registered | A row in `HELD` with `DEED_IN_LIEU` and the opening book value, and the move `ASSET_ON_BOOKS` |
| None, no row | A transfer S2 reports as not registered or reversed | X4 | No row, no record, no answer |
| HELD | A second fact for the same agreement and date | X7 | Unchanged, the repeat is counted |
| HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED, RENTED | A take-on fact for an asset that already has a row | X7 | Unchanged, the repeat is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The registered transfer arrives for a case in `ASSET_PENDING_TAKE_ON` | The package in force is loaded | Evaluating |
| Evaluating | R-DIS-02 fires | The decision record is written | Applying |
| Applying | Row, outbox row and answer are written | The transaction commits | Waiting for the next fact |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |

`ASSET_PENDING_TAKE_ON` and `ASSET_ON_BOOKS` are the DISPOSAL states of TSD S5 T4 and live on the case of record; the holding values are those of `LOV-HOLDING`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA (TSD S5 T6.1): the primary role of the feature, holding C, R, U and A |
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU: reads the asset, corrects the take-on facts |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the asset where the deed in lieu follows enforcement |
| The 23 roles of TSD S5 T6.1 that hold R | Read only, in scope |
| RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | RA: read, and approve where a book value or a floor needs it |
| PT-VALUER, PT-AUCTION, PT-RAMC, SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | The rights the matrix gives them; the service identities run the step under the same checks |
| rwb-asset service identity | Runs the step, evaluates the rule, writes the record and the row, publishes the event and answers the move; no grant on another schema |

The rights are the rows of TSD S5 T6.1 and nothing wider. The FSD says the feature runs unattended with the sale officer as also-user; both hold, because the step runs under the service identity and the officer acts on SCR-22 and on the correction paths. DP-08 is not in this story's pattern set: the capability area and right are declared per operation.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-028 | asset (S5, `rwb_asset`) | id | Write, the asset reference of the row, the event and the answer |
| DF-COL-029 | asset (S5) | case_id | Write, from the case reference |
| DF-COL-030 | asset (S5) | collateral_id | Write, from the ACE collateral reference |
| DF-COL-031 | asset (S5) | asset_ref | Write, from the ACE NPA asset |
| DF-COL-032 | asset (S5) | asset_code | Write, from the ACE NPA asset |
| DF-COL-033 | asset (S5) | asset_type | Write, against `LOV-ASSET-TYPE` (a property value on this route) |
| DF-COL-034 | asset (S5) | transfer_in_type | Write, against `LOV-TRANSFER-IN` (`DEED_IN_LIEU`) |
| DF-COL-035 | asset (S5) | from_segment | Write, against `LOV-SEGMENT` |
| DF-COL-036 | asset (S5) | transfer_in_date | Write, the registered transfer date |
| DF-COL-037 | asset (S5) | book_value | Write, the opening book value of the agreement |
| DF-COL-038 | asset (S5) | auction_purchase_price | Not written on this route |
| DF-COL-039 | asset (S5) | repossessed_date | Written where the ACE fact gives it; empty on a deed in lieu |
| DF-COL-040 | asset (S5) | stock_date | Write, the date the property enters stock |
| DF-COL-041 | asset (S5) | holding_status | Write, against `LOV-HOLDING` (`HELD`) |
| DF-COL-042 | asset (S5) | holding_cost_to_date | Not written here: RWB-S5-E3023-APP writes it |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, in `rwb_asset`) | rule id, version, inputs reference, outcome, decided at | Write through the library, before the row changes |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset`, `v_ace_collateral` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, segment, book_value, collateral_id | Not read: no `v_ace_*` grant; the facts arrive on the data product (BR4) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code, route state | Not read as a table: the state arrives on the rwb-case answer |

Field IDs are those of TSD S5 T3.1 and the Logical Data Model v8; the agreement reference has no field id in any source and travels as a fact of the S2 answer (GAP-2840; ASM-4705). **No new table, no new column, no migration**: `asset` arrives with the DB story, this story writes fifteen existing columns, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_asset` by the library's own migration.

**No personal data.** The rows carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters the schema, the record, a log, an event or a workflow input; every fixture is synthetic and the property address stays an ACE fact.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the two reads whose shapes RWB-S5-E3020-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with title, condition, valuations, costs and listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

Errors are 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503. `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds` belong to the listing and pricing stories of this service.

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use |
|---|---|---|---|
| The transfer read of `RWB-S2-E3012-CON` (operation name Not specified in the source documents (GAP-2840; ASM-4705)) | `/api/recovery/treatment/v1` | S2 rwb-treatment | The registered deed in lieu transfer, its date, its opening book value and the reversal state; faked |
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2842; ASM-4707)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE NPA asset and collateral facts with the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the account link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2844; ASM-4709)) | rwb-case (P3) | P3 rwb-case | `ASSET_ON_BOOKS` with the rule and its version; on the workflow boundary it is the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The rows are class C dependencies in fact that the metadata row does not carry, and the absence is recorded as GAP-2840, -4 and -6.

#### 12.3 Events published

| Event | Topic | Payload | Consumers | When |
|---|---|---|---|---|
| `AssetTakenOn` (`rwb.asset.AssetTakenOn.v1`) | `rwb.asset.events.v1` | Case, asset reference, asset type, transfer-in type `DEED_IN_LIEU`, taken-on date and the rule ID with its version; CloudEvents; no personal data | rwb-case and rwb-payment | In the transaction that inserts the row, from the outbox |

The topic carries the retry and `.dlt` topics of the platform (DP-14). The outbox is the DP-09 library, which the pattern set does not carry (GAP-2843; ASM-4708). `AssetSold` belongs to the sale stories.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none is a deed in lieu transfer; the S2 contract answers it synchronously. This story holds no consumer group and no inbox row of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: case, route, asset reference and package in force; signals: case state, package in force, approval answer |
| `takeOnAsset` | Activity, the one take-on step | `rwb-asset` | The case and registered transfer in; the rule with its version, the asset reference, the event and the case move out, with the record, the row and the outbox row in one transaction |

The activity name is a target design choice and is fixed by no source document; no child workflow exists for the agreement in this service.

#### 12.6 Schedules

None. The step runs from the registered transfer and the case signal. The service's single Schedule is JOB-19 Re-appraisal monthly, which belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`); read as S5 from TSD S5 T3.1 and Architecture v5 slides 19 and 41 while the Ownership Map names no `asset` row (GAP-2841; ASM-4706) | The taken-on property; this story inserts the row and writes the columns of §11 |
| asset_sale | S5 (`rwb_asset`), Ownership Map | Not written by this story: the sale stories |
| listing | S5 (`rwb_asset`), Ownership Map | Not written by this story: the listing and pricing stories |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated fact and the answer it holds |
| outbox_event | PLT library, created in `rwb_asset` | The `AssetTakenOn` row relayed to `rwb.asset.events.v1` (DP-09) |

Never read as a table: `treatment` (S2), `recovery_case` and `assignment` (P3), `collateral` and every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7). No foreign key leaves the schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-treatment transfer fake (`RWB-S2-E3012-CON`) | A registered transfer with its date and opening book value; a transfer not registered; a reversal; no answer beyond 2 s | AC1, AC2, X4, X5 |
| rwb-source-data data-product fake | The ACE NPA asset and collateral facts; a stale product with its date; no answer beyond 2 s | AC1, AC3, X6 |
| rwb-case state and move fake | `ASSET_PENDING_TAKE_ON` and `ASSET_ON_BOOKS`; an accepted and a refused move | AC1, AC2, AC3, X3 |
| rwb-decision rule-package fake | The DISPOSAL package at its version with R-DIS-01, R-DIS-02 and R-DIS-03 | AC1, AC2, AC3 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| Outbox relay stub (`RWB-PLT-TE006-CON`) | A relayed `AssetTakenOn` and a relay that fails and retries | AC1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer | AC1 |

The fakes are test-only and are replaced by the real services in SIT; the operation names of the S2 read, the data-product read and the move answer carry the placeholder until their owners confirm them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two asset reads on `/api/recovery/asset/v1`; the S2 transfer read, the data-product read, the case state read and the move answer; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `AssetTakenOn` on `rwb.asset.events.v1` from the outbox |
| Temporal | 1 workflow, 1 activity | `AssetDisposalWorkflow` and its take-on step on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `takeon`; front end `src/modules/recovery/asset/AssetTakeOn.tsx`, the fragment SCR-21 and SCR-22 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies as a prohibition: the service holds no `v_ace_*` grant and reads no ACE view. DP-03 is the transaction rule of the step, DP-13 moves the base of the two reads, and DP-19 is how the screens reach the service. The outbox library of DP-09 is needed by the published event and is absent from the pattern set and from the build row (GAP-2843; ASM-4708).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` take-on branch | Workflow | Waits for the registered transfer, loads the package in force, reports the outcome to the parent |
| `takeOnAsset` | Activity | The one step: read the transfer, the ACE facts and the case, evaluate R-DIS-02, write the record, the row and the event, answer the move |
| `AssetTakeOnEvaluator` | Service | The rule evaluation against the DISPOSAL package version in force |
| `AssetDecisionRecordWriter` | Library adapter | Writes the decision record before any change and refuses the step when the write fails (DP-03) |
| `AssetTakeOnWriter` | Repository | Inserts `asset` and writes its columns in one transaction with the idempotency row and the optimistic lock |
| `AssetEventPublisher` | Outbox adapter | Writes the `AssetTakenOn` outbox row in the same transaction |
| `TreatmentTransferClient`, `SourceDataProductClient`, `CaseStateClient` | Clients | The S2 read, the data-product read and the case state and move, one hop, 2 s, breaker |
| `AssetController` | Controller | The two reads, the right, the pagination and the problem mapping |
| `AssetTakeOn` | React component | Shows the asset, its book value and its take-on state on SCR-21 and SCR-22, read only |

**Database and migrations.** No Flyway file: `asset` arrives with the DB story, and the record, key and outbox are library objects created in `rwb_asset` (DP-03, DP-09). No column is added for the agreement reference or the registered date: the reference is a fact of the S2 answer and the date is written to DF-COL-036.

**Configuration and reference data.** `LOV-ASSET-TYPE`, `LOV-TRANSFER-IN`, `LOV-SEGMENT` and `LOV-HOLDING` at their version (TSD S5 T3.2); the DISPOSAL package and its version from rwb-decision (P7); the capability area "Asset and disposal" and its rights from rwb-access. The 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The take-on branch of `AssetDisposalWorkflow` and its input record on `rwb-asset`.
2. The three clients against their fakes, with the 2 s budget, the breaker, the reversal, the stale and the no-answer paths (AC1, X4, X5, X6).
3. `AssetTakeOnEvaluator` over the DISPOSAL package with R-DIS-02 and the no-fire path (AC1, AC2).
4. `AssetDecisionRecordWriter` against the stub, with the failed-write path (AC4, X1).
5. `AssetTakeOnWriter` with one transaction, the fifteen columns, `DEED_IN_LIEU`, the book value, the idempotency row and the optimistic lock (AC2, X7).
6. `AssetEventPublisher` and the `AssetTakenOn` envelope (AC1).
7. The move answer and the parent signal (AC2, AC3).
8. `AssetController` with the rights, the pagination and the problem mapping (AC1).
9. `AssetTakeOn` and the two screens through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read, no write to `rwb_treatment`, `rwb_case` or `rwb_payment` (X8, BR3, BR4, BR6).

**Feature flag.** `rwb.asset.take-on-v1`, a flag of the platform library: off holds the transfer, writes nothing and answers no move.

**Done when.** The tests of §16 pass, the step runs from a synthetic registered transfer, R-DIS-02 produces its record, row, event and move, a repeated fact writes once, a forced record failure changes nothing, no `treatment` row and no `v_ace_*` read exist, and the screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set. It names the floor percentage and the approval limit, which are the pricing story's, so no path here raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set. It names the age of an appraisal, which is the re-appraisal story's, so no path here raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or of the fact is absent or invalid (X3, X4) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the list or the asset (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the case is stale after a late or failed batch (X6, VR-S5-002-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The six IDs are those of the legacy message set and FSD S5 A2.2.3.1, and the text is copied unchanged.

### 15. Screens and states

SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its take-on, held, listed and sold states are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its book value and its holding status, rwb-case for the case and its route state, rwb-source-data for the ACE fact and rwb-valuation for the valuation references; this story fixes the rwb-asset answers, and the route and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the take-on state of SCR-22 — the record with its transfer date, its `DEED_IN_LIEU` type and its opening book value — and the states it shows on refusal and failure: MSG-P4-002, MSG-P7-003 and MSG-P1-001. The held, listed and sold states belong to the holding, pricing and sale stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-020-01 | AC1 | Component | A synthetic registered transfer for a synthetic case; the asset row, the event and the move asserted on the fakes |
| TC-E3-020-02 | AC2 | Integration | The registered transfer with an opening book value; the row, the outbox row and the `ASSET_ON_BOOKS` move asserted end to end |
| TC-E3-020-03 | AC3 | Component | The vehicle repossession fact of the sibling route; the contract answers and no duplicate of R-DIS-01 |
| TC-E3-020-04 | AC4 | Component | The record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E3-020-05 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E3-020-06 | Principle 5 | Component | A forced record failure at the moment of the insert; no row, no event, no answer |

The six legacy cases are carried in their legacy order with the Level column added: `System` maps to `Component` on the fakes and TC-E3-020-02 to `Integration` because it crosses the rwb-treatment, rwb-source-data and rwb-case boundaries. The full test is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same IDs; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in code: the one-working-day target, the book value rule, the lists and the rule rows stay data, reference data or the rule package, never a constant or a default.
- No personal data in `rwb_asset`, in the `AssetTakenOn` payload, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only.
- The agreement stays with rwb-treatment and the ACE facts with rwb-source-data: a build that adds a `treatment` row or a `v_ace_*` read fails the boundary test (DP-01, DP-05).
- The case stays with rwb-case and the money with rwb-payment: no `recovery_case` row, no posting and no balance change is written here (BR5).
- One base, one topic, one queue and one login per service; no module or test names another service's base or topic as its own (DP-13, DP-14).
- The decision is recorded before the change and the event is written in the same transaction; a build that publishes outside the outbox fails the review (DP-03, DP-09).
- No retired element returns: no shared job table, no Quartz row, no monolith base, no second event on the topic.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-001 | Every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step (Business Requirements Program v4); the split plan allocates no id for this slice (GAP-2845; ASM-4710) | The take-on step, the `asset` row and `AssetTakenOn` | TC-E3-020-01, -02, -04 |
| ADR-013 | 19 services inside ACE | rwb-asset as owner of the asset record | TC-E3-020-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login | TC-E3-020-06 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `AssetTakenOn` outbox row | TC-E3-020-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget | TC-E3-020-02 |
| ADR-022 | Local decision record plus central ledger | The record written before the change | TC-E3-020-04, -06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-020, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E3-020-01 to TC-E3-020-06 |
| Feature and screens | FEAT-AST-02, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-02, with R-DIS-01 and R-DIS-03 tabled, from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the elements, the error set and the fakes: RWB-S5-E3020-CON.
- The deed in lieu agreement, its figures, the registration and the reversal: rwb-treatment (S2) on `RWB-S2-E3012-CON` (GAP-2840).
- The Land Office registration and the title work: officer and legal steps, with no service owner (GAP-2846; ASM-4711).
- The vehicle repossession and LED auction routes: RWB-S5-E3019-APP and RWB-S5-E3021-APP (GAP-2839).
- The holding-age clock, the provision steps and the monthly cost of carry: RWB-S5-E3023-APP, with the posting in rwb-payment (P8).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3) (GAP-2844).
- The ACE NPA asset and collateral facts and the freshness of the data product: rwb-source-data (P1) (GAP-2842).
- The valuations of the property: rwb-valuation (S1); the listing, the floor price and the auction rounds: the pricing and auction stories of this service.
- The document, its custody and its retention: rwb-document (P5).
- The composite route and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey and its evidence: the wave 2 harness. The deployment, the flag, the dashboards, the alerts and the runbook: the operations story of this legacy key.
