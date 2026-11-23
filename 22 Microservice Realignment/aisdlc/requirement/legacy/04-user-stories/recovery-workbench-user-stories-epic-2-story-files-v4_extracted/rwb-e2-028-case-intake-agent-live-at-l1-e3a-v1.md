<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 028 Case intake agent live at L1 E3a v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 028 Case intake agent live at L1 E3a v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-028 Case intake agent live at L1 [E3a]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-028 |
| Epic | E3, release 31 January 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-07 Run the case intake agent at L1 |
| Requirement IDs | REQ-DRI-001, REQ-ACA-005 |
| BRD section | Business Requirements Program, sections 5.7 and 5.4 |
| L3 process | 06 Take over and own the case |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-061, RWB-E1-035, RWB-E1-027, RWB-E2-031 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case intake summary and gap flags shown on the case record for every new case, marked as agent output, with a control to accept, correct or reject it**, so that **I start from a summary instead of reading every file, and the bank measures how often the summary is right**.

## 2. Business rationale

A case owner reads accounts, documents, appraisals and contact points before the first action on a new case. After the shadow results and the approved L1 proposal (RWB-E1-061), the intake summary is shown to the owner, who decides what to do with it. Each accept, correction or rejection is recorded as a decision with the agent and prompt versions (REQ-DRI-001), so acceptance and correction rates are measured by segment. Personal data stays masked in the agent call and in the stored summary (REQ-ACA-005).

## 3. Preconditions

- RWB-E1-061 is done and policy "INTAKE" version "P2" with mode L1 is approved by RW-RISK, valid from 2027-01-25.
- RWB-E1-035 is done: SCR-03 Case record shows the history timeline.
- RWB-E1-027 is done: the P7 DecisionLogWriter is available.
- RWB-E2-031 is done: GET /admin/agent-metrics and SCR-46 show acceptance by segment.
- The case owner holds RW-CASEOWN with Case record CRU and the case is in their scope.

## 4. Flow

1. SY-CASEWF: creates case "RW-2027-000501" and writes EV-01 CaseCreated.
2. System: runs agent "INTAKE" in mode L1 through the orchestrator and stores the summary and gap flags on the agent run.
3. Case owner: opens SCR-03 Case record for the case.
4. System: loads the case record and, without waiting on the model, calls GET /cases/{caseId}/agent-outputs for the stored L1 output.
5. System: shows the panel "Agent summary" with the agent name, the version "INTAKE@P2/PR3", the gap flags with reasons and the controls Accept, Correct and Reject.
6. Case owner: chooses Accept, or Correct or Reject with a reason.
7. System: writes one decision log entry (decision D6, agent version, recommendation reference, final call ACCEPTED, CORRECTED or REJECTED, reason), then stores the feedback on the agent run.
8. System: the panel shows the recorded verdict; the next JOB-15 run counts it in the acceptance and correction rates by segment.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent timed out or failed a guardrail for the case | The case record loads with no summary; the panel shows the message; the miss is on the agent run | MSG-P10-005 | AC3 |
| X2 | The owner corrects or rejects without a reason | Refused with 422; nothing stored | MSG-P7-005 | AC4 |
| X3 | The decision log write fails on feedback | Feedback not stored; panel keeps the controls; incident raised (R-UNI-39) | MSG-P7-003 | AC5 |
| X4 | Feedback already given, or two owners send at once | Second request refused with 409 | MSG-GEN-004 | AC6 |
| X5 | The case is outside the user's scope | Refused with 404 | MSG-P4-003 | AC7 |
| X6 | The agent's mode is SHADOW for the case segment | No output returned; no panel | None to a user | AC8 |
| X7 | The run used data older than the business date | Panel shows the stale warning with the data date | MSG-P1-001 | AC9 |
| X8 | A role without Case record U sends feedback | Refused with 403 | MSG-P4-002 | TC-E2-028-10 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the stored runs of RWB-E1-059, the approved L1 policy of RWB-E1-061 and the metrics of RWB-E2-031 |
| Negotiable | Panel layout and wording follow the design system; verdicts and the mode per segment are data |
| Valuable | Saves the owner the first read of every file on a new case and measures the summary's accuracy |
| Estimable | Two endpoints, one panel, one decision log mapping, one migration |
| Small | One back end and one front end developer for two weeks |
| Testable | Each criterion is a system or browser test with synthetic cases |

## 7. Acceptance criteria

```gherkin
Feature: Case intake agent live at L1 [E3a]

  Background:
    Given policy "INTAKE" version "P2" with mode "L1" and prompt "PR3" is in force from 2027-01-25
    Given case owner "owner.user07" holds RW-CASEOWN and owns case "RW-2027-000501"

  Scenario: AC1 Summary shown
    Given a new case "RW-2027-000501" with an ANSWERED intake run and gap flags MISSING_DOCUMENT and NO_VALID_APPRAISAL
    When the case record view loads
    Then the panel "Agent summary" shows the summary, the two gap flags with reasons, agent "INTAKE", version "INTAKE@P2/PR3" and the marker "Agent output"
    Then the controls Accept, Correct and Reject are shown
    Then the case record loads in under 2 seconds whether or not the panel has data

  Scenario: AC2 Acceptance measured
    Given a month of summaries in January 2027 for segment MORTGAGE and BKK: 300 with feedback, 240 accepted, 45 corrected and 15 rejected
    When the dashboard refreshes after JOB-15
    Then SCR-46 shows for "INTAKE" and MORTGAGE/BKK acceptance rate 0.8000 and correction rate 0.1500
    Then each feedback has one decision log entry with decision "D6" and agent version "INTAKE@P2/PR3"

  Scenario: AC3 Fallback
    Given the agent timed out for case "RW-2027-000502"
    When the view loads
    Then the case shows without a summary and the panel shows MSG-P10-005
    Then the agent run holds status "TIMED_OUT" and fallback true

  Scenario: AC4 Correction without a reason
    When "owner.user07" chooses Correct on case "RW-2027-000501" with an empty reason
    Then the system refuses the request with 422 and MSG-P7-005
    Then no decision log entry and no feedback are stored

  Scenario: AC5 The decision cannot be recorded
    Given the decision log writer fails
    When "owner.user07" chooses Accept
    Then the system refuses the request with 503 and MSG-P7-003
    Then no agent_feedback row exists for the run and the controls stay on the panel

  Scenario: AC6 Feedback given twice
    Given "owner.user07" accepted the summary of case "RW-2027-000501"
    When a second feedback request for the same run arrives
    Then the system refuses it with 409 and MSG-GEN-004
    Then one decision log entry exists for the run

  Scenario: AC7 A case outside the user's scope
    Given case "RW-2027-000601" belongs to team "HP-NE" outside the scope of "owner.user07"
    When "owner.user07" requests GET /cases/{caseId}/agent-outputs for it
    Then the system refuses the request with 404 and MSG-P4-003

  Scenario: AC8 A segment still in shadow
    Given the INTAKE policy for segment UNSECURED is mode "SHADOW"
    When the owner opens unsecured case "RW-2027-000701"
    Then GET /cases/{caseId}/agent-outputs returns an empty list and no panel is shown

  Scenario: AC9 Stale input
    Given the run for case "RW-2027-000503" used data as of 2027-01-26 and the business date is 2027-01-28
    When the view loads
    Then the panel shows MSG-P1-001 with the date 2027-01-26 above the summary
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only runs in mode L1 for the case segment are returned to a user; shadow output is never returned | agent_policy.autonomy_mode, segment fields (New) |
| BR2 | Agent output is marked "Agent output" with the agent name and version | REQ-DRI-001; labels "Agent version" |
| BR3 | Feedback writes one decision log entry before it is stored: decision D6 (LOV-DECISION, assumed code), agent version, recommendation reference, final call, reason | Principle 5; R-UNI-39; CTL-06 |
| BR4 | A correction or a rejection needs a reason | CTL-07; MSG-P7-005 |
| BR5 | One feedback per run and item; the intake summary is item "SUMMARY" | agent_feedback unique key (New) |
| BR6 | The case record never waits for the model; the panel reads stored output | NFR-009; R-UNI-32 |
| BR7 | The summary holds masking tokens only | CTL-11 |

## 9. State transitions

None. This story does not change a case status. It writes one agent_feedback row (verdict ACCEPTED, CORRECTED or REJECTED) and one decision log entry per feedback.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Reads the panel for cases in scope (Case record R); gives feedback (Case record U) |
| RW-TEAMMGR | Reads the panel for team cases (Case record R); no feedback |
| SY-AGENT | Runs the agent (read only) |
| SY-DECLOG | Writes the entry |
| RW-COE | Reads acceptance on SCR-46 (Platform administration R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-011 | recovery_case | team_code | Read (scope) |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-WRK-012 | assignment | assignee_user_id | Read (owner check through P3) |
| DF-DOC-004 | document | document_type | Read (gap reasons) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (through the P7 DecisionLogWriter) |
| DF-AGT-036 | agent_run | id | Read |
| DF-AGT-037 | agent_run | agent_code | Read |
| DF-AGT-038 | agent_run | agent_version | Read |
| DF-AGT-043 | agent_run | autonomy_mode | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-049 | agent_run | output | Read |
| DF-AGT-050 | agent_run | confidence | Read |
| DF-AGT-055 | agent_run | data_as_of | Read |
| DF-AGT-056 | agent_run | run_at | Read |
| DF-AGT-097 | agent_feedback | id | Write |
| DF-AGT-098 | agent_feedback | agent_run_id | Write |
| DF-AGT-099 | agent_feedback | item_key | Write |
| DF-AGT-100 | agent_feedback | verdict | Write |
| DF-AGT-101 | agent_feedback | reason | Write |
| Standard column | agent_feedback | created_by | Write |
| Standard column | agent_feedback | created_at | Write |
| DF-AGT-102 | agent_feedback | decision_log_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /api/recovery/v1/cases/{caseId}/agent-outputs** (new, see additions)
- Request: path caseId (uuid).
- Response: 200, array of AgentOutput (runId, agent, agentVersion, mode "L1", status, summary, gaps[{gapType, reason}], confidence, dataAsOf, feedback). Empty array when no L1 output exists.
- Errors: 401; 403 (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 503.
- Authorization: Case record, R, scope applied. Idempotency: read only.

**POST /api/recovery/v1/agent-runs/{runId}/feedback** (new)
- Request: AgentFeedbackRequest (itemKey, default "SUMMARY"; verdict ACCEPTED, CORRECTED or REJECTED; reason, required for CORRECTED and REJECTED, at most 1,000 characters); header If-Match with the run row version.
- Response: 200 AgentOutput with feedback set.
- Errors: 401; 403; 404; 409 feedback exists or row changed (MSG-GEN-004); 422 reason missing (MSG-P7-005); 503 decision not recorded (MSG-P7-003).
- Authorization: Case record, U, scope applied. Idempotency: one feedback per run and item (itemKey, default "SUMMARY"); a repeat returns 409.

**Decision log mapping:** case_id; decision_code "D6"; agent_version "INTAKE@P2/PR3"; model_version; inputs_ref = agent run reference; recommendation = {"runId", "gaps"}; final_call = verdict; override_reason = reason; approver_user_id = the owner.

**Events:** EV-01 CaseCreated consumed; EV-28 AgentRunCompleted published by the orchestrator; EV-08 DecisionRecorded published by P7.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/intake/`; front end `src/modules/recovery/agent/intake/`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAgentOutputController | Controller | GET /cases/{caseId}/agent-outputs and POST /agent-runs/{runId}/feedback |
| AgentFeedbackService | Service | Validates, writes the decision log entry, then stores feedback in one transaction |
| AgentOutputQueryService | Service | Returns L1 outputs for a case after the P3 scope check |
| IntakeShadowListener | Listener | Extended: uses the mode of the policy in force for the segment (SHADOW or L1) |
| AgentSummaryPanel | React component | Panel on SCR-03 with marker, version, gaps, controls and states |

**Database:** migration `V10_008__agent_feedback.sql` creates agent_feedback (id, agent_run_id, item_key varchar(20), verdict varchar(10), reason varchar(1000), created_by uuid, created_at timestamptz, decision_log_id uuid, standard record columns) with unique (agent_run_id, item_key) and check verdict in ('ACCEPTED','CORRECTED','REJECTED').

**Configuration and reference data:** policy INTAKE P2 (mode L1 per segment) loaded by RW-COE and approved by RW-RISK; panel labels in the label standard (DL10 for Thai).

**Build steps**
1. Create the agent_feedback table with its unique key and check constraint.
2. Build AgentOutputQueryService with the P3 scope check and the mode filter (AC1, AC7, AC8).
3. Build AgentFeedbackService with the decision log write first (AC2, AC4, AC5, AC6).
4. Build CaseAgentOutputController and the problem responses.
5. Build AgentSummaryPanel: loading, empty, unavailable (MSG-P10-005), stale (MSG-P1-001), feedback given (AC1, AC3, AC9).
6. Browser test: case record load time with the panel under 2 seconds on 50 documents.

**Feature flag:** `rwb.agent.intake-l1`. Off: GET /cases/{caseId}/agent-outputs returns an empty list and the panel is hidden.

**Done when:** the tests in section 16 pass and SCR-46 shows acceptance by segment for the UAT cases.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-005 | No L1 summary for the case because the run failed | The agent summary is not available for this case. Work from the case record. |
| MSG-P7-005 | Correct or Reject with no reason | Enter the reason you are not following the recommendation. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Feedback already given or row changed | Someone else changed this record. Reload it to see their change. |
| MSG-P4-003 | Case outside scope | This case is not in your scope. |
| MSG-P1-001 | Summary built on stale data | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-03 Case record (states loading, read only, editable, on hold) gains the panel "Agent summary". Panel states: loading (skeleton), empty (no panel when no L1 output), unavailable (MSG-P10-005), stale (MSG-P1-001 above the summary), ready (summary, gaps, Accept, Correct, Reject), recorded (verdict and date, no controls). In the read only state of SCR-03 the controls are hidden. SCR-46 Agent monitor (state live) shows the acceptance and correction rates.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-028-01 | AC1, BR1, BR2, BR6 | System | Case RW-2027-000501 with an ANSWERED run and two gaps |
| TC-E2-028-02 | AC2, BR3 | System | January 2027, MORTGAGE/BKK: 300 feedback, 240, 45, 15 |
| TC-E2-028-03 | AC3, BR6 | System | Case RW-2027-000502 with a TIMED_OUT run |
| TC-E2-028-04 | AC4, BR4 | System | Correct with an empty reason |
| TC-E2-028-05 | AC5, BR3 | System | Decision log writer fails on Accept |
| TC-E2-028-06 | AC6, BR5 | System | Second feedback on the same run |
| TC-E2-028-07 | AC7 | System | Case RW-2027-000601 in team HP-NE |
| TC-E2-028-08 | AC8, BR1 | System | Unsecured case RW-2027-000701, segment in SHADOW |
| TC-E2-028-09 | AC9 | System | Data as of 2027-01-26, business date 2027-01-28 |
| TC-E2-028-10 | Access | Access | RW-PHONECOL (Case record R only) sends feedback; refused with MSG-P4-002 |
| TC-E2-028-11 | Principle 5 | Resilience | Decision log write forced to fail on feedback; no feedback stored; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the mode per segment and the verdict list are data.
- No personal data in logs, tests or prompts; the summary shows masking tokens.
- No read of another module's tables; scope and owner come through the P3 interface.
- Agent output never changes the case: no status, task or field is set from the summary.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records the agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32, R-UNI-39 | TC-E2-028-01, TC-E2-028-02, TC-E2-028-03, TC-E2-028-04, TC-E2-028-05, TC-E2-028-06, TC-E2-028-09, TC-E2-028-11 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Business Requirements Program, section 5.4 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E2-028-07, TC-E2-028-08, TC-E2-028-10 |

## 19. Out of scope

- Agent actions taken without the owner (autonomy L2 and above, Epic 8).
- Editing the summary text in the Workbench; a correction records the reason only.
- Intake document classification (P5 stories).
