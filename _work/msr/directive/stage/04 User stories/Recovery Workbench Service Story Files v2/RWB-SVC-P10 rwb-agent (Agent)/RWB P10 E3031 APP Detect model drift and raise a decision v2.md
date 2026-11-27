# RWB-P10-E3031-APP Detect model drift and raise a decision

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E3031-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-P10-I |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-031 for rwb-agent. The drift check stays with the service that owns the agent rows: the facts are built per agent and segment from `agent_run` and `agent_evaluation`, the calibration figure is read from the ACE score facts through rwb-source-data's contract (DP-05), the thresholds and the review date are rows of the policy version in force, a breach writes `agent_alert` with type DRIFT together with the local decision record that names the owner role and the review date (DP-03), and the result is read on SCR-46 through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E3031-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (8 resolved, 9 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer (RW-RISK)**, I want **the Workbench to watch the calibration and the drift of each agent and segment on the rows its own runs and evaluations leave, to raise a drift alert that carries the measured value against the threshold of the policy version in force, and to record a decision with an owner role and a review date on a breach**, so that **an agent whose answers are drifting is caught on evidence rather than on a complaint, a person owns the correction with a date on it, and no alert is raised for a segment whose sample is too small to prove anything**.

### 2. Business rationale

The legacy story RWB-E3-031 gave one unattended check to the risk and model risk officer: it watched calibration and drift, it raised a decision with an owner and a date on a breach, and it wrote the result to the decision log with the rule version (FEAT-AGT-13; FSD P10 v3 A2.13). It depends on FEAT-AGT-06, the agent monitor that gathers the runs, the fallbacks and the evaluation scores in one place. Without the check an agent that starts answering outside its reviewed behaviour keeps preparing work for officers, and nobody holds a dated decision to fix it. The BOT AI Risk Management Guidelines of 12 Sep 2025 name lifecycle risk management and accuracy as a condition of running the agents at all, and Arch v5 keeps the AI inside rwb-agent where it can be switched off (slide 35).

In the target the evidence and the check are in the same service. rwb-agent owns the agent policies, the prompts, the runs, the guardrails and the evaluations (Arch v5 slide 41), so the drift step reads `agent_run` for the run outcomes of the window — the LOV-AGENT-RUN statuses, the fallback flag and the confidences — and `agent_evaluation` with `agent_evaluation_run` for the latest DONE evaluation of the agent version: its agreement rate, its precision, its recall and its sample size. The calibration figure is the one fact of another service: it comes from the ACE score facts, read through rwb-source-data's contract and never from a table (DP-05; DP-01). The thresholds, the minimum sample, the alert role and the review date are rows of the `agent_policy` version in force, so no value a business person may change is written in code (BR-P10-013).

On a breach the step writes `agent_alert` with `alert_type` DRIFT, the segment, the business date, the measured value, the threshold value and the role that holds the alert, and it writes the local decision record in the same transaction, which is what makes the owner role and the review date part of the decision and not part of a screen (DP-03; R-UNI-39). The notification leaves through the ACE notification path and the row keeps `sent_at` empty until it succeeds, so a notification outage loses no alert (R-UNI-33, R-UNI-35; FSD A2.6 AC-EXC-P10-006-03). The officer then reads the alert and the decision on SCR-46 Agent monitor through the gateway-bff composite route, which composes the agent read with the other services the screen needs (DP-19).

The realignment work is what leaves the slice. The legacy read of `rule_row` for the rule version goes, because no Drools package decides a drift breach: the version on the record is the policy version of `agent_policy`, and `rule_row` stays with rwb-decision. The legacy `assignment` row goes, because a breach raises a decision with an owner role rather than a case task, and `assignment` and `task` stay with rwb-case. The direct read of the score view becomes the rwb-source-data contract, the decision-log write becomes the local decision-record library plus the shared topic `rwb.decision-record.v1`, and the screen stops being served by the monolith and comes from the gateway-bff composite route.

This story owns both legacy criteria of RWB-E3-031 — AC1 and AC2 — and copies them verbatim in section 7. AC3 to AC10 are new and test the microservice deliverable of the title only. The legacy story carries no requirement ID; section 18 records that and traces the feature instead.

### 3. Preconditions

- RWB-PLT-E1027-CON is published: the local decision-record library, the record shape and the shared topic `rwb.decision-record.v1` with its CloudEvents envelope. This story writes its record through the library and never writes the shared topic directly.
- RWB-PLT-N001-CON is published: the gateway-bff composite route contract for SCR-46 and its stub, so the exposure of the result is built and tested before the screen story lands.
- The `rwb_agent` schema exists with the agent runtime baseline migration — `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation`, `agent_feedback` and `agent_alert` (TSD P10 v2 T3.1; RWB-P10-E1058-APP owns the schema and the baseline). This story issues no migration of its own (ASM-1065).
- The epic design of service epic RWB-SVC-P10 under business epic EP03 is the design this story builds against. The signed epic design record is not held in the story or in the source documents, so no sign-off date and no signatory are claimed: the sign-off is Not specified in the source documents (DOR-RWB-P10-E3031-APP-14).
- At least one agent has run and one evaluation has finished for the business date, because the facts are built from rows and not from a calculation of this story (FEAT-AGT-01, FEAT-AGT-05, FEAT-AGT-06).
- Policy versions are in force for the business date with `agent_code`, `policy_version`, `model_code`, `model_version`, `autonomy_mode`, `segment_product_group`, `segment_region_code`, `confidence_floor`, `alert_role`, `review_date` and `watch_measures`. The threshold of each watched measure, the minimum sample and the review date are rows of the version in force, and their literal values are Not specified in the source documents (GAP-0646; ASM-1060).
- The list values used by the step are those of TSD P10 v2 T3.2: LOV-AGENT (INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER), LOV-AGENT-ALERT (COST_CAP, DRIFT), LOV-AGENT-RUN (ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, TOOL_UNAVAILABLE, MODEL_ERROR, DISABLED), LOV-PRODUCT (MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED) and LOV-REGION. The lists are reference data owned by rwb-case under the §R3 default ruling, and the step holds no copy of a list in code.
- The ACE score facts of the model code and model version in force are reachable through rwb-source-data's contract: `score_key`, `account_key`, `model_code`, `model_version`, `score_value`, `estimate_value` and the four remaining fields of DF-ACE-270 to DF-ACE-279. The exact operation and its product path are Not specified in the source documents (GAP-0646; ASM-1063).
- The drift window is the week to the business date, and the cadence belongs to the agent monitor run that starts the step (ASM-1061).
- The login is the rwb-agent login (DP-02): its name is Not specified in the source documents (GAP-0646; ASM-1069).

### 4. Flow

1. The agent monitor run for the business date has finished and has left the runs and the evaluation results of the date in `rwb_agent`. The DriftCheck step is registered at the end of that run on task queue `rwb-agent`; it is also startable for a business date on its own, so it is built and tested on Day 1 and the wiring into the monitor run belongs to the monitor story (FEAT-AGT-06; ASM-1061).
2. The step reads the policy versions in force on the business date from `agent_policy` — a version whose `valid_from` is after the date, or whose `valid_to` is before it, is not in force — and takes the agent, the model code and version, the segment product group and region, the `alert_role`, the `review_date` and the `watch_measures` of each.
3. For each agent and segment in force, DriftFacts builds one fact set from three sources. From `agent_run` it counts the runs of the window by `status` over LOV-AGENT-RUN, the runs whose `fallback` is true, and the confidence values. From `agent_evaluation_run` and `agent_evaluation` it takes the latest run in status DONE for the agent version with its `sample_size`, `agreement_rate`, `precision_value` and `recall_value`. From the rwb-source-data contract it takes the score facts of the model code and version and computes the calibration figure as the mean absolute difference between `score_value` and `estimate_value`.
4. A score row with an empty `estimate_value` counts as not scored: it is listed in the fact set and it is never counted as a zero difference. The number of scored and unscored rows is part of the facts, so the officer can see what the figure rests on.
5. A run whose `status` is not in LOV-AGENT-RUN is not mapped to a bucket: it is listed as a data error with the value it carried and it is excluded from the counts, and the step continues.
6. DriftDetector compares each watched measure of the policy version with its threshold. A measure whose sample is below the minimum sample of the policy version is not compared at all: the segment is reported as "not enough feedback" and raises no alert (FSD A2.6 AC-EXC-P10-006-04; legacy RWB-E2-031).
7. RecordAndApply runs in one `rwb_agent` transaction: it writes the `agent_alert` row with `alert_type` DRIFT, the `agent_code`, the `segment`, the `business_date`, the `measured_value`, the `threshold_value` and `sent_to_role` from `alert_role`, with `sent_at` empty; it writes the local decision record with the owner role and the review date; and it inserts the DecisionRecorded row in the outbox. A failed record write rolls the whole transaction back, so no alert row and no outbox row exist (DP-03; R-UNI-39).
8. The notification of the alert leaves through the ACE notification path to the holders of the role in `sent_to_role`. `sent_at` is written when the notification succeeds; where the path is unavailable the row keeps `sent_at` empty and it is sent when the sender succeeds, so no alert is lost (R-UNI-33, R-UNI-35; FSD A2.6 AC-EXC-P10-006-03).
9. The DecisionRecorded row is relayed from the outbox to `rwb.decision-record.v1`, and rwb-decision seals it into the central ledger. The step waits for no confirmation: the drift decision is not a point of no return.
10. A rerun for the same business date recomputes the same facts, finds the alert of the key and writes nothing: no second alert row, no second record and no second notification. The repeat is counted once in the step summary (R-UNI-40).
11. The officer reads the alert and the decision on SCR-46 Agent monitor. The screen is served by the gateway-bff composite route, which calls the agent read on `/api/recovery/agent/v1` and merges the answers; the browser calls no owner service directly (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The sample of an agent and segment is below the minimum sample of the policy version | No measure is compared, no alert row and no record exist, and the monitor shows "not enough feedback" for the segment | None | AC7 |
| X2 | The rwb-source-data contract returns an error, or the score facts are older than the business date | The calibration measure is recorded as not available for that agent and segment; no alert and no record are written for it; the measure built from the agent's own rows is still written | None | AC10 |
| X3 | The local decision record cannot be written | The transaction rolls back: no alert row, no outbox row and no notification; the step fails and is retried | MSG-P7-003 | AC2 |
| X4 | The notification path is unavailable | The alert row is kept with `sent_at` empty and sent when the sender succeeds | None | AC4 |
| X5 | A run carries a status outside LOV-AGENT-RUN | The value is listed as a data error and excluded from the counts; no bucket is invented and the step continues | None | AC3 |
| X6 | The policy version in force has no `review_date` | No record and no notification are written for that version; the version is named as a configuration exception, because a decision without a date is not raised and no date is defaulted | None | AC5 |
| X7 | The step runs twice for the same business date | No second alert row, no second record and no second notification | None | AC6 |
| X8 | An agent version has a policy in force and no run in the window | No alert is raised and the segment shows "not enough feedback" (FSD A2.6 AC-EXC-P10-006-02) | None | AC7 |
| X9 | A caller without the Platform administration right opens the monitor route | Refused; nothing is returned and nothing is written | MSG-P4-002 | AC8 |

The step writes no case field and raises no case task on any path, so none of these exceptions moves a case. The rollback of X3 and the retry of X4 are the behaviours FSD A2.13 AC-EXC-P10-013-02 and FSD A2.6 AC-EXC-P10-006-03 describe.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the platform contracts RWB-PLT-E1027-CON and RWB-PLT-N001-CON, the agent runtime baseline and the rwb-source-data fake; it waits for no in-lane story and starts itself for a business date |
| Negotiable | The thresholds, the minimum sample, the watched measure, the alert role and the review date are rows of the policy version in force; the segment composition and the window are agreed defaults, recorded as assumptions |
| Valuable | A drifting agent is caught on its own run and evaluation evidence, and a named role owns a dated decision to correct it |
| Estimable | One step, one facts builder, one detector, one alert writer, one decision-record writer, one client, no controller |
| Small | Fits one sprint with its tests |
| Testable | Each of the ten criteria of section 7 is one automated test against the rwb-source-data and decision-record fakes; no criterion needs a screen |

### 7. Acceptance criteria

```gherkin
Feature: Detect model drift and raise a decision

  Background:
    Given agent "SCREENING" is in force on 2026-12-15 with policy version "P1" and model version "MODEL-A-2026-10"
    Given its segment is product group "MORTGAGE" and region "BKK"
    Given its policy version holds the drift threshold, the minimum sample and review date 2027-01-31 as rows

  Scenario: AC1 Detect model drift and raise a decision (legacy RWB-E3-031 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then watches calibration and drift, and raises a decision with an owner and a date on a breach
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E3-031 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The drift facts are built per agent and segment (new, D-RCV-60)
    Given the week to 2026-12-15 holds 50 runs of "SCREENING" on "SCREENING:MORTGAGE:BKK": 34 ANSWERED, 6 TIMED_OUT, 4 GUARDRAIL_FAILED, 3 BELOW_FLOOR, 2 TOOL_UNAVAILABLE and 1 MODEL_ERROR
    Given the latest evaluation run of "SCREENING" in status DONE holds sample size 200, agreement rate 0.9100, precision 0.9444 and recall 0.8947 on the same segment
    Given the rwb-source-data contract mock returns 40 score facts of "MODEL-A-2026-10" with score_value and estimate_value, and 4 rows with an empty estimate_value
    When the DriftCheck step runs for business date 2026-12-15
    Then one fact set holds the run counts by the statuses of LOV-AGENT-RUN, the fallback share of the runs whose fallback is true, the agreement rate and the sample size of the latest DONE evaluation run, and the calibration figure over the 40 scored rows
    Then the 4 rows with an empty estimate_value are listed as not scored and are not counted as a zero difference
    Then every run and evaluation field is read from agent_run, agent_evaluation_run and agent_evaluation in rwb_agent, and the score facts from the rwb-source-data contract, and no table of another schema is read

  Scenario: AC4 A breach raises a drift alert for the agent and segment (new, D-RCV-60)
    Given the fallback share of "SCREENING" on "SCREENING:MORTGAGE:BKK" is above the drift threshold of policy version "P1"
    When the DriftCheck step runs for business date 2026-12-15
    Then one agent_alert row holds agent_code "SCREENING", alert_type "DRIFT", segment "SCREENING:MORTGAGE:BKK", business_date 2026-12-15, the measured_value of the facts, the threshold_value of the policy row and sent_to_role "RW-RISK" from alert_role
    Then sent_at is empty until the notification to the holders of RW-RISK succeeds, and it is written when they are notified
    Then no agent_alert row holds alert_type "COST_CAP", and no alert is written for agent "INTAKE", which is under its threshold

  Scenario: AC5 The decision names the owner role and the review date (new, D-RCV-60)
    Given the breach of AC4 and policy version "P1" with alert_role "RW-RISK" and review_date 2027-01-31
    When the DriftCheck step records the breach for 2026-12-15
    Then one decision record is written before the notification leaves, and it names agent "SCREENING", policy version "P1", model version "MODEL-A-2026-10", alert type "DRIFT", segment "SCREENING:MORTGAGE:BKK", the measured and threshold values, owner role "RW-RISK" and review date 2027-01-31
    Then the agent_alert row, the decision record and the outbox row commit in one rwb_agent transaction
    Then rwb.decision.DecisionRecorded.v1 is written to the outbox on rwb.decision-record.v1 with the record reference and the facts of the breach
    Then no rule row is read and no package version is named, because no Drools package decides a drift breach

  Scenario: AC6 A rerun for the same business date raises nothing new (new, D-RCV-60)
    Given the alert row and the decision record of AC4 exist for business date 2026-12-15
    When the DriftCheck step runs again for 2026-12-15 over the same facts
    Then no second agent_alert row and no second decision record exist for agent "SCREENING", segment "SCREENING:MORTGAGE:BKK" and business date 2026-12-15
    Then no second notification is sent and the repeat is counted once in the step summary

  Scenario: AC7 A segment with too small a sample raises no drift alert (new, D-RCV-60)
    Given the week to 2026-12-15 holds 12 runs of "SCREENING" on "SCREENING:MORTGAGE:BKK"
    Given the minimum sample of policy version "P1" is above 12
    When the DriftCheck step runs for 2026-12-15
    Then no agent_alert row exists for "SCREENING" on that segment and date
    Then no decision record is written for that segment
    Then the monitor shows "not enough feedback" for the segment
    When an agent version with a policy in force has no run in the window
    Then no alert is raised for it either

  Scenario: AC8 The result reaches SCR-46 through the gateway-bff route only (new, D-RCV-60)
    Given the alert row and the decision record of AC4 exist for 2026-12-15
    When the risk and model risk officer opens SCR-46 Agent monitor in state live
    Then the alert and the decision are served by the gateway-bff composite route, with agent "SCREENING", alert type "DRIFT", segment "SCREENING:MORTGAGE:BKK", the measured and threshold values and review date 2027-01-31
    And the browser calls no owner service directly
    Given user "U-5001" holds RW-REFADM, which has no Platform administration right
    When "U-5001" calls the same route
    Then the call is refused with 403 and MSG-P4-002 and nothing is written

  Scenario: AC9 The step moves no case and rewrites no run (new, D-RCV-60)
    Given the week to 2026-12-15 holds one run in status TIMED_OUT with fallback true under R-UNI-32 and one run in status DISABLED
    When the DriftCheck step runs for 2026-12-15
    Then no agent_run row is inserted or updated, and no run is started, retried or ended by the step
    Then the TIMED_OUT run counts as a fallback in the facts and its fallback value stays true
    Then the DISABLED run counts in the DISABLED bucket and its status is not changed
    Then no case status is read or written for the segment and no task is raised

  Scenario: AC10 The score facts are unavailable or stale (new, D-RCV-60)
    Given the rwb-source-data contract mock returns an error on the first run, and facts dated 2026-12-14 on the second
    When the DriftCheck step runs for 2026-12-15 on each
    Then the calibration measure is recorded as not available for "SCREENING" on "SCREENING:MORTGAGE:BKK", with the reason of the run
    Then no agent_alert row and no decision record are written for that measure
    Then the measure built from agent_run and agent_evaluation is still written, and no value is defaulted for the missing one
```

AC1 and AC2 are the legacy criteria of RWB-E3-031, copied verbatim. AC3 to AC10 are new for this service change and test only the drift step, the alert, the decision record, the score-fact read and the exposure of the result.

Scenario: AC11 Every business rule BR1 to BR12 in section 8 holds in the step run (new, D-RCV-60)
    Then each rule BR1 to BR12 holds in the step run

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The calibration and the drift of every agent and segment are watched on the rows the agent leaves, and a breach raises a decision with an owner and a date | FEAT-AGT-13; FSD P10 v3 A2.13; legacy RWB-E3-031 |
| BR2 | The agent or the model that does not answer inside 60 seconds falls back to the rule result and the fallback is recorded on the decision; the drift step counts that fallback as a run outcome and never re-decides it | R-UNI-32; TSD P10 v2 NFR-010 |
| BR3 | The decision record is written before the notification leaves and no alert proceeds unrecorded: the alert row, the record and the outbox row are one transaction | Principle 5; R-UNI-39; DP-03 |
| BR4 | No value a business person may change is written in code: the threshold of each watched measure, the minimum sample, the alert role and the review date are rows of the `agent_policy` version in force | BR-P10-013 |
| BR5 | The score facts are read through rwb-source-data's contract and the agent rows from `rwb_agent`; no table of another service is read and no foreign key crosses a schema | DP-01; DP-05; ADR-010 |
| BR6 | One decision per breach: an alert for the same agent, segment and business date is written once, a rerun writes nothing and the repeat is counted; where several measures breach for one agent, segment and date, the alert row carries the first breaching measure in the order of the policy row and the decision record names every measure that breached, because `agent_alert` has no measure column | R-UNI-40; DF-AGT-103 to DF-AGT-111; ASM-1067 |
| BR7 | A drift alert carries `alert_type` DRIFT, one of the two values of LOV-AGENT-ALERT; the cost cap is COST_CAP and belongs to the monitor story | TSD P10 v2 T3.2; FEAT-AGT-06 |
| BR8 | A segment below the minimum sample of the policy version raises no drift alert and is shown as "not enough feedback" | FSD P10 v3 A2.6 AC-EXC-P10-006-04; legacy RWB-E2-031; ASM-1064 |
| BR9 | The alert is addressed to the role in `agent_policy.alert_role` and the notification goes through the ACE notification path to the holders of that role; the row keeps `sent_at` empty until the notification succeeds | FSD P10 v3 A2.6 AC-ALT-P10-006-01 and AC-EXC-P10-006-03; DF-AGT-015 |
| BR10 | The run outcomes are counted under the values of LOV-AGENT-RUN; a value outside the list is a data error and is never mapped to a bucket | TSD P10 v2 T3.2 |
| BR11 | The step writes no case status and no agent run row: `recovery_case` belongs to rwb-case and `agent_run` is written by the run step only | TSD P10 v2 T4; DP-01 |
| BR12 | The date on the decision is `review_date` of the policy version in force; a version in force without a review date supports no decision and no date is defaulted | FSD P10 v3 A2.13; DF-AGT-016; ASM-1066 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| NO_ALERT | DRIFT_BREACH | a watched measure is over its policy threshold and the sample is at or above the minimum | ALERT_OPEN |
| ALERT_OPEN | DECISION_RECORDED | the alert row, the decision record and the outbox row commit in one transaction | RECORDED |
| RECORDED | NOTIFICATION_SENT | the notification path confirms the send | RECORDED, with `sent_at` set |
| ALERT_OPEN | DECISION_WRITE_FAILED | the decision record cannot be written | NO_ALERT, because the transaction rolls back |

These are the states of the drift evaluation and of its alert row, not a case state machine. `agent_alert` holds no status column (TSD P10 v2 T3.1, DF-AGT-103 to DF-AGT-111), so ALERT_OPEN and RECORDED are read from the row and its decision record, and the last transition is read from `sent_at`. **This story moves no case status**: `recovery_case.status` is neither read nor written, no task and no assignment row is written, and the case side of a drift decision belongs to rwb-case (BR11).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Risk and model risk officer (RW-RISK) | The primary reader of the drift alert and its decision on SCR-46, and the role the policy addresses through `alert_role` |
| Center of excellence analyst (RW-COE) | Owns the policy versions, their `watch_measures`, the review date and the alert role; reads the alert and the decision |
| Platform administrator (RW-PLATADM) | Reads the alert and the run evidence the facts rest on, and may rerun the step for a business date |
| rwb-agent service identity (the rwb-agent login, DP-02) | Runs the step; reads the agent rows and the score facts through their contracts; writes the alert row, the decision record and the outbox row |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| SY-RULES rules identity | Not used by this story: no Drools package is evaluated for a drift breach, so no rule row and no package version is read |
| RW-AUDIT, RW-COMPLY | Read the alert and the decision through the monitor read, as the legacy permission list allows |
| RW-REFADM | Holds no Platform administration right; refused on the monitor route with MSG-P4-002 |

The legacy permission list of RWB-E3-031 gives Platform administration R to RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM and does not list RW-RISK, while FSD P10 v3 A2.6 and A2.13 name the risk and model risk officer as the primary user; the right under which RW-RISK reads the drift alert is therefore Not specified in the source documents (GAP-0646; ASM-1068) and is reconciled by rwb-access with the monitor story. The per-service login name is Not specified in the source documents (GAP-0646; ASM-1069); the story names it "the rwb-agent login (DP-02)" until it is agreed.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-103 to DF-AGT-111 | agent_alert | id, agent_code, alert_type, segment, business_date, measured_value, threshold_value, sent_to_role, sent_at | Write |
| DF-AGT-036 to DF-AGT-060 | agent_run | agent_code, model_version, status, fallback, confidence, run_at, data_as_of, segment_product_group, segment_region_code, evaluation_run_id | Read |
| DF-AGT-070 to DF-AGT-085 | agent_evaluation_run | agent_code, sample_code, sample_version, policy_version, prompt_version, model_version, status, finished_at | Read |
| DF-AGT-086 to DF-AGT-096 | agent_evaluation | evaluation_run_id, approach, label_key, sample_size, agreement_rate, precision_value, recall_value | Read |
| DF-AGT-001 to DF-AGT-025 | agent_policy | agent_code, policy_version, model_code, model_version, autonomy_mode, segment_product_group, segment_region_code, confidence_floor, alert_role, review_date, watch_measures, valid_from, valid_to, status | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision, owner P7) | all fields, written through P7's library and sealed by rwb-decision | Write locally |
| DF-ACE-270 to DF-ACE-279 | v_ace_score | score_key, account_key, model_code, model_version, score_value, estimate_value and the four remaining fields | Read, through rwb-source-data's contract (DP-05) |
| DF-WRK-009 to DF-WRK-016 | assignment (rwb_case, owner P3) | No longer read by this slice: a drift breach raises a decision with an owner role, not a case task; `assignment` and `task` stay with rwb-case and carry no row for this feature | Not used |
| DF-REF-001 to DF-REF-015 | rule_row (rwb_decision, owner P7) | No longer read by this slice: the version on the decision is `agent_policy.policy_version`, and no Drools package is evaluated, so no rule row and no package version is read | Not used |

Field IDs are those of the Logical Data Model and Data Dictionary v9. The facts are built inside `rwb_agent` and no foreign key crosses a schema (DP-01). The score facts are the only data of another service: they are read through rwb-source-data's contract and never from `v_ace_score` directly, and their operation is Not specified in the source documents (GAP-0646; ASM-1063). The account key of a score row is not written to `agent_alert`: the segment is the agent, the product group and the region, so the alert carries no account and no personal data. The segment string and its composition are Not specified in the source documents (GAP-0646; ASM-1062).

### 12. Contract

The contract versions this story builds against are those of the two platform contracts it depends on. RWB-PLT-E1027-CON publishes the local decision-record library, the record shape and the shared topic `rwb.decision-record.v1`, and that is the version this story writes its record through. RWB-PLT-N001-CON publishes the gateway-bff composite route for SCR-46 on the `/api/recovery/agent/v1` path, the `/v1` path of the consumed agent read. The version of the rwb-source-data score-facts operation is Not specified in the source documents (GAP-0646; DOR-RWB-P10-E3031-APP-23).

#### 12.1 REST operations provided

None. The drift check runs as a step of the agent runtime and not on a request path. The alert and the decision it writes are read through the existing P10 monitor read on `/api/recovery/agent/v1/admin/agent-runs` and `/api/recovery/agent/v1/admin/agent-metrics`, which this story does not own, and through the gateway-bff composite route for SCR-46 (DP-19).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-0646; ASM-1063) | rwb-source-data (P1) | The ACE score facts of the model code and model version in force: `score_key`, `account_key`, `model_code`, `model_version`, `score_value`, `estimate_value` and the four remaining fields (DP-05) | One hop, 2 s |

No `POST /api/recovery/access/v1/authorise` call is made by this story: the step runs unattended under the service identity and exposes no operation, and the rights on the monitor read belong to the story that owns the read.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | decision record reference, agent code, alert type DRIFT, segment, business date, policy version, model version, measured value, threshold value, owner role |

The row is written to the outbox in the same transaction as the alert row and relayed with the CloudEvents envelope (DP-03). No agent event is published for the alert: the P10 OUT line of Arch v5 slide 16 names AgentRunCompleted only, so the alert is read from the table through the monitor read and not from a topic. No personal data is carried.

#### 12.4 Events consumed

None. The step is started by the agent monitor run and reads no topic; it has no inbox handler of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| DriftCheckStep | Step of the agent runtime monitor run (the run and its Schedule belong to the monitor story) | `rwb-agent` | Reads the policies in force, builds the facts, compares the measures, records and notifies, and writes the run summary |
| DriftFacts | Activity | `rwb-agent` | Reads `agent_run`, `agent_evaluation_run`, `agent_evaluation` and the score facts, and returns one fact set per agent and segment |
| DriftEvaluate | Activity | `rwb-agent` | Compares each watched measure with the policy row, applies the minimum sample and names the breaches and the reported segments |
| RecordAndApply | Activity (workflow kit) | `rwb-agent` | Writes the alert row, the decision record and the outbox row in one transaction, and sets `sent_at` when the notification succeeds |

No new workflow template is defined: the step joins the existing agent runtime monitor run of the queue `rwb-agent`, and the four steps of the workflow model apply to it (Temporal and Drools design slide 13).

#### 12.6 Schedules

None new. The cadence of the drift check belongs to the agent monitor run that starts the step; the window is the week to the business date and no Schedule is created, changed or owned by this story (ASM-1061). The Arch v5 job map names no job for the agent monitor (slide 44), so the Schedule itself belongs to the monitor story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_alert | P10 (rwb_agent) | The drift alert row: DF-AGT-103 to DF-AGT-111; created by the agent runtime baseline migration, not by this story |
| agent_run | P10 (rwb_agent) | Read only here: the run outcomes the facts rest on |
| agent_evaluation_run | P10 (rwb_agent) | Read only here: the latest DONE evaluation of the agent version |
| agent_evaluation | P10 (rwb_agent) | Read only here: the agreement rate, the precision, the recall and the sample size |
| agent_policy | P10 (rwb_agent) | Read only here: the version in force, its `watch_measures`, its `alert_role` and its `review_date` |

`decision_log_entry` is a rwb-decision table and is written only through the P7 decision-record library (DP-01, DP-03). The score facts are read from rwb-source-data and no copy of a score row is written into `rwb_agent`.

Reference data read here: the lists LOV-AGENT-ALERT (BR7) and LOV-AGENT-RUN (BR10), and the parameters of the `agent_policy` version in force: watch_measures, the drift threshold, the minimum sample, alert_role and review_date (BR4). The reference-data contract for these reads follows DP-06 and DP-07; its named contract is Not specified in the source documents (DOR-RWB-P10-E3031-APP-20).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 contract of the score facts (DP-05) | 40 scored rows and 4 rows with an empty `estimate_value` for "MODEL-A-2026-10"; an error answer; facts dated 2026-12-14; facts for a model version that is not in force |
| Decision-record library stub | The P7 record contract and `rwb.decision-record.v1` (DP-03) | A committed record with its reference; a forced write failure; the outbox row and its relay |
| gateway-bff composite route stub | The DP-19 route of SCR-46 | The merged screen answer with the alert and the decision; the refusal of a role without Platform administration R with MSG-P4-002 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 1 consumed | The rwb-source-data score-facts read; one hop, 2 s; no operation is provided |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` published through the outbox; nothing consumed |
| Temporal | 0 workflows, 3 activities | DriftFacts, DriftEvaluate and RecordAndApply on the queue `rwb-agent`, inside the existing monitor run |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent`, module `drift`, Java package `th.co.scb.ace.workbench.recovery.agent.drift`. No front-end module: the screen is the monitor story's, and this story feeds it through the gateway-bff route.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Both H dependencies of the table are platform contract stories and are the two build dependencies of the metadata rows. DP-05 resolves to the rwb-source-data contract and to no view of this service: the score facts are not copied into `rwb_agent`, so no `v_ace_*` view is granted to the rwb-agent login (ADR-010).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DriftCheckStep | Step of the agent runtime monitor run | Reads the versions in force, drives the activities, writes the run summary and counts the repeats |
| DriftFacts | Activity and fact builder | Builds one fact set per agent and segment from `agent_run`, `agent_evaluation_run` and `agent_evaluation`, and the calibration figure from the score-fact client |
| ScoreFactClient | Client | Calls the rwb-source-data operation with one hop, the 2 s timeout and a breaker per downstream (DP-05) |
| DriftDetector | Service | Compares each watched measure of the policy row with its threshold, applies the minimum sample and returns the breaches and the "not enough feedback" segments |
| AlertWriter | Repository | Writes the `agent_alert` row and sets `sent_at` when the notification succeeds; holds the key of agent, segment and business date, and the order of the measures of the policy row (ASM-1067) |
| DecisionRecordWriter | Library adapter | Writes the local decision record with the owner role, the review date, the policy version and the model version, hash-linked, in the same transaction (DP-03) |
| Controller | None | The step exposes no operation; the alert is read through the monitor read and the gateway-bff route |

**Database and migrations**

- No new table and no new column in this story. `agent_alert` and its nine fields come from the agent runtime baseline migration of `rwb_agent`, which RWB-P10-E1058-APP owns, and this story adds only what TSD P10 v2 T3.1 already lists (ASM-1065).
- If the baseline does not carry `agent_alert` when the step is picked up, the script that adds it takes its number from the rwb-agent Flyway sequence; that number is Not specified in the source documents (GAP-0646; ASM-1065) and no number is claimed here.
- One index for the step, on the key it reads: `agent_alert (agent_code, alert_type, segment, business_date)`, so the rerun check of AC6 is a key lookup and not a scan. The index name is a naming-library value and not a business value.

**Configuration and reference data**

- Policy versions in force (RW-COE): `agent_code` over LOV-AGENT, `policy_version`, `model_code`, `model_version`, `autonomy_mode`, the segment product group and region, `confidence_floor`, `alert_role`, `review_date` and `watch_measures`. The threshold of each watched measure and the minimum sample are entries of `watch_measures`, whose keys and literal values are Not specified in the source documents (GAP-0646; ASM-1060).
- List values of TSD P10 v2 T3.2: LOV-AGENT, LOV-AGENT-ALERT (COST_CAP, DRIFT), LOV-AGENT-RUN and LOV-PRODUCT for the segment, held as reference data by rwb-case under the §R3 default ruling; the step reads no list row and holds no copy of a list in code.
- The window is the week to the business date, and the minimum sample is a policy row (ASM-1061, ASM-1064).
- The segment is composed of the agent code, the product group and the region within `agent_alert.segment` varchar(30); the composition is Not specified in the source documents (GAP-0646; ASM-1062).

**Build steps**

1. ScoreFactClient against the rwb-source-data fake, with the 2 s timeout, the breaker and the unscored-row handling; tests for AC3 and AC10.
2. DriftFacts over `agent_run` and `agent_evaluation`, with the LOV-AGENT-RUN buckets and the data error for an unknown status; test for AC3 and AC9.
3. DriftDetector with the policy-row thresholds and the minimum-sample guard; tests for AC4, AC7 and AC9.
4. AlertWriter and DecisionRecordWriter in one transaction with the outbox row, and the rollback path; tests for AC2, AC5 and AC6.
5. The notification call and the `sent_at` write, including the unavailable path; test for AC4.
6. The rerun key and the step summary; test for AC6.
7. The gateway-bff route contract test with the refusal path; test for AC8.
8. Register the step at the end of the agent monitor run and run it for a business date on its own over synthetic rows; test for AC6.

**Done when.** The tests in section 16 pass, no alert row exists without its decision record, every decision record names the owner role and the review date of the policy version in force, the rwb-source-data contract tests stay green, and no run of the SIT week raised a drift alert for a segment below its minimum sample.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record cannot be written on a breach | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | A required value of a policy version or of the step is empty | Enter {field}. |
| MSG-P4-002 | A role without the Platform administration right opens the monitor route | You cannot {action} here. Your role does not include it. |

The three messages are the legacy messages of RWB-E3-031 and keep their wording. MSG-P10-004 is the message FSD P10 v3 A2.6 names for the agent alert sent to the holders of the role; its wording is not in the extracts and it is not restated here. No other message is added by this story.

### 15. Screens and states

No screen in this story (legacy RWB-E3-031). SCR-46 Agent monitor, states Shadow, live and paused, shows the drift alert and its decision; it is read through the gateway-bff composite route and it is not changed here, because the screen and its read belong to the agent monitor story (RWB-P10-E1063-APP). What this story adds to that screen is the data: the agent, the alert type, the segment, the measured and threshold values and the review date on the decision, all of them read from `agent_alert` and the decision record through the monitor read and the composite route (DP-19). The screen fields, their order and their masking are Not specified in the source documents (GAP-0646; ASM-1068) and stay with the monitor story.

States of SCR-46 in this story: empty, loading, error and no access are Not specified in the source documents (CG-ALL-2864; DOR-RWB-P10-E3031-APP-10).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-031-01 | AC1 | Component | Agent "SCREENING" in force on 2026-12-15 with policy version "P1"; 50 runs of the week; the drift threshold row; one breach |
| TC-E3-031-02 | AC2 | Component | Decision record store stopped |
| TC-E3-031-03 | Access | Component | User "U-5001" holding RW-REFADM, which has no Platform administration right, calls the SCR-46 route; refused with MSG-P4-002 |
| TC-E3-031-04 | Principle 5 | NFR | Decision record write forced to fail on the DRIFT alert; no alert row, no outbox row and no notification |
| TC-E3-031-05 | AC3 | Component | 50 runs of the week with the six statuses; evaluation run DONE with sample 200 and agreement 0.9100; 40 scored and 4 unscored score facts |
| TC-E3-031-06 | AC4 | Component | Fallback share above the policy threshold for "SCREENING" and under it for "INTAKE"; notification path up, then down |
| TC-E3-031-07 | AC5 | Component | Policy version "P1" with alert_role "RW-RISK" and review_date 2027-01-31; one breach |
| TC-E3-031-08 | AC6 | Component | The step run twice for 2026-12-15 over the same facts |
| TC-E3-031-09 | AC7 | Component | 12 runs in the week against the policy minimum sample; an agent version with a policy and no run |
| TC-E3-031-10 | AC8 | Contract | gateway-bff route stub with the alert and the decision; the refusal of RW-REFADM |
| TC-E3-031-11 | AC9 | Component | One TIMED_OUT run with fallback true and one DISABLED run; snapshot of the `agent_run` rows before and after the step |
| TC-E3-031-12 | AC10 | Component | rwb-source-data stub returning an error, then facts dated 2026-12-14 |
| TC-E3-031-13 | AC11 (BR1 to BR12) | Not specified in the source documents (NEWAC-RWB-P10-E3031-APP-AC11) | Not specified in the source documents (NEWAC-RWB-P10-E3031-APP-AC11) |
| TC-E3-031-14 | Tables of 12.7 (ASM-3438) | Component | Boundary: agent_policy version in force with no review_date; agent_run rows on the first and last day of the week to 2026-12-14 |

The legacy levels map System to Component, Access to Component and Principle 5 to NFR, because the cross-service behaviour of this key is proved by the integration story of the wave. No `-ITG` copy is held here: the integration copies of this key belong to the integration story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the thresholds, the minimum sample, the watched measure, the alert role and the review date are rows of the policy version in force (BR-P10-013).
- No personal data in logs, tests, workflow history or prompts: the facts hold agent codes, segments, counts and rates; the account key of a score row is consumed and never written to `agent_alert` or to a log, and the workflow payloads pass the payload codec.
- No read of another service's tables: the score facts come through rwb-source-data's contract and the agent rows from `rwb_agent`; the record is written through the P7 library; `rwb_agent` holds no foreign key into another schema (DP-01, DP-05).
- The decision record is written before the notification leaves, in one transaction with the alert row; a failed write rolls the whole transaction back (R-UNI-39).
- The step starts no agent run, retries no run and changes no run status: the 60-second fallback of R-UNI-32 stays with the run step.
- The step moves no case status and raises no task or assignment row; the case side of a drift decision belongs to rwb-case.
- No value is defaulted for a measure whose facts are missing: the measure is reported as not available and raises no alert.
- Only the alert and the decision are new data; no copy of a score row, an evaluation row or a run row is written outside `rwb_agent`.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (the legacy story carries no requirement ID) | Calibration and drift are watched, and a decision with an owner and a date is raised on a breach | No BRD section carries the feature (GAP-0646) | FEAT-AGT-13 | All recovery processes (legacy RWB-E3-031) | R-UNI-32 | TC-E3-031-01, TC-E3-031-11 |
| None (the legacy story carries no requirement ID) | The result is written to the decision log with the rule version, and nothing is written when the record fails | No BRD section carries the feature (GAP-0646) | FEAT-AGT-13 | All recovery processes (legacy RWB-E3-031) | R-UNI-39 | TC-E3-031-02, TC-E3-031-04, TC-E3-031-07 |
| R-UNI-32 | The agent or the model that does not answer inside the timeout falls back to the rule result and the fallback is recorded | Business Rules and Routing Logic v4, Universal rules | FEAT-AGT-11 for the fallback; FEAT-AGT-13 counts it | All recovery processes | R-UNI-32 | TC-E3-031-11 |
| D-RCV-60 DP-03 | The decision record is written locally before the action, and the shared topic carries it to the central ledger | Decision log, D-RCV-60; Template and Rules §R5.5 | FEAT-AGT-13 | All recovery processes | R-UNI-39 | TC-E3-031-02, TC-E3-031-04, TC-E3-031-07 |
| D-RCV-60 DP-05 | The ACE score facts are read through the owner's contract and never from a table | Template and Rules §R5.5; Architecture v5 slide 16 | FEAT-AGT-13 | All recovery processes | None | TC-E3-031-05, TC-E3-031-12 |
| D-RCV-60 DP-19 | The screen composes the result through the gateway-bff route and calls no owner service directly | Template and Rules §R5.5; Architecture v5 slides 13 and 41 | FEAT-AGT-13 | All recovery processes | None | TC-E3-031-10, TC-E3-031-03 |

The legacy story RWB-E3-031 carries no requirement ID: it names its feature (FEAT-AGT-13) and no BRD in the extracts carries that feature, so no BRD section and no requirement is cited for it and the absence is recorded as GAP-0646. The feature source is the Epics 3 to 8 Specification v3 row E3 · P10 · FEAT-AGT-13 and FSD P10 v3 A2.13; the rule is R-UNI-32; the decision is D-RCV-60.

### 19. Out of scope

- The agent monitor run, its Schedule, its run summary and the cost-cap alert with type COST_CAP (FEAT-AGT-06; RWB-P10-E1063-APP).
- The agent run itself, the guardrail checker and the 60-second rule fallback of the run step (FEAT-AGT-01, FEAT-AGT-02, FEAT-AGT-11; RWB-P10-E1058-APP and the agent run story).
- The evaluation harness that produces the scores the facts read, and the extraction evaluation (FEAT-AGT-05; RWB-P10-E1060-APP).
- The review of agent risk at the committee, which consumes the alert and the decision (FEAT-AGT-16; Epic 8).
- The change, approval and rollback of a policy version, its `watch_measures` and its review date (FEAT-AGT-12; RWB-P10-E3030-APP).
- The champion and challenger test of two model versions (FEAT-AGT-14; RWB-P10-E8003-APP).
- The central ledger, its sealing and the ledger read (P7 rwb-decision).
- The data products, the freshness rule of a data product and the score facts themselves (P1 rwb-source-data).
- The roles, the rights, the scope and the masking rules (P4 rwb-access), and the reconciliation of the RW-RISK right on the monitor read.
- The rights of the monitor read, the screen SCR-46 and its states (RWB-P10-E1063-APP).
- The deployment of this capability: chart values, queue and topic provisioning, dashboards and the runbook.
