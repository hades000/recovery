# RWB-P4-AD009-CON Load a list of values version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD009-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | CG-W4 |
| Epic design sign-off | Accepted under the programme directive. Signed epic design record: Not specified in the source documents (DOR-RWB-P4-AD009-CON-14) |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement |
| Contract version | /v1 of base /api/recovery/access/v1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-009 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 8 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **solution architect**, I want **the published contract baseline of the administration ingest of a list of values: an OpenAPI 3.1 document for the two console operations under the access base, the `LovLoad` and `LovLoadCheck` schemas with the two load states, the multipart request shape, the error envelope and its message IDs, the consumed reference-data, parameters and authorise operations with their owners, and the contract fakes**, so that **the app story, the screen through gateway-bff and the wave 4 harness can build on Day 1 against a fixed, testable boundary that states in writing which side stores the rows and which side only checks them**.

The boundary this baseline fixes is the D-RCV-60 split of RWB-AD-009: under the R-PREC default ruling `lov_value`, `reference_version`, `reference_row` and the reference-load operations belong to P3 `rwb-case` (ASM-0071, ASM-0041), and `rwb-access` provides the console ingest and its checks. The service facts are `rwb-access`, schema `rwb_access`, base `/api/recovery/access/v1`, topic `rwb.access.events.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

This story owns no legacy acceptance criterion: the two legacy criteria of RWB-AD-009 belong to RWB-P4-AD009-APP. Every criterion below tests the artefact.

### 2. Business rationale

Contract-first REST, one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Here it also settles an ownership question that the documents answer two ways: the TSD P4 v3 lists the list-of-values paths and their rows in the access module, and the R-PREC default ruling puts parameters and reference data with `rwb-case`. A written contract is the only place where that split stops being an argument: the document declares the two operations `rwb-access` serves, declares the three operations it consumes and their owners, declares that it writes no `lov_value` row, and states that the console path is reconciled at review before it is frozen (GAP-0811; ASM-1512).

With the boundary fixed and faked, the app story builds without waiting for `rwb-case`'s reference-data contract, the screen can be wired through gateway-bff on the same day, and a change on either side is caught by a contract test rather than in an integration window. The baseline also fixes the naming the checks require: base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with the event names `rwb.access.<Event>.v1`, queue `rwb-access` and the packet `th.co.scb.ace.workbench.recovery.access`.

It serves REQ-DRI-011 by declaring the version, the valid-from date and the row count as first-class fields of the load, REQ-DRI-010 by declaring the caps as parameters rather than as constants in the document, and REQ-ACA-013 by declaring the two operations the administration screen SCR-40 calls.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), whose message the record of a load uses.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19), which is the only consumer of the two console operations.
- The platform error envelope and the RFC 9457 problem media type are the platform baseline; where this document narrows them it does so explicitly, and it never redefines them.
- The owners of the consumed operations come from the ownership map only: `POST /admin/reference-loads`, `GET /admin/lists/{listCode}` and the parameters reads are P3 `rwb-case`'s (ASM-0041), and the authorise operation is this service's own.
- The public path the Workbench console uses for the load is Not specified in the source documents (GAP-0811; ASM-1512): the document declares the path under the access base and the review reconciles it with the owner's operation before the baseline is frozen.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document with the base path, the security scheme, the shared components and the two console operations.
2. Draft the multipart request of the load: the part `file`, the query parameters `lovCode` and `validFrom`, and the required `Idempotency-Key`.
3. Draft `LovLoad` and `LovLoadCheck`, including the `checks[]` lines with their field and row, and the two states LOADED and REFUSED.
4. Agree the error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the 409 shape that carries `valueCode` and `count`.
5. Declare the consumed operations with their owners, one hop and the 2 s client budget, and the parameters and reference-data reads as client-library calls.
6. State in the document that no `lov_value`, `reference_version` or `reference_row` row is written by this service and that no reference table is declared by it, naming the owner contract.
7. Publish the contract tables of section 12 (nine sub-tables) and the fakes.
8. Add the contract tests: schema validation, the state set, the error mapping, the consumed-owner check, the no-reference-table check and the drift check between a fake and the document.
9. Tag the baseline and hand it to RWB-P4-AD009-APP, RWB-P4-AD010-APP, the gateway-bff route story and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 schema validation | The pipeline fails and the baseline is not tagged | None | AC1 |
| X2 | A request is malformed, or the `file` part is absent | 422 with the error envelope and the failing pointer or field | MSG-GEN-001 | AC1, AC3 |
| X3 | A caller holds no right on the operation | 403 with the error envelope and the refusal code | MSG-P4-002 | AC3 |
| X4 | The load would remove a value code in use | 409 with the envelope, `valueCode` and `count` | MSG-GEN-004 | AC3 |
| X5 | A schema or an example carries a personal field | The review fails and the field is removed before the tag | None | AC6 |
| X6 | The document declares a reference table of its own, or an operation owned by another service as provided | The review fails | None | AC5 |
| X7 | A fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X8 | A consumed operation is renamed by its owner | The contract test fails and the pinned version is raised at review | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes and the P3 contract only |
| Negotiable | The field-level detail of the check lines and the exact console path are settled with the owner and the screen at review; the two operations, the states, the envelope and the split are fixed by the target architecture |
| Valuable | Unblocks the app story, the approval story and the wave 4 harness on Day 1, and writes down which service stores the rows |
| Estimable | One document, two schemas, one error envelope, nine contract tables, three fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Administration ingest of a list of values, contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access side of the legacy journey is the console ingest and its checks

  Scenario: AC1 The OpenAPI 3.1 document describes the two console operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/lov-loads and GET /admin/lov-loads/{loadId} with the owner rwb-access
    Then the load declares the multipart request with the part file and the query parameters lovCode and validFrom, and the required Idempotency-Key header
    Then each operation declares its security right and its responses 401, 403, 409, 422 and 503, and the GET also declares 404

  Scenario: AC2 The load and its check lines are declared with two states (new, D-RCV-60)
    Given the LovLoad and LovLoadCheck schemas of the document
    When the contract review runs on the published document and reads its load schemas
    Then LovLoad carries loadId, lovCode, validFrom, rowCount, checks and state
    Then LovLoadCheck carries name, result, row, field and detail, with row and field present only for a row check
    Then state is one of LOADED and REFUSED and the document declares no other value
    Then the page-level fields carry no case number, no party key and no personal field

  Scenario: AC3 Every failure is one envelope with one message and the 409 carries its count (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 409, 422 or 503 response is produced by a console operation
    Then the body carries code, message, messageId, traceId and the field list, with the problem media type
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002 and 422 carries MSG-GEN-001 with field and row
    Then 409 carries MSG-GEN-004 with valueCode and count, and 503 carries MSG-P7-003 for a record that cannot be written
    Then no response declares a business text other than the agreed one for its message ID

  Scenario: AC4 The consumed operations are declared as consumed with their owners (new, D-RCV-60)
    Given the reference-load and list reads of the rwb-case contract, the parameters read of the same contract and the authorise operation
    When the contract review runs on the published document and reads its consumed operations
    Then each is declared in the consumed section with its owner P3 or P4, one hop and the 2 s client budget
    Then the document declares no operation owned by rwb-case as provided by rwb-access
    Then the parameters and reference-data reads are declared as client-library calls of DP-06 and DP-07

  Scenario: AC5 The document writes no list row and says who does (new, D-RCV-60)
    Given the document and its shared components
    When the contract review runs on the published document and reads its shared components and owners
    Then it states that this service writes no lov_value, reference_version or reference_row row
    Then it names the owner contract and the ruling ASM-0071 and ASM-0041
    Then no schema of the document declares a reference table, a list row or a version row
    Then no table of another service appears as a table of this contract

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the three fakes of section 12.8 and the document
    When the contract tests run
    Then each fake answers a path, a status and a body the document declares
    Then a fake that drifts from the document fails the build
    Then no schema, no example and no fake carries a name, an e-mail address or a personal field

  Scenario: AC7 Each business rule of section 8 is met by the document (new, D-RCV-60)
    Given the document and the business rules BR1 to BR9 of section 8
    When the contract review runs
    Then BR1 holds: every path begins with /api/recovery/access/v1 and no other service base appears
    Then BR2 holds: every consumed operation is declared as consumed with its owner from the ownership map
    Then BR3 holds: no reference table is declared and no lov_value, reference_version or reference_row row is written here
    Then BR4 holds: the load state is LOADED or REFUSED only
    Then BR5 holds: every failure uses one envelope and one message ID per condition
    Then BR6 holds: a usage refusal is 409 with valueCode and count
    Then BR7 holds: the document declares a 422 above a cap and no numeric limit of its own
    Then BR8 holds: the POST requires Idempotency-Key and the read declares it not applicable
    Then BR9 holds: no schema, example or fake carries a personal field

  Scenario: AC8 The GET operation answers 404 for a load that does not exist (new, D-RCV-60)
    Given the GET operation of the document for a load identifier
    When the contract review reads its responses for an unknown loadId
    Then the GET declares 404 for a loadId that names no load
    Then the 404 body uses the same envelope as AC3

  Scenario: AC9 A load runs its checks in order and a failing row is refused with 422 (new, D-RCV-60)
    Given the POST operation of the document and the load checks of AC2
    When the contract review reads the load checks and their failure answer
    Then the required English label is checked; the other checks and their order are Not specified in the source documents (GAP-0814)
    Then the Thai label is optional and is not a check
    Then a failing check is answered 422 with MSG-GEN-001 naming the field and the row
```

These six criteria test the artefact only. Neither of the two legacy criteria of RWB-AD-009 is restated here: they belong to RWB-P4-AD009-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's base or path | DP-13; Architecture v5 slide 41 |
| BR2 | A consumed operation is described as consumed, never as provided, and its owner comes from the ownership map | DP-11; Ownership Map v1 |
| BR3 | The document declares no reference table of its own and states that no `lov_value`, `reference_version` or `reference_row` row is written by this service | DP-01; ASM-0071; ASM-0041 |
| BR4 | A load state is one of LOADED and REFUSED; the later states of the version lifecycle belong to the owner and the approval story | TSD P4 v3 T3.2, T4; RWB-P4-AD010-APP |
| BR5 | Every failure uses one envelope and one message ID per condition, and the business texts are copied unchanged from the legacy story and the screen specification | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR6 | A usage refusal is declared as 409 with `valueCode` and `count`, because the count is the answer the administrator acts on (legacy AC2) | Legacy RWB-AD-009 AC2; ASM-1514 |
| BR7 | The caps are parameters, not constants: the document declares the 422 above a cap and never a numeric limit of its own; the parameter rows hold the file cap and the row cap, read through DP-06, Not specified in the source documents (GAP-0815), and the parameter keys are fixed at contract review | REQ-DRI-010; ASM-1516; GAP-0815 |
| BR8 | The load is idempotent on `Idempotency-Key`, and the header is required on the POST and not applicable on the read | Architecture v5 slide 11; R-UNI-40 |
| BR9 | No personal data in any schema, example or fake: a loader is a user reference and a group, never a name or a contact | Template and Rules §R7.2 s17; FSD P4 v3 A2.17.3.2 |

### 9. State transitions

The contract has its own lifecycle, and it also declares the state set of a load.

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the two schemas, the envelope and the consumed set are described | In review |
| In review | Consumer sign-off | The app story, the approval story, the screen route and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field, a status or a message ID is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a state is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

| Load state declared | Meaning in the contract | Who moves it on |
|---|---|---|
| `LOADED` | The owner stored the rows and versioned them; the load waits for the list owner's approval | The approval story, RWB-P4-AD010-APP |
| `REFUSED` | A check refused the file; nothing was stored | Terminal: a corrected file is a new load |

`APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK` and `VALIDATED` are values of LOV-VERSION-STATUS (TSD P4 v3 T3.2) and are not part of this document's answer for a load.

The SCR-40 Reference data screen states that the contract answers are Empty (an empty enabled-list answer with no error), Loaded (`LOADED`), Refused (`REFUSED`, or 422, or 409) and Waiting for approval (the `LOADED` answer and the approval step of RWB-P4-AD010-APP), as set out in section 16. The loading state, the error wording and the no-access state of SCR-40 are not declared in this story: the loading indication, the screen wording of an error, and the response to a call without the right declared in section 12.1 are Not specified in the source documents (DOR-RWB-P4-AD009-CON-10).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version, and confirms the console path once it is reconciled |
| Tech lead of rwb-case (P3) | Reviews the three consumed operations and owns their definitions, the list rows, the usage count and the versioning |
| Tech lead of the gateway-bff route | Reviews the two provided operations as the only ones the SCR-40 route calls |
| Data steward | Confirms that no personal data field is declared in a schema, an example or a fake |
| Security administrator, as the reader of the administration screens | Confirms that the C and R rights on Reference data are the ones the document declares (REQ-ACA-013; TSD P4 v3 T6.1) |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | Data field ID |
|---|---|---|
| `LovLoad` | `loadId`, `lovCode`, `validFrom`, `rowCount`, `checks[]`, `state` (LOADED, REFUSED), and on the read `loadedBy` as a user reference and `loadedAt` | Not specified in the source documents (DOR-RWB-P4-AD009-CON-7) |
| `LovLoadCheck` | `name`, `result` (PASSED, FAILED, NOT_RUN), `row` and `field` for a row check, and `detail` | Not specified in the source documents (DOR-RWB-P4-AD009-CON-7) |
| The load request | `multipart/form-data` part `file` (CSV or XLSX), query `lovCode` and `validFrom`, header `Idempotency-Key` | Not specified in the source documents (DOR-RWB-P4-AD009-CON-7) |
| The file | A header row and the columns `value_code`, `label_en`, `label_th`, `sort_order` and `valid_from`, which are the columns of `lov_value` DF-REF-027 to DF-REF-033 (TSD P4 v3 T3.1) | DF-REF-027 to DF-REF-033 |
| The usage refusal | `valueCode`, `count`, `messageId` MSG-GEN-004, and no case number and no case-level row; the source and scope of the count are Not specified in the source documents (GAP-0813) | Not specified in the source documents (DOR-RWB-P4-AD009-CON-7) |
| Event payload | The `REF-LOAD` or `REF-DENY` record: the decision code, the list code, the version, the row count, the check result and the time; no personal field | Not specified in the source documents (DOR-RWB-P4-AD009-CON-7) |

The exact type, length and required flag of each field of `LovLoad` and `LovLoadCheck` and the names of the check lines are Not specified in the source documents (GAP-0814; ASM-1515). The console path is `/api/recovery/access/v1/admin/lov-loads`; the rwb-case reference-load path and the field name (table or lovCode) are reconciled at contract review before the endpoint is frozen (GAP-0811; ASM-1512). This baseline fixes the field names above and leaves that detail to the review. The list-of-values versions are read through the owner's operation of section 12.2; the partner identity attributes and the refresh interval are Not specified in the source documents (GAP-1567).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/lov-loads` | `multipart/form-data` with the part `file` and the query parameters `lovCode` and `validFrom`; required `Idempotency-Key`; 201 with `LovLoad` in state LOADED or REFUSED | Reference data C |
| GET | `/admin/lov-loads/{loadId}` | 200 with `LovLoad`, its `checks[]`, its state, `loadedBy` and `loadedAt` | Reference data R |

Errors for both: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 409 usage refusal with `valueCode` and `count` (MSG-GEN-004, POST only), 422 a malformed request or a failed row check with `field` and `row` (MSG-GEN-001), 503 the record not written (MSG-P7-003) or the owner contract unavailable, and 404 an unknown `loadId` on the read. The POST is idempotent on `Idempotency-Key`; the read is not applicable and the document states that no consumer sends the header to it.

The document declares the path under the access base because the ownership map gives `POST /admin/reference-loads` and `GET /admin/lists/{listCode}` to P3 `rwb-case` (ASM-0041), and the console load is served by this service. Which of the two paths the Workbench console calls is Not specified in the source documents (GAP-0811; ASM-1512); the document names the access path and the review reconciles it before the baseline is frozen. The TSD's request field `table` is carried as `lovCode`, and the reconciliation covers the name as well.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | The load: the file, the list code and `validFrom`; the owner stores the rows, versions them and answers LOADED |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The list in force and the count of records using each value code |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access (own) | The capability area and letter answer behind the C and R checks |
| (library) | The parameters contract of rwb-case | P3 rwb-case | DP-06: the file-size cap, the row cap and the enabled lists |
| (library) | The reference-data contract of rwb-case | P3 rwb-case | DP-07: the list metadata and the version in force |

None of the P3 operations is declared as provided by rwb-access.

#### 12.3 Events published

No event of this service is published on `rwb.access.events.v1` for this capability: `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` are the service's two event types (Architecture v5 slide 41) and belong to the role, permission and delegation stories. The only message the load produces is `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, written by the DP-03 library in the transaction that produces the answer; the document declares its payload — the decision code `REF-LOAD` or `REF-DENY`, the list code, the version, the row count, the check result and the time — and declares no personal field in it.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 41 (events IN: none); the contract declares no subscription for the load.

#### 12.5 Workflows and activities

None. The load is synchronous and request-driven; the contract declares no workflow, no activity and no signal, and the `rwb-access` queue carries none of this capability.

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is a Schedule of `rwb-access` and belongs to another story; the contract declares no Schedule for the load.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role of the loader behind the C and R checks |
| `permission` | P4 (rwb_access) | The Reference data letters of that role |
| local decision record (DP-03 library) | PLT library, created in `rwb_access` | The `REF-LOAD` and `REF-DENY` entry a load writes |
| `outbox_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the record and the idempotency row of the key |
| `lov_value`, `reference_version`, `reference_row` | P3 (rwb_case) | Not declared as a table of this contract: reference data of P3 under ASM-0071, reached through the owner's operations of 12.2 |

The document declares no reference table and no list row of its own, and no table of another service appears as a table of this contract (DP-01, BR3).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-access lov-load WireMock (owned by this baseline) | `POST /admin/lov-loads` with 201 and load `RL-2026-014` in `LOADED`, `lovCode` LOV-ROUTE, `validFrom` 2027-01-01, `rowCount` 12 and the check lines; 201 with state `REFUSED` and a failed check on `label_en` at row 4; 409 with `valueCode` `R2` and `count` 37; 422 for a malformed multipart; 403 with MSG-P4-002; 503 with MSG-P7-003; `GET /admin/lov-loads/{loadId}` with 200 and with 404 | App story, screen route, contract tests, wave 4 harness |
| rwb-case reference-data WireMock | `POST /admin/reference-loads` answering `RL-2026-014` in `LOADED` with 12 rows; `GET /admin/lists/{listCode}` for LOV-ROUTE with 12 values in force and 37 open cases on `R2`; a 503 timeout | App story, contract tests, wave 4 harness |
| parameters fake | The file-size cap, the row cap and the enabled lists, as parameter rows | App story, contract tests |
| decision-record fake | The record append, the hash-chain check and a forced failure answering 503 with MSG-P7-003 | App story, contract tests |

Every fixture is synthetic; no fake carries a name, an e-mail address or a personal field.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed (plus 2 client libraries) | The console load and its read provided; the reference-load, the list read and the authorise consumed; one hop, 2 s timeout |
| Kafka | 1 message type declared, 0 consumed | `rwb.decision-record.DecisionRecorded.v1` written by the DP-03 library; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | None for this capability |
| File | 1 input | One multipart upload, CSV or XLSX; the caps are parameters |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-v1.yaml` with the two console operations and the shared components, the `LovLoad` and `LovLoadCheck` schemas, `contract/error-envelope.yaml`, the idempotency and versioning rules in the contract README, and the WireMock mapping sets of 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The contract carries the dependencies of the app story it serves and adds none of its own: by rule a CON story has no build dependency and starts on Day 1 (Template and Rules §R5.7).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem media type and the shared components; schema lint in the pipeline.
2. The two console operations with the shapes of section 11; the multipart request, the idempotency header and the two states.
3. The three consumed operations with their owners, the one-hop rule and the 2 s client budget, and the two client-library reads named as libraries.
4. The error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the 409 shape carrying `valueCode` and `count`.
5. The no-reference-table statement of AC5, with the ruling it rests on, in the document and in the README.
6. The fakes and the fixtures of 12.8.
7. The six contract tests, including the drift test that fails the build when a fake and the document disagree.
8. Baseline tag and the consumer sign-off note of the app story, the screen route, the P3 owner and the wave 4 harness.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD009-APP | The two provided operations, the two schemas, the envelope and the fakes |
| RWB-P4-AD010-APP | The `LOADED` answer and the record shape it reads when it approves the version |
| The gateway-bff route story (RWB-PLT-N001-CON) | The two operations as the only ones the SCR-40 route calls |
| RWB-P3-E1043-CON and RWB-P3-E1042-CON owners | The consumed operations as this service uses them; no P3 operation is claimed as provided |
| The wave 4 harness | The fakes and the fixtures of 12.8 |

**Done when.** The OpenAPI document validates in the pipeline, the six contract tests pass, every fake answers a path the document declares, and the app story, the approval story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the right calls an operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A malformed request, a row without `label_en`, a duplicate `value_code`, an unknown list code, a missing `valid_from`, a file above a cap, or a replayed key with another file | Enter {field}. |
| MSG-GEN-004 | A load would remove a value code in use | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the texts are the agreed texts of the legacy story and the SCR-40 screen specification and are copied unchanged. The 409 also carries `valueCode` and `count`, and the 422 carries `field` and `row`; the sentence the screen composes around the count is a screen matter and is Not specified in the source documents (GAP-0813; ASM-1514).

### 15. Screens and states

| Screen | State the contract serves | Contract element the screen consumes |
|---|---|---|
| SCR-40 Reference data | Empty | An empty enabled-list answer with no error, and the two operations still callable |
| SCR-40 Reference data | Loaded | `LovLoad` with state `LOADED`, the row count and the check lines |
| SCR-40 Reference data | Refused | `LovLoad` with state `REFUSED`, or 422 with `field` and `row`, or 409 with `valueCode` and `count` |
| SCR-40 Reference data | Waiting for approval | The `LOADED` answer, and the approval step which is the approval story's operation |
| SCR-40 Reference data | Versions | The list in force read through the owner's operation of 12.2, with the `lov_value` columns of the SCR-40 specification |
| SCR-40 Reference data | Loading | Not specified in the source documents (CG-ALL-4710) |
| SCR-40 Reference data | Error | Not specified in the source documents (CG-ALL-4710) |
| SCR-40 Reference data | No access | Not specified in the source documents (CG-ALL-4710) |

The screen is served by the gateway-bff composite route of DP-19, which calls the two operations of this contract and the owner's list read in parallel, one hop each, and merges the answers. The composite route specification and the field-level mapping are Not specified in the source documents (GAP-0811; ASM-1512); this contract fixes the access side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-009-CON-01 | AC1 | Contract | The OpenAPI 3.1 document validates; the base, the two operations, the multipart request, the five error responses and the GET 404 are present |
| TC-AD-009-CON-02 | AC2 | Contract | `LovLoad` and `LovLoadCheck` field sets; the state set is exactly LOADED and REFUSED |
| TC-AD-009-CON-03 | AC3 | Contract | 401, 403, 409, 422 and 503 carry one envelope, a valid message ID and, on the 409, `valueCode` and `count` |
| TC-AD-009-CON-04 | AC4 | Contract | The three consumed operations and the two client libraries carry their owner, one hop and the 2 s budget |
| TC-AD-009-CON-05 | AC5 | Contract | The no-reference-table statement, the ruling it names, and no reference table in any schema |
| TC-AD-009-CON-06 | AC6 | Contract | Each fake matches a declared path and body; a drifted fake fails the build; no personal field in any schema, example or fake |
| TC-AD-009-CON-07 | AC5 | Contract | Boundary: the tables of section 12.7 are the only owned tables; any further table in a schema fails the build |
| TC-AD-009-CON-08 | AC7 | Contract | Each rule BR1 to BR9 of section 8 is met: one base, consumed operations, no reference table, LOADED or REFUSED only, one envelope, 409 with valueCode and count, caps as parameters, Idempotency-Key, no personal field |
| TC-AD-009-CON-09 | AC8 | Contract | The GET declares 404 for an unknown loadId; the 404 body uses the AC3 envelope |
| TC-AD-009-CON-10 | AC9 | Contract | The English label check runs; the other checks and their order are Not specified in the source documents (GAP-0814); a failing check is 422 with MSG-GEN-001 naming the field and the row; the Thai label is optional |

No `-ITG` copy is written here: the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the enabled lists, the list codes and the caps stay reference data and parameters; the document declares the 422 above a cap and never a numeric limit.
- No personal data in a schema, an example or a fake: a loader is a user reference and a group, and no name, e-mail address or contact field is declared.
- The contract names only operations owned by rwb-access and only tables of `rwb_access` and of the platform library; the three P3 operations and the `lov_value` rows are consumed and documented as consumed (DP-01, ASM-0071, ASM-0041).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- Every example is synthetic; no production payload or list extract is copied into a schema or a fake.
- The error envelope, the problem media type and the naming rule come from the platform library; this contract narrows them but never redefines them.
- A usage refusal is declared with its count, so the screen can tell the administrator what the removal would break (BR6).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-011 | A reference data service holds every versioned table with valid-from and valid-to, author and approver | The load's `validFrom` and `rowCount`, the consumed reference-load and list reads, and the statement that the owner versions the rows | TC-AD-009-CON-02, TC-AD-009-CON-04, TC-AD-009-CON-05, TC-AD-009-CON-07 |
| REQ-DRI-010 | A parameter catalog holds every threshold and limit, versioned, changed without a code release | The caps declared as parameter reads of DP-06 and the 422 above a cap | TC-AD-009-CON-04 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The two console operations the SCR-40 route calls and their C and R rights | TC-AD-009-CON-01, TC-AD-009-CON-03 |

| Legacy reference | Where it is kept |
|---|---|
| The `lov_value` fields DF-REF-027 to DF-REF-033 as the file columns | Section 11 |
| AC1 and AC2, the valid load and the code-in-use refusal | RWB-P4-AD009-APP; the 409 shape of sections 7 and 12.1 |
| The legacy message table MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | Section 14, with MSG-GEN-004 of the SCR-40 specification |
| SCR-40 Reference data with the versions and the load | Sections 12.1 and 15 |
| The legacy test cases TC-AD-009-01 to TC-AD-009-04 | RWB-P4-AD009-APP, section 16 |

### 19. Out of scope

- The implementation of the two operations, the parser, the checks and the record (RWB-P4-AD009-APP).
- The approval, verification and rollback of a load and their operations (RWB-P4-AD010-APP on the owner's contract).
- The `lov_value` table, `reference_version`, `reference_row` and the reference-load and list operations themselves: P3 `rwb-case` under ASM-0071 and ASM-0041.
- The rule-version read and approve that the legacy story carried, and SCR-39 Rules and parameters: P7 `rwb-decision` under ASM-0040 and RWB-P4-AD011-APP in this service epic.
- The composite route implementation, the screen build and the masking of customer fields on other screens.
- Deployment of this capability: the Helm values, the topic subscription, the dashboards and the runbook.
- The cross-service journey harness and its evidence (RWB-ITG-W4), and a `-ITG` copy of any test case.
