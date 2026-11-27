# RWB-P4-AD012-CON Approve a rule version

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD012-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-AD012-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (base `/api/recovery/access/v1`) |
| Approval gate paths | `/api/recovery/access/v1/admin/rule-version-approvals` (two console operations; the registry approve is consumed and reconciled at contract review) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-012 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P4-AD012-CON-L215, HELD-RWB-P4-AD012-CON-L48). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 18 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the access-side approval gate for a rule version: an OpenAPI 3.1 document for the two console operations, the `RuleVersionApproval`, `ChecklistItem` and `DecisionRecordRef` schemas, the two refusal shapes of a self-approval and an incomplete checklist, the error envelope and the message mapping, the registry, authorise and parameters operations declared as consumed with their owners, the statement that no rule table and no version state are written here, and the contract fakes of section 12**, so that **the app story and the SCR-39 console build the gate on Day 1 against a fixed document while the version and its lifecycle stay `rwb-decision`'s and no operation of the registry is claimed here**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story approved a rule version inside the monolith, where the approver, the approved time and the checklist were columns of one row and the screen was a page of the same module; nothing outside it could say what an approval consisted of. In the target the version, its states and its checklist are the registry's rows in `rwb-decision` (Architecture v5 slides 27 and 41; ASM-0069) and the authority that decides who may approve is `rwb-access`'s data. The two halves meet on a contract, and that contract has to say exactly what the gate accepts, what it answers, what it refuses, which record it writes and what it does not write.

If that field-level contract is agreed once and faked for the registry's approve operation, its version list read, the own authorise operation and the parameters read, the app story builds in parallel with P7, a change in the registry is caught in a contract test rather than in an integration window, and the two refusals that matter most — the author who cannot approve and the checklist that is not complete — have a fixed status, a fixed message id and a fixed body before either side codes them. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The decision-record half is part of the same baseline. R-UNI-39 says an action that cannot be recorded does not proceed, and the legacy key carries that rule as its forced-failure test case; a contract that did not declare the record reference in the approval answer would leave the app story and the console guessing what to show after an approval that is recorded but whose downstream call timed out.

### 3. Preconditions

- The service template and the naming library are available, so the base, the topic and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the RFC 9457 problem response and the `Idempotency-Key` rule on every POST are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the ownership map only. The registry's approve operation and its version list are P7 `rwb-decision`'s under ASM-0040 and ASM-0069, and the two gate operations are `rwb-access`'s; the dependency list of the app story carries no P7 rule-package contract, which is the gap this baseline closes with a fake (GAP-0826; ASM-1527).
- The API Specification v5 declares no `rwb-access` path for this gate, so the two provided paths are this baseline's proposal and are frozen here before either side builds (GAP-0827; ASM-1528).
- The seven checklist items are the ones TSD P4 v3 T6.3 writes — request, impact, test result, approver, load, verify and rollback plan — and the text of MSG-P3-022 is Not specified in the source documents (GAP-0829; ASM-1530).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two console operations of `rwb-access` with the shared components the service uses.
2. Declare the approve operation, its `versionId`, its `Idempotency-Key` and its 200 answer with the `RuleVersionApproval` schema, and the read operation on the same base.
3. Declare `RuleVersionApproval`, `ChecklistItem` and `DecisionRecordRef`, and the effective-dating statement the answer carries.
4. Agree the error envelope and the message mapping: 401, 403, 404, 409, 422 and 503, with one message id per condition, and the three distinct 409 bodies — a self-approval, an incomplete checklist and a version that moved.
5. Declare the consumed operations with their owners, one hop and the 2 s client budget: the registry's approve operation, the registry's version list, the own authorise operation and the `rwb-case` parameters read.
6. State what the service does not write: no `rule_package`, no `rule_package_version`, no `rule_row`, no state of a version and no checklist item; the gate writes one decision-record entry and stores one answer.
7. Publish the contract tables of section 12, nine sub-tables, and the contract fakes.
8. Add the contract tests: schema validation, envelope validation, message mapping, the three 409 shapes, the consumed-operation list, the no-write statement and drift detection between a fake and the document.
9. Tag the baseline and hand it to RWB-P4-AD012-APP, the SCR-39 console and the P7 and P3 owners whose operations it consumes.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request path, query or header fails schema validation | 400 or 422 with the error envelope and the failing pointer | MSG-GEN-001 | AC1, AC3 |
| X2 | A caller without the A letter in Rules and parameters | 403 with the error envelope and the refusal code; the document declares that one refusal entry is written | MSG-P4-002 | AC1, AC3 |
| X3 | The approver is the version's author | 409 with the error envelope and its own code, distinct from the checklist refusal and from the state conflict | MSG-P7-002 | AC1, AC3 |
| X4 | An item of the seven-item checklist is missing | 409 with the error envelope, the missing item codes and the checklist state | MSG-P3-022 | AC3, AC4 |
| X5 | The version is not in `LOADED` | 409 with the error envelope and the state the registry returned | MSG-GEN-004 | AC3 |
| X6 | The decision-record append fails | 503 declared on the approve operation; no registry call | MSG-P7-003 | AC3, AC5 |
| X7 | The registry does not answer inside the 2 s budget | 503 declared on both operations; no version is reported as approved | None | AC1, AC4 |
| X8 | A field of the answer has no source definition | The field is marked with the placeholder and carried as a gap in the app story | None | AC2 |
| X9 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X10 | A document or a fake carries a personal data field | The contract test fails: no name, no e-mail address and no personal field is declared | None | AC6 |

Screen states: the empty, loading, error and no-access states of the console are the app story's (RWB-P4-AD012-APP). Their triggers are Not specified in the source documents (CG-ALL-4760), and the empty and loading states have no message here: Not specified in the source documents (DOR-RWB-P4-AD012-CON-10).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the DP-03 library and the P7, P3 and own-service contracts only |
| Negotiable | The field names of the checklist state and of the record reference, and the screen field list, are settled with the registry owner and the approvers; the operations, the three 409 shapes, the envelope and the no-write statement are fixed |
| Valuable | Unblocks the app story and the SCR-39 console on Day 1 and keeps the version and its lifecycle out of the `rwb-access` document |
| Estimable | One OpenAPI document, one envelope, three refusal shapes, nine contract tables, five fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Access-side rule-version approval contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access-side half of the legacy journey is the approval gate, its record and the version read

  Scenario: AC1 The OpenAPI 3.1 document describes the two console operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/rule-version-approvals and GET /admin/rule-version-approvals/{versionId} with the owner rwb-access
    Then the approve operation declares versionId, the Idempotency-Key header and no body
    Then the approve operation names Rules and parameters A and the read names Rules and parameters R
    Then both operations declare 401 and 403, the approve declares 404, 409, 422 and 503, and the read declares 404 and 503

  Scenario: AC2 The approval answer is declared once (new, D-RCV-60)
    Given the RuleVersionApproval, ChecklistItem and DecisionRecordRef schemas of the document
    When the gate produces the approval answer for an approve request
    Then RuleVersionApproval carries versionId, packageCode, versionLabel, validFrom, checklistState, decisionRecordReference, decisionRecordState, state, approverReference, approvedAt and the effective-dating statement
    Then ChecklistItem carries the seven item codes of the specification with their label, their required flag and their present flag
    Then DecisionRecordRef carries the entry reference, the chain sequence and the outcome
    Then the state property of the answer is one of LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED, read from LOV-VERSION-STATUS
    Then no property of any schema is a name, an e-mail address or a personal field

  Scenario: AC3 Every failure is one envelope with one message and its own 409 (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by a gate operation
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002
    Then 409 carries MSG-P7-002 for a self-approval, MSG-P3-022 with the missing item codes for an incomplete checklist, and MSG-GEN-004 with the registry state for a version that moved
    Then 422 carries MSG-GEN-001 naming the field, and 503 carries MSG-P7-003
    Then the response carries the problem media type and the trace identifier

  Scenario: AC4 The four consumed operations are declared as consumed (new, D-RCV-60)
    Given the registry approve operation, the registry version list, the own authorise operation and the rwb-case parameters read
    When the gate reads the consumed operations
    Then each is declared in the consumed section with its owner P7, P4 or P3, one hop and the 2 s client budget
    Then the approve is declared as POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve with the owner rwb-decision
    Then the version list is declared as GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions with the owner rwb-decision and its change_checklist property
    Then the document declares no operation owned by rwb-decision, rwb-case or the platform as provided by rwb-access

  Scenario: AC5 The document states that no rule table, no version state and no checklist item is written here (new, D-RCV-60)
    Given the contract tables of section 12
    When the gate runs an approval
    Then the document states that no rule_package, rule_package_version, rule_row or rule_test_case table is written by rwb-access and that the registry holds them under ASM-0069
    Then the document states that the gate writes one decision-record entry through the DP-03 library and stores one answer per Idempotency-Key, and nothing else
    Then the document states that the version state change and the checklist are the registry's, and that the answer reports them and changes them not
    Then 12.7 names role, permission, the idempotency and outbox tables and no rule table

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of section 12.8
    When the contract tests run
    Then each fake answers the paths and payloads of 12.2 and 12.8, including the approved answer, the checklist refusal, the self-approval refusal, the state conflict and the two 503s
    Then a contract test fails on any drift between a fake and the document
    Then no schema, example or fake holds a name, an e-mail address or a personal field

  Scenario: AC7 Each business rule of section 8 is tested by a contract case (new, D-RCV-60)
    Given the business rules BR1 to BR11 of section 8
    When the contract tests run
    Then each rule has a case in section 16 that fails the build on a breach
```

These seven criteria test the artefact only. No criterion restates a legacy acceptance criterion; the two legacy criteria of RWB-AD-012 belong to RWB-P4-AD012-APP, and so do the legacy test cases TC-AD-012-01 to TC-AD-012-04.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 14 |
| BR2 | A consumed operation is described as consumed, never as provided, and its owner comes from the ownership map | DP-11; Ownership Map v1; ASM-0040 |
| BR3 | The contract declares no rule table and no version state of `rwb-access`, because the registry is P7's | DP-01; ASM-0069 |
| BR4 | The authority is the A letter in Rules and parameters, read as data and never as a role name, and a missing letter is a declared 403 with MSG-P4-002 | TSD P4 v3 T6.1; REQ-ACA-003 |
| BR5 | A self-approval is its own declared 409 with MSG-P7-002, never a 403 and never a silent accept; the author cannot approve | TSD P4 v3 T6.3; Temporal and Drools Design slide 15 |
| BR6 | An incomplete change checklist is its own declared 409 with MSG-P3-022 and the missing item codes, never a silent accept and never a fallback to the version in force; the wording of MSG-P3-022 is Not specified in the source documents (GAP-0829) | TSD P4 v3 T6.3; REQ-CWC-013 |
| BR7 | The state set of an answer is the LOV-VERSION-STATUS values the registry returns; the document declares no state of its own and never invents one | TSD P4 v3 T3.2 and T4 |
| BR8 | The approval answer names the decision-record entry and its state, because the record is written before the answer and R-UNI-39 forbids an unrecorded approval; the entry carries the package, the version label, the status change LOADED to APPROVED or refused, the valid-from date, the approver reference and the outcome REQUESTED, is written in the local transaction before the registry call, and carries decision code Not specified in the source documents (GAP-0830) | DP-03; R-UNI-39; GAP-0830 |
| BR9 | The checklist catalogue, the capability area, the letters and the decision code are parameter rows, reference values and list values, never a value in the document | DP-06; BR-P4-018; GAP-0828 |
| BR10 | No schema, example or fake carries a personal data field | Principle 5; NFR-040 |
| BR11 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the three schemas, the envelope, the three 409 shapes and the four consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the registry owner, the parameters owner and the console accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake, or a personal field in a schema or an example | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-access` | Owns the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Risk and model risk officer role owner | Confirms that the A letter in Rules and parameters is the only authority for an approval and that the self-approval refusal is the declared 409 |
| Tech lead of `rwb-decision` (P7) | Reviews the two consumed registry operations, the `change_checklist` property and the state set; owns their definitions |
| Tech lead of `rwb-case` (P3) | Reviews the parameters read and its version-in-force rule |
| Console lead and the QA team | Review and sign off the screen states of section 15 and the field list they consume |
| Data steward | Confirms that no personal data field is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| `RuleVersionApproval` | `versionId`, `packageCode`, `versionLabel`, `validFrom`, `checklistState`, `decisionRecordReference`, `decisionRecordState`, `state`, `approverReference`, `approvedAt` and the effective-dating statement; the version fields the registry holds as DF-REF-279, DF-REF-281, DF-REF-286, DF-REF-282, DF-REF-289 and DF-REF-291 | DF-REF-279, DF-REF-281, DF-REF-286, DF-REF-282, DF-REF-289, DF-REF-291 |
| `ChecklistItem` | one entry per item of the seven-item checklist: `itemCode` from the catalogue, `label`, `required` and `present`; the seven item codes are request, impact, test result, approver, load, verify and rollback plan, and the content of the registry's `change_checklist` (DF-REF-295) is read into them | DF-REF-295 |
| `DecisionRecordRef` | `entryId`, `chainSequence`, `outcome` and `writtenAt` of the entry the gate appends through the DP-03 library | Not specified in the source documents (DOR-RWB-P4-AD012-CON-7) |
| Request | the `versionId` of the operation and the `Idempotency-Key` header; no body, no personal field and no caller identity in the payload | Not specified in the source documents (DOR-RWB-P4-AD012-CON-7) |
| Event payloads | the `DecisionRecorded` message of the DP-03 library; no personal field | Not specified in the source documents (DOR-RWB-P4-AD012-CON-7) |

The exact field-level names of the checklist state and of the record reference are this baseline's choice and are carried as the gaps of GAP-0831 and ASM-1532; where a field of the registry's answer has no source definition, the app story carries the placeholder.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/rule-version-approvals` | Path or query `versionId`, no body; answers 200 with `RuleVersionApproval`; `Idempotency-Key` required | Rules and parameters A |
| GET | `/admin/rule-version-approvals/{versionId}` | Answers `RuleVersionApproval` with the checklist state, the local entry reference and the registry's status | Rules and parameters R |

Errors: 401 no session (MSG-P4-001) and 403 no right (MSG-P4-002) on both; the approve adds 404 for a version the registry does not hold, three distinct 409s — MSG-P7-002 for a self-approval, MSG-P3-022 with the missing item codes for an incomplete checklist and MSG-GEN-004 with the registry state for a version that moved — 422 for an empty version id (MSG-GEN-001) and 503 for a record that cannot be written (MSG-P7-003) or a registry that is unavailable; the read adds 404 and 503. The POST carries the `Idempotency-Key` header and the document states that a repeated key answers the first answer; the GET carries none.

The two operations sit under this service's base of DP-13. The registry's approve operation and version list are `rwb-decision`'s under ASM-0040 and are consumed, never provided, here. The API Specification v5 declares no `rwb-access` path for this gate, so these two paths are the baseline's proposal and this document is where they are frozen (GAP-0827; ASM-1528).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve` | P7 `rwb-decision` | Moves the version `LOADED` to `APPROVED` after the registry's own re-checks and answers the moved version |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 `rwb-decision` | The version row with its status, checksum, author, approver, test result and `change_checklist` |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` | The Rules and parameters A or R check behind both provided operations |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The checklist catalogue with the version in force (DP-06) |

None of the four is declared as provided by this document except the authorise operation, which is this service's own and is consumed here by its own guard. The two `rwb-decision` operations are the registry half, and the `change_checklist` property on the version list is the one the gate reads (GAP-0832; ASM-1533).

#### 12.3 Events published

| Event | Topic | Owner | Declared shape |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | the entry of an approval or a refusal: the decision code, the package, the version label, the status change, the valid-from date, the approver reference, the grant id where one is active, and the outcome |

Nothing is declared on `rwb.access.events.v1`. The service's own topic carries `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` (Architecture v5 slide 14), and this gate changes neither an access policy nor a delegation limit.

#### 12.4 Events consumed

None. This contract declares no subscription, and the read answers from the registry on request.

#### 12.5 Workflows and activities

None. No workflow and no activity is declared: the approval is one synchronous command with one downstream call, and the promotion at 00:01 is a Temporal Schedule of `rwb-decision`.

#### 12.6 Schedules

None. An approval is request-driven and the only Schedule of the version lifecycle runs on the registry's queue.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's role and its class behind the A and R letters |
| `permission` | P4 (`rwb_access`) | The letter of the caller's role in Rules and parameters, with its matrix version |
| `idempotency_key`, `outbox_event`, `processed_event` | PLT library, created in `rwb_access` | The stored answer of an approval and the outbox row of the decision-record entry (DP-09) |

No rule table is named in the contract and no table of another service is read (DP-01). `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` stay P7 `rwb-decision`'s under ASM-0069 and appear only as consumed shapes; the checklist is `rule_package_version.change_checklist` (DF-REF-295) and the version state is `status` (DF-REF-282), both reported and neither written here.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision rule-package WireMock | `POST /admin/rule-package-versions/{versionId}/approve` answering version "ENTRY-2027.01" in state `APPROVED` with approvedAt 2026-12-15 and approver reference "U-7103"; a version in `LOADED` with author "U-7101" and all seven checklist items; a version in `LOADED` with six items and no rollback plan; a version in `IN_FORCE`; a 404; a 503 and a timeout; `GET /admin/rule-packages/{packageCode}/versions` answering the same versions with their `change_checklist` | App story, contract tests, console |
| parameters fake | `GET /api/recovery/case/v1/admin/parameters` answering the checklist catalogue of seven items, all required, with the version in force on 15 December 2026 | App story, contract tests |
| decision-record fake | The append of an approval and of a refusal entry, the hash-chain check, the outbox row and a forced failure answering 503 with MSG-P7-003 | App story, contract tests |
| authorise and guard fake | `POST /authorise` granting Rules and parameters A to RW-RISK and refusing RW-COE, RW-CASEOWN, RW-REFADM and RW-AUDIT with MSG-P4-002, and a no-role answer with MSG-P4-001 | App story, contract tests |
| gateway-bff composite route fake | The SCR-39 route calling the read and the approve, one hop each, and merging the version fields with the checklist state and the record reference | Console, app story |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The approve and the read provided; two registry operations, the own authorise operation and the `rwb-case` parameters read consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | The promotion at 00:01 is the registry's |
| File | None | The workbook is the load story's and the registry's; this contract declares no file |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-rule-version-approval-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml` with the message mapping, the `RuleVersionApproval`, `ChecklistItem` and `DecisionRecordRef` schemas, the three refusal shapes, the idempotency and versioning rules in the contract README, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is in this contract's pattern set because the approval answer names the decision-record entry and the document declares the event of the library; DP-05 is here because the approver's group resolves through the service's own `v_ace_iam_group` view and no personal field of it is declared. There is no DP-04: the Drools kit, the compile and the evaluation belong to the registry and the model-owning services, and this contract claims neither.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The two operations with the `versionId`, the `Idempotency-Key` and the answer of the approve.
3. The three schemas and the LOV-VERSION-STATUS values of the answer.
4. The error envelope and the message-id mapping, with the business texts copied from the legacy story and the catalogues where they exist, and the placeholder for the checklist text.
5. The three 409 bodies: the self-approval, the incomplete checklist with its missing item codes, and the state conflict with the registry state.
6. The four consumed operations with their owners, the one-hop rule and the 2 s client budget, with the `change_checklist` property on the registry's version list.
7. The five fakes and the stub fixtures of section 12.8.
8. The eight contract tests: schema, answer shape, envelope, message mapping, the three 409s, consumed list, the no-write statement and drift.
9. Baseline tag and the consumer sign-off note from the app story, the console and the P7 and P3 owners.

**Feature switch.** The document declares no switch: a gate that could be switched off would quietly approve without its checklist, which is the failure the gate exists to prevent, so the refusal path is the control and it is not a flag. The service-level feature flag of the service baseline is outside this contract.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD012-APP | The two provided operations, the three schemas, the three 409 shapes and the five fakes |
| SCR-39 console build | The states of section 15, the version fields, the checklist state and the record reference |
| The P7 rule-package owner of `rwb-decision` | The two consumed operations as `rwb-access` uses them, the `change_checklist` property and the state set; no P7 operation is claimed as provided |
| RWB-P3-E1042-CON (P3 `rwb-case`) | The parameters read, its version-in-force rule and the checklist catalogue key, which is Not specified in the source documents (GAP-0828; ASM-1529) |

**Done when.** The OpenAPI document validates in the pipeline, the eight contract tests pass, the five fakes answer every consumed path, and the app story, the console and the P7 and P3 owners have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session or no role row | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without the A or R letter in Rules and parameters | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | An empty version id or a missing `Idempotency-Key` | Enter {field}. |
| MSG-GEN-004 | The version is not in `LOADED` | Someone else changed this record. Reload it to see their change. |
| MSG-P3-022 | An item of the seven-item checklist is missing | Not specified in the source documents (GAP-0829; ASM-1530) |
| MSG-P7-002 | The approver is the version's author | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The decision-record entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message ids are contract elements; the text is the agreed text taken from the legacy story and the catalogues where it already existed. MSG-P7-002 is the decision centre's separation-of-duty message and is reused word for word, as the legacy key and TSD P4 v3 T6.3 write it. MSG-P3-022 is the checklist message, whose text the sources do not give; the document carries the id and the placeholder, and the body names the missing item codes so the console can show each one from the contract alone.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-39 Rules and parameters | Empty | The read with no version for the package: an empty list and no error |
| SCR-39 Rules and parameters | Loaded, waiting for approval | `RuleVersionApproval` with the version label, the valid-from date, the checksum, the test result and the checklist state |
| SCR-39 Rules and parameters | Checklist incomplete | The 409 with MSG-P3-022 and the missing `ChecklistItem` entries |
| SCR-39 Rules and parameters | Approved | The 200 with `APPROVED`, the approver reference, the approved time, the `DecisionRecordRef` and the effective-dating statement |
| SCR-39 Rules and parameters | Refused | The 409 with MSG-P7-002, MSG-P4-002 or MSG-GEN-004 and the state the registry returned |
| SCR-39 Rules and parameters | Record failed | The 503 with MSG-P7-003 and the statement that nothing was approved |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (CG-ALL-4760) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (CG-ALL-4760) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (CG-ALL-4760) |

The screens are served by the gateway-bff composite route (DP-19), which calls the two gate operations and the registry's version operations in parallel, one hop each, and merges the answers. The composite route specification is the platform's; this document fixes the access side of the merge only, and the version state shown is the registry's, because the transition is the registry's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-012-CON-01 | AC1 | Contract | The OpenAPI 3.1 document validates; the base, the two operations, the `Idempotency-Key`, the two rights, and the error responses 401, 403, 404, 409, 422 and 503 |
| TC-AD-012-CON-02 | AC2 | Contract | `RuleVersionApproval` with its eleven elements, `ChecklistItem` per item of the seven, `DecisionRecordRef` with its four elements, the state set of LOV-VERSION-STATUS, and no personal field |
| TC-AD-012-CON-03 | AC3 | Contract | The envelope with MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-004, MSG-P3-022, MSG-P7-002 and MSG-P7-003; the three distinct 409 bodies |
| TC-AD-012-CON-04 | AC4 | Contract | The four consumed operations with their owner, one hop and the 2 s budget, the `change_checklist` property on the version list, and no P7, P3 or platform operation declared as provided |
| TC-AD-012-CON-05 | AC5 | Contract | The no-rule-table, no-state and no-checklist-write statement, the one record entry and one stored answer, and 12.7 naming no rule table |
| TC-AD-012-CON-06 | AC6 | Contract | The five fakes match the document; a drifted fake, a missing 409 shape and a personal field each fail the build |
| TC-AD-012-CON-07 | AC5 | Contract (boundary) | Each table of 12.7 with its owner; the role and permission letters at the edge of the A and R rights; no rule table and no table of another service read |
| TC-AD-012-CON-08 | AC7 | Contract | BR1 to BR11 of section 8: one breach case per rule; the build fails on each breach |

The legacy test cases TC-AD-012-01 to TC-AD-012-04 are owned by RWB-P4-AD012-APP, which holds the two legacy criteria and the two cases that test them; this contract baseline keeps no copy of them and adds only the contract cases above.

### 17. Guardrails

- No business value in the contract: the checklist catalogue, the capability area, the letters and the decision code stay parameter rows, reference values and list values with versions (BR9). The document names the parameter, never its value as a constant.
- No personal data in a schema, an example or a fake: user references, codes, dates and counts only, and a contract test fails on a personal field (BR10).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the registry tables and the two registry operations are consumed and documented as consumed (DP-01, ASM-0069).
- One REST base per service; a document that names another service's base fails the review (DP-13).
- The version state in every example is a LOV-VERSION-STATUS value the registry returns; the document declares no state of its own and no transition (BR7).
- A self-approval and an incomplete checklist are their own declared 409s with their own message ids, never one generic conflict and never a silent accept (BR5, BR6).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope and the `Idempotency-Key` rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated load to production with a version stamp and no code release | The approve operation, the version read, the `RuleVersionApproval` schema and the consumed registry operations; the stamp is the registry's version label and the gate's record | TC-AD-012-CON-01, TC-AD-012-CON-02, TC-AD-012-CON-04 |
| REQ-DRI-010 | A parameter catalog holds every threshold and limit, versioned | The parameters read with the version in force, the checklist catalogue and the document's refusal to hold a value | TC-AD-012-CON-04, TC-AD-012-CON-05 |
| REQ-ACA-013 | Full administration screens are available, with their rights | The A and R letters on the two operations and the six screen states through the composite route | TC-AD-012-CON-01, TC-AD-012-CON-03, TC-AD-012-CON-07 |

### 19. Out of scope

- The implementation of the gate: the authority read, the checklist gate, the separation-of-duty rule, the record appender, the idempotency store and the registry client (RWB-P4-AD012-APP).
- The registry half: the state change `LOADED` to `APPROVED` and `IN_FORCE`, the promotion at 00:01, the checksum, the compile, the checks, the scenario run, the dry run, the change report and the rollback (P7 `rwb-decision`; ASM-0069).
- The `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` tables, their migrations and the `change_checklist` column; the document reports them and writes none.
- The workbook load and its row gate (RWB-P4-AD011-APP) and the rollback (RWB-P4-AD013-APP).
- The authoring of the change checklist; the document declares how it is read and reported, not how it is filled.
- The deployment, the Helm chart, the topic subscription values, the dashboards and the runbook of this capability.
- The operations of other services beyond the four consumed here; the registry, `rwb-case` and platform contracts are consumed and faked, never defined here.
- The cross-service journey evidence: no ITG story is split from this legacy key, so no `-ITG` copy of a test case is written here.
