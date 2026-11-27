# RWB-P10-E1058-CON Agent platform set-up [E1a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1058-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Epic design sign-off | Epic design is signed in the month before build (Decision Log v12 DT05); no signed design record for this epic is in the source documents (DOR-RWB-P10-E1058-CON-14) |
| Size | Not specified in the source documents (DOR-RWB-P10-E1058-CON-16) |
| Contract version | v1, base path /api/recovery/agent/v1 (DP-13) |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-N001-CON (platform prerequisites of the service template, not per-story blockers) |
| Contract dependencies | RWB-P10-E2032-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, and the published contract of the P4 authorise call (Not specified in the source documents (GAP-2404)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-024, FR-P10-025) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of RWB-E1-058 for rwb-agent. This is the agent-platform contract of the key: the eleven operations of the platform on the base `/api/recovery/agent/v1` (DP-13), the schema `rwb_agent` with the eight agent tables and their keys (DP-01), the EV-28 payload on `rwb.agent.events.v1` with its envelope and registry subject (DP-09), the decision-record payload written through the local library on `rwb.decision-record.v1` (DP-03), the INT-23 model-gateway request at the boundary with the policy timeout (DP-11 as the recorded exception), the consumed contracts of rwb-case, rwb-document, rwb-access and rwb-decision (DP-06, DP-07, DP-08), and the contract fakes every build of the key uses. It builds no business behaviour and adds no business value. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 24 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-agent**, I want **the agent-platform side of RWB-E1-058 fixed as a contract on Day 1 - the eleven operations on the base `/api/recovery/agent/v1` with their requests, answers, rights, refusals and idempotency, the schema `rwb_agent` and its eight tables with their keys, the EV-28 payload on `rwb.agent.events.v1` as a CloudEvents 1.0 message with a retry topic and a `.dlt` topic, the decision-record payload on `rwb.decision-record.v1`, the INT-23 request at the boundary with its timeout and its status mapping, and the five contract fakes with their synthetic fixtures**, so that **the app story, the infrastructure story and the deployment story of this key, and the calling services that reach an agent through the rwb-agent contract, all build against one agreed and testable shape on Day 1, without waiting for the agent runtime to be complete and without any of them inventing an answer of its own**.

### 2. Business rationale

The legacy key was written against a Java interface inside one process: `AgentOrchestrator.run` returned an `AgentRunResult`, `ToolGateway` called another module's interface, `RecoveryAccessGuard` and `PromptInputMasker` ran in the caller's transaction, the run row and the decision log entry were tables of one schema, and `EV-28` was an in-process event written by the same deployment (legacy section 12). In the target every one of those is a boundary:

- the published interface becomes a contract with two faces - the operations of the platform on the base `/api/recovery/agent/v1` and the run that a calling step reaches through the agent runtime client and AgentRunWorkflow on queue `rwb-agent` (DP-11, DP-13, DP-20; ASM-0850);
- the run table becomes one table of eight in schema `rwb_agent`, owned by P10, with the keys that the legacy section 13 fixed and the field list of TSD P10 v2 T3.1 (DP-01; AC4);
- the run completion becomes EV-28 on the service's own topic with a retry topic and a `.dlt` topic, and a decision of a calling step becomes a record on the shared topic through the local library (DP-09, DP-03; AC3);
- the case facts, the parameter keys, the lists, the document fields, the right and the masking decision come through their owners' contracts, because the service holds no grant on another schema (DP-06, DP-07, DP-08; ASM-0851);
- the model is reached at the Enterprise AI private endpoint INT-23, which is the only outside call of the service, and its request is small and load-bearing: the model code, the masked inputs and the output schema reference (ASM-0850; AC5).

Contract-first only works if the seam is written down once. The seam here is the platform every later agent stands on: four other agent keys of this service and the calling services of wave 1 read a run, a version or a score through it. If the shape is agreed and faked on Day 1, four teams move at once - the app story of RWB-P10-E1058-APP builds the gateway client, the store, the guardrail, the harness and the workflow against these fakes; the infrastructure story provisions the endpoint, the topic, the queue, the login and the alarms against the same names; the deployment story wires the migration job, the probes and the alerts against the same operations; and the calling services read one shape. Without it, each caller invents its own answer, the version record of a run stops matching the version in force, and the evidence of what an agent answered stops being readable by the owner.

This document owns the consumed side and the provided side of the key and never restates what another owner holds: the case, its parameters and its lists are rwb-case's, the document and its fields are rwb-document's, the right and the masking policy are rwb-access's, the central decision ledger is rwb-decision's, the case-output read as a business feature is Epic 3's, and the metrics read belongs to the monitor story (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the base, the topic, the event names, the queue and the schema follow the platform rule and not a local choice (§R4; DP-13, DP-14).
- The CloudEvents 1.0 envelope, the platform error envelope, the idempotency rule and the message-catalogue convention are the platform baseline; this document narrows them where it must and says so.
- The decision-record library of RWB-PLT-E1027-CON publishes the record shape and the topic `rwb.decision-record.v1` with its envelope (DP-03).
- The outbox and inbox library of RWB-PLT-TE006-CON publishes the outbox and inbox envelope, the relay and the `.dlt` rule (DP-09).
- The parameter and reference-data client libraries of RWB-PLT-E1042-CON and RWB-PLT-E1043-CON and the access guard library of RWB-PLT-E1037-CON are published (DP-06, DP-07, DP-08).
- The per-service Flyway library of RWB-PLT-E1044-CON and the gateway-bff route contract of RWB-PLT-N001-CON are published (DP-15, DP-19).
- The agent runtime client of RWB-P10-TE013-CON is known: it submits to AgentRunWorkflow on queue `rwb-agent` and returns the run result or the fallback to the caller (DP-20).
- The Enterprise AI private endpoint INT-23 is named as the external system and its request elements are the legacy ones; its host, port, certificate and the Key Vault entries are Not specified in the source documents (GAP-0608; ASM-0854) and are provisioned by RWB-P10-E1058-INF.
- No per-story build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W1; the platform prerequisites named in the header are not per-story blockers.
- The deployment values of the service (replica counts, resources, probes, windows and alert thresholds) are Not specified in the source documents (GAP-0609); each is a reviewed value per environment, the later migrations follow the service's own Flyway sequence, and the flag rwb.agent.platform is read from the platform library and never held in a chart.

### 4. Flow

1. Draft the eleven operations of the platform on the base `/api/recovery/agent/v1`: method, path below the base, request members, answer resource, rights, refusals, idempotency and the one-hop budget, taking the operation set from TSD P10 v2 T-A.1 and T-A.2 and the legacy section 12 (AC1).
2. Fix the error model: the status codes per operation, the business message IDs of the legacy section 14 and the platform codes, and the rule that no refusal is answered without one of them (AC2).
3. Declare the schema `rwb_agent` with the eight agent tables, their columns from TSD P10 v2 T3.1, their keys from the legacy section 13 and the ownership ruling that every one of them is P10's (AC4).
4. Declare EV-28 `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`: the CloudEvents 1.0 envelope, the key, the payload members taken from the `agent_run` fields, the registry subject with BACKWARD compatibility, and the retry and `.dlt` route (AC3).
5. Declare the decision-record payload written through the local library on `rwb.decision-record.v1`, with the rule that the record of a case step is written by that step and never by an agent run (AC3).
6. Fix the INT-23 request at the boundary: the model code, the masked inputs and the output schema reference, the policy timeout, and the mapping of a timeout, a 4xx, a 5xx and a schema failure to a status of LOV-AGENT-RUN with fallback true (AC5).
7. Restate the consumed operations of rwb-case, rwb-document, rwb-access and rwb-decision with their rights, their answers and their 2 s budget, and mark each as the owner's and not this story's (AC1). Case facts are read only through the rwb-source-data tool contract, and extracted document fields only through the rwb-document tool contract, each in one hop within the 2 s budget; rwb_agent holds no grant on the recovery schema or on any other service schema.
8. Write the contract fakes with synthetic fixtures: rwb-case, rwb-document, rwb-access, rwb-decision, the gateway-bff route, the INT-23 model gateway, the decision-record library and the outbox (AC5, AC6).
9. Publish the nine sub-tables of section 12 and the contract tests, including a drift test between each fake and this document (AC6).
10. Tag the baseline and hand it to RWB-P10-E1058-APP, RWB-P10-E1058-INF, RWB-P10-E1058-OPS, the other agent keys of the service and RWB-ITG-E1058-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of an operation drifts from this document: a renamed member, a retyped field, a dropped status | The contract test fails and the merge is blocked | None | AC1 |
| X2 | A request misses a required member, or a role without the right calls an operation | Refused with 422 and MSG-GEN-001 naming the member, or with 403 and MSG-P4-002; nothing is written | MSG-GEN-001, MSG-P4-002 | AC1, AC2 |
| X3 | A prompt, policy or sample file fails a load check | Refused with 422 and MSG-P10-001; the version in force is unchanged and no version row exists | MSG-P10-001 | AC2 |
| X4 | The person who loaded a version approves it, or two approvals of one row version arrive at once | Refused with 409 and MSG-P7-002 for the loader, and with 409 and MSG-GEN-004 for the second approval | MSG-P7-002, MSG-GEN-004 | AC2 |
| X5 | An evaluation is started on an empty sample, or on a sample already RUNNING | Refused with 422 and MSG-P10-002, or with 409 and MSG-P10-003 | MSG-P10-002, MSG-P10-003 | AC2 |
| X6 | A payload gains a personal field, fails its registry subject, or the topic is unreachable | The payload is refused before the relay and routed to the `.dlt` topic with an alert; the outbox row is kept until the relay succeeds | None | AC3 |
| X7 | A name outside the family `rwb.agent.<Event>.v1` is published on the agent topic | The registry subject does not resolve and the message is refused before the relay | None | AC3 |
| X8 | The model gateway answers a 4xx or a 5xx, returns nothing inside the policy timeout, or answers outside the output schema | The run maps to MODEL_ERROR, TIMED_OUT or GUARDRAIL_FAILED with fallback true, and no status outside LOV-AGENT-RUN is written | None | AC5 |
| X9 | A fake drifts from this document, or a fixture holds a production value | The contract test fails, the merge is blocked, and the fixture is replaced with a synthetic one | None | AC6 |
| X10 | A key of an agent table is loosened, or a foreign key crosses a schema | The schema drift test fails against the declared keys and the boundary scan blocks the change | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and the four owner contracts as published, and owns no running code |
| Negotiable | The media type, the paging of a list, the exact member types of a report and the fixture composition are settled with their owners; the operation set, the table keys, the event payload, the boundary mapping and the message IDs are fixed by this realignment |
| Valuable | Unblocks the app, infrastructure and deployment stories of this key and the four agent keys of the service on Day 1 |
| Estimable | Eleven operations, eight tables, two event payloads, one boundary contract, eight fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is asserted against the artefact - a schema file, a payload, a fake, a key, a status - and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Agent-platform contract baseline of rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the decision-record library, the outbox library and the access guard library of the platform are in force
    Given the rwb-agent service identity exists and holds grants on schema rwb_agent only

  Scenario: AC1 The eleven operations of the platform are declared on the agent base (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When the eleven operations of section 12.1 are reviewed against TSD P10 v2 T-A.1 and the legacy section 12
    Then GET /admin/agent-runs takes query agent, from and to and answers AgentRun[] with 200, 401, 403 and 503 under Platform administration R with scope applied
    Then GET /admin/agent-configs, POST /admin/agent-configs and POST /admin/agent-configs/{versionId}/approve answer AgentConfigVersion with their 201, 409, 422 and 404 cases under Rules and parameters R, C and A
    Then POST /admin/agent-samples, POST /admin/agent-evaluations, GET /admin/agent-evaluations and GET /admin/agent-evaluations/{evaluationId}/report answer AgentSample, AgentEvaluationRun and AgentEvaluationReport with their 201, 202, 404, 409 and 422 cases under Rules and parameters C and R
    Then GET /admin/agent-metrics answers AgentMetric[] for the monitor, GET /cases/{caseId}/agent-outputs answers AgentOutput[] under Case record R, and POST /agent-runs/{runId}/feedback answers AgentOutput under Case record U
    Then every operation is declared once, under the base /api/recovery/agent/v1, one hop per call, with the 2 s client budget of DP-11 on every caller and the 60 s model call inside the run
    Then a request that misses a required member is refused with 422 and MSG-GEN-001 and no operation answers on the legacy monolith base

  Scenario: AC2 The error model keeps the legacy message IDs and statuses (new, D-RCV-60)
    Given the message catalogue of the platform and the legacy messages of RWB-E1-058 section 14
    When every refusal of section 12.1 is reviewed
    Then MSG-P10-001 is answered with 422 for a file that fails a check, MSG-P10-002 with 422 for an empty sample and MSG-P10-003 with 409 for an evaluation already RUNNING
    Then MSG-P7-002 is answered with 409 for a loader who approves their own version, MSG-GEN-004 with 409 for a row that changed and MSG-P4-002 with 403 for a role without the right
    Then MSG-GEN-001 is answered with 422 for an empty required member, and 401 is answered for no session with the platform code
    Then every refusal body carries the status, the code, the detail and the message ID where a business message applies, and no refusal is answered without one of them

  Scenario: AC3 EV-28 and the record payload are declared and no personal field is carried (new, D-RCV-60)
    Given a run of agent "ECHO" for case "RW-2026-000101" that ends ANSWERED
    When the outbox relay publishes it
    Then the message type is rwb.agent.AgentRunCompleted.v1 on rwb.agent.events.v1, keyed by the case ID, and it is validated against its registry subject with BACKWARD compatibility before the relay
    Then the envelope carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype, with the run ID as its subject
    Then the payload carries run ID, agent_code, agent_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms and run_at, and the status is one of LOV-AGENT-RUN
    Then a payload that fails its subject, or a name outside the family rwb.agent.<Event>.v1, is refused before the relay and routed to the .dlt topic with an alert
    Then the decision-record payload on rwb.decision-record.v1 carries the record reference, the decision code, the agent version, the model version, the inputs reference, the final call and the actions, is written by the local library in the transaction of the calling step, and names the run ID of the agent
    Then no account number, no name and no personal field appears in either payload or in the inputs reference

  Scenario: AC4 The schema rwb_agent and the eight agent tables are declared with their keys (new, D-RCV-60)
    Given the schema file of section 12.7 and the field list of TSD P10 v2 T3.1
    When the eight tables and their keys are reviewed
    Then agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run, agent_evaluation, agent_feedback and agent_alert are owned by P10 in schema rwb_agent and no other table of the schema holds agent data
    Then the primary key of each is id, and the unique keys are (agent_code, policy_version), (agent_code, prompt_version), (idempotency_key), the sample key of this document and the partial unique index of agent_evaluation_run on (agent_code, sample_code, sample_version) where status = 'RUNNING'
    Then agent_run holds the status, the fallback, the guardrail result, the confidence, the latency, the tokens, the cost and the three versions that EV-28 and the listing publish
    Then every cross-service reference of the schema is an ID only, no foreign key crosses a schema, and the boundary scan blocks a migration that adds one

  Scenario: AC5 The boundary contracts and the fakes are declared (new, D-RCV-60)
    Given the consumed contracts of rwb-case, rwb-document, rwb-access and rwb-decision
    When the boundary contract and the fakes of section 12.8 are reviewed
    Then the INT-23 request carries the model code, the masked inputs and the output schema reference and nothing else, and the call is bounded by timeout_seconds of the policy in force
    Then a timeout writes TIMED_OUT, a 4xx or a 5xx writes MODEL_ERROR and a failed schema writes GUARDRAIL_FAILED with check code SCHEMA, each with fallback true
    Then the rwb-case fake answers the case read, the parameter read, the reference-data read and the list read, the rwb-document fake answers the document read, and the rwb-access fake answers the authorise call, the masking policy and the session read
    Then the rwb-decision fake answers the record read-back, and the route stub, the model-gateway fake, the decision-record stub and the outbox stub answer the paths and payloads this document declares
    Then every fixture is synthetic and no fake holds a production account, document, prompt or model answer

  Scenario: AC6 The nine sub-tables are complete and every fake matches them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables and the fakes are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then every consumed operation of 12.2 names its owner service, its right and its 2 s budget, and every published event of 12.3 names its topic, its key and its registry subject
    Then a drift between a fake and this document fails the contract test, and the test runs in the pipeline before any app, infrastructure or deployment build of this key

  Scenario: AC7 The decision record is written by the deciding step and never by an agent run (new, D-RCV-60)
    Given the decision-record payload of section 12.3 and the local decision-record library of the platform
    When the writers of the decision record are reviewed against BR8
    Then the decision-record type and the central ledger are owned by rwb-decision
    Then the record is written through the local library by the step that took the decision
    Then no agent run writes a decision record
```

**Target reading.** The operation set, the rights, the status codes and the message texts are those of TSD P10 v2 T-A.1 and T-A.2 and of the legacy section 12 and 14, copied rather than invented; the table names, the field list and the lists of values are those of TSD P10 v2 T3.1 and T3.2; the keys are those of the legacy section 13; the event is EV-28 of Arch v5 slide 43 with the payload members of `agent_run`; and the boundary is the INT-23 request of the legacy section 12 with the policy timeout of the approved version. Where a source is silent, this document names the element and writes the §R9 placeholder with its gap and assumption rather than a value.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One base per service: every operation of this key is declared on `/api/recovery/agent/v1` and no operation is declared on the legacy monolith base or on another service's base | DP-13; §R4; Arch v5 slide 41 |
| BR2 | One topic per service with a retry topic and a `.dlt` topic, one event name pattern `rwb.agent.<Event>.v1`, and the topic and the event names of this key are rwb-agent's alone | DP-09; DP-14; §R4 |
| BR3 | Every message is a CloudEvents 1.0 message keyed by the case ID, validated against its registry subject with BACKWARD compatibility before the relay, and routed to `.dlt` on failure | DP-09; Arch v5 slide 42 |
| BR4 | EV-28 carries run facts only: the payload is the `agent_run` fields this document names, with no account number, no name and no personal field | Arch v5 slides 42 and 43; Template and Rules §R7.2 s17 |
| BR5 | The schema is `rwb_agent`, the eight agent tables are P10's, the primary key is `id` in each, and no foreign key crosses a schema | DP-01; Arch v5 slide 41; legacy section 13 |
| BR6 | A run status is always one of LOV-AGENT-RUN, and a timeout, an error and a schema failure map to TIMED_OUT, MODEL_ERROR and GUARDRAIL_FAILED and never to an invented value | TSD P10 v2 T3.2; legacy section 5 |
| BR7 | No business value in the contract: the model code and version, the timeout, the floor, the tool list, the price and the list values are rows of the policy version and of the owner contracts, and the contract only names them | Template and Rules §R7.2 s17; legacy BR11 |
| BR8 | The decision-record type and the central ledger are rwb-decision's, and the record itself is written by the step that took the decision through the local library; no agent run writes one | DP-03; ADR-022; legacy section 19 |
| BR9 | The two admin reads of this key, the metrics read and the case-output read are declared once and read by their consumers; a consumer never redefines a shape it does not own | DP-13; TSD P10 v2 T-A.1 |
| BR10 | Every payload and every fixture is synthetic: no production account, document, prompt, model answer or record is copied into a schema, a payload or a fake | Template and Rules §R7.2 s17 |
| BR11 | The tool gateway is read-only for the whole of wave 1 and wave 2; the allowed tool list of the policy version is an allow list that can only narrow what a run may read. A write tool is an open question and not a requirement of this contract | Arch v5 slides 16 and 35; FSD P10 v3 A2.2 and A2.6.3.2; GAP-1528 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operations, the schema, the payloads, the boundary contract and the fakes are described | In review |
| In review | Consumer sign-off | The app, infrastructure and deployment stories of this key and its calling services accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a query parameter, a payload field or an operation is added without removing one | Baselined |
| Baselined | Breaking change | A member, a status, a key or a payload field is removed, renamed or retyped | In review, with the owner of the affected contract |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | An owner publishes a new version of a consumed contract | rwb-case, rwb-document, rwb-access or rwb-decision changes a shape | In review, aligned to the owner |

These are the states of this document, not of a case or a run. The run states themselves are those of LOV-AGENT-RUN and belong to RWB-P10-E1058-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the operations, the schema, the two payloads, the boundary contract, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to an operation, a key or a payload, and the recorded exception of the 60 second boundary budget |
| The rwb-case, rwb-document and rwb-access owners | Own the consumed operations and sign off the shapes taken from their documents |
| The rwb-decision owner | Owns the record shape, the shared topic and the ledger, and signs off the record mapping |
| The rwb-agent app, infrastructure and deployment stories | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule, the decision-record library, the outbox library and the guard library this document reuses |
| Data steward | Confirms that no personal data field is declared in a payload, a boundary request or a fixture |

The identity that calls INT-23 is the rwb-agent service identity (DP-02); its name, the Key Vault entries it uses and the certificate it presents are Not specified in the source documents (GAP-0606, GAP-0608; ASM-0848, ASM-0854) and are fixed by RWB-P10-E1058-INF.

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Provided operations | the eleven operations of 12.1: run listing, config listing, config load, config approve, sample load, evaluation start, evaluation listing, evaluation report, metrics read, case-output read, run feedback | Not specified in the source documents (DOR-RWB-P10-E1058-CON-7) |
| Request shapes | the query of a listing; the multipart body of a load (file, kind, agent, validFrom) and of a sample (file, agent, sampleCode); AgentEvaluationRequest with agent, sampleCode, sampleVersion and approaches; AgentFeedbackRequest; path identifiers as uuid | Not specified in the source documents (DOR-RWB-P10-E1058-CON-7) |
| Answer shapes | AgentRun[] (id, agent, agentVersion, caseId, outcome, fallback, latencyMs), AgentConfigVersion[] (versionId, agent, kind, version, status, validFrom, validTo, loadedBy, approvedBy, bodyHash), AgentSample, AgentEvaluationRun with its AgentEvaluation score rows, AgentEvaluationReport, AgentMetric[], AgentOutput[] | Not specified in the source documents (DOR-RWB-P10-E1058-CON-7) |
| Refusal | the platform problem response: status, code, detail, the message ID where a business message applies | Not specified in the source documents (DOR-RWB-P10-E1058-CON-7) |
| EV-28 payload | agent, caseid, fallback, outcome, runid | Not specified in the source documents (DOR-RWB-P10-E1058-CON-7) |
| Record payload | record reference, decision code, agent version, model version, inputs reference, final call, actions {caseId, agentRunId} | Not specified in the source documents (DOR-RWB-P10-E1058-CON-7) |
| Boundary request | model code, masked inputs, output schema reference, timeout; the boundary answer is the answer of the model owner checked against that schema | Not specified in the source documents (DOR-RWB-P10-E1058-CON-7) |
| Table keys | primary key `id` on each of the eight tables; unique (agent_code, policy_version), (agent_code, prompt_version), (idempotency_key), the sample key, and the partial unique index of agent_evaluation_run on (agent_code, sample_code, sample_version) where status = 'RUNNING' | Not specified in the source documents (DOR-RWB-P10-E1058-CON-7) |

The sample key of this document is (agent_code, sample_code, sample_version, subject_id, label_key), taken from the legacy section 13; the physical schema of today states (sample_code, sample_version, label_key) and the difference is carried as GAP-0606 and settled in ASM-0858. The member types of AgentEvaluationReport and AgentMetric[] beyond the members named here, the type and length of the inputs reference, and the boundary answer shape are Not specified in the source documents (GAP-0607; ASM-0849, ASM-0850); this document fixes the element names and leaves the types to the review with their owners. AgentEvaluationRequest may be extended, backward-compatibly, by a pair of version labels for a champion and challenger comparison (RWB-E8-003); the two field names and the proposal shape are agreed with this contract at the contract freeze and are Not specified in the source documents (GAP-0645). `agent_run_daily`, named by FSD P10 v3 A2.6, is not in the Ownership Map, the logical model, the physical schema or Data Classification v5 and is out of this baseline (ASM-0859).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10). Every path below is relative to that base. The exact path names are carried by this service contract, the API Specification v4 and the Ownership Map; the paths named in FSD P10 v3 stay the behavioural reference. The names `/agent-policies` and `GET /agent-runs/{id}` of Arch v5 slide 16 are not among the eleven operations of this contract.

| Method | Path | Purpose | Rights | Idempotency |
|---|---|---|---|---|
| GET | `/admin/agent-runs` | List agent runs with fallbacks: query agent, from, to; 200 AgentRun[] | Platform administration R, scope applied | Read only; writes nothing |
| GET | `/admin/agent-configs` | List prompt and policy versions per agent: query agent, kind, status; 200 AgentConfigVersion[] | Rules and parameters R | Read only; writes nothing |
| POST | `/admin/agent-configs` | Load a new prompt or policy version from a checked file; 201 AgentConfigVersion in status LOADED | Rules and parameters C | Idempotency-Key header; a repeat returns the stored response |
| POST | `/admin/agent-configs/{versionId}/approve` | Approve a loaded version with If-Match on the row version; 200 AgentConfigVersion in status APPROVED | Rules and parameters A | Idempotency-Key header; a repeat returns the stored response |
| POST | `/admin/agent-samples` | Load a labeled evaluation sample; 201 AgentSample with the sample version and the row count | Rules and parameters C | Idempotency-Key header; a repeat returns the stored response. A new load creates the next sample version |
| POST | `/admin/agent-evaluations` | Start the evaluation harness for an agent on a labeled sample; 202 AgentEvaluationRun in status RUNNING | Rules and parameters C | Idempotency-Key header; a repeat returns the stored response. One RUNNING evaluation per agent, sample and sample version |
| GET | `/admin/agent-evaluations` | List evaluation runs with their score rows; query agent, from, to; 200 AgentEvaluationRun[] | Rules and parameters R | Read only; writes nothing |
| GET | `/admin/agent-evaluations/{evaluationId}/report` | Read the report of one evaluation run; 200 AgentEvaluationReport | Rules and parameters R | Read only; writes nothing |
| GET | `/admin/agent-metrics` | Read agent measures per agent, version, segment and day for the monitor; query agent, segment, version, from, to; 200 AgentMetric[] | Rules and parameters R | Read only; writes nothing |
| GET | `/cases/{caseId}/agent-outputs` | Read the recorded agent outputs of a case; 200 AgentOutput[] | Case record R, scope applied | Read only; writes nothing |
| POST | `/agent-runs/{runId}/feedback` | Record a person's verdict on an item of an L1 agent output; 200 AgentOutput | Case record U, scope applied | Idempotency-Key header; a repeat returns the stored response |

Errors: 401 no session, 403 a role without the right (MSG-P4-002), 404 an unknown version, evaluation, run or case, 409 a version number that exists, an approver who is the loader (MSG-P7-002), a version not in LOADED, a row changed since it was read (MSG-GEN-004), an evaluation already RUNNING (MSG-P10-003) or a feedback already recorded, 422 a file that fails a check (MSG-P10-001), an empty sample (MSG-P10-002) or a missing required member (MSG-GEN-001), 503 the store or a consumed contract unavailable. The 401, 404 and 503 answers carry the platform code and no message ID, because the Error and Message Standard v4 gives none that fits; MSG-GEN-006 is not used, since its text says the request is queued and will be retried (CG-ALL-2516). Idempotency: every POST carries an Idempotency-Key header; the sample load creates the next sample version; one RUNNING evaluation is allowed per agent, sample and sample version; the feedback operation is idempotent on its key; the reads write nothing.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts the tool gateway returns as SY-AGENT; one hop, 2 s |
| GET | `/api/recovery/case/v1/parameters/{key}` | P3 rwb-case | The parameter keys a run reads, with the version in force (DP-06) |
| GET | `/api/recovery/case/v1/reference-data/{lovCode}` | P3 rwb-case | LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS, LOV-SUBJECT-TYPE and LOV-FEEDBACK with their version (DP-07) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The document and its extracted fields, read as SY-AGENT by the document tool |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right, the scope and the masking decision of the caller, through the guard library (DP-08) |
| GET | `/api/recovery/access/v1/masking-policies` | P4 rwb-access | The masking policy in force for the agent identity, read once per run (DP-08) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The session and rights of a caller, for the session answer of 12.1 |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The sealed record of a step, read back to prove the record reference of EV-28 and of the record event |

Every operation is one hop with the 2 s client budget (DP-11, ADR-020). The call to INT-23 is external and is declared in 12.8 and 12.9, not here. The paths of the parameter, reference-data and session reads are the owner's and are fixed by their own contract documents; a drift is corrected there and never here.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | agent, caseid, fallback, outcome, runid |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | record reference, decision code, agent version, model version, inputs reference, final call, actions {caseId, agentRunId} |

Both are CloudEvents 1.0 messages inserted in the outbox in the same transaction as the row they describe and relayed by the outbox library; a payload is validated against its registry subject before the relay (DP-09; BR3). The family name pattern is `rwb.agent.<Event>.v1`: EV-28 is the only member the sources name, and a run-started or run-failed member is a new version of this contract agreed with its consumers, never an invented name (ASM-0849). The consumers of EV-28 are rwb-decision, rwb-document and rwb-deviation (Arch v5 slide 43); the consumers of the record event are rwb-decision's ledger and rwb-reporting.

Data Classification v5 classes a field named `outcome` as Customer data, Confidential, on the deviation, treatment, hearing and decision_log_entry entities. Wherever an `outcome` member is carried in these payloads, its handling rule applies: a business fact only (a code, an amount or a date), never beside a direct identifier; in logs, a code or an id only, never the customer value.

#### 12.4 Events consumed

None in this contract. The service consumes no topic for this key: CaseCreated and DocumentStored are the intake and screening consumers and are declared by RWB-P10-E1059-CON and RWB-P10-E1062-CON. The inbox of the outbox library is installed with the schema of 12.7 and dedupes on the event ID where a consumer is added.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (Arch v5 slide 16) | `rwb-agent` | Input: agent code, case ID, subject ID, trigger event, idempotency key, inputs. One execution per idempotency key, with the policy timeout of up to 60 seconds and then the rule result. Started as a child by a stage workflow on DocumentStored (classification) or CaseCreated (screening) for the route agent or the pricing agent. Workflow ID form and duplicate-start policy: Not specified in the source documents (CG-ALL-2519) |
| ResolveAgentConfig | Activity | `rwb-agent` | Output: the approved policy and prompt versions in force on the run date and the parameter and list values read through the owner contracts |
| GatherInputs | Activity | `rwb-agent` | Output: the tool results of the allow-list, read through the owner contracts as the agent identity |
| MaskInputs | Activity | `rwb-agent` | Output: the masked inputs and the masking decision; no personal value leaves the activity |
| CallModelGateway | Activity | `rwb-agent` | Input: model code, masked inputs, output schema reference, timeout. Output: the answer or the mapped status TIMED_OUT, MODEL_ERROR |
| CheckGuardrail | Activity | `rwb-agent` | Input: the answer and its schema reference. Output: the check codes SCHEMA, TOOL_NOT_ALLOWED and BELOW_FLOOR, or a clean answer |
| RecordAgentRun | Activity (workflow kit) | `rwb-agent` | Input: the run row and the outbox row; one transaction, no partial write |

The workflow name, the queue and the 60 second budget are those of Arch v5 slide 16 and the workflow kit of the Temporal and Drools design ("Agent run with rule fallback", slide 12); the activity names and their inputs and outputs are this document's and are accepted by RWB-P10-E1058-APP. A calling step submits through the agent runtime client of RWB-P10-TE013-CON and never starts the workflow itself (DP-20).

#### 12.6 Schedules

None. No Temporal Schedule belongs to this key: the Arch v5 job map names no job for the agent platform (slide 44), a run is started by a calling step and an evaluation by RW-COE through `POST /admin/agent-evaluations`. No quota, retention job or Schedule is invented here.

#### 12.7 Tables owned

| Table | Owner | Key and contracted use |
|---|---|---|
| agent_policy | P10 (rwb_agent) | Primary key `id`; unique (agent_code, policy_version). A version of an agent's policy: model code and version, output schema reference, allowed tools, autonomy mode, segment, confidence floor, timeout, daily cap, price, alert role, review date, status and validity |
| agent_prompt | P10 (rwb_agent) | Primary key `id`; unique (agent_code, prompt_version). A version of an agent's prompt text with its hash, status and validity; the body is never returned by a read |
| agent_run | P10 (rwb_agent) | Primary key `id`; unique (idempotency_key). One call of an agent with agent_version, prompt_version, model_version, case_id, subject_id, autonomy_mode, trigger_event, status, fallback, guardrail_result, output, confidence, latency_ms, tokens_in, tokens_out, cost_thb, data_as_of, run_at, evaluation_run_id and decision_log_id; index on (agent_code, run_at) |
| agent_sample | P10 (rwb_agent) | Primary key `id`; unique (agent_code, sample_code, sample_version, subject_id, label_key). One labeled subject in a versioned evaluation sample |
| agent_evaluation_run | P10 (rwb_agent) | Primary key `id`; partial unique index on (agent_code, sample_code, sample_version) where status = 'RUNNING'. One evaluation of an agent version against a sample, with its versions, status, timestamps, cost, p95 latency and failure counts |
| agent_evaluation | P10 (rwb_agent) | Primary key `id`; evaluation_run_id. The score of one approach on one label key: sample size, TP, FP, FN, agreement, precision and recall |
| agent_feedback | P10 (rwb_agent) | Primary key `id`; agent_run_id. A person's verdict on an item of a run, with its reason and its record reference |
| agent_alert | P10 (rwb_agent) | Primary key `id`; agent_code, alert_type and business_date. A cost-cap or drift alert of an agent with its measured and threshold values and its recipient role |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | The outbox, inbox and idempotency envelope of the service (DP-09) |

The eight agent tables are created in `rwb_agent` by the rwb-agent Flyway sequence; agent_feedback and agent_alert are created by the stories that own their behaviour (RWB-P10-E2032-APP and RWB-P10-E1063-APP) and are declared here because every build of the key needs their shape. `decision_log_entry` is a rwb-decision table and is reached only through its contract (DP-01, DP-03). No foreign key crosses a schema; `case_id`, `subject_id`, `evaluation_run_id` and `decision_log_id` are cross-service references by ID only. The migration takes the next number of the service's own Flyway sequence, in the form V0001 to Vnnnn (Service Template Specification v1 §3.1); the number itself is Not specified in the source documents (CG-ALL-2529), and the legacy file name `V10_001__agent_runtime.sql` is not used (ASM-0856).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock | The case facts of RW-2026-000101, RW-2026-000102 and RW-2026-000103; the parameter keys of the policy in force; LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS, LOV-SUBJECT-TYPE and LOV-FEEDBACK with their versions; a list version that lacks a value the run uses; a case that does not exist; an answer beyond 2 s | Contract tests, app story |
| rwb-document WireMock | A document with its extracted fields and their confidence; a document that does not exist; an answer beyond 2 s | Contract tests, app story |
| rwb-access WireMock | `POST /authorise` granting Rules and parameters C to RW-COE, A to RW-RISK, Platform administration R to RW-PLATADM and Case record R and U to their holders, refusing a role without the right, and returning the masking decision; `GET /masking-policies` with the masking policy of the agent identity; `GET /me/session` with the rights of the caller | Contract tests, app and deployment stories |
| rwb-decision WireMock | The sealed record of a step with its record reference and its decision code; a record that is not found | Contract tests, app story |
| gateway-bff route stub | A pass-through route in front of the eleven operations, one hop, with the media types preserved; a route that refuses an unknown path | Contract tests, deployment story |
| Model gateway fake (INT-23) | An answer of 1,200 ms with 900 input and 150 output tokens; an answer with field "summary" missing; an answer with confidence 0.79; silence for 61 seconds; a 4xx and a 5xx | Contract tests, app and infrastructure stories |
| Decision-record library stub | One record written in the same transaction as its outbox row, with a record reference returned to the caller | Contract tests, app story |
| Outbox and inbox stub | The relay of a valid message, the refusal of a payload that fails its subject, and the `.dlt` route | Contract tests, app and infrastructure stories |

Every fixture is synthetic. The model gateway fake is the only stand-in for an external system: no test calls a live model endpoint with real prompts, and no fixture holds a production account, document, prompt, model answer or record.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 11 provided, 8 consumed | The eleven operations of 12.1 on `/api/recovery/agent/v1`; the case, parameter, reference-data, document, authorise, masking-policy, session and record read-back operations of 12.2; one hop, 2 s each; the INT-23 call is HTTPS at the boundary with the policy timeout of up to 60 seconds |
| Kafka | 2 published, 0 consumed | EV-28 on `rwb.agent.events.v1` with its retry topic and its `.dlt` topic, and the record event on `rwb.decision-record.v1`; both through the outbox, both CloudEvents 1.0 |
| Temporal | 1 workflow, 6 activities | AgentRunWorkflow and ResolveAgentConfig, GatherInputs, MaskInputs, CallModelGateway, CheckGuardrail and RecordAgentRun on queue `rwb-agent` in namespace `rwb-recovery` |
| File | None | The policy, prompt and sample files arrive in the multipart body of a load operation; no file path, bucket or container is named, because the policy, the prompt and the sample are rows of `rwb_agent` |

### 13. Solution plan

**Deliverables.** `contract/agent-operations.yaml` (the eleven operations, their queries, requests, answers, rights, refusals and idempotency), `contract/agent-schema.sql` and `contract/agent-schema.md` (the eight tables, their columns and keys, and the library objects they rely on), `contract/agent-run-completed.asyncapi.yaml` (EV-28 on `rwb.agent.events.v1` with its registry subject and its `.dlt` route), `contract/agent-decision-record.md` (the record payload and the rule that the calling step writes it), `contract/model-gateway-boundary.yaml` (the INT-23 request, the schema reference and the status mapping) and the eight WireMock mappings with their synthetic fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON for the app story; the payload and topic are declared here |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON and C RWB-P3-E1042-CON for the app story; the paths are restated here |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON for the app story; the lists are restated here |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON and C RWB-P4-E1037-CON for the app story; the rights are declared here |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story; the topic, the envelope and the subject are declared here |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none here; the budget is declared for every operation |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story; the keys are declared here |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story; the route stub is declared here |
| DP-20 | Agent client | rwb-agent contract | H RWB-P10-TE013-CON for the app story; the workflow and the run result are declared here |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts and RWB-P10-TE013-CON are the build dependencies its consumers add, and no C or I dependency is claimed. DP-11 is the pattern of every operation and of the eight consumed reads; the model boundary keeps the policy timeout of up to 60 seconds as the recorded exception to the 2 s budget, and no other hop is allowed to inherit it (ASM-0850).

**Build steps**

1. Write the operation contract from TSD P10 v2 T-A.1 and T-A.2 and the legacy section 12, with the rights, the status codes, the message IDs and the idempotency of each; add a lint to the pipeline (AC1, AC2).
2. Write the schema file with the eight tables, their columns from TSD P10 v2 T3.1 and their keys from the legacy section 13, and the boundary note on cross-service references (AC4).
3. Write the EV-28 AsyncAPI document: the envelope, the key, the payload members, the registry subject and the `.dlt` route (AC3).
4. Write the record payload and the rule that the calling step writes it through the library in its own transaction (AC3).
5. Write the boundary contract: the request, the schema reference, the policy timeout and the mapping to LOV-AGENT-RUN (AC5).
6. Build the eight fakes and their synthetic fixtures, including the 61 second silence and the payload that fails its subject (AC5, AC6).
7. Add the six contract tests of section 16, including the drift test between each fake and this document (AC6).
8. Tag the baseline and collect the sign-off of the app, infrastructure and deployment stories of this key and of the calling services.

**Done when.** The six contract artefacts validate in the pipeline, the six contract tests pass, the eight fakes answer every consumed path and payload, the nine sub-tables are complete with `None` where empty, and the app, infrastructure and deployment stories of this key and its calling services have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | A prompt, policy or sample file fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | Evaluation started on a sample with no labeled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Evaluation started while the same one is running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P7-002 | Loader tries to approve their own version | You prepared this decision, so you cannot approve it. |
| MSG-GEN-004 | Approval of a version that changed since it was read | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required member of a request is empty | Enter {field}. |

The seven texts are the legacy messages of RWB-E1-058 and MSG-GEN-001 of the platform, copied character for character; this contract adds no message ID. Thai text for each message follows decision DL10. In MSG-P4-002 the {action} value is the operation the caller attempted, for example "read the agent runs", "load a configuration" or "record feedback".

### 15. Screens and states

None in this story. The contract serves the admin reads that the agent monitor screen SCR-46 (no access: refused with MSG-P4-002; empty, loading and error: Not specified in the source documents (DOR-RWB-P10-E1058-CON-10)) of RWB-E2-031 and RWB-P10-E1063-APP will compose, the case-output read of the Epic 3 case record, and the future feedback area of a case; it fixes no screen field, no order and no masking rule. The admin reads are reached through the gateway-bff route (DP-19), and the exact route name and path are Not specified in the source documents (GAP-0607; ASM-0857). Screen Specifications v1 gives SCR-46 the states Shadow, live and paused, with access by Platform administration checked on every request; it describes no empty, loading or error state (CG-ALL-2530).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E1058-CON-01 | AC1, BR1, BR9 | Contract | The eleven operations validated against their schema: the query and body members of each, a request missing each required member, the four reads and the five refusal codes |
| TC-P10-E1058-CON-02 | AC2, BR6, BR7 | Contract | One case per message ID: MSG-P10-001 with 422, MSG-P10-002 with 422, MSG-P10-003 with 409, MSG-P7-002 with 409, MSG-GEN-004 with 409, MSG-P4-002 with 403 and MSG-GEN-001 with 422 |
| TC-P10-E1058-CON-03 | AC3, BR2, BR3, BR4 | Contract | EV-28 for a run of "ECHO" on case RW-2026-000101: the envelope, the key, the payload members, a status outside LOV-AGENT-RUN, a name outside the family, a payload that fails its subject and the `.dlt` route |
| TC-P10-E1058-CON-04 | AC4, BR5 | Contract | The eight tables and their columns and keys against the schema file; the partial unique index of agent_evaluation_run; a migration that adds a cross-schema foreign key |
| TC-P10-E1058-CON-05 | AC5, BR8, BR11 | Contract | The boundary request and the six model-gateway answers, reached only through ModelGatewayClient with a deterministic stub and the masked inputs asserted on the captured model request; the rwb-case, rwb-document, rwb-access and rwb-decision fakes; the record payload of a step with its record reference; no agent run writes a record; no prompt text or model answer in any response or log; the tool gateway offers reads only and the allowed tool list of the policy version only narrows them |
| TC-P10-E1058-CON-06 | AC6, BR10 | Contract | The nine sub-tables complete with None where empty, the eight fakes answering every consumed path, and the drift test between each fake and this document |
| TC-P10-E1058-CON-07 | AC4, BR5 | Contract | Boundary of each of the eight tables of 12.7 against its keys: a second row with the same primary key, a second row with the same unique key of the table, and a row with its key column absent |
| TC-P10-E1058-CON-08 | AC7, BR8 | Contract | A step that takes a decision writes its record through the local decision-record library; an agent run writes no record; the decision-record type and the central ledger are declared as rwb-decision's |

### 17. Guardrails

- No business value in the contract: the model code and version, the timeout, the floor, the tool list, the price and the list values stay rows of the policy version and of the owner contracts, and the contract only names them (BR7).
- No personal data in a payload, an example or a fixture: identifiers and facts only, the inputs reference holds the masked snapshot, and every fixture is synthetic (BR4, BR10).
- The contract names the agent base, the agent topic and the agent queue as rwb-agent's and consumes every other operation and topic; a document that declares another service's path or topic as provided fails the review (BR1, BR2).
- The eight agent tables are P10's and no foreign key crosses a schema; the record table of rwb-decision is read only through its contract (BR5, BR8).
- Every payload is validated against its registry subject before the relay and a refusal is routed to `.dlt` and alerted (BR3).
- The model boundary carries the model code, the masked inputs and the schema reference only; nothing else of the case leaves the service (BR6).
- The two admin reads, the metrics read, the case-output read and the feedback operation are declared once and never redefined by a consumer (BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-010 | Agents run under service identities and the same role checks as people | The rights of the eleven operations, the session read, the agent identity at the boundary, MSG-P4-002 | TC-P10-E1058-CON-01, TC-P10-E1058-CON-02 |
| REQ-ACA-005 | Personal data masked by role in every agent call | The masking decision and the masking policy of rwb-access, the masked inputs of the boundary request, the no-personal-field rule of EV-28 and of the record | TC-P10-E1058-CON-03, TC-P10-E1058-CON-05 |
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | The policy and prompt version resource, the parameter and list reads, the check limits of the versioned schema | TC-P10-E1058-CON-01, TC-P10-E1058-CON-05 |
| D-RCV-60 DP-01 | One schema per service and no cross-service table read | The schema `rwb_agent`, the eight tables, the ID-only references and the boundary scan | TC-P10-E1058-CON-04, TC-P10-E1058-CON-07 |
| D-RCV-60 DP-03 | Local decision record plus central ledger | The record payload, the local library and `rwb.decision-record.v1` | TC-P10-E1058-CON-03, TC-P10-E1058-CON-05, TC-P10-E1058-CON-08 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | EV-28, its envelope, its registry subject, its retry topic and its `.dlt` topic | TC-P10-E1058-CON-03, TC-P10-E1058-CON-06 |
| D-RCV-60 DP-13 | One REST base per service | `/api/recovery/agent/v1` for the eleven operations and no operation on another base | TC-P10-E1058-CON-01 |
| D-RCV-60 DP-15 | Per-service Flyway and migration ownership | The keys and the creation of the eight tables in the service's own sequence | TC-P10-E1058-CON-04 |
| ASM-0849 | EV-28 is the only member the sources name and the payload is taken from the `agent_run` fields | The event of 12.3 and the registry subject of 12.8 | TC-P10-E1058-CON-03 |
| ASM-0850 | The in-process orchestrator becomes the run contract behind the agent runtime client, and the boundary keeps the policy timeout | The workflow of 12.5 and the boundary of 12.8 | TC-P10-E1058-CON-05 |
| ASM-0858 | The sample key keeps the legacy columns and is reconciled with the physical schema at build | The keys of 12.7 and the note of section 11 | TC-P10-E1058-CON-04 |

### 19. Out of scope

- The implementation of the operations, the gateway client, the store, the guardrail, the harness and the workflow (RWB-P10-E1058-APP).
- The network path to INT-23, the login, the Key Vault entries, the topic with its retry and `.dlt` topics, the queue, the sizing, the budgets and the pipeline gates (RWB-P10-E1058-INF).
- The chart, the pipeline, the migration job, the configuration and secrets injection, the probes, the dashboards, the alerts and the runbook (RWB-P10-E1058-OPS).
- The central decision ledger, its sealing and its read, and the record shape of rwb-decision.
- The case, the parameters, the reference data, the document, the right and the masking policy, which are their owners'.
- The four other agent keys of the service (RWB-P10-E1059, E1060, E1062 and E1063) and the TDR offer-suggestion key of Epic 2, whose payloads are declared where their behaviour is built.
- The member types of AgentEvaluationReport and AgentMetric[] beyond the elements named here, the type of the inputs reference, the INT-23 host and certificate, the route name in front of the admin reads and the `agent_run_daily` table named by FSD P10 v3, which are Not specified in the source documents (GAP-0607, GAP-0608; ASM-0849, ASM-0850, ASM-0854, ASM-0857, ASM-0859).
- Open decision DL10 is still open; this document proceeds on its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 until DL10 is closed.
- The model endpoint path, the masking route and the agent run evidence of the target are Not specified in the source documents (GAP-0368); the boundary is proved through ModelGatewayClient with a deterministic stub and the P10 admin and run contracts, and every legacy value, status and message is kept unchanged.
