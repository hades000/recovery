# RWB-ITG-E2009-ITG Steering dashboard v1 data set

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2009-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E2009-ITG-16); the squad sizes it at refinement |
| Depends on (build) | RWB-P10-E1063-APP, RWB-P9-E2009-APP, RWB-P3-E2009-APP, RWB-S8-E2009-APP (not built yet) |
| Contract dependencies | RWB-P9-E2009-CON |
| Contract version | v1 (the /v1 path), as stated by RWB-P9-E2009-CON |
| Integration dependencies | RWB-P10-E1063-APP, RWB-P9-E2009-APP, RWB-P3-E2009-APP, RWB-S8-E2009-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-WKM-009, REQ-WKM-006) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-009 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 22 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness for the steering dashboard v1 data set across rwb-reporting, rwb-case, rwb-agent and rwb-deviation**, so that **the measure set, the reconciliation gate and the dashboard read are proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production endpoint, no screen, no table, no migration, no workflow and no schedule, it serves no operation, it owns no table and it starts no workflow. The real behaviour is owned by the four I stories RWB-P9-E2009-APP (the seven steering measures, the reconciliation gate, the publish state and GET /reports/measures in rwb-reporting), RWB-P3-E2009-APP (the case facts and the case list count of the business date), RWB-P10-E1063-APP (the agent runs, the agent metrics and the outcome counts of a run) and RWB-S8-E2009-APP (the deviation read that the dashboard's case scope depends on), and those four stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-009 journey crosses more than one service. rwb-reporting holds the measure definitions in force, the measure snapshots, the publish state of a business date and the measures read; rwb-case holds the case facts and the case list count the dashboard reconciles against; rwb-agent holds the agent runs, their acceptance and override outcomes and the metrics read; rwb-deviation holds the deviation records of the cases in the measure; rwb-source-data holds the freshness of each data product and the rerun control; and rwb-access answers the role, scope and rights check behind the read. Until those services are exercised together on one business date, the program cannot show that the steering committee and the teams read the same numbers, which is the outcome REQ-WKM-009 and REQ-WKM-006 target.

The legacy story is split. The four I stories build the calculators, the reconciliation gate, the publish state, the measures read, the screen, the agent metrics and the deviation read. This story is the fifth slice: it runs the journey once per business date against the published contracts or their fakes and records the evidence. What the harness proves, in one repeatable run, is:

- JOB-15 on the synthetic day 2026-12-15, with definition version MD-2026.12 in force, produces a value for each of the seven measures: CASES_BY_STAGE, CASES_BY_QUEUE_AGE, DECISIONS_LOGGED, TREATMENTS, LETTERS_SENT, AGENT_ACCEPTANCE and AGENT_OVERRIDE.
- The case-list reconciliation is a gate and not a warning: when the dashboard count of CASES_BY_STAGE is 240 and the case list count is 239, no snapshot rows and no published extract exist for 2026-12-15, the latest published day stays 2026-12-14, MSG-P9-002 names 239, 240 and 2026-12-15, and the alert reaches the Reporting and BI analyst and the data steward.
- The freshness stamp travels with the measure read, and a stale source shows its own date: a notice data product dated 2026-12-14 makes LETTERS_SENT show 2026-12-14 and MSG-P1-001 name the data product and that date.
- The agent rates are per agent and version: case-intake 1.2.0 with 200 recommendations, 170 accepted and 30 overridden gives 85.0 percent acceptance and 15.0 percent override, and deviation-screen 0.9.0 with no runs gives no rate and the words "No runs".
- The date filter and the rerun behave: from after to is refused with 422 and MSG-GEN-003, and a rerun of a published day gives the same values with the frozen baseline of 2026-11-27 unchanged.
- REQ-WKM-009 and REQ-WKM-006 hold at the integration level, so the numbers on SCR-37 and in the Power BI report come from the same published rows.

**DP-17 applied.** The data lake and the INT-19 extract are removed (Architecture v5 slide 37; ADR-018; Template and Rules v1 §R5.5 DP-17). In the target, rwb-reporting holds the reporting read model in its own schema `rwb_reporting` and publishes `rwb.reporting.ReportPublished.v1` on `rwb.reporting.events.v1`; the event and the read model replace the extract, and Power BI reads rwb-reporting, not a lake. The harness therefore asserts the read model and the published event, never an extract file and never a lake path. A scenario that needed lake data would be a gap; this story needs none.

### 3. Preconditions

- The four I stories have published contracts and are deployed in the SIT environment, or their contract fakes of §12.8 stand in for them: RWB-P9-E2009-APP (measures, reconciliation, publish state and the measures read in rwb-reporting), RWB-P3-E2009-APP (case facts and the case list count), RWB-P10-E1063-APP (agent runs, outcomes and metrics) and RWB-S8-E2009-APP (the deviation read).
- Definition version MD-2026.12 is in force for business date 2026-12-15, with the seven measure codes CASES_BY_STAGE, CASES_BY_QUEUE_AGE, DECISIONS_LOGGED, TREATMENTS, LETTERS_SENT, AGENT_ACCEPTANCE and AGENT_OVERRIDE loaded through the rwb-reporting contract (legacy sections 3 and 7 Background).
- The synthetic day 2026-12-15 holds 240 open cases, 1,412 decision log entries, 38 treatments and 95 notices sent, seeded through the owning contracts or the published fakes (legacy section 7 Background).
- The frozen baseline of 2026-11-27 exists and is readable through the measures read, so each value can be asserted beside it (legacy BR5).
- The test users are the roles of §10: RW-PRODHEAD and RW-TEAMMGR for the reads, RW-BIANAL and RW-DATASTEW for the hold alert, and a role without Reporting R for the refusal of §5 (legacy sections 10 and 15).
- gateway-bff is deployed with the composite steering route of DP-19 available. The gateway-bff composite steering route path and its merge order: Not specified in the source documents (GAP-0391; ASM-0566).
- The harness environment, its seeding of a full measure day, its evidence format and retention, and its pass/fail gate: Not specified in the source documents (GAP-0391; ASM-0566).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date 2026-12-15, the definition version in force and the contract versions of the six services it is about to exercise.
2. Harness: seeds the synthetic day 2026-12-15 (240 open cases, 1,412 decision log entries, 38 treatments, 95 notices sent), the agent runs of case-intake 1.2.0 and deviation-screen 0.9.0, and definition version MD-2026.12 through the owning contracts or the published fakes, then reads each item back to assert the seeded state.
3. Harness: observes the JOB-15 Reporting extract run for business date 2026-12-15 and records its run state and its business date; it starts nothing and waits for the run.
4. Harness: reads the seven measures through the measures read for 2026-12-15 and asserts a value for each code, the period 2026-12-15, the freshness stamp and the baseline of 2026-11-27 beside each value (AC1).
5. Harness: asserts the case-list reconciliation, first with case list 240 against case facts 240, then with case facts 239, and asserts no snapshot rows, no published day for 2026-12-15, the latest published day 2026-12-14, MSG-P9-002 naming 239, 240 and 2026-12-15, and the alert reaching RW-BIANAL and RW-DATASTEW (AC2).
6. Harness: reads the agent measures and asserts case-intake 1.2.0 at 85.0 percent acceptance and 15.0 percent override, deviation-screen 0.9.0 with no rate and the words "No runs", and that no agent output is copied into the evidence (AC3).
7. Harness: forces the notice data product DP07 to the 2026-12-14 load, asserts LETTERS_SENT shows 2026-12-14 and MSG-P1-001 names DP07 and 2026-12-14 (AC4).
8. Harness: sends the measures read with from 2026-12-15 and to 2026-12-01 and asserts 422 with MSG-GEN-003 naming "from" and "to"; then asserts the product filter returns only the rows of the chosen product (AC4, TC-E2-009-06-ITG, TC-E2-009-08-ITG).
9. Harness: calls the authorise operation for a role without Reporting R and asserts the refusal with MSG-P4-002 and no measure rows in the answer (TC-E2-009-10-ITG).
10. Harness: reruns the published business date 2026-12-15 through the job rerun control and asserts the same values for every measure and that the frozen baseline rows of 2026-11-27 are unchanged (AC4, TC-E2-009-09-ITG).
11. Harness: asserts the Power BI read path — the rwb-reporting read model and the `ReportPublished` event of 2026-12-15 on `rwb.reporting.events.v1`, with no data lake and no extract file — and writes one run report per business date, keyed by story and business date; the report format and retention are Not specified in the source documents (GAP-0391; ASM-0566).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | The dashboard count of CASES_BY_STAGE is 239 while the case list shows 240 open cases at the 2026-12-15 cut-off | No snapshot rows and no published day for 2026-12-15; the latest published day stays 2026-12-14; the message names 239, 240 and 2026-12-15; the alert reaches RW-BIANAL and RW-DATASTEW and the publish state of 2026-12-15 is held | MSG-P9-002 | TC-E2-009-04-ITG | AC2 |
| X2 | The notice data product DP07 is still the 2026-12-14 load | LETTERS_SENT shows the 2026-12-14 value with its own date; the message names DP07 and 2026-12-14; no measure is reported as if it were fresh | MSG-P1-001 | TC-E2-009-05-ITG | AC4 |
| X3 | The measures read is sent with from 2026-12-15 and to 2026-12-01 | 422 on the direct call and on the composite route; the message names "from" and "to"; no rows are returned and nothing is written | MSG-GEN-003 | TC-E2-009-06-ITG | AC4 |
| X4 | Agent deviation-screen 0.9.0 made no recommendations on 2026-12-15 | No AGENT_ACCEPTANCE and no AGENT_OVERRIDE value for that agent and version; the answer carries "No runs"; the run does not treat the absence as a zero | None | TC-E2-009-07-ITG | AC3 |
| X5 | JOB-15 is rerun for the published business date 2026-12-15 | The rows for 2026-12-15 carry the same values; the duplicate run leaves one published day; the frozen baseline rows of 2026-11-27 are unchanged | None | TC-E2-009-09-ITG | AC4 |
| X6 | A role without Reporting R calls the measures read or the composite steering route | 403 on the direct call; the composite route hides the measures; no row is returned | MSG-P4-002 | TC-E2-009-10-ITG | None owned here (RWB-P9-E2009-APP) |
| X7 | The seed pack cannot be loaded, another run holds the environment lock, or the evidence cannot be written | The run refuses to start and names the missing seed item or the lock holder, or is marked failed with the local evidence kept for the rerun; no scenario is reported as passed | None | All -ITG cases (the run refuses to start) | None owned here (run refusal) |
| X8 | No definition version is in force for 2026-12-15, or MD-2026.12 is not the version the measures read names | No measure value is asserted as published for the day; the run records the missing version and fails the gate for that business date; the harness never substitutes a version of its own | None | TC-E2-009-01-ITG | Background |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the four I stories or their fakes are available; it builds no service feature and has no build dependency |
| Negotiable | The seed pack, the assertion set and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The measure set, the reconciliation gate and the dashboard read are proven once across services, with the freshness and the baseline on the evidence |
| Estimable | One harness project, one journey specification, one fake pack, one per-run report |
| Small | Fits in two weeks with its tests, on the basis of the INVEST check of the legacy story RWB-E2-009 that this slice is split from |
| Testable | Each scenario of §7 is one automated journey on synthetic data with a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Steering dashboard v1 data set - wave 2 integration harness

  Background:
    Given the business date is 2026-12-15
    Given definition version "MD-2026.12" is in force with measures "CASES_BY_STAGE", "CASES_BY_QUEUE_AGE", "DECISIONS_LOGGED", "TREATMENTS", "LETTERS_SENT", "AGENT_ACCEPTANCE" and "AGENT_OVERRIDE"
    Given the synthetic day 2026-12-15 holds 240 open cases, 1,412 decision log entries, 38 treatments and 95 notices sent
    Given the frozen baseline of 2026-11-27 is readable through the measures read

  Scenario: AC1 The composite steering route through gateway-bff returns all seven measures (new, D-RCV-60)
    Given the harness calls the composite steering route at "Not specified in the source documents (GAP-0391; ASM-0566)" with from 2026-12-15 and to 2026-12-15
    When gateway-bff composes the answer from rwb-reporting and rwb-access
    Then the answer holds a value for each published measure (CASES_BY_ROUTE, CASES_BY_AGE, CASES_BY_QUEUE, REALIZED_RECOVERY, TIME_IN_STAGE, TAT_BY_ROUTE, CASES_BY_STAGE, DECISIONS_LOGGED, AGENT_ACCEPTANCE, AGENT_OVERRIDE; the measure count is open, GAP-1649) with period "2026-12-15"
    And the answer carries the freshness stamp, the baseline value of 2026-11-27 beside each value, and one trace spanning the gateway and each owning service
    And every call in the composition is one hop with the 2 s budget and no service reads another service's schema
    And the Power BI path reads the rwb-reporting read model and the published event for 2026-12-15, with no data lake and no extract file

  Scenario: AC2 The reconciliation gate holds the publish when the counts differ (new, D-RCV-60)
    Given the case list shows 240 open cases at the 2026-12-15 cut-off
    Given the case facts read for the dashboard total 239
    When the harness observes the JOB-15 Reporting extract run for business date 2026-12-15
    Then no snapshot rows and no published extract exist for 2026-12-15
    And the latest published day stays 2026-12-14
    And MSG-P9-002 names 239, 240 and 2026-12-15
    And the alert reaches the Reporting and BI analyst and the data steward
    And the publish state of 2026-12-15 is held

  Scenario: AC3 The agent measures are per agent and version (new, D-RCV-60)
    Given agent "case-intake" version "1.2.0" made 200 recommendations on 2026-12-15, of which 170 were accepted and 30 overridden with a reason
    Given agent "deviation-screen" version "0.9.0" made no recommendations on 2026-12-15
    When the harness reads the agent measures for 2026-12-15
    Then "AGENT_ACCEPTANCE" for "case-intake" "1.2.0" is 85.0 percent and "AGENT_OVERRIDE" is 15.0 percent
    And no rate is written for "deviation-screen" "0.9.0" and the answer carries "No runs"
    And no agent output is copied into the run report

  Scenario: AC4 Stale source, the date filter and the rerun of a published day (new, D-RCV-60)
    Given the notice data product "DP07" is from 2026-12-14 because the 2026-12-15 load has not arrived
    When the harness reads the measures for 2026-12-15
    Then "LETTERS_SENT" shows the value for 2026-12-14 and MSG-P1-001 names "DP07" and 2026-12-14
    When the harness sends the measures read with from 2026-12-15 and to 2026-12-01
    Then the answer is status 422 with MSG-GEN-003 naming "from" and "to"
    When the harness reruns the published business date 2026-12-15
    Then the rows for 2026-12-15 hold the same values
    And the frozen baseline rows of 2026-11-27 are unchanged

  Scenario: AC10 A redelivered consumed event is applied once (new, D-RCV-60)
    Given a consumed event for business date 2026-12-15 has been applied once
    When the same event is delivered again to the harness
    Then the day's measures hold the same values as before the redelivery
    And the redelivered event is not applied a second time

  Scenario: AC11 A failed or unanswered consumed call is reported and writes nothing (new, D-RCV-60)
    Given the harness calls a consumed service for business date 2026-12-15
    When the call fails or does not answer
    Then the answer reports the failure
    And no partial value is written for 2026-12-15

  Scenario: AC12 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case status at the 2026-12-15 cut-off that the model does not allow to change to the requested status
    When the harness requests that status change
    Then the status change is refused
    And the case status stays unchanged
```

These seven criteria are new for the ITG harness and do not restate the nine legacy criteria owned by RWB-P9-E2009-APP.

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

The rules are unchanged by the split. The harness asserts these seven rules against the owning services and re-implements none of them: it reads the definitions, the snapshots, the publish state and the rates through the rwb-reporting contract and never holds a formula, a tolerance or a band of its own. No BR row is changed by this story.

### 9. State transitions

None for the case. The harness changes no case status, route state, stage clock or timer. The table is what it observes on a business date and on a JOB-15 run.

| Observed object | State | Meaning |
|---|---|---|
| Business date (measure_publish) | Published | The reconciliation passed and the snapshot rows are readable for the day |
| Business date (measure_publish) | Held | The dashboard count differs from the case list count; the previous published day stays the latest |
| JOB-15 Reporting extract run | Not started, Started, Succeeded, Failed | The observed run state of the extract for the business date; the harness starts none of them |

A held day is published by the first run whose counts match, and a rerun of a published day keeps the same values; the harness asserts both and never sets a publish state itself.

The harness adds run states of its own only: Not started, Seeding, Running, Passed, Failed, with the latest run for a build deciding the gate. The gate definition is Not specified in the source documents (GAP-0391; ASM-0566).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, Tribe lead and squad members | Reads SCR-37 and the measures in the evidence (Reporting R); approves the steering definitions MD-2026.12 |
| RW-PRODHEAD, product head | The synthetic user for the filtered read and the stale-source read (Reporting R) |
| RW-TEAMMGR, team manager | The synthetic user for the date-order refusal and for the in-scope read (Reporting R) |
| RW-BIANAL, Reporting and BI analyst | Receives the hold alert the harness asserts; builds the Power BI report that reads rwb-reporting (Reporting CRUD) |
| RW-DATASTEW, data steward | Receives the hold alert and reads the reconciliation of 239 against 240 (Reporting CRU) |
| RW-FINANCE, Finance and CFO delegate | Reads the measures of the evidence (Reporting R) |
| RW-REFADM, reference data administrator | Loads the definition version the harness seeds (Reference data C) |
| Integration and QA team | Runs the harness, keeps the fake mappings, the seed pack and the evidence, and owns the pass/fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision; authorisation is answered by rwb-access through the operation of §12.2 |

Separation of duty: the analyst who loads a definition version does not approve it, and the harness seeds both steps with distinct test users. It asserts the refusal of a role without Reporting R and never grants a right itself.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary. The write rows of the legacy story belong to RWB-P9-E2009-APP; this story reads their result. Owner and team are read by ID; the display name is resolved from the P3 queue_member and assignment rows behind the rwb-access masking policy, and no personal data travels on an event.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through rwb-case contract |
| DF-CAS-003 | recovery_case | product_group | Read through rwb-case contract |
| DF-CAS-005 | recovery_case | status | Read through rwb-case contract |
| DF-CAS-006 | recovery_case | stage_code | Read through rwb-case contract |
| DF-CAS-008 | recovery_case | route_code | Read through rwb-case contract |
| DF-CAS-010 | recovery_case | queue_id | Read through rwb-case contract |
| DF-CAS-013 | recovery_case | entry_date | Read through rwb-case contract |
| DF-WRK-002 | queue | queue_code | Read through rwb-case contract |
| DF-TRT-004 | treatment | treatment_type | Read through rwb-treatment contract as projected by rwb-reporting |
| DF-TRT-013 | treatment | outcome | Read through rwb-treatment contract as projected by rwb-reporting |
| DF-LEG-018 | notice | notice_type | Read through rwb-comms contract as projected by rwb-reporting |
| DF-LEG-019 | notice | sent_date | Read through rwb-comms contract as projected by rwb-reporting |
| DF-LEG-022 | notice | delivery_status | Read through rwb-comms contract as projected by rwb-reporting |
| DF-DEC-003 | decision_log_entry | decision_code | Read through rwb-reporting contract, from the decision-record ingest |
| DF-DEC-007 | decision_log_entry | agent_version | Read through rwb-reporting contract, from the decision-record ingest |
| DF-DEC-012 | decision_log_entry | final_call | Read through rwb-reporting contract, from the decision-record ingest |
| DF-DEC-013 | decision_log_entry | override_reason | Read through rwb-reporting contract, from the decision-record ingest |
| DF-DEC-016 | decision_log_entry | decided_at | Read through rwb-reporting contract, from the decision-record ingest |
| DF-RPT-032 | measure_definition | measure_code | Read through rwb-reporting contract |
| DF-RPT-034 | measure_definition | formula | Read through rwb-reporting contract |
| DF-RPT-035 | measure_definition | data_product | Read through rwb-reporting contract |
| DF-RPT-037 | measure_definition | definition_version | Read through rwb-reporting contract |
| DF-RPT-042 | measure_snapshot | measure_code | Read through rwb-reporting contract |
| DF-RPT-043 | measure_snapshot | definition_version | Read through rwb-reporting contract |
| DF-RPT-044 | measure_snapshot | business_date | Read through rwb-reporting contract |
| DF-RPT-045 | measure_snapshot | product_group | Read through rwb-reporting contract |
| DF-RPT-046 | measure_snapshot | dimension_code | Read through rwb-reporting contract |
| DF-RPT-047 | measure_snapshot | dimension_value | Read through rwb-reporting contract |
| DF-RPT-048 | measure_snapshot | value | Read through rwb-reporting contract |
| DF-RPT-049 | measure_snapshot | case_count | Read through rwb-reporting contract |
| DF-RPT-052 | measure_snapshot | published_at | Read through rwb-reporting contract |
| DF-RPT-054 | measure_publish | business_date | Read through rwb-reporting contract |
| DF-RPT-055 | measure_publish | status | Read through rwb-reporting contract |
| DF-RPT-056 | measure_publish | case_list_count | Read through rwb-reporting contract |
| DF-RPT-057 | measure_publish | dashboard_count | Read through rwb-reporting contract |
| DF-RPT-058 | measure_publish | held_reason | Read through rwb-reporting contract |

The harness reads no schema directly (DP-01) and seeds nothing by SQL (DP-15). Test data is synthetic: the 240 open cases, the 1,412 decision log entries, the 38 treatments, the 95 notices, the two agent versions and the definition version are seeded through the owning operations and their fakes, and no production case, party, notice or agent output is used or copied into an evidence file. The GET /reports/measures read is declared in the wave 1 contract for this harness and the P3 catalog consumer; the dashboard, its filters and SCR-37 stay with RWB-P9-E2009-APP, and the connection of any reporting client to the read is an open decision for the PRD step. The steering dashboard is read as the dashboard and measure resources of rwb-reporting through gateway-bff, not as a Power BI data set (ADR-018). The composite steering route path and merge order, the harness repository and SIT environment, the seeded measure day, the evidence format and retention, and the pass/fail gate are to be agreed at the wave 2 entry check: Not specified in the source documents (GAP-0391).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | Reads the seven measures of the business date with period, dimension, freshness stamp and baseline value (AC1, AC2, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | Reads the case list count of the cut-off and the product split used by the reconciliation and the filter (AC2, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads one case fact of the seeded day, to prove the case facts behind CASES_BY_STAGE exist (AC2) |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | Reads the runs of case-intake 1.2.0 and deviation-screen 0.9.0 on 2026-12-15, and the no-runs answer (AC3) |
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | P10 rwb-agent | Reads the recommendations, accepted and overridden counts behind the two rates (AC3) |
| GET | `/api/recovery/agent/v1/cases/{caseId}/agent-outputs` | P10 rwb-agent | Proves the outputs are counted and never copied into the evidence (AC3, BR3) |
| GET | `/api/recovery/deviation/v1/deviations` | S8 rwb-deviation | Reads the deviation records behind the case scope of the measures (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | Reads the freshness of DP07 and of every data product behind the seven measures (AC4, BR4) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Drives the rerun control of the published day, so the same values and the unchanged baseline are asserted (AC4) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and Reporting right check used by the composite route and by the direct call; supplies the MSG-P4-002 refusal (TC-E2-009-10-ITG) |

The composite steering route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0391; ASM-0566).

#### 12.3 Events published

None. The harness produces no event; it consumes the events of §12.4 with its own consumer group.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| `rwb.reporting.ReportPublished.v1` | `rwb.reporting.events.v1` | P9 rwb-reporting | One event per published business date with the business date, the definition version and the measure set; no event for a held day; the event is the path the reporting read model reads after DP-17 |
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | The load of the business date is ready before the extract is observed, and the freshness of DP07 matches the load that arrived |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (ledger); the owning service publishes its own record | The 1,412 decision log entries of the day reach the ledger and agree with DECISIONS_LOGGED, and the agent version and override reason on the records agree with the two agent rates (BR3) |
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | The runs of case-intake 1.2.0 and the absence of runs of deviation-screen 0.9.0 on the day, which is the denominator the rates use (BR6) |
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | The deviation records of the cases in the measure are the ones the dashboard scope reads, so a case with an open deviation is counted once (AC1) |

Consumers dedupe through their own inbox table; the harness consumes with its own group and never asserts a producer's outbox row.

#### 12.5 Workflows and activities

JOB-15 Reporting extract is observed, not built. Architecture v5 slide 44 makes it an Airflow-triggered extract in rwb-reporting with no data lake: it is not a Temporal workflow and not a Temporal Schedule, and the harness starts nothing. The harness waits for the run for business date 2026-12-15, records its run state and the business date, and then asserts the measures, the reconciliation outcome, the publish state and the event of §12.4.

No workflow is built, no activity is added and no Nexus operation is created by this story. The extract and its measure calculations belong to RWB-P9-E2009-APP; the Airflow edge belongs to the platform.

#### 12.6 Schedules

None. JOB-15 is the Airflow edge for the extract, so the harness adds no Temporal Schedule and creates no cron. It waits for the run and asserts its outcome only.

#### 12.7 Tables owned

None. The harness owns no table in any schema (DP-01); it reads and writes through the operations of §12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-reporting | `GET /api/recovery/reporting/v1/reports/measures` | OpenAPI of P9 | The seven measures of 2026-12-15 with period, dimension, freshness stamp and the 2026-11-27 baseline; the held day with 239 against 240; the stale LETTERS_SENT value for 2026-12-14; 422 with MSG-GEN-003 for the date pair; 403 with MSG-P4-002 for the refusal; the no-runs answer for deviation-screen 0.9.0 |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases`, `GET /api/recovery/case/v1/cases/{caseId}` | OpenAPI of P3 | 240 open cases at the 2026-12-15 cut-off, 140 of them MORTGAGE; the case facts list totalling 239 for the held case; one case fact per seeded case |
| WireMock rwb-agent | `GET /api/recovery/agent/v1/admin/agent-runs`, `GET /api/recovery/agent/v1/admin/agent-metrics`, `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` | OpenAPI of P10 | case-intake 1.2.0 with 200 recommendations, 170 accepted and 30 overridden; deviation-screen 0.9.0 with no runs; the output count only, never the output text |
| WireMock rwb-deviation | `GET /api/recovery/deviation/v1/deviations` | OpenAPI of S8 | The deviation records of the cases in the measure, including the open deviation of the seeded case |
| WireMock rwb-source-data | `GET /api/recovery/source-data/v1/data-products/freshness`, `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | OpenAPI of P1 | DP07 fresh at 2026-12-15 and stale at 2026-12-14; the freshness of every other product of the measure set; 202 for the rerun and the same values after it |
| WireMock rwb-access | `POST /api/recovery/access/v1/authorise` | OpenAPI of P4 | Allow Reporting R with the recovered scope for RW-PRODHEAD, RW-TEAMMGR, RW-BIANAL, RW-DATASTEW, RW-FINANCE and RW-TRIBE; refuse a role without Reporting R with MSG-P4-002 |

Each fake is replaced by the real service as its I story lands, contract by contract, without a change to the scenarios. The harness repository, its environment, its seeding of a full measure day, its evidence format and retention, and its pass/fail gate: Not specified in the source documents (GAP-0391; ASM-0566).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Ten consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes `rwb.reporting.ReportPublished.v1`, `rwb.source-data.AceDataReady.v1`, `rwb.decision.DecisionRecorded.v1`, `rwb.agent.AgentRunCompleted.v1` and `rwb.deviation.DeviationRaised.v1`; publishes nothing |
| Temporal | No | The extract is Airflow-triggered and is not a Temporal workflow; the harness starts no workflow and adds no activity |
| File | No | Reads and writes no file of the business flow; the reporting read model and the event replace the extract, and the run report is harness evidence only |

### 13. Solution plan

**Package.** Folder `integration/recovery-steering-dashboard` in the ACE repository, package `<ACE base package>.recovery.integration.steeringdashboard`. Not part of any deployed service, and it owns no schema, table or migration (DP-01, DP-15).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the four I stories, which replace the fakes with real services one at a time.

**DP-17 applied.** The data lake and the INT-19 extract are removed (Architecture v5 slide 37; ADR-018). rwb-reporting holds the reporting read model in its own schema and publishes `rwb.reporting.ReportPublished.v1` on `rwb.reporting.events.v1`; the read model and the event replace the extract, and Power BI reads rwb-reporting. The harness asserts the read model and the event, holds no lake path, and fails a run that needs one. No lake row, no lake copy and no extract file is a dependency of this story.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, with the run lock and the build ID; stops at the first failed assertion with the trace |
| CompositeRouteClient | Harness adapter | Calls the gateway-bff composite steering route and the ten consumed operations of §12.2, with the test user of the scenario |
| FakePack | WireMock project | Serves rwb-reporting, rwb-case, rwb-agent, rwb-deviation, rwb-source-data and rwb-access from the published OpenAPI documents of §12.8 |
| MeasureAssertion | Assertion | Reads the seven measures and fails the run on a missing code, a wrong period, a missing freshness stamp or a missing baseline value |
| ReconciliationAssertion | Assertion | Compares the CASES_BY_STAGE total with the case list count, and fails the run when a held day has snapshot rows or a published date, or when the message does not name both counts and the business date |
| AgentRateAssertion | Assertion | Computes 170 over 200 and 30 over 200, fails the run on any other rate, and fails a rate for an agent with no runs |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0391; ASM-0566) |

**Environment and test data**

- Environment: SIT, one namespace, the four I stories deployed from their wave 2 builds or replaced by the §12.8 fakes, with the gateway route for `/api/recovery/*`, the topics of §12.4 and the shared topic `rwb.decision-record.v1`. Harness repository, environment and seeding: Not specified in the source documents (GAP-0391; ASM-0566).
- Data: synthetic day 2026-12-15 with 240 open cases, 1,412 decision log entries, 38 treatments and 95 notices sent; definition version MD-2026.12; the frozen baseline of 2026-11-27; agents case-intake 1.2.0 (200 recommendations, 170 accepted, 30 overridden) and deviation-screen 0.9.0 (no runs); notice data product DP07 dated 2026-12-14 in the stale case and 2026-12-15 in the healthy case; case list 240 against case facts 239 in the held case; the date pair from 2026-12-15 to 2026-12-01. No production record is copied and no agent output text enters the evidence.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and CompositeRouteClient against the published OpenAPI documents of the six services, with the run lock and the build ID.
2. Publish FakePack for the six services from the same documents, and prove the harness runs green from Day 1 on the fakes with the healthy seed of 2026-12-15.
3. Add the composite route assertion of AC1, including the 2 s per-call budget, the single trace and the no-cross-schema check.
4. Add MeasureAssertion over the seven codes with period, freshness stamp and the 2026-11-27 baseline, and the held-day assertion of AC2 with MSG-P9-002 and the alert to the two roles.
5. Add AgentRateAssertion for case-intake 1.2.0 and the no-runs answer of deviation-screen 0.9.0, and assert that no agent output is copied (AC3).
6. Add the stale-source case of AC4 with MSG-P1-001 naming DP07 and 2026-12-14, and the date-order refusal with MSG-GEN-003 naming from and to.
7. Add the rerun of the published day with the unchanged baseline, and the access refusal with MSG-P4-002 for a role without Reporting R.
8. Add the DP-17 assertion over the rwb-reporting read model and `ReportPublished`, write RunReportWriter, replace each fake with the real service as its I story lands, attach the report to the wave 2 release record and evaluate the gate; the gate definition: Not specified in the source documents (GAP-0391; ASM-0566).

**Feature switch:** `rwb.reporting.steering` is the legacy switch of RWB-E2-009 and stays with RWB-P9-E2009-APP; the harness asserts its enabled state only. The harness has no production feature flag and runs in the test environment only.

**Done when:** the journey runs green against the four deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, the seven measures carry the definition version and the freshness stamp, the held day leaves the latest published day at 2026-12-14 with no snapshot rows, and the Power BI read and the measures read return the same values from the rwb-reporting rows for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P9-002 | The dashboard count differs from the case list | The case count on the dashboard ({count}) does not match the case list ({listCount}) for {date}. The publish is held. |
| MSG-P1-001 | A source is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-003 | Dates in the wrong order | {field} cannot be before {other}. |
| MSG-P4-002 | The role lacks Reporting R | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values; it does not own the message text. In this journey {count} is 239, {listCount} is 240 and {date} is 2026-12-15 for MSG-P9-002; {product} is "DP07 Legal" and {date} is 2026-12-14 for MSG-P1-001; {field} is "from" and {other} is "to" for MSG-GEN-003. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-37 Steering dashboard | Loading | The composite steering route returns the measures for 2026-12-15 and the answer is complete before the screen renders; the harness asserts the answer the Loading state waits on, not the skeleton |
| SCR-37 Steering dashboard | Filtered | The chosen product, route and date return only the matching rows, each beside the baseline of 2026-11-27, with the business date and the freshness stamp |
| SCR-37 Steering dashboard | Held | The answer carries MSG-P9-002 with 239, 240 and 2026-12-15, and the latest published day is 2026-12-14 |
| SCR-37 Steering dashboard | Stale | The answer carries MSG-P1-001 with "DP07 Legal" and 2026-12-14, and LETTERS_SENT shows the 2026-12-14 value |
| SCR-37 Steering dashboard | Empty | Not specified in the source documents (CG-ALL-613) |
| SCR-37 Steering dashboard | Error | Not specified in the source documents (CG-ALL-613) |
| SCR-37 Steering dashboard | No access | Not specified in the source documents (CG-ALL-613) |

The harness opens no screen and renders no page; it asserts the operations and the answers the screen consumes. SCR-37 is served by the dashboard data set and the report reads of rwb-reporting on its resources, behind the gateway-bff route. Screen-level behaviour, layout and message rendering remain with RWB-P9-E2009-APP. The harness environment and evidence detail: Not specified in the source documents (GAP-0391; ASM-0566).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-009-01-ITG | AC1, BR1, BR4 | Integration | Synthetic day 2026-12-15 |
| TC-E2-009-02-ITG | AC2, BR1, BR2 | Integration | 240 open cases; 1,412 decision log entries |
| TC-E2-009-03-ITG | AC3, BR3 | Integration | case-intake 1.2.0: 200 recommendations, 170 accepted, 30 overridden |
| TC-E2-009-04-ITG | AC4, BR2 | Integration | Case list 240, case facts 239 |
| TC-E2-009-05-ITG | AC5, BR4 (run by RWB-P9-E2009-APP) | Integration | Notice product dated 2026-12-14 |
| TC-E2-009-06-ITG | AC6 (run by RWB-P9-E2009-APP) | Integration | from 2026-12-15, to 2026-12-01 |
| TC-E2-009-07-ITG | AC7, BR6 (run by RWB-P9-E2009-APP) | Integration | deviation-screen 0.9.0 with no runs |
| TC-E2-009-08-ITG | AC8, BR7 (run by RWB-P9-E2009-APP) | Integration | Filter MORTGAGE |
| TC-E2-009-09-ITG | AC9, BR5 (run by RWB-P9-E2009-APP) | Integration | JOB-15 rerun for 2026-12-15 |
| TC-E2-009-10-ITG | Access | Component | PT-LAWFIRM calls GET /reports/measures; refused with MSG-P4-002 |
| TC-E2-009-11-ITG | AC10 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E2009-ITG-AC10) |
| TC-E2-009-12-ITG | AC11 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E2009-ITG-AC11) |
| TC-E2-009-13-ITG | AC12 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E2009-ITG-AC12) |

The full legacy test, with its Given, When and Then, is in the legacy test case workbook, tab Story test cases, under the legacy test case ID. The Covers column names the legacy AC of RWB-E2-009 that the ITG copy is derived from; the Level column maps the legacy System level to Integration and the legacy Access level to Component. Each `-ITG` case runs the legacy Given, When and Then across the six contracts of §12.2 and the seeded day, and the nine legacy criteria themselves stay owned by RWB-P9-E2009-APP.

### 17. Guardrails

- No business value in code: the measure definitions, the formulas, the reconciliation tolerance and the age bands are data held by rwb-reporting; the harness reads them and never holds a copy or a threshold.
- No personal data in logs, tests, traces or reports: the evidence holds measure codes, counts, rates, dates, roles and agent versions only; the agent outputs are counted, never copied.
- No read of another service's schema and no direct ACE read: every read goes through the owner's contract, and the harness fails a run whose trace shows a cross-schema read (DP-01).
- No data lake: DP-17 removes the lake and INT-19, the reporting read model and `ReportPublished` replace the extract, and the harness fails a run that needs a lake path or an extract file.
- Counts on SCR-37 and in Power BI come from the same rows: the harness asserts both reads on one published business date and reports a difference as a failure, not as a warning.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner, and every call carries the 2 s budget of DP-11.
- A fake that outlives its service is a defect, not a configuration: each fake is replaced by the real service as its I story lands, and the harness never runs against UAT or production.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-009 | Steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-OCC-12, FEAT-RPT-03, FEAT-RPT-08 | 15 Manage performance, data and AI | None; NFR-065 and NFR-066 apply | TC-E2-009-01-ITG, TC-E2-009-04-ITG, TC-E2-009-06-ITG |
| REQ-WKM-006 | Queue counts and ageing reported daily and reconciled to the case list | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-RPT-08 | 15 Manage performance, data and AI | None; DL25 applies | TC-E2-009-01-ITG, TC-E2-009-02-ITG, TC-E2-009-04-ITG |

The measure values, the reconciliation gate and the two rates carry REQ-WKM-009 and REQ-WKM-006 at the integration level; this story adds no requirement ID of its own. The test lists in the table above follow RTM v7; the other test cases of this story are listed in section 16.

Open decisions apply to this story: DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863) and DL25 (assumptions ASM-0728, ASM-0735, ASM-0743, ASM-2602). Both decisions are still open.

### 19. Out of scope

- The four owning I stories RWB-P9-E2009-APP, RWB-P3-E2009-APP, RWB-P10-E1063-APP and RWB-S8-E2009-APP, and every screen, endpoint, table, migration, workflow and schedule they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-reporting, rwb-case, rwb-agent, rwb-deviation, rwb-source-data and rwb-access, which their CON stories own.
- The CON and OPS stories of the wave, the platform gateway-bff composite route implementation (RWB-PLT-N001-CON), and the platform configuration of Kafka, the workflow platform and observability.
- The data lake and the INT-19 extract, which DP-17 removes; no lake read, lake copy or extract file is built or asserted.
- Power BI itself: the report ownership, the visuals and the 07:30 refresh belong to the Reporting and BI analyst role and its own delivery, not to this story.
- The other legacy journeys of RWB-ITG-W2 (RWB-E2-006, RWB-E2-007, RWB-E2-008, RWB-E2-010) and their harnesses.
- Queue measures and service level breaches for team managers (RWB-E1-030, RWB-E2-011), the agent monitoring dashboard with latency and cost (RWB-E2-031), benefit realisation (FEAT-RPT-06) and the regulatory returns (FEAT-RPT-07).
