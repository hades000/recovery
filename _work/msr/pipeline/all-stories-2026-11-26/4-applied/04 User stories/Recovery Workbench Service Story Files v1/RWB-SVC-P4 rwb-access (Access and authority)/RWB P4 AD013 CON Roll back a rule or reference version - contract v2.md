# RWB-P4-AD013-CON Roll back a rule or reference version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-013 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-AD013-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the access-side rollback gate: an OpenAPI 3.1 document for the two console operations that undo a rule version or a reference-data version, the `VersionRollbackRequest` and `VersionRollback` schemas, the single state this service produces, the error envelope and the message mapping, the two owner rollback operations and the authorise operation declared as consumed with their owners, the statement that no rule table and no reference table is written here and that a rollback is recorded twice, the contract tables of section 12 and the contract fakes**, so that **the app story and the console build the gate on Day 1 against a fixed document while the rule registry stays `rwb-decision`'s and the reference store stays `rwb-case`'s, and no operation of either owner is claimed here**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story undid a bad version inside the monolith: one endpoint moved a rule row and a reference row, one log write said something happened, and nothing outside that module could tell which version went or which came back. In the target the two restores belong to two services — `rwb-decision` holds the rule package version and its states (ASM-0069) and `rwb-case` holds the reference version (DP-07) — while the person undoing a bad morning is in front of one administration screen. The two sides of that meet on a contract, and the contract has to say exactly what the gate accepts, what it answers, what it refuses and what it does not write.

If that field-level contract is agreed once and faked for the two owner rollback operations and the authorise operation, the app story builds in parallel with P7 and P3, a change in either owner is caught in a contract test rather than in an integration window, and the two facts of a rollback — the withdrawal and the restoration — are fixed as contract elements before either side writes them. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service with no event of this journey on it, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline carries a second, quieter purpose: it is where the product says out loud that an undo is two records and not one. A single entry would let the audit trail claim that a version was never in force; the contract declares both entries, their decision codes and their two references in the answer, so a screen, an auditor or a report that reads only the contract still learns that a version was withdrawn before another was restored.

### 3. Preconditions

- The service template and the naming library are available, so the base, the topic and the queue follow the platform rule rather than a local choice.
- The platform error envelope, the RFC 9457 problem response and the `Idempotency-Key` rule on every POST are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the ownership map only: `POST /admin/rule-package-versions/{versionId}/rollback` is P7's under ASM-0040, `POST /admin/reference-loads/{loadId}/rollback` is P3's under ASM-0041, and the two console operations of this contract are `rwb-access`'s.
- The owner halves — `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` in `rwb-decision`, and `reference_row`, `reference_version` and `lov_value` in `rwb-case` — are consumed and never defined here (ASM-0069, ASM-0071, DP-07).
- The decision record is the platform library of DP-03 with the shared topic `rwb.decision-record.v1`, and the two decision codes of a rollback are proposed values pending the decision-code list — Not specified in the source documents (GAP-0854; ASM-1555).
- The two provided paths have no source in the API Specification v4 or in the P4 technical specification, and no source declares a rollback resource that can be read back — Not specified in the source documents (GAP-0852; ASM-1553).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two console operations of `rwb-access` with the shared components the service uses.
2. Declare `POST /admin/version-rollbacks` with the five-field request, the `Idempotency-Key` header, the 201 answer with the `Location` of the read, and the read of a rollback by `rollbackId`.
3. Declare the `VersionRollbackRequest` and `VersionRollback` schemas, the two target kinds, the single state `ROLLED_BACK`, the two decision-record references and the statement about decisions taken from the effective time.
4. Agree the error envelope and the message mapping: 401, 403, 404, 409, 422 and 503, with one message id per condition and the separation-of-duty refusal declared once.
5. Declare the three consumed operations with their owners, one hop and the 2 s client budget: the P7 rule-package rollback, the P3 reference-load rollback and the own authorise operation.
6. State what the service does not write: no rule table, no reference table and no version state, and the two decision-record entries that it does write.
7. State that nothing is published on `rwb.access.events.v1` and that the only topic of the journey is `rwb.decision-record.v1`.
8. Publish the contract tables of section 12, nine sub-tables, and the contract fakes.
9. Add the contract tests: schema validation, envelope validation, message mapping, the consumed-operation list, the no-table and two-record statements, and drift detection between a fake and the document.
10. Tag the baseline and hand it to RWB-P4-AD013-APP and to the P7 and P3 owners whose operations it consumes.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request body field fails schema validation, is empty or is out of its declared set | 422 with the error envelope and the failing pointer | MSG-GEN-001 | AC1, AC2, AC3 |
| X2 | A caller without the C or U letter in the area of the target, or without the A letter where the approver is checked | 403 with the error envelope and the refusal code | MSG-P4-002 | AC1, AC3 |
| X3 | The caller is the loader of the version in force | 409 with the separation-of-duty code, declared once | MSG-P7-002 | AC3 |
| X4 | The target is unknown to the owner | 404 with the error envelope; no empty answer is invented | None | AC1, AC4 |
| X5 | The owner answers that the version is no longer in force | 409 with the owner's code carried in `detail` | MSG-GEN-004 | AC3 |
| X6 | The owner does not answer inside the 2 s budget, or the record cannot be written | 503 declared on both operations; no state is reported as changed | MSG-P7-003 | AC3, AC4 |
| X7 | A field of the answer has no source definition | The field is declared with the placeholder and carried as a gap in the app story | None | AC2 |
| X8 | A contract fake drifts from the document, or carries a personal data field | The contract test fails and the merge is blocked | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes and the P7, P3 and own-service contracts only |
| Negotiable | The field names of the answer, the reason bounds and the two decision codes are settled with the two owners; the operations, the state, the envelope and the two-record statement are fixed |
| Valuable | Unblocks the app story and both screens on Day 1 and keeps two owners' tables out of the `rwb-access` document |
| Estimable | One OpenAPI document, one envelope, one refusal shape, nine contract tables, five fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Access-side rollback contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access-side half of the legacy journey is the rollback gate and its read

  Scenario: AC1 The OpenAPI 3.1 document describes the two console operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/version-rollbacks and GET /admin/version-rollbacks/{rollbackId} with the owner rwb-access
    Then the POST declares the body VersionRollbackRequest and the Idempotency-Key header and answers 201 with the Location of the read
    Then the POST names Rules and parameters C or U for a rule target and Reference data C or U for a reference target, and the read names Rules and parameters R or Reference data R
    Then both operations declare 401 and 403, the POST declares 404, 409, 422 and 503, and the read declares 404

  Scenario: AC2 The request, the answer and the single state are declared once (new, D-RCV-60)
    Given the VersionRollbackRequest and VersionRollback schemas of the document
    Then VersionRollbackRequest carries targetKind, targetId, previousVersionId, effectiveDate and reason
    Then targetKind is the enumeration RULE and REFERENCE, and reason declares a minimum and a maximum length
    Then VersionRollback carries rollbackId, targetKind, targetId, restoredVersion, effectiveFrom, state, decisionRecordRefs and statement
    Then state is the single value ROLLED_BACK and decisionRecordRefs carries exactly two references
    Then statement is the declared text that decisions taken from effectiveFrom use the restored version
    Then no property of either schema is a name, an e-mail address or a personal field

  Scenario: AC3 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by a console operation
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002 and 422 carries MSG-GEN-001 naming the field
    Then the separation-of-duty refusal is declared once as 409 with MSG-P7-002, and a version no longer in force is declared as 409 with MSG-GEN-004
    Then 503 carries MSG-P7-003 and the response carries the problem media type and the trace identifier
    Then the document states the MSG-P7-002 text as the decision centre's and kept verbatim, not redefined here

  Scenario: AC4 The three consumed operations are declared as consumed (new, D-RCV-60)
    Given the P7 rule-package rollback, the P3 reference-load rollback and the own authorise operation
    Then each is declared in the consumed section with its owner P7, P3 or P4, one hop and the 2 s client budget
    Then the rule arm is declared as POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback with the owner rwb-decision
    Then the reference arm is declared as POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback with the owner rwb-case
    Then the document declares no operation owned by rwb-decision, rwb-case or the platform as provided by rwb-access

  Scenario: AC5 The document states what is not written and that a rollback is two records (new, D-RCV-60)
    Given the contract tables of section 12
    Then the document states that no rule_package, rule_package_version, rule_row, reference_row, reference_version or lov_value table is written by rwb-access
    Then the document states that a rollback writes two decision-record entries, one for the withdrawal and one for the restoration, with decision codes and two references
    Then 12.7 names role, permission and the library tables and no rule table and no reference table
    Then the document states that nothing is published on rwb.access.events.v1 and that rwb.decision-record.v1 is the only topic of the journey

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of section 12.8
    When the contract tests run
    Then each fake answers the paths and payloads of 12.2 and 12.8, including the accepted rollback of each arm, the separation-of-duty refusal and the 503
    Then a contract test fails on any drift between a fake and the document
    Then no schema, example or fake holds a name, an e-mail address or a personal field
```

These six criteria test the artefact only. No criterion restates a legacy acceptance criterion, and the legacy test cases TC-AD-013-01, TC-AD-013-02 and TC-AD-013-03 are owned by RWB-P4-AD013-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 14 |
| BR2 | A consumed operation is described as consumed, never as provided, and its owner comes from the ownership map | DP-11; Ownership Map v1; ASM-0040; ASM-0041 |
| BR3 | The contract declares no rule table and no reference table of `rwb-access`, because those tables are P7's and P3's | DP-01; ASM-0069; DP-07 |
| BR4 | A rollback is two decision-record entries declared as contract elements: a withdrawal and a restoration, each with its decision code and its reference | Legacy RWB-AD-013 AC1 ("both changes are logged"); DP-03; GAP-0854; ASM-1555 |
| BR5 | Error responses use one envelope and one message id per condition; the business texts are copied from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR6 | The single state of this contract is `ROLLED_BACK`; the other values of LOV-VERSION-STATUS are the owners' and are passed through unchanged | TSD P4 v3 T3.2 and T4 |
| BR7 | The answer carries the statement that decisions taken from the effective time use the restored version, and the read repeats it | Legacy RWB-AD-013 AC1; R-UNI-38; GAP-0853; ASM-1554 |
| BR8 | The reason length, the target kinds and the areas are rows and list values, never a value in the document | DP-06; TSD P4 v3 T3.2; BR-P4-022 |
| BR9 | No schema, example or fake carries a personal data field | Principle 5; NFR-040 |
| BR10 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |
| BR11 | Nothing is declared on `rwb.access.events.v1`: a rollback is neither an access policy change nor a delegation-limit change | Architecture v5 slides 14 and 43 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the two schemas, the envelope and the three consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the two owner teams and the console accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake, or a personal field in a schema or an example | A contract test fails | In review |

The document declares one business state for the artefact it describes, `ROLLED_BACK`, and no transition of it: the transitions of a rule package version are `rwb-decision`'s (TSD P4 v3 T4) and those of a reference version are `rwb-case`'s.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-access` | Owns the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Tech lead of `rwb-decision` (P7) | Reviews the consumed rule-package rollback and the state it answers; owns its definition |
| Tech lead of `rwb-case` (P3) | Reviews the consumed reference-load rollback and the effective dating it answers |
| Console lead and the QA team | Review and sign off the screen states of section 15 and the field list they consume |
| Data steward | Confirms that no personal data field is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| `VersionRollbackRequest` | `targetKind` (`RULE` or `REFERENCE`), `targetId`, `previousVersionId`, `effectiveDate`, `reason`; no caller identity in the body and no personal field |
| `VersionRollback` | `rollbackId`, `targetKind`, `targetId`, `restoredVersion`, `effectiveFrom`, `state`, `decisionRecordRefs[]` (exactly two), `statement` |
| Refusal | `code`, `message` with `messageId`, `state` of the owner where it answered one, `traceId`, `instance` |
| Decision record | the two entries the app story writes: decision code, target kind, the two version labels, the effective date, the loader and approver references, the outcome |
| Event payloads | None of this contract: the only topic of the journey is the shared `rwb.decision-record.v1` of DP-03 |

The decision codes and the exact text of the statement are the two fields of this document that no source defines — Not specified in the source documents (GAP-0854; ASM-1555; GAP-0853; ASM-1554). The version labels are the owners' and are carried unchanged; the rollback id is the gate's own and is the handle the screen, the two entries and the read share.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/version-rollbacks` | Body `VersionRollbackRequest`; answers 201 with `VersionRollback` and the `Location` of the read; `Idempotency-Key` required | Rules and parameters C or U for a rule target; Reference data C or U for a reference target |
| GET | `/admin/version-rollbacks/{rollbackId}` | Answers `VersionRollback` from the stored answer of the accepted call, with its two record references | Rules and parameters R, or Reference data R |

Errors: 401 no session (MSG-P4-001) and 403 no right (MSG-P4-002) on both; the POST adds 404 for an unknown target, 409 for the separation of duty (MSG-P7-002) and for a version no longer in force (MSG-GEN-004), 422 for a missing or out-of-range field (MSG-GEN-001), and 503 when the record or the owner fails (MSG-P7-003); the read adds 404 for an unknown rollback. The POST carries the `Idempotency-Key` header and the document states that a repeated key answers the first answer; the GET is a read and carries none.

The two operations have no source path in the API Specification v4 or in the P4 technical specification, and no source declares a rollback that can be read back — Not specified in the source documents (GAP-0852; ASM-1553). The two owner operations themselves are P7's and P3's under ASM-0040 and ASM-0041 and are consumed, never provided, here.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback` | P7 `rwb-decision` | The rule arm: withdraw the version in force to `ROLLED_BACK` and put the version before it in force, with the reason |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | P3 `rwb-case` | The reference arm: the same move on a reference-data version, with the reason |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` | The C, U, A or R check behind the two provided operations |

None of the three is declared as provided by this document except the authorise operation, which is this service's and is consumed here by its own guard. The two owner rollbacks are the halves that move the versions.

#### 12.3 Events published

None. `rwb.access.events.v1` carries only `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` (Architecture v5 slide 14), and this contract adds no event type. The two facts of a rollback travel on the shared `rwb.decision-record.v1` of DP-03 as `rwb.decision-record.DecisionRecorded.v1` entries written by the app story through the record library; the contract declares the entries and their two references, and the topic is the platform's.

#### 12.4 Events consumed

None. This contract declares no subscription: `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and the gate answers a request rather than reacting to one.

#### 12.5 Workflows and activities

None. No workflow and no activity is declared: a rollback is one synchronous command with one downstream call, and the promotion and chain-check Schedules belong to `rwb-decision`.

#### 12.6 Schedules

None. A rollback is request-driven and this document declares no timer and no schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's role and its class behind the letters |
| `permission` | P4 (`rwb_access`) | The letter of the caller in the area of the target and in the approver's area |
| `outbox_event`, `idempotency_key`, `processed_event` | PLT library, created in `rwb_access` | The outbox rows of the two entries and the stored answer the read replays (DP-09) |

No rule table and no reference table is named in the contract and no table of another service is read (DP-01). `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` stay P7 `rwb-decision`'s under ASM-0069, and `reference_row`, `reference_version` and `lov_value` stay P3 `rwb-case`'s under DP-07; they appear only as consumed shapes.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision rule-package WireMock | `POST /admin/rule-package-versions/{versionId}/rollback` answering "ENTRY-2026.12" withdrawn to `ROLLED_BACK` with "ENTRY-2026.11" in force from 15 December 2026; a 409 for a version no longer in force; a 503 and a timeout | App story, contract tests, console |
| rwb-case reference-data WireMock | `POST /admin/reference-loads/{loadId}/rollback` answering load "LD-2026-118" restored to "LOV-ROUTE 2026.11" in force from 15 December 2026; the version read behind the reference arm; a 404 and a 503 | App story, contract tests |
| parameters fake | The reason length of 20 to 1000 and the rollback switch, with the version in force on 15 December 2026 | App story, contract tests |
| decision-record fake | The append of the two entries and the reference each returns; a forced failure for the 503 | App story, contract tests |
| authorise and guard fake | `POST /authorise` granting C and U to RW-COE and RW-REFADM, A to RW-RISK and R to RW-CASEOWN and RW-AUDIT, and refusing a caller with no role with MSG-P4-001 | App story, contract tests |
| gateway-bff composite route fake | The SCR-40 and SCR-39 routes calling the rollback and the read, one hop each, and merging the answer with the version list | Console, app story |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The rollback and its read provided; the two owner rollbacks and the own authorise operation consumed; one hop, 2 s timeout |
| Kafka | 0 published, 0 consumed | No event in this contract; the record topic belongs to the platform library |
| Temporal | 0 workflows, 0 activities | No workflow in the gate |
| File | None | A rollback reads no file |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-version-rollback-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml` with the message mapping, the `VersionRollbackRequest` and `VersionRollback` schemas, the refusal contract, the two-record statement and the idempotency and versioning rules in the contract README, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the only pattern that carries a rule of this document rather than a dependency: the record library is what makes "both changes are logged" two entries instead of one, and the contract declares them as contract elements. DP-07 is declared because the reference arm is a consumed reference-data operation and the document names no reference table of its own. There is no DP-04: this gate embeds no Drools kit and evaluates no rule.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The two provided operations with the five-field request, the `Idempotency-Key` and the `Location` of the read.
3. The `VersionRollbackRequest` and `VersionRollback` schemas, the two target kinds and the single state of BR6.
4. The error envelope and the message-id mapping, with the business texts copied from the legacy story where they existed and MSG-P7-002 kept verbatim from its owner.
5. The two decision-record references in the answer and the statement of BR7, declared once and repeated by the read.
6. The three consumed operations with their owners, the one-hop rule and the 2 s client budget.
7. The six fakes and the stub fixtures of section 12.8.
8. The seven contract tests: schema, envelope, message mapping, refusal shape, consumed list, the no-table and two-record statements, and drift.
9. Baseline tag and the consumer sign-off note from the app story, the console and the P7 and P3 owners.

**Feature switch.** The document declares no switch: a rollback gate that is switched off would leave a breach-causing version in force while the screen said nothing, so the refusal path is the control and it is not a flag. The one parameter that changes the gate's behaviour is the row of DP-06, and the contract names the row, never its value.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD013-APP | The two provided operations, the two schemas, the two-record statement and the six fakes |
| SCR-40 and SCR-39 console build | The states of section 15, the answer fields and the two references |
| The P7 rule-package owner of `rwb-decision` | The consumed rule-package rollback as the gate uses it; no P7 operation is claimed as provided |
| The P3 reference-data owner of `rwb-case` | The consumed reference-load rollback and the effective dating it answers |

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the six fakes answer every consumed path, and the app story, the console and the P7 and P3 owners have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is empty, `targetKind` is outside its enumeration, the date is not a date or the reason is outside its bounds | Enter {field}. |
| MSG-GEN-004 | The owner answers that the version is no longer in force | Someone else changed this record. Reload it to see their change. |
| MSG-P4-001 | No session, or no role row for the caller | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the C, U, A or R letter required by the condition | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A target outside the caller's scope | This case is not in your scope. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-P7-002 | The caller is the loader of the version in force | Not specified in the source documents (GAP-0855; ASM-1556); the text is the decision centre's and is kept verbatim |
| MSG-P7-003 | The record cannot be written, or the owner cannot be reached inside the budget | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message ids are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-P7-002 is declared once, as a 409 on the POST, because the rollback is refused by a state the record already knows rather than by a missing right; the approval story of the same module answers 403 for the same condition and the P4 technical specification carries no text for the message, so both the text and the status are carried as one gap — Not specified in the source documents (GAP-0855; ASM-1556).

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-40 Reference data | Version in force | The version list of the owner, with the rollback action where the caller holds the letter |
| SCR-40 Reference data | Rollback form | `VersionRollbackRequest` with targetKind REFERENCE, the load, the previous version and the date defaulted to today |
| SCR-40 Reference data | Refused | The 422, 403 or 409 envelope with its `messageId`, and the 503 with MSG-P7-003 |
| SCR-40 Reference data | Rolled back | `VersionRollback` with the restored version, `effectiveFrom`, `state` `ROLLED_BACK`, the two references and the statement |
| SCR-39 Rules and parameters | Version in force and rollback form | The same elements with targetKind RULE and the package version |
| SCR-39 Rules and parameters | Rolled back and refused | The same answer and the same envelopes as SCR-40 |

The screens are served by the gateway-bff composite route (DP-19), which calls the two operations and the owner's version list in parallel, one hop each, and merges the answers. The composite route specification is the platform's; this document fixes the access side of the merge only, and it fixes that the statement about decisions from the effective time is shown from the answer rather than rebuilt on the screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-013-CON-01 | AC1 | Contract | The document validates; the base, the two operations, the two target kinds, the rights and the error responses 401, 403, 404, 409, 422 and 503 |
| TC-AD-013-CON-02 | AC2 | Contract | The five request fields and the eight answer fields; the two target kinds; the single state `ROLLED_BACK`; exactly two record references; the statement; no personal field |
| TC-AD-013-CON-03 | AC3 | Contract | The envelope with MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-004, MSG-GEN-001, MSG-GEN-004, MSG-P7-002 and MSG-P7-003, and the single 409 declaration of the separation of duty |
| TC-AD-013-CON-04 | AC4 | Contract | The three consumed operations with owner, one hop and the 2 s budget; no P7, P3 or platform operation declared as provided |
| TC-AD-013-CON-05 | AC5 | Contract | The no-table statement, the two-record statement and 12.7 naming no rule table and no reference table; nothing declared on the access topic |
| TC-AD-013-CON-06 | AC6 | Contract | The six fakes match the document; a drifted fake and a personal field each fail the build |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The three legacy test cases TC-AD-013-01, TC-AD-013-02 and TC-AD-013-03 are owned by RWB-P4-AD013-APP and are not copied here; no ITG story is split from this legacy key, so no `-ITG` copy is written either.

### 17. Guardrails

- No business value in the contract: the reason bounds, the target kinds, the areas and the version states stay parameter rows and list values with versions (BR8). The document names the parameter, never its value as a constant.
- No personal data in a schema, an example or a fake: user references, codes, version labels, dates and a reason only, and a contract test fails on a personal field (BR9).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the two owner tables and the two owner rollback operations are consumed and documented as consumed (DP-01, ASM-0069, DP-07).
- One REST base per service; a document that names another service's base fails the review (DP-13).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- A rollback is always two records: a document or an implementation that declares one entry fails the review (BR4).
- The error envelope and the `Idempotency-Key` rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated template load to production with a version stamp and no code release, and rolls back to the previous version by one call | The rollback operation, the restored version in the answer and the consumed rule-package rollback | TC-AD-013-CON-01, TC-AD-013-CON-02, TC-AD-013-CON-04 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned | The reason bounds read from the parameter row and the document's refusal to hold a value | TC-AD-013-CON-02, TC-AD-013-CON-04 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available | The C, U, A and R letters on the operations and the SCR-40 and SCR-39 states through the composite route | TC-AD-013-CON-01, TC-AD-013-CON-03 |
| R-UNI-38 | A new rule version applies from its effective date and open cases keep the version they were decided under | The `effectiveFrom` field and the statement in the answer | TC-AD-013-CON-02, TC-AD-013-CON-05 |
| R-UNI-39 | An action whose decision record cannot be written does not proceed | The 503 with MSG-P7-003 and the two-record statement | TC-AD-013-CON-05 |

### 19. Out of scope

- The implementation of the gate, the validation pass, the date rule, the separation-of-duty rule, the owner client, the record writer and the idempotency store (RWB-P4-AD013-APP).
- The two owner halves: the rule-package rollback and its states (P7 `rwb-decision`; ASM-0069; ASM-0040) and the reference-load rollback (P3 `rwb-case`; DP-07; ASM-0041).
- The `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `reference_row`, `reference_version` and `lov_value` tables, and their migrations.
- The load, the approval and the promotion of a version, with their screens and their contracts.
- The rule change report, the dry run and the chain check of `rwb-decision`.
- The deployment, the Helm chart, the metrics, the dashboards and the runbook of this capability.
- The operations of other services beyond the three consumed here; the `rwb-decision`, `rwb-case` and platform contracts are consumed and faked, never defined here.
- The cross-service journey evidence: no ITG story is split from this legacy key, so no `-ITG` copy of a test case is written here.
