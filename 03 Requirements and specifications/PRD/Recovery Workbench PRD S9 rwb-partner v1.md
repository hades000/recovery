SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD S9 rwb-partner v1
description: Product requirements for the Recovery Workbench partner management service (S9 rwb-partner) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S9 Partner management v3.md
service: S9 rwb-partner
epic: RWB-SVC-S9
wave: 4
decision: D-RCV-60
---

# Recovery Workbench PRD S9 rwb-partner v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD S9 rwb-partner |
| Document ID | S9-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft. The BRD is read as approved for this run and the approval itself is carried as an assumption (ASM-3038) |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | S9 rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epics | EP06 (Epic 6, debt sale, write-off and partners, wave 4) and EP07 (Epic 7, deviations and partners, wave 4). Two earlier slices, EP01 and EP02, are carried in section 10.2 because the split plan gives them S9 stories (GAP-1843; GAP-1844; ASM-3024; ASM-3025) |
| Release | EP06, 30 April 2027 (tentative); EP07, 31 May 2027 (tentative) |
| Schema | `rwb_partner` |
| REST base | `/api/recovery/partner/v1` for staff paths behind gateway-bff, and `/partner/v1/*` for the partner portal behind the partner gateway (ASM-3030) |
| Topic | `rwb.partner.events.v1` |
| Temporal task queue | `rwb-partner` |
| Workflow | InstructionWorkflow (the Partner instruction kit template, with the service level timers of each partner type) |
| Java package | `th.co.scb.ace.workbench.recovery.partner` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Business analyst, S9 |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), ADR-010, ADR-013 to ADR-023 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epics 3 to 8 v1; FSD S9 Partner management v3; Architecture v5; Temporal and Drools Design v1; Business Rules and Routing Logic v4; Logical Data Model and Data Dictionary v8; Non Functional Specification v3 |
| Upstream requirement IDs | REQ-S9-001 to REQ-S9-009; BR-059, BR-060, BR-070, BR-071; RULE-021, RULE-023, RULE-024; R-UNI-25, R-UNI-26, R-UNI-27, R-UNI-28, R-UNI-29, R-UNI-45; R-WO-30 to R-WO-35; R-LIT-24 to R-LIT-29; REQ-ACA-012, REQ-S7-006 and REQ-S7-007 as requirements delivered by other services that bound this one |
| Upstream acceptance criteria | AC-S9-001-01 to AC-S9-015-01 (main success flow, one per feature); AC-EXC-S9-001-01 to AC-EXC-S9-015-01 (role without the right); AC-EXC-S9-001-02 to AC-EXC-S9-015-02 (decision cannot be recorded). The FSD defines no alternate flow and no system background event for any of the fifteen features (GAP-1842; ASM-3023) |
| Generated IDs | CAP-S9-001 to CAP-S9-018; FR-S9-001 to FR-S9-043; NFR-S9-001 to NFR-S9-026; AC-S9-001 to AC-S9-030; JRN-S9-01 to JRN-S9-08; ROL-S9-01 to ROL-S9-15; OQ-S9-01 to OQ-S9-24 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD S9 Partner management v3 (15 November 2026) and Business Requirements Epics 3 to 8 v1, realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD S9 Partner management v3. Its requirement IDs, feature IDs, validation rules, business rules, message IDs, lists, screen IDs and acceptance criterion IDs are carried unchanged; the microservice realignment changes the read path, the owner of the payment and the fee settlement, the owner of the approval route, the wave in which four slices land and the partner portal contract, not the requirement substance. The CAP, FR, NFR, AC, journey, role and open-question IDs of this document are new and exist only here (ASM-3041).

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only. Everything else unchanged from v2 |
| 1 and 2 | Not specified in the source documents (ASM-3040) | Earlier versions of the FSD. Their dates and change notes are not in the sources read, and are carried as an open item rather than reconstructed |
| 1 (PRD) | 22 November 2026 | First PRD of this family (ASM-3039). CAP, FR, NFR, AC, journey and open-question IDs are new; the FSD requirement IDs (REQ-S9-001 to REQ-S9-009), feature IDs (FEAT-PRM-01 to FEAT-PRM-15), validation rule IDs (VR-S9-001-1 to VR-S9-015-1), business rule IDs (BR-S9-001 to BR-S9-015), acceptance criteria IDs (AC-S9-001-01 to AC-S9-015-01 and their exception rows), the routing rule IDs R-UNI-25 to R-UNI-29, R-UNI-45, R-WO-30 to R-WO-35 and R-LIT-24 to R-LIT-29, the message IDs (MSG-GEN-001, MSG-P1-001, MSG-P4-002, MSG-P7-003), the list IDs (LOV-PARTNER-TYPE, LOV-PANEL), the list and capability IDs the Logical Data Model adds (LOV-CAPABILITY PARTNER_PORTAL, LOV-INSTRUCTION, LOV-INSTR-STATUS), the field IDs (DF-PRT-001 to DF-PRT-016, DF-REF-212 to DF-REF-217), the event IDs EV-20 and EV-21 and the screen IDs (SCR-34, SCR-35, SCR-36, PRT-01 to PRT-04) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the program requirements REQ-S9-001 to REQ-S9-009 (section 5.16) and of the non-functional requirements (section 6) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-059, BR-060, BR-070 and BR-071, RULE-021, RULE-023 and RULE-024, KPI-011, the E6 and E7 scope, the assumptions, the risks and the open questions Q-019 and Q-023 |
| Recovery Workbench Functional Specifications by Module v6, FSD S9 Partner management v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Business Rules and Routing Logic v4 | Rules | Source of the recall, exit, conflict, insolvency, conduct-breach and re-selection rules R-UNI-25 to R-UNI-29 and R-UNI-45, and of the placement and instruction rules R-WO-30 to R-WO-35 and R-LIT-24 to R-LIT-29. It holds no partner route set (GAP-1840; ASM-3021) |
| Recovery Workbench Logical Data Model and Data Dictionary v8 | Data | Source of the `partner`, `partner_instruction` and `partner_user` fields DF-PRT-001 to DF-PRT-016 and DF-REF-212 to DF-REF-217, and of the lists LOV-PARTNER-TYPE, LOV-PANEL, LOV-INSTRUCTION, LOV-INSTR-STATUS and LOV-CAPABILITY |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, only rwb-source-data reads ACE, the connection matrix of slide 13, Kafka, Temporal, the partner gateway and no data lake |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: InstructionWorkflow on `rwb-partner` with the service level timers, the Partner instruction kit template, the partner clocks, and the universal rule package that arrives in Epic 3 |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every operation, event, workflow, table, list and job named here |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder, register, wave map and decoupling-pattern rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-partner (S9) is the recovery module's partner management. It turns "partners are instructed and paid by email and spreadsheet, and allocation is not based on performance" into a product: a panel held as versioned data with each partner type's contract, fee schedule, service levels and scope, and one named owner for each type; work placed with the partner the scorecard rule picks on measured return, capacity and panel status, with an override that carries a reason; an instruction issued through the partner portal with a clock by partner type and a chase and a recall when the service level is missed; a contact, a promise and a cash result on the case the same day instead of in a mailbox; a recovery matched and a fee calculated from the contracted schedule; a post charge-off account placed with the agency the panel rule picks; a monthly score, a fee claim checked against the schedule and the result, and a review held on the six points every partner type is managed on; a contractual notice and a cure period when a target is missed; an exit or a conflict, an insolvency or an upheld conduct breach that recalls every open case held by that partner; and conduct sampled against the rules with the breach raised and the allocation suspended.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-partner | One deployable with its own API and worker, schema `rwb_partner`, login, topic `rwb.partner.events.v1`, task queue `rwb-partner` and lifecycle | The panel becomes one owned product with its own release, instead of a spreadsheet and an inbox per partner type |
| The panel and the terms as versioned data | Panel status, contract end, fee schedule, service levels, scope and one owner role per partner type, each a versioned row read at run time with its version | Allocation by measured return is only possible if the panel, the terms and the score are data, not a person's knowledge |
| Allocation on measured return | The partner chosen by the scorecard rule on measured return, capacity, panel status and instruction type, with the score and the rule version on the record | Allocation by habit is the difference between a panel and a rota |
| InstructionWorkflow and the partner clock | One workflow per instruction with the service level timer of the partner type, a chase, then a recall and a re-selection | A service level kept in an inbox is a service level nobody measures |
| The result on the case the same day | Contact, promise and cash reported through the portal, attached to the case the same day and published as PartnerResultSubmitted | A result that arrives by email arrives tomorrow, and the case waits |
| The fee as a governed claim | The fee calculated from the contracted schedule and the recorded result, the claim checked against both, and the approval recorded with its level | Money leaving the bank on a partner's own invoice is money with no control |
| The placement after charge-off | The charged-off account placed with the agency chosen on measured return, held when no agency has capacity, recalled and replaced when it underperforms | Placement by memory leaves a charged-off book with the wrong agency, or with none |
| The score, the review and the exit as product behaviour | The monthly score from the measured results, the review on the six points, the notice and cure period, and the exit that recalls every open case | A panel that is not scored, reviewed and exited is an unmanaged cost base |
| Conduct sampled and the allocation suspended | Contacts and complaints sampled against the conduct rules, the breach raised, the allocation suspended and the case reported to the review | A breach found by a customer complaint is the control arriving too late |
| The partner identity and the portal channel | A partner user bound to one firm and one partner role, and every instruction and result exchanged through the partner gateway under FAPI 2.0 | Partners exchange data through the portal and the external gateway, and not by email |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its ingestion and its backups | REUSE | ACE team |
| The read-only view contract and the freshness of each data product | REUSE, elsewhere | P1 rwb-source-data (this service reads it by contract; GAP-1835; ASM-3016) |
| Case record, CMMN state, queues, tasks, allocation and the case timers | REUSE | P3 rwb-case (the case is moved by rwb-case on the facts this service publishes) |
| Approval workflow, delegation limits, decision record, hash chain and rule package registry | REUSE | P7 rwb-decision (GAP-1857; ASM-3043) |
| Roles, capability areas, masking policy and the delegation table | REUSE | P4 rwb-access (the internal role model; ASM-3033) |
| Document hub, custody, the write-once container and retention | REUSE | P5 rwb-document (this service calls it by REST; slide 13) |
| Payment and proceeds matching, fees, posting to ALS and the general ledger | REUSE, elsewhere | P8 rwb-payment (this service calculates the fee and holds the claim; GAP-1836; ASM-3017) |
| Notice content, merge fields, template versions and proof of delivery | REUSE, elsewhere | P6 rwb-comms (the contractual notice on a missed target; GAP-1859; ASM-3045) |
| The asset record, the floor price and the disposal state | REUSE, elsewhere | S5 rwb-asset (the extra cost on a held asset is recorded here against the asset reference; GAP-1847; ASM-3028) |
| The post charge-off treatment decision and the recovery after charge-off | REUSE, elsewhere | S7 rwb-writeoff (GAP-1854; ASM-3035) |
| The interaction ledger and the case timeline | REUSE, elsewhere | P1 rwb-source-data for the ledger, P3 for the timeline (default ruling, DP-18) |
| Parameters and reference data | REUSE, elsewhere | P3 rwb-case (default ruling, DP-06 and DP-07) |
| Measures, the steering dashboard and the regulatory reports | REUSE, elsewhere | P9 rwb-reporting (GAP-1858; ASM-3044) |
| Screens and the two routes that serve them | REUSE | gateway-bff for staff screens and the partner gateway for partner screens (ADR-019; RWB-PLT-EDGE; GAP-1848; ASM-3029) |
| Quartz and its shared tables | REPLACED | Temporal durable timers and Schedules through the workflow kit (ADR-016, DP-10) |
| The Power BI copy of the scorecard | REMOVED | No data lake; the read model in rwb-reporting (ADR-018; GAP-1846; ASM-3027) |
| Collections before day 90 on EFS | OUT OF SCOPE | EFS and the ACE collection module |
| Booking in the core bank and the credit decision | OUT OF SCOPE | The officer and the lending system; this service records the instruction and the result |
| The partner's own case system, its own invoicing and its own field records | OUT OF SCOPE | Each firm, each agency and each vendor |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014; slides 37 and 45).
2. The service writes only schema `rwb_partner`; no cross-schema join and no foreign key into `public` (ADR-014, DP-01, DP-02).
3. The slide 13 connection matrix gives the S9 Partner row exactly two outgoing calls: REST to P5 Document, and REST to Outside through the partner gateway. Every other fact arrives as a Temporal call or an event from another service; this service makes no REST or Temporal call to rwb-case, rwb-decision, rwb-payment, rwb-source-data, rwb-comms or rwb-asset (slide 13; GAP-1835, GAP-1836, GAP-1847, GAP-1857, GAP-1859).
4. REST is one hop from gateway-bff with a 2 s timeout, an Idempotency-Key on every POST and RFC 9457 problem details; a GET is retried once with jitter (ADR-020; slides 10 and 11).
5. Events are CloudEvents 1.0 on Kafka with an outbox and an inbox, retry at 1 minute, 10 minutes and 1 hour and then a dead-letter topic; topic `rwb.partner.events.v1`, keyed by case (ADR-015, DP-09, DP-14; slides 9 and 11).
6. Temporal namespace `rwb-recovery`, task queue `rwb-partner`; InstructionWorkflow is built from the Partner instruction kit template with a service level timer per partner type, and schedules and durable timers replace Quartz (ADR-016, DP-10; slide 17; Temporal slide 12, slide 25).
7. Rules are versioned data evaluated in process by the embedded Drools kit; the universal rule package R-UNI-01 to R-UNI-50 arrives in Epic 3, and the partner decisions are governed in rwb-decision (ADR-017, DP-04; Temporal slide 5, slide 25; GAP-1840).
8. There is no data lake: the forum report and the measures are read from the decision record and the events into rwb-reporting (ADR-018, DP-17; GAP-1858).
9. The edge is two gates: staff reach the service through gateway-bff with a Redis session, and partners reach it only through the partner gateway in the DMZ under FAPI 2.0 with multi-factor authentication and a scope to their own cases (ADR-019; slide 10; NFR-050; GAP-1848, GAP-1849).
10. Personal data stays out of events, workflow inputs and logs; masking is by role, using the permission data cached from rwb-access, and each service authorises the object itself (slide 10; NFR-039, NFR-040).
11. A service is created in its wave. This one is created in wave 4, while the split plan places four of its stories in waves 1 and 2 and two wave-3 services call it; the ordering is carried as three conflict gaps and answered by contract-first delivery (GAP-1843, GAP-1844, GAP-1845; ASM-3024, ASM-3025, ASM-3026).
12. Every value a business person may change is a versioned data row read at run time, changed through a validated load without a code release (principle 1; BR-S9-001 to BR-S9-015; FR-S9-002, FR-S9-028).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-S9-01 | Partner and agency manager | The panel with its terms, allocation by measured return, the override with its reason, the instruction and its clock, the score, the review and the exit | JRN-S9-01 to JRN-S9-07 |
| ROL-S9-02 | Head of the partner type | The recall on an insolvency, the decision on a contract end and the position of every case that partner holds | JRN-S9-06 |
| ROL-S9-03 | Reference data administrator | Panel, contract, fee schedule, service level, scope and owner role as versioned data with a valid-from date | JRN-S9-01 |
| ROL-S9-04 | Case owner | The result of the instruction on the case the same day, and the next action when the partner does not perform | JRN-S9-04 |
| ROL-S9-05 | Credit administration | The recovery matched to the case and the fee claim that agrees with it | JRN-S9-04 |
| ROL-S9-06 | Finance and CFO delegate | A fee claim checked against the schedule and the result, approved at the level the limit names | JRN-S9-05 |
| ROL-S9-07 | Head of Litigation, Head of Asset Liquidity | The firm and the vendor instruction, and the instruction recalled when the partner fails | JRN-S9-03, JRN-S9-06 |
| ROL-S9-08 | NPA and asset manager | The extra cost on a held asset recorded and approved before it is committed | JRN-S9-07 |
| ROL-S9-09 | Conduct and QA officer | The sample of partner contacts and complaints, the breach raised and the suspension of allocation | JRN-S9-07 |
| ROL-S9-10 | Field collector | Visits, photographs and bills captured against the case from the field, including with no network connection | JRN-S9-07 |
| ROL-S9-11 | Partner user (external role) | The instructions placed with it, their due dates, a place to record the result and upload the evidence, and its invoice | JRN-S9-03, JRN-S9-04 |
| ROL-S9-12 | Compliance and PDPA officer | Masking by role, an access log that cannot be skipped, and a partner identity scoped to its own cases | JRN-S9-08 |
| ROL-S9-13 | Internal audit | An instruction reproducible from the log with its rule version, its approver and its recall reason | JRN-S9-08 |
| ROL-S9-14 | Platform administrator | A timer that reports a breach, an alert with a named owner, and a replay path for a failed event | JRN-S9-03, JRN-S9-06 |
| ROL-S9-15 | Developer | A typed contract to build against, a fake for every dependency, and a build that fails on a direct ACE read | JRN-S9-08 |

Non-human actors: the case workflow and the stage workflows that call this service by Temporal (rwb-case, rwb-litigation, rwb-asset); InstructionWorkflow on `rwb-partner`; the approval workflow on rwb-decision; the document hub on rwb-document; the outbox relay; the consumers of InstructionIssued and PartnerResultSubmitted (the partner portal, rwb-litigation, rwb-asset and rwb-case); the partner gateway in the DMZ. The partner is reached through the partner gateway and never by a direct call from an internal service.

# 4. User journeys

## 4.1 Current state (as built and as run today)

1. Partners are instructed by email and paid from a spreadsheet; the panel, the fee schedule and the service levels are held by the person who owns the relationship.
2. Allocation follows habit and rotation rather than performance, and a vendor allocation takes 2 working days from the request.
3. An instruction is a letter or an email, and the due date lives in the officer's calendar; no clock runs on the partner and no recall path exists.
4. The result returns by email and is keyed onto the case by a person, so the case waits a day or more for a result the partner already holds.
5. The fee arrives as an invoice, is checked by reading the contract, and is paid on a screen decision with no record of the schedule version behind it.
6. A charged-off account is placed with an agency by memory; a recall is a telephone call and nothing records the reason.
7. The monthly score, the review on the six points and the exit are kept in a document outside the Workbench, so the panel and the case list disagree.

Consequence: allocation is not based on performance, no one can say which partner holds which case, and no fee can be defended against the schedule it was charged under (FSD S9 A1.3; Temporal and Drools Design v1 slide 25 note).

## 4.2 Target state (this product)

### JRN-S9-01 The panel and the terms held as data (on request, reference data administrator and partner and agency manager)

1. The reference data administrator records the partner on the panel with its code, registered name, type from LOV-PARTNER-TYPE and status from LOV-PANEL, and the contract end date.
2. The contract terms, the fee schedule, the service levels and the scope are loaded as versioned rows with a valid-from date, and the version in force is the one every later step reads.
3. One owner role is recorded for each partner type, and a partner type with no owner role cannot be allocated work.
4. The panel status can move to ACTIVE only when the contract end, the fee schedule and the service levels are present.
5. The change history of the panel row is readable with the version that was in force at each instruction.

### JRN-S9-02 Work placed by measured return, and the override (on the placement trigger, partner and agency manager)

1. A case needs a partner, and the calling stage workflow starts the instruction on `rwb-partner` by Temporal.
2. The service reads the panel and the score in force, and applies the scorecard rule on measured return, capacity, panel status and instruction type.
3. The partner chosen, its score, its capacity, its panel status and the rule version are written to the instruction record.
4. A partner whose status is on notice, suspended or exited is not chosen where the rule excludes it, and the work is held with the rule that held it.
5. The partner and agency manager may place the work with another partner, and the override records the role, the reason and the date; the override rate is reported monthly.
6. A conduct breach upheld against a partner suspends its allocation until the review clears it.

### JRN-S9-03 The instruction through the portal and the partner clock (daily, partner and agency manager and partner user)

1. The instruction is written with its type from LOV-INSTRUCTION, the instruction date, the due date and the status SENT, and InstructionIssued is published as EV-20.
2. The service level timer of the partner type starts as a durable timer in InstructionWorkflow, and the due date is visible to the partner and to the manager.
3. The partner accepts or declines through the portal; a decline re-selects the next partner on the scorecard, and the instruction moves to DECLINED.
4. A partner that misses its service level is chased once; a second miss recalls the work, records the reason and re-selects on the scorecard within 2 working days.
5. The work is recalled on a panel exit or a contract end within 5 working days, on a declared conflict within 2 working days, and on an insolvency or an upheld conduct breach the same day.
6. Every recall records the reason, and the recalculated partner clock of the new instruction starts at the re-issue.

### JRN-S9-04 The result on the case and the fee calculated (daily, case owner and credit administration)

1. The partner records the result through the portal and uploads its evidence through the document hub link.
2. The service writes the result code and the date to the instruction, moves it to DONE the same day and publishes PartnerResultSubmitted as EV-21.
3. The case moves on the published fact, because rwb-case listens to the topic; the contact, the promise and the cash are the facts the case receives.
4. The fee is calculated from the contracted schedule in force and the recorded result, and the schedule version applied is written with the amount.
5. Money recovered by the agency is matched to the case and the instruction, and a payment that matches nothing is shown with its value date until it is matched.

### JRN-S9-05 The monthly score, the fee approval and the review (monthly, partner and agency manager, Finance and CFO delegate)

1. The monthly score is built from the measured results of the month for every partner, with the measures and the weights in force.
2. The score is published to the panel and to the review forum, and each partner's position against its service levels is visible on SCR-36.
3. The fee claim is checked against the schedule in force and the recorded result; a difference is shown rather than approved.
4. The claim that agrees is approved through the approval workflow with the level the limit names, and the approver, the level and the rule version are on the record.
5. The review is held on the six points every partner type is managed on, with an action, an owner role and a date for each, and a review that skips a point cannot be completed.

### JRN-S9-06 The missed target, the notice, the cure period and the exit (on trigger, partner and agency manager and Head of the partner type)

1. A partner that misses its targets has the contractual notice issued from the approved template and the cure period started as a durable timer.
2. The notice content, the merge fields and the proof of delivery belong to rwb-comms; this service decides that a notice is due and records the template version and the approver.
3. When the cure period expires with no cure, the case for an exit is presented with the score, the breaches and the open cases.
4. The exit ends the contract, recalls every open case the partner holds within 5 working days, and re-selects each on the scorecard.
5. The partner, its instructions, its results and its fees remain readable after the exit.

### JRN-S9-07 Conduct, the extra cost and the field visit (per sample and per visit; conduct and QA officer, field collector and NPA and asset manager)

1. A sample of partner contacts and complaints is drawn against the conduct rules, with the sample size and the rule version recorded.
2. A breach is raised with the sample behind it, the allocation is suspended, and the case is reported to the review.
3. The NPA and asset manager records an additional partner cost on a held asset with its evidence, and it is approved before it is committed.
4. The field collector records the visit, the photographs and the bills against the case from the field, with no network connection, and the evidence uploads when the device reconnects.

### JRN-S9-08 Evidence and measures read later (audit, Compliance and developer)

1. An auditor reads one instruction: the partner chosen and its score, the rule version, the override or the recall with its reason, each timer and its breach, the result, the fee with the schedule version, and the approvals.
2. Compliance reads the masking matrix, the access log per personal field, the partner identity binding and the scope of each partner user to its own cases.
3. The business reads the override rate and the placement by scorecard from the decision record, not from a separate count.
4. A developer builds against the published contract and its fake; a build that reaches a view, an ACE table or another service's schema fails.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic. One capability of this module is Should and the rest are Must.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-S9-001 | A partner onboarded with its contract, fee schedule, service levels and scope | A partner enters the panel as a governed record with its terms, and no partner is active without them | BR-060 | Must | 4 | FEAT-PRM-01 (A2.1) |
| CAP-S9-002 | The panel, the fee schedule and the service level held as versioned data, with one owner role per type | Every value a person may change is a dated row with a version, and each partner type has a named owner role (REQ-S9-002; GAP-1851; ASM-3032) | BR-060 | Must | 4 | FEAT-PRM-02 (A2.2) |
| CAP-S9-003 | Work allocated by measured return | The partner the scorecard rule picks is chosen on score, capacity, status and instruction type, not by rotation or habit | BR-060 | Must | 4 | FEAT-PRM-03 (A2.3) |
| CAP-S9-004 | An override that carries a reason | A different partner can be chosen, and the role, the reason and the date are on the record and counted | BR-060 | Must | 4 | FEAT-PRM-04 (A2.4) |
| CAP-S9-005 | The partner result on the case the same day | The contact, the promise and the cash are on the case the day the partner reports them | BR-060 | Must | 4 | FEAT-PRM-05 (A2.5) |
| CAP-S9-006 | A charged-off account placed with an agency | The placement follows the panel rule, is held when no agency has capacity, and is recalled and replaced when it underperforms | BR-059 | Must | 4 | FEAT-PRM-06 (A2.6) |
| CAP-S9-007 | The recovery matched and the agency fee calculated | The money recovered is matched to the case and the fee is calculated from the schedule in force, with the version behind it | BR-060 | Must | 4 | FEAT-PRM-07 (A2.7) |
| CAP-S9-008 | The monthly scorecard | Every partner carries a monthly score built from its measured results and published to the panel | BR-070 | Must | 4 | FEAT-PRM-08 (A2.8) |
| CAP-S9-009 | The fee claim checked and approved | A claim is checked against the schedule and the result, a difference is shown, and the approval carries its level | BR-070 | Must | 4 | FEAT-PRM-09 (A2.9) |
| CAP-S9-010 | The partner review on the six points | Every partner type is reviewed on the same six points, with an action, an owner role and a date | BR-070 | Must | 4 | FEAT-PRM-10 (A2.10) |
| CAP-S9-011 | The notice on a missed target and the cure period | A missed target sends the contractual notice and starts a cure period that is a timer, not a diary note | BR-070 | Must | 4 | FEAT-PRM-11 (A2.11) |
| CAP-S9-012 | The contract ended and every open case recalled | An exit, a conflict, an insolvency or an upheld breach recalls every open case that partner holds, with the reason | BR-070 | Must | 4 | FEAT-PRM-12 (A2.12) |
| CAP-S9-013 | Conduct sampled and a breach raised | Contacts and complaints are sampled against the conduct rules, the breach is raised and the allocation suspended | BR-070 | Must | 4 | FEAT-PRM-13 (A2.13) |
| CAP-S9-014 | The extra cost and service on a held asset | An additional partner cost is recorded with its evidence and approved before it is committed | BR-071 | Must | 4 | FEAT-PRM-14 (A2.14) |
| CAP-S9-015 | Field work captured from the field | The visit, the photographs and the bills reach the case from the field, including with no network connection | BR-071 | Should | 4 | FEAT-PRM-15 (A2.15) |
| CAP-S9-016 | The partner identity and the portal channel | A partner user signs in through the partner gateway, is bound to one firm and one partner role, and sees only its own cases; every instruction and result moves through the portal and not by email | BR-060 | Must | 2 | No feature row: REQ-ACA-012, RWB-E2-019 and the screen PRT-01 (GAP-1852; ASM-3033) |
| CAP-S9-017 | The partner clock, the chase and the recall on every partner type | A service level is a durable timer, a miss is chased once, and a second miss is recalled and re-selected | BR-070 | Must | 4 | A2.3, A2.10 to A2.13; R-UNI-25 to R-UNI-29 and R-UNI-45 |
| CAP-S9-018 | One decision record per partner step and the data date behind it | Every step answers an audit question with its rule version, its inputs, its approval and its approver, and states how old the data it read is | BR-060, BR-070 | Must | 4 | A2.1 to A2.15 (the decision log entry and the freshness rule of every step) |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Direct read of the ACE views and of the ACE batch-status view | Not carried | rwb-source-data's contract (GAP-1835; ASM-3016) |
| Payment, proceeds matching, the posting to ALS and the general ledger, and the payment of the fee | Not carried | P8 rwb-payment (GAP-1836; ASM-3017) |
| The approval route, the delegation limits and the sealing of the decision record | Not carried | P7 rwb-decision (GAP-1857; ASM-3043) |
| The notice content, the merge fields, the template versions and the proof of delivery | Not carried | P6 rwb-comms (GAP-1859; ASM-3045) |
| Document custody, the upload link, the write-once container and retention | Not carried | P5 rwb-document |
| The post charge-off treatment decision and the recovery after charge-off | Reused, elsewhere | S7 rwb-writeoff (GAP-1854; ASM-3035) |
| The asset record, the floor price and the disposal state | Reused, elsewhere | S5 rwb-asset (GAP-1847; ASM-3028) |
| The interaction ledger and the case timeline | Reused, elsewhere | P1 rwb-source-data and P3 rwb-case (DP-18) |
| Parameters, reference data and the case list | Reused, elsewhere | P3 rwb-case (default rulings) |
| The measures, the steering dashboard and the forum report | Reused, elsewhere | P9 rwb-reporting (GAP-1858; ASM-3044) |
| Quartz scheduling of the partner clocks | Replaced | Durable timers and Schedules through the workflow kit (ADR-016, DP-10; GAP-1841; ASM-3022) |
| The Power BI copy of the scorecard | Removed | The read model in rwb-reporting (ADR-018; GAP-1846; ASM-3027) |
| The partner's own system, invoicing and field records | Out of scope | Each firm, each agency and each vendor |
| Collections before day 90 and the credit decision | Out of scope | EFS, the ACE collection module and the lending system |

# 6. Functional requirements

Every requirement is specific and testable. The FSD REQ column keeps the trace to the requirement row the FSD serves; where the FSD serves a BRD requirement through features with no REQ row of their own, the column says so and the BR column carries the trace. The Rule column names the routing rule of Business Rules and Routing Logic v4 that carries the transition where one exists; a dash means no rule row covers the step, which is carried as a gap (GAP-1840; ASM-3021). Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Rule | Priority | Wave |
|---|---|---|---|---|---|---|---|
| FR-S9-001 | The service SHALL create and maintain a partner record with `partner_code`, `partner_name`, `partner_type` from LOV-PARTNER-TYPE, `panel_status` from LOV-PANEL, `contract_end` and `score`, SHALL refuse a record with a required field empty with MSG-GEN-001, and SHALL write every change as a new version with its actor and its date. | CAP-S9-001 | BR-060 | REQ-S9-001 | VR-S9-001-1; BR-S9-001 | Must | 4 |
| FR-S9-002 | The service SHALL hold the contract terms, the fee schedule, the service levels and the scope of each partner type as versioned data rows with a valid-from date, SHALL read the version in force at run time, and SHALL hold no business value of them in code. | CAP-S9-002 | BR-060 | REQ-S9-001 | BR-S9-002 | Must | 4 |
| FR-S9-003 | The service SHALL record exactly one owner role for each partner type as a panel row read at run time, SHALL show a type with no owner role as unowned, and SHALL refuse an allocation where the type has no owner role. | CAP-S9-002 | BR-060 | REQ-S9-002 | — | Must | 4 |
| FR-S9-004 | The service SHALL refuse every action of this module to a role without capability area PARTNER_PORTAL with MSG-P4-002, and SHALL change nothing on the partner, the instruction or the case on a refusal. | CAP-S9-002 | BR-060 | REQ-S9-001 | VR-S9-002-1; AC-EXC-S9-001-01 to AC-EXC-S9-015-01 | Must | 4 |
| FR-S9-005 | The service SHALL move a partner to ACTIVE only where the contract end, the fee schedule, the service levels and the scope are present and current, and SHALL refuse the status change with the missing item named where one is absent. | CAP-S9-001 | BR-060 | REQ-S9-001 | VR-S9-001-1 | Must | 4 |
| FR-S9-006 | The service SHALL choose the partner by the scorecard rule on measured return, capacity, panel status and instruction type when an instruction is requested, and SHALL record the partner, its score, its capacity, its panel status and the rule and scorecard versions applied. | CAP-S9-003 | BR-060 | REQ-S9-003 | — | Must | 4 |
| FR-S9-007 | The service SHALL exclude a partner whose panel status is on notice, suspended or exited from the choice where the rule excludes it, SHALL hold the work with the rule and the status that held it, and SHALL allocate on no rotation, no fixed share and no list order. | CAP-S9-003 | BR-060 | REQ-S9-003 | R-UNI-29 | Must | 4 |
| FR-S9-008 | The service SHALL record an override with the partner chosen, the role that made it, the reason and the date, SHALL apply the override to the instruction, and SHALL make the override rate readable monthly per partner type and partner. | CAP-S9-004 | BR-060 | REQ-S9-003 | VR-S9-004-1; KPI-011 | Must | 4 |
| FR-S9-009 | The service SHALL refuse an override to a partner that the rule excludes or that has no current panel status, SHALL return the instruction unchanged, and SHALL record the refusal with its reason. | CAP-S9-004 | BR-060 | REQ-S9-003 | R-UNI-29 | Must | 4 |
| FR-S9-010 | The service SHALL write the instruction with its type from LOV-INSTRUCTION, the instruction date, the due date, the status SENT and the calling service, SHALL start InstructionWorkflow on task queue `rwb-partner`, and SHALL start the service level timer of the partner type as a durable timer. | CAP-S9-017 | BR-070 | REQ-S9-005 | R-UNI-25 | Must | 4 |
| FR-S9-011 | The service SHALL publish InstructionIssued (EV-20) on `rwb.partner.events.v1` in the same transaction as the instruction through the outbox, as a CloudEvents 1.0 message keyed by case, and SHALL carry no personal data and no amount in it. | CAP-S9-017 | BR-070 | REQ-S9-008 | — | Must | 4 |
| FR-S9-012 | The service SHALL record an acceptance and a refusal of an instruction through the portal, SHALL move the instruction to ACCEPTED or DECLINED with its date, and SHALL show the answer to the partner and to the partner and agency manager. | CAP-S9-017 | BR-070 | REQ-S9-005 | LOV-INSTR-STATUS | Must | 4 |
| FR-S9-013 | The service SHALL record a decline with its reason, SHALL re-select the next partner on the scorecard, and SHALL record the partner that declined so that it is not chosen again for the same instruction. | CAP-S9-017 | BR-070 | REQ-S9-005 | R-UNI-45 | Must | 4 |
| FR-S9-014 | The service SHALL chase the partner once when the service level is missed, and where the second service level is also missed SHALL recall the work with its reason, move the instruction to RECALLED, and notify the partner and agency manager. | CAP-S9-017 | BR-070 | REQ-S9-005 | R-UNI-25 | Must | 4 |
| FR-S9-015 | The service SHALL re-select the next partner on the scorecard within 2 working days of a recall, SHALL re-issue the instruction with a new due date, and SHALL restart the partner clock from the re-issue. | CAP-S9-017 | BR-070 | REQ-S9-005 | R-UNI-45 | Must | 4 |
| FR-S9-016 | The service SHALL recall every open case held by a partner on a panel exit or a contract end within 5 working days, on a declared conflict of interest within 2 working days, and on an insolvency or an upheld conduct breach the same day, and SHALL record the reason with each recall. | CAP-S9-012 | BR-070 | REQ-S9-006 | R-UNI-26, R-UNI-27, R-UNI-28, R-UNI-29 | Must | 4 |
| FR-S9-017 | The service SHALL stop the fee payments of a partner that has entered insolvency, SHALL record the stop with its date and its role, and SHALL present the documents and the cash that partner holds for securing. | CAP-S9-012 | BR-070 | REQ-S9-006 | R-UNI-28 | Must | 4 |
| FR-S9-018 | The service SHALL hold the service level timer of every instruction as a durable timer inside InstructionWorkflow through the workflow kit, SHALL resume the timer where it stopped after a restart, and SHALL use no Quartz table, connection or job. | CAP-S9-017 | BR-070 | REQ-S9-005 | — | Must | 4 |
| FR-S9-019 | The service SHALL place a charged-off account with the agency chosen on measured return where the treatment is soft recovery and an agency on the panel has capacity, SHALL issue an instruction of type COLLECT, and SHALL record the agency, the terms and the end date. | CAP-S9-006 | BR-059 | No REQ-S9 row; BR-059 serves FEAT-PRM-06 from REQ-S7-006 | R-WO-30 | Must | 4 |
| FR-S9-020 | The service SHALL hold the placement where no agency on the panel has capacity, SHALL escalate on the timer with the role that owns the escalation, and SHALL record the hold with its cause rather than place the account by hand. | CAP-S9-006 | BR-059 | No REQ-S9 row; BR-059 serves FEAT-PRM-06 from REQ-S7-006 | R-WO-31 | Must | 4 |
| FR-S9-021 | The service SHALL recall a placement whose measured return is below the panel threshold or whose conduct breaches are above zero, SHALL record the recall reason, and SHALL place the account with the next agency on the scorecard. | CAP-S9-006 | BR-059 | No REQ-S9 row; BR-059 serves FEAT-PRM-06 from REQ-S7-007 | R-WO-34, R-WO-35 | Must | 4 |
| FR-S9-022 | The service SHALL record the result a partner reports through the portal with its result code and its date, SHALL move the instruction to DONE the same day, SHALL attach the evidence through the document contract, and SHALL publish PartnerResultSubmitted (EV-21) so that rwb-case, rwb-litigation and rwb-asset move on the published fact. | CAP-S9-005 | BR-060 | REQ-S9-008 | R-WO-33 | Must | 4 |
| FR-S9-023 | The service SHALL refuse a result reported against an instruction that is not ACCEPTED or IN_PROGRESS, SHALL return the submission to the partner with the status that refused it, and SHALL change nothing on the case. | CAP-S9-005 | BR-060 | REQ-S9-008 | LOV-INSTR-STATUS | Must | 4 |
| FR-S9-024 | The service SHALL record the money an agency reports as recovered against the case and the instruction, SHALL take the match and the payment outcome from the owner of payment rather than computing them itself, and SHALL show a recovery it cannot match, with its value date, until the owner of payment matches it. | CAP-S9-007 | BR-060 | REQ-S9-004 | — | Must | 4 |
| FR-S9-025 | The service SHALL calculate the fee from the contracted fee schedule in force and the recorded result, SHALL record the amount with the schedule version applied, and SHALL calculate no fee from a schedule that is not current. | CAP-S9-007 | BR-060 | REQ-S9-004 | BR-S9-009 | Must | 4 |
| FR-S9-026 | The service SHALL run the monthly scorecard and the conduct sample from a Temporal Schedule in `rwb-partner` through the workflow kit, SHALL start each run against the data date it states, and SHALL run no Quartz table, connection or job. | CAP-S9-008 | BR-070 | REQ-S9-007 | — | Must | 4 |
| FR-S9-027 | The service SHALL produce the monthly score, the review outcome, the conduct result and the override rate from the decision record, SHALL publish the facts on `rwb.partner.events.v1` for the review forum and the measures in rwb-reporting, and SHALL ship no extract to an external reporting tool. | CAP-S9-008 | BR-070 | REQ-S9-007 | KPI-011 | Must | 4 |
| FR-S9-028 | The service SHALL read the scorecard measures, their weights, the thresholds and the panel capacity rule as versioned data rows, SHALL state the version applied on each score, and SHALL hold no measure, weight or threshold in code. | CAP-S9-008 | BR-070 | REQ-S9-003 | — | Must | 4 |
| FR-S9-029 | The service SHALL check a fee claim against the fee schedule in force and the recorded result, SHALL show the difference and the item that differs where they disagree, and SHALL not approve a claim that differs. | CAP-S9-009 | BR-070 | REQ-S9-004 | BR-S9-009 | Must | 4 |
| FR-S9-030 | The service SHALL take the approval of a fee claim through the approval workflow on rwb-decision with the delegation limit read at run time, and SHALL record the level applied, the approver role and the rule version with the approval. | CAP-S9-009 | BR-070 | REQ-S9-004 | — | Must | 4 |
| FR-S9-031 | The service SHALL pay no fee itself and call no payment interface, SHALL publish the approved claim as the fact the owner of payment acts on, and SHALL record the payment reference it is given against the claim. | CAP-S9-009 | BR-070 | REQ-S9-004 | — | Must | 4 |
| FR-S9-032 | The service SHALL hold the review on the six points of REQ-S9-001 as one versioned checklist per partner type, SHALL record an action, an owner role and a date for each point, and SHALL refuse to complete a review that skips a point. | CAP-S9-010 | BR-070 | REQ-S9-001 | — | Must | 4 |
| FR-S9-033 | The service SHALL issue the contractual notice on a missed target from the approved template, SHALL leave the notice content, the merge fields and the proof of delivery to rwb-comms, SHALL record the template version and the approver, and SHALL start the cure period as a durable timer (GAP-1859; ASM-3045). | CAP-S9-011 | BR-070 | REQ-S9-005 | R-UNI-25 | Must | 4 |
| FR-S9-034 | The service SHALL end a partner contract on the decision of the role the limit names, SHALL recall every open case that partner holds within 5 working days, SHALL re-select each case on the scorecard, and SHALL keep the partner, its instructions, its results and its fees readable after the exit. | CAP-S9-012 | BR-070 | REQ-S9-006 | R-UNI-26 | Must | 4 |
| FR-S9-035 | The service SHALL sample partner contacts and complaints against the conduct rules with the sample size and the rule version recorded, SHALL raise a breach with the sample behind it, SHALL suspend the allocation of the partner, and SHALL report the breach to the review. | CAP-S9-013 | BR-070 | REQ-S9-006 | R-UNI-29 | Must | 4 |
| FR-S9-036 | The service SHALL record an additional partner cost on a held asset against the asset reference the asset module publishes, SHALL attach its evidence, SHALL require the approval the limit names before it is committed, and SHALL record the approver and the date. | CAP-S9-014 | BR-071 | REQ-S9-009 | — | Must | 4 |
| FR-S9-037 | The service SHALL capture a field visit, its photographs and its bills against the case with no network connection, SHALL hold them on the device until it reconnects, SHALL upload the evidence through the document contract, and SHALL record the visit with its time and the collector role. | CAP-S9-015 | BR-071 | REQ-S9-009 | — | Should | 4 |
| FR-S9-038 | The service SHALL bind a partner user to one partner and one partner role with a validity period in `partner_user`, SHALL accept partner access only through the partner gateway with FAPI 2.0 and multi-factor authentication, and SHALL scope every partner answer to the cases of that partner. | CAP-S9-016 | BR-060 | REQ-S9-008 | — | Must | 2 |
| FR-S9-039 | The service SHALL exchange every instruction and every result through the portal paths of the contract, SHALL accept no instruction, result or invoice by email or by file drop as a supported exchange, and SHALL record the channel each exchange arrived on. | CAP-S9-016 | BR-060 | REQ-S9-008 | — | Must | 2 |
| FR-S9-040 | The service SHALL write its decision record in the same transaction as the state change and SHALL publish DecisionRecorded; where the record cannot be written it SHALL change nothing, show MSG-P7-003 and raise an incident. | CAP-S9-018 | BR-060 | No REQ row; module conformance | — | Must | 4 |
| FR-S9-041 | The service SHALL record the business date and load time of every data product it reads at each automatic step, SHALL show a stale product with the date it belongs to and MSG-P1-001, and SHALL hold the step where the freshness cannot be read. | CAP-S9-018 | BR-060 | No REQ row; VR-S9-003-1, VR-S9-005-1, VR-S9-007-1, VR-S9-008-1, VR-S9-013-1 | — | Must | 4 |
| FR-S9-042 | The service SHALL obtain every fact it does not own through a published contract. A read of a `recovery.v_ace_*` view, a read of an ACE table, a call to a service the connection matrix does not give this service, and a constraint in schema `rwb_partner` that references a table outside it, SHALL fail the build and the boundary test. | CAP-S9-018 | BR-060 | No REQ row; module conformance | — | Must | 4 |
| FR-S9-043 | The service SHALL publish its contract before its build starts: the staff resources under `/api/recovery/partner/v1`, the portal resources under `/partner/v1/*`, the topic `rwb.partner.events.v1` with InstructionIssued and PartnerResultSubmitted, the task queue `rwb-partner` with InstructionWorkflow, and the call types it offers and accepts; and every story SHALL build against that contract and its fake. | CAP-S9-018 | BR-060 | No REQ row; module conformance | — | Must | 2 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Source NFR | Priority | Test |
|---|---|---|---|---|---|---|
| NFR-S9-001 | The partner list, the placement and allocation screen, the scorecard screen and the portal instruction screen respond inside the user's wait under the busiest-hour load. | Under 2 seconds at the 95th percentile | BR-060 | NFR-008 | Must | Performance test in system test |
| NFR-S9-002 | The service carries the partner population of the programme across 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers. | About 50 partner users online in the busiest hour of about 320 named users; 48 concurrent partner users at peak | BR-060 | NFR-003 | Must | Volume test at the stated population |
| NFR-S9-003 | A rule evaluation at an allocation, a score or a fee check completes inside the user's wait. | Under 300 milliseconds at the 95th percentile | BR-060 | NFR-011 | Must | Rule timing test with the partner package in force |
| NFR-S9-004 | Every automatic step states the business date and the load time of the data products it read, and a stale product is visible at the step with MSG-P1-001. | Every step | BR-060 | NFR-013, NFR-014 | Must | Hold an ACE batch in system test |
| NFR-S9-005 | The service holds no load window, no staging table and no catch-up job: a late ACE batch holds the step and raises an alert. | No load, no staging, no catch-up | BR-060 | NFR-015 | Must | Hold and release the batch |
| NFR-S9-006 | The service is available during business hours and outside them, when the partner clocks and the portal run. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | BR-060 | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-S9-007 | The service inherits the ACE recovery point and recovery time, and a running instruction resumes where it stopped, including across a Continue-As-New. | The ACE recovery point objective and recovery time objective; workflow history preserved | BR-060 | NFR-022, NFR-023 | Must | Failover, restore and worker-restart test before the first release |
| NFR-S9-008 | An interface failure is retried and then moved to an exception queue with a task for a named owner, and no outbound action is lost. | Three retries per item, then the exception queue | BR-060 | NFR-025, NFR-026 | Must | Force a failure at each interface |
| NFR-S9-009 | Every scheduled job has a run book, monitoring and an alert to the operations channel, and a failing job alerts a named owner. | Alert within 15 minutes to the named owner | BR-070 | NFR-067, NFR-068 | Must | Schedule failure drill |
| NFR-S9-010 | Every partner step is reproducible from the log, including the rule, scorecard and schedule versions and the inputs used. | Every step reproducible | BR-060 | NFR-033 | Must | Re-run a sample of steps from the log |
| NFR-S9-011 | Every instruction, score, review, claim and recall carries the rule version applied and the approver who allowed it. | Every action | BR-070 | NFR-034 | Must | Decision record inspection |
| NFR-S9-012 | The decision log hash chain is checked daily and a break is reported to Compliance the same day. | Daily check, same-day report | BR-060 | NFR-035 | Must | Chain break drill |
| NFR-S9-013 | Party identifiers and contact values are masked at rest and on every screen, portal view and agent call, by role, and each screen and each partner view receives only the personal data it needs. | Masked at rest and in use; data minimisation per screen and per partner view | BR-060 | NFR-039, NFR-040 | Must | Masking matrix test across roles |
| NFR-S9-014 | Every read of a personal field is logged, and the read is refused rather than returned where the log cannot be written. | Every read | BR-060 | NFR-042 | Must | Access log reconciliation against reads |
| NFR-S9-015 | A data subject access, correction or erasure request is worked inside the statutory period, across the partner, the instruction, the result and the field evidence. | Statutory period | BR-060 | NFR-043 | Must | Data subject request drill |
| NFR-S9-016 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | BR-060 | NFR-045 | Must | Environment data review |
| NFR-S9-017 | Every record this service holds carries a data classification that sets its handling. | Classification applied per record | BR-060 | NFR-047 | Must | Classification review |
| NFR-S9-018 | Recovery and partner data stay in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | BR-060 | NFR-046 | Must | Tenancy review |
| NFR-S9-019 | Staff authenticate with single sign-on and multi-factor authentication; a partner account uses multi-factor and is scoped to its own cases; service identities carry the same role checks. | Entra ID single sign-on with multi-factor; partner accounts multi-factor through the partner gateway and scoped; service identities | BR-060 | NFR-050, NFR-051 | Must | Sign-in, partner scope and identity test |
| NFR-S9-020 | Secrets are held in the key store, data is encrypted at rest and in transit, and the build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | No secrets in code or prompts; encrypted; pipeline checks pass | BR-060 | NFR-052, NFR-053, NFR-054 | Must | Pipeline and key store review |
| NFR-S9-021 | Every screen label, validation message and error message is available in Thai and in English. | Every screen, label and message in both languages | BR-070 | NFR-059 | Must | Language review per screen |
| NFR-S9-022 | The screens meet the bank's accessibility standard and run on the browsers the bank supports. | WCAG 2.1 level AA; the current and previous major versions of Microsoft Edge and Google Chrome | BR-060 | NFR-060, NFR-061 | Must | Accessibility and browser test |
| NFR-S9-023 | The partner-facing screens work on the devices partners use, and the field application captures evidence with no network connection and uploads when it reconnects. | Desktop browsers and tablets for field and auction partners; offline capture | BR-071 | NFR-062, NFR-063 | Must | Device and offline drill |
| NFR-S9-024 | The decision log holds one record for every partner step for the full retention period without degrading query time. | About 36 GB for the decision log and the interaction ledger by the end of 2031; a single case history query under 2 seconds at that size | BR-060 | NFR-007 | Must | Query timing at the 2031 size |
| NFR-S9-025 | Logs, traces and metrics are produced across the workflow and the decisions, and the business measures per decision are produced from the decision record and not from a separate count. | Across the workflow and the decisions; measures from the log | BR-070 | NFR-064, NFR-065 | Must | Observability review and measure reconciliation |
| NFR-S9-026 | Every record carries a retention and archive rule by record class, a document is disposed of or extended by a recorded decision, and a legal hold overrides the class. | Retention class per record; periods open under DL26 (GAP-1853; ASM-3034) | BR-060 | NFR-028, NFR-031, NFR-072, NFR-074 | Must | Retention class and legal hold review |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_partner`. Every table carries the record columns of the platform library. The Ownership Map, the Logical Data Model and the physical schema fix three tables for this service (`partner`, `partner_user` and `partner_instruction`) and none for the scorecard, the fee claim, the review, the conduct sample or the field visit that Architecture v5 names as the schema's content, so those five are named as entity groups and the physical names are written with the DB story (GAP-1837; ASM-3018). Retention is stated by class; the periods are open (GAP-1853; ASM-3034).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `partner` | Owned table (Ownership Map; DF-PRT-001 to DF-PRT-007) | `id` (uuid, primary key), `partner_code` (`varchar(20)`, unique), `partner_name` (`varchar(160)`), `partner_type` from LOV-PARTNER-TYPE, `panel_status` from LOV-PANEL (default ACTIVE), `contract_end`, `score` (`numeric(5,2)`), the version in force, and the owner role row of the partner type (GAP-1851; ASM-3032) | [CONFIDENTIAL] | Workbench record; the panel and the terms are loaded here | Workbench record class; period open |
| `partner_user` | Owned table (Ownership Map; DF-REF-212 to DF-REF-217) | `id` (uuid), `identity_ref` (`varchar(64)`, unique), `partner_id`, `role_code` from LOV-ROLE, `valid_from`, `valid_to` (no later than the firm's contract end) | [PII] | The partner gateway identity, bound here | Workbench record class; period open |
| `partner_instruction` | Owned table (Ownership Map; DF-PRT-008 to DF-PRT-016) | `id` (uuid), `case_id` (`varchar(255)` business key, no foreign key; GAP-1838; ASM-3019), `partner_id`, `instruction_type` from LOV-INSTRUCTION, `instructed_at`, `due_at`, `status` from LOV-INSTR-STATUS (default SENT), `result_code` (`varchar(40)`), `fee_amount` (`numeric(18,2)`, baht) | [SENSITIVE_FINANCIAL] | Workbench record; the result and the invoice arrive through the portal | Workbench record class; period open |
| `partner_scorecard` (entity group) | Owned record, one per partner per month | The month, the measures and their weights in force, the measured values, the score, the version of the measures applied, the publication date | [CONFIDENTIAL] | Workbench record, built from the measured results | Workbench record class; period open |
| `fee_claim` (entity group) | Owned record, one per claim per instruction | The claim reference, the instruction, the schedule version applied, the calculated fee, the claimed amount, the difference and its item, the approval level, the approver role and the payment reference | [SENSITIVE_FINANCIAL] | Workbench record; the invoice arrives through the portal | Workbench record class; period open |
| `partner_review` (entity group) | Owned record, one per review per partner | The review date, the six points of the checklist with the version applied, the action, the owner role and the date per point, the breaches considered and the outcome | [CONFIDENTIAL] | Workbench record | Workbench record class; period open |
| `conduct_sample` (entity group) | Owned record, one per sample per partner | The sample month, the sample size, the contacts and complaints sampled, the rule version applied, the breach raised and its evidence, the suspension it caused | [PII], [CONFIDENTIAL] | Workbench record; the contacts and complaints are read through their owners | Workbench record class; period open |
| `field_visit` (entity group) | Owned record, one per visit per case | The case, the partner and the collector role, the visit time and place, the result, the evidence references in the document hub, and the device and upload state | [PII], [CONFIDENTIAL] | The field application; the evidence is held by rwb-document | Workbench record class; period open |
| `outbox_event`, `processed_event`, `idempotency_key` | Platform library objects created in this schema | Library-defined | [CONFIDENTIAL] | Service template | Library policy (PLT) |

The field lists of the scorecard, the fee claim, the review, the conduct sample and the field visit are open: the FSD repeats the same eight columns in ten features and names no other field (GAP-1839; ASM-3020). No copy of an ACE column is held and no foreign key leaves the schema.

## 8.2 Data read but not owned

| Data | Read through | Views behind it | Classification of the data read |
|---|---|---|---|
| Case, party, stage, queue and task facts, and the instruction request that starts this service | rwb-case contract, by the Temporal call the caller makes | none (case schema) | [PII], [SENSITIVE_FINANCIAL] |
| The business date and load time of each data product | rwb-source-data contract (GAP-1835; ASM-3016) | `v_ace_batch_status` behind the contract (the exact view names are not in the sources read) | [CONFIDENTIAL] |
| The matched recovery and the payment outcome | rwb-payment contract, or the source-data contract that carries the outcome (GAP-1836; ASM-3017) | none (payment schema) | [SENSITIVE_FINANCIAL] |
| The document, the upload link and the custody state | rwb-document contract (REST; slide 13) | none (document schema) | [CONFIDENTIAL], [PII] |
| The approval route, the delegation limit and the sealed decision record | rwb-decision contract (Temporal; GAP-1857; ASM-3043) | none (decision schema) | [CONFIDENTIAL] |
| Roles, capability areas, masking policy and the delegation table | rwb-access permission data, cached | none (access schema) | [CONFIDENTIAL] |
| The asset reference, the floor price and the disposal state | rwb-asset contract, or the fact the asset module publishes with its call (GAP-1847; ASM-3028) | none (asset schema) | [SENSITIVE_FINANCIAL] |
| Parameters, the six-point checklist and the reference data the panel reads | rwb-case contract (default rulings, DP-06 and DP-07) | none (case schema) | [CONFIDENTIAL] |
| The contacts and complaints the conduct sample tests | Their owners: rwb-comms for the contact, and the case record for the complaint | none | [PII] |

Counts are not stated: the FSD gives no field count for this module beyond the eight repeated catalog columns, and no count is recomputed here.

## 8.3 Field-level requirements for personal and financial data

The FSD marks all eight repeated catalog columns as not personal data, and the partner, the instruction type and the panel status are firm data. The fields below are personal or financial data and are handled as such by this document.

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| `partner_user.identity_ref` | The partner identity directory reference of the person acting for the firm | [PII] | Masked on every screen; never in an event, a workflow input or a log; every read logged (NFR-S9-013, NFR-S9-014) |
| Partner contact name and contact value in a result | Who the partner spoke to and how | [PII] | Handled by rwb-case and rwb-comms as the owners of the contact; this service carries the result code and the date, not the personal content, in its event |
| `partner_instruction.fee_amount` and the claim amount | What the bank pays the partner | [SENSITIVE_FINANCIAL] | Read by role on the fee screens; not carried in InstructionIssued or PartnerResultSubmitted |
| The matched recovery amount | What the agency recovered | [SENSITIVE_FINANCIAL] | Shown on the fee screen only; no amount in an event |
| `partner.partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, `score` | The firm and its standing | [CONFIDENTIAL] | Shown by role; the score is visible to the partner on PRT-01 only as its own position |
| Conduct sample content naming a customer | The contact or complaint tested | [PII] | Masked by role; held only on the sample record; never in an event |
| Field visit photographs and bills | The evidence captured at the visit | [PII], [CONFIDENTIAL] | Held by rwb-document through the upload link; no document content in a log or an event |
| The instruction, its due date and its status | The work placed with a firm | [CONFIDENTIAL] | Visible to that partner on its own instructions only (NFR-S9-019) |

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code: the panel status, the contract end, the fee schedule, the service levels, the scope, the owner role of each partner type, the scorecard measures and weights, the thresholds, the panel capacity rule, the six-point checklist, the conduct rules and the approval levels (BR-S9-001 to BR-S9-015; FR-S9-002, FR-S9-028, FR-S9-032).
2. This service holds no copy of an ACE column and no staging table; it reads ACE data through a contract only (GAP-1835; ASM-3016).
3. A link to a record of another service is a business-key column with no foreign key, and this applies to `partner_instruction.case_id`, which the Logical Data Model types as a cross-reference to `recovery_case` (GAP-1838; ASM-3019).
4. A personal field is not returned when the access log cannot be written.
5. Personal data is not put in an event, a workflow input or a log; InstructionIssued and PartnerResultSubmitted carry the case, the instruction, the step, the outcome and the versions, not the parties, the contact or the amounts.
6. A record is never deleted on an exit: the partner, its instructions, its results and its fees stay readable after the contract ends, and a legal hold overrides the retention class (NFR-S9-026; GAP-1853; ASM-3034).
7. A partner answer is scoped to its own cases, and the scope is applied by the service and not only by the gateway (NFR-S9-019; FR-S9-038).

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-case (P3) | In and out | Temporal activity on `rwb-partner` from the case and stage workflows; events listened to by rwb-case | P3 | The case starts an instruction and owns the case state, the queues and the timers; it moves on InstructionIssued and PartnerResultSubmitted because it listens to this topic. The slide 13 matrix gives this service no call to P3 (slide 13) |
| rwb-litigation (S4) | In and out | Temporal activity (issueInstruction) and events listened to (InstructionIssued, PartnerResultSubmitted) | S4 | The law firm instruction, the receipt and the court number the firm returns. Slide 13 S4 row: T and E to S9. The service is created after the S4 release (GAP-1845; ASM-3026) |
| rwb-asset (S5) | In and out | Temporal activity (issueInstruction) and events listened to | S5 | The auction vendor and valuer instruction, the round result and the extra cost on a held asset. Slide 13 S5 row: T and E to S9 (GAP-1847; ASM-3028) |
| rwb-document (P5) | Out | REST, one hop, 2 s timeout; the upload link and the partner upload | P5 | The only outgoing call the matrix gives this service besides the partner gateway. Slide 13 S9 row: R to P5 |
| rwb-decision (P7) | Out and in | Temporal activity and child workflow (ApprovalWorkflow); the shared topic `rwb.decision-record.v1` | P7 | The fee approval and the delegation limit. The matrix gives the S9 row no P7 cell, so the path is carried as a gap (GAP-1857; ASM-3043) |
| rwb-payment (P8) | Out and in | Events and the contract of the owner of payment | P8 | The matched recovery, the fee payment and the posting. The matrix gives the S9 row no P8 cell (GAP-1836; ASM-3017) |
| rwb-comms (P6) | Out and in | Temporal child workflow for the contractual notice; the proof-of-delivery event listened to | P6 | The notice on a missed target, its template version and its proof of delivery. The matrix gives the S9 row no P6 cell and no event cell, so both paths are carried as a gap (GAP-1859; ASM-3045) |
| rwb-source-data (P1) | Out | REST, one hop, 2 s timeout, GET retried once with jitter | P1 | The business date and load time of every data product. Slide 13 S9 row: no P1 cell (GAP-1835; ASM-3016) |
| rwb-access (P4) | In | Cached permission data through the guard library, not a call on the hot path | P4 | Roles, capability area PARTNER_PORTAL, masking policy and the delegation table |
| rwb-reporting (P9) | Out | Events and the decision record | P9 | The forum report and the measures. The P9 row of the matrix has no S9 cell (GAP-1858; ASM-3044) |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | SCR-34 Partner list, SCR-35 Placement and allocation, SCR-36 Partner scorecard (GAP-1848; ASM-3029) |
| Partner gateway (DMZ) | In and out | REST under FAPI 2.0 with sender-constrained tokens, PAR, strong client authentication and multi-factor; slide 13 S9 row: R to Outside | Platform edge (RWB-PLT-EDGE) with this service | PRT-01 Partner home, PRT-02 Instruction, PRT-03 Upload result, PRT-04 Invoice; the /partner/v1/* base (GAP-1849; ASM-3030) |
| Kafka topic `rwb.partner.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by case | This service | InstructionIssued (EV-20) and PartnerResultSubmitted (EV-21). EV-20 consumers: the partner portal; EV-21 consumers: rwb-litigation, rwb-asset and rwb-case (slide 43) |
| Shared topic `rwb.decision-record.v1` | Out | CloudEvents 1.0 | P7 | Each local decision record, collected into the central ledger |
| ACE common audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |
| AMIS, the field application and the partner invoice channel | Out and in | Through rwb-integration and the partner gateway, not by a direct call, where a path exists | P2 with the external system | The extra cost and the field evidence (GAP-1847; ASM-3028) |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5 (ADR-018); no extract leaves this service |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Who answers the freshness of each data product and the case facts this module needs, given that the slide 13 matrix gives the S9 row no cell to rwb-source-data and no cell to rwb-case? | Solution architect with P1 and P3 | Five validation rules and every automatic step depend on it, and the boundary test cannot be written until it is fixed (GAP-1835; ASM-3016) |
| Who matches the money and pays the fee, and which path brings the match back to this service, given that the matrix gives the S9 row no cell to rwb-payment while the FSD names ALS and GL? | Solution architect with P8 | The fee claim, the fee payment and the recovery match are the money paths of the product (GAP-1836; ASM-3017) |
| Which call type carries the fee approval to the approval workflow, given that the matrix gives the S9 row no cell to P7 while every other route service shows T to P7? | Solution architect with P7 | A fee approved without the route leaves money leaving the bank on a screen decision (GAP-1857; ASM-3043) |
| How does the forum report reach rwb-reporting, given that the P9 row subscribes to six services and not to this one? | Solution architect with P9 | The review forum report is a Must requirement and the read model is the only permitted reporting path (GAP-1858; ASM-3044) |
| Which service issues the partner instruction for a wave-3 litigation or auction release, and is the capability in E4 or in E6 (BRD Q-019)? | Solution architect with the S4 and S5 owners | Two releases in wave 3 depend on a service created in wave 4 (GAP-1845; ASM-3026; GAP-1482; ASM-2587) |
| What is the start mechanism of InstructionWorkflow: a child workflow the caller starts, or an activity the caller runs on this service's queue? | Solution architect with the platform workflow owner | The workflow contract and the caller's code both depend on it, and both readings appear in the sources (slide 17 and Temporal slide 12) |
| Which path carries the AMIS call and the asset reference, and where is the extra cost approved? | Solution architect with P2 and S5 | The extra cost capability has no confirmed edge (GAP-1847; ASM-3028) |
| Which service issues the contractual notice and proves its delivery, and what starts the cure period when the proof arrives? | Solution architect with P6 | The notice is a Must behaviour of the exit path and this service is given no path to the notice owner (GAP-1859; ASM-3045) |

# 10. Release slicing proposal

The service is wave 4 and serves EP06, whose release is 30 April 2027 (tentative), and EP07, whose release is 31 May 2027 (tentative). Three slices precede the service: the split plan places four stories earlier, and two wave-3 services call it, so the release plan is a contract plan for those slices and a build plan for the two waves. Each slice is a list of capabilities, not stories.

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox, inbox, decision-record and permission-guard libraries, the Temporal workflow kit with the Partner instruction template and the approval child, the schema and login provision, the Kafka event platform and naming library, the edge and the partner gateway route with its FAPI 2.0 profile, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Before wave 4 — the contract slices earlier epics need

| Slice | Wave and release | Capabilities | Why here |
|---|---|---|---|
| 1.1 The partner document path | Wave 1, 30 November 2026 (tentative) | No product capability of this service | The split plan gives RWB-E1-032 and RWB-E1-057 an S9 slice each, and both are document-intake paths that belong to the document hub in wave 1. The slice is a contract obligation on the partner document source, not a build in this service (GAP-1843; ASM-3024) |
| 2.1 The partner identity and the portal contract | Wave 2, 31 December 2026 (tentative) | CAP-S9-016 | The split plan gives RWB-E2-019 and RWB-E2-034 an S9 slice each; PRT-01 Partner home is first needed in E2, and the partner_user binding and the FAPI 2.0 route are what the portal screens need before any panel work (GAP-1844; ASM-3025) |
| 3.1 The instruction contract | Wave 3, 28 February 2027 and 31 March 2027 (tentative) | The published contract of CAP-S9-017: InstructionWorkflow, the activities issueInstruction and recordResult, and the events EV-20 and EV-21 | rwb-litigation releases law firms through the portal at 31 March 2027 (tentative) and rwb-asset releases auction vendors at 28 February 2027 (tentative), while this service is created in wave 4. The contract and its fake let both build and demonstrate on time (GAP-1845; ASM-3026; GAP-1482) |

Rationale: contract-first is the only way to keep three release dates while the service that owns the capability is created in wave 4; the fake is what rwb-case, rwb-litigation, rwb-asset and the seven screens test against until wave 4 lands. The rule in R5.6 applies: a story whose wave map wave is earlier than its service's wave keeps the wave map wave.

## 10.3 Wave 4 — EP06 (release 30 April 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 6.1 The record, the contract and the boundary | CAP-S9-018 | Every later slice writes a decision record, and the boundary test must fail the build on a read the matrix does not give this service from the first story |
| 6.2 The panel and the terms | CAP-S9-001, CAP-S9-002 | Allocation by measured return needs the panel, the fee schedule, the service levels and one owner role per type as data before any work is placed |
| 6.3 Allocation, the override and the partner clock | CAP-S9-003, CAP-S9-004, CAP-S9-017 | Allocation by habit is the practice the product replaces, and the clock is what makes a late partner visible |
| 6.4 The instruction and the result | CAP-S9-005 | A result that arrives tomorrow is a case that waits, and the same-day result is the value the portal brings |
| 6.5 The placement, the recovery and the fee | CAP-S9-006, CAP-S9-007 | Recovery after charge-off is a revenue stream, and a fee with no schedule behind it cannot be defended |

Rationale: the EP06 slice is the smallest set that delivers the panel, the allocation, the instruction, the result, the placement and the fee for the panel, and each slice is independently demonstrable. Every capability of EP06 is Must, so no slice may slip without holding the release.

## 10.4 Wave 4 — EP07 (release 31 May 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 7.1 The monthly score and the measures | CAP-S9-008 | A panel that is not scored is a panel that is not managed, and the score is the input to the next month's allocation |
| 7.2 The fee claim and its approval | CAP-S9-009 | Money leaving the bank on a partner's own invoice is money with no control |
| 7.3 The review on the six points | CAP-S9-010 | The six points are the same for every partner type, so one review behaviour covers the panel |
| 7.4 The notice, the cure period and the exit | CAP-S9-011, CAP-S9-012 | A missed target with no notice and an exit with no recall leave work with a firm the bank has ended |
| 7.5 Conduct and the suspension | CAP-S9-013 | A breach found by a customer complaint is the control arriving too late |
| 7.6 The extra cost and the field visit | CAP-S9-014, CAP-S9-015 | Field evidence that is not captured on the case is not evidence; CAP-S9-015 is Should and may slip inside the wave without holding the release |

Rationale: EP07 is the management half of the product and depends on a month of measured results from EP06, which is why it sits one release later inside the same wave. The service wave and both business epic waves are 4, so no capability of E6 or E7 sits in a later wave than its epic (section 10.3 of the program BRD).

## 10.5 Later increments

| Increment | What unlocks it |
|---|---|
| The partner rule set as a governed package | Phase 2 of the Drools design, with the allocation, scoring, review, fee and conduct rules authored from the FSD, their version label and their owner in rwb-decision (GAP-1840; ASM-3021) |
| The scorecard measures, weights and thresholds at full width | The measures agreed by the partner and agency manager with the center of excellence (GAP-1856; ASM-3037) |
| The five remaining entity groups' physical tables | The data architect's table list, added with the DB story (GAP-1837; ASM-3018) |
| The scorecard and conduct Schedules in the job map | The two rows added to the job map with their run books (GAP-1841; ASM-3022) |
| The forum report at full width | The S9 to P9 edge agreed, so that the read model carries the score, the review and the conduct result (GAP-1858; ASM-3044) |
| The fee approval route confirmed | The P7 path agreed and the S9 cell added to the matrix (GAP-1857; ASM-3043) |
| The partner portal at full width | The partner gateway live in the DMZ with its penetration test, and the four portal screens owned (GAP-1848; GAP-1849; NFR-S9-019) |
| Retention periods for the partner records | The DL26 answer from Compliance (GAP-1853; ASM-3034) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in system test against synthetic data; no production data is used. The FSD's own acceptance criteria are one generic statement per feature (GAP-1842; ASM-3023), so each criterion below is a product-level statement of the rule that feature names.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-S9-001 | FR-S9-001, FR-S9-005 | a partner to be onboarded with no record on the panel, and a second partner whose fee schedule is absent | each is saved, and the second is moved to ACTIVE | the first is on the panel with its code, name, type from LOV-PARTNER-TYPE, status from LOV-PANEL and contract end, and a version; the second stays below ACTIVE with the missing item named, and a save with a required field empty shows MSG-GEN-001 | AC-S9-001-01; VR-S9-001-1; BR-S9-001 |
| AC-S9-002 | FR-S9-002, FR-S9-028 | a fee schedule and a set of scorecard measures in force | a new version is loaded with a valid-from date and an instruction and a score are taken after it | each step reads the new version and records the version applied, and no code release is needed | AC-S9-002-01; BR-S9-002; AC-S9-008-01 |
| AC-S9-003 | FR-S9-003 | a partner type with an owner role, and a second type with none | work is allocated for each type | the first allocates and records the owner role; the second is refused as unowned and the refusal is on the record | AC-S9-002-01; REQ-S9-002; GAP-1851 |
| AC-S9-004 | FR-S9-004 | a user whose role lacks capability area PARTNER_PORTAL | the user opens the panel and attempts an override | the action is refused with MSG-P4-002 and the partner, the instruction and the case are unchanged | AC-EXC-S9-001-01 to AC-EXC-S9-015-01; VR-S9-002-1 |
| AC-S9-005 | FR-S9-006, FR-S9-007 | a panel of five agencies with different scores, capacities and panel statuses | an instruction is requested, then requested again with the highest-scoring agency suspended | the first choice is the one the scorecard rule picks and the score, the capacity, the status and the rule version are on the record; the second choice skips the suspended agency and states the rule and the status that moved it | AC-S9-003-01; R-UNI-29 |
| AC-S9-006 | FR-S9-008, FR-S9-009 | an instruction allocated to one partner | the partner and agency manager overrides it to another partner, then attempts an override to a suspended partner | the override records the partner, the role, the reason and the date and is counted in the monthly rate; the second attempt is refused and the instruction is unchanged | AC-S9-004-01; KPI-011 |
| AC-S9-007 | FR-S9-010, FR-S9-018 | a case that needs a partner, and a worker stopped across the due date | the instruction is issued and the worker restarts after the due date | the instruction is at SENT with its type, dates and calling service, InstructionWorkflow holds the service level timer of the partner type, the timer resumes where it stopped, and no Quartz table, connection or job exists | AC-S9-003-01; Temporal and Drools Design v1 slide 25; DP-10 |
| AC-S9-008 | FR-S9-011 | an instruction and its state change | the transaction commits | InstructionIssued is on `rwb.partner.events.v1` as a CloudEvents 1.0 message keyed by case, written through the outbox in the same transaction, with no party and no amount in it | AC-S9-003-01; ADR-015; DP-09 |
| AC-S9-009 | FR-S9-012, FR-S9-013 | an instruction at SENT | the partner declines it through the portal, then the next partner accepts it | the first is at DECLINED with its reason and is not chosen again for the instruction; the next partner is selected on the scorecard and the second instruction is at ACCEPTED | AC-S9-003-01; R-UNI-45; LOV-INSTR-STATUS |
| AC-S9-010 | FR-S9-014, FR-S9-015 | an instruction at ACCEPTED with its clock running | the first service level passes with no result, then the second passes | the partner is chased once with the first miss; the second miss recalls the work with its reason, the instruction is at RECALLED, the next partner is selected within 2 working days and the new clock starts at the re-issue | AC-S9-005-01; R-UNI-25; R-UNI-45 |
| AC-S9-011 | FR-S9-016, FR-S9-034 | a partner holding 40 open cases | the contract is ended | the contract end is recorded with the role that decided it, every one of the 40 cases is recalled within 5 working days with its reason, each is re-selected on the scorecard, and the partner, its instructions, its results and its fees are still readable | AC-S9-012-01; R-UNI-26 |
| AC-S9-012 | FR-S9-016, FR-S9-017 | a partner that declares a conflict, and a second partner that becomes insolvent | each event is recorded | the conflict recalls the affected work within 2 working days; the insolvency recalls every open case the same day, stops the fee payments with their date and role, and lists the documents and the cash to secure | AC-S9-012-01; R-UNI-27; R-UNI-28 |
| AC-S9-013 | FR-S9-019, FR-S9-020 | a charged-off account whose treatment is soft recovery | a panel with an agency that has capacity is read, then the same account is read against a panel with no capacity | the first places the account with the agency chosen on measured return through an instruction of type COLLECT with its terms and end date; the second holds the placement with its cause and escalates on the timer | AC-S9-006-01; R-WO-30; R-WO-31 |
| AC-S9-014 | FR-S9-021 | a placement whose measured return falls below the panel threshold, and a second whose conduct breaches are above zero | the monthly test runs | each placement is recalled with its reason and the account is placed with the next agency on the scorecard | AC-S9-006-01; R-WO-34; R-WO-35 |
| AC-S9-015 | FR-S9-022, FR-S9-023 | an instruction at ACCEPTED, and a second already at DONE | a result is reported against each through the portal | the first is at DONE the same day with its result code and date, its evidence is attached through the document contract, and PartnerResultSubmitted is published; the second is refused with the status that refused it and nothing changes on the case | AC-S9-005-01; R-WO-33; LOV-INSTR-STATUS |
| AC-S9-016 | FR-S9-024 | money reported as recovered by an agency, including one payment that matches no case | the match from the owner of payment is read, and the unmatched payment is reviewed | the matched recovery is on the case and the instruction with its amount and value date, and the recovery this service cannot match is shown with its value date until the owner of payment matches it | AC-S9-007-01; GAP-1836 |
| AC-S9-017 | FR-S9-025, FR-S9-029 | a fee schedule in force and a recorded result, and a claim against it that is 4 percent higher | the fee is calculated and the claim is checked | the calculated fee carries the schedule version applied, and the claim is refused with the difference and the item that differs shown | AC-S9-007-01; AC-S9-009-01; BR-S9-009 |
| AC-S9-018 | FR-S9-030, FR-S9-031 | a fee claim that agrees with the schedule and the result | the claim is approved | the approval carries the level the limit names, the approver role and the rule version; no payment is made by this service and the approved claim is published as the fact the owner of payment acts on | AC-S9-009-01; GAP-1857 |
| AC-S9-019 | FR-S9-026 | the month end of a month with measured results | the monthly run starts | the scorecard and the conduct sample run from a Temporal Schedule in `rwb-partner`, each states the data date it ran on, and no Quartz table, connection or job exists | AC-S9-008-01; AC-S9-013-01; DP-10; GAP-1841 |
| AC-S9-020 | FR-S9-027 | a month of scores, reviews, conduct results and overrides | the forum report is read | the score, the review outcome, the conduct result and the override rate are produced from the decision record and published for rwb-reporting, and no extract is written to an external tool | AC-S9-008-01; ADR-018; DP-17; GAP-1858 |
| AC-S9-021 | FR-S9-032 | a partner review under way on the six points of REQ-S9-001 | one point is left without an action, then all six are completed and the review is finished | the first cannot be completed and the missing point is named; the second is completed with an action, an owner role and a date for each point, and the checklist version is on the record | AC-S9-010-01; REQ-S9-001 |
| AC-S9-022 | FR-S9-033 | a partner that has missed its targets and a current approved template | the notice is issued | the notice leaves from the approved template through rwb-comms, the case records the template version and the approver, and the cure period runs as a durable timer that resumes after a restart | AC-S9-011-01; R-UNI-25 |
| AC-S9-023 | FR-S9-035 | a sample of partner contacts and complaints drawn against the conduct rules | the sample is analysed and one breach is upheld | the breach is raised with the sample and the rule version behind it, the allocation of that partner is suspended, and the breach is reported to the review | AC-S9-013-01; R-UNI-29 |
| AC-S9-024 | FR-S9-036 | an additional partner cost on a held asset, with its evidence | the cost is recorded, then approved at the level the limit names | the cost is on the case against the asset reference with its evidence, the approval records the approver and the date, and no cost is committed before that approval | AC-S9-014-01 |
| AC-S9-025 | FR-S9-037, NFR-S9-023 | a field collector with no network connection at a visit | the visit, its photographs and its bills are captured and the device reconnects | the visit is held on the device, then reaches the case with its time and collector role, and the evidence reaches rwb-document through the upload link | AC-S9-015-01; NFR-062 |
| AC-S9-026 | FR-S9-038, FR-S9-039, NFR-S9-019 | a partner user of one firm, and a sign-in attempt from outside the partner gateway | the partner user signs in and requests another firm's instruction, and the second attempt is made on the staff route | the user reaches its own cases only through the partner gateway with multi-factor authentication, the partner user is bound to one firm and one role with validity, the other firm's answer is refused, the staff route refuses a partner identity, and no email or file drop path is accepted as an exchange | AC-S9-001-01; AC-EXC-S9-001-01; REQ-ACA-012; NFR-050 |
| AC-S9-027 | FR-S9-040 | a state change and a decision log store that is unavailable | the action is taken | nothing changes, MSG-P7-003 is shown, an incident is raised, and the decision record and DecisionRecorded are written only when the store is available | AC-EXC-S9-001-02 to AC-EXC-S9-015-02; NFR-034 |
| AC-S9-028 | FR-S9-041, NFR-S9-004 | a data product that belongs to an earlier business date | an automatic step reads it | the step states the business date and the load time, shows the product as stale with the date it belongs to and MSG-P1-001, and holds rather than proceeding | VR-S9-003-1; VR-S9-005-1; VR-S9-007-1; VR-S9-008-1; VR-S9-013-1 |
| AC-S9-029 | FR-S9-042, FR-S9-043 | the service build and its contract | the build runs, and a change adds a read of a view and a call the matrix does not give this service | the build fails on the read and on the call, and the contract publishes the staff base, the portal base, the topic with its two events, the task queue with its workflow and its call types before the first application story | Architecture v5 slide 13; ADR-014; ADR-020 |
| AC-S9-030 | NFR-S9-001, NFR-S9-002, NFR-S9-003 | the stated partner population and the busiest-hour load | the partner list, the allocation screen, the scorecard and the portal instruction screen are used | each responds under 2 seconds at the 95th percentile, the service carries about 50 partner users online of about 320 named users across 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers, and a rule evaluation completes under 300 milliseconds at the 95th percentile | NFR-008; NFR-003; NFR-011 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| BR-059 (REQ-S7-006, REQ-S7-007; FEAT-PRM-06 has no REQ-S9 row) | CAP-S9-006 | FR-S9-019, FR-S9-020, FR-S9-021 | NFR-S9-002, NFR-S9-006, NFR-S9-019 | AC-S9-013, AC-S9-014 |
| BR-060 (REQ-S9-001, REQ-S9-002, REQ-S9-003, REQ-S9-004, REQ-S9-008) | CAP-S9-001, CAP-S9-002, CAP-S9-003, CAP-S9-004, CAP-S9-005, CAP-S9-007, CAP-S9-016, CAP-S9-018 | FR-S9-001, FR-S9-002, FR-S9-003, FR-S9-004, FR-S9-005, FR-S9-006, FR-S9-007, FR-S9-008, FR-S9-009, FR-S9-011, FR-S9-022, FR-S9-023, FR-S9-024, FR-S9-025, FR-S9-038, FR-S9-039, FR-S9-040, FR-S9-041, FR-S9-042, FR-S9-043 | NFR-S9-001, NFR-S9-002, NFR-S9-003, NFR-S9-004, NFR-S9-005, NFR-S9-006, NFR-S9-007, NFR-S9-008, NFR-S9-010, NFR-S9-012, NFR-S9-013, NFR-S9-014, NFR-S9-015, NFR-S9-016, NFR-S9-017, NFR-S9-018, NFR-S9-019, NFR-S9-020, NFR-S9-022, NFR-S9-024, NFR-S9-026 | AC-S9-001, AC-S9-002, AC-S9-003, AC-S9-004, AC-S9-005, AC-S9-006, AC-S9-007, AC-S9-008, AC-S9-009, AC-S9-015, AC-S9-016, AC-S9-017, AC-S9-018, AC-S9-026, AC-S9-027, AC-S9-028, AC-S9-029, AC-S9-030 |
| BR-070 (REQ-S9-005, REQ-S9-006, REQ-S9-007) | CAP-S9-008, CAP-S9-009, CAP-S9-010, CAP-S9-011, CAP-S9-012, CAP-S9-013, CAP-S9-017 | FR-S9-010, FR-S9-012, FR-S9-013, FR-S9-014, FR-S9-015, FR-S9-016, FR-S9-017, FR-S9-018, FR-S9-026, FR-S9-027, FR-S9-028, FR-S9-029, FR-S9-030, FR-S9-031, FR-S9-032, FR-S9-033, FR-S9-034, FR-S9-035 | NFR-S9-009, NFR-S9-011, NFR-S9-021, NFR-S9-025 | AC-S9-010, AC-S9-011, AC-S9-012, AC-S9-019, AC-S9-020, AC-S9-021, AC-S9-022, AC-S9-023 |
| BR-071 (REQ-S9-009, Should) | CAP-S9-014, CAP-S9-015 | FR-S9-036, FR-S9-037 | NFR-S9-023 | AC-S9-024, AC-S9-025 |

BR coverage: 4 of the 4 BRD requirements that name this service (BR-059, BR-060, BR-070, BR-071) are covered by at least one functional requirement, and every functional requirement traces to one of them. Three traces need a note. REQ-S9-002 (one named owner per partner type) is served by no FSD feature and is carried by FR-S9-003, which is a coverage gap in the FSD and not in this document (GAP-1851; ASM-3032). FEAT-PRM-06 (a charged-off account placed with an agency) has no REQ-S9 row of its own; BR-059 sources it from REQ-S7-006 and REQ-S7-007, so the trace runs through BR-059 (GAP-1854; ASM-3035). REQ-S9-009 is the only Should requirement of this module and it is covered by two functional requirements, of which FR-S9-037 may slip inside the wave. No BRD requirement of this module is left without a functional requirement.

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Boundary and conformance test output in system test | FR-S9-042, FR-S9-043 | Developer with the security administrator |
| Contract test against the case, document, decision, payment, source-data and asset contracts and their fakes | FR-S9-022, FR-S9-030, FR-S9-031, FR-S9-036, FR-S9-038, FR-S9-042 | Developer with P3, P5, P7, P8, P1 and S5 |
| Panel drill: a partner onboarded, a missing fee schedule, a versioned load and the owner role of each type | FR-S9-001 to FR-S9-005 | Reference data administrator with the QA team |
| Allocation drill on a panel of five agencies with different scores, capacities and statuses, and the override matrix | FR-S9-006 to FR-S9-009, NFR-S9-003 | Partner and agency manager with the QA team |
| Instruction drill: issue, accept, decline, chase, recall, re-select, and a worker restart across a service level | FR-S9-010 to FR-S9-018, NFR-S9-007 | QA team with the platform administrator |
| Result drill: a result the same day, a result on a closed instruction, an evidence upload and the published event | FR-S9-022, FR-S9-023, FR-S9-011 | Case owner with the QA team |
| Placement drill: an agency with capacity, a panel with none, an underperforming placement and the replacement | FR-S9-019, FR-S9-020, FR-S9-021 | Partner and agency manager with the credit administration |
| Recovery and fee drill: a matched recovery, an unmatched payment, a fee from the schedule and a claim that differs | FR-S9-024, FR-S9-025, FR-S9-029 | Credit administration with the Finance and CFO delegate |
| Monthly Schedule drill: the scorecard and the conduct sample from a Temporal Schedule, with a missed run and its alert | FR-S9-026, NFR-S9-009 | QA team with the platform administrator |
| Forum report reconciliation against the decision record | FR-S9-027, FR-S9-025 | Internal audit with the conduct and QA officer |
| Fee approval matrix across the delegation levels and the approver path | FR-S9-030, FR-S9-031 | Finance and CFO delegate with the QA team |
| Review drill: a review that skips a point, and one that completes on all six | FR-S9-032 | Conduct and QA officer |
| Notice and cure drill, including a restart across the cure period | FR-S9-033 | Partner and agency manager with the QA team |
| Exit, conflict, insolvency and breach drill: every open case recalled inside its time limit, and the record readable after | FR-S9-016, FR-S9-017, FR-S9-034, FR-S9-035 | Head of the partner type with the QA team |
| Conduct sample drill, with a breach upheld and the suspension applied | FR-S9-035 | Conduct and QA officer with P7 |
| Extra-cost drill: recorded against the asset reference, approved before commitment | FR-S9-036 | NPA and asset manager with S5 |
| Field drill: capture with no network connection, upload on reconnect, evidence in the document hub | FR-S9-037, NFR-S9-023 | Field collector with the QA team |
| Partner identity drill: sign-in through the partner gateway, scope to its own cases, a staff route refusing a partner identity | FR-S9-038, FR-S9-039, NFR-S9-019 | Security administrator with Compliance |
| Masking matrix, access log reconciliation, classification review and the data subject request | NFR-S9-013 to NFR-S9-018, NFR-S9-026 | Compliance and PDPA officer |
| Performance and volume test at the stated partner population | NFR-S9-001, NFR-S9-002, NFR-S9-003 | QA team |
| Decision reproducibility and a QA sample of closed instructions | FR-S9-040, NFR-S9-010, NFR-S9-011 | Internal audit with the conduct and QA officer |

# 12. Open questions

The BRD open question Q-019 names this module and is carried forward at OQ-S9-10. Q-023 asks for the first-time-right baseline of case packs and write-off returns, and no requirement of this module carries it, so it is not repeated here. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-S9-01 | Which path carries the case facts and the freshness of each data product into this service, given that the matrix gives the S9 row no cell to rwb-source-data and no cell to rwb-case while five validation rules read the freshness? | Solution architect with P1 and P3 | Before wave 1 system test | CAP-S9-018 | GAP-1835; ASM-3016 |
| OQ-S9-02 | Who matches the money recovered by an agency and pays the fee, and which path brings the match and the payment outcome back to this service? | Solution architect with P8 | Before wave 4 system test | CAP-S9-007, CAP-S9-009 | GAP-1836; ASM-3017 |
| OQ-S9-03 | Which tables hold the scorecard, the fee claim, the review, the conduct sample and the field visit in schema `rwb_partner`, given that the map, the model and the schema list three tables for six items? | Data architect | Before the S9 DB story | CAP-S9-008, CAP-S9-009, CAP-S9-010, CAP-S9-013, CAP-S9-015 | GAP-1837; ASM-3018 |
| OQ-S9-04 | Is `partner_instruction.case_id` a cross-reference `uuid` with a foreign key to `recovery_case` as the model types it, or a business key with no foreign key as ADR-014 requires? | Data architect | Before the S9 DB story | CAP-S9-003 to CAP-S9-007 | GAP-1838; ASM-3019 |
| OQ-S9-05 | Which fields carry the score, the fee claim, the review point, the conduct breach and the field visit, given that the FSD repeats eight columns in ten features and lists none of them? | Business analyst, S9 with the data architect | Before wave 4 story writing | CAP-S9-008 to CAP-S9-015 | GAP-1839; ASM-3020 |
| OQ-S9-06 | Which rules govern the allocation, the score, the review, the fee check, the conduct sample and the field capture, and who authors them, given that the routing logic holds no partner rule set? | Center of excellence analyst with P7 | Before wave 4 release | CAP-S9-003, CAP-S9-004, CAP-S9-008 to CAP-S9-015 | GAP-1840; ASM-3021 |
| OQ-S9-07 | What triggers the monthly scorecard and the conduct sample, and who adds the two rows to the job map? | Solution architect with the platform workflow owner | Before wave 4 system test | CAP-S9-008, CAP-S9-013 | GAP-1841; ASM-3022 |
| OQ-S9-08 | Why is every acceptance criterion in this module the same generic statement, and who writes the step-specific criteria before the stories are cut? | Business analyst, S9 | Before wave 4 story writing | All capabilities | GAP-1842; ASM-3023 |
| OQ-S9-09 | Do the four stories the split plan places in wave 1 and wave 2 stay contract-only slices, and who owns the published partner identity and portal contract until wave 4? | Solution architect with the programme manager | Before wave 1 system test | CAP-S9-016 | GAP-1843; GAP-1844; ASM-3024; ASM-3025 |
| OQ-S9-10 | Is the partner instruction capability in E4 or in E6 (BRD Q-019), and how do the wave-3 litigation and auction releases instruct a law firm and a vendor before this service exists? | Solution architect with the S4 and S5 owners | Before wave 3 system test | CAP-S9-017 | GAP-1845; ASM-3026; GAP-1482; ASM-2587 |
| OQ-S9-11 | Does the forum report and the scorecard reach rwb-reporting through events, given that the P9 row subscribes to no partner topic and the data lake is removed? | Solution architect with P9 | Before wave 4 release | CAP-S9-008 | GAP-1846; GAP-1858; ASM-3027; ASM-3044 |
| OQ-S9-12 | Which path carries the AMIS call, and where is the additional partner cost on a held asset approved? | Solution architect with P2 and S5 | Before wave 4 system test | CAP-S9-014 | GAP-1847; ASM-3028 |
| OQ-S9-13 | Which service owns each of the seven screens, and where does each cell in the screen matrix route from? | Solution architect with the platform edge owner | Before wave 2 system test | CAP-S9-016, CAP-S9-001, CAP-S9-003, CAP-S9-008 | GAP-1848; ASM-3029 |
| OQ-S9-14 | Do the staff paths keep `/api/recovery/partner/v1` and the portal paths `/partner/v1/*`, and which one does the service contract publish? | Solution architect with the platform edge owner | Before the S9 contract story closes | CAP-S9-016, CAP-S9-018 | GAP-1849; ASM-3030 |
| OQ-S9-15 | Is the capability area of this module PARTNER_PORTAL, and are LOV-INSTRUCTION and LOV-INSTR-STATUS the lists of the instruction? | Security administrator with the business analyst, S9 | Before wave 4 release | CAP-S9-002, CAP-S9-016, CAP-S9-017 | GAP-1850; ASM-3031 |
| OQ-S9-16 | Where is the owner role of each partner type held, given that REQ-S9-002 is Must and no feature or field carries it? | Partner and agency manager with the business analyst, S9 | Before wave 4 release | CAP-S9-002 | GAP-1851; ASM-3032 |
| OQ-S9-17 | Which service holds the partner identity binding, given that REQ-ACA-012 is delivered by rwb-access in wave 1 and `partner_user` is this service's table? | Security administrator with P4 and S9 | Before wave 2 system test | CAP-S9-016 | GAP-1852; ASM-3033 |
| OQ-S9-18 | What retention class and what period apply to the partner, the instruction, the partner user and the field evidence (DL26)? | Compliance and PDPA officer | Before wave 4 release | CAP-S9-006, CAP-S9-012, CAP-S9-015 | GAP-1853; ASM-3034 |
| OQ-S9-19 | Does this service own the placement instruction, or does S7 own the placement as its own requirement row says, and what is the boundary between the two? | Solution architect with the S7 owner | Before wave 4 system test | CAP-S9-006 | GAP-1854; ASM-3035 |
| OQ-S9-20 | Who owns the wording of the module's own messages, and who approves the Thai and the English versions (DL10)? | Business analyst, S9 with Legal counsel and Compliance | Before wave 4 release | All capabilities | GAP-1855; ASM-3036 |
| OQ-S9-21 | What are the scorecard measures, their weights, the thresholds and the panel capacity rule? | Partner and agency manager with the center of excellence analyst | Before wave 4 release | CAP-S9-003, CAP-S9-008 | GAP-1856; ASM-3037 |
| OQ-S9-22 | Which call type carries the fee approval to the approval workflow, given that the matrix gives this service no cell to rwb-decision? | Solution architect with P7 | Before wave 4 system test | CAP-S9-009, CAP-S9-018 | GAP-1857; ASM-3043 |
| OQ-S9-23 | Which service issues the contractual notice on a missed target and who proves its delivery, given that the matrix gives this service no cell to rwb-comms and no event cell at all? | Solution architect with P6 | Before wave 4 system test | CAP-S9-011 | GAP-1859; ASM-3045 |
| OQ-S9-24 | What is the start mechanism of InstructionWorkflow: a child workflow the caller starts, or an activity the caller runs on this service's queue? | Solution architect with the platform workflow owner | Before the S9 contract story closes | CAP-S9-017, CAP-S9-018 | Architecture v5 slide 17; Temporal and Drools Design v1 slide 12; GAP-1845 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (ASM-3038).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 5.16 (S9 requirements, REQ-S9-001 to REQ-S9-009), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan, E4 to E7), 9 (DL06, DL10, DL11, DL18, DL26), 10.1 to 10.6 (the service epic RWB-SVC-S9, schema, wave and contract-first delivery), 11 (the trace of each requirement to its service epic and wave) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 7.3 (epics, services and waves under D-RCV-60), 8.4 (BR-059, BR-060), 8.5 (BR-070, BR-071), 9 (RULE-021, RULE-023, RULE-024), 10 (KPI-011), 11 (ASM-026, DEP-005, DEP-007, DEP-009, RISK-007), 12 (Q-019, Q-023), 13 (governance), 14 (traceability) |
| Recovery Workbench FSD S9 Partner management v3 | Document control, Existing capability check, A1.1 to A1.4 (scope, the fifteen features, background, preconditions), A2.1 to A2.15 (functional decomposition with validation rules, business rules, field catalog, roles and acceptance criteria), Requirements served (REQ-S9-001 to REQ-S9-009), Screens (SCR-34 to SCR-36, PRT-01 to PRT-04), Appendix A and B |
| Recovery Workbench Business Rules and Routing Logic v4 | The universal rules R-UNI-25 to R-UNI-29 and R-UNI-45, the placement rules R-WO-30 to R-WO-35, the firm selection rules R-LIT-24 to R-LIT-29, and the ten route sets that hold no partner rule set |
| Recovery Workbench Logical Data Model and Data Dictionary v8 | The `partner`, `partner_instruction` and `partner_user` tables and their fields DF-PRT-001 to DF-PRT-016 and DF-REF-212 to DF-REF-217; LOV-PARTNER-TYPE, LOV-PANEL, LOV-INSTRUCTION, LOV-INSTR-STATUS and LOV-CAPABILITY |
| Recovery Workbench Architecture v5 | Slides 4 and 9 to 13 (19 modules, call types, timeouts, retry and the connection matrix S9 row), 17 (the S9 contract), 29 (one schema and login per service), 37 (what changes and why, including the removal of the data lake), 38 (waves), 41 (service catalogue), 42 and 43 (event catalogue), 44 (job map), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Slide 5 (the nine journeys and the rule sets), slide 12 (the workflow kit and where it is used), slide 25 (S9 Partner management: the seven steps, the Drools decisions, the approvals, the clocks and the point of no return) |
| Recovery Workbench Microservice Ownership Map v1 | Services, tables (`partner`, `partner_user`, `partner_instruction`), endpoints (six S9 rows), events (EV-20, EV-21), workflows (InstructionWorkflow), jobs (no S9 row) and the rulings |
| Recovery Workbench Non Functional Specification v3 | The numeric targets carried in section 7 |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (U1 to U10), R3 (R-PREC), R5 (services, naming, decoupling patterns, wave map and lanes), R8 (header and versioning) and R9 (placeholder and register rules) |
| _work/msr/plan/split_plan.json | `stats` (1,034 slices, 358 legacy stories, 939 Day-1 stories, 510 lanes) and `legacy` (the twenty legacy stories that carry an S9 slice, in waves 1, 2 and 4) |
| _work/msr/plan/ids.json | The realignment decision D-RCV-60 and the ADR and Decision Log identifiers this document cites |
