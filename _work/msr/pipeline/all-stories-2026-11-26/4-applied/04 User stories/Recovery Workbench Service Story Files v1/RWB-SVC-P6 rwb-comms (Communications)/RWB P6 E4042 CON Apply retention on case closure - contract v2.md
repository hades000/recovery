# RWB-P6-E4042-CON Apply retention on case closure

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4042-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-042 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E4042-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the retention coverage of rwb-comms — the `GET /cases/{caseId}/retention-coverage` read fixed under `/api/recovery/comms/v1` because no source names a retention operation, its five-element coverage answer, the consumed `rwb.case.CaseStateChanged.v1` element with the closing state, the decision element of code D9 with rule R-WO-47 or R-WO-48, the case-hold fact with reason `RETENTION_CLASS_MISSING`, the statement that this service owns no retention class, period, disposal or run, the nine contract tables and the three fakes**, so that **the app story of this legacy key builds against one fixed, testable contract on Day 1 and a retention class, a period, a closing state, a reason code or a disposal can never be declared by rwb-comms without a failing build**.

### 2. Business rationale

Contract-first REST with one hop is the decoupling decision (DP-13, ADR-020). The legacy key is thin and its retention work belongs to the document hub: R-WO-47 closes a case only when a retention class is on every document, R-WO-48 holds that closure and raises a Document Hub task, and the class, its period and the disposal or extension decision are the document hub's reference data (REQ-DCM-010, REQ-DCM-019, NFR-028 with DL26, NFR-074; Ownership Map: `retention_rule`, `retention_action` and JOB-17 all P5). What the communications service owns is the notice, and the notice is what points at a document. The legacy story nevertheless names two notice endpoints and screen SCR-33, and no source gives it a retention operation at all: the TSD P6 endpoint inventory stops at API-P6-011, and the P5 API rows carry no read of a document's retention class.

The baseline therefore has two jobs. It fixes the one element this service can own — a read of the coverage of the notice documents of a case, with a fixed answer shape and a fixed access right — and it fixes, in the negative, everything this service must never declare: no retention table, no class, no period, no disposal, no retention event and no Schedule, because the only retention run of the catalogue is JOB-17 of rwb-document. It also fixes the two consumed elements the check needs, the closing event of rwb-case and the hold-and-task fact, and the decision element through which the coverage becomes a recorded decision under the library of DP-03. The naming is fixed as the checks require: schema `rwb_comms`, base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with retry and `.dlt` topics, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`.

The contested points are carried as gaps and assumptions rather than settled quietly: no source names the coverage operation or its answer shape, the plan declares no C row for the P5 retention read, the hold-and-task operation of rwb-case has no name and no message, the retention class list and the periods are unset, and screen SCR-33 of the legacy story is a template screen that does not fit an unattended check.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule and not a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it says so.
- The notice generation contract RWB-P6-E1052-CON and the dispatch contract RWB-P6-E2021-CON are published, so the `notice` fields this read projects have one owner document.
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided. The retention class is P5 rwb-document's, the case state, the task and the timer are P3 rwb-case's, and the decision ledger is P7 rwb-decision's.
- The retention class read of a document has no published row in any source and no C row in the plan of this key; the path and the answer of that read are Not specified in the source documents (GAP-1141; ASM-2088), and this baseline declares it as consumed and faked.
- The hold of the closure and the Document Hub task of R-WO-48 have no operation name, no body and no message in any source; the reason code `RETENTION_CLASS_MISSING`, the state `RETENTION_RUNNING`, the owner "Operational Excellence", the system "Document Hub" and the five working days are the rule's own columns (GAP-1143; ASM-2090).
- The retention classes, the class per document type and the periods are unset (NFR-028, DL26) and are not declared here in any form (GAP-1144; ASM-2091).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive change to the rwb-comms OpenAPI 3.1 document: the coverage resource, the 200 answer, the four error responses, the access right and no Idempotency-Key, and mark the operation as fixed by this baseline because no source names it.
2. Fix the coverage answer: one entry per notice document of the case with `noticeId`, `caseId`, `documentId`, `noticeType` and `classPresent`, and no class value, no period and no disposal anywhere in the answer.
3. Record the consumed `rwb.case.CaseStateChanged.v1` element with its topic, its owner, its key, its payload and the closing state of R-WO-47, and record the dedupe rule.
4. Record the negative declarations of the baseline: no retention table, no retention column, no class, no period, no disposal, no retention event of this service, no workflow, no Schedule and no job.
5. Record the case-hold and Document Hub task element as consumed and faked, with reason code `RETENTION_CLASS_MISSING` and the five working days of R-WO-48 as the task timer of rwb-case.
6. Record the decision element: decision code D9, rule R-WO-47 or R-WO-48, rule version, the covered and the missing-class result, through the local decision-record library on `rwb.decision-record.v1`.
7. Publish the nine contract tables of section 12 and the three contract fakes.
8. Add the contract tests: schema validation, the closed answer, the event validation against the registry, the absence tests of section 4 step 4, the absence of a cross-schema read, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-P6-E4042-APP and the platform contract owners.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | The platform schema message | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | The answer carries a class value, a period or a disposal | The closed-set test fails the build | None | AC2 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X5 | A consumer cannot deserialise a `rwb.comms` event, or an event of this service is declared | The registry test and the absence test fail the build | None | AC4 |
| X6 | A retention table, a retention column or a Schedule appears in the document or in the schema note | The absence test fails the build | None | AC4 |
| X7 | The document declares another service's operation as provided | The review fails the baseline; the operation is described as consumed and faked | None | AC8 |
| X8 | The hold-and-task row is called with an operation no source names | The row carries the placeholder and the fake answers the published document | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the two same-service contracts it projects and the Ownership Map only |
| Negotiable | The answer field types, the class code element and the hold-and-task body are settled with the P5, P3 and gateway-bff owners; the base, the event name and the decision code are fixed by the target and by R-WO-47 and R-WO-48 |
| Valuable | Unblocks the app story of this key on Day 1 and stops the service from ever declaring a retention class, a period or a disposal of its own |
| Estimable | One document change, one event element, one decision element, nine contract tables, three fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the retention coverage of rwb-comms

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-comms is /api/recovery/comms/v1 and its topic is rwb.comms.events.v1
    Given the ownership map gives the retention class to rwb-document and the case state, the task and the timer to rwb-case

  Scenario: AC1 The coverage read is declared and validates (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /cases/{caseId}/retention-coverage under the base /api/recovery/comms/v1, owned by rwb-comms, with the answer of status 200
    Then the operation declares capability area Documents with right R and scope applied, and no Idempotency-Key
    Then it declares the error responses 401, 403, 404 and 503 with one envelope and one message ID per condition
    Then the document marks the operation as fixed by this baseline, because no source names a retention operation of rwb-comms and the TSD P6 endpoint inventory stops at API-P6-011

  Scenario: AC2 The coverage answer is a closed set with no retention value (new, D-RCV-60)
    Given the coverage resource of the baseline
    When its properties are compared with the ownership map
    Then an entry carries noticeId, caseId, documentId, noticeType and classPresent, and classPresent is a boolean
    Then the answer carries no class code, no class list, no period, no disposal and no task state
    Then the class fact of an entry is declared as received from the rwb-document contract at the moment of the read and never stored in rwb_comms
    Then the exact field types, the maximum page size and the optional class code element are Not specified in the source documents (GAP-1142; ASM-2089) and the document marks them so
    Then a build that adds a retention value to the answer fails the closed-set test

  Scenario: AC3 The consumed closing event is fixed (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with the event catalogue
    Then rwb.case.CaseStateChanged.v1 is declared as consumed, event 05 of the catalogue on rwb.case.events.v1, owner P3 rwb-case, keyed by caseId
    Then its payload is declared as caseId, fromState, toState and changedAt, with no personal data field
    Then the closing state that starts the check is CASE_CLOSED, the closing state of R-WO-47
    Then the other states of rwb-case are declared as its vocabulary and as data of their owner, not as contract constants
    Then the dedupe rule by the CloudEvents id and the idempotence of one case and one closing state are declared
    Then the document declares no consumed event of any other service and no second topic for this capability

  Scenario: AC4 This service owns no retention element and no run (new, D-RCV-60)
    Given the tables, events, workflows and schedules of the baseline
    When the nine sub-tables are reviewed
    Then no retention table and no retention column is declared in rwb_comms, and retention_rule, retention_action, document, document_type and case_document_check are named as P5 rwb-document's
    Then the class, the class per document type, the periods and the disposal or extension decision are declared as the owner's reference data and never as contract constants
    Then no event of rwb-comms announces a retention action, and the decision record stays on the shared rwb.decision-record.v1 through the library (DP-03)
    Then no workflow, no activity, no Schedule, no Quartz row and no job table is declared, and JOB-17 is declared as rwb-document's Schedule
    Then an absence test fails a build that declares a retention table, a retention column, a retention event or a Schedule

  Scenario: AC5 The case-hold and Document Hub task element is consumed and faked (new, D-RCV-60)
    Given the consumed row of the baseline for the case fact
    When it is compared with R-WO-48
    Then the reason code is RETENTION_CLASS_MISSING and the state it holds is RETENTION_RUNNING, as the rule names them
    Then the task, its owner Operational Excellence, its Document Hub system and its five working days are declared as rwb-case's and not as state of this service
    Then the operation name, its body and the message of a missing class are Not specified in the source documents (GAP-1143; ASM-2090) and the document marks them so
    Then the row is declared as consumed, one hop, never as provided, and the rwb-case fake answers the accepted and the refused case
    Then the baseline declares that a missing, refused or late answer never produces a covered outcome

  Scenario: AC6 The decision element is fixed with its code and its rule (new, D-RCV-60)
    Given the decision element of the baseline
    When it is compared with R-WO-47, R-WO-48 and the decision-record library
    Then the decision code is D9, the rule is R-WO-47 for a covered coverage and R-WO-48 for a missing class, and the rule version in force is carried with it
    Then the element is declared on the shared rwb.decision-record.v1 through the local library and never as an event of this service
    Then the results are COVERED for the all-present case and CLASS_MISSING for the case with at least one absent class, and no result carries a class value or a period
    Then the element declares that a failed write blocks the step and raises the incident of R-UNI-39

  Scenario: AC7 The three contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the event it serves
    Then the rwb-document fake answers a class present, a class absent, a document absent and an answer beyond the budget
    Then the rwb-case fake answers the closing event with toState CASE_CLOSED, a repeat delivery with the same CloudEvents id, an accepted fact with reason RETENTION_CLASS_MISSING and a refused fact
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The nine tables are complete and no cross-schema read is declared (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the ownership map, with None where the element is empty
    Then the tables named as owned are notice, template, merge_field and the local decision record, and recovery_case, task, timer, decision_log_entry, document, document_type, retention_rule, retention_action and case_document_check are named as other owners' and consumed only through their contracts
    Then the document declares no view of this service and no read of a v_ace_ view
    Then the call-type summary declares one operation provided, two consumed, no event published and one consumed, and no Temporal and no file call
```

These eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P6-E4042-APP and they copy no criterion of the legacy story. The legacy criteria of RWB-E4-042 are AC1 and AC2, both owned by the app story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId and carries no personal data | Architecture v5 slides 42 and 43 notes |
| BR4 | A read declares no Idempotency-Key; this baseline has no POST of its own | Architecture v5 platform baseline |
| BR5 | Error responses use one envelope and one message ID per condition; the message texts copied from the legacy story stay unchanged | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR8 | This service owns no retention class, period, disposal or retention run: they are rwb-document's, and JOB-17 is its Schedule | Ownership Map; Architecture v5 slides 16, 41 and 44; NFR-028 |
| BR9 | The closing state `CASE_CLOSED`, the reason code `RETENTION_CLASS_MISSING`, the five working days and the other case states are data of their owners and not contract constants | R-WO-47; R-WO-48 |
| BR10 | The decision record is the local library's entry with code D9 on the shared `rwb.decision-record.v1`, never a new event of this service | DP-03; Architecture v5 slide 42 (event 08) |
| BR11 | No workflow and no Schedule is part of this capability: the trigger is the consumed event | Template and Rules §R5.5 (DP-10 not applied); Architecture v5 slide 44 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The read, the answer, the event element, the negative declarations and the decision element are described | In review |
| In review | Consumer sign-off | The app story and the rwb-document, rwb-case, rwb-decision and gateway-bff owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example an optional class code in an entry | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a retention value appears in the answer | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A retention table, a retention event or a Schedule appears | The absence test of AC4 fails | In review |

The coverage states of section 9 of the app story are the app story's; this baseline fixes the answer and the negative declarations and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI and AsyncAPI documents and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the fixed coverage path and the correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, and the rwb-document, rwb-case, rwb-decision and gateway-bff owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule and the decision library the document reuses |
| Data steward | Confirms that no personal data field and no retention value is declared in the answer or in an event |

The per-service login name behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-comms login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Coverage resource | One entry per notice document of a case: `noticeId` DF-LEG-015, `caseId` DF-LEG-016, `documentId` DF-LEG-017, `noticeType` DF-LEG-018 and `classPresent`; the class value is not part of the answer |
| Closing event | `caseId`, `fromState`, `toState`, `changedAt` of `rwb.case.CaseStateChanged.v1`, with `toState` `CASE_CLOSED` of R-WO-47 as the trigger |
| Case fact | The hold of the closure and the Document Hub task with reason `RETENTION_CLASS_MISSING`; the body beyond the reason code and the case ID is Not specified in the source documents (GAP-1143; ASM-2090) |
| Decision element | Decision code D9, rule R-WO-47 or R-WO-48, rule version, case ID, notice ID, result COVERED or CLASS_MISSING, decided at; DF-DEC-001 to DF-DEC-018 |
| Event payloads | IDs, codes and dates only; no name, address, identity number or contact point |
| Not declared | Any retention class, class list, period, disposal, retention action or retention run; those are rwb-document's reference data (GAP-1144; ASM-2091) |

The field-level types, lengths and required flags of the coverage entry are settled in the baseline review; this story fixes the five element names, the boolean presence fact and the closedness of the answer.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/retention-coverage` | Coverage of status 200 out: one entry per notice document of the case with `noticeId`, `caseId`, `documentId`, `noticeType` and `classPresent` | Documents, right R, scope applied | Not applicable |

The operation answers 401, 403, 404 and 503, each with the error envelope and one message ID of section 14. The operation is fixed by this baseline because no source names a retention operation of rwb-comms (GAP-1142; ASM-2089); the document carries that statement in its description, so no reader mistakes the path for a legacy one.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | the retention class read of a document on the rwb-document contract | P5 rwb-document | The class present or absent per document, faked. No source names the path and the plan declares no C row for it (GAP-1141; ASM-2088) |
| POST | the case fact that holds the closure and asks for the Document Hub task with reason `RETENTION_CLASS_MISSING` | P3 rwb-case | The hold and the task of R-WO-48, faked. The operation, its body and the message are Not specified in the source documents (GAP-1143; ASM-2090) |

Each row is one hop on the owner's published contract, and no row reads a table or a view of another service. The document declares no other consumed operation: in particular it declares no reference-data read, no approval, no ledger write and no file call, because those capabilities are not part of this legacy key.

#### 12.3 Events published

None. The catalogue carries no retention event of rwb-comms, and the decision record is relayed on the shared `rwb.decision-record.v1` by the local library of DP-03, not by an event of this service.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | caseId, fromState, toState, changedAt; consumed as the trigger of the coverage check, with `toState` `CASE_CLOSED` of R-WO-47 and dedupe by the CloudEvents id |

This is the only consumed event of the baseline. The catalogue names rwb-comms as one of its consumers, so the row is not a new claim of this document.

#### 12.5 Workflows and activities

None. The trigger is the consumed event and the check is one listener step in rwb-comms; the operation and the decision element name no workflow and no activity. DP-10 is not in the pattern set of this key, so no Temporal element is declared here and the absence test of AC4 fails a build that adds one.

#### 12.6 Schedules

None. The only retention run of the catalogue is JOB-17 of rwb-document on its own Schedule (Architecture v5 slide 44), and this baseline declares no Schedule, no Quartz row, no shared job table and no batch table.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | The notice rows the coverage read projects: `id`, `case_id`, `document_id`, `notice_type` |
| template, merge_field | P6 (rwb_comms) | Read only, for the notice type and the template provenance of an entry |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The coverage decisions of code D9 (DP-03) |

`retention_rule`, `retention_action`, `document`, `document_type` and `case_document_check` are P5 rwb-document's, `recovery_case`, `task` and `timer` are P3 rwb-case's, `decision_log_entry` is P7 rwb-decision's, `interaction` is P1 rwb-source-data's and `outbound_item` and `interface_config` are P2 rwb-integration's; the document names them only as consumed answers (DP-01). No table of `rwb_comms` carries a class, a period or a disposal (AC4).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document WireMock | A class for a document, no class for a document, a document absent, an answer beyond the budget; the class value is an opaque code of the owner and the list behind it is stubbed with the placeholder (GAP-1141; ASM-2088) | App story, contract tests |
| rwb-case WireMock | `CaseStateChanged` with `toState` `CASE_CLOSED`, a repeat delivery with the same CloudEvents id, an accepted fact with reason `RETENTION_CLASS_MISSING`, a refused fact | App story, contract tests |
| decision-record library stub | A healthy chain and outbox, and a stopped chain | App story, contract tests |

The hold-and-task body of the rwb-case fake carries the placeholder until the rwb-case owner publishes the operation (GAP-1143; ASM-2090).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 consumed | The coverage read provided; the class read of P5 and the case fact of P3 consumed; one hop each |
| Kafka | None declared as published, 1 declared as consumed | `rwb.case.CaseStateChanged.v1`; the decision record is the library's on the shared topic |
| Temporal | None | No workflow, no activity and no Schedule: the trigger is the event |
| File | None | No file is read or written by this capability |

### 13. Solution plan

**Deliverables.** The additive change to `openapi/rwb-comms-v1.yaml` for the coverage read, the AsyncAPI fragment note naming the one consumed event, the contract README rows for the closed answer, the negative declarations and the decision element, and the three WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is applied as a prohibition and adds no dependency: the class arrives on the owner's contract. DP-10 is not applied: no Schedule, no Quartz row, no workflow. DP-14 applies through the naming rule of the platform library, which the document restates and does not add as a dependency.

**Build steps**

1. Add the coverage resource and the 200 answer to the OpenAPI document and validate the closed-set rule of AC2 in the pipeline.
2. Record the consumed event element of AC3 and validate the AsyncAPI fragment against the registry.
3. Record the negative declarations of AC4 and write the absence test for a retention table, a retention column, a retention event and a Schedule.
4. Record the consumed case fact of AC5 with the placeholder on its operation, body and message.
5. Record the decision element of AC6 with code D9, the two rules and the two results.
6. Publish the three fakes and the eight contract tests; a drift between a fake and the document fails the build.
7. Baseline tag and the consumer sign-off note, including the app story and the rwb-document, rwb-case and gateway-bff owners.

**Done when.** The OpenAPI and AsyncAPI artefacts validate in the pipeline, the eight contract tests pass, the three fakes answer every consumed path and the drift test is green, and the app story has accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The role lacks the Documents right | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The schema-validation message of a failed response body and the message of a consumed call that does not answer in time are the platform's own and are not redefined here. The message a missing class shows and the message a refused case fact returns are Not specified in the source documents (GAP-1143; ASM-2090), because R-WO-48 names the hold and the task and no source names a message ID for either.

MSG-P7-003 and MSG-P4-002 are copied unchanged from the legacy story, which is the source of both texts.

### 15. Screens and states

The baseline serves the coverage of a case on the case record documents panel through the gateway-bff composite route (DP-19); the panel, its field list and its masking belong to the story that owns the case record view and to RWB-PLT-N001-CON. SCR-33 Template approval of the legacy story is the template screen of the same module and is not served by this baseline (GAP-1145; ASM-2092). The background-event row AC-BG-P6-021-01 of the FSD A2.21 is the notice dispatch run of A2.20 and is not a retention run, so the baseline serves no run screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-042-01 | AC1 | End to end | Case `RC-2026-000412` closing with `N-0101`/`DOC-0101` and `N-0102`/`DOC-0102`; the contract half answers the coverage answer of AC2, the event of AC3 and the decision of AC6 |
| TC-E4-042-02 | AC2 | End to end | The decision chain is forced to fail; the contract half answers the stopped chain of AC7 |
| TC-E4-042-03 | Access | Component | RW-COMPLY reads the coverage in scope; a role without the Documents right is refused with MSG-P4-002; the contract half answers the 403 of AC1 |
| TC-E4-042-04 | Principle 5 | NFR | The decision log write is forced to fail on 10 closing cases; the contract half answers the stopped chain of AC7 |
| TC-P6-E4042-CON-01 | AC1 | Contract | The document validates; the one operation, its base, its access, its four error responses and the absent Idempotency-Key are present |
| TC-P6-E4042-CON-02 | AC2 | Contract | The coverage entry validates with five elements and a boolean; no class value, no period and no disposal in the answer |
| TC-P6-E4042-CON-03 | AC3 | Contract | The consumed event validates against the registry with its four fields, the closing state and the dedupe rule |
| TC-P6-E4042-CON-04 | AC4 | Contract | The absence test: no retention table, no retention column, no retention event, no workflow and no Schedule |
| TC-P6-E4042-CON-05 | AC5 | Contract | The case fact row carries the reason code and the placeholder, and the fake answers the accepted and the refused case |
| TC-P6-E4042-CON-06 | AC6 | Contract | The decision element carries D9, the two rules, the rule version and the two results |
| TC-P6-E4042-CON-07 | AC7 | Component | The three fakes match the document; a drifted fake fails the build |
| TC-P6-E4042-CON-08 | AC8 | Contract | The nine sub-tables present with owners; no cross-schema read; the call-type summary counts |

The four legacy cases keep their legacy order and their legacy intent as the evidence the contract serves; the eight contract cases test the artefact and are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the closing state, the reason code, the task timer and the retention classes stay data or reference data of their owners.
- The contract declares no retention value: there is no class, no class list, no period and no disposal in the schema, in an example or in a fake.
- No personal data in a schema, an example or a fake: notice IDs, case IDs, document IDs, notice types, codes and dates only.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the class read and the case fact are consumed and faked, never declared as provided (DP-01).
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No retired or foreign element is introduced: the absence test fails a build that declares a retention table, a retention column, a retention event, a Quartz row or a Schedule.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-010 | Every document carries a retention class | The coverage entry and its `classPresent` element, and the class read row of 12.2 | TC-P6-E4042-CON-01, TC-P6-E4042-CON-02, TC-P6-E4042-CON-05 |
| REQ-DCM-019 | Retention runs by class; a disposal or an extension is a recorded decision | The decision element and the statement that the disposal stays rwb-document's | TC-P6-E4042-CON-04, TC-P6-E4042-CON-06 |
| REQ-DCM-016 | A legal hold overrides the retention class | The statement that the hold is rwb-case's and rwb-document's and is not read here | TC-P6-E4042-CON-04 |
| NFR-028 | Retention classes per document type; the periods are not set | The negative declaration of the classes and the periods | TC-P6-E4042-CON-02, TC-P6-E4042-CON-04 |
| NFR-074 | A document at the end of its period is disposed of or extended by a recorded decision | The decision element and the two results it carries | TC-P6-E4042-CON-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-042, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, both owned by RWB-P6-E4042-APP; this baseline copies neither |
| Test cases | The four legacy cases as the evidence the contract serves, and the eight new contract cases TC-P6-E4042-CON-01 to -08 |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-019 (edge: gateway-bff), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The implementation of the coverage check, the listener and the decision path (RWB-P6-E4042-APP).
- The retention class, the class list, the class per document type, the periods and the disposal or extension decision, with their tables `retention_rule` and `retention_action` and the run JOB-17 (P5 rwb-document).
- The case state, the closing state set, the hold of the closure, the Document Hub task and its timer (P3 rwb-case): consumed and faked, never defined here.
- The legal hold of REQ-DCM-016 and R-UNI-20 (rwb-case with rwb-document).
- The central decision ledger and its schema (P7 rwb-decision); this baseline declares only the library element of DP-03.
- The notice generation and dispatch contracts of the same service (RWB-P6-E1052-CON, RWB-P6-E2021-CON): projected, not redefined.
- The case record documents panel, the composite route and the screen field list (RWB-PLT-N001-CON and the story that owns the case record view).
- SCR-33 Template approval and the template capability (RWB-P6-E1034-APP, RWB-P6-AD017-APP).
- The deployment, the dashboards, the alerts and the runbook of this capability: the plan declares no OPS story for this legacy key.
