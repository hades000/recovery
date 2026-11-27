# RWB-P4-AD007-CON Access log search and export

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD007-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P4-AD007-CON-16) |
| Contract version | v1 (major version 1 in the path /api/recovery/access/v1) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-007 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 11 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the access-log search and export of `rwb-access`: an OpenAPI 3.1 document for the two reads, the `AccessLogEntry` and `AccessLogPage` schemas, the query parameters and their bounds, the CSV column order, one RFC 9457 error envelope with its message IDs, the consumed authorise, parameters and reference-data operations with their owners, one hop and the 2 s budget, the contract tables of section 12 and the contract fakes**, so that **the app story, the integration harness and every consumer of the access log can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, `rwb-case` or the central ledger to be built**.

This contract carries no legacy acceptance criterion: AC1 to AC5 of RWB-AD-007 belong to RWB-P4-AD007-APP, and the six criteria of section 7 test the document, the schemas, the envelope, the consumed declarations and the fakes.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story answered the access-log query from one table of the monolith, so the shape of the answer, the paging and the masking were decided by whichever screen asked. In the target the entry is written by `rwb-access` in its own schema as a decision-record entry of DP-03, hash-linked and collected centrally within five minutes (Architecture v5 slide 28; ADR-022), and the search is one operation of the owner. An audit consumer, the gateway-bff route and the integration harness each need that answer to mean the same thing, including the two version fields and the CSV column order, or every one of them will invent its own.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the platform library, the parameters and reference-data contracts of `rwb-case` and the ledger work of P7, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline also fixes the one thing audit asks of it: every answer states the matrix version and the masking version its entries were read under, so a printed answer can be defended years later without re-reading the source system.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the two reads, and it is a consumer of this baseline.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The access entry is a decision-record entry of the DP-03 library (RWB-PLT-E1027-CON), written by RWB-P4-E1039-APP; this document describes the entry as that schema publishes it and adds no field.
- The operations and their owners are taken from the ownership map only: `GET /admin/access-log` is P4's, and the authorise, parameters and reference-data operations this document consumes are P4's and P3's. No table of another service is named (DP-01).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two reads with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the paging parameters and the entry schema.
2. Fix the `AccessLogEntry` and `AccessLogPage` schemas and the six query parameters, with the page default 50, the page maximum 200 and the export cap 10,000 held as parameter rows behind the contract.
3. Fix the CSV column order of the export and the masking fields the file declares, so the file can never be less masked than the screen.
4. Agree the error envelope and the message-ID mapping for 401, 403, 422 and 503, with the business texts copied unchanged from the legacy story where the message already existed.
5. Declare the consumed authorise, parameters and reference-data operations as consumed, each with its owner, one hop and the 2 s client budget.
6. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
7. Add the contract tests: schema validation, the entry and page shapes, the CSV order, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
8. Tag the baseline and hand it to RWB-P4-AD007-APP, the Epic 8 screen work of RWB-PLT-N001-CON and the integration harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC5 |
| X3 | A response of 401, 403, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A CSV column is missing, reordered or unmasked where the screen masks it | The contract test fails; the file may never be less masked than the screen | None | AC3 |
| X5 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X6 | An example, a fake or a schema carries a name, an e-mail address or a personal field | The review and the pipeline refuse the document | None | AC6 |
| X7 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X8 | The page bounds or the cap change | The parameter row changes and the document's defaults are restated; no schema change and no new major version | None | AC2 |
| X9 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |
| X10 | The query matches no entry | The page returns no items with total 0; the screen shows the empty state | None | AC2 |
| X11 | The read is waiting for its answer | The screen shows the loading state and no entry until the page or the file arrives | None | AC2, AC3 |
| X12 | The read fails with 401, 403, 422 or 503 | The screen shows the problem envelope of the response and no partial entry | The message ID the response carries (section 14) | AC4 |
| X13 | The caller has no Platform administration R | The screen shows no entry and the 403 refusal | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the DP-03 entry schema and the P3 and P4 contracts only |
| Negotiable | The CSV column order and the cap are settled with audit and the integration harness; the base, the operations, the names and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the screen route and the harness on Day 1, and keeps the central ledger out of the `rwb-access` contract |
| Estimable | One OpenAPI document, one error envelope, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Access log search and export contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access-log half of the legacy journey is the search and the export over the local decision-record chain

  Scenario: AC1 The OpenAPI 3.1 document describes the two reads (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the access log is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares GET /admin/access-log and GET /admin/access-log/export with the owner rwb-access
    Then every operation names its security right, Platform administration R, and its error responses 401, 403, 422 and 503
    Then no operation of another service is declared as provided by rwb-access
    Then no field is removed, renamed or retyped within major version 1

  Scenario: AC2 The entry, the page and the query parameters are fixed (new, D-RCV-60)
    Given the AccessLogEntry and AccessLogPage schemas of the document
    When the document is read against the entry and page schemas and the query declaration
    Then the entry carries decisionCode as one of AC-READ, AC-DENY and AC-EXPT, actorReference, capabilityArea, right, caseReference, documentReference, dataProductReference, roleCode, matrixVersion, maskingVersion, grantId, incidentReference and decidedAt
    Then the page carries items, page, size, total, matrixVersion, maskingVersion, chain, coveredFrom and coveredTo
    Then the query declares user, from, to, event, capabilityArea, page and size
    Then page defaults to 50 and size is capped at 200, read from the parameters contract and never from code
    Then from and to are required and a period that ends before it starts is refused

  Scenario: AC3 The export declares the column order and the same masking (new, D-RCV-60)
    Given the export operation of the document
    When the export operation is read and compared with the screen declaration
    Then its answer is text/csv in UTF-8 with one header row
    Then the columns are decided_at, decision_code, actor_reference, capability_area, right, case_reference, document_reference, data_product_reference, role_code, matrix_version, masking_version, grant_id, incident_reference
    Then the screen declares the same columns in the same order, so the file carries the same masking fields as the screen
    Then the cap is 10,000 rows and the response above it is 422 with no file

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 422 or 503 response is produced by either read
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002
    Then 422 carries MSG-GEN-001 or MSG-GEN-003 and 503 carries MSG-P7-003
    Then no operation declares a second error shape

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation, the parameters read and the reference-data read this service calls
    When the consumed operations are read from the document and each owner is checked
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters and GET /api/recovery/case/v1/admin/lists/{listCode} are declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then no operation owned by rwb-case or by rwb-decision is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then no schema, example or fake carries a name, an e-mail address or a personal field

  Scenario: AC7 The document names only the owned tables (new, D-RCV-60)
    Given the owned tables of section 12.7 of this story
    When the document is read for table names
    Then it names the tables role, permission, masking_rule and the local decision-record table only
    Then it names no table of another service and no central ledger

  Scenario: AC8 A provided read answers 404 as one problem envelope with no list (new, D-RCV-60)
    Given the two reads of the document are provided by rwb-access
    When a provided read answers 404
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then its messageId is Not specified in the source documents (NEWAC-RWB-P4-AD007-CON-AC8)
    Then no operation declares a second error shape
```

These eight criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-AD-007 belong to RWB-P4-AD007-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1, AC5; TC-AD-007-CON-01, TC-AD-007-CON-05 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5; TC-AD-007-CON-05 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4; TC-AD-007-CON-04 |
| BR4 | The entry is the decision-record entry of DP-03: the contract describes it and adds no field | DP-03; RWB-PLT-E1027-CON | AC2; TC-AD-007-CON-02 |
| BR5 | The contract declares no table of another service and no central ledger; `decision_log_entry` is P7's | DP-01; ASM-A6-tables | AC7; TC-AD-007-CON-07 |
| BR6 | The export can never be less masked than the screen, and the masking version of the entry decides the rendering | DP-07; NFR-039 | AC3; TC-AD-007-CON-03 |
| BR7 | The page bounds and the export cap are parameter rows behind the contract, never constants in code | DP-06; BR-P4-016 | AC2, AC3; TC-AD-007-CON-02, TC-AD-007-CON-03 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC1; TC-AD-007-CON-01 |
| BR9 | No personal data in a schema, an example or a fake: references, codes, versions and times only | NFR-040; DP-05 | AC6; TC-AD-007-CON-06 |
| BR10 | Every answer states the chain it read and the period it covers, so a printed answer is defensible | FSD P4 v3 A2.16; ASM-1502 | AC2; TC-AD-007-CON-02 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the entry and page schemas, the envelope and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the gateway-bff route and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A parameter row changes | The page bound or the cap changes | Baselined, with the defaults restated in the document |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the entry and page schemas, the envelope and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Audit representative and the integration and QA team | Review and sign off the entry fields, the versions in the answer, the CSV column order and the cap |
| Tech lead of rwb-case (P3) | Reviews the parameters and reference-data operations as rwb-access uses them; owns their definitions |
| Security administrator and the platform owner of the authorise contract | Review the security right of both reads and the refusal mapping with MSG-P4-002 |
| Data steward | Confirms that no personal data field is declared in the entry, the examples or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

The access-log search reads the local decision-record chain of rwb_access only, and every answer states the chain and the period it covers; the end-to-end view of the central ledger belongs to the integration story.

| Item | Content | BR Field ID |
|---|---|---|
| Access entry | `decisionCode`, `actorReference`, `capabilityArea`, `right`, `caseReference`, `documentReference`, `dataProductReference`, `roleCode`, `matrixVersion`, `maskingVersion`, `grantId`, `incidentReference`, `decidedAt`, from the decision record DF-DEC-003, DF-DEC-002 (empty for an access event), DF-DEC-008, DF-DEC-014 and DF-DEC-016 | BR4 |
| Access page | `items[]` of the entry, `page`, `size`, `total`, `matrixVersion`, `maskingVersion`, `chain`, `coveredFrom`, `coveredTo` | BR10 |
| Query | `user` (staff user reference; no name is accepted, displayed or logged), `from`, `to`, `event`, `capabilityArea`, `page`, `size`; `page` default 50, `size` maximum 200 | BR7, BR9 |
| CSV answer | `text/csv` UTF-8, one header row, the thirteen columns of AC3, the same masking as the screen, 10,000 rows maximum | BR6 |
| Masking declaration | `matrixVersion` and `maskingVersion` on every entry and on the page, so the file's masking version is the entry's; the fields the role sees unmasked come from `masking_rule` DF-REF-198 to DF-REF-204 and are read by the owner, not by the consumer | BR6 |
| Refusal | `messageId` MSG-P4-002 or MSG-GEN-001 or MSG-GEN-003 with the field list, and MSG-P7-003 for the record failure | BR3 |

The field-level detail of the access facts inside the existing entry — types, lengths, required flags, the sort parameters and the exact CSV header order the review will accept — is Not specified in the source documents (GAP-0801; ASM-1502) and is confirmed with audit and with the entry schema of RWB-P4-E1039-APP before the endpoint is frozen. The export format, its columns and its cap are Not specified in the source documents (GAP-0802; ASM-1503) and are fixed by AC3 and section 12.1.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/admin/access-log` | AccessLogPage: query `user`, `from` (required), `to` (required), `event`, `capabilityArea`, `page` (default 50), `size` (max 200); items of the entry of section 11, with `matrixVersion`, `maskingVersion`, `chain`, `coveredFrom` and `coveredTo` | Platform administration R, scope applied |
| GET | `/admin/access-log/export` | `text/csv`, UTF-8, one header row, the column order of AC3, the same rows in the same order and the same masking as the search; cap 10,000 rows | Platform administration R, scope applied |

Errors for both: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 422 a required field empty or a code not in its list (MSG-GEN-001) and a period that ends before it starts (MSG-GEN-003) and the export over the cap, 503 the entry of the read cannot be written (MSG-P7-003). Both are reads, so the Idempotency-Key rule of every POST does not apply and the baseline states it so that no consumer sends the header. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration R check behind both reads, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The page default 50, the page maximum 200 and the export cap 10,000, with the version in force (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-CAPABILITY, LOV-EVENT and LOV-SCOPE with the version in force (DP-07) |

None of the three is declared as provided by rwb-access, and no operation of `rwb-decision`, `rwb-document` or the central ledger appears in the document at all.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a search (AC-READ), of a refusal (AC-DENY) and of an export (AC-EXPT) with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

The access event writer is RWB-P4-E1039-APP and the policy change event `rwb.access.AccessPolicyChanged.v1` is RWB-P4-E1037-APP's; this document declares the record message only, because it is the only event of the two reads.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and the read of the local chain needs no subscription.

#### 12.5 Workflows and activities

None. No workflow and no activity is part of this contract, and the `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only.

#### 12.6 Schedules

None. Both reads are request-driven.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role code an entry carries |
| `permission` | P4 (rwb_access) | The Platform administration R letter and the matrix version |
| `masking_rule` | P4 (rwb_access) | The masking version and the field list that apply to an entry |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The entry the document describes, and the entries the two reads append |

No table of another service is named in the contract (DP-01): `decision_log_entry` is P7 rwb_decision's, `case` and `assignment` are P3's, `document` is P5's, and `lov_value`, `reference_version` and `reference_row` are P3 reference data read through DP-07. The case, document and data-product references in an entry are values, not foreign keys.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| authorise fake | `POST /authorise` with a granted answer for RW-AUDIT, RW-COE and RW-PLATADM with Platform administration R, and a refused answer with MSG-P4-002 for RW-PHONECOL | App story, contract tests, harness |
| decision-record fake | A seeded chain of a week under matrix version MAT-2026.11 and masking versions MSK-2026.11 and MSK-2026.10, with AC-READ, AC-DENY and AC-EXPT entries, one grant entry with grant id BG-2026-000412 and incident INC0004521, the append, the hash-link check and a forced failure | App story, contract tests |
| parameters fake | `GET /admin/parameters` with the page default 50, the page maximum 200 and the cap 10,000 | App story, contract tests |
| reference-data fake | `GET /admin/lists/{listCode}` for LOV-CAPABILITY, LOV-EVENT and LOV-SCOPE at version REF-2026.11 | App story, contract tests, harness |
| gateway-bff fake | The composite route of SCR-43 with the access-log panel and the export state, calling the two reads | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The search and the export provided; the authorise, parameters and reference-data reads consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | 1 CSV answer | The export response; no file input and no file store |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-accesslog-v1.yaml` (OpenAPI 3.1) with the two reads and the shared components, `contract/error-envelope.yaml`, the `AccessLogEntry` and `AccessLogPage` schemas with their examples, the CSV column contract in the contract README, the paging and versioning rules, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none: the contract declares no ACE field, and the group of an actor reference stays behind the owner's own view |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The two reads with the shapes of section 11; the entry, the page, the query parameters and their bounds.
3. The CSV column contract with the thirteen columns, one header row, the masking fields of the screen and the cap of 10,000 rows.
4. The consumed operations with their owners, the one-hop rule and the 2 s client budget.
5. The error envelope and the message-ID mapping, with the business texts copied unchanged from the legacy story.
6. The five fakes and the stub fixtures of section 12.8.
7. The six contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note from the app story, the screen route and the harness.

**Feature switch.** Both reads are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; the document declares no 404 branch of its own and adds no parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD007-APP | The two provided reads, the entry and page schemas, the CSV column order and the five fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-43) | The two reads as the panel and the export state call them |
| The integration harness of the wave 4 access journey | The entry fields, the two version fields and the fakes, as the evidence it records |

The retention of an access entry — and with it the retention of the fakes that carry one — is Not specified in the source documents (GAP-0805; ASM-1506); it follows the decision log's retention rule, and the deprecation window of a published field is the versioning rule of BR8.

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every declared path, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | Your session has ended. Sign in again to continue. |
| MSG-P4-002 | A role without Platform administration R reads either operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, a user value is not a staff user reference, or a code is not in its list | Enter {field}. |
| MSG-GEN-003 | The period ends before it starts | {field} cannot be before {other}. |
| MSG-P7-003 | The entry of the read cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. The export cap response is a 422 of the same envelope, and its message is Not specified in the source documents (GAP-0802; ASM-1503).

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access | Access log, list | The page with the entries, `matrixVersion` and `maskingVersion`, paged at 50 and at most 200 |
| SCR-43 Roles and access | Access log, filtered | The same page narrowed by `user`, `from`, `to`, `event` and `capabilityArea`, validated against LOV-CAPABILITY, LOV-EVENT and LOV-SCOPE |
| SCR-43 Roles and access | Access log, empty | An empty `items` with total 0 and no error |
| SCR-43 Roles and access | Export | The `text/csv` answer with one header row, the same columns, the same order and the same masking as the screen |
| SCR-43 Roles and access | Export over the cap | The 422 of the envelope with no file |
| SCR-43 Roles and access | Break-glass warning | The warning of the answer, shown as the MSG-P4-004 banner over the list |
| SCR-43 Roles and access | Refused | The 403 of the envelope with MSG-P4-002 and no list |
| SCR-43 Roles and access | Loading | Not specified in the source documents (CG-ALL-4665) |
| SCR-43 Roles and access | Error | Not specified in the source documents (CG-ALL-4665) |
| SCR-43 Roles and access | No access | Not specified in the source documents (CG-ALL-4665) |

The screens are served by the gateway-bff composite route (DP-19), which calls the two reads and the session read in parallel, one hop each, and merges the answers. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work; the document fixes the access-log side of the merge only, and the masking version on each entry is what the route renders with.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-007-CON-01 | AC1 | Contract | The document validates; the base, the two reads, Platform administration R and the four error responses are present; no foreign operation is provided; no field is removed, renamed or retyped |
| TC-AD-007-CON-02 | AC2 | Contract | The entry and page schemas and the six query parameters, with page 50 and size 200 |
| TC-AD-007-CON-03 | AC3 | Contract | The thirteen CSV columns in order, one header row, the same masking fields as the screen and the cap of 10,000 rows with 422 above |
| TC-AD-007-CON-04 | AC4 | Contract | A 401, 403, 422 and 503 response carry one problem envelope with a valid message ID |
| TC-AD-007-CON-05 | AC5 | Contract | Three consumed operations with their owners P4 and P3, one hop and the 2 s budget; none declared as provided |
| TC-AD-007-CON-06 | AC6 | Component | The five fakes match the document; a drifted fake fails the build; no name, e-mail address or personal field |
| TC-AD-007-CON-07 | AC7 | Contract | The owned tables of section 12.7 only; no table of another service and no central ledger is named |
| TC-AD-007-CON-08 | AC8 | Contract | A 404 answer of a provided read carries one problem envelope with messageId Not specified in the source documents (NEWAC-RWB-P4-AD007-CON-AC8) |

### 17. Guardrails

- No business value in the contract: the page bounds, the cap, the capability areas, the events and the scopes stay parameter rows and reference data behind the document.
- No personal data in a schema, an example or a fake: staff user references, codes, versions and times only (BR9).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the ledger, the case, the document and the reference tables are consumed or absent, never named as this service's (DP-01, BR5).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The export can never be less masked than the screen, and the masking version of the entry is the one the file and the route use (BR6).
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-006 | Every read is written to the access log, and the log is readable | The two reads, the entry schema and the `rwb.decision.DecisionRecorded.v1` declaration; the writer itself is RWB-P4-E1039-APP's | TC-AD-007-CON-01, TC-AD-007-CON-02 |
| REQ-ACA-007 | An access outside the matrix is refused and the refusal is recorded | The 403 with MSG-P4-002, the authorise operation as consumed and the AC-DENY code in the entry | TC-AD-007-CON-04, TC-AD-007-CON-05 |
| REQ-DRI-012 | Audit can query the record and receive it with versions and the final call | `matrixVersion`, `maskingVersion`, `chain` and the period on the page; the CSV columns of AC3 | TC-AD-007-CON-02, TC-AD-007-CON-03 |
| REQ-ACA-013 | The administration screens for roles, permissions and delegation are available to the security administrator | The reads as the SCR-43 route consumes them, and the room the page leaves for the reference lists in force | TC-AD-007-CON-01, TC-AD-007-CON-05 |

The requirement IDs are taken from the FSD feature table and the Program BRD under the fill order of Template and Rules §R7.3, because the Work Package carries the requirement list of this story empty; the set is fixed by the FSD "Requirements served" rows and does not change.

### 19. Out of scope

- The implementation of the search and the export (RWB-P4-AD007-APP).
- The access event writer, the entry shape and the break-glass grant (RWB-P4-E1039-APP), and the matrix and masking policy (RWB-P4-E1037-APP); this document consumes their shapes.
- The central ledger, the query API over `rwb_decision` and the chain verification (P7 rwb-decision).
- The screen SCR-43 Roles and access, its other panels and its composite route specification (RWB-PLT-N001-CON and the Epic 8 screen work).
- The access review list and its Schedule (RWB-P4-AD008-APP).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the `rwb-case` parameters and reference-data contracts and the authorise operation are consumed and faked, never defined here.
- The cross-service journey harness and its evidence.
