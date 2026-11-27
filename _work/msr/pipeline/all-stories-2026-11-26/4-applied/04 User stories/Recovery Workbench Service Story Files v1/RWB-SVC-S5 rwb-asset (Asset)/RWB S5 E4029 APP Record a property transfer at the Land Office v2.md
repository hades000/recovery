# RWB-S5-E4029-APP Record a property transfer at the Land Office

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4029-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-U |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4029-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-029 for rwb-asset. The four legacy criteria are kept word for word with their origin tag, and the six legacy test cases keep their IDs. The title transfer becomes a branch of `AssetDisposalWorkflow` on queue `rwb-asset` in namespace `rwb-recovery`: it takes the registration the officer records, releases the documents from custody on the rwb-document contract (DP-05 boundary, name not published), writes the status on `listing` and the holding status on `asset` in `rwb_asset`, records the outcome before any change through the local decision-record library (DP-03), and answers `ASSET_SOLD` to rwb-case; it publishes nothing. The Land Office itself stays a person and officer step with no service and no interface (GAP-2937; ASM-4833), and no element of the service holds the registration reference or the title status (GAP-2938; ASM-4834). AC3 owns R-DIS-02, whose behaviour is RWB-S5-E3020-APP's (GAP-2940; ASM-4836). The base becomes `/api/recovery/asset/v1` (DP-13) and SCR-21 and SCR-22 read through the gateway-bff route (DP-19). Gaps: the custody release has no published operation and the C row is empty (GAP-2939; ASM-4835); R-DIS-53 has no owner (GAP-2941; ASM-4837); the plan carries no requirement id (GAP-2942; ASM-4838); the sources are in review (GAP-2943; ASM-4839). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4029-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **to track the Land Office transfer, which stays a person and officer step**, so that **assets sell sooner at approved prices** (legacy RWB-E4-029, word for word).

This is the application slice of legacy RWB-E4-029. It owns:

- the four legacy criteria with their origin tag, and the rules, messages and screens they depend on;
- the title-transfer branch of `AssetDisposalWorkflow` on `rwb-asset`, the child of the case workflow for the disposal stage (Architecture v5 slide 13);
- the evaluation of R-DIS-52 on the registration the officer records, with the DISPOSAL package version in force; R-DIS-02 is tabled in §8 because AC3 names it (GAP-2940; ASM-4836);
- the release of the documents from custody on a document-hub operation that carries the placeholder until P5 publishes it (GAP-2939; ASM-4835);
- the status writes of this step in `rwb_asset`: `listing.status` and `asset.holding_status` set to the sold value of their lists, in one transaction with the record and the idempotency row (GAP-2938; ASM-4834);
- the decision record of the outcome before the change (DP-03) and the case answer `ASSET_SOLD` with the rule and its version;
- the reads of SCR-21 and SCR-22 on `/api/recovery/asset/v1` through the gateway-bff route (DP-13, DP-19).

It does not own: the published shapes and the fakes, which are RWB-S5-E4029-CON; the payment term, the award and the confirmation that starts the title transfer, which are FEAT-AST-18's story (R-DIS-47 to R-DIS-49); the vehicle registration through SCIS, FEAT-AST-19's story (R-DIS-51); the take-on of the property after a deed in lieu, which is RWB-S5-E3020-APP (R-DIS-02); the rejection of a transfer and its blocked title (R-DIS-53) (GAP-2941; ASM-4837); the documents, their custody and their retention, rwb-document (P5); the case and its route states, rwb-case (P3); the proceeds and their posting, rwb-payment (P8) and FEAT-AST-21's story; the rule package, rwb-decision (P7); the deployment, the operations story of this key.

### 2. Business rationale

Legacy RWB-E4-029 tracked the last person step of a property sale: after the buyer paid, the title moved at the Land Office and the asset left the stock only when the registration was in hand. The FSD keeps it as FEAT-AST-20 in module S5, run by the sale officer with Legal counsel as the second user, between the payment term of FEAT-AST-18 and the proceeds of FEAT-AST-21 (FSD S5 A2.20.2). The metric is unchanged: the NPA sales cycle moves from 1,486 days to a target of 1,095 days, measured on the decision log and the Workbench records, reviewed monthly (FSD S5 A2.20.1). R-DIS-52 allows ten working days for the step.

What D-RCV-60 changes:

- **the step is this service's case branch.** `AssetDisposalWorkflow` on `rwb-asset` receives the registration, evaluates the rule and writes the status of the asset and of its listing; the case state stays with rwb-case (DP-13, DP-19).
- **the registration itself stays outside every service.** The feature says so in one sentence, and no integration id, no operation and no system row models the Land Office; the officer's act is a case task and the registration reference has no element in `rwb_asset` (GAP-2937, GAP-2938; ASM-4833, ASM-4834).
- **the custody release crosses one boundary.** The legacy `document` and `document_custody` rows are rwb-document's; this story calls its release operation with an idempotency key and never reads those tables (DP-05; GAP-2939).
- **the decision is recorded first**, one per registration, in the row's transaction — what AC1 asked and AC4 tested.
- **nothing is published.** EV-22 `AssetTakenOn` is the take-on story's, and the sale event is not in any source for this step; §12.3 states the absence and a build that publishes here fails it.

### 3. Preconditions

- RWB-S5-E4029-CON tagged: the two reads, the status writes, the consumed rows, the decision-record and rule-package elements, the error set and the fakes.
- `asset`, `asset_sale` and `listing` exist in `rwb_asset` with the TSD S5 T3.1 columns and the standard record columns of T3.0; the DB story creates them and this story adds no table, no column and no migration (GAP-2938; ASM-4834).
- The DISPOSAL package is in force at its version with R-DIS-52 and R-DIS-02, authored in rwb-decision (P7) and loaded through the service template.
- The officer's registration arrives as the `TITLE_REGISTERED` signal of `AssetDisposalWorkflow`, recorded on the case task in rwb-case; no operation and no interface exist for it (GAP-2937; ASM-4833).
- The rwb-document release operation is baselined with its fake; its name is Not specified in the source documents (GAP-2939; ASM-4835).
- The rwb-case state read and the case-move answer are behind fakes; no source publishes their names.
- The `LOV-HOLDING`, `LOV-LISTING` and `LOV-ASSET-TYPE` lists are reference data with their version (TSD S5 T3.2).
- RWB-PLT-E1027-CON writes in the caller's transaction (DP-03); RWB-PLT-N001-CON serves the two screens, one hop each (DP-19).
- The service holds its own login on `rwb_asset`, no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-05).
- The sources of the slice are In review with empty sign-off tables; both stories stand at Draft and no approval is needed to build against a Draft baseline (GAP-2943; ASM-4839).

### 4. Flow

1. R-DIS-48 in the payment story has confirmed the sale and started the title transfer; the case is in `TITLE_TRANSFER_PENDING` and the asset is held or sold in its listing.
2. The sale officer registers the transfer at the Land Office outside the Workbench, receives the registered title and records it on the case task; no service calls the Land Office (GAP-2937; ASM-4833).
3. `AssetDisposalWorkflow` on `rwb-asset` wakes on the `TITLE_REGISTERED` signal, which carries the case reference, the asset reference, the registration date and the reference the officer entered.
4. The step confirms `TITLE_TRANSFER_PENDING` on the rwb-case contract and reads the asset and its sale from `rwb_asset`: asset type, holding status, the listing and its status, and the `asset_sale` row of the case (GAP-2938; ASM-4834).
5. `TitleTransferEvaluator` loads the package in force and evaluates R-DIS-52: from `TITLE_TRANSFER_PENDING`, on `TITLE_REGISTERED`, with `asset_type` a property value, release the documents from custody and record the transfer. Where no rule fires the step changes nothing and reports the reason to the parent (X3, X6).
6. `AssetDecisionRecordWriter` writes one record **before any change**: case, asset, listing, rule ID with its version, the registration date and reference as the inputs reference, the outcome and the case move. A failed write stops the step (DP-03; AC1, AC4).
7. The step calls the rwb-document release with the asset and document-custody scope and an idempotency key derived from the case, the asset and the registration date; the call is one hop with a 2 s budget and a breaker. It answers "released" or refuses; a refusal or a timeout leaves nothing committed and the workflow retries (X4).
8. `TitleTransferWriter` writes the status of the listing and the holding status of the asset in one `rwb_asset` transaction with the record and the idempotency row, under the optimistic lock: `listing.status` takes the sold value of `LOV-LISTING` and `asset.holding_status` takes the sold value of `LOV-HOLDING` (GAP-2938; ASM-4834).
9. `CaseMoveAnswer` answers rwb-case with `ASSET_SOLD`, the rule ID, the version and the decided-at time; rwb-case writes the case and its route state.
10. A repeated registration for the same case, asset and date writes nothing, releases nothing and sends no second answer; the repeat is counted (X5).
11. A registration rejected at the Land Office is not this branch: R-DIS-53 holds the transfer and blocks the title (GAP-2941; ASM-4837).
12. SCR-21 and SCR-22 read the asset, its holding status and the status of its listing from this service through the composite route, read only; the workflow returns to its durable timer and continues as new at the stage end and at least every 28 days.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record cannot be written | Nothing written, nothing released, no move answered; the statuses stay as they were | MSG-P7-003 | AC4, TC-E4-029-04, TC-E4-029-06 |
| X2 | The role lacks the Asset and disposal right | 403 before any read or write | MSG-P4-002 | AC1, TC-E4-029-05 |
| X3 | The case is not in `TITLE_TRANSFER_PENDING` | The rule does not fire; nothing written; the state is reported to the parent | None | AC2 |
| X4 | The custody release refuses, or does not answer inside 2 s, or its breaker is open | Nothing committed; the step retries on the workflow schedule; the caller sees 503 in the platform envelope | None | AC2 |
| X5 | The same registration arrives twice, or the same key twice | One release, one write, one answer | None | AC1 |
| X6 | The asset type is a vehicle, not a property | R-DIS-52 does not fire; the vehicle path is R-DIS-51 on FEAT-AST-19's story | None | AC2 |
| X7 | A required element of the registration or of a request is absent or invalid | 422 with the field named; nothing written | MSG-GEN-001 | AC1 |
| X8 | A statement reaches a `v_ace_*` view, `recovery_case`, `document`, `document_custody` or a foreign schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | §17, BR6 |
| X9 | The Land Office rejects the transfer | Held for R-DIS-53, which no story of this split owns; the branch writes nothing | None | GAP-2941 |

X1 to X3 are the legacy paths carried onto the split, X4 to X7 come from the one boundary the step crosses and the shape of its input, X8 is the DP-01 and DP-05 boundary and X9 is the rule the split leaves without an owner.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the CON baseline and the rwb-case, rwb-document and rwb-decision fakes; no live P3 or P5 |
| Negotiable | Activity name, decision code and signal shape are ours; the rules, messages, screens, statuses and reads are fixed |
| Valuable | The asset leaves the stock on the day the title registers, and the officer's step is tracked without a paper chase |
| Estimable | One branch, one evaluator, one record per registration, one boundary call, two status writes, one answer, two read-only screen fragments |
| Small | Two weeks with its tests on the fakes |
| Testable | Each criterion on synthetic cases through the fakes, plus the access, wrong-state, refused-release, repeat and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Record a property transfer at the Land Office

  Background:
    Given case "RC-2026-000591" holds property asset "AST-2026-000591" in listing "LS-2026-000591"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-52 and R-DIS-02
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Record a property transfer at the Land Office (legacy RWB-E4-029 AC1)
    Given the rwb-case contract mock returns the case "RC-2026-000591" in state TITLE_TRANSFER_PENDING
    Given the rwb-document contract mock returns the documents of asset "AST-2026-000591" held in custody
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then tracks the Land Office transfer, which stays a person and officer step
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-52 (legacy RWB-E4-029 AC2)
    Given the rwb-case contract mock returns the case "RC-2026-000592" in state TITLE_TRANSFER_PENDING
    Given the rwb-document contract mock returns the documents of asset "AST-2026-000592" held in custody
    Given a case in state TITLE_TRANSFER_PENDING
    When title registered
    Then release the documents from custody and record the transfer at the Land Office
    Then the case moves to ASSET_SOLD

  Scenario: AC3 Rule R-DIS-02 (legacy RWB-E4-029 AC3)
    Given the rwb-treatment contract mock returns the registered deed in lieu transfer of the property with the opening book value
    Given the rwb-case contract mock returns the case "RC-2026-000593" in state ASSET_PENDING_TAKE_ON
    Given a case in state ASSET_PENDING_TAKE_ON
    When dil transfer registered
    Then create the asset record from AMIS with the opening book value
    Then the case moves to ASSET_ON_BOOKS

  Scenario: AC4 Not recorded (legacy RWB-E4-029 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria word for word with the origin tag added: the repeated `Then`, `the user acts on the screen`, `title registered`, `dil transfer registered` and `the decision log cannot be written` stand, and the `Given the <service> contract mock returns <x>` lines are the only additions. AC2's release and the case move happen in three places: rwb-document releases the documents, rwb-case writes the move to `ASSET_SOLD`, and this story evaluates the rule, writes the statuses, records and answers. AC3 is R-DIS-02, whose asset record is created by RWB-S5-E3020-APP; here it is asserted at the take-on boundary and not built twice (GAP-2940; ASM-4836).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-52 | Asset disposal | D8.1 to D8.3 | TITLE_TRANSFER_PENDING | TITLE_REGISTERED | asset_type = property | Release the documents from custody and record the transfer at the Land Office | ASSET_SOLD | Sale officer | the Land Office, Document Hub | 10 working days |
| R-DIS-02 | Asset disposal | D8.1 to D8.3 | ASSET_PENDING_TAKE_ON | DIL_TRANSFER_REGISTERED | asset_type = property and transfer registered | Create the asset record from AMIS with the opening book value | ASSET_ON_BOOKS | Sale officer | AMIS, the Land Office | 1 working day |

Both rows are copied character for character from the Business Rules and Routing Logic v4. Their owner column is a business role, so the case moves in rwb-case on this story's answer while the statuses, the record and the release are handled here. The Land Office in the systems column stays a person and officer step with no interface (GAP-2937; ASM-4833). R-DIS-53, R-DIS-54 and R-DIS-55 are FEAT-AST-21's and the rejection's; R-DIS-47 to R-DIS-49 are FEAT-AST-18's; R-DIS-51 is FEAT-AST-19's.

| ID | Rule | Source |
|---|---|---|
| BR1 | The status of the listing and the holding status of the asset are this service's: they are written here on the values of `LOV-LISTING` and `LOV-HOLDING`, in `rwb_asset` | TSD S5 T3.1, T3.2; GAP-2938 |
| BR2 | The record precedes the change, one per registration, with the rule and package version; a failed write changes nothing | DP-03; AC1, AC4 |
| BR3 | The Land Office is never called: the registration enters as the officer's signal and the service holds no interface, no file and no screen for it | GAP-2937; ASM-4833 |
| BR4 | The documents and their custody stay with rwb-document: one release call with an idempotency key, no read of `document` or `document_custody` | DP-05; GAP-2939 |
| BR5 | The case move is answered, not written; `recovery_case` and `assignment` are rwb-case's | TSD S5 T3.3; GAP-2938 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_asset` | DP-01; TSD S5 T3.3 |
| BR7 | Every value a business person may change is rule data or reference data with a version: the ten working days, the statuses and the asset types | FSD S5 BR-S5-020; TSD S5 T3.2 |
| BR8 | No event is published: EV-22 `AssetTakenOn` is the take-on story's and no source gives this step one | TSD S5 T5.3 |
| BR9 | A repeated registration or key writes once, releases once and answers once | TSD S5 T-A.2 |
| BR10 | No personal data in a row, a record, a log or a workflow input; a buyer is a code and the property address stays an ACE fact | §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is applied by the parent `CaseWorkflow` on this story's answer (BR5).

| From (case state) | Event | Condition | To |
|---|---|---|---|
| TITLE_TRANSFER_PENDING | `TITLE_REGISTERED` under R-DIS-52 | `asset_type` is a property value | ASSET_SOLD, answer `ASSET_SOLD` |
| ASSET_PENDING_TAKE_ON | `DIL_TRANSFER_REGISTERED` under R-DIS-02 | Property and transfer registered | ASSET_ON_BOOKS, built by RWB-S5-E3020-APP and asserted here |
| Any | A registration in another state, a vehicle, or a repeat | X3, X6, X5 | Unchanged, no answer |

| `listing.status` | Event | Condition | To |
|---|---|---|---|
| Live or under offer | The registration is recorded | R-DIS-52 fires and the release answered | SOLD |
| Any | The state is wrong, the type is a vehicle, or the release refuses | X3, X4, X6 | Unchanged |

| `asset.holding_status` | Event | Condition | To |
|---|---|---|---|
| HELD, LISTED, UNDER_OFFER or SOLD | The registration is recorded | R-DIS-52 fires | The sold value of `LOV-HOLDING`, written in the same transaction |
| Any | The record or the transaction fails | X1 | Unchanged |

The status values are the `LOV-LISTING` and `LOV-HOLDING` rows of TSD S5 T3.2 and the states are the DISPOSAL machine's (TSD S5 T4). The registration reference and the title status have no element of their own (GAP-2938; ASM-4834).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA (TSD S5 T6.1): the primary role of the feature; records the registration on the case task and reads the asset |
| RW-LEGAL, legal counsel | Asset and disposal R: the second user of the feature, reads the asset, its listing and its status |
| RW-NPAMGR, RW-ENFORCE | Asset and disposal CRU: read, and correct a registration recorded in error |
| The further roles of the legacy read row and of TSD S5 T6.1 that hold R | Asset and disposal R, in scope |
| RW-HEADNPA, RW-HEADASL, RW-PRODHEAD | Asset and disposal RA: read, and approve where a sale-level limit is involved |
| SY-CASEWF, SY-RULES | The matrix's right, under the same checks as a person |
| rwb-asset service identity | Runs the branch, evaluates the rule, writes the statuses and records; no grant on another schema and no `v_ace_*` grant |

The rights are the legacy permission table and the rows of TSD S5 T6.1, nothing wider: the legacy table gives the capability area R to the 30 roles of the read row and C to RW-ENFORCE, RW-SALEOFF, RW-NPAMGR and SY-DATALOAD, and the matrix adds the officer's write through RW-SALEOFF CRUA and RW-NPAMGR CRU. DP-08 is not in the pattern set: the right is declared per operation and the guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-028 to DF-COL-042 | asset (S5, `rwb_asset`) | id, case_id, asset_ref, asset_type, transfer_in_type, transfer_in_date, book_value, holding_status and 7 more | Read: asset_type and the sale link; write: `holding_status` |
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_key, sale_channel, start_price, floor_price, round_no, listed_at, status | Read: the listing of the asset; write: `status` |
| DF-SAL-009 to DF-SAL-019 | asset_sale (S5, `rwb_asset`) | id, asset_key, listing_id, contract_date, sale_date, sale_price, transfer_fee and 6 more | Read: the sale of the case; not written here |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the library, before the change |
| Not specified in the source documents (GAP-2938; ASM-4834) | none | the title status, the Land Office registration date and reference | No element; the reference rides in the record and the date in the workflow input |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and 19 more | Not read as a table: the state arrives on the rwb-case answer |
| DF-WRK-009 to DF-WRK-016 | assignment (P3) | id, case_id, task_id, assignee_user_id and 5 more | Not read: the officer's task is rwb-case's |
| DF-DOC-001 to DF-DOC-011 | document (P5) | id, case_id, document_type, storage_ref and 7 more | Not read: released through the rwb-document operation |
| DF-DOC-018 to DF-DOC-024 | document_custody (P5) | id, document_id, moved_at, from_location, to_location, held_by and 2 more | Not read: released through the rwb-document operation |
| DF-ACE-220 to DF-ACE-230 | `v_ace_npa_sale` (P1) | npa_sale_key, npa_asset_key, contract_date, sale_date, sale_price, transfer_fee and 5 more | Not read: no `v_ace_*` grant; `asset_sale` already carries the AMIS sale facts (BR4) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 10 more | Not read or written: rwb-decision |

Field IDs follow TSD S5 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no column, no migration**: the tables come with the DB story and `decision_record` and `idempotency_key` are library objects in `rwb_asset` (DP-03). **No personal data**: identifiers, codes, dates, amounts and a rule version only; every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the shapes of RWB-S5-E4029-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the holding status and the listing status of each asset (API-S5-001) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out with its title, its sale, its holding status and the status of its listing (API-S5-002) | Asset and disposal, R, scope applied | Not applicable |

No write operation is declared: the officer's registration is a case task and enters as a workflow signal, because no source gives the step an operation (GAP-2937; ASM-4833). `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's and `POST /assets/{assetId}/listings` (API-S5-004) is the pricing story's. Errors: 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001, 503 when a library or a contract does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state before the rule fires; faked |
| The case-move answer (name Not specified in the source documents (GAP-2939; ASM-4835)) | rwb-case (P3) | P3 rwb-case | `ASSET_SOLD` with the rule and its version; on the workflow boundary it is the stage outcome the parent applies; faked |
| The document custody release (name Not specified in the source documents (GAP-2939; ASM-4835)) | `/api/recovery/document/v1` | P5 rwb-document | The release of the documents of the asset, with an idempotency key, in place of the legacy `document_custody` write (DP-05); faked |

Three rows, one hop each, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). The custody release is a class C dependency in fact that the plan's empty C row does not carry (GAP-2939; ASM-4835).

#### 12.3 Events published

None. EV-22 `AssetTakenOn` is the take-on story's (TSD S5 T5.3) and no source gives the title transfer an event; the branch writes no outbox row and adds nothing to `rwb.asset.events.v1`. A build that publishes here fails the absence test.

#### 12.4 Events consumed

None. The registration, the case state and the package in force arrive as signals of `AssetDisposalWorkflow`; the branch adds no consumer group and no inbox row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one per case per stage, continues-as-new across the holding | `rwb-asset` in `rwb-recovery` | Input: case, route, asset, listing, package in force; signals: registration recorded, case state, package in force |
| `recordLandOfficeTransfer` | Activity, the title-transfer step | `rwb-asset` | Registration and case in; rule ID with version, the two statuses, the release answer and the case move out, one transaction |

No child workflow and no second queue. The activity name is a design choice of this story; the two boundary calls run on their owners' queues.

#### 12.6 Schedules

None. R-DIS-52's ten working days run as a workflow timer and a case SLA, not as a Temporal Schedule. The service's single Schedule is JOB-19, the re-appraisal story's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`); read as S5 from TSD S5 T3.1 while the Ownership Map names only `listing` and `asset_sale` (GAP-2938; ASM-4834) | This story writes `holding_status` |
| listing | S5 (`rwb_asset`) | This story writes `status` |
| asset_sale | S5 (`rwb_asset`) | Read only here; written by the auction-round and proceeds stories |
| decision_record | PLT library in `rwb_asset` | One record per registration (DP-03) |
| idempotency_key | PLT library in `rwb_asset` | The key of the repeated registration and of the release |

Not owned and never read as a table: `recovery_case`, `assignment`, `task`, `timer` (P3), `document`, `document_custody` (P5), `decision_log_entry`, `rule_row` (P7), `proceeds` (P8), every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state fake | `TITLE_TRANSFER_PENDING`, `ASSET_PENDING_TAKE_ON` and a case in another state | AC1 to AC3, X3 |
| rwb-case move fake | `ASSET_SOLD` and `ASSET_ON_BOOKS` accepted; a move refused for an unexpected state | AC2, AC3 |
| rwb-document release fake | Documents released; custody already released; a refusal; no answer inside 2 s | AC2, X4 |
| rwb-decision package fake | The DISPOSAL package at its version with R-DIS-52 and R-DIS-02 | AC1 to AC3 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| Composite route fake | The merged SCR-21 and SCR-22 answer for `RC-2026-000591` | AC1 |
| Registration signal fake | A property registration, a vehicle registration and a repeated registration | AC1, AC2, X5, X6 |

The fakes are test-only; the release and move rows carry their placeholder until their owners confirm the names (GAP-2939; ASM-4835).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two asset reads on `/api/recovery/asset/v1`; the case state read, the case-move answer and the custody release; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The registration and the case state are workflow signals |
| Temporal | 1 workflow, 1 activity owned | `AssetDisposalWorkflow` and `recordLandOfficeTransfer` on `rwb-asset`; the release and case calls on their owners' queues; no Schedule |
| File | None | The Land Office has no interface and no file (GAP-2937) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset.title`; front end `src/modules/recovery/asset/TitleTransfer.tsx`, the fragment SCR-22 embeds, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition here: the legacy `v_ace_npa_sale` read leaves the service and `asset_sale` carries the AMIS sale facts, while the custody release goes to rwb-document and never to its tables. DP-03 is the transaction rule of the step, DP-13 moves the base and DP-19 is how the screens reach the service.

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` title branch | Workflow | Waits on the registration signal and the case state, loads the package in force, reports to the parent |
| `recordLandOfficeTransfer` | Activity | The one step: read, evaluate, record, release, write, answer |
| `TitleTransferEvaluator` | Service | R-DIS-52 on the state, the event and the asset type |
| `AssetDecisionRecordWriter` | Library adapter | One record per registration before any change (DP-03) |
| `TitleTransferWriter` | Repository | `listing.status` and `asset.holding_status` in one transaction with the idempotency row and the lock |
| `DocumentReleaseClient`, `CaseStateClient`, `CaseMoveAnswer` | Clients | The release, the state read and the answer, one hop, 2 s |
| `AssetController` | Controller | The two reads, the rights and the 400/401/403/404/422/503 map |
| `TitleTransfer` | React component | The registration, the statuses and the refusal states on SCR-22, read only |

**Database.** No Flyway file: the tables come with the DB story and the record and key are library objects created in `rwb_asset`; no column is added for the registration reference (GAP-2938; ASM-4834).

**Configuration.** The ten working days, the lists `LOV-HOLDING`, `LOV-LISTING` and `LOV-ASSET-TYPE` at their version (TSD S5 T3.2); the DISPOSAL package and its version from rwb-decision; the capability rows from rwb-access; the flag and the 2 s budget as platform configuration (ADR-020).

**Build steps.** (1) the title branch and its input record; (2) `TitleTransferEvaluator` with the property, vehicle and wrong-state paths (AC2, X3, X6); (3) `AssetDecisionRecordWriter` against the stub (AC1, AC4, X1); (4) `DocumentReleaseClient` with the key, the refusal and the timeout (AC2, X4); (5) `TitleTransferWriter` with the two statuses and the idempotency row (AC2, X5); (6) `CaseMoveAnswer` (AC2, AC3); (7) `AssetController` with the rights and the error map (AC1, X2); (8) the screen fragment through the route fake (AC1); (9) the boundary test (X8, BR4, BR5, BR6, BR8).

**Feature flag.** `rwb.asset.title-transfer-v1`; off means the registration is held, nothing is released and no move is answered.

**Done when.** §16 passes, a synthetic registration releases the documents, writes the two statuses, records the outcome and answers `ASSET_SOLD`, a repeat writes once, a refused release leaves nothing committed, a forced record failure changes nothing, no case, document or `v_ace_*` read exists, and the two screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the registration or of a request is absent or invalid (X7) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads or acts (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the statuses change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S5-001 | Carried from the legacy message set; it names the floor and the approval limit, which are the pricing story's, so no path here raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set; it names the age of an appraisal, which is the re-appraisal story's, so no path here raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |

The five IDs are the legacy and platform sets copied unchanged; no message is reworded and none is added. The Land Office rejection of X9 has no message in any source (GAP-2941; ASM-4837).

### 15. Screens and states

SCR-21 Asset list (loading, list) and SCR-22 Asset record (take-on, held, listed, sold) are served through the gateway-bff route (DP-19), which calls rwb-asset for the asset, its holding status and its listing, rwb-case for the route state and rwb-document for the custody state. This story fixes the rwb-asset answers only; the route and the field list are RWB-PLT-N001-CON.

The states it produces are the sold state of SCR-22 — the registration date, the sold status of the listing and the holding status of the asset — and the refusal, not-recorded, wrong-state, refused-release and vehicle states with MSG-P4-002, MSG-P7-003, MSG-GEN-001 and X4 to X6. Take-on and held are the take-on and holding stories'.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-029-01 | AC1 | Component | Case `RC-2026-000591` with a property and a live listing; the registration, the record, the two statuses and the answer on the fakes |
| TC-E4-029-02 | AC2 | Integration | Case `RC-2026-000592` at `TITLE_TRANSFER_PENDING`; the release, the statuses and `ASSET_SOLD` across the rwb-document and rwb-case fakes |
| TC-E4-029-03 | AC3 | Integration | Case `RC-2026-000593` at `ASSET_PENDING_TAKE_ON` with a registered deed in lieu transfer; the asset record and `ASSET_ON_BOOKS` at the take-on boundary |
| TC-E4-029-04 | AC4 | Component | Record stub stopped; nothing written, nothing released, MSG-P7-003 shown |
| TC-E4-029-05 | Access | Component | A role without the right; 403 with MSG-P4-002, no read and no write |
| TC-E4-029-06 | Principle 5 | Component | A forced record failure at the moment of the status write; no row change, no release, no answer |

The six cases are the legacy cases in their order with the Level column added: TC-E4-029-02 and -03 run `Integration` because each crosses two or three boundaries, the rest `Component` on their fakes. The full text is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 3 harness, which carries the real document-hub call.

### 17. Guardrails

- No business value in code: the ten working days, the statuses, the asset types and the rule rows stay reference data or rule rows with a version.
- No personal data in the schema, a workflow input or a log; a buyer is a code, the property address stays an ACE fact and every fixture is synthetic.
- The Land Office is never called: no interface, no file and no screen is built for it (BR3).
- The documents stay with rwb-document: no `document` or `document_custody` row is read or written here (DP-05, BR4).
- The case stays with rwb-case: no `recovery_case` or `assignment` row here (BR5).
- ACE data only through the owner's contract: no `v_ace_*` grant and no ACE read (DP-05).
- One base, one topic, one queue and one login per service (DP-13, DP-14).
- The record precedes the change, the release is idempotent and the repeat is deduped (DP-03, BR2, BR9).
- No retired element returns: no shared job table, no Quartz row, no monolith base, no data-lake export of a transfer.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-008 | Title transfer is prepared and recorded for vehicles and for property (Business Requirements Program v5); shared with FEAT-AST-19, and the plan carries no id for this slice (GAP-2942; ASM-4838) | The title branch, the release, the statuses and the answer | TC-E4-029-01, -02 |
| ADR-013 | 19 services inside ACE | rwb-asset owns the transfer record and the statuses | TC-E4-029-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its login | TC-E4-029-06 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The registration signal and the durable timer; no Quartz row | TC-E4-029-01 |
| ADR-020 | Contract-first REST, one hop, 2 s | The three consumed rows and the release budget | TC-E4-029-02 |
| ADR-022 | Local decision record plus central ledger | The record before the change | TC-E4-029-04, -06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-029, Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word |
| Test cases | TC-E4-029-01 to TC-E4-029-06 |
| Feature and screens | FEAT-AST-20, SCR-21 and SCR-22 |
| Rules | R-DIS-52 owned, R-DIS-02 tabled, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the elements, the error set and the fakes: RWB-S5-E4029-CON.
- The Land Office itself: a person and officer step with no service and no interface (GAP-2937; ASM-4833).
- The registration reference and the title status: no element of the service (GAP-2938; ASM-4834).
- The rejection of a transfer and the blocked title: R-DIS-53, with no owner in this split (GAP-2941; ASM-4837).
- The payment term, the award and the confirmation that starts the transfer: FEAT-AST-18's story (R-DIS-47 to R-DIS-49).
- The vehicle registration through SCIS: FEAT-AST-19's story (R-DIS-51).
- The take-on of the property after a deed in lieu: RWB-S5-E3020-APP (R-DIS-02) (GAP-2940).
- The proceeds, the shortfall and the vendor fee: FEAT-AST-21's story and rwb-payment (P8).
- The documents, their custody and their retention: rwb-document (P5) (GAP-2939).
- The case, its states and the parent workflow: rwb-case (P3).
- The rule rows and the package version: rwb-decision (P7).
- The composite route and the field list: RWB-PLT-N001-CON and the edge stories.
- The real document-hub call and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards and the runbook: the operations story of this key.
