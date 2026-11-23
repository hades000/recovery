# RWB-P10-E3030-CON Change an autonomy level

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E3030-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-030 for rwb-agent. The autonomy change is fixed as a contract on the service's own configuration operations under `/api/recovery/agent/v1` (DP-13; TSD P10 v2 API-P10-002 to API-P10-004), on the version shape of `agent_policy` and `agent_prompt` (TSD P10 v2 T3.1 and T3.2), on the decision-record payload written through the local library and `rwb.decision-record.v1` (DP-03), on the ordering rule that a version takes effect only after approval, and on the fakes of rwb-decision, rwb-access and the gateway-bff route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-agent**, I want **the autonomy-configuration slice fixed as a contract: the shape of an agent configuration version — the policy and prompt fields with their types, lengths, required flags and lists, the autonomy mode and its list, the status and its list, the dates and the approver — the three configuration operations with their rights, errors and Idempotency-Key rules, the decision-record payload written on a change, the ordering rule that a new version takes effect only after approval and only from its valid-from date, the message set, and the contract fakes for rwb-decision and rwb-access**, so that **the app and test stories of this key build on Day 1 against one agreed, testable shape, and a change of what an agent may do unattended cannot be read one way by the loader, another by the approver and a third by the run**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s client budget is the decoupling rule (DP-11, ADR-020), and the decision record written locally in the same transaction as the change and sealed centrally is the record rule (Temporal and Drools design slides 11 and 16; R-UNI-39; DP-03). Both only work if the seam is written down once. The seam here is small and load-bearing: one version shape used by the load, the approval, the read and the run; one status list that decides when a version is in force; one record payload that names the version and the approver role; and one error map shared by the three operations, so that the same refusal means the same thing to the screen, the test and the run.

The contract also states what this service does not own. The central ledger, its sealing and the ledger read are rwb-decision's; the rights, the roles, the scope and the masking are rwb-access's; the parameters and the reference lists of the Workbench are rwb-case's under the §R3 default ruling. This document therefore declares the consumed record and access sides as fakes and never restates another service's operation as its own (DP-01, DP-03).

Two things this contract deliberately does not do. It does not restate the model-gateway contract of RWB-P10-E2032-CON: how a model call is made, what a run costs and how a fallback is decided are that key's and the run stories'. It does not restate the runtime behaviour of RWB-P10-E1058-CON: what a run does with a guardrail failure, with a timeout or with an output that misses its schema is that contract's. This document fixes what a configuration version is, how it comes into force and how the change is recorded, and nothing else.

The realignment work that leaves the slice: the shared API base, the in-process decision-log write, and the shared configuration service of P3 as the home of the level. In the target the level is `autonomy_mode` of the owning service's version (TSD P10 v2 DF-AGT-008), and the change is one of the three configuration operations the service already publishes. The one open disagreement between sources is recorded rather than smoothed over: the service summary on Arch v5 slide 16 names `GET/POST /agent-policies (admin)` while the operation inventory of TSD P10 v2 T-A.1 and the Ownership Map name `GET /admin/agent-configs`, `POST /admin/agent-configs` and the approve (GAP-0637; ASM-1004).

This story owns no legacy criterion: RWB-E3-030 has two, and both belong to RWB-P10-E3030-APP (AC1 and AC2). Every criterion here is new and tests a contract artefact of the title only.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the REST base `/api/recovery/agent/v1`, the topic `rwb.agent.events.v1` and the shared topic `rwb.decision-record.v1` follow the platform rule and not a local choice (DP-13).
- The CloudEvents 1.0 envelope and the platform error envelope are the platform baseline; this document narrows them where it must and says so (DP-03).
- The decision-record library contract is published (RWB-PLT-E1027-CON): the record shape of chain_seq, inputsRef, ruleId, ruleVersion, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, prev_hash and entry_hash, the hash chain and the outbox relay are its elements, and this story reuses them rather than redefining them (Temporal and Drools design slide 16; DP-03).
- The access contract and the guard of the service template are in force (P4 rwb-access): the capability areas, the rights R, C, A and U and the refusal of a role without the right are read from it, and this contract names the rights without restating the matrix (DP-01; FSD P10 v3 A2.12.3.3).
- The configuration operations exist as published by TSD P10 v2 T-A.1 and carried by the Ownership Map v1 with owner P10: API-P10-002, API-P10-003 and API-P10-004. This story is their contract and declares no operation of another service as its own.
- The lists are those of TSD P10 v2 T3.2: LOV-AGENT, LOV-AUTONOMY (OFF, SHADOW, L1), LOV-CONFIG-STATUS (LOADED, APPROVED, RETIRED), LOV-ROLE, LOV-PRODUCT and LOV-REGION. The list rows are reference data of rwb-case under the §R3 default ruling and are not re-declared here (ASM-0997).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Fix the version shape: the fields of `agent_policy` (DF-AGT-001 to DF-AGT-025) and of `agent_prompt` (DF-AGT-026 to DF-AGT-035) with the physical type, the required flag and the list of each, and the version element that the load, the approval, the read and the run all use.
2. Fix the three operations with method, path, purpose, right, request, response, error codes and the Idempotency-Key rule from TSD P10 v2 T-A.2, and attribute each to rwb-agent.
3. Fix the decision-record payload written on a change: the elements the local record carries, the element that names the configuration version, and the rule that the version row, the record and the outbox row are one transaction.
4. Fix the ordering rule: LOADED, APPROVED, RETIRED, the version in force for a business date, the four-eyes rule of the approval and the refusal codes that go with each.
5. Publish the message set and the error map, with the legacy wording kept character for character and every further message named by ID only.
6. Publish the contract tables of section 12 and the three contract fakes.
7. Add the contract tests: the version shape, the three operations, the record payload, the ordering rule, the message map and a drift test between each fake and this document.
8. Tag the baseline and hand it to the app story of this key, to the test stories and to the integration story of the wave.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A configuration version carries a field this document does not declare, or omits a required one | The load is refused by the validator of the operation before any row is written, and the field is named | MSG-GEN-001 | AC1 |
| X2 | A version carries an autonomy mode outside LOV-AUTONOMY, or a status outside LOV-CONFIG-STATUS | The load is refused; no value is mapped, defaulted or added to a list | MSG-GEN-001 | AC1 |
| X3 | A fake or an implementation drifts from this document | The contract test fails and the merge is blocked | None | AC2, AC3, AC4, AC6 |
| X4 | The record cannot be written when the version is approved | The approval transaction rolls back and the version keeps status LOADED; no outbox row exists | MSG-P7-003 | AC3 |
| X5 | The approver is the loader, or the version does not exist, or it is already APPROVED | The approval is refused with 409 for the four-eyes case and for an approved version, and with 404 for one that does not exist | MSG-P7-002 for the four-eyes case | AC4 |
| X6 | A caller without the right of the operation | Refused with 403; nothing is written and nothing is returned | MSG-P4-002 | AC2, AC5 |
| X7 | A field-level detail of the version or of the record is missing from the source material | The element is named here at the level the source supports, the placeholder is written where a value is needed, and one gap row and its assumptions are carried | None | AC1, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelope, the record library contract, the access contract and the operation inventory as published |
| Negotiable | The element names of the record payload and the file column order are settled with their owners; the version shape, the operations and the ordering rule are fixed by this realignment |
| Valuable | Unblocks the app story of this key and every test that has to read one version shape, one status list and one error map |
| Estimable | One version shape, three operations, one record payload, one ordering rule, one message set, nine tables and three fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the schema, the document, the fake — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Autonomy-configuration contract baseline for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the decision-record library contract of RWB-PLT-E1027-CON is in force
    Given the configuration operations are the three of TSD P10 v2 API-P10-002, API-P10-003 and API-P10-004

  Scenario: AC1 The configuration version shape is fixed (new, D-RCV-60)
    Given the version contract of this story
    When a policy version and a prompt version are validated against it
    Then the version element carries the agent code over LOV-AGENT, the kind POLICY or PROMPT, the version label inside varchar(20), the autonomy mode over LOV-AUTONOMY, the status over LOV-CONFIG-STATUS, the valid-from date, the optional valid-to date and the loader and approver references
    Then a POLICY version also carries the model code and version, the output schema reference, the allowed tools, the confidence floor, the timeout, the daily cost cap, the price per 1k tokens, the alert role, the review date, the promotion conditions, the watched measures and the fallback rule, and a PROMPT version carries the body text and its SHA-256 hash
    Then the approved-by role and the approval instant are read from the approver reference and from updated_at of the row at the APPROVED transition, because agent_policy carries approved_by and no approved_at column
    Then a version whose autonomy mode is outside LOV-AUTONOMY or whose required field is empty is refused with MSG-GEN-001 and no value is mapped or defaulted

  Scenario: AC2 The three configuration operations are fixed and attributed (new, D-RCV-60)
    Given the operation tables of section 12
    When the three operations are reviewed
    Then the read, the load and the approve are each described with method, path, purpose, right, request, response, error codes and the Idempotency-Key rule
    Then the read needs Rules and parameters R, the load C and the approve A, and a caller without the right is refused with 403 and MSG-P4-002
    Then every operation is attributed to rwb-agent on the base /api/recovery/agent/v1 and none is declared as another service's
    Then the summary label /agent-policies of the Arch v5 slide 16 line is recorded as the service summary and not as a path, and this document follows the operation inventory of TSD P10 v2 T-A.1 and the Ownership Map

  Scenario: AC3 The decision-record payload written on a change is fixed (new, D-RCV-60)
    Given the record library contract and the payload of section 12.3
    When a version is approved
    Then the record carries the agent code, the kind, the configuration version, the autonomy mode, the version in force before the change, the approver role, the valid-from date and the record reference
    Then the configuration version travels in the rule-version element of the record and no rule row and no package version is named, because no Drools package decides a configuration change
    Then the version row, the local record and the outbox row are one rwb_agent transaction, and a refused record write leaves the version LOADED and writes no outbox row
    Then rwb.decision-record.DecisionRecorded.v1 is relayed on rwb.decision-record.v1 with the CloudEvents attributes id, source, type, specversion, time, subject and datacontenttype, and carries no personal data

  Scenario: AC4 The ordering rule is fixed (new, D-RCV-60)
    Given a version in status LOADED with valid_from 2026-12-16
    When the version in force for 2026-12-16 is asked for
    Then the answer is the APPROVED version of the agent and not the LOADED one
    When the version is approved by a person other than the loader
    Then it is in force from 2026-12-16 and not before, and the previous version stays readable with its own dates and its own autonomy mode
    Then the loader who approves their own version is refused with 409 and MSG-P7-002, and a version that does not exist is refused with 404
    Then no date, status or level is defaulted to make a version take effect

  Scenario: AC5 The message set and the error map are fixed (new, D-RCV-60)
    Given the messages of the legacy story RWB-E3-030 and the error codes of TSD P10 v2 T-A.2
    When the map is reviewed
    Then MSG-GEN-001 is the refusal of an empty or out-of-list value, MSG-P4-002 the refusal of a role without the right and MSG-P7-003 the refusal of a change that cannot be recorded
    Then each message keeps the legacy wording character for character, and 422, 403 and 503 are the codes each one is answered with where the operation table states them
    Then MSG-P7-002 and MSG-P10-001 are named by ID only, because their wording is not in the legacy message set or the extracts, and no text is invented for them

  Scenario: AC6 The nine contract tables and the three fakes are complete (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.2, 12.4, 12.5 and 12.6 are None, and 12.7 names only rwb_agent tables and the platform library objects
    Then the rwb-decision record stub, the rwb-access guard stub and the gateway-bff route stub answer every path and payload this document declares, and a drift between a fake and this document fails the contract test
    Then this document declares no operation of rwb-decision, rwb-access or rwb-case as provided, and no table of another schema as owned
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One version shape for the load, the approval, the read and the run; the version is `agent_policy` or `agent_prompt` and its label is unique for the agent and the kind | TSD P10 v2 T3.1; ASM-0995 |
| BR2 | The autonomy mode is one of the values of LOV-AUTONOMY and the status one of the values of LOV-CONFIG-STATUS; the contract accepts no other value and maps none | TSD P10 v2 T3.2; ASM-0992 |
| BR3 | A version takes effect only after approval and only from its valid-from date; a LOADED version is never in force | FSD P10 v3 A2.1 AC-ALT-P10-001-01; TSD P10 v2 DF-AGT-021 to DF-AGT-023 |
| BR4 | The loader may not approve their own version | FSD P10 v3 A2.1 AC-EXC-P10-001-03 |
| BR5 | The version row, the local decision record and the outbox row are one transaction; a refused record write leaves the version LOADED | Principle 5; R-UNI-39; DP-03 |
| BR6 | The configuration version travels in the rule-version element of the record, and no rule row and no package version is named, because no Drools package decides a configuration change | Legacy RWB-E3-030 AC1; ASM-0998 |
| BR7 | One REST base per service and one topic per service: this document declares `/api/recovery/agent/v1` and consumes the shared record topic; it never declares another service's path as provided | DP-13; DP-01; Ownership Map v1 |
| BR8 | The rights are rwb-access's: the contract names the capability area and the right of each operation and never restates role membership | DP-01; FSD P10 v3 A2.12.3.3; ASM-0994 |
| BR9 | Both admin operations carry the Idempotency-Key rule, and a repeat with the same key writes nothing new | TSD P10 v2 T-A.2; R-UNI-40 |
| BR10 | No business value in the contract: the level, the label, the dates, the thresholds and the review date are rows of the loaded version and never literals of this document | BR-P10-012; Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | LOAD accepted | the file follows the version shape, the lists and the identity rule | LOADED |
| None | LOAD refused | a required field is empty, a value is outside its list, or the label exists for the agent and the kind | None, and nothing is written |
| LOADED | APPROVE | the approver is not the loader and the record is written in the same transaction | APPROVED |
| LOADED | SELF_APPROVAL refused | the approver is the loader | LOADED, unchanged |
| LOADED | RECORD refused | the local decision record cannot be written | LOADED, because the transaction rolls back |
| APPROVED | IN FORCE | the business date is at or after `valid_from` and before `valid_to` | APPROVED, in force for the date |
| APPROVED | RETIRE | `valid_to` is passed or a later version is approved for the same agent | RETIRED, and the row stays readable |

The status column carries the three values of LOV-CONFIG-STATUS (TSD P10 v2 DF-AGT-021); "in force for a date" is read from the status with the two date columns and is not a fourth value, so the contract adds no status and no state to the table. The contract document itself moves Draft → In review → Baselined as the app and test stories accept it, and a breaking change to a consumed element returns it to In review.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the version shape, the three operations, the record payload, the ordering rule, the message map and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to the version shape or to the record payload, and any change to the ordering rule |
| The rwb-decision owner | Owns the record library and the shared topic, and signs off the payload and the transaction rule taken from its document |
| The rwb-access owner | Owns the capability areas, the rights and the role matrix, and signs off the right named on each operation |
| The rwb-case owner | Owns the lists and the parameters, and confirms that this contract re-declares neither |
| The rwb-agent app and test stories of this key | Review and accept the parts they consume |
| Center of excellence analyst (RW-COE) and risk and model risk officer (RW-RISK) | Named as the actors of the load and of the approval; the roles stay rows of rwb-access |

The deployment identity that serves the three operations is Not specified in the source documents (GAP-0637; ASM-1009); the document names it "the rwb-agent login (DP-02)" and leaves the name to the platform set-up story.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Version element | agent code over LOV-AGENT, kind POLICY or PROMPT, version label inside varchar(20), autonomy mode over LOV-AUTONOMY, status over LOV-CONFIG-STATUS, valid-from date, optional valid-to date, loader reference, approver reference |
| Policy fields of the version | model code, model version, output schema reference, allowed tools, confidence floor, timeout in seconds, daily cost cap, price per 1k tokens, alert role, review date, promotion conditions, watched measures, fallback rule, segment product group, segment region (DF-AGT-004 to DF-AGT-020) |
| Prompt fields of the version | body text and its SHA-256 hash in `body_hash`, with the same status, date and loader elements (DF-AGT-026 to DF-AGT-035) |
| Standard record columns | state, version, created_at, created_by, updated_at, updated_by (TSD P10 v2 T3.0); the approval instant is `updated_at` at the APPROVED transition |
| Load request | multipart file, kind, agent, validFrom, and the Idempotency-Key header (TSD P10 v2 API-P10-003) |
| Record payload | agent code, kind, configuration version, autonomy mode, the version in force before the change, approver role, valid-from date, record reference |
| Event envelope | the CloudEvents 1.0 attributes and the record reference; identifiers and facts only, no personal data |

The element names of the record payload are those of the record shape of the Temporal and Drools design (slide 16), read into this contract as the shell of the record, with the configuration version travelling in the rule-version element (ASM-1005); how the library names each member in JSON is its own and is not restated. The kind takes the two values POLICY and PROMPT, from the two resource names of TSD P10 v2 T3.1, because T3.2 carries no list for it (GAP-0637; ASM-1006). The column set and the column order of the loaded file are Not specified in the source documents (GAP-0637; ASM-1007), and this document fixes the element set from the FSD field catalog and TSD P10 v2 T3.1 and leaves the physical layout to the contract freeze. `agent_policy` carries `approved_by` and no `approved_at`, so the approval instant is a derived element and not a column (GAP-0637; ASM-0996).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Method | Path | Purpose | Right | Errors | Idempotency |
|---|---|---|---|---|---|---|
| API-P10-002 | GET | `/api/recovery/agent/v1/admin/agent-configs` | List the policy and prompt versions per agent with status and dates; query agent, kind, status | Rules and parameters R | 401, 403, 503 | Not applicable |
| API-P10-003 | POST | `/api/recovery/agent/v1/admin/agent-configs` | Load a new policy or prompt version from a checked file; multipart file, kind, agent, validFrom | Rules and parameters C | 401, 403, 409, 422, 503 | Idempotency-Key header |
| API-P10-004 | POST | `/api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` | Approve a loaded version; no request body | Rules and parameters A | 401, 403, 404, 409, 503 | Idempotency-Key header |

The three operations are rwb-agent's and are declared once, by this contract. The service summary line of Arch v5 slide 16 names `GET/POST /agent-policies (admin)`; that line is a summary of the admin surface and not an operation inventory, and the paths above are the ones the operation inventory of TSD P10 v2 T-A.1 carries (GAP-0637; ASM-1004). The monitor read `GET /api/recovery/agent/v1/admin/agent-runs` (API-P10-001) is the monitor stories' and is not declared here.

#### 12.2 REST operations consumed

None. This contract consumes the record library and the access guard as platform elements and declares no REST operation of another service; a call of rwb-decision or rwb-access from the change path would be a separate C dependency and is not claimed (ASM-0999).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | record reference, agent code, kind, configuration version, autonomy mode, the version in force before the change, approver role, valid-from date |

The payload is written to the outbox in the same transaction as the version row and relayed with the CloudEvents 1.0 envelope by the record library (DP-03). No agent event is published by a change: the P10 OUT line of Arch v5 slide 16 names AgentRunCompleted only, the agent event `rwb.agent.AgentRunCompleted.v1` (EV-28) on the service topic `rwb.agent.events.v1` is the run path's, and a configuration change publishes none.

#### 12.4 Events consumed

None. The change path reads no topic and this contract declares no inbox handler.

#### 12.5 Workflows and activities

None. The load and the approval are synchronous operations of the request path and the record is written in the request transaction; this contract declares no workflow, no activity and no task queue. AgentRunWorkflow on the queue `rwb-agent` reads the version in force at run time and belongs to the run contract.

#### 12.6 Schedules

None. No Schedule creates, promotes or retires a configuration version: the effective date is `valid_from` of the row, and the Arch v5 job map names no job for an agent configuration change.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_policy | P10 (rwb_agent) | The policy version and its autonomy mode, status, dates, loader and approver (DF-AGT-001 to DF-AGT-025) |
| agent_prompt | P10 (rwb_agent) | The prompt version on the same version element (DF-AGT-026 to DF-AGT-035) |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | The outbox, inbox and idempotency envelope of the record write and the two admin operations |

No other table is declared. `decision_log_entry` and `approval` are rwb-decision's and `role` and `permission` are rwb-access's; `parameter_catalog`, `parameter_value`, `reference_row` and `lov_value` are rwb-case's, and the contract declares none of them (DP-01; Ownership Map v1).

#### 12.8 Contract fakes

| Fake | Serves | Documented answer |
|---|---|---|
| rwb-decision record stub | The record library contract and `rwb.decision-record.v1` (DP-03) | A committed record with its reference; a forced write failure; the outbox row and its relay with the CloudEvents attributes |
| rwb-access guard stub | The rights of the three operations (P4) | Rules and parameters R granted to RW-AUDIT, C to RW-COE and A to RW-RISK; a role without the right refused with 403 and MSG-P4-002 |
| gateway-bff route stub | The DP-19 route of SCR-46 | The merged screen answer carrying the version in force, its autonomy mode and its state; the refusal path of a role without the right; the degraded answer when the agent read is unreachable |

A drift between any fake and this document fails the contract test. The list rows of TSD P10 v2 T3.2 are not faked here; they arrive through the reference-data wiring of the platform set-up story and this contract adds no list dependency (ASM-0997).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed | The read, the load and the approve on `/api/recovery/agent/v1`; no operation of another service |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.v1` published through the outbox by the record library |
| Temporal | None | The change is synchronous; the run that reads the version is AgentRunWorkflow's |
| File | 1 per load | The checked configuration file is the input of the POST and is stored as rows |

### 13. Solution plan

**Deliverables.** `contract/agent-config-version.yaml` (the version shape of `agent_policy` and `agent_prompt`, with the lists of TSD P10 v2 T3.2), `contract/agent-config-operations.yaml` (the three operations with rights, errors and the Idempotency-Key rule), `contract/agent-config-record.md` (the record payload, the transaction rule and the event), `contract/agent-config-ordering.md` (LOADED, APPROVED, RETIRED, the in-force rule and the four-eyes refusal), `contract/agent-config-messages.md` (the message map) and the three WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/agent/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Both dependencies are platform contract stories and neither is a build dependency of this story, which is Day 1 by rule. DP-13 adds no dependency because it is a naming rule.

**Build steps**

1. Write the version shape and the list references; add a schema lint that refuses a field outside the shape and a value outside its list.
2. Write the three operations with their rights, errors and the Idempotency-Key rule, and the note that resolves the Arch v5 summary label against the operation inventory.
3. Write the record payload and the transaction rule from the record library contract, with the version in the rule-version element.
4. Write the ordering rule: the three statuses, the in-force test, the four-eyes refusal and the 404 case.
5. Write the message map with the three legacy texts character for character and the two further IDs named only.
6. Build the three fakes and their fixtures.
7. Add the six contract tests, including the drift test between each fake and this document.
8. Tag the baseline and collect the sign-off of the app and test stories of this key and of the integration story of the wave.

**Done when.** The five contract files validate in the pipeline, the six contract tests pass, the three fakes answer every path and payload this document declares, and the app and test stories of this key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value of a version is empty, or a value is outside its list | Enter {field}. |
| MSG-P4-002 | A caller without the right of the operation calls the read, the load or the approve | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written on the approval | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three texts are the legacy texts of RWB-E3-030 and keep their wording character for character; this contract adds no message. Two further messages are named by the specifications and are recorded by ID only, because their wording is in neither the legacy message set nor the extracts: MSG-P7-002 for an approver who is also the loader (FSD P10 v3 A2.1 AC-EXC-P10-001-03) and MSG-P10-001 for a configuration file that fails a check (FSD P10 v3 A2.1 AC-EXC-P10-001-02). The `{field}` value names a field of the version shape only, and no text is invented for the two IDs.

### 15. Screens and states

None in this story. The contract serves SCR-46 Agent monitor, states Shadow; live; paused, through the gateway-bff composite route only (DP-19), and the screen, its fields and its masking belong to the monitoring stories (RWB-P10-E1063-APP and RWB-P10-E2031-APP). The states are named here because the route answers them: the contract fixes the elements the route may carry — the version in force, its autonomy mode and its status — and fixes no panel and no layout. How a state of the screen maps to a value of LOV-AUTONOMY is Not specified in the source documents (GAP-0637; ASM-1008) and is settled with the monitor stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E3030-CON-01 | AC1 | Contract | A policy version and a prompt version validated against the version shape; an empty required field, an autonomy mode outside LOV-AUTONOMY and a version label over 20 characters are each refused |
| TC-P10-E3030-CON-02 | AC2 | Contract | The three operations documented with method, path, purpose, right, errors and Idempotency-Key; the right of each checked against the operation inventory; the Arch v5 summary label resolved |
| TC-P10-E3030-CON-03 | AC3 | Contract | A committed record, a forced write failure and the relayed event; the payload fields of section 12.3 compared element by element |
| TC-P10-E3030-CON-04 | AC4 | Component | A LOADED version with valid_from 2026-12-16 and an APPROVED version; the in-force answer before and after the approval; the self-approval and the missing version |
| TC-P10-E3030-CON-05 | AC5 | Component | The three messages compared character for character with the legacy texts; the two further IDs present with no text |
| TC-P10-E3030-CON-06 | AC6 | Component | The nine sub-tables complete; 12.2, 12.4, 12.5 and 12.6 None; the three fakes matching this document and failing on a drift |

### 17. Guardrails

- No business value in the contract: the level, the label, the dates, the thresholds, the review date and the alert role are rows of the loaded version and never literals of this document (BR-P10-012).
- No personal data in an event, a fake or an example: the record carries agent codes, list values, dates and role names, and the loader and approver are references and not identities.
- The contract names only `rwb_agent` tables as owned and only rwb-agent's operations as provided; the record library, the access guard and the lists are consumed and never restated as this service's (DP-01, DP-03, DP-13).
- One REST base and one topic per service; a document that names another service's base as provided, or a topic outside `rwb.agent.events.v1` and the shared record topic, fails the review (DP-13).
- The version shape accepts no value outside its list and maps none, so a level the source does not name cannot enter through a file.
- Every example and fixture is synthetic; no production file, record or payload is copied into a schema or a fake.
- The envelope, the record shape and the access guard come from the platform library; this story narrows them but never redefines them.
- The wording of every message that this contract names is the legacy wording; where a source gives no text, the ID is recorded and no text is written.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| None (the legacy story carries no requirement ID) | The autonomy level of one agent and one decision is changed as a versioned configuration row | The version shape, the three operations and the ordering rule | TC-P10-E3030-CON-01, TC-P10-E3030-CON-02, TC-P10-E3030-CON-04 |
| FEAT-AGT-12 | Change an autonomy level for one agent and one decision, as a versioned configuration row | The version element, the autonomy mode list and the status list | TC-P10-E3030-CON-01, TC-P10-E3030-CON-04 |
| BR-P10-012 | No value a business person may change is written in code | The version shape as data and the refusal of a value outside its list | TC-P10-E3030-CON-01, TC-P10-E3030-CON-05 |
| D-RCV-60 DP-03 | The decision record is written locally in the same transaction and the shared topic carries it to the central ledger | The record payload, the transaction rule and the event of section 12.3 | TC-P10-E3030-CON-03 |
| D-RCV-60 DP-13 and DP-19 | One base and one topic per service, and the screen composed through the gateway-bff route | The three operation paths, the route fake and the screen note of section 15 | TC-P10-E3030-CON-02, TC-P10-E3030-CON-06 |
| R-UNI-39 | The state change, the record and the outbox row are one transaction | The transaction rule of section 12.3 and the rollback of AC3 | TC-P10-E3030-CON-03 |
| R-UNI-40 | A repeat of a request has no further effect | The Idempotency-Key rule of the two admin operations | TC-P10-E3030-CON-02 |

The legacy story RWB-E3-030 carries no requirement ID and no BRD in the extracts carries FEAT-AGT-12, so the first row records the absence and the trace runs through the feature (Epics 3 to 8 Specification v3 row E3 · P10 · FEAT-AGT-12; FSD P10 v3 A2.12; GAP-0637).

### 19. Out of scope

- The implementation of the three operations, the validator, the repository and the record writer (RWB-P10-E3030-APP).
- The model-gateway contract of this service: the model call, the cost and the fallback of R-UNI-32 (RWB-P10-E2032-CON and the run contract).
- The runtime behaviour of a run: the guardrail checker, the output schema check, the timeout and the run status (RWB-P10-E1058-CON and the run stories).
- The writer and the sealing of the central ledger, the approval table and the ledger read (P7 rwb-decision), and the record library and the shared topic themselves (RWB-PLT-E1027-CON).
- The capability areas, the rights, the role matrix, the scope and the masking (P4 rwb-access).
- The lists, the parameters and the reference data, and their contract (P3 rwb-case), and the reference-data wiring of the platform set-up story.
- The autonomy level per decision step and the step-up with committee approval, which carry their own contracts (RWB-P10-AD020-CON and RWB-P10-E8004-CON).
- SCR-46 and its panels (RWB-P10-E1063-APP and RWB-P10-E2031-APP), and the gateway-bff route contract itself (RWB-PLT-N001-CON).
- Deployment: chart values, queue and topic provisioning, dashboards and the runbook.
- The real cross-service proof of the change, which belongs to the integration story of the wave.
