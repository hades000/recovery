# RWB-S5-E3025-APP Maintain a held property

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3025-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-025 |
| Feature | FEAT-AST-07 |
| Requirement | Not specified in the source documents (GAP-2866); plan reqs list empty; anchors BR-S5-007, R-DIS-10, R-DIS-11 and R-DIS-12 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S5-E3025-APP-16); the squad sizes it at refinement |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E3025-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-S5-E3025-CON; rwb-source-data, rwb-partner, rwb-case and rwb-decision contracts |
| Contract version | Not specified in the source documents (DOR-RWB-S5-E3025-APP-23); the contract version is fixed by the build dependency RWB-S5-E3025-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-025 split out for rwb-asset. The three legacy acceptance criteria are kept word for word with their origin tag. The step becomes one step of `AssetDisposalWorkflow` on task queue `rwb-asset`: it records maintenance, insurance and custody costs on the asset row in `rwb_asset`, raises the work order to the property services vendor as a partner instruction, and records the decision through the local decision-record library before the row changes (DP-03). The ACE asset fact reaches the service on the rwb-source-data data-product contract, never through a `v_ace_*` read (DP-05); the base becomes `/api/recovery/asset/v1` (DP-13); SCR-21 and SCR-22 read through the gateway-bff composite route (DP-19). No source names the cost operation, its closed list, the vendor instruction or an event for this step, so those are recorded (GAP-2862, GAP-2863, GAP-2866, GAP-2868; ASM-4747 to ASM-4750, ASM-4755, ASM-4756). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3025-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 20 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **NPA and asset manager**, I want **to record maintenance, insurance and custody costs against the asset**, so that **assets sell sooner at approved prices**.

The held property is a property the bank already owns after repossession, deed in lieu or auction purchase, and it sits at `ASSET_HELD` of the DISPOSAL set while it is held (TSD S5 T4). The step is the record of what holding it costs: the maintenance, the insurance and the custody of the asset and its documents. The cost lands on the asset the service owns (`asset`, DF-COL-028 to DF-COL-042, with `holding_cost_to_date` at DF-COL-042), the work order to the property services vendor leaves as a partner instruction through the partner gateway, and the decision record carries the rule ID with the version in force. The app reads the asset, the ACE asset fact and the case state through published contracts, writes no other service's table and publishes no event of its own.

### 2. Business rationale

The asset sits on the bank's books for years: the FSD S5 A2.7.1 measures an NPA sales cycle of 1,486 days against a target of 1,095 days, and it attributes part of the delay to the manual handling of listings and floor prices. A held property that is not maintained, insured or guarded sells later and lower, and today the cost of holding it is invisible to the officer who decides the price. This step makes those costs visible on the asset record, with the rule version that allowed them, so the disposal route and the floor are set with the cost of carry in front of the officer.

The legacy step crossed four boundaries at once: the officer screen, the ACE asset fact read through `v_ace_npa_asset`, the decision log and the case state. The target splits them. rwb-source-data owns the ACE asset and collateral facts, rwb-case owns the case and its route state, rwb-partner owns the partner and the portal instruction, rwb-decision governs the DISPOSAL rule package, and rwb-asset owns the asset record, the cost and the decision record of the step. Each boundary is a published contract with a fake, so the step is built on Day 1 against `RWB-S5-E3025-CON` without waiting for any other service.

Three source defects are recorded and not smoothed over. The feature records costs, yet the legacy AC2 and the FSD S5 A2.7.3.1 attach R-DIS-37, the bid-in-round rule that moves `ROUND_OPEN` to `BID_RECEIVED`, and the routing logic gives the held-property work orders to R-DIS-10, R-DIS-11 and R-DIS-12 (GAP-2864; ASM-4751). The write operation, its closed list and its answer shape are named by no source, and the only write the legacy endpoint table gives is the rwb-valuation valuation order (GAP-2862; ASM-4747, ASM-4748). The custody of documents is P5's fact and the two price messages of the legacy message set belong to the pricing story (GAP-2865; ASM-4754).

### 3. Preconditions

- `RWB-S5-E3025-CON` is baselined: the asset read, the cost element with its closed list, the consumed rwb-source-data and rwb-case rows, the partner-instruction element, the decision-record element and the fakes.
- The service template and the naming library are in force (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule and not a local choice.
- The user holds a Workbench role with the Asset and disposal right the operation declares, in scope (FSD S5 A1.4; TSD S5 T6.1).
- The DISPOSAL package is in force at its version and carries R-DIS-10, R-DIS-11 and R-DIS-12, and the rule rows are governed in rwb-decision (P7). R-DIS-37 is in force as the legacy master gives it (GAP-2864).
- The asset is at `ASSET_HELD`, its `holding_status` is `HELD` of `LOV-HOLDING`, and title is clear or under transfer, because R-DIS-10 is entered only from `ASSET_HELD` (TSD S5 T4; FSD S5 A2.6.3.1).
- The ACE asset and collateral facts answer on the rwb-source-data data-product contract with a freshness stamp; rwb-asset holds no grant on any `v_ace_*` view and reads none (DP-05; GAP-2862; ASM-4752).
- The case state and the case move answer on the rwb-case contract; this story writes no `recovery_case` row (GAP-2862; ASM-4753).
- The property services vendor and its fee schedule answer on the rwb-partner contract, through the partner gateway; this story writes no vendor row (R-DIS-10; GAP-2863; ASM-4750).
- The decision-record library `RWB-PLT-E1027-CON` and the gateway-bff composite route `RWB-PLT-N001-CON` are available, which are the two platform CON stories of the build row.
- No build dependency on another service: the app builds against CON stories and their fakes (Template and Rules §R5.7), and Ready to start is Day 1 because its only non-CON build row is the same-service contract.

### 4. Flow

1. The officer opens SCR-21 Asset list or SCR-22 Asset record through the gateway-bff composite route (DP-19) and selects a held asset; the read answers from `asset` on `/api/recovery/asset/v1` (DP-13).
2. The service reads the asset, the ACE asset fact of the case from rwb-source-data and the case state from rwb-case, each on its published contract, one hop with a 2 s budget (DP-05, DP-11).
3. The officer records a cost: its kind, its amount, its invoice date and its vendor reference, plus the work order it belongs to where one exists.
4. The service validates the required fields (VR-S5-007-1, MSG-GEN-001) and checks the role, the capability area and the scope (MSG-P4-002).
5. The step asks Drools for R-DIS-10, R-DIS-11 or R-DIS-12 at the version in force and receives the outcome with the rule ID and the package version.
6. The service writes the decision record through the local library on the shared `rwb.decision-record.v1` before any row changes (DP-03); a failed write stops the step with MSG-P7-003.
7. On `WORK_ORDER_RAISED` the service raises the work order to the property services vendor as a partner instruction through the L3 kit and the rwb-partner contract, and moves the case to `WORK_ORDER_OPEN` (R-DIS-10).
8. The step waits on a durable timer. On `WORK_ACCEPTED` it releases the invoice for payment, adds the cost to `holding_cost_to_date` and returns the asset and the case to `ASSET_HELD` (R-DIS-11). On `WORK_REFUSED` it blocks the invoice and leaves the work order open (R-DIS-12).
9. The service writes the asset row and the outbox row in one transaction, records the interaction in the ledger of rwb-source-data where the FSD asks for a ledger entry (DP-18), and repeats receive, ask, record and apply, wait.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field of the cost is empty or invalid | Nothing is written; the field is named | MSG-GEN-001 | AC1 |
| X2 | The role lacks the Asset and disposal right, or the asset is outside the scope | The read or the write is refused and no row changes | MSG-P4-002 | AC4 |
| X3 | The decision record cannot be written | Nothing changes; the incident is raised by the library's own alerting | MSG-P7-003 | AC3 |
| X4 | The asset is not at `ASSET_HELD`, or its `holding_status` is not `HELD` | The work order is refused and the state is reported; no cost is written | MSG-GEN-001 | AC1 |
| X5 | The rwb-source-data answer is stale after a late batch | The screen shows the date of the data product and the officer decides whether to continue; the check is the owner's | None stated in the sources (GAP-2865) | AC1 |
| X6 | The rwb-partner contract refuses the instruction or does not answer within 2 s | The work order stays at `ASSET_HELD`, an outbox retry runs, and no cost is released | None stated in the sources (GAP-2863) | AC1 |
| X7 | The bid rule outcome arrives for a case not in `ROUND_OPEN` | The rule is not applied and the round is left open | None stated in the sources (GAP-2864) | AC2 |
| X8 | The rule package is not in force at the version the decision record names | The step stops; the package registry is the owner's | None stated in the sources | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The step is one step of `AssetDisposalWorkflow`, builds against its own CON and the two platform CONs, and reads other services only on published contracts with fakes |
| Negotiable | The operation name, the element names, the closed list and the example values are settled in the contract baseline; the outcomes of R-DIS-10, R-DIS-11 and R-DIS-12 are fixed by the rule package |
| Valuable | The cost of holding a property becomes visible on the asset record and in the decision log, which is what the disposal route and the floor are set on |
| Estimable | One activity, one write surface, one work-order instruction, one read of the ACE fact and one of the case, the decision record, and the assertions on six fakes |
| Small | Fits one sprint with the tests, on top of the baseline |
| Testable | Every criterion is asserted on the asset row, the decision record, the work-order instruction and the case move, on fakes only |

### 7. Acceptance criteria

```gherkin
Feature: Maintain a held property

  Background:
    Given asset "AST-2026-000512" of case "RC-2026-000512" is held with holding_status "HELD"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Maintain a held property (legacy RWB-E3-025 AC1)
    Given the rwb-source-data contract mock returns the ACE asset fact of DF-ACE-208 to DF-ACE-219 for "AST-2026-000512" with its freshness stamp
    Given the rwb-case contract mock returns the case state "ASSET_HELD" for "RC-2026-000512"
    Given the rwb-decision contract mock returns the DISPOSAL package at its version in force
    Given the rwb-partner contract mock returns the work order accepted by the property services vendor
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then records maintenance, insurance and custody costs against the asset
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DIS-37 (legacy RWB-E3-025 AC2)
    Given the rwb-case contract mock returns the case state "ROUND_OPEN" for "RC-2026-000512"
    Given the rwb-partner contract mock returns the bid reported on the auction portal for the open round
    Given a case in state ROUND_OPEN
    When bid placed
    Then record the bid against the round and the asset
    Then the case moves to BID_RECEIVED

  Scenario: AC3 Not recorded (legacy RWB-E3-025 AC3)
    Given the rwb-decision contract mock returns no acknowledgement on rwb.decision-record.v1 and the local decision-record stub returns a stopped chain
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 Access refused (exception X2) (new, D-RCV-60)
    Given the user's role lacks the Asset and disposal right, or the asset is outside the scope
    When the user acts on the screen
    Then the read or the write is refused and no row changes
    Then the user sees MSG-P4-002

  Scenario: AC5 No foreign read, no foreign write and no event from this step (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the ACE asset fact of DF-ACE-208 to DF-ACE-219 for "AST-2026-000512" with its freshness stamp
    Given the rwb-partner contract mock returns the work order accepted by the property services vendor
    When the user acts on the screen
    Then the ACE asset fact is read on the rwb-source-data contract and no v_ace_* view is read
    Then no recovery_case row, no case column and no document row is written or read
    Then the work order leaves through the rwb-partner contract and the step publishes no event

  Scenario: AC6 Error answers of the provided operations (no legacy origin; added by this story) (new, D-RCV-60)
    Given the provided operations of section 12 are called
    Then a request with no valid credential is answered 401
    Then a request by a role that lacks the right is answered 403
    Then a request for an asset not found is answered 404

  Scenario: AC7 Replay of a write with the same idempotency key (no legacy origin; added by this story) (new, D-RCV-60)
    Given the cost write of section 12 has been accepted once with its idempotency_key
    When the same write is replayed with the same idempotency_key
    Then the first answer is returned and no second cost is written

  Scenario: AC8 Activity retry and timeout (no legacy origin; added by this story) (new, D-RCV-60)
    Given the rwb-partner contract mock does not answer within 2 s
    When the work order is raised
    Then the work order stays at "ASSET_HELD", an outbox retry runs and no cost is released

  Scenario: AC9 A consumed call fails (no legacy origin; added by this story) (new, D-RCV-60)
    Given the rwb-decision contract mock returns no rule package in force at the version the decision record names
    When the action is taken
    Then the step stops and nothing changes

  Scenario: AC10 A status change the model does not allow is refused (no legacy origin; added by this story) (new, D-RCV-60)
    Given the rwb-case contract mock returns a case state other than "ASSET_HELD" for "RC-2026-000512"
    When the work order is raised
    Then the work order is refused, the state is reported and no cost is written
```

The first three criteria are the legacy criteria of RWB-E3-025 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `bid placed` and `the decision record cannot be written` all stand, with the decision log wording replaced under CG-ALL-9806. The cross-service parts are mocked, so each criterion carries one or more `Given the <service> contract mock returns <x>` lines, and those added lines are the only additions to the legacy text.

AC2 needs one note. R-DIS-37 is the bid-in-round rule, and the Business Rules and Routing Logic v4 gives it from `ROUND_OPEN` to `BID_RECEIVED` with the auction portal as its channel, while the held-property work orders of the same feature are R-DIS-10, R-DIS-11 and R-DIS-12 (GAP-2864; ASM-4751). The criterion is kept because the legacy master owns it and this story is its owner; the bid itself is recorded against the round and the asset by the round operation API-S5-005, and this story records no bid of its own.

AC4 is added by this story for exception X2, which section 5 covered only by the access case; it has no legacy origin and is tested by TC-E3-025-04. AC5 is added by this story for the cross-service limits of BR7 to BR11 and is tested by TC-E3-025-06 and TC-E3-025-07. AC6 to AC10 are added by this story for the error answers, the replay of a write, the retry and timeout of an activity, a failed consumed call and a disallowed status change; they are tested by TC-E3-025-09 to TC-E3-025-13.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The cost of holding the asset is recorded against the asset: its kind, its amount, its invoice date and its vendor reference are facts of the record, and the running total is `holding_cost_to_date` (DF-COL-042) | TSD S5 T3.1; FSD S5 A2.7.2; ASM-4749 | AC1; TC-E3-025-01, TC-E3-025-07 |
| BR2 | The three cost kinds are maintenance, insurance and custody, read from reference data with its version; no kind, no amount, no threshold and no vendor is a constant of the code | FSD S5 A2.7.3.1 (BR-S5-007); legacy RWB-E3-025 AC1; ASM-4748 | AC1; TC-E3-025-01 |
| BR3 | The decision record is written through the local library on the shared `rwb.decision-record.v1` before the asset row changes; a failed write leaves everything unchanged and shows MSG-P7-003 | DP-03; legacy AC1 and AC3 | AC1, AC3; TC-E3-025-01, TC-E3-025-03, TC-E3-025-05 |
| BR4 | A required field that is empty or invalid stops the step and names the field | VR-S5-007-1; FSD S5 A2.7.3.1 | AC1; TC-E3-025-08 |
| BR5 | A held asset that needs storage, property tax, insurance, security or eviction raises a work order to the property services vendor and moves to `WORK_ORDER_OPEN`; the vendor's invoice is released for payment only when the sale officer accepts it, within 3 working days, and the asset returns to `ASSET_HELD`; a refusal blocks the invoice and leaves the work order open | Business Rules and Routing Logic v4, rows R-DIS-10, R-DIS-11 and R-DIS-12 | AC1; TC-E3-025-01, TC-E3-025-06 |
| BR6 | A bid placed on an open round is recorded against the round and the asset and moves the case to `BID_RECEIVED`, at the package version in force | Business Rules and Routing Logic v4, row R-DIS-37; legacy AC2; GAP-2864 | AC2; TC-E3-025-02 |
| BR7 | The ACE asset, collateral and score facts are read on the rwb-source-data contract or not at all: this service writes no `v_ace_*` read and joins no ACE table | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2862 | AC1, AC5; TC-E3-025-06 |
| BR8 | The case of record, its route state and its move belong to rwb-case: this story requests the move and writes no `recovery_case` row and no case column | Ownership Map (owner P3); GAP-2862; ASM-4753 | AC2, AC5; TC-E3-025-07 |
| BR9 | The custody of documents is P5's fact; this story records the custody cost against the asset and reads no document row | Legacy Data table (`document_custody`, DF-DOC-018 to DF-DOC-024); GAP-2865; ASM-4754 | AC5; TC-E3-025-07 |
| BR10 | The service publishes no event from this step: the catalogue of the service gives it EV-22 only, which the take-on step publishes | _work/msr/context/S5.md (events of S5); GAP-2868; ASM-4755 | AC5; TC-E3-025-06 |
| BR11 | The work order leaves through the L3 partner instruction and the rwb-partner contract behind the partner gateway; no vendor, no fee and no portal address is a value of this service | Architecture v5 slides 8 and 12; GAP-2863; ASM-4750 | AC5; TC-E3-025-06 |

### 9. State transitions

The step moves the asset's case and the work order, and it leaves the holding status where it found it.

| From | Event | Condition | To | Rule |
|---|---|---|---|---|
| `ASSET_HELD` | `WORK_ORDER_RAISED` | storage, property tax, insurance, security or eviction required | `WORK_ORDER_OPEN` | R-DIS-10 |
| `WORK_ORDER_OPEN` | `WORK_ACCEPTED` | `sale_officer_accepted = Y` | `ASSET_HELD` | R-DIS-11 |
| `WORK_ORDER_OPEN` | `WORK_REFUSED` | `sale_officer_accepted = N` | `WORK_ORDER_OPEN` | R-DIS-12 |
| `ROUND_OPEN` | `BID_PLACED` | any | `BID_RECEIVED` | R-DIS-37 (legacy AC2; GAP-2864) |

`holding_status` stays `HELD` of `LOV-HOLDING` through the step; a cost does not list, sell, transfer or rent the asset, and `asset_sale` is not written here. The case state is rwb-case's: this story asks for the move with the rule ID and the package version and never writes the row (BR8). The rule rows and their 40 states are governed in rwb-decision, and the step evaluates three of them at the version in force.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| NPA and asset manager | Records the maintenance, insurance and custody cost and opens the work order (primary actor of FSD S5 A2.7.3.3) |
| Partner and agency manager | Also uses the step (FSD S5 A2.7.3.3) |
| Sale officer | Accepts or refuses the vendor's invoice within 3 working days (R-DIS-11, R-DIS-12) and holds `CRUA` on Asset and disposal |
| Property services vendor | Acts on the work order on the partner portal; never reads a Workbench table |
| Service owner of rwb-asset | Owns the activity, the asset row, the decision record and the work-order instruction |
| Data steward | Confirms that no personal data enters the record, the instruction, an event or a log |
| Rule owner in rwb-decision | Owns R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37 and their versions; this story names them and changes none |
| rwb-access authorise check (DP-08) | Authorises every REST operation of section 12 on the Asset and disposal right with the scope applied, before the operation runs; this story names the check and writes no role or grant |

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Owned table | `asset` in `rwb_asset`: DF-COL-028 to DF-COL-042, with `holding_status` (DF-COL-041) at `HELD` and `holding_cost_to_date` (DF-COL-042) carrying the running cost | DF-COL-028 to DF-COL-042 |
| Library objects in `rwb_asset` | `decision_record` (DP-03), `idempotency_key` and `outbox_event` (DP-09) | DP-03, DP-09 |
| Recorded facts | The cost kind of `LOV-HOLDING-COST` (maintenance, insurance, custody), the amount, the invoice date and the vendor reference; the work order reference, the vendor and the date accepted (ASM-4748, ASM-4749) | Not specified in the source documents (DOR-RWB-S5-E3025-APP-7) |
| Reference data read | The cost kind list `LOV-HOLDING-COST` (maintenance, insurance, custody) read through the reference-data contract of DP-06 and DP-07 with its version; the rule rows R-DIS-10, R-DIS-11 and R-DIS-12 read from rwb-decision at the version in force; no kind, amount, threshold or vendor is a constant of the code (BR2) | DP-06, DP-07 |
| ACE asset fact (consumed) | DF-ACE-208 to DF-ACE-219 of `v_ace_npa_asset` and the collateral and score facts, read on the rwb-source-data data product with its freshness stamp, never copied and never written (DP-05; GAP-2862) | DF-ACE-208 to DF-ACE-219 |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the asset row changes (DP-03) | DF-DEC-001 to DF-DEC-018 |
| Not owned here | `recovery_case` and `timer` (P3), `document` and the custody of documents (P5), `decision_log_entry` and `rule_row` (P7), `proceeds` and the posting (P8), `partner_instruction` (S9), `listing` and `asset_sale` (S5, the pricing and auction stories') | None (not owned here) |
| Not specified in the sources | The cost element and its closed list, the work-order instruction and its answer, and the operation names of the consumed reads: Not specified in the source documents (GAP-2862, GAP-2863, GAP-2867; ASM-4747, ASM-4748, ASM-4750) | Not specified in the source documents (DOR-RWB-S5-E3025-APP-7) |

No new table, no new column and no migration is declared by this story: the cost is recorded on the columns the data model already gives, and whether the DB story of this service adds a cost table is a step D1 decision (ASM-4749).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets/{assetId}` | Asset out, with its holding status, its holding cost to date and its listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |
| POST | The cost write, operation name Not specified in the source documents (GAP-2862; ASM-4747) | The cost element in, the asset with its new `holding_cost_to_date` and the work-order reference out (ASM-4747) | Asset and disposal, right C, scope applied | `Idempotency-Key` required |

The read answers 401, 403 with MSG-P4-002, 404 and 503; the write answers 400 with MSG-GEN-001, 401, 403 with MSG-P4-002, 404, 409, 422 and 503. `GET /assets`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings` and `POST /listings/{listingId}/rounds` are the other operations of the service and belong to the stock, pricing and round stories; API-S5-003 `POST /assets/{assetId}/valuations` is rwb-valuation's under ASM-0043. None of them is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| The DP06 Collateral and assets read (operation name Not specified in the source documents (GAP-2862; ASM-4747)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE asset fact of DF-ACE-208 to DF-ACE-219 with the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and its route state; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2862; ASM-4753)) | rwb-case (P3) | P3 rwb-case | The move to `WORK_ORDER_OPEN`, `ASSET_HELD` or `BID_RECEIVED` with the rule ID and its version; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The rows are class C in fact while the metadata row reads None, because the plan records no contract dependency for this key (GAP-2862, GAP-2863).

#### 12.3 Events published

None. The service publishes EV-22 `AssetTakenOn` from its take-on step and no catalogue event covers a holding cost or a work-order state, so this step writes the outbox row of its own transaction only and publishes nothing (BR10; GAP-2868; ASM-4755).

#### 12.4 Events consumed

None declared by this step. The S5 row of the connection matrix shows subscribes cells towards S4, S9 and P8, and no source names the events or their data for a held-property cost, so this story consumes nothing and the vendor answer arrives on the partner instruction of 12.5 (GAP-2868; ASM-4755).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`; workflow ID form and start rule: Not specified in the source documents (CG-ALL-9801) | `rwb-asset` | The stage that hosts the holding step; its timer and its outcome for the parent |
| `recordHoldingCost` | Activity (design name) | `rwb-asset` | The cost element (closed list LOV-HOLDING-COST) written once on `/api/recovery/asset/v1` as an additive write and recorded on holding_cost_to_date; a custody cost is recorded against the asset with no document row read (GAP-2862, GAP-2865); the rule ID with the package version, the asset update and the decision record out |
| `raiseWorkOrder` | Activity (design name) through the L3 partner instruction kit | `rwb-asset` | The work order to the property services vendor on the rwb-partner contract; the instruction reference back |
| `applyWorkOrderAnswer` | Activity (design name) | `rwb-asset` | The accepted or refused invoice, the cost released and the case move out |

The timer of 3 working days of R-DIS-11 is a durable timer of the workflow, not a Quartz row, a Schedule or a case timer. The two activity names are design names with no source and are settled in the contract baseline review (GAP-2863, GAP-2867), which publishes the cost element with its closed list, the work-order instruction row and the case-move row. This step publishes and consumes no event; the outbox and inbox library RWB-PLT-TE006-CON is a build dependency of the asset row and outbox write (GAP-2868).

#### 12.6 Schedules

None. The FSD S5 A2.7.4.4 declares no background event for the feature, the step runs from the officer action and from the vendor answer, and JOB-19 Re-appraisal monthly is the single Schedule of the service and belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `asset` | S5 (`rwb_asset`) | The held asset, its `holding_status` and its `holding_cost_to_date` |
| `decision_record` | PLT library, created in `rwb_asset` | The local hash-linked record of the rule outcome (DP-03) |
| `idempotency_key` | PLT library, created in `rwb_asset` | The key of a repeated cost request and the answer it holds |
| `outbox_event` | PLT library, created in `rwb_asset` | The relay row of the step; the step publishes no event of its own (BR10) |
| Round, bid and holding-cost movement (entity groups) | Owned in `rwb_asset` (S5): the auction round and the bid placed on it, and the cost movement that adds to `holding_cost_to_date`; physical table names left to the S5 DB story (GAP-1752) | None (entity group) |

`recovery_case` and `timer` (P3), `document` and the custody of documents (P5), `proceeds` (P8), `partner_instruction` (S9), `decision_log_entry` and `rule_row` (P7), `listing` and `asset_sale` (S5, the pricing and auction stories') and every `v_ace_*` view (P1) are not owned here, and no foreign key leaves `rwb_asset` (DP-01, BR7).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The ACE asset fact of `AST-2026-000512` for case `RC-2026-000512` with its collateral, its segment, its book value and its freshness stamp; a stale product; no answer beyond 2 s | AC1 |
| rwb-case state and move fake | The states `ASSET_HELD`, `WORK_ORDER_OPEN` and `ROUND_OPEN` of `RC-2026-000512`; an accepted move and a refused move | AC1, AC2 |
| rwb-partner instruction fake | The work order accepted by the property services vendor with its instruction reference; a refusal; a bid reported on the open round | AC1, AC2 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37; a package out of force | AC1, AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC3 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for `RC-2026-000512` | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The cost element, its closed list and the work-order answer have no published shape until the baseline of `RWB-S5-E3025-CON` fixes them, so the fakes derive from that document and carry the placeholder until it is baselined (GAP-2862, GAP-2863, GAP-2867).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The asset read and the cost write on `/api/recovery/asset/v1`; the rwb-source-data data-product read, the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record is the library's on `rwb.decision-record.v1` (DP-03) |
| Temporal | 1 workflow, 3 activities, 1 durable timer | `AssetDisposalWorkflow` on `rwb-asset`, the partner instruction through the L3 kit, the 3-working-day timer of R-DIS-11; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Deliverables.** One activity `recordHoldingCost` inside `AssetDisposalWorkflow`, the write surface the baseline publishes, the work order through the partner instruction kit, the decision record through the local library, the read of the ACE fact and of the case state, the asset and `holding_cost_to_date` update, and the test doubles of six fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP13 | `/api/recovery/v1` | `/api/recovery/asset/v1` | none |
| DP19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is applied as a prohibition: the service holds no `v_ace_*` grant, so the ACE asset and collateral facts are consumed on the rwb-source-data contract only (BR7; GAP-2862; ASM-4752). DP-13 moves the base and nothing else, and DP-19 puts SCR-21 and SCR-22 behind the composite route, whose screen model is the edge contract's. The pattern table adds the two platform CON rows the metadata table carries, and it adds nothing else.

**Build steps**

1. Generate the activity and its workflow step from the service template, on queue `rwb-asset`.
2. Wire the read of the asset and of the ACE fact, with the 2 s budget and the breaker.
3. Implement the cost record against the element and the closed list of the baseline, with VR-S5-007-1 and the right check.
4. Wire the rule evaluation of R-DIS-10, R-DIS-11 and R-DIS-12 at the version in force, and the R-DIS-37 outcome as the legacy criterion gives it.
5. Write the decision record before the row changes and prove the stopped-chain path.
6. Raise the work order through the partner instruction kit and apply the accepted and refused answers, with the durable timer.
7. Update `holding_cost_to_date` and the case move in one transaction, then write the test doubles of 12.8 and the assertions of the five legacy cases.

**Done when.** The three criteria and the five legacy cases pass on the fakes, the decision record is written before every change, the work order is answered in both directions, no `v_ace_*` read and no `recovery_case` write exists in the build, and the contract baseline has accepted the element, the list and the instruction shape.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it (GAP-2865) | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it (GAP-2865) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of the cost is absent or invalid (VR-S5-007-1), or the asset is not at `ASSET_HELD` | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares, or the asset is out of scope | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the asset row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are the legacy set of RWB-E3-025, copied unchanged; no message is reworded and no new one is added. The two price messages are carried because the legacy set holds them, and the paths that raise them belong to the pricing and re-appraisal stories (GAP-2865).

### 15. Screens and states

SCR-21 Asset list in its loading and list states (empty, error and no access: Not specified in the source documents (CG-ALL-9807)), and SCR-22 Asset record in its take-on, held, listed and sold states (empty, loading, error and no access: Not specified in the source documents (CG-ALL-9808)), both through the gateway-bff composite route (DP-19). This step works on the held state: it shows the holding status, the cost to date and the open work order with the vendor and the date accepted. The composite route calls rwb-asset for the asset and its holding cost, rwb-case for the case state, rwb-source-data for the ACE asset fact and rwb-partner for the vendor and the instruction; the route specification and the screen field list belong to `RWB-PLT-N001-CON`, and this story fixes no screen field. The refusal, not-recorded and stale-data states show the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-025-01 | AC1 | Component | Held asset `AST-2026-000512` of case `RC-2026-000512`; the maintenance, insurance and custody cost recorded, the decision record written with its rule version, the asset row and `holding_cost_to_date` asserted on the fakes |
| TC-E3-025-02 | AC2 | Component | Case `RC-2026-000512` at `ROUND_OPEN` with a bid on the open round; the bid recorded against the round and the asset and the `BID_RECEIVED` move asserted |
| TC-E3-025-03 | AC3 | Component | The decision-record stub stopped; no asset change, no work order and MSG-P7-003 shown |
| TC-E3-025-04 | AC4 (Access, X2) | Component | A role without the Asset and disposal right; the write refused with MSG-P4-002 and nothing changed |
| TC-E3-025-05 | Principle 5 | Component | A forced decision record write failure at the moment of the insert; no row, no instruction and no answer |
| TC-E3-025-06 | AC5; operations, events and activities of section 12 | Contract | The cost write of section 12 (POST) and the consumed reads checked against the published contracts of their owners; the step's events asserted absent (BR10) |
| TC-E3-025-07 | AC5; tables of section 12.7 | Boundary | Each table of section 12.7 exercised at the edge of its contracted use (asset, decision_record, idempotency_key, outbox_event); the non-owned tables asserted unwritten and no foreign key out of rwb_asset |
| TC-E3-025-08 | AC1 (X1; BR4) | Component | A required field of the cost empty or invalid; nothing written and the field named with MSG-GEN-001 |
| TC-E3-025-09 | AC6 (error answers 401, 403, 404) | Contract | The provided operations of section 12 called without a valid credential, by a role lacking the right and for an asset not found; answers 401, 403 and 404 asserted |
| TC-E3-025-10 | AC7 (replay, same idempotency key) | Component | The cost write of section 12 accepted once and replayed with the same idempotency_key; one cost row and the first answer asserted |
| TC-E3-025-11 | AC8 (X6; retry and timeout) | Component | The rwb-partner contract mock silent beyond 2 s; the work order at `ASSET_HELD`, the outbox retry and no released cost asserted |
| TC-E3-025-12 | AC9 (X8; failed consumed call) | Component | The rwb-decision contract mock returns no package in force at the version the decision record names; the step stopped and nothing changed asserted |
| TC-E3-025-13 | AC10 (X4; disallowed status change) | Component | Case `RC-2026-000512` in a state other than `ASSET_HELD`; the work order refused, the state reported and no cost written asserted |

The first five cases are the legacy cases of RWB-E3-025 in their legacy order, with the Level column added: the legacy level `System` maps to `Component` because the step is tested on its own fakes, and no case is end to end because the build holds no I dependency. TC-E3-025-06 (Contract), TC-E3-025-07 (Boundary) and TC-E3-025-08 (Component, X1) are added by this story; their Given, When and Then follow in the next Test Cases version under the same IDs. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in code: the cost kinds, the amounts, the 3-working-day term, the lists and the rule rows stay reference data or rule rows; a change of a value is a data change, not a build (BR2).
- No personal data in the record, the partner instruction, the outbox, a workflow input or a log: identifiers, codes, amounts, dates and a rule version only.
- ACE data only through the owner's contract or a `v_ace_*` view this service actually holds, which is none (BR7).
- No read of another service's table and no foreign key out of `rwb_asset`: the case is rwb-case's, the documents are P5's, the vendor and the instruction are rwb-partner's (DP-01).
- The decision record is written before the change, in the same transaction as the row, and a failure stops the action (BR3).
- No schedule, no Quartz row and no shared job table: the timer is the workflow's durable timer and the schedule of the service belongs to another story.
- No event is published without a catalogue row; a step that needs one raises the catalogue change first (BR10).
- No retired element is reintroduced: no data lake write, no shared service login and no monolith base.

### 18. Traceability

| Requirement ID | Requirement (short) | Element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| FEAT-AST-07 (requirement id Not specified in the source documents (GAP-2866; ASM-4756)) | Records maintenance, insurance and custody costs against the asset (FSD S5 A2.7; Epics 3 to 8 Specification v3) | The cost record, the work order, the decision record and the case move | TC-E3-025-01, TC-E3-025-04 | FEAT-AST-07 | Not specified in the source documents (DOR-RWB-S5-E3025-APP-2) |
| BR-S5-007 | No value a business person may change is written in code; it is read from reference data with its version | The closed list of the cost kinds and the rule rows | TC-E3-025-01, TC-E3-025-05 | FEAT-AST-07 | Not specified in the source documents (DOR-RWB-S5-E3025-APP-2) |
| R-DIS-10, R-DIS-11, R-DIS-12 | The work order to the property services vendor, its acceptance and its refusal | The work-order instruction and the durable timer | TC-E3-025-01 | FEAT-AST-07 | Not specified in the source documents (DOR-RWB-S5-E3025-APP-2) |
| R-DIS-37 | Record the bid against the round and the asset, and move to `BID_RECEIVED` | The bid outcome of the legacy criterion | TC-E3-025-02 | FEAT-AST-07 | Not specified in the source documents (DOR-RWB-S5-E3025-APP-2) |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The decision record and the outbox row | TC-E3-025-05 | FEAT-AST-07 | Not specified in the source documents (DOR-RWB-S5-E3025-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget | TC-E3-025-01 | FEAT-AST-07 | Not specified in the source documents (DOR-RWB-S5-E3025-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-025, disposition Split (rework) |
| Legacy criteria | AC1 to AC3, owned word for word by this story; AC4 and AC5 added by this story |
| Test cases | TC-E3-025-01 to TC-E3-025-08 |
| Feature and screens | FEAT-AST-07; SCR-21 Asset list and SCR-22 Asset record; states of both screens: no access is X2 (MSG-P4-002); empty, loading and error states are Not specified in the source documents (DOR-RWB-S5-E3025-APP-10) |
| Rules | R-DIS-10, R-DIS-11, R-DIS-12 and R-DIS-37, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-019, ADR-020, ADR-022 |

### 19. Out of scope

- The contract baseline of the step: `RWB-S5-E3025-CON`, which fixes the element, the closed list, the consumed rows, the instruction and the fakes.
- The holding-age clock, the provision steps and the monthly cost of carry of R-DIS-06: the holding stories of this service, with the posting itself in rwb-payment (P8).
- The re-appraisal of the asset and JOB-19: the re-appraisal story of this service, and rwb-valuation (S1) for the valuation itself.
- The listing, the floor price and the auction rounds, and the bid that R-DIS-37 records: the pricing, listing and round stories of this service, with API-S5-004 and API-S5-005.
- The eviction of occupants on the same held asset: RWB-S5-E4021-APP of wave 3, which starts from `EVICTION_REQUIRED` of R-DIS-13.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The ACE NPA asset, collateral and score facts and the freshness of the data product: rwb-source-data (P1).
- The property services vendor, its fee schedule and the partner portal: rwb-partner (S9) and the partner gateway.
- The custody of the documents themselves: rwb-document (P5).
- The authoring, testing, approval and versioning of the DISPOSAL package and of the four rule rows: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: `RWB-PLT-N001-CON` and the edge stories.
- The deployment, the flags, the dashboards, the alerts and the runbook of this step: the operations story of this legacy key.
