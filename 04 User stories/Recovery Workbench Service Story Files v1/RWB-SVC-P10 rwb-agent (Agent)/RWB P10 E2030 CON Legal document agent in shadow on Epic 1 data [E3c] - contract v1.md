# RWB-P10-E2030-CON Legal document agent in shadow on Epic 1 data [E3c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2030-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-007, FR-P10-012, FR-P10-013, FR-P10-014) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract slice of RWB-E2-030 for rwb-agent, written on Day 1. It fixes the seam the app story builds against: the run start and run read on `/api/recovery/agent/v1` (DP-13), the `legal-pack-v1` output with its completeness list, the consumed boundary of rwb-document (RWB-P5-E2025-CON), rwb-litigation and rwb-case, the policy payload narrowed with the review date and the evaluation run ID (DP-06), the restated evaluation and score shapes of RWB-P10-E1061-CON, the event contract of `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` with its retry and `.dlt` topics (DP-09), the lists of rwb-case (DP-07), the gateway-bff route (DP-19) and the five fakes. It adds no business behaviour, no table and no migration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the legal document key fixed as a contract on Day 1 - the run start and run read of agent "LEGAL_DOC" on `/api/recovery/agent/v1`, the `legal-pack-v1` output and its completeness list, the three document reads of RWB-P5-E2025-CON with the by-case legal-action and case reads, the policy payload with mode SHADOW, review date, evaluation run ID, allowed tools and schema reference, the restated evaluation and score shapes, the EV-28 event on `rwb.agent.events.v1`, the gateway-bff route, the error taxonomy and five fakes**, so that **the app story, the Epic 5 pack story and every reader of a legal-pack score build against one agreed, testable shape without waiting for the model, and no reader is offered a pack from a monolith table, a lake artefact or a schedule that does not exist**.

### 2. Business rationale

The legacy key RWB-E2-030 was written against objects inside the monolith: the run wrote `agent_run` and `agent_evaluation` rows beside the policy row, the documents, their fields and the checklist came from `DocumentQueryService` in process, the open legal action from `LegalActionQueryService` in process, and the whole path was served on the legacy monolith base (legacy sections 4, 11, 12 and 13). In the target every one of those is a boundary:

- The run, the sample, the evaluation run, the score rows, the prompt and the policy version are rwb-agent's own tables in `rwb_agent`; the operations that start and report an evaluation already belong to RWB-P10-E1061-CON and the configuration and sample operations to RWB-P10-E1058-CON, so this key narrows them and adds no member of its own (DP-01).
- The documents, their checked fields and the case-type checklist are P5 rwb-document, read through RWB-P5-E2025-CON one hop with the 2 s budget (DP-11).
- The case and the legal action are P3 rwb-case and S4 rwb-litigation and are read through their contracts; no service opens another service's table (DP-01).
- The minimum sample of 50 and the promotion check list are parameter and policy values read at load time, never code (DP-06); the lists come from the reference-data contract (DP-07).
- The run facts leave as CloudEvents on `rwb.agent.events.v1` with the platform's retry and `.dlt` topics (DP-09, DP-14).
- The base and the route are the platform's: `/api/recovery/agent/v1` behind gateway-bff (DP-13, DP-19).

Contract-first only works if the seam is written down once. The seam here is small and load-bearing: one run start and one run read whose answer carries the pack, one output schema with its completeness list, three boundary reads with their failure mapping, one policy payload with the review date, two restated evaluation shapes whose score row carries 0.9200 on 46 of 50, one event, one route, one error taxonomy and one fake set that makes the app story testable on Day 1.

If the shape is agreed and faked on Day 1, two teams move at once: RWB-P10-E2030-APP builds the assembler, the checks, the scorer and the validator against these fakes, and the Epic 5 pack story of S4 consumes the same output schema and score row. Without it, each caller invents its own pack member, the panel and the evaluation report drift apart, and a promotion is decided on a number nobody can reproduce.

This document defines the provided side on the agent base and the consumed side of the key, and never restates what another owner holds: the configuration and sample operations are RWB-P10-E1058-CON's, the evaluation operations are RWB-P10-E1061-CON's, the parameters and lists are rwb-case's, the documents and the checklist are rwb-document's, and the legal action is rwb-litigation's (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the REST base, the topic and the event names follow the platform rule and not a local choice (§R4; DP-13, DP-14).
- The CloudEvents 1.0 envelope and the platform problem response are the platform baseline; this document narrows them where it must and says so.
- The agent runtime baseline of RWB-P10-E1058-CON is in force: the policy, prompt and sample resources, the configuration operations, the approval and the admin run read are its elements, and this story narrows the policy payload with the review date, the evaluation run ID, the allowed tools and the schema reference rather than redefining it.
- The evaluation baseline of RWB-P10-E1061-CON is in force: the start, the list and the report operations, their statuses and their messages; this story restates them with the legal narrowing and adds no operation.
- The rwb-document contract RWB-P5-E2025-CON is in force for the documents of a case, the checked fields of a document and the checklist of a case type. The three paths this key consumes below the P5 base are named by no source and are fixed here against the fake (GAP-0628; ASM-0944).
- The rwb-case contracts are published: `GET /api/recovery/case/v1/cases/{caseId}` (RWB-P3-E2015-CON), `GET /api/recovery/case/v1/admin/parameters` (RWB-P3-E1042-CON) and `GET /api/recovery/case/v1/admin/lists/{listCode}` (RWB-P3-E1043-CON).
- The rwb-litigation by-case legal-action read is published before this lane starts; its path is named by no source and is consumed and faked here with no C row of its own (GAP-0628; ASM-0944).
- The outbox and inbox library of RWB-PLT-TE006-CON publishes the envelope, the relay, the retry topics and the `.dlt` rule. The gateway-bff route contract and its stub are published by RWB-PLT-N001-CON.
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W2.

### 4. Flow

1. Draft the run start and the run read on `/api/recovery/agent/v1` with their input, their answer and the run statuses of LOV-AGENT-RUN.
2. Fix the `legal-pack-v1` output and the completeness list: one item per checklist code with its status, its document IDs and its defect reason, plus the confidence.
3. Fix the consumed boundary: the three document reads, the by-case legal-action read and the case read, each one hop with the 2 s budget, and the mapping of a failed read to TOOL_UNAVAILABLE with the reason naming the read.
4. Fix the policy payload and the promote-or-keep outcome: mode SHADOW with the review date, mode L1 with the conditions, the evaluation run ID, the allowed tools, the schema reference and the 60-second timeout, loaded and then approved by a person other than the loader.
5. Restate the evaluation start, list and report with the legal narrowing, and fix the score row: one row per checklist code with the sample size, the agreement rate at four decimals and the not-run cases counted.
6. Declare the event: `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` with the retry and `.dlt` topics, the run facts of this document and no pack member.
7. Fix the route, the parameter and list reads, and the boundary of section 12.2.
8. Write the five fakes: rwb-document, rwb-litigation, rwb-case, the model gateway and the gateway-bff route.
9. State the absence rules: no new table, no migration, no Schedule, no lake artefact and no pack on a topic.
10. Publish the nine sub-tables and the seven contract tests, and tag the baseline for the app story and the Epic 5 pack story.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of the pack, of the score row or of the policy payload drifts from this document: a renamed item member, a dropped status, a retyped figure | The contract test fails and the merge is blocked | None | AC1, AC2, AC5 |
| X2 | A caller sends a request the contract does not allow: a policy file that fails a check, a sample with no labelled row, a second evaluation of the same sample | The operation refuses with 422 or 409 and names the check or the state; nothing is written | MSG-P10-001, MSG-P10-002, MSG-P10-003 | AC4, AC5 |
| X3 | The contract declares a table of another service, a lake artefact, a Schedule or a pack on a topic | The review refuses the document, because none of those exists in the target | None | AC6 |
| X4 | A payload gains a personal field or fails its registry subject | The data-steward review and the contract test refuse the payload; a produced message that fails is routed to `.dlt` with an alert | None | AC6 |
| X5 | A consumed read slows beyond 2 s or fails | The run is answered TOOL_UNAVAILABLE with fallback true and the read named, and the case is scored as not run | None to a user | AC3 |
| X6 | A restated operation drifts from its baseline of RWB-P10-E1058-CON or RWB-P10-E1061-CON | The contract test fails and this document is aligned, because the baseline is the owner | None | AC1, AC4, AC5 |
| X7 | A field-level detail of a consumed read, a pack member or the route is missing from the source material | The element carries the placeholder, the combined gap row and one assumption row, and the fake is written to the assumed shape | None | AC2, AC3, AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and route stub, the agent runtime and evaluation baselines and the rwb-case, rwb-document and rwb-litigation contracts as published |
| Negotiable | The types of the pack members, the exact consumed paths and the route name are settled with their owners; the pack shape, the policy payload, the score row, the event and the fakes are fixed by this realignment |
| Valuable | Unblocks the app story on Day 1 and gives the Epic 5 pack story one output schema and one score row |
| Estimable | Two provided operations, two narrowed configuration payloads, three restated evaluation operations, three boundary reads, one event and five fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact - the contract file, the payload, the fake - and never against a model outcome |

### 7. Acceptance criteria

```gherkin
Feature: Legal document agent in shadow - contract slice for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the agent runtime baseline of RWB-P10-E1058-CON and the evaluation baseline of RWB-P10-E1061-CON are in force
    Given the outbox library of RWB-PLT-TE006-CON and the gateway-bff route stub of RWB-PLT-N001-CON are in force

  Scenario: AC1 The run start and the run read are fixed on the agent base (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When RW-COE starts one shadow run of agent "LEGAL_DOC" for case "RW-2026-000901" in evaluation run "EV-LEGAL-S1-001"
    Then POST /api/recovery/agent/v1/agent-runs takes agent "LEGAL_DOC", caseId, evaluationRunId and the idempotency key and answers 202 with an AgentRun in status "ANSWERED", "TIMED_OUT", "GUARDRAIL_FAILED", "BELOW_FLOOR" or "TOOL_UNAVAILABLE" as the statuses of LOV-AGENT-RUN
    Then GET /api/recovery/agent/v1/agent-runs/{runId} answers the run of Arch v5 slide 16 with agent, agentVersion, caseId, outcome, fallback and latencyMs, plus autonomyMode, guardrailResult, output and evaluationRunId
    Then a repeat of the same idempotency key returns the first run and creates no second run and no second model call
    Then the path of the run start below the base is Not specified in the source documents (GAP-0628; ASM-0947) and this document fixes it instead of inventing a business value

  Scenario: AC2 The legal-pack-v1 output and the completeness list are fixed (new, D-RCV-60)
    Given the output schema "legal-pack-v1" referenced by policy "LEGAL_DOC" version "P1"
    When the answer of a run is validated against it
    Then the schema carries items[] with itemCode, status, documentIds[] and defectReason, and confidence at four decimals (DF-AGT-050)
    Then itemCode takes its values from the 9 items of case type "MORTGAGE_CIVIL" including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF", status is PRESENT, MISSING or DEFECT, documentIds holds only IDs the rwb-document contract returned for the same case, and defectReason is required when status is DEFECT
    Then the completeness list is the same items[] read by itemCode and nothing else, and both are stored in agent_run.output (DF-AGT-049) with no member copied to another table
    Then a pack that names a document of another case fails check "SCHEMA_RULE" and an item with no status fails check "SCHEMA", each with run status "GUARDRAIL_FAILED"
    Then the types beyond the legacy names are fixed by this document and no business value is written in code (GAP-0628; ASM-0944)

  Scenario: AC3 The three boundary reads of the key are fixed with their failure mapping (new, D-RCV-60)
    Given the rwb-document contract RWB-P5-E2025-CON and the rwb-case and rwb-litigation contracts
    When a run assembles its input for case "RW-2026-000901" with 14 documents and an open legal action
    Then the documents of a case are read at GET /api/recovery/document/v1/cases/{caseId}/documents with id, caseId, documentType and writeOnce, the checked fields at GET /api/recovery/document/v1/documents/{documentId}/fields with fieldName and the masked fieldValue, and the checklist of a case type at GET /api/recovery/document/v1/cases/{caseId}/document-checklist with the 9 itemCodes of "MORTGAGE_CIVIL"
    Then the open legal action is read by case from rwb-litigation, the case facts of DF-CAS-001, DF-CAS-003 and DF-CAS-017 from rwb-case, and no document, legal action or case table is named as an answer source
    Then each read is one hop with the 2 s client budget, and a failed or slow read answers run status "TOOL_UNAVAILABLE" with fallback true and the reason naming the read, so the case is listed as not run (R-UNI-33)
    Then the three P5 paths, the legal-action path and the field names are the assumed shape of this document (GAP-0628; ASM-0944)

  Scenario: AC4 The policy payload and the promote-or-keep outcome are fixed (new, D-RCV-60)
    Given the policy resource baselined in RWB-P10-E1058-CON
    When RW-COE loads policy "LEGAL_DOC" version "P2" with mode "SHADOW", review date 2027-03-15 and evaluation run "EV-LEGAL-S1-001", and RW-RISK approves it
    Then the payload carries kind POLICY, agent "LEGAL_DOC", policyVersion "P2", autonomyMode "SHADOW", reviewDate, evaluationRunId, promotionConditions, allowedTools, outputSchemaRef "legal-pack-v1" and timeoutSeconds 60, and answers 201 with an AgentConfigVersion in status "LOADED"
    Then POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve answers 200 with status "APPROVED", approvedBy and validFrom, 404 for an unknown version and 409 with MSG-P7-002 when the approver loaded the version
    Then a load with mode "SHADOW" and no review date is refused with 422 and MSG-P10-001 naming check "review date present", and a load with mode "L1" is accepted only when every stated condition is met by the evaluation, otherwise refused with 422 and MSG-P10-001 naming check "sample size at least 50"
    Then the six members beyond the baseline are additive and no member of the baseline is removed (ASM-0956)

  Scenario: AC5 The evaluation operations and the score row of this key are fixed (new, D-RCV-60)
    Given the evaluation operations of RWB-P10-E1061-CON and sample "LEGAL-S1" version 1 on 50 cases
    When the evaluation of agent "LEGAL_DOC" on "LEGAL-S1" version 1 is started and reported
    Then POST /api/recovery/agent/v1/admin/agent-evaluations takes agent, sampleCode, sampleVersion and approaches and answers 202 with an AgentEvaluationRun in status "RUNNING", 422 with MSG-P10-002 for a sample with no labelled row and 409 with MSG-P10-003 for a second evaluation while one is RUNNING
    Then GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report answers sampleSize 50, the three versions, one score row per checklist item, the not-run cases with their failure type, the cost and the latency
    Then the score row for "DEMAND_NOTICE_PROOF" with 46 agreeing cases answers agreementRate 0.9200 and the evaluation with one case not run answers sampleSize 49, and the rate is the value DF-AGT-094 at four decimals
    Then this document restates the operations and adds no member; the narrowing to "LEGAL_DOC" and the not-run count are its only content (ASM-0957)

  Scenario: AC6 The event contract is declared and no pack, table, migration or Schedule is added (new, D-RCV-60)
    Given a completed shadow run of agent "LEGAL_DOC" for case "RW-2026-000901"
    When the outbox row is relayed
    Then rwb.agent.events.v1 carries rwb.agent.AgentRunCompleted.v1 (EV-28), keyed by the case ID, with the retry topic and the .dlt topic, and its envelope carries id, source, type, specversion, time, subject and datacontenttype, with the run ID as its subject
    Then the payload carries run ID, agent_code, agent_version, prompt_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, tokens_in, tokens_out, cost_thb and run_at, and no item, no document ID, no defect reason and no personal field
    Then this document publishes no second event, declares no pack topic, no new table, no migration, no Temporal Schedule and no lake table, extract or credential, because DP-15 and DP-10 are not patterns of this key and no data lake exists
    Then a payload that fails its registry subject is refused before the relay and routed to .dlt with an alert

  Scenario: AC7 The route, the fakes and the error taxonomy are complete (new, D-RCV-60)
    Given the nine sub-tables of section 12 and the gateway-bff route stub of RWB-PLT-N001-CON
    When the document and the five fakes are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then the route is a pass-through of one hop in front of the operations and preserves the JSON and CSV media types, and its name and path are Not specified in the source documents (GAP-0628; ASM-0950)
    Then the error taxonomy is the platform problem response with 401, 403 with MSG-P4-002, 404, 409 with MSG-P7-002 or MSG-P10-003, 422 with MSG-P10-001 or MSG-P10-002 and 503, and no operation adds a code outside it
    Then the fakes rwb-document, rwb-litigation, rwb-case, the model gateway and the route answer every consumed path and payload of this document, every fixture is synthetic, and a drift between a fake and this document fails the contract test
```

**Target reading.** This contract adds no behaviour and no business value. Agent "LEGAL_DOC", the policy versions "P1" and "P2", prompt "PR1", case type "MORTGAGE_CIVIL" with its 9 items, sample "LEGAL-S1" version 1, the 50 and 49 scored cases, the 46 agreeing cases and agreement 0.9200, the review date 2027-03-15, the 60-second timeout, the case "RW-2026-000901" with 14 documents and the refusal codes are the legacy values of RWB-E2-030, copied character for character; the member names are those of TSD P10 Agent runtime v2 T3.1 and the API specification v4. Four elements are settled here and marked where they appear: the run start path, which no source names (ASM-0947); the consumed paths and field names of the boundary (ASM-0944); the six policy members beyond the baseline (ASM-0956); and the route (ASM-0950).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The run start and the run read are the agent runtime's and this key adds no operation of its own; the configuration and evaluation operations are restated from RWB-P10-E1058-CON and RWB-P10-E1061-CON and never redefined | DP-11; DP-13; ASM-0947 |
| BR2 | The `legal-pack-v1` answer carries one item per checklist code with a status, its document IDs and a required defect reason, and only documents the rwb-document contract returned for the same case | Legacy AC1, AC4, AC5; CTL-19; TSD P10 Agent runtime v2 T3.1 DF-AGT-049 |
| BR3 | The documents, their fields and the checklist are consumed from RWB-P5-E2025-CON one hop with the 2 s budget; no table of `rwb_document` is an answer source | DP-01; DP-11; ASM-0944 |
| BR4 | A failed or slow consumed read answers run status TOOL_UNAVAILABLE with fallback true and the reason naming the read, and the case is scored as not run | Legacy AC6; R-UNI-33 |
| BR5 | The mode, the review date, the evaluation run ID, the promotion conditions, the allowed tools and the schema reference are policy data with a version, loaded and then approved by a person other than the loader | Legacy AC3, AC8, AC9; MSG-P7-002; DP-06 |
| BR6 | The score row is the baseline `AgentEvaluation` with the checklist code as its label key, the sample size and the agreement rate at four decimals; a row that does not reproduce its rate is refused | Legacy AC2, BR5; DF-AGT-089, DF-AGT-090, DF-AGT-094 |
| BR7 | Every message is a CloudEvents 1.0 message on `rwb.agent.events.v1`, keyed by the case, validated against its registry subject before the relay and routed to `.dlt` on failure; the pack is never published | DP-09; DP-14; EV-28 |
| BR8 | The contract declares no new table, no migration, no Schedule and no lake artefact, because DP-15 and DP-10 are not patterns of this key and no data lake exists | ADR-018; Owned tables of P10 |
| BR9 | No business value in the contract: the 9 items, the 50 cases, the 0.9200, the date and the timeout are policy and reference rows, and the contract only names them | Template and Rules §R7.2 s17; DP-06; DP-07 |
| BR10 | One base and one topic per service: this contract declares `/api/recovery/agent/v1` and `rwb.agent.events.v1` for rwb-agent and never another service's path or topic as its own | DP-13; DP-14 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The run start, the pack, the boundary reads, the policy payload, the score row, the event, the route and the fakes are described | In review |
| In review | Consumer sign-off | The app story and the Epic 5 pack story accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a query parameter or a payload field is added without removing one | Baselined |
| Baselined | Breaking change | A member of the pack, of the score row, of the policy payload or of the event is removed, renamed or retyped | In review, with the owner of the affected contract |
| Baselined | Drift in a fake or against a baseline | A contract test fails | In review |

These are the states of this document. The states of the run (LOV-AGENT-RUN), of the evaluation (RUNNING, DONE, FAILED) and of the policy version (LOADED, APPROVED, RETIRED) are values of their lists and belong to RWB-P10-E2030-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the run start and read, the pack, the policy payload, the score row, the event, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to an operation or a payload |
| The rwb-document owner | Owns the three reads and the checklist, and signs off the consumed shapes and the field names |
| The rwb-litigation owner | Owns the by-case legal-action read and signs off its shape |
| The rwb-case owner | Owns the case read, the parameters and the lists, and signs off the parameter and list values |
| The app story and the Epic 5 pack story of this key | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the problem response, the naming rule, the outbox library and the route this document reuses |
| Data steward | Confirms that no personal data field is declared in an event or in an answer |

The identity that reads the consumed contracts is the rwb-agent service identity; its name is fixed with the deployment story (DP-02 is not a pattern of this key).

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Run start request | agent "LEGAL_DOC", caseId, evaluationRunId, idempotency key |
| Run answer | id, agent, agentVersion, caseId, outcome, fallback, latencyMs, autonomyMode, guardrailResult, output (the pack and the completeness list), evaluationRunId |
| Pack | items[] with itemCode (the 9 codes of "MORTGAGE_CIVIL"), status PRESENT, MISSING or DEFECT, documentIds[], defectReason when DEFECT; confidence at four decimals |
| Documents read | id, caseId, documentType, writeOnce; the 14 documents of "RW-2026-000901" |
| Fields read | fieldName, fieldValue masked; DF-DOC-014 and DF-DOC-015 |
| Checklist read | the 9 itemCodes of the case type including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF" |
| Legal action read | id, actionType, status; one open action on "RW-2026-000901" |
| Policy request | kind POLICY, agent "LEGAL_DOC", policyVersion "P2", autonomyMode "SHADOW", reviewDate 2027-03-15, evaluationRunId, promotionConditions, allowedTools, outputSchemaRef "legal-pack-v1", timeoutSeconds 60 |
| Policy answer | the version resource of the baseline with status LOADED or APPROVED, approvedBy, validFrom and the review date |
| Score row | labelKey the checklist code, sampleSize 50 or 49, agreementRate 0.9200 for "DEMAND_NOTICE_PROOF"; DF-AGT-089, DF-AGT-090, DF-AGT-094 |
| AgentRunCompleted payload | run ID, agent_code, agent_version, prompt_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, tokens_in, tokens_out, cost_thb, run_at |
| Consumed values | the minimum sample 50 and the promotion check list through the parameters contract; LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS, LOV-AGENT-RUN and LOV-SUBJECT-TYPE through the reference-data contract; the case facts through the case read |

The member types beyond the names the legacy story and TSD P10 Agent runtime v2 T3.1 give - the type of `documentIds`, the member name of the defect reason, the exact type of `confidence` and `agreementRate` beyond four decimals - are Not specified in the source documents (GAP-0628; ASM-0944, ASM-0957). No table of another schema is an answer source: the answer comes from `rwb_agent` and the boundary reads (DP-01).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10). This key adds no operation: the seven operations below are the baselines of RWB-P10-E1058-CON and RWB-P10-E1061-CON restated with the legal narrowing.

| Method | Path | Purpose | Rights | Errors |
|---|---|---|---|---|
| POST | `/api/recovery/agent/v1/agent-runs` | Start one shadow run of "LEGAL_DOC" for a sampled case at the path fixed here; 202 AgentRun | Case record C, scope applied | 401, 403, 404, 409, 422, 503 |
| GET | `/api/recovery/agent/v1/agent-runs/{runId}` | Read the run with its outcome, guardrail result, pack and completeness list (Arch v5 slide 16) | Platform administration R, scope applied | 401, 403, 404, 503 |
| POST | `/api/recovery/agent/v1/admin/agent-samples` | Load sample "LEGAL-S1" version 1; 201 AgentSample with rows 50 | Rules and parameters C | 401, 403, 422, 503 |
| POST | `/api/recovery/agent/v1/admin/agent-evaluations` | Start the evaluation of "LEGAL_DOC" on "LEGAL-S1" version 1; 202 AgentEvaluationRun in status RUNNING | Rules and parameters C | 401, 403, 409 MSG-P10-003, 422 MSG-P10-002, 503 |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations` | List the evaluation runs with their scores and proposals, JSON or CSV | Rules and parameters R | 401, 403, 503 |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report` | Read the report: sampleSize, agreement per item, the not-run cases, cost, latency | Rules and parameters R | 401, 403, 404, 409 MSG-P10-008, 503 |
| POST | `/api/recovery/agent/v1/admin/agent-configs` and `/admin/agent-configs/{versionId}/approve` | Load and approve policy version "P2" with its mode, review date, evaluation run ID, tools and schema reference | Rules and parameters C and A | 401, 403, 404, 409 MSG-P7-002, 422 MSG-P10-001, 503 |

The path of the run start below the base is Not specified in the source documents (GAP-0628; ASM-0947): the sources name the read `GET /agent-runs/{id}` on Arch v5 slide 16 and no start operation, so this document fixes the pair instead of inventing a business value. Errors: 401 no session, 403 no right (MSG-P4-002), 404 an unknown run, version or evaluation, 409 a self-approval or a second evaluation, 422 a failed check or an empty sample, 503 a store or a consumed contract unavailable.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document (RWB-P5-E2025-CON; ASM-0944) | The documents of a case with their type and write-once flag | One hop, 2 s |
| GET | `/api/recovery/document/v1/documents/{documentId}/fields` | P5 rwb-document (RWB-P5-E2025-CON; ASM-0944) | The checked field names and their masked values | One hop, 2 s |
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` | P5 rwb-document (RWB-P5-E2025-CON; ASM-0944) | The 9 itemCodes of case type "MORTGAGE_CIVIL" | One hop, 2 s |
| GET | the by-case legal-action read of rwb-litigation: Not specified in the source documents (GAP-0628; ASM-0944) | S4 rwb-litigation | The open legal action of the case and its type | One hop, 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case (RWB-P3-E2015-CON) | The case facts of DF-CAS-001, DF-CAS-003 and DF-CAS-017 | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case (RWB-P3-E1042-CON) | The minimum scored sample of 50 and the promotion check list in force, with their version (DP-06) | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS, LOV-AGENT-RUN and LOV-SUBJECT-TYPE (DP-07) | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11, ADR-020). A failure or a slow answer maps to TOOL_UNAVAILABLE on the run (BR4). No lake operation and no INT-19 or INT-20 path is consumed; the model endpoint INT-23 is called inside the run, not from this boundary.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` with the retry topic and the `.dlt` topic | P10 | the case ID | run ID, agent_code, agent_version, prompt_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, tokens_in, tokens_out, cost_thb, run_at |

The event is inserted in the outbox in the same transaction as the run row and relayed by the library of RWB-PLT-TE006-CON; it is validated against its registry subject before the relay and a refusal is routed to `.dlt` with an alert. It carries no item, no document ID, no defect reason and no personal field: the pack stays in `agent_run.output` (BR7; ASM-0954). This contract publishes no second event and declares no pack topic.

#### 12.4 Events consumed

None. A run of this key is started by the harness of the evaluation and not by a topic, so no event is consumed. The event-triggered run paths of rwb-agent (`CaseCreated`, `DocumentStored`) belong to RWB-P10-E1059-CON and RWB-P10-E1062-CON and are declared there.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow, one execution per case and evaluation run | `rwb-agent` | Input: agent "LEGAL_DOC", case ID, evaluation run ID, policy version, idempotency key. Output: the run with its mode, its pack, its completeness list and its status; the 60-second policy budget then the rule result (R-UNI-32) |
| AssembleLegalPackInputs | Activity | `rwb-agent` | Input: the case, the legal action, the documents with their masked fields and the checklist. Output: the masked model input and the item list, or the refusal naming the failed read (BR3, BR4) |
| ScoreLegalPack | Activity | `rwb-agent` | Input: the run and the officers' rows of `agent_sample`. Output: one `agent_evaluation` row per item with the sample size and the rate at four decimals (BR6) |

The workflow identity, the queue and the 60-second budget are those of Arch v5 slide 16; the activity names and their members are this contract's and are accepted by RWB-P10-E2030-APP.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this contract: the evaluation is started by RW-COE and a run is started by the harness, never on a cadence, and DP-10 is not a pattern of this key. The retired Quartz scheduler is not replaced by a schedule here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_run | P10 (`rwb_agent`) | The run, its mode, its status, its guardrail result, its pack in `output`, its run-at and its evaluation run ID; no column added |
| agent_policy | P10 (`rwb_agent`) | The versions "P1" and "P2" with mode, review date, evaluation run ID and conditions; no column added |
| agent_prompt | P10 (`rwb_agent`) | Prompt version "PR1" and the schema reference "legal-pack-v1"; no column added |
| agent_sample | P10 (`rwb_agent`) | The labelled rows of "LEGAL-S1" version 1: case, label key and expected value; no column added |
| agent_evaluation_run | P10 (`rwb_agent`) | The evaluation of "LEGAL_DOC" on "LEGAL-S1" version 1, its status and its counts; no column added |
| agent_evaluation | P10 (`rwb_agent`) | One score row per checklist code with the sample size and the agreement rate; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox, inbox and idempotency envelope of the completion event and of the run start (DP-09) |

No new table and no migration: the legacy story states "no new table", and every column these shapes read arrives with RWB-P10-E1058-APP and RWB-P10-E1061-APP, because DP-15 is not a pattern of this key (BR8). No table of another service is declared and no foreign key crosses a schema: `recovery_case`, `legal_action`, `document`, `document_field`, `document_checklist_item`, `parameter_catalog`, `parameter_value`, `reference_row` and `reference_version` are P3, S4 and P5 and are reached through their contracts (DP-01). No lake table is declared, because no data lake exists.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document WireMock | The three reads: 14 documents for "RW-2026-000901" with their types and the write-once flag, the masked fields, the 9 itemCodes of "MORTGAGE_CIVIL"; a 503 for "RW-2026-000903"; a document "D-7001" of another case; a delay beyond 2 s | Contract tests, app story |
| rwb-litigation WireMock | One open legal action for "RW-2026-000901", a case with no action, a delay beyond 2 s | Contract tests, app story |
| rwb-case WireMock | The case facts of three cases, the minimum sample 50 and the promotion check list, the six lists, an unknown case, a delay beyond 2 s | Contract tests, app story |
| Model gateway fake (INT-23) | A valid legal-pack answer; an answer naming a document of another case; an answer with no status for "MORTGAGE_DEED"; silence for 61 seconds | Contract tests, app story |
| gateway-bff route stub | A pass-through in front of the operations, one hop, JSON and CSV media types preserved, the refusal passed through unchanged | Contract tests, app story |

The outbox stub, the workflow kit stub and the access guard stub are the platform's and are used but not declared here. Every fixture is synthetic and holds no personal data.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 7 provided, 7 consumed | The run start and read, the sample load, the three evaluation operations and the two configuration operations, restated from their baselines; the three document reads, the legal-action read, the case read, the parameters and the lists consumed, one hop and 2 s each |
| Kafka | 1 published, 0 consumed | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` with its retry and `.dlt` topics, keyed by the case ID; no pack topic |
| Temporal | 1 workflow, 2 activities | AgentRunWorkflow with AssembleLegalPackInputs and ScoreLegalPack on the queue `rwb-agent` |
| File | 1 component | The sample file of "LEGAL-S1" version 1 is read once by the sample operation; no other file is read or written |

### 13. Solution plan

**Deliverables.** `contract/agent-run.yaml` (the run start and read with their statuses and members), `contract/legal-pack-v1.yaml` (the items, their statuses, the document IDs and the defect reason), `contract/agent-legal-boundaries.md` (the three document reads, the legal-action read, the case read, the parameters and the lists with their budgets and the failure mapping), `contract/agent-legal-policy.md` (the six policy members, the LOADED and APPROVED outcomes and the two refusals), `contract/agent-legal-evaluation.md` (the restated operations and the score row), `contract/agent-run-completed.asyncapi.yaml` (the event, its envelope, subject and `.dlt` route) and the five WireMock mappings with their synthetic fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` | Own schema `rwb_agent`; other services through their contracts | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON for the app story; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON for the app story; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-28, outbox | Outbox and inbox library; the owner's topic; CloudEvents | H RWB-PLT-TE006-CON for the app story; none here |
| DP-13 | `/api/recovery/v1` | `/api/recovery/agent/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story; none here |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts it names are those its consumer RWB-P10-E2030-APP adds, and the C dependencies of the key are the published contracts of rwb-case and rwb-document.

**Build steps**

1. Write the run start and read contract with their statuses, their members and the idempotency rule.
2. Write `legal-pack-v1` with the items, the three statuses, the document IDs and the required defect reason, and state that itemCode comes from the P5 checklist.
3. Write the boundary document: the three document reads, the legal-action read, the case read, the parameters and the lists, each one hop with the 2 s budget, and the TOOL_UNAVAILABLE mapping.
4. Write the policy document with the six members beyond the baseline, the LOADED and APPROVED outcomes and the two refusals.
5. Write the evaluation document with the restated operations, the score row, the 0.9200 on 46 of 50 and the not-run count of 49.
6. Write the AsyncAPI document with its envelope, key, subject and `.dlt` route, and state that no pack member is published.
7. Build the five WireMock mappings and their synthetic fixtures, including the 503, the foreign document and the silent model.
8. Add the contract tests of section 16, including the drift test between each fake and this document.
9. State the absence rules and tag the baseline for the app story and the Epic 5 pack story.

**Done when.** The six contract files validate in the pipeline, the seven contract tests pass, the five fakes answer every consumed path and payload, no sub-table declares a new table, a migration, a Schedule or a lake artefact, and the app story has accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | The policy version fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | The evaluation is started on a sample with no labelled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | The same evaluation is already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P10-008 | The report of a run that is not DONE is requested | The report of {agent} on sample {sample} is not ready. Wait for the evaluation to finish. |
| MSG-P7-002 | The loader approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |

MSG-P10-001, MSG-P10-002, MSG-P7-002 and MSG-P4-002 are the legacy messages of RWB-E2-030, copied character for character; MSG-P10-003 and MSG-P10-008 are the messages of the evaluation baseline. This contract adds no message.

### 15. Screens and states

None in this story. The contract serves the agent monitor SCR-46 indirectly and the score read of the evaluation; the monitor belongs to RWB-P10-E1063-CON and the score read to RWB-P10-E2030-APP. The contract fixes no screen field, no order and no masking rule beyond the masked field read, and it returns no pack to a screen (BR2). The route in front of the operations is a pass-through of one hop (DP-19), and its name and path are Not specified in the source documents (GAP-0628; ASM-0950).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E2030-CON-01 | AC1 | Contract | The run start and read validated against their schema: case "RW-2026-000901", 202, the five run statuses, the repeat of one idempotency key, 404 and 403 |
| TC-P10-E2030-CON-02 | AC2 | Contract | `legal-pack-v1`: the 9 itemCodes of "MORTGAGE_CIVIL", PRESENT, MISSING and DEFECT, the required defect reason, the foreign document "D-7001" and an item with no status |
| TC-P10-E2030-CON-03 | AC3 | Contract | The three document reads, the legal-action read and the case read; a 503 and a delay beyond 2 s answering TOOL_UNAVAILABLE |
| TC-P10-E2030-CON-04 | AC4 | Contract | Policy "LEGAL_DOC" "P2" with review date 2027-03-15, LOADED, APPROVED, 409 MSG-P7-002, 422 with no review date and 422 for L1 at 49 cases |
| TC-P10-E2030-CON-05 | AC5 | Contract | Evaluation on "LEGAL-S1" version 1: 202 RUNNING, 409 MSG-P10-003, 422 MSG-P10-002, report with 50 and 49, 0.9200 for "DEMAND_NOTICE_PROOF" and 409 MSG-P10-008 |
| TC-P10-E2030-CON-06 | AC6 | Contract | The EV-28 envelope, its subject and payload, the `.dlt` route, a payload that fails its subject, and the absence of a pack member, a table, a migration or a Schedule |
| TC-P10-E2030-CON-07 | AC7 | Contract | The nine sub-tables present, the route stub of RWB-PLT-N001-CON, the error taxonomy and the drift test of the five fakes |

Every case is Contract level because each tests the artefact and its fakes, not a business outcome. The cases are written by this story and carry no legacy ID; the legacy cases of the key are kept by the app story.

### 17. Guardrails

- No business value in the contract: the 9 items, the 50 cases, the 0.9200, the review date and the timeout are data with a version (BR9).
- No personal data in an event, a workflow input, a fake or a log; the field values crossing the boundary are masked at their source.
- No read of another service's tables: the documents, the fields, the checklist, the legal action and the case come through their contracts (BR3).
- No new table, no migration, no Schedule and no lake artefact; the pack is returned by no screen and published on no topic (BR7, BR8).
- The contract fakes of this story are synthetic and hold no production case, document or officer pack.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested | Business Requirements Program, section 5.11 | FEAT-AGT-09 | 8.2 Instruct and file | R-LIT-16, R-LIT-17, R-UNI-33 | TC-P10-E2030-CON-01, TC-P10-E2030-CON-02, TC-P10-E2030-CON-03 |
| REQ-DCM-011 | The document checklist of a case type is reference data, and every pack is checked against it | Business Requirements Program, section 5.11 | FEAT-AGT-09 | 8.2 Instruct and file | R-LIT-16, CTL-19 | TC-P10-E2030-CON-02, TC-P10-E2030-CON-05 |

The contract slice serves the same two requirements as the app story, because it fixes the shapes through which they are met. It adds no requirement of its own.

### 19. Out of scope

- The behaviour of the agent, the scorer and the validator (RWB-P10-E2030-APP).
- The agent runtime, the sample and the configuration baselines, which this document restates and never redefines (RWB-P10-E1058-CON).
- The evaluation operations, the report and the messages of the harness (RWB-P10-E1061-CON).
- The agent monitor, its reads and its metrics (RWB-P10-E1063-CON and RWB-P10-E2031-CON).
- The Epic 5 pack assembly and the officer verification in the litigation flow, and the integration proof against the real P5, S4 and P3 services.
