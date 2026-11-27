# RWB-P10-E8003-APP Run a champion and challenger test

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E8003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Readiness decisions | RD-P1-005, RD-P1-008, RD-P1-040, RD-P1-060 |
| Parallel lane | L-P10-J |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P10-E8003-APP-16) |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-060: Align the P1 entity route references and retain the separate score-read gap.
- The decision event type reads `rwb.decision.DecisionRecorded.v1`; the topic `rwb.decision-record.v1` is unchanged (RD-P1-008).
- The readiness pair of rwb-source-data is cited with its 202 answer and `RUNNING` / `DONE` / `LATE` status (RD-P1-005, RD-P1-040).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-003 for rwb-agent. The legacy story carries no endpoint and no screen ("the work runs as a service or a scheduled job inside the recovery module"); this story reworks the comparison as the champion and challenger step of the evaluation harness that rwb-agent already owns, extends the three existing evaluation operations with the two version labels, stores the per-version score rows in `agent_evaluation` and the winner on `agent_evaluation_run.proposal`, reads the ACE score facts through the rwb-source-data contract, writes the local decision record naming both versions, and leaves the comparison read to SCR-46 through the gateway-bff composite route. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E8003-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 9 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **centre of excellence analyst (RW-COE)**, I want **to run two policy or model versions of one agent side by side on the same labeled sample, to read each version's score, the comparison of the two and the version that won, and to have the result written to the decision log with both version labels**, so that **a version is only ever proposed for an autonomy change on measured evidence a person can read and quote, and the comparison itself decides no case and moves nothing**.

### 2. Business rationale

Legacy RWB-E8-003 carries FEAT-AGT-14 (admin, priority Should, depends on FEAT-AGT-05 the evaluation harness) in module P10 Agent runtime: the analyst runs two rule or model versions side by side and compares the outcome, and the result goes to the decision log with the rule version. The legacy story names no endpoint ("None. The work runs as a service or a scheduled job inside the recovery module") and no screen, and its data is `decision_log_entry` (DF-DEC-001 to DF-DEC-018), `v_ace_score` (DF-ACE-270 to DF-ACE-279) and `rule_row` (DF-REF-001 to DF-REF-015). Without a readable comparison an autonomy change would rest on an opinion, and the bank's AI risk position requires measured evidence and a human decision before an agent is trusted further.

The key has one slice in this realignment, so this story carries the whole of RWB-E8-003 and owns both of its legacy criteria. In the target rwb-agent already owns the evaluation harness of FEAT-AGT-05 through `POST /admin/agent-evaluations`, `GET /admin/agent-evaluations` and `GET /admin/agent-evaluations/{evaluationId}/report` (API-P10-005 to API-P10-008: the sample load and the three evaluation operations), and it owns the data that comparison needs in `rwb_agent` (DP-01): `agent_policy` with the versions compared (DF-AGT-001 to DF-AGT-025), `agent_sample` with the labeled rows (DF-AGT-061 to DF-AGT-069), `agent_evaluation_run` with its status and its `proposal` (DF-AGT-070 to DF-AGT-085), `agent_evaluation` with the score of one approach on one label key (DF-AGT-086 to DF-AGT-096) and `agent_run` with one call per version and subject (DF-AGT-036 to DF-AGT-060). The capability becomes a step of that harness rather than a second harness: the request names the champion and the challenger version label, the step runs both, the scores sit per version in `agent_evaluation`, and the winner and the decision sit on `agent_evaluation_run.proposal`.

Three cross-service parts are decoupled. The outcome facts behind the comparison are the ACE score rows in `v_ace_score`, and rwb-agent reads them through the rwb-source-data contract and never from the view or from any table of that schema (DP-05). The result is written by the local decision-record library and relayed on `rwb.decision-record.v1` to the central ledger in rwb-decision, in the same transaction as the proposal (DP-03). The comparison is read on SCR-46 Agent monitor through the gateway-bff composite route, so the browser never calls rwb-agent directly (DP-19).

What the story does not do is as important as what it does. A comparison is a test: it changes no case field, no task, no queue, no route state, no autonomy level and no policy version. The challenger is compared, never put in force, and the promotion of a winner is the separate legacy key RWB-E8-004 (RWB-P10-E8004-APP). The legacy `rule_row` read is dropped with reason: the route rows of a package are `rwb-decision`'s, a comparison names policy and model versions of an agent, and this story reads no rule row and holds no copy of a package.

### 3. Preconditions

- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). RWB-P7-E1027-CON publishes the central ledger behind it.
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-46 Agent monitor (DP-19). Its field list, its hop order and its merge rules are Not specified in the source documents (GAP-0645; ASM-1059).
- The evaluation harness of RWB-P10-E1058-APP and its contract RWB-P10-E1058-CON are in place: `POST /api/recovery/agent/v1/admin/agent-evaluations` with `AgentEvaluationRequest`, `GET /api/recovery/agent/v1/admin/agent-evaluations` with the JSON and CSV answers, and `GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report` with `AgentEvaluationReport`. This story extends those three operations and publishes no new path and no new schema.
- The `rwb_agent` schema baseline is applied: `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation`, `agent_feedback`, `agent_alert` and the outbox, inbox and idempotency objects exist.
- Agent "INTAKE" holds policy version "P1" with status "APPROVED" and policy version "P2" with status "LOADED", each row holding `model_code`, `model_version`, `timeout_seconds`, `confidence_floor` and `daily_cost_cap_thb` (DF-AGT-004, DF-AGT-005, DF-AGT-011, DF-AGT-012, DF-AGT-013).
- Sample "INTAKE-S1" version 1 holds 200 labeled rows for agent "INTAKE" in `agent_sample` (DF-AGT-061 to DF-AGT-069), each row with its `subject_type`, `subject_id`, `label_key` and `expected_value`.
- The comparison measure, the sample floor below which a comparison is not read and the decision threshold that names a winner are rows of the policy version: Not specified in the source documents (GAP-0645; ASM-1053).
- The rwb-source-data contract publishes the operation that returns the ACE score facts of a set of subjects from `v_ace_score`: Not specified in the source documents (GAP-0645; ASM-1054).
- The lists LOV-AGENT (INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER), LOV-EXTRACT-APPROACH (AGENT, OCR_TEMPLATE, MODEL, OCR_AND_MODEL), LOV-EVAL-STATUS (RUNNING, DONE, FAILED) and LOV-CONFIG-STATUS (LOADED, APPROVED, RETIRED) are loaded in the reference data of rwb-agent, and LOV-AGENT-RUN holds ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, TOOL_UNAVAILABLE, MODEL_ERROR and DISABLED.
- The two versions of a comparison are two `agent_policy` rows of the same `agent_code`; a run whose labels name another agent's version is refused before any call is made.

### 4. Flow

1. RW-COE starts a champion and challenger run from SCR-46 Agent monitor, or from a scripted call in a test; the request reaches rwb-agent through gateway-bff, one hop, and the browser calls no owner service directly (DP-19).
2. rwb-agent receives `POST /api/recovery/agent/v1/admin/agent-evaluations` with the agent code, the sample code and version, and the two version labels. The labels are a backward-compatible extension of `AgentEvaluationRequest`: the fields the legacy request carries are unchanged, and the request field names the pair is carried in are Not specified in the source documents (GAP-0645; ASM-1052).
3. ChallengerRequest validates the request: the agent code is in LOV-AGENT, the sample exists with at least one labeled row, both labels name an `agent_policy` row of that agent with a status in LOV-CONFIG-STATUS, and the two labels differ. A missing label is refused with 422 and MSG-GEN-001; nothing is written.
4. ChallengerRequest resolves each label to its policy row and reads that version's `timeout_seconds`, `confidence_floor`, `daily_cost_cap_thb`, `model_code` and `model_version`; no limit and no threshold is read from code.
5. The service writes one `agent_evaluation_run` row with status "RUNNING", `agent_code`, `sample_code`, `sample_version`, `requested_by`, and the champion in `policy_version` and `model_version`; the pair, the measure and the state of the comparison sit in `proposal` (DF-AGT-084), so the legacy reader of the run keeps working.
6. VersionPairRunner runs the champion and then the challenger over the same labeled rows: one `agent_run` row per version and subject, with `trigger_event` "EVALUATION", the `autonomy_mode` of the version, the `idempotency_key` built from the run, the version label and the subject, and the latency, tokens, cost and status of LOV-AGENT-RUN.
7. Each call is ended at `timeout_seconds` of its version, 60 seconds for the versions in force: R-UNI-32 fixes the window, and a comparison run records the timeout as a failure instead of substituting a result, because a test decides no case.
8. OutcomeComparator reads the outcome facts of the sample's subjects through the rwb-source-data contract (DP-05) — `score_key`, `account_key`, `model_code`, `model_version`, `score_value`, `estimate_value` of `v_ace_score` (DF-ACE-270 to DF-ACE-279) — and joins them to the labeled rows on the subject; it never reads `v_ace_score` and never reads a table of `rwb_source_data`.
9. OutcomeComparator scores each version against the labels and writes one `agent_evaluation` row per version and label key: `approach` from LOV-EXTRACT-APPROACH, `label_key`, `sample_size`, `true_positive`, `false_positive`, `false_negative`, `agreement_rate`, `precision_value` and `recall_value`. `agent_evaluation` carries no column that names the version of a score row, so the version of each row is named on the run's `proposal`, and the exact field names are Not specified in the source documents (GAP-0645; ASM-1057).
10. The comparator compares the two versions on the measure read from the policy rows and names the winner, or records that neither version wins on the measure; the measure, the sample floor and the decision threshold are rows and are Not specified in the source documents (GAP-0645; ASM-1053).
11. ComparisonWriter writes the comparison into `proposal` — both version labels, each version's value for the measure, the winner and the decision — and closes the run with status "DONE", `finished_at`, `total_cost_thb`, `p95_latency_ms` and `failure_counts`.
12. DecisionRecordWriter writes the local decision record with both version labels, the sample, the measure and the winner in the same `rwb_agent` transaction as the proposal (DP-03); the outbox relays DecisionRecorded on `rwb.decision-record.v1` and the central ledger in rwb-decision collects it. A failed record write rolls the whole transaction back: the run stays "RUNNING", no proposal and no score row of the pair is stored, and the caller sees MSG-P7-003.
13. A version that does not answer inside its timeout, a subject with no score fact, or a label that resolves to no row on the policy version ends the run with status "FAILED" and its cause in `failure_counts`; no winner is written to `proposal` and the failure is recorded on the decision record.
14. RW-COE reads the comparison with `GET /admin/agent-evaluations` in JSON for the screen and with `Accept: text/csv` for the export, and reads one run's report with `GET /admin/agent-evaluations/{evaluationId}/report`; the screen answer of SCR-46 is composed by gateway-bff from that read, one hop, and the browser calls nothing else (DP-19).
15. Nothing of the run reaches a case: no `recovery_case` field, no task, no queue, no route state, no autonomy level and no policy version changes. The winner of a comparison is evidence for the separate promotion story (legacy RWB-E8-004, RWB-P10-E8004-APP).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The request names no champion or no challenger version | 422; the run is not started and no run, score or decision row exists | MSG-GEN-001 | AC9 |
| X2 | The two labels name the same policy version | 422; a comparison needs two versions and nothing is written | MSG-GEN-001 | AC9 |
| X3 | The sample of the pair has no labeled row | The run is not started; the empty-sample refusal of the harness stays with RWB-P10-E1058-APP and is answered there | None | AC3 |
| X4 | The same request arrives twice with the same Idempotency-Key | The first run and its comparison return; no second run, no second score row and no second decision record | None | AC11 |
| X5 | A version's model does not answer inside its `timeout_seconds` | The call is ended at the timeout, the `agent_run` rows of that version hold status "TIMED_OUT" and fallback true, and the run ends "FAILED" with the failure in its counts | None | AC8 |
| X6 | A subject of the sample has no score fact in the rwb-source-data answer | The subject is counted as not scored and named in the failure counts; the run scores the subjects it has | None | AC6 |
| X7 | The rwb-source-data operation does not answer | One hop, 2 s timeout; the step retries and the run stays "RUNNING"; no score row is written from a partial answer | None | AC6 |
| X8 | The local decision record cannot be written | The transaction rolls back: the proposal, the score rows and the status change are not stored and the caller sees MSG-P7-003 | MSG-P7-003 | AC2 |
| X9 | A role without the Rules and parameters right calls a run or a read | Refused with 403 before any validation; nothing is read and nothing is written | MSG-P4-002 | AC13, AC15 |
| X10 | The comparison is read straight from rwb-agent by a browser | The route does not exist for the browser: SCR-46 reads the gateway-bff composite route only | None | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1: the story extends three operations it already has, builds against the P1 contract fake, the P7 decision contract and the gateway-bff route stub, and its only build dependencies are two platform contract stories |
| Negotiable | The versions, the measure, the sample floor, the threshold, the timeout and the cost cap are rows; the story fixes the behaviour of the comparison, not its values |
| Valuable | An autonomy change is proposed on a comparison a person can read, with both versions and the winner in the decision log |
| Estimable | One extension of the request, one step, one comparator, one writer, one decision-record write, one export and one report |
| Small | Fits one sprint with its tests: it adds no table, no endpoint path and no workflow template |
| Testable | Every criterion of section 7 is one automated test; the two cross-service answers are stubbed in their contract fakes and the comparison is asserted row by row in `agent_evaluation` and `agent_evaluation_run.proposal` |

### 7. Acceptance criteria

```gherkin
Feature: Run a champion and challenger test

  Background:
    Given agent "INTAKE" holds policy version "P1" with status "APPROVED" and policy version "P2" with status "LOADED"
    Given sample "INTAKE-S1" version 1 holds 200 labeled rows for agent "INTAKE"
    Given the policy row of each version holds timeout_seconds, confidence_floor and daily_cost_cap_thb

  Scenario: AC1 Run a champion and challenger test (legacy RWB-E8-003 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then runs two rule or model versions side by side and compares the outcome
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-003 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Two versions of one agent run side by side on one sample (new, D-RCV-60)
    Given RW-COE posts a run for agent "INTAKE" on sample "INTAKE-S1" version 1 with champion "P1" and challenger "P2"
    When the champion and challenger step runs
    Then one agent_evaluation_run row exists for the pair with status "RUNNING" and requested_by the caller
    Then both versions run over the same 200 labeled rows and one agent_run row exists per version and subject with trigger_event "EVALUATION"
    Then the run closes with status "DONE", finished_at, total_cost_thb, p95_latency_ms and failure_counts
    Then agent_evaluation holds one score row per version and label_key, each with sample_size 200, true_positive, false_positive, false_negative, agreement_rate, precision_value and recall_value
    Then no case field, task, queue, route state, autonomy level or policy version changes

  Scenario: AC4 The winner and the decision sit on the run's proposal (new, D-RCV-60)
    Given the run of AC3 closed with status "DONE"
    When the run is read
    Then agent_evaluation_run.proposal names the champion "P1", the challenger "P2", the comparison measure, each version's value for it and the winner
    Then the winner is the version the measure and the threshold of the policy rows name, and the run names no autonomy change and no policy version change
    Then GET /admin/agent-evaluations returns the same pair and the same winner for the run

  Scenario: AC5 The decision record names both versions (new, D-RCV-60)
    Given the run of AC3 closed with status "DONE"
    When the result is recorded
    Then one local decision record exists for the run naming the agent, the champion "P1", the challenger "P2", sample "INTAKE-S1" version 1, the measure and the winner
    Then the record and the proposal commit in one rwb_agent transaction
    Then rwb.decision.DecisionRecorded.v1 is written to the outbox and relayed on rwb.decision-record.v1 with the record reference, the agent code, both version labels and the evaluation run ID
    Then the payload carries no case ID and no personal data

  Scenario: AC6 The outcome facts come from the rwb-source-data contract (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the score facts of the sample's subjects
    When OutcomeComparator scores the two versions
    Then each version's agreement, precision and recall come from the answer of the rwb-source-data operation and from no table
    Then no statement of rwb-agent names the ACE view or any rwb_source_data table
    Then a subject with no score fact is counted as not scored and named in failure_counts
    Then GET /admin/agent-evaluations/{evaluationId}/report lists the count of not-scored subjects

  Scenario: AC7 The comparison is read on SCR-46 through one composite route (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-46 Agent monitor
    Given run "EV-INTAKE-001" closed with champion "P1", challenger "P2" and a winner
    When RW-COE opens SCR-46 for the run
    Then the comparison panel shows the agent, the sample, the champion, the challenger, each version's score and the winner
    Then the browser calls one composite route and no rwb-agent operation directly
    Then no route of the service is reachable from the browser outside the gateway

  Scenario: AC8 A version that does not answer inside its timeout fails the run (new, D-RCV-60)
    Given the model stub of policy version "P2" does not answer for 61 seconds
    Given the policy row of "P2" holds timeout_seconds 60
    When the champion and challenger step runs for "P1" against "P2"
    Then the calls of "P2" are ended at 60 seconds and their agent_run rows hold status "TIMED_OUT" and fallback true
    Then the run closes with status "FAILED" and failure_counts holds TIMED_OUT for "P2"
    Then no winner is written to proposal
    Then the score rows of "P1" are kept and the report names the run as failed

  Scenario: AC9 A run with no challenger version is refused (new, D-RCV-60)
    Given the request names champion "P1" and no challenger version
    When RW-COE posts the run
    Then the request is refused with 422 and MSG-GEN-001 naming the challenger version field
    Then no agent_evaluation_run row, no agent_run row and no agent_evaluation row exist
    Then no decision record is written
    When the request names "P1" as both champion and challenger
    Then it is refused with 422 and nothing is written

  Scenario: AC10 The comparison exports as CSV (new, D-RCV-60)
    Given two runs closed with status "DONE"
    When RW-COE reads GET /admin/agent-evaluations with Accept text/csv
    Then the answer holds one line per version pair with the run ID, the agent, the sample, the champion, the challenger, each version's value for the measure and the winner
    Then the response is a CSV file and the JSON answer of the same query holds the same pairs
    Then no line carries a case ID or a personal field

  Scenario: AC11 A repeated request with the same key acts once (new, D-RCV-60)
    Given the run of AC3 was started with Idempotency-Key "INTAKE:INTAKE-S1:1:P1:P2"
    When the same request arrives again with the same key
    Then no second agent_evaluation_run row and no second set of score rows exist
    Then the first run and its comparison are returned and the idempotency hit is counted
    Then one comparison exists for the sample and version pair

  Scenario: AC12 SCR-46 shows its empty, loading, error and no-access states (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-46 Agent monitor with no run for agent "INTAKE"
    When RW-COE opens SCR-46 for the agent
    Then the comparison panel shows an empty state and no winner
    Then the panel shows a loading state until the composite route answers
    Then the panel shows an error state with its message Not specified in the source documents (DOR-RWB-P10-E8003-APP-10) when the composite route does not answer
    Then a role without the Rules and parameters right sees the access refusal MSG-P4-002 and no comparison

  Scenario: AC13 A role without the Rules and parameters right is refused before validation (new, D-RCV-60)
    Given the rwb-access stub refuses the Rules and parameters right for the caller
    When the caller posts a run
    Then the request is refused with 403 and MSG-P4-002 before any validation
    Then nothing is read and nothing is written

  Scenario: AC14 Each version's call uses the limits of its own policy row (new, D-RCV-60)
    Given the labels "P1" and "P2" name two agent_policy rows of agent "INTAKE"
    When the champion and challenger step runs
    Then the calls of "P1" use the timeout_seconds, confidence_floor and daily_cost_cap_thb of "P1"
    Then the calls of "P2" use the timeout_seconds, confidence_floor and daily_cost_cap_thb of "P2"
    Then no call of one version uses the limits of the other

  Scenario: AC15 A role without the Rules and parameters right is refused on the comparison read (new, D-RCV-60)
    Given the rwb-access stub refuses the Rules and parameters right for the caller
    When the caller reads GET /admin/agent-evaluations
    Then the request is refused with 403 and MSG-P4-002 before any read
    Then nothing is read

  Scenario: AC16 The two labels name policy rows of one agent (new, D-RCV-60)
    Given the label "P2" names an agent_policy row of an agent other than "INTAKE"
    When RW-COE posts a run for agent "INTAKE" with champion "P1" and challenger "P2"
    Then the request is refused with 422 and nothing is written

  Scenario: AC17 Error answers 401 and 404 of the provided operations (new, D-RCV-60)
    Given the caller sends no credential
    When the caller reads GET /admin/agent-evaluations
    Then the answer is 401 and no comparison is returned
    Given the evaluationId names no stored run
    When the caller reads GET /admin/agent-evaluations/{evaluationId}/report
    Then the answer is 404 with the message Not specified in the source documents (NEWAC-RWB-P10-E8003-APP-AC14)
```

AC1 and AC2 are the two criteria of legacy RWB-E8-003, copied word for word with their origin tags: the key has one slice in this realignment, so the whole legacy deliverable sits here and no second story owns a part of it. AC3 to AC17 are new for the rwb-agent slice and test only what this story delivers: the pair of versions on one sample through the evaluation operations (AC3), the winner on `proposal` (AC4), the decision record naming both versions (AC5), the outcome facts read through the P1 contract and never from a table (AC6), the comparison read on SCR-46 through the gateway-bff route only (AC7), the states of the run (AC8), the request itself (AC9), the export (AC10), the repeat (AC11), the SCR-46 states (AC12), the access refusal of a run (AC13) and of a read (AC15), each version's own policy limits (AC14), the two labels of one agent (AC16) and the 401 and 404 answers (AC17). The legacy wording of AC1 says "the user acts on the screen" while the legacy story also says it has no screen; the screen that shows the result is SCR-46 Agent monitor, which this story reads through the gateway and does not change (section 15).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | After 60 seconds the rule result is used and the fallback is recorded on the decision; a comparison run makes no case decision, so the same 60-second budget (`timeout_seconds` of the version) ends the call and a version that does not answer inside it is scored as a failure, never replaced by a result | R-UNI-32; NFR-010; DF-AGT-012 |
| BR2 | A decision that cannot be recorded does not proceed: the decision record, the proposal, the score rows and the status change are one transaction, and a failed record write leaves nothing behind | Principle 5; R-UNI-39; DP-03 |
| BR3 | No value a business person may change is written in code: the compared versions, the comparison measure, the sample floor, the decision threshold, the timeout, the confidence floor and the daily cost cap are rows with a version | BR-P10-014; DF-AGT-011 to DF-AGT-013 |
| BR4 | rwb-agent reads no table of another service and no ACE view: the score facts of `v_ace_score` arrive through the rwb-source-data contract, and no statement of this service names the view or the schema | DP-01; DP-05; ADR-010 |
| BR5 | One comparison exists per sample and version pair: a repeat with the same Idempotency-Key returns the first run and counts the hit, and a second run of the same pair while one is open is refused by the harness | R-UNI-40; DP-09 |
| BR6 | The challenger never runs in force: both versions run in the comparison only, and no autonomy level and no policy version changes on this path — a promotion is the separate legacy key RWB-E8-004 with the approval of RW-RISK | FEAT-AGT-14; FEAT-AGT-15; RWB-E8-004 |
| BR7 | A score row holds the result of one approach on one label key of one version, with `approach` from LOV-EXTRACT-APPROACH and its counts, agreement, precision and recall; the version of the row is named on the run's `proposal` because `agent_evaluation` has no version column | DF-AGT-086 to DF-AGT-096; LOV-EXTRACT-APPROACH |
| BR8 | The run's status is a value of LOV-EVAL-STATUS: RUNNING while the versions run, DONE when both are scored, FAILED when a version does not answer or a subject is not scored; a run that ends FAILED writes no winner | LOV-EVAL-STATUS; DF-AGT-077 |
| BR9 | A comparison decides nothing: no case field, task, queue, route state, autonomy level or policy version moves, and the result is evidence for a person, not a decision on a case | FEAT-AGT-14; legacy RWB-E8-003 intent |
| BR10 | The two compared labels name two `agent_policy` rows of the same agent, and each call uses the timeout, the confidence floor and the daily cost cap of its own version | DF-AGT-002, DF-AGT-003, DF-AGT-011 to DF-AGT-013 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| none | A run is requested for one sample and a version pair | the request passes validation and the record is written in the same transaction | RUNNING |
| RUNNING | Both versions scored over the sample | every compared label has a value and the record is written | DONE |
| RUNNING | A version does not answer inside its timeout, or a subject is not scored | `failure_counts` names the cause | FAILED |
| RUNNING | A required label is missing or the same version is named twice | nothing is written and the request is refused | none |

These are the states of the champion and challenger run (`agent_evaluation_run.status`, DF-AGT-077, values of LOV-EVAL-STATUS) and of the comparison stored on the run's `proposal` (DF-AGT-084). This story moves no case status, no route state and no autonomy level: the legacy key has no case state machine of its own (TSD P10 T4), and a promotion of the winning version is a separate story (legacy RWB-E8-004, RWB-P10-E8004-APP). A run in DONE or FAILED is never reopened: a rerun is a new run with its own ID and its own decision record.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, centre of excellence analyst | Primary: starts a champion and challenger run on a sample and a version pair, and reads the comparison, the report and the CSV export (Rules and parameters C and R) |
| RW-RISK, risk and model risk officer | Approver and reader: reads the comparison and the report, and approves a promotion in the separate story RWB-P10-E8004-APP; approves no run here |
| RW-PLATADM, platform administrator | Reads the runs and works a run that ended FAILED (Platform administration CRUD per TSD P10 T6.1) |
| RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read the runs and the comparison; the legacy permission table grants them Platform administration R, and the evaluation operations declare Rules and parameters R |
| RW-SECADM, security administrator | Reads the runs and the rights that guard them; changes no run (Platform administration CRUDA per TSD P10 T6.1) |
| rwb-agent service identity (the rwb-agent login, DP-02) | Runs the two versions, writes the run, the agent runs, the score rows and the proposal, and reads the score facts through the P1 contract |
| Decision-record library identity | Writes the local decision record with both version labels and its outbox row (Decision log C) |
| Model gateway (INT-23, through the private endpoint of the SCB tenant) | Serves each version's model call; it decides nothing and holds no run state |

The legacy permission table grants Platform administration R to RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM, while appendix T-A of the TSD declares Rules and parameters C on `POST /admin/agent-evaluations` and R on the two reads. Under the source precedence the TSD wins, so the operations are guarded by Rules and parameters and the six roles stay as the readers and the starter of a run; the difference is recorded in the gap row of section 18. No role in this story may change an autonomy level, a policy version or a case by starting a comparison.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-070 to DF-AGT-085 | agent_evaluation_run | id, agent_code, sample_code, sample_version, policy_version, prompt_version, model_version, status, started_at, finished_at, requested_by, total_cost_thb, p95_latency_ms, failure_counts, proposal, review_count | Write, and read for the comparison |
| DF-AGT-084 | agent_evaluation_run | proposal: the champion and the challenger label, each version's value for the measure, the winner and the decision | Write |
| DF-AGT-086 to DF-AGT-096 | agent_evaluation | id, evaluation_run_id, approach, label_key, sample_size, true_positive, false_positive, false_negative, agreement_rate, precision_value, recall_value | Write |
| DF-AGT-036 to DF-AGT-060 | agent_run | id, agent_code, agent_version, prompt_version, model_version, subject_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, confidence, latency_ms, tokens_in, tokens_out, cost_thb, data_as_of, run_at, evaluation_run_id | Write |
| DF-AGT-001 to DF-AGT-025 | agent_policy | id, agent_code, policy_version, model_code, model_version, autonomy_mode, confidence_floor, timeout_seconds, daily_cost_cap_thb, evaluation_run_id, status, valid_from, valid_to | Read |
| DF-AGT-061 to DF-AGT-069 | agent_sample | id, agent_code, sample_code, sample_version, subject_type, subject_id, label_key, expected_value, labeled_by | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision, owner P7) | all fields | Write locally; the central entry is sealed by rwb-decision |
| DF-ACE-270 to DF-ACE-279 | v_ace_score, through the rwb-source-data contract | score_key, account_key, model_code, model_version, score_value, estimate_value and the rest of the row | Read, through the P1 contract only |

The legacy story names three data sets and each one is settled here. `decision_log_entry` with DF-DEC-001 to DF-DEC-018 still applies: the record is written by the local library in `rwb_agent` and sealed by rwb-decision, and this story never writes the central table. `v_ace_score` with DF-ACE-270 to DF-ACE-279 still applies: the score facts are the outcome the two versions are compared on, and they are read through the rwb-source-data contract and never from the view (DP-05). `rule_row` with DF-REF-001 to DF-REF-015 is no longer read by this slice: a route row of a package is `rwb-decision`'s (P7) and this comparison names policy and model versions of an agent, so the rule-row read and its field IDs are dropped from the story. The legacy key names no DF-WRK field and no assignment row: the assignment table is `rwb-case`'s (P3) and nothing here places work in a queue. Field IDs are those in the Logical Data Model and Data Dictionary v9, and no foreign key crosses a schema (DP-01).

Reference data that this story reads: the lists LOV-EVAL-STATUS and LOV-EXTRACT-APPROACH, and the parameters of the agent_policy row, namely timeout_seconds, confidence_floor, daily_cost_cap_thb and policy_version. They are read under the reference-data pattern DP-06 and DP-07; the reference-data contract name is Not specified in the source documents (DOR-RWB-P10-E8003-APP-20).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10). All three operations exist in the evaluation harness of RWB-P10-E1058-APP; this story extends them backward compatibly and publishes no new path.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/admin/agent-evaluations` | Starts an evaluation of one agent on one labeled sample; the request carries the champion and the challenger version label as an optional extension of `AgentEvaluationRequest`, and a request without them keeps the single-version behaviour of the harness | Rules and parameters C, scope applied | Idempotency-Key header |
| GET | `/admin/agent-evaluations` | Lists evaluation runs with their score rows and, for a champion and challenger run, the pair and the winner of `proposal`; the same answer as CSV when `Accept: text/csv` | Rules and parameters R, scope applied | Not applicable: the call writes nothing |
| GET | `/admin/agent-evaluations/{evaluationId}/report` | Reads one run's report: sample size, per-version scores, failure counts, cost, latency, the comparison and the winner | Rules and parameters R, scope applied | Not applicable |

Errors: 401 no session (MSG-P4-001), 403 no Rules and parameters right (MSG-P4-002), 404 unknown evaluation run (message Not specified in the source documents (CG-ALL-2868)), 409 the pair is already running (MSG-P10-003), 422 a required label missing (MSG-GEN-001) or a label that resolves to no policy row of the agent (message Not specified in the source documents (CG-ALL-2868)), 503 store down (message Not specified in the source documents (CG-ALL-2868)). The request and response field names of the two version labels and of the comparison on `proposal` are Not specified in the source documents (GAP-0645; ASM-1052).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-0645; ASM-1054) | rwb-source-data (P1) | The score facts of the sample's subjects from `v_ace_score` (DF-ACE-270 to DF-ACE-279), the outcome the two versions are compared on | One hop; 2 s timeout |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Rules and parameters right and the scope before a run, a read and the export, cached by the guard library | One hop; 2 s timeout |

The P1 score read is the only cross-service read. Its route, request and paging remain Pending with the P1 contract owner (GAP-0645, ASM-1054). The P1 5.1.0 entity routes under RD-P1-060 provide customer, account and collateral facts. Score facts do not appear in those answers. Use the score fake pending the P1 score contract.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 owns the type and the central ledger; rwb-agent writes its own record | evaluation run ID | decision record reference, agent code, champion version label, challenger version label, sample code and version, the measure, the winner (or the failure), business date |

The event is written to the outbox in the same transaction as the proposal and relayed with the CloudEvents envelope; no personal data and no case ID is carried (DP-09). The type is written through the local decision-record library of RWB-PLT-E1027-CON (DP-03).

#### 12.4 Events consumed

None. A champion and challenger run is started by a person, never by an event, and no event of the agent runtime starts or changes a comparison.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| ChampionChallengerStep | Step of the existing evaluation run of rwb-agent, started by `POST /admin/agent-evaluations` (RWB-P10-E1058-APP) | `rwb-agent` | Runs the champion and the challenger over one sample, scores both, compares them and writes the proposal |
| VersionPairRunner | Activity | `rwb-agent` | Calls each version for each labeled subject with that version's timeout and the model gateway, and writes one `agent_run` row per version and subject |
| OutcomeComparator | Activity | `rwb-agent` | Reads the score facts through the P1 contract, scores each version and writes one `agent_evaluation` row per version and label key |
| ComparisonWriter | Activity | `rwb-agent` | Writes the pair, the values, the winner and the decision into `proposal` and closes the run; part of the same transaction as the decision record |

This story adds no workflow template and no Queue of its own: the comparison is a step inside the evaluation run that rwb-agent already has, and the name of that run is not given by any source document, so the step is named here and the run is referred to as the evaluation run (GAP-0645; ASM-1058).

#### 12.6 Schedules

None new. The legacy story says the work "runs as a service or a scheduled job inside the recovery module", but the feature is admin work started by RW-COE (FSD P10 A2.14 step 1), so a comparison is never run on a cadence and no Schedule, no job and no timer is created by this story. The measurement jobs of the agent monitor (the daily cost and drift checks) stay with their own stories.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_evaluation_run | P10 (rwb_agent) | The run of the pair, its status, its costs, its failure counts and its `proposal` with the winner |
| agent_evaluation | P10 (rwb_agent) | One score row per version and label key |
| agent_run | P10 (rwb_agent) | One call per version and subject, with its status and its cost |
| agent_policy | P10 (rwb_agent) | Read only: the two versions, their labels and their limits |
| agent_sample | P10 (rwb_agent) | Read only: the labeled rows of the sample |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | Outbox, inbox and idempotency objects (DP-09) |

rwb-agent reads no table of another service and holds no foreign key across services (DP-01). `decision_log_entry`, `rule_row` and `rule_package_version` are rwb-decision tables and are written or read only through its contract.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 score-fact contract read of DP-05 (this key has no P1 CON story of its own, so the read is faked against the published P1 contract) | Score facts for the 200 subjects of sample "INTAKE-S1" version 1; an answer with 6 subjects missing; a delay beyond 2 s; an unavailable answer |
| rwb-decision decision-record stub | The P7 side of the local decision-record library (DP-03) | Acceptance of a record with both version labels; the unavailable store of AC2; the `RulePackageInForce` answer is not called by this story |
| gateway-bff composite route (WireMock) | The DP-19 route of SCR-46 Agent monitor | The merged comparison panel of AC7 and the failed-run answer of AC8 |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Rules and parameters C and R, and refusing both for a role without the right |
| Model gateway stub (INT-23) | The private model endpoint per version | Answers for "P1" and for "P2"; the 61-second silence of AC8 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | The extended run request, the list with the comparison and the report provided; the P1 score-fact read and the P4 authorise consumed; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` published through the local library; nothing consumed |
| Temporal | 1 step, 0 workflows | ChampionChallengerStep inside the existing evaluation run, with VersionPairRunner, OutcomeComparator and ComparisonWriter as activities |
| File | None | The CSV answer is a response body, not a file; this story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent`, module `challenger`, Java package `th.co.scb.ace.workbench.recovery.agent.challenger`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The two H dependencies of the table are exactly the two rows of the metadata table, because both are platform contract stories: RWB-PLT-E1027-CON for the record and RWB-PLT-N001-CON for the route. DP-05 resolves to the rwb-source-data contract and to no ACE view of its own: the score facts are read, never copied, and `rwb_agent` holds no grant on `v_ace_score`. DP-19 resolves to the route of SCR-46, which this story consumes and does not build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ChallengerRequest | Controller extension | Validates the pair on `POST /admin/agent-evaluations`: agent code in LOV-AGENT, both labels present and different, each label a policy row of the agent with a status in LOV-CONFIG-STATUS; refuses with 422 and MSG-GEN-001; resolves each label to its limits |
| VersionPairRunner | Activity | Runs each version over the same labeled rows, one `agent_run` row per version and subject, with that version's `timeout_seconds`, the model gateway and the idempotency key of the run |
| OutcomeComparator | Activity | Reads the score facts through the P1 contract, joins them to the labels on the subject, scores each version on the measure and writes one `agent_evaluation` row per version and label key |
| ComparisonWriter | Activity | Writes the pair, each version's value, the winner and the decision into `agent_evaluation_run.proposal` and closes the run with its costs, latency and failure counts |
| DecisionRecordWriter | Library adapter | Writes the local decision record with both version labels and the evaluation run ID, in the same transaction as the proposal (DP-03) |
| EvaluationQueryController | Controller extension | Serves the comparison on `GET /admin/agent-evaluations` in JSON and CSV and on the report operation, with the access check and the scope |

**Database and migrations**

- No table and no column is added. The champion and the challenger label, each version's value, the winner and the decision live in `agent_evaluation_run.proposal` (DF-AGT-084, jsonb); the score of one approach on one label key lives in `agent_evaluation` (DF-AGT-086 to DF-AGT-096); the call of one version on one subject lives in `agent_run` (DF-AGT-036 to DF-AGT-060).
- One index supports the run and the pair: `ix_agent_evaluation_run_pair ON agent_evaluation_run (agent_code, sample_code, sample_version)`, so the pair of a sample is read without a scan and the harness can refuse a second open run of the same pair.
- The migration runs in the rwb-agent Flyway sequence of `rwb_agent` alone. Its file number is `V<number>__champion_challenger.sql`, and the number is Not specified in the source documents (GAP-0645; ASM-1056).

**Configuration and reference data**

- LOV-AGENT, LOV-EXTRACT-APPROACH, LOV-EVAL-STATUS, LOV-CONFIG-STATUS and LOV-AGENT-RUN, owner RW-COE, read through the service's reference data.
- The compared versions with their `timeout_seconds`, `confidence_floor` and `daily_cost_cap_thb` (RW-COE loads a policy version, RW-RISK approves it, per the harness stories).
- The comparison measure, the sample floor and the decision threshold as rows of the policy version: Not specified in the source documents (GAP-0645; ASM-1053).
- The score-fact read of the P1 contract: Not specified in the source documents (GAP-0645; ASM-1054).
- The challenger runs in the comparison only: no run puts a version in force, and no run changes an autonomy level (ASM-1055).
- No feature switch: the legacy story names none, and the run is started by RW-COE.

**Build steps**

1. ChallengerRequest over the existing request of `POST /admin/agent-evaluations`, with the pair validated against `agent_policy` and the refusal paths; tests for AC9.
2. VersionPairRunner against the model gateway stub, with the per-version timeout, one `agent_run` row per version and subject and the idempotency key; tests for AC3 and AC8.
3. OutcomeComparator with the P1 contract fake and the label join, and the score rows per version and label key; tests for AC6 and the row shape of AC3.
4. ComparisonWriter and DecisionRecordWriter in one transaction, with the rollback when the record cannot be written; tests for AC2, AC4 and AC5.
5. EvaluationQueryController for the JSON, the CSV and the report answers, with the access check and the scope; tests for AC7, AC10 and the refused role.
6. The idempotent repeat of the run request; test for AC11.
7. Contract-fake run of every cross-service answer in isolation, so the story builds before the P1 read and the SCR-46 route are live.
8. A run over sample "INTAKE-S1" version 1 in SIT to confirm that the run changes no case, no autonomy level and no policy version, and that the decision record of every run names both versions.

**Done when.** The tests in section 16 pass, the contract tests of the P1 read, the decision-record library and the gateway-bff route stay green, every champion and challenger run in SIT holds one score row per version and label key and one winner on its proposal, and no case, no autonomy level and no policy version has moved because of a comparison.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the run request is empty | Enter {field}. |
| MSG-P10-003 | The run is started while the same evaluation is running (409) | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-001 | No session (401) | Not specified in the source documents (DOR-RWB-P10-E8003-APP-9) |
| MSG-P4-002 | A role without the Rules and parameters right calls a run or a read | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The comparison cannot be written to the decision log | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

For MSG-GEN-001 in this story, {field} is "champion version" or "challenger version" and never a version value, so the message names no row and no agent. For MSG-P4-002, {action} is the name of the operation the caller tried. MSG-P7-003 is the wording of the legacy validation table and is raised unchanged when the decision record cannot be written (R-UNI-39). No other message is added by this story: the empty-sample and second-run refusals of the harness keep their own identifiers with RWB-P10-E1058-APP.

### 15. Screens and states

No screen in this story: the legacy story says so and this slice keeps that answer. The comparison is read on SCR-46 Agent monitor, states Shadow; live; paused, and the states empty, loading, error and no access, which the screen specification does not give and which are Not specified in the source documents (CG-ALL-2875); the panel shows the agent, the sample, the champion, the challenger, each version's score and the winner for one run. SCR-46 is owned by the agent monitor stories (RWB-P10-E1063-APP and RWB-P10-E2031-APP) and is not changed here: this story delivers the read it consumes.

SCR-46 is served by the gateway-bff composite route, which calls rwb-agent `GET /admin/agent-evaluations` and `GET /admin/agent-evaluations/{evaluationId}/report`, one hop each, and merges the answers into the screen model (DP-19). The comparison panel of SCR-46, its field list, its merge rules and its state mapping are Not specified in the source documents (GAP-0645; ASM-1059); the browser calls no owner service directly, and no CSP exception is added for rwb-agent.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-003-01 | AC1 | Component | Run a champion and challenger test |
| TC-E8-003-02 | AC2 | Component | Not recorded |
| TC-E8-003-03 | Access, AC13 | Component | A role without the right is refused with MSG-P4-002 |
| TC-E8-003-04 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-E8-003-05 | AC3, AC11, BR5, BR7 | Component | Agent "INTAKE", sample "INTAKE-S1" version 1, champion "P1" and challenger "P2" |
| TC-E8-003-06 | AC4, BR6, BR7 | Component | The proposal of the pair with the measure, both values and the winner |
| TC-E8-003-07 | AC5, BR2 | Component | Decision record naming both version labels and the run |
| TC-E8-003-08 | AC6, BR4 | Component | P1 stub with 200 score facts, 6 of them missing; the view is never queried |
| TC-E8-003-09 | AC7, BR9 | Component | gateway-bff route stub serving the comparison of run "EV-INTAKE-001" |
| TC-E8-003-10 | AC8, BR1, BR8 | Component | Model stub of "P2" silent for 61 seconds; `timeout_seconds` 60 |
| TC-E8-003-11 | AC9, BR3 | Component | No challenger label, and "P1" named twice |
| TC-E8-003-12 | AC10 | Component | Two runs in DONE; `Accept: text/csv` |
| TC-E8-003-13 | AC12 | Component | gateway-bff route stub with no run for "INTAKE" and with no answer; a role without the right |
| TC-E8-003-14 | Contract (section 12) | Contract | Each operation, event and activity of section 12 against its published contract and Temporal Catalog v1 |
| TC-E8-003-15 | Boundary (section 12.7, ASM-3438) | Component | Each table of section 12.7 written or read only by its owner; no foreign key across services |
| TC-E8-003-16 | AC14, BR10 | Component | Labels "P1" and "P2" of agent "INTAKE", each with its own timeout_seconds, confidence_floor and daily_cost_cap_thb |
| TC-E8-003-17 | AC15 | Component | A role without the Rules and parameters right reads GET /admin/agent-evaluations |
| TC-E8-003-18 | AC16, BR10 | Component | Label "P2" names an agent_policy row of another agent; champion "P1" of agent "INTAKE" |
| TC-E8-003-19 | AC17 | Component | No credential on GET /admin/agent-evaluations; unknown evaluationId on the report route |

The four legacy test cases keep their legacy identifiers and their data, TC-E8-003-03 gains the cover AC13, and their level maps System to Component, Access to Component and Principle 5 to NFR, because this story proves the comparison at component level and the cross-service answers are stubbed. TC-E8-003-05 to TC-E8-003-13 and TC-E8-003-16 to TC-E8-003-19 are new and cover the new criteria (AC13 is covered by TC-E8-003-03), and TC-E8-003-14 and TC-E8-003-15 are the contract and boundary tests of section 12. No `-ITG` copy exists for this key: it has one slice, and both of its legacy criteria are exercised here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the versions, the comparison measure, the sample floor, the decision threshold, the timeout, the confidence floor and the daily cost cap are rows with a version (BR-P10-014).
- No personal data in logs, tests, workflow history or prompts: a comparison carries agent codes, sample codes, version labels, subject IDs and scores, never a name, an address or an identity number; the sample rows carry synthetic subjects and the report carries no case ID.
- No read of another service's tables and no ACE view: the score facts come only through the rwb-source-data contract, and `rwb_agent` holds no foreign key and no grant into another schema (DP-01, DP-05).
- The decision record is written before the comparison is stored, in one transaction with it, so a comparison that cannot be recorded does not exist (R-UNI-39).
- A comparison is a test: it changes no case, no task, no queue, no route state, no autonomy level and no policy version, and the challenger never runs in force (BR6, BR9).
- Every outbound event is written to the outbox in the same transaction as the proposal and carries IDs and facts only (DP-09).
- One comparison per sample and version pair: the idempotency key of the run and the index on the pair return the first run instead of a second one (R-UNI-40).
- The browser reaches the comparison only through the gateway-bff route; no owner operation is exposed to it (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None carried by the legacy story | Legacy RWB-E8-003 carries no requirement ID; the feature is FEAT-AGT-14 Run a champion and challenger test, and the Program BRD v4 holds no requirement row for it (GAP-0645) | None: the feature appears only in the Epic 3 to 8 feature table, row E8 P10 FEAT-AGT-14 | FEAT-AGT-14 | All recovery processes | R-UNI-32, R-UNI-39 | TC-E8-003-01, TC-E8-003-02, TC-E8-003-04, TC-E8-003-05 |
| D-RCV-60 DP-03 | The comparison is recorded in the local decision record naming both versions and relayed on `rwb.decision-record.v1` | Decision log, D-RCV-60; Template and Rules §R5.5 | FEAT-AGT-14 | All recovery processes | R-UNI-39 | TC-E8-003-02, TC-E8-003-04, TC-E8-003-07 |
| D-RCV-60 DP-05 | The outcome facts are read from `v_ace_score` through the rwb-source-data contract and never from a table | Decision log, D-RCV-60; Template and Rules §R5.5; Architecture v5 slide 15 | FEAT-AGT-14 | All recovery processes | DP-05 | TC-E8-003-08 |
| D-RCV-60 DP-19 | The comparison is read on SCR-46 through the gateway-bff composite route only | Decision log, D-RCV-60; Template and Rules §R5.5 | FEAT-AGT-14 | All recovery processes | BR9 | TC-E8-003-09 |

The legacy story carries no requirement identifier, so no requirement ID is invented here: the traceability of this slice runs on the feature FEAT-AGT-14 and on the three decoupling decisions. The missing BRD row and the missing feature-level requirement are recorded in the gap row of this story.

### 19. Out of scope

- Raising or lowering an autonomy level with approval and the approval of RW-RISK: legacy RWB-E8-004 (RWB-P10-E8004-APP).
- The evaluation harness itself, the sample load, the policy and prompt versions and the report structure: RWB-P10-E1058-APP, RWB-P10-E1060-APP and RWB-P10-E1061-APP.
- The agent runtime, the model gateway, the guardrails and the agent run with its 60-second fallback: RWB-P10-E1058-APP and RWB-P10-TE013-APP.
- The agent monitor screens and their states: RWB-P10-E1063-APP and RWB-P10-E2031-APP.
- The drift and cost alerts of the agent: RWB-P10-E3031-APP and the monitor stories.
- The rule packages, their route rows and the DMN model registry: rwb-decision, with its own stories.
- The central decision ledger behind `rwb.decision-record.v1`: rwb-decision (P7).
- The roles, the rights, the scope and the masking policy as data: rwb-access (P4).
- The ACE view behind the score facts and its read contract: rwb-source-data (P1).
- The deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook.
