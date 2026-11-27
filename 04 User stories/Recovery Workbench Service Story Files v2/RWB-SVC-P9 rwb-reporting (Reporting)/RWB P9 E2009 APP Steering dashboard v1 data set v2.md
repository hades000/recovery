# RWB-P9-E2009-APP Steering dashboard v1 data set

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E2009-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P9-E2009-APP-16); the squad sizes at refinement |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P9-A |
| Ready to start | After RWB-P9-E1013-APP |
| Depends on (build) | RWB-P9-E2009-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P9-E1013-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P10-E1063-CON |
| Contract version | v1 (REST base /api/recovery/reporting/v1) |
| Integration dependencies | None |
| External dependencies | RWB-P9-E2009-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (FR-P9-007, FR-P9-009, FR-P9-010, FR-P9-011, FR-P9-012, FR-P9-027) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E2-009 for rwb-reporting — the seven steering calculators over the event-derived read model, the case-list reconciliation that holds a publish, `measure_publish` in `rwb_reporting`, the local record of each publish decision, the scheduled run JOB-15 and `GET /reports/measures` behind SCR-37 — is split from the published shapes (RWB-P9-E2009-CON) and from the deployment of the build (RWB-P9-E2009-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P9-E2009-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 32 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Tribe lead (RW-TRIBE)**, I want **a data set for the steering dashboard with cases by stage, queue and age, decisions logged, treatments, letters sent and agent acceptance, published each morning and reconciled to the case list**, so that **the steering committee reads the same numbers the teams work with**.

Inside rwb-reporting this is the steering half of RWB-E2-009:

- service `rwb-reporting`, schema `rwb_reporting`, REST base `/api/recovery/reporting/v1`, topic `rwb.reporting.events.v1` with event names `rwb.reporting.<Event>.v1`, Temporal task queue `rwb-reporting` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.reporting` (R4, DP-13);
- JOB-15 as the Temporal Schedule `reportingMeasuresDaily` at 01:30 on queue `rwb-reporting`, with no Quartz row and no Spring Batch descriptor (DP-10);
- the read model built from events — `CaseCreated` (EV-01), `CaseAllocated` (EV-02), `CaseStateChanged` (EV-05), `DecisionRecorded` (EV-08), `TreatmentApproved` (EV-10), `NoticeDispatched` (EV-14), `AgentRunCompleted` (EV-28) — plus the agent contract RWB-P10-E1063-CON for acceptance and override, and no data lake anywhere (DP-17);
- the publish or hold of the business date, recorded on `measure_publish` — the table RWB-P9-E1013-APP creates — through the same publish recorder, in the service's own schema (DP-01, DP-15);
- one local decision record per business date — published or held — written before the snapshot rows and relayed on `rwb.decision-record.v1` (DP-03);
- the case facts of the business date and the count of open cases at the cut-off, read on the rwb-case contract that RWB-P3-E1013-APP declares with the same run (DP-11);
- the lists of the measures — LOV-PRODUCT, LOV-MEASURE-UNIT, LOV-MEASURE-DIM, LOV-DATA-PRODUCT and LOV-MEASURE-PUBLISH — on the reference-data contract of rwb-case (DP-07);
- `GET /reports/measures` on the per-service base, served to SCR-37 through the gateway-bff composite route (DP-19).

Not here: the published shapes and the fakes (RWB-P9-E2009-CON); the deployment, the topics, the alerts and the runbook (RWB-P9-E2009-OPS); the measure set and JOB-15's first build of RWB-E1-013 (RWB-P9-E1013-APP); the queue and service-level measures of RWB-E1-030 and RWB-E2-011; the agent monitoring dashboard with latency and cost of RWB-E2-031; benefit realisation of FEAT-RPT-06; regulatory returns of FEAT-RPT-07.

### 2. Business rationale

The steering committee receives numbers counted by hand that differ from the numbers the teams see in their queues. RWB-E2-009 adds the steering measures to the nightly measure set, holds the publish when the dashboard case count differs from the case list, and serves the values to SCR-37. It serves REQ-WKM-009 and REQ-WKM-006, NFR-065, NFR-066 and the zero tolerance of DL25.

The legacy story reaches its facts through six in-process interfaces and puts its extract in a data lake. Under D-RCV-60 four things move:

- **the facts become events.** rwb-reporting builds its read model from the events of P3, S2, P6, P7 and P10 instead of calling their Java interfaces, and the agent rates come from the agent contract RWB-P10-E1063-CON (DP-17, DP-11).
- **the lake is gone.** INT-19 and INT-20 are removed; the same snapshot rows that serve SCR-37 feed the Power BI refresh through the extract hand-over, so the screen and the report cannot disagree (DP-17).
- **the scheduler is gone.** JOB-15 is a Temporal Schedule on this service's queue, and a rerun is a workflow-level action, not a second job (DP-10).
- **the row is written here, first.** The publish or hold decision is a local decision record committed in the same transaction as `measure_publish` (DP-03), which is what legacy AC9 and BR5 ask for.

### 3. Preconditions

- RWB-P9-E2009-CON is tagged `v1` as the delta of this key on the parent baseline of RWB-P9-E1013-CON: `baselineValue` on `Measure`, the fixing of `dimension`, the four consumed declarations and the extract hand-over activity, the eight subscriptions, the registration contract of JOB-15, the message map and the fakes.
- RWB-P9-E1013-APP is done: `measure_definition`, `measure_snapshot` and `measure_publish` exist, the measure set runs at 01:30, the publish recorder and the frozen baseline of 2026-11-27 stand, and the steering calculators extend the same measure set.
- RWB-PLT-E1027-CON (local record), RWB-PLT-E1043-CON (reference-data client), RWB-PLT-E1071-CON (Schedule and workflow kit), RWB-PLT-E1044-CON (Flyway sequence and drift gate) and RWB-PLT-N001-CON (gateway-bff composite route) are published.
- RWB-P3-E1043-CON serves LOV-PRODUCT, LOV-MEASURE-UNIT, LOV-MEASURE-DIM, LOV-DATA-PRODUCT and LOV-MEASURE-PUBLISH, and RWB-P10-E1063-CON serves the runs of an agent and version for a business date.
- Definition version "MD-2026.12" is loaded and approved by the Tribe lead: the seven steering measures of the legacy `Background`, with the reconciliation tolerance of zero (DL25). The version is a data row; no measure code is a constant.
- The legacy story's five fact interfaces (`CaseReportingApi`, `DecisionLogApi`, `TreatmentApi`, `NoticeApi`, `AgentMonitorApi`) have no target operation names and no published payloads; each fact arrives on an event or on a contract named here, with the placeholder where the field list is not fixed (GAP-2576; ASM-4243).
- The service runs as login `rwb_reporting` on schema `rwb_reporting`, holds no grant on another `rwb_*` schema, and reads no `v_ace_*` view: reporting data arrives on events and contracts only (DP-01, DP-17).
- `rwb.reporting.steering` is the feature flag of the platform library; off means the run writes its record, holds the business date and publishes nothing.

### 4. Flow

1. The Schedule `reportingMeasuresDaily` opens one workflow execution per business date D at 01:30, with the execution id derived from D so a rerun joins the run (DP-10).
2. `checkFreshness` reuses the freshness gate of RWB-P9-E1013-APP and asks rwb-source-data for the data products of D; a source that is not fresh leaves the freshness stamp at its own date and raises MSG-P1-001 (DP-17).
3. `loadReadModel` replays the events of D from `rwb.case.events.v1`, `rwb.treatment.events.v1`, `rwb.comms.events.v1`, `rwb.decision-record.v1` and `rwb.agent.events.v1` into the run-scoped fact view of the workflow, deduplicated on the event id and ordered per case by the sequence of the outbox (DP-17).
4. `loadAgentFacts` reads the runs of every agent and version for D on RWB-P10-E1063-CON: recommendations, accepted, overridden with a reason, and the version of each run (DP-11).
5. `computeMeasures` runs the seven calculators — CASES_BY_STAGE, CASES_BY_QUEUE_AGE, DECISIONS_LOGGED, TREATMENTS, LETTERS_SENT, AGENT_ACCEPTANCE, AGENT_OVERRIDE — over the fact view and writes one candidate row set per measure, product, dimension and value, with the definition version in force.
6. `reconcileCounts` sums CASES_BY_STAGE at the cut-off of D, reads the case facts of D on `GET /api/recovery/case/v1/cases/facts` — the read RWB-P3-E1013-APP declares — and counts the open cases of the same cut-off, with the product filter optional (DP-11).
7. Where the two counts are equal, the transaction writes one local decision record with the outcome PUBLISHED, writes the snapshot rows with their `published_at`, writes the publish row of the business date as PUBLISHED with the two counts and no held reason through the recorder of RWB-P9-E1013-APP, and hands the extract over (DP-03, DP-01).
8. Where they differ, the transaction writes the record with the outcome HELD, writes the publish row as HELD with both counts and the held reason, writes no snapshot row and publishes no extract, and raises MSG-P9-002 to the Reporting and BI analyst and the data steward (BR2).
9. `handOverExtract` hands the published day's extract to rwb-integration as an activity on its queue, with the business date as its freshness stamp; INT-19, the data lake load area, is not used (DP-17).
10. `GET /reports/measures` answers the published rows on `/api/recovery/reporting/v1`: filtered by measure, product, route and period, with the scope of the role applied, the business date and freshness stamp in `X-Data-As-Of`, and each value beside its baseline value of 2026-11-27 (DP-13).
11. A rate whose denominator is zero — an agent and version with no run in D — writes no AGENT_ACCEPTANCE row; the screen shows "No runs" for that pair (BR6).
12. The run closes with its summary — measures written, the two counts, the publish status, the extract hand-over — and the visibility view of the workflow kit shows it to the Reporting and BI analyst; the rerun of the same business date replays the same execution and writes the same values (AC9).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Dashboard case count differs from the case list | The record and `measure_publish` are written as HELD, the previous day stays the latest published, and both counts are named | MSG-P9-002 | AC4, BR2 |
| X2 | A source load for the business date is stale | The measure is written from the last complete day, with that date as its freshness stamp | MSG-P1-001 | AC5, BR4 |
| X3 | A query with `from` after `to` | Refused before any read, with the two field names | MSG-GEN-003 | AC6 |
| X4 | An agent and version has no run in the day | No rate row is written and the screen shows "No runs" for that pair | None | AC7, BR6 |
| X5 | JOB-15 is rerun for a published business date | The rows are replaced with the same values, the frozen baseline of 2026-11-27 is untouched, and one record is added | None | AC9, BR13 |
| X6 | The role lacks Reporting R | The read is refused and nothing changes | MSG-P4-002 | TC-E2-009-10, BR7, AC10 |
| X7 | The local decision record cannot be written | The transaction writes nothing: no snapshot row, no `measure_publish`, no extract | MSG-P7-003 | BR12, AC11 |
| X8 | The case-facts contract does not answer inside 2 s, or its breaker is open | `reconcileCounts` retries on the workflow policy; the day stays unpublished rather than published unverified | None | BR9, AC12 |
| X9 | The extract hand-over to rwb-integration fails | The snapshot rows stand as published, the extract is retried from the run, and the reporting analyst is alerted | MSG-GEN-006 | BR10, AC13 |
| X10 | A component, a statement or a test reaches another service's schema, a `v_ace_*` view or the data lake | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17, AC14 |

X1 to X5 are the exception paths of RWB-E2-009 carried onto the split; X6 to X10 are the paths the microservice adds. The tolerance is zero (DL25), so no path publishes a day whose counts differ; no path writes a measure code, a formula, an age band or a tolerance as a constant.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts after RWB-P9-E1013-APP against RWB-P9-E2009-CON, the platform contracts and the rwb-case, rwb-reports and agent contract fakes, on its own schema, with no live neighbour |
| Negotiable | The workflow, activity and consumer-group names, the run-fact view and the run summary are this story's choice; the measures, messages, statuses and field sets are fixed |
| Valuable | One set of numbers for the committee and the teams, and a day that cannot be published while the counts disagree |
| Estimable | One Schedule, one workflow, six activities, seven calculators, one reconciliation check, one row, one read and four consumed contracts |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic day built from event fixtures and contract fakes with known answers |

### 7. Acceptance criteria

```gherkin
Feature: Steering dashboard v1 data set

  Background:
    Given definition version "MD-2026.12" is in force with measures "CASES_BY_STAGE", "CASES_BY_QUEUE_AGE", "DECISIONS_LOGGED", "TREATMENTS", "LETTERS_SENT", "AGENT_ACCEPTANCE" and "AGENT_OVERRIDE"
    Given the synthetic day 2026-12-15 holds 240 open cases, 1,412 decision record entries, 38 treatments and 95 notices sent

  Scenario: AC1 Refresh (legacy RWB-E2-009 AC1)
    Given the rwb-source-data contract mock returns the loads of business date 2026-12-15 with their checks passed
    Given the loads of business date 2026-12-15 passed their checks
    When JOB-15 runs at 01:30 on 2026-12-16
    Then GET /reports/measures?from=2026-12-15&to=2026-12-15 returns a value for each measure of the published set with period "2026-12-15"
    Then the INT-19 extract for 2026-12-15 has freshness stamp 2026-12-15 for the 07:30 Power BI refresh

  Scenario: AC2 Reconciles (legacy RWB-E2-009 AC2)
    Given the rwb-case contract mock returns 240 open cases at the 2026-12-15 cut-off
    Given the case list shows 240 open cases at the 2026-12-15 cut-off
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the sum of "CASES_BY_STAGE" for 2026-12-15 is 240
    Then "DECISIONS_LOGGED" for 2026-12-15 is 1,412, the count of decision record entries decided that day

  Scenario: AC3 Agent measures (legacy RWB-E2-009 AC3)
    Given the rwb-agent contract mock returns 200 recommendations, 170 accepted and 30 overridden for "case-intake" "1.2.0" on 2026-12-15
    Given agent "case-intake" version "1.2.0" made 200 recommendations on 2026-12-15, of which 170 were accepted and 30 overridden with a reason
    When JOB-15 runs at 01:30 on 2026-12-16
    Then "AGENT_ACCEPTANCE" for "case-intake" "1.2.0" on 2026-12-15 is 85.0 percent
    Then "AGENT_OVERRIDE" for "case-intake" "1.2.0" on 2026-12-15 is 15.0 percent
    Then SCR-37 shows both rates by agent

  Scenario: AC4 Counts do not match (legacy RWB-E2-009 AC4)
    Given the rwb-case contract mock returns 240 open cases at the 2026-12-15 cut-off
    Given the case facts read for the dashboard total 239
    Given the case list shows 240 open cases at the 2026-12-15 cut-off
    When JOB-15 runs at 01:30 on 2026-12-16
    Then no snapshot rows and no extract are published for 2026-12-15
    Then SCR-37 shows 2026-12-14 as the latest day with MSG-P9-002 naming 239, 240 and 2026-12-15
    Then an alert goes to the Reporting and BI analyst and the data steward

  Scenario: AC5 Stale source (legacy RWB-E2-009 AC5)
    Given the rwb-comms event mock returns the notice data product of 2026-12-14 for business date 2026-12-15
    Given the notice data product is from 2026-12-14 because the 2026-12-15 load has not arrived
    When a product head opens SCR-37 on 2026-12-16
    Then "LETTERS_SENT" shows the value for 2026-12-14
    Then SCR-37 shows MSG-P1-001 naming "DP07 Legal" and 2026-12-14

  Scenario: AC6 Dates in the wrong order (legacy RWB-E2-009 AC6)
    Given a team manager holds RW-TEAMMGR with Reporting R
    When a team manager sends GET /reports/measures?from=2026-12-15&to=2026-12-01
    Then the response is status 422 with MSG-GEN-003 naming "from" and "to"

  Scenario: AC7 Agent with no runs (legacy RWB-E2-009 AC7)
    Given the rwb-agent contract mock returns no recommendations for "deviation-screen" "0.9.0" on 2026-12-15
    Given agent "deviation-screen" version "0.9.0" made no recommendations on 2026-12-15
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the system writes no "AGENT_ACCEPTANCE" value for "deviation-screen" on 2026-12-15
    Then SCR-37 shows "No runs" for "deviation-screen" on 2026-12-15

  Scenario: AC8 Filter by product (legacy RWB-E2-009 AC8)
    Given the rwb-case contract mock returns 140 open Mortgage cases at the 2026-12-15 cut-off
    Given the measures for 2026-12-15 are published and the case list shows 140 open Mortgage cases at the cut-off
    When a product head sends GET /reports/measures?measure=CASES_BY_STAGE&product=MORTGAGE&from=2026-12-15&to=2026-12-15
    Then the response holds only rows with product "MORTGAGE"
    Then their sum is 140

  Scenario: AC9 Rerun of a published day (legacy RWB-E2-009 AC9)
    Given the measures for 2026-12-15 are published
    When JOB-15 is rerun for business date 2026-12-15 from SCR-44
    Then the rows for 2026-12-15 hold the same values
    Then the frozen baseline rows of 2026-11-27 are unchanged

  Scenario: AC10 Role lacks Reporting R (exception X6; BR7) (new, D-RCV-60)
    Given a role holds no Reporting R
    When a caller holding that role sends GET /reports/measures?measure=CASES_BY_STAGE&from=2026-12-15&to=2026-12-15
    Then the read is refused with MSG-P4-002 and nothing changes

  Scenario: AC11 Decision record cannot be written (exception X7; BR12) (new, D-RCV-60)
    Given the local decision record cannot be written for the publish of 2026-12-15
    When JOB-15 runs at 01:30 on 2026-12-16
    Then no snapshot row, no "measure_publish" row and no extract are written for 2026-12-15
    Then MSG-P7-003 is raised and nothing is changed

  Scenario: AC12 Case-facts read unanswered (exception X8; BR9) (new, D-RCV-60)
    Given the rwb-case contract mock does not answer inside 2 s for the 2026-12-15 cut-off
    When JOB-15 runs at 01:30 on 2026-12-16
    Then "reconcileCounts" retries on the workflow policy
    Then 2026-12-15 stays unpublished with no snapshot rows and no extract

  Scenario: AC13 Extract hand-over fails (exception X9; BR10) (new, D-RCV-60)
    Given the hand-over of the 2026-12-15 extract to rwb-integration fails
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the snapshot rows for 2026-12-15 stand as published
    Then the extract is retried from the run and the reporting analyst is alerted

  Scenario: AC14 Reach into another schema (exception X10; BR8) (new, D-RCV-60)
    Given a component issues a statement that reaches another service's schema or a "v_ace_*" view
    When the boundary test runs in the build
    Then the grant refuses the statement and the boundary test fails the build

  Scenario: AC15 Measure rows are data (BR11) (new, D-RCV-60)
    Given "CASES_BY_STAGE" is held in measure_definition with definition_version "MD-2026.12"
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the value for "CASES_BY_STAGE" is computed from its definition row
    Then no measure code, formula, unit, age band, data product or publish status is written as a constant

  Scenario: AC16 Same business date twice (BR13) (new, D-RCV-60)
    Given the measures for 2026-12-15 are published
    When JOB-15 runs twice for business date 2026-12-15 with the same execution id
    Then the rows for 2026-12-15 hold the same values once
    Then 2026-12-15 is published once

  Scenario: AC17 Error answers of the provided operations (added by D-RCV-60) (new, D-RCV-60)
    Given a caller holds no valid credential for GET /reports/measures
    When the caller sends GET /reports/measures?from=2026-12-15&to=2026-12-15
    Then the response is status 401
    Given a caller holds a credential but no Reporting R
    When the caller sends GET /reports/measures?from=2026-12-15&to=2026-12-15
    Then the response is status 403
    Given a caller asks for a path the contract does not provide
    When the caller sends that request
    Then the response is status 404

  Scenario: AC18 Duplicate delivery of a consumed event (added by D-RCV-60) (new, D-RCV-60)
    Given an event consumed from the rwb-source-data contract is delivered a second time
    When the event is consumed again
    Then the rows for the business date hold the same values once

  Scenario: AC19 Activity retried or timed out (added by D-RCV-60) (new, D-RCV-60)
    Given an activity of JOB-15 does not complete inside its timeout
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the activity is retried on the workflow policy
    Then no snapshot rows are published for the business date until the activity completes

  Scenario: AC20 Consumed call fails or does not answer (added by D-RCV-60) (new, D-RCV-60)
    Given a consumed contract call returns an error or does not answer
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the business date stays unpublished with no snapshot rows and no extract

  Scenario: AC21 Status change the model does not allow (added by D-RCV-60) (new, D-RCV-60)
    Given a status change that the model does not allow is requested
    When the change is sent to the service
    Then the change is refused and nothing is changed
```

The nine criteria are those of RWB-E2-009, copied word for word with the origin tag added to the `Scenario` line: the repeated `Then`, the legacy names "JOB-15", "case list", "data product" and "the INT-19 extract" all stand. Seven carry one added line because the fact behind the `Given` comes from another service: the rwb-source-data freshness of AC1, the rwb-case case list of AC2, AC4 and AC8, the rwb-agent runs of AC3 and AC7, and the rwb-comms notice data product of AC5. Where the legacy text says the decision log entry, this build means the local decision record of DP-03 and reads each criterion with that meaning; JOB-15 is the scheduled run of this build; where it says the data lake or INT-19, this build hands the extract to rwb-integration and keeps the freshness stamp (GAP-2576; ASM-4245); where it says SCR-37, the screen reaches the service through the gateway-bff composite route (DP-19). The test cases of section 16 are the ten legacy ones.

AC10 to AC14 cover the exception paths X6 to X10 that the microservice adds, and AC15 and AC16 cover the business rules BR11 and BR13, which no criterion covered before. AC17 to AC21 cover the provided-operation errors, a redelivered event, a retried or timed-out activity, a failed consumed call and a disallowed status change, which no criterion covered before.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Steering measures are computed from Workbench records and the decision log, never from a separate count | NFR-065; REQ-WKM-009 |
| BR2 | The dashboard case count equals the case list count at the same cut-off, or the publish is held | REQ-WKM-006; DL25 (tolerance zero) |
| BR3 | Agent acceptance is accepted recommendations over all recommendations, and override is overridden over all, per agent and version | NFR-066; DF-DEC-007, DF-DEC-013 |
| BR4 | A measure is shown with its business date and freshness stamp; stale data shows its date | MSG-P1-001 rule; FEAT-RPT-08 |
| BR5 | Each value is shown beside the frozen baseline of 2026-11-27 | REQ-WKM-009; RWB-E1-013 BR2 |
| BR6 | A rate with no runs in the denominator is not computed | NFR-066 |
| BR7 | Every query applies the role's scope | CTL-09 |
| BR8 | The facts of a measure arrive on events; no measure reads another service's table and none reads an ACE view | DP-01, DP-17 |
| BR9 | The comparison is made against the case facts of the same cut-off read on the P3 contract; an unanswered read is never treated as a match | DP-11; legacy BR2 |
| BR10 | The published day's snapshot rows are the single source of both SCR-37 and the Power BI extract | Legacy guardrail 4; DP-17 |
| BR11 | Measure code, formula, unit, age band, data product and the publish status are data rows with a version, never constants | Principle 1; DP-07 |
| BR12 | The record, the snapshot rows and `measure_publish` commit together or not at all; a failed record write changes nothing and answers MSG-P7-003 | DP-03; legacy AC9 |
| BR13 | The same business date twice writes the same values once and publishes once; the execution id and the business-date key carry the rule | Legacy AC9; DP-10 |

### 9. State transitions

None of a case: RWB-E2-009 says so and this slice keeps it. The states here are the publish state of a business date and the execution state of the run.

| From (`measure_publish.status`) | Event | Condition | To |
|---|---|---|---|
| Not existing | The run completes and the two counts are equal | BR2 holds for the cut-off | PUBLISHED, with the snapshot rows and the extract hand-over |
| Not existing | The run completes and the two counts differ | BR2 fails by any amount | HELD, with both counts and the held reason; no snapshot row |
| HELD | A later run of the same date | The counts now agree | PUBLISHED; the HELD row is replaced and the record is kept |
| PUBLISHED | A rerun of the same date | AC9, X5 | Unchanged values; `published_at` refreshed by the run |

The values of `measure_publish.status` are LOV-MEASURE-PUBLISH (PUBLISHED, HELD) of TSD P9 T3.2; this story writes both and nothing else. The run states are those of the workflow kit: Running, Completed, Failed.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery service identity of rwb-reporting (`rwb_reporting`) | Opens the Schedule run, loads the facts, computes the measures, reconciles, writes the record, the snapshots and `measure_publish`, and hands the extract over; holds no grant on another `rwb_*` schema |
| The rwb-access authorisation check | Authorises each read of `GET /reports/measures` against the caller's Reporting R and scope before any data is read (BR7) |
| The local decision-record library (RWB-PLT-E1027-CON) | Writes the publish or held record in the caller's transaction and publishes `DecisionRecorded` on `rwb.decision-record.v1` (DP-03) |
| The reference-data client (RWB-PLT-E1043-CON) | Serves the five lists of the measures from RWB-P3-E1043-CON with their version (DP-07) |
| RW-TRIBE, Tribe lead and squad members | Reads SCR-37 and the measures (Reporting R); approves the steering definitions |
| RW-PRODHEAD, product head | Reads SCR-37 (Reporting R) |
| RW-TEAMMGR, team manager | Reads SCR-37 for teams in scope (Reporting R) |
| RW-BIANAL, Reporting and BI analyst | Builds the Power BI report, receives the hold and extract alerts, and reruns a business date from the visibility view (Reporting CRUD) |
| RW-DATASTEW, data steward | Receives the hold alert and reads the reconciliation (Reporting CRU) |
| RW-FINANCE, Finance and CFO delegate | Reads SCR-37 (Reporting R) |
| RW-REFADM, reference data administrator | Loads the steering definitions (Reference data C) |

The rights are the rows of TSD P9 T6.1 and of the legacy authority table, and nothing wider. No person is named: every duty is a role.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, DF-CAS-003, DF-CAS-005, DF-CAS-006, DF-CAS-008, DF-CAS-010, DF-CAS-013 | `recovery_case` (P3) | id, product_group, status, stage_code, route_code, queue_id, entry_date | Read on the read model of EV-01 and EV-05; never as a table |
| DF-WRK-002 | `queue` (P3) | queue_code | Read on the read model of EV-02 |
| DF-TRT-004, DF-TRT-013 | `treatment` (S2) | treatment_type, outcome | Read on the read model of EV-10 |
| DF-LEG-018, DF-LEG-019, DF-LEG-022 | `notice` (P6) | notice_type, sent_date, delivery_status | Read on the read model of EV-14 and EV-15; never as a table |
| DF-DEC-003, DF-DEC-007, DF-DEC-012, DF-DEC-013, DF-DEC-016 | `decision_log_entry` (P7) | decision_code, agent_version, final_call, override_reason, decided_at | Read on the read model of EV-08 and EV-28 |
| DF-RPT-032, DF-RPT-034, DF-RPT-035, DF-RPT-037 | `measure_definition` (P9) | measure_code, formula, data_product, definition_version | Read |
| DF-RPT-042, DF-RPT-043, DF-RPT-044, DF-RPT-045, DF-RPT-046, DF-RPT-047, DF-RPT-048, DF-RPT-049, DF-RPT-052 | `measure_snapshot` (P9) | measure_code, definition_version, business_date, product_group, dimension_code, dimension_value, value, case_count, published_at | Write |
| DF-RPT-054, DF-RPT-055, DF-RPT-056, DF-RPT-057, DF-RPT-058 | `measure_publish` (P9) | business_date, status, case_list_count, dashboard_count, held_reason | Write, this story's own row |

Field IDs are those of the Logical Data Model and Data Dictionary and of TSD P9 T3.1. The three tables are the parent baseline of RWB-P9-E1013-CON (DF-RPT-031 to DF-RPT-058); this key adds no column and no table, only the steering reconciliation of the publish row and the index of the snapshot by measure, date and product. `decision_record` is a library object created in `rwb_reporting` by the library's own migration (DP-03, DP-15); it is not an entity of LDM v9 and has no row in Data Classification v5, so it is named here as a library object only; no other table is added, and no fact table is created for the read model, which lives for the duration of the run (GAP-2576; ASM-4243). No migration of the monolith is reused (GAP-2576; ASM-4247). No personal data is written: identifiers, codes, counts, rates, amounts, dates and a definition version only. The INT-19 extract and the Power BI data set are not part of this slice (GAP-3088; GAP-2576): the freshness stamp stays on the answer for the SCR-37 refresh, and the measure resources are read through gateway-bff (GAP-1662).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-reporting (P9), base `/api/recovery/reporting/v1` (DP-13). The published shape, the error model and the fakes are RWB-P9-E2009-CON; this story supplies the behaviour.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/reports/measures` | API-P9-001: a list of `Measure` — measure, product, route, period, value, dimension, baselineValue — filtered by `measure`, `product`, `route`, `from` and `to`, with `X-Data-As-Of` | Reporting, right R, scope applied | Not applicable |

The ownership row of the service carries this one operation and this story publishes none other. The legacy path `monolith-base/reports/measures` moves to the per-service base and keeps its operation path (DP-13).

#### 12.2 REST operations consumed

| Operation | Base / contract | Owner | Use |
|---|---|---|---|
| The case facts of a business date (API-P3-001 as RWB-P3-E1013-APP declares it) | `/api/recovery/case/v1` | P3 rwb-case | `GET /cases/facts` with the as-of time and the row count; the open cases at the cut-off give the case-list count of BR2 for AC2, AC4 and AC8; faked |
| The runs of an agent and version for a business date (name Not specified in the source documents (GAP-2576; ASM-4244)) | RWB-P10-E1063-CON | P10 rwb-agent | recommendations, accepted, overridden, latency and version for AGENT_ACCEPTANCE and AGENT_OVERRIDE; faked (GAP-2576; ASM-4246) |
| The freshness of the data products of a business date (the read RWB-P1-E1013-APP declares) | `/api/recovery/source-data/v1` | P1 rwb-source-data | `GET /data-products/freshness` with the product and its date; reused from the gate of RWB-P9-E1013-APP; faked |
| LOV-PRODUCT, LOV-MEASURE-UNIT, LOV-MEASURE-DIM, LOV-DATA-PRODUCT, LOV-MEASURE-PUBLISH | RWB-P3-E1043-CON | P3 rwb-case | the lists of the measures and of the publish status, with their version; faked |
| The extract hand-over of a published day (name and file shape Not specified in the source documents (GAP-2576; ASM-4245)) | activity on the rwb-integration queue, P2 | P2 rwb-integration | the INT-19 replacement for the 07:30 Power BI refresh; faked |

Every REST row is one hop with a 2 s timeout, a single GET retry with jitter and a breaker per downstream (DP-11, ADR-020). The case-facts and freshness reads are the ones the parent slice already calls, and neither sits in this story's C column, which carries the reference-data and agent contracts only: the row is declared from those stories and the same gap is recorded in RWB-P9-E1013-APP (GAP-2576; ASM-4243). The activity row runs on the owner's queue and returns its answer to the workflow.

#### 12.3 Events published

| Event | Topic | Trigger | Payload used |
|---|---|---|---|
| `DecisionRecorded` (EV-08), the local record of a publish or hold | `rwb.decision-record.v1`, owned by rwb-decision | The publish transaction commits | the record id, the business date, the decision code and the outcome; no measure value |

The ownership rows of the service carry no event of its own, so `rwb.reporting.events.v1` exists with its `.retry` and `.dlt` topics and this story publishes nothing of it. `DecisionRecorded` is written by the local library to this service's outbox on the shared topic (DP-03).

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When | Owner service |
|---|---|---|---|---|---|
| `CaseCreated` (EV-01), `CaseStateChanged` (EV-05) | `rwb.case.events.v1` | `rwb-reporting.case.v1` | the case id, product group, stage, route, queue and business date; CASES_BY_STAGE and CASES_BY_QUEUE_AGE | replayed for the business date of the run | P3 (rwb-case) |
| `CaseAllocated` (EV-02) | `rwb.case.events.v1` | `rwb-reporting.case.v1` | the queue and the owner of a case; CASES_BY_QUEUE_AGE | as above | P3 (rwb-case) |
| `DecisionRecorded` (EV-08) | `rwb.decision-record.v1` | `rwb-reporting.decision.v1` | the decision code, the agent version, the final call, the override reason and the time; DECISIONS_LOGGED, AGENT_OVERRIDE | as above | P7 |
| `TreatmentApproved` (EV-10) | `rwb.treatment.events.v1` | `rwb-reporting.treatment.v1` | the treatment id, case and terms; TREATMENTS | as above | S2 |
| `NoticeDispatched` (EV-14), `NoticeDelivered` (EV-15) | `rwb.comms.events.v1` | `rwb-reporting.notice.v1` | the notice id, case, type and sent date; LETTERS_SENT | as above | P6 (rwb-comms) |
| `AgentRunCompleted` (EV-28) | `rwb.agent.events.v1` | `rwb-reporting.agent.v1` | the run id, agent, case, outcome and fallback; the agent rates, with RWB-P10-E1063-CON as the contract of record | as above | P10 (rwb-agent) |

The consumer groups are declared once by RWB-P9-E2009-CON and registered by RWB-P9-E2009-OPS. The run replays a bounded window — the business date and the look-back the age bands need — rather than consuming continuously, so no read-model table is needed; a repeat is deduplicated on the event id (GAP-2576; ASM-4243).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `reportingMeasuresDaily` (JOB-15; name Not specified in the source documents (GAP-2576; ASM-4244)) | Workflow, one execution per business date, started by the Schedule | `rwb-reporting`, namespace `rwb-recovery` | input: the business date; the execution id is derived from the date, so a rerun joins the run |
| `checkFreshness` | Activity | `rwb-reporting` | the freshness gate of RWB-P9-E1013-APP for the data products of the day; the stamps out, or MSG-P1-001 |
| `loadReadModel` | Activity | `rwb-reporting` | the events of the day in; the run-scoped fact view out, deduplicated on the event id |
| `loadAgentFacts` | Activity | `rwb-reporting` | the runs of every agent and version on RWB-P10-E1063-CON |
| `computeMeasures` | Activity | `rwb-reporting` | the seven candidate row sets with the definition version in force |
| `reconcileCounts` | Activity | `rwb-reporting` | the dashboard sum and the case-list count of the same cut-off in; the outcome and the two counts out |
| `publishDay` | Activity | `rwb-reporting` | the one transaction: the record, the snapshot rows, `measure_publish` and the extract hand-over |

The names are this story's design choice: the sources name JOB-15 at 01:30 and no source names the workflow or its activities (GAP-2576; ASM-4244).

#### 12.6 Schedules

| Schedule | Workflow | Queue | Cadence | Overlap and catch-up |
|---|---|---|---|---|
| `reportingMeasuresDaily` (JOB-15) | `reportingMeasuresDaily` for the previous business date | `rwb-reporting` | 01:30 on each business day, replacing the Quartz row (DP-10) | one execution per business date; a late start catches up the missed dates one by one; a rerun joins the existing execution (values as environment values) |

The bank's Airflow edge runs the ACE ingestion and may trigger the same workflow by its start signal; it calls no schema and no operator edits a row to force a publish. No other Schedule belongs to this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `measure_definition` | P9 (`rwb_reporting`) | The definition in force per measure and version; read only here (RWB-P9-E1013-APP is its writer) |
| `measure_snapshot` | P9 (`rwb_reporting`) | One row per measure, business date, product and dimension value; written here; the baseline rows of 2026-11-27 are frozen and never rewritten |
| `measure_publish` | P9 (`rwb_reporting`) | The publish state of a business date: status, both counts and the held reason; written here through the recorder of RWB-P9-E1013-APP, one row per business date |
| `decision_record` | PLT library, created in `rwb_reporting` | One local record per publish decision (DP-03) |

Never read as a table: `recovery_case`, `queue`, `assignment` and `timer` (P3), the treatment record (S2), `notification` (P6), `decision_log_entry` (P7), the agent run records (P10) and every `v_ace_*` view. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-reporting OpenAPI fake | `GET /reports/measures` with the seven measures of 2026-12-15, the product filter, the baseline beside each value and `X-Data-As-Of`; a 422 on a reversed period and a 403 without Reporting R | AC1, AC6, AC8, TC-E2-009-10 |
| Event fixtures of EV-01, EV-02, EV-05, EV-08, EV-10, EV-14 and EV-28 | the synthetic day 2026-12-15: 240 open cases, 1,412 decisions, 38 treatments and 95 notices, plus the notice day of 2026-12-14 | AC1 to AC5, AC7 |
| rwb-case count fake | 240 open cases at the 2026-12-15 cut-off, 140 Mortgage cases, and 239 case facts for the mismatch of AC4 | AC2, AC4, AC8 |
| rwb-case facts fake | the case facts of 2026-12-15 with 240 open cases at the cut-off, 140 Mortgage cases, and a row set whose open count is 239 for the mismatch of AC4 | AC2, AC4, AC8 |
| rwb-agent runs fake | 200 recommendations, 170 accepted and 30 overridden for "case-intake" "1.2.0"; no run for "deviation-screen" "0.9.0" | AC3, AC7 |
| rwb-comms notice fake | the notice data product of 2026-12-14 for the business date 2026-12-15, and MSG-P1-001 for "DP07 Legal" | AC5 |
| rwb-source-data freshness fake | the data products of 2026-12-15 fresh, and a notice product that is not fresh | AC1, AC5, X2 |
| rwb-integration hand-over fake | an accepted extract for 2026-12-15 with its freshness stamp, and a failed hand-over | AC1, X9 |
| Reference-data fake | the five lists of TSD P9 T3.2 with one version | AC1, AC8 |
| Local decision-record stub | a healthy chain returning the sequence and the entry hash, and a stopped chain returning MSG-P7-003 | X7 |
| gateway-bff composite route fake | the merged SCR-37 answer, with the measures read once and the hold or stale message of the latest day | AC3, AC4, AC5, AC7 |

The fakes are test-only and are replaced by the real services in SIT. The consumed operation names are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2576; ASM-4244).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `/reports/measures` on `/api/recovery/reporting/v1`; the case facts, the agent runs, the data-product freshness and the reference-data lists; one hop, 2 s |
| Kafka | 1 published by the library, 8 consumed | `DecisionRecorded` on `rwb.decision-record.v1`; EV-01, EV-02, EV-05, EV-08, EV-10, EV-14, EV-15 and EV-28 replayed for the business date; no event of the service's own |
| Temporal | 1 workflow, 6 activities, 1 Schedule | `reportingMeasuresDaily` on `rwb-reporting` at 01:30, with the extract hand-over activity on the rwb-integration queue |
| File | 1 out | the published day's extract, handed to rwb-integration for the Power BI refresh; no file is read |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.reporting`, module `steering`; front end `src/modules/recovery/reporting/SteeringDashboard.tsx`, the fragment SCR-37 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>`, recovery schema | Owner's schema `rwb_reporting`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed; reporting from events into rwb-reporting | none; the extract of AC1 is a gap and is handed to rwb-integration |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-17 is the largest change of this key: the legacy INT-19 extract has no lake to land in, so the published rows are the single source of the screen and the Power BI refresh, and the hand-over goes through rwb-integration. The agent facts of DP-04, DP-05 and DP-09 do not apply here: no package is evaluated, no ACE view is read and no domain event is published.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `reportingMeasuresDaily` | Workflow | JOB-15: the run of one business date, its steps, its summary and its rerun |
| `SteeringCalculators` | Service | one calculator per steering measure code, driven by the definition rows |
| `CountReconciliation` | Service | BR2 before publish; writes the outcome into `measure_publish` and the record |
| `MeasureController` | Controller | `GET /reports/measures` with the filters, the scope and `X-Data-As-Of` |
| `MeasureQueryRepository` | Repository | reads the published `measure_snapshot` rows by filter |
| `ExtractHandover` | Client | the P2 activity that hands the published day's extract over |
| `SteeringDashboard` | React component | SCR-37: filters by product, route and date; value beside baseline; agent rates; freshness and hold messages |

**Build steps.** (1) Take the CON delta on the parent baseline and the snapshot index of the key; test the keys and the `baselineValue` field. (2) Build the event fixtures and `loadReadModel`; test the counts of AC1 and AC2. (3) Build `SteeringCalculators` and `loadAgentFacts`; test the values of AC3, the percentage rule of BR3 and the no-run case of AC7. (4) Build `CountReconciliation` and `publishDay`; test AC4, AC9 and the record of BR12. (5) Build `MeasureController` with the date check, the scope and the header; test AC6 and AC8. (6) Build the SCR-37 fragment and the stale and hold messages; test AC5 in the browser. (7) Wire `checkFreshness` and `ExtractHandover`; test X2 and X9. **Done when** the tests of section 16 pass and the Power BI report and SCR-37 show the same values for one SIT day.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P9-002 | The dashboard count differs from the case list | The case count on the dashboard ({count}) does not match the case list ({listCount}) for {date}. The publish is held. |
| MSG-P1-001 | A source is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-003 | Dates in the wrong order | {field} cannot be before {other}. |
| MSG-P4-002 | The role lacks Reporting R | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The local record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | The system named is unavailable | {system} is not available. Your request is queued and will be retried. |

The first four texts are the legacy texts of RWB-E2-009 section 14, unchanged; the last two are the platform texts the split adds. A message names a measure code, a product, a count and a date, and never a case, an account or a customer value.

### 15. Screens and states

SCR-37 Steering dashboard (capability area Reporting) is served through the gateway-bff composite route (DP-19):

| State | What the user sees and does |
|---|---|
| Loading | Skeleton rows while `GET /reports/measures` returns |
| Filtered | Values for the chosen product, route and dates, each beside the baseline of 2026-11-27, with the business date; agent rates by agent and version; MSG-P9-002 or MSG-P1-001 when the latest day is held or stale |
| No runs | "No runs" for an agent and version with no recommendation in the day, and no rate |
| Empty | Not specified in the source documents (CG-ALL-7841) |
| No access | Not specified in the source documents (CG-ALL-7841) |
| Error | MSG-P4-002, MSG-GEN-003 or MSG-GEN-006 with its field names and no partial value |

The screen builds no number of its own: it renders the published rows and their stamps. SCR-44 shows the run summary from the workflow visibility query. SCR-44 states: empty, loading, error and no access are each Not specified in the source documents (CG-ALL-7842).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-009-01 | AC1, BR1, BR4 | End to end | Synthetic day 2026-12-15 |
| TC-E2-009-02 | AC2, BR1, BR2 | Component | 240 open cases; 1,412 decision record entries |
| TC-E2-009-03 | AC3, BR3 | Component | case-intake 1.2.0: 200 recommendations, 170 accepted, 30 overridden |
| TC-E2-009-04 | AC4, BR2 | Component | Case list 240, case facts 239 |
| TC-E2-009-05 | AC5, BR4 | Component | Notice product dated 2026-12-14 |
| TC-E2-009-06 | AC6 | Contract | from 2026-12-15, to 2026-12-01 |
| TC-E2-009-07 | AC7, BR6 | Component | deviation-screen 0.9.0 with no runs |
| TC-E2-009-08 | AC8, BR7 | Component | Filter MORTGAGE |
| TC-E2-009-09 | AC9, BR5 | End to end | JOB-15 rerun for 2026-12-15 |
| TC-E2-009-10 | Access | Contract | PT-LAWFIRM calls GET /reports/measures; refused with MSG-P4-002 |
| TC-E2-009-11 | Tables of section 12.7 | Component | Not specified in the source documents (DOR-RWB-P9-E2009-APP-12) |
| TC-E2-009-12 | AC17 | Contract | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC16) |
| TC-E2-009-13 | AC18 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC17) |
| TC-E2-009-14 | AC19 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC18) |
| TC-E2-009-15 | AC20 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC19) |
| TC-E2-009-16 | AC21 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC20) |
| TC-E2-009-17 | AC10 | Contract | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC10) |
| TC-E2-009-18 | AC11 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC11) |
| TC-E2-009-19 | AC12 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC12) |
| TC-E2-009-20 | AC13 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC13) |
| TC-E2-009-21 | AC14 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC14) |
| TC-E2-009-22 | AC15 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC15) |
| TC-E2-009-23 | AC16 | Component | Not specified in the source documents (NEWAC-RWB-P9-E2009-APP-AC16) |

The ten are the legacy test cases of RWB-E2-009, with the legacy Level "System" mapped to the levels of the template and the legacy Level "Access" mapped to Contract; the full Given, When and Then stay in Recovery Workbench Test Cases v8.xlsx under the same ID. TC-E2-009-10 carries no acceptance criterion of its own and is kept because it tests the access refusal of the operation this story publishes. TC-E2-009-11 is new in this story, has no legacy source and tests the tables of section 12.7. Integration copies of these IDs end in `-ITG` and belong to RWB-ITG-E2009-ITG.

### 17. Guardrails

- No business value in code: measures, formulas, units, age bands, the tolerance and the publish status are data rows with a version; the LOV values are reference data of RWB-P3-E1043-CON.
- No personal data in logs, tests, workflow history, events or prompts: measures carry counts, rates, amounts and codes only, and agent outputs are counted, never copied.
- No read of another service's tables and no ACE view: every fact arrives on an event or on its owner's contract (DP-01, DP-17).
- Counts on SCR-37 and in the Power BI extract come from the same `measure_snapshot` rows of a published business date.
- A day is never published on an unanswered case-list count, and an operator never edits `measure_publish` to force a publish.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-009 | Steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-OCC-12, FEAT-RPT-03, FEAT-RPT-08 | 15 Manage performance, data and AI | None; NFR-065 and NFR-066 apply | TC-E2-009-01, TC-E2-009-03, TC-E2-009-05, TC-E2-009-06, TC-E2-009-07, TC-E2-009-09, TC-E2-009-10 |
| REQ-WKM-006 | Queue counts and ageing reported daily and reconciled to the case list | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-RPT-08 | 15 Manage performance, data and AI | None; DL25 applies | TC-E2-009-02, TC-E2-009-04, TC-E2-009-08 |

The nine criteria and the ten test cases of RWB-E2-009 are all owned by this story; nothing of the key is left unowned. The interface INT-19 that AC1 names is removed under DP-17 and its requirement row stays in the RTM against the legacy key, with the replacement stated in section 12.2 (GAP-2576; ASM-4245). Open decision DL25 applies to REQ-WKM-006 and is still open; its assumptions are ASM-0728, ASM-0735, ASM-0743 and ASM-2602.

### 19. Out of scope

- Queue measures and service level breaches for team managers (RWB-E1-030, RWB-E2-011).
- The agent monitoring dashboard with latency and cost (RWB-E2-031).
- Benefit realisation against the baseline (FEAT-RPT-06, Epic 6).
- Regulatory returns (FEAT-RPT-07, Epic 8).
- The baseline measure set, `measure_definition` and `measure_snapshot` of RWB-E1-013 (RWB-P9-E1013-APP) and their shapes (RWB-P9-E1013-CON).
- The published shapes and the fakes of this key (RWB-P9-E2009-CON) and the deployment of the build (RWB-P9-E2009-OPS).
