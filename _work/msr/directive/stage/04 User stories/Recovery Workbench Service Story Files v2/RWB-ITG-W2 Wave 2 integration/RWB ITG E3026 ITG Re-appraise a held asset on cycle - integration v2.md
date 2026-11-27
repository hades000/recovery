# RWB-ITG-E3026-ITG Re-appraise a held asset on cycle

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E3026-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E3026-APP (build not done; this story builds against the published owner documents and their fakes on Day 1) |
| Contract dependencies | RWB-S5-E3026-CON; RWB-PLT-E1071-CON (wave 0 library the Schedule of RWB-S5-E3026-APP needs) |
| Contract version | v1 (path version used in §12.2); exact contract version not specified in the source documents (DOR-RWB-ITG-E3026-ITG-23) |
| Integration dependencies | RWB-S5-E3026-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Size | Not specified in the source documents (DOR-RWB-ITG-E3026-ITG-16); the squad sizes it at refinement |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-026 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E3026-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **one repeatable cross-service journey harness that carries a held asset from ASSET_HELD through the monthly re-appraisal cycle on rwb-asset, the order to SVAF through the rwb-integration outbound interface, the decision record in rwb-decision, the appraisal value read back through the ACE views on rwb-source-data, the accept, re-order and re-list outcomes and the state the owning service reaches**, so that **an asset never sits past its re-appraisal interval without an order in flight, and the value that resets the list and the floor price is the value the valuer actually reported**.

This story owns only AC3 of the legacy key. AC1, AC2 and AC4 are owned by the app story of this legacy key, RWB-S5-E3026-APP, and the harness observes their effects where the AC3 journey passes through them; it adds no criterion of its own for built behaviour.

### 2. Business rationale

The NPA sales cycle runs at 1,486 days today (Temporal and Drools Design, slide on the asset disposal stage). A held asset that is never re-appraised keeps a stale value on the list price and on the floor, so it either fails to sell at a price the bank may approve or sells at a price the latest valuation no longer supports. The cycle is the control that stops that: the monthly JOB-19 Re-appraisal Schedule on rwb-asset looks for an appraisal older than 12 months with one_year_rule_applied = N (R-DIS-15), orders the re-appraisal through the rwb-valuation contract, and the case moves to REAPPRAISAL_ORDERED. The value then comes back through the ACE views, R-DIS-16 and R-DIS-17 accept it and reset the list and floor price inputs (ASSET_HELD), R-DIS-18 re-orders the appraisal when the officer rejects it, and R-DIS-44 re-lists a NO_BID_AT_FLOOR asset and orders a re-appraisal where the cycle is due (RELISTED).

That chain crosses four services and four call types: the Schedule, the rules and the state on rwb-asset, the outbound interface config and the outbound item on rwb-integration, the appraisal and holding facts read only by rwb-source-data from v_ace_valuation and v_ace_npa_asset, the decision record on the local decision-record library and the shared topic, the case read on rwb-case and the authorisation on rwb-access. A defect at any hop shows up as an order that never left, a value that never came back, or a state the screen does not reflect. This story proves that chain with one run per business date on a fixed clock, and it carries REQ-S5-003 and REQ-RDF-004 and FEAT-AST-09 into evidence.

The harness is decoupled the way the services are: it calls each owner's base `/api/recovery/<short>/v1` and never a monolith base (DP-13, DP-01), it calls through the gateway-bff composite route where a screen would (DP-19), the decision record is read from rwb-decision and its library and topic (DP-03), the appraisal and holding facts are read through rwb-source-data's data-product contract and never from a table (DP-05), and the monthly run is exercised on the Schedule in rwb-asset and not on a Quartz row (DP-10, exercised, not owned).

### 3. Preconditions

- The Asset and disposal journey data are seeded at the asset in state ASSET_HELD with an appraisal_date older than 12 months and one_year_rule_applied = N, which is the R-DIS-15 condition; the fixed clock, the seeded appraisal age, the harness environment, the data seeding set and the evidence format and retention are Not specified in the source documents (GAP-0427; ASM-0603).
- The re-appraisal order goes to the rwb-valuation contract and the harness reads the order it produces; the interface ID, the file pattern and the fixture contents are Not specified in the source documents (GAP-0427; ASM-0603).
- The published contracts of rwb-asset, rwb-integration, rwb-source-data, rwb-decision, rwb-case and rwb-access are in the contract registry, and a WireMock stub set is generated from each one, so the harness runs green from Day 1 before RWB-S5-E3026-APP is live.
- The data product DP06 Collateral and assets is readable through the rwb-source-data contract (DP-05), and the rule package that carries R-DIS-15, R-DIS-16, R-DIS-17, R-DIS-18 and R-DIS-44 is in force in rwb-decision with a known version; the harness reads both and sets neither.
- The R-DIS-15 input flag one_year_rule_applied is readable as data on the asset of the case under test; its field ID in the data dictionary is Not specified in the source documents (GAP-0427; ASM-0603).
- The access rights of the Asset and disposal capability area with right R are in force on rwb-access for the seeded role, and the refusal path for a role without R is available.
- No build dependency. Day 1, with the fakes in place from the first run, and each fake replaced by the real service as RWB-S5-E3026-APP and the other owners' stories land.

### 4. Flow

1. Harness: fixes the run clock at the business date of the run, so the monthly JOB-19 Re-appraisal Schedule on rwb-asset runs once inside the window and every date in the run is derived from the clock rather than from a live calendar (DP-10). The clock fixture and the window control are Not specified in the source documents (GAP-0427; ASM-0603).
2. Harness: seeds the asset of the case under test in state ASSET_HELD through the owning services' published operations only, with the appraisal_date older than 12 months and one_year_rule_applied = N; it asserts the state first with `GET /api/recovery/asset/v1/assets/{assetKey}` and the case with `GET /api/recovery/case/v1/cases/{caseId}`.
3. Harness: asserts the appraisal and holding facts the cycle reads are returned by the data product DP06 through `GET /api/recovery/source-data/v1/data-products/{productCode}/records`: appraisal_date and appraised_value over v_ace_valuation, and asset_key, transfer_in_date and book_value over v_ace_npa_asset, with the freshness stamp of the ACE batch. The asset service never reads the ACE views itself; only rwb-source-data reads them (DP-05, DP-01).
4. Harness: releases the fixed clock to the JOB-19 window and asserts that rwb-asset applies R-DIS-15: the from_state is ASSET_HELD, the event is REAPPRAISAL_CYCLE_DUE and the condition is the appraisal older than 12 months with one_year_rule_applied = N, read from the rule row the service loaded.
5. Harness: asserts the state of the asset becomes REAPPRAISAL_ORDERED on `GET /api/recovery/asset/v1/assets/{assetKey}`, and that the case reflects the move.
6. Harness: asserts the re-appraisal order left through rwb-integration's outbound interface: one outbound item on `GET /api/recovery/integration/v1/admin/outbound-items` for the SVAF interface, carrying the asset and the case, and one outbox delivery on `GET /api/recovery/integration/v1/admin/outbox/deliveries`; the interface config row carries the interface ID and DP06 as its data product.
7. Harness: subscribes to `rwb.integration.events.v1` and asserts `rwb.integration.FileDelivered.v1` for the SVAF order file, or `rwb.integration.FileFailed.v1` and the retry path when the fixture forces a refusal.
8. Harness: asserts exactly one decision record for the cycle, on `GET /api/recovery/decision/v1/decision-log` and on `rwb.decision.DecisionRecorded.v1` from `rwb.decision-record.v1`, carrying the case, the rule R-DIS-15 and its rule version; the record, the asset state change and the outbox row are one transaction, so a cycle that fired leaves all three or none.
9. Harness: plays the valuer through the SVAF fixture and reads the reported value back through the same DP06 data-product contract (R-DIS-16), then asserts the accept path: R-DIS-17 updates the appraised value and resets the list and floor price inputs, and the asset returns to ASSET_HELD.
10. Harness: repeats the receipt with a value the officer rejects and asserts R-DIS-18: the appraisal is re-ordered, the reason is recorded on the decision record, and the asset is REAPPRAISAL_ORDERED again.
11. Harness: seeds an asset in NO_BID_AT_FLOOR inside the re-list limit, applies the re-list and asserts R-DIS-44: the asset is re-listed, a re-appraisal is ordered where the cycle is due, and the state is RELISTED.
12. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` with Asset and disposal right R, and records the refusal path for a caller without R.
13. Harness: writes one run report per business date keyed by story and business date, with the criterion and its assertions, and holds the wave gate on the result.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC3 |
| X2 | The JOB-19 window does not open inside the run window on the fixed clock | The run fails and the report names the window and the clock fixture; the run is not marked passed | None | AC3 |
| X3 | R-DIS-15 does not fire although the appraisal is older than 12 months and one_year_rule_applied = N | The run fails and the report names the rule row, the rule version and the two input values | None | AC3 |
| X4 | The order is applied but no outbound item exists on the SVAF interface | The run fails on AC3 regardless of the state; the report names the interface config row | None | AC3 |
| X5 | `rwb.integration.FileFailed.v1` is the outcome of the SVAF order file | The run fails on AC3, because the order has not reached SVAF; the report names the outbound item, the failure and the retry path the owner recorded | None | AC3 |
| X6 | The decision record is written twice for one cycle, or once without the state change | The run fails and the report counts the records and names the state | None | AC3 |
| X7 | The decision record cannot be written | Nothing moves: the asset stays ASSET_HELD and the order is not raised; the run asserts the message and the unchanged state | MSG-P7-003 | AC3 |
| X8 | The appraisal comes back but the officer rejects it | The run asserts R-DIS-18: a new order and a reason on the record, and the asset back in REAPPRAISAL_ORDERED; the rule set carries no message ID for the rejection | None | AC3 |
| X9 | A caller without Asset and disposal right R is authorised | The run fails on the access check and the report names the operation | MSG-P4-002 | AC3 |

The report text is for the wave entry check and is not part of the message standard. The business messages the journey produces are in section 14 and are asserted as data on the asset, the decision record and the outbound item.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the fakes from Day 1; the only wait is RWB-S5-E3026-APP, and the other owners replace their fakes one at a time |
| Negotiable | The fixed clock, the fixtures, the interface ID and the report shape are configuration agreed at the wave entry check, not business values in code |
| Valuable | The re-appraisal cycle, the SVAF order and the value that resets the price inputs are proven across services before the wave opens |
| Estimable | One harness runner, one stub set, one cycle fixture on a fixed clock, one run report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against the fakes on Day 1 and again against the real rwb-asset when RWB-S5-E3026-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Re-appraise a held asset on cycle

  Background:
    Given the run clock is fixed at the business date of the run, so the monthly JOB-19 Re-appraisal Schedule on rwb-asset runs once inside the window
    Given the asset of the case under test is in state "ASSET_HELD" with an appraisal_date older than 12 months and one_year_rule_applied "N"

  Scenario: AC3 Rule R-DIS-15 (legacy RWB-E3-026 AC3)
    Given a case in state ASSET_HELD
    When reappraisal cycle due
    Then order the re-appraisal through the rwb-valuation contract
    Then the case moves to REAPPRAISAL_ORDERED

  Scenario: AC5 The business rules BR1 to BR10 are asserted against their owning services and published contracts and none is re-implemented (new, D-RCV-60)
    Given the case under test and its asset are seeded through published owner operations only
    When the cycle runs on the fixed clock
    Then each rule BR1 to BR10 is asserted against its owning service and published contract
    Then the harness re-implements none of the rules

  Scenario: AC6 A redelivered consumed event is applied once (new, D-RCV-60)
    Given a consumed event has already been applied to the case under test
    When the same event is delivered again
    Then the case state and the decision record are written once

  Scenario: AC7 A consumed call that fails or does not answer does not change the case state (new, D-RCV-60)
    Given a consumed call on the case under test is set to fail or to not answer
    When the cycle runs on the fixed clock
    Then the case state is unchanged

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case in state ASSET_HELD
    When a status change the model does not allow is requested on the case under test
    Then the change is refused
    Then the case state is unchanged
```

AC1, AC2 and AC4 are owned by the app stories of this legacy key (RWB-S5-E3026-APP) and are not restated here; AC3 is the cross-service criterion this ITG copy owns, and the harness asserts it as one journey across rwb-asset, rwb-integration, rwb-source-data, rwb-decision, rwb-case and rwb-access.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | A held asset whose appraisal_date is older than 12 months and whose one_year_rule_applied is N is ordered for re-appraisal through the rwb-valuation contract, and the state moves from ASSET_HELD to REAPPRAISAL_ORDERED | R-DIS-15; REQ-S5-003; FEAT-AST-09 | AC3, AC5; TC-E3-026-03-ITG, TC-E3-026-07-ITG |
| BR2 | The re-appraisal order is sent through the rwb-valuation contract and the accepted value and its date are read back through rwb-source-data; rwb-asset does not send a file itself | Architecture v5 slide 13 connection matrix (GAP-1758) | AC5; TC-E3-026-07-ITG |
| BR3 | The reported value is recorded and the outlier check runs before any officer sees it | R-DIS-16 | AC5; TC-E3-026-07-ITG |
| BR4 | An accepted value updates the appraised value and resets the list and floor price inputs, and the asset returns to ASSET_HELD | R-DIS-17 | AC5; TC-E3-026-07-ITG |
| BR5 | A rejected value re-orders the appraisal and records the reason, and the asset stays in REAPPRAISAL_ORDERED | R-DIS-18 | AC5; TC-E3-026-07-ITG |
| BR6 | A NO_BID_AT_FLOOR asset inside the re-list limit is re-listed and a re-appraisal is ordered where the cycle is due, and the state is RELISTED | R-DIS-44 | AC5; TC-E3-026-07-ITG |
| BR7 | The holding age clock starts when the asset is taken on and the provision step clock runs from it; this story reads the holding facts the cycle uses and asserts neither clock | R-DIS-06; R-DIS-09 | AC5; TC-E3-026-07-ITG |
| BR8 | Every cycle writes one decision record with the rule ID and the rule version, and the record, the state change and the outbox row are one transaction | Principle 5; R-UNI-39; DP-03; Temporal and Drools Design slide 11 | AC5; TC-E3-026-07-ITG |
| BR9 | An appraisal more than a year old is warned to the user before pricing | MSG-S5-002 | AC5; TC-E3-026-07-ITG |
| BR10 | The appraisal and the holding facts are read from the ACE views through rwb-source-data only, never from a table of another service | DP-05; DP-01; REQ-RDF-004 | AC5; TC-E3-026-07-ITG |

The harness asserts these ten rules against the owning services and the published contracts; it re-implements none of them and changes no BR row. Reference data: the holding thresholds, step sizes and re-appraisal interval are read as versioned parameters from the parameter catalog under reference-data contracts DP-06 and DP-07. They are owned by the NPA and asset manager, their values are Not specified in the source documents (GAP-1468), and the loaded version is shown on the asset record. The appraisal reference, type, value and date are read as an appraisal view of the consumed fact on v_ace_valuation and are not columns of rwb_asset; the reason vocabulary and the inputs one_year_rule_applied and relist_count are versioned inputs whose lists and field IDs are Not specified in the source documents (GAP-2870) until the baseline review fills them before the baseline is tagged.

### 9. State transitions

The harness changes no business state. It seeds through the owning services' published operations, drives the Schedule on a fixed clock, and asserts the states the owners reached.

| From | Event | Condition | To | Rule |
|---|---|---|---|---|
| ASSET_HELD | REAPPRAISAL_CYCLE_DUE | appraisal_date older than 12 months and one_year_rule_applied = N | REAPPRAISAL_ORDERED | R-DIS-15 |
| REAPPRAISAL_ORDERED | VALUER_REPORTED then VALUE_ACCEPTED | outlier_flag = N or officer_accepted = Y | ASSET_HELD, with the list and floor price inputs reset | R-DIS-16, R-DIS-17 |
| REAPPRAISAL_ORDERED | VALUER_REPORTED then VALUE_REJECTED | officer_accepted = N | REAPPRAISAL_ORDERED, with the reason recorded and a new order raised | R-DIS-16, R-DIS-18 |
| NO_BID_AT_FLOOR | RELIST_RULE_APPLIED | relist_count below the re-list limit | RELISTED, with a re-appraisal ordered where the cycle is due | R-DIS-44 |

REAPPRAISAL_RECEIVED is the intermediate state R-DIS-16 sets between the report and the accept or the reject; the harness asserts the end state the owning service reaches and not that intermediate row.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| The monthly cycle finds a stale appraisal | rwb-asset, on the JOB-19 Re-appraisal Schedule | The rule row R-DIS-15 fired with the from_state ASSET_HELD and the two input values (TC-E3-026-03-ITG) |
| The order is raised | rwb-asset, through rwb-integration's outbound interface | One outbound item on the SVAF interface and one outbox delivery (TC-E3-026-03-ITG) |
| The order file reaches the interface or fails | rwb-integration | `rwb.integration.FileDelivered.v1` or `rwb.integration.FileFailed.v1` on `rwb.integration.events.v1` (TC-E3-026-03-ITG) |
| One decision record with the rule version | the decision-record library in rwb-asset, collected by rwb-decision | One entry on `GET /api/recovery/decision/v1/decision-log` with R-DIS-15 and its version (TC-E3-026-03-ITG) |
| The asset state moves | rwb-asset | ASSET_HELD, REAPPRAISAL_ORDERED, RELISTED and NO_BID_AT_FLOOR read back on the asset (TC-E3-026-03-ITG) |
| The value resets the price inputs | rwb-asset, on the value read back through rwb-source-data | The appraised value and the reset list and floor price inputs (TC-E3-026-03-ITG) |

The case status moves are made by P3 on the events rwb-asset publishes. A state the harness set by hand would prove nothing, so the report names the owner and the operation that made each move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Reads the asset, its price inputs and its re-appraisal state through the rwb-asset contract; owns the journey case for the run |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL and the other roles with Asset and disposal R | Read the same journey evidence; the legacy permission table lists 31 roles with right R on Asset and disposal |
| QA lead | Owns the harness configuration, the fixed clock, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-asset, rwb-integration, rwb-source-data, rwb-decision, rwb-case and rwb-access make every state change the harness asserts |
| No approval level from the delegation of authority applies | The harness takes no business decision; the floor approval and the route approval are other stories |

Authorisation is answered by rwb-access on `POST /api/recovery/access/v1/authorise` for every call, and the harness asserts the refusal of a role without Asset and disposal right R.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read, through the rwb-case contract |
| DF-CAS-002 | recovery_case | case_no | Read, through the rwb-case contract |
| DF-CAS-005 | recovery_case | status | Read, through the rwb-case contract |
| DF-CAS-007 | recovery_case | route_state | Read, through the rwb-case contract |
| DF-CAS-021 | recovery_case | rule_version | Read, through the rwb-case contract |
| DF-ACE-187 | v_ace_valuation | valuation_key | Read through the rwb-source-data data-product contract |
| DF-ACE-188 | v_ace_valuation | asset_key | Read through the rwb-source-data data-product contract |
| DF-ACE-189 | v_ace_valuation | appraisal_no | Read through the rwb-source-data data-product contract |
| DF-ACE-190 | v_ace_valuation | appraisal_type | Read through the rwb-source-data data-product contract |
| DF-ACE-191 | v_ace_valuation | appraised_value | Read through the rwb-source-data data-product contract |
| DF-ACE-193 | v_ace_valuation | appraisal_date | Read through the rwb-source-data data-product contract; the R-DIS-15 age input |
| DF-ACE-195 | v_ace_valuation | data_as_of | Read through the rwb-source-data data-product contract |
| DF-ACE-208 | v_ace_npa_asset | asset_ref | Read through the rwb-source-data data-product contract |
| DF-ACE-209 | v_ace_npa_asset | asset_key | Read through the rwb-source-data data-product contract |
| DF-ACE-213 | v_ace_npa_asset | transfer_in_date | Read through the rwb-source-data data-product contract; the holding fact |
| DF-ACE-214 | v_ace_npa_asset | book_value | Read through the rwb-source-data data-product contract |
| DF-DEC-002 | decision_log_entry | case_id | Read, through the rwb-decision contract |
| DF-DEC-004 | decision_log_entry | rule_id | Read, through the rwb-decision contract |
| DF-DEC-005 | decision_log_entry | rule_version | Read, through the rwb-decision contract |
| DF-REF-002 | rule_row | rule_id | Read, through the rwb-decision rule registry |
| DF-REF-003 | rule_row | rule_version | Read, through the rwb-decision rule registry |
| DF-REF-005 | rule_row | from_state | Read, through the rwb-decision rule registry |
| DF-REF-006 | rule_row | event_code | Read, through the rwb-decision rule registry |
| DF-REF-009 | rule_row | to_state | Read, through the rwb-decision rule registry |
| DF-OPS-137 | interface_config | interface_id | Read, through the rwb-integration admin operation |
| DF-OPS-142 | interface_config | data_product | Read, through the rwb-integration admin operation |
| DF-OPS-169 | outbound_item | interface_id | Read, through the rwb-integration admin operation |
| DF-OPS-170 | outbound_item | idempotency_key | Read, through the rwb-integration admin operation |
| DF-OPS-175 | outbound_item | status | Read, through the rwb-integration admin operation |
| DF-EXT-041 | valuation_ext | stale_flag | Read; the Workbench flag on an ACE appraisal |
| DF-EXT-042 | valuation_ext | age_days | Read; the days from the appraisal date to today |
| Not specified in the source documents (GAP-0427; ASM-0603) | valuation_ext | one_year_rule_applied | Read; the R-DIS-15 input flag |

The asset, its price inputs and its re-appraisal state are read through the rwb-asset contract and are not tabulated field by field here, because the ownership map gives the operation and not the S5 field IDs. Test data is synthetic; no production asset, case or decision is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row. Every owner comes from the Ownership Map.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/asset/v1/assets/{assetKey}` | S5 rwb-asset | The asset, its state ASSET_HELD, REAPPRAISAL_ORDERED, RELISTED or NO_BID_AT_FLOOR, its appraised value and its list and floor price inputs |
| GET | `/api/recovery/asset/v1/assets` | S5 rwb-asset | The asset list the cycle and the re-list are asserted against |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The SVAF re-appraisal order as one outbound item with its interface config |
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | The outbox delivery of the order and of the decision record |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The appraisal over v_ace_valuation and the holding facts over v_ace_npa_asset, on data product DP06 Collateral and assets (DP-05); source field names as the rwb-source-data contract returns them, with contract fields, business key and freshness response confirmed with P1 before wave 2 system test |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The one decision record of the cycle, its rule R-DIS-15 and its rule version |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case status and route state before and after the cycle |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and Asset and disposal right R for each call, including the refusal path (Architecture v5 slides 14 and 41) |

Where a screen would compose these, the harness calls the gateway-bff composite route (DP-19); the composite route path and merge order belong to RWB-PLT-N001-CON and are not restated here. No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it consumes the owners' events and writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The SVAF re-appraisal order file reached the interface, and the outbound item is Delivered |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The order file was refused; the item is Retry or Exception and the retry path is recorded, and the state assertion of AC3 is unaffected |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision, written by the local library in rwb-asset | Exactly one record for the cycle, carrying the case, the rule R-DIS-15 and its rule version (DP-03) |

`rwb.asset.AssetTakenOn.v1` and `rwb.asset.AssetSold.v1` are not consumed: the journey starts in ASSET_HELD after the take-on and never reaches a sale. Every event carries IDs and business facts only, keyed by caseId or assetKey, and the harness asserts that no personal data is present (DP-09).

#### 12.5 Workflows and activities

None added. The harness starts, changes and owns no workflow and no activity. It exercises AssetDisposalWorkflow on the rwb-asset task queue, in which the re-appraisal stage of R-DIS-15 and JOB-19 run (Temporal and Drools Design, S5 slide 21), and it asserts the effect through the owner's contract and topic. The workflow is owned by RWB-S5-E3026-APP.

#### 12.6 Schedules

None added. JOB-19 Re-appraisal, monthly on rwb-asset (Architecture v5 slide 44), is exercised on the business date of the run through the fixed clock only; no cron, overlap policy or catch-up window is set by this story (DP-10). The clock fixture and the window control are Not specified in the source documents (GAP-0427; ASM-0603).

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); it reads through the owning services' contracts. `rwb_asset`, `rwb_integration`, `rwb_source_data`, `rwb_decision`, `rwb_case` and `rwb_access` are the owners' schemas and are not touched directly.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-asset | `GET /assets/{assetKey}`, `GET /assets`, and the asset state and price inputs | Day-1 run of AC3 before RWB-S5-E3026-APP is live: ASSET_HELD, REAPPRAISAL_ORDERED, RELISTED and NO_BID_AT_FLOOR, with the reset price inputs |
| WireMock stub for rwb-integration | `GET /admin/outbound-items`, `GET /admin/outbox/deliveries`, `rwb.integration.events.v1` | The SVAF outbound item, the interface config row with DP06, the delivery and the failure outcome |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records` | The appraisal over v_ace_valuation and the holding facts over v_ace_npa_asset, with the freshness stamp |
| WireMock stub for rwb-decision | `GET /decision-log` | The single R-DIS-15 record with its rule version, and the duplicate and missing cases |
| WireMock stub for rwb-case | `GET /cases/{caseId}` | The case status and route state before and after the cycle |
| WireMock stub for rwb-access | `POST /authorise` | The allow path for Asset and disposal R and the refusal with MSG-P4-002 |
| SVAF order-file fixture | The outbound file the interface config describes | The order file and its acknowledgement, keyed by business date, for the Delivered and Failed outcomes |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The interface ID, the file pattern, the fixture contents, the fixed clock value, the environment, the data seeding set and the evidence format and retention are Not specified in the source documents (GAP-0427; ASM-0603).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` from `rwb.integration.events.v1` and `rwb.decision.DecisionRecorded.v1` from `rwb.decision-record.v1` consumed (DP-09) |
| Temporal | None added; AssetDisposalWorkflow on `rwb-asset` exercised through the JOB-19 Re-appraisal run on the fixed clock (DP-10) |
| File | The SVAF re-appraisal order file as a fixture through rwb-integration's outbound interface |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays None. The only blocking dependency is the I story RWB-S5-E3026-APP; until it is live the run uses the rwb-asset stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs AC3 for one business date and holds the run lock; it stops at the first failed assertion with the trace |
| CycleClockFixture | Fixture | Holds the business date fixed, seeds the appraisal_date older than 12 months and one_year_rule_applied = N, and opens the JOB-19 window once, so the same cycle is produced on every run without waiting for a live calendar |
| FakePack | Fake | The six WireMock stubs generated from the published contracts, with the contract version pinned |
| SvafOrderFixture | Fixture | The SVAF re-appraisal order file and its acknowledgement, keyed by business date, for the Delivered and Failed outcomes |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference in the trace, so no service reads another service's tables and the ACE views are read only by rwb-source-data |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention are Not specified in the source documents (GAP-0427; ASM-0603) |

**Environment and test data.** SIT, one namespace, against the fakes from Day 1 and the real services as RWB-S5-E3026-APP and the other owners land, on the case under test and its asset in ASSET_HELD, a second asset in NO_BID_AT_FLOOR for the R-DIS-44 branch, and the rule row of R-DIS-15. The environment, the seeding set, the interface ID and the evidence retention are Not specified in the source documents (GAP-0427; ASM-0603). Seeding uses only the owning services' published operations, never a schema write. Each run starts from the seeded state at the fixed business date, so a repeated run is deterministic.

**Build steps**

1. Generate the six stubs from the published contracts and pin each contract version in the run report; fail the run on a version mismatch (X1).
2. Build CycleClockFixture and prove the JOB-19 window opens once and that a run repeats identically on the same clock (X2).
3. Build JourneyRunner for AC3's precondition: seed ASSET_HELD through the rwb-asset contract, assert the appraisal age and one_year_rule_applied = N through the rwb-source-data data-product contract, and assert the rule row R-DIS-15 with its version.
4. Add the cycle assertion: R-DIS-15 fires, the state becomes REAPPRAISAL_ORDERED, and one outbound item exists on the SVAF interface with one outbox delivery (X3, X4).
5. Add the SvafOrderFixture and the event probe for `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1`, and assert both outcomes (X5).
6. Add the decision-record assertion: exactly one record with R-DIS-15 and the rule version, and the state change and the outbox row in the same transaction; force the write failure and assert nothing moves with MSG-P7-003 (X6, X7).
7. Add the receipt and accept path: the value read back through DP06, R-DIS-17 resetting the list and floor price inputs, and the asset back in ASSET_HELD.
8. Add the reject path of R-DIS-18 and the re-list path of R-DIS-44, and assert REAPPRAISAL_ORDERED and RELISTED (X8).
9. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a caller without Asset and disposal R (X9).
10. Add the RunReportWriter and the gate, then swap each stub for its real owner as the stories land and rerun AC3.

**Feature switch.** The harness has no production feature flag and runs in the test environment only. The production switch that guards the cycle in rwb-asset is Not specified in the source documents (GAP-0427; ASM-0603), and the harness reads it from configuration rather than holding a copy.

**Done when.** The tests of section 16 pass for AC3; the criterion passes against the six fakes on Day 1 and again against the real rwb-asset and the other owners as they land; and the wave entry check holds a run report keyed by story and business date with the contract, rule and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | The floor is below the limit the approver's level may approve | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | The appraisal on the asset is more than a year old | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field is missing on the order or on the value | Enter {field}. |
| MSG-P4-002 | A role without Asset and disposal right R takes the action | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

The harness produces none of these messages itself; it asserts the message the owning service returns and names the message ID in the report, so a run failure points at a service and a message and not only at a date. Thai text for each message follows decision DL10. DL10 stays open with the business lead and Legal and Compliance; the story proceeds on assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863, confirmed by D-RCV-60, and the harness asserts message IDs, so the open Thai wording does not hold the build.

### 15. Screens and states

SCR-21 Asset list and SCR-23 Listing and price show the states this journey sets:

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-21 Asset list | Loading | The asset list answers through the owner's contract at once, with the asset in its state |
| SCR-21 Asset list | List | The asset in ASSET_HELD, REAPPRAISAL_ORDERED or RELISTED, with the appraisal date and the age that the cycle reads |
| SCR-21 Asset list | Empty | Not specified in the source documents (CG-ALL-850) |
| SCR-21 Asset list | Loading | Not specified in the source documents (CG-ALL-850) |
| SCR-21 Asset list | Error | MSG-GEN-004 when someone else changed the record |
| SCR-21 Asset list | No access | A role outside Asset and disposal access, checked on every request, is refused with MSG-P4-002 |
| SCR-23 Listing and price | Draft | The appraised value and the list and floor price inputs before the cycle |
| SCR-23 Listing and price | Below limit | MSG-S5-001 when the floor sits below the limit the level may approve, and MSG-S5-002 for an appraisal more than a year old |
| SCR-23 Listing and price | Approved | The value accepted under R-DIS-17 and the list and floor price inputs reset |
| SCR-23 Listing and price | Published | The asset re-listed under R-DIS-44 as RELISTED |
| SCR-23 Listing and price | Empty | Not specified in the source documents (CG-ALL-851) |
| SCR-23 Listing and price | Loading | Not specified in the source documents (CG-ALL-851) |
| SCR-23 Listing and price | Error | MSG-GEN-004 when someone else changed the record |
| SCR-23 Listing and price | No access | A role outside Asset and disposal access, checked on every request, is refused with MSG-P4-002 |

The harness renders no screen. It reads these states through the rwb-asset, rwb-integration, rwb-source-data and rwb-decision contracts, and it asserts the same SCR-21 and SCR-23 states a sale officer would see, so a passed run means the screen has the right data behind it. What the wave entry check looks at instead is the run report, whose format and retention are Not specified in the source documents (GAP-0427; ASM-0603).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-026-01-ITG | AC1 (run by RWB-S5-E3026-APP) | Integration | The cycle raises the order when the holding period passes the re-appraisal interval, and one record carries the rule version |
| TC-E3-026-02-ITG | AC2 (run by RWB-S5-E3026-APP) | Integration | NO_BID_AT_FLOOR inside the re-list limit; re-list and re-appraisal in the same run |
| TC-E3-026-03-ITG | AC3 | Integration | ASSET_HELD with appraisal_date older than 12 months and one_year_rule_applied = N; JOB-19 on the fixed clock; order to the rwb-valuation contract |
| TC-E3-026-04-ITG | AC4 (run by RWB-S5-E3026-APP) | Integration | Decision log write forced to fail |
| TC-E3-026-05-ITG | Access | Component | A role without Asset and disposal right R; refused with MSG-P4-002 |
| TC-E3-026-06-ITG | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-E3-026-07-ITG | AC5 | Integration | BR1 to BR10 on the fixed clock; test data Not specified in the source documents (NEWAC-RWB-ITG-E3026-ITG-AC5) |
| TC-E3-026-08-ITG | AC6 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E3026-ITG-AC6) |
| TC-E3-026-09-ITG | AC7 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E3026-ITG-AC7) |
| TC-E3-026-10-ITG | AC8 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E3026-ITG-AC8) |

The six ITG copies keep the legacy test case IDs of RWB-E3-026: TC-E3-026-01, TC-E3-026-02, TC-E3-026-03, TC-E3-026-04, TC-E3-026-05 and TC-E3-026-06, with the `-ITG` suffix on the copy. TC-E3-026-03-ITG is the copy that runs the legacy criterion this story owns (AC3), and TC-E3-026-07-ITG to TC-E3-026-10-ITG run AC5 to AC8; the other five are carried at ITG level for the legacy trace, and the behaviour they cover is built by RWB-S5-E3026-APP, which owns their criteria, not this story. The full legacy test, with its Given, When and Then, is in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under the legacy test case ID. The fixed clock, the JOB-19 window control, the SVAF interface ID and its fixture, the harness seeding and the evidence format are agreed with QA and the rwb-asset and rwb-integration owners at the wave 2 entry check; their values are Not specified in the source documents (GAP-0427).

### 17. Guardrails

- No business value in code: the 12 month appraisal age, the one_year_rule_applied flag, the re-list limit, the rule versions, the interface ID, the clock and the fixture contents are data held by the owning services or by the harness configuration; the harness reads them and never holds a copy.
- No personal data in logs, fixtures, reports, tests or prompts: only case, asset and decision identifiers are asserted, and the assertions are on codes and values.
- No read of another service's tables: every read and every seed goes through the owning contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and the ACE views v_ace_valuation and v_ace_npa_asset are read only by rwb-source-data (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- The harness never sets an asset state, a price input, a decision record or an outbound item by hand; it seeds through the owners and asserts what they reached.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never calls SVAF: the order file is a fixture and the outside system is not contacted.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S5-003 | Holding age drives re-appraisal and the provision step by rule | Business Requirements Program v5, section 5.12 S5 Assets and auction | FEAT-AST-09 | 09 Dispose assets and sell debt (D8) | R-DIS-15, R-DIS-16, R-DIS-17, R-DIS-18, R-DIS-44, R-DIS-06, R-DIS-09 | TC-E3-026-03-ITG, TC-E3-026-01-ITG, TC-E3-026-02-ITG |
| REQ-RDF-004 | Collateral records and appraisal values available on the case without a person looking them up in CCMS or SVAF, read through the ACE views | Business Requirements Epic 1 v4, section 4; Program v4, section 5.1 | FEAT-AST-09 | 09 Dispose assets and sell debt (D8) | R-DIS-15, R-DIS-16 | TC-E3-026-03-ITG |

The legacy story lists no requirement IDs, so the two rows above are the requirements its feature and its data carry in the BRD; REQ-RDF-004 is tabulated for the appraisal value and the holding facts read through v_ace_valuation and v_ace_npa_asset on DP06, and for nothing else. No requirement ID is invented here. The legacy slices RWB-E1-069, RWB-E1-018 and RWB-E2-006 do not cite REQ-RDF-004 in their section 18; this integration trace is accepted as the citing record (GAP-3213).

### 19. Out of scope

- RWB-S5-E3026-APP, the app story of this legacy key, and its AC1, AC2 and AC4, the asset state machine, the price inputs, the re-list and the AssetDisposalWorkflow.
- The other criteria of this legacy key and every screen, endpoint, table, event and Schedule they build.
- The appraisal order itself in rwb-valuation (FEAT-VAL-01, REQ-S1-001) and the outlier check of FEAT-VAL-03, which the receiving service owns.
- The SVAF interface config and the outbound item implementation on rwb-integration, which are P2's stories; this story exercises them and asserts their effect.
- The data product DP06 and the ACE views, which rwb-source-data owns (DP-05); this story reads them through the contract.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and observability.
- Production code in any service: the harness is test and evidence only.
- The fixed clock value, the interface ID, the fixtures, the harness environment and the evidence format and retention: carried as one gap and one assumption, not decided here.
