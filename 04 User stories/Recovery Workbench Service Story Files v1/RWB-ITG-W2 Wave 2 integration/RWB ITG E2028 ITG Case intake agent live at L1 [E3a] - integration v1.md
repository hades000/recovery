# RWB-ITG-E2028-ITG Case intake agent live at L1 [E3a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2028-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP07, DP09, DP10, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1035-APP, RWB-P10-E2028-APP, RWB-P7-E2028-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-014, FR-PLT-015, FR-PLT-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-028 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a repeatable cross-service journey harness for the case intake agent at L1 — a `CaseCreated` event that starts a run on rwb-agent, the stored summary read through the P10 agent-output operation, the owner's verdict and its D6 decision record, the acceptance measure and the fallback — with the evidence pack attached to the wave 2 release**, so that **the intake-agent journey is proven end to end across rwb-agent, rwb-case, rwb-decision and rwb-access before RWB-P10-E2028-APP, RWB-P3-E1035-APP and RWB-P7-E2028-APP claim Done**.

This story builds the harness, its contract fakes, its seed pack, its evidence pack and its pass or fail gate. It builds no production endpoint, no screen, no table and no migration. Nothing it writes is deployed to a service.

No single app story can prove the journey. RWB-P3-E1035-APP can prove that a case is created and that `CaseCreated` leaves rwb-case. RWB-P10-E2028-APP can prove that a run is started, that the model is called through the Enterprise AI private endpoint, that the summary and gap flags are stored and that a verdict is accepted. RWB-P7-E2028-APP can prove that a decision record is written and that the ledger read returns it. The agreement between the four of them — one event starting one L1 run whose stored output, verdict, decision record and acceptance measure all describe the same case on the same business date — is this story, and only this story.

### 2. Business rationale

RWB-E2-028 split into three app stories and this integration story. The app stories build the agent runtime, the agent-output read, the feedback write, the decision-log mapping and the panel inside their own services. What no app story can prove on its own is the chain the business actually relies on: a new case raises `CaseCreated` on the case topic, rwb-agent consumes it under the policy in force for the segment, runs the model, stores a summary and the gap flags, publishes `AgentRunCompleted`, rwb-agent serves that stored output back to the case without waiting on the model, the case owner gives a verdict, rwb-decision holds one D6 entry that names the agent and prompt versions, and the acceptance and correction rates for the segment move by exactly that feedback. That proof is this story.

The journey carries two requirements. Every decision records the agent and prompt versions (REQ-DRI-001): the harness asserts that the decision record names version "INTAKE@P2/PR3" and that the D6 code is the one the feedback wrote, so a reader of the ledger can tell which model and which prompt produced the recommendation that was followed or overruled. Personal data stays masked by role on every screen and in every agent call (REQ-ACA-005): the harness asserts that the summary it reads back carries masking tokens and that neither the events, the workflow inputs, the logs nor the evidence pack carry a direct identifier.

The D6 decision is the anchor. Legacy section 12 gives the mapping: case, decision code "D6", agent version "INTAKE@P2/PR3", the model version, the run reference as the inputs reference, the recommendation, the final call from the verdict and the reason as the override reason. The harness exercises that mapping across rwb-agent and rwb-decision, so a change to the mapping on either side is caught before the owner sees a verdict that no ledger entry supports.

Architecture v5 changes the path, not the business. In the monolith the agent client, the feedback table, the scope check and the decision log all sat in one deployment and one schema. In the target:

- the local decision record and the shared topic `rwb.decision-record.v1` carry the entry, with rwb-decision holding the ledger (DP-03);
- the mode per segment, the verdict list and the panel labels are reference data served by rwb-case's contract, never values in code (DP-07);
- the events are CloudEvents on the owner's topic, with an outbox on the producer and an inbox on the consumer, so a duplicate never counts twice (DP-09);
- the run is an `AgentRunWorkflow` on queue `rwb-agent` with a 60 s limit and the rule result after it, which is the fallback of R-UNI-32 (DP-10);
- every path is on the owner's base `/api/recovery/<short>/v1` (DP-13);
- each service migrates its own schema through its own Flyway sequence (DP-15);
- the panel reaches the model through the gateway-bff composite route, so the harness drives the same route the screens use (DP-19).

The measure is the journey evidence: for each owned criterion, one pass or fail with the event, the run, the output, the verdict, the decision record, the measure and the fallback flag captured in one report that can be re-run for any build.

### 3. Preconditions

- The wave 2 harness environment (SIT) is available with the gateway route for `/api/recovery/*`, the topics `rwb.case.events.v1`, `rwb.agent.events.v1` and the shared topic `rwb.decision-record.v1`, the Temporal namespace `rwb-recovery` with the queues `rwb-agent` and `rwb-case`, and the Enterprise AI private endpoint test profile (INT-23). Not specified in the source documents (GAP-0410; ASM-0585): the harness environment, its seed pack and its evidence format.
- The three integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-P10-E2028-APP (rwb-agent, the agent-output read and the feedback write), RWB-P3-E1035-APP (rwb-case, the case record and `CaseCreated`) and RWB-P7-E2028-APP (rwb-decision, the D6 mapping and the ledger read).
- Policy "INTAKE" version "P2" with mode "L1" and prompt "PR3" is in force from 2027-01-25, and the policy fixture carries mode "SHADOW" for segment UNSECURED (legacy sections 3 and 7).
- Case "RW-2027-000501" is owned by "owner.user07", who holds RW-CASEOWN with Case record CRU and the case in that user's scope, and the case carries the gap flags MISSING_DOCUMENT and NO_VALID_APPRAISAL (legacy sections 3 and 7).
- January 2027 for segment MORTGAGE and region BKK holds 300 runs with feedback: 240 accepted, 45 corrected and 15 rejected, which is acceptance 0.8000 and correction 0.1500 (legacy AC2).
- The seeded states the scenarios name are present: case "RW-2027-000502" with a run that reached the 60 s limit, case "RW-2027-000503" whose run used data as of 2027-01-26 against business date 2027-01-28, case "RW-2027-000601" in team "HP-NE" outside the owner's scope, unsecured case "RW-2027-000701" with segment UNSECURED in SHADOW, and a test user of role RW-PHONECOL holding Case record R only.
- The feature switch `rwb.agent.intake-l1` is on in the harness profile (legacy section 13).
- Synthetic cases, synthetic owners and masking tokens only: no customer name, account number, national identifier or contact detail enters the harness, the seed pack or the evidence pack (legacy section 17).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date and the versions of the six contracts it is about to exercise.
2. Harness: seeds cases "RW-2027-000501", "RW-2027-000502", "RW-2027-000503", "RW-2027-000601" and "RW-2027-000701", owner "owner.user07", team "HP-NE", the segments and scopes, the RW-PHONECOL test user and the policy fixture (INTAKE P2, mode L1 per segment, SHADOW for UNSECURED, prompt PR3).
3. Harness: calls the P4 session operation against the rwb-access fake and records the role, the scope and the Case record right the journey runs under.
4. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` and records the owner, the team, the region, the product group and the two gap flags the journey starts from.
5. Harness: subscribes to `rwb.case.events.v1` and `rwb.agent.events.v1` with its own consumer group before the case is created, so the run window starts before the event.
6. Harness: publishes `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` for case "RW-2027-000501", or lets rwb-case create the case through its own operation where RWB-P3-E1035-APP has landed, and records which of the two paths was used.
7. Harness: waits for `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` inside the run window and records the run ID, the time to completion and the fallback flag.
8. Harness: reads the run through `GET /api/recovery/agent/v1/agent-runs` and records status, autonomy mode, agent code, agent version, data as of and the fallback flag.
9. Harness: calls `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` and asserts the summary, the two gap flags with reasons, agent "INTAKE", version "INTAKE@P2/PR3", the marker "Agent output" and the absence of feedback.
10. Harness: posts the feedback through `POST /api/recovery/agent/v1/agent-runs/{runId}/feedback` with an If-Match of the run row version, then reads `GET /api/recovery/decision/v1/decision-log` and asserts one D6 entry with agent version "INTAKE@P2/PR3" and the final call that matches the verdict, before the agent_feedback row is asserted.
11. Harness: reads `GET /api/recovery/agent/v1/admin/agent-metrics` and asserts acceptance 0.8000 and correction 0.1500 for INTAKE on MORTGAGE/BKK; asserts the SHADOW case returns an empty list with no decision record, the stale case carries MSG-P1-001 with 2027-01-26, the out-of-scope case answers 404 and the timed out case answers with no summary and fallback true.
12. Harness: writes the per-scenario evidence into one run report keyed by story key and business date, evaluates the gate, attaches the report to the wave 2 release record, releases the lock and restores the seed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent timed out or failed a guardrail for the case | The run holds status "TIMED_OUT" with fallback true and no summary is returned; the scenario passes only when both are true | MSG-P10-005 | AC4 |
| X2 | The owner corrects or rejects without a reason | The feedback answers 422; no decision record and no agent_feedback row is written | MSG-P7-005 | AC5 |
| X3 | The decision log write fails on feedback | The feedback answers 503 and no agent_feedback row is written; the run is still readable with no verdict, and the incident is raised under R-UNI-39 by the service, not by the harness | MSG-P7-003 | AC6 |
| X4 | Feedback already given for the run and item, or two requests arrive at once | The second request answers 409; exactly one decision record exists | MSG-GEN-004 | AC7 |
| X5 | The case is outside the user's scope | The agent-outputs read answers 404 | MSG-P4-003 | AC8 |
| X6 | The agent's mode is SHADOW for the case segment | The agent-outputs operation returns an empty list and no decision record is written for the case | None to a user | AC9 |
| X7 | The run used data older than the business date | The output carries MSG-P1-001 with the data date 2027-01-26 above the summary; the scenario passes only when both the message and the date are present | MSG-P1-001 | AC1 |
| X8 | A user without Case record U sends feedback | The feedback answers 403 | MSG-P4-002 | TC-E2-028-10-ITG |
| X9 | The seed pack cannot be loaded (case not owned, policy version absent, segment missing, counts off) | The run refuses to start and names the missing seed item; no scenario is reported | None | All |
| X10 | The evidence pack cannot be attached to the release record | The run is marked failed; the local evidence file is kept for rerun | None | All |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the three published contracts or their fakes, the policy fixture and the Enterprise AI test profile; it builds no service feature and has no build dependency |
| Negotiable | The scenarios, the seeded values, the verdict list, the mode per segment and the fixture counts are data files, never code |
| Valuable | The intake-agent journey is proven once across three services, with the D6 record and the acceptance measure in the same evidence as the summary |
| Estimable | One journey runner, one fake set, one fixture pack, three assertion helpers, one evidence collector, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a fixed Given, When and Then and a recorded pass or fail in the report |

### 7. Acceptance criteria

```gherkin
Feature: Case intake agent live at L1 [E3a]

  Background:
    Given policy "INTAKE" version "P2" with mode "L1" and prompt "PR3" is in force from 2027-01-25
    Given case "RW-2027-000501" is owned by "owner.user07" with RW-CASEOWN and is in that user's scope

  Scenario: AC1 L1 summary journey from CaseCreated to the stored output (new, D-RCV-60)
    Given the harness subscribes to `rwb.case.events.v1` and `rwb.agent.events.v1` before the case is created
    Given case "RW-2027-000501" has an ANSWERED intake run with gap flags MISSING_DOCUMENT and NO_VALID_APPRAISAL
    When rwb-case publishes `rwb.case.CaseCreated.v1` for the case and rwb-agent completes the run
    Then the run read through `GET /api/recovery/agent/v1/agent-runs` shows agent "INTAKE" and version "INTAKE@P2/PR3"
    Then `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` returns the summary, the two gap flags with reasons, agent "INTAKE", version "INTAKE@P2/PR3" and the marker "Agent output"
    Then the evidence records that the run was started by `rwb.case.CaseCreated.v1` on `rwb.case.events.v1`
    Then the agent-outputs read answers inside the 2 s timeout of one hop

  Scenario: AC2 Feedback writes the decision record before it is stored (new, D-RCV-60)
    Given the run of case "RW-2027-000501" has no feedback
    When "owner.user07" sends POST /api/recovery/agent/v1/agent-runs/{runId}/feedback with verdict "ACCEPTED" and an If-Match of the run row version
    Then one decision record exists with decision code "D6", agent version "INTAKE@P2/PR3" and final call "ACCEPTED"
    Then exactly one agent_feedback row exists for the run and item "SUMMARY"
    Then the next agent-outputs read returns the verdict "ACCEPTED" on that run
    Then the evidence records that the decision record was written before the feedback row

  Scenario: AC3 Acceptance measured for the January 2027 MORTGAGE/BKK cohort (new, D-RCV-60)
    Given January 2027 for segment MORTGAGE and region BKK holds 300 runs with feedback, 240 accepted, 45 corrected and 15 rejected
    When the harness reads GET /api/recovery/agent/v1/admin/agent-metrics for "INTAKE"
    Then the answer holds acceptance rate 0.8000 and correction rate 0.1500 for MORTGAGE/BKK
    Then each of the 300 feedback rows has one decision record with decision "D6" and agent version "INTAKE@P2/PR3"

  Scenario: AC4 Rule fallback on a timed out run (new, D-RCV-60)
    Given case "RW-2027-000502" has a run that reached the 60 s limit of AgentRunWorkflow
    When the harness reads the run and the agent outputs for the case
    Then the run holds status "TIMED_OUT" and fallback true
    Then `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` returns no summary for the case

  Scenario: AC5 Correction without a reason (new, D-RCV-60)
    When "owner.user07" sends POST /api/recovery/agent/v1/agent-runs/{runId}/feedback with verdict "CORRECTED" and an empty reason
    Then the answer is 422 with MSG-P7-005
    Then no decision record and no agent_feedback row exist for the run

  Scenario: AC6 The decision cannot be recorded (new, D-RCV-60)
    Given the rwb-decision decision log answers unavailable
    When "owner.user07" sends POST /api/recovery/agent/v1/agent-runs/{runId}/feedback with verdict "ACCEPTED"
    Then the answer is 503 with MSG-P7-003
    Then no agent_feedback row exists for the run
    Then the next agent-outputs read still returns the run with no verdict

  Scenario: AC7 Feedback given twice (new, D-RCV-60)
    Given "owner.user07" accepted the summary of case "RW-2027-000501" and the run holds one decision record
    When a second feedback request arrives for the same run and item "SUMMARY"
    Then the answer is 409 with MSG-GEN-004
    Then one decision record exists for the run

  Scenario: AC8 A case outside the user's scope (new, D-RCV-60)
    Given case "RW-2027-000601" belongs to team "HP-NE" outside the scope of "owner.user07"
    When "owner.user07" requests GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs for it
    Then the answer is 404 with MSG-P4-003

  Scenario: AC9 A segment still in shadow (new, D-RCV-60)
    Given the INTAKE policy for segment UNSECURED is mode "SHADOW"
    When the harness requests the agent outputs for unsecured case "RW-2027-000701"
    Then `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` returns an empty list
    Then no decision record is written for the case
```

No legacy acceptance criterion is owned by this story: the nine above are new and test only the integration deliverable, using the legacy values of RWB-E2-028 and no other. The stale-input assertion of legacy AC9 is carried inside AC1's evidence, because a harness has no panel to warn.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only runs in mode L1 for the case segment are returned to a user; shadow output is never returned | agent_policy.autonomy_mode, segment fields (New); AC9 |
| BR2 | Agent output is marked "Agent output" with the agent name and version | REQ-DRI-001; labels "Agent version" |
| BR3 | Feedback writes one decision log entry before it is stored: decision D6 (LOV-DECISION, assumed code), agent version, recommendation reference, final call, reason | Principle 5; R-UNI-39; CTL-06 |
| BR4 | A correction or a rejection needs a reason | CTL-07; MSG-P7-005 |
| BR5 | One feedback per run and item; the intake summary is item "SUMMARY" | agent_feedback unique key (New) |
| BR6 | The case record never waits for the model; the panel reads stored output | NFR-009; R-UNI-32 |
| BR7 | The summary holds masking tokens only | CTL-11 |

The rules are unchanged by the split. The harness asserts them across the service boundaries and restates none of them in code: the mode per segment, the verdict list and the item key are seeded data.

### 9. State transitions

None for the case. This story changes no case status; the harness asserts that no status, task or field moves because of an agent run or a verdict.

The agent run carries the status rwb-agent gives it, and the harness asserts only the two the legacy story names: "ANSWERED" for a completed run and "TIMED_OUT" with fallback true for a run that reached the 60 s limit. The feedback carries one verdict: ACCEPTED, CORRECTED or REJECTED, written once per run and item.

The harness adds a run state of its own only: Not started, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, test user "owner.user07" | Reads the agent output for cases in scope (Case record R) and gives one verdict per run (Case record U) |
| RW-TEAMMGR | Reads the agent output for team cases (Case record R); gives no verdict |
| SY-AGENT | Runs the agent and stores the output (read only to the harness) |
| SY-DECLOG | Writes the D6 entry the harness asserts, through rwb-decision's contract only |
| RW-COE | Reads acceptance and correction by segment (Platform administration R) |
| Integration lead | Agrees the fake set, the Enterprise AI test profile and the run window with the three service owners |
| QA lead | Owns the seed pack, the evidence format and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 case operation |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 case operation |
| DF-CAS-009 | recovery_case | owner_user_id | Read through the P3 case operation |
| DF-CAS-011 | recovery_case | team_code | Read through the P3 case operation (scope) |
| DF-CAS-012 | recovery_case | region_code | Read through the P3 case operation |
| DF-WRK-012 | assignment | assignee_user_id | Read through the P3 case operation (owner check) |
| DF-DOC-004 | document | document_type | Read through the P10 agent output, in the gap reasons; the document itself belongs to P5 |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 decision log operation |
| DF-AGT-036 to DF-AGT-050 | agent_run | id, agent_code, agent_version, autonomy_mode, status, output, confidence | Read through the P10 agent-run and agent-output operations |
| DF-AGT-055, DF-AGT-056 | agent_run | data_as_of, run_at | Read through the P10 agent-run operation |
| DF-AGT-097 to DF-AGT-102 | agent_feedback | id, agent_run_id, item_key, verdict, reason, decision_log_id | Read through the P10 agent-output operation; written by rwb-agent through its own contract, never by the harness |
| Standard column | agent_feedback | created_by, created_at | Read through the P10 agent-output operation |

The harness owns no table in any schema and no schema at all: no table, no view, no migration and no seed table is created by this story. It reads and writes only through the operations of section 12, and its own evidence holds identifiers, statuses, message ids and timestamps only, never personal data. Per-service Flyway (DP-15) belongs to the services under test, not to the harness. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/cases/{caseId}/agent-outputs` | P10 rwb-agent | Reads the stored L1 output: summary, gap flags with reasons, agent, agent version, marker and verdict (AC1, AC2, AC4, AC6, AC8, AC9) |
| POST | `/api/recovery/agent/v1/agent-runs/{runId}/feedback` | P10 rwb-agent | Records one verdict with an If-Match of the run row version; the D6 record is written first (AC2, AC5, AC6, AC7) |
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | P10 rwb-agent | Reads acceptance and correction by segment for INTAKE (AC3) |
| GET | `/api/recovery/agent/v1/agent-runs` | P10 rwb-agent | Reads the run: status, autonomy mode, agent and agent version, data as of, fallback flag (AC1, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case, its owner, team, region and product group the journey starts from (AC1, AC8) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Asserts the D6 entry, its agent version and its final call (AC2, AC3, AC5, AC6, AC7, AC9) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout, and every POST carries an If-Match and a key per scenario. The scope and owner check that rwb-agent makes inside its own process is not a path in the Ownership Map, so the harness seeds it through the role and scope of the rwb-access fake (12.8) and reads the resulting answer through the P10 operation instead of calling an access path.

#### 12.3 Events published

None. The harness publishes no Kafka event on a production topic; the one `CaseCreated` it sends is a seed message on the test topic, and the evidence goes to the release record through the pipeline.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | Asserts that the run of case "RW-2027-000501" was started by the case event inside the run window (DP-09) |
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Closes the run window and gives the run ID, the status and the fallback flag before the output read (DP-09, DP-10) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | Asserts that the D6 entry reached the shared topic inside the run window, alongside the ledger read of 12.2 (DP-03, DP-09) |

The harness consumes with its own consumer group and never reads a producer's outbox, inbox or schema.

#### 12.5 Workflows and activities

`AgentRunWorkflow` on queue `rwb-agent` is exercised, not built: the run has a 60 s limit and then the rule result (R-UNI-32), and the harness asserts which of the two the run ended on through the status and the fallback flag (AC1, AC4). JOB-11 Outbox sender is observed on its every-minute window, so the harness knows when a seed message or a produced event should have crossed the topic.

The harness starts no workflow, adds no activity and writes no schedule. The agent call to the Enterprise AI private endpoint (INT-23), the guardrail check and the storage of the output belong to RWB-P10-E2028-APP.

#### 12.6 Schedules

None. The harness adds no workflow and no schedule; the 60 s limit is inside `AgentRunWorkflow` and JOB-11's every-minute window is the platform's, both only observed.

#### 12.7 Tables owned

None. The harness owns no table in any schema and no schema of its own; it reads and writes through the operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-agent | The four P10 operations of 12.2 | OpenAPI of P10 | The output with summary and gaps, the empty list for SHADOW, the run with status "TIMED_OUT" and fallback true, 200 with the verdict on feedback, 422 MSG-P7-005, 409 MSG-GEN-004, 403 MSG-P4-002, 503 MSG-P7-003, and the metrics answer 0.8000 and 0.1500; keeps the request journal for the If-Match and ordering assertions |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases/{caseId}` | OpenAPI of P3 | The case, its owner, team, region and product group, and the ANSWERED case with the two gap flags |
| WireMock rwb-decision | `GET /api/recovery/decision/v1/decision-log` | OpenAPI of P7 | The D6 entry with agent version "INTAKE@P2/PR3" and the final call; 503 for AC6 |
| WireMock rwb-access | The P4 session operation | OpenAPI of P4 | The role, the scope and the Case record right of "owner.user07", the RW-PHONECOL user with Case record R only (MSG-P4-002) and case "RW-2027-000601" outside scope (MSG-P4-003) |
| Enterprise AI private endpoint test profile | The model call rwb-agent makes | The INT-23 contract, not in this workspace | A completion and a guardrail pass per scenario, and a timeout for AC4, with masking tokens in place of identifiers |

Each fake is replaced by the real service as its integration dependency lands, without a change to the scenarios. Not specified in the source documents (GAP-0410; ASM-0585): the fake set, the concrete fixture values, the test profile of the private endpoint, the harness environment and the evidence format.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 6 consumed, one hop on the owner's base with the 2 s timeout; the P4 session operation is called against the fake only and is not a production path of this story |
| Kafka | 3 events consumed on `rwb.case.events.v1`, `rwb.agent.events.v1` and `rwb.decision-record.v1`; none published on a production topic |
| Temporal | Observed only: `AgentRunWorkflow` on queue `rwb-agent` with the 60 s limit, and JOB-11 Outbox sender; no workflow, activity or schedule added |
| File | None |

### 13. Solution plan

**Package.** Folder `integration/recovery-agent-intake` in the ACE repository, package `<ACE base package>.recovery.integration.agentintake`. Not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | The D6 entry is read through rwb-decision and the `DecisionRecorded` event is read on the shared topic; the harness never reads a decision table |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The mode per segment, the verdict list and the item key are seeded reference data, never values in the harness code |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | The harness subscribes with its own consumer group and asserts the three events, never a producer's table |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | `AgentRunWorkflow` is observed on queue `rwb-agent`, including the 60 s limit and the rule result behind it; the harness adds no workflow and no schedule |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 uses the owner's base, so the harness never calls a monolith base |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The harness runs no migration and reads no schema; it asserts the seeded state through the contracts, so each service migrates on its own |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the real case record uses, on the same bases |

The platform H dependencies in the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the three I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date and holds the run lock |
| FakeRegistry | Configuration | WireMock mappings for rwb-agent, rwb-case, rwb-decision and rwb-access, one set per contract version, plus the Enterprise AI test profile selection |
| AgentFixturePack | Data | Cases, owners, segments, scopes, the policy fixture, the five seeded cases and the January 2027 counts, per scenario |
| OutputAssertion | Service | Compares the summary, the gap flags and reasons, the agent, the version and the marker against the fixture, and the empty list for SHADOW |
| FeedbackAssertion | Service | Posts the verdict, then checks the D6 entry, its agent version, its final call, the single agent_feedback row and the message of each refusal |
| MetricAssertion | Service | Reads the metrics operation and compares acceptance 0.8000 and correction 0.1500 for INTAKE on MORTGAGE/BKK |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with the event, the run, the output, the verdict, the decision record, the measure and the fallback flag |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached |

**Environment and test data.** SIT, the wave 2 harness profile, one business date, synthetic cases and synthetic owners only. The seeded values are the legacy section 7 Background, the five cases of section 3 and the January 2027 counts; no other value is added. Not specified in the source documents (GAP-0410; ASM-0585): the environment, the seed pack and the evidence format.

**Build steps**

1. Write the AgentFixturePack with the Background, the five cases, the policy fixture and the January 2027 counts; test that a bad seed stops the run (X9).
2. Write the FakeRegistry with the four WireMock mapping sets and the Enterprise AI test profile selection, with the policy and verdict data loaded from files.
3. Write JourneyRunner for AC1: publish `CaseCreated`, wait for `AgentRunCompleted`, read the run and assert the stored output and the `CaseCreated` link.
4. Add AC2 and AC7 with the feedback write, the If-Match, the decision-record-first ordering and the duplicate refusal.
5. Add AC5 and AC6 with the 422 and the 503, asserting that neither writes a feedback row.
6. Add AC3 with the metrics read and the one-D6-entry-per-feedback sweep, and AC4 with the 60 s limit, the TIMED_OUT status and the fallback flag.
7. Add AC8 and AC9 with the out-of-scope case and the SHADOW segment, then write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record and rerun the nine scenarios on the release build.

**Feature switch.** `rwb.agent.intake-l1` is on in the harness profile, as the legacy story sets it. Off, the agent-outputs operation returns an empty list and the harness reports the journey as not applicable rather than as passed. The harness itself is a pipeline stage selected by the run profile, not by a business flag.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all nine owned scenarios, and each fake has been replaced by the real service where its I story has landed in SIT. The fixture pack and the evidence sign-off wait for the values of the gap and assumption rows cited in sections 3, 12.8 and 13.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-005 | No L1 summary for the case because the run failed | The agent summary is not available for this case. Work from the case record. |
| MSG-P7-005 | Correct or Reject with no reason | Enter the reason you are not following the recommendation. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Feedback already given or row changed | Someone else changed this record. Reload it to see their change. |
| MSG-P4-003 | Case outside scope | This case is not in your scope. |
| MSG-P1-001 | Summary built on stale data | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The harness asserts these messages and never rewrites them. Its own report text is for the release team and is not part of the message standard.

### 15. Screens and states

SCR-03 Case record gains the panel "Agent summary": loading (skeleton), empty (no panel when no L1 output), unavailable (MSG-P10-005), stale (MSG-P1-001 above the summary with the data date), ready (summary, gap flags, Accept, Correct, Reject) and recorded (verdict and date, no controls). In the read only state of SCR-03 the controls are hidden. SCR-46 Agent monitor (state live) shows acceptance and correction by segment.

No screen is built by this story. The harness drives the operations behind those states and asserts the same six states through the contracts: the output present, absent, stale, filtered by mode and carrying a verdict. The panel and its states belong to RWB-P10-E2028-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-028-10-ITG | Access | Component | RW-PHONECOL (Case record R only) sends feedback; refused with MSG-P4-002 |
| TC-E2-028-01-ITG | AC1, BR1, BR2, BR6 | Integration | Case RW-2027-000501 with an ANSWERED run and two gaps |
| TC-E2-028-02-ITG | AC3, BR3 | Integration | January 2027, MORTGAGE/BKK: 300 feedback, 240, 45, 15 |
| TC-E2-028-03-ITG | AC4, BR6 | Integration | Case RW-2027-000502 with a TIMED_OUT run |
| TC-E2-028-04-ITG | AC5, BR4 | Integration | Correct with an empty reason |
| TC-E2-028-05-ITG | AC2, AC6, BR3 | Integration | Accept writes the record first; then the decision log writer fails on Accept |
| TC-E2-028-06-ITG | AC7, BR5 | Integration | Second feedback on the same run |
| TC-E2-028-07-ITG | AC8 | Integration | Case RW-2027-000601 in team HP-NE |
| TC-E2-028-08-ITG | AC9, BR1 | Integration | Unsecured case RW-2027-000701, segment in SHADOW |
| TC-E2-028-09-ITG | AC1, BR6 | Integration | Data as of 2027-01-26, business date 2027-01-28 |
| TC-E2-028-11-ITG | Principle 5 | NFR | Decision log write forced to fail on feedback; no feedback stored; MSG-P7-003 |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the app story's case, run across the four contracts and the Enterprise AI test profile. The app stories keep the unit and component copies of the same cases. TC-E2-028-09-ITG covers the stale assertion inside AC1, because the harness has no panel to warn.

### 17. Guardrails

- No business value in code: the mode per segment, the verdict list, the item key, the policy version and the prompt version are data in the seed pack, never values in the harness.
- No personal data in events, workflow inputs, logs, evidence or agent calls. The summary carries masking tokens and the seed holds synthetic cases and synthetic owners only.
- No read of another service's tables and no schema of the harness's own: every read and write goes through the operations of 12.2, and the harness runs no migration.
- Agent output never changes the case: the harness asserts that no status, task or field moves because of a run or a verdict.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.
- The harness never runs against UAT or production, and a value that must change changes in the seed pack through a reviewed change, never by an exception in a scenario.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records the agent and prompt versions | Business Requirements Program, sections 5.7 and 5.4 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32, R-UNI-39 | TC-E2-028-01-ITG, TC-E2-028-02-ITG, TC-E2-028-03-ITG, TC-E2-028-04-ITG, TC-E2-028-05-ITG, TC-E2-028-06-ITG, TC-E2-028-09-ITG, TC-E2-028-11-ITG |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Business Requirements Program, sections 5.7 and 5.4 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-07-ITG, TC-E2-028-08-ITG, TC-E2-028-10-ITG |

### 19. Out of scope

- Agent actions taken without the owner (autonomy L2 and above, Epic 8).
- Editing the summary text in the Workbench; a correction records the reason only.
- Intake document classification (P5 stories).
- Production code of any service in the journey: the operations of rwb-agent, rwb-case, rwb-decision and rwb-access, their schemas and their screens belong to their own stories.

The harness, the fakes and the evidence pack cover the four items above only as a caller or a consumer would see them; building any of them is out of scope for this story.
