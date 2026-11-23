SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD S3 rwb-guarantee v1
description: Product requirements for the Recovery Workbench guarantee service (S3 rwb-guarantee) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.md; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.md
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S3 Guarantees and guarantors v3.md
service: S3 rwb-guarantee
epic: RWB-SVC-S3
wave: 3
decision: D-RCV-60
---

# Recovery Workbench PRD S3 rwb-guarantee v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD S3 rwb-guarantee |
| Document ID | S3-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | S3 rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 (Epic 4, route decision, guarantees and auction, wave 3) |
| Schema | `rwb_guarantee` |
| REST base | `/api/recovery/guarantee/v1` |
| Topic | `rwb.guarantee.events.v1` |
| Temporal task queue | `rwb-guarantee` |
| Java package | `th.co.scb.ace.workbench.recovery.guarantee` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Business analyst, S3, with the guarantee officer as business owner role |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), ADR-010, ADR-013 to ADR-023 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epics 3 to 8 v1; FSD S3 Guarantees and guarantors v3; Architecture v5; Temporal and Drools Design v1; Microservice Ownership Map v1 |
| Upstream requirement IDs | REQ-S3-001 to REQ-S3-007; BR-022, BR-023, BR-024, BR-025; NFR-001, NFR-008, NFR-009, NFR-010, NFR-011, NFR-013, NFR-014, NFR-015, NFR-020, NFR-021, NFR-022, NFR-023, NFR-024, NFR-025, NFR-026, NFR-027, NFR-033, NFR-034, NFR-035, NFR-039, NFR-040, NFR-042, NFR-045, NFR-046, NFR-047, NFR-049, NFR-051, NFR-052, NFR-053, NFR-054, NFR-055, NFR-059, NFR-060, NFR-061, NFR-064, NFR-066, NFR-067, NFR-068, NFR-078 |
| Upstream feature IDs | FEAT-GUA-01 to FEAT-GUA-08 |
| Upstream rule, field and list IDs | R-GUA-01 to R-GUA-32; BR-S3-001 to BR-S3-008; VR-S3-001-1 to VR-S3-008-1; DF-TRT-015 to DF-TRT-022; LOV-CLAIM-TYPE, LOV-CLAIM-STATUS |
| Upstream API and interface IDs | API-S3-001 (POST /cases/{caseId}/guarantee-claims); API-S3-002 (PATCH /guarantee-claims/{claimId}); INT-29 |
| Upstream workflow, screen and stories | GuaranteeClaimWorkflow; SCR-17 Guarantee claim; RWB-E4-013 to RWB-E4-020 (8 legacy stories) |
| Upstream acceptance criteria | AC-S3-001-01 to AC-S3-008-01 (main success flow, one per feature, each a placeholder); AC-EXC-S3-001-01 to AC-EXC-S3-008-01 (role without the right); AC-EXC-S3-001-02 to AC-EXC-S3-008-02 (decision cannot be recorded). The FSD defines no alternate flow and no system background event for any of the eight features |
| Generated IDs | CAP-S3-001 to CAP-S3-013; FR-S3-001 to FR-S3-032; NFR-S3-001 to NFR-S3-030; AC-S3-001 to AC-S3-022; ROL-S3-01 to ROL-S3-12; JRN-S3-01 to JRN-S3-05; OQ-S3-01 to OQ-S3-16 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD S3 Guarantees and guarantors v3 (15 November 2026), Business Requirements Epics 3 to 8 v1 and Business Requirements Program v5, realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

This is version 1 of the PRD S3 family: the folder holds no earlier PRD for this service, so there is no earlier version to supersede (ASM-2897).

## 1.3 Inherited history and ID continuity

The product baseline is FSD S3 Guarantees and guarantors v3. Its requirement IDs, feature IDs, rule IDs, field IDs, list IDs and acceptance criterion IDs are carried unchanged; the microservice realignment changes the read path, the owner of four capabilities and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only. Everything else unchanged from v2 |
| 1 and 2 | Not specified in the source documents (GAP-1735; ASM-2893) | Earlier versions of the FSD. Their dates and change notes are not in the sources read, and are carried as an open item rather than reconstructed |
| 2 (TSD S3) | 28 October 2026 | Technical baseline read for the data model: one object `guarantee_claim`, its eight fields DF-TRT-015 to DF-TRT-022, two lists and one relationship, 32 rules over 17 states, and API-S3-001 and API-S3-002 |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, journey and open-question IDs are new. The FSD requirement IDs (REQ-S3-001 to REQ-S3-007), feature IDs (FEAT-GUA-01 to FEAT-GUA-08), rule IDs (R-GUA-01 to R-GUA-32, BR-S3-001 to BR-S3-008), validation rule IDs (VR-S3-001-1 to VR-S3-008-1), field IDs (DF-TRT-015 to DF-TRT-022), list IDs (LOV-CLAIM-TYPE, LOV-CLAIM-STATUS), message IDs (MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001), API IDs (API-S3-001, API-S3-002), interface ID (INT-29), workflow ID (GuaranteeClaimWorkflow), screen ID (SCR-17) and acceptance criterion IDs are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the program requirements REQ-S3-001 to REQ-S3-007 and of the non-functional requirements |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-022 to BR-025, the E4 scope, the measures, the risks and the open questions |
| Recovery Workbench Functional Specifications by Module v6, FSD S3 Guarantees and guarantors v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Technical Specifications by Module v5, TSD S3 Guarantees and guarantors v2 | Technical specification | Read for the confirmed object, field, list, state and API facts; its own architecture is superseded by Arch v5 |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, only rwb-source-data reads ACE, Kafka, Temporal, no data lake, edge and gateway |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: GuaranteeClaimWorkflow on `rwb-guarantee`, the notice and approval children, the 32-rule guarantee set, the claim deadline clock and the release authorities |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, endpoint, workflow and ruling named here |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-guarantee (S3) is the recovery module's guarantee route: the claim on a Thai Credit Guarantee Corporation scheme or on an insurer, and the pursuit of the guarantors and co-borrowers behind a debt. It turns "a guarantee is found, and somebody has to file before the deadline" into a product: a claim that exists as one record from the day the guarantee is found; a deadline that is a clock in the workflow rather than a date in a spreadsheet, with a warning before it passes and a recorded loss when it does; a claim assembled against the scheme checklist, verified by the guarantee officer and submitted with its reference on the case; a claim followed through query, part payment, rejection and resubmission to the money; a subrogation position recorded at the moment of payment so the bank's share of every later recovery is not lost; a demand that reaches every guarantor and co-borrower from the approved template and is timed from proof of delivery; a guarantor answer that enters the same treatment paths as a borrower's; and a case that closes when the guarantee clears the debt, or returns its residual to the route decision.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-guarantee | One deployable with its own API and worker, schema `rwb_guarantee`, login, topic `rwb.guarantee.events.v1`, task queue `rwb-guarantee` and lifecycle | The guarantee route becomes one owned product with its own release, instead of a screen and a job inside a single deployable |
| The claim as a governed record | One record per claim with its type, deadline, amount claimed, amount paid and status, linked to the case by business key | A claim filed from memory is a claim that is filed late or filed twice |
| The claim deadline as a workflow timer | The deadline, the preparation window and the warning window are durable timers inside GuaranteeClaimWorkflow | The design states it plainly: a missed claim deadline cannot be undone, so the date cannot live in a person's diary |
| The claim as a tracked case state | Query, part payment, rejection, resubmission and the balance claim are states the case shows, not notes in a document | The claim is money in flight, and its position has to be readable without asking the officer |
| The subrogation position | The TCG share of every later recovery is recorded against the case at payment | What the guarantor may reclaim, or must share, is the position the bank loses when nobody writes it down |
| The guarantor demand on the shared notice path | The demand to every guarantor and co-borrower goes through the communications service from an approved template, timed from proof of delivery | The notice is a legal step; its period runs from delivery, not from posting |
| The claim events | GuaranteeClaimFiled and GuaranteeClaimSettled on `rwb.guarantee.events.v1`, consumed by rwb-case and rwb-reporting | The case moves on the claim, not on a poll, and the measure counts the claim, not a table copy |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its ingestion from the TCG channel, SVAF and ALS, and its backups | REUSE | ACE team |
| The read-only view contract and the freshness of every data product | REUSE, elsewhere | P1 rwb-source-data (this service reads it by contract) |
| Case record, CMMN state, queues, tasks, allocation and the case timers | REUSE | P3 rwb-case (GuaranteeClaimWorkflow is its child workflow) |
| Approval workflow, decision record, hash chain and rule package registry | REUSE | P7 rwb-decision |
| Roles, capability areas, masking policy and the delegation table | REUSE | P4 rwb-access |
| Notices, templates, merge fields and proof of delivery | REUSE | P6 rwb-comms |
| Payment and proceeds matching, posting to the ledger and the payment events | REUSE | P8 rwb-payment |
| Documents, checklist evidence and the scheme document set | REUSE | P5 rwb-document |
| Agent runtime, model endpoint, guardrails and run record | REUSE | P10 rwb-agent (GAP-1719; ASM-2877) |
| Appraisal and the re-appraisal order behind a collateral event | REUSE, elsewhere | S1 rwb-valuation (FEAT-VAL-01 through the P1 contract) |
| Screens and the composite route that serves them | REUSE | Platform edge, gateway-bff (RWB-PLT-EDGE) |
| Quartz scheduling of the claim and notice clocks | REPLACED | Temporal workflow kit (PLT); ADR-016, DP-10 |
| The module's published Java interface and in-process calls to other modules | REPLACED | Contract-first REST and Temporal call types; ADR-020, DP-11 |
| Direct call to WIN for the guarantor letter and to ALS for the posting | MOVED | P6 for the notice, P8 for the posting |
| The dated DP04 guarantee-claim copy read for reporting | REUSE, elsewhere | P1 rwb-source-data (ASM-0080) |
| Collections before day 90 and decisions D1 to D4 | OUT OF SCOPE | EFS and the ACE collection module |
| Booking in the core bank and credit approval in the lending system | OUT OF SCOPE | The officer and the core bank; this service records the result |
| The TCG quota and claim policy itself | OUT OF SCOPE | The scheme owner; the values are reference data here (GAP-1728; ASM-2886) |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014; slides 37 and 45).
2. The service writes only schema `rwb_guarantee`; no cross-schema join and no foreign key into `public` (ADR-014, DP-01).
3. A route service reaches a shared capability through Temporal, never REST. The connection matrix gives this service Temporal to P7 and to P6, Temporal and events to and from P6, events from P8, and no cell to P1, P2 or P10 (slide 13, ADR-020; GAP-1717, GAP-1718, GAP-1719).
4. REST is one hop from gateway-bff with a 2 s timeout, an Idempotency-Key on every POST and RFC 9457 problem details; a GET is retried once with jitter, and there is a circuit breaker and a bulkhead per downstream (ADR-020; slides 10 and 11).
5. Events are CloudEvents 1.0 on Kafka with an outbox and an inbox, retry at 1 minute, 10 minutes and 1 hour and then a dead-letter topic; topic `rwb.guarantee.events.v1`, key `caseId` (ADR-015, DP-09, DP-14; slides 9 and 11).
6. Temporal namespace `rwb-recovery`, task queue `rwb-guarantee`; GuaranteeClaimWorkflow is a child of CaseWorkflow started on its owner's queue; Schedules and durable timers replace Quartz, and no shared scheduler table remains (ADR-016, DP-10; slide 18; Temporal slide 19).
7. Rules are versioned data evaluated in process by the embedded Drools kit; the guarantee route set is 32 rules over 17 states and its package is Phase 2 (ADR-017, DP-04; Temporal slide 19; GAP-1723, ASM-2881).
8. There is no data lake: claim measures and reporting read the decision record and the events into rwb-reporting (ADR-018, DP-17).
9. Personal data stays out of events, workflow inputs and logs; masking is by role, using the permission data cached from rwb-access, and each service authorises the object itself (slide 10; NFR-039, NFR-040).
10. The bank scheduler owns only the cross-system edges and signals the business date; it never enters the case journey (slide 32).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-S3-01 | Guarantee officer | A claim prepared before the deadline, a warning before it passes, and a submission it can own | JRN-S3-01, JRN-S3-02, JRN-S3-03 |
| ROL-S3-02 | Case owner | A demand that reaches every guarantor and co-borrower, a place to record the answer, and a case that moves on it | JRN-S3-04 |
| ROL-S3-03 | Head of Litigation | The warning when a claim is about to be lost, and the release of a TCG guarantee at the authority it names | JRN-S3-02, JRN-S3-05 |
| ROL-S3-04 | Product head (Mortgage, HP, SSME) | A release of a guarantor inside the level the delegation names | JRN-S3-05 |
| ROL-S3-05 | Team manager | Claims that are ageing, missed or stalled in a query, visible without asking | JRN-S3-03 |
| ROL-S3-06 | Center of excellence analyst | The rule package and version applied at every claim step, and a rule set that measures can be read against | JRN-S3-05 |
| ROL-S3-07 | Risk and model risk officer | The agent's acceptance, override, latency and cost on claim preparation, and the runs where the checklist result was used | JRN-S3-05 |
| ROL-S3-08 | Compliance and PDPA officer | Masking by role, an access log that cannot be skipped, a classification on every record, and the conduct position on a disputed guarantee | JRN-S3-04, JRN-S3-05 |
| ROL-S3-09 | Internal audit | A claim, its rejection, its payment and its share reproducible from the log with the rule version applied | JRN-S3-05 |
| ROL-S3-10 | Platform administrator | A timer that reports a breach, an alert with a named owner, and a replay path | JRN-S3-03 |
| ROL-S3-11 | Hardship and vulnerability specialist | An insurance claim raised on a collateral event without losing the contact limits of the case (FSD A2.8 role) | JRN-S3-04 |
| ROL-S3-12 | Developer | A typed contract to build against, a fake for every dependency, and a build that fails on a direct ACE read | JRN-S3-05 |

Non-human actors: the case workflow that starts GuaranteeClaimWorkflow; the approval workflow on rwb-decision; the notice dispatch on rwb-comms; the claim preparation agent on rwb-agent; the payment matching that produces ProceedsMatched; the outbox relay; the consumers of GuaranteeClaimFiled and GuaranteeClaimSettled; the TCG claim channel as an external system (INT-29).

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. Guarantee and TCG claims are late because deadlines are not tracked (FSD A1.3); the scheme's deadline is held in a person's record and not in the case.
2. The claim is assembled by hand from the case facts and the documents the scheme requires, and the checklist is a document rather than a control.
3. The claim status is one of five values on a module record, while the claim itself moves through seventeen states that nothing shows on the case.
4. The demand to guarantors and co-borrowers goes out on the shared notice path, and the pursuit outcome is written into a narrative rather than against the party.
5. What the guarantor may reclaim, and the share the scheme takes of every later recovery, is recorded late or not at all.
6. The claim result is entered into the TCG portal by the guarantee officer, and the reference is typed into the case; the module publishes no event.

Consequence: a claim can be lost without anybody noticing, and a paid claim can leave the bank with a share nobody recorded.

## 4.2 Target state (this product)

### JRN-S3-01 The guarantee found, and the deadline begins (at takeover or at a later review, guarantee officer and system)

1. A guarantee is found on the case at takeover, and the case reaches decision D6.5 or D6.6; rwb-case starts GuaranteeClaimWorkflow on this service.
2. Where the guarantee type is the TCG scheme and a scheme code is present, the claim deadline is read from the reference data for that scheme and the deadline timer starts from the date the default conditions are met (R-GUA-01).
3. Where the scheme's default conditions are not satisfied, the claim is recorded as not arising, the guarantee is held, and the conditions are tested again at the later review (R-GUA-02, R-GUA-03).
4. The claim exists as one record on the case with its type, deadline and amount claimed, from the moment the guarantee is found; the case shows the days remaining.

### JRN-S3-02 Prepare, verify and submit the claim (as the preparation window opens, guarantee officer)

1. Where the days to the deadline reach the preparation window, the claim enters preparation (R-GUA-04).
2. The claim is assembled against the scheme checklist; the agent assembles it through the agent contract, and the checklist result is used where the agent is slow or its answer fails the schema check (GAP-1719; ASM-2877).
3. A complete checklist presents the claim to the guarantee officer for approval (R-GUA-07); an incomplete one raises the retrieval requests and holds the claim (R-GUA-08), and the claim returns to preparation when the documents are supplied (R-GUA-10).
4. Where the days to the deadline reach the warning window, the guarantee officer and the Head of Litigation are escalated (R-GUA-11).
5. The guarantee officer verifies and approves the claim (R-GUA-12), or sends it back for rework with the reason (R-GUA-13).
6. The claim is submitted and its reference, date and channel are recorded on the case; the claim moves to CLAIM_SUBMITTED (GAP-1718; ASM-2876).
7. Where the deadline passes before submission, the claim is recorded as lost with its reason and amount, the breach is reported, and the loss cannot be undone (R-GUA-05, R-GUA-09).

### JRN-S3-03 Track the claim to payment (as the claim moves, guarantee officer and team manager)

1. A query from the scheme holds the claim and raises a task to the guarantee officer; the answer resubmits the claim, and a query that lapses treats the claim as rejected (R-GUA-14, R-GUA-15, R-GUA-16).
2. A rejection records its reason and is assessed for resubmission: a curable reason reworks the claim, and a reason that is not curable closes the guarantee and returns the full balance to the route decision (R-GUA-17, R-GUA-18, R-GUA-19).
3. A part payment is matched and posted, and the balance claim is submitted while the deadline still allows it (R-GUA-20, R-GUA-21).
4. The claim's status, its paid amount and any shortfall are on the case, and the team manager sees the claims that are ageing or stalled without asking for a list.

### JRN-S3-04 The guarantor demand and the answer (in parallel with the claim, case owner)

1. Where the guarantee type is a personal guarantor, a co-borrower or a corporate, the demand is issued from the approved template to every guarantor and co-borrower on the case, and its period is timed from proof of delivery (R-GUA-06).
2. The case owner negotiates inside the range and records the outcome against the party, with the required fields enforced (VR-S3-006-1, MSG-GEN-001).
3. An answer that settles books the treatment, reduces the balance and closes the guarantee (R-GUA-28), and the guarantor then follows the same treatment paths as a borrower.
4. A refusal, or no reply by the notice expiry, records the refusal and returns the case to the route decision (R-GUA-29).
5. A dispute about the guarantee raises the deviation X1, stops contact on the disputed item and holds the pursuit; a dispute that is not upheld resumes the pursuit from the notice, and one that is upheld releases the guarantor and returns the case to the route decision (R-GUA-30, R-GUA-31, R-GUA-32).

### JRN-S3-05 The position after payment, and the evidence read later (at payment; audit and risk later)

1. Where the paid amount equals the guaranteed amount, the payment is matched and posted and the subrogation position is set with the share the scheme holds of every later recovery (R-GUA-22, R-GUA-23, R-GUA-24).
2. Where the balance after the guaranteed share is zero, the guarantee and the case are closed (R-GUA-26); where a balance remains, the residual returns to the route decision at D6 (R-GUA-25), and a recorded loss does the same (R-GUA-27).
3. A release of a guarantor, or of a TCG guarantee, runs through the approval path in rwb-decision with the level the delegation table names at run time (GAP-1725; ASM-2883).
4. An auditor reads one claim end to end: the deadline, the assembler, the checklist, the approval, the submission reference, each query and rejection with its reason, each payment, the share, and the rule version applied at every step.
5. The model risk officer reads the agent's acceptance, override, latency and cost on claim preparation, and the runs where the checklist result was used instead (NFR-066, NFR-078).
6. A developer builds against the published contract and its fake; a build that reads an ACE view or an ACE table directly fails (GAP-1717; ASM-2875).

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-S3-001 | The claim as one governed record | A claim exists from the day the guarantee is found, with its type, deadline, amount claimed and status, and it is read and updated through one contract | BR-022 | Must | 3 | FEAT-GUA-01 (A2.1) |
| CAP-S3-002 | The claim deadline clock and the warning | The deadline is a timer the workflow holds, a warning arrives before it passes, and a loss is recorded with its reason | BR-022 | Must | 3 | FEAT-GUA-01 (A2.1) |
| CAP-S3-003 | Claim preparation against the scheme checklist | The claim is assembled against the checklist, with the documents it needs named, and an incomplete claim is held rather than filed | BR-022 | Must | 3 | FEAT-GUA-01 (A2.1) |
| CAP-S3-004 | Officer verification and submission | The guarantee officer verifies and approves the claim, and the submission is recorded with its reference on the case | BR-022 | Must | 3 | FEAT-GUA-02 (A2.2) |
| CAP-S3-005 | The claim tracked to payment | Query, part payment, rejection, resubmission and the balance claim are states the case shows | BR-022 | Must | 3 | FEAT-GUA-03 (A2.3) |
| CAP-S3-006 | The subrogation position | What the scheme shares of every later recovery is recorded at payment, not reconstructed afterwards | BR-023 | Must | 3 | FEAT-GUA-04 (A2.4) |
| CAP-S3-007 | Guarantor and co-borrower notices | The demand reaches every guarantor and co-borrower from the approved template, timed from proof of delivery | BR-024 | Must | 3 | FEAT-GUA-05 (A2.5) |
| CAP-S3-008 | Guarantor negotiation and the answer | The case owner negotiates inside the range, records the outcome against the party, and the guarantor enters the borrower's treatment paths | BR-024 | Must | 3 | FEAT-GUA-06 (A2.6) |
| CAP-S3-009 | Closure when the guarantee clears the debt | A payment that clears the balance closes the case, and a residual returns to the route decision instead of sitting in a guarantee state | BR-023 | Must | 3 | FEAT-GUA-07 (A2.7) |
| CAP-S3-010 | Insurance claim on a collateral event | A stolen, written-off or damaged collateral files its claim and triggers the re-appraisal before the next decision | BR-025 | Must | 3 | FEAT-GUA-08 (A2.8) |
| CAP-S3-011 | Freshness and the data date at the claim | Every claim step shows how old its data is, and a stale product is seen rather than assumed | BR-022 | Must | 3 | A2.1 to A2.8 (VR-S3-001-1 to VR-S3-008-1) |
| CAP-S3-012 | Guarantor pursuit, dispute and release | A disputed guarantee stops contact and holds the pursuit, and a release runs through the approval the delegation names | BR-024 | Must | 3 | A2.5 and A2.6 with R-GUA-28 to R-GUA-32 |
| CAP-S3-013 | Claim eligibility before submission | A claim that does not meet the scheme's conditions is not filed, and the reason is recorded | BR-022 | Should | 3 | A2.1 (R-GUA-02), A2.2 |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Direct read of the ACE claim, party, balance and scheme views | Not carried | rwb-source-data's contract (GAP-1717; ASM-2875) |
| Filing the claim inside the TCG portal | Not carried as an automatic submission | The guarantee officer, or rwb-integration when INT-29 becomes available (GAP-1718; ASM-2876) |
| Quartz scheduling of the claim deadline and notice clocks | Replaced | Durable timers in GuaranteeClaimWorkflow through the workflow kit (ADR-016, DP-10) |
| The guarantor letter through WIN and the posting through ALS, called directly | Not carried | P6 rwb-comms for the notice, P8 rwb-payment for the posting |
| The module's published Java interface and in-process calls | Replaced | Contract-first REST and Temporal call types (ADR-020, DP-11) |
| The dated DP04 guarantee-claim copy held for reporting | Reused, elsewhere | P1 rwb-source-data, built from the events (ASM-0080) |
| Where the guarantor, the guaranteed amount and the share are recorded today | Open | This service's schema in a record that no source confirms (GAP-1721; ASM-2879) |
| The guarantee route's number in the route mix | Not asserted here | Reference data once the numbering is agreed (GAP-1732; ASM-2890) |

# 6. Functional requirements

Every requirement is specific and testable. The FSD REQ column keeps the trace to the source program requirement. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-S3-001 | The service SHALL obtain every case, party, guarantee, balance, payment and freshness fact it needs through the contracts of the services that own them, and SHALL NOT read a `recovery.v_ace_*` view or an ACE table. A read of a view, a read of an ACE table, and a constraint in schema `rwb_guarantee` that references a table outside it, SHALL fail the build and the boundary test. | CAP-S3-001 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-002 | The service SHALL hold one claim record per claim, linked to the case by a business-key column of type `uuid` that carries no foreign key, and SHALL hold the claim type from LOV-CLAIM-TYPE, the claim deadline, the amount claimed in baht, the date filed, the amount paid in baht and the claim status from LOV-CLAIM-STATUS, with the field identifiers DF-TRT-015 to DF-TRT-022. | CAP-S3-001 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-003 | The service SHALL show on the claim both the state GuaranteeClaimWorkflow is in and the published claim status, SHALL hold one current state per claim at any time, and SHALL make the two agree through a mapping held as versioned reference data (GAP-1720; ASM-2878). | CAP-S3-001 | BR-022 | REQ-S3-002 | Must | 3 |
| FR-S3-004 | The service SHALL open a claim through `POST /cases/{caseId}/guarantee-claims` (API-S3-001) under the capability area Treatment and offer with right C, SHALL require an Idempotency-Key, SHALL return the claim with 201, and SHALL return 409 without creating a second claim where that case already carries a claim of the same type. | CAP-S3-001 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-005 | The service SHALL record the claim result through `PATCH /guarantee-claims/{claimId}` (API-S3-002) under the same capability area with right U, SHALL return the updated claim with 200, and SHALL reject a value that is not in LOV-CLAIM-STATUS or LOV-CLAIM-TYPE with 422 and MSG-GEN-001. | CAP-S3-005 | BR-022 | REQ-S3-002 | Must | 3 |
| FR-S3-006 | The service SHALL refuse the open, the update, the approval, the negotiation and the release to a role without the capability area, with MSG-P4-002, and SHALL change nothing on the claim or the case on a refusal. | CAP-S3-001 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-007 | The service SHALL write the decision record for every claim step before the change it describes, SHALL record the rule package and rule version evaluated, and where the record cannot be written SHALL change nothing, show MSG-P7-003 and raise an incident. | CAP-S3-001 | BR-022 | REQ-S3-002 | Must | 3 |
| FR-S3-008 | The service SHALL start the claim deadline timer from the date the scheme's default conditions are met where the guarantee type is the TCG scheme and a scheme code is present (R-GUA-01), SHALL hold it as a durable timer inside GuaranteeClaimWorkflow, and SHALL use no Quartz table, connection or job. | CAP-S3-002 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-009 | The service SHALL read the claim deadline, the preparation window and the warning window from versioned reference data per scheme at run time, and a change SHALL take effect from its valid-from date without a code release. | CAP-S3-002 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-010 | The service SHALL move the claim into preparation where the days to the deadline reach the preparation window (R-GUA-04), and SHALL record the days remaining and the window applied with that move. | CAP-S3-003 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-011 | The service SHALL assemble the claim against the scheme checklist, SHALL present it to the guarantee officer for approval where every checklist item is present (R-GUA-07), SHALL raise the retrieval requests and hold the claim where an item is missing (R-GUA-08), and SHALL return the claim to preparation when the missing items are supplied (R-GUA-10). | CAP-S3-003 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-012 | The service SHALL ask the claim preparation agent to assemble the claim through the rwb-agent contract, SHALL wait at most 60 seconds for its answer, and where the answer arrives late or fails its schema check SHALL use the checklist result and continue the preparation, recording which of the two assembled the claim (GAP-1719; ASM-2877). | CAP-S3-003 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-013 | The service SHALL escalate to the guarantee officer and the Head of Litigation where the days to the deadline reach the warning window (R-GUA-11), and SHALL show the days remaining with the escalation. | CAP-S3-002 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-014 | The service SHALL record the claim as lost, with the reason and the amount claimed, and report the breach where the deadline passes before submission (R-GUA-05, R-GUA-09), and SHALL not allow a step that reverses the loss. | CAP-S3-002 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-015 | The service SHALL let the guarantee officer verify and approve the claim (R-GUA-12) or send it back for rework with the reason (R-GUA-13), SHALL record the approving role, the time and the rule version, and SHALL change the claim only on the approval. | CAP-S3-004 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-016 | The service SHALL record the submission of a claim with its reference, its date and the channel used, SHALL move the claim to CLAIM_SUBMITTED on that record, and where no TCG interface exists SHALL accept the reference the guarantee officer enters after filing outside the Workbench (GAP-1718; ASM-2876). | CAP-S3-004 | BR-022 | REQ-S3-001 | Must | 3 |
| FR-S3-017 | The service SHALL test a claim against the scheme's eligibility conditions before submission, SHALL not submit a claim that fails them, and SHALL record the failed condition and the rule version with the claim. | CAP-S3-013 | BR-022 | REQ-S3-007 | Should | 3 |
| FR-S3-018 | The service SHALL record that no claim arises and hold the guarantee where the scheme's default conditions are not satisfied (R-GUA-02), and SHALL test the conditions again at the later review and start the deadline timer where they are then met (R-GUA-03). | CAP-S3-013 | BR-022 | REQ-S3-007 | Should | 3 |
| FR-S3-019 | The service SHALL hold the claim and raise a task to the guarantee officer on a query from the scheme (R-GUA-14), SHALL resubmit on the answer (R-GUA-15), and SHALL record the lapse and treat the claim as rejected where the query response window passes (R-GUA-16). | CAP-S3-005 | BR-022 | REQ-S3-002 | Must | 3 |
| FR-S3-020 | The service SHALL record a rejection with its reason (R-GUA-17), SHALL assess resubmission, SHALL rework a claim whose reason is curable inside the deadline (R-GUA-18), and SHALL close the guarantee and return the full balance to the route decision where the reason is not curable or the deadline has passed (R-GUA-19). | CAP-S3-005 | BR-022, BR-023 | REQ-S3-006 | Must | 3 |
| FR-S3-021 | The service SHALL match a part payment to the claim, record the amount paid and the shortfall on the case, and submit the balance claim while the deadline still allows it (R-GUA-20, R-GUA-21). | CAP-S3-005 | BR-022 | REQ-S3-002 | Must | 3 |
| FR-S3-022 | The service SHALL set the subrogation position where the amount paid equals the guaranteed amount, and SHALL record the share the scheme holds of every later recovery against the case with the rule version applied (R-GUA-22, R-GUA-23, R-GUA-24). | CAP-S3-006 | BR-023 | REQ-S3-003 | Must | 3 |
| FR-S3-023 | The service SHALL close the guarantee and the case where the balance after the guaranteed share is zero (R-GUA-26), and SHALL return the residual to the route decision at D6 where a balance remains or a loss is recorded (R-GUA-25, R-GUA-27), so that rwb-case moves the case without a second action. | CAP-S3-009 | BR-023 | REQ-S3-003 | Must | 3 |
| FR-S3-024 | The service SHALL issue the demand to every guarantor and co-borrower on the case where the guarantee type is a personal guarantor, a co-borrower or a corporate (R-GUA-06), SHALL take the letter from the approved template in rwb-comms through its contract, and SHALL time the notice period from proof of delivery. | CAP-S3-007 | BR-024 | REQ-S3-004 | Must | 3 |
| FR-S3-025 | The service SHALL record a guarantor answer that settles as a treatment booked against the case, with the balance reduced and the guarantee closed (R-GUA-28), and SHALL put the guarantor into the same treatment paths a borrower enters. | CAP-S3-008 | BR-024 | REQ-S3-005 | Must | 3 |
| FR-S3-026 | The service SHALL record a refusal, or the expiry of the notice with no reply, against the party and SHALL return the case to the route decision (R-GUA-29). | CAP-S3-008 | BR-024 | REQ-S3-005 | Must | 3 |
| FR-S3-027 | The service SHALL let the case owner negotiate inside the range in force, SHALL record the outcome against the party with the range and the rule version applied, and SHALL enforce the required fields with MSG-GEN-001 (VR-S3-006-1). | CAP-S3-008 | BR-024 | REQ-S3-005 | Must | 3 |
| FR-S3-028 | The service SHALL raise the deviation X1, stop contact on the disputed item and hold the pursuit on a dispute about the guarantee (R-GUA-30), SHALL resume the pursuit from the notice where the dispute is not upheld (R-GUA-31), and SHALL release the guarantor and return the case to the route decision where it is upheld (R-GUA-32). | CAP-S3-012 | BR-024 | REQ-S3-005 | Must | 3 |
| FR-S3-029 | The service SHALL route a release of a guarantor, and a release of a TCG guarantee, through the approval path in rwb-decision, SHALL read the level and the limit that apply from the delegation table at run time, and SHALL record the level applied and the approving role (GAP-1725; ASM-2883). | CAP-S3-012 | BR-024 | REQ-S3-006 | Must | 3 |
| FR-S3-030 | The service SHALL file an insurance claim where the collateral is stolen, written off or damaged, SHALL record its type from LOV-CLAIM-TYPE, and SHALL raise the re-appraisal order through the rwb-valuation contract so that the new value is in force before the next decision. | CAP-S3-010 | BR-025 | REQ-S3-002 | Must | 3 |
| FR-S3-031 | The service SHALL start no claim step on a data product whose freshness cannot be read, SHALL show the stale product with its date and MSG-P1-001, SHALL record the business date and load time it acted on, and SHALL hold no load window, staging table or catch-up job. | CAP-S3-011 | BR-022 | REQ-S3-002 | Must | 3 |
| FR-S3-032 | The service SHALL publish GuaranteeClaimFiled at submission and GuaranteeClaimSettled at payment or release on `rwb.guarantee.events.v1`, keyed by case, carrying identifiers and facts and no personal data, for rwb-case and rwb-reporting (GAP-1727; ASM-2885). | CAP-S3-001 | BR-022 | REQ-S3-002 | Must | 3 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target the sources leave open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-S3-001 | The claim deadline, the preparation window and the warning window are read as versioned reference data per scheme and a change takes effect from its valid-from date without a release. | Every threshold read at run time | BR-022 | Must | Reference-data change test with no deployment |
| NFR-S3-002 | The guarantee claim screen responds inside the user's wait under the busiest-hour load, including the reads where case and claim data are joined. | Under 2 seconds at the 95th percentile | NFR-008, NFR-009 | Must | Performance test in SIT |
| NFR-S3-003 | The claim read, the claim update and the checklist answer are served inside the user's wait with the owning contracts in the path. | Under 2 seconds at the 95th percentile | NFR-008, NFR-009 | Must | Performance test with the contract fakes and with the real contracts |
| NFR-S3-004 | A rule evaluation at a claim step completes inside the user's wait. | Under 300 milliseconds at the 95th percentile | NFR-011 | Must | Rule timing test with the package in force |
| NFR-S3-005 | The claim preparation agent answers inside its target; after that the checklist result is used and the preparation continues. | Under 60 seconds, then the checklist result | NFR-010, NFR-024, NFR-055 | Must | Agent timeout and schema-failure drill |
| NFR-S3-006 | Every claim step records the business date and load time of the data products it read. | Every step | NFR-013 | Must | Claim record inspection |
| NFR-S3-007 | A missing, failed or late ACE batch is visible at the claim and alerts the data steward. | Visible at the claim; alert to the steward | NFR-014 | Must | Hold an ACE batch in SIT |
| NFR-S3-008 | The service holds no load window, no staging table and no catch-up job: a late ACE batch delays the claim step and raises an alert. | No load, no staging, no catch-up | NFR-015 | Must | Hold and release the batch |
| NFR-S3-009 | The service carries the claim volume of its share of the case volume; the number of claims a month is not stated in the sources. | The case volume of NFR-001 (about 23,600 open cases at go-live, 3,110 new accounts a month); the claim share is Not specified in the source documents (GAP-1734; ASM-2892) | NFR-001 | Must | Volume test at the case volume, with the claim share set first |
| NFR-S3-010 | The service is available during business hours and outside them, when the deadline timers and the notice periods run. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-S3-011 | The service inherits the ACE recovery point and recovery time, and a running claim resumes where it stopped. | The ACE recovery point objective and recovery time objective; workflow history preserved | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-S3-012 | Every claim decision is reproducible from the log, including the rule, model, agent and prompt versions and the inputs used. | Every decision reproducible | NFR-033 | Must | Re-run a sample of claims from the log |
| NFR-S3-013 | Every claim action carries the rule version applied and the role that allowed it. | Every action | NFR-034 | Must | Decision record inspection |
| NFR-S3-014 | The decision log hash chain is checked daily and a break is reported to Compliance the same day. | Daily check, same-day report | NFR-035 | Must | Chain break drill |
| NFR-S3-015 | Agent acceptance, override rate, latency and cost are measured and reported for the claim preparation agent. | Measured per agent | NFR-066 | Must | Agent measure report review |
| NFR-S3-016 | A model or agent write to the claim is logged with the model or agent version, on the same terms as a decision taken by a person. | Every write | NFR-078 | Must | Agent write inspection |
| NFR-S3-017 | Party identifiers, guarantor names and contact points are masked at rest and on every screen and agent call, by role. | Masked at rest and in use | NFR-039 | Must | Masking matrix test across roles |
| NFR-S3-018 | Each screen and each agent receives only the personal data it needs for the claim step in front of it. | Data minimisation per screen and per agent | NFR-040 | Must | Contract review per screen and per agent |
| NFR-S3-019 | Every read of a personal field is logged, and the read is refused rather than returned where the log cannot be written. | Every read | NFR-042 | Must | Access log reconciliation against reads |
| NFR-S3-020 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | NFR-045 | Must | Environment data review |
| NFR-S3-021 | Every data product and record this service holds carries a data classification that sets its handling. | Classification applied per record | NFR-047 | Must | Classification review |
| NFR-S3-022 | Recovery data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | NFR-046 | Must | Tenancy review |
| NFR-S3-023 | Staff authenticate with single sign-on and multi-factor authentication, and agents run under service identities subject to the same role checks. | Entra ID single sign-on with multi-factor; service identities | NFR-049, NFR-051 | Must | Sign-in and identity test |
| NFR-S3-024 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-S3-025 | The build blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency, and every agent output is schema checked with the checklist fallback. | Pipeline checks pass; schema check on every agent output | NFR-054, NFR-055 | Must | Pipeline run with a seeded violation; agent output with a bad schema |
| NFR-S3-026 | Screen labels, validation messages, claim messages and notice wording served with this service are available in Thai and in English. | Every label and message in Thai and English | NFR-059 | Must | Label and message review |
| NFR-S3-027 | Logs, traces and metrics are produced for the claim step, the approval and the agent, every triggered job and timer has a run book, and a failure alerts a named owner. | Every job and timer covered; alert within 15 minutes to the named owner | NFR-064, NFR-067, NFR-068 | Must | Observability review and alert drill |
| NFR-S3-028 | A call is one hop with a 2 s timeout, a breaker and a bulkhead; a failure is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; events that cannot be processed go to the dead-letter topic and are replayed. | One hop; 2 s timeout; three retries then the exception queue; dead-letter with replay | NFR-025, NFR-026 | Must | Failure injection |
| NFR-S3-029 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in schema `rwb_guarantee`. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-S3-030 | The guarantee claim screen meets the bank's accessibility standard and works on the browsers the bank supports. | WCAG 2.1 level AA; the current and previous major versions of Microsoft Edge and Google Chrome | NFR-060, NFR-061 | Must | Accessibility scan and browser test |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_guarantee`. Every table carries the record columns of the platform library (`is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by`). One table name is confirmed; the other two are named as entity groups after Architecture v5 slide 18 because no source gives them a table or a field list (GAP-1721; ASM-2879). Retention is stated by class; the periods are open (GAP-1729; ASM-2887).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `guarantee_claim` | Owned record, confirmed; one per claim per case and type | `id` (`uuid`), `case_id` (`uuid`, business key, no foreign key), `claim_type` (varchar(25), LOV-CLAIM-TYPE), `claim_deadline` (date), `claimed_amount` (numeric(18,2)), `filed_at` (date), `paid_amount` (numeric(18,2)), `status` (varchar(12), LOV-CLAIM-STATUS); DF-TRT-015 to DF-TRT-022 | [SENSITIVE_FINANCIAL] | Workbench; the TCG claim facts read through the owning contracts | Workbench record class; period open |
| Guarantee and guarantor pursuit (entity group) | Owned record, unnamed in the sources | The guarantee type and scheme code the rules read, the guaranteed amount, the party and its contact point used for the demand, the notice, its template version and its proof of delivery, the negotiation outcome and its range, the dispute and its outcome, the release and its level | [CONFIDENTIAL]; [PII] for the party fields | Workbench; the party read through the source-data contract | Workbench record class; period open |
| Subrogation position (entity group) | Owned record, unnamed in the sources | The case, the amount paid, the share the scheme holds of every later recovery, its valid-from date and the rule version that set it | [SENSITIVE_FINANCIAL] | Workbench, at payment | Workbench record class; period open |
| `outbox_event`, `processed_event`, `idempotency_key` | Platform library objects created in this schema | Library-defined | [CONFIDENTIAL] | Service template | Library policy (PLT) |

No copy of an ACE column is held and no foreign key leaves the schema (ADR-014, DP-01).

## 8.2 Data read but not owned

| Data | Read through | Views behind it | Classification of the data read |
|---|---|---|---|
| Case, party, stage, queue, tasks and timers | rwb-case contract (Temporal activity and REST) | none (case schema) | [PII], [SENSITIVE_FINANCIAL] |
| Customer, party and contact facts for the demand | rwb-source-data contract (REST) | `v_ace_contact`, `v_ace_party_product` | [PII] |
| Balances and the position that decides whether the guarantee cleared the debt | rwb-source-data contract (REST) | `v_ace_account` | [SENSITIVE_FINANCIAL] |
| Guarantee and scheme facts the rules read | rwb-source-data contract (REST) | Not specified in the source documents (GAP-1717; ASM-2875) | [SENSITIVE_FINANCIAL] |
| Freshness of each data product | rwb-source-data contract (REST) | `v_ace_batch_status` | [CONFIDENTIAL] |
| Payment, proceeds and the posting result | rwb-payment contract and the ProceedsMatched event | none (payment schema) | [SENSITIVE_FINANCIAL] |
| Notices, templates, merge fields and proof of delivery | rwb-comms contract and the NoticeDelivered event | none (comms schema) | [PII], [CONFIDENTIAL] |
| Documents and the scheme checklist evidence | rwb-document contract | none (document schema) | [CONFIDENTIAL] |
| Roles, capability areas, masking policy and the delegation table | rwb-access permission data, cached | none (access schema) | [CONFIDENTIAL] |
| Rule packages and the version in force | rwb-decision contract and events | none (decision schema) | [CONFIDENTIAL] |
| LOV-CLAIM-TYPE, LOV-CLAIM-STATUS and the other reference data | rwb-case reference-data contract | none (case schema) | [CONFIDENTIAL] |
| The appraisal behind a collateral event and its re-appraisal | rwb-valuation contract and the source-data contract | `v_ace_valuation` | [SENSITIVE_FINANCIAL] |

Counts are not stated: the FSD gives no field count for the guarantor and subrogation records, and no count is recomputed here.

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| `claimed_amount` and `paid_amount` | What the bank claims and what it was paid, in baht | [SENSITIVE_FINANCIAL] | Read access by role; no financial value in an event, a workflow input or a log |
| The subrogation share and the guaranteed amount | What the scheme holds of every later recovery | [SENSITIVE_FINANCIAL] | Shown only to the roles that own the position; not carried in GuaranteeClaimSettled |
| `claim_deadline`, `filed_at`, `claim_type` and `status` | The date the claim is won or lost, and its position | [CONFIDENTIAL] | Shown on the claim and the case; the date drives the deadline, the warning and the loss |
| Guarantor and co-borrower name and contact point | The parties the demand reaches | [PII] | Masked by role; the identification number never leaves in clear; every read logged |
| Customer identification number and name, where the claim screen shows the case party | The party the case belongs to | [PII] | Masked by role; every read logged; refused where the log cannot be written |
| The claim in the agent's prompt and output | The material the agent assembles the claim from | [CONFIDENTIAL] | No personal data in the prompt, the output or the log (NFR-040) |

The FSD marks all seven claim fields as not personal data. The party fields reach the claim screen through the case and source-data contracts and are handled as personal data by this document.

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code: the claim deadline, the preparation and warning windows, the subrogation share, the negotiation range and the release levels.
2. This service holds no copy of an ACE column and no staging table; it reads ACE data through the owning contracts only (GAP-1717; ASM-2875).
3. A link to a case or to an ACE record is a business-key column with no foreign key.
4. A personal field is not returned when the access log cannot be written.
5. Personal data is not put in an event, a workflow input or a log; GuaranteeClaimFiled and GuaranteeClaimSettled carry the case, the claim, the state and the versions, not the party and not the amounts.
6. ACE data is retained by ACE, and the archive of a Workbench record belongs to rwb-document.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-case (P3) | In and out | Temporal child workflow (GuaranteeClaimWorkflow) and REST; events | P3 | The case starts the claim and owns the parent workflow, the queues, the tasks and the timer path; this service publishes the claim events for it |
| rwb-decision (P7) | Out | Temporal child workflow and activity (approval); decision record library | P7 | The approval for a release, the rule package governance, the decision record and the hash chain |
| rwb-comms (P6) | Out and in | Temporal child workflow (guarantor notice); events listened to | P6 | The demand, its template, its merge fields and its proof of delivery; NoticeDelivered returns the date the notice period runs from |
| rwb-payment (P8) | In | Event, ProceedsMatched | P8 | The matched payment that sets the paid amount; the posting to the ledger stays with P8 |
| rwb-agent (P10) | Out | Temporal activity through the agent contract | P10 | The claim preparation agent; the connection matrix gives no S3 cell to P10 (GAP-1719; ASM-2877) |
| rwb-valuation (S1) | Out | REST or a Temporal activity through the valuation contract | S1 | The re-appraisal order behind a collateral event; the path is open (GAP-1717; ASM-2875) |
| rwb-source-data (P1) | Out | REST, one hop, 2 s timeout | P1 | The party, balance and freshness facts. The connection matrix gives no S3 cell to P1, so the path is carried as open (GAP-1717; ASM-2875) |
| rwb-document (P5) | Out | REST through the document contract | P5 | The scheme checklist evidence and the claim submission pack |
| rwb-access (P4) | In | Cached permission data through the guard library, not a call on the hot path | P4 | Roles, the capability area Treatment and offer, the masking policy and the delegation table |
| rwb-integration (P2) | Out | REST or a file run through the integration contract | P2 | The TCG claim channel when INT-29 becomes available; the matrix gives no S3 cell to P2 (GAP-1718; ASM-2876) |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | The guarantee claim screen (SCR-17) and the claim read (GAP-1730; ASM-2888) |
| Kafka topic `rwb.guarantee.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by case | This service | GuaranteeClaimFiled, GuaranteeClaimSettled; consumers rwb-case and rwb-reporting. Neither event has an EV number in the catalogue (GAP-1727; ASM-2885) |
| rwb-reporting (P9) | Out | Events and the decision record | P9 | Claims filed inside the deadline, the claim position and the override measures; read from the decision log, not from a separate count |
| Thai Credit Guarantee Corporation (INT-29) | Out | Not available today; entered and filed by the guarantee officer | The bank integration owner with the scheme | The claim submission channel; the reference is recorded on the claim (GAP-1718; ASM-2876) |
| ACE common audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5 (ADR-018); no extract leaves this service |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| How do the guarantee, party and scheme facts reach this service, and what does the freshness response look like, given that the connection matrix gives S3 no cell to rwb-source-data? | Solution architect with P1 | Every claim step reads a fact and a date; without the path the boundary test has nothing to fail on (GAP-1717; ASM-2875) |
| Does the claim submission stay a person's entry for E4, or does it become an rwb-integration interface when INT-29 arrives? | Solution architect with the integration lead | The 100 percent inside-the-deadline measure rests on this answer, and so does the claim event (GAP-1718; ASM-2876) |
| Does the claim preparation agent run on rwb-agent from this service, and what is recorded when the checklist result is used instead? | Solution architect with P10 | The agent story cannot be built against a call the matrix does not show (GAP-1719; ASM-2877) |
| Which operation serves the claim read that SCR-17 needs, and on which path? | Solution architect | The architecture gives the service a GET and the contract publishes none (GAP-1726; ASM-2884) |

# 10. Release slicing proposal

The service is wave 3: it is created with Epic 4 (release 28 February 2027 (tentative)). Each slice is a list of capabilities, not stories. Every date is copied unchanged from the release plan and marked (tentative) (ASM-2896).

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library and the decision-record library, the Temporal workflow kit with the approval child, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product. The service wave (3) and the business epic wave of E4 (3) are the same, so no wave conflict is raised (ASM-2895).

## 10.2 Before wave 3 — nothing this service must publish first

No earlier epic consumes a claim contract: the E3 stories that depend on an E4 feature depend on FEAT-VAL-01 and FEAT-VAL-06, which belong to rwb-valuation (BRD Q-016, ASM-2584), and no E3 story names a guarantee claim. The claim contract therefore lands inside wave 3 with its own stories, and no fake is published ahead of the service.

## 10.3 Wave 3 — Epic 4 (release 28 February 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 3.1 The claim record, its contract and its read path | CAP-S3-001, CAP-S3-011 | Nothing else can be claimed until the claim exists with its data date, and the boundary test must fail the build on a direct ACE read from the first story |
| 3.2 The deadline clock and the warning | CAP-S3-002 | The product exists because the deadline is missed; the timer, the warning and the recorded loss are the first behaviours to demonstrate |
| 3.3 Preparation and the scheme checklist | CAP-S3-003 | A claim assembled against the checklist is the difference between a filing and a rejection |
| 3.4 Verification and submission | CAP-S3-004 | The officer's verification is the control, and the submission reference is what makes the claim traceable |
| 3.5 Tracked to payment | CAP-S3-005 | Query, part payment, rejection and resubmission are where the claim spends its life |
| 3.6 Subrogation and closure | CAP-S3-006, CAP-S3-009 | A paid claim that leaves its share unrecorded is money lost after the recovery |
| 3.7 Guarantor notices and negotiation | CAP-S3-007, CAP-S3-008 | The guarantor is a party to the debt and must be reached on the same terms as the borrower |
| 3.8 Pursuit, dispute and release | CAP-S3-012 | A disputed guarantee must stop contact, and a release must be approved by the role that owns it |
| 3.9 The insurance claim on a collateral event | CAP-S3-010 | The insurance recovery and the new value both change the next route decision |
| 3.10 Claim eligibility before submission | CAP-S3-013 | Ineligible claims are not filed; this slice is Should and may slip within the wave without holding the release |

Rationale: the wave-3 slice is the smallest set that delivers the Epic 4 outcome for this route, and each slice is independently demonstrable. CAP-S3-013 is Should and may slip; every other capability is Must and is needed for the release.

## 10.4 Later increments

| Increment | What unlocks it |
|---|---|
| The guarantee rule set as a governed package | Phase 2 of the Drools design, with the 32 rules, their version label and their owner in rwb-decision (GAP-1723; ASM-2881) |
| The TCG claim channel as an interface | INT-29 becoming available, then a path through rwb-integration, which the connection matrix does not yet give (GAP-1718; ASM-2876) |
| The guarantor through the partner gateway | The partner portal live at the edge, with the guarantor as a partner user type (S9 rwb-partner) |
| The release of a guarantor and of a TCG guarantee at full authority | DL18 and BRD Q-001 answering the levels, then the release read from the delegation table (GAP-1725; ASM-2883) |
| The guarantor and subrogation record set | The data architect's table list, added with the S3 DB story (GAP-1721; ASM-2879) |
| Claim measures at full width | The rwb-reporting read model, fed by the decision record and the two claim events (ADR-018) |
| The claim read and the screen at full width | The read operation added to the contract and the composite route agreed (GAP-1726; GAP-1730; ASM-2888) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion, the named rule or the confirmed v5 constraint that proves it, so a criterion is never invented where the source has one. Because every criterion of the FSD is a placeholder and its exception rows are identical across the eight features, each criterion below is written from the rules it tests and keeps the FSD identifier as its evidence (GAP-1733; ASM-2891). Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-S3-001 | FR-S3-002, FR-S3-003, FR-S3-004, NFR-S3-002 | a case with no claim and a published claim contract | a claim is opened with its type, deadline and amount claimed | one claim record exists linked to the case by business key with no foreign key, carrying the type from LOV-CLAIM-TYPE and the status from LOV-CLAIM-STATUS; the claim shows both the workflow state and the published status and the two agree; a second open of the same type returns 409 and creates nothing | AC-S3-006-01; API-S3-001; DF-TRT-015 to DF-TRT-022 |
| AC-S3-002 | FR-S3-001, NFR-S3-025 | a branch that reads a `recovery.v_ace_*` view directly and a schema constraint that references a table outside `rwb_guarantee` | the pipeline and the boundary test run | the build fails naming the view read and the cross-schema constraint; the conformance step passes with no ACE object in this schema | Arch v5 slides 37 and 45; GAP-1717; ASM-2875 |
| AC-S3-003 | FR-S3-008, FR-S3-009, NFR-S3-001 | a TCG guarantee with a scheme code and a deadline for that scheme in reference data | the claim is opened and the workflow restarts mid-wait | the deadline timer starts from the date the default conditions are met, survives the restart as a durable timer, and no Quartz table or job is used; a change to the deadline in reference data applies from its valid-from date with no release | AC-S3-001-01; R-GUA-01; Temporal slide 19; ADR-016 |
| AC-S3-004 | FR-S3-010, FR-S3-011 | a claim inside its preparation window and a scheme checklist with one item missing, then supplied | the preparation runs twice | the claim enters preparation with the days remaining and the window applied; the first run raises the retrieval requests and holds the claim; the second presents the claim to the guarantee officer for approval | AC-S3-001-01; R-GUA-04, R-GUA-07, R-GUA-08, R-GUA-10 |
| AC-S3-005 | FR-S3-012, NFR-S3-005 | the agent does not answer inside 60 seconds, and a second run answers with a schema the check rejects | the preparation runs in both cases | the checklist result is used and the preparation continues; the agent, model and prompt versions are recorded with the attempt, and the claim states which of the two assembled it | AC-S3-001-01; R-GUA-04; NFR-010, NFR-055; GAP-1719; ASM-2877 |
| AC-S3-006 | FR-S3-013, FR-S3-014 | a claim inside its warning window, and a second claim whose deadline passes before submission | the timer fires on both | the first escalates to the guarantee officer and the Head of Litigation with the days remaining; the second records the lost claim with its reason and amount, reports the breach and refuses a step that would reverse the loss | AC-S3-003-01; R-GUA-05, R-GUA-09, R-GUA-11 |
| AC-S3-007 | FR-S3-015 | a claim whose checklist is complete, and a second claim the officer sends back | both are verified | the first records the approval with its role, time and rule version and moves on; the second returns to preparation with the officer's reason and no approval on the record | AC-S3-001-01; R-GUA-12, R-GUA-13 |
| AC-S3-008 | FR-S3-016, FR-S3-032, NFR-S3-028 | an approved claim and a TCG channel that is not interfaced | the submission is recorded | the claim carries its reference, its date and the channel used, moves to CLAIM_SUBMITTED, and GuaranteeClaimFiled is in the outbox keyed by the case and carries no personal data; a failed publish is retried and then dead-lettered and replayed | AC-S3-002-01; R-GUA-12; INT-29; GAP-1718; ASM-2876 |
| AC-S3-009 | FR-S3-017, FR-S3-018 | a claim that fails one scheme condition, and a guarantee whose conditions are not met at takeover but are met at the later review | each is tested | the failing claim is not submitted and records the failed condition with the rule version; the second records that no claim arises, holds the guarantee, and starts the deadline timer when the conditions are met | AC-S3-002-01; REQ-S3-007; R-GUA-02, R-GUA-03 |
| AC-S3-010 | FR-S3-019 | a submitted claim on which the scheme raises a query, and a second query that receives no answer inside its window | the query events arrive | the first holds the claim and raises a task to the guarantee officer, and resubmits on the answer; the second records the lapse and treats the claim as rejected | AC-S3-003-01; R-GUA-14, R-GUA-15, R-GUA-16 |
| AC-S3-011 | FR-S3-020 | a rejection with a curable reason inside the deadline, and a rejection with a reason that is not curable | each is handled | the first reworks the claim and resubmits it; the second closes the guarantee, returns the full balance to the route decision and records the reason and the rule version | AC-S3-003-01; R-GUA-17, R-GUA-18, R-GUA-19 |
| AC-S3-012 | FR-S3-021 | a submitted claim and a part payment on it, with the deadline still open | the payment is matched and posted | the claim records the amount paid and the shortfall on the case, and the balance claim is submitted while the deadline allows it | AC-S3-002-01; R-GUA-20, R-GUA-21; EV-25 |
| AC-S3-013 | FR-S3-022 | a claim whose paid amount equals the guaranteed amount | the payment is recorded | the subrogation position is set with the share the scheme holds of every later recovery, its valid-from date and the rule version applied | AC-S3-004-01; R-GUA-22, R-GUA-23, R-GUA-24 |
| AC-S3-014 | FR-S3-023, FR-S3-032 | a claim that clears the balance in full, and a claim that leaves a residual | both are closed | the first closes the guarantee and the case and GuaranteeClaimSettled is in the outbox keyed by the case; the second returns the residual to the route decision at D6 and the case moves without a second action | AC-S3-007-01; R-GUA-25, R-GUA-26, R-GUA-27 |
| AC-S3-015 | FR-S3-024, NFR-S3-026 | a case with two personal guarantors and a co-borrower, and an approved template in rwb-comms | the notice falls due | the demand is issued to all three from the approved template through the notice path, and its period is timed from proof of delivery, not from posting | AC-S3-005-01; R-GUA-06; EV-13, EV-14, EV-15 |
| AC-S3-016 | FR-S3-025, FR-S3-026 | a guarantor who pays inside the range, and a guarantor who refuses or does not reply by the expiry | each answer is recorded | the first books the treatment, reduces the balance and closes the guarantee; the second records the refusal against the party and returns the case to the route decision | AC-S3-006-01; R-GUA-28, R-GUA-29 |
| AC-S3-017 | FR-S3-027 | a case owner with a negotiation inside the range and a submission with a required field empty | both are attempted | the negotiation records the outcome, the range and the rule version against the party; the empty field is refused with MSG-GEN-001 and nothing changes | AC-S3-006-01; VR-S3-006-1 |
| AC-S3-018 | FR-S3-028 | a guarantor who disputes the guarantee, and a dispute that is then not upheld, then a second dispute that is upheld | each outcome arrives | the first raises X1, stops contact on the disputed item and holds the pursuit; the second resumes the pursuit from the notice; the third releases the guarantor and returns the case to the route decision | AC-S3-006-01; R-GUA-30, R-GUA-31, R-GUA-32 |
| AC-S3-019 | FR-S3-029, NFR-S3-013 | a release of a guarantor and a release of a TCG guarantee, with a delegation table in force | each release is requested | the request goes to the level the delegation table names at run time, and the release records the level applied, the approving role and the rule version; no level is read from code | Temporal slide 19; GAP-1725; ASM-2883 |
| AC-S3-020 | FR-S3-030 | a collateral recorded as stolen, and a collateral written off | each is recorded on the case | an insurance claim is opened with its type from LOV-CLAIM-TYPE, and a re-appraisal order is raised so that the new value is in force before the next route decision | AC-S3-008-01; BR-025; FEAT-VAL-01 |
| AC-S3-021 | FR-S3-031, NFR-S3-006, NFR-S3-007 | one data product is STALE at the business date and a second cannot be read at all | a claim step is requested | the stale product is shown with its date and MSG-P1-001 and the step records the business date and load time it used; with the second product unreadable no claim step starts, and the steward is alerted | VR-S3-001-1; NFR-013, NFR-014 |
| AC-S3-022 | FR-S3-006, FR-S3-007, NFR-S3-014 | a user without the capability area, signed in with single sign-on, and a decision-log store that rejects every write | each acts | the first is refused with MSG-P4-002 and nothing changes on the claim or the case; the second changes nothing, shows MSG-P7-003 and raises an incident, and the daily chain check reports the gap the same day | AC-EXC-S3-001-01, AC-EXC-S3-001-02; NFR-035 |

## 11.2 Requirement trace summary

| BR | Program requirement | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|---|
| BR-022 | REQ-S3-001 | CAP-S3-001, CAP-S3-002, CAP-S3-003, CAP-S3-004, CAP-S3-013 | FR-S3-001, FR-S3-002, FR-S3-004, FR-S3-006, FR-S3-008, FR-S3-009, FR-S3-010, FR-S3-011, FR-S3-012, FR-S3-013, FR-S3-014, FR-S3-015, FR-S3-016, FR-S3-017, FR-S3-018 | NFR-S3-001, NFR-S3-002, NFR-S3-003, NFR-S3-004, NFR-S3-005, NFR-S3-006, NFR-S3-007, NFR-S3-008, NFR-S3-009, NFR-S3-010, NFR-S3-011, NFR-S3-012, NFR-S3-015, NFR-S3-016, NFR-S3-020, NFR-S3-024, NFR-S3-025, NFR-S3-027, NFR-S3-030 | AC-S3-001, AC-S3-002, AC-S3-003, AC-S3-004, AC-S3-005, AC-S3-006, AC-S3-007, AC-S3-008, AC-S3-009, AC-S3-021 |
| BR-022 | REQ-S3-002 | CAP-S3-001, CAP-S3-005, CAP-S3-010, CAP-S3-011 | FR-S3-003, FR-S3-005, FR-S3-007, FR-S3-019, FR-S3-021, FR-S3-030, FR-S3-031, FR-S3-032 | NFR-S3-006, NFR-S3-007, NFR-S3-008, NFR-S3-014, NFR-S3-021, NFR-S3-022, NFR-S3-028, NFR-S3-029 | AC-S3-010, AC-S3-012, AC-S3-020, AC-S3-021, AC-S3-022 |
| BR-022, BR-023 | REQ-S3-006 | CAP-S3-005 | FR-S3-020 | NFR-S3-012, NFR-S3-013 | AC-S3-011 |
| BR-023 | REQ-S3-003 | CAP-S3-006, CAP-S3-009 | FR-S3-022, FR-S3-023 | NFR-S3-012, NFR-S3-013 | AC-S3-013, AC-S3-014 |
| BR-024 | REQ-S3-004 | CAP-S3-007 | FR-S3-024 | NFR-S3-017, NFR-S3-018, NFR-S3-019, NFR-S3-026 | AC-S3-015 |
| BR-024 | REQ-S3-005 | CAP-S3-008, CAP-S3-012 | FR-S3-025, FR-S3-026, FR-S3-027, FR-S3-028 | NFR-S3-017, NFR-S3-018, NFR-S3-019 | AC-S3-016, AC-S3-017, AC-S3-018 |
| BR-024 | REQ-S3-006 | CAP-S3-012 | FR-S3-029 | NFR-S3-013, NFR-S3-023, NFR-S3-026 | AC-S3-019 |
| BR-022 | REQ-S3-007 | CAP-S3-013 | FR-S3-017, FR-S3-018 | NFR-S3-001 | AC-S3-009 |
| BR-025 | Not specified in the source documents (GAP-1724; ASM-2882) | CAP-S3-010 | FR-S3-030 | NFR-S3-006, NFR-S3-021 | AC-S3-020 |

BR coverage: 7 of the 7 program requirements of this module (REQ-S3-001 to REQ-S3-007) and 4 of the 4 BRD requirements of E4 that name this service (BR-022 to BR-025) are covered by at least one functional requirement. No requirement of this module is left without a functional requirement, and no functional requirement lacks a source requirement (ASM-2897). BR-025 has no program requirement of its own, and its trace through REQ-S3-002 is an assumption recorded as GAP-1724 (ASM-2882).

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Boundary and conformance test output in system test | FR-S3-001, NFR-S3-025 | Developer with the security administrator |
| Contract test against the case, comms, payment, source-data and agent contracts and their fakes | FR-S3-001 to FR-S3-005, FR-S3-012, FR-S3-024, FR-S3-031 | Developer with P1, P3, P6, P8 and P10 |
| Deadline drill: a guarantee found, the timer, the warning, a restart, and a claim lost | FR-S3-008 to FR-S3-014, NFR-S3-001, NFR-S3-011 | QA team with the guarantee officer |
| Preparation and checklist drill with a missing item, a supplied item and an officer send-back | FR-S3-010, FR-S3-011, FR-S3-015 | Guarantee officer with the QA team |
| Agent timeout and schema-failure drill on claim preparation | FR-S3-012, NFR-S3-005, NFR-S3-015, NFR-S3-016 | QA team with the model risk officer |
| Submission and claim event test, including a manual reference entry and a dead-letter replay | FR-S3-016, FR-S3-032, NFR-S3-028 | QA team with the integration lead |
| Tracking drill: query, part payment, balance claim, rejection, resubmission and residual | FR-S3-019 to FR-S3-023 | Guarantee officer with the QA team |
| Notice and negotiation test with two guarantors, a co-borrower, a refusal and a dispute | FR-S3-024 to FR-S3-028, NFR-S3-026 | Case owner with P6 and the QA team |
| Release approval matrix test across the delegation levels | FR-S3-029, NFR-S3-013 | Product head with the QA team |
| Insurance claim and re-appraisal test | FR-S3-030 | Hardship and vulnerability specialist with S1 |
| Decision reproducibility and agent measure review | FR-S3-007, NFR-S3-012, NFR-S3-015, NFR-S3-016 | Internal audit with the model risk officer |
| Masking matrix, access log reconciliation and classification review | NFR-S3-017 to NFR-S3-022 | Compliance and PDPA officer |
| Performance and volume test at the stated volume | NFR-S3-002, NFR-S3-003, NFR-S3-009 | QA team |

# 12. Open questions

The FSD holds no open-question register of its own, so the questions below are the product-level ones this document needs to close, with the BRD questions they sit beside. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-S3-01 | How do the case, party, guarantee, balance and freshness facts reach this service, given that the connection matrix gives S3 no cell to rwb-source-data and only that service reads the views? | Solution architect with P1 | Before wave 3 system test | CAP-S3-001, CAP-S3-011 | GAP-1717; ASM-2875; Arch v5 slides 13, 37 and 45 |
| OQ-S3-02 | Which channel files the claim to the TCG, and does INT-29 stay a person's entry for E4 with the reference recorded on the claim? | Solution architect with the integration lead | Before wave 3 system test | CAP-S3-004 | GAP-1718; ASM-2876; TSD S3 T5.1 |
| OQ-S3-03 | Does the claim preparation agent run on rwb-agent from this service, and what is recorded when the checklist result is used instead? | Solution architect with P10 | Before wave 3 system test | CAP-S3-003 | GAP-1719; ASM-2877; DP-20 |
| OQ-S3-04 | Which state model governs the claim — the five values of LOV-CLAIM-STATUS or the seventeen workflow states over 32 rules — and are R-GUA-23 and R-GUA-24, and R-GUA-05 and R-GUA-09, one rule or two? | Business analyst, S3 with P7 | Before wave 3 system test | CAP-S3-001, CAP-S3-005, CAP-S3-006 | GAP-1720, GAP-1723; ASM-2878, ASM-2881 |
| OQ-S3-05 | Which record holds the guarantee, the guarantor and the subrogation share, given that only `guarantee_claim` is confirmed? | Data architect | Before the S3 DB story | CAP-S3-006, CAP-S3-012 | GAP-1721; ASM-2879 |
| OQ-S3-06 | Which rules and which field set govern the guarantor notice, and who owns the template it is sent from? | Business analyst, S3 with P6 | Before wave 3 system test | CAP-S3-007 | GAP-1722; ASM-2880 |
| OQ-S3-07 | Is the insurance claim a product requirement of this service under its own REQ-S3 identifier, or is it served by REQ-S3-002? | Product Owner | Before wave 3 release | CAP-S3-010 | GAP-1724; ASM-2882; BR-025 |
| OQ-S3-08 | What is each release level for a guarantor and for a TCG guarantee, and who substitutes for each approver (DL18)? | Risk with the product heads | Before wave 3 release | CAP-S3-012 | GAP-1725; ASM-2883; GAP-1464; ASM-2569 |
| OQ-S3-09 | What is the TCG quota and the claim deadline for each scheme, and what are the preparation and warning windows? | Guarantee officer | Before wave 3 system test | CAP-S3-002, CAP-S3-013 | GAP-1728; ASM-2886; GAP-1476; ASM-2581 |
| OQ-S3-10 | Which operation serves the claim read, and on which path does the gateway call it? | Solution architect | Before the S3 contract story closes | CAP-S3-001, CAP-S3-004 | GAP-1726; ASM-2884 |
| OQ-S3-11 | Do GuaranteeClaimFiled and GuaranteeClaimSettled get EV numbers and catalogue rows, and does the payload carry the claim amount? | Solution architect | Before wave 3 system test | CAP-S3-001, CAP-S3-009 | GAP-1727; ASM-2885; Arch v5 slides 18 and 43 |
| OQ-S3-12 | What classification and what retention period apply to the claim, the guarantor record and the subrogation position (DL26)? | Compliance and PDPA officer | Before wave 3 release | CAP-S3-001, CAP-S3-006 | GAP-1729; ASM-2887; GAP-1475; ASM-2580 |
| OQ-S3-13 | Which service owns SCR-17 and where does its gateway route sit? | Solution architect | Before wave 3 release | CAP-S3-003, CAP-S3-004 | GAP-1730; ASM-2888; DP-19 |
| OQ-S3-14 | Who owns the wording of MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001, and who approves the Thai and English versions? | Business analyst, S3 | Before wave 3 release | All messages | GAP-1731; ASM-2889 |
| OQ-S3-15 | Is the guarantee claim route R4, or does the numbering change when the litigation route is settled? | Business analyst, S3 with P7 | Before wave 3 system test | CAP-S3-009 | GAP-1732; ASM-2890 |
| OQ-S3-16 | What claim volume a month, and how many guarantors and notices a case produces, does the product carry? | Business lead | Before wave 3 release | NFR-S3-009 | GAP-1734; ASM-2892 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (ASM-2894).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 5.10 (S3 requirements, REQ-S3-001 to REQ-S3-007), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan), 9 (open decisions incl. DL18, DL26, DL43), 10.1 and 10.2 (the service epic RWB-SVC-S3, schema, wave and topic), 10.3 (waves and releases) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 4.4 (delivery model under D-RCV-60), 5 (stakeholders and roles), 6 (current state), 7.1 and 7.3 (E4 scope, services and wave), 8.2 (BR-022 to BR-025), 10 (KPI-001, KPI-011, KPI-012), 11.1 to 11.4 (ASM, CON, DEP, RISK), 12 (Q-001, Q-012, Q-013, Q-016), 13 (governance) |
| Recovery Workbench FSD S3 Guarantees and guarantors v3 | Document control, Existing capability check, A1 (context, scope, dependencies, feature overview, background, preconditions), A2.1 to A2.8 (functional decomposition with rules, field catalog, roles and acceptance criteria), Requirements served, Screens, Appendix A and B |
| Recovery Workbench TSD S3 Guarantees and guarantors v2 | T3.0 to T3.3 (record columns, `guarantee_claim`, DF-TRT-015 to DF-TRT-022, lists, relationship), T4 (32 rules over 17 states), T5.1 (INT-29) and T5.3 (events), T6.1 (capability area Treatment and offer), T-A.1 and T-A.2 (API-S3-001, API-S3-002) |
| Recovery Workbench Architecture v5 | Slides 3 (the eight routes), 4 (19 modules), 9 to 13 (call types, timeouts, retry, the connection matrix), 14 to 20 (service contracts, S3 on slide 18), 27 (rule governance), 30 (19 schemas), 32 (bank scheduler at the edges), 37 (what changes and why), 41 (service catalogue), 42 and 43 (event catalogue), 44 (job map), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Slide 13 (workflow per stage), slide 15 (rule governance and versioning), slide 16 (decision record), slide 19 (S3 guarantee claims: the seven steps, the clock, the 32 rules, the approvers, the release authorities, the point of no return) and its open decisions list |
| Recovery Workbench Business Rules and Routing Logic v4 | R-GUA-01 to R-GUA-32 with their from-states, events, conditions and to-states; R-LIT-01 (route numbering) |
| Recovery Workbench Microservice Ownership Map v1 | Services (S3 row: schema, REST base, topic, queue), Endpoints (POST and PATCH), Workflows (GuaranteeClaimWorkflow), Tables (`guarantee_claim`, `dp_guarantee_claim`), Events (no S3 row), Rulings (`dp_guarantee_claim`, `valuation_ext`) |
| Recovery Workbench API Specification v4 | Paths `/cases/{caseId}/guarantee-claims` and `/guarantee-claims/{claimId}`; schemas GuaranteeClaim, GuaranteeClaimRequest and GuaranteeClaimUpdate; capability area and error responses |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R5 (target structure, DP table, wave map), R8 (outputs), R9 (gaps and assumptions) |
