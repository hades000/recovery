# RWB-ITG-E1058-ITG Agent platform set-up [E1a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1058-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-058 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P10-E1058-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-058 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer** proving the agent platform end to end on the real SIT services of rwb-agent (P10), rwb-source-data (P1), rwb-case (P3), rwb-access (P4) and rwb-document (P5), I want **one suite that loads, approves, runs, checks, scores and reports a test agent through every service the platform touches**, so that **the gateway, the versioned prompt and policy store, the guardrail checker, the tool path, the masking path, the idempotency and the evaluation harness are proved on real services, with the versions recorded, before wave 1 exits**.

### 2. Business rationale

Every later agent in the programme - the case intake agent, the extraction evaluation, the route agent and the deviation screening agent - is called through one path: an approved policy and prompt version, a model call through the gateway, a guardrail check, one run row with its versions, and a score when the agent is evaluated. RWB-E1-058 defined that path when all of it lived in one module. In the target it is still owned by one service, rwb-agent (P10), but it is no longer delivered by one service: the run reads case facts from rwb-case (P3) and extracted document fields from rwb-document (P5) through the tool gateway, it masks personal values through rwb-access (P4) before any value reaches a prompt, it takes its reference and dictionary facts from rwb-source-data (P1) and rwb-case, and it announces every finished run on its own topic for rwb-decision and the consumers of `rwb.agent.events.v1`.

The component copy of the behaviour is RWB-P10-E1058-APP. That story builds and unit-tests the six tables, the four components and the eight endpoints inside rwb-agent, against the published contracts of its neighbours. This integration story exists because four of the facts that make the platform trustworthy cannot be proved inside one service, and because the legacy story leaves no criterion that a single service can sign off on its own:

- The version record and the run record are one fact about the case: a run that used prompt version "PR1" on 2026-11-19 and "PR2" on 2026-11-20 can only be asserted by reading the run rows through the P10 contract after the version was approved through the same contract, with the older version still readable.
- The masked request is a fact that spans two services: rwb-agent builds the prompt, but the masking tokens come from rwb-access, and the assertion is that neither the request body, nor the run row, nor the application log holds a national ID number, a phone number, a name or an account number.
- The tool path is a fact about three services: the agent asks for `read_case`, and the answer comes from rwb-case or rwb-document through its published contract under the identity SY-AGENT; a refused tool (`propose_deviation`) must leave the run in GUARDRAIL_FAILED and hand the calling step back to the rule result.
- The fallback is a fact about the caller: a step inside rwb-case or rwb-document that reaches the agent through the agent runtime client and AgentRunWorkflow must still get a rule result inside its own budget when the model does not answer in 60 seconds, and no calling service may reach the agent by a direct REST call.

The suite therefore carries no legacy criterion: every criterion of this story is new (D-RCV-60) and is written to prove the deliverable in the title on real services, with the legacy values of RWB-E1-058 (agent "ECHO", policy "P1", prompt "PR1", model "MODEL-A-2026-10", 60 seconds, confidence floor 0.80, allowed tool `read_case`, 1,200 ms and 900/150 tokens, 0.0500 baht per 1,000 tokens) so that a reader can follow the legacy story beside it.

The only thing that is faked is the outside world: INT-23, the enterprise model endpoint, is reached through a recorded external stub that carries its OpenAPI 3.1 contract, because no suite may call a live model endpoint with real prompts, and a clock and four fault switches (timeout, schema, floor, tool) are needed to reach the exception paths deterministically. P1, P3, P4 and P5 are the real services on their published SIT contracts, and a run that needs a fake for any of them fails the preflight, because a fake would defeat the purpose of the run.

The measures the story is read against are the same as the legacy story: the agent fallback rate, target below 10 percent per month, read from the agent run table through the P10 contract, and a failure count per guardrail check code. The evaluation report carries the legacy score rows (sample size, true positives, false positives, false negatives, precision and recall) and the three versions, and the agent-outputs read carries the run id, outcome, fallback and output reference without prompt text (ASM-0504).

### 3. Preconditions

- RWB-P1-E1001-APP is done: the source-data tables, the ACE view contract and the extension tables are in place in rwb_source_data, so the case, party and product facts the tool path reads are available through the P1 contract.
- RWB-P1-E1069-APP is done: the data products, their freshness and the data dictionary over tables and fields are published, including the field list the suite reads for the agent tables.
- RWB-P10-E1058-APP is done: rwb-agent is deployed with schema `rwb_agent`, the six tables (agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run, agent_evaluation), the gateway client, the orchestrator, the guardrail checker, the evaluation harness and the eight admin operations of section 12.2.
- The published contracts of P1, P3, P4 and P5 are versioned in the registry, and the suite consumes only those contracts.
- The test agent "ECHO" exists with policy version "P1" approved (model "MODEL-A-2026-10", timeout 60 seconds, confidence floor 0.80, allowed tools `read_case`, price 0.0500 baht per 1,000 tokens) and prompt version "PR1" approved, loaded by RW-COE and approved by RW-RISK.
- The service identity SY-AGENT exists with its managed identity and the seeded permissions Case record R, Documents R, Rules and parameters R, Reference data R and Decision log C, and rwb-access answers the masking request for it.
- The INT-23 stub is deployed with its OpenAPI 3.1 document, its 1,200 ms answer with 900 input and 150 output tokens, its clock and its four fault switches.
- The harness RWB-ITG-W1J01-ITG is available with the synthetic case set, the synthetic identities and the topic, queue and namespace wiring of wave 1.
- The SIT environment is available with the Temporal namespace `rwb-recovery`, queue `rwb-agent`, topic `rwb.agent.events.v1` with its retry and `.dlt` topics, `rwb.decision-record.v1` and the schema registry.
- No production data is read, copied or connected to; every case number, borrower, national ID number, mobile number, account number and identity used by the run is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: runs the preflight, which reads the OpenAPI documents of P1, P3, P4, P5 and P10 and the AsyncAPI document of `rwb.agent.events.v1`, and fails before any assertion if a path, a field, a status code or an event schema has drifted; it also confirms that no fake is configured for P1, P3, P4 or P5.
2. Harness: loads prompt version "PR2" for agent "ECHO" through `POST /api/recovery/agent/v1/admin/agent-configs` as RW-COE with valid from 2026-11-20, then approves it as RW-RISK through `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve`, and reads both versions back through `GET /api/recovery/agent/v1/admin/agent-configs` to confirm "PR1" is still readable with its text hash unchanged.
3. Harness: moves the run clock to 2026-11-19 and back to 2026-11-20, and asserts through the P10 run read that the first run names prompt version "PR1" and the second names "PR2".
4. Harness: seeds the synthetic case "RW-2026-000101" in rwb-case through the W1J01 set, so `GET /api/recovery/case/v1/cases/{caseId}` answers with the facts the tool path reads.
5. Harness: asks the agent orchestrator of rwb-agent to run agent "ECHO" for case "RW-2026-000101" with the idempotency key of the run, in the same way a calling step does; the run resolves the approved policy and prompt in force, reads `read_case` through the tool gateway as SY-AGENT, masks the values through rwb-access, calls INT-23 through the gateway client with the policy timeout, checks the answer and records one run row.
6. Harness: consumes `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` and asserts the envelope, the run ID, agent "ECHO", the case ID, outcome "ANSWERED" and fallback false, and that the event was written to the outbox in the same transaction as the run row.
7. Harness: reads the run back through `GET /api/recovery/agent/v1/admin/agent-runs` and asserts agent "ECHO", agentVersion "ECHO@P1/PR1", the case ID, outcome "ANSWERED", fallback false and latencyMs 1,200; it reads the run row facts (policy "P1", prompt "PR1", model "MODEL-A-2026-10", 900 and 150 tokens, 0.0525 baht) through the same contract and through `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs`, never through a table.
8. Harness: consumes `DecisionRecorded` on `rwb.decision-record.v1` for the step that called the agent, and asserts that the decision of the calling step names the agent run ID and the rule result it fell back to; the agent itself records no decision of its own.
9. Harness, exception paths: switches INT-23 to the timeout, schema, floor and tool faults in turn and asserts TIMED_OUT at 60,000 ms, GUARDRAIL_FAILED with check code "SCHEMA", BELOW_FLOOR at 0.79 and GUARDRAIL_FAILED with check code "TOOL_NOT_ALLOWED", each with fallback true and each leaving one run row.
10. Harness, masking: seeds the synthetic national ID number and mobile number on case "RW-2026-000103", runs the agent, and asserts the masking tokens of rwb-access in the recorded request and the absence of any personal value in the request body, the run row and the application log.
11. Harness, refusals: loads a policy file with timeout_seconds 0 and asserts 422 with MSG-P10-001 and no new version; has synthetic user "U-4101" load and then approve its own version and asserts 409 with MSG-P7-002 and status LOADED; has two RW-RISK approvals of the same row version and asserts one 200 and one 409 with MSG-GEN-004; repeats a run request with the same idempotency key and asserts one run row and one model call; calls the admin operations as synthetic user "RW-CASEOWN" and asserts 403 with MSG-P4-002.
12. Harness: loads labeled sample "ECHO-S1" version 1 with 20 rows through `POST /api/recovery/agent/v1/admin/agent-samples`, starts the evaluation through `POST /api/recovery/agent/v1/admin/agent-evaluations`, polls `GET /api/recovery/agent/v1/admin/agent-evaluations` to status "DONE", and reads the scores: 20 run rows with trigger "EVALUATION" and mode "SHADOW", one score row per label key with sample size, true positives, false positives, false negatives, precision and recall, each carrying policy "P1", prompt "PR1" and model "MODEL-A-2026-10".
13. Harness: starts an evaluation on sample "ECHO-S2" with 0 rows and asserts 422 with MSG-P10-002 and no run row; starts the same evaluation again while it is RUNNING and asserts 409 with MSG-P10-003 and one RUNNING row.
14. Harness, callers: drives a step inside rwb-case (P3) and a step inside rwb-document (P5) through the agent runtime client of the platform contract, with INT-23 silent for 61 seconds, and asserts AgentRunWorkflow on queue `rwb-agent`, one run row, fallback true, the rule result returned to the step and its decision record, and no direct REST call from the calling service to rwb-agent.
15. Harness: reads the evaluation report through `GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report` and asserts precision, recall, sample size, the three versions and the absence of any personal value; then cleans up the synthetic set, the two business dates, the sample and the evaluation run and writes the evidence report with one verdict per test case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | INT-23 does not answer within the policy timeout of 60 seconds | Run status TIMED_OUT, fallback true, latency 60,000 ms; the calling step uses the rule result (R-UNI-32) | None to a user | AC6, AC17 |
| X2 | The answer fails its output schema | Run status GUARDRAIL_FAILED, check code SCHEMA with the missing field name, fallback true; the failure count for the code rises by 1 | None to a user | AC3 |
| X3 | The agent asks for a tool that is not on its allowed list | The tool call is refused and logged, the run is GUARDRAIL_FAILED with check code TOOL_NOT_ALLOWED, fallback true | None to a user | AC5 |
| X4 | The answer confidence is below the policy confidence floor | Run status BELOW_FLOOR, fallback true | None to a user | AC10 |
| X5 | A prompt, policy or sample file fails a load check | The load is refused in full, the version in force is unchanged, no new version row exists | MSG-P10-001 | AC8 |
| X6 | The person who loaded a version tries to approve it | The approval is refused, the version stays LOADED | MSG-P7-002 | AC9 |
| X7 | Two approvals of the same row version arrive at once | The first approves, the second is refused with 409 | MSG-GEN-004 | AC12 |
| X8 | The same run request arrives twice with the same idempotency key | One run row and one model call; the repeat returns the first result and the idempotency hit is counted (R-UNI-40) | None to a user | AC11 |
| X9 | An evaluation is started on a sample with no labeled rows for the agent | Refused with 422, no evaluation run and no run row | MSG-P10-002 | AC13 |
| X10 | An evaluation is started while one for the same agent and sample is running | Refused with 409, one RUNNING row stays | MSG-P10-003 | AC14 |
| X11 | A role without Platform administration R calls an admin operation | Refused with 403, nothing changes | MSG-P4-002 | AC16, TC-E1-058-16-ITG |
| X12 | A consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1 |
| X13 | A fake is configured for P1, P3, P4 or P5 | The preflight refuses the run: only INT-23, the clock and the four fault switches may be stubbed | None | Section 12.8 |
| X14 | The INT-23 stub drifts from its OpenAPI 3.1 document | The preflight fails on the stub contract test, so no assertion is made against an endpoint that no longer matches | None | AC1, AC6 |
| X15 | The W1J01 synthetic set, or the synthetic identity or sample it carries, is missing or does not match the run | The run fails as a fixture fault and names the missing element; no production value is substituted | None | AC1, AC4, AC16 |
| X16 | A suite step tries to read a service schema directly | The step does not exist: the suite is built with no client for a service schema, and the pipeline scan fails any change that adds one | None | Section 17 |

X1 to X11 are the legacy exception paths of RWB-E1-058 carried onto the real services; X12 to X16 are the failures that only appear when the run leaves one service. X11 is proved by the access test rather than by an acceptance criterion of its own, as in the legacy story, and is covered by AC16 here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the three integration dependencies and the published contracts of P1, P3, P4, P5 and P10, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval, the report layout and the fault-switch names are configuration; the agent, the policy and prompt versions, the model version, the timeout, the floor, the tool list, the price, the statuses and the message IDs are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: a run row and its event in one transaction, version dating, schema, floor and tool checks, masking before the prompt, the tool path, five refusals, idempotency and an evaluation with its versions |
| Estimable | One suite module, one external stub control, one fixture builder, five contract probes, one evaluation driver and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a REST response, a Kafka event, a run row read through the contract, a score row, a log scan or an evaluation report |

### 7. Acceptance criteria

```gherkin
Feature: Agent platform set-up [E1a], proven across the wave 1 services

  Background:
    Given the test agent "ECHO" has policy version "P1" approved with model "MODEL-A-2026-10", timeout 60 seconds, confidence floor 0.80 and allowed tools "read_case"
    Given prompt version "PR1" is approved for agent "ECHO"
    Given the model endpoint stub answers in 1,200 milliseconds with 900 input tokens and 150 output tokens
    Given the policy price is 0.0500 baht per 1,000 tokens
    Given all involved services are deployed in SIT with their published contracts and SY-AGENT holds Case record R, Documents R, Rules and parameters R, Reference data R and Decision log C
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded and no production value is used

  Scenario: AC1 An approved endpoint returns one run row and one event (new, D-RCV-60)
    Given the approved model endpoint INT-23 is reachable on the private endpoint of the SCB tenant through the recorded external stub of its OpenAPI 3.1 contract
    When the orchestrator of rwb-agent runs agent "ECHO" for case "RW-2026-000101"
    Then the call succeeds with run status "ANSWERED"
    Then one agent run row holds agent "ECHO", policy version "P1", prompt version "PR1", model version "MODEL-A-2026-10", latency 1,200 ms, tokens in 900, tokens out 150 and cost 0.0525 baht
    Then the system writes one `rwb.agent.AgentRunCompleted.v1` event to the outbox in the same transaction as the run row, with the run ID, agent "ECHO", the case ID, outcome "ANSWERED" and fallback false
    Then the event is delivered to `rwb.agent.events.v1` and no personal field is present in it

  Scenario: AC2 Prompt versions take effect on their valid-from date and stay readable (new, D-RCV-60)
    Given prompt version "PR1" is in force for agent "ECHO"
    When RW-COE loads prompt version "PR2" and RW-RISK approves it with valid from 2026-11-20
    Then prompt version "PR2" exists with status "APPROVED" on `GET /api/recovery/agent/v1/admin/agent-configs`
    Then prompt version "PR1" stays readable through the same operation with its text hash unchanged
    Then a run on 2026-11-19 uses "PR1" and a run on 2026-11-20 uses "PR2"

  Scenario: AC3 A schema failure sets GUARDRAIL_FAILED and fallback (new, D-RCV-60)
    Given the model stub returns an answer with field "summary" missing from the output schema of "ECHO"
    When the guardrail runs
    Then the system rejects the output with run status "GUARDRAIL_FAILED" and fallback true
    Then the guardrail result holds check code "SCHEMA" with the missing field name
    Then the count of check code "SCHEMA" failures for "ECHO" on the business date rises by 1
    Then the calling step receives the rule result

  Scenario: AC4 An evaluation scores 20 labeled rows with the versions recorded (new, D-RCV-60)
    Given labeled sample "ECHO-S1" version 1 with 20 rows for agent "ECHO"
    When RW-COE starts the evaluation of "ECHO" on "ECHO-S1" through `POST /api/recovery/agent/v1/admin/agent-evaluations`
    Then one evaluation run ends with status "DONE" and 20 agent run rows with trigger "EVALUATION" and mode "SHADOW"
    Then one score row per label key holds sample size, true positives, false positives, false negatives, precision and recall
    Then each score row holds policy version "P1", prompt version "PR1" and model version "MODEL-A-2026-10"

  Scenario: AC5 A tool outside the allow-list is refused (new, D-RCV-60)
    Given an agent with the allowed tool list "read_case"
    When it calls the tool "propose_deviation", which is not on its list
    Then the system refuses the tool call and it is not executed
    Then the agent run holds status "GUARDRAIL_FAILED", check code "TOOL_NOT_ALLOWED" and fallback true
    Then the orchestrator returns a fallback result with reason "TOOL_NOT_ALLOWED" so the calling step takes the rule path

  Scenario: AC6 A model that does not answer inside 60 s ends TIMED_OUT with fallback (new, D-RCV-60)
    Given the model stub does not answer for 61 seconds
    When the orchestrator runs agent "ECHO" for case "RW-2026-000102"
    Then the system ends the call at 60 seconds
    Then the agent run holds status "TIMED_OUT", fallback true and latency 60,000 ms
    Then the orchestrator returns a fallback result with reason "TIMED_OUT" (R-UNI-32)

  Scenario: AC7 Personal data is masked before the model call (new, D-RCV-60)
    Given case "RW-2026-000103" has a borrower with a synthetic national ID number and a synthetic mobile number
    When the orchestrator builds the request to the model endpoint
    Then the request body holds the masking tokens returned by the P4 masking service for SY-AGENT
    Then the request body, the agent run row and the application log hold no national ID number, phone number, name or account number

  Scenario: AC8 A policy file with timeout_seconds 0 is refused in full (new, D-RCV-60)
    Given a policy file for agent "ECHO" with timeout_seconds 0
    When RW-COE loads it through `POST /api/recovery/agent/v1/admin/agent-configs`
    Then the system refuses the load with 422 and MSG-P10-001 naming check "timeout_seconds between 1 and 120"
    Then policy version "P1" stays in force and no new version row exists

  Scenario: AC9 The loader cannot approve their own version (new, D-RCV-60)
    Given synthetic user "U-4101" loaded policy version "P2" for agent "ECHO"
    When "U-4101" calls `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` for "P2"
    Then the system refuses the approval with 409 and MSG-P7-002
    Then version "P2" keeps status "LOADED"

  Scenario: AC10 An answer at confidence 0.79 against floor 0.80 is BELOW_FLOOR (new, D-RCV-60)
    Given the model stub returns a valid answer with confidence 0.79
    When the guardrail runs with confidence floor 0.80
    Then the agent run holds status "BELOW_FLOOR" and fallback true
    Then the orchestrator returns a fallback result with reason "BELOW_FLOOR"

  Scenario: AC11 A repeated run request makes no second run or model call (new, D-RCV-60)
    Given agent "ECHO" ran for case "RW-2026-000101" with idempotency key "ECHO:RW-2026-000101:2026-11-30"
    When the same request arrives again with the same key
    Then no second agent run row and no second model call exist
    Then the system returns the first result and the idempotency hit is counted (R-UNI-40)

  Scenario: AC12 Two approvals at once: one succeeds, one 409 (new, D-RCV-60)
    Given policy version "P2" for agent "ECHO" has status "LOADED" and row version 1
    When two RW-RISK users approve "P2" at the same time
    Then one approval succeeds and "P2" has status "APPROVED"
    Then the system refuses the other with 409 and MSG-GEN-004

  Scenario: AC13 An evaluation on a sample with 0 rows is refused (new, D-RCV-60)
    Given sample "ECHO-S2" has 0 labeled rows for agent "ECHO"
    When RW-COE starts the evaluation of "ECHO" on "ECHO-S2"
    Then the system refuses the request with 422 and MSG-P10-002
    Then no evaluation run and no agent run row exist

  Scenario: AC14 A second evaluation while one runs is refused (new, D-RCV-60)
    Given the evaluation of "ECHO" on "ECHO-S1" version 1 has status "RUNNING"
    When RW-COE starts the same evaluation again
    Then the system refuses the request with 409 and MSG-P10-003
    Then one evaluation run exists for "ECHO" on "ECHO-S1" version 1 with status "RUNNING"

  Scenario: AC15 Agent runs are listed without prompt text, answer or personal field (new, D-RCV-60)
    Given 3 runs of agent "ECHO" between 2026-11-30 and 2026-12-01
    When RW-PLATADM calls `GET /api/recovery/agent/v1/admin/agent-runs` with agent "ECHO", from "2026-11-30" and to "2026-12-01"
    Then 3 AgentRun items return with id, agent, agentVersion, caseId, outcome, fallback and latencyMs
    Then no item holds the prompt text, the model answer or a personal field

  Scenario: AC16 A role without Platform administration R is refused (new, D-RCV-60)
    Given synthetic user "RW-CASEOWN" holds no Platform administration R right and the suite confirms it on `GET /api/recovery/access/v1/me/session`
    When "RW-CASEOWN" calls `GET /api/recovery/agent/v1/admin/agent-runs` and `POST /api/recovery/agent/v1/admin/agent-configs`
    Then both calls are refused with 403 and MSG-P4-002
    Then no agent run row and no configuration version row changes

  Scenario: AC17 Another service reaches the agent through the agent runtime client and AgentRunWorkflow (new, D-RCV-60)
    Given a calling step in rwb-case (P3) and a calling step in rwb-document (P5) use the agent runtime client of the platform contract
    When the step runs agent "ECHO" for case "RW-2026-000102" and the model stub does not answer for 61 seconds
    Then AgentRunWorkflow runs on queue "rwb-agent" with the 60 second budget of the policy and ends with status "TIMED_OUT"
    Then one agent run row exists for the call and fallback is true
    Then the calling step takes the rule result and records it in its decision on `rwb.decision-record.v1`
    Then no direct REST call from the calling service to rwb-agent is made

  Scenario: AC18 The evaluation report holds the measures, versions and no personal data (new, D-RCV-60)
    Given the evaluation of "ECHO" on "ECHO-S1" version 1 ended with status "DONE"
    When RW-COE reads `GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report`
    Then the report holds precision and recall, the sample size 20, and policy version "P1", prompt version "PR1" and model version "MODEL-A-2026-10"
    Then the report holds no national ID number, phone number, name or account number
```

**Target reading.** The agent, its policy and prompt versions, the model version, the timeout, the confidence floor, the tool list, the price and the statuses are the legacy values of RWB-E1-058, copied character for character; the agent tables are the P10 tables in schema `rwb_agent` (DP-01), the topic is `rwb.agent.events.v1` with CloudEvents and an outbox (DP-09), the base is `/api/recovery/agent/v1` (DP-13) and the queue is `rwb-agent`. The in-process `AgentOrchestrator` of the legacy section 12 becomes the P10 contract that a calling service reaches through the agent runtime client and AgentRunWorkflow (DP-20), so AC17 asserts the workflow and the rule result rather than a Java interface. The evaluation report and the agent-outputs read carry the measures of the legacy score rows, and their response shape is the one named by the contract reads of section 12.2 (ASM-0504).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every model call goes through the model gateway client of rwb-agent to the endpoint chosen under DL33, reached on its private endpoint; no other component and no calling service calls the endpoint | DL33; INT-23; DP-20 |
| BR2 | The orchestrator uses the policy and prompt versions in force on the run date with status APPROVED, read from the P10 rows of schema `rwb_agent`; an open run keeps the version it started with | agent_policy.valid_from (DF-AGT-022); R-UNI-38 |
| BR3 | If the endpoint does not answer within agent_policy.timeout_seconds (60, assumed; DL11), the run ends TIMED_OUT and the calling step uses the rule result | R-UNI-32; NFR-010; AgentRunWorkflow |
| BR4 | Every answer is checked in this order: output schema, allowed tool list, confidence floor; the first failed check sets the status and fallback is true | agent_policy.output_schema_ref, allowed_tools, confidence_floor (DF-AGT-006, 007, 011) |
| BR5 | Personal values are masked by rwb-access before any value reaches a prompt, and the request body, the run row and the log hold the masking tokens only | CTL-11; REQ-ACA-005; DP-08 |
| BR6 | The agent runs as SY-AGENT and passes the same permission check as a person on every tool call; a case read goes to rwb-case and a document read goes to rwb-document through its published contract, never to a table | REQ-ACA-010; role SY-AGENT; DP-01; DP-11 |
| BR7 | Cost of a run = (tokens in + tokens out) / 1,000 x agent_policy.price_per_1k_tokens_thb, rounded to 4 decimals; the price is 0.0500 baht under DL33 | agent_policy.price_per_1k_tokens_thb (DF-AGT-014); DL33 |
| BR8 | A prompt or policy version is loaded by RW-COE and approved by RW-RISK; the same person may not do both | CTL-08; separation of duty |
| BR9 | A run request with an idempotency key already used returns the first result, with one run row and one model call | R-UNI-40 |
| BR10 | A file load is refused in full if any row fails a check, and the version in force is unchanged | Principle 1; CTL-08 |
| BR11 | No business value (model name, threshold, timeout, price, tool list) is written in code; the suite reads every one of them through the P10 contract | Principle 1; DT02 |
| BR12 | The run row and its `rwb.agent.AgentRunCompleted.v1` event are written in one transaction through the outbox, and the event carries IDs and facts only | ADR-015; DP-09; Arch v5 slide 16 |
| BR13 | An evaluation runs the agent in shadow on every labeled row and stores one score row per label key with its policy, prompt and model versions; an empty sample is refused and one RUNNING run per agent and sample is allowed | agent_evaluation_run (DF-AGT-070 to 083); agent_evaluation (DF-AGT-086 to 096) |
| BR14 | Every REST call of the run is one hop to the owning service with a 2 s client budget; the 60 s model budget is the workflow budget of AgentRunWorkflow and is never a REST budget of a caller | ADR-020; DP-11; Arch v5 slide 16 |
| BR15 | Prompt text and model answers never appear in an API response of a listing, in an event, in a workflow history or in the application log; the run read returns id, agent, agentVersion, caseId, outcome, fallback and latencyMs only | Legacy section 12 and 17; Arch v5 slide 42 notes |
| BR16 | No cross-service table read: the suite and every service read another service's data through its contract, and the P1 data dictionary is the only view the suite takes of the agent tables | DP-01; DP-05; ADR-020 |
| BR17 | The source facts a tool returns come from rwb-source-data (P1) through its contract, and the reference data and parameters come from rwb-case (P3) through its contracts, never from a copy in `rwb_agent` | DP-05; DP-06; DP-07 |
| BR18 | No production value is read, copied or connected to; every case, party, national ID number, mobile number, account number and identity of the run is synthetic, and the suite refuses to start outside SIT | Legacy section 17; Guardrail |

### 9. State transitions

The state transitions of an agent configuration version:

| From | Event | Condition | To |
|---|---|---|---|
| None | Configuration file loaded | Every check passes | LOADED (agent_policy.status or agent_prompt.status) |
| None | Configuration file loaded | A check fails | No row; load refused (MSG-P10-001) |
| LOADED | Approved by RW-RISK | Approver is not the loader and the row version still matches | APPROVED |
| LOADED | Approved by the loader | None | LOADED, approval refused (MSG-P7-002) |
| LOADED | Two approvals at once | The second finds the row changed | APPROVED for the first, 409 MSG-GEN-004 for the second |
| APPROVED | A later version is approved | Later valid from date reached | RETIRED (valid_to set to the day before) |

The state transitions of an agent run:

| From | Event | Condition | To |
|---|---|---|---|
| None | Run requested | Answer passes every check | ANSWERED (agent_run.status) |
| None | Run requested | The endpoint does not answer in 60 seconds | TIMED_OUT, fallback true |
| None | Run requested | The output schema check fails | GUARDRAIL_FAILED, check code SCHEMA, fallback true |
| None | Run requested | The tool allow-list check fails | GUARDRAIL_FAILED, check code TOOL_NOT_ALLOWED, fallback true |
| None | Run requested | The confidence is below the floor | BELOW_FLOOR, fallback true |
| None | The same idempotency key arrives again | A run row already exists | No transition; the first result is returned |

The state transitions of an evaluation:

| From | Event | Condition | To |
|---|---|---|---|
| None | Evaluation started | The sample has rows and none is running | RUNNING (agent_evaluation_run.status) |
| None | Evaluation started | The sample has 0 labeled rows | No row; 422 MSG-P10-002 |
| None | Evaluation started | One for the same agent and sample version is RUNNING | No row; 409 MSG-P10-003 |
| RUNNING | Last sample row scored | None | DONE |

The states the run observes across the services:

| Item | States |
|---|---|
| INT-23 stub | Answering in 1,200 ms, silent for 61 seconds, schema fault, floor fault, tool fault |
| Agent run | ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, each with fallback true or false |
| Evaluation run | RUNNING, DONE |
| Suite run | Not started, preflight failed, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the stub control and its fault switches, the clock, the cleanup and the evidence report |
| RW-COE, centre of excellence analyst | Loads prompt, policy and sample files; starts and reads evaluations; reads versions and scores (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves prompt and policy versions (Rules and parameters A); reads scores and the evaluation report |
| RW-PLATADM, platform administrator | Reads agent runs (Platform administration R); runs the gateway configuration per environment |
| RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs (Platform administration R); RW-SECADM may decode a payload under break-glass, which this story does not use |
| SY-AGENT, agent platform | Runs agents; reads case facts from rwb-case and extracted fields from rwb-document through the tool gateway (R); reads reference data and parameters (R) |
| Service owner of rwb-agent (P10) | Owns the six tables, the gateway client, the orchestrator, the guardrail checker, the evaluation harness, the eight admin operations, the topic and queue `rwb-agent` |
| Service owner of rwb-source-data (P1) | Owns the data dictionary read and the source facts the tool path returns |
| Service owner of rwb-case (P3) | Owns the case read the tool path uses and the parameters and reference data |
| Service owner of rwb-access (P4) | Owns the masking service, the right check, the session read and the refusal of MSG-P4-002 |
| Service owner of rwb-document (P5) | Owns the document read the tool path uses |
| No role | Reads a service schema directly, writes an agent table from outside rwb-agent, or takes production data into the run |

Approval levels: no delegation of authority level applies; the approval of a version is the Rules and parameters A right, as in the legacy story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 contract; seeded synthetically |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 contract; seeded synthetically |
| DF-CAS-012 | recovery_case | region_code | Read through the P3 contract; seeded synthetically |
| DF-REF-012 | rule_row | valid_from | Read through the P7 contract (version-in-force pattern only; no rule row is written) |
| DF-AGT-001 to DF-AGT-016, DF-AGT-021 to DF-AGT-025 | agent_policy | id, agent_code, policy_version, model_code, model_version, output_schema_ref, allowed_tools, autonomy_mode, segment_product_group, segment_region_code, confidence_floor, timeout_seconds, daily_cost_cap_thb, price_per_1k_tokens_thb, alert_role, review_date, status, valid_from, valid_to, loaded_by, approved_by | Read through the P10 contract; written by rwb-agent (owner P10, schema `rwb_agent`) |
| DF-AGT-026 to DF-AGT-035 | agent_prompt | id, agent_code, prompt_version, body_text, body_hash, status, valid_from, valid_to, loaded_by, approved_by | Read through the P10 contract, except body_text, which is never returned; written by rwb-agent (owner P10) |
| DF-AGT-036 to DF-AGT-057 | agent_run | id, agent_code, agent_version, prompt_version, model_version, case_id, subject_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, guardrail_result, output, confidence, latency_ms, tokens_in, tokens_out, cost_thb, data_as_of, run_at, evaluation_run_id | Read through the P10 contract, except output and subject_id, which the listing never returns; written by rwb-agent (owner P10) |
| DF-AGT-061 to DF-AGT-069 | agent_sample | id, agent_code, sample_code, sample_version, subject_type, subject_id, label_key, expected_value, labeled_by | Loaded through the P10 contract; read back as counts only; written by rwb-agent (owner P10) |
| DF-AGT-070 to DF-AGT-083 | agent_evaluation_run | id, agent_code, sample_code, sample_version, policy_version, prompt_version, model_version, status, started_at, finished_at, requested_by, total_cost_thb, p95_latency_ms, failure_counts | Read through the P10 contract; written by rwb-agent (owner P10) |
| DF-AGT-086 to DF-AGT-096 | agent_evaluation | id, evaluation_run_id, approach, label_key, sample_size, true_positive, false_positive, false_negative, agreement_rate, precision_value, recall_value | Read through the P10 contract and the evaluation report; written by rwb-agent (owner P10) |
| DF-ACE fields of the case and party facts | v_ace_* views | the facts the `read_case` tool returns | Read by rwb-source-data only and asserted here through the P1 and P3 contracts; never read by the suite |

Field IDs are those of RWB-E1-058 and are copied unchanged; agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run and agent_evaluation are the P10 tables of schema `rwb_agent` in the ownership map. The suite owns no field and no table: it reads every row of this table through a contract of section 12 and writes only through the admin operations of rwb-agent, with synthetic values. No field ID of agent_alert or agent_feedback is used, because the cost alert and the monitoring dashboard belong to RWB-E1-063 and RWB-E2-031 and are out of scope.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The reserved names of P2 rwb-integration - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` - are not used, and no `rwb_integration` table is written. The agent platform belongs to P10 rwb-agent, base `/api/recovery/agent/v1`, topic `rwb.agent.events.v1`, queue `rwb-agent` and schema `rwb_agent`.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | AC1 and AC15: the run listing - id, agent, agentVersion, caseId, outcome, fallback, latencyMs - with no prompt text, answer or personal field | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | AC2 and AC15: the version list for agent, kind and status, with the text hash and no prompt body | 2 s |
| POST | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | AC2 and AC8: the load of prompt "PR2" and of the policy file with timeout_seconds 0 | 2 s + load time |
| POST | `/api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` | P10 rwb-agent | AC2, AC9 and AC12: the approval, with If-Match on the row version | 2 s |
| POST | `/api/recovery/agent/v1/admin/agent-samples` | P10 rwb-agent | AC4 and AC13: the load of sample "ECHO-S1" version 1 and of the empty "ECHO-S2" | 2 s + load time |
| POST | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | AC4, AC13 and AC14: the start of an evaluation and the two refusals | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | AC4 and AC14: the evaluation run with its score rows, polled to status "DONE" | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report` | P10 rwb-agent | AC18: the evaluation report - precision, recall, sample size and the three versions | 2 s |
| GET | `/api/recovery/agent/v1/cases/{caseId}/agent-outputs` | P10 rwb-agent | AC1: the recorded output of a run for a case, read back through the owner instead of the agent_run table | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC1 and AC7: the case facts the `read_case` tool returns, and the case of a masked run | 2 s |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | AC17: the document facts the tool path returns for the calling step of rwb-document | 2 s |
| GET | `/api/recovery/source-data/v1/admin/data-dictionary/fields` | P1 rwb-source-data | Section 11: the field list of the agent tables, read as a dictionary instead of a table | 2 s |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | AC16: the rights of the caller, which prove that RW-CASEOWN holds no Platform administration R | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the suite calls no service through another service. The 60 second model budget is not a REST budget: it belongs to AgentRunWorkflow of section 12.5.

#### 12.3 Events published

None. The suite publishes no business event; it observes the events of the owning services, listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | What the suite asserts |
|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Exactly one event per run, written to the outbox in the same transaction as the run row; run ID, agent "ECHO", the case ID, outcome "ANSWERED", "TIMED_OUT", "GUARDRAIL_FAILED" or "BELOW_FLOOR", fallback, and no personal field; CloudEvents 1.0, key caseId |
| `DecisionRecorded` | `rwb.decision-record.v1` | every service, ledger in P7 rwb-decision | The decision record of the calling step names the agent run ID and the rule result it fell back to; the agent itself records no decision, so a run that produces no record of its own is the assertion underneath AC17 |

A consumer dedupes on the event ID through its inbox (ADR-015, DP-09). The payload of each event is the owner's published schema; the suite asserts the envelope and the fields above and never the whole body of a prompt or an answer.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (observed, P10) | `rwb-agent` | One run: resolve the approved policy and prompt, run the tool calls, mask, call the gateway with the 60 s budget, check the answer, record the run row and its outbox event; a timeout ends the run TIMED_OUT and returns the rule result to the caller (Arch v5 slide 16: "AgentRunWorkflow: 60 s, then rule result"; DP-20) |

The suite starts no workflow of its own: it calls the agent through the agent runtime client of the platform contract and observes the workflow on queue `rwb-agent` through the Temporal visibility query, with the search attributes of the run. The tool calls and the gateway call are activities of rwb-agent and are observed through the run row and the event, not started by the suite. The timer of the rule fallback inside a case step, and the decision record of that step, are RWB-TE-013 and are out of scope.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story. The evaluation is started by RW-COE through `POST /api/recovery/agent/v1/admin/agent-evaluations` and the run is started by a calling step, so the suite triggers nothing on a cadence and starts no schedule of its own.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The six agent tables of schema `rwb_agent` are owned by P10 rwb-agent and are read through the operations of section 12.2; the case facts, the document facts, the dictionary and the session are read through P3, P5, P1 and P4. No agent_alert, agent_feedback or outbox table is read.

#### 12.8 Contract fakes

None for a service contract. The only fakes are external to the nineteen services:

| Stub | Purpose |
|---|---|
| INT-23 WireMock stub with its OpenAPI 3.1 contract | Stands in for the enterprise model endpoint that no suite may call with real prompts; returns the 1,200 ms answer with 900 input and 150 output tokens, and holds the recorded request for the masking assertion |
| Clock control | Moves the run date between 2026-11-19 and 2026-11-20 for the valid-from assertion of AC2, and places the 3 runs between 2026-11-30 and 2026-12-01 for AC15 |
| Fault switch: timeout | Makes the stub silent for 61 seconds, for AC6 and AC17 |
| Fault switch: schema | Returns an answer with field "summary" missing, for AC3 |
| Fault switch: floor | Returns a valid answer with confidence 0.79, for AC10 |
| Fault switch: tool | Makes the agent ask for `propose_deviation`, for AC5 |

P1 rwb-source-data, P3 rwb-case, P4 rwb-access and P5 rwb-document are the real SIT services on their published contracts and are not faked in the normal path; a run configured with a fake for any of them fails the preflight (X13). The synthetic identities of the run come from the harness RWB-ITG-W1J01-ITG, not from a mock of rwb-access.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 13 | The nine P10 admin and read operations, the P3 case read, the P5 document read, the P1 dictionary read and the P4 session read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 2 event types | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` and `DecisionRecorded` on `rwb.decision-record.v1`; CloudEvents 1.0, key caseId |
| Temporal | None | 1 workflow observed | AgentRunWorkflow on queue `rwb-agent` in namespace `rwb-recovery`; the suite observes it, it starts nothing |
| File | None | None | No file in this story |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a stub control for INT-23 with its clock and four fault switches, a fixture builder for the synthetic cases, identities and samples, a set of contract probes over P1, P3, P4, P5 and P10, an evaluation driver, a masking and log scan, a caller driver for the rule fallback, and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts and the AsyncAPI documents, run order, report and exit code |
| ModelStubControl | Test harness | Deploys the INT-23 stub from its OpenAPI 3.1 document, sets the 1,200 ms answer, the token counts and the four fault switches, and exports the recorded request and the call count |
| ClockControl | Test harness | Moves the run date for AC2 and places the runs of AC15; never changes a service clock |
| ConfigProbe | Test harness | Loads, approves and lists prompt and policy versions; asserts the valid-from behaviour, the text hash, the full refusal of a bad file, the loader-not-approver rule and the two-approval race |
| RunProbe | Test harness | Reads a run through the admin listing and the case agent-outputs read; asserts status, fallback, latency, tokens, cost, the three versions and the absence of prompt text, answer and personal fields |
| EventProbe | Test harness | Consumes `rwb.agent.AgentRunCompleted.v1` and `DecisionRecorded`; asserts one event per run, the outbox fact, the envelope, the key and the absence of a personal field |
| MaskingProbe | Test harness | Seeds the synthetic national ID number and mobile number, asserts the masking tokens in the recorded request and scans the request body, the run row and the application log for any personal pattern |
| ToolPathProbe | Test harness | Asserts that `read_case` is answered through the P3 and P5 contracts as SY-AGENT, and that `propose_deviation` is refused with check code TOOL_NOT_ALLOWED |
| EvaluationDriver | Test harness | Loads a sample, starts an evaluation, polls it to DONE, reads the score rows and the report, and proves the empty-sample and already-running refusals |
| CallerDriver | Test harness | Drives a step in rwb-case and a step in rwb-document through the agent runtime client, observes AgentRunWorkflow, and asserts the rule result and the decision record of the step |
| AccessProbe | Test harness | Reads the caller session through P4 and asserts that RW-CASEOWN is refused with 403 and MSG-P4-002 |
| ReportWriter | Test harness | One row per test case with the evidence and the elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table, no schema object and no migration.

**Configuration and reference data**

- The SIT endpoints of P1, P3, P4, P5 and P10, the topic names `rwb.agent.events.v1` and `rwb.decision-record.v1`, queue `rwb-agent`, namespace `rwb-recovery` and the schema-registry address, all as configuration.
- The synthetic cases RW-2026-000101, RW-2026-000102 and RW-2026-000103, the synthetic user U-4101, the synthetic user RW-CASEOWN and the sample codes ECHO-S1 and ECHO-S2, all from the W1J01 set.
- The agent "ECHO", the policy versions "P1" and "P2", the prompt versions "PR1" and "PR2", the model version "MODEL-A-2026-10", the timeout 60 seconds, the confidence floor 0.80, the allowed tool `read_case`, the price 0.0500 baht per 1,000 tokens, the stub answer 1,200 ms with 900 and 150 tokens, the run dates 2026-11-19, 2026-11-20, 2026-11-30, 2026-12-01 and the valid from 2026-11-20, read through the P10 contract and never written in the suite code (BR11).
- The parameters and reference data the tool path needs, read through the P3 contracts (DP-06, DP-07).
- The 2 s client budget, the evaluation poll interval and the 60 s workflow budget.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

The H and C dependencies of the table stay with the service, platform and operations stories that own them; this story carries none of its own, and an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7). The I list names the three builds whose behaviour the run exercises: the source-data tables, the data dictionary and freshness, and the agent platform itself.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Agent configuration set | Policy versions "P1" and "P2", prompt versions "PR1" and "PR2" with valid from 2026-11-20, the model version and the price, loaded and approved through the P10 contract | AC1 to AC12, AC15, AC18 |
| Stub answers | The 1,200 ms answer with 900 and 150 tokens, the schema-fault answer, the 0.79 answer and the 61 s silence, held by ModelStubControl | AC1, AC3, AC6, AC10, AC17 |
| Synthetic case set | Cases RW-2026-000101, RW-2026-000102 and RW-2026-000103 with a borrower holding a synthetic national ID number and a synthetic mobile number, and one document for the P5 calling step | AC1, AC6, AC7, AC17 |
| Sample set | Sample "ECHO-S1" version 1 with 20 labeled rows, and sample "ECHO-S2" with 0 rows | AC4, AC13, AC14, AC18 |
| Identity set | The synthetic users U-4101 and RW-CASEOWN, RW-COE, RW-RISK and RW-PLATADM session grants, and SY-AGENT | AC8 to AC12, AC15, AC16 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints, the two topics, queue `rwb-agent` and the namespace, with the contract preflight that fails on any drift and refuses a fake for P1, P3, P4 or P5.
2. Build ModelStubControl over the INT-23 OpenAPI 3.1 document, with the recorded request, the call count, the clock and the four fault switches.
3. Build ConfigProbe: load, approve, list and refuse, including the loader-not-approver rule, the row-version race and the full refusal of the bad policy file (AC2, AC8, AC9, AC12).
4. Build RunProbe and EventProbe over the admin listing, the case agent-outputs read and the two events; assert the run row, the cost, the three versions and the outbox fact (AC1, AC11).
5. Build MaskingProbe: seed the synthetic national ID number and mobile number, assert the P4 masking tokens, and scan the request, the run row and the log (AC7, TC-ITG-E1058-ITG-19).
6. Build ToolPathProbe: the `read_case` path through P3 and P5 as SY-AGENT, and the refused `propose_deviation` (AC5, AC17).
7. Build the four fault paths through the stub: timeout at 60,000 ms, schema check code SCHEMA, floor 0.79 and the tool refusal (AC3, AC6, AC10).
8. Build EvaluationDriver: sample load, start, poll to DONE, score rows with the three versions, the empty-sample refusal, the already-running refusal and the report (AC4, AC13, AC14, AC18).
9. Build CallerDriver and AccessProbe: the P3 and P5 calling steps through the agent runtime client with the rule result and the decision record, and the 403 with MSG-P4-002 (AC16, AC17).
10. Build ReportWriter, the cleanup of the synthetic set, the samples and the evaluation, and the evidence report; run the whole suite twice to prove that a repeated run adds no run row and makes no second model call.

**Done when.** The nineteen test cases of section 16 pass on the real services in SIT, the eighteen criteria of section 7 are signed off against the contracts, exactly one `rwb.agent.AgentRunCompleted.v1` and one run row exist per run, the log scan finds no personal data, the synthetic set is cleaned up, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | A prompt, policy or sample file fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | Evaluation started on a sample with no labeled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Evaluation started while the same one is running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P7-002 | Loader tries to approve their own version | You prepared this decision, so you cannot approve it. |
| MSG-GEN-004 | Approval of a version that changed since it was read | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required form field is empty (agent, kind, file) | Enter {field}. |

The seven texts are copied unchanged from RWB-E1-058 and this story adds no message ID. Thai text for each message follows decision DL10. In AC8 the {kind} value is "policy", the {agent} value is "ECHO" and the {check} value is "timeout_seconds between 1 and 120".

### 15. Screens and states

No screen in this story. RW-PLATADM and the other Platform administration R holders read runs through `GET /api/recovery/agent/v1/admin/agent-runs`; RW-COE and RW-RISK read versions, evaluations and scores through the configuration and evaluation operations of section 12.2. The listing states the run asserts through that operation are: an empty result for an agent with no run, a list of runs with id, agent, agentVersion, caseId, outcome, fallback and latencyMs, and a filtered list by agent and date. The evaluation states are RUNNING with a progress count and DONE with its score rows. The agent monitor screen SCR-46 and its states come in RWB-E2-031 and are out of scope, as is the autonomy-level screen of Epic 3.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-058-01-ITG | AC1, BR1, BR7, BR12 | Integration | Agent ECHO, case RW-2026-000101, stub answer 1,200 ms, 900 and 150 tokens, cost 0.0525 baht; end to end on the real services |
| TC-E1-058-02-ITG | AC2, BR2 | Integration | Prompt PR1 then PR2 valid from 2026-11-20; runs on 2026-11-19 and 2026-11-20; end to end on the real services |
| TC-E1-058-03-ITG | AC3, BR4 | Integration | Stub answer missing field "summary"; check code SCHEMA; end to end on the real services |
| TC-E1-058-04-ITG | AC4, BR13 | Integration | Sample ECHO-S1 version 1, 20 rows, trigger EVALUATION, mode SHADOW; end to end on the real services |
| TC-E1-058-05-ITG | AC5, BR4, BR6 | Integration | Tool call "propose_deviation" with allow-list "read_case"; check code TOOL_NOT_ALLOWED; end to end on the real services |
| TC-E1-058-06-ITG | AC6, BR3 | NFR | Stub silent for 61 seconds; run ends TIMED_OUT at 60,000 ms with fallback true; end to end on the real services |
| TC-E1-058-07-ITG | AC7, BR5 | Integration | Case RW-2026-000103 with a synthetic national ID number and mobile number; masking tokens of P4 for SY-AGENT; end to end on the real services |
| TC-E1-058-08-ITG | AC8, BR10 | Contract | Policy file with timeout_seconds 0; 422 with MSG-P10-001; P1 stays in force; end to end on the real services |
| TC-E1-058-09-ITG | AC9, BR8 | Integration | Synthetic user U-4101 approves its own version P2; 409 with MSG-P7-002; end to end on the real services |
| TC-E1-058-10-ITG | AC10, BR4 | Integration | Stub confidence 0.79, floor 0.80; run ends BELOW_FLOOR with fallback true; end to end on the real services |
| TC-E1-058-11-ITG | AC11, BR9 | Integration | Key ECHO:RW-2026-000101:2026-11-30 sent twice; one run row and one model call; end to end on the real services |
| TC-E1-058-12-ITG | AC12 | Integration | Two parallel approvals of P2, row version 1; one 200 and one 409 with MSG-GEN-004; end to end on the real services |
| TC-E1-058-13-ITG | AC13, BR13 | Contract | Sample ECHO-S2 with 0 rows; 422 with MSG-P10-002 and no run row; end to end on the real services |
| TC-E1-058-14-ITG | AC14, BR13 | Integration | Evaluation of ECHO on ECHO-S1 version 1 already RUNNING; 409 with MSG-P10-003; end to end on the real services |
| TC-E1-058-15-ITG | AC15, BR15 | Contract | 3 runs of ECHO from 2026-11-30 to 2026-12-01; listing fields only; end to end on the real services |
| TC-E1-058-16-ITG | AC16, BR6 | Integration | Synthetic user RW-CASEOWN calls the admin listing and the load; 403 with MSG-P4-002; end to end on the real services |
| TC-ITG-E1058-ITG-17 | AC17, BR14, BR3 | End to end | A step in rwb-case (P3) and a step in rwb-document (P5) through the agent runtime client with the stub silent for 61 seconds; one run row, fallback true, rule result in the decision record, no direct REST from the caller |
| TC-ITG-E1058-ITG-18 | AC18, BR13, BR15 | Integration | Evaluation of ECHO on ECHO-S1 version 1 DONE; report holds precision, recall, sample size 20 and the three versions; no personal value |
| TC-ITG-E1058-ITG-19 | AC7, BR5 | NFR | Log and response scan over the whole run for national ID number, phone number, name and account number patterns; request body and run row included |

TC-E1-058-01-ITG to TC-E1-058-16-ITG are the copies of the legacy test cases of RWB-E1-058, kept with their legacy IDs and given the `-ITG` suffix, one for each criterion AC1 to AC16. TC-ITG-E1058-ITG-17, -18 and -19 are new (D-RCV-60): 17 carries the caller-side fallback of AC17, 18 the evaluation report of AC18, and 19 the personal-data scan that closes AC7 across every artefact of the run. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, the timeout and the personal-data scan are NFR, and the two payload refusals and the listing shape are Contract.

### 17. Guardrails

- No business value in code or in the suite: the agent, the model version, the prompt and policy versions, the timeout, the confidence floor, the tool list, the price and the daily cap are the approved P10 rows, read through the contract at run time (BR11).
- No personal data in logs, events, prompts, workflow inputs, fixtures or the report: the run carries case IDs, agent codes, version labels, check codes, token counts, costs and dates only, and every national ID number, mobile number and account number is synthetic.
- Masking before the prompt: no value reaches INT-23 before rwb-access has returned its masking token for SY-AGENT, and the recorded request is scanned for personal patterns on every run.
- The model endpoint is reached only through the gateway client of rwb-agent and only on its private endpoint; the suite reaches it only through the recorded stub of its OpenAPI 3.1 contract, and a caller that reaches the agent by direct REST fails the run.
- Prompt text and model answers never appear in a response of section 12.2, in `rwb.agent.AgentRunCompleted.v1`, in `DecisionRecorded`, in a workflow history or in the application log; the listing returns ids and measures only (BR15).
- No cross-service table read and no schema client in the suite: every fact is read through a contract of section 12.2, 12.4 or 12.5, and a pipeline scan fails any change that adds a schema connection (DP-01).
- One hop and a 2 s client budget on every REST call, and the 60 s model budget only inside AgentRunWorkflow; the suite calls no service through another service (ADR-020, DP-11).
- No production access and no production namespace: the run is pinned to SIT with the synthetic set and refuses to start against any other environment.
- Clean-up in the same run: the synthetic cases, the sample and the evaluation run, the loaded versions and the stub deployment are removed or retired, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-010 | Agents run under service identities with the same role checks as people | The SY-AGENT tool path through P3 and P5, `GET /api/recovery/access/v1/me/session`, MSG-P4-002, `DecisionRecorded` | TC-E1-058-01-ITG, TC-E1-058-05-ITG, TC-E1-058-16-ITG, TC-ITG-E1058-ITG-17 |
| REQ-ACA-005 | Personal data masked by role in every agent call | The P4 masking tokens, the INT-23 recorded request, and the log and response scan over the request body, the run row and the application log | TC-E1-058-07-ITG, TC-ITG-E1058-ITG-19 |
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | The nine config operations of 12.2, the valid-from behaviour, the evaluation versions, the report | TC-E1-058-02-ITG, TC-E1-058-04-ITG, TC-E1-058-06-ITG, TC-E1-058-08-ITG, TC-E1-058-09-ITG, TC-ITG-E1058-ITG-18 |
| DP-01 | Owner's schema per service; no cross-service table read | `rwb_agent` behind the P10 contract; the P1 dictionary read instead of a table | TC-E1-058-01-ITG, TC-E1-058-15-ITG |
| DP-03 | Local decision record and the shared topic | `DecisionRecorded` on `rwb.decision-record.v1` for the calling step | TC-ITG-E1058-ITG-17 |
| DP-06 | Parameters contract of rwb-case | The parameters the tool path reads, never a value in the suite | TC-E1-058-01-ITG |
| DP-07 | Reference-data contract of rwb-case | The reference values the tool path reads | TC-E1-058-01-ITG |
| DP-08 | Authorise contract of rwb-access and the guard library | The session read, the 403 refusal, the masking request | TC-E1-058-16-ITG, TC-E1-058-07-ITG |
| DP-09 | Outbox, inbox and CloudEvents | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`, one event per run, key caseId | TC-E1-058-01-ITG, TC-E1-058-11-ITG |
| DP-11 | One hop and a 2 s timeout | The thirteen calls of 12.2 and the preflight contract test | TC-E1-058-08-ITG, TC-E1-058-13-ITG, TC-E1-058-15-ITG |
| DP-13 | `/api/recovery/<short>/v1` | `/api/recovery/agent/v1`, `/api/recovery/case/v1`, `/api/recovery/document/v1`, `/api/recovery/source-data/v1`, `/api/recovery/access/v1` | Every test case, at the preflight |
| DP-15 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; the agent tables are P10 migrations | Every test case, at the preflight |
| DP-19 | Screen route through gateway-bff | No screen in this story; the admin reads stand in for the future monitor screen | TC-E1-058-15-ITG |
| DP-20 | Agent client through the rwb-agent contract | The agent runtime client and AgentRunWorkflow on queue `rwb-agent` | TC-ITG-E1058-ITG-17 |
| ASM-0502 | P10 reaches INT-23 only through ModelGatewayClient on the private endpoint under SY-AGENT, and the suite uses one WireMock stub of the OpenAPI 3.1 contract | The stub of section 12.8 and the 60 s gateway budget | TC-E1-058-01-ITG, TC-E1-058-03-ITG, TC-E1-058-06-ITG, TC-E1-058-10-ITG |
| ASM-0503 | A calling service reaches an agent run through the RWB-TE-013 agent runtime client, which submits to AgentRunWorkflow on queue rwb-agent | The observed AgentRunWorkflow and the admin and case output reads of 12.2 | TC-ITG-E1058-ITG-17 |
| ASM-0504 | Guardrail, masking and run evidence stay in agent_run and are read through the P10 contract without prompt text, answer or personal field | GET /admin/agent-runs and the evaluation report | TC-E1-058-03-ITG, TC-E1-058-05-ITG, TC-E1-058-10-ITG, TC-E1-058-15-ITG, TC-ITG-E1058-ITG-18 |
| ASM-0505 | Personal data is masked before the model call by the P4 masking contract, and P4 is a wave-1 platform precondition, not an APP story this suite builds on | The captured model request at the stub and the masking assertion of AC7 | TC-E1-058-07-ITG, TC-ITG-E1058-ITG-19 |
| ASM-0506 | Prompt, policy and sample loading and approval stay on the P10 admin endpoints, with one synthetic user loading and a different one approving | GET and POST /admin/agent-configs, the approve operation, the sample load and the evaluation reads | TC-E1-058-02-ITG, TC-E1-058-08-ITG, TC-E1-058-09-ITG, TC-E1-058-12-ITG, TC-E1-058-13-ITG, TC-E1-058-14-ITG |
| ASM-0507 | Case and document facts reach P10 only through P3 GET /cases/{caseId} and P5 GET /documents/{documentId}; P1 provides the synthetic data and the field dictionary | GET /cases/{caseId}, GET /documents/{documentId} and GET /admin/data-dictionary/fields | TC-E1-058-01-ITG, TC-E1-058-07-ITG, TC-ITG-E1058-ITG-17 |
| RWB-E1-058 (legacy story) | Agent platform set-up [E1a]: the eighteen criteria AC1 to AC18 | The thirteen REST operations, the two events, the observed workflow and the stub of section 12 | The nineteen test cases of section 16 |
| RWB-P10-E1058-APP (component copy) | The agent platform inside rwb-agent: the six tables, the four components and the eight admin operations | The P10 contract itself | The nineteen test cases of section 16, run here on the real services |

### 19. Out of scope

- The application builds this run depends on: RWB-P1-E1001-APP, RWB-P1-E1069-APP and RWB-P10-E1058-APP.
- The contract, database, operations and infrastructure stories of the legacy key.
- The rule fallback inside a case step and the decision record entry of that step, which belong to RWB-TE-013; this story asserts only the rule result that comes back and the record the calling step writes.
- The case intake agent, the extraction evaluation and the deviation screening agent.
- The monitoring dashboard and the cost alert (RWB-E1-063, RWB-E2-031), and the agent monitor screen SCR-46.
- Changing an autonomy level through a screen (FEAT-AGT-12, Epic 3) and drift detection (FEAT-AGT-13, Epic 3).
- The choice of model endpoint (DL33): the run reads the model version of the policy and never selects an endpoint.
- The build of the harness RWB-ITG-W1J01-ITG itself and the non-functional epic RWB-ITG-NFR.
