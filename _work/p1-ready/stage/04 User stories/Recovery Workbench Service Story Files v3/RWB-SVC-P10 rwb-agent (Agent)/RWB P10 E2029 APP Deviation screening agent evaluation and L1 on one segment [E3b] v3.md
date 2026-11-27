# RWB-P10-E2029-APP Deviation screening agent evaluation and L1 on one segment [E3b]

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2029-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P10-E2029-APP-16); the squad sizes it at refinement |
| Patterns applied | DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1062-APP |
| Depends on (build) | RWB-P10-E2029-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-N001-CON, RWB-P10-E1062-APP, RWB-P10-E1061-CON, RWB-P10-E2028-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E2015-CON |
| Contract version | v1, base path `/api/recovery/agent/v1` (as stated in RWB-P10-E2029-CON) |
| Readiness decisions | RD-P1-004 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-007, FR-P10-012, FR-P10-013, FR-P10-014) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E2-029 for rwb-agent. The business behaviour of the legacy story is kept whole - the evaluation of the screening agent on sample "SCREEN-S2" version 1 over 500 cases, the L1 proposal for segment MORTGAGE and region BKK, the mode per segment, the panel "Proposed deviations", the confirm path through the S8 deviation service under R-DEV-01, the reject path with its reason and its decision record, the confidence floor 0.80, the codes X1 to X7, the ten criteria and the twelve test cases. Only the seams move: the two E3 operations are served on the base `/api/recovery/agent/v1` (DP-13) with the shape baselined in RWB-P10-E1058-CON and published for E3 by RWB-P10-E2028-CON; the sample, the runs, the scores, the policy rows and the feedback stay in schema `rwb_agent`; the decision log becomes the local decision-record library on the shared topic `rwb.decision-record.v1` (DP-03); the ACE collateral input of X7 is read through rwb-source-data or the service's own read-only view (DP-05); the floor, the segment values and the promotion condition are read from the rwb-case parameters and reference data (DP-06, DP-07); the outbox follows the platform envelope (DP-09); the legacy in-process `DeviationService.raise`, the case read, the owner check and the ledger become REST contracts with a mock, one hop and a 2 s budget (DP-11); and the panel is reached through the gateway-bff route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E2029-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (29 resolved, 17 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **conduct and QA officer (RW-CONDUCT)**, I want **the deviation screening agent scored on 500 shadow cases and switched to L1 for Mortgage cases in Bangkok, with its proposed X flags shown on the panel "Proposed deviations" of SCR-03 Case record to the case owner to confirm or reject, each confirmation raised as a deviation through the rwb-deviation service under R-DEV-01 and each rejection written as a decision record before the feedback is stored**, so that **deviations on that segment are flagged from the first day a sign appears and the error rate per flag is known**.

### 2. Business rationale

A deviation found weeks late means contact that should have stopped and clocks that should have paused. The shadow results of RWB-E1-062 give a measured precision and recall per code. This story scores a larger shadow run, records the proposal to go to L1 on one segment, and then shows the agent's proposals to the owner of each Mortgage case in Bangkok, who confirms or rejects each one. A confirmed proposal raises the deviation through the S8 deviation service, so the flag shows on the case and in every queue (REQ-DVH-006), and detection draws on case data, call notes and documents (REQ-DVH-001). Every other segment stays in shadow.

The legacy key was written inside one deployment; the target moves four seams and changes no business value:

- The runs, the scores, the policy versions and the feedback are P10 rows of `rwb_agent`, created by the earlier P10 stories; this story adds no table and no migration.
- The decision record of a rejection is written by the local library of DP-03 and published on `rwb.decision-record.v1`; rwb-decision owns the central ledger and seals the entry.
- The deviation service, the case of record, the owner check and the interaction ledger are other services; rwb-agent reaches each by one REST hop against its published contract and its fake, inside the 2 s client budget.
- The floor, the segment values, the condition and the seven codes are rows of the policy, the parameters and the reference data of rwb-case, read at run time and written nowhere in code.

The cross-service behaviour of this key - that a confirmation really raises one deviation and really moves the case to "On hold" under R-DEV-01, that the record is sealed in rwb-decision, and that the panel really reads the case facts - is proved by the wave 2 integration work of RWB-ITG-W2, which is why the story carries no integration dependency.

### 3. Preconditions

- RWB-P10-E1062-APP is done: agent "SCREENING" runs in shadow from EV-01 CaseCreated and EV-16 DocumentStored, and stores one run per case and event with its proposed codes, their reasons, their source references, the preceding contact reference and their confidence.
- RWB-P10-E2029-CON is published: the screening narrowing of the evaluation start and the report, the score row shape per code, the policy payload with the two segment members and its approval, the decision-record mapping, the two event contracts, the error taxonomy and the fakes.
- RWB-P10-E2028-CON is published: the E3 operations `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` with its `proposals[]` member and `POST /api/recovery/agent/v1/agent-runs/{runId}/feedback`. This story restates them and adds no member.
- RWB-P10-E1061-CON is published: the evaluation start, the list and the report, and the L1 proposal payload with its condition check and its approval, reused here for agent "SCREENING" and policy "SCREENING" version "P2".
- RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON are published: the decision-record library and shared topic, the parameters and reference-data client libraries, the outbox and inbox library with the CloudEvents envelope, and the gateway-bff route contract with its stub.
- The rwb-case contracts are published: `GET /api/recovery/case/v1/cases/{caseId}` (RWB-P3-E2015-CON), the parameters (RWB-P3-E1042-CON) and the lists (RWB-P3-E1043-CON).
- The rwb-deviation raise and open-deviation reads are consumed as REST contracts with a mock, one hop and the 2 s budget (DP-11); the story of the S8 slice that publishes the raise is Not specified in the source documents (GAP-0625; ASM-0931).
- The L1 proposal checks exist in the policy loader of RWB-P10-E1061-CON, reused with the screening agent and its evaluation run.
- Sample "SCREEN-S2" version 1 holds the business analysts' review of 500 shadow cases, loaded through `POST /api/recovery/agent/v1/admin/agent-samples` of RWB-P10-E1058-APP.
- The case owner holds RW-CASEOWN (Case record CRU) and the case is in scope.
- The per-service login of rwb-agent under DP-02 is Not specified in the source documents (GAP-0625; ASM-0930); the story names it "the rwb-agent login (DP-02)" until it is agreed, and SY-AGENT stays the actor name of the run.
- The release date 31 January 2027 is tentative and is copied unchanged.

### 4. Flow

1. RW-COE starts the evaluation of "SCREENING" on "SCREEN-S2" version 1 through `POST /api/recovery/agent/v1/admin/agent-evaluations` of RWB-P10-E1061-CON (AC1).
2. The harness scores the 500 shadow cases and the service stores one `agent_evaluation` row per code X1 to X7 with the sample size, the true positives, the false positives, the false negatives, precision and recall (AC1; BR7).
3. `ScreeningEvaluationReporter` reads the run row and its score rows and confirms the counts: X1 with 41 true positives, 4 false positives and 5 false negatives gives precision 0.9111 and recall 0.8913 (AC1).
4. RW-COE loads policy "SCREENING" version "P2" with prompt "PR2", mode L1 for segment MORTGAGE and region BKK, the evaluation run, the promotion condition, the fallback rule and the watch measures through `POST /admin/agent-configs`; the promotion check reads the parameters and the lists of rwb-case at run time and refuses the load on a failed condition (DP-06, DP-07; AC1, AC10).
5. RW-RISK approves it through `POST /admin/agent-configs/{versionId}/approve`; the row stays LOADED until then and the version in force keeps serving (AC1).
6. `ScreeningModeListener` consumes EV-01 CaseCreated from `rwb.case.events.v1` and EV-16 DocumentStored from `rwb.document.events.v1`, dedupes on the event ID in the inbox, and `ResolveScreeningMode` reads `agent_policy.segment_product_group` and `agent_policy.segment_region_code` of the approved row: a Mortgage case in region BKK runs in L1, every other segment in shadow (BR1; AC2, AC3).
7. The run path of RWB-P10-E1062-APP assembles the masked inputs - the case facts, the open deviations, the ledger entries of the window and the documents with their masked fields - calls the model and stores one `agent_run` row with its proposals, their reasons, their sources, the preceding contact reference and their confidence (AC2, AC3, AC6, AC7).
8. The case owner opens SCR-03 through the gateway-bff route; `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` answers `AgentOutput[]` and the panel lists each proposed code with its reasons, its sources, its confidence and the marker "Agent output" (DP-19; AC2).
9. `ScreeningOutputFilter` drops a proposal whose code is already open on the case, read through the rwb-deviation contract, and sets the marker "Low confidence" on a proposal below the floor 0.80 of the policy in force (AC6, AC7).
10. The owner confirms a proposal: `ScreeningFeedbackHandler` calls the raise of rwb-deviation with the case ID, the code, the reason, the document IDs of the sources, `raisedBy` "SCREENING_AGENT" and the run ID, the return point, the agent version and the policy segment pair (fields Not specified in the source documents (GAP-3100)), receives the deviation ID and the decision log entry ID, and stores `agent_feedback` with verdict ACCEPTED, item key the code and that entry ID (AC2; BR2, BR3).
11. The owner rejects a proposal with a reason: the handler writes the decision record first - decision the code, agent version "SCREENING@P2/PR2", final call REJECTED and the reason - through the library of DP-03 in the same transaction as the feedback, and only then stores `agent_feedback` with verdict REJECTED and the entry ID (BR4; AC4, AC5, AC9).
12. A rejection without a reason is refused with 422 and MSG-P7-005 before anything is written; a second confirmation of the same proposal is refused with 409 and MSG-GEN-004 and leaves one deviation; a decision record that cannot be written refuses the action with 503 and MSG-P7-003 and stores no feedback row (AC5, AC8, AC9).
13. Every read of another service is one hop on that service's base inside the 2 s budget; the model call keeps its own 60-second budget inside the run of RWB-P10-E1062-APP (DP-05, DP-11).

**Screen states.** SCR-03 (panel): empty - a case with no L1 run shows no screening output (12.1; AC3); no access - refused with 403 and MSG-P4-002 (X8); error - the read answers 503 with MSG-P7-003 (12.1); loading - Not specified in the source documents (DOR-RWB-P10-E2029-APP-10). SCR-08 and SCR-46: empty, loading, error and no access states are Not specified in the source documents (DOR-RWB-P10-E2029-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case is not Mortgage in region BKK | The run is in shadow; nothing is shown | None to a user | AC3 |
| X2 | Reject with no reason | Refused with 422 | MSG-P7-005 | AC5 |
| X3 | A proposal is below the confidence floor 0.80 | Shown with the marker "Low confidence" | None to a user | AC6 |
| X4 | The proposed code is already open on the case | The proposal is not shown | None to a user | AC7 |
| X5 | Two confirmations of the same proposal at once | One deviation; the second is refused with 409 | MSG-GEN-004 | AC8 |
| X6 | The decision log write fails on a rejection | Nothing stored; incident raised (R-UNI-39) | MSG-P7-003 | AC9 |
| X7 | The L1 proposal names scores below a stated condition | Policy load refused | MSG-P10-001 | AC10 |
| X8 | A role without Case record U confirms or rejects | Refused with 403 | MSG-P4-002 | AC11, AC12 |
| X9 | The parameters or the list read of rwb-case does not answer inside 2 s, or answers without the floor or the promotion condition | The load or the run is refused with 422 and MSG-P10-001 naming the missing parameter; no default and no code value is used and the version in force keeps serving | MSG-P10-001 | AC10 |
| X10 | The raise of rwb-deviation answers 503 or does not answer inside 2 s on a confirmation | The confirmation is refused with 503, no `agent_feedback` row is stored and the owner retries; rwb-agent raises no deviation of its own | None to a user | AC2, AC16 |
| X11 | The feature flag `rwb.agent.screening-l1` is off | Every segment runs in shadow and the panel is hidden, whatever the policy row says | None to a user | AC3 |

X1 to X8 are the legacy exception paths carried onto the service, with their legacy trigger, message and criterion unchanged. X9 to X11 are the failures that appear when the parameters and the lists become contracts, when the raise becomes a REST hop, and when the flag is read through the platform library instead of a local property.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reuses the screening run path (RWB-P10-E1062-APP), the evaluation contract (RWB-P10-E1061-CON), the E3 operations of RWB-P10-E2028-CON, the decision-record and outbox libraries and the three rwb-case contracts; it is the only in-lane story after RWB-P10-E1062-APP |
| Negotiable | The segment, the floor and the condition are rows of the policy and the parameters; the package, the component names and the panel layout are design |
| Valuable | Flags deviations on Mortgage cases in Bangkok when the sign appears, with a person deciding each one |
| Estimable | One evaluation report read, one mode resolver, one output filter, one feedback handler with two verdicts, one decision record, one panel, against four contract clients |
| Small | Two developers for two weeks, the legacy estimate, unchanged |
| Testable | Each of the ten criteria is one automated test on an observable: a score row, a policy row, a run row, a panel element, a deviation, a feedback row, a decision record or a refusal code |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent evaluation and L1 on one segment [E3b]

  Background:
    Given policy "SCREENING" version "P2" with prompt "PR2" has mode "L1" for segment MORTGAGE and BKK and mode "SHADOW" for every other segment
    Given case owner "owner.user07" holds RW-CASEOWN

  Scenario: AC1 Evaluation (legacy RWB-E2-029 AC1)
    Given the rwb-case parameters contract mock returns the promotion checks in force for agent "SCREENING"
    Given the shadow run on 500 cases in sample "SCREEN-S2" version 1
    When the evaluation runs
    Then precision and recall per flag X1 to X7 are stored with sample size 500
    Then for X1 with 41 true positives, 4 false positives and 5 false negatives precision is 0.9111 and recall is 0.8913
    Then the system records the L1 proposal as policy "SCREENING" version "P2" with status "LOADED", segment MORTGAGE and BKK and the evaluation run ID

  Scenario: AC2 L1 on one segment (legacy RWB-E2-029 AC2)
    Given the rwb-case contract mock returns case "RW-2027-000801" with product group MORTGAGE, region BKK and status "In progress"
    Given the rwb-source-data contract mock returns the interaction ledger of case "RW-2027-000801" with the preceding contact
    Given the rwb-deviation contract mock returns deviation X1 raised with raised_by "SCREENING_AGENT", its decision record ID and the case status "On hold" under rule R-DEV-01
    Given Mortgage case "RW-2027-000801" in region BKK and a complaint note on 2027-01-26
    When the agent runs
    Then the panel "Proposed deviations" shows X1 with its reasons, the preceding contact and the marker "Agent output"
    Then when the owner confirms X1 the S8 service raises deviation X1 with raised_by "SCREENING_AGENT" under rule R-DEV-01
    Then the case status becomes "On hold" and agent_feedback holds verdict "ACCEPTED" for item "X1" with the S8 decision record ID

  Scenario: AC3 Other segments (legacy RWB-E2-029 AC3)
    Given the rwb-case contract mock returns case "RW-2027-000802" with product group HIRE_PURCHASE and region BKK
    Given hire purchase case "RW-2027-000802" in region BKK
    When the agent runs
    Then the result stays in shadow and GET /cases/{caseId}/agent-outputs returns no screening output

  Scenario: AC4 The owner rejects a proposal (legacy RWB-E2-029 AC4)
    Given the rwb-decision contract mock returns the decision record of case "RW-2027-000801" as recorded with its entry ID
    Given the agent proposes X6 on case "RW-2027-000801"
    When the owner rejects X6 with reason "Customer answered on 2027-01-25"
    Then one decision record holds decision "X6", agent version "SCREENING@P2/PR2", final call "REJECTED" and the reason
    Then the system raises no deviation and agent_feedback holds "REJECTED" for item "X6"

  Scenario: AC5 Reject without a reason (legacy RWB-E2-029 AC5)
    When the owner rejects X6 with an empty reason
    Then the system refuses the request with 422 and MSG-P7-005

  Scenario: AC6 A low-confidence proposal (legacy RWB-E2-029 AC6)
    Given the rwb-case contract mock returns case "RW-2027-000803" with product group MORTGAGE and region BKK
    Given the agent proposes X2 with confidence 0.72 on case "RW-2027-000803"
    When the panel loads
    Then X2 shows with the marker "Low confidence"

  Scenario: AC7 A code already open (legacy RWB-E2-029 AC7)
    Given the rwb-deviation contract mock returns deviation X1 open on case "RW-2027-000801"
    Given deviation X1 is open on case "RW-2027-000801"
    When the agent proposes X1 again
    Then the panel does not show X1

  Scenario: AC8 Two confirmations at once (legacy RWB-E2-029 AC8)
    Given the rwb-deviation contract mock returns one deviation X1 for case "RW-2027-000804" and 409 MSG-GEN-004 for the second raise
    Given two sessions of "owner.user07" confirm X1 on case "RW-2027-000804" at the same time
    When both requests arrive
    Then one deviation X1 exists and the second request is refused with 409 and MSG-GEN-004

  Scenario: AC9 The rejection cannot be recorded (legacy RWB-E2-029 AC9)
    Given the decision record writer fails
    When the owner rejects X6 with a reason
    Then the system refuses the request with 503 and MSG-P7-003 and no agent_feedback row exists

  Scenario: AC10 A proposal with scores below its condition (legacy RWB-E2-029 AC10)
    Given the rwb-case parameters contract mock returns the promotion checks in force for agent "SCREENING"
    Given X4 has recall 0.6000 in the evaluation of "SCREEN-S2"
    When RW-COE loads an L1 proposal with condition "recall at least 0.75 for every code"
    Then the system refuses the load with 422 and MSG-P10-001 naming "X4 recall 0.6000 below 0.75"

  Scenario: AC11 A role without Case record U confirms or rejects (legacy RWB-E2-029 test TC-E2-029-11, X8) (new, D-RCV-60)
    Given the agent proposes X1 on case "RW-2027-000801"
    When a user without Case record U ("RW-PHONECOL") confirms X1
    Then the system refuses the request with 403 and MSG-P4-002

  Scenario: AC12 A role without Case record U rejects (new, D-RCV-60)
    Given the agent proposes X1 on case "RW-2027-000801"
    When a user without Case record U ("RW-PHONECOL") rejects X1 with reason "Customer answered on 2027-01-25"
    Then the system refuses the request with 403 and MSG-P4-002

  Scenario: AC13 Boundary rules of the service (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2027-000801" with product group MORTGAGE, region BKK and status "In progress"
    When the agent runs
    Then the mode is resolved from the approved policy row of rwb_agent and the case facts read through the rwb-case contract
    Then the rejection decision record is written by the local library in the same transaction as the feedback and published on rwb.decision-record.v1
    Then the collateral appraisal date of an X7 proposal is read through rwb-source-data (DP-05) and never from an ACE table or a v_ace_* view
    Then the floor, the promotion condition and the segment values are read from the rwb-case parameters with their version
    Then every read of another service is one hop with a 2 s client budget
    Then the panel is reached through the gateway-bff route and no screen calls the service directly

  Scenario: AC14 Error answers of the provided operations (new, D-RCV-60)
    Given no session is presented to GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs
    When the panel reads the agent outputs
    Then the system answers 401 with MSG-P4-001 and returns no output
    Given the caller has no Case record U
    When the caller posts a verdict to POST /api/recovery/agent/v1/agent-runs/{runId}/feedback
    Then the system answers 403 and MSG-P4-002
    Given the caller has Case record U and run "{runId}" does not exist
    When the caller posts a verdict to POST /api/recovery/agent/v1/agent-runs/{runId}/feedback
    Then the system answers 404 with MSG-P4-003 and stores no agent_feedback row

  Scenario: AC15 Replay of a write with the same idempotency key (new, D-RCV-60)
    Given the owner confirms X1 on case "RW-2027-000801" with an idempotency key
    When the same confirmation is replayed with the same idempotency key
    Then the system returns the outcome of the first request and raises no second deviation
    Then no second agent_feedback row exists

  Scenario: AC16 Retry and timeout of a call to rwb-deviation (new, D-RCV-60)
    Given the rwb-deviation contract mock does not answer inside 2 s on a confirmation of X1
    When the owner confirms X1 on case "RW-2027-000801"
    Then the system refuses the confirmation with 503, stores no agent_feedback row and raises no deviation
    Then the owner retries the confirmation as a new request
```

**Target reading.** The segment MORTGAGE and region BKK, policy "SCREENING" version "P2", prompt "PR2", sample "SCREEN-S2" version 1, the 500 cases, the counts 41, 4 and 5, the scores 0.9111 and 0.8913, the cases "RW-2027-000801" to "RW-2027-000804", the complaint note of 2027-01-26, the rejection reason, the confidence 0.72, the floor 0.80, the recall 0.6000 against the condition 0.75, the statuses "LOADED", "On hold", "ACCEPTED" and "REJECTED", the agent version "SCREENING@P2/PR2", the codes X1 to X7, R-DEV-01, R-UNI-39 and the messages MSG-P7-005, MSG-P7-003, MSG-GEN-004, MSG-P10-001 and MSG-P4-002 are the legacy values of RWB-E2-029, copied character for character. The ten scenario titles and every legacy Given, When and Then are kept, and each carries the origin tag of its legacy criterion. The one change of wording is that the criteria say decision record where the legacy text says decision log.

Each scenario whose content crosses a service boundary gained one or more inserted Givens of the form `Given the <service> contract mock returns <x>`, and nothing the service owns is mocked. AC1 and AC10 read the promotion checks through the rwb-case parameters contract. AC2 reads the case facts and the status through the P3 contract, the preceding contact through the rwb-source-data contract (DP-05) and the raised deviation with its entry ID through the rwb-deviation contract. AC3 and AC6 read the case facts through the P3 contract. AC4 reads the recorded entry back from rwb-decision, which seals what the local library writes. AC7 and AC8 read the open deviations and the raise outcome through the rwb-deviation contract. AC5 and AC9 cross no boundary: the reason check and the record write are the service's own. The window of the screening read is the one fixed by RWB-P10-E1062-APP and read through the parameters; the legacy criteria name no window and this story sets none. No deviation, screening or queue volume is stated for this module: the only quantities are the evaluation samples of 200 and 500 cases, and no source states the deviations open at go-live, the screening runs a night, the deviation queue size or the rule evaluations per screen. The platform figures are 23,600 open cases at go-live and 3,110 new a month (NFR-001), about 370 staff online of 914 (NFR-002) and 300 milliseconds per rule evaluation (NFR-011); the 05:00 to 07:00 morning run includes rwb-deviation (Architecture v5 slide 33). No volume target is set here; the real deviation rate is measured in the shadow run before the wave 2 volume test is sized.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Mode L1 applies only where the case product group and region match the policy segment; elsewhere the mode is SHADOW | agent_policy.segment_product_group, segment_region_code (DF-AGT-009, DF-AGT-010); legacy BR1 |
| BR2 | The agent raises nothing itself; a deviation is raised only when a person confirms the proposal | Agent catalog, screening agent "May decide alone: Nothing"; SY-AGENT has no Case record U; legacy BR2 |
| BR3 | A confirmed proposal is raised through S8 with raised_by SCREENING_AGENT, and R-DEV-01 pauses the stage clock and routes the case | R-DEV-01; R-DEV-19 to R-DEV-21 from the design (rule package and promotion stay in rwb-decision); LOV-RAISED-BY; legacy BR3 |
| BR4 | A rejection needs a reason and writes a decision record before the feedback is stored | CTL-07; Principle 5; R-UNI-39; legacy BR4 |
| BR5 | A proposal for a code already open is not shown | deviation.deviation_code (DF-CAS-038); legacy BR5 |
| BR6 | A proposal below the floor 0.80 is shown with the marker "Low confidence" | agent_policy.confidence_floor (DF-AGT-011); FEAT-DVH-08; legacy BR6 |
| BR7 | An L1 proposal must meet its stated conditions on the named evaluation | Principle 1; CTL-08; legacy BR7 |
| BR8 | The mode of a run is resolved from the approved policy row of `rwb_agent` and the case facts read through the rwb-case contract; no other service decides the mode | DP-01; DP-11; ownership of `agent_policy` |
| BR9 | The decision record of a rejection is written by the local library in the same transaction as the feedback and published on `rwb.decision-record.v1`; rwb-decision owns the central ledger and seals the entry | DP-03; ADR-022; R-UNI-39 |
| BR10 | ACE facts - the collateral appraisal date of an X7 proposal - are read through the rwb-source-data contract or the service's own read-only `v_ace_*` view, never from an ACE table and never from another service's row | DP-05; §R7.2 s17; ownership of `valuation_ext` |
| BR11 | The floor, the promotion condition and the segment values are parameters and reference data of rwb-case, read at run time with their version and never written in code | DP-06; DP-07; BR-P10-008; FSD P10 A2.8.3 |
| BR12 | Every read of another service is one hop on that service's base with a 2 s client budget; the model call keeps its own 60-second budget inside the run | DP-11; ADR-020; NFR-010 |
| BR13 | The panel is reached through the gateway-bff route and the two E3 operations are served on `/api/recovery/agent/v1`; no screen calls the service directly and no monolith base is served | DP-13; DP-19; ADR-019 |

### 9. State transitions

No case-state transition for a confirmed proposal is listed in this story. The two source rows were removed (CG-ALL-2714; CG-ALL-2715) because their From status is not a value of LOV-CASE-STATUS and Case and Workflow Model v6 has no such row.

A rejected proposal changes no case status. The state of one proposal of a run and of its feedback row:

| From | Event | Condition | To |
|---|---|---|---|
| Proposed | The panel loads | The code is already open on the case | Not shown; no feedback row |
| Proposed | The panel loads | The confidence is below the floor of the policy in force | Shown with the marker "Low confidence" |
| Proposed | The owner confirms | The raise succeeds | Deviation raised; `agent_feedback` ACCEPTED with the entry ID |
| Proposed | The owner confirms | The raise answers 409 | One deviation; 409 MSG-GEN-004; no second feedback row |
| Proposed | The owner confirms | The raise answers 503 or times out | No feedback row; the owner retries |
| Proposed | The owner rejects with a reason | The record is written | Decision record REJECTED, then `agent_feedback` REJECTED |
| Proposed | The owner rejects without a reason | The reason is empty | No write; 422 MSG-P7-005 |
| Proposed | The owner rejects with a reason | The record cannot be written | No write; 503 MSG-P7-003; incident under R-UNI-39 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN | Reads proposals for cases in scope (Case record R); confirms or rejects (Case record U) |
| SY-AGENT | Runs the agent (read only) |
| S8 deviation service, under the owner's identity | Raises the deviation and writes its decision log entry |
| RW-COE | Runs the evaluation and loads the L1 proposal (Rules and parameters C) |
| RW-RISK | Approves the L1 proposal (Rules and parameters A) |
| RW-CONDUCT | Reads scores (Rules and parameters R) |
| The rwb-agent login (DP-02) | Resolves the mode, filters the proposals, writes `agent_feedback` and the record in `rwb_agent`, and calls the P3, P1, S8 and P7 contracts |
| rwb-deviation (S8) | Owns the deviation, applies R-DEV-01 and publishes EV-06 |
| rwb-decision (P7) | Owns the central ledger, `decision_log_entry` and the sealing of a record |
| rwb-source-data (P1) | Owns the interaction ledger, the ACE view contract and the extension tables |
| rwb-case (P3) | Owns the case of record, the owner check, the parameters and the reference lists |
| rwb-access (DP-08) | Authorises each REST operation of this story before the operation runs, against the Authority rows of this section |
| No role | Reads `rwb_case`, `rwb_deviation`, `rwb_decision` or another service's schema as a table, or raises a deviation without a person's confirmation |

The login of the service is Not specified in the source documents (GAP-0625; ASM-0930) and is named with the platform at the wave 2 build start. No delegation of authority level applies; the approval of the L1 proposal is the Rules and parameters A right of RW-RISK and the separation of duty between loader and approver is the one fixed by RWB-P10-E1061-CON.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case (P3) | id | Read |
| DF-CAS-003 | recovery_case (P3) | product_group | Read |
| DF-CAS-005 | recovery_case (P3) | status | Read |
| DF-CAS-012 | recovery_case (P3) | region_code | Read |
| DF-CAS-037 | deviation (S8) | case_id | Write (through the S8 interface) |
| DF-CAS-038 | deviation (S8) | deviation_code | Write (through the S8 interface) |
| DF-CAS-040 | deviation (S8) | raised_by | Write (through the S8 interface) |
| DF-WRK-012 | assignment (P3) | assignee_user_id | Read (owner check through P3) |
| DF-ACE-193 | v_ace_valuation (P1) | appraisal_date | Read (X7 collateral event inputs) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7) | all fields | Write (rejections, through the library of DP-03) |
| DF-AGT-036 | agent_run (P10 `rwb_agent`) | id | Read |
| DF-AGT-038 | agent_run (P10 `rwb_agent`) | agent_version | Read |
| DF-AGT-043 | agent_run (P10 `rwb_agent`) | autonomy_mode | Read |
| DF-AGT-046 | agent_run (P10 `rwb_agent`) | status | Read |
| DF-AGT-049 | agent_run (P10 `rwb_agent`) | output | Read |
| DF-AGT-050 | agent_run (P10 `rwb_agent`) | confidence | Read |
| DF-AGT-059 | agent_run (P10 `rwb_agent`) | segment_product_group | Read |
| DF-AGT-060 | agent_run (P10 `rwb_agent`) | segment_region_code | Read |
| DF-AGT-098 | agent_feedback (P10 `rwb_agent`) | agent_run_id | Write |
| DF-AGT-099 | agent_feedback (P10 `rwb_agent`) | item_key | Write |
| DF-AGT-100 | agent_feedback (P10 `rwb_agent`) | verdict | Write |
| DF-AGT-101 | agent_feedback (P10 `rwb_agent`) | reason | Write |
| Standard column | agent_feedback (P10 `rwb_agent`) | created_by | Write |
| Standard column | agent_feedback (P10 `rwb_agent`) | created_at | Write |
| DF-AGT-102 | agent_feedback (P10 `rwb_agent`) | decision_log_id | Write |
| DF-AGT-003 | agent_policy (P10 `rwb_agent`) | policy_version | Write |
| DF-AGT-008 | agent_policy (P10 `rwb_agent`) | autonomy_mode | Write |
| DF-AGT-009 | agent_policy (P10 `rwb_agent`) | segment_product_group | Write |
| DF-AGT-010 | agent_policy (P10 `rwb_agent`) | segment_region_code | Write |
| DF-AGT-017 | agent_policy (P10 `rwb_agent`) | evaluation_run_id | Write |
| DF-AGT-018 | agent_policy (P10 `rwb_agent`) | promotion_conditions | Write |
| DF-AGT-089 | agent_evaluation (P10 `rwb_agent`) | label_key | Write |
| DF-AGT-090 | agent_evaluation (P10 `rwb_agent`) | sample_size | Write |
| DF-AGT-095 | agent_evaluation (P10 `rwb_agent`) | precision_value | Write |
| DF-AGT-096 | agent_evaluation (P10 `rwb_agent`) | recall_value | Write |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-E2-029. The eight agent tables are the P10 rows of `rwb_agent` in the Ownership Map; `recovery_case` and `assignment` belong to P3, `deviation` to S8, `decision_log_entry` to P7 and `valuation_ext` with `v_ace_valuation` to P1, and each is reached through its owner's contract, never as a table (DP-01, DP-05, DP-11). No field of another service's table is written here: the deviation, the case status and the entry are written by their owners on a call of this story. The policy write is the configuration operation of RWB-P10-E1058-APP used to load version "P2"; the sample is loaded through the sample operation of the same story.

### 12. Contract

The contract values the sources leave open are Not specified in the source documents (GAP-0626; GAP-2193; GAP-2194; GAP-2402; GAP-3100). This story builds no code value for them and adds no table, so the Flyway position of rwb_agent is Not specified in the source documents (GAP-2193).

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10). Neither operation is new here: both are baselined in RWB-P10-E1058-CON and published for E3 by RWB-P10-E2028-CON, and this story supplies their screening behaviour and adds no member.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/agent-outputs` | Read the L1 outputs of a case for the panel: `AgentOutput[]` with `proposals[{code, reasons, sourceRefs, precedingContactId, confidence, lowConfidence, feedback}]`; a case with no L1 run answers no screening output; errors 401, 403, 404 (MSG-P4-003), 503 | Case record R, scope applied | Not applicable: the call writes nothing |
| POST | `/agent-runs/{runId}/feedback` | Record the owner's verdict on one proposal: AgentFeedbackRequest with itemKey = the code ("X1" … "X7"), verdict ACCEPTED or REJECTED and reason, required for REJECTED; 200 AgentOutput; errors 401, 403, 404, 409 (MSG-GEN-004), 422 (MSG-P7-005), 503 (MSG-P7-003) | Case record U, scope applied | Idempotency-Key header; one feedback per run and item |

Errors: 401 no session (MSG-P4-001), 403 no Case record right (MSG-P4-002), 404 an unknown case or run (MSG-P4-003), 409 a second verdict on the same item (MSG-GEN-004), 422 an empty reason (MSG-P7-005), 503 the store, the library or a consumed contract unavailable (MSG-P7-003). The configuration operations `POST /admin/agent-configs`, `POST /admin/agent-configs/{versionId}/approve` and `POST /admin/agent-samples` of RWB-P10-E1058-CON and the evaluation operations with the report read of RWB-P10-E1061-CON are used here and are not re-declared.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case (RWB-P3-E2015-CON) | AC2, AC3, AC6: the case facts and the status - product group MORTGAGE, region BKK, "In progress", then "On hold" after R-DEV-01 | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case (RWB-P3-E1042-CON) | AC1, AC6, AC10: the floor 0.80, the segment values and the promotion condition in force | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | AC1, AC2, AC8: LOV-DEVIATION (X1 to X7), LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-FEEDBACK, LOV-PRODUCT, LOV-REGION, LOV-RAISED-BY | One hop, 2 s |
| GET | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | AC7: the open deviations of the case, so a code already open is not shown | One hop, 2 s |
| POST | the raise of rwb-deviation: Not specified in the source documents (GAP-0625; ASM-0931) | S8 rwb-deviation | AC2, AC8: the legacy `DeviationService.raise(caseId, deviationCode, reason, documentIds, raisedBy, agentRunId)`, answered with the deviation ID and the entry ID | One hop, 2 s |
| GET | the interaction-ledger read of rwb-source-data for the entries of a case in a window: Not specified in the source documents (GAP-0625; ASM-0936) | P1 rwb-source-data | AC2: the preceding contact of an X1 proposal, and the ACE facts of X7 through the contract or the service's own `v_ace_*` view (DP-05) | One hop, 2 s |
| GET | the sealed entry read of rwb-decision: Not specified in the source documents (GAP-0625; ASM-0933) | P7 rwb-decision | AC4, AC9: the sealed entry of the record the local library wrote, so `agent_feedback.decision_log_id` names it | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11); rwb-agent calls no service through another service and holds no schema client of another service. The ACE read of X7 adds no dependency (DP-05).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| DecisionRecorded, the record type of the library | `rwb.decision-record.v1`, shared, with its retry and `.dlt` topics (DP-03) | P7 rwb-decision owns the ledger; the library of RWB-PLT-E1027-CON owns the envelope | the case ID | the record of a rejection: decision the code, agent version "SCREENING@P2/PR2", final call REJECTED, the reason, the run ID and the entry ID |

The record is inserted by the library in the same transaction as the `agent_feedback` row and published by the outbox relay of RWB-PLT-TE006-CON; the payload carries no personal data (section 17). This story publishes no agent event of its own: `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` comes from the run path of RWB-P10-E1062-APP, and EV-06 DeviationRaised on `rwb.deviation.events.v1` is published by S8 on a confirmation.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Use | Rule |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 rwb-case | AC2, AC3: a new case of the segment starts one L1 run, any other case one shadow run | Dedupe on the event ID in the inbox; one run per case and event |
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 rwb-document | AC2, AC3: a new document on an open case starts one run in the mode of its segment | Dedupe on the event ID; payload documentId, caseId, type and source |

No other topic is consumed. The open deviations, the case facts, the ledger, the ACE facts and the entry are read through their owners' REST contracts (DP-11).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow, one per case and triggering event (of RWB-P10-E1062-APP, restated) | `rwb-agent` | Input: agent "SCREENING", case ID, subject ID, trigger event, event ID, idempotency key and the resolved mode. One execution per key, the 60-second policy budget, then the rule result (R-UNI-32). Workflow ID form: Not specified in the source documents (CG-ALL-2718); start rule: a run starts from EV-01 or EV-16; the screening start named in the AgentRunWorkflow row of Temporal Workflow and Activity Catalog v1 is CaseCreated |
| ResolveScreeningMode | Activity, added by this story | `rwb-agent` | Reads the approved policy row of `rwb_agent` and the case facts of the P3 contract; output: mode L1 or SHADOW, the policy version and the segment it matched, or the refusal of X9 |

The confirmation and the rejection are synchronous inside the feedback request: the handler calls the S8 raise, writes the record, stores the feedback and answers 200, so no workflow is added beyond the relay of the record.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story: the evaluation is started by RW-COE, a run starts from EV-01 or EV-16, and a verdict comes from a person. The legacy Quartz scheduler is retired and DP-10 is not a pattern of this key.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_feedback | P10 (`rwb_agent`) | One verdict per run and item key, with its reason and the entry ID; created by the earlier P10 stories, no column added |
| agent_policy | P10 (`rwb_agent`) | The approved row "SCREENING" version "P2" with its segment fields, its evaluation run and its condition; written through the operation of RWB-P10-E1058-APP |
| agent_evaluation | P10 (`rwb_agent`) | One score row per code X1 to X7: counts, sample size, precision and recall; no column added |
| agent_evaluation_run | P10 (`rwb_agent`) | The evaluation of "SCREENING" on "SCREEN-S2" version 1 and its scores; no column added |
| agent_run | P10 (`rwb_agent`) | The L1 and shadow runs of the segment, read for the panel; no column added |
| agent_sample, agent_prompt | P10 (`rwb_agent`) | The sample "SCREEN-S2" version 1 and prompt version "PR2", read only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox, inbox and idempotency envelope of the feedback and the record (DP-09) |

No new table and no migration: the legacy story states "no new table", and every column this story uses exists from RWB-P10-E1058-APP, RWB-P10-E1062-APP and RWB-P10-E2028-APP, so the Flyway sequence of `rwb_agent` is not extended (GAP-0625; ASM-0938). rwb-agent reads no table of another service and holds no cross-service foreign key (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock | The P3 contracts of RWB-P3-E2015-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON | Cases "RW-2027-000801" to "RW-2027-000804" with MORTGAGE, BKK and "In progress", then "On hold"; HIRE_PURCHASE for "RW-2027-000802"; the floor 0.80 and the condition "recall at least 0.75 for every code"; LOV-DEVIATION with X1 to X7 and the seven other lists; an unknown case and an answer beyond 2 s |
| rwb-deviation WireMock | The raise and the open-deviation read | X1 raised with `raised_by` "SCREENING_AGENT" and its entry ID; X1 already open on "RW-2027-000801"; one deviation and a 409 MSG-GEN-004 for the second raise on "RW-2027-000804"; a 503 on the raise |
| rwb-source-data WireMock | The ledger read and the ACE facts of X7 | The ledger of "RW-2027-000801" with the preceding contact; the appraisal date of an X7 collateral; an empty ledger; an answer beyond 2 s |
| rwb-decision WireMock | The sealed entry read | The recorded entry of the rejection on "RW-2027-000801"; an unknown entry; an answer beyond 2 s |
| decision-record library stub | The platform library of RWB-PLT-E1027-CON | An accepted record with its entry ID, a writer failure for AC9, a `.dlt` route on a permanent relay failure |
| gateway-bff route stub | The route of RWB-PLT-N001-CON | A pass-through in front of the panel read, one hop, query and media type preserved, the 403 passed through unchanged |

Every fixture is synthetic and holds no personal data; no test calls the model endpoint INT-23. The inbox and outbox stubs, the access guard stub and the evaluation fixture of RWB-P10-E1061-CON are used but not declared here.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided by the baseline and used, 7 consumed | The panel read and the feedback operation; the case read, the parameters, the lists, the open deviations, the raise, the ledger and the sealed entry, one hop and 2 s each |
| Kafka | 1 published, 2 consumed | The record on `rwb.decision-record.v1`; `CaseCreated` and `DocumentStored`; EV-28 and EV-06 published by the run path and by S8 |
| Temporal | 1 workflow restated, 1 activity added | AgentRunWorkflow with ResolveScreeningMode on the queue `rwb-agent` |
| File | None | No file is read or written; the sample arrives through the sample operation of RWB-P10-E1058-APP |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.screening` inside rwb-agent; the front end module of the panel lives with the SCR-03 composition and is reached through the gateway-bff route.

**Pattern application**

| DP | Microservice pattern | Dependency added |
|---|---|---|
| DP-03 | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | ACE data through rwb-source-data's contract or the service's own views | none |
| DP-06 | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/agent/v1` | none |
| DP-19 | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 and DP-11 add no dependency of their own: the ACE facts arrive through the owner's contract or the service's own view, and the legacy in-process calls are the C contracts of the key and their fakes. The S8 raise is consumed with a mock because no source names the story that publishes it (GAP-0625; ASM-0931).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ScreeningModeListener, ResolveScreeningMode | Listener and activity | BR1, BR8: the mode per segment from the approved policy row, with the product group and the region checked through the rwb-case lists |
| ScreeningEvaluationReporter | Service | BR7: reads the run and its score rows, keeps precision and recall per code at four decimals, confirms the sample size 500 |
| ScreeningProposalReadService | Service | Serves the panel read from `agent_run` and `agent_feedback` of `rwb_agent` only |
| ScreeningOutputFilter | Service | BR5, BR6: drops a code already open and sets the marker "Low confidence" below the floor in force |
| ScreeningFeedbackHandler | Service | Both verdicts: ACCEPTED calls the raise and stores the feedback with the entry ID; REJECTED writes the record first, then the feedback |
| DecisionRecordWriter | Client of the platform library | BR4, BR9: inserts the record and the outbox row in the feedback transaction and reads the entry ID back |
| ProposedDeviationsPanel | React component | The panel on SCR-03: code, reasons, sources, confidence, the marker, Confirm, and Reject with a reason |
| AgentFeedbackService | Service | Extended with the item keys X1 to X7 and the one-verdict rule |
| CaseFactReader, ParameterValueReader, ReferenceDataReader | Clients | The P3 case read, the parameters and the lists (DP-06, DP-07, DP-11) |
| DeviationRaiseClient, OpenDeviationReader | Clients | The S8 raise and the open deviations of the case (DP-11) |
| LedgerReader, AceFactReader | Clients | The preceding contact of X1 and the appraisal date of X7 through P1 or the own view (DP-05) |

**Database and migrations.** No new table and no new column: `agent_feedback`, `agent_policy`, `agent_evaluation`, `agent_evaluation_run`, `agent_run`, `agent_sample` and `agent_prompt` exist from the earlier P10 stories (GAP-0625; ASM-0938). The indexes the panel and the evaluation need - on `agent_feedback (agent_run_id, item_key)` and on `agent_evaluation (evaluation_run_id, label_key)` - are created by the earlier migrations if not already present. No other schema is touched (DP-01).

**Configuration and reference data.** Policy "SCREENING" version "P2" with prompt "PR2", mode L1 for MORTGAGE and BKK, shadow elsewhere, the evaluation run of "SCREEN-S2" version 1, the condition "recall at least 0.75 for every code", the fallback rule and the watch measures, loaded by RW-COE and approved by RW-RISK. Sample "SCREEN-S2" version 1, the analysts' review of 500 cases. The floor 0.80, the segment values and the condition as parameters of rwb-case (DP-06) and the eight lists as its reference data (DP-07); the parameter keys are Not specified in the source documents (GAP-0625; ASM-0934). The flag `rwb.agent.screening-l1` is kept as a legacy reference and read through the platform flag library: off, every segment runs in shadow and the panel is hidden (ASM-0939).

**Build steps**

1. Run the evaluation on "SCREEN-S2" version 1 and load the L1 proposal in SIT, against the parameters and lists fakes (AC1, AC10).
2. Extend the listener for the mode per segment with ResolveScreeningMode and the P3 case read (AC2, AC3).
3. Build ScreeningOutputFilter with the open-deviation read and the floor in force (AC6, AC7).
4. Build ScreeningFeedbackHandler for both verdicts, with the raise on ACCEPTED and the record first on REJECTED (AC2, AC4, AC5, AC9).
5. Add the parallel-confirmation test against the S8 fake, the 409 and the one-deviation outcome (AC8).
6. Build ProposedDeviationsPanel with its four states and the route in front of the panel read (AC2, AC6).
7. Pipeline scans: no business value of the segment, the floor or the condition in the source; no monolith base path; no other service's table name; no ACE table name outside the owner's view.
8. Contract tests of the two E3 operations against their baselines, so a drift is corrected in RWB-P10-E2028-CON and never here.

**Done when.** The twelve test cases of section 16 pass, the evaluation stores seven score rows with sample size 500 and X1 at 0.9111 and 0.8913, policy "P2" is LOADED with MORTGAGE and BKK and is refused when a condition fails, a Mortgage case in Bangkok shows its proposals and a hire purchase case shows none, a confirmation raises one deviation with its entry ID and an ACCEPTED row, a rejection writes one record and a REJECTED row, the refusals answer 422, 409 and 503 with their messages, and the scans find no code value and no monolith base.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-005 | Reject without a reason | Enter the reason you are not following the recommendation. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Second confirmation of the same proposal | Someone else changed this record. Reload it to see their change. |
| MSG-P10-001 | L1 proposal fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-S8-001 | Deviation raised after confirmation | {deviation} was raised. The case is with {handler}. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case or the run is unknown | This case is not in your scope. |
| MSG-P4-001 | No session (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |

The texts of the legacy table are copied unchanged except MSG-P4-003, whose text is copied from the Error and Message Standard v4. MSG-P4-001, for the 401 answer of AC14, is also copied from that standard and is the one message ID added to the legacy set; MSG-P4-003 is the access message the legacy section 12 names for an unknown case or run, kept here so the refusal set of the key is complete. In AC5 the empty reason is refused before anything is written; in AC8 the {action} of MSG-GEN-004 is the second confirmation and the first one stands; in AC9 no feedback row exists; in AC10 {kind} is the policy file, {agent} is "SCREENING" and {check} is "X4 recall 0.6000 below 0.75"; in the access test {action} is "confirm or reject a proposed deviation".

### 15. Screens and states

SCR-03 Case record gains the panel "Proposed deviations" with states: empty (no panel), loading (Not specified in the source documents (CG-ALL-2723)), error (503 read answer, see section 4), no access (403 with MSG-P4-002), ready (proposals with Confirm and Reject), low confidence (marker on the proposal), recorded (verdict and date). After a confirmation SCR-03 shows the on hold banner of the deviation and SCR-08 Deviation queue lists it for the named handler, and its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-2724); SCR-46 Agent monitor shows SCREENING as live for MORTGAGE/BKK and shadow elsewhere; its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-2725).

In the target the panel is composed by the gateway-bff route (DP-19) and reads `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs`; the verdict goes to `POST /api/recovery/agent/v1/agent-runs/{runId}/feedback`. The four states are unchanged, and a proposal is hidden when its code is already open or when the flag is off. The route name and path are Not specified in the source documents (GAP-0625; ASM-0937); the route passes the read and the refusal through unchanged.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-029-11 | AC11, Access | Contract | RW-PHONECOL confirms X1; refused with MSG-P4-002 |
| TC-E2-029-01 | AC1, BR7 | Component | SCREEN-S2 version 1, 500 cases; X1 counts 41, 4, 5 |
| TC-E2-029-02 | AC2, BR1, BR2, BR3 | Component | Mortgage case RW-2027-000801 in BKK, complaint note 2027-01-26 |
| TC-E2-029-03 | AC3, BR1 | Component | Hire purchase case RW-2027-000802 in BKK |
| TC-E2-029-04 | AC4, BR4 | Component | Reject X6 with a reason |
| TC-E2-029-05 | AC5, BR4 | Component | Reject X6 with an empty reason |
| TC-E2-029-06 | AC6, BR6 | Component | X2 with confidence 0.72 |
| TC-E2-029-07 | AC7, BR5 | Component | X1 already open on the case |
| TC-E2-029-08 | AC8 | Component | Two parallel confirmations of X1 |
| TC-E2-029-09 | AC9, BR4 | Component | Decision record writer fails on rejection |
| TC-E2-029-10 | AC10, BR7 | Component | X4 recall 0.6000, condition 0.75 |
| TC-E2-029-12 | Principle 5 | NFR | Record write forced to fail on a rejection; nothing stored; MSG-P7-003 |
| TC-E2-029-13 | 12.7 tables (ASM-3438) | Boundary | Tables of section 12.7 read by rwb-agent; no read of another service's table |
| TC-E2-029-14 | AC12, Access | Contract | RW-PHONECOL rejects X1; refused with 403 and MSG-P4-002 |
| TC-E2-029-15 | AC13, BR8, BR9, BR10, BR11, BR12, BR13 | Boundary | Not specified in the source documents (NEWAC-RWB-P10-E2029-APP-AC12) |
| TC-E2-029-16 | AC14, Access | Contract | Request without a session; caller without Case record U; run ID that does not exist; answers 401, 403, 404 |
| TC-E2-029-17 | AC15 | Component | Not specified in the source documents (NEWAC-RWB-P10-E2029-APP-AC14) |
| TC-E2-029-18 | AC16, BR12 | NFR | rwb-deviation mock silent beyond 2 s on a confirmation of X1 |

The twelve test cases TC-E2-029-01 to TC-E2-029-12 are the legacy cases of RWB-E2-029, kept with their IDs, order and data, and TC-E2-029-13 to TC-E2-029-18 are added by this story (TC-E2-029-13 for the tables of section 12.7); the legacy System level maps to Component, Access to Contract because the refusal is proved through the route and the contract, and Resilience to NFR because the failure of the record write is held to R-UNI-39 and the platform envelope. The full test of each legacy case, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

For the SIT journey of deviation screening, the harness environment and its seeding, the SCREEN-S2 version 1 fixture pack with the 500 labelled cases, the Enterprise AI test profile for SCREENING, the controls that force a decision record failure and two parallel confirmations, the evidence report format and its retention, and the pass and fail gate of wave 2 are Not specified in the source documents (GAP-0411). They are agreed at the wave 2 entry check and held as data files with the story.

### 17. Guardrails

- No business value in code: the segment, the floor and the condition are rows of the policy, the parameters and the reference data, read with their version (BR11).
- No personal data in logs, tests, events or prompts; reasons on the panel hold masking tokens.
- No read of another service's table: the case, the deviation, the ledger and the entry come through their owners' contracts, and ACE facts only through rwb-source-data or the service's own read-only `v_ace_*` view (BR10).
- The agent never raises a deviation without a person's confirmation, and no rejection reaches the feedback row before its record is written (BR2, BR4, BR9).
- Every consumed call is one hop with a 2 s client budget; the model call keeps its own 60-second budget inside the run (BR12).
- The panel is reached through the gateway-bff route and never from a screen to the service (BR13).
- The feedback is idempotent on the run, the item key and the verdict, and one deviation exists per confirmed proposal (AC8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-AGT-08, FEAT-DVH-07 | 11 Handle customer care and deviations | R-UNI-39 | TC-E2-029-01, TC-E2-029-03, TC-E2-029-04, TC-E2-029-05, TC-E2-029-06, TC-E2-029-09, TC-E2-029-10, TC-E2-029-12 |
| REQ-DVH-006 | A deviation flag is visible on the case and in every queue | Business Requirements Program, section 5.15 | FEAT-DVH-07 | 11 Handle customer care and deviations | R-DEV-01 | TC-E2-029-02, TC-E2-029-07, TC-E2-029-08, TC-E2-029-11 |
| DP-03 (D-RCV-60) | Record written locally and sealed centrally | Template and Rules §R5.5; ADR-022 | FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-39 | TC-E2-029-04, TC-E2-029-09, TC-E2-029-12 |
| DP-05 (D-RCV-60) | ACE facts through the owner's contract or the own view | Template and Rules §R5.5 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-E2-029-02 |
| DP-06, DP-07 (D-RCV-60) | The floor, the segment, the condition and the lists are read at run time | Template and Rules §R5.5 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-E2-029-01, TC-E2-029-02, TC-E2-029-06, TC-E2-029-10 |
| DP-09 (D-RCV-60) | The record leaves through the outbox with the CloudEvents envelope and the `.dlt` route | Template and Rules §R5.5; ADR-015 | FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-39 | TC-E2-029-09, TC-E2-029-12 |
| DP-11 (D-RCV-60) | Every consumed read and the raise are REST contracts with a mock, one hop, 2 s | Template and Rules §R5.5; ADR-020 | FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-39 | TC-E2-029-02, TC-E2-029-03, TC-E2-029-07 |
| DP-13, DP-19 (D-RCV-60) | The operations sit on the agent base and the panel is reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-AGT-08, FEAT-DVH-07 | 11 Handle customer care and deviations | None | TC-E2-029-02, TC-E2-029-03, TC-E2-029-11 |
| CTL-07, CTL-08, Principle 5 | A rejection carries its reason and an L1 proposal meets its stated conditions | Business Requirements Program, section 5.15 | FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-39 | TC-E2-029-04, TC-E2-029-05, TC-E2-029-10, TC-E2-029-12 |

The gap GAP-0625 records the areas the sources leave open for this story - the service login, the story that publishes the S8 raise, the parameter keys, the route path and the migration numbering - and each default it raises is settled by ASM-0930 to ASM-0942. The cross-service behaviour is proved by the wave 2 integration work of RWB-ITG-W2, and the contract of this key is RWB-P10-E2029-CON.

### 19. Out of scope

- L1 on further segments (a later policy version; FEAT-AGT-12, Epic 3).
- The deviation flows after the flag (S8, Epic 7).
- The agent handling X6 and X7 within policy (R-DEV-06, Epic 7).
- The contract of this key with its fakes: RWB-P10-E2029-CON.
- The agent runtime, its configuration and sample operations and the run path: RWB-P10-E1058-APP and RWB-P10-E1062-APP.
- The evaluation harness and the proposal payload as shapes: RWB-P10-E1061-CON.
- The E3 operations and their base shape: RWB-P10-E2028-CON, which this slice restates.
- The deviation record, R-DEV-01 and the case status it changes: rwb-deviation (S8) and rwb-case (P3).
- The central ledger, its hash chain and its sealing: rwb-decision (P7).
- The interaction ledger, the ACE view contract and the extension tables: rwb-source-data (P1).
- The agent monitor screen SCR-46: RWB-E2-031.
- The cross-service proof of this key: the integration work of RWB-ITG-W2.
