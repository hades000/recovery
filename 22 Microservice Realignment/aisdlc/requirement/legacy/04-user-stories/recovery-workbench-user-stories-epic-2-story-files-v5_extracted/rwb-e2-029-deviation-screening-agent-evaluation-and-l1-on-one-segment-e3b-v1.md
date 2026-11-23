<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 029 Deviation screening agent evaluation and L1 on one segment E3b v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 029 Deviation screening agent evaluation and L1 on one segment E3b v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-029 Deviation screening agent evaluation and L1 on one segment [E3b]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-029 |
| Epic | E3, release 31 January 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-DVH-07 Screen for deviations with the agent at L1 on one segment; FEAT-AGT-08 Run the deviation screening agent at L1 |
| Requirement IDs | REQ-DVH-001, REQ-DVH-006 |
| BRD section | Business Requirements Program, section 5.15 |
| L3 process | 11 Handle customer care and deviations |
| Decision | X1 to X7 |
| Priority | Must |
| Depends on | RWB-E1-062, RWB-E2-015, RWB-E1-061, RWB-E2-028 |
| Status | Ready for build |

## 1. Story

As a **conduct and QA officer (RW-CONDUCT)**, I want **the deviation screening agent scored on 500 shadow cases and switched to L1 for Mortgage cases in Bangkok, with its proposed X flags shown to the case owner to confirm or reject**, so that **deviations on that segment are flagged from the first day a sign appears and the error rate per flag is known**.

## 2. Business rationale

A deviation found weeks late means contact that should have stopped and clocks that should have paused. The shadow results of RWB-E1-062 give a measured precision and recall per code. This story scores a larger shadow run, records the proposal to go to L1 on one segment, and then shows the agent's proposals to the owner of each Mortgage case in Bangkok, who confirms or rejects each one. A confirmed proposal raises the deviation through the S8 deviation service, so the flag shows on the case and in every queue (REQ-DVH-006), and detection draws on case data, call notes and documents (REQ-DVH-001). Every other segment stays in shadow.

## 3. Preconditions

- RWB-E1-062 is done: SCREENING runs in shadow and scores per code.
- RWB-E2-015 is done: the S8 deviation service raises a deviation, applies R-DEV-01 and shows the flag on SCR-03 and the queues.
- RWB-E1-061 is done: the L1 proposal checks exist in the policy loader.
- RWB-E2-028 is done: GET /cases/{caseId}/agent-outputs, POST /agent-runs/{runId}/feedback and agent_feedback exist.
- Sample "SCREEN-S2" version 1 holds the business analysts' review of 500 shadow cases.
- The case owner holds RW-CASEOWN (Case record CRU) and the case is in scope.

## 4. Flow

1. RW-COE: starts the evaluation of "SCREENING" on "SCREEN-S2" version 1.
2. System: stores precision and recall per code X1 to X7 with sample size 500.
3. RW-COE: loads policy "SCREENING" version "P2" with mode L1 for segment MORTGAGE and BKK, the evaluation run, the conditions, the fallback and the measures; RW-RISK approves it.
4. System: on EV-01 or EV-16 for a Mortgage case in region BKK, runs SCREENING in mode L1; for any other segment, runs it in shadow.
5. Case owner: opens SCR-03 Case record; the panel "Proposed deviations" lists each proposed code with reasons, sources, confidence and the marker "Agent output".
6. Case owner: confirms a proposal; the system calls the S8 deviation service, which raises the deviation with raised_by SCREENING_AGENT and applies R-DEV-01.
7. System: stores feedback ACCEPTED for that code, linked to the decision log entry S8 wrote.
8. Case owner: rejects a proposal with a reason; the system writes a decision log entry with final call REJECTED and stores feedback REJECTED.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case is not Mortgage in region BKK | The run is in shadow; nothing is shown | None to a user | AC3 |
| X2 | Reject with no reason | Refused with 422 | MSG-P7-005 | AC5 |
| X3 | A proposal is below the confidence floor 0.80 | Shown with the marker "Low confidence" | None to a user | AC6 |
| X4 | The proposed code is already open on the case | The proposal is not shown | None to a user | AC7 |
| X5 | Two confirmations of the same proposal at once | One deviation; the second is refused with 409 | MSG-GEN-004 | AC8 |
| X6 | The decision log write fails on a rejection | Nothing stored; incident raised (R-UNI-39) | MSG-P7-003 | AC9 |
| X7 | The L1 proposal names scores below a stated condition | Policy load refused | MSG-P10-001 | AC10 |
| X8 | A role without Case record U confirms or rejects | Refused with 403 | MSG-P4-002 | TC-E2-029-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the screening agent (RWB-E1-062), the deviation service (RWB-E2-015) and the output and feedback endpoints (RWB-E2-028) |
| Negotiable | The segment, the floor and the conditions are values in the policy row |
| Valuable | Flags deviations on Mortgage cases in Bangkok when the sign appears, with a person deciding each one |
| Estimable | One panel, one confirm path through S8, one reject path, one evaluation |
| Small | Two developers for two weeks |
| Testable | Each criterion runs on synthetic cases in two segments |

## 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent evaluation and L1 on one segment [E3b]

  Background:
    Given policy "SCREENING" version "P2" with prompt "PR2" has mode "L1" for segment MORTGAGE and BKK and mode "SHADOW" for every other segment
    Given case owner "owner.user07" holds RW-CASEOWN

  Scenario: AC1 Evaluation
    Given the shadow run on 500 cases in sample "SCREEN-S2" version 1
    When the evaluation runs
    Then precision and recall per flag X1 to X7 are stored with sample size 500
    Then for X1 with 41 true positives, 4 false positives and 5 false negatives precision is 0.9111 and recall is 0.8913
    Then the system records the L1 proposal as policy "SCREENING" version "P2" with status "LOADED", segment MORTGAGE and BKK and the evaluation run ID

  Scenario: AC2 L1 on one segment
    Given Mortgage case "RW-2027-000801" in region BKK and a complaint note on 2027-01-26
    When the agent runs
    Then the panel "Proposed deviations" shows X1 with its reasons, the preceding contact and the marker "Agent output"
    Then when the owner confirms X1 the S8 service raises deviation X1 with raised_by "SCREENING_AGENT" under rule R-DEV-01
    Then the case status becomes "On hold" and agent_feedback holds verdict "ACCEPTED" for item "X1" with the S8 decision log entry ID

  Scenario: AC3 Other segments
    Given hire purchase case "RW-2027-000802" in region BKK
    When the agent runs
    Then the result stays in shadow and GET /cases/{caseId}/agent-outputs returns no screening output

  Scenario: AC4 The owner rejects a proposal
    Given the agent proposes X6 on case "RW-2027-000801"
    When the owner rejects X6 with reason "Customer answered on 2027-01-25"
    Then one decision log entry holds decision "X6", agent version "SCREENING@P2/PR2", final call "REJECTED" and the reason
    Then the system raises no deviation and agent_feedback holds "REJECTED" for item "X6"

  Scenario: AC5 Reject without a reason
    When the owner rejects X6 with an empty reason
    Then the system refuses the request with 422 and MSG-P7-005

  Scenario: AC6 A low-confidence proposal
    Given the agent proposes X2 with confidence 0.72 on case "RW-2027-000803"
    When the panel loads
    Then X2 shows with the marker "Low confidence"

  Scenario: AC7 A code already open
    Given deviation X1 is open on case "RW-2027-000801"
    When the agent proposes X1 again
    Then the panel does not show X1

  Scenario: AC8 Two confirmations at once
    Given two sessions of "owner.user07" confirm X1 on case "RW-2027-000804" at the same time
    When both requests arrive
    Then one deviation X1 exists and the second request is refused with 409 and MSG-GEN-004

  Scenario: AC9 The rejection cannot be recorded
    Given the decision log writer fails
    When the owner rejects X6 with a reason
    Then the system refuses the request with 503 and MSG-P7-003 and no agent_feedback row exists

  Scenario: AC10 A proposal with scores below its condition
    Given X4 has recall 0.6000 in the evaluation of "SCREEN-S2"
    When RW-COE loads an L1 proposal with condition "recall at least 0.75 for every code"
    Then the system refuses the load with 422 and MSG-P10-001 naming "X4 recall 0.6000 below 0.75"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Mode L1 applies only where the case product group and region match the policy segment; elsewhere the mode is SHADOW | agent_policy.segment_product_group, segment_region_code (New) |
| BR2 | The agent raises nothing itself; a deviation is raised only when a person confirms the proposal | Agent catalog, screening agent "May decide alone: Nothing"; role SY-AGENT has no Case record U |
| BR3 | A confirmed proposal is raised through S8 with raised_by SCREENING_AGENT, and R-DEV-01 pauses the stage clock and routes the case | R-DEV-01; LOV-RAISED-BY |
| BR4 | A rejection needs a reason and writes a decision log entry before the feedback is stored | CTL-07; Principle 5; R-UNI-39 |
| BR5 | A proposal for a code already open is not shown | deviation.deviation_code |
| BR6 | A proposal below the floor 0.80 is shown with the marker "Low confidence" | agent_policy.confidence_floor (New); FEAT-DVH-08 |
| BR7 | An L1 proposal must meet its stated conditions on the named evaluation | Principle 1; CTL-08 |

## 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ANY_STATE | DEVIATION_FLAGGED | The owner confirms a proposal; deviation_code in X1 to X7 (R-DEV-01, applied by S8) | DEV_FLAGGED |
| New, Assigned, In progress, any Waiting | Deviation flagged | As above | On hold |

A rejected proposal changes no case status.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Reads proposals for cases in scope (Case record R); confirms or rejects (Case record U) |
| SY-AGENT | Runs the agent (read only) |
| S8 deviation service, under the owner's identity | Raises the deviation and writes its decision log entry |
| RW-COE | Runs the evaluation and loads the L1 proposal (Rules and parameters C) |
| RW-RISK | Approves the L1 proposal (Rules and parameters A) |
| RW-CONDUCT | Reads scores (Rules and parameters R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-CAS-037 | deviation | case_id | Write (through the S8 interface) |
| DF-CAS-038 | deviation | deviation_code | Write (through the S8 interface) |
| DF-CAS-040 | deviation | raised_by | Write (through the S8 interface) |
| DF-WRK-012 | assignment | assignee_user_id | Read (owner check through P3) |
| DF-ACE-193 | v_ace_valuation | appraisal_date | Read (X7 collateral event inputs) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (rejections, through the P7 DecisionLogWriter) |
| DF-AGT-036 | agent_run | id | Read |
| DF-AGT-038 | agent_run | agent_version | Read |
| DF-AGT-043 | agent_run | autonomy_mode | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-049 | agent_run | output | Read |
| DF-AGT-050 | agent_run | confidence | Read |
| DF-AGT-059 | agent_run | segment_product_group | Read |
| DF-AGT-060 | agent_run | segment_region_code | Read |
| DF-AGT-098 | agent_feedback | agent_run_id | Write |
| DF-AGT-099 | agent_feedback | item_key | Write |
| DF-AGT-100 | agent_feedback | verdict | Write |
| DF-AGT-101 | agent_feedback | reason | Write |
| Standard column | agent_feedback | created_by | Write |
| Standard column | agent_feedback | created_at | Write |
| DF-AGT-102 | agent_feedback | decision_log_id | Write |
| DF-AGT-003 | agent_policy | policy_version | Write |
| DF-AGT-008 | agent_policy | autonomy_mode | Write |
| DF-AGT-009 | agent_policy | segment_product_group | Write |
| DF-AGT-010 | agent_policy | segment_region_code | Write |
| DF-AGT-017 | agent_policy | evaluation_run_id | Write |
| DF-AGT-018 | agent_policy | promotion_conditions | Write |
| DF-AGT-089 | agent_evaluation | label_key | Write |
| DF-AGT-090 | agent_evaluation | sample_size | Write |
| DF-AGT-095 | agent_evaluation | precision_value | Write |
| DF-AGT-096 | agent_evaluation | recall_value | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/cases/{caseId}/agent-outputs** (new, RWB-E2-028): returns AgentOutput items for SCREENING in mode L1 with proposals[{code, reasons, sourceRefs, precedingContactId, confidence, lowConfidence, feedback}]; Case record R; errors 401, 403, 404 (MSG-P4-003), 503.

**POST /api/recovery/v1/agent-runs/{runId}/feedback** (new, RWB-E2-028): AgentFeedbackRequest with itemKey = the code (for example "X1"), verdict ACCEPTED or REJECTED, reason (required for REJECTED); 200 AgentOutput; errors 401, 403, 404, 409 (MSG-GEN-004), 422 (MSG-P7-005), 503 (MSG-P7-003); Case record U; one feedback per run and item.

**Published interface called on ACCEPTED:**

```java
// S8, from RWB-E2-015
DeviationRaised DeviationService.raise(UUID caseId, String deviationCode, String reason,
                                       List<UUID> documentIds, String raisedBy, UUID agentRunId);
// returns deviationId and decisionLogEntryId
```

**POST /api/recovery/v1/admin/agent-evaluations** and **POST /api/recovery/v1/admin/agent-configs** (new, RWB-E1-058): evaluation of SCREEN-S2 and the L1 proposal; Rules and parameters C; approval through POST /admin/agent-configs/{versionId}/approve, Rules and parameters A.

**Events:** EV-01 CaseCreated and EV-16 DocumentStored consumed; EV-28 AgentRunCompleted published; EV-06 DeviationRaised published by S8 on confirmation.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/screening/`; front end `src/modules/recovery/agent/screening/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ScreeningShadowListener | Listener | Extended: mode per segment from the policy in force |
| ScreeningFeedbackHandler | Service | ACCEPTED: calls DeviationService.raise, stores feedback with the S8 entry ID; REJECTED: writes the decision log entry, then feedback |
| ScreeningOutputFilter | Service | Removes proposals for codes already open; sets lowConfidence |
| ProposedDeviationsPanel | React component | Panel on SCR-03: code, reasons, sources, confidence, Confirm and Reject with reason |
| AgentFeedbackService | Service | Extended with item keys for codes |

**Database:** no new table; uses agent_feedback (RWB-E2-028) and agent_policy segment fields (RWB-E1-058).

**Configuration and reference data:** policy SCREENING P2 with segment MORTGAGE and BKK, loaded by RW-COE, approved by RW-RISK; sample SCREEN-S2 loaded by RW-COE.

**Build steps**
1. Run the evaluation on SCREEN-S2 and load the L1 proposal in SIT (AC1, AC10).
2. Extend the listener for the mode per segment (AC2, AC3).
3. Build ScreeningOutputFilter (AC6, AC7).
4. Build ScreeningFeedbackHandler for both verdicts with the decision log first on rejection (AC2, AC4, AC5, AC9).
5. Add the unique key test for parallel confirmations (AC8).
6. Build ProposedDeviationsPanel with the common states.

**Feature flag:** `rwb.agent.screening-l1`. Off: every segment runs in shadow and the panel is hidden.

**Done when:** the tests in section 16 pass and UAT confirms the panel on Mortgage cases in Bangkok only.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-005 | Reject without a reason | Enter the reason you are not following the recommendation. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Second confirmation of the same proposal | Someone else changed this record. Reload it to see their change. |
| MSG-P10-001 | L1 proposal fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-S8-001 | Deviation raised after confirmation | {deviation} was raised. The case is with {handler}. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-03 Case record gains the panel "Proposed deviations" with states: empty (no panel), ready (proposals with Confirm and Reject), low confidence (marker on the proposal), recorded (verdict and date). After a confirmation SCR-03 shows the on hold banner of the deviation, and SCR-08 Deviation queue lists it for the named handler. SCR-46 Agent monitor shows SCREENING as live for MORTGAGE/BKK and Shadow elsewhere.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-029-01 | AC1, BR7 | System | SCREEN-S2 version 1, 500 cases; X1 counts 41, 4, 5 |
| TC-E2-029-02 | AC2, BR1, BR2, BR3 | System | Mortgage case RW-2027-000801 in BKK, complaint note 2027-01-26 |
| TC-E2-029-03 | AC3, BR1 | System | Hire purchase case RW-2027-000802 in BKK |
| TC-E2-029-04 | AC4, BR4 | System | Reject X6 with a reason |
| TC-E2-029-05 | AC5, BR4 | System | Reject X6 with an empty reason |
| TC-E2-029-06 | AC6, BR6 | System | X2 with confidence 0.72 |
| TC-E2-029-07 | AC7, BR5 | System | X1 already open on the case |
| TC-E2-029-08 | AC8 | System | Two parallel confirmations of X1 |
| TC-E2-029-09 | AC9, BR4 | System | Decision log writer fails on rejection |
| TC-E2-029-10 | AC10, BR7 | System | X4 recall 0.6000, condition 0.75 |
| TC-E2-029-11 | Access | Access | RW-PHONECOL confirms X1; refused with MSG-P4-002 |
| TC-E2-029-12 | Principle 5 | Resilience | Decision log write forced to fail on a rejection; nothing stored; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the segment, floor and conditions are policy values.
- No personal data in logs, tests or prompts; reasons shown on the panel hold masking tokens.
- No read of another module's tables; deviations are raised only through the S8 interface.
- The agent never raises a deviation without a person's confirmation.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-AGT-08, FEAT-DVH-07 | 11 Handle customer care and deviations | R-UNI-39 | TC-E2-029-01, TC-E2-029-03, TC-E2-029-04, TC-E2-029-05, TC-E2-029-06, TC-E2-029-09, TC-E2-029-10, TC-E2-029-12 |
| REQ-DVH-006 | A deviation flag is visible on the case and in every queue | Business Requirements Program, section 5.15 | FEAT-DVH-07 | 11 Handle customer care and deviations | R-DEV-01 | TC-E2-029-02, TC-E2-029-07, TC-E2-029-08, TC-E2-029-11 |

## 19. Out of scope

- L1 on further segments (a later policy version; FEAT-AGT-12, Epic 3).
- The deviation flows after the flag (S8, Epic 7).
- The agent handling X6 and X7 within policy (R-DEV-06, Epic 7).
