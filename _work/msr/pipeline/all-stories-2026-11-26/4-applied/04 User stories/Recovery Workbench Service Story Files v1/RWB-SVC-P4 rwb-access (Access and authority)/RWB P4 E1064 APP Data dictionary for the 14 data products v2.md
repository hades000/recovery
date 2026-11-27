# RWB-P4-E1064-APP Data dictionary for the 14 data products

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1064-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-064 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-AA |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1064-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-RDF-001, REQ-RDF-011) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-064 for rwb-access. The 122 objects, the 1,366 fields, the 14 data products, the 30 ACE views and the eight acceptance criteria of the legacy story stay with the dictionary's owner; what lands in rwb-access is the authority half of the same dictionary: the Reference data letters that authorise a field definition's read, change and approval, the owner role each of the 14 products must resolve to, the personal-field marker of every field ID at the masking version in force, and the gate that approves or returns the dictionary governance load after those checks. The rows are `role`, `permission` and `masking_rule` of this service's own schema `rwb_access` (DP-01, DP-15); the field definitions stay P1's and are read one hop through the published contract (DP-05, DP-11); the lists come from rwb-case's reference-data contract (DP-07); the read sits behind the composite route of gateway-bff (DP-19); every path is on base `/api/recovery/access/v1` (DP-13). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E1064-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW), a reference data administrator (RW-REFADM) and a security administrator (RW-SECADM)**, I want **the authority register of the data dictionary held as versioned data in `rwb_access`  -  the Reference data letters that decide who may read, change and approve a field definition, the one owner role each of the 14 data products resolves to, and the marker per field ID that decides whether a personal field is clear or masked  -  with a gate that approves or returns the dictionary governance load only after those checks pass**, so that **no field definition reaches publication with an owner role that is not a role, with a personal field that no masking rule covers, or with an approval given by the person who wrote it, and a change of owner role, letter or masking exception needs a version and no deployment**.

This is the authority slice of legacy RWB-E1-064 in `rwb-access`. It delivers, and only this:

- `GET /api/recovery/access/v1/admin/dictionary-authority`, the register: the matrix version and the masking version in force, one entry per role with its Reference data letters, and, for the field list asked, the owner role and the marker of each field ID (section 12.1).
- `POST /api/recovery/access/v1/admin/dictionary-authority-loads/{loadId}/approve`, the gate: the Reference data `A` check, the four-eyes rule, the owner-role check over the 14 products and the personal-field coverage check over the field IDs of the load, then one call to the load owner (section 12.2).
- `POST /api/recovery/access/v1/admin/dictionary-authority-loads/{loadId}/return`, the other outcome of the same gate: the load goes back to its author with a coded reason.
- The rows that make both true: the `permission` rows in the capability area `REFERENCE_DATA` for RW-DATASTEW (`RU`), RW-REFADM (`CRUD`), RW-COE (`CRUD`) and the reader roles (`R`), the `role` rows each owner role resolves to, and the `masking_rule` rows keyed on the dictionary's field IDs at the masking version in force.

It builds no dictionary table, no loader and no field definition: `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` are P1's in `rwb_source_data`, their read model `v_data_dictionary` with them, and the 122 and 1,366 rows are P1's baseline (DP-01, DP-15). It creates none of the 30 `recovery.v_ace_*` views and reads none: the ACE source-column form of a view field is a fact of P1's contract (DP-05). The five admin operations and the contract baseline are RWB-P1-E1064-CON and RWB-P1-E1064-APP. The matrix and masking loads themselves, and the masking pack, are the load path's and the pack owner's (section 19). This story writes no row of any table: it decides the gate and reads its own three tables, which is what keeps the dictionary's authority answer inside one service and the definitions inside their owner's.

### 2. Business rationale

The legacy story measures the dictionary one way: every field returns a source, an owner, a refresh cycle and a late behavior (REQ-RDF-001), and every product has one catalog entry naming its owner and system of record (REQ-RDF-011). Three of those answers are not P1's at all in the target: an owner role is a `role` row, the right to read or change a definition is a `permission` row, and whether a personal field is clear to a role is a `masking_rule` row. In the monolith the data engine reached them in process through `FieldMasker` and `RecoveryAccessGuard`, so the dictionary could publish an owner role the role table had never heard of, and a personal field that no masking rule covered.

Splitting those three answers into `rwb-access` makes them checkable before publication instead of after. The register answers, for one field ID, the owner role, the letters of every role in the Reference data capability area and the marker at the masking version in force. The gate answers whether a governance load may become the definition in force at all: the approver holds `A`, is not the author, every owner role resolves to a role row, and every personal field ID of the load has a masking row. A change of owner role, letter or exception is then a version with a valid-from date, no release, and the earlier rows stay readable for their own dates (FSD P4 A2.3.1, A2.4.1; BR-P4-003, BR-P4-004: no value a business person may change is written in code).

**What D-RCV-60 changes.** Not the dictionary's content and not its nine rules: they stay with RWB-P1-E1064-APP. The legacy authority column and its `Reference data` rights become rows of this service; the in-process mask and permission read becomes one register read on `/api/recovery/access/v1` (DP-11, DP-13); the load's approval becomes a gate that calls the load owner instead of a monolith endpoint (DP-07, DP-11); the definitions it checks against arrive one hop from P1's contract, not from a shared schema (DP-01, DP-05); the screen reads the register through gateway-bff (DP-19).

**Why rwb-access.** The four questions the gate asks are this service's data and nobody else's: a role, a letter, a masking exception and a four-eyes rule. Held in P1 they would be a second copy of the matrix; held here they are the rows that already answer `POST /authorise` and the role catalogue, so the dictionary cannot drift from the access policy that governs every other read (Architecture v5 slide 41). The register returns a marker and two version labels and never a value, a rendering or a clear personal field.

No source names the register's request and answer field names, its marker vocabulary, its read path or the number of personal fields among the 1,366 (GAP-0890; ASM-1611) and (GAP-0892; ASM-1613). No role in TSD P4 T6.1 holds the Reference data `A` letter that API-P4-006 requires of an approver (GAP-0891; ASM-1612), and no source states the target apply path of an approved load (GAP-0893; ASM-1614).

### 3. Preconditions

- RWB-P4-E1037-APP delivered the `rwb_access` baseline: `role` (DF-REF-034 to DF-REF-039), `permission` (DF-REF-040 to DF-REF-044), `masking_rule` (DF-REF-198 to DF-REF-204) and `role_conflict` (DF-REF-205 to DF-REF-211) exist in the service's schema on the per-service Flyway sequence of DP-15.
- RWB-P4-E1037-CON published the authorise contract the gate reads the letters through (DP-08 is not a pattern of this story, so the call is the service's own and adds no dependency).
- RWB-P1-E1064-CON is baselined: the five dictionary operations on `/api/recovery/source-data/v1`, the five schemas and one error envelope are published with fakes, so the register and the gate build from Day 1 against the contract and its fake (DP-11).
- P1's dictionary holds the 122 objects and 1,366 fields with `is_personal`, `owner_role`, `refresh_cycle` and `late_behavior` on every field, and each of the 14 `data_product` rows names one owner role (legacy RWB-E1-064 §3 and §11; DP-01).
- Matrix version `PM-2026.11` is in force in `permission` and masking version `MASK-SIT-01` in `masking_rule`; both labels are the ones the FSD and TSD examples carry, and a production masking label is the pack owner's (TSD P4 T3.2).
- LOV-ROLE and LOV-CAPABILITY are read with the version in force through the reference-data contract of `rwb-case` (DP-07); no role code and no capability area is written in code, and no source fixes that read's query names.
- The Reference data letters of the dictionary roles are those of TSD P4 T6.1: RW-DATASTEW `RU`, RW-REFADM and RW-COE `CRUD`, RW-COMPLY `RU`, and `R` for RW-SECADM, RW-PLATADM, RW-CASEOWN, RW-AUDIT, RW-TRIBE and SY-DATALOAD. No role holds `A` in that matrix, which is GAP-0891: the approver is a role the SIT matrix gives the `A` letter, fixed as an assumption and not as a business value (ASM-1612).
- The four-eyes rule is the module's: the author of a load cannot approve it (FSD P4 AC-EXC-P4-004-03, MSG-P7-002).
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. A data steward opens SCR-40 Reference data through the gateway-bff composite route (DP-19) and reads the register with `GET /api/recovery/access/v1/admin/dictionary-authority` for a field list.
2. `DictionaryAuthorityController` resolves the caller's roles from the session and their `REFERENCE_DATA` letters from `permission` at the matrix version in force; a token with no role is 401 MSG-P4-001 and a caller without the `R` letter is 403 MSG-P4-002 before any row is read.
3. `AuthorityRegisterService` answers the matrix version, the masking version, one entry per role with its Reference data letters, and for each field ID asked the owner role and the marker. The owner role and the personal flag come from P1's field read, one hop, 2 s, cached for the call (DP-11, DP-05).
4. `MaskingMarkerService` resolves the marker per field ID at the masking version in force: `clear` only where a `masking_rule` row for a role the caller holds, that field ID and that version says `unmasked` true, and `masked` otherwise, including where no row exists.
5. A reference data administrator submits the dictionary governance load to the load owner with table code `sys_fields`, valid from 2026-11-30, exactly 1,366 field rows; the owner validates the file, the source system and the view column and holds the version in LOADED (DP-07).
6. A second person holding the Reference data `A` letter calls `POST /admin/dictionary-authority-loads/{loadId}/approve` with an `Idempotency-Key`, one hop to this service.
7. `DictionaryLoadGate` checks the `A` letter, the four-eyes rule against the author, then reads P1's dictionary and asks four questions of the load: every `owner_role` resolves to a `role` row, every `product_code` of the 14 has exactly one owner role, every personal field ID has at least one `masking_rule` row at the version in force, and no field ID is unknown to the dictionary.
8. Where every check passes, the gate calls the owner's `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve` once, one hop, with the same `Idempotency-Key`; the owner moves the version LOADED to APPROVED and to IN_FORCE from 2026-11-30 and answers it (DP-11, DP-07).
9. The gate answers the approval with the load ID, the table code, the row count, the approver reference, the state and both version labels, and writes no row of its own.
10. Where a check fails, the gate refuses whole with MSG-P1-002 naming the first failing check, writes nothing, and the matrix, masking and dictionary versions in force stay in force.
11. An approver who returns the load calls `POST /admin/dictionary-authority-loads/{loadId}/return` with a `reasonCode` from the owner's coded reason list; the load goes back to LOADED with the version returned to its author, and the author reads the reason on SCR-40. An empty or unknown `reasonCode` is 422 MSG-GEN-001 and nothing is returned.
12. A new ACE column reaches the register the same way it reaches the dictionary: the view column exists first, P1's field row follows, and the load's field ID then resolves here; no applied migration is edited and this story adds no endpoint of its own for a column.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The token holds no Workbench role | 401 before any role, letter or field ID is read | MSG-P4-001 | AC9 |
| X2 | The caller's roles hold no Reference data `R` on the register, or no `A` on the gate | 403 and nothing is read or approved | MSG-P4-002 | AC9 |
| X3 | The author of the load calls approve on it | 409; the load stays LOADED and the versions in force stay in force | MSG-P7-002 | AC4 |
| X4 | A row of the load names an `owner_role` that is not a role row, or a field ID the dictionary does not hold | Load refused whole; the version in force stays | MSG-P1-002 | AC2, AC5, AC7 |
| X5 | A row of the load names a personal field ID with no `masking_rule` row at the masking version in force | Load refused whole; the field stays masked for every role | MSG-P1-002 | AC3, AC5 |
| X6 | One of the 14 products carries two owner roles, or its owner role is missing | Load refused whole and the first failing product is named | MSG-P1-002 | AC2 |
| X7 | Two approvers decide the same load from the same version | The second is refused with 409 | MSG-GEN-004 | AC8 |
| X8 | A decision carries no `If-Match` version, or a `reasonCode` is empty or not in the coded list | 428 or 422; nothing is decided | MSG-GEN-004, MSG-GEN-001 | AC6, AC8 |
| X9 | P1's dictionary read or the list read does not answer inside 2 s | The gate answers 503 and approves nothing; no answer is guessed from a stale cache | MSG-GEN-006 | AC5, AC6 |

X1 to X3 and X7 to X9 are the module's paths carried onto the split; X4 to X6 are the three dictionary checks this service adds, which in the monolith were nobody's. A refused load is never partially applied: the owner's version moves as one unit and this gate writes no row of its own, so a failure at any check leaves every version in force untouched.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P1-E1064-CON and its fake, the `rwb_access` baseline and the rwb-case list contract from Day 1; it needs neither the dictionary tables nor the views of its own |
| Negotiable | Owner roles, letters, masking exceptions, version labels and reason codes are data rows and reference data; the story fixes only the register shape, the four checks and the refusal rule |
| Valuable | A field definition cannot be published with an owner role, a personal field or an approval that the access policy does not support, and a change needs a version and no deployment |
| Estimable | One register read, one gate with four checks, one two-call decision, one return path, no DDL and no migration |
| Small | Fits one sprint as a secondary slice of the legacy key, with its tests |
| Testable | Each criterion is one API test on synthetic rows and one contract-fake run; no ACE value and no production data is needed |

### 7. Acceptance criteria

```gherkin
Feature: The authority register and the governance gate of the data dictionary in rwb-access

  Background:
    Given the dictionary holds 122 objects and 1,366 fields from V0001 and its 14 data products are DP01 to DP14
    Given data product "DP01" Account and arrears has owner role RW-DATASTEW and system of record "ACE (ingested from ALS)"
    Given matrix version "PM-2026.11" is in force in "permission" and masking version "MASK-SIT-01" is in force in "masking_rule"
    Given contract "DC-ACE" for source system "ACE" and read interfaces "V0002" and "V0003" is "DRAFT" with 304 mapped fields
    Given the field IDs of the register are "DF-ACE-018", "DF-ACE-074" and "DF-ACE-204"

  Scenario: AC1 The register answers the owner role, the letters and the marker of a field (new, D-RCV-60)
    Given the caller holds "RW-DATASTEW", whose Reference data letters are "RU" in "PM-2026.11"
    When the caller reads GET /api/recovery/access/v1/admin/dictionary-authority for field IDs "DF-ACE-018", "DF-ACE-074" and "DF-ACE-204"
    Then the answer is 200 and names matrixVersion "PM-2026.11" and maskingVersion "MASK-SIT-01"
    And the entry for "DF-ACE-018" names ownerRole "RW-DATASTEW" and refreshCycle "DAILY"
    And every role entry carries its Reference data letters, for example "CRUD" for RW-REFADM, "CRUD" for RW-COE and "R" for RW-CASEOWN
    And the marker of "DF-ACE-074" is "clear" for "RW-COMPLY" and "masked" for "RW-CASEOWN"
    And no answer carries a field value, a masked rendering or a last four digits

  Scenario: AC2 Each of the 14 data products resolves to exactly one owner role (new, D-RCV-60)
    Given the 14 data products DP01 to DP14, each with one owner role in the dictionary
    When the caller reads the register for the product list
    Then all 14 products are returned and each names one owner role that is a role row in "rwb_access"
    And "DP01" names "RW-DATASTEW", whose Reference data letters include "R"
    And a product that names two owner roles is reported as a failure naming the product code
    And a product whose owner role is not a role row is reported as a failure naming the product code and the role code

  Scenario: AC3 Every personal field ID of the dictionary has a masking marker (new, D-RCV-60)
    Given the dictionary marks a field as personal with "is_personal" true
    When the register resolves the marker of that field ID at "MASK-SIT-01"
    Then the marker is "masked" for every role without an "unmasked" row for that field ID and version
    And the marker is "clear" only for a role whose row for that field ID and version says "unmasked" true
    And a personal field ID with no row at all is reported as a coverage failure and stays "masked" for every role
    And the number of personal fields among the 1,366 is Not specified in the source documents (GAP-0892; ASM-1613) and is reported as a count, never as a fixed value

  Scenario: AC4 The governance load is approved by a second person with the A letter (new, D-RCV-60)
    Given load "LD-2026-064" for table code "sys_fields" with 1,366 rows and valid from 2026-11-30, authored by "RW-REFADM"
    And the approver holds the Reference data "A" letter in the matrix version in force
    When that approver calls POST /api/recovery/access/v1/admin/dictionary-authority-loads/LD-2026-064/approve with Idempotency-Key "k-064"
    Then the answer is 200 with state "APPROVED", rowCount 1366, table "sys_fields" and validFrom 2026-11-30
    And the owner of the load is called once and moves the version to IN_FORCE from 2026-11-30
    And a second call with the same Idempotency-Key answers the first answer and approves nothing twice
    When the author "RW-REFADM" calls approve on the same load
    Then the call is refused with status 409 and MSG-P7-002 and the load stays LOADED

  Scenario: AC5 A load with one bad row is refused whole (new, D-RCV-60)
    Given load "LD-2026-065" whose rows give "DP07" the owner role "RW-NOSUCH" and name field ID "DF-ACE-999"
    When the approver with the A letter approves it
    Then the call is refused with MSG-P1-002 naming the first failing check, the product code and the role code
    And no row of "LD-2026-065" is applied and the versions in force stay in force
    When a second load is corrected and approved, only the corrected load is in force
    And a personal field ID of the load with no masking row at "MASK-SIT-01" refuses the load whole with MSG-P1-002

  Scenario: AC6 A load is returned to its author with a coded reason (new, D-RCV-60)
    Given load "LD-2026-066" awaits approval and its author holds "RW-REFADM"
    When the approver calls POST /api/recovery/access/v1/admin/dictionary-authority-loads/LD-2026-066/return with reasonCode "REF-RSN-03" and Idempotency-Key "k-066"
    Then the answer is 200 with state "LOADED" and reasonCode "REF-RSN-03"
    And the load is back with its author and the version in force is unchanged
    When the same call is made with an empty reasonCode or a code that is not in the list
    Then the call is refused with status 422 and MSG-GEN-001 and nothing is returned

  Scenario: AC7 A new ACE column resolves in the register only after its dictionary row exists (new, D-RCV-60)
    Given the dictionary holds no row for "insurance_expiry" of "v_ace_collateral_detail" and no field ID "DF-ACE-204"
    Given RWB-P1-E1064-APP adds "public.collateral_detail.insurance_expiry" and V0003 exposes it
    When a load names field ID "DF-ACE-204" with owner role RW-DATASTEW before the dictionary row exists
    Then the load is refused whole with MSG-P1-002 naming the unknown field ID
    When the same load is sent after the dictionary row and the view column exist
    Then the register answers "DF-ACE-204" with ownerRole "RW-DATASTEW", refreshCycle "WEEKLY" and lateBehavior "Keep the previous value and mark DP06 stale"
    And no Flyway migration file was edited by this story

  Scenario: AC8 An approval takes effect from its valid-from date and never retroactively (new, D-RCV-60)
    Given load "LD-2026-067" is approved on 2026-11-28 with valid from 2026-12-01
    When the register is read on 2026-11-30 and again on 2026-12-01
    Then the read on 2026-11-30 answers the version in force on that date
    And the read on 2026-12-01 answers the new version and its label
    And the older rows stay readable with their own valid_to date
    When two approvers decide the same load from version 1 at once
    Then the first decision is saved and the second is refused with status 409 and MSG-GEN-004
    When a decision carries no If-Match version
    Then it is refused with status 428 and MSG-GEN-004

  Scenario: AC9 A caller without the Reference data right is refused, and a refused approval writes nothing (new, D-RCV-60)
    Given the caller holds "RW-TRIBE", whose Reference data letters are "R"
    When the caller calls the approve operation for load "LD-2026-064"
    Then the call is refused with status 403 and MSG-P4-002 before any load, letter or field row is read
    And the load stays LOADED and the versions in force stay in force
    When a token holds no Workbench role
    Then the register and both decisions answer status 401 and MSG-P4-001
```

The nine criteria are new and prove only this deliverable: the register, its three answers, the four checks of the gate, the return path, the date effect and the refusal shape. No legacy criterion text is copied here. The eight criteria of RWB-E1-064 (the 122 and 1,366 counts, the 30 views, DF-ACE-018's source column, the new-ACE-column load, the field version history, the DC-ACE confirmation, the optimistic lock and the DRAFT version on change) are owned by RWB-P1-E1064-APP and appear in section 16 as regression evidence with the slice each contributes here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The dictionary's authority answers are data with a version: a role, a letter, an owner role and a masking exception are rows; no role code, capability area, letter, field ID or version label is written in Java, and the lists arrive through the reference-data contract | FSD P4 A2.3.3.1 and A2.4.3.1 (BR-P4-003, BR-P4-004); TSD P4 T3.1 and T3.2; DP-07 |
| BR2 | The Reference data letters of a role are its `permission` row in the capability area `REFERENCE_DATA` at the matrix version in force; a role without a row has no right, and a missing row never opens an area | TSD P4 T3.1 (`permission`), T6.1 and T3.2 (LOV-CAPABILITY); FSD P4 A2.4.4.3 (AC-EXC-P4-004-06); CTL-09 |
| BR3 | Each of the 14 data products names exactly one owner role, and that owner role is a `role` row; a product with two owner roles or with an owner role that is not a role row cannot be published | Legacy RWB-E1-064 BR3 and AC3; REQ-RDF-001; FSD P4 A2.3.3.1 |
| BR4 | A personal field is `clear` to a role only where a `masking_rule` row for that role, that field ID and the masking version in force says `unmasked` true; every other case, including no row at all, is `masked` | FSD P4 A2.5.3.1; TSD P4 T3.1 (`masking_rule`); FSD P4 AC-EXC-P4-004-05 |
| BR5 | A load is approved only by a caller holding the Reference data `A` letter, and never by its author: the gate applies the four-eyes rule before it calls the owner | API-P4-006; FSD P4 AC-EXC-P4-004-03 (MSG-P7-002) |
| BR6 | A load with one failing row is refused whole, with the first failing check named, and every version in force stays in force; a refused load is never partially applied | Legacy RWB-E1-064 BR6; FSD P4 AC-EXC-P4-004-02 (MSG-P1-002); CTL-08 |
| BR7 | An approved version takes effect from its valid-from date and never retroactively; the older rows stay readable with their valid-to date, and the previous version stays in force until then | Legacy RWB-E1-064 BR7; FSD P4 AC-P4-004-01; TSD P4 T3.2 (LOV-VERSION-STATUS) |
| BR8 | The field definitions, their 122 and 1,366 rows and the 14 product rows are P1's and are read through its contract only; `rwb_access` holds no copy of a definition and no foreign key across a schema | Ownership Map (`sys_objects`, `sys_fields`, `data_product` P1); DP-01; DP-05 |
| BR9 | This story writes no row of any table: it reads `role`, `permission` and `masking_rule` in its own schema and decides a gate that the load owner applies | Legacy RWB-E1-064 BR8 and BR9; ADR-021; DP-15 |
| BR10 | The register answers a marker and two version labels and never a field value, a rendering or a last four digits; the value stays with rwb-source-data | NFR-039; NFR-040; FSD P4 A2.5.3.1 |

### 9. State transitions

This service holds no case, task or approval state of its own beyond the decision it records on a load. The states it answers are the marker of a field, the four outcomes of a gate decision and the lifecycle of a matrix and masking version, which the load path and the pack owner write.

| From | Event | Condition | To |
|---|---|---|---|
| Version in force | A register read for a field ID | A covering `unmasked` row exists for a role the caller holds | Field answered `clear` for that role |
| Version in force | A register read for a field ID | No covering row, or `unmasked` false | Field answered `masked` |
| Load LOADED | Approve called | `A` letter held, caller is not the author, all four checks pass | Owner moves the version to APPROVED, then to IN_FORCE from its valid-from date |
| Load LOADED | Approve called | The caller is the author | Refused 409 MSG-P7-002; the load stays LOADED |
| Load LOADED | Approve called | A check fails | Refused whole with MSG-P1-002; no row applied and every version in force stays |
| Load LOADED | Return called with a coded reason | `A` letter held and the code is in the list | LOADED, back with its author, reason recorded |
| Load LOADED | Return called with an empty or unknown code | Any | Refused 422 MSG-GEN-001; nothing returned |
| Version in force | A new version is approved and its valid-from date is reached | No deployment | The new version answers every read from that date; the older rows stay readable for their own dates |

The version lifecycle labels are TSD P4 T3.2 (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED). This story reads the two versions in force and writes no state row of its own; the approval and the rollback are the load path's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Reads the register and is the owner role of the data products (`RU` in Reference data, TSD P4 T6.1); authors a governance load through the load path, and may not approve its own load |
| RW-REFADM, reference data administrator | Authors and prepares the governance load (`CRUD` in Reference data); approves a load only where the matrix gives it the `A` letter (ASM-1612) |
| RW-COE, center of excellence analyst | Reads the register and changes a definition through P1's operations (`CRUD` in Reference data) |
| RW-SECADM, security administrator | Holds `CRUDA` in Platform administration and `R` in Reference data: reads the register and the gate answers, and owns the matrix and masking versions through the load path |
| RW-COMPLY, Compliance and PDPA officer | Reads the register and the personal-field markers (`RU` in Reference data); owns the masking pack content through the load path |
| RW-AUDIT, RW-TRIBE, RW-CASEOWN, RW-PLATADM and other roles with `R` in Reference data | Read the register only; may not approve or return a load |
| SY-DATALOAD, data load | Applies an approved load on the owner's path; reads the register only |
| ACE team lead | Confirms the ACE read path and owns the ACE columns P1's contract names; this story names none of them and reads no view |
| rwb-source-data (P1) | Owns the 122 objects, the 1,366 fields, the 14 product rows and the 30 views; answers the field read and applies the load |
| rwb-case (P3) | Owns the reference lists, the load submission and the approve call this gate makes (DP-07) |
| No approval level from the delegation of authority applies | The story takes no business decision; the DoA answer is RWB-P4-E2013-APP's and `delegation_limit` is not read |

Every "who" is a role code or a service, never a person. The refusal shape is 403 with an RFC 9457 problem response, `messageId` set to MSG-P4-002, and the area and right named in the detail.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | `role` | id | Read |
| DF-REF-035 | `role` | role_code | Read: the owner role of a product resolves here |
| DF-REF-036 | `role` | role_name | Read: named in the register entry |
| DF-REF-037 | `role` | role_class | Read |
| DF-REF-038 | `role` | default_scope | Read |
| DF-REF-039 | `role` | entra_group | Not read by this story |
| DF-REF-040 | `permission` | id | Read |
| DF-REF-041 | `permission` | role_id | Read |
| DF-REF-042 | `permission` | capability_area | Read: the `REFERENCE_DATA` row is the one this story answers from |
| DF-REF-043 | `permission` | letters | Read: the `R`, `C`, `U`, `D` and `A` letters of a role |
| DF-REF-044 | `permission` | matrix_version | Read: the matrix version in force |
| DF-REF-198 | `masking_rule` | id | Read |
| DF-REF-199 | `masking_rule` | role_code | Read |
| DF-REF-200 | `masking_rule` | field_id | Read: the dictionary's field IDs are the keys |
| DF-REF-201 | `masking_rule` | unmasked | Read: the only path to a `clear` marker |
| DF-REF-202 | `masking_rule` | masking_version | Read: the masking version in force |
| DF-REF-203 | `masking_rule` | valid_from | Read |
| DF-REF-204 | `masking_rule` | valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | role_code, conflicts_with, conflict_version | Not read: the sign-in conflict check is RWB-P4-E1022-APP's |
| DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 | `delegation_limit` | approval limits | Not read: the DoA lookup is RWB-P4-E2013-APP's |
| DF-REF-088 to DF-REF-111 | P1's `sys_objects`, `sys_fields`, `sys_field_version` | `owner_role` (DF-REF-107), `refresh_cycle` (DF-REF-108), `late_behavior` (DF-REF-109), `is_personal` (DF-REF-105) | Read through the P1 contract only (DP-11, DP-05); no row is copied into `rwb_access` |
| DF-REF-070 to DF-REF-079 | P1's `data_product` | the 14 products and their owner roles | Read through the P1 contract only; no copy |
| DF-ACE-018, DF-ACE-074, DF-ACE-204 | P1's `sys_fields` and the 30 `recovery.v_ace_*` views | `days_past_due`, `id_no_last4`, `insurance_expiry` | Named as field IDs only: keys of `masking_rule` and of the register's answers; no view is read |

This story writes no row of any table and creates no table, column or index. The field ID is a value in `masking_rule`, with no foreign key across a schema; `role_id` is the one existing key inside `rwb_access`. Field IDs and values are those of the Logical Data Model and Data Dictionary v9 and of legacy RWB-E1-064; no count of the personal fields is stated by any source (GAP-0892; ASM-1613).

### 12. Contract

Base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access` (DP-13, DP-14, DP-02, DP-15).

#### 12.1 REST operations provided

Three operations, all on the service's base and all owned by P4 `rwb-access`. This slice adds no other path.

| Method | Path | Purpose | Schemas | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/admin/dictionary-authority` | The register: the matrix and masking versions in force, one entry per role with its Reference data letters, and per requested field ID the owner role, the refresh cycle, the late behavior and the marker | `DictionaryAuthority` out | Reference data `R`, scope applied | Not applicable, read only |
| POST | `/admin/dictionary-authority-loads/{loadId}/approve` | The gate: the `A` check, the four-eyes rule, the four dictionary checks, then one call to the load owner | `DictionaryLoadDecision` out | Reference data `A` | `Idempotency-Key` required; a repeat answers the stored answer; `If-Match` on the decision version |
| POST | `/admin/dictionary-authority-loads/{loadId}/return` | The other outcome of the gate: the load goes back to its author with a coded reason | `DictionaryLoadDecision` out | Reference data `A` | `Idempotency-Key` required |

Request and answer shapes, as this story fixes them:

- `/admin/dictionary-authority`: query `fieldIds`, `productCodes`, `role`. Answer: `matrixVersion`, `maskingVersion`, `roles` (each with `roleCode`, `roleClass`, `defaultScope`, and `letters` as a list of `capabilityArea` and `letters`), and `fields` (each with `fieldId`, `entity`, `fieldName`, `ownerRole`, `refreshCycle`, `lateBehavior`, `isPersonal` and a `markers` list of `roleCode` and `marker` where the marker is `masked` or `clear`), plus `products` (each with `productCode`, `ownerRole`).
- `/admin/dictionary-authority-loads/{loadId}/approve`: no request body beyond the header `Idempotency-Key` and `If-Match`. Answer: `loadId`, `table`, `rowCount`, `validFrom`, `state`, `approverReference`, `decidedAt`, `firstFailingCheck`, `matrixVersion`, `maskingVersion`.
- `/admin/dictionary-authority-loads/{loadId}/return`: body `reasonCode`; answer as above with `state` LOADED and `reasonCode`.

The request and answer field names above, the marker vocabulary and the shape of the register's role part are Not specified in the source documents (GAP-0890; ASM-1611). Errors: 401 no Workbench role (MSG-P4-001); 403 no Reference data `R` or `A` (MSG-P4-002); 404 unknown load or unknown table code; 409 the author approves their own load (MSG-P7-002) or a stale decision version (MSG-GEN-004); 422 an empty or unknown `reasonCode` (MSG-GEN-001); 428 no `If-Match` (MSG-GEN-004); 503 the dictionary read, the list read or the owner is unavailable (MSG-GEN-006); and the load refusal of MSG-P1-002, which names the first failing check.

The register read is the inbound surface this slice adds to P4; the load submission itself is not a path of this service, because the file goes to the load owner and only its decision passes through the gate (DP-07).

#### 12.2 REST operations consumed

| Method | Path | Owner | Contracted use |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/admin/data-dictionary/fields` | P1 rwb-source-data (RWB-P1-E1064-CON) | The 1,366 field definitions with `fieldId`, `entity`, `fieldName`, `ownerRole`, `refreshCycle`, `lateBehavior` and `isPersonal`, filtered by entity, field and product; the owner role, the personal flag and the unknown-field check of the gate come from it. One hop, 2 s timeout, breaker per downstream, cached for the call (DP-11, DP-05) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (DP-07) | LOV-CAPABILITY (`REFERENCE_DATA` among the 14 areas) and LOV-ROLE, with the version in force; the coded reason list of a return; no list value is a constant in code. One hop, 2 s timeout (DP-07, DP-11) |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | P3 rwb-case (DP-07) | The one call the gate makes when every check passes: the owner moves the version LOADED to APPROVED and to IN_FORCE from its valid-from date and answers the version; the same `Idempotency-Key` is presented so a retry resumes the call. One hop, 2 s timeout, breaker (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access (own) | The `R` and `A` letters of the caller in `REFERENCE_DATA`, with the MSG-P4-002 refusal shape; a service-internal call, one hop |

No other service is called. The dictionary's own operations (`PATCH /admin/data-dictionary/fields/{fieldCode}`, the three contract operations) are not called: this story changes no definition and publishes no contract, and the confirmation of DC-ACE stays with RWB-P1-E1064-APP.

#### 12.3 Events published

None. DP-09 is not a pattern of this story, so this slice holds no outbox row, adds no topic and publishes no event. The topic of the service is `rwb.access.events.v1` with event names `rwb.access.<Event>.v1` (DP-14), and the pack gives the service zero events: a matrix version, an approval and a return are synchronous decisions of the load path, and the policy-change event belongs to the load stories, not here.

#### 12.4 Events consumed

None. The matrix version and the masking version in force are read from `rwb_access` on each call and the dictionary is read on demand; no consumer group is declared and no event starts the gate.

#### 12.5 Workflows and activities

None. The register read, the four checks and the one owner call are synchronous steps in the caller's thread. The six-monthly access review list (JOB-18) is a Schedule of this service and belongs to RWB-P4-AD008-APP; this story starts no workflow and registers no activity on the `rwb-access` queue.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: a governance load is submitted by a person and decided by a second person.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| `role` | `rwb_access` | P4 | Read only: the owner role of a product resolves to a row, and the register lists the role |
| `permission` | `rwb_access` | P4 | Read only: the `REFERENCE_DATA` letters of a role and the matrix version in force |
| `masking_rule` | `rwb_access` | P4 | Read only: the marker of a field ID and the masking version in force |
| `role_conflict` | `rwb_access` | P4 | Not read: the sign-in conflict check is RWB-P4-E1022-APP's |
| `delegation_limit` | `rwb_access` | P4 | Not read: the DoA lookup is RWB-P4-E2013-APP's |

No table is created, altered or indexed by this story, and no row is written. `sys_objects`, `sys_fields`, `sys_field_version`, `data_product`, `data_contract` and the read model `v_data_dictionary` are P1's in `rwb_source_data` and are named here, not created (DP-01, DP-15); the 30 `recovery.v_ace_*` views are P1's in schema `recovery`, owned by `ace_view_owner`, and are neither read nor described here (DP-05). No foreign key crosses a schema. `lov_value` and the reference tables are P3's under the ownership ruling and arrive through DP-07.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Dictionary fake | RWB-P1-E1064-CON | A page with the 122 objects and the 1,366 fields, a single field, `DF-ACE-018` with owner role RW-DATASTEW and refresh DAILY, `DF-ACE-204` with refresh WEEKLY, a field marked personal, an unknown field ID, a 404 and a timeout |
| Reference-list fake | RWB-P3-E1043-CON (DP-07) | LOV-CAPABILITY with the 14 areas and `REFERENCE_DATA` among them, LOV-ROLE with and without a role a load names, the coded reason list with `REF-RSN-03`, an empty list and a timeout |
| Load-owner fake | RWB-P3-E1043-CON (DP-07) | An approve that moves the version to APPROVED and IN_FORCE, a load no longer LOADED (409), a 503 and a timeout |
| Matrix fixture | `permission` | `PM-2026.11` with `RU` for RW-DATASTEW, `CRUD` for RW-REFADM and RW-COE, `R` for RW-CASEOWN, RW-TRIBE, RW-AUDIT and SY-DATALOAD, an `A` row for the approver role of the fixture (ASM-1612), and `PM-2026.12` for AC8 |
| Masking fixture | `masking_rule` | `MASK-SIT-01` with one `unmasked` true row for RW-COMPLY and `DF-ACE-074`, no row for `DF-ACE-018`, and one personal field ID with no row for the coverage case of AC3 |
| Load fixture | The gate | `LD-2026-064` (1,366 rows, valid from 2026-11-30), `LD-2026-065` (one bad owner role and one unknown field ID), `LD-2026-066` (returned), `LD-2026-067` (valid from 2026-12-01) |

A fixture that answers a shape the document does not declare fails the build, and a shape the document declares with no fixture to answer it fails the build. The fakes carry no production data and no personal value: the register answers markers, never values.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 3 operations on `/api/recovery/access/v1` | 3 external (P1 field read, P3 list read, P3 approve) and 1 own (authorise) | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11, DP-13) |
| Kafka | None | None | The topic `rwb.access.events.v1` is provisioned and unused by this slice (DP-14) |
| Temporal | None | None | Queue `rwb-access`; JOB-18 is RWB-P4-AD008-APP's |
| File | None | The load file is the owner's, never read here | The gate sees a load ID and an answer, not a file |
| Reference load | None | 1 approve call to the load owner | The gate decides; the owner applies (DP-07) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.dictionary`, module `dictionary`, in the service root `th.co.scb.ace.workbench.recovery.access`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process read of the permission matrix and the masking rules by the data engine (DP-11: one REST contract with a mock), the single recovery schema that held both the dictionary and the policy (DP-01: this service's `rwb_access` only), the `recovery.v_ace_*` view read behind the field's source column (DP-05: P1's contract, and this service reads no view at all), the monolith reference-load endpoint (DP-07: the rwb-case contract and its owner call), the `/api/recovery/v1` base (DP-13), the V0001 baseline that held `sys_fields`, `permission` and `masking_rule` in one migration (DP-15: the rows sit on the service's own sequence) and the screen that read the dictionary directly (DP-19: the gateway-bff composite route).

This is a secondary slice and it adds no H dependency of its own. The four metadata dependency rows stay exactly as this Work Package fixes them: the platform libraries, the per-service Flyway baseline and the gateway route are already build dependencies of the P4 service's own stories, and this story builds against the published contract and its fake. No H, C, I or X dependency is created here beyond the one contract dependency the Work Package names.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DictionaryAuthorityController` | Controller | The register read: query validation, the `R` check, and the error mapping to RFC 9457 problem responses |
| `AuthorityRegisterService` | Service | The matrix and masking versions in force, one entry per role with its letters, and per field ID the owner role, the refresh cycle, the late behavior and the marker |
| `MaskingMarkerService` | Service | The `clear` or `masked` marker per field ID at the masking version in force; no row means `masked` |
| `DictionaryLoadGate` | Service | The static checks of the gate: the `A` letter, the four-eyes rule, the owner role of each product, the unknown field ID, the personal-field coverage |
| `DictionaryLoadDecisionController` | Controller | The approve and the return operations, the `Idempotency-Key` and `If-Match` handling, and the decision answer |
| `LoadOwnerClient` | Client | The one-hop call to the load owner's approve, with the 2 s timeout and the breaker; a resumed call reuses the same key |
| `DictionaryFieldClient` | Client | The P1 field read of section 12.2, cached for the call, with the 404 and the timeout paths |
| `ReferenceLists` | Service | LOV-CAPABILITY, LOV-ROLE and the coded reason list through DP-07; no Java enum of areas, roles or reasons |
| `AuthorityRepository` | Repository | Read-only queries over `role`, `permission` and `masking_rule` in schema `rwb_access`; no write method |

**Database and migrations**

- No table, column, index or Flyway version of its own: `role`, `permission`, `masking_rule` and `role_conflict` are created and loaded by RWB-P4-E1037-APP on the per-service sequence of DP-15, and the repository exposes no save, update or delete, so a read or a decision can never change a policy row.
- If the SIT plan needs an index the creating story does not hold, it is added to that story's migration. The predicates are `capability_area`, `matrix_version`, `role_code`, `field_id` and `masking_version`; no `v_ace_*` or `public` object is created, altered or granted.

**Configuration and reference data**

- The two versions in force are read from their version columns; the SIT labels are `PM-2026.11` and `MASK-SIT-01`, the ones the source examples carry, and no production label is fixed here.
- LOV-CAPABILITY (the 14 areas, `REFERENCE_DATA` among them), LOV-ROLE and the coded reason list arrive through DP-07 with the version in force; no area, role code or reason code is a constant in code.
- The approver role that holds `A` is a matrix row, not a code constant: the SIT fixture gives it the letter and GAP-0891 records that TSD P4 T6.1 gives it to no role (ASM-1612). The login is the rwb-access login (DP-02) and no credential is named.

**Build steps**

1. `AuthorityRepository` with the read-only queries and a test that it has no write method.
2. `AuthorityRegisterService`, `MaskingMarkerService` and `GET /admin/dictionary-authority`, with the `R` check before any read; AC1, AC9.
3. `DictionaryFieldClient` against the P1 fake: owner role, personal flag, unknown field ID, 404, timeout; AC1, AC2, AC3, AC7.
4. `DictionaryLoadGate`, four checks in a fixed order with the first failure named; AC2, AC3, AC5, AC7.
5. `DictionaryLoadDecisionController` with the `A` check, the four-eyes rule, `Idempotency-Key` and `If-Match`; AC4, AC8.
6. `LoadOwnerClient` (one call, the same key on a retry, the 409, the 503) and the return path with the coded reason list; AC4, AC5, AC6.
7. The version test on a fixed clock (2026-11-30 and 2026-12-01) and a contract-fake run of the three operations; AC8.

**Feature switch.** None of its own. The service-level flag of RWB-P4-E1037-CON governs the baseline; a matrix, masking or dictionary version is released and rolled back as data on the load path, never by a flag, and this story always answers the version in force.

**Done when.** The tests in section 16 pass; the register answers both version labels, the letters of every role and, per field ID, the owner role and the marker; the gate approves a clean load, refuses a bad owner role, an unknown field ID or an uncovered personal field, refuses the author's own approval, and returns a load with a coded reason; an approval dated 2026-12-01 answers only from that date; and the build is green with no write statement and no read of a view or `public` table.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on all three operations |
| MSG-P4-002 | No Reference data `R` on the register, or no `A` on the gate | You cannot {action} here. Your role does not include it. | This story, on the register and on both decisions |
| MSG-P7-002 | The author of the load approves it | The person who loaded this version cannot approve it. A second person must approve. | This story, on approve |
| MSG-P1-002 | A dictionary check fails | The {source} load for {date} was refused: {check}. The previous load is still in use. | This story, on approve |
| MSG-GEN-001 | A required field or a reason code is empty or unknown | Enter {field}. | This story, on return and on a missing load ID |
| MSG-GEN-004 | A decision is sent from an old version, or with no `If-Match` | Someone else changed this record. Reload it to see their change. | This story, on the decisions |
| MSG-GEN-006 | P1's dictionary read, the list read or the owner is unavailable | {system} is not available. Your request is queued and will be retried. | This story, on all three operations |

No new message identifier is created: MSG-P4-001, MSG-P4-002, MSG-P7-002, MSG-P1-002, MSG-GEN-001, MSG-GEN-004 and MSG-GEN-006 are the ones the legacy story and the module already carry. For MSG-P4-002 the `{action}` names the action the caller tried  -  "read the register", "approve a load", "return a load"  -  and never a case fact or a field value. In MSG-P1-002 the `{check}` is the coded check name, for example `OWNER_ROLE_UNKNOWN`, and names no value. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built by this story. The register and the two decisions are what SCR-40 Reference data shows once Epic 8 delivers the screen; before that, the steward and the administrators use the operations directly, through the gateway-bff composite route of DP-19 with one hop per call.

| Screen | State | Where it is |
|---|---|---|
| SCR-40 Reference data | Loading, list, empty; the matrix and masking versions in force; a field row with its owner role and marker | E8; the route reads `GET /admin/dictionary-authority` |
| SCR-40 Reference data | Load waiting for approval; APPROVED from the valid-from date; returned with the reason code; refusal with MSG-P1-002 and the first failing check | E8; the route calls the two decisions |
| SCR-43 Roles and access | The Reference data letters of each role; unchanged by this story, which adds no screen state | E8; served by RWB-P4-E1016-APP |

The screen fields and the rendering of the register are Not specified in the source documents (GAP-0890; ASM-1611). This story returns a marker, an owner role and two version labels and never a rendering: the masked rendering belongs to the screen owner and the value belongs to rwb-source-data.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-064-01 | AC1, BR1, BR2 | Component | Seeded 122 objects and 1,366 fields through the P1 fake; the register read with and without a field list; matrix `PM-2026.11`; the count and completeness assertions of the dictionary itself are P1's |
| TC-E1-064-02 | AC2, AC3, BR3, BR4 | Component | The 14 products DP01 to DP14; DP01 with RW-DATASTEW; one product with two owner roles; one personal field ID with no masking row at `MASK-SIT-01` |
| TC-E1-064-03 | AC1, AC7, BR8 | Component | `DF-ACE-018` with owner RW-DATASTEW, refresh DAILY and late behavior "Keep the previous value and mark DP01 stale", read from the P1 fake and answered with its marker; the value `days_past_due` 95 is P1's and is not read here |
| TC-E1-064-04 | AC7, BR6, BR9 | Component | Load `LD-2026-065` before and after the dictionary row of `DF-ACE-204` exists; the corrected load and the unknown field ID; no migration edited |
| TC-E1-064-05 | AC8, BR7 | Contract | `LD-2026-067` approved on 2026-11-28 with valid from 2026-12-01; a fixed clock at 2026-11-30 and 2026-12-01; the older rows and their valid_to; the change history of a field definition itself is P1's |
| TC-E1-064-06 | AC4, AC5, BR5 | End to end | `LD-2026-064` with 1,366 rows authored by RW-REFADM, approved by the approver role of the fixture; the author's own approval refused with MSG-P7-002; the owner fake moving the version |
| TC-E1-064-07 | AC8, BR5 | Contract | Two approvers deciding `LD-2026-067` from version 1; one decision with no `If-Match`; the optimistic lock of a field definition is P1's |
| TC-E1-064-08 | AC8, BR7 | Component | Load approved and then a new version opened for 2026-12-01; the version in force on 2026-11-30 stays answered; the DRAFT contract version on a change is P1's |
| TC-E1-064-09 | AC9, BR10 | Component | RW-TRIBE with `R` only calls approve; refused 403 MSG-P4-002; a token with no role answers 401 MSG-P4-001 on all three operations; nothing written |

Every legacy test case of this key appears once and states the slice it contributes here. TC-E1-064-01 answers the register's completeness over the dictionary the P1 fake serves; TC-E1-064-02 the owner role and the personal coverage; TC-E1-064-03 the owner role, refresh cycle and late behavior a register entry names; TC-E1-064-04 the new-ACE-column path on the authority side; TC-E1-064-05 and TC-E1-064-07 the versioning and the lock of the decision; TC-E1-064-06 the whole-load refusal and the four-eyes rule; TC-E1-064-08 the date effect on the authority rows; and TC-E1-064-09 the refusal shape of a role without the right, which is this service's own answer. The read half of each legacy case (the dictionary row, the field version, the DC-ACE confirmation, the DRAFT contract) is RWB-P1-E1064-APP's and is not repeated. The `-ITG` copies belong to RWB-ITG-E1064-ITG. The full test, with its Given, When and Then, is in the Recovery Workbench Test Cases workbook, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: role codes, capability areas, letters, owner roles, field IDs, masking exceptions, version labels and reason codes are data rows or reference data read with the version in force; the lists arrive through DP-07.
- No personal data in answers, logs, tests or prompts: the register answers a marker, an owner role and two version labels, never a value, a rendering or a last four digits; every test row is synthetic and every fixture names a role code, never a person.
- The clear identity number never leaves ACE: `id_no_last4` (`DF-ACE-074`) is a field ID in this policy and a masked value in the customer view; this service reads neither the value nor the view.
- ACE data only through the owner's contract or `v_ace_*` views  -  and this service reads neither: the dictionary field read is P1's contract, and a class that names a view or a `public` table fails the build (DP-05, DP-01).
- No cross-schema read and no cross-schema key: `rwb_access` holds no foreign key into another schema and no copy of a definition, a product or a case row.
- A missing role, a missing letter, a missing owner role row and a missing masking row all resolve to refused or `masked`, never to allowed and never to `clear`.
- An approved version is never edited in place: a change is a new version with a later valid-from date, the load path is the only writer, and this story adds no write statement.
- No event is produced here: the topic is provisioned and unused, and the policy-change event belongs to the load stories.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner, and every field with a source, an owner, a refresh cycle and a late behavior  -  here, the one owner role each product resolves to and the letters that authorise a definition's read, change and approval | Business Requirements Epic 1, sections 3.1, 4 and 5 | None | All recovery processes | BR-P4-003; BR-P4-004; CTL-08; CTL-09; BR1, BR2, BR3, BR6 | TC-E1-064-01, TC-E1-064-02, TC-E1-064-03, TC-E1-064-04, TC-E1-064-06 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record and refresh  -  here, the owner role of the entry, the personal-field markers it carries and the version in force | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ACA-03; FEAT-ACA-04; FEAT-ACA-05 | All recovery processes | BR-P4-003; BR-P4-004; NFR-039; NFR-040; BR4, BR5, BR7, BR10 | TC-E1-064-05, TC-E1-064-07, TC-E1-064-08, TC-E1-064-09 |

The dictionary's content and its 122 and 1,366 rows are traced in RWB-P1-E1064-APP and RWB-P1-E1064-CON under the same two requirements. The legacy story is RWB-E1-064, disposition Split (rework); its other slices are RWB-P1-E1064-CON, RWB-P1-E1064-APP, RWB-P1-E1064-OPS and RWB-ITG-E1064-ITG.

### 19. Out of scope

- The five dictionary tables, the 122 objects, the 1,366 fields, the 14 product rows, the read model `v_data_dictionary`, the field version history, the data contracts and the DC-ACE confirmation: RWB-P1-E1064-APP and RWB-P1-E1064-CON. This story names them and reads none of them from a table.
- The 30 `recovery.v_ace_*` views, their definitions, their grants and the view conformance test: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- The submission, validation, verification and rollback of a reference load, and the file itself: the load owner under DP-07 (`POST /admin/reference-loads`, `.../verify`, `.../rollback`) and the approval gate of the lists of values, RWB-P4-AD010-APP, which covers the LOV load family and not this one.
- The matrix and masking load path, the masking pack content and its roster, and the version lifecycle rows: the pack owner under DL26 and the load stories RWB-P4-AD009-APP and RWB-P4-E1037-APP. This story reads the two versions in force and writes no row of them.
- The role catalogue and the authorise answer themselves (`GET /admin/roles`, `/masking-policies`, `/authorise`): RWB-P4-E1016-APP and RWB-P4-E1037-CON.
- The session, the role conflict check and the Entra group mapping: RWB-P4-E1022-APP and RWB-P1-E1014-CON.
- The delegation of authority lookup and the approval limits: RWB-P4-E2013-APP.
- The access log of a dictionary read and break-glass: RWB-P4-E1039-APP and RWB-P4-AD007-APP.
- The composed end-to-end proof across P1, P3 and P4: RWB-ITG-E1064-ITG. The E8 screen SCR-40 itself and the gateway route: their E8 stories and RWB-PLT-N001-CON.
- Cases for stage 2 data products (legacy RWB-E2-010) and the sandbox dictionary (RWB-E1-065).
