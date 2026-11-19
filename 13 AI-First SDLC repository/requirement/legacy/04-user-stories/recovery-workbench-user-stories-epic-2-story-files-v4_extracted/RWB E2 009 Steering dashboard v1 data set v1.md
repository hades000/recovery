<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 009 Steering dashboard v1 data set v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 009 Steering dashboard v1 data set v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-009 Steering dashboard v1 data set

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-009 |
| Epic | E2, release 31 December 2026 |
| Module | P9 Reporting |
| Feature | FEAT-OCC-12 Publish the steering dashboard; FEAT-RPT-03 Publish the steering dashboard; FEAT-RPT-08 Refresh and publish the measure set |
| Requirement IDs | REQ-WKM-009, REQ-WKM-006 |
| BRD section | Business Requirements Epic 2, sections 3.9 and 4 |
| L3 process | 15 Manage performance, data and AI |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-013, RWB-E1-063 |
| Status | Ready for build |

## 1. Story

As the **Tribe lead (RW-TRIBE)**, I want **a data set for the steering dashboard with cases by stage, queue and age, decisions logged, treatments, letters sent and agent acceptance, published each morning and reconciled to the case list**, so that **the steering committee reads the same numbers the teams work with**.

## 2. Business rationale

The steering committee receives numbers counted by hand that differ from what the teams see in their queues. This story adds the steering measures to the nightly measure set, holds the publish when the dashboard case count differs from the case list, serves the values through GET /reports/measures to SCR-37 and through the data lake extract to Power BI, and adds agent acceptance and override rates. It serves REQ-WKM-009 and REQ-WKM-006, NFR-065 and NFR-066.

## 3. Preconditions

- RWB-E1-013 is done: measure_definition, measure_snapshot, MeasureCatalog and JOB-15 run, with the baseline of 2026-11-27 frozen.
- RWB-E1-063 is done: agent runs and their outcomes are readable through the P10 monitoring interface.
- The steering definitions, version "MD-2026.12", are loaded and approved by the Tribe lead.
- Notices, treatments and decision log entries are readable through the P6, P3 and P7 reporting interfaces.
- The reader holds a role with Reporting R and the case scope "All", or reads only the teams in their scope.

## 4. Flow

1. JOB-15 Reporting extract, nightly 01:30: reads the definitions in force, including the steering measures of MD-2026.12.
2. System: computes each steering measure for the previous business date from the owning modules' reporting interfaces.
3. System: compares the total of CASES_BY_STAGE with the open case count of the case list at the same cut-off (P3 interface).
4. System: if the counts are equal, writes the snapshot rows and the INT-19 extract with the freshness stamp; if not, holds the publish, keeps the previous day as the latest published and alerts the Reporting and BI analyst and the data steward.
5. Reporting and BI analyst: the Power BI data set refreshes at 07:30 from the extract.
6. Product head or team manager: opens SCR-37 Steering dashboard; the screen calls GET /reports/measures with product, route and date filters.
7. System: checks Reporting R and the scope, returns the published values with the business date and the freshness stamp, and shows the baseline beside each value.
8. System: computes agent acceptance and override rates per agent and version from the decision log and the agent runs; an agent with no runs shows "No runs" and no rate.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Dashboard case count differs from the case list | Publish held; previous day stays; alert | MSG-P9-002 | AC4 |
| X2 | A source load for the business date is stale | Previous day shown with its date | MSG-P1-001 | AC5 |
| X3 | Query with from after to | Refused | MSG-GEN-003 | AC6 |
| X4 | An agent has no runs on the day | No rate; "No runs" shown | None | AC7 |
| X5 | JOB-15 rerun for a published business date | Rows replaced with the same values; baseline unchanged | None | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Extends the measure set of RWB-E1-013; agent data from RWB-E1-063 |
| Negotiable | Steering measures are definition rows; layout of SCR-37 follows the ACE components |
| Valuable | One set of numbers for the committee and the teams |
| Estimable | Seven calculators, one reconciliation check, one endpoint, one screen |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic day with known answers |

## 7. Acceptance criteria

```gherkin
Feature: Steering dashboard v1 data set

  Background:
    Given definition version "MD-2026.12" is in force with measures "CASES_BY_STAGE", "CASES_BY_QUEUE_AGE", "DECISIONS_LOGGED", "TREATMENTS", "LETTERS_SENT", "AGENT_ACCEPTANCE" and "AGENT_OVERRIDE"
    Given the synthetic day 2026-12-15 holds 240 open cases, 1,412 decision log entries, 38 treatments and 95 notices sent

  Scenario: AC1 Refresh
    Given the loads of business date 2026-12-15 passed their checks
    When JOB-15 runs at 01:30 on 2026-12-16
    Then GET /reports/measures?from=2026-12-15&to=2026-12-15 returns a value for each of the 7 measures with period "2026-12-15"
    Then the INT-19 extract for 2026-12-15 has freshness stamp 2026-12-15 for the 07:30 Power BI refresh

  Scenario: AC2 Reconciles
    Given the case list shows 240 open cases at the 2026-12-15 cut-off
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the sum of "CASES_BY_STAGE" for 2026-12-15 is 240
    Then "DECISIONS_LOGGED" for 2026-12-15 is 1,412, the count of decision log entries decided that day

  Scenario: AC3 Agent measures
    Given agent "case-intake" version "1.2.0" made 200 recommendations on 2026-12-15, of which 170 were accepted and 30 overridden with a reason
    When JOB-15 runs at 01:30 on 2026-12-16
    Then "AGENT_ACCEPTANCE" for "case-intake" "1.2.0" on 2026-12-15 is 85.0 percent
    Then "AGENT_OVERRIDE" for "case-intake" "1.2.0" on 2026-12-15 is 15.0 percent
    Then SCR-37 shows both rates by agent

  Scenario: AC4 Counts do not match
    Given the case list shows 240 open cases at the 2026-12-15 cut-off
    Given the case facts read for the dashboard total 239
    When JOB-15 runs at 01:30 on 2026-12-16
    Then no snapshot rows and no extract are published for 2026-12-15
    Then SCR-37 shows 2026-12-14 as the latest day with MSG-P9-002 naming 239, 240 and 2026-12-15
    Then an alert goes to the Reporting and BI analyst and the data steward

  Scenario: AC5 Stale source
    Given the notice data product is from 2026-12-14 because the 2026-12-15 load has not arrived
    When a product head opens SCR-37 on 2026-12-16
    Then "LETTERS_SENT" shows the value for 2026-12-14
    Then SCR-37 shows MSG-P1-001 naming "DP07 Legal" and 2026-12-14

  Scenario: AC6 Dates in the wrong order
    Given a team manager holds RW-TEAMMGR with Reporting R
    When a team manager sends GET /reports/measures?from=2026-12-15&to=2026-12-01
    Then the response is status 422 with MSG-GEN-003 naming "from" and "to"

  Scenario: AC7 Agent with no runs
    Given agent "deviation-screen" version "0.9.0" made no recommendations on 2026-12-15
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the system writes no "AGENT_ACCEPTANCE" value for "deviation-screen" on 2026-12-15
    Then SCR-37 shows "No runs" for "deviation-screen" on 2026-12-15

  Scenario: AC8 Filter by product
    Given the measures for 2026-12-15 are published and the case list shows 140 open Mortgage cases at the cut-off
    When a product head sends GET /reports/measures?measure=CASES_BY_STAGE&product=MORTGAGE&from=2026-12-15&to=2026-12-15
    Then the response holds only rows with product "MORTGAGE"
    Then their sum is 140

  Scenario: AC9 Rerun of a published day
    Given the measures for 2026-12-15 are published
    When JOB-15 is rerun for business date 2026-12-15 from SCR-44
    Then the rows for 2026-12-15 hold the same values
    Then the frozen baseline rows of 2026-11-27 are unchanged
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Steering measures are computed from Workbench records and the decision log, never from a separate count | NFR-065; REQ-WKM-009 |
| BR2 | The dashboard case count equals the case list count at the same cut-off, or the publish is held | REQ-WKM-006; DL25 (tolerance zero) |
| BR3 | Agent acceptance is accepted recommendations over all recommendations, and override is overridden over all, per agent and version | NFR-066; DF-DEC-007, DF-DEC-013 |
| BR4 | A measure is shown with its business date and freshness stamp; stale data shows its date | MSG-P1-001 rule; FEAT-RPT-08 |
| BR5 | Each value is shown beside the frozen baseline of 2026-11-27 | REQ-WKM-009; RWB-E1-013 BR2 |
| BR6 | A rate with no runs in the denominator is not computed | NFR-066 |
| BR7 | Every query applies the role's scope | CTL-09 |

## 9. State transitions

None. This story does not change a case status. It sets the publish status of a business date (published or held) and the JOB-15 run status.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, Tribe lead and squad members | Reads SCR-37 and the measures (Reporting R); approves the steering definitions |
| RW-PRODHEAD, product head | Reads SCR-37 (Reporting R) |
| RW-TEAMMGR, team manager | Reads SCR-37 for teams in scope (Reporting R) |
| RW-BIANAL, Reporting and BI analyst | Builds the Power BI report; receives the hold alert (Reporting CRUD) |
| RW-DATASTEW, data steward | Receives the hold alert; reads the reconciliation (Reporting CRU) |
| RW-FINANCE, Finance and CFO delegate | Reads SCR-37 (Reporting R) |
| RW-REFADM, reference data administrator | Loads the steering definitions (Reference data C) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-008 | recovery_case | route_code | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-LEG-018 | notice | notice_type | Read |
| DF-LEG-019 | notice | sent_date | Read |
| DF-LEG-022 | notice | delivery_status | Read |
| DF-DEC-003 | decision_log_entry | decision_code | Read |
| DF-DEC-007 | decision_log_entry | agent_version | Read |
| DF-DEC-012 | decision_log_entry | final_call | Read |
| DF-DEC-013 | decision_log_entry | override_reason | Read |
| DF-DEC-016 | decision_log_entry | decided_at | Read |
| DF-RPT-032 | measure_definition | measure_code | Read |
| DF-RPT-034 | measure_definition | formula | Read |
| DF-RPT-035 | measure_definition | data_product | Read |
| DF-RPT-037 | measure_definition | definition_version | Read |
| DF-RPT-042 | measure_snapshot | measure_code | Write |
| DF-RPT-043 | measure_snapshot | definition_version | Write |
| DF-RPT-044 | measure_snapshot | business_date | Write |
| DF-RPT-045 | measure_snapshot | product_group | Write |
| DF-RPT-046 | measure_snapshot | dimension_code | Write |
| DF-RPT-047 | measure_snapshot | dimension_value | Write |
| DF-RPT-048 | measure_snapshot | value | Write |
| DF-RPT-049 | measure_snapshot | case_count | Write |
| DF-RPT-052 | measure_snapshot | published_at | Write |
| DF-RPT-054 | measure_publish | business_date | Write |
| DF-RPT-055 | measure_publish | status | Write |
| DF-RPT-056 | measure_publish | case_list_count | Write |
| DF-RPT-057 | measure_publish | dashboard_count | Write |
| DF-RPT-058 | measure_publish | held_reason | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/reports/measures** (api.yaml, x-module P9)

| Item | Value |
|---|---|
| Request | Query: measure, product, route, from, to (dates, from on or before to) |
| Response | 200 array of Measure: measure, product, route, period, value, and the new dimension and baselineValue. The response header X-Data-As-Of carries the business date of the latest published day |
| Errors | 401 no session (MSG-P4-001); 403 role lacks Reporting R (MSG-P4-002); 422 dates in the wrong order (MSG-GEN-003); 503 store unavailable (MSG-GEN-006) |
| Authorization | Reporting, right R, scope applied |
| Idempotency | Not applicable |

The Measure schema in api.yaml has no dimension or baseline field. This story adds dimension (the dimension code and value, for example "agent:case-intake:1.2.0") and baselineValue to the Measure schema, recorded as missing fields in the additions file.

**Job JOB-15 Reporting extract**: as in RWB-E1-013, with the reconciliation step before publish. Idempotency key unchanged. Restart: rerun from SCR-44; a held day is published by the first run whose counts match.

**Published interfaces called**

```java
Stream<CaseFact> CaseReportingApi.caseFacts(LocalDate businessDate);                     // P3
long CaseReportingApi.openCaseCount(LocalDate cutOff, Optional<String> productGroup);   // P3, the case list count
Stream<DecisionFact> DecisionLogApi.decisionFacts(LocalDate businessDate);              // P7
Stream<TreatmentFact> TreatmentApi.treatmentFacts(LocalDate businessDate);              // P3
Stream<NoticeFact> NoticeApi.noticeFacts(LocalDate businessDate);                       // P6
Stream<AgentRunFact> AgentMonitorApi.runFacts(LocalDate businessDate);                  // P10, RWB-E1-063
```

## 13. Solution plan

- Package: folder `recovery/reporting/steering`, Java package `recovery.reporting.steering`; front end folder `recovery/reporting/steering`.

| Component | Type | Responsibility |
|---|---|---|
| SteeringCalculators | Service | One calculator per steering measure code |
| CountReconciliation | Service | BR2 check before publish; writes measure_publish |
| ReportingExtractJob | Job | From RWB-E1-013; adds the steering calculators and the reconciliation step |
| MeasureController | Controller | GET /reports/measures with filters, scope and X-Data-As-Of |
| MeasureQueryRepository | Repository | Reads published measure_snapshot rows by filter |
| SteeringDashboard | React component | SCR-37: filters by product, route and date; value beside baseline; agent rates; freshness and hold messages |

- Database: new table measure_publish (unique business_date). Index on measure_snapshot (measure_code, business_date, product_group). Flyway migration `V2_009__measure_publish.sql`.
- Configuration and reference data: steering definitions MD-2026.12 (Tribe lead approves; RW-REFADM loads); reconciliation tolerance zero (DL25); age bands from RWB-E1-013.
- Build steps:
  1. Write the migration and the measure_publish entity.
  2. Build the seven calculators against stub interfaces with the synthetic day; test AC1, AC2 values and AC3, AC7.
  3. Build CountReconciliation and wire it before publish in ReportingExtractJob; test AC4 and AC9.
  4. Build MeasureController with filters, date check, scope and X-Data-As-Of; test AC6 and AC8.
  5. Build SteeringDashboard with Loading and filtered states and the stale and held messages; test AC5 in the browser.
- Feature flag: `rwb.reporting.steering`.
- Done when: the tests in section 16 pass, and the Power BI report and SCR-37 show the same values for one SIT day.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P9-002 | The dashboard count differs from the case list | The case count on the dashboard ({count}) does not match the case list ({listCount}) for {date}. The publish is held. |
| MSG-P1-001 | A source is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-003 | Dates in the wrong order | {field} cannot be before {other}. |
| MSG-P4-002 | The role lacks Reporting R | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-37 Steering dashboard (module P9, capability area Reporting):

| State | What the user sees and does |
|---|---|
| Loading | Skeleton rows while GET /reports/measures returns |
| Filtered | Values for the chosen product, route and dates, each beside the baseline of 2026-11-27, with the business date; agent rates by agent and version; MSG-P9-002 or MSG-P1-001 when the latest day is held or stale |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-009-01 | AC1, BR1, BR4 | System | Synthetic day 2026-12-15 |
| TC-E2-009-02 | AC2, BR1, BR2 | System | 240 open cases; 1,412 decision log entries |
| TC-E2-009-03 | AC3, BR3 | System | case-intake 1.2.0: 200 recommendations, 170 accepted, 30 overridden |
| TC-E2-009-04 | AC4, BR2 | System | Case list 240, case facts 239 |
| TC-E2-009-05 | AC5, BR4 | System | Notice product dated 2026-12-14 |
| TC-E2-009-06 | AC6 | System | from 2026-12-15, to 2026-12-01 |
| TC-E2-009-07 | AC7, BR6 | System | deviation-screen 0.9.0 with no runs |
| TC-E2-009-08 | AC8, BR7 | System | Filter MORTGAGE |
| TC-E2-009-09 | AC9, BR5 | System | JOB-15 rerun for 2026-12-15 |
| TC-E2-009-10 | Access | Access | PT-LAWFIRM calls GET /reports/measures; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: measures, formulas, tolerance and bands are data.
- No personal data in logs, tests or prompts. Measures carry counts, rates, amounts and codes only; agent outputs are counted, never copied.
- No read of another module's tables. Every fact comes through the owning module's reporting interface.
- Counts on SCR-37 and in Power BI come from the same measure_snapshot rows.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-009 | Steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-OCC-12, FEAT-RPT-03, FEAT-RPT-08 | 15 Manage performance, data and AI | None; NFR-065 and NFR-066 apply | TC-E2-009-01, TC-E2-009-03, TC-E2-009-05, TC-E2-009-06, TC-E2-009-07, TC-E2-009-09, TC-E2-009-10 |
| REQ-WKM-006 | Queue counts and ageing reported daily and reconciled to the case list | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-RPT-08 | 15 Manage performance, data and AI | None; DL25 applies | TC-E2-009-02, TC-E2-009-04, TC-E2-009-08 |

## 19. Out of scope

- Queue measures and service level breaches for team managers (RWB-E1-030, RWB-E2-011).
- The agent monitoring dashboard with latency and cost (RWB-E2-031).
- Benefit realisation against the baseline (FEAT-RPT-06, Epic 6).
- Regulatory returns (FEAT-RPT-07, Epic 8).
