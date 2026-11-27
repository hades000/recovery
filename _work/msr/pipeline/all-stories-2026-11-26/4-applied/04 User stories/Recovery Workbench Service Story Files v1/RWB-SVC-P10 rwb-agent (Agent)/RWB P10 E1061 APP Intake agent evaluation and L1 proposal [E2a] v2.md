# RWB-P10-E1061-APP Intake agent evaluation and L1 proposal [E2a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1061-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-061 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP13, DP15, DP19 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1059-APP |
| Depends on (build) | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-E1059-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to REQ-DRI-010, REQ-DRI-011) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E1-061 for rwb-agent. The behaviour of the legacy story is unchanged, so the disposition is Moved (no impact) and the content is carried onto the service rather than rewritten: the evaluation tables the report reads and the policy row the L1 proposal writes are P10's own in schema `rwb_agent` (DP-01), the four promotion columns arrive with the service's own migration `V10_004__policy_promotion.sql` in the P10 Flyway sequence (DP-15), the report operation is served on the base `/api/recovery/agent/v1` and the legacy monolith base is retired for it (DP-13), the minimum sample and the check list of an autonomy step are read through the rwb-case parameters contract instead of the local policy schema (DP-06), LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-EVAL-STATUS are read through the rwb-case reference-data contract instead of being code enumerations (DP-07), and the reads are reached through the gateway-bff route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P10-E1061-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the evaluation report of the case intake agent and the proposal to run it at autonomy level 1, built inside rwb-agent from the stored shadow results - the four `rwb_agent` tables of the evaluation harness, the report operation on the base `/api/recovery/agent/v1` with its JSON, CSV and PDF answers, the L1 promotion checks inside the policy load, and the four promotion columns added by the service's own migration - reading the minimum sample and the check list through the rwb-case parameters contract and the three lists through the rwb-case reference-data contract**, so that **the risk and model risk officer approves the step to L1 on measured results, on the same values the legacy story fixed, before wave 1 exits**.

### 2. Business rationale

The step from shadow to L1 puts agent output in front of case owners, so the approver needs the agreement rate, the failure types, the cost and the latency on a stated sample before deciding. The legacy story produced that report from the evaluation run of RWB-E1-059 and held the L1 proposal as a versioned policy row with its conditions, fallback and measures to watch (REQ-DRI-010), approved and dated like any other reference row (REQ-DRI-011). Nothing goes to L1 until RW-RISK approves the row. That behaviour is unchanged and is copied here value for value: the evaluation run "EV-INTAKE-001", the 200 shadow runs with 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR, the total cost 412.6000 baht, the cost per case 2.0630 baht, the median latency 4,100 ms, the 95th percentile 9,800 ms, the policy "INTAKE" versions "P1" and "P2", the prompt "PR1", the condition "agreement at least 0.85 for every gap type", the NO_CONTACT_POINT agreement 0.8150 and the sample size 150 of "EV-INTAKE-003" are the legacy values and every criterion of section 7 keeps them character for character.

In the legacy delivery the report, the score rows, the shadow runs and the policy row sat in one module and one `recovery` schema, the minimum sample was a value of the local policy JSON schema, the mode and status values were code enumerations, and the report was served by the monolith on the legacy monolith base. The disposition is Moved (no impact), so what changes is only where each fact lives and how it is reached:

- The evaluation run, the score rows and the shadow runs the report aggregates are P10 rwb-agent, schema `rwb_agent`: agent_evaluation_run, agent_evaluation and agent_run (DP-01; BR7).
- The policy row the proposal writes is P10 rwb-agent too: agent_policy in `rwb_agent`, extended with the four promotion columns by the service's own migration (DP-01, DP-15; BR8).
- The minimum sample of an autonomy step and the promotion check list in force are values of the rwb-case parameters contract, read at load time and never written in code; the legacy wording "set in the policy loader schema" is read as the versioned parameter row (DP-06; BR4; ASM-0870).
- LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-EVAL-STATUS are reference data of rwb-case, read through the reference-data contract, so mode "L1" and status "LOADED" are checked against the list in force and not against an enumeration in the service (DP-07; BR3; ASM-0873).
- The report operation is served on the base `/api/recovery/agent/v1`, and the legacy monolith base is retired for it (DP-13; AC1, AC3).
- The four promotion columns are added by `V10_004__policy_promotion.sql` in the rwb-agent Flyway sequence, in the service's own schema (DP-15). The legacy number is kept because it follows the `V10_003__evaluation_proposal.sql` of the extraction evaluation in the same P10 sequence.
- RW-COE, RW-RISK and RW-AUDIT reach the reads through the gateway-bff route, which is the only route a screen or an export will use (DP-19).

This key carries no integration dependency (I = None) and the story set holds no integration story for it: the two cross-service parts - the parameter values and the three lists - are consumed through published contracts and proved against their fakes by the contract tests of RWB-P10-E1061-CON, and this story claims no cross-service behaviour of its own. It owns the seven legacy acceptance criteria AC1 to AC7, unchanged.

### 3. Preconditions

- RWB-P10-E1059-APP is done: the case intake agent "INTAKE" exists in rwb-agent, runs in mode SHADOW on a CaseCreated event through the agent platform, and policy version "P1" (SHADOW) with prompt version "PR1" is approved and in force.
- Evaluation run "EV-INTAKE-001" of "INTAKE" on sample "INTAKE-S1" version 1 has status DONE and holds 200 labeled cases with 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR; the 200 runs cost 412.6000 baht in total with median latency 4,100 ms and 95th percentile 9,800 ms (legacy Background, copied unchanged).
- RWB-P10-E1058-APP is done: the agent platform, the prompt and policy store, the configuration operations `POST /api/recovery/agent/v1/admin/agent-configs` and `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve`, and the evaluation harness of RWB-P10-E1060-APP with `POST /api/recovery/agent/v1/admin/agent-evaluations` and `GET /api/recovery/agent/v1/admin/agent-evaluations` exist in rwb-agent (ASM-0871).
- RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are published: the parameters client library, the reference-data client library, the per-service Flyway sequence with parameterized schema names, and the gateway-bff route contract with its stub.
- The `rwb_agent` schema baseline exists with the standard record columns and the Flyway history table of the service; agent_evaluation_run, agent_evaluation, agent_run and agent_policy are created by the P10 migrations, and this story adds only the four promotion columns to agent_policy.
- Agent "INTAKE" has policy version "P1" approved in mode SHADOW with prompt version "PR1" and a model version; the report reads those versions from the evaluation run row and never from a constant.
- The rwb-case contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: `GET /api/recovery/case/v1/admin/parameters` for the minimum sample and the promotion check list in force, and `GET /api/recovery/case/v1/admin/lists/{listCode}` for LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-EVAL-STATUS.
- The minimum sample of an autonomy step for agent "INTAKE" is 200 in the parameters contract in force, and the L1 check list carries the three checks of BR2 to BR4: the named evaluation run is DONE, every stated condition is met by the scores, the sample size reaches the minimum, and the conditions, the fallback and the measures are present (ASM-0870).
- RW-COE holds Rules and parameters C and RW-RISK holds Rules and parameters A; RW-AUDIT holds R on the report and the versions. The refusals of MSG-P4-002 are proved by the access test case TC-E1-061-08.
- The login of this service is the rwb-agent login: Not specified in the source documents (GAP-0612; ASM-0869).
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. RW-COE requests the report of an evaluation run through `GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report`, with Accept application/json, text/csv or application/pdf (AC1).
2. EvaluationReportService reads the run row and refuses the request with 409 and MSG-P10-008 when the run is not DONE, so a report exists only for a finished evaluation (AC3; legacy X1).
3. For a DONE run the service aggregates the stored rows of `rwb_agent` only: the sample size, the agreement rate per gap type and the failure counts from agent_evaluation and agent_evaluation_run, the total cost and the latency percentiles from the agent_run rows, and the policy, prompt and model versions from the run row (BR1, BR4; AC1).
4. The service computes cost per case as total cost divided by the number of runs at four decimals, and the median and the 95th percentile over all runs including timeouts at 60,000 ms (BR1; AC1).
5. The report object carries counts, rates, versions and durations only; no personal field and no customer, party or account identifier is read into it (BR5; AC1).
6. EvaluationReportExporter writes the CSV and the PDF from the same report object, so the three answers of the operation cannot disagree (AC1; section 15).
7. RW-COE loads policy "INTAKE" version "P2" with mode "L1", evaluation run "EV-INTAKE-001", the conditions "agreement at least 0.85 for every gap type", the fallback "rule result per R-UNI-32" and the measures "acceptance, correction rate, fallback rate below 0.10" through `POST /api/recovery/agent/v1/admin/agent-configs` (AC2).
8. PromotionProposalValidator runs inside the policy load for mode "L1": it checks that the named run is DONE, that the conditions, the fallback and the measures to watch are present, that every stated condition is met by the scores of that run, and that the sample size reaches the minimum read through the parameters contract (BR2, BR3, BR6; AC4, AC5, AC6).
9. Mode "L1" and the status values are checked against LOV-AUTONOMY and LOV-CONFIG-STATUS read through the reference-data contract; a mode or a status outside the list in force is refused by the same check (BR3).
10. A load that passes is stored as a new agent_policy version in `rwb_agent` with status LOADED, the four promotion columns filled and the loader recorded as loaded_by (AC2).
11. Version "P1" stays in force until RW-RISK approves "P2": the load alone changes no mode in flight (BR6; AC2).
12. RW-RISK approves version "P2" with a valid from date through `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve`; the approval moves the row to APPROVED and records approved_by and valid_from (AC2).
13. The approval is refused with 409 and MSG-P7-002 when the user who approves is the user who loaded the version (BR6; AC7).
14. The report and the version reads are reached through the gateway-bff route in front of the admin path, one hop each, so a screen never calls rwb-agent directly (DP-19).
15. The story writes agent_policy rows and reads agent_evaluation_run, agent_evaluation and agent_run; it writes nothing else and changes no case, no document and no threshold in force (BR7, BR8; section 17).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The report is requested for an evaluation that is still running | Refused with 409 | MSG-P10-008 | AC3 |
| X2 | The L1 proposal has no conditions, no fallback or no measures | Load refused in full | MSG-P10-001 | AC4 |
| X3 | The evaluation scores do not meet a stated condition | Load refused, naming the gap type and the score | MSG-P10-001 | AC5 |
| X4 | The sample size is below the minimum of 200 cases | Load refused | MSG-P10-001 | AC6 |
| X5 | The loader tries to approve the proposal | Refused with 409 | MSG-P7-002 | AC7 |
| X6 | A role without the right | Refused with 403 | MSG-P4-002 | TC-E1-061-08 |
| X7 | The parameters contract does not answer inside the 2 s budget, or answers without the minimum sample or without the check list for agent "INTAKE" | The load is refused with 422 and MSG-P10-001 naming the missing parameter; no default and no value in code is used, and no version row is written | MSG-P10-001 | AC2, AC6 |
| X8 | LOV-AUTONOMY, LOV-CONFIG-STATUS or LOV-EVAL-STATUS does not answer inside the 2 s budget, or the mode or status offered is not in the list in force | The load or the approval is refused with 422 and MSG-P10-001 naming the list and the value, and the version in force keeps serving | MSG-P10-001 | AC2, AC7 |
| X9 | The migration `V10_004__policy_promotion.sql` fails in the service's Flyway sequence | The new version does not start and the version in force keeps serving; no version row is created and no report is served | None | AC1, AC2 |
| X10 | The report is requested for a run of an agent the caller may not read, or through a route that is not the gateway-bff route | Refused with 403 with MSG-P4-002, or 404 at the edge; nothing is read | MSG-P4-002 | AC1, TC-E1-061-08 |

X1 to X6 are the legacy exception paths of RWB-E1-061 carried onto the service; X7 to X10 are the failures that appear when the parameter and list reads leave the service and when the schema and the route become the service's own responsibility. X6 is not reached by a criterion of this story: it is proved by the access test case TC-E1-061-08, and the message is kept so a reader finds the legacy set complete.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads only the stored results of RWB-P10-E1059-APP and the agent platform of RWB-P10-E1058-APP; it waits only for the in-lane story RWB-P10-E1059-APP and owns its own schema objects |
| Negotiable | The package layout, the component names, the export column order and the PDF rendering are design; the run, the sample, the counts, the cost, the latencies, the policy and prompt versions, the conditions, the measures, the minimum sample and the message IDs are fixed by the legacy story |
| Valuable | Gives the approver one report and one row to approve for the first autonomy step, on measured results |
| Estimable | One report operation with three media types, one validator inside the existing policy load, four columns in one migration, two contract clients and one route |
| Small | Three to four days, as in the legacy estimate |
| Testable | Each of the seven criteria of section 7 is one automated test on an observable: a REST answer, a stored row, a report field, a migration record or a scan of the source |

### 7. Acceptance criteria

```gherkin
Feature: Intake agent evaluation and L1 proposal [E2a]

  Background:
    Given evaluation run "EV-INTAKE-001" of "INTAKE" on sample "INTAKE-S1" version 1 has status "DONE"
    Given it holds 200 shadow runs: 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR
    Given the 200 runs cost 412.6000 baht in total with median latency 4,100 ms and 95th percentile 9,800 ms

  Scenario: AC1 Report (legacy RWB-E1-061 AC1)
    Given the shadow results
    When the report is written
    Then it holds sample size 200, the agreement rate per gap type, failure counts 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR
    Then it holds total cost 412.6000 baht, cost per case 2.0630 baht, median latency 4,100 ms and 95th percentile 9,800 ms
    Then it holds policy "P1", prompt "PR1" and the model version, and no personal field

  Scenario: AC2 Proposal (legacy RWB-E1-061 AC2)
    Given the rwb-case reference-data contract mock returns LOV-AUTONOMY with OFF, SHADOW and L1 and LOV-CONFIG-STATUS with LOADED, APPROVED and RETIRED
    Given the report
    When RW-COE loads policy "INTAKE" version "P2" with mode "L1", evaluation run "EV-INTAKE-001", conditions "agreement at least 0.85 for every gap type", fallback "rule result per R-UNI-32" and measures "acceptance, correction rate, fallback rate below 0.10"
    Then the system stores version "P2" with status "LOADED" and holds the conditions, the fallback and the measures to watch
    Then "P1" stays in force until RW-RISK approves "P2"

  Scenario: AC3 Report on an unfinished evaluation (legacy RWB-E1-061 AC3)
    Given evaluation run "EV-INTAKE-002" has status "RUNNING"
    When RW-COE requests its report
    Then the system refuses the request with 409 and MSG-P10-008

  Scenario: AC4 A proposal without its measures (legacy RWB-E1-061 AC4)
    Given the rwb-case parameters contract mock returns the minimum sample 200 for an autonomy step in force
    Given a policy file with mode "L1" and no measures to watch
    When RW-COE loads it
    Then the system refuses the load with 422 and MSG-P10-001 naming check "measures to watch present"

  Scenario: AC5 Scores below a stated condition (legacy RWB-E1-061 AC5)
    Given the rwb-case parameters contract mock returns the minimum sample 200 for an autonomy step in force
    Given gap type NO_CONTACT_POINT has agreement 0.8150 in "EV-INTAKE-001"
    When RW-COE loads a proposal with condition "agreement at least 0.85 for every gap type"
    Then the system refuses the load with 422 and MSG-P10-001 naming "NO_CONTACT_POINT 0.8150 below 0.85"

  Scenario: AC6 Sample below the minimum (legacy RWB-E1-061 AC6)
    Given the rwb-case parameters contract mock returns the minimum sample 200 for an autonomy step in force
    Given evaluation run "EV-INTAKE-003" has sample size 150
    When RW-COE loads a proposal that names it
    Then the system refuses the load with 422 and MSG-P10-001 naming check "sample size at least 200"

  Scenario: AC7 The loader cannot approve the proposal (legacy RWB-E1-061 AC7)
    Given the rwb-case reference-data contract mock returns LOV-CONFIG-STATUS with LOADED, APPROVED and RETIRED
    Given user "coe.user01" loaded version "P2"
    When user "coe.user01" approves "P2"
    Then the system refuses the approval with 409 and MSG-P7-002
```

**Target reading.** The agent "INTAKE", its policy versions "P1" and "P2", the prompt "PR1", the evaluation runs "EV-INTAKE-001", "EV-INTAKE-002" and "EV-INTAKE-003", the sample "INTAKE-S1" version 1, the 200 runs with 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR, the total cost 412.6000 baht, the cost per case 2.0630 baht, the median 4,100 ms, the 95th percentile 9,800 ms, the gap type NO_CONTACT_POINT with agreement 0.8150, the sample size 150, the conditions, the fallback, the measures and the message IDs are the legacy values of RWB-E1-061, copied character for character, and the Background keeps its three lines. Each Scenario line keeps its legacy number and title and carries the origin tag of its criterion; every legacy Given, When and Then is kept word for word.

Five of the seven criteria carry one inserted line, `Given the rwb-case contract mock returns ...`, as their first Given, because the criterion crosses into rwb-case: AC2 and AC7 name a mode and a status whose lists are reference data of rwb-case (DP-07; ASM-0873), and AC4, AC5 and AC6 run through a load that reads the minimum sample of an autonomy step from the parameters contract (DP-06; ASM-0870). AC1 and AC3 need none: AC1 aggregates only the run, score and shadow rows of `rwb_agent` - the cost 412.6000 baht and the two latencies are the agent_run rows of this service and are not a figure of another service - and AC3 asserts only the refusal of a report for a run that is not DONE. The report object is the legacy one of section 12: sampleSize, agreementByLabel[], failureCounts, totalCostThb, costPerCaseThb, latencyP50Ms, latencyP95Ms, agent, sampleSize and the three versions (ASM-0877 in RWB-P10-E1061-CON). The in-process monolith call of the legacy section 13 becomes one operation on the base `/api/recovery/agent/v1` (DP-13); the four promotion columns arrive by P10's own migration `V10_004__policy_promotion.sql` (DP-15); the minimum sample and the check list come from the parameters contract instead of the local policy schema (DP-06); the three lists come from the reference-data contract instead of the service's enumerations (DP-07); and the reads are reached through the gateway-bff route (DP-19). The behaviour is unchanged, which is why the disposition is Moved (no impact) and no legacy criterion is added to or dropped from this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The report holds the sample size, the agreement rate per gap type, the failure counts by type, the total and per-case cost, the median and 95th percentile latency, and the policy, prompt and model versions; cost per case = total cost / runs at 4 decimals, and the percentiles are computed over all runs including timeouts at 60,000 ms | agent_evaluation_run (DF-AGT-070 to DF-AGT-083); agent_run (DF-AGT-051, DF-AGT-054); legacy BR4 |
| BR2 | Every stated condition of an L1 proposal is checked against the scores of the named run before the version is stored | Principle 1; CTL-08; legacy BR2 |
| BR3 | The mode and the status of a version are always values of LOV-AUTONOMY and LOV-CONFIG-STATUS in force, read through the rwb-case reference-data contract | TSD P10 v2 T3.2; DP-07; ASM-0873 |
| BR4 | The minimum sample for an autonomy step is a parameter value of rwb-case read at load time - 200 for agent "INTAKE" - and never a value in code | FEAT-AGT-03; DP-06; ASM-0870 |
| BR5 | No personal field is read into the report, the CSV or the PDF: the report holds counts, rates, versions and durations only | Legacy section 17; Template and Rules §R7.2 s17 |
| BR6 | The fallback of an L1 agent is the rule result, the loader and the approver are different people, and a load changes no mode in force before the approval and its valid from date | R-UNI-32; legacy BR5, BR6 |
| BR7 | rwb-agent reads no table of another service and holds no foreign key across services: the parameter values and the lists come through the rwb-case contracts | DP-01; DP-06; DP-07 |
| BR8 | The story writes agent_policy only, in `rwb_agent`, and adds the four promotion columns by `V10_004__policy_promotion.sql` in its own Flyway sequence | DP-01; DP-15; Ownership Map (P10 owns agent_policy) |

### 9. State transitions

No case state transition: this story does not change a case status and touches no case of record. The transitions of the policy version are these:

| From | Event | Condition | To |
|---|---|---|---|
| None | An L1 proposal loaded through `POST /admin/agent-configs` | The named run is DONE, the conditions, the fallback and the measures are present, every condition is met and the sample reaches the minimum | LOADED (agent_policy.status, DF-AGT-021) with loaded_by (DF-AGT-024) |
| None | An L1 proposal loaded | A condition, the fallback or the measures is missing | No row; 422 MSG-P10-001 |
| None | An L1 proposal loaded | A stated condition is not met by the scores, or the sample is under the minimum | No row; 422 MSG-P10-001 |
| None | An L1 proposal loaded | The parameters or reference-data contract does not answer, or a value is outside its list | No row; 422 MSG-P10-001 |
| LOADED | RW-RISK approves through `POST /admin/agent-configs/{versionId}/approve` | The approver is not the loader and the valid from date is given | APPROVED with approved_by (DF-AGT-025) and valid_from (DF-AGT-022) |
| LOADED | The loader approves their own version | The user who loaded the version is the user who approves it | LOADED; 409 MSG-P7-002 |
| LOADED | A later version is loaded and approved | None | The earlier version keeps its status and its dates; RETIRED is reached by the configuration story of Epic 3, not here |

The evaluation run states RUNNING, DONE and FAILED are read by this story and are set by the evaluation harness of RWB-P10-E1060-APP; the report is refused for anything but DONE (AC3). The state of a version in force changes no case, no document and no threshold; the mode takes effect only on a business run after the approval and its valid from date (BR6).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Requests and exports the report; loads the proposal (Rules and parameters C) |
| RW-RISK, risk and model risk officer | Reads the report; approves the proposal (Rules and parameters A) |
| RW-AUDIT, internal audit | Reads the report and the versions (Rules and parameters R) |
| rwb-agent service identity (the rwb-agent login, DP-02) | Builds the report, runs the promotion checks inside the load, writes agent_policy in `rwb_agent`, reads the agent_run and agent_evaluation rows of its own schema, and reads the rwb-case contracts |
| rwb-access (P4) | Answers the right check and refuses a role without the right with MSG-P4-002 |
| No role | Reads `rwb_case`, `rwb_agent` of another deployment or any other service's schema, changes a version in force, changes a case, or reads production data |
| Approval levels | No delegation of authority level applies; the approval of the L1 proposal is the Rules and parameters A right, as in the legacy story |

The login of the service is Not specified in the source documents (GAP-0612; ASM-0869); the story names it "the rwb-agent login (DP-02)" until it is agreed.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-070 | agent_evaluation_run | id | Read |
| DF-AGT-071 | agent_evaluation_run | agent_code | Read |
| DF-AGT-072 | agent_evaluation_run | sample_code | Read |
| DF-AGT-073 | agent_evaluation_run | sample_version | Read |
| DF-AGT-074 | agent_evaluation_run | policy_version | Read |
| DF-AGT-075 | agent_evaluation_run | prompt_version | Read |
| DF-AGT-076 | agent_evaluation_run | model_version | Read |
| DF-AGT-077 | agent_evaluation_run | status | Read; the report exists only for DONE |
| DF-AGT-081 | agent_evaluation_run | total_cost_thb | Read |
| DF-AGT-082 | agent_evaluation_run | p95_latency_ms | Read |
| DF-AGT-083 | agent_evaluation_run | failure_counts | Read |
| DF-AGT-089 | agent_evaluation | label_key | Read |
| DF-AGT-090 | agent_evaluation | sample_size | Read |
| DF-AGT-094 | agent_evaluation | agreement_rate | Read |
| DF-AGT-095 | agent_evaluation | precision_value | Read |
| DF-AGT-096 | agent_evaluation | recall_value | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-051 | agent_run | latency_ms | Read |
| DF-AGT-054 | agent_run | cost_thb | Read |
| DF-AGT-057 | agent_run | evaluation_run_id | Read |
| DF-AGT-002 | agent_policy | agent_code | Write |
| DF-AGT-003 | agent_policy | policy_version | Write |
| DF-AGT-008 | agent_policy | autonomy_mode | Write |
| DF-AGT-021 | agent_policy | status | Write |
| DF-AGT-022 | agent_policy | valid_from | Write |
| DF-AGT-024 | agent_policy | loaded_by | Write |
| DF-AGT-025 | agent_policy | approved_by | Write |
| DF-AGT-017 | agent_policy | evaluation_run_id | Write, in the column added by `V10_004__policy_promotion.sql` |
| DF-AGT-018 | agent_policy | promotion_conditions | Write, in the column added by `V10_004__policy_promotion.sql` |
| DF-AGT-019 | agent_policy | watch_measures | Write, in the column added by `V10_004__policy_promotion.sql` |
| DF-AGT-020 | agent_policy | fallback_rule | Write, in the column added by `V10_004__policy_promotion.sql` |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value (rwb_case, owner P3) | the minimum sample of an autonomy step for "INTAKE" and the promotion check list, with the version in force | Read through the parameters contract |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row (rwb_case, owner P3) | LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-EVAL-STATUS with the version in force | Read through the reference-data contract |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-E1-061. agent_evaluation_run, agent_evaluation, agent_run and agent_policy are the P10 tables of schema `rwb_agent` in the Ownership Map; parameter_catalog, parameter_value, reference_version and reference_row are P3's and are read only through its contracts (DP-06, DP-07). No field of agent_alert, agent_feedback, agent_sample or agent_prompt is written here, and no personal field is read into the report at all.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/agent-evaluations/{evaluationId}/report` | The report of one evaluation run: sample size, agreement per gap type, failure counts, total and per-case cost, median and 95th percentile latency and the three versions; Accept application/json, text/csv or application/pdf; 200 AgentEvaluationReport; 409 when the run is not DONE (MSG-P10-008) | Rules and parameters R, scope applied | Not applicable: the call writes nothing and the same run gives the same report |

`POST /admin/agent-configs` and `POST /admin/agent-configs/{versionId}/approve` are provided by the agent platform of RWB-P10-E1058-APP and are not re-declared here: this story adds the L1 promotion checks inside the load (the 422 answers of AC4, AC5, AC6 and X7) and reuses the approval check for an L1 version (AC7). The shape of the version resource, the status values and the error taxonomy are the baseline's (ASM-0871). `POST /admin/agent-evaluations` and `GET /admin/agent-evaluations`, which start and read the run this report aggregates, are the evaluation harness of RWB-P10-E1060-APP.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | AC4, AC5, AC6 and X7: the minimum sample of an autonomy step for agent "INTAKE" and the promotion check list in force, read before a version is stored | One hop, 2 s, cached by the client library for the life of the request |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | AC2, AC7 and X8: LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-EVAL-STATUS in force, read before a version is stored or approved and before a run status is reported | One hop, 2 s, cached by the client library for the life of the request |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11 behind DP-06 and DP-07); rwb-agent calls no service through another service and holds no schema client of another service.

#### 12.3 Events published

None. The report is built on the admin request path and the promotion changes a configuration row: neither publishes a business event of this key, and the evaluation completion is read through `GET /admin/agent-evaluations` and the report operation. `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` is published by a business run of an agent and belongs to RWB-P10-E1058-APP, not here.

#### 12.4 Events consumed

None. The report is started by RW-COE on request and the load is started by RW-COE through the configuration operations; the events the agent runtime consumes belong to the business runs of RWB-P10-E1058-APP.

#### 12.5 Workflows and activities

None. The report and the promotion checks run inside rwb-agent on the admin request path and start no workflow. `AgentRunWorkflow` on the queue `rwb-agent` in the namespace `rwb-recovery` belongs to the agent platform of RWB-P10-E1058-APP and to RWB-ITG-TE013-ITG; the shadow runs this report aggregates were made by it.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story: the report is requested by a person and the proposal is loaded by a person, never on a cadence, and the legacy Quartz entry of the evaluation does not exist in the target (JOB-05 is retired and JOB-21 only scans stuck workflows).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_evaluation_run | P10 (rwb_agent) | The run the report is built from; read only here, written by the evaluation harness of RWB-P10-E1060-APP |
| agent_evaluation | P10 (rwb_agent) | The score of one label key in a run: sample_size, agreement_rate, precision and recall, read only here |
| agent_run | P10 (rwb_agent) | The shadow runs: status, latency_ms and cost_thb, from which the total cost, the cost per case and the two latencies are computed |
| agent_policy | P10 (rwb_agent) | The versioned policy row the L1 proposal writes; this story adds evaluation_run_id, promotion_conditions, watch_measures and fallback_rule by `V10_004__policy_promotion.sql` |

rwb-agent reads no table of another service and holds no foreign key across services (DP-01, BR7). The parameter and reference rows of schema `rwb_case` are P3's and are read through its two contracts; a pipeline scan finds no `rwb_case`, no `recovery.` and no other service's table name in the rwb-agent sources. `V10_004__policy_promotion.sql` runs in the rwb-agent Flyway sequence of `rwb_agent` and touches no other schema (DP-15).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case parameters WireMock | The P3 parameters contract of RWB-P3-E1042-CON | The minimum sample 200 for agent "INTAKE" and the promotion check list with its version; a version that raises the minimum above 200; an answer without the minimum; a delay beyond 2 s |
| rwb-case reference-data WireMock | The P3 reference-data contract of RWB-P3-E1043-CON | LOV-AUTONOMY with OFF, SHADOW and L1, LOV-CONFIG-STATUS with LOADED, APPROVED and RETIRED, and LOV-EVAL-STATUS with RUNNING, DONE and FAILED; a list version that lacks L1; a delay beyond 2 s |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the report read and the two configuration operations, one hop, with the JSON, CSV and PDF media types preserved |
| agent-run fixture | The event rows of RWB-P10-E1059-APP and RWB-P10-E1060-APP | The 200 stored runs of "EV-INTAKE-001" with 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR, 412.6000 baht in total, median 4,100 ms and 95th percentile 9,800 ms; and "EV-INTAKE-003" with sample size 150 |

The access stub and the configuration store stub are the platform's and are used but not declared here. Every fixture is synthetic: no production run, no customer identifier and no personal value appears in one, and the agent model endpoint INT-23 is never called by a test of this story.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 consumed, 2 restated | The report operation on `/api/recovery/agent/v1`; the rwb-case parameters and list reads; the configuration load and approve restated from RWB-P10-E1058-APP; one hop and 2 s each |
| Kafka | None | The report and the promotion publish no event and consume no topic |
| Temporal | None | No workflow and no schedule in this story |
| File | None | The report leaves as the body of the read with Accept text/csv or application/pdf; no file path is used and the exported pack of the steering committee is not a file of this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.eval.report`, module `eval-report`, Java package `th.co.scb.ace.workbench.recovery.agent.eval.report` inside the rwb-agent service; the promotion checks sit in `th.co.scb.ace.workbench.recovery.agent.config` beside the policy loader of RWB-P10-E1058-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies of this table are the ones in the metadata rows: the three platform contract stories and RWB-PLT-N001-CON are build dependencies, RWB-P3-E1042-CON and RWB-P3-E1043-CON are contract dependencies built against their fakes, and RWB-P10-E1059-APP is the in-lane story that produced the shadow runs. DP-11 sits behind DP-06 and DP-07 on the two reads (one hop, 2 s) and adds no dependency of its own.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentEvaluationController | Controller | Adds `GET /admin/agent-evaluations/{evaluationId}/report` on the agent base, the access check and the three media types (DP-13) |
| EvaluationReportService | Service | Aggregates the stored run, score and shadow rows into the report object: sample size, agreement per gap type, failure counts, total cost, cost per case and the two latencies (BR1) |
| EvaluationReportExporter | Service | Writes the CSV and the PDF from the same report object, so the three answers cannot disagree |
| PromotionProposalValidator | Service | BR2 to BR4 and BR6 inside the policy load for mode "L1": the run is DONE, the three parts are present, every condition is met and the sample reaches the minimum |
| PolicyParameterReader | Client | Reads the minimum sample and the promotion check list through the parameters contract, caches them for the request and fails closed when a value is missing (DP-06) |
| ReferenceListReader | Client | Reads LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-EVAL-STATUS through the reference-data contract (DP-07) |
| AgentPromotionRepository | Repository | Reads agent_evaluation_run, agent_evaluation and agent_run and writes agent_policy in `rwb_agent` only (DP-01) |

**Database and migrations**

- `V10_004__policy_promotion.sql` adds `evaluation_run_id` uuid, `promotion_conditions` jsonb, `watch_measures` jsonb and `fallback_rule` varchar(20) to `agent_policy` in `rwb_agent`, runs after `V10_003__evaluation_proposal.sql` in the rwb-agent Flyway sequence and touches no other schema (DP-15; AC2, AC6).
- The four tables are created by the P10 migrations of RWB-P10-E1058-APP and RWB-P10-E1060-APP; this story adds no table of its own, no column outside the four and no foreign key across services (DP-01; BR8).
- One index for the read: `ix_agent_policy_l1 ON agent_policy (agent_code, status, valid_from)`, so the version in force for an agent is found without a scan.

**Configuration and reference data**

- The minimum sample of an autonomy step for "INTAKE" - 200 - and the promotion check list: values of the rwb-case parameters contract, loaded and versioned by RWB-P3-E1042-CON, read at load time and never written in code (DP-06; ASM-0870).
- LOV-AUTONOMY (OFF, SHADOW, L1), LOV-CONFIG-STATUS (LOADED, APPROVED, RETIRED) and LOV-EVAL-STATUS (RUNNING, DONE, FAILED): reference data of rwb-case read through its contract (DP-07; ASM-0873).
- Policy version "P1" of agent "INTAKE" in force with prompt version "PR1", and the run "EV-INTAKE-001" with its 200 labelled runs, loaded through the evaluation harness of RWB-P10-E1060-APP.
- The list codes, the 2 s client budget and the CSV column order as service configuration.
- The legacy feature flag `rwb.agent.promotion` is kept as the legacy reference and is held by the platform library, not by this service: off, a policy with mode L1 is refused with 422 (ASM-0874).

**Build steps**

1. Flyway migration `V10_004__policy_promotion.sql` and the repository over `rwb_agent` (AC2, AC6).
2. EvaluationReportService over the 200-run fixture with the counts of the Background: 188, 7, 3, 2, 412.6000 baht, 2.0630 baht, 4,100 ms, 9,800 ms (AC1).
3. EvaluationReportExporter and the three media types of the report operation, from the same object (AC1).
4. The 409 of a run that is not DONE, with MSG-P10-008 (AC3).
5. PolicyParameterReader and ReferenceListReader against the two rwb-case fakes, with the missing-value and the delay paths (X7, X8; AC4, AC6).
6. PromotionProposalValidator inside the load: the three checks of AC4, AC5 and AC6 and the condition comparison against the scores of "EV-INTAKE-001" (AC2, AC4, AC5, AC6).
7. The loader-versus-approver 409 with MSG-P7-002 for an L1 version (AC7).
8. Pipeline scans for another service's table name, for a cross-schema foreign key and for the value 200 and the three lists in the source (BR4, BR7, BR8).
9. gateway-bff route contract test in front of the report read and the two configuration operations.

**Done when.** The eight test cases of section 16 pass, the report operation answers on `/api/recovery/agent/v1` in JSON, CSV and PDF, the report of "EV-INTAKE-001" carries the legacy counts and the legacy cost and latencies, the migration applies cleanly on an empty `rwb_agent` schema, no value of the minimum sample and no list value appears in the source, and no version in force and no case has changed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-008 | Report requested before the evaluation is done | The evaluation of {agent} on sample {sample} has not finished. The report is ready when it is done. |
| MSG-P10-001 | The proposal fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P7-002 | Loader approves own proposal | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The four texts are copied unchanged from RWB-E1-061 and this story adds no message ID. Thai text for each message follows decision DL10. In AC3 the {agent} value is "INTAKE" and the {sample} value is "INTAKE-S1" version 1. In AC4, AC5, AC6, X7 and X8 the {kind} value is "policy" and the {check} value is the check name - "measures to watch present", "NO_CONTACT_POINT 0.8150 below 0.85", "sample size at least 200", the missing parameter name, or the list and the value outside it. In the access test the {action} value is "read the report or approve the proposal".

### 15. Screens and states

No screen in this story. RW-COE requests and exports the report through the report operation and RW-RISK reads it, with Accept text/csv or application/pdf for the steering committee pack; the reads are reached through the gateway-bff route in front of the admin path, so a screen never calls rwb-agent directly (DP-19). The report holds counts, rates, versions and durations only, so there is no personal field to mask on it. The agent monitor screen SCR-46 - the screen that shows runs, fallback, latency and cost per agent and comes with RWB-E2-031 - and the autonomy screen of Epic 3 are not changed by this story, and the exact path of the gateway-bff route in front of the reads is Not specified in the source documents (GAP-0612; ASM-0872).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-061-01 | AC1, BR1 | Component | Evaluation "EV-INTAKE-001", 200 runs, 412.6000 baht, cost per case 2.0630 baht, median 4,100 ms, 95th percentile 9,800 ms, policy "P1", prompt "PR1", no personal field |
| TC-E1-061-02 | AC2, BR1, BR6 | Component | Policy "INTAKE" version "P2" with mode L1, run "EV-INTAKE-001", the conditions, the fallback and the measures; status LOADED; "P1" still in force |
| TC-E1-061-03 | AC3 | Component | Evaluation "EV-INTAKE-002" RUNNING; 409 with MSG-P10-008 and no report body |
| TC-E1-061-04 | AC4, BR2 | Component | L1 policy file without measures; 422 with MSG-P10-001 naming "measures to watch present" |
| TC-E1-061-05 | AC5, BR2 | Component | NO_CONTACT_POINT agreement 0.8150; 422 with MSG-P10-001 naming "NO_CONTACT_POINT 0.8150 below 0.85" |
| TC-E1-061-06 | AC6, BR4 | Component | Evaluation "EV-INTAKE-003" with sample size 150; 422 with MSG-P10-001 naming "sample size at least 200" |
| TC-E1-061-07 | AC7, BR6 | Component | Loader "coe.user01" approves version "P2"; 409 with MSG-P7-002 and the version stays LOADED |
| TC-E1-061-08 | X6, access | Contract | RW-CASEOWN requests the report and approves a version; refused with 403 and MSG-P4-002 |

TC-E1-061-01 to TC-E1-061-07 are the legacy test cases of RWB-E1-061, kept with their legacy IDs and their legacy data; the legacy "System" level maps to Component here, because the cross-service behaviour of this key is proved against the contract fakes and the contract tests of RWB-P10-E1061-CON rather than on the real services. TC-E1-061-08 is the legacy access test case, mapped to Contract because its subject is the refusal of a consumed operation at the boundary. The contract-level facts of the service placement - the base of the report operation, the four columns of the migration, the shape of the L1 payload, the topic and the four fakes - are tested by TC-P10-E1061-CON-01 to TC-P10-E1061-CON-06 in RWB-P10-E1061-CON and are not duplicated here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the minimum sample 200, the promotion check list, the three lists, the check names and the message IDs are parameter and reference values read at run time, and a missing value refuses the load instead of falling back to a default (BR3, BR4).
- No personal data in logs, tests or the report: the report holds counts, rates, versions and durations only, the fixtures are synthetic, and no account number, national ID number or name appears in a log, a CSV or a PDF (BR5).
- No read of another service's tables and no schema client: the parameter values and the lists come through the rwb-case contracts, the right through rwb-access, and no foreign key crosses a schema (DP-01, DP-06, DP-07).
- The only table this story writes is agent_policy, in `rwb_agent`, and the four promotion columns arrive only by `V10_004__policy_promotion.sql` (BR8, DP-15).
- A proposal never changes the mode in force before it is approved and its valid from date is reached, and the loader and the approver are different people (BR6, R-UNI-32).
- One hop and a 2 s client budget on every consumed REST call; the model budget belongs to the agent platform and is never a REST budget of this story (DP-11, ADR-020).
- The reads are reached through the gateway-bff route and never from a screen to the service (DP-19).
- The report publishes no event and writes no decision record: the run, the score and the version rows are internal to rwb-agent and are read through its own contract.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | Business Requirements Program, section 5.7; Business Requirements Epic 1, section 3.9 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32 | TC-E1-061-01, TC-E1-061-02, TC-E1-061-03, TC-E1-061-04, TC-E1-061-05, TC-E1-061-06 |
| REQ-DRI-011 | Every versioned table has valid from and to dates, author and approver | Business Requirements Program, section 5.7; Business Requirements Epic 1, section 3.9 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E1-061-02, TC-E1-061-07, TC-E1-061-08 |
| D-RCV-60 DP-01 | The evaluation run, score and shadow rows and the policy row are owned by rwb-agent in schema `rwb_agent` | Business Requirements Epic 1, section 3.9; Template and Rules §R5.5 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E1-061-01, TC-E1-061-02 |
| D-RCV-60 DP-06 | The minimum sample and the promotion check list are parameter values read through the rwb-case parameters contract | Template and Rules §R5.5 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E1-061-04, TC-E1-061-05, TC-E1-061-06 |
| D-RCV-60 DP-07 | LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-EVAL-STATUS are read through the rwb-case reference-data contract | Template and Rules §R5.5 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E1-061-02, TC-E1-061-07 |
| D-RCV-60 DP-13 | The report operation is served on the base `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E1-061-01, TC-E1-061-03 |
| D-RCV-60 DP-15 | The four promotion columns arrive with the service's own migration in its own Flyway sequence | Template and Rules §R5.5; ADR-021 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E1-061-02, TC-E1-061-06 |
| D-RCV-60 DP-19 | The report and version reads are reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E1-061-01, TC-E1-061-08 |
| R-UNI-32 | An agent that does not answer inside its budget falls back to the rule result and the fallback is recorded | Business Rules and Routing Logic, R-UNI-32 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32 | TC-E1-061-02 |
| RWB-E1-061 (legacy story) | Intake agent evaluation and L1 proposal [E2a]: the seven criteria AC1 to AC7 and the access test | Business Requirements Epic 1, section 3.9 | FEAT-AGT-07 | 06 Take over and own the case | None | The eight legacy test cases of section 16 |
| RWB-P10-E1061-CON (contract story) | The evaluation start, read and report operations, the L1 payload, the approval, the topic and the four fakes, tested at contract level | Business Requirements Epic 1, section 3.9 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-P10-E1061-CON-01 to TC-P10-E1061-CON-06 |

The gap GAP-0612 records the areas the sources leave open for this story - the service login, the owner of the minimum sample, the split of the evaluation operations between the two app stories, the route path in front of the reads, the source of the three lists and the flag of the promotion - and each default it raises is settled by ASM-0869 to ASM-0874.

### 19. Out of scope

- Showing the intake summary to case owners at L1 (RWB-E2-028).
- Changing an autonomy level from a screen (FEAT-AGT-12, Epic 3).
- The steering committee meeting itself and its minutes.
- The agent platform, the prompt and policy store, the configuration operations and the business runs of RWB-P10-E1058-APP, and the evaluation harness of RWB-P10-E1060-APP.
- The parameter rows and the reference rows themselves: P3 rwb-case, RWB-P3-E1042-CON and RWB-P3-E1043-CON, reached only through their contracts.
- The right check and its roles: P4 rwb-access.
- The contract, database, operations and infrastructure stories of the legacy key, and the deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook.
- The gateway-bff route name and path in front of the reads, which are Not specified in the source documents (GAP-0612; ASM-0872).
