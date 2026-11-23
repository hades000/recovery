# RWB-P10-E2032-CON TDR offer-suggestion model through the model gateway [E3e]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2032-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-032 for rwb-agent. This is the model-gateway and agent-run contract slice of the legacy key: the operation that replaces `ModelSuggestionClient.suggestOffer` and its `OfferSuggestion` record on `/api/recovery/agent/v1` (DP-11, DP-13), the decision-record payload mapping of the legacy section 12 on the local library and `rwb.decision-record.v1` (DP-03), the EV-28 `AgentRunCompleted` payload on `rwb.agent.events.v1` (DP-09), the two admin reads this key uses, the INT-23 model-gateway client at the boundary, and the four contract fakes. It does not restate the whole rwb-agent contract, whose baseline is RWB-P10-E1058-CON, and it builds no business behaviour. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the TDR offer-suggestion model fixed as a contract on Day 1: the published operation that replaces the in-process `ModelSuggestionClient.suggestOffer` and the eight members of its answer, the decision-record payload mapping of the legacy section 12, the EV-28 `AgentRunCompleted` payload as a CloudEvents 1.0 message, the shape of the two admin reads this key uses, the INT-23 model-gateway request at the boundary with its 60-second policy timeout, and the four contract fakes**, so that **the app story, the infrastructure story and every story that reads a suggestion or an agent run build against one agreed, testable shape without waiting for the agent runtime to be complete**.

### 2. Business rationale

The legacy key RWB-E2-032 was written against a Java interface inside the monolith: `ModelSuggestionClient.suggestOffer` returned an `OfferSuggestion` record, the decision log was written by the in-process `DecisionLogWriter`, the agent run was a table of the same schema, and the account facts came from the same `recovery` tables (legacy section 12). In the target every one of those is a boundary. The interface becomes one REST operation under `/api/recovery/agent/v1` with one hop and a client budget (DP-11, DP-13; ADR-020); the decision log becomes a local record library and the shared topic `rwb.decision-record.v1` (DP-03; ADR-022); the run completion becomes EV-28 on the service's own topic (DP-09; Arch v5 slide 43); the account, the payments and the treatment come through their owners' contracts (DP-05); and the model is reached on the Enterprise AI private endpoint, INT-23, which is the only outside call the service has (Arch v5 slide 16).

Contract-first only works if the seam is written down once. The seam here is small and load-bearing: one operation whose answer carries the eight legacy members so the treatment service needs no change of shape, one record payload that keeps decision "D5", final call "SUGGESTION_RECORDED" and `agent_version` null, one event payload that carries the run facts and no personal data, and one request to the model gateway that names the model code, the masked inputs and the output schema "tdr-offer-v1".

If the shape is agreed and faked on Day 1, three teams move at once. The app story of RWB-P10-E2032-APP builds the mode gate, the guardrail, the record and the outbox against these fakes; the infrastructure story of RWB-P10-E2032-INF provisions the private path to INT-23, the topic with its retry and `.dlt` topics, the queue and the secrets against the same names; and the stories that read a run or a suggestion read one shape. Without it, each caller invents its own answer, the eight legacy members drift, and the record that proves what the model suggested stops matching what the treatment record shows.

This story defines the consumed side and the one provided side of this key, and never restates what another owner holds: the two admin reads are baselined in RWB-P10-E1058-CON, the ledger is rwb-decision's, the treatment is rwb-treatment's, and the account data is rwb-source-data's (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the REST base, the topic and the event names follow the platform rule and not a local choice (§R4; DP-13).
- The CloudEvents 1.0 envelope and the platform error envelope are the platform baseline; this document narrows them where it must and says so.
- The agent runtime baseline contract of RWB-P10-E1058-CON is in force: the two admin reads, the policy and prompt resources, the run resource and the error taxonomy are its elements, and this story reuses them rather than redefining them. Its task queue is `rwb-agent` and its namespace `rwb-recovery` (§R4).
- The decision-record library of RWB-PLT-E1027-CON publishes the record shape and the topic `rwb.decision-record.v1` with its envelope; the local write and the relay are its elements (DP-03).
- The outbox and retry library of RWB-PLT-TE006-CON publishes the outbox and inbox envelope, the relay and the `.dlt` rule (DP-09).
- The parameter and reference-data contracts of rwb-case are published by RWB-PLT-E1042-CON and RWB-PLT-E1043-CON with their client libraries (DP-06, DP-07).
- The treatment entity contract of RWB-P3-E2004-CON and the runtime treatment owner rwb-treatment (S2) are known, and the rwb-treatment fake is available for the treatment read (ASM-0979).
- The private endpoint of Enterprise AI (INT-23) is named as the external system and its request elements are the legacy ones; its host, port and certificate are Not specified in the source documents (GAP-0634; ASM-0988) and are provisioned by RWB-P10-E2032-INF.
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W2.

### 4. Flow

1. Draft the operation that replaces `ModelSuggestionClient.suggestOffer`: its method, its path below the base `/api/recovery/agent/v1`, its request members, its answer members — the eight legacy ones — and its refusal codes.
2. Fix the decision-record payload mapping of the legacy section 12 on the local library and the shared topic: the case, the decision code, the versions, the inputs reference, the recommendation, the final call and the actions.
3. Declare the EV-28 `AgentRunCompleted` payload on `rwb.agent.events.v1`: the envelope, the key, the payload members taken from the `agent_run` fields of TSD P10 v2 T3.1, and the no-personal-data rule.
4. Restate the two admin reads this key uses, taken from TSD P10 v2 T-A.2, with their query, their answer resource, their rights, their errors and their one-hop budget, and mark them as baselined in RWB-P10-E1058-CON.
5. Fix the INT-23 model-gateway client contract at the boundary: the request members, the output schema "tdr-offer-v1", the policy timeout of 60 seconds, and the mapping of a timeout, a 4xx, a 5xx and a schema failure to a run status of LOV-AGENT-RUN.
6. Write the four contract fakes: rwb-treatment, rwb-decision, rwb-case and the model gateway, each with the answers, the errors and the timings this key's tests need.
7. Publish the nine sub-tables of section 12 and the contract tests: the operation shape, the record mapping, the event envelope and its registry subject, the admin read shapes, the boundary mapping, and a drift test between each fake and this document.
8. Tag the baseline and hand it to RWB-P10-E2032-APP, RWB-P10-E2032-INF and the test cases of this key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field of the suggestion operation drifts from this document: a renamed member, a retyped amount, a dropped one of the eight | The contract test fails and the merge is blocked | None | AC1 |
| X2 | A caller sends a request without the case ID, the treatment ID or the idempotency key | The operation refuses the request with 422 and names the field; nothing is written | MSG-GEN-001 | AC1 |
| X3 | The record payload or the event payload gains a personal field | The data-steward review and the contract test refuse the payload; nothing is published | None | AC2, AC3 |
| X4 | A produced payload fails its registry subject, or the relay cannot reach the topic | The message is refused before the relay and routed to the `.dlt` topic of the agent topic with an alert | None | AC3 |
| X5 | The admin read shape drifts from the baseline of RWB-P10-E1058-CON | The contract test fails on the baseline and this document is aligned, because the baseline is the owner | None | AC4 |
| X6 | The model gateway answers a 4xx, a 5xx or nothing inside the policy timeout | The answer maps to MODEL_ERROR or TIMED_OUT, and no status outside LOV-AGENT-RUN is written | None | AC5 |
| X7 | A field-level detail of a consumed operation or of a record member is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC1, AC2, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the agent runtime baseline contract, the decision-record library, the outbox library and the rwb-case contracts as published |
| Negotiable | Field-level detail of the consumed operations is settled with their owners; the operation shape, the record mapping, the event payload and the boundary mapping are fixed by this realignment |
| Valuable | Unblocks the app and infrastructure stories of this key on Day 1 and gives every reader of a suggestion or a run one shape |
| Estimable | One provided operation, four consumed reads, one record mapping, one event, two admin read shapes, one boundary contract and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the schema file, the payload, the fake, the document — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: TDR offer-suggestion contract slice for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the agent runtime baseline contract of RWB-P10-E1058-CON is in force
    Given the decision-record library and the outbox library of the platform are in force

  Scenario: AC1 The suggestion operation replaces the in-process interface (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When the treatment service asks for a suggestion for treatment "T-1001" with the idempotency key "TDR_OFFER:T-1001"
    Then one operation answers with the eight members agentRunId, decisionLogEntryId, modelCode, modelVersion, installments, monthlyAmountThb, interestRate and confidence, with the names and the types of this document
    Then the request carries the case ID, the treatment ID and the idempotency key, and a request without one of them is refused with 422 and MSG-GEN-001
    Then the operation is declared once, under the base /api/recovery/agent/v1, with one hop and the 2 s client budget of DP-11 on every caller, and the model call of up to 60 seconds happens inside the service (ASM-0978)
    Then the refusals are 409 for a repeat that returns the stored answer, 503 with MSG-P7-003 when the decision cannot be recorded, and 200 with no suggestion and MSG-P10-007 when the model is not in service
    Then the rwb-treatment fake answers the request and a drift between the fake and this document fails the contract test

  Scenario: AC2 The decision-record payload mapping is fixed (new, D-RCV-60)
    Given the legacy mapping of section 12 of RWB-E2-032
    When a suggestion is recorded for treatment "T-1001" on case "RW-2026-001001"
    Then the record carries case_id "RW-2026-001001", decision_code "D5", model_version "TDR-OFFER-1.0", agent_version null, inputs_ref equal to the masked inputs snapshot, recommendation equal to the suggestion, final_call "SUGGESTION_RECORDED" and actions {treatmentId, agentRunId}
    Then the record is written by the local decision-record library of RWB-PLT-E1027-CON in the same transaction as the agent_run row, and its reference is stored in agent_run.decision_log_id
    Then its outbox row is rwb.decision-record.DecisionRecorded.v1 on rwb.decision-record.v1, keyed by the record reference, and rwb-decision seals it into the central ledger
    Then no account number, no customer name and no personal field appears in inputs_ref or in the payload

  Scenario: AC3 EV-28 AgentRunCompleted is declared on the agent topic (new, D-RCV-60)
    Given a run of agent "TDR_OFFER" for case "RW-2026-001001"
    When the run completes and the outbox relay publishes it
    Then the message type is rwb.agent.AgentRunCompleted.v1 on rwb.agent.events.v1 and it is keyed by the case ID
    Then the envelope carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype, with the run ID as its subject
    Then the payload carries the run facts this document names from the agent_run fields of TSD P10 v2 T3.1: run ID, agent_code, agent_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, run_at
    Then the status is one of LOV-AGENT-RUN and no status outside the list is published
    Then a payload that fails the registry subject is refused before the relay and routed to the .dlt topic with an alert, and no personal data is carried

  Scenario: AC4 The two admin reads this key uses are contracted (new, D-RCV-60)
    Given the agent runtime baseline contract of RWB-P10-E1058-CON
    When the two admin reads are reviewed against it
    Then GET /api/recovery/agent/v1/admin/agent-runs takes the query agent, from and to, answers AgentRun[] and declares 401, 403 and 503 under Platform administration R with scope applied
    Then GET /api/recovery/agent/v1/admin/agent-configs takes the query agent, kind and status, answers AgentConfigVersion[] and declares 401, 403 and 503 under Rules and parameters R with scope applied
    Then the answer of the config read shows the TDR_OFFER version "P1" with mode "OFF" and review date 2027-02-28, and the version, mode and review date are the members this key reads
    Then neither read is declared as owned by this story, and a drift is corrected against the baseline and never against this document
    Then the gateway-bff route in front of the two reads is a pass-through of one hop, and its route name and path are Not specified in the source documents (GAP-0634; ASM-0987)

  Scenario: AC5 The INT-23 boundary is fixed with its timeout and its statuses (new, D-RCV-60)
    Given the model-gateway client contract of this document
    When a suggestion is asked for with policy version "P2" in mode "L1"
    Then the request carries the model code, the masked inputs and the output schema "tdr-offer-v1" and nothing else
    Then the call is bounded by timeout_seconds of the policy version in force, 60 seconds for the versions of this key (NFR-010)
    Then mode "OFF" makes no call at all, a timeout writes TIMED_OUT with fallback true, a 4xx or a 5xx writes MODEL_ERROR with fallback true, and a failed schema writes GUARDRAIL_FAILED with check "SCHEMA"
    Then the model-gateway fake answers a valid answer of 84 installments of 18,900.00 baht, an answer with installments -12, silence for 61 seconds, a 4xx and a 5xx

  Scenario: AC6 The nine sub-tables are complete and the four fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables and the four fakes are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then the fakes rwb-treatment, rwb-decision, rwb-case and the model gateway answer every consumed path and payload of this document
    Then a drift between a fake and this document fails the contract test, and the four fake fixtures are synthetic
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The suggestion is one operation under `/api/recovery/agent/v1` and one answer of eight members; no caller embeds the agent runtime and no in-process interface survives | DP-11; DP-13; legacy section 12 |
| BR2 | The record keeps decision "D5", final call "SUGGESTION_RECORDED" and `agent_version` null, and is written before the answer leaves | Legacy section 12; Principle 5; R-UNI-39; DP-03 |
| BR3 | EV-28 carries run facts only: the payload is the `agent_run` fields named here, with no account number, no customer name and no personal field | Arch v5 slides 42 and 43; Template and Rules §R7.2 s17 |
| BR4 | Every message is a CloudEvents 1.0 message on the owner's topic, keyed by the case ID, validated against its registry subject before the relay, and routed to `.dlt` on failure | DP-09; DP-14; Arch v5 slide 42 |
| BR5 | The two admin reads belong to the agent runtime baseline; this document restates only the members this key reads and never declares them as its own | RWB-P10-E1058-CON; DP-13 |
| BR6 | The model is reached only on the Enterprise AI private endpoint (INT-23) with the model code, the masked inputs and the output schema "tdr-offer-v1", bounded by the timeout of the policy version in force | Legacy BR1; TSD P10 v2 T5.1; NFR-010 |
| BR7 | A run status is always one of LOV-AGENT-RUN; a timeout, an error and a schema failure map to TIMED_OUT, MODEL_ERROR and GUARDRAIL_FAILED and never to an invented value | TSD P10 v2 T3.2 |
| BR8 | No business value in the contract: the model code and version, the schema limits, the timeout, the mode and the review date are rows of the policy version, and the contract only names them | Template and Rules §R7.2 s17; BR-P10-010 |
| BR9 | One base and one topic per service: this contract declares `/api/recovery/agent/v1` and `rwb.agent.events.v1` for rwb-agent and never another service's path or topic as its own | DP-13; DP-14; Arch v5 slide 41 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the record mapping, the event payload, the two admin read shapes and the boundary contract are described | In review |
| In review | Consumer sign-off | The app and infrastructure stories of this key and the test cases accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a query parameter or a payload field is added without removing one | Baselined |
| Baselined | Breaking change to the operation or to a payload | A member of the eight, a record member or an event member is removed, renamed or retyped | In review, with the owner of the affected contract |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | The agent runtime baseline changes an admin read | RWB-P10-E1058-CON publishes a new shape | Baselined, aligned to the baseline |

These are the states of this document, not of a case, a treatment or a run. The run states themselves are those of LOV-AGENT-RUN and belong to RWB-P10-E2032-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the operation shape, the record mapping, the event payload, the boundary contract, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to the operation, the record or the event, and any change to the boundary timeout |
| The rwb-decision owner | Owns the record shape and the shared topic, and signs off the mapping taken from its document |
| The rwb-treatment, rwb-source-data and rwb-case owners | Own the consumed operations and sign off the shapes taken from their documents |
| The rwb-agent app and infrastructure stories | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule, the decision-record library and the outbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in the record, the event or the boundary request |

The identity that calls the model gateway is the rwb-agent service identity (DP-02); its name, the Key Vault entries it uses and the certificate it presents are Not specified in the source documents (GAP-0634; ASM-0976) and are fixed by RWB-P10-E2032-INF.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Suggestion request | case ID, treatment ID, idempotency key `TDR_OFFER:<treatmentId>` |
| Suggestion answer | agentRunId, decisionLogEntryId, modelCode, modelVersion, installments, monthlyAmountThb, interestRate, confidence (the eight legacy members) |
| Refusal | the platform problem response: status, code, detail, the message ID when a business message applies |
| Decision record | case_id, decision_code "D5", model_version, agent_version null, inputs_ref, recommendation, final_call "SUGGESTION_RECORDED", actions {treatmentId, agentRunId} |
| Record event payload | record reference, decision "D5", model version, agent version null, final call, the suggested terms, the actions |
| EV-28 payload | run ID, agent_code, agent_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, run_at |
| Admin read answers | AgentRun[] and AgentConfigVersion[] as published by RWB-P10-E1058-CON; the members this key reads are the version, the mode and the review date |
| Boundary request | model code, masked inputs, output schema "tdr-offer-v1"; the boundary answer is the suggestion in the shape of the model owner |

The field-level detail of the suggestion request beyond the three members named above, the type and length of `inputs_ref`, and the boundary answer shape are Not specified in the source documents (GAP-0634; ASM-0983, ASM-0986); this document fixes the element names and leaves the types to the review with their owners. The host, port and certificate of INT-23 are Not specified in the source documents (GAP-0634; ASM-0988) and belong to RWB-P10-E2032-INF.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Rights |
|---|---|---|---|
| POST | `/api/recovery/agent/v1/<suggestion path>` — Not specified in the source documents (GAP-0634; ASM-0977) | Replaces `ModelSuggestionClient.suggestOffer`: one suggestion for one treatment, answered with the eight legacy members | The service identity of the caller; Treatment and offer R |

The two admin reads this key uses are provided by rwb-agent and baselined in RWB-P10-E1058-CON; 12.2 of that document owns their full shape. This contract restates only the members this key reads and declares no admin operation of its own.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract |
|---|---|---|---|
| GET | Not specified in the source documents (GAP-0634; ASM-0980) | P1 rwb-source-data | The account facts and the 12 months of payments, masked before the boundary request |
| GET | Not specified in the source documents (GAP-0634; ASM-0979) | S2 rwb-treatment | The treatment, its case and its type; the contract baseline of the entity is RWB-P3-E2004-CON |
| GET | Not specified in the source documents (GAP-0634; ASM-0979) | P3 rwb-case | The case facts, and the parameter and reference-data values in force (DP-06, DP-07) |
| GET | Not specified in the source documents (GAP-0634; ASM-0981) | P7 rwb-decision | The sealed decision record of a suggestion, read back for AC3 |

Every operation is one hop with a 2 s client budget (DP-11, ADR-020). The call to INT-23 is external and is declared in 12.9, not here.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | run ID, agent_code, agent_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, run_at |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | record reference, decision "D5", model version, agent version null, final call "SUGGESTION_RECORDED", the suggested terms, the actions |

Both are CloudEvents 1.0 messages inserted in the outbox in the same transaction as the run row and relayed by the outbox library; a payload is validated against its registry subject before the relay (DP-09; BR4).

#### 12.4 Events consumed

None. This key reads no topic. The inbox of the outbox library is used only for the relay's own dedupe, and the consumers of EV-28 are rwb-decision, rwb-document and rwb-deviation, not this service (Arch v5 slide 43).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (Arch v5 slide 16) | `rwb-agent` | Input: agent code, case ID, subject ID, trigger event, idempotency key. One execution per idempotency key, with the 60-second budget and then the rule result |
| BuildTdrInputs | Activity | `rwb-agent` | Output: the masked inputs and the inputs reference; no personal field leaves the activity |
| CallModelGateway | Activity | `rwb-agent` | Input: model code, masked inputs, output schema, timeout. Output: the suggestion or the mapped status TIMED_OUT, MODEL_ERROR |
| CheckGuardrail | Activity | `rwb-agent` | Input: the answer and the output schema reference. Output: the check code and the outcome, SCHEMA included |
| RecordAndApply | Activity (workflow kit) | `rwb-agent` | Input: the run row, the record and the outbox rows; one transaction, no partial write |

The workflow name, the queue and the 60-second budget are those of Arch v5 slide 16; the activity names and their inputs and outputs are this story's and are accepted by RWB-P10-E2032-APP.

#### 12.6 Schedules

None. The suggestion is request-driven and the Arch v5 job map names no job for an agent suggestion (slide 44). No Temporal Schedule is declared, changed or owned by this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_run | P10 (rwb_agent) | The run facts of the EV-28 payload and the stored answer of an idempotency key; no column added |
| agent_policy | P10 (rwb_agent) | The values the contract names: model code and version, output schema, timeout, mode, review date; no column added |
| agent_prompt | P10 (rwb_agent) | The prompt version, where a run names one; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | The outbox, inbox and idempotency envelope (DP-09) |

`decision_log_entry` is a rwb-decision table and is reached only through the decision-record library (DP-01, DP-03). No foreign key crosses a schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-treatment WireMock | Treatment "T-1001" of type "RESTRUCTURE" on case "RW-2026-001001"; treatment "T-1002" of type "SETTLEMENT"; a treatment that does not exist; a slow answer | Contract tests, app story |
| rwb-decision WireMock | The sealed record of the suggestion with decision "D5" and final call "SUGGESTION_RECORDED"; a record that is not found | Contract tests, app story |
| rwb-case WireMock | The lists LOV-AGENT, LOV-AUTONOMY and LOV-AGENT-RUN; the parameter values in force; an answer with a mode outside LOV-AUTONOMY | Contract tests, app story |
| Model gateway fake (INT-23) | An answer of 84 installments of 18,900.00 baht; an answer with installments -12; silence for 61 seconds; a 4xx and a 5xx; an answer outside the output schema | Contract tests, app story, infrastructure tests |

The decision-record library stub, the outbox stub and the gateway-bff route stub are the platform's and are used but not declared here. Every fixture is synthetic.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | The suggestion operation on `/api/recovery/agent/v1`, and the reads of rwb-source-data, rwb-treatment, rwb-case and rwb-decision; one hop, 2 s each; the INT-23 call is HTTPS at the boundary, with the policy timeout |
| Kafka | 2 published, 0 consumed | EV-28 on `rwb.agent.events.v1` and the record on `rwb.decision-record.v1`, both through the outbox |
| Temporal | 1 workflow, 4 activities | AgentRunWorkflow and BuildTdrInputs, CallModelGateway, CheckGuardrail and RecordAndApply on the queue `rwb-agent` |
| File | None | No file is read or written; the input snapshot travels inside the record |

### 13. Solution plan

**Deliverables.** `contract/agent-suggestion-operation.yaml` (the operation, its request, its answer with the eight members, its refusals and its budget), `contract/agent-decision-record.md` (the record mapping of the legacy section 12 on the shared topic), `contract/agent-run-completed.asyncapi.yaml` (EV-28 on `rwb.agent.events.v1`), `contract/agent-admin-reads.md` (the two admin reads this key uses, aligned to RWB-P10-E1058-CON), `contract/model-gateway-boundary.yaml` (the INT-23 request, the output schema "tdr-offer-v1" and the status mapping) and the four WireMock mappings with their fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON; C RWB-P7-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | H RWB-P10-E2032-CON for the app story; none here |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts it names are those its consumers add, and the only C dependency of the key, RWB-P7-E1027-CON, is the rwb-decision side of the shared record. DP-11 is the pattern of the operation and of the four consumed reads; the model boundary keeps the policy timeout of 60 seconds, the recorded exception of ASM-0978.

**Build steps**

1. Write the operation contract: method, path below the base, the three request members, the eight answer members with their types, and the refusal codes with MSG-P7-003, MSG-P10-007 and MSG-GEN-001; add a lint to the pipeline.
2. Write the record mapping and its payload, with `agent_version` null and the actions, and the rule that the record is written before the answer.
3. Write the EV-28 AsyncAPI document: the envelope, the key, the payload members and the registry subject; declare the `.dlt` route.
4. Restate the two admin reads against the baseline, with their query, answer, rights and errors, and mark the baseline as owner.
5. Write the boundary contract: the request, "tdr-offer-v1", the 60-second policy timeout and the mapping of a timeout, a 4xx, a 5xx and a schema failure to LOV-AGENT-RUN.
6. Build the four WireMock mappings and their synthetic fixtures, including the silent answer of 61 seconds.
7. Add the contract tests of section 16, including the drift test between each fake and this document.
8. Tag the baseline and collect the sign-off of the app and infrastructure stories of this key.

**Done when.** The six contract files validate in the pipeline, the six contract tests pass, the four fakes answer every consumed path and payload, and the app and infrastructure stories of this key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required member of the request is empty | Enter {field}. |
| MSG-P10-007 | No suggestion: the model is not in service, the call timed out, the gateway answered an error or the schema check failed | No offer suggestion is available for this treatment. The TDR model is not in service. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right reads an admin operation | You cannot {action} here. Your role does not include it. |

The three business messages are the legacy messages of RWB-E2-032 and keep their wording character for character; MSG-GEN-001 is the platform message of an empty required field. This contract adds no message.

### 15. Screens and states

None in this story. The contract serves SCR-14 Treatment record and the two admin reads indirectly: the suggestion area of SCR-14 is composed by the gateway-bff route (DP-19) and belongs to RWB-P10-E2032-APP, and the agent run and config reads belong to RWB-P10-E1058-CON. The contract fixes no screen field, no order and no masking rule.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E2032-CON-01 | AC1 | Contract | The operation validated against its schema: the eight answer members, a request missing each of the three members, and the four refusal codes |
| TC-P10-E2032-CON-02 | AC2 | Contract | The record written for treatment "T-1001" on case "RW-2026-001001": decision "D5", agent_version null, final call "SUGGESTION_RECORDED", the actions, and the outbox row |
| TC-P10-E2032-CON-03 | AC3 | Component | EV-28 for a run of "TDR_OFFER": the envelope, the key, the payload members, a status outside LOV-AGENT-RUN, a registry refusal and the `.dlt` route |
| TC-P10-E2032-CON-04 | AC4 | Contract | The two admin reads against the baseline: query, answer, rights, errors, and the version, mode and review date 2027-02-28 of "TDR_OFFER" version "P1" |
| TC-P10-E2032-CON-05 | AC5 | Contract | The boundary request and the five model-gateway fake answers: valid, installments -12, silence for 61 seconds, a 4xx and a 5xx |
| TC-P10-E2032-CON-06 | AC6 | Component | The nine sub-tables complete with None where empty, and the four fakes answering every consumed path and payload |

### 17. Guardrails

- No business value in the contract: the model code and version, the schema limits, the timeout, the mode and the review date stay rows of the policy version, and the contract only names them.
- No personal data in a record, an event, an example or a fake: identifiers and facts only, and the inputs reference holds the masked snapshot.
- The contract names the agent operation and the agent topic as rwb-agent's and consumes every other operation and topic; a document that declares another service's path or topic as provided fails the review (DP-13, DP-14).
- The two admin reads are restated, never redefined: the baseline RWB-P10-E1058-CON owns them and a drift is corrected there.
- Every payload is validated against its registry subject before the relay, and a refusal is routed to `.dlt` and alerted (DP-09).
- The model boundary carries the model code, the masked inputs and the output schema only; nothing else of the case leaves the service.
- Every fixture is synthetic; no production account, payment, model answer or record is copied into a schema, a payload or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CHO-006 | A treatment record holds every offer's type, terms, approval and outcome | The suggestion operation and its eight members; the stored answer of an idempotency key | TC-P10-E2032-CON-01 |
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | The record mapping with decision "D5", the model version and `agent_version` null; the EV-28 payload with the run versions | TC-P10-E2032-CON-02, TC-P10-E2032-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The provided operation, the four consumed reads and their budgets; the boundary timeout as the recorded exception | TC-P10-E2032-CON-01, TC-P10-E2032-CON-05 |
| ADR-022 | Local decision record plus central ledger | The record written by the library before the answer and carried on `rwb.decision-record.v1` | TC-P10-E2032-CON-02 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | The EV-28 AsyncAPI document, its registry subject and its `.dlt` route | TC-P10-E2032-CON-03, TC-P10-E2032-CON-06 |
| D-RCV-60 DP-13 | One REST base per service | The base `/api/recovery/agent/v1` and the two admin reads restated from the baseline | TC-P10-E2032-CON-01, TC-P10-E2032-CON-04 |

### 19. Out of scope

- The implementation of the operation, the mode gate, the guardrail, the record and the outbox (RWB-P10-E2032-APP).
- The network path to INT-23, the topic, its retry and `.dlt` topics, the queue, the secrets and the capacity (RWB-P10-E2032-INF).
- The whole agent runtime contract, its policy and prompt resources and the full shape of the two admin reads (RWB-P10-E1058-CON).
- The agent runtime itself, the other agents, the evaluation harness and the monitor (RWB-P10-E1058-APP, RWB-P10-E1060-APP, RWB-P10-E1063-APP).
- The central decision ledger, its sealing and its read (P7 rwb-decision).
- The treatment, the case, the account and payment data, the parameters, the reference data and the access rights (rwb-treatment, rwb-case, rwb-source-data, rwb-access).
- The Helm values, the consumer group, the dashboards, the alerts and the runbook of this key, which are held by its infrastructure story.
- The field-level completeness of the boundary answer, the type of `inputs_ref`, the INT-23 host and certificate and the gateway-bff route name, which are Not specified in the source documents (GAP-0634; ASM-0983, ASM-0986, ASM-0987, ASM-0988).
