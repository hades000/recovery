# RWB-P4-AD002-APP Permission matrix as a versioned load

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-002 for rwb-access — the permission matrix loaded as one complete dated version in `rwb_access`, with its whole-file checks, its version status before approval, its effective-from date, the matrix read, the version read and the versions list, and the access-policy event. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-AD002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 28 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD002-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP08, DP13, DP19 |
| Parallel lane | L-P4-B |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-AD002-APP-16); set at refinement |
| Depends on (build) | RWB-P4-AD002-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-P4-E1037-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As an **application owner**, I want **the permission matrix of roles against the 14 capability areas loaded as one complete, dated version of `permission` in `rwb_access`, checked as a whole**, so that **a permission changes without a code release and every change waits for an approval and takes effect on its date**.

This is the rwb-access slice of legacy RWB-AD-002 and its load half: the matrix rows of one version, the whole-file checks, the version status before approval, the effective-from date, the matrix read, the version read and the versions list.

- **Naming:** base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1` with names `rwb.access.<Event>.v1`, queue `rwb-access` in namespace `rwb-recovery` (unused here), package `th.co.scb.ace.workbench.recovery.access`.
- **A matrix row:** one `permission` row is one role against one capability area — `role_id` (DF-REF-041), `capability_area` (DF-REF-042, LOV-CAPABILITY), `letters` (DF-REF-043, varchar(5), `C`, `R`, `U`, `D`, `A` in that order or a dash) and `matrix_version` (DF-REF-044, varchar(20)) (FSD P4 v3 A2.4 field catalog; TSD P4 v3 T3.1). The legacy wording stands: "the permission matrix of roles against the 14 capability areas".
- **The 14 areas:** CASE_RECORD, QUEUE_AND_ALLOCATION, TREATMENT_AND_OFFER, LITIGATION, ASSET_AND_DISPOSAL, DEBT_SALE, WRITE_OFF_AND_POSTING, DOCUMENTS, RULES_AND_PARAMETERS, REFERENCE_DATA, DECISION_LOG, PARTNER_PORTAL, REPORTING, PLATFORM_ADMINISTRATION (TSD P4 v3 T3.2), read through the reference-data contract of rwb-case (DP-07), never by SQL and never as a constant.
- **Version and status:** the label is `matrix_version`; the status is the standard `state` column (TSD P4 v3 T3.0) in the vocabulary LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED). The valid-from and valid-to dates and the approver reference are added to `permission` by this story's migration (GAP-2263; ASM-3727), and the label is minted by a single set that supersedes the version in force, so a change is a versioned change and not an edit in place (GAP-2304).
- **The boundary with the approval:** this story writes a version and stops at VALIDATED. **RWB-P4-AD010-APP owns the approve, the verify and the rollback**, and AC1 ends where the legacy criterion ends, at "waits for the application owner's approval"; the approver role is read as the parameter `rwb.refload.approver.permission` through DP-06 (ASM-3728).
- **The four operations:** the matrix load, the matrix read, the version read and the versions list, at the paths fixed by RWB-P4-AD002-CON on the service base. Neither the paths nor their right has an ownership-map row or a T-A row, where the only role read is `GET /admin/roles` (API-P4-007) — **Not specified in the source documents (GAP-2263; ASM-1453)**.
- **The check is whole:** one row per active `role` row per area, computed from `role` and LOV-CAPABILITY and never a constant; any gap or letter outside the vocabulary refuses the file in full and names the missing role (legacy AC2; ASM-3729).
- **The effective date:** a version answers as the matrix in force only when it is APPROVED and only from its valid-from date; from that date every endpoint checks against it through the guard of RWB-P4-E1037-CON and RWB-PLT-E1037-CON (DP-08), which reads the `permission` rows in force on the day of the request (legacy AC3).
- **The change is recorded:** every load and every refusal writes one local decision-record entry through DP-03 — `AC-VERS` for a version written, `AC-DENY` for a refusal — on the shared topic `rwb.decision-record.v1`; the central ledger stays P7 rwb-decision's.
- **The signal:** `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` with change kind `MATRIX`, the version, the status, the effective date and the row count, and no personal data (ASM-3730).
- **Authority:** the letters come from the caller's own `role` and `permission` rows through the authorise contract (DP-08). The matrix is Platform administration in TSD P4 v3 T6.1 — `R` for the reads, `C` for the load, held by RW-SECADM (CRUDA) and RW-PLATADM (CRUD); the legacy rows "Reference data C: RW-COE, RW-REFADM" and "Rules and parameters A: RW-RISK" are not carried (ASM-1454).
- **Screens:** SCR-43 Roles and access shows the roles, their permissions, the scope and the group mapping, served by the gateway-bff composite route (DP-19; RWB-PLT-N001-CON). Where the load form sits is Not specified in the source documents (GAP-2263; ASM-3731).
- **Not this story:** the approval, verify and rollback (RWB-P4-AD010-APP, RWB-P4-AD009-APP); the roles catalogue and the masking policy (RWB-P4-E1019-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON); the sibling slices RWB-P4-AD001-APP, RWB-P4-AD004-APP, RWB-P4-AD005-APP, RWB-P4-AD008-APP and RWB-P4-AD006-APP; and the legacy Data rows `assignment` (P3 rwb-case) and `document` (P5 rwb-document), neither read nor written here.

### 2. Business rationale

What a role may do lives in documents and people's heads today, so a permission change needs a code release or a manual data fix, and audit findings record unsuitable access for that reason. Legacy RWB-AD-002 answered it by loading the matrix as one versioned file approved before it took effect. The realignment keeps the answer and makes it a service answer: the matrix is rows of `permission` in `rwb_access`, a version is a label with a status and an effective date, and a file is checked as a whole before a single row is stored.

Three consequences are the point of the split. The matrix is data, not a release — the measure is rule and limit changes made without a code release, target 100 percent (FSD P4 v3 A2.4). The check is whole-file, because a missing role silently removes a right from everyone holding that role, so a refused load leaves the version in force untouched and names the gap. And the load and the approval are two acts with two owners: the load needs the `C` letter of Platform administration, and the approval is RWB-P4-AD010-APP's gate, so a version cannot approve itself by being loaded (ASM-3728).

The realignment also corrects the legacy right. The legacy row set made the load "Reference data C" for RW-COE and RW-REFADM, but the matrix is role administration and TSD P4 v3 T6.1 puts the `permission` rows in Platform administration; the reference data of the estate (`lov_value`, `reference_row`, `reference_version`) is P3 rwb-case's. The letters are therefore read from Platform administration (ASM-1454), and the reference-data contract is consumed for one thing only: the 14 areas a complete file must cover.

The matrix reaches the estate as one signal. `rwb.access.AccessPolicyChanged.v1` is the one access-policy event the architecture gives this service (Architecture v5 slides 14 and 43), services refresh their cached permission data on it (slide 20), and a matrix load **is** an access-policy change (ASM-3730).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD002-CON | The published matrix contract: the four operations, the `PermissionMatrix`, `PermissionMatrixRow`, `PermissionMatrixVersion` and `PermissionMatrixPage` schemas, the whole-matrix and effective-date rules, the event declaration, the error envelope and the fakes |
| RWB-PLT-E1027-CON | The local decision-record library and topic `rwb.decision-record.v1` (DP-03): the `AC-VERS` and `AC-DENY` entries |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters library and contract (DP-06): the approver role of the `permission` table as data |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data library and contract (DP-07): LOV-CAPABILITY and its 14 values in force |
| RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The guard library and the authorise contract (DP-08): the `R` and `C` letters, MSG-P4-002 and MSG-P4-001 |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-43 and merges the matrix read with the access-log read |
| `role` and `permission` in `rwb_access` | The role rows a file must cover (DF-REF-034 to DF-REF-039) and the matrix rows (DF-REF-040 to DF-REF-044), from the service baseline of RWB-E1-037 and RWB-P4-E1037-APP. This story writes `permission` only |
| The version dates, status and approver reference | The status is the standard `state` column; the dates and approver reference are added to `permission` by this story's migration (GAP-2263; ASM-3727) |
| The matrix file | One row per role and area with the letters in the vocabulary of DF-REF-043. The labels `PM-2026.11` (in force), `PM-2026.12` (756 rows) and the refused `PM-2026.13` are the values of FSD P4 v3 AC-P4-004-01 and of the tests (ASM-3729) |
| No approval of this document | The story is born Draft (realignment v1) under D-RCV-60 and builds against a Draft contract; the contract freezes when its consumers pass their contract tests |

**Wave.** Wave 4 is the W-MAP wave of business epic EP08 (Template and Rules §R5.6), not the Arch v5 wave 1 of the service; the release date is copied unchanged and marked tentative.

### 4. Flow

1. The administrator opens SCR-43 through the composite route of DP-19; the route calls the matrix read (or the versions list) and the access-log read in parallel, one hop each, and merges them.
2. The guard authorises at the door (DP-08): `R` of Platform administration for the reads, `C` for the load. No Workbench role is 401 with MSG-P4-001 and a missing letter is 403 with MSG-P4-002; both write one `AC-DENY` entry before the answer leaves.
3. The load is `POST /api/recovery/access/v1/admin/permission-matrix-loads` with a multipart body — the file, the `matrixVersion` label, the `validFrom` date — and an `Idempotency-Key`; a repeated key answers the first answer and stores no second version.
4. `CapabilityAreaReader` reads LOV-CAPABILITY through DP-07 and gets the 14 areas in force; where the read misses the 2 s budget the load answers 503 with MSG-GEN-006 and writes nothing.
5. `PermissionMatrixChecks` runs over the whole file before a row is written: every active `role` row once per area, no repeated pair, letters within `C`, `R`, `U`, `D`, `A` or the dash and at most 5 characters, every role code an active role, the label present and within 20 characters, the valid-from present and not earlier than the load day, no required field empty (MSG-GEN-001).
6. A file that fails any check is refused in full: 422 with MSG-P1-002 naming the check, the missing role or the duplicate pair; no row is stored and the version in force is unchanged (legacy AC2).
7. An existing label is 409 with MSG-GEN-004 and nothing is written.
8. The rows are written in one transaction with the standard columns, the version's dates and approver reference; the version is LOADED while written and VALIDATED on commit. No version is APPROVED and none is IN_FORCE.
9. `MatrixVersionRecorder` writes one `AC-VERS` entry in the same transaction through DP-03 — label, row count, role count, effective date, acting user reference, time, no name — with its outbox row; where the entry cannot be written nothing is stored and the call is 503 with MSG-P7-003.
10. After the commit one `rwb.access.AccessPolicyChanged.v1` is published with change kind `MATRIX`, the version, the status VALIDATED, the effective date and the row count — no letters, no user reference (ASM-3730).
11. The load answers 201 with the version: label, status VALIDATED, dates, counts, author reference, decision-record reference and the role it waits for from the parameter (DP-06). The version waits for the application owner's approval (legacy AC1).
12. The version read answers one version by label whether or not it is in force; a valid-from in the future or a status VALIDATED is answered as a version, never as the matrix in force.
13. The versions list answers the labels with their status and dates, filtered by status.
14. The matrix read answers the rows in force on the date asked: the version whose valid-from is the latest not after that date and whose status is APPROVED or IN_FORCE, one version whole and never a mixture.
15. From its valid-from date every endpoint checks against the new version, because the guard reads the `permission` rows in force on the day of the request (legacy AC3); no deployment, restart or manual cache flush is needed.
16. Every call is one hop on the caller's thread inside the 2 s budget (DP-11); the group reference arrives read-only from `v_ace_iam_group` of the same database (DP-05).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is empty, the label exceeds 20 characters, or the valid-from is in the past | 422 with the field named; nothing written | MSG-GEN-001 | AC2 |
| X2 | A role of the environment is missing from the file | 422, refused in full with the missing role named; the version in force stays | MSG-P1-002 | AC2 |
| X3 | A role and area pair appears twice | 422 naming the duplicate pair; nothing stored | MSG-P1-002 | AC2 |
| X4 | A letter is outside the vocabulary, or the letter string is longer than 5 characters | 422 naming the row and the letters; nothing stored | MSG-P1-002 | AC2 |
| X5 | The file names a role code the environment does not hold as an active `role` row | 422 naming the role code; nothing stored | MSG-P1-002 | AC2 |
| X6 | The version label already exists | 409 with the envelope; the stored version is answered | MSG-GEN-004 | AC1 |
| X7 | The caller holds no `C` for the load or no `R` for a read | 403 before any row is read or written, one `AC-DENY` entry | MSG-P4-002 | AC1 |
| X8 | The caller holds no Workbench role | 401, one `AC-DENY` entry | MSG-P4-001 | AC1 |
| X9 | LOV-CAPABILITY cannot be read through DP-07 | 503; nothing written and the version in force unchanged | MSG-GEN-006 | AC1, AC2 |
| X10 | The decision-record entry cannot be written | 503; no row stored and the version in force unchanged | MSG-P7-003 | AC1 |
| X11 | Two loads of the same label arrive at once | One stored, one entry; the other 409 and writes nothing | MSG-GEN-004 | AC1 |
| X12 | A read arrives while a load commits, or asks for a VALIDATED version | The read answers one version whole; a VALIDATED version is never answered as in force | None | AC3 |

No path of this story approves, verifies or rolls back a version; its only writes are the `permission` rows of a new version, its decision-record entry, its outbox row and the stored answer of an `Idempotency-Key`.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the matrix contract and its fakes, the decision-record library, the parameters and reference-data contracts and the guard; writes one service's own `permission` rows and reads its own `role` rows |
| Negotiable | Labels, dates, letters and the approver role are data rows and parameters; the story fixes the checks, the version rule and the read shapes |
| Valuable | A permission change is one checked file, one dated version, one recorded decision and one published access-policy event, with no release |
| Estimable | One migration adding the version dates, one check set, four operations, one record entry and one event |
| Small | Fits one sprint with its tests; the approval, the masking rules and the screens are other stories' |
| Testable | Every criterion is one automated test over synthetic role rows and a stubbed reference-data contract; no real role, person or entitlement is needed |

### 7. Acceptance criteria

```gherkin
Feature: Permission matrix as a versioned load

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given a matrix version is the "matrix_version" of the "permission" rows of one environment in "rwb_access"
    Given a complete matrix holds every active role once against each of the 14 capability areas of "LOV-CAPABILITY"

  Scenario: AC1 Load a matrix version (legacy RWB-AD-002 AC1)
    Given the rwb-case contract mock returns the 14 capability areas of LOV-CAPABILITY in force
    Given a matrix file with every role and area
    When the reference data administrator loads it
    Then it passes the checks and waits for the application owner's approval

  Scenario: AC2 Incomplete matrix refused (legacy RWB-AD-002 AC2)
    Given a file with a role missing
    When it is loaded
    Then the system refuses it in full with the missing role named

  Scenario: AC3 Takes effect on its date (legacy RWB-AD-002 AC3)
    Given an approved version with a valid from date
    When the date arrives
    Then every endpoint checks against the new version

  Scenario: AC4 Every business rule of section 8 is covered (no legacy origin) (new, D-RCV-60)
    Given the business rules BR1 to BR12 of section 8
    When the story is built and tested
    Then each rule is answered by this story and covered by a test case in section 16

  Scenario: AC5 Error answers of the provided operations (401, 403, 404) (new, D-RCV-60)
    Given a caller of the provided operations
    When the caller holds no Workbench role, holds no letter the operation needs, or asks for a resource that does not exist
    Then the answer is 401, 403, or 404 for the missing resource; the error messages and the 404 condition are Not specified in the source documents (NEWAC-RWB-P4-AD002-APP-AC5)

  Scenario: AC6 Replay of a write with the same Idempotency-Key (new, D-RCV-60)
    Given a load answered with an Idempotency-Key
    When the same Idempotency-Key is sent again
    Then the first answer is returned and no second version is stored

  Scenario: AC7 A consumed call fails or does not answer (no legacy origin) (new, D-RCV-60)
    Given a consumed contract call that fails or does not answer
    When a load or read needs the answer of that call
    Then no row is stored and the operation answers with an error, the error code being Not specified in the source documents (NEWAC-RWB-P4-AD002-APP-AC7)
```

The three criteria are the legacy criteria of RWB-AD-002, copied word for word with their origin tag. One Given line is added to AC1: the mocked answer of the reference-data contract (DP-07, the C dependency RWB-P3-E1043-CON) that returns the 14 areas of LOV-CAPABILITY in force, because the completeness rule of AC1 and AC2 is measured against that list. Every legacy value is kept character for character — the file "with every role and area", the missing role, the refusal "in full with the missing role named", the approved version "with a valid from date" and the rule that every endpoint checks against the new version.

AC1 ends where the legacy criterion ends, at "waits for the application owner's approval": the approval is RWB-P4-AD010-APP's (ASM-3728) and this story writes VALIDATED and no further. AC2 is answered by `PermissionMatrixChecks` over the whole file. AC3 is answered by the valid-from date this story stores and by the guard, which resolves the version in force on the day of the request for every endpoint.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A matrix is one `permission` row per role and area: `role_id` (DF-REF-041), `capability_area` (DF-REF-042, LOV-CAPABILITY), `letters` (DF-REF-043) and `matrix_version` (DF-REF-044). No role code, area, label or date is written in code | Legacy Data table; TSD P4 v3 T3.1; FSD P4 v3 A2.4 |
| BR2 | A complete matrix holds exactly one row for every active `role` row against each of the 14 areas, and a file with any gap is refused in full with the missing role named | Legacy AC1, AC2; FSD P4 v3 AC-EXC-P4-004-02; TSD P4 v3 T3.2; ASM-3729 |
| BR3 | The letters are `C`, `R`, `U`, `D` and `A` in that order or the dash for none, and never anything else | FSD P4 v3 A2.4 field catalog; DF-REF-043 |
| BR4 | A version is a label with a status from LOV-VERSION-STATUS and a valid-from date; an applied version is never edited and a change is a new dated version | Legacy AC3; TSD P4 v3 T3.2, T4; DP-15 |
| BR5 | This story writes a version VALIDATED and stops: it never approves, verifies or rolls back, and the approval of the `permission` table is RWB-P4-AD010-APP's | Legacy AC1; ASM-3728 |
| BR6 | A version answers as the matrix in force only when it is APPROVED and only from its valid-from date; before that date the version in force before it answers for every endpoint | Legacy AC3; TSD P4 v3 T4; ASM-3727 |
| BR7 | The reads need the `R` letter of Platform administration and the load needs `C`; no Workbench role is 401 with MSG-P4-001, a missing letter is 403 with MSG-P4-002, and both refusals are recorded | TSD P4 v3 T6.1; FSD P4 v3 VR-P4-004-1, VR-P4-004-2; DP-08; ASM-1454 |
| BR8 | Every load and every refusal writes one local decision-record entry — `AC-VERS` or `AC-DENY` — and where the entry cannot be written no `permission` row is stored | DP-03; Principle 5; FSD P4 v3 AC-EXC-P4-004-07; MSG-P7-003 |
| BR9 | A matrix load is published as `rwb.access.AccessPolicyChanged.v1` with change kind `MATRIX`, the version, the status, the effective date and the row count, and no personal data; no second event name exists for it | Architecture v5 slides 14, 20, 43; ASM-3730 |
| BR10 | LOV-CAPABILITY is read through the reference-data contract (DP-07) and the approver role through the parameters contract (DP-06); never by SQL and never as a constant | DP-06; DP-07; ownership map |
| BR11 | No statement names a table of another service or a `public` table: `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value`, `decision_log_entry`, `assignment` and `document` are never read | DP-01; ownership map |
| BR12 | A repeated load with the same `Idempotency-Key` answers the first answer and stores no second version; two loads of one label are one stored version and one 409 | Architecture v5 slide 11; DP-09 idempotency rule |

Where the rules sit: BR1 to BR4 are answered from `permission` and from the reference list of the 14 areas, with the checks before the write. BR5 is the absence of an approve, verify or rollback operation. BR6 is the read predicate — status APPROVED or IN_FORCE and the latest valid-from not after the date asked. BR7 is the guard of DP-08 in one hop. BR8 is the decision-record library and the service-template outbox. BR9 is the publication after commit. BR10 is the two clients. BR11 is enforced by the module map and boundary rule BND-6 of RWB-P4-E1069-APP. BR12 is the stored answer of the load.

Test coverage of the rules (criterion, then test case): BR1 by AC1 (TC-AD-002-01); BR2 and BR3 by AC2 (TC-AD-002-02); BR4 and BR6 by AC3 (TC-AD-002-03); BR5 by AC1 (TC-AD-002-01); BR7 by the access test (TC-AD-002-04); BR8 by the NFR test (TC-AD-002-05); BR9 and BR12 by AC1 (TC-AD-002-06); BR10 and BR11 by AC1 (TC-AD-002-07).

### 9. State transitions

None for a case, a task or a session. The states here are the states of a matrix version (LOV-VERSION-STATUS, TSD P4 v3 T3.2, in the standard `state` column).

| From | Event | Condition | To |
|---|---|---|---|
| No version of the environment | a matrix is loaded by this story | Every check passes and the entry is written | The rows are VALIDATED under the label; no version is in force yet |
| No version of the environment | a matrix is loaded and a check fails, or the entry cannot be written | Any failed check, or a 503 from the record library | REFUSED; no row stored and nothing in force |
| VALIDATED | the approval of RWB-P4-AD010-APP | The approver's gate passes and the entry is written | APPROVED with its valid-from date; this story does not make the transition |
| APPROVED | the valid-from date arrives | None | IN_FORCE; the matrix read answers it and every endpoint checks against it |
| IN_FORCE | a later version is approved and its date arrives | None | SUPERSEDED; the later version answers from its date and the old rows stay readable for audit |
| IN_FORCE | a rollback (RWB-P4-AD009-APP, RWB-P4-AD010-APP) | The rollback gate passes | ROLLED_BACK; this story reads it only to refuse it as the matrix in force |

This story writes LOADED inside its transaction and VALIDATED on commit, and reads the later states the approval stories write.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (per-service login, DP-02) | Answers the three reads, writes a matrix version, runs the checks, writes the decision-record entry and publishes the event |
| RW-SECADM, security administrator | CRUDA in Platform administration (TSD P4 v3 T6.1): loads a version and reads every version |
| RW-PLATADM, platform administrator | CRUD in Platform administration: loads a version as the security administrator does, and reads the versions |
| RW-AUDIT, internal audit | `R` in Platform administration: reads the matrix, the versions and the entries; writes nothing |
| RW-COE, center of excellence analyst | CRUD in Rules and parameters and `R` in Platform administration: reads the matrix only, because the matrix is not a rule or a parameter |
| RW-REFADM, reference data administrator | CRUD in Reference data and no right in Platform administration: does not load the matrix, which is not reference data (ASM-1454) |
| The application owner | Approves each version outside this story, on the gate of RWB-P4-AD010-APP (legacy AC1) |
| The guard (RWB-P4-E1037-CON, RWB-PLT-E1037-CON) | Resolves the letters of every caller and checks every endpoint against the version in force (DP-08) |
| Every other role and service identity | Reads the matrix through the guard and no operation of this story |
| Delegation of authority | No level applies: a permission letter is not a credit decision and no `delegation_limit` row is read |

The legacy permission table gives the rule-version approve the `A` letter of Rules and parameters for RW-RISK and the reference-load the `C` letter of Reference data for RW-COE and RW-REFADM. Neither row is kept for the matrix: the rule paths belong to the rule-version stories of this service and P7 rwb-decision (ASM-0040), the reference-load path belongs to P3 rwb-case (ASM-0041), and the matrix is Platform administration in TSD P4 v3 T6.1 (ASM-1454).

### 11. Data

| BR Field ID | Table | Field | Read or write |
|---|---|---|---|
| DF-REF-040 | `permission` (`rwb_access`) | id | Written, one per row of a new version |
| DF-REF-041 | `permission` | role_id | Written, from the role the file names |
| DF-REF-042 | `permission` | capability_area (LOV-CAPABILITY) | Written, one of the 14 areas |
| DF-REF-043 | `permission` | letters | Written, `C`, `R`, `U`, `D`, `A` in that order or the dash |
| DF-REF-044 | `permission` | matrix_version | Written and read; the label of the row |
| DF-REF-034 to DF-REF-038 | `role` (`rwb_access`) | id, role_code, role_name, role_class, default_scope | Read; the role rows a file is checked against and the scope the matrix answer shows |
| Not a field ID: added by this story's migration (GAP-2263; ASM-3727) | `permission` | the version status, the valid-from and valid-to dates, the approver reference | Written by the load and read by all four operations; the status uses the standard `state` column |
| DF-ACE-301 to DF-ACE-304 | `v_ace_iam_group` (ACE, read-only view) | entra_group, role_code, source_system, data_as_of | Read through the P1 ACE-view contract (DP-05) for the group reference of the loader; never written; test data and acceptance criteria use the same contract and do not query the view |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb_case` | lov_code, value_code, label_en, sort_order, valid_from | **Never read by SQL**: LOV-CAPABILITY arrives through the reference-data contract (DP-07) |
| DF-WRK-009 to DF-WRK-016 | `assignment` of `rwb_case` | id, case_id, task_id, assignee_user_id, assigned_at, ended_at | Not read and not written; the legacy Data table names it and the ownership map gives it to P3 |
| DF-DOC-001 to DF-DOC-011 | `document` of `rwb_document` | id, case_id, person_key, document_type, source, storage_ref | Not read and not written; the legacy Data table names it and the ownership map gives it to P5 |
| the DP-03 library's table | local decision record | the `AC-VERS` and `AC-DENY` entries of a load and of a refusal | Written through the library; no field invented here |

The version status, the dates and the approver reference have no column on `permission` in TSD P4 v3 T3.1, so this story adds the dates and the approver reference by its migration, as legacy AC3 needs an approved version with a valid-from (GAP-2263; ASM-3727). The rights of the four operations are Platform administration `R` for the three reads and `C` for the load, as TSD P4 v3 T6.1 gives them (ASM-1454). Field IDs are those of the Logical Data Model and Data Dictionary v9; the legacy physical names `role` and `permission` are kept.

### 12. Contract

Contract version built against: Not specified in the source documents (DOR-RWB-P4-AD002-APP-23).

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`. The four paths are fixed by RWB-P4-AD002-CON and have no ownership-map row and no T-A row — **Not specified in the source documents (GAP-2263; ASM-1453)**.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/access/v1/admin/permission-matrix` | The matrix rows in force on the date asked: role code and name, class, default scope, area, letters, version label. Query `roleCode`, `capabilityArea`, `matrixVersion`, `validOn`, `page`, `size` | Platform administration `R` | Read only |
| POST | `/api/recovery/access/v1/admin/permission-matrix-loads` | Load a matrix file with its label and valid-from; check it whole and store the version VALIDATED | Platform administration `C` | `Idempotency-Key`; the same key returns the first answer |
| GET | `/api/recovery/access/v1/admin/permission-matrix-versions/{matrixVersion}` | One version by label: status, dates, counts, author and approver references, decision-record reference and rows | Platform administration `R` | Read only |
| GET | `/api/recovery/access/v1/admin/permission-matrix-versions` | The versions with status, dates and row counts. Query `status`, `page`, `size` | Platform administration `R` | Read only |

`GET /admin/roles` (API-P4-007) and `GET /me/session` (API-P4-012) are the service's own and are not restated here; the role rows, their scope, their conflicts and the masking policy are RWB-P4-E1019-APP's, RWB-P4-E1037-APP's and RWB-P4-E1037-CON's.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case`, RWB-P3-E1042-CON (DP-06) | The approver role `rwb.refload.approver.permission`, so the role a version waits for is data (ASM-3728) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case`, RWB-P3-E1043-CON (DP-07) | LOV-CAPABILITY and its 14 values in force, which a complete matrix must cover |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own), RWB-P4-E1037-CON (DP-08) | The Platform administration `R` or `C` of the caller, with the MSG-P4-002 shape |

`recovery.v_ace_iam_group` (SELECT) is a read-only SQL read and not a call: it is granted and contracted by RWB-P1-E1069-APP (DP-05) and answers the group of the caller, its source system and its `data_as_of`; it is never `public.iam_group`. No other list is resolved, because role class, scope and letters travel as codes in `role` and `permission`.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | Change kind `MATRIX`, the version label, the status VALIDATED, the effective date, the row count and the time; no letters, no user reference, no personal data |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library, consumed by P7 | Entry id, decision code (`AC-VERS`, `AC-DENY`), the version label, the row count and the time |

Both use the CloudEvents 1.0 envelope with id, source, type, specversion, time, subject and datacontenttype. `rwb.access.DoaLimitChanged.v1` is not published here and no second access event name exists for a matrix load (ASM-3730). Consumers refresh their cached permission data on `AccessPolicyChanged` and then resolve the version in force on the date asked, so an unapproved version changes no answer.

#### 12.4 Events consumed

None. rwb-access is a reference-data owner in Architecture v5 slide 14 (events: none), the version in force is read from `rwb_access` on each call, and this story writes no inbox row.

#### 12.5 Workflows and activities

None. The load, the three reads and the publish are synchronous work in the caller's thread. The six-monthly access review (JOB-18, Architecture v5 slide 44) is RWB-P4-AD008-APP's; this story registers no activity on the `rwb-access` queue.

#### 12.6 Schedules

None. No Temporal Schedule and no quartz job sits here: the valid-from date is a row value the read resolves.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `permission` | `rwb_access` | P4 | Writes the rows of each loaded version and reads them; adds the version dates and approver reference (ASM-3727) |
| `role` | `rwb_access` | P4 | Reads the active role codes a file must cover, the name, the class and the default scope; never writes |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_access` | PLT library | Created by the service baseline; the library writes the outbox row and the stored answer |
| `masking_rule`, `role_conflict`, `delegation_limit` | `rwb_access` | P4 | Not read and not written: RWB-P4-AD004-APP's, RWB-P4-E1019-APP's and RWB-P4-E1038-APP's |
| `v_ace_iam_group` | ACE, read-only view | ACE / P1 `rwb-source-data` | Read through the P1 ACE-view contract (DP-05) |
| `lov_value`, `reference_row`, `reference_version` | `rwb_case` | P3 | **Never read by SQL**; LOV-CAPABILITY arrives through the contract (DP-07) |
| `parameter_catalog`, `parameter_value` | `rwb_case` | P3 | **Never read by SQL**; the approver role arrives through the contract (DP-06) |
| `decision_log_entry`, `approval` | `rwb_decision` | P7 | Not read and not written; the local entry is the library's |
| `assignment` | `rwb_case` | P3 | Not read and not written; named by the legacy Data table |
| `document` | `rwb_document` | P5 | Not read and not written; named by the legacy Data table |

No foreign key crosses a schema and no statement names a table outside `rwb_access` except the read-only ACE view of the P1 contract.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| Matrix contract fake (RWB-P4-AD002-CON) | The four paths of 12.1 with `PM-2026.11` in force, `PM-2026.12` VALIDATED and the refused `PM-2026.13` | AC1, AC2, AC3 and every test that reads or writes a version |
| Reference-data fake (RWB-P3-E1043-CON) | LOV-CAPABILITY with its 14 areas in force, and the 503 of an unavailable store | AC1 and AC2, so no area and no count is a constant |
| Parameters fake (RWB-P3-E1042-CON) | `rwb.refload.approver.permission=RW-SECADM` | AC1, so the approver role is data |
| Decision-record fake (RWB-PLT-E1027-CON) | The entry append, the hash-chain check and the 503 with MSG-P7-003 | AC1, AC2 and the NFR case |
| Authorise and guard fake (RWB-PLT-E1037-CON, RWB-P4-E1037-CON) | The `R` and `C` letters of RW-SECADM and RW-PLATADM, MSG-P4-002 for a role without them and MSG-P4-001 for no role | AC1 and AC3 |
| Gateway-bff route fake (RWB-PLT-N001-CON) | The SCR-43 route with the matrix rows, the versions and the access log | AC1 and AC3 |
| rwb-source-data contract fake | The group of the loader through the P1 ACE-view contract, with its source system and a `data_as_of` | AC1 |

Fake library version for the rwb-case contract fakes (RWB-P3-E1042-CON, RWB-P3-E1043-CON): Not specified in the source documents (DOR-RWB-P4-AD002-APP-22).

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 operations under `/api/recovery/access/v1` | 3 operations | OpenAPI 3.1, one hop, 2 s timeout; plus one read-only SQL read of the ACE view |
| Kafka | 2 published | 0 | `rwb.access.AccessPolicyChanged.v1` and the library's `rwb.decision.DecisionRecorded.v1` |
| Temporal | None | None | No workflow, activity or Schedule |
| File | None at run time | None | The matrix file arrives in the multipart body of the load and is not stored as a file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.permissionmatrix`, in the service root `th.co.scb.ace.workbench.recovery.access`; base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1`, queue `rwb-access` (unused here).

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

DP-03 is the entry of every load and refusal with its outbox row. DP-05 is the read-only view that answers the group of the loader; the view and its grant come from RWB-P1-E1069-APP and add no dependency here. DP-06 is the approver role as data. DP-07 is the 14 areas as data. DP-08 is the guard that resolves the letters and checks every endpoint against the version in force. DP-13 is the base of the four operations. DP-19 is the composite route of SCR-43. The outbox relay and the inbox are the service template's objects and add no dependency.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V4001_2__permission_matrix_version.sql` | Migration | Adds the valid-from, valid-to and approver-reference columns of a version to `permission`, a unique key on (matrix_version, role_id, capability_area) and an index for the version-in-force read |
| `PermissionMatrixChecks` | Service | The whole-file checks of BR2 and BR3: one row per active role per area, letters, duplicates, unknown role codes, label, valid-from, required fields |
| `PermissionMatrixRepository` | Repository | Reads the rows in force on a date, one version by label and the versions; writes the rows of a new version in one transaction |
| `PermissionMatrixService` | Service | Assembles the three answers, resolves the version in force, computes the expected row count from `role` and LOV-CAPABILITY and writes the version VALIDATED |
| `CapabilityAreaReader` | Client | LOV-CAPABILITY through DP-07 with the 2 s budget and the 503 with MSG-GEN-006 |
| `ApproverParameterClient` | Client | `rwb.refload.approver.permission` through DP-06; no approver role in code |
| `MatrixVersionRecorder` | Service | Writes the `AC-VERS` and `AC-DENY` entries through DP-03 and the outbox row of the event |
| `AceGroupReader` | Client | Reads `v_ace_iam_group` read-only through the P1 contract with `data_as_of` |

**Database and migrations**

- Writes `permission` in `rwb_access` only: the rows of a version and its dates and approver reference; it changes no column of `role`.
- `V4001_2__permission_matrix_version.sql` sits on the per-service Flyway sequence after the V0001 baseline (DP-15); it drops nothing and copies no ACE value.
- The read predicate is the version whose valid-from is the latest not after the day asked and whose state is APPROVED or IN_FORCE; the version is a value, never a date in code.
- A new version is written by insert only; no update rewrites the rows of a stored version. The approval and the rollback are RWB-P4-AD010-APP's writes.
- DB access uses the per-service login (DP-02); no grant on any schema other than `rwb_access` or on `public` is added beyond the SELECT on the ACE view that RWB-P1-E1069-APP grants.

**Configuration and reference data**

- Labels, dates, letters and role codes are rows of the file and of `permission`; none is a constant (BR1).
- The approver role arrives as `rwb.refload.approver.permission` (DP-06) and the 14 areas as LOV-CAPABILITY (DP-07).
- `PM-2026.11`, `PM-2026.12` with 756 rows and the refused `PM-2026.13` are the values of the criteria and the tests (ASM-3729).
- No feature switch: a matrix changes by rows and dates, not by a flag.

**Build steps**

1. The migration with the date and approver columns, the unique key and the index, plus a fixture that applies it twice; test AC1.
2. `CapabilityAreaReader` and `ApproverParameterClient` over their fakes; test AC1.
3. `PermissionMatrixChecks` with one failing fixture per rule — a missing role, a duplicated pair, an invalid letter string, an unknown role code, an empty label, a label over 20 characters, a valid-from in the past; test AC2.
4. `PermissionMatrixRepository` and `PermissionMatrixService` with the version written VALIDATED, the version-in-force resolution on a fixed clock and the computed row count; tests AC1 and AC3.
5. `MatrixVersionRecorder` with the `AC-VERS` entry, the outbox row and the forced failure answering 503 with MSG-P7-003; tests AC1 and the NFR case.
6. The four operations with the `R` and `C` letters through the guard, and the `AC-DENY` entry of a refusal; test AC1.
7. The publication with change kind `MATRIX` after commit, and the assertion that nothing is published when the transaction fails; test AC1.
8. `AceGroupReader` over the ACE-view fake with `data_as_of`, and the 503 when the view cannot be read.
9. The boundary check: no statement names a `public` table, a `v_ace_*` view other than `v_ace_iam_group` or a table of another service; BND-6 of RWB-P4-E1069-APP stays green.

**Done when.** The tests of section 16 pass; `permission` holds `PM-2026.11` in force and `PM-2026.12` VALIDATED with its valid-from; a file with a role missing is refused in full with the role named; a caller without the letter is refused with MSG-P4-002 and one `AC-DENY` entry is written; a forced record failure leaves nothing stored and answers 503 with MSG-P7-003; the load publishes `rwb.access.AccessPolicyChanged.v1` with change kind `MATRIX`; on its valid-from date the approved version is the one the matrix read and the guard answer; and no statement names a table outside `rwb_access` or a `public` table.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller holds no Recovery Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. | The guard, on all four operations |
| MSG-P4-002 | No Platform administration `R` for a read, or no `C` for the load | You cannot {action} here. Your role does not include it. | The guard, on all four operations |
| MSG-GEN-001 | A required field is empty, the label is too long or the valid-from is in the past | Enter {field}. | The checks, as a 422 with the field |
| MSG-P1-002 | A role is missing, a pair is repeated, a letter is outside the vocabulary or a role code is unknown | The {source} load for {date} was refused: {check}. The previous load is still in use. | The checks, as a 422 naming the gap |
| MSG-GEN-004 | The label already exists, or the version asked for does not exist | Someone else changed this record. Reload it to see their change. | The load and the reads |
| MSG-GEN-006 | LOV-CAPABILITY cannot be read through DP-07 | The reference data is not available. Try again later. | The load, on the reference read |
| MSG-P7-003 | The decision-record entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The load and the refusals, through DP-03 |

Every error is an RFC 9457 problem response with `messageId` set and `detail` carrying the filled text. For MSG-P4-002 the {action} value names the action tried — "load the permission matrix", "read the permission matrix", "read a matrix version", "list the matrix versions" — never a case fact or another person's entitlement. For MSG-P1-002 the {check} value names the failed check, the missing role or the duplicate pair, and {source} and {date} are the label and its valid-from date.

**Note on the legacy message table, carried once.** Legacy RWB-AD-002 lists MSG-P4-004, the break-glass warning "Emergency access is on until {time}. Every action is recorded." No operation of this story produces it: the break-glass grant and its warning are RWB-P4-AD006-APP's and RWB-P4-E1039-APP's. MSG-P4-001, MSG-P4-002, MSG-GEN-001 and MSG-P7-003 are kept as the legacy story has them, MSG-P1-002 keeps its text, and MSG-GEN-004 and MSG-GEN-006 are the service's existing messages for an existing label and an unavailable reference answer.

### 15. Screens and states

No screen is built by this story. SCR-43 Roles and access shows the roles, their permissions, the scope and the group mapping with the access log, and the security administrator, the platform administrator and internal audit read it there; it is served by the gateway-bff composite route of DP-19, which calls the matrix read (or the versions list) and the access-log read in parallel, one hop each. The screen field list, the column order and the merge are the screen owner's, and this story returns the rows and the versions only. Where the load form sits is **Not specified in the source documents (GAP-2263; ASM-3731)**.

| Screen | State | What the operator sees |
|---|---|---|
| SCR-43 Roles and access | List | The matrix rows in force: role code and name, area, letters and the version label |
| SCR-43 Roles and access | Versions | The labels with their status (VALIDATED, APPROVED, IN_FORCE, SUPERSEDED), their dates and row counts |
| SCR-43 Roles and access | Load | The load form: file, version label and valid-from, with the checks answered field by field |
| SCR-43 Roles and access | Loaded | The new version with status VALIDATED, its row count, commit time, decision-record reference and the role it waits for |
| SCR-43 Roles and access | Refused | MSG-P1-002 with the missing role or duplicate pair, or MSG-GEN-001 with the field |
| SCR-43 Roles and access | Refused, no right | MSG-P4-002 or MSG-P4-001, with no row and no version |
| SCR-43 Roles and access | Not available | MSG-GEN-006 for the reference list and MSG-P7-003 for the record, each with its retry advice |
| SCR-43 Roles and access | Empty | Not specified in the source documents (CG-ALL-4540) |
| SCR-43 Roles and access | Loading | Not specified in the source documents (CG-ALL-4540) |
| SCR-43 Roles and access | Error | Not specified in the source documents (CG-ALL-4540) |
| SCR-43 Roles and access | No access | Not specified in the source documents (CG-ALL-4540) |

The legacy pair SCR-39 Rules and parameters ("versions; load; approval") and SCR-40 Reference data ("versions; load") is not served by this story: the rule versions are RWB-P4-AD011-APP's and the reference lists are RWB-P4-AD009-APP's and RWB-P4-AD010-APP's. The empty, loading, error and no access states of SCR-39 and SCR-40 are Not specified in the source documents (CG-ALL-4538; CG-ALL-4539).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-002-01 | AC1 | End to end | Legacy test "Load a matrix version": `PM-2026.12` covers every active role of SIT once against the 14 areas with validFrom 1 December 2026; the load answers 201 with status VALIDATED, 756 rows and the approver role `RW-SECADM` from the parameter; the version waits for the approval and no endpoint answers it as in force before its date |
| TC-AD-002-02 | AC2 | End to end | Legacy test "Incomplete matrix refused": the file omits one role of the roster; 422 with MSG-P1-002 naming that role, no row of the version stored, `PM-2026.11` stays in force; a duplicated pair and the letters "RX" are refused with the same message |
| TC-AD-002-03 | AC3 | End to end | Legacy test "Takes effect on its date": `PM-2026.12` approved with validFrom 1 December 2026 on a fixed clock; on 30 November 2026 the matrix read and the guard answer `PM-2026.11`, on 1 December 2026 they answer `PM-2026.12`, with no deployment between the reads |
| TC-AD-002-04 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002": a caller holding `RW-PHONECOL` with no Platform administration letter calls the load and the three reads; 403 with MSG-P4-002 on each, one `AC-DENY` entry each, no row written |
| TC-AD-002-05 | Principle 5 | NFR | Legacy test "A forced decision log write failure stops the action with MSG-P7-003": the decision-record write forced to fail on a load; 503 with MSG-P7-003, no `permission` row stored, `PM-2026.11` unchanged and no event published |
| TC-AD-002-06 | AC1, AC6 | Contract | Contract test of the four operations, the event and the activities of section 12 against the matrix contract fake (RWB-P4-AD002-CON); a repeated load with the same `Idempotency-Key` answers the first answer and stores no second version |
| TC-AD-002-07 | AC1 | Component | Boundary test of the tables of section 12.7 (ASM-3438): only `permission` and `role` in `rwb_access` are read or written; no statement names a table of another service, a `public` table or a `v_ace_*` view other than `v_ace_iam_group`; LOV-CAPABILITY and the approver role come through the contracts only |
| TC-AD-002-08 | AC4 | Not specified in the source documents (NEWAC-RWB-P4-AD002-APP-AC4) | Not specified in the source documents (NEWAC-RWB-P4-AD002-APP-AC4) |
| TC-AD-002-09 | AC5 | Not specified in the source documents (NEWAC-RWB-P4-AD002-APP-AC5) | Not specified in the source documents (NEWAC-RWB-P4-AD002-APP-AC5) |
| TC-AD-002-10 | AC6 | Not specified in the source documents (NEWAC-RWB-P4-AD002-APP-AC6) | Not specified in the source documents (NEWAC-RWB-P4-AD002-APP-AC6) |
| TC-AD-002-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-P4-AD002-APP-AC7) |

The five legacy test cases keep their IDs and their legacy Covers values; the legacy test name is written in the Data column and the Level column follows Template and Rules §R7.2 — the three criteria are end-to-end tests of the loaded version, the legacy level Access maps to Component and Principle 5 maps to NFR. The full test with its Given, When and Then is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. The ITG copy of the set is the integration harness's and is not written here, so no `-ITG` id appears.

### 17. Guardrails

- No business value in code: labels, dates, letters, role codes, the 14 areas and the approver role are rows and contract answers, and a test proves that a new version and a new area list need no build (BR1, BR10).
- No personal data anywhere: a matrix row is a role code, an area and letters, an entry carries a user reference and no name, and no test row, log, event or prompt holds a name or an e-mail address.
- No read of another schema (DP-01): the reference, parameter and ledger tables, `assignment` and `document` are never read by SQL; the only external read is the read-only ACE view `v_ace_iam_group`.
- ACE data only through the owner's contract or the service's own `v_ace_*` view (DP-05): no statement names `public.iam_group`, a `public` table or a table of another service, and BND-6 of RWB-P4-E1069-APP stays green.
- One writer for the matrix: only this story's load writes the rows of a new version, a stored version is never edited, and the state changes after VALIDATED are the approval stories' (BR4, BR5).
- Default deny on every call: a missing role is 401 and a missing letter is 403 with MSG-P4-002, never an allow (BR7).
- A complete file or nothing: a refused load leaves the version in force untouched, so a partial load can never remove a right quietly (BR2).
- A version answers whole or not at all, and an unapproved version is never answered as the matrix in force (BR6).
- One migration per story on the service's own Flyway sequence (DP-15); one event name with change kind `MATRIX` (BR9).

### 18. Traceability

No requirement ID is recorded for legacy RWB-AD-002 in TSD P4 v3 T8, and the Work Package carries the requirement list of this key as empty; TSD P4 v3 T8 records REQ-ACA-003 against FEAT-ACA-01 and RWB-E1-022. The key serves FEAT-ACA-04 (hold the role to permission matrix as data) and FEAT-ADM-01 (run the full administration screens) of FSD P4 v3.

| Feature | Where this story answers it | Test cases | L3 process |
|---|---|---|---|
| FEAT-ACA-04, hold the role to permission matrix as data | The matrix as rows with a label, a status and an effective date, changed without a release (sections 4, 8, 11) | TC-AD-002-01, TC-AD-002-03 | Not specified in the source documents (DOR-RWB-P4-AD002-APP-2) |
| FEAT-ADM-01, the full administration screens | The four operations behind SCR-43 and the composite route (12.1, 15) | TC-AD-002-04 | Not specified in the source documents (DOR-RWB-P4-AD002-APP-2) |
| The whole-file refusal with the missing role named | MSG-P1-002 and no row stored (sections 5, 14) | TC-AD-002-02 | Not specified in the source documents (DOR-RWB-P4-AD002-APP-2) |
| The record-before-change rule | The `AC-VERS` entry of DP-03 before the matrix stands (sections 4, 14) | TC-AD-002-05 | Not specified in the source documents (DOR-RWB-P4-AD002-APP-2) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-AD002-CON | Contract | H: the matrix contract, its four schemas, the whole-matrix and effective-date rules, the event declaration and the fakes |
| RWB-P4-E1037-CON, RWB-P4-E1037-APP | Contract; App development | H (contract): the authorise contract and the guard that checks every endpoint against the version in force |
| RWB-P4-AD010-APP | App development | The approval, verify and rollback of a loaded version; this story stops at VALIDATED |
| RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON | Contract | H: the record library, the parameters and reference-data libraries, the guard library and the composite route |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the parameters and reference-data contracts that answer the approver role and the 14 areas |
| RWB-P1-E1069-APP | App development | The ACE view `v_ace_iam_group` and its SELECT grant, read read-only; named, not on the build row |
| RWB-P4-E1019-APP | App development | The role rows, classes, scopes and conflicts this story reads |
| RWB-P4-AD001-APP, RWB-P4-AD004-APP, RWB-P4-AD005-APP, RWB-P4-AD008-APP | App development | Sibling slices of the same module: group mapping, masking profiles, separation of duty, access review |

| Legacy reference | Where it is kept |
|---|---|
| The story statement (the matrix of roles against the 14 capability areas as a versioned file) | Sections 1, 2, 8 (BR1, BR2) |
| Legacy AC1, AC2 and AC3, word for word with their origin tags | Section 7 |
| The Data rows `permission` DF-REF-040 to DF-REF-044 and `role` DF-REF-034 to DF-REF-038 | Section 11 |
| The `assignment` and `document` rows of the legacy Data table | Section 11; another service's, not read here |
| The legacy endpoints `POST /admin/rule-versions/{versionId}/approve` and `POST /admin/reference-loads` | Section 19; other owners, not carried |
| The permission checks Reference data and Rules and parameters | Sections 8 (BR7), 10; not kept for the matrix (ASM-1454) |
| MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P1-002, MSG-P7-003 and the break-glass warning MSG-P4-004 | Section 14, exception paths |
| Screens SCR-39, SCR-40 and SCR-43 | Section 15 |
| Legacy test cases TC-AD-002-01 to TC-AD-002-05 | Section 16 |

### 19. Out of scope

- The approval of a matrix version, the verify and the rollback of a loaded version: RWB-P4-AD010-APP (legacy RWB-AD-010), with RWB-P4-AD009-APP for the rollback of a configuration version. This story ends at VALIDATED and never writes APPROVED or IN_FORCE.
- The legacy endpoint `POST /admin/rule-versions/{versionId}/approve` under the monolith base that DP-13 replaces: the rule-version approve, the rule packages and the registry belong to the rule-version stories of this service and P7 rwb-decision (ASM-0040); no path of it is carried here.
- The legacy endpoint `POST /admin/reference-loads` under the same base: the generic reference-load path and its store belong to P3 rwb-case (ASM-0041) with the approval in RWB-P4-AD010-APP; this story provides neither and calls neither.
- The roles catalogue `GET /admin/roles` (API-P4-007), the role rows, classes, scopes, role conflicts and masking rules: RWB-P4-E1019-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON.
- The masking profiles per role, the separation-of-duty check, the group-to-role mapping, the access review list and its Schedule (JOB-18), the access-log search and the break-glass grant: RWB-P4-AD004-APP, RWB-P4-AD005-APP, RWB-P4-AD001-APP, RWB-P4-AD008-APP, RWB-P4-AD007-APP, RWB-P4-AD006-APP and RWB-P4-E1039-APP.
- The reference data and the parameter values of the estate, including LOV-CAPABILITY and the approver role: P3 rwb-case under DP-06 and DP-07; this story consumes them and holds no such row.
- The central decision ledger and its query: P7 rwb-decision; this story writes the local entry only.
- `assignment` and `document`: P3 rwb-case and P5 rwb-document, named by the legacy Data table and not read here.
- The delegation of authority table and its limits: RWB-P4-E1038-APP and RWB-P4-E2013-APP.
- The Helm chart, topic creation, metrics, alerts and runbook of this capability (an OPS story of this legacy key), and the integration harness with its `-ITG` copies of the test cases.
