# RWB-P4-E8017-CON Manage an incident

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8017-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Contract version | Major version 1 in the path `/api/recovery/access/v1`; document version Not specified in the source documents (DOR-RWB-P4-E8017-CON-23) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-017 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 8 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the published contract baseline of the incident record of `rwb-access`: an OpenAPI 3.1 document for the three operations, the `Incident`, `IncidentStep` and `HeldArea` schemas, the five-step set and the two-state set, one RFC 9457 error envelope with its message IDs, the consumed authorise and parameters reads with their owners, one hop and the 2 s budget, the contract tables of section 12 and the contract fakes**, so that **the app story, the incident surface of the gateway-bff route and Internal audit can build against a fixed, testable contract on Day 1 without waiting for `rwb-access` or `rwb-case`, and no party invents its own step names, its own state names or its own hold`**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-017 belong to RWB-P4-E8017-APP, and the six criteria of section 7 test the document, the schemas, the closed sets, the envelope, the consumed declarations and the fakes.

The baseline is the incident record only. The rule-version paths the legacy story names are the registry's, the break-glass grant and the access-log search are RWB-P4-E1039-APP's, and the enforcement of a hold is the guard's of RWB-P4-E1037-APP; none of them appears here as provided.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy key answered the incident path inside one administration screen against the monolith's own rule tables, so the names of the steps, the meaning of a hold and the point at which an incident is closed were decided by whichever screen asked. In the target the incident is a record of the service that holds the access policy, and three parties read it: the surface that shows it, the administrator who takes the hold, and Internal audit, who reads it months later as the evidence that an incident happened at all.

Fix that contract once, with fakes, and the app story builds in parallel with the record library and with the parameters contract of `rwb-case`, and a drift between a fake and the document is caught in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

Two things the baseline fixes are what audit asks for. First, the five steps are a closed set named from the legacy criterion itself, so no surface can claim a sixth step. Second, a hold states its areas, its rights and its scope, and states that it changes no value in force, so a reviewer can tell a hold from a policy change without opening a second document.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the three operations and is a consumer of this baseline.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- A step is an entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the entry as that library publishes it and adds no field to the library's own schema.
- The parameters version arrives through the `rwb-case` contract (P3, DP-06); this document declares that read as consumed and names no parameter row as this service's.
- The operations and their owners are taken from the ownership map only: the three incident operations are P4's, the authorise operation this document consumes is P4's, and the parameters read is P3's.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the three operations with the shared components used across the `rwb-access` administration operations: the security scheme, the problem envelope, the identifier parameters and the incident schema.
2. Fix the `Incident` schema, the `IncidentStep` schema and the `HeldArea` schema, with the held-area list, the rights list and the scope as closed enums.
3. Fix the five step names of the legacy criterion as the closed set of `step`, and the two states `OPEN` and `CLOSED` as the closed set of `state`, with the rule that the first two steps come from the open and the last three from the closure.
4. Agree the error envelope and the message-ID mapping for 401, 403, 404, 409, 422 and 503, with the business texts copied unchanged from the legacy message table of RWB-E8-017 where the message already existed.
5. Declare the consumed operations as consumed, each with its owner, one hop and the 2 s client budget: the own authorise operation and the `rwb-case` parameters read.
6. Publish the contract tables of section 12 (nine sub-tables) and the four contract fakes.
7. Add the contract tests: schema validation, the incident and step shapes, the closed sets, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
8. Tag the baseline and hand it to RWB-P4-E8017-APP, the incident surface of RWB-PLT-N001-CON and Internal audit as the reader of the record.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC5 |
| X3 | A response of 401, 403, 404, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A step outside the five, or a state outside the two, is declared | The contract test fails; both sets are closed | None | AC3 |
| X5 | A held area, a right or a scope is declared as a free string | The contract test fails; the three lists are closed enums of the technical specification | None | AC2 |
| X6 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X7 | An example, a fake or a schema carries a name, an e-mail address or a personal field | The review and the pipeline refuse the document | None | AC6 |
| X8 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X9 | A field of the answer has no source definition | The field is carried with the placeholder and the gap is recorded | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the DP-03 entry schema and the `rwb-case` parameters contract only |
| Negotiable | The record code of a step and the field-level shape of a step inside the entry are settled with audit and with the library owner; the operations, the five steps, the two states and the three lists are fixed |
| Valuable | Unblocks the app story, the incident surface and the audit reader on Day 1, and keeps the registry, the guard and the break-glass work out of the `rwb-access` incident contract |
| Estimable | One OpenAPI document, one error envelope, three schemas, two closed sets, nine contract tables, four fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Incident record contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the incident half of the legacy journey is the record that names the areas and rights held, the fix and the report of one incident

  Scenario: AC1 The OpenAPI 3.1 document describes the three operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the incident record is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/incidents, POST /admin/incidents/{incidentId}/closure and GET /admin/incidents/{incidentId} with the owner rwb-access
    Then the open names Platform administration C, the closure Platform administration U and the read Platform administration R, and each names its error responses: 401, 403, 409, 422 and 503 on the open, 401, 403, 404, 409, 422 and 503 on the closure, and 401, 403, 404 and 503 on the read
    Then no operation of another service is declared as provided by rwb-access

  Scenario: AC2 The incident, the step and the held area are fixed (new, D-RCV-60)
    Given the Incident, IncidentStep and HeldArea schemas of the document
    When the Incident, IncidentStep and HeldArea schemas are checked against the field lists below
    Then Incident carries incidentId, incidentReference, state, detectedAt, heldFrom, heldTo, heldAreas, reason, parametersVersion, steps, fixReference, reportReference, resolvedAt, actorReference and recordedAt
    Then IncidentStep carries step, entryId, recordedAt and parametersVersion
    Then HeldArea carries capabilityArea, rights and scope, all three required, with capabilityArea enumed to the fourteen values of LOV-CAPABILITY, rights to C, R, U, D and A, and scope to OWN, TEAM, REGION and ALL
    Then incidentReference, detectedAt, at least one held area and reason are required on the open, and resolvedAt, fixReference, reportReference and reason on the closure
    Then no field of the incident carries a name, an e-mail address or a personal field

  Scenario: AC3 The five steps and the two states are closed sets (new, D-RCV-60)
    Given the step and state properties of the document
    When the step and state enums are checked against the closed lists below
    Then the step values are exactly DETECTED, HELD, FIXED, RECORDED and REPORTED
    Then the open answers DETECTED and HELD and the closure answers FIXED, RECORDED and REPORTED
    Then the state values are exactly OPEN and CLOSED
    Then the read declares the five steps in path order and the state derived from them
    Then no sixth step and no third state is declared anywhere in the document

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by the operation that declares it
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002 and the 404 of a record outside the caller's areas carries MSG-P4-003
    Then 409 carries MSG-GEN-004, 422 carries MSG-GEN-001, and 503 carries MSG-P7-003
    Then the 422 declares the field path of the refused entry
    Then no operation declares a second error shape

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation and the parameters read this service calls
    When the consumed and provided operations of the document are checked against the ownership map
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then no operation owned by rwb-case, rwb-decision or rwb-comms is declared as provided by rwb-access
    Then no table of another service is named as this service's and no incident table is named at all

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the four contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the decision-record fake answers the two entries of one incident and a forced write failure, and the read returns the five steps
    Then no schema, example or fake carries a name, an e-mail address or a personal field

  Scenario: AC7 The document changes only additively within major version 1 (new, D-RCV-60)
    Given the baseline of major version 1 is tagged
    When the document is compared with that baseline
    Then no field, operation, step, state or enum value is removed, renamed or retyped
    Then any such change is declared as a new major version

  Scenario: AC8 Every business rule of section 8 is covered by a criterion and a test case (new, D-RCV-60)
    Given the business rules table of section 8
    When each rule is traced to the criteria and test cases of this story
    Then each of BR1 to BR12 names at least one criterion and one test case that exist in this story
    Then a rule that is an architecture constraint is tested by a guardrail test

  Scenario: AC9 A replayed write with the same idempotency key is answered once (new, D-RCV-60)
    Given a write of POST /admin/incidents or POST /admin/incidents/{incidentId}/closure has been answered for an idempotency key
    When the same write is sent again with the same idempotency key
    Then the repeated request is answered with the answer of the first write
    Then no second entry is written for it
```

These nine criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-017 belong to RWB-P4-E8017-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1; TC-E8-017-CON-01 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5; TC-E8-017-CON-05 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy message table where the message exists | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4; TC-E8-017-CON-04 |
| BR4 | A step is an entry of the DP-03 library: the contract describes the fields it carries and adds no field to the library's schema | DP-03; RWB-PLT-E1027-CON | AC2; TC-E8-017-CON-02 |
| BR5 | The contract declares no table of another service and no central ledger, and names no incident table, because the record is the chain and no schema holds an incident | DP-01; ASM-1594 | AC5; TC-E8-017-CON-05, TC-E8-017-CON-07 |
| BR6 | The five step names are the five words of the legacy criterion and are a closed set; a missing step cannot be declared by a consumer | Legacy RWB-E8-017 AC1; Template and Rules §R7.2 s7 | AC3; TC-E8-017-CON-03 |
| BR7 | The two states are `OPEN` and `CLOSED`, a closed incident is never re-opened, and a second closure is a 409 | ASM-1594; FSD P4 v3 AC-EXC-P4-007-05 for the duplicate rule | AC3, AC4; TC-E8-017-CON-03, TC-E8-017-CON-04 |
| BR8 | The held areas, the rights and the scopes are the closed lists of TSD P4 v3 T3.2 and the letters of `permission.letters`; a free string is refused by the schema | TSD P4 v3 T3.1 and T3.2 | AC2; TC-E8-017-CON-02 |
| BR9 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC7; TC-E8-017-CON-08 |
| BR10 | No personal data in a schema, an example or a fake: references, codes, versions, dates, times, rights and scopes only | NFR-040; FSD P4 v3 A2.28.3.2 | AC2, AC6; TC-E8-017-CON-02, TC-E8-017-CON-06 |
| BR11 | The contract states the right of each operation as the one TSD P4 v3 T6.1 gives it  -  Platform administration C, U and R  -  and names no Rules and parameters letter | TSD P4 v3 T6.1; GAP-0879; ASM-1595 | AC1; TC-E8-017-CON-01 |
| BR12 | The identifier a consumer quotes is the incident id, and the incident id is opaque to every consumer but this service | ASM-1594; ASM-1596 | AC2; TC-E8-017-CON-02 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the three schemas, the two closed sets, the envelope and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the incident surface and the audit reader accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | A step or a state changes in the sources | The closed set changes and the change is reviewed with the audit reader | In review |
| Baselined | Drift in a fake | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the three schemas, the two closed sets, the envelope and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Internal audit representative | Reviews and signs off the five steps, the two states and the fields that make a hold defensible after the fact |
| Tech lead of rwb-case (P3) | Reviews the parameters read as rwb-access uses it; owns its definition |
| Platform owner of the authorise contract and the security administrator | Review the rights of the three operations and the refusal mapping with MSG-P4-002 and MSG-P4-003 |
| Data steward | Confirms that no personal data field is declared in the incident, the steps, the examples or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Incident | `incidentId`, `incidentReference`, `state`, `detectedAt`, `heldFrom`, `heldTo`, `heldAreas`, `reason`, `parametersVersion`, `steps`, `fixReference`, `reportReference`, `resolvedAt`, `actorReference`, `recordedAt` | BR5, BR7, BR12 |
| Step | `step`, `entryId`, `recordedAt`, `parametersVersion`; the step values are `DETECTED`, `HELD`, `FIXED`, `RECORDED` and `REPORTED`, from the five words of RWB-E8-017 AC1 | BR4, BR6 |
| Held area | `capabilityArea` from the fourteen values of LOV-CAPABILITY, `rights` from C, R, U, D and A (DF-REF-043), `scope` from LOV-SCOPE (OWN, TEAM, REGION, ALL) | BR8 |
| Refusal | `messageId` MSG-P4-002, MSG-P4-003, MSG-GEN-001 or MSG-GEN-004, with the field path on a validation refusal, and MSG-P7-003 on a record or parameters failure | BR3, BR10 |

The record code a step is written under, the field-level shape of a step inside the entry of the chain, and the format of the incident id are Not specified in the source documents (GAP-0879; ASM-1596) and are confirmed with audit and with the library owner before the baseline is tagged. The five steps and the three held-area lists are document-sourced and are fixed here as closed sets. This contract declares no feed from the observability platform.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/incidents` | `Incident` answer in state `OPEN`: body `incidentReference`, `detectedAt` (timestamp), `heldAreas` with `capabilityArea`, `rights` and `scope`, and `reason`; `Idempotency-Key` required; `Location` of the read | Platform administration C |
| POST | `/admin/incidents/{incidentId}/closure` | The same `Incident` in state `CLOSED` with `heldTo`, `fixReference` and `reportReference`; body `resolvedAt`, `fixReference`, `reportReference` and `reason`; `Idempotency-Key` required | Platform administration U |
| GET | `/admin/incidents/{incidentId}` | The `Incident` with `steps` as the five step rows in path order | Platform administration R |

Errors on the open: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 409 the reference is already open (MSG-GEN-004), 422 a required field empty, a time not a timestamp or a value outside its list (MSG-GEN-001), 503 the step cannot be recorded or the parameters contract is unavailable (MSG-P7-003). Errors on the closure: the same, with 404 for an unknown incident id and 409 for an incident already `CLOSED`, and no 409 for a reference. Errors on the read: 401 (MSG-P4-001), 403 and 404 for a record outside the caller's areas (MSG-P4-003), 404 for an unknown incident id, 503 (MSG-P7-003), and no 409 or 422. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the consumers with BACKWARD compatibility (BR9).

Both writes carry an `Idempotency-Key` requirement of their own, and the document states that a replay answers the first answer and appends no second entry. The rule-version paths of the legacy story are not declared here at all: they are the registry's in `rwb-decision`, and the load gate and the approval belong to RWB-P4-AD011-APP and RWB-P4-AD012-APP.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration C check of the open, the U check of the closure and the R check of the read, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The parameters version in force on the date of the step, carried on the entry (DP-06) |

Neither is declared as provided by rwb-access. The authorise operation is declared as consumed because the guard is a separate story of the same contract set (RWB-P4-E1037-CON); the parameters read is the only call that leaves the service, and it is the C dependency `RWB-P3-E1042-CON` of the metadata.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a step: the incident id, the reference, the steps of the entry, the held areas with their rights and scopes, the detection or resolution time, the fix reference, the report reference and the parameters version, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

The two events of `rwb-access`'s own topic  -  `AccessPolicyChanged` and `DoaLimitChanged`  -  belong to other stories of this service, and a hold is not a policy change, so this document declares the record message only. No hold and no incident is published on the service topic, because that would put the access policy of the bank on a topic.

#### 12.4 Events consumed

None. The detection arrives as the reference and the detection time a person enters, and no source declares a feed from the observability platform to P4 (GAP-0879; ASM-1594), so the baseline declares no subscription and no inbox row.

#### 12.5 Workflows and activities

None. No workflow and no activity is part of this contract; both writes are synchronous and the `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only.

#### 12.6 Schedules

None. All three operations are request-driven, and no step of an incident is a scheduled step.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role and class of the caller |
| `permission` | P4 (rwb_access) | The C, U and R letters in Platform administration, and the letters of the caller in the held areas |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The two entries of an incident, read by incident id and written once each |
| `idempotency_key`, `outbox_event`, `processed_event` | PLT library, created in rwb_access | The idempotency row and the outbox row of an entry; no inbox row |
| `delegation_limit`, `masking_rule`, `role_conflict` | P4 (rwb_access) | Named as this service's and named as untouched: a hold writes no value in force |
| `decision_log_entry` | P7 (rwb_decision) | Not named as this service's and not read: the central ledger is P7's |

No incident table is named, because none exists in any schema of the sources (BR5). No table of another service is named in the contract (DP-01): the parameters version arrives as a document of a consumed operation and never as a schema read.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| parameters fake | `GET /admin/parameters` with the parameters version "PAR-2026.11" in force on 15 December 2026, and a second version after it | App story, contract tests |
| authorise fake | `POST /authorise` with a granted answer for RW-PLATADM with `CRUD` and for RW-AUDIT with `R`, and a refused answer with MSG-P4-002 for RW-PHONECOL with `-` | App story, contract tests |
| decision-record fake | The append of an entry, the hash-link check, the read of the two entries of one incident id and their five steps, the replay by `Idempotency-Key` and a forced write failure | App story, contract tests, audit reader |
| gateway-bff fake | The incident surface of the composite route: the open form with its held areas, the closure form and the read with its five steps | Screen route |

The reference "INC0004521", the fix "CHG-4471" and the report "IR-2026-031" of the fixtures are synthetic and no production payload and no real person reference is copied into a fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | The open, the closure and the read provided; the authorise and parameters reads consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-incident-v1.yaml` (OpenAPI 3.1) with the three operations and the shared components, `contract/error-envelope.yaml`, the `Incident`, `IncidentStep` and `HeldArea` schemas with their examples, the step set and the state set as named components, the versioning rules of section 12.1, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. There is no DP-01 in the set because the contract declares no table as written by the incident record, and no DP-09 row of its own because the outbox row is the library's.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The three operations with the shapes of section 11; the incident, the step and the held area.
3. The five steps and the two states as closed enums, and the 409 of a second open and a second closure stated in the two writes.
4. The consumed operations with their owners, the one-hop rule and the 2 s client budget.
5. The error envelope and the message-ID mapping, with the business texts copied unchanged from the legacy message table where the message exists.
6. The four fakes and the stub fixtures of section 12.8, including the forced write failure of the decision-record fake.
7. The six contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note from the app story, the incident surface and the audit reader.

**Feature switch.** None of the three operations carries a flag of its own; the administration surface is switched by the service baseline of this service, and the document declares no flag, no parameter and no extra branch.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8017-APP | The three operations, the three schemas, the two closed sets and the four fakes |
| RWB-PLT-N001-CON (gateway-bff and the incident surface) | The open form, the closure form and the read with its five steps, and the `field` path of a 422 for the form's marking |
| Internal audit as the reader of the record | The five steps, the parameters version of each, the held areas and the window, as the evidence it reads after the fact |

The record code of a step, the field-level shape of a step inside the entry and the incident-id format are Not specified in the source documents (GAP-0879; ASM-1596); they are settled with audit and with the library owner, and the deprecation window of a published field is the versioning rule of BR9.

**Done when.** The document validates in the pipeline, the six contract tests pass, the four fakes answer every declared path, and the app story, the incident surface and the audit reader have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without Platform administration C writes, or without U closes, or without R reads | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The caller holds `-` in every area the incident holds | This case is not in your scope. |
| MSG-GEN-001 | A required field is empty, a time is not a timestamp, or an area, a right or a scope is outside its list | Enter {field}. |
| MSG-GEN-004 | The reference is already open, or the incident is already `CLOSED` | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | A step cannot be recorded, or the parameters contract is unavailable | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text, taken unchanged from the legacy message table of RWB-E8-017 and from FSD P4 v3 where the message already existed. MSG-GEN-001 carries `{field}` filled with the field path of the refused entry, and MSG-P4-004 of the legacy table  -  the break-glass banner  -  is not declared here because it is RWB-P4-E1039-APP's and is produced by no operation of this document.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| The incident surface of the composite route | Detect and hold form | The `HeldArea` lists, the detection time and the reason |
| The incident surface of the composite route | Open | The `Incident` in state `OPEN` with `heldFrom` and the steps `DETECTED` and `HELD` |
| The incident surface of the composite route | Already open | The 409 of the envelope with MSG-GEN-004 and the reference named |
| The incident surface of the composite route | Fix and close form | The resolution time, the fix reference, the report reference and the reason |
| The incident surface of the composite route | Closed | The `Incident` in state `CLOSED` with `heldTo` and the steps `FIXED`, `RECORDED` and `REPORTED` |
| The incident surface of the composite route | Report | The read with the five steps in path order and the parameters version of each |
| The incident surface of the composite route | Not in your areas | The 404 of the envelope with MSG-P4-003 and no field of the incident |
| The incident surface of the composite route | Refused | The 403 of the envelope with MSG-P4-002 and no form |
| SCR-39 Rules and parameters (legacy) | Empty | Not specified in the source documents (CG-ALL-5653; GAP-0879; ASM-1594) |
| SCR-39 Rules and parameters (legacy) | Loading | Not specified in the source documents (CG-ALL-5653; GAP-0879; ASM-1594) |
| SCR-39 Rules and parameters (legacy) | Error | Not specified in the source documents (CG-ALL-5653; GAP-0879; ASM-1594) |
| SCR-39 Rules and parameters (legacy) | No access | Not specified in the source documents (CG-ALL-5653; GAP-0879; ASM-1594) |
| SCR-41 Delegation of authority (legacy) | Empty | Not specified in the source documents (CG-ALL-5654; GAP-0879; ASM-1594) |
| SCR-41 Delegation of authority (legacy) | Loading | Not specified in the source documents (CG-ALL-5654; GAP-0879; ASM-1594) |
| SCR-41 Delegation of authority (legacy) | Error | Not specified in the source documents (CG-ALL-5654; GAP-0879; ASM-1594) |
| SCR-41 Delegation of authority (legacy) | No access | Not specified in the source documents (CG-ALL-5654; GAP-0879; ASM-1594) |

The surface is served by the gateway-bff composite route (DP-19), which calls the three operations, one hop each, and merges the answers. No source names an incident screen: the legacy screen table names SCR-39 Rules and parameters and SCR-41 Delegation of authority, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work (GAP-0879; ASM-1594).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-017-CON-01 | AC1 | Contract | The document validates; the base, the three operations, the rights C, U and R and the declared error responses are present; no foreign operation is provided |
| TC-E8-017-CON-02 | AC2 | Contract | The incident, step and held-area schemas with the required fields, the fourteen areas, the five rights and the four scopes as closed enums, and no personal field |
| TC-E8-017-CON-03 | AC3 | Contract | The five steps and the two states as closed enums, `DETECTED` and `HELD` on the open, `FIXED`, `RECORDED` and `REPORTED` on the closure, and no sixth step and no third state |
| TC-E8-017-CON-04 | AC4 | Contract | A 401, 403, 404, 409, 422 and 503 response carry one problem envelope with a valid message ID, and the 422 carries the field path |
| TC-E8-017-CON-05 | AC5 | Contract | Two consumed operations with their owners P4 and P3, one hop and the 2 s budget; none declared as provided; no incident table and no foreign table named |
| TC-E8-017-CON-06 | AC6 | Component | The four fakes match the document; a drifted fake fails the build; the decision-record fake answers two entries and the five steps; no name, e-mail address or personal field |
| TC-E8-017-CON-07 | AC5 | Contract | Each table of section 12.7 with its owner; the decision-record table read by incident id and written once per entry; a hold writes no row to delegation_limit, masking_rule or role_conflict; no incident table and no foreign table named |
| TC-E8-017-CON-08 | AC7 | Contract | The document compared with the tagged baseline of major version 1; no removed, renamed or retyped field, operation, step, state or enum value |
| TC-E8-017-CON-09 | AC8 | Guardrail | Each rule BR1 to BR12 of section 8 names at least one criterion and one test case that exist in sections 7 and 16 |
| TC-E8-017-CON-10 | AC9 | Component | The same write sent twice with the same idempotency key; the second answer equals the first and one entry is written; the key name is Not specified in the source documents (NEWAC-RWB-P4-E8017-CON-AC8) |

### 17. Guardrails

- No business value in the contract: the areas, rights and scopes are the closed lists of the technical specification fixed by the document, and the parameters version stays a read behind it.
- No personal data in a schema, an example or a fake: staff references, codes, versions, dates, times, rights and scopes only (BR10).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the parameters read is consumed and the ledger is absent (DP-01, BR5).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- The registry, the guard, the break-glass grant and the access-log search are declared as consumed or not at all: the document adds no rule-version, approve, grant or search path to `rwb-access` (BR11).
- A closed set stays closed: a new step, a new state, a new area or a new right is a reviewed contract change and never a value a caller may invent (BR6, BR7, BR8).
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake and no real person reference appears in a fixture.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision writes one record holding the rule and configuration versions, the actions taken and the outcome | The incident and step shapes with the parameters version, and the record message that carries them | TC-E8-017-CON-02, TC-E8-017-CON-03 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | The `rwb-case` parameters read as consumed and the `parametersVersion` on the incident and on each step | TC-E8-017-CON-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The three operations and their rights, the refused caller, the scope refusal and the screen states of section 15 | TC-E8-017-CON-04, TC-E8-017-CON-05 |

The requirement IDs are the rows this story serves, taken from the Program BRD and the FSD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this story.

### 19. Out of scope

- The implementation of the incident record (RWB-P4-E8017-APP).
- The registry's own contract: the rule-version load, its approval, the version states, the checksum and the change report (`rwb-decision`, P7, RWB-P4-E8007-CON). The legacy endpoints `POST /admin/rule-versions` and its approve are named there and not here.
- The enforcement of a hold on the calls of the other services: the guard contract of RWB-P4-E1037-CON and the authorise operation it publishes, declared here as consumed.
- The break-glass grant, the access-log search and the denial entries of a refusal: RWB-P4-E1039-CON.
- The incident surface itself, its panels and its composite route specification: RWB-PLT-N001-CON and the Epic 8 screen work.
- The monitoring that raises a detection and the observability platform that holds it: RWB-PLT-OBS.
- The central ledger `decision_log_entry` and the query API over it.
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The audit reader's own report and its evidence pack.
- The cross-service journey harness and the `-ITG` copies of the test cases.
