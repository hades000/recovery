# RWB-P10-E2028-CON Case intake agent live at L1 [E3a]

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2028-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP07, DP09, DP10, DP13, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P10-E2028-CON-16) |
| Depends on (build) | None; the six platform contracts named in section 3 (RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) are delivery prerequisites, not per-story blockers |
| Contract dependencies | RWB-P3-E1043-CON; the published P3 case read and P4 authorise call |
| Contract version | v1, path base `/api/recovery/agent/v1` (DOR-RWB-P10-E2028-CON-23) |
| Readiness decisions | RD-P1-005, RD-P1-008, RD-P1-041 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- The decision event type reads `rwb.decision.DecisionRecorded.v1`; the topic `rwb.decision-record.v1` is unchanged (RD-P1-008).
- The consumed freshness read and its fake carry status `LOADED` / `STALE` and the never-stamped answer (RD-P1-005, RD-P1-041).

**Change log.** D-RCV-60, 22 November 2026: contract slice of RWB-E2-028 for rwb-agent, split from the legacy key. This document fixes the seam of the L1 intake capability on Day 1 and builds no behaviour: the agent-outputs read and the feedback operation on the base `/api/recovery/agent/v1` (DP-13), the L1 answer element with its run, agent, version, mode, status, summary, gaps, confidence, data date and feedback members, the L1 request and its outcome members with the row version and the item key, the segment eligibility answer that turns the mode of the approved `agent_policy` row of schema `rwb_agent` into a contract (DP-07 for the reference values it reads), the decision-record mapping of a verdict with its idempotency key through the local library and the shared topic `rwb.decision-record.v1` (DP-03), the event contract of `rwb.agent.AgentRunCompleted.v1` and of the L1 acceptance record on `rwb.agent.events.v1` with the retry and `.dlt` topics (DP-09), the event-started workflow registration the answer depends on (DP-10), the migration that creates `agent_feedback` in the service's own Flyway sequence (DP-15), the gateway-bff route in front of the two operations (DP-19), the four fakes and the error taxonomy. It carries no legacy criterion of its own: the nine criteria of RWB-E2-028 stay with RWB-P10-E2028-APP and its eleven legacy test cases with it. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 15 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the L1 intake capability fixed as a contract on Day 1: the agent-outputs read and the feedback operation on the base `/api/recovery/agent/v1` with their rights, their idempotency and their refusals, the L1 answer element and the L1 request and outcome members with their names and types, the segment eligibility answer that says whether a case of a segment is served at L1 or left in shadow, the decision-record mapping of a verdict with its idempotency key, the event contract of `rwb.agent.AgentRunCompleted.v1` and of the L1 acceptance record on `rwb.agent.events.v1` with the retry and `.dlt` topics, the event-started workflow registration the answer depends on, the gateway-bff route, the four fakes and the error taxonomy**, so that **the app story, the deployment story, the monitor of this service and every caller of an agent output build against one agreed, testable shape without waiting for a run to succeed, and no caller is offered a mode, a member or a status that the service does not serve**.

### 2. Business rationale

The legacy key RWB-E2-028 was written against objects inside the monolith: an in-process `CaseQueryService` answered the case facts and the owner check, a loader table beside the code held the mode per segment, a `DecisionLogWriter` of the same deployment wrote the decision log, the panel called `CaseAgentOutputController` directly on the monolith base, and the acceptance figures were read from a nightly copy. In the target each of those is a boundary or is gone:

- The case facts, the owner, the team scope and the reference values are rwb-case's, so the read and the verdict cross a REST contract with one hop and a 2 s client budget (DP-07, DP-11 behind it).
- The mode, the segment, the segment threshold and the confidence floor are columns of the approved `agent_policy` row of schema `rwb_agent` (DP-01, DP-15). The contract has to say what the read answers for a segment that is still in shadow, or an app and a screen will each invent a different empty answer.
- The decision log is the local record of DP-03 published on `rwb.decision-record.v1` and sealed in the central ledger of rwb-decision, so the mapping of a verdict to a record and the key that stops a second verdict are contract, not implementation.
- The run is an event-started Temporal workflow on the queue `rwb-agent` (DP-10) and the facts leave as CloudEvents on `rwb.agent.events.v1` through the outbox (DP-09), so the event payloads are contract as well.
- A screen reaches the two operations only through the gateway-bff route (DP-19).

Contract-first only works if the seam is written once. The seam here is small and load-bearing: one read whose answer carries the summary, its gap flags and the recorded verdict; one verdict operation with its request, its outcome and its two refusals; one eligibility answer that decides L1 against shadow; one record mapping with its key; two event payloads with their retry and `.dlt` topics; one route; and one fake set that makes the app, the deployment and the monitor testable on Day 1.

If the shape is agreed and faked on Day 1, four teams move at once. RWB-P10-E2028-APP builds the mode resolver, the read, the verdict path and the record against these fakes; RWB-P10-E2031-APP counts its acceptance and override rates from the same event and entry facts; the rwb-case story RWB-P3-E1035-CON knows what the service asks of the case record and the case-decision proposal; and RWB-P10-E2028-OPS registers the queue, the topic and the rights against the same names. Without it, each caller invents its own empty answer for a shadow segment, the acceptance count of the monitor and the feedback row drift apart, and a second verdict slips through.

This story defines the provided side of the two operations and the consumed side of the seam, and never restates what another owner holds: the case, the case-decision proposal and the reference data are rwb-case's, the entry and its sealing are rwb-decision's, the business date is rwb-source-data's, and the platform envelopes are the platform's (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the REST base, the topic and the event names follow the platform rule and not a local choice (§R4; DP-13).
- The CloudEvents 1.0 envelope, the registry subject check, the retry topic and the `.dlt` rule are the platform baseline of RWB-PLT-TE006-CON, and this document narrows them where it must and says so (DP-09).
- The workflow kit of RWB-PLT-E1071-CON publishes the event-started workflow registration with namespace `rwb-recovery`, the activity contract and the worker versioning (DP-10).
- The decision-record library of RWB-PLT-E1027-CON publishes the record type, the writer, the `rwb.decision-record.v1` topic and its retry and `.dlt` rule (DP-03).
- The reference-data client library of RWB-PLT-E1043-CON is published, and the per-service Flyway sequence of RWB-PLT-E1044-CON fixes the migration naming this document uses (DP-07, DP-15).
- The gateway-bff route contract of RWB-PLT-N001-CON is published with its stub (DP-19).
- The two E3 operations of TSD P10 Agent runtime v2 T-A.1 (API-P10-010 `GET /cases/{caseId}/agent-outputs` first in E3 and API-P10-011 `POST /agent-runs/{runId}/feedback` first in E3) are the operations this document shapes; the platform baseline of the service is RWB-P10-E1058-CON and the L1 proposal payload is RWB-P10-E1061-CON, both named here as context and neither claimed as a build dependency.
- The rwb-case contracts of RWB-P3-E1035-CON and RWB-P3-E1043-CON and the rwb-decision contract of RWB-P7-E1027-CON are known, and the rwb-source-data freshness read of Arch v5 slide 15 is known; each is consumed as a boundary and none is a build dependency of this story.
- The field names of the eight P10 tables and of `agent_feedback` are those of TSD P10 Agent runtime v2 T3.1 (DF-AGT-001 to DF-AGT-111).
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W2. The service identity of rwb-agent is the agent service identity (DP-02), with grants on rwb_agent only, until the platform fixes its login (GAP-0622; ASM-0916). The Enterprise AI test tenant, guardrail profile, harness pack, seeding and evidence format are to be agreed with the P10 owner, the platform team and QA at the wave 2 contract review (GAP-0410).

### 4. Flow

1. Draft the two operations that replace the legacy controller: the agent-outputs read and the feedback operation, their method, their path under `/api/recovery/agent/v1`, their rights, their idempotency and their refusal codes.
2. Fix the L1 answer element: the run, the agent, the version, the mode, the status, the summary, the gap flags with their reasons, the confidence, the data date and the feedback, with the empty answer defined for a case with no L1 output and for a segment in shadow.
3. Fix the L1 request and its outcome: the item key with its default, the three verdicts, the reason rule and its length, the row version on the request, the outcome element and the second-verdict refusal.
4. Fix the segment eligibility answer that turns `autonomy_mode`, `segment_product_group`, `segment_region_code` and the confidence floor of the approved policy row into a contract, and say what a caller learns when the segment is SHADOW or the row carries no mode.
5. Fix the decision-record mapping of a verdict: the case, the decision code, the agent version, the model version, the run reference as the inputs snapshot, the recommendation, the final call, the reason and the approver, with the idempotency key that makes one record per run and item.
6. Fix the two event payloads on `rwb.agent.events.v1` with their envelope, their key, their members, their registry subject, the retry topic and the `.dlt` topic, and the record the library publishes on `rwb.decision-record.v1`.
7. Fix the workflow registration the answer depends on: the event-started `AgentRunWorkflow` on the queue `rwb-agent` in namespace `rwb-recovery`, its two activities and the statement that no Schedule exists for a cadence.
8. Fix the gateway-bff route in front of the two operations, one hop, with the refusal passed through, and name its path as open with the edge owner.
9. Write the four fakes — rwb-case, rwb-decision with the record side, rwb-source-data and the gateway-bff route — the error taxonomy of section 12.1, and publish the nine sub-tables with the contract tests of section 16.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of the L1 answer element or of the L1 request drifts from this document: a renamed member, a retyped date, a dropped gap reason | The contract test fails and the merge is blocked | None | AC1, AC2, AC3 |
| X2 | A request member is missing, the item key is outside the list, or the verdict is outside ACCEPTED, CORRECTED and REJECTED | The operation refuses with 422 and names the member; nothing is read or written | MSG-GEN-001 | AC3, AC8 |
| X3 | The read is declared for a segment in shadow, or the contract answers an L1 output without naming the mode of the policy row that allowed it | The review refuses the document, because a shadow output is never served | None | AC4 |
| X4 | The record mapping drops a member the ledger needs, or the idempotency key stops being one record per run and item | The contract test against the library fails and the mapping is corrected | None | AC5 |
| X5 | A payload gains a personal field, or fails its registry subject | The data-steward review and the contract test refuse the payload; a produced message that fails is routed to `.dlt` with an alert | None | AC6 |
| X6 | The route in the document drifts from the registration of RWB-P10-E2028-OPS, or a screen path reaches the service directly | The contract test between the document and the registration fails and one of the two is corrected; the deployment owns the registration | None | AC7 |
| X7 | A field-level detail of a consumed operation, of a payload member or of a path is missing from the source material | The element carries the placeholder, one gap row and one assumption row, and the fake is written to the assumed shape | None | AC1, AC5, AC6, AC7, AC8 |
| X8 | A fake drifts from this document, or a refusal code of section 12.1 is answered with another code | The contract test fails on the fake and on the error taxonomy | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the workflow kit, the decision-record library, the reference-data library and the route contract as published |
| Negotiable | Field-level detail of the consumed operations, the page size (there is none) and the route path are settled with their owners; the read shape, the request and outcome members, the eligibility answer, the record mapping and the event payloads are fixed by this realignment |
| Valuable | Unblocks the app, deployment and monitor stories of this key on Day 1 and gives every caller of an agent output one shape, including the empty answer of a shadow segment |
| Estimable | Two provided operations, one eligibility answer, one record mapping, three event payloads, one workflow registration, one route, four consumed boundaries and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the schema file, the payload, the fake, the document — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Case intake L1 contract slice for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the decision-record library of RWB-PLT-E1027-CON and the workflow kit of RWB-PLT-E1071-CON are in force
    Given the target environment is SIT

  Scenario: AC1 The two L1 operations are contracted on the agent base (new, D-RCV-60)
    Given the contract files of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When the panel of the case record asks for the outputs of case "RW-2027-000501" and then records a verdict on its run
    Then one operation answers on GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs with 200 and an AgentOutput[] in the member names and types of this document
    Then the other answers on POST /api/recovery/agent/v1/agent-runs/{runId}/feedback with 200 and the same AgentOutput with its feedback set
    Then the read declares Case record R and no idempotency, and the verdict declares Case record U with an Idempotency-Key header and the If-Match row version
    Then both are one hop under the base with the 2 s client budget of DP-11 to the caller
    Then a difference between either operation and this document fails the contract test

  Scenario: AC2 The L1 answer element is fixed member by member (new, D-RCV-60)
    Given the answer element declared in this document
    When the outputs of case "RW-2027-000501" are read
    Then each element carries runId, agent "INTAKE", agentVersion "INTAKE@P2/PR3", mode "L1", status, summary, gaps with gapType and reason, confidence, dataAsOf and feedback
    Then the gaps MISSING_DOCUMENT and NO_VALID_APPRAISAL answer with their reasons and the element carries the marker "Agent output"
    Then a case with no L1 output answers an empty array, and a case whose segment is in shadow also answers an empty array and never a shadow summary
    Then dataAsOf is the date the run used, so a caller can compare it with the business date without reading the run
    Then the member names and their types are fixed by this document

  Scenario: AC3 The L1 request and its outcome members are fixed (new, D-RCV-60)
    Given the verdict operation of this document
    When a verdict is sent for the summary item of a run of case "RW-2027-000501"
    Then the request carries itemKey with the default "SUMMARY", verdict ACCEPTED, CORRECTED or REJECTED, reason required for CORRECTED and REJECTED and at most 1 000 characters, and the If-Match header with the run row version
    Then the outcome is the AgentOutput of AC2 with feedback set to the verdict, the reason and the recorded date
    Then a verdict outside the three values, a missing item key and an over-long reason are refused with 422 and MSG-GEN-001 naming the member
    Then a request whose If-Match version is stale is refused with 409 and MSG-GEN-004

  Scenario: AC4 The segment eligibility answer is fixed (new, D-RCV-60)
    Given the approved policy row "INTAKE" version "P2" of schema rwb_agent with its autonomy_mode, segment_product_group, segment_region_code, segment threshold and confidence floor
    When the eligibility of a case is asked
    Then the answer carries the case ID, the policy version, the mode of the segment (L1 or SHADOW), the segment it matched, the confidence floor in force and the eligibility outcome SERVED or SHADOW
    Then a case of segment MORTGAGE and BKK answers mode L1 and SERVED, and a case of segment UNSECURED answers mode SHADOW and SHADOW with no summary member
    Then a policy row with no mode, no segment threshold or no confidence floor is refused with 422 naming the missing value and is never answered with a default, and the contract declares no mode, segment, threshold or floor literal of its own
    Then the answer names the product group and the region as values of LOV-PRODUCT and LOV-REGION read through the rwb-case reference-data contract

  Scenario: AC5 The decision-record mapping and its idempotency key are fixed (new, D-RCV-60)
    Given the decision-record library of RWB-PLT-E1027-CON and the shared topic rwb.decision-record.v1
    When a verdict on the summary item of case "RW-2027-000501" is recorded
    Then one record is written with case_id, decision_code "D6", agent_version "INTAKE@P2/PR3", model_version, inputs_ref equal to the run reference, recommendation, final_call equal to the verdict, override_reason equal to the reason and approver_user_id equal to the owner
    Then the record and the agent_feedback row are written in one transaction and the entry ID is carried back to the feedback row
    Then the idempotency of the verdict is one record per run and item key, a repeat answers 409 and MSG-GEN-004, and no second record and no second feedback row exist
    Then a record that cannot be written refuses the verdict with 503 and MSG-P7-003 and stores no feedback row

  Scenario: AC6 The event contract of the run and of the acceptance is declared (new, D-RCV-60)
    Given a run of agent "INTAKE" for case "RW-2027-000501" and the verdict recorded on its summary
    When the outbox relay publishes
    Then the message types are rwb.agent.AgentRunCompleted.v1 and rwb.agent.AgentFeedbackRecorded.v1 on rwb.agent.events.v1, keyed by the case ID, each with the retry topic and the .dlt topic of the agent topic
    Then each envelope carries id, source, type, specversion, time, subject and datacontenttype, with the run ID as the subject
    Then the completion payload carries the run facts of the agent_run fields of TSD P10 Agent runtime v2 T3.1 and the acceptance payload carries the run ID, case ID, item key "SUMMARY", verdict, agent version, entry ID and recorded time
    Then the decision record of AC5 is declared on rwb.decision-record.v1 through the library and carries no daily copy and no lake write
    Then a payload that fails its registry subject is refused before the relay and routed to .dlt with an alert, and no personal data is carried
    Then the name of the acceptance event is fixed under the naming rule of §R4, because the catalogue names only AgentRunCompleted

  Scenario: AC7 The workflow registration and the gateway-bff route are fixed (new, D-RCV-60)
    Given the workflow kit of RWB-PLT-E1071-CON and the route contract of RWB-PLT-N001-CON
    When the registration and the route of this document are reviewed
    Then AgentRunWorkflow is registered as an event-started workflow on the task queue rwb-agent in namespace rwb-recovery, with ResolveIntakeMode and RecordIntakeFeedback as its activities
    Then the contract declares no Schedule for a cadence, because a run starts from rwb.case.CaseCreated.v1 and a verdict comes from a person
    Then the gateway-bff route is a pass-through of one hop in front of the two operations, preserving the query, the If-Match header, the media type and the refusal
    Then no screen path reaches rwb-agent directly, and the route name and path are Not specified in the source documents (GAP-0623; ASM-0923)

  Scenario: AC8 The four fakes and the error taxonomy are complete (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables and the four fakes are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then 401, 403, 404, 409, 422 and 503 are declared with the message of each: MSG-P4-002 for 403, MSG-P4-003 for 404, MSG-GEN-004 for 409, MSG-GEN-001 and MSG-P7-005 for 422 and MSG-P7-003 for 503
    Then the fakes rwb-case, rwb-decision with the record side, rwb-source-data and the gateway-bff route answer every consumed path, header and payload of this document
    Then no sub-table declares a lake table, an extract, a lake credential or an INT-19 or INT-20 path
    Then a drift between a fake and this document, or a refusal answered with another message, fails the contract test

  Scenario: AC9 Each business rule BR1 to BR14 is traced to a test case (new, D-RCV-60)
    Given the business rules of section 8 and the test cases of section 16
    When the covers column of section 16 is reviewed against section 8
    Then each rule BR1 to BR14 is named in the covers column of at least one test case
    Then a rule with no test case fails the review

  Scenario: AC10 A redelivered consumed event starts no second run (new, D-RCV-60)
    Given the consumed event rwb.case.CaseCreated.v1 for case RW-2027-000501 and a run already started from it
    When the same event is delivered a second time
    Then no second AgentRunWorkflow is started and no second run is written
    Then the redelivery is answered as a duplicate and the run and its feedback stay as first written
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The two operations are provided by rwb-agent under `/api/recovery/agent/v1` and no caller reads the tables of rwb-agent | DP-11; DP-13; legacy section 12 |
| BR2 | The answer element carries runId, agent, agentVersion, mode, status, summary, gaps, confidence, dataAsOf and feedback, and no member is dropped or renamed without a new version | Legacy section 12; TSD P10 Agent runtime v2 T-A.2 API-P10-010 |
| BR3 | A shadow output is never served: the read answers an empty array for a case whose segment is SHADOW, and the eligibility answer names the mode and the outcome | agent_policy.autonomy_mode (DF-AGT-008); legacy BR1 |
| BR4 | The verdict request carries the item key with its default, the three verdicts, the reason rule with its length and the row version, and its outcome is the answer element with the feedback set | Legacy sections 7 and 12; TSD P10 Agent runtime v2 T-A.2 API-P10-011 |
| BR5 | The record of a verdict maps to the ledger members of this document and is written by the local library in one transaction with the feedback row, then sealed by rwb-decision, which owns `decision_log_entry` | DP-03; ADR-022; R-UNI-39; legacy section 12 |
| BR6 | One record and one feedback per run and item key: a repeat answers 409 and the contract carries both the idempotency key and the row version | agent_feedback unique key (DF-AGT-098, DF-AGT-099); legacy BR5 |
| BR7 | Every event is a CloudEvents 1.0 message on the owner's topic, keyed by the case ID, validated against its registry subject before the relay, with a retry topic and a `.dlt` topic | DP-09; DP-14; Arch v5 slide 42 |
| BR8 | The run is an event-started workflow on the queue `rwb-agent` in namespace `rwb-recovery` and no Schedule is declared for a cadence | DP-10; Arch v5 slides 16 and 44 |
| BR9 | `agent_feedback` is created by `V10_008__agent_feedback.sql` in the rwb-agent Flyway sequence of schema `rwb_agent`, with its unique key and its verdict check | DP-15; ADR-021; Ownership Map (agent_feedback owner P10) |
| BR10 | No business value in the contract: the mode, the segment, the segment threshold, the confidence floor, the decision code, the lists and the item key are rows of the policy and of the reference data read through their owners, and the contract only names them | DP-07; §R7.2 s17; legacy section 13 |
| BR11 | One base and one topic per service: this contract declares `/api/recovery/agent/v1`, `rwb.agent.events.v1` and `rwb.agent.<Event>.v1` for rwb-agent and never another service's path or topic as its own | DP-13; DP-14; Arch v5 slide 41 |
| BR12 | The case, the owner, the team scope, the case-decision proposal and the reference values are rwb-case's and are consumed; the entry is rwb-decision's; the business date is rwb-source-data's | DP-01; Template and Rules §R3 default rulings |
| BR13 | The deployment values of rwb-agent are not literals of this contract: the login is a secret reference, the migration runs as a pre-deploy job of the rwb-agent Flyway sequence, and each value no source names stays Not specified in the source documents (GAP-0624) | GAP-0624; legacy RWB-E2-028 sections 3, 4, 5 and 13 |
| BR14 | The gateway-bff route, the topic partitions, retry and retention, the consumer groups and the alert window are not literals of this contract: each is Not specified in the source documents (GAP-2192); rwb-decision, rwb-document, rwb-deviation and rwb-reporting keep their own consumer groups, not created in rwb-agent | GAP-2192; legacy RWB-E2-028 sections 3, 4, 5 and 13 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the answer and request members, the eligibility answer, the record mapping, the event payloads, the registration, the route and the fakes are described | In review |
| In review | Consumer sign-off | The app, deployment and monitor stories of this key accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a header or a payload field is added without removing one | Baselined |
| Baselined | Breaking change to the read, to the request or to a payload | A member or a code of the answer, the request or an event is removed, renamed or retyped | In review, with the owner of the affected contract |
| Baselined | Drift in a fake, in a refusal code or against a consumed owner | A contract test fails | In review |
| Baselined | The record type or the envelope changes | RWB-PLT-E1027-CON or RWB-PLT-TE006-CON publishes a new shape | Baselined, aligned to the library |

These are the states of this document, not of a case or a run. The run states are ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, TOOL_UNAVAILABLE, MODEL_ERROR and DISABLED (LOV-AGENT-RUN) and belong to the app story; the verdict states are ACCEPTED, CORRECTED and REJECTED (LOV-FEEDBACK).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the read shape, the request and outcome members, the eligibility answer, the record mapping, the event payloads, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to the operations, the members, the mapping or a payload, and any change to the registration |
| The rwb-case owner | Owns the case record, the case-decision proposal and the reference data, and signs off the shapes taken from its documents |
| The rwb-decision owner | Owns the central ledger, the entry and the sealing, and signs off the record mapping and the record payload |
| The rwb-source-data owner | Owns the freshness read and signs off the business-date member |
| The app, deployment and monitor stories of this key | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule, the decision-record library, the workflow kit and the route contract |
| Data steward | Confirms that no personal data field is declared in the answer, in the request or in an event |

The identity that consumes the case record, the reference data, the entry and the freshness read is the rwb-agent service identity (DP-02); its name is the rwb-agent login (DP-02), with grants on `rwb_agent` only, and is fixed with the deployment story.

The two operations are authorised through the rwb-access authorise check (DP-08) before any read or write, and no caller is served an answer without it.

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Read query | The case ID in the path; no query member and no paging | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |
| Answer element | runId, agent, agentVersion, mode, status, summary, gaps[{gapType, reason}], confidence, dataAsOf, feedback{verdict, reason, recordedAt, decisionEntryId}; the REST member types, the lengths of summary, gapType and reason beyond the table, and the form of the feedback member are Not specified in the source documents (GAP-0623) | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |
| Empty answer | An empty array for a case with no L1 run and for a case whose segment is SHADOW | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |
| Verdict request | itemKey (default "SUMMARY", the only item of an intake output; GAP-0622; ASM-0919), verdict ACCEPTED, CORRECTED or REJECTED, reason (required for CORRECTED and REJECTED, at most 1 000 characters), If-Match header with the run row version | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |
| Verdict outcome | The answer element of the run with `feedback` set; a repeat for the same run and item answers 409 MSG-GEN-004, the unique key checked first and the If-Match version second (GAP-0623) | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |
| Eligibility answer | caseId, policyVersion, mode L1 or SHADOW, segmentProductGroup, segmentRegionCode, confidenceFloor, outcome SERVED or SHADOW | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |
| Record mapping | case_id, decision_code "D6", agent_version "INTAKE@P2/PR3", model_version, inputs_ref (the run reference), recommendation, final_call (the verdict), override_reason, approver_user_id; the D6 record is written through the local decision-record library with this mapping (GAP-0622); the decision-log append request and answer are Not specified in the source documents (GAP-1294), and the reads, LOV-DECISION value D6, the three-verdict list, the reason codes, MSG-P7-009 and the rwb-decision login are to be agreed at the wave 2 contract review (GAP-1294) | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |
| Event payloads | agent, caseid, fallback, outcome, runid for `AgentRunCompleted` (EV-28); run ID, case ID, item key, verdict, agent version, entry ID and recorded time for `rwb.agent.AgentFeedbackRecorded.v1`; the record as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed by the case ID, with the retry and `.dlt` topics | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |
| Consumed values | LOV-PRODUCT, LOV-REGION, LOV-AUTONOMY, LOV-FEEDBACK, LOV-DECISION, LOV-AGENT and LOV-AGENT-RUN through the reference-data contract; the business date through the freshness read; the business date of the stale check is Not specified in the source documents (GAP-0622) | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |
| Refusal | the platform problem response: status, code, detail and the message ID when a business message applies; a verdict outside LOV-FEEDBACK is refused with 422 | Not specified in the source documents (DOR-RWB-P10-E2028-CON-7) |

The type and length of `summary`, the nested type of each gap reason, the form of `recordedAt` and `dataAsOf` beyond a date, and the member names of the eligibility answer beyond those named here are Not specified in the source documents (GAP-0623; ASM-0924); this document fixes the member names and leaves the types to the review with their owners. No table of any schema is declared as an answer source: the read answers from `rwb_agent` and every other fact comes through its owner (DP-01).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Rights | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/agent-outputs` | Read the L1 agent outputs of a case: `AgentOutput[]` with the members of section 11; an empty array when no L1 output exists or the segment is in shadow; 200 | Case record R, scope applied; 401, 403 (MSG-P4-002), 404 (MSG-P4-003), 503 | Not applicable: the call writes nothing |
| POST | `/agent-runs/{runId}/feedback` | Record the owner's verdict on one item of an L1 output: AgentFeedbackRequest; 200 AgentOutput with the feedback set | Case record U, scope applied; 401, 403 (MSG-P4-002), 404 (MSG-P4-003), 409 (MSG-GEN-004), 422 (MSG-GEN-001, MSG-P7-005), 503 (MSG-P7-003) | Idempotency-Key header; one feedback per run and item key; a repeat returns 409 |

**Error taxonomy.** 401 no session and no body member; 403 the caller's role lacks the Case record right, with MSG-P4-002; 404 an unknown case, an unknown run or a case outside the caller's scope, with MSG-P4-003; 409 a second verdict for the same run and item, or an `If-Match` version that is not the current one, with MSG-GEN-004 and with the unique key of `agent_run_id` and `item_key` checked first (GAP-0623; ASM-0925); 422 a missing or out-of-list `itemKey`, a verdict outside the three values or a reason that is missing or longer than 1 000 characters, with MSG-GEN-001 for the request member and MSG-P7-005 for the reason (GAP-0623; ASM-0920); 503 the store, the decision-record library or a consumed owner unavailable, with MSG-P7-003. Every refusal is the platform problem response and carries the message ID of the business message where one applies. The configuration operations and the L1 proposal payload of RWB-P10-E1061-CON and the metric read of RWB-P10-E2031-APP are provided by their own documents and are not re-declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case (RWB-P3-E1035-CON) | The case facts, the owner and the team scope the read and the verdict are checked against, and the source of the product group and region the eligibility answer compares (DP-07) |
| POST | the case-decision proposal operation of rwb-case: Not specified in the source documents (GAP-0623) | P3 rwb-case (RWB-P3-E1035-CON) | The verdict proposed to the case record, so the answer's `feedback` and the case record agree |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | LOV-PRODUCT, LOV-REGION, LOV-AUTONOMY, LOV-FEEDBACK, LOV-DECISION, LOV-AGENT and LOV-AGENT-RUN, checked before a member is answered or a verdict stored (DP-07) |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision (RWB-P7-E1027-CON) | The sealed entry a verdict's record became, carried as `decisionEntryId` and counted by the monitor |
| GET | `/data-products/freshness` | P1 rwb-source-data | The business date of the source data, being the published operation for the `GET /freshness` of Arch v5 slide 15; the business date of the stale check is Not specified in the source documents (GAP-0622). Per product the answer carries `status` `LOADED` or `STALE` from the stamp in use (the latest stamp row); a never-stamped product answers `businessDate` null with `status` `STALE` (rwb-source-data.yaml 5.1.0; RD-P1-005, RD-P1-041) |

Every operation is one hop with a 2 s client budget (the one-hop rule behind every consumed read, DP-11 behind DP-07). The record itself is not a REST call: it is written by the library of RWB-PLT-E1027-CON and sealed by rwb-decision.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | agent, caseid, fallback, outcome, runid |
| `rwb.agent.AgentFeedbackRecorded.v1` | `rwb.agent.events.v1` with the retry topic and the `.dlt` topic | P10 | the case ID | run ID, case_id, item_key, verdict, agent_version, decision entry ID, recorded_at |
| DecisionRecorded, the decision-record type of the library | `rwb.decision-record.v1`, the shared decision-record topic, with its retry and `.dlt` rule | P7 rwb-decision owns the central ledger; the library of RWB-PLT-E1027-CON owns the envelope | the case ID | the record of a verdict with the members of section 11 |

All three are inserted in the outbox in the same transaction as the row they describe and relayed by the outbox library; the payload is validated against its registry subject before the relay and a refusal is routed to the `.dlt` topic with an alert (DP-09; BR7). No personal data is carried. `AgentRunCompleted` is EV-28 of Arch v5 slide 43; `AgentFeedbackRecorded` is fixed under the naming rule of §R4 because the catalogue names one event of the topic (GAP-0623). No daily event and no lake copy is declared.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Use | Rule |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 rwb-case | The event that starts the run the answer reads, keyed by the case ID | Dedupe on the event ID in the inbox; one run per case and event |

No other topic is consumed by the seam this document fixes. The case, the lists, the entry and the business date are read through their owners' REST contracts (DP-11).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow, event-started, one execution per case and triggering event, workflow ID = the case ID and the event ID | `rwb-agent` | Input: agent code "INTAKE", case ID, trigger event "CaseCreated", event ID, idempotency key and the resolved mode. The 60-second policy budget, then the rule result (R-UNI-32) |
| ResolveIntakeMode | Activity | `rwb-agent` | Input: the case ID and the approved policy row. Output: mode L1 or SHADOW, the policy version, the segment and the confidence floor, or the refusal of X3 |
| RecordIntakeFeedback | Activity (workflow kit, one transaction) | `rwb-agent` | Input: the verdict, the reason, the run row version and the case proposal. Output: the record, the feedback row and the outbox row, or no write at all |

The workflow and the queue are those of Arch v5 slide 16; the two activity names are this document's and are accepted by RWB-P10-E2028-APP.

#### 12.6 Schedules

None. The contract declares no Schedule for a cadence: a run starts from `rwb.case.CaseCreated.v1` through the event-started registration of 12.5, and a verdict comes from a person (DP-10; BR8). The lease of the legacy Quartz entry is retired with the stage and no job table is named.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_feedback | P10 (`rwb_agent`) | The verdict row of the request and the `feedback` member of the answer; created by `V10_008__agent_feedback.sql` with unique (agent_run_id, item_key) and the verdict check |
| agent_run | P10 (`rwb_agent`) | The run facts of the answer and of the completion payload; no column added |
| agent_policy | P10 (`rwb_agent`) | The approved row whose mode, segment, segment threshold and confidence floor the eligibility answer reads; no column added |
| agent_prompt | P10 (`rwb_agent`) | The approved prompt version carried in `agentVersion`; read only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox, inbox and idempotency envelope of the events and of the verdict (DP-09) |

No table of another service is declared and no foreign key crosses a schema (DP-01). `recovery_case`, `assignment`, `reference_row` and `reference_version` are P3's, `decision_log_entry` is P7's, and each is reached through its contract. The migration runs in the rwb-agent Flyway sequence of `rwb_agent` and touches no other schema (DP-15; BR9).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock | Cases "RW-2027-000501" to "RW-2027-000503" with product group MORTGAGE and region BKK in the caller's scope; "RW-2027-000601" in team HP-NE outside it; "RW-2027-000701" with segment UNSECURED; the case-decision proposal with its accepted answer and its 404; LOV-PRODUCT with UNSECURED, LOV-REGION, LOV-AUTONOMY, LOV-FEEDBACK, LOV-DECISION with "D6", LOV-AGENT and LOV-AGENT-RUN; a delay beyond 2 s | Contract tests, app story, monitor story |
| rwb-decision WireMock and decision-record stub | One sealed entry per feedback with decision "D6" and agent version "INTAKE@P2/PR3"; an unknown entry; a failed record write for the 503; a `.dlt` route on a permanent relay failure | Contract tests, app story, monitor story |
| rwb-source-data WireMock | Business date 2027-01-28 over the ACE load of 2027-01-26; a business date equal to the data date; stamps with `status` `LOADED` and `STALE`, and a never-stamped answer (`businessDate` null, `status` `STALE`); a failed answer; a delay beyond 2 s | Contract tests, app story |
| gateway-bff route stub | A pass-through route in front of the two operations, one hop, with the query, the `If-Match` header and the media type preserved, and the 403, 404, 409, 422 and 503 passed through unchanged | Contract tests, app story, deployment story |

The outbox stub, the workflow kit stub, the access guard stub and the model gateway stub are the platform's and are used but not declared here. Every fixture is synthetic and holds no personal data.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The agent-outputs read and the feedback operation provided; the case read, the case-decision proposal, the lists, the entry read and the freshness read consumed, one hop and 2 s each |
| Kafka | 3 published, 1 consumed | `AgentRunCompleted`, `AgentFeedbackRecorded` and the decision record on their topics with retry and `.dlt`; `CaseCreated` consumed |
| Temporal | 1 workflow, 2 activities, 0 Schedules | AgentRunWorkflow with ResolveIntakeMode and RecordIntakeFeedback on the queue `rwb-agent`, event-started |
| File | None | No file is read or written and no extract exists: the answer is the body of the read and the feed is the topic |

### 13. Solution plan

**Deliverables.** `contract/agent-outputs-read.yaml` (the read, its rights, its empty answer and its refusals), `contract/agent-output-element.md` (the answer element and its members), `contract/agent-feedback.yaml` (the verdict request, its outcome and its headers), `contract/agent-segment-eligibility.md` (the eligibility answer and its refusal), `contract/agent-decision-mapping.md` (the record mapping and its idempotency key), `contract/agent-events.asyncapi.yaml` (the two events and the record on their topics with retry and `.dlt`), `contract/agent-intake-workflow.md` (the event-started registration and its activities), `contract/agent-error-taxonomy.md` (the six codes and their messages) and the four WireMock mappings with their fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON for the app story |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON for the app story; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON for the app story |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts it names are those its consumers add. DP-13 fixes the base and DP-09 and DP-10 fix the topic and the queue; DP-11 sits behind every consumed read and adds no row. DP-01 (the service's own schema) holds behind all of them.

**Components of the document**

| Part | Content |
|---|---|
| Read contract | Method, path under the base, the case ID in the path, no query and no paging, the answer element, the empty answer and the four refusal codes |
| Answer element | The ten members of section 11 with their names and their source field, and the rule that a member leaves only with a new version |
| Verdict contract | The request members, the item key default, the three verdicts, the reason rule, the `If-Match` header, the outcome and the two idempotency rules |
| Eligibility answer | The mode, the segment, the confidence floor and the SERVED or SHADOW outcome, with the refusal when the policy row is incomplete |
| Record mapping | The nine ledger members and the one-record-per-run-and-item rule |
| Event contract | The two events and the record: envelope, key, subject, members, registry subject, retry and `.dlt` |
| Registration | The event-started workflow, the queue, the namespace and the two activities, and the statement that no Schedule exists |
| Route | The pass-through of one hop in front of the two operations and the refusals it preserves |
| Fakes | The four fakes of 12.8 with their answers, their errors and their timings |

**Build steps**

1. Write the read contract and the answer element with the empty answer of the shadow segment and the ten members.
2. Write the verdict contract with its request, its outcome, its headers and its two idempotency rules.
3. Write the eligibility answer with its SERVED and SHADOW outcomes and its incomplete-row refusal.
4. Write the record mapping and the one-record rule against the library of RWB-PLT-E1027-CON.
5. Write the AsyncAPI document of the two events and of the record, with the retry and `.dlt` topics and the registry subjects.
6. Write the registration document of the event-started workflow and its two activities, and state the absence of a Schedule.
7. Write the error taxonomy: the six codes, the message of each and the member that raises it.
8. Write the route document and build the four WireMock mappings with their synthetic fixtures.
9. Add the contract tests of section 16, including the drift test between each fake and this document.

**Done when.** The nine contract files validate in the pipeline, the eight contract tests pass, the four fakes answer every consumed path, header and payload, no sub-table declares a lake artefact, and the app, deployment and monitor stories of this key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required request member is missing, the item key is outside the list or the verdict is outside the three values | Enter {field}. |
| MSG-P7-005 | Correct or Reject with no reason, or a reason longer than 1 000 characters | Enter the reason you are not following the recommendation. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | A second verdict for the same run and item, or a stale row version | Someone else changed this record. Reload it to see their change. |
| MSG-P4-003 | The case or the run is unknown, or the case is outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |

The six texts appear in the sources of this key and keep their wording character for character; MSG-GEN-001 is the platform message of an empty required field. This contract adds no message. In the access test the {action} value is "read an agent summary or give feedback on it", and the 401 refusal carries no business message.

### 15. Screens and states

None in this story. The contract serves the panel "Agent summary" of SCR-03 Case record indirectly: the panel is composed by the gateway-bff route (DP-19) and belongs to RWB-P10-E2028-APP; SCR-46 Agent monitor belongs to RWB-P10-E2031-APP; and both are changed by their own stories. The contract fixes no screen field, no order and no masking rule. States of SCR-03: loading as Screen Specifications v1 defines it; empty, error and no access are Not specified in the source documents (CG-ALL-2703). States of SCR-46: empty, loading, error and no access are Not specified in the source documents (CG-ALL-2704). The exact path of the gateway-bff route in front of the two operations is Not specified in the source documents (GAP-0623; ASM-0923); it is taken from the gateway-bff edge contract RWB-PLT-N001-CON when published.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E2028-CON-01 | AC1 | Contract | The two operations validated against their schema: the base, the paths, the rights, the idempotency, the If-Match header and the four and six refusal codes |
| TC-P10-E2028-CON-02 | AC2 | Contract | The answer element of case "RW-2027-000501" with the two gaps and their reasons; the empty answer of "RW-2027-000701" whose segment is UNSECURED |
| TC-P10-E2028-CON-03 | AC3, AC4 | Contract | The verdict request of the summary item; a verdict outside the three values; a reason of 1 001 characters; the eligibility answer for MORTGAGE/BKK and for UNSECURED; a policy row with no floor |
| TC-P10-E2028-CON-04 | AC5 | Contract | The record of one verdict with its nine members; a repeat for the same run and item answering 409 with no second record |
| TC-P10-E2028-CON-05 | AC6 | Contract | The completion and the acceptance payloads for a run of INTAKE; a status outside LOV-AGENT-RUN; a registry refusal and the `.dlt` route; the record on its own topic |
| TC-P10-E2028-CON-06 | AC7 | Contract | The registration of AgentRunWorkflow with its queue, its namespace and its two activities; the absence of a Schedule; the route pass-through of one hop with the header preserved |
| TC-P10-E2028-CON-07 | AC8 | Contract | The four fakes answering every consumed path, header and payload, and a drifted fake failing the test |
| TC-P10-E2028-CON-08 | AC8 | Contract | The six refusal codes with their messages: 401 without a body member, 403 MSG-P4-002, 404 MSG-P4-003, 409 MSG-GEN-004, 422 MSG-GEN-001 and MSG-P7-005, 503 MSG-P7-003 |
| TC-P10-E2028-CON-09 | §12.7 tables (ASM-3438) | Contract | The boundary of each §12.7 table: its owner schema, the unique key of agent_feedback and the verdict check, and no foreign key across a schema |
| TC-P10-E2028-CON-10 | BR1, BR2, BR3, BR4, BR5, BR6 | Contract | The two operations on the base, the answer shape, the empty answer for a SHADOW segment, the verdict request and outcome, and the one-record and 409 rule |
| TC-P10-E2028-CON-11 | BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 | Contract | The event envelope and topics, the event-started workflow with no Schedule, the migration, the policy and reference values, the single base and topic, the owner of each read, and no unnamed deployment, route or topic value carried as a literal |
| TC-P10-E2028-CON-12 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-P10-E2028-CON-AC9) |
| TC-P10-E2028-CON-13 | AC10 | Contract | Not specified in the source documents (NEWAC-RWB-P10-E2028-CON-AC10) |

The thirteen test cases are this story's own (D-RCV-60) and test the contract artefacts and never a business outcome: the legacy test cases TC-E2-028-01 to TC-E2-028-11 stay with RWB-P10-E2028-APP and are not copied here. Every case runs at Level Contract, because each asserts a schema, a payload, a header, a fake or a refusal and none asserts a stored business row.

### 17. Guardrails

- No business value in the contract: the mode, the segment, the segment threshold, the confidence floor, the decision code, the lists and the item key stay rows of the policy and of the reference data, and the contract only names them.
- No personal data in an event, an answer, a request, an example or a fake: identifiers and facts only, and the fixtures are synthetic.
- The contract names the agent base and the agent topic as rwb-agent's and consumes every other operation and topic; a document that declares another service's path or topic as provided fails the review (DP-13, DP-14).
- No lake table, extract, lake credential or INT-19 or INT-20 path is declared anywhere in this contract.
- Every payload is validated against its registry subject before the relay, and a refusal is routed to `.dlt` and alerted (DP-09).
- The contract declares no Schedule and no job table; the run is event-started (DP-10).
- The record mapping never carries a personal field beyond the owner's identifier, and the library owns its envelope.
- The route is the only way a screen reaches the two operations, and the refusal is passed through unchanged (DP-19).
- Every fixture is synthetic; no production run, summary, case or verdict is copied into a schema, a payload or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision records the agent and prompt versions | The answer element, the record mapping and the acceptance payload carry the agent version and the prompt and model versions | TC-P10-E2028-CON-02, TC-P10-E2028-CON-04, TC-P10-E2028-CON-05 |
| REQ-ACA-005 | Personal data masked by role on every screen and every agent call | The answer element and both payloads are declared with identifiers and facts only, and the fake fixtures hold no personal data | TC-P10-E2028-CON-02, TC-P10-E2028-CON-05 |
| D-RCV-60 DP-03 | Decision record written locally and sealed centrally | The record mapping on `rwb.decision-record.v1` with its idempotency key | TC-P10-E2028-CON-04, TC-P10-E2028-CON-05 |
| D-RCV-60 DP-07 | Reference data read from rwb-case | The eligibility answer names LOV-PRODUCT and LOV-REGION and reads them through the reference-data contract | TC-P10-E2028-CON-03 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | The two events and the record with their topics, their registry subjects, the retry topic and the `.dlt` route | TC-P10-E2028-CON-05 |
| D-RCV-60 DP-10 | Temporal event-started workflows replace Quartz | The registration of AgentRunWorkflow with its queue, its namespace and the absence of a Schedule | TC-P10-E2028-CON-06 |
| D-RCV-60 DP-13 | One REST base per service | The two operations under `/api/recovery/agent/v1` | TC-P10-E2028-CON-01 |
| D-RCV-60 DP-15 | Per-service Flyway sequence | `agent_feedback` created by `Vnnnn__agent_feedback.sql` (next free number of the rwb-agent sequence; Not specified in the source documents (CG-ALL-2702)) in `rwb_agent` | TC-P10-E2028-CON-01, TC-P10-E2028-CON-04 |
| D-RCV-60 DP-19 | gateway-bff composite route | The pass-through route in front of the two operations | TC-P10-E2028-CON-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The read shapes, the request and outcome members and the four fakes | TC-P10-E2028-CON-01, TC-P10-E2028-CON-07 |

The gap GAP-0623 records the areas the sources leave open for this contract — the member types beyond the names, the record event name, the name of the acceptance event, the route path, the 409 rule and the invalid-verdict refusal — and each default it raises is settled by ASM-0920, ASM-0922, ASM-0923, ASM-0924 and ASM-0925. The login, the decision code and the item key of the key are the defaults of GAP-0622, settled by ASM-0916, ASM-0917 and ASM-0919. The behaviour of the seam is RWB-P10-E2028-APP's and the cross-service proof is RWB-ITG-W2's.

### 19. Out of scope

- The implementation of the mode resolver, the read, the verdict path and the record (RWB-P10-E2028-APP).
- The chart, the migration job, the queue and topic provisioning, the consumer groups, the dashboards, the alerts and the runbook (RWB-P10-E2028-OPS).
- The whole agent runtime contract of the service and the shadow run path (the earlier P10 stories and the platform baseline RWB-P10-E1058-CON).
- The L1 proposal payload and the configuration operations (RWB-P10-E1061-CON) and the metric read (RWB-P10-E2031-APP).
- The case of record, the case-decision proposal and the reference data (P3 rwb-case; RWB-P3-E1035-CON, RWB-P3-E1043-CON).
- The central decision ledger, the entry and the sealing (P7 rwb-decision; RWB-P7-E1027-CON).
- The ACE view contract, the extension tables and the freshness read (P1 rwb-source-data).
- The platform envelopes, the decision-record library, the workflow kit and the route contract themselves (RWB-PLT-TE006-CON, RWB-PLT-E1027-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON).
- The panel and the screen composition of SCR-03 and SCR-46 (RWB-P10-E2028-APP, RWB-P10-E2031-APP).
- The end-to-end proof across services (RWB-ITG-W2).
