# RWB-P10-E2029-CON Deviation screening agent evaluation and L1 on one segment [E3b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2029-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P10-E2029-CON-16); the squad sizes it at refinement |
| Patterns applied | DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | rwb-document and the call-note field of rwb-source-data: Not specified in the source documents (GAP-1822), to be confirmed by the owners before the shadow screening test; no copy of a document is held in schema rwb_deviation |
| Contract version | v1, the path `/api/recovery/agent/v1` |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-007, FR-P10-012, FR-P10-013, FR-P10-014) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract slice of RWB-E2-029 for rwb-agent. It fixes the screening narrowing of the evaluation start and the evaluation report on `/api/recovery/agent/v1` (DP-13, restated from RWB-P10-E1061-CON and never redefined), the segment-eligibility and L1 decision request and outcome with the two segment members and the approval, the score row shape per code with the counts, precision and recall, the decision-record mapping and the idempotency of one feedback per run and item (DP-03), the event contracts on `rwb.agent.events.v1` and on `rwb.decision-record.v1` with their retry and `.dlt` topics (DP-09), the parameters and lists of rwb-case (DP-06, DP-07), the ledger and ACE facts reached through rwb-source-data (DP-05), the one-hop reads with the 2 s budget (DP-11), the gateway-bff route (DP-19) and the fakes. Because there is no data lake, the contract declares no lake table, no extract, no lake credential, no INT-19 or INT-20 path and no daily agent table. It builds no business behaviour and adds no migration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the screening key fixed as a contract on Day 1: the evaluation start and the report narrowed to agent "SCREENING" on sample "SCREEN-S2" version 1, the policy payload with mode L1, segment MORTGAGE and region BKK and its approval, the score row shape per code X1 to X7, the mapping of a confirmation and a rejection to one decision record with their idempotency, the event contracts of the run completion and of the decision record with the retry and `.dlt` topics, the gateway-bff route, the error taxonomy and the fakes**, so that **the app story, the S8 and P7 slices of this key and the integration copy build against one agreed, testable shape without waiting for the evaluation to run, and no reader is offered a lake artefact or a daily agent table that does not exist**.

### 2. Business rationale

The legacy key was written against objects inside one deployment: the evaluation wrote `agent_evaluation` rows beside the policy row, the panel filtered proposals in process, the decision log writer of the same deployment wrote the rejection, the deviation interface was a Java call, and the case and the ledger were read from the same schema. In the target each of those is a boundary:

- The evaluation harness and the score rows are rwb-agent's own tables, and the operations that start and report an evaluation are already baselined by RWB-P10-E1061-CON; this key narrows them and adds no member (DP-01, DP-11).
- The segment and the autonomy mode are columns of the approved policy row, so the L1 decision is a configuration version and its approval, not code (DP-06).
- The case, the deviation and the ledger are P3, S8 and P1; the record type and the central ledger are P7's, and each service writes its own record through the local library on `rwb.decision-record.v1` (DP-03, DP-05).
- The run and score facts leave as CloudEvents on `rwb.agent.events.v1` with the platform retry and `.dlt` topics (DP-09).
- The data lake is removed by Architecture v5 (ADR-018), so the contract names no lake table, no extract and no daily agent aggregate; the aggregate of the monitoring story is a read of its own.

Contract-first only works if the seam is written once. Here it is small and load-bearing: one evaluation request and one report whose row carries the legacy figures, one policy payload that names the segment and one read that answers it, one feedback write whose record and idempotency are fixed, two event payloads, one route, one error taxonomy and one fake set. With that agreed on Day 1, the app story builds the evaluator, the resolver, the filter and the handler against the fakes; the S8 slice takes the raise with `raisedBy` "SCREENING_AGENT" and the refusal of a second confirmation; the P7 slice takes the record this key maps; and RWB-ITG-W2 proves the same behaviour across the real services. Without it, each caller invents its own score row, the report and the panel drift apart, and a confirmed deviation loses its record.

This story defines the provided side on the agent base and the consumed side of the key, and never restates what another owner holds: the evaluation operations are RWB-P10-E1061-CON's, the run and proposal shapes are RWB-P10-E1062-CON's, the panel and feedback operations are RWB-P10-E2028-CON's, the configuration operations are RWB-P10-E1058-CON's, and the parameters and lists are rwb-case's (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the base, the topic and the event names follow the platform rule and not a local choice (§R4; DP-13, DP-14).
- The CloudEvents 1.0 envelope and the platform problem response are the baseline; this document narrows them where it must and says so.
- RWB-P10-E1058-CON is in force: the policy and prompt resources, the configuration operations, the approval and the run resource; this story narrows the policy payload with the two segment members rather than redefining it.
- RWB-P10-E1061-CON is in force: the evaluation start, the list and the report, their statuses and their messages; this story restates them with the screening narrowing and adds no operation.
- RWB-P10-E1062-CON is in force: the run and proposal shapes and the agent topic with its retry and `.dlt` topics. RWB-P10-E2028-CON is in force: the case agent-outputs read, the feedback operation and the `agent_feedback` resource.
- RWB-PLT-E1027-CON is published: the decision-record library and the shared topic, with the record fields, the hash chain and the idempotent write (DP-03). RWB-PLT-TE006-CON is published: the envelope, the relay, the retry topics and the `.dlt` rule. RWB-PLT-E1042-CON and RWB-PLT-E1043-CON publish the parameters and reference-data client libraries, and RWB-PLT-N001-CON the route contract and its stub.
- The rwb-case contracts are published: `GET /api/recovery/case/v1/cases/{caseId}` (RWB-P3-E2015-CON), the parameters (RWB-P3-E1042-CON) and the lists (RWB-P3-E1043-CON).
- The rwb-deviation raise and open-deviation reads are published shapes; the raise returns the deviation ID and the entry ID the feedback maps (ASM-0931).
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W2.

### 4. Flow

1. Draft the evaluation start and report as this key narrows them: agent "SCREENING", sample "SCREEN-S2" version 1, the statuses RUNNING, DONE and FAILED, the refusal codes and the report members.
2. Fix the score row shape: one row per code X1 to X7 with the label key, sample size 500, the true positives, false positives and false negatives, precision and recall at four decimals, and the legacy X1 figures 41, 4 and 5 giving 0.9111 and 0.8913.
3. Fix the segment-eligibility and L1 decision request: `autonomyMode` "L1", `segmentProductGroup` MORTGAGE, `segmentRegionCode` BKK, the prompt version, the evaluation run ID and the promotion conditions, its LOADED outcome, the approval with MSG-P7-002 and the read that answers the segment of a case.
4. Fix the decision-record mapping: an accepted confirmation stores the entry ID the raise returns; a rejection writes one record through the library with decision "X6", agent version "SCREENING@P2/PR2", final call REJECTED and the reason, and only then the feedback; the one-feedback rule and its key are declared.
5. Declare the two events: `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` with the retry and `.dlt` topics and the run facts including the two segment members, and DecisionRecorded on `rwb.decision-record.v1` with the record fields of the library.
6. Fix the route, the parameter and list reads and the boundary of 12.2, one hop and a 2 s budget each, and name the values the contract expects.
7. Write the five fakes: rwb-case, rwb-deviation, the decision-record library, the model gateway and the route, each with the answers, errors and timings this key's tests need.
8. State the absence rule: no lake table, no extract, no lake credential, no INT-19 or INT-20 path and no daily agent table.
9. Publish the nine sub-tables and the contract tests, and tag the baseline for the app story, the S8 and P7 slices and the integration copy.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of the report, the score row or the policy payload drifts from this document: a renamed member, a dropped count, a retyped figure | The contract test fails and the merge is blocked | None | AC1, AC2, AC3 |
| X2 | A caller sends a request the contract does not allow: an empty reason on a rejection, a sample with no labelled row, a second evaluation of the same version | The operation refuses with 422 or 409 and names the member or the state; nothing is written | MSG-P7-005, MSG-P10-002, MSG-P10-003 | AC1, AC4 |
| X3 | The contract declares a lake table, an extract, a lake credential, an INT-19 or INT-20 path, or a daily agent table | The review refuses the document: no lake exists and the aggregate belongs to another story | None | AC7 |
| X4 | A payload gains a personal field or fails its registry subject | The data-steward review and the contract test refuse it; a produced message that fails is routed to `.dlt` with an alert | None | AC5 |
| X5 | A restated operation drifts from its baseline | The contract test fails and this document is aligned, because the baseline is the owner | None | AC1, AC3, AC4 |
| X6 | The record cannot be written on a rejection, or the route refuses the read | The operation answers 503 and nothing is stored; the refusal is passed through the route unchanged | MSG-P7-003 | AC4, AC6 |
| X7 | A field-level detail of a consumed operation, a payload member or the route is missing from the source material | The element carries the placeholder, one gap row and one assumption row, and the fake is written to the assumed shape | None | AC2, AC6, AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the agent runtime, evaluation, run and panel baselines, the record library, the outbox library and the rwb-case and rwb-deviation contracts as published |
| Negotiable | Field-level detail of the consumed operations, the page size of the evaluation list and the member types are settled with their owners; the narrowing, the score row, the segment payload, the record mapping, the payloads and the route are fixed here |
| Valuable | Unblocks the app, S8, P7 and integration slices of this key on Day 1 and gives every reader of a screening score one shape |
| Estimable | Two provided operations restated, two configuration operations narrowed, two panel operations restated, two events, two consumed boundaries and five fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact - the contract file, the payload, the fake, the document - and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening evaluation and L1 contract slice for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the agent runtime contract of RWB-P10-E1058-CON and the evaluation contract of RWB-P10-E1061-CON are in force
    Given the decision-record library of RWB-PLT-E1027-CON and the outbox library of RWB-PLT-TE006-CON are in force

  Scenario: AC1 The evaluation start and report are narrowed, not redefined (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When RW-COE starts, then reads the evaluation of agent "SCREENING" on sample "SCREEN-S2" version 1
    Then POST /api/recovery/agent/v1/admin/agent-evaluations takes the members agent, sampleCode, sampleVersion and approaches and answers 202 with an AgentEvaluationRun in status RUNNING carrying agent "SCREENING", sampleCode "SCREEN-S2", sampleVersion 1 and its evaluationId
    Then the same operation answers 422 with MSG-P10-002 for a sample with no labelled row and 409 with MSG-P10-003 for a second evaluation of the same agent and sample version while one is RUNNING
    Then GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report answers AgentEvaluationReport with sampleSize 500, the three versions, agreementByLabel[], failureCounts, totalCostThb, costPerCaseThb, latencyP50Ms, latencyP95Ms, 409 with MSG-P10-008 for a run that is not DONE and 404 for an unknown run
    Then both operations are one hop on /api/recovery/agent/v1 with the 2 s client budget and both are the baseline shape restated, so this document adds no member and no operation

  Scenario: AC2 One score row per code carries the counts, precision and recall (new, D-RCV-60)
    Given evaluation run "EV-SCREEN-S2-001" of agent "SCREENING" on sample "SCREEN-S2" version 1 in status DONE
    When its report is read
    Then the report names one score row per code X1 to X7, each with labelKey, sampleSize 500, truePositive, falsePositive, falseNegative, precisionValue and recallValue at four decimals
    Then X1 with 41 true positives, 4 false positives and 5 false negatives answers precisionValue 0.9111 and recallValue 0.8913, and X4 answers recallValue 0.6000
    Then the five members beyond the baseline AgentEvaluation are the columns DF-AGT-091 to DF-AGT-096 of TSD P10 Agent runtime v2 T3.1, and a row whose counts do not reproduce its precision and recall fails the contract test
    Then the score row names no personal field, no customer identifier and no account number

  Scenario: AC3 The segment-eligibility and L1 decision request and outcome are fixed (new, D-RCV-60)
    Given the policy resource baselined in RWB-P10-E1058-CON
    When RW-COE loads policy "SCREENING" version "P2" with mode "L1" for segment MORTGAGE and BKK and RW-RISK approves it with a valid-from date
    Then the payload carries kind POLICY, agent "SCREENING", policyVersion "P2", autonomyMode "L1", segmentProductGroup "MORTGAGE", segmentRegionCode "BKK", promptVersion "PR2", evaluationRunId and promotionConditions, and answers 201 with an AgentConfigVersion in status LOADED
    Then POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve answers 200 with status APPROVED, approvedBy and validFrom, 404 for an unknown version and 409 with MSG-P7-002 when the approver loaded the version
    Then GET /api/recovery/agent/v1/admin/agent-configs answers the versions with their segment, so a case whose product group and region match the approved row is L1, every other case is SHADOW, and a row with no segment applies to all cases in SHADOW
    Then eligibility is answered from the approved row and the case facts read through the rwb-case contract, and never from a table of another service

  Scenario: AC4 The decision-record mapping and the feedback idempotency are fixed (new, D-RCV-60)
    Given the panel and feedback operations baselined in RWB-P10-E2028-CON and the decision-record library of RWB-PLT-E1027-CON
    When the owner confirms one proposal and rejects another
    Then POST /api/recovery/agent/v1/agent-runs/{runId}/feedback takes AgentFeedbackRequest with itemKey the code, verdict ACCEPTED or REJECTED and reason required for REJECTED, and answers 422 with MSG-P7-005 for an empty reason
    Then a confirmation stores verdict "ACCEPTED" with decision_log_id set to the entry ID returned by the rwb-deviation contract, and the answer carries that ID for the item
    Then a rejection writes one record through the library with decision "X6", agent version "SCREENING@P2/PR2", final call "REJECTED" and the reason, in the same transaction as the feedback row, and answers 503 with MSG-P7-003 and no agent_feedback row when the record cannot be written
    Then one feedback exists per run and item, the pair (agent_run_id, item_key) is unique, and a second verdict is refused with 409 and MSG-GEN-004

  Scenario: AC5 The two event contracts are declared with their retry and .dlt topics (new, D-RCV-60)
    Given a run of agent "SCREENING" for case "RW-2027-000801" in mode "L1" on 2027-01-26
    When the run completes and a rejection is recorded
    Then rwb.agent.events.v1 carries rwb.agent.AgentRunCompleted.v1, keyed by the case ID, with the retry topic and the .dlt topic, and its envelope carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype, with the run ID as its subject
    Then the payload carries run ID, agent_code, agent_version, prompt_version, model_version, case_id, autonomy_mode, segment_product_group, segment_region_code, trigger_event, status, fallback, confidence, latency_ms, tokens_in, tokens_out, cost_thb and run_at
    Then rwb.decision-record.v1 carries DecisionRecorded for the rejection, inserted by the library in the same transaction as the record and the feedback, with the record fields and its hash chain
    Then a payload that fails its registry subject is refused before the relay and routed to .dlt with an alert, and no personal data is carried

  Scenario: AC6 The route, the fakes and the error taxonomy are complete (new, D-RCV-60)
    Given the contract section of this story and the gateway-bff route stub of RWB-PLT-N001-CON
    When the nine sub-tables and the five fakes are reviewed
    Then each of 12.1 to 12.9 is present, names its owner and writes None where it is empty
    Then the gateway-bff route is a pass-through of one hop in front of the operations, preserves the JSON and CSV media types, and its route name and path are Not specified in the source documents (GAP-0626; ASM-0937)
    Then the error taxonomy is the platform problem response with 401, 403 with MSG-P4-002, 404, 409 with MSG-GEN-004, MSG-P7-002 or MSG-P10-003, 422 with MSG-P7-005, MSG-P10-001 or MSG-P10-002 and 503 with MSG-P7-003, and no operation adds a code outside it
    Then the fakes rwb-case, rwb-deviation, the decision-record library, the model gateway and the route answer every consumed path and payload of this document, and a drift between a fake and this document fails the contract test

  Scenario: AC7 The contract declares no lake artefact and no daily agent table (new, D-RCV-60)
    Given the contract section and the schema reference of this story
    When the document is reviewed against the Ownership Map and the no-lake rule
    Then no sub-table declares a lake table, an extract, a lake credential, an INT-19 or INT-20 path, or a daily agent table, because no data lake exists and the daily aggregate belongs to RWB-P10-E2031-CON
    Then the only tables named are the agent tables of rwb_agent and the platform outbox, inbox and idempotency tables, and every other value is reached through its owner
    Then no migration and no column is declared here: the segment, floor, evaluation and promotion columns are created by the earlier P10 stories, because DP-15 is not a pattern of this key
    Then every fixture is synthetic and no production case, complaint note, document or score row is copied into a fake

  Scenario: AC8 The twelve business rules are proved against the contract artefacts (new, D-RCV-60)
    Given the twelve business rules BR1 to BR12 of section 8
    When the contract file, the two event schemas, the table list and the fakes of this story are read against them
    Then each of BR1 to BR12 is proved by a contract test of section 16, at the boundary or in the guardrails where the rule is an architecture constraint, and never against a business outcome
    Then a rule restated from a baseline is proved as a narrowing only, and a drift is corrected in its baseline
```

**Target reading.** This contract adds no behaviour and no business value. Agent "SCREENING", the policy versions "P1" and "P2" with prompt "PR2", the segment MORTGAGE and BKK, the floor 0.80, sample "SCREEN-S2" version 1, the 500 cases, the codes X1 to X7, the X1 counts 41, 4 and 5, the precision 0.9111 and recall 0.8913, the recall 0.6000, the condition "recall at least 0.75 for every code", the case "RW-2027-000801" and the date 2027-01-26 are the legacy values of RWB-E2-029, copied character for character, and the score-row keys are the field names of TSD P10 Agent runtime v2 T3.1 (DF-AGT-089 to DF-AGT-096). Four elements are settled here and marked where they appear: the five score-row members beyond the baseline `AgentEvaluation` (ASM-0941); the two segment members and the run facts on the completion payload (ASM-0940); the decision-record mapping and the one-feedback pair (ASM-0942); and the route in front of the operations (GAP-0626; ASM-0937).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The evaluation is two operations restated from their baseline - start and report - with the screening narrowing, and no caller embeds the harness or reads `rwb_agent` | DP-11; DP-13; RWB-P10-E1061-CON; legacy section 12 |
| BR2 | The report carries one score row per code X1 to X7 with the sample size, the counts, precision and recall at four decimals, and a row that does not reproduce its ratios is refused | Legacy AC1; TSD P10 T3.1 DF-AGT-090 to DF-AGT-096 |
| BR3 | The L1 decision is a policy version with `autonomyMode` "L1" and the two segment members, loaded LOADED and approved with a valid-from date by a person other than the loader | Legacy AC1, section 10; MSG-P7-002; LOV-CONFIG-STATUS |
| BR4 | Segment eligibility is answered from the approved row and the case facts read through the rwb-case contract; a case outside the segment is SHADOW and no row of another service is read | Legacy BR1; DP-01; DP-06 |
| BR5 | A confirmation stores the entry ID the rwb-deviation contract returns, and a rejection writes one record through the library before its feedback, so record and feedback are one transaction or neither | Legacy AC2, AC4, AC9; R-UNI-39; DP-03 |
| BR6 | One feedback exists per run and item, and a second verdict is refused with 409 and MSG-GEN-004 | Legacy section 12; legacy AC8 |
| BR7 | Every message is a CloudEvents 1.0 message on the owner's topic, keyed by the case ID, validated against its registry subject before the relay and routed to `.dlt` on failure | DP-09; DP-14 |
| BR8 | The contract declares no data lake and no daily agent table: the aggregate belongs to RWB-P10-E2031-CON and no lake table, extract, credential or path is named | ADR-018; DP-17 ruling |
| BR9 | The parameters, the eight lists and the segment values are read from rwb-case at run time with their version and never written in the contract as values | DP-06; DP-07 |
| BR10 | Every consumed call and every provided operation is one hop with a 2 s client budget on the base of its owner | DP-11; DP-13; ADR-020 |
| BR11 | A restated operation is never redefined: a drift is corrected in its baseline, and this document only narrows | DP-01; §R3 precedence |
| BR12 | The panel read and the verdict are reached through the gateway-bff route, which passes requests and refusals through unchanged | DP-19; ADR-019 |

### 9. State transitions

The policy version, which carries the L1 decision:

| From | Event | Condition | To |
|---|---|---|---|
| None | RW-COE loads the version | The file passes every check, including the condition on the named evaluation | LOADED |
| LOADED | RW-RISK approves it | The approver is not the loader | APPROVED, with approvedBy and validFrom |
| LOADED | A later version is approved | The new version takes effect on its valid-from date | RETIRED |
| LOADED | The condition fails on the named evaluation | AC10 of the app story | Refused; the version in force is unchanged and no row exists |

The evaluation run: RUNNING on the start, DONE when every labelled row is scored, FAILED when the harness stops; a report is answered only for DONE (409 MSG-P10-008 otherwise). The feedback row: none before the verdict; ACCEPTED with the entry ID the raise returns; REJECTED with the entry ID the library returns, written after the record; no row when the record cannot be written (503 MSG-P7-003) or the reason is empty (422 MSG-P7-005).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns this contract, its nine sub-tables and its fakes, and publishes them on Day 1 |
| RW-COE | Loads a policy version, a prompt version and a sample, and starts an evaluation (Rules and parameters C) |
| RW-RISK | Approves a loaded version (Rules and parameters A) and may not approve its own load |
| RW-CONDUCT | Reads scores and reports (Rules and parameters R) |
| The case owner | Sends a verdict through the feedback operation (Case record U) |
| rwb-deviation (S8) | Owns the raise, the deviation and its entry; this key fixes only the members it consumes |
| rwb-decision (P7) | Owns the central ledger, the sealing and the record fields of the library |
| rwb-case (P3) | Owns the case, the owner check, the parameters and the lists |
| rwb-source-data (P1) | Owns the interaction ledger and the ACE views |
| No role | Redefines a restated operation, names a lake artefact or a daily agent table, or declares a migration here |

The login and the agent identity behind the run are Not specified in the source documents (GAP-0626; ASM-0930). The separation of duty between loader and approver is the one fixed by RWB-P10-E1061-CON and is not restated as a rule of its own.

Each REST operation of this contract is checked by the rwb-access authorise check (DP-08) before it runs; this contract names the check and does not redefine it.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-AGT-070 to DF-AGT-085 | agent_evaluation_run (P10 `rwb_agent`) | all fields | Contract shape: the evaluation run and its statuses |
| DF-AGT-086 to DF-AGT-096 | agent_evaluation (P10 `rwb_agent`) | all fields | Contract shape: one score row per code, with the counts, precision and recall |
| DF-AGT-001 to DF-AGT-025 | agent_policy (P10 `rwb_agent`) | all fields | Contract shape: the L1 decision, the segment members and the approval |
| DF-AGT-026 to DF-AGT-035 | agent_prompt (P10 `rwb_agent`) | all fields | Contract shape: the prompt version "PR2" bound to the policy |
| DF-AGT-061 to DF-AGT-069 | agent_sample (P10 `rwb_agent`) | all fields | Contract shape: the labelled sample "SCREEN-S2" version 1 |
| DF-AGT-097 to DF-AGT-102 | agent_feedback (P10 `rwb_agent`) | all fields | Contract shape: the verdict, the item key and the entry ID |
| DF-AGT-036 to DF-AGT-060 | agent_run (P10 `rwb_agent`) | the run facts of the completion payload | Contract shape: the event payload |
| DF-CAS-037, DF-CAS-038, DF-CAS-040 | deviation (S8) | case_id, deviation_code, raised_by | Read shape of the raise answer, through the owner |
| DF-ACE-193 | v_ace_valuation (P1) | appraisal_date | Read through the owner, for the X7 input |

Every field is a column of a P10 table in `rwb_agent` or a member of a shape another owner publishes, copied from TSD P10 Agent runtime v2 T3.1 and the Logical Data Model; this document declares no new column and no migration (GAP-0626; ASM-0938). The payload of the completion event carries IDs and facts only and no personal field.

### 12. Contract

Open values at the contract. Each is carried to the named check and nothing is built against it until then:
- Harness environment, SCREEN-S2 fixture pack, Enterprise AI test profile for SCREENING, evidence format and retention, and the wave 2 release gate: Not specified in the source documents (GAP-0411). Agreed at the wave 2 entry check.
- The rwb-deviation (S8) raise operation: method, path, answer resource, refusal codes, and the members of its request and answer: Not specified in the source documents (GAP-0626). Agreed at the wave 2 contract freeze.
- The rwb-decision operation that reads a sealed decision-log entry, and its members: Not specified in the source documents (GAP-2194). Agreed at the wave 2 contract freeze.
- The five score-row members beyond the baseline AgentEvaluation: Not specified in the source documents (GAP-2194). To be confirmed with the data steward.
- The run facts and the two segment members of rwb.agent.AgentRunCompleted.v1, and the gateway-bff route name and path: Not specified in the source documents (GAP-2194). Fixed in the gateway-bff contract.
- The decision-log append path, the evaluation and run reads, the case-less promotion variant, and the rwb-decision login: Not specified in the source documents (GAP-2402). Agreed at the wave 2 contract review. Until then the fakes follow the assumed shapes of this section.
- The rwb-agent login, the S8 raise story, the three parameter keys of rwb-case, the gateway-bff route and the Flyway position of rwb_agent: Not specified in the source documents (GAP-2193). The story uses placeholders and builds no code value.

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10). Two operations are restated from their baselines for the screening slice, and two are narrowed configuration operations. None is new here.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/admin/agent-evaluations` | Start the evaluation of agent "SCREENING" on "SCREEN-S2" version 1; 202 AgentEvaluationRun in RUNNING; 422 MSG-P10-002 on a sample with no labelled row; 409 MSG-P10-003 while one is RUNNING | Rules and parameters C | Idempotency-Key header |
| GET | `/admin/agent-evaluations/{evaluationId}/report` | Read the report: sampleSize 500, agreementByLabel[], failureCounts, cost, latency, the three versions; 409 MSG-P10-008 when not DONE | Rules and parameters R | Not applicable |
| POST | `/admin/agent-configs` | Load policy "SCREENING" version "P2" with `autonomyMode` "L1", `segmentProductGroup` MORTGAGE, `segmentRegionCode` BKK, prompt "PR2", the evaluation run and the promotion conditions; 201 LOADED; 422 MSG-P10-001 on a failed check | Rules and parameters C | Idempotency-Key header |
| POST | `/admin/agent-configs/{versionId}/approve` | Approve the loaded version; 200 APPROVED with approvedBy and validFrom; 409 MSG-P7-002 when the approver loaded it | Rules and parameters A | Idempotency-Key header |
| GET | `/admin/agent-configs` | Read the versions with their segment, so eligibility is answered from the approved row | Rules and parameters R | Not applicable |
| GET | `/cases/{caseId}/agent-outputs` | The screening narrowing of the panel read of RWB-P10-E2028-CON: `proposals[]` with code, reasons, sources, the preceding contact, confidence, lowConfidence and feedback; no screening output for a case with no L1 run | Case record R | Not applicable |
| POST | `/agent-runs/{runId}/feedback` | The verdict on one item, with itemKey the code, verdict ACCEPTED or REJECTED and a reason required for REJECTED; 422 MSG-P7-005, 409 MSG-GEN-004, 503 MSG-P7-003 | Case record U | Idempotency-Key header; one feedback per run and item |

Errors are the platform problem response: 401 no session, 403 with MSG-P4-002, 404 an unknown case, run or version, 409 with MSG-GEN-004, MSG-P7-002 or MSG-P10-003, 422 with MSG-P7-005, MSG-P10-001 or MSG-P10-002, 503 with MSG-P7-003. No operation adds a code outside this set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case (RWB-P3-E2015-CON) | The case facts of eligibility: product group, region and status | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case (RWB-P3-E1042-CON) | The floor 0.80, the segment values and the promotion condition, read at run time (DP-06) | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | LOV-DEVIATION, LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-FEEDBACK, LOV-PRODUCT, LOV-REGION, LOV-RAISED-BY (DP-07) | One hop, 2 s |
| GET | `/api/recovery/deviation/v1/deviations?caseId=` | S8 rwb-deviation | The open deviations, so a code already open is not offered; the case-record read has no recorded owner and is an open question for the S8 solution architect, settled in the S8 contract story (GAP-1818) | One hop, 2 s |
| POST | the raise of rwb-deviation: Not specified in the source documents (GAP-0626; ASM-0931) | S8 rwb-deviation | Assumed members, not specified in the source documents (GAP-0626; ASM-0931): the request members caseId, deviationCode, reason, documentIds, raisedBy and agentRunId; the answer members deviationId and decisionLogEntryId | One hop, 2 s |
| GET | the interaction-ledger read of rwb-source-data: Not specified in the source documents (GAP-0626; ASM-0936) | P1 rwb-source-data | The preceding contact of a proposal and the ACE facts of X7 (DP-05), read only through this contract and never from an ACE view or table; the P1 field list is Not specified in the source documents (GAP-1816), confirmed with P1 before the wave 2 system test | One hop, 2 s |
| GET | the sealed entry read of rwb-decision: Not specified in the source documents (GAP-0626; ASM-0933) | P7 rwb-decision | The entry ID the feedback names, sealed in the central ledger | One hop, 2 s |

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1`, with `rwb.agent.events.v1.retry` and `rwb.agent.events.v1.dlt` | P10 rwb-agent; envelope by RWB-PLT-TE006-CON | the case ID; the run ID as the subject | agent, caseid, fallback, outcome, runid |
| DecisionRecorded | `rwb.decision-record.v1`, shared, with its retry and `.dlt` topics | P7 rwb-decision owns the ledger and the record type; the library of RWB-PLT-E1027-CON writes it | the case ID | decision the code, agent version "SCREENING@P2/PR2", final call REJECTED, the reason, the run ID and the entry ID |

Both payloads are CloudEvents 1.0 with the attributes id, source, type, specversion, time, subject and datacontenttype; a payload that fails its registry subject is refused before the relay and routed to `.dlt` with an alert, and neither carries a personal field.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Use | Rule |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 rwb-case | Declared as the trigger of a run, so the membership of this key is complete | Dedupe on the event ID; the story of this slice publishes nothing on it |
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 rwb-document | Declared as the trigger of a run; payload documentId, caseId, type and source | Dedupe on the event ID |

This contract declares no consumed topic of its own beyond the two triggers of the app story; it consumes no topic to build.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow of RWB-P10-E1062-APP, declared here for the key | `rwb-agent` | Input: agent code "SCREENING", case ID, subject ID, trigger event, event ID, idempotency key and the resolved mode; one execution per key; the 60-second policy budget then the rule result (R-UNI-32). Started as a child by a stage workflow for the route agent or the pricing agent, on DocumentStored (classification) or CaseCreated (screening). Workflow ID form: Not specified in the source documents (CG-ALL-2730). Duplicate-start policy: Not specified in the source documents (CG-ALL-2730) |
| ResolveScreeningMode | Activity of the app story, declared here for the key | `rwb-agent` | Output: mode L1 or SHADOW, the policy version and the matched segment, or a refusal |

The confirmation and the rejection are synchronous inside the feedback request; no workflow is added by this contract, and the activity names are fixed here so the app story and the fakes agree.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this key: the evaluation is started by a person, a run starts from an event, and a verdict comes from a person. The legacy Quartz scheduler is retired and DP-10 is not a pattern of this key.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_evaluation_run | P10 (`rwb_agent`) | The evaluation of "SCREENING" on "SCREEN-S2" version 1; shape fixed by 12.1 |
| agent_evaluation | P10 (`rwb_agent`) | One score row per code with the counts, precision and recall; shape fixed by AC2 |
| agent_policy | P10 (`rwb_agent`) | The L1 decision with `autonomyMode`, the two segment members, the evaluation run and the conditions |
| agent_prompt | P10 (`rwb_agent`) | Prompt version "PR2" and its hash, bound to the policy |
| agent_sample | P10 (`rwb_agent`) | The labelled sample "SCREEN-S2" version 1 |
| agent_feedback | P10 (`rwb_agent`) | The verdict, the item key and the entry ID; the pair (agent_run_id, item_key) is unique |
| agent_run | P10 (`rwb_agent`) | The run facts carried on the completion payload |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The envelope, the inbox dedupe and the idempotency keys of DP-09 |

No table is created and no column is added; no table of another service is named as a source (DP-01), and no lake table, extract or daily aggregate exists in this schema (BR8).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this key |
|---|---|---|
| rwb-case WireMock | The P3 contracts of RWB-P3-E2015-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON | A case with MORTGAGE and BKK and one with HIRE_PURCHASE; the floor 0.80; the condition "recall at least 0.75 for every code"; LOV-DEVIATION with X1 to X7 and the seven other lists; an unknown case; an answer beyond 2 s |
| rwb-deviation WireMock | The raise and the open-deviation read | A raise answered with a deviation ID and an entry ID; X1 already open; a 409 MSG-GEN-004 on the second raise; a 503 |
| rwb-source-data WireMock | The ledger read and the ACE facts | The ledger with the preceding contact; the appraisal date of X7; an empty ledger; an answer beyond 2 s |
| rwb-decision WireMock | The sealed entry read | A recorded entry with its ID; an unknown entry; an answer beyond 2 s |
| decision-record library stub | The library of RWB-PLT-E1027-CON | An accepted record with its entry ID, a writer failure, a `.dlt` route on a permanent relay failure |
| model gateway stub | The model endpoint INT-23 | An answered call with its versions, latency, tokens and cost; a timeout; a schema failure; no real model call |
| gateway-bff route stub | The route of RWB-PLT-N001-CON | A pass-through in front of the operations, one hop, media types preserved, refusals passed through unchanged |

Every fixture is synthetic and holds no personal data and no production case, complaint note or score row.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 7 provided (5 restated, 2 narrowed) and 7 consumed per 12.2 | The evaluation start and report, the configuration load, the approval and the read, the panel read and the verdict; the case read, the parameters, the lists, the open deviations, the raise, the ledger and the entry |
| Kafka | 2 published, 2 declared as triggers | The run completion on `rwb.agent.events.v1`, the record on `rwb.decision-record.v1`; `CaseCreated` and `DocumentStored` consumed by the app story |
| Temporal | 1 workflow, 1 activity declared | AgentRunWorkflow with ResolveScreeningMode on the queue `rwb-agent` |
| File | None | The sample and the configuration arrive through the upload operations of 12.1; no file crosses this contract |

### 13. Solution plan

**Package and artefacts.** The contract lives with rwb-agent, `th.co.scb.ace.workbench.recovery.agent.contract`, as the OpenAPI and AsyncAPI fragments of the agent base, the JSON Schemas of the two payloads and the fake set of 12.8.

**Pattern application**

| DP | Microservice pattern | Dependency added |
|---|---|---|
| DP-03 | Local decision-record library and the shared topic | H RWB-PLT-E1027-CON (of the app story) |
| DP-05 | ACE data through rwb-source-data's contract or the own view | none |
| DP-06 | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Outbox and inbox library; owner topic; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | REST contract with mock; one hop; 2 s timeout | none |
| DP-13 | `/api/recovery/agent/v1` | none |
| DP-19 | gateway-bff composite route | H RWB-PLT-N001-CON |

This story is Day 1 and has no build dependency: the platform rows are the app story's H dependencies, and the rwb-case rows are its C dependencies, consumed here only as published shapes.

**Work items**

| Item | Deliverable |
|---|---|
| Evaluation narrowing | The OpenAPI fragment of the start and the report, the AgentEvaluationRun and AgentEvaluationReport schemas, the statuses and the three messages |
| Score row | The schema of `agent_evaluation` per code with the counts, precision and recall at four decimals, and the ratio check of the contract test |
| Segment and L1 decision | The policy payload with the two segment members, its LOADED and APPROVED outcomes, the separations of duty and the eligibility read |
| Record mapping | The mapping of ACCEPTED to the raise entry ID and of REJECTED to a library record written first, with the unique pair (agent_run_id, item_key) |
| Events | The AsyncAPI of `rwb.agent.AgentRunCompleted.v1` with its retry and `.dlt` topics and of DecisionRecorded, with the registry subjects |
| Boundaries | The seven consumed shapes, the route, the error taxonomy and the absence rule |
| Fakes | The seven fakes of 12.8, with the answers, errors and timings the app, S8, P7 and integration tests need |

**Build steps**

1. Draft the two evaluation operations and the score row, with the X1 figures 41, 4 and 5 and the ratios 0.9111 and 0.8913 as contract examples (AC1, AC2).
2. Draft the policy payload with the segment members and the approval outcome, and the eligibility read (AC3).
3. Draft the feedback mapping and the idempotency pair against the record library (AC4).
4. Draft the two event schemas with their topics, retry and `.dlt` rules and registry subjects (AC5).
5. Write the error taxonomy, the route and the seven fakes (AC6).
6. Review against the Ownership Map and the no-lake rule, and remove every lake artefact and daily aggregate (AC7).
7. Publish, tag the baseline and hand the fakes to the app, S8, P7 and integration stories.

**Done when.** The seven contract tests of section 16 pass, the fakes answer every consumed path, the two event schemas carry their retry and `.dlt` topics, the X1 figures and the ratios appear exactly as in the legacy story, no lake artefact or daily aggregate is named, and the app story can start against the fakes on Day 1.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-002 | The approver loaded the version | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-005 | Reject without a reason | Enter the reason you are not following the recommendation. |
| MSG-P10-001 | A configuration file fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | The sample has no labelled row | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | A second evaluation is started while one runs | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P10-008 | The report is read on a run that is not DONE | The report is not ready: the evaluation is {status}. |
| MSG-GEN-004 | A second verdict on the same item | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The message IDs and their texts are copied from the legacy story and the P10 FSD where they exist; this contract invents no text and adds no code. MSG-P7-002, MSG-P10-002, MSG-P10-003 and MSG-P10-008 are the messages of the baselines this document restates and are named so a reader of the key finds the whole refusal set; the wording stays with its owner.

### 15. Screens and states

None. This story delivers no screen: the panel "Proposed deviations" on SCR-03, its states empty, loading, error and no access (empty, error and no access: Not specified in the source documents (CG-ALL-2739)) and the gateway-bff route in front of it are the app story's (section 15 of RWB-P10-E2029-APP), and this document fixes only the operations the panel and the verdict use.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E2029-CON-01 | AC1 | Contract | The OpenAPI fragment of the start and report; a run not DONE; an unknown run |
| TC-P10-E2029-CON-02 | AC2 | Contract | One row per code X1 to X7; X1 counts 41, 4, 5 giving 0.9111 and 0.8913; X4 recall 0.6000 |
| TC-P10-E2029-CON-03 | AC3 | Contract | Policy "SCREENING" P2 with MORTGAGE and BKK; the approval by a second person; a row with no segment |
| TC-P10-E2029-CON-04 | AC4 | Contract | A confirmation with the raise entry ID; a rejection with the record first; a second verdict on the same item |
| TC-P10-E2029-CON-05 | AC5 | Contract | The two schemas against their registry subjects; the retry and `.dlt` topics; a payload with a personal field |
| TC-P10-E2029-CON-06 | AC6 | Contract | The nine sub-tables, the seven fakes, the route and the error taxonomy |
| TC-P10-E2029-CON-07 | AC7 | Contract | The document against the Ownership Map; the absence of a lake table, an extract and a daily aggregate |
| TC-P10-E2029-CON-08 | AC6 | Contract | Boundary: the nine sub-tables of 12.7 at their owner; a table of another service named as a source; a column added to a table |
| TC-P10-E2029-CON-09 | BR1, BR10, BR11 | Contract | The start and report with no embedded harness and no read of rwb_agent; a call over one hop with the 2 s budget; a drift flagged in its baseline |
| TC-P10-E2029-CON-10 | BR2, BR3 | Contract | A score row whose ratios do not reproduce; a policy LOADED and approved by a person other than the loader |
| TC-P10-E2029-CON-11 | BR4, BR9 | Contract | A case outside the segment answered SHADOW; the parameters and lists read at run time with their version |
| TC-P10-E2029-CON-12 | BR5, BR6 | Contract | A confirmation with the entry ID; a rejection with the record written before the feedback; a second verdict refused with 409 |
| TC-P10-E2029-CON-13 | BR7, BR8 | Contract | A CloudEvents message validated before the relay and routed to .dlt on failure; no lake table and no daily agent table |
| TC-P10-E2029-CON-14 | BR12 | Contract | The panel and the verdict passed through the gateway-bff route unchanged |
| TC-P10-E2029-CON-15 | AC8 | Contract | The twelve rules of section 8 read against the contract file, the two event schemas, the table list and the fakes; test data Not specified in the source documents (NEWAC-RWB-P10-E2029-CON-AC11) |

Level is Contract for all fifteen, because each test reads the artefact and never a business outcome. The twelve legacy test cases of RWB-E2-029 belong to RWB-P10-E2029-APP; no ITG copy is created here, and the cross-service proof is the work of RWB-ITG-W2.

No deviation, screening or queue volume is stated for this module. The only quantities are the platform figures (NFR-001: 23,600 open cases at go-live and 3,110 new a month; NFR-002: about 370 staff online of 914; NFR-011: 300 milliseconds per rule evaluation) and the two evaluation samples of 200 and 500 cases. The deviation rate is measured in the shadow run before the wave 2 volume test is sized (GAP-1833).

### 17. Guardrails

- No business value in the contract: the segment, the floor and the condition appear only as examples copied from the legacy story and as rows read at run time (BR9).
- No personal data in a payload, a fixture or a log; every fixture is synthetic and no customer identifier appears in a schema.
- No lake artefact and no daily agent table: the absence rule is a review gate and a contract test (BR8).
- A restated operation is narrowed, never redefined; a drift is corrected in its baseline (BR11).
- Each call is one hop on the owner's base with a 2 s client budget, and no schema of another service is named (BR10).
- The record and the feedback are one transaction or neither, and the pair (agent_run_id, item_key) is the only idempotency key of a verdict (BR5, BR6).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-AGT-08, FEAT-DVH-07 | 11 Handle customer care and deviations | R-UNI-39 | TC-P10-E2029-CON-02, TC-P10-E2029-CON-04 |
| REQ-DVH-006 | A deviation flag is visible on the case and in every queue | Business Requirements Program, section 5.15 | FEAT-DVH-07 | 11 Handle customer care and deviations | R-DEV-01 | TC-P10-E2029-CON-04 |
| DP-03 (D-RCV-60) | Record written locally and sealed centrally | Template and Rules §R5.5; ADR-022 | FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-39 | TC-P10-E2029-CON-04, TC-P10-E2029-CON-05 |
| DP-05 (D-RCV-60) | ACE facts through the owner's contract or the own view | Template and Rules §R5.5 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-P10-E2029-CON-06 |
| DP-06, DP-07 (D-RCV-60) | The floor, the segment, the condition and the lists are read at run time | Template and Rules §R5.5 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-P10-E2029-CON-03, TC-P10-E2029-CON-06 |
| DP-09 (D-RCV-60) | Outbox, owner topic and the CloudEvents envelope with retry and `.dlt` | Template and Rules §R5.5; ADR-015 | FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-39 | TC-P10-E2029-CON-05 |
| DP-11, DP-13 (D-RCV-60) | REST contract with mock, one hop, 2 s, on the agent base | Template and Rules §R5.5; ADR-020 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-P10-E2029-CON-01, TC-P10-E2029-CON-06 |
| DP-19 (D-RCV-60) | The panel and the verdict are reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-DVH-07 | 11 Handle customer care and deviations | None | TC-P10-E2029-CON-06 |
| RWB-E2-029 (legacy story) | The contract of the screening key: the operations, the score row, the record mapping and the events | Business Requirements Program, section 5.15 | FEAT-AGT-08, FEAT-DVH-07 | 11 Handle customer care and deviations | R-DEV-01, R-UNI-39 | The fifteen contract tests of section 16 |

The gap GAP-0626 records the areas the sources leave open from the contract side - the story that publishes the S8 raise, the members of the raise, the ledger and entry reads, the parameter keys, the route name and path, the score-row members and the payload members - and each default it raises is settled by ASM-0930 to ASM-0942. The app slice is RWB-P10-E2029-APP and the cross-service proof is RWB-ITG-W2.

### 19. Out of scope

- The application behaviour of the key: RWB-P10-E2029-APP.
- The evaluation harness, its operations and the proposal payload as baselines: RWB-P10-E1061-CON and RWB-P10-E1058-CON.
- The run path, the proposal shape and the agent topic: RWB-P10-E1062-CON.
- The panel and feedback baselines: RWB-P10-E2028-CON.
- The deviation record, R-DEV-01, the case status and the open-deviation read: rwb-deviation (S8) and rwb-case (P3).
- The central ledger, the record fields and the sealing: rwb-decision (P7).
- The interaction ledger, the ACE views and the extension tables: rwb-source-data (P1).
- The daily agent aggregate and its drift alert: RWB-P10-E2031-CON.
- The agent monitor screen SCR-46 and its measures: RWB-E2-031.
- Any data lake artefact, extract, credential or INT-19 and INT-20 path: removed by Architecture v5 (ADR-018).
- The cross-service proof of the key: the integration work of RWB-ITG-W2.
