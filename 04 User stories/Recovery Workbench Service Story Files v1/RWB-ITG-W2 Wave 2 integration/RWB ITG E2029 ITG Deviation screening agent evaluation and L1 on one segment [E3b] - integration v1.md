# RWB-ITG-E2029-ITG Deviation screening agent evaluation and L1 on one segment [E3b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2029-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2015-APP, RWB-P10-E2029-APP, RWB-S8-E2029-APP, RWB-P7-E2029-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DVH-001, REQ-DVH-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-029 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a repeatable cross-service harness for the deviation screening agent — the SCREEN-S2 evaluation with precision and recall per code, the L1 proposal and its approval for MORTGAGE in BKK, the proposals a run stores, the owner's confirmation that raises X1 through rwb-deviation under R-DEV-01 and pauses the stage clock, the rejection that writes its decision record first, and the measure the evaluation carries — with the evidence pack attached to the wave 2 release**, so that **the deviation-screening journey is proven end to end across rwb-agent, rwb-case, rwb-deviation and rwb-decision before RWB-P3-E2015-APP, RWB-P10-E2029-APP, RWB-S8-E2029-APP and RWB-P7-E2029-APP claim Done**.

This story builds the harness, its contract fakes, its seed pack, its evidence pack and its pass or fail gate. It builds no production endpoint, no screen, no table and no migration. Nothing it writes is deployed to a service.

No single app story can prove the journey. RWB-P3-E2015-APP can prove that the case record carries the product group and region, that the timers are stored and that the case turns "On hold" when a deviation clears it. RWB-P10-E2029-APP can prove that the evaluation is scored per code on a sample, that the L1 proposal is loaded and approved, that a run in mode L1 stores proposals and that a verdict is accepted or refused. RWB-S8-E2029-APP can prove that a raise with `raised_by` "SCREENING_AGENT" creates one deviation under R-DEV-01. RWB-P7-E2029-APP can prove that a rejection writes one decision record with the agent version and the reason, and that the ledger read returns it. The agreement of all four — one evaluation of 500 cases whose precision 0.9111 and recall 0.8913 for X1 are the numbers the L1 proposal names, one run whose proposals the owner decides, one confirmation that raises exactly one deviation and pauses exactly one clock while the prescription clock keeps running, one rejection that leaves one decision record and no deviation — is this story, and only this story.

### 2. Business rationale

RWB-E2-029 split into four app stories and this integration story. The app stories build the evaluation and the policy load, the output read and the feedback write, the deviation raise with its decision log entry, the decision-record mapping and the timer pause and resume inside their own services. What no app story can prove on its own is the chain the business actually relies on: SCREENING is evaluated on sample "SCREEN-S2" version 1 and the score per code is stored; the L1 proposal for segment MORTGAGE and region BKK is loaded with that evaluation run and its conditions, and approved; a run on a Mortgage case in Bangkok stores proposals, and the case record shows them; the owner confirms one, rwb-deviation raises that deviation with `raised_by` "SCREENING_AGENT" and applies R-DEV-01, which pauses the stage clock and leaves the prescription clock running, and the case goes "On hold"; the owner rejects another, and the decision record is written before the feedback row and no deviation exists; and the measure the evaluation stored is the measure the proposal and the reader see. That proof is this story.

The journey carries two requirements. Deviations X1 to X7 are detected from case data, call notes, documents and external flags (REQ-DVH-001): the harness asserts that the run of case "RW-2027-000801" was started on `CaseCreated` and drew on the complaint note stored on 2027-01-26 through `DocumentStored`, and that the proposals it reads back carry their reasons and sources. A deviation flag is visible on the case record and in every queue (REQ-DVH-006): the harness asserts that the case reads back "On hold" through rwb-case and that the same X1 the confirmation raised is the deviation `DeviationRaised` announces on the deviation topic, which is what every queue projects.

Architecture v5 changes the path, not the business. In the monolith the agent client, the policy row, the feedback table, the deviation raise, the timers and the decision log all sat in one deployment and one schema. In the target:

- the local decision record and the shared topic `rwb.decision-record.v1` carry every entry, with rwb-decision holding the ledger (DP-03);
- the ACE data behind the X7 collateral inputs is read only by rwb-source-data through the `v_ace_*` views, and every other service asks its contract, so the harness reads the appraisal date through the owner's answer and never a view (DP-05);
- the policy version, the segment and the parameters behind it are configuration data served by the owning service, never values in code (DP-06);
- the deviation codes X1 to X7, the `raised_by` value "SCREENING_AGENT" and the verdict list are reference data of the owning contract, not literals in a scenario (DP-07);
- the events are CloudEvents on the owner's topic, with an outbox on the producer and an inbox on the consumer, so a replay never counts a case twice (DP-09);
- the in-process `DeviationService.raise` of the monolith is a REST contract with a mock, one hop and the 2 s timeout, and the answer carries the deviation ID and the decision log entry ID (DP-11);
- every path is on the owner's base `/api/recovery/<short>/v1` (DP-13);
- the proposal panel is composed by gateway-bff from the P10 output and the P3 case, so the harness drives the same route the case record uses (DP-19).

The measure is the journey evidence: for each owned criterion, one pass or fail with the evaluation rows, the policy version, the run, the proposals, the confirmation, the deviation, the case state, the two clocks, the rejection record and the measure captured in one report that can be re-run for any build.

### 3. Preconditions

- Policy "SCREENING" version "P2" with prompt "PR2" is in force with mode "L1" for segment MORTGAGE and region BKK and mode "SHADOW" for every other segment, and carries the confidence floor 0.80 (legacy sections 3, 7 and 8).
- Sample "SCREEN-S2" version 1 holds the analysts' review of 500 shadow cases, with the X1 counts 41 true positives, 4 false positives and 5 false negatives, which is precision 0.9111 and recall 0.8913, and X4 at recall 0.6000 against the condition "recall at least 0.75 for every code" (legacy AC1 and AC10).
- Cases "RW-2027-000801" (Mortgage, region BKK, complaint note 2027-01-26, and a proposal for X6), "RW-2027-000802" (hire purchase, region BKK), "RW-2027-000803" (X2 at confidence 0.72) and "RW-2027-000804" (X1 confirmed twice at once) are seeded, owned by "owner.user07" with RW-CASEOWN and Case record CRU, and in that user's scope; a test user of role RW-PHONECOL holds Case record R only (legacy sections 3 and 7, TC-E2-029-11).
- The four integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-P3-E2015-APP (rwb-case, the case record and the two clocks), RWB-P10-E2029-APP (rwb-agent, the evaluation, the policy load, the output read and the feedback write), RWB-S8-E2029-APP (rwb-deviation, the raise and R-DEV-01) and RWB-P7-E2029-APP (rwb-decision, the decision record and the ledger read).
- The wave 2 harness environment (SIT) is available with the gateway route for `/api/recovery/*`, the topics `rwb.case.events.v1`, `rwb.document.events.v1`, `rwb.agent.events.v1`, `rwb.deviation.events.v1` and the shared topic `rwb.decision-record.v1`, the Temporal namespace `rwb-recovery` with the queues `rwb-agent` and `rwb-deviation`, and the Enterprise AI private endpoint test profile (INT-23). Not specified in the source documents (GAP-0411; ASM-0586): the harness environment and its seeding, the SCREEN-S2 fixture pack with its 500 labels, the Enterprise AI test profile and the evidence format.
- The feature switch `rwb.agent.screening-l1` is on in the harness profile (legacy section 13).
- Synthetic cases, synthetic owners and masking tokens only: no customer name, account number, national identifier or contact detail enters the harness, the seed pack or the evidence pack; the reason on a proposal holds masking tokens (legacy sections 14 and 17).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date and the versions of the four contracts it is about to exercise.
2. Harness: seeds the policy fixture (SCREENING P2 PR2, mode L1 for MORTGAGE in BKK and SHADOW elsewhere, floor 0.80), the sample SCREEN-S2 version 1 with its 500 cases and the X1 and X4 counts, cases "RW-2027-000801" to "RW-2027-000804", owner "owner.user07", the RW-PHONECOL test user and the segments.
3. Harness: calls the P4 session operation against the rwb-access fake and records the role, the scope and the Case record right the journey runs under.
4. Harness: subscribes to the five topics with its own consumer group before the run starts, so the window opens before the first event.
5. Harness: drives the evaluation through `POST /api/recovery/agent/v1/admin/agent-evaluations` on sample "SCREEN-S2" version 1 and reads it back through `GET /api/recovery/agent/v1/admin/agent-evaluations`, asserting sample size 500, precision 0.9111 and recall 0.8913 for X1 and recall 0.6000 for X4.
6. Harness: drives the L1 proposal through `POST /api/recovery/agent/v1/admin/agent-configs` for policy "SCREENING" version "P2" with segment MORTGAGE and BKK and the evaluation run ID, and approves it through `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` as RW-RISK; it then asserts through `GET /api/recovery/agent/v1/admin/agent-runs` that the runs of the segment carry mode L1 and the runs outside it carry SHADOW.
7. Harness: drives the case event — `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` for case "RW-2027-000801", and `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` for the complaint note of 2027-01-26 — and waits for `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` inside the run window.
8. Harness: reads `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` and asserts the X1 proposal with its reasons, its sources, the preceding contact and the marker "Agent output"; it asserts X2 at confidence 0.72 with the marker "Low confidence" on case "RW-2027-000803" and an empty list for the hire purchase case "RW-2027-000802".
9. Harness: confirms X1 on case "RW-2027-000801" through `POST /api/recovery/agent/v1/agent-runs/{runId}/feedback` with verdict "ACCEPTED" and an If-Match, and rejects X6 on the same case with verdict "REJECTED" and the reason "Customer answered on 2027-01-25".
10. Harness: reads the deviation the confirmation raised through `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` and, where the row must be touched, `PATCH /api/recovery/deviation/v1/deviations/{deviationId}`; then reads the case state through `GET /api/recovery/case/v1/cases/{caseId}` and the two clocks through `GET /api/recovery/case/v1/cases/{caseId}/timers`.
11. Harness: reads the evaluation rows through `GET /api/recovery/agent/v1/admin/agent-evaluations` and the decision records through `GET /api/recovery/decision/v1/decision-log`, asserting the one "X6" entry with agent version "SCREENING@P2/PR2" and final call "REJECTED", and the entry S8 wrote for the X1 confirmation.
12. Harness: writes the per-scenario evidence into one run report keyed by story key and business date, applies the gate, attaches the report to the wave 2 release record, releases the lock and restores the seed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case is not Mortgage in region BKK | The run stays in shadow; the outputs read returns nothing and no decision record is written | None to a user | AC3 |
| X2 | Reject with no reason | Refused with 422; no decision record and no feedback row | MSG-P7-005 | AC5 |
| X3 | A proposal is below the confidence floor 0.80 | Shown with the marker "Low confidence" and passed only when the marker and the confidence are both present | None to a user | AC8 |
| X4 | The proposed code is already open on the case | The proposal is not shown, so the harness confirms nothing and raises nothing | None to a user | TC-E2-029-07-ITG |
| X5 | Two confirmations of the same proposal at once | One deviation exists, the confirmation that loses answers 409, and no second feedback row is stored | MSG-GEN-004 | AC7 |
| X6 | The decision record cannot be written on a rejection | The rejection answers 503, no feedback row exists, and the incident is raised by the service under R-UNI-39, not by the harness | MSG-P7-003 | AC6 |
| X7 | The L1 proposal names a score below a stated condition | The load answers 422 and names the failing code and value; the version in force is unchanged | MSG-P10-001 | AC9 |
| X8 | A role without Case record U confirms or rejects | The request answers 403 and no feedback row is stored | MSG-P4-002 | TC-E2-029-11-ITG |
| X9 | The seed pack cannot be loaded (policy version absent, sample size not 500, counts off, contract version missing) | The run refuses to start and names the missing seed item; no scenario is reported | None | AC1 |
| X10 | The evidence pack cannot be attached to the release record | The run is marked failed and the local evidence file is kept for a rerun | None | TC-E2-029-12-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the four published contracts or their fakes, the policy and sample fixtures and the Enterprise AI test profile; it builds no service feature and has no build dependency |
| Negotiable | The scenarios, the seeded cases, the policy segment and floor, the 500 labels and the evidence format are data files, never code |
| Valuable | The deviation-screening journey is proven once across four services, with the evaluation score, the raised deviation, the two clocks and the rejection record in the same evidence as the proposals |
| Estimable | One journey runner, one fake set, one fixture pack, three assertion helpers, one evidence collector, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a fixed Given, When and Then and a recorded pass or fail in the report |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent evaluation and L1 on one segment [E3b]

  Background:
    Given policy "SCREENING" version "P2" with prompt "PR2" has mode "L1" for segment MORTGAGE and BKK and mode "SHADOW" for every other segment
    Given case owner "owner.user07" holds RW-CASEOWN and the cases are in that user's scope

  Scenario: AC1 The evaluation scores every code and the L1 proposal names it (new, D-RCV-60)
    Given the shadow run on 500 cases in sample "SCREEN-S2" version 1
    When the harness posts the evaluation through `POST /api/recovery/agent/v1/admin/agent-evaluations` and reads it back through `GET /api/recovery/agent/v1/admin/agent-evaluations`
    Then precision and recall per code X1 to X7 are stored with sample size 500
    Then for X1 with 41 true positives, 4 false positives and 5 false negatives precision is 0.9111 and recall is 0.8913
    Then the L1 proposal is recorded as policy "SCREENING" version "P2" with status "LOADED", segment MORTGAGE and BKK and the evaluation run ID
    Then the approval through `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` is accepted and the L1 proposal is the policy the next run carries

  Scenario: AC2 The L1 journey from the proposal to the raised deviation and the paused clock (new, D-RCV-60)
    Given Mortgage case "RW-2027-000801" in region BKK and a complaint note on 2027-01-26
    When the case event and the document event arrive and the agent runs in mode L1
    Then `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` returns X1 with its reasons, the preceding contact and the marker "Agent output"
    Then when "owner.user07" confirms X1 the S8 service raises deviation X1 with raised_by "SCREENING_AGENT" under rule R-DEV-01 and answers the deviation ID and the decision log entry ID
    Then `GET /api/recovery/case/v1/cases/{caseId}` shows case status "On hold"
    Then `GET /api/recovery/case/v1/cases/{caseId}/timers` shows the stage clock paused and the prescription clock running
    Then agent_feedback holds verdict "ACCEPTED" for item "X1" with the S8 decision log entry ID
    Then `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1` announces the same deviation inside the run window

  Scenario: AC3 Other segments stay in shadow (new, D-RCV-60)
    Given hire purchase case "RW-2027-000802" in region BKK with mode "SHADOW"
    When the agent runs for the case
    Then the run stays in shadow and `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` returns nothing
    Then no deviation is raised and no decision record is written for the case

  Scenario: AC4 A rejection writes its decision record before the feedback row (new, D-RCV-60)
    Given the agent proposes X6 on case "RW-2027-000801"
    When "owner.user07" rejects X6 with the reason "Customer answered on 2027-01-25"
    Then one decision record holds decision "X6", agent version "SCREENING@P2/PR2", final call "REJECTED" and the reason
    Then the decision record exists before the agent_feedback row and agent_feedback holds "REJECTED" for item "X6"
    Then no deviation is raised for the case by the rejection

  Scenario: AC5 Reject without a reason (new, D-RCV-60)
    When "owner.user07" rejects X6 with an empty reason
    Then the answer is 422 with MSG-P7-005
    Then no decision record and no agent_feedback row exist for the rejection

  Scenario: AC6 The rejection cannot be recorded (new, D-RCV-60)
    Given the rwb-decision decision log answers unavailable
    When "owner.user07" rejects X6 with a reason
    Then the answer is 503 with MSG-P7-003
    Then no agent_feedback row exists and no deviation is raised

  Scenario: AC7 Two confirmations at once (new, D-RCV-60)
    Given two sessions of "owner.user07" confirm X1 on case "RW-2027-000804" at the same time
    When both requests arrive
    Then one deviation X1 exists and the second request answers 409 with MSG-GEN-004
    Then exactly one agent_feedback row holds "ACCEPTED" for item "X1"

  Scenario: AC8 A low-confidence proposal (new, D-RCV-60)
    Given the agent proposes X2 with confidence 0.72 on case "RW-2027-000803"
    When the harness reads the outputs for the case
    Then X2 is returned with the marker "Low confidence" and confidence 0.72

  Scenario: AC9 A proposal with scores below its condition (new, D-RCV-60)
    Given X4 has recall 0.6000 in the evaluation of "SCREEN-S2"
    When RW-COE loads an L1 proposal with condition "recall at least 0.75 for every code"
    Then the load answers 422 with MSG-P10-001 naming "X4 recall 0.6000 below 0.75"
    Then the version in force is unchanged
```

No legacy acceptance criterion is owned by this story: the `acs` list is empty and the nine above are new. They test only the integration deliverable, using the legacy values of RWB-E2-029 and inventing none.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Mode L1 applies only where the case product group and region match the policy segment; elsewhere the mode is SHADOW and nothing is returned to a user | agent_policy.segment_product_group, segment_region_code (New); AC3, AC1 |
| BR2 | The agent raises nothing itself; a deviation exists only when a person confirms the proposal | Agent catalog, screening agent "May decide alone: Nothing"; role SY-AGENT has no Case record U; AC2, AC7 |
| BR3 | A confirmed proposal is raised through S8 with raised_by "SCREENING_AGENT", and R-DEV-01 pauses the stage clock, keeps the prescription clock running and routes the case | R-DEV-01; LOV-RAISED-BY; AC2 |
| BR4 | A rejection needs a reason and writes its decision record before the feedback row; a failure to record leaves nothing behind | CTL-07; Principle 5; R-UNI-39; AC4, AC5, AC6 |
| BR5 | A proposal for a code already open on the case is not shown | deviation.deviation_code; TC-E2-029-07-ITG |
| BR6 | A proposal below the confidence floor 0.80 is shown with the marker "Low confidence" | agent_policy.confidence_floor (New); FEAT-DVH-08; AC8 |
| BR7 | An L1 proposal must meet its stated conditions on the named evaluation, and a failed check leaves the version in force unchanged | Principle 1; CTL-08; AC9 |

The rules are unchanged by the split. The harness asserts them across the service boundaries and restates none of them in code: the segment, the floor 0.80, the condition "recall at least 0.75 for every code" and the verdict list are seeded data.

### 9. State transitions

None for the case itself: the harness holds no case record and moves no state of its own. What it asserts is that the owning services move the case exactly as the legacy story says — "On hold" on a confirmation (R-DEV-01 applied by S8), and no case status change at all on a rejection.

The run carries the autonomy mode the policy sets for its segment, and the harness asserts the two the legacy story names: L1 for MORTGAGE in BKK and SHADOW everywhere else, on the run row as well as on the policy row. The evaluation carries the sample size 500 and one precision and one recall per code. The feedback carries one verdict per run and item: ACCEPTED for item "X1" with the S8 decision log entry ID on the confirm path, REJECTED with the reason on the reject path.

The harness adds a run state of its own only: Not started, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, test user "owner.user07" | Reads the proposals for cases in scope (Case record R); confirms or rejects (Case record U) |
| RW-COE | Runs the evaluation and loads the L1 proposal (Rules and parameters C) |
| RW-RISK | Approves the L1 proposal (Rules and parameters A) |
| RW-CONDUCT | Reads the scores per code (Rules and parameters R) |
| SY-AGENT | Runs the agent and stores the proposals and the feedback (read only to the harness) |
| SY-DECLOG | Writes the rejection record and the record S8 writes, through the owners' contracts only |
| Integration lead | Agrees the fake set, the Enterprise AI test profile and the run window with the four service owners |
| QA lead | Owns the seed pack, the evidence format and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 case operation |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 case operation (segment match) |
| DF-CAS-005 | recovery_case | status | Read through the P3 case operation ("On hold" after a confirmation) |
| DF-CAS-012 | recovery_case | region_code | Read through the P3 case operation (segment match) |
| DF-WRK-012 | assignment | assignee_user_id | Read through the P3 case operation (owner check) |
| DF-ACE-193 | v_ace_valuation | appraisal_date | Read through the P10 agent-output operation, in the X7 proposal's sources; the view belongs to P1 and the harness reads none |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 decision log operation; written by P7 and P10 through their own contracts, never by the harness |
| DF-AGT-036 | agent_run | id | Read through the P10 agent-run list |
| DF-AGT-038 | agent_run | agent_version | Read through the P10 agent-run list ("SCREENING@P2/PR2") |
| DF-AGT-043 | agent_run | autonomy_mode | Read through the P10 agent-run list (L1 or SHADOW) |
| DF-AGT-046 | agent_run | status | Read through the P10 agent-run list |
| DF-AGT-049 | agent_run | output | Read through the P10 agent-output operation (the proposals) |
| DF-AGT-050 | agent_run | confidence | Read through the P10 agent-output operation (0.72 on X2) |
| DF-AGT-059 | agent_run | segment_product_group | Read through the P10 agent-run list |
| DF-AGT-060 | agent_run | segment_region_code | Read through the P10 agent-run list |
| DF-AGT-098 | agent_feedback | agent_run_id | Read through the P10 agent-output operation; written by rwb-agent through its own contract |
| DF-AGT-099 | agent_feedback | item_key | Read through the P10 agent-output operation ("X1", "X6") |
| DF-AGT-100 | agent_feedback | verdict | Read through the P10 agent-output operation ("ACCEPTED", "REJECTED") |
| DF-AGT-101 | agent_feedback | reason | Read through the P10 agent-output operation (masking tokens only) |
| DF-AGT-102 | agent_feedback | decision_log_id | Read through the P10 agent-output operation (the S8 entry ID) |
| DF-AGT-003 | agent_policy | policy_version | Write through the P10 agent-config operation; read back on the run |
| DF-AGT-008 | agent_policy | autonomy_mode | Write through the P10 agent-config operation; read back on the run |
| DF-AGT-009 | agent_policy | segment_product_group | Write through the P10 agent-config operation; read back on the run |
| DF-AGT-010 | agent_policy | segment_region_code | Write through the P10 agent-config operation; read back on the run |
| DF-AGT-017 | agent_policy | evaluation_run_id | Write through the P10 agent-config operation |
| DF-AGT-018 | agent_policy | promotion_conditions | Write through the P10 agent-config operation |
| DF-AGT-089 | agent_evaluation | label_key | Write through the P10 agent-evaluation operation; read back through its read |
| DF-AGT-090 | agent_evaluation | sample_size | Write through the P10 agent-evaluation operation (500) |
| DF-AGT-095 | agent_evaluation | precision_value | Write through the P10 agent-evaluation operation (0.9111 for X1) |
| DF-AGT-096 | agent_evaluation | recall_value | Write through the P10 agent-evaluation operation (0.8913 for X1, 0.6000 for X4) |

The harness owns no table in any schema and no schema at all: no table, no view, no migration and no seed table is created by this story (DP-01). It reads and writes only through the operations of section 12, and its own evidence holds identifiers, statuses, message ids and timestamps only, never personal data. Per-service Flyway belongs to the services under test and the harness runs no migration of its own. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case, its product group, region and status: the segment match before the run and "On hold" after the confirmation (AC2, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | Asserts the paused stage clock and the running prescription clock after R-DEV-01 is applied (AC2) |
| GET | `/api/recovery/agent/v1/cases/{caseId}/agent-outputs` | P10 rwb-agent | Reads the stored proposals with reasons, sources, preceding contact, confidence, the marker "Agent output", the marker "Low confidence" and the verdict (AC2, AC3, AC4, AC8) |
| POST | `/api/recovery/agent/v1/agent-runs/{runId}/feedback` | P10 rwb-agent | Records one verdict per run and item with an If-Match of the run row version; the decision record is written first on a rejection (AC2, AC4, AC5, AC6, AC7) |
| POST | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | Runs the evaluation of "SCREENING" on sample "SCREEN-S2" version 1 and stores precision and recall per code with sample size 500 (AC1, AC9) |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | Reads the evaluation rows back: 500, 0.9111 and 0.8913 for X1, 0.6000 for X4 (AC1, AC9) |
| POST | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | Loads the L1 proposal as policy "SCREENING" version "P2" with segment MORTGAGE and BKK, the evaluation run ID and the conditions (AC1, AC9) |
| POST | `/api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` | P10 rwb-agent | Approves the proposal as RW-RISK, and answers 409 with MSG-P7-002 when the loader tries to approve what it loaded (AC1, AC9) |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | Reads the runs of a segment to assert mode L1 for MORTGAGE in BKK and SHADOW elsewhere (AC1, AC2, AC3) |
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The only way a deviation is raised (DP-01): code "X1", `raised_by` "SCREENING_AGENT", R-DEV-01 applied, answering the deviation ID and the decision log entry ID (AC2, AC7) |
| PATCH | `/api/recovery/deviation/v1/deviations/{deviationId}` | S8 rwb-deviation | The other deviation row in the Ownership Map; the harness asserts what it needs from the raise answer and the `DeviationRaised` event and touches this path only where a scenario must update the row it created (AC2, AC7) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Asserts the one "X6" entry with agent version "SCREENING@P2/PR2" and final call "REJECTED", the S8 entry of the confirmation, and that a shadow case wrote none (AC2, AC3, AC4, AC5, AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout, and every POST carries an If-Match and a key per scenario. The scope and owner check that rwb-agent and rwb-deviation make inside their own process is not a path in the Ownership Map, so the harness seeds it through the role and scope of the rwb-access fake (12.8) and reads the resulting answer through the owner's operation.

#### 12.3 Events published

None. The harness publishes no Kafka event on a production topic; the `CaseCreated` and `DocumentStored` it sends are seed messages on the test topic, and the evidence goes to the release record through the pipeline.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | Asserts that the run of case "RW-2027-000801" was started by the case event inside the run window (DP-09) |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | The document side of REQ-DVH-001: the complaint note of 2027-01-26 is the source the X1 proposal names (DP-09) |
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Closes the run window and gives the run ID and the mode before the output read (DP-09) |
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Closes the confirm window and proves that the flag every queue projects is the deviation the confirmation raised (REQ-DVH-006, DP-09) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | Asserts that the "X6" record and the S8 record reached the shared topic inside the run window, alongside the ledger read of 12.2 (DP-03, DP-09) |

The harness consumes with its own consumer group and never reads a producer's outbox, inbox or schema.

#### 12.5 Workflows and activities

`AgentRunWorkflow` on queue `rwb-agent` is observed, not built: the run has a 60 s limit and then the rule result (R-UNI-32), and the harness asserts which of the two the run ended on from the run it reads back (AC2, AC3). `DeviationWorkflow`, the child workflow of the case on queue `rwb-deviation`, is observed after the raise, and the harness reads the result of the pause from the two clocks (AC2).

The harness starts no workflow, adds no activity and writes no schedule. The agent call to the Enterprise AI private endpoint (INT-23), the guardrail check and the storage of the proposals belong to RWB-P10-E2029-APP; the raise, the pause of the stage clock and the routing belong to RWB-S8-E2029-APP and RWB-P3-E2015-APP.

#### 12.6 Schedules

None. The harness adds no workflow and no schedule; the 60 s limit is inside `AgentRunWorkflow` and the every-minute outbox relay is the platform's, both only observed.

#### 12.7 Tables owned

None. The harness owns no table in any schema and no schema of its own; it reads and writes through the operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-agent | The seven P10 operations of 12.2 | OpenAPI of P10 | The output with proposals for MORTGAGE in BKK, the empty list for SHADOW, the evaluation rows with sample size 500 and 0.9111, 0.8913 and 0.6000, the proposal load and its approval, the run list with mode L1 and SHADOW, 200 with the verdict on feedback, 422 MSG-P10-001, 409 MSG-P7-002 and the refusals of 422 MSG-P7-005, 409 MSG-GEN-004, 403 MSG-P4-002 and 503 MSG-P7-003; keeps the request journal for the If-Match and ordering assertions |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timers` | OpenAPI of P3 | The case with its owner, region, product group and status, the "On hold" case after the confirmation, and the two timer rows: the paused stage clock and the running prescription clock |
| WireMock rwb-deviation | `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` and `PATCH /api/recovery/deviation/v1/deviations/{deviationId}` | OpenAPI of S8 | The raised deviation with its decision log entry ID and R-DEV-01 applied, and 409 on the second raise of the same code |
| WireMock rwb-decision | `GET /api/recovery/decision/v1/decision-log` | OpenAPI of P7 | The "X6" entry with agent version "SCREENING@P2/PR2" and final call "REJECTED", the S8 entry of the confirmation, and 503 for AC6 |
| WireMock rwb-access | The P4 session operation | OpenAPI of P4 | The role, the scope and the Case record right of "owner.user07" (CRU), and the RW-PHONECOL user with Case record R only (MSG-P4-002) |
| Enterprise AI private endpoint test profile | The model call rwb-agent makes | The INT-23 contract, not in this workspace | A completion for the screening run, an answer at confidence 0.72 for the X2 case, and a timeout for the failure path, with masking tokens in place of identifiers |

Each fake is replaced by the real service as its integration dependency lands, without a change to the scenarios. Not specified in the source documents (GAP-0411; ASM-0586): the fake set, the concrete fixture values, the SCREEN-S2 labels, the Enterprise AI test profile, the harness environment, the forced failure and parallel-confirmation controls, and the evidence format and the gate.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 12 consumed, one hop on the owner's base with the 2 s timeout; the P4 session operation is called against the fake only and is not a production path of this story |
| Kafka | 5 events consumed on `rwb.case.events.v1`, `rwb.document.events.v1`, `rwb.agent.events.v1`, `rwb.deviation.events.v1` and `rwb.decision-record.v1`; none published on a production topic |
| Temporal | Observed only: `AgentRunWorkflow` on queue `rwb-agent` with the 60 s limit and the rule result behind it (R-UNI-32), and `DeviationWorkflow` on queue `rwb-deviation`; no workflow, activity or schedule added |
| File | None |

### 13. Solution plan

**Package.** Folder `integration/recovery-agent-deviation` in the ACE repository, package `<ACE base package>.recovery.integration.agentdeviation`. Not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | The "X6" rejection record and the record S8 writes are read through rwb-decision, and `DecisionRecorded` is read on the shared topic; the harness never reads a decision table |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | The X7 collateral input is the appraisal date DF-ACE-193, which only P1 reads from the view; the harness asserts it through the P10 output and reads no view and seeds no ACE data |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The policy version, the segment, the floor 0.80 and the condition "recall at least 0.75 for every code" are configuration values supplied through the owning service's admin operation, never constants in the harness |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The codes X1 to X7, the `raised_by` value "SCREENING_AGENT" and the verdict list are reference data read from the owner's contract, not literals in the scenarios |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | The harness subscribes with its own consumer group to the five topics and asserts the five events; it never reads a producer's outbox or inbox |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The in-process `DeviationService.raise` of the monolith is the S8 POST on the owner's base with the 2 s timeout; the harness asserts the deviation ID and the decision log entry ID it answers |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 uses the owner's base, so no scenario can call a monolith path |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The panel "Proposed deviations" is composed by gateway-bff from the P10 output and the P3 case; the harness drives the same route the case record uses, on the same bases |

The platform H dependencies in the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the four I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date and holds the run lock |
| FakeRegistry | Configuration | WireMock mappings for rwb-agent, rwb-case, rwb-deviation, rwb-decision and rwb-access, one set per contract version, plus the Enterprise AI test profile selection |
| ScreeningFixturePack | Data | Policy SCREENING P2 PR2, sample SCREEN-S2 version 1 with the 500 labels, cases "RW-2027-000801" to "RW-2027-000804", the RW-PHONECOL test user, the segment and the counts, per scenario |
| ProposalAssertion | Service | Compares the proposals, their reasons and sources, the preceding contact, the marker "Agent output", the marker "Low confidence", the confidence 0.72 and the empty list for SHADOW |
| DeviationAssertion | Service | Confirms and rejects through the feedback operation, then checks the raised deviation, `raised_by` "SCREENING_AGENT", R-DEV-01, the case status, the two clocks and the message of each refusal |
| MetricAssertion | Service | Reads the evaluation rows and compares sample size 500, precision 0.9111 and recall 0.8913 for X1, recall 0.6000 for X4, and the condition that refuses the load |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with the evaluation, the policy version, the run, the proposals, the confirmation, the deviation, the case state, the two clocks, the rejection record and the measure |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached to the release record |

**Environment and test data.** SIT, the wave 2 harness profile, one business date, synthetic cases and synthetic owners only. The seeded values are the legacy section 7 Background, the policy and sample fixtures of section 3, the four cases of section 3 and the counts 41, 4, 5 and 0.6000; no other value is added. Not specified in the source documents (GAP-0411; ASM-0586): the environment and its seeding, the SCREEN-S2 fixture pack, the Enterprise AI test profile, the forced failures and the evidence format.

**Build steps**

1. Write the ScreeningFixturePack with the Background, the policy fixture, sample "SCREEN-S2" version 1 with its 500 labels, the four cases and the counts; test that a bad seed stops the run (X9).
2. Write the FakeRegistry with the five WireMock mapping sets and the Enterprise AI test profile selection, with the policy, the condition and the verdict list loaded from files.
3. Write JourneyRunner for AC1: post the evaluation, read it back, load the L1 proposal, approve it, and assert the numbers and the evaluation run ID on the proposal.
4. Add AC2 with the case and document events, the outputs read, the confirmation, the deviation raise, the case status, the two clocks, the feedback row and the `DeviationRaised` window.
5. Add AC3 and AC8 with the SHADOW case and the low-confidence proposal, then AC4 and AC7 with the rejection record first, the duplicate refusal and its 409.
6. Add AC5 and AC6 with the 422 and the 503, asserting that neither writes a feedback row, then AC9 with the condition that refuses the load.
7. Write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record and rerun the nine scenarios on the release build.

**Feature switch.** `rwb.agent.screening-l1` is on in the harness profile, as the legacy story sets it. Off, every segment runs in shadow and the outputs read returns nothing, so the harness reports the journey as not applicable rather than as passed. The harness itself is a pipeline stage selected by the run profile, not by a business flag.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all nine owned scenarios, and each fake has been replaced by the real service where its I story has landed in SIT. The fixture pack and the evidence sign-off wait for the values of the gap and assumption rows cited in sections 3, 12.8 and 13.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-005 | Reject without a reason | Enter the reason you are not following the recommendation. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Second confirmation of the same proposal | Someone else changed this record. Reload it to see their change. |
| MSG-P10-001 | L1 proposal fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-S8-001 | Deviation raised after confirmation | {deviation} was raised. The case is with {handler}. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The harness asserts these messages and never rewrites them. Its own report text is for the release team and is not part of the message standard.

### 15. Screens and states

SCR-03 Case record gains the panel "Proposed deviations" with states: empty (no panel), ready (proposals with reasons, sources, confidence and Confirm and Reject), low confidence (the marker on the proposal), and recorded (the verdict and the date). After a confirmation SCR-03 shows the on hold banner of the deviation and the paused stage clock, with the prescription clock still running. SCR-08 Deviation queue lists the flagged case for the named handler. SCR-46 Agent monitor shows SCREENING as live for MORTGAGE in BKK and Shadow elsewhere.

No screen is built by this story. The harness drives the operations behind those states and asserts the same states through the contracts; the panel, the queue and the monitor belong to their own app stories. The screen fixtures that reproduce these states are in no source read. Not specified in the source documents (GAP-0411; ASM-0586).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-029-11-ITG | Access | Component | RW-PHONECOL (Case record R only) confirms X1; refused with MSG-P4-002 across the P10 and S8 contracts |
| TC-E2-029-01-ITG | AC1, BR7 | Integration | SCREEN-S2 version 1, 500 cases; X1 counts 41, 4, 5; the proposal names the evaluation run the evaluation read returns |
| TC-E2-029-02-ITG | AC2, BR1, BR2, BR3 | Integration | Mortgage case RW-2027-000801 in BKK, complaint note 2027-01-26; one deviation with `raised_by` "SCREENING_AGENT" and one paused clock |
| TC-E2-029-03-ITG | AC3, BR1 | Integration | Hire purchase case RW-2027-000802 in BKK; empty outputs and no decision record |
| TC-E2-029-04-ITG | AC4, BR4 | Integration | Reject X6 with a reason; one decision record before the feedback row and no deviation |
| TC-E2-029-05-ITG | AC5, BR4 | Integration | Reject X6 with an empty reason; 422 and nothing stored |
| TC-E2-029-06-ITG | AC8, BR6 | Integration | X2 with confidence 0.72; the marker "Low confidence" through the P10 output |
| TC-E2-029-07-ITG | AC2, BR5 | Integration | X1 already open on the case; the proposal is not returned and nothing is raised |
| TC-E2-029-08-ITG | AC7 | Integration | Two parallel confirmations of X1; one deviation, one feedback row, 409 MSG-GEN-004 |
| TC-E2-029-09-ITG | AC6, BR4 | Integration | Decision log writer fails on rejection; 503 MSG-P7-003 and no feedback row |
| TC-E2-029-10-ITG | AC9, BR7 | Integration | X4 recall 0.6000, condition 0.75; 422 MSG-P10-001 naming the code and the value |
| TC-E2-029-12-ITG | Principle 5 | NFR | Decision log write forced to fail on a rejection; nothing stored; MSG-P7-003 |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the legacy case of the same number, run across the four contracts and the Enterprise AI test profile, with the cross-service assertion added — the deviation, the case state, the two clocks or the decision record that a single service cannot show. The app stories keep the unit and component copies of the same cases.

### 17. Guardrails

- No business value in code: the segment, the floor 0.80, the condition, the sample size 500 and the verdict list are data in the seed pack, never values in the harness.
- No personal data in events, workflow inputs, logs, evidence or agent calls: the reasons carry masking tokens and the seed holds synthetic cases and synthetic owners only.
- No read of another service's tables and no schema of the harness's own: every read and write goes through the operations of 12.2, no `v_ace_*` view is read, and only S8 raises a deviation.
- Agent output never changes the case: the harness asserts that no status, task or field moves because of a run or a verdict, and that only the confirmation moves the case.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.
- The harness never runs against UAT or production, and a value that must change changes in the seed pack through a reviewed change, never by an exception in a scenario.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-DVH-07, FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-39 | TC-E2-029-01-ITG, TC-E2-029-03-ITG, TC-E2-029-04-ITG, TC-E2-029-05-ITG, TC-E2-029-06-ITG, TC-E2-029-09-ITG, TC-E2-029-10-ITG, TC-E2-029-12-ITG |
| REQ-DVH-006 | A deviation flag is visible on the case and in every queue | Business Requirements Program, section 5.15 | FEAT-DVH-07 | 11 Handle customer care and deviations | R-DEV-01 | TC-E2-029-02-ITG, TC-E2-029-07-ITG, TC-E2-029-08-ITG, TC-E2-029-11-ITG |

### 19. Out of scope

- L1 on further segments: a later policy version, outside this journey.
- The deviation flows after the flag in S8: routing, contact stop, handling and return belong to RWB-S8-E2029-APP.
- The agent handling X6 and X7 within policy, which the S8 flows own.
- Production code of any service in the journey: the operations of rwb-agent, rwb-case, rwb-deviation and rwb-decision, their schemas and their screens belong to their own stories.

The harness, the fakes and the evidence pack cover the four items above only as a caller or a consumer would see them; building any of them is out of scope for this story.
