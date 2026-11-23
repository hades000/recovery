# RWB-P10-E8004-CON Raise or lower an autonomy level with approval

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E8004-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-004 for rwb-agent. The approval-gated version-change slice is fixed as a contract before any build: the load-then-approve two-step of the two admin operations with their rights, errors and Idempotency-Key rules from TSD P10 v2 T-A.2, the approval reference carried on the configuration version, the consumed rwb-decision approval read that carries the approval id and the approved level, the decision-record payload of the change (DP-03, `rwb.decision-record.v1`), the message set of the legacy story and the fakes for rwb-decision and rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of an approval-gated autonomy change fixed as a contract: the load-then-approve two-step of `POST /api/recovery/agent/v1/admin/agent-configs` and `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` with their rights, error codes and Idempotency-Key rules, the approval reference the configuration version carries, the rwb-decision approval read this service consumes, the decision-record payload of the change, the message set and the fakes for rwb-decision and rwb-access**, so that **the app, infrastructure and test stories of this legacy key build on Day 1 against one agreed, testable shape without waiting for rwb-decision, and no team invents its own reading of what "approved" means for a level**.

### 2. Business rationale

A level change in the target is two writes and one read in three services, and only the read is another service's: rwb-agent loads a version and sets its level, rwb-decision holds the approval that authorises the level, and the local decision-record library carries the change to the central ledger. Contract-first REST with one hop and a 2 s timeout is the decoupling rule (DP-11, ADR-020), central governance with local state is the decision of Arch v5 (slide 41: rwb-decision owns the approvals and the central ledger; rwb-agent owns the policy versions, prompts, runs, guardrails and evaluations), and the local record plus the shared topic is ADR-022. All three only hold if the seam is written down once.

The seam is small and load-bearing. A version must never be created approved, or the four-eyes rule becomes decoration. An approval must be read by id and by nothing else, or two services disagree about what was approved. The level of the approval and the level of the agent must not be confused: rwb-decision routes by delegation of authority with an `approval_level` of LOV-APPROVAL-LEVEL, L1 to L6 (TSD P7 v2 T3.2), while an autonomy level is a value of LOV-AUTONOMY, OFF, SHADOW and L1 (TSD P10 v2 T3.2). The two lists share three strings and mean different things, so the contract fixes which element carries the autonomy level and forbids reading the other as one.

If the shape is agreed and faked on Day 1, three teams move at once. The app story of RWB-P10-E8004-APP builds the version write, the approval client and the record against the fakes, with the approval-reference column and its migration; the infrastructure story of the service (RWB-P10-E1058-INF) provides the schema, the login and the certificate against the same document; the test stories of the wave read one message set and one error catalogue. Without it, the approval reference becomes a free-text field, the 409 of a second approval means one thing in one service and another in the next, and the record of a level change stops being evidence.

The contract also states what it does not cover. The shapes of the two operations are baselined by RWB-P10-E3030-CON and the plain level change of Epic 3 by RWB-P10-E3030-APP; the autonomy level per decision step and its resolution by RWB-P10-AD020-CON and RWB-P10-AD020-APP; the runtime, the run and the admin surface by RWB-P10-E1058-CON and RWB-P10-E1058-APP. This story adds only the approval-gated slice and never restates those baselines as its own.

### 3. Preconditions

- The service template of the platform and the naming library are available (RWB-PLT-E1047-CON), so the REST base, the topic and the event names follow the platform rule and not a local choice (DP-13, DP-14).
- The CloudEvents 1.0 envelope, the problem-response envelope and the Idempotency-Key rule are the platform baseline (DP-09, DP-03); this document narrows them where it must and says so.
- The configuration operations are baselined by RWB-P10-E3030-CON: the pair of operations, their media types, their request bodies and their error catalogue. This story consumes that baseline and adds only the approval-gated behaviour, the approval reference and the record.
- The local decision-record library is available (RWB-PLT-E1027-CON, DP-03): the record shape of chain_seq, inputsRef, ruleId, ruleVersion, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, prev_hash and entry_hash, the hash link and the outbox row.
- The rwb-decision approval read exists as published by rwb-decision: `GET /api/recovery/decision/v1/approvals/{approvalId}` (API-P7-008). This story consumes it and fakes it; it defines no part of it.
- The authorise contract of rwb-access exists as published (RWB-P4-E1037-CON), and the two operations declare the Rules and parameters right C and A that the gateway-bff route asserts before the call reaches rwb-agent (DP-19). The guard library of DP-08 is not a pattern of this key (ASM-1031).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the two-step of the change: what the load creates, what the approve does, and the one status transition between them, with the guarantee that no version is created APPROVED.
2. Fix the rights, the error codes and the Idempotency-Key rule of each operation from TSD P10 v2 T-A.2, and state what each 409 and each 404 means.
3. Fix the approval reference on the configuration version: its element name, its type, when it is written, that it is immutable afterwards, and how it is read back.
4. Publish the consumed rwb-decision approval read with its purpose, its rights, its errors and the 2 s client budget, and state which element carries the approved level.
5. Publish the decision-record payload of a level change: what each record element carries when no Drools package is evaluated, and what is forbidden.
6. Publish the message set of the change and the mapping from the error codes to the messages.
7. Publish the contract tables of section 12 and the three fakes.
8. Add the contract tests: the two-step, the error catalogue, the approval reference, the consumed read, the payload, the messages, and a drift test between each fake and this document.
9. Tag the baseline and hand it to RWB-P10-E8004-APP, to the infrastructure story of the service and to the test stories of wave 4.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A load arrives with a level that is not a value of LOV-AUTONOMY | Refused with 422 before any row is written; the field is named | MSG-GEN-001 | AC1, AC3 |
| X2 | An approve arrives for a version that is already APPROVED or is RETIRED | Refused with 409; the row, its approval reference and its record are unchanged | None | AC2 |
| X3 | An approve arrives for a version id that does not exist | Refused with 404 and no write | None | AC2 |
| X4 | The caller loaded the version and also approves it | Refused with 409 and the version stays LOADED (the four-eyes rule of FSD P10 v3 A2.1 AC-EXC-P10-001-03) | MSG-P7-002 | AC2 |
| X5 | The approval read answers 404, or the approval is not APPROVED, or its level differs from the version | Refused with 409 or 404, the version stays LOADED, no approval reference and no record | None | AC4 |
| X6 | The same POST is repeated under the same Idempotency-Key | The first answer is returned, nothing is written twice and the repeat is counted | None | AC2 |
| X7 | A caller without the Rules and parameters right goes through the route | Refused with 403 before the service is reached | MSG-P4-002 | AC2, AC6 |
| X8 | A fake drifts from this document, or the service names another service's path as its own | The contract test fails and the merge is blocked | None | AC7, AC8 |
| X9 | A field-level detail of a consumed element is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC4, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the configuration baseline of RWB-P10-E3030-CON, the decision-record library and the rwb-decision approval read as published |
| Negotiable | The field-level detail of the consumed approval answer is settled with its owner; the approval reference, the payload and the error meanings are fixed by this realignment |
| Valuable | Unblocks the app, infrastructure and test stories of this key and stops three services reading "approved" three ways |
| Estimable | One two-step, one error catalogue, one extension field, one consumed operation, one payload, one message set and three fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the OpenAPI document, the schema fragment, the fake, this document — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Approval-gated autonomy version-change contract for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the configuration operations of RWB-P10-E3030-CON are the baseline of the two admin paths
    Given the level values of LOV-AUTONOMY are OFF, SHADOW and L1

  Scenario: AC1 The load-then-approve two-step is fixed (new, D-RCV-60)
    Given the contract of this story
    When the two steps are reviewed
    Then POST /api/recovery/agent/v1/admin/agent-configs creates one policy or prompt version for one agent with the level and the valid-from date it is given, and its status is LOADED
    Then POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve moves a LOADED version to APPROVED and takes effect from its valid_from
    Then no version is created APPROVED, and no path sets APPROVED without the approve operation
    Then the version that was in force closes with valid_to the day before the new valid_from and status RETIRED, and needs no second approve operation
    Then a previous version stays readable with its own level after it closes

  Scenario: AC2 The rights, the error codes and the Idempotency-Key rule are fixed (new, D-RCV-60)
    Given the contract tables of section 12
    When the two operations are reviewed
    Then the load declares the Rules and parameters right C and the approve declares the Rules and parameters right A, each with the scope applied
    Then the load answers 401, 403, 409, 422 and 503, and the approve answers 401, 403, 404, 409 and 503
    Then both POSTs take an Idempotency-Key header, and a repeat under the same key returns the first answer and writes nothing
    Then 409 on the approve means the version is not LOADED, the caller loaded it, or the request conflicts; 404 means the version id is unknown

  Scenario: AC3 The approval reference on the version is fixed (new, D-RCV-60)
    Given the configuration version resource of the contract
    When the extension is reviewed
    Then the version carries one approval reference element, the approval id of rwb-decision, written by the approve operation only
    Then the element is empty on a LOADED version and immutable once the version is APPROVED
    Then GET /api/recovery/agent/v1/admin/agent-configs returns it with the version, its status and its dates
    Then the element is declared a backward-compatible extension, and no existing element of the resource changes name, type or length

  Scenario: AC4 The consumed approval read carries the approval and the approved level (new, D-RCV-60)
    Given the approval read GET /api/recovery/decision/v1/approvals/{approvalId} of rwb-decision
    When the contract is reviewed
    Then the read is documented with its purpose, its right, its errors and the 2 s client budget, and it is attributed to rwb-decision and never declared as provided by rwb-agent
    Then its answer carries the approval id, the approval status of LOV-APPROVAL-STATUS, the decision code and the approved autonomy level of the approval subject
    Then no approval_level of LOV-APPROVAL-LEVEL is used as an autonomy level, and the two lists are named as different lists
    Then a 404, a status other than APPROVED, and a level that differs from the version are each mapped to a refusal of the approve call

  Scenario: AC5 The decision-record payload of a level change is fixed (new, D-RCV-60)
    Given the record shape of the local decision-record library
    When the payload of a level change is reviewed
    Then the record carries the agent code, the previous policy version and level, the new policy version and level, the approval reference, the approver identity and the valid-from date
    Then ruleId and ruleVersion are empty, because no Drools package is evaluated for a level change, and the change is named by the decision code and the two policy versions
    Then the record is hash-linked to the previous record and commits in one rwb_agent transaction with the version row and the outbox row
    Then rwb.decision-record.DecisionRecorded.v1 is published on rwb.decision-record.v1 with the record reference and the change facts and no personal data

  Scenario: AC6 The message set of the change is fixed (new, D-RCV-60)
    Given the legacy message table of RWB-E8-004
    When the message set is reviewed
    Then MSG-GEN-001, MSG-P4-002 and MSG-P7-003 appear with their legacy wording unchanged
    Then each message is mapped to the code and the condition that raises it, and to no other
    Then MSG-P7-002 is named by id for the four-eyes refusal and is not restated, because its wording is not in the source extracts
    Then this contract adds no message

  Scenario: AC7 The three fakes match the document (new, D-RCV-60)
    Given the fakes of section 12.8
    When the contract tests run
    Then the rwb-decision approval fake answers APPROVED for the level of the version, REFUSED, RETURNED, a level that differs, an unknown id and a slow answer
    Then the decision-record fake answers a committed record and a forced 503
    Then the rwb-access fake grants and refuses the Rules and parameters right C and A for the named roles
    Then a drift between any fake and this document fails the contract test and blocks the merge

  Scenario: AC8 The boundary and the nine sub-tables are fixed (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.1 names the two admin operations on the rwb-agent base and no operation of another service
    Then 12.4 and 12.6 are None and 12.7 names only rwb_agent tables and the library objects
    Then the contract restates no element of the configuration baseline of RWB-P10-E3030-CON, of the per-step resolution of RWB-P10-AD020-CON or of the runtime of RWB-P10-E1058-CON
    Then no path of the contract sits outside /api/recovery/agent/v1 or /api/recovery/decision/v1, and no old monolith base appears
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A version is loaded and then approved, never created approved; APPROVED is reachable only through the approve operation | FEAT-AGT-15; FSD P10 v3 A2.15 and A2.1 AC-ALT-P10-001-01; TSD P10 v2 T3.2 LOV-CONFIG-STATUS |
| BR2 | The load carries the Rules and parameters right C and the approve the right A, and both take an Idempotency-Key header | TSD P10 v2 T-A.1 and T-A.2 API-P10-003 and API-P10-004 |
| BR3 | The approval is a fact of rwb-decision, read by approval id through its contract; rwb-agent stores only the reference | Arch v5 slide 41; legacy RWB-AD-020 AC2; ASM-1025 |
| BR4 | An autonomy level is a value of LOV-AUTONOMY, and the `approval_level` of LOV-APPROVAL-LEVEL is a different value that is never read as an autonomy level | TSD P10 v2 T3.2; TSD P7 v2 T3.2; ASM-1025 |
| BR5 | The record is written before the version takes effect, in one transaction with the row and the outbox row, and no change proceeds unrecorded | Principle 5; R-UNI-39; DP-03 |
| BR6 | One REST base per service: this contract declares `/api/recovery/agent/v1` as provided and `/api/recovery/decision/v1` as consumed, and never the reverse | DP-13; Arch v5 slide 41 |
| BR7 | No business value in the contract: levels, dates, approval ids and decision codes are data of the version row and of the approval | BR-P10-015; Template and Rules §R7.2 s17 |
| BR8 | The approval reference is a backward-compatible extension: it is added, no existing element changes, and a client that ignores it still reads the version | ASM-1026 |
| BR9 | No personal data in the answer, the payload, a fake or a log: identifiers and business facts only | Template and Rules §R7.2 s17 |
| BR10 | This contract restates no element of RWB-P10-E3030-CON, RWB-P10-AD020-CON or RWB-P10-E1058-CON; it adds the approval-gated slice only | The split plan of the service epic RWB-SVC-P10 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two-step, the error catalogue, the approval reference, the consumed read, the payload and the fakes are described | In review |
| In review | Consumer sign-off | RWB-P10-E8004-APP, the infrastructure story and the test stories accept the document and the fakes | Baselined |
| Baselined | Additive change | An element is added to the version resource, the record payload or the fake without removing one | Baselined |
| Baselined | Breaking change to a consumed element | rwb-decision removes, renames or retypes an element this contract consumes | In review, with the owner of that element |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A new level enters LOV-AUTONOMY | A level is added to the list, a value above L1 among them | In review, because the contract states the list the change may carry |

These are the states of the contract document, not of a version. The states of a configuration version are LOADED, APPROVED and RETIRED (TSD P10 v2 T3.1, DF-AGT-021) and are fixed by AC1.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the two-step, the error catalogue, the approval reference, the payload and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to the consumed element and any change to the two-step |
| The rwb-decision owner | Owns the approval read of API-P7-008 and signs off the elements taken from its document |
| The rwb-access owner | Owns the authorise contract and the Rules and parameters rights C and A the route asserts |
| The rwb-agent app, infrastructure and test stories | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the problem response, the Idempotency-Key rule and the decision-record shape this document reuses |
| Data steward | Confirms that no personal data element is declared in the answer, the payload or a fake |

The identity that calls the approval read and writes the record is Not specified in the source documents (GAP-0641; ASM-1029); the document names it "the rwb-agent login (DP-02)" and leaves the name to the infrastructure story of the service.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Configuration version resource | agent_code, kind, policy_version or prompt_version, the level of LOV-AUTONOMY, valid_from, valid_to, status of LOV-CONFIG-STATUS, loaded_by, approved_by and the approval reference (DF-AGT-001 to DF-AGT-035) |
| Approval reference | One element holding the approval id of rwb-decision; empty until approval and immutable afterwards; the backward-compatible extension of ASM-1026 |
| Consumed approval answer | approval id, approval status of LOV-APPROVAL-STATUS, decision code, the approved autonomy level of the approval subject, the approver identity; no personal data (DF-DEC-034 to DF-DEC-053, read through P7) |
| Decision-record payload | agent code, previous policy version and level, new policy version and level, approval reference, approver identity, valid-from date, decision code; ruleId and ruleVersion empty (DF-DEC-001 to DF-DEC-018, DF-DEC-028) |
| Event payload | record reference, agent code, both policy versions and levels, approval reference, valid-from date; identifiers and business facts only |
| Error catalogue | The two operations' codes with the condition each one names, and the message of each |

The field-level detail of the consumed approval answer — property names, types, lengths and required flags — is Not specified in the source documents beyond "Read one approval with its routing details for the decision screen" (GAP-0641; ASM-1032), and the name and type of the approval reference element are agreed here as an extension (GAP-0641; ASM-1026). No production approval, payload or approval id is copied into an example or a fake.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Method | Path | Right | Errors | Idempotency |
|---|---|---|---|---|---|
| API-P10-003 load a version | POST | `/api/recovery/agent/v1/admin/agent-configs` | Rules and parameters C, scope applied | 401, 403, 409, 422, 503 | Idempotency-Key header |
| API-P10-004 approve a version | POST | `/api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` | Rules and parameters A, scope applied | 401, 403, 404, 409, 503 | Idempotency-Key header |

The load takes the checked file, the kind, the agent and the valid-from date and answers the version resource; the approve takes no request body and answers the same resource with status APPROVED and the approval reference set (TSD P10 v2 T-A.2). The base, the request bodies and the media types are the baseline of RWB-P10-E3030-CON; what this contract adds to them is the two-step, the approval reference, the meaning of each 409 and 404 (ASM-1030), the decision record and the message mapping. The reads `GET /api/recovery/agent/v1/admin/agent-configs` (API-P10-002) and `GET /api/recovery/agent/v1/admin/agent-runs` (API-P10-001, the legacy read of this key on the rwb-agent base) are consumed here and are not re-declared.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/approvals/{approvalId}` | P7 rwb-decision | The approval of the change: its id, its status of LOV-APPROVAL-STATUS, its decision code and the approved autonomy level of its subject; faked with APPROVED, REFUSED, RETURNED, a differing level, a 404 and a slow answer |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Rules and parameters right C on the load and A on the approve, asserted by the gateway-bff route before the call reaches rwb-agent (DP-19); the guard library of DP-08 is not wired by this key, so the call is the route's and not this service's |

Both are one hop with a 2 s client budget (DP-11, ADR-020). The approval read is called by rwb-agent on every approve; the authorise call is the route's and is faked for the route tests only (ASM-1031).

#### 12.3 Events published

| Event | Topic | Owner of the type | Payload (IDs and facts only) | Published by |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger | record reference, agent code, both policy versions and levels, approval reference, valid-from date | The local decision-record library, in the transaction of the approve (DP-03) |

The contract fixes the payload of a level change and does not define the envelope, which is the platform library's. The element map of a change with no Drools package — the two policy versions and levels in `recommendation` and `inputsRef`, `ruleId` and `ruleVersion` empty, the approval reference with the approver — is agreed here (ASM-1033). No `rwb.agent.events.v1` event is published for a change: the P10 OUT line of Arch v5 slide 16 and the event catalogue row 28 name AgentRunCompleted only.

#### 12.4 Events consumed

None. The two operations are on a request path and the change reads no topic; the service has no inbox handler for this slice.

#### 12.5 Workflows and activities

None. The change is synchronous on the two request paths and starts no workflow and no activity on task queue `rwb-agent`. The approval is routed by the kit's ApprovalWorkflow on rwb-decision (Temporal and Drools design slides 12 and 13) and this contract reads its outcome through the approval read, not through Temporal.

#### 12.6 Schedules

None. No job in the Arch v5 job map belongs to a level change (slide 44), and this contract registers no Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_policy | P10 (rwb_agent) | The version resource of a policy: the level, the dates, the status, the loader, the approver and the approval reference; no other column changes |
| agent_prompt | P10 (rwb_agent) | The version resource of a prompt: the same two-step and statuses; named for the shape only, not changed by this slice |
| outbox_event, idempotency_key | PLT library, created in rwb_agent | The transaction outbox of the record and the Idempotency-Key envelope of the two POSTs (DP-03) |

No other table is named. `approval` and `decision_log_entry` are rwb-decision's and are reached only through the approval read and the record library (DP-01). The approval reference lives on the version and not in a table of its own (ASM-1026).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision WireMock — approvals | `GET /approvals/{approvalId}` with an APPROVED approval for the level of the version, an APPROVED approval for another level, a REFUSED, a RETURNED, a 404 and a slow answer | RWB-P10-E8004-APP, contract tests |
| Decision-record library stub | A committed record with its reference and its outbox row; a forced 503 on the write | RWB-P10-E8004-APP, contract tests |
| rwb-access WireMock | `POST /authorise` granting Rules and parameters C to RW-COE and A to RW-RISK, and refusing a role that holds Platform administration R only | The route tests of RWB-P10-E8004-APP and the test stories of wave 4 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The load and the approve on `/api/recovery/agent/v1`; the approval read on `/api/recovery/decision/v1` and the authorise call of the route; one hop, 2 s |
| Kafka | 1 published, none consumed | `rwb.decision-record.v1`, published by the library in the transaction of the approve |
| Temporal | None | No workflow and no activity; the ApprovalWorkflow is rwb-decision's |
| File | 1 file per load | The checked configuration file the load carries; no runtime file exchange by this slice |

### 13. Solution plan

**Deliverables.** `contract/agent-config-approval-two-step.yaml` (the two operations, the two-step and the error catalogue of section 12.1), `contract/agent-config-approval-ref.yaml` (the approval reference element and its read-back), `contract/decision-approval-consumed.yaml` (the consumed approval read of rwb-decision), `contract/autonomy-change-record.md` (the record payload of a level change), `contract/autonomy-change-messages.md` (the message set and its mapping) and the three WireMock mappings with their fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is applied as the schema rule: the version resource is `agent_policy` in `rwb_agent`, the approval is read through its owner and the record through the library. It adds no dependency, which is why the metadata rows are None on every side and the story is Day 1 by rule.

**Build steps**

1. Write the two-step document: the load and the approve, the status transition, the in-force window of the new version and the close of the superseded one.
2. Write the error catalogue: the codes of each operation, the meaning of each 409 and of the 404, and the message of each condition.
3. Write the extension document for the approval reference, with the read-back on the admin read and the rule that no existing element changes.
4. Document the consumed approval read from the rwb-decision document, with the 2 s budget, the error codes and the element that carries the approved level.
5. Write the record payload: the element map of a level change and the empty rule elements, with the hash link and the outbox row.
6. Write the message set with the three legacy texts unchanged and the mapping of each to its code.
7. Build the three WireMock mappings and their fixtures.
8. Add the contract tests, including the drift test between each fake and this document, and the test that no old monolith base or foreign path appears.
9. Tag the baseline and collect the sign-off of RWB-P10-E8004-APP, the infrastructure story and the test stories of wave 4.

**Done when.** The six contract files validate in the pipeline, the contract tests of section 16 pass, the three fakes answer every consumed path and payload, no path outside the two bases appears, and RWB-P10-E8004-APP and the infrastructure story of the service have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of the load or of the approve is empty, or the level is not a value of LOV-AUTONOMY | Enter {field}. |
| MSG-P4-002 | A role without the Rules and parameters right C or A reaches either operation | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record of the change cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-002 | The caller loaded the version and also approves it | Not restated here: it is rwb-decision's four-eyes message, named by FSD P10 v3 A2.1 AC-EXC-P10-001-03 with the 409, and its wording is not in the extracts |

The three texts are the legacy messages of RWB-E8-004 and keep their wording character for character. The contract adds no message. The wording of a refusal of a value outside LOV-AUTONOMY follows MSG-GEN-001, which names the field; no other wording is asserted.

### 15. Screens and states

None changed in this story. The contract serves SCR-46 Agent monitor, states Shadow, live and paused, through the gateway-bff composite route: the version, its level, its status, its dates and its approval reference. The screen, its fields, its order and its masking belong to the monitor story (RWB-P10-E1063-APP) and its data to RWB-P10-E8004-APP. The three states of the monitor are not the states of a version: a version is LOADED, APPROVED or RETIRED (AC1).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E8004-CON-01 | AC1 | Contract | The two operations of the OpenAPI document; a load and an approve traced through the two-step; an assertion that no other path sets APPROVED; the close of the superseded version |
| TC-P10-E8004-CON-02 | AC2 | Contract | The rights table, the two error lists and the Idempotency-Key header of each POST; the meaning of each 409 and of the 404 |
| TC-P10-E8004-CON-03 | AC3 | Contract | The version resource before and after the extension; a client that ignores the new element; the read-back on the admin read |
| TC-P10-E8004-CON-04 | AC4 | Contract | The consumed approval read documented with purpose, right, errors and budget; the fake answers APPROVED, REFUSED, RETURNED, a differing level, a 404 and a slow answer; one DoA level "L6" that must not be read as a level |
| TC-P10-E8004-CON-05 | AC5 | Contract | The record payload of a level change with empty ruleId and ruleVersion; the hash link; the outbox row; the assertion that no personal data element is present |
| TC-P10-E8004-CON-06 | AC6 | Component | The three legacy message texts compared character for character with the legacy table; the mapping of each to its code; MSG-P7-002 named and not restated |
| TC-P10-E8004-CON-07 | AC7 | Component | The three fakes run against the document; one deliberate drift in each fake must fail the contract test |
| TC-P10-E8004-CON-08 | AC8 | Component | The nine sub-tables complete; 12.4 and 12.6 None; no path outside the two bases; no element of RWB-P10-E3030-CON, RWB-P10-AD020-CON or RWB-P10-E1058-CON restated |

### 17. Guardrails

- No business value in the contract: the levels, the dates, the approval ids and the decision codes stay data of the version row and of the approval.
- No personal data in the answer, the payload, an example or a fake: identifiers and business facts only.
- The contract names only rwb_agent tables and only rwb-agent operations as provided; the approval read and the authorise call are consumed and never restated as this service's (DP-01, DP-13).
- One REST base and one topic per service; a document that names another service's base as provided, or a topic outside the naming rule, fails the review (DP-13, DP-14).
- The approval level of rwb-decision and the autonomy level of rwb-agent are named as different lists in every table, and no example maps one to the other (BR4).
- The approval reference is added and never substituted for an existing element; a client that ignores it still reads a complete version (BR8).
- Every example and fixture is synthetic; no production approval, payload or approval id is copied into a schema or a fake.
- The envelope, the problem response, the Idempotency-Key rule and the record shape come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| None (the legacy story carries no requirement ID) | A level is raised or lowered with the approval each needs, and the version shows the approval it was granted under | The two-step, the approval reference and the consumed approval read | TC-P10-E8004-CON-01, TC-P10-E8004-CON-03, TC-P10-E8004-CON-04 |
| None (the legacy story carries no requirement ID) | The result is written to the decision log with the rule version, and nothing changes when it cannot be | The record payload, the transaction and MSG-P7-003 | TC-P10-E8004-CON-05, TC-P10-E8004-CON-06 |
| D-RCV-60 DP-03 | The record is written locally before the change and carried to the central ledger on the shared topic | The payload of section 12.3 and the record fake | TC-P10-E8004-CON-05, TC-P10-E8004-CON-07 |
| D-RCV-60 DP-13 | The two operations sit on `/api/recovery/agent/v1` and the old monolith base is gone | The base of section 12.1 and the absence test | TC-P10-E8004-CON-08 |
| D-RCV-60 DP-19 | The screen and the rights reach the service through the gateway-bff route | The authorise call of the route and its fake | TC-P10-E8004-CON-07, TC-P10-E8004-CON-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed read and its 2 s client budget | TC-P10-E8004-CON-04 |
| ADR-022 | Local decision record plus central ledger | The record payload and the shared topic | TC-P10-E8004-CON-05 |

The legacy story RWB-E8-004 carries no requirement ID, so no requirement is cited for it and the absence is recorded as GAP-0641. The feature source is the Epics 3 to 8 Specification v3 row E8 · P10 · FEAT-AGT-15 and FSD P10 v3 A2.15.

### 19. Out of scope

- The implementation of the two operations, the approval client, the version write and the record (RWB-P10-E8004-APP).
- The configuration operations baseline, its request bodies, its media types and its error catalogue (RWB-P10-E3030-CON) and the plain level change of Epic 3 (RWB-P10-E3030-APP).
- The autonomy level per decision step and its per-step resolution (RWB-P10-AD020-CON and RWB-P10-AD020-APP).
- The agent runtime and the admin surface of the service (RWB-P10-E1058-CON and RWB-P10-E1058-APP).
- The approvals, their DoA routing, their statuses, their workflow and the central ledger (P7 rwb-decision).
- The roles, the rights, the scope, the masking rules and the authorise contract itself (P4 rwb-access; RWB-P4-E1037-CON).
- The gateway-bff route contract itself (RWB-PLT-N001-CON) and the decision-record library itself (RWB-PLT-E1027-CON).
- The schema column and the migration of the approval reference (RWB-P10-E8004-APP) and the schema `rwb_agent`, its login and the certificate (RWB-P10-E1058-INF).
- The screen SCR-46, its fields and its three states (RWB-P10-E1063-APP).
- The real cross-service proof of the load, the approval and the effect (the integration story of wave 4).
- The field-level completeness of the consumed approval answer (GAP-0641; ASM-1032).
