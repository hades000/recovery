# RWB-P10-E1059-CON Case intake agent in shadow [E1b]

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1059-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Contract version | v1 (path base /api/recovery/agent/v1) |
| Readiness decisions | RD-P1-005, RD-P1-041, RD-P1-062 |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-059 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P10-E1059-CON-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-024, FR-P10-025) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-062: Define the missing data date and fail-closed age handling for never-stamped inputs.
- The consumed freshness read and its fake carry status `LOADED` / `STALE` and the never-stamped answer (RD-P1-005, RD-P1-041). Never-stamped input persists `data_as_of` null.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-059 for rwb-agent. This is the contract slice of the legacy key: the two run operations the intake flow uses on `/api/recovery/agent/v1` - one to start a run and one to read it (DP-11, DP-13, DP-20) - the intake answer shape "intake-summary-v1" with its four gap types and its no-personal-data rule, the `rwb.agent.AgentRunCompleted.v1` payload as a CloudEvents 1.0 message on `rwb.agent.events.v1` with its retry and `.dlt` topics (DP-09), the event-driven interface that replaces the legacy in-process listener and any job-style trigger, the rwb-source-data read contract the intake inputs are built from (DP-05), the cases, parameters and lists read from rwb-case (DP-06, DP-07), and the six fakes every consumer builds against. It does not restate the whole rwb-agent contract, whose baseline is RWB-P10-E1058-CON and RWB-P10-TE013-CON, and it builds no business behaviour. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the intake run fixed as a contract on Day 1: the start operation and the read operation on `/api/recovery/agent/v1` that the intake flow uses, with the run key, the mode and the run status of LOV-AGENT-RUN; the intake answer shape "intake-summary-v1" with its four gap types, the summary of at most 1,500 characters of masked tokens, the gap array and the confidence, and no personal data in it; the `rwb.agent.AgentRunCompleted.v1` payload on `rwb.agent.events.v1` with its retry and `.dlt` topics; the event-driven interface that replaces the in-process listener and any job-style trigger; the rwb-source-data read contract the inputs are built from; and the six fakes**, so that **the app story of this key, the operations story and every story that reads an agent run build against one agreed, testable shape without waiting for the intake agent to be complete**.

### 2. Business rationale

The legacy key RWB-E1-059 was written against a monolith: an `IntakeShadowListener` inside the same module received the case creation event from the same schema, `read_case`, `read_accounts`, `read_documents`, `read_valuations` and `read_contact_points` were in-process query services of the same deployment (these are the legacy service names, not fields or entities of LDM v9 or Data Classification v5: `read_case` has no counterpart there, the nearest entries `red_case_no` and `ace_case` being unrelated - CG-ALL-2562), the ACE facts came from `v_ace_*` views of the same database, the answer was validated against a schema file beside the code, and the run completion was an application event written by the same transaction. In the target every one of those is a boundary. The in-process call becomes one REST operation under `/api/recovery/agent/v1` with one hop and a client budget (DP-11, DP-13; ADR-020); the case, its parties and its accounts are read through the rwb-case contracts (DP-06, DP-07); the ACE facts are read through rwb-source-data (DP-05); the documents through rwb-document; the run completion becomes EV-28 on the service's own topic (DP-09; Arch v5 slide 43 row 28); and the run is started from the event by the runtime that owns it, not by a listener that shares a schema with the case store (DP-20; Arch v5 slide 16).

Contract-first only works if the seam is written down once. The seam here is small and load-bearing: one operation whose answer carries the run the intake flow needs, one read whose answer in SHADOW carries no content, one answer shape whose three members and four gap types are the legacy ones, one event payload that carries the run facts and no personal data, and one consumed read side whose four tool operations and freshness stamp are named.

If the shape is agreed and faked on Day 1, three teams move at once. RWB-P10-E1059-APP builds the listener, the assembler, the guardrail and the scorer against these fakes; the operations story of the service provisions the topic with its retry and `.dlt` topics, the queue and the indexes against the same names; and RWB-P10-E1061-APP, which reads a run of this agent for its report and its L1 proposal, reads one shape. Without it, each caller invents its own answer, the run key drifts, and the score that decides autonomy level 1 stops matching the run it was computed from.

This story defines the provided side and the consumed side of this key and never restates what another owner holds: the agent runtime baseline is RWB-P10-E1058-CON and RWB-P10-TE013-CON, the case is rwb-case's, the ACE facts are rwb-source-data's, the documents are rwb-document's and the rights are rwb-access's (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the REST base `/api/recovery/agent/v1`, the topic `rwb.agent.events.v1` and the event names `rwb.agent.<Event>.v1` follow the platform rule and not a local choice (§R4; DP-13, DP-14).
- The CloudEvents 1.0 envelope and the platform error envelope are the platform baseline; this document narrows them where it must and says so.
- The agent runtime baseline contract of RWB-P10-E1058-CON is in force: the policy and prompt resources, the admin configuration and run reads, the run resource, the error taxonomy and the evaluation operations are its elements, and this story reuses them rather than redefining them. Its task queue is `rwb-agent` and its namespace `rwb-recovery` (§R4; ASM-0865).
- The agent runtime client contract of RWB-P10-TE013-CON is the consumer of the two operations of this document for every caller inside the platform; this document fixes the members the intake flow reads and leaves the rest to that baseline.
- The outbox and retry library of RWB-PLT-TE006-CON publishes the outbox and inbox envelope, the relay, the retry topics (1 min, 10 min, 1 h) and the `.dlt` rule (DP-09).
- The decision-record library of RWB-PLT-E1027-CON is in force; a shadow run writes no decision record with it (BR7).
- The parameter and reference-data contracts of rwb-case are published by RWB-PLT-E1042-CON and RWB-PLT-E1043-CON with their client libraries (DP-06, DP-07).
- The rwb-source-data tool reads and the freshness read are named by the platform contract and their paths are Not specified in the source documents (GAP-0611; ASM-0866); the P1 fake is written to the assumed shape.
- The document read of RWB-P5-E1053-CON is published with its fake (ASM-0864).
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W1.

### 4. Flow

1. Draft the start operation: its method, its path below the base `/api/recovery/agent/v1`, its request members - agent code "INTAKE", case ID, business date, trigger "CaseCreated", idempotency key `INTAKE:<caseId>:<businessDate>` - its answer, its refusal codes and its one-hop budget (DP-11, DP-13, DP-20).
2. Draft the read operation: its path, its answer, the run facts it returns, the rule that in mode SHADOW the answer carries neither the summary nor the gap flags, and its refusal codes; shadow-run evidence is read through the P10 admin and case output reads only.
3. Fix the intake answer shape "intake-summary-v1": summary at most 1,500 characters of masked tokens only, gaps as an array of gapType from the enum, reason and sourceRef, confidence from 0 to 1, and the rule that no personal field appears in the answer, the run row or the event payload.
4. Declare `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`: the envelope, the key, the payload members of Kafka Catalog v1 row EV-28, the registry subject, the retry topics and the `.dlt` route (DP-09).
5. Fix the event-driven interface: `rwb.case.CaseCreated.v1` on `rwb.case.events.v1`, consumed through the inbox, starts one AgentRunWorkflow on queue `rwb-agent` for the run key, and the document states that no job table, no Quartz entry and no shared schedule table is used (DP-09, DP-20; ASM-0863), and the event and workflow path is proven as set out in ASM-B-ITG-W1-08-E1059-1 to -6.
6. Fix the consumed read side: the four rwb-source-data reads, the freshness stamp from the rwb-source-data freshness read written to data_as_of, the rwb-case reads of the case, the accounts, the parties, the parameters and the lists, the rwb-document read and the rwb-access authorise call, each one hop with 2 s and read through its owner's published operation only (DP-05, DP-06, DP-07, DP-11). Per product the answer carries `status` `LOADED` or `STALE` from the stamp in use (the latest stamp row); a never-stamped product answers `businessDate` null with `status` `STALE` (rwb-source-data.yaml 5.1.0; RD-P1-005, RD-P1-041). When never stamped, store `data_as_of` null, omit `X-Data-As-Of` and show the STALE indicator. A required input-age check fails (RD-P1-062).
7. Write the six contract fakes: rwb-case, rwb-source-data, rwb-document, rwb-access, the model stub of the agent platform and the gateway-bff route stub, each with the answers, the errors and the timings this key's tests need.
8. Publish the nine sub-tables of section 12 and the contract tests: the operation shapes, the answer shape, the event envelope and its registry subject, the event-driven start, the consumed read side and a drift test between each fake and this document.
9. Tag the baseline and hand it to RWB-P10-E1059-APP, RWB-P10-E1061-APP and the test cases of this key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field of the start or the read operation drifts from this document: a renamed member, a retyped business date, a dropped refusal | The contract test fails and the merge is blocked | None | AC1, AC2 |
| X2 | A caller sends a request without the case ID, the business date or the idempotency key | The operation refuses the request with 422 and names the field; nothing is written | MSG-GEN-001 | AC1 |
| X3 | The answer or the event payload gains a personal field | The data-steward review and the contract test refuse the payload; nothing is published | None | AC3, AC4 |
| X4 | A produced payload fails its registry subject, or the relay cannot reach the topic | The message is refused before the relay and routed to the `.dlt` topic of `rwb.agent.events.v1` with an alert | None | AC4 |
| X5 | A member of the run resource or of an admin read drifts from the baselines RWB-P10-E1058-CON and RWB-P10-TE013-CON | The contract test fails on the baseline and this document is aligned, because the baseline is the owner | None | AC2 |
| X6 | A consumed read answers beyond 2 s or refuses | The answer maps to TOOL_UNAVAILABLE with fallback true; no partial input set is used and no invented default is applied | None | AC6 |
| X7 | A field-level detail of a consumed operation, a member of the answer or the path of a consumed read is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC1, AC3, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the agent runtime baselines, the outbox library, the decision-record library and the rwb-case contracts as published |
| Negotiable | The field-level detail of the consumed operations is settled with their owners; the two operation shapes, the answer shape, the event payload and the start interface are fixed by this realignment |
| Valuable | Unblocks the two app stories of this key on Day 1 and gives every reader of an intake run one shape |
| Estimable | Two provided operations, ten consumed reads, one answer shape, one event, one start interface and six fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact - the schema file, the payload, the fake, the contract test - and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Case intake run contract slice for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the agent runtime baseline contracts of RWB-P10-E1058-CON and RWB-P10-TE013-CON are in force
    Given the outbox and decision-record libraries of the platform are in force

  Scenario: AC1 The start operation replaces the in-process listener (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When the intake flow asks for a run of agent "INTAKE" for case "RW-2026-000301" with business date 2026-11-30 and idempotency key "INTAKE:RW-2026-000301:2026-11-30"
    Then one operation answers 202 with the run resource and its run ID, in mode "SHADOW" and a status of LOV-AGENT-RUN
    Then a request without the case ID, the business date or the idempotency key is refused with 422 and MSG-GEN-001 naming the field, and a role without the right is refused with 403 and MSG-P4-002
    Then a repeat with the same key answers 409 with the stored run, and no second run row and no second model call exist (R-UNI-40)
    Then the operation is declared once, below the base /api/recovery/agent/v1, with one hop and the 2 s client budget of DP-11 on every caller, and the model call of up to 60 seconds happens inside the service
    Then the path of the operation is fixed by this document and no source names it (GAP-0611; ASM-0862)

  Scenario: AC2 The read operation carries no shadow content (new, D-RCV-60)
    Given a run of agent "INTAKE" for case "RW-2026-000301" in mode "SHADOW" on business date 2026-11-30
    When GET /api/recovery/agent/v1/agent-runs/{runId} is called
    Then the answer carries the run ID, agent_code "INTAKE", agent_version, prompt_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, latency_ms, tokens_in, tokens_out, cost_thb, data_as_of and run_at
    Then the answer carries neither the summary nor the gap flags in mode "SHADOW", and no other user-facing operation returns them
    Then the operation declares 401, 403, 404 and 503 under Platform administration R with scope applied
    Then the run resource and the admin reads are baselined in RWB-P10-E1058-CON and RWB-P10-TE013-CON, and a drift is corrected there and never here

  Scenario: AC3 The intake answer shape is fixed and carries no personal data (new, D-RCV-60)
    Given the output schema "intake-summary-v1" is in force with the gap types MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT and STALE_INPUT
    When an answer of agent "INTAKE" for case "RW-2026-000301" is validated
    Then the answer carries summary as a string of at most 1,500 characters of masked tokens only, gaps as an array of gapType, reason and sourceRef, and confidence from 0 to 1
    Then the four gap type values are the only values accepted, and a gapType outside the enum, a missing member or a confidence outside 0 to 1 gives status GUARDRAIL_FAILED with check "SCHEMA_RULE"
    Then no account number, no customer name and no personal field appears in the answer, in agent_run.output or in the event payload
    Then the answer shape is versioned with the policy version "P1" and the prompt version "PR1", and the gap type list is data and not a constant of the source

  Scenario: AC4 EV-28 AgentRunCompleted is declared on the agent topic (new, D-RCV-60)
    Given a run of agent "INTAKE" for case "RW-2026-000301" on business date 2026-11-30
    When the run completes and the outbox relay publishes it
    Then the message type is rwb.agent.AgentRunCompleted.v1 on rwb.agent.events.v1 and it is keyed by the case ID
    Then the envelope carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype, with the run ID as its subject
    Then the payload carries run ID, agent_code "INTAKE", agent_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms and run_at, and no other member
    Then the status is one of LOV-AGENT-RUN and no status outside the list is published
    Then a payload that fails the registry subject is refused before the relay and routed to the .dlt topic with an alert, after the retry topics of 1 min, 10 min and 1 h, and no personal data is carried

  Scenario: AC5 The run is started by the event, not by a job (new, D-RCV-60)
    Given a CaseCreated event for case "RW-2026-000301" of 2026-11-30 on rwb.case.events.v1
    When the event is consumed
    Then one AgentRunWorkflow is started on the task queue rwb-agent for the run key "INTAKE:RW-2026-000301:2026-11-30" with trigger_event "CaseCreated", through the agent run template of the workflow kit
    Then the same event ID delivered twice starts no second workflow and no second run, and the repeat is counted (R-UNI-40)
    Then the contract names no Quartz table, no JOB entry and no shared schedule table, and the run key is the only dedupe element
    Then the workflow platform contract is not a build dependency of this document, because the run is started and read through the agent runtime client contract of RWB-P10-TE013-CON (ASM-0863)

  Scenario: AC6 The rwb-source-data read contract it consumes is fixed (new, D-RCV-60)
    Given the tool reads read_accounts, read_valuations and read_contact_points and the freshness read of rwb-source-data, answered by the rwb-source-data WireMock fake of section 12.8
    When the intake input set is built for case "RW-2026-000301"
    Then the contract names the four reads, the SY-AGENT service identity, one hop and the 2 s budget, and the business-date completeness stamp written to data_as_of
    Then only masked values leave rwb-agent towards the model gateway, and the service reads no recovery.v_ace_* view
    Then a read that answers beyond 2 s or refuses maps to TOOL_UNAVAILABLE with fallback true, and no invented default is applied
    Then the paths of the four reads are Not specified in the source documents (GAP-0611; ASM-0866)

  Scenario: AC7 The nine sub-tables are complete and the six fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables and the six fakes are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then the fakes rwb-case, rwb-source-data, rwb-document, rwb-access, the model stub and the gateway-bff route stub answer every consumed path and payload of this document
    Then a drift between a fake and this document fails the contract test, and the six fixtures are synthetic

  Scenario: AC8 The rules BR1, BR2, BR3, BR4, BR5, BR7, BR8 and BR9 each have a criterion or a guardrail test and a test case in section 16 (new, D-RCV-60)
    Given the business rules BR1, BR2, BR3, BR4, BR5, BR7, BR8 and BR9 of section 8
    When the contract trace is reviewed against sections 7 and 16
    Then each rule has a criterion in section 7 or a guardrail test, and a test case row in section 16
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The intake run is one start operation and one read operation under `/api/recovery/agent/v1`; no caller embeds the agent runtime and no in-process listener interface survives | DP-11; DP-13; DP-20; legacy section 12 |
| BR2 | The run key is `INTAKE:<caseId>:<businessDate>`, one run per key, and a repeat returns the stored run with 409 | Legacy section 12; R-UNI-40; AC3, AC6 |
| BR3 | In mode SHADOW the read returns run metadata only: the summary and the gap flags are stored and never returned by a user-facing operation | Legacy section 7 AC1, section 12 and section 15; BR1 of the legacy story; AC2 |
| BR4 | The answer carries summary, gaps and confidence only, with masked tokens in the summary and no personal field anywhere in the answer, the run row or the payload | Legacy section 12; REQ-ACA-005; Template and Rules §R7.2 s17 |
| BR5 | The four gap types are the enum of the output schema version in force, are data and are never a constant of the source | Legacy BR3; agent_policy.output_schema_ref (DF-AGT-006); DP-06 |
| BR6 | Every message is a CloudEvents 1.0 message on `rwb.agent.events.v1`, keyed by the case ID, validated against its registry subject before the relay, retried on the three retry topics and routed to `.dlt` on failure | DP-09; Arch v5 slides 42 and 43 |
| BR7 | A shadow run writes no decision record: the record that proves a decision is written when a person acts on the answer, and this contract promises none | DP-03; legacy BR1; AC2 |
| BR8 | A run status is always one of LOV-AGENT-RUN and an evaluation status one of LOV-EVAL-STATUS; a timeout, an error, a tool failure, a schema failure and a disabled agent map to TIMED_OUT, MODEL_ERROR, TOOL_UNAVAILABLE, GUARDRAIL_FAILED and DISABLED and never to an invented value | TSD P10 v2 T3.2 |
| BR9 | One base and one topic per service: this contract declares `/api/recovery/agent/v1` and `rwb.agent.events.v1` for rwb-agent and never another service's path or topic as its own | DP-13; DP-14; Arch v5 slide 41 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the answer shape, the event payload, the start interface, the consumed read side and the fakes are described | In review |
| In review | Consumer sign-off | The app stories of this key and the test cases accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a query parameter or a payload field is added without removing one | Baselined |
| Baselined | Breaking change to an operation or a payload | A member, a refusal code or an event member is removed, renamed or retyped | In review, with the owner of the affected contract |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | The agent runtime baseline changes the run resource | RWB-P10-E1058-CON or RWB-P10-TE013-CON publishes a new shape | Baselined, aligned to the baseline |

These are the states of this document, not of a case or a run. The run states themselves are those of LOV-AGENT-RUN and belong to RWB-P10-E1059-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the two operations, the answer shape, the event payload, the start interface, the document and the six fakes; tags the baseline |
| Solution architect | Approves a breaking change to an operation, the answer shape or the event, and any change to the 60 second budget |
| The rwb-source-data owner | Owns the tool reads and the freshness read and signs off the shapes taken from its document |
| The rwb-case, rwb-document and rwb-access owners | Own the consumed operations and sign off the shapes taken from their documents |
| The rwb-agent app stories of this key and RWB-P10-E1061-APP | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule, the outbox library and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in the answer, the event or the consumed read |

The identity that starts and reads a run is the rwb-agent service identity (DP-02); its name, the entries it uses and the credentials it presents are Not specified in the source documents (GAP-0610; ASM-0861) and are fixed by the operations story of the service.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Start request | agent code "INTAKE", case ID, business date, trigger "CaseCreated", idempotency key `INTAKE:<caseId>:<businessDate>` |
| Start answer | the run resource: run ID, mode "SHADOW", a status of LOV-AGENT-RUN, the run key |
| Read answer | run ID, agent_code, agent_version, prompt_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, guardrail_result, confidence, latency_ms, tokens_in, tokens_out, cost_thb, data_as_of, run_at; no summary and no gap flags in SHADOW |
| Intake answer | summary (at most 1,500 characters, masked tokens only), gaps (array of gapType, reason, sourceRef), confidence (0 to 1) |
| Refusal | the platform problem response: status, code, detail, the message ID when a business message applies |
| EV-28 payload | run ID, agent_code, agent_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, run_at |
| Consumed read inputs | the case ID and the business date; the answers are the owners' shapes, of which this document names only the members the intake flow reads |

The field-level detail of the start request beyond the five members named above, the type and length of sourceRef, the exact member set of the rwb-source-data tool answers and the paths of the four reads are Not specified in the source documents (GAP-0611; ASM-0862, ASM-0866); this document fixes the element names and leaves the types to the review with their owners. The BR Field ID of each of the seven rows above is Not specified in the source documents (DOR-RWB-P10-E1059-CON-7). `read_case`, `read_accounts`, `read_documents`, `read_valuations` and `read_contact_points` are operation names, not fields or entities of LDM v9 or Data Classification v5 (CG-ALL-2562; DOR-RWB-P10-E1059-CON-7).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/agent-runs` - the path is fixed by this document; no source names it (GAP-0611; ASM-0862) | Start one run of an agent for a case and a business date: request agent "INTAKE", caseId, businessDate, trigger "CaseCreated" and the idempotency key; 202 AgentRun with the run ID and a status of LOV-AGENT-RUN | the service identity of the caller; Rules and parameters C, scope applied | Idempotency-Key header and the run key; a repeat answers 409 with the stored run |
| GET | `/agent-runs/{runId}` | Read one run: the run facts of 12.3 and of the `agent_run` fields; in mode "SHADOW" the answer carries neither the summary nor the gap flags (Arch v5 slides 16 and 41) | Platform administration R, scope applied; the caller's own run always | Not applicable: the call writes nothing |

Errors: 401 no session (Not specified in the source documents (CG-ALL-2571)), 403 no right (MSG-P4-002), 404 no run for the identifier (Not specified in the source documents (CG-ALL-2571)), 409 a repeat of the run key (R-UNI-40) (Not specified in the source documents (CG-ALL-2571)), 422 a missing or malformed request member (MSG-GEN-001), 503 the store or a consumed contract unavailable (Not specified in the source documents (CG-ALL-2571); the business analyst confirms the system-unavailable message of the standard). The full run resource, the admin configuration and run reads and the evaluation operations are baselined in RWB-P10-E1058-CON and RWB-P10-TE013-CON; this document fixes the two operations the intake flow uses and redefines neither (ASM-0865). No operation of this document is served on the legacy monolith base (DP-13).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts the input set is built from, and the proof that the case read returns no agent output |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | P3 rwb-case | The accounts of the case, masked before the model call |
| GET | `/api/recovery/case/v1/cases/{caseId}/parties` | P3 rwb-case | The parties of the case, masked before the model call |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The reference lists the answer is validated against, in force at run time (DP-07) |
| POST | the parameters resolve operation of the rwb-case contract - path Not specified in the source documents (GAP-0611; ASM-0865) | P3 rwb-case | The values of the policy and prompt versions in force (DP-06) |
| POST | the `read_accounts`, `read_valuations` and `read_contact_points` tool reads of rwb-source-data - paths Not specified in the source documents (GAP-0611; ASM-0866) | P1 rwb-source-data | The ACE account facts, the appraisals and the contact points of the case (DP-05) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The last complete business date, written to data_as_of (DP-05). `status` `LOADED` / `STALE`; `businessDate` null with `STALE` when never stamped |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The documents of the case with their type and review status (ASM-0864) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and the scope before a start or a read |

Every operation is one hop with a 2 s client budget (DP-11, ADR-020); the model call to INT-23 is the agent platform's boundary with the policy timeout and is declared in 12.9, not here. This contract declares no contract dependency of its own: it is Day 1, and each consumer adds the contract dependencies of the operations it builds against (§R5.7).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | agent, caseid, fallback, outcome, runid |

One CloudEvents 1.0 message, inserted in the outbox in the same transaction as the run row and relayed by the outbox library; it is validated against its registry subject before the relay, retried on the topics of 1 min, 10 min and 1 h and routed to `rwb.agent.events.v1.dlt` with an alert on failure (DP-09; BR6). No decision record is published for a shadow run (BR7), and no personal data is carried (BR4).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Key | Dedupe |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 | the case ID | Inbox on the event ID, then the run key `INTAKE:<caseId>:<businessDate>` |

This is the event-driven interface that replaces the legacy in-process listener and any job-style trigger: the event starts one AgentRunWorkflow for the run key and nothing else starts an intake run (AC5; BR2).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (Arch v5 slide 16) | `rwb-agent` | Input: agent code "INTAKE", case ID, business date, trigger "CaseCreated", idempotency key. One execution per key, with the 60 second budget and then the run status. Workflow ID: Not specified in the source documents (CG-ALL-2573); duplicate-start policy: Not specified in the source documents (CG-ALL-2573) |
| BuildIntakeInputs | Activity | `rwb-agent` | Output: the masked input set, the inputs reference and data_as_of; no personal field leaves the activity |
| CallModelGateway | Activity | `rwb-agent` | Input: model code, masked inputs, output schema "intake-summary-v1", timeout. Output: the answer or the mapped status TIMED_OUT, MODEL_ERROR, TOOL_UNAVAILABLE |
| CheckGuardrail | Activity | `rwb-agent` | Input: the answer and the output schema reference. Output: the check code and the outcome, SCHEMA_RULE included |
| RecordShadowRun | Activity (workflow kit) | `rwb-agent` | Input: the run row and the outbox row; one `rwb_agent` transaction, no partial write |

The workflow name, the queue and the 60 second budget are those of Arch v5 slide 16; the activity names and their inputs and outputs are this story's and are accepted by RWB-P10-E1059-APP. The workflow is started by the agent runtime contract of RWB-P10-TE013-CON, which is why the workflow platform contract is not a build dependency here (ASM-0863).

#### 12.6 Schedules

None. The intake run is event-started and never on a cadence, and the Arch v5 job map names no job for an agent run (slide 44). No Temporal Schedule is declared, changed or owned by this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_run | P10 (rwb_agent) | The run facts of the read answer and of the EV-28 payload, the stored answer of a run key and data_as_of; no column added |
| agent_policy | P10 (rwb_agent) | The values the contract names: autonomy_mode, confidence_floor, timeout_seconds, allowed_tools, output_schema_ref; no column added |
| agent_prompt | P10 (rwb_agent) | The prompt version a run names; no column added |
| agent_sample, agent_evaluation_run, agent_evaluation | P10 (rwb_agent) | Named only: the sample and the scores the evaluation of this agent reads and writes belong to RWB-P10-E1059-APP |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox, inbox and idempotency envelope (DP-09) |

`recovery_case`, `case_account` and `case_party` are rwb-case tables, `document` is a rwb-document table and the account, appraisal and contact-point rows are rwb-source-data's; all of them are reached only through their owners' operations, and `decision_log_entry` is rwb-decision's and is not written here. No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock | The 200 Epic 1 cases created 2026-11-30 to 2026-12-04 with their CaseCreated events; case "RW-2026-000301"; the case reads that return no agent output; the accounts, the parties, the lists and the policy values in force; a case that does not exist | Contract tests, app story |
| rwb-source-data WireMock | The account facts, the appraisals and their dates, the contact points and their usage codes; freshness stamps with `status` `LOADED` and `STALE`, and a never-stamped answer (`businessDate` null, `status` `STALE`); a delay beyond 2 s and a refusal | Contract tests, app story |
| rwb-document WireMock | The documents of a case with their type and review status; a case with no document; a delay beyond 2 s | Contract tests, app story |
| rwb-access WireMock | `POST /authorise` granting Rules and parameters C to RW-COE and R to RW-RISK, and refusing a role without the right | Contract tests, app story |
| Model stub (INT-23 boundary) | A valid "intake-summary-v1" answer with the four gap types; silence for 61 seconds; an answer with a missing member; an answer with a confidence under 0.80 | Contract tests, app story |
| gateway-bff route stub | A pass-through route of one hop in front of the base `/api/recovery/agent/v1`, with the query parameters and the media types preserved; its route name and path are Not specified in the source documents (GAP-0610; ASM-0868) | Contract tests, app story |

The decision-record library stub and the outbox stub are the platform's and are used but not declared here. Every fixture is synthetic.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 10 consumed | The start and the read operation on `/api/recovery/agent/v1`; the rwb-case case, accounts and parties reads, the list read and the parameter read; the three tool reads and the freshness read of rwb-source-data; the rwb-document read and the rwb-access authorise call; one hop, 2 s each; the INT-23 call is HTTPS at the boundary with the 60 second policy timeout |
| Kafka | 1 published, 1 consumed | EV-28 on `rwb.agent.events.v1` through the outbox, and CaseCreated on `rwb.case.events.v1` through the inbox |
| Temporal | 1 workflow, 4 activities | AgentRunWorkflow and BuildIntakeInputs, CallModelGateway, CheckGuardrail and RecordShadowRun on the queue `rwb-agent` |
| File | None | No file is read or written; the input snapshot travels inside the run and the event |

### 13. Solution plan

**Deliverables.** `contract/agent-run-operations.yaml` (the start and the read operation, their members, their refusals and their budget), `contract/intake-summary-v1.json` (the answer shape with the four gap types and the 1,500 character limit), `contract/agent-run-completed.asyncapi.yaml` (EV-28 on `rwb.agent.events.v1`, its registry subject, its retry and `.dlt` topics), `contract/intake-run-start.md` (the event-driven interface and the run key, aligned to RWB-P10-TE013-CON), `contract/intake-consumed-reads.md` (the ten consumed operations with their owners and budgets) and the six WireMock and stub mappings with their synthetic fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON for the app story; none here |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | C RWB-P3-E1042-CON for the app story; none here |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | C RWB-P3-E1043-CON for the app story; none here |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story; none here |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none here; the consumer adds RWB-P10-E1059-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story; none here |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story; none here |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON for the app story; none here |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts and the P3, P5 and P4 contracts it names are those its consumers add, and each C dependency of the key sits on the app story and not here. DP-03 is named because the run record of the platform uses the library; a shadow run writes no record with it (BR7).

**Build steps**

1. Write the two operation contracts: method, path below the base, the request members, the answer members, the refusal codes with MSG-GEN-001, MSG-P4-002 and the 409 of a repeat; add a lint to the pipeline.
2. Write the answer shape `intake-summary-v1.json` with the 1,500 character limit, the three members and the four gap types, and a check that it carries no personal field.
3. Write the EV-28 AsyncAPI document: the envelope, the key, the payload members, the registry subject, the three retry topics and the `.dlt` route.
4. Write the start interface document: the CaseCreated consumption, the run key, the one workflow per key, and the statement that no job table is used.
5. Write the consumed read side with the ten operations, their owners and their budgets, and mark the paths the sources do not name.
6. Build the six fakes and their synthetic fixtures, including the silent model answer and the slow read.
7. Add the contract tests of section 16, including the drift test between each fake and this document.
8. Tag the baseline and collect the sign-off of the app stories of this key.

**Done when.** The six contract files validate in the pipeline, the eight contract tests pass, the six fakes answer every consumed path and payload, and RWB-P10-E1059-APP and RWB-P10-E1061-APP have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required member of the request is empty | Enter {field}. |
| MSG-P4-002 | A role without the right calls an operation | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | A consumed data product is stale | {product} is from {date}. Today's load has not arrived. |

The two business messages MSG-P4-002 and MSG-P1-001 are the messages reachable from RWB-E1-059; MSG-P4-002 keeps its wording character for character and MSG-P1-001 takes the wording of the Error and Message Standard v4; MSG-GEN-001 is the platform message of an empty required field. This contract adds no message. In AC1 the {action} value is "start a run of this agent" and in AC2 "read a run".

### 15. Screens and states

None in this story. The contract serves the admin reads through the gateway-bff route indirectly: the route in front of `/api/recovery/agent/v1` is a pass-through of one hop and belongs to RWB-PLT-N001-CON (DP-19), the run monitor screen SCR-46 belongs to RWB-E2-031 and is not changed, and the case screens are not touched because a shadow run shows nothing to a case owner. The contract fixes no screen field, no order and no masking rule; the route name and path are Not specified in the source documents (GAP-0610; ASM-0868). The states of SCR-46 (empty, loading, error, no access) are Not specified in the source documents (CG-ALL-2583).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E1059-CON-01 | AC1, BR1, BR2, BR9 | Contract | The start operation validated against its schema: the five request members, a request missing each of them, the 202 answer, the 409 of a repeat with the stored run, the 403 of a role without the right |
| TC-P10-E1059-CON-02 | AC2, BR3, BR7 | Contract | The read operation for a SHADOW run of "INTAKE" on case "RW-2026-000301": the run facts present, the summary and the gap flags absent, 401, 403, 404 and 503 |
| TC-P10-E1059-CON-03 | AC3, BR4, BR5 | Contract | The answer shape: a valid answer, a summary of 1,501 characters, a gapType outside the enum, a missing member, confidence 1.2, and a scan of the payload for a personal field |
| TC-P10-E1059-CON-04 | AC4, BR8 | Contract | EV-28 for a run of "INTAKE": the envelope, the key, the five payload members, a status outside LOV-AGENT-RUN, a registry refusal, the three retry topics and the `.dlt` route |
| TC-P10-E1059-CON-05 | AC5, BR1 | Component | A CaseCreated event of 2026-11-30 for case "RW-2026-000301" twice; one AgentRunWorkflow per run key, one run, the repeat counted, and a scan for a job table |
| TC-P10-E1059-CON-06 | AC6 | Contract | The four rwb-source-data reads and the freshness read: the shape, the SY-AGENT identity, the 2 s budget, the TOOL_UNAVAILABLE mapping, and a scan for a `recovery.v_ace_*` reference in the sources |
| TC-P10-E1059-CON-07 | AC7 | Component | The nine sub-tables complete with None where empty, and the six fakes answering every consumed path and payload |
| TC-P10-E1059-CON-08 | AC7, BR6 | Contract | A drift test between each of the six fakes and this document, and a scan of every fixture for a production value |
| TC-P10-E1059-CON-09 | AC7 | Component | The table boundary of section 12.7: each of the nine tables with its owner and contracted use, a write to a table another service owns refused, and a scan of the sources for a foreign key across a schema |
| TC-P10-E1059-CON-10 | AC8, BR1, BR2, BR3, BR4, BR5, BR7, BR8, BR9 | Contract | Not specified in the source documents (NEWAC-RWB-P10-E1059-CON-AC8) |

### 17. Guardrails

- No business value in the contract: the agent code, the policy and prompt versions, the 60 second timeout, the confidence floor 0.80, the 1,500 character limit and the four gap types are rows and schema values in force, and the contract only names them (BR5).
- No personal data in an answer, an event, an example or a fake: identifiers and facts only, the summary holds masked tokens only, and no fixture carries a real account number, name or national ID (BR4).
- The contract names the two run operations and the agent topic as rwb-agent's and consumes every other operation and topic; a document that declares another service's path or topic as provided fails the review (DP-13, DP-14).
- The run resource and the admin reads are restated, never redefined: RWB-P10-E1058-CON and RWB-P10-TE013-CON own them and a drift is corrected there (BR1).
- Every payload is validated against its registry subject before the relay, retried on the three retry topics and routed to `.dlt` with an alert on failure (BR6, DP-09).
- A shadow run promises no decision record, so no consumer waits for one before acting (BR7).
- Every fixture is synthetic; no production account, document, model answer or run is copied into a schema, a payload or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-005 | Personal data is masked in every agent call | The answer shape with a masked summary and no personal field; the event payload of IDs and facts only | TC-P10-E1059-CON-03, TC-P10-E1059-CON-04 |
| REQ-ACA-010 | Agents run under service identities with role checks | The start and the read operation with their rights, the SY-AGENT identity of the consumed reads | TC-P10-E1059-CON-01, TC-P10-E1059-CON-02, TC-P10-E1059-CON-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two provided operations and the ten consumed reads with their budgets | TC-P10-E1059-CON-01, TC-P10-E1059-CON-06 |
| D-RCV-60 DP-05 | ACE data only through the owner's contract or the service's own views | The four rwb-source-data reads and the freshness read | TC-P10-E1059-CON-06 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | The EV-28 AsyncAPI document, its registry subject, its retry and `.dlt` topics, and the CaseCreated consumption | TC-P10-E1059-CON-04, TC-P10-E1059-CON-05 |
| D-RCV-60 DP-11 | An in-process call becomes a REST contract with a mock, one hop and 2 s | The two provided operations and the six fakes | TC-P10-E1059-CON-01, TC-P10-E1059-CON-07 |
| D-RCV-60 DP-13 | One REST base per service | The base `/api/recovery/agent/v1` and the run resource restated from the baselines | TC-P10-E1059-CON-01, TC-P10-E1059-CON-02 |
| D-RCV-60 DP-20 | The agent client is the rwb-agent contract | The start and the read operation as the intake flow's interface, consumed through RWB-P10-TE013-CON | TC-P10-E1059-CON-01, TC-P10-E1059-CON-05 |

### 19. Out of scope

- The implementation of the listener, the assembler, the guardrail, the scorer and the migration (RWB-P10-E1059-APP).
- The whole agent runtime contract, its policy and prompt resources, the admin configuration reads and the evaluation operations (RWB-P10-E1058-CON, RWB-P10-TE013-CON).
- The report and the L1 proposal of this agent (RWB-P10-E1061-APP).
- The case, its parties and its accounts (rwb-case), the ACE facts and the freshness stamp (rwb-source-data), the documents (rwb-document) and the rights (rwb-access).
- The central decision ledger and the sealing of records (P7 rwb-decision).
- The topic, its retry and `.dlt` topics, the queue, the secrets, the indexes and the capacity of the service, which are held by its operations story.
- The field-level detail of the consumed answers, the type of sourceRef, the paths the sources do not name and the gateway-bff route name, which are Not specified in the source documents (GAP-0611; ASM-0862, ASM-0866, ASM-0868).
- The legacy criterion AC5 of RWB-E1-059 (stale input flagged from a COMPLETED ALS row) and its test case TC-E1-059-05, which the split assigns to the integration slice RWB-ITG-E1059-ITG (wave 1): they are not owned by this contract and are not reconstructed here (GAP-0610).
