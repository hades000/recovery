# RWB-P10-E1061-CON Intake agent evaluation and L1 proposal [E2a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1061-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement (DOR-RWB-P10-E1061-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1: base /api/recovery/agent/v1 and topic rwb.agent.events.v1 (DOR-RWB-P10-E1061-CON-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to REQ-DRI-010, REQ-DRI-011) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract slice of RWB-E1-061 for rwb-agent, written on Day 1 because a contract story carries no build dependency (§R5.7). The behaviour of the legacy key is unchanged - the disposition is Moved (no impact) - and only its seams are written down: the three evaluation operations on the base `/api/recovery/agent/v1` (DP-13), the L1 proposal payload with its policy-version binding and the approval operation used here, the agent topic `rwb.agent.events.v1` with the rule that an evaluation completes into a status and publishes no business message of its own, the parameter and reference-data operations of rwb-case this key consumes (DP-06, DP-07), and the four fakes the app story builds against. It does not restate the whole rwb-agent contract, whose baseline is RWB-P10-E1058-CON, and it fixes no table of its own beyond the four `rwb_agent` tables of the key (DP-01) and no migration beyond `V10_004__policy_promotion.sql` (DP-15). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 9 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the intake agent evaluation and the L1 proposal fixed as a contract on Day 1: the three evaluation operations on `/api/recovery/agent/v1` with their query, their answer resources and their refusals, the L1 proposal payload with the four promotion members and its policy-version binding, the approval operation used here with its separation-of-duty refusal, the declaration of `rwb.agent.events.v1` with the rule that an evaluation publishes no message of its own, the parameter and reference-data operations of rwb-case that the promotion checks read, and the four contract fakes**, so that **the app story RWB-P10-E1061-APP, the operations story of the key and every story that reads an evaluation or a policy version build against one agreed, testable shape on Day 1 without waiting for the service to be complete**.

### 2. Business rationale

The legacy key RWB-E1-061 was written against in-process calls inside the monolith: the report was a service method behind the admin controller, the four promotion members were columns of the same `recovery` schema, the minimum sample was a value of the local policy JSON schema, the mode and status values were code enumerations, and the approval was the in-process maker-checker of the same deployment (legacy sections 12 and 13). In the target each of those is a boundary or an owner:

- The report is one REST operation on the base `/api/recovery/agent/v1`, with one hop and a 2 s client budget (DP-13; ADR-020).
- The four promotion members are columns of `agent_policy` in `rwb_agent`, added by the service's own migration in its own Flyway sequence (DP-01, DP-15).
- The minimum sample and the promotion check list are parameter values of rwb-case, reached through its contract (DP-06); the three lists are reference data of rwb-case (DP-07).
- The version in force is reached through the gateway-bff route by every screen and every export (DP-19).
- The completion of an evaluation is a row state, not a business event: the one business event of the service, `rwb.agent.AgentRunCompleted.v1` (EV-28), belongs to a business run of an agent and is declared here only so that the topic is complete.

Contract-first only works if the seam is written down once and faked on Day 1. The seam here is small and load-bearing: one report operation whose answer carries the legacy report members so that the approver's pack needs no change of shape, one payload for the L1 proposal that binds exactly one evaluation run and one policy version, one approval operation whose refusal is the separation of duty, and one honest statement that an evaluation completion is read and not published. Without it the app story invents its own answer, the report members drift from the legacy ones, and the row that proves what was measured stops matching the report the committee approved.

This story defines the provided side of this key and consumes the two rwb-case contracts. It restates nothing that another owner holds: the configuration operations and the policy resource are baselined in RWB-P10-E1058-CON, the evaluation harness that produces the runs is RWB-P10-E1060-APP, and the parameter rows and reference rows are rwb-case's (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the REST base, the topic and the event names follow the platform rule and not a local choice (§R4; DP-13).
- The CloudEvents 1.0 envelope and the platform error envelope are the platform baseline; this document narrows them where it must and says so.
- The agent runtime baseline contract of RWB-P10-E1058-CON is in force: the policy and prompt resources, the configuration operations `POST /admin/agent-configs` and `POST /admin/agent-configs/{versionId}/approve`, the error taxonomy and the queue `rwb-agent` in the namespace `rwb-recovery` are its elements, and this story reuses them rather than redefining them.
- The evaluation harness of RWB-P10-E1060-APP is known and produces the run resource this contract reads: it is the `POST /api/recovery/agent/v1/admin/agent-evaluations` operation of that story, and this contract fixes the shape once for both keys (ASM-0871).
- The parameter and reference-data contracts of rwb-case are published by RWB-PLT-E1042-CON and RWB-PLT-E1043-CON with their client libraries, and the operations are `GET /api/recovery/case/v1/admin/parameters` and `GET /api/recovery/case/v1/admin/lists/{listCode}` owned by P3 (DP-06, DP-07).
- The four `rwb_agent` tables of the key - agent_evaluation_run, agent_evaluation, agent_run and agent_policy - are the P10 objects of the Ownership Map, and the four promotion columns are added by `V10_004__policy_promotion.sql` (DP-01, DP-15).
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W1.

### 4. Flow

1. Draft the three evaluation operations below the base `/api/recovery/agent/v1`: the start, the read and the report, with their query, their answer resource, their rights, their errors and their one-hop budget (AC1).
2. Fix the L1 proposal payload on the configuration load: the kind, the agent, the policy version, the autonomy mode, the four promotion members and the binding to exactly one evaluation run (AC2).
3. Fix the approval operation used here: its request, its answer, the separation-of-duty refusal and the dates it writes (AC3).
4. Declare the agent topic: `rwb.agent.events.v1` with `rwb.agent.AgentRunCompleted.v1` (EV-28), its envelope, its key, its registry subject and its retry and `.dlt` topics, and the rule that an evaluation completion publishes no message of its own (AC4).
5. Write the parameter and reference-data operations this key consumes, as owned by rwb-case, with the values the promotion checks read and the two lists (AC5).
6. Write the four fakes: the parameters fake, the reference-data fake, the gateway-bff route stub and the evaluation-run fixture, each with the answers and the failures this key's tests need (AC5; 12.8).
7. Publish the nine sub-tables of section 12 and the contract tests of section 16, and mark every shape that another document owns as baselined there (AC6).
8. Tag the baseline and hand it to RWB-P10-E1061-APP and to the test cases of this key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of an answer or of a payload drifts from this document: a renamed member, a retyped amount, a dropped one of the four promotion members | The contract test fails and the merge is blocked | None | AC1, AC2 |
| X2 | A caller asks for the report of a run that is not DONE | The operation refuses with 409 and names the run | MSG-P10-008 | AC1 |
| X3 | A payload carries a personal field, a customer identifier or an account number | The data-steward review and the contract test refuse the payload; nothing is written | None | AC2 |
| X4 | The payload names a run that does not belong to the agent or to the policy version it binds | The load is refused with 422 before the row is stored | MSG-P10-001 | AC2 |
| X5 | A produced message fails its registry subject, or the relay cannot reach the topic | The message is refused before the relay and routed to the `.dlt` topic of the agent topic with an alert | None | AC4 |
| X6 | A shape owned by another document is restated here and drifts from it | The contract test fails on the owner's document and this document is aligned, because the owner is the baseline | None | AC3, AC6 |
| X7 | A member, a query parameter, a type or a route path is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC1, AC2, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the agent runtime baseline contract and the two rwb-case contracts as published |
| Negotiable | The member names and their types are fixed here; the values stay rows of the parameter, reference and policy tables, and the review with the owners settles any type detail |
| Valuable | Unblocks the app story of this key on Day 1 and gives every reader of an evaluation, a report or a policy version one shape |
| Estimable | Three provided evaluation operations, two restated configuration operations, two consumed reads, one topic declaration and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact - the schema file, the payload, the fake, the document - and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Intake agent evaluation and L1 proposal contract slice for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the agent runtime baseline contract of RWB-P10-E1058-CON is in force
    Given agent "INTAKE" has run 200 shadow cases on sample "INTAKE-S1" version 1 in evaluation run "EV-INTAKE-001"

  Scenario: AC1 The three evaluation operations are fixed on the agent base (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When RW-COE starts, reads and reports the evaluation of agent "INTAKE" on sample "INTAKE-S1" version 1
    Then POST /api/recovery/agent/v1/admin/agent-evaluations answers 202 with an AgentEvaluationRun in status RUNNING, and 409 with MSG-P10-003 when one for the same agent and sample version is already RUNNING, and 422 with MSG-P10-002 when the sample has no labelled rows
    Then GET /api/recovery/agent/v1/admin/agent-evaluations takes the query agent, from and to and answers AgentEvaluationRun[] under Rules and parameters R with scope applied
    Then GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report answers AgentEvaluationReport with the members agent, sampleSize, agreementByLabel[], failureCounts, totalCostThb, costPerCaseThb, latencyP50Ms, latencyP95Ms, policyVersion, promptVersion and modelVersion, in JSON, text/csv and application/pdf
    Then the report operation answers 409 with MSG-P10-008 for a run that is not DONE, 404 for an unknown run and 403 with MSG-P4-002 for a role without the right
    Then every operation is one hop on /api/recovery/agent/v1 and none of them is served on the legacy monolith base

  Scenario: AC2 The L1 proposal payload binds one run and one policy version (new, D-RCV-60)
    Given the policy resource of the agent runtime baseline
    When RW-COE loads policy "INTAKE" version "P2" with mode "L1" and the four promotion members through POST /api/recovery/agent/v1/admin/agent-configs
    Then the payload carries kind POLICY, agent "INTAKE", policyVersion "P2", autonomyMode "L1", evaluationRunId "EV-INTAKE-001", promotionConditions, watchMeasures and fallbackRule, and the answer is 201 with an AgentConfigVersion in status LOADED
    Then promotionConditions carries the condition "agreement at least 0.85 for every gap type", fallbackRule carries "rule result per R-UNI-32", and watchMeasures carries "acceptance, correction rate, fallback rate below 0.10"
    Then the binding is exactly one evaluation run of the same agent, of sample "INTAKE-S1" version 1, in status DONE, and a payload that names no run, a run of another agent or a run that is not DONE is refused with 422 and MSG-P10-001
    Then the payload and the answer carry no personal field, no customer identifier and no account number, and the report body is never copied into the payload
    Then the shape of agent_policy and of the version resource is the baseline's, and this document adds the four promotion member names only (ASM-0876, ASM-0877)

  Scenario: AC3 The approval operation used here is fixed (new, D-RCV-60)
    Given version "P2" of policy "INTAKE" in status LOADED, loaded by user "coe.user01"
    When RW-RISK approves it through POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve with a valid from date
    Then the operation answers 200 with the version in status APPROVED, approved_by recorded and valid_from set, and 404 for an unknown version and 409 with MSG-GEN-004 for a version that is already approved
    Then the approval is refused with 409 and MSG-P7-002 when the user who approves the version is the user who loaded it
    Then the operation is one hop on /api/recovery/agent/v1 under Rules and parameters A with scope applied, and its shape is the baseline's and is restated, never redefined

  Scenario: AC4 The agent topic is declared and an evaluation publishes no message of its own (new, D-RCV-60)
    Given the AsyncAPI document of this story and the topic rwb.agent.events.v1 with its retry and .dlt topics
    When an evaluation run of agent "INTAKE" reaches status DONE
    Then no message is published on rwb.agent.events.v1 for the evaluation run, and the completion is visible through GET /admin/agent-evaluations and through the report operation
    Then the declared business event on rwb.agent.events.v1 is rwb.agent.AgentRunCompleted.v1 (EV-28), a CloudEvents 1.0 message keyed by the case ID with the run ID as its subject, carrying run facts only and no personal data
    Then a produced message that fails its registry subject is routed to the .dlt topic of rwb.agent.events.v1 with an alert, and an event for the completion of an evaluation is not declared, because no source names one (ASM-0875)

  Scenario: AC5 The parameter and reference-data fakes are named and answer every consumed value (new, D-RCV-60)
    Given the two consumed operations of section 12.2 and the four fakes of section 12.8
    When a contract test of this key runs
    Then the rwb-case parameters fake answers GET /api/recovery/case/v1/admin/parameters with the minimum sample 200 for an autonomy step, the promotion check list and its version, a version that raises the minimum above 200, an answer without the minimum, and a delay beyond 2 s
    Then the rwb-case reference-data fake answers GET /api/recovery/case/v1/admin/lists/{listCode} with LOV-AUTONOMY OFF, SHADOW and L1, LOV-CONFIG-STATUS LOADED, APPROVED and RETIRED, LOV-EVAL-STATUS RUNNING, DONE and FAILED, a list version that lacks L1, and a delay beyond 2 s
    Then the gateway-bff route stub is a pass-through of one hop in front of the three provided operations and preserves the JSON, CSV and PDF media types
    Then the evaluation-run fixture holds 200 runs with 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR, 412.6000 baht in total, median 4,100 ms and 95th percentile 9,800 ms, and a run "EV-INTAKE-003" with sample size 150
    Then every fixture is synthetic and a drift between a fake and this document fails the contract test

  Scenario: AC6 The nine sub-tables are complete and every shape has one owner (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables and the ownership of each shape are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then the evaluation operations, the L1 payload and the topic are declared here, the configuration operations and the policy resource are baselined in RWB-P10-E1058-CON, and the parameter and reference rows are rwb-case's
    Then no operation of another service is declared as provided by rwb-agent and no rwb-agent path is declared as another service's (DP-13)
    Then the four promotion columns are the only schema change of this key and arrive by V10_004__policy_promotion.sql in the rwb-agent Flyway sequence (DP-15)

  Scenario: AC7 Every business rule BR1 to BR9 of section 8 is verified by a named test case (new, D-RCV-60)
    Given the business rules of section 8 and their Covered by column
    When the contract tests of this key are reviewed
    Then each of BR1 to BR9 names at least one test case of section 16 in its Covered by cell

  Scenario: AC8 A request without an authenticated identity is refused with 401 on every provided operation (new, D-RCV-60)
    Given the operations of section 4 of this contract
    When a caller sends a request on /api/recovery/agent/v1 without an authenticated identity
    Then the answer is 401 with the platform error envelope of section 3, and its message code is Not specified in the source documents (NEWAC-RWB-P10-E1061-CON-AC8)

  Scenario: AC9 A replay of a write with the same idempotency key is answered under the replay rule (new, D-RCV-60)
    Given a write on /api/recovery/agent/v1 has been accepted with an idempotency key
    When the same write is sent again with the same idempotency key
    Then the replay rule and its answer are Not specified in the source documents (NEWAC-RWB-P10-E1061-CON-AC9)

  Scenario: AC10 A consumed call that fails or does not answer within 2 s is refused (new, D-RCV-60)
    Given the rwb-case parameters fake and the reference-data fake of AC5 are running
    When RW-COE loads policy "INTAKE" version "P2" and a consumed call fails or does not answer within 2 s
    Then the load is refused with the error of the RWB-P10-E1058-CON error taxonomy, and that error's code is Not specified in the source documents (NEWAC-RWB-P10-E1061-CON-AC10)
```

**Target reading.** This contract adds no behaviour and no business value: the run, the sample, the 200 runs with 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR, the 412.6000 baht, the condition "agreement at least 0.85 for every gap type", the fallback "rule result per R-UNI-32", the measures "acceptance, correction rate, fallback rate below 0.10", the minimum sample 200, the sample size 150 of "EV-INTAKE-003", the user "coe.user01" and the message IDs are the legacy values of RWB-E1-061, copied character for character, and the keys of the promotion payload are the field names of TSD P10 v2 T3.1 (DF-AGT-017 to DF-AGT-020). The disposition of the key is Moved (no impact): the contract states the seams of an unchanged behaviour. Three values are not named by any source and are marked where they appear: the route path and route name of the gateway-bff route in front of the reads - Not specified in the source documents (GAP-0613; ASM-0872) - the name of an event for the completion of an evaluation, which no source names and which this contract therefore does not declare (GAP-0613; ASM-0875), and the type and length of the members beyond the names the legacy report and TSD T3.1 give (GAP-0613; ASM-0876, ASM-0877).

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The evaluation is three operations on one base - start, read and report - and no caller embeds the evaluation harness or reads `rwb_agent` | DP-11 behind DP-01; DP-13; legacy section 12 | AC1; TC-P10-E1061-CON-01 |
| BR2 | The report exists only for a run in status DONE, and its members are the legacy report members; the same run gives the same report | Legacy AC1, AC3; MSG-P10-008 | AC1; TC-P10-E1061-CON-01 |
| BR3 | An L1 proposal binds exactly one DONE evaluation run of the same agent and one policy version, and the four promotion members are columns of agent_policy | Legacy BR1; TSD P10 v2 T3.1 DF-AGT-017 to DF-AGT-020 | AC2; TC-P10-E1061-CON-02 |
| BR4 | The loader and the approver are different people, and the approval writes approved_by and valid_from | Legacy BR6; R-UNI-39; MSG-P7-002 | AC3; TC-P10-E1061-CON-03 |
| BR5 | The minimum sample and the promotion check list are parameter values of rwb-case read at load time, and the three lists are reference data of rwb-case: no such value is written in the contract | DP-06; DP-07; ASM-0873 | AC5; TC-P10-E1061-CON-05 |
| BR6 | `rwb.agent.events.v1` carries `rwb.agent.AgentRunCompleted.v1` (EV-28) and nothing else; an evaluation completion is a row state and publishes no message | Arch v5 slide 43 row 28; DP-14; ASM-0875 | AC4; TC-P10-E1061-CON-04 |
| BR7 | Every message is a CloudEvents 1.0 message on the owner's topic, keyed by the case ID, validated against its registry subject before the relay and routed to `.dlt` on failure, with retry topics | DP-09; DP-14; Arch v5 slide 42 | AC4; TC-P10-E1061-CON-04 |
| BR8 | One base and one topic per service: this contract declares `/api/recovery/agent/v1` and `rwb.agent.events.v1` for rwb-agent and never another service's path or topic as its own | DP-13; DP-14; Arch v5 slide 41 | AC1; AC4; TC-P10-E1061-CON-01; TC-P10-E1061-CON-04 |
| BR9 | No personal data in a payload, an example or a fake: the report and the proposal carry identifiers, facts and rates only | Legacy section 17; Template and Rules §R7.2 s17 | AC6; TC-P10-E1061-CON-06 |

### 9. State transitions

These are the states of this document, not of a case or a policy version:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three evaluation operations, the L1 payload, the approval, the topic and the four fakes are described | In review |
| In review | Consumer sign-off | The app story of this key and the test cases accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a query parameter or a payload field is added without removing one | Baselined |
| Baselined | Breaking change to an operation or to the payload | A member of the report, of the L1 payload or of the topic declaration is removed, renamed or retyped | In review, with the owner of the affected contract |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A baseline changes a restated shape | RWB-P10-E1058-CON publishes a new policy resource | Baselined, aligned to the baseline |

The run states RUNNING, DONE and FAILED are those of LOV-EVAL-STATUS and are set by the evaluation harness; the version states LOADED, APPROVED and RETIRED are those of LOV-CONFIG-STATUS and belong to RWB-P10-E1061-APP and RWB-P10-E1058-APP. This document fixes neither table of values; it names them as reference data read through the rwb-case contract.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the operation shapes, the L1 payload, the topic declaration, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to an operation, to the payload or to the topic declaration |
| The rwb-case owner | Owns the parameter and reference-data operations and signs off the two consumed shapes |
| The rwb-agent app and operations stories | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule and the outbox and retry rule this document reuses |
| Data steward | Confirms that no personal data field is declared in a report, a payload, an event or a fake |

The identity that reads the two consumed operations is the rwb-agent service identity (DP-02); its login is Not specified in the source documents (GAP-0612; ASM-0869).

Every operation of section 4 is authorised through the rwb-access check of DP-08; the name of that check and its rights are Not specified in the source documents (DOR-RWB-P10-E1061-CON-6).

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Start request | agent, sampleCode, sampleVersion, approaches; 202 AgentEvaluationRun; 409 a same evaluation already RUNNING; 422 an empty sample | Not specified in the source documents (DOR-RWB-P10-E1061-CON-7) |
| Read answer | AgentEvaluationRun[] with the run row members of TSD P10 v2 T3.1 (DF-AGT-070 to DF-AGT-085), with Accept text/csv for the score and proposal rows | Not specified in the source documents (DOR-RWB-P10-E1061-CON-7) |
| Report answer | agent, sampleSize, agreementByLabel[], failureCounts, totalCostThb, costPerCaseThb, latencyP50Ms, latencyP95Ms, policyVersion, promptVersion, modelVersion (the legacy report members) | Not specified in the source documents (DOR-RWB-P10-E1061-CON-7) |
| L1 payload | kind "POLICY", agent "INTAKE", policyVersion, autonomyMode, evaluationRunId, promotionConditions, watchMeasures, fallbackRule, validFrom | Not specified in the source documents (DOR-RWB-P10-E1061-CON-7) |
| Approval request and answer | the version ID in the path, the valid from date in the body; the AgentConfigVersion answer with status APPROVED, approved_by and valid_from | Not specified in the source documents (DOR-RWB-P10-E1061-CON-7) |
| Error | the platform problem response: status, code, detail, the business message ID when one applies | Not specified in the source documents (DOR-RWB-P10-E1061-CON-7) |
| Topic | `rwb.agent.events.v1`, `rwb.agent.AgentRunCompleted.v1` (EV-28), CloudEvents 1.0, key the case ID, subject the run ID, payload as Kafka Catalog v1 | Not specified in the source documents (DOR-RWB-P10-E1061-CON-7) |
| Consumed values | the minimum sample 200 for agent "INTAKE" and the promotion check list; LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-EVAL-STATUS with their versions | Not specified in the source documents (DOR-RWB-P10-E1061-CON-7) |

The type and length of the members beyond the names the legacy report and TSD P10 v2 T3.1 give, and the internal member names of `promotionConditions` and `watchMeasures` beyond the three legacy texts, are Not specified in the source documents (GAP-0613; ASM-0876, ASM-0877); this document fixes the member names and leaves the nested types to the review with the owners. The route name and path of the gateway-bff route are Not specified in the source documents (GAP-0613; ASM-0872), and no event name for the completion of an evaluation is specified (GAP-0613; ASM-0875).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Rights | Idempotency |
|---|---|---|---|---|
| POST | `/admin/agent-evaluations` | Start the evaluation of an agent on a labelled sample: agent "INTAKE", sampleCode "INTAKE-S1", sampleVersion 1; 202 AgentEvaluationRun in status RUNNING; 409 a same evaluation already RUNNING (MSG-P10-003); 422 a sample with no labelled rows (MSG-P10-002) | Rules and parameters C, scope applied | Idempotency-Key header |
| GET | `/admin/agent-evaluations` | List evaluation runs with their scores and proposals: query agent, from, to; 200 AgentEvaluationRun[]; with Accept text/csv the score and proposal rows | Rules and parameters R, scope applied | Not applicable: the call writes nothing |
| GET | `/admin/agent-evaluations/{evaluationId}/report` | The report of one run: agent, sampleSize, agreementByLabel[], failureCounts, totalCostThb, costPerCaseThb, latencyP50Ms, latencyP95Ms and the three versions; 200 AgentEvaluationReport in application/json, text/csv or application/pdf; 409 the run is not DONE (MSG-P10-008); 404 unknown run | Rules and parameters R, scope applied | Not applicable: the same run gives the same report |

`POST /admin/agent-configs` and `POST /admin/agent-configs/{versionId}/approve` are provided by rwb-agent and baselined in RWB-P10-E1058-CON, which owns their full shape. This contract restates only the members this key writes or reads and declares no configuration operation of its own: the four promotion members of the L1 payload (AC2) and the separation-of-duty refusal of the approval (AC3). Errors of the three operations above: 401 no session, 403 no right (MSG-P4-002), 404 unknown run, 409 the business refusal named per operation, 422 a payload or a sample that fails a check (MSG-P10-001), 503 the store or a consumed contract unavailable.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The minimum sample of an autonomy step for agent "INTAKE" - 200 - and the promotion check list in force, with their version (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-EVAL-STATUS in force, against which the mode "L1" and the status values of every answer are checked (DP-07) |

Every operation is one hop with a 2 s client budget and is cached by the client library for the life of the request (DP-11 behind DP-06 and DP-07). No other service's data is read, and no schema client of another service exists in rwb-agent. The right check is the guard library's and is not a REST operation of this key.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | runid, agent, caseid, outcome, fallback (member names as in Kafka Catalog v1, EV-28) |

`rwb.agent.AgentRunCompleted.v1` is the one business event of the service and is published by a business run of an agent, through the outbox in the same transaction as the run row and validated against its registry subject before the relay. The topic carries its retry topics and its `.dlt` topic as the platform naming rule sets them (DP-09, DP-14).

No message is published when an evaluation run completes. An evaluation ends in `agent_evaluation_run.status` DONE and is read through `GET /admin/agent-evaluations`, the report operation and the CSV answer of the read. No source names an event for the completion of an evaluation, so this contract declares none, and a `rwb.agent.<Something>.v1` message invented for that state would be an unowned event type (ASM-0875). If the programme later wants one, its name is Not specified in the source documents (GAP-0613; ASM-0875) and it is added here first, never in a service.

#### 12.4 Events consumed

None. This key reads no topic: the evaluation is started by RW-COE on request through `POST /admin/agent-evaluations` and reads its inputs through the two contracts of 12.2. The consumers of EV-28 are rwb-decision, rwb-document and rwb-deviation (Arch v5 slide 43), not this service.

#### 12.5 Workflows and activities

None. The evaluation, the report and the promotion checks run inside rwb-agent on the admin request path and start no workflow of their own. `AgentRunWorkflow` on the task queue `rwb-agent` in the namespace `rwb-recovery` belongs to the agent platform of RWB-P10-E1058-CON and RWB-ITG-TE013-ITG, and the shadow runs this report aggregates were made by it; this contract declares neither its input nor its activities.

#### 12.6 Schedules

None. The evaluation is started by a person, the report is requested by a person and the proposal is loaded by a person; the Arch v5 job map names no job for an agent evaluation (slide 44). No Temporal Schedule is declared, changed or owned by this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_evaluation_run | P10 (rwb_agent) | The run resource of the start and the read, and the source of the report; status is one of LOV-EVAL-STATUS; no column added |
| agent_evaluation | P10 (rwb_agent) | The score rows the report aggregates by label key: sample_size, agreement_rate, precision and recall; no column added |
| agent_run | P10 (rwb_agent) | The shadow runs the report costs and times: status, latency_ms, cost_thb, evaluation_run_id; no column added |
| agent_policy | P10 (rwb_agent) | The L1 proposal row and its four promotion members evaluation_run_id, promotion_conditions, watch_measures and fallback_rule, added by `V10_004__policy_promotion.sql` (DP-15) |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | The outbox, inbox and idempotency envelope of the one declared event (DP-09) |

`parameter_catalog`, `parameter_value`, `reference_version` and `reference_row` are P3's tables of schema `rwb_case` and are reached only through the two contracts of 12.2 (DP-01, DP-06, DP-07). No foreign key crosses a schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case parameters fake (WireMock) | `GET /api/recovery/case/v1/admin/parameters`: the minimum sample 200 for agent "INTAKE" and the promotion check list with its version; a version that raises the minimum above 200; an answer without the minimum; a delay beyond 2 s | Contract tests, app story |
| rwb-case reference-data fake (WireMock) | `GET /api/recovery/case/v1/admin/lists/{listCode}`: LOV-AUTONOMY with OFF, SHADOW and L1; LOV-CONFIG-STATUS with LOADED, APPROVED and RETIRED; LOV-EVAL-STATUS with RUNNING, DONE and FAILED; a list version that lacks L1; a delay beyond 2 s | Contract tests, app story |
| gateway-bff route stub | A pass-through route of one hop in front of the three provided operations, preserving application/json, text/csv and application/pdf and returning the 403 of MSG-P4-002 unchanged; its route name and path are Not specified in the source documents (GAP-0613; ASM-0872) | Contract tests, app story |
| Evaluation-run fixture (in-service, not WireMock) | The 200 stored runs of "EV-INTAKE-001" with 188 ANSWERED, 7 TIMED_OUT, 3 GUARDRAIL_FAILED and 2 BELOW_FLOOR, 412.6000 baht, median 4,100 ms and 95th percentile 9,800 ms; the run "EV-INTAKE-003" with sample size 150; a run in status RUNNING | Contract tests, app story |

The configuration store stub, the outbox stub and the access stub are the platform's and are used but not declared here. Every fixture is synthetic: no production run, no customer identifier and no personal value appears in one, and the agent model endpoint INT-23 is never called by a test of this contract.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed, 2 restated | The start, the read and the report on `/api/recovery/agent/v1`; the rwb-case parameters read and list read; the configuration load and approve restated from RWB-P10-E1058-CON; one hop, 2 s each |
| Kafka | 1 declared, 0 consumed | `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` with its retry and `.dlt` topics; no message for the completion of an evaluation |
| Temporal | None | No workflow and no schedule in this contract; `AgentRunWorkflow` on the queue `rwb-agent` is the agent platform's |
| File | None | The report leaves as the body of the read with Accept text/csv or application/pdf; no file is read or written, and no sample file is loaded by this key |

### 13. Solution plan

**Deliverables.** `contract/agent-evaluation-operations.yaml` (the start, the read and the report with their query, answers, rights, errors and budget), `contract/agent-l1-proposal.yaml` (the payload with the four promotion members and the run binding), `contract/agent-config-approval.md` (the approval operation as restated from the baseline, with the separation-of-duty refusal), `contract/agent-evaluation-topic.asyncapi.yaml` (`rwb.agent.events.v1` with EV-28, the retry and `.dlt` topics and the rule that an evaluation publishes none), `contract/agent-promotion-parameters.md` (the two consumed operations and the values the promotion reads) and the four fake mappings with their synthetic fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON for the app story; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON for the app story; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts it names are those its consumer adds, and the two C dependencies, RWB-P3-E1042-CON and RWB-P3-E1043-CON, are the rwb-case side of the parameter and list reads, built against their fakes. DP-11 is the pattern of the three provided and the two consumed reads; DP-09 and DP-14 sit behind the one declared event and add no dependency here.

**Build steps**

1. Write the three evaluation operations with their query, answer resources, rights, errors and one-hop budget, and add a lint to the pipeline (AC1).
2. Write the L1 payload with the four promotion member names, the run binding and the no-personal-data rule (AC2).
3. Restate the approval operation from the baseline with the separation-of-duty refusal and mark the baseline as owner (AC3).
4. Write the AsyncAPI document for `rwb.agent.events.v1`: EV-28, its envelope, key, subject, registry subject, retry and `.dlt` topics, and the statement that an evaluation publishes no message (AC4).
5. Write the two consumed operations and the values the promotion reads, with the parameter and reference-data owners named (AC5).
6. Build the four fake mappings and their synthetic fixtures, including the missing parameter, the list without L1 and the two delays (AC5).
7. Add the six contract tests of section 16, including the drift test between each fake and this document (AC6).
8. Tag the baseline and collect the sign-off of the app story of this key and of the rwb-case owner on the two restated consumed shapes.

**Done when.** The six contract files validate in the pipeline, the six contract tests pass, the four fakes answer every consumed path and payload, and RWB-P10-E1061-APP has accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-008 | Report requested before the evaluation is done | The evaluation of {agent} on sample {sample} is still running. Open the report when it has finished. |
| MSG-P10-001 | The proposal fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | The sample has no labelled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Same evaluation already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P7-002 | Loader approves own proposal | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | The version is already approved | This version is already approved. |

The five business messages of the evaluation and the promotion are the legacy messages of RWB-E1-061 and RWB-E1-058 and keep their wording character for character, except MSG-P10-008, whose text is that of the Error and Message Standard v4; MSG-P4-002 and MSG-GEN-004 are the platform messages of a right and of a state already reached. This contract adds no message. Thai text for each message follows decision DL10. Decision DL10 is open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive. Screen SCR-46 has four states in this contract: empty, loading, error and no access; the no-access state shows MSG-P4-002, and the empty, loading and error states carry no message, Not specified in the source documents (DOR-RWB-P10-E1061-CON-10).

### 15. Screens and states

None in this story. The contract serves the report export for the steering committee pack and the version reads of the configuration operations: both are reached through the gateway-bff route (DP-19) and belong to RWB-P10-E1061-APP and RWB-P10-E1058-CON. The contract fixes no screen field, no order and no masking rule, and the agent monitor screen SCR-46 and the autonomy screen of Epic 3 are untouched. The route name and path of the gateway-bff route are Not specified in the source documents (GAP-0613; ASM-0872). The states of SCR-46 are empty, loading, error and no access; Screen Specifications v1 defines none of them, so their content is Not specified in the source documents (CG-ALL-2604), apart from the no-access message that section 14 names.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E1061-CON-01 | AC1 | Contract | The three evaluation operations validated against their schema: the query, the answer members of the report, the 202, 200 and 409 answers, and no answer on the legacy monolith base |
| TC-P10-E1061-CON-02 | AC2 | Contract | The L1 payload for policy "INTAKE" version "P2": kind POLICY, the four promotion members, the run binding to "EV-INTAKE-001", a payload without a run, a run of another agent and a run that is not DONE |
| TC-P10-E1061-CON-03 | AC3 | Contract | The approval of version "P2" by RW-RISK with a valid from date, the 200 answer, the 404, the 409 of MSG-GEN-004 and the 409 of MSG-P7-002 for the loader "coe.user01" |
| TC-P10-E1061-CON-04 | AC4 | Contract | `rwb.agent.events.v1` with EV-28: the envelope, the key, the subject, the payload members, the retry and `.dlt` topics, a registry refusal, and no message after an evaluation reaches DONE |
| TC-P10-E1061-CON-05 | AC5 | Contract | The four fakes: the minimum sample 200, the version that raises it, the missing minimum, the three lists, the list without L1, the two delays and the 200-run fixture |
| TC-P10-E1061-CON-06 | AC6 | Contract | The nine sub-tables complete with None where empty, the ownership of each shape, and a drift test between each fake and this document |
| TC-P10-E1061-CON-07 | AC6 | Contract | The boundary of the tables of 12.7: each table with no row and with its None members where empty, and the owner of each table |
| TC-P10-E1061-CON-08 | AC7 | Contract | BR1 to BR9 of section 8, each with the test case named in its Covered by cell |
| TC-P10-E1061-CON-09 | AC8 | Contract | A request without an authenticated identity on each provided operation: the 401 answer and the platform error envelope |
| TC-P10-E1061-CON-10 | AC9 | Contract | A write sent twice with the same idempotency key, and the answer to the replay as the replay rule states it |
| TC-P10-E1061-CON-11 | AC10 | Contract | The parameters fake and the reference-data fake with a delay beyond 2 s, and a consumed call that fails: the refused load and its error |

TC-P10-E1061-CON-01 to TC-P10-E1061-CON-11 are new (D-RCV-60) and test only the deliverables of this story: the three operation shapes, the L1 payload and its binding, the approval, the topic declaration, the four fakes, the completeness and boundary of section 12, the coverage of the business rules, the 401 answer, the replay of a write and the failed consumed call. They add no `-ITG` copy, because this key carries no integration dependency and the story set holds no integration story for it; the cross-service behaviour is proved against the fakes.

### 17. Guardrails

- No business value in the contract: the minimum sample 200, the check list, the three lists, the conditions, the measures and the run identifiers stay rows of the parameter, reference and policy tables, and the contract only names them (BR5).
- No personal data in a payload, an example or a fake: identifiers, facts and rates only, and the report body is never copied into the L1 payload (BR9).
- Of the EV-28 payload members of section 12.3, runid (run ID, DF-AGT-036), agent (agent_code, DF-AGT-037), caseid (case_id, DF-AGT-041) and fallback (DF-AGT-047) are classed Not personal on their `agent_run` rows in Data Classification and Personal Data Inventory v5; the class of outcome is Not specified in the source documents (DOR-RWB-P10-E1061-CON-11). A same-named column of another table does not change the class of these fields.
- The contract names the agent base and the agent topic as rwb-agent's and consumes every other operation and topic; a document that declares another service's path or topic as provided fails the review (BR8, DP-13, DP-14).
- The configuration operations and the policy resource are restated, never redefined: the baseline RWB-P10-E1058-CON owns them and a drift is corrected there (BR3, X6).
- Every payload is validated against its registry subject before the relay, and a refusal is routed to `.dlt` and alerted with the retry topics in between (BR7).
- An event is declared only where a source names it: the completion of an evaluation publishes no message, and no unowned event type is invented (BR6, ASM-0875).
- Every fixture is synthetic; no production run, report, policy version or customer value is copied into a schema, a payload or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | The minimum sample and the check list read through the parameters contract; the three lists read through the reference-data contract; the four promotion members as columns, not code | TC-P10-E1061-CON-02, TC-P10-E1061-CON-05 |
| REQ-DRI-011 | Every versioned table has valid from and to dates, author and approver | The approval operation with approved_by and valid_from, and the four promotion members on the version row | TC-P10-E1061-CON-02, TC-P10-E1061-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three provided operations, the two consumed reads and their budgets | TC-P10-E1061-CON-01, TC-P10-E1061-CON-05 |
| ADR-021 | Per-service Flyway and migration ownership | `V10_004__policy_promotion.sql` in the rwb-agent sequence, in `rwb_agent` only | TC-P10-E1061-CON-06 |
| D-RCV-60 DP-06 | Parameters read through the rwb-case contract | The parameters fake and the promotion values it answers | TC-P10-E1061-CON-05 |
| D-RCV-60 DP-07 | Reference data read through the rwb-case contract | The reference-data fake and the three lists it answers | TC-P10-E1061-CON-05 |
| D-RCV-60 DP-09 and DP-14 | Kafka with outbox, inbox and CloudEvents on the owner's topic | The AsyncAPI document of `rwb.agent.events.v1` with EV-28, its registry subject and its `.dlt` route | TC-P10-E1061-CON-04 |
| D-RCV-60 DP-13 | One REST base per service | The base `/api/recovery/agent/v1` for the three provided operations | TC-P10-E1061-CON-01 |
| RWB-E1-061 (legacy story) | Intake agent evaluation and L1 proposal [E2a]: the report, the proposal, the checks and the approval | The report members, the four promotion members, the three checks and the separation-of-duty refusal | TC-P10-E1061-CON-01, TC-P10-E1061-CON-02, TC-P10-E1061-CON-03 |

The gap GAP-0613 records the areas the sources leave open for this contract - the name of an evaluation-completed event, the nested types of the promotion members, the type detail of the report members, the route path of the gateway-bff route and the shape of the config approval answer - and each default it raises is settled by ASM-0872, ASM-0875, ASM-0876 and ASM-0877.

### 19. Out of scope

- The implementation of the report, the promotion checks and the version row (RWB-P10-E1061-APP).
- The whole agent runtime contract, the policy and prompt resources and the full shape of the configuration operations (RWB-P10-E1058-CON).
- The evaluation harness that produces the runs and the extraction evaluation (RWB-P10-E1060-APP).
- The parameter rows, the reference rows and their versions (P3 rwb-case, RWB-P3-E1042-CON and RWB-P3-E1043-CON).
- The access rights and the guard library (P4 rwb-access), the topic provisioning and the consumer groups (RWB-PLT-EVT), and the deployment, dashboards and runbook of this key.
- An event for the completion of an evaluation, whose name is Not specified in the source documents (GAP-0613; ASM-0875).
- The nested types of `promotionConditions` and `watchMeasures`, the type detail of the report members and the route path of the gateway-bff route, which are Not specified in the source documents (GAP-0613; ASM-0872, ASM-0876, ASM-0877).
