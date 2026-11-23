# RWB-P10-AD020-CON Autonomy level per decision step

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-AD020-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-020 |
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

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-020 for rwb-agent. The per-step autonomy slice of the rwb-agent contract is written down once: how a decision step is named in the agent configuration, how the level in force for a step is resolved by a run, the response shape of the agent configuration read carrying the step, the level, the version label and the approval reference as a backward-compatible extension (DP-13), the case agent-output read that shows an answer as a recommendation at L1, the decision-record members that carry the step, the level and the version through the local library (DP-03), and the three fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-agent**, I want **the per-step autonomy slice of this service's contract fixed as a contract — the name of a decision step in the agent configuration, the rule that resolves the level in force for a step, the four elements that the agent configuration and agent output reads carry, the decision-record members that carry the step, the level and the version, and the fakes for rwb-decision, rwb-access and the rwb-valuation route output**, so that **the app, the contract tests and the stories that raise, lower and review a level build on Day 1 against one agreed, testable shape, and no team decides by itself what "the level of a step" means in a payload**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s budget is the decoupling rule (DP-11, ADR-020), and a decision record written locally then sealed centrally is the record rule (DP-03, ADR-022). Both only work if the seam is written once. The seam here is the smallest one in the agent runtime and the one with the most readers: the level of a step is read by the run that applies it, by the admin read that shows it, by the monitor that displays it, by the change story that loads a new version and by the committee story that reviews it. If each of them names the step, the level, the version and the approval reference in its own way, the four values cannot be reconciled and the sentence the legacy story states — an agent never acts beyond what the committee approved — becomes unprovable.

The legacy story RWB-AD-020 gave the behaviour and two criteria: a step at L1 shows its answer as a recommendation and a person decides, and a committee approval for L2 shows its reference on the version that takes effect (legacy RWB-AD-020 AC1 and AC2). Its data was one row of `decision_log_entry`, its endpoint one admin read, its screen SCR-46. In the target the record belongs to rwb-decision and is written through the library, the admin read is answered on the service base, and the screen is composed by gateway-bff. What is left for a contract is the shape of the four values across those moves.

The contract also states what this service does not own: the approval, its reference and the delegation ladder are rwb-decision's; the rights and the roles are rwb-access's; the route decision D6 and its route agent output are rwb-valuation's; the lists LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-DECISION are reference data of rwb-case under the §R3 default ruling. A contract that restated any of them as its own would be a second source of truth for a value it cannot change.

This story owns no legacy criterion: both legacy criteria belong to RWB-P10-AD020-APP, and every criterion here is new and tests the contract artefacts of the title only. It carries no build dependency and is Day 1 by rule (Template and Rules §R5.7).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the REST base and the topic follow the platform rule and not a local choice.
- The CloudEvents 1.0 envelope and the platform error envelope are the platform baseline; this document narrows them where it must and says so.
- The local decision-record library contract is available (RWB-PLT-E1027-CON, DP-03): the record shape, the hash chain and the shared topic `rwb.decision-record.v1` are its elements, and this story reuses them rather than redefining them.
- The gateway-bff composite route contract is available (RWB-PLT-N001-CON, DP-19): one hop, a 2 s budget and a breaker per downstream are its elements, and the route for SCR-46 is declared there and consumed here.
- The rwb-decision approval read is published by rwb-decision: `GET /api/recovery/decision/v1/approvals/{approvalId}` returns the approval, and its reference is what a version shows. The `approval` table and the delegation ladder L1 to L6 belong to rwb-decision and this document consumes them.
- The rwb-access authorise operation is published by rwb-access: `POST /api/recovery/access/v1/authorise` answers a capability area and a right for a role. This document consumes it and defines none of it.
- The rwb-valuation route decision D6 and its route agent output exist as published by the rwb-valuation stories (Arch v5 slide 41). The operation that returns the route agent output is Not specified in the source documents (GAP-0639; ASM-1021).
- The values the contract names are the list values of the documents: LOV-AUTONOMY (OFF, SHADOW, L1) and LOV-CONFIG-STATUS (LOADED, APPROVED, RETIRED) of TSD P10 v2 T3.2, and LOV-DECISION (D1 to D9 with sub-decisions, X1 to X7) of the Logical Data Model v8. The legacy criteria name L1 and L2.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the shape of a policy version resource for this slice: the step, the autonomy mode, the version label and the approval reference, beside the fields the published configuration read already answers (API-P10-002).
2. Fix the resolution rule of the level in force for a step and a date, including the two-versions-in-force case and the no-version case.
3. Publish the response shape of the agent configuration read with the four elements, and the rule that no published element is removed, renamed or retyped.
4. Publish the response shape of the case agent-output read that shows an answer as a recommendation at L1, with the element that marks it as a recommendation and the reference of the version it ran under.
5. Publish the decision-record members that carry the step, the level and the version through the library, and the rule that `approval_level` is not reused for the autonomy mode.
6. Publish the three fakes and their stubs.
7. Add the contract tests: the version resource shape, the resolution rule, the two read shapes, the record members, the fakes and their drift against this document.
8. Tag the baseline and hand it to RWB-P10-AD020-APP and to the stories that load, approve, raise, lower and review a level.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A policy version resource carries no step, no autonomy mode, or a mode outside LOV-AUTONOMY | The load is refused with the field named, so such a version can never be in force | MSG-GEN-001 | AC1 |
| X2 | Two versions of the same step are in force on the same date | The resolution returns no level and the configuration exception names both version labels; no level is chosen by order, by label or by load date | None | AC2 |
| X3 | A read is asked for a version that does not exist, or for a step with no version in force | The configuration read answers the versions it holds; the run resolves OFF and the answer says so, and no level is defaulted | None | AC2, AC3 |
| X4 | A fake drifts from this document, or a caller sends an element this document does not declare | The contract test fails and the merge is blocked | None | AC6 |
| X5 | An answer is asked to assert an applied outcome at L1 | The agent-output shape has no element for an applied outcome; the answer is marked as a recommendation and nothing else | None | AC4 |
| X6 | An autonomy mode is sent on the decision record's `approval_level` | The record is refused by the record schema validation of the library, and the mode travels on the member this document fixes | MSG-P7-003 | AC5 |
| X7 | A field-level detail of a consumed operation is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the decision-record library contract, the gateway-bff route contract and the published operations of rwb-decision, rwb-access and rwb-valuation |
| Negotiable | The element names of the four values, the member keys of the record and the stubbed route-output operation are settled with their owners; the resolution rule and the recommendation marker are fixed by this realignment |
| Valuable | Unblocks the app story of this key and the four stories that load, approve, raise and review a level, and makes "the level of a step" one shape in every payload |
| Estimable | One version shape, one resolution rule, two read shapes, one record extension, three fakes, nine tables |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the schema file, the rule document, the fake, the document — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Per-step autonomy contract baseline for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the decision-record library contract of RWB-PLT-E1027-CON and the gateway-bff route contract of RWB-PLT-N001-CON are in force
    Given the legacy values of the two criteria are L1 and L2, and the screen states are Shadow, live and paused

  Scenario: AC1 The policy version shape carries the step, the level, the version and the approval reference (new, D-RCV-60)
    Given the contract file contract/agent-step-autonomy.yaml of this story
    When a policy version resource is validated against it
    Then it carries the step as a value of LOV-DECISION such as D6.3, the autonomy mode as a value of LOV-AUTONOMY, the policy version label and the approval reference
    Then the four elements are additive: no element of the published configuration read is removed, renamed or retyped
    Then a resource without a step, without a mode, or with a mode outside LOV-AUTONOMY is refused at the load with MSG-GEN-001 naming the field
    Then the element names are those this contract fixes and they stay assumptions until the wave 4 contract freeze

  Scenario: AC2 The level in force for a step is resolved by one rule (new, D-RCV-60)
    Given the resolution rule of contract/agent-step-resolution.md
    When a run asks for the level of step "D6.3" on 2026-12-15 for the agent that owns it
    Then the rule selects the version whose status is APPROVED and whose valid_from is on or before the date and whose valid_to is empty or on or after it
    Then at most one version is in force for a step and a date, and where two are in force the resolution returns no level, writes nothing and reports a configuration exception naming both version labels
    Then a version in LOADED or RETIRED status resolves no level, and a step with no version in force resolves OFF
    Then the resolution reads rwb_agent only, and the date it uses is the run date and not the date of the case or of the approval

  Scenario: AC3 The agent configuration read carries the step, the level, the version and the approval reference (new, D-RCV-60)
    Given the GET /api/recovery/agent/v1/admin/agent-configs response of this contract
    When the rwb-agent WireMock answers the path for the policy versions of one agent
    Then each version object carries the step, the autonomy mode, the policy version label and the approval reference beside the elements of the published operation
    Then a request without the query parameters answers the same shape as before this contract, and the media type stays application/json
    Then no element of the published response is removed, and a payload that carries one of the four elements without a step is refused by the validation of this contract

  Scenario: AC4 The case agent-output read shows an L1 answer as a recommendation (new, D-RCV-60)
    Given the GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs response of this contract
    When the run of step "D6.3" answered at mode "L1" for case "RW-2026-000401"
    Then each answer carries the mode, the step, the policy version, the run reference and an element that marks it as a recommendation
    Then the answer carries no element for an applied outcome, no case field and no case state
    When the run answered at mode "L2" under a version that carries the approval reference the rwb-decision mock answers
    Then the answer carries the mode "L2" and that approval reference, and it is marked as applied under that reference

  Scenario: AC5 The decision-record members carry the step, the level and the version (new, D-RCV-60)
    Given the record is written through the rwb-decision library (DP-03)
    When a record of the run of step "D6.3" at "L1" under version "P1" is written
    Then decision_code carries the step "D6.3" in the existing column of the record and no column is added to it
    Then the autonomy mode and the policy version travel as the named members autonomyMode and policyVersion of the record's recommendation, and the step is not repeated there as a free text value
    Then approval_level is not used for the autonomy mode, because LOV-APPROVAL-LEVEL is the delegation ladder L1 to L6 and its L1 is a different value
    Then the library computes prev_hash and entry_hash and the record is accepted with the two members present

  Scenario: AC6 The fakes answer every consumed path and payload (new, D-RCV-60)
    Given the three fakes of section 12.8
    When the contract tests run
    Then rwb-decision answers GET /api/recovery/decision/v1/approvals/{approvalId} with the approval reference of an L2 version, a 404 for an unknown reference, and a committed record and a forced failure from the library stub
    Then rwb-access answers POST /api/recovery/access/v1/authorise with Platform administration R for the six roles of the legacy permission list and a refusal for RW-REFADM
    Then the rwb-valuation fake answers the route output of the route decision D6, and the operation it stubs is named in this document
    Then a drift between any fake and this document fails the contract test

  Scenario: AC7 The nine contract tables are complete and the ownership is exact (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.3 and 12.6 are None, and 12.7 names only the rwb_agent tables and the library objects
    Then this contract declares no operation of another service as provided, and no topic outside rwb.agent.events.v1
    Then the contract adds no message beyond the three legacy messages, and no business value is written in it
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The autonomy level of a decision step is data of the policy version in force: the step, the mode, the version label and the approval reference travel together and are never split across payloads | Legacy RWB-AD-020 AC1 and AC2; FEAT-AGT-12; BR-P10-012; BR-P10-015 |
| BR2 | A version is in force only when its status is APPROVED and its `valid_from`..`valid_to` window contains the run date; at most one version is in force per step and date, and a second one is an exception and never a precedence order | TSD P10 v2 T3.1; ASM-1012 |
| BR3 | The step is a decision code of LOV-DECISION and is carried as data in the request, on the run and on the record; no step code is a constant of this service or of its contract | LDM v8 DF-DEC-003 and the LOV-DECISION row |
| BR4 | The autonomy mode is not carried on `approval_level`: that field is the delegation ladder L1 to L6 of LOV-APPROVAL-LEVEL, and its L1 is a different value from the autonomy L1 | LDM v8 DF-DEC-011 and DF-DEC-038; TSD P10 v2 T3.2; ASM-1015 |
| BR5 | At L1 an answer is a recommendation and a person decides; the contract fixes a marker for that and no element for an applied outcome, so a caller cannot mistake one for the other | Legacy RWB-AD-020 AC1; TSD P10 v2 T-A.2 API-P10-010; ASM-1020 |
| BR6 | The four elements are a backward-compatible extension: an element is added, never removed, renamed or retyped, and a caller that omits them keeps the behaviour it had | Template and Rules §R5.5 DP-13; TSD P10 v2 T-A.2 API-P10-001 and API-P10-002 |
| BR7 | The approval reference is rwb-decision's: the reference a version shows is the one `GET /api/recovery/decision/v1/approvals/{approvalId}` answers, and this service holds no approval of its own | Arch v5 slide 41; Ownership Map v1 (approval rows under P7); ASM-1011 |
| BR8 | The rights are rwb-access's: this contract consumes the authorise operation and declares no role, no right and no scope of its own | §R3 default ruling; Ownership Map v1 (POST /authorise under P4) |
| BR9 | The route decision D6 and its route agent output are rwb-valuation's; this contract consumes that output and restates none of it | Arch v5 slide 41 (rwb-valuation owns valuations, D6 route decision, route agent output); ASM-1021 |
| BR10 | No business value in the contract: levels, steps, dates, references, thresholds and role codes are data of the versions and the lists, and the contract names shapes only | Template and Rules §R7.2 s17; BR-P10-012; BR-P10-015 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The version shape, the resolution rule, the two read shapes and the record members are described | In review |
| In review | Consumer sign-off | The app story and the stories that load, approve, raise and review a level accept the document and the fakes | Baselined |
| Baselined | Additive change | An element, a member or a stub is added without removing one | Baselined |
| Baselined | Breaking change of a consumed operation | rwb-decision, rwb-access or rwb-valuation removes, renames or retypes an element this contract consumes | In review, with the owner of that operation |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | The list values change | LOV-AUTONOMY, LOV-CONFIG-STATUS or LOV-DECISION gains a value with its owner's approval | Baselined, with the list version named |

These are the states of the document and not of a case. The contract states no case state machine and no run state machine: the states of a policy version are read from `status`, `valid_from` and `valid_to` of `agent_policy`, and they belong to the story that applies them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the version shape, the resolution rule, the two read shapes, the record members, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to a consumed contract and any change to the resolution rule |
| The rwb-decision owner | Owns the approval read and the delegation ladder, and signs off the shapes taken from its document |
| The rwb-access owner | Owns the authorise operation and signs off its consumed shape |
| The rwb-valuation owner | Owns the route decision D6 and its route agent output and signs off the stubbed shape |
| The rwb-agent app story and the stories that load, approve, raise and review a level | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data element is declared in any of the shapes |

The workload identity that reads the tables and calls the three contracts is Not specified in the source documents (GAP-0639; ASM-1018); the document names it "the rwb-agent login (DP-02)" and leaves the name to the infrastructure story of the service.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Policy version resource | the step (a LOV-DECISION value), the autonomy mode (a LOV-AUTONOMY value), the policy version label, the approval reference, the model code and version, the output schema reference, `valid_from`, `valid_to` and the status over LOV-CONFIG-STATUS (DF-AGT-001 to DF-AGT-025) |
| Step scope of the version | the named member of the version that names the decision step it governs, with the key and the fallback of a dedicated column left open (DF-AGT-018; ASM-1010) |
| Agent run resource | the step it ran, the autonomy mode it ran under, the policy version, the model version, the run reference and `decision_log_id` (DF-AGT-036 to DF-AGT-060, especially DF-AGT-043 and DF-AGT-058) |
| Agent output resource | the mode, the step, the policy version, the run reference, the record reference, the recommendation marker and the answer payload as the run stored it (DF-AGT-049) |
| Decision record members | `decision_code` for the step, `recommendation.autonomyMode` and `recommendation.policyVersion` for the level and the version, `agent_version` and `model_version` for the versions, the hash chain from the library (DF-DEC-003, DF-DEC-007, DF-DEC-009, DF-DEC-011, DF-DEC-017, DF-DEC-018) |
| Approval reference | the identifier the approval read answers for the version, taken from the `approval` table of rwb-decision and held on the version (ASM-1011) |

The element names of the four values, the key of the step member and the member names of the record are Not specified in the source documents (GAP-0639; ASM-1017 and ASM-1015): this story fixes them, states them as assumptions, and leaves their types and lengths to the review with the owners of the consumed operations. No personal data element is declared: the shapes carry identifiers, codes, versions and references.

### 12. Contract

#### 12.1 REST operations provided

The three reads below are provided by rwb-agent and owned by the stories named; this contract fixes the extension that each of them carries for the per-step autonomy slice, and it adds no operation.

| Operation | Path | Right | Implementing story |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-runs` | Platform administration R | RWB-P10-E1063-APP |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | Rules and parameters R | RWB-P10-E3030-APP with the agent platform set-up of RWB-P10-E1058-APP |
| GET | `/api/recovery/agent/v1/cases/{caseId}/agent-outputs` | Case record R | The agent runtime stories of this epic |

The base is the service base `/api/recovery/agent/v1` and the legacy monolith base answers none of the three (DP-13). The four elements this contract adds — the step, the autonomy mode, the policy version label and the approval reference — are backward-compatible additions to the published answers of TSD P10 v2 T-A.2 API-P10-001, API-P10-002 and API-P10-010.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/approvals/{approvalId}` | P7 rwb-decision | The approval and its reference for the version that shows it; faked with a committee approval for L2 and a 404 |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The capability area and the right of the caller on the three reads; faked with Platform administration R for the six roles and a refusal |
| POST | Not specified in the source documents (GAP-0639; ASM-1021) | S1 rwb-valuation | The route agent output of the route decision D6 that a step at L1 answers on; faked |

Every operation is one hop with a 2 s client budget (DP-11, ADR-020). rwb-decision's approval is read when a version is loaded or approved and not on the run path, so the run path holds no synchronous read of another service for the level.

#### 12.3 Events published

None. This contract publishes no event type. The shared event `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library of DP-03 when a record is written, its schema is unchanged by this story, and the agent event `rwb.agent.AgentRunCompleted.v1` (EV-28) is the run story's.

#### 12.4 Events consumed

None. The per-step autonomy slice consumes no topic: the level is read from a row, and the approval reference is read when a version is loaded or approved. A consumer that would need the level subscribes to the run event and the events of the owning service, and that is the run story's contract.

#### 12.5 Workflows and activities

None declared. The resolution is an activity of the existing `AgentRunWorkflow` on the task queue `rwb-agent`, and its input and output are declared in the run contract; this story fixes only the rule by which the activity resolves a level, so that the run contract and the contract tests read the same rule.

#### 12.6 Schedules

None. The per-step autonomy slice has no Schedule: the level is read when a run starts, and no temporal schedule, timer or cadence is part of this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_policy | P10 (rwb_agent) | The version, its mode, its window, its status and its step member; no column added by this contract |
| agent_run | P10 (rwb_agent) | The mode the run ran under and the link to its record; no column added by this contract |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | The outbox envelope of the record write (DP-09) |

`decision_log_entry` and `approval` are rwb-decision tables and are never read or written directly (DP-01; DP-03). No other table is named in the contract.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision WireMock and record stub | `GET /approvals/{approvalId}` with the approval reference of an L2 version and a 404 for an unknown reference; a committed record, a forced failure and the outbox relay | App story, contract tests |
| rwb-access WireMock | `POST /authorise` granting Platform administration to RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM, and refusing RW-REFADM | Contract tests, the monitor route test |
| rwb-valuation WireMock | The route agent output of the route decision D6 for one case, and an empty answer for a case with no route decision | Contract tests |
| gateway-bff route stub | The composite answer of SCR-46 with the runs, their steps and their levels, and the refusal of a role without the right | The app story's route test |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The three admin and case reads of 12.1 extended; the approval read, the authorise call and the route output of 12.2; one hop, 2 s |
| Kafka | None published, none consumed | The record event is the library's and the run event is the run story's |
| Temporal | None declared | The resolution is an activity of the existing `AgentRunWorkflow` |
| File | None | No file is read or written by this slice |

### 13. Solution plan

**Deliverables.** `contract/agent-step-autonomy.yaml` (the policy version shape with the step, the mode, the label and the approval reference), `contract/agent-step-resolution.md` (the resolution rule of the level in force, the two-in-force case and the no-version case), `contract/agent-output-recommendation.yaml` (the agent output shape and its recommendation marker), `contract/decision-record-autonomy.md` (the record members and the rule that `approval_level` is not reused), and the three WireMock mapping sets. The file names are this story's choice and are Not specified in the source documents (GAP-0639; ASM-1019).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/agent/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Both H dependencies are platform contract stories, and this story still carries no build dependency because it consumes them as published and fakes them (Template and Rules §R5.7 rule 1). DP-05 resolves to the rwb-source-data contract for the case facts a step answers on and to no view of this service; the contract declares no `v_ace_*` element.

**Build steps**

1. Write the policy version shape: the step, the mode, the label and the approval reference, with the list values named and the additive rule stated; test for AC1.
2. Write the resolution rule with the window, the two-in-force case, the retired case and the OFF case; test for AC2.
3. Write the two read shapes and the rule that no published element is removed; tests for AC3 and AC4.
4. Write the record members and the `approval_level` rule with the owners of rwb-decision; test for AC5.
5. Build the three WireMock mapping sets and their fixtures; test for AC6.
6. Add the drift test between each fake and this document, and the completeness test of the nine sub-tables; tests for AC6 and AC7.
7. Tag the baseline and collect the sign-off of the app story and of the four stories that load, approve, raise and review a level.

**Done when.** The four contract files validate in the pipeline, the contract tests of section 16 pass, the three fakes answer every consumed path and payload, and RWB-P10-AD020-APP and the four stories of this key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of a policy version resource is empty, or an autonomy mode is outside its list | Enter {field}. |
| MSG-P4-002 | A role without the right in the capability area calls one of the three reads | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written, or a record is refused because the mode was sent on `approval_level` | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three texts are the legacy texts of RWB-AD-020 and keep their wording character for character; this contract adds no message. The `{field}` value is the element the validation names, and `{action}` is the read the caller attempted; neither carries a value of a record.

### 15. Screens and states

None in this story. SCR-46 Agent monitor, in its legacy states Shadow, live and paused, shows the runs of a step with the step, the level, the policy version and the approval reference; the screen and its read belong to RWB-P10-E1063-APP and are composed through the gateway-bff route (DP-19). This contract fixes the shape the screen reads and not the screen: no field order, no label and no masking rule is declared here, and the panel that shows the level per step is the monitor story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-AD020-CON-01 | AC1 | Contract | A version resource with the four elements; a resource without a step; a resource with a mode outside LOV-AUTONOMY; a published element removed |
| TC-P10-AD020-CON-02 | AC2 | Contract | "P1" in force to 2027-01-14 and "P2" from 2027-01-15; two versions in force on one date; a retired version; no version in force |
| TC-P10-AD020-CON-03 | AC3 | Contract | The `GET /admin/agent-configs` answers with and without the query parameters; one answer with a mode and no step |
| TC-P10-AD020-CON-04 | AC4 | Contract | The `GET /cases/{caseId}/agent-outputs` answer at L1 and at L2 with the approval reference of the mock |
| TC-P10-AD020-CON-05 | AC5 | Contract | A record of "D6.3" at "L1" under "P1"; a record that carries the mode on `approval_level` |
| TC-P10-AD020-CON-06 | AC6 | Component | The three fakes answering every consumed path; one drifted stub per fake |
| TC-P10-AD020-CON-07 | AC7 | Contract | The nine sub-tables of section 12; the ownership of each row; the absence of a provided operation of another service |

### 17. Guardrails

- No business value in the contract: levels, steps, dates, references, thresholds and role codes stay data of the versions and the lists.
- No personal data in an event, an activity input, an example or a fake: identifiers, codes, versions and references only.
- The contract names only rwb-agent operations as provided and only rwb_agent tables as owned; the approval, the rights and the route output are consumed and never restated as this service's (DP-01, DP-13).
- One REST base and one topic per service; a document that names another service's base as provided, or a topic outside `rwb.agent.events.v1`, fails the review (DP-13).
- The autonomy mode never travels on `approval_level`, and the delegation ladder is never restated in this contract.
- Every example and fixture is synthetic; no production record, approval or payload is copied into a schema or a fake.
- The envelope, the naming rule and the record library elements come from the platform library; this story narrows them but never redefines them.
- The contract adds no level, no ladder and no list value: a value it does not find in a source is carried as a gap and an assumption and never invented.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| None (the legacy story carries no requirement ID) | The level of a step is data and a step up shows the approval reference of the version that takes effect | The version shape, the approval reference element, the record members | TC-P10-AD020-CON-01, TC-P10-AD020-CON-05 |
| FEAT-AGT-12 | An autonomy level is changed for one agent and one decision as a versioned configuration row | The version shape and the resolution rule | TC-P10-AD020-CON-01, TC-P10-AD020-CON-02 |
| FEAT-AGT-15 | An autonomy level is raised or lowered with the approval each change needs | The approval reference element and its consumed read | TC-P10-AD020-CON-03, TC-P10-AD020-CON-06 |
| BR-P10-012 and BR-P10-015 | No value a business person may change is written in code | The list values named and never restated, and the resolution reading a row | TC-P10-AD020-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed operations with the 2 s client budget | TC-P10-AD020-CON-06 |
| ADR-022 | Local decision record plus central ledger | The record members and the library envelope | TC-P10-AD020-CON-05 |
| D-RCV-60 DP-19 | The screen composes its answer through the gateway-bff route | The composite route stub and the agent output shape | TC-P10-AD020-CON-04, TC-P10-AD020-CON-06 |

The legacy story RWB-AD-020 carries no requirement ID and names no feature, so no BRD section is cited; the features are FSD P10 v3 A2.12 and A2.15, the rules are BR-P10-012 and BR-P10-015, the decisions are D-RCV-60 and ADR-020, and the gap that records the absent requirement row is GAP-0639.

### 19. Out of scope

- The implementation of the resolver, the run writer, the recommendation presenter and the record adapter (RWB-P10-AD020-APP).
- The load, the approval and the rollback of a policy version (RWB-P10-E3030-APP and RWB-P10-E3030-CON), and the raise or lower of a level with approval (RWB-P10-E8004-APP and RWB-P10-E8004-CON).
- The agent run itself, its guardrails, its tool gateway and the 60-second rule fallback (RWB-P10-E1058-APP, RWB-P10-E1061-APP), and the monitor SCR-46 and its read (RWB-P10-E1063-APP).
- The committee review of agent risk (RWB-P10-E8005-APP), the central ledger and its sealing (P7 rwb-decision), the delegation ladder L1 to L6 and the approval row (P7).
- The rights, the roles, the scope and the masking rules (P4 rwb-access), and the lists LOV-AUTONOMY, LOV-CONFIG-STATUS and LOV-DECISION (P3 rwb-case under the §R3 default ruling).
- The route decision D6, its route agent output and the valuation behind it (S1 rwb-valuation).
- The case facts a step answers on and their data products (P1 rwb-source-data).
- The deployment of this capability: chart values, queue and topic provisioning, dashboards and the runbook.
