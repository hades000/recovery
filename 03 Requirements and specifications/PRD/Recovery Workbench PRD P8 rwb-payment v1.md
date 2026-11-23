SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD P8 rwb-payment v1
description: Product requirements for the Recovery Workbench payment service (P8 rwb-payment) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.md; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.md; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.md
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P8 Payments and posting v3.md
tsd: _work/msr/extract/Recovery Workbench Technical Specifications by Module v5/Recovery Workbench TSD P8 Payments and posting v2.md
service: P8 rwb-payment
epic: RWB-SVC-P8
wave: 2
decision: D-RCV-60
---

# Recovery Workbench PRD P8 rwb-payment v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD P8 rwb-payment |
| Document ID | P8-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | P8 rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 2 (service created with Epic 2) |
| Business epics | EP02 (Epic 2, wave 2); EP03 (Epic 3, wave 2); EP04 (Epic 4, wave 3); EP06 (Epic 6, wave 4) |
| Schema | `rwb_payment` |
| REST base | `/api/recovery/payment/v1` |
| Topic | `rwb.payment.events.v1` |
| Temporal task queue | `rwb-payment` |
| Java package | `th.co.scb.ace.workbench.recovery.payment` |
| Product owner role | Autonomous Ops for matching (REQ-CHO-009); Business lead for the missed payment event (REQ-CHO-007); Data steward and data product owner for booking confirmation (REQ-CHO-008) |
| Requirement owner role | Product owner with the Credit Administration officer, Finance and CFO delegate, and the reconciliation officer |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), D-RCV-36 (T1 and T2, amended by ADR-017) and ADR-010 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epic 2 v3; Business Requirements Epics 3 to 8 v1; FSD P8 Payments and posting v3; TSD P8 Payments and posting v2; Architecture v5 |
| Upstream requirement IDs | REQ-CHO-007, REQ-CHO-008, REQ-CHO-009; REQ-S2-010; REQ-S4-010; REQ-S5-009; REQ-S6-008; REQ-S7-005, REQ-S7-007; REQ-S9-004; REQ-APD-001; REQ-DRI-001, REQ-DRI-002, REQ-DRI-005, REQ-DRI-007, REQ-DRI-010, REQ-DRI-011; REQ-RDF-009. FSD P8 v3 issues no requirement ID of its own: its "Requirements served" table and its T8 requirement traceability table are empty (GAP-1624; ASM-2760). The program BRD has no P8 requirement section; the requirement IDs above are read from sections 5.3, 5.9, 5.11 and 5.12 to 5.16 as its section 11 states (GAP-1498; ASM-2783) |
| Upstream business requirement IDs | BR-030 (sales proceeds applied), BR-033 (settlement, auction and enforcement proceeds, fees, posting and daily reconciliation), BR-043 (enforcement proceeds), BR-054 (write-off posting, provision release and provision inputs), BR-059 (post charge-off recovery and agency fee), RULE-002 (decision record before any action) |
| Upstream Epic 2 keys | RWB-E2-008 (payment matching with the missed payment event); RWB-E2-027 (payment matching rules with the data team) |
| Upstream acceptance criteria | AC-P8-001-01, AC-ALT-P8-001-01, AC-ALT-P8-001-02, AC-EXC-P8-001-01 to AC-EXC-P8-001-10; AC-P8-002-01, AC-ALT-P8-002-01, AC-ALT-P8-002-02, AC-EXC-P8-002-01 to AC-EXC-P8-002-07; AC-P8-003-01 to AC-P8-011-01 and their exception rows (the main-flow rows of A2.3 to A2.11 carry the placeholder text "Written one epic ahead": GAP-1625; ASM-2761) |
| Upstream business rules | VR-P8-001-1 to VR-P8-011-1 (data product stale, `v_ace_batch_status`); BR-P8-001 to BR-P8-011 (no value a business person may change is written in code); R-RES-26, R-RES-27, R-RES-28; R-SET-14, R-SET-15, R-SET-16, R-SET-17, R-SET-19, R-SET-23, R-SET-24, R-SET-26, R-SET-27; R-UNI-03, R-UNI-39, R-UNI-48; R-WO-37, R-WO-38, R-WO-39 |
| Upstream identifiers preserved | FEAT-PAY-01 to FEAT-PAY-11; JOB-07 and JOB-08; EV-11 TreatmentBooked, EV-12 PaymentMissed, EV-25 ProceedsMatched, EV-26 AceDataReady; SCR-28 Proceeds matching, SCR-29 Posting; LOV-MATCH, LOV-MATCH-TYPE, LOV-PROCEEDS-SRC; DF-FIN-001 to DF-FIN-009; DF-REF-261 to DF-REF-273; MSG-P8-001 and MSG-P8-002 (their wording and channel are open: GAP-1637; ASM-2773), MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-002; INT-02, INT-03, INT-16; API-P8-001, API-P8-002; DL06, DL11, DL26, DL35, DL43 |
| Generated IDs | CAP-P8-001 to CAP-P8-012; FR-P8-001 to FR-P8-032; NFR-P8-001 to NFR-P8-020; AC-P8-001 to AC-P8-024; JRN-P8-01 to JRN-P8-06; ROL-P8-01 to ROL-P8-14; OQ-P8-01 to OQ-P8-12 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD P8 Payments and posting v3 (15 November 2026) and TSD P8 Payments and posting v2 (28 October 2026), realigned to the BRDs v5 / v3 / v1 and to Architecture v5 under D-RCV-60 |
| Approval | None recorded. The approval table in section 13 is deliberately empty; the missing approval is carried as an assumption (GAP-1642; ASM-2778) |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD P8 Payments and posting v3, paired with TSD P8 v2. Its history and its identifier set are carried unchanged; the microservice realignment changes the owner, the trigger, the read path and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD and the TSD |
|---|---|---|
| FSD v1 and v2 | Not specified in the source documents (ASM-2784) | The FSD v3 change note states that everything except the matching trigger and the matching acceptance criteria is unchanged from v2 |
| FSD v3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010): source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. The payment matching acceptance criteria and the matching trigger read `v_ace_payment` and `v_ace_batch_status`. Everything else unchanged from v2 |
| TSD v2 | 28 October 2026 | Payment and posting object definitions (`proceeds`, `payment_match_rule`), the match lists of values, the ALS and GL interfaces (INT-02, INT-03, INT-16), the RBAC matrix for the "Write-off and posting" capability area, and two operations (API-P8-001, API-P8-002) |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, JRN, ROL and OQ identifiers are new. The FSD feature IDs (FEAT-PAY-01 to FEAT-PAY-11), the FSD acceptance criteria IDs (AC-P8-xxx), the business rule IDs (VR-P8-xxx, BR-P8-xxx, R-UNI-xx, R-RES-xx, R-SET-xx, R-WO-xx), the job IDs (JOB-07, JOB-08), the event IDs (EV-11, EV-12, EV-25, EV-26), the screen IDs (SCR-28, SCR-29), the operation IDs (API-P8-001, API-P8-002), the interface IDs (INT-02, INT-03, INT-16), the field IDs (DF-FIN-001 to DF-FIN-009, DF-REF-261 to DF-REF-273), the list-of-values names and the message IDs are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the business requirements and of the non-functional requirements; section 11 states that P8's requirements are carried in sections 5.3 and 5.12 to 5.14, and this PRD also reads section 5.9 for the deed in lieu rental, section 5.11 for enforcement proceeds and section 5.16 for the fee schedule (GAP-1641; ASM-2777) |
| Recovery Workbench Business Requirements Epic 2 v3 | BRD | Source of the Epic 2 requirements this service delivers (RWB-E2-008, RWB-E2-027) and of the wave-2 release |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-030, BR-033, BR-043, BR-054, BR-059 and of the Epic 3, 4 and 6 scope this service serves |
| Recovery Workbench Functional Specifications by Module v6, FSD P8 Payments and posting v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Technical Specifications by Module v5, TSD P8 Payments and posting v2 | TSD | Source of the object and field definitions, the lists of values, the RBAC matrix and the two operations |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, Kafka, Temporal, no data lake, edge and gateway (R-PREC rank 1) |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: task queue, workflow kit, event-started work, the PAYMENT_MATCH and BOOKING_MATCH rule packages evaluated locally (R-PREC rank 2) |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, operation, event, job and workflow |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Batch and Scheduling Design v4 | Design | JOB-07 and JOB-08 as triggers on the ACE batch-complete record for ALS, after JOB-02 |
| Recovery Workbench Business Rules and Routing Logic v4 | Rules | Source of R-RES-26 to R-RES-28, R-SET-14 to R-SET-27, R-UNI-03, R-UNI-39 and R-UNI-48 |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-payment (P8) is the recovery service that turns money received into a matched, posted and reconciled recovery position. It answers four questions on every business date: which receipt pays which plan installment, settlement, fee, sale or lot; which payment is due and did not arrive; which accounting entries follow from the money; and whether what the Workbench matched agrees with the ACE position.

The service owns one record of money received on a case (`proceeds`), one topic (`rwb.payment.events.v1`), one set of matching activities and two operations. It owns no case state, no treatment record and no ledger: a matched or missed payment is reported to the services that hold those facts.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-payment | One deployable with its own API and worker, schema `rwb_payment`, login, topic `rwb.payment.events.v1`, task queue `rwb-payment` and lifecycle | Payment matching becomes one owned contract with its own release, instead of a module inside a single deployable |
| The event-started matching run | JOB-07 (matchPayments) and JOB-08 (confirmBookings) start from AceDataReady for the ALS batch, not from a scheduler entry. The two workflows are named after their activities because no v5 source names them (GAP-1639; ASM-2775) | The run cannot start on data that has not arrived, so a late batch is visible instead of silently matching old money |
| The proceeds record as the one statement of money received | One row per receipt per business date, with its match state, source, amount and posting reference | Every matched caption on every screen and every posting file reads the same row |
| Matching rules as versioned data | Amount tolerance, window before and after, grace days, partial floor and priority held as versioned rows, with the PAYMENT_MATCH rule package registered centrally and evaluated in this service | A policy change does not wait for a code release, and every match states the version it used |
| The missed payment as a published fact | PaymentMissed (EV-12) on the owner's topic, consumed by the case, the treatment plan and communications | A broken plan is known the day after it breaks, not at the next review |
| The posting file as a service output | One posting file per posting run, delivered through rwb-integration, with a manifest and a delivery status | Settlement, sale and write-off postings leave through one logged, retried path |
| The daily money reconciliation | Matched proceeds compared to the ACE position and to the posting the service itself delivered | A recovery that is not matched is a recovery the book does not see |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its backups and ACE ingestion of ALS, GL and the partner feeds | REUSE | ACE team |
| The read-only `recovery.v_ace_*` views, including `v_ace_payment`, `v_ace_account` and `v_ace_batch_status` | REUSE, owned by rwb-source-data and read by this service through its contract | P1 rwb-source-data |
| Sign-in, access check, field masking policy and the delegation of authority table | REUSE | ACE common sign-in; P4 rwb-access; P7 rwb-decision for the delegation table |
| Decision record, audit trail and hash chain | REUSE | P7 rwb-decision through the local decision-record library and topic `rwb.decision-record.v1` |
| Rule package registry, four-eyes approval and effective dating | REUSE | P7 rwb-decision; the PAYMENT_MATCH and BOOKING_MATCH packages are evaluated locally here (ADR-017, DP-04) |
| Case state, plan timers and treatment records | REUSE, elsewhere | P3 rwb-case; S2 rwb-treatment |
| Parameters and reference data (including the matching values) | REUSE, elsewhere | P3 rwb-case (R-PREC default ruling, DP-06, DP-07) |
| File delivery, retry and the interface run log | REUSE, elsewhere | P2 rwb-integration (`deliverFile`) |
| Document generation and notices triggered by a missed payment | REUSE, elsewhere | P5 rwb-document; P6 rwb-comms |
| Reporting, measures and regulatory returns | REUSE, elsewhere | P9 rwb-reporting |
| The `payment_match_rule` table (DF-REF-261 to DF-REF-273) | RETIRED | Retired by D-RCV-36; the values become versioned rows and the logic a rule package (GAP-1628; ASM-2764) |
| A direct read of ALS or a write of a booking into ALS (INT-02, INT-03) | REMOVED | The officer books in ALS; the Workbench reads the booked position back through `v_ace_account` after the next ACE batch (REQ-CHO-008) |
| The monthly inbound GL file load (INT-16) | REMOVED | The ledger is an outside system; the Workbench delivers its postings out and does not take a ledger file in (GAP-1635; ASM-2771) |
| The data quality exception table of the monolith | REMOVED, no replacement table | The orphan is reported on the rwb-source-data reconciliation break list (GAP-1627; ASM-2763) |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; the service writes only schema `rwb_payment` and reads ACE data only through the rwb-source-data contract (ADR-014, DP-01, DP-05).
2. REST is one hop from gateway-bff with a 2 s timeout; anything longer is a workflow (ADR-020, DP-11).
3. Events are CloudEvents on Kafka with outbox and inbox; topic `rwb.payment.events.v1`; retry and `.dlt` topics (ADR-015, DP-09, DP-14).
4. Temporal namespace `rwb-recovery`, task queue `rwb-payment`; JOB-07 and JOB-08 are event-started workflows, and no Quartz table is used (ADR-016, DP-10).
5. The rule registry is central in rwb-decision and the evaluation is local: PAYMENT_MATCH and BOOKING_MATCH are named packages, evaluated inside an activity under 300 ms (ADR-017, DP-04).
6. There is no data lake and no dashboard connection: INT-19 and INT-20 are removed and reporting reads events into rwb-reporting (ADR-018, DP-17).
7. Personal data stays out of events, workflow inputs and logs; the mask is applied by the owning service (Arch v5 slide 45).
8. Dead-letter and replay rules, typed failures and the non-retryable list follow the platform standard (Arch v5 slide 13).
9. The service is created with Epic 2 and grows in Epic 3, Epic 4 and Epic 6; its wave in Architecture v5 is 2 (Arch v5 slides 4 and 38).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-P8-01 | Credit Administration officer (RW-CREDITAD) | Matching that runs without a person, an unmatched list they can clear, the run result and the alert when a run fails | JRN-P8-01, JRN-P8-02 |
| ROL-P8-02 | Reconciliation officer | The daily comparison between what the Workbench matched, what ACE shows and what was posted, with the difference named | JRN-P8-06 |
| ROL-P8-03 | Case owner | The plan position after each receipt, and a missed payment known the day after | JRN-P8-01 |
| ROL-P8-04 | Restructuring officer | Payments matched to the plan installment, and a settlement payment that closes the money side | JRN-P8-01, JRN-P8-03 |
| ROL-P8-05 | Data steward and data product owner | The booked position of an agreed settlement confirmed against its treatment, and the ACE payment data behind every match | JRN-P8-03 |
| ROL-P8-06 | Finance and CFO delegate (RW-FINANCE) | A posting file they can trust, and the provision inputs built from the posted population | JRN-P8-05, JRN-P8-06 |
| ROL-P8-07 | Write-off team member and write-off committee member (RW-WRITEOFF, RW-WOCOMM) | A post charge-off payment applied and recorded as recovery, with the agency fee | JRN-P8-06 |
| ROL-P8-08 | Debt sale officer (RW-DEBTSALE) | Buyer remittance matched to the award | JRN-P8-02 |
| ROL-P8-09 | Sale officer | Auction, broker and asset proceeds matched to the case and applied to the balance | JRN-P8-04 |
| ROL-P8-10 | Litigation officer | Court and legal fees calculated from the schedule, approved where needed and paid | JRN-P8-05 |
| ROL-P8-11 | Center of excellence analyst (RW-COE) | The rule version and the rule ID behind every match, and the unmatched list as a rule gap signal | JRN-P8-02, JRN-P8-06 |
| ROL-P8-12 | Internal auditor (RW-AUDIT) | One reproducible decision record per match, with the inputs and the version | JRN-P8-06 |
| ROL-P8-13 | Platform administrator | The run result, the run monitor, a rerun by business date, and an alert to a named owner | JRN-P8-01, JRN-P8-06 |
| ROL-P8-14 | Developer | A typed contract, an event schema and a fake for each dependency, and a build that fails on a direct ACE read | JRN-P8-06 |

Non-human actors: the bank scheduler (Airflow) and rwb-source-data publishing AceDataReady (EV-26), which starts the matching run; the Temporal worker; the outbox relay; rwb-integration delivering the posting file; rwb-debtsale and rwb-asset calling `postProceeds` as a saga step; the consumers of the published events.

# 4. User journeys

## 4.1 Current state (as built and as specified before this release)

1. Payments are matched to plans and settlements by hand.
2. Broken plans are found late.
3. The matching values sit in a module table (`payment_match_rule`) that the physical schema now records as retired by D-RCV-36.
4. A settlement booking is made by the officer in the core system, and the confirmation is read from the next day's data.
5. The posting to the ledger and its daily reconciliation are described only as features; the FSD background states the current problem in one sentence, that payments are matched to plans and settlements by hand and broken plans are found late.

Consequence: a receipt can be applied to the wrong plan or to none, and the plan that broke is found at the next review rather than the next morning.

## 4.2 Target state (this product)

### JRN-P8-01 Matching, missed payment and the run result (unattended, every business date)

1. ACE completes the ALS batch for a business date and rwb-source-data publishes AceDataReady (EV-26) with the source and the business date.
2. rwb-payment starts the matchPayments activity (JOB-07 as an event-started workflow) and reads the matching version in force.
3. It reads the payments of the business date from `v_ace_payment` through the rwb-source-data contract and applies PAYMENT_MATCH in priority order: exact, window, partial.
4. Each match writes one `proceeds` row with the case, the treatment where one applies, the source, the amount, the received date, the matched-to value and the posting reference, and publishes ProceedsMatched (EV-25).
5. Where an installment's due date plus the grace days in force has passed with no matching payment, it publishes PaymentMissed (EV-12) once for that installment; the case and the plan move under the rules of their owners.
6. It writes the run summary: payments read, matched, unmatched, missed and repeated; a failed run raises an alert to Credit Administration.
7. Nothing is matched for a business date whose ALS batch is not complete, and the stale data is shown with its business date (MSG-P1-001).

### JRN-P8-02 Unmatched receipt cleared by hand (Credit Administration, SCR-28)

1. The officer opens SCR-28 Proceeds matching and filters the list to unmatched receipts.
2. Each row shows the receipt date, the amount, the source, the ACE payment reference and the reason it matched nothing.
3. The officer chooses the case and the account key for a receipt and confirms the match; the service records the decision with the rule gap and publishes ProceedsMatched.
4. A receipt that names an account on no open case is not written as a proceeds row; it is reported as an orphan for the data steward and the ACE team.
5. A receipt that belongs to a lot already sold is remitted to the buyer under the debt sale rules, and the case records it.

### JRN-P8-03 Settlement payment and booking confirmation (SCR-29)

1. A settlement reaches its payment state and the customer pays.
2. The matching run finds the payment against the accepted settlement: the amount equal to the settlement amount clears the money side; a part payment clears it only where an installment plan is agreed; a payment that matches no treatment is unmatched.
3. The service reports the outcome to rwb-treatment, which moves the settlement, and to rwb-case, which records it; this service moves no case state.
4. The officer books the agreed terms in the core system; after the next ACE batch the booking confirmation run (JOB-08, confirmBookings) matches approved treatments to the booked position read from `v_ace_account` and publishes TreatmentBooked (EV-11).
5. A treatment with no booked position raises a task to the officer; a booked position with no treatment is listed for the same officer.

### JRN-P8-04 Proceeds applied and the residual routed (sale, enforcement, auction)

1. Money arrives from an auction, a broker, an enforcement sale or the LED, with its source in LOV-PROCEEDS-SRC.
2. The matching run matches it to the case and writes one proceeds row with the source and the matched-to value.
3. The receipt is applied to the balance in the order the policy holds as versioned data, and the order version is recorded.
4. Proceeds that clear the balance in full are reported so that the case closes and any remaining security is released; a residual is raised to the next decision.
5. Where the residual or the shortfall changes the route, the route decision is reopened by its owner, not by this service.

### JRN-P8-05 Fees, postings and the posting file (Finance, Credit Administration)

1. A fee that arises on the case (partner, court, legal or other charge) is calculated from the fee rows in force, with the schedule version recorded.
2. A fee above the approval limit in the delegation of authority table is routed for approval before it is paid; the approver and the limit are recorded.
3. The officer approves the booking or posting on SCR-29 Posting.
4. The service builds the posting file for the run with one line per posting, a manifest with a count and a checksum, and hands it to rwb-integration for delivery.
5. A delivery that fails after three retries becomes an exception item with a task for a named owner; the interface run is visible to the platform administrator.

### JRN-P8-06 Daily money reconciliation and provision inputs (reconciliation officer, Finance, audit)

1. After the matching run and the posting run, the reconciliation compares the matched proceeds of the business date to the payment position read from `v_ace_payment` and `v_ace_account` and to the posting file the service delivered.
2. Each difference is written as a break with its check, its case, its amount and its reason, and carries an owner role.
3. Zero unexplained variance is the target; a break is worked and closed, never deleted.
4. Finance receives the provision inputs built from the posted population, with the version of the definitions used.
5. An auditor reads one decision record per match with the rule package version, the matching values version and the inputs used.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic. Every capability names the FSD feature it re-expresses.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-P8-001 | Payment matched to the plan installment, with the missed payment raised | A receipt lands on the installment it pays, and a broken plan is known the day after it breaks | REQ-CHO-007, REQ-CHO-009; RWB-E2-008 | Must | 2 | FEAT-PAY-01 (A2.1) |
| CAP-P8-002 | Unmatched receipt held on the exception list and cleared by hand | Money that matches nothing is listed with its reason and cleared by a person, not lost | REQ-CHO-009; RWB-E2-027 | Must | 2 | FEAT-PAY-02 (A2.2) |
| CAP-P8-003 | Settlement payment matched to the treatment | The money side of a settlement closes on the payment, not on a person's note | REQ-CHO-009 | Must | 3 | FEAT-PAY-03 (A2.3) |
| CAP-P8-004 | Auction, broker and enforcement proceeds matched | Sale and enforcement money reaches the right case with its source named | REQ-S4-010, REQ-CHO-009 | Must | 3 | FEAT-PAY-04 (A2.4) |
| CAP-P8-005 | Fees and charges computed from data | Partner, court and legal fees are computed from the schedule in force, with its version | REQ-S9-004, REQ-S7-007 | Must | 3 | FEAT-PAY-05 (A2.5) |
| CAP-P8-006 | Settlement booking confirmed against the core system | The booked position is read back from ACE, and a treatment with no booking is a task | REQ-CHO-008 | Must | 2 | FEAT-PAY-06 (A2.6) |
| CAP-P8-007 | Accounting entries posted to the ledger through a posting file | Settlement, sale and write-off postings leave through one logged, retried path | REQ-S6-008, REQ-S7-005, REQ-DRI-007 | Must | 3 | FEAT-PAY-07 (A2.7) |
| CAP-P8-008 | Provision inputs for Finance | Finance receives the provision inputs from the posted population, not a hand-built sheet | REQ-S7-005, REQ-S7-007; BR-054 | Must | 4 | FEAT-PAY-08 (A2.8) |
| CAP-P8-009 | Deed in lieu rental taken by auto-debit | The monthly rental is collected, receipted and its arrears followed up without a person | REQ-S2-010 | Must | 3 | FEAT-PAY-09 (A2.9) |
| CAP-P8-010 | Proceeds applied to the case balance in the policy order | Every receipt is applied the same way, and the order used is recorded | REQ-S5-009; BR-030 | Must | 3 | FEAT-PAY-10 (A2.10) |
| CAP-P8-011 | Daily reconciliation of money movements | The Workbench position, the ACE position and the posting are compared every day, with the break named | REQ-CHO-009; BR-033 | Must | 3 | FEAT-PAY-11 (A2.11) |
| CAP-P8-012 | Matching values and rule package held as versioned data | A policy change takes effect from its valid-from date with no code release, and every match states the version used | REQ-DRI-010, REQ-DRI-011; RWB-E2-027 | Must | 2 | FEAT-PAY-01, FEAT-PAY-02 (A2.1, A2.2) |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Hold matching rules in the module table `payment_match_rule` (DF-REF-261 to DF-REF-273) | Retired by D-RCV-36 | Versioned parameter and reference rows in rwb-case; the PAYMENT_MATCH rule package in rwb-decision (GAP-1628; ASM-2764) |
| Write a settlement booking into ALS (INT-03 as a write) | Removed | The officer books in ALS; this service reads the booked position back through `v_ace_account` (REQ-CHO-008) |
| Take a monthly inbound GL file (INT-16) | Removed | No ledger file enters the Workbench; the service delivers its postings out (GAP-1635; ASM-2771) |
| Hold the money exception as a data quality exception row of the monolith | Removed, no replacement table | The orphan is reported on the rwb-source-data reconciliation break list (GAP-1627; ASM-2763) |
| Reverse a matched payment and reopen the case (R-SET-23, R-SET-24) | Not in this release | Open question OQ-P8-05; the behaviour is specified nowhere in the FSD (GAP-1632; ASM-2768) |
| Post the decision log to a data lake | Not in this service | No data lake in v5; the decision record goes to rwb-decision (ADR-018, DP-17) |

# 6. Functional requirements

Every requirement is specific and testable. The BR column is the business requirement the product behaviour serves; the FSD trace column names the FSD feature and the source acceptance criterion, because FSD P8 v3 issues no requirement ID of its own (GAP-1624; ASM-2760). Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD trace | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-P8-001 | The service SHALL match each payment of the business date read from `v_ace_payment` to at most one installment, settlement, fee, sale or lot, and SHALL write exactly one `proceeds` row per payment per business date holding the case, the treatment where one applies, the ACE payment reference as a business key, the source, the amount, the received date, the matched-to value and the posting reference. | CAP-P8-001 | REQ-CHO-009 | FEAT-PAY-01; AC-P8-001-01 | Must | 2 |
| FR-P8-002 | The service SHALL match by the ACE payment reference of the payment, and SHALL NOT add a foreign key from `proceeds` to any ACE table or to any other service's schema. | CAP-P8-001 | REQ-CHO-009 | FEAT-PAY-01; AC-P8-001-01 | Must | 2 |
| FR-P8-003 | The service SHALL apply the matching values in force in priority order - exact, window, partial - reading the amount tolerance, the window days before and after, the grace days, the partial floor and the priority from versioned rows, and SHALL record the version in force and the rule ID on every match. | CAP-P8-012 | REQ-DRI-010, REQ-DRI-011; RWB-E2-027 | FEAT-PAY-01, FEAT-PAY-02; A2.1.3.1 | Must | 2 |
| FR-P8-004 | The service SHALL match a payment received inside the window in force to the installment and SHALL mark a payment outside that window as unmatched with a decision record, with no day count, percentage or amount written in code. | CAP-P8-001 | REQ-CHO-009; RWB-E2-027 | FEAT-PAY-01; AC-ALT-P8-001-02, AC-EXC-P8-001-06 | Must | 2 |
| FR-P8-005 | The service SHALL publish PaymentMissed (EV-12) with the treatment, the due date and the amount due once for each installment whose due date plus the grace days in force has passed with no matching payment, and SHALL NOT publish it where a payment inside the window in force matched that installment. | CAP-P8-001 | REQ-CHO-007 | FEAT-PAY-01; AC-ALT-P8-001-01; R-RES-27, R-RES-28 | Must | 2 |
| FR-P8-006 | The service SHALL start no matching run for a business date before AceDataReady reports the ALS batch for that date as complete, SHALL read payments only through the rwb-source-data contract over `v_ace_payment`, and SHALL publish no missed payment for a business date whose batch is incomplete. | CAP-P8-001 | REQ-CHO-009, REQ-RDF-009 | FEAT-PAY-01; AC-EXC-P8-001-03 | Must | 2 |
| FR-P8-007 | The service SHALL treat a rerun of the same business date as a repeat: it SHALL leave one `proceeds` row per payment of that date, SHALL publish no second ProceedsMatched or PaymentMissed for the same key, and SHALL count the repeated event it ignored. | CAP-P8-001 | REQ-CHO-009 | FEAT-PAY-01; AC-EXC-P8-001-04; R-UNI-40 | Must | 2 |
| FR-P8-008 | The service SHALL stop before matching and write no `proceeds` row and no event when no matching value version is in force for the business date, SHALL report MSG-P8-002, and SHALL show the run as failed with an alert to Credit Administration. | CAP-P8-012 | REQ-DRI-010 | FEAT-PAY-02; AC-EXC-P8-001-05 | Must | 2 |
| FR-P8-009 | The service SHALL write the decision record before the `proceeds` row and before the event, and where the decision record cannot be written it SHALL write nothing, report MSG-P7-003, raise an incident, and leave the payment to be matched by the next run of that business date. | CAP-P8-001 | REQ-DRI-001, REQ-DRI-002, REQ-DRI-005; RULE-002 | FEAT-PAY-01; AC-EXC-P8-001-08; R-UNI-39 | Must | 2 |
| FR-P8-010 | The service SHALL write a `proceeds` row with the matched-to value UNMATCHED and no treatment for a payment that matches no installment, settlement, fee, sale or lot, SHALL return it on the unmatched filter of the receipt list, and SHALL report the count in the run summary with MSG-P8-001. | CAP-P8-002 | REQ-CHO-009; RWB-E2-027 | FEAT-PAY-02; AC-EXC-P8-001-01; R-UNI-03 | Must | 2 |
| FR-P8-011 | The service SHALL write no `proceeds` row for a payment whose account is on no open case and SHALL report it as an orphan with the check name "References" for the data steward and the ACE team, never deleting or changing the ACE payment record. | CAP-P8-002 | REQ-CHO-009 | FEAT-PAY-02; AC-EXC-P8-001-02 | Must | 2 |
| FR-P8-012 | The service SHALL provide the manual match operation POST /proceeds/{proceedsId}/match for a receipt with the matched-to value UNMATCHED, holding the case and the account key, answered idempotently on the Idempotency-Key header, SHALL answer a second match of the same receipt with status 409, and SHALL refuse a call without the right with MSG-P4-002. | CAP-P8-002 | REQ-CHO-009 | FEAT-PAY-02; API-P8-002; AC-EXC-P8-001-09; R-SET-27 | Must | 2 |
| FR-P8-013 | The service SHALL provide the receipt list operation GET /proceeds with filters for match state and receipt date range and with paging, scoped to the cases and queues the role allows, and SHALL show for each row the receipt date, the amount, the source, the ACE payment reference, the matched-to value and the case. | CAP-P8-002 | REQ-CHO-009 | FEAT-PAY-02; API-P8-001; SCR-28 | Must | 2 |
| FR-P8-014 | The service SHALL publish TreatmentBooked (EV-11) with the treatment, the booking reference and the business date when an approved treatment resolves to a booked position read from `v_ace_account`, and SHALL raise a task to the officer for a treatment whose booking does not appear in the next completed batch. | CAP-P8-006 | REQ-CHO-008 | FEAT-PAY-06; EV-11; JOB-08 | Must | 2 |
| FR-P8-015 | The service SHALL match a settlement payment to the accepted treatment, SHALL close the money side where the amount received equals the settlement amount in force or where a part payment agrees with an installment plan, SHALL mark it unmatched where no treatment matches, and SHALL hold it on the exception list where the amount differs and no installment plan is agreed. | CAP-P8-003 | REQ-CHO-009 | FEAT-PAY-03; R-SET-14, R-SET-15, R-SET-16, R-SET-26 | Must | 3 |
| FR-P8-016 | The service SHALL report the outcome of a settlement payment to rwb-treatment and rwb-case with the payment, the treatment and the outcome, and SHALL NOT move a case state, a plan state or a settlement state itself. | CAP-P8-003 | REQ-CHO-009 | FEAT-PAY-03; R-SET-17, R-SET-19 | Must | 3 |
| FR-P8-017 | The service SHALL match proceeds from an auction, a broker, an enforcement sale, the LED, an agency, an insurer or a guarantor to the case with its source recorded, and SHALL put money that matches no case, sale or lot on the exception list. | CAP-P8-004 | REQ-S4-010, REQ-CHO-009; BR-043 | FEAT-PAY-04 | Must | 3 |
| FR-P8-018 | The service SHALL apply each receipt to the case balance in the order held as versioned data, SHALL record the order version applied on the proceeds record, and SHALL NOT hold the order, a priority or a percentage in code. | CAP-P8-010 | REQ-S5-009; BR-030 | FEAT-PAY-10 | Must | 3 |
| FR-P8-019 | The service SHALL report to rwb-case and rwb-asset when proceeds clear the balance in full, and SHALL raise a residual as the amount to be decided where the balance is not cleared, so that the case closes or the next decision opens under its owner's rules. | CAP-P8-010 | REQ-S5-009; BR-030 | FEAT-PAY-10; R-UNI-48 | Must | 3 |
| FR-P8-020 | The service SHALL calculate partner, court, legal and other charges from the fee rows in force, SHALL record the schedule version and the fee basis on the fee item, and SHALL write no rate, cap or threshold in code. | CAP-P8-005 | REQ-S9-004, REQ-S7-007 | FEAT-PAY-05, FEAT-LIT-15 | Must | 3 |
| FR-P8-021 | The service SHALL route a fee above the limit in the delegation of authority table for that decision, product and amount to approval through rwb-decision, SHALL pay no fee before the approval is recorded, and SHALL record the approver, the limit and the rule version with the payment. | CAP-P8-005 | REQ-APD-001, REQ-S9-004 | FEAT-PAY-05, FEAT-LIT-15 | Must | 3 |
| FR-P8-022 | The service SHALL read the booked position of an agreed settlement back from `v_ace_account` after the next completed ACE batch, SHALL NOT write a booking, a term or an amount into ALS or into any other system of record, and SHALL record the booked position, the business date it was read on and the treatment it confirms. | CAP-P8-006 | REQ-CHO-008 | FEAT-PAY-06; INT-03 | Must | 2 |
| FR-P8-023 | The service SHALL build one posting file per posting run holding the accounting entries for settlements, sales of assets and write-offs, and SHALL hand it to rwb-integration for delivery with a manifest that states the line count and a checksum. | CAP-P8-007 | REQ-S6-008, REQ-S7-005, REQ-DRI-007 | FEAT-PAY-07; INT-16 | Must | 3 |
| FR-P8-024 | The service SHALL write one posting line per entry with the case, the account key, the entry type, the amount, the value date, the business date and the posting reference, SHALL carry no personal data on a file line, and SHALL log every delivery with its outcome; a delivery that fails after three retries SHALL become an exception item with a task for a named owner. | CAP-P8-007 | REQ-DRI-007 | FEAT-PAY-07 | Must | 3 |
| FR-P8-025 | The service SHALL record the approval of a booking or a posting taken on SCR-29 Posting with the approving role, the limit that applied and the time, SHALL include an approved item in the next posting run, and SHALL show the confirmation returned by the next completed ACE batch against the item. | CAP-P8-007 | REQ-S6-008, REQ-S7-005 | FEAT-PAY-07; SCR-29 | Must | 3 |
| FR-P8-026 | The service SHALL take the monthly rental of a deed in lieu by auto-debit on the due date held in the treatment, SHALL issue the receipt against the case, and SHALL report arrears to rwb-treatment for its follow-up without stopping the arrangement itself. | CAP-P8-009 | REQ-S2-010 | FEAT-PAY-09 | Must | 3 |
| FR-P8-027 | The service SHALL reconcile, for every business date, the matched proceeds to the payment position read from `v_ace_payment` and `v_ace_account` and to the posting file it delivered, by count and by amount, and SHALL write one result per check with its variance. | CAP-P8-011 | REQ-CHO-009; BR-033 | FEAT-PAY-11 | Must | 3 |
| FR-P8-028 | The service SHALL write every difference found by the reconciliation as a break with its check, case, amount and reason, SHALL raise a task to Credit Administration and the reconciliation officer, SHALL treat zero unexplained variance as the target, and SHALL never delete a break. | CAP-P8-011 | REQ-CHO-009; BR-033 | FEAT-PAY-11 | Must | 3 |
| FR-P8-029 | The service SHALL build the provision inputs for Finance from the posted population of the business date, with the definition versions used, and SHALL refuse to publish a set whose posted population does not reconcile. | CAP-P8-008 | REQ-S7-005; BR-054 | FEAT-PAY-08 | Must | 4 |
| FR-P8-030 | The service SHALL apply a payment received after charge-off to the charged-off balance, SHALL record it as post charge-off income and calculate the agency fee due from the contracted schedule, and SHALL report it to rwb-writeoff and rwb-partner for their records. | CAP-P8-008 | REQ-S7-007; BR-059 | FEAT-WOF-15, FEAT-PAY-05; R-WO-37 | Must | 4 |
| FR-P8-031 | The service SHALL refuse to act on a stale data product: it SHALL show the business date and the load time of the payment data it used on every result and screen, and SHALL return MSG-P1-001 naming the product and its date where the ALS batch for the business date is not complete. | CAP-P8-001 | REQ-RDF-009 | FEAT-PAY-01; VR-P8-001-1; NFR-014 | Must | 2 |
| FR-P8-032 | The service SHALL enforce the capability area and right on both operations, SHALL filter every result by the scope of the role, SHALL return MSG-P4-002 and change nothing where the right is missing, and SHALL write the refusal with the role and the operation. | CAP-P8-002 | REQ-CHO-009 | FEAT-PAY-02; AC-EXC-P8-001-09; API-P8-001, API-P8-002 | Must | 2 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and from the BRDs. A target the source does not set is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-P8-001 | The matching run of a business date completes inside the overnight chain that puts work in front of the teams before the working day starts. | Payment matching and booking confirmation complete before 07:00 on the business date of the completed ALS batch, after case creation and allocation (NFR-019, NFR-014) | REQ-CHO-009 | Must | Timed run in SIT on a full business date |
| NFR-P8-002 | The receipt list and the posting list answer inside the user's wait at the busiest-hour load. | Under 2 seconds at the 95th percentile (NFR-008) | REQ-CHO-009 | Must | Performance test in SIT |
| NFR-P8-003 | A match decision completes inside the run's wait, evaluated locally. | Under 300 milliseconds per rule evaluation at the 95th percentile (NFR-011) | REQ-DRI-011 | Must | Rule evaluation profile |
| NFR-P8-004 | The service acts only on a complete, fresh batch and states the business date of the data it used on every result. | No run and no event on an incomplete batch; MSG-P1-001 on a stale product (NFR-013, NFR-014, NFR-015) | REQ-RDF-009 | Must | Hold and release the ALS batch |
| NFR-P8-005 | The service is available during business hours and outside them, when the matching and posting runs happen. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window (NFR-020, NFR-021) | REQ-CHO-009 | Must | Availability read monthly from monitoring |
| NFR-P8-006 | The service inherits the ACE recovery point and recovery time. | The ACE recovery point objective and recovery time objective (NFR-022, NFR-023) | REQ-DRI-007 | Must | Failover and restore test before the first release |
| NFR-P8-007 | Every match, miss, posting and reconciliation result is reproducible from its decision record. | Every decision reproducible, with the rule package version, the matching values version and the inputs used (NFR-033, NFR-034) | REQ-DRI-001, REQ-DRI-002 | Must | Reproduce a sample from the log |
| NFR-P8-008 | The decision log chain is verified, and a break is reported the same day. | Daily check, same-day report (NFR-035). The chain is held and verified by rwb-decision; this service acts on a reported break | REQ-DRI-002 | Must | Chain break drill |
| NFR-P8-009 | No action proceeds unlogged. | Nothing written and nothing published without its decision record (REQ-DRI-005, R-UNI-39) | REQ-DRI-005 | Must | Decision log outage test |
| NFR-P8-010 | Personal data is masked by role, and each consumer receives only the personal data it needs. | Masked at rest and in use; data minimisation per screen and per consumer (NFR-039, NFR-040) | REQ-CHO-009 | Must | Masking matrix test; contract review per consumer |
| NFR-P8-011 | Every read of a personal field on the receipt and posting surfaces is logged. | 100 percent of personal field reads (NFR-042) | REQ-CHO-009 | Must | Access log reconciliation |
| NFR-P8-012 | Data is encrypted at rest and in transit, secrets live in the key store, and the pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Encrypted; no secret in code, configuration or prompt; pipeline checks pass (NFR-052, NFR-053, NFR-054) | REQ-DRI-007 | Must | Security review, secret scan, pipeline run |
| NFR-P8-013 | Staff authenticate with single sign-on and multi-factor authentication; the runs and the model-free rule evaluation use service identities. | Entra ID single sign-on with multi-factor; service identities (NFR-049, NFR-051) | REQ-CHO-009 | Must | Sign-in and identity test |
| NFR-P8-014 | Logs, traces and metrics cover the matching run, the posting run and the reconciliation, and every run has a run book, monitoring and an alert to a named owner within the target. | Every run covered; alert within 15 minutes (NFR-064, NFR-067, NFR-068) | REQ-DRI-007 | Must | Observability review and alert drill |
| NFR-P8-015 | A call is one hop with a 2 s timeout; a failed call is retried on a schedule and after three retries becomes an exception item with a task for a named owner; an event that cannot be processed goes to the dead-letter topic and is replayed. | One hop; 2 s timeout; three retries then the exception queue; dead-letter replay (NFR-025, NFR-026) | REQ-DRI-007 | Must | Failure injection |
| NFR-P8-016 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in its own schema. | Rollback by previous tag; per-service migration (NFR-027) | REQ-DRI-007 | Must | Rollback rehearsal |
| NFR-P8-017 | Labels, validation messages and error messages served with this service's operations are available in Thai and in English. | Every label and message in Thai and English (NFR-059) | REQ-CHO-009 | Must | Label and message review |
| NFR-P8-018 | Workbench data stays in the bank's own cloud tenancy in the agreed region, and every record class carries a classification that sets its handling. | SCB Azure, Southeast Asia; classification applied per record class (NFR-046, NFR-047) | REQ-DRI-007 | Must | Tenancy and classification review |
| NFR-P8-019 | The service carries the receipt volume of a business date at the busy month without degradation of the matching run or the receipt list. | The daily receipt volume of the busiest business date, sized from the programme volume of 3,110 new accounts a month and about 23,600 open cases at go-live (NFR-001); the receipt count itself is not stated in the sources (GAP-1643; ASM-2779) | REQ-CHO-009 | Must | Volume test at the stated volume |
| NFR-P8-020 | Money records are kept by record class for the period the policy sets, and nothing is deleted without a recorded decision. | Record class per record type; retention periods not set (NFR-028, NFR-031; DL26) | REQ-DRI-002 | Must | Retention review with Compliance |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_payment`. Every table carries the seven standard record columns of the platform library. Retention is stated by class; the periods are open (GAP-1642; ASM-2778).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `proceeds` | Transaction (one row per receipt per business date) | `id` (DF-FIN-001); `case_id` (DF-FIN-002); `treatment_id` (DF-FIN-003); the ACE payment reference as a business key of type `varchar(255)` with no foreign key (DF-FIN-004, corrected per GAP-1634; ASM-2770); `source` from LOV-PROCEEDS-SRC (DF-FIN-005); `amount` (DF-FIN-006); `received_date` (DF-FIN-007); `matched_to` from LOV-MATCH (DF-FIN-008); `posting_ref` (DF-FIN-009); the matching values version and the rule ID applied | [SENSITIVE_FINANCIAL] | ACE `v_ace_payment`, read through rwb-source-data, plus the Workbench match | Record class set by Compliance (DL26) |
| `posting_file` | Transaction (one row per posting run and delivery) | Fields: Not specified in the source documents (GAP-1630; ASM-2766). The required content is the run, the business date, the line count, the checksum, the manifest, the delivery outcome and the retry count | [SENSITIVE_FINANCIAL] | Built by this service | Record class set by Compliance (DL26) |
| `reconciliation_result` (this service's own result rows) | Transaction (one row per check per business date) | Check, business date, count and amount on each side, variance, reason, result, owner role. Field list: Not specified in the source documents (GAP-1636; ASM-2772) | [CONFIDENTIAL] | Workbench computation over its own rows and the ACE position | Record class set by Compliance (DL26) |
| `reconciliation_break` | Transaction | Check, business date, case, amount, reason, state, owner role. Field list: Not specified in the source documents (GAP-1636; ASM-2772) | [CONFIDENTIAL] | Workbench computation | Record class set by Compliance (DL26) |
| `outbox_event`, `processed_event` | Library objects created in the service schema | Platform library columns | [CONFIDENTIAL] | Platform library, owned by RWB-PLT-EVT and RWB-PLT-LIB | Platform retention |

Not carried: `payment_match_rule` (DF-REF-261 to DF-REF-273). It is retired by D-RCV-36; the values live as versioned parameter and reference rows in rwb-case and the logic as the PAYMENT_MATCH rule package in rwb-decision (GAP-1628; ASM-2764).

## 8.2 Data read but not owned

| Data | Owner | Classification of the data read | How it is reached |
|---|---|---|---|
| `v_ace_payment` (payments, payment code, amount, date) | P1 rwb-source-data (view); ACE team (table) | [SENSITIVE_FINANCIAL] | REST or Temporal activity of rwb-source-data over the view contract (DP-05) |
| `v_ace_account` (balance, arrears, booked position) | P1 rwb-source-data; ACE team | [SENSITIVE_FINANCIAL] | rwb-source-data contract |
| `v_ace_batch_status` (batch and business date) | P1 rwb-source-data; ACE team | [CONFIDENTIAL] | AceDataReady (EV-26) and the freshness stamp of the data product |
| Case, treatment, plan and timer facts | P3 rwb-case; S2 rwb-treatment | [SENSITIVE_FINANCIAL] | Their published contracts |
| Matching values in force (tolerance, window, grace, partial floor, priority) | P3 rwb-case (parameters and reference data; R-PREC default ruling, DP-06, DP-07) | [CONFIDENTIAL] | Parameters and reference-data contract |
| PAYMENT_MATCH and BOOKING_MATCH rule package and version | P7 rwb-decision | [CONFIDENTIAL] | Rule-package registry, verified by checksum (ADR-017, DP-04) |
| Delegation of authority limit for a fee approval | P7 rwb-decision (table); P4 rwb-access (authority matrix) | [CONFIDENTIAL] | Their published contracts |
| Fee rows in force | Not specified in the source documents (GAP-1633; ASM-2769) | [SENSITIVE_FINANCIAL] | Versioned rows, owner to be confirmed |
| Decision record and its chain | P7 rwb-decision | [CONFIDENTIAL] | Local decision-record library and topic `rwb.decision-record.v1` |

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| `proceeds.amount`, `proceeds.received_date` | Amount and date of money received | [SENSITIVE_FINANCIAL] | Read access by role; no amount on an event |
| `proceeds.case_id`, `proceeds.treatment_id` | The case and the treatment the money belongs to | [CONFIDENTIAL] | Identifiers only; no customer fact is copied into this schema |
| `proceeds.source`, `proceeds.matched_to`, `proceeds.posting_ref` | Where the money came from, what it paid, and the posting it produced | [SENSITIVE_FINANCIAL] | Read access by role |
| the ACE payment reference on `proceeds` | Business key of the ACE payment, used for matching | [SENSITIVE_FINANCIAL] | A business-key string with no foreign key; never used to read an ACE table directly |
| Customer identity, name, national number | Held by ACE and by the case store | [PII] | Not copied into `rwb_payment`; a screen that shows a customer name reads it through the case contract, masked by role (NFR-039, NFR-040) |
| Posting file lines | Case, account key, entry type, amount, value date, business date, posting reference | [SENSITIVE_FINANCIAL] | No personal data on a file line; the file travels through rwb-integration with a manifest and a checksum |

## 8.4 Data rules

1. No value a business person may change (tolerance, window, grace days, partial floor, priority, fee rate, application order) is written in code; each is a versioned row read at run time (BR-P8-001 to BR-P8-011, principle 1).
2. The link from `proceeds` to an ACE payment is a business-key column with no foreign key, and no statement in `rwb_payment` reads a `public` table or another service's schema (DP-01, DP-05).
3. One receipt of one business date produces one `proceeds` row; a rerun replaces nothing and duplicates nothing (R-UNI-40).
4. A decision record is written before the row and before the event; a failed write means no row and no event (REQ-DRI-005).
5. No personal data appears on an event payload, a workflow input or a log line; a published event carries identifiers, amounts, dates and the rule version only (Arch v5 slide 45, DP-09).
6. A money record is never deleted; a correction is a new record that names the one it corrects (REQ-DRI-002).

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-source-data (P1) | In | Kafka event AceDataReady (EV-26) and Temporal activity for payments of a business date | P1 | The matching run starts on the event; the payment facts are read through the contract, never from a view of another service |
| rwb-source-data (P1) | Out | REST or activity: orphan business keys and freshness facts | P1 | An unmatched payment on an account with no open case is reported as an orphan (GAP-1627; ASM-2763) |
| rwb-case (P3) | In | Parameter and reference-data contract for the matching values, and the case scope of a role | P3 | Cached read; a value change takes effect from its valid-from date (DP-06, DP-07) |
| rwb-case (P3) | Out | REST and events: ProceedsMatched, PaymentMissed, and the case facts of the receipt | P3 | The case state moves under the rules of rwb-case, not here |
| rwb-treatment (S2) | In | Kafka events TreatmentApproved (EV-10) and the treatment and plan facts of a receipt | S2 | A settlement payment closes the money side and is reported back |
| rwb-treatment (S2) | Out | Kafka events and REST: the payment outcome and the rental arrears of a deed in lieu | S2 | Plan timers and the cure period belong to rwb-treatment |
| rwb-asset (S5) | In | Kafka event AssetSold and the asset proceeds of a case | S5 | Proceeds are applied to the balance and the residual is raised |
| rwb-debtsale (S6) | In and out | Kafka event LotAwarded (EV-23); Temporal activity `postProceeds` called as a saga step | S6 | `postProceeds` is this service's activity on the task queue `rwb-payment`; the buyer remittance is matched to the award |
| rwb-writeoff (S7) | In and out | Kafka event WriteOffApproved (EV-24); ProceedsMatched back to the write-off service | S7 | A post charge-off payment is applied and recorded as income |
| rwb-guarantee (S3) | Out | Kafka event ProceedsMatched | S3 | A guarantee payment clears the balance and closes the money side |
| rwb-decision (P7) | In | Rule-package registry (GET of the model and its checksum) and the delegation of authority table | P7 | PAYMENT_MATCH and BOOKING_MATCH are evaluated locally; the registry is the only source of a package (ADR-017, DP-04) |
| rwb-decision (P7) | Out | Kafka topic `rwb.decision-record.v1` through the local decision-record library | P7 | One record per match, miss, posting and reconciliation result |
| rwb-access (P4) | In | REST, cached: authorise, role scope and field masking policy | P4 | A denied right returns MSG-P4-002 and is recorded |
| rwb-integration (P2) | Out | Temporal activity `deliverFile` with the posting file and its manifest | P2 | Delivery is logged, retried and moved to the exception queue after three retries (REQ-DRI-007) |
| gateway-bff and the edge | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | SCR-28 Proceeds matching and SCR-29 Posting are served over this service's two operations |
| rwb-comms (P6) | Out | Kafka event PaymentMissed (EV-12) | P6 | The notice path of a missed payment is rwb-comms's |
| rwb-reporting (P9) | Out | Kafka events through the read model | P9 | Receipts matched, unmatched and posted are reported from events, not from a second count |
| Kafka topic `rwb.payment.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and `.dlt` topics, keyed by case | This service | TreatmentBooked (EV-11), PaymentMissed (EV-12), ProceedsMatched (EV-25) |
| ALS (core bank) | None | No direct call | ACE team | Read back through `v_ace_account` after the next completed ACE batch; the officer books in ALS (REQ-CHO-008) |
| General ledger | Out only | File through rwb-integration | Outside the 19 services; delivery by P2 | The Workbench does not take a ledger file in (GAP-1635; ASM-2771) |
| ATS and AMIS (auto-debit path) | Not specified in the source documents (GAP-1631; ASM-2767) | No interface in the v5 catalogue | Not specified in the source documents (GAP-1631; ASM-2767) | The deed in lieu rental needs a debiting route; open question OQ-P8-06 |
| LED portal (enforcement proceeds) | Not specified in the source documents (GAP-1631; ASM-2767) | No interface in the v5 catalogue | Not specified in the source documents (GAP-1631; ASM-2767) | The LED proceeds are expected to arrive as ACE data; open question OQ-P8-07 |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Which path carries the manual match and the receipt list: the two operations of the API Specification (GET /proceeds and POST /proceeds/{proceedsId}/match) or the two named in Architecture v5 slide 17 (GET /cases/{id}/payments and POST /proceeds/{id}/allocate)? | Solution architect | The published contract, the screen route and the story split all follow the answer (GAP-1626; ASM-2762) |
| Is a payment received inside the day a named same-day trigger (DL06), and if so, on which interface, given that ACE has no real-time feed today? | Solution architect with the ACE team | Decides whether the matching run stays once per business date (GAP-1640; ASM-2776) |
| Which service and which file layout carry the ledger posting, and what does the ledger return as confirmation? | Solution architect with Finance | The posting file content and the confirmation path are unset (GAP-1630; ASM-2766) |
| Who calls `postProceeds` inside the debt sale saga, in which order, and what compensation applies when the posting fails? | Solution architect with S6 | The saga step is named in Architecture v5 and its contract is not published |

# 10. Release slicing proposal

The service is created in wave 2 with Epic 2: it is the second wave of the programme, releasing on 31 December 2026 (tentative). Each slice is a list of capabilities, not stories. Release dates are copied unchanged from the programme release plan and marked tentative (U7, DL48).

## 10.1 Wave 0 - platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library, the Temporal workflow kit, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Wave 2 - Epic 2 and Epic 3 (release 31 December 2026 and 31 January 2027, both tentative)

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 Matching and the missed payment | CAP-P8-001 | This is the Epic 2 promise on this service: a payment lands on its installment and a broken plan is known the day after (RWB-E2-008) |
| 2.2 Matching values and the rule package | CAP-P8-012 | The values must be data before the first match runs, and the version must be recorded from the first decision (RWB-E2-027) |
| 2.3 Unmatched list and manual match | CAP-P8-002 | Money that matches nothing needs a place to go on the same release that starts matching it |
| 2.4 Booking confirmation | CAP-P8-006 | Epic 3 delivers a settlement end to end to booking, so the booked position must be read back in the same release (GAP-1629; ASM-2765) |

Rationale: the wave-2 slice is the smallest set that delivers the Epic 2 outcome plus the Epic 3 booking read-back for this service. Both legacy stories that name this service (RWB-E2-008 and RWB-E2-027) land here; they are split as rework and carry the contract-first order of the run rules.

## 10.3 Wave 3 - Epic 4 (release 28 February 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 3.1 Settlement payment | CAP-P8-003 | A settlement that is signed and booked must close its money side inside the same release |
| 3.2 Sale and enforcement proceeds | CAP-P8-004, CAP-P8-010 | Auction, broker and enforcement money reaches the case, is applied in one order, and the residual is raised (BR-030, BR-043) |
| 3.3 Fees | CAP-P8-005 | Court, legal and partner fees are paid through an approved path, not by hand |
| 3.4 Posting and the posting file | CAP-P8-007 | The accounting entries of settlements, sales and write-offs leave through one logged path (REQ-S6-008, REQ-S7-005) |
| 3.5 Deed in lieu rental | CAP-P8-009 | The rental auto-debit is a customer-facing commitment of the deed in lieu route (REQ-S2-010) |
| 3.6 Daily money reconciliation | CAP-P8-011 | The comparison is only meaningful once settlement, sale and write-off postings exist (BR-033) |

Rationale: Epic 4 is the route decision release; every route that produces money needs its matching, its posting and its daily reconciliation inside that release, otherwise the recovery is not visible to the book.

## 10.4 Wave 4 - Epic 6 (release 30 April 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 4.1 Provision inputs and post charge-off recovery | CAP-P8-008 | Provision inputs follow the posted write-off population, and post charge-off recovery follows charge-off (BR-054, BR-059) |

Rationale: the write-off release is the first that posts a population to the ledger; the provision inputs and the post charge-off recovery can only be built once that population exists.

## 10.5 Later increments

| Increment | What unlocks it |
|---|---|
| Payment reversal and the case reopen (R-SET-23, R-SET-24) | A product decision that the reversal is in scope, and its written behaviour (OQ-P8-05; GAP-1632) |
| A same-day payment trigger | A real-time or intraday feed named under DL06 (OQ-P8-02; GAP-1640) |
| The ledger confirmation loop at line level | A ledger return interface and its reconciliation rule (GAP-1630) |
| Fee tables in force with their owner | The fee table, its owner and its schedule agreed (GAP-1633) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one; where the source carries only the placeholder row, the criterion is written here and marked as a new one for this PRD. Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-P8-001 | FR-P8-001, FR-P8-002, FR-P8-031 | `v_ace_payment` for business date 2026-12-14 holds payment "PAY-90001" of 12,500.00 THB on account "A-0555" dated 2026-12-14, and the ALS batch for that date is complete | JOB-07 runs on 2026-12-15 | a `proceeds` row exists for case "RC-2026-000555" with treatment "T-0701", source "CUSTOMER", amount 12,500.00, matched-to "INSTALLMENT" and the ACE payment reference as a business key; ProceedsMatched is in the outbox; the row states the business date and the matching values version applied; no foreign key exists from `proceeds` to an ACE table | AC-P8-001-01 |
| AC-P8-002 | FR-P8-003, FR-P8-004 | the matching values version "PM-2026.12" is in force, with priorities 1 to 3 and a window that admits a payment 10 days before its due date and refuses one 11 days before | the matching run reads the values and reports the version on every row | each match carries the version and the rule ID; a payment 10 days before the due date is matched to "INSTALLMENT" and one 11 days before is "UNMATCHED" with a decision record; no day count appears in code | AC-ALT-P8-001-02, AC-EXC-P8-001-06 |
| AC-P8-003 | FR-P8-003, FR-P8-008 | a parameter file for version "PM-2027.02" gives rows "WINDOW" and "PARTIAL" the same priority and sets the tolerance to 120 | the file is loaded and the next run starts | the load is refused whole with status 422 and MSG-GEN-002 naming "amount_tolerance_pct", 0 and 100; "PM-2026.12" stays in force; the run does not use the refused version | AC-EXC-P8-001-07 |
| AC-P8-004 | FR-P8-005 | no payment on account "A-0555" appears in `v_ace_payment` between 2026-12-05 and 2026-12-15, and the grace days in force are passed | JOB-07 runs on 2026-12-16 for business date 2026-12-15 | PaymentMissed is in the outbox once with treatment "T-0701", due date 2026-12-15 and amount due 12,500.00; rwb-case and rwb-treatment consume it; a second run of the same date publishes no second event | AC-ALT-P8-001-01 |
| AC-P8-005 | FR-P8-006, FR-P8-031, NFR-P8-004 | the ALS batch for business date 2026-12-15 is not complete in the batch record | the scheduled time for JOB-07 on 2026-12-16 passes | JOB-07 does not run for 2026-12-15; no PaymentMissed is written for due date 2026-12-15; the screen shows MSG-P1-001 naming "DP01 Account and arrears" and 2026-12-14 | AC-EXC-P8-001-03 |
| AC-P8-006 | FR-P8-007 | JOB-07 completed for business date 2026-12-14 with 1 matched and 1 unmatched payment | JOB-07 is rerun for 2026-12-14 | the `proceeds` table still holds 2 rows for that date; no second ProceedsMatched and no second PaymentMissed is written; the repeat is counted on the run summary | AC-EXC-P8-001-04 |
| AC-P8-007 | FR-P8-003, FR-P8-008 | no matching values version is in force for 2026-12-15 | JOB-07 starts for 2026-12-15 | it stops before matching with MSG-P8-002; no `proceeds` row and no event is written; the run monitor shows JOB-07 failed with an alert to Credit Administration | AC-EXC-P8-001-05 |
| AC-P8-008 | FR-P8-009, NFR-P8-007, NFR-P8-009 | the decision log store is unavailable during the run of 2026-12-15 | "PAY-91001" is matched | no `proceeds` row is written for "PAY-91001"; the run summary shows MSG-P7-003 for it; an incident is raised under R-UNI-39; the next run for 2026-12-14 matches it | AC-EXC-P8-001-08 |
| AC-P8-009 | FR-P8-010, FR-P8-013 | `v_ace_payment` for 2026-12-14 holds payment "PAY-90002" of 3,000.00 THB on account "A-0555", which pays no installment | JOB-07 runs on 2026-12-15 | a `proceeds` row exists for "PAY-90002" with matched-to "UNMATCHED" and no treatment; the unmatched filter of the receipt list returns it; the run summary shows MSG-P8-001 with 1 unmatched payment for 2026-12-14 | AC-EXC-P8-001-01 |
| AC-P8-010 | FR-P8-011 | `v_ace_payment` holds payment "PAY-90003" on account "A-0999" that is on no open case | JOB-07 runs on 2026-12-15 | no `proceeds` row is written for "PAY-90003"; it is reported as an orphan with the check name "References" for the data steward and the ACE team; the ACE payment record is unchanged | AC-EXC-P8-001-02; GAP-1627; ASM-2763 |
| AC-P8-011 | FR-P8-012, FR-P8-032 | an unmatched receipt exists and two users act: one with the update right in the capability area, one without | both call POST /proceeds/{proceedsId}/match with the same Idempotency-Key | the first call matches the receipt and publishes ProceedsMatched; the repeat with the same key changes nothing and returns the same answer; the call without the right is refused with MSG-P4-002, nothing changes, and the refusal is recorded | AC-EXC-P8-001-09; API-P8-002 |
| AC-P8-012 | FR-P8-013, NFR-P8-002, NFR-P8-011 | 3 receipts of a business date, one matched, one unmatched and one on a case outside the role's scope | the officer opens SCR-28 with the matched filter set to false | one row is returned with its receipt date, amount, source, payment reference, matched-to value and case; the out-of-scope row is absent; the read of a personal field on the row writes one access log entry | FSD SCR-28; GAP-1624; ASM-2760 |
| AC-P8-013 | FR-P8-014, FR-P8-022 | an approved settlement treatment has no booked position in `v_ace_account`, and a second treatment has one | JOB-08 runs after the next completed ALS batch | TreatmentBooked is published for the booked treatment with its booking reference and business date; the officer receives a task for the other; the run wrote nothing into ALS | AC-P8-006-01; GAP-1629; ASM-2765 |
| AC-P8-014 | FR-P8-015, FR-P8-016 | three settlement payments: one equal to the settlement amount, one part payment against an agreed installment plan, and one that matches no treatment | the matching run reads them | the first closes the money side with matched-to "SETTLEMENT"; the second is recorded against the plan; the third is written as "UNMATCHED" and reported to rwb-treatment and rwb-case; no case state changed inside this service | AC-P8-003-01; R-SET-14, R-SET-15, R-SET-16, R-SET-26 |
| AC-P8-015 | FR-P8-017 | an auction payment, a broker payment and an LED enforcement payment for one case, and one payment that matches no case | the matching run reads them | each is written with its own source from LOV-PROCEEDS-SRC and matched to the case; the fourth goes to the exception list; ProceedsMatched names the case and the amount and carries no personal data | AC-P8-004-01; BR-043; R-UNI-03 |
| AC-P8-016 | FR-P8-018, FR-P8-019 | two receipts on one case, one that clears the balance in full and one that leaves a residual | the apply step runs for both | each receipt is applied in the order of the version in force and the order version is on the row; the clearing receipt is reported so the case can close and remaining security be released; the residual is raised as the amount to be decided | AC-P8-010-01; R-UNI-48 |
| AC-P8-017 | FR-P8-020, FR-P8-021 | a court fee inside the limit in force and a partner fee above it | the fees are calculated and one is approved and one is not | each fee carries the basis and the schedule version; the fee inside the limit is paid; the fee above the limit is not paid until the approval is recorded, and the approver, the limit and the rule version are on the item | AC-P8-005-01; GAP-1633; ASM-2769 |
| AC-P8-018 | FR-P8-023, FR-P8-024, NFR-P8-015 | a posting run with three entries; rwb-integration is unavailable for the first three attempts | the run builds the file and hands it over | the file holds one line per entry with case, account key, entry type, amount, value date, business date and posting reference, and no personal data; the manifest states the line count and checksum; after three failed attempts an exception item exists with a task for a named owner; the interface run is visible | AC-P8-007-01; GAP-1630; ASM-2766 |
| AC-P8-019 | FR-P8-025 | an approved booking waiting on SCR-29 Posting | the officer approves it and the next ALS batch completes | the approval is recorded with the approving role, the limit and the time; the item is in the next posting run; the confirmation from the next completed batch is shown against the item | AC-P8-007-01; SCR-29 |
| AC-P8-020 | FR-P8-026 | a deed in lieu arrangement with a monthly rental due | the due date arrives and the auto-debit is taken | one receipt is issued against the case and the arrangement is not stopped; a missed rental is reported to rwb-treatment for follow-up and appears on the arrears list | AC-P8-009-01; GAP-1631; ASM-2767 |
| AC-P8-021 | FR-P8-027, FR-P8-028 | the matched proceeds of a business date agree with `v_ace_payment` and with the delivered posting file, and a second date is 12 receipts short of the ACE position | the reconciliation runs for both dates | the first date writes a PASS result per check with variance zero; the second writes a BREAK with the count and the amount variance, a break row per case with its reason and an owner role, and a task to Credit Administration; no break is deleted by a rerun | AC-P8-011-01; GAP-1636; ASM-2772 |
| AC-P8-022 | FR-P8-029, FR-P8-030 | the applied postings of an approved write-off population and a payment received after charge-off | the provision inputs are built and the payment is matched | the provision inputs state the posted population and the definition versions used and refuse to publish a set that does not reconcile; the post charge-off payment is recorded as income with the agency fee from the contracted schedule | AC-P8-008-01; BR-054, BR-059; R-WO-37 |
| AC-P8-023 | FR-P8-001, FR-P8-010, NFR-P8-010 | receipts on a case whose customer is masked for the role, and one receipt on a case outside the role's scope | the officer reads the receipt list and the posting list | neither list shows a clear customer identity or a national number; the out-of-scope receipt is absent; each consumer receives only the fields its contract declares | NFR-039, NFR-040; Arch v5 slide 45 |
| AC-P8-024 | NFR-P8-001, NFR-P8-003, NFR-P8-014, NFR-P8-019 | a business date at the volume of the busiest month, with the receipt list open at the busiest hour | the matching run, the posting run and the receipt read are measured | the run completes before 07:00 on the business date of the completed batch; a rule evaluation stays under 300 ms at the 95th percentile; the list answers under 2 s at the 95th percentile; every run has a run book, a trace, and an alert that reaches a named owner within 15 minutes | NFR-001, NFR-008, NFR-011, NFR-019, NFR-064, NFR-068 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| REQ-CHO-007 | CAP-P8-001 | FR-P8-005 | NFR-P8-001, NFR-P8-004 | AC-P8-004, AC-P8-005 |
| REQ-CHO-008 | CAP-P8-006 | FR-P8-014, FR-P8-022 | NFR-P8-001 | AC-P8-013 |
| REQ-CHO-009 | CAP-P8-001, CAP-P8-002, CAP-P8-003, CAP-P8-011 | FR-P8-001, FR-P8-002, FR-P8-004, FR-P8-006, FR-P8-007, FR-P8-010, FR-P8-011, FR-P8-012, FR-P8-013, FR-P8-015, FR-P8-016, FR-P8-017, FR-P8-027, FR-P8-028, FR-P8-032 | NFR-P8-001, NFR-P8-002, NFR-P8-005, NFR-P8-010, NFR-P8-011, NFR-P8-013, NFR-P8-017, NFR-P8-019 | AC-P8-001, AC-P8-002, AC-P8-006, AC-P8-009, AC-P8-011, AC-P8-012, AC-P8-014, AC-P8-021, AC-P8-023, AC-P8-024 |
| REQ-S4-010 | CAP-P8-004 | FR-P8-017 | NFR-P8-015 | AC-P8-015 |
| REQ-S5-009 | CAP-P8-010 | FR-P8-018, FR-P8-019 | NFR-P8-010 | AC-P8-016 |
| REQ-S2-010 | CAP-P8-009 | FR-P8-026 | NFR-P8-005 | AC-P8-020 |
| REQ-S6-008 | CAP-P8-007 | FR-P8-023, FR-P8-025 | NFR-P8-015 | AC-P8-018, AC-P8-019 |
| REQ-S7-005 | CAP-P8-007, CAP-P8-008 | FR-P8-023, FR-P8-025, FR-P8-029 | NFR-P8-020 | AC-P8-018, AC-P8-019, AC-P8-022 |
| REQ-S7-007 | CAP-P8-005, CAP-P8-008 | FR-P8-020, FR-P8-030 | NFR-P8-020 | AC-P8-017, AC-P8-022 |
| REQ-S9-004 | CAP-P8-005 | FR-P8-020, FR-P8-021 | NFR-P8-012 | AC-P8-017 |
| REQ-APD-001 | CAP-P8-005 | FR-P8-021 | NFR-P8-007 | AC-P8-017 |
| REQ-DRI-001, REQ-DRI-002, REQ-DRI-005, RULE-002 | CAP-P8-001, CAP-P8-007 | FR-P8-009, FR-P8-025 | NFR-P8-007, NFR-P8-008, NFR-P8-009, NFR-P8-020 | AC-P8-008, AC-P8-019, AC-P8-022 |
| REQ-DRI-007 | CAP-P8-007 | FR-P8-023, FR-P8-024 | NFR-P8-006, NFR-P8-012, NFR-P8-014, NFR-P8-015, NFR-P8-016, NFR-P8-018 | AC-P8-018, AC-P8-024 |
| REQ-DRI-010, REQ-DRI-011 | CAP-P8-012 | FR-P8-003, FR-P8-008 | NFR-P8-003 | AC-P8-002, AC-P8-003, AC-P8-007 |
| REQ-RDF-009 | CAP-P8-001 | FR-P8-006, FR-P8-031 | NFR-P8-004 | AC-P8-001, AC-P8-005 |
| BR-030 | CAP-P8-010 | FR-P8-018, FR-P8-019 | NFR-P8-010 | AC-P8-016 |
| BR-033 | CAP-P8-011 | FR-P8-027, FR-P8-028 | NFR-P8-001, NFR-P8-019 | AC-P8-021, AC-P8-024 |
| BR-043 | CAP-P8-004 | FR-P8-017 | NFR-P8-015 | AC-P8-015 |
| BR-054 | CAP-P8-008 | FR-P8-029 | NFR-P8-020 | AC-P8-022 |
| BR-059 | CAP-P8-008 | FR-P8-030 | NFR-P8-020 | AC-P8-022 |
| RULE-002 | CAP-P8-001, CAP-P8-007 | FR-P8-009 | NFR-P8-007, NFR-P8-009 | AC-P8-008 |

BR coverage: 24 requirement statements are cited - 18 program requirements (REQ-CHO, REQ-S, REQ-APD, REQ-DRI, REQ-RDF), the five numbered business requirements of the Epics 3 to 8 BRD (BR-030, BR-033, BR-043, BR-054, BR-059) and RULE-002 - and every one of them is served by at least one functional or non-functional requirement. No BR cited here is left without an FR. Three nearby BRs are deliberately not served by this service and are listed so the gap is explicit: REQ-S7-006 (post charge-off placement with an agency, served by S7 rwb-writeoff; this service contributes only the payment and the fee), REQ-S9-001 to REQ-S9-003 (partner selection, contract and targets, served by S9 rwb-partner; this service reads only the fee schedule), and REQ-S5-010 (transfer, buy-back and rental approvals, served by S5 rwb-asset; this service takes the rental and the proceeds). The program BRD states that P8 has no requirement section of its own (GAP-1498; ASM-2783); its requirements are read from sections 5.3, 5.9, 5.11, 5.12 to 5.14 and 5.16, which is why the enforcement proceeds requirement (REQ-S4-010, section 5.11) is cited here although the BRD's note names only 5.3 and 5.12 to 5.14 (GAP-1641; ASM-2777).

## 11.3 BR to epic trace

| BR | Business epic | Service epic | Release |
|---|---|---|---|
| REQ-CHO-007, REQ-CHO-008, REQ-CHO-009 | EP02 (REQ-CHO-007, REQ-CHO-009), EP03 (REQ-CHO-008) | RWB-SVC-P8 | 31 December 2026 and 31 January 2027 (both tentative) |
| REQ-S4-010 | EP04 (E4 scope), EP05 (E5 litigation scope) | RWB-SVC-P8 | 28 February 2027 (tentative) |
| REQ-S5-009, REQ-S6-008 | EP04, EP06 | RWB-SVC-P8 | 28 February 2027 and 30 April 2027 (both tentative) |
| REQ-S7-005, REQ-S7-007 | EP06 | RWB-SVC-P8 | 30 April 2027 (tentative) |
| REQ-S9-004, REQ-APD-001, REQ-DRI-001, REQ-DRI-002, REQ-DRI-005, REQ-DRI-007, REQ-DRI-010, REQ-DRI-011, REQ-RDF-009 | Cross-epic | RWB-SVC-P8 with RWB-PLT-* and RWB-ITG-W2 to W4 | Wave 0 then every wave |

## 11.4 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Matching run on a full business date with matched, unmatched and missed cases | FR-P8-001 to FR-P8-011, FR-P8-031, NFR-P8-001, NFR-P8-004 | Credit Administration officer with the QA team |
| Refused parameter load and a run with no version in force | FR-P8-003, FR-P8-008, AC-P8-003, AC-P8-007 | Reference data administrator with the QA team |
| Decision log outage drill | FR-P8-009, NFR-P8-009 | Platform administrator |
| Manual match, duplicate key and refused right on both operations | FR-P8-012, FR-P8-013, FR-P8-032 | Credit Administration officer with the security administrator |
| Settlement, sale and enforcement proceeds end to end with the residual raised | FR-P8-015 to FR-P8-019 | Restructuring officer and sale officer with the QA team |
| Fee calculation, approval limit and posting file delivery with a forced failure | FR-P8-020, FR-P8-021, FR-P8-023 to FR-P8-025, NFR-P8-015 | Finance and CFO delegate with the QA team |
| Reconciliation run with a seeded difference and a cleared break | FR-P8-027, FR-P8-028 | Reconciliation officer |
| Provision inputs and post charge-off recovery against a posted population | FR-P8-029, FR-P8-030 | Finance and CFO delegate with the write-off team |
| Masking matrix, access log reconciliation and contract review per consumer | NFR-P8-010, NFR-P8-011, AC-P8-023 | Compliance and PDPA officer |
| Performance and volume test at the stated volume | NFR-P8-002, NFR-P8-003, NFR-P8-019 | QA team |
| Availability, failover and restore test, and the rollback rehearsal | NFR-P8-005, NFR-P8-006, NFR-P8-016 | IT lead with the DevOps team |
| Security review, secret scan and pipeline run with a seeded violation, and the sign-in identity test | NFR-P8-012, NFR-P8-013 | Security administrator |
| Thai and English label and message review | NFR-P8-017 | Business lead with Legal and Compliance |
| Tenancy, classification and retention review by record class | NFR-P8-018, NFR-P8-020 | Compliance and PDPA officer |

# 12. Open questions

FSD P8 v3 carries no open question table of its own, so nothing is carried forward from it. The BRD open decisions that bear on this service are carried with their DL identifiers. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-P8-01 | Which two operations does the contract publish for this service: GET /proceeds and POST /proceeds/{proceedsId}/match, or the paths named in Architecture v5 slide 17? | Solution architect | Before wave 2 contract publication | CAP-P8-002, FR-P8-012, FR-P8-013 | GAP-1626; ASM-2762 |
| OQ-P8-02 | Is a payment received a named same-day trigger under DL06, and on which interface, given that ACE has no real-time feed today? | Solution architect with the ACE team | Before wave 2 system test | CAP-P8-001, FR-P8-006 | DL06; GAP-1640; ASM-2776 |
| OQ-P8-03 | Where do the matching values live: as parameter and reference rows of rwb-case (DP-06, DP-07), or inside the PAYMENT_MATCH rule package of rwb-decision (DP-04)? | Solution architect with P3 and P7 | Before wave 2 system test | CAP-P8-012, FR-P8-003, FR-P8-008 | GAP-1628; ASM-2764 |
| OQ-P8-04 | Is the data quality exception list of the monolith replaced, or is the orphan reported on the reconciliation break list of rwb-source-data? | Data architect | Before wave 2 system test | CAP-P8-002, FR-P8-011 | GAP-1627; ASM-2763 |
| OQ-P8-05 | Is a reversed payment in scope for this service, and what happens to the matched proceeds row and to the case? | Business lead with Credit Administration | Before wave 3 | CAP-P8-003, CAP-P8-010 | GAP-1632; ASM-2768; R-SET-23, R-SET-24 |
| OQ-P8-06 | Which interface takes the deed in lieu rental by auto-debit, and who owns the ATS and AMIS route? | Solution architect with the partner manager | Before wave 3 | CAP-P8-009, FR-P8-026 | GAP-1631; ASM-2767 |
| OQ-P8-07 | How do LED and enforcement proceeds reach the Workbench, given that the LED portal is outside the 19 services? | Solution architect with the litigation owner | Before wave 3 | CAP-P8-004, FR-P8-017 | GAP-1631; ASM-2767 |
| OQ-P8-08 | What is the posting file layout, which ledger receives it, and what does the ledger return? | Finance and CFO delegate with the solution architect | Before wave 3 | CAP-P8-007, FR-P8-023, FR-P8-024 | GAP-1630; ASM-2766 |
| OQ-P8-09 | Which fee tables exist, who owns them, and on what schedule are partner and court fees set? | Finance and CFO delegate with the partner and agency manager | Before wave 3 | CAP-P8-005, FR-P8-020, FR-P8-021 | GAP-1633; ASM-2769 |
| OQ-P8-10 | In which order is a receipt applied to the balance, and who owns that policy row? | Finance and CFO delegate | Before wave 3 | CAP-P8-010, FR-P8-018 | GAP-1636; ASM-2772 |
| OQ-P8-11 | Does the ledger position of the daily reconciliation come from the delivered posting file alone, or is a ledger return expected? | Reconciliation officer with Finance | Before wave 3 | CAP-P8-011, FR-P8-027 | GAP-1635; ASM-2771 |
| OQ-P8-12 | What baseline, target and measurement definition apply to "receipts matched the same day", and what is the daily receipt volume for the volume test? | Product owner with the Tribe lead | Before wave 2 release | CAP-P8-001, NFR-P8-019 | GAP-1638, GAP-1643; ASM-2774, ASM-2779 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (GAP-1642; ASM-2778).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 5.3 (REQ-CHO-007, REQ-CHO-008, REQ-CHO-009), 5.9 (REQ-S2-010), 5.11 (REQ-S4-010), 5.12 (REQ-S5-009), 5.13 (REQ-S6-008), 5.14 (REQ-S7-005, REQ-S7-007), 5.16 (REQ-S9-004), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan), 9 (open decisions DL06, DL11, DL26, DL43), 10 (delivery model), 11 (requirement trace and the note that P8 has no requirement section), 12 (gaps and assumptions) |
| Recovery Workbench Business Requirements Epic 2 v3 | 3.8 (P8 requirements RWB-E2-008 and RWB-E2-027), 4 (program requirements met), 8 (delivery model, waves), 9 (trace), 10.3 (change log) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 7 (scope and the epics that name RWB-SVC-P8), 8 (BR-030, BR-033, BR-043, BR-054, BR-059, RULE-002), 9 (trace to stories and to the specification features) |
| Recovery Workbench FSD P8 Payments and posting v3 | Document control, existing capability check, A1 (context, scope, feature overview A1.2, preconditions), A2.1 to A2.11 (functional decomposition, business rules VR-P8-xxx and BR-P8-xxx, acceptance criteria AC-P8-xxx), Requirements served (empty), Screens (SCR-28, SCR-29), Appendix A and B |
| Recovery Workbench TSD P8 Payments and posting v2 | T3.0 to T3.3 (standard columns, `proceeds` DF-FIN-001 to DF-FIN-009, `payment_match_rule` DF-REF-261 to DF-REF-273, lists of values, relationships), T5 (INT-02, INT-03, INT-16), T6.1 (RBAC matrix for "Write-off and posting"), T7 (NFR-049 to NFR-056), Appendix T-A (API-P8-001, API-P8-002), Appendix T-B (DL06, DL11, DL35) |
| Recovery Workbench Architecture v5 | Slides 4 and 38 (19 services, waves, P8 created with Epics 2-3), 13 (dead-letter and replay standard), 14 to 20 (service contracts; slide 17 gives the rwb-payment contract), 37 (no data lake), 41 (service catalogue row for P8), 42 and 43 (event catalogue: EV-11, EV-12, EV-25, EV-26), 44 (job map: JOB-07 and JOB-08 as event-triggered workflows), 45 (architect questions on personal data) |
| Recovery Workbench Temporal and Drools Design v1 | Task queue and workflow kit, the PAYMENT_MATCH and BOOKING_MATCH packages as the only named Phase 1 packages besides RESTRUCTURE, local evaluation under 300 ms, `postProceeds` as a saga step, the worked example of a missed payment on 16 December |
| Recovery Workbench Batch and Scheduling Design v4 | JOB-07 (payment matching) and JOB-08 (booking confirmation): trigger on the ACE batch-complete record for ALS, after JOB-02, owner Credit Administration, exception list as the failure path |
| Recovery Workbench Business Rules and Routing Logic v4 | R-RES-26 to R-RES-28; R-SET-14 to R-SET-19, R-SET-23, R-SET-24, R-SET-26, R-SET-27; R-UNI-03, R-UNI-39, R-UNI-40, R-UNI-48; R-WO-37 to R-WO-39 |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic) |
| Recovery Workbench Logical Data Model and Data Dictionary v8 | `proceeds` (DF-FIN-001 to DF-FIN-009) and `payment_match_rule` (DF-REF-261 to DF-REF-273, each recorded as retired by D-RCV-36) |
| Recovery Workbench API Specification v4 | `/proceeds` and `/proceeds/{proceedsId}/match` (x-module P8, first release E2 and E4), the `Proceeds`, `ProceedsPage` and `MatchRequest` schemas |
| Recovery Workbench Microservice Ownership Map v1 | Tables (P8 owns `proceeds`), operations (GET /proceeds, POST /proceeds/{proceedsId}/match), events (EV-11, EV-12, EV-25), jobs (JOB-07, JOB-08 with their event-started replacements) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R4 (services and naming), R5 (target structure, wave map), R8 (outputs), R9 (gaps and assumptions) |
