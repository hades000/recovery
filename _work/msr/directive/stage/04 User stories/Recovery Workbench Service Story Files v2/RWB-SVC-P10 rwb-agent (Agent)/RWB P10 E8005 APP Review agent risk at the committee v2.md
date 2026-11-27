# RWB-P10-E8005-APP Review agent risk at the committee

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E8005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P10-L |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P10-E8005-APP-16); the squad sizes it at refinement |
| Depends on (build) | RWB-P10-E8005-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | rwb-agent.yaml (Recovery Workbench API Specification v5), base /api/recovery/agent/v1; version number Not specified in the source documents (DOR-RWB-P10-E8005-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-005 for rwb-agent. The committee pack is built from the rows this service already holds — `agent_run` for performance and fallbacks, `agent_feedback` for acceptance and overrides, `agent_alert` for incidents and `agent_evaluation_run` for failure counts (DP-01) — the score facts are read through rwb-source-data's contract and never from a view (DP-05), the committee outcome is written through the local decision-record library and `rwb.decision-record.v1` (DP-03), the two reads move to `/api/recovery/agent/v1` (DP-13) and are composed for SCR-46 by the gateway-bff route (DP-19). The Power BI integration point of the legacy module is replaced by the read and the export, because Arch v5 removes the lake and the Power BI connection. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E8005-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 10 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer**, I want **to put agent performance, overrides and incidents in front of the strategy and model committee**, so that **agents prepare the work and people decide where they must**.

### 2. Business rationale

The legacy story RWB-E8-005 gave the risk and model risk officer one outcome and no mechanism: agent performance, overrides and incidents reach the strategy and model committee, and the result is written to the decision log with the rule version (FEAT-AGT-16; FSD P10 v3 A2.16). It depends on FEAT-AGT-06, the agent monitor, because the facts a committee reviews are the ones the monitor gathers. The BOT AI Risk Management Guidelines of 12 Sep 2025 make board accountability, lifecycle risk management and accuracy conditions of running the agents at all, and the Workbench answers them by keeping the AI inside rwb-agent where it can be switched off (Arch v5 slide 35, slide 41).

In the target the evidence and the review are in the same service. rwb-agent owns the agent policies, the prompts, the runs, the guardrails and the evaluations (Arch v5 slide 41), so the pack reads its own rows and asks nobody for a table: the performance figures are `agent_run` — the statuses of LOV-AGENT-RUN, the `fallback` flag, the confidences, the latencies and the cost — the acceptance and the overrides are `agent_feedback` over LOV-FEEDBACK (ACCEPTED, CORRECTED, REJECTED) joined to the run it answers, the incidents are `agent_alert` over the two values of LOV-AGENT-ALERT (COST_CAP and DRIFT), and the failure counts are `agent_evaluation_run.failure_counts` of the evaluation run the agent version was scored in. That is the shape FSD A2.6 gives the monitor — acceptance, override, latency and cost per agent — turned into the one document a committee reads, and it is the same evidence the monitor screen and the drift and champion stories work from (DP-01; FSD A2.6.1).

One figure is not this service's: the score facts of `v_ace_score` (DF-ACE-270 to DF-ACE-279) come from the ACE views, which only rwb-source-data reads, so the pack's score column is read through rwb-source-data's contract with one hop and a 2 s timeout, and a failed or stale answer is shown as not available rather than defaulted (DP-05; ADR-010; Arch v5 slide 45).

The review itself is a decision, and every decision is recorded: the committee outcome is written through the local decision-record library, hash-linked, in one transaction with its outbox row, and relayed as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` to the central ledger in rwb-decision (DP-03; ADR-022; Temporal and Drools design slide 11). A failed write changes nothing and the officer sees MSG-P7-003, which is the legacy criterion AC2 and the FSD exception AC-EXC-P10-016-02. The pack and its export are read on `/api/recovery/agent/v1` (DP-13) through the gateway-bff composite route that serves SCR-46 Agent monitor, so the browser calls no owner service directly (DP-19).

The realignment work is what leaves the slice. The legacy read of `decision_log_entry` becomes the P7 library; the direct read of the score view becomes the rwb-source-data contract; `rule_row` is not read at all, because the version on a committee record is the policy version in force with the agent, prompt and model versions of the runs reviewed, and no Drools package is evaluated by a committee review (ASM-1037). The Power BI integration point of FSD A2.16 is replaced by the two reads and the CSV export, because Arch v5 removes the data lake and the Power BI connection (DP-17; Arch v5 slides 7 and 8).

This story owns both legacy criteria of RWB-E8-005 — AC1 and AC2 — and copies them verbatim in section 7. AC3 to AC11 are new and test the microservice deliverable of the title only. The legacy story carries no requirement ID; section 18 records that and traces the feature instead.

### 3. Preconditions

- RWB-P10-E8005-CON is published: the shape of the two pack reads on `/api/recovery/agent/v1`, the CSV and JSON export rule, the committee-outcome members of the decision record, the errors and rights of the two operations and the three fakes. This story builds against that document and its fakes, and the export media types it leaves open are the agreed reading recorded as an assumption (GAP-0642; ASM-1039).
- RWB-PLT-E1027-CON is published: the local decision-record library, the record shape and the shared topic `rwb.decision-record.v1` with its CloudEvents envelope. This story writes its record through the library and never writes the shared topic directly (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route contract for SCR-46 and its stub, so the exposure of the pack is built and tested before the screen is wired (DP-19).
- The `rwb_agent` schema exists with the agent runtime baseline migration — `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation`, `agent_feedback` and `agent_alert` (TSD P10 v2 T3.1; RWB-P10-E1058-APP owns the schema and the baseline). This story issues no migration of its own (ASM-1041).
- Runs, feedback and alerts exist for the window the pack covers, and at least one evaluation run of the reviewed agent version is in status DONE, because the pack is built from rows and not from a calculation of this story (FEAT-AGT-01, FEAT-AGT-05, FEAT-AGT-06).
- The list values the pack groups by are those of TSD P10 v2 T3.2: LOV-AGENT (INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER), LOV-AGENT-RUN (ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, TOOL_UNAVAILABLE, MODEL_ERROR, DISABLED), LOV-AGENT-ALERT (COST_CAP, DRIFT), LOV-FEEDBACK (ACCEPTED, CORRECTED, REJECTED) and LOV-PRODUCT for the segment. The lists are reference data owned by rwb-case under the §R3 default ruling, and the pack holds no copy of a list in code.
- The ACE score facts of the model code and model version in force are reachable through rwb-source-data's contract: `score_key`, `account_key`, `model_code`, `model_version`, `score_value`, `estimate_value` and the four remaining fields of DF-ACE-270 to DF-ACE-279. The exact operation and its product path are Not specified in the source documents (GAP-0642; ASM-1035).
- The pack window is the week to the business date, and the window, the row set and the four headings are the agreed reading of FEAT-AGT-16 recorded as an assumption (GAP-0642; ASM-1034).
- The login is the rwb-agent login (DP-02): its name is Not specified in the source documents (GAP-0642; ASM-1042).

### 4. Flow

1. The risk and model risk officer opens SCR-46 Agent monitor in state live for the business date and asks for the committee pack. The screen is served by the gateway-bff composite route, which calls the agent reads on `/api/recovery/agent/v1` and merges the answers; the browser calls no owner service directly (DP-19).
2. The route calls `GET /api/recovery/agent/v1/admin/agent-runs` (TSD P10 v2 API-P10-001) with the agent, the from and the to parameters, and `GET /api/recovery/agent/v1/admin/agent-metrics` (API-P10-009) with the agent, the segment, the version, the from and the to parameters (DP-13).
3. For each agent and segment in the window, the pack takes its performance from `agent_run`: the run count by each status of LOV-AGENT-RUN, the count and the share of the runs whose `fallback` is true, and the `confidence`, `latency_ms` and `cost_thb` values the rows carry. A status outside LOV-AGENT-RUN is not mapped to a bucket: it is listed as a data error with the value it carried and it is excluded from the counts.
4. The acceptance and the overrides come from `agent_feedback` over the run it answers: ACCEPTED is the acceptance count, and CORRECTED and REJECTED are the overrides, with the `item_key` and the `reason` of each override carried to the pack as a fact and never as free text into a log.
5. The incidents come from `agent_alert` for the window: one line per alert with `alert_type` over LOV-AGENT-ALERT, the `segment`, the `business_date`, the `measured_value`, the `threshold_value` and `sent_to_role`. A `sent_at` that is empty is shown as not yet notified, because an alert is not lost when the notification path is down (R-UNI-33, R-UNI-35; FSD A2.6 AC-EXC-P10-006-03).
6. The failure counts come from `agent_evaluation_run.failure_counts` of the latest run in status DONE for the agent version, and the policy version, the model code and the model version come from the `agent_policy` version in force on the business date.
7. The score column is read from the rwb-source-data contract for the model code and model version in force. A contract error, or facts older than the business date, mark the score column as not available for that agent and segment with the reason of the run; no value is defaulted and the rest of the pack is still served (DP-05).
8. The pack is returned as AgentMetricsPack and AgentRunsPack with the members fixed by RWB-P10-E8005-CON, and the officer exports it as JSON or as text/csv. The export carries the same rows and the same member order as the read, and no member that the read does not hold (ASM-1039).
9. The committee outcome is submitted from the screen. The service writes the local decision record through the P7 library with the pack reference, the business date, the policy version in force, the agent, prompt and model versions reviewed, the outcome code, the owner role and the review date, together with its outbox row, in one `rwb_agent` transaction (DP-03; R-UNI-39).
10. The DecisionRecorded row is relayed from the outbox to `rwb.decision-record.v1`, and rwb-decision seals it into the central ledger. A failed record write rolls the transaction back, so nothing is stored and the officer sees MSG-P7-003 (AC2; FSD A2.16.4.3 AC-EXC-P10-016-02).
11. A second submission of the same pack for the same business date writes no second record and sends no second notification; the repeat is counted once in the pack summary (ASM-1040; R-UNI-40).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The rwb-source-data contract returns an error, or the score facts are older than the business date | The score column is marked as not available for that agent and segment with the reason of the run; no value is defaulted; the rest of the pack is served | None | AC4 |
| X2 | The local decision record cannot be written | The transaction rolls back: no record, no outbox row and no notification; nothing changes and the officer sees MSG-P7-003 | MSG-P7-003 | AC2 |
| X3 | A caller without the right of the read opens the pack or exports it | Refused; nothing is returned, nothing is exported and nothing is written | MSG-P4-002 | AC9 |
| X4 | A run carries a status outside LOV-AGENT-RUN, or an alert a type outside LOV-AGENT-ALERT | The value is listed as a data error and excluded from the counts; no bucket and no incident type is invented and the pack continues | None | AC3 |
| X5 | An agent in force has no run in the window | The agent shows zero runs and no incident, and the pack says so; no row is fabricated (FSD A2.6 AC-EXC-P10-006-02) | None | AC10 |
| X6 | The pack is submitted twice for the same business date | No second record and no second notification; the repeat is counted once | None | AC5 |
| X7 | An export is asked for with a media type the contract does not declare | Refused before any row is written; the declared media types are named in the answer | None | AC8 |
| X8 | A pack row would carry an account key, a subject id or a reason text with personal data | The member is absent from the pack and from the export by schema, and the value is never logged | None | AC7 |

No exception here moves a case: this story writes no case field, raises no task and holds no queue, and the case side of a committee outcome belongs to rwb-case.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against RWB-P10-E8005-CON, the two platform contracts and the three fakes; it waits for no in-lane story and reads rows the service already holds |
| Negotiable | The window, the row set, the export media types and the recorded version identifiers are agreed readings, recorded as assumptions, and the thresholds stay rows |
| Valuable | A committee sees one pack of agent performance, overrides and incidents that is built from the agent's own evidence and is recorded as a decision |
| Estimable | Two read operations, four fact readers, one score client, one exporter, one record writer, no new table |
| Small | Fits one sprint with its tests |
| Testable | Each of the eleven criteria of section 7 is one automated test against the three fakes and seeded `rwb_agent` rows; no criterion needs a live model |
| Traceable | Every criterion carries its origin tag, the two legacy criteria verbatim, and the feature FEAT-AGT-16 is traced in section 18 |

### 7. Acceptance criteria

```gherkin
Feature: Review agent risk at the committee

  Background:
    Given agent "SCREENING" is in force on 2026-12-15 with policy version "P1" and model version "MODEL-A-2026-10"
    Given its segment is product group "MORTGAGE" and region "BKK"
    Given the strategy and model committee reviews the pack for business date 2026-12-15

  Scenario: AC1 Review agent risk at the committee (legacy RWB-E8-005 AC1)
    Given the rwb-source-data contract mock returns the score facts of "MODEL-A-2026-10" and the outcomes of agent "SCREENING" are the rows of agent_run, agent_feedback and agent_alert in rwb_agent
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then puts agent performance, overrides and incidents in front of the strategy and model committee
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-005 AC2)
    Given the rwb-decision contract mock refuses the decision log write
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The pack is built from this service's own rows (new, D-RCV-60)
    Given the week to 2026-12-15 holds 50 agent_run rows of "SCREENING" on "SCREENING:MORTGAGE:BKK": 34 ANSWERED, 6 TIMED_OUT, 4 GUARDRAIL_FAILED, 3 BELOW_FLOOR, 2 TOOL_UNAVAILABLE and 1 MODEL_ERROR, of which 9 carry fallback true
    Given agent_feedback holds 40 rows over those runs: 30 ACCEPTED, 7 CORRECTED and 3 REJECTED
    Given agent_alert holds two rows for the window: one COST_CAP and one DRIFT, and one row of type DRIFT with an empty sent_at
    Given agent_evaluation_run holds one run in status DONE for the agent version with failure_counts of 2 TIMED_OUT and 1 MODEL_ERROR
    When the pack is read for 2026-12-15
    Then the performance section holds the run count by the statuses of LOV-AGENT-RUN, the count and the share of the runs whose fallback is true, and the confidence, latency and cost values of the rows
    Then the overrides section holds acceptance 30, corrections 7 and rejections 3 over LOV-FEEDBACK
    Then the incidents section holds the two alert types of LOV-AGENT-ALERT with their segment, business date, measured value, threshold value and role, and the DRIFT row is shown as not yet notified
    Then the failure counts are those of the latest DONE evaluation run
    Then every one of those values is read from agent_run, agent_feedback, agent_alert, agent_evaluation_run and agent_policy in rwb_agent, and no table of another schema is read

  Scenario: AC4 The score facts come through the rwb-source-data contract (new, D-RCV-60)
    Given the rwb-source-data contract mock returns 40 score facts of "MODEL-A-2026-10" for the business date
    When the pack is read for 2026-12-15
    Then the score column holds the facts of the contract for the agent and segment and names the model code and model version they belong to
    Given the same call is made when the contract returns an error, and again when it returns facts dated 2026-12-14
    Then the score column is marked as not available for "SCREENING" on "SCREENING:MORTGAGE:BKK" with the reason of the run
    Then no value is defaulted for it and the performance, override and incident sections are still served
    Then no v_ace_score view is read by this service and no score row is written into rwb_agent

  Scenario: AC5 The committee outcome is written through the library and the shared topic (new, D-RCV-60)
    Given the pack of AC3 has been read for business date 2026-12-15
    When the committee outcome is submitted
    Then one decision record is written before the outcome is shown as taken, and it names the pack reference, business date 2026-12-15, policy version "P1", the agent, prompt and model versions reviewed, the outcome code, the owner role and the review date
    Then the record and its outbox row commit in one rwb_agent transaction
    Then rwb.decision.DecisionRecorded.v1 is written to the outbox on rwb.decision-record.v1 in the CloudEvents envelope with the record reference as its key
    Then the outcome carries no personal data, holds identifiers and facts only, and no rule row is read and no package version is named
    When the same pack is submitted again for 2026-12-15
    Then no second record and no second notification exist, and the repeat is counted once

  Scenario: AC6 The pack is read on the agent base through the gateway-bff route (new, D-RCV-60)
    Given the pack of AC3 is available for 2026-12-15
    When the risk and model risk officer opens SCR-46 Agent monitor in state live
    Then the pack is served by the gateway-bff composite route, which calls GET /api/recovery/agent/v1/admin/agent-runs and GET /api/recovery/agent/v1/admin/agent-metrics with one hop each
    Then the merged answer carries the performance, override and incident sections of the pack
    And the browser calls no owner service directly
    Then each of the two calls carries a 2 s budget and its own breaker, and a failed call leaves the other section on the screen with its own state

  Scenario: AC7 No personal data reaches the pack, the export or a log (new, D-RCV-60)
    Given the runs and the feedback of AC3 include an account key, a subject id and a corrected-item reason that names a person
    When the pack is read and exported
    Then no pack member and no export column carries an account key, a customer name, a personal identifier or free text of the reason
    Then the log of the read holds the agent codes, the segments, the counts, the rates and the business date only
    Then the decision record event carries identifiers and facts only, and the workflow and activity payloads pass the payload codec when any is used

  Scenario: AC8 The pack exports as CSV or JSON with the same rows (new, D-RCV-60)
    Given the pack of AC3 has been read for 2026-12-15
    When the officer exports it as JSON and again as text/csv
    Then both files carry the same rows in the same member order as the read, and the CSV header is formed from the member names
    Then an export carries no member the read does not hold, and the incidents keep their alert type, segment, business date, measured and threshold values
    When an export is asked for with a media type the contract does not declare
    Then it is refused before any row is written and the declared media types are named

  Scenario: AC9 A role without the right is refused with MSG-P4-002 (new, D-RCV-60)
    Given user "U-5001" holds RW-REFADM, which carries neither Platform administration R nor Rules and parameters R
    When "U-5001" calls the runs read, the metrics read and the export route
    Then each call is refused with 403 and MSG-P4-002
    Then nothing is returned, nothing is exported and nothing is written
    Given a caller holds the right of the runs read only
    Then the metrics read is refused and the runs read is served

  Scenario: AC10 An agent with no runs shows zero and raises nothing (new, D-RCV-60)
    Given agent "EXTRACT" has a policy in force on 2026-12-15 and no agent_run row in the window
    When the pack is read for 2026-12-15
    Then "EXTRACT" is listed with zero runs, an empty override section and no incident
    Then no row is fabricated for it and no alert is raised by the read (FSD A2.6 AC-EXC-P10-006-02)
    Then an agent that holds no policy in force on the date is named as not in force and is not packed

  Scenario: AC11 The three monitor states change no row (new, D-RCV-60)
    Given SCR-46 Agent monitor holds the states Shadow, live and paused
    When the pack is read for 2026-12-15 in each of the three states
    Then the same agents, segments, counts and incidents are returned in all three
    Then the state changes no row and starts no run, and pausing the monitor stops no read of the pack

  Scenario: AC12 The business rules of section 8 hold for one committee pack (new, D-RCV-60)
    Given the rows of AC3, the score facts of AC4 and agent "EXTRACT" of AC10 are in place for business date 2026-12-15
    Given one run status outside LOV-AGENT-RUN, one alert type outside LOV-AGENT-ALERT, one alert with an empty sent_at and one failed or stale score facts answer are also stubbed
    When the pack is read and exported, and the committee outcome is submitted twice
    Then agent performance, overrides and incidents reach the committee as one pack and the outcome is recorded as a decision (BR1)
    Then the pack rows come only from agent_run, agent_feedback, agent_alert, agent_evaluation_run and agent_policy, and no table of another service is read (BR2)
    Then ACCEPTED is counted as acceptance, and CORRECTED and REJECTED are counted as overrides (BR3)
    Then the incidents are the COST_CAP and DRIFT alerts of the window, and an alert with an empty sent_at is shown as not yet notified and is not dropped (BR4)
    Then the score facts are read through the rwb-source-data contract, and a failed or stale answer is shown as not available with no value defaulted (BR5)
    Then the decision record and its outbox row commit in one transaction before the outcome is shown as taken (BR6)
    Then the record names the policy version in force with the agent, prompt and model versions of the runs reviewed, no Drools package is evaluated and no rule_row is read (BR7)
    Then the repeat submission writes no second record, sends no second notification and is counted once (BR8)
    Then the thresholds, the caps and the review date are those of the agent_policy version in force, and the list values are reference data of rwb-case (BR9)
    Then a run status outside LOV-AGENT-RUN or an alert type outside LOV-AGENT-ALERT is a data error and is mapped to no bucket (BR10)
    Then "EXTRACT" is listed with zero runs and no incident, and no row is fabricated for it (BR11)
    Then the pack, its export and the two reads carry no personal data (BR12)
    Then the two reads are served only on /api/recovery/agent/v1 through the gateway-bff composite route, and the browser calls no owner service directly (BR13)

  Scenario: AC13 The error answers 401 and 404 of the provided operations return no pack section (new, D-RCV-60)
    Given the runs read and the metrics read of AC6 are offered through the gateway-bff composite route; both operations are not yet published in rwb-agent.yaml (CG-ALL-2894; CG-ALL-2895)
    When GET /api/recovery/agent/v1/admin/agent-runs and GET /api/recovery/agent/v1/admin/agent-metrics are called without a valid token, and a provided operation answers 404
    Then each call without a valid token is answered 401 and the 404 answer is passed on as 404
    Then the condition under which a provided operation answers 404 is Not specified in the source documents (NEWAC-RWB-P10-E8005-APP-AC13)
    Then no 401 or 404 answer returns a pack section or writes a row

  Scenario: AC14 A retried or timed-out activity writes no second record and defaults no value (new, D-RCV-60)
    Given an activity of the pack read or of the committee outcome is retried by the workflow
    Given a later attempt of the same activity times out
    When the pack is read or the committee outcome is submitted
    Then the retry writes no second decision record and no second outbox row, and the repeat is counted once as in AC5
    Then the timed-out attempt defaults no value, and the retry and timeout counts are Not specified in the source documents (NEWAC-RWB-P10-E8005-APP-AC14)
```

AC1 and AC2 are the legacy criteria of RWB-E8-005, copied verbatim with their values and their message IDs. **Target reading.** Each of the two legacy criteria gains exactly one `Given` as its first line, and no legacy line is changed, reordered or dropped: AC1 gains the `Given` that stubs the rwb-source-data contract and names the three tables of `rwb_agent` the outcomes come from, because the legacy line "the data and the rule version this feature needs are in place" cannot be executed without naming where the data now lives; AC2 gains the `Given` that stubs the rwb-decision contract whose write is forced to fail, because the legacy line "the decision log cannot be written" is now a failure of another service's contract and not of a local log. AC3 to AC11 are new for this service change and test only the pack, its score read, the committee record, the exposure of the pack on the two reads and the PII rule.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Agent performance, overrides and incidents reach the strategy and model committee as one pack, and the committee outcome is recorded as a decision | FEAT-AGT-16; FSD P10 v3 A2.16; legacy RWB-E8-005 |
| BR2 | The pack is built from the rows this service owns — `agent_run`, `agent_feedback`, `agent_alert`, `agent_evaluation_run` and `agent_policy` — and never from another service's table | DP-01; Arch v5 slide 41; ADR-010 |
| BR3 | Acceptance and overrides are counted over LOV-FEEDBACK: ACCEPTED is acceptance, CORRECTED and REJECTED are overrides | TSD P10 v2 T3.2 LOV-FEEDBACK; FSD P10 v3 A2.6.1 |
| BR4 | Incidents are the `agent_alert` rows of the window, over the two values of LOV-AGENT-ALERT, COST_CAP and DRIFT; an alert with an empty `sent_at` is shown as not yet notified and is never dropped | TSD P10 v2 T3.2 and T3.1 DF-AGT-103 to DF-AGT-111; FSD P10 v3 A2.6 AC-EXC-P10-006-03; R-UNI-33 |
| BR5 | The score facts of the ACE views are read through rwb-source-data's contract; a failed or stale answer is shown as not available and no value is defaulted | DP-05; ADR-010; Arch v5 slide 45 |
| BR6 | The committee outcome is written through the local decision-record library before it is shown as taken, and the record and its outbox row commit with it in one transaction | Principle 5; R-UNI-39; DP-03; ADR-022 |
| BR7 | The version on the committee record is the policy version in force with the agent, prompt and model versions of the runs reviewed; no Drools package is evaluated and no `rule_row` is read | ASM-1037; TSD P10 v2 T3.1 DF-AGT-003, DF-AGT-038 to DF-AGT-040 |
| BR8 | One record per pack and business date: a repeat submission writes no second record and sends no second notification, and the repeat is counted once | R-UNI-40; ASM-1040 |
| BR9 | No value a business person may change is written in code: the thresholds, the caps and the review date are rows of the `agent_policy` version in force, and the list values are reference data of rwb-case | BR-P10-016; Template and Rules §R3 |
| BR10 | The run outcomes are counted under the values of LOV-AGENT-RUN and the incidents under LOV-AGENT-ALERT; a value outside a list is a data error and is never mapped to a bucket | TSD P10 v2 T3.2; BR-P10-016 |
| BR11 | An agent in force with no run in the window is listed with zero runs and no incident; no row is fabricated for it | FSD P10 v3 A2.6 AC-EXC-P10-006-02 |
| BR12 | The pack, its export and the two reads carry no personal data: agent codes, segments, statuses, counts, rates, costs, dates and identifiers only | Template and Rules §R7.2 s17; Arch v5 slide 42 note; DP-03 |
| BR13 | The reads are served only on `/api/recovery/agent/v1` and reached through the gateway-bff composite route; the browser calls no owner service directly | DP-13; DP-19; Arch v5 slide 41 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| NOT_PACKED | PACK_READ | the officer reads the pack for a business date and the rows of the window are in `rwb_agent` | PACK_READ |
| PACK_READ | PACK_EXPORTED | the officer exports the pack as JSON or CSV | PACK_READ, exported |
| PACK_READ | OUTCOME_RECORDED | the decision record and its outbox row commit in one transaction | RECORDED |
| PACK_READ | RECORD_FAILED | the decision record cannot be written | NOT_RECORDED, with nothing changed and MSG-P7-003 |
| RECORDED | OUTCOME_RECORDED | the same pack is submitted again for the same business date | RECORDED, no second record |

These are the states of the committee pack and of its record, not a case state machine: `agent_run` and `agent_alert` hold no pack column or pack status (TSD P10 v2 T3.1), so PACK_READ and RECORDED are read from the read itself and from the decision record of the pack reference. **This story moves no case status**: `recovery_case.status` is neither read nor written, no task and no assignment row is written, and the case side of a committee outcome belongs to rwb-case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Risk and model risk officer (RW-RISK) | The primary reader of the pack on SCR-46 and the role the committee outcome is recorded for |
| Center of excellence analyst (RW-COE) | Owns the policy versions, their thresholds, their caps and their review date; reads the pack, as the legacy permission list allows |
| Data steward and data product owner (RW-DATASTEW) | Reads the pack and the score column it draws through rwb-source-data |
| Internal audit (RW-AUDIT), Compliance and PDPA officer (RW-COMPLY) | Read the pack and its record, as the legacy permission list allows |
| Platform administrator (RW-PLATADM) | Reads the pack, the runs and the alerts, and may export it; holds Platform administration CRUD |
| Security administrator (RW-SECADM) | Reads the pack and its record, as the legacy permission list allows |
| rwb-agent service identity (the rwb-agent login, DP-02) | Reads the agent rows, calls the score-fact contract and writes the record and its outbox row |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| RW-REFADM | Holds neither right named here; refused on the two reads and on the export with MSG-P4-002 |

The legacy permission list of RWB-E8-005 gives Platform administration R to RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM and does not list RW-RISK, while FSD P10 v3 A2.16 names the risk and model risk officer as the primary user; TSD P10 v2 T-A.2 gives the runs read Platform administration R and the metrics read Rules and parameters R. The right under which RW-RISK reads the pack is therefore Not specified in the source documents (GAP-0642; ASM-1038) and is reconciled by rwb-access. The per-service login name is Not specified in the source documents (GAP-0642; ASM-1042).

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-036 to DF-AGT-060 | agent_run | agent_code, agent_version, prompt_version, model_version, case_id, autonomy_mode, status, fallback, confidence, latency_ms, cost_thb, data_as_of, run_at, evaluation_run_id, segment_product_group, segment_region_code | Read |
| DF-AGT-097 to DF-AGT-102 | agent_feedback | agent_run_id, item_key, verdict, reason, decision_log_id | Read |
| DF-AGT-103 to DF-AGT-111 | agent_alert | agent_code, alert_type, segment, business_date, measured_value, threshold_value, sent_to_role, sent_at | Read |
| DF-AGT-070 to DF-AGT-085 | agent_evaluation_run | agent_code, policy_version, prompt_version, model_version, status, finished_at, failure_counts | Read |
| DF-AGT-001 to DF-AGT-025 | agent_policy | agent_code, policy_version, model_code, model_version, autonomy_mode, segment_product_group, segment_region_code, daily_cost_cap_thb, alert_role, review_date, valid_from, valid_to, status | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision, owner P7) | all fields, written through P7's library and sealed by rwb-decision | Write locally |
| DF-ACE-270 to DF-ACE-279 | v_ace_score | score_key, account_key, model_code, model_version, score_value, estimate_value and the four remaining fields | Read, through rwb-source-data's contract (DP-05) |
| DF-REF-001 to DF-REF-015 | rule_row (rwb_decision, owner P7) | No longer read by this slice: the version on the record is `agent_policy.policy_version` with the agent, prompt and model versions of the runs, and no Drools package is evaluated by a committee review | Not used |

Field IDs are those of the Logical Data Model and Data Dictionary v9. The pack is built inside `rwb_agent` and no foreign key crosses a schema (DP-01). The score facts are the only data of another service: they are read through rwb-source-data's contract and never from `v_ace_score` directly, and their operation is Not specified in the source documents (GAP-0642; ASM-1035). The account key of a score row is consumed and never written to a pack member, an export column or a log; the segment is the agent, the product group and the region, so the pack carries no account and no personal data. The free-text reason and any subject identifier of an agent_feedback row are read only to be dropped and are written to no pack member, export column or log (BR12; AC7). The composition of `agent_alert.segment` is the one the drift story records and is not restated here. The lists read are LOV-FEEDBACK, LOV-AGENT-ALERT and LOV-AGENT-RUN, held as reference data of rwb-case (DP-06, DP-07); the parameters read are the thresholds, caps and review date of agent_policy; the DF-ACE-270 to DF-ACE-279 values used by the Given and test-data lines come from the rwb-source-data fake of §12.8 only (DP-05).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Right | Response | Note |
|---|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-runs` | Platform administration R | AgentRunsPack: the runs, the acceptance and override counts, the fallbacks and the failure counts, per agent, version, segment and day | TSD P10 v2 API-P10-001; the shape is fixed by RWB-P10-E8005-CON |
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | Rules and parameters R | AgentMetricsPack: one measure set per agent, version, segment and day, with the incidents of the window | TSD P10 v2 API-P10-009; the shape is fixed by RWB-P10-E8005-CON |

Both operations are declared with query `agent`, `from` and `to` for the runs read and `agent`, `segment`, `version`, `from` and `to` for the metrics read (TSD P10 v2 T-A.2), one hop with a 2 s budget from the gateway-bff route, and an export of the same rows as JSON or as text/csv. Their member-level shape, their export rule, their errors and their rights are the contract of RWB-P10-E8005-CON; this story implements them and adds no third operation.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-0642; ASM-1035) | rwb-source-data (P1) | The ACE score facts of the model code and model version in force: `score_key`, `account_key`, `model_code`, `model_version`, `score_value`, `estimate_value` and the four remaining fields (DP-05) | One hop, 2 s |

No `POST /api/recovery/access/v1/authorise` call is made by this story: the rights of the two reads are declared by the contract and enforced on the edge and in the controller, and rwb-access owns the matrix.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | record reference, pack reference, business date, policy version, agent, prompt and model versions reviewed, segment set, outcome code, owner role, review date |

The row is written to the outbox in the same transaction as the record and relayed with the CloudEvents envelope (DP-03). One REST base and one topic per service: the service's own topic is `rwb.agent.events.v1` and its events are named `rwb.agent.<Event>.v1`, of which the P10 OUT line of Arch v5 slide 16 and event catalogue row 28 name one, `rwb.agent.AgentRunCompleted.v1` (EV-28). That event belongs to the run story, so no event of this topic is published by this story and the pack is read from the service's rows and not from a topic. No personal data is carried.

#### 12.4 Events consumed

None. The two reads are served on the request path and the story has no inbox handler of its own. The rows the pack reads are written by the run, feedback and monitor steps of this service.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| RecordAndApply | Activity (workflow kit) | `rwb-agent` | Writes the local decision record with its outbox row in one transaction, and returns the record reference; a failed write rolls the transaction back |

No workflow template, no Schedule and no new activity beyond the kit's `RecordAndApply` are introduced: the pack is assembled on the request path of the two reads, and the committee cadence is not a job of this service (Arch v5 slide 44 carries no committee job).

#### 12.6 Schedules

None. The pack covers a window of the rows the service already holds, and no Schedule is created, changed or owned by this story. The committee meets on its own cadence, which no source states and this story does not model (GAP-0642; ASM-1034).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_run | P10 (rwb_agent) | Read only here: the performance, fallback, latency and cost figures of the pack |
| agent_feedback | P10 (rwb_agent) | Read only here: acceptance and overrides over LOV-FEEDBACK |
| agent_alert | P10 (rwb_agent) | Read only here: the incidents of the window over LOV-AGENT-ALERT |
| agent_evaluation_run | P10 (rwb_agent) | Read only here: the failure counts of the latest DONE evaluation run |
| agent_policy | P10 (rwb_agent) | Read only here: the version in force, its model code and version, its caps and its review date |

`decision_log_entry` is a rwb-decision table and is written only through the P7 decision-record library (DP-01, DP-03). No table and no column is added by this story; the index it asks for is the read key of its two operations (ASM-1041).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 contract of the score facts (DP-05) | 40 score rows of "MODEL-A-2026-10" for the business date; an error answer; facts dated 2026-12-14; a model version that is not in force |
| Decision-record library stub | The P7 record contract and `rwb.decision-record.v1` (DP-03) | A committed record with its reference; a forced write failure; the outbox row and its relay; a repeat submission of the same pack |
| gateway-bff composite route stub | The DP-19 route of SCR-46 | The merged answer holding both pack sections; one failing call with the other section served; the refusal of a role without the right with MSG-P4-002 |

Every Given and test-data line of this story takes its score facts from the rwb-source-data WireMock fake above and never from `v_ace_score` (DP-05).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The two pack reads on `/api/recovery/agent/v1` with their export answers; the rwb-source-data score-facts read, one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` published through the outbox; nothing consumed |
| Temporal | 0 workflows, 1 activity | The kit's `RecordAndApply` on the queue `rwb-agent`; the pack is assembled on the request path |
| File | CSV and JSON export of the pack | No file is read; the export is the answer of the read and holds no member the read does not hold |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent`, module `committee`, Java package `th.co.scb.ace.workbench.recovery.agent.committee`. No front-end module: the screen is the monitor story's, and this story serves the two reads the route composes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 resolves to the rwb-source-data contract and to no view of this service: the score facts are not copied into `rwb_agent`, so no `v_ace_*` view is granted to the rwb-agent login (ADR-010). The two H dependencies on platform contract stories and RWB-P10-E8005-CON are the three build dependencies of the metadata rows.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentRunReadController, AgentMetricReadController | Controller | The two read operations on `/api/recovery/agent/v1`, their parameters, their rights, the JSON and CSV answers and the 403, 422 and 503 answers |
| CommitteePackService | Service | Assembles the pack for an agent, a segment and a window, and marks a section as not available instead of defaulting a value |
| RunFactReader | Repository and fact builder | Reads `agent_run` over LOV-AGENT-RUN, and the runs whose `fallback` is true, with their confidence, latency and cost |
| FeedbackReader | Repository and fact builder | Reads `agent_feedback` over LOV-FEEDBACK and joins each verdict to the run and segment it answers |
| IncidentReader | Repository | Reads `agent_alert` over LOV-AGENT-ALERT for the window, including the rows whose `sent_at` is empty |
| EvaluationReader | Repository | Reads the latest DONE `agent_evaluation_run` of the agent version and its `failure_counts` |
| ScoreFactClient | Client | Calls the rwb-source-data operation with one hop, the 2 s timeout and a breaker per downstream (DP-05) |
| PackExporter | Serialiser | Writes the pack as JSON and as text/csv with the same rows and member order as the read |
| CommitteeRecordWriter | Library adapter | Writes the local decision record with the pack reference, the versions, the outcome, the owner role and the review date, hash-linked, in one transaction (DP-03) |

**Database and migrations**

- No new table and no new column in this story. Every table it reads comes from the agent runtime baseline migration of `rwb_agent`, which RWB-P10-E1058-APP owns, and this story adds only reads (ASM-1041).
- One index for the two reads on the key they scan: `agent_run (agent_code, run_at)` and `agent_feedback (agent_run_id)`, so a pack for a window is a range lookup and not a scan. If an index must ship with a migration, its number comes from the rwb-agent Flyway sequence; that number is Not specified in the source documents (GAP-0642; ASM-1041) and no number is claimed here.
- `decision_log_entry` is written only through the P7 library, in the caller's transaction, and is never joined (DP-01, DP-03).

**Configuration and reference data**

- Policy versions in force (RW-COE): `agent_code` over LOV-AGENT, `policy_version`, `model_code`, `model_version`, `autonomy_mode`, the segment product group and region, `daily_cost_cap_thb`, `alert_role`, `review_date` and the watched measures. The caps, the thresholds and the review date are rows of the version in force and their literal values are Not specified in the source documents (GAP-0642; ASM-1034).
- List values of TSD P10 v2 T3.2: LOV-AGENT, LOV-AGENT-RUN, LOV-AGENT-ALERT, LOV-FEEDBACK and LOV-PRODUCT, held as reference data by rwb-case under the §R3 default ruling; the pack reads no list row and holds no copy of a list in code.
- The pack window is the week to the business date and the four headings are performance, acceptance and overrides, incidents and failure counts (ASM-1034).
- The export media types are JSON by default and text/csv on request (ASM-1039).

**Build steps**

1. ScoreFactClient against the rwb-source-data fake, with the 2 s timeout, the breaker and the not-available rule; tests for AC4 and AC10.
2. RunFactReader over `agent_run`, with the LOV-AGENT-RUN buckets, the fallback share and the data error for an unknown status; tests for AC3 and AC11.
3. FeedbackReader and IncidentReader over `agent_feedback` and `agent_alert`, with the override counts and the not-yet-notified rule; test for AC3.
4. EvaluationReader and CommitteePackService, with the not-in-force rule and the zero-run agent; test for AC10.
5. PackExporter with the JSON and CSV answers over the same rows; test for AC8.
6. The two controllers with their rights, their 403 and 422 answers and the PII rule on every member; tests for AC7 and AC9.
7. CommitteeRecordWriter in one transaction with the outbox row, the rollback path and the repeat submission; tests for AC2 and AC5.
8. The gateway-bff route contract test with the two calls, the one failing call and the refusal path; test for AC6.

**Done when.** The tests in section 16 pass, every pack section names the table it was read from, no pack, export or log holds an account key, a pack submitted twice leaves one record, and a pack read while the score contract is down is served with that column marked not available rather than zeroed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required member of the pack or of the outcome is empty | Enter {field}. |
| MSG-P4-002 | A role without the right of the read or of the export opens it | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written on a committee outcome | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three messages are the legacy messages of RWB-E8-005 and keep their wording character for character. MSG-P10-004 is the message FSD P10 v3 A2.6 names for the agent alert sent to the holders of the role; its wording is not in the extracts and it is not restated here. No other message is added by this story.

### 15. Screens and states

SCR-46 Agent monitor, states Shadow; live; paused, is where the pack is read (legacy RWB-E8-005). Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-2900; DOR-RWB-P10-E8005-APP-10). The screen is served by the gateway-bff composite route and it is not changed here: the screen, its states and its other panels belong to the agent monitor story (RWB-P10-E1063-APP). What this story adds is the pack: the agent, the version, the segment and the day, the run counts by status, the fallback share, the acceptance and override counts, the latency and cost values, the incidents with their measured and threshold values, the failure counts and the score column read through rwb-source-data. The three states return the same rows on every read (AC11). The screen fields, their order and their masking are Not specified in the source documents (GAP-0642; ASM-1036) and stay with the monitor story; the pack leaves the Workbench through its JSON and CSV export, which replaces the Power BI integration point of the legacy module (ASM-1036).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-005-01 | AC1 | Component | Agent "SCREENING" in force on 2026-12-15 with policy version "P1"; 50 runs, 40 feedback rows and two alerts of the week; the rwb-source-data stub up; one committee outcome |
| TC-E8-005-02 | AC2 | Component | Decision record store stopped; nothing stored, no outbox row and MSG-P7-003 |
| TC-E8-005-03 | Access | Component | User "U-5001" holding RW-REFADM, which has neither right, calls the runs read, the metrics read and the export; each refused with MSG-P4-002 |
| TC-E8-005-04 | Principle 5 | NFR | Decision record write forced to fail on a committee outcome; no record, no outbox row and no notification |
| TC-E8-005-05 | AC3 | Component | 50 runs over the six statuses with 9 fallbacks; 30 ACCEPTED, 7 CORRECTED and 3 REJECTED; one COST_CAP and one DRIFT alert, the DRIFT one unsent; failure_counts of 2 TIMED_OUT and 1 MODEL_ERROR |
| TC-E8-005-06 | AC4 | Component | rwb-source-data stub returning 40 score facts, then an error, then facts dated 2026-12-14 |
| TC-E8-005-07 | AC5 | Component | One committee outcome on the pack of 2026-12-15, then the same pack submitted again; the record, its outbox row and the repeat |
| TC-E8-005-08 | AC6 | Contract | gateway-bff route stub calling both reads with one hop each; one call failing and the other served; the browser-direct call refused |
| TC-E8-005-09 | AC7 | NFR | Runs and feedback seeded with an account key, a subject id and a free-text reason; pack, export and log scanned for every one of them |
| TC-E8-005-10 | AC8 | Component | The same pack exported as JSON and as text/csv; an undeclared media type refused before any row is written |
| TC-E8-005-11 | AC9 | Component | Callers holding Platform administration R only, Rules and parameters R only, both, and neither; the four answers of the two reads and the export |
| TC-E8-005-12 | AC10 | Component | Agent "EXTRACT" with a policy in force and no run in the window; an agent with no policy version in force on the date |
| TC-E8-005-13 | AC11 | Component | The same pack read in state Shadow, live and paused; the three answers compared row for row |
| TC-E8-005-14 | §12.7 tables | Component | Boundary values at the window edges for the five tables of §12.7 (agent_run, agent_feedback, agent_alert, agent_evaluation_run, agent_policy); Not specified in the source documents (DOR-RWB-P10-E8005-APP-12) |
| TC-E8-005-15 | AC12, BR1 to BR13 | Component | The rows of AC3, the score facts of AC4 and agent "EXTRACT" of AC10 for 2026-12-15; one export; one committee outcome submitted twice; a run status outside LOV-AGENT-RUN and an alert type outside LOV-AGENT-ALERT |
| TC-E8-005-16 | AC13 | Contract | gateway-bff route stub for GET /api/recovery/agent/v1/admin/agent-runs and GET /api/recovery/agent/v1/admin/agent-metrics; each read called without a valid token (401) and one stubbed 404 answer; the 404 condition is Not specified in the source documents (NEWAC-RWB-P10-E8005-APP-AC13); both paths are not yet in rwb-agent.yaml (CG-ALL-2894, CG-ALL-2895) |
| TC-E8-005-17 | AC14 | Component | Activity stub of the pack read and of the committee outcome retried, then timed out on a later attempt; the record, its outbox row and the repeat |

The legacy levels map System to Component, Access to Component and Principle 5 to NFR, because the cross-service behaviour of this key is proved by the integration story of the wave; no `-ITG` copy is held here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the thresholds, the caps, the alert role and the review date are rows of the policy version in force, and the list values are reference data of rwb-case (BR-P10-016).
- No personal data in logs, tests, events or exports: the pack holds agent codes, segments, statuses, counts, rates, costs and dates; an account key or a subject id is consumed and never written to a pack member, a CSV column or a log, and a free-text reason is not carried into the pack or a log.
- No read of another service's tables: the score facts come through rwb-source-data's contract and the pack rows from `rwb_agent`; the record is written through the P7 library; `rwb_agent` holds no foreign key into another schema (DP-01, DP-05).
- The decision record is written before the outcome is shown as taken, in one transaction with its outbox row; a failed write rolls the transaction back and nothing is stored (R-UNI-39).
- The reads start no agent run, retry no run and change no run status: the 60-second fallback of R-UNI-32 stays with the run step.
- The story moves no case status and raises no task or assignment row; the case side of a committee outcome belongs to rwb-case.
- No value is defaulted for a section whose facts are missing: the section is marked as not available with the reason of the run.
- Only the decision record and its outbox row are written; no copy of a score row, an evaluation row or a run row is written outside `rwb_agent`.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (the legacy story carries no requirement ID) | Agent performance, overrides and incidents reach the strategy and model committee | No BRD section carries the feature (GAP-0642) | FEAT-AGT-16 | All recovery processes (legacy RWB-E8-005) | BR-P10-016 | TC-E8-005-01, TC-E8-005-05 |
| None (the legacy story carries no requirement ID) | The result is written to the decision log with the rule version, and nothing changes when it cannot be recorded | No BRD section carries the feature (GAP-0642) | FEAT-AGT-16 | All recovery processes (legacy RWB-E8-005) | R-UNI-39 | TC-E8-005-02, TC-E8-005-04, TC-E8-005-07 |
| R-UNI-39 | The decision record is written before the change and a failed write changes nothing | Business Rules and Routing Logic v4, Universal rules | FEAT-AGT-16 | All recovery processes | R-UNI-39 | TC-E8-005-04, TC-E8-005-07 |
| D-RCV-60 DP-01 | The pack is built from the service's own schema and no other service's table is read | Template and Rules §R5.5; Architecture v5 slide 41 | FEAT-AGT-16 | All recovery processes | None | TC-E8-005-05, TC-E8-005-12 |
| D-RCV-60 DP-03 | The committee outcome is recorded locally through the library and carried on the shared topic | Template and Rules §R5.5; Decision Log D-RCV-60 | FEAT-AGT-16 | All recovery processes | R-UNI-39 | TC-E8-005-02, TC-E8-005-04, TC-E8-005-07 |
| D-RCV-60 DP-05 | The ACE score facts are read through the owner's contract and never from a table | Template and Rules §R5.5; Architecture v5 slides 15 and 45 | FEAT-AGT-16 | All recovery processes | None | TC-E8-005-06 |
| D-RCV-60 DP-13 and DP-19 | The pack is read on the agent base through the gateway-bff route and the browser calls no owner service | Template and Rules §R5.5; Architecture v5 slides 13 and 41 | FEAT-AGT-16 | All recovery processes | None | TC-E8-005-08, TC-E8-005-11 |

The legacy story RWB-E8-005 carries no requirement ID: it names its feature (FEAT-AGT-16) and no BRD in the extracts carries that feature, so no BRD section and no requirement is cited for it and the absence is recorded as GAP-0642. The feature source is the Epics 3 to 8 Specification v3 row E8 · P10 · FEAT-AGT-16 and FSD P10 v3 A2.16; the rule is R-UNI-39; the decision is D-RCV-60.

### 19. Out of scope

- The agent monitor run, its Schedule, its run summary, the cost-cap alert and the monitor panels of SCR-46 with their states (FEAT-AGT-06; RWB-P10-E1063-APP).
- The agent run itself, the guardrail checker and the 60-second rule fallback of the run step (FEAT-AGT-01, FEAT-AGT-02, FEAT-AGT-11; RWB-P10-E1058-APP).
- The drift check and its alert of type DRIFT, which this pack reads as an incident and does not raise (FEAT-AGT-13; RWB-P10-E3031-APP).
- The evaluation harness that produces the failure counts and the scores the pack reads (FEAT-AGT-05; RWB-P10-E1060-APP).
- The change, the approval and the rollback of a policy version, its caps and its review date (FEAT-AGT-12; RWB-P10-E3030-APP).
- The champion and challenger test of two model versions (FEAT-AGT-14; RWB-P10-E8003-APP).
- The central ledger, its sealing and the ledger read (P7 rwb-decision).
- The score facts themselves, their data product and its freshness rule (P1 rwb-source-data).
- The roles, the rights, the scope and the masking rules (P4 rwb-access), and the reconciliation of the RW-RISK right on the pack.
- The member-level shape, the export rule, the errors and the rights of the two operations (RWB-P10-E8005-CON).
- The deployment of this capability: chart values, queue and topic provisioning, dashboards and the runbook.
