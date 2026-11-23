SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD S2 rwb-treatment v1
description: Product requirements for the Recovery Workbench treatment service (S2 rwb-treatment) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S2 TDR, settlement and deed in lieu v3.md
service: S2 rwb-treatment
epic: RWB-SVC-S2
wave: 2
decision: D-RCV-60
---

# Recovery Workbench PRD S2 rwb-treatment v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD S2 rwb-treatment |
| Document ID | S2-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | S2 rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 (service wave, Architecture v5 slide 41) |
| Business epic | EP02 (Epic 2, wave 2, release 31 December 2026 (tentative)). The requirements of this module are scheduled in E3 (release 31 January 2027 (tentative)); see section 10 and GAP-1709 |
| Schema | `rwb_treatment` |
| REST base | `/api/recovery/treatment/v1` |
| Topic | `rwb.treatment.events.v1` |
| Temporal task queue | `rwb-treatment` |
| Java package | `th.co.scb.ace.workbench.recovery.treatment` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Business analyst, S2 |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), ADR-010, ADR-013 to ADR-023 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epic 2 v3; FSD S2 TDR, settlement and deed in lieu v3; Architecture v5; Temporal and Drools Design v1 |
| Upstream requirement IDs | REQ-S2-001 to REQ-S2-010 (program requirements, and the same IDs in the FSD); RWB-E2-004, RWB-E2-006, RWB-E2-007, RWB-E2-008, RWB-E2-010, RWB-E2-017, RWB-E2-018, RWB-E2-025, RWB-E2-026, RWB-E2-027, RWB-E2-032 (Epic 2 development-detail requirements naming this service); NFR-001, NFR-002, NFR-005, NFR-006, NFR-008, NFR-009, NFR-010, NFR-011, NFR-013, NFR-014, NFR-015, NFR-020, NFR-021, NFR-022, NFR-023, NFR-024, NFR-025, NFR-026, NFR-027, NFR-028, NFR-029, NFR-033, NFR-034, NFR-035, NFR-038, NFR-039, NFR-040, NFR-042, NFR-044, NFR-045, NFR-046, NFR-047, NFR-049, NFR-051, NFR-052, NFR-053, NFR-054, NFR-055, NFR-058, NFR-059, NFR-060, NFR-061, NFR-062, NFR-064, NFR-065, NFR-066, NFR-067, NFR-068, NFR-077 |
| Upstream acceptance criteria | AC-S2-001-01 to AC-S2-018-01 (main success flow, one per feature); AC-EXC-S2-001-01 to AC-EXC-S2-018-01 (role without the right); AC-EXC-S2-001-02 to AC-EXC-S2-018-02 (decision cannot be recorded). The FSD defines no alternate flow and no system background event for any of the eighteen features |
| Generated IDs | CAP-S2-001 to CAP-S2-019; FR-S2-001 to FR-S2-042; NFR-S2-001 to NFR-S2-032; AC-S2-001 to AC-S2-024; JRN-S2-01 to JRN-S2-06; ROL-S2-01 to ROL-S2-14; OQ-S2-01 to OQ-S2-16 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD S2 TDR, settlement and deed in lieu v3 (15 November 2026) and Business Requirements Epic 2 v3 (22 November 2026), realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD S2 TDR, settlement and deed in lieu v3. Its feature IDs, requirement IDs, rule IDs, validation rule IDs and acceptance criterion IDs are carried unchanged; the microservice realignment changes the read path, the mechanism of the timers, the owner of several capabilities and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Encumbrance and title checks read the ACE collateral views. Everything else unchanged from v2. |
| 1 and 2 | Not specified in the source documents (GAP-1715; ASM-2868) | Earlier versions of the FSD. Their dates and change notes are not in the sources read, and are carried as an open item rather than reconstructed |
| 1 (PRD) | 22 November 2026 | First PRD of this family (ASM-2870). CAP, FR, NFR, AC, journey and open-question IDs are new; the FSD feature IDs (FEAT-TRT-01 to FEAT-TRT-18), requirement IDs (REQ-S2-001 to REQ-S2-010), validation rule IDs (VR-S2-001-1 to VR-S2-018-1), business rule IDs (BR-S2-001 to BR-S2-018), routing rule IDs (R-RES-01 to R-RES-33, R-SET-01 to R-SET-23, R-DIL-01 to R-DIL-32), acceptance criteria IDs (AC-S2-001-01 to AC-S2-018-01 and their exception rows), message IDs (MSG-S2-001, MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001), list IDs (LOV-TREATMENT, LOV-PROPOSER) and screen IDs (SCR-14, SCR-15, SCR-16) are preserved character for character |

The FSD's own dependency sentence repeats FEAT-CHO-08 twice. It is carried as written and marked (GAP-1715; ASM-2868).

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the program requirements REQ-S2-001 to REQ-S2-010 and of the non-functional requirements |
| Recovery Workbench Business Requirements Epic 2 v3 | BRD | Source of the Epic 2 requirements that name this service (RWB-E2-004 to RWB-E2-032), the delivery model, the wave map and the open decisions |
| Recovery Workbench Functional Specifications by Module v6, FSD S2 TDR, settlement and deed in lieu v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, only rwb-source-data reads ACE, Kafka, Temporal, Nexus to ACE Common, no data lake, edge and gateway |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: TreatmentWorkflow on `rwb-treatment`, the approval, document and payment children, the three Drools packages, the clocks and the pivots |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every operation, event, workflow, table and job named here |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-treatment (S2) is the recovery module's offer and plan. It turns "a route is approved, then a person negotiates and tracks it by hand for 23 to 26 days" into a product: a treatment record for every offer with its terms, its approval and its outcome; a settlement negotiated inside a rule-set range with the gap to the floor shown; a TDR plan whose affordability and installment come from the bank's own calculator and whose band and rule version are on the record; an offer that carries a validity period and returns the case to the state it came from when it lapses; a signature that routes to operations for booking in the same step; a booked plan whose schedule and timers start without a person setting them; a broken plan that returns the case to a decision instead of leaving it in a plan state; and a deed in lieu taken from readiness through transfer to the asset record, with the collateral released and the documents generated on the same path.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-treatment | One deployable with its own API and worker, schema `rwb_treatment`, login, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` and lifecycle | The treatment becomes one owned product with its own release, instead of a screen inside a single deployable |
| The treatment as a governed record | Type, terms, approval reference, booking reference and outcome held once per offer, with the rule version applied | REQ-CHO-006 asks for a record of every offer; a plan without a record cannot be reported or audited |
| The offer as a timer, not a state | The validity period is a durable timer inside TreatmentWorkflow, and expiry returns the case to its prior status | REQ-S2-002; a wait that is a routed state is a case somebody has to remember |
| The plan as a workflow with a schedule | The plan timers and the break rule run in the workflow, started from the first due date | REQ-CHO-007, REQ-S2-009; a missed payment is known the day after it breaks |
| Settlement, deed in lieu and buy-back as three sagas | Each step an activity on the owning service's queue, each pivot confirmed by the central ledger before it executes | Arch v5 slide 26; booking and title transfer are irreversible, so the steps before them must be undoable |
| The treatment as an event | TreatmentApproved and TreatmentClosed on `rwb.treatment.events.v1`, and TreatmentBooked and PaymentMissed consumed from rwb-payment | The case, the customer letter and the payment move on the fact, not on a poll |
| The rules as packages with a version | The restructure, payment-match and booking-match packages evaluated in process, with the package and rule version on every decision | 44% of TDR cases deviate today (R-RES-10); a deviation is only explainable with the version that produced it |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its ingestion of ALS, CCMS and the scheme data, and its backups | REUSE | ACE team |
| The read-only view contract and the freshness of every data product | REUSE, elsewhere | P1 rwb-source-data (this service reads it by contract; GAP-1696; ASM-2849) |
| The ACE restructure calculator and the affordability calculation | REUSE, elsewhere | ACE Common, reached as a Nexus operation in the `ace-collection` namespace (Architecture v5 slide 24) |
| Case record, CMMN state, queues, tasks, allocation and the case timers | REUSE | P3 rwb-case (TreatmentWorkflow is its child workflow) |
| Approval workflow, decision record, hash chain and rule package registry | REUSE | P7 rwb-decision |
| Roles, capability areas, masking policy and the delegation of authority table | REUSE | P4 rwb-access |
| Document metadata, custody, OCR, generation from templates and signatures | REUSE | P5 rwb-document |
| Notices, templates, merge fields, e-signature request and proof of delivery | REUSE | P6 rwb-comms |
| Payment and proceeds matching, booking confirmation, posting files | REUSE | P8 rwb-payment |
| Interface configuration and the ACE integration paths (NLEADS credit pack, ALS booking, CCMS release) | REUSE | P2 rwb-integration |
| Deviation screening, pause and return | REUSE | S8 rwb-deviation |
| Asset record, floor price, take-on and disposal | REUSE | S5 rwb-asset |
| The route decision that starts a treatment | REUSE | S1 rwb-valuation |
| Screens and the composite route that serves them | REUSE | Platform edge, gateway-bff (RWB-PLT-EDGE) |
| Quartz scheduler and its shared timer tables | REPLACED | Durable timers and Schedules through the workflow kit (PLT); ADR-016, DP-10 (GAP-1701; ASM-2854) |
| Embedded Drools with Excel decision tables evaluated in the monolith | MOVED | Governance in P7, evaluation local in this service (ADR-017, DP-04) |
| Booking in the core bank and the credit decision in NLEADS | OUT OF SCOPE | The officer, the core bank and the credit system; this service records the result |
| Collections before day 90 on EFS | OUT OF SCOPE | EFS and the ACE collection module |
| The data lake copy of the treatment record | REMOVED | ADR-018; the reporting copy is P1's dated DP04 copy, read-only (ASM-0080; GAP-1716; ASM-2869) |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-014; slides 37 and 45).
2. The service writes only schema `rwb_treatment`; no cross-schema join and no foreign key into `public` (ADR-014, DP-01).
3. A route service reaches a shared capability through Temporal, never REST; the slide 13 matrix gives this service Temporal calls to rwb-decision, rwb-document and rwb-payment, event subscriptions from rwb-deviation, and one Nexus operation to ACE Common (slides 13, 18 and 24).
4. REST is one hop from gateway-bff with a 2 s timeout, an Idempotency-Key on every POST and RFC 9457 problem details; a GET is retried once with jitter (ADR-020; slides 10 and 11).
5. Events are CloudEvents 1.0 on Kafka with an outbox and an inbox, retry at 1 minute, 10 minutes and 1 hour and then a dead-letter topic; topic `rwb.treatment.events.v1`, key `caseId` (ADR-015, DP-09, DP-14; slides 21 and 22).
6. Temporal namespace `rwb-recovery`, task queue `rwb-treatment`; TreatmentWorkflow is a child of the case workflow and uses Continue-As-New at every stage end and at least every 28 days (ADR-016, DP-10, DP-12; slides 24 and 25).
7. A deal that spans services is a saga: each step a local transaction, a compensating activity before the pivot and a retry until done after it; the settlement and deed in lieu pivots are the debt released once the customer pays and the title transfer registered (slide 26).
8. Rules are versioned data evaluated in process by the embedded Drools kit; authoring, testing and promotion are governed in rwb-decision (ADR-017, DP-04; slides 27 and 28).
9. There is no data lake: treatment measures and reporting read the decision record and the events into rwb-reporting (ADR-018, DP-17).
10. Personal data stays out of events, workflow inputs and logs; masking is by role, using the permission data cached from rwb-access, and each service authorises the object itself (slide 10; NFR-039, NFR-040).
11. The bank scheduler owns only the cross-system edges and signals the business date; it never enters the case journey (slide 32). `AceDataReady` is produced by rwb-source-data and consumed by rwb-case, rwb-payment, rwb-deviation and rwb-writeoff, not by this service (slide 43; GAP-1702; ASM-2855).

# 3. Personas and roles

Roles only; no person is named anywhere in this document (ASM-2873).

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-S2-01 | Restructuring officer (FCR) | A treatment record, the payoff and the range, and an offer to build and send without re-keying | JRN-S2-01, JRN-S2-02, JRN-S2-03 |
| ROL-S2-02 | Case owner | The treatment, its validity and its outcome on the case, and the case returned to the right state when an offer lapses | JRN-S2-01, JRN-S2-03, JRN-S2-04 |
| ROL-S2-03 | Product head (Mortgage, HP, SSME) | A settlement below the floor named to them with the gap, and the limit they are deciding inside | JRN-S2-02 |
| ROL-S2-04 | Credit approval committee member | A plan that states its band, its deviation and the rule version applied | JRN-S2-02, JRN-S2-03 |
| ROL-S2-05 | Restructure operations officer | The booked terms confirmed and the schedule visible | JRN-S2-04 |
| ROL-S2-06 | Sale officer | Deed in lieu readiness, the transfer price against the floor, and the asset taken on | JRN-S2-05 |
| ROL-S2-07 | Legal counsel | Encumbrance and title checks before negotiation, and the document set produced from Legal-approved templates | JRN-S2-05 |
| ROL-S2-08 | Field collector | The inspection, its checklist and its bills recorded against the case the same day | JRN-S2-05 |
| ROL-S2-09 | NPA and asset manager | The auto-unlock outcome, the exceptions summarised, and the buy-back rental running without a person | JRN-S2-05 |
| ROL-S2-10 | Credit Administration | The booked plan and the settled account posted to their systems of record without re-keying | JRN-S2-04 |
| ROL-S2-11 | Team manager | Offers that lapsed, plans that broke and approvals that are overdue, named before they become a complaint | JRN-S2-03, JRN-S2-04, JRN-S2-06 |
| ROL-S2-12 | Compliance and PDPA officer | Masking by role, an access log that cannot be skipped, and a classification on every record | JRN-S2-06 |
| ROL-S2-13 | Internal audit | A treatment reproduced from the log with its rule, package and approver | JRN-S2-06 |
| ROL-S2-14 | Developer | A typed contract to build against, a fake for every dependency, and a build that fails on a direct ACE read | JRN-S2-06 |

Non-human actors: the case workflow that starts TreatmentWorkflow; the approval workflow on rwb-decision; the document service that generates and holds the papers; the communications service that sends the offer; the payment service that books and matches; the outbox relay; the consumers of TreatmentApproved and TreatmentClosed. The customer is reached through the communications service and never by a direct call from this service.

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. The restructure proposal is opened in the collections system, and the officer rebuilds the terms in a Workbench screen so that two records of one offer exist.
2. The payoff and the settlement range are worked out by hand from balances a person reads, so the range and the floor are checked after the offer rather than before.
3. The offer's validity is a date in a note or a tracked spreadsheet; nothing returns the case to its prior state when it lapses.
4. The plan timers are set by hand on a shared scheduler, and a plan booked in the core system is confirmed by a person reading the next file.
5. Deed in lieu readiness is checked late, sometimes after negotiation, and the transfer price, the encumbrance and the title are reconciled at the end.
6. Restructures, settlements and deeds in lieu take 23 to 26 days and are tracked by hand (FSD S2 A1.3); 44% of TDR cases deviate today (R-RES-10).

Consequence: one offer exists in two places, and nobody can say which version the customer accepted.

## 4.2 Target state (this product)

### JRN-S2-01 The treatment opened from the approved route (daily, restructuring officer and case owner)

1. The route decision is approved with route R1 (restructure), R2 (settlement) or R3 (deed in lieu); rwb-case starts TreatmentWorkflow on this service (Arch v5 slides 18 and 25).
2. The treatment record opens with its type from LOV-TREATMENT, its proposer and the decision that approved it.
3. The officer sees the proposal that came from the collections system and confirms the terms; the case does not leave the Workbench.
4. Every limit, threshold and range applied is read from versioned reference data, with the version recorded on the treatment.

### JRN-S2-02 A settlement negotiated inside the range (daily, restructuring officer and product head)

1. The officer sees the payoff as at a date, the range and the floor for the product, and the gap between the offer and the floor.
2. An offer inside the range is built and released; an offer outside the range is routed to credit approval with the reason recorded.
3. An offer below the floor goes to the approver or the committee the delegation table names, with the gap to the floor.
4. The approval, its level, its approver role and the rule version are recorded, and the case moves only on the approval.
5. An approval that is not answered inside its service level escalates to the named role rather than stalling.

### JRN-S2-03 The TDR plan offered (daily, restructuring officer)

1. The case goes to the ACE affordability and plan calculation as a Nexus operation into ACE Common, and the result is recorded against the offer.
2. The service produces the model installment and the range the officer may move within, from the rule and the reference data in force.
3. A plan outside the range or carrying the deviation flag goes to credit approval before the offer leaves.
4. The offer is released to the customer through rwb-comms and its validity period starts as a timer; the wait is not a routed state.
5. The validity period passes without a signature: the case returns to the status it came from, and the offer is recorded as expired.

### JRN-S2-04 The signed offer booked and the plan running (daily, operations officer and Credit Administration)

1. The customer signs inside the validity period; the signature, wet ink or electronic, is on the case.
2. The case routes to operations for booking with the signed offer and the credit approval behind it.
3. rwb-payment books the plan and confirms it from the next ALS load; this service records the booking reference and sets the schedule.
4. The plan timers start from the first due date and the plan moves to running.
5. A due payment does not arrive: rwb-payment publishes PaymentMissed, the break rule counts it, and the case returns to the route decision with the reason recorded. At or above the break limit, the restructure route is barred by rule.

### JRN-S2-05 A deed in lieu taken to the asset record (case by case, sale officer, legal counsel and field collector)

1. Encumbrance, title and eligibility are checked before negotiation; an unresolved encumbrance on a mortgage asset blocks the route and holds the case.
2. The transfer price is agreed; a price below the floor goes for a second signature.
3. The credit approval, contract and mortgage documents are generated from Legal-approved templates and sent for signature.
4. The field inspection is captured with its checklist and bills; the auto-unlock rule runs and the exceptions are summarised for the approver.
5. The asset is taken on by rwb-asset, the debt is settled and the collateral is released, each at its pivot with the ledger confirmation first.
6. Where the customer rents the asset back, the rental, its auto-debit and its receipts run without a person.

### JRN-S2-06 Evidence and measures read later (audit, team manager, developer)

1. An auditor reads one treatment: its type, terms, the rule and package versions applied, the approval with its level and approver, the booking reference and the outcome.
2. The team manager reads the offers that lapsed, the approvals overdue and the plans broken, from the decision record and the events rather than a separate count.
3. A developer builds against the published contract and its fake; a build that reads an ACE view or an ACE table directly fails.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour, and each maps to one FSD feature. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Release | FSD feature |
|---|---|---|---|---|---|---|
| CAP-S2-001 | The treatment record | Every offer has one record with its type, terms, approval reference and outcome | RWB-E2-004; REQ-S2-001 | Must | 2 | FEAT-TRT-01 (A2.1) |
| CAP-S2-002 | Settlement offer inside the range | The officer sees the payoff, the range and the floor before the offer is built, not after | REQ-S2-004 | Must | 3 | FEAT-TRT-02 (A2.2) |
| CAP-S2-003 | Approval below the floor | A settlement below the floor reaches the approver or committee the matrix names, with the gap | REQ-S2-004 | Must | 3 | FEAT-TRT-03 (A2.3) |
| CAP-S2-004 | TDR plan offer | The plan carries its band, its deviation flag and the rule version applied | RWB-E2-004; REQ-S2-001 | Must | 3 | FEAT-TRT-04 (A2.4) |
| CAP-S2-005 | Affordability through ACE | The affordability result is the bank's own calculation, recorded against the offer | REQ-S2-004 | Must | 3 | FEAT-TRT-05 (A2.5) |
| CAP-S2-006 | Plan installment and the range | The officer moves the installment only inside a range the rule set fixes | REQ-S2-004 | Must | 3 | FEAT-TRT-06 (A2.6) |
| CAP-S2-007 | Offer sent with a validity timer | The offer carries its validity, and the wait is a timer rather than a state somebody watches | REQ-S2-002 | Must | 3 | FEAT-TRT-07 (A2.7) |
| CAP-S2-008 | Signed offer routed for booking | A signature inside the validity moves the case to operations in the same step | REQ-S2-003 | Must | 3 | FEAT-TRT-08 (A2.8) |
| CAP-S2-009 | Return on no signature | A decline or an expiry puts the case back where it came from, with the reason | REQ-S2-002; REQ-S2-003 | Must | 3 | FEAT-TRT-09 (A2.9) |
| CAP-S2-010 | Booked plan and its schedule | The booking reference and the schedule are recorded from the payment service's confirmation | REQ-S2-008 | Must | 3 | FEAT-TRT-10 (A2.10) |
| CAP-S2-011 | Broken plan detected and handled | A missed payment returns the case to a decision instead of leaving it in a plan state | REQ-S2-009 | Must | 3 | FEAT-TRT-11 (A2.11) |
| CAP-S2-012 | Deed in lieu to ownership transfer | The deed in lieu runs from offer to transfer as one governed series of steps | REQ-S2-005 | Must | 3 | FEAT-TRT-12 (A2.12) |
| CAP-S2-013 | Encumbrance and eligibility first | The asset is checked for transfer before anybody negotiates on it | REQ-S2-005 | Must | 3 | FEAT-TRT-13 (A2.13) |
| CAP-S2-014 | Asset unlocked as a non performing asset | The qualifying asset moves to the asset list by rule, and the exceptions reach the approver | REQ-S2-007 | Must | 3 | FEAT-TRT-14 (A2.14) |
| CAP-S2-015 | Collateral inspection in the field | The inspection, its checklist and its bills are on the case the same day | REQ-S2-005; RWB-E2-024 | Must | 3 | FEAT-TRT-15 (A2.15) |
| CAP-S2-016 | Deed in lieu buy-back rental | The rental, its auto-debit and its receipt loop run for a standard arrangement | REQ-S2-010 | Should | 4 | FEAT-TRT-16 (A2.16) |
| CAP-S2-017 | Collateral released after settlement | The security is released once the settlement clears, and the release is recorded | REQ-S2-008 | Must | 3 | FEAT-TRT-17 (A2.17) |
| CAP-S2-018 | Treatment document set | The agreement, contract, credit approval and mortgage documents come from approved templates | REQ-S2-006; RWB-E2-026 | Must | 3 | FEAT-TRT-18 (A2.18) |
| CAP-S2-019 | Data date and freshness at the treatment | Every treatment and offer states how old the data behind it is | REQ-S2-001; NFR-013 | Must | 2 | A2.1 to A2.18 (VR-S2-006-1, VR-S2-010-1, VR-S2-011-1, VR-S2-016-1); A2.6 |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Direct read of the ACE collateral, ALS, CCMS and scheme views | Not carried | rwb-source-data's contract (GAP-1696; ASM-2849) |
| Writing the case status back to the collections system | Not carried | The rwb-integration contract (GAP-1697; ASM-2850) |
| Quartz scheduling of the plan timers | Replaced | Durable timers and the plan schedule in TreatmentWorkflow through the workflow kit (GAP-1701; ASM-2854) |
| Booking in the core bank and the ALS/NLEADS writes | Reused, elsewhere | P8 rwb-payment with P2 rwb-integration (GAP-1703; ASM-2856) |
| Document generation, custody and signature capture | Reused, elsewhere | P5 rwb-document and P6 rwb-comms (GAP-1704; ASM-2857) |
| The CCMS release request and the Land Office title check | Reused, elsewhere | P2 rwb-integration for the interface, P1 for the ACE-ingested view (GAP-1705; ASM-2858) |
| The affordability and installment calculation | Reused, elsewhere | The ACE restructure calculator through Nexus (Arch v5 slide 24) |
| The treatment rules as Excel decision tables in the monolith | Moved | Governance in P7 rwb-decision; evaluation local (GAP-1707; ASM-2860) |
| The dated reporting copy of the treatment | Reused, elsewhere | P1 rwb-source-data DP04 copy, read-only (ASM-0080; GAP-1716; ASM-2869) |

# 6. Functional requirements

Every requirement is specific and testable. The FSD requirement column keeps the trace to the source requirement of the module; the BR column keeps the trace to the BRD. The release column is the wave of the slice that carries the requirement (section 10).

| FR ID | Requirement | CAP | BR | FSD REQ | Priority | Release |
|---|---|---|---|---|---|---|
| FR-S2-001 | The service SHALL open one treatment record for the approved route R1 (restructure), R2 (settlement) or R3 (deed in lieu) when rwb-case starts TreatmentWorkflow, and SHALL open no second open treatment for the same start event, which is deduplicated through the inbox. | CAP-S2-001 | RWB-E2-004; REQ-S2-001 | REQ-S2-001 | Must | 2 |
| FR-S2-002 | The service SHALL hold the treatment with the fields of the FSD catalog: the case, the decision that approved it, the treatment type from LOV-TREATMENT, the proposer from LOV-PROPOSER, the time it was proposed, the offer amount in baht, the haircut amount in baht and the number of installments. | CAP-S2-001 | RWB-E2-004; REQ-S2-001 | REQ-S2-001 | Must | 2 |
| FR-S2-003 | The service SHALL link the treatment to the case, the decision and the customer only by business-key columns with no foreign key outside schema `rwb_treatment`, and SHALL hold one schema and one login for its own writes. | CAP-S2-001 | RWB-E2-004; REQ-S2-001 | REQ-S2-001 | Must | 2 |
| FR-S2-004 | The service SHALL obtain every collateral, payoff, affordability, customer and plan-status fact through the rwb-source-data contract. A read of a `recovery.v_ace_*` view, a read of an ACE table, and a constraint in schema `rwb_treatment` that references a table outside it, SHALL fail the build and the boundary test. | CAP-S2-001 | RWB-E2-004; REQ-S2-001 | REQ-S2-001 | Must | 2 |
| FR-S2-005 | The service SHALL refuse the creation, the change, the approval request, the offer release, the booking and the transfer to a role without the capability area, with MSG-P4-002, and SHALL change nothing on a refusal. | CAP-S2-001 | REQ-S2-001 | REQ-S2-001 | Must | 2 |
| FR-S2-006 | The service SHALL write a local decision record for every state change and SHALL publish DecisionRecorded to `rwb.decision-record.v1`; where the record cannot be written the service SHALL change nothing, raise an incident and show MSG-P7-003. | CAP-S2-001 | REQ-S2-001 | REQ-S2-001 | Must | 2 |
| FR-S2-007 | The service SHALL serve the payoff as at a business date, the settlement range and the floor for the product from versioned reference data, and SHALL show the gap between an offer and the floor before the offer can be released. | CAP-S2-002 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-008 | The service SHALL stop an offer outside the range from being released without an approval, SHALL route it to credit approval with the coded reason, and SHALL record the range, the floor and the rule version the test used. | CAP-S2-002 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-009 | The service SHALL record on the settlement the offer amount, the haircut, the payoff date, the floor, the range, the version set in force and the role that built it. | CAP-S2-002 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-010 | The service SHALL route a settlement below the floor to the approver or the committee the delegation table names, through the approval workflow of rwb-decision, and SHALL show the gap to the floor to that approver. | CAP-S2-003 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-011 | The service SHALL record the approval, the rejection or the return of a treatment with the level applied, the approver role, the limit read from the delegation table at the time and the rule version, and SHALL move the case only on an approval. | CAP-S2-003 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-012 | The service SHALL escalate an approval that is not answered inside its service level to the role the delegation table names, and SHALL not treat an unanswered approval as granted. | CAP-S2-003 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-013 | The service SHALL build the TDR plan offer with its band, its installment and the rule version applied, and SHALL record the deviation flag where the offer falls outside the range. | CAP-S2-004 | RWB-E2-004; REQ-S2-001 | REQ-S2-001 | Must | 3 |
| FR-S2-014 | The service SHALL send a plan outside the range or carrying the deviation flag to credit approval before the offer leaves, and SHALL record the reason of the deviation. | CAP-S2-004 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-015 | The service SHALL obtain the affordability assessment and the plan calculation from the ACE restructure calculator as a Nexus operation into ACE Common, SHALL record its result against the offer, and SHALL leave the offer unbuildable where the calculation cannot be obtained. | CAP-S2-005 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-016 | The service SHALL produce the model installment and the range the officer may move within from the rule set and the reference data in force, and SHALL record the rule version and the versions the calculation used. | CAP-S2-006 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-017 | The service SHALL refuse to calculate the payoff or the range on a data product whose freshness cannot be read or whose business date is not the current one, SHALL show the stale product with its date and MSG-P1-001, and SHALL record the business date and load time it used. | CAP-S2-006 | REQ-S2-004 | REQ-S2-004 | Must | 3 |
| FR-S2-018 | The service SHALL release the approved offer to the customer through rwb-comms, which consumes TreatmentApproved, and SHALL start the validity period as a durable timer inside TreatmentWorkflow; no routed state and no scheduler table SHALL hold the wait. | CAP-S2-007 | REQ-S2-002 | REQ-S2-002 | Must | 3 |
| FR-S2-019 | The service SHALL publish TreatmentApproved on `rwb.treatment.events.v1`, keyed by the case, when a treatment is approved for release, and SHALL record the channel, the template version and the validity end with the offer. | CAP-S2-007 | REQ-S2-002 | REQ-S2-002 | Must | 3 |
| FR-S2-020 | The service SHALL route the case to operations for booking when a verified signature is received inside the validity period, wet ink or electronic, and SHALL publish the booking instruction on the path that rwb-payment owns. | CAP-S2-008 | REQ-S2-003 | REQ-S2-003 | Must | 3 |
| FR-S2-021 | The service SHALL refuse to route a signature received after the validity period has passed, SHALL record the late signature and its date, and SHALL leave the case in the return path. | CAP-S2-008 | REQ-S2-003 | REQ-S2-003 | Must | 3 |
| FR-S2-022 | The service SHALL return the case to the status it held before the offer when the customer declines or the validity timer passes, and SHALL record that status, the reason and the time. | CAP-S2-009 | REQ-S2-002; REQ-S2-003 | REQ-S2-002 | Must | 3 |
| FR-S2-023 | The service SHALL record the booking reference from TreatmentBooked on `rwb.payment.events.v1`, SHALL set the payment schedule from the booked terms and SHALL show the booking on the treatment. | CAP-S2-010 | REQ-S2-008 | REQ-S2-008 | Must | 3 |
| FR-S2-024 | The service SHALL start the plan timers as durable timers inside TreatmentWorkflow from the first due date, and SHALL record the schedule, its first due date and the version set it was built from. | CAP-S2-010 | REQ-CHO-007; REQ-S2-008 | REQ-S2-008 | Must | 3 |
| FR-S2-025 | The service SHALL post the booked terms, the settled account and the released collateral to their systems of record through the rwb-payment and rwb-integration contracts without re-keying, and SHALL record the reference each system returned. | CAP-S2-010 | REQ-S2-008; RWB-E2-007 | REQ-S2-008 | Must | 3 |
| FR-S2-026 | The service SHALL count a missed payment received as PaymentMissed on `rwb.payment.events.v1` against the break rule in force, and SHALL mark the plan broken when the cure period has passed with no payment. | CAP-S2-011 | REQ-S2-009; RWB-E2-008 | REQ-S2-009 | Must | 3 |
| FR-S2-027 | The service SHALL return the case to the route decision with the coded reason broken_plan when the break count is below the limit in force, SHALL bar the restructure route at or above it, and SHALL record the break count, the limit and the rule version. | CAP-S2-011 | REQ-S2-009 | REQ-S2-009 | Must | 3 |
| FR-S2-028 | The service SHALL run the deed in lieu as a series of steps that each write their own local transaction, with a compensating step before each pivot and a retry until done after it, and SHALL wait for the central ledger acknowledgement before each pivot executes. | CAP-S2-012 | REQ-S2-005 | REQ-S2-005 | Must | 3 |
| FR-S2-029 | The service SHALL record the deed in lieu agreement with its transfer price, its date and its terms, and SHALL route a transfer price below the floor for a second signature before the deed is put to the customer. | CAP-S2-012 | REQ-S2-005 | REQ-S2-005 | Must | 3 |
| FR-S2-030 | The service SHALL run the encumbrance, title and eligibility checks before negotiation starts, SHALL record the check with its result, its data date and its rule version, and SHALL block the route and hold the case where a mortgage asset has an unresolved encumbrance. | CAP-S2-013 | REQ-S2-005 | REQ-S2-005 | Must | 3 |
| FR-S2-031 | The service SHALL raise a task to recreate the title set before release where the title documents are not found, SHALL name the owner role of that task and SHALL not release the collateral while the task is open. | CAP-S2-013 | REQ-S2-005 | REQ-S2-005 | Must | 3 |
| FR-S2-032 | The service SHALL apply the asset auto-unlock rule after the checklist, the photographs and the bills are captured, SHALL release the asset for transfer where the rule passes, and SHALL summarise the exceptions for the approver where it does not. | CAP-S2-014 | REQ-S2-007 | REQ-S2-007 | Must | 3 |
| FR-S2-033 | The service SHALL request the asset take-on from S5 rwb-asset through its contract once the unlock passes, and SHALL record the asset reference that returns against the treatment. | CAP-S2-014 | REQ-S2-007 | REQ-S2-007 | Must | 3 |
| FR-S2-034 | The service SHALL accept the field inspection, its checklist, its bills and its photographs from the field application through the rwb-document contract, with the location and the time of capture, and SHALL record the inspection against the treatment. | CAP-S2-015 | REQ-S2-005; RWB-E2-024 | REQ-S2-005 | Must | 3 |
| FR-S2-035 | The service SHALL refuse the inspection and the auto-unlock step where a required item of the checklist is missing, SHALL show MSG-GEN-001 naming the field, and SHALL change nothing else on the case. | CAP-S2-015 | REQ-S2-005 | REQ-S2-005 | Must | 3 |
| FR-S2-036 | The service SHALL set up the deed in lieu buy-back rental with its rent, its first due date, its auto-debit instruction and its receipt loop where the customer rents the asset back, and SHALL record the arrears follow-up on the treatment. | CAP-S2-016 | REQ-S2-010 | REQ-S2-010 | Should | 4 |
| FR-S2-037 | The service SHALL create no rental and no auto-debit instruction where the customer does not rent the asset back, and SHALL record that decision on the treatment. | CAP-S2-016 | REQ-S2-010 | REQ-S2-010 | Should | 4 |
| FR-S2-038 | The service SHALL request the collateral release through the rwb-integration contract once the settlement funds have cleared, SHALL record the release reference and its date, and SHALL close the treatment when the installments paid equal the installments due. | CAP-S2-017 | REQ-S2-008 | REQ-S2-008 | Must | 3 |
| FR-S2-039 | The service SHALL reopen the case and record the reversal against the treatment where a payment is reversed after the release, and SHALL restart the steps that the reversal invalidates. | CAP-S2-017 | REQ-S2-008 | REQ-S2-008 | Must | 3 |
| FR-S2-040 | The service SHALL generate the credit approval, the contract and the mortgage documents for the treatment chosen from Legal-approved templates through the rwb-document contract, with the case facts filled and no re-keying, and SHALL record the template and version used. | CAP-S2-018 | REQ-S2-006; RWB-E2-026 | REQ-S2-006 | Must | 3 |
| FR-S2-041 | The service SHALL request the signature of the generated documents on the legal path, wet ink where Legal requires it and electronic where Legal permits it, and SHALL record the signed document and its verification against the treatment; the path that carries the request is open (GAP-1704; ASM-2857). | CAP-S2-018 | REQ-S2-006; RWB-E2-018 | REQ-S2-006 | Must | 3 |
| FR-S2-042 | The service SHALL show the business date and load time of every data product behind a treatment or an offer, SHALL show a stale product with the date it belongs to, and SHALL start no offer, calculation or booking on a data product that cannot be read. | CAP-S2-019 | REQ-S2-001; NFR-013 | REQ-S2-001 | Must | 2 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-S2-001 | The treatment screen, the settlement offer screen and the deed in lieu screen respond inside the user's wait under the busiest-hour load. | Under 2 seconds at the 95th percentile | NFR-008 | Must | Performance test in SIT |
| NFR-S2-002 | The treatment with its documents and its history loads inside the case record target, with 50 documents on the case. | Under 2 seconds | NFR-009 | Must | Performance test with a 50-document case |
| NFR-S2-003 | A rule evaluation at the offer, the range and the break test completes inside the user's wait. | Under 300 milliseconds per evaluation at the 95th percentile | NFR-011 | Must | Rule timing test with the package in force |
| NFR-S2-004 | A TDR offer suggestion from the model gateway answers inside its target; after that the rule result is used and the offer can still be built. | Under 60 seconds, then the rule result | NFR-010, NFR-024 | Could | Agent timeout drill |
| NFR-S2-005 | The service carries the restructure path volume. | About 3,000 restructure accounts a month reach the bank's restructure process | NFR-005 | Must | Volume test at the stated volume |
| NFR-S2-006 | The service carries the deed in lieu volume. | 1,000 cases a month in 2027, from 685 today | NFR-006 | Must | Volume test at the stated volume |
| NFR-S2-007 | The service carries the case inventory and the concurrent load of the programme. | About 23,600 open cases at go-live and 26,500 at the end of 2027; 3,110 new accounts a month; about 370 staff online in the busiest hour; about 21 requests a second in the busiest hour | NFR-001, NFR-002 | Must | Volume and concurrency test |
| NFR-S2-008 | Every treatment, offer and decision states the business date and load time of the data products it read. | Every treatment and offer | NFR-013 | Must | Decision record inspection |
| NFR-S2-009 | A missing, failed or late ACE batch is visible at the treatment and alerts the data steward. | Visible at the treatment; alert to the steward | NFR-014 | Must | Hold an ACE batch in SIT |
| NFR-S2-010 | The service holds no load window, no staging table and no catch-up job: a late ACE batch delays the offer and raises an alert. | No load, no staging, no catch-up | NFR-015 | Must | Hold and release the batch |
| NFR-S2-011 | The service is available during business hours and outside them, when the offer and plan timers run. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-S2-012 | The service inherits the ACE recovery point and recovery time, and a running TreatmentWorkflow resumes where it stopped. | The ACE recovery point objective and recovery time objective; workflow history preserved | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-S2-013 | Every treatment is reproducible from the log, including the rule, package, model and agent versions and the inputs used. | Every treatment reproducible | NFR-033 | Must | Re-run a sample of treatments from the log |
| NFR-S2-014 | Every action carries the rule version applied and the approver who allowed it. | Every action | NFR-034 | Must | Decision record inspection |
| NFR-S2-015 | The decision log hash chain is checked daily and a break is reported to Compliance the same day. | Daily check, same-day report | NFR-035 | Must | Chain break drill |
| NFR-S2-016 | Business measures per treatment are produced from the decision log and not from a separate count. | From the log | NFR-065 | Must | Measure reconciliation to the log |
| NFR-S2-017 | Agent acceptance, override rate, latency and cost are measured and reported per agent where the offer suggestion is used. | Measured per agent | NFR-066 | Should | Agent measure report review |
| NFR-S2-018 | Party identifiers are masked at rest and on every screen and agent call, by role. | Masked at rest and in use | NFR-039 | Must | Masking matrix test across roles |
| NFR-S2-019 | Each screen and each agent receives only the personal data it needs. | Data minimisation per screen and per agent | NFR-040 | Must | Contract review per screen and per agent |
| NFR-S2-020 | Every read of a personal field is logged, and the read is refused rather than returned where the log cannot be written. | Every read | NFR-042 | Must | Access log reconciliation against reads |
| NFR-S2-021 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | NFR-045 | Must | Environment data review |
| NFR-S2-022 | Every record this service holds carries a data classification that sets its handling. | Classification applied per record | NFR-047 | Must | Classification review |
| NFR-S2-023 | Recovery data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | NFR-046 | Must | Tenancy review |
| NFR-S2-024 | Staff authenticate with single sign-on and multi-factor authentication, and agents run under service identities subject to the same role checks. | Entra ID single sign-on with multi-factor; service identities | NFR-049, NFR-051 | Must | Sign-in and identity test |
| NFR-S2-025 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-S2-026 | The build blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency, and every agent output is schema checked with the rule fallback. | Pipeline checks pass; schema check on every agent output | NFR-054, NFR-055 | Must | Pipeline run with a seeded violation; agent output with a bad schema |
| NFR-S2-027 | Screen labels, validation messages and error messages served with this service's operations are available in Thai and in English, and customer documents follow the customer's language. | Every label and message in Thai and English; Thai by default for a customer | NFR-059, NFR-058 | Must | Label and message review |
| NFR-S2-028 | The treatment screens meet the bank's accessibility standard and work on the browsers the bank supports, and the field capture works with no network connection. | WCAG 2.1 level AA; the current and previous major versions of Microsoft Edge and Google Chrome; offline capture | NFR-060, NFR-061, NFR-062 | Must | Accessibility scan, browser test and offline capture test |
| NFR-S2-029 | Logs, traces and metrics are produced for the treatment, the offer, the booking and the plan, every triggered job has a run book, and a failure alerts a named owner. | Every job covered; alert within 15 minutes to the named owner | NFR-064, NFR-067, NFR-068 | Must | Observability review and alert drill |
| NFR-S2-030 | A call is one hop with a 2 s timeout; a failure is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; events that cannot be processed go to the dead-letter topic and are replayed. | One hop; 2 s timeout; three retries then the exception queue; dead-letter with replay | NFR-025, NFR-026 | Must | Failure injection |
| NFR-S2-031 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in schema `rwb_treatment`. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-S2-032 | Legal documents are held write-once for their retention period, retention runs by class, a channel consent is applied on every send, and a failed write to the interaction ledger raises an incident rather than being discarded. | Write-once for legal types; retention class per type; consent applied on every send; no silent ledger gap | NFR-028, NFR-029, NFR-044, NFR-077 | Must | Retention, consent and ledger failure drills |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_treatment`. Every table carries the record columns of the platform library. The Ownership Map lists one table for this service (`treatment`), while Architecture v5 slide 18 and slide 41 give it four entity groups, so the groups are named as the architecture names them and the physical names and field lists are written with the DB story (GAP-1698; ASM-2851; GAP-1712; ASM-2865). Retention is stated by class; the periods are open (GAP-1711; ASM-2864).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `treatment` | Owned record, one per offer per case | `case_id` (uuid), `decision_log_id` (uuid), `treatment_type` (LOV-TREATMENT), `proposed_by` (LOV-PROPOSER), `proposed_at`, `offer_amount`, `haircut_amount`, `installments`, the band, the deviation flag, the approval level and approver role, the outcome, the booking reference, the validity end, the rule and package versions | [SENSITIVE_FINANCIAL] | The officer and the rules; the facts it rests on are read through contracts | Workbench record class; period open |
| `treatment_contract` | Owned record, one per contract of a treatment | Treatment reference, contract reference, the terms, the credit approval reference, the document references held by rwb-document, the signed date | [SENSITIVE_FINANCIAL] | The treatment and rwb-document | Workbench record class; period open |
| `treatment_agreement` | Owned record, one per settlement or deed in lieu agreement | Treatment reference, agreement type, the transfer price or the settlement amount, the haircut, the floor, the second-signature reference, the pivot state and its ledger acknowledgement | [SENSITIVE_FINANCIAL] | The officer and the approval; the value comes from S1 | Workbench record class; period open |
| `plan_timer` | Owned record behind the workflow's timers, one per due date | Treatment reference, the due date, the amount due, the state, the break count and the cure date | [SENSITIVE_FINANCIAL] | The booked terms and rwb-payment | Workbench record class; period open |
| `outbox_event`, `processed_event`, `idempotency_key`, `decision_record` | Platform library objects created in this schema | Library-defined | [CONFIDENTIAL] | Service template | Library policy (PLT; ASM-0074) |

No copy of an ACE column is held, no staging table exists, and no foreign key leaves the schema.

## 8.2 Data read but not owned

| Data | Read through | Views behind it | Classification of the data read |
|---|---|---|---|
| Payoff, balance and plan status | rwb-source-data contract | `v_ace_account`, `v_ace_payment`, the ALS and plan data | [SENSITIVE_FINANCIAL] |
| Collateral, encumbrance and title facts | rwb-source-data contract | `v_ace_collateral`, `v_ace_collateral_detail` | [SENSITIVE_FINANCIAL] |
| Customer and contact facts on the treatment screen | rwb-source-data contract, joined at the edge | `v_ace_customer` | [PII] |
| Freshness of each data product | rwb-source-data contract | `v_ace_batch_status` | [CONFIDENTIAL] |
| Case, party, stage, queue and timers | rwb-case contract (Temporal activity and REST) | none (case schema) | [PII], [SENSITIVE_FINANCIAL] |
| Roles, capability areas, masking policy and the delegation table | rwb-access permission data, cached | none (access schema) | [CONFIDENTIAL] |
| Rule packages and the version in force | rwb-decision contract and events | none (decision schema) | [CONFIDENTIAL] |
| LOV-TREATMENT, LOV-PROPOSER and other reference data | rwb-case reference-data contract | none (case schema) | [CONFIDENTIAL] |
| Documents, signatures and the field extraction | rwb-document contract | none (document schema) | [PII], [CONFIDENTIAL] |
| Payments, matched proceeds and booking confirmation | rwb-payment contract and events | none (payment schema) | [SENSITIVE_FINANCIAL] |
| Deviation and contact-stop state | rwb-deviation events | none (deviation schema) | [CONFIDENTIAL] |
| Asset record, floor price and take-on | rwb-asset contract | none (asset schema) | [SENSITIVE_FINANCIAL] |
| The dated reporting copy of the treatment | rwb-source-data contract, read only | none (`dp_treatment`, P1) | [CONFIDENTIAL] |

Counts are not stated: the FSD gives a field catalog of eight fields and no count for the module, and no count is recomputed here.

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| Offer amount, haircut amount, installments | The terms of the offer, in baht | [SENSITIVE_FINANCIAL] | Read access by role; no financial value in an event, a workflow input or a log |
| Transfer price and floor | The value the deed in lieu runs on | [SENSITIVE_FINANCIAL] | Served on the deed in lieu screen only; the gap to the floor is shown only to the approver |
| Treatment type, proposer, proposed at | The shape of the offer | [CONFIDENTIAL] | Shown on the treatment; drives the rule set applied |
| Case identifier and decision reference | The case and the decision the treatment belongs to | [CONFIDENTIAL] | Carried in events as an identifier only |
| Customer name and identification number, where the treatment screen shows the case party | The party the case belongs to | [PII] | Masked by role; the identification number never leaves in clear; every read logged |
| Contact value, where the offer is sent | How the customer is reached | [PII] | Masked by default, full only where a masking row for the role allows it; the send itself is rwb-comms's |
| Inspection photographs, bills and the auto-debit account | The evidence of the field visit and the rental arrangement | [PII], [CONFIDENTIAL] | Held by rwb-document and rwb-payment; this service holds the reference, not the content |
| Rule, package, model and prompt versions | The material the decision was taken with | [CONFIDENTIAL] | No personal data in the prompt, the output or the log (NFR-040) |

The FSD marks all eight fields of its catalog as not personal data. The party fields reach the screen through the case and source-data contracts and are handled as personal data by this document (GAP-1711; ASM-2864).

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code: the range, the floor, the settlement and DIL limits, the break limit, the cure period, the validity period, the approval limits and the rental terms (BR-S2-001 to BR-S2-018).
2. This service holds no copy of an ACE column and no staging table; it reads ACE data through the source-data contract only (GAP-1696; ASM-2849).
3. A link to an ACE or another service's record is a business-key column with no foreign key.
4. A personal field is not returned when the access log cannot be written.
5. Personal data is not put in an event, a workflow input or a log; TreatmentApproved, TreatmentClosed and DecisionRecorded carry the case, the treatment, the decision and the versions, not the amounts.
6. ACE data is retained by ACE, the archive of a Workbench record belongs to rwb-document, and the dated reporting copy is P1's (ASM-0080).

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-source-data (P1) | Out and in | REST, one hop, 2 s timeout, GET retried once with jitter | P1 | The only path to payoff, collateral, encumbrance, customer and freshness facts. Slide 13 shows no S2 cell to P1, so the path is carried as open (GAP-1696; ASM-2849) |
| ACE database, tables behind the 30 views | Not read | None | ACE team | Read only through the P1 contract. No direct `public` read and no DML from this service |
| rwb-case (P3) | In and out | Temporal child workflow (TreatmentWorkflow) and REST; events listened to | P3 | The case starts the treatment and owns the parent workflow, the queues, the tasks and the timer path |
| rwb-decision (P7) | Out and in | Temporal activity and child workflow (ApprovalWorkflow); events listened to | P7 | Approval routing on the delegation, the decision ledger and the hash chain, rule package governance, RulePackageInForce (EV-30) |
| rwb-access (P4) | In | Cached permission data through the guard library, not a call on the hot path | P4 | Roles, capability areas, masking and the delegation table |
| rwb-document (P5) | Out | Temporal activity | P5 | Document generation from Legal-approved templates, custody, field extraction and signatures |
| rwb-comms (P6) | Out, by event | Event consumed; no direct call is shown in the connection matrix | P6 | The offer and notice dispatch and the e-signature request; TreatmentApproved is consumed by P6 (EV-10). Slide 13 gives this service no cell to P6, so the dispatch is carried on the event and the signature request path is open (GAP-1704; ASM-2857) |
| rwb-payment (P8) | Out and in | Temporal activity; events listened to | P8 | postProceeds and the booking path; TreatmentApproved is consumed by P8; TreatmentBooked (EV-11) and PaymentMissed (EV-12) are consumed here |
| rwb-integration (P2) | Out | REST or an activity per the integration contract | P2 | The NLEADS credit pack, the ALS booking path and the CCMS release request (GAP-1703; ASM-2856) |
| rwb-deviation (S8) | In | Events listened to | S8 | DeviationRaised (EV-06) pauses the stage; DeviationCleared returns it (GAP-1705; ASM-2858) |
| rwb-asset (S5) | Out | REST | S5 | Asset take-on and the asset reference for a deed in lieu; slide 13 shows no S2 cell to S5, so the path is carried as open |
| rwb-valuation (S1) | In | Through rwb-case (the route decision starts the stage) | S1 | The approved route R1, R2 or R3 and the transfer price the deed in lieu runs on |
| ACE Common restructure calculator | Out | Temporal Nexus operation into the `ace-collection` namespace (`restructure.calculate`) | ACE Common | Affordability and plan calculation; the namespaces stay isolated (Arch v5 slides 24 and 26) |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | The treatment record (SCR-14), the settlement offer (SCR-15) and the deed in lieu (SCR-16); the composite route joins this service's answer with rwb-case, rwb-document and rwb-payment |
| Kafka topic `rwb.treatment.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by case | This service | TreatmentApproved (EV-10) and TreatmentClosed; consumers rwb-comms, rwb-payment, rwb-case and rwb-reporting (GAP-1700; ASM-2853) |
| rwb-reporting (P9) | Out, by event | Event listened to | P9 | Treatment measures, lapse and break rates, and the settlement turnaround; rwb-reporting listens to this service's events and reads the decision record, so the measures come from the log and not from a separate count |
| ACE common audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5 (ADR-018); no extract leaves this service |
| Field application | In | Through rwb-document and the edge | P5 with the platform edge | Inspection photographs, bills and checklist, captured offline and uploaded on reconnection (NFR-062) |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Which path carries the payoff, collateral and encumbrance facts, given that slide 13 gives this service no REST cell to rwb-source-data and the FSD names the views directly? | Solution architect with P1 | Every value the offer rests on comes through it (GAP-1696; ASM-2849) |
| Who writes the case status back to the collections system, and is it a P2 interface or an ACE-side path? | Solution architect with the integration lead | A returned case that is not written back is a case two systems disagree about (GAP-1697; ASM-2850) |
| Which of the two offer commands is published: `POST /treatments/{id}/offer` on slide 18 or `POST /treatments/{treatmentId}/submit` in the map, and is there a `GET /treatments` list? | Solution architect | Fixes the gateway route and the screen's client before the screen is built (GAP-1699; ASM-2852) |
| Does the treatment asset take-on reach rwb-asset directly, given that slide 13 shows no S2 cell to S5? | Solution architect with the S5 owner | The asset record is S5's, and a deed in lieu that books the asset twice is a wrong register (GAP-1705; ASM-2858) |
| Do the rental, its auto-debit and its receipts sit here or in rwb-payment, which owns payment and proceeds matching? | Solution architect with the P8 owner | Two writers of one receipt loop leave arrears unattributable (GAP-1703; ASM-2856) |

# 10. Release slicing proposal

The service is created in wave 2 (EP02, release 31 December 2026 (tentative)); the requirements of the module are the E3 release (31 January 2027 (tentative)) (ASM-2871). Each slice is a list of capabilities, not stories.

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library, the Temporal workflow kit with the approval, saga, document and human-task templates, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product. The service wave (2) and the wave of the business epic EP02 (2) are the same, so no wave conflict is raised (ASM-2872); the difference between EP02 and the E3 release of the requirements is a release-sequencing gap (GAP-1709; ASM-2862).

## 10.2 Wave 2 — Epic 2 (release 31 December 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 Published contract and fake | CAP-S2-001 | Every other service that talks to the treatment needs the contract and a fake: rwb-case starts the stage, rwb-payment consumes TreatmentApproved, rwb-document and rwb-comms answer the offer. Contract-first is the only order that lets wave 2 and wave 3 build in parallel |
| 2.2 Treatment record and read path | CAP-S2-001, CAP-S2-019 | Epic 2 asks for a treatment record with its plan timers (RWB-E2-004), and nothing else can be built until the record exists with its data date; the boundary test must fail the build on a direct ACE read from the first story |

## 10.3 Wave 3 — Epic 3 (release 31 January 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 3.1 Settlement inside the range | CAP-S2-002, CAP-S2-003 | The settlement is the offer that carries the most money and the most authority; the range and the floor must be in the path before the offer |
| 3.2 TDR plan, affordability and installment | CAP-S2-004, CAP-S2-005, CAP-S2-006 | A plan built without the bank's own affordability result is an opinion the committee cannot sign |
| 3.3 Offer, validity and return | CAP-S2-007, CAP-S2-009 | The validity period and the return are what stop a lapsed offer becoming a case with no state |
| 3.4 Signature and booking | CAP-S2-008, CAP-S2-010 | A signature that does not book, or a booking that is not confirmed, is the hand-off this release exists to close (E3 theme: settlements and deeds in lieu end to end to booking) |
| 3.5 Broken plan | CAP-S2-011 | A plan that breaks and stays in a plan state is the case the programme exists to remove |
| 3.6 Deed in lieu, readiness and transfer | CAP-S2-012, CAP-S2-013, CAP-S2-014, CAP-S2-015 | The deed in lieu is one chain: readiness, encumbrance, inspection, unlock and transfer; delivered as one slice it can be tested end to end |
| 3.7 Documents and signatures | CAP-S2-018 | The papers are the release condition of the deed in lieu, and the templates are Legal's |
| 3.8 Collateral release | CAP-S2-017 | The release is the last irreversible step of a settlement, and it needs the payment path from 3.4 |

Rationale: the wave-3 slice is the smallest set that delivers the E3 outcome "settlements and deeds in lieu end to end to booking", and each slice is independently demonstrable. CAP-S2-015 is listed inside 3.6 rather than as a slice of its own, because the unlock rule cannot run without the inspection.

## 10.4 Wave 4 and later increments

| Increment | What unlocks it |
|---|---|
| Buy-back rental (CAP-S2-016) | The Should requirement REQ-S2-010 and the rental reach into AMIS and ATS; it is planned after the E3 release and before the E6 partner and fee work |
| TDR offer suggestion from the model gateway | RWB-E2-032 (Could) through the agent contract of P10; the offer is built with the rule result until the model is approved, with the 60 s limit and the schema check (NFR-S2-004, NFR-S2-026) |
| Litigation from a broken settlement | E5: R-LIT-40 resumes litigation when a settlement breaks; the event this service publishes is what starts it |
| Measures at full width | The rwb-reporting read model, fed by the decision record and the events (ADR-018) |
| The S2 table set in the Ownership Map and the physical schema | The data architect's table list, added with the DB story (GAP-1698; ASM-2851) |
| The three rule packages as governed packages | The package codes, version labels and owners in rwb-decision (GAP-1707; ASM-2860) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one; where the source criterion is a placeholder, the evidence names the source step or rule it was written from (GAP-1708; ASM-2861). Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-S2-001 | FR-S2-001, FR-S2-002, FR-S2-003, NFR-S2-005 | a route decision approved for R1, R2 or R3 and a case with no open treatment | rwb-case starts the treatment stage, and the same start event is delivered twice | one treatment exists with its type from LOV-TREATMENT, its proposer, the decision that approved it and its terms; the second delivery adds no treatment; every link is a business-key column with no foreign key | AC-S2-001-01; Arch v5 slides 18, 22 and 25 |
| AC-S2-002 | FR-S2-004, NFR-S2-026 | a branch that reads `recovery.v_ace_collateral` directly and a schema constraint that references an ACE table | the pipeline and the boundary test run | the build fails naming the view read and the cross-schema constraint; the conformance step passes with no ACE object in this schema | Arch v5 slides 37 and 45; GAP-1696; ASM-2849 |
| AC-S2-003 | FR-S2-005, NFR-S2-024 | a user without the capability area, signed in with single sign-on | they try to build an offer and to release it | both actions are refused with MSG-P4-002 and nothing changes on the treatment or the case | AC-EXC-S2-002-01, AC-EXC-S2-007-01; VR-S2-013-1 |
| AC-S2-004 | FR-S2-006, NFR-S2-013, NFR-S2-015 | the decision record store rejects every write | the officer changes the treatment | nothing changes on the case, MSG-P7-003 is shown and an incident is raised; the daily hash-chain check reports the gap the same day | AC-EXC-S2-001-02; NFR-035 |
| AC-S2-005 | FR-S2-007, FR-S2-009 | a payoff as at the business date, a settlement range and a floor in force for the product | the settlement offer screen is opened | the payoff, the range, the floor and the gap to the floor are shown before an offer can be released; the treatment records all four with the version set in force | AC-S2-002-01; FSD S2 A2.2.2 step 1 |
| AC-S2-006 | FR-S2-008, FR-S2-010 | an offer inside the range and a second offer below the floor | each offer is released | the first is released and recorded; the second is stopped, routed to the approver the delegation table names with the gap to the floor, and recorded with the reason and the rule version | AC-S2-003-01; VR-S2-002-1, VR-S2-003-1; R-SET-05 |
| AC-S2-007 | FR-S2-011, FR-S2-012 | an approver inside the limit, and an approval left unanswered past its service level | the approval is granted, and in the second case the service level passes | the treatment records the level applied, the approver role, the limit read at the time and the rule version; the unanswered approval escalates to the named role and is never treated as granted | AC-S2-003-01; REQ-APD-007, REQ-APD-009 |
| AC-S2-008 | FR-S2-013, FR-S2-014 | a TDR plan inside the range, and a second plan carrying the deviation flag | each plan offer is built | the first carries its band, its installment and the rule version; the second carries the flag and the coded reason and is sent to credit approval before it leaves | AC-S2-004-01; R-RES-10 |
| AC-S2-009 | FR-S2-015, NFR-S2-030 | the ACE restructure calculator answers for one case and is unavailable for a second | the affordability step runs | the first records the result against the offer; the second leaves the offer unbuildable, retries on the schedule and then raises a task for a named owner, and nothing is recorded as an affordability result | AC-S2-005-01; Arch v5 slide 24; NFR-026 |
| AC-S2-010 | FR-S2-016, FR-S2-017, NFR-S2-003, NFR-S2-008 | balances of the case, a range in force and one data product dated before the business date | the installment is calculated | the model installment and the range are produced from the rule set with the rule version and the data date recorded; the stale product is shown with its date and MSG-P1-001, and no calculation is served on it | AC-S2-006-01; VR-S2-006-1; NFR-011 |
| AC-S2-011 | FR-S2-018, FR-S2-019, NFR-S2-011 | an approved offer and a running TreatmentWorkflow | the offer is released | TreatmentApproved is in the outbox keyed by the case and reaches rwb-comms and rwb-payment; the validity end is recorded and the wait is a durable timer, not a routed state and not a scheduler table | AC-S2-007-01; EV-10; DP-10 |
| AC-S2-012 | FR-S2-020, FR-S2-021 | a verified signature one day inside the validity period, and a second signature two days after it | each signature is received | the first routes the case to operations for booking with the booking instruction on the payment path; the second is refused, recorded with its date, and the case stays in the return path | AC-S2-008-01; R-RES-16 |
| AC-S2-013 | FR-S2-022 | an offer with no signature and its validity timer passing, and a second case where the customer declines | the timer passes, and the decline arrives | both cases return to the status they held before the offer, and that status, the reason and the time are recorded | AC-S2-009-01; R-RES-17, R-RES-18 |
| AC-S2-014 | FR-S2-023, FR-S2-024, NFR-S2-031 | TreatmentBooked on `rwb.payment.events.v1` with a booking reference and a first due date | the event is consumed | the booking reference, the schedule and the first due date are recorded, the plan timers start as durable timers and the plan moves to running; a rollback redeploys the previous tag and the migration stays in `rwb_treatment` | AC-S2-010-01; EV-11; R-RES-22, R-RES-25 |
| AC-S2-015 | FR-S2-025, FR-S2-038 | booked terms and a settlement whose funds have cleared | the posting step runs | the booked terms and the settled account are posted through the payment and integration contracts with the reference each system returned, and the collateral release reference and its date are recorded; no field is re-keyed | AC-S2-010-01, AC-S2-017-01; REQ-S2-008 |
| AC-S2-016 | FR-S2-026, FR-S2-027, NFR-S2-014 | PaymentMissed for a due installment, the cure period passing, and a break count below then at the limit | the break rule runs | the plan is marked broken with the break count, the limit and the rule version; below the limit the case returns to the route decision with reason broken_plan; at the limit the restructure route is barred | AC-S2-011-01; EV-12; R-RES-29, R-RES-30 |
| AC-S2-017 | FR-S2-028, FR-S2-029 | a deed in lieu at the notification step, and the transfer step failing before the pivot | the saga runs, and a step fails | each step writes its own transaction, the completed steps are compensated before the pivot, the pivot waits for the ledger acknowledgement, and after the pivot the step is retried until it succeeds; a transfer price below the floor needs the second signature before the deed goes to the customer | AC-S2-012-01; Arch v5 slide 26; R-DIL-15 |
| AC-S2-018 | FR-S2-030, FR-S2-031 | a mortgage asset with an unresolved encumbrance, and a second asset whose title documents are not found | the readiness checks run | the first route is blocked and the case is held with the check, its data date and its rule version recorded; the second raises a task to recreate the title set with a named owner role and no release happens while it is open | AC-S2-013-01; R-DIL-04, R-SET-22 |
| AC-S2-019 | FR-S2-032, FR-S2-033, FR-S2-034, FR-S2-035 | a complete inspection and a second with a checklist item missing | the auto-unlock rule runs | the complete case is released for transfer, the asset take-on is requested from rwb-asset and the asset reference recorded; the incomplete case is refused with MSG-GEN-001 naming the field and nothing else changes | AC-S2-014-01, AC-S2-015-01; R-DIL-22, R-DIL-23 |
| AC-S2-020 | FR-S2-036, FR-S2-037 | a customer who rents the asset back and a second who does not | the buy-back is set up | the first has a rental, a first due date, an auto-debit instruction and a receipt loop with the arrears follow-up recorded; the second has none and the decision is recorded | AC-S2-016-01; R-DIL-32 |
| AC-S2-021 | FR-S2-039, NFR-S2-032 | a settlement released, and a payment reversed after the release | the reversal arrives | the case reopens, the reversal is recorded against the treatment and the steps the reversal invalidates restart; no ledger entry is discarded and a failed ledger write raises an incident | AC-S2-017-01; R-SET-23; NFR-077 |
| AC-S2-022 | FR-S2-040, FR-S2-041 | a deed in lieu approved with its transfer price, and templates approved by Legal | the document set is requested | the credit approval, the contract and the mortgage documents are generated from the approved templates with the case facts and no re-keying, the template and version are recorded, and the signature is requested on the legal path with the signed document recorded against the treatment | AC-S2-018-01; R-DIL-14 |
| AC-S2-023 | FR-S2-042, NFR-S2-009, NFR-S2-010 | one data product stale and a second that cannot be read at all | the treatment is opened | the stale product is shown with its date and MSG-P1-001 and the business date and load time used are recorded; with the second unreadable no offer starts, no load and no catch-up job runs, and the data steward is alerted | AC-EXC-S2-006-01; VR-S2-010-1; NFR-014 |
| AC-S2-024 | NFR-S2-001, NFR-S2-002, NFR-S2-007, NFR-S2-028 | the stated case inventory, 370 staff online and the busiest hour | the three treatment screens are exercised | each screen answers under 2 seconds at the 95th percentile, the treatment with 50 documents loads under 2 seconds, the volume test passes at 3,000 restructure accounts and 1,000 deeds in lieu a month, and the accessibility and browser checks pass | NFR-008, NFR-009, NFR-005, NFR-006; Arch v5 slide 41 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| REQ-S2-001 (RWB-E2-004) | CAP-S2-001, CAP-S2-004, CAP-S2-019 | FR-S2-001, FR-S2-002, FR-S2-003, FR-S2-004, FR-S2-005, FR-S2-006, FR-S2-013, FR-S2-042 | NFR-S2-007, NFR-S2-008, NFR-S2-009, NFR-S2-010, NFR-S2-020, NFR-S2-022, NFR-S2-026 | AC-S2-001, AC-S2-002, AC-S2-003, AC-S2-004, AC-S2-023 |
| REQ-S2-002 | CAP-S2-007, CAP-S2-009 | FR-S2-018, FR-S2-019, FR-S2-022 | NFR-S2-011, NFR-S2-012, NFR-S2-029, NFR-S2-030 | AC-S2-011, AC-S2-013 |
| REQ-S2-003 | CAP-S2-008, CAP-S2-009 | FR-S2-020, FR-S2-021, FR-S2-022 | NFR-S2-009, NFR-S2-030 | AC-S2-012 |
| REQ-S2-004 | CAP-S2-002, CAP-S2-003, CAP-S2-005, CAP-S2-006 | FR-S2-007, FR-S2-008, FR-S2-009, FR-S2-010, FR-S2-011, FR-S2-012, FR-S2-014, FR-S2-015, FR-S2-016, FR-S2-017 | NFR-S2-001, NFR-S2-003, NFR-S2-013, NFR-S2-014, NFR-S2-017 | AC-S2-005, AC-S2-006, AC-S2-007, AC-S2-008, AC-S2-009, AC-S2-010 |
| REQ-S2-005 | CAP-S2-012, CAP-S2-013, CAP-S2-015 | FR-S2-028, FR-S2-029, FR-S2-030, FR-S2-031, FR-S2-034, FR-S2-035 | NFR-S2-006, NFR-S2-019, NFR-S2-022, NFR-S2-028 | AC-S2-017, AC-S2-018, AC-S2-019 |
| REQ-S2-006 (RWB-E2-026, RWB-E2-018) | CAP-S2-018 | FR-S2-040, FR-S2-041 | NFR-S2-027, NFR-S2-032 | AC-S2-022 |
| REQ-S2-007 | CAP-S2-014 | FR-S2-032, FR-S2-033 | NFR-S2-018, NFR-S2-022 | AC-S2-019 |
| REQ-S2-008 (RWB-E2-007) | CAP-S2-010, CAP-S2-017 | FR-S2-023, FR-S2-024, FR-S2-025, FR-S2-038, FR-S2-039 | NFR-S2-012, NFR-S2-030, NFR-S2-031, NFR-S2-032 | AC-S2-014, AC-S2-015, AC-S2-021 |
| REQ-S2-009 (RWB-E2-008) | CAP-S2-011 | FR-S2-026, FR-S2-027 | NFR-S2-013, NFR-S2-014, NFR-S2-016 | AC-S2-016 |
| REQ-S2-010 | CAP-S2-016 | FR-S2-036, FR-S2-037 | NFR-S2-032 | AC-S2-020 |
| NFR-013 (data date across the module) | CAP-S2-019 | FR-S2-042, FR-S2-017 | NFR-S2-008, NFR-S2-009, NFR-S2-010 | AC-S2-010, AC-S2-023 |

BR coverage: 10 of the 10 program requirements of this module (REQ-S2-001 to REQ-S2-010) and 11 of the 11 Epic 2 requirements that name this service (RWB-E2-004, RWB-E2-006, RWB-E2-007, RWB-E2-008, RWB-E2-010, RWB-E2-017, RWB-E2-018, RWB-E2-025, RWB-E2-026, RWB-E2-027, RWB-E2-032) are covered by at least one functional requirement. No requirement of this module is left without a functional requirement, and no functional requirement lacks a source requirement (ASM-2874). RWB-E2-006 (credit pack for NLEADS) is carried by FR-S2-011 and FR-S2-040, with P2 as the owner of the pack path; RWB-E2-007 (booking confirmation) by FR-S2-023 and FR-S2-025; RWB-E2-008 (missed payment) by FR-S2-026; RWB-E2-010 (stage 2 data products) and RWB-E2-025 (extraction for the stage 2 and 3 types) by FR-S2-002, FR-S2-034 and FR-S2-040, with P1 and P5 as the owners of the copy and the extraction; RWB-E2-017, RWB-E2-018 and RWB-E2-026 (document generation, e-signature, templates) by FR-S2-040 and FR-S2-041; RWB-E2-027 (payment matching rules) by FR-S2-026; RWB-E2-032 (TDR offer suggestion) by section 10.4 and NFR-S2-004.

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Boundary and conformance test output in system test | FR-S2-004, NFR-S2-026 | Developer with the security administrator |
| Contract test against the source-data contract and its fake | FR-S2-004, FR-S2-007, FR-S2-016, FR-S2-042 | Developer with P1 |
| Treatment record and route start test with a second start attempt | FR-S2-001, FR-S2-002, FR-S2-003 | QA team |
| Settlement range, floor and below-floor approval matrix test | FR-S2-007 to FR-S2-012, NFR-S2-003 | Product head with the QA team |
| Affordability drill: calculator available, slow and unavailable | FR-S2-015, NFR-S2-030 | QA team with the ACE team |
| Offer, validity timer and return drill with an expiry and a decline | FR-S2-018, FR-S2-019, FR-S2-021, FR-S2-022, NFR-S2-011 | QA team |
| Booking confirmation, schedule and plan timer test from TreatmentBooked | FR-S2-023, FR-S2-024, FR-S2-025 | Restructure operations officer with the QA team |
| Broken plan drill across the break limit, including the barred route | FR-S2-026, FR-S2-027, NFR-S2-013 | QA team with the case owner |
| Deed in lieu end-to-end test with a failed step before and after the pivot | FR-S2-028, FR-S2-029, FR-S2-030, FR-S2-031 | Legal counsel with the QA team |
| Inspection, unlock and asset take-on test, including the missing checklist item | FR-S2-032 to FR-S2-035, NFR-S2-028 | Field collector and sale officer with the QA team |
| Document generation and signature test against Legal-approved templates | FR-S2-040, FR-S2-041 | Legal counsel with P5 and P6 |
| Collateral release and payment reversal test | FR-S2-038, FR-S2-039, NFR-S2-032 | Credit Administration with the QA team |
| Reproducibility review of a sample of treatments, and the treatment measures reconciled to the log | NFR-S2-013, NFR-S2-014, NFR-S2-016 | Internal audit with the center of excellence |
| Masking matrix, access log reconciliation and classification review | NFR-S2-018 to NFR-S2-023 | Compliance and PDPA officer |
| Performance, volume and accessibility test at the stated volume | NFR-S2-001, NFR-S2-002, NFR-S2-005, NFR-S2-006, NFR-S2-007, NFR-S2-028 | QA team |

# 12. Open questions

The FSD's open items are carried forward with their IDs where they have one. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-S2-01 | Does this service read payoff, collateral, encumbrance, customer and freshness facts through the source-data contract, and who confirms the contract fields and the freshness response, given that the connection matrix gives this service no cell to rwb-source-data? | Solution architect with P1 | Before wave 3 system test | CAP-S2-001, CAP-S2-002, CAP-S2-006, CAP-S2-013, CAP-S2-019 | GAP-1696; ASM-2849; Arch v5 slides 13, 37 and 45 |
| OQ-S2-02 | Which service writes the case status back to the collections system when an offer lapses, and on which interface? | Solution architect with the integration lead | Before wave 3 system test | CAP-S2-009 | GAP-1697; ASM-2850 |
| OQ-S2-03 | Which tables hold the treatment, the contracts, the settlement and deed in lieu agreements and the plan timers in schema `rwb_treatment`, given that the Ownership Map lists one table? | Data architect | Before the S2 DB story | CAP-S2-001, CAP-S2-012, CAP-S2-017 | GAP-1698; ASM-2851 |
| OQ-S2-04 | Is the offer command published as `POST /treatments/{id}/offer` or as `POST /treatments/{treatmentId}/submit`, and is a `GET /treatments` list part of the contract? | Solution architect | Before the S2 contract story closes | CAP-S2-004, CAP-S2-007 | GAP-1699; ASM-2852 |
| OQ-S2-05 | Does TreatmentClosed get an EV number and a catalogue row, and is rwb-reporting its second consumer? | Solution architect | Before wave 3 system test | CAP-S2-011, CAP-S2-017 | GAP-1700; ASM-2853 |
| OQ-S2-06 | Are the plan timers durable timers inside TreatmentWorkflow, and what replaces the shared Quartz timer check for a plan due date? | Solution architect | Before wave 3 system test | CAP-S2-010, CAP-S2-011 | GAP-1701; ASM-2854; DP-10 |
| OQ-S2-07 | What starts the treatment when no case child is running, given that the FSD's trigger names a completed ACE batch and AceDataReady does not list this service as a consumer? | Solution architect with P1 | Before the S2 contract story closes | CAP-S2-001, CAP-S2-019 | GAP-1702; ASM-2855 |
| OQ-S2-08 | Do the booking confirmation and the payment matching stay with rwb-payment, with this service only consuming TreatmentBooked and PaymentMissed? | Solution architect with the P8 owner | Before wave 3 system test | CAP-S2-010, CAP-S2-011, CAP-S2-016 | GAP-1703; ASM-2856 |
| OQ-S2-09 | Who owns the treatment document set and the signature request: rwb-document and rwb-comms as the architecture fixes, or the document hub as the FSD names it? | Solution architect with the P5 and P6 owners | Before wave 3 system test | CAP-S2-018 | GAP-1704; ASM-2857 |
| OQ-S2-10 | Which path carries the CCMS collateral release and the Land Office title check, and does the asset take-on reach rwb-asset directly? | Solution architect with the integration lead | Before wave 3 system test | CAP-S2-012, CAP-S2-013, CAP-S2-014, CAP-S2-017 | GAP-1705; ASM-2858 |
| OQ-S2-11 | What is each approval level and limit by decision, product and loss, and who is the substitute for each (DL18)? The design quotes two different sets of numbers | Risk with the product heads | Before wave 3 release | CAP-S2-003, CAP-S2-012 | GAP-1706; ASM-2859; DL18 |
| OQ-S2-12 | What are the package codes, version labels and owners of the restructure, payment-match and booking-match packages, and when does each arrive? | Center of excellence analyst with P7 | Before wave 3 release | CAP-S2-002, CAP-S2-006, CAP-S2-010, CAP-S2-011 | GAP-1707; ASM-2860; DP-04 |
| OQ-S2-13 | Which feature codes of other modules are prerequisites of this module in the plan, given that FEAT-CHO-06, FEAT-OCC-07 and the others name no service? | Solution architect | Before the S2 contract story closes | All capabilities | GAP-1713; ASM-2866 |
| OQ-S2-14 | What is the field list of the contract, the settlement and deed in lieu agreement and the plan timer, beyond the eight fields of the FSD catalog? | Data architect | Before the S2 DB story | CAP-S2-001, CAP-S2-012, CAP-S2-017 | GAP-1712; ASM-2865 |
| OQ-S2-15 | Which service owns the wording of MSG-S2-001, and who approves its Thai and English versions with the four messages this service shows (DL10)? | Business analyst, S2 | Before wave 3 release | All messages | GAP-1710; ASM-2863; DL10 |
| OQ-S2-16 | What classification and what retention period apply to the treatment, the agreements and the plan timers (DL26)? | Compliance and PDPA officer | Before wave 3 release | CAP-S2-001, CAP-S2-012 | GAP-1711; ASM-2864; DL26 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (GAP-1714; ASM-2867).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 2 (business outcomes), 5.9 (S2 requirements, REQ-S2-001 to REQ-S2-010), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan incl. E2 and E3 dates), 9 (open decisions incl. DL10, DL18, DL26, DL43), 10.1 and 10.2 (the service epic RWB-SVC-S2, schema and wave) |
| Recovery Workbench Business Requirements Epic 2 v3 | 1 and 2 (epic outcome, benefits), 3 (RWB-E2-004 to RWB-E2-033), 4 (program requirements met), 6 (acceptance), 7 and 7.1 (open decisions and their effect), 8.1 to 8.4 (19 service epics, waves, contract-first), 9 (requirement to service epic traceability) |
| Recovery Workbench FSD S2 TDR, settlement and deed in lieu v3 | Document control, Existing capability check, A1 (scope, features, background, preconditions), A2.1 to A2.18 (functional decomposition with rules, field catalog, roles and acceptance criteria), Requirements served, Screens, Appendix A and B |
| Recovery Workbench Architecture v5 | Slides 3 (the eight routes), 4 (19 modules), 9 to 13 (call types, timeouts, retry, the connection matrix), 14 to 20 (service contracts incl. slide 18), 21 to 26 (Kafka, the event journey, Temporal layers and runtime, the saga in slide 26), 27 (rule governance), 30 (19 schemas), 32 (bank scheduler at the edges), 37 (what changes and why), 41 (service catalogue), 42 and 43 (event catalogue), 44 (job map), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Slides 13 (workflow per stage), 15 (rule governance and versioning), 16 (decision record), 18 (S2 restructure, settlement and deed in lieu: steps, clocks, packages, DoA, pivots), 21 and 27 (sagas) |
| Recovery Workbench Microservice Ownership Map v1 | Services (S2 row), Endpoints (four S2 treatment paths and the P5, P6, P8, P2 paths this service uses), Workflows (TreatmentWorkflow), Events (EV-06, EV-10, EV-11, EV-12, EV-30 and the additional TreatmentClosed row), Jobs (no S2 row; JOB-05 retired, JOB-07, JOB-08 and JOB-11), Tables (treatment; dp_treatment as P1's date copy) and Rulings |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic), 4 (partner access) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R4 (services and naming), R5 (target structure, DP table, wave map, lanes), R7 (fill order), R8 (outputs), R9 (gaps and assumptions) |
