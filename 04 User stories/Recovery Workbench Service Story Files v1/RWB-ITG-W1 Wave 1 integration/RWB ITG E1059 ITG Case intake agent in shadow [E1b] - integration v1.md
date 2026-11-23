# RWB-ITG-E1059-ITG Case intake agent in shadow [E1b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1059-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-059 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1030-APP, RWB-P10-E1059-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-059 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer** proving the case intake agent end to end on the real SIT services of rwb-agent (P10) and rwb-case (P3), with the published contracts of rwb-source-data (P1), rwb-document (P5) and rwb-access (P4) as wave-1 preconditions, I want **one suite that runs agent "INTAKE" in SHADOW on every CaseCreated event, reads the five tools from their owners as SY-AGENT, masks the personal values, flags stale input from the P1 freshness contract, scores the 200-case sample and proves that no shadow answer reaches a user**, so that **the shadow guarantee and its measured agreement rate are proved across the services that now share it, with the policy, prompt and model versions recorded, before the step to autonomy level 1 is decided**.

### 2. Business rationale

RWB-E1-059 built the case intake agent when the event listener, the tool gateway, the guardrail checker, the evaluation harness and all five source reads lived in one module. In the target the run is still owned by one service, rwb-agent (P10), but the facts it needs and the evidence it leaves are spread over five contracts: the trigger is EV-01 CaseCreated published by rwb-case (P3); three of the five tools are answered by rwb-case and one each by rwb-document (P5) and rwb-source-data (P1); the stale-input fact that legacy AC5 turns on arrives through the P1 freshness contract; personal values are masked by rwb-access (P4) before a value reaches a prompt; and the promise that no case owner ever sees a shadow answer has to hold on three reads owned by two services.

The component copy of the behaviour is RWB-P10-E1059-APP: it builds and unit-tests the intake listener, the input assembler, the output scorer, the output schema "intake-summary-v1" and the prompt version "PR1" inside rwb-agent, against the published contracts of its neighbours. This integration story exists because three facts that make the shadow run trustworthy cannot be proved inside one service, and because the legacy story leaves no criterion that a single service can sign off on its own:

- **The trigger and the run.** The event is published by rwb-case, consumed by the P10 inbox and turned into AgentRunWorkflow on queue `rwb-agent`; the case changes nothing, and rwb-case makes no REST call to rwb-agent. The legacy in-process `IntakeShadowListener` is gone, so the only path from a new case to a shadow run is Kafka (ASM-0510).
- **The tool path.** Five tools with three owners: `read_case`, `read_accounts` and `read_contact_points` from rwb-case, `read_documents` from rwb-document and `read_valuations` from rwb-source-data, each one hop under the identity SY-AGENT (ASM-0509).
- **The stale input.** The legacy criterion reads `v_ace_batch_status`; the target has one reader of the ACE views, rwb-source-data, and the business-date freshness reaches the run through its data-product contract, so the same `data_as_of 2026-11-28` and `STALE_INPUT` have to be proved through a published operation (GAP-0369; ASM-0508).
- **The shadow guarantee.** No summary and no gap flag may appear on the P10 admin listing, on the P10 agent-outputs read, or on the P3 case and timeline reads; the absence is a fact about three contracts owned by two services (ASM-0512).
- **The event the run leaves behind.** One `rwb.agent.AgentRunCompleted.v1` per run, written to the outbox in the same transaction as the run row (ASM-0513).
- **The evaluation.** Scores are produced and read only through the P10 admin operations, from a labelled sample the suite loads as data and never writes as a table row (ASM-0511).

The suite carries the legacy criterion AC5 word for word and writes thirteen new criteria. Every business value is the legacy value of RWB-E1-059, copied character for character: agent "INTAKE", policy "P1", mode SHADOW, timeout 60 seconds, confidence floor 0.80, prompt "PR1", output schema "intake-summary-v1", the gap types MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT and STALE_INPUT, samples "INTAKE-S1" version 1 and version 2 and "INTAKE-S3", cases RW-2026-000301, RW-2026-000302 and RW-2026-000303, the business dates 2026-11-30 to 2026-12-04, `data_as_of` 2026-11-28, the 200 labelled cases, 182 agreeing cases, the agreement rate 0.9100, the failure count 1 for TIMED_OUT and the messages MSG-P10-002, MSG-P10-003 and MSG-P4-002.

The only thing that is faked is the outside world. INT-23, the enterprise model endpoint, is reached through a recorded stub of its OpenAPI 3.1 contract, because no suite may call a live model endpoint with real prompts, and the stub carries the four fault switches and the clock that make the exception paths deterministic. rwb-source-data, rwb-case, rwb-access, rwb-document and rwb-agent are the real SIT services on their published contracts; a run configured with a fake for any of them fails the preflight, because a fake would defeat the purpose of the run.

The measures the story is read against are the legacy measures of RWB-E1-059: the agreement rate per gap type with its precision and recall on a labelled sample, the sample size, and a failure count per run status. The evidence report names, for every criterion, the contract element it was observed on, one verdict per test case and the versions in force.

### 3. Preconditions

- RWB-P3-E1030-APP is done for rwb-case (P3): the service is deployed with schema `rwb_case`, and the case, timeline, accounts and parties reads of section 12.2 are live on its published contract, with EV-01 CaseCreated published on `rwb.case.events.v1`. This is the P3 build whose behaviour AC1, AC2, AC6, AC11 and AC14 exercise.
- RWB-P10-E1059-APP is done for rwb-agent (P10): the service is deployed with schema `rwb_agent`, the intake listener, the input assembler, the output scorer, the gateway client, the guardrail checker, the evaluation harness, AgentRunWorkflow on queue `rwb-agent` and the six admin and read operations of section 12.2. This is the P10 build whose behaviour every criterion exercises.
- The published contracts of P5 rwb-document, P1 rwb-source-data, P4 rwb-access and P7 rwb-decision are versioned in the registry as wave-1 published-contract preconditions, and the suite consumes only those contracts; P5, P1, P4 and P7 are not builds this suite depends on (section 12.2, DP-11).
- Agent policy "INTAKE" version "P1" is approved: mode SHADOW, timeout 60 seconds, confidence floor 0.80, allowed tools `read_case`, `read_accounts`, `read_documents`, `read_valuations`, `read_contact_points`, and output schema "intake-summary-v1".
- Agent prompt "INTAKE" version "PR1" is approved.
- The output schema "intake-summary-v1" lists the gap types as data: MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT, STALE_INPUT.
- Labelled sample "INTAKE-S1" version 1 is loaded by RW-COE: the business analysts' review of 200 Epic 1 cases, one row per case and gap type with an expected value Y or N; sample version 2 carries labels for 180 of the 200 cases and sample "INTAKE-S3" carries none.
- The service identity SY-AGENT exists with its managed identity and the seeded permissions Case record R, Documents R and Reference data R, and rwb-access answers the masking request for it.
- The INT-23 stub is deployed with its OpenAPI 3.1 document, its answer, its clock and the four fault switches of section 12.8.
- The harness RWB-ITG-W1J01-ITG is available with the synthetic case set, the synthetic identities and the topic, queue and namespace wiring of wave 1.
- The SIT environment is available with the Temporal namespace `rwb-recovery`, queue `rwb-agent`, the topics `rwb.case.events.v1` and `rwb.agent.events.v1` with their retry and `.dlt` topics, and the schema registry.
- No production data is read, copied or connected to; every case number, borrower, national ID number, mobile number, account number and identity used by the run is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: runs the preflight, which reads the OpenAPI documents of P3 and P10 and the AsyncAPI documents of `rwb.case.events.v1` and `rwb.agent.events.v1`, and fails before any assertion if a path, a field, a status code or an event schema has drifted; it also confirms that no fake is configured for P1, P3, P4, P5 or P10.
2. Harness: reads policy version "P1" and prompt version "PR1" of agent "INTAKE" through `GET /api/recovery/agent/v1/admin/agent-configs` and asserts mode SHADOW, timeout 60 seconds, confidence floor 0.80, the five tools and output schema "intake-summary-v1"; nothing is loaded, because the versions are a precondition.
3. Harness: seeds the 200 synthetic cases of 2026-11-30 to 2026-12-04, and the three named cases RW-2026-000301, RW-2026-000302 and RW-2026-000303, through the W1J01 set in rwb-case.
4. Harness: consumes `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` for case "RW-2026-000301" and asserts the envelope, the key caseId and the business date.
5. Harness: asserts that the event enters the P10 inbox and starts AgentRunWorkflow on queue `rwb-agent` in namespace `rwb-recovery`, with the run key "INTAKE:<caseId>:<businessDate>"; rwb-case makes no REST call to rwb-agent and no suite step calls the agent on behalf of the case.
6. Run: rwb-agent resolves the approved policy and prompt in force, assembles the masked input set through the five tools as SY-AGENT - `read_case`, `read_accounts` and `read_contact_points` from P3, `read_documents` from P5, `read_valuations` from P1 - each on one hop with the 2 s client budget.
7. Run: rwb-agent asks rwb-access for the masking tokens of SY-AGENT, builds the prompt from the masked values and calls INT-23 through the gateway client with the 60 second policy budget; the stub records the request body for the masking assertion.
8. Run: rwb-agent takes the business-date freshness from `GET /api/recovery/source-data/v1/data-products/freshness` and the DP01 records from `GET /api/recovery/source-data/v1/data-products/{productCode}/records`, stores `data_as_of 2026-11-28` for business date 2026-11-30, and applies check "SCHEMA_RULE" so that an answer without STALE_INPUT falls back.
9. Run: the guardrail checks the schema, the tool list and the confidence floor in that order, then rwb-agent writes one run row with mode SHADOW and one `rwb.agent.AgentRunCompleted.v1` event to the outbox in the same transaction.
10. Harness: reads the runs through `GET /api/recovery/agent/v1/admin/agent-runs` and asserts 200 items with id, agent, agentVersion, caseId, outcome, fallback and latencyMs and no summary or gap flags; it reads `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` and asserts that no shadow output comes back, and it reads `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timeline` and asserts the same absence plus an unchanged case, task, queue and decision-log state.
11. Harness: replays the same CaseCreated event ID, and asserts one run for the case and business date, a counted repeat and no second model call (R-UNI-40).
12. Harness, exception paths: switches INT-23 to the timeout fault for case "RW-2026-000302" and asserts status "TIMED_OUT", fallback true, latency 60,000 ms, no second run and the failure count for TIMED_OUT on 2026-11-30 equal to 1; then switches the schema, floor and tool faults in turn and asserts GUARDRAIL_FAILED with check code "SCHEMA", BELOW_FLOOR at 0.79 and GUARDRAIL_FAILED with check code "TOOL_NOT_ALLOWED".
13. Harness: loads sample "INTAKE-S1" version 1 through `POST /api/recovery/agent/v1/admin/agent-samples`, starts the evaluation through `POST /api/recovery/agent/v1/admin/agent-evaluations`, polls `GET /api/recovery/agent/v1/admin/agent-evaluations` to status "DONE", and reads one score row per gap type with the agreement rate, precision, recall, sample size 200, agreement rate 0.9100 for MISSING_DOCUMENT on 182 agreeing cases, and policy "P1", prompt "PR1" and the model version on every row.
14. Harness: repeats the evaluation on sample version 2 with 180 labels and asserts sample size 180 and the 20 unlabelled cases listed on the evaluation run, then starts an evaluation on sample "INTAKE-S3" with no rows and asserts 422 with MSG-P10-002, and calls the two evaluation operations as synthetic user "RW-CASEOWN" and asserts 403 with MSG-P4-002 after reading the session through P4.
15. Harness: consumes `rwb.agent.AgentRunCompleted.v1` for every run, asserts exactly one event per run with runId, agent "INTAKE", the case ID, outcome and fallback and no personal field, then cleans up the synthetic cases, the samples, the evaluation runs and the stub deployment and writes the evidence report with one verdict per test case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The model stub does not answer within the policy timeout of 60 seconds | Run status TIMED_OUT, fallback true, latency 60,000 ms, failure count for the type rises by 1; no retry for that event | None to a user | AC10 |
| X2 | The answer fails its output schema, or omits STALE_INPUT for a stale input | Run status GUARDRAIL_FAILED, check code SCHEMA_RULE with the missing element, fallback true | None to a user | AC3, AC5 |
| X3 | The answer confidence is below the policy floor of 0.80 | Run status BELOW_FLOOR, fallback true | None to a user | Section 4 step 12 |
| X4 | The agent asks for a tool that is not on its allowed list | The tool call is refused, the run is GUARDRAIL_FAILED with check code TOOL_NOT_ALLOWED, fallback true | None to a user | Section 4 step 12 |
| X5 | The same CaseCreated event arrives twice with the same event ID | One run for the case and business date; the repeat is counted on the inbox and no second model call is made (R-UNI-40) | None to a user | AC6 |
| X6 | An admin or case read is asked for the shadow output | No operation returns the summary or the gap flags; the run listing returns metadata only | None to a user | AC1, AC11 |
| X7 | An evaluation is started on a sample with no labelled rows for "INTAKE" | Refused with 422, no evaluation run and no run row for the sample | MSG-P10-002 | AC9 |
| X8 | An evaluation is started while one for the same agent and sample version is running | Refused with 409, one RUNNING row stays | MSG-P10-003 | Section 13 |
| X9 | A role without Rules and parameters R starts or reads evaluations | Refused with 403, nothing changes | MSG-P4-002 | AC13 |
| X10 | A consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1 |
| X11 | A fake is configured for P1, P3, P4, P5 or P10 | The preflight refuses the run: only INT-23, the clock and the fixtures may be stubbed | None | Section 12.8 |
| X12 | The INT-23 stub drifts from its OpenAPI 3.1 document | The preflight fails on the stub contract test, so no assertion is made against an endpoint that no longer matches | None | AC1, AC10 |
| X13 | The W1J01 synthetic set, or the identity or sample it carries, is missing or does not match the run | The run fails as a fixture fault and names the missing element; no production value is substituted | None | AC1, AC4, AC13 |
| X14 | The P1 freshness answer and the DP01 record read disagree on the business date | The run fails as a contract fault against rwb-source-data and no run row is asserted; the disagreement is reported to the P1 owner | None | AC3 |
| X15 | A suite step tries to read a service schema directly | The step does not exist: the suite is built with no client for a service schema, and the pipeline scan fails any change that adds one | None | Section 17 |
| X16 | A shadow answer appears in a case field, a task, a queue row or a timeline entry | The run fails on AC1 or AC11 and the leak is reported against the owning service, because the shadow guarantee is the point of the story | None | AC1, AC11 |

X1 to X9 are the legacy exception paths of RWB-E1-059 carried onto the real services; X7 is legacy X6, X5 is legacy X3, X6 is legacy X5 and X9 is legacy X7. X10 to X16 are the failures that only appear when the run leaves one service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the two integration dependencies and the published contracts of P1, P3, P4, P5 and P10, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval, the report layout and the fault-switch names are configuration; the agent, the policy and prompt versions, the mode, the timeout, the floor, the tool list, the gap types, the sample codes and versions, the case numbers, the dates, the agreement rate and the message IDs are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: the event-started run, the five-tool path under SY-AGENT, masking before the prompt, the stale-input answer, the shadow guarantee on three reads, one event per run, idempotency, the two score shapes and one refusal |
| Estimable | One suite module, one external stub control, one fixture builder, five contract probes, one evaluation driver and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a REST response, a Kafka event, a run row read through the contract, a score row, a log scan or the evidence report |

### 7. Acceptance criteria

```gherkin
Feature: Case intake agent in shadow [E1b], proven across the wave 1 services

  Background:
    Given agent "INTAKE" has approved policy "P1" with mode "SHADOW", timeout 60 seconds, confidence floor 0.80, output schema "intake-summary-v1" and allowed tools read_case, read_accounts, read_documents, read_valuations and read_contact_points
    Given prompt version "PR1" is approved for agent "INTAKE"
    Given the gap types in output schema "intake-summary-v1" are MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT and STALE_INPUT
    Given the INT-23 model stub answers from its OpenAPI 3.1 contract and holds the four fault switches of section 12.8
    Given all involved services are deployed in SIT with their published contracts and SY-AGENT holds Case record R, Documents R and Reference data R
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded and no production value is used

  Scenario: AC1 A CaseCreated event makes one shadow run and changes no case (new, D-RCV-60)
    Given case "RW-2026-000301" is created in rwb-case (P3) on business date 2026-11-30 and EV-01 CaseCreated is published on `rwb.case.events.v1`
    When rwb-agent (P10) consumes the event and runs agent "INTAKE" with run key "INTAKE:<caseId>:<businessDate>"
    Then one agent run exists with agent "INTAKE", mode "SHADOW", trigger "CaseCreated" and the run key of the case and business date 2026-11-30
    Then no case field, task, queue or decision-log entry changes
    Then `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timeline` return no agent output

  Scenario: AC2 The five tools are answered by their owners under SY-AGENT (new, D-RCV-60)
    Given agent "INTAKE" runs for case "RW-2026-000301" as SY-AGENT
    When it calls the tools read_case, read_accounts, read_contact_points, read_documents and read_valuations
    Then read_case, read_accounts and read_contact_points are answered by rwb-case (P3) on `GET /api/recovery/case/v1/cases/{caseId}`, `/accounts` and `/parties`
    Then read_documents is answered by rwb-document (P5) on `GET /api/recovery/document/v1/cases/{caseId}/documents`
    Then read_valuations is answered by rwb-source-data (P1) on `GET /api/recovery/source-data/v1/collateral/{id}`
    Then every call is one hop with the 2 s client budget, no tool reads a schema and every call passes the SY-AGENT permission check

  Scenario: AC3 The stale input reaches the run through the P1 freshness contract (new, D-RCV-60)
    Given rwb-source-data (P1) answers `GET /api/recovery/source-data/v1/data-products/freshness` for business date 2026-11-30 with data_as_of 2026-11-28
    And `GET /api/recovery/source-data/v1/data-products/{productCode}/records` for DP01 answers the records of the same last complete business date
    When agent "INTAKE" runs for case "RW-2026-000303" on 2026-11-30
    Then the run stores data_as_of 2026-11-28
    Then the stored gap flags include STALE_INPUT
    Then an answer without STALE_INPUT fails the guardrail check "SCHEMA_RULE" with fallback true

  Scenario: AC4 Personal data is masked before the model call (new, D-RCV-60)
    Given case "RW-2026-000301" has a borrower with a synthetic national ID number, a synthetic mobile number, a name and an account number
    When rwb-agent builds the request to INT-23 for agent "INTAKE"
    Then the request body holds the masking tokens returned by rwb-access (P4) for SY-AGENT
    Then the request body, the agent run row and the application log hold no national ID number, phone number, name or account number

  Scenario: AC5 Stale input is flagged (legacy RWB-E1-059 AC5)
    Given v_ace_batch_status holds a COMPLETED ALS row for 2026-11-28 and none for 2026-11-30
    When the agent runs for case "RW-2026-000303"
    Then the run holds data_as_of 2026-11-28
    Then the stored gap flags include STALE_INPUT
    Then an answer without STALE_INPUT fails check "SCHEMA_RULE" with fallback true

  Scenario: AC6 A repeated event has no further effect (new, D-RCV-60)
    Given EV-01 CaseCreated for case "RW-2026-000301" was processed on 2026-11-30
    When the same event arrives again with the same event ID
    Then one agent run exists for the case and business date and the repeat is counted on the P10 inbox (R-UNI-40)
    Then no second model call is made for the repeat

  Scenario: AC7 The evaluation scores the 200-case sample with the versions recorded (new, D-RCV-60)
    Given labelled sample "INTAKE-S1" version 1 holds the business analysts' review of 200 Epic 1 cases, one row per case and gap type
    When RW-COE starts the evaluation of "INTAKE" on "INTAKE-S1" version 1 through `POST /api/recovery/agent/v1/admin/agent-evaluations`
    Then one evaluation run ends with status "DONE" and one score row per gap type holds the agreement rate, precision, recall and sample size 200
    Then for MISSING_DOCUMENT with 182 agreeing cases the agreement rate is 0.9100
    Then each score row holds policy version "P1", prompt version "PR1" and the model version

  Scenario: AC8 A partly labelled sample scores on the labelled cases (new, D-RCV-60)
    Given sample "INTAKE-S1" version 2 has labels for 180 of the 200 cases
    When the comparison runs
    Then each score row holds sample size 180
    Then the evaluation run lists the 20 unlabelled cases as unlabelled

  Scenario: AC9 An evaluation on an empty sample is refused (new, D-RCV-60)
    Given sample "INTAKE-S3" has no labelled rows for "INTAKE"
    When RW-COE starts the evaluation through `POST /api/recovery/agent/v1/admin/agent-evaluations`
    Then the system refuses the request with 422 and MSG-P10-002
    Then no evaluation run and no agent run row exist for "INTAKE-S3"

  Scenario: AC10 A failed run is counted and not retried (new, D-RCV-60)
    Given the INT-23 model stub does not answer for case "RW-2026-000302"
    When agent "INTAKE" runs on the CaseCreated event of the case
    Then the run holds status "TIMED_OUT", fallback true and latency 60,000 ms
    Then the system makes no second run for that event
    Then the failure count for type "TIMED_OUT" on 2026-11-30 is 1

  Scenario: AC11 No endpoint returns the shadow output (new, D-RCV-60)
    Given the 200 runs of agent "INTAKE" between 2026-11-30 and 2026-12-04
    When RW-PLATADM calls `GET /api/recovery/agent/v1/admin/agent-runs` with agent "INTAKE", from "2026-11-30" and to "2026-12-04"
    Then 200 AgentRun items return with id, agent, agentVersion, caseId, outcome, fallback and latencyMs
    Then no item holds the summary or the gap flags
    Then `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` returns no shadow output and the P3 case and timeline reads show no agent output

  Scenario: AC12 One AgentRunCompleted event per run, written with the run row (new, D-RCV-60)
    Given agent "INTAKE" finished a run for case "RW-2026-000301"
    When the run row is written
    Then one `rwb.agent.AgentRunCompleted.v1` event is written to the outbox in the same transaction, with runId, agent "INTAKE", the case ID, outcome and fallback
    Then the event is delivered to `rwb.agent.events.v1` as CloudEvents 1.0 with key caseId
    Then exactly one event exists per run and it holds no personal field

  Scenario: AC13 A role without the right is refused (new, D-RCV-60)
    Given synthetic user "RW-CASEOWN" holds no Rules and parameters right and the suite confirms it on `GET /api/recovery/access/v1/me/session`
    When "RW-CASEOWN" calls `POST /api/recovery/agent/v1/admin/agent-evaluations` and `GET /api/recovery/agent/v1/admin/agent-evaluations`
    Then both calls are refused with 403 and MSG-P4-002
    Then no evaluation run and no score row is created or changed

  Scenario: AC14 The run is AgentRunWorkflow on rwb-agent, started by the event (new, D-RCV-60)
    Given EV-01 CaseCreated enters the inbox of rwb-agent (P10)
    When the run starts
    Then AgentRunWorkflow runs on queue "rwb-agent" in namespace "rwb-recovery" and records the run of agent "INTAKE"
    Then rwb-case (P3) makes no REST call to rwb-agent and the only path from case to agent is the event
    Then the run names policy version "P1" and prompt version "PR1" as the versions in force
```

**Target reading.** The agent, its policy and prompt versions, the mode, the timeout, the confidence floor, the five tools, the output schema, the four gap types, the sample codes and versions, the case numbers, the business dates, `data_as_of`, the agreement counts and the messages are the legacy values of RWB-E1-059, copied character for character. AC5 is the legacy criterion kept word for word, including its `v_ace_batch_status` line, so that a reader can hold the two stories side by side; AC3 is the target route of the same fact, where the freshness and the DP01 records come from rwb-source-data through its published contract and no view is read by any service other than P1 (GAP-0369; ASM-0508). The in-process `IntakeShadowListener` of the legacy section 12 becomes the P10 inbox on `rwb.case.events.v1` and AgentRunWorkflow on queue `rwb-agent` (DP-09, DP-20), so AC14 asserts the workflow and AC1 the unchanged case rather than a Java listener. The score rows keep the legacy agreement rate, precision, recall and sample size, read through the P10 evaluation operations (ASM-0511), and the shadow guarantee is asserted at the three contracts that could leak it (ASM-0512).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | In SHADOW mode the output is stored and never shown, and nothing on the case changes: no case field, task, queue, timeline entry or decision-log entry | agent_policy.autonomy_mode = SHADOW (legacy BR1) |
| BR2 | The agent runs once per case per business date on EV-01 CaseCreated, with the run key "INTAKE:<caseId>:<businessDate>" | R-UNI-40; legacy BR2 |
| BR3 | Gap types are the enum in the approved output schema, not code | Principle 1; agent_policy.output_schema_ref (legacy BR3) |
| BR4 | When an input is older than the business date, the answer must include STALE_INPUT, and the run records the `data_as_of` of the last complete business date | VR-P10-003-1; legacy BR4 |
| BR5 | Agreement rate per gap type = cases where the agent flag equals the label / labelled cases, to 4 decimals | agent_evaluation.agreement_rate (legacy BR5) |
| BR6 | A run that times out or fails a check is not retried for the same event | R-UNI-32; INT-23 retry rule (legacy BR6) |
| BR7 | Personal fields are masked by rwb-access before the model call, and the request body, the run row and the log hold the masking tokens only | CTL-11; legacy BR7; DP-08 |
| BR8 | The five tools are answered by their owners on their published contracts: rwb-case for the case, the accounts and the contact points, rwb-document for the documents, rwb-source-data for the valuations; no tool reads a schema | DP-01; DP-05; DP-11; ASM-0509 |
| BR9 | The business-date freshness and the stale-input fact reach the run only through the P1 data-product and freshness operations; no service outside rwb-source-data reads an ACE view | DP-05; ASM-0508 |
| BR10 | The run is started by the event: rwb-case publishes CaseCreated, the P10 inbox consumes it and starts AgentRunWorkflow on queue `rwb-agent`, and rwb-case makes no REST call to rwb-agent | DP-09; DP-20; ASM-0510 |
| BR11 | The run row and its `rwb.agent.AgentRunCompleted.v1` event are written in one transaction through the outbox, and the event carries IDs and facts only | ADR-015; DP-09; ASM-0513 |
| BR12 | Every REST call of the suite and of the run is one hop to the owning service with a 2 s client budget; the 60 second model budget is the workflow budget of AgentRunWorkflow and never a REST budget of a caller | ADR-020; DP-11 |
| BR13 | The summary and the gap flags never appear in an API response, an event, a workflow history or the application log; the run listing returns id, agent, agentVersion, caseId, outcome, fallback and latencyMs only | Legacy sections 12 and 17; ASM-0512 |
| BR14 | Sample loading, evaluation start and evaluation reads stay on the P10 admin operations, and an empty sample is refused while one evaluation per agent and sample version may run | agent_sample; agent_evaluation_run; ASM-0511 |
| BR15 | No business value (agent, mode, timeout, floor, tool list, gap types, sample codes) is written in the suite; every one of them is read through the P10 contract at run time | Principle 1; DP-01 |
| BR16 | No production value is read, copied or connected to; every case, party, national ID number, mobile number, account number and identity of the run is synthetic, and the suite refuses to start outside SIT | Legacy section 17; guardrail |

### 9. State transitions

This story changes no case status. The states it observes and asserts on an agent run:

| From | Event | Condition | To |
|---|---|---|---|
| None | CaseCreated consumed and run started | Answer passes the schema, the tool and the floor checks | ANSWERED (agent_run.status, mode SHADOW) |
| None | CaseCreated consumed and run started | The endpoint does not answer in 60 seconds | TIMED_OUT, fallback true |
| None | CaseCreated consumed and run started | The schema check fails, including a missing STALE_INPUT | GUARDRAIL_FAILED, check code SCHEMA_RULE, fallback true |
| None | CaseCreated consumed and run started | The tool allow-list check fails | GUARDRAIL_FAILED, check code TOOL_NOT_ALLOWED, fallback true |
| None | CaseCreated consumed and run started | The confidence is below 0.80 | BELOW_FLOOR, fallback true |
| None | The same event ID arrives again | A run row already exists for the case and business date | No transition; the repeat is counted (R-UNI-40) |

The states of an evaluation run:

| From | Event | Condition | To |
|---|---|---|---|
| None | Evaluation started | The sample has labelled rows and none is running | RUNNING (agent_evaluation_run.status) |
| None | Evaluation started | The sample has 0 labelled rows | No row; 422 MSG-P10-002 |
| None | Evaluation started | One for the same agent and sample version is RUNNING | No row; 409 MSG-P10-003 |
| RUNNING | Last sample row scored | None | DONE |

The states the suite observes across the services:

| Item | States |
|---|---|
| INT-23 stub | Answering, silent for 61 seconds, schema fault, floor fault, tool fault |
| Agent run | ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, each with fallback true or false |
| Evaluation run | RUNNING, DONE |
| Case | Unchanged before and after every run (AC1) |
| Suite run | Not started, preflight failed, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the stub control and its fault switches, the clock, the cleanup and the evidence report |
| RW-COE, centre of excellence analyst | Loads the labelled sample, starts the evaluation and reads the scores (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Reads the scores (Rules and parameters R) |
| RW-PLATADM, platform administrator | Reads the run metadata (Platform administration R) |
| RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read the run metadata (Platform administration R) |
| RW-CASEOWN, case owner | Sees nothing from this story and is refused the two evaluation operations (AC13) |
| SY-AGENT, agent platform | Reads the case, the accounts and the contact points from rwb-case, the documents from rwb-document and the valuations from rwb-source-data (Case record R, Documents R, Reference data R) |
| SY-CASEWF, case workflow | Publishes EV-01 CaseCreated on `rwb.case.events.v1` |
| Service owner of rwb-agent (P10) | Owns the policy, prompt, run, sample and evaluation tables, the inbox, AgentRunWorkflow, the guardrail checker, the evaluation harness, the six admin and read operations, the topic and queue `rwb-agent` |
| Service owner of rwb-case (P3) | Owns the case, timeline, accounts and parties reads and the CaseCreated event |
| Service owner of rwb-source-data (P1) | Owns the freshness and data-product reads, the valuation read and the ACE view contract |
| Service owner of rwb-document (P5) | Owns the document read the tool path uses |
| Service owner of rwb-access (P4) | Owns the masking service, the right check, the session read and the refusal of MSG-P4-002 |
| No role | Reads a service schema directly, writes an agent table from outside rwb-agent, or takes production data into the run |

Approval levels: no delegation of authority level applies; the versions of the policy and the prompt are approved before the run, as in the legacy story, and this suite loads none of them.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, 002, 003, 005, 013, 016, 017 | recovery_case | id, case_no, product_group, status, entry_date, total_outstanding_at_entry, prescription_date | Read through the P3 contract; seeded synthetically |
| DF-DOC-001, 002, 004, 008 | document | id, case_id, document_type, review_status | Read through the P5 contract; seeded synthetically |
| DF-ACE-191, DF-ACE-193 | v_ace_valuation | appraised_value, appraisal_date | Read by rwb-source-data only and asserted here through the P1 valuation and data-product reads; never read by the suite |
| DF-ACE-075, DF-ACE-080 | v_ace_contact | contact_type, usage_code | Read by rwb-source-data only and asserted here through the P3 parties read; never read by the suite |
| DF-AGT-036 to DF-AGT-057 | agent_run | id, agent_code, agent_version, prompt_version, model_version, case_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, guardrail_result, output, confidence, latency_ms, tokens_in, tokens_out, cost_thb, data_as_of, run_at, evaluation_run_id | Read through the P10 contract, except output and the summary and gap flags, which no operation returns; written by rwb-agent (owner P10, schema `rwb_agent`) |
| DF-AGT-063 to DF-AGT-068 | agent_sample | sample_code, sample_version, subject_id, label_key, expected_value | Loaded through the P10 sample operation and read back as counts only; written by rwb-agent (owner P10) |
| DF-AGT-070 to DF-AGT-085 | agent_evaluation_run | all fields, including status, sample_size and failure_counts | Read through the P10 contract; written by rwb-agent (owner P10) |
| DF-AGT-087 to DF-AGT-096 | agent_evaluation | evaluation_run_id, label_key, sample_size, true_positive, false_positive, false_negative, agreement_rate, precision_value, recall_value | Read through the P10 contract; written by rwb-agent (owner P10) |
| DF-AGT-001 to DF-AGT-035 | agent_policy, agent_prompt | the approved policy version "P1" and prompt version "PR1" in force | Read through the P10 contract, except the prompt body, which is never returned |

Field IDs are those of RWB-E1-059 and are copied unchanged. Every table named here belongs to the service that owns it in the ownership map: agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run and agent_evaluation to P10 in schema `rwb_agent`, recovery_case to P3 in schema `rwb_case`, document to P5 in schema `rwb_document`. The suite owns no field and no table: it reads every row of this table through a contract of section 12 and writes only through the sample and evaluation operations of rwb-agent, with synthetic values. No field of agent_alert or agent_feedback is used, because the cost alert and the monitoring dashboard belong to RWB-E1-063 and RWB-E2-031 and are out of scope.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The reserved names of P2 rwb-integration - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` - are not used, and no `rwb_integration` table is written. The intake agent belongs to P10 rwb-agent, base `/api/recovery/agent/v1`, topic `rwb.agent.events.v1`, queue `rwb-agent` and schema `rwb_agent`.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | AC1, AC10 and AC11: the run listing - id, agent, agentVersion, caseId, outcome, fallback, latencyMs - with no summary, no gap flags and no personal field | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | Preconditions and step 2: the policy version "P1" and the prompt version "PR1" in force, with the text hash and no prompt body | 2 s |
| POST | `/api/recovery/agent/v1/admin/agent-samples` | P10 rwb-agent | AC7, AC8 and AC9: the load of sample "INTAKE-S1" version 1, version 2 and "INTAKE-S3" | 2 s + load time |
| POST | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | AC7, AC9 and AC13: the start of an evaluation, the empty-sample refusal and the 403 of RW-CASEOWN | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | AC7, AC8 and AC13: the evaluation run with its score rows, polled to status "DONE", and the 403 of RW-CASEOWN | 2 s |
| GET | `/api/recovery/agent/v1/cases/{caseId}/agent-outputs` | P10 rwb-agent | AC11: the recorded output of a run for a case, read back through the owner instead of the agent_run table, and the assertion that no shadow output comes back | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC1, AC2 and AC11: the case facts the `read_case` tool returns and the unchanged case | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | P3 rwb-case | AC1 and AC11: the timeline entry that no shadow run may add | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | P3 rwb-case | AC2: the accounts the `read_accounts` tool returns | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/parties` | P3 rwb-case | AC2: the contact points the `read_contact_points` tool returns, already masked by the owner | 2 s |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | AC2: the documents the `read_documents` tool returns | 2 s |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | AC3 and AC5: the `data_as_of` of the business date, which is 2026-11-28 for 2026-11-30 | 2 s |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | AC3: the DP01 records of the last complete business date | 2 s |
| GET | `/api/recovery/source-data/v1/collateral/{id}` | P1 rwb-source-data | AC2: the valuations the `read_valuations` tool returns | 2 s |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | AC13: the rights of the caller, which prove that RW-CASEOWN holds no Rules and parameters right | 2 s |

The fifteen paths are the six P10 operations, the four P3 case reads, the P5 document read, the three P1 reads and the P4 session read. Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the suite calls no service through another service and never through rwb-integration. The 60 second model budget is not a REST budget: it belongs to AgentRunWorkflow of section 12.5. No operation of this table returns the summary or the gap flags, which is the contract fact underneath AC11 (GAP-0369; ASM-0512).

#### 12.3 Events published

None. The suite publishes no business event and writes no outbox row; it observes the events of the owning services, listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | What the suite asserts |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | The envelope, the key caseId, the case ID and the business date, and that the event enters the P10 inbox and starts AgentRunWorkflow with the run key "INTAKE:<caseId>:<businessDate>"; the replay of the same event ID produces one run and a counted repeat (AC1, AC6, AC14) |
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Exactly one event per run, written to the outbox in the same transaction as the run row; runId, agent "INTAKE", the case ID, outcome and fallback, CloudEvents 1.0 with key caseId, and no personal field (AC12) |

Both event types are asserted. A consumer dedupes on the event ID through its inbox (ADR-015, DP-09). The payload of each event is the owner's published AsyncAPI schema; the suite asserts the envelope and the fields above and never the whole body of a prompt or an answer.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (observed, P10) | `rwb-agent` | One shadow run: resolve the approved policy and prompt in force, run the five tool calls, mask the values, call the gateway with the 60 second budget, check the answer, record the run row and its outbox event (Arch v5 slide 16: "AgentRunWorkflow: 60 s, then rule result"; DP-20) |

The suite starts no workflow of its own: the run is started by EV-01 CaseCreated through the P10 inbox, and the suite observes it on queue `rwb-agent` in namespace `rwb-recovery` through the Temporal visibility query with the run key as the search attribute. The tool calls and the gateway call are activities of rwb-agent and are observed through the run row and the events, not started by the suite.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story. The run is started by a Kafka event and the evaluation is started by RW-COE through `POST /api/recovery/agent/v1/admin/agent-evaluations`, so the suite triggers nothing on a cadence and starts no schedule of its own.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The agent tables of schema `rwb_agent` are owned by P10 rwb-agent and are read through the operations of section 12.2; the case, timeline, accounts and parties rows of schema `rwb_case` are owned by P3, the documents by P5 and the freshness and data products by P1, and each is read through its owner's contract. No outbox table, agent_alert table or agent_feedback table is read.

#### 12.8 Contract fakes

None for a service contract. The only fakes are outside the nineteen services:

| Stub | Purpose |
|---|---|
| INT-23 WireMock stub with its OpenAPI 3.1 contract | Stands in for the enterprise model endpoint that no suite may call with real prompts; returns the recorded answer and holds the request body for the masking assertion of AC4 |
| Clock control | Places the runs and evaluations on the business dates 2026-11-30 to 2026-12-04 and the stale date 2026-11-28; it never changes a service clock |
| Fault switch: timeout | Makes the stub silent for 61 seconds, for AC10 |
| Fault switch: schema | Returns an answer with a field missing from output schema "intake-summary-v1", for the guardrail path |
| Fault switch: floor | Returns a valid answer with confidence 0.79 against the floor 0.80, for the guardrail path |
| Fault switch: tool | Makes the agent ask for a tool outside its allowed list, for the guardrail path |
| W1J01 synthetic fixture set | The 200 synthetic cases, the three named cases, the synthetic borrower values, the sample files and the synthetic identities, with no production value |

rwb-source-data (P1), rwb-case (P3), rwb-access (P4), rwb-document (P5) and rwb-agent (P10) are the real SIT services on their published contracts and are not faked in the normal path; a run configured with a fake for any of them fails the preflight (X11). The synthetic identities come from the harness RWB-ITG-W1J01-ITG, not from a mock of rwb-access.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 15 | The six P10 admin and read operations, the four P3 case reads, the P5 document read, the three P1 reads and the P4 session read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 2 event types | `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` and `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`; CloudEvents 1.0, key caseId |
| Temporal | None | 1 workflow observed | AgentRunWorkflow on queue `rwb-agent` in namespace `rwb-recovery`; the suite observes it and starts nothing |
| File | None | None | No file in this story; the sample is loaded through the P10 operation, not from a file |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a stub control for INT-23 with its clock and four fault switches, a fixture builder for the synthetic cases, identities and samples, a set of contract probes over P1, P3, P4, P5 and P10, an evaluation driver, a masking and log scan, a workflow observer and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published OpenAPI and AsyncAPI documents, run order, report and exit code |
| ModelStubControl | Test harness | Deploys the INT-23 stub from its OpenAPI 3.1 document, sets the answer, the four fault switches and the clock, and exports the recorded request and the call count |
| IntakeRunProbe | Test harness | Asserts the run of agent "INTAKE" - mode SHADOW, trigger CaseCreated, the run key, status, fallback, latency and the three versions - through the P10 run listing |
| ToolPathProbe | Test harness | Asserts that the five tools are answered by P3, P5 and P1 as SY-AGENT, one hop each with the 2 s budget, and that no tool reads a schema |
| FreshnessProbe | Test harness | Seeds the stale business date through P1 and asserts `data_as_of 2026-11-28`, STALE_INPUT and the SCHEMA_RULE fallback (AC3, AC5) |
| ShadowProbe | Test harness | Asserts that the admin listing, the agent-outputs read and the P3 case and timeline reads carry no summary and no gap flags (AC1, AC11) |
| MaskingProbe | Test harness | Seeds the synthetic national ID number, mobile number, name and account number, asserts the P4 masking tokens, and scans the request body, the run row and the application log |
| EventProbe | Test harness | Consumes CaseCreated and AgentRunCompleted, asserts one event per run, the outbox fact, the envelope, the key and the absence of a personal field |
| EvaluationDriver | Test harness | Loads a sample, starts an evaluation, polls it to DONE, reads the score rows, and proves the partly labelled and empty-sample cases |
| WorkflowProbe | Test harness | Observes AgentRunWorkflow on queue `rwb-agent`, asserts that the event started it with the run key, and that rwb-case made no REST call to rwb-agent |
| AccessProbe | Test harness | Reads the caller session through P4 and asserts that RW-CASEOWN is refused with 403 and MSG-P4-002 |
| ReportWriter | Test harness | One row per test case with its evidence and elapsed time, one line per criterion, and the cleanup record |

**Database.** None of its own. The suite writes no service table, no schema object and no migration.

**Configuration and reference data**

- The SIT endpoints of P1, P3, P4, P5 and P10, the topics `rwb.case.events.v1` and `rwb.agent.events.v1`, queue `rwb-agent`, namespace `rwb-recovery` and the schema-registry address, all as configuration.
- The synthetic cases RW-2026-000301, RW-2026-000302 and RW-2026-000303 and the 200-case set of 2026-11-30 to 2026-12-04, the synthetic borrower values, the synthetic user RW-CASEOWN and SY-AGENT, and the sample codes INTAKE-S1 and INTAKE-S3, all from the W1J01 set.
- The agent "INTAKE", policy version "P1", mode SHADOW, timeout 60 seconds, confidence floor 0.80, prompt version "PR1", output schema "intake-summary-v1", the four gap types, the 200 labelled cases, the 182 agreeing cases, the agreement rate 0.9100 and the failure count 1, read through the P10 contract and never written in the suite code (BR15).
- The 2 s client budget, the evaluation poll interval and the 60 s workflow budget.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits in this suite |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The suite holds no schema client; every agent, case, document, data-product and session fact is read through the operations of 12.2, and the agent tables stay behind the P10 contract |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | AC1 asserts that no decision-log entry is added by a shadow run, observed on the P3 timeline; the library and its topic stay with the owning services and the platform story |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | `read_valuations`, the freshness read and the DP01 record read are the P1 contract; no `v_ace_*` view is read by the suite or by rwb-agent (AC2, AC3) |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The parameters the tool path and the guardrail use are answered by P3 at run time and read through its contract, never held in the suite |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The reference values behind the accounts and contact points are read through the P3 contract in the same run (AC2) |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | EV-01 CaseCreated on `rwb.case.events.v1` into the P10 inbox, and one AgentRunCompleted on `rwb.agent.events.v1` from the outbox in the run transaction (AC6, AC12, AC14) |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The five tools, the case and timeline reads, the freshness reads and the session read are one hop each with the 2 s budget; the preflight fails on any drift (AC2, AC3, AC13) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 carries the service base `/api/recovery/agent/v1`, `/api/recovery/case/v1`, `/api/recovery/document/v1`, `/api/recovery/source-data/v1` and `/api/recovery/access/v1` |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The suite owns no migration and proves at the preflight that the agent tables are P10 migrations and the case tables P3 migrations |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | No screen in this story; the admin and case reads the suite asserts stand in for the monitor screen of RWB-E2-031, whose composite route belongs to the edge story |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON | The run is started by the P10 inbox and AgentRunWorkflow on queue `rwb-agent`, and no calling service reaches rwb-agent by REST (AC14) |

The H and C dependencies of the table stay with the service, platform and operations stories that own them; this story carries none of its own, and an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7). The I list names the two builds whose behaviour the suite exercises: the case service reads and the CaseCreated event of rwb-case, and the intake agent of rwb-agent. P5, P1, P4 and P7 appear as wave-1 published-contract preconditions only.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Agent configuration set | Policy version "P1" with mode SHADOW, timeout 60 seconds, floor 0.80, the five tools and output schema "intake-summary-v1", and prompt version "PR1", read through the P10 contract and not loaded by the suite | AC1 to AC14 |
| Stub answers | The recorded answer, the schema-fault answer, the 0.79 answer and the 61 s silence, held by ModelStubControl over the INT-23 OpenAPI 3.1 contract | AC4, AC10, section 5 |
| Synthetic case set | The 200 cases of 2026-11-30 to 2026-12-04 and the cases RW-2026-000301, RW-2026-000302 and RW-2026-000303, with a borrower holding a synthetic national ID number, a mobile number, a name and an account number, contact points, documents and a valuation | AC1 to AC6, AC10, AC11 |
| Sample set | Sample "INTAKE-S1" version 1 with 200 labelled cases, version 2 with 180 labels, and sample "INTAKE-S3" with none | AC7, AC8, AC9 |
| Identity set | SY-AGENT, the synthetic user RW-CASEOWN, and the RW-COE, RW-RISK and RW-PLATADM session grants | AC2, AC4, AC7, AC13 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints, the two topics, queue `rwb-agent` and the namespace, with the contract preflight that fails on any drift and refuses a fake for P1, P3, P4, P5 or P10 (AC1, section 5 X10 to X12).
2. Build ModelStubControl over the INT-23 OpenAPI 3.1 document, with the recorded request, the call count, the clock and the four fault switches (AC4, AC10).
3. Build IntakeRunProbe and WorkflowProbe: the event-started run on queue `rwb-agent`, the run key, mode SHADOW and the versions in force, and the proof that rwb-case makes no REST call to rwb-agent (AC1, AC14).
4. Build ToolPathProbe: the five tools answered by P3, P5 and P1 as SY-AGENT, one hop with the 2 s budget and no schema read (AC2).
5. Build FreshnessProbe: seed the stale business date through P1, then assert `data_as_of 2026-11-28`, STALE_INPUT and the SCHEMA_RULE fallback (AC3, AC5).
6. Build MaskingProbe: seed the synthetic personal values, assert the P4 masking tokens and scan the request body, the run row and the log (AC4).
7. Build ShadowProbe: the admin listing of 200 runs with metadata only, the agent-outputs read and the P3 case and timeline reads, all without the summary or the gap flags (AC1, AC11).
8. Build EventProbe: one AgentRunCompleted per run, the outbox fact, the envelope, the key and the absence of a personal field, and the replay of the same CaseCreated event ID (AC6, AC12).
9. Build EvaluationDriver: the 200-case sample with the three versions, the partly labelled sample with 180, the empty-sample refusal, the already-running refusal and the score rows with 0.9100 for MISSING_DOCUMENT (AC7, AC8, AC9).
10. Build the timeout and guardrail paths through the stub, and AccessProbe with the 403 of RW-CASEOWN (AC10, AC13).
11. Build ReportWriter, the cleanup of the synthetic set, the samples and the evaluation runs, and the evidence report; run the whole suite twice to prove that a repeated run adds no run row and makes no second model call.

**Done when.** The fourteen test cases of section 16 pass on the real services in SIT, the fourteen criteria of section 7 are signed off against the contracts, exactly one `rwb.agent.AgentRunCompleted.v1` and one run row exist per run, the case is unchanged after every shadow run, the log scan finds no personal data, the synthetic set is cleaned up, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-002 | Evaluation started on an empty sample | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Same evaluation already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-E1-059 and this story adds no message ID. Thai text for each message follows decision DL10. In AC9 the {sample} value is "INTAKE-S3" and the {agent} value is "INTAKE"; in AC13 the {action} values are the two evaluation operations.

### 15. Screens and states

No screen in this story. No case owner sees the output, and the case owner screen shows nothing from this story (AC11). RW-PLATADM and the other Platform administration R holders read runs through `GET /api/recovery/agent/v1/admin/agent-runs`; RW-COE and RW-RISK read evaluations and scores through the two evaluation operations of section 12.2. The states the suite asserts through those reads are: an empty result for an agent with no run, a list of 200 runs with id, agent, agentVersion, caseId, outcome, fallback and latencyMs and no summary or gap flags, a filtered list by agent and date, an evaluation RUNNING and then DONE with its score rows and sample size 200 or 180, and a refusal of 422 or 403 with its message. The agent monitor screen SCR-46 and its states come in RWB-E2-031 and are out of scope, as is the autonomy-level screen of Epic 3.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-059-01-ITG | AC1, AC11 | Integration | 200 synthetic cases created 2026-11-30 to 2026-12-04; the case, task, queue and timeline state before and after the run; end to end on the real services |
| TC-E1-059-02-ITG | AC7 | Integration | Sample INTAKE-S1 version 1, 200 cases, MISSING_DOCUMENT 182 agreeing cases, agreement rate 0.9100, policy P1, prompt PR1 and the model version; end to end on the real services |
| TC-E1-059-03-ITG | AC1, AC6 | Integration | Case RW-2026-000301 created 2026-11-30 with the run key INTAKE:<caseId>:2026-11-30; end to end on the real services |
| TC-E1-059-04-ITG | AC10 | Integration | Stub silent for case RW-2026-000302; status TIMED_OUT, fallback true, no retry, failure count 1 on 2026-11-30; end to end on the real services |
| TC-E1-059-05-ITG | AC5 | Integration | data_as_of 2026-11-28 for business date 2026-11-30; STALE_INPUT in the stored gap flags; the SCHEMA_RULE fallback; end to end on the real services |
| TC-E1-059-06-ITG | AC6 | Integration | The same CaseCreated event ID sent twice for case RW-2026-000301; one run, counted repeat; end to end on the real services |
| TC-E1-059-07-ITG | AC8 | Integration | Sample INTAKE-S1 version 2, 180 of 200 labelled, the 20 unlabelled cases listed; end to end on the real services |
| TC-E1-059-08-ITG | AC9 | Contract | Sample INTAKE-S3 with no labelled rows; 422 with MSG-P10-002 and no evaluation run; end to end on the real services |
| TC-E1-059-09-ITG | AC13 | Integration | Synthetic user RW-CASEOWN calls POST and GET /admin/agent-evaluations; 403 with MSG-P4-002; the right proved on GET /me/session; end to end on the real services |
| TC-ITG-E1059-ITG-10 | AC2 | Integration | The five tools answered by P3, P5 and P1 as SY-AGENT, one hop and 2 s each, no schema read; end to end on the real services |
| TC-ITG-E1059-ITG-11 | AC3 | Contract | P1 freshness answers data_as_of 2026-11-28 for business date 2026-11-30 and the DP01 records agree; STALE_INPUT stored; end to end on the real services |
| TC-ITG-E1059-ITG-12 | AC4 | NFR | Synthetic national ID number, mobile number, name and account number; P4 masking tokens; scan of the request body, the run row and the application log |
| TC-ITG-E1059-ITG-13 | AC12 | Integration | One rwb.agent.AgentRunCompleted.v1 per run, outbox in the run transaction, CloudEvents 1.0, key caseId, no personal field; end to end on the real services |
| TC-ITG-E1059-ITG-14 | AC14 | End to end | EV-01 CaseCreated into the P10 inbox and AgentRunWorkflow on queue rwb-agent in namespace rwb-recovery; no REST call from P3 to P10 |

TC-E1-059-01-ITG to TC-E1-059-09-ITG are the copies of the legacy test cases of RWB-E1-059, kept with their legacy IDs and given the `-ITG` suffix. TC-ITG-E1059-ITG-10 to TC-ITG-E1059-ITG-14 are new (D-RCV-60): 10 carries the five-tool path of AC2, 11 the P1 freshness route of AC3, 12 the personal-data scan of AC4, 13 the outbox event of AC12 and 14 the event-started workflow of AC14. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, the freshness and empty-sample payload refusals are Contract, the personal-data scan is NFR, and the event-started run is End to end.

### 17. Guardrails

- No business value in code or in the suite: the agent, the mode, the policy and prompt versions, the timeout, the confidence floor, the tool list, the output schema and the gap types are the approved P10 rows, read through the contract at run time (BR15).
- No personal data in logs, events, prompts, fixtures or the report: the run and the report carry case IDs, agent codes, version labels, check codes, dates and counts only, and every national ID number, mobile number, name and account number is synthetic.
- Masking before the prompt: no value reaches INT-23 before rwb-access has returned its masking token for SY-AGENT, and the recorded request is scanned for personal patterns on every run.
- No shadow output in any user-facing response: the admin listing, the agent-outputs read and the P3 case and timeline reads are asserted empty of the summary and the gap flags on every run (BR13, ASM-0512).
- No cross-service table read and no schema client in the suite: every fact is read through a contract of section 12.2, 12.4 or 12.5, and a pipeline scan fails any change that adds a schema connection (DP-01).
- One hop and a 2 s client budget on every REST call, and the 60 s model budget only inside AgentRunWorkflow; the suite calls no service through another service (ADR-020, DP-11).
- The model endpoint is reached only through the gateway client of rwb-agent and only on its private endpoint; the suite reaches it only through the recorded stub of its OpenAPI 3.1 contract, and a fake for any of the five services fails the preflight.
- No production access and no production namespace: the run is pinned to SIT with the synthetic set and refuses to start against any other environment.
- Clean-up in the same run: the synthetic cases, the samples, the evaluation runs and the stub deployment are removed or retired, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-005 | Personal data is masked by role in every agent call | The P4 masking tokens, the INT-23 recorded request, and the scan of the request body, the run row and the application log | TC-ITG-E1059-ITG-12, TC-E1-059-01-ITG |
| REQ-ACA-010 | Agents run under service identities with the same role checks as people | The SY-AGENT tool path through P3, P5 and P1, `GET /api/recovery/access/v1/me/session`, MSG-P4-002 and the 403 refusal | TC-ITG-E1059-ITG-10, TC-E1-059-09-ITG, TC-ITG-E1059-ITG-14 |
| DP-01 | Owner's schema per service; no cross-service table read | `rwb_agent` behind the P10 contract and `rwb_case` behind P3; the suite holds no schema client | TC-E1-059-01-ITG, TC-E1-059-02-ITG |
| DP-03 | Local decision record and the shared topic | The decision-log entry a shadow run must not add, observed on the P3 timeline; the library and topic stay with the owning services | TC-E1-059-01-ITG |
| DP-05 | ACE facts and valuations through rwb-source-data | `GET /api/recovery/source-data/v1/collateral/{id}`, the freshness read and the DP01 record read; no `v_ace_*` view read by the suite | TC-ITG-E1059-ITG-10, TC-ITG-E1059-ITG-11 |
| DP-06 | Parameters contract of rwb-case | The parameters the tool path and the guardrail read at run time, never a value in the suite | TC-ITG-E1059-ITG-10 |
| DP-07 | Reference-data contract of rwb-case | The reference values behind the accounts and contact points, read through P3 | TC-ITG-E1059-ITG-10 |
| DP-09 | Outbox, inbox and CloudEvents | CaseCreated into the P10 inbox and one AgentRunCompleted from the outbox for every run | TC-ITG-E1059-ITG-13, TC-E1-059-03-ITG |
| DP-11 | One hop and a 2 s timeout | The fifteen paths of 12.2 and the preflight contract test | TC-E1-059-08-ITG, TC-ITG-E1059-ITG-11 |
| DP-13 | `/api/recovery/<short>/v1` | `/api/recovery/agent/v1`, `/api/recovery/case/v1`, `/api/recovery/document/v1`, `/api/recovery/source-data/v1`, `/api/recovery/access/v1` | Every test case, at the preflight |
| DP-15 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; the agent tables are P10 migrations and the case tables P3 migrations | Every test case, at the preflight |
| DP-19 | Screen route through gateway-bff | No screen in this story; the admin and case reads stand in for the future monitor screen | TC-E1-059-01-ITG, TC-E1-059-02-ITG |
| DP-20 | Agent client through the rwb-agent contract | The P10 inbox and AgentRunWorkflow on queue `rwb-agent`, with no REST call from P3 | TC-ITG-E1059-ITG-14 |
| ASM-0508 | Freshness and data-product route for `data_as_of` and STALE_INPUT | The P1 freshness read and the DP01 record read, and the legacy AC5 kept word for word | TC-ITG-E1059-ITG-11, TC-E1-059-05-ITG |
| ASM-0509 | The five tools answered by P3, P5 and P1 | The case, accounts, parties, documents and valuation reads of 12.2 | TC-ITG-E1059-ITG-10 |
| ASM-0510 | EV-01 to inbox to AgentRunWorkflow on `rwb-agent`; no REST from P3 | CaseCreated on `rwb.case.events.v1`, the P10 inbox and the observed workflow | TC-ITG-E1059-ITG-14, TC-E1-059-03-ITG, TC-E1-059-06-ITG |
| ASM-0511 | Evaluation driven only through the P10 admin operations | The sample load and the two evaluation operations of 12.2 | TC-E1-059-02-ITG, TC-E1-059-07-ITG, TC-E1-059-08-ITG |
| ASM-0512 | No shadow output through the P10 admin, the agent-outputs or the P3 reads | The admin listing, the agent-outputs read and the case and timeline reads of 12.2 | TC-E1-059-01-ITG |
| ASM-0513 | AgentRunCompleted on `rwb.agent.events.v1` from the outbox in one transaction | `rwb.agent.AgentRunCompleted.v1` and the run row transaction | TC-ITG-E1059-ITG-13 |
| RWB-E1-059 (legacy story) | Case intake agent in shadow [E1b]: the eight criteria AC1 to AC8 | The fifteen paths, the two events, the observed workflow and the stubs of section 12 | The fourteen test cases of section 16 |
| RWB-P10-E1059-APP (component copy) | The intake listener, the input assembler, the output scorer, the schema and the prompt inside rwb-agent | The P10 contract itself | The fourteen test cases of section 16, run here on the real services |

The gap GAP-0369 is carried by every row above that names a P1 or P3 contract element, because it is the row that records why those routes had to be assumed; no test case traces to the gap itself.

### 19. Out of scope

- The application builds this run depends on: RWB-P3-E1030-APP and RWB-P10-E1059-APP.
- The contract, database, operations and infrastructure stories of the legacy key.
- The build of rwb-source-data (P1), rwb-document (P5), rwb-access (P4) and rwb-decision (P7), which appear here only as wave-1 published-contract preconditions.
- The evaluation report and the L1 autonomy proposal (RWB-E1-061), and the step to autonomy level 1 (RWB-E2-028).
- Showing the summary or the gap flags to a case owner, and the monitor screen SCR-46 with the monitoring dashboard and cost alert (RWB-E1-063, RWB-E2-031).
- Document classification and field extraction, including the extraction evaluation (RWB-E1-053, RWB-E1-060).
- The deviation screening agent in shadow (RWB-E1-062) and the route agent.
- The build of the harness RWB-ITG-W1J01-ITG itself and the non-functional epic RWB-ITG-NFR.
