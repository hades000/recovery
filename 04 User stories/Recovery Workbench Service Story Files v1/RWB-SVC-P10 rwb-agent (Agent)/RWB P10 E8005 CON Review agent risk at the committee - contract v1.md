# RWB-P10-E8005-CON Review agent risk at the committee

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E8005-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-005 for rwb-agent. This is the committee-review read contract slice of the committee pack: the response shape of the two admin reads on `/api/recovery/agent/v1` (DP-13), the CSV and JSON export rule, the committee-outcome members of the decision record written through the local library and `rwb.decision-record.v1` (DP-03), the rule that no personal data appears in a pack, an event, a log or an export, the score-fact read through rwb-source-data's contract (DP-05) and the fakes of the three consumed surfaces. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the committee review fixed as a contract: the response shape of the two admin reads that serve the committee pack, the CSV and JSON export rule, the committee-outcome members of the decision record on `rwb.decision-record.v1`, the rule that no personal data appears in a pack, an event, a log or an export, the score-fact read through rwb-source-data's contract, the errors and rights of TSD T-A.2 and the fakes for rwb-decision and rwb-source-data**, so that **the app story, the edge and the tests build on Day 1 against one agreed, testable shape without waiting for rwb-decision or rwb-source-data to be built**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling rule (DP-11, ADR-020), and a screen composes its answer behind gateway-bff rather than calling owners (DP-19). Both only work if the seam is written down once. The seam here is the one document a committee reads: a pack whose numbers come from the service's own runs, feedback and alerts, whose one external column is read through a contract, and whose outcome is recorded through the library so that it cannot diverge from the ledger.

If the shape is agreed and faked on Day 1, three consumers move at once. The app story builds the fact readers, the exporter and the record writer against the P7, P1 and gateway fakes; the platform edge builds the composite route against the two declared responses and their errors; the tests of this key read one member list rather than each their own. Without it, every consumer reads `AgentRun[]` and `AgentMetric[]` — the type names TSD T-A.2 publishes with no element list — in its own way, and the committee pack becomes a second, unchecked reporting surface.

The contract also states what this service does not own and does not restate: the configuration operations and their load and approval belong to RWB-P10-E3030-CON, the agent runtime, the run step and the guardrail checker belong to RWB-P10-E1058-CON, the record shape and the central ledger belong to P7 rwb-decision, and the ACE score facts belong to P1 rwb-source-data. This story declares the consumed and the provided side of one read surface and nothing else.

### 3. Preconditions

- The service naming rule and the platform error envelope are the platform baseline, so the REST base, the media types and the failure shape follow the platform rule and not a local choice (DP-13; Architecture v5 slide 41).
- The CloudEvents 1.0 envelope and the shared topic `rwb.decision-record.v1` are in force: the record members this contract declares are carried in that envelope with the record reference as the key (DP-03; Architecture v5 slide 42 row 08).
- The decision-record library contract of RWB-PLT-E1027-CON is in force: this document declares the members a committee review contributes and reuses the library's record shape, hash link and outbox rather than redefining them (DP-03).
- The gateway-bff route contract of RWB-PLT-N001-CON is in force: this document declares the two responses the route composes for SCR-46 and the refusal path (DP-19).
- TSD P10 v2 T-A.1 and T-A.2 are the published inventory and detail of the operations: API-P10-001 `GET /admin/agent-runs` with Platform administration R, and API-P10-009 `GET /admin/agent-metrics` with Rules and parameters R. T-A.2 gives the purpose, the query and the response type name only, so the member lists of this contract are an additive extension (GAP-0643; ASM-1043).
- The rwb-source-data contract is published as its owner delivers it: the score-facts operation and its product path are Not specified in the source documents (GAP-0643; ASM-1043) and this document fixes the client rule and the fake, not the path.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7 rule 1), and the two platform contracts and the two owner contracts are consumed as published baselines and not as build dependencies.

### 4. Flow

1. Draft the response contract of the runs read: the members of AgentRunsPack — the runs, the acceptance and override counts, the fallbacks and the failure counts — each named after the TSD column that carries it.
2. Draft the response contract of the metrics read: the members of AgentMetricsPack — one measure set per agent, version, segment and day, with the incidents of the window — and mark every member that T-A.2 leaves open as an additive extension.
3. Fix the export rule: the same rows and the same member order as the read, JSON by default and text/csv on request, a header row formed from the member names, and no member the read does not hold.
4. Fix the committee-outcome members of the decision record and the rule that the record is written through the library before the outcome is shown as taken, one per pack and business date.
5. Publish the personal-data rule as a rubric that a schema check enforces on the pack, the export, the event and the log.
6. Publish the score-fact read rule: one hop, 2 s, through rwb-source-data's contract with no `v_ace_*` view of this service's schema, and a not-available mark instead of a default when the answer fails or is stale.
7. Take the errors and rights of the two reads from TSD T-A.2, state the 422 condition, and state that the Case record R right of the case outputs is not this slice's.
8. Build the three fakes and add the contract tests, including a drift test between each fake and this document.
9. Tag the baseline and hand it to the app story of this key, to the platform edge and to the tests.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response member is added, renamed or retyped without a contract change | The contract test fails and the merge is blocked | None | AC1, AC2, AC8 |
| X2 | A read is called with a parameter the contract does not declare, or with an unreadable date | Refused with 422 before a row is read; the parameter and the value are named in the problem response | None | AC7 |
| X3 | A caller holds neither of the two rights, or lacks the right of the read it calls | Refused with 403 and MSG-P4-002; nothing is returned and nothing is exported | MSG-P4-002 | AC7 |
| X4 | A pack, an export, an event or a log would carry an account key, a subject id or a personal identifier | The schema check refuses the member and the fixture; no member is declared for it and no free text is carried | None | AC5 |
| X5 | An export is asked for with a media type the contract does not declare | Refused before any row is written; the declared media types are named | None | AC3 |
| X6 | The record is submitted twice for the same pack and business date | The contract states one record per pack and business date, and a repeat writes nothing | None | AC4 |
| X7 | A field-level detail of a consumed operation is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC6, AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the P7 library contract, the P1 contract, TSD T-A.1 and T-A.2 and the Ownership Map as published |
| Negotiable | The member names, the export order and the record members are settled with their owners; this contract fixes them once and marks every open element |
| Valuable | Unblocks the app story of this key, the gateway-bff route and the tests against one pack shape and one record payload |
| Estimable | Two read responses, one export rule, one record member set, one PII rubric, one client rule and three fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the schema file, the example, the fake, the document — and never against a business outcome |
| Traceable | FEAT-AGT-16 and the legacy key are traced in section 18, and every DP of the metadata table appears in section 13 |

### 7. Acceptance criteria

```gherkin
Feature: Committee-review read contract of rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the decision-record library contract of RWB-PLT-E1027-CON and the gateway-bff route contract of RWB-PLT-N001-CON are in force
    Given agent "SCREENING" reviews its segment "SCREENING:MORTGAGE:BKK" for business date 2026-12-15 under policy version "P1"

  Scenario: AC1 The runs read answers one fixed resource (new, D-RCV-60)
    Given the contract section of this story
    When GET /api/recovery/agent/v1/admin/agent-runs is called with agent, from and to
    Then the answer is AgentRunsPack, whose members are the runs, the acceptance count, the override count, the fallback count and share, and the failure counts
    Then every member is named after the TSD column that carries it, and every member TSD T-A.2 leaves open is declared as an additive extension of API-P10-001
    Then the run members are those of agent_run over LOV-AGENT-RUN, the acceptance and override members those of agent_feedback over LOV-FEEDBACK, and the failure counts those of agent_evaluation_run
    Then the rwb-agent WireMock answers the operation with this document's shape and a drift between the fake and the document fails the contract test

  Scenario: AC2 The metrics read answers the committee pack (new, D-RCV-60)
    Given the contract section of this story
    When GET /api/recovery/agent/v1/admin/agent-metrics is called with agent, segment, version, from and to
    Then the answer is AgentMetricsPack, one measure set per agent, version, segment and day, with the incidents of the window
    Then an incident carries the alert type over LOV-AGENT-ALERT, the segment, the business date, the measured value, the threshold value, the role and whether it was notified
    Then a measure whose source answer failed or is older than the business date is declared as not available with a reason, and no member of the shape defaults a value
    Then the resource is a backward-compatible extension of API-P10-009 and no member is removed from the two type names TSD T-A.2 publishes

  Scenario: AC3 The export rule is fixed (new, D-RCV-60)
    Given the pack of AC1 and AC2
    When a pack is exported as JSON and again as text/csv
    Then both exports carry the same rows and the same member order as the read
    Then the CSV header is formed from the member names and the CSV holds no member the read does not hold
    Then the declared media types are application/json and text/csv, and any other media type is refused before a row is written
    Then the newline convention and the file name are agreed with the platform edge owner and are not asserted by this contract

  Scenario: AC4 The committee outcome has one fixed record payload (new, D-RCV-60)
    Given the decision-record library contract and the shared topic rwb.decision-record.v1
    When a committee outcome is submitted for a pack
    Then the record is written through the library and carries the pack reference, the business date, the policy version in force, the agent, prompt and model versions reviewed, the segment set, the outcome code, the owner role and the review date
    Then the record is relayed as rwb.decision-record.DecisionRecorded.v1 on rwb.decision-record.v1 in the CloudEvents envelope with the record reference as its key
    Then the member set is an additive member set of the P7 record shape, which this contract does not redefine
    Then one record exists per pack and business date, and a repeat submission writes no second record and sends no second notification

  Scenario: AC5 No personal data in a pack, an event, a log or an export (new, D-RCV-60)
    Given the rubric of this contract on personal data
    When the pack schema, the export, the record payload and the log fields are checked
    Then no member, column, payload field or log field carries an account key, a subject id, a customer name, a personal identifier or free text of an override reason
    Then the pack and the event carry identifiers and business facts only, and the log carries agent codes, segments, counts, rates, costs and the business date
    Then a fixture that carries an account key is refused by the schema check and fails the contract test

  Scenario: AC6 The score-fact read is consumed under one rule (new, D-RCV-60)
    Given the rwb-source-data contract for the ACE score facts
    When the score-fact read is described
    Then it is one hop to rwb-source-data with a 2 s client budget and a breaker, and it names the model code and model version it asks for
    Then no `v_ace_*` view is granted to the rwb-agent login, and no score row is written into rwb_agent
    Then a failed answer, or facts older than the business date, produce the not-available mark of AC2 and never a default
    Then the rwb-source-data WireMock answers the operation with the facts, an error, and stale facts, and a drift between the fake and the document fails the contract test

  Scenario: AC7 The errors and rights are those of TSD T-A.2 (new, D-RCV-60)
    Given TSD P10 v2 T-A.1 and T-A.2
    When the two operations are reviewed
    Then the runs read answers 401, 403 and 503 under Platform administration R, and the metrics read answers 401, 403, 422 and 503 under Rules and parameters R
    Then the 422 condition of the metrics read is an unreadable agent, segment, version or date parameter, and it is refused before a row is read
    Then a refused caller answers 403 with MSG-P4-002 and a refused export answers the code of the read it exports
    Then the Case record R right that T-A.2 gives the case agent-output operations is declared as not part of this slice

  Scenario: AC8 The fakes match the document (new, D-RCV-60)
    Given the three fakes of this contract
    When the contract tests run
    Then the rwb-source-data WireMock answers the score-fact read with the facts, the error and the stale answer of AC6
    Then the rwb-decision decision-record stub answers the record write with a committed record and its reference, and with a forced write failure
    Then the gateway-bff composite route stub answers the two reads merged, one call failing with the other section served, and a refused role with MSG-P4-002
    Then every fixture is synthetic and no production payload, score row or record is copied into a fake

  Scenario: AC9 The nine contract tables are complete and name only this service's elements (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.1 names only the two rwb-agent reads, 12.4 and 12.6 are None, and 12.7 names only rwb_agent tables and the library tables
    Then no element of the configuration contract of RWB-P10-E3030-CON and no element of the runtime contract of RWB-P10-E1058-CON is restated
    Then the record shape and the central ledger remain P7's, and the score facts remain P1's
```

Every criterion here is new and belongs to this contract slice: the legacy criteria of RWB-E8-005 stay with RWB-P10-E8005-APP and are not copied into this document.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One read shape for the committee pack: AgentRunsPack and AgentMetricsPack, each member named after the TSD column that carries it | TSD P10 v2 T-A.1, T-A.2 and T3.1; ASM-1043 |
| BR2 | The member lists are an additive, backward-compatible extension of API-P10-001 and API-P10-009; no published type, path, query or right is removed | TSD P10 v2 T-A.2; Architecture v5 slide 42 note (BACKWARD compatibility) |
| BR3 | The pack is built from `agent_run`, `agent_feedback`, `agent_alert`, `agent_evaluation_run` and `agent_policy`; no other service's table is read | DP-01; Arch v5 slide 41; Ownership Map v1 |
| BR4 | The score facts are read through rwb-source-data's contract, one hop, 2 s, and never through a `v_ace_*` view of this service's schema; a failed or stale answer is marked not available | DP-05; DP-01; ADR-010; Arch v5 slide 45 |
| BR5 | A pack exports as the same rows in the same member order, as JSON by default and as text/csv on request | ASM-1044; TSD P10 v2 T-A.2 (the JSON or CSV precedent) |
| BR6 | The committee outcome is recorded through the P7 library, in one transaction with its outbox row, and carried on `rwb.decision-record.v1` in the CloudEvents envelope | DP-03; ADR-022; Arch v5 slide 42 row 08 |
| BR7 | One record per pack and business date; a repeat submission writes nothing | R-UNI-40; ASM-1040 |
| BR8 | No personal data in a pack, an export, an event or a log: identifiers and business facts only | Template and Rules §R7.2 s17; Arch v5 slide 42 note; DP-03 |
| BR9 | The errors and rights of the two reads are those of TSD T-A.2 and are declared once, with the 422 condition stated by this contract | TSD P10 v2 T-A.1 and T-A.2; ASM-1046 |
| BR10 | No business value in the contract: the caps, the thresholds, the review date and the list values stay rows and reference data, and no literal is declared as an element | BR-P10-016; Template and Rules §R7.2 s17 |
| BR11 | This contract declares no element of the configuration operations and none of the run, guardrail, evaluation or feedback operations; those belong to their own contracts | RWB-P10-E3030-CON; RWB-P10-E1058-CON |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two responses, the export rule, the record members, the PII rubric and the client rule are described | In review |
| In review | Consumer sign-off | The app story of this key, the platform edge and the tests accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, an export column or a record member is added without removing one | Baselined |
| Baselined | Breaking change | An element of the two responses, of the export or of the record members is removed, renamed or retyped | In review, with the owner of that element |
| Baselined | Drift in a fake | A contract test fails | In review |

These are the states of this contract document and not a case state machine. The contract declares no status, state or transition of a pack, a run, an alert or a case, and it writes none.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the document, the schemas, the examples and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to the two responses, to the export rule or to the record members |
| P7 decision-record owner | Owns the record shape, the library and the central ledger, and signs off the committee-outcome members |
| P1 rwb-source-data contract owner | Owns the score-facts operation and its product path, and signs off the client rule of this contract |
| Platform edge owner (RWB-PLT-N001-CON) | Owns the composite route that reads the two responses for SCR-46 |
| Model risk function with the Center of Excellence analyst | Confirms the members a committee pack must carry and the members it must not carry |
| Data steward and PDPA officer | Confirms the personal-data rubric of AC5 |
| The rwb-agent app story of this key | Reviews and accepts the parts it implements |

The deployment identity that reads the rows and calls the two contracts is Not specified in the source documents (GAP-0643; ASM-1043); the document names it "the rwb-agent workload identity (DP-02)" and leaves the name to the infrastructure story.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| AgentRunsPack | pack reference, agent, version, segment, business date and window; the run count by status over LOV-AGENT-RUN; the acceptance count and the override count over LOV-FEEDBACK; the fallback count and its share; the confidence, latency and cost values carried by agent_run; the failure counts of agent_evaluation_run |
| AgentMetricsPack | pack reference, agent, version, segment, day; one measure set per agent, version, segment and day; the incidents of the window with alert type over LOV-AGENT-ALERT, segment, business date, measured value, threshold value, sent-to role and notified flag; the score column with its not-available mark and reason |
| Policy facts carried | policy version in force, model code, model version, autonomy mode, daily cost cap, alert role, review date, read from the agent_policy version in force (DF-AGT-001 to DF-AGT-025) |
| Export | the same rows and member order as the read; CSV header from the member names; media types application/json and text/csv |
| Record payload of a committee outcome | pack reference, business date, policy version, agent, prompt and model versions reviewed, segment set, outcome code, owner role, review date |
| Log fields | agent codes, segments, counts, rates, costs and business date; identifiers only, no personal data |
| Score facts | score_key, account_key, model_code, model_version, score_value, estimate_value and the four remaining fields of DF-ACE-270 to DF-ACE-279, read through the P1 contract and never declared as a pack member |

The field-level names of the response members beyond the TSD columns, and the types and lengths of each, are Not specified in the source documents (GAP-0643; ASM-1043): this document fixes the member names after the TSD columns, marks them as additive, and leaves the types to the review with the owners of the two operations. The record member names are likewise an additive set agreed with the P7 owner (ASM-1045). The export newline convention and file name are Not specified in the source documents (GAP-0643; ASM-1044) and are settled with the platform edge owner.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Access as declared | Response | Element source |
|---|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-runs` | Platform administration R | AgentRunsPack: runs, acceptance and override counts, fallbacks, failure counts | TSD P10 v2 T3.1 agent_run, agent_feedback, agent_evaluation_run; T-A.2 API-P10-001 |
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | Rules and parameters R | AgentMetricsPack: one measure set per agent, version, segment and day, with the incidents and the score column | TSD P10 v2 T3.1 agent_run, agent_alert; T3.2 LOV-AGENT-RUN, LOV-AGENT-ALERT, LOV-FEEDBACK; T-A.2 API-P10-009 |

The two operations are rwb-agent's under the Ownership Map, their base is `/api/recovery/agent/v1` (DP-13) and both are called only by the gateway-bff route for SCR-46 (DP-19). This contract fixes their member lists and their export answers; it adds no third operation and declares no path of another service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Contract element |
|---|---|---|---|
| GET | Not specified in the source documents (GAP-0643; ASM-1043) | P1 rwb-source-data | The score facts of the model code and model version in force; one hop, 2 s client budget, a breaker per downstream and a not-available answer with a reason |

DP-05 is resolved to the contract and not to a view of this service's schema: the score facts are one hop to rwb-source-data, no `v_ace_*` view is granted to the rwb-agent login, and no `v_ace_*` view of another service is opened (DP-05; DP-01; GAP-0643). The record write is a library call and not a REST operation (DP-03).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the ledger; each producer writes its own record through the library | the record reference | the committee-outcome members of section 11 and no personal data |

The type, the envelope and the schema are P7's and this contract does not redefine them: it declares the members a committee review contributes to the record before the library relays it (DP-03). One REST base, one topic and one schema per service: this contract's base is `/api/recovery/agent/v1`, its schema is `rwb_agent`, its Temporal task queue is `rwb-agent`, and its own event topic is `rwb.agent.events.v1` with events named `rwb.agent.<Event>.v1`. None of those events is declared here: the one event of the topic is `rwb.agent.AgentRunCompleted.v1` (EV-28), which belongs to the run path of RWB-P10-E1058-CON and is not restated by this contract.

#### 12.4 Events consumed

None. The two reads are answered from the service's own rows; the story has no inbox handler and consumes no topic.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| RecordAndApply | Activity (workflow kit) | `rwb-agent` | Input: the committee-outcome members and the pack reference. Output: the record reference. One transaction with the outbox row; a forced failure raises the failure and writes nothing |

The pack itself is assembled on the request path of the two reads, so this contract declares no workflow and no activity of its own beyond the kit's `RecordAndApply` input and output.

#### 12.6 Schedules

None. The committee cadence is not a job of this service and Arch v5 slide 44 carries no committee job; no Schedule is declared, created or changed by this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_run | P10 (rwb_agent) | The performance, fallback, latency and cost members; read only |
| agent_feedback | P10 (rwb_agent) | The acceptance and override members over LOV-FEEDBACK; read only |
| agent_alert | P10 (rwb_agent) | The incident members over LOV-AGENT-ALERT; read only |
| agent_evaluation_run | P10 (rwb_agent) | The failure counts member; read only |
| agent_policy | P10 (rwb_agent) | The policy version, model code and version, cap, alert role and review date; read only |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | The outbox envelope of the record and the idempotency of a repeat submission (DP-09) |

No other table is named in the contract. `decision_log_entry` is P7's and is written only through the library (DP-01, DP-03); `v_ace_score` is a P1 data product and is never joined.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock | The score facts of the model code and version in force for the business date; an error answer; facts older than the business date; a model version that is not in force | App story, contract tests |
| rwb-decision decision-record stub | A committed record with its reference; a forced write failure; the outbox row and its relay to `rwb.decision-record.v1`; a repeat submission | App story, contract tests |
| gateway-bff composite route stub | The two reads merged into one answer; one call failing with the other section served; a refused role answering 403 with MSG-P4-002 | App story, edge, contract tests |

Every fixture is synthetic (ASM-1047). A fixture that carries an account key, a subject id or a free-text personal reason is refused by the schema check of AC5.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The two rwb-agent reads on `/api/recovery/agent/v1`; the rwb-source-data score-fact read, one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` through the outbox, in the CloudEvents envelope |
| Temporal | 0 workflows, 1 activity contract | The kit's `RecordAndApply` on the queue `rwb-agent` |
| File | The CSV and JSON export | The export of a pack as the answer of its read; no file is read by the contract |

### 13. Solution plan

**Deliverables.** `contract/agent-runs-pack.yaml` (the runs read and its response members, with the additive extension marked), `contract/agent-metrics-pack.yaml` (the metrics read as the committee pack), `contract/pack-export.md` (the CSV and JSON rule), `contract/committee-outcome-record.md` (the record members on the P7 library and `rwb.decision-record.v1`), `contract/pii-rubric.md` (the rule of AC5) and the three WireMock mappings.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 resolves to the rwb-source-data contract and to no `v_ace_*` view of this service's schema (DP-01, DP-05). The DP table names a platform contract for DP-03 and DP-19, and this story consumes both as published baselines: a CON story carries no build dependency (Template and Rules §R5.7 rule 1), which is why the three dependency rows of the metadata table read None.

**Build steps**

1. Write the runs response: the members, their TSD source columns and the additive mark; add a schema lint to the pipeline.
2. Write the metrics response as the committee pack, with the incident members and the not-available mark.
3. Write the export rule: the media types, the member order, the header row and the refusal of an undeclared type.
4. Write the committee-outcome record members with the P7 owner and the topic contract.
5. Write the PII rubric and wire it into the schema check of both responses and of the export.
6. Document the score-fact client rule, its 2 s budget, its breaker and its not-available answer.
7. Document the errors and rights of the two reads from T-A.2, with the 422 condition.
8. Build the three fakes and their fixtures.
9. Add the nine contract tests, including the drift test between each fake and this document.
10. Tag the baseline and collect the sign-off of the app story, the platform edge and the tests.

**Done when.** The five contract files validate in the pipeline, the nine contract tests pass, the three fakes answer every declared element, and the app story, the platform edge and the tests of this key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required member of a call, a pack or an outcome is empty | Enter {field}. |
| MSG-P4-002 | A role without the right of the read or of the export opens it | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written on a committee outcome | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three texts are the legacy texts of RWB-E8-005 and keep their wording character for character. No message is added by this contract, and MSG-P10-004, whose wording is not in the extracts, is not restated.

### 15. Screens and states

None in this story. The contract serves the two reads that the gateway-bff composite route composes for SCR-46 Agent monitor, states Shadow; live; paused, and that route and that screen belong to the monitor story and to RWB-PLT-N001-CON. The three states change no row of the two responses (AC11 of RWB-P10-E8005-APP), and the contract fixes no screen field, order or masking rule.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E8005-CON-01 | AC1 | Contract | The runs response schema against the TSD column names; a removed member, a renamed member and a retyped member each fail the drift test |
| TC-P10-E8005-CON-02 | AC2 | Contract | The metrics response with one measure set per agent, version, segment and day; an incident of each LOV-AGENT-ALERT type; a not-available measure with a reason |
| TC-P10-E8005-CON-03 | AC3 | Contract | The same pack exported as JSON and as text/csv; the header row; an undeclared media type refused before a row is written |
| TC-P10-E8005-CON-04 | AC4 | Component | A committee outcome written through the stub: the members, the envelope and the key; a forced failure; a repeat submission for the same pack and date |
| TC-P10-E8005-CON-05 | AC5 | Component | A fixture with an account key, a subject id and a free-text reason; the schema check refuses each, and the log fields are scanned |
| TC-P10-E8005-CON-06 | AC6 | Contract | The score-fact fake with the facts, an error and stale facts; the 2 s budget and the breaker declared; the not-available mark |
| TC-P10-E8005-CON-07 | AC7 | Contract | The two operations against T-A.2: 401, 403, 503 and the 422 condition; Platform administration R and Rules and parameters R; the refusal with MSG-P4-002 |
| TC-P10-E8005-CON-08 | AC8 | Contract | The three fakes against the document, including the synthetic-fixture check |
| TC-P10-E8005-CON-09 | AC9 | Component | The nine sub-tables present and attributed; 12.4 and 12.6 None; no element of the configuration contract and none of the runtime contract restated |

The levels are Contract for the schema, export, error and fake criteria and Component for the record and completeness criteria. No `-ITG` copy is held here.

### 17. Guardrails

- No business value in the contract: caps, thresholds, the review date and the list values stay rows and reference data, and no literal is declared as an element.
- No personal data in an event, an export, a log field, an example or a fake: identifiers and business facts only.
- The contract names only rwb-agent operations as provided and only the P1 score-fact read as consumed; it restates no operation of another service (DP-01, DP-13).
- One REST base and one topic per service: a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1` for an owned event, fails the review.
- Every change to the two responses is additive; a breaking change is a new contract version and a new review (§R8.2).
- The record shape, the ledger and the record schema stay P7's; this contract adds members and redefines nothing.
- Every example and fixture is synthetic; no production payload, score row or record is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| None (the legacy story carries no requirement ID) | Agent performance, overrides and incidents reach the strategy and model committee | The two pack responses, their members and the export rule | TC-P10-E8005-CON-01, TC-P10-E8005-CON-02, TC-P10-E8005-CON-03 |
| R-UNI-39 | The decision record is written before the change and a failed write changes nothing | The committee-outcome member set, the library write and the forced failure | TC-P10-E8005-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two reads and the consumed score-fact operation with their budgets | TC-P10-E8005-CON-06, TC-P10-E8005-CON-07 |
| ADR-022 | Local decision record plus central ledger | The record members and the relay on `rwb.decision-record.v1` | TC-P10-E8005-CON-04 |
| D-RCV-60 DP-05 | The ACE score facts are read through the owner's contract | The client rule and the not-available mark | TC-P10-E8005-CON-06 |
| D-RCV-60 DP-19 | The screen composes the pack through the gateway-bff route | The route stub and the refusal path | TC-P10-E8005-CON-08 |

The legacy story RWB-E8-005 carries no requirement ID: it names its feature (FEAT-AGT-16) and no BRD in the extracts carries that feature, so no BRD section and no requirement is cited for it and the absence is recorded as GAP-0643.

### 19. Out of scope

- The implementation of the two reads, the fact readers, the exporter and the record writer (RWB-P10-E8005-APP).
- The configuration operations, their load, their approval and their rollback (RWB-P10-E3030-CON and RWB-P10-E3030-APP), which this contract does not restate.
- The agent runtime contract: the run, the guardrail checker, the evaluation harness and the feedback operation (RWB-P10-E1058-CON), which this contract does not restate.
- The drift check and the champion and challenger test (RWB-P10-E3031-APP, RWB-P10-E8003-APP).
- The record shape, the hash link, the central ledger and the ledger read (P7 rwb-decision).
- The score facts, their data product and its freshness rule (P1 rwb-source-data).
- The composite route of SCR-46, its merge rules and its breaker values (RWB-PLT-N001-CON and RWB-P10-E1063-APP).
- The roles, the rights, the scope and the masking rules (P4 rwb-access).
- The deployment of this capability: chart values, queue and topic provisioning, dashboards and the runbook.
