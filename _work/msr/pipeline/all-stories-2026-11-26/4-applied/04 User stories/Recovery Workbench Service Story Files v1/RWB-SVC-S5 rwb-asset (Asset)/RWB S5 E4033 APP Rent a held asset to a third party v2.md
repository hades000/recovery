# RWB-S5-E4033-APP Rent a held asset to a third party

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4033-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-S5-Y |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4033-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-033 for rwb-asset. The three legacy criteria are kept word for word with their origin tag and one or two mocked `Given` lines each; the rental becomes one step of `AssetDisposalWorkflow` on task queue `rwb-asset` that evaluates R-DIS-25 with the DISPOSAL package version in force, writes the rental terms and `holding_status` = `RENTED` in `rwb_asset`, records the decision through the local decision-record library before any change (DP-03), asks rwb-payment for the auto-debit and rwb-comms for the arrears notice, and answers `RENTAL_ACTIVE` to rwb-case without writing a `recovery_case` row. The base is `/api/recovery/asset/v1` (DP-13) and the two screens read through the gateway-bff composite route (DP-19); DP-05 applies as a prohibition because the ACE facts stay with rwb-source-data. The rental terms, the auto-debit and case-move names, the arrears follow-up and ATS have no source value (GAP-2965; ASM-4862, ASM-4863, ASM-4864, ASM-4865); the legacy Data and Endpoints tables name surfaces this service does not read or call (GAP-2965; ASM-4867); the plan carries no requirement id and no approval record exists for a Draft baseline (GAP-2965; ASM-4866, ASM-4868). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4033-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **to record the rental terms, the auto-debit and the arrears follow-up on a held asset once its disposal route is approved as a rental, and to have the decision recorded with its rule version**, so that **a held asset earns an approved rent on an approved term while it waits for a sale, instead of sitting idle through a 1,486-day NPA sales cycle**.

It owns the three legacy criteria with their messages, screens and roles; one rental step of `AssetDisposalWorkflow` on queue `rwb-asset` in namespace `rwb-recovery`, the stage child of `CaseWorkflow`; the R-DIS-25 evaluation; the rental terms and `holding_status` = `RENTED` of `LOV-HOLDING` on the `asset` row in `rwb_asset`; the decision record written before the row changes (DP-03); the requests to rwb-payment and rwb-comms; the `RENTAL_ACTIVE` answer to rwb-case; and the two reads behind SCR-21 and SCR-22 on `/api/recovery/asset/v1` through the gateway-bff route (DP-13, DP-19).

It does not own the published shapes, lists, consumed rows and fakes (RWB-S5-E4033-CON), the case and its route states and the approval (P3, P7), the money and the arrears follow-up (P8), the notice (P6), the ACE asset, customer and account facts (P1), the decision ledger (P7) or the deployment (the operations story of this legacy key).

### 2. Business rationale

The FSD keeps the objective and the metric: the NPA sales cycle is measured on the decision log and the Workbench records, reviewed monthly, and moves from 1,486 days to a target of 1,095 days (FSD S5 A2.24.1). The program keeps REQ-S5-010, "a transfer to the asset management company, a buy-back and a rental each follow a recorded approval" (Business Requirements Program v5), and BR-030 that a third-party rental carries its recorded approval (Epics 3 to 8 BRD v1 BR-030).

D-RCV-60 changes who owns the asset, the case, the money and the record. The asset and its holding status are this service's: `asset_sale` and `listing` are S5's, and Architecture v5 slide 41 gives rwb-asset "assets taken on, holding, floor price, listings, auction rounds", while the `asset` row has no Ownership Map row and is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 (GAP-2965; ASM-4867). The route decision stays with rwb-case and rwb-decision: the approval is the kit's `ApprovalWorkflow` and the route state is a column of `recovery_case`, which is P3's, so this story reads the state and answers the move and writes neither. The money stays with rwb-payment (P8), whose FEAT-PAY-09 already runs a rental auto-debit (FSD P8 A2.9): this story holds a mandate reference and never an amount, an instalment or a balance. The notice stays with rwb-comms, because `notice` and `template` are P6's. The decision is recorded first, in the same transaction as the asset change, which is what legacy AC1 asked for and AC3 tested. No event is published: Architecture v5 slide 19 OUT gives the service exactly two event names, `AssetTakenOn` and `AssetSold`, and a rental is neither.

Two values are carried as a gap rather than chosen quietly: the rental terms have no physical column set, and the auto-debit, case-move and ATS surfaces have no published name or specification (GAP-2965; ASM-4862, ASM-4863, ASM-4865).

### 3. Preconditions

- RWB-S5-E4033-CON is published: the reads, the rental element and its closed lists, the consumed rows, the decision-record element, the error set and the fakes are baselined and handed to this story.
- The rwb-case state read and move answer are available for the fake; where rwb-case publishes a move operation its name is Not specified in the source documents (GAP-2965; ASM-4863).
- The rwb-payment auto-debit request is available for the fake; its name and shape are Not specified in the source documents (GAP-2965; ASM-4863), and the amount, the schedule and the receipt stay with rwb-payment.
- The rwb-comms notice request is published as `POST /cases/{caseId}/notices`, so the arrears notice can be requested on Day 1 against its fake.
- RWB-PLT-E1027-CON is published with its writer fake: the record is written in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-22 reach this service through the gateway-bff composite route, one hop each (DP-19).
- `asset` exists in `rwb_asset` with the columns of DF-COL-028 to DF-COL-042 and the rental set read as added by the DB story of this service; this story adds no table and no migration (GAP-2965; ASM-4862).
- The DISPOSAL package is in force with R-DIS-25 and R-DIS-63, approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the case is in `ROUTE_WITH_APPROVER` with `route = rental` when the approval answer arrives.
- The service runs as its own login on `rwb_asset`, with no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_asset` or `rwb_case` is refused (DP-05).
- A Draft contract baseline needs no approval; the baseline is tagged by RWB-S5-E4033-CON when its tests pass (GAP-2965; ASM-4868).

### 4. Flow

1. The route of a held asset is approved as a rental: the kit's `ApprovalWorkflow` on rwb-decision answers, the case router forwards `ROUTE_APPROVED` to `CaseWorkflow`, and the case stays in `ROUTE_WITH_APPROVER` until the stage applies the move (R-DIS-25). Nothing of that approval is written here.
2. The rental step of `AssetDisposalWorkflow` on queue `rwb-asset` receives the approved route for the case in `ROUTE_WITH_APPROVER` with `route = rental`, and reads the case state and reference on the rwb-case contract, read only, to confirm the from-state and the route.
3. The step reads its own `asset` row of the case: `id` (DF-COL-028), `case_id` (DF-COL-029), `asset_ref` (DF-COL-031), `asset_type` (DF-COL-033) and `holding_status` (DF-COL-041). No ACE view and no foreign table is read.
4. `RentalTermsEvaluator` loads the package version in force and evaluates R-DIS-25 on the fact route = rental, returning the rule ID, the version, the action and the to-state `RENTAL_ACTIVE`.
5. Where no rule fires, or the case is not in `ROUTE_WITH_APPROVER` with `route = rental`, the step changes nothing, writes no record and reports the reason to the parent.
6. `AssetDecisionRecordWriter` writes one decision record **before any change**: case reference, asset reference, rule ID with its version, inputs reference, outcome, case move and decided-at time. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
7. `AssetRentalWriter` updates the `asset` row in one transaction with the record and the idempotency row: `holding_status` set to `RENTED`, and the rental start date, tenant reference, term, rent, currency, payment method and auto-debit reference in the column set of ASM-4862, with the optimistic lock on `version` (GAP-2965).
8. `PaymentAutoDebitClient` asks rwb-payment to set the auto-debit of the case and the asset for the rental term, one hop with a 2 s budget and a breaker; the mandate, the amount, the schedule, the receipt and every instalment are the owner's. `CommsNoticeClient` asks rwb-comms for the arrears notice on `POST /cases/{caseId}/notices` with the case reference and the notice type and no personal data (GAP-2965; ASM-4863, ASM-4864).
9. `CaseMoveAnswer` answers rwb-case with `RENTAL_ACTIVE`, the rule ID, the version and the decided-at time; rwb-case writes the case and its route state, and this service writes neither.
10. No event is published: no outbox row is written and the two event names of the service stay `AssetTakenOn` and `AssetSold`. A repeated approval with the same case, asset reference and rule version writes nothing, sends no second mandate, notice or move, and counts the repeat.
11. SCR-21 Asset list and SCR-22 Asset record read the asset, its holding status `RENTED` and its rental terms through the gateway-bff composite route, read only, next to the case of rwb-case and the debit of rwb-payment (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record cannot be written | Nothing is written: no rental terms, no holding change, no mandate, no notice and no move answer leaves the service | MSG-P7-003 | AC3, TC-E4-033-03, TC-E4-033-05 |
| X2 | The role does not hold the Asset and disposal right | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E4-033-04 |
| X3 | The case is not in `ROUTE_WITH_APPROVER`, or its route is not `rental` | 409 and nothing written; no rental on a route never approved as a rental | None | AC2 |
| X4 | A required rental term is absent or invalid | 422 before any write; the missing field is named | MSG-GEN-001 | AC1 |
| X5 | A consumed contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's schedule; nothing is committed and no move is answered; the caller sees 503 with the platform envelope | None | AC1, AC2 |
| X6 | The asset is already `RENTED` with the same terms and rule version | One change, one record, one mandate, one notice and one answer; the repeat is counted | None | AC1 |
| X7 | The asset is `SOLD`, `TRANSFERRED` or `UNDER_OFFER` when the rental is asked for | 409 and nothing written; an asset that has left the holding cannot be rented | None | AC2 |
| X8 | A statement, a component or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17 |

X1 to X3 are the legacy exception paths carried onto the split, X4 to X7 are the paths the target call types and the rental state add, and X8 is the DP-05 and DP-01 boundary. The arrears value a later tenant-default step reads is not a constant of this story and no value of it appears here (GAP-2965; ASM-4864).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E4033-CON, the rwb-payment, rwb-case and rwb-comms fakes and the decision-record stub, on its own schema |
| Negotiable | The activity name, the decision code per rule, the stage outcome shape and the rental column names are this story's choice; the rule, the messages, the screens, the reads and the holding value are fixed |
| Valuable | A held asset earns an approved rent on an approved term, with the decision recorded and the debit with the service that owns the money |
| Estimable | One workflow step, one evaluator, one record write, one row update, two client calls and one move answer |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and assets through the fakes, plus the access and failed-write component cases |

### 7. Acceptance criteria

```gherkin
Feature: Rent a held asset to a third party

  Background:
    Given case "RC-2026-000521" carries the held vehicle "AST-2026-000521" with holding status "HELD"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-25 and R-DIS-63
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Rent a held asset to a third party (legacy RWB-E4-033 AC1)
    Given the rwb-case contract mock returns the case state "ASSET_HELD" for "RC-2026-000521"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then records the rental, the debit and the arrears follow-up while the asset is held
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-25 (legacy RWB-E4-033 AC2)
    Given the rwb-case contract mock returns the case state "ROUTE_WITH_APPROVER" for "RC-2026-000521"
    Given the rwb-payment contract mock returns the auto-debit set for "RC-2026-000521"
    Given a case in state ROUTE_WITH_APPROVER
    When route approved
    Then set the rental terms and the auto-debit, and hold the asset as rented
    Then the case moves to RENTAL_ACTIVE

  Scenario: AC3 Not recorded (legacy RWB-E4-033 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria word for word with the origin tag added: the repetition of `Then`, `the action is taken`, `the user acts on the screen`, `the decision log cannot be written` and `route approved` all stand, and the `Given the <service> contract mock returns <x>` lines are the only additions. What the legacy lines describe happens in four places: rwb-case holds the case and writes the move, rwb-decision holds the approval and the package, this story evaluates R-DIS-25 and writes the record, the rental terms, the holding status and the answer, and rwb-payment holds the mandate, the debit and the arrears follow-up — which is why AC1's "rental, debit and arrears follow-up" is recorded here and held there (GAP-2965; ASM-4864). The rental terms have no column set in TSD S5 T3.1, so the set is read as an addition to `asset` by the DB story of this service (GAP-2965; ASM-4862). The legacy `v_ace_npa_asset`, `v_ace_customer` and `v_ace_account` reads are not reproduced (GAP-2965; ASM-4867).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-25 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = rental | Set the rental terms and the auto-debit, and hold the asset as rented | RENTAL_ACTIVE | Sale officer | ATS | None |

The row is the row of Business Rules and Routing Logic v4, copied character for character. Its owner column is a business role and its `Systems` cell names ATS, an external system outside the 19 services: it is tracked and not built, and no interface of it is specified in TSD S5 T5.1 (GAP-2965; ASM-4865). The move to `RENTAL_ACTIVE` is written by rwb-case on this story's answer, the rental terms and the holding status here, and the auto-debit by rwb-payment on request. The next rule on the route set, R-DIS-63 "rental_arrears above the threshold" returns the asset to `ASSET_HELD`; its value has no source, belongs to the tenant-default step and is not written here (ASM-4864).

| ID | Rule | Source |
|---|---|---|
| BR1 | `holding_status` and the rental terms are columns of `asset` in `rwb_asset`, and no other service writes them | Architecture v5 slide 41; TSD S5 T3.1; ASM-4867 |
| BR2 | The decision is recorded before the row changes, with the rule ID and the package version; a failed write changes nothing | DP-03; TSD S5 T2; legacy RWB-E4-033 AC1 and AC3 |
| BR3 | ACE facts stay with rwb-source-data: no `v_ace_*` read and no ACE table read, and the asset fact comes from this service's own row | DP-05; Architecture v5 slides 29 and 41; GAP-2965 |
| BR4 | The case move is answered and not written: `recovery_case`, the route states and the approval are P3's and P7's | Ownership Map; GAP-2965 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id` and `collateral_id` are identifiers of other services' facts | DP-01; TSD S5 T3.3 |
| BR6 | No amount, instalment, balance or receipt is written here; the auto-debit is a request answered by an identifier | Architecture v5 slide 41; FSD P8 A2.9; GAP-2965 |
| BR7 | This step publishes no event: the two event names stay `AssetTakenOn` and `AssetSold`, and a rental is neither | Architecture v5 slide 19 OUT; Template and Rules §R4 |
| BR8 | Every value a business person may change is reference data or a rule row read with its version | TSD S5 T3.2; FSD S5 BR-S5-024 |
| BR9 | The same approval twice, or the same `Idempotency-Key` twice, writes once, sends one mandate, one notice and one answer | TSD S5 T-A.2; Architecture v5 slide 11 |

### 9. State transitions

The case route state is rwb-case's and is not changed here: the step answers the move and the parent applies it (BR4). What this story owns is the holding status and the step state.

| From (`asset.holding_status`) | Event | Condition | To |
|---|---|---|---|
| HELD | The approved rental route under R-DIS-25 | route = rental and case in `ROUTE_WITH_APPROVER` | `RENTED`, with the move answer `RENTAL_ACTIVE` |
| RENTED | A rental for the same asset and rule version | X6 | Unchanged, the repeat is counted |
| LISTED, UNDER_OFFER, SOLD, TRANSFERRED | An approved rental route | X7 | Unchanged, 409 and nothing written |
| HELD | A route that is not `rental`, or a case not in `ROUTE_WITH_APPROVER` | X3 | Unchanged, no record and no answer |
| RENTED | A tenant default under R-DIS-63 | The rental_arrears value of rwb-payment, on a later step | `HELD` on that step, not this one |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The approved rental route arrives for a case in `ROUTE_WITH_APPROVER` | The package in force is loaded | Evaluating |
| Evaluating | R-DIS-25 fires | The decision record is written | Applying |
| Applying | The row is updated, the two requests and the move answer are sent | The transaction commits | Waiting for the next route answer |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | A downstream contract does not answer inside 2 s | X5 | Waiting, retried on the workflow's schedule |

The values are those of `LOV-HOLDING` in TSD S5 T3.2: HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED; the route states are those of the DISPOSAL machine of TSD S5 T4 and live on the case of record.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA (TSD S5 T6.1): the primary role and the owner of R-DIS-25 |
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU: reads the asset, corrects the rental terms and confirms the arrangement |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the asset and the rental arrangement of a repossessed vehicle |
| The other roles of TSD S5 T6.1, and the partner and service identities | Asset and disposal R, or RU as the matrix gives it: read only or the partner's own assets, never the rental decision |
| rwb-asset service identity | Runs the step, evaluates the rule, writes the record and the row, requests the mandate and the notice and answers the move; it holds no grant on another schema |

The rights are the rows of TSD S5 T6.1 and nothing wider. The legacy Permission checks table gives Asset and disposal R to nine roles and 23 more, and C to RW-ENFORCE, RW-SALEOFF, RW-NPAMGR and SY-DATALOAD; the TSD matrix agrees on every role it lists and is the one applied. The FSD names the sale officer as primary and the NPA and asset manager as also-user (FSD S5 A2.24.3.3): the officer approves the route and the step runs under the service identity once the approval arrives. DP-08 is not in this story's pattern set: the capability area and right are declared per operation, and the guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-028 | asset (S5, `rwb_asset`) | id | Read, the asset reference of the record, the requests and the answer |
| DF-COL-029 | asset (S5, `rwb_asset`) | case_id | Read, the case the rental belongs to |
| DF-COL-031 | asset (S5, `rwb_asset`) | asset_ref | Read, the reference the rent is set against |
| DF-COL-033 | asset (S5, `rwb_asset`) | asset_type | Read, against `LOV-ASSET-TYPE` |
| DF-COL-041 | asset (S5, `rwb_asset`) | holding_status | Write, against `LOV-HOLDING` (`RENTED`) |
| Not specified in the source documents (GAP-2965; ASM-4862) | asset (S5, `rwb_asset`) | the rental terms: rental start date, tenant reference, term, rent, rent currency, payment method and auto-debit reference | Write, in the column set ASM-4862 reads as added to `asset` by the DB story |
| Standard columns | asset (S5, `rwb_asset`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Read and write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, outcome, case move, decided at | Write through the local library, before the row changes |
| DF-SAL-009 to DF-SAL-019 | asset_sale (S5, `rwb_asset`) | the sale columns of an asset | Not written: a rental is not a sale and R-DIS-25 writes no sale row |
| DF-ACE-208 to DF-ACE-219, DF-ACE-055 to DF-ACE-074, DF-ACE-001 to DF-ACE-042 | `v_ace_npa_asset`, `v_ace_customer`, `v_ace_account` (P1) | asset_ref, asset_key, asset_code, book_value; person_key, cif_no, first_name; account_key, account_code, total_balance and the rest | Not read: no `v_ace_*` grant, DP-05 as a prohibition (BR3) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, status, stage_code and 18 more | Not read as a table: the case state arrives on the rwb-case read (BR4) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rule travels in the package loaded from rwb-decision |

Field IDs are those of TSD S5 v2 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table and no migration**: `asset` arrives with the DB story of this service, `decision_record` and `idempotency_key` are library objects created in `rwb_asset` (DP-03), and no outbox row is written (BR7). **No personal data**: the rows carry identifiers, codes, amounts, dates and a rule version; the tenant reference is the identifier of the arrangement and not a contact value, and every fixture is synthetic (GAP-2965; ASM-4862).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the two reads whose shapes RWB-S5-E4033-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetKey}` | Asset out with its title, condition, valuations, costs, listing references, holding status and rental terms (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

The errors are 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 when the library or a consumed contract does not answer. The operation IDs are those of TSD S5 T-A.1 and are not redefined here. No operation writes the rental: the officer's act is the route approval in rwb-decision and the stage task in rwb-case, so a REST write operation for the rental is Not specified in the source documents (GAP-2965; ASM-4862). `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's under the Ownership Map ruling on the valuation operation; the listing and round operations (API-S5-004, API-S5-005) belong to the pricing and auction stories of this service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The auto-debit request (operation name Not specified in the source documents (GAP-2965; ASM-4863)) | `/api/recovery/payment/v1` | P8 rwb-payment | Sets the auto-debit of the case and the asset for the rental term and answers its reference; the amount, schedule, receipt and arrears follow-up stay with the owner; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The state `ROUTE_WITH_APPROVER`, the route `rental` and the case reference; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2965; ASM-4863)) | `/api/recovery/case/v1` | P3 rwb-case | Carries `RENTAL_ACTIVE` with the rule and its version; on the workflow boundary the stage outcome the parent applies; faked |
| `POST /cases/{caseId}/notices` | `/api/recovery/comms/v1` | P6 rwb-comms | Requests the arrears notice with the case reference and the notice type and no personal data; template, merge fields and delivery are P6's; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These four rows are class C dependencies in fact, and the plan's C row for this slice is None; the absence is recorded as GAP-2965 with ASM-4863.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset exactly two event names, `AssetTakenOn` and `AssetSold`; a rental is neither, so the step writes no outbox row and declares no third event. The two names stay with RWB-S5-E3019-APP and the sale stories of this service.

#### 12.4 Events consumed

None. The rental starts from the approved route the parent `CaseWorkflow` forwards as a signal, not from an event: Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult`, `ProceedsMatched` and `PartnerResultSubmitted`, and none is the rental approval. The story holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new across the holding | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the approved route, the asset reference and the package in force; signals: the case state, the package in force and the approval answer |
| `rentHeldAsset` | Activity, the one rental step | `rwb-asset` | Case and approved route in; rule ID with its version, asset reference, debit reference, notice and case move out, with the record and the `asset` row written in one transaction |

No child workflow for the case, the approval or the money exists in this service. The activity name is a target design choice fixed by no source; the trigger is the arrival of the approved route for a case in `ROUTE_WITH_APPROVER`, because the FSD declares no background event (FSD S5 A2.24.4.4).

#### 12.6 Schedules

None. The step runs from the approved route and the case signal, and owns no Temporal Schedule and no legacy Quartz job. The service's single Schedule is JOB-19 Re-appraisal monthly, which belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`) | The held asset; this story sets `holding_status` to `RENTED` and writes the rental terms of §11 |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated approval and the answer it holds |

Not owned and never read as a table: `recovery_case`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `notice` and `template` (P6), `proceeds` and every payment table (P8), every `v_ace_*` view (P1), and `listing` and `asset_sale` (this service's pricing and sale stories). No foreign key leaves the schema (DP-01, DP-05). `outbox_event` exists in the schema from the library and this story writes no row in it.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | The state `ROUTE_WITH_APPROVER` with the route `rental` for case `RC-2026-000521`; the same case with route `auction`; a case in `RENTAL_ACTIVE`; no answer beyond 2 s | AC1, AC2, X3, X5 |
| rwb-case case-move fake | The move `RENTAL_ACTIVE` accepted, and a move refused because the case is not in the expected state | AC2, X3 |
| rwb-payment auto-debit fake | The auto-debit set for case `RC-2026-000521` with its mandate reference; a refused mandate with its reason; no answer beyond 2 s | AC1, AC2, X5 |
| rwb-comms notice fake | The arrears notice accepted with its notice reference, and a refused request | AC1, X5 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-25 and R-DIS-63 | AC1, AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000521`, with the asset and its rental terms read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the auto-debit request and the move answer carry the placeholder until their owners confirm them (GAP-2965; ASM-4863). ATS has no fake: it has no interface specification, and the debit it would carry is rwb-payment's (ASM-4865).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two asset reads; the rwb-payment auto-debit request, the rwb-case state read and move answer and the rwb-comms notice request; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The step publishes and consumes nothing; the two event names stay with the take-on and the sale |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and its rental step on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `rental`; front end `src/modules/recovery/asset/AssetRental.tsx`, the fragment SCR-21 and SCR-22 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: no `v_ace_*` grant, no ACE view and no ACE table, and the asset fact comes from this service's own row. DP-03 is the transaction rule: the record and the row commit together or not at all. DP-13 moves the base of the two reads and nothing else. DP-19 is how the two screens reach this service, one hop through the gateway.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` rental branch | Workflow | Waits for the approved route, loads the package in force and reports the outcome to the parent |
| `rentHeldAsset` | Activity | Reads the case and the asset, evaluates R-DIS-25, writes the record and the row, requests the mandate and the notice, answers the move |
| `RentalTermsEvaluator` | Service | The rule evaluation against the package in force, with the holding value and the route condition of the closed lists |
| `AssetDecisionRecordWriter`, `AssetRentalWriter` | Library adapter and repository | The record written before any change (DP-03); the `asset` update with its rental set, the idempotency row and the optimistic lock |
| `PaymentAutoDebitClient`, `CaseStateClient`, `CommsNoticeClient` | Clients | One hop each, 2 s, breaker, no amount held, no personal data |
| `AssetController`, `AssetRental` | Controller and React component | The two reads with their rights and problem mapping; the asset, its holding status and its rental terms on SCR-21 and SCR-22, read only |

**Database and migrations.** No Flyway file here: `asset` arrives with the DB story of this service, the rental set is the one ASM-4862 reads as added by the same story, and the record and the idempotency key are library objects created in `rwb_asset` (GAP-2965; ASM-4862). No outbox row is written.

**Configuration and reference data.** `LOV-HOLDING` with `RENTED`, `LOV-ASSET-TYPE` and `LOV-SEGMENT` at their version (TSD S5 T3.2), read as reference data and never as constants. The DISPOSAL package and its version are governed in rwb-decision and loaded on `RulePackageInForce`; the route condition and the R-DIS-63 value are values of the package and of rwb-payment, not of this build (ASM-4864). The mandate values, the receipt and the arrears limit are rwb-payment's parameters, read through its contract; the capability area and its rights are access rows of rwb-access; ATS is tracked and not configured, called, faked or built (ASM-4865); the 2 s budget and the single hop are ADR-020.

**Build steps**

1. The rental branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset` as the stage child of `CaseWorkflow`.
2. `CaseStateClient` against its fake, with the 2 s budget, the breaker, the wrong-state and the no-answer paths (AC1, AC2, X3, X5).
3. `RentalTermsEvaluator` over the package, with R-DIS-25, the route condition and the no-fire path (AC2, X3); then `AssetDecisionRecordWriter` against the library stub with the failed-write path (AC3, X1).
4. `AssetRentalWriter` with the one transaction, `RENTED`, the rental set, the idempotency row and the optimistic lock (AC1, AC2, X6).
5. `PaymentAutoDebitClient`, `CommsNoticeClient` and `CaseMoveAnswer`, with the refused and no-answer paths (AC1, AC2, X5).
6. `AssetController` with the rights, the pagination and the problem mapping, and `AssetRental` on the two screens through the composite route fake (AC1), then the boundary test (X8).

**Feature flag.** `rwb.asset.rental-v1`, a flag of the platform library; off means the step holds the approved route, writes nothing, sends no request and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of §16 pass, the step runs from a synthetic approved rental route in SIT, R-DIS-25 produces its record, row, mandate, notice and move, a repeated approval writes once, a forced record failure changes nothing, no `recovery_case` row and no outbox row exists in the build, and SCR-21 and SCR-22 answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this story raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set. It names the age of an appraisal, which is the re-appraisal story's, so no path of this story raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required rental term or request field is absent or invalid (VR-S5-024-1, X4) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the list or the asset (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five IDs are those of the legacy message set and FSD S5 A2.24.3.1, and the text is the legacy and FSD wording copied unchanged; no message is reworded and no new one is added. MSG-S5-001 and MSG-S5-002 are carried because they are in the message set of the feature, and no path of this story raises them. The arrears value of R-DIS-63 raises no message of this story (ASM-4864).

### 15. Screens and states

SCR-21 Asset list (loading, list) and SCR-22 Asset record (take-on, held, listed, sold) are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset and its holding status, rwb-case for the case and its route state, rwb-source-data for the ACE asset fact, rwb-valuation for the valuation references and rwb-payment for the debit; this story fixes the rwb-asset answers only, and the route specification and the field list belong to RWB-PLT-N001-CON.

The legacy screen table names four states of SCR-22 and no rented state, while `LOV-HOLDING` carries `RENTED`: the asset keeps the held state of the screen and shows `holding_status` = `RENTED` with its rental terms, the case route and the debit reference, and the difference is recorded (GAP-2965; ASM-4862). The refusal, not-recorded and invalid states show MSG-P4-002, MSG-P7-003 and MSG-GEN-001 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-033-01 | AC1 | Component | The approved rental route of case `RC-2026-000521` and asset `AST-2026-000521`; the terms, the record, the mandate, the notice and the move asserted on the fakes |
| TC-E4-033-02 | AC2 | Integration | Case `RC-2026-000521` at `ROUTE_WITH_APPROVER` with route `rental`; the auto-debit answered by rwb-payment and the `RENTAL_ACTIVE` move answered to rwb-case |
| TC-E4-033-03 | AC3 | Component | The decision-record stub stopped; nothing written, no mandate, no notice, no move and MSG-P7-003 shown |
| TC-E4-033-04 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E4-033-05 | Principle 5 | Component | A forced decision log write failure at the moment of the asset update; no row change, no mandate and no answer |

The five cases are the legacy cases of RWB-E4-033 in their legacy order, with the Level column added: `System` maps to `Component` where the step is tested on its fakes, and TC-E4-033-02 maps to `Integration` because it crosses the rwb-payment and rwb-case boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the route condition, the states, the `RENTED` value, the term limits, the arrears value and the rule row stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_asset`, a workflow input, a notice request or a log: identifiers, codes, amounts, dates and a rule version only, every fixture synthetic, and the tenant reference an identifier of the arrangement and never a contact value.
- ACE data only through the owner's contract or the `v_ace_*` views: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05, BR3).
- The case stays with rwb-case and rwb-decision and the money with rwb-payment: no `recovery_case` row, no approval row, no posting, no balance, no receipt and no arrears decision is written here (BR4, BR6).
- One base, one topic, one queue and one login per service, and no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No event is published and no third event name is added to the service; a build that writes an outbox row fails the review (BR7).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no ATS interface invented without a specification (ASM-4865).
- The decision is recorded before the change; a build that writes the asset row first fails the review (DP-03, BR2).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-010 | A transfer to the asset management company, a buy-back and a rental each follow a recorded approval (FSD S5 requirements served; Business Requirements Program v5; BR-030 of Epics 3 to 8 BRD v1); the split plan carries no requirement id for this slice (GAP-2965; ASM-4866) | The rental step, the R-DIS-25 evaluation, the record and the `asset` row | TC-E4-033-01, TC-E4-033-02, TC-E4-033-03 |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the asset and its holding status | TC-E4-033-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login | TC-E4-033-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget | TC-E4-033-02 |
| ADR-022 | Local decision record plus central ledger | The record written before the change | TC-E4-033-03, TC-E4-033-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-033, disposition Split (rework) |
| Legacy criteria | AC1 to AC3, owned word for word by this story |
| Test cases | TC-E4-033-01 to TC-E4-033-05 |
| Feature and screens | FEAT-AST-24, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-25 from the Business Rules and Routing Logic v4, governed in rwb-decision; R-DIS-63 named as the later tenant-default step |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two reads, the rental element, the closed lists, the consumed rows, the error set and the fakes: RWB-S5-E4033-CON.
- The case of record, its route states, the parent `CaseWorkflow` and the stage task: rwb-case (P3) (GAP-2965); the approval, the rule package and the decision ledger: rwb-decision (P7).
- The auto-debit, the receipt, the instalments, the arrears follow-up and the rental_arrears value: rwb-payment (P8) under FEAT-PAY-09 (ASM-4864); the arrears notice, its template and its delivery: rwb-comms (P6).
- The ACE NPA asset, customer and account facts: rwb-source-data (P1) (ASM-4867).
- ATS and its interface: an external system with no specification in TSD S5 T5.1, tracked and not built here (ASM-4865).
- The holding-age clock, the provision steps and the monthly cost of carry: RWB-S5-E3023-APP; the return of the asset to the holding on a tenant default (R-DIS-63): a later step of this service.
- The deed in lieu buy-back rental of the customer's own asset: rwb-treatment (S2) and rwb-payment (P8), a different route set (R-DIL-32, R-DIL-34).
- The listing, the floor price and the auction rounds: the pricing and auction stories of this service (API-S5-004, API-S5-005).
- The gateway-bff composite route and the field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness; the deployment, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
