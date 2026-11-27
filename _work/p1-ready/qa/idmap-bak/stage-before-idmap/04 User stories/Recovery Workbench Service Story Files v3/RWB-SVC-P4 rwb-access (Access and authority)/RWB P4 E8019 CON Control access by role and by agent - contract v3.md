# RWB-P4-E8019-CON Control access by role and by agent

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8019-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Contract version | 1 (path /api/recovery/access/v1; additive within major version 1, BR8) |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E8019-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-019 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the access matrix of `rwb-access`: an OpenAPI 3.1 document for the matrix read, the set of one role's or one agent's letters, the second approval of an agent's change and the report, the `AccessMatrix`, `AccessMatrixChange` and `AccessMatrixReport` schemas over the three role classes with letters, versions and a reason and with no person, the change state set, one RFC 9457 error envelope with its message IDs, the consumed authorise, parameters and group-mapping operations with their owners and the 2 s budget, the contract tables of section 12 and the five contract fakes**, so that **the app story, the SCR-43 route, the `rwb-source-data` team and the integration harness can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, `rwb-source-data` or `rwb-case` to be built**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-019 belong to RWB-P4-E8019-APP, and the six criteria of section 7 test the document, the schemas, the state set, the envelope, the consumed declarations, the event and the fakes.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story set the rights of roles and agents inside a screen of the monolith, where the letters, the rules and the decision log were rows of one schema and no other team had to agree on what a grant meant. In the target the matrix is this service's (Architecture v5 slide 41: P4 owns recovery roles as data and scope) and it is read by the guard of every service, by the gateway-bff, by the agent runtime and by the administration screens, so a grant has to be a published shape before anyone can build against it.

Two things must be fixed once. The first is the boundary: the matrix read, the set, the approval and the report are this service's, and the ACE group mapping is `rwb-source-data`'s, consumed and never claimed. The second is what a change says: the role code, the capability area, the letters before and after, both matrix versions, a reason and a time - and never a person, because a matrix that named its administrators would copy personal data into every event that announces a policy change and into the report that Compliance, Risk and Internal audit read.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the `rwb-source-data` contract, the parameters contract of `rwb-case` and the local decision-record library, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service and its `AccessPolicyChanged` event, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline also states the one thing it is not: it defines no role row, no class of its own and no agent table. An agent is a role of class `NON_HUMAN_ACTOR` in the same schema, and the document says so, which is what keeps one matrix rather than two.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the four operations behind SCR-43 Roles and access, and it is a consumer of this baseline.
- The ownership map puts `role`, `permission`, `role_conflict` and `masking_rule` in P4, `iam_group` and its ACE view in P1, `partner_user` in S9 and `decision_log_entry` in P7; the document names only this service's tables as its own (DP-01).
- The role and permission fields are TSD P4 v3 T3.1 DF-REF-034 to DF-REF-044, the three role classes and the fourteen capability areas are TSD P4 v3 T3.2 LOV-ROLE-CLASS and LOV-CAPABILITY, and the rights of `RW-SECADM`, `RW-AUDIT` and the case roles are the rows of TSD P4 v3 T6.1. The matrix operation itself is not in the appendix T-A, which declares `GET /admin/roles` (API-P4-007) only, so its paths and shapes are fixed here (GAP-0885; ASM-1604).
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The change entry is a decision-record entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the fields this service records and no field of another service.
- No build dependency: this story is Day 1 by rule (Template and Rules R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the four operations with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the paging parameters and the schemas.
2. Fix the `AccessMatrix` and `AccessMatrixRow` schemas: the matrix version in force, one row per role with its code, name, class, default scope and letters per capability area, and the group-mapping block that comes from the `rwb-source-data` answer.
3. Fix the `ChangeRequest` and `AccessMatrixChange` schemas: `capabilityArea`, `letters`, `reason` and `secondApproverRole` in, and `changeId`, the letters before and after, both matrix versions, the state, the time, the approving role code and the reason out - and no person field of any kind.
4. Fix the `AccessMatrixReport` schema and the query parameters of the read, with the page default and maximum held as parameter rows behind the contract and the CSV media type declared.
5. Fix the change state set - `PENDING_APPROVAL`, `APPLIED`, `REFUSED`, `SUPERSEDED` - and state the rule that a change to a `NON_HUMAN_ACTOR` role is applied only after a second person, not the requester, approves it (ASM-1605).
6. Agree the error envelope and the message-ID mapping for 401, 403, 404, 409, 422 and 503, with the business texts taken from the legacy story where the message already existed and MSG-P7-002 carried as a message ID only.
7. Declare the consumed own authorise operation, the `rwb-case` parameters read and the `rwb-source-data` group-mapping read as consumed, each with its owner, one hop and the 2 s client budget; declare that no ACE view, no `iam_group` row, no partner user and no P7 table is named as this service's.
8. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
9. Add the contract tests: schema validation, the three role classes and the letters, the state set and the four-eyes rule, the envelope and message IDs, the consumed declarations, the event schema and drift detection between a fake and the document.
10. Tag the baseline and hand it to RWB-P4-E8019-APP, the SCR-43 route of RWB-PLT-N001-CON, the `rwb-source-data` tech lead and the harness of the wave 4 access journey.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner, or declares the group-mapping read as provided here | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC4 |
| X3 | A response of 401, 403, 404, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC3 |
| X4 | A schema carries a name, an e-mail address, a user reference or another personal field | The contract test fails; the review refuses the document | None | AC2, AC6 |
| X5 | A role class outside `BANK_USER`, `PARTNER_USER` and `NON_HUMAN_ACTOR` is declared, or a letter outside `C`, `R`, `U`, `D`, `A` and the dash | The review refuses the document | None | AC2 |
| X6 | A change state outside the four values is declared, or a change to a `NON_HUMAN_ACTOR` role can be applied without a second approver | The review refuses the document | None | AC3, AC2 |
| X7 | The document declares an ACE view, an `iam_group` row, a partner user table or a P7 table as this service's | The review refuses the document | None | AC4, AC6 |
| X8 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X9 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC4 |
| X10 | The policy event schema carries a personal field, or a change can be published without a stored version | The contract test fails | None | AC5 |
| X11 | A field of an answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |
| X12 | The SCR-43 route asks the report and the matrix holds no row for the filter | The report answers an empty page with total 0 and no 404 (BR12) | None | AC2 |
| X13 | The caller holds no Platform administration R for the read or the report | The read answers 403 with the envelope and MSG-P4-002 | MSG-P4-002 | AC1 |
| X14 | A store or a read cannot be served while SCR-43 loads the matrix | The read answers 503 with the envelope and MSG-P7-003 | MSG-P7-003 | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the T4 fields and lists, the T6.1 rights, the DP-03 entry schema and the P1 and P3 contracts only |
| Negotiable | The page bounds and the second-approval switch are parameter rows behind the document; the base, the paths, the three role classes and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the SCR-43 route, the `rwb-source-data` team and the harness on Day 1, and keeps the person out of a change and out of the report |
| Estimable | One OpenAPI document, one error envelope, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Control access by role and by agent contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the matrix of roles, partner role classes and agents is rwb-access's and the ACE group mapping is rwb-source-data's

  Scenario: AC1 The OpenAPI 3.1 document describes the matrix, the set, the approval and the report (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the access matrix is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares GET /admin/access-matrix, PATCH /admin/access-matrix/{roleCode}, POST /admin/access-matrix/{roleCode}/approve and GET /admin/access-matrix/report with the owner rwb-access
    Then the read and the report name Platform administration R, the set names Platform administration U and the approval names Platform administration A
    Then every operation names its error responses 401, 403, 404, 409, 422 and 503 where it can produce them
    Then the set and the approval require an If-Match header and an Idempotency-Key, and the two reads carry neither
    Then no operation of rwb-source-data, rwb-case or rwb-agent is declared as provided by rwb-access

  Scenario: AC2 The matrix, change and report schemas are fixed over three role classes and carry no person (new, D-RCV-60)
    Given the AccessMatrix, AccessMatrixRow, ChangeRequest, AccessMatrixChange and AccessMatrixReport schemas of the document
    When the contract tests read the five schemas
    Then AccessMatrixRow carries roleCode, roleName, roleClass, defaultScope and the letters of each capability area, and roleClass is one of BANK_USER, PARTNER_USER and NON_HUMAN_ACTOR
    Then the letters of a row are C, R, U, D and A in that order or a dash, and the capability areas are the fourteen of LOV-CAPABILITY
    Then ChangeRequest carries capabilityArea, letters, reason and secondApproverRole, and the set of a NON_HUMAN_ACTOR role declares secondApproverRole as required
    Then AccessMatrixChange carries changeId, roleCode, capabilityArea, lettersBefore, lettersAfter, matrixVersionBefore, matrixVersion, state, changedAt, changedByRole and reason
    Then each change mints the next matrixVersion label in one set and supersedes the version in force, so a change is read against the version it replaced
    Then AccessMatrixReport carries version and items of roleCode, roleClass, capabilityArea, letters, matrixVersion, changedAt, changedByRole and reason, with page, size and total, and declares text/csv
    Then no schema declares a name, an e-mail address, a user reference or a personal field value
    Then page and size are read from the parameters contract and never from code
    Then a schema change is additive within major version 1 and a removed, renamed or retyped field is a new major version
    Then an empty report answers an empty page with total 0 and never a 404

  Scenario: AC3 The change state set and the four-eyes rule are fixed (new, D-RCV-60)
    Given the state set of a change in the document
    When the contract tests read the set and the approval operations of a change
    Then state is one of PENDING_APPROVAL, APPLIED, REFUSED and SUPERSEDED
    Then the document states that a change to a BANK_USER or PARTNER_USER role is answered 200 with state APPLIED, and a change to a NON_HUMAN_ACTOR role is answered 202 with state PENDING_APPROVAL
    Then the document states that only a caller who is not the requester and who holds Platform administration A may approve the change, and that the requester's own approval is 403 with MSG-P7-002
    Then the document states that the approval is idempotent and that a repeat approve of an applied change answers 409 with MSG-GEN-004
    Then no workflow and no Schedule is declared for the capability
    Then a replay of a write answers the same status and body as the first answer and publishes no second event
    Then the approver of a NON_HUMAN_ACTOR change is the role named by its secondApproverRole in the matrix and is never taken from code

  Scenario: AC4 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation, the parameters read and the group-mapping read this service calls
    When the contract tests read each consumed declaration of the document
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then GET /api/recovery/source-data/v1/iam-groups is declared as consumed with the owner P1 rwb-source-data
    Then each carries one hop and the 2 s client budget with a breaker
    Then the document states that rwb-access reads no ACE view and holds no iam_group row, and that the group mapping is answered only by rwb-source-data
    Then no operation owned by rwb-source-data, rwb-case, rwb-agent or rwb-partner is declared as provided by rwb-access

  Scenario: AC5 The policy event is declared with codes and versions and no personal data (new, D-RCV-60)
    Given the event component of the document
    When the contract tests read the event declaration and the outbox write of the stored change
    Then rwb.access.AccessPolicyChanged.v1 is declared on rwb.access.events.v1 with the role code, the role class, the capability area, the letters before and after, the matrix version before and after, the change kind and the effective time
    Then the event carries no name, no e-mail address, no user reference and no personal field value
    Then the event is written from the outbox of the transaction that stores the change, so no event is published for a change that is not stored
    Then rwb.decision.DecisionRecorded.v1 is declared as published through the DP-03 library and DoaLimitChanged is declared as another story's and not published here

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the group-mapping fake answers a role with its mapped group codes, the source system and dataAsOf only, and no person
    Then the authorise fake answers RW-SECADM with CRUDA in Platform administration and RW-CASEOWN with a dash, and no role code is a constant in the document

  Scenario: AC7 The business rules BR1 to BR12 are each met by the document (new, D-RCV-60)
    Given the business rules BR1 to BR12 of section 8
    When the contract tests read the document against each rule
    Then the document declares one REST base /api/recovery/access/v1 and no path of another service (BR1)
    Then each consumed operation is declared as consumed with its owner from the ownership map (BR2)
    Then each error response uses one envelope and one message ID per condition (BR3)
    Then no schema carries an ACE group row, a partner user, a masking profile or a decision ledger row (BR4)
    Then no schema, example, fake or entry carries a name, an e-mail address, a user reference or a personal field value (BR5)
    Then the matrix covers BANK_USER, PARTNER_USER and NON_HUMAN_ACTOR in the same rows and declares no agent grant, agent table or agent identity (BR6)
    Then the change state set is PENDING_APPROVAL, APPLIED, REFUSED and SUPERSEDED, and a NON_HUMAN_ACTOR change is applied only by a second person who is not the requester (BR7)
    Then a schema change is additive within major version 1 (BR8)
    Then a write requires If-Match and Idempotency-Key, and a replay answers the first answer (BR9)
    Then no workflow, no activity and no Schedule is declared for the capability (BR10)
    Then the group mapping is consumed from rwb-source-data with one hop and the 2 s budget, and no ACE view or iam_group row is named as this service's (BR11)
    Then the report is a read with the two media types and answers an empty page rather than a 404 (BR12)
```

These seven criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-019 belong to RWB-P4-E8019-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1, AC7; TC-E8-019-CON-01, TC-E8-019-CON-08 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC4, AC7; TC-E8-019-CON-04, TC-E8-019-CON-08 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are taken from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules R7.2 s14 | AC1, AC7; TC-E8-019-CON-01, TC-E8-019-CON-08 |
| BR4 | The schemas carry the fields of this service and no field of another service: no ACE group row, no partner user, no masking profile and no decision ledger row | DP-01; Ownership Map v1 (`iam_group` = P1, `partner_user` = S9, `decision_log_entry` = P7) | AC2, AC4, AC7; TC-E8-019-CON-02, TC-E8-019-CON-04, TC-E8-019-CON-08 |
| BR5 | The document carries role codes, classes, scopes, letters, versions, times and a reason; no schema, example, fake or entry of this contract carries a name, an e-mail address, a user reference or a personal field value | NFR-040; REQ-ACA-013 | AC2, AC5, AC7; TC-E8-019-CON-02, TC-E8-019-CON-05, TC-E8-019-CON-08 |
| BR6 | One matrix covers the three role classes and an agent is a role of class `NON_HUMAN_ACTOR` with letters in the same rows; the document declares no separate agent grant, no agent table and no agent identity | TSD P4 v3 T3.2 LOV-ROLE-CLASS; TSD P4 v3 T6.1; REQ-ACA-010; ASM-1610 | AC2, AC7; TC-E8-019-CON-02, TC-E8-019-CON-08 |
| BR7 | The change state set is `PENDING_APPROVAL`, `APPLIED`, `REFUSED` and `SUPERSEDED`, and a `NON_HUMAN_ACTOR` change is applied only by a second person who is not the requester | GAP-0886; ASM-1605 | AC3, AC7; TC-E8-019-CON-03, TC-E8-019-CON-08 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC2, AC7; TC-E8-019-CON-02, TC-E8-019-CON-08 |
| BR9 | A write requires `If-Match` on the matrix version and an `Idempotency-Key`; a replay answers the first answer and publishes no second event | Architecture v5 slide 42; DP-09; DP-03 | AC3, AC7; TC-E8-019-CON-03, TC-E8-019-CON-08 |
| BR10 | The contract declares no workflow, no activity and no Schedule for the capability | Architecture v5 slide 14; TSD P4 v3 T5.3 | AC3, AC7; TC-E8-019-CON-03, TC-E8-019-CON-08 |
| BR11 | The group mapping is consumed from `rwb-source-data` with its owner, one hop and the 2 s budget, and no ACE view or `iam_group` row is named as this service's | DP-05; Ownership Map v1; GAP-0889; ASM-1608 | AC4, AC7; TC-E8-019-CON-04, TC-E8-019-CON-08 |
| BR12 | The report is declared with the fields and the two media types; it is a read, it carries no person and it answers an empty page rather than a 404 | REQ-ACA-013; GAP-0887; ASM-1606 | AC2, AC7; TC-E8-019-CON-02, TC-E8-019-CON-08 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The four operations, the schemas, the state set, the consumed operations and the event are described | In review |
| In review | Consumer sign-off | The app story, the SCR-43 route, the `rwb-source-data` tech lead and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, a role class is removed or a state is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A consumed operation changes | The group-mapping read or the parameters read changes | Baselined, with the client budget and the stub restated |

The state set the document fixes for a change is `PENDING_APPROVAL`, `APPLIED`, `REFUSED` and `SUPERSEDED`; the matrix version of one row moves from its label in force to the label a change mints, and the label before keeps an end of validity and stays readable. The lifecycle of a whole matrix file - `LOADED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `REFUSED` - is the matrix-pack capability's and is not declared here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the four operations, the schemas, the state set and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Security administrator, as the primary actor | Reviews the matrix read, the set, the approval and the report as SCR-43 consumes them, and the four-eyes rule of an agent's change |
| Compliance and PDPA officer and Risk and model risk officer | Review the report fields and the absence of a person in the matrix and the report |
| Internal audit | Reviews the report fields, the version history and the stable order of the read |
| Tech lead of rwb-source-data (P1) | Reviews the group-mapping read as `rwb-access` consumes it and owns its definition, its path and its answer |
| Tech lead of rwb-case (P3) | Reviews the parameters read as `rwb-access` uses it; owns its definition |
| Tech lead of rwb-agent (P10) | Confirms that no agent identity, allowed-action list or run record is declared in this document |
| Data steward | Confirms that no name, e-mail address, user reference or personal field is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | Field ID |
|---|---|---|
| `AccessMatrix` | `matrixVersion`, `items[]`, `page`, `size`, `total`, `groupMappingAvailable` | Not specified in the source documents (DOR-RWB-P4-E8019-CON-7) |
| `AccessMatrixRow` | `roleCode` DF-REF-035, `roleName` DF-REF-036, `roleClass` DF-REF-037 (one of `BANK_USER`, `PARTNER_USER`, `NON_HUMAN_ACTOR`), `defaultScope` DF-REF-038 (one of `OWN`, `TEAM`, `REGION`, `ALL`), `letters[]` of `capabilityArea` DF-REF-042 and `letters` DF-REF-043 with `matrixVersion` DF-REF-044, `conflictFlag`, `groupMapping` of `groups[]`, `sourceSystem` and `dataAsOf` | DF-REF-035 to DF-REF-044 |
| `ChangeRequest` | `capabilityArea`, `letters`, `reason`, `secondApproverRole`; `If-Match` on `matrixVersion` and an `Idempotency-Key` in the header | Not specified in the source documents (DOR-RWB-P4-E8019-CON-7) |
| `AccessMatrixChange` | `changeId`, `roleCode`, `capabilityArea`, `lettersBefore`, `lettersAfter`, `matrixVersionBefore`, `matrixVersion`, `state`, `changedAt`, `changedByRole`, `reason`, and the warning field of a break-glass grant | Not specified in the source documents (DOR-RWB-P4-E8019-CON-7) |
| `AccessMatrixReport` | `version`, `items[]` of `roleCode`, `roleClass`, `capabilityArea`, `letters`, `matrixVersion`, `changedAt`, `changedByRole`, `reason`, `page`, `size`, `total`; media type `text/csv` for the CSV form | Not specified in the source documents (DOR-RWB-P4-E8019-CON-7) |
| Group mapping, as consumed | `roleCode` DF-ACE-302, `entra_group` DF-ACE-301, `source_system` DF-ACE-303, `data_as_of` DF-ACE-304, answered by `rwb-source-data` | DF-ACE-301 to DF-ACE-304 |
| Roles and letters | `role` DF-REF-034 to DF-REF-039, `permission` DF-REF-040 to DF-REF-044 and `role_conflict` DF-REF-205 to DF-REF-211, read behind the matrix answer | DF-REF-034 to DF-REF-044 and DF-REF-205 to DF-REF-211 |
| Events | `rwb.access.AccessPolicyChanged.v1` with the change fields of the table above, and `rwb.decision.DecisionRecorded.v1` with the entry of a change, from the DP-03 library | Not specified in the source documents (DOR-RWB-P4-E8019-CON-7) |
| Refusal | `messageId` MSG-P4-001 on a 401, MSG-P4-002 and MSG-P7-002 on a 403, MSG-GEN-001 on a 404 and a 422, MSG-GEN-004 on a 409 and MSG-P7-003 on a 503 | Not specified in the source documents (DOR-RWB-P4-E8019-CON-7) |

The exact request and answer field set of the four operations, the type and length of each field, the shape of the matrix version label a change mints, the report columns and the change state set are Not specified in the source documents (GAP-0885; ASM-1604) and (GAP-0886; ASM-1605) and (GAP-0887; ASM-1606): FSD P4 v3 A2.30 names the journey, two rules and one message, TSD P4 v3 T-A declares `GET /admin/roles` (API-P4-007) and no matrix operation, and the T6.1 matrix gives the rights without an operation. The group-mapping read is Not specified either, because the sources name the ACE view (`v_ace_iam_group`, DF-ACE-301 to DF-ACE-304) and not the P1 operation that would answer it, so the path is fixed here and raised with the P1 owner (GAP-0889; ASM-1608). The four-eyes rule of an agent's change is Not specified in the sources as a right of this capability: TSD P4 v3 T6.3 states it for a rule package version, and it is applied here by the decision of this run (GAP-0886; ASM-1605). The right of the capability is a conflict between the legacy story and the T6.1 matrix (GAP-0888; ASM-1607).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/admin/access-matrix` | `AccessMatrix` out: `matrixVersion`, `items[]` of `roleCode`, `roleName`, `roleClass`, `defaultScope` and the letters of each capability area, the group-mapping block and `groupMappingAvailable`, paged | Platform administration R, scope applied |
| PATCH | `/admin/access-matrix/{roleCode}` | `ChangeRequest` in; `AccessMatrixChange` out in state `APPLIED` with the letters before and after and both versions, or 202 with state `PENDING_APPROVAL` for a `NON_HUMAN_ACTOR` role; `Location` of the report filtered to the role | Platform administration U; `If-Match` on the matrix version and an `Idempotency-Key` required |
| POST | `/admin/access-matrix/{roleCode}/approve` | `AccessMatrixChange` out in state `APPLIED` with the applied `matrixVersion` | Platform administration A, and the approver is not the requester of the change; `If-Match` and an `Idempotency-Key` required |
| GET | `/admin/access-matrix/report` | `AccessMatrixReport` out: one row per role and capability area with its version, time and reason, paged, in JSON or `text/csv` | Platform administration R, scope applied |

Errors for the reads: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 422 a query value of the wrong shape or an unknown class (MSG-GEN-001), 503 the store cannot be read (MSG-P7-003). Errors for the writes: 401 (MSG-P4-001), 403 no right (MSG-P4-002) and an approval by the requester (MSG-P7-002), 404 a `changeId` that names no change (MSG-GEN-001), 409 a stale `If-Match`, a pending change of the same role and area, or a repeat approve (MSG-GEN-004), 422 a required field empty or a letter outside the set (MSG-GEN-001), 503 the change cannot be recorded (MSG-P7-003). Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

The four paths and their shapes are fixed here (GAP-0885; ASM-1604) and confirmed by the contract review before they are frozen. `GET /admin/roles` (API-P4-007) is another story's operation and is not redefined here; the matrix read of this document is the one that covers the role classes and the agents. No operation of `rwb-source-data`, `rwb-case`, `rwb-agent` or `rwb-partner` is declared as provided in this document.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration R, U and A checks behind the four operations, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The report page bounds, the second-approval switch and the parameter version recorded on the entry, with the version in force (DP-06) |
| GET | `/api/recovery/source-data/v1/iam-groups` | P1 rwb-source-data | The ACE group mapping per role: the mapped group codes, the role code, the source system and the date of the data, one hop, cached for a short window (DP-05; GAP-0889; ASM-1608) |

None of the three is declared as provided by rwb-access. The group-mapping read is the one that keeps `v_ace_iam_group` and `iam_group` in P1: the document names the view only as the origin of the field ids and declares that `rwb-access` reads neither the view nor the table and writes no `role.entra_group` value (BR11). The parameters read carries the page bounds and the switch, so neither is a constant in the document.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 rwb-access; consumed by every service that caches the permission data | The change kind, the role code, the role class, the capability area, the letters before and after, the matrix version before and after, the approving role code and the effective time, in the CloudEvents 1.0 envelope, from the outbox of the transaction that stores the change |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a change with the role, the area, the letters before and after, both versions, the reason and the time, with its `prev_hash` and `entry_hash` |

The event name and the topic are those Architecture v5 slide 14 fixes, and slide 43 states that every consumer of the permission data refreshes its cache on `AccessPolicyChanged`; the payload shape is Not specified in the source documents and is fixed here (GAP-0889; ASM-1609). The payload carries codes, letters, versions and times and no personal data by BR5 and NFR-040. `rwb.access.DoALimitChanged.v1` is RWB-P4-E8008-APP's and is declared here as neither published nor consumed.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14, and the four operations of this contract need no subscription. The document declares no inbox and no consumer group, and no ACE, partner, agent or case event is consumed.

#### 12.5 Workflows and activities

None. No workflow, no activity and no signal is part of this contract: a set and an approval are synchronous, the approval step is a right and a state on the change, and the matrix takes effect without a workflow. The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only (BR10).

#### 12.6 Schedules

None. All four operations are request-driven, and the effective time of a change is the time of its record and not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role code, name, class, default scope and stored group answer of a matrix row |
| `permission` | P4 (rwb_access) | The letters of each role and capability area and the matrix version that carries them |
| `role_conflict` | P4 (rwb_access) | The conflict flag of a matrix row |
| `masking_rule` | P4 (rwb_access) | Named only; the profiles are RWB-P4-AD004-APP's and are not part of this document's answers |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The change entry the record event carries and the time and reason the report answers |
| `idempotency_key` | PLT library, created in rwb_access | The stored request and answer of a change or an approval, so one key answers one change (DP-09; ASM-0074) |

No table of another service is named in the contract (DP-01): `v_ace_iam_group` and `iam_group` are ACE's and P1's and arrive in the consumed answer; `partner_user` is S9's; `decision_log_entry` is P7's; `lov_value`, `parameter_catalog` and `parameter_value` are P3's. No ACE view is created, copied or named as this service's, and the document holds no group row and no partner row (BR4, BR11).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| group-mapping fake | `GET /iam-groups` answering group "RWB-SIT-SY-AGENT01" mapped to role "SY-AGENT" with source system `ENTRA_ID` and `dataAsOf` "2026-11-20", a role with two groups, a role with no group and a 503 (GAP-0889; ASM-1608) | App story, contract tests, harness |
| authorise fake | `POST /authorise` with a granted answer for RW-SECADM with `CRUDA` and for RW-AUDIT, RW-COMPLY and RW-RISK with `R` in Platform administration, and a refused answer with MSG-P4-002 for RW-CASEOWN with a dash | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with the page bounds, the second-approval switch and the parameter version at the version in force | App story, contract tests |
| decision-record fake | The append of a change, the hash-link check, a seeded chain of the last changes and a forced failure | App story, contract tests |
| gateway-bff fake | The composite route of SCR-43 with the matrix grid, the change form, the approval panel and the report view | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed | The matrix read, the set, the approval and the report provided; the authorise, parameters and group-mapping operations consumed; one hop, 2 s timeout |
| Kafka | 2 event types published, 0 consumed | `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` and `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, through the outbox and the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output; the CSV form of the report is a media type of the read, and the matrix pack load is another story's |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-access-matrix-v1.yaml` (OpenAPI 3.1) with the four operations and the shared components, `contract/error-envelope.yaml`, the `AccessMatrix`, `AccessMatrixRow`, `ChangeRequest`, `AccessMatrixChange` and `AccessMatrixReport` schemas with their examples, the state-set rule, the four-eyes rule and the versioning rules in the contract README, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. Here the ACE group mapping is consumed from the `rwb-source-data` contract and no view is declared as this service's | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. The group-mapping read adds no dependency, because DP-05 reads the ACE data through the owner's contract and the contract's fake: the `rwb-source-data` operation is consumed and faked, and the path it will have is raised as the key's gap (GAP-0889; ASM-1608).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The four operations with the shapes of section 11: the matrix read and its paging, the set with `If-Match` and `Idempotency-Key`, the approval, and the report with its two media types.
3. The schemas of the three role classes and the letters: `BANK_USER`, `PARTNER_USER` and `NON_HUMAN_ACTOR`, `C`, `R`, `U`, `D`, `A` and the dash, and the fourteen capability areas, as closed sets of the document.
4. The state set of BR7 and the four-eyes rule stated in the document and in the contract README, with the 202 of a pending agent change and the 403 with MSG-P7-002 of the requester's own approval.
5. The consumed operations with their owners, the one-hop rule and the 2 s client budget, and the explicit statement that no ACE view, no `iam_group` row and no partner table is this service's.
6. The error envelope and the message-ID mapping for 401, 403, 404, 409, 422 and 503, with the texts of the legacy messages and MSG-P7-002 as an ID only.
7. The event component of AC5 with the change fields and the no-personal-data rule, and the record event of the DP-03 library.
8. The five fakes and the stub fixtures of section 12.8, including a role of each class and the agent's group mapping.
9. The six contract tests; a drift between a fake and the document fails the build.
10. Baseline tag and the consumer sign-off note from the app story, the SCR-43 route, the `rwb-source-data` tech lead and the harness.

**Feature switch.** All four operations are switched by the service baseline of RWB-P4-E1037-CON and by the `rwb.access.access-matrix` flag of RWB-P4-E8019-APP; the document declares the 403 shape a switched-off set answers and adds no parameter of its own.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8019-APP | The four provided operations, the five schemas, the state set, the four-eyes rule and the five fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-43) | The matrix grid, the change form with its `If-Match`, the approval panel and the report view as they call them |
| The `rwb-source-data` tech lead | The group-mapping read as consumed, its path, its owner and its answer of group codes, source system and data as of, and that no ACE row is claimed here |
| The `rwb-case` tech lead | The parameters read as consumed, with the page bounds and the second-approval switch |
| The harness of the wave 4 access journey | The role code, the class, the letters, the versions, the reason and the times, as the evidence it records |

The shape of the matrix version label, the report columns and the change state set are Not specified in the source documents (GAP-0885; ASM-1604) and (GAP-0887; ASM-1606): they are confirmed with Compliance, Risk, Internal audit and the decision-record library owner before the operations are frozen.

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every declared path, the `rwb-source-data` and `rwb-case` tech leads have accepted the three consumed operations, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without Platform administration R reads, without U sets, or without A approves | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, a role or area is unknown, the letters are outside the set, or a `changeId` names no change | Enter {field}. |
| MSG-GEN-004 | `If-Match` names a version that is not in force, a change is pending for the same role and area, or an approve names a change that is not pending | Someone else changed this record. Reload it to see their change. |
| MSG-P7-002 | The requester of a non-human actor change approves that change | Not specified in the source documents (GAP-0886; ASM-1605) |
| MSG-P7-003 | A store, the record or the outbox cannot be written, or a read cannot be served | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-P7-002 carries a message ID and no text in this baseline, because the four-eyes rule of a non-human actor change is a decision of this run and not a wording of a source (GAP-0886; ASM-1605); the message catalogue supplies the text before the operations are frozen. MSG-P4-003, the legacy scope message, is declared on no response of this document, because a role grant is not a case and this capability scopes no case.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access | Matrix, grid | `AccessMatrix` with one row per role and agent, its class, its scope, its letters per area and its group mapping |
| SCR-43 Roles and access | Matrix, group mapping absent | `AccessMatrix` with `groupMappingAvailable` false and no group block, and no error |
| SCR-43 Roles and access | Change, form | `ChangeRequest` with `capabilityArea`, `letters`, `reason` and `secondApproverRole`, and the `If-Match` of the version read |
| SCR-43 Roles and access | Change, applied | `AccessMatrixChange` in state `APPLIED` with the letters before and after and both versions |
| SCR-43 Roles and access | Change, pending | `AccessMatrixChange` in state `PENDING_APPROVAL` with the approval action |
| SCR-43 Roles and access | Change, stale | The 409 of the envelope with MSG-GEN-004 and a reload action |
| SCR-43 Roles and access | Change, refused | The 403 of the envelope with MSG-P4-002, and with MSG-P7-002 for the requester's own approval |
| SCR-43 Roles and access | Change, break-glass | The warning field of MSG-P4-004 with the end time of the grant |
| SCR-43 Roles and access | Report | `AccessMatrixReport` in JSON, with the version, time and reason of each row, and the CSV media type |
| SCR-43 Roles and access | Report, empty | An empty `items` with total 0 and no error |
| SCR-43 Roles and access | Not recorded | The 503 of the envelope with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |
| SCR-43 Roles and access | Empty | Not specified in the source documents (CG-ALL-5707) |
| SCR-43 Roles and access | Loading | Not specified in the source documents (CG-ALL-5707) |
| SCR-43 Roles and access | Error | Not specified in the source documents (CG-ALL-5707) |
| SCR-43 Roles and access | No access | Not specified in the source documents (CG-ALL-5707) |

The screens are served by the gateway-bff composite route (DP-19), which calls the four operations of this contract, one hop each. The composite route specification and the screen field list belong to RWB-PLT-N001-CON; the masking profile panel is RWB-P4-AD004-APP's, the scope panel is RWB-P4-AD003-APP's and the separation of duty panel is RWB-P4-AD005-APP's and none of the three is part of this document.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-019-CON-01 | AC1 | Contract | The document validates; the base, the four operations, the rights R, U and A, the five error responses, the `If-Match` and the `Idempotency-Key` on the two writes are present; no P1, P3, P10 or S9 operation is provided |
| TC-E8-019-CON-02 | AC2 | Contract | The fields of the five schemas, the three role classes, the letters and the dash, the fourteen capability areas, the required `secondApproverRole` of a non-human actor change, and no name, e-mail address, user reference or personal field |
| TC-E8-019-CON-03 | AC3 | Contract | The four change states, the 200 and 202 branches by role class, the four-eyes rule and its MSG-P7-002, the repeat approve answering 409, and no workflow or Schedule |
| TC-E8-019-CON-04 | AC4 | Contract | Three consumed operations with their owners P4, P3 and P1, one hop and the 2 s budget; no ACE view or `iam_group` row named as this service's |
| TC-E8-019-CON-05 | AC5 | Contract | `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` with the change fields and no personal value; the outbox rule; `DoaLimitChanged` declared as another story's |
| TC-E8-019-CON-06 | AC6 | Component | The five fakes match the document; a drifted fake fails the build; the group-mapping fake answers codes and a date and no person; the authorise fake carries no constant role code |
| TC-E8-019-CON-07 | AC4 | Contract | The six owned tables of section 12.7 with their owner P4; no table of another service named as this service's, including no ACE view, iam_group, partner_user, decision_log_entry, lov_value, parameter_catalog or parameter_value |
| TC-E8-019-CON-08 | AC7 | Contract | The document meets the business rules BR1 to BR12 of section 8: one REST base, consumed operations, one error envelope, no foreign schema field or personal value, the three role classes in one matrix, the change states and the four-eyes rule, additive changes, If-Match and Idempotency-Key, no workflow or Schedule, the group mapping by one hop, and the report as a read |

### 17. Guardrails

- No business value in the contract: the page bounds and the second-approval switch stay parameter rows behind the document, and the role codes, the classes and the letters stay rows and closed sets.
- No personal data in a schema, an example or a fake: role codes, classes, scopes, letters, versions, reasons and times only, and no administrator reference in any answer (BR5).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; `v_ace_iam_group` and `iam_group` are P1's, `partner_user` is S9's and `decision_log_entry` is P7's, and each is consumed or absent, never named as this service's (BR4, BR11).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- One matrix for three classes: the document declares no separate agent grant, no agent table and no agent identity, so a change to an agent is a change to a role (BR6).
- Two people for an agent: the document states that the requester of a non-human actor change cannot approve it, and the schema requires the second approver (BR7).
- The policy event is written from the outbox of the same transaction as the change, so no consumer can be told of a change that is not stored (AC5).
- Every example in the document is synthetic; no production entitlement, group or personal value is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A write without its `If-Match` or its `Idempotency-Key` is refused by the contract, and a replay never makes a second version or a second event (BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release | The set operation, the minted matrix version and the version history the report answers | TC-E8-019-CON-01, TC-E8-019-CON-03 |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do | `AccessMatrix` and `AccessMatrixRow` with the letters of each capability area and the version | TC-E8-019-CON-02, TC-E8-019-CON-04 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people | The `NON_HUMAN_ACTOR` class in the matrix, the 202 and the approval of an agent's change, and no agent identity in this document | TC-E8-019-CON-02, TC-E8-019-CON-03 |
| REQ-CWC-018 | A model or agent writing to a queue passes the same permission checks as a person, runs under a service identity, and its write is logged with the model or agent version | The same letters for an agent and the change entry the record event carries; the run and the model version are P10's | TC-E8-019-CON-03, TC-E8-019-CON-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The four operations as the SCR-43 route consumes them, with the report and the refusal shapes | TC-E8-019-CON-04, TC-E8-019-CON-06 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules R7.3; the Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 control access by role and by agent, with the matrix reported and the result recorded | Sections 4, 7 (AC1, AC2), 11, 12.1, 12.3 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 7, 12.1, 12.3, 14 |
| The permission checks: Rules and parameters C for RW-COE and A for RW-RISK | Sections 3, 7 (AC1), 10, 11; the target right is Platform administration R, U and A (GAP-0888); the Rules and parameters letters belong to the rule-change stories |
| The data rows `role` DF-REF-034 to DF-REF-038, `permission` DF-REF-040 to DF-REF-044, `decision_log_entry` DF-DEC-001 to DF-DEC-018 and `v_ace_iam_group` DF-ACE-301 to DF-ACE-304 | Section 11, section 12.7 |
| The endpoints `/admin/rule-versions` and `/admin/rule-versions/{versionId}/approve` as the story listed them | Section 12.1, replaced by the four matrix operations; the rule-version operations are RWB-P4-E8007-APP's |
| The legacy screens SCR-39 Rules and parameters and SCR-41 Delegation of authority as the story named them | Section 15, carried to SCR-43 Roles and access |
| MSG-P4-004, MSG-P4-002, MSG-P4-001, MSG-GEN-001, MSG-P7-003 | Section 14 |
| Legacy key RWB-E8-019, story RWB-P4-E8019-APP, contract RWB-P4-E8019-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the four operations, the report and the approval (RWB-P4-E8019-APP).
- The matrix pack load, the whole-file validation of a matrix version and its approve path (RWB-P4-AD002-APP and RWB-P4-E1037-APP), and the `GET /admin/roles` operation (API-P4-007) of that capability, which this document does not redefine.
- The masking profiles per role and field (RWB-P4-AD004-APP), the scope per role (RWB-P4-AD003-APP) and the separation of duty pairs (RWB-P4-AD005-APP).
- The ACE group mapping itself, the `iam_group` rows and the ACE views behind them (P1 `rwb-source-data` and the ACE team). This document consumes one operation of that contract.
- Partner users, their identity, firm, cases and portal (S9 `rwb-partner`); only the `PARTNER_USER` role class is declared here.
- The agent runtime, the agent service identity, the allowed-action list and the run records (P10 `rwb-agent`).
- The central decision ledger, the query API over `rwb_decision` and the chain verification (P7 `rwb-decision`).
- The delegation of authority table and its limits (RWB-P4-E1038-APP and RWB-P4-E2013-APP), and the access log, its search and export and break-glass grants (RWB-P4-E1039-APP).
- The screen SCR-43 Roles and access, its other panels and its composite route specification (RWB-PLT-N001-CON).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the authorise operation, the parameters read and the group-mapping read are consumed and faked, never defined here.
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases; no ITG story is split from this legacy key.
