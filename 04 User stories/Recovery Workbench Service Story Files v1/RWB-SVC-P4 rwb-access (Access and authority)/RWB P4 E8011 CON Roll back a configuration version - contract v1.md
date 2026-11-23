# RWB-P4-E8011-CON Roll back a configuration version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8011-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-011 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the configuration rollback of `rwb-access`: an OpenAPI 3.1 document for the rollback and its read, the `ConfigRollbackRequest` and `ConfigRollback` schemas, the four target kinds, the version-state set, the decision-record declaration on `rwb.decision-record.v1` in AsyncAPI, one RFC 9457 error envelope with its message IDs, the consumed authorise and parameters operations with their owners, one hop and the 2 s budget, the contract tables of section 12 and the contract fakes**, so that **the app story, the SCR-39 and SCR-41 routes and any consumer of a configuration change can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, the four configuration tables or `rwb-case` to be built**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-011 belong to RWB-P4-E8011-APP, and the six criteria of section 7 test the document, the schemas, the target-kind and state sets, the record declaration, the envelope, the consumed declarations and the fakes.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story undid a configuration version inside the monolith, where the meaning of "previous version", the effect on a row and the record of the act were whatever the screen happened to write. In the target a version is a set of rows of `rwb-access`'s own schema with a label, a rollback is a state and date change on those rows, and the act is recorded twice — once for the withdrawal and once for the restoration.

The FSD fixes the property the contract has to express and no more: any versioned table returns to its previous version, each row keeps its record ID, and the rollback is recorded with the caller, the time and the reason (FSD P4 v3 A2.3 AC-ALT-P4-003-01, A2.22). A contract that leaves the four target kinds, the "version before" rule, the state names or the answer's shape open leaves the app story, the two screen routes and the audit consumer to guess; and a contract that answers a row's contents rather than its identity publishes the delegation table's person references to every caller.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the parameters contract of `rwb-case`, the local decision-record library and the load and approval stories of the four tables, and it catches drift between a fake and the document in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, the shared topic `rwb.decision-record.v1`, the topic `rwb.access.events.v1` that this capability does not use, the task queue `rwb-access` in namespace `rwb-recovery` and the Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline is also the place where the boundary against the other rollback story is written down: the rule package versions of `rwb-decision` and the reference-data versions of `rwb-case` are not provided here, and their gate is RWB-P4-AD013-CON, which the app story of this key does not call.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the record declaration follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that serves the version panels of SCR-39 and SCR-41 and calls the two operations, and it is a consumer of this baseline.
- The four tables are other P4 stories' (`permission` of RWB-P4-AD002-APP, `masking_rule` of RWB-P4-AD004-APP, `role_conflict` of RWB-P4-AD005-APP and `delegation_limit` of RWB-P4-E1038-APP); this document describes rows of them as TSD P4 v3 T3.1 publishes them and adds no column.
- The platform error envelope, the CloudEvents 1.0 envelope and the AsyncAPI conventions are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the ownership map only: the two operations are P4's, and the authorise and parameters operations this document consumes are P4's and P3's. No table of another service is named (DP-01).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the rollback and its read, with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the error responses and the two schemas.
2. Fix the `ConfigRollbackRequest` schema as `targetKind`, `versionLabel` and `reason`, and the `ConfigRollback` answer schema with the rollback id, the two labels, the effective moment, the two counts, the state, the two record references and the location.
3. Fix the four target kinds — `PERMISSION_MATRIX`, `MASKING_PROFILE`, `ROLE_CONFLICT`, `DELEGATION_LIMIT` — each naming the table and the version column it moves, and state that no other table is rollbackable through this document.
4. Fix the version-state set of a rollback — `ROLLED_BACK` on the withdrawn rows and `IN_FORCE` on the restored ones — out of the seven values of LOV-VERSION-STATUS, and state the transition each operation may cause.
5. Declare `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` in AsyncAPI with its two-entry key and its payload, and state in the same element that the capability publishes nothing on `rwb.access.events.v1` and that the entry carries no personal field.
6. Agree the error envelope and the message-ID mapping for 401, 403, 404, 409, 422 and 503, with the business texts taken from the legacy story where the message already existed and MSG-P3-015 carried as a message ID only.
7. Declare the consumed authorise and parameters operations as consumed with their owners, one hop and the 2 s client budget, and declare the loads, the approvals and the AD013 gate as neither provided nor consumed.
8. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
9. Add the contract tests: schema validation, the field names, the target-kind and state sets, the record declaration, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
10. Tag the baseline and hand it to RWB-P4-E8011-APP, the SCR-39 and SCR-41 routes of RWB-PLT-N001-CON and the harness of the wave 4 administration journey.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner | The review refuses the document | None | AC1, AC5 |
| X3 | A target kind other than the four is declared, or a kind names no table and no version column | The review refuses the document | None | AC1, AC2 |
| X4 | A response of 401, 403, 404, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X5 | A field of a schema is not one of the TSD field names or the T3.0 columns, or a required field is optional | The contract test fails | None | AC2 |
| X6 | A state outside the seven of LOV-VERSION-STATUS is declared, or a transition that would leave a table with no version in force | The review refuses the document | None | AC3 |
| X7 | The record declaration carries a personal field, or the capability declares a business event it does not publish | The contract test fails and the review refuses the document | None | AC3, AC6 |
| X8 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X9 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X10 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the TSD field names, the DP-03 record schema and the P3 and P4 contracts only |
| Negotiable | The two paths, the label pattern and the record codes are confirmed with the security administrator and the screen routes; the base, the state values and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the SCR-39 and SCR-41 routes and the harness on Day 1, and writes the boundary against the other rollback story down |
| Estimable | One OpenAPI document, one AsyncAPI element, one error envelope, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Roll back a configuration version contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the rollback half of the legacy journey is a state and date change on the rows of a table that carries a version label

  Scenario: AC1 The OpenAPI 3.1 document describes the rollback and its read (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the configuration rollback is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/config-rollbacks and GET /admin/config-rollbacks/{rollbackId} with the owner rwb-access
    Then the rollback names the U letter in the area of the target kind and the read names the R letter
    Then both name their error responses 401, 403, 404, 409, 422 and 503 and the rollback requires an Idempotency-Key
    Then the load, the approval and the rollback of a rule package version or a reference-data version appear in no path

  Scenario: AC2 The two schemas carry the table field names and the four target kinds (new, D-RCV-60)
    Given the ConfigRollbackRequest and ConfigRollback schemas of the document
    Then ConfigRollbackRequest carries targetKind, versionLabel and reason, all three required
    Then targetKind is one of PERMISSION_MATRIX, MASKING_PROFILE, ROLE_CONFLICT and DELEGATION_LIMIT, and nothing else
    Then each kind names its table and its version column: permission.matrix_version, masking_rule.masking_version, role_conflict.conflict_version and delegation_limit.limit_version
    Then ConfigRollback carries rollbackId, targetKind, withdrawnVersion, restoredVersion, effectiveFrom, rowsWithdrawn, rowsRestored, state, decisionRecordRefs and location
    Then every field maps to DF-REF-044, DF-REF-202, DF-REF-209 or DF-REF-055, or to a standard record column of TSD P4 v3 T3.0, or to an identifier this document mints
    Then no schema carries a row value, a holder reference or a personal field
    Then no submitted date is accepted and the effective moment is answered by the service

  Scenario: AC3 The state set and the record declaration are fixed (new, D-RCV-60)
    Given the state set of a rollback in the document
    Then the values used are ROLLED_BACK and IN_FORCE of LOV-VERSION-STATUS and no value outside the seven is declared
    Then a rollback writes ROLLED_BACK on the withdrawn rows and IN_FORCE on the restored rows in one transaction
    Then the document states that no row is inserted, deleted or re-identified by a rollback
    Then the AsyncAPI document declares rwb.decision-record.DecisionRecorded.v1 on the topic rwb.decision-record.v1
    Then its payload is the withdrawal entry and the restoration entry, each with the target kind, the two labels, the two counts, the caller reference, the reason and the time
    Then the capability declares no message on rwb.access.events.v1
    Then no workflow and no Schedule is declared for the capability

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by either operation
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002
    Then 409 carries MSG-GEN-004 for a label that is not in force or a switch that is off and MSG-P3-015 for a table with no earlier version
    Then 422 carries MSG-GEN-001 and 503 carries MSG-P7-003
    Then 404 on the read carries MSG-GEN-004 and no other error shape is declared

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation and the parameters read this service calls
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then the loads, the approvals, the delegation lookup and the rollback gate of RWB-P4-AD013-CON are declared as neither provided nor consumed here
    Then no operation owned by rwb-decision or by rwb-case is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document and against the AsyncAPI element
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the configuration fixture holds two matrix versions, one masking version, one role-conflict version and two delegation versions
    Then no schema, example, fake or record entry carries a name, an e-mail address or a personal field
```

These six criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-011 belong to RWB-P4-E8011-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are taken from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR4 | The schemas carry the version columns and the standard record columns of TSD P4 v3 T3.1 and T3.0, and add no field of another service | TSD P4 v3 T3.0, T3.1; DP-01 |
| BR5 | The target kinds are the four tables of this service that carry a version label; `role` has no version label and is not a target kind | TSD P4 v3 T3.1; ASM-3769 |
| BR6 | The state set is the seven values of LOV-VERSION-STATUS; a rollback writes `ROLLED_BACK` and `IN_FORCE` and no transition declared here leaves a table with no version in force | TSD P4 v3 T3.2; FSD P4 v3 A2.3 |
| BR7 | A rollback inserts, deletes and re-identifies no row, and the answer carries counts and labels rather than row contents | FSD P4 v3 A2.3 AC-ALT-P4-003-01; ASM-3769 |
| BR8 | The record declaration is `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`; the capability declares no business event, because the ownership map gives `rwb-access` none | Ownership Map v1; DP-03 |
| BR9 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |
| BR10 | A write requires an `Idempotency-Key`; a replay answers the first answer and appends no third entry | Architecture v5 slide 42; DP-09 |
| BR11 | The contract declares no workflow, no activity and no Schedule for the capability | Architecture v5 slide 14; TSD P4 v3 T5.3 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the two schemas, the four target kinds, the state set and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the two screen routes and the harness accept the document, the record declaration and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or the record payload changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A consumed operation changes | The parameters read or its version handling changes | Baselined, with the client budget and the stub restated |

The state set the document fixes for the rows of a rollback is the pair `ROLLED_BACK` and `IN_FORCE` out of the seven values of LOV-VERSION-STATUS; the load and approval lifecycle of the four tables (loaded, validated, approved, in force, superseded, refused) is the contracts of their own stories and is not restated here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the two schemas, the target-kind set, the state set, the record declaration and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Security administrator (RW-SECADM), as the reader of the access configuration | Reviews the matrix, masking and role-conflict target kinds and the U and R letters |
| Center of excellence analyst (RW-COE), as the roller of a delegation version | Reviews the `DELEGATION_LIMIT` kind and the fields the SCR-41 route sends |
| Tech lead of rwb-case (P3) | Reviews the parameters operation as rwb-access uses it; owns its definition |
| Tech lead of rwb-access with RWB-P4-AD013-CON and the four load stories | Confirms that the rule and reference rollback gate, the loads and the approvals stay out of this document |
| Data steward | Confirms that no personal field and no holder reference is declared in a schema, an example, a fake or the record payload |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| `ConfigRollbackRequest` | `targetKind` (required, one of the four), `versionLabel` (required), `reason` (required) |
| `ConfigRollback` | `rollbackId` (minted here), `targetKind`, `withdrawnVersion`, `restoredVersion`, `effectiveFrom`, `rowsWithdrawn`, `rowsRestored`, `state`, `decisionRecordRefs` (the two entry ids), `location` |
| Target kinds | `PERMISSION_MATRIX` → `permission.matrix_version` DF-REF-044; `MASKING_PROFILE` → `masking_rule.masking_version` DF-REF-202; `ROLE_CONFLICT` → `role_conflict.conflict_version` DF-REF-209; `DELEGATION_LIMIT` → `delegation_limit.limit_version` DF-REF-055 |
| State set | `ROLLED_BACK` and `IN_FORCE` of LOV-VERSION-STATUS, in the `state` column of TSD P4 v3 T3.0 |
| Record event | `rwb.decision-record.DecisionRecorded.v1` with the withdrawal entry and the restoration entry of a rollback |
| Refusal | `messageId` MSG-P4-001, MSG-P4-002, MSG-GEN-004 on a 404 and on the first 409, MSG-P3-015 on the second 409, MSG-GEN-001 on a 422 and MSG-P7-003 on a 503 |

The request and answer field set of the two operations, the type and length of each field, the label pattern of the three tables that are not the delegation table, the ordering rule that decides the "version before", the two record codes and the text of MSG-P3-015 are Not specified in the source documents (GAP-2280; ASM-3769, ASM-3772): TSD P4 v3 T3.1 fixes the columns and the ownership map fixes the operations, and this document fixes the rest by AC2, AC3 and section 12.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/config-rollbacks` | `ConfigRollbackRequest` in, `ConfigRollback` out with state `ROLLED_BACK`, the two labels, the two counts and the two record references | U in the area of the target kind, scope applied; `Idempotency-Key` required |
| GET | `/admin/config-rollbacks/{rollbackId}` | `ConfigRollback` out, the stored answer and its two record references | R in the area of the target kind |

Errors for both: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 404 an unknown `rollbackId` on the read (MSG-GEN-004), 409 a label that is not in force or a switch that is off (MSG-GEN-004) and a table with no earlier version (MSG-P3-015), 422 a required field empty or a reason outside its bound (MSG-GEN-001), 503 the record or the outbox row cannot be written (MSG-P7-003). The rollback is a write, so every request carries an `Idempotency-Key` and a replay answers the first answer with no third entry (BR10). Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR9).

The two paths are Not specified in the source documents (GAP-2280; ASM-3769): the legacy story names the rule-version paths that are P7's, and the write paths of this capability are fixed here and confirmed by the contract review before they are frozen. The loads, the approvals, the delegation lookup and the AD013 gate are not declared in this document.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The U check in the area of the target kind, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The reason length bound and the rollback switch, with the version in force (DP-06) |

Neither is declared as provided by rwb-access, and no operation of `rwb-decision`, `rwb-case` or the central ledger appears in the document as provided.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | AsyncAPI message keyed by the entry id, payload the withdrawal entry and the restoration entry of a rollback, in the CloudEvents 1.0 envelope |

The declaration states that a rollback publishes nothing on `rwb.access.events.v1`, because the ownership map gives `rwb-access` zero events (BR8); a consumer that needs the new state of a table reads it through that table's own read. The record payload carries the target kind, the two labels, the two counts, the caller reference, the reason and the time, and no name, no e-mail address and no personal field, and never a holder or substitute reference of a delegation row.

#### 12.4 Events consumed

None. `rwb-access` is a configuration owner, and the two operations of this contract need no subscription. The document declares no inbox and no consumer group.

#### 12.5 Workflows and activities

None. No workflow, no activity and no signal is part of this contract: a rollback is synchronous and immediate. The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only (BR11).

#### 12.6 Schedules

None. The two operations are request-driven, and the effective moment of a rollback is the moment of the call and not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `permission` | P4 (rwb_access) | The rows of the two matrix versions a rollback moves; the columns are those of TSD P4 v3 T3.1 |
| `masking_rule` | P4 (rwb_access) | The rows of the two masking versions a rollback moves |
| `role_conflict` | P4 (rwb_access) | The rows of the two conflict versions a rollback moves |
| `delegation_limit` | P4 (rwb_access) | The rows of the two delegation versions a rollback moves |
| `role` | P4 (rwb_access) | The role code and class behind the U and R letters; no role row is a target of this contract |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The withdrawal entry and the restoration entry the record event carries |

No table of another service is named in the contract (DP-01): `decision_log_entry` and the rule registry are P7 `rwb_decision`'s, `reference_version`, `reference_row` and `lov_value` are P3 `rwb_case`'s, and `document` is `rwb_document`'s. The identifiers of a row are this service's own and the answer carries counts, never row contents.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| authorise fake | `POST /authorise` granted for RW-PLATADM with CRUD in Platform administration and for RW-COE with CRUD in Rules and parameters, refused with MSG-P4-002 for RW-CASEOWN with R only | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with the reason length and the rollback switch, on and off, at version PAR-2026.11 | App story, contract tests |
| decision-record fake | The append of a withdrawal and a restoration, the hash-link check, the replay of an `Idempotency-Key` and a forced failure | App story, contract tests |
| configuration fixture | `MTX-2026.05` and `MTX-2026.11` over the same role rows with different letters, `MSK-2026.11`, `RCF-2026.11` as a single version, and `DOA-2026.11` with `DOA-2027.01` | App story, contract tests, harness |
| gateway-bff fake | The composite route of SCR-39 and SCR-41 with the version panel, the rollback form and the rolled-back state, calling both operations | Screen routes, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The rollback and its read provided; the authorise and parameters reads consumed; one hop, 2 s timeout |
| Kafka | 1 event type published, 0 consumed | `rwb.decision-record.DecisionRecorded.v1` through the DP-03 library; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output; the loads of the four tables are other stories' |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-config-rollback-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `asyncapi/rwb-access-config-rollback-v1.yaml` with the record declaration, `contract/error-envelope.yaml`, the `ConfigRollbackRequest` and `ConfigRollback` schemas with their examples, the target-kind and state-set rules in the contract README, the versioning rules, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The two operations with the shapes of section 11: `ConfigRollbackRequest` in, `ConfigRollback` out, the U and R letters and the `Idempotency-Key`.
3. The four target kinds with their tables and version columns, and the list of what is not a target kind (`role`, the rule tables, the reference tables).
4. The state set and the transition rule of BR6, stated in the document and in the README, with the no-row-moved rule of BR7 and the one-transaction rule named as required.
5. The AsyncAPI element of `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, the two-entry payload, and the explicit statement that no business event is published.
6. The consumed operations with their owners, the one-hop rule and the 2 s client budget.
7. The error envelope and the message-ID mapping for 401, 403, 404, 409, 422 and 503, with the texts of the legacy messages and MSG-P3-015 as an ID only.
8. The five fakes and the stub fixtures of section 12.8, including the two matrix versions and the single-version conflict table.
9. The six contract tests; a drift between a fake and the document fails the build.
10. Baseline tag and the consumer sign-off note from the app story, the two screen routes and the harness.

**Feature switch.** Both operations are switched by the service baseline of RWB-P4-E1037-CON and by the rollback switch parameter; the document declares no 404 branch of its own for the switch and adds no second parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8011-APP | The two provided operations, the two schemas, the four target kinds, the state set, the record declaration and the five fakes |
| RWB-PLT-N001-CON (gateway-bff, SCR-39 and SCR-41) | The two operations as the version panel, the rollback form and the rolled-back state call them |
| The harness of the wave 4 administration journey | The labels, the state set, the counts and the record references, as the evidence it records |

The ordering rule the contract fixes for "the version before" is Not specified in the source documents (GAP-2280; ASM-3769): the document states that the three dated tables order by `valid_from` and that `permission` orders by its label per the pattern the review agrees, and the rule is confirmed with RWB-P4-AD002-APP before the endpoints are frozen.

**Done when.** The document validates in the pipeline, the six contract tests pass, the AsyncAPI element matches the published topic, the five fakes answer every declared path, and the app story, the two screen routes and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A caller without the U letter in the area of the target kind, or without R on the read | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, the reason is too long, or `targetKind` is not one of the four values | Enter {field}. |
| MSG-GEN-004 | A label that names no row, a label that is not in force, the switch off, or an unknown `rollbackId` | Someone else changed this record. Reload it to see their change. |
| MSG-P3-015 | The table has no version before the named one | Not specified in the source documents (GAP-2280; ASM-3772) |
| MSG-P7-003 | The record entry or the outbox row cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-P3-015 carries a message ID and no text in this baseline, because the FSD states the refusal and not its wording; the message catalogue supplies the text before the endpoints are frozen.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-39 Rules and parameters | Versions, list | The version labels and states of the matrix, the masking profile and the role-conflict table, the version in force marked |
| SCR-39 Rules and parameters | Rollback, form | `ConfigRollbackRequest` with the named version, the label that will be restored and the reason with its bound |
| SCR-39 Rules and parameters | Rollback, done | `ConfigRollback` with the two labels, the two counts, the two record references and the effective moment |
| SCR-39 Rules and parameters | Rollback, refused | The 403 of the envelope with MSG-P4-002, the 409 with MSG-GEN-004 or MSG-P3-015 and the 422 with MSG-GEN-001 |
| SCR-39 Rules and parameters | Rollback, not recorded | The 503 of the envelope with MSG-P7-003 |
| SCR-41 Delegation of authority | Versions, list | The DoA version labels and states, the version in force marked |
| SCR-41 Delegation of authority | Rollback, done | `ConfigRollback` for `DELEGATION_LIMIT` with the withdrawn and restored DoA versions and the two record references |

The screens are served by the gateway-bff composite route (DP-19), which lists the versions of a table and calls the two operations of this contract, one hop each. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work; the document fixes the rollback side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-011-CON-01 | AC1 | Contract | The document validates; the base, the two operations, the U and R letters, the six error responses and the `Idempotency-Key` are present; no load, approval or AD013 path is provided |
| TC-E8-011-CON-02 | AC2 | Contract | The two schemas, the four target kinds with their tables and version columns, the field mapping to DF-REF-044, DF-REF-202, DF-REF-209, DF-REF-055 and T3.0, and the absence of a submitted date and of a row value |
| TC-E8-011-CON-03 | AC3 | Contract | The two states out of the seven; the no-insert, no-delete and no-re-identify rule; the record declaration on `rwb.decision-record.v1` with its two entries and no business event |
| TC-E8-011-CON-04 | AC4 | Contract | A 401, 403, 404, 409, 422 and 503 response carry one problem envelope with a valid message ID, and the 409 carries MSG-GEN-004 or MSG-P3-015 |
| TC-E8-011-CON-05 | AC5 | Contract | Two consumed operations with their owners P4 and P3, one hop and the 2 s budget; the loads, the approvals and the AD013 gate declared as neither provided nor consumed |
| TC-E8-011-CON-06 | AC6 | Component | The five fakes match the document and the AsyncAPI element, the fixture holds the four kinds, a drifted fake fails the build, and no personal field appears |

The legacy rows TC-E8-011-01 to TC-E8-011-04 are the app story's and name their criteria there; this contract owns no legacy criterion and adds no `-ITG` row, because no integration story is split from this key.

### 17. Guardrails

- No business value in the contract: the labels, the states, the reason bound and the switch stay rows and values behind the document.
- No personal data in a schema, an example, a fake or the record payload: references, labels, counts and times only.
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the central ledger, reference data and the rule registry are absent or consumed, never named as this service's (DP-01).
- One REST base, one topic and one event-name pattern per service; a document that names another service's base or topic fails the review (DP-13).
- The rule and reference rollback gate of RWB-P4-AD013-CON stays out of this document: its two owner operations are neither provided nor consumed here.
- A target kind that is not one of the four fails the review, and so does a schema that answers a row value or a holder reference.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A write without its `Idempotency-Key` is refused by the contract, and a replay never appends a third entry.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated template load to production with a version stamp and no code release, and rolls back to the previous version by one call | The rollback operation, the four kinds, the state set and the two record entries | TC-E8-011-CON-01, TC-E8-011-CON-03 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | The parameters read as consumed, the reason bound and the switch behind the document, and the version label as data | TC-E8-011-CON-02, TC-E8-011-CON-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The two operations as the SCR-39 and SCR-41 routes consume them, with the U and R letters and the refusal shapes | TC-E8-011-CON-04, TC-E8-011-CON-06 |

The requirement IDs are taken from the FSD feature table and the Program BRD under the fill order of Template and Rules §R7.3, which is the order the Work Package directs; the Work Package itself carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 any versioned table returned to its previous version and the rollback recorded | Sections 4, 7, 11, 12.1 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 7, 12.1, 14 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 3, 7 (AC1, AC5), 10, 12.1, 14 |
| The endpoints of the legacy story: the rule-version paths that are P7's | Sections 12.1, 19 |
| The data table: `role` and `rule_row` fields | Sections 11, 12.7 |
| MSG-P4-002, MSG-P4-004, MSG-GEN-001, MSG-P3-015, MSG-P7-003 | Sections 7 (AC4), 14 |
| Legacy key RWB-E8-011, story RWB-P4-E8011-APP, contract RWB-P4-E8011-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the rollback and its read (RWB-P4-E8011-APP).
- The rule package versions of `rwb-decision` and the reference-data versions of `rwb-case`, and the gate in front of them (RWB-P4-AD013-CON, RWB-P4-AD013-APP); this document declares neither their operations nor their tables.
- The load, the approval and the four-eyes rule of the four tables (RWB-P4-AD002-CON, RWB-P4-AD004-CON, RWB-P4-AD005-CON, RWB-P4-E1038-CON); this document consumes their shapes.
- The columns, indexes and migrations of the four tables (DP-15), and the role list itself (RWB-P4-AD001-CON, RWB-P4-E1019-CON).
- The delegation lookup `GET /api/recovery/access/v1/doa-limits` and the authority decision behind `POST /authorise` (RWB-P4-E2013-CON, RWB-P4-E1037-CON).
- The screens SCR-39 and SCR-41, their other panels and their composite route specification (RWB-PLT-N001-CON and the Epic 8 screen work).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the authorise operation and the `rwb-case` parameters read are consumed and faked, never defined here.
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases.
