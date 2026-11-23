# RWB-S8-E2009-APP Steering dashboard v1 data set

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E2009-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-S8-F |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P9-E2009-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to REQ-WKM-009, REQ-WKM-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the steering data set of RWB-E2-009 is realigned onto rwb-deviation (S8, service wave 2, business wave 2), as the secondary serving of the dashboard the split plan gives this service. The seven measure calculators, the count reconciliation, the agent rates and the SCR-37 read keep their legacy values; the facts behind them arrive on the owners' published contracts instead of the six in-process interfaces and the Workbench tables (DP-11), the definitions, the frozen baseline of 2026-11-27 and the publication rules are consumed on RWB-P9-E2009-CON, the read moves onto `/api/recovery/deviation/v1` (DP-13), JOB-15 becomes a Temporal Schedule through the workflow kit (DP-10), the INT-19 extract to Power BI is removed with the data lake (DP-17), and the schema, decision-record, reference-data, Flyway and route rules of the service apply (DP-01, DP-03, DP-07, DP-15, DP-19). The legacy module is P9 Reporting and the plan gives this slice no build row although six DP rows add a platform prerequisite, and the connection matrix carries no S8-to-P9 call and no P9 subscription to S8 (GAP-3087 to GAP-3090; ASM-5270 to ASM-5279). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **Tribe lead (RW-TRIBE)**, I want **a data set for the steering dashboard with cases by stage, queue and age, decisions logged, treatments, letters sent and agent acceptance, published each morning and reconciled to the case list**, so that **the steering committee reads the same numbers the teams work with**.

This story owns:

- the **measure answer** of the deviation serving on `/api/recovery/deviation/v1`: the seven measures of definition version "MD-2026.12" for a business-date range, each value beside the frozen baseline of 2026-11-27, with the business date, the definition version, the dimension and the freshness stamp (legacy section 12; DP-13);
- the **seven calculators**, one per measure code, and the **dimension** of each row (`product:`, `route:`, `agent:` and `deviation:`, for example `agent:case-intake:1.2.0`);
- the **deviation column** of the answer: the deviation codes X1 to X7 open on the counted cases at the cut-off, read from `deviation` in `rwb_deviation` (REQ-DVH-006; TSD S8 T3.1 and T3.2);
- the **count reconciliation** before a day is published: the sum of "CASES_BY_STAGE" against the count of the case list at the same cut-off, tolerance zero (legacy BR2; DL25);
- the **morning refresh**: Temporal Schedule `steering-measures` at 01:30 and `SteeringMeasureRefreshWorkflow` on queue `rwb-deviation`, which replaces JOB-15 in this service (DP-10);
- the **two agent rates** per agent and version, and the "No runs" answer for an agent with no recommendations;
- the **provenance record**: one decision-record entry per refresh run and per measure read, holding the definition version, the business date, the two counts and the verdict (DP-03).

It does not own: the canonical measure build, the `measure_definition`, `measure_snapshot` and `measure_publish` tables, the frozen baseline rows and the Power BI read model (RWB-P9-E2009-CON; rwb-reporting, P9); the case, treatment, decision, notice and agent facts (P3, P3, P7, P6 and P10); the deviation write path and its timers (`DeviationWorkflow`, the write stories of this service); the contract surface and its fakes; and the schema, migration, deployment and observability of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

The steering committee receives numbers counted by hand that differ from what the teams see in their queues (legacy section 2). The target keeps one measure set and one reconciliation rule, and makes the serving reproducible:

- **The facts are the owners' answers**, one hop each and with a fake on Day 1: the case facts and the case-list count from rwb-case, the decision facts from rwb-decision, the treatment facts from rwb-case, the notice facts from rwb-comms and the agent run facts from rwb-agent (DP-11). No service reads another service's tables and no Workbench copy of a fact is kept (DP-01).
- **The definitions are read, never coded**: the measure codes, formulas, data products, the definition version "MD-2026.12" and the baseline of 2026-11-27 are the reporting owner's rows, consumed on RWB-P9-E2009-CON; the lists the filters use are reference data of rwb-case at their version (DP-07).
- **A published day is a claim that can be checked**: the reconciliation of the dashboard total against the case list runs before the day is published, and a mismatch of one case holds the day (legacy BR2, DL25).
- **The deviation column is why this slice sits in S8**: `deviation` is this service's one table, and the codes open at the cut-off are read here rather than copied from a case column (DP-01, REQ-DVH-006; ASM-5271).
- **The morning run is a durable schedule**, not a Quartz row: the schedule survives a restart, catches up a missed night and can be rerun for one business date with the same values (DP-10).
- **No data lake**: the INT-19 extract and the Power BI data set of the legacy story are removed with the lake, and the reporting read model is built from events by rwb-reporting (DP-17; GAP-3088).

No business value moves into code: measures, formulas, tolerance, age bands, the schedule time and the labels are data.

### 3. Preconditions

- RWB-P9-E2009-CON is published and tagged: the measure definition read, the published measure and baseline read, the publication calendar and the error set are baselined, with their fakes, and handed to this story (DP-11; GAP-3087).
- The five platform contract stories the DP rows add are published: RWB-PLT-E1027-CON (decision record), RWB-PLT-E1043-CON (reference data), RWB-PLT-E1071-CON (workflow kit), RWB-PLT-E1044-CON (Flyway) and RWB-PLT-N001-CON (gateway-bff route); the plan's build row is empty and they are declared here as prerequisites (ASM-5272).
- The case, treatment, decision, notice and agent contracts answer with a business date per answer and a freshness answer for the latest business date; their operation names are not published (GAP-3087; ASM-5274).
- `deviation` exists in `rwb_deviation` from the DB story of this service with its columns and the standard record columns of TSD S8 T3.0; this story reads it and adds no table, no column and no migration.
- The service runs as its own login on `rwb_deviation`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_reporting` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-02).
- The role of the reader carries Reporting R and a scope; the lists of products, routes and measures are readable at their version (legacy sections 3 and 10; DP-07).
- No approval is needed to build against a Draft contract baseline; the status of the source documents is taken as an assumption and the story stays in Draft (ASM-5270).

### 4. Flow

1. Temporal Schedule `steering-measures` fires at 01:30 Asia/Bangkok on task queue `rwb-deviation` and starts `SteeringMeasureRefreshWorkflow` with the business date it closes (DP-10).
2. `ReadMeasureDefinitions` reads the definitions in force on RWB-P9-E2009-CON, including the seven steering measures of "MD-2026.12" and the frozen baseline rows of 2026-11-27 (DP-11).
3. `ReadFacts` reads the case facts, the case-list count at the cut-off, the treatment facts, the decision facts, the notice facts and the agent run facts of the business date, each on its owner's contract and each with its business date and freshness answer (DP-11).
4. `ComputeMeasures` runs one calculator per measure code and fills each row's dimension, value and `baselineValue`; `AgentRates` computes acceptance and override per agent and version, and writes no rate where the denominator is zero (legacy BR3, BR6).
5. `ReconcileCounts` compares the sum of "CASES_BY_STAGE" with the case-list count at the same cut-off; equal, the day is published; different, the day is held and `RaiseHoldAlert` sends MSG-P9-002 to the Reporting and BI analyst and the data steward (legacy BR2, DL25; DP-11).
6. `ReadDeviationColumn` reads the `deviation` rows open at the cut-off for the counted cases: code, raised-at, paused state and handler; a case with two codes shows both (TSD S8 T3.1; REQ-DVH-006).
7. `RecordProvenance` appends one decision-record entry through the local library with the definition version, the business date, the two counts and the verdict (DP-03).
8. A reader opens SCR-37 through the gateway-bff composite route; the screen calls `GET /reports/measures` with measure, product, route and date filters; the answer carries the published values with their business date and freshness stamp, the baseline beside each value and the header `X-Data-As-Of` (DP-19).
9. The screen shows the deviation codes of each counted row; an agent with no runs shows "No runs"; the latest published day is 2026-12-14 while 2026-12-15 is held (legacy AC4, AC7).
10. Nothing else is written: the story moves no case status, starts no workflow of another service and writes no measure table (DP-01).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The dashboard case count differs from the case-list count at the cut-off | The day is held; the previous day stays the latest published; the alert is sent | MSG-P9-002 | AC4 |
| X2 | A source answer behind a measure is stale for the business date | The value of the stale product shows with its own date | MSG-P1-001 | AC5 |
| X3 | A query with from after to | Refused before any read | MSG-GEN-003 | AC6 |
| X4 | An agent has no runs on the day | No rate is computed; "No runs" shows | None | AC7 |
| X5 | A refresh is rerun for a business date already published | The same values are answered and a second provenance entry is written; the baseline rows of 2026-11-27 are unchanged | None | AC9 |
| X6 | The role lacks Reporting R | 403 before any fact is read | MSG-P4-002 | TC-E2-009-10 |
| X7 | The reporting contract or the service's own schema does not answer | 503 with the platform envelope; nothing partial shows | MSG-GEN-006 | AC1, BR8 |

X1 to X5 are the paths of RWB-E2-009; X6 and X7 are the target's access and availability paths.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-P9-E2009-CON and six fakes (case, treatment, decision, notice, agent, notification), on its own schema, and needs no live P3, P6, P7, P9 or P10 |
| Negotiable | The calculator shape, the workflow activities and the dimension format are this story's choice; the measure codes, the values, the tolerance and the messages are fixed |
| Valuable | One set of numbers for the committee and the teams, with the deviation codes of the counted cases beside them |
| Estimable | Seven calculators, one reconciliation, one workflow with five activities, one schedule, one endpoint and one screen |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on the synthetic day of 2026-12-15 through the fakes, plus the access refusal and the boundary test |

### 7. Acceptance criteria

The split plan assigns this slice no legacy criterion (GAP-3089; ASM-5276), so the nine criteria are new under D-RCV-60 and keep the legacy scenario values of RWB-E2-009 word for word, with an owner's contract mock line in place of each read the legacy story took from a Workbench table or an in-process interface.

```gherkin
Feature: Steering dashboard v1 data set

  Background:
    Given definition version "MD-2026.12" is in force with measures "CASES_BY_STAGE", "CASES_BY_QUEUE_AGE", "DECISIONS_LOGGED", "TREATMENTS", "LETTERS_SENT", "AGENT_ACCEPTANCE" and "AGENT_OVERRIDE"
    Given the synthetic day 2026-12-15 holds 240 open cases, 1,412 decision log entries, 38 treatments and 95 notices sent
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Refresh (new, D-RCV-60)
    Given the loads of business date 2026-12-15 passed their checks
    Given the rwb-reporting contract mock returns definition version "MD-2026.12" and the baseline rows of 2026-11-27
    Given the rwb-case, rwb-decision, rwb-comms and rwb-agent contract mocks return the facts of 2026-12-15 with a fresh stamp
    When the steering measure refresh runs at 01:30 on 2026-12-16
    Then GET /reports/measures?from=2026-12-15&to=2026-12-15 returns a value for each of the 7 measures with period "2026-12-15"
    Then the answer for 2026-12-15 carries freshness stamp 2026-12-15 for the 07:30 refresh of SCR-37

  Scenario: AC2 Reconciles (new, D-RCV-60)
    Given the rwb-case contract mock returns 240 open cases at the 2026-12-15 cut-off
    Given the rwb-decision contract mock returns 1,412 decision log entries decided on 2026-12-15
    When the steering measure refresh runs at 01:30 on 2026-12-16
    Then the sum of "CASES_BY_STAGE" for 2026-12-15 is 240
    Then "DECISIONS_LOGGED" for 2026-12-15 is 1,412, the count of decision log entries decided that day
    Then the row of the stage of case RW-2026-000502 names deviation "X3", read from the service's own deviation rows

  Scenario: AC3 Agent measures (new, D-RCV-60)
    Given the rwb-agent contract mock returns agent "case-intake" version "1.2.0" with 200 recommendations on 2026-12-15, of which 170 were accepted and 30 overridden with a reason
    When the steering measure refresh runs at 01:30 on 2026-12-16
    Then "AGENT_ACCEPTANCE" for "case-intake" "1.2.0" on 2026-12-15 is 85.0 percent
    Then "AGENT_OVERRIDE" for "case-intake" "1.2.0" on 2026-12-15 is 15.0 percent
    Then SCR-37 shows both rates by agent

  Scenario: AC4 Counts do not match (new, D-RCV-60)
    Given the rwb-case contract mock returns 240 open cases at the 2026-12-15 cut-off
    Given the case facts read for the dashboard total 239
    When the steering measure refresh runs at 01:30 on 2026-12-16
    Then the day 2026-12-15 is held: no measure answer and no published verdict are returned for it
    Then SCR-37 shows 2026-12-14 as the latest day with MSG-P9-002 naming 239, 240 and 2026-12-15
    Then an alert goes to the Reporting and BI analyst and the data steward

  Scenario: AC5 Stale source (new, D-RCV-60)
    Given the notice data product is from 2026-12-14 because the 2026-12-15 load has not arrived
    When a product head opens SCR-37 on 2026-12-16
    Then "LETTERS_SENT" shows the value for 2026-12-14
    Then SCR-37 shows MSG-P1-001 naming "DP07 Legal" and 2026-12-14

  Scenario: AC6 Dates in the wrong order (new, D-RCV-60)
    Given a team manager holds RW-TEAMMGR with Reporting R
    When a team manager sends GET /reports/measures?from=2026-12-15&to=2026-12-01
    Then the response is status 422 with MSG-GEN-003 naming "from" and "to"

  Scenario: AC7 Agent with no runs (new, D-RCV-60)
    Given the rwb-agent contract mock returns no recommendation for agent "deviation-screen" version "0.9.0" on 2026-12-15
    When the steering measure refresh runs at 01:30 on 2026-12-16
    Then the system writes no "AGENT_ACCEPTANCE" value for "deviation-screen" on 2026-12-15
    Then SCR-37 shows "No runs" for "deviation-screen" on 2026-12-15

  Scenario: AC8 Filter by product (new, D-RCV-60)
    Given the measures for 2026-12-15 are published and the case list shows 140 open Mortgage cases at the cut-off
    When a product head sends GET /reports/measures?measure=CASES_BY_STAGE&product=MORTGAGE&from=2026-12-15&to=2026-12-15
    Then the response holds only rows with product "MORTGAGE"
    Then their sum is 140

  Scenario: AC9 Rerun of a published day (new, D-RCV-60)
    Given the measures for 2026-12-15 are published
    When the refresh is rerun for business date 2026-12-15 with that business date as its input
    Then the rows for 2026-12-15 hold the same values
    Then the frozen baseline rows of 2026-11-27 are unchanged
    Then a second provenance entry for the run is recorded with the same counts and verdict
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Steering measures are computed from the owners' published facts and the decision record, never from a separate count | NFR-065; REQ-WKM-009 |
| BR2 | The dashboard case count equals the case-list count at the same cut-off, or the day is held; the tolerance is zero | REQ-WKM-006; DL25 |
| BR3 | Agent acceptance is accepted recommendations over all recommendations, and override is overridden over all, per agent and version | NFR-066; DF-DEC-007, DF-DEC-013 |
| BR4 | A measure is shown with its business date and freshness stamp; stale data shows its own date | MSG-P1-001 rule; FEAT-RPT-08 |
| BR5 | Each value is shown beside the frozen baseline of 2026-11-27, read on the reporting contract and never copied or updated here | REQ-WKM-009; baseline of 2026-11-27 |
| BR6 | A rate with no runs in the denominator is not computed, and the screen shows "No runs" | NFR-066 |
| BR7 | Every query applies the role's scope and the Reporting right | CTL-09 |
| BR8 | A day is answered only when every measure of the definition version in force has a value with a business date; a missing or failed source holds the day and answers 503 rather than a partial set | Legacy section 5; AC1, X7 |
| BR9 | The deviation column names the codes X1 to X7 open on the counted cases at the cut-off, read from `deviation` in `rwb_deviation`; a code is never copied into a measure row or taken from a case column | REQ-DVH-006; TSD S8 T3.1 and T3.2; DP-01 |
| BR10 | No data lake: no INT-19 extract is written and no file is delivered; the answer serves SCR-37 and the Power BI read model is built by rwb-reporting from events | DP-17; GAP-3088 |
| BR11 | One provenance entry per refresh run and per measure read, holding the definition version, the business date, the two counts and the verdict, and no measure value and no personal data | DP-03; legacy section 11 |

### 9. State transitions

The story changes no case status and no deviation state (legacy section 9). It sets the publish status of a business date, which is derived from the reconciliation of that date, and it records the run of the refresh.

| From | Event | To | Effect |
|---|---|---|---|
| No status for the date | The refresh runs and the counts are equal | Published for the business date | The answer is returned for that date and the provenance entry names published |
| No status for the date | The refresh runs and the counts differ by any amount | Held for the business date | No answer for that date, the previous day stays the latest, MSG-P9-002 and the alert |
| Published for the business date | The refresh is rerun for the same date with the same inputs | Published for the business date | The same values, a second provenance entry, the baseline rows unchanged |
| Held for the business date | A later run whose counts match | Published for the business date | The first run whose counts match publishes the day (legacy section 12) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, Tribe lead and squad members | Reads SCR-37 and the measures (Reporting R); approves the steering definitions |
| RW-PRODHEAD, product head | Reads SCR-37 (Reporting R) |
| RW-TEAMMGR, team manager | Reads SCR-37 for the teams in scope (Reporting R) |
| RW-BIANAL, Reporting and BI analyst | Consumes the measure answer and the freshness stamp; receives the hold alert (Reporting R) |
| RW-DATASTEW, data steward | Receives the hold alert; reads the reconciliation from the provenance record (Reporting R) |
| RW-FINANCE, Finance and CFO delegate | Reads SCR-37 (Reporting R) |
| RW-REFADM, reference data administrator | Loads the steering definitions through the reference-data contract of rwb-case (Reference data C; DP-07) |
| PT-LAWFIRM | No Reporting right; refused with MSG-P4-002 |
| rwb-reporting (P9) | Owns the measure definitions, the canonical measure build, the frozen baseline and the publication rules this story consumes |

### 11. Data

| BR Field ID | Field or entity | Owner | Use in this story |
|---|---|---|---|
| DF-RPT-032, 034, 035, 037 | `measure_definition`: measure_code, formula, data_product, definition_version | P9 rwb-reporting | **Read** on RWB-P9-E2009-CON: the seven measures in force and their version |
| DF-RPT-042 to DF-RPT-049, 052 | `measure_snapshot`: measure_code, definition_version, business_date, product_group, dimension_code, dimension_value, value, case_count, published_at | P9 rwb-reporting | **Read** on the contract for the published days and the frozen baseline rows of 2026-11-27; never written here |
| DF-RPT-054 to DF-RPT-058 | `measure_publish`: business_date, status, case_list_count, dashboard_count, held_reason | P9 rwb-reporting | **Read** on the contract for the publication rules; the verdict of this serving is derived, not written to this table |
| DF-CAS-001, 003, 005, 006, 008, 010, 013 | `recovery_case`: id, product_group, status, stage_code, route_code, queue_id, entry_date | P3 rwb-case | The case facts and the case-list count; consumed, never written (DP-11) |
| DF-WRK-002 | `queue`: queue_code | P3 rwb-case | The queue code of the queue and age measure; consumed |
| DF-TRT-004, 013 | `treatment`: treatment_type, outcome | P3 rwb-case | The treatment facts behind "TREATMENTS"; consumed |
| DF-LEG-018, 019, 022 | `notice`: notice_type, sent_date, delivery_status | P6 rwb-comms | The notice facts behind "LETTERS_SENT", with their product and freshness answer; consumed |
| DF-DEC-003, 007, 012, 013, 016 | `decision_log_entry`: decision_code, agent_version, final_call, override_reason, decided_at | P7 rwb-decision | The decision facts behind "DECISIONS_LOGGED", "AGENT_ACCEPTANCE" and "AGENT_OVERRIDE"; consumed through the decision-record surface (DP-03) |
| DF-CAS-036 to DF-CAS-045 | `deviation`: id, case_id, deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at, outcome | S8, `rwb_deviation` | **Read**, one row per code open at the cut-off, for the deviation column (BR9) |
| None: library table | `decision_record` | Platform library in `rwb_deviation` | **Write**, one provenance entry per run and per read, hash-linked; no measure value and no personal data (DP-03) |

The field IDs are those of the Logical Data Model and Data Dictionary v8; the `measure_*` and `decision_log_entry` rows are other owners' and are consumed on their contracts, never read as tables (DP-01). The product groups, routes and measure codes the filters offer are reference data of rwb-case read at their version (DP-07; ASM-5278). Age bands and the tolerance of zero are data, not constants (legacy sections 2 and 13).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). The legacy path `GET monolith-base/reports/measures` is kept with the base moved; the operation is a read and writes only the provenance entry (DP-03).

| Method | Path | Shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/reports/measures` | `Measure[]`: measure, product, route, period, value, dimension (code and value, for example `agent:case-intake:1.2.0` or `deviation:X3`), baselineValue, definitionVersion and the deviation codes open on the counted cases; query measure, product, route, from, to; header `X-Data-As-Of` carries the business date of the latest published day | Reporting R, scope applied | Not applicable; a read, safe to repeat |

Errors: 401 with MSG-P4-001, 403 with MSG-P4-002, 422 with MSG-GEN-003 when from is after to, 503 with MSG-GEN-006 when the reporting contract or the service's schema does not answer. The `dimension` and `baselineValue` fields are the two additions the legacy story records as missing from the Measure schema in `api.yaml` (ASM-5277).

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The measure definition and published measure read, with the baseline rows of 2026-11-27; operation name Not specified in the source documents (GAP-3087; ASM-5274) | P9 rwb-reporting, on RWB-P9-E2009-CON | The seven measures in force, the definition version, the published values of a day and the frozen baseline |
| The case fact and case-list count read; operation name Not specified in the source documents (GAP-3087; ASM-5274) | P3 rwb-case | The case facts behind "CASES_BY_STAGE" and "CASES_BY_QUEUE_AGE", and the count at the cut-off for BR2 |
| The treatment fact read; operation name Not specified in the source documents (GAP-3087; ASM-5274) | P3 rwb-case | The treatment facts behind "TREATMENTS" |
| The decision fact read on the decision-record surface; operation name Not specified in the source documents (GAP-3087; ASM-5274) | P7 rwb-decision | The entries behind "DECISIONS_LOGGED" and the two agent rates, with their agent version and override reason |
| The notice fact read; operation name Not specified in the source documents (GAP-3087; ASM-5274) | P6 rwb-comms | The notice facts behind "LETTERS_SENT", with the product of the answer and its freshness |
| The agent run fact read; operation name Not specified in the source documents (GAP-3087; ASM-5274) | P10 rwb-agent | The recommendations, acceptances and overrides per agent and version |
| The notification send; operation name Not specified in the source documents (GAP-3087; ASM-5279) | P6 rwb-comms | The hold alert of MSG-P9-002 to the Reporting and BI analyst and the data steward |

Every call is one hop with a 2 s budget and a breaker, and none retries inside a measure. The reporting contract is the one C row of this slice; the other six reads are consumed contracts with fakes and no C row (GAP-3087; ASM-5274).

#### 12.3 Events published

None. A refresh and a read publish no business event: the provenance entry is written locally through the library of DP-03 and relayed on the shared `rwb.decision-record.v1`, and this service's own topic `rwb.deviation.events.v1` carries the two deviation events of its write stories (DP-14 applied as naming only; ASM-5273).

#### 12.4 Events consumed

None. Every measure is computed from the owners' read answers at refresh time and answered with the business date of each answer, so a stale source is shown with its own date and MSG-P1-001 rather than kept fresh by a subscription (BR4).

#### 12.5 Workflows and activities

| Item | Queue | Responsibility |
|---|---|---|
| `SteeringMeasureRefreshWorkflow` | `rwb-deviation` | One run per business date: read the definitions, read the facts, compute the measures and the rates, reconcile the counts, read the deviation column, record the provenance |
| `ReadMeasureDefinitions` activity | `rwb-deviation` | The definitions in force and the baseline rows on RWB-P9-E2009-CON |
| `ReadFacts` activity | `rwb-deviation` | The six fact reads on their owners' contracts, each with its business date and freshness answer |
| `ComputeMeasures` activity | `rwb-deviation` | One calculator per measure code, the dimension and the two agent rates |
| `ReconcileCounts` activity | `rwb-deviation` | BR2 at tolerance zero; returns published or held with the two counts |
| `RecordProvenance` activity | `rwb-deviation` | One decision-record entry per run (DP-03) |

The workflow has no timer and no signal; it ends when the day is published or held, and its history stays far below the Continue-As-New threshold because each run is one business date.

#### 12.6 Schedules

| Schedule | Queue | When | Behaviour |
|---|---|---|---|
| `steering-measures` | `rwb-deviation` | Daily at 01:30 Asia/Bangkok, business date = the day it closes | Replaces JOB-15 in this service (DP-10); catches up one missed night, refuses a duplicate run for a date already published unless it is rerun with that business date as its input, and takes the business date as an input for a rerun (legacy AC9) |

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | Read only: the codes X1 to X7 open at the cut-off, with raised-at, paused state and handler, for the deviation column |
| `decision_record` | Platform library in `rwb_deviation` | Written: one provenance entry per run and per read, holding the definition version, the business date, the two counts and the verdict (DP-03) |

`measure_definition`, `measure_snapshot`, `measure_publish`, `recovery_case`, `queue`, `treatment`, `notice`, `decision_log_entry` and every `v_ace_*` view are other owners' and are named only; this story adds no table and no column, and no foreign key leaves `rwb_deviation` (DP-01, DP-15).

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| Reporting measure fake (`RWB-P9-E2009-CON`) | Definition version MD-2026.12 with the seven measures; the published day of 2026-12-14; the frozen baseline rows of 2026-11-27; a held day; an unavailable answer | AC1, AC2, AC4, AC9 |
| rwb-case fact and count fake | 240 open cases at the cut-off, 239 case facts, 140 open Mortgage cases, the stage and queue of RW-2026-000502 | AC1, AC2, AC4, AC8 |
| rwb-case treatment fake | 38 treatments of 2026-12-15 | AC1 |
| rwb-decision decision-record fake | 1,412 entries of 2026-12-15; agent versions and override reasons | AC1, AC2, AC3 |
| rwb-comms notice fake | 95 notices sent of 2026-12-15; the notice product dated 2026-12-14 | AC1, AC5 |
| rwb-agent run fake | case-intake 1.2.0 with 200 recommendations, 170 accepted, 30 overridden; deviation-screen 0.9.0 with no runs | AC1, AC3, AC7 |
| rwb-comms notification fake | The hold alert accepted for the two recipients | AC4 |
| gateway-bff composite route fake | The assembled SCR-37 for a synthetic day | AC1 to AC9 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 7 consumed | `GET /reports/measures` on `/api/recovery/deviation/v1`; the reporting, case (two), decision, notice, agent and notification reads; one hop, 2 s each |
| Kafka | None | No business event published or consumed; the provenance entry rides the library's `rwb.decision-record.v1` |
| Temporal | 1 workflow, 5 activities, 1 Schedule | `SteeringMeasureRefreshWorkflow` on queue `rwb-deviation`; Schedule `steering-measures` at 01:30 |
| File | None | No INT-19 extract and no file; the data lake is removed (DP-17, BR10) |

### 13. Solution plan

**Deliverables.** The measure answer on the target base, the seven calculators, `AgentRates`, `CountReconciliation`, `DeviationColumnReader`, `ProvenanceWriter`, `SteeringMeasureRefreshWorkflow` with its five activities and the `steering-measures` Schedule, and the SCR-37 components with their held, stale and "No runs" states.

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>`, "recovery schema" | Own schema `rwb_deviation`; `measure_snapshot` and `measure_publish` are read on the reporting contract, never as tables | None |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and the shared topic `rwb.decision-record.v1`; the decision facts are consumed on the decision-record surface | H `RWB-PLT-E1027-CON` (not in the empty build row, ASM-5272) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case for the product, route and measure lists of the filters | H `RWB-PLT-E1043-CON`; C `RWB-P3-E1043-CON` |
| DP-10 | Quartz, JOB-nn | Temporal Schedule `steering-measures` and `SteeringMeasureRefreshWorkflow` through the workflow kit | H `RWB-PLT-E1071-CON` |
| DP-11 | In-process call, published interface | One REST read per owner fact with a fake, one hop, 2 s, no retry inside a measure | C from the legacy dependency (`RWB-P9-E2009-CON`) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-15 | V0001 baseline, migration | Per-service Flyway in `rwb_deviation`; this story adds no table and no column | H `RWB-PLT-E1044-CON` |
| DP-17 | Data lake, INT-19, INT-20 | Removed: no lake and no extract; the freshness stamp serves SCR-37 and the Power BI read model belongs to rwb-reporting | None (the lake need is a gap, GAP-3088) |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-37 | H `RWB-PLT-N001-CON` |

**Build steps.** (1) Read the definitions and the baseline on RWB-P9-E2009-CON and the six fact families on their owners' contracts, with their business dates and freshness answers. (2) Build the seven calculators and the two agent rates against the fakes with the synthetic day; prove AC1, AC2, AC3 and AC7. (3) Build `CountReconciliation` and the held answer; prove AC4 and AC9. (4) Build the endpoint with the filters, the date check, the scope and `X-Data-As-Of`; prove AC6 and AC8. (5) Add the deviation column from `deviation`; prove AC2's last step and the boundary test. (6) Add the schedule and the workflow, the provenance writer and the alert; prove AC5 and AC4's alert. (7) Build the SCR-37 components with the held, stale, "No runs" and error states.

**Done when.** AC1 to AC9 pass at component and contract level on the fakes, the boundary test shows no statement on `rwb_reporting`, `rwb_case` or a `v_ace_*` view, a held day answers no value with MSG-P9-002, and one SIT day answers the same values from the refresh and from a rerun.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P9-002 | The dashboard count differs from the case list (X1) | The case count on the dashboard ({count}) does not match the case list ({listCount}) for {date}. The publish is held. |
| MSG-P1-001 | A source is stale (X2) | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-003 | Dates in the wrong order (X3) | {field} cannot be before {other}. |
| MSG-P4-002 | The role lacks Reporting R (X6) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | The reporting contract or the schema does not answer (X7) | {service} is not available now. Try again in a few minutes. |

The wording is the legacy wording, copied unchanged; no message is reworded and none is added. The legacy MSG-P4-001 and MSG-GEN-003 rows stay with the platform error envelope.

### 15. Screens and states

SCR-37 Steering dashboard (served by rwb-deviation for this slice, through the gateway-bff composite route, DP-19):

| State | What the user sees and does |
|---|---|
| Loading | Skeleton rows while `GET /reports/measures` returns |
| Filtered | Values for the chosen product, route and dates, each beside the baseline of 2026-11-27, with the business date; the deviation codes of the counted cases; agent rates by agent and version |
| Held | 2026-12-14 as the latest day with MSG-P9-002 naming the two counts and the held date |
| Stale input | MSG-P1-001 above the affected measure with the product and its date |
| No runs | "No runs" for an agent with no recommendations on the day |
| Error | MSG-GEN-006 for the panel; nothing partial shows |

The screen shows no Workbench load, job or file status, and no figure that is not in the answer (BR4, BR10).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-009-01 | AC1, BR1, BR4 | Component | Synthetic day 2026-12-15; definition version MD-2026.12; the six fact fakes fresh |
| TC-E2-009-02 | AC2, BR1, BR2, BR9 | Component | 240 open cases; 1,412 decision log entries; an open X3 on RW-2026-000502 |
| TC-E2-009-03 | AC3, BR3 | Component | case-intake 1.2.0: 200 recommendations, 170 accepted, 30 overridden |
| TC-E2-009-04 | AC4, BR2 | Component | Case list 240, case facts 239 |
| TC-E2-009-05 | AC5, BR4 | Component | Notice product dated 2026-12-14 |
| TC-E2-009-06 | AC6 | Contract | from 2026-12-15, to 2026-12-01 |
| TC-E2-009-07 | AC7, BR6 | Component | deviation-screen 0.9.0 with no runs |
| TC-E2-009-08 | AC8, BR7 | Contract | Filter MORTGAGE, 140 open Mortgage cases |
| TC-E2-009-09 | AC9, BR5, BR11 | Component | Rerun for 2026-12-15; the baseline rows of 2026-11-27 |
| TC-E2-009-10 | Access (X6) | Contract | PT-LAWFIRM calls `GET /reports/measures` and is refused with MSG-P4-002 |

The ten ids are the legacy cases of RWB-E2-009, kept in their legacy order; the two that read the answer through the gateway route are carried at Contract level and their end-to-end half belongs to the wave 2 harness. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same id.

### 17. Guardrails

- No business value in code: the seven measures, their formulas, the tolerance, the age bands, the schedule time and the labels are data rows read at their version (DP-07).
- No personal data in events, workflow inputs, the provenance entry, logs or prompts; measures carry counts, rates, amounts and codes only, and agent outputs are counted, never copied.
- ACE data only through the owner's contract: no `v_ace_*` view, no ACE table and no other service's schema is read, and a statement that tries is refused by the grant and fails the boundary test (DP-01, DP-02).
- No measure table, no report copy and no extract file in this service: the answer is computed from the owners' answers and the one table it reads is its own `deviation` (DP-01, DP-17).
- The reconciliation runs before any value is answered, and a held day answers nothing (BR2, BR8).
- One base, one topic, one queue and one login per service; this story adds no second base and no new topic (DP-13, DP-14).

### 18. Traceability

| Legacy | Story | Test |
|---|---|---|
| RWB-E2-009 AC1 to AC9 | Not copied as owned criteria: the plan assigns this slice no legacy AC (GAP-3089); AC1 to AC9 restate each scenario as new (D-RCV-60) with the legacy values kept word for word | TC-E2-009-01 to TC-E2-009-09 |
| RWB-E2-009 section 12, GET /reports/measures and JOB-15 | Section 12.1 with the base moved, and the `steering-measures` Schedule in 12.6 | TC-E2-009-01, TC-E2-009-06, TC-E2-009-09 |
| RWB-E2-009 section 12, INT-19 extract | Removed with the data lake (DP-17; GAP-3088) | None |
| RWB-E2-009 section 16, Access test | X6 | TC-E2-009-10 |
| RWB-E2-009 BR1 to BR7 | BR1 to BR7, restated with the owners' contracts as the source | Section 16 |

| Source | What it supplies |
|---|---|
| REQ-WKM-009, REQ-WKM-006 | The steering measures and the reconciliation to the case list |
| Legacy RWB-E2-009 sections 1 to 19 | The story, the flow, the nine scenarios, the seven rules, the messages, the fields and the ten test cases, all kept in substance |
| FSD S8 Requirements served REQ-DVH-006 and TSD S8 T3.1, T3.2, T5.2 | The deviation code list, the `deviation` columns and the published-interface rule behind the deviation column |
| Context pack S8 rwb-deviation and the connection matrix | Schema, base, topic, queue, the one owned table, and the P1, P3 and P10 links |
| Split plan, slice RWB-S8-E2009-APP | H, C, I, X, the lane, the wave and the release (GAP-3087, GAP-3090; ASM-5279) |

### 19. Out of scope

- The published measure set of the reporting owner: the `measure_definition`, `measure_snapshot` and `measure_publish` tables, the canonical JOB-15 build, the frozen baseline and the Power BI read model (RWB-P9-E2009-CON; rwb-reporting, P9).
- Queue measures and service level breaches for team managers (RWB-E1-030, RWB-E2-011) and the agent monitoring dashboard with latency and cost (RWB-E2-031).
- Benefit realisation against the baseline (FEAT-RPT-06, Epic 6) and the regulatory returns (FEAT-RPT-07, Epic 8).
- Raising, routing, clearing and escalating a deviation, its contact stop and its timers (`DeviationWorkflow`, the write stories of this service, RWB-E1-062 and RWB-S8-E7001-APP to RWB-S8-E7007-APP).
- The schema, the migration, the login and the deployment of `rwb_deviation` (the DB, INF and OPS stories of this key), and any change to a legacy file or to built Epic 1 code.
