SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD S7 rwb-writeoff v1
description: Product requirements for the Recovery Workbench write-off and recovery service (S7 rwb-writeoff) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S7 Write-off and recovery v3.md
service: S7 rwb-writeoff
epic: RWB-SVC-S7
wave: 4
decision: D-RCV-60
---

# Recovery Workbench PRD S7 rwb-writeoff v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD S7 rwb-writeoff |
| Document ID | S7-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | S7 rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 (Epic 6, debt sale and write-off, wave 4) |
| Schema | `rwb_writeoff` |
| REST base | `/api/recovery/writeoff/v1` |
| Topic | `rwb.writeoff.events.v1` |
| Temporal task queue | `rwb-writeoff` |
| Java package | `th.co.scb.ace.workbench.recovery.writeoff` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Business analyst, S7 |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), ADR-010, ADR-013 to ADR-023 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epics 3 to 8 v1; FSD S7 Write-off and recovery v3; Architecture v5; Temporal and Drools Design v1; Business Rules and Routing Logic v4; Logical Data Model and Data Dictionary v8; Non Functional Specification v3 |
| Upstream requirement IDs | REQ-S7-001 to REQ-S7-008; BR-051, BR-052, BR-053, BR-054, BR-055, BR-056, BR-057, BR-058, BR-059; RULE-019, RULE-020, RULE-021, RULE-022; R-WO-01 to R-WO-51 |
| Upstream acceptance criteria | AC-S7-001-01 to AC-S7-016-01 (main success flow, one per feature); AC-EXC-S7-001-01 to AC-EXC-S7-016-01 (role without the right); AC-EXC-S7-001-02 to AC-EXC-S7-016-02 (decision cannot be recorded); AC-BG-S7-001-01 to AC-BG-S7-016-01 (the monthly write-off scan). The FSD defines no alternate flow for any of the sixteen features |
| Generated IDs | CAP-S7-001 to CAP-S7-017; FR-S7-001 to FR-S7-041; NFR-S7-001 to NFR-S7-036; AC-S7-001 to AC-S7-026; JRN-S7-01 to JRN-S7-06; ROL-S7-01 to ROL-S7-14; OQ-S7-01 to OQ-S7-17 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD S7 Write-off and recovery v3 (15 November 2026) and Business Requirements Epics 3 to 8 v1, realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD S7 Write-off and recovery v3. Its requirement IDs, feature IDs, rule IDs and acceptance criterion IDs are carried unchanged; the microservice realignment changes the read path, the writer of the posting, the owner of the pack document and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Write-off eligibility waits on the ACE ALS batch; write_off mirrored GL fields left for DEF-05. Everything else unchanged from v2 |
| 1 and 2 | Not specified in the source documents (GAP-1810; ASM-2986) | Earlier versions of the FSD. Their dates and change notes are not in the sources read, and are carried as an open item rather than reconstructed |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, journey and open-question IDs are new; the FSD requirement IDs (REQ-S7-001 to REQ-S7-008), feature IDs (FEAT-WOF-01 to FEAT-WOF-16), validation rule IDs (VR-S7-001-1 to VR-S7-016-1), business rule IDs (BR-S7-001 to BR-S7-016), routing rule IDs (R-WO-01 to R-WO-51), acceptance criteria IDs (AC-S7-001-01 to AC-S7-016-01 and their exception and background rows), message IDs (MSG-S7-001, MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001), the list IDs (LOV-STAGE, LOV-TREATMENT, LOV-ROUTE-SET, LOV-CAPABILITY), the case states named by the routing rules (SCAN_DUE to CASE_CLOSED) and the screen ID (SCR-27) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the program requirements REQ-S7-001 to REQ-S7-008 (section 5.14) and of the non-functional requirements (section 6) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-051 to BR-059, RULE-019 to RULE-022, KPI-009, the E6 scope, the assumptions ASM-013 and ASM-014, the risks and the open questions Q-006, Q-007, Q-012 and Q-023 |
| Recovery Workbench Functional Specifications by Module v6, FSD S7 Write-off and recovery v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Business Rules and Routing Logic v4 | Rules | Source of R-WO-01 to R-WO-51, the twenty-plus case states of D9 and the service level of each transition |
| Recovery Workbench Logical Data Model and Data Dictionary v8 | Data | Source of the `write_off` fields DF-FIN-010 to DF-FIN-020 and of the read-only `v_ace_write_off` view |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, only rwb-source-data reads ACE, Kafka, Temporal, no data lake, strict mode at the point of no return |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: WriteOffWorkflow on `rwb-writeoff`, the monthly Schedule on the 3rd working day, the write-off route set of 51 rules, the Saga runner for the posting |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every operation, event, workflow, table and job named here |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-writeoff (S7) is the recovery module's write-off. It turns "a population is assembled by hand each month, the committee decides on it, and the posting is reconciled afterwards" into a product: an eligibility scan that runs on both tracks by rule when the ACE batch is complete; a tax test with the criteria version it ran under; a pack built from the case, the provision carried and the recovery history without a person assembling it; a case taken out of the population with a reason, or held out because a deviation is open; a committee that approves, rejects or defers per account inside its delegation with the limit recorded; a posting that reaches ALS and the general ledger, releases the provision and sends the inputs Finance needs; a reconciliation of what was approved against what posted, with every difference raised; an exception loop with one named owner and a time limit; a placement with an agency or a sale of the charged-off book; a recovery recorded as post charge-off income with the agency fee; and a case that closes only after its retention period, with the closing entry and the rule, the reason and the approver behind it.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-writeoff | One deployable with its own API and worker, schema `rwb_writeoff`, login, topic `rwb.writeoff.events.v1`, task queue `rwb-writeoff` and lifecycle | The write-off becomes one owned product with its own release, instead of a monthly spreadsheet and a committee pack assembled by hand |
| The scan as a Schedule | JOB-16 is a Temporal Schedule in this service on the 3rd working day, started against the ACE ALS batch | The population is proposed on a date the business can see, and a late batch holds the scan instead of starting a load |
| The pack as a product behaviour | The pack is assembled from the case facts, the provision carried, the route history, the legal and asset state and the residual, by the write-off agent with a template fallback | The committee decides on a pack, and a pack built by hand arrives late |
| The committee decision as one record | Per account: approve, reject or defer, the limit applied, the approver, the reason and the rule version | The decision, the limit and the reason are the audit trail of a write-off |
| The posting as a saga step | The posting is a step on rwb-payment's queue that waits for the central ledger to confirm the decision record | A write-off is the point of no return, so it is the one step that does not proceed on an unconfirmed record |
| Approved against posted as one published control | The reconciliation of the approved and the posted population, with every difference raised | A write-off approved but not posted leaves an overstated book, and the difference is the control that catches a wrong population |
| The closure as a workflow outcome | Retention runs as a durable timer, closure needs a retention class on every document, and a reopening needs a written rule, a reason and an approver | Closure without a control is how a written-off case returns to the list |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its ingestion of the GL write-off posting and its backups | REUSE | ACE team |
| The read-only view contract, the GL outcome and the freshness of each data product | REUSE, elsewhere | P1 rwb-source-data (this service reads it by contract) |
| Case record, CMMN state, queues, tasks, allocation and the case timers | REUSE | P3 rwb-case (WriteOffWorkflow is its child workflow) |
| Approval workflow, decision record, hash chain, central ledger, rule package registry and DoA limits | REUSE | P7 rwb-decision (with P4 for the delegation table) |
| Payment and proceeds matching, posting to ALS and the general ledger, fees and posting files | REUSE, elsewhere | P8 rwb-payment (GAP-1793; ASM-2969) |
| Document hub, the pack document, retention class and the retention job JOB-17 | REUSE, elsewhere | P5 rwb-document (GAP-1797; ASM-2973) |
| Panel, agency instruction, result, fee and scorecard | REUSE, elsewhere | S9 rwb-partner (GAP-1798; ASM-2974) |
| Debt sale lot, data room, award and transfer of a charged-off population | REUSE, elsewhere | S6 rwb-debtsale (GAP-1799; ASM-2975) |
| Interface configuration, the Finance file window and the GL write-off event | REUSE, elsewhere | P2 rwb-integration (GAP-1796; ASM-2972) |
| Roles, capability areas, masking policy and the delegation table | REUSE | P4 rwb-access |
| Agent runtime, prompt register, guardrails and the run record | REUSE | P10 rwb-agent (GAP-1811; ASM-2987) |
| Write-off measures, completeness and the steering measures | REUSE, elsewhere | P9 rwb-reporting (GAP-1813; ASM-2989) |
| Screens and the composite route that serves them | REUSE | Platform edge, gateway-bff (RWB-PLT-EDGE) |
| Quartz and its shared tables, including the scheduler JOB-16 ran on | REPLACED | Temporal Schedules through the workflow kit (PLT); ADR-016, DP-10 |
| The Power BI copy of the write-off population | REMOVED | No data lake; completeness is published from rwb-reporting (ADR-018; GAP-1813; ASM-2989) |
| Booking in ALS and GL and their own posting logic | OUT OF SCOPE | ALS and the general ledger; this service records the reference it is given |
| Collections before day 90 and decisions D1 to D4 | OUT OF SCOPE | EFS and the ACE collection module |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014; slides 37 and 45).
2. The service writes only schema `rwb_writeoff`; no cross-schema join and no foreign key into `public` (ADR-014, DP-01).
3. A route service reaches a shared capability through Temporal, never REST; this service's REST reads are to rwb-source-data for the GL outcome (slide 20; slide 13; ADR-020).
4. REST is one hop from gateway-bff with a 2 s timeout, an Idempotency-Key on every POST and RFC 9457 problem details; a GET is retried once with jitter (ADR-020; slide 10; slide 11).
5. Events are CloudEvents 1.0 on Kafka with an outbox and an inbox, retry at 1 minute, 10 minutes and 1 hour and then a dead-letter topic; topic `rwb.writeoff.events.v1`, key `caseId` (ADR-015, DP-09, DP-14; slides 9 and 11).
6. Temporal namespace `rwb-recovery`, task queue `rwb-writeoff`; WriteOffWorkflow is a child of the case workflow; Schedules and durable timers replace Quartz (ADR-016, DP-10).
7. Rules are versioned data evaluated in process by the embedded Drools kit; the write-off route set is governed in rwb-decision (ADR-017, DP-04; GAP-1802; ASM-2978).
8. There is no data lake: completeness and the write-off measures are read from the decision record and the events into rwb-reporting (ADR-018, DP-17).
9. A write-off is a point of no return: the posting waits until rwb-decision confirms the decision record in the central ledger (slide 28, strict mode; session 6.3 of this document; GAP-1807; ASM-2983).
10. Personal data stays out of events, workflow inputs and logs; masking is by role, using the permission data cached from rwb-access, and each service authorises the object itself (slide 10; NFR-039, NFR-040).
11. The bank scheduler owns only the cross-system edges and signals the business date; it never enters the case journey or the monthly scan (slide 32; slide 44).
12. A service is created in its wave: this one in wave 4, the same wave as the business epic it serves, so no capability of E6 sits in a later wave than E6 (section 7.3 of the epic BRD; section 10 of the program BRD).

# 3. Personas and roles

Roles only; no person is named anywhere in this document. The capability area is `WRITE_OFF_AND_POSTING` (LOV-CAPABILITY) with the case stage `WRITE_OFF` (LOV-STAGE) and the treatment `WRITE_OFF` (LOV-TREATMENT).

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-S7-01 | Write-off team member | The monthly population with its reasons, a pack per case, and a removal with a reason that sticks | JRN-S7-01, JRN-S7-02 |
| ROL-S7-02 | Write-off committee member | A pack per account, the limit that applies, and the decision with its reason | JRN-S7-02, JRN-S7-03 |
| ROL-S7-03 | Credit approval committee member (product head with Risk) | The pack above the write-off committee limit, with the value, the provision and the recovery position | JRN-S7-03 |
| ROL-S7-04 | Credit Administration officer | A posting that reaches ALS and the general ledger, a rejection that comes back with its cause, and a re-post inside the retry limit | JRN-S7-04, JRN-S7-05 |
| ROL-S7-05 | Finance and CFO delegate | The provision released, the provision inputs and the tax file, on the month-end close | JRN-S7-04 |
| ROL-S7-06 | Partner and agency manager | A placement decided on measured return, a result on the case the same day, and a recall when the agency underperforms | JRN-S7-05 |
| ROL-S7-07 | Debt sale officer | A charged-off population handed to the sale route with the approval its limit requires | JRN-S7-05 |
| ROL-S7-08 | Head of Asset Liquidity | The post charge-off population and its terms, inside the approved population | JRN-S7-05 |
| ROL-S7-09 | Case owner | A rejection that returns the case to recovery, and a deferred case back at its review date | JRN-S7-03 |
| ROL-S7-10 | Center of excellence analyst | The eligibility and tax criteria as a versioned load, with the version each scan ran under | JRN-S7-01, JRN-S7-06 |
| ROL-S7-11 | Compliance and PDPA officer | Masking by role, an access log that cannot be skipped, a classification on every record, and the retention class behind every closure | JRN-S7-06 |
| ROL-S7-12 | Internal audit | A write-off reproducible from the log: the population rule, the pack, the decision, the limit, the approver and the posting reference | JRN-S7-06 |
| ROL-S7-13 | Risk and model risk officer | The approved-against-posted reconciliation, the singleton exceptions, and the pack agent's acceptance and override | JRN-S7-06 |
| ROL-S7-14 | Platform administrator | A Schedule that reports a missed run, an alert with a named owner, and a replay path | JRN-S7-04 |
| ROL-S7-15 | Developer | A typed contract to build against, a fake for every dependency, and a build that fails on a direct ACE read | JRN-S7-06 |
| ROL-S7-16 | Outsourced agency (external role) | An instruction with the accounts, the placement terms and the end date | JRN-S7-05 |

Non-human actors: the case workflow on rwb-case that starts WriteOffWorkflow; the monthly Schedule that starts the scan; the approval workflow on rwb-decision; the write-off agent on rwb-agent; the outbox relay; the consumers of WriteOffApproved. The agency and the buyer are reached through the partner portal at the edge and never by a direct call from this service.

# 4. User journeys

## 4.1 Current state (as built and as run today)

1. The write-off population is assembled by hand each month from local lists and spreadsheets, so the population cannot be reconciled to the book.
2. Eligibility and the tax criteria are applied by hand, and the version of the criteria a case was tested against cannot be shown afterwards.
3. The committee pack is built by collecting documents and balances from several systems; a pack that arrives late is decided late.
4. The committee decision is recorded in the minutes and re-keyed into the posting request.
5. The posting to ALS and the general ledger is re-keyed, and a rejected posting is chased by mail.
6. The write-off exception loop has no named owner and no time limit, so its cases do not close.
7. The approved population and the posted population are compared by hand, at the month end, after the book is closed.

Consequence: the population, the provision and the posting cannot be defended to audit, and a case can sit for months between an approval and a posting.

## 4.2 Target state (this product)

### JRN-S7-01 The monthly scan (monthly, 3rd working day; write-off team member and center of excellence)

1. The Schedule fires on the 3rd working day, and the scan checks that the cut-off date is reached and that the ACE batch for the ALS source is COMPLETED in the batch status the source-data contract returns.
2. The service reads the version of the eligibility and tax rules in force, and holds the scan where the tax criteria version is not published, with MSG-S7-001.
3. Every open case is tested against the eligibility rule on both tracks and against the tax criteria, and the population is proposed with the rule version it was tested under.
4. Each proposed account carries the tax result and the criteria version behind it.
5. The write-off team reads the population with its counts and its reasons; a product that is stale is shown with its date rather than assumed current.

### JRN-S7-02 Pack, removal and committee routing (within 3 working days of the scan; write-off team member and committee member)

1. The pack is prepared for each proposed case from the balance, the provision carried, the route history, the legal and asset state and the residual; the write-off agent drafts it and the template pack is used where the agent does not answer inside its target.
2. A pack without the provision carried or without its document is held with a data quality task, and routed once both are present.
3. A case is removed from the population with a reason, or held out because a deviation is open and routed to the deviation handler; it returns at the next cut-off once the cause is cleared.
4. A pack inside the write-off committee limit is routed to the committee queue and booked into the monthly meeting; a pack above the limit is escalated to the credit approval committee chaired by the product head with Risk.

### JRN-S7-03 The committee decision (monthly meeting; committee member, credit committee and case owner)

1. The committee member opens the pack and approves, rejects or defers per account.
2. An approval inside the delegation records the final call, the approver, the limit applied and the rule version, and releases the case to posting.
3. A rejection records its reason and returns the case to the pursue track.
4. A deferral records a review date, sets the review timer and holds the case until the next scan.
5. A rejection without a reason and a deferral without a review date are refused and returned to the committee; an action by a role without the capability area is refused with MSG-P4-002 and changes nothing.

### JRN-S7-04 Posting, provision and reconciliation (month-end close window; Credit Administration officer, Finance and the platform administrator)

1. A posting task is created when the posting window is open and no unmatched payment is in flight; the posting is executed on rwb-payment's queue and waits for the central ledger to confirm the decision record.
2. ALS and the general ledger return a reference and the reference is recorded; a rejection holds the posting with its cause.
3. A rejected posting is re-posted while the retry count is below the limit and the cause is cleared; at the limit the case goes to the write-off exception with the correction the owner decides.
4. The provision carried is released and the released amount recorded; the provision inputs and the tax file reach Finance and a rejected file is retried and then raised as a task.
5. The approved and the posted populations are reconciled, completeness is published, and every difference is raised.

### JRN-S7-05 Post charge-off recovery, placement and closure (daily, then per term; Credit Administration, partner and agency manager, debt sale officer)

1. The post charge-off treatment is decided by rule; an account is placed with the agency chosen on measured return, and the instruction leaves through the partner portal the same day.
2. Where no agency on the panel has capacity the placement is held and escalated on its timer; a placement that underperforms is recalled with a reason and replaced from the scorecard.
3. A customer payment after charge-off is matched to the case and the placement, posted as post charge-off income and the agency fee calculated; an unmatched payment goes to the exception list and is matched when the case is identified.
4. A payment that belongs to a sold account is remitted to the buyer under the remittance rule.
5. A charged-off population is handed to the debt sale route where the placement type is sale, and the sale closes the case when the buyer settles and the data transfer completes.
6. A placement that expires with nothing recovered closes the placement and starts the retention timer.

### JRN-S7-06 Evidence and measures read later (audit, compliance, center of excellence and risk)

1. An auditor reads one write-off: the population rule and its version, the tax result, the pack, the committee decision with the limit and the approver, the posting reference, the provision released and the closure entry.
2. Compliance reads the masking matrix, the access log of every personal read, the classification of every record and the retention class behind every closure.
3. The center of excellence reads the criteria versions in force by valid-from date, and every scan and decision taken under each.
4. Risk reads the approved-against-posted reconciliation, the exceptions raised and their age, and the pack agent's acceptance and override.
5. A developer builds against the published contract and its fake; a build that reads an ACE view or an ACE table directly fails.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-S7-001 | The monthly eligibility scan on both tracks | The population is proposed by rule on the 3rd working day, with the rule version behind it, instead of being assembled by hand | BR-051 | Must | 4 | FEAT-WOF-01 (A2.1) |
| CAP-S7-002 | The tax criteria test | Every proposed account carries its tax result and the criteria version it was tested under | BR-051 | Must | 4 | FEAT-WOF-02 (A2.2) |
| CAP-S7-003 | The committee pack | The pack exists per case from the case facts, the provision and the recovery history before anyone asks for it | BR-052 | Must | 4 | FEAT-WOF-03 (A2.3) |
| CAP-S7-004 | Removal from the population | A case leaves the population with a reason, or because a deviation is open, and comes back when the cause is cleared | BR-052 | Must | 4 | FEAT-WOF-04 (A2.4) |
| CAP-S7-005 | Committee routing and the meeting | The population reaches the committee queue and the monthly meeting, and a pack above the limit reaches the credit approval committee | BR-052, BR-053 | Must | 4 | FEAT-WOF-05 (A2.5) |
| CAP-S7-006 | Approval inside the delegation | The committee approves per account inside its delegation, and the limit applied, the approver and the rule version are on the record | BR-053 | Must | 4 | FEAT-WOF-06 (A2.6) |
| CAP-S7-007 | Rejection | A rejection records its reason and returns the case to recovery instead of leaving it in the population | BR-053 | Must | 4 | FEAT-WOF-07 (A2.7) |
| CAP-S7-008 | Deferral with a review date | A case the committee is not ready to decide is held on purpose, with a date it is looked at again | BR-053 | Must | 4 | FEAT-WOF-08 (A2.8) |
| CAP-S7-009 | Posting to ALS and the general ledger | An approved write-off posts through the posting service, records the reference it is given, and is re-posted or excepted when it is rejected | BR-054 | Must | 4 | FEAT-WOF-09 (A2.9) |
| CAP-S7-010 | Provision release and the Finance feed | The provision carried is released and the inputs Finance needs leave from the posted population | BR-054 | Must | 4 | FEAT-WOF-10 (A2.10) |
| CAP-S7-011 | Approved against posted | What the committee approved is compared to what posted, completeness is published, and every difference is raised | BR-055 | Must | 4 | FEAT-WOF-11 (A2.11) |
| CAP-S7-012 | The write-off exception loop | A case the rules cannot clear has one owner and a time limit, and a correction to pick | BR-056 | Must | 4 | FEAT-WOF-12 (A2.12) |
| CAP-S7-013 | Closure after retention | A case closes only after its retention period and with a retention class on every document, and a reopening needs a written rule | BR-057 | Must | 4 | FEAT-WOF-13 (A2.13) |
| CAP-S7-014 | Criteria as a versioned load | The eligibility and tax criteria change as a validated load from their valid-from date, with no code release | BR-058 | Should | 4 | FEAT-WOF-14 (A2.14) |
| CAP-S7-015 | Recovery after charge-off | A payment after charge-off is applied and recorded as income with the agency fee, and the account is placed by rule | BR-059 | Must | 4 | FEAT-WOF-15 (A2.15) |
| CAP-S7-016 | Sale of a charged-off population | A charged-off population is sold under the placement and sale rules, and the buyer remittance closes the item | BR-059 | Must | 4 | FEAT-WOF-16 (A2.16) |
| CAP-S7-017 | The data date and the read path | Every scan, decision and posting states which data it ran on and how old that data is, and a stale product is seen rather than assumed | BR-051, BR-054, BR-055 | Must | 4 | A2.1 to A2.16 (VR-S7-001-1 to VR-S7-016-1); A2.5 and A2.11 |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Direct read of the ACE GL write-off view and the batch status view | Not carried | rwb-source-data's contract (GAP-1792; ASM-2968) |
| Posting to ALS and the general ledger from this service | Not carried | P8 rwb-payment, with the outcome read back through P1 (GAP-1793; ASM-2969) |
| Holding the pack document | Not carried | P5 rwb-document (GAP-1797; ASM-2973) |
| Agency instruction, result and recall by direct call | Not carried | S9 rwb-partner through the partner portal (GAP-1798; ASM-2974) |
| The debt sale lot, data room and award | Reused, elsewhere | S6 rwb-debtsale (GAP-1799; ASM-2975) |
| The Finance file window and the GL write-off event as an interface | Not carried | P2 rwb-integration (GAP-1796; ASM-2972) |
| Quartz scheduling of the monthly scan | Replaced | A Temporal Schedule through the workflow kit (GAP-1801; ASM-2977) |
| The Power BI copy of the population and of completeness | Removed | rwb-reporting from the events and the decision record (ADR-018) |
| Booking logic in ALS and GL, and the accounting policy behind it | Out of scope | ALS and the general ledger |
| The eligibility and tax criteria themselves as policy values | Open | The write-off committee member with Finance (Q-006) |

# 6. Functional requirements

Every requirement is specific and testable. The FSD requirement column keeps the trace to the source requirement of the module, and the rule column names the routing rule of Business Rules and Routing Logic v4 that carries the transition. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Rule | Priority | Wave |
|---|---|---|---|---|---|---|---|
| FR-S7-001 | The service SHALL obtain every case, balance, provision, GL posting and batch-status fact it needs through the rwb-source-data contract. A read of a `recovery.v_ace_*` view, a read of an ACE table, and a constraint in schema `rwb_writeoff` that references a table outside it, SHALL fail the build and the boundary test. | CAP-S7-017 | BR-051 | REQ-S7-001 | — | Must | 4 |
| FR-S7-002 | The service SHALL record on every scan, every committee decision and every posting the business date and load time of each data product it read, SHALL show a stale product with the date it belongs to and MSG-P1-001, and SHALL start no posting on a data product whose freshness cannot be read. | CAP-S7-017 | BR-054 | REQ-S7-005 | VR-S7-005-1, VR-S7-011-1, VR-S7-015-1 | Must | 4 |
| FR-S7-003 | The service SHALL run the eligibility scan from a Temporal Schedule on the 3rd working day of the month, SHALL start it against the ALS batch recorded as COMPLETED in the batch status the contract returns, and SHALL run no Quartz table, connection or job. | CAP-S7-001 | BR-051 | REQ-S7-001 | R-WO-01 | Must | 4 |
| FR-S7-004 | The service SHALL test every open case against the eligibility rule on both tracks and against the tax criteria when the cut-off date is reached and the ALS batch is complete, SHALL propose the population it selects, and SHALL record the rule and criteria version each case was tested under. | CAP-S7-001 | BR-051 | REQ-S7-001 | R-WO-01 | Must | 4 |
| FR-S7-005 | The service SHALL hold the scan and show MSG-S7-001 where the tax criteria version is not published, SHALL hold the scan and raise an incident where the ALS extract is absent for the cut-off date, and SHALL restart the scan for that cut-off date once the cause is cleared. | CAP-S7-002 | BR-051 | REQ-S7-001 | R-WO-02, R-WO-03, R-WO-04 | Must | 4 |
| FR-S7-006 | The service SHALL record the tax criteria result per proposed account, with the criteria version behind it, and SHALL make that result readable with the account, the scan run and the case. | CAP-S7-002 | BR-051 | REQ-S7-001 | R-WO-01 | Must | 4 |
| FR-S7-007 | The service SHALL read every eligibility threshold, tax criterion, committee limit, retry limit, cost and responsibility centre mapping and service level from versioned reference data or a governed rule package, and a change SHALL take effect from its valid-from date without a code release. | CAP-S7-014 | BR-058 | REQ-S7-001 | BR-S7-001 to BR-S7-016 | Should | 4 |
| FR-S7-008 | The service SHALL return a scan with its run reference, its cut-off date, its rule version, the population it proposed and the counts per state, so that a person can read what the scan did without recomputing it. | CAP-S7-001 | BR-051 | REQ-S7-001 | AC-BG-S7-001-01 | Must | 4 |
| FR-S7-009 | The service SHALL prepare the committee pack per proposed case from the balance, the provision carried, the route history, the legal and asset state and the residual, SHALL obtain the draft through the rwb-agent contract, SHALL wait at most 60 seconds for it, and SHALL use the template pack where the answer is late or fails its schema check. | CAP-S7-003 | BR-052 | REQ-S7-002 | R-WO-05 | Must | 4 |
| FR-S7-010 | The service SHALL hold a pack whose provision carried or pack document is absent, SHALL raise a data quality task with a named owner role, and SHALL route the pack to the committee once both are present. | CAP-S7-003 | BR-052 | REQ-S7-002 | R-WO-09, R-WO-10 | Must | 4 |
| FR-S7-011 | The service SHALL remove a case from the proposed population only with a `removal_reason` recorded, SHALL keep the removal visible with its reason, and SHALL show the case out of the population from that point. | CAP-S7-004 | BR-052 | REQ-S7-002 | R-WO-07 | Must | 4 |
| FR-S7-012 | The service SHALL hold a case out of the population where a deviation X1 to X7 is open, SHALL route it to the deviation handler, and SHALL record which deviation held it. | CAP-S7-004 | BR-052 | REQ-S7-002 | R-WO-06 | Must | 4 |
| FR-S7-013 | The service SHALL return a removed case to the next monthly scan once the deviation is cleared or the reason is resolved, and SHALL keep the earlier removal and its reason readable. | CAP-S7-004 | BR-052 | REQ-S7-002 | R-WO-08 | Must | 4 |
| FR-S7-014 | The service SHALL route a pack whose amount is inside the write-off committee limit to the committee queue and book it into the monthly meeting before the meeting date. | CAP-S7-005 | BR-052 | REQ-S7-002 | R-WO-11 | Must | 4 |
| FR-S7-015 | The service SHALL escalate a pack whose amount is above the write-off committee limit to the credit approval committee chaired by the product head with Risk, with the pack and its evidence, before the scheduled meeting. | CAP-S7-005 | BR-053 | REQ-S7-003 | R-WO-12 | Must | 4 |
| FR-S7-016 | The service SHALL record a committee approval per account with the final call, the approver role, the limit applied and the rule version, and SHALL release the case to posting in the same step. | CAP-S7-006 | BR-053 | REQ-S7-003 | R-WO-13, R-WO-15 | Must | 4 |
| FR-S7-017 | The service SHALL record a rejection with its `decision_reason` and SHALL return the case to the pursue track with the case owner as the next actor. | CAP-S7-007 | BR-053 | REQ-S7-003 | R-WO-14, R-WO-16 | Must | 4 |
| FR-S7-018 | The service SHALL record a deferral with a `review_date`, SHALL set the review timer, SHALL hold the case until that date, and SHALL return the case to the next monthly scan when the review date is reached. | CAP-S7-008 | BR-053 | REQ-S7-003 | R-WO-17, R-WO-19 | Must | 4 |
| FR-S7-019 | The service SHALL refuse a rejection without a reason and a deferral without a review date, SHALL return the decision to the committee unchanged, and SHALL record the refusal. | CAP-S7-006 | BR-053 | REQ-S7-003 | R-WO-18 | Must | 4 |
| FR-S7-020 | The service SHALL take the approval through the approval workflow on rwb-decision with the delegation limit that applies to the decision, the product and the amount read at run time, and SHALL record the level applied and the approver role on the decision. | CAP-S7-006 | BR-053 | REQ-S7-003 | — | Must | 4 |
| FR-S7-021 | The service SHALL refuse every action of this capability to a role without the capability area `WRITE_OFF_AND_POSTING` with MSG-P4-002, and SHALL change nothing on a refusal. | CAP-S7-006 | BR-053 | REQ-S7-003 | VR-S7-012-2 | Must | 4 |
| FR-S7-022 | The service SHALL write its decision record in the same transaction as the state change and SHALL publish DecisionRecorded; where the record cannot be written it SHALL change nothing, show MSG-P7-003 and raise an incident. | CAP-S7-006 | BR-053 | REQ-S7-003 | — | Must | 4 |
| FR-S7-023 | The service SHALL create the posting task when the posting window is open and no unmatched payment is in flight, and SHALL obtain the posting to ALS and the general ledger as a step on rwb-payment's queue; it SHALL write no posting entry itself and SHALL call ALS or the general ledger directly on no path. | CAP-S7-009 | BR-054 | REQ-S7-005 | R-WO-20 | Must | 4 |
| FR-S7-024 | The service SHALL record the posting reference it is given on confirmation, SHALL hold the posting where the result is rejected and show the rejection with its cause. | CAP-S7-009 | BR-054 | REQ-S7-005 | R-WO-21, R-WO-22 | Must | 4 |
| FR-S7-025 | The service SHALL re-post while the retry count is below the retry limit and the cause is cleared, and at or above the limit SHALL raise the write-off exception for correction instead of retrying again. | CAP-S7-009 | BR-054 | REQ-S7-005 | R-WO-23, R-WO-24 | Must | 4 |
| FR-S7-026 | The service SHALL release the provision carried on a posted write-off and record the amount released against the case and the posting reference. | CAP-S7-010 | BR-054 | REQ-S7-005 | R-WO-25 | Must | 4 |
| FR-S7-027 | The service SHALL produce the provision inputs and the tax file from the posted population, SHALL deliver them through the rwb-integration contract on the month-end close, SHALL retry a rejected file, and SHALL raise a task with a named owner role after the retry limit. | CAP-S7-010 | BR-054 | REQ-S7-005 | R-WO-26, R-WO-27, R-WO-28 | Must | 4 |
| FR-S7-028 | The service SHALL reconcile the approved population to the posted population by count and by amount, SHALL publish completeness, and SHALL raise a write-off exception for every difference with the case, the count and the amount that differ. | CAP-S7-011 | BR-055 | REQ-S7-005 | R-WO-42, R-WO-43 | Must | 4 |
| FR-S7-029 | The service SHALL hold the posting until rwb-decision confirms the decision record in the central ledger, and SHALL proceed only on that acknowledgement; where the ledger is late the posting waits and an alert is raised rather than the posting being taken on an unconfirmed record. | CAP-S7-009 | BR-054 | REQ-S7-005 | — | Must | 4 |
| FR-S7-030 | The service SHALL open the write-off exception with one named owner role and a time limit, SHALL record the cause and the case, and SHALL show the exception with its age against that limit. | CAP-S7-012 | BR-056 | REQ-S7-004 | R-WO-24 | Must | 4 |
| FR-S7-031 | The service SHALL offer the exception owner the three corrections — re-post to ALS and the general ledger, return the case to the next monthly scan, refer the pack back to the committee — and SHALL record the correction chosen, its reason and the actor. | CAP-S7-012 | BR-056 | REQ-S7-004 | R-WO-44, R-WO-45, R-WO-46 | Must | 4 |
| FR-S7-032 | The service SHALL raise the write-off exception where a post charge-off payment reopens a question on an approved write-off, and SHALL refer that case to the committee. | CAP-S7-012 | BR-056 | REQ-S7-004 | R-WO-41 | Must | 4 |
| FR-S7-033 | The service SHALL decide the post charge-off treatment by rule, SHALL place the account with the agency chosen on measured return where the treatment is soft recovery and an agency on the panel has capacity, and SHALL record the agency, the terms and the end date. | CAP-S7-015 | BR-059 | REQ-S7-006 | R-WO-29, R-WO-30 | Must | 4 |
| FR-S7-034 | The service SHALL hold the placement and escalate on its timer where no agency on the panel has capacity, SHALL recall a placement whose measured return is below the panel threshold or whose conduct breaches are above zero, SHALL record the recall reason, and SHALL place the account with the next agency on the scorecard. | CAP-S7-015 | BR-059 | REQ-S7-006 | R-WO-31, R-WO-34, R-WO-35 | Must | 4 |
| FR-S7-035 | The service SHALL hand a charged-off population to the debt sale route where the placement type is sale, SHALL record the population handed over and the route it went to, and SHALL record the closure of the case when the buyer settles and the data transfer completes, with the case state itself moved by rwb-case as its owner. | CAP-S7-016 | BR-059 | REQ-S7-006 | R-WO-32, R-WO-50 | Must | 4 |
| FR-S7-036 | The service SHALL match a payment received after charge-off to the case and the placement, SHALL post it as post charge-off income, SHALL calculate the agency fee from the contracted schedule, and SHALL do the same for a payment that matches a closed case with no placement. | CAP-S7-015 | BR-059 | REQ-S7-007 | R-WO-37, R-WO-49 | Must | 4 |
| FR-S7-037 | The service SHALL send a payment that matches no case and no placement to the exception list, SHALL show it with its value date, and SHALL match and post it once the case or the placement is identified. | CAP-S7-015 | BR-059 | REQ-S7-007 | R-WO-38, R-WO-39 | Must | 4 |
| FR-S7-038 | The service SHALL remit a payment that belongs to an account sold before the payment arrived to the buyer under the remittance rule, SHALL record the remittance against the sold account, and SHALL close the item when the buyer confirms receipt. | CAP-S7-016 | BR-059 | REQ-S7-006 | R-WO-40, R-WO-51 | Must | 4 |
| FR-S7-039 | The service SHALL start the retention timer when a placement closes with nothing recovered, SHALL close the case only where no placement, no sale and no exception is open and a retention class is present on every document, and SHALL hold the closure with a document task where a retention class is missing. | CAP-S7-013 | BR-057 | REQ-S7-008 | R-WO-36, R-WO-47, R-WO-48 | Must | 4 |
| FR-S7-040 | The service SHALL write the closing entry with the cash recovered and the loss, SHALL stop every timer of the stage, and SHALL report the closure to rwb-case, which owns the case state and moves the case to closed; the event by which the closure reaches it is open (GAP-1800; ASM-2976). | CAP-S7-013 | BR-057 | REQ-S7-008 | R-WO-47 | Must | 4 |
| FR-S7-041 | The service SHALL allow a closed write-off to be reopened only through a written rule, a reason and an approver, and SHALL record all three with the reopening. | CAP-S7-013 | BR-057 | REQ-S7-008 | — | Must | 4 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-S7-001 | The write-off proposal screen and the committee pack view respond inside the user's wait under the busiest-hour load, including the reads where case, pack and provision data are joined. | Under 2 seconds at the 95th percentile | NFR-008, NFR-009 | Must | Performance test in system test |
| NFR-S7-002 | A case's write-off history reads inside the user's wait with the decision log at its stated size. | Under 2 seconds; about 36 GB for the decision log and the interaction ledger by the end of 2031 | NFR-007 | Must | Volume read test |
| NFR-S7-003 | An eligibility or tax rule evaluation inside the scan completes inside the user's wait. | Under 300 milliseconds per rule evaluation at the 95th percentile | NFR-011 | Must | Rule timing test with the package in force |
| NFR-S7-004 | The pack agent answers inside its target; after that the template pack is used and the pack is still routed. | Under 60 seconds, then the template pack | NFR-010, NFR-024 | Must | Agent timeout drill |
| NFR-S7-005 | The service carries the stated volume of cases and staff. | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts at 90 days past due a month; about 370 staff online in the busiest hour of 914 named users | NFR-001, NFR-002 | Must | Volume test at the stated volume |
| NFR-S7-006 | The monthly scan of the 3rd working day completes inside the window the pack has, so that no pack misses the meeting. | Inside the 3 working days the pack has to be prepared | NFR-002, R-WO-05 | Must | Scan timing test at the stated volume |
| NFR-S7-007 | Every scan, committee decision, posting and closure states the business date and load time of the data products it read. | Every record | NFR-013 | Must | Record inspection |
| NFR-S7-008 | A missing, failed or late ACE batch is visible at the scan, the committee pack and the posting, and alerts the data steward. | Visible at each point; alert to the steward | NFR-014 | Must | Hold an ACE batch in system test |
| NFR-S7-009 | The service holds no load window, no staging table and no catch-up job: a late ACE batch holds the scan or the posting and raises an alert. | No load, no staging, no catch-up | NFR-015 | Must | Hold and release the batch |
| NFR-S7-010 | The service is available during business hours and in the month-end close window, when the posting runs. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-S7-011 | The service inherits the ACE recovery point and recovery time, and a running write-off workflow resumes where it stopped. | The ACE recovery point objective and recovery time objective; workflow history preserved | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-S7-012 | A call is one hop with a 2 s timeout; a failure is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; events that cannot be processed go to the dead-letter topic and are replayed. | One hop; 2 s timeout; three retries then the exception queue; dead-letter with replay | NFR-025, NFR-026 | Must | Failure injection |
| NFR-S7-013 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in schema `rwb_writeoff`. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-S7-014 | A case closes after its retention period and a reopening needs a written rule, a reason and an approver. | Retention period by record class; the periods are open under DL26 | NFR-031 | Must | Closure and reopen drill |
| NFR-S7-015 | Every document on a write-off case carries a retention class, and the class sets how long it is kept. | A class on every document; periods open | NFR-028 | Must | Retention class review |
| NFR-S7-016 | A legal hold stops the closure and the disposal of the case or document it covers, for as long as it is in place. | Hold overrides retention | NFR-072 | Must | Legal hold drill |
| NFR-S7-017 | A record or document reaching the end of its retention period is disposed of or extended by a recorded decision, and is never removed silently. | Recorded decision on every disposal | NFR-074 | Must | Disposal audit |
| NFR-S7-018 | The decision log is retained for the period the regulator and internal audit require. | Set by Compliance; open under DL26 | NFR-030 | Must | Retention configuration review |
| NFR-S7-019 | Every write-off is reproducible from the log, including the rule and criteria versions, the pack, the decision, the limit, the approver and the posting reference. | Every write-off reproducible | NFR-033 | Must | Re-run a sample of write-offs from the log |
| NFR-S7-020 | Every action carries the rule version applied and the approver role who allowed it. | Every action | NFR-034 | Must | Decision record inspection |
| NFR-S7-021 | The decision log hash chain is checked daily and a break is reported to Compliance the same day. | Daily check, same-day report | NFR-035 | Must | Chain break drill |
| NFR-S7-022 | Write-off returns reach first-time-right on the quality assurance sample. | 90 percent | NFR-037, KPI-009 | Must | QA sample of closed write-offs, tested against the rule version applied |
| NFR-S7-023 | Party identifiers are masked at rest and on every screen and agent call, by role. | Masked at rest and in use | NFR-039 | Must | Masking matrix test across roles |
| NFR-S7-024 | Each screen and each agent receives only the personal data it needs, and no personal data is put in an event, a workflow input or a log. | Data minimisation per screen and per agent | NFR-040 | Must | Contract review per screen and per agent; event inspection |
| NFR-S7-025 | Every read of a personal field is logged, and the read is refused rather than returned where the log cannot be written. | Every read | NFR-042 | Must | Access log reconciliation against reads |
| NFR-S7-026 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | NFR-045 | Must | Environment data review |
| NFR-S7-027 | Every data product and record this service holds carries a data classification that sets its handling. | Classification applied per record | NFR-047 | Must | Classification review |
| NFR-S7-028 | Recovery data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | NFR-046 | Must | Tenancy review |
| NFR-S7-029 | Staff authenticate with single sign-on and multi-factor authentication, and agents run under service identities subject to the same role checks. | Entra ID single sign-on with multi-factor; service identities | NFR-049, NFR-051 | Must | Sign-in and identity test |
| NFR-S7-030 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-S7-031 | The build blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency, and every agent output is schema checked with the template fallback. | Pipeline checks pass; schema check on every agent output | NFR-054, NFR-055 | Must | Pipeline run with a seeded violation; agent output with a bad schema |
| NFR-S7-032 | Penetration testing and a security review are completed before the first production release. | Before the first production release | NFR-056 | Must | Security sign-off |
| NFR-S7-033 | Screen labels, validation messages and error messages served with this service's operations are available in Thai and in English. | Every label and message in Thai and English | NFR-059 | Must | Label and message review |
| NFR-S7-034 | The write-off screens meet the bank's accessibility standard and work on the browsers the bank supports. | WCAG 2.1 level AA; the current and previous major versions of Microsoft Edge and Google Chrome | NFR-060, NFR-061 | Must | Accessibility scan and browser test |
| NFR-S7-035 | Logs, traces and metrics are produced for the scan, the committee decision and the posting, every scheduled or triggered job has a run book, and a failure alerts a named owner. | Every job covered; alert within 15 minutes to the named owner | NFR-064, NFR-065, NFR-067, NFR-068 | Must | Observability review and alert drill |
| NFR-S7-036 | A write by the pack agent is logged with the model and prompt version, on the same terms as a decision taken by a person. | Every agent write | NFR-078 | Must | Agent write inspection |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_writeoff`. Every table carries the record columns of the platform library. The Ownership Map holds one table for this service, `write_off`, whose eleven fields are the Logical Data Model's DF-FIN-010 to DF-FIN-020; Architecture v5 gives the schema four entity groups and names no table for the other three, so those groups are described as entities and their physical names are written with the DB story (GAP-1794; ASM-2970). Retention is stated by class; the periods are open (GAP-1808; ASM-2984).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `write_off` | Owned record, one per write-off of a case balance; the only table the Ownership Map gives this service | `id`; `case_id`; `decision_log_id`; `amount` numeric(18,2); `tax_criteria_met`; `committee_date`; `posted_date`; `responsibility_center` varchar(10); `cost_center` varchar(10); `gl_product` varchar(10); `recovered_after` numeric(18,2) | [SENSITIVE_FINANCIAL] | Workbench decision; the amount, the posting date and the GL codes are mirrored from the general ledger (DEF-05; GAP-1809) | Workbench record class; period open |
| `eligibility` (entity group) | Owned record, one per case per scan | Case number, scan run reference, cut-off date, business date, eligibility result per track, tax criteria result, criteria version, rule version, the state the case moved to | [SENSITIVE_FINANCIAL] | Workbench decision taken on the data the source-data contract returns | Workbench record class; period open |
| `committee` (entity group) | Owned record, one per committee decision per account | Case number, pack reference, the pack inputs (balance, provision carried, route history, legal and asset state, residual), the committee, the decision (approve, reject, defer), the limit applied, the approver role, the reason, the review date, the decided at, the rule version | [SENSITIVE_FINANCIAL] | Workbench decision | Workbench record class; period open |
| `posting` (entity group) | Owned record, one per posting attempt | Posting task reference, window, attempt count, ALS reference, general ledger reference, result, rejection cause, the ledger acknowledgement, the provision released and its amount, the Finance file reference and its status | [SENSITIVE_FINANCIAL] | P8 rwb-payment through the posting step, and P1 for the GL outcome | Workbench record class; period open |
| `recovery_after_chargeoff` (entity group) | Owned record, one per recovery, placement or sale | Case number, the payment and its value date, the placement and the agency, the agency fee, the income posted, the recall and its reason, the sale and its route, the remittance to the buyer, the retention start and the closing entry | [SENSITIVE_FINANCIAL] | Workbench decision and the payments the service consumes | Workbench record class; period open |
| `outbox_event`, `processed_event`, `idempotency_key` | Platform library objects created in this schema | Library-defined | [CONFIDENTIAL] | Service template | Library policy (PLT; ASM-0074) |

The FSD field catalog of A2.4, A2.6, A2.7, A2.8, A2.12, A2.14 and A2.16 lists eight fields of `write_off` and no field of the three other entity groups. Three of the eleven model fields are therefore not in the FSD catalog (`gl_product`, `recovered_after`, and `id` as the record identifier), and the removal reason, the review date and the pack reference the rules require are held in no listed field (GAP-1809, GAP-1810; ASM-2985, ASM-2986). No copy of an ACE column is held and no foreign key leaves the schema.

## 8.2 Data read but not owned

| Data | Read through | Views or source behind it | Classification of the data read |
|---|---|---|---|
| The GL write-off posting (amount, posting date, responsibility centre, cost centre, GL product, source system, data as of) | rwb-source-data contract (REST) | `v_ace_write_off` | [SENSITIVE_FINANCIAL] |
| Freshness of each data product, including the ALS source | rwb-source-data contract (REST) | `v_ace_batch_status` | [CONFIDENTIAL] |
| Balances, arrears and the account facts behind the balance and the provision | rwb-source-data contract (REST) | `v_ace_account`, `v_ace_payment` | [SENSITIVE_FINANCIAL] |
| Case, party, stage, queue and timers | rwb-case contract (Temporal activity and REST) | none (case schema) | [PII], [SENSITIVE_FINANCIAL] |
| Roles, capability areas, masking policy and the delegation table | rwb-access permission data, cached | none (access schema) | [CONFIDENTIAL] |
| Rule packages, the version in force and the DoA limits | rwb-decision contract and events; P4 for the limits | none (decision and access schemas) | [CONFIDENTIAL] |
| Reference data and the lists LOV-STAGE, LOV-TREATMENT, LOV-ROUTE-SET, LOV-CAPABILITY | rwb-case reference-data contract | none (case schema) | [CONFIDENTIAL] |
| The pack document and its retention class | rwb-document contract | none (document schema) | [CONFIDENTIAL] |
| The agency panel, the scorecard and the placement result | rwb-partner contract and events | none (partner schema) | [CONFIDENTIAL] |
| The payment and the proceeds matched to a case | rwb-payment events | none (payment schema) | [SENSITIVE_FINANCIAL] |

Counts are not stated: the FSD gives no field count for this module, and no count is recomputed here.

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| `write_off.amount` | The amount written off, in baht | [SENSITIVE_FINANCIAL] | Read by role; no amount in an event, a workflow input or a log |
| `write_off.recovered_after` | What has been recovered after charge-off to date | [SENSITIVE_FINANCIAL] | Served on the case and the proposal screen only; not carried in WriteOffApproved |
| `write_off.committee_date`, `posted_date` | When the committee decided and when the posting took effect | [CONFIDENTIAL] | Shown on the pack and the case; the posting date comes from the GL outcome |
| `write_off.responsibility_center`, `cost_center`, `gl_product` | The GL coding of the posting | [CONFIDENTIAL] | Mirrored from the general ledger; never re-keyed and never guessed |
| `write_off.tax_criteria_met` | Whether the account met the tax criteria | [CONFIDENTIAL] | Recorded with the criteria version; shown on the pack |
| Customer identification number and name, where the proposal or pack screen shows the case party | The party the case belongs to | [PII] | Masked by role; the identification number never leaves in clear; every read logged |
| Contact value, where the screen shows the last contact | How the customer was last reached | [PII] | Masked by default, full only where a masking row for the role allows it |
| The pack document and its extracted fields | The evidence the committee decides on | [CONFIDENTIAL] | Held in the document hub, read by role; the number never appears unmasked in a pack copy |
| The agency placement and the buyer tape | Who holds the account after charge-off | [CONFIDENTIAL] | The tape is masked before it leaves; the remittance carries the reference, not the amount |

The Logical Data Model marks all eleven `write_off` fields as not personal data. The party fields reach the screen through the case contract and are handled as personal data by this document.

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code: the eligibility thresholds on both tracks, the tax criteria, the committee limit, the retry limit, the panel threshold and the cost and responsibility centre mapping.
2. This service holds no copy of an ACE column and no staging table; it reads the GL outcome and the batch status through the source-data contract only (GAP-1792; ASM-2968).
3. A link to an ACE record is a business-key column of type `varchar(255)` with no foreign key, and the two foreign keys of `write_off` stay inside schema `rwb_writeoff` (Architecture v5 slide 29).
4. A personal field is not returned when the access log cannot be written.
5. Personal data is not put in an event, a workflow input or a log; WriteOffApproved carries the case, the write-off reference, the decision and the versions, not the amount.
6. The decision record and the state change are written in one transaction, and the ledger acknowledgement before the posting is what makes the write-off irreversible (strict mode; section 6 FR-S7-029).
7. ACE data is retained by ACE; the archive of a Workbench document belongs to rwb-document.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-source-data (P1) | Out and in | REST, one hop, 2 s timeout, GET retried once with jitter; listens to its events | P1 | The only path to the GL write-off outcome, the balance facts and the freshness of each product; this service reads no view and no ACE table (GAP-1792; ASM-2968) |
| ACE database, the 30 views behind them | Not read | None | ACE team | Read only through the P1 contract. No direct `public` read and no DML from this service |
| rwb-case (P3) | In and out | Temporal child workflow (WriteOffWorkflow) and REST; events listened to | P3 | The case starts the stage and owns the parent workflow, the case state, the queues, the tasks and the timer path; this service publishes WriteOffApproved on the approval and reports the closure to it (GAP-1800; ASM-2976) |
| rwb-decision (P7) | Out and in | Temporal child workflow (the committee approval) and activity; the central ledger; rule package events | P7 | The approval on the delegation, the decision record, the ledger acknowledgement before the posting, the rule package in force |
| rwb-payment (P8) | Out and in | Temporal activity (the posting step); listens to ProceedsMatched | P8 | The posting to ALS and the general ledger, and the payment and proceeds matching that becomes a post charge-off recovery (GAP-1793, GAP-1812; ASM-2969, ASM-2988) |
| rwb-document (P5) | Out | Contract for the pack document, its retention class and the retention job | P5 | The pack document is held there; the write-off holds the reference and the retention class (GAP-1797; ASM-2973) |
| rwb-partner (S9) | Out | Partner contract and the partner portal at the edge | S9 | The agency instruction, the result and the recall; same wave as this service (GAP-1798; ASM-2974) |
| rwb-integration (P2) | Out | File or interface per the integration contract | P2 | The provision inputs and the tax file to Finance; the connection matrix gives this service no P2 cell (GAP-1796; ASM-2972) |
| rwb-debtsale (S6) | Out | Contract; the sale route | S6 | The post charge-off population where the placement type is sale (GAP-1799; ASM-2975) |
| rwb-access (P4) | In | Cached permission data through the guard library, not a call on the hot path | P4 | Roles, the capability area `WRITE_OFF_AND_POSTING`, masking policy and the delegation table |
| rwb-agent (P10) | Out | Agent contract; Temporal activity | P10 | The write-off agent that drafts the pack, with the template fallback (GAP-1811; ASM-2987) |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | The write-off proposal screen (SCR-27), the pack view and the committee commands; the composite route joins this service's answer with rwb-case and rwb-document (GAP-1814; ASM-2990) |
| Kafka topic `rwb.writeoff.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by case | This service | WriteOffApproved (EV-24); consumers rwb-case, rwb-payment and rwb-reporting |
| Kafka topic `rwb.source-data.events.v1` | In | CloudEvents 1.0; inbox and dedupe | P1 | AceDataReady (EV-26) signals that the ALS source for the business date is complete |
| Kafka topic `rwb.payment.events.v1` | In | CloudEvents 1.0; inbox and dedupe | P8 | ProceedsMatched (EV-25) is the post charge-off recovery this service records |
| rwb-reporting (P9) | Out | Events and the decision record | P9 | Completeness, the approved-against-posted position and the write-off measures; produced from the log, not from a separate count |
| ACE common audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |
| ALS and the general ledger (external) | Not called | None | The core bank | Reached only through P8's posting step; this service records the outcome it is given |
| Finance provision feed (external) | Not called | None | Finance | Reached through P2's file window |
| Data lake and the Power BI copy (INT-19, INT-20) | Removed | None | None | Removed in v5 (ADR-018); no extract leaves this service |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Which service posts the write-off to ALS and the general ledger: does this service call the posting itself, as the FSD says, or does the posting run as a step on rwb-payment's queue, as Architecture v5 slide 20 shows, given that the connection matrix gives this service no cell to ALS, the general ledger or rwb-integration? | Solution architect with the P8 owner | Decides who owns the point of no return and where the rejection, the retry and the re-post are handled (GAP-1793; ASM-2969) |
| Which path carries the provision inputs and the tax file to Finance, given that P2 is the outbound-only interface service and the matrix shows no S7 cell to P2? | Solution architect with the integration lead | Decides whether the Finance feed is a P2 interface or an activity on another service's queue (GAP-1796; ASM-2972) |
| Who holds the pack document, and through which call: the document hub at P5, which the matrix does not connect to this service, or a reference held here? | Solution architect with the P5 owner | The pack document is what the committee decides on and the retention class sits on it (GAP-1797; ASM-2973) |
| How is an agency instruction issued and its result returned, when the partner portal is S9 and S9 is created in the same wave as this service? | Partner and agency manager with S9 | Placement, result and recall cannot be demonstrated before S9 exists (GAP-1798; ASM-2974) |
| How is a charged-off population handed to the debt sale route, given that S6 is created one wave earlier and neither service's matrix row shows the other? | Solution architect with the S6 owner | The sale of a charged-off population cannot be sequenced without the hand-over (GAP-1799; ASM-2975) |

# 10. Release slicing proposal

The service is wave 4 and serves EP06, whose release is 30 April 2027 (tentative). Wave 4 also carries EP07 at 31 May 2027 (tentative) and EP08 at 30 June 2027 (tentative); every capability of this product lands inside EP06, and no capability of it is held for the later releases of the same wave. Each slice is a list of capabilities, not stories. The service wave and the business epic wave are both 4, so no capability of E6 sits in a later wave than its epic (section 10.3 of the program BRD).

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox, inbox and decision-record libraries, the Temporal workflow kit with the approval child and the Saga runner, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Earlier waves — contracts this service consumes, not ones it publishes

| Slice | Capabilities | Why here |
|---|---|---|
| 0.1 Contracts consumed from wave 1 and wave 2 services | CAP-S7-001, CAP-S7-009, CAP-S7-015 | The read path (P1, wave 1), the approval and the ledger (P7, wave 1), the document hub (P5, wave 1) and the posting and payment matching (P8, wave 2) all exist before wave 4, so this service builds against published contracts and their fakes and waits for no service except S9 (GAP-1798) |

No contract of this service is needed before wave 4: no earlier business epic consumes a write-off capability, because the write-off hands its population to the debt sale route inside E6 (R-WO-32) and not before.

## 10.3 Wave 4 — EP06 (release 30 April 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 4.1 Scan, read path and data date | CAP-S7-001, CAP-S7-017 | Nothing else can be decided until the population exists with the data date it was tested on, and the boundary test must fail the build on a direct ACE read from the first story |
| 4.2 Tax criteria and the versioned load | CAP-S7-002, CAP-S7-014 | An ineligible write-off is a tax and audit exposure, so the tax result and the version behind it land with the scan |
| 4.3 Pack, removal and routing | CAP-S7-003, CAP-S7-004, CAP-S7-005 | The committee decides on a pack; a pack with no removal path and no meeting booking is a pack that arrives late or includes a case that should be held |
| 4.4 The committee decision | CAP-S7-006, CAP-S7-007, CAP-S7-008 | The decision, the limit and the reason are the audit trail; approve, reject and defer are one behaviour |
| 4.5 Posting, provision and reconciliation | CAP-S7-009, CAP-S7-010, CAP-S7-011 | An approved write-off that does not post leaves an overstated book, and the approved-against-posted control is what catches a wrong population |
| 4.6 The exception loop | CAP-S7-012 | This loop has no owner today, so its cases do not close; it is the release's answer to that finding |
| 4.7 Recovery after charge-off and the sale | CAP-S7-015, CAP-S7-016 | Recovery after charge-off is a revenue stream; it needs the payment match that P8 already publishes, and the sale route that S6 already owns |
| 4.8 Closure and retention | CAP-S7-013 | A closure without the retention class and the reopening control is how a written-off case returns to the list |

Rationale: the wave-4 slice is the smallest set that delivers the E6 outcome for this service, and each slice is independently demonstrable. CAP-S7-014 is Should and may slip within the wave without holding the release. CAP-S7-016 carries a scheduling risk of its own: the agency and the buyer are reached through S9 and S6, and S9 is created in this wave, so the placement and the sale are demonstrable only once the partner contract is published in the same wave (GAP-1798, GAP-1799).

## 10.4 Later increments

| Increment | What unlocks it |
|---|---|
| The write-off route set as a governed package | Phase 2 of the Drools design, with the 51 rules R-WO-01 to R-WO-51, their version label and their owner in rwb-decision (GAP-1802; ASM-2978) |
| The eligibility and tax criteria as business policy | The criteria and the meaning of the two tracks agreed by the write-off committee member with Finance (Q-006; GAP-1803) |
| The exception loop with a named owner and a published time limit | The owner and the limit decided (Q-007; GAP-1804; ASM-014) |
| The write-off cap as a reported position | The cap agreed, so that the population can be held inside it and the headroom reported (GAP-1805; RISK-004) |
| The provision feed as a managed interface | The P2 interface agreed for the Finance file (GAP-1796) |
| The four remaining entity groups' physical tables | The data architect's table list, added with the DB story (GAP-1794; ASM-2970) |
| Completeness and the write-off measures at full width | The rwb-reporting read model, fed by the decision record and the events (ADR-018) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in system test against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-S7-001 | FR-S7-003, FR-S7-004, FR-S7-008, NFR-S7-006 | a cut-off date that has been reached, the ALS source recorded as COMPLETED, and the rules in force | the Schedule fires on the 3rd working day | the scan tests every open case against the eligibility rule on both tracks, proposes the population, returns the run reference, the cut-off date, the rule version and the counts per state, and completes inside the 3 working days the pack has | AC-S7-001-01, AC-BG-S7-001-01; R-WO-01 |
| AC-S7-002 | FR-S7-005 | the tax criteria version has not been published, and in a second run the ALS extract is absent for the cut-off date | the scan is triggered | the first run is held and shows MSG-S7-001; the second is held and raises an incident; both restart for that cut-off date once the cause is cleared | AC-S7-002-01; R-WO-02, R-WO-03, R-WO-04; VR-S7-001-1 |
| AC-S7-003 | FR-S7-006, FR-S7-007 | a population of accounts, some meeting the tax criteria and some not, and a new criteria version with a valid-from date | the scan runs under the new version and an earlier scan is read | each account carries its tax result with the criteria version behind it, the earlier scan keeps the version it ran under, and no release was needed for the change | AC-S7-002-01; R-WO-01; BR-S7-002 |
| AC-S7-004 | FR-S7-001, FR-S7-002, NFR-S7-007, NFR-S7-008 | a branch that reads `v_ace_write_off` directly, a schema constraint that references an ACE table, one data product STALE at the business date and a second that cannot be read at all | the pipeline, the boundary test and then a scan and a posting run | the build fails naming the view read and the cross-schema constraint; the stale product is shown with its date and MSG-P1-001; with the second product unreadable no posting starts; every record states the business date and load time it used | AC-EXC-S7-009-01; VR-S7-005-1; NFR-013, NFR-014 |
| AC-S7-005 | FR-S7-009, NFR-S7-004, NFR-S7-031 | a proposed case with its balance, provision carried, route history, legal and asset state and residual; in a second run the agent does not answer inside 60 seconds and a third answers with a schema the check rejects | the pack is prepared | the pack exists from those inputs in the first run; in the second and third the template pack is used, the pack is still routed, and the model and prompt versions are recorded with the attempt | AC-S7-003-01; R-WO-05; NFR-010, NFR-024, NFR-055 |
| AC-S7-006 | FR-S7-010 | a pack without the provision carried, and a second without its document | the pack is prepared | the pack is held with a data quality task for a named owner role; once both are present the pack is routed to the committee and the hold is closed | AC-S7-003-01; R-WO-09, R-WO-10 |
| AC-S7-007 | FR-S7-011, FR-S7-012, FR-S7-013 | a proposed case, a removal with no reason, a case with an open deviation X3, and a case whose removal cause is cleared | the team removes the cases and the deviation is cleared | the removal without a reason is refused and nothing changes; the case with the deviation is held out and routed to the deviation handler with the deviation recorded; both cases return at the next cut-off with the earlier removal and its reason readable | AC-S7-004-01; R-WO-06, R-WO-07, R-WO-08 |
| AC-S7-008 | FR-S7-014 | a pack inside the write-off committee limit and a monthly meeting in the calendar | the pack is routed | the pack is in the committee queue and booked into the meeting before the meeting date | AC-S7-005-01; R-WO-11 |
| AC-S7-009 | FR-S7-015 | an amount above the write-off committee limit | the pack is routed | the pack reaches the credit approval committee chaired by the product head with Risk with its evidence, before the scheduled meeting | AC-S7-005-01; R-WO-12 |
| AC-S7-010 | FR-S7-016, FR-S7-020, NFR-S7-020 | an amount inside the delegation and a delegation table in force | the committee approves the account | the decision records the final call, the approver role, the limit applied and the rule version, the approval is taken through the approval workflow, and the case is released to posting in the same step | AC-S7-006-01; R-WO-13, R-WO-15 |
| AC-S7-011 | FR-S7-017 | a pack in front of the committee | the committee rejects it with a reason | the reason is recorded and the case returns to the pursue track with the case owner as the next actor | AC-S7-007-01; R-WO-14, R-WO-16 |
| AC-S7-012 | FR-S7-018 | a pack the committee is not ready to decide and a review date | the committee defers it | the review date is recorded, the review timer is set, the case is held, and it returns to the next monthly scan on the review date | AC-S7-008-01; R-WO-17, R-WO-19 |
| AC-S7-013 | FR-S7-019 | a rejection with no reason and a deferral with no review date | the committee submits each decision | both are refused and returned to the committee unchanged, with the refusal recorded | AC-S7-007-01, AC-S7-008-01; R-WO-18 |
| AC-S7-014 | FR-S7-021, FR-S7-022, NFR-S7-019, NFR-S7-025 | a user without the capability area `WRITE_OFF_AND_POSTING`, signed in with single sign-on, and a decision record store that rejects every write | they try to approve, reject and defer, and then a decision is taken with the store down | every attempt is refused with MSG-P4-002 and nothing changes; with the store down nothing changes, MSG-P7-003 is shown, an incident is raised, and the decision is reproducible from the log with its rule version and approver once it is recorded | AC-EXC-S7-006-01, AC-EXC-S7-006-02, AC-EXC-S7-012-02; NFR-033, NFR-034, NFR-042 |
| AC-S7-015 | FR-S7-023, FR-S7-029, NFR-S7-012 | an approved write-off, a posting window that is open, no unmatched payment in flight, and a central ledger that has not yet confirmed the decision record | the posting task is created | the posting waits for the ledger acknowledgement and proceeds only on it; where the ledger is late an alert is raised and no posting is taken on an unconfirmed record; the posting runs as a step on the posting service's queue and this service writes no posting entry | AC-S7-009-01; Arch v5 slide 28 (strict mode); NFR-025 |
| AC-S7-016 | FR-S7-024, FR-S7-025, NFR-S7-012 | ALS and the general ledger return a reference in the first run, reject the second inside the retry limit, and reject the third at the retry limit | the posting runs in each case | the first records the reference; the second is held with its cause and re-posted; the third raises the write-off exception instead of retrying again | AC-S7-009-01; R-WO-21 to R-WO-24 |
| AC-S7-017 | FR-S7-026, FR-S7-027, NFR-S7-009 | a posted write-off with a provision carried, and a Finance file that is rejected once then accepted | the provision is released and the feed runs | the released amount is recorded against the case and the posting reference; the file is retried and its reference recorded once accepted; no load window and no staging table is created at any point | AC-S7-010-01; R-WO-25 to R-WO-28 |
| AC-S7-018 | FR-S7-028, NFR-S7-022 | an approved population of a known count and amount, and a posted population that differs by one case and one amount | the reconciliation runs | completeness is published, and a write-off exception is raised with the case, the count and the amount that differ; the first-time-right position is measured on the quality assurance sample against the rule version applied | AC-S7-011-01; AC-BG-S7-011-01; R-WO-42, R-WO-43; NFR-037, KPI-009 |
| AC-S7-019 | FR-S7-030, FR-S7-031, FR-S7-032 | a case at the retry limit, a case whose correction the owner decides, and a payment that reopens a question on an approved write-off | the exception is opened and worked | the exception has one named owner role, a time limit and its age; the correction chosen is recorded with its reason and its actor among re-post, return to scan and refer to committee; the questioned write-off is referred to the committee | AC-S7-012-01; R-WO-24, R-WO-41, R-WO-44 to R-WO-46 |
| AC-S7-020 | FR-S7-033, FR-S7-034 | an account whose post charge-off treatment is soft recovery, an agency on the panel with capacity in the first run and none in the second, and a placement whose measured return falls below the panel threshold | the treatment is decided and the placement runs | the first account is placed with the agency chosen on measured return with its terms and end date recorded; the second is held and escalated on its timer; the third is recalled with its reason and placed with the next agency on the scorecard | AC-S7-015-01, AC-S7-016-01; R-WO-29 to R-WO-31, R-WO-34, R-WO-35 |
| AC-S7-021 | FR-S7-036, FR-S7-037, FR-S7-038 | a payment that matches a case and its placement, a payment that matches nothing, and a payment that belongs to an account sold before it arrived | the payments are received | the first is posted as post charge-off income with the agency fee calculated; the second is on the exception list with its value date and is matched and posted once the case is identified; the third is remitted to the buyer with the remittance recorded and the item closed on confirmation | AC-S7-015-01; R-WO-37 to R-WO-40, R-WO-49, R-WO-51 |
| AC-S7-022 | FR-S7-035 | a charged-off population whose placement type is sale and an approved limit | the population is handed over and the buyer settles | the population and the route it went to are recorded, the case closes when the buyer settles and the data transfer completes, and the sale value is on the case | AC-S7-016-01; R-WO-32, R-WO-50 |
| AC-S7-023 | FR-S7-039, FR-S7-040, NFR-S7-014, NFR-S7-015 | a placement that expires with nothing recovered, a case with no open placement, sale or exception, a document with no retention class, and a legal hold on a second case | the retention timer runs and the closure is evaluated | the closure is refused with a document task where the retention class is missing; the clean case closes with the closing entry carrying the cash recovered and the loss and every timer stopped; the case under legal hold does not close | AC-S7-013-01; AC-BG-S7-013-01; R-WO-36, R-WO-47, R-WO-48; NFR-028, NFR-031, NFR-072 |
| AC-S7-024 | FR-S7-041 | a closed write-off | a reopen is attempted with no written rule, then with a written rule, a reason and an approver | the first attempt is refused and nothing changes; the second is recorded with all three | AC-S7-013-01; R-WO-47 |
| AC-S7-025 | NFR-S7-023, NFR-S7-024, NFR-S7-027, NFR-S7-028 | the roles of section 3, a proposal screen, a pack view and an agent call | each role reads a case and the agent drafts a pack | personal fields are masked by role, the identification number never leaves in clear, the agent receives no personal data, every read of a personal field is logged, every record carries its classification, and no personal data appears in WriteOffApproved, in a workflow input or in a log | AC-EXC-S7-001-01; NFR-039, NFR-040, NFR-042, NFR-047 |
| AC-S7-026 | NFR-S7-010, NFR-S7-032, NFR-S7-035 | the service in the month-end close window, and a scheduled run that fails to start | the window opens and the failure occurs | the service is available at the stated level in and out of business hours; the missed run alerts the named owner within 15 minutes with its run book; penetration testing and the security review are signed off before the first production release | AC-BG-S7-001-01; NFR-020, NFR-021, NFR-056, NFR-068 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| REQ-S7-001 (BR-051, RULE-019) | CAP-S7-001, CAP-S7-002, CAP-S7-017 | FR-S7-001, FR-S7-002, FR-S7-003, FR-S7-004, FR-S7-005, FR-S7-006, FR-S7-007, FR-S7-008 | NFR-S7-003, NFR-S7-005, NFR-S7-006, NFR-S7-007, NFR-S7-008, NFR-S7-009, NFR-S7-012 | AC-S7-001, AC-S7-002, AC-S7-003, AC-S7-004 |
| REQ-S7-002 (BR-052) | CAP-S7-003, CAP-S7-004, CAP-S7-005 | FR-S7-009, FR-S7-010, FR-S7-011, FR-S7-012, FR-S7-013, FR-S7-014 | NFR-S7-001, NFR-S7-004, NFR-S7-024, NFR-S7-031, NFR-S7-036 | AC-S7-005, AC-S7-006, AC-S7-007, AC-S7-008 |
| REQ-S7-003 (BR-053, RULE-019) | CAP-S7-005, CAP-S7-006, CAP-S7-007, CAP-S7-008 | FR-S7-015, FR-S7-016, FR-S7-017, FR-S7-018, FR-S7-019, FR-S7-020, FR-S7-021, FR-S7-022 | NFR-S7-010, NFR-S7-019, NFR-S7-020, NFR-S7-021, NFR-S7-029, NFR-S7-033, NFR-S7-034 | AC-S7-009, AC-S7-010, AC-S7-011, AC-S7-012, AC-S7-013, AC-S7-014 |
| REQ-S7-005 (BR-054, BR-055, RULE-020) | CAP-S7-009, CAP-S7-010, CAP-S7-011 | FR-S7-023, FR-S7-024, FR-S7-025, FR-S7-026, FR-S7-027, FR-S7-028, FR-S7-029 | NFR-S7-002, NFR-S7-011, NFR-S7-012, NFR-S7-013, NFR-S7-019 | AC-S7-015, AC-S7-016, AC-S7-017, AC-S7-018 |
| REQ-S7-004 (BR-056, RULE-020) | CAP-S7-012 | FR-S7-030, FR-S7-031, FR-S7-032 | NFR-S7-012, NFR-S7-019, NFR-S7-035 | AC-S7-019 |
| REQ-S7-006 (BR-059, RULE-021) | CAP-S7-015, CAP-S7-016 | FR-S7-033, FR-S7-034, FR-S7-035, FR-S7-038 | NFR-S7-010, NFR-S7-012, NFR-S7-023, NFR-S7-024, NFR-S7-028 | AC-S7-020, AC-S7-022 |
| REQ-S7-007 (BR-059, RULE-021) | CAP-S7-015 | FR-S7-036, FR-S7-037 | NFR-S7-002, NFR-S7-012, NFR-S7-025 | AC-S7-021 |
| REQ-S7-008 (BR-057, RULE-022) | CAP-S7-013 | FR-S7-039, FR-S7-040, FR-S7-041 | NFR-S7-014, NFR-S7-015, NFR-S7-016, NFR-S7-017, NFR-S7-018 | AC-S7-023, AC-S7-024 |
| BR-058 (RULE-019) | CAP-S7-014 | FR-S7-007 | NFR-S7-003, NFR-S7-019, NFR-S7-035 | AC-S7-003 |

BR coverage: 8 of the 8 program requirements of this module (REQ-S7-001 to REQ-S7-008) and 9 of the 9 BRD requirements of E6 that name this service (BR-051 to BR-059) are covered by at least one functional requirement, and the four rules RULE-019 to RULE-022 are covered by the same set. No requirement of this module is left without a functional requirement, and no functional requirement lacks a source requirement. Program requirement REQ-S7-004 is carried by three requirements only because the loop has no owner and no time limit in any source (Q-007; GAP-1804).

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Boundary and conformance test output in system test | FR-S7-001, NFR-S7-031 | Developer with the security administrator |
| Scan drill on the 3rd working day, with a held scan, a failed ALS extract and a restart | FR-S7-003, FR-S7-004, FR-S7-005, FR-S7-006, NFR-S7-006 | QA team |
| Criteria load test with a new version from its valid-from date and no release | FR-S7-007, AC-S7-003 | Center of excellence analyst with the QA team |
| Pack test with an agent timeout, a failed schema check and a pack missing its provision | FR-S7-009, FR-S7-010, NFR-S7-004, NFR-S7-036 | QA team with the model risk officer |
| Population drill with a removal without a reason and a case held by an open deviation | FR-S7-011, FR-S7-012, FR-S7-013 | Write-off team member with the QA team |
| Committee matrix test across the limit, the escalation and the three decisions, including the two refusals | FR-S7-014 to FR-S7-022, NFR-S7-020 | Write-off committee member with the QA team |
| Posting drill with a rejection inside and at the retry limit, and a ledger that has not acknowledged | FR-S7-023, FR-S7-024, FR-S7-025, FR-S7-029, NFR-S7-012 | Credit Administration officer with the QA team |
| Provision release, Finance feed and reconciliation test with a seeded difference | FR-S7-026, FR-S7-027, FR-S7-028, NFR-S7-022 | Finance and CFO delegate with the QA team |
| Exception loop test with each of the three corrections | FR-S7-030, FR-S7-031, FR-S7-032 | Write-off committee member with the QA team |
| Placement, recall, recovery and remittance test through the partner portal | FR-S7-033 to FR-S7-038 | Partner and agency manager with S9 |
| Closure and reopen test with a missing retention class and a legal hold | FR-S7-039, FR-S7-040, FR-S7-041, NFR-S7-014 to NFR-S7-018 | Compliance and PDPA officer with the QA team |
| Write-off reproducibility and the approved-against-posted review | FR-S7-028, NFR-S7-019, NFR-S7-022 | Internal audit with the risk and model risk officer |
| Masking matrix, access log reconciliation and classification review | NFR-S7-023 to NFR-S7-028 | Compliance and PDPA officer |
| Performance and volume test at the stated volume | NFR-S7-001, NFR-S7-002, NFR-S7-003, NFR-S7-005 | QA team |

# 12. Open questions

The FSD's and the BRD's open items are carried forward with their IDs where they have one. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-S7-01 | Does this service read the GL write-off outcome, the balances and the batch status through the source-data contract, and who confirms the contract fields and the freshness response for the ALS source? | Solution architect with P1 | Before wave 4 system test | CAP-S7-001, CAP-S7-009, CAP-S7-017 | GAP-1792; ASM-2968; Arch v5 slides 37 and 45 |
| OQ-S7-02 | Which service owns the write-off posting — this service, P8 as a saga step, or P2 as an interface — and where are the rejection, the retry and the re-post handled? | Solution architect with the P8 owner | Before wave 4 system test | CAP-S7-009, CAP-S7-010, CAP-S7-011 | GAP-1793; ASM-2969 |
| OQ-S7-03 | Which tables hold the eligibility, committee, posting and recovery-after-charge-off groups in schema `rwb_writeoff`, given that the Ownership Map lists only `write_off`? | Data architect | Before the S7 DB story | CAP-S7-001, CAP-S7-005, CAP-S7-009, CAP-S7-015, CAP-S7-013 | GAP-1794; ASM-2970 |
| OQ-S7-04 | Are `GET /write-offs`, `POST /write-offs` and `POST /write-offs/{id}/submit` published by this service, given that slide 20 names them and the Ownership Map and the API specification hold only the scan and the committee-decision operations? | Solution architect | Before the S7 contract story closes | CAP-S7-005, CAP-S7-006, CAP-S7-009 | GAP-1795; ASM-2971 |
| OQ-S7-05 | Which path carries the provision inputs and the tax file to Finance, when P2 is the outbound-only interface service and the matrix gives this service no P2 cell? | Solution architect with the integration lead | Before wave 4 system test | CAP-S7-010 | GAP-1796; ASM-2972 |
| OQ-S7-06 | Who holds the pack document: the document hub at P5, which the matrix does not connect to this service, or a reference held here with the document elsewhere? | Solution architect with the P5 owner | Before wave 4 system test | CAP-S7-003, CAP-S7-013 | GAP-1797; ASM-2973 |
| OQ-S7-07 | How is an agency instructed, scored and recalled when the partner portal is S9 and S9 is created in the same wave as this service? | Partner and agency manager with S9 | Before wave 4 system test | CAP-S7-015 | GAP-1798; ASM-2974 |
| OQ-S7-08 | How is a charged-off population handed to the debt sale route, given that S6 is created one wave earlier and neither service's matrix row shows the other? | Solution architect with the S6 owner | Before wave 4 system test | CAP-S7-016 | GAP-1799; ASM-2975 |
| OQ-S7-09 | Which service moves the case through the twenty case states of D9, given that rwb-case owns the case state and the parent workflow and this service publishes WriteOffApproved? | Solution architect with the P3 owner | Before wave 4 system test | CAP-S7-001, CAP-S7-006, CAP-S7-013 | GAP-1800; ASM-2976 |
| OQ-S7-10 | What are the write-off tax criteria, and what are the two tracks the monthly scan runs on? | Write-off committee member | Before wave 4 release | CAP-S7-001, CAP-S7-002, CAP-S7-014 | Q-006; GAP-1803; ASM-013 |
| OQ-S7-11 | Which role owns the write-off exception loop, and what is its time limit? | Head of recovery | Before wave 4 release | CAP-S7-012 | Q-007; GAP-1804; ASM-014 |
| OQ-S7-12 | What is the write-off cap the policy names, what does it apply to, and how is the headroom reported? | Head of Asset Liquidity with Risk | Before wave 4 release | CAP-S7-001, CAP-S7-011 | GAP-1805; RISK-004 |
| OQ-S7-13 | What is each committee level and limit by decision, product and amount, who is the substitute for each, and who chairs the credit approval committee for a write-off above the limit? | Risk with the product heads | Before wave 4 release | CAP-S7-005, CAP-S7-006 | Q-001; DL18; GAP-1806; ASM-2982 |
| OQ-S7-14 | Which rule package does the scan evaluate, who owns the 51 write-off rules, and when does the package arrive, given that the package codes are Phase 2? | Center of excellence analyst with P7 | Before wave 4 release | CAP-S7-001, CAP-S7-002, CAP-S7-014 | GAP-1802; ASM-2978; DP-04 |
| OQ-S7-15 | What retention period applies to each write-off record class, and which fields are masked for which role (DL26)? | Compliance and PDPA officer | Before wave 4 release | CAP-S7-013, all personal fields | Q-012; DL26; GAP-1808; ASM-2984 |
| OQ-S7-16 | What is the baseline for write-off returns right first time, against the 90 percent target? | Conduct and QA officer | Before wave 4 release | NFR-S7-022 | Q-023; KPI-009; NFR-037 |
| OQ-S7-17 | Which fields does DEF-05 add or change in `write_off`, given that the FSD defers the mirrored GL fields to it and no source read here defines it? | Data architect | Before the S7 DB story | CAP-S7-009, CAP-S7-010 | GAP-1809; ASM-2985 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. Neither the BRD nor the FSD carries an approval this PRD could inherit, so a missing approval is carried as an assumption and not as an answer (GAP-1815; ASM-2991).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 5.14 (S7 requirements, REQ-S7-001 to REQ-S7-008), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan), 9 (open decisions incl. DL18, DL26, DL43), 10.1 to 10.4 (the service epic RWB-SVC-S7, schema and wave 4) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 3.1 and 3.2 (context and problem), 4.2 and 4.4 (E6 outcome, delivery model), 5 (stakeholders and the write-off roles), 7.1 and 7.3 (E6 scope, service and wave), 8.4 (BR-051 to BR-059), 9 (RULE-019 to RULE-022), 10 (KPI-009), 11.1 to 11.4 (ASM-013, ASM-014, CON, DEP-005, DEP-009, DEP-010, RISK-004), 12 (Q-001, Q-006, Q-007, Q-012, Q-023), 13 (governance) |
| Recovery Workbench FSD S7 Write-off and recovery v3 | Document control, Existing capability check, A1 (context, scope, dependencies, feature overview), A2.1 to A2.16 (functional decomposition with field catalog, rules, roles, acceptance criteria and background events), Requirements served, Screens, Appendix A and B |
| Recovery Workbench Business Rules and Routing Logic v4 | The write-off route set R-WO-01 to R-WO-51: state, event, condition, action, next state, owner, systems and the service level of each transition |
| Recovery Workbench Logical Data Model and Data Dictionary v8 | `write_off` and its fields DF-FIN-010 to DF-FIN-020, the read-only `v_ace_write_off` and its fields DF-ACE-261 to DF-ACE-269, the LOVs LOV-STAGE, LOV-TREATMENT, LOV-ROUTE-SET and LOV-CAPABILITY, and the relationships of `write_off` to the case and to the decision log entry |
| Recovery Workbench Physical Schema v6.sql | `write_off`, its two in-schema foreign keys and its comments; the `recovery.v_ace_write_off` view and its note that the write-off decision stays in `recovery.write_off` |
| Recovery Workbench Architecture v5 | Slides 9 to 13 (call types, timeouts, retry, the connection matrix and the S7 row), 20 (the S7 service contract), 24 and 25 (the Temporal model and the child per stage), 28 (the decision record and strict mode at the point of no return), 29 (one schema and login per service), 37 and 45 (what changes and why; who reads ACE), 41 (service catalogue), 42 and 43 (event catalogue, EV-24, EV-25, EV-26), 44 (job map, JOB-16 and JOB-17) |
| Recovery Workbench Temporal and Drools Design v1 | Slide 12 (where S7 uses the kit), slide 13 (WriteOffWorkflow on `rwb-writeoff`), slide 23 (S7 write-off: the seven steps, the Drools decision, who approves, the clocks, the point of no return), and the Phase 2 note on the rule packages |
| Recovery Workbench Microservice Ownership Map v1 | Services (S7 row), Endpoints (`POST /write-off-scans`, `POST /write-offs/{writeOffId}/committee-decision`), Workflows (WriteOffWorkflow), Events (EV-24), Jobs (JOB-16), Tables (`write_off`) and Rulings (JOB-16, ASM-0066) |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R5 (target structure, DP table, wave map), R8 (outputs), R9 (gaps and assumptions) |
