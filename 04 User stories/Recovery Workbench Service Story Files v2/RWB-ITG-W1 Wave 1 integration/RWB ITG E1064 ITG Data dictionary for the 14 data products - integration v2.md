# RWB-ITG-E1064-ITG Data dictionary for the 14 data products

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1064-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-ITG-E1064-ITG-14); confirm with the epic design record |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-064 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1064-ITG-16); set by the squad at refinement |
| Patterns applied | DP01, DP05, DP07, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1064-CON |
| Contract fake library version | None used: P1, P3 and P4 are the real SIT services on their published contracts and are not faked (section 12.8); published fake library version Not specified in the source documents (DOR-RWB-ITG-E1064-ITG-22) |
| Integration dependencies | RWB-P1-E1064-APP, RWB-P4-E1064-APP (not built yet; the run needs their published contracts in SIT) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-005, FR-PLT-006, FR-PLT-007) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-064 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-ITG-E1064-ITG-L339). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 15 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer** proving the data dictionary and its ACE read contract end to end on the real SIT services of rwb-source-data (P1) and rwb-access (P4) and their published contracts, I want **one suite that reads the 122 objects and 1,366 fields, adds a new ACE column through a governed reference load, versions a field change, records the ACE confirmation and publishes DC-ACE**, so that **every definition of the 14 data products is proved to come from one governed load under one owner, the ACE read path is proved to be agreed before it is published, and the 30 ACE views are proved to have one dictionary row per column, before wave 1 exits**.

### 2. Business rationale

The dictionary is the only place that says what a field is, where it comes from and who owns it. It covers 122 objects and 1,366 fields: the 92 Workbench tables hold 1,062 fields, 49 of them on the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`, and the 30 `v_ace_*` views hold 304 fields, 177 in Section A and 127 in Section B. The Workbench loads no source data (D-RCV-35 U1), so every source is either ACE, whose columns are recorded as `public.table.column` on the view fields where the view reads one column, or the Workbench itself. This story does not create a table, a column or a migration: V0001 owns `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` and seeds the 122 objects and 1,366 fields.

RWB-E1-064 defined that dictionary, its change history, its reference load and its ACE read contract when all of it lived in one module. In the target the dictionary stays with one service, rwb-source-data (P1), but it is no longer delivered by one service. The governance rows are submitted, approved and verified on the reference-data contract of rwb-case (P3) and applied by P1; the ACE columns the dictionary describes are read by P1 alone, because only P1 holds SELECT on the 30 `recovery.v_ace_*` views (Arch v5 slide 29); the change is authorised by the Reference data right of rwb-access (P4); and the dictionary and contract reads are served as one composite route on gateway-bff (Arch v5 slide 20).

The component copies of the behaviour are RWB-P1-E1064-APP and RWB-P4-E1064-APP. Those stories build and unit-test the metadata tables, the field and contract operations, the load apply path and the right check inside their own services, against the published contracts of their neighbours. This integration story exists because four of the facts that make the dictionary trustworthy cannot be proved inside one service:

- The governance fact is one fact about two services. A new ACE column reaches the dictionary only when the view column exists and the load has been submitted, approved and verified on P3 and applied by P1, with no applied migration edited; a load with one bad row must leave the dictionary in force untouched (ASM-0531).
- The source fact is a fact about the only reader of the views. `ACC0000017` has `delay_days` 95, and the suite may assert that value only through P1's data-product record read, never through a `recovery.v_ace_*` query of its own (ASM-0533).
- The agreement fact crosses from a role to a contract state. The ACE team lead's confirmation, recorded as a role, a date and a stored document reference, is what turns DC-ACE from DRAFT into PUBLISHED, and a contract without a confirmation must be refused (ASM-0534).
- The conformance fact is a merge gate. CHK-01 compares every view column with `sys_fields`, so a view column with no dictionary row fails the pipeline and blocks the merge (ASM-0535).

The suite therefore carries no legacy criterion: every criterion of this story is new (D-RCV-60) and is written to prove the deliverable in the title on real services, carrying the legacy values of RWB-E1-064 - 122 objects, 1,366 fields, 92 tables, 1,062 table fields, 49 extension fields, 30 views, 304 view fields, 177 and 127, 297 of 304, the 7 derived fields, `ACC0000017`, 95, `DF-ACE-018`, `DF-ACE-204`, `DF-ACE-020`, `DC-ACE`, `DC-ACE-2`, `V0002`, `V0003`, 2026-11-12, 2026-11-18 and `DOC-SYN-0640` - so that a reader can follow the legacy story beside it. The area the sources leave open is recorded once as GAP-0373 and settled by ASM-0531 to -6; every one of those defaults applies in this story.

P3 rwb-case is not an I dependency of this suite. It is a wave-1 published-contract precondition: the reference-load operations are published and versioned in the registry before the suite runs, and the suite consumes them exactly as it consumes the P1 and P4 contracts (ASM-0531). The two I dependencies are the builds whose behaviour the run exercises, the P1 dictionary and contract behaviour and the P4 session and right check.

The only thing that is faked is the outside world: the ACE source behind the 30 views, reached through a recorded stub of `public.account` and `public.collateral_detail`, and a clock that places the confirmation on 2026-11-12 and the field change on 2026-11-18. P1, P3 and P4 are the real services on their published SIT contracts, and a run that needs a fake for any of them fails the preflight, because a fake would defeat the purpose of the run.

The measure the story is read against is the legacy measure: 100 percent of the 1,366 fields return a data type, a physical type, a description, a source system, an owner role, a refresh cycle and a behaviour when late, all 30 views have one dictionary row per column, and DC-ACE is PUBLISHED at version 1 with its 304 fields and the read interfaces V0002 and V0003.

### 3. Preconditions

- RWB-P1-E1064-APP is done: `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` exist in schema `rwb_source_data` with the V0001 seed of 122 objects and 1,366 fields, and the dictionary and contract operations, the data-product record read and the freshness read of section 12.2 are published.
- RWB-P4-E1064-APP is done: the session read and the Reference data right check of section 12.2 are published, so a PATCH of a field by a role that holds Reference data R only is refused with 403 and MSG-P4-002.
- The P3 rwb-case reference-load contract is published and versioned in the registry, with table `sys_fields` accepted as a load target (ASM-0531). P3 rwb-case is a wave-1 published-contract precondition of this suite and not an I dependency; the suite submits, approves and verifies the load on P3 and asserts the applied result only through P1.
- V0001, V0002 and V0003 are applied in SIT, and the 30 `recovery.v_ace_*` views exist with SELECT granted to `rwb_source_data` alone (Arch v5 slide 29).
- CHK-01, the view conformance test of RWB-E1-069, runs in the pipeline and compares every view column with `sys_fields` (ASM-0535).
- The W1J01 synthetic fixture set is available with the dictionary fixture, the ACE column fixture in which `v_ace_collateral_detail` holds 11 fields and no row for `insurance_expiry`, the contract fixture, and the synthetic users RW-DATASTEW, RW-REFADM, RW-TRIBE and RW-COE with their session grants.
- The ACE source stub is deployed: `public.account` holds `ACC0000017` with `delay_days` 95, and `public.collateral_detail` holds and withholds `insurance_expiry` under its control, so the accepted and the refused load of AC4 are both deterministic.
- gateway-bff is deployed with the `/api/recovery/source-data/v1/**` route, its Redis session store and the 2 s client budget (ASM-0536).
- The synthetic data steward holds RW-DATASTEW (Reference data U), the reference data administrator holds RW-REFADM (Reference data C), RW-TRIBE holds Reference data R only, and the confirming role for the ACE read contract is "ACE team lead" (ASM-0534).
- No production data is read, copied or connected to; every account number, national ID number, phone number, name and identity used by the run is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: runs the preflight, which reads the OpenAPI documents of P1, P3 and P4 for the operations of section 12.2 and fails before any assertion if a path, a field, a status code or a message ID has drifted; it also confirms that no fake is configured for P1, P3 or P4, and that the W1J01 fixture set and the ACE source stub are the versions the suite expects.
2. Harness: reads the dictionary page `GET /api/recovery/source-data/v1/admin/data-dictionary/fields?page=1&size=1` through gateway-bff with the session cookie of a Reference data R holder and asserts 122 objects and 1,366 fields, then the 1,062 table fields with the 49 on the four extension tables and the 304 view fields with 177 from Section A and 127 from Section B.
3. Harness: asserts that every one of the 1,366 fields returns a data type, a physical type, a description, a source system, an owner role, a refresh cycle and a behaviour when late, that 297 of the 304 view fields name an ACE column in the form `public.table.column`, and that the 7 derived fields carry source system ACE and no single ACE column.
4. Harness: counts the source-system rows of the 30 `v_ace_*` objects through the same P1 read and asserts one object row and one field row per view column, no column without a row and no row without a column, and the 49 extension fields `DF-EXT-001` to `DF-EXT-049`.
5. Harness: reads `v_ace_account` / `days_past_due` through the P1 dictionary read and asserts `DF-ACE-018`, data type `NUMBER`, physical type `integer`, source system ACE, source field `public.account.delay_days`, data product `DP01`, refresh cycle `DAILY`, owner role `RW-DATASTEW` and late behaviour "Keep the previous value and mark DP01 stale"; then reads `DP01` for `ACC0000017` through `GET /api/recovery/source-data/v1/data-products/{productCode}/records` and asserts `days_past_due` 95 (ASM-0533).
6. Harness: confirms that the ACE source stub holds `v_ace_collateral_detail` at 11 fields with no row for `insurance_expiry`, adds `public.collateral_detail.insurance_expiry` so that `V0003` exposes it as `v_ace_collateral_detail.insurance_expiry`, and submits `DF-ACE-204` as a load for table `sys_fields` through `POST /api/recovery/case/v1/admin/reference-loads` as RW-REFADM (ASM-0531).
7. Harness: approves the load through `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve` and verifies it through `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/verify`; P1's own load path applies the approved rows in the transaction of the approval and carries the load state on the load record, and the suite then asserts the new row and version 1 of `DF-ACE-204` through the P1 dictionary read, and asserts that CHK-01 passes on the next pipeline run and that every applied migration file hash is unchanged (ASM-0535).
8. Harness: repeats the same load naming `public.collateral_detail.insurance_date` and asserts the refusal in full with MSG-P1-002 and no row written; and repeats it once more naming a single ACE column for a derived field and asserts the same refusal (ASM-0533).
9. Harness: with the clock at 2026-11-18, changes the late behaviour of `DF-ACE-018` to "Keep the previous value, mark DP01 stale and alert the data steward daily" with the reason "add the daily stale alert for DP01" and the If-Match version, asserts version 2 dated 2026-11-18 with that reason and version 1 still readable, then sends a change with an empty reason and asserts 422 with MSG-GEN-001 with the field left at version 2.
10. Harness: records the confirmation of `DC-ACE` on 2026-11-12 as role "ACE team lead" with document reference `DOC-SYN-0640` through `PATCH /api/recovery/source-data/v1/admin/data-contracts/{contractId}` as RW-DATASTEW, publishes it through `POST /api/recovery/source-data/v1/admin/data-contracts/{contractId}/publish`, and asserts status PUBLISHED at version 1 with the confirmation, 304 fields and the read interfaces `V0002` and `V0003`; then publishes `DC-ACE-2` with no confirmation and asserts 409 with MSG-P1-021 for system ACE (ASM-0534).
11. Harness, concurrency: has two data stewards read `DF-ACE-020` at version 1 and both send a change with version 1, asserts the first saved as version 2 and the second refused 409 with MSG-GEN-004, then sends a third change with no If-Match version and asserts 428 with MSG-GEN-004.
12. Harness, contract version: with `DC-ACE` PUBLISHED at version 1, changes `DF-ACE-018` to version 2 and asserts that `DC-ACE` version 2 is created as DRAFT while version 1 stays PUBLISHED and in force.
13. Harness, access and privacy: reads the rights of each synthetic user through `GET /api/recovery/access/v1/me/session`, has RW-DATASTEW change a field with PATCH and the If-Match version, has RW-TRIBE send `PATCH /api/recovery/source-data/v1/admin/data-dictionary/fields/DF-ACE-018` and asserts 403 with MSG-P4-002 and no version written, then scans every response and log of the dictionary, the contracts and the load and asserts that no national ID number, phone number, name or account number appears and that the confirmation names a role, not a person (ASM-0536).
14. Harness: cleans up the synthetic load, the two business dates, the fixture rows and the extra contract version, restores the stub and the clock, and writes the evidence report with one verdict per test case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Publish of a contract without the ACE team's confirmation | 409; the contract stays DRAFT | MSG-P1-021 | AC6 |
| X2 | A field change without a reason | 422; no version written | MSG-GEN-001 | AC5 |
| X3 | A dictionary load with an unknown field, a missing attribute, a source system outside ACE and Workbench, or an ACE source field that is not a column of the view and is not one of the 7 derived fields | The load is refused in full; the dictionary in force stays | MSG-P1-002 | AC4, AC13 |
| X4 | Two stewards change the same field from the same version | The second change is refused with 409 | MSG-GEN-004 | AC7 |
| X5 | A field of a published contract changes | A new DRAFT contract version; the published version stays in force | None to a user | AC8 |
| X6 | A view column exists with no `sys_fields` row | CHK-01 fails and the merge is blocked | `v_ace_collateral_detail.insurance_expiry` has no data dictionary entry | AC2, AC4 |
| X7 | A field definition is changed with no If-Match version | 428; no version written | MSG-GEN-004 | AC7 |
| X8 | A role that holds Reference data R only sends a field change | 403; no version written | MSG-P4-002 | AC11 |
| X9 | The P1 store or a view is unavailable | The read fails with 503 and the suite retries on the same business date; the dictionary in force is unchanged | MSG-GEN-006 | AC1, AC10 |
| X10 | A consumed contract drifts from the published one (path, field, status code or message ID) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC10 |
| X11 | A fake is configured for P1, P3 or P4 | The preflight refuses the run: only the ACE source stub, the W1J01 fixture set and the clock may be stubbed | None | AC14 |
| X12 | The W1J01 fixture set, or the dictionary, ACE column or contract fixture it carries, is missing or does not match the run | The run fails as a fixture fault and names the missing element; no production value is substituted | None | AC1, AC4, AC12 |
| X13 | A suite step tries to read a service schema or a `recovery.v_ace_*` view directly | The step does not exist: the suite is built with no client for a service schema, and the pipeline scan fails any change that adds one | None | AC15 |

X1 to X7 are the legacy exception paths of RWB-E1-064 carried onto the real services; X8 to X13 are the failures that only appear when the run leaves one service. X8 is proved by the access test rather than by an acceptance criterion of its own, as in the legacy story, and is covered by AC11 here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the two I dependencies, the P3 published reference-load contract and the published contracts of P1 and P4, not their source code, and it owns no schema, no table and no migration |
| Negotiable | The fixture composition, the poll interval, the report layout and the stub control names are configuration; the counts, the field IDs, the field values, the late behaviours, the contract codes, the interfaces and the message IDs are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: one governed load, one owner per field, one row per view column, a versioned change with a reason, a confirmation before a publish, a new DRAFT on change and a right check at the edge |
| Estimable | One suite module, one load driver, five probes, one privacy scan and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a REST response, a status code and message ID, a contract version, a CHK-01 result, a migration file hash or a scan of the responses and logs |

### 7. Acceptance criteria

```gherkin
Feature: Data dictionary for the 14 data products, proven across the wave 1 services

  Background:
    Given the dictionary holds 122 objects and 1,366 fields from V0001
    Given the governance load of owner role, refresh cycle and late behaviour was published on 2026-11-30
    Given data product "DP01" Account and arrears has owner role RW-DATASTEW and system of record "ACE (ingested from ALS)"
    Given contract "DC-ACE" for source system "ACE" and read interfaces "V0002" and "V0003" is "DRAFT" with 304 mapped fields
    Given all involved services are deployed in SIT with their published contracts and the RWB-ITG-W1J01-ITG synthetic set is loaded
    Given no production value is used and P1, P3 and P4 are not faked

  Scenario: AC1 Every field is defined (new, D-RCV-60)
    Given the dictionary holds 122 objects and 1,366 fields from V0001, read only through the rwb-source-data contract
    When a developer calls `GET /api/recovery/source-data/v1/admin/data-dictionary/fields?page=1&size=1`
    Then the response reports 122 objects and 1,366 fields
    Then the 92 Workbench tables hold 1,062 fields, of which 49 are on the four extension tables
    Then the 30 v_ace_* views hold 304 fields, 177 from Section A and 127 from Section B
    Then every field has a data type, a physical type, a description, a source system, an owner role, a refresh cycle and a behaviour when late
    Then 297 of the 304 view fields name an ACE column in the form public.table.column
    Then the count of personal fields is that of sys_fields.is_personal at the version in force, read only through the rwb-source-data contract, and is not written as a constant
    Then the 7 derived view fields v_ace_contact.contact_type, city, post_code and country, and v_ace_plan.installments, recommended_installment and recommended_package carry source system ACE and no single ACE column

  Scenario: AC2 Every ACE view has dictionary rows (new, D-RCV-60)
    Given V0001, V0002 and V0003 are applied in SIT and the suite reads the ACE dictionary rows only through the rwb-source-data contract
    When the suite counts the dictionary rows of source system "ACE" through the P1 contract
    Then 30 v_ace_* objects are returned with 304 fields
    Then each v_ace_* view has one sys_objects row and one sys_fields row per column
    Then no v_ace_* view has a column without a row and no row without a column
    Then the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext hold 49 fields, DF-EXT-001 to DF-EXT-049

  Scenario: AC3 The arrears field comes from the ACE delay days (new, D-RCV-60)
    Given V0001 and V0002 are applied in SIT
    Given the ACE source stub holds account "ACC0000017" with delay_days 95 in public.account, which only rwb-source-data reads
    When the developer reads entity "v_ace_account" and field "days_past_due" through `GET /api/recovery/source-data/v1/admin/data-dictionary/fields?entity=v_ace_account&field=days_past_due`
    Then the row holds field ID "DF-ACE-018", data type "NUMBER" and physical type "integer"
    Then the row holds source system "ACE" and source field "public.account.delay_days"
    Then the row holds data product "DP01", refresh cycle "DAILY", owner role "RW-DATASTEW" and late behaviour "Keep the previous value and mark DP01 stale"
    Then `GET /api/recovery/source-data/v1/data-products/DP01/records` for "ACC0000017" returns days_past_due 95, and the value is not asserted by a view query

  Scenario: AC4 A new ACE column is a dictionary change through the reference load (new, D-RCV-60)
    Given a dictionary fixture in which the P1 dictionary holds 11 fields for v_ace_collateral_detail and no row for "insurance_expiry"
    Given the ACE source stub adds public.collateral_detail.insurance_expiry as RWB-ACE-001 does, and V0003 exposes it as v_ace_collateral_detail.insurance_expiry, which only rwb-source-data reads
    When the reference data administrator loads field "DF-ACE-204" with source system "ACE", source field "public.collateral_detail.insurance_expiry", owner RW-DATASTEW, refresh "WEEKLY" and late behaviour "Keep the previous value and mark DP06 stale" through `POST /api/recovery/case/v1/admin/reference-loads` with table sys_fields
    Then the load is validated and the field row and version 1 of DF-ACE-204 are written
    Then `GET /api/recovery/source-data/v1/admin/data-dictionary/fields?entity=v_ace_collateral_detail&field=insurance_expiry` returns the row
    Then CHK-01 passes on the next pipeline run and no Flyway migration file was edited
    When the same load names source field "public.collateral_detail.insurance_date"
    Then the load is refused in full with MSG-P1-002 and no row is written

  Scenario: AC5 A change keeps its history (new, D-RCV-60)
    Given field "DF-ACE-018" is at version 1 with late behaviour "Keep the previous value and mark DP01 stale"
    When the data steward changes its late behaviour to "Keep the previous value, mark DP01 stale and alert the data steward daily" with reason "add the daily stale alert for DP01" on 2026-11-18
    Then field "DF-ACE-018" is at version 2 dated 2026-11-18 with that reason
    Then version 1 stays readable with its own date and late behaviour
    When the data steward sends a further change with an empty reason
    Then the system refuses the call with status 422 and MSG-GEN-001 for field "reason"
    Then field "DF-ACE-018" stays at version 2

  Scenario: AC6 The ACE read path is agreed before it is published (new, D-RCV-60)
    Given the data steward recorded the confirmation of "DC-ACE" by role "ACE team lead" on 2026-11-12 with document reference "DOC-SYN-0640"
    When the data steward publishes "DC-ACE"
    Then the contract status is "PUBLISHED" with version 1 and the confirmation on 2026-11-12
    Then the contract lists 304 fields and the read interfaces "V0002" and "V0003"
    When a contract "DC-ACE-2" has no recorded confirmation and the data steward publishes it
    Then the system refuses the call with status 409 and MSG-P1-021 for system "ACE"

  Scenario: AC7 Two changes to the same field at once (new, D-RCV-60)
    Given two data stewards read field "DF-ACE-020" at version 1
    When both send a change with version 1
    Then the system saves the first change as version 2
    Then the system refuses the second with status 409 and MSG-GEN-004
    When a third steward sends a change with no If-Match version
    Then the system refuses it with status 428 and MSG-GEN-004

  Scenario: AC8 A change to a field in a published contract opens a new draft (new, D-RCV-60)
    Given contract "DC-ACE" is "PUBLISHED" at version 1
    When field "DF-ACE-018" changes to version 2
    Then the system creates contract "DC-ACE" version 2 as "DRAFT"
    Then version 1 stays "PUBLISHED" and in force

  Scenario: AC9 The load is approved on P3 and applied by P1 (new, D-RCV-60)
    Given a dictionary fixture with the row for "DF-ACE-204" to add
    When the reference data administrator submits the load through `POST /api/recovery/case/v1/admin/reference-loads`, approves it through `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve` and verifies it through `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/verify`
    Then the approved rows are applied by P1 and read back through `GET /api/recovery/source-data/v1/admin/data-dictionary/fields`
    Then the suite calls no P1 reference-load operation and reads no sys_fields table
    Then every applied Flyway migration file is unchanged

  Scenario: AC10 The dictionary read is one hop through gateway-bff and role checked (new, D-RCV-60)
    Given the caller holds a session cookie on gateway-bff
    When the developer reads the dictionary and the contracts through `/api/recovery/source-data/v1/**`
    Then every call is one hop to rwb-source-data with the 2 s client budget
    Then the caller's rights are read through `GET /api/recovery/access/v1/me/session`
    Then "RW-DATASTEW" changes a field with `PATCH /api/recovery/source-data/v1/admin/data-dictionary/fields/{fieldCode}` and the If-Match version and the change succeeds
    Then no call passes through a second service to reach the dictionary

  Scenario: AC11 A role without Reference data U is refused (new, D-RCV-60)
    Given "RW-TRIBE" holds Reference data R only and the suite confirms it on `GET /api/recovery/access/v1/me/session`
    When "RW-TRIBE" sends `PATCH /api/recovery/source-data/v1/admin/data-dictionary/fields/DF-ACE-018`
    Then the call is refused with 403 and MSG-P4-002
    Then no version is written

  Scenario: AC12 The dictionary holds definitions, not personal values (new, D-RCV-60)
    Given the responses and the logs of the dictionary, the contracts and the load
    When the suite scans them
    Then each holds definitions, roles, dates and column names only
    Then no national ID number, phone number, name or account number is found
    Then the confirmation of "DC-ACE" names a role, not a person

  Scenario: AC13 The seven derived fields carry ACE and no single column (new, D-RCV-60)
    Given the 7 derived view fields v_ace_contact.contact_type, city, post_code and country, and v_ace_plan.installments, recommended_installment and recommended_package are held in the P1 dictionary, which the suite reads only through the rwb-source-data contract
    When the suite reads them through the P1 dictionary contract
    Then each carries source system "ACE" and no single ACE column
    When a load names a single ACE column for one of the 7 derived fields
    Then the load is refused in full with MSG-P1-002

  Scenario: AC14 A fake is refused for P1, P3 or P4 (new, D-RCV-60)
    Given a run is configured with a fake for P3
    When the preflight of the suite starts
    Then the run is refused before any step
    Then only the ACE source stub, the W1J01 fixture set and the clock may be stubbed

  Scenario: AC15 The suite reads no service schema and no ACE view (new, D-RCV-60)
    Given the suite is built with its clients
    When the pipeline scans the suite for a client to rwb_source_data, rwb_case or rwb_access and for a read of a recovery.v_ace_* view
    Then the scan finds none
    Then the ACE value of days_past_due is read through the P1 data-product record read
    When a change adds such a client or such a view read
    Then the pipeline scan fails the change

  Scenario: AC16 The story adds no table, column, index or constraint (new, D-RCV-60)
    Given the migration file hashes of P1 and P3 are recorded before the run in SIT
    When the suite compares them with the migration file hashes after the run
    Then no DDL and no migration file added or edited by this story is found
    Then sys_objects, sys_fields, sys_field_version, data_product and data_contract are created by V0001 and owned by P1 in rwb_source_data

  Scenario: AC17 No business value is written in code and no production value is read (new, D-RCV-60)
    Given the suite source and the run configuration
    When the suite is scanned and run against SIT
    Then no owner role, refresh cycle, late behaviour, count or contract content is a constant in the code
    Then the run refuses to start against any environment other than SIT

  Scenario: AC18 A consumed call fails or does not answer (new, D-RCV-60)
    Given the suite calls a consumed service through its published contract
    When the consumed call fails or gets no answer within the 2 s client budget
    Then the run stops at that step and the failure is reported against the owning service
    Then no fake is put in its place and no value is substituted
```

**Target reading.** The counts, the field IDs, the source field, the late behaviours, the contract codes, the interfaces, the dates and the document reference are the legacy values of RWB-E1-064, copied character for character. The five monolith endpoints become the P1 operations of `/api/recovery/source-data/v1` (DP-13), the load becomes the P3 reference-load contract with P1 as the applying service (DP-07, ASM-0531), the `recovery.v_ace_*` reads of the legacy story become the P1 data-product and dictionary reads (DP-05, ASM-0533), the session and the right check come from P4 (ASM-0536), and the composite read is the gateway-bff route (DP-19). The confirmation stays a role, a date and a stored document reference, because no person name is recorded anywhere (ASM-0534).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every field carries its data type, physical type, description, source system, owner role, refresh cycle and behaviour when late, and every view field names its ACE column as `public.table.column`, or, for the 7 derived view fields, states that the view derives it | REQ-RDF-001; sys_fields |
| BR2 | The dictionary holds 122 objects and 1,366 fields: 92 tables with 1,062 fields, 49 of them on the four extension tables, and 30 views with 304 fields, 177 in Section A and 127 in Section B | D-RCV-35; Data Tier Map v1 section 8 |
| BR3 | Each data product has exactly one system of record and one owner role; a source is either an ACE column recorded on a view field or the Workbench itself | REQ-RDF-001; data_product; D-RCV-35 U1 |
| BR4 | A data contract is published only after its confirming role is recorded with a date and a stored document reference; a publish without a confirmation is refused with 409 and MSG-P1-021 | DL12 (open; assumptions ASM-0189, ASM-2559 and ASM-2608 confirmed); data_contract; ASM-0534 |
| BR5 | A field change creates a new `sys_field_version` row with a date and a reason; earlier versions stay readable, and a change with an empty reason is refused with 422 and MSG-GEN-001 | Reference data change process; DT02; Principle 1 |
| BR6 | A dictionary load with an exception is refused in full; an ACE source field that is not a column of the view is an exception unless the view derives it | Reference data change process, step 3; CTL-08 |
| BR7 | A change to a field of a published contract opens a new contract version as DRAFT; the published version stays in force until the new one is confirmed and published | R-UNI-38 |
| BR8 | `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` stay with P1 rwb-source-data and are created by V0001; this story adds no table, column, index or constraint and publishes rows only through the P3 load and the P1 operations | RWB-E1-001; D-RCV-28; DP-01; DP-15 |
| BR9 | A new ACE column reaches the dictionary as a reference load after its view column exists; an applied migration is never edited, and CHK-01 blocks the merge until the row exists | RWB-E1-069; BR-P1-001; ASM-0535 |
| BR10 | The load is submitted, approved and verified through the P3 rwb-case reference-load contract and the approved rows are applied by P1; the suite drives no P1 reference-load operation and reads no `sys_fields` table | ASM-0531; DP-07; DP-01 |
| BR11 | The dictionary and the contracts are read and changed only through the P1 operations of section 12.2; the suite holds no client for `rwb_source_data`, `rwb_case` or `rwb_access` | ASM-0532; DP-01 |
| BR12 | Only P1 reads the 30 `recovery.v_ace_*` views; the suite asserts the ACE value of `days_past_due` through the P1 data-product record read and never queries a view | Arch v5 slide 29; DP-05; ASM-0533 |
| BR13 | Every dictionary, contract and session call is one hop through gateway-bff to the owning service with the 2 s client budget, and no call passes through a second service | ADR-020; DP-11; DP-19; ASM-0536 |
| BR14 | The Reference data right is checked on every read and every change; a role with Reference data R only is refused a change with 403 and MSG-P4-002 and no version is written | DP-08; P4 right check; RWB-E1-064 section 10 |
| BR15 | The dictionary holds definitions, not values: no API response, event, workflow input, fixture or log of this story carries a national ID number, phone number, name or account number, and the confirmation names a role, not a person | Legacy section 17; Template and Rules §R7.2 s17 |
| BR16 | No business value is written in code or in the suite: the owners, refresh cycles, late behaviours, counts and contract content are data rows read at run time | Principle 1; DT02 |
| BR17 | No DDL and no migration of this story: V0001 owns the five tables, and the only schema change a criterion touches is the one RWB-ACE-001 makes in ACE | RWB-E1-001; DP-15 |
| BR18 | No production value is read, copied or connected to; the run is pinned to SIT with the synthetic set and refuses to start against any other environment | Legacy section 17; Guardrail |

### 9. State transitions

None of the case status. This story observes and changes the data contract status:

| From | Event | Condition | To |
|---|---|---|---|
| None | Contract created for source system ACE | 304 fields mapped | DRAFT (data_contract.status) |
| DRAFT | Published by the data steward | The confirming role, date and document reference are recorded | PUBLISHED, version 1 |
| DRAFT | Published by the data steward | No confirmation is recorded | No transition; 409 MSG-P1-021 |
| PUBLISHED | A field of the contract changes | The field reaches a new version | A new version DRAFT; the published version stays PUBLISHED and in force |
| DRAFT | The new version is confirmed and published | Every check passes | PUBLISHED; the earlier version retires from force |

The field versions and the load:

| From | Event | Condition | To |
|---|---|---|---|
| None | A field is read at its first definition | The load was applied | Version 1 with its date |
| Version n | A change with a reason and the If-Match version | The row version still matches | Version n+1 with its date and reason; version n stays readable |
| Version n | A change with an empty reason | None | No version; 422 MSG-GEN-001 |
| Version n | A change from a stale version | The row version moved on | No version; 409 MSG-GEN-004 |
| Version n | A change with no If-Match version | None | No version; 428 MSG-GEN-004 |
| None | A load submitted on P3 | A row fails a check | No row anywhere; MSG-P1-002, the dictionary in force stays |
| Submitted | Approved and verified on P3 | Every row passes | Applied by P1; the rows and their version 1 exist |

The states the run observes across the services:

| Item | States |
|---|---|
| Data contract | DRAFT, PUBLISHED, a new DRAFT version of a published contract |
| Field | Version 1, version 2, refused change |
| Reference load | Submitted, approved, verified, refused in full |
| CHK-01 | Passed on the next pipeline run, failed and the merge blocked |
| Suite run | Not started, preflight failed, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the stub and clock control, the cleanup and the evidence report |
| RW-DATASTEW, data steward and data product owner | Changes field definitions, records the confirmation, publishes the contract (Reference data U) |
| RW-REFADM, reference data administrator | Submits the dictionary load on P3 (Reference data C) |
| RW-COE, centre of excellence analyst | Reads and changes field definitions and reads the contracts (Reference data CRUD) |
| ACE team lead | Confirms the ACE read contract as a role; owns the ACE columns DC-ACE names (RWB-ACE-001) |
| RW-TRIBE, RW-AUDIT and other roles with Reference data R | Read the dictionary and the contracts and may not change them |
| Service owner of rwb-source-data (P1) | Owns the five metadata tables, the dictionary and contract operations, the data-product record read and the freshness read, and is the only reader of the 30 views |
| Service owner of rwb-case (P3) | Owns the reference-load contract that submits, approves, verifies and rolls back the governance load, and the list read |
| Service owner of rwb-access (P4) | Owns the session read, the Reference data right check and the refusal of MSG-P4-002 |
| Service owner of gateway-bff | Owns the composite route and the session cookie |
| No role | Reads a service schema or a `recovery.v_ace_*` view directly, edits an applied migration, or takes production data into the run |

Approval levels: no delegation of authority level applies; the confirmation of the ACE read contract is the confirming role's record under BR4, as in the legacy story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-088 | sys_objects | object_name | Read through the P1 contract |
| DF-REF-091 | sys_objects | data_product | Read through the P1 contract |
| DF-REF-092 | sys_objects | system_of_record | Read through the P1 contract |
| DF-REF-095 | sys_fields | field_id | Read through the P1 contract |
| DF-REF-096 | sys_fields | object_name | Read through the P1 contract |
| DF-REF-097 | sys_fields | field_name | Read through the P1 contract |
| DF-REF-098 | sys_fields | data_type | Loaded through P3, applied by P1, read through the P1 contract |
| DF-REF-099 | sys_fields | physical_type | Loaded through P3, applied by P1, read through the P1 contract |
| DF-REF-103 | sys_fields | source_system | Loaded through P3, applied by P1, read through the P1 contract |
| DF-REF-104 | sys_fields | source_field | Loaded through P3, applied by P1, read through the P1 contract |
| DF-REF-105 | sys_fields | is_personal | Read through the P1 contract |
| DF-REF-106 | sys_fields | description | Loaded through P3, applied by P1, read through the P1 contract |
| DF-REF-107 | sys_fields | owner_role | Loaded through P3, applied by P1, read through the P1 contract |
| DF-REF-108 | sys_fields | refresh_cycle | Loaded through P3, applied by P1, read through the P1 contract |
| DF-REF-109 | sys_fields | late_behavior | Loaded through P3, applied by P1, read through the P1 contract |
| DF-REF-110 | sys_fields | interface_id | Loaded through P3, applied by P1, read through the P1 contract |
| DF-REF-111 to DF-REF-115 | sys_field_version | all fields | Written by P1 on a change; read through the P1 contract |
| DF-OPS-010 to DF-OPS-020 | data_contract | all fields | Written by P1 through the contract operations; read through the P1 contract |
| DF-REF-070 to DF-REF-079 | data_product | all fields | Read through the P1 contract |
| DF-EXT-001 to DF-EXT-049 | party_ext, contact_point_ext, account_ext, valuation_ext | all fields | Read through the P1 dictionary contract; owned by P1 |
| DF-ACE-018, DF-ACE-020, DF-ACE-204 | v_ace_account, v_ace_collateral_detail | days_past_due, the changed field, insurance_expiry | Read through the P1 dictionary and data-product contracts; never by a view query |
| DF-ACE fields of the 304 view fields | the 30 v_ace_* views | every column of every view | Read by P1 only and asserted here through the P1 dictionary contract |

`sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` exist in Recovery Workbench Physical Schema v7, are created by V0001 and are owned by P1 in schema `rwb_source_data` (Ownership Map). This story writes no DDL and no row of its own: the rows are written by P1 on the P3 load and on the P1 operations. Field IDs are those of the Logical Data Model and Data Dictionary and are copied unchanged. No criterion or test data of this story reads a `recovery.v_ace_*` view; the 30 views are read by P1 only and asserted here through the P1 dictionary and data-product contracts (BR12).

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The reserved names of P2 rwb-integration - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` - are not used, and no `rwb_integration` table is written. The dictionary and the contracts belong to P1 rwb-source-data, base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, queue `rwb-source-data` and schema `rwb_source_data`; the reference load belongs to P3 rwb-case, base `/api/recovery/case/v1`, queue `rwb-case` and schema `rwb_case`; the session and the right check belong to P4 rwb-access, base `/api/recovery/access/v1`, queue `rwb-access` and schema `rwb_access`.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/admin/data-dictionary/fields` | P1 rwb-source-data | AC1, AC2, AC3, AC4, AC5 and AC13: the field page with the object and field counts, and the entity and field reads with `page`, `size`, `entity` and `field` | 2 s |
| PATCH | `/api/recovery/source-data/v1/admin/data-dictionary/fields/{fieldCode}` | P1 rwb-source-data | AC5, AC7, AC10 and AC11: the versioned change with its reason and the If-Match version, and its refusals | 2 s |
| GET | `/api/recovery/source-data/v1/admin/data-contracts` | P1 rwb-source-data | AC6 and AC8: the contract with its status, version, field count and confirmation | 2 s |
| PATCH | `/api/recovery/source-data/v1/admin/data-contracts/{contractId}` | P1 rwb-source-data | AC6: the recorded confirmation as role, date and document reference | 2 s |
| POST | `/api/recovery/source-data/v1/admin/data-contracts/{contractId}/publish` | P1 rwb-source-data | AC6 and AC8: the publish of DC-ACE, the refusal of DC-ACE-2 and the new DRAFT version | 2 s |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | AC3: the ACE value `days_past_due` 95 for `ACC0000017`, read through the owner instead of a view (ASM-0533) | 2 s |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | AC1 and AC3: the business-date freshness of DP01 and DP06 that tells the suite which read is in force | 2 s |
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | AC4 and AC9: the submission of the dictionary load with table `sys_fields` (ASM-0531) | 2 s + load time |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | P3 rwb-case | AC9: the approval that releases the rows to P1 (ASM-0531) | 2 s |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/verify` | P3 rwb-case | AC9: the verification of the applied rows (ASM-0531) | 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | AC1 and AC4: the list a field's `listCode` names, read as reference data instead of a table (DP-07) | 2 s |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | AC10 and AC11: the caller's rights, which prove that RW-TRIBE holds Reference data R only (ASM-0536) | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the suite calls no service through another service, and every call reaches the service through the gateway-bff route of AC10 (ASM-0536). The P3 contract also offers `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback`, and P4 offers `POST /api/recovery/access/v1/authorise`; no criterion of this story calls either, so they are named here as contract surface and are not counted among the twelve calls. The suite drives no P1 reference-load operation, because the reference load belongs to P3 (ASM-0531).

#### 12.3 Events published

None. The suite publishes no business event; it observes no event of the owning services in this story, because a dictionary read, a field change and a contract publish are synchronous calls on the contracts of section 12.2.

#### 12.4 Events consumed

None. No criterion of this story is asserted on a Kafka topic, so the suite consumes no event and configures no consumer group. The events of the owning services - `AceDataReady` and `AceDataLate` on `rwb.source-data.events.v1` (Arch v5 slide 15) - are the P1 behaviour of RWB-P1-E1064-APP and are out of scope here.

#### 12.5 Workflows and activities

None. No Temporal workflow or activity belongs to this story. The load is a synchronous submission, approval and verification on the P3 contract, and P1 applies the approved rows in its own transaction; the suite starts no workflow and observes none.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story. The governance load is submitted by a role and not on a cadence, and the view conformance test CHK-01 runs in the build pipeline rather than on a Temporal Schedule (ASM-0535).

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). `sys_objects`, `sys_fields`, `sys_field_version`, `data_product` and `data_contract` are owned by P1 rwb-source-data in `rwb_source_data` and are read only through the operations of section 12.2; the reference load is written through the P3 contract; the 30 `recovery.v_ace_*` views are read by P1 alone (Arch v5 slide 29). No `sys_fields`, `sys_field_version`, `data_contract`, `data_product` or reference-load table is read by the suite.

#### 12.8 Contract fakes

None for a service contract. The only fakes are outside the nineteen services:

| Stub | Purpose |
|---|---|
| ACE source stub of `public.account` and `public.collateral_detail` | Stands in for the ACE tables behind the 30 views: `public.account` holds `ACC0000017` with `delay_days` 95 for AC3, and `public.collateral_detail` holds the `insurance_expiry` control that exposes the column for the accepted load and withholds it for the refusal of AC4 and AC13. Only P1 reads it; the suite exercises it through P1's contracts and never queries a view |
| W1J01 synthetic fixture set | The dictionary fixture, the ACE column fixture with `v_ace_collateral_detail` at 11 fields, the contract fixture, and the synthetic users and account numbers of the run |
| Clock control | Places the confirmation on 2026-11-12 and the field change on 2026-11-18, and moves the business date the freshness read reports |

The suite builds against version v1 of the data dictionary contract, `openapi/rwb-source-data-v1.yaml` (OpenAPI 3.1, `/v1` in the path), published by RWB-P1-E1064-CON. ACE data in criteria and test data is set up in the ACE source stub or the W1J01 fixture set and is read only through the rwb-source-data contract, never from a view or an extension table.

P1 rwb-source-data, P3 rwb-case and P4 rwb-access are the real SIT services on their published contracts and are not faked in the normal path; a run configured with a fake for any of them fails the preflight (X11). The synthetic identities of the run come from the harness RWB-ITG-W1J01-ITG, not from a mock of rwb-access.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 12 | The seven P1 dictionary, contract, data-product and freshness reads and changes, the four P3 reference-load and list calls and the one P4 session read; one hop through gateway-bff, 2 s (DP-11, DP-13, DP-19) |
| Kafka | None | None | No event in this story |
| Temporal | None | None | No workflow and no Schedule in this story |
| File | None | None | The load file is read by P3, not by the suite; no file in this story |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a load driver over the P3 reference-load contract, a dictionary probe, a contract probe, a change probe, a value probe over the P1 data-product records, a gate probe over CHK-01 and the migration file hashes, an access probe over the P4 session, a privacy scan and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts of P1, P3 and P4, the run order, the report and the exit code |
| LoadDriver | Test harness | Submits, approves and verifies the `sys_fields` load on the P3 contract and records the load ID and its outcome (ASM-0531) |
| DictionaryProbe | Test harness | Reads the counts, the completeness of the seven attributes, the 297 of 304 ACE column names, the 7 derived fields, the 49 extension fields and one row per view column |
| ChangeProbe | Test harness | The versioned change with a reason and If-Match, the empty reason, the stale version and the missing If-Match |
| ContractProbe | Test harness | Records the confirmation, publishes DC-ACE, refuses DC-ACE-2 and asserts the new DRAFT version on a field change |
| ValueProbe | Test harness | Reads `days_past_due` 95 for `ACC0000017` through the P1 data-product record read (ASM-0533) |
| GateProbe | Test harness | Asserts the CHK-01 result of the next pipeline run and that every applied migration file hash is unchanged (ASM-0535) |
| AccessProbe | Test harness | Reads the session through P4, asserts the rights of each synthetic user and the 403 with MSG-P4-002 (ASM-0536) |
| PrivacyScan | Test harness | Scans every response and log of the dictionary, the contracts and the load for any personal pattern |
| ReportWriter | Test harness | One row per test case with the evidence and the elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table, no schema object and no migration; the only rows it causes are written by P1 on the P3 load and on the P1 operations, with synthetic values. The schemas it touches are owned elsewhere: `rwb_source_data` by P1 and `rwb_case` by P3.

**Configuration and reference data**

- The SIT endpoints of P1, P3 and P4, the gateway-bff address, the 2 s client budget and the poll interval, all as configuration.
- The counts and identifiers the criteria assert - 122 objects, 1,366 fields, 92 tables, 1,062 table fields, 49 extension fields, 30 views, 304 view fields, 177 and 127, 297 of 304, the 7 derived fields, `ACC0000017`, 95, `DF-ACE-018`, `DF-ACE-204`, `DF-ACE-020`, `DC-ACE`, `DC-ACE-2`, `V0002`, `V0003`, 2026-11-12, 2026-11-18 and `DOC-SYN-0640` - read through the P1 contract and the W1J01 fixture set and never written in the suite code (BR16).
- The confirming role "ACE team lead", the role of RW-DATASTEW, RW-REFADM, RW-TRIBE and RW-COE, and the Reference data right each holds (ASM-0534, ASM-0536).
- The rules of the view conformance test CHK-01 and the expected migration file hashes (ASM-0535).

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

Where each pattern sits in this story:

- **DP-01** sits on the whole suite: the five metadata tables are P1's tables in `rwb_source_data` and the reference-load tables are P3's in `rwb_case`, and the suite holds no schema client for either and reads no `sys_fields` row directly.
- **DP-05** sits on every view field of the dictionary: the 304 `v_ace_*` fields are described by P1 and the ACE value of `days_past_due` is asserted through P1's data-product record read, because only P1 reads the 30 views (Arch v5 slide 29; ASM-0533).
- **DP-07** sits on the load and on the list read: the reference-load path is P3 rwb-case (ASM-0531), a published-contract precondition of wave 1 rather than a build dependency of this suite, and the list a field's `listCode` names is read through the rwb-case reference-data read, whose path is Not specified in the source documents (GAP-0498), on one hop with the 2 s client budget; no list is written as a constant in code.
- **DP-11** sits on every call of section 12.2: the dictionary, the contract, the load and the session are each one hop on the owner's published contract with the 2 s client budget.
- **DP-13** sits on every base: `/api/recovery/source-data/v1`, `/api/recovery/case/v1` and `/api/recovery/access/v1`, and the legacy `/api/recovery/v1` base appears in no call of the suite.
- **DP-15** sits on the migration gate: V0001 owns the five tables in P1's own Flyway sequence, the ACE view change of RWB-ACE-001 is made by the ACE team, and the suite asserts the file hashes and the CHK-01 result instead of editing a migration (ASM-0535).
- **DP-19** sits on the read path: the dictionary and contract reads pass through gateway-bff on the composite route with the session cookie, one hop and a 2 s timeout, with no screen in this story (ASM-0536).

The H and C dependencies of these rows stay with the service, platform and operations stories that own them: this suite carries none of its own, and an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7). The I list names the two builds whose behaviour the run exercises.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Dictionary fixture | A seeded dictionary of 122 objects and 1,366 fields that reports the counts, the seven attributes, the 297 of 304 ACE column names and the 7 derived fields; one view column that can be left without a row for the CHK-01 failure | AC1, AC2, AC12, AC13 |
| ACE column fixture | `v_ace_collateral_detail` at 11 fields with no row for `insurance_expiry`, and the control that adds and withholds `public.collateral_detail.insurance_expiry` behind the ACE source stub | AC4, AC9, AC13 |
| Contract fixture | `DC-ACE` as DRAFT with 304 fields and the read interfaces `V0002` and `V0003`, the confirmation as role, date and document reference, and `DC-ACE-2` with no confirmation | AC6, AC8 |
| Identity set | The synthetic users RW-DATASTEW, RW-REFADM, RW-TRIBE and RW-COE with their session grants, and the confirming role "ACE team lead" | AC5 to AC8, AC10, AC11 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P1, P3 and P4 through gateway-bff, with the contract preflight that fails on any drift and refuses a fake for P1, P3 or P4.
2. Build DictionaryProbe over the P1 field read: the counts, the seven attributes, `page` and `size`, the entity and field reads, the extension fields and the row per view column (AC1, AC2).
3. Build ValueProbe over `GET /data-products/{productCode}/records` and the freshness read, so the ACE value and the business date in force are read through P1 and never through a view (AC3).
4. Build LoadDriver over the P3 reference-load contract: submit, approve and verify, with the accepted row, the wrong ACE column and the derived-field row (AC4, AC9, AC13).
5. Build GateProbe: the CHK-01 result of the next pipeline run and the migration file hashes, so a missing row or an edited migration fails the run (AC4, AC9).
6. Build ChangeProbe: the reasoned change on 2026-11-18, the empty reason, the stale version and the missing If-Match, each asserted with its status and message ID (AC5, AC7).
7. Build ContractProbe: the confirmation, the publish, the refusal of DC-ACE-2 and the new DRAFT version on a field change (AC6, AC8).
8. Build AccessProbe: the session read for each synthetic user, the successful PATCH as RW-DATASTEW and the 403 with MSG-P4-002 as RW-TRIBE (AC10, AC11).
9. Build PrivacyScan over the responses and logs of the dictionary, the contracts and the load, and assert that the confirmation names a role (AC12).
10. Build ReportWriter, the cleanup of the load, the fixture rows, the two business dates and the extra contract version, and the evidence report; run the whole suite twice to prove that a repeated run adds no second field version and no second contract version.

**Done when.** The 18 test cases of section 16 pass on the real services in SIT, all 30 views have dictionary rows in SIT, DC-ACE is PUBLISHED at version 1 with its 304 fields and the confirmation, the log scan finds no personal data, the synthetic set and the fixture rows are cleaned up, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-021 | Publish of a contract with no confirmation | The data contract for {system} cannot be published until its system owner confirms it. |
| MSG-GEN-001 | Reason or confirmation field empty | Enter {field}. |
| MSG-GEN-004 | Change from an old version, or no If-Match version | Someone else changed this record. Reload it to see their change. |
| MSG-P1-002 | Dictionary load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | The store or a view is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without Reference data U | You cannot {action} here. Your role does not include it. |

The text of MSG-P1-021 is copied from Error and Message Standard v4, the other five texts are copied unchanged from RWB-E1-064, and this story adds no message ID. Thai text for each message follows decision DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 confirmed). In AC4 and AC13 the {source} value is "dictionary" and the {check} value names the first failing row, in AC5 the {field} value is "reason", in AC6 the {system} value is "ACE" and in AC11 the {action} value is "change this field".

### 15. Screens and states

No screen in this story. Developers, analysts and data stewards read the dictionary through `GET /api/recovery/source-data/v1/admin/data-dictionary/fields` and the contracts through `GET /api/recovery/source-data/v1/admin/data-contracts`, both through gateway-bff on the composite route with the session cookie (ASM-0536). The states the run reads through those operations are: a field page with the object and field counts and an empty filter result for an entity with no field, a field with its version history and its late behaviour, a contract as DRAFT then PUBLISHED with its confirmation, and a published contract with a second version as DRAFT. SCR-40 Reference data shows the versioned tables from Epic 8 and is out of scope, and its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-397); until then the dictionary changes go by the reference load or by the endpoints.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-064-01-ITG | AC1, BR1, BR2 | Integration | The seeded 122 objects and 1,366 fields; `page=1&size=1`; the 92 tables, the 1,062 fields, the 49 extension fields, the 30 views and the 304 fields, 177 and 127; the 297 of 304 and the 7 derived fields; end to end on the real services |
| TC-E1-064-02-ITG | AC2, BR2 | Integration | 30 views with 304 fields; one `sys_objects` row and one `sys_fields` row per column; `DF-EXT-001` to `DF-EXT-049`; end to end on the real services |
| TC-E1-064-03-ITG | AC3, BR1, BR3 | Integration | `ACC0000017` with `delay_days` 95; `DF-ACE-018`, `NUMBER`, integer, `public.account.delay_days`, `DP01`, `DAILY`, `RW-DATASTEW` and the late behaviour; the 95 read through the P1 data-product records; end to end on the real services |
| TC-E1-064-04-ITG | AC4, BR6, BR9 | Integration | The dictionary fixture without `DF-ACE-204`; `v_ace_collateral_detail` at 11 fields; the load with `public.collateral_detail.insurance_expiry` and with `public.collateral_detail.insurance_date`; CHK-01 and the migration hashes; end to end on the real services |
| TC-E1-064-05-ITG | AC5, BR5 | Integration | `DF-ACE-018` version 1 to version 2 on 2026-11-18 with the reason "add the daily stale alert for DP01"; version 1 readable; the empty reason refused 422; end to end on the real services |
| TC-E1-064-06-ITG | AC6, BR4 | Contract | `DC-ACE` with 304 fields; the confirmation on 2026-11-12 as "ACE team lead" with `DOC-SYN-0640`; `DC-ACE-2` with no confirmation; end to end on the real services |
| TC-E1-064-07-ITG | AC7 | Integration | Two changes to `DF-ACE-020` from version 1; one change with no If-Match; end to end on the real services |
| TC-E1-064-08-ITG | AC8, BR7 | Integration | Published `DC-ACE` at version 1 and a change to `DF-ACE-018`; version 2 created as DRAFT; end to end on the real services |
| TC-E1-064-09-ITG | AC11, BR14 | Integration | RW-TRIBE holds Reference data R only, proved through the P4 session read; the PATCH of `DF-ACE-018` refused 403 with MSG-P4-002; end to end on the real services |
| TC-ITG-E1064-ITG-10 | AC9, BR10 | End to end | The load submitted, approved and verified on P3 and applied by P1; the result read through the P1 dictionary; no P1 reference-load call and no `sys_fields` read; end to end on the real services |
| TC-ITG-E1064-ITG-11 | AC10, BR13 | Contract | The dictionary and contract reads through gateway-bff with the session cookie, one hop and 2 s; the P4 session read; the PATCH with If-Match as RW-DATASTEW |
| TC-ITG-E1064-ITG-12 | AC12, BR15 | NFR | The scan of every response and log of the dictionary, the contracts and the load for national ID number, phone number, name and account number patterns; the confirmation names a role |
| TC-ITG-E1064-ITG-13 | AC13, BR1 | Contract | The 7 derived view fields with source system ACE and no single ACE column; a load naming a single ACE column refused in full with MSG-P1-002 |
| TC-ITG-E1064-ITG-14 | AC14 | Contract | A run configured with a fake for P1, P3 or P4; the preflight refuses it before any step; the ACE source stub, the W1J01 fixture set and the clock are the only stubs |
| TC-ITG-E1064-ITG-15 | AC15, BR11, BR12 | Contract | A scan of the suite for a client to rwb_source_data, rwb_case or rwb_access and for a read of a recovery.v_ace_* view; the scan finds none; days_past_due read through the P1 data-product records |
| TC-ITG-E1064-ITG-16 | AC16, BR8, BR17 | Contract | The migration file hashes of P1 and P3 compared before and after the run; no DDL and no migration file added or edited by this story |
| TC-ITG-E1064-ITG-17 | AC17, BR16, BR18 | NFR | A scan of the suite code for a business value written as a constant; a run against an environment other than SIT is refused at start |
| TC-ITG-E1064-ITG-18 | AC18, BR13 | Integration | A consumed call that fails or gets no answer within the 2 s client budget; the run stops at that step; no fake is put in its place; end to end on the real services |

TC-E1-064-01-ITG to TC-E1-064-09-ITG are the copies of the legacy test cases of RWB-E1-064, kept with their legacy IDs and given the `-ITG` suffix; the legacy access test TC-E1-064-09 is the copy behind AC11 and keeps that position. TC-ITG-E1064-ITG-10 to -13 are new (D-RCV-60): 10 carries the P3-to-P1 load path of AC9, 11 the gateway-bff route and the right check of AC10, 12 the personal-data scan of AC12 and 13 the derived-field rule of AC13. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, the load path is End to end, the route and the derived-field rule are Contract, and the personal-data scan is NFR. TC-ITG-E1064-ITG-14 to -17 are new (D-RCV-60): 14 carries the fake refusal of AC14, 15 the client and view-read scan of AC15, 16 the no-DDL check of AC16 and 17 the no-constant and SIT-pin check of AC17. TC-ITG-E1064-ITG-18 is new (D-RCV-60) and carries the failed-call stop of AC18.

### 17. Guardrails

- No business value in code or in the suite: the counts, the owners, the refresh cycles, the late behaviours, the contract codes and the interfaces are approved data rows, read through the P1 contract at run time (BR16).
- No personal data in logs, events, fixtures, prompts or the report: the dictionary holds definitions, not values, and the confirmation names a role, not a person (BR15). Every national ID number, phone number, name and account number of the run is synthetic and the scan proves their absence.
- No cross-service table read and no schema client in the suite: every fact is read through a contract of section 12.2, and a pipeline scan fails any change that adds a schema connection or a view query (DP-01, DP-05).
- Only the public ACE column names recorded in the dictionary appear in the story; no recovery class reads an ACE table directly, and only P1 holds SELECT on the 30 views (Arch v5 slide 29).
- A published contract is never edited in place; a change makes a new version, and the published version stays in force (BR7).
- No DDL and no migration of this story: V0001 owns the five tables, an applied migration is never edited, and CHK-01 remains the merge gate (BR9, ASM-0535).
- One hop and a 2 s client budget on every REST call through gateway-bff; the suite calls no service through another service and no service through a direct connection (ADR-020, DP-11, DP-19).
- No production access and no production namespace: the run is pinned to SIT with the synthetic set, and it refuses to start against any other environment.
- Clean-up in the same run: the load, the fixture rows, the two business dates and the extra contract version are removed or retired, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner, every field typed, sourced and owned | The P1 dictionary read, the P1 data-product record read and the freshness read, the P3 load, the 122 objects and 1,366 fields of V0001 | TC-E1-064-01-ITG, TC-E1-064-02-ITG, TC-E1-064-03-ITG, TC-E1-064-06-ITG, TC-E1-064-09-ITG, TC-ITG-E1064-ITG-10 |
| REQ-RDF-011 | Catalog entry per data product with definition, owner, system of record and refresh, changed by a governed load and a version | The P3 reference-load contract, the P1 field and contract operations, `sys_field_version`, the CHK-01 gate, MSG-P1-002 and MSG-P1-021 | TC-E1-064-04-ITG, TC-E1-064-05-ITG, TC-E1-064-07-ITG, TC-E1-064-08-ITG, TC-ITG-E1064-ITG-10, TC-ITG-E1064-ITG-13 |
| DP-01 | Owner's schema per service; never read another service's tables | `rwb_source_data` behind the P1 contract, `rwb_case` behind the P3 load, no schema client in the suite, no `sys_fields` read | TC-E1-064-01-ITG, TC-E1-064-02-ITG, TC-ITG-E1064-ITG-10 |
| DP-05 | ACE views read through rwb-source-data's contract | The 304 view fields and `days_past_due` 95 read through the P1 dictionary and data-product contracts, in place of a `recovery.v_ace_*` query | TC-E1-064-01-ITG, TC-E1-064-03-ITG, TC-ITG-E1064-ITG-13 |
| DP-07 | Reference-data contract of rwb-case | The P3 reference-load submit, approve and verify operations and the list read; a wave-1 published-contract precondition, not an I dependency | TC-E1-064-04-ITG, TC-ITG-E1064-ITG-10 |
| DP-11 | One hop and a 2 s timeout | The twelve calls of 12.2 and the preflight contract test | TC-ITG-E1064-ITG-11 |
| DP-13 | `/api/recovery/<short>/v1` | `/api/recovery/source-data/v1`, `/api/recovery/case/v1` and `/api/recovery/access/v1` | Every test case, at the preflight |
| DP-15 | Per-service Flyway and migration ownership | V0001 in P1's own sequence; no migration of this story; the migration file hashes and CHK-01 | TC-E1-064-04-ITG, TC-ITG-E1064-ITG-10 |
| DP-19 | Screen route through gateway-bff | The composite route `/api/recovery/source-data/v1/**` with the session cookie and the 2 s budget, with no screen in this story | TC-ITG-E1064-ITG-11 |
| ASM-0531 | The load is submitted, approved and verified on P3 rwb-case and applied by P1, which publishes no reference-load operation of its own | The P3 reference-load operations of 12.2 and the P1 apply path | TC-E1-064-04-ITG, TC-ITG-E1064-ITG-10 |
| ASM-0532 | The dictionary and contract reads and changes stay with P1 rwb-source-data under `/api/recovery/source-data/v1` | The five P1 dictionary and contract operations of 12.2 | TC-E1-064-01-ITG, TC-E1-064-05-ITG, TC-E1-064-06-ITG |
| ASM-0533 | `days_past_due` is asserted through the P1 data-product record read, and only P1 reads the 30 views | `GET /data-products/{productCode}/records` and the 297 of 304 and 7 derived-field rules | TC-E1-064-03-ITG, TC-E1-064-04-ITG, TC-ITG-E1064-ITG-13 |
| ASM-0534 | The confirmation is a role, a date and a stored document reference, and a publish without it is refused 409 with MSG-P1-021 | `PATCH /admin/data-contracts/{contractId}` and `POST /admin/data-contracts/{contractId}/publish` | TC-E1-064-06-ITG, TC-E1-064-08-ITG, TC-ITG-E1064-ITG-12 |
| ASM-0535 | CHK-01 stays the merge gate and no applied migration is edited | The gate probe, the migration file hashes and the next pipeline run | TC-E1-064-04-ITG, TC-ITG-E1064-ITG-10 |
| ASM-0536 | The dictionary and contract reads are served through gateway-bff on the composite route, one hop and 2 s, and the rights are read through the P4 session | The gateway-bff route, the session read and MSG-P4-002 | TC-E1-064-09-ITG, TC-ITG-E1064-ITG-11 |
| GAP-0373 | Reference-load owner, ACE view value read and confirmation form are not named for the target | Settled by ASM-0531 to -6 and asserted by the eight test cases above | TC-E1-064-03-ITG, TC-E1-064-04-ITG, TC-E1-064-06-ITG, TC-ITG-E1064-ITG-10, TC-ITG-E1064-ITG-11 |

### 19. Out of scope

- The application builds this run depends on: RWB-P1-E1064-APP and RWB-P4-E1064-APP.
- The contract, database, operations and infrastructure stories of the legacy key, and the P3 rwb-case reference-load story that publishes the load contract.
- The tables, the seed and the dictionary view: RWB-E1-001 and RWB-P1-E1001-APP.
- The 30 ACE views, their grants and the view conformance test: RWB-E1-069 and RWB-ITG-E1069-ITG. This story asserts the CHK-01 result and the migration hashes; it builds neither.
- The catalog endpoint, access by product and PDPA masking: RWB-E1-016.
- Freshness stamps per data product: RWB-E1-015; this story reads the freshness of DP01 and DP06 only to know which business date is in force.
- Retention per product and table: RWB-E1-017.
- The reference data screen SCR-40 and its states: Epic 8.
- Contracts for stage 2 data products: RWB-E2-010.
- The build of the harness RWB-ITG-W1J01-ITG, of the ACE source stub and of the gateway-bff route, and the non-functional epic RWB-ITG-NFR.
