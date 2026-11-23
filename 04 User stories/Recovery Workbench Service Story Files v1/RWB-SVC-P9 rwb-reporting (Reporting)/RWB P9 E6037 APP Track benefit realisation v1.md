# RWB-P9-E6037-APP Track benefit realisation

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E6037-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P9-D |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P9-E6037-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the benefit-realisation slice of RWB-E6-037 for rwb-reporting — the monthly comparison of every measure of the benefit model against the frozen baseline, computed from the decision log and the event-derived read model, the monthly step of the existing JOB-15 run, one local decision record per month, and `GET /reports/measures` with the baseline comparison — is split from the published shapes (RWB-P9-E6037-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **finance and CFO delegate (RW-FINANCE)**, I want **each measure of the benefit model shown for a closed calendar month beside its frozen baseline, computed from the decision log and the events of the month and recorded with the definition version and the rule version in force**, so that **the benefit the programme claims is read from the same record the teams work on, and not counted by hand from spreadsheets at month end**.

Inside rwb-reporting this is the benefit half of RWB-E6-037:

- service `rwb-reporting`, schema `rwb_reporting`, REST base `/api/recovery/reporting/v1`, topic `rwb.reporting.events.v1` with event names `rwb.reporting.<Event>.v1`, Temporal task queue `rwb-reporting` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.reporting` (DP-13);
- the read model of the month built from events and from the decision record of every decision (`DecisionRecorded`, EV-08, on `rwb.decision-record.v1`), with no data lake and no ACE view read by this service (DP-17, DP-05);
- one local decision record per closed month — the tracking record with the measure set, the baseline date and the definition version — written before the month's rows are published and relayed on `rwb.decision-record.v1` (DP-03);
- the month's rows written to `measure_snapshot` in `rwb_reporting`, beside the frozen baseline rows of 2026-11-27, which are never rewritten (DP-01);
- `GET /reports/measures` on the per-service base, each value beside its `baselineValue` with `variance` and `variancePercent`, served to SCR-37 through the gateway-bff composite route (DP-13, DP-19).

Not here: the published shapes, the error model and the fakes (RWB-P9-E6037-CON); the baseline measure set, `measure_definition` and the frozen baseline of 2026-11-27 (RWB-P9-E1013-APP and RWB-P9-E1013-CON); the steering measures and the daily publish or hold of JOB-15 (RWB-P9-E2009-APP and RWB-P9-E2009-CON); the deployment, the topics and the runbook (RWB-P9-E2009-OPS); regulatory returns of FEAT-RPT-07 (RWB-E8-001) and the classification and re-ageing of FEAT-RPT-10 (RWB-E8-002).

### 2. Business rationale

The benefits of the programme are measured today by hand from spreadsheets at month end, after the month has closed and after the numbers have been argued over. FEAT-RPT-06 asks for the opposite: the measures of the benefit model tracked against the baseline, monthly, from the decision log. The baseline exists from Epic 1 — six measures under definition version "MD-2026.11", frozen on business date 2026-11-27 (RWB-P9-E1013-APP) — and the daily measures exist from Epic 2 (RWB-P9-E2009-APP). What no story owns is the comparison: a month's value, the baseline value, the variance, and the record that says which definition version and which rule version produced them.

RWB-E6-037 is three lines of behaviour and three facts. The behaviour is: track the measures against the baseline monthly, record the result with the rule version, and stop if the record cannot be written. The facts are the decision log entry, the score rows and the rule rows it reaches in the monolith through `DecisionLogApi`, `v_ace_score` and the rule table. Under D-RCV-60 all four things move, and they move for one reason: a benefit number that cannot be reproduced is not a benefit number.

- **the facts become events.** The month's facts arrive on the events of the services that own them and on `rwb.decision-record.v1`; rwb-reporting reads no `v_ace_score` row and calls no Java interface of another module (DP-17, DP-05).
- **the baseline is data.** The baseline is not recomputed and not typed in: it is the frozen `measure_snapshot` rows of 2026-11-27 read beside the month, so a benefit number cannot drift because a spreadsheet was refreshed (DP-01).
- **the record is written first.** The tracking record is a local decision record committed in the same transaction as the month's rows, so a month that cannot be recorded is a month that is not published (DP-03).
- **the screen is one route.** The Finance delegate reads the benefit view on SCR-37 through the gateway-bff composite route, which merges the reporting answer with the case-side and decision-side answers of the same screen (DP-19).

That is why the story is small and the risk is not: every failure here looks like a number, not an error.

### 3. Preconditions

- RWB-P9-E6037-CON is published: the additive change to `GET /reports/measures` — the `baselineDate` parameter, the `baselineValue`, `variance` and `variancePercent` row fields and the `X-Data-As-Of` header — its error model and its contract fakes. The field names of the three added properties are Not specified in the source documents (GAP-2580; ASM-4256).
- RWB-P9-E1013-APP is done: `measure_definition` holds definition version "MD-2026.11" with the six measures "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE", and the baseline rows of business date 2026-11-27 are written and frozen.
- The JOB-15 run of RWB-P9-E2009-APP exists as the Schedule `reportingMeasuresDaily` at 01:30 on queue `rwb-reporting`, with its workflow, its activities and its read-model loader; this story adds one step to it and no workflow, no activity of its own task queue registration and no Schedule.
- The decision-record library RWB-PLT-E1027-CON is published, so the month's tracking record is written in the caller's transaction and relayed on `rwb.decision-record.v1` (DP-03).
- The gateway-bff composite route RWB-PLT-N001-CON is published, so the benefit section of SCR-37 is composed at the edge and the browser calls one route (DP-19).
- Which measures belong to the benefit model is Not specified in the source documents (GAP-2579; ASM-4251): the assumed rule is the measures of the definition version in force that hold a frozen baseline row, membership being data and never code.
- Which business day of the new month runs the monthly step, and how a month is keyed in `measure_snapshot`, are Not specified in the source documents (GAP-2579; ASM-4252; ASM-4253).
- The service runs as login `rwb_reporting` on schema `rwb_reporting`, holds no grant on another `rwb_*` schema, reads no `v_ace_*` view and writes no other service's table (DP-01, DP-05).
- No build dependency outside the three contract stories; Day 1 by rule (Template and Rules §R5.7), because every H dependency is a contract.

### 4. Flow

1. The Schedule `reportingMeasuresDaily` opens the JOB-15 execution of business date D, with the execution id derived from D so a rerun joins the run (RWB-P9-E2009-APP, DP-10 inherited).
2. D is the first business date of a new calendar month, so the run opens the benefit step for the closed month M (the assumed timing; GAP-2579; ASM-4252).
3. `loadBenefitModel` reads the measures of the definition version in force that hold a frozen `measure_snapshot` row, with their data product, unit and dimension, from `measure_definition` and the baseline rows (GAP-2579; ASM-4251).
4. `loadBenefitReadModel` replays the events of M — `CaseCreated` and `CaseStateChanged` on `rwb.case.events.v1`, `TreatmentApproved` on `rwb.treatment.events.v1`, `LotAwarded` on `rwb.debtsale.events.v1`, `WriteOffApproved` on `rwb.writeoff.events.v1`, `NoticeDispatched` on `rwb.comms.events.v1`, `FileDelivered` on `rwb.integration.events.v1` — and `DecisionRecorded` on `rwb.decision-record.v1`, deduplicated on the event id and ordered per case by the sequence of the outbox (DP-17).
5. The data-product date of each source of M is read on the rwb-source-data readiness answer; a source whose last complete day is before the end of M marks the affected measure with that date instead of the month's, and raises MSG-P1-001 (DP-05).
6. `computeBenefit` computes each measure of M from the facts by the formula of its definition row — counts, amounts, days or percentages — and pairs it with the baseline value of the same measure, product and dimension.
7. `variance` is the month value less the baseline value and `variancePercent` is the variance over the baseline value when the baseline value is not zero; both are computed and never stored (GAP-2579; ASM-4256).
8. In one `rwb_reporting` transaction the step writes the month's `measure_snapshot` rows under the dimension of each measure, keyed by the last business date of M, with the definition version in force, and writes one local decision record naming the measure set, the baseline date 2026-11-27, the definition version and the rule version in force (DP-03, DP-01; GAP-2579; ASM-4253).
9. A measure with no frozen baseline row writes no variance, is flagged as having no baseline and never blocks the month (AC4).
10. `GET /reports/measures?from=<first day of M>&to=<last day of M>&baselineDate=2026-11-27` answers the month's rows on `/api/recovery/reporting/v1`, filtered by measure, product and route, with the scope of the role applied and the business date in `X-Data-As-Of` (DP-13).
11. A rerun of the same month replaces the month's rows with the same values, writes no second decision record and leaves the frozen baseline untouched (AC5).
12. SCR-37 shows the benefit section through the gateway-bff composite route, which calls rwb-reporting once for the measures and merges them with the rest of the screen (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no month row and no record; the read answers nothing for the month and the run is retried | MSG-P7-003 | AC2, AC5 |
| X2 | A source of M is stale | The affected measure carries the stale data-product date, the stale flag and its date, and the rest of the month publishes | MSG-P1-001 | AC3 |
| X3 | A measure of the definition version has no frozen baseline row | No variance and no percentage is written for it; the row is flagged as having no baseline | None | AC4 |
| X4 | The period sent to the read is inverted | Refused before any read, naming the two fields | MSG-GEN-003 | AC6 |
| X5 | A required query field is empty | Refused before any read, naming the field | MSG-GEN-001 | AC6 |
| X6 | The role lacks Reporting R | The read is refused and nothing is returned | MSG-P4-002 | AC6, TC-E6-037-03 |
| X7 | The month holds no fact — no case, no decision, no treatment and no notice moved in M | The month writes its rows with zero counts and no rate rows, and publishes | None | AC3 |
| X8 | A rerun of a month already published | The rows are replaced with the same values and no second record is written | None | AC5 |
| X9 | The read model loader reaches another service's schema, a `v_ace_*` view or the data lake | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17 |
| X10 | A measure code, a formula, a unit or the baseline date is written as a constant | The definition-rows test fails the build | None (pipeline log) | Section 17 |

X1 to X3 are the exception paths that RWB-E6-037 fixes in AC2 and in the data of the feature; X4 to X10 are the paths the microservice adds. No path publishes a month whose record could not be written, and no path writes a measure code, a formula, a unit or a baseline date as a constant.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against RWB-P9-E6037-CON, the decision-record library and the composite route; the events of the month are replayed from fixtures, with no live neighbour |
| Negotiable | The step, activity and calculator names, the read-model shape and the run summary are this story's choice; the measures, the baseline, the messages and the recorded facts are fixed |
| Valuable | The benefit the programme claims is read from the decision log and reproduced from the frozen baseline |
| Estimable | One step on the existing workflow, two activities, one calculator, one record, one read and one screen section |
| Small | Fits one sprint with its tests |
| Testable | Each criterion runs against a synthetic month built from event fixtures and the baseline rows of 2026-11-27 |

### 7. Acceptance criteria

```gherkin
Feature: Track benefit realisation

  Background:
    Given definition version "MD-2026.11" is in force with measures "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE"
    Given the baseline rows of business date 2026-11-27 are frozen with "CASES_BY_ROUTE" 120 cases and "REALIZED_RECOVERY" 4,350,000.00 THB
    Given the closed calendar month of 2026-12-01 to 2026-12-31 holds 138 cases entered and 4,912,000.00 THB of realised recovery

  Scenario: AC1 Track benefit realisation (legacy RWB-E6-037 AC1)
    Given the rwb-source-data contract mock returns the data this feature needs
    Given the rwb-decision contract mock returns the rule version this feature needs
    When the user acts on the screen
    Then tracks the measures in the benefit model against the baseline, monthly
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E6-037 AC2)
    Given the rwb-decision contract mock returns the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The month is computed from the decision log and the events (new, D-RCV-60)
    Given the events of 2026-12-01 to 2026-12-31 hold 138 CaseCreated events and 1,412 DecisionRecorded events
    Given the readiness answer of rwb-source-data reports every source of the month complete to 2026-12-31
    When the benefit step runs for the closed month in the JOB-15 execution of 2027-01-01
    Then measure_snapshot holds a row for each of the 6 measures of "MD-2026.11" with business date 2026-12-31 and the definition version
    Then "CASES_BY_ROUTE" for 2026-12-31 is 138 cases
    Then "REALIZED_RECOVERY" for 2026-12-31 is 4,912,000.00 THB
    Then no measure code, formula, unit or baseline date is read from code, and each is read from measure_definition or from the request

  Scenario: AC4 The variance is taken against the frozen baseline (new, D-RCV-60)
    Given the month rows of AC3 are published
    Given measure "COST_PER_CASE" is listed for the benefit model and holds no frozen baseline row
    When the benefit step runs for the closed month
    Then "REALIZED_RECOVERY" carries baselineValue 4,350,000.00, variance 562,000.00 and variancePercent 12.92
    Then "CASES_BY_ROUTE" carries baselineValue 120, variance 18 and variancePercent 15.00
    Then no variance and no variancePercent is written for "COST_PER_CASE" and its row is flagged as having no baseline
    Then the baseline rows of 2026-11-27 are unchanged, still frozen and still marked baseline

  Scenario: AC5 One record per month and a rerun changes nothing (new, D-RCV-60)
    Given the month of 2026-12 has been published and its tracking record exists
    When the benefit step runs again for the same month
    Then the month rows hold the same values and the same business date
    Then no second decision record is written and the existing record keeps its rule version and definition version
    Given the local decision-record store is unavailable
    When the benefit step runs for the month of 2027-01
    Then no measure_snapshot row is written for 2027-01 and nothing is published
    Then the run record carries MSG-P7-003 and the next run publishes the month

  Scenario: AC6 The Finance delegate reads the month beside the baseline (new, D-RCV-60)
    Given user "U-9001" holds RW-FINANCE, whose Reporting letter is "R"
    Given the month of 2026-12 is published
    When "U-9001" calls GET /api/recovery/reporting/v1/reports/measures?from=2026-12-01&to=2026-12-31&baselineDate=2026-11-27
    Then the answer holds one row per measure of "MD-2026.11" with value, baselineValue, variance and variancePercent for the period "2026-12"
    Then the header X-Data-As-Of carries 2026-12-31
    Given a user holding a role without the Reporting right
    When the same operation is called
    Then the call is refused with status 403 and MSG-P4-002 and no row is returned

  Scenario: AC7 SCR-37 shows the benefit section read only (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-37 for the period 2026-12
    Given the month of 2026-12 is published
    When the Finance and CFO delegate opens SCR-37
    Then the benefit section shows the month, the six measures, each value beside the baseline of 2026-11-27 and the variance
    Then the stale flag and its date appear for a measure whose source is stale
    Then the screen builds no number of its own and offers no action that changes a measure, a baseline or a record
    And the browser calls one composite route and no owner service directly
```

AC1 and AC2 are the legacy criteria of RWB-E6-037, copied word for word with the origin tag added to the `Scenario` line: the repeated `Then` of AC1, the words "the data", "the rule version", "the screen" and "the decision log" all stand, and the cross-service part of each `Given` is expressed by the contract mock it runs against — `rwb-source-data` for the data and `rwb-decision` for the rule version and the decision log. AC3 to AC7 are new for the rwb-reporting slice and test only the deliverable of the title: the month's computation, the variance against the frozen baseline, the one record per month, the read and the screen section. The month, the case count, the amounts and the test user are synthetic fixtures of the same kind as the FSD examples, and no measure value of a real month is fixed here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A benefit measure is computed from Workbench records and the decision log, never from a separate count and never by hand | NFR-065; FSD P9 A2.6; FEAT-RPT-06 |
| BR2 | The measures of the benefit model are the measures of the definition version in force that hold a frozen baseline row; membership is data, never code | Principle 1; FSD P9 BR-P9-006 |
| BR3 | Each month is shown beside the frozen baseline of the same measure, product and dimension, and the baseline rows are never rewritten | RWB-E1-013 baseline 2026-11-27; FSD P9 BR-P9-006 |
| BR4 | Variance is the month value less the baseline value; variance percent is the variance over the baseline value and is written only when the baseline value is not zero | Derived from BR3; GAP-2579; ASM-4256 |
| BR5 | The month, the baseline date, the definition version and the rule version in force are recorded in one local decision record before the month is published | Legacy AC1; DP-03; Principle 5 |
| BR6 | A month that cannot be recorded is not published: no row and no record | Legacy AC2; MSG-P7-003 |
| BR7 | A source that is stale marks its measure with the stale data-product date; the measure is never silently computed from an older month | FSD P9 VR-P9-006-1; MSG-P1-001 |
| BR8 | A measure with no baseline row is shown without a variance and never blocks the month | Derived from BR2; FSD P9 A2.6 |
| BR9 | The same month twice writes the same rows once and one record; the month key and the definition version carry the rule | Legacy AC1; BR5 |
| BR10 | Every read applies the role's scope and the Reporting right, and a read writes nothing | TSD P9 T6.1, T6.2 |
| BR11 | No measure code, formula, unit, age band, data product or baseline date is a constant; each is a data row or a request value | Principle 1; FSD P9 BR-P9-006; VR-P9-006-1 |
| BR12 | The month's facts arrive on events; rwb-reporting reads no other service's table and no `v_ace_*` view | DP-01; DP-05; DP-17 |
| BR13 | The month's rows and the baseline rows are the same `measure_snapshot` table of this service, so the comparison cannot read two different stores | DP-01; FSD P9 A2.6 |

### 9. State transitions

None of a case: RWB-E6-037 says so and this slice keeps it. The states here are the tracking state of a month and the execution state of the run.

| From (month state) | Event | Condition | To |
|---|---|---|---|
| Not existing | The benefit step completes and the record commits | BR5 holds and every measure of BR2 is computed | Published, with the month rows and one record |
| Not existing | The record cannot be written | BR6 fails | Not published; the month is retried by the next run |
| Published | A rerun of the same month | BR9 | Published with the same values and the same record |
| Published | A measure added to the definition version later | BR2 does not apply to a closed month | Unchanged; the new measure starts with the next month |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery service identity of rwb-reporting (`rwb_reporting`) | Runs the benefit step, loads the month's facts, computes the measures and writes the month rows and the record; holds no grant on another `rwb_*` schema |
| The local decision-record library (RWB-PLT-E1027-CON) | Writes the month's tracking record in the caller's transaction and publishes `DecisionRecorded` on `rwb.decision-record.v1` (DP-03) |
| RW-FINANCE, Finance and CFO delegate | Reads the benefit section of SCR-37 and the measures of a month (Reporting R) |
| RW-BIANAL, Reporting and BI analyst | Reads the measures, the definition versions and the variance, and receives the stale alert (Reporting CRUD) |
| RW-TRIBE, Tribe lead and squad members | Reads a month beside the baseline (Reporting R) |
| RW-PRODHEAD, product head | Reads a month for the products in scope (Reporting R) |
| RW-DATASTEW, data steward | Receives the stale alert and reads the data-product date behind a measure (Reporting CRU) |
| RW-AUDIT, internal audit | Reads the record of a month and its variance (Reporting R) |
| A role holding no Reporting right | Refused on the read with MSG-P4-002 |

The rights are the rows of TSD P9 T6.1 and of the legacy permission table, and nothing wider. No person is named: every duty is a role.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-RPT-032, DF-RPT-034, DF-RPT-035, DF-RPT-036, DF-RPT-037, DF-RPT-040 | `measure_definition` (P9) | measure_code, formula, data_product, unit, definition_version, valid_from | Read, to fix the measure set and the formula of each measure |
| DF-RPT-042 to DF-RPT-052 | `measure_snapshot` (P9) | measure_code, definition_version, business_date, product_group, dimension_code, dimension_value, value, case_count, is_baseline, frozen, published_at | Read for the frozen baseline rows of 2026-11-27; write for the month's rows |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (PLT library, created in `rwb_reporting`) | the record of the month: measure set, baseline date, definition version, rule version and outcome | Write, one row per month |
| DF-DEC-003, DF-DEC-007, DF-DEC-012, DF-DEC-013, DF-DEC-016 | `decision_log_entry` (P7) | decision_code, agent_version, final_call, override_reason, decided_at | Read on the read model of `DecisionRecorded` (EV-08); never as a table |
| DF-CAS-001, DF-CAS-003, DF-CAS-005, DF-CAS-008, DF-CAS-010, DF-CAS-013 | `recovery_case` (P3) | id, product_group, status, stage_code, route_code, entry_date | Read on the read model of `CaseCreated` and `CaseStateChanged`; never as a table |
| DF-TRT-004, DF-TRT-013 | `treatment` (S2) | treatment_type, outcome | Read on the read model of `TreatmentApproved` |
| DF-LEG-018, DF-LEG-019, DF-LEG-022 | `notice` (P6) | notice_type, sent_date, delivery_status | Read on the read model of `NoticeDispatched` |
| The payment and write-off facts of the month (field IDs Not specified in the source documents (GAP-2579; ASM-4255)) | `write_off` (S7), `debt_sale_lot` (S6) | the amount realised in the month | Read on the read model of `WriteOffApproved` and `LotAwarded`; never as a table |

Field IDs are those of the Logical Data Model and Data Dictionary v8 and of TSD P9 T3.1. `measure_publish` is not written by this story: the daily publish or hold of a business date stays RWB-P9-E2009-APP's. No table is added and no migration is needed, because `measure_snapshot` already carries the definition version, the baseline flag and the frozen flag; how a month is keyed when no month column exists is Not specified in the source documents (GAP-2579; ASM-4253). No personal data is written: measure codes, codes, counts, amounts, days, percentages, dates and a definition version only.

### 12. Contract

#### 12.1 REST operations provided

None added by this story. It supplies the behaviour behind `GET /api/recovery/reporting/v1/reports/measures` — the operation the Ownership Map gives P9 rwb-reporting — whose published shape is RWB-P9-E6037-CON and whose first build is RWB-P9-E2009-APP.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/reports/measures` | API-P9-001: a list of `Measure` — measure, product, route, period, value, dimension, `baselineValue`, `variance`, `variancePercent` — filtered by `measure`, `product`, `route`, `from`, `to` and `baselineDate`, with `X-Data-As-Of` | Reporting, right R, scope applied | Not applicable; a read writes nothing |

#### 12.2 REST operations consumed

None. The month's facts arrive on events and the data-product dates on the readiness answer of rwb-source-data, which runs as an activity on the owner's queue and returns its answer to the workflow (DP-05, DP-17). No REST call of another service is made by this story, so the two-second one-hop budget of ADR-020 is not exercised and no breaker is configured.

#### 12.3 Events published

| Event | Topic | Trigger | Payload used |
|---|---|---|---|
| `DecisionRecorded` (EV-08), the local record of a tracked month | `rwb.decision-record.v1`, owned by rwb-decision | The month's transaction commits | the record id, the month, the baseline date, the definition version, the rule version and the outcome; no measure value |

The service topic `rwb.reporting.events.v1` carries no event type of this view (GAP-2580; ASM-4258); the publish marker of a measure run belongs to the Epic 1 measure story and is not published here. `DecisionRecorded` is written by the local library to this service's outbox on the shared topic (DP-03).

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When |
|---|---|---|---|---|
| `CaseCreated` (EV-01), `CaseStateChanged` (EV-05) | `rwb.case.events.v1` | `rwb-reporting.case.v1` | the case id, product group, stage, route and entry date; CASES_BY_ROUTE, CASES_BY_AGE, CASES_BY_QUEUE, TIME_IN_STAGE | replayed for the month of the run |
| `DecisionRecorded` (EV-08) | `rwb.decision-record.v1` | `rwb-reporting.decision.v1` | the decision code, the time and the rule version; the decision measures and BR1 | as above |
| `TreatmentApproved` (EV-10) | `rwb.treatment.events.v1` | `rwb-reporting.treatment.v1` | the treatment id, case and outcome | as above |
| `LotAwarded`, `AccountsTransferred` | `rwb.debtsale.events.v1` | `rwb-reporting.debtsale.v1` | the lot, the case and the amount realised | as above |
| `WriteOffApproved` | `rwb.writeoff.events.v1` | `rwb-reporting.writeoff.v1` | the write-off id, the case and the amount | as above |
| `NoticeDispatched` (EV-14) | `rwb.comms.events.v1` | `rwb-reporting.notice.v1` | the notice id, case, type and sent date | as above |
| `FileDelivered` | `rwb.integration.events.v1` | `rwb-reporting.integration.v1` | the interface, the business date and the delivery result | as above |

The consumer groups are declared once by RWB-P9-E6037-CON and registered by RWB-P9-E2009-OPS. The run replays a bounded window — the month and the look-back of the age measures — rather than consuming continuously, so no read-model table is added and a repeat is deduplicated on the event id. The money facts of the month arrive on the debt-sale and write-off events of S6 and S7, the services the connection matrix gives this row of P9.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `reportingMeasuresDaily` (JOB-15, owned by RWB-P9-E2009-APP) | Workflow, one execution per business date | `rwb-reporting`, namespace `rwb-recovery` | This story adds one step to it; it adds no workflow and changes no input |
| `loadBenefitModel` | Activity | `rwb-reporting` | the measures of the definition version in force with a frozen baseline row in; the measure set with its formulas out |
| `loadBenefitReadModel` | Activity | `rwb-reporting` | the events of the month in; the run-scoped month fact view out, deduplicated on the event id |
| `computeBenefit` | Activity | `rwb-reporting` | the month fact view and the baseline rows in; the month rows with value, baselineValue, variance and variancePercent out |
| `recordAndPublishBenefit` | Activity | `rwb-reporting` | the one transaction: the local decision record and the month rows |

The step and activity names are this story's design choice: no source names the step that tracks benefit realisation, and JOB-15 is the one job the ownership row of the service carries (GAP-2579; ASM-4252).

#### 12.6 Schedules

None added. The 01:30 daily Schedule `reportingMeasuresDaily` is RWB-P9-E2009-APP's and this story only opens the benefit step inside its first execution of a new month; no cron entry, no second Schedule and no Quartz row is created. The bank's Airflow may trigger the same workflow by its start signal and calls no schema.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `measure_definition` | P9 (`rwb_reporting`) | The definition in force per measure and version; read only here (RWB-P9-E1013-APP is its writer) |
| `measure_snapshot` | P9 (`rwb_reporting`) | The frozen baseline rows of 2026-11-27 read; the month's rows written; the baseline is never rewritten |
| `decision_record` | PLT library, created in `rwb_reporting` | The month's tracking record, hash-linked, written in the same transaction (DP-03) |
| `outbox_event`, `processed_event` | PLT library, created in `rwb_reporting` | The outbox row of the record and the inbox of the replayed events (DP-09) |

Never read as a table: `recovery_case`, `queue` and `timer` (P3), the treatment record (S2), the notice record (P6), the write-off and debt-sale records (S7, S6), `decision_log_entry` (P7) and every `v_ace_*` view. No foreign key leaves the schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-reporting OpenAPI fake | `GET /reports/measures` for 2026-12-01 to 2026-12-31 with the six measures, each beside its baseline of 2026-11-27 and its variance, with `X-Data-As-Of` 2026-12-31; a 403 without Reporting R; a 422 on a reversed period; an empty month | AC6, AC7, TC-E6-037-03 |
| Event fixtures of the seven event types | the synthetic month: 138 CaseCreated, 1,412 DecisionRecorded, the treatments, lots, write-offs and notices of the month, and a month with nothing in it | AC3, AC4 |
| Baseline fixture | the frozen rows of 2026-11-27 with CASES_BY_ROUTE 120 and REALIZED_RECOVERY 4,350,000.00, and a measure with no baseline row | AC4 |
| rwb-source-data readiness fake | every source complete to 2026-12-31, and one source stale to 2026-12-14 with MSG-P1-001 | AC3, X2 |
| Local decision-record stub | a healthy chain returning the sequence and the entry hash, and a stopped chain returning MSG-P7-003 | AC2, AC5 |
| gateway-bff composite route fake | the merged SCR-37 answer with the benefit section, the stale flag and the period selector | AC7 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided by this story, 0 consumed | The read is provided by RWB-P9-E6037-CON; no cross-service REST call is made |
| Kafka | 1 published by the library, 7 consumed | `DecisionRecorded` on `rwb.decision-record.v1`; the case, treatment, debt-sale, write-off, comms and integration events replayed for the month |
| Temporal | 1 workflow inherited, 4 activities | The benefit step of `reportingMeasuresDaily` on `rwb-reporting`; no Schedule added |
| File | None | No file is read or written; the extract hand-over stays RWB-P9-E2009-APP's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.reporting`, module `benefit`, Java package `th.co.scb.ace.workbench.recovery.reporting.benefit`; front end `src/modules/recovery/reporting/BenefitSection.tsx`, the fragment SCR-37 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`: one record per month, written before the month rows | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract — the readiness answer on its queue — or, for a monitoring measure, the service's own projection; rwb-reporting reads no `v_ace_*` view | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for the benefit section of SCR-37 | H RWB-PLT-N001-CON |

No pattern is claimed outside this list: the month runs on the Schedule that already exists, so DP-10 is not applied here, and the story writes no decision-log entry of another service, so the shared ledger stays P7's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `BenefitStep` | Step of the existing workflow | Opens the month, sequences the two loaders and the calculator, and commits the month |
| `BenefitModelLoader` | Service | Reads the measures of the definition version in force with a frozen baseline row and their formulas |
| `BenefitReadModel` | Service | Replays the month's events into a run-scoped fact view, deduplicated on the event id |
| `BenefitCalculator` | Service | One calculator per measure driven by the definition rows; value, baselineValue, variance and variancePercent |
| `MonthWriter` | Repository | Writes the month rows to `measure_snapshot` in schema `rwb_reporting` only |
| `BenefitRecordWriter` | Library adapter | Writes the month's local decision record with the definition version and the rule version, in the same transaction (DP-03) |
| `MeasureController` | Controller | `GET /reports/measures` with the period, the baseline date, the scope and `X-Data-As-Of` |
| `BenefitSection` | React component | The benefit section of SCR-37: month, measures, baseline, variance and stale flag, read only |

**Build steps**

1. Take RWB-P9-E6037-CON tagged, and add the `baselineDate` parameter, the three row fields and the header to the query of `MeasureController`; test the shape of AC6.
2. Build the month fixtures of the seven event types and `BenefitReadModel`; test the replay and the deduplication of AC3.
3. Build `BenefitModelLoader` and `BenefitCalculator`; test the six measures of AC3 and the calculated variance of AC4.
4. Build `MonthWriter` and `BenefitRecordWriter` in one transaction; test AC5 and the failed-record path of X1.
5. Build the stale flag and the date from the readiness answer; test X2.
6. Build the read with the period check, the scope and the header; test AC6 and the refusal of X6.
7. Build the `BenefitSection` of SCR-37 and the composite-route contract test; test AC7.
8. Replay one month twice and compare the rows byte for byte; test BR9.

**Feature switch.** `rwb.p9.benefit-tracking`, a service configuration value read as a parameter. Off: the step records the month as not tracked and publishes nothing; on: the step computes and publishes the month.

**Done when.** The tests of section 16 pass, one SIT month is published with its record, the baseline rows of 2026-11-27 are unchanged, and a rerun of the same month writes the same values and no second record.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required query field is empty | Enter {field}. |
| MSG-GEN-003 | The period sent is inverted | {field} cannot be before {other}. |
| MSG-P4-002 | The role lacks the Reporting right | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The month's record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | A source of the month is stale | {product} is from {date}. Today's ACE batch has not arrived. |

The first four texts are the legacy texts of RWB-E6-037 section 14, unchanged; MSG-GEN-003 and MSG-P1-001 are the FSD P9 texts of A2.6 and the platform texts the split adds. A message names a measure code, a product, a count and a date, and never a case, an account or a customer value.

### 15. Screens and states

SCR-37 Steering dashboard (capability area Reporting) carries the benefit section; the legacy story says "No screen in this story", and the screen the FSD A2.6 names for the Finance and CFO delegate is assumed to be this section of SCR-37 rather than a new screen (GAP-2579; ASM-4254).

| State | What the user sees and does |
|---|---|
| Loading | Skeleton rows while `GET /reports/measures` returns |
| Published month | The month, the six measures, each value beside the baseline of 2026-11-27 and the variance, with the business date |
| Stale | The measure, its stale date and MSG-P1-001 for the source that has not arrived |
| No baseline | A measure without a frozen baseline row, shown with no variance and the reason |
| No tracking | The month not tracked yet, with no value and no action |
| Error | MSG-P4-002, MSG-GEN-001, MSG-GEN-003 or MSG-P7-003 with its field names and no partial value |

The section builds no number of its own: it renders the published rows and their stamps. The screen field order, the masking and the merge order belong to RWB-PLT-N001-CON, and the editable states of SCR-37 stay with the stories that own them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-037-01 | AC1, AC3 | Component | Synthetic month 2026-12: 138 cases, 1,412 decisions, 4,912,000.00 THB realised |
| TC-E6-037-02 | AC2, AC5 | Component | Local decision-record store stopped on the month of 2027-01 |
| TC-E6-037-03 | Access, AC6 | Contract | A role without Reporting R calls GET /reports/measures; refused with MSG-P4-002 |
| TC-E6-037-04 | Principle 5, AC2 | NFR | A forced record write failure leaves no month row and answers MSG-P7-003 |
| TC-P9-E6037-APP-05 | AC4 | Component | Baseline of 2026-11-27: CASES_BY_ROUTE 120, REALIZED_RECOVERY 4,350,000.00; a measure with no baseline row |
| TC-P9-E6037-APP-06 | AC5, BR9 | Component | The same month published twice; rows and record compared |
| TC-P9-E6037-APP-07 | AC7 | End to end | The composite route serves the benefit section of SCR-37 for 2026-12 |

The four legacy test cases of RWB-E6-037 are kept with their legacy IDs and their legacy order, with the legacy Level "Access" mapped to Contract and the legacy Principle 5 case mapped to NFR; the two criteria this slice adds carry their own IDs. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these IDs belong to the wave 4 integration harness.

### 17. Guardrails

- No business value in code: measure codes, formulas, units, data products, dimensions and the baseline date are data rows or request values, and the definition version is read, never written.
- No personal data in logs, tests, workflow history, events or prompts: measures carry counts, amounts, days, percentages, codes and a definition version only.
- No read of another service's tables and no ACE view: every fact arrives on an event or on its owner's contract (DP-01, DP-05, DP-17).
- The month's rows and the record are one transaction: a month that cannot be recorded is never published (DP-03).
- The baseline rows of 2026-11-27 are frozen: no path rewrites, unfreezes or recomputes them.
- A measure of a closed month is never silently recomputed from a partial source; the stale date stands beside the value.
- Every example is synthetic and every measure value of a real month comes from the run, never from a fixture promoted to production.
- No data lake and no Power BI target is written by this story; the extract hand-over stays RWB-P9-E2009-APP's (DP-17).

### 18. Traceability

The Epics 3 to 8 story RWB-E6-037 carries no requirement ID, so this story claims none (GAP-2579; ASM-4255). The trace goes through the legacy feature, the FSD criterion and the rules that the story applies.

| Requirement ID | Requirement (short) | Source section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (the legacy story carries no requirement ID) | Track the measures in the benefit model against the baseline, monthly | Recovery Workbench User Stories Epics 3 to 8 v3, RWB-E6-037, and FSD P9 A2.6 | FEAT-RPT-06 | 15 Manage performance, data and AI | BR-P9-006; VR-P9-006-1 | TC-E6-037-01, TC-E6-037-02 |
| D-RCV-60 DP-03 | The month is recorded locally in the same transaction and published on `rwb.decision-record.v1` | Template and Rules §R5.5 | FEAT-RPT-06 | 15 Manage performance, data and AI | BR5, BR6 | TC-E6-037-04, TC-P9-E6037-APP-06 |
| D-RCV-60 DP-05 | The data products of the month are read through rwb-source-data's answer; no ACE view is read by rwb-reporting | Template and Rules §R5.5 | FEAT-RPT-06 | 15 Manage performance, data and AI | BR7, BR12 | TC-E6-037-01 |
| D-RCV-60 DP-13 | The view is served on `/api/recovery/reporting/v1` | Template and Rules §R5.5 | FEAT-RPT-06 | 15 Manage performance, data and AI | BR10 | TC-E6-037-03 |
| D-RCV-60 DP-19 | SCR-37 is a gateway-bff composite route over rwb-reporting and the other owners of the screen, read only | Template and Rules §R5.5 | FEAT-RPT-06 | 15 Manage performance, data and AI | BR10 | TC-P9-E6037-APP-07 |
| NFR-065 | Business measures per decision are produced from the decision log and not from a separate count | TSD P9 T7 | FEAT-RPT-06 | 15 Manage performance, data and AI | BR1 | TC-E6-037-01 |

The legacy endpoint of RWB-E6-037 (`GET /reports/measures` under the monolith base) moves to the per-service base and keeps its operation path (DP-13); the legacy `v_ace_score` read and the rule table it names are replaced by the events of section 12.4 and by the definition rows of this service (DP-05, DP-17).

### 19. Out of scope

- The published shapes, the error model and the fakes of the read (RWB-P9-E6037-CON).
- The baseline measure set, `measure_definition`, the frozen baseline of 2026-11-27 and JOB-15's first build (RWB-P9-E1013-APP and RWB-P9-E1013-CON).
- The steering measures, the daily publish or hold and the extract hand-over (RWB-P9-E2009-APP and RWB-P9-E2009-CON), and the deployment, topics, alerts and runbook (RWB-P9-E2009-OPS).
- The decision log itself, its hash chain and the central ledger (rwb-decision, P7); this story writes a local record only.
- The event types of the month: they are owned and published by P3, S2, S6, S7, P6, P2 and P7.
- The regulatory returns of FEAT-RPT-07 (RWB-E8-001) and the classification and re-ageing of FEAT-RPT-10 (RWB-E8-002).
- The editable states of SCR-37 and the screen field list (RWB-PLT-N001-CON and the stories that own the screen).
- The cross-service journey harness and its evidence, when a wave 4 journey story is raised for this legacy key.
