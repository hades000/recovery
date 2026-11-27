# RWB-P10-E1058-APP Agent platform set-up [E1a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1058-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-058 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-P10-A |
| Ready to start | Day 1 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P10-E1058-APP-14); no signed epic design record found in this story or the md sources |
| Size | Not specified in the source documents (DOR-RWB-P10-E1058-APP-16); section 6 gives two weeks for two developers |
| Depends on (build) | RWB-P10-E1058-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-TE013-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P10-E1058-APP-23); the operations in section 12.1 sit on the /v1 base |
| Integration dependencies | None |
| External dependencies | RWB-P10-E1058-INF, RWB-P10-E1058-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-024, FR-P10-025) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E1-058 for rwb-agent. The behaviour of the legacy story is unchanged and is delivered by the service instead of by the monolith. The six agent tables move into schema `rwb_agent` in the service's own Flyway sequence (DP-01, DP-15); the eight admin operations and the case-output read answer on the base `/api/recovery/agent/v1` and the legacy monolith base is retired for them (DP-13); the model gateway client reaches the Enterprise AI private endpoint INT-23 as the service identity (DP-11 at the boundary); the prompt, policy and sample versions are the service's own rows and the version in force is resolved from them, while the parameter keys are read through the parameters contract of rwb-case (DP-06) and the lists through its reference-data contract (DP-07); the right check and the masking decision go to rwb-access through the guard library (DP-08); the run row, its outbox row and `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` are written in one transaction through the outbox and inbox library (DP-09); the local decision-record library and `rwb.decision-record.v1` are installed and their write path proved, while the record of a case step stays with RWB-P10-TE013 (DP-03); the tool gateway reads case facts from rwb-case and extracted fields from rwb-document as one hop with a 2 s budget against contract fakes (DP-11); the admin reads are reached through the gateway-bff route (DP-19); and a calling step reaches an agent through the rwb-agent contract and AgentRunWorkflow on queue `rwb-agent`, never through an in-process interface (DP-20). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E1058-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 28 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the agent platform built as the rwb-agent service - the model gateway client, the prompt and policy store, the guardrail checker, the evaluation harness, the tool gateway and the run record in schema `rwb_agent`, the eight admin configuration and evaluation operations and the case-output read on the base `/api/recovery/agent/v1`, the decision-record library and the outbox with `rwb.agent.events.v1`, and AgentRunWorkflow on the queue `rwb-agent` - reading case facts from rwb-case, document fields from rwb-document, the parameters and lists from the rwb-case contracts and the right and the masking decision from rwb-access**, so that **every Workbench agent is built, called, checked and scored through one path with its versions recorded, on the same values the legacy story fixed, and no module reaches another module's table to do it**.

### 2. Business rationale

Officers gather and check case facts by hand before every decision, and no agent can help until there is one controlled way to call a model. The legacy story gave every later agent the same gateway, the same versioned prompts and policies, the same output checks and the same scoring, so that an agent runs under a service identity (REQ-ACA-010), sees only masked personal data (REQ-ACA-005) and reads every threshold from a versioned row (REQ-DRI-010). The measure is unchanged: the agent fallback rate, target below 10 percent per month, read from the agent run table (FSD P10 v3 A2.1).

In the legacy delivery there was one module, one process and one recovery schema: `ModelGatewayClient` called the endpoint in the same process, `ToolGateway` called another module's Java interface, `RecoveryAccessGuard` and `PromptInputMasker` ran in the same transaction as the caller, the run row and the decision log entry were two tables of the same schema, and the row of the version in force was a query on the same connection. The behaviour is unchanged, so the disposition is Split (rework): the legacy story's fifteen criteria are carried word for word and every value stays, and what changes is where each fact lives and how it is reached.

- The six tables of the platform - agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run and agent_evaluation - are P10's own, in schema `rwb_agent`, created by the service's own Flyway sequence, and no other module reads them (DP-01, DP-15).
- The eight admin operations and the case-output read are served on the base `/api/recovery/agent/v1`, and the legacy monolith base is retired for them (DP-13).
- The calling contract of the legacy `AgentOrchestrator` interface is not a Java interface any more: a calling step reaches a run through the agent runtime client and AgentRunWorkflow on queue `rwb-agent`, one hop, and takes the rule result when the run falls back (DP-20, DP-11; ASM-0848, ASM-0850).
- The policy values that used to be columns read in process - the timeout, the confidence floor, the output schema reference, the allowed tools, the price and the cap - stay rows of the approved policy version, and the parameter keys and the lists come through the rwb-case contracts instead of the casewf.config table (DP-06, DP-07).
- The right check and the masking decision come from rwb-access through the guard library, on every operation and before any value reaches a prompt (DP-08; AC7).
- The run row and its `rwb.agent.AgentRunCompleted.v1` event are written in one transaction through the outbox, and the message is a CloudEvents 1.0 record on `rwb.agent.events.v1` with a retry topic and a `.dlt` topic; a decision of a calling step is recorded through the local decision-record library on `rwb.decision-record.v1` and never by the agent (DP-09, DP-03; AC1).
- The tool gateway reads case facts from rwb-case and extracted fields from rwb-document as SY-AGENT, one hop with the 2 s client budget, and never reads a `rwb_case` or `rwb_document` table (DP-11; AC5).
- The admin reads are reached through the gateway-bff route, so no screen calls rwb-agent directly (DP-19).

The cross-service behaviour of this key - that a run row and its event appear together, that the version in force follows its valid-from date across two services, that the masked request carries the tokens of another service, and that a calling step still gets a rule result when the model does not answer - is proved by RWB-ITG-E1058-ITG, which is why this story carries no integration dependency (I = None) and claims none. This story builds and unit-tests its own deliverables against the published contracts and their fakes, owns the fifteen legacy acceptance criteria AC1 to AC15 and adds none: the service change is stated in sections 1, 2, 4, 12 and 13 and is proved by the contract tests of section 16 and by RWB-ITG-E1058-ITG.

### 3. Preconditions

- RWB-P10-E1058-CON is baselined: the nine operations of section 12.1, the EV-28 payload on `rwb.agent.events.v1`, the record mapping, the eight `rwb_agent` tables and their keys, the error model and the contract fakes are published and versioned.
- RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are available: the decision-record library, the parameters and reference-data client libraries, the access guard library, the outbox and inbox library, the per-service Flyway sequence with parameterized schema names, and the gateway-bff route contract with its stub.
- RWB-P10-TE013-CON is available: the agent runtime client with its fallback, which is how a calling step submits to AgentRunWorkflow on queue `rwb-agent`.
- The `rwb_agent` schema and the rwb-agent login exist with grants on that schema only, and the Flyway history table of the service is created (DP-02; ASM-0848).
- The rwb-case contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: `GET /api/recovery/case/v1/parameters/{key}` for the parameter keys the run reads and `GET /api/recovery/case/v1/reference-data/{lovCode}` for LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS and LOV-SUBJECT-TYPE. This story builds against those contracts and their fakes and never reads a `rwb_case` table (ASM-0852).
- The rwb-access contract of RWB-P4-E1037-CON is published: `POST /api/recovery/access/v1/authorise` for the Rules and parameters and Platform administration rights and for the masking decision, and `GET /api/recovery/access/v1/masking-policies` for the masking policy in force for SY-AGENT (DP-08; ASM-0851).
- The rwb-case case read `GET /api/recovery/case/v1/cases/{caseId}` and the rwb-document document read `GET /api/recovery/document/v1/documents/{documentId}` are published for the tool gateway, with their fakes (ASM-0853).
- The service identity SY-AGENT exists with the Entra ID managed identity and the seeded permissions Case record R, Documents R, Rules and parameters R, Reference data R and Decision log C; the legacy story names the DEV identity `RWB-DEV-SY-AGENT` and the SIT, UAT and PROD equivalents, and the names of those registrations are Not specified in the source documents (GAP-0606; ASM-0848).
- The Enterprise AI private endpoint INT-23 is reachable on its private endpoint in the SCB tenant, and its host, port, certificate and the Key Vault entries of the service are provisioned by RWB-P10-E1058-INF and are Not specified in the source documents (GAP-0608; ASM-0854).
- The masking capability of RWB-E1-037 is delivered by rwb-access (RWB-P4-E1037-APP): its masking policy masks personal fields by role, including for SY-AGENT, and is read through the rwb-access contract and not through a table (DP-08).
- A person holding RW-COE loads prompts, policies and labeled samples; a person holding RW-RISK approves them; the two rights and their refusal come from rwb-access (legacy section 3; AC8, AC9, AC12).
- The `rwb_agent` schema baseline is empty apart from its Flyway history, so the migration of this story applies on a clean schema (section 12.7).
- The release date 30 November 2026 is tentative and is copied unchanged; the PRD reference is Pending (C1) and the story proceeds in Draft status (ASM-0855).

### 4. Flow

1. The rwb-agent Flyway sequence runs `Vnnnn__agent_runtime.sql` in `rwb_agent` and creates agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run and agent_evaluation with the standard record columns and the keys of section 13 (DP-01, DP-15).
2. RW-COE loads a prompt file and a policy file for agent "INTAKE" through `POST /api/recovery/agent/v1/admin/agent-configs`; the guard library asks rwb-access for Rules and parameters C before the body is read (DP-08).
3. AgentConfigService validates each file against the versioned policy and prompt JSON schemas, stores it as a new version with status "LOADED" and keeps every earlier version readable; one failed check refuses the whole file and leaves the version in force untouched (BR8; AC8).
4. RW-RISK approves the version through `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` with If-Match on the row version, and the version takes effect on its valid from date; the loader cannot approve their own version, and a second approval of the same row version is refused with 409 (BR2; AC2, AC9, AC12).
5. A calling step submits a run through the agent runtime client of RWB-P10-TE013-CON, which starts AgentRunWorkflow on queue `rwb-agent` with the agent code, the case ID, the subject ID, the trigger event, the idempotency key and the inputs (DP-20; AC1, AC11).
6. ResolveAgentConfig reads the approved policy and prompt versions in force on the run date, with their output schema reference, allowed tools, timeout, confidence floor, price and cap, and reads the parameter keys and the lists through the rwb-case contracts (DP-06, DP-07; AC2).
7. GatherInputs runs the tools on the allow-list through the tool gateway as SY-AGENT: `read_case` goes to `GET /api/recovery/case/v1/cases/{caseId}`, and a document tool goes to `GET /api/recovery/document/v1/documents/{documentId}`, one hop each with the 2 s client budget; a tool off the list is refused and the refusal is recorded (DP-11; AC5).
8. MaskInputs asks rwb-access for the masking decision on every gathered value and replaces each personal value with the token it returns, so no value reaches the prompt unmasked (DP-08; AC7).
9. CallModelGateway calls INT-23 with the model code, the masked inputs and the output schema reference, bounded by timeout_seconds of the policy in force, and returns the answer, the token counts and the latency (BR3; AC1, AC6).
10. CheckGuardrail runs the three checks in order - output schema, allowed tool list, confidence floor - and returns the check codes it found (BR4; AC3, AC5, AC10).
11. RecordAgentRun writes one agent_run row with the agent, policy, prompt and model versions, status, fallback, guardrail result, confidence, latency, tokens and cost, and writes the `rwb.agent.AgentRunCompleted.v1` outbox row in the same transaction (DP-09; AC1, AC11).
12. The outbox relay publishes the message to `rwb.agent.events.v1` after the payload passes its registry subject; a payload that fails the subject, or a topic that is unreachable, is routed to the `.dlt` topic with an alert and the outbox row is kept (BR4; AC1).
13. The workflow answers the calling step with the checked answer, or with a fallback result and its reason so the step takes the rule path; where the step records a decision, it does so through the local decision-record library on `rwb.decision-record.v1`, in its own transaction (DP-03; AC6, AC10).
14. RW-COE loads a labeled sample through `POST /api/recovery/agent/v1/admin/agent-samples` and starts the evaluation harness through `POST /api/recovery/agent/v1/admin/agent-evaluations`; the harness runs the agent in shadow on every sample row, scores it against the labels and stores the scores with the policy, prompt and model versions (AC4, AC13, AC14).
15. The evaluation is read through `GET /api/recovery/agent/v1/admin/agent-evaluations` and its report through `GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report`, and a run's recorded output is read through `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs`; the run listing is read through `GET /api/recovery/agent/v1/admin/agent-runs` (AC15).
16. RW-PLATADM and the other Platform administration R holders reach the admin reads through the gateway-bff route, one hop, so no screen calls rwb-agent directly; the run changes no case status and no other service's data (DP-19; AC15).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The model endpoint does not answer within the policy timeout of 60 seconds | Run status TIMED_OUT, fallback true; the caller uses the rule result (R-UNI-32) | None to a user | AC6 |
| X2 | The answer fails its output schema | Run status GUARDRAIL_FAILED, failure counted by check code; fallback true | None to a user | AC3 |
| X3 | The agent asks for a tool that is not on its allowed list | The tool call is refused and logged; run status GUARDRAIL_FAILED; fallback true | None to a user | AC5 |
| X4 | The answer confidence is below the policy confidence floor | Run status BELOW_FLOOR; fallback true | None to a user | AC10 |
| X5 | A prompt or policy file fails a load check | The load is refused in full; the version in force is unchanged | MSG-P10-001 | AC8 |
| X6 | The person who loaded a version tries to approve it | Approval refused; version stays LOADED | MSG-P7-002 | AC9 |
| X7 | Two approvals of the same version arrive at once | The first approves; the second is refused with 409 | MSG-GEN-004 | AC12 |
| X8 | The same run request arrives twice with the same idempotency key | One run row; the repeat returns the first result and is counted (R-UNI-40) | None to a user | AC11 |
| X9 | An evaluation is started on a sample with no labeled rows for the agent | Refused with 422; no run starts | MSG-P10-002 | AC13 |
| X10 | An evaluation is started while one for the same agent and sample is running | Refused with 409 | MSG-P10-003 | AC14 |
| X11 | A role without the right calls an endpoint | Refused with 403; nothing changes | MSG-P4-002 | AC16 (TC-E1-058-16, TC-E1-058-18) |
| X12 | A consumed contract does not answer inside the 2 s client budget, or answers outside its published shape | The read is counted as a failed read of the run; the tool result is empty, the guardrail records the failure, and the run ends with fallback true; a contract test against the fake blocks a merge that changes the shape | None to a user | AC17 (TC-E1-058-19) |
| X13 | The parameter key or the list version in force names a value the policy does not allow | The run is refused before the model call, the offending value is named on the run, and no code default is used in its place | None to a user | AC18 (TC-E1-058-20) |
| X14 | A migration of the service's Flyway sequence fails | The new version does not start, the version in force keeps serving, and no run row and no version row is written | None | AC19 (TC-E1-058-21) |
| X15 | A value reaches the model request that rwb-access did not return as a masking token | The request is refused before it leaves the service, the run ends with fallback true, and the incident is raised against the masking path | None to a user | AC7 |

X1 to X11 are the legacy exception paths of RWB-E1-058 carried onto the service; X12 to X15 are the failures that appear when the read leaves the service and when the schema, the parameters and the masking become the service's own responsibility. X11 is reached by AC16 and is proved by the access test case TC-E1-058-16 through the rwb-access contract fake and across services by RWB-ITG-E1058-ITG, and the message is kept so a reader finds the legacy set complete.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the platform contracts and the published rwb-case and rwb-access contracts with their fakes; no other agent story is needed, because a test agent "ECHO" with a fixed prompt proves every path |
| Negotiable | The package layout, the component and activity names, the poll of the evaluation and the column order of a response are design; the model, prompts, thresholds, timeout, tool lists, price, statuses and message IDs are fixed by the legacy story |
| Valuable | Every later agent (RWB-P10-E1059-APP to RWB-P10-E2032-APP) is built on it, and every model call carries its versions from the first call |
| Estimable | Six new tables, eight components plus the workflow and its six activities, nine operations, four contract clients and the access guard, no screen |
| Small | Fits in two weeks for two developers with its tests, as in the legacy estimate |
| Testable | Each criterion below is one automated test on an observable: a REST answer, a stored row, an event on the topic, a check code, a fallback reason or a scan of the source |

### 7. Acceptance criteria

```gherkin
Feature: Agent platform set-up [E1a]

  Background:
    Given the test agent "ECHO" has policy version "P1" approved with model "MODEL-A-2026-10", timeout 60 seconds, confidence floor 0.80 and allowed tools "read_case"
    Given prompt version "PR1" is approved for agent "ECHO"
    Given the model endpoint stub answers in 1,200 milliseconds with 900 input tokens and 150 output tokens
    Given the policy price is 0.0500 baht per 1,000 tokens

  Scenario: AC1 Approved endpoint (legacy RWB-E1-058 AC1)
    Given the rwb-case contract mock returns the case facts of case "RW-2026-000101"
    Given the approved model endpoint on the private endpoint of the SCB tenant
    When the orchestrator runs agent "ECHO" for case "RW-2026-000101"
    Then the call succeeds with run status "ANSWERED"
    Then one agent run row holds agent "ECHO", policy version "P1", prompt version "PR1", model version "MODEL-A-2026-10", latency 1,200 ms, tokens in 900, tokens out 150 and cost 0.0525 baht
    Then the system writes one AgentRunCompleted event to the outbox with the run ID, agent "ECHO", the case ID, outcome "ANSWERED" and fallback false

  Scenario: AC2 Prompt versions (legacy RWB-E1-058 AC2)
    Given prompt version "PR1" is in force for agent "ECHO"
    When RW-COE loads prompt version "PR2" and RW-RISK approves it with valid from 2026-11-20
    Then prompt version "PR2" exists with status "APPROVED"
    Then prompt version "PR1" stays readable through GET /admin/agent-configs with its text hash unchanged
    Then a run on 2026-11-19 uses "PR1" and a run on 2026-11-20 uses "PR2"

  Scenario: AC3 Schema check (legacy RWB-E1-058 AC3)
    Given the model stub returns an answer with field "summary" missing from the output schema of "ECHO"
    When the guardrail runs
    Then the system rejects the output with run status "GUARDRAIL_FAILED" and fallback true
    Then the guardrail result holds check code "SCHEMA" with the missing field name
    Then the count of check code "SCHEMA" failures for "ECHO" on the business date rises by 1

  Scenario: AC4 Evaluation suite (legacy RWB-E1-058 AC4)
    Given labeled sample "ECHO-S1" version 1 with 20 rows for agent "ECHO"
    When RW-COE starts the evaluation of "ECHO" on "ECHO-S1"
    Then one evaluation run ends with status "DONE" and 20 agent run rows with trigger "EVALUATION" and mode "SHADOW"
    Then one score row per label key holds sample size, true positives, false positives, false negatives, precision and recall
    Then each score row holds policy version "P1", prompt version "PR1" and model version "MODEL-A-2026-10"

  Scenario: AC5 Guardrails (legacy RWB-E1-058 AC5)
    Given an agent with the allowed tool list "read_case"
    When it calls the tool "propose_deviation", which is not on its list
    Then the system refuses the tool call and not executed
    Then the agent run holds status "GUARDRAIL_FAILED", check code "TOOL_NOT_ALLOWED" and fallback true
    Then the orchestrator returns a fallback result with reason "TOOL_NOT_ALLOWED" so the calling step takes the rule path

  Scenario: AC6 The model does not answer inside the timeout (legacy RWB-E1-058 AC6)
    Given the model stub does not answer for 61 seconds
    When the orchestrator runs agent "ECHO" for case "RW-2026-000102"
    Then the system ends the call at 60 seconds
    Then the agent run holds status "TIMED_OUT", fallback true and latency 60,000 ms
    Then the orchestrator returns a fallback result with reason "TIMED_OUT" (R-UNI-32)

  Scenario: AC7 Personal data is masked before the model call (legacy RWB-E1-058 AC7)
    Given the rwb-access contract mock returns the masking decision and the masking tokens for SY-AGENT for the synthetic national ID number and the synthetic mobile number
    Given case "RW-2026-000103" has a borrower with a synthetic national ID number and a synthetic mobile number
    When the orchestrator builds the request to the model endpoint
    Then the request body holds the masking tokens returned by the P4 masking service for SY-AGENT
    Then the request body, the agent run row and the application log hold no national ID number, phone number, name or account number

  Scenario: AC8 A configuration file that fails a check is refused (legacy RWB-E1-058 AC8)
    Given a policy file for agent "ECHO" with timeout_seconds 0
    When RW-COE loads it through POST /admin/agent-configs
    Then the system refuses the load with 422 and MSG-P10-001 naming check "timeout_seconds between 1 and 120"
    Then policy version "P1" stays in force and no new version row exists

  Scenario: AC9 The loader cannot approve their own version (legacy RWB-E1-058 AC9)
    Given user "coe.user01" loaded policy version "P2" for agent "ECHO"
    When user "coe.user01" calls POST /admin/agent-configs/{versionId}/approve for "P2"
    Then the system refuses the approval with 409 and MSG-P7-002
    Then version "P2" keeps status "LOADED"

  Scenario: AC10 An answer below the confidence floor falls back (legacy RWB-E1-058 AC10)
    Given the model stub returns a valid answer with confidence 0.79
    When the guardrail runs with confidence floor 0.80
    Then the agent run holds status "BELOW_FLOOR" and fallback true
    Then the orchestrator returns a fallback result with reason "BELOW_FLOOR"

  Scenario: AC11 A repeated run request has no further effect (legacy RWB-E1-058 AC11)
    Given agent "ECHO" ran for case "RW-2026-000101" with idempotency key "ECHO:RW-2026-000101:2026-11-30"
    When the same request arrives again with the same key
    Then no second agent run row and no second model call exist
    Then the system returns the first result and the idempotency hit is counted (R-UNI-40)

  Scenario: AC12 Two approvals of one version at the same time (legacy RWB-E1-058 AC12)
    Given policy version "P2" for agent "ECHO" has status "LOADED" and row version 1
    When two RW-RISK users approve "P2" at the same time
    Then one approval succeeds and "P2" has status "APPROVED"
    Then the system refuses the other with 409 and MSG-GEN-004

  Scenario: AC13 An evaluation on an empty sample is refused (legacy RWB-E1-058 AC13)
    Given sample "ECHO-S2" has 0 labeled rows for agent "ECHO"
    When RW-COE starts the evaluation of "ECHO" on "ECHO-S2"
    Then the system refuses the request with 422 and MSG-P10-002
    Then no evaluation run and no agent run row exist

  Scenario: AC14 A second evaluation while one is running is refused (legacy RWB-E1-058 AC14)
    Given the evaluation of "ECHO" on "ECHO-S1" version 1 has status "RUNNING"
    When RW-COE starts the same evaluation again
    Then the system refuses the request with 409 and MSG-P10-003
    Then one evaluation run exists for "ECHO" on "ECHO-S1" version 1 with status "RUNNING"

  Scenario: AC15 Agent runs are listed without their content (legacy RWB-E1-058 AC15)
    Given the rwb-access contract mock returns Platform administration R for RW-PLATADM
    Given 3 runs of agent "ECHO" between 2026-11-30 and 2026-12-01
    When RW-PLATADM calls GET /admin/agent-runs with agent "ECHO", from "2026-11-30" and to "2026-12-01"
    Then 3 AgentRun items return with id, agent, agentVersion, caseId, outcome, fallback and latencyMs
    Then no item holds the prompt text, the model answer or a personal field

  Scenario: AC16 A role without the right is refused (exception X11) (new, D-RCV-60)
    Given RW-CASEOWN holds no Platform administration right
    When RW-CASEOWN calls GET /admin/agent-runs with agent "ECHO", from "2026-11-30" and to "2026-12-01"
    Then the system refuses the call with 403 and MSG-P4-002
    Then no agent run item is returned

  Scenario: AC17 A consumed contract does not answer inside its budget (exception X12) (new, D-RCV-60)
    Given the rwb-case contract fake does not answer inside the 2 s client budget
    When the orchestrator runs agent "ECHO" for case "RW-2026-000101"
    Then the tool result is empty and the guardrail records the failed read
    Then the agent run holds fallback true and the run ends

  Scenario: AC18 A parameter value the policy does not allow refuses the run (exception X13) (new, D-RCV-60)
    Given the parameter key read from rwb-case names a value that the policy does not allow
    When the orchestrator runs agent "ECHO" for case "RW-2026-000101"
    Then the run is refused before the model call and the offending value is named on the run
    Then no code default is used and the model endpoint is not called

  Scenario: AC19 A failed migration keeps the version in force (exception X14) (new, D-RCV-60)
    Given the migration Vnnnn__agent_runtime.sql of the rwb-agent Flyway sequence fails
    When the service starts with the new version
    Then the new version does not start and the version in force keeps serving
    Then no run row and no version row is written

  Scenario: AC20 Architecture rules of the service hold (BR11 to BR17) (new, D-RCV-60)
    Given the service is built from its own code, its own schema and its own topic definitions
    When the guard and boundary tests of section 13 run
    Then no business value is written in code, every table sits in schema rwb_agent and no foreign key crosses services
    Then the run row and its outbox row are written in one transaction on rwb.agent.events.v1, and a calling step reaches a run only through the agent runtime client and queue rwb-agent
    Then every other REST call is one hop with the 2 s client budget, the right check and masking decision come from rwb-access through the guard library, and no prompt text or model answer appears in a listing, an event, a workflow history or the application log

  Scenario: AC21 Error answers of the provided operations (new, D-RCV-60)
    Given a call to GET /admin/agent-runs arrives with no session
    When the call is made
    Then the system refuses the call with 401 and MSG-P4-001, and no agent run item is returned
    When a caller who holds the read right calls GET /cases/{caseId}/agent-outputs for a case that does not exist
    Then the system answers 404 and no item is returned

```

**Target reading.** Every value of the legacy criteria is copied character for character - the agent "ECHO", policy version "P1", prompt versions "PR1" and "PR2", the model version "MODEL-A-2026-10", the timeout of 60 seconds and the 61 seconds of the stub, the confidence floor 0.80 and the answer 0.79, the allowed tool "read_case" and the refused tool "propose_deviation", the price 0.0500 baht per 1,000 tokens and the cost 0.0525 baht, the stub answer of 1,200 milliseconds with 900 input and 150 output tokens, the cases RW-2026-000101, RW-2026-000102 and RW-2026-000103, the samples ECHO-S1 with 20 rows and ECHO-S2 with 0 rows, the dates 2026-11-19, 2026-11-20, 2026-11-30 and 2026-12-01, the users "coe.user01" and RW-CASEOWN, the statuses ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, LOADED, APPROVED, RUNNING and DONE, the check codes SCHEMA and TOOL_NOT_ALLOWED, and the messages MSG-P10-001, MSG-P10-002, MSG-P10-003, MSG-P7-002, MSG-GEN-004 and MSG-P4-002. The scenario lines of AC1 to AC15 keep their legacy titles and every legacy Given, When and Then; three of them carry one inserted Given as their first line, `Given the rwb-case contract mock returns ...` on AC1, `Given the rwb-access contract mock returns ...` on AC7 and on AC15, because those three criteria read across a service boundary: AC1 reads the case facts the tool gateway gathers, AC7 the masking decision and the masking tokens of rwb-access, and AC15 the Platform administration right that authorises the listing. AC2, AC3, AC4, AC5, AC6, AC8, AC9, AC10, AC11, AC12, AC13 and AC14 read nothing outside rwb-agent beyond the rule row the version-in-force pattern takes through the contract, so they carry no inserted line. The legacy in-process `AgentOrchestrator` interface becomes the published rwb-agent contract behind the agent runtime client and AgentRunWorkflow on queue `rwb-agent` (DP-20); the legacy `ToolGateway` calls into other modules become the two owner reads of AC1 and AC5 (DP-11); the legacy name of the monolith base has no place in this story (DP-13); and the tables, the schema, the migration, the topic and the route are those of section 12. The service change itself - the base of the operation set, the schema and the no-cross-schema rule, the tool reads, the parameter and list reads, and the right and masking path with the route in front of the admin reads - is stated in sections 1, 2, 4, 12 and 13 and is proved by the contract tests of the operations, the schema, the tool reads and the access path, and across services by RWB-ITG-E1058-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every model call goes through the model gateway client of rwb-agent to the endpoint chosen under DL33, reached on its private endpoint as the service identity; no other component and no calling service calls the endpoint | DL33; INT-23; DP-20; legacy BR1 |
| BR2 | The orchestrator uses the policy and prompt versions in force on the run date with status APPROVED; open runs keep the version they started with | agent_policy.valid_from (DF-AGT-022); R-UNI-38; legacy BR2 |
| BR3 | If the endpoint does not answer within agent_policy.timeout_seconds (60, assumed; DL11), the run ends TIMED_OUT and the rule result is used | R-UNI-32; NFR-010; legacy BR3 |
| BR4 | Every answer is checked in this order: output schema, allowed tool list, confidence floor; the first failed check sets the status and fallback is true | agent_policy.output_schema_ref, allowed_tools, confidence_floor (DF-AGT-006, DF-AGT-007, DF-AGT-011); legacy BR4 |
| BR5 | Personal fields are masked through rwb-access before any value reaches a prompt, and the request body, the run row and the log hold the masking tokens only | CTL-11; REQ-ACA-005; DP-08; legacy BR5 |
| BR6 | The agent runs as SY-AGENT and passes the same permission check as a person on every tool call | REQ-ACA-010; role SY-AGENT; legacy BR6 |
| BR7 | Cost of a run = (tokens in + tokens out) / 1,000 x agent_policy.price_per_1k_tokens_thb, rounded to 4 decimals; price assumed 0.0500 baht, DL33 | agent_policy.price_per_1k_tokens_thb (DF-AGT-014); DL33; legacy BR7 |
| BR8 | A prompt or policy version is loaded by RW-COE and approved by RW-RISK; the same person may not do both | CTL-08; separation of duty; legacy BR8 |
| BR9 | A run request with an idempotency key already used returns the first result | R-UNI-40; legacy BR9 |
| BR10 | A file load is refused in full if any row fails a check | Principle 1; CTL-08; legacy BR10 |
| BR11 | No business value (model name, threshold, timeout, price, tool list, list value) is written in code; it is read from the approved policy row and the rwb-case contracts at run time, and a missing value stops the run | Principle 1; DT02; DP-06; DP-07; legacy BR11 |
| BR12 | The six tables of the platform are P10's own in schema `rwb_agent`, created by the service's own Flyway sequence; the service reads no table of another service and holds no foreign key across services | DP-01; DP-15; Arch v5 slide 41 |
| BR13 | The run row and its `rwb.agent.AgentRunCompleted.v1` outbox row are written in one transaction, and the message is a CloudEvents 1.0 record on `rwb.agent.events.v1` with a retry topic and a `.dlt` topic, carrying IDs and facts only | DP-09; ADR-015; Arch v5 slides 42 and 43 |
| BR14 | A calling step reaches a run only through the agent runtime client and AgentRunWorkflow on queue `rwb-agent`, and the 60 second model budget is the workflow budget, never the 2 s budget of a caller | DP-20; DP-11; ADR-020; Arch v5 slide 16 |
| BR15 | Every other REST call of the service is one hop with the 2 s client budget, and a read that does not answer inside it is a failed read and not a retry inside the transaction | DP-11; ADR-020 |
| BR16 | The right check and the masking decision are answered by rwb-access through the guard library, cached for the life of the call, and a refusal writes nothing | DP-08; Arch v5 slide 41 |
| BR17 | Prompt text and model answers never appear in an API response of the listing, in an event, in a workflow history or in the application log | Legacy sections 12 and 17; Arch v5 slide 42 note |

### 9. State transitions

None. This story does not change a case status. It changes the status of an agent configuration version, of an agent run and of an evaluation run.

| From | Event | Condition | To |
|---|---|---|---|
| None | Configuration file loaded | Every check passes | LOADED (agent_policy.status or agent_prompt.status) |
| None | Configuration file loaded | A check fails | No row; load refused (MSG-P10-001) |
| LOADED | Approved by RW-RISK | Approver is not the loader and the row version matches | APPROVED |
| LOADED | Approved by the loader | None | LOADED; approval refused (MSG-P7-002) |
| LOADED | Two approvals at once | The second finds the row changed | APPROVED for the first; 409 MSG-GEN-004 for the second |
| APPROVED | A later version is approved | Later valid from date reached | RETIRED (valid_to set to the day before) |
| None | Run requested | Answer passes every check | ANSWERED (agent_run.status) |
| None | Run requested | Timeout, check failure or floor | TIMED_OUT, GUARDRAIL_FAILED or BELOW_FLOOR, fallback true |
| None | Run requested | A tool is off the allow-list | GUARDRAIL_FAILED with check code TOOL_NOT_ALLOWED, fallback true |
| None | The same idempotency key arrives again | A run row already exists | No transition; the first result is returned |
| None | Evaluation started | Sample has rows; none running | RUNNING (agent_evaluation_run.status) |
| None | Evaluation started | Sample has 0 rows, or the same one is RUNNING | No row; 422 MSG-P10-002 or 409 MSG-P10-003 |
| RUNNING | Last sample row scored | None | DONE |

The states of the environment of the service - the migration applied, the topic and the queue reachable, the contracts answering - belong to RWB-P10-E1058-INF and RWB-P10-E1058-OPS and are not asserted here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, centre of excellence analyst | Loads prompt, policy and sample files; starts evaluations; reads versions and scores (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves prompt and policy versions (Rules and parameters A); reads scores |
| RW-PLATADM, platform administrator | Reads agent runs (Platform administration CRUD; R used here); runs the gateway configuration per environment |
| RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs (Platform administration R) |
| SY-AGENT, agent platform | Runs agents; reads case facts from rwb-case and extracted fields from rwb-document through the tool gateway (R); reads parameters and reference data (R) |
| The rwb-agent service identity (the rwb-agent login, DP-02) | Writes the six tables in `rwb_agent`, writes the outbox rows, calls the owner contracts and reaches INT-23 |
| rwb-access (P4) | Answers the right check and the masking decision, and refuses a role without the right with MSG-P4-002 |
| rwb-case (P3), rwb-document (P5) | Own the case facts, the parameters, the lists and the document fields this service reads |
| No role | Reads or writes `rwb_case`, `rwb_document` or any other service's schema, edits an agent run row from outside the service, or reaches INT-23 directly |

The login of the service is Not specified in the source documents (GAP-0606; ASM-0848); the story names it "the rwb-agent login (DP-02)" until it is agreed. Approval levels: no delegation of authority level applies; the approval of a version is the Rules and parameters A right, as in the legacy story.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-CAS-001, DF-CAS-003, DF-CAS-012 | recovery_case (rwb_case, owner P3) | id, product_group, region_code | Read through the rwb-case contract |
| DF-REF-012 | rule_row (rwb_decision, owner P7) | valid_from | Read through the version-in-force pattern only; no rule row is written |
| DF-AGT-001 to DF-AGT-016, DF-AGT-021 to DF-AGT-025 | agent_policy | id, agent_code, policy_version, model_code, model_version, output_schema_ref, allowed_tools, autonomy_mode, segment_product_group, segment_region_code, confidence_floor, timeout_seconds, daily_cost_cap_thb, price_per_1k_tokens_thb, alert_role, review_date, status, valid_from, valid_to, loaded_by, approved_by | Write, and read back through the admin read |
| DF-AGT-026 to DF-AGT-035 | agent_prompt | id, agent_code, prompt_version, body_text, body_hash, status, valid_from, valid_to, loaded_by, approved_by | Write; body_text is never returned by a read |
| DF-AGT-036 to DF-AGT-060 | agent_run | id, agent_code, agent_version, prompt_version, model_version, case_id, subject_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, guardrail_result, output, confidence, latency_ms, tokens_in, tokens_out, cost_thb, data_as_of, run_at, evaluation_run_id, decision_log_id, segment_product_group, segment_region_code | Write; the listing returns ids and measures only |
| DF-AGT-061 to DF-AGT-069 | agent_sample | id, agent_code, sample_code, sample_version, subject_type, subject_id, label_key, expected_value, labeled_by | Write at the load; read back as counts |
| DF-AGT-070 to DF-AGT-085 | agent_evaluation_run | id, agent_code, sample_code, sample_version, policy_version, prompt_version, model_version, status, started_at, finished_at, requested_by, total_cost_thb, p95_latency_ms, failure_counts, proposal, review_count | Write; no operation of this story fills proposal or review_count, and the proposal is filled by RWB-P10-E1060-APP |
| DF-AGT-086 to DF-AGT-096 | agent_evaluation | id, evaluation_run_id, approach, label_key, sample_size, true_positive, false_positive, false_negative, agreement_rate, precision_value, recall_value | Write |
| DF-REF-132 to DF-REF-184 | parameter_catalog, parameter_value, reference_version, reference_row (rwb_case, owner P3) | the parameter keys the run reads and the lists LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS and LOV-SUBJECT-TYPE with their versions | Read through the rwb-case parameters and reference-data contracts |
| DF-DOC-001 to DF-DOC-017 | document, document_field (rwb_document, owner P5) | the document and its extracted fields | Read through the rwb-document contract |

Field IDs are those of the Logical Data Model and Data Dictionary, copied from RWB-E1-058. agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run and agent_evaluation are the P10 tables of schema `rwb_agent` in the Ownership Map; agent_feedback and agent_alert are P10 as well and are created by the stories that own their behaviour (RWB-P10-E2032-APP and RWB-P10-E1063-APP), so this story writes neither. Every read of another service's data in this table goes through that service's contract and never through its table.

Personal data: the fields of this story hold IDs, codes, measures and masking tokens only (BR5, BR17, AC15). The fields that P2 classes as personal data are Not specified in the source documents (DOR-RWB-P10-E1058-APP-11); this story carries no personal field on that basis.

Screens: this story builds no screen. The empty, loading, error and no-access states of screen SCR-46 are Not specified in the source documents (DOR-RWB-P10-E1058-APP-10) and are not built here.

The tool name read_case is a value of agent_policy.allowed_tools and of GatherInputs; it is not a field or entity of the Logical Data Model v9 or Data Classification v5, and it is not a data row of this table.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10). The operation set is the one baselined in RWB-P10-E1058-CON.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/agent-runs` | List agent runs with fallbacks: query agent, from, to; 200 AgentRun[] | Platform administration R, scope applied | Not applicable: the call writes nothing |
| GET | `/admin/agent-configs` | List prompt and policy versions per agent with status, dates and text hash: query agent, kind, status; 200 AgentConfigVersion[] | Rules and parameters R | Not applicable |
| POST | `/admin/agent-configs` | Load a new prompt or policy version from a checked file: multipart file, kind, agent, validFrom; 201 AgentConfigVersion in status LOADED | Rules and parameters C | Idempotency-Key header, and the version number is unique per agent and kind |
| POST | `/admin/agent-configs/{versionId}/approve` | Approve a loaded version: If-Match with the row version; 200 AgentConfigVersion in status APPROVED | Rules and parameters A | Idempotency-Key header; a second approval of an APPROVED version is 409 |
| POST | `/admin/agent-samples` | Load a labeled evaluation sample: multipart file, agent, sampleCode; 201 AgentSample with the sample version and the row count | Rules and parameters C | Idempotency-Key header; each load creates the next sample version |
| POST | `/admin/agent-evaluations` | Start the evaluation harness for an agent on a labeled sample: AgentEvaluationRequest with agent, sampleCode, sampleVersion, approaches; 202 AgentEvaluationRun in status RUNNING | Rules and parameters C | Idempotency-Key header; one RUNNING run per agent, sample and sample version |
| GET | `/admin/agent-evaluations` | List evaluation runs with their score rows: query agent, from, to; 200 AgentEvaluationRun[] | Rules and parameters R | Not applicable |
| GET | `/admin/agent-evaluations/{evaluationId}/report` | Read the report of one evaluation run: sample size, agreement, failures, cost, latency and the three versions; 200 AgentEvaluationReport | Rules and parameters R | Not applicable |
| GET | `/cases/{caseId}/agent-outputs` | Read the recorded outputs of the runs of a case: 200 AgentOutput[] | Case record R, scope applied | Not applicable |

Errors: 401 no session (MSG-P4-001), 403 a role without the right (MSG-P4-002), 404 an unknown version, evaluation or case (Not specified in the source documents (CG-ALL-2495)), 409 a version number that already exists, an approver who is the loader (MSG-P7-002), a version that is not LOADED, a row changed since it was read (MSG-GEN-004) or an evaluation already RUNNING (MSG-P10-003), 422 a file that fails a check (MSG-P10-001) or a sample with no labeled rows (MSG-P10-002), 503 the store or a consumed contract unavailable (Not specified in the source documents (CG-ALL-2495)). The case-output read is delivered here because a run's evidence is read through the owner by RWB-ITG-E1058-ITG; its first business use is the Epic 3 case record. The metrics read `/admin/agent-metrics` and the feedback operation `/agent-runs/{runId}/feedback` are baselined in RWB-P10-E1058-CON and are built by RWB-P10-E1063-APP and the Epic 3 story; they are not provided here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC1 and AC5: the case facts the `read_case` tool returns, read as SY-AGENT | One hop, 2 s |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | AC5: the document and its extracted fields, read as SY-AGENT by the document tool | One hop, 2 s |
| GET | `/api/recovery/case/v1/parameters/{key}` | P3 rwb-case | AC2: the parameter keys the run reads, with their version in force | One hop, 2 s |
| GET | `/api/recovery/case/v1/reference-data/{lovCode}` | P3 rwb-case | AC2: LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS and LOV-SUBJECT-TYPE with their version | One hop, 2 s |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | AC7: the Rules and parameters, Platform administration and Case record rights, the scope and the masking decision, before each operation | One hop, 2 s |
| GET | `/api/recovery/access/v1/masking-policies` | P4 rwb-access | AC7: the masking policy in force for SY-AGENT, read once per run | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11); rwb-agent calls no service through another service and holds no schema client of another service. The model budget of up to 60 seconds belongs to AgentRunWorkflow and to INT-23 and is never a REST budget of this story.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | runid, agent, caseid, fallback, outcome (EV-28 fields of Kafka Catalog v1) |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | record reference, decision code, agent version, model version, inputs reference, final call, the actions |

Both are CloudEvents 1.0 messages inserted in the outbox in the same transaction as the row they describe and relayed by the outbox library; a payload is validated against its registry subject before the relay (DP-09). The agent operations of this story write no decision record: the record of a case step is written by that step through the same library, which RWB-P10-TE013 owns, and this story proves the library's write path with one synthetic record in its tests (DP-03; ASM-0849).

#### 12.4 Events consumed

None. The service consumes no topic in this story. The inbox of the outbox library is installed and its first consumers are declared where the behaviour is built: `rwb.case.CaseCreated.v1` by RWB-P10-E1059-APP and `rwb.document.DocumentStored.v1` by RWB-P10-E1062-APP (Arch v5 slide 16). This story dedupes through the inbox table it creates and proves the dedupe with a replay of its own event in a test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow, one execution per idempotency key; workflow ID form Not specified in the source documents (CG-ALL-2498); started as a child of the route or pricing stage workflow per Temporal Catalog v1; duplicate-start policy Not specified in the source documents (CG-ALL-2498) | `rwb-agent` | Input: agent code, case ID, subject ID, trigger event, idempotency key, inputs. The 60 second budget of the policy, then the rule result (Arch v5 slide 16) |
| ResolveAgentConfig | Activity | `rwb-agent` | Output: the approved policy and prompt versions in force on the run date, their schema reference, tools, timeout, floor, price and cap, and the parameter and list values |
| GatherInputs | Activity | `rwb-agent` | Output: the tool results read through the owner contracts; a tool off the allow-list is refused here |
| MaskInputs | Activity | `rwb-agent` | Output: the masked inputs and the masking decision; no personal value leaves the activity |
| CallModelGateway | Activity | `rwb-agent` | Input: model code, masked inputs, output schema reference, timeout. Output: the answer, the token counts and the latency, or the mapped status TIMED_OUT or MODEL_ERROR |
| CheckGuardrail | Activity | `rwb-agent` | Input: the answer and its schema reference. Output: the check codes SCHEMA, TOOL_NOT_ALLOWED or BELOW_FLOOR, or a clean answer |
| RecordAgentRun | Activity (workflow kit) | `rwb-agent` | Input: the run row and the outbox row; one transaction, no partial write |

The workflow name, the queue and the 60 second budget are those of Arch v5 slide 16 and the Temporal and Drools design (slide 12, "Agent run with rule fallback"); the activity names and their inputs and outputs are this story's design and are accepted by RWB-P10-E1058-CON. A calling step submits through the agent runtime client of RWB-P10-TE013-CON and never starts the workflow itself (DP-20).

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story: the Arch v5 job map names no job for the agent platform (slide 44), a run is started by a calling step, and an evaluation is started by RW-COE. The retention of the run rows is a data decision of the service and no source names a Schedule for it.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_policy | P10 (rwb_agent) | A version of an agent's policy: model, tools, autonomy, limits and fallback; unique (agent_code, policy_version) |
| agent_prompt | P10 (rwb_agent) | A version of an agent's prompt text with its hash; unique (agent_code, prompt_version) |
| agent_run | P10 (rwb_agent) | One call of an agent, with its versions, checks, answer, cost and fallback; unique (idempotency_key) |
| agent_sample | P10 (rwb_agent) | One labeled subject in a versioned evaluation sample |
| agent_evaluation_run | P10 (rwb_agent) | One evaluation of an agent version against a sample; one RUNNING run per agent, sample and sample version by a partial unique index |
| agent_evaluation | P10 (rwb_agent) | The score of one approach on one label key: TP, FP, FN, sample_size, precision and recall |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | The outbox, inbox and idempotency envelope (DP-09) |

The tables are created by `Vnnnn__agent_runtime.sql` in the rwb-agent Flyway sequence; agent_feedback and agent_alert are P10 tables created by RWB-P10-E2032-APP and RWB-P10-E1063-APP. The service reads no table of another service and holds no foreign key across services (DP-01): `case_id`, `subject_id`, `evaluation_run_id` and `decision_log_id` are cross-service references by ID only, as TSD P10 v2 T3.3 draws them.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock | The P3 contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON, and the case read | The parameter keys of the policy in force; LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS and LOV-SUBJECT-TYPE with their versions; the case facts of RW-2026-000101, RW-2026-000102 and RW-2026-000103; a list version that lacks a value the run uses; an answer beyond 2 s |
| rwb-document WireMock | The P5 contract | The document and its extracted fields for DOC-2026-000101; a document that does not exist; an answer beyond 2 s |
| rwb-access WireMock | The P4 contract of RWB-P4-E1037-CON | `POST /authorise` granting Rules and parameters C to RW-COE, A to RW-RISK and Platform administration R to RW-PLATADM, refusing a role without the right, the masking decision, and `GET /masking-policies` with the masking policy of SY-AGENT |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the admin operations and the case-output read, one hop, with the media types preserved |
| INT-23 model gateway stub | The external request of section 12.9 | An answer of 1,200 ms with 900 input and 150 output tokens; an answer with field "summary" missing; an answer with confidence 0.79; silence for 61 seconds; a 4xx and a 5xx; each request body is captured, and the masking assertion of AC7 reads the captured request |
| Decision-record library stub and outbox stub | The platform libraries of RWB-PLT-E1027-CON and RWB-PLT-TE006-CON | One record written in the same transaction as its outbox row; a failed subject that routes to `.dlt` |

Every fixture is synthetic. No test calls a live model endpoint with real prompts, and no test reads a production account, document or record.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 9 provided, 6 consumed | The eight admin operations and the case-output read provided on `/api/recovery/agent/v1`; the case read, the document read, the parameter read, the reference-data read, the authorise call and the masking-policy read consumed; one hop, 2 s each; the INT-23 call is HTTPS at the boundary with the policy timeout of up to 60 seconds |
| Kafka | 1 published, 0 consumed | EV-28 on `rwb.agent.events.v1` through the outbox, with the retry topic and the `.dlt` topic; the record event on `rwb.decision-record.v1` is the library's and this story's operations write none |
| Temporal | 1 workflow, 6 activities | AgentRunWorkflow and ResolveAgentConfig, GatherInputs, MaskInputs, CallModelGateway, CheckGuardrail and RecordAgentRun on queue `rwb-agent` |
| File | None | The policy, prompt and sample files arrive in the multipart body of a load operation and no file path or bucket is used; the policy, the prompt and the sample are rows of `rwb_agent` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent`, the service module `rwb-agent`, with sub-packages `gateway`, `config`, `orchestrator`, `guardrail`, `eval`, `api` and `workflow`. Front end: none.

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
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | H RWB-P10-TE013-CON |

The H and C dependencies of this table are the ones in the metadata rows: the platform contract stories, RWB-P10-E1058-CON and RWB-P10-TE013-CON are build dependencies, and RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P4-E1037-CON are contract dependencies built against their fakes. DP-11 sits behind the tool reads and adds no dependency of its own; the 60 second model budget is the workflow budget and not a REST budget.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentRuntimeController | Controller | `GET /admin/agent-runs` and `GET /cases/{caseId}/agent-outputs`; maps errors to problem responses |
| AgentConfigController | Controller | `GET` and `POST /admin/agent-configs`, and `POST /admin/agent-configs/{versionId}/approve` |
| AgentEvaluationController | Controller | `POST /admin/agent-samples`, `POST` and `GET /admin/agent-evaluations`, and the report |
| ModelGatewayClient | Client | Calls INT-23 as the service identity with the model code, the masked inputs and the schema reference, bounded by the policy timeout; no retry inside a step |
| AgentConfigService | Service | Validates and stores prompt and policy versions, resolves the version in force for a date, and enforces that the loader is not the approver |
| AgentOrchestrator | Service | Runs one agent step: resolve config, gather inputs through the tools, mask, call, check, record |
| AgentRuntimeService | Service | Implements the orchestrator; writes agent_run and the outbox event in one transaction |
| ToolGateway | Service | Executes allowed tools only, as SY-AGENT, through the rwb-case and rwb-document contracts; holds no schema client |
| GuardrailChecker | Service | Schema check (JSON Schema draft 2020-12), tool allow-list check and confidence floor check, with the check codes |
| PromptInputMasker | Client | Reads the masking policy of rwb-access and replaces every personal value with its token before the prompt is built |
| EvaluationHarness | Service | Runs the agent in shadow on each sample row, scores it against the labels and writes the score rows |
| AgentRunRepository, AgentConfigRepository, AgentEvaluationRepository | Repository | Read and write the six `rwb_agent` tables only |
| AgentPolicy, AgentPrompt, AgentRun, AgentSample, AgentEvaluationRun, AgentEvaluation | Entity | JPA entities for the six tables |
| AgentRunWorkflow and its six activities | Workflow kit | The run of one agent on queue `rwb-agent`, with the 60 second budget and the rule result |

**Database and migrations.** `Vnnnn__agent_runtime.sql` creates the six tables in `rwb_agent` with the standard record columns (is_active, state, version, created_at, created_by, updated_at, updated_by) and the keys of TSD P10 v2 T3.1 and the legacy section 13: primary key on `id`; unique (agent_code, policy_version) on agent_policy; unique (agent_code, prompt_version) on agent_prompt; unique (idempotency_key) on agent_run; unique (agent_code, sample_code, sample_version, subject_id, label_key) on agent_sample; a partial unique index on agent_evaluation_run (agent_code, sample_code, sample_version) where status = 'RUNNING'; and the index agent_run (agent_code, run_at). The library objects outbox_event, processed_event and idempotency_key are created by the same migration from the platform library. In this file name nnnn is the next number of the service's own Flyway sequence (V0001 to Vnnnn, Service Template Specification v1 §3), and the later P10 migrations of this service take the numbers after it (ASM-0856). The sample key above follows the legacy story: the physical schema of today states (sample_code, sample_version, label_key), and the difference is carried as GAP-0606 and settled in ASM-0858.

**Configuration and reference data**

- Policy version "P1" of agent "ECHO" (mode SHADOW, allowed tools `read_case`, output schema reference of the test agent) and prompt version "PR1", loaded by RW-COE and approved by RW-RISK through the operations of this story; the test seed files are synthetic and live in `src/test/resources/agent/`.
- The parameter keys of the policy in force, read through `GET /api/recovery/case/v1/parameters/{key}`; no key name is written in code (DP-06; ASM-0852).
- LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS and LOV-SUBJECT-TYPE, read through `GET /api/recovery/case/v1/reference-data/{lovCode}` (DP-07).
- The versioned policy and prompt JSON schemas, which hold the check limits (timeout 1 to 120 seconds, confidence floor 0 to 1) and are versioned with the policy loader (legacy section 13).
- Environment properties that are not business values: the service base URL, the INT-23 endpoint reference held in Key Vault, the topic and queue names, and the 2 second client budget.
- The feature flag `rwb.agent.platform`, held as a row of the platform feature-flag library (ASM-0851): off, the orchestrator returns a fallback result with reason "DISABLED" and makes no model call.

**Build steps**

1. Write the Flyway migration and the entities; test the keys with Testcontainers PostgreSQL, on an empty `rwb_agent` schema.
2. Build AgentConfigService and AgentConfigController: load, validate, store, approve, version in force by date, loader-not-approver and the row-version race (AC2, AC8, AC9, AC12).
3. Build ModelGatewayClient against a WireMock stub of INT-23, with the timeout and the token and latency mapping (AC1, AC6).
4. Build PromptInputMasker over the rwb-access masking policy read and a log filter test that fails on any personal pattern (AC7).
5. Build GuardrailChecker and ToolGateway with the allow-list, the schema check and the floor check (AC3, AC5, AC10).
6. Build AgentRunWorkflow and AgentRuntimeService: orchestrate, record agent_run, the outbox row, idempotency and the fallback result (AC1, AC11).
7. Build EvaluationHarness and AgentEvaluationController: sample load, start, poll, score rows, report, empty sample and already-running refusals (AC4, AC13, AC14).
8. Build AgentRuntimeController for the run listing and the case-output read, with the access tests (AC15).
9. Build the contract clients for the rwb-case and rwb-access contracts, the parameter and list reads, and the missing-value path (X13).
10. Pipeline scans for another service's table name, for a cross-schema foreign key, for a list or parameter value in the source, and for a personal pattern in the log (AC7).

**Done when.** The sixteen test cases of section 16 pass, the nine operations answer on `/api/recovery/agent/v1`, a DEV run of agent "ECHO" over the legacy fixture produces one run row and one event with the legacy values, the migration applies cleanly on an empty `rwb_agent` schema, no list or parameter value appears in the source, the log scan finds no personal data, and the dependency on RWB-P10-E1058-INF and RWB-P10-E1058-OPS for the endpoint, the topic and the deployment is recorded and not restated here.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | A prompt, policy or sample file fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | Evaluation started on a sample with no labeled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Evaluation started while the same one is running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P7-002 | Loader tries to approve their own version | You prepared this decision, so you cannot approve it. |
| MSG-GEN-004 | Approval of a version that changed since it was read | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | No session | Not specified in the source documents (DOR-RWB-P10-E1058-APP-9) |
| MSG-GEN-001 | A required form field is empty (agent, kind, file) | Enter {field}. |

The seven texts other than MSG-P4-001 are copied unchanged from RWB-E1-058. MSG-P4-001 is used by this story and its text is not specified in the source documents (DOR-RWB-P10-E1058-APP-9). Thai text for each message follows decision DL10. In AC8 the {kind} value is "policy", the {agent} value is "ECHO" and the {check} value is "timeout_seconds between 1 and 120". In the access test TC-E1-058-16 the {action} value is "read the agent runs or load a configuration".

### 15. Screens and states

No screen in this story. RW-PLATADM and the other Platform administration R holders read runs through `GET /api/recovery/agent/v1/admin/agent-runs`; RW-COE and RW-RISK read versions, evaluations, scores and the report through the configuration and evaluation operations; a case's recorded outputs are read through `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs`. All of them are reached through the gateway-bff route in front of the admin path, so a screen never calls rwb-agent directly (DP-19), and the exact route name and path are Not specified in the source documents (GAP-0607; ASM-0857). The agent monitor screen SCR-46 and its states come with RWB-E2-031 and RWB-P10-E1063-APP and are not changed here; the autonomy-level screen is Epic 3 and is out of scope. The states empty, loading, error and no access of SCR-46 are Not specified in the source documents (CG-ALL-2508).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-058-01 | AC1, BR1, BR7 | Component | Agent ECHO, case RW-2026-000101, stub answer 1,200 ms, 900 and 150 tokens |
| TC-E1-058-02 | AC2, BR2 | Component | Prompt PR1 then PR2 valid from 2026-11-20; runs on 2026-11-19 and 2026-11-20 |
| TC-E1-058-03 | AC3, BR4 | Component | Stub answer missing field "summary" |
| TC-E1-058-04 | AC4 | Component | Sample ECHO-S1 version 1, 20 rows |
| TC-E1-058-05 | AC5, BR4, BR6 | Component | Tool call "propose_deviation" with allow-list "read_case" |
| TC-E1-058-06 | AC6, BR3 | Component | Stub silent for 61 seconds |
| TC-E1-058-07 | AC7, BR5 | Component | Case RW-2026-000103 with synthetic national ID and mobile number |
| TC-E1-058-08 | AC8, BR10 | Component | Policy file with timeout_seconds 0 |
| TC-E1-058-09 | AC9, BR8 | Component | Loader coe.user01 approves own version P2 |
| TC-E1-058-10 | AC10, BR4 | Component | Stub confidence 0.79, floor 0.80 |
| TC-E1-058-11 | AC11, BR9 | Component | Key ECHO:RW-2026-000101:2026-11-30 sent twice |
| TC-E1-058-12 | AC12 | Component | Two parallel approvals of P2, row version 1 |
| TC-E1-058-13 | AC13 | Component | Sample ECHO-S2 with 0 rows |
| TC-E1-058-14 | AC14 | Component | Evaluation of ECHO on ECHO-S1 version 1 already RUNNING |
| TC-E1-058-15 | AC15 | Component | 3 runs of ECHO from 2026-11-30 to 2026-12-01 |
| TC-E1-058-16 | Access | Contract | RW-CASEOWN calls GET /admin/agent-runs and POST /admin/agent-configs through the rwb-access contract fake; refused with MSG-P4-002 |
| TC-E1-058-17 | BR12, ASM-3438 | Component | Migration Vnnnn__agent_runtime.sql run on an empty rwb_agent schema; each table of section 12.7 is created and no foreign key crosses services |
| TC-E1-058-18 | AC16, BR16 | Contract | RW-CASEOWN calls GET /admin/agent-runs with no Platform administration right through the rwb-access contract fake; refused with MSG-P4-002 |
| TC-E1-058-19 | AC17, BR15 | Component | rwb-case contract fake answers outside the 2 s client budget; the tool result is empty, the guardrail records the failed read and the run ends with fallback true |
| TC-E1-058-20 | AC18, BR11 | Component | Parameter key from rwb-case names a value the policy does not allow; the run is refused before the model call, the value is named on the run and no code default is used |
| TC-E1-058-21 | AC19 | Component | Migration of the rwb-agent Flyway sequence fails; the new version does not start, the version in force keeps serving and no run row or version row is written |
| TC-E1-058-22 | BR13 | Component | One run completion; the run row and its outbox row are written in one transaction, and a failed write leaves neither |
| TC-E1-058-23 | BR14 | Component | Calling step submits agent ECHO for case RW-2026-000101 through the agent runtime client; the run is reached only through that client and queue rwb-agent |
| TC-E1-058-24 | BR17 | Component | Run of ECHO checked in the listing, the event, the workflow history and the application log; none holds prompt text or a model answer |
| TC-E1-058-25 | AC20, BR11, BR12, BR13, BR14, BR15, BR16, BR17 | Contract | Rules of section 8 checked against the service code, the rwb_agent schema, the topic definitions and the guard and boundary tests of section 13 |
| TC-E1-058-26 | AC21 | Contract | Call to GET /admin/agent-runs with no session answers 401 with MSG-P4-001; GET /cases/{caseId}/agent-outputs for a case that does not exist answers 404; the right is checked through the rwb-access contract fake |

TC-E1-058-01 to TC-E1-058-16 are the sixteen legacy test cases of RWB-E1-058, kept in legacy order with their legacy IDs and their legacy data. The legacy System level becomes Component because each of them now proves one component or one operation of the service against its fakes, and the legacy Access level becomes Contract because the refusal is proved against the published rwb-access contract. The service change that the legacy criteria do not name - the base of the operation set, the schema and the no-cross-schema rule, the tool reads, the parameter and list reads, and the right and masking path - is proved by the contract tests of section 13 and by the `-ITG` copies of RWB-ITG-E1058-ITG, which runs the same behaviour against the real services. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: model, prompt, timeout, confidence floor, tool list, price, cap and list values are read from approved version rows and the rwb-case contracts at run time, and a missing value stops the run instead of falling back to a default (BR11, DP-06, DP-07).
- No personal data in logs, tests, events, workflow inputs or prompts: test data is synthetic in DEV and masked in SIT, and no national ID number, name, phone number or account number reaches the model, the run row or the log (BR5, legacy section 17).
- ACE data only through the owner's contract: case facts come from rwb-case and document fields from rwb-document, and the service holds no grant on `rwb_case`, `rwb_document` or any other schema (DP-01, DP-11).
- The service writes its own schema only: the six tables and the library objects in `rwb_agent`, and no cross-schema foreign key (BR12, DP-15).
- The model endpoint is reached only through ModelGatewayClient, as the service identity, on its private endpoint, with the endpoint reference in Key Vault and never in a value or a log (BR1).
- Prompt text and model answers never appear in the listing, in an event, in a workflow history or in the application log (BR17).
- Every consumed call is one hop with the 2 s client budget, and the 60 second model budget is the workflow budget only (BR14, BR15).
- The admin reads are reached through the gateway-bff route and never from a screen to the service (DP-19).
- Every message is a CloudEvents 1.0 record validated against its registry subject before the relay, with a `.dlt` route on failure (BR13, DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-010 | Agents run under service identities with the same role checks as people | Business Requirements Program, section 5.4 | FEAT-AGT-01, FEAT-AGT-02 | All recovery processes | R-UNI-32, R-UNI-40 | TC-E1-058-01, TC-E1-058-05, TC-E1-058-16 |
| REQ-ACA-005 | Personal data masked by role in every agent call | Business Requirements Program, section 5.4 | FEAT-AGT-01 | All recovery processes | None | TC-E1-058-07 |
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | Business Requirements Program, section 5.7 | FEAT-AGT-01, FEAT-AGT-05, FEAT-AGT-11 | 15 Manage performance, data and AI | R-UNI-38 | TC-E1-058-02, TC-E1-058-04, TC-E1-058-06, TC-E1-058-08, TC-E1-058-09 |
| D-RCV-60 DP-01 | The six agent tables are the service's own in `rwb_agent`, and every other fact is read through its owner's contract | Template and Rules §R5.5; Arch v5 slide 41 | FEAT-AGT-01 | 15 Manage performance, data and AI | None | TC-E1-058-01, TC-E1-058-05, TC-E1-058-17 |
| D-RCV-60 DP-03 | The local decision-record library and `rwb.decision-record.v1` are installed, and the record of a step stays with its owner | Template and Rules §R5.5; ADR-022 | FEAT-AGT-01 | 15 Manage performance, data and AI | None | TC-E1-058-01 |
| D-RCV-60 DP-06 | The parameter values are read through the rwb-case parameters contract at run time | Template and Rules §R5.5 | FEAT-AGT-01 | 15 Manage performance, data and AI | R-UNI-38 | TC-E1-058-02, TC-E1-058-06 |
| D-RCV-60 DP-07 | The lists are read through the rwb-case reference-data contract | Template and Rules §R5.5 | FEAT-AGT-01 | 15 Manage performance, data and AI | None | TC-E1-058-04, TC-E1-058-13 |
| D-RCV-60 DP-08 | The right check and the masking decision come from rwb-access through the guard library | Template and Rules §R5.5 | FEAT-AGT-01, FEAT-AGT-02 | 15 Manage performance, data and AI | None | TC-E1-058-07, TC-E1-058-16 |
| D-RCV-60 DP-09 | The run row and its event are written through the outbox on `rwb.agent.events.v1` | Template and Rules §R5.5; ADR-015 | FEAT-AGT-01 | 15 Manage performance, data and AI | None | TC-E1-058-01, TC-E1-058-11 |
| D-RCV-60 DP-11 | The tool reads are one hop with a 2 s client budget against the owner contracts | Template and Rules §R5.5; ADR-020 | FEAT-AGT-01 | 15 Manage performance, data and AI | None | TC-E1-058-01, TC-E1-058-05, TC-E1-058-06 |
| D-RCV-60 DP-13 | The operations are served on `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-01 | 15 Manage performance, data and AI | None | TC-E1-058-08, TC-E1-058-15 |
| D-RCV-60 DP-15 | The six tables are created by the service's own Flyway sequence | Template and Rules §R5.5; ADR-021 | FEAT-AGT-01 | 15 Manage performance, data and AI | None | TC-E1-058-01, TC-E1-058-04, TC-E1-058-17 |
| D-RCV-60 DP-19 | The admin reads are reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-AGT-01 | 15 Manage performance, data and AI | None | TC-E1-058-15 |
| D-RCV-60 DP-20 | A calling step reaches a run through the rwb-agent contract and AgentRunWorkflow | Template and Rules §R5.5 | FEAT-AGT-01, FEAT-AGT-11 | 15 Manage performance, data and AI | R-UNI-32 | TC-E1-058-06, TC-E1-058-11 |
| RWB-E1-058 (legacy story) | Agent platform set-up [E1a]: the fifteen criteria AC1 to AC15 and the access test | Business Requirements Epic 1, section 3.9 | FEAT-AGT-01, FEAT-AGT-02, FEAT-AGT-05, FEAT-AGT-11 | 15 Manage performance, data and AI | R-UNI-32, R-UNI-38, R-UNI-40 | The sixteen legacy test cases of section 16 |
| RWB-ITG-E1058-ITG (integration copy) | The same behaviour proved across rwb-case, rwb-document, rwb-access and rwb-agent on the real services | Business Requirements Epic 1, section 3.9 | FEAT-AGT-01 | 15 Manage performance, data and AI | None | The nineteen test cases of that story |

The gap GAP-0606 records what the sources leave open for this story - the service login, the gateway-bff route, the tool reads of the two owners, the parameter keys and lists, the sample key and the migration numbering - and each default it raises is settled by an assumption row of this key. The two external dependencies are tracked and do not block the build: RWB-P10-E1058-INF provisions the endpoint, the topic, the queue and the login, and RWB-P10-E1058-OPS deploys the service.

Open decisions DL10, DL11 and DL33 stay open and each carries its assumptions: DL10 with ASM-2250, ASM-2357, ASM-2377 and ASM-2863; DL11 with ASM-0553, ASM-0703, ASM-1051 and ASM-1104; DL33 with ASM-0135, ASM-0140 and ASM-0890.

The legacy criterion AC5 (stale input flagged from a COMPLETED ALS row) and its test case TC-E1-059-05 are not owned by this story. They sit with RWB-ITG-E1059-ITG, and this story neither builds nor reconstructs them (GAP-0610).

### 19. Out of scope

- The cross-service behaviour of this key: RWB-ITG-E1058-ITG, and the harness RWB-ITG-W1J01-ITG.
- The contract baseline, the payload schemas, the error model and the fakes as published artefacts: RWB-P10-E1058-CON.
- The private path to INT-23, the login, the Key Vault entries, the topic with its retry and `.dlt` topics, the queue and its worker identity, the sizing, the budgets and the pipeline gates: RWB-P10-E1058-INF.
- The chart, the pipeline, the migration job, the configuration and secrets injection, the probes, the dashboards, the alerts, the runbook and the blue-green path of the admin operations: RWB-P10-E1058-OPS.
- The rule fallback inside a case step and the decision record of that step: RWB-P10-TE013 and RWB-P10-TE013-CON.
- The case intake agent (RWB-P10-E1059-APP), the extraction evaluation (RWB-P10-E1060-APP), the TDR offer-suggestion model (RWB-P10-E2032-APP) and the deviation screening agent (RWB-P10-E1062-APP).
- The monitoring dashboard, the cost alert and the metrics read (RWB-E1-063, RWB-E2-031, RWB-P10-E1063-APP).
- Changing an autonomy level through a screen (FEAT-AGT-12, Epic 3), the feedback operation of a run and the case-output read as a business feature (Epic 3).
- The choice of model endpoint (DL33): the run reads the model code and version of the policy and never selects an endpoint.
