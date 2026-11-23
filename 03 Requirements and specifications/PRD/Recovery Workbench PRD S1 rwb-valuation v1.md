SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD S1 rwb-valuation v1
description: Product requirements for the Recovery Workbench valuation and route service (S1 rwb-valuation) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S1 Valuation and route v3.md
service: S1 rwb-valuation
epic: RWB-SVC-S1
wave: 3
decision: D-RCV-60
---

# Recovery Workbench PRD S1 rwb-valuation v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD S1 rwb-valuation |
| Document ID | S1-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | S1 rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 (Epic 4, route decision, wave 3) |
| Schema | `rwb_valuation` |
| REST base | `/api/recovery/valuation/v1` |
| Topic | `rwb.valuation.events.v1` |
| Temporal task queue | `rwb-valuation` |
| Java package | `th.co.scb.ace.workbench.recovery.valuation` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Business analyst, S1 |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), ADR-010, ADR-013 to ADR-023 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epics 3 to 8 v1; FSD S1 Valuation and route v3; Architecture v5; Temporal and Drools Design v1 |
| Upstream requirement IDs | REQ-S1-001 to REQ-S1-008; BR-016, BR-017, BR-018, BR-019, BR-020, BR-021; NFR-001, NFR-008, NFR-009, NFR-010, NFR-011, NFR-012, NFR-013, NFR-014, NFR-015, NFR-020, NFR-021, NFR-022, NFR-023, NFR-025, NFR-026, NFR-027, NFR-033, NFR-034, NFR-035, NFR-039, NFR-040, NFR-042, NFR-045, NFR-046, NFR-047, NFR-049, NFR-051, NFR-052, NFR-053, NFR-054, NFR-055, NFR-059, NFR-060, NFR-061, NFR-064, NFR-066, NFR-067, NFR-068, NFR-078 |
| Upstream acceptance criteria | AC-S1-001-01 to AC-S1-012-01 (main success flow, one per feature); AC-EXC-S1-001-01 to AC-EXC-S1-012-01 (role without the right); AC-EXC-S1-001-02 to AC-EXC-S1-012-02 (decision cannot be recorded). The FSD defines no alternate flow and no system background event for any of the twelve features |
| Generated IDs | CAP-S1-001 to CAP-S1-013; FR-S1-001 to FR-S1-028; NFR-S1-001 to NFR-S1-029; AC-S1-001 to AC-S1-020; JRN-S1-01 to JRN-S1-05; ROL-S1-01 to ROL-S1-12; OQ-S1-01 to OQ-S1-15 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD S1 Valuation and route v3 (15 November 2026) and Business Requirements Epics 3 to 8 v1, realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD S1 Valuation and route v3. Its requirement IDs, feature IDs and acceptance criterion IDs are carried unchanged; the microservice realignment changes the read path, the owner of three capabilities and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Valuation field catalog re-pointed to `v_ace_valuation` plus `recovery.valuation_ext`; SVAF appraisal and COLLINS scores read from ACE. Everything else unchanged from v2 |
| 1 and 2 | Not specified in the source documents (GAP-1695; ASM-2843) | Earlier versions of the FSD. Their dates and change notes are not in the sources read, and are carried as an open item rather than reconstructed |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, journey and open-question IDs are new; the FSD requirement IDs (REQ-S1-001 to REQ-S1-008), feature IDs (FEAT-VAL-01 to FEAT-VAL-12), validation rule IDs (VR-S1-001-1 to VR-S1-012-1), business rule IDs (BR-S1-001 to BR-S1-012), acceptance criteria IDs (AC-S1-001-01 to AC-S1-012-01 and their exception rows), message IDs (MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001), list ID (LOV-APPRAISAL) and screen ID (SCR-13) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the program requirements REQ-S1-001 to REQ-S1-008 and of the non-functional requirements |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-016 to BR-021, the E4 scope, the measures, the risks and the open questions |
| Recovery Workbench Functional Specifications by Module v6, FSD S1 Valuation and route v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, only rwb-source-data reads ACE, Kafka, Temporal, no data lake, edge and gateway |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: RouteDecisionWorkflow on `rwb-valuation`, the approval and agent children, the rule kit and the 60 s agent limit |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every operation, event, workflow, table and job named here |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-valuation (S1) is the recovery module's route decision. It turns "valuation and rules propose, an approver signs off" into a product: an appraisal that is current, sourced and questioned before it is used; the expected return, the payoff and the settlement range for a case with the versions they were computed under; a recommendation that names its option, its reasons, its confidence and the alternatives it rejected; an approval taken inside the delegation of authority or at the committee above it; a hold with a review date where no route fits; a re-decision when the facts move; and a route that starts its flow and its clocks in the same step as its approval.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-valuation | One deployable with its own API and worker, schema `rwb_valuation`, login, topic `rwb.valuation.events.v1`, task queue `rwb-valuation` and lifecycle | The route decision becomes one owned product with its own release, instead of a screen inside a single deployable |
| The appraisal as a governed record | The appraisal value, its date, its appraiser, its acceptance and its band, held once and linked to the collateral by business key | A route decided on a value nobody accepted is a route that cannot be defended |
| The recommendation as a product behaviour | The route agent proposes a route with its reasons, its confidence and the alternatives, and falls back to the rule result inside 60 seconds | The approver sees why, not only what |
| Route timers as workflow timers | The route's clocks live in RouteDecisionWorkflow as durable timers | The case is held by the workflow while it waits for the appraisal and the approval, rather than by a table polled by a scheduler |
| The decision as a reproducible record | Routes considered, values and returns used, recommendation, approval level and approver, rule and model versions | Every route decision answers an audit question without a person reconstructing it |
| The route decision as an event | RouteDecided on `rwb.valuation.events.v1`, consumed by rwb-case | The case moves on the approval in the same transaction, not on a poll |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its ingestion of SVAF appraisals and COLLINS scores and its backups | REUSE | ACE team |
| The read-only view contract and the freshness of every data product | REUSE, elsewhere | P1 rwb-source-data (this service reads it by contract) |
| The appraisal acceptance row in `valuation_ext` | REUSE, elsewhere | P1 rwb-source-data (GAP-1678; ASM-2826) |
| Case record, CMMN state, queues, tasks, allocation and the case timers | REUSE | P3 rwb-case (RouteDecisionWorkflow is its child workflow) |
| Approval workflow, decision record, hash chain and rule package registry | REUSE | P7 rwb-decision |
| Roles, capability areas, masking policy and the delegation table | REUSE | P4 rwb-access |
| Route agent runtime, model endpoint, guardrails and run record | REUSE | P10 rwb-agent |
| Interface configuration and outbound delivery of the valuation order | REUSE | P2 rwb-integration (GAP-1683; ASM-2831) |
| Collateral and asset record, floor price and the monthly re-appraisal | REUSE, elsewhere | S5 rwb-asset |
| Screens and the composite route that serves them | REUSE | Platform edge, gateway-bff (RWB-PLT-EDGE) |
| Quartz scheduler and its shared tables | REPLACED | Temporal workflow kit (PLT); ADR-016, DP-10 (GAP-1684; ASM-2832) |
| Embedded Drools with the Excel route decision tables evaluated in the monolith | MOVED | P7 for governance and versioning; evaluation stays local in this service (ADR-017, DP-04) |
| COLLINS model development and the affordability calculation | OUT OF SCOPE | Data and AI; the ACE restructure calculator |
| Booking in the core bank and credit approval in the lending system | OUT OF SCOPE | The officer and the core bank; this service records the result |
| Collections before day 90 and decisions D1 to D4 | OUT OF SCOPE | EFS and the ACE collection module |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014; slides 37 and 45).
2. The service writes only schema `rwb_valuation`; no cross-schema join and no foreign key into `public` (ADR-014, DP-01).
3. A route service reaches a shared capability through Temporal, never REST; this service's one synchronous call is REST to rwb-source-data (slide 13, ADR-020).
4. REST is one hop from gateway-bff with a 2 s timeout, an Idempotency-Key on every POST and RFC 9457 problem details; a GET is retried once with jitter (ADR-020; slide 10; slide 11).
5. Events are CloudEvents 1.0 on Kafka with an outbox and an inbox, retry at 1 minute, 10 minutes and 1 hour and then a dead-letter topic; topic `rwb.valuation.events.v1`, key `caseId` (ADR-015, DP-09, DP-14; slides 9 and 11).
6. Temporal namespace `rwb-recovery`, task queue `rwb-valuation`; RouteDecisionWorkflow is a child of the case workflow; Schedules and durable timers replace Quartz (ADR-016, DP-10).
7. Rules are versioned data evaluated in process by the embedded Drools kit; authoring, testing and promotion are governed in rwb-decision (ADR-017, DP-04).
8. There is no data lake: route measures and reporting read the decision record and the events into rwb-reporting (ADR-018, DP-17).
9. Personal data stays out of events, workflow inputs and logs; masking is by role, using the permission data cached from rwb-access, and each service authorises the object itself (slide 10; NFR-039, NFR-040).
10. The bank scheduler owns only the cross-system edges and signals the business date; it never enters the case journey (slide 32).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-S1-01 | Case owner | A recommendation with its reasons, a value they can accept, and an approval inside their own limit | JRN-S1-01, JRN-S1-03, JRN-S1-04 |
| ROL-S1-02 | Sale officer | The accepted value on the case, and the appraisal evidence behind it | JRN-S1-02, JRN-S1-03 |
| ROL-S1-03 | Product head (Mortgage, HP, SSME) | Route decisions inside the delegation for the product, and the exceptions named | JRN-S1-03 |
| ROL-S1-04 | Credit approval committee member | A pack that states the value, the return, the payoff, the recommendation and the reasons | JRN-S1-03 |
| ROL-S1-05 | Team manager | A held case with a review date, and route decisions that do not sit unapproved | JRN-S1-04 |
| ROL-S1-06 | Center of excellence analyst | Every recommendation accepted, overridden or rejected per route, with the rule version applied | JRN-S1-05 |
| ROL-S1-07 | Risk and model risk officer | The agent's acceptance, override, latency and cost per agent, and its fallback evidence | JRN-S1-05 |
| ROL-S1-08 | Compliance and PDPA officer | Masking by role, an access log that cannot be skipped, and a classification on every record | JRN-S1-05 |
| ROL-S1-09 | Internal audit | A route decision that is reproducible from the log with its rule, model and prompt versions | JRN-S1-05 |
| ROL-S1-10 | Platform administrator | A workflow that reports a breach, an alert with a named owner, and a replay path | JRN-S1-04 |
| ROL-S1-11 | Developer | A typed contract to build against, a fake for every dependency, and a build that fails on a direct ACE read | JRN-S1-05 |
| ROL-S1-12 | Panel valuer (external role) | A valuation order with the asset, the type and the date it is needed | JRN-S1-02 |

Non-human actors: the case workflow that starts RouteDecisionWorkflow; the approval workflow on rwb-decision; the route agent on rwb-agent; the outbox relay; the consumers of RouteDecided. The valuer is reached through the partner gateway at the edge and never by a direct call from this service.

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. The route is chosen on officer judgment written up in an account plan; there is no recommendation that states its reasons or its alternatives.
2. The appraisal value, the appraisal date and the appraiser are read from the ACE collateral and valuation data, with the acceptance held in a Workbench extension row that has no single stated writer.
3. The expected return and the payoff are worked out ad hoc for the case in front of the officer.
4. The route's clocks are set on the shared scheduler, and a route that is approved but not started is a case with no clock.
5. A change in the value, the band or the classification after the decision does not reopen it.

Consequence: two officers reach two different routes on the same facts, and neither can show why.

## 4.2 Target state (this product)

### JRN-S1-01 The route decision from the daily case (daily, case owner)

1. The case reaches route decision D6 in CaseWorkflow, or it is reopened; rwb-case starts RouteDecisionWorkflow on this service.
2. The workflow reads the appraisal age against the limit in force and orders a valuation where the appraisal is stale; the order leaves through rwb-integration.
3. It reads the collateral and appraisal facts through the rwb-source-data contract, with the business date and load time of each data product.
4. It asks for the expected return of each route, the payoff and the settlement range, with the rule and model versions in force.
5. It runs the route agent; an answer inside 60 seconds is used, and otherwise the rule result is used and the case still routes.
6. The case owner sees the recommendation with its reasons, its confidence and the alternatives considered, and accepts the value the decision runs on.

### JRN-S1-02 Appraisal ordered, received, questioned and accepted (on trigger, sale officer)

1. The appraisal arrives from SVAF through ACE ingestion and is read through the source-data contract with its value, date and appraiser.
2. The value is compared with the market value and the previous accepted value; a gap beyond the thresholds in force raises an outlier flag before the value can be accepted.
3. The accepting role accepts the value with a reason where a flag is open; the acceptance records who, when and the band the value falls in.
4. The value now fixes the band the route decision runs on, and the decision record states which value and which band it used.

### JRN-S1-03 Recommendation and approval (daily, case owner and committee)

1. The recommendation names the route, the reasons, the confidence and the alternatives.
2. Where the amount is inside the case owner's delegation, the approval request goes to that limit and the level applied and the approver are recorded.
3. Where it is above the limit, the approval goes to the credit approval committee with the value, the return, the payoff, the settlement range, the recommendation and the reasons.
4. A rejection or a return records its reason and leaves the case where it was; an approval moves it.
5. A decision that cannot be recorded changes nothing and raises an incident.

### JRN-S1-04 Hold, re-decision and the clock (as the facts move, case owner and team manager)

1. Where no route fits yet, the case owner holds the case with a review date and a reason; the hold is visible on the case.
2. A change in the exposure band, the valuation or the classification, or a payment or a deviation, reopens the decision; the earlier decision and its evidence stay.
3. Reopening a closed decision needs a written rule, a reason and an approver.
4. On approval the route flow and its timers start in the same step, and RouteDecided reaches rwb-case; a timer that passes raises its task and its alert.

### JRN-S1-05 Evidence and measures read later (audit, center of excellence and risk)

1. An auditor reads one route decision: the routes considered, the values and returns used, the recommendation and its reasons, the approval with its level and approver, and the rule and model versions.
2. The center of excellence reads the acceptance and override rate per route and product, with the coded reason of every override, from the decision record and not from a separate count.
3. The model risk officer reads the agent's acceptance, override, latency and cost per agent, and the runs where the rule result was used instead.
4. A developer builds against the published contract and its fake; a build that reads an ACE view or an ACE table directly fails.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-S1-001 | Valuation record and appraisal receipt | The value the route runs on is one governed record, linked to the collateral, with its date and its appraiser | BR-017 | Must | 3 | FEAT-VAL-02 (A2.2) |
| CAP-S1-002 | Appraisal age watch and the valuation order | A stale appraisal is ordered without a person asking, and the order is visible on the case | BR-016 | Must | 3 | FEAT-VAL-01 (A2.1) |
| CAP-S1-003 | Outlier flag before acceptance | A value that jumps against the market and the last value is questioned before it is used | BR-017 | Must | 3 | FEAT-VAL-03 (A2.3) |
| CAP-S1-004 | Appraisal acceptance and the value band | The accepting role fixes the value and the band the decision runs on, and the case shows who and when | BR-017 | Must | 3 | FEAT-VAL-04 (A2.4) |
| CAP-S1-005 | Expected return by route with its model version | Every route carries its expected return, and the decision states the version it was computed under | BR-018 | Must | 3 | FEAT-VAL-05 (A2.5) |
| CAP-S1-006 | Payoff and settlement range with the floor | The payoff and the range are calculated from current balances by rule, with the floor applied | BR-018 | Must | 3 | FEAT-VAL-06 (A2.6) |
| CAP-S1-007 | Route recommendation with reasons, confidence and alternatives | The approver sees why a route is proposed and what was rejected, including the fallback where the agent is slow | BR-019 | Must | 3 | FEAT-VAL-07 (A2.7) |
| CAP-S1-008 | Approval inside the delegation | The approval goes to the limit that applies, and the level and the approver are on the record | BR-020 | Must | 3 | FEAT-VAL-08 (A2.8) |
| CAP-S1-009 | Committee approval above the limit | A route beyond the case owner's limit reaches the committee with its evidence pack | BR-020 | Must | 3 | FEAT-VAL-09 (A2.9) |
| CAP-S1-010 | Hold with a review date | A case with no right route is held on purpose, with a date it is looked at again | BR-020 | Must | 3 | FEAT-VAL-10 (A2.10) |
| CAP-S1-011 | Re-decision on new information | A value, a band, a payment or a deviation reopens the decision instead of leaving a stale one in force | BR-020 | Should | 3 | FEAT-VAL-11 (A2.11) |
| CAP-S1-012 | Route start and timers in the same step | An approved route starts its flow and its clocks at once, and the case moves on the event | BR-021 | Must | 3 | FEAT-VAL-12 (A2.12) |
| CAP-S1-013 | Freshness and data date at the decision | Every valuation and every decision states how old its data is, and a stale product is seen rather than assumed | BR-017, BR-018 | Must | 3 | A2.1 to A2.12 (VR-S1-001-1 to VR-S1-012-1); A2.2 |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Direct read of the ACE collateral, valuation and score views | Not carried | rwb-source-data's contract (GAP-1677; ASM-2825) |
| Writing the appraisal acceptance into `recovery.valuation_ext` | Not carried | P1 rwb-source-data, read and written by contract (GAP-1678; ASM-2826) |
| Quartz scheduling of the route timers | Replaced | Durable timers in RouteDecisionWorkflow through the workflow kit (GAP-1684; ASM-2832) |
| Direct call to SVAF for a valuation order | Not carried | The rwb-integration contract (GAP-1683; ASM-2831) |
| The asset record, the floor price and the monthly re-appraisal | Reused, elsewhere | S5 rwb-asset (this service supplies the accepted appraisal) |
| COLLINS model development and the affordability calculation | Out of scope | Data and AI; the ACE restructure calculator |
| The route rules as Excel decision tables in the monolith | Moved | Governance in P7 rwb-decision; evaluation local, route package in Phase 2 (GAP-1687; ASM-2835) |

# 6. Functional requirements

Every requirement is specific and testable. The FSD requirement column keeps the trace to the source. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-S1-001 | The service SHALL obtain every collateral, appraisal, balance and score fact it needs through the rwb-source-data contract. A read of a `recovery.v_ace_*` view, a read of an ACE table, and a constraint in schema `rwb_valuation` that references a table outside it, SHALL fail the build and the boundary test. | CAP-S1-001 | BR-017 | REQ-S1-002 | Must | 3 |
| FR-S1-002 | The service SHALL link each appraisal it holds to the ACE asset, and through it to the collateral, by a business-key column of type `varchar(255)` with no foreign key, and SHALL hold one record per ACE appraisal key. | CAP-S1-001 | BR-017 | REQ-S1-002 | Must | 3 |
| FR-S1-003 | The service SHALL hold the appraisal record with the appraisal key, the asset key, the appraisal number, the appraisal type from LOV-APPRAISAL, the appraised value in baht, the forced sale value in baht, the appraisal date, the valuer, the outlier flag, the acceptance state, who accepted it, when it was accepted and the band it fixes. | CAP-S1-001 | BR-017 | REQ-S1-002 | Must | 3 |
| FR-S1-004 | The service SHALL return the valuation of a case with the business date and the load time of each data product behind it and with its status LOADED or STALE, and SHALL show a stale product with the date it belongs to. | CAP-S1-013 | BR-017 | REQ-S1-002 | Must | 3 |
| FR-S1-005 | The service SHALL compare the appraisal age in days at the business date with the limit in force and SHALL place a valuation order where the appraisal is older than the limit, without a person asking for it. | CAP-S1-002 | BR-016 | REQ-S1-001 | Must | 3 |
| FR-S1-006 | The service SHALL raise the valuation order through the rwb-integration contract and SHALL record the order with its date, the rule version and the limit applied; a failed order SHALL be retried on a schedule and SHALL then move to an exception queue with a task for a named owner. | CAP-S1-002 | BR-016 | REQ-S1-001 | Must | 3 |
| FR-S1-007 | The service SHALL test the appraisal age when the route decision starts, when the decision is reopened and when an appraisal arrives for the case, and SHALL run no scheduled job of its own. | CAP-S1-002 | BR-016 | REQ-S1-001 | Must | 3 |
| FR-S1-008 | The service SHALL flag a new value as an outlier where it differs from the market value or from the previous accepted value by more than the thresholds in force, and SHALL record the gap, both values and the rule version with the flag. | CAP-S1-003 | BR-017 | REQ-S1-002 | Must | 3 |
| FR-S1-009 | The service SHALL hold the acceptance of a value while an outlier flag on it is open, SHALL accept the value where the accepting role gives a reason, and SHALL record that reason with the acceptance. | CAP-S1-003 | BR-017 | REQ-S1-002 | Must | 3 |
| FR-S1-010 | The service SHALL record an accepted value with the accepting role, the time and the band the value falls in, where the band is read from reference data and fixed for the decision that follows. | CAP-S1-004 | BR-017 | REQ-S1-002 | Must | 3 |
| FR-S1-011 | The service SHALL refuse the acceptance, the approval, the hold and the re-decision to a role without the capability area, with MSG-P4-002, and SHALL change nothing on a refusal. | CAP-S1-004 | BR-017 | REQ-S1-002 | Must | 3 |
| FR-S1-012 | The service SHALL serve the expected return of each of the eight recovery routes for the case at the decision, with the model version and the score version it was computed under. | CAP-S1-005 | BR-018 | REQ-S1-003 | Must | 3 |
| FR-S1-013 | The service SHALL refresh the rules and rates in force when the rule package in force changes, and SHALL record on each decision the package and rule version that was evaluated. | CAP-S1-005 | BR-018 | REQ-S1-003 | Must | 3 |
| FR-S1-014 | The service SHALL calculate the payoff from the current balances of the case and the settlement range from the rules with the floor applied, and SHALL record the rule version with each calculated value. | CAP-S1-006 | BR-018 | REQ-S1-004 | Must | 3 |
| FR-S1-015 | The service SHALL read every limit, threshold, range and floor from versioned reference data, and a change SHALL take effect from its valid-from date without a code release. | CAP-S1-006 | BR-018 | REQ-S1-004 | Must | 3 |
| FR-S1-016 | The service SHALL return the recommended route with the option, the reasons, the confidence and the alternatives considered, and SHALL show that recommendation with the return, the payoff and the value it rests on. | CAP-S1-007 | BR-019 | REQ-S1-005 | Must | 3 |
| FR-S1-017 | The service SHALL run the route agent through the rwb-agent contract, SHALL wait at most 60 seconds for its answer, and where the answer arrives late or fails its schema check SHALL use the rule result and still present a route. | CAP-S1-007 | BR-019 | REQ-S1-005 | Must | 3 |
| FR-S1-018 | The service SHALL record the agent, model and prompt versions with an agent answer, and SHALL record an override of the recommendation with a coded reason and the overriding role. | CAP-S1-007 | BR-019 | REQ-S1-005 | Must | 3 |
| FR-S1-019 | The service SHALL request the approval at the delegation limit that applies to the decision, the product and the amount, read from rwb-access at run time, and SHALL record the level applied and the approver. | CAP-S1-008 | BR-020 | REQ-S1-006 | Must | 3 |
| FR-S1-020 | The service SHALL record an approval, a rejection or a return with its reason and the rule version, SHALL move the case only on an approval, and where the decision cannot be recorded SHALL change nothing, raise an incident and show MSG-P7-003. | CAP-S1-008 | BR-020 | REQ-S1-006 | Must | 3 |
| FR-S1-021 | The service SHALL raise the approval to the credit approval committee where the amount is above the case owner's limit, with the value, the return, the payoff, the settlement range, the recommendation and its reasons, and SHALL record the committee's decision with the level applied. | CAP-S1-009 | BR-020 | REQ-S1-006 | Must | 3 |
| FR-S1-022 | The service SHALL hold a case where no route fits, with a reason and a review date, SHALL show the hold and its date on the case, and SHALL return the case to the decision on the review date. | CAP-S1-010 | BR-020 | REQ-S1-006 | Must | 3 |
| FR-S1-023 | The service SHALL reopen the route decision where the exposure band, the valuation or the classification changes after the decision, or where a payment or a deviation changes the picture, and SHALL keep the earlier decision and its evidence. | CAP-S1-011 | BR-020 | REQ-S1-008 | Should | 3 |
| FR-S1-024 | The service SHALL reopen a closed route decision only through a written rule, a reason and an approver, and SHALL record all three with the new decision. | CAP-S1-011 | BR-020 | REQ-S1-008 | Should | 3 |
| FR-S1-025 | The service SHALL start the chosen route flow and set its timers in the same step as the approval, and SHALL publish RouteDecided on `rwb.valuation.events.v1` keyed by the case, so that rwb-case moves the case without a second action. | CAP-S1-012 | BR-021 | REQ-S1-007 | Must | 3 |
| FR-S1-026 | The service SHALL set the route timers as durable timers inside RouteDecisionWorkflow through the workflow kit, and SHALL report a timer breach on the case timer path that rwb-case owns; no Quartz table, connection or job SHALL be used. | CAP-S1-012 | BR-021 | REQ-S1-007 | Must | 3 |
| FR-S1-027 | The service SHALL start no route decision on a data product whose freshness cannot be read, SHALL show the stale product with its date and MSG-P1-001, and SHALL record the business date and load time it decided on. | CAP-S1-013 | BR-018 | REQ-S1-003 | Must | 3 |
| FR-S1-028 | The service SHALL hold a route decision record that carries the routes considered, the values and returns used, the recommendation with its reasons, confidence and alternatives, the approval with its level and approver, and the rule and model versions; the physical field list is open (GAP-1694; ASM-2842). | CAP-S1-007 | BR-019 | REQ-S1-005 | Must | 3 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-S1-001 | The route decision screen responds inside the user's wait under the busiest-hour load, including the reads where case and ACE data are joined. | Under 2 seconds at the 95th percentile | NFR-008, NFR-009 | Must | Performance test in SIT |
| NFR-S1-002 | The valuation, the return by route and the payoff are served inside the user's wait with the source-data contract in the path. | Under 2 seconds at the 95th percentile | NFR-008, NFR-009 | Must | Performance test in SIT with the contract stub and with the real contract |
| NFR-S1-003 | A rule evaluation at the route decision completes inside the user's wait. | Under 300 milliseconds at the 95th percentile | NFR-011 | Must | Rule timing test with the package in force |
| NFR-S1-004 | The route agent answers inside its target; after that the rule result is used and the case still routes. | Under 60 seconds, then the rule result | NFR-010, NFR-024 | Must | Agent timeout drill |
| NFR-S1-005 | Every valuation, recommendation and decision states the business date and load time of the data products it read. | Every decision | NFR-013 | Must | Decision record inspection |
| NFR-S1-006 | A missing, failed or late ACE batch is visible at the decision and alerts the data steward. | Visible at the decision; alert to the steward | NFR-014 | Must | Hold an ACE batch in SIT |
| NFR-S1-007 | The service holds no load window, no staging table and no catch-up job: a late ACE batch delays the decision and raises an alert. | No load, no staging, no catch-up | NFR-015 | Must | Hold and release the batch |
| NFR-S1-008 | The service carries the stated volume of route decisions and valuations. | 28,119 accounts in the active inventory; 3,110 new accounts a month; about 23,600 open cases at go-live and 26,500 at the end of 2027; about 21 requests a second in the busiest hour | NFR-001 | Must | Volume test at the stated volume |
| NFR-S1-009 | The service is available during business hours and outside them, when the approval timers run. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-S1-010 | The service inherits the ACE recovery point and recovery time, and a running route decision resumes where it stopped. | The ACE recovery point objective and recovery time objective; workflow history preserved | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-S1-011 | Every route decision is reproducible from the log, including the rule, model, agent and prompt versions and the inputs used. | Every decision reproducible | NFR-033 | Must | Re-run a sample of decisions from the log |
| NFR-S1-012 | Every action carries the rule version applied and the approver who allowed it. | Every action | NFR-034 | Must | Decision record inspection |
| NFR-S1-013 | The decision log hash chain is checked daily and a break is reported to Compliance the same day. | Daily check, same-day report | NFR-035 | Must | Chain break drill |
| NFR-S1-014 | Agent acceptance, override rate, latency and cost are measured and reported per agent. | Measured per agent | NFR-066 | Must | Agent measure report review |
| NFR-S1-015 | A model or agent write is logged with the model or agent version, on the same terms as a decision taken by a person. | Every write | NFR-078 | Must | Agent write inspection |
| NFR-S1-016 | Party identifiers are masked at rest and on every screen and agent call, by role. | Masked at rest and in use | NFR-039 | Must | Masking matrix test across roles |
| NFR-S1-017 | Each screen and each agent receives only the personal data it needs. | Data minimisation per screen and per agent | NFR-040 | Must | Contract review per screen and per agent |
| NFR-S1-018 | Every read of a personal field is logged, and the read is refused rather than returned where the log cannot be written. | Every read | NFR-042 | Must | Access log reconciliation against reads |
| NFR-S1-019 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | NFR-045 | Must | Environment data review |
| NFR-S1-020 | Every data product and record this service holds carries a data classification that sets its handling. | Classification applied per record | NFR-047 | Must | Classification review |
| NFR-S1-021 | Recovery data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | NFR-046 | Must | Tenancy review |
| NFR-S1-022 | Staff authenticate with single sign-on and multi-factor authentication, and agents run under service identities subject to the same role checks. | Entra ID single sign-on with multi-factor; service identities | NFR-049, NFR-051 | Must | Sign-in and identity test |
| NFR-S1-023 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-S1-024 | The build blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency, and every agent output is schema checked with the rule fallback. | Pipeline checks pass; schema check on every agent output | NFR-054, NFR-055 | Must | Pipeline run with a seeded violation; agent output with a bad schema |
| NFR-S1-025 | Screen labels, validation messages and error messages served with this service's operations are available in Thai and in English. | Every label and message in Thai and English | NFR-059 | Must | Label and message review |
| NFR-S1-026 | Logs, traces and metrics are produced for the route decision, the approval and the agent, every triggered job has a run book, and a failure alerts a named owner. | Every job covered; alert within 15 minutes to the named owner | NFR-064, NFR-067, NFR-068 | Must | Observability review and alert drill |
| NFR-S1-027 | A call is one hop with a 2 s timeout; a failure is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; events that cannot be processed go to the dead-letter topic and are replayed. | One hop; 2 s timeout; three retries then the exception queue; dead-letter with replay | NFR-025, NFR-026 | Must | Failure injection |
| NFR-S1-028 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in schema `rwb_valuation`. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-S1-029 | The route decision screen meets the bank's accessibility standard and works on the browsers the bank supports. | WCAG 2.1 level AA; the current and previous major versions of Microsoft Edge and Google Chrome | NFR-060, NFR-061 | Must | Accessibility scan and browser test |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_valuation`. Every table carries the record columns of the platform library. The Ownership Map fixes no table name for this service, so the three entity groups are named as Architecture v5 slide 18 names them and the physical names are written with the DB story (GAP-1679; ASM-2827). Retention is stated by class; the periods are open (GAP-1692; ASM-2840).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `valuations` (entity group) | Owned record, one per ACE appraisal key | `valuation_key` (`varchar(255)`), `asset_key` (`varchar(255)`), appraisal number, appraisal type (LOV-APPRAISAL), appraised value, forced sale value, appraisal date, valuer, outlier flag and its gap, acceptance state, accepted by role, accepted at, band; the valuation order, its date, its reference and the limit applied | [SENSITIVE_FINANCIAL] | ACE appraisal data read through the source-data contract; the acceptance is a Workbench decision | Workbench record class; period open |
| `route_decision` (entity group, "D6 route decision") | Owned record, one per decision per case | Case number, business date, the routes considered, the value and its band, the return, the payoff and the settlement range per route, the recommended route, the reasons, the confidence, the alternatives, the approval level, the approver role, the decision, the decided at, the rule version and the model version | [SENSITIVE_FINANCIAL] | Workbench decision; the position it rests on is read through contracts | Workbench record class; period open |
| `route_agent_output` (entity group) | Owned record, one per agent run on a case | Agent run reference, the recommended route, the reasons, the confidence, the alternatives, the model version, the prompt version, the run time, the outcome (accepted, overridden, rejected) and the coded override reason | [CONFIDENTIAL] | rwb-agent through the agent contract | Workbench record class; period open |
| `outbox_event`, `processed_event`, `idempotency_key` | Platform library objects created in this schema | Library-defined | [CONFIDENTIAL] | Service template | Library policy (PLT; ASM-0074) |

The field lists of the decision record and the agent output are open (GAP-1694; ASM-2842). No copy of an ACE column is held and no foreign key leaves the schema.

## 8.2 Data read but not owned

| Data | Read through | Views behind it | Classification of the data read |
|---|---|---|---|
| Collateral and appraisal facts | rwb-source-data contract (REST) | `v_ace_collateral`, `v_ace_collateral_detail`, `v_ace_valuation` | [SENSITIVE_FINANCIAL] |
| Balances and payment position for the payoff | rwb-source-data contract (REST) | `v_ace_account`, `v_ace_payment` | [SENSITIVE_FINANCIAL] |
| COLLINS scores for the return by route | rwb-source-data contract (REST) | `v_ace_score` | [CONFIDENTIAL] |
| Freshness of each data product | rwb-source-data contract (REST) | `v_ace_batch_status` | [CONFIDENTIAL] |
| Case, party, stage, queue and timers | rwb-case contract (Temporal activity and REST) | none (case schema) | [PII], [SENSITIVE_FINANCIAL] |
| Roles, capability areas, masking policy and the delegation table | rwb-access permission data, cached | none (access schema) | [CONFIDENTIAL] |
| Rule packages and the version in force | rwb-decision contract and events | none (decision schema) | [CONFIDENTIAL] |
| LOV-APPRAISAL and other reference data | rwb-case reference-data contract | none (case schema) | [CONFIDENTIAL] |
| The appraisal acceptance row in `valuation_ext` | rwb-source-data contract (REST) | none (extension table) | [CONFIDENTIAL] |

Counts are not stated: the FSD gives no field count for this module, and no count is recomputed here.

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| Appraised value and forced sale value | The value the route runs on, in baht | [SENSITIVE_FINANCIAL] | Read access by role; no financial value in an event, a workflow input or a log |
| Payoff amount and settlement range | What the bank expects to recover | [SENSITIVE_FINANCIAL] | Served on the decision screen only; not carried in RouteDecided |
| Appraisal date, appraisal type, appraisal number | The identity and the age of the value | [CONFIDENTIAL] | Shown on the decision; the date drives the staleness check |
| Valuer reference (`valuer_partner_id`) | The partner who made the appraisal | [CONFIDENTIAL] | Read by role; the valuer is an external role, reached through the partner gateway |
| Customer identification number and name, where the decision screen shows the case party | The party the case belongs to | [PII] | Masked by role; the identification number never leaves in clear; every read logged |
| Contact value, where the decision screen shows the last contact | How the customer was last reached | [PII] | Masked by default, full only where a masking row for the role allows it |
| Agent output and its prompt | The recommendation and the material it was given | [CONFIDENTIAL] | No personal data in the prompt, the output or the log (NFR-040) |

The FSD marks all eight valuation catalog fields as not personal data. The party fields reach the screen through the case contract and are handled as personal data by this document.

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code: the appraisal age limit, the outlier thresholds, the settlement range, the floor, the approval levels and the route numbers.
2. This service holds no copy of an ACE column and no staging table; it reads ACE data through the source-data contract only (GAP-1677; ASM-2825).
3. A link to an ACE record is a business-key column of type `varchar(255)` with no foreign key.
4. A personal field is not returned when the access log cannot be written.
5. Personal data is not put in an event, a workflow input or a log; RouteDecided carries the case, the route, the decision and the versions, not the values.
6. ACE data is retained by ACE, and the archive of a Workbench record belongs to rwb-document.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-source-data (P1) | Out and in | REST, one hop, 2 s timeout, GET retried once with jitter | P1 | The only path to collateral, appraisal, balance, score and freshness facts; this service reads no view and no ACE table (GAP-1677; ASM-2825) |
| ACE database, tables behind the 30 views | Not read | None | ACE team | Read only through the P1 contract. No direct `public` read and no DML from this service |
| rwb-case (P3) | In and out | Temporal child workflow (RouteDecisionWorkflow) and REST; events listened to | P3 | The case starts the decision and owns the parent workflow, the queues, the tasks and the timer path; this service publishes RouteDecided for it |
| rwb-decision (P7) | Out and in | Temporal activity and child workflow (ApprovalWorkflow); events listened to | P7 | Approval routing on the delegation, rule package governance, the decision record and the hash chain |
| rwb-access (P4) | In | Cached permission data through the guard library, not a call on the hot path | P4 | Roles, capability areas, masking policy and the delegation table |
| rwb-agent (P10) | Out | Temporal, child workflow and activity | P10 | The route agent under its contract, 60 s then the rule result (DP-20; C dependency on the P10 contract story) |
| rwb-integration (P2) | Out | REST or an activity per the integration contract | P2 | The valuation order to SVAF. The slide 13 matrix shows no S1 cell to P2, so the path is carried as open (GAP-1683; ASM-2831) |
| rwb-asset (S5) | In | REST | This service | The accepted appraisal for the floor price and the monthly re-appraisal (GAP-1682; ASM-2830) |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | The route decision screen (SCR-13), the valuation read and the approval commands; the composite route joins this service's answer with rwb-case |
| Kafka topic `rwb.valuation.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by case | This service | RouteDecided; consumer rwb-case. The event has no EV number in the catalogue yet (GAP-1680; ASM-2828) |
| rwb-reporting (P9) | Out | Events and the decision record | P9 | Acceptance and override per route and product, and the route measures; produced from the decision log, not from a separate count |
| ACE common audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |
| Partner gateway (valuer) | Out | Through the edge, not by direct call | Platform edge with S9 | The valuation order reaches the panel valuer; the path is the integration service's |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5 (ADR-018); no extract leaves this service |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Which path does the valuation order take, given that the slide 13 matrix shows no S1 cell to rwb-integration and the FSD names SVAF directly? | Solution architect with the integration lead | Decides whether the order is a P2 interface or an activity on another service's queue (GAP-1683; ASM-2831) |
| Which of the two route commands is published: `POST /cases/{id}/route-proposals` on slide 18 or `POST /cases/{caseId}/route` in the API specification? | Solution architect | Fixes the gateway route and the screen's client before the screen is built (GAP-1681; ASM-2829) |
| Does rwb-asset keep the two asset valuation paths, or does it read the appraisal from this service? | Solution architect with the S5 owner | Two writers of one appraisal record would leave the floor price on a value the case never accepted (GAP-1682; ASM-2830) |

# 10. Release slicing proposal

The service is wave 3: it is created with Epic 4 (release 28 February 2027 (tentative)). Each slice is a list of capabilities, not stories.

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library, the Temporal workflow kit with the approval and agent children, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product. The service wave (3) and the business epic wave of E4 (3) are the same, so no wave conflict is raised (ASM-2846).

## 10.2 Before wave 3 — the contract Epic 3 consumes (release 31 January 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 0.1 Published contract and fake | CAP-S1-001, CAP-S1-006 | Epic 3 needs an early valuation and the payoff figure for a deed in lieu one release before this service exists, so the contract, its fake and its schema are published first and E3 builds against them (GAP-1689; ASM-2837) |

Rationale: contract-first is the only way to keep the E3 release date while the service that owns the capability is created in wave 3; the fake is what E3 tests against until wave 3 lands.

## 10.3 Wave 3 — Epic 4 (release 28 February 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 3.1 Read path and valuation record | CAP-S1-001, CAP-S1-013 | Nothing else can be decided until the valuation exists with its data date, and the boundary test must fail the build on a direct ACE read from the first story |
| 3.2 Appraisal watch and order | CAP-S1-002 | A route decided on a stale value is a wrong route, and the order has to leave the service without a person |
| 3.3 Outlier and acceptance | CAP-S1-003, CAP-S1-004 | The value is the largest single input to the route; it must be questioned and accepted before it is used |
| 3.4 Return, payoff and range | CAP-S1-005, CAP-S1-006 | A route recommended without its return and its floor is an opinion |
| 3.5 Recommendation and agent | CAP-S1-007 | The approver must see why, and the case must still route when the agent is slow |
| 3.6 Approval and committee | CAP-S1-008, CAP-S1-009 | The decision has to be taken by the role that owns it, inside the delegation or at the committee |
| 3.7 Hold and re-decision | CAP-S1-010, CAP-S1-011 | A case with no right route needs a home, and a decision must not outlive its facts |
| 3.8 Route start and timers | CAP-S1-012 | An approved route that does not start is a case with no clock |

Rationale: the wave-3 slice is the smallest set that delivers the Epic 4 outcome, and each slice is independently demonstrable. CAP-S1-011 is Should and may slip within the wave without holding the release.

## 10.4 Later increments

| Increment | What unlocks it |
|---|---|
| The route rule package as a governed package | Phase 2 of the Drools design, with the rule set, its version label and its owner in rwb-decision (GAP-1687; ASM-2835) |
| A printed route number on the recommendation | The route numbering agreed between the sources, then held as reference data (GAP-1688; ASM-2836) |
| Route start for the litigation, guarantee, asset, debt sale and write-off routes | E5 and E6 releases, each consuming the same RouteDecided event |
| The panel valuer through the partner portal | The partner portal live at the edge, first needed for valuers at Epic 4 (Non-functional specification v3 section 4) |
| Route measures and agent measures at full width | The rwb-reporting read model, fed by the decision record and the events (ADR-018) |
| The S1 table set in the Ownership Map and the physical schema | The data architect's table list, added with the DB story (GAP-1679; ASM-2827) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-S1-001 | FR-S1-001, FR-S1-002, FR-S1-003, NFR-S1-008 | the source-data contract is published with its fake and an asset carries two appraisals | the valuations of the case are read and one appraisal is accepted | one record exists per ACE appraisal key, linked by the asset key with no foreign key; the appraised value, forced sale value, type, date and valuer match the contract; the accepted record carries who accepted it and when | AC-S1-002-01 |
| AC-S1-002 | FR-S1-001, NFR-S1-024 | a branch that reads `recovery.v_ace_valuation` directly and a schema constraint that references an ACE table | the pipeline and the boundary test run | the build fails naming the view read and the cross-schema constraint; the conformance step passes with no ACE object in this schema | Arch v5 slides 37 and 45; GAP-1677; ASM-2825 |
| AC-S1-003 | FR-S1-005, FR-S1-006 | an appraisal older than the limit in force at the business date | the route decision starts | a valuation order is raised through the integration contract and recorded with its date, its rule version and the limit applied; the case owner sees the order without asking for it | AC-S1-001-01 |
| AC-S1-004 | FR-S1-006, NFR-S1-027 | the integration contract rejects every order | the appraisal-age check runs | the order is retried on the schedule and then appears in the exception queue with a task for a named owner; nothing else on the case changes | AC-EXC-S1-001-02; GAP-1683; ASM-2831 |
| AC-S1-005 | FR-S1-008, FR-S1-009 | a new value 30 percent above the previous accepted value and the same as the market value | the value is read and the accepting role tries to accept it | the outlier flag is set with both values, the gap and the rule version; the acceptance is held until a reason is given, and the reason is recorded | AC-S1-003-01 |
| AC-S1-006 | FR-S1-010, FR-S1-012 | an accepted value in the second band and the return in force for all eight routes | the recommendation is requested | the decision carries the accepted value, the band it falls in and the return of each route with its model and score version | AC-S1-004-01, AC-S1-005-01 |
| AC-S1-007 | FR-S1-011, NFR-S1-022 | a user without the capability area, signed in with single sign-on | they try to accept a value and to approve a route | both actions are refused with MSG-P4-002 and nothing changes on the case or the valuation | AC-EXC-S1-004-01, AC-EXC-S1-008-01 |
| AC-S1-008 | FR-S1-013 | the rule package in force is promoted to a new version while a decision is open | the next evaluation runs | the decision records the new package and rule version, and the earlier decision keeps the version it was taken under | AC-S1-005-01; Arch v5 slide 43 (RulePackageInForce); DP-04 |
| AC-S1-009 | FR-S1-014, FR-S1-015 | balances of the case, a settlement range and a floor in force for the product | the payoff and the range are requested | both are calculated from the current balances by rule with the floor applied and the rule version recorded; changing the floor in reference data changes the answer from its valid-from date without a release | AC-S1-006-01 |
| AC-S1-010 | FR-S1-016, NFR-S1-003 | the routes score within a millisecond band of each other | the recommendation is requested | the reasons, the confidence and the alternatives considered are present for the recommended route; each rule evaluation completes inside 300 milliseconds at the 95th percentile | AC-S1-007-01; NFR-011 |
| AC-S1-011 | FR-S1-017, FR-S1-018, NFR-S1-004 | the route agent does not answer inside 60 seconds, and a second run answers with a schema the check rejects | the recommendation is requested in both cases | the rule result is used and a route is still presented; the agent, model and prompt versions are recorded with the attempt; the fallback is visible on the decision | AC-S1-007-01; NFR-010, NFR-024, NFR-055 |
| AC-S1-012 | FR-S1-019, FR-S1-020, NFR-S1-012 | an amount inside the case owner's delegation and a delegation table in force | the approval is requested and granted | the request goes to the level the table names, and the decision records the level applied, the approver and the rule version | AC-S1-008-01 |
| AC-S1-013 | FR-S1-021 | an amount above the case owner's limit | the approval is requested | the request reaches the credit approval committee with the value, the return, the payoff, the settlement range, the recommendation and its reasons, and the committee decision is recorded with the level applied | AC-S1-009-01 |
| AC-S1-014 | FR-S1-022 | no route fits the case at the decision | the case owner holds the case with a review date | the hold and its date are on the case; the case returns to the decision on the review date | AC-S1-010-01 |
| AC-S1-015 | FR-S1-023 | a route decision taken at one exposure band, and the band changes the next day | the case is read | the decision reopens, and the earlier decision and its evidence are still readable | AC-S1-011-01 |
| AC-S1-016 | FR-S1-024 | a closed route decision | a reopen is attempted with no written rule, then with a rule, a reason and an approver | the first attempt is refused and nothing changes; the second is recorded with all three | AC-S1-011-01; R-UNI-50; GAP-1688; ASM-2836 |
| AC-S1-017 | FR-S1-025, FR-S1-026, NFR-S1-028 | an approved route and a running RouteDecisionWorkflow | the approval is granted | the route flow and its timers start in the same step, RouteDecided is in the outbox keyed by the case, and rwb-case moves the case; a rollback redeploys the previous tag and the migration stays in `rwb_valuation` | AC-S1-012-01; Arch v5 slides 18 and 43; GAP-1680; ASM-2828 |
| AC-S1-018 | FR-S1-020, NFR-S1-013 | the decision record store rejects every write | the approval is granted | nothing changes on the case, MSG-P7-003 is shown and an incident is raised; the daily hash-chain check reports the gap the same day | AC-EXC-S1-008-02, AC-EXC-S1-009-02; NFR-035 |
| AC-S1-019 | FR-S1-004, FR-S1-027, NFR-S1-005, NFR-S1-006 | one data product is STALE at the business date and a second cannot be read at all | the decision is requested | the stale product is shown with its date and MSG-P1-001 and the decision records the business date and load time it used; with the second product unreadable no decision starts | AC-EXC-S1-001-01; VR-S1-001-1; NFR-013, NFR-014 |
| AC-S1-020 | FR-S1-028, NFR-S1-011, NFR-S1-014, NFR-S1-015 | a decision taken with an agent answer and one taken with the rule fallback | an auditor reads both from the log and the model risk officer reads the agent measures | each decision shows the routes considered, the values and returns used, the recommendation with its reasons, confidence and alternatives, the approval with its level and approver, and the rule and model versions; the agent measures show acceptance, override, latency and cost with the run where the rule result was used | AC-S1-007-01; NFR-033, NFR-066, NFR-078; GAP-1694; ASM-2842 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| REQ-S1-001 (BR-016) | CAP-S1-002 | FR-S1-005, FR-S1-006, FR-S1-007 | NFR-S1-006, NFR-S1-007, NFR-S1-027 | AC-S1-003, AC-S1-004, AC-S1-019 |
| REQ-S1-002 (BR-017) | CAP-S1-001, CAP-S1-003, CAP-S1-004 | FR-S1-001, FR-S1-002, FR-S1-003, FR-S1-004, FR-S1-008, FR-S1-009, FR-S1-010, FR-S1-011 | NFR-S1-008, NFR-S1-016, NFR-S1-017, NFR-S1-018, NFR-S1-020, NFR-S1-024 | AC-S1-001, AC-S1-002, AC-S1-005, AC-S1-007, AC-S1-019 |
| REQ-S1-003 (BR-018) | CAP-S1-005, CAP-S1-013 | FR-S1-012, FR-S1-013, FR-S1-027 | NFR-S1-002, NFR-S1-003, NFR-S1-005 | AC-S1-006, AC-S1-008, AC-S1-019 |
| REQ-S1-004 (BR-018) | CAP-S1-006 | FR-S1-014, FR-S1-015 | NFR-S1-001, NFR-S1-002 | AC-S1-009 |
| REQ-S1-005 (BR-019) | CAP-S1-007 | FR-S1-016, FR-S1-017, FR-S1-018, FR-S1-028 | NFR-S1-003, NFR-S1-004, NFR-S1-011, NFR-S1-014, NFR-S1-015, NFR-S1-024 | AC-S1-010, AC-S1-011, AC-S1-020 |
| REQ-S1-006 (BR-020) | CAP-S1-008, CAP-S1-009, CAP-S1-010 | FR-S1-019, FR-S1-020, FR-S1-021, FR-S1-022 | NFR-S1-009, NFR-S1-010, NFR-S1-012, NFR-S1-013, NFR-S1-027 | AC-S1-012, AC-S1-013, AC-S1-014, AC-S1-018 |
| REQ-S1-007 (BR-021) | CAP-S1-012 | FR-S1-025, FR-S1-026 | NFR-S1-009, NFR-S1-010, NFR-S1-026, NFR-S1-028 | AC-S1-017 |
| REQ-S1-008 (BR-020) | CAP-S1-011 | FR-S1-023, FR-S1-024 | NFR-S1-011, NFR-S1-012 | AC-S1-015, AC-S1-016 |

BR coverage: 8 of the 8 program requirements of this module (REQ-S1-001 to REQ-S1-008) and 6 of the 6 BRD requirements of E4 that name this service (BR-016 to BR-021) are covered by at least one functional requirement. No requirement of this module is left without a functional requirement, and no functional requirement lacks a source requirement (ASM-2848).

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Boundary and conformance test output in system test | FR-S1-001, NFR-S1-024 | Developer with the security administrator |
| Contract test against the source-data contract and its fake | FR-S1-001 to FR-S1-004, FR-S1-014, FR-S1-027 | Developer with P1 |
| Appraisal age drill: an appraisal past the limit, a failed order and its replay | FR-S1-005, FR-S1-006, FR-S1-007, NFR-S1-006, NFR-S1-027 | QA team |
| Outlier and acceptance drill with a held acceptance and a reason | FR-S1-008, FR-S1-009, FR-S1-010 | Sale officer with the QA team |
| Recommendation test with an agent timeout and a failed schema check | FR-S1-016, FR-S1-017, FR-S1-018, NFR-S1-004, NFR-S1-024 | QA team with the model risk officer |
| Approval matrix test across the delegation levels and the committee path | FR-S1-019, FR-S1-020, FR-S1-021, NFR-S1-012 | Product head with the QA team |
| Hold, review date and re-decision test, including a reopen with and without a written rule | FR-S1-022, FR-S1-023, FR-S1-024 | Team manager with the QA team |
| Route start, RouteDecided and timer breach test | FR-S1-025, FR-S1-026, NFR-S1-026 | QA team |
| Decision reproducibility and agent measure review | FR-S1-028, NFR-S1-011, NFR-S1-014, NFR-S1-015 | Internal audit with the model risk officer |
| Masking matrix, access log reconciliation and classification review | NFR-S1-016 to NFR-S1-021 | Compliance and PDPA officer |
| Performance and volume test at the stated volume | NFR-S1-001, NFR-S1-002, NFR-S1-003, NFR-S1-008 | QA team |

# 12. Open questions

The FSD's open items are carried forward with their IDs where they have one. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-S1-01 | Does this service read collateral and appraisal facts through the source-data contract, and who confirms the contract fields and the freshness response? | Solution architect with P1 | Before wave 3 system test | CAP-S1-001, CAP-S1-005, CAP-S1-006, CAP-S1-013 | GAP-1677; ASM-2825; Arch v5 slides 37 and 45 |
| OQ-S1-02 | Who writes the appraisal acceptance, the stale flag and the age in days: the extension row in P1's `valuation_ext`, or this service's valuation record? FSD P1 OQ-P1-05 stays open | Data architect with P1 | Before wave 3 system test | CAP-S1-001, CAP-S1-003, CAP-S1-004 | GAP-1678; ASM-2826; OQ-P1-05; ASM-0081 |
| OQ-S1-03 | Which tables hold the valuations, the D6 route decision and the route agent output in schema `rwb_valuation`, given that the Ownership Map lists none? | Data architect | Before the S1 DB story | CAP-S1-001, CAP-S1-007, CAP-S1-012 | GAP-1679; ASM-2827 |
| OQ-S1-04 | Does RouteDecided get an EV number and a catalogue row, and which service consumes it besides rwb-case? | Solution architect | Before wave 3 system test | CAP-S1-012 | GAP-1680; ASM-2828; GAP-1685 |
| OQ-S1-05 | Is the route command published as `POST /cases/{id}/route-proposals` or as `POST /cases/{caseId}/route`, and does the valuation read keep the path `GET /cases/{id}/valuation`? | Solution architect | Before the S1 contract story closes | CAP-S1-007, CAP-S1-008, CAP-S1-013 | GAP-1681; ASM-2829 |
| OQ-S1-06 | Do the two asset valuation writes stay here, and does rwb-asset read the accepted appraisal through this service? | Solution architect with the S5 owner | Before wave 3 system test | CAP-S1-001, CAP-S1-004 | GAP-1682; ASM-2830; ASM-0043 |
| OQ-S1-07 | Which path carries the valuation order to SVAF, when the connection matrix gives this service no cell to rwb-integration? | Solution architect with the integration lead | Before wave 3 system test | CAP-S1-002 | GAP-1683; ASM-2831 |
| OQ-S1-08 | What is the route numbering? R-LIT-01 starts litigation on route R4, while the case journeys call R4 the guarantee claim and R5 litigation | Business analyst, S1 with P7 | Before wave 3 system test | CAP-S1-012 | GAP-1688; ASM-2836 |
| OQ-S1-09 | How is the E3 deed in lieu tested before this service is created, and who owns the published contract and its fake? | Solution architect | Before E3 system test | CAP-S1-001, CAP-S1-006 | GAP-1689; ASM-2837; BRD Q-016 |
| OQ-S1-10 | What is each approval level and limit by decision, product and amount, and who is the substitute for each (DL18)? | Risk with the product heads | Before wave 3 release | CAP-S1-008, CAP-S1-009 | GAP-1691; ASM-2839; DL18; BRD Q-001 |
| OQ-S1-11 | Which rule package does the route decision evaluate, who owns it, and when does it arrive, given that no S1 package exists yet? | Center of excellence analyst with P7 | Before wave 3 release | CAP-S1-005, CAP-S1-006, CAP-S1-007 | GAP-1687; ASM-2835; DP-04 |
| OQ-S1-12 | What is the field list of the route decision record and of the route agent output? | Data architect | Before the S1 DB story | CAP-S1-007 | GAP-1694; ASM-2842 |
| OQ-S1-13 | Which service owns the route decision screen SCR-13, and where does the cell in the screen matrix route from? | Solution architect | Before wave 3 release | CAP-S1-007, CAP-S1-008 | Arch v5 slide 41 (edge and gateway); DP-19 |
| OQ-S1-14 | Which service owns the wording of the four messages the decision shows, and who approves the Thai and English versions? | Business analyst, S1 | Before wave 3 release | All messages | GAP-1690; ASM-2838 |
| OQ-S1-15 | What classification and what retention period apply to the valuation record, the route decision and the agent output (DL26)? | Compliance and PDPA officer | Before wave 3 release | CAP-S1-001, CAP-S1-007 | GAP-1692; ASM-2840; DL26 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (GAP-1693; ASM-2841).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 2 (business outcomes), 5.8 (S1 requirements, REQ-S1-001 to REQ-S1-008), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan), 9 (open decisions incl. DL18, DL26, DL43), 10.1 and 10.2 (the service epic RWB-SVC-S1, schema and wave) |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 7.1 and 7.3 (E4 scope, service and wave), 8.2 (BR-016 to BR-021), 10 (KPI-003, KPI-011, KPI-012), 11.1 to 11.4 (ASM, CON, DEP, RISK), 12 (Q-001, Q-002, Q-012, Q-014, Q-016), 13 (governance) |
| Recovery Workbench FSD S1 Valuation and route v3 | Document control, Existing capability check, A1 (context, scope, dependencies, feature overview), A2.1 to A2.12 (functional decomposition with field catalog, rules, roles and acceptance criteria), Requirements served, Screens, Appendix A and B |
| Recovery Workbench Architecture v5 | Slides 3 (the eight routes and D6), 4 (19 modules), 9 to 13 (call types, timeouts, retry, the connection matrix), 14 to 20 (service contracts), 27 (rule governance), 30 (19 schemas), 32 (bank scheduler at the edges), 37 (what changes and why), 41 (service catalogue), 42 and 43 (event catalogue), 44 (job map), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Slides 13 (workflow per stage), 15 (rule governance and versioning), 16 (decision record), 17 (S1 route decision: steps, clocks, Drools, open point) |
| Recovery Workbench Microservice Ownership Map v1 | Services (S1 row), Endpoints (route and valuation paths), Workflows (RouteDecisionWorkflow), Events (EV-01 to EV-30), Jobs, Tables (no S1 row) and Rulings |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic), 4 (partner access, valuers first needed at Epic 4) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R5 (target structure, DP table, wave map), R8 (outputs), R9 (gaps and assumptions) |
