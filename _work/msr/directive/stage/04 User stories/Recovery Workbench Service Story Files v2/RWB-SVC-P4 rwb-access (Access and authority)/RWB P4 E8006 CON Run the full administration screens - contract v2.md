# RWB-P4-E8006-CON Run the full administration screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8006-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP07, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | 1 (major version 1 in path /api/recovery/access/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-006 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8006-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 12 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Tribe lead and squad members (RW-TRIBE)**, I want **the published contract baseline of the administration home of `rwb-access`: an OpenAPI 3.1 document for the entitlement read, the `AdminHome` and `AdminHomeArea` schemas, the error envelope with its message IDs, the consumed authorise, parameters and reference-data operations with their owners and their one-hop budget, the declared `rwb.decision.DecisionRecorded.v1` message, the contract tables of section 12 and the five contract fakes**, so that **the app story, the gateway-bff composite route and every panel owner can compose one administration surface on Day 1 without waiting for `rwb-access`, `rwb-case` or the central ledger to be built**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-006 belong to RWB-P4-E8006-APP, and the six criteria of section 7 test the document, the schemas, the declared message, the envelope, the consumed declarations and the fakes.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story drew the whole administration surface in process: one screen read the recovery schema and the two endpoints wrote a reference load and a rule version straight into it. In the target that surface has five owners — roles and permissions in `rwb-access`, queues and parameters in `rwb-case`, templates in `rwb-comms`, panels in `rwb-partner`, autonomy in `rwb-agent` — and one composite route at the edge that may draw none of them unless the caller is entitled (DP-19). Without a fixed entitlement contract every panel owner would invent its own check, and the same administrator would be shown a different surface by each one.

The baseline fixes the one answer all of them consume: one row per capability area in force, with the caller's letters, the default scope, whether the area may be opened, and the matrix, masking and list versions the answer was built under. Fixing it once, with faked consumers, lets the app story build in parallel with the platform library, the parameters and reference-data contracts of `rwb-case` and the panel work of the other services, and it catches a drift between a fake and the document in a contract test rather than in an integration window.

The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`. And it fixes the one thing an auditor asks of the surface: every answer names the versions it was built under and the chain the open was recorded in, so a printed surface can be defended years later.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that consumes this answer and merges it with each owner's panel list, one hop each.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The open entry is a decision-record entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the entry as that library publishes it and adds no field.
- The owners of the consumed operations are taken from the ownership map: the authorise operation is P4 `rwb-access`'s own path, declared as consumed with the fake of RWB-P4-E1037-CON, and the parameters and reference-data operations are P3 `rwb-case`'s under DP-06 and DP-07. The entitlement read itself is not an ownership-map row: no source names it, so this contract fixes it on the DP-13 base of `rwb-access` and the point is carried in GAP-0867 and ASM-1568. `GET /admin/roles` (API-P4-007) and `GET /me/session` (API-P4-012) are other P4 stories' and are neither provided nor consumed here. No table of another service is named (DP-01).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope and the version fields.
2. Fix the `AdminHome` and `AdminHomeArea` schemas: one area row per capability area of the list in force, the letters, the scope, `mayOpen`, and the three versions plus the role class, the chain and the recorded time on the answer.
3. Fix the response of the read as an account of the rows behind it, and state that the areas come from the reference list in force and never from a value in the document.
4. Declare the `rwb.decision.DecisionRecorded.v1` message of the open on `rwb.decision-record.v1` with its key and its payload, and declare no `rwb.access.<Event>.v1` message.
5. Agree the error envelope and the message-ID mapping for 401, 403 and 503, with the business texts copied unchanged from the legacy story where the message already existed.
6. Declare the consumed authorise, parameters and reference-data operations as consumed, each with its owner, one hop and the 2 s client budget.
7. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
8. Add the contract tests: schema validation, the two schemas, the message declaration, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
9. Tag the baseline and hand it to RWB-P4-E8006-APP, the composite route work of RWB-PLT-N001-CON and the wave 4 access journey harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC5 |
| X3 | A response of 401, 403 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | An area row is declared without `mayOpen`, or a version field is missing from the answer | The contract test fails; the surface could not decide a panel | None | AC2 |
| X5 | The document names a capability area, a scope or a role class as a constant value | The review refuses the document; the values are reference lists in force | None | AC2 |
| X6 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X7 | An example, a fake or a schema carries a name, an e-mail address or a personal field | The review and the pipeline refuse the document | None | AC6 |
| X8 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X9 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the DP-03 entry schema and the P3 and P4 contracts only |
| Negotiable | The operation name, the field names and the cache lifetime parameter are settled with the app story and the screen route; the base, the names and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the composite route and the harness on Day 1, and keeps the panel lists and the central ledger out of the `rwb-access` contract |
| Estimable | One OpenAPI document, one declared message, one error envelope, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Administration home contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the administration surface is composed at the edge from this answer and each owner's panel list

  Scenario: AC1 The OpenAPI 3.1 document describes the entitlement read (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the administration home is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares GET /api/recovery/access/v1/admin/home with the owner rwb-access
    Then the operation names its security right, Platform administration R, and its error responses 401, 403 and 503
    Then no operation of another service is declared as provided by rwb-access, and GET /admin/roles, GET /me/session and GET /admin/access-log are absent from the provided set

  Scenario: AC2 The answer and the area row are fixed (new, D-RCV-60)
    Given the AdminHome and AdminHomeArea schemas of the document
    When the answer is built for a caller under the reference lists in force
    Then the answer carries areas, matrixVersion, maskingVersion, listVersion, roleClass, chain and recordedAt
    Then each area row carries capabilityArea, letters, scope and mayOpen
    Then letters is the caller's letter set or a dash and scope is the role's default scope
    Then one row is answered per capability area of the reference list in force, and no area is a constant in the document
    Then the document states that an area the caller does not hold is answered with mayOpen false and is never dropped

  Scenario: AC3 The record message and its entry are fixed (new, D-RCV-60)
    Given the event declaration of the document
    When an open is recorded in the decision-record table
    Then rwb.decision.DecisionRecorded.v1 is declared on the topic rwb.decision-record.v1 with the entry id as its key
    Then the declared entry of an open carries the caller reference, matrixVersion, maskingVersion and the areas answered, and no case id
    Then the entry carries the library's read code from the decision-code set of the local library
    Then no rwb.access.AccessPolicyChanged.v1 and no rwb.access.DoaLimitChanged.v1 is declared by this document

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403 or 503 response is produced by the read
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002 and 503 carries MSG-P7-003
    Then no operation declares a second error shape

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation, the parameters read and the reference-data read this service calls
    When the consumed operations are checked against the ownership map
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters and GET /api/recovery/case/v1/admin/lists/{listCode} are declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then no operation owned by rwb-case, rwb-comms, rwb-partner, rwb-agent or rwb-decision is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then no schema, example or fake carries a name, an e-mail address or a personal field

  Scenario: AC7 The document names only the tables it owns (new, D-RCV-60)
    Given the table list of the contract
    Then the tables named are role, permission, masking_rule and the local decision-record table of the DP-03 library
    Then no table of another service and no central ledger is named

  Scenario: AC8 The cache lifetime is a parameter row read through DP-06 (new, D-RCV-60)
    Given the administration home answer and its cache lifetime
    Then the lifetime is read through DP-06 from a parameter row whose name is Not specified in the source documents (GAP-0867)
    Then no cache lifetime value is a constant in the document or in code

  Scenario: AC9 A schema change stays within major version 1 only when additive (new, D-RCV-60)
    Given the schemas of the document at major version 1
    When a field is removed, renamed or retyped
    Then that change is a new major version and is not made within version 1
    Then any other schema change within version 1 is additive

  Scenario: AC10 The 404 of the provided read is one envelope with one message (new, D-RCV-60)
    Given the provided read of the administration home
    When the read answers 404
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then no operation declares a second error shape for the 404
```

These ten criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-006 belong to RWB-P4-E8006-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1; TC-E8-006-CON-01 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5; TC-E8-006-CON-05 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4; TC-E8-006-CON-04 |
| BR4 | The open entry is the decision-record entry of DP-03: the contract describes it and adds no field | DP-03; RWB-PLT-E1027-CON | AC3; TC-E8-006-CON-03 |
| BR5 | The contract declares no table of another service and no central ledger; the panel lists are the owners' and `decision_log_entry` is P7's | DP-01; ASM-A6-tables | AC7; TC-E8-006-CON-07 |
| BR6 | The capability areas, the scopes and the role classes are reference lists in force; the document declares the fields and no value of them | DP-07; TSD P4 v3 T3.2 | AC2; TC-E8-006-CON-02 |
| BR7 | The cache lifetime of the answer is a parameter row behind the contract, never a constant in code | DP-06; BR-P4-017 | AC8; TC-E8-006-CON-08 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC9; TC-E8-006-CON-09 |
| BR9 | No personal data in a schema, an example or a fake: references, codes, versions and times only | NFR-040 | AC6; TC-E8-006-CON-06 |
| BR10 | Every answer states the versions it was built under and the chain the open was recorded in, so a printed answer is defensible | FSD P4 v3 A2.17.4.1; ASM-1570 | AC2; TC-E8-006-CON-02 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The read, the two schemas, the message declaration, the envelope and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the composite route and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A reference list changes | A new area, scope or role class is in force | Baselined, with no document change |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the two schemas, the envelope and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Security administrator | Reviews the entitlement fields, the right of the read and the refusal mapping with MSG-P4-002 |
| Tech lead of rwb-case (P3) | Reviews the parameters and reference-data operations as rwb-access uses them; owns their definitions |
| Owner of the gateway-bff contract | Reviews the answer as the composite route consumes it, and confirms that no panel list is declared by this service |
| Data steward | Confirms that no personal data field is declared in the answer, the examples or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Administration home | `areas[]` of the area row, `matrixVersion`, `maskingVersion`, `listVersion`, `roleClass`, `chain`, `recordedAt` | BR10 |
| Area row | `capabilityArea` (a value of LOV-CAPABILITY in force), `letters` (C, R, U, D, A or a dash), `scope` (a value of LOV-SCOPE), `mayOpen` (boolean) | BR6 |
| Versions | `matrixVersion` from `permission.matrix_version` (DF-REF-044), `maskingVersion` from `masking_rule.masking_version` (DF-REF-202), `listVersion` from the reference version in force of the areas, scopes and role classes | BR10 |
| Role class | A value of LOV-ROLE-CLASS from `role.role_class` (DF-REF-037) | BR6 |
| Open entry | The decision-record entry of DF-DEC-001 to DF-DEC-018: `decision_code` DF-DEC-003 with the library's read code, `case_id` DF-DEC-002 empty, `inputs_ref` DF-DEC-008 with the caller reference, the matrix version, the masking version and the areas answered, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | BR4 |
| Refusal | `messageId` MSG-P4-001, MSG-P4-002 or MSG-P7-003 with the detail text and the instance | BR3 |

The operation path is GET /api/recovery/access/v1/admin/home (AC1); the operation name and the field names of the answer are Not specified in the source documents (GAP-0867; AC2) and are fixed by this contract before the endpoint is frozen; the cache lifetime is read through DP-06 from a parameter row whose name is Not specified in the source documents (GAP-0867; AC8). The meaning of `mayOpen` for a read-only area is Not specified in the source documents (GAP-0867; ASM-1568) and is fixed by this contract before the endpoint is frozen. The record code of an open is the library's read code, which the library publishes and not this document (ASM-1570).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/admin/home` | AdminHome: `areas[]` of the area row of section 11, plus `matrixVersion`, `maskingVersion`, `listVersion`, `roleClass`, `chain` and `recordedAt`; no query parameter | Platform administration R, scope applied |

The full path of the provided operation is `/api/recovery/access/v1/admin/home`, on the base of DP-13. Errors: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002) and 503 the entry of the open cannot be written or a version the answer needs is missing (MSG-P7-003). The read carries no Idempotency-Key and the document states it so that no consumer sends the header. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

The provided set of this document is one operation. `GET /admin/roles` is API-P4-007 of RWB-P4-E1019-APP, `GET /me/session` is API-P4-012 and `GET /admin/access-log` is API-P4-008 of RWB-P4-AD007-APP; none of them appears as provided here, and the legacy `POST /admin/reference-loads` and the rule-version paths are not declared at all because they are `rwb-case`'s and `rwb-decision`'s.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration R check behind the read, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The cache lifetime of the answer, with the version in force (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS with the version in force (DP-07) |

None of the three is declared as provided by rwb-access, and no operation of `rwb-comms`, `rwb-partner`, `rwb-agent` or `rwb-decision` appears in the document at all: the panel lists are the composite route's, and the central ledger is P7's.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of an open with the caller reference, `matrixVersion`, `maskingVersion`, the areas answered and no case id, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

This document declares the record message only. `rwb.access.AccessPolicyChanged.v1` belongs to RWB-P4-E1037-APP and `rwb.access.DoaLimitChanged.v1` to RWB-P4-E1038-APP; neither is declared here, and this service publishes no other event of the administration surface.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and an entitlement answer needs no subscription.

#### 12.5 Workflows and activities

None. No workflow and no activity is part of this contract, and the `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only.

#### 12.6 Schedules

None. The open of the surface is request-driven.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role class and the default scope the answer carries |
| `permission` | P4 (rwb_access) | The letters of each capability area and the matrix version |
| `masking_rule` | P4 (rwb_access) | The masking version in force for the caller's role |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The entry the document describes and the read appends |

No table of another service is named in the contract (DP-01): `lov_value`, `reference_version` and `reference_row` are P3 reference data read through DP-07, `queue` is P3's, `template` is P6's, `rule_package` and `rule_row` are P7's, `partner_user` is S9's and `decision_log_entry` is P7 rwb_decision's.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| authorise fake | `POST /authorise` with a granted answer for RW-PLATADM, RW-SECADM, RW-COE, RW-DATASTEW, RW-AUDIT and RW-COMPLY with Platform administration R, and a refused answer with MSG-P4-002 for RW-PHONECOL | App story, contract tests, harness |
| decision-record fake | The append of an open entry with its `prev_hash` and `entry_hash`, the hash-link check and a forced failure | App story, contract tests |
| parameters fake | `GET /admin/parameters` with the cache lifetime of the answer as a row and the version in force | App story, contract tests |
| reference-data fake | `GET /admin/lists/{listCode}` for LOV-CAPABILITY with its 14 areas, LOV-SCOPE and LOV-ROLE-CLASS at version REF-2026.11 | App story, contract tests, harness |
| gateway-bff fake | The composite route of the administration surface: the entitlement panel of this answer and the panel lists of P3, P6, S9 and P10, merged one hop each | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | The entitlement read provided; the authorise, parameters and reference-data reads consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | 0 | No file input and no file answer |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-adminhome-v1.yaml` (OpenAPI 3.1) with the read and the shared components, `contract/error-envelope.yaml`, the `AdminHome` and `AdminHomeArea` schemas with their examples, the AsyncAPI fragment that declares `rwb.decision.DecisionRecorded.v1` for this read, the versioning rules, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The read with the shape of section 11; the answer and the area row, the four row fields and the six answer fields.
3. The statement of the area source: one row per area of the reference list in force, the version of the list on the answer, and no area as a value in the document.
4. The message declaration of `rwb.decision.DecisionRecorded.v1` with its key, its payload and the read code of the entry.
5. The consumed operations with their owners, the one-hop rule and the 2 s client budget.
6. The error envelope and the message-ID mapping, with the business texts copied unchanged from the legacy story.
7. The five fakes and the stub fixtures of section 12.8.
8. The six contract tests; a drift between a fake and the document fails the build.
9. Baseline tag and the consumer sign-off note from the app story, the screen route and the harness.

**Feature switch.** The read is switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; the document declares no 404 branch of its own and adds no parameter.

**Publisher sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8006-APP | The provided read, the two schemas, the message declaration and the five fakes |
| RWB-PLT-N001-CON (gateway-bff and the SCR-43 route) | The answer as the entitlement panel consumes it, and the statement that the panel lists are not this service's |
| The integration harness of the wave 4 access journey | The area fields, the three versions, the open entry and the fakes, as the evidence it records |

The cache lifetime of the answer is a parameter row behind the document and its name is Not specified in the source documents (GAP-0867; ASM-1569); the deprecation window of a published field is the versioning rule of BR8.

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every declared path, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without Platform administration R reads the operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of the answer has no value in the rows in force | Enter {field}. |
| MSG-P7-003 | The entry of the open cannot be written, or a version the answer needs is missing | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story RWB-E8-006 where the message already existed, and from the FSD for MSG-GEN-001. The document declares the 401, the 403 and the 503 of this read and no other error shape.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| Administration surface | Home, entitled | The answer with one card per area of `mayOpen` true, and the three versions, the role class, the chain and the recorded time |
| Administration surface | Home, not entitled | The same answer with `mayOpen` false on the areas the caller does not hold; the row is always present |
| Administration surface | Home, versions | `matrixVersion`, `maskingVersion`, `listVersion`, `recordedAt` and `chain` on the answer |
| SCR-39 Rules and parameters, SCR-42 Queues and service levels, SCR-43 Roles and access, SCR-47 Personal data | Panel of an entitled area | The owner's panel, reached from the card; the panel list and its content are not part of this document |
| SCR-39 Rules and parameters, SCR-42 Queues and service levels, SCR-43 Roles and access, SCR-47 Personal data | Empty | Not specified in the source documents (DOR-RWB-P4-E8006-CON-10; CG-ALL-5443) |
| SCR-39 Rules and parameters, SCR-42 Queues and service levels, SCR-43 Roles and access, SCR-47 Personal data | Loading | Not specified in the source documents (DOR-RWB-P4-E8006-CON-10; CG-ALL-5443) |
| SCR-39 Rules and parameters, SCR-42 Queues and service levels, SCR-43 Roles and access, SCR-47 Personal data | Error | Not specified in the source documents (DOR-RWB-P4-E8006-CON-10; CG-ALL-5443) |
| SCR-39 Rules and parameters, SCR-42 Queues and service levels, SCR-43 Roles and access, SCR-47 Personal data | No access | Not specified in the source documents (DOR-RWB-P4-E8006-CON-10; CG-ALL-5443) |
| Administration surface | Home, refused | The 403 of the envelope with MSG-P4-002 and no card |
| Administration surface | Home, not recorded | The 503 of the envelope with MSG-P7-003 and no card |
| Administration surface | Break-glass warning | The warning of the session read, shown as the MSG-P4-004 banner over the cards |

The screens are served by the gateway-bff composite route (DP-19), which calls this read and each owner's panel list in parallel, one hop each, and merges the answers. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work; the document fixes the entitlement side of the merge only, and `mayOpen` is what the route renders with.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-006-CON-01 | AC1 | Contract | The document validates; the base, the provided read, Platform administration R and the three error responses are present; no foreign operation is provided |
| TC-E8-006-CON-02 | AC2 | Contract | The answer and the area row fields, one row per area of the list in force, and no area, scope or class as a value in the document |
| TC-E8-006-CON-03 | AC3 | Contract | The record message on `rwb.decision-record.v1` with its key and payload, the read code of the entry, no case id, and no `rwb.access.<Event>.v1` declared |
| TC-E8-006-CON-04 | AC4 | Contract | A 401, 403 and 503 response carry one problem envelope with a valid message ID |
| TC-E8-006-CON-05 | AC5 | Contract | Three consumed operations with their owners P4 and P3, one hop and the 2 s budget; none declared as provided |
| TC-E8-006-CON-06 | AC6 | Component | The five fakes match the document; a drifted fake fails the build; no name, e-mail address or personal field |
| TC-E8-006-CON-07 | AC7 | Contract | The document names only the owned tables role, permission, masking_rule and the local decision-record table; no foreign table or central ledger |
| TC-E8-006-CON-08 | AC8 | Contract | The cache lifetime is read through DP-06 from a parameter row whose name is Not specified in the source documents (GAP-0867); no cache lifetime value is declared in the document or code |
| TC-E8-006-CON-09 | AC9 | Contract | An additive schema change stays within major version 1; a removed, renamed or retyped field is a new major version |
| TC-E8-006-CON-10 | AC10 | Contract | The 404 of the provided read is one problem envelope with a valid message ID; no second error shape |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The ten rows test the artefact and are the contract story's own; the four legacy rows of RWB-E8-006 stay with RWB-P4-E8006-APP. No `-ITG` id appears in this table.

### 17. Guardrails

- No business value in the contract: the capability areas, the scopes and the role classes are reference lists in force, and the cache lifetime is a parameter row behind the document.
- No personal data in a schema, an example or a fake: references, codes, versions and times only (BR9).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the panel lists, the case, the template, the rule registry, the partner user and the ledger are consumed or absent, never named as this service's (DP-01, BR5).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The document declares one provided operation and no panel list, so no consumer can read an entitlement the service did not answer (BR5, BR6).
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release | The area row built from the rows in force, the role class and the versions on the answer | TC-E8-006-CON-02, TC-E8-006-CON-05 |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do | `letters`, `mayOpen` and `matrixVersion` on the answer, and the 403 with MSG-P4-002 | TC-E8-006-CON-02, TC-E8-006-CON-04 |
| REQ-CWC-006 | Roles, teams, queues and capacity are held as versioned reference data and change without a code release | `listVersion` on the answer and the statement that no area is a value in the document | TC-E8-006-CON-02 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The read as the composite route consumes it, and the room the answer leaves for the panel lists in force | TC-E8-006-CON-01, TC-E8-006-CON-05 |

The requirement IDs are the four rows this story serves; each is taken from the FSD "Requirements served" table and the Program BRD under the fill order of Template and Rules §R7.3, because the Work Package carries no requirement list for this story.

### 19. Out of scope

- The implementation of the entitlement read (RWB-P4-E8006-APP).
- The role administration, the permission matrix and the masking rules as data (RWB-P4-E1037-APP), and the access event writer and the break-glass grant (RWB-P4-E1039-APP); this document consumes their shapes.
- `GET /admin/roles` (RWB-P4-E1019-APP), `GET /me/session` and `GET /admin/access-log` (RWB-P4-AD007-APP); none is defined here.
- The reference-load and rule-version operations of the legacy story: `rwb-case` (P3) and `rwb-decision` (P7).
- The central ledger, the query API over `rwb_decision` and the chain verification (P7 rwb-decision).
- The panel lists of `rwb-case`, `rwb-comms`, `rwb-partner` and `rwb-agent`, and the composite route specification and screen field list of the administration surface (RWB-PLT-N001-CON and the Epic 8 screen work).
- The access review list and its Schedule (RWB-P4-AD008-APP).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the `rwb-case` parameters and reference-data contracts and the authorise operation are consumed and faked, never defined here.
- The cross-service journey harness and its evidence.
