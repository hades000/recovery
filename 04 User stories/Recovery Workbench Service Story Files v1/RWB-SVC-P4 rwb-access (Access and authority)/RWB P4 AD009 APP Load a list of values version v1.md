# RWB-P4-AD009-APP Load a list of values version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD009-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-P4-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-AD009-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-009 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **reference data administrator, and the access service that holds the administration console's door**, I want **a list of values loaded from a file as a new version with a valid-from date, after a set of checks that name the failing row, the failing field and the count of records that still use a value code I am removing**, so that **a code list changes without a code release, an administrator cannot remove a code that open cases still use, and the decision record shows who loaded which version, how many rows it carried and what the checks answered**.

Inside `rwb-access` this is the administration-ingest slice of the legacy story RWB-AD-009:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- **The split, stated plainly.** Under the R-PREC default ruling the list-of-values rows — `lov_value` (DF-REF-027 to DF-REF-033), `reference_version` and `reference_row` — and the reference-load operations belong to P3 `rwb-case` (ASM-0071, ASM-0041). `rwb-access` therefore writes no `lov_value` row and creates no reference table of its own. What this story owns is the **console ingest and its checks**: the endpoint the administration screen calls, the authority check behind it, the file checks, the usage check, and the decision record of an accepted or a refused load. The rows are stored and versioned by `rwb-case` through its own contract, and the public path the console uses is reconciled at contract review before it is frozen (GAP-0811; ASM-1512).
- **Provided by this story**, under the access base of DP-13: `POST /api/recovery/access/v1/admin/lov-loads` — multipart `file` with query `lovCode` and `validFrom`, header `Idempotency-Key`; it parses the file, runs the checks, hands the accepted rows to the `rwb-case` reference-data contract and answers `loadId`, `lovCode`, `validFrom`, `rowCount`, `checks` and `state` (LOADED or REFUSED), on the Reference data C right. And `GET /api/recovery/access/v1/admin/lov-loads/{loadId}` — the load, its check result and its state, on the Reference data R right.
- **Consumed:** `POST /api/recovery/case/v1/admin/reference-loads` (the owner stores and versions the rows and answers LOADED), `GET /api/recovery/case/v1/admin/lists/{listCode}` (the list in force and the count of records using a value code), the parameters and reference-data reads through the DP-06 and DP-07 client libraries, and the service's own `POST /api/recovery/access/v1/authorise` for the right. One hop, 2 s timeout, cached reads.
- **Recorded, not stored:** an accepted load appends one decision-record entry with decision code `REF-LOAD` and a refused load one with `REF-DENY` — the list code, the version, the row count, the check result and the time, and no personal data (DP-03).
- **Not in this story:** the approval of the load and its rollback (RWB-P4-AD010-APP), the rule-version endpoints and the rule screens (RWB-P4-AD011-APP), the `lov_value` table and the reference-load endpoints themselves (P3 `rwb-case`), and the reference data itself.

### 2. Business rationale

Reference data is the control that lets a code list change without a release (REQ-DRI-011), and the FSD makes it a screen with versions and a load (FEAT-ADM-01, A2.17, REQ-ACA-013). Today the load is a file handed around and put in by hand: nothing names the row that failed, and nothing stops a value code being dropped while open cases still hold it. The legacy story RWB-AD-009 fixed only the second half of that problem and carried a permission table for the rule-version endpoints, which are a different capability. In the target the rows are reference data of `rwb-case` under DP-07, so the only thing `rwb-access` can add is the door and the checks: the console ingest, the authority answer, the file and usage checks, and the record. That is what makes an administrator's load reviewable without giving the access service a second copy of a versioned table (DP-01).

The story serves REQ-DRI-011 by making the version, its valid-from date, its row count and its author-and-approver path visible to the reference-data service, REQ-DRI-010 by making the caps and the enabled lists parameters rather than constants, and REQ-ACA-013 by putting the load on the administration screen SCR-40 with its four states for the security administrator and the reference data administrator. It supports the measure *rule and limit changes made without a code release*, target 100 percent (FSD P4 v3 A2.17.1), and it carries the two universal rules that a version applies from its effective date (R-UNI-38) and that no action proceeds unlogged (R-UNI-39).

The FSD module file has **no section for a list-of-values load**: A2.17 covers the administration screens as a whole and its field catalog is the role and permission screen (FSD P4 v3 A2.17.3.2), so the load's own steps and checks come from the legacy story and from the TSD, and their detail is a documented gap (GAP-0814; ASM-1515).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD009-CON (same service, its own contract story) | The published contract baseline: the two console operations, the `LovLoad` and `LovLoadCheck` schemas, the state set LOADED and REFUSED, the error envelope and the message IDs, and the fakes |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the `REF-LOAD` and `REF-DENY` entries of every load |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the file-size cap, the row cap and the enabled lists |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): the lists, their versions and the usage count of a value code |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19), through which SCR-40 loads the file and reads the answer |
| RWB-P4-E1037-CON (same service, its own contract story) | The authorise shape and the refusal with MSG-P4-002 that every operation of this service uses; this story adds no dependency of its own on it |
| RWB-P4-E1038-APP (same service, its own story) | The service's per-service login, schema and Flyway sequence, in which `role` and `permission` and the library tables already exist |

Business preconditions carried from RWB-AD-009:

- The list `LOV-ROUTE` is a list of values with codes and English labels, and its rows are `value_code`, `label_en`, `label_th`, `sort_order` and `valid_from` (TSD P4 v3 T3.1, DF-REF-027 to DF-REF-033, held by P3 under ASM-0071).
- A load that removes a value code still used by open cases is refused with the count of records using the code (legacy AC2). The source and scope of that count are Not specified in the source documents (GAP-0813; ASM-1514): the story reads it from the owner's usage check and never recomputes it.
- The file format is Not specified in the source documents (GAP-0812; ASM-1513): a CSV or XLSX file with a header row and the five columns of `lov_value`.
- The checks other than the English label are Not specified in the source documents (GAP-0814; ASM-1515): parse, required columns, required English label, duplicate value code in the file and in the list, unknown list code, valid-from present, Thai label optional.
- The file-size and row caps are Not specified in the source documents (GAP-0815; ASM-1516): 5 MB and 5,000 rows, and 422 above either. Both are parameter rows, not constants.

### 4. Flow

1. The reference data administrator opens SCR-40 through the gateway-bff composite route of DP-19, picks the list, picks a file and a valid-from date, and submits.
2. `POST /api/recovery/access/v1/admin/lov-loads` arrives as `multipart/form-data` with the part `file` and the query parameters `lovCode` and `validFrom`, and the header `Idempotency-Key`. The controller validates the query: `lovCode` and `validFrom` are required and a missing one is 422 with MSG-GEN-001 naming the field.
3. The controller resolves the caller's role through the service's own `v_ace_iam_group` read (DP-05) and reads the `permission` row of that role in the capability area Reference data. A caller without the C letter is refused with 403 and MSG-P4-002, and one `REF-DENY` entry is written with the caller reference, the list code and the right asked (AC4).
4. Idempotency: the service looks up the `Idempotency-Key` and the digest of the file. A key already used with the same digest answers the load it answered the first time, with the same `loadId` and `rowCount`, and stores no second version (AC5, R-UNI-40).
5. `LovFileParser` reads the file as CSV or XLSX and requires a header row with the columns `value_code`, `label_en`, `label_th`, `sort_order` and `valid_from`. The size and row caps come from the parameter rows read through DP-06; a file above either cap is 422 with MSG-GEN-001 named on `file`.
6. `LovLoadCheckService` runs the row checks: `label_en` is required on every row, `value_code` is required and unique within the file, `sort_order` and `valid_from` are required where the column exists, and the Thai label is optional. A failure is 422 with MSG-GEN-001 naming the field and the row number, and nothing is sent to the owner (AC3).
7. The list code is resolved through the reference-data contract of DP-07 against the lists this service is enabled for. An unknown list code is 422 with MSG-GEN-001 named on `lovCode`.
8. `UsageReader` reads `GET /api/recovery/case/v1/admin/lists/{listCode}` from `rwb-case`: the list in force and, for each value code, the count of records using it. A value code present in the list in force and absent from the file with a count above zero refuses the load with 409 carrying `valueCode` and `count`, and one `REF-DENY` entry is written (AC2). The count is returned by the owner; it is never recomputed from a table of this service.
9. On a pass, the service hands the file to `POST /api/recovery/case/v1/admin/reference-loads` of `rwb-case` with the list as the table and `validFrom`. The owner stores the rows, versions them and answers the load with its `loadId` in state `LOADED`. This service writes no `lov_value` row, no `reference_version` row and no `reference_row` row (ASM-0071).
10. The service appends one decision-record entry with decision code `REF-LOAD`, carrying the list code, the version, the row count, the check result and the time, and no personal data. The record, the idempotency row and the answer commit in one local transaction.
11. The endpoint answers 201 with `loadId`, `lovCode`, `validFrom`, `rowCount`, `checks` (one line per check with its result) and `state` = `LOADED`. The load waits for the list owner's approval, which is RWB-P4-AD010-APP's.
12. `GET /api/recovery/access/v1/admin/lov-loads/{loadId}` answers the load, its check result and its state on the Reference data R right; the state and the row count are read from the owner contract, and the local record is read for who loaded it and when. An unknown `loadId` is 404.
13. Where `rwb-case` does not answer inside the 2 s budget or answers 5xx, the endpoint answers 503 and no load is recorded and no record is written. Where the record cannot be written, the local transaction rolls back, the endpoint answers 503 with MSG-P7-003 and nothing is answered; the operator retries the same file with the same `Idempotency-Key`, which finds the owner's load and completes the record before answering (R-UNI-39).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `lovCode`, `validFrom` or the `file` part is missing | 422, no parse and no record | MSG-GEN-001 | AC3 |
| X2 | A row has no `label_en` | 422 naming `label_en` and the row number; nothing is sent to the owner | MSG-GEN-001 | AC3 |
| X3 | A `value_code` repeats within the file or against the list in force | 422 naming `value_code` and the row number; nothing is sent to the owner | MSG-GEN-001 | AC3 |
| X4 | The list code is not an enabled reference list | 422 naming `lovCode` | MSG-GEN-001 | AC3 |
| X5 | The load removes a value code with a count above zero | 409 with `valueCode` and `count`, one `REF-DENY` entry; the list in force is unchanged | MSG-GEN-004, with the count in the body | AC2 |
| X6 | The file exceeds the size or row cap | 422 naming `file`; nothing is parsed beyond the cap | MSG-GEN-001 | AC3 |
| X7 | The loader holds no C letter in Reference data | 403, one `REF-DENY` entry with the role, the list and the right; nothing is parsed | MSG-P4-002 | AC4 |
| X8 | The `rwb-case` reference-data contract does not answer | 503, no load, no record; a retry of the same file with the same key is safe | None (RFC 9457 problem with the trace identifier) | AC5 |
| X9 | The decision record cannot be written | The local transaction rolls back and the endpoint answers 503 with MSG-P7-003; no answer is issued | MSG-P7-003 | AC4 |
| X10 | A replayed request with a different file under the same `Idempotency-Key` | 422 naming the key; the first answer is not returned and no version is stored | MSG-GEN-001 | AC5 |

No exception path of this story writes a `lov_value` row, changes a version and approves a load: the rows are `rwb-case`'s and the approval is RWB-P4-AD010-APP's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the contract of RWB-P4-AD009-CON and the fakes of the reference-data, parameters and decision-record libraries; no other story of the lane has to exist in the environment |
| Negotiable | The checks, the caps, the file format and the enabling of a list are modelled as parameter and reference rows, so the review can widen or narrow them without a rewrite |
| Valuable | One door and one check set replace a manual file load with no row-level diagnosis and no usage guard |
| Estimable | Two endpoints, one parser, one check service, one usage read, one record appender and two client libraries |
| Small | Fits two weeks with its tests; there is no table of its own, no workflow and no approval in it |
| Testable | Each criterion has a component test against the fakes, and the refusal and replay rules are asserted on the record and on the answer |

### 7. Acceptance criteria

```gherkin
Feature: Load a list of values version

  Background:
    Given the environment is SIT
    Given the reference data administrator holds RW-REFADM with the C letter in the capability area Reference data
    Given the list "LOV-ROUTE" is an enabled reference list with 12 values in force

  Scenario: AC1 Valid load (legacy RWB-AD-009 AC1)
    Given the rwb-case contract mock returns load "RL-2026-014" in state "LOADED" with 12 rows accepted for LOV-ROUTE from 1 January 2027
    Given a file for LOV-ROUTE with codes and English labels
    When I load it
    Then it passes the checks and waits for the list owner's approval

  Scenario: AC2 Code in use removed (legacy RWB-AD-009 AC2)
    Given the rwb-case contract mock returns 37 open cases using code "R2" of LOV-ROUTE
    Given a load that removes a code used by open cases
    When it is loaded
    Then the system refuses it with the count of records using the code

  Scenario: AC3 A row without an English label or with a duplicate code is refused with its row (new, D-RCV-60)
    Given a file for LOV-ROUTE whose row 4 has no label_en and whose row 7 repeats value_code "R2" of row 3
    When the file is posted to POST /api/recovery/access/v1/admin/lov-loads with lovCode "LOV-ROUTE", validFrom "2027-01-01" and an Idempotency-Key
    Then the response is 422 with message MSG-GEN-001 naming "label_en" and row 4
    Then a second file with only the duplicate is 422 naming "value_code" and row 7
    Then the rwb-case reference-load operation is not called and no version is stored

  Scenario: AC4 A loader without the reference data right is refused and every load is recorded (new, D-RCV-60)
    Given test user "U-9410" holds RW-CASEOWN with the R letter only in Reference data
    When "U-9410" posts a valid file for LOV-ROUTE
    Then the response is 403 with message MSG-P4-002 and the file is not parsed
    Then one decision-record entry is written with decision code "REF-DENY", the role, the list and the right "C"
    Given the reference data administrator loads the valid file of AC1
    Then one decision-record entry is written with decision code "REF-LOAD", list "LOV-ROUTE", version "RL-2026-014", rowCount 12 and the check result
    Then neither entry carries a name, an e-mail address or any personal field

  Scenario: AC5 The same file sent twice with the same key answers the first load (new, D-RCV-60)
    Given the accepted load "RL-2026-014" of AC1 with its Idempotency-Key
    When the same file is posted again with the same Idempotency-Key
    Then the response is 200 with the same loadId "RL-2026-014", rowCount 12 and state "LOADED"
    Then the rwb-case reference-load operation is not called a second time and no second version is stored
    Then one idempotency hit is recorded and no second REF-LOAD entry is written
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A list of values is loaded as a new version with a valid-from date; the accepted rows are stored and versioned by `rwb-case`, and this service writes no `lov_value`, `reference_version` or `reference_row` row | REQ-DRI-011; ASM-0071 |
| BR2 | The list rows and the reference-load operations are `rwb-case`'s (ASM-0041); this service provides the console ingest and its checks under its own base, and the public console path is reconciled at contract review | GAP-0811; ASM-1512 |
| BR3 | The file is a CSV or XLSX with a header row and the columns `value_code`, `label_en`, `label_th`, `sort_order` and `valid_from`, which are the columns of `lov_value` | TSD P4 v3 T3.1, DF-REF-027 to DF-REF-033; ASM-1513 |
| BR4 | `label_en` is required on every row, `value_code` is unique within the file and against the list in force, the list code is known and `valid_from` is present; the Thai label is optional | Legacy AC1; ASM-1515 |
| BR5 | A load that removes a value code still used by open cases is refused with the count of records using the code, and the count comes from the owner's usage check, never from a table of this service | Legacy AC2; ASM-1514 |
| BR6 | The file-size and row caps are parameter rows read through DP-06 and are not constants in code | REQ-DRI-010; ASM-1516 |
| BR7 | The load requires the C letter in Reference data and the read requires R; a role without the right is refused with MSG-P4-002 and the refusal is recorded | TSD P4 v3 T6.1; REQ-ACA-013 |
| BR8 | A replay of the same file with the same `Idempotency-Key` answers the first load and stores no second version; the same key with a different file is refused | R-UNI-40; Architecture v5 slide 11 |
| BR9 | An accepted load writes one `REF-LOAD` entry and a refused load one `REF-DENY` entry, with no personal data; an answer that cannot be recorded is not returned | R-UNI-39; DP-03 |
| BR10 | No business value in code: the enabled lists and their versions are reference data (DP-07), and the caps, the column names and the limits are parameters or reference data (DP-06) | FSD P4 v3 BR-P4-017; A2.17.3.1 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is one call to the owner's reference-load operation and no write statement in this service; the version the owner answers is the version the record names.
- BR2 is the reason the story exists at all: the legacy story's rule-version endpoints (`/admin/rule-versions` and its approve) are P7 `rwb-decision`'s under ASM-0040 and are RWB-P4-AD011-APP's here, and the `lov_value` table is P3's under ASM-0071, so the access service keeps the door and the checks and gives up the storage.
- BR4 is a row walk of the parsed file plus one comparison against the list in force; the row number is carried into the problem response so the administrator can fix the file without guessing.
- BR5 is a comparison of the value codes in the file against the usage counts of the owner's list read; the count in the refusal is copied from that answer character for character.
- BR6 is a parameter read before the file is parsed, so an oversized file is refused before a byte of it is interpreted.
- BR8 is the idempotency row of the library keyed on the key and the file digest; a second call inside the window returns the stored answer and writes no second `REF-LOAD` entry.
- BR9 is the record appender of DP-03 inside the transaction that produces the answer.

### 9. State transitions

This service holds no list-of-values version: the states below are the lifecycle of a load in `rwb-case`, which this story starts in `LOADED` or `REFUSED` and RWB-P4-AD010-APP moves on. The state names are the values of LOV-VERSION-STATUS (TSD P4 v3 T3.2), and `VALIDATED` is in that list but is not produced by this story's two answers.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | A file is posted and every check passes | The owner stores the rows and versions them | `LOADED` |
| (none) | A file is posted and a file or list check fails | 422, nothing reaches the owner | `REFUSED` |
| (none) | A file is posted and a value code in use would be removed | 409 with the count, nothing reaches the owner | `REFUSED` |
| `LOADED` | The list owner approves the version | A second person with the A letter in Reference data (RWB-P4-AD010-APP) | `APPROVED` |
| `APPROVED` | The valid-from date is reached | The date passes | `IN_FORCE` |
| `IN_FORCE` | A newer version reaches its valid-from date | R-UNI-38: decisions from that date use the new version | `SUPERSEDED` |
| `IN_FORCE` | A rollback is recorded | RWB-P4-AD010-APP | `ROLLED_BACK` |
| `REFUSED` | A corrected file is posted | None: a refusal is terminal and the next file is a new load | A new load |

| Command | Condition | Outcome |
|---|---|---|
| Load a list of values | C letter in Reference data, all checks pass, owner answers | 201, `LOADED`, one `REF-LOAD` entry |
| Load a list of values | No C letter | 403 MSG-P4-002, one `REF-DENY` entry, no version |
| Load a list of values | A row check fails | 422 MSG-GEN-001 with the field and the row, one `REF-DENY` entry |
| Load a list of values | A value code in use would be removed | 409 MSG-GEN-004 with `valueCode` and `count`, one `REF-DENY` entry |
| Load a list of values | The owner contract does not answer | 503, no version, no entry |
| Read a load | R letter in Reference data | 200 with the state and the check result |
| Read a load | Unknown `loadId` | 404 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM Reference data administrator | C, R, U and D on Reference data in the TSD matrix: post a load, read it and correct a file (TSD P4 v3 T6.1). The T6.1 refinement that withholds upload applies to rule packages, not to reference data |
| RW-COE Center of excellence analyst | CRUD on Reference data in the same matrix: it may post and read a load here; the approval of the version is RWB-P4-AD010-APP's |
| Every other RW- role that holds R on Reference data | Reads a load and its check result; posts nothing |
| RW-RISK Risk and model risk officer | Holds A in the decision-log and rule columns of the matrix; it does not hold C here and posts no load. The legacy story's "Rules and parameters A for RW-RISK" row is the rule-version approval and is RWB-P4-AD011-APP's |
| RW-AUDIT Internal audit | R on Reference data: reads the loads; it reads the entries through the decision log of `rwb-decision` and calls no write operation |
| RW-SECADM Security administrator | R on Reference data and CRUDA on Platform administration: it reaches SCR-40 as the administration screen of REQ-ACA-013 and reads a load |
| `rwb-access` itself | Reads `role` and `permission` in its own schema, reads the group of the loader through its own `v_ace_iam_group` ACE view (DP-05) and writes no personal data |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON, and this story adds none of its own.

### 11. Data

| BR Field ID | Where it lives | Field | Read or write |
|---|---|---|---|
| DF-REF-027 | `lov_value` of P3 `rwb_case` | id | Through the owner contract only; never from a table |
| DF-REF-028 | `lov_value` of P3 | lov_code | Through the owner contract only |
| DF-REF-029 | `lov_value` of P3 | value_code | Checked in the file and against the list in force |
| DF-REF-030 | `lov_value` of P3 | label_en | Required on every row |
| DF-REF-031 | `lov_value` of P3 | label_th | Optional on every row |
| DF-REF-032 | `lov_value` of P3 | sort_order | Required where the column exists |
| DF-REF-033 | `lov_value` of P3 | valid_from | Present on every row and on the load |
| DF-REF-034 to DF-REF-039 | `role` in `rwb_access` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` in `rwb_access` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `REF-LOAD` and `REF-DENY` entries | Write |
| (outbox) | outbox library table in `rwb_access` | the record row | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| (idempotency) | `idempotency_key` in `rwb_access` | the key, the file digest and the stored answer | Write and read |

No `lov_value`, `reference_version`, `reference_row`, `case`, `recovery_case` or `decision_log_entry` row is read or written: the list rows and the versions are `rwb-case`'s (P3, ASM-0071), the case and its records are `rwb-case`'s, and the central ledger is `rwb-decision`'s (P7, ASM-0069). The list, its versions and the usage count arrive in the answers of the `rwb-case` contract, not by a schema read (DP-01, DP-07). Field IDs are those of the Logical Data Model and Data Dictionary v8.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/lov-loads` | P4 `rwb-access` | `multipart/form-data` part `file` (CSV or XLSX); query `lovCode`, `validFrom` (ISO date); header `Idempotency-Key` | 201 `loadId`, `lovCode`, `validFrom`, `rowCount`, `checks[]` (`name`, `result`, `row`, `field`, `detail`), `state` (LOADED, REFUSED) | 400 malformed multipart; 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-GEN-004 with `valueCode` and `count`; 422 MSG-GEN-001 with `field` and `row`; 503 MSG-P7-003 or the owner unavailable | Reference data C | `Idempotency-Key` required |
| GET | `/api/recovery/access/v1/admin/lov-loads/{loadId}` | P4 `rwb-access` | Path `loadId` | 200 `loadId`, `lovCode`, `validFrom`, `rowCount`, `checks[]`, `state`, `loadedBy` (a user reference), `loadedAt` | 401 MSG-P4-001; 403 MSG-P4-002; 404 unknown load; 503 owner unavailable | Reference data R | Not applicable, read only |

The two operations sit under the base `/api/recovery/access/v1` of DP-13. The TSD P4 v3 names the same capability as API-P4-004 `GET /admin/lists/{listCode}` and API-P4-005 `POST /admin/reference-loads` with the request fields `file`, `table` and `validFrom` (T4, T-A.2); under the R-PREC default ruling those paths and those rows are P3 `rwb-case`'s (ASM-0041), so this service keeps the console ingest under its own base and calls the owner operation of 12.2. The TSD's field name `table` is carried here as `lovCode`, because the console loads a list of values only; the two names are reconciled with the owner's contract at the same review that fixes the public console path (GAP-0811; ASM-1512). The `ReferenceLoad` shape of the TSD is carried here as `LovLoad` with `checks[]`, and its field-level detail is Not specified in the source documents (GAP-0814; ASM-1515).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 `rwb-case` | The load: multipart `file`, `table` (the list code) and `validFrom`; the owner stores and versions the rows and answers the load in `LOADED` with its version |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | The list in force and, per value code, the count of records using it; the usage check of BR5 |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own) | The capability-area and letter answer behind the C and R checks; cached for the request |
| (client library) | parameters contract of `rwb-case` | P3 `rwb-case` | DP-06: the file-size cap, the row cap and the enabled lists |
| (client library) | reference-data contract of `rwb-case` | P3 `rwb-case` | DP-07: the list metadata and the version in force used in the answer |

Every call is one hop with a 2 s timeout and a breaker, and the reads are cached for the request and for a short time to key (DP-11).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained `REF-LOAD` or `REF-DENY` entry of a load: the decision code, the list code, the version, the row count, the check result and the time |

No event of this service is published on `rwb.access.events.v1` by this story. The two event types the service owns — `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` (Architecture v5 slide 41) — belong to the role, permission and delegation stories, and a reference-data version is not an access policy. Neither payload here carries a name, an e-mail address or a personal field.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 41 (events IN: none), and this story adds no subscription. The version in force is read from the owner's contract when the load and the read need it, not from an event.

#### 12.5 Workflows and activities

None. The load is a request-driven synchronous operation; it starts no Temporal workflow, registers no activity on the `rwb-access` queue and holds no state between requests beyond the record and the idempotency row.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) and the delegation-of-authority load are Schedules of `rwb-access` and belong to other stories.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role and the class of the loader |
| `permission` | P4 (`rwb_access`) | Read only: the Reference data letters of that role |
| local decision record (DP-03 library table) | PLT library, created in `rwb_access` | Write: one `REF-LOAD` or `REF-DENY` entry per load |
| `outbox_event` | PLT library, created in `rwb_access` | Write: the outbox row of the record |
| `idempotency_key` | PLT library, created in `rwb_access` | Write and read: the key, the file digest and the stored answer |
| `processed_event` | PLT library, created in `rwb_access` | None: no event is consumed |
| `lov_value`, `reference_version`, `reference_row` | P3 (`rwb_case`) | Not read and not written: reference data of P3 under ASM-0071, reached through the DP-07 contract |

This service creates no table for the list rows and declares no reference table of its own. No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case reference-data WireMock | RWB-P3-E1043-CON | `POST /admin/reference-loads` answering load `RL-2026-014` in state `LOADED` with `rowCount` 12 for LOV-ROUTE from 2027-01-01; `GET /admin/lists/{listCode}` for LOV-ROUTE with 12 values in force and 37 open cases on `R2`; a 409 usage answer; a 503 timeout |
| parameters fake | RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The file-size cap, the row cap and the enabled lists, served from the parameter rows |
| authorise and guard fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | Granted for RW-REFADM and RW-COE with Reference data C and R; refused with MSG-P4-002 for RW-CASEOWN with R only |
| access fixture | RWB-P4-E1038-APP | `role` and `permission` rows for RW-REFADM, RW-COE, RW-CASEOWN and RW-AUDIT, and the group mapping read through `v_ace_iam_group` |
| decision-record fake | RWB-PLT-E1027-CON | The record append, the hash-chain check and the forced failure of X9 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed (plus 2 client libraries) | Base `/api/recovery/access/v1`; one hop, 2 s timeout, cached reads |
| Kafka | 1 event type published through the DP-03 library; 0 consumed | `rwb.decision-record.v1`; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | No workflow and no Schedule in this story |
| File | 1 input, 0 output | One `multipart/form-data` upload per load, CSV or XLSX, capped by parameter |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/reference`, Java package `th.co.scb.ace.workbench.recovery.access.reference`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is used for one read only: the group of the loader, resolved through the service's own `v_ace_iam_group` ACE view, so the record names a group and never a person's details. The metadata row names no other pattern, and this story adds no build dependency beyond `RWB-P4-AD009-CON` and the four platform contracts above. The legacy markers this slice replaces are the monolith base `/api/recovery/v1` (DP-13) and the in-process reference-data reader (DP-07, now the owner's contract).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LovLoadController` | Controller | `POST /admin/lov-loads` and `GET /admin/lov-loads/{loadId}`: multipart reading, query validation, the `Idempotency-Key`, RFC 9457 errors |
| `LovFileParser` | Service | CSV and XLSX parsing with a header row, the five columns, and the size and row caps read before parsing |
| `LovLoadCheckService` | Service | The row and list checks of BR3, BR4 and BR6, with the failing row and field in the answer |
| `UsageReader` | Service | The owner's list read and the usage count per value code; no local recomputation |
| `ReferenceLoadClient` | Client | The DP-07 client library call to `POST /admin/reference-loads`, one hop, 2 s, with the breaker |
| `LoadRecordWriter` | Service | The `REF-LOAD` and `REF-DENY` entries and their outbox rows in the transaction that produces the answer |
| `PermissionReader` | Service | The `role` and `permission` rows of the caller and the `v_ace_iam_group` read |

**Database and migrations**

- This story creates no table of its own and owns no Flyway migration for the list rows. `role`, `permission` and the library tables are created by the service baseline in the per-service sequence of the service DB story, and this story reads and writes them.
- No write statement for a list row exists in the codebase of this module: the repository of this story exposes no save, update or delete against a reference table, because the rows are the owner's.
- The record, the outbox row and the idempotency row commit in one local transaction; a failure rolls them back and the answer is withheld with MSG-P7-003.
- The file itself is not stored: the accepted bytes are streamed to the owner's contract and are not written to a local store, and the record names the version rather than the file.

**Configuration and reference data**

- The enabled lists and their versions are reference data read through DP-07 (RWB-P3-E1043-CON); no list code is a constant in code (BR10).
- The file-size cap, the row cap and the column names are parameters read through DP-06 (RWB-P3-E1042-CON). The parameter keys are Not specified in the source documents (GAP-0815; ASM-1516) and the contract review fixes them; the values carried here are 5 MB and 5,000 rows.
- The file format, the columns and the checks come from BR3 and BR4; the detail behind them is a documented gap (GAP-0812, GAP-0814).

**Build steps**

1. `LovFileParser` with the CSV and XLSX header handling and the five columns; tests for a missing header, a missing column, an oversized file and an over-long file.
2. `LovLoadCheckService` with the required English label, the duplicate code in the file and the row numbering; tests for AC3.
3. `UsageReader` and `ReferenceLoadClient` against the DP-07 fakes; tests for the accepted load of AC1 and the 409 of AC2 with the count copied from the answer.
4. The owner-unavailable path: 503, no record, no version (X8).
5. `PermissionReader` and the refusal of AC4 with MSG-P4-002, then the `REF-LOAD` and `REF-DENY` entries with no personal data.
6. The idempotency row and the replay of AC5, including a replayed key with a different file.
7. `GET /admin/lov-loads/{loadId}` against the owner contract and the local record; the 404 and the read right.
8. The forced record failure of X9 and the 503 with MSG-P7-003.
9. The composite route check of SCR-40 through gateway-bff, with the four states of section 15.

**Feature switch.** The story carries no switch of its own. Which lists the console may load is enabled by reference data and not by a flag, so turning a list off is a reference-data change; when a list is not enabled the operation answers 422 naming `lovCode`, and the contract declares that answer.

**Done when.** The tests of section 16 pass; the valid file of AC1 is stored by the fakes in `LOADED` with 12 rows and one `REF-LOAD` entry; the file that removes `R2` is refused with 409 and the count 37 of AC2; a row without `label_en` and a duplicate code are refused with 422 and their row numbers; a loader without the C letter is refused with MSG-P4-002 and one `REF-DENY` entry; a replayed key stores no second version; and the forced record failure answers 503 with MSG-P7-003.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. | The service's sign-in path |
| MSG-P4-002 | The caller holds no C letter in Reference data, or no R on the read | You cannot {action} here. Your role does not include it. | This story, on both operations |
| MSG-GEN-001 | A required query field is empty, a row has no `label_en`, a `value_code` repeats, the list code is unknown, `valid_from` is missing, the file is above a cap, or the key is replayed with another file | Enter {field}. | This story, with the field and the row number in the body |
| MSG-GEN-004 | The load would remove a value code still used by open cases | Someone else changed this record. Reload it to see their change. | This story, on the 409, with `valueCode` and `count` in the body |
| MSG-P7-003 | The record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, after a failed record append |
| MSG-P4-003 | A record outside the caller's scope | This case is not in your scope. | Not produced here: this story reads no case. The legacy message table carries it and the scope filter of the list read is the owner's |

Every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The 409 also carries `valueCode` and `count`, and the 422 carries `field` and `row`, so the screen can point at the failing row without a second call; the exact sentence the screen composes around the count is a screen matter and is Not specified in the source documents (GAP-0813; ASM-1514).

### 15. Screens and states

One screen is served, through the gateway-bff composite route of DP-19. The composite route calls the access operations of this story and the owner's list read in parallel, one hop each, and merges the answers; SCR-39 Rules and parameters belongs to RWB-P4-AD011-APP and is not served here.

| Screen | State | What the screen shows |
|---|---|---|
| SCR-40 Reference data | Empty | No list is enabled for the role: the list picker is empty and the file control is disabled, with no error |
| SCR-40 Reference data | Loaded | The load answered `LOADED`: the list code, the valid-from date, the row count, one line per check with its result, and that the version waits for the list owner's approval |
| SCR-40 Reference data | Refused | The load answered `REFUSED`, or the operation answered 422 or 409: the failing field and row for a check, and the value code with the count of records using it for a usage refusal |
| SCR-40 Reference data | Waiting for approval | The load is `LOADED` and the screen shows the approval as the next step, which is RWB-P4-AD010-APP's |
| SCR-40 Reference data | Versions | The list in force and its versions, read through the owner's contract, with the columns `lov_code`, `value_code`, `label_en`, `label_th`, `sort_order` and `valid_from` of the screen specification |

The screen fields are the `lov_value` columns of the SCR-40 specification; none of them is personal data. The composite route shape and the field-level mapping are Not specified in the source documents (GAP-0811; ASM-1512), and this story fixes only the two operations behind the route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-009-01 | AC1, BR1, BR3 | Component | A 12-row CSV for LOV-ROUTE with codes and English labels, valid from 2027-01-01, against the `rwb-case` fake answering `RL-2026-014` in `LOADED` |
| TC-AD-009-02 | AC2, BR5 | Component | A file that omits `R2` while the owner's list read answers 37 open cases on `R2`; the 409 carries 37 |
| TC-AD-009-03 | AC4, BR7 | Component | RW-CASEOWN with R only posts a valid file; 403 MSG-P4-002 and one `REF-DENY` entry |
| TC-AD-009-04 | X9, BR9 | NFR | The decision-record append forced to fail during a valid load; 503 MSG-P7-003 and no answer |
| TC-AD-009-05 | AC3, BR3, BR4, BR6 | Component | A file with no `label_en` on row 4, a duplicate `R2` on row 7, an unknown list code, and a file above the size and row caps |
| TC-AD-009-06 | AC5, BR8 | Component | The same file posted twice with the same Idempotency-Key, then the same key with another file |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy levels Access, Data, Process and System map to Component, and Resilience maps to NFR. No `-ITG` copy is written here: the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the enabled lists and their versions are reference data through DP-07, and the caps, the column names and the limits are parameters through DP-06 (BR10). A test proves that a new list needs no build.
- No personal data anywhere: the loader is a user reference and a group from `v_ace_iam_group`, and no name, e-mail address or personal field appears in the request, the answer, the record or the outbox payload.
- No read of another service's tables (DP-01): `lov_value`, `reference_version`, `reference_row` and the case are `rwb-case`'s, `decision_log_entry` is `rwb-decision`'s, and no foreign key crosses a schema. The list and its versions arrive in the contract answer.
- One writer for the rows: `rwb-case` stores and versions the list rows; this service's module has no write statement against a reference table, so a load cannot change a version behind the owner's back.
- ACE data only through the owner's contract or its own `v_ace_*` view (DP-05): the only ACE read is the group of the loader through `v_ace_iam_group`, and it is not personal data.
- No answer without its record: the `REF-LOAD` or `REF-DENY` entry commits with the answer, and the answer is withheld with MSG-P7-003 when it cannot be written (BR9, R-UNI-39).
- A refusal names what is wrong and nothing else: a usage refusal returns the value code and the count, never a case number, a party key or a case-level row.
- The same bytes with the same key answer the same load: the operation is idempotent on the key and the digest, so a retry after a timeout cannot create a second version (BR8, R-UNI-40).
- Every file is synthetic in development and in test: no production list extract is copied into a schema, a fake or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-011 | A reference data service holds every versioned table with valid-from and valid-to, author and approver | E1, 3.4 | FEAT-ADM-01 | A2.17 Run the full administration screens | BR1, BR2, BR3, BR5 | TC-AD-009-01, TC-AD-009-02, TC-AD-009-05 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold and limit, versioned, changed without a code release | E1, 3.4 | FEAT-ADM-01 | A2.17 Run the full administration screens | BR6, BR10 | TC-AD-009-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | E8, 3.2 | FEAT-ADM-01 | A2.17 Run the full administration screens | BR7 | TC-AD-009-03 |
| R-UNI-38 | A new version applies from its effective date | Universal rules | FEAT-ADM-01 | A2.17 | BR1, the state transitions of section 9 | TC-AD-009-01 |
| R-UNI-39 | A decision log entry that cannot be written blocks the action | Universal rules | FEAT-ADM-01 | A2.17 | BR9 | TC-AD-009-04 |
| R-UNI-40 | The same event twice with the same key is ignored and the idempotency hit recorded | Universal rules | FEAT-ADM-01 | A2.17 | BR8 | TC-AD-009-06 |

| Legacy reference | Where it is kept |
|---|---|
| As a reference data administrator, I want a list of values loaded as a new version with a valid from date, so that a code list changes without a code release | Section 1 |
| AC1 Valid load: it passes the checks and waits for the list owner's approval | Section 7, AC1 |
| AC2 Code in use removed: refused with the count of records using the code | Sections 5, 7, 8 |
| The `lov_value` fields DF-REF-027 to DF-REF-033 and the valid-from date | Sections 3, 11, 12 |
| The legacy endpoints `/admin/rule-versions` and its approve, and the SCR-39 screen | Moved: P7 `rwb-decision` under ASM-0040 and RWB-P4-AD011-APP; sections 1, 10, 19 |
| The legacy permission table (Rules and parameters R; A for RW-RISK) | Section 10: it is the rule-version approval and belongs to RWB-P4-AD011-APP |
| SCR-40 Reference data with the versions and the load | Sections 15 and 19 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-GEN-004, MSG-P7-003 | Section 14 and the exception paths |
| Legacy test cases TC-AD-009-01 to TC-AD-009-04 | Section 16, extended with TC-AD-009-05 and TC-AD-009-06 |
| The guardrails of RWB-AD-009 | Section 17 |

### 19. Out of scope

- The approval of the load, its verification and its rollback (legacy RWB-AD-010): the states `APPROVED`, `IN_FORCE`, `SUPERSEDED` and `ROLLED_BACK`, and the `POST /admin/reference-loads/{loadId}/approve`, `.../verify` and `.../rollback` paths, which are RWB-P4-AD010-APP's on the owner's contract.
- The `lov_value` table, `reference_version`, `reference_row` and the reference-load operations themselves: P3 `rwb-case` under the R-PREC default ruling and ASM-0071 and ASM-0041. This story calls that contract and writes none of those rows.
- The rule-version read and approve that the legacy story carried as its endpoints, the rule package version lifecycle, SCR-39 Rules and parameters and its approval: P7 `rwb-decision` under ASM-0040, and RWB-P4-AD011-APP in this service epic.
- The delegation of authority table and its load: RWB-P4-E1038-APP.
- The conditional fields beyond the five columns of the list, and the version diff report: not specified in the sources and not carried by this story.
- The integration harness RWB-ITG-W4 and any `-ITG` copy of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of the legacy key).
