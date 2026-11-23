SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD S5 rwb-asset v1
description: Product requirements for the Recovery Workbench assets and auction service (S5 rwb-asset) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S5 Assets and auction v3.md
service: S5 rwb-asset
epic: RWB-SVC-S5
wave: 2
decision: D-RCV-60
---

# Recovery Workbench PRD S5 rwb-asset v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD S5 rwb-asset |
| Document ID | S5-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | S5 rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epics | EP03 (Epic 3, settle, deed in lieu and assets, wave 2, release 31 January 2027 (tentative)); EP04 (Epic 4, route decision, guarantees and auction, wave 3, release 28 February 2027 (tentative)) |
| Schema | `rwb_asset` |
| REST base | `/api/recovery/asset/v1` |
| Topic | `rwb.asset.events.v1` |
| Temporal task queue | `rwb-asset` |
| Java package | `th.co.scb.ace.workbench.recovery.asset` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Business analyst, S5 |
| Decision | D-RCV-60 (microservice realignment); inherits ADR-010, ADR-013 to ADR-023 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epics 3 to 8 v1; FSD S5 Assets and auction v3; TSD S5 Assets and auction v2; Architecture v5; Temporal and Drools Design v1 |
| Upstream requirement IDs | REQ-S5-001 to REQ-S5-010; BR-010, BR-011, BR-012, BR-013, BR-014, BR-026, BR-027, BR-028, BR-029, BR-030; RULE-001, RULE-002, RULE-006, RULE-007, RULE-008, RULE-011, RULE-023, RULE-028, RULE-030, RULE-031, RULE-032; NFR-001, NFR-002, NFR-003, NFR-008, NFR-009, NFR-010, NFR-011, NFR-013, NFR-014, NFR-015, NFR-020, NFR-021, NFR-022, NFR-023, NFR-024, NFR-025, NFR-026, NFR-027, NFR-028, NFR-031, NFR-033, NFR-034, NFR-035, NFR-036, NFR-039, NFR-040, NFR-042, NFR-045, NFR-046, NFR-047, NFR-049, NFR-050, NFR-051, NFR-052, NFR-053, NFR-054, NFR-055, NFR-059, NFR-060, NFR-061, NFR-063, NFR-064, NFR-066, NFR-067, NFR-068, NFR-078 |
| Upstream acceptance criteria | AC-S5-001-01 to AC-S5-025-01 (main success flow, one per feature); AC-EXC-S5-001-01 to AC-EXC-S5-025-01 (role without the right); AC-EXC-S5-001-02 to AC-EXC-S5-025-02 (decision cannot be recorded). The FSD defines no alternate flow and no system background event for any of the twenty-five features |
| Generated IDs | CAP-S5-001 to CAP-S5-019; FR-S5-001 to FR-S5-044; NFR-S5-001 to NFR-S5-031; AC-S5-001 to AC-S5-032; JRN-S5-01 to JRN-S5-06; ROL-S5-01 to ROL-S5-15; OQ-S5-01 to OQ-S5-20 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD S5 Assets and auction v3 (15 November 2026) and TSD S5 Assets and auction v2 (28 October 2026), realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD S5 Assets and auction v3. Its requirement IDs, feature IDs, rule IDs, validation rule IDs, message IDs, screen IDs and acceptance criterion IDs are carried unchanged; the microservice realignment changes the read path, the owner of four capabilities and the delivery waves, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 (FSD) | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Asset field catalog re-pointed to `v_ace_npa_asset`, `v_ace_asset` and `v_ace_collateral`; asset record opened on the ACE NPA asset; COLLINS economics from `v_ace_score`. Everything else unchanged from v2 |
| 2 (TSD) | 28 October 2026 | Technical baseline: three objects (`asset`, `listing`, `asset_sale`), the DISPOSAL state machine with 72 rules over 40 states, six lists of values, five API operations and the RBAC matrix (GAP-1761; ASM-2929) |
| 1 and 2 (FSD) | Not specified in the source documents (GAP-1766; ASM-2934) | Earlier versions of the FSD. Their dates and change notes are not in the sources read, and are carried as an open item rather than reconstructed |
| 1 (PRD) | 22 November 2026 | First PRD of this family (ASM-2938). CAP, FR, NFR, AC, journey and open-question IDs are new; the FSD requirement IDs (REQ-S5-001 to REQ-S5-010), feature IDs (FEAT-AST-01 to FEAT-AST-25), rule IDs (R-DIS-01 to R-DIS-71), validation rule IDs (VR-S5-001-1 to VR-S5-025-1, VR-S5-016-2), business rule IDs (BR-S5-001 to BR-S5-025), acceptance criteria IDs (AC-S5-001-01 to AC-S5-025-01 and their exception rows), message IDs (MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001, MSG-S5-001, MSG-S5-002), list IDs (LOV-ASSET-TYPE, LOV-HOLDING, LOV-LISTING, LOV-SALE-CHANNEL, LOV-SEGMENT, LOV-TRANSFER-IN) and screen IDs (SCR-21, SCR-22, SCR-23, SCR-24, PRT-06) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the program requirements REQ-S5-001 to REQ-S5-010 and of the non-functional requirements |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-010 to BR-014 and BR-026 to BR-030, the E3 and E4 scope, the measures (KPI-008), the rules RULE-001 to RULE-032, the risks and the open questions |
| Recovery Workbench Functional Specifications by Module v6, FSD S5 Assets and auction v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Technical Specifications by Module v5, TSD S5 Assets and auction v2 | TSD | Constraint: the three objects, the lists of values, the DISPOSAL state machine, the five API operations and the RBAC matrix |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, only rwb-source-data reads ACE, Kafka, Temporal, no data lake, edge and gateway |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: AssetDisposalWorkflow on `rwb-asset`, its seven steps, JOB-19, the 72-rule disposal set in Phase 2, the approval ladder and the two clocks |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every operation, event, workflow, table and job named here |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-asset (S5) is the recovery module's disposal of held assets. It turns "take the asset on, hold it, price it, sell it, transfer it" into a product: an asset that is on the books with its source, its date taken in, its holding cost and its provision step; a statutory notice with its proof of delivery; a holding age that drives the re-appraisal and the provision step without a person watching a list; a stock balance with one owner and one number; a disposal route recommended with its expected return; a start price and a floor that a named role approved; a listing published from one action; auction rounds that step down the ladder to the floor; a bid below the floor that needs a second signature; a payment term that is enforced; a title that is transferred; proceeds that are applied and a shortfall that is raised; and every other exit — a pool to the asset management company, a buy-back, a rental, a broker — on a recorded approval.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-asset | One deployable with its own API and worker, schema `rwb_asset`, login, topic `rwb.asset.events.v1`, task queue `rwb-asset` and lifecycle | The asset and its sale become one owned product with its own release, instead of screens inside a single deployable |
| The take-on as a governed record | One holding record per ACE asset key, opened from a repossession, a deed in lieu transfer or an LED handover, with its source, its date taken in, its book value and its provision step | REQ-S5-001 asks for the asset position an auditor asks for first; today the take-on is a hand-kept list |
| The stock balance with one owner | One screen and one monthly number for the non performing asset stock, with a named owner role | The balance has no owner today (BR-012, Q-009) |
| Holding age as a governed clock | The holding age, the provision step, the re-appraisal interval and the cost of carry run as timers and rules, not as a person watching a spreadsheet | Provision is a function of time held (BR-011) |
| The price and the floor as an approved pair | A start price and a floor proposed from the accepted value, the floor approved by the named role, and the floor withheld from publication | Price discipline is where the NPA sales cycle is won or lost (BR-014) |
| The auction as a loop of timed rounds | Each round is a step of AssetDisposalWorkflow on the owner's queue, with the price step set by rule and the clock held by the workflow | A ladder run by hand is a price run by memory (BR-027, RULE-007) |
| The vendor instruction through the partner contract | The allocated auction vendor is instructed through rwb-partner, not by telephone or mail | FEAT-AST-14 and FEAT-AST-15 need one instruction and one result path |
| The sale and its proceeds as one event | AssetSold on `rwb.asset.events.v1`, and the proceeds applied through rwb-payment with the shortfall raised for the next decision | Money applied or a residual decision: every exit ends in the same place (BR-030) |
| AssetTakenOn as an event | AssetTakenOn (EV-22) on `rwb.asset.events.v1`, consumed by rwb-case and rwb-payment | The case and the payment position move on the take-on in the same step, not on a poll |
| The decision as a reproducible record | Route, price, floor approval, round, award, transfer and exit, each with its rule version, its inputs and its actor | Every sale answers an audit question without a person reconstructing it (RULE-002, NFR-033) |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its ingestion of AMIS, RPS, CCMS, LIT and SVAF data and its backups | REUSE | ACE team |
| The read-only view contract and the freshness of every data product | REUSE, elsewhere | P1 rwb-source-data (this service reads it by contract) (GAP-1750; ASM-2918) |
| The asset record as an extension of the ACE NPA asset | REUSE, and the Workbench record is this service's | ACE team keeps the ACE asset; S5 holds the take-on and holding record (GAP-1751; ASM-2919) |
| Case record, CMMN state, queues, tasks, allocation and the case timers | REUSE | P3 rwb-case (AssetDisposalWorkflow is its child workflow) |
| Approval workflow, decision record, hash chain and rule package registry | REUSE | P7 rwb-decision |
| Roles, capability areas, masking policy and the delegation table | REUSE | P4 rwb-access |
| Documents, custody and the write-once container | REUSE | P5 rwb-document (GAP-1767; ASM-2935) |
| Notices, templates and proof of delivery | REUSE | P6 rwb-comms (GAP-1767; ASM-2935) |
| Vendor panel, vendor instruction, vendor result and the vendor scorecard | REUSE, elsewhere | S9 rwb-partner (GAP-1757; ASM-2925) |
| Payment, proceeds matching, fees and posting to ALS and the ledger | REUSE, elsewhere | P8 rwb-payment (GAP-1759; ASM-2927) |
| The accepted appraisal and the valuation order | REUSE, elsewhere | S1 rwb-valuation (GAP-1758; ASM-2926) |
| Route and performance measures | REUSE, elsewhere | P9 rwb-reporting, from the decision record and the events |
| Screens and the composite route that serves them | REUSE | Platform edge, gateway-bff (RWB-PLT-EDGE) |
| Quartz scheduler and its shared tables | REPLACED | Temporal Schedules and durable timers through the workflow kit (PLT); ADR-016, DP-10 |
| Embedded Drools with the disposal decision tables evaluated in the monolith | MOVED | P7 for governance and versioning; evaluation stays local in this service (ADR-017, DP-04) |
| The direct read of the ACE views and the direct posting to ALS and GL | NOT CARRIED | rwb-source-data and rwb-payment by contract (GAP-1750, GAP-1759; ASM-2918, ASM-2927) |
| Debt sale of a pool of accounts (D9) | OUT OF SCOPE | S6 rwb-debtsale; this service raises the residual and the re-list limit outcome |
| Litigation, the writ and the enforcement auction ladder | OUT OF SCOPE | S4 rwb-litigation; this service consumes JudgmentRecorded and AuctionResult |
| Write-off of the residual | OUT OF SCOPE | S7 rwb-writeoff |
| Booking in the core bank and credit approval in the lending system | OUT OF SCOPE | The officer and the core bank; this service records the result |
| Collections before day 90 and decisions D1 to D4 | OUT OF SCOPE | EFS and the ACE collection module |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014; slides 30, 37 and 45).
2. The service writes only schema `rwb_asset`; no cross-schema join and no foreign key into `public` (ADR-014, DP-01).
3. A route service reaches a shared capability through Temporal, never REST; a fact from ACE arrives through the rwb-source-data contract, and the slide 13 matrix draws no S5 cell to P1 (GAP-1750; ASM-2918).
4. REST is one hop from gateway-bff with a 2 s timeout, an Idempotency-Key on every POST and RFC 9457 problem details; a GET is retried once with jitter (ADR-020; slides 10 and 11).
5. Events are CloudEvents 1.0 on Kafka with an outbox and an inbox, retry at 1 minute, 10 minutes and 1 hour and then a dead-letter topic; topic `rwb.asset.events.v1` (ADR-015, DP-09, DP-14; slides 9 and 11).
6. Temporal namespace `rwb-recovery`, task queue `rwb-asset`; AssetDisposalWorkflow is a child of the case workflow; JOB-19 is a Temporal Schedule and Schedules and durable timers replace Quartz (ADR-016, DP-10; slides 19 and 44).
7. Rules are versioned data evaluated in process by the embedded Drools kit; authoring, testing and promotion are governed in rwb-decision, and every approval reads the delegation table cached from rwb-access (ADR-017, DP-04; RULE-011; DL18 open) (GAP-1763; ASM-2931).
8. There is no data lake: the asset and sale measures and the reporting read model come from the decision record and the events into rwb-reporting (ADR-018, DP-17).
9. Personal data stays out of events, workflow inputs and logs; masking is by role, and each service authorises the object itself (slide 10; NFR-039, NFR-040).
10. Documents are held in Blob with WORM through rwb-document only, and notices leave through rwb-comms and rwb-integration (slide 37; slides 16 and 17) (GAP-1767; ASM-2935).
11. Partners reach the bank through the partner gateway in the DMZ and users through gateway-bff (ADR-019; slide 10).
12. The bank scheduler owns only the cross-system edges and signals the business date; it never enters the case journey (slide 32).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-S5-01 | NPA and asset manager | Every asset on the books with its age, its cost and its provision step, and one stock balance with one owner | JRN-S5-01, JRN-S5-02 |
| ROL-S5-02 | Head of NPA | The floor approved at the level they own, the below-floor bid in front of them, and the exits that need their signature | JRN-S5-03, JRN-S5-04, JRN-S5-06 |
| ROL-S5-03 | Sale officer | An asset record, a price to propose, a listing to publish, a bid to accept and a transfer to record | JRN-S5-03, JRN-S5-04, JRN-S5-05, JRN-S5-06 |
| ROL-S5-04 | Auction vendor (external role) | One instruction with the asset, its starting bid and its schedule, and a round to run and report | JRN-S5-04 |
| ROL-S5-05 | Legal counsel | The eviction and the Land Office transfer named, tracked and closed, with their documents | JRN-S5-02, JRN-S5-05 |
| ROL-S5-06 | Enforcement owner | The judgment and enforcement result that puts an asset on the books or a sale in motion | JRN-S5-01 |
| ROL-S5-07 | Head of Asset Liquidity | A pool transfer to the asset management company or the joint venture with its approval and its price | JRN-S5-06 |
| ROL-S5-08 | RAMC user (external role) | The pool, its price and its schedule, and one transfer to record | JRN-S5-06 |
| ROL-S5-09 | Customer (borrower) | A buy-back offered at the template price with the approval the limit requires | JRN-S5-06 |
| ROL-S5-10 | Credit Administration officer | The sale recorded and the proceeds applied, with the shortfall raised | JRN-S5-05 |
| ROL-S5-11 | Partner and agency manager | The vendor's instruction, its result and its score, and the maintenance and broker partners' costs | JRN-S5-02, JRN-S5-06 |
| ROL-S5-12 | Product head (Mortgage, HP, SSME) | Assets of their product sold inside the delegation, and the exceptions named | JRN-S5-03 |
| ROL-S5-13 | Compliance and PDPA officer | Masking by role, an access log that cannot be skipped, and a classification on every record | JRN-S5-06 |
| ROL-S5-14 | Internal audit | A take-on, a price, a round and a sale that are reproducible from the record with their rule versions | JRN-S5-06 |
| ROL-S5-15 | Platform administrator | A workflow that reports a breach, an alert with a named owner, and a replay path | JRN-S5-04 |

Non-human actors: the case workflow that starts AssetDisposalWorkflow; the approval workflow on rwb-decision; the pricing agent on rwb-agent where an agent is used at all; the outbox relay; the consumers of AssetTakenOn and AssetSold. The auction vendor and the RAMC user are reached through the partner gateway at the edge and never by a direct call from this service.

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. The take-on is a hand-kept entry per repossession, deed in lieu or auction purchase; the same asset can appear twice and the date taken in is the date somebody typed it.
2. The holding age, the provision step and the cost of carry are watched on a spreadsheet, so a step is applied when somebody remembers.
3. The non performing asset stock balance has no owner and no single number (BR-012).
4. The floor price and the listing are checked by hand, and the floor can be seen by the market (the NPA sales cycle is 1,486 days against a target of 1,095).
5. The auction runs on phone calls and mail: the vendor is chosen by habit, the round is recorded afterwards, and a bid below the floor is accepted on a verbal agreement.
6. The transfer and the proceeds are reconciled by hand, and the shortfall is noticed when the case is read again.

Consequence: the same asset is priced twice, sold once and defended nowhere; the provision step trails the holding by weeks.

## 4.2 Target state (this product)

### JRN-S5-01 Take-on from the three sources (on trigger, system and sale officer)

1. A repossession completes, a deed in lieu transfer is registered, or the bank takes the property at the enforcement auction; rwb-case starts AssetDisposalWorkflow on this service.
2. The workflow reads the ACE asset facts through the rwb-source-data contract with the business date and the load time behind them, and matches the record to the ACE asset key.
3. It opens one holding record with the source (LOV-TRANSFER-IN), the date taken in, the opening book value, the condition, the photographs, the location and the provision step in force.
4. It starts the holding age and the provision step clocks, and publishes AssetTakenOn for rwb-case and rwb-payment.
5. Where the statutory notice is required, it is raised through rwb-comms and the take-on waits for its proof of delivery; where delivery is not proved, the asset sits in the failed notice queue with a task for the sale officer.

### JRN-S5-02 Hold, care and the provision step (monthly and on events, NPA and asset manager)

1. The NPA and asset manager reads the asset list with the age, the holding cost, the value and the sale status of every asset held.
2. The monthly scan tests the holding age against the provision thresholds in force and records the step applied with its threshold, its rule version and its date.
3. Maintenance, insurance and custody costs are recorded against the asset, with their evidence in the document hub and the work order accepted before its invoice is released.
4. The stock balance is published monthly with the count and the value by class and status, under the one owner role in force.
5. Where occupants refuse possession, the eviction is opened with Legal named, and the asset returns to hold and resumes its disposal route when the property is vacant.

### JRN-S5-03 Price and list (on the disposal decision, sale officer and Head of NPA)

1. On the monthly re-appraisal scan, an appraisal older than the interval in force raises a re-appraisal order and records it; a price is refused on an appraisal older than a year (MSG-S5-002).
2. The route is recommended — auction, broker, RAMC, buy-back or rental — with the expected return on each and the reasons, and the route is approved inside the delegation or at the committee above it.
3. A start price and a floor are proposed from the accepted value; the floor goes to the approver role the delegation names, and a floor below that role's limit is refused with MSG-S5-001.
4. The approved floor becomes the reserve, with the step schedule for the asset class, and is not published.
5. The listing is published from one action: the prices, the rounds and the schedule are recorded, the auction channel is instructed, and the bank channel step is recorded with its date and reference where the interface does not exist yet.

### JRN-S5-04 Run the auction (per round, auction vendor and sale officer)

1. The asset is allocated to one panel vendor by the allocation rule in force, and the vendor is instructed with the asset, the starting bid, the inspection evidence and the schedule.
2. The vendor lists the asset, runs the round and reports the bids; each bid is recorded against the round and the asset.
3. A round that closes with no bid steps the price down the published ladder and opens the next round, while the re-list count is below the limit; at the limit the outcome is recorded and the case is raised to the next decision.
4. A bid below the floor goes for a second signature and is accepted only with it; a sale at or above THB 50m goes to sealed bids at the committee.
5. The winning bidder's payment is tracked against the five-day term; where it is absent when due, the award is cancelled, the asset is released and the round reopens.

### JRN-S5-05 Transfer and proceeds (per sale, sale officer and Credit Administration officer)

1. The vehicle registration is transferred through SCIS and the submission and its 10-working-day clock are recorded; the Land Office transfer of a property is recorded as an officer step with its documents.
2. The sale is recorded with its contract and sale dates, its price, its transfer fee, its taxes and its gain or loss.
3. The proceeds are handed to rwb-payment, the matched result comes back on ProceedsMatched, and a residual above zero is raised for the next decision instead of being left on the case.
4. AssetSold reaches rwb-payment and rwb-case in the same step as the sale, so the case moves without a second action.

### JRN-S5-06 The other exits, and the read-back (per exit, and at audit)

1. A pool of assets goes to the asset management company or the joint venture with committee approval, the transfer price from the template version and the transfer recorded.
2. A customer buy-back runs on the terms the limit requires, at the template price and with a second signature.
3. A rental is recorded with its terms, its auto-debit and its arrears follow-up while the asset is held; a broker sale runs with its fee and terms for the asset classes the rule names, tracked to the sale.
4. An auditor reads one take-on, one price, one round and one sale: the facts used, the rule versions, the allocation and its reason, the approvals with their levels and approvers, the bids and the outcome.
5. The compliance officer reads the masking matrix and the access log; a developer builds against the published contract and its fake, and a build that reads an ACE view or an ACE table directly fails.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-S5-001 | Asset take-on from the three sources | Every repossessed, surrendered or auction-purchased asset is on the books once, with its source and its date taken in | BR-010 | Must | 2 | FEAT-AST-01 (A2.1), FEAT-AST-02 (A2.2), FEAT-AST-03 (A2.3) |
| CAP-S5-002 | Statutory notice and proof of delivery | The notice the repossession needs is served and its proof is on the case, and an unproved notice holds the take-on | BR-010 | Must | 2 | FEAT-AST-04 (A2.4) |
| CAP-S5-003 | Holding age and the provision step | The provision step is applied by rule at each threshold, without a person watching a list | BR-011 | Must | 2 | FEAT-AST-05 (A2.5) |
| CAP-S5-004 | Stock balance with one owner | The non performing asset stock has one number and one named owner, reported monthly | BR-012 | Must | 2 | FEAT-AST-06 (A2.6) |
| CAP-S5-005 | Holding costs and the work order | Maintenance, insurance and custody costs are on the asset, and a repair is accepted before its invoice is released | BR-013 | Must | 2 | FEAT-AST-07 (A2.7) |
| CAP-S5-006 | Re-appraisal on cycle | The re-appraisal is ordered when the period passes, and its value resets the price inputs | BR-011 | Must | 2 | FEAT-AST-09 (A2.9) |
| CAP-S5-007 | Disposal route with its expected return | The route is proposed with the return on each option and its reasons, and approved by the role that owns it | BR-014 | Must | 2 | FEAT-AST-10 (A2.10) |
| CAP-S5-008 | Start price, floor and the floor approval | The floor is approved at the level in force, refused below that level, and withheld from publication | BR-014 | Must | 2 | FEAT-AST-11 (A2.11) |
| CAP-S5-009 | Listing published from one action | One action records the listing and issues the publication, and shows what was published and what stayed manual | BR-014 | Must | 2 | FEAT-AST-12 (A2.12) |
| CAP-S5-010 | Eviction with Legal named | The eviction is opened, tracked and closed with Legal on it, and the asset resumes its route when vacant | BR-026 | Must | 3 | FEAT-AST-08 (A2.8) |
| CAP-S5-011 | The price ladder and the rounds | Each round steps the price down the published ladder until a bid clears the floor, and every round is recorded | BR-027 | Must | 3 | FEAT-AST-13 (A2.13), FEAT-AST-15 (A2.15) |
| CAP-S5-012 | Vendor allocation and instruction | One panel vendor is allocated by the rule in force, with its reason, and instructed through the partner contract | BR-027 | Must | 3 | FEAT-AST-14 (A2.14) |
| CAP-S5-013 | Below the floor with a second signature | A bid under the floor cannot be accepted without a second signature, and a large sale goes to sealed bids | BR-028 | Must | 3 | FEAT-AST-16 (A2.16) |
| CAP-S5-014 | Re-list on no bid and the re-list limit | A round with no bid re-lists at the next step, and at the limit the case moves to the next decision | BR-027 | Must | 3 | FEAT-AST-17 (A2.17) |
| CAP-S5-015 | The five-day payment term | The winning bidder's payment is tracked, and a missed term cancels the award and reopens the round | BR-028 | Must | 3 | FEAT-AST-18 (A2.18) |
| CAP-S5-016 | Title transfer for a vehicle and a property | The vehicle transfer is submitted through SCIS and the property transfer is recorded at the Land Office, each with its clock | BR-029 | Must | 3 | FEAT-AST-19 (A2.19), FEAT-AST-20 (A2.20) |
| CAP-S5-017 | Proceeds applied and shortfall raised | The sale is recorded, the proceeds are applied through rwb-payment and the residual reaches the next decision | BR-030 | Must | 3 | FEAT-AST-21 (A2.21) |
| CAP-S5-018 | The other exits on a recorded approval | A pool to the asset management company, a buy-back, a rental and a broker sale each carry their approval | BR-030 | Must | 3 | FEAT-AST-22 (A2.22), FEAT-AST-23 (A2.23), FEAT-AST-24 (A2.24), FEAT-AST-25 (A2.25) |
| CAP-S5-019 | Freshness and the data date | Every take-on, price, listing and round states how old its data is, and a stale product is seen rather than assumed | BR-010, BR-011, BR-014 | Must | 2 | A2.1 to A2.25 (VR-S5-001-1 to VR-S5-025-1, VR-S5-016-2) |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Direct read of the ACE NPA asset, asset, collateral and score views | Not carried | rwb-source-data's contract (GAP-1750; ASM-2918) |
| The asset record as an ACE-owned extension | Not carried as an extension | This service's holding record, keyed by the ACE asset key (GAP-1751; ASM-2919) |
| Direct posting of proceeds, cost of carry and fees to ALS and the general ledger | Not carried | P8 rwb-payment through postProceeds (GAP-1759; ASM-2927) |
| Direct call to SVAF for a re-appraisal | Not carried | The valuation owner's contract, read back through rwb-source-data (GAP-1758; ASM-2926) |
| Quartz scheduling of the re-appraisal and the round clocks | Replaced | JOB-19 as a Temporal Schedule and durable timers in AssetDisposalWorkflow (ADR-016, DP-10) |
| Automatic publication to HOME.SCB | Deferred | An officer step recorded with its date and reference until INT-27 exists (GAP-1756; ASM-2924) |
| The disposal decision tables as Excel in the monolith | Moved | Governance in P7 rwb-decision; evaluation local, disposal package in Phase 2 (GAP-1761; ASM-2929) |
| The debt sale of the asset's residual and the write-off | Out of scope | S6 rwb-debtsale and S7 rwb-writeoff |

# 6. Functional requirements

Every requirement is specific and testable. The FSD requirement column keeps the trace to the source. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-S5-001 | The service SHALL obtain every asset, collateral, appraised value and COLLINS score fact it needs through the rwb-source-data contract. A read of a `recovery.v_ace_*` view, a read of an ACE table, and a constraint in schema `rwb_asset` that references a table outside it, SHALL fail the build and the boundary test. | CAP-S5-019 | BR-010 | REQ-S5-001 | Must | 2 |
| FR-S5-002 | The service SHALL link each holding record to its ACE asset, and through it to the collateral, by a business-key column of type `varchar(255)` with no foreign key, and SHALL hold one record per ACE asset key with no copy of an ACE column. | CAP-S5-001 | BR-010 | REQ-S5-001 | Must | 2 |
| FR-S5-003 | The service SHALL open one holding record on each take-on trigger — a completed repossession, a registered deed in lieu transfer, or an LED handover after the 100, 90, 80 then 70 percent ladder — and SHALL record the source from LOV-TRANSFER-IN, the date taken in, the opening book value, the condition, the photographs, the location and the provision step in force. | CAP-S5-001 | BR-010 | REQ-S5-001 | Must | 2 |
| FR-S5-004 | The service SHALL publish AssetTakenOn on `rwb.asset.events.v1` in the same transaction as the holding record, with the asset key and the case, for rwb-case and rwb-payment, and SHALL NOT carry a value, a party or any other personal data in it. | CAP-S5-001 | BR-010 | REQ-S5-001 | Must | 2 |
| FR-S5-005 | The service SHALL refuse the take-on, the price, the floor, the listing, the round, the award, the transfer and every exit to a role without the capability area, with MSG-P4-002, and SHALL change nothing on a refusal. | CAP-S5-001 | BR-010 | REQ-S5-001 | Must | 2 |
| FR-S5-006 | The service SHALL write one append-only decision record for every take-on, price, floor approval, listing, round, award, transfer and exit before the change it records, carrying the rule version, the inputs snapshot and the actor; where the record cannot be written it SHALL change nothing, show MSG-P7-003 and raise an incident. | CAP-S5-001 | BR-010, BR-030 | REQ-S5-001, REQ-S5-009 | Must | 2 |
| FR-S5-007 | The service SHALL read every threshold, interval, approval limit, ladder step, re-list limit, template price and timer from versioned reference data or from the rule package in force, SHALL apply a change from its valid-from date without a code release, and SHALL record the version applied. | CAP-S5-003 | BR-011, BR-014 | REQ-S5-003 | Must | 2 |
| FR-S5-008 | The service SHALL raise the statutory notice the take-on requires through the rwb-comms contract, SHALL hold the take-on until a proof of delivery is recorded, and SHALL record the proof with its date, its channel and the address it was served to. | CAP-S5-002 | BR-010 | REQ-S5-001 | Must | 2 |
| FR-S5-009 | Where the proof of delivery is absent, the service SHALL keep the asset in the failed notice queue, raise a task for the sale officer naming the address, and re-serve on a confirmed address before the take-on resumes. | CAP-S5-002 | BR-010 | REQ-S5-001 | Must | 2 |
| FR-S5-010 | The service SHALL count the holding age in days from the date taken in at the business date and SHALL apply the provision step the policy sets at each threshold, recording the step, the threshold, the rule version and the date it was applied. | CAP-S5-003 | BR-011 | REQ-S5-003 | Must | 2 |
| FR-S5-011 | The service SHALL start the holding age and provision step clocks and charge the cost of carry monthly while the title is clear or under transfer, and SHALL hold the clocks and stop the charge while the title is unresolved. | CAP-S5-003 | BR-011 | REQ-S5-003 | Must | 2 |
| FR-S5-012 | The service SHALL record the title state on the holding record, SHALL block the disposal route while the title is unresolved, and SHALL release the asset to hold and to the disposal route when the title is clear. | CAP-S5-003 | BR-011 | REQ-S5-003 | Must | 2 |
| FR-S5-013 | The service SHALL publish the non performing asset stock balance monthly with its count and its value by asset class and holding status, with the business date it was taken at. | CAP-S5-004 | BR-012 | REQ-S5-002 | Must | 2 |
| FR-S5-014 | The service SHALL hold the owner of the stock balance as a role in versioned reference data, SHALL show it on the balance and on the report, and SHALL refuse to publish a balance where no owner role is in force. | CAP-S5-004 | BR-012 | REQ-S5-002 | Must | 2 |
| FR-S5-015 | The service SHALL record maintenance, insurance and custody costs against the asset with their type, their date, their amount, their evidence in the document hub and their approval where a limit applies, and SHALL roll them into the holding cost to date. | CAP-S5-005 | BR-013 | REQ-S5-001 | Must | 2 |
| FR-S5-016 | The service SHALL raise a work order for a repair, SHALL record its acceptance or refusal with the reason, and SHALL release its invoice for payment only on acceptance. | CAP-S5-005 | BR-013 | REQ-S5-001 | Must | 2 |
| FR-S5-017 | The service SHALL read the accepted appraisal and its date through the owner's contract and SHALL test the appraisal age against the interval in force at the business date. | CAP-S5-006 | BR-011 | REQ-S5-003 | Must | 2 |
| FR-S5-018 | The service SHALL raise the re-appraisal order on the monthly Schedule where the appraisal is older than the interval in force, through the valuation owner's contract, and SHALL record the order with its date, its rule version and the interval applied; a failed order SHALL be retried and then moved to an exception queue with a task for a named owner. | CAP-S5-006 | BR-011 | REQ-S5-003 | Must | 2 |
| FR-S5-019 | On the appraisal arriving, the service SHALL update the appraised value and reset the list and floor price inputs, and SHALL refuse to price an asset whose appraisal is older than a year with MSG-S5-002. | CAP-S5-006 | BR-014 | REQ-S5-004 | Must | 2 |
| FR-S5-020 | The service SHALL propose the disposal route — auction, broker, RAMC, buy-back or rental — with the expected return on each option and the reasons, and SHALL record the chosen route with the rule version and the economics it rested on. | CAP-S5-007 | BR-014 | REQ-S5-004 | Must | 2 |
| FR-S5-021 | Where a pricing agent proposes the route or the price, the service SHALL reach it only through the rwb-agent contract, SHALL wait at most 60 seconds, SHALL fall back to the rule result where the answer is late or fails its schema check, and SHALL record the model and prompt versions and any override with its coded reason. | CAP-S5-007 | BR-014 | REQ-S5-004 | Must | 2 |
| FR-S5-022 | The service SHALL record the route approval with the level applied and the approver, SHALL move the asset only on an approval, and SHALL raise the approval to the committee where the amount is above the level that applies. | CAP-S5-007 | BR-014 | REQ-S5-004 | Must | 2 |
| FR-S5-023 | The service SHALL propose a start price and a floor price for every asset from the accepted appraisal and the rules in force, and SHALL show both with the value and the rule version they were derived from. | CAP-S5-008 | BR-014 | REQ-S5-004 | Must | 2 |
| FR-S5-024 | The service SHALL route the floor to the approver role the delegation names, SHALL refuse a floor below that role's limit with MSG-S5-001, and on approval SHALL fix the floor as the reserve with the step schedule for the asset class. | CAP-S5-008 | BR-014 | REQ-S5-004 | Must | 2 |
| FR-S5-025 | The service SHALL publish the listing from one action: it SHALL record the listing with its sale channel, start price, floor, rounds and schedule, SHALL issue the publication to the auction channel through the partner contract, and SHALL record the bank channel step with its date and reference where that interface is not available. | CAP-S5-009 | BR-014 | REQ-S5-005 | Must | 2 |
| FR-S5-026 | The service SHALL publish a listing only where at least one photograph and an inspection report are held and the title is clear, and SHALL withhold the floor price from every publication. | CAP-S5-009 | BR-014 | REQ-S5-005 | Must | 2 |
| FR-S5-027 | The service SHALL open an eviction with Legal named where the occupants refuse possession, SHALL track it with its documents, and SHALL return the asset to hold and resume its disposal route when the property is vacant. | CAP-S5-010 | BR-026 | No requirement ID (BR-026; FEAT-AST-08) | Must | 3 |
| FR-S5-028 | The service SHALL run each auction round as a timed step of AssetDisposalWorkflow, SHALL step the price down the published ladder at each round while the round price is above the floor, and SHALL record each round with its number, its price, its opening and closing times and its outcome. | CAP-S5-011 | BR-027 | REQ-S5-006 | Must | 3 |
| FR-S5-029 | The service SHALL record each bid the vendor reports against the round and the asset, with its amount, its bidder reference and its time, and SHALL treat a bid at or above the floor as clearing the round. | CAP-S5-011 | BR-027 | REQ-S5-006 | Must | 3 |
| FR-S5-030 | The service SHALL allocate one panel vendor to each asset by the allocation rule in force, and SHALL record the rule version, the reason, the vendor and its capacity state with the allocation. | CAP-S5-012 | BR-027 | REQ-S5-006 | Must | 3 |
| FR-S5-031 | The service SHALL instruct the allocated vendor through the rwb-partner contract with the asset, the starting bid, the inspection evidence and the schedule, and SHALL record the instruction and its result on the asset. | CAP-S5-012 | BR-027 | REQ-S5-006 | Must | 3 |
| FR-S5-032 | The service SHALL route a bid below the floor for a second signature, SHALL hold the sale until that signature is present, and SHALL record the signature, its role and the reason with the sale. | CAP-S5-013 | BR-028 | REQ-S5-007 | Must | 3 |
| FR-S5-033 | The service SHALL raise a sale at or above the amount in force for sealed bids to the committee before the award, with the bids and the floor, and SHALL record the committee's decision with the level applied. | CAP-S5-013 | BR-028 | REQ-S5-007 | Must | 3 |
| FR-S5-034 | Where a round closes with no bid, the service SHALL re-list the asset at the next price step while the re-list count is below the limit in force, and at the limit SHALL record the outcome and raise the case to the next decision instead of running another round. | CAP-S5-014 | BR-027 | REQ-S5-006 | Must | 3 |
| FR-S5-035 | The service SHALL record the winning bidder and the amount due with the five-day payment term from the award, and SHALL show the due date on the asset and on the case task. | CAP-S5-015 | BR-028 | REQ-S5-007 | Must | 3 |
| FR-S5-036 | Where the payment is absent when the term expires, the service SHALL cancel the award, release the asset, reopen the round and record the reason, and SHALL record the vendor's score effect where the vendor is at fault. | CAP-S5-015 | BR-028 | REQ-S5-007 | Must | 3 |
| FR-S5-037 | The service SHALL prepare and submit the vehicle registration transfer through the integration contract, record the submission, its reference and its 10-working-day clock, and SHALL record the Land Office transfer of a property as an officer step with its date, its reference and its documents. | CAP-S5-016 | BR-029 | REQ-S5-008 | Must | 3 |
| FR-S5-038 | The service SHALL record the sale with its contract date, its sale date, its price, its transfer fee, its specific business tax, its corporate income tax, its incentive and its gain or loss. | CAP-S5-017 | BR-030 | REQ-S5-009 | Must | 3 |
| FR-S5-039 | The service SHALL hand the proceeds to rwb-payment, SHALL apply the result it receives on ProceedsMatched to the sale, SHALL raise the residual above zero for the next decision, and SHALL publish AssetSold on `rwb.asset.events.v1` in the same transaction as the sale. | CAP-S5-017 | BR-030 | REQ-S5-009 | Must | 3 |
| FR-S5-040 | The service SHALL record a pool transfer to the asset management company or the joint venture with its committee approval, its transfer price from the template version and its transfer, and SHALL track it from instruction to completion. | CAP-S5-018 | BR-030 | REQ-S5-010 | Must | 3 |
| FR-S5-041 | The service SHALL open a customer buy-back at the template price with the approval the limit requires and the second signature where the rule requires it, and SHALL record the terms and the outcome. | CAP-S5-018 | BR-030 | REQ-S5-010 | Must | 3 |
| FR-S5-042 | The service SHALL record a rental of a held asset with its terms, its auto-debit and its arrears follow-up, and SHALL hold the asset as rented for the rental period. | CAP-S5-018 | BR-030 | REQ-S5-010 | Must | 3 |
| FR-S5-043 | The service SHALL open a broker sale with its fee and its terms for the asset classes the rule names, and SHALL track it to the sale. | CAP-S5-018 | BR-030 | REQ-S5-010 | Must | 3 |
| FR-S5-044 | The service SHALL return, with every asset read and with every take-on, price, listing and round, the business date and the load time of each data product behind it with its status LOADED or STALE, SHALL show a stale product with its date and MSG-P1-001, and SHALL start no take-on, price, listing or round on a product whose freshness cannot be read. | CAP-S5-019 | BR-010, BR-014 | REQ-S5-001, REQ-S5-004 | Must | 2 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Source NFR | Priority | Test |
|---|---|---|---|---|---|---|
| NFR-S5-001 | The asset list loads with the age, the holding cost, the value and the sale status of every asset held, under the busiest-hour load. | Under 2 seconds | BR-012 | NFR-008 | Must | Performance test in SIT |
| NFR-S5-002 | The asset record loads for an asset with 50 documents. | Under 2 seconds | BR-010, BR-013 | NFR-009 | Must | Performance test in SIT |
| NFR-S5-003 | A rule evaluation at the disposal decision, the price step and the floor approval completes inside the user's wait. | Under 300 milliseconds at the 95th percentile | BR-014, BR-027 | NFR-011 | Must | Rule timing test with the package in force |
| NFR-S5-004 | The pricing agent answers inside its target; after that the rule result is used and the disposal still proceeds. | Under 60 seconds, then the rule result | BR-014 | NFR-010, NFR-024 | Must | Agent timeout drill |
| NFR-S5-005 | The service carries the asset population of the non performing book and the round volume of the auction cycle. | The case volume of NFR-001: about 23,600 open cases at go-live and 26,500 at the end of 2027; the asset and round volumes are not stated (GAP-1769; ASM-2937) | BR-010, BR-011 | NFR-001 | Must | Volume test at the stated volume, rerun when the asset volume is given |
| NFR-S5-006 | Every take-on, price, listing and round states the business date and the load time of the data products it read. | Every take-on, price, listing and round | BR-010, BR-014 | NFR-013 | Must | Decision record inspection |
| NFR-S5-007 | A missing, failed or late ACE batch is visible at the take-on, the price and the round, and alerts the data steward. | Visible at the action; alert to the steward | BR-010 | NFR-014 | Must | Hold an ACE batch in SIT |
| NFR-S5-008 | The service holds no load window, no staging table and no catch-up job: a late ACE batch delays the action and raises an alert. | No load, no staging, no catch-up | BR-010 | NFR-015 | Must | Hold and release the batch |
| NFR-S5-009 | The service is available during business hours and outside them, when the round clocks and the monthly scan run. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | BR-010 | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-S5-010 | The service inherits the ACE recovery point and recovery time, and a running AssetDisposalWorkflow resumes where it stopped. | The ACE recovery point objective and recovery time objective; workflow history preserved | BR-010 | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-S5-011 | Every take-on, price, round and sale is reproducible from the log, including the rule version and the inputs used. | Every action reproducible | BR-030 | NFR-033 | Must | Re-run a sample from the log |
| NFR-S5-012 | Every action carries the rule version applied and the approver who allowed it. | Every action | BR-014, BR-028 | NFR-034 | Must | Decision record inspection |
| NFR-S5-013 | The floor approval and the second signature read the delegation table in force at the moment of the action, and a change to it takes effect from its valid-from date. | Read at run time; no code release | BR-014, BR-028 | NFR-034 | Must | Delegation change drill |
| NFR-S5-014 | The decision log hash chain is checked daily and a break is reported to Compliance the same day. | Daily check, same-day report | BR-030 | NFR-035 | Must | Chain break drill |
| NFR-S5-015 | An audit or regulatory request about an asset, a round or a sale is answered inside its deadline with the decision history and the supporting documents. | Inside the deadline set by the requester | BR-010 | NFR-036 | Must | One request rehearsed in SIT |
| NFR-S5-016 | Agent acceptance, override rate, latency and cost are measured and reported per agent where an agent proposes a route or a price. | Measured per agent | BR-014 | NFR-066 | Must | Agent measure report review |
| NFR-S5-017 | A model or agent write to a round, a price or a task is logged with its model or agent version, on the same terms as a decision taken by a person. | Every write | BR-030 | NFR-078 | Must | Agent write inspection |
| NFR-S5-018 | Party and bidder identifiers are masked at rest and on every screen and agent call, by role. | Masked at rest and in use | BR-010 | NFR-039 | Must | Masking matrix test across roles |
| NFR-S5-019 | Each screen and each agent receives only the personal data it needs. | Data minimisation per screen and per agent | BR-010 | NFR-040 | Must | Contract review per screen and per agent |
| NFR-S5-020 | Every read of a personal field is logged, and the read is refused rather than returned where the log cannot be written. | Every read | BR-010 | NFR-042 | Must | Access log reconciliation against reads |
| NFR-S5-021 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | BR-010 | NFR-045 | Must | Environment data review |
| NFR-S5-022 | Every data product and every record this service holds carries a data classification that sets its handling. | Classification applied per record | BR-010 | NFR-047 | Must | Classification review |
| NFR-S5-023 | Recovery data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | BR-010 | NFR-046 | Must | Tenancy review |
| NFR-S5-024 | Staff authenticate with single sign-on and multi-factor authentication; partner users of the auction vendor and the RAMC authenticate with multi-factor and are scoped to their own assets. | Entra ID single sign-on with multi-factor; partner multi-factor and scope | BR-010 | NFR-049, NFR-050, NFR-051 | Must | Sign-in, identity and scope test |
| NFR-S5-025 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | BR-010 | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-S5-026 | The build blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency, and every agent output is schema checked with the rule fallback. | Pipeline checks pass; schema check on every agent output | BR-014 | NFR-054, NFR-055 | Must | Pipeline run with a seeded violation |
| NFR-S5-027 | Screen labels, validation messages and error messages served with this service's operations are available in Thai and in English. | Every label and message in Thai and English | BR-010 | NFR-059 | Must | Label and message review |
| NFR-S5-028 | Logs, traces and metrics are produced for the take-on, the price, the round and the sale, every Schedule and job has a run book, and a failure alerts a named owner. | Every job covered; alert within 15 minutes to the named owner | BR-010, BR-011 | NFR-064, NFR-067, NFR-068 | Must | Observability review and alert drill |
| NFR-S5-029 | A call is one hop with a 2 s timeout; a failure is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; events that cannot be processed go to the dead-letter topic and are replayed. | One hop; 2 s timeout; three retries then the exception queue; dead-letter with replay | BR-010, BR-027, BR-029 | NFR-025, NFR-026 | Must | Failure injection |
| NFR-S5-030 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in schema `rwb_asset`. | Rollback by previous tag; per-service migration | BR-010 | NFR-027 | Must | Rollback rehearsal |
| NFR-S5-031 | The asset screens meet the bank's accessibility standard, work on the browsers the bank supports, and work on the devices the auction partner actually uses. | WCAG 2.1 level AA; the current and previous major versions of Microsoft Edge and Google Chrome; tablets for the auction partner | BR-012 | NFR-060, NFR-061, NFR-063 | Must | Accessibility scan, browser test and device test |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_asset`. Every table carries the record columns of the platform library (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`). The Ownership Map names two of the five entity groups, so the physical names of the rest are written with the DB story (GAP-1752; ASM-2920). Retention is stated by class; the periods are open (GAP-1764; ASM-2932).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `asset` holding record (entity group) | Owned record, one per ACE asset key; the map lists no row for it (GAP-1751; ASM-2919) | `asset_key` (`varchar(255)`), case and collateral references by business key, `asset_ref`, `asset_code`, `asset_type` (LOV-ASSET-TYPE), `transfer_in_type` (LOV-TRANSFER-IN), `from_segment` (LOV-SEGMENT), `transfer_in_date`, `book_value`, `auction_purchase_price`, `repossessed_date`, `stock_date`, `holding_status` (LOV-HOLDING), `holding_cost_to_date`, the title state, the date taken in, the provision step with its threshold and rule version, and the notice state with its proof | [SENSITIVE_FINANCIAL] | ACE asset facts through the source-data contract; the take-on and the holding are this service's decisions (DF-COL-028 to DF-COL-042) | Workbench record class; period open |
| `listing` (map: S5) | Owned record, one per listing of an asset | `id`, `asset_id`, `sale_channel` (LOV-SALE-CHANNEL), `start_price`, `floor_price`, `round_no`, `listed_at`, `status` (LOV-LISTING), the approved floor with its approver role and level, the step schedule and the publication references (DF-SAL-001 to DF-SAL-008) | [SENSITIVE_FINANCIAL] | Workbench; the value it derives from is read through contracts | Workbench record class; period open |
| `asset_sale` (map: S5) | Owned record, one per sale of an asset | `id`, `asset_id`, `listing_id`, `contract_date`, `sale_date`, `sale_price`, `transfer_fee`, `specific_business_tax`, `corporate_income_tax`, `gain_loss`, `incentive_amount`, the winning bid, the second signature where a bid was below the floor, and the residual raised (DF-SAL-009 to DF-SAL-019) | [SENSITIVE_FINANCIAL] | Workbench; the posting result comes from rwb-payment | Workbench record class; period open |
| Auction round and bid (entity group) | Owned records, one per round and one per bid; no map row (GAP-1752; ASM-2920) | Round number, opening and closing time, the price at that round, the ladder step applied with its rule version, the outcome, the re-list count; bid amount, bidder reference, bid time and the clearing result | [SENSITIVE_FINANCIAL], with the bidder reference [PII] | Workbench and the vendor's reported result through the partner contract | Workbench record class; period open |
| Holding cost movement (entity group) | Owned records, one per cost and one per work order; no map row (GAP-1752; ASM-2920) | Cost type, date, amount, the evidence reference in the document hub, the approval where a limit applies, the work order with its acceptance or refusal and the invoice release | [SENSITIVE_FINANCIAL] | Workbench; the posting is rwb-payment's | Workbench record class; period open |
| `outbox_event`, `processed_event`, `idempotency_key` | Platform library objects created in this schema | Library-defined | [CONFIDENTIAL] | Service template | Library policy (PLT; ASM-0074) |

No copy of an ACE column is held, and no foreign key leaves the schema. The field list of the round, the bid and the cost movement is taken from the rules that use them and is open until the DB story (GAP-1752; ASM-2920).

## 8.2 Data read but not owned

| Data | Read through | Views behind it | Classification of the data read |
|---|---|---|---|
| The NPA asset, asset type and transfer-in facts | rwb-source-data contract (REST) | `v_ace_npa_asset`, `v_ace_asset` | [SENSITIVE_FINANCIAL] |
| The collateral the asset came from | rwb-source-data contract (REST) | `v_ace_collateral` | [SENSITIVE_FINANCIAL] |
| COLLINS economics for the route and the price | rwb-source-data contract (REST) | `v_ace_score` | [CONFIDENTIAL] |
| Freshness of each data product | rwb-source-data contract (REST) | `v_ace_batch_status` | [CONFIDENTIAL] |
| The accepted appraisal, its date and its valuer | The valuation owner's contract for the order, and rwb-source-data for the value (GAP-1758; ASM-2926) | `v_ace_valuation` behind P1 | [SENSITIVE_FINANCIAL] |
| Case, party, stage, queue and tasks | rwb-case contract (Temporal activity and REST) | none (case schema) | [PII], [SENSITIVE_FINANCIAL] |
| Roles, capability areas, masking policy and the delegation table | rwb-access permission data, cached | none (access schema) | [CONFIDENTIAL] |
| Rule packages and the version in force | rwb-decision contract and events | none (decision schema) | [CONFIDENTIAL] |
| Vendor panel, instructions, results and scorecards | rwb-partner contract (Temporal activity and REST) | none (partner schema) | [CONFIDENTIAL] |
| Documents, custody and retention state | rwb-document contract | none (document schema) | [CONFIDENTIAL], [PII] |
| Notice templates and the proof of delivery | rwb-comms contract and events | none (comms schema) | [CONFIDENTIAL], [PII] |
| Proceeds, fees and the matched posting | rwb-payment contract and ProceedsMatched | none (payment schema) | [SENSITIVE_FINANCIAL] |
| LOV-ASSET-TYPE, LOV-HOLDING, LOV-LISTING, LOV-SALE-CHANNEL, LOV-SEGMENT and LOV-TRANSFER-IN | rwb-case reference-data contract | none (case schema) | [CONFIDENTIAL] |

Counts are not stated: the FSD gives no field count for this module, and no count is recomputed here.

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| Book value, auction purchase price, holding cost to date | What the bank has in the asset, in baht | [SENSITIVE_FINANCIAL] | Read access by role; no value in an event, a workflow input or a log |
| Start price, floor price, sale price, gain or loss | The pricing and the outcome of the sale | [SENSITIVE_FINANCIAL] | Served on the asset, listing and sale screens; the floor is withheld from every publication and is never carried in a published event |
| Bid amount and bidder reference | Who bid what | [SENSITIVE_FINANCIAL], [PII] | The bidder reference is masked by role and never published in an event |
| Transfer fee, specific business tax, corporate income tax, incentive | What the sale cost and what it produced | [SENSITIVE_FINANCIAL] | Held on the sale record; the posting values go to rwb-payment, not through an event |
| Customer identification number and name, where the case party is shown | The party the case belongs to | [PII] | Masked by role; the identification number never leaves in clear; every read logged |
| Contact value, where the buy-back or the notice shows the last contact | How the customer was reached | [PII] | Masked by default, full only where a masking row for the role allows it |
| Vendor and partner reference (auction vendor, broker, valuer) | Who did the work | [CONFIDENTIAL] | Read by role; partners are external roles reached through the partner gateway |
| Agent output and its prompt, where an agent is used | The proposal and the material it was given | [CONFIDENTIAL] | No personal data in the prompt, the output or the log (NFR-040) |

The FSD marks the eight asset catalog fields (`asset_key`, `asset_ref`, `asset_code`, `asset_type`, `transfer_in_type`, `from_segment`, `transfer_in_date` and the collateral key) as not personal data. The bidder and party fields reach the screens through this service's own records and through the case contract, and are handled as personal data by this document (GAP-1764; ASM-2932).

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code: the provision thresholds, the re-appraisal interval, the cost of carry, the floor limits, the ladder, the re-list limit, the template price, the payment term and the transfer clock.
2. This service holds no copy of an ACE column and no staging table; it reads ACE data through the source-data contract only (GAP-1750; ASM-2918).
3. A link to an ACE record is a business-key column of type `varchar(255)` with no foreign key.
4. A personal field is not returned when the access log cannot be written.
5. Personal data is not put in an event, a workflow input or a log; AssetTakenOn and AssetSold carry the asset, the case, the outcome and the versions, not the values.
6. ACE data is retained by ACE, and the archive of a Workbench record belongs to rwb-document.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-source-data (P1) | Out and in | REST, one hop, 2 s timeout, GET retried once with jitter | P1 | The only path to the NPA asset, asset, collateral, score and freshness facts; the slide 13 matrix draws no S5 cell to P1 (GAP-1750; ASM-2918) |
| ACE database, tables behind the 30 views | Not read | None | ACE team | Read only through the P1 contract. No direct `public` read and no DML from this service |
| rwb-case (P3) | In and out | Temporal child workflow (AssetDisposalWorkflow) and REST; events listened to | P3 | The case starts the disposal and owns the parent workflow, the queues, the tasks and the timer path; this service publishes AssetTakenOn and AssetSold for it |
| rwb-decision (P7) | Out and in | Temporal activity and child workflow (approval); events listened to | P7 | Approval routing on the delegation for the floor, the route, the below-floor bid, the sealed-bid sale, the RAMC pool and the buy-back; rule package governance; the decision record and the hash chain |
| rwb-access (P4) | In | Cached permission data through the guard library, not a call on the hot path | P4 | Roles, capability areas, masking policy and the delegation table |
| rwb-agent (P10) | Out, where an agent is used | Temporal, child workflow and activity | P10 | The pricing agent under its contract, 60 s then the rule result (DP-20; GAP-1760; ASM-2928) |
| rwb-partner (S9) | Out and in | Temporal activity (issueInstruction) and REST; PartnerResultSubmitted listened to | S9 | The vendor panel, the instruction and the reported result. FEAT-PRM-03 is delivered in wave 4, so this service builds against the contract and its fake (GAP-1757; ASM-2925) |
| rwb-payment (P8) | Out and in | Temporal activity (postProceeds); ProceedsMatched listened to | P8 | Proceeds, fees, cost of carry and every posting, with the residual returned for the next decision (GAP-1759; ASM-2927) |
| rwb-litigation (S4) | In | Events | S4 | JudgmentRecorded and AuctionResult put an asset on the books or open enforcement |
| rwb-document (P5) | Out | REST through the document contract | P5 | Photographs, the inspection report, the Land Office and transfer documents, the cost evidence; write-once custody (GAP-1767; ASM-2935) |
| rwb-comms (P6) | Out and in | REST or an activity; the proof of delivery listened to | P6 | The statutory notice and its proof of delivery (GAP-1767; ASM-2935) |
| rwb-integration (P2) | Out | REST or an activity per the integration contract | P2 | The SCIS vehicle registration transfer, and the HOME.SCB publication where the interface exists (GAP-1756; ASM-2924) |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | SCR-21 asset list, SCR-22 asset record, SCR-23 listing and price, SCR-24 auction rounds and PRT-06 transfer confirmation |
| Partner gateway | In | Through the edge, not by direct call | Platform edge with S9 | The auction vendor and the RAMC user (ADR-019) |
| Kafka topic `rwb.asset.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by asset | This service | AssetTakenOn (EV-22) and AssetSold; AssetSold has no EV number yet (GAP-1753; ASM-2921) |
| Kafka topics consumed | In | CloudEvents 1.0, inbox deduplicated | P8, S4, S9 | ProceedsMatched, JudgmentRecorded, AuctionResult and PartnerResultSubmitted |
| Temporal Schedule JOB-19 | In | Schedule, overlap policy SKIP, catch-up window | This service | The monthly re-appraisal scan on `rwb-asset` (Arch v5 slide 44; Temporal design slide 21) |
| rwb-reporting (P9) | Out | Events and the decision record | P9 | The NPA sales cycle (KPI-008) and the asset measures, produced from the log and not from a separate count |
| ACE common audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |
| ALS, GL, AMIS, RPS, CCMS and SVAF as direct interfaces | Removed | None | ACE team, P1, P8 | ACE ingests them and rwb-payment posts; this service holds no such interface (GAP-1750, GAP-1758, GAP-1759) |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5 (ADR-018); no extract leaves this service |
| HOME.SCB (INT-27) | Deferred | Recorded officer step | P2 with the sale officer | Not available today; the requirement keeps REQ-S5-005's wording and the step is recorded (GAP-1756; ASM-2924) |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Which path carries the asset, collateral and score facts, given that the FSD reads the views and the slide 13 matrix gives this service no P1 cell? | Solution architect with P1 | Decides the read path of every take-on, price and round (GAP-1750; ASM-2918) |
| Does the re-appraisal order go to the valuation owner or to rwb-integration, and who reads the accepted value back? | Solution architect with the S1 and P2 owners | Without an order path the monthly re-appraisal cannot be shown (GAP-1758; ASM-2926) |
| Does the vendor instruction run on the published rwb-partner contract before wave 4 delivers the panel? | Solution architect with the S9 owner | The wave 3 allocation cannot instruct a vendor without it (GAP-1757; ASM-2925) |
| Which row of the connection matrix carries the statutory notice and the document upload from this service? | Solution architect | The notice and its proof are the second fact an auditor asks for (GAP-1767; ASM-2935) |
| Is the round operation `POST /auction-rounds` or `POST /listings/{listingId}/rounds`, and what is the REST base of this service? | Solution architect | Fixes the gateway route and the screen client before the screen is built (GAP-1754; ASM-2922) |

# 10. Release slicing proposal

The service is wave 2: it is created with Epic 3 (release 31 January 2027 (tentative)). Each slice is a list of capabilities, not stories. The dates are copied from the BRD release plan and are tentative (U7, DL48) (ASM-2939).

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library, the Temporal workflow kit with the approval child, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Wave 1 — the Epic 1 slice this service epic carries (release 30 November 2026 (tentative))

| Slice | Legacy and story | What it is | Why now |
|---|---|---|---|
| 1.1 Reconciliation and data quality report, asset part | RWB-E1-011, slice RWB-S5-E1011-APP (wave 1) | The asset part of the reconciliation and data quality report of Epic 1, carried in this service epic | The wave map of Epic 1 is earlier than the service's own wave, and the earlier wave is kept (R5.6); the slice adds no product capability of this PRD and its requirement is read from the Epic 1 BRD |

Rationale: the slice is a preserved Epic 1 reporting need that the split assigns to this service epic, so it sits before the product slices and does not move the release.

## 10.3 Wave 2 — Epic 3: take-on, hold, price and list (release 31 January 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 The contract, the schema and the fake | CAP-S5-001, CAP-S5-019 | The contract is Day 1 in every service epic and has no build dependency; the boundary test must fail the build on a direct ACE read from the first story |
| 2.2 Take-on from the three sources | CAP-S5-001, CAP-S5-002 | Nothing else can be held, priced or sold until the asset is on the books once, with its notice proved |
| 2.3 Hold, provision step and stock balance | CAP-S5-003, CAP-S5-004 | The provision step and the one owned balance are the two things the business asks for first (BR-011, BR-012) |
| 2.4 Costs, work order and re-appraisal | CAP-S5-005, CAP-S5-006 | Holding cost and the re-appraisal interval decide the price, and the price is the next slice |
| 2.5 Route, price and floor | CAP-S5-007, CAP-S5-008 | The floor approval is the control the E3 release is judged on (BR-014) |
| 2.6 The listing from one action | CAP-S5-009 | The release outcome is "asset record, floor price and listing on HOME.SCB", so the listing closes wave 2 |

Rationale: the wave-2 slice is the smallest set that delivers the Epic 3 outcome, and each slice is independently demonstrable.

## 10.4 Wave 3 — Epic 4: the auction and the exits (release 28 February 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 3.1 Eviction | CAP-S5-010 | An occupied property cannot be sold, and the eviction has no legal owner today (BR-026) |
| 3.2 Rounds and the ladder | CAP-S5-011 | The loop of timed rounds is the core of the Epic 4 outcome |
| 3.3 Allocation and instruction | CAP-S5-012 | A round cannot run without a vendor, and the instruction is the contract dependency of the wave (GAP-1757; ASM-2925) |
| 3.4 Below the floor, sealed bids and the re-list | CAP-S5-013, CAP-S5-014 | The two ways an auction loses money are a below-floor sale and a ladder run past its limit (BR-028, REQ-S5-006) |
| 3.5 The payment term | CAP-S5-015 | An unpaid award is the second control on the sale (BR-028) |
| 3.6 Transfer, proceeds and the other exits | CAP-S5-016, CAP-S5-017, CAP-S5-018 | Every exit from a held asset ends in money applied or a residual decision (BR-030) |

Rationale: the wave-3 slice delivers the Epic 4 outcome and each slice is independently demonstrable; the vendor instruction is built against the published S9 contract and its fake so the wave 4 panel does not block the release.

## 10.5 Later increments

| Increment | What unlocks it |
|---|---|
| The disposal rule package as a governed package | Phase 2 of the Drools design, with the rule set, its version label and its owner in rwb-decision (GAP-1761; ASM-2929) |
| Automatic publication to HOME.SCB and the EASY app | The INT-27 interface, which the TSD records as not available today (GAP-1756; ASM-2924) |
| Allocation by the scorecard instead of by distance | The rule decision behind R-DIS-30 and the rule package (GAP-1755; ASM-2923) |
| The vendor panel, the instruction and the vendor score | FEAT-PRM-03 and the partner portal delivered in wave 4 (GAP-1757; ASM-2925) |
| The asset and round volumes as stated targets | The volume the sources do not state (GAP-1769; ASM-2937) |
| The classification and retention periods applied | DL26 and Q-012 answered (GAP-1764; ASM-2932) |
| The S5 table set in the Ownership Map and the physical schema | The data architect's table list, added with the DB story (GAP-1752; ASM-2920) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-S5-001 | FR-S5-002, FR-S5-003, FR-S5-004, NFR-S5-006 | the source-data contract is published with its fake, and one asset arrives from each of a repossession, a registered deed in lieu transfer and an LED handover | the take-on runs three times | one holding record exists per ACE asset key with its source from LOV-TRANSFER-IN, its date taken in, its book value and its provision step, linked by the business key with no foreign key; AssetTakenOn is in the outbox once per take-on | AC-S5-001-01, AC-S5-002-01, AC-S5-003-01 |
| AC-S5-002 | FR-S5-001, NFR-S5-026 | a branch that reads `recovery.v_ace_npa_asset` directly and a schema constraint that references an ACE table | the pipeline and the boundary test run | the build fails naming the view read and the cross-schema constraint; the conformance step passes with no ACE object in this schema | Arch v5 slides 37 and 45; GAP-1750; ASM-2918 |
| AC-S5-003 | FR-S5-008, FR-S5-009 | a take-on that requires the statutory notice, once with a proof of delivery and once without | the take-on runs in both cases | the first opens once the proof is recorded with its date, channel and address; the second sits in the failed notice queue with a task for the sale officer naming the address, and resumes on a confirmed address | AC-S5-004-01, AC-EXC-S5-004-01 |
| AC-S5-004 | FR-S5-010, FR-S5-011, FR-S5-012 | an asset held across a provision threshold, and a second asset whose title is unresolved | the monthly scan and the business date advance | the step, its threshold, its rule version and its date are recorded on the first; the second keeps its clock held and its route blocked until the title is clear | AC-S5-005-01 |
| AC-S5-005 | FR-S5-013, FR-S5-014 | a book of held assets, with an owner role in force and then with none | the monthly balance is published twice | the first publishes the count and the value by class and status with the owner role and the business date; the second is refused with the reason and no balance is issued | AC-S5-006-01 |
| AC-S5-006 | FR-S5-015, FR-S5-016, NFR-S5-002 | an asset with a repair, an insurance premium and a custody fee, and an inspection report in the hub | the costs are recorded and the work is accepted and then refused on a second asset | the costs are on the asset with their evidence and roll into the holding cost to date; the accepted work releases its invoice and the refused one does not | AC-S5-007-01 |
| AC-S5-007 | FR-S5-017, FR-S5-018, NFR-S5-028 | an appraisal older than the interval in force at the business date | the monthly Schedule runs | a re-appraisal order is raised through the valuation owner's contract and recorded with its date, its rule version and the interval applied, and JOB-19 is visible in the Schedule list | AC-S5-009-01; Arch v5 slide 44 (JOB-19); Temporal design slide 21 |
| AC-S5-008 | FR-S5-019, FR-S5-044, NFR-S5-006, NFR-S5-007 | one asset whose appraisal is older than a year and one whose data product is STALE | the price is requested in both cases | the first is refused with MSG-S5-002; the second shows the product with its date and MSG-P1-001 and records the business date and load time it used; neither proceeds | VR-S5-009-1, VR-S5-010-1; MSG-S5-002, MSG-P1-001; NFR-013, NFR-014 |
| AC-S5-009 | FR-S5-020, FR-S5-021, NFR-S5-003, NFR-S5-004 | the five disposal options score within a millisecond band of each other, and the pricing agent answers slowly on a second run | the route is requested twice | the recommended route carries the return on each option and the reasons; the second run uses the rule result, records the model and prompt versions and shows the fallback; each rule evaluation completes inside 300 milliseconds at the 95th percentile | AC-S5-010-01; NFR-010, NFR-011, NFR-024 |
| AC-S5-010 | FR-S5-022, NFR-S5-013 | a route inside the sale officer's limit, and a second above it | the approval is requested and granted in both cases | the first records the level applied and the approver; the second reaches the committee with the route, its return and the floor, and the committee decision is recorded; a change to the delegation table applies from its valid-from date without a release | AC-S5-010-01; DL18 open (GAP-1763; ASM-2931) |
| AC-S5-011 | FR-S5-023 | an accepted appraisal and the rules in force | the price is proposed | a start price and a floor are proposed with the value and the rule version they were derived from | AC-S5-011-01 |
| AC-S5-012 | FR-S5-024, NFR-S5-012 | a floor inside the Head of NPA's limit, and a second below it | the approval is requested in both cases | the first is approved, recorded with the level and the approver and becomes the reserve with the step schedule; the second is refused with MSG-S5-001 and nothing changes | AC-S5-011-01; VR-S5-011-1; MSG-S5-001 |
| AC-S5-013 | FR-S5-025, FR-S5-026 | an asset with photographs, an inspection report and a clear title | the listing is published from one action | the listing is recorded with its channel, prices, rounds and schedule, the auction channel is instructed, the floor is absent from the publication, and the bank channel step is recorded with its date and reference | AC-S5-012-01; GAP-1756; ASM-2924 |
| AC-S5-014 | FR-S5-025 | an asset with no inspection report | the listing is published | the publication is refused with the missing evidence named and nothing is published | VR-S5-015-1; AC-EXC-S5-012-01 |
| AC-S5-015 | FR-S5-027 | a held property with occupants who refuse possession | the eviction is opened | the eviction is recorded with Legal named and its documents, and the asset returns to hold and resumes its route when the property is vacant | AC-S5-008-01 |
| AC-S5-016 | FR-S5-028 | a listing at its start price with a floor and a schedule | the first round runs and closes with no bid | the round is recorded with its number, its price, its opening and closing times and its outcome, and the next round opens at the price the ladder sets, above the floor | AC-S5-013-01 |
| AC-S5-017 | FR-S5-030, FR-S5-031, NFR-S5-029 | four panel vendors, one suspended and one at capacity, and the allocation rule in force | the asset is allocated and instructed | one vendor is allocated with the rule version and the reason, the suspended and full vendors are passed over, and the instruction is recorded with its result; a rejected instruction is retried and then moved to the exception queue | AC-S5-014-01, AC-EXC-S5-014-02; GAP-1757; ASM-2925 |
| AC-S5-018 | FR-S5-029 | an open round | the vendor reports two bids, one above and one below the floor | both are recorded against the round and the asset with their amounts, bidder references and times, and the one above the floor clears the round | AC-S5-015-01 |
| AC-S5-019 | FR-S5-032 | a bid below the floor | the sale is attempted without a second signature and then with one | the first is held and nothing is agreed; the second is agreed with the signature, its role and the reason recorded | AC-S5-016-01 |
| AC-S5-020 | FR-S5-033 | a sale at or above the amount in force for sealed bids | the award is attempted before the committee has decided | the award is held, the bids and the floor go to the committee, and the decision is recorded with the level applied | AC-S5-016-01; Temporal design slide 21 (R-DIS-22) |
| AC-S5-021 | FR-S5-034 | a round that closes with no bid, once below the re-list limit and once at it | the round closes in both cases | the first re-lists at the next price step with the re-list count recorded; at the limit the outcome is recorded and the case is raised to the next decision | AC-S5-017-01 |
| AC-S5-022 | FR-S5-035, FR-S5-036 | an award with the five-day term, and a second award whose payment never arrives | the term expires in both cases | the first records the bidder, the amount and the due date; the second cancels the award, releases the asset, reopens the round and records the reason, and records the vendor's score effect where the vendor is at fault | AC-S5-018-01; RULE-008 |
| AC-S5-023 | FR-S5-037 | a vehicle sale and a property sale | the transfers are prepared | the vehicle transfer is submitted through the integration contract with its reference and its 10-working-day clock, and the property transfer is recorded with its date, its reference and its documents | AC-S5-019-01, AC-S5-020-01 |
| AC-S5-024 | FR-S5-038, FR-S5-039, NFR-S5-011 | a sale agreed at a price, with fees and taxes, and a residual above zero | the sale is completed | the sale is recorded with its dates, price, fee, taxes and gain or loss; the proceeds are handed to rwb-payment; ProceedsMatched is applied; the residual is raised for the next decision; AssetSold is in the outbox in the same transaction | AC-S5-021-01; GAP-1753; ASM-2921; GAP-1759; ASM-2927 |
| AC-S5-025 | FR-S5-040, FR-S5-041, FR-S5-042, FR-S5-043 | a pool of assets for the asset management company, a buy-back, a rental and a broker sale | each exit is opened | each carries its approval at the level in force, the transfer price from the template version where a pool moves, the second signature where the rule requires it, and its terms and outcome recorded | AC-S5-022-01, AC-S5-023-01, AC-S5-024-01, AC-S5-025-01 |
| AC-S5-026 | FR-S5-005, NFR-S5-024 | a user without the capability area and a partner user scoped to another asset | they try to take on, price, list, record a round and accept a bid | every action is refused with MSG-P4-002, the partner sees only their own assets, and nothing changes | AC-EXC-S5-001-01 to AC-EXC-S5-025-01; MSG-P4-002; NFR-050 |
| AC-S5-027 | FR-S5-006, NFR-S5-014 | the decision record store rejects every write | a take-on, a price and an award are attempted | nothing changes on the asset, MSG-P7-003 is shown and an incident is raised; the daily hash-chain check reports the gap the same day | AC-EXC-S5-001-02 to AC-EXC-S5-025-02; MSG-P7-003; NFR-035 |
| AC-S5-028 | FR-S5-007, NFR-S5-012 | the provision thresholds, the floor limits and the re-list limit in force | each one is changed in reference data and the decision is re-run | the answer changes from the valid-from date without a code release, and the decision records the version applied | AC-S5-005-01, AC-S5-011-01; RULE-001 |
| AC-S5-029 | FR-S5-020, FR-S5-021, NFR-S5-016, NFR-S5-017 | a route proposed by the rule set and one proposed with an agent answer | an auditor reads both records and the model risk officer reads the agent measures | each record shows the options, the returns, the route, the reasons, the rule version and the actor; the agent measures show acceptance, override, latency and cost, and the run where the rule result was used | AC-S5-010-01; NFR-033, NFR-066, NFR-078 |
| AC-S5-030 | FR-S5-013, FR-S5-015, NFR-S5-018, NFR-S5-019, NFR-S5-020, NFR-S5-022 | the asset, listing and sale records with a bidder reference and a party reference | the screens and the agent call are read across roles, and the access log is compared with the reads | the bidder and party references are masked by role, each screen and the agent receive only what they need, every read of a personal field is in the log, and every record carries its classification | AC-S5-006-01; NFR-039, NFR-040, NFR-042, NFR-047 |
| AC-S5-031 | FR-S5-025, FR-S5-034, NFR-S5-028, NFR-S5-029 | a running AssetDisposalWorkflow, a failed vendor instruction and an event that cannot be processed | the failures are injected | the workflow reports its breach, the instruction is retried and then queued with a task for a named owner, the event goes to the dead-letter topic and is replayed, and each raises its alert within 15 minutes | AC-EXC-S5-013-02; NFR-025, NFR-026, NFR-068 |
| AC-S5-032 | FR-S5-011, FR-S5-038, NFR-S5-023, NFR-S5-030 | a production release with a migration in `rwb_asset` | the release is rolled back | the previous tag is redeployed, the migration stays in `rwb_asset`, and no recovery data has left the bank's tenancy | NFR-027, NFR-046 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| BR-010 (REQ-S5-001) | CAP-S5-001, CAP-S5-002, CAP-S5-019 | FR-S5-001, FR-S5-002, FR-S5-003, FR-S5-004, FR-S5-005, FR-S5-006, FR-S5-008, FR-S5-009, FR-S5-044 | NFR-S5-002, NFR-S5-005, NFR-S5-006, NFR-S5-007, NFR-S5-008, NFR-S5-009, NFR-S5-010, NFR-S5-015, NFR-S5-018, NFR-S5-019, NFR-S5-020, NFR-S5-021, NFR-S5-022, NFR-S5-023, NFR-S5-024, NFR-S5-025, NFR-S5-027, NFR-S5-028, NFR-S5-029, NFR-S5-030 | AC-S5-001, AC-S5-002, AC-S5-003, AC-S5-005, AC-S5-006, AC-S5-026, AC-S5-027, AC-S5-030, AC-S5-031, AC-S5-032 |
| BR-011 (REQ-S5-003) | CAP-S5-003, CAP-S5-006 | FR-S5-007, FR-S5-010, FR-S5-011, FR-S5-012, FR-S5-017, FR-S5-018 | NFR-S5-005, NFR-S5-028 | AC-S5-004, AC-S5-007, AC-S5-028 |
| BR-012 (REQ-S5-002) | CAP-S5-004 | FR-S5-013, FR-S5-014 | NFR-S5-001, NFR-S5-031 | AC-S5-005, AC-S5-030 |
| BR-013 (REQ-S5-001) | CAP-S5-005 | FR-S5-015, FR-S5-016 | NFR-S5-002 | AC-S5-006, AC-S5-030 |
| BR-014 (REQ-S5-004, REQ-S5-005) | CAP-S5-007, CAP-S5-008, CAP-S5-009, CAP-S5-019 | FR-S5-007, FR-S5-019, FR-S5-020, FR-S5-021, FR-S5-022, FR-S5-023, FR-S5-024, FR-S5-025, FR-S5-026, FR-S5-044 | NFR-S5-003, NFR-S5-004, NFR-S5-006, NFR-S5-012, NFR-S5-013, NFR-S5-016, NFR-S5-026 | AC-S5-008, AC-S5-009, AC-S5-010, AC-S5-011, AC-S5-012, AC-S5-013, AC-S5-014, AC-S5-029 |
| BR-026 | CAP-S5-010 | FR-S5-027 | None of its own; the shared performance, security and audit targets of section 7 apply | AC-S5-015 |
| BR-027 (REQ-S5-006) | CAP-S5-011, CAP-S5-012, CAP-S5-014 | FR-S5-028, FR-S5-029, FR-S5-030, FR-S5-031, FR-S5-034 | NFR-S5-003, NFR-S5-029 | AC-S5-016, AC-S5-017, AC-S5-018, AC-S5-021, AC-S5-031 |
| BR-028 (REQ-S5-007) | CAP-S5-013, CAP-S5-015 | FR-S5-032, FR-S5-033, FR-S5-035, FR-S5-036 | NFR-S5-012, NFR-S5-013 | AC-S5-019, AC-S5-020, AC-S5-022 |
| BR-029 (REQ-S5-008) | CAP-S5-016 | FR-S5-037 | NFR-S5-029 | AC-S5-023 |
| BR-030 (REQ-S5-009, REQ-S5-010) | CAP-S5-017, CAP-S5-018 | FR-S5-006, FR-S5-038, FR-S5-039, FR-S5-040, FR-S5-041, FR-S5-042, FR-S5-043 | NFR-S5-011, NFR-S5-014, NFR-S5-017 | AC-S5-024, AC-S5-025, AC-S5-027, AC-S5-029 |

BR coverage: 10 of the 10 BRD requirements that name this service (BR-010 to BR-014 and BR-026 to BR-030) are covered by at least one functional requirement, and the 10 program requirements REQ-S5-001 to REQ-S5-010 that sit under them are covered in the same rows. No requirement of this module is left without a functional requirement, and no functional requirement lacks a source requirement (ASM-2941). BR-015 (agent autonomy), BR-016 to BR-025 and BR-031 to BR-033 name other services and are not this product's requirement.

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Boundary and conformance test output in system test | FR-S5-001, FR-S5-002, NFR-S5-026 | Developer with the security administrator |
| Contract test against the source-data contract and its fake | FR-S5-001 to FR-S5-003, FR-S5-017, FR-S5-044 | Developer with P1 |
| Take-on drill from the three sources, with the notice proved and unproved | FR-S5-003, FR-S5-004, FR-S5-008, FR-S5-009 | QA team with the sale officer |
| Provision step, title block and clock drill over a month of business dates | FR-S5-010, FR-S5-011, FR-S5-012 | NPA and asset manager with the QA team |
| Monthly balance and owner role test, with and without an owner in force | FR-S5-013, FR-S5-014 | Head of NPA with the QA team |
| Cost, work order and invoice release test | FR-S5-015, FR-S5-016 | NPA and asset manager with the finance user |
| Re-appraisal order and stale-appraisal refusal drill | FR-S5-017, FR-S5-018, FR-S5-019 | QA team with the S1 owner |
| Recommendation test with an agent timeout and a failed schema check | FR-S5-020, FR-S5-021 | QA team with the model risk officer |
| Floor approval matrix across the delegation levels and the committee path | FR-S5-022, FR-S5-024, NFR-S5-013 | Head of NPA with the QA team |
| Listing publication test, including the withheld floor and the recorded manual step | FR-S5-025, FR-S5-026 | Sale officer with the QA team |
| Round, allocation and instruction drill against the S9 fake | FR-S5-028 to FR-S5-031 | QA team with the S9 owner |
| Below-floor signature, sealed-bid sale, re-list limit and payment-term drill | FR-S5-032 to FR-S5-036 | Sale officer with the QA team |
| Transfer, sale, proceeds and residual test with the payment fake | FR-S5-037, FR-S5-038, FR-S5-039 | Credit Administration officer with the QA team |
| Exit approvals test for the pool, the buy-back, the rental and the broker | FR-S5-040 to FR-S5-043 | Head of NPA with the Head of Asset Liquidity |
| Decision reproducibility and measure review | FR-S5-006, NFR-S5-011, NFR-S5-016 | Internal audit with the model risk officer |
| Masking matrix, access log reconciliation and classification review | NFR-S5-018 to NFR-S5-022 | Compliance and PDPA officer |
| Performance and volume test at the stated volume, rerun when the asset volume is given | NFR-S5-001, NFR-S5-002, NFR-S5-003, NFR-S5-005 | QA team |
| Accessibility, browser and partner device test | NFR-S5-031 | QA team with the Partner and agency manager |

# 12. Open questions

The BRD's and the FSD's open items are carried forward with their IDs where they have one. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-S5-01 | Does this service read the NPA asset, asset, collateral and score facts through the source-data contract, and who confirms the contract fields, the business key and the freshness response? | Solution architect with P1 | Before wave 2 system test | CAP-S5-001, CAP-S5-007, CAP-S5-008, CAP-S5-019 | GAP-1750; ASM-2918; Arch v5 slides 37 and 45 |
| OQ-S5-02 | Is the asset a table of this service in schema `rwb_asset`, or an extension of the ACE asset owned by ACE? | Data architect with the ACE team | Before the S5 DB story | CAP-S5-001, CAP-S5-003 | GAP-1751; ASM-2919 |
| OQ-S5-03 | Which tables hold the asset, the listing, the sale, the auction round with its bids and the holding cost movement in schema `rwb_asset`, given that the Ownership Map lists two of the five? | Data architect | Before the S5 DB story | CAP-S5-001, CAP-S5-011, CAP-S5-018 | GAP-1752; ASM-2920 |
| OQ-S5-04 | Does AssetSold get an EV number and a catalogue row, and which service consumes it besides rwb-payment and rwb-case? | Solution architect | Before wave 3 system test | CAP-S5-017 | GAP-1753; ASM-2921 |
| OQ-S5-05 | Is the round operation `POST /auction-rounds` or `POST /listings/{listingId}/rounds`, and is the base `/api/recovery/asset/v1`? | Solution architect | Before the S5 contract story closes | CAP-S5-009, CAP-S5-011 | GAP-1754; ASM-2922 |
| OQ-S5-06 | Is a vendor allocated by distance and capacity or by the scorecard (BR-027 and FEAT-AST-14 against R-DIS-30)? | Business analyst, S5 with the center of excellence analyst | Before wave 3 release | CAP-S5-012 | GAP-1755; ASM-2923 |
| OQ-S5-07 | Is the HOME.SCB publication automated at Epic 3, and who owns the interface when it exists? | Solution architect with the integration lead | Before wave 2 system test | CAP-S5-009 | GAP-1756; ASM-2924; BRD Q-019 |
| OQ-S5-08 | Does the partner instruction capability land in E4 or in E6, and does the wave 3 allocation run on the published contract and its fake until wave 4? | Solution architect with the S9 owner | Before wave 3 release | CAP-S5-012 | GAP-1757; ASM-2925; BRD Q-019 |
| OQ-S5-09 | Which path carries the re-appraisal order, and does this service read the accepted appraisal through rwb-valuation or through rwb-source-data? | Solution architect with the S1 owner | Before wave 2 system test | CAP-S5-006, CAP-S5-008 | GAP-1758; ASM-2926; ASM-0043 |
| OQ-S5-10 | Who posts the proceeds, the fees and the cost of carry: this service or rwb-payment, and what does ProceedsMatched carry back? | Solution architect with the P8 owner | Before wave 3 system test | CAP-S5-017 | GAP-1759; ASM-2927 |
| OQ-S5-11 | Is a pricing agent part of this product at all, and if it is, which service runs it and under which autonomy level? | Solution architect with the model risk officer | Before wave 2 system test | CAP-S5-007, CAP-S5-008 | GAP-1760; ASM-2928; DP-20 |
| OQ-S5-12 | Which rule package does the disposal decision evaluate, what is its code, and when do the remaining rules and the 40 states arrive? | Center of excellence analyst with P7 | Before wave 2 release | CAP-S5-003 to CAP-S5-018 | GAP-1761; ASM-2929; DP-04 |
| OQ-S5-13 | Which role owns the non performing asset stock balance (Q-009)? | Head of NPA | Before wave 2 release | CAP-S5-004 | GAP-1762; ASM-2930; BRD Q-009 |
| OQ-S5-14 | What is each floor and sale approval level and limit by decision, product and amount, and who substitutes (DL18, Q-001)? | Risk with the product heads | Before wave 2 release | CAP-S5-008, CAP-S5-013 | GAP-1763; ASM-2931; DL18; BRD Q-001 |
| OQ-S5-15 | What classification and what retention period apply to the asset, listing, round and sale records (DL26, Q-012)? | Compliance and PDPA officer | Before wave 2 release | CAP-S5-001, CAP-S5-017 | GAP-1764; ASM-2932; DL26; BRD Q-012 |
| OQ-S5-16 | What is the floor price basis by product, and does the basis change the floor test (Q-002)? | Product head (Mortgage, HP, SSME) | Before wave 2 release | CAP-S5-008 | BRD Q-002; VR-S5-011-1 |
| OQ-S5-17 | What are the provision step thresholds and the re-appraisal interval for a held asset (Q-005)? | NPA and asset manager | Before wave 2 release | CAP-S5-003, CAP-S5-006 | BRD Q-005; BR-011 |
| OQ-S5-18 | Which row of the connection matrix carries the statutory notice and the document upload, and does the proof of delivery arrive as an event? | Solution architect with the P5 and P6 owners | Before wave 2 system test | CAP-S5-002, CAP-S5-005, CAP-S5-016 | GAP-1767; ASM-2935 |
| OQ-S5-19 | Who owns the wording of the six messages this module shows, and who approves the Thai and English versions (DL10)? | Business analyst, S5 with the business lead | Before wave 2 release | All messages | GAP-1768; ASM-2936; DL10 |
| OQ-S5-20 | What are the asset population, the round volume and the holding cost volume the sizing must carry? | Solution architect with the data product owner | Before wave 2 release | NFR-S5-005 | GAP-1769; ASM-2937; NFR-001 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (GAP-1765; ASM-2933).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 2 (business outcomes), 5.12 (S5 requirements, REQ-S5-001 to REQ-S5-010), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan: E1 30 November 2026, E3 31 January 2027, E4 28 February 2027, all tentative), 9 (open decisions incl. DL10, DL18, DL26, DL43), 10.1 to 10.6 (the service epic RWB-SVC-S5, schema, wave 2, contract-first delivery, ownership of the shared items) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 5 (stakeholders and user groups), 7.1 and 7.3 (E3 and E4 scope, services and waves), 8.1 and 8.2 (BR-010 to BR-014 and BR-026 to BR-030), 9 (RULE-001 to RULE-032), 10 (KPI-008 and KPI-011), 11.1 to 11.4 (assumptions, constraints, dependencies, risks), 12 (Q-001, Q-002, Q-005, Q-008, Q-009, Q-012, Q-016, Q-019), 13 (governance), 14 (traceability) |
| Recovery Workbench FSD S5 Assets and auction v3 | Document control, Existing capability check, A1 (context, scope, dependencies, feature overview FEAT-AST-01 to FEAT-AST-25), A2.1 to A2.25 (functional decomposition with field catalog, rules R-DIS-01 to R-DIS-71, validation rules VR-S5-001-1 to VR-S5-025-1, roles and acceptance criteria), Requirements served, Screens (SCR-21 to SCR-24, PRT-06), Appendix A and B |
| Recovery Workbench TSD S5 Assets and auction v2 | T3.1 to T3.3 (DF-COL-028 to DF-COL-042, DF-SAL-001 to DF-SAL-019, LOV-ASSET-TYPE, LOV-HOLDING, LOV-LISTING, LOV-SALE-CHANNEL, LOV-SEGMENT, LOV-TRANSFER-IN, relationships), T4 (DISPOSAL, 72 rules over 40 states), T5 (INT-11, INT-12, INT-13, INT-27), T5.3 (events), T6 (RBAC matrix), T7 (NFR-049 to NFR-056), T8, Appendix T-A (API-S5-001 to API-S5-005), Appendix T-B (DL06, DL11, DL35) |
| Recovery Workbench Architecture v5 | Slides 3 to 4 (the recovery map and the 19 modules), 9 to 13 (call types, timeouts, retry, the connection matrix), 14 to 20 (service contracts, incl. S5 rwb-asset), 27 (rule governance), 30 (19 schemas), 32 (bank scheduler at the edges), 37 (what changes and why), 38 (waves), 41 (service catalogue), 42 and 43 (event catalogue, EV-22 and the '+' rows), 44 (job map, JOB-19), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Slide 13 (one child workflow per stage), 15 (rule governance and versioning), 21 (S5 disposal: the seven steps, the 72-rule set, the approval ladder, the two clocks, the re-list and the below-floor rules), slide 33 note 3 (the Phase 2 package codes) |
| Recovery Workbench Microservice Ownership Map v1 | Services (S5 row), Endpoints (GET /assets, GET /assets/{assetKey}, POST /assets/{assetKey}/listings, POST /listings/{listingId}/rounds, and the two superseded assetId paths), Workflows (AssetDisposalWorkflow), Events (EV-22), Jobs (JOB-19), Tables (asset_sale, listing) and Rulings |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic), 4 (partner access) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R5 (target structure, DP table, wave map, lanes), R8 (outputs, header, versioning), R9 (gaps and assumptions) |
| _work/msr/plan/split_plan.json and _work/msr/plan/ownership.json | Slice waves and release dates for RWB-S5-E1011-APP, RWB-S5-E3019 to RWB-S5-E3029 and RWB-S5-E4021 to RWB-S5-E4034; the owner of every operation, event, job, workflow and table named here |
