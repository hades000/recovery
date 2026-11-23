SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD S8 rwb-deviation v1
description: Product requirements for the Recovery Workbench deviation handling service (S8 rwb-deviation) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD S8 Deviation handling v3.md
service: S8 rwb-deviation
epic: RWB-SVC-S8
wave: 2
decision: D-RCV-60
---

# Recovery Workbench PRD S8 rwb-deviation v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD S8 rwb-deviation |
| Document ID | S8-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft. The BRD is read as approved for this run and the approval itself is carried as an assumption (ASM-3012) |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | S8 rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 2 |
| Business epic | EP02 (Epic 2, screening), EP03 (Epic 3, the deceased slice), EP07 (Epic 7, the X1 to X7 flows) |
| Release | 31 December 2026 (tentative) for the E2 slice; 31 January 2027 (tentative) for the E3 slice; 31 May 2027 (tentative) for the E7 slice |
| Schema | `rwb_deviation` |
| REST base | `/api/recovery/deviation/v1` |
| Topic | `rwb.deviation.events.v1` |
| Temporal task queue | `rwb-deviation` |
| Workflow | DeviationWorkflow (child of CaseWorkflow; can start at any time and pauses the stage clock) |
| Java package | `th.co.scb.ace.workbench.recovery.deviation` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Business analyst, S8 |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5), ADR-010, ADR-013 to ADR-023, DL44 to DL49 |
| Upstream artifacts | Business Requirements Program v5; Business Requirements Epic 2 v3; Business Requirements Epics 3 to 8 v1; FSD S8 Deviation handling v3; Architecture v5; Temporal and Drools Design v1; Microservice Ownership Map v1 |
| Upstream requirement IDs | REQ-DVH-001 to REQ-DVH-011; REQ-S8-001 to REQ-S8-007; BR-062, BR-063, BR-064, BR-065, BR-066, BR-067, BR-068, BR-069; BR-079; RULE-012, RULE-013, RULE-014; R-DEV-01 to R-DEV-22; NFR-001, NFR-002, NFR-008, NFR-009, NFR-010, NFR-011, NFR-013, NFR-014, NFR-015, NFR-020, NFR-021, NFR-022, NFR-023, NFR-024, NFR-025, NFR-026, NFR-027, NFR-033, NFR-034, NFR-035, NFR-038, NFR-039, NFR-040, NFR-042, NFR-043, NFR-045, NFR-046, NFR-047, NFR-049, NFR-051, NFR-052, NFR-053, NFR-054, NFR-055, NFR-059, NFR-060, NFR-061, NFR-064, NFR-065, NFR-067, NFR-068 |
| Upstream acceptance criteria | AC-S8-001-01 to AC-S8-019-01 (main success flow, one per feature); AC-ALT-S8-001-01 to AC-ALT-S8-009-02 (alternate flow, E2 features only); AC-EXC-S8-001-01 to AC-EXC-S8-019-02 (exception flow). The FSD defines no alternate flow for A2.10 to A2.19 and no system background event for any feature (GAP-1823; ASM-3001) |
| Generated IDs | CAP-S8-001 to CAP-S8-019; FR-S8-001 to FR-S8-056; NFR-S8-001 to NFR-S8-029; AC-S8-001 to AC-S8-023; JRN-S8-01 to JRN-S8-07; ROL-S8-01 to ROL-S8-13; OQ-S8-01 to OQ-S8-16 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD S8 Deviation handling v3 (15 November 2026), Business Requirements Program v5, Business Requirements Epic 2 v3 and Business Requirements Epics 3 to 8 v1, realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD S8 Deviation handling v3. Its requirement IDs, feature IDs, rule IDs and acceptance criterion IDs are carried unchanged; the microservice realignment changes the read path, the carrier of the outside effects, the timer technology, the owner of the screens and the release in which the E7 flows land, not the requirement substance. The CAP, FR, NFR, AC, journey, role and open-question IDs of this document are new and exist only here (ASM-3014).

| Version | Date | Change carried from the FSD |
|---|---|---|
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Constraint, freshness rule and trigger wording only. Everything else unchanged from v2 |
| 1 and 2 | Not specified in the source documents (GAP-1834; ASM-3015) | Earlier versions of the FSD. Their dates and change notes are not in the sources read, and are carried as an open item rather than reconstructed |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, journey, role and open-question IDs are new; the FSD requirement IDs (REQ-DVH-001 to REQ-DVH-011, REQ-S8-001 to REQ-S8-007), feature IDs (FEAT-DVH-01 to FEAT-DVH-09, FEAT-DVF-01 to FEAT-DVF-10), validation rule IDs (VR-S8-001-1 to VR-S8-019-1), business rule IDs (BR-S8-001 to BR-S8-019), routing rule IDs (R-DEV-01 to R-DEV-22), acceptance criteria IDs (AC-S8-001-01 to AC-S8-019-01 and the AC-ALT and AC-EXC rows), message IDs (MSG-P1-001, MSG-P3-003, MSG-P3-004, MSG-P3-018, MSG-P4-002, MSG-P7-003, MSG-GEN-001, MSG-GEN-006), list IDs (LOV-DEVIATION, LOV-RAISED-BY) and screen IDs (SCR-06, SCR-08) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v5 | BRD | Source of the program requirements REQ-DVH-001 to REQ-DVH-011 and REQ-S8-001 to REQ-S8-007, of the service epic and wave, and of the non-functional requirements |
| Recovery Workbench Business Requirements Epic 2 v3 | BRD | Source of the E2 screening scope, the three deviation stories and the case record view the deviation flag sits on |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | BRD | Source of BR-062 to BR-069 and BR-079, of RULE-012 to RULE-014, of the E7 scope, the measures, the risks and the open questions |
| Recovery Workbench Functional Specifications by Module v6, FSD S8 Deviation handling v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, only rwb-source-data reads ACE, Kafka, Temporal, no data lake, the connection matrix, the event catalogue and the job map |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: DeviationWorkflow on `rwb-deviation`, the pause of one timer and not the other, the 10 working day escalation, the deviation route set |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every operation, event, workflow and table named here: S8 owns DeviationWorkflow, EV-06, EV-07 and the `deviation` table |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-deviation (S8) is the recovery module's exception handling. It turns "an exception stops the normal route, gets a named owner and a clock" into a product: a flag with a code and a reason raised by a person or by rule; a stage clock paused while the legal clock keeps running; the case routed to the role that owns the code, or to the team manager where no role does; contact stopped on a dispute, a hardship case or a death; the case returned to the exact state it paused in, or to the route decision where the outcome changes the route; more than one deviation open on one case with its own owner each; the screening agent in shadow and then at level 1 on one segment, with a person in front of every flag below the confidence threshold; and every X1 to X7 flow run end to end with its approver, its contact rules and its return point.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-deviation | One deployable with its own API and worker, schema `rwb_deviation`, login, topic `rwb.deviation.events.v1`, task queue `rwb-deviation` and lifecycle | Deviation handling becomes one owned product with its own release, instead of a set of screens and a scheduler table inside a single deployable |
| The deviation as a governed record | The code, the reason, the raised-by, the paused state, the handler, the contact stop and the cleared-at held once per deviation and linked to the case by business key | An exception handled in a note is an exception nobody can count, and a pause nobody can justify |
| The two clocks as workflow timers | The stage clock is a durable timer that pauses and resumes inside DeviationWorkflow; the prescription clock is never paused | The law does not pause for a deviation, and a timer that lives in a shared scheduler table loses the paused state on a restart |
| The code-to-owner route as a rule | Each code routes to the role that owns it, an unmapped code routes to the team manager and is recorded as unmapped | An exception with no owner is a case that stalls, which is the risk the BRD already names |
| The screening agent as a governed run | Shadow runs with their scores, then level 1 on one segment with a person in front of every low-confidence flag | A flag that changes a customer's case must earn the autonomy it runs at |
| The deviation as an event | DeviationRaised and DeviationCleared on `rwb.deviation.events.v1`, consumed by rwb-case, rwb-comms and rwb-treatment | The case pauses and the contact stops in the same step as the flag, not on a poll |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables, its ingestion of party and account flags and its backups | REUSE | ACE team |
| The read-only view contract and the freshness of every data product | REUSE, elsewhere | P1 rwb-source-data (this service reads it by contract) |
| Sign-in, access check, audit and personal-data logging | REUSE | ACE common module and P4 rwb-access |
| Case record, CMMN state, queues, tasks, allocation and the case timers | REUSE | P3 rwb-case (DeviationWorkflow is its child workflow) |
| Workflow and state machine, and the stage clock that the deviation pauses | REUSE | P3 rwb-case; the pause is signalled from DeviationWorkflow |
| Decision record and audit trail, the hash chain and the rule package registry | REUSE | P7 rwb-decision, written through the decision-record library |
| Attachments, evidence and the document store the screening reads | REUSE, elsewhere | P5 rwb-document (GAP-1822; ASM-3000) |
| Notification path and the outbound sends a contact stop holds | REUSE | P6 rwb-comms (it consumes DeviationRaised and DeviationCleared) |
| Roles, capability areas, masking policy and the delegation table | REUSE | P4 rwb-access |
| Agent runtime, model endpoint, guardrails, autonomy policy and run record | REUSE | P10 rwb-agent |
| The outside systems the X flows reach: the fraud system, the bureau, the external flow system, the litigation system, the appraisal system and the partner portal | MOVED | P2 rwb-integration or the owning service's contract (GAP-1821; ASM-2999) |
| Screens and the composite routes that serve them | REUSE | Platform edge, gateway-bff (RWB-PLT-EDGE); this service owns neither screen (GAP-1830; ASM-3008) |
| Quartz scheduler and its shared tables | REPLACED | Temporal workflow kit (PLT); ADR-016, DP-10 (GAP-1817; ASM-2995) |
| Embedded Drools with the deviation decision tables in the monolith | MOVED, in part | Governance and versioning in P7; evaluation stays local (ADR-017, DP-04) |
| The restructure calculator | NOT USED | ACE common module; the FSD marks it reused and not used |
| Collections before day 90 on EFS | OUT OF SCOPE | EFS and the ACE collection module |
| Booking in the core bank | OUT OF SCOPE | The officer and the core bank |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014; slides 12 and 45). The FSD's own read wording is superseded by this (ASM-2994).
2. The service writes only schema `rwb_deviation`; no cross-schema join and no foreign key into `public` (ADR-014, DP-01).
3. DeviationWorkflow is a Temporal child of CaseWorkflow on task queue `rwb-deviation`; it can start at any time in the case and it pauses the stage clock (slide 25; Temporal design slides 8 and 24).
4. REST is one hop from gateway-bff with a 2 s timeout, an Idempotency-Key on every POST and RFC 9457 problem details; a GET is retried once with jitter (ADR-020; slides 10 and 11).
5. Events are CloudEvents 1.0 on Kafka with an outbox and an inbox, retry at 1 minute, 10 minutes and 1 hour and then a dead-letter topic; topic `rwb.deviation.events.v1`, key `caseId` (ADR-015, DP-09, DP-14; slides 9 and 11).
6. Temporal namespace `rwb-recovery`; the pause and the resume are durable timers inside DeviationWorkflow, and Schedules and durable timers replace Quartz (ADR-016, DP-10).
7. Rules are versioned data evaluated in process by the embedded Drools kit; authoring, testing and promotion are governed in rwb-decision (ADR-017, DP-04). The deviation route set is 22 rules and its package is Phase 2 (GAP-1826; ASM-3004).
8. There is no data lake: deviation measures and conduct reporting read the decision record and the events into rwb-reporting (ADR-018, DP-17).
9. Personal data stays out of events, workflow inputs and logs; masking is by role, using the permission data cached from rwb-access, and each service authorises the object itself (slide 10; NFR-039, NFR-040).
10. The bank scheduler owns only the cross-system edges and signals the business date; it never enters the case journey, and deviation screening is started by the readiness event rather than by a job of this service (slide 31, slide 32).
11. The decision record is written through the shared local decision-record library and the shared decision record topic (DP-03); an approval that a deviation carries is a step inside its own workflow, because the connection matrix gives S8 no rwb-decision cell (GAP-1820; ASM-2998).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-S8-01 | Case owner | To raise a deviation with a reason, to see the case paused and stopped, and to get it back where it was | JRN-S8-01, JRN-S8-02, JRN-S8-04 |
| ROL-S8-02 | Complaint officer | The X1 flow, its evidence pack and its service level | JRN-S8-03 |
| ROL-S8-03 | Hardship and vulnerability specialist | The X2 contact limits and the X3 estate position, with Legal beside them | JRN-S8-03, JRN-S8-06 |
| ROL-S8-04 | Fraud investigator | The X4 referral, the hold on recovery action and the outcome that routes the case | JRN-S8-03 |
| ROL-S8-05 | Legal counsel | The X3 estate claim and the X5 claim deadline with its filing evidence | JRN-S8-03, JRN-S8-06 |
| ROL-S8-06 | Enforcement owner | The X5 route to litigation and then to write-off after the receiver reports | JRN-S8-03 |
| ROL-S8-07 | Conduct and QA officer | The low-confidence review, the complaint-to-contact match and the breach path | JRN-S8-02, JRN-S8-07 |
| ROL-S8-08 | Team manager | The unmapped codes, the deviations past their service level and the queue by age | JRN-S8-05 |
| ROL-S8-09 | Center of excellence analyst | The override and deviation patterns of the month, with the rule version applied | JRN-S8-07 |
| ROL-S8-10 | Risk and model risk officer | The screening agent's acceptance, override, precision and recall per code and per segment | JRN-S8-07 |
| ROL-S8-11 | Compliance and PDPA officer | A contact stop that cannot be bypassed, a data subject request held, and an access log that cannot be skipped | JRN-S8-04, JRN-S8-07 |
| ROL-S8-12 | Internal audit and platform administrator | A deviation reproducible from the log, a workflow that reports a breach, and an alert with a named owner | JRN-S8-05, JRN-S8-07 |
| ROL-S8-13 | Developer | A typed contract to build against, a fake for every dependency, and a build that fails on a direct ACE read | JRN-S8-07 |

Non-human actors: the case workflow that starts DeviationWorkflow; the case router that delivers DeviationRaised and DeviationCleared to it; the screening agent on rwb-agent; the outbox relay; the consumers of the two events. The customer is never a user of this product and is never contacted by it.

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. A complaint, a hardship case, a death, a fraud flag, a bankruptcy, a lost contact or a damaged collateral is handled case by case in notes, with no clock and no owner outside the officer's own list.
2. The stage service level keeps running while the exception is worked, so the case counts as late for a reason nobody can see.
3. Contact continues after a death or a hardship notice because the stop lives in a person's memory and not in the system.
4. The legal deadline is tracked beside the stage deadline with no rule that says which one pauses.
5. The screening of cases for these exceptions is done by reading call notes, so it is done unevenly and cannot be measured.

Consequence: two officers handle the same exception two different ways, the case is counted late while it is lawfully stopped, and the bank cannot show that it stopped contacting a deceased customer's family.

## 4.2 Target state (this product)

### JRN-S8-01 The flag from the screening run or from the officer (daily, case owner and screening agent)

1. The readiness event for the business date starts the screening run; a newly stored document, a closed agent run and a new case each start a run of their own.
2. The run reads the case, its party flags and its documents through the contracts of their owners, with the business date and load time of each.
3. Where a rule fires, the deviation is raised with its code, its reasons and its source references; the screening agent proposes a code with its reasons and its confidence.
4. The case owner raises a deviation by hand where the officer sees what the rules did not, with a reason and the evidence reference.
5. A code outside the list, or a flag with no reason, is refused and nothing changes.

### JRN-S8-02 Pause, stop and route (same day, case owner, conduct and QA officer)

1. The stage clock pauses and the prescription clock does not; the case keeps the state it was in and shows it is on hold.
2. The prescription date is shown with its warning where it falls inside the warning window.
3. The code routes the case to the role that owns it; an unmapped code routes to the team manager and is recorded as unmapped.
4. A dispute, a hardship case or a death sets the contact stop, and every outbound send is held from that moment.
5. A flag below the confidence threshold waits for a person before it changes the case, and a rejection needs a reason.

### JRN-S8-03 The owner works the exception (X1 to X7, complaint officer, specialist, fraud investigator, Legal and enforcement owner)

1. The owner sees the deviation on the case and works it inside its service level, with the route the code implies.
2. X1 assembles its evidence pack from the documents and records the resolution.
3. X2 applies the contact limits and reaches a hardship or relief decision.
4. X4 refers to the fraud team and holds recovery action until the flag is confirmed or cleared.
5. X5 files the claim with the receiver or the Legal Execution Department before the deadline.
6. X6 runs the skip trace through the bureau, the internal data and the agency inside its window.
7. X7 files the insurance claim, which a person approves, and asks for the collateral to be re-appraised.

### JRN-S8-04 Clear, resume and stop the stop (on resolution, case owner and Compliance)

1. The owner records the outcome, its reason and the role that took it, and the record is written to the decision record.
2. The case returns to the exact state it paused in; where the outcome changes the route, it returns to the route decision instead.
3. Clearing a flag that was never a deviation is recorded as an override with its reason.
4. The contact stop is lifted only on the clear, and the lift is published so rwb-comms releases the sends.
5. A data subject request holds the automated processing on the case and routes it to Compliance inside the statutory period.

### JRN-S8-05 Escalation and the queue (as the clock runs, team manager)

1. The queue shows every open deviation by code, handler and age.
2. A deviation not resolved inside its service level escalates to the team manager.
3. An unmapped code appears in the manager's list with its case, so the mapping can be fixed in reference data and not in code.
4. The case shows its open deviations on the record view and in every queue view it appears in.

### JRN-S8-06 The death on the case (on trigger, specialist and Legal)

1. X3 is raised, the stage clock pauses and the prescription clock keeps running.
2. Contact stops on every channel and the stop is visible on the case with its approver.
3. The heirs and the estate are notified, and the insurance claim path starts.
4. Where the insurance does not clear the position, the case returns to the route decision against the estate.
5. The case resumes later at the state it paused in, or re-routes, and the whole history stays readable.

### JRN-S8-07 Evidence and measures read later (audit, center of excellence, risk and developer)

1. An auditor reads one deviation: its code, who raised it, the role that owned it, the role that approved it, the pause and the resume, and the rule version applied.
2. The center of excellence reads the override and deviation patterns of the month, with the coded reason of every override.
3. The risk and model risk officer reads the agent's precision, recall, acceptance and override per code and per segment, and the runs it stayed in shadow.
4. The compliance officer reads every contact stop, every lift and every breach, and every personal-data read behind them.
5. A developer builds against the published contract and its fake; a build that reads an ACE view or an ACE table directly fails.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic. The BR column carries the program requirement of the E2 and E3 slices and the BRD requirement of the E7 slice, because Epic 2 has no BR numbering of its own.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-S8-001 | Deviation flag with its code, reason and source | An exception is a record with a code, a reason and a source, raised by a person or by rule, instead of a note | REQ-DVH-001 | Must | 2 | FEAT-DVH-01 (A2.1) |
| CAP-S8-002 | Stage clock paused, prescription clock running | The case stops being counted late while it is lawfully stopped, and the legal deadline never pauses | REQ-DVH-002; RULE-012 | Must | 2 | FEAT-DVH-02 (A2.2), FEAT-DVH-03 (A2.3) |
| CAP-S8-003 | Route to the named owner by code | Each code reaches the role that owns it, and a code with no owner reaches the team manager and is recorded | REQ-DVH-003; RULE-014 | Must | 2 | FEAT-DVH-04 (A2.4) |
| CAP-S8-004 | Contact stop for X1 to X3 and its lift | No one contacts a disputed, vulnerable or deceased customer until the stop is lifted on the record | REQ-DVH-004; RULE-013 | Must | 2 | FEAT-DVH-05 (A2.5) |
| CAP-S8-005 | Clear, resume and re-route | The case returns to the exact state it paused in, or to the route decision where the outcome changes the route | REQ-DVH-005 | Must | 2 | FEAT-DVH-06 (A2.6) |
| CAP-S8-006 | The deviation visible on the case and in every queue | The flag, its code, its owner, its approver and the stop are on the case record and on every list the case appears in | REQ-DVH-006 | Must | 2 | A2.2, A2.3 and A2.9 criteria; SCR-08 |
| CAP-S8-007 | Screening in shadow | The agent proposes codes with reasons against a real population and changes nothing | REQ-DVH-001 | Must | 2 | FEAT-DVH-07 (A2.7) |
| CAP-S8-008 | Screening at level 1 on one segment, with a person below the threshold | A proposal is shown to the owner on one segment and confirmed by them, and a low-confidence flag always waits for a person | REQ-DVH-001, REQ-DVH-006 | Must | 2 | FEAT-DVH-07 (A2.7), FEAT-DVH-08 (A2.8) |
| CAP-S8-009 | Two deviations on one case | Each open deviation has its own owner and the case resumes only when all are cleared | REQ-DVH-005 | Must | 2 | FEAT-DVH-09 (A2.9) |
| CAP-S8-010 | X1 dispute and complaint end to end | The complaint runs from detection through its evidence pack to resolution inside its service level | BR-062 | Must | 4 | FEAT-DVF-01 (A2.10) |
| CAP-S8-011 | X2 vulnerability and hardship end to end | The case follows the contact limits set for it and reaches a hardship or relief decision | BR-063 | Must | 4 | FEAT-DVF-02 (A2.11) |
| CAP-S8-012 | X3 deceased customer end to end | Contact stops, the heirs and the estate are told, the insurance claim is filed and the estate position is settled | BR-064; REQ-DVH-008 | Must | 2 and 4 | FEAT-DVF-03 (A2.12) |
| CAP-S8-013 | X4 fraud end to end | The case is referred to the fraud team, recovery action is held, and the case routes on the outcome | BR-065; REQ-DVH-010 | Must | 4 | FEAT-DVF-04 (A2.13) |
| CAP-S8-014 | X5 bankruptcy and seizure end to end | Direct collection stops and the claim is filed before its deadline | BR-066; REQ-DVH-009 | Must | 4 | FEAT-DVF-05 (A2.14) |
| CAP-S8-015 | X6 lost contact and skip trace end to end | The skip trace runs inside its window and the case returns to a decision either way | BR-067 | Must | 4 | FEAT-DVF-06 (A2.15) |
| CAP-S8-016 | X7 collateral event end to end | The insurance claim is filed with a person's approval and the collateral is re-appraised before the next decision | BR-068 | Must | 4 | FEAT-DVF-07 (A2.16) |
| CAP-S8-017 | Override review, complaint matching and the breach path | Overrides are reviewed monthly, a complaint is matched to the contact that caused it, and a contact sent against a stop opens a breach | BR-069; REQ-DVH-007, REQ-S8-006 | Must | 4 | FEAT-DVF-08 (A2.17), FEAT-DVF-09 (A2.18), FEAT-DVF-10 (A2.19) |
| CAP-S8-018 | Data subject request hold | Automated processing on the case is held and the request reaches Compliance inside the statutory period | BR-079; REQ-S8-007 | Must | 4 | A1.1 in scope; Requirements served REQ-S8-007 |
| CAP-S8-019 | Escalation when a deviation runs past its service level | A deviation nobody resolves reaches the team manager instead of sitting open | REQ-DVH-003, REQ-S8-006 | Should | 2 | A2.9 criteria; R-DEV-20 in the design |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Direct read of the ACE views and the batch-status view | Not carried | rwb-source-data's contract (GAP-1816; ASM-2994) |
| Quartz scheduling of the pause, the prescription clock and the resume | Replaced | Durable timers in DeviationWorkflow through the workflow kit (GAP-1817; ASM-2995) |
| Direct call to the fraud system, the bureau, the external flow system, the litigation system, the appraisal system or the partner portal | Not carried | The rwb-integration contract or the owning service's contract (GAP-1821; ASM-2999) |
| A copy of a document or of call-note text inside the deviation schema | Not carried | P5 rwb-document and the P1 contract (GAP-1822; ASM-3000) |
| The two deviation screens as pages inside this service | Not carried | gateway-bff composite routes at the edge (GAP-1830; ASM-3008) |
| The decision log copy to a data lake | Removed | No data lake in v5 (ADR-018); measures read the decision record and the events |
| The restructure calculator | Out of scope | ACE common module; the FSD marks it reused and not used |
| Collections before day 90 on EFS and booking in the core bank | Out of scope | EFS, the ACE collection module and the core bank |

# 6. Functional requirements

Every requirement is specific and testable. The FSD REQ column keeps the trace to the requirement the FSD serves; the BR column keeps the trace to the BRD requirement where one exists, and to the program requirement of the E2 and E3 slices where the epic has no BR numbering of its own. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-S8-001 | The service SHALL hold one deviation record per case and code with the case reference, the code from LOV-DEVIATION (X1 to X7), the reason, the source reference, the raised-at time, the raised-by from LOV-RAISED-BY, the paused state, the handler, the contact stop and the cleared-at, and SHALL link the record to the case by business key with no foreign key. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-002 | The service SHALL detect a deviation by rule from case data, call notes, documents and external party flags, and SHALL record the rule and package version that fired; no deviation SHALL exist where neither a rule nor a person raised one. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-003 | The service SHALL accept a deviation raised by an officer with a reason and an evidence reference, SHALL require the reason, and SHALL record the role that raised it. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-004 | The service SHALL refuse a code outside LOV-DEVIATION and a flag with no reason, with MSG-GEN-001, and SHALL change nothing on the case. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-005 | The service SHALL pause the stage clock of the case and only that clock while a deviation is open, SHALL never pause the prescription clock, and SHALL not replace the case state with a deviation state (R-DEV-01). | CAP-S8-002 | REQ-DVH-002; RULE-012 | REQ-DVH-002 | Must | 2 |
| FR-S8-006 | The service SHALL hold the pause and the resume as durable timers inside DeviationWorkflow through the workflow kit, and SHALL use no Quartz table, connection or job; a worker restart SHALL not lose the pause or the state the case paused in. | CAP-S8-002 | REQ-DVH-002 | REQ-DVH-002 | Must | 2 |
| FR-S8-007 | The service SHALL keep the prescription date visible and unchanged for the life of the deviation, SHALL show it with MSG-P3-003 where it falls inside the warning window in force, and SHALL show no warning outside that window. | CAP-S8-002 | REQ-DVH-002 | REQ-DVH-002 | Must | 2 |
| FR-S8-008 | The service SHALL record the routing state the case was in when it paused, SHALL return the case to that state on the clear, and SHALL refuse a resume with no recorded paused state (R-DEV-08, R-DEV-18). | CAP-S8-002 | REQ-DVH-002 | REQ-DVH-005 | Must | 2 |
| FR-S8-009 | The service SHALL route each code to the role that owns it: X1 to the complaint officer, X2 to the specialist, X3 to the specialist with Legal, X4 to the fraud team, X5 to Legal, X6 to the agent, and X7 to the agent with a person approving the insurance claim (R-DEV-02 to R-DEV-06). | CAP-S8-003 | REQ-DVH-003; RULE-014 | REQ-DVH-003 | Must | 2 |
| FR-S8-010 | The service SHALL route a code with no owner to the team manager and SHALL record it as unmapped, and the unmapped count SHALL be readable per month (RULE-014, R-DEV-21). | CAP-S8-003 | REQ-DVH-003; RULE-014 | REQ-DVH-003 | Must | 2 |
| FR-S8-011 | The service SHALL raise a task in the queue of the owning role through the rwb-case contract and SHALL record the handler on the deviation. | CAP-S8-003 | REQ-DVH-003 | REQ-DVH-003 | Must | 2 |
| FR-S8-012 | The service SHALL set the contact stop automatically for X1, X2 and X3, SHALL hold every outbound send from that moment, and SHALL show the stop and its reason on the case (RULE-013). | CAP-S8-004 | REQ-DVH-004; RULE-013 | REQ-DVH-004 | Must | 2 |
| FR-S8-013 | The service SHALL publish DeviationRaised (EV-06) as CloudEvents 1.0 on `rwb.deviation.events.v1`, keyed by the case and written through the outbox, so that rwb-case pauses the stage clock, rwb-comms holds the sends and the route sets react to the raised flag. | CAP-S8-004 | REQ-DVH-004 | REQ-DVH-004 | Must | 2 |
| FR-S8-014 | The service SHALL lift the contact stop only on the clear and SHALL publish DeviationCleared (EV-07) in the same step, so that a stop is never lifted by a second action. | CAP-S8-004 | REQ-DVH-004 | REQ-DVH-004 | Must | 2 |
| FR-S8-015 | The service SHALL record the outcome, its coded reason and the role that took it on a clear, SHALL write the decision record through the decision-record library, and SHALL change nothing where that record cannot be written. | CAP-S8-005 | REQ-DVH-005 | REQ-DVH-005 | Must | 2 |
| FR-S8-016 | The service SHALL return the case to the state it paused in, or to the route decision D6 where the outcome changes the route, and SHALL record which of the two was taken (R-DEV-19). | CAP-S8-005 | REQ-DVH-005 | REQ-DVH-005 | Must | 2 |
| FR-S8-017 | The service SHALL clear a flag the owner marks as not a deviation with a reason, SHALL count it as an override, and SHALL keep the flag, the reason and the role (R-DEV-07). | CAP-S8-005 | REQ-DVH-005 | REQ-DVH-005 | Must | 2 |
| FR-S8-018 | The service SHALL show the code, the handler, the approver, the raised date, the return point, the contact stop and the state of every open deviation on the case record view and in every queue view the case appears in. | CAP-S8-006 | REQ-DVH-006 | REQ-DVH-006 | Must | 2 |
| FR-S8-019 | The service SHALL serve the deviation section of the case record as a read that never blocks the record: where it fails or does not answer inside 2 seconds the timers and the prescription date SHALL still show, the section SHALL show MSG-GEN-006 naming "Deviation handling", and the on-hold banner SHALL show from the case's own flag. | CAP-S8-006 | REQ-DVH-006 | REQ-DVH-006 | Must | 2 |
| FR-S8-020 | The service SHALL serve the open deviations by code, by handler and by age for the deviation queue, with the case, the code, the owner and the age of each. | CAP-S8-006 | REQ-DVH-006 | REQ-DVH-006 | Must | 2 |
| FR-S8-021 | The service SHALL store, for a shadow screening run, the proposed codes with their reasons and source references and the mode SHADOW, and SHALL raise no deviation record, set deviation_open false on every case, set no contact stop, and return no proposal from a user-facing operation. | CAP-S8-007 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-022 | The service SHALL hold one screening run per case and event key and SHALL count a repeated event without creating a second run (R-UNI-40). | CAP-S8-007 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-023 | The service SHALL store one score row per code X1 to X7 for a scored sample, with its precision, its recall and its sample size, and SHALL read the analyst flags it is compared against from the sample named with its version. | CAP-S8-007 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-024 | The service SHALL start a screening run when the business date becomes ready, when a case is created, when a document is stored for an open case and when an agent run completes, SHALL record the run key and the trigger of each run, and SHALL read its documents through P5's contract and its call notes through P1's contract. | CAP-S8-007 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-025 | The service SHALL show a level 1 proposal for a case on the segment the autonomy policy names, with the proposed code, its reasons, the preceding contact and the marker that the proposal is agent output. | CAP-S8-008 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-026 | The service SHALL raise the deviation on the owner's confirmation with raised-by SCREENING_AGENT under R-DEV-01, SHALL move the case to its on-hold state, and SHALL record the agent feedback as accepted with the decision log entry reference. | CAP-S8-008 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-027 | The service SHALL keep every segment outside the autonomy policy in shadow and SHALL return no screening output for a case on such a segment. | CAP-S8-008 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-028 | The service SHALL put every flag below the confidence threshold in front of a person before it changes the case, SHALL require a reason on a rejection, and where the decision record cannot be written SHALL refuse the request with 503 and MSG-P7-003 and leave no feedback row. | CAP-S8-008 | REQ-DVH-001, REQ-DVH-006 | REQ-DVH-001 | Must | 2 |
| FR-S8-029 | The service SHALL hold more than one open deviation on one case, each with its own code, owner, contact stop and paused state. | CAP-S8-009 | REQ-DVH-005 | REQ-DVH-005 | Must | 2 |
| FR-S8-030 | The service SHALL resume the case only when every open deviation on it is cleared, and while any remains open SHALL keep the case paused and show all of them (R-DEV-09). | CAP-S8-009 | REQ-DVH-005 | REQ-DVH-005 | Must | 2 |
| FR-S8-031 | The service SHALL assemble the X1 evidence pack from the documents of the case through P5's contract, SHALL record the resolution with its reason, and SHALL hold the pack reference on the deviation. | CAP-S8-010 | BR-062 | REQ-S8-001 | Must | 4 |
| FR-S8-032 | The service SHALL return an X1 case to the same decision with its timers resumed, and SHALL record whether the service level was met. | CAP-S8-010 | BR-062 | REQ-S8-003 | Must | 4 |
| FR-S8-033 | The service SHALL apply the contact limits set for an X2 case, SHALL place the case in the specialist queue, and SHALL record the hardship or relief decision with the rule version applied. | CAP-S8-011 | BR-063 | REQ-S8-002 | Must | 4 |
| FR-S8-034 | The service SHALL stop every contact on an X3 case, SHALL record the notification to the heirs and the estate, and SHALL start the insurance claim path (R-DEV-03, R-DEV-06). | CAP-S8-012 | BR-064 | REQ-DVH-008 | Must | 2 |
| FR-S8-035 | The service SHALL return an X3 case to the route decision against the estate where the insurance does not clear the position, and SHALL record that return (R-DEV-12). | CAP-S8-012 | BR-064 | REQ-DVH-008 | Must | 4 |
| FR-S8-036 | The service SHALL refer an X4 case to the fraud team, SHALL hold recovery action until the flag is confirmed or cleared, SHALL track the inquiry, and SHALL route the case on the outcome. | CAP-S8-013 | BR-065 | REQ-DVH-010 | Must | 4 |
| FR-S8-037 | The service SHALL stop direct collection on an X5 case, SHALL start the claim deadline clock, SHALL record the filing with the official receiver or the Legal Execution Department before the deadline, and SHALL route the case to litigation and then to write-off after the receiver reports (R-DEV-05, R-DEV-15). | CAP-S8-014 | BR-066 | REQ-DVH-009 | Must | 4 |
| FR-S8-038 | The service SHALL run the X6 skip trace through the bureau, the internal data and the agency sources inside its window, and SHALL route the case to escalation or to the route decision when the trace is exhausted (R-DEV-17). | CAP-S8-015 | BR-067 | REQ-S8-004 | Must | 4 |
| FR-S8-039 | The service SHALL file the X7 insurance claim with a person's approval, SHALL request the re-appraisal through the owning service, and SHALL return the case to the route decision (R-DEV-06). | CAP-S8-016 | BR-068 | REQ-S8-005 | Must | 4 |
| FR-S8-040 | The service SHALL put the overrides of the month in front of the review forum with the reason and the outcome of each, read from the decision record and not from a separate count. | CAP-S8-017 | BR-069 | REQ-S8-006 | Must | 4 |
| FR-S8-041 | The service SHALL match a complaint to the contact that preceded it and SHALL hold that reference on the deviation and on the case. | CAP-S8-017 | BR-069 | REQ-DVH-007 | Must | 4 |
| FR-S8-042 | The service SHALL open the breach path where a message went out against a contact stop, with the message, the stop and the role that sent it, and SHALL raise a conduct record. | CAP-S8-017 | BR-069 | REQ-S8-006 | Must | 4 |
| FR-S8-043 | The service SHALL hold the automated processing on a case under a data subject request and SHALL route the request to Compliance inside the statutory period. | CAP-S8-018 | BR-079 | REQ-S8-007 | Must | 4 |
| FR-S8-044 | The service SHALL escalate a deviation that is not resolved inside its service level to the team manager, and SHALL keep the escalation and its date on the deviation (R-DEV-20). | CAP-S8-019 | REQ-DVH-003 | REQ-DVH-003 | Should | 2 |
| FR-S8-045 | The service SHALL read the case, party, stage, queue and timer facts through the rwb-case contract, SHALL join no other schema, and SHALL carry no constraint in `rwb_deviation` that references a table outside it. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-046 | The service SHALL read party flags, deceased and bankrupt markers and the freshness of each data product through the rwb-source-data contract, SHALL read no `recovery.v_ace_*` view and no ACE table, and a direct read SHALL fail the build and the boundary test. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-047 | The service SHALL authorise every action against the capability area held for the role in the permission data cached from rwb-access, SHALL refuse with MSG-P4-002, and SHALL change nothing on a refusal. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-048 | The service SHALL write every flag, route, contact stop, clear and override to the decision record through the decision-record library, and where that record cannot be written SHALL change nothing, SHALL show MSG-P7-003 and SHALL raise an incident. | CAP-S8-005 | REQ-DVH-005 | REQ-DVH-005 | Must | 2 |
| FR-S8-049 | The service SHALL read the code-to-owner map, the contact-stop rules, the service levels, the escalation period, the warning window, the confidence threshold and the skip trace window from versioned reference data, SHALL hold none of them in code, and SHALL apply a change from its valid-from date without a release. | CAP-S8-003 | REQ-DVH-003; RULE-014 | REQ-DVH-003 | Must | 2 |
| FR-S8-050 | The service SHALL state the business date and the load time of every data product behind a screening run and a deviation, and SHALL show a stale product with its date and MSG-P1-001 rather than use it silently. | CAP-S8-007 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-051 | The service SHALL accept an Idempotency-Key on every command, SHALL answer a failure with RFC 9457 problem details, SHALL hold a call to 2 seconds, SHALL retry on a schedule and then move the item to the exception queue with a task for a named owner, and SHALL replay a dead-lettered event. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-052 | The service SHALL keep personal data out of its events, its workflow inputs and its logs, SHALL mask a personal field by role, and SHALL refuse a personal read rather than return it where the access log cannot be written. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-053 | The service SHALL write only schema `rwb_deviation` and SHALL carry its own migration sequence in that schema. | CAP-S8-001 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |
| FR-S8-054 | The service SHALL reach every outside system through the rwb-integration contract or the contract of the service that owns it, and SHALL make no direct call to the fraud system, the bureau, the external flow system, the litigation system, the appraisal system or the partner portal. | CAP-S8-013 | BR-065 | REQ-DVH-010 | Must | 4 |
| FR-S8-055 | The service SHALL produce the deviation measure (closed inside the service level, by code and by handler) from the decision record and the events into rwb-reporting, and SHALL not keep a second count of its own. | CAP-S8-017 | BR-069 | REQ-S8-006 | Must | 4 |
| FR-S8-056 | The service SHALL run the screening agent through the rwb-agent contract with the schema check on every output and the rule fallback, and SHALL record the policy, its version, the segment, the model version and the prompt version with the run. | CAP-S8-008 | REQ-DVH-001 | REQ-DVH-001 | Must | 2 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-S8-001 | The case record view with the deviation flag and the raise screen respond inside the user's wait under the busiest-hour load. | Under 2 seconds at the 95th percentile | NFR-008, NFR-009 | Must | Performance test in SIT |
| NFR-S8-002 | A rule evaluation at a screening run or a raise completes inside the user's wait. | Under 300 milliseconds at the 95th percentile | NFR-011 | Must | Rule timing test with the package in force |
| NFR-S8-003 | The screening agent answers inside its target; after that the rule result is used and the screening run still records its outcome. | Under 60 seconds, then the rule result | NFR-010, NFR-024 | Must | Agent timeout drill |
| NFR-S8-004 | The screening run for the business date completes in time for the case list, which is available on the latest completed ACE batch. | The case list available by 07:00 | NFR-013 | Must | Morning run test in SIT |
| NFR-S8-005 | Every screening run and every deviation states the business date and the load time of the data products it read. | Every run and every deviation | NFR-013 | Must | Data date inspection |
| NFR-S8-006 | A missing, failed or late ACE batch is visible at the screening and on the deviation, and alerts the data steward. | Visible at the decision; alert to the steward | NFR-014 | Must | Hold an ACE batch in SIT |
| NFR-S8-007 | The service holds no load window, no staging table and no catch-up job: a late ACE batch delays the screening and raises an alert. | No load, no staging, no catch-up | NFR-015 | Must | Hold and release the batch |
| NFR-S8-008 | The service carries the stated population and concurrency, and the two evaluation samples the FSD names. | 23,600 open cases at go-live and 26,500 at the end of 2027; 3,110 new accounts a month; about 370 staff online in the busiest hour; about 21 requests a second at peak; samples of 200 and 500 cases for the agent evaluation (ASM-3011) | NFR-001, NFR-002 | Must | Volume test at the stated population |
| NFR-S8-009 | A deviation is worked to the service level in force and escalates when that level is passed. | The service level, the escalation period and the skip trace window as versioned reference data; set with DL22 (GAP-1827; ASM-3005) | NFR-001 | Must | Escalation drill with a level set in reference data |
| NFR-S8-010 | The service is available during business hours and outside them, when a case waits on a paused clock. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-S8-011 | The service inherits the ACE recovery point and recovery time, and a running DeviationWorkflow resumes where it stopped with the pause intact. | The ACE recovery point objective and recovery time objective; workflow history preserved | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-S8-012 | Every deviation is reproducible from the log, and every measure is produced from the log. | Every decision reproducible; measures from the log | NFR-033, NFR-065 | Must | Re-run a sample of deviations from the log |
| NFR-S8-013 | The screening agent runs only at the autonomy level its evidence supports, its output is schema checked on every run with the rule fallback, and a level change needs the approval the policy names. | Schema check on every output; the autonomy policy read from versioned reference data (GAP-1828; ASM-3006) | NFR-055, NFR-078 | Must | Autonomy and schema-check drill |
| NFR-S8-014 | Every action carries the rule version applied and the role that allowed it. | Every action | NFR-034 | Must | Decision record inspection |
| NFR-S8-015 | The decision log hash chain is checked daily and a break is reported to Compliance the same day. | Daily check, same-day report | NFR-035 | Must | Chain break drill |
| NFR-S8-016 | No personal data is carried in an event, a workflow input or a log, and every personal field is masked by role on every screen and every agent call. | Masked at rest and in use; minimisation per screen and per agent | NFR-039, NFR-040 | Must | Masking matrix test across roles; event payload review |
| NFR-S8-017 | The two events are CloudEvents 1.0 through the outbox and the inbox, retried at 1 minute, 10 minutes and 1 hour and then dead-lettered with a replay path, and they carry no personal and no financial value. | Retry three times then the dead-letter topic; replay available (ASM-3010) | NFR-025, NFR-026 | Must | Failure injection and replay |
| NFR-S8-018 | Every read of a personal field is logged, and the read is refused rather than returned where the log cannot be written. | Every read | NFR-042 | Must | Access log reconciliation against reads |
| NFR-S8-019 | Every outbound contact carries a conduct check result, and a contact sent against a block is caught and raised. | Every contact | NFR-038 | Must | Breach path drill |
| NFR-S8-020 | A data subject request is answered inside the statutory period, with automated processing held on the case meanwhile. | Statutory period; not set as a working service level | NFR-043 | Must | Request drill with a held case |
| NFR-S8-021 | No production data is used in development, and user acceptance uses masked copies. | Synthetic in development, masked in user acceptance | NFR-045 | Must | Environment data review |
| NFR-S8-022 | Screen labels, validation messages and error messages served with this service's operations are available in Thai and in English. | Every label and message in Thai and English | NFR-059 | Must | Label and message review |
| NFR-S8-023 | Every record this service holds carries a data classification that sets its handling. | Classification applied per record, on the working scheme of section 8 (GAP-1829; ASM-3007) | NFR-047 | Must | Classification review |
| NFR-S8-024 | Recovery data stays in the bank's own cloud tenancy in the agreed region, and the model endpoint is reached over a private endpoint. | SCB Azure, Southeast Asia; private endpoint | NFR-046, NFR-048 | Must | Tenancy review |
| NFR-S8-025 | Staff authenticate with single sign-on and multi-factor authentication, and the agent runs under a service identity subject to the same role checks. | Entra ID single sign-on with multi-factor; service identities | NFR-049, NFR-051 | Must | Sign-in and identity test |
| NFR-S8-026 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-S8-027 | The build blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency; logs, traces and metrics are produced for the flag, the pause, the route, the clear and the agent, and a failure alerts a named owner. | Pipeline checks pass; alert within 15 minutes to the named owner | NFR-054, NFR-064, NFR-067, NFR-068 | Must | Pipeline run with a seeded violation; alert drill |
| NFR-S8-028 | A production release rolls back by redeploying the previous tag, and the service carries its own migration sequence in schema `rwb_deviation`. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-S8-029 | The two screens and the case record section meet the bank's accessibility standard and work on the browsers the bank supports. | WCAG 2.1 level AA; the current and previous major versions of Microsoft Edge and Google Chrome | NFR-060, NFR-061 | Must | Accessibility scan and browser test |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_deviation`. Every table carries the record columns of the platform library. The Ownership Map fixes one table name for this service, `deviation`; the other four entity groups are named as product entities and their physical names are written with the DB story (GAP-1819; ASM-2997). The record class and the retention period are open (GAP-1829; ASM-3007).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `deviation` (named in the Ownership Map) | Owned record, one per case and code | `case_id` (business key, `varchar(255)`), deviation code (LOV-DEVIATION, X1 to X7), reason, source reference, raised at, raised by (LOV-RAISED-BY), paused state, handler role, contact stop, cleared at, outcome and its coded reason, approver role, rule and package version, decision record reference | [CONFIDENTIAL] | Workbench decision; the case link is read through the P3 contract | Deviation record class; period open |
| screening run (entity group) | Owned record, one per case and event key | Run key `SCREENING:<caseId>:<eventId>`, case reference, trigger (business date ready, document stored, agent run completed), mode (SHADOW or L1), policy and its version, segment, business date, load time per data product, model and prompt version, outcome | [CONFIDENTIAL] | rwb-agent through its contract; documents through P5; call notes and party flags through P1 | Deviation record class; period open |
| screening score (entity group) | Owned record, one per code per scored sample | Sample name and version, code X1 to X7, precision, recall, true positives, false positives, false negatives, sample size | [CONFIDENTIAL] | The comparison the business analyst runs against the sample | Deviation record class; period open |
| contact stop (entity group) | Owned record, one per case and stop | Case reference, code that set it, set at, set by rule and its version, lifted at, lifted by role, lift reason | [CONFIDENTIAL] | This service's own decision | Deviation record class; period open |
| breach record (entity group) | Owned record, one per breach | Case reference, the message that went out, the stop it crossed, the role that sent it, detected at, conduct record reference | [CONFIDENTIAL] | The event from rwb-comms and the conduct check | Deviation record class; period open |
| `outbox_event`, `processed_event`, `idempotency_key` | Platform library objects created in this schema | Library-defined | [CONFIDENTIAL] | Service template | Library policy (PLT; ASM-0074) |

No copy of an ACE column is held, no document and no call-note text is stored, and no foreign key leaves the schema.

## 8.2 Data read but not owned

| Data | Read through | Views behind it | Classification of the data read |
|---|---|---|---|
| Case, party, stage, queue, task and timer facts | rwb-case contract (Temporal activity and REST) | none (case schema) | [PII], [SENSITIVE_FINANCIAL] |
| Party flags, deceased and bankrupt markers | rwb-source-data contract (REST) | the party and account views behind the contract | [PII] |
| Freshness of each data product | rwb-source-data contract (REST) | `v_ace_batch_status` | [CONFIDENTIAL] |
| Call notes for the screening | rwb-source-data contract (REST) — field set open (GAP-1822; ASM-3000) | the interaction data behind the contract | [PII] |
| Documents for the screening and the X1 evidence pack | rwb-document contract | none (document schema) | [PII], [CONFIDENTIAL] |
| Roles, capability areas, masking policy and the delegation table | rwb-access permission data, cached | none (access schema) | [CONFIDENTIAL] |
| Rule packages, the version in force and the autonomy policy | rwb-decision contract and events; rwb-agent contract | none (decision and agent schemas) | [CONFIDENTIAL] |
| LOV-DEVIATION and LOV-RAISED-BY | rwb-case reference-data contract | none (case schema) | [CONFIDENTIAL] |
| The decision record and the hash chain | rwb-decision through the decision-record library and the shared topic | none (decision schema) | [CONFIDENTIAL] |

Counts are not stated: the FSD gives no field count for this module, and no count is recomputed here.

## 8.3 Field-level requirements for personal and financial data

The FSD marks all eight deviation catalog fields as not personal data (A2.8.3.2 and the same table repeated in nine features). The customer data the screening reads is personal data and is handled as such here.

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| deviation.case_id | The case the deviation belongs to | [CONFIDENTIAL] | A business key of type `varchar(255)`; no foreign key; the case is read through the P3 contract |
| deviation.deviation_code | X1 to X7 | [CONFIDENTIAL] | Held as a code from LOV-DEVIATION, never as free text |
| deviation.raised_at, deviation.cleared_at | When it was raised and cleared | [CONFIDENTIAL] | Timestamps used for the service level and the escalation; never in an event payload as anything but a state |
| deviation.raised_by | Screening agent, rule, officer or customer contact | [CONFIDENTIAL] | A code from LOV-RAISED-BY; the raising person's identifier is held by role, not by employee record |
| deviation.paused_state | The routing state the case was in when paused | [CONFIDENTIAL] | The exact state value the case can be returned to (R-DEV-08) |
| deviation.handler_user_id | The named handler | [CONFIDENTIAL] | A staff identifier, not customer personal data; masked from roles outside the owning queue |
| deviation.contact_stop | True when contact is stopped | [CONFIDENTIAL] | The only field an outbound send is refused on; it is a conduct control record |
| deviation.cleared_at | When it cleared | [CONFIDENTIAL] | Present only with the cleared outcome and its reason |
| Call notes and document text read by the screening | The material the agent reads | [PII] | Read through P1 and P5 at run time; no copy is stored; minimised to what the screening needs (NFR-040) |
| Customer name, identification number and contact value, where the case record section shows the party | The party the case belongs to | [PII] | Masked by role; every read logged; never in an event, a workflow input or a log |

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code: the code-to-owner map, the contact-stop rules, the service levels, the escalation period, the prescription warning window, the confidence threshold and the skip trace window (BR-S8-001 to BR-S8-019).
2. This service holds no copy of an ACE column and no staging table; it reads ACE data through the two contracts only (GAP-1816; ASM-2994).
3. No document, no call-note text and no agent prompt is stored in `rwb_deviation`; the screening keeps its codes, its reasons and its source references (GAP-1822; ASM-3000).
4. A link to a case is a business-key column of type `varchar(255)` with no foreign key.
5. A personal field is not returned when the access log cannot be written.
6. The contact stop is a record, not a flag on a person's screen: it is set by rule, lifted only by a clear, and every lift carries its reason and its role (ASM-3007).
7. A deviation record, a screening run and a breach record are retained by record class; the classes are assigned here and the periods are open under DL26 and Q-012.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document. The S8 row of the slide 13 matrix ends at P3 (E), P1 (R and E) and P10 (T and E); every other edge below is marked with the gap it rests on.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| rwb-source-data (P1) | Out and in | REST, one hop, 2 s timeout, GET retried once with jitter | P1 | Party flags, deceased and bankrupt markers, the call-note read and freshness. The only path to ACE data; this service reads no view and no ACE table (GAP-1816; ASM-2994) |
| ACE database, the tables behind the 30 views | Not read | None | ACE team | Read only through the P1 contract. No direct `public` read and no DML from this service |
| rwb-case (P3) | In and out | Temporal child workflow (DeviationWorkflow) and signal; REST for the case and queue read; events published to it | P3 | The case starts the stage and owns the parent workflow, the state, the queues, the tasks and the timers; this service publishes DeviationRaised and DeviationCleared for it |
| rwb-comms (P6) | In and out | Events both ways | P6 | It consumes the two deviation events and holds the sends while a stop is on; it publishes the event that opens the breach path (GAP-1832; ASM-3010) |
| rwb-document (P5) | Out | Contract dependency on the document read | P5 | The documents the screening reads and the X1 evidence pack; no document is copied into this schema (GAP-1822; ASM-3000) |
| rwb-decision (P7) | Out | Decision-record library and the shared decision record topic; rule package and autonomy policy read | P7 | The record, the hash chain, the rule registry and the approval the policy names; the matrix gives S8 no REST cell, so nothing here is a synchronous call (GAP-1820; ASM-2998) |
| rwb-access (P4) | In | Cached permission data through the guard library, not a call on the hot path | P4 | Roles, capability areas and masking policy |
| rwb-agent (P10) | Out and in | Temporal child workflow and activity; event listened to | P10 | The screening agent under its contract, 60 s then the rule result, and the autonomy policy that decides shadow or level 1 (GAP-1828; ASM-3006) |
| rwb-integration (P2) | Out | Contract dependency per the integration contract | P2 | The fraud referral, the bureau and agency skip trace, the claim filing and the insurance claim. The matrix gives S8 no P2 cell, so the carrier is open (GAP-1821; ASM-2999) |
| rwb-asset (S5) and rwb-valuation (S1) | Out | Through the owning service's contract | S5, S1 | The re-appraisal the X7 flow asks for and the route decision the case returns to |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | The raise screen and the deviation queue, and the deviation section of the case record; the composite route joins this service's answer with rwb-case (GAP-1830; ASM-3008) |
| Kafka topic `rwb.deviation.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by case | This service | DeviationRaised (EV-06) to rwb-case, rwb-comms and rwb-treatment; DeviationCleared (EV-07) to rwb-case and rwb-comms (ASM-3010) |
| rwb-reporting (P9) | Out | Events and the decision record | P9 | The deviation measure, the override pattern and the conduct measures; produced from the log, not from a separate count |
| ACE common audit and personal-data logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Which path serves the deviation read for the case record and the queue, given that the Architecture slide records GET /deviations, the Ownership Map records no read at all and the FSD times a read at two seconds? | Solution architect | The case record section and the queue cannot be built, and the failure criterion of AC-EXC-S8-002-02 cannot be tested, until one path wins (GAP-1818; ASM-2996) |
| Which carrier takes the five outside effects: the integration service, or the service that already owns the interface to that system? | Solution architect with the integration lead | Five of the seven X codes cannot leave the bank until the carrier is fixed (GAP-1821; ASM-2999) |
| Does the approval a deviation carries stay a step in DeviationWorkflow, or does it become an approval workflow on rwb-decision with a new matrix cell? | Solution architect with the P7 owner | The approval is a control the FSD asserts and the matrix does not carry (GAP-1820; ASM-2998) |
| Where do the documents and the call notes reach the screening, and who confirms the field sets with P5 and P1? | Solution architect with the P5 and P1 owners | The screening cannot run against a population whose input is unowned (GAP-1822; ASM-3000) |
| Which payload do the two events carry, and does a consumer read the deviation back or take the state from the event? | Solution architect | The contract of the topic and the read operation are decided together (GAP-1832; ASM-3010) |

# 10. Release slicing proposal

The service is wave 2: it is created with Epic 2 (release 31 December 2026 (tentative)). Its three business epics are EP02 and EP03 in wave 2 and EP07 in wave 4, so the service is created with the screening slice and the E7 flows land after it (release 31 May 2027 (tentative)). The service wave (2) and the EP02 and EP03 waves (2) are the same and EP07 is later, so no wave conflict is raised (ASM-3013). Each slice is a list of capabilities, not stories. Every date is copied unchanged and marked (tentative).

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox, inbox and decision-record libraries, the Temporal workflow kit with the child workflow and timer support, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Wave 2 — Epic 2, screening, pause, handling and return (release 31 December 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 The record and the read path | CAP-S8-001, CAP-S8-006 | Nothing can be flagged, paused or counted until the deviation exists with its code, its reason and its state, and the boundary test must fail the build on a direct ACE read from the first story |
| 2.2 The two clocks | CAP-S8-002 | A pause that stops the legal clock is a regulatory failure, and a pause that does not survive a restart is not a pause |
| 2.3 The code-to-owner route | CAP-S8-003, CAP-S8-019 | The exception is only handed over if it reaches a role, and the escalation is what stops it sitting there |
| 2.4 The contact stop | CAP-S8-004 | Contact after a death or a hardship notice is the most serious conduct failure this module prevents |
| 2.5 Clear, resume and re-route | CAP-S8-005, CAP-S8-009 | A case that cannot be released, or that is released while a second deviation is open, is a case worked under a false clock |
| 2.6 Screening in shadow and at level 1 | CAP-S8-007, CAP-S8-008 | The agent must earn its level on a measured sample, and a person must stay in front of every low-confidence flag |

Rationale: the wave-2 slice is the smallest set that delivers the E2 outcome, and each slice is independently demonstrable. CAP-S8-019 is Should and may slip within the wave without holding the release.

## 10.3 Wave 2 — Epic 3, the deceased slice (release 31 January 2027 (tentative))

| Slice | Capabilities | Why it matters here |
|---|---|---|
| 3.1 Death stops the contact and starts the claim | CAP-S8-012 (the contact stop, the notification and the insurance claim path only) | The program requirement on death is tagged E3 and the BRD's Q-015 is open; the conduct control cannot wait for wave 4 (GAP-1825; ASM-3003) |

Rationale: the deceased flow is served twice on purpose. The E3 slice stops contact, tells the heirs and the estate and starts the insurance claim path; the full X3 flow, with its approver and its return point, lands in wave 4 with the other E7 flows.

## 10.4 Wave 4 — Epic 7, the X1 to X7 flows (release 31 May 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 4.1 X1 dispute and complaint | CAP-S8-010 | The most frequent exception, and the one that measures conduct |
| 4.2 X2 vulnerability and hardship | CAP-S8-011 | The contact limits are a regulatory duty that needs its own decision recorded |
| 4.3 X3 deceased, end to end | CAP-S8-012 (the approver, the estate position and the return point) | The E3 slice stops contact; this slice settles the estate position and re-routes |
| 4.4 X4 fraud | CAP-S8-013 | Recovery action against a fraud case destroys evidence |
| 4.5 X5 bankruptcy and seizure | CAP-S8-014 | A missed claim deadline is a debt that can never be recovered |
| 4.6 X6 lost contact and skip trace | CAP-S8-015 | The case must move whether or not contact is restored |
| 4.7 X7 collateral event | CAP-S8-016 | The value and the insurance position both change the route |
| 4.8 Override review, complaint matching and the breach path | CAP-S8-017 | Override and conduct are measurable only if they are collected on purpose |
| 4.9 The data subject request hold | CAP-S8-018 | The statutory period runs whether or not the product is ready for it |

Rationale: the ten E7 features are released as the flows they belong to, each demonstrable on its own, and each builds on the wave-2 record, clock, route and stop. The placeholder criteria of these features are written when their stories are groomed (GAP-1824; ASM-3002).

## 10.5 Later increments

| Increment | What unlocks it |
|---|---|
| The deviation rule package as a governed package | Phase 2 of the Drools design, with the 22 rules, their version label and their owner registered in rwb-decision (GAP-1826; ASM-3004) |
| The autonomy level raised above 1 | The measured evidence and the threshold the model risk officer accepts under Q-014 and BR-084 (GAP-1828; ASM-3006) |
| The table set of the screening run, the score, the stop and the breach record in the Ownership Map | The data architect's list, added with the DB story (GAP-1819; ASM-2997) |
| The service level and the escalation period as set values | DL22 set by the business lead (GAP-1827; ASM-3005) |
| Retention and disposal by record class | DL26 and Q-012 closed (GAP-1829; ASM-3007) |
| Deviation measures at full width | The rwb-reporting read model, fed by the decision record and the events (ADR-018) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one; where the source row asserts the case record view rather than the behaviour it sits under, the gap and the assumption are named next to it (GAP-1823; ASM-3001). Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-S8-001 | FR-S8-001, FR-S8-003, FR-S8-004, FR-S8-045 | a case owned by the complaint officer and the codes of LOV-DEVIATION | the officer raises a deviation with a reason and an evidence reference, then tries a code outside the list and a flag with no reason | one record exists with the code, the reason, the raised-at, the raised-by, the paused state and the source reference, linked to the case by business key with no foreign key; the out-of-list code and the reasonless flag are refused with MSG-GEN-001 and nothing changes | AC-S8-001-01 |
| AC-S8-002 | FR-S8-002, FR-S8-005, FR-S8-006, FR-S8-008 | a case with a running stage timer, a prescription date and facts a rule fires on | the readiness event starts the screening run, and the worker is restarted while the deviation is open | the deviation is raised with the rule and package version; the stage timer pauses and the prescription date is unchanged; the case state is not replaced; after the restart the pause and the paused state are intact | AC-S8-002-01 (source row asserts the case record view); GAP-1823 |
| AC-S8-003 | FR-S8-007, FR-S8-019 | a case with prescription date 2027-02-13, sixty days after the business date, a second case at 2027-03-16, ninety-one days, and a deviation read that does not answer inside 2 seconds | the case record is opened in each case | the first date shows with MSG-P3-003 and the second shows no warning; with the slow read the timers and the prescription date still show, the deviation section shows MSG-GEN-006 naming "Deviation handling", and the on-hold banner shows from the case's own flag | AC-ALT-S8-002-02; AC-EXC-S8-002-02 |
| AC-S8-004 | FR-S8-008, FR-S8-015, FR-S8-016, FR-S8-048 | case RW-2026-000502 with X3 raised on 2026-12-10, paused at state WITH_FCR_OFFICER, with a decision record store that is available and then unavailable | the owner clears the deviation with its outcome and reason, and in a second run the record cannot be written | the case returns to WITH_FCR_OFFICER, or to the route decision where the outcome changes the route; the decision record carries the outcome, the reason, the role and the rule version; where the record cannot be written nothing changes, MSG-P7-003 shows and an incident is raised | AC-ALT-S8-002-01 (state and return point); AC-EXC-S8-006-04 |
| AC-S8-005 | FR-S8-009, FR-S8-010, FR-S8-011 | one case for each code X1 to X7, and a code with no row in the code-to-owner reference data | each deviation is raised | each case reaches the role that owns its code, X3 reaches the specialist with Legal, X7 reaches the agent with a person approving the claim, and the unmapped code reaches the team manager with the unmapped flag recorded and readable per month | AC-S8-004-01 (source row asserts the case record view); GAP-1823 |
| AC-S8-006 | FR-S8-012, FR-S8-013, FR-S8-014, FR-S8-042 | a dispute, a hardship case and a deceased case, each with an outbound letter queued, and a later send made against a stop | the deviation is raised, the stop is set, and a message is sent while it is on | the stop is set and shown with its reason; DeviationRaised is in the outbox keyed by the case; the letter is held; the stop is lifted only on the clear with DeviationCleared; the send against the stop opens the breach path with the message, the stop and the role that sent it | AC-ALT-S8-005-01; AC-EXC-S8-005-02 |
| AC-S8-007 | FR-S8-018, FR-S8-020 | case RW-2026-000502 with X3 raised on 2026-12-10, a handler role, an approval recorded in the decision log entry, paused state WITH_FCR_OFFICER and the contact stop true | the case record and the deviation queue are opened | the record shows "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date, and shows the code, the handler, the approver, the raised date, the return point and "Contact stopped"; the queue lists the deviation by code, handler and age | AC-ALT-S8-002-01 |
| AC-S8-008 | FR-S8-021, FR-S8-022 | 200 cases with their call notes and documents, and a document event that arrives twice | the agent runs, then the same event ID arrives again | each run stores its proposed codes with reasons and source references in mode SHADOW; no deviation record exists, deviation_open stays false on every case, no contact stop is set and no user-facing operation returns a proposal; the repeat creates no second run and is counted | AC-S8-001-01; AC-EXC-S8-001-01 |
| AC-S8-009 | FR-S8-023, FR-S8-024 | the analyst flags for the same 200 cases in sample SCREEN-S1 version 1, and open case RW-2026-000401 receiving a DEATH_CERTIFICATE | the comparison runs, and the stored document event is processed | one score row per code X1 to X7 holds precision, recall and sample size 200, and for X6 with 18 true positives, 2 false positives and 6 false negatives the row holds 0.9000 and 0.7500; one shadow run exists with key SCREENING:<caseId>:<eventId> and trigger DocumentStored | AC-ALT-S8-001-01; AC-ALT-S8-001-02 |
| AC-S8-010 | FR-S8-025, FR-S8-026, FR-S8-027 | mortgage case RW-2027-000801 in region BKK with a complaint note dated 2027-01-26, and hire purchase case RW-2027-000802 in region BKK | the agent runs and the owner confirms X1 on the first case | the panel shows X1 with its reasons, the preceding contact and the "Agent output" marker; the confirmation raises X1 with raised_by SCREENING_AGENT under R-DEV-01, the case becomes "On hold", and the feedback holds ACCEPTED with the decision record reference; the second case stays in shadow and returns no screening output | AC-ALT-S8-007-01; AC-ALT-S8-007-02 |
| AC-S8-011 | FR-S8-017, FR-S8-028, FR-S8-048 | a flag below the confidence threshold, and a decision record store that rejects every write | the reviewer rejects the flag with a reason, and in a second run the write fails | nothing on the case changes before a person acts; the rejection is recorded as an override with its reason; on the failed write the request is refused with 503 and MSG-P7-003 and no feedback row exists | AC-EXC-S8-007-01; AC-S8-008-01 |
| AC-S8-012 | FR-S8-029, FR-S8-030 | one case with an open X1 and an open X3, each with its own owner and stop | one of the two is cleared | the case stays paused and shows both, and it resumes only when both are cleared | AC-S8-009-01 (source row asserts the case record view); GAP-1823 |
| AC-S8-013 | FR-S8-031, FR-S8-032 | an X1 case with its documents and a complaint still inside its service level | the officer assembles the pack and records the resolution | the pack reference is held on the deviation, the resolution carries its reason and rule version, and the case returns to the same decision with its timers resumed and the service level result recorded | AC-S8-010-01 (source row reads "Written one epic ahead"); GAP-1824 |
| AC-S8-014 | FR-S8-033, FR-S8-034, FR-S8-035 | an X2 case with its contact limits, and an X3 case in which the insurance does not clear the position | each flow runs | X2 records the limits, the specialist queue and the hardship or relief decision with its rule version; X3 stops contact, records the notification to the heirs and the estate, starts the claim, and returns the case to the route decision against the estate | AC-S8-011-01 and AC-S8-012-01 (source rows read "Written one epic ahead"); GAP-1824 |
| AC-S8-015 | FR-S8-036, FR-S8-037 | an X4 case with a confirmed fraud flag, and an X5 case with a claim deadline inside its window | each flow runs | recovery action is held for as long as the fraud flag stands, the inquiry is tracked and the case routes on the outcome; the X5 case stops direct collection, records the filing before the deadline, and routes to litigation and then to write-off after the receiver reports | AC-S8-013-01 and AC-S8-014-01 (source rows read "Written one epic ahead"); GAP-1824 |
| AC-S8-016 | FR-S8-038, FR-S8-039 | an X6 case whose skip trace is exhausted, and an X7 case with a collateral event | each flow runs | the skip trace runs inside its window and the case routes to escalation or to the route decision; the X7 claim is filed only with a person's approval, the re-appraisal is requested through its owner, and the case returns to the route decision | AC-S8-015-01 and AC-S8-016-01 (source rows read "Written one epic ahead"); GAP-1824 |
| AC-S8-017 | FR-S8-040, FR-S8-041 | a month of overrides with their reasons, and a complaint with a known preceding contact | the review runs and the complaint is worked | the forum sees every override with its reason and its outcome, read from the decision record and not from a separate count; the complaint carries its preceding contact reference on the deviation and on the case | AC-S8-017-01 and AC-S8-018-01 (source rows read "Written one epic ahead"); GAP-1824 |
| AC-S8-018 | FR-S8-043 | a case under a data subject request with automated processing running | the request is received | the automated processing on the case is held, the hold is visible on the case, and the request reaches Compliance inside the statutory period | NFR-043; AC-S8-019-01 (source row reads "Written one epic ahead"); GAP-1824 |
| AC-S8-019 | FR-S8-044 | a deviation open past the service level held in reference data | the clock passes the level | the deviation escalates to the team manager, and the escalation and its date are on the deviation | R-DEV-20; Temporal and Drools Design slides 8 and 24; GAP-1827 |
| AC-S8-020 | FR-S8-045, FR-S8-046, FR-S8-047 | a branch that reads a `recovery.v_ace_*` view directly, a schema constraint that references an ACE table, and a user without the capability area | the pipeline and the boundary test run, and the user tries a raise and a clear | the build fails naming the view read and the cross-schema constraint; the boundary test passes with no ACE object in this schema; both actions are refused with MSG-P4-002 and nothing changes | Arch v5 slides 12, 13 and 45; AC-EXC-S8-004-02; GAP-1816 |
| AC-S8-021 | FR-S8-049, FR-S8-050, FR-S8-055 | a code-to-owner row changed in reference data, one data product STALE at the business date, and a month of closed deviations | the screening runs and the measure is read | the new owner applies from its valid-from date with no release; the stale product is shown with its date and MSG-P1-001 and the run records the business date and load time it used; the measure is read from the decision record and the events with no separate count | VR-S8-001-1; MSG-P1-001; NFR-065 |
| AC-S8-022 | FR-S8-051, FR-S8-052, FR-S8-053 | a command repeated with the same Idempotency-Key, a consumer that is down when an event is published, and a personal field read by a role without the mask | the command is retried, the consumer recovers, and the read is attempted | one effect exists for the repeated command; the event is retried at 1 minute, 10 minutes and 1 hour and then dead-lettered and replayed; the payload carries no personal and no financial value; the read is refused where the access log cannot be written; every object is in schema `rwb_deviation` | NFR-025, NFR-026, NFR-039, NFR-042 |
| AC-S8-023 | FR-S8-054, FR-S8-056 | the agent does not answer inside 60 seconds and a second answer fails the schema check, and an outside effect is triggered | the screening runs and the referral is made | the rule result is used and the run still records its outcome; the policy, the segment, the model version and the prompt version are recorded with the run; the outside effect leaves through a contract with its fake and never by a direct call | NFR-010, NFR-024, NFR-055; GAP-1821 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| REQ-DVH-001 | CAP-S8-001, CAP-S8-007, CAP-S8-008 | FR-S8-001, FR-S8-002, FR-S8-003, FR-S8-004, FR-S8-021, FR-S8-022, FR-S8-023, FR-S8-024, FR-S8-025, FR-S8-026, FR-S8-027, FR-S8-028, FR-S8-045, FR-S8-046, FR-S8-047, FR-S8-050, FR-S8-051, FR-S8-052, FR-S8-053, FR-S8-056 | NFR-S8-001, NFR-S8-002, NFR-S8-003, NFR-S8-005, NFR-S8-006, NFR-S8-007, NFR-S8-013, NFR-S8-016, NFR-S8-018, NFR-S8-027 | AC-S8-001, AC-S8-002, AC-S8-008, AC-S8-009, AC-S8-010, AC-S8-020, AC-S8-021, AC-S8-022, AC-S8-023 |
| REQ-DVH-002; RULE-012 | CAP-S8-002 | FR-S8-005, FR-S8-006, FR-S8-007, FR-S8-008 | NFR-S8-010, NFR-S8-011 | AC-S8-002, AC-S8-003 |
| REQ-DVH-003; RULE-014 | CAP-S8-003, CAP-S8-019 | FR-S8-009, FR-S8-010, FR-S8-011, FR-S8-044, FR-S8-049 | NFR-S8-009, NFR-S8-014 | AC-S8-005, AC-S8-019, AC-S8-021 |
| REQ-DVH-004; RULE-013 | CAP-S8-004 | FR-S8-012, FR-S8-013, FR-S8-014 | NFR-S8-016, NFR-S8-017, NFR-S8-019 | AC-S8-006 |
| REQ-DVH-005 | CAP-S8-005, CAP-S8-009 | FR-S8-008, FR-S8-015, FR-S8-016, FR-S8-017, FR-S8-029, FR-S8-030, FR-S8-048 | NFR-S8-012, NFR-S8-014, NFR-S8-015 | AC-S8-004, AC-S8-011, AC-S8-012 |
| REQ-DVH-006 | CAP-S8-006, CAP-S8-008 | FR-S8-018, FR-S8-019, FR-S8-020, FR-S8-028 | NFR-S8-001, NFR-S8-022, NFR-S8-029 | AC-S8-003, AC-S8-007, AC-S8-011 |
| REQ-DVH-007 | CAP-S8-017 | FR-S8-041 | NFR-S8-019 | AC-S8-017 |
| REQ-DVH-008 (E3; BR-064 in E7) | CAP-S8-012 | FR-S8-034, FR-S8-035 | NFR-S8-016, NFR-S8-019 | AC-S8-014 |
| REQ-DVH-009; BR-066 | CAP-S8-014 | FR-S8-037, FR-S8-054 | NFR-S8-017, NFR-S8-019 | AC-S8-015, AC-S8-023 |
| REQ-DVH-010; BR-065 | CAP-S8-013 | FR-S8-036, FR-S8-054 | NFR-S8-013, NFR-S8-017 | AC-S8-015, AC-S8-023 |
| REQ-DVH-011 (E7) | CAP-S8-010 to CAP-S8-017 | FR-S8-031 to FR-S8-042 | NFR-S8-009, NFR-S8-012, NFR-S8-019 | AC-S8-013 to AC-S8-018 |
| REQ-S8-001; BR-062 | CAP-S8-010 | FR-S8-031, FR-S8-032 | NFR-S8-009, NFR-S8-012 | AC-S8-013 |
| REQ-S8-002; BR-063 | CAP-S8-011 | FR-S8-033 | NFR-S8-009, NFR-S8-019 | AC-S8-014 |
| REQ-S8-003; BR-062 | CAP-S8-010 | FR-S8-032 | NFR-S8-009 | AC-S8-013 |
| REQ-S8-004; BR-067 | CAP-S8-015 | FR-S8-038, FR-S8-054 | NFR-S8-009, NFR-S8-017 | AC-S8-016 |
| REQ-S8-005; BR-068 | CAP-S8-016 | FR-S8-039, FR-S8-054 | NFR-S8-009, NFR-S8-017 | AC-S8-016 |
| REQ-S8-006; BR-069 | CAP-S8-017, CAP-S8-019 | FR-S8-040, FR-S8-042, FR-S8-044, FR-S8-055 | NFR-S8-009, NFR-S8-012, NFR-S8-019 | AC-S8-017, AC-S8-019, AC-S8-021 |
| REQ-S8-007; BR-079 | CAP-S8-018 | FR-S8-043 | NFR-S8-020 | AC-S8-018 |

BR coverage: 11 of the 11 program requirements of this module (REQ-DVH-001 to REQ-DVH-011), 7 of the 7 program requirements of the E7 set (REQ-S8-001 to REQ-S8-007) and 9 of the 9 BRD requirements that name this service (BR-062 to BR-069 and BR-079) are covered by at least one functional requirement. BR-069 covers two program requirements (REQ-DVH-007 and REQ-S8-006) and BR-062 covers two (REQ-S8-001 and REQ-S8-003), which is why the row count is higher than the requirement count. REQ-DVH-008 has one program requirement and one BRD requirement with two different epics, and is carried as an open question with its two release slices (GAP-1825; ASM-3003). No requirement of this module is left without a functional requirement, and no functional requirement lacks a source requirement (ASM-3014).

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Boundary and conformance test output in system test | FR-S8-045, FR-S8-046, NFR-S8-027 | Developer with the security administrator |
| Contract test against the source-data, case, document and agent contracts and their fakes | FR-S8-011, FR-S8-024, FR-S8-031, FR-S8-045, FR-S8-046, FR-S8-056 | Developer with P1, P3, P5 and P10 |
| Pause and resume drill with a worker restart, and a prescription date across the pause | FR-S8-005, FR-S8-006, FR-S8-007, FR-S8-008, NFR-S8-011 | QA team |
| Contact stop drill across three channels and a send made against a stop | FR-S8-012, FR-S8-014, FR-S8-042, NFR-S8-019 | Conduct and QA officer with the QA team |
| Code-to-owner matrix test for X1 to X7 and an unmapped code | FR-S8-009, FR-S8-010, FR-S8-044 | Center of excellence analyst with the QA team |
| Shadow run on 200 cases and a scored sample of 500, with the score rows read back | FR-S8-021, FR-S8-022, FR-S8-023, NFR-S8-008 | Risk and model risk officer with the QA team |
| Level 1 run on one segment, with a confirmation, a rejection and a failed decision record write | FR-S8-025, FR-S8-026, FR-S8-027, FR-S8-028, NFR-S8-013 | Conduct and QA officer with the model risk officer |
| Two-deviation case and a resume that waits for both | FR-S8-029, FR-S8-030 | Case owner with the QA team |
| X1 to X7 flow test per code, at wave 4, with its approver and its return point | FR-S8-031 to FR-S8-042 | Business analyst, S8 with the QA team |
| Decision reproducibility, the override review and the measure read | FR-S8-040, FR-S8-055, NFR-S8-012, NFR-S8-014 | Internal audit with the center of excellence analyst |
| Masking matrix, access log reconciliation and classification review | NFR-S8-016, NFR-S8-018, NFR-S8-023 | Compliance and PDPA officer |
| Failure injection: retry, exception queue, dead-letter and replay | FR-S8-051, NFR-S8-017 | QA team |
| Performance test at the stated population, and the morning run before 07:00 | NFR-S8-001, NFR-S8-004, NFR-S8-008 | QA team |

# 12. Open questions

The FSD's and the BRD's open items are carried forward with their IDs where they have one. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-S8-01 | Which operation serves the deviation read that the case record and the queue need, and is the raise path `/deviations`, `/cases/{caseId}/deviations` or both? | Solution architect | Before the S8 contract story closes | CAP-S8-006, CAP-S8-007, CAP-S8-008 | GAP-1818; ASM-2996; Arch v5 slide 15; Ownership Map Endpoints |
| OQ-S8-02 | Which tables hold the screening run, the screening score, the contact stop and the breach record in schema `rwb_deviation`, given that the Ownership Map lists `deviation` only? | Data architect | Before the S8 DB story | CAP-S8-004, CAP-S8-007, CAP-S8-017 | GAP-1819; ASM-2997 |
| OQ-S8-03 | Is the approval a deviation carries a step in DeviationWorkflow, or an approval workflow on rwb-decision with a new matrix cell? | Solution architect with the P7 owner | Before wave 2 system test | CAP-S8-005, CAP-S8-012 | GAP-1820; ASM-2998; AC-ALT-S8-002-01 |
| OQ-S8-04 | Which carrier takes the fraud referral, the bureau and agency skip trace, the claim filing, the insurance claim and the re-appraisal, given that the S8 row has no rwb-integration cell? | Solution architect with the integration lead | Before wave 4 system test | CAP-S8-013, CAP-S8-014, CAP-S8-015, CAP-S8-016 | GAP-1821; ASM-2999; DP-16 |
| OQ-S8-05 | Which epic owns the deceased customer flow: E3 for REQ-DVH-008 or E7 for FEAT-DVF-03 and RWB-E7-003? | Product Owner | Before the E3 release | CAP-S8-012 | GAP-1825; ASM-3003; BRD Q-015; ASM-022 |
| OQ-S8-06 | What is the deviation service level, the escalation period and the skip trace window (DL22)? | Business lead | Before wave 2 release | CAP-S8-002, CAP-S8-019, CAP-S8-015 | GAP-1827; ASM-3005; BRD Q-003; DL22 |
| OQ-S8-07 | What confidence threshold sends a flag to a person, and what measured evidence earns level 1 on a segment? | Risk and model risk officer | Before the level 1 run | CAP-S8-007, CAP-S8-008 | GAP-1828; ASM-3006; BRD Q-014; BR-084 |
| OQ-S8-08 | What classification and what retention period apply to the deviation record, the screening run and the breach record (DL26)? | Compliance and PDPA officer | Before wave 2 release | CAP-S8-001, CAP-S8-007, CAP-S8-017 | GAP-1829; ASM-3007; BRD Q-012; DL26 |
| OQ-S8-09 | Which service owns the raise screen and the deviation queue, and where does the composite route sit at the edge? | Solution architect | Before wave 2 release | CAP-S8-006, CAP-S8-007 | GAP-1830; ASM-3008; DP-19 |
| OQ-S8-10 | Who approves the Thai and English wording of the eight messages this service shows (DL10)? | Business analyst, S8 | Before wave 2 release | All messages | GAP-1831; ASM-3009; DL10; NFR-059 |
| OQ-S8-11 | What payload do DeviationRaised and DeviationCleared carry, and does a consumer read the deviation back or take the state from the event? | Solution architect | Before wave 2 system test | CAP-S8-004, CAP-S8-005, CAP-S8-006 | GAP-1832; ASM-3010; EV-06, EV-07 |
| OQ-S8-12 | Who owns the deviation rule package, when does it move out of Phase 2, and which ten of the 22 R-DEV rules does the package carry? | Center of excellence analyst with P7 | Before wave 2 system test | CAP-S8-001, CAP-S8-003, CAP-S8-019 | GAP-1826; ASM-3004; DP-04 |
| OQ-S8-13 | Which fields of the call notes and of the documents does the screening read, and which owner publishes them? | Solution architect with the P1 and P5 owners | Before the shadow screening test | CAP-S8-007, CAP-S8-008 | GAP-1822; ASM-3000 |
| OQ-S8-14 | Do the seven E2 features keep the case-record criterion as their only main success flow, or does the FSD owner rewrite each one against the behaviour it carries? | Business analyst, S8 with the QA lead | Before wave 2 system test | CAP-S8-001 to CAP-S8-009 | GAP-1823; ASM-3001 |
| OQ-S8-15 | Who writes the acceptance criteria of the ten E7 features that read "Written one epic ahead"? | Business analyst, S8 with the QA lead | Before wave 4 system test | CAP-S8-010 to CAP-S8-018 | GAP-1824; ASM-3002 |
| OQ-S8-16 | What is the deviation rate at go-live, and therefore the volume the screening run and the queue are sized for? | Solution architect | Before the wave 2 volume test | CAP-S8-007, CAP-S8-008, CAP-S8-019 | GAP-1833; ASM-3011 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (ASM-3012).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v5 | 5.15 (S8 requirements, REQ-DVH-001 to REQ-DVH-011 and REQ-S8-001 to REQ-S8-007), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan and the requirement-to-service table), 9 (open decisions incl. DL10, DL22, DL26), 10.1 and 10.2 (the service epic RWB-SVC-S8, schema, wave and business epics) |
| Recovery Workbench Business Requirements Epic 2 v3 | 3 (the three deviation stories and the case record view), the E2 requirement list (REQ-DVH-001 to REQ-DVH-010, REQ-OCC-010), 8.1 (service epics), the story-to-service table |
| Recovery Workbench Business Requirements Epics 3 to 8 v1 | 8.5 (E7 deviations and partners, BR-062 to BR-069), 8.8 (BR-079), 9 (RULE-012 to RULE-014, RULE-027), 10 (measures), 11.1 to 11.4 (ASM-004, ASM-022, DEP-009, RISK-006), 12 (Q-003, Q-012, Q-014, Q-015), 13 (governance) |
| Recovery Workbench FSD S8 Deviation handling v3 | Document control, Existing capability check, A1 (context, scope, dependencies, feature overview, preconditions), A2.1 to A2.19 (functional decomposition with field catalog, rules, roles and acceptance criteria), Requirements served (18 requirements), Screens (SCR-06, SCR-08), Appendix A and B |
| Recovery Workbench Architecture v5 | Slides 3 (the eight routes and the deviation as always-on), 4 (19 modules), 9 to 13 (call types, timeouts, retry, the connection matrix incl. the S8 row), 14 to 20 (service contracts, incl. slide 15 for S8), 25 (one case workflow with a child per stage), 30 (19 schemas), 31 (the morning run and the readiness event), 32 (the bank scheduler at the edges), 33 (busy times), 41 (service catalogue), 42 and 43 (event catalogue, EV-06 and EV-07), 44 (job map), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Slide 8 (the X3 example, the signal and the two clocks), slide 13 (DeviationWorkflow on its own queue), slide 24 (the S8 flow, the 22 rule route set, the escalation after 10 working days, the skip trace window, the Phase 2 package note) |
| Recovery Workbench Microservice Ownership Map v1 | Services (S8 row: wave 2, schema, REST base, topic, queue), Tables (`deviation`), Endpoints (POST /cases/{caseId}/deviations, PATCH /deviations/{deviationId}), Events (EV-06, EV-07), Workflows and activities (DeviationWorkflow), Jobs (no S8 row), Parameters and Rulings |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic), 4 (partner access) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R5 (target structure, DP table, wave map), R8 (outputs), R9 (gaps and assumptions) |
| _work/msr/plan/split_plan.json | stats (1,034 slices, 358 legacy keys) and legacy (disposition and wave of the S8 stories RWB-E1-062, RWB-E2-015, RWB-E2-029 and RWB-E7-001 to RWB-E7-010) |
| _work/msr/plan/ids.json | D-RCV-60 and the allocated ADR-013 to ADR-023 and DL44 to DL49; this document introduces no new decision and cites them as inherited |
