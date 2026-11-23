# RWB-S5-E4028-APP Transfer vehicle registration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4028-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-T |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4028-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-028 for rwb-asset. The three legacy criteria are kept word for word with their origin tag and the five legacy test cases keep their IDs. The transfer becomes the title-transfer branch of `AssetDisposalWorkflow` on queue `rwb-asset` in namespace `rwb-recovery`: from `TITLE_TRANSFER_PENDING` it prepares the transfer pack from the asset, the sale and the registration facts, submits it through the adapter that fronts SCIS (INT-28), evaluates R-DIS-51 on the DISPOSAL package in force, records the outcome before the row changes (DP-03), answers `ASSET_SOLD` to rwb-case and publishes nothing. The legacy `v_ace_npa_asset` and `v_ace_npa_sale` reads leave the service for the rwb-source-data data-product contract (DP-05), the base becomes `/api/recovery/asset/v1` (DP-13) and SCR-21 and SCR-22 read through the gateway-bff route (DP-19). Gaps: no interface row or call type for SCIS, and DP-16 outside the pattern set (GAP-2931; ASM-4828); the FSD submits while INT-28 says the officer prepares it (GAP-2932; ASM-4829); no element holds the registration particulars or the submission reference (GAP-2933; ASM-4830); R-DIS-53 has no owning story (GAP-2934; ASM-4831); the package load without the DP-04 platform row (GAP-2935; ASM-4796); REQ-S5-008 is claimed twice (GAP-2936; ASM-4832). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **the Workbench to prepare and submits the registration transfer through SCIS**, so that **assets sell sooner at approved prices** (legacy RWB-E4-028, word for word).

This is the application slice of legacy RWB-E4-028. It owns:

- the three legacy criteria with their origin tag, and the rule, messages and screens they depend on;
- the title-transfer branch of `AssetDisposalWorkflow` on `rwb-asset`, a child of the case workflow (Architecture v5 slide 13): from `TITLE_TRANSFER_PENDING`, on `REGISTRATION_TRANSFERRED`, under R-DIS-51 and `asset_type = vehicle`, to `ASSET_SOLD`;
- the preparation of the transfer pack from the asset, the sale and the registration facts, and its submission through the adapter that fronts SCIS (INT-28) — the adapter row is stubbed and faked on Day 1 (GAP-2931; ASM-4828);
- the decision record of the submission and its answer **before** the `asset` and `asset_sale` rows change (DP-03);
- the write of `holding_status` on `asset` and of the transfer status on the sale in `rwb_asset`;
- the case answer `ASSET_SOLD` to rwb-case, with the rule and its version;
- the reads behind SCR-21 and SCR-22 on `/api/recovery/asset/v1` through the gateway-bff route (DP-13, DP-19).

It does not own: the shape of the pack, the reads, the consumed rows, the decision-record and rule-package elements, the error set and the fakes, which are RWB-S5-E4028-CON; the five-day payment term and its confirmation, FEAT-AST-18's story; the property transfer at the Land Office (R-DIS-52), FEAT-AST-20's story; the rejected transfer (R-DIS-53), which no story row of the split owns (GAP-2934; ASM-4831); the proceeds and the shortfall, FEAT-AST-21; the documents and their custody, rwb-document (P5); the case and its states, rwb-case (P3); the rules and their package, rwb-decision (P7); the SCIS adapter itself, rwb-integration (P2); the deployment, the flag and the runbook, the operations story of this key.

### 2. Business rationale

Legacy RWB-E4-028 closed the sale of a vehicle: once the buyer had paid, the bank could not call the asset sold until the registration book had changed hands at the Department of Land Transport through SCIS, and the case waited on an officer's errand. The FSD keeps it as FEAT-AST-19 in module S5, run by the system, between FEAT-AST-18, which confirms the payment under R-DIS-48 (into `TITLE_TRANSFER_PENDING`), and FEAT-AST-21, which applies the proceeds under R-DIS-54 (out of `ASSET_SOLD`). BR-029 of the Epic 4 BRD states the outcome: the title transfer is prepared and submitted for a vehicle through SCIS and recorded for a property at the Land Office.

What D-RCV-60 changes:

- **the transfer state is this service's.** `asset` and `asset_sale` are S5's tables in `rwb_asset`; `holding_status` carries `SOLD` and the sale carries its transfer status (Ownership Map; TSD S5 T3.1, `LOV-HOLDING`).
- **SCIS is a boundary, not a read.** The legacy data table read `v_ace_npa_asset` and `v_ace_npa_sale`; under DP-05 those facts arrive on the rwb-source-data data-product contract, and the submission leaves through rwb-integration (INT-28). Neither interface publishes an operation name or an approach, so both rows carry the placeholder and a fake (GAP-2931; ASM-4828).
- **the decision is recorded first**, once per submission, in the row's transaction — what AC1 asked and AC3 tested.
- **nothing is published.** EV-22 `AssetTakenOn` is the take-on story's (TSD S5 T5.3); §12.3 states the absence and a build that adds an event fails it.

The timer the rule row names — 5 working days — is the transfer clock; it stays a rule-row value and is never a constant (BR3).

### 3. Preconditions

- RWB-S5-E4028-CON tagged: the two reads, the four consumed rows, the decision-record element, the rule-package element, the error set and the fakes.
- `asset` exists in `rwb_asset` with DF-COL-028 to DF-COL-042 and `asset_sale` with DF-SAL-009 to DF-SAL-019 (TSD S5 T3.1), plus the standard columns of T3.0; no column is added (GAP-2933; ASM-4830).
- The case is in `TITLE_TRANSFER_PENDING`, written by rwb-case on FEAT-AST-18's answer under R-DIS-48; the asset carries `asset_type = VEHICLE` from `LOV-ASSET-TYPE` and `holding_status` from `LOV-HOLDING`.
- The DISPOSAL package is in force at its version and carries R-DIS-51, loaded through the service template; DP-04 is outside the pattern set of this slice (GAP-2935; ASM-4796).
- The SCIS adapter row (INT-28) and the rwb-source-data product are answered by their fakes; neither operation name is published (GAP-2931; ASM-4828).
- The transfer due fact, the payment confirmation and the adapter answer arrive as signals and activity results of `AssetDisposalWorkflow`; no subscription is added.
- RWB-PLT-E1027-CON writes in the caller's transaction (DP-03); RWB-PLT-N001-CON serves the two screens, one hop each (DP-19).
- The service holds its own login on `rwb_asset`, no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-05).
- No approval is needed to build against a Draft baseline; the contract is tagged when its tests pass (ASM-4829).

### 4. Flow

1. The buyer's payment is confirmed and R-DIS-48 moves the case to `TITLE_TRANSFER_PENDING`; the running `AssetDisposalWorkflow` enters its title-transfer branch on the durable timer of the rule row (5 working days).
2. `TitleTransferEvaluator` reads the case state on the rwb-case contract and the asset and sale facts on the rwb-source-data contract, with their data date; a stale product is refused (X5).
3. It confirms `asset_type = VEHICLE` from `LOV-ASSET-TYPE`; a property or another type is not this branch's and is answered as out of scope (X3).
4. `RegistrationPackBuilder` assembles the pack from `asset_ref`, `asset_code`, `asset_type`, `transfer_in_type`, the sale dates, the sale price and the transfer fee; the registration particulars of the vehicle and the submission reference are Not specified in the source documents (GAP-2933; ASM-4830).
5. `submitRegistrationTransfer` submits the pack through the adapter that fronts SCIS (INT-28) as an activity on the owner's queue; where the interface answers "not available", the officer's submission is recorded instead of an automatic one (GAP-2932; ASM-4829).
6. `AssetDecisionRecordWriter` writes one record **before any change**, with the rule id, the rule version and the package version; a failed write stops the step (DP-03; AC1, AC3).
7. `TitleTransferWriter` writes `holding_status` = `SOLD` on `asset` and the transfer status on the sale in one `rwb_asset` transaction with the record and the idempotency row.
8. `CaseMoveAnswer` answers `ASSET_SOLD` with the rule and its version; rwb-case writes the case state, and the workflow records the stage outcome for its parent.
9. R-DIS-51's condition holds, so the branch ends: the workflow returns to the parent and the stage closes; the proceeds step of FEAT-AST-21 is started by the parent, not here.
10. An adapter answer that rejects the transfer moves nothing: the step holds, the pack and the answer are recorded, and R-DIS-53's `TITLE_BLOCKED` is not taken here because no story row owns it (GAP-2934; ASM-4831) — the branch fails closed and raises an alert.
11. A repeated signal or key writes once and is counted; the workflow continues-as-new at each stage end and at least every 28 days.
12. Nothing is published: no outbox row, no topic write, no consumer group (BR7, §12.3).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record cannot be written | Nothing written, no move answered, the asset and the sale unchanged | MSG-P7-003 | AC3, TC-E4-028-03, TC-E4-028-05 |
| X2 | The role lacks the Asset and disposal right | 403 before any read or write | MSG-P4-002 | AC1, TC-E4-028-04 |
| X3 | The asset is not a vehicle, or the case is in another state | The rule does not fire; nothing written; the state reported to the parent | None | AC2 |
| X4 | A required element of the pack is absent or invalid | 422 or a held step with the field named; nothing submitted | MSG-GEN-001 | AC1 |
| X5 | The source-data product is stale after a late or failed batch | The step holds, writes nothing and shows the data date; it resumes on the next fresh answer | MSG-P1-001 | AC1 |
| X6 | The adapter answers rejected, or no answer inside 2 s | Nothing moves; the pack and the answer are recorded; the rejection alert is raised; `TITLE_BLOCKED` is not taken (GAP-2934; ASM-4831) | None | AC1, AC2 |
| X7 | The same signal or key arrives twice | One submission, one record, one answer | None | AC1 |
| X8 | The composite route or a consumed contract does not answer | Retry on the workflow schedule; 503 in the platform envelope | None | AC1, AC2 |
| X9 | A statement reaches a `v_ace_*` view, `recovery_case` or a foreign schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | §17, BR9 |

X1 to X3 are the legacy paths on the split, X4 to X8 what the pack, the boundaries and the adapter add, and X9 the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the CON baseline and the fakes; no live P1, P2, P3 or P7 |
| Negotiable | Activity name, decision code and pack element order are ours; rule, messages, screens, rows and reads are fixed |
| Valuable | A sold vehicle reaches `ASSET_SOLD` on the workbench instead of on an officer's errand, and the record shows what was submitted and when |
| Estimable | One branch, one evaluator, one pack builder, one record per outcome, two row changes, one answer, three clients, two screen fragments |
| Small | Two weeks with its tests on the fakes |
| Testable | Each criterion on synthetic cases through the fakes, plus the access, wrong-type, stale, rejected, repeat and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Transfer vehicle registration

  Background:
    Given case "RC-2026-000541" holds vehicle asset "AST-2026-000541" of type VEHICLE with a sale agreed
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-51
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Transfer vehicle registration (legacy RWB-E4-028 AC1)
    Given the rwb-integration contract mock returns the SCIS transfer of vehicle asset "AST-2026-000541" accepted with its submission reference
    Given the rwb-source-data contract mock returns the asset "AST-2026-000541" of type VEHICLE and its sale at today's data date
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then prepares and submits the registration transfer through SCIS
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-51 (legacy RWB-E4-028 AC2)
    Given the rwb-case contract mock returns the case "RC-2026-000542" in state TITLE_TRANSFER_PENDING
    Given the rwb-integration contract mock returns the SCIS transfer of vehicle asset "AST-2026-000542" accepted
    Given a case in state TITLE_TRANSFER_PENDING
    When registration transferred
    Then transfer the registration through SCIS
    Then the case moves to ASSET_SOLD

  Scenario: AC3 Not recorded (legacy RWB-E4-028 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria word for word with the origin tag added: `its trigger arrives`, `registration transferred`, `the action is taken` and `the decision log cannot be written` stand unchanged, and the `Given the <service> contract mock returns <x>` lines are the only additions. The work happens in three places: rwb-case writes `ASSET_SOLD`, rwb-integration carries the SCIS submission, rwb-source-data answers the asset and sale facts; this story prepares the pack, evaluates R-DIS-51, writes the two rows, records and answers. AC2's `registration transferred` is the adapter's accepted answer, not an officer's confirmation (GAP-2932; ASM-4829).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-51 | Asset disposal | D8.1 to D8.3 | TITLE_TRANSFER_PENDING | REGISTRATION_TRANSFERRED | asset_type = vehicle | Transfer the registration through SCIS | ASSET_SOLD | Workbench | SCIS | 5 working days |

The row is copied character for character from the Business Rules and Routing Logic v4. Its owner column is a business role, so the case stays in the state and moves in rwb-case on this story's answer, while the `asset` and `asset_sale` rows are written here. R-DIS-48 (the payment confirmation into `TITLE_TRANSFER_PENDING`) is FEAT-AST-18's, R-DIS-52 (property) is FEAT-AST-20's, and R-DIS-53 (rejection) belongs to no story row of the split (GAP-2934; ASM-4831).

| ID | Rule | Source |
|---|---|---|
| BR1 | The transfer is this service's: `holding_status` on `asset` and the transfer status on `asset_sale` are elements of `rwb_asset`, and no other service writes them | Ownership Map; TSD S5 T3.1; Architecture v5 slide 41 |
| BR2 | The record precedes the change, one per submission, with the rule and package version; a failed write changes nothing | DP-03; AC1, AC3 |
| BR3 | The 5 working days of the rule row, the asset type, the transfer-in type and the statuses are rule rows or reference data with a version, never a constant | TSD S5 T3.2; legacy Guardrails |
| BR4 | The case move is answered, not written; the states are rwb-case's | Ownership Map (P3); GAP-2931 |
| BR5 | The pack is built only from elements the sources name; the registration particulars and the submission reference carry the placeholder and are not invented as columns | GAP-2933; ASM-4830 |
| BR6 | The ACE facts are rwb-source-data's and the SCIS submission is rwb-integration's: no `v_ace_*` read and no direct external call from this service | DP-05; Architecture v5 slides 8 and 13 |
| BR7 | No event is published and none is consumed; EV-22 `AssetTakenOn` is the take-on story's | TSD S5 T5.3 |
| BR8 | A repeated signal or key writes once, answers once and is counted | TSD S5 T-A.2 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_asset` | DP-01; TSD S5 T3.3 |
| BR10 | No personal data in the schema, a record, a log or a workflow input; the pack carries a vehicle reference and amounts, never a person | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case state is rwb-case's and is applied by the parent `CaseWorkflow` on this story's answer (BR4).

| From (case state) | Event | Condition | To |
|---|---|---|---|
| TITLE_TRANSFER_PENDING | `REGISTRATION_TRANSFERRED` under R-DIS-51 | `asset_type = vehicle` and the adapter accepted the transfer | ASSET_SOLD, answer `ASSET_SOLD` |
| TITLE_TRANSFER_PENDING | The adapter rejected the transfer under R-DIS-53 | `asset_type = vehicle` | Unchanged here: `TITLE_BLOCKED` is not taken (GAP-2934) |
| Any | Another state, another asset type or a repeated signal | X3, X7 | Unchanged |

| `holding_status` (asset) | Event | Condition | To |
|---|---|---|---|
| Under offer | The transfer is accepted under R-DIS-51 | The record is written | SOLD, with the sale's transfer status |
| Any | The adapter rejects or does not answer | X6 | Unchanged |

The statuses are the `LOV-HOLDING` rows of TSD S5 T3.2; the case states are the DISPOSAL machine's (TSD S5 T4).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and the further roles of the legacy read row | Asset and disposal R: reads the asset, the sale and the transfer status in scope |
| SY-CASEWF, SY-RULES, SY-AGENT | The matrix's right, under the same checks as a person |
| rwb-asset service identity | Runs the branch unattended; no grant on another schema and no `v_ace_*` grant |

The rights are the row of the legacy permission table and TSD S5 T6.1, nothing wider: the legacy story declares Asset and disposal R only, and this step runs unattended, so no role is given a write here. DP-08 is not in the pattern set: the right is declared per operation and the guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-028 to DF-COL-042 | asset (S5, `rwb_asset`) | id, case_id, collateral_id, asset_ref, asset_code, asset_type, transfer_in_type, from_segment, transfer_in_date, book_value, auction_purchase_price, repossessed_date, stock_date, holding_status, holding_cost_to_date | Write: `holding_status` = SOLD; read: `asset_ref`, `asset_code`, `asset_type`, `transfer_in_type` |
| DF-SAL-009 to DF-SAL-019 | asset_sale (S5, `rwb_asset`) | id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee and 5 more | Write: the transfer status; read: the dates, the price and the fee |
| Standard columns | asset, asset_sale (S5, `rwb_asset`) | state, version, created_at/by, updated_at/by, is_active | Write, with the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the library, before the change |
| Not specified in the source documents (GAP-2933; ASM-4830) | asset (S5, `rwb_asset`) | the registration particulars of the vehicle and the SCIS submission reference with its date | No column; the pack and the reference are held with the submission record |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, book_value and 9 more | Not read: rwb-source-data contract (BR6) |
| DF-ACE-220 to DF-ACE-230 | `v_ace_npa_sale` (P1) | npa_sale_key, npa_asset_key, contract_date, sale_date, sale_price, transfer_fee and 5 more | Not read: rwb-source-data contract (BR6) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and 19 more | Not read: rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 10 more | Not read or written: rwb-decision |
| DF-DOC-001 to DF-DOC-011 | document (P5) | id, case_id, document_type, storage_ref and 8 more | Not read: the custody release is FEAT-AST-20's |

Field IDs follow TSD S5 T3.1 and the Logical Data Model and Data Dictionary v8. **No new table, no column, no migration**: the tables come with the DB story, and `decision_record` and `idempotency_key` are library objects in `rwb_asset` (DP-03). **No personal data**: a vehicle reference, codes, amounts, dates and a rule version only; every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the shapes of RWB-S5-E4028-CON; the transfer itself is submitted by the workflow, not by a REST call.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the transfer status of each asset (API-S5-001) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out with title, sale and transfer status (API-S5-002) | Asset and disposal, R, scope applied | Not applicable |

`GET /assets/{assetKey}` and `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds` are the other stories' rows of this service. Errors: 400, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 503 when a library or a contract does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state and the stage it is in; faked |
| Case-move answer (name Not specified in the source documents (GAP-2931; ASM-4828)) | rwb-case (P3) | P3 rwb-case | `ASSET_SOLD` with the rule and its version; faked |
| Asset and NPA sale data product (name Not specified in the source documents (GAP-2931; ASM-4828)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset, sale and registration facts with their data date, in place of the legacy `v_ace_npa_asset` and `v_ace_npa_sale` reads (DP-05); faked |
| SCIS vehicle-registration transfer (name Not specified in the source documents (GAP-2931; ASM-4828)) | queue `rwb-integration` | P2 rwb-integration | The transfer pack out and its accepted or rejected answer with the submission reference back (INT-28); faked |

One hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). The rwb-integration row is an activity on the owner's queue because a route service reaches a shared capability through Temporal, never REST (Architecture v5 slide 13). DP-16 is outside the pattern set of this slice, so the row carries no C dependency and the story builds on the adapter's document and fake (GAP-2931; ASM-4828).

#### 12.3 Events published

None. EV-22 `AssetTakenOn` is the take-on story's and the sale events are the sale stories'; a completed transfer writes no outbox row and adds nothing to `rwb.asset.events.v1`. A build that publishes here fails the absence test.

#### 12.4 Events consumed

None. The transfer due fact, the payment confirmation and the adapter answer arrive as signals and activity results of `AssetDisposalWorkflow`, so this slice adds no consumer group and no inbox row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one per case per stage, continues-as-new across the holding | `rwb-asset` in `rwb-recovery` | Input: case, route, asset, sale, package in force; signals: transfer due, payment confirmed, adapter answer, package in force |
| `submitRegistrationTransfer` | Activity, the pack, the submission and the write | `rwb-asset` | Asset, sale and case in; rule IDs with versions, `holding_status`, transfer status, submission reference and case move out, one transaction |

No child workflow and no second queue. The activity name is a design choice of this story; the SCIS submission runs as an activity on `rwb-integration`'s queue.

#### 12.6 Schedules

None. The 5 working days of R-DIS-51 run as a durable timer inside the workflow; the step owns no Temporal Schedule and no Quartz job. The service's single Schedule is JOB-19, the re-appraisal story's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`) | This story writes `holding_status` |
| asset_sale | S5 (`rwb_asset`) | This story writes the transfer status of the sale |
| decision_record | PLT library in `rwb_asset` | One record per submission (DP-03) |
| idempotency_key | PLT library in `rwb_asset` | The key of the repeated signal |

Not owned and never read as a table: `recovery_case`, `assignment`, `task`, `timer` (P3), `decision_log_entry`, `rule_row`, `approval` (P7), `listing` (S5 but the sibling stories'), `document`, `document_custody` (P5), `proceeds` (P8), `deviation` (S8), every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state fake | `TITLE_TRANSFER_PENDING` for the fixture cases; a case in another state | AC2, X3 |
| rwb-case move fake | `ASSET_SOLD` accepted; a move refused for an unexpected state | AC1, AC2 |
| rwb-source-data product fake | Vehicle asset `AST-2026-000541` with its sale at today's date; a stale product; a property asset | AC1, X3, X5 |
| SCIS transfer fake | Accepted with the submission reference; rejected; no answer inside 2 s | AC1, AC2, X6 |
| rwb-decision package fake | The DISPOSAL package at its version with R-DIS-51 | AC1 to AC3 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC3, X1 |
| Composite route fake | The merged SCR-21 and SCR-22 answer for `RC-2026-000541` | AC1 |
| Repeat-signal fake | The same signal twice and the same key twice | AC1, X7 |

The fakes are test-only; the placeholder rows carry their gap until their owners confirm the names (GAP-2931; ASM-4828).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two asset reads on `/api/recovery/asset/v1`; the case state read, the case-move answer and the source-data product; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The transfer facts are workflow signals |
| Temporal | 1 workflow, 1 activity owned, 1 consumed | `AssetDisposalWorkflow` and `submitRegistrationTransfer` on `rwb-asset`; the SCIS transfer activity on `rwb-integration`; no Schedule |
| File | None | INT-28 names no file and no API approach (GAP-2931) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset.titletransfer`; front end `src/modules/recovery/asset/TitleTransfer.tsx`, the fragment SCR-22 embeds, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition here: the legacy `v_ace_npa_asset` and `v_ace_npa_sale` reads leave the service for the P1 boundary and no `v_ace_*` grant is kept. DP-03 is the transaction rule of the step, DP-13 moves the base, DP-19 is how the screens reach the service. The SCIS boundary and the source-data row are built on documents and fakes on Day 1 (GAP-2931), and the package in force is loaded through the service template without the DP-04 platform row (GAP-2935).

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` title-transfer branch | Workflow | Waits on the timer and the signals, loads the package in force, reports to the parent |
| `submitRegistrationTransfer` | Activity | The one step: read, prepare, submit, evaluate, write, answer |
| `TitleTransferEvaluator` | Service | R-DIS-51 on the asset type, the case state and the adapter answer |
| `RegistrationPackBuilder` | Service | The pack from the asset, the sale and the registration facts |
| `AssetDecisionRecordWriter` | Library adapter | One hash-linked record per submission before any change (DP-03) |
| `TitleTransferWriter` | Repository | `asset` and `asset_sale` in one transaction with the idempotency row and the lock |
| `ScisTransferActivity`, `SourceDataClient`, `CaseStateClient`, `CaseMoveAnswer` | Clients | The adapter activity and the three consumed rows, one hop, 2 s |
| `TitleTransferController` | Controller | The two reads, the right and the 400/401/403/404/503 map |
| `TitleTransfer` | React component | The transfer state on SCR-22, read only |

**Database.** No Flyway file: tables from the DB story, library objects from the library's migration, no column added for the particulars (GAP-2933).

**Configuration.** The 5 working days of the rule row, the asset type and the transfer-in type at their version (TSD S5 T3.2); the DISPOSAL package and version from rwb-decision; the capability row from rwb-access; the flag and the 2 s budget as platform configuration (ADR-020).

**Build steps.** (1) the branch and its input record; (2) `RegistrationPackBuilder` from the source-data fake (AC1, X4); (3) the adapter activity against its fake, accepted, rejected and timed out (AC1, AC2, X6); (4) `TitleTransferEvaluator` with R-DIS-51 and the asset-type guard (AC2, X3); (5) the record writer against the stub (AC3, X1); (6) `TitleTransferWriter` with the idempotency row (AC1, X7); (7) `CaseMoveAnswer` (AC1, AC2); (8) `TitleTransferController` with the right and the error map (X2); (9) the screen fragment through the route fake; (10) the staleness path (X5) and the boundary test (X9, BR6, BR7).

**Feature flag.** `rwb.asset.vehicle-registration-transfer-v1`; off means the branch holds, nothing is submitted, nothing is written and no move is answered.

**Done when.** §16 passes, an accepted transfer moves the case to `ASSET_SOLD` and shows the submission record in SIT, a rejected or timed-out transfer changes nothing and alerts, a repeat writes once, a forced record failure changes nothing, no case row and no `v_ace_*` read exists, and the two screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the pack or of a request is absent or invalid (X4) | Enter {field}. |
| MSG-P4-002 | A role without the right reads or the step is called without it (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the rows change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The asset or sale fact is stale after a late or failed batch (X5) | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-S5-001 | A floor price arrives under the approver's limit on a read of the sale (X3) | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | An appraisal more than a year old is carried on the asset read (X5) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |

The six IDs are the legacy and platform sets, copied unchanged; no message is reworded and none is added. The legacy staleness rule VR-S5-019-1 is carried by MSG-P1-001 on the source-data row. No message exists for a rejected transfer: the rejection is recorded and alerted, not shown (GAP-2934).

### 15. Screens and states

SCR-22 Asset record (take-on, held, listed, sold) and SCR-21 Asset list (loading, list) are served through the gateway-bff route (DP-19), which calls rwb-asset for the asset, the sale and the transfer status, rwb-case for the state and rwb-source-data for the facts. This story fixes the rwb-asset answers only; the route and field list are RWB-PLT-N001-CON.

The state it produces is the sold state of SCR-22 — the submission reference, the date, the accepted answer and the sale's transfer status — plus the refusal, not-recorded, wrong-type, stale, rejected and repeated states with MSG-P4-002, MSG-P7-003, MSG-GEN-001, MSG-P1-001 and the rejection alert. Take-on, held and listed belong to the take-on, holding and pricing stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-028-01 | AC1 | Component | Case `RC-2026-000541` with a vehicle asset in `TITLE_TRANSFER_PENDING`; the pack, the submission reference, the record and the sale status on the fakes |
| TC-E4-028-02 | AC2 | Integration | Case `RC-2026-000542` at `TITLE_TRANSFER_PENDING`; R-DIS-51 fires on the accepted answer and `ASSET_SOLD` arrives across the rwb-integration, rwb-source-data and rwb-case fakes |
| TC-E4-028-03 | AC3 | Component | Record stub stopped; nothing written, no move answered, MSG-P7-003 shown |
| TC-E4-028-04 | Access | Component | A role without the right; 403 with MSG-P4-002, no read and no write |
| TC-E4-028-05 | Principle 5 | Component | A forced record failure at the step; no row change, no answer, no event |

The five cases are the legacy cases in their order with the Level column added: TC-E4-028-02 runs `Integration` because it crosses three boundaries, the rest `Component` on their fakes. The full text is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; the `-ITG` copies (TC-E4-028-02-ITG and its siblings) belong to the wave 3 harness, which carries the real SCIS, source-data and case calls.

### 17. Guardrails

- No business value in code: the 5 working days, the asset type, the transfer-in type and the statuses stay reference data or rule rows with a version.
- No personal data in the schema, a workflow input or a log; a vehicle is identified by its asset reference and every fixture is synthetic.
- ACE data only through the owner's contract: no `v_ace_*` grant, no ACE read, and no direct external call to SCIS from this service (DP-05, BR6).
- The case stays with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row here (BR4).
- One base, one topic, one queue and one login per service (DP-13, DP-14).
- No retired element returns: no shared job table, no Quartz row, no monolith base, no data-lake export of a transfer.
- The record precedes the change and the repeated signal is deduped (DP-03, BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-008 | The title transfer is prepared and submitted for a vehicle through SCIS (BR-029 of the Epic 4 BRD; the same ID is mapped to FEAT-AST-08 in TSD S5 T8: GAP-2936; ASM-4832) | The pack, the submission, R-DIS-51 and the two answers | TC-E4-028-01, TC-E4-028-02 |
| BR-029 | The title transfer is prepared and submitted for a vehicle through SCIS and recorded for a property at the Land Office | The vehicle half of the requirement | TC-E4-028-01, TC-E4-028-02 |
| ADR-013 | 19 services inside ACE | rwb-asset owns the transfer state and the sale status | TC-E4-028-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its login | TC-E4-028-05 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The durable timer and the signals; no Quartz row | TC-E4-028-02 |
| ADR-020 | Contract-first REST, one hop, 2 s | The consumed rows and the adapter activity | TC-E4-028-01, -02 |
| ADR-022 | Local decision record plus central ledger | The record before the change | TC-E4-028-03, -05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-028, Split (rework) |
| Legacy criteria | AC1 to AC3, owned word for word |
| Test cases | TC-E4-028-01 to TC-E4-028-05 |
| Feature and screens | FEAT-AST-19, SCR-21 and SCR-22 |
| Rules | R-DIS-51, governed in rwb-decision; R-DIS-48 and R-DIS-52 belong to the sibling stories; R-DIS-53 has no owner (GAP-2934) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The shape of the pack and the reads, the consumed rows, the record and rule-package elements, the error set and the fakes: RWB-S5-E4028-CON.
- The five-day payment term and the confirmation that moves the case to `TITLE_TRANSFER_PENDING`: FEAT-AST-18's story (R-DIS-47, R-DIS-48).
- The property transfer at the Land Office and the custody release of its documents: FEAT-AST-20's story (R-DIS-52).
- The rejected transfer and `TITLE_BLOCKED`: R-DIS-53 belongs to no story row of the split (GAP-2934); this slice fails closed and alerts.
- The proceeds, the vendor fee and the shortfall: FEAT-AST-21's story (R-DIS-54, R-DIS-55).
- The vehicle registration particulars and the SCIS pack layout: Not specified in the source documents (GAP-2933; ASM-4830).
- The SCIS adapter itself, its protocol and its file or API approach: rwb-integration (P2) and INT-28 (GAP-2931; ASM-4828).
- The documents of the case: rwb-document (P5).
- The case, its states and the parent workflow: rwb-case (P3).
- The rule rows and the package version: rwb-decision (P7) (GAP-2935).
- The composite route and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The real SCIS call and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards and the runbook: the operations story of this key.
