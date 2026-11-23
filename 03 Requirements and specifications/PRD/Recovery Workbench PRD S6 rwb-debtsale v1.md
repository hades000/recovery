SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD S6 rwb-debtsale v1
description: Product requirements for the Recovery Workbench debt sale service (S6 rwb-debtsale) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slicing by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S6 Debt sale v3.md
service: S6 rwb-debtsale
epic: RWB-SVC-S6
wave: 3
decision: D-RCV-60
---

# Recovery Workbench PRD S6 rwb-debtsale v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD S6 rwb-debtsale |
| Document ID | S6-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | S6 rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 3 (service created in wave 3; lot building releases in EP05, award and transfer in EP06) |
| Business epic | EP05 (Epic 5, litigation and debt sale preparation, wave 3) and EP06 (Epic 6, debt sale and write-off, wave 4) |
| Schema | `rwb_debtsale` |
| REST base | `/api/recovery/debtsale/v1` |
| Topic | `rwb.debtsale.events.v1` |
| Temporal task queue | `rwb-debtsale` |
| Java package | `th.co.scb.ace.workbench.recovery.debtsale` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Business analyst, S6 |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), ADR-010, ADR-013 to ADR-023 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epics 3 to 8 v1; FSD S6 Debt sale v3; Architecture v5; Temporal and Drools Design v1; Microservice Ownership Map v1; Physical Schema v6; Logical Data Model and Data Dictionary v8; Business Rules and Routing Logic v4; Non Functional Specification v3 |
| Upstream requirement IDs | REQ-S6-001 to REQ-S6-009; BR-044, BR-045, BR-046, BR-047, BR-048, BR-049, BR-050; RULE-015, RULE-016, RULE-017, RULE-018; R-DS-01 to R-DS-41; NFR-001, NFR-003, NFR-007, NFR-008, NFR-009, NFR-010, NFR-011, NFR-013, NFR-014, NFR-015, NFR-020, NFR-021, NFR-022, NFR-023, NFR-024, NFR-025, NFR-026, NFR-027, NFR-028, NFR-031, NFR-033, NFR-034, NFR-035, NFR-039, NFR-040, NFR-041, NFR-042, NFR-045, NFR-046, NFR-047, NFR-049, NFR-050, NFR-051, NFR-052, NFR-053, NFR-054, NFR-055, NFR-058, NFR-059, NFR-060, NFR-061, NFR-063, NFR-064, NFR-065, NFR-067, NFR-068 |
| Upstream acceptance criteria | AC-S6-001-01 to AC-S6-016-01 (main success flow, one per feature); AC-EXC-S6-001-01 to AC-EXC-S6-016-01 (role without the right); AC-EXC-S6-001-02 to AC-EXC-S6-016-02 (decision cannot be recorded). The FSD defines no alternate flow and no system background event for any of the sixteen features |
| Generated IDs | CAP-S6-001 to CAP-S6-017; FR-S6-001 to FR-S6-033; NFR-S6-001 to NFR-S6-031; AC-S6-001 to AC-S6-022; JRN-S6-01 to JRN-S6-05; ROL-S6-01 to ROL-S6-13; OQ-S6-01 to OQ-S6-16 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD S6 Debt sale v3 (15 November 2026) and Business Requirements Epics 3 to 8 v1, realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD S6 Debt sale v3. Its requirement IDs, feature IDs, rule IDs and acceptance criterion IDs are carried unchanged; the microservice realignment changes the read path, the owner of the tape masking capability, the workflow shape and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. COLLINS lot economics read from `v_ace_score`. Everything else unchanged from v2 |
| 1 and 2 | Not specified in the source documents (GAP-1770; ASM-2963) | Earlier versions of the FSD. Their dates and change notes are not in the sources read and are carried as an open item rather than reconstructed |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, journey and open-question IDs are new; the FSD requirement IDs (REQ-S6-001 to REQ-S6-009), feature IDs (FEAT-DBS-01 to FEAT-DBS-16), validation rule IDs (VR-S6-001-1 to VR-S6-016-1), business rule IDs (BR-S6-001 to BR-S6-016), routing rule IDs (R-DS-01 to R-DS-41), acceptance criteria IDs (AC-S6-001-01 to AC-S6-016-01 and their exception rows), message IDs (MSG-S6-001, MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001), list IDs (LOV-SEGMENT, LOV-BUYER-CLASS), screen IDs (SCR-25, SCR-26) and partner screen ID (PRT-05) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the program requirements REQ-S6-001 to REQ-S6-009 and of the non-functional requirements; 5.13 is the debt sale section, 10.2 and 10.3 fix the service epic and the wave |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-044 (E5) and BR-045 to BR-050 (E6), of RULE-015 to RULE-018, of KPI-005 and KPI-006, of RISK-005 and of Q-001, Q-010, Q-011, Q-012 |
| Recovery Workbench Functional Specifications by Module v6, FSD S6 Debt sale v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, only rwb-source-data reads ACE, Kafka, Temporal, no data lake, edge and gateway, the saga with the transfer as pivot |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: DebtSaleWorkflow as a saga on `rwb-debtsale`, the seven steps and the pivot, the 41-rule debt sale route set, the approval by authority, the clocks, the kit's agent run with rule fallback |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every operation, event, workflow, table and job named here |
| Recovery Workbench Physical Schema v6 and Logical Data Model and Data Dictionary v8 | Data | Source of the table and field names, the field IDs DF-SAL-020 to DF-SAL-037, the LOVs and the personal-data flags |
| Recovery Workbench Business Rules and Routing Logic v4 | Rules | Source of R-DS-01 to R-DS-41 and of the state ladder the features move through |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-debtsale (S6) is the recovery module's debt sale. It turns "a sale run on spreadsheets with no baseline turnaround" into a product: a sale population selected by rule inside the policy cap with every exclusion named; lots built with an estimated price from the COLLINS lot economics and with tiered buyer terms and a reserve price; a reserve and a set of terms approved by the committee that owns them; a data tape masked under PDPA before it reaches a data room; a data room that opens only to a buyer who has signed the agreement and passed the KYC, licensing and eligibility check, and that closes the door again on a buyer that fails; a bid recorded on the lot, not in an email; an award tested against the reserve and the cap and approved by the authority the limit names; the agreement and the customer notices generated from templates; a transfer file per lot delivered encrypted to the buyer; a derecognition and a general ledger posting that follow the award without re-keying; a put-back claim decided against the sale terms with a reason; and a case that stops every open action the same day its account is sold in a lot.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-debtsale | One deployable with its own API and worker, schema `rwb_debtsale`, login, topic `rwb.debtsale.events.v1`, task queue `rwb-debtsale` and lifecycle | Debt sale becomes one owned product with its own release, instead of a set of spreadsheet runs and screens inside a single deployable |
| The lot as a governed record | Lot number, cut-off date, segment, reserve price, buyer and buyer class, signing date, approval authority, payment terms and status, held once and linked to the accounts by business key | A sale population and a price that cannot be reconciled to the book is the defect the program exists to remove |
| The masked tape as a controlled artefact | The tape is built under the PDPA masking rules, checked before it leaves, and rejected and rebuilt when an unmasked identifier is found | Personal data leaving the bank unmasked is the highest-impact risk of this module (RISK-005) |
| The data room as product behaviour | The room opens only to a buyer with the agreement signed and the checks passed, and a buyer that fails is barred with a reason and the lot released | An unqualified buyer must not hold a bank's debt book |
| The award as a tested decision | The bid is tested against the reserve and the 54 percent cap, and the award carries the approval its limit names, the price achieved and the authority applied | The award price is the last control on the sale |
| The sale as one saga | DebtSaleWorkflow runs the seven steps across five services with the transfer as the pivot: the steps before it can be undone, the steps after it are retried until they succeed | The sale is only complete when the book and the money agree |
| The sale as an event | LotAwarded and AccountsTransferred on `rwb.debtsale.events.v1`, consumed by rwb-case and rwb-payment, and by rwb-reporting for the ledger of what was sold | A sold case that keeps working creates work against a book the bank no longer owns |
| The cap as a reported position | The sale population is held inside the policy cap and the headroom is written where the business reads it | The cap is a regulatory and board limit, not a target (BR-050) |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its ingestion of COLLINS scores and its backups | REUSE | ACE team |
| The read-only view contract and the freshness of every data product | REUSE, elsewhere | P1 rwb-source-data (this service reads it by contract) |
| Case record, CMMN state, stage ladder, queues, tasks, allocation and the case timers | REUSE | P3 rwb-case (the case side of a sale is moved by rwb-case on the event) |
| Approval workflow, delegation lookup, decision record, hash chain and rule package registry | REUSE | P7 rwb-decision |
| Roles, capability areas, masking policy, delegation of authority table and access log | REUSE | P4 rwb-access |
| Party identifiers, contact points and the PII logging path | REUSE | ACE common, through P4's masking policy |
| Document metadata, the data room pack, custody and retention | REUSE | P5 rwb-document |
| Notice templates, merge fields and proof of delivery | REUSE | P6 rwb-comms |
| Payment and proceeds matching, fees, bookings and posting files | REUSE | P8 rwb-payment |
| Buyer panel, partner users, instructions, results and fees | REUSE, elsewhere | S9 rwb-partner |
| The buyer file transfer over MFT and the delivery record | REUSE, elsewhere | P2 rwb-integration (INT-25) |
| Measures, the sale ledger and regulatory extracts | REUSE, elsewhere | P9 rwb-reporting, read from events and the decision record |
| Agent runtime, prompt versions, guardrails and run record | REUSE, elsewhere | P10 rwb-agent (where the lot estimate uses an agent) |
| Screens and the composite route that serves them | REUSE | Platform edge, gateway-bff for staff; the partner gateway in the DMZ for buyers |
| Quartz scheduler and its shared tables | REPLACED | Temporal Schedules and durable timers through the workflow kit (PLT); ADR-016, DP-10 |
| Embedded Drools with the debt sale decision tables evaluated in the monolith | MOVED | Governance and versioning in P7; evaluation stays local in this service (ADR-017, DP-04) |
| Masks and edits applied by hand to a spreadsheet tape | REPLACED | The tape is built under the masking policy read from P4 and checked before release (GAP-1783; ASM-2955) |
| Direct derecognition and ledger posting from the module | MOVED | P8 rwb-payment posts; this service records the result (GAP-1779; ASM-2951) |
| The data lake copy and Power BI (INT-19, INT-20) | REMOVED | rwb-reporting read model from events (ADR-018, DP-17) |
| COLLINS model development and the affordability calculation | OUT OF SCOPE | Data and AI; the ACE restructure calculator |
| Booking in the core bank (ALS) and credit approval in the lending system | OUT OF SCOPE | The officer and the core bank; this service records the result |
| Collections before day 90 and decisions D1 to D4 | OUT OF SCOPE | EFS and the ACE collection module |
| Buyer KYC and licensing as an internal process of the bank | OUT OF SCOPE | The bank's existing KYC and licensing checks, read as data (GAP-1776; ASM-2948) |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014; slides 37 and 45).
2. The service writes only schema `rwb_debtsale`; no cross-schema join and no foreign key into another schema or into `public` (ADR-014, DP-01).
3. The slide 13 connection matrix gives the S6 row no cell to rwb-source-data: the reads this module needs (COLLINS lot economics, account balances at cut-off, freshness) therefore have no confirmed path and are carried as the first open question (GAP-1770; ASM-2942).
4. The calls the matrix does fix for S6: Temporal to rwb-decision (the approval child), Temporal to rwb-document (the data room pack), Temporal and events to rwb-payment (postProceeds and ProceedsMatched), Temporal to rwb-integration (deliverFile), and events from rwb-case (slide 13; slide 19).
5. REST is one hop from the gateway with a 2 s timeout, an Idempotency-Key on every POST and RFC 9457 problem details; a GET is retried once with jitter (ADR-020; slides 10 and 11).
6. Events are CloudEvents 1.0 on Kafka with an outbox and an inbox, retry at 1 minute, 10 minutes and 1 hour and then a dead-letter topic; topic `rwb.debtsale.events.v1`, key `caseId` (ADR-015, DP-09, DP-14; slides 9 and 11).
7. Temporal namespace `rwb-recovery`, task queue `rwb-debtsale`; DebtSaleWorkflow is a stage workflow of the case model and a saga with the transfer as the pivot; the steps after the pivot wait for the central ledger to confirm the decision record in strict mode (ADR-016; slides 25 and 26).
8. Rules are versioned data evaluated in process by the embedded Drools kit; the debt sale route set is 41 rules and its package is Phase 2 governance (ADR-017, DP-04; design slide 22).
9. There is no data lake: sale measures, the sale ledger and the cap headroom read the events and the decision record into rwb-reporting (ADR-018, DP-17).
10. Personal data stays out of events, workflow inputs and logs; masking is by role using the permission data cached from rwb-access, and each service authorises the object itself (slide 10; NFR-039, NFR-040, NFR-041).
11. Buyers reach the platform through the partner gateway in the DMZ, staff through gateway-bff, and the buyer file leaves over MFT (ADR-019, INT-25; slides 32 and 41).
12. The bank scheduler owns only the cross-system edges and signals the business date; it never enters the sale cycle (slide 32).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-S6-01 | Debt sale officer | A sale population selected by rule, a lot to build, a reserve to propose, a tape to check and the award to run inside the approval taken | JRN-S6-01, JRN-S6-02, JRN-S6-03 |
| ROL-S6-02 | Head of Asset Liquidity | The lots, the reserve and the tiered terms in front of the committee, the award approved on the limit, and the cap position visible | JRN-S6-02, JRN-S6-03 |
| ROL-S6-03 | Credit approval committee member | A pack that states the lot, the price achieved against the reserve, the cap applied and the reasons | JRN-S6-02, JRN-S6-03 |
| ROL-S6-04 | Debt buyer and AMC (external role) | The data room for a lot, its masked tape, the terms and a bid submitted inside the window | JRN-S6-02 |
| ROL-S6-05 | Credit Administration officer | The posting and the derecognition result, and a rejection that can be corrected and re-posted | JRN-S6-04 |
| ROL-S6-06 | Case owner | Their case out of the population with a reason, and a case closed the same day its account is sold in a lot | JRN-S6-01, JRN-S6-05 |
| ROL-S6-07 | Compliance and PDPA officer | A tape masked before it leaves, an access log per read, a classification on every record and a bar decision with its evidence | JRN-S6-03, JRN-S6-05 |
| ROL-S6-08 | Partner and agency manager | The buyer panel and the panel status that the qualification check reads | JRN-S6-03 |
| ROL-S6-09 | Internal audit | One sale that can be reconstructed: the population, the exclusions, the price, the approval, the tape check and the transfer | JRN-S6-05 |
| ROL-S6-10 | Center of excellence analyst | The cap, the windows and the criteria as versioned data, and every sale with the rule version applied | JRN-S6-05 |
| ROL-S6-11 | Platform administrator | A workflow that reports a breach, an alert with a named owner and a replay path | JRN-S6-04 |
| ROL-S6-12 | Developer | A typed contract to build against, a fake for every dependency, and a build that fails on a direct ACE read | JRN-S6-05 |
| ROL-S6-13 | Finance and CFO delegate | The provision input of the sold population, from the posted population and not from a separate count | JRN-S6-04 |

Non-human actors: the case workflow that starts DebtSaleWorkflow for the sale stage; the ApprovalWorkflow on rwb-decision; the document hub that holds the data room pack; the partner gateway that admits a buyer; the outbox relay; the consumers of LotAwarded and AccountsTransferred; rwb-payment, which owns the posting. Where the lot estimate uses an agent it is reached through rwb-agent and never by a direct call from a screen.

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. The sale population, the lot, the reserve and the buyer terms live in a spreadsheet, and the eligibility rules are applied by whoever builds the sheet.
2. The tape is masked by hand, and a mask missed by hand is a mask nobody sees until the file has left the bank.
3. The data room is a folder and a set of emails; whether a buyer has signed the agreement or holds a licence is checked from memory and from a mailbox.
4. The bid arrives in an email, and the price achieved against the reserve is written up after the fact.
5. The transfer, the derecognition and the ledger posting are re-keyed in the systems that own them, and the case around a sold account keeps working until somebody notices.
6. The put-back claim is a letter and a discussion; the account returns to the bank without a recorded reason and without an adjustment.

Consequence: the population, the price and the provision cannot be reconciled to the book, and personal data can leave the bank unmasked (BRD Epics 3 to 8 sections 6 and 8.4).

## 4.2 Target state (this product)

### JRN-S6-01 The monthly cycle: population and exclusions (monthly, debt sale officer)

1. The sale cycle opens on its schedule; the workflow reads the rules in force and selects the accounts for sale from the case list.
2. An account with an open deviation or a fraud flag is excluded with a recorded reason and returns to the case list for the next cycle.
3. The population is tested against the policy cap, and the headroom is written where the business reads it.
4. The case owner can see that their case is in the population, or why it is not.

### JRN-S6-02 Lot, tape, room and bid (per lot, debt sale officer and buyer)

1. The accounts are grouped into lots; a lot below the minimum size is merged into the next lot.
2. The lot is priced from the COLLINS lot economics, with the tiered buyer terms and the reserve price proposed; the estimate is recorded with the model and rule version it was computed under.
3. The lot, the reserve and the terms go to the committee; an approval inside the delegation approves them, a raised reserve reprices and returns, a withdrawal records its reason.
4. The masked tape is built under the masking rules in force, checked, and rejected and rebuilt where an unmasked identifier is found.
5. The data room opens to buyers who have signed the non-disclosure agreement; a buyer's KYC, licensing and panel status are checked before the buyer is admitted.
6. A qualified buyer bids inside the window; the bid is recorded against the lot and the buyer, and the window closes against the reserve and the cap.

### JRN-S6-03 Award and approval (per lot, debt sale officer and committee)

1. The best bid is tested against the reserve and the 54 percent cap; a bid below the reserve goes to the committee as a below-reserve outcome with the options to re-offer or withdraw.
2. The award is routed for the approval the delegation names, the level applied and the approver are recorded, and the price achieved against the reserve is kept with them.
3. The sale agreement and the customer notices are generated from approved templates and held on the case.
4. A buyer that fails the qualification check is refused with the reason, given the remediation window, and barred and released to the next bidder where the window is not met.

### JRN-S6-04 Settlement, transfer and posting (per lot, buyer, Credit Administration and the saga)

1. The settlement term starts and the buyer pays; a payment in full confirms settlement and releases the data transfer; a cancellation or an expired term cancels the award, scores the buyer and re-offers the lot to the next qualified bidder.
2. The awarded account data is delivered to the buyer as an encrypted file per lot with its manifest, and the transfer is recorded.
3. The balance is derecognised and the posting goes out; a rejection holds the posting, raises an exception task with a named owner, and is re-posted when the cause is cleared.
4. The sale agreement, the guarantee and the put-back clause are readable from the case, and Finance receives the provision input from the posted population.

### JRN-S6-05 Put-back, case closure and evidence (after the sale, officer and audit)

1. A buyer claim inside the sale terms is recorded and reviewed inside its window; a valid claim returns the account to the bank, adjusts the settlement, reverses the derecognition and returns the account to the case list; a claim outside the terms is refused with a reason.
2. The lot closes with no claim inside the window and the realised recovery is recorded by lot and by buyer.
3. On the award, every open action on a case whose account is sold stops the same day and the case closes.
4. An auditor reads one sale: the population and the exclusions, the price and the model version, the approval and the authority, the masking check, the transfer and the posting, with the rule version of each step.
5. A developer builds against the published contract and its fake; a build that reads an ACE view or an ACE table directly fails.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic. Every capability names the FSD feature it delivers and the wave in which its epic releases it.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-S6-001 | Sale population selected by rule with the cap applied | The population comes from the case list by rule, and every account left out has a reason | BR-044, BR-050 | Must | 3 | FEAT-DBS-01 (A2.1) |
| CAP-S6-002 | Lots built and priced from the COLLINS lot economics | A lot carries its accounts, its estimated price, its tiered terms and a proposed reserve | BR-044 | Must | 3 | FEAT-DBS-02 (A2.2) |
| CAP-S6-003 | Masked data tape with a masking check | The tape cannot reach the data room with an unmasked identifier on it | BR-044 | Must | 3 | FEAT-DBS-03 (A2.3) |
| CAP-S6-004 | Data room opened to admitted buyers only | The room opens to a buyer who has signed the agreement, and not to anyone else | BR-044 | Must | 4 | FEAT-DBS-04 (A2.4) |
| CAP-S6-005 | Lot, reserve and tiered terms approved | The reserve and the terms are approved by the committee that owns them, with the reason recorded | BR-044 | Must | 4 | FEAT-DBS-05 (A2.5) |
| CAP-S6-006 | Buyer qualification against KYC and licensing | A buyer is admitted on evidence, not on memory | BR-045 | Must | 4 | FEAT-DBS-06 (A2.6) |
| CAP-S6-007 | Barring with a remediation window | A buyer that fails is refused with a reason, given a window, and barred and released where the window is not met | BR-045 | Must | 4 | FEAT-DBS-07 (A2.7) |
| CAP-S6-008 | Bids taken inside the window | The bid is a record on the lot, and the window closes against the reserve | BR-046 | Must | 4 | FEAT-DBS-08 (A2.8) |
| CAP-S6-009 | Award tested and approved | The award carries the price against the reserve, the cap test and the approval level applied | BR-047 | Must | 4 | FEAT-DBS-09 (A2.9) |
| CAP-S6-010 | Sale agreement and customer notices generated | The agreement and the customer notices come from approved templates on the case | BR-047 | Must | 4 | FEAT-DBS-10 (A2.10) |
| CAP-S6-011 | Encrypted transfer file per lot | The buyer receives the awarded data as a controlled file with a manifest, and the transfer is recorded | BR-048 | Must | 4 | FEAT-DBS-11 (A2.11) |
| CAP-S6-012 | Derecognition and general ledger posting | The sold accounts leave the book and post without re-keying, and a rejection is held and corrected | BR-048 | Must | 4 | FEAT-DBS-12 (A2.12) |
| CAP-S6-013 | Put-back claim decided on the sale terms | A claim is upheld and the account returned, or refused with a reason, inside its window | BR-049 | Must | 4 | FEAT-DBS-13 (A2.13) |
| CAP-S6-014 | Sold case stopped and closed the same day | The case stops working on the award and closes | BR-049 | Must | 4 | FEAT-DBS-14 (A2.14) |
| CAP-S6-015 | Buyer remittance confirmed against the award | The money side of the lot closes on the award, and a cancellation is scored against the buyer | BR-048 | Must | 4 | FEAT-DBS-15 (A2.15) |
| CAP-S6-016 | Debt sale cap held and headroom reported | The sale population stays inside the cap, and the headroom is a figure the business reads | BR-050 | Must | 4 | FEAT-DBS-16 (A2.16) |
| CAP-S6-017 | Data date, freshness and the ACE read path | Every lot, tape and award states how old its data is, and this service reads ACE data by contract only | BR-044, BR-048 | Must | 3 | A2.1 to A2.16 (VR-S6-001-1 to VR-S6-016-1); A2.1, A2.2 |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Direct read of `v_ace_score`, `v_ace_account` and `v_ace_batch_status` by this service | Not carried | rwb-source-data's contract (GAP-1770; ASM-2942) |
| A separate "PII service" that masks the tape | Not carried as a service | The masking policy of rwb-access applied in this service before P5 stores the pack, with the check in the release gate (GAP-1783; ASM-2955) |
| Direct derecognition and general ledger posting from the module | Not carried | P8 rwb-payment posts; the result is recorded here (GAP-1779; ASM-2951) |
| Direct call to WIN for the customer notices and the sale agreement | Not carried | P6 rwb-comms for the notice, P2 rwb-integration for the registered mail file (INT-14) (GAP-1775; ASM-2947) |
| Quartz scheduling of the monthly sale cycle | Replaced | A Temporal Schedule or an event-started workflow through the workflow kit (GAP-1781; ASM-2953) |
| One workflow per case for the sale stage only | Amended | DebtSaleWorkflow is the stage workflow and a saga across the lot; the case side is moved by rwb-case on the event (GAP-1780; ASM-2952) |
| Buyer KYC, licensing and panel maintenance inside this service | Reused, elsewhere | The panel is S9 rwb-partner; the KYC and licence facts are read as data (GAP-1776; ASM-2948) |
| COLLINS model development and the affordability calculation | Out of scope | Data and AI; the ACE restructure calculator |
| The data lake extract of the sold population | Removed | rwb-reporting read model from events (ADR-018, DP-17) |

# 6. Functional requirements

Every requirement is specific and testable. The FSD REQ column keeps the trace to the source requirement, and the rule column names the routing rules of the source. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Rules | Priority | Wave |
|---|---|---|---|---|---|---|---|
| FR-S6-001 | The service SHALL select the accounts eligible for sale at the sale cycle from the case list by the eligibility rule in force, SHALL exclude any account with an open deviation or a fraud flag, and SHALL record each exclusion with its reason and return the account to the case list for the next cycle. | CAP-S6-001 | BR-044 | REQ-S6-001 | R-DS-01, R-DS-02, R-DS-03 | Must | 3 |
| FR-S6-002 | The service SHALL test the sale population against the policy cap in force, SHALL record the cap value, its version and the resulting headroom, and SHALL not offer a population that would breach the cap. | CAP-S6-001, CAP-S6-016 | BR-044, BR-050 | REQ-S6-001 | RULE-015 | Must | 3 |
| FR-S6-003 | The service SHALL group the selected accounts into lots with the lot number, the balance cut-off date, the segment from LOV-SEGMENT and the outstanding per account at cut-off, and SHALL merge a lot below the minimum lot size into the next lot. | CAP-S6-002 | BR-044 | REQ-S6-002 | R-DS-05 | Must | 3 |
| FR-S6-004 | The service SHALL estimate the price of each lot, the tiered buyer terms and the reserve price from the COLLINS lot economics with the rule and model versions in force, and SHALL record those versions with the estimate. | CAP-S6-002 | BR-044 | REQ-S6-002 | R-DS-04 | Must | 3 |
| FR-S6-005 | The service SHALL take the lot, the reserve and the tiered terms to the approval the delegation names, SHALL record an approval with the authority that approved it, SHALL return a raised reserve to the committee for repricing, and SHALL withdraw a lot with a recorded reason. | CAP-S6-005 | BR-044 | REQ-S6-002 | R-DS-06, R-DS-07, R-DS-08, R-DS-09 | Must | 4 |
| FR-S6-006 | The service SHALL build the data tape for an approved lot under the PDPA masking rules in force, SHALL check the tape for an unmasked identifier before it leaves, and SHALL reject and rebuild the tape where the check fails. | CAP-S6-003 | BR-044 | REQ-S6-003 | R-DS-10, R-DS-11, R-DS-12 | Must | 3 |
| FR-S6-007 | The service SHALL release a tape to the data room only where the masking check passed, SHALL hold the tape in P5 rwb-document, and SHALL refuse the release of a tape that has not passed the check. | CAP-S6-003 | BR-044 | REQ-S6-003 | NFR-041, R-DS-13 | Must | 3 |
| FR-S6-008 | The service SHALL open the data room of a lot only to a buyer with the non-disclosure agreement signed on the lot, and SHALL record the buyer admitted and the time of admission. | CAP-S6-004 | BR-044 | REQ-S6-003 | R-DS-13 | Must | 4 |
| FR-S6-009 | The service SHALL run the KYC, licensing and eligibility check on a bidder before the bidder is admitted, using the KYC result, the licence expiry and the panel status in force, and SHALL record the check, its evidence and its outcome. | CAP-S6-006 | BR-045 | REQ-S6-004 | R-DS-14, R-DS-15, R-DS-16 | Must | 4 |
| FR-S6-010 | The service SHALL refuse access to a bidder whose check fails, SHALL record the refusal and its reason, SHALL open the remediation window in force, and SHALL re-open the check where the evidence arrives inside the window. | CAP-S6-007 | BR-045 | REQ-S6-005 | R-DS-16, R-DS-40 | Must | 4 |
| FR-S6-011 | The service SHALL bar a buyer where the window closes with no evidence or where the failure is a licence breach, SHALL remove the buyer from the panel through the S9 rwb-partner contract, and SHALL release the lot to the next qualified bidder. | CAP-S6-007 | BR-045 | REQ-S6-005 | R-DS-41 | Must | 4 |
| FR-S6-012 | The service SHALL open the bidding window on a cleared buyer at the tiered terms, SHALL record each bid against the lot and the buyer, and SHALL close the window on its close date. | CAP-S6-008 | BR-046 | FEAT-DBS-08 | R-DS-17, R-DS-18 | Must | 4 |
| FR-S6-013 | The service SHALL test the best bid against the reserve price and the policy cap in force, SHALL raise a best bid below the reserve to the committee as a below-reserve outcome, and SHALL re-offer at a revised reserve or withdraw the lot as the committee decides. | CAP-S6-009 | BR-047 | REQ-S6-006 | R-DS-19, R-DS-20, R-DS-21, R-DS-22 | Must | 4 |
| FR-S6-014 | The service SHALL award the lot only where the price has been tested against the reserve and the cap and the award has the approval the delegation names, and SHALL record the price achieved, the reserve, the cap applied, the approval level and the approving role. | CAP-S6-009 | BR-047 | REQ-S6-006 | R-DS-23 | Must | 4 |
| FR-S6-015 | The service SHALL generate the sale agreement and the customer notices for an awarded lot from the approved templates, SHALL hold them on the case through P5, and SHALL record the versions generated. | CAP-S6-010 | BR-047 | REQ-S6-006 | R-DS-23 | Must | 4 |
| FR-S6-016 | The service SHALL record the buyer, the buyer class from LOV-BUYER-CLASS, the signing date, the payment terms and the approval authority on the awarded lot. | CAP-S6-009 | BR-047 | REQ-S6-006 | R-DS-23 | Must | 4 |
| FR-S6-017 | The service SHALL start the settlement term on the award, SHALL confirm settlement on a payment in full, and SHALL record the settlement date against the award. | CAP-S6-015 | BR-048 | REQ-S6-008 | R-DS-24, R-DS-25 | Must | 4 |
| FR-S6-018 | The service SHALL cancel the award and score the cancellation against the buyer where the buyer cancels with a reason or the settlement term expires without payment, and SHALL re-offer the lot to the next qualified bidder where one exists. | CAP-S6-015 | BR-048 | REQ-S6-008 | R-DS-26, R-DS-27, R-DS-28 | Must | 4 |
| FR-S6-019 | The service SHALL build the transfer file for an awarded lot with the awarded account data and its manifest, SHALL hand it to P2 rwb-integration for encrypted delivery to the buyer over MFT (INT-25), and SHALL record the delivery and its reference. | CAP-S6-011 | BR-048 | REQ-S6-008 | R-DS-29 | Must | 4 |
| FR-S6-020 | The service SHALL record the derecognition of the sold balance and SHALL have the posting made through P8 rwb-payment, holding the posting and raising an exception task with a named owner where the posting is rejected, and re-posting where the cause is cleared. | CAP-S6-012 | BR-048 | REQ-S6-008 | R-DS-30, R-DS-31, R-DS-32, R-DS-33 | Must | 4 |
| FR-S6-021 | The service SHALL send the provision input of the sold population to Finance from the posted population, and SHALL not compute a second count of it. | CAP-S6-012 | BR-048 | REQ-S6-008 | R-DS-31 | Must | 4 |
| FR-S6-022 | The service SHALL record a put-back claim raised inside the sale terms, SHALL review it against the terms inside the claim window, and SHALL uphold it or refuse it with a recorded reason. | CAP-S6-013 | BR-049 | REQ-S6-009 | R-DS-35, R-DS-38 | Must | 4 |
| FR-S6-023 | The service SHALL return an upheld claim to the bank, adjust the settlement, reverse the derecognition and return the account to the case list, and SHALL close the lot with its realised recovery where no claim is raised inside the window. | CAP-S6-013 | BR-049 | REQ-S6-009 | R-DS-36, R-DS-37, R-DS-34, R-DS-39 | Must | 4 |
| FR-S6-024 | The service SHALL record the realised recovery by lot and by buyer at the close of the lot, and SHALL publish it for rwb-reporting from the record and the events, not from a separate count. | CAP-S6-016 | BR-050 | FEAT-DBS-16 | R-DS-34 | Must | 4 |
| FR-S6-025 | The service SHALL stop every open action on a case whose account is awarded in a sold lot the same day, and SHALL have the case closed by rwb-case, on LotAwarded and AccountsTransferred. | CAP-S6-014 | BR-049 | REQ-S6-007 | R-UNI-47, EV-23 | Must | 4 |
| FR-S6-026 | The service SHALL publish LotAwarded on `rwb.debtsale.events.v1` when a lot is awarded and AccountsTransferred when the transfer is recorded, keyed by the case, in the same transaction as its state change, and SHALL consume ProceedsMatched idempotently through its inbox. | CAP-S6-011, CAP-S6-014 | BR-048, BR-049 | REQ-S6-007, REQ-S6-008 | DP-09; EV-23, EV-25 | Must | 4 |
| FR-S6-027 | The service SHALL run the sale as DebtSaleWorkflow on `rwb-debtsale` with the transfer as the pivot: the steps before the pivot SHALL have a compensating action, and the steps after it SHALL be retried until they succeed and SHALL wait for the central ledger to confirm the decision record in strict mode. | CAP-S6-011, CAP-S6-012 | BR-048 | REQ-S6-008 | ADR-016, DP-12 | Must | 4 |
| FR-S6-028 | The service SHALL open the sale cycle from a Temporal Schedule or an event-started workflow on its own queue, SHALL use no Quartz table, connection or job, and SHALL record the cycle date it ran for. | CAP-S6-001 | BR-044 | REQ-S6-001 | DP-10 | Must | 3 |
| FR-S6-029 | The service SHALL read every limit, cap, window, threshold and criterion it applies from versioned reference data in force at the business date, and a change SHALL take effect from its valid-from date without a code release. | All | BR-044 to BR-050 | All | BR-S6-001 to BR-S6-016 | Must | 3 |
| FR-S6-030 | The service SHALL obtain every ACE fact it needs — the account balance at cut-off, the COLLINS lot economics, the party identifier and the freshness of each data product — through the rwb-source-data contract, and a read of a `recovery.v_ace_*` view, a read of an ACE table, or a constraint in schema `rwb_debtsale` that references a table outside it SHALL fail the build and the boundary test. | CAP-S6-017 | BR-044, BR-048 | All | DP-01, DP-05 | Must | 3 |
| FR-S6-031 | The service SHALL state the business date and the load time of each data product behind a lot, a tape, an award and a posting, SHALL show a stale product with its date and MSG-P1-001, and SHALL start no step on a data product whose freshness cannot be read. | CAP-S6-017 | BR-044, BR-048 | All | VR-S6-001-1 to VR-S6-016-1; NFR-013, NFR-014 | Must | 3 |
| FR-S6-032 | The service SHALL refuse the selection, the lot approval, the award, the transfer, the posting and the claim decision to a role without the capability area, with MSG-P4-002, and SHALL change nothing on a refusal; and where the decision record cannot be written it SHALL change nothing, raise an incident and show MSG-P7-003. | All | BR-044 to BR-050 | All | AC-EXC-S6-001-01 to AC-EXC-S6-016-02 | Must | 3 |
| FR-S6-033 | The service SHALL hold the lot, the lot accounts, the data room state, the buyer terms, the bids, the award and the transfer as its own records in schema `rwb_debtsale`, with the lot and the lot account named as the Ownership Map names them and the other five held as entity groups until the physical names are fixed with the DB story (GAP-1771; ASM-2943). | CAP-S6-002, CAP-S6-008, CAP-S6-009 | BR-044, BR-046, BR-047 | All | DP-01, DP-15 | Must | 3 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-S6-001 | The lot builder screen responds inside the user's wait, including the read of a lot with all of its accounts and the rules in force. | Under 2 seconds at the 95th percentile | NFR-008, NFR-009 | Must | Performance test in SIT |
| NFR-S6-002 | The data room read of a lot responds inside the buyer's wait through the partner gateway, with the source-data contract in the path. | Under 2 seconds at the 95th percentile | NFR-008 | Must | Performance test in SIT with the contract stub and with the real contract |
| NFR-S6-003 | A rule evaluation at the selection, the pricing, the qualification and the award completes inside the user's wait. | Under 300 milliseconds at the 95th percentile | NFR-011 | Must | Rule timing test with the package in force |
| NFR-S6-004 | The masking check and the tape build complete inside the window the rule in force allows, and a failed check returns the tape for rebuild without leaving the window. | The window in force (3 working days in the routing logic) | NFR-025, NFR-026 | Must | Tape drill with a seeded unmasked identifier |
| NFR-S6-005 | Where the lot estimate uses an agent, the agent answers inside its target; after that the rule result is used and the lot is still priced. | Under 60 seconds, then the rule result | NFR-010, NFR-024 | Must | Agent timeout drill |
| NFR-S6-006 | The service carries the partner and buyer concurrency and the case volume it serves. | About 50 partner users in the busiest hour, of about 320 named users across 35 buyers; about 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts a month | NFR-001, NFR-003 | Must | Volume test at the stated volume |
| NFR-S6-007 | The transfer file of a lot is built, handed over and recorded without holding the workflow past its step timeout, and a failed delivery is retried and then escalated. | One file per lot; retry on schedule; exception queue after three retries | NFR-025, NFR-026 | Must | Failure injection on the delivery |
| NFR-S6-008 | A sale fact reaches rwb-reporting inside the business day it happens, from the events and the decision record. | Same business day | NFR-065 | Must | Measure reconciliation against the events |
| NFR-S6-009 | Every lot, tape, award and posting states the business date and the load time of the data products it read. | Every record | NFR-013 | Must | Record inspection |
| NFR-S6-010 | A missing, failed or late ACE batch is visible at the lot and raises an alert to the data steward; the service holds no load window, staging table or catch-up job. | Visible at the lot; alert to the steward; no load | NFR-014, NFR-015 | Must | Hold and release the batch |
| NFR-S6-011 | The service is available during business hours, when the sale cycle, the bids and the award run, and outside them when a saga step is retried. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-S6-012 | The service inherits the ACE recovery point and recovery time, and a running DebtSaleWorkflow resumes where it stopped. | The ACE recovery point objective and recovery time objective; workflow history preserved | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-S6-013 | Every sale step is reproducible from the log, including the rule package and rule version, the model version of the lot estimate, the approval and the masking check result. | Every step reproducible | NFR-033 | Must | Re-run a sample sale from the log |
| NFR-S6-014 | Every action on a lot carries the rule version applied and the approver who allowed it. | Every action | NFR-034 | Must | Decision record inspection |
| NFR-S6-015 | The decision log hash chain is checked daily, and a break is reported to Compliance the same day. | Daily check, same-day report | NFR-035 | Must | Chain break drill |
| NFR-S6-016 | The decision log answers a single sale history query at its 2031 size inside the user's wait. | Under 2 seconds | NFR-007 | Must | Query test at the forecast size |
| NFR-S6-017 | The debt sale data tape is masked before it reaches the data room, and no unmasked identifier leaves the bank on a tape or a transfer file. | Masked tape; masked transfer | NFR-041 | Must | Masking matrix test on the tape and on the transfer file |
| NFR-S6-018 | Party identifiers are masked at rest and on every screen and every buyer file, by role. | Masked at rest and in use | NFR-039 | Must | Masking matrix test across roles and across the buyer file |
| NFR-S6-019 | Each screen and each buyer receives only the personal data it needs; the buyer file carries no field the sale terms do not name. | Data minimisation per screen and per file | NFR-040 | Must | Contract review per screen and per file |
| NFR-S6-020 | Every read of a personal field is logged, and the read is refused rather than returned where the log cannot be written. | Every read | NFR-042 | Must | Access log reconciliation against reads |
| NFR-S6-021 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | NFR-045 | Must | Environment data review |
| NFR-S6-022 | Every record this service holds carries a data classification and a retention class that set its handling and its disposal. | Classification and retention class per record | NFR-047, NFR-028, NFR-031 | Must | Classification review |
| NFR-S6-023 | Recovery data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | NFR-046 | Must | Tenancy review |
| NFR-S6-024 | Staff authenticate with single sign-on and multi-factor; partner users authenticate with multi-factor and are scoped to their own lots; agents run under service identities subject to the same role checks. | Entra ID single sign-on with multi-factor; partner multi-factor scoped; service identities | NFR-049, NFR-050, NFR-051 | Must | Sign-in and identity test on both gateways |
| NFR-S6-025 | Data is encrypted at rest and in transit, the buyer file is encrypted in transit and at rest (INT-25), and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review, secret scan and file inspection |
| NFR-S6-026 | The build blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency, and every agent output is schema checked with the rule fallback. | Pipeline checks pass; schema check on every agent output | NFR-054, NFR-055 | Must | Pipeline run with a seeded violation; agent output with a bad schema |
| NFR-S6-027 | Screen labels, validation messages and error messages served with this service's operations are available in Thai and in English, and the customer documents are produced in the customer's language. | Every label and message in Thai and English; documents Thai by default | NFR-059, NFR-058 | Must | Label, message and document review |
| NFR-S6-028 | The staff screens meet the bank's accessibility standard and work on the browsers the bank supports, and the data room works on the devices buyers use. | WCAG 2.1 level AA; the current and previous major versions of Microsoft Edge and Google Chrome; desktop browsers and tablets for partner users | NFR-060, NFR-061, NFR-063 | Must | Accessibility scan and browser and device test |
| NFR-S6-029 | Logs, traces and metrics are produced for the cycle, the saga, the masking check and the delivery, every triggered job has a run book, and a failure alerts a named owner. | Every job covered; alert within 15 minutes to the named owner | NFR-064, NFR-067, NFR-068 | Must | Observability review and alert drill |
| NFR-S6-030 | A call is one hop with a 2 s timeout; a failure is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; events that cannot be processed go to the dead-letter topic and are replayed. | One hop; 2 s timeout; three retries then the exception queue; dead-letter with replay | NFR-025, NFR-026 | Must | Failure injection on each call type |
| NFR-S6-031 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in schema `rwb_debtsale`. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_debtsale`. Every table carries the record columns of the platform library (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`). The Ownership Map gives this service two tables, `debt_sale_lot` and `debt_sale_account`, while Architecture v5 gives it six things to hold (lots, data room, buyer terms, bids, award, transfer); the four without a table are carried as entity groups and their physical names are fixed with the DB story (GAP-1771; ASM-2943). Retention is stated by class; the periods are open (GAP-1790; ASM-2962).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `debt_sale_lot` (DF-SAL-020 to DF-SAL-030) | Owned table, one row per lot | `id`; `lot_no` (`varchar(15)`, unique, for example 1/2024); `cut_off_date`; `segment` (LOV-SEGMENT); `reserve_price` (`numeric(18,2)`, baht); `buyer_partner_id`; `buyer_class` (LOV-BUYER-CLASS); `signing_date`; `approval_authority` (`varchar(60)`); `payment_terms` (`varchar(400)`); `status` (LOV-LOT-STATUS: building, offered, awarded, transferred, closed) | [SENSITIVE_FINANCIAL] | Workbench decision; the balance position behind it is read by contract | Workbench record class; period open |
| `debt_sale_account` (DF-SAL-031 to DF-SAL-037) | Owned table, one row per account in a lot | `id`; `lot_id`; `account_key` (`varchar(255)`, business key of the ACE account, no foreign key); `borrower_code` (`varchar(20)`); `outstanding` (`numeric(18,2)`, at cut-off); `selling_price` (`numeric(18,2)`); `put_back_status` (LOV-PUTBACK: none, claimed, accepted, rejected) | [PII] for `borrower_code`; [SENSITIVE_FINANCIAL] for `outstanding` and `selling_price` (GAP-1786; ASM-2958) | ACE account data read through the source-data contract; the selling price is a Workbench decision | Workbench record class; period open |
| Data room state (entity group) | Owned record, one per lot per buyer | The lot, the buyer, the agreement signed at, the admission decision, the check applied, the refusal reason | [CONFIDENTIAL] | Workbench decision; the buyer identity is read from the panel by contract | Workbench record class; period open |
| Buyer terms (entity group) | Owned record, one per lot and tier | The lot, the tier, the price band, the payment terms and the validity in force, the version applied | [CONFIDENTIAL] | Workbench decision; the values are reference data | Workbench record class; period open |
| Bid (entity group) | Owned record, one per bid | The lot, the buyer, the amount, the bid time, the window it was made in, the outcome | [SENSITIVE_FINANCIAL] | The buyer through the partner gateway | Workbench record class; period open |
| Award (entity group) | Owned record, one per awarded lot | The lot, the winning buyer, the price achieved, the reserve, the cap applied, the approval level and approver, the decision, the decided at, the rule version | [SENSITIVE_FINANCIAL] | Workbench decision; the approval is P7's record | Workbench record class; period open |
| Transfer (entity group) | Owned record, one per delivered file | The lot, the file reference, the manifest, the delivered at, the delivery outcome, the posting reference | [CONFIDENTIAL] | Workbench record; the delivery is P2's, the posting P8's | Workbench record class; period open |
| `outbox_event`, `processed_event`, `idempotency_key` | Platform library objects created in this schema | Library-defined | [CONFIDENTIAL] | Service template | Library policy (PLT) |

No copy of an ACE column is held, and no foreign key leaves the schema: `debt_sale_lot.buyer_partner_id` is a business-key column with no foreign key, although the Physical Schema v6 still writes a foreign key to `partner` (GAP-1772; ASM-2944). The business status in `status` (LOV-LOT-STATUS) and the state ladder of the routing rules (LOT_BUILT to LOT_CLOSED) are two vocabularies held side by side: the state is the workflow position and the status is what the screen shows (GAP-1785; ASM-2957).

## 8.2 Data read but not owned

| Data | Read through | Views or tables behind it | Classification of the data read |
|---|---|---|---|
| Account balance at cut-off, account key and borrower code | rwb-source-data contract (the path is open: GAP-1770; ASM-2942) | `v_ace_account` | [PII], [SENSITIVE_FINANCIAL] |
| COLLINS lot economics for the price estimate | rwb-source-data contract (path open) | `v_ace_score` | [SENSITIVE_FINANCIAL] |
| Freshness of each data product | rwb-source-data contract (path open) | `v_ace_batch_status` | [CONFIDENTIAL] |
| Case, party, stage, queue and the case timers | rwb-case contract (Temporal and REST) and its events | none (case schema) | [PII], [SENSITIVE_FINANCIAL] |
| Roles, capability areas, masking policy and the delegation table | rwb-access permission data, cached, and the approval child | none (access schema) | [CONFIDENTIAL] |
| Rule packages and the version in force | rwb-decision contract and events | none (decision schema) | [CONFIDENTIAL] |
| Buyer panel, panel status, partner users and the fee schedule | S9 rwb-partner contract | none (partner schema) | [CONFIDENTIAL] |
| KYC result and licence expiry of a buyer | Open: no source is named (GAP-1776; ASM-2948) | none stated | [CONFIDENTIAL] |
| Document metadata, the data room pack and custody | P5 rwb-document contract (Temporal activity) | none (document schema) | [CONFIDENTIAL] |
| Proceeds and payment matching | P8 rwb-payment events (`ProceedsMatched`) and its contract | none (payment schema) | [SENSITIVE_FINANCIAL] |
| LOV-SEGMENT and LOV-BUYER-CLASS | rwb-case reference-data contract | none (case schema) | [CONFIDENTIAL] |

Counts are not stated: the sources give no field count for a lot or an account beyond the field IDs listed, and no count is recomputed here.

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| `debt_sale_account.borrower_code` | The borrower of the account in the lot | [PII] | Masked on every screen and on the tape and the transfer file; the field is flagged not personal in the Logical Data Model and is handled as personal here (GAP-1786; ASM-2958) |
| `debt_sale_account.account_key` | The business key of the ACE account | [PII] in use, [CONFIDENTIAL] at rest | Masked where the key identifies the customer on the tape; never used as a foreign key |
| `debt_sale_account.outstanding`, `debt_sale_account.selling_price` | The balance at cut-off and the price allocated to the account | [SENSITIVE_FINANCIAL] | Read access by role; no financial value in an event, a workflow input or a log |
| `debt_sale_lot.reserve_price` | The lowest price approved for the lot | [SENSITIVE_FINANCIAL] | Visible to the officer, the committee and the approver only; not carried in LotAwarded |
| `debt_sale_lot.buyer_partner_id`, `buyer_class` | The winning buyer and its class | [CONFIDENTIAL] | The buyer is an external party; the identifier is the panel's |
| Bid amount and buyer | The price a buyer offers | [SENSITIVE_FINANCIAL] | Visible to the officer and the committee inside the window only; the losing bids are not published |
| Party name and identification number, where a screen shows the case party | The party the case belongs to | [PII] | Masked by role; the identification number never leaves in clear; every read logged |
| The transfer file content | The awarded account data delivered to the buyer | [PII], [SENSITIVE_FINANCIAL] | Masked under the sale terms, encrypted, delivered with a manifest, and never carried in an event or a log |

The FSD marks all eight lot catalog fields as not personal data. The account-level attributes reach this service through the case and source-data contracts and are handled as personal and financial data by this document.

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code: the cap and its period, the minimum lot size, the reserve basis, the approval bands, the remediation window, the claim window, the settlement term, the masking rules and the sale terms (GAP-1777, GAP-1778, GAP-1791; ASM-2949, ASM-2950, ASM-2963).
2. This service holds no copy of an ACE column and no staging table; it reads ACE data through the source-data contract only (GAP-1770; ASM-2942).
3. A link to an ACE record or to another service's record is a business-key column with no foreign key (GAP-1772; ASM-2944).
4. A personal field is not returned when the access log cannot be written.
5. Personal data is not put in an event, a workflow input or a log; LotAwarded carries the lot, the case, the award and the versions, and AccountsTransferred the lot, the case and the delivery reference, not the balances.
6. The tape and the transfer file are derived artefacts: the tape is held by P5, the file by P2, and neither is stored in this schema (GAP-1783; ASM-2955).
7. ACE data is retained by ACE, and the archive of a Workbench record belongs to P5 rwb-document.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-source-data (P1) | Out | REST for a screen, Temporal activity inside the workflow | P1 | The only path to the balance at cut-off, the COLLINS economics and the freshness. The slide 13 matrix gives this service no cell to P1, so the path is carried as open (GAP-1770; ASM-2942) |
| ACE database, tables behind the 30 views | Not read | None | ACE team | Read only through the P1 contract. No direct `public` read and no DML from this service |
| rwb-case (P3) | In and out | Child workflow start and signals; events listened to | P3 | The case stage starts DebtSaleWorkflow; this service publishes LotAwarded and AccountsTransferred, and rwb-case stops the open actions and closes the case (R-UNI-47) |
| rwb-decision (P7) | Out | Temporal child workflow (ApprovalWorkflow), decision record and central ledger | P7 | The lot approval and the award go to the authority the delegation names; a strict-mode step waits for the ledger to confirm the record |
| rwb-access (P4) | In | Cached permission data through the guard library, and the masking policy | P4 | Roles, capability areas, the delegation table and the PDPA masking rules the tape is built under |
| rwb-document (P5) | Out | Temporal activity (data room pack) | P5 | The masked tape, the sale agreement and the customer notices are held as documents, with custody and retention |
| rwb-payment (P8) | Out and in | Temporal activity (postProceeds) and the event ProceedsMatched | P8 | Settlement confirmation, the posting and the proceeds matching; the derecognition result is recorded here (GAP-1779; ASM-2951) |
| rwb-integration (P2) | Out | Temporal activity (deliverFile) | P2 | The encrypted buyer file per lot over MFT (INT-25) and, for the customer notices, the registered mail file (INT-14) (GAP-1775; ASM-2947) |
| rwb-comms (P6) | Out | Through the workflow kit's Notify child | P6 | The customer notices of the sale; the slide 13 matrix gives this service no P6 cell, so the path is carried as open (GAP-1775; ASM-2947) |
| rwb-partner (S9) | Out | REST | S9 | The buyer panel, the panel status the check reads, and the bar that removes a buyer from the panel (GAP-1776; ASM-2948) |
| rwb-agent (P10) | Out | Temporal, child workflow and activity | P10 | Where the lot estimate uses an agent: 60 s then the rule result (GAP-1784; ASM-2956) |
| rwb-reporting (P9) | Out | Events and the record | P9 | Realised recovery by lot and by buyer, the cap headroom and the sale measures, from the events and not from a separate count |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | SCR-25 Lot builder and SCR-26 Award; the composite route joins this service's answer with rwb-case and rwb-partner (GAP-1787; ASM-2959) |
| Partner gateway (DMZ) | In | REST under the partner path, multi-factor, scoped to the buyer's own lots | Platform edge with S9 (ADR-019) | PRT-05 Data room and the bid; the buyer never reaches gateway-bff (GAP-1774; ASM-2946) |
| Kafka topic `rwb.debtsale.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by case | This service | LotAwarded (EV-23) and AccountsTransferred (no event number yet); consumers rwb-case, rwb-payment and rwb-reporting (GAP-1782; ASM-2954) |
| Kafka topic `rwb.payment.events.v1` | In | Events consumed through the inbox | P8 | ProceedsMatched (EV-25) closes the money side of the lot |
| ACE common audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |
| ALS, GL and the WIN registered mail | Out, indirectly | Through P8 for the posting and through P2 for the file | P8, P2 | No direct ALS, GL or WIN interface is opened by this service (GAP-1775, GAP-1779; ASM-2947, ASM-2951) |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5 (ADR-018); no extract leaves this service |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Which path carries the account balance, the COLLINS lot economics and the freshness, given that the connection matrix gives this service no cell to rwb-source-data? | Solution architect with P1 | The whole read path of every feature depends on it (GAP-1770; ASM-2942) |
| Who provides the KYC result, the licence expiry and the panel status a buyer is admitted on, and is the panel S9's? | Compliance and PDPA officer with S9 | No buyer can be admitted on an unowned fact (GAP-1776; ASM-2948) |
| Which of the two API namings is published: `/lots` (slide 19) or `/debt-sale-lots` (API Specification v4), and are the buyer operations published under the `/partner` path? | Solution architect | Fixes the gateway route and the screen client before either is built (GAP-1773, GAP-1774; ASM-2945, ASM-2946) |
| Who derecognises the sold balance: this service, P8, or the core bank, and how is the result read back? | Solution architect with P8 and the ACE team | The sale is not complete until the book agrees (GAP-1779; ASM-2951) |
| Is the sale one workflow per lot or one child workflow per case, and how are the case steps reached from the lot workflow? | Solution architect | Fixes the workflow shape and the parent close policy before the first story (GAP-1780; ASM-2952) |
| Which schedule or workflow opens the monthly sale cycle, and who owns its trigger row in the job map? | Platform administrator with the solution architect | A sale that nobody starts is a sale that does not run (GAP-1781; ASM-2953) |

# 10. Release slicing proposal

The service is created in wave 3. Its own capabilities release in two epics: EP05 (wave 3, release 31 March 2027 (tentative)) takes the population, the lot, the tape and the data room; EP06 (wave 4, release 30 April 2027 (tentative)) takes the buyer, the bid, the award, the transfer, the posting, the put-back and the cap report. Each slice is a list of capabilities, not stories. The service wave (3) and the E6 wave (4) do not conflict: the conflict rule applies where a business epic wave is earlier than the service wave, and here it is later. The release dates are the ones in the Program BRD release plan, copied unchanged and marked tentative (ASM-2965, ASM-2966).

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library, the Temporal workflow kit with the approval, Notify, document, agent and saga children, the schema and login provision, the Kafka event platform and naming library, the edge and both gateways, and observability. These belong to the platform epics and are not capabilities of this product. The prerequisite feature codes the FSD names from other modules (FEAT-DRI-07, FEAT-RDF-15, FEAT-OCC-07, FEAT-APD-01) are other services' capabilities and are consumed as contract dependencies, not as build dependencies (GAP-1789; ASM-2961).

## 10.2 Wave 3 — EP05, litigation and debt sale preparation (release 31 March 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 3.1 Published contract, lot and lot account | CAP-S6-002, CAP-S6-017 | Nothing can be built or tested until the lot and its accounts exist with their data date, and the boundary test must fail the build on a direct ACE read from the first story |
| 3.2 Sale cycle and population | CAP-S6-001 | The population by rule, with every exclusion named, is the first thing the business can see and the first thing audit asks for |
| 3.3 Pricing and the committee | CAP-S6-002, CAP-S6-005 | A lot without an estimated price and an approved reserve cannot be offered, and the reserve is the last control before the tape is spent |
| 3.4 Masked tape and data room | CAP-S6-003, CAP-S6-004 | The tape is the artefact that can lose personal data, and the room is what the buyer sees; neither is safe to defer |
| 3.5 Cap enforcement and headroom | CAP-S6-016 | The cap is a board limit; applying it at selection without reporting the headroom leaves the limit unread (the report itself lands with 4.7) |

Rationale: the wave-3 slice delivers the Epic 5 outcome, "debt sale lot data and the buyer data room", and every slice is independently demonstrable. The data room is opened in the same wave because a tape with no room is a tape with no reader.

## 10.3 Wave 4 — EP06, debt sale and write-off (release 30 April 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 4.1 Buyer qualification and barring | CAP-S6-006, CAP-S6-007 | An unqualified buyer must not see a tape, so the gate and its bar land before the first bid |
| 4.2 Bids and the window | CAP-S6-008 | A bid on the case is the difference between a sale and an email |
| 4.3 Award, agreement and notices | CAP-S6-009, CAP-S6-010 | The award is the last price control and the customer has a right to be told |
| 4.4 Settlement, transfer and posting | CAP-S6-011, CAP-S6-012, CAP-S6-015 | The sale is only complete when the book and the money agree, and the saga's pivot is the transfer |
| 4.5 Put-back and case closure | CAP-S6-013, CAP-S6-014 | A sold case that keeps working creates work against a book the bank no longer owns, and the claim is the buyer's remedy |
| 4.6 Sale ledger | CAP-S6-016 | Realised recovery by lot and by buyer, and the cap headroom, from the events into rwb-reporting |
| 4.7 Sale measures and the cap report at full width | CAP-S6-016, CAP-S6-017 | The measures read the events and the decision record once both exist across the whole cycle |

Rationale: the wave-4 slice is the smallest set that delivers the Epic 6 outcome for debt sale, and the slices follow the saga: everything before the pivot can be undone, everything after it must finish.

## 10.4 Later increments

| Increment | What unlocks it |
|---|---|
| The debt sale rule package as a governed package | Phase 2 of the Drools design, with the 41-rule set, its version label and its owner in rwb-decision (GAP-1771; ASM-2943; design slide 22) |
| An agent-assisted lot estimate | The pricing agent's policy, guardrails and threshold agreed in rwb-agent, with the rule result as the fallback (GAP-1784; ASM-2956) |
| The buyer self-service data room at full width | The partner portal live at the edge with the buyer population on it (ADR-019; Non Functional Specification v3 section 4) |
| The cap basis and period as a confirmed policy | The Head of Asset Liquidity answering Q-010, then held as reference data (GAP-1777; ASM-2949) |
| The data room, bid, award and transfer table set in the Ownership Map and the physical schema | The data architect's table list, added with the DB story (GAP-1771; ASM-2943) |
| The realised recovery and provision measures at full width | The rwb-reporting read model, fed by the events and the record (ADR-018) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-S6-001 | FR-S6-001, FR-S6-028, NFR-S6-003 | a case list with accounts inside and outside the eligibility rule, one with an open deviation X2 and one with a fraud flag | the sale cycle opens | the eligible accounts are selected, each excluded account is recorded with its reason and returned to the case list, and the cycle date and rule version are recorded; no Quartz job is used | AC-S6-001-01; R-DS-01, R-DS-02, R-DS-03 |
| AC-S6-002 | FR-S6-002, FR-S6-024, NFR-S6-008 | a cap in force for the period and a population that would breach it if the last accounts were added | the population is tested and the cycle runs to its close | the population is held inside the cap, the cap value and its version are recorded with the headroom, and the headroom is readable in rwb-reporting inside the business day | AC-S6-016-01; BR-050, RULE-015 |
| AC-S6-003 | FR-S6-003, FR-S6-004, FR-S6-033 | a selected population, a minimum lot size in force and the COLLINS economics in force | the lots are built and priced | each lot carries its number, cut-off date, segment and outstanding per account; a lot below the minimum is merged; the estimate, the terms and the reserve carry the rule and model versions applied; one row exists per lot and per lot account with no foreign key leaving the schema | AC-S6-002-01; GAP-1771; ASM-2943 |
| AC-S6-004 | FR-S6-005 | a priced lot and a delegation table in force | the lot goes to the committee; the reserve is raised once and approved the second time; a third lot is withdrawn | the approval records the authority that approved it; the raised reserve returns the lot to the committee repriced; the withdrawal records its reason and returns the accounts to the case list | AC-S6-005-01; R-DS-06, R-DS-07, R-DS-08, R-DS-09 |
| AC-S6-005 | FR-S6-006, FR-S6-007, NFR-S6-017 | an approved lot and a masking rule set in force; one run with a seeded unmasked identifier and one clean run | the tape is built and checked | the seeded run is rejected, the tape is marked rejected and rebuilt, and no tape reaches the data room; the clean run passes the check and is released as a document; no unmasked identifier is present on either | AC-S6-003-01; R-DS-10, R-DS-11, R-DS-12; NFR-041 |
| AC-S6-006 | FR-S6-008, NFR-S6-019 | a lot with two buyers, one with the agreement signed and one without | the data room is opened and each buyer asks for the lot | the signed buyer is admitted and the admission is recorded; the unsigned buyer is refused and nothing is disclosed; the buyer answer carries no field the terms do not name | AC-S6-004-01; R-DS-13, NFR-040 |
| AC-S6-007 | FR-S6-009, FR-S6-010, FR-S6-011 | a signed buyer whose KYC result is failed and whose licence has expired, and a second buyer whose check passes | both ask for admission and the window is run twice, once with evidence supplied and once without | the passing buyer is admitted with the evidence recorded; the failing buyer is refused with the reason, re-checked when evidence arrives, and barred with the panel updated through S9 and the lot released where the window closes without evidence | AC-S6-006-01, AC-S6-007-01; R-DS-14 to R-DS-16, R-DS-40, R-DS-41 |
| AC-S6-008 | FR-S6-012 | a cleared buyer, one lot and a bid window in force | the buyer bids twice inside the window and once after it closes | both bids inside the window are recorded against the lot and the buyer with their times; the late bid is refused and nothing changes | AC-S6-008-01; R-DS-17, R-DS-18 |
| AC-S6-009 | FR-S6-013 | one lot whose best bid is above the reserve and one whose best bid is below it | the window closes | the first lot goes to the award test; the second is raised to the committee as a below-reserve outcome, and on the committee decision is either re-offered at a revised reserve or withdrawn with its reason | AC-S6-009-01; R-DS-19 to R-DS-22 |
| AC-S6-010 | FR-S6-014, FR-S6-016, NFR-S6-014 | a tested bid inside the delegation and a second one above it | the award is requested in both cases | the first records the price achieved, the reserve, the cap applied, the approval level and the approving role; the second reaches the committee and records the level applied; the buyer, the buyer class, the signing date, the payment terms and the approval authority are on the lot | AC-S6-009-01; R-DS-23; GAP-1778; ASM-2950 |
| AC-S6-011 | FR-S6-015, NFR-S6-027 | an awarded lot and the approved templates in force | the agreement and the notices are generated | the agreement and the notices are produced from the templates in the customer's language, held on the case with their versions recorded, and no field is re-keyed | AC-S6-010-01; R-DS-23; NFR-058 |
| AC-S6-012 | FR-S6-017, FR-S6-018, FR-S6-027 | an awarded lot with a settlement term, one buyer who pays in full and one who does not | the term runs | the paying buyer's settlement is confirmed and the transfer released; the other award is cancelled with its reason, the cancellation is scored against the buyer, and the lot is re-offered to the next qualified bidder | AC-S6-015-01; R-DS-24 to R-DS-28 |
| AC-S6-013 | FR-S6-019, NFR-S6-007, NFR-S6-025 | a settled lot and the delivery contract in force; one delivery that fails every retry | the transfer runs | the file and its manifest are handed over, delivered encrypted and recorded with the delivery reference; the failed delivery is retried on the schedule, appears in the exception queue with a task for a named owner, and nothing else on the lot changes | AC-S6-011-01; R-DS-29; INT-25, NFR-026 |
| AC-S6-014 | FR-S6-020, FR-S6-021, NFR-S6-012 | a transferred lot; the posting is rejected once and then cleared | derecognition and posting run | the derecognition is recorded, the posting is made through P8, the rejection holds the posting and raises an exception task, and the cleared cause re-posts; the provision input reaches Finance from the posted population | AC-S6-012-01; R-DS-30 to R-DS-33; GAP-1779; ASM-2951 |
| AC-S6-015 | FR-S6-022, FR-S6-023 | a posted lot with one claim inside the sale terms and one outside them, and a second lot with no claim | the window closes | the valid claim returns the account, adjusts the settlement, reverses the derecognition and returns the account to the case list; the invalid claim is refused with its reason; the lot with no claim closes with its realised recovery by lot and by buyer | AC-S6-013-01; R-DS-34 to R-DS-39 |
| AC-S6-016 | FR-S6-025, FR-S6-026, NFR-S6-008 | an awarded lot whose accounts carry open actions on their cases | the award is recorded | LotAwarded is in the outbox in the same transaction and every open action stops the same day; AccountsTransferred follows the delivery; rwb-case closes the case and rwb-reporting reads both events | AC-S6-014-01; R-UNI-47, EV-23; GAP-1782; ASM-2954 |
| AC-S6-017 | FR-S6-026, FR-S6-027 | a running DebtSaleWorkflow at the transfer step and the central ledger refusing to confirm the record | the transfer step is attempted | the step waits and is retried, is not treated as failed, and the earlier steps keep their compensating actions available; no partial transfer is published as done | AC-S6-011-01; design slide 22 and 26 (pivot at transfer, strict mode); GAP-1780; ASM-2952 |
| AC-S6-018 | FR-S6-030, FR-S6-031, NFR-S6-009, NFR-S6-010 | a branch that reads `recovery.v_ace_score` directly, a constraint in `rwb_debtsale` that references `partner`, and one data product STALE at the business date | the pipeline and the boundary test run and the lot is read | the build fails naming the view read and the cross-schema constraint; the stale product is shown with its date and MSG-P1-001 and the lot records the business date and load time it used | AC-EXC-S6-001-01; VR-S6-001-1; GAP-1770, GAP-1772; ASM-2942, ASM-2944 |
| AC-S6-019 | FR-S6-032, NFR-S6-024 | a user without the capability area on the staff gateway and a buyer signed in through the partner gateway on a lot that is not theirs | each tries to read the lot, approve it and bid on it | every action is refused with MSG-P4-002 and nothing changes; the buyer sees no lot outside its scope | AC-EXC-S6-001-01 to AC-EXC-S6-016-01; NFR-050 |
| AC-S6-020 | FR-S6-032, NFR-S6-015 | the decision record store rejecting every write | the award is attempted | nothing changes on the lot, MSG-P7-003 is shown and an incident is raised; the daily hash-chain check reports the gap the same day | AC-EXC-S6-009-02, AC-EXC-S6-016-02; NFR-035 |
| AC-S6-021 | FR-S6-029, NFR-S6-013, NFR-S6-022 | a cap, a minimum lot size, a remediation window and a claim window in force, then new values from a valid-from date | a sale runs before and after the change, and an auditor reads both | each step applies the value in force at its business date, the version applied is recorded, and both sales are reproducible from the log with their classification and retention class | AC-S6-001-01, AC-S6-002-01; BR-S6-001 to BR-S6-016; NFR-033, NFR-047 |
| AC-S6-022 | FR-S6-033, NFR-S6-031 | a release of the lot, bid and award slices | a rollback is rehearsed | the previous tag is redeployed and the data stays; the migration sequence in `rwb_debtsale` is unchanged by the rollback and no other schema is touched | AC-S6-002-01; NFR-027, ADR-014 |

## 11.2 Requirement trace summary

| BR | Program requirement | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|---|
| BR-044 | REQ-S6-001 | CAP-S6-001, CAP-S6-016 | FR-S6-001, FR-S6-002, FR-S6-028 | NFR-S6-003, NFR-S6-006, NFR-S6-009, NFR-S6-010, NFR-S6-013, NFR-S6-021 | AC-S6-001, AC-S6-002, AC-S6-021 |
| BR-044 | REQ-S6-002 | CAP-S6-002, CAP-S6-005 | FR-S6-003, FR-S6-004, FR-S6-005, FR-S6-033 | NFR-S6-001, NFR-S6-005, NFR-S6-013, NFR-S6-014, NFR-S6-022, NFR-S6-031 | AC-S6-003, AC-S6-004, AC-S6-022 |
| BR-044 | REQ-S6-003 | CAP-S6-003, CAP-S6-004 | FR-S6-006, FR-S6-007, FR-S6-008 | NFR-S6-002, NFR-S6-004, NFR-S6-017, NFR-S6-018, NFR-S6-019, NFR-S6-020, NFR-S6-023, NFR-S6-025 | AC-S6-005, AC-S6-006, AC-S6-019 |
| BR-045 | REQ-S6-004 | CAP-S6-006 | FR-S6-009 | NFR-S6-020, NFR-S6-024, NFR-S6-028 | AC-S6-007, AC-S6-019 |
| BR-045 | REQ-S6-005 | CAP-S6-007 | FR-S6-010, FR-S6-011 | NFR-S6-006, NFR-S6-014, NFR-S6-022, NFR-S6-030 | AC-S6-007 |
| BR-046 | FEAT-DBS-08 | CAP-S6-008 | FR-S6-012, FR-S6-033 | NFR-S6-001, NFR-S6-002, NFR-S6-006, NFR-S6-018, NFR-S6-028, NFR-S6-030 | AC-S6-008, AC-S6-019 |
| BR-047 | REQ-S6-006 | CAP-S6-009, CAP-S6-010 | FR-S6-013, FR-S6-014, FR-S6-015, FR-S6-016 | NFR-S6-003, NFR-S6-014, NFR-S6-027, NFR-S6-029 | AC-S6-009, AC-S6-010, AC-S6-011 |
| BR-048 | REQ-S6-008 | CAP-S6-011, CAP-S6-012, CAP-S6-015 | FR-S6-017, FR-S6-018, FR-S6-019, FR-S6-020, FR-S6-021, FR-S6-026, FR-S6-027 | NFR-S6-007, NFR-S6-008, NFR-S6-011, NFR-S6-012, NFR-S6-015, NFR-S6-016, NFR-S6-025, NFR-S6-030 | AC-S6-012, AC-S6-013, AC-S6-014, AC-S6-016, AC-S6-017, AC-S6-020 |
| BR-049 | REQ-S6-007, REQ-S6-009 | CAP-S6-013, CAP-S6-014 | FR-S6-022, FR-S6-023, FR-S6-025, FR-S6-026 | NFR-S6-008, NFR-S6-013, NFR-S6-014, NFR-S6-016 | AC-S6-015, AC-S6-016 |
| BR-050 | FEAT-DBS-16 (RULE-015) | CAP-S6-016 | FR-S6-002, FR-S6-024 | NFR-S6-008, NFR-S6-013 | AC-S6-002, AC-S6-015 |
| All — read path and limits | All REQ-S6 · All BR | CAP-S6-017 | FR-S6-029, FR-S6-030, FR-S6-031, FR-S6-032 | NFR-S6-009, NFR-S6-010, NFR-S6-021, NFR-S6-024, NFR-S6-026, NFR-S6-031 | AC-S6-018, AC-S6-019, AC-S6-020, AC-S6-021, AC-S6-022 |

BR coverage: 9 of the 9 program requirements of this module (REQ-S6-001 to REQ-S6-009) and 7 of the 7 BRD requirements that name this service (BR-044 to BR-050) are covered by at least one functional requirement. No requirement of this module is left without a functional requirement, and no functional requirement lacks a source requirement. BR-046 and BR-050 have no program requirement ID of their own; they trace to the FSD features FEAT-DBS-08 and FEAT-DBS-16 and to RULE-015 (ASM-2967).

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Boundary and conformance test output in system test | FR-S6-030, NFR-S6-026 | Developer with the security administrator |
| Contract test against the source-data, partner, payment and document contracts and their fakes | FR-S6-009, FR-S6-011, FR-S6-019, FR-S6-020, FR-S6-030, FR-S6-031 | Developer with P1, S9, P8 and P5 |
| Sale cycle drill: a population with exclusions, a cap breach avoided and a stale product | FR-S6-001, FR-S6-002, FR-S6-031, NFR-S6-010 | QA team |
| Lot and pricing test with a below-minimum lot, a raised reserve and a withdrawal | FR-S6-003, FR-S6-004, FR-S6-005 | Debt sale officer with the QA team |
| Tape and masking drill with a seeded unmasked identifier, a rejection and a rebuild | FR-S6-006, FR-S6-007, FR-S6-008, NFR-S6-017 | Compliance and PDPA officer with the QA team |
| Buyer qualification drill: pass, fail, remediation and bar | FR-S6-009, FR-S6-010, FR-S6-011 | Compliance and PDPA officer with S9 |
| Bid window and award matrix across the delegation levels and the committee path | FR-S6-012, FR-S6-013, FR-S6-014, FR-S6-016, NFR-S6-014 | Head of Asset Liquidity with the QA team |
| Saga drill: pivot at the transfer, a rejected posting and an upheld put-back | FR-S6-019, FR-S6-020, FR-S6-023, FR-S6-027, NFR-S6-007 | QA team with P8 and P2 |
| Sale reproducibility and decision record review | FR-S6-024, FR-S6-033, NFR-S6-013, NFR-S6-015, NFR-S6-016 | Internal audit with the center of excellence analyst |
| Masking matrix, access log reconciliation and classification review on the tape and the transfer file | NFR-S6-017 to NFR-S6-022 | Compliance and PDPA officer |
| Performance and volume test at the stated partner concurrency and case volume | NFR-S6-001, NFR-S6-002, NFR-S6-003, NFR-S6-006 | QA team |

# 12. Open questions

The BRD's open items are carried forward with their IDs where they have one. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-S6-01 | Which path carries the account balance at cut-off, the COLLINS lot economics and the freshness, given that the connection matrix gives this service no cell to rwb-source-data? | Solution architect with P1 | Before wave 3 system test | CAP-S6-001 to CAP-S6-003, CAP-S6-017 | GAP-1770; ASM-2942; Arch v5 slides 13, 37 and 45 |
| OQ-S6-02 | Which tables hold the data room state, the buyer terms, the bids, the award and the transfer, given that the Ownership Map lists only `debt_sale_lot` and `debt_sale_account`? | Data architect | Before the S6 DB story | CAP-S6-004, CAP-S6-008, CAP-S6-009, CAP-S6-011, CAP-S6-012 | GAP-1771; ASM-2943 |
| OQ-S6-03 | Does `debt_sale_lot.buyer_partner_id` keep a foreign key to `partner`, which sits in another service's schema, or become a business-key column with no foreign key? | Data architect with S9 | Before the S6 DB story | CAP-S6-009, CAP-S6-011 | GAP-1772; ASM-2944; ADR-014 |
| OQ-S6-04 | Is the lot resource published as `/lots` (slide 19) or `/debt-sale-lots` (API Specification v4), and is there a staff read of the bids? | Solution architect | Before the S6 contract story closes | CAP-S6-008, CAP-S6-009 | GAP-1773; ASM-2945 |
| OQ-S6-05 | Do the buyer operations (`/partner/data-room/...`) belong to this service behind the partner gateway, and does a buyer ever reach gateway-bff? | Solution architect with the edge owner | Before wave 4 system test | CAP-S6-004, CAP-S6-006, CAP-S6-008 | GAP-1774; ASM-2946; ADR-019 |
| OQ-S6-06 | How are the customer notices of the sale sent, given that the saga names rwb-comms, the FSD names WIN and the connection matrix gives this service no P6 cell? | Solution architect with P6 and P2 | Before wave 4 system test | CAP-S6-010 | GAP-1775; ASM-2947 |
| OQ-S6-07 | What licensing and eligibility criteria must a debt buyer meet, and who may bar it (BRD Q-011)? | Compliance and PDPA officer | Before wave 4 release | CAP-S6-006, CAP-S6-007 | GAP-1776; ASM-2948; BRD Q-011 |
| OQ-S6-08 | What is the basis and the period of the debt sale cap, beyond the 54 percent figure (BRD Q-010)? | Head of Asset Liquidity | Before wave 4 release | CAP-S6-001, CAP-S6-016 | GAP-1777; ASM-2949; BRD Q-010 |
| OQ-S6-09 | What is each approval limit and the substitute for each (DL18), and do the PARC and ExCo bands of the design stand? | Risk with the product heads | Before wave 4 release | CAP-S6-005, CAP-S6-009 | GAP-1778; ASM-2950; DL18 |
| OQ-S6-10 | Who derecognises the sold balance, and how does the posting reach ALS and the general ledger without a direct interface from this service? | Solution architect with P8 and the ACE team | Before wave 4 system test | CAP-S6-012, CAP-S6-015 | GAP-1779; ASM-2951 |
| OQ-S6-11 | Is the sale one workflow per lot or one child workflow per case, and how does the lot workflow move the case? | Solution architect | Before the first story of the epic | CAP-S6-011, CAP-S6-012, CAP-S6-014 | GAP-1780; ASM-2952 |
| OQ-S6-12 | Which Temporal Schedule or event opens the monthly sale cycle, and who owns its row in the job map? | Platform administrator with the solution architect | Before wave 3 system test | CAP-S6-001 | GAP-1781; ASM-2953 |
| OQ-S6-13 | Does AccountsTransferred get an EV number and a catalogue row, and which consumers besides rwb-case, rwb-payment and rwb-reporting subscribe? | Solution architect | Before wave 4 system test | CAP-S6-011, CAP-S6-014 | GAP-1782; ASM-2954 |
| OQ-S6-14 | What are the put-back claim window, the buyer remediation window and the settlement term, and which role fixes them (DL22)? | Head of Asset Liquidity | Before wave 4 release | CAP-S6-007, CAP-S6-013, CAP-S6-015 | GAP-1791; ASM-2963; DL22 |
| OQ-S6-15 | What classification and what retention period apply to the lot, the lot account, the tape and the transfer file (DL26)? | Compliance and PDPA officer | Before wave 3 release | CAP-S6-002, CAP-S6-003, CAP-S6-011 | GAP-1790; ASM-2962; DL26 |
| OQ-S6-16 | Which service owns the wording of MSG-S6-001 and the Thai and English versions of the four shared messages, and who approves them? | Business analyst, S6 | Before wave 4 release | All messages | GAP-1788; ASM-2960 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (ASM-2964).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 2 (business outcomes), 5.13 (S6 requirements, REQ-S6-001 to REQ-S6-009), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan), 9 (open decisions incl. DL18, DL22, DL26, DL43), 10.1 to 10.5 (the service epic RWB-SVC-S6, schema, wave, contract-first delivery, shared item owners) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 4.2 and 4.4 (E5 and E6 releases, delivery model), 5 (stakeholders, incl. Head of Asset Liquidity, debt sale officer, debt buyer and AMC), 6 (current state), 7.1 and 7.3 (E5 and E6 scope, services and waves), 8.3 and 8.4 (BR-044, BR-045 to BR-050), 9 (RULE-015 to RULE-018), 10 (KPI-005, KPI-006, KPI-011), 11.1 to 11.4 (ASM-017, ASM-018, ASM-028, ASM-029, CON-010, DEP-009, RISK-002, RISK-005), 12 (Q-001, Q-010, Q-011, Q-012), 13 (governance) |
| Recovery Workbench FSD S6 Debt sale v3 | Document control, Existing capability check, A1 (context, scope, dependencies, feature overview), A2.1 to A2.16 (functional decomposition with field catalog, rules, roles and acceptance criteria), Requirements served, Screens, Appendix A and B |
| Recovery Workbench Business Rules and Routing Logic v4 | R-DS-01 to R-DS-41 (the debt sale route set, the state ladder and the escalation of each rule) |
| Recovery Workbench Architecture v5 | Slides 3 (the eight routes and D8 debt sale), 4 (19 modules), 9 to 13 (call types, timeouts, retry, the connection matrix), 14 to 20 (service contracts, S6 IN and OUT), 25 and 26 (stage workflows, the seven-step debt sale saga and its pivot), 30 (19 schemas), 31 to 32 (the bank scheduler at the edges), 37 (what changes and why), 41 (service catalogue), 42 and 43 (event catalogue: EV-23, EV-25, AccountsTransferred), 44 (job map), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Slides 12 and 13 (the workflow kit and the stage workflow steps), 22 (S6 debt sale: the seven steps, the 41-rule set, who approves, the clocks, the pivot and the undo) |
| Recovery Workbench Microservice Ownership Map v1 | Services (S6 row: schema, REST base, topic, queue), API (the five S6 operations), Events (EV-23), Workflows (DebtSaleWorkflow), Tables (`debt_sale_lot`, `debt_sale_account`), Jobs (no S6 row) |
| Recovery Workbench Physical Schema v6 and Logical Data Model and Data Dictionary v8 | `debt_sale_lot` and `debt_sale_account` definitions, the foreign keys and indexes, DF-SAL-020 to DF-SAL-037, LOV-LOT-STATUS, LOV-PUTBACK, LOV-SEGMENT, LOV-BUYER-CLASS, DP09 (debt sale data product), the personal-data flags |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency, incl. 35 buyers), 3.1 to 3.12 (requirements by quality characteristic), 4 (partner access: debt buyers first needed at Epic 5) |
| Recovery Workbench API Specification v4 | `/debt-sale-lots`, `/debt-sale-lots/{lotId}`, `/debt-sale-lots/{lotId}/award`, `/partner/data-room/{lotId}`, `/partner/data-room/{lotId}/bids` with their capability rights and first release |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R4 (services and naming), R5 (target structure, DP table, wave map), R8 (outputs), R9 (gaps and assumptions) |
