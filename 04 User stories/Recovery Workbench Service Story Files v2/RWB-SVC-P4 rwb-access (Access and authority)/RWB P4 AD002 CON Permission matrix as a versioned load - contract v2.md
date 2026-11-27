# RWB-P4-AD002-CON Permission matrix as a versioned load

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-002 for rwb-access — the contract of the permission matrix as a dated version: the load with its whole-file checks, the version status before approval, the effective-from date, the matrix read, the version read, the versions list and the access-policy event. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-AD002-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (27 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD002-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Contract version | 1 (major version 1, base /api/recovery/access/v1; see BR14) |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP08, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-AD002-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **tech lead**, I want **the published contract baseline of the permission matrix as a versioned load — an OpenAPI 3.1 document for the load, the matrix read, the version read and the versions list, the `PermissionMatrix`, `PermissionMatrixRow`, `PermissionMatrixVersion` and `PermissionMatrixPage` schemas with the status and the effective dates, the whole-matrix rule, the rule that a version takes effect only when approved and only from its valid-from date, the `rwb.access.AccessPolicyChanged.v1` declaration with change kind `MATRIX`, one RFC 9457 error envelope, the consumed parameters and reference-data reads and the read-only ACE group view, the contract tables of section 12 and the fakes**, so that **the app story builds on Day 1 against a fixed, testable contract, and every consumer knows which version of the matrix it is checked against and on which date**.

The deliverable is the matrix **as a dated version**: the load, the two reads, the list and the event that tells the services a version was loaded. The approval is not contracted here — it is RWB-P4-AD010-APP's on the reference-load path and RWB-P4-AD010-CON declares the console side — and the enforcement of the letters is RWB-P4-E1037-CON's guard.

### 2. Business rationale

Contract-first REST, one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the monolith the matrix was a table read in the same connection, and a change of rights was a release or a manual data fix nobody outside the team could describe. In the target the matrix is rows of P4's own `permission` with a label, a status and an effective date, so the two answers that matter — which letters does this role hold on this date, and which version is in force — are written down once, with their fields, rights, versions and event.

The first consequence is the whole-file check. A row-level check would accept a file that silently omits a role, and an omitted role removes a right from every person holding it; the contract states that a complete matrix holds every active role once against each of the 14 areas of LOV-CAPABILITY, that a file with any gap is refused in full and that the missing role is named, because the refusal text and the message identity are what the administrator acts on.

The second consequence is the split between loading and taking effect. A loaded version is not a permission change: it is a proposal that waits for the approval of RWB-P4-AD010-APP and changes no answer until it is approved **and** its valid-from date has arrived. Both states use LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) of TSD P4 v3 T3.2, the vocabulary the reference loads and the rule packages use, so the service has one answer to "which value was in force when".

The third consequence is one event name. `rwb.access.AccessPolicyChanged.v1` is the one access-policy event the architecture gives `rwb-access` (Architecture v5 slides 14 and 43), services already refresh their cached permission data on it (slide 20), and a matrix load **is** an access-policy change; the payload carries the version, its status and its effective date and no letter of a role.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the base, topic and event names follow the platform rule rather than a local choice.
- The guard contract is published: RWB-PLT-E1037-CON and RWB-P4-E1037-CON fix the authorise contract and the library (DP-08) through which every operation demands its letter; the dependency is carried by RWB-P4-AD002-APP.
- RWB-PLT-E1027-CON is published: the decision-record library and topic `rwb.decision-record.v1` (DP-03), whose `AC-VERS` entry records every load; carried by the app story.
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters library and contract (DP-06), through which the approver role is read; carried by the app story (ASM-3728).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data library and contract (DP-07), through which LOV-CAPABILITY and its 14 values are read; carried by the app story.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that serves SCR-43 and merges the matrix read with the access-log read; carried by the app story.
- `v_ace_iam_group` (DF-ACE-301 to DF-ACE-304) is granted and contracted by RWB-P1-E1069-APP (DP-05); this document declares it as a read-only consumed read with its `data_as_of`.
- The version status, the effective dates and the approver reference are this key's own decision (GAP-2263; GAP-0789; ASM-3727): `permission` in TSD P4 v3 T3.1 carries `matrix_version` (DF-REF-044) and the standard `state` column (T3.0) and no date column, while legacy AC3 needs an approved version with a valid-from. This document fixes the field names and types of the four schemas; the physical columns of the valid-from, valid-to and approver-reference fields are added by this key's migration (GAP-2263; GAP-0789).
- The four operations have no ownership-map row and no T-A row, which holds only `GET /admin/roles` (API-P4-007), `GET /admin/access-log` (API-P4-008) and the reference-load paths (API-P4-005, API-P4-006, API-P4-009, API-P4-010) — **Not specified in the source documents (GAP-2264; ASM-1453)**.
- The rights are Platform administration in TSD P4 v3 T6.1 — `R` for the reads and `C` for the load, held by RW-SECADM (CRUDA) and RW-PLATADM (CRUD) — and the legacy rows "Reference data C: RW-COE, RW-REFADM" and "Rules and parameters A: RW-RISK" are not kept: the matrix is role administration, `permission` is P4's, and reference data is P3 rwb-case's (ASM-1454).
- The approval is not this document's: the legacy criterion names "the application owner's approval", TSD P4 v3 T6.1 holds no application-owner role, and the approval of a loaded version is RWB-P4-AD010-APP's with the approver role read from `rwb.refload.approver.permission=RW-SECADM` (ASM-3728).
- The completeness rule is a rule and not a count: the count is computed from `role` and LOV-CAPABILITY, and the labels `PM-2026.11`, `PM-2026.12` with 756 rows and the refused `PM-2026.13` are the values of FSD P4 v3 AC-P4-004-01 and of the fakes (ASM-3729).
- No build dependency: Day 1 by rule (Template and Rules §R5.7), in contract group CG-W4 because business epic EP08 is wave 4 in the W-MAP (§R5.6).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the four matrix operations under `/api/recovery/access/v1`, with the shared components the `rwb-access` operations use.
2. Draft `PermissionMatrix`, `PermissionMatrixRow`, `PermissionMatrixVersion` and `PermissionMatrixPage`: role code and name, class, default scope, area, letters, version label, status, valid-from and valid-to, row and role counts, author and approver references, decision-record reference, the role the version waits for and the page of rows.
3. State the completeness rule: one row for every active role against each of the 14 areas; an omitted role, a repeated pair and a letter outside the vocabulary are one refusal with the gap named, and the whole file is refused.
4. State the load-and-approve-before-effective rule: the load writes VALIDATED and no more; a version is APPROVED only through the gate of RWB-P4-AD010-APP and in force only from its valid-from date after that approval; an applied version is never edited and a change is a new dated version.
5. State the version-in-force rule: the matrix read answers the version whose valid-from is the latest not after the date asked and whose status is APPROVED or IN_FORCE, one version whole; a VALIDATED version is never answered as the matrix in force.
6. State the rights: Platform administration `R` for the three reads and `C` for the load, with an active role on every call and the 401 and 403 of the default deny rule.
7. Agree the error envelope and the message mapping for 401, 403, 404, 409, 422 and 503, with the business texts copied unchanged from the legacy story where the message exists, except MSG-GEN-006, which takes the text of the Error and Message Standard v4.
8. Declare `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` with change kind `MATRIX`, the version, the status, the effective date and the row count, and the decision-record type on `rwb.decision-record.v1`; declare no third event name.
9. Declare the consumed parameters read, the consumed reference-data read and the read-only ACE view with their owners and the one-hop budget, and declare no operation of another service as provided.
10. Publish the contract tables of section 12 and the fakes, then add the contract tests: schema validation, the whole-matrix rule, the version and date rule, the rights, the envelope, the owner declarations and the drift between a fake and the document.
11. Tag the baseline and hand it to RWB-P4-AD002-APP, to RWB-P4-AD010-APP for the approval side and to RWB-P4-E1037-CON and RWB-P4-E1037-APP, whose guard checks every endpoint against the version this document declares.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A schema declares a person's name, an e-mail address or the letters of a named individual | The review fails and the property is removed | None | AC2 |
| X3 | A field of the matrix or the version has no source definition | The field is named by this document's own decision and the gap is carried | None | AC2 |
| X4 | The document declares a load that approves, or a version in force with no valid-from date | The review fails: the load writes VALIDATED, the approval is another gate, an applied version is never rewritten | None | AC3 |
| X5 | The document declares another event name, or a second access event for a matrix load | The review fails; the event is `rwb.access.AccessPolicyChanged.v1` with change kind `MATRIX` | None | AC4 |
| X6 | The document declares an operation or a table of another service as provided | The review fails; the parameters read, the list read and the ACE view are documented as consumed | None | AC5 |
| X7 | An error response carries no `messageId`, or one outside the agreed set | The contract test fails and the merge is blocked | None | AC6 |
| X8 | A fake drifts from the document | The contract test fails and the merge is blocked | None | AC7 |
| X9 | The parameters read, the reference read or the ACE view misses the 2 s budget | The call answers 503 and the document declares the 503 | MSG-GEN-006 | AC5, AC6 |
| X10 | The document declares a complete matrix as a fixed row count | The review fails: the count is computed from `role` and LOV-CAPABILITY, never a constant | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; it reads the ownership map, the platform envelopes, the guard contract, the parameters and reference-data contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON and the ACE-view contract of RWB-P1-E1069-APP |
| Negotiable | The field-level detail of the four schemas and the payload are settled with the app story and the approval story; the base, rights, event name and envelope are fixed by the architecture and the Workbench |
| Valuable | Unblocks the app story on Day 1 with a written answer to "which letters does this role hold on this date, and which version is in force", and keeps the approval, the masking rules and the roles catalogue out of the matrix contract |
| Estimable | One document, four schemas, one error envelope with seven message IDs, one event declaration, nine contract tables, six fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: The permission matrix as a versioned load, contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the permission matrix is the "permission" rows of one "matrix_version" of one environment in "rwb_access"
    Given a complete matrix holds every active role once against each of the 14 capability areas of "LOV-CAPABILITY"

  Scenario: AC1 The OpenAPI 3.1 document describes the four matrix operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/permission-matrix-loads, GET /admin/permission-matrix, GET /admin/permission-matrix-versions and GET /admin/permission-matrix-versions/{matrixVersion} with the owner rwb-access
    Then the three reads declare Platform administration with the right R, and the load declares Platform administration with the right C
    Then every operation declares 401, 403, 404, 409, 422 and 503
    Then the load declares the Idempotency-Key header and the three reads declare none

  Scenario: AC2 The four schemas carry the matrix, the version and the dates (new, D-RCV-60)
    Given the schemas PermissionMatrix, PermissionMatrixRow, PermissionMatrixVersion and PermissionMatrixPage of the document
    When the rwb-access document is published and its four schemas are checked against the matrix rules
    Then PermissionMatrixRow carries roleCode, roleName, roleClass, defaultScope, capabilityArea, letters and matrixVersion
    Then PermissionMatrix carries matrixVersion, versionStatus, validFrom, validTo, validOn, rowCount and the rows
    Then PermissionMatrixVersion carries matrixVersion, versionStatus, validFrom, validTo, rowCount, roleCount, capabilityAreaCount, authorReference, approverReference, decisionRecordEntryRef, pendingApproverRole and the rows
    Then PermissionMatrixPage carries items, page, size and total with a default of 50 and a maximum of 200
    Then the letters are declared as C, R, U, D and A in that order or a dash, and the version status is declared with the values of LOV-VERSION-STATUS
    Then no schema, no parameter and no example declares a person's name, an e-mail address, an identity number or the letters of a named individual
    Then the valid-from and valid-to dates, the approver reference and the pending approver role are declared as fields of the version, because no physical column is specified for them in the source documents

  Scenario: AC3 The whole-matrix rule and the load-and-approve-before-effective rule (new, D-RCV-60)
    Given the description of the load operation and of the three reads
    When the rwb-access document is published and the description of the load and of the three reads is reviewed
    Then the load declares that a complete matrix holds exactly one row for every active role against each of the 14 areas of LOV-CAPABILITY
    Then the load declares that a file with a missing role, a repeated role and area pair or a letter outside the vocabulary is refused in full with the gap named, and that no row of a refused version is stored
    Then the load answers the version VALIDATED, and the document states that the approval of a version is not the load and belongs to the gate of RWB-P4-AD010-APP
    Then the document states that a version is in force only when it is APPROVED and only from its valid-from date, and that an applied version is never edited
    Then the matrix read answers the version whose valid-from is the latest not after the date asked and whose status is APPROVED or IN_FORCE
    Then the document states that a VALIDATED version is never answered as the matrix in force, that the expected row count is computed and never a constant, and that a new matrix needs no deployment and no code change

  Scenario: AC4 The matrix load is published as the access-policy event (new, D-RCV-60)
    Given the events section of the document
    When the rwb-access document is published and its events section is reviewed against the event rules
    Then rwb.access.AccessPolicyChanged.v1 is declared on the topic rwb.access.events.v1 with change kind MATRIX, the version label, the resulting status, the effective date and the row count
    Then rwb.decision.DecisionRecorded.v1 is declared on the shared topic rwb.decision-record.v1 for the entry of the load and of the refusal
    Then no other event name is declared for this capability, and no second name for a matrix load appears anywhere in the document
    Then no payload carries a letter of a role, a user reference or a personal field

  Scenario: AC5 The consumed reads are declared as consumed (new, D-RCV-60)
    Given the consumed section of the document
    When the rwb-access document is published and its consumed section is checked against the ownership map
    Then GET /api/recovery/case/v1/admin/parameters is declared with the owner rwb-case and the parameters contract RWB-P3-E1042-CON, for the approver role rwb.refload.approver.permission
    Then GET /api/recovery/case/v1/admin/lists/{listCode} is declared with the owner rwb-case and the reference-data contract RWB-P3-E1043-CON, for LOV-CAPABILITY and its 14 values
    Then the read-only ACE group view v_ace_iam_group is declared as consumed, read through the ACE group fake of section 12.8, with the owner of RWB-P1-E1069-APP, its fields DF-ACE-301 to DF-ACE-304 and its data_as_of
    Then all three are declared one hop, with the 2 s budget and the 503 when the read does not answer in time
    Then no operation, table or list owned by another service is declared as provided

  Scenario: AC6 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by any of the four operations
    Then the body carries the code, the message, the messageId, the traceId and the field list, with the problem media type
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002, 404 and 409 carry MSG-GEN-004, 422 carries MSG-GEN-001 or MSG-P1-002 and 503 carries MSG-P7-003 or MSG-GEN-006
    Then the 422 of the completeness rule carries MSG-P1-002 with the missing role or the repeated pair named
    Then the message texts are the legacy texts where the message already exists, and the break-glass warning MSG-P4-004 is declared on no operation

  Scenario: AC7 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the six contract fakes of section 12.8
    When a fake is compared with the document
    Then the matrix fake answers the four paths of 12.1: PM-2026.11 in force, PM-2026.12 VALIDATED with its valid-from date and 756 rows, the refused PM-2026.13 with a missing role and a repeated pair, 409 for an existing label and 403 with MSG-P4-002
    Then the reference-data fake answers LOV-CAPABILITY with its 14 values in force, and one value list version later
    Then the parameters fake answers rwb.refload.approver.permission as "RW-SECADM"
    Then the decision-record fake answers the entry append and the 503 with MSG-P7-003
    Then a contract test fails on any drift between a fake and the document, and no fake carries a name or an e-mail address

  Scenario: AC8 A schema change is additive within major version 1 (new, D-RCV-60)
    Given the document is baselined at major version 1
    When a field is added, removed, renamed or retyped
    Then a field added within major version 1 is an additive change
    Then a removed, renamed or retyped field is declared as a new major version
```

These eight criteria test the artefact only. None restates a legacy criterion: the three legacy criteria of RWB-AD-002 are owned by RWB-P4-AD002-APP and their tests sit in section 16 as the cases this contract is the ground of.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's path, table or event | DP-13; Architecture v5 slides 14, 41 | AC1, AC5 |
| BR2 | A consumed read is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5 |
| BR3 | Events are named `rwb.<short>.<Event>.v1` on `rwb.<short>.events.v1`, the shared record type stays on `rwb.decision-record.v1`, and the envelope is CloudEvents 1.0 | Architecture v5 slides 14, 20, 43; Template and Rules §R4 | AC4 |
| BR4 | This capability publishes one event, `rwb.access.AccessPolicyChanged.v1`, with change kind `MATRIX`; `rwb.access.DoaLimitChanged.v1` belongs to the delegation table and no third name exists | Architecture v5 slides 14, 20, 43; ASM-3730 | AC4 |
| BR5 | The contract declares no table of another service: `lov_value`, `reference_row`, `reference_version`, `parameter_catalog` and `parameter_value` are P3's, `decision_log_entry` and `approval` are P7's, `assignment` is P3's and `document` is P5's | DP-01; ownership map | AC5 |
| BR6 | A complete matrix holds exactly one row for every active role against each of the 14 areas, a file with any gap is refused in full with the gap named, and the expected count is computed and never a constant | Legacy AC1, AC2; FSD P4 v3 AC-EXC-P4-004-02; TSD P4 v3 T3.2; ASM-3729 | AC3 |
| BR7 | The letters are `C`, `R`, `U`, `D` and `A` in that order or a dash, and the version status is LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) | FSD P4 v3 A2.4; DF-REF-043; TSD P4 v3 T3.2 | AC2 |
| BR8 | The load writes a version VALIDATED and never APPROVED or IN_FORCE; the approval is the gate of RWB-P4-AD010-APP and a version is in force only from its valid-from date and only after it | Legacy AC1, AC3; ASM-3728; ASM-3727 | AC3 |
| BR9 | An applied version is never edited: a change is a new version with its own label and effective date | Legacy AC3; TSD P4 v3 T4; DP-15 | AC3 |
| BR10 | The three reads need Platform administration `R` and the load needs `C`; an active role is required on every call, and the default deny rule answers 401 and 403 | TSD P4 v3 T6.1; FSD P4 v3 VR-P4-004-1, VR-P4-004-2; ASM-1454 | AC1 |
| BR11 | The approver role and the 14 areas are read as data through the parameters and reference-data contracts, and neither is declared as a constant or an enumerated list of the document | DP-06; DP-07; ASM-3728 | AC5 |
| BR12 | Error responses use one envelope and one message ID per condition, and the business texts are copied unchanged from the legacy story where the message exists | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC6 |
| BR13 | No schema, parameter, example or fake declares a name, an e-mail address, an identity number or the letters of a named individual | REQ-ACA-005; guardrails | AC2, AC4 |
| BR14 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC8 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | The four operations, the four schemas, the event and the consumed reads are described | The document validates and the contract tests pass | In review |
| In review | Consumer sign-off | RWB-P4-AD002-APP, RWB-P4-AD010-APP and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A matrix version is loaded | The load writes the version VALIDATED and publishes the access-policy event | Baselined |

A matrix version has its own states — VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED — and they are the app story's and the approval story's data states, declared here and not states of this document.

The change kind `MATRIX` of `rwb.access.AccessPolicyChanged.v1` is an attribute of the event; it is not a value added to the closed list LOV-CAPABILITY, which keeps its 14 values.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-access` | Owns the document, the four schemas, the event declaration and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Security administrator and the audit representative | Review and sign off the rights, the completeness rule and the effective dates |
| Tech lead of the approval gate of RWB-P4-AD010 | Reviews the state the load leaves and the fields the approval reads |
| Tech lead of the guard of RWB-P4-E1037 | Reviews the letters, the version-in-force rule and the answer the guard reads |
| Tech lead of the reference-data contract of rwb-case | Reviews the declared LOV-CAPABILITY read and its budget |
| Data steward | Confirms that no personal data property is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

BR Field ID of each row of the table below: Not specified in the source documents (DOR-RWB-P4-AD002-CON-7).

| Item | Content |
|---|---|
| Matrix row | `roleCode` (DF-REF-035), `roleName` (DF-REF-036), `roleClass` (DF-REF-037, LOV-ROLE-CLASS), `defaultScope` (DF-REF-038, LOV-SCOPE), `capabilityArea` (DF-REF-042, LOV-CAPABILITY), `letters` (DF-REF-043), `matrixVersion` (DF-REF-044) |
| Matrix | `matrixVersion`, `versionStatus`, `validFrom`, `validTo`, `validOn`, `rowCount`, `rows[]` |
| Matrix version | `matrixVersion`, `versionStatus`, `validFrom`, `validTo`, `rowCount`, `roleCount`, `capabilityAreaCount`, `authorReference`, `approverReference`, `decisionRecordEntryRef`, `pendingApproverRole`, `rows[]` |
| Matrix page | `items[]`, `page`, `size` (default 50, maximum 200), `total` |
| Load request | multipart: the file, `matrixVersion` and `validFrom`; the `Idempotency-Key` header |
| Version status | The values of LOV-VERSION-STATUS; the storage is the standard `state` column of TSD P4 v3 T3.0 |
| Version dates and approver | `validFrom`, `validTo`, `approverReference`, this key's own decision (GAP-2264; ASM-3727) |
| Capability areas | LOV-CAPABILITY with its 14 values, read through DP-07 |
| Approver role | `rwb.refload.approver.permission`, read through DP-06 |
| Event payloads | IDs, codes, counts and times only; no letters, no user reference, no personal field |
| Decision-record entry | The `AC-VERS` and `AC-DENY` entries through DP-03; their fields are the library's and are not redefined here |

Two values the sources do not fix are this baseline's own decision. The valid-from and valid-to dates, the approver reference and the pending approver role have no physical column in TSD P4 v3 T3.1 while legacy AC3 needs them; this key adds the valid-from, valid-to and approver-reference columns to `permission` by its own migration (GAP-2263; GAP-0789; ASM-3727). The operation paths, their rights and their answer shapes have no ownership-map row and no T-A row, and the legacy rows name Reference data and Rules and parameters — **Not specified in the source documents (GAP-2264; ASM-1453, ASM-1454)**. The field names, types and lengths of the four schemas are fixed by this document and its own decision, and no physical column is dictated by it (ASM-3732).

The end state of a load is VALIDATED. APPROVED and IN_FORCE are reached only through the approval gate of RWB-P4-AD010-APP. The expected row count is computed from the active roles and LOV-CAPABILITY at load time and is never fixed in code. The event `rwb.access.AccessPolicyChanged.v1` is published after the commit, and changes within major version 1 are additive only. The deprecation window and the retention of the fakes are Not specified in the source documents (GAP-2264; GAP-0790) and are recorded with the platform contract owner.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/permission-matrix-loads` | multipart with the file, `matrixVersion` and `validFrom`, and the `Idempotency-Key` header; `PermissionMatrixVersion` out with status VALIDATED | Platform administration `C` |
| GET | `/admin/permission-matrix` | `PermissionMatrixPage`: query `roleCode`, `capabilityArea`, `matrixVersion`, `validOn`, `page`, `size`; the rows in force on `validOn` | Platform administration `R` |
| GET | `/admin/permission-matrix-versions/{matrixVersion}` | `PermissionMatrixVersion`: status, dates, row and role counts, author and approver references, decision-record reference, pending approver role and rows | Platform administration `R` |
| GET | `/admin/permission-matrix-versions` | `PermissionMatrixPage` of the versions: label, status, dates and row count; query `status`, `page`, `size` | Platform administration `R` |

Errors for all four: 401 no session or no Workbench role (MSG-P4-001), 403 no right (MSG-P4-002), 404 an unknown label (MSG-GEN-004), 409 a label that exists or a repeated key answered differently (MSG-GEN-004), 422 a missing or invalid field (MSG-GEN-001) or an incomplete matrix (MSG-P1-002), 503 the record entry not written (MSG-P7-003) or the reference list not readable (MSG-GEN-006). The load is idempotent by `Idempotency-Key`; the same key returns the first answer and writes no second version. Major version 1 sits in the path (BR14).

`GET /admin/roles` (API-P4-007), `GET /admin/access-log` (API-P4-008) and `GET /me/session` (API-P4-012) are the service's own operations of RWB-P4-E1019-APP, RWB-P4-E1037-CON, RWB-P4-AD007-APP and RWB-P4-E1022-CON; this document neither restates nor changes them, and the matrix answer here is the flat `permission` rows of one version, not the roles catalogue answer.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case`, RWB-P3-E1042-CON (DP-06) | The approver role `rwb.refload.approver.permission`, so the role a version waits for is data |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case`, RWB-P3-E1043-CON (DP-07) | LOV-CAPABILITY with its 14 values in force, which a complete matrix must cover |

The ACE group reference is a read-only SQL read and not a REST call: `recovery.v_ace_iam_group` (DF-ACE-301 to DF-ACE-304), owner RWB-P1-E1069-APP (DP-05), one hop in the same database, declared with its `data_as_of` and its 503. Nothing else is consumed. The service's own `POST /api/recovery/access/v1/authorise` is declared by RWB-P4-E1037-CON and is not declared again here.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | Change kind `MATRIX`, the version label, the status VALIDATED, the effective date, the row count and the time |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library, consumed by P7 | Entry id, decision code (`AC-VERS`, `AC-DENY`), the version label, the row count and the time |

Both use the CloudEvents 1.0 envelope with id, source, type, specversion, time, subject and datacontenttype. No message carries a letter of a role, a user reference, a name, an e-mail address or an identity number. `rwb.access.DoaLimitChanged.v1` is not declared here and no second name exists for a matrix load (BR4, ASM-3730).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none) and this capability adds no subscription.

#### 12.5 Workflows and activities

None. The four operations are synchronous REST answers in the caller's thread with no workflow, activity or signal. The six-monthly access review Schedule (JOB-18) is RWB-P4-AD008-CON's.

#### 12.6 Schedules

None. Nothing about a matrix runs on a clock: the valid-from date is a row value the read resolves.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `permission` | P4 (`rwb_access`) | The matrix rows and their version label (DF-REF-040 to DF-REF-044); the version dates and the approver reference are this key's own decision (GAP-2264; ASM-3727) |
| `role` | P4 (`rwb_access`) | The role code, name, class and default scope a row and a complete file are checked against; read only |
| `v_ace_iam_group` | ACE, read-only view, owner RWB-P1-E1069-APP | The group reference of the caller: `entra_group`, `role_code`, `source_system`, `data_as_of`; never written |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | Appear nowhere as tables; the list and the parameter are consumed operations (DP-01, DP-06, DP-07) |
| `decision_log_entry`, `approval` | P7 (`rwb_decision`) | Appear nowhere; the local entry is the library's and the central ledger is P7's |
| `assignment` | P3 (`rwb_case`) | Appears nowhere; the legacy Data table names it |
| `document` | P5 (`rwb_document`) | Appears nowhere; the legacy Data table names it |

No foreign key crosses a schema, and the contract names no table outside `rwb_access` except the read-only ACE view it consumes.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `rwb-access` permission-matrix WireMock | The four paths of 12.1: `PM-2026.11` in force, `PM-2026.12` VALIDATED with validFrom 1 December 2026 and 756 rows, the refused `PM-2026.13` with a missing role and a repeated pair, the stored answer for a repeated `Idempotency-Key`, 409 for an existing label, 422 with MSG-GEN-001 and MSG-P1-002, 403 with MSG-P4-002 and 503 with MSG-P7-003 | App story, approval story, contract tests, wave 4 harness |
| Matrix file fixtures | The accepted `PM-2026.12` and the refused `PM-2026.13` | App story, contract tests |
| Reference-data fake (RWB-P3-E1043-CON) | LOV-CAPABILITY with its 14 values in force, and one value list version later | App story, contract tests |
| Parameters fake (RWB-P3-E1042-CON) | `rwb.refload.approver.permission` = "RW-SECADM" | App story, contract tests |
| Decision-record fake (RWB-PLT-E1027-CON) | The entry append, the hash-chain check and the 503 with MSG-P7-003 | App story, contract tests |
| ACE group fake | The group of the loader with its source system and a `data_as_of`, and one group the view no longer holds | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 2 consumed | The load, the matrix read, the version read and the versions list provided; the parameters read and the list read consumed; one hop, 2 s timeout; plus one read-only SQL read of the ACE view |
| Kafka | 2 published, 0 consumed | `rwb.access.AccessPolicyChanged.v1` and `rwb.decision.DecisionRecorded.v1` |
| Temporal | None | No workflow, activity or Schedule |
| File | One upload | The matrix file arrives in the multipart body of the load; no file is stored or served |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-permission-matrix-v1.yaml` (OpenAPI 3.1) with the four operations and the shared components, the four schemas, the `contract/error-envelope.yaml` with the agreed message IDs, the event declaration with change kind `MATRIX`, the parameters stub with its owner, the LOV-CAPABILITY stub, the ACE-view stub with its `data_as_of` and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

A contract story adds no build dependency of its own: each DP above is **referred to, and the consuming story carries the dependency**, and that story is RWB-P4-AD002-APP, whose H row carries the five platform CON stories and RWB-P4-E1037-CON and whose C row carries RWB-P3-E1042-CON and RWB-P3-E1043-CON. DP-03 is contracted as the entry declared on `rwb.decision-record.v1`; DP-05 as the read-only ACE view through the P1 contract; DP-06 as the consumed parameters read; DP-07 as the consumed list read; DP-08 as the guard of every operation; DP-13 as the base of the document; DP-19 as the composite route of SCR-43.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The four operations and the four schemas of section 11, with the page, the version, the status and the dates.
3. The completeness rule and the version rule in the operation descriptions: one row per role per area, a whole-file refusal, VALIDATED at the load, APPROVED only by the gate, in force only from the date, an applied version never edited (BR6, BR8, BR9).
4. The rights of the three reads and of the load, and the 401 and 403 of the default deny rule.
5. The error envelope and the message-ID mapping with the legacy texts copied unchanged and the note on MSG-P4-004.
6. The event declaration and the decision-record type with the change kind and the payload.
7. The consumed parameters read, the consumed list read and the ACE view with their owners, the one-hop rule, the 2 s budget and the 503.
8. The six fakes and the fixtures of section 12.8.
9. The eight contract tests; a drift between a fake and the document fails the build.
10. Baseline tag and the sign-off note of the app story, the approval story and the guard story.

**Feature switch.** None. The four operations are operations of the service; the load is a data change guarded by the `C` letter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD002-APP | The four operations, the four schemas, the completeness and version rules, the event declaration and the six fakes |
| RWB-P4-AD010-APP, the approval gate | The state a load leaves (VALIDATED), the version read and the pending approver role it approves against |
| RWB-P4-E1037-CON, RWB-P4-E1037-APP, the guard | The letters, the version-in-force rule and the matrix row the guard reads at every endpoint |
| The wave 4 harness | The fakes of 12.8 and the parameters, list and ACE-view stubs |

The deprecation window of a published field and the retention of the contract fakes are **Not specified in the source documents (GAP-2264; ASM-3733)**, and the baseline is used while its stories remain Draft under D-RCV-60 with no approval record (ASM-3733).

**Done when.** The OpenAPI document validates in the pipeline, the eight contract tests pass, the six fakes answer every consumed and every provided path, and the app, approval and guard stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session, no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | No Platform administration `R` for a read, or no `C` for the load | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is empty, the label is too long or the valid-from is in the past | Enter {field}. |
| MSG-P1-002 | A role is missing, a pair is repeated, a letter is outside the vocabulary or a role code is unknown | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-004 | The label exists, or the version asked for does not exist | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The reference list or the parameter cannot be read | Not specified in the source documents (CG-ALL-4550); the Error and Message Standard v4 text applies |
| MSG-P7-003 | The decision-record entry could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-004 | Not declared on any operation of this document; the break-glass warning of RWB-P4-AD006-APP and RWB-P4-E1039-APP | Emergency access is on until {time}. Every action is recorded. |

The message IDs are contract elements; the text is the agreed text, taken from the legacy story where the message already existed. The legacy warning MSG-P4-004 ("Emergency access is on until {time}. Every action is recorded.") is the break-glass warning of RWB-P4-AD006-APP and RWB-P4-E1039-APP and is declared on no operation. The legacy permission rows "Reference data C: RW-COE, RW-REFADM" and "Rules and parameters A: RW-RISK" are not carried as the rights of these operations; the rights are Platform administration `R` and `C` (ASM-1454).

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access | List | The matrix read with the rows in force and the version label |
| SCR-43 Roles and access | Versions | The versions list with the status and the dates of each version |
| SCR-43 Roles and access | Load | The load request with the file, the label and the valid-from, and the field-level 422 answers |
| SCR-43 Roles and access | Loaded | The written version with status VALIDATED, its row count, decision-record reference and pending approver role |
| SCR-43 Roles and access | Refused | 403 with MSG-P4-002, 401 with MSG-P4-001, and 422 with MSG-P1-002 or MSG-GEN-001 |
| SCR-43 Roles and access | Not available | 503 with MSG-GEN-006 or MSG-P7-003 |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (DOR-RWB-P4-AD002-CON-10) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (DOR-RWB-P4-AD002-CON-10) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (DOR-RWB-P4-AD002-CON-10) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (DOR-RWB-P4-AD002-CON-10) |
| SCR-40 Reference data | Empty | Not specified in the source documents (DOR-RWB-P4-AD002-CON-10) |
| SCR-40 Reference data | Loading | Not specified in the source documents (DOR-RWB-P4-AD002-CON-10) |
| SCR-40 Reference data | Error | Not specified in the source documents (DOR-RWB-P4-AD002-CON-10) |
| SCR-40 Reference data | No access | Not specified in the source documents (DOR-RWB-P4-AD002-CON-10) |
| SCR-43 Roles and access | Empty | Not specified in the source documents (CG-ALL-4555) |
| SCR-43 Roles and access | Loading | Not specified in the source documents (CG-ALL-4555) |
| SCR-43 Roles and access | Error | Not specified in the source documents (CG-ALL-4555) |
| SCR-43 Roles and access | No access | Not specified in the source documents (CG-ALL-4555) |

The screens are served by the gateway-bff composite route (DP-19), which calls the matrix read or the versions list and the access-log read in parallel, one hop each. The composite route specification, the screen field list, the column order and the placement of the load form are **Not specified in the source documents (GAP-2264; ASM-3731)**; this document fixes the matrix side of the merge only. The legacy pair SCR-39 Rules and parameters and SCR-40 Reference data is not declared here; its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-4553; CG-ALL-4554): the rule versions are RWB-P4-AD011-CON's and the reference lists are RWB-P4-AD009-CON's and RWB-P4-AD010-CON's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-002-01 | AC1 | Contract | Legacy test "Load a matrix version" on the contract side: the document declares the load and the three reads at their paths with their rights and their errors, and the fake answers `PM-2026.12` VALIDATED with 756 rows and validFrom 1 December 2026; the behaviour is tested by RWB-P4-AD002-APP at End to end |
| TC-AD-002-02 | AC2 | Contract | Legacy test "Incomplete matrix refused" on the contract side: the document declares the whole-file rule and the 422 with MSG-P1-002 naming the gap, and the fake answers the refused `PM-2026.13` with a missing role and a repeated pair |
| TC-AD-002-03 | AC3 | Contract | Legacy test "Takes effect on its date" on the contract side: the document declares VALIDATED at the load, APPROVED only through the gate and in force only from the valid-from; the matrix read answers the version in force on the date asked and a VALIDATED version is never answered as in force |
| TC-AD-002-04 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002": the document declares 403 with MSG-P4-002 on all four operations for a caller without the Platform administration letter, and the fake answers it with the refusal entry |
| TC-AD-002-05 | Principle 5 | NFR | Legacy test "A forced decision log write failure stops the action with MSG-P7-003": the document declares the 503 with MSG-P7-003 and the fake answers it, so no consumer treats a refused load as a version stored |
| TC-AD-002-06 | AC4 | Contract | The event declared with change kind MATRIX, the version label PM-2026.12, the status VALIDATED and the row count as computed at load; no second event name; no personal field in the payload |
| TC-AD-002-07 | AC5 | Contract | Each consumed read declared as consumed with its owner, its contract, the 2 s budget and the 503; no operation, table or list of another service declared as provided |
| TC-AD-002-08 | AC6 | Contract | The error envelope with code, message, messageId, traceId and field list under the problem media type; 401 MSG-P4-001, 403 MSG-P4-002, 404 and 409 MSG-GEN-004, 422 MSG-P1-002 naming the gap, 503 MSG-P7-003 |
| TC-AD-002-09 | AC7 | Contract | Each fake compared with the document: PM-2026.11, PM-2026.12, PM-2026.13, LOV-CAPABILITY with 14 values, rwb.refload.approver.permission as RW-SECADM, the 503 with MSG-P7-003; no fake carries a name or an e-mail address |
| TC-AD-002-10 | §12.7 tables (ASM-3438) | Contract | Boundary test on the tables of §12.7; the boundary values are not specified in the source documents (DOR-RWB-P4-AD002-CON-12) |
| TC-AD-002-11 | AC8 | Contract | An added field and a removed field of a schema; the added field is additive within major version 1 and the removed field is declared as a new major version |

The five legacy test cases keep their IDs and their legacy Covers values, and the legacy test name is written in the Data column. The Level column follows §R7.2: the operations, the whole-file rule and the version rule are tested against the artefact at Contract, the legacy Access row stays Component and the legacy Principle 5 row stays NFR. The behaviour of each case in the running service is RWB-P4-AD002-APP's at End to end, and the full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. The ITG copy of the set is the integration harness's, so no `-ITG` id appears.

### 17. Guardrails

- No business value in the contract: labels, dates, letters, the approver role and the 14 areas are rows, parameters and consumed contract answers; the document fixes names and types only.
- No personal data in a schema, an example or a fake: a matrix row is a role code, an area and letters, and a name or an e-mail address in the document fails the review (BR13).
- The contract names only `rwb-access` tables, the read-only ACE view it consumes, and operations owned by `rwb-access` or declared as consumed (DP-01, BR5).
- One REST base, one topic and one event name for the capability, with the shared record type on `rwb.decision-record.v1` (DP-13, BR3, BR4).
- The load and the approval are two acts: VALIDATED is the declared end state of the load, so no consumer can read the load as an approval (BR8).
- A version is in force only from its date and only after its approval, and an applied version is never edited, so no consumer reads "the latest rows" as the truth (BR6, BR9).
- The reference list and the approver role are consumed, never enumerated, so a new area or a new approver role is a data change with no contract change (BR11).
- Every example and every fake is synthetic; no production role, person or entitlement is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

No requirement ID is recorded for legacy RWB-AD-002 in TSD P4 v3 T8, and the Work Package carries the requirement list of this key as empty; TSD P4 v3 T8 records REQ-ACA-003 against FEAT-ACA-01 and RWB-E1-022. The key serves FEAT-ACA-04 (hold the role to permission matrix as data) and FEAT-ADM-01 (run the full administration screens) of FSD P4 v3.

| Feature | Contract element | Test cases |
|---|---|---|
| FEAT-ACA-04, hold the role to permission matrix as data | The matrix row, the version status and the effective dates of 12.1 and 12.7, and the load that writes a dated version | TC-AD-002-01, TC-AD-002-03 |
| FEAT-ADM-01, the full administration screens | The four operations and the SCR-43 states they feed through the composite route | TC-AD-002-04 |
| The whole-file refusal and the named gap | The 422 with MSG-P1-002 of 12.1 and the completeness rule of AC3 | TC-AD-002-02 |
| The record-before-change rule | The 503 with MSG-P7-003 and the decision-record type of 12.3 | TC-AD-002-05 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy AC1, AC2 and AC3 | The behaviour of RWB-P4-AD002-APP; this contract carries the elements they are tested against, and section 16 keeps their test cases |
| The matrix of roles against the 14 capability areas and the version label | Sections 3, 7, 11 |
| The Data rows `permission` DF-REF-040 to DF-REF-044 and `role` DF-REF-034 to DF-REF-038 | Sections 11, 12.7 |
| The `assignment` and `document` rows of the legacy Data table | Sections 11, 12.7; another service's, declared nowhere |
| The legacy endpoints `POST /admin/rule-versions/{versionId}/approve` and `POST /admin/reference-loads` | Section 19; other owners, not carried |
| The permission checks Reference data and Rules and parameters | 12.1, 8 (BR10); not carried as the rights of these operations |
| MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P1-002, MSG-GEN-004, MSG-GEN-006, MSG-P7-003 and the break-glass warning MSG-P4-004 | Section 14, exception paths |
| Screens SCR-39, SCR-40 and SCR-43 | Section 15 |
| Legacy test cases TC-AD-002-01 to TC-AD-002-05 | Section 16 |

### 19. Out of scope

- The implementation of the four operations, the migration, the checks, the reference reader, the record entry and the event: RWB-P4-AD002-APP.
- The approval, the verify and the rollback of a loaded version on the reference-load path: RWB-P4-AD010-APP and RWB-P4-AD010-CON, with RWB-P4-AD009-APP for the rollback of a configuration version. This document declares the state the load leaves and the fields the approval reads; it declares no approve operation.
- The legacy endpoint `POST /admin/rule-versions/{versionId}/approve` under the monolith base that DP-13 replaces: the rule-version approve and the rule packages are the rule-version stories' and P7 rwb-decision's under ASM-0040; no path of it appears here.
- The legacy endpoint `POST /admin/reference-loads` under the same base: the generic reference-load path is P3 rwb-case's under ASM-0041 and its approval is RWB-P4-AD010-APP's; neither appears here.
- The guard, the masker and the `@PersonalData` annotation: RWB-PLT-E1037-CON and RWB-PLT-E1037-APP; the roles catalogue, the masking policy and the role conflicts: RWB-P4-E1019-APP, RWB-P4-E1037-APP and RWB-P4-E1037-CON.
- The masking profiles per role, the separation-of-duty check at sign-in, the group-to-role mapping, the access review and the break-glass grant: RWB-P4-AD004-APP, RWB-P4-AD005-APP, RWB-P4-AD001-APP, RWB-P4-AD008-APP and RWB-P4-AD006-APP.
- The reference data and the parameter values of the estate, including LOV-CAPABILITY and the approver role: P3 rwb-case under DP-06 and DP-07; this contract declares two consumed reads and no table of either.
- The central decision ledger and its query: P7 rwb-decision; the local entry is the library's.
- `assignment` and `document`: P3 rwb-case and P5 rwb-document, named by the legacy Data table and declared nowhere.
- The deployment of the capability — Helm values, topic creation, dashboards, runbook — the integration harness and its evidence, and the `-ITG` copies of the test cases.
- The field-level completeness of the four schemas beyond what section 11 fixes (GAP-2264; ASM-3732).
