# RWB-P1-E1001-APP Recovery tables for the 14 data products

### Version 3 changes

- RD-P1-021 and RD-P1-025 align the baseline dictionary counts, add `data_product_source`, correct the data-product seed values, and define the personal-field check (review findings #1, #2, #3, #10, #14, #16, #17, #21, #22).
- RD-P1-024 removes the case-list table and workflow from P1 while retaining its dictionary rows as retired (review findings #4, #9, #15).
- RD-P1-001, RD-P1-003, RD-P1-008 and RD-P1-020 align repeat-load, event and reference-load authority behavior (review findings #6, #8, #11, #16, #20).
- RD-P1-020 and RD-P1-045: version history stays in rwb-case, the handler updates `data_product` in place, a repeat changes nothing and flag-off behaviour is stated; the four platform library tables are applied by this story's migration (review findings #5, #6, #7, #16, #19, #23; AC1, AC10, AC20 to AC24).
- Still pending: the apply-handler transport (NEW-GAP-F12-1), the approver role for this load (NEW-GAP-S1-1), the column that records the applied version (NEW-GAP-S1-2), the L3 and module links (NEW-GAP-S1-3) and the field declaration format (GAP-2537).
- Finishing pass (RD-P1-068; requests W4-data-0038 and W3-messages-0032): the Test Cases v9 IDs are cited; the `data_product` key follows Physical Schema v9; the later-migration dictionary rows, the 12 seeded source rows and the library `decision_record` table are stated; messages cite Error and Message Standard v6.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Schema and login | rwb_source_data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-001 |
| Legacy disposition | Must change |
| Build status | In build |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP11, DP14, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E1001-APP-16); the squad sizes the story at refinement |
| Depends on (build) | RWB-PLT-NF06-DB, RWB-PLT-TE006-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Service baseline (preconditions) | The six platform CON contracts RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-E1047-CON and RWB-PLT-N001-CON, with RWB-PLT-NF06-DB, are the service baseline; build against them and their fakes. The metadata row stays None and Ready to start stays Day 1 |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Contract version | rwb-case.yaml 5.1.0 (API Specification v7), which holds `/admin/reference-loads` under `/api/recovery/case/v1`; this story adds nothing to rwb-source-data.yaml |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v3.md (FR-P1-001, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-029, FR-P1-031) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-008, RD-P1-020, RD-P1-021, RD-P1-024, RD-P1-025, RD-P1-045, RD-P1-068 |
| Status | Draft (P1 developer readiness) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-001 is realigned into rwb-source-data. The built migration `V0001__rwb_e1_001_recovery_schema.sql` and the 92-table estate with its dictionary are kept as built; this story carries P1's share of that estate into the service's own schema `rwb_source_data` (DP-01, DP-15), keeps the one data product catalog and the one data dictionary that describe all 14 data products, seeds the 49 extension-table dictionary fields, and leaves the four extension tables to RWB-P1-E1069-DB, the 30 views and their grants to RWB-P1-E1069-APP and RWB-P1-E1069-DB, freshness to RWB-P1-E1015-APP and the dictionary endpoint to RWB-P1-E1064-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P1-E1001-APP-L241, X20 RWB-P1-E1001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (35 resolved, 59 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applies RD-P1-001, RD-P1-003, RD-P1-008, RD-P1-020, RD-P1-021, RD-P1-024 and RD-P1-025; resolves confirmed P1 review findings where ruled and records pending items below. Agent: S1-stories.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the 14 data product rows, product-to-source map and the P1 dictionary for the 93-table and 30-view baseline in rwb_source_data**, so that **each data product has one named owner and consumers read the P1 data through its published contracts**.

The legacy story built the estate as one schema. D-RCV-60 keeps the behaviour and moves the ownership:

- **Kept as built:** migration `V0001__rwb_e1_001_recovery_schema.sql` remains the as-built regression baseline. This story does not rewrite it (Template and Rules R6, "Must change"; U2).
- **The new work is the schema split:** every service now writes its own schema `rwb_<name>` with its own login and its own Flyway sequence, forward only (DP-01, DP-02, DP-15; Arch v5 slides 29, 41 and 45). P1's share lands in `rwb_source_data`; the tables of the other services land with their owners' DB stories. No service reads another service's tables (DP-01); a call goes to the owner's contract, one hop, 2 s timeout (DP-11).
- **One catalog, one dictionary, one home:** `data_product` holds 14 rows; `sys_objects` and `sys_fields` carry the 123-object / 1,379-field Physical Schema v8 baseline plus `data_product_source` and its three fields (at least 124 objects / 1,382 fields; RD-P1-021, RD-P1-025). The view `v_data_dictionary` stays in `rwb_source_data`.
- **The four extension tables are P1's but are not created here.** `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` live in `rwb_source_data` and are delivered by the sibling DB story **RWB-P1-E1069-DB**, the DB and grant slice of RWB-E1-069. This story seeds and keeps their 49 dictionary fields (DF-EXT-001 to DF-EXT-049) and creates none of the four tables.
- **The other 74 service tables do not land in this schema.** P1 owns 17 target tables: 13 P1 application tables created by this story and four extension tables created by RWB-P1-E1069-DB. `case_list_row` and `lake_copy_watermark` have no target; their dictionary rows remain marked retired (RD-P1-021, RD-P1-024, RD-P1-025).
- **Bases and names:** REST base `/api/recovery/source-data/v1`, login and schema `rwb_source_data`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-02, DP-13, DP-14; Arch v5 slides 29 and 41). This story adds no REST operation and publishes no business event of its own; section 12 identifies its shared library write.
- **Screens:** through the gateway-bff composite route (DP-19). No screen is in this story.

### 2. Business rationale

The Workbench holds no copy of source data. ACE ingests ALS, SCBPDM, EFS, COLLINS, CCMS, SVAF, AMIS, RPS, LIT, WIN, GL, NLEADS, EasyApp and Entra ID, and the Workbench reads what it needs through the 30 `recovery.v_ace_*` views (D-RCV-35 U1 and U4, ADR-010). The current dictionary baseline describes 89 Workbench tables, four extension tables and 30 ACE source views, plus the catalog and metadata registry. Each data product has one named owner and a system-of-record value that follows the forms in BR3 (REQ-RDF-001, RD-P1-025). The measure it serves is "the ACE batch is complete when the Workbench reads it on 99 percent of days", because the dictionary and catalog resolve later reads and freshness stamps.

**What D-RCV-60 changes.** Not the rationale, and not the estate: the built migration is the as-built baseline and stays as built. What changes is the ownership boundary inside the same ACE database. The estate was held in one schema; it is now split across 19 `rwb_*` schemas, one per service, each with its own login, its own Flyway sequence and its own grants, and each checked by a boundary test that fails the build on a cross-schema reference (DP-01, DP-02, DP-15; Arch v5 slides 29, 41 and 45). This story is P1's share of that move: the 14 data products, the dictionary that describes them and the tables P1 writes.

**Why the catalog and the dictionary stay with P1.** They are the one place where a number, a field or a freshness stamp is resolved to a data product and an owner (REQ-RDF-001, REQ-RDF-011). Split across 19 schemas they would answer 19 ways, and every other service reading them would be a cross-schema read the boundary rule forbids. Held in `rwb_source_data` they stay one catalog and one dictionary, reachable by contract and by the dictionary read model, with no second copy anywhere.

**Why the extension tables arrive with a separate story.** The four extension tables are P1 data, but their DDL, keys, indexes and grants belong to RWB-P1-E1069-DB. This story seeds their dictionary rows and creates none of them; the conformance test defers their physical comparison until those tables exist.

**What the split does not change.** The Workbench still holds no copy of source data; P1 still reads ACE only through the 30 `recovery.v_ace_*` views (DP-05, ADR-010); and P1 now additionally holds no grant on any other `rwb_*` schema and creates no constraint that points at one.

### 3. Preconditions

- RWB-PLT-E1044-CON is in place: Flyway runs in the rwb-source-data pipeline and takes the schema name of the service's own schema from configuration. The legacy parameter `recoverySchema = recovery` and the built `V0001__rwb_e1_001_recovery_schema.sql` are the as-built baseline and are not re-opened.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON define the reference-load process: rwb-case verifies and approves a version and then calls the apply handler of rwb-source-data (RD-P1-020). Pending: the transport, request and response of that call and the table code of this load, owner solution architect with the rwb-case service owner, tracked as NEW-GAP-F12-1.
- RWB-PLT-TE006-CON is published: the DDL template of the four platform library tables `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key`, which this story's migration applies in `rwb_source_data` (DP-09, GAP-0109, ASM-2473).
- The DEV and SIT databases of the ACE service exist, the schema `rwb_source_data` exists with its login, and the pipeline service identity may run migrations in that schema only (DP-02, DP-15).
- P3 reference-load roles and authorization are enforced by rwb-case. A reader of the dictionary read model has read access in DEV or SIT.
- The 14-product reference version is prepared from section 13 with a synthetic owner user ID for each product in DEV and SIT.
- RWB-PLT-E1027-CON (the local decision-record library), RWB-PLT-E1047-CON (topic naming) and RWB-PLT-N001-CON (the gateway-bff composite route) are in place.
- The four extension tables are delivered by RWB-P1-E1069-DB in the same schema; this story creates none and defers their physical comparison until their migration (AC1, AC5).
- The 30 `recovery.v_ace_*` views are not created here. RWB-P1-E1069-APP and RWB-P1-E1069-DB own the view migrations and grants (DP-05); the conformance test defers their physical comparison until the views exist.

### 4. Flow

1. Pipeline: runs this story's Flyway migration in DEV on the rwb-source-data sequence after the service baseline (DP-15).
2. Migration: creates the 13 P1 application tables in section 11, their indexes, `v_data_dictionary` and the append-only trigger on `interaction`; it applies the RWB-PLT-TE006-CON DDL template for `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` without redefining them, and creates none of the four extension tables.
3. Migration: inserts the 14 `data_product` seed rows, the 123 baseline `sys_objects` rows and 1,379 baseline `sys_fields` rows from Physical Schema v8, then adds `data_product_source` with DF-REF-300 to DF-REF-302; the final baseline is at least 124 objects and 1,382 fields.
4. Migration: marks `case_list_row` and `lake_copy_watermark` dictionary records retired; it creates neither table. It creates `fk_sys_objects_data_product` inside `rwb_source_data`.
5. Migration: seeds `data_product_source` from the source mapping in RD-P1-021. The source-system codes for the core bank remain Pending under NEW-ASM-B3.
6. Pipeline: runs dictionary conformance for tables and views present in `rwb_source_data`, ignoring the seven standard columns; it fails on an unmatched field or different physical type for an existing object. Extension fields and ACE view fields are deferred until their owning migrations create the tables or views; retired dictionary rows are excluded.
7. Pipeline: repeats the migration and conformance stages in SIT.
8. Reference-load process: rwb-case owns submission, verification, approval and reference-version state. After approval it calls the P1 apply handler for the `data_product` version; the transport, request, response and table code are Pending under NEW-GAP-F12-1.
9. P1 handler: checks the 14 product codes, system-of-record grammar, owner role, owner user ID and refresh cycle without writing data during validation.
10. P1 handler: applies the approved version in one transaction in `rwb_source_data`: it updates the 14 `data_product` rows in place, sets `valid_from` to the version's valid-from date and writes the local DecisionRecorded record through the PLT library in the same transaction. It is idempotent on (table code, version). Pending: the column that records the applied version number on `data_product`, owner data architect, tracked as NEW-GAP-S1-2.
11. Developer or data steward: queries `v_data_dictionary` for entity `v_ace_account` and field `days_past_due`.
12. System: returns DF-ACE-018, data type NUMBER, physical type integer, source system ACE, source field `public.account.delay_days`, product DP01, system of record `ACE (ingested from ALS)`, refresh cycle DAILY and the DP01 owner.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A statement in the split migration fails | The transaction rolls back; no table of that migration remains in `rwb_source_data`; the pipeline stage names the failing statement | None (pipeline log) | AC4 |
| X2 | A physical column has no dictionary row, or an active dictionary row has no column or has another physical type | The conformance test fails and names the schema, table, column and field ID | None (pipeline log) | AC5 |
| X3 | The migration runs again after it is applied | Flyway skips it; no table, dictionary row or seed value changes | None | AC6 |
| X4 | A catalog value has no system of record, more than one, a bare source name, more than 200 characters, or no named owner | The P1 handler refuses the full version and returns every failed row; no P1 row changes | MSG-P1-003 | AC11, AC21 |
| X5 | The catalog version does not hold each of DP01 to DP14 once | The P1 handler refuses the full version; no P1 row changes | MSG-P1-004 | AC8, AC22 |
| X6 | A product code, owner role or refresh cycle is outside its list | The P1 handler refuses the full version; no P1 row changes | MSG-P1-007 | AC9, AC22 |
| X7 | The same table, valid from and content hash are loaded again, or an applied (table code, version) is delivered again | rwb-case answers 200 with the first load's body for the repeat load; the P1 handler changes no row and writes no outbox row for a re-delivered version (RD-P1-001, RD-P1-020) | None | AC10 |
| X8 | The rwb-case reference-load authorization refuses the caller, or the author tries to approve | rwb-case answers its published Problem response; the P1 handler is not called | MSG-P4-002 or MSG-P7-002 (rwb-case) | RWB-P3-E1043-CON AC4; AC20 |
| X9 | The flag `rwb.p1.data-catalog` is off | The handler applies nothing and rwb-case gets the unavailable answer of the handler contract (RD-P1-045 item 4); the answer shape is Pending under NEW-GAP-F12-1 | None | AC24 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the per-service Flyway sequence (RWB-PLT-E1044-CON), schema baseline (RWB-PLT-NF06-DB), and rwb-case reference-load contract (RWB-P3-E1043-CON) |
| Negotiable | Product names, definitions, owners and refresh cycles remain reference data; the table ownership and checks follow RD-P1-021 and RD-P1-025 |
| Valuable | Gives P1-owned data one schema, one catalog, one source map and one dictionary for the 14 products |
| Estimable | One migration, one read model, one conformance test and one reference-table handler; the call transport is tracked as NEW-GAP-F12-1 |
| Small | One migration, one read model, one conformance test and one handler; deferred extension and view comparisons run after their owning migrations |
| Testable | Each acceptance criterion below is an automated test; new and changed tests are listed for Test Cases v9 |

### 7. Acceptance criteria

```gherkin
Feature: Recovery tables for the 14 data products

  Scenario: AC1 Baseline schema and dictionary are deployed
    Given the schema rwb_source_data of RWB-PLT-NF06-DB exists and holds no table
    When this story's Flyway migration runs in DEV and then SIT
    Then the schema holds the 13 P1 application tables listed as created in section 11, including data_product_source, plus outbox_event, outbox_delivery, processed_event and idempotency_key from the library DDL template, plus the decision_record table of the RWB-PLT-E1027-CON library migration, and no table of another service
    Then data_product holds 14 rows, DP01 to DP14, with the values of section 13
    Then rwb_source_data contains no case_list_row or lake_copy_watermark table; the case_list_row object and field rows stay in sys_objects and sys_fields marked retired
    Then sys_objects contains at least 124 rows and sys_fields contains at least 1,382 rows, including the three fields DF-REF-300 to DF-REF-302 and the 304 ACE view fields
    Then party_ext, contact_point_ext, account_ext and valuation_ext are not created by this migration
    Then no constraint in rwb_source_data references public or another rwb_* schema
    Then account_key, person_key, asset_key, payment_code and contact_key remain varchar(255) business keys with no foreign key

  Scenario: AC4 Failed migration leaves no partial schema
    Given a copy of this migration in which the statement creating efs_ledger_outcome fails
    When the pipeline applies it in DEV
    Then the stage fails naming the statement, no table created by this migration remains in rwb_source_data and Flyway has no successful history row for this version

  Scenario: AC5 Column without a dictionary entry fails the build
    Given the migration is applied and a branch adds column efs_ledger_outcome.test_col without a sys_fields row
    When the dictionary conformance test runs
    Then it fails naming schema rwb_source_data, table efs_ledger_outcome and column test_col
    Then changing `data_product.system_of_record` to text fails with DF-REF-074, expected varchar(200), found text
    Then extension fields and the 304 ACE view fields are compared with columns only after the owning RWB-P1-E1069 migrations create them

  Scenario: AC6 Repeated migration has no effect
    Given this migration has already been applied in SIT
    When the pipeline runs it again in SIT
    Then Flyway reports the version as already applied and no table, dictionary row or catalog seed changes

  Scenario: AC8 Catalog missing a product is refused
    Given a proposed data_product version contains 13 rows and no row for DP09
    When the rwb-source-data handler checks the version
    Then the P1 handler refuses the full version with MSG-P1-004 "The catalog must hold the 14 data products DP01 to DP14. Missing: DP09." (answer shape Pending, NEW-GAP-F12-1)
    Then no data_product row, decision record or outbox row changes

  Scenario: AC9 Value outside a catalog list is refused
    Given the reference-data fake returns LOV-ROLE without DP_OWNER and the proposed version has DP_OWNER on DP04 and HOURLY on DP05
    When the rwb-source-data handler checks the version
    Then the P1 handler refuses the full version with MSG-P1-007 "Row 4: owner_role must be one of the role codes in LOV-ROLE." and "Row 5: refresh_cycle must be one of DAILY, WEEKLY, MONTHLY, ON_CHANGE." in row order (answer shape Pending, NEW-GAP-F12-1)
    Then no data_product row, decision record or outbox row changes

  Scenario: AC10 Applied version delivered again
    Given the data_product version with validFrom 2026-11-30 has been approved in the rwb-case fake and applied by the handler
    When the same table code and version are delivered to the handler again
    Then no data_product row changes, including its version and updated_at columns
    Then no second DecisionRecorded row is written to outbox_event
    Then MSG-P1-011 is not raised

  Scenario: AC11 Bare source name is refused
    Given the proposed data_product version has system_of_record CCMS on DP06
    When the rwb-source-data handler checks the version
    Then the P1 handler refuses the full version with MSG-P1-003 "DP06 must have exactly one system of record and one named owner." (answer shape Pending, NEW-GAP-F12-1)
    Then the current data_product version remains in force and no row is written

  Scenario: AC13 Personal fields are flagged in the dictionary
    Given the baseline migration is applied in DEV
    When the conformance test compares is_personal by Field ID with the Fields sheet of Data Classification v5
    Then the personal-field sets match in both directions for the baseline objects

  Scenario: AC14 Dictionary is seeded before the views exist
    Given the migration is applied before any recovery.v_ace_* view migration
    When the conformance test reads sys_objects and sys_fields
    Then the baseline counts are at least 124 objects and 1,382 fields, including 304 view-field dictionary rows deferred until their views exist
    Then case_list_row remains a retired dictionary entry with no physical table

  Scenario: AC15 Field declaration is checked through the Change Register
    Given the data architect has published the declaration format tracked by GAP-2537
    When a service field declaration is handed to the dictionary seed through the Change Register
    Then every declared field maps to a sys_fields row and every unmatched declaration fails the conformance test
    Then the declaring service neither writes rwb_source_data nor reads it at run time

  Scenario: AC16 Dictionary read model returns the seeded field
    Given the baseline migration is applied and DP01 has an owner user ID
    When v_data_dictionary is queried for entity v_ace_account and field days_past_due
    Then one row returns DF-ACE-018, NUMBER, integer, ACE, public.account.delay_days, DP01, DAILY and the DP01 owner

  Scenario: AC17 Catalog decision record is atomic
    Given the decision-record library fake fails to append DecisionRecorded
    When the data_product version is applied
    Then the transaction changes no data_product row and writes no outbox_event row

  Scenario: AC18 Interaction is append only
    Given one row exists in interaction
    When an UPDATE or DELETE targets that row
    Then the statement is rejected and the row remains unchanged

  Scenario: AC19 Service schema boundary is enforced
    Given the baseline migration is applied and login rwb_source_data is inspected
    When its grants, joins and constraints are checked
    Then it has no grant on another rwb_* schema and no constraint points outside rwb_source_data

  Scenario: AC20 A version that is not approved changes nothing
    Given a data_product version in status VALIDATED in the rwb-case fake whose author then tries to approve it and is refused with MSG-P7-002
    When data_product is read
    Then the 14 rows are unchanged, the handler has received no call and outbox_event has no new row

  Scenario: AC21 Missing owner and over-length system of record are both reported
    Given a version in which DP02 has no owner_user_id and DP07 has a system_of_record of 201 characters
    When the handler checks the version
    Then it refuses the full version with "DP02 must have exactly one system of record and one named owner." and "DP07 must have exactly one system of record and one named owner."
    Then no data_product row, decision record or outbox row changes

  Scenario: AC22 Duplicate or unknown product code is refused
    Given one version of 14 rows holds DP08 twice and no DP09, and another holds DP01 to DP14 plus a 15th row DP15
    When the handler checks each version
    Then the first is refused with MSG-P1-004 naming DP09 and the second with MSG-P1-007 for row 15 field product_code
    Then no data_product row changes

  Scenario: AC23 Two versions delivered at the same time never mix
    Given two approved data_product versions with different valid-from dates and different owner_user_id values on all 14 rows
    When both are delivered to the handler concurrently
    Then each is applied in its own transaction and the 14 rows afterwards all carry the owner_user_id and valid_from of the same one version

  Scenario: AC24 Handler is off
    Given the flag rwb.p1.data-catalog is off
    When an approved version is delivered
    Then no data_product row, decision record or outbox row changes and the caller gets the unavailable answer
```

**Pending coverage.** AC15 cannot run until the declaration format of GAP-2537 is published. The answer shape that AC8, AC9, AC11, AC21, AC22 and AC24 assert towards rwb-case is Pending under NEW-GAP-F12-1; the message IDs, texts and unchanged data are testable against the handler now. AC12 of version 2 (role without Reference data C) belongs to the rwb-case load operation and is not tested here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every table column and every view column in the recovery estate has exactly one row in the data dictionary, with its BR Field ID, types, source system and meaning | Logical Data Model and Data Dictionary; sys_fields |
| BR2 | Workbench data is held in the 14 data products DP01 to DP14 | REQ-RDF-001; sys_objects.data_product |
| BR3 | A system-of-record value matches `^ACE \(ingested from [^)]+\)$`, equals `Recovery Workbench`, is one sentence of at most 200 characters containing both `ACE (ingested from ` and `Recovery Workbench`, or starts `Recovery Workbench, with ` and contains `ACE`; each product has one named owner | REQ-RDF-001; D-RCV-35 U1; RD-P1-025 |
| BR4 | The catalog values are a versioned data load, changed without a code release; a load with an exception is refused in full | Principle 1; DT02; CTL-08 |
| BR5 | Where a product is fed by several sources (DP06, DP07, DP13), its one system of record names ACE and every source it ingests; a bare source name is refused because no source reaches the Workbench except through ACE | D-RCV-35; ADR-010 |
| BR6 | Schema names come from parameters; one migration per story; forward only in PROD | RWB-E1-044 |
| BR7 | Personal fields carry is_personal = true in the dictionary so masking (RWB-E1-016) can read them | sys_fields.is_personal; CTL-11 |
| BR8 | The recovery estate holds no copy of source data. No constraint references a table in schema public, and a link to an ACE record is a varchar(255) business key with no foreign key | D-RCV-35 U4; ADR-010; Data Tier Map section 1 |
| BR9 | The baseline migration seeds the dictionary for the tables and the 30 views before the views exist; the view columns are matched from the second view migration onward by the view conformance test of RWB-E1-069 | D-RCV-29 amended; RWB-E1-069 |

Where each rule lives in the target: nothing in the rule text changes, and the IDs are kept. BR1, BR2 and BR7 are answered inside `rwb_source_data` by `sys_objects`, `sys_fields` and `data_product`; the baseline contains at least 124 object rows and 1,382 field rows, including the source map and retired dictionary entries. BR1 runs table by table in the owning schema. BR3, BR4 and BR5 are answered by `data_product` in `rwb_source_data`; rwb-case owns reference-load version state and approval, and P1 applies an approved version through the reference-data contract (DP-07, RD-P1-020). `data_product_source` is owned and read by P1; its source-code seed follows NEW-ASM-B3 (RD-P1-021). BR6 is answered twice: the legacy `recoverySchema` parameter stays with the as-built baseline, and each service's own schema name now comes from its own Flyway configuration (DP-02, DP-15). BR8 becomes the boundary rule of the split as well as of the estate: no constraint points at `public`, and none points at another `rwb_*` schema (DP-01). BR9 is unchanged in substance: this story seeds the Physical Schema v8 dictionary plus data_product_source and its three fields, including the 49 extension-table fields and 304 view fields, before extension tables and view migrations run.

### 9. State transitions

This story changes the Flyway sequence of `rwb_source_data` and applies reference versions whose approval state is owned by rwb-case (RD-P1-020). P1 stores the current values for the 14 products in `data_product`; the approved reference version and its verification, approval and rollback state remain in `rwb_case.reference_version`.

| From | To | Trigger |
|---|---|---|
| rwb_source_data at its baseline, no P1 table of this story | rwb_source_data at this story's migration version with 13 P1 tables and the dictionary seed | The pipeline applies this story's migration in DEV, then in SIT |
| Reference version not applied in rwb_source_data | Approved P3 reference version applied to the P1-owned data_product rows | rwb-case approves the version and invokes the P1 handler |
| P1-owned rows for the reference version are in force | Same rows remain in force | The handler receives the same table, validFrom and content hash; it returns the first response with HTTP 200 and writes nothing (RD-P1-001) |

`data_product` holds the current values only (`uk_data_product` on `product_code`): the handler updates the rows in place, and earlier versions, their content hash, author, approver and rollback stay in `rwb_case.reference_version` (RD-P1-020). The 14 seeded rows are the baseline catalog with owner role RW-DATASTEW and an empty `owner_user_id`; the first approved version names the owners, and is not a repeat because rwb-case holds no earlier version.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Pipeline service identity (rwb-source-data pipeline) | Runs the service migration and dictionary conformance test in DEV and SIT, in `rwb_source_data` only |
| RW-REFADM, reference data administrator | Submits a reference version through the rwb-case contract; P3 checks the caller's rights |
| RW-DATASTEW, data steward and data product owner | Supplies the named product owner and reviews catalog values; P1 does not verify or approve the P3 reference version |
| Developers and data steward in DEV and SIT | Query `v_data_dictionary` with read access |
| rwb-case reference-load service | Verifies and approves the reference version, records the state, and invokes the P1 handler after approval (RD-P1-020) |

P1 validates and applies approved catalog content. The "confirm" step of version 2 is the approve operation of rwb-case (`POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve`, right A resolved by rwb-access; the author cannot approve, MSG-P7-002), and apply runs only after it. Pending: which role holds Reference data A for a `data_product` load (RW-DATASTEW holds R and U only), owner business analyst with compliance, tracked as NEW-GAP-S1-1.

### 11. Data

P1 owns 17 target tables: 13 application tables created by this story and four extension tables created by RWB-P1-E1069-DB. This story's migration also applies the four platform library tables (below), which are owned by PLT and are not counted in the 17. The local `decision_record` table that every service owns is created in `rwb_source_data` by the shared library migration of RWB-PLT-E1027-CON, not by this story's migration file, and is not counted in the 17; its DDL is Pending, owner platform lead (library owner), NEW-GAP-F08-7, and the library's own migration runs in the Testcontainers build. `case_list_row` and `lake_copy_watermark` have no target; their dictionary rows stay marked retired (RD-P1-021, RD-P1-024, RD-P1-025).

| # | Table | Schema | BR Field IDs | Fields | Read or write in this story |
|---:|---|---|---|---|---|
| 1 | data_product | rwb_source_data | DF-REF-070 to DF-REF-079 | all 10 fields | Create; seed 14 rows; apply approved versions |
| 2 | data_product_access | rwb_source_data | DF-REF-080 to DF-REF-086 | all 7 fields | Create; read only here |
| 3 | data_product_load | rwb_source_data | DF-OPS-001 to DF-OPS-009 | all 9 fields | Create; freshness stamp is written by RWB-P1-E1015-APP; not a reference-load state table (RD-P1-020) |
| 4 | data_contract | rwb_source_data | DF-OPS-010 to DF-OPS-020 | all 11 fields | Create; read only here |
| 5 | sys_objects | rwb_source_data | DF-REF-087 to DF-REF-093 | all 7 fields | Create; seed at least 124 rows, including the retired case_list_row object |
| 6 | sys_fields | rwb_source_data | DF-REF-094 to DF-REF-110 | all 17 fields | Create; seed at least 1,382 rows, including retired case_list_row fields |
| 7 | sys_field_version | rwb_source_data | DF-REF-111 to DF-REF-115 | all 5 fields | Create; read only here |
| 8 | data_product_source | rwb_source_data | DF-REF-300 to DF-REF-302 | all 3 fields | Create and seed source rows per RD-P1-021; source codes for core bank remain pending under NEW-ASM-B3 |
| 9 | reconciliation_result | rwb_source_data | DF-OPS-118 to DF-OPS-129 | all 12 fields | Create; read only here |
| 10 | dp_treatment | rwb_source_data | DF-TRT-034 to DF-TRT-051 | all 18 fields | Create; read only here |
| 11 | dp_guarantee_claim | rwb_source_data | DF-TRT-052 to DF-TRT-061 | all 10 fields | Create; read only here |
| 12 | interaction | rwb_source_data | DF-INT-001 to DF-INT-038 | all fields of the ledger | Create with append-only trigger; read only here |
| 13 | efs_ledger_outcome | rwb_source_data | DF-REF-128 to DF-REF-131 | all 4 fields | Create; read only here |
| 14 | party_ext | rwb_source_data | DF-EXT-001 to DF-EXT-005 (DF-EXT-006 to DF-EXT-012 are standard columns) | 5 business fields; 12 total | Seed dictionary fields only; RWB-P1-E1069-DB creates the table |
| 15 | contact_point_ext | rwb_source_data | DF-EXT-013 to DF-EXT-019 (DF-EXT-020 to DF-EXT-026 are standard columns) | 7 business fields; 14 total | Seed dictionary fields only; RWB-P1-E1069-DB creates the table |
| 16 | account_ext | rwb_source_data | DF-EXT-027 to DF-EXT-028 (DF-EXT-029 to DF-EXT-035 are standard columns) | 2 business fields; 9 total | Seed dictionary fields only; RWB-P1-E1069-DB creates the table |
| 17 | valuation_ext | rwb_source_data | DF-EXT-036 to DF-EXT-042 (DF-EXT-043 to DF-EXT-049 are standard columns) | 7 business fields; 14 total | Seed dictionary fields only; RWB-P1-E1069-DB creates the table |
| 18 | lake_copy_watermark | none | DF-OPS-130 to DF-OPS-135 | all 6 fields | No target; its dictionary object and field rows are marked retired (DP-17) |

Physical Schema v8 supplies the baseline of 123 objects, 1,379 fields and 304 ACE view fields. RD-P1-021 adds `data_product_source` and DF-REF-300 to DF-REF-302, so this migration seeds at least 124 objects and 1,382 fields. The case-list and lake-copy dictionary rows remain for baseline compatibility but are marked retired; their tables and operations are absent. The baseline dictionary covers 93 tables (89 Workbench and 4 extension) and 30 views, 123 objects (RD-P1-025); `data_product_source` is added to it as the 124th object (RD-P1-021). The dictionary seed of Physical Schema v9 holds 127 objects and 1,408 fields; the rows of `job_run`, `job_run_check`, `business_day_readiness` and DF-EXT-050 in it belong to later story migrations and are not seeded by this migration.

The 74 tables of the other services sit in their owning schemas and are not read, written or granted to this service (RD-P1-021). The four platform library tables `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` are owned by PLT and exist in every service schema (GAP-0109; Physical Schema v9 `rwb_source_data.sql`). Each service's own database step applies its copy (ASM-2473); in rwb-source-data that is this story's migration, from the RWB-PLT-TE006-CON DDL template. Their columns and dictionary rows are the library's, and no P1 story redefines them.

### 12. Contract

#### 12.1 REST operations provided

None. This story adds no REST operation. The data-product read and catalog-entry operations belong to RWB-P1-E1016-APP, freshness belongs to RWB-P1-E1015-APP, and the dictionary endpoint belongs to RWB-P1-E1064-APP. This story implements the `data_product` reference-table handler; its call transport and typed contract from rwb-case are Pending under NEW-GAP-F12-1.

#### 12.2 REST operations consumed

No REST operation is specified for this story. rwb-case invokes the P1 handler after its reference-load approval; the transport and request/response type are Pending under NEW-GAP-F12-1. The story reads no ACE table (DP-05).

#### 12.3 Events published

This story publishes no business event on `rwb.source-data.events.v1`. Applying a catalog version writes a local DecisionRecorded record through the PLT library and its outbox to `rwb.decision-record.v1`; the event type is `rwb.decision.DecisionRecorded.v1` (RD-P1-008). `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (RD-P1-003).

#### 12.4 Events consumed

None. A catalog load is a synchronous reference load; no event starts it.

#### 12.5 Workflows and activities

None. This story registers no Temporal workflow, activity or schedule. Its schema migration and reference-table handler are not Temporal work.

#### 12.6 Schedules

None. The migration runs on a deployment and the catalog load on a reference load; no Temporal Schedule is created or changed here (DP-10 is not in this story's pattern set).

#### 12.7 Tables owned

| Table | Schema | Owner (Ownership Map) | This story |
|---|---|---|---|
| data_product | rwb_source_data | P1 | Creates; seeds 14 products and applies approved reference versions |
| data_product_access | rwb_source_data | P1 | Creates; read only here |
| data_product_load | rwb_source_data | P1 | Creates; freshness stamp is written by RWB-P1-E1015-APP; not a load-state table |
| data_contract | rwb_source_data | P1 | Creates; read only here |
| sys_objects | rwb_source_data | P1 | Creates; seeds at least 124 object rows, including the retired case_list_row row |
| sys_fields | rwb_source_data | P1 | Creates; seeds at least 1,382 field rows, including retired case_list_row fields |
| sys_field_version | rwb_source_data | P1 | Creates; read only here |
| data_product_source | rwb_source_data | P1 | Creates and seeds P1's product-to-source map (RD-P1-021) |
| reconciliation_result | rwb_source_data | P1 | Creates; read only here |
| dp_treatment | rwb_source_data | P1 | Creates; read only here |
| dp_guarantee_claim | rwb_source_data | P1 | Creates; read only here |
| interaction | rwb_source_data | P1 | Creates with its append-only trigger; read only here |
| efs_ledger_outcome | rwb_source_data | P1 | Creates; read only here |
| party_ext, contact_point_ext, account_ext, valuation_ext | rwb_source_data | P1 | Dictionary fields only; RWB-P1-E1069-DB creates the tables |
| lake_copy_watermark | none | none | No target; its dictionary rows stay marked retired |
| case_list_row | none | none | No table or operations in P1; its dictionary rows stay marked retired (RD-P1-024, RD-P1-025) |
| the 74 tables of the other services | their owners' schemas | P2, P3, P4, P5, P6, P7, P8, P9, P10, S1 to S9 | Never read or written by this story; no cross-schema grant, join, constraint or view |
| outbox_event | rwb_source_data | PLT | Applied by this story's migration from the library DDL template; the decision-record library appends through it |
| outbox_delivery | rwb_source_data | PLT | Applied by this story's migration from the library DDL template; used by the local outbox relay |
| processed_event | rwb_source_data | PLT | Applied by this story's migration from the library DDL template; not written by this story |
| idempotency_key | rwb_source_data | PLT | Applied by this story's migration from the library DDL template; this story adds no REST POST |

The P1 login reads and writes only `rwb_source_data`, with SELECT on the 30 `recovery.v_ace_*` views. The four PLT-owned tables are applied in `rwb_source_data` by this story's migration; the decision-record library writes through the local `outbox_event` table (GAP-0109, RD-P1-003, RD-P1-008).

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| rwb-case reference-data contract fake (RWB-PLT-E1043-CON, RWB-P3-E1043-CON) | P3 submission, approval, version state and, once NEW-GAP-F12-1 is settled, the call to the P1 handler; until then tests call the handler class directly | Full, refused, unapproved and repeated reference versions; fake version publication remains a delivery step |
| Decision-record library fake (RWB-PLT-E1027-CON) | Local decision record and outbox append to `rwb.decision-record.v1` | Atomic application of a catalog version |
| Flyway sequence fake (RWB-PLT-E1044-CON) | Per-service Flyway sequence | Migration in a container database, forward only |
| Schema baseline (RWB-PLT-NF06-DB) | P1 service schema and boundary test | Migration starts on the service schema only |

The platform fake layout and published fake version remain Pending with the platform library owner.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None specified | The transport of the rwb-case call to the handler is Pending under NEW-GAP-F12-1 |
| Kafka | No business event on the service topic | None | PLT library writes `rwb.decision.DecisionRecorded.v1` to `rwb.decision-record.v1` |
| Temporal | None | None | No workflow, activity or schedule |
| File | 1 | 0 | The approved `data_product` reference version, delivered through the P3 reference-load process |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.catalog`, with the published types in `...sourcedata.catalog.api`. Service base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data` (not used by this story). The migration sits on the service's own Flyway sequence, `rwb-source-data`'s pipeline (DP-15).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<seq>__rwb_p1_e1001_data_products.sql` (sequence fixed at merge under D-RCV-28) | Flyway migration | Creates the 13 P1 application tables, indexes, `interaction` append-only trigger and `v_data_dictionary`; seeds 14 products, at least 124 objects, at least 1,382 fields, and `data_product_source`; applies the library DDL template for the four platform tables. Does not create extension tables |
| DataDictionaryConformanceTest | Test (pipeline) | Compares `information_schema.columns` with active `sys_fields` rows in both directions, ignoring the 7 standard columns and deferring extension and view fields until their objects exist; excludes retired rows and names any unmatched active field or physical type difference |
| DataProduct | Entity | Maps `data_product` in `rwb_source_data` |
| DataProductRepository | Repository | Reads and writes `data_product` in `rwb_source_data`; no statement names another schema |
| DataProductCatalogHandler | Published interface implementation | Implements the reference-table handler of the rwb-case reference-data contract for table code `data_product`: `validate` writes nothing, `apply` writes the whole file in one transaction and writes the local decision record with it |

**Database**

- Creates the 13 P1 application tables listed in section 11 and nothing else outside `rwb_source_data`. It does not create `case_list_row`, `lake_copy_watermark`, an extension table, or a table of another service. It applies the RWB-PLT-TE006-CON DDL template for `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` unchanged. The case-list and lake-copy records remain in the dictionary marked retired (RD-P1-024, RD-P1-025).
- Creates `data_product` with id uuid primary key, product_code varchar(25) not null and unique (`uk_data_product`), product_name varchar(80) not null, definition varchar(400) not null, system_of_record varchar(200) not null, owner_role varchar(20) not null, owner_user_id uuid, refresh_cycle varchar(10) not null with values DAILY, WEEKLY, MONTHLY and ON_CHANGE, expected_by varchar(20), valid_from date not null and the 7 standard columns.
- Creates `v_data_dictionary` in `rwb_source_data`, joining `sys_fields` to `sys_objects` on object_name and left joining `data_product` on product_code where the product is active, returning active rows only (`sys_fields.is_active` and `sys_objects.is_active`). Its columns are `field_id`, `object_name`, `field_name`, `data_type`, `physical_type`, `source_system`, `source_field` and `is_personal` from `sys_fields`; `data_product` from `sys_objects`; and `system_of_record`, `refresh_cycle`, `owner_role` and `owner_user_id` from `data_product`. It reads no ACE table and no other service's table. It is a read-model view object recorded here by this story, not an LDM v11 or Data Classification v5 entity.
- Adds `fk_sys_objects_data_product`; `sys_objects.data_product` is nullable. Product objects name DP01 to DP14; operational objects leave it empty. The 24 placeholder rows of `delegation_limit` are not seeded.
- The migration inserts the `data_product` rows, `data_product_source` rows and dictionary rows in one transaction. The source mapping table uses DF-REF-300 to DF-REF-302; core-bank source codes remain Pending under NEW-ASM-B3.
- No constraint points at schema `public` and none points at another `rwb_*` schema; a link to an ACE record stays a varchar(255) business key with no foreign key (BR8, DP-01).
- The tables, keys and indexes of the four extension tables arrive with RWB-P1-E1069-DB, on the same service sequence, after this story (DP-15).

**Configuration and reference data.** The schema name of the service's own schema comes from the deployment configuration of `rwb-source-data` (RWB-PLT-E1044-CON); the legacy parameter `recoverySchema` stays the as-built value of the baseline. Seed values inserted by the migration and repeated in the first catalog load file, with the owner user IDs, prepared by the reference data administrator and confirmed by the data steward:

| Code | Name | Definition | System of record | Refresh cycle | Expected by | Valid from |
|---|---|---|---|---|---|---|
| DP01 | Account and arrears | Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments | ACE (ingested from ALS) | DAILY | 08:00 | 2026-11-30 |
| DP02 | Customer and party | Customers, guarantors, co-borrowers and heirs, identity masked to the last four, contact points, consent and flags for vulnerability, death and bankruptcy | ACE (ingested from SCBPDM and the core bank) | DAILY | 08:00 | 2026-11-30 |
| DP03 | Case and ownership | The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP04 | Treatment and offers | Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome | ACE (ingested from the core bank) for the plan, with the treatment held in the Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP05 | Contact and promises | Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS | ACE (ingested from EFS) | DAILY | 08:00 | 2026-11-30 |
| DP06 | Collateral and assets | Collateral, appraisals, assets held after repossession or transfer, listings and sale results | ACE (ingested from CCMS, SVAF, AMIS and RPS) | WEEKLY | MON 08:00 | 2026-11-30 |
| DP07 | Legal events and cases | Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement | ACE (ingested from LIT and WIN) for the court record and the proof of delivery, with notices and enforcement held in the Recovery Workbench | DAILY | 08:00 | 2026-11-30 |
| DP08 | Partner performance | Partners on the panel, work placed with each, results, fees and scorecards | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP09 | Debt sale | Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP10 | Documents and extracted fields | Documents against the case, the fields read from them, retention class and custody of originals | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP11 | Scores and route economics | Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions | ACE (ingested from COLLINS) | DAILY | 08:00 | 2026-11-30 |
| DP12 | Decision log | One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP13 | Money and closure | Payments and proceeds matched to the case, write-off postings and recovery after charge-off | ACE (ingested from ALS and GL) | DAILY | 08:00 | 2026-11-30 |
| DP14 | Reference data | Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned | Recovery Workbench, with the ACE lists read through the views | ON_CHANGE | As it changes | 2026-11-30 |

Owner role RW-DATASTEW for every product; owner user IDs per environment. DP10 system_of_record is `Recovery Workbench` per RD-P1-025.
Product-to-source rows from RD-P1-021 (source codes for core bank await confirmation under NEW-ASM-B3):

| Product code | Source system |
|---|---|
| DP01 | ALS |
| DP02 | SCBPDM |
| DP02 | Pending: ACE source-system code for core bank; owner ACE team lead; NEW-ASM-B3 |
| DP04 | Pending: ACE source-system code for core bank; owner ACE team lead; NEW-ASM-B3 |
| DP05 | EFS |
| DP06 | CCMS |
| DP06 | SVAF |
| DP06 | AMIS |
| DP06 | RPS |
| DP07 | LIT |
| DP07 | WIN |
| DP11 | COLLINS |
| DP13 | ALS |
| DP13 | GL |

DP03, DP08, DP09, DP10, DP12 and DP14 have no `data_product_source` row and are never STALE (RD-P1-021). The migration seeds 12 source rows now; the two core bank rows wait for NEW-ASM-B3.

**Build steps**

The naming rule of D-RCV-28 (2026-11-05) is kept: a Flyway file is named `V<seq>__<story>_<name>.sql` with a four-digit sequence taken in merge order, line 1 is `-- Story: <story key>`, and the file is applied on the owning service's sequence (DP-15). The RWB-E1-001 baseline `V0001__rwb_e1_001_recovery_schema.sql` stays as built; this story's file is `V<seq>__rwb_p1_e1001_data_products.sql`, next free sequence at merge, in `rwb-source-data`'s pipeline. Each service schema has one V0001 baseline on its own sequence, and the view file follows the source V0002 and V0003 sections (GAP-0112).

1. Write the P1 application migration on the service Flyway sequence using the 13 P1 tables in section 11, the 14 `data_product` seeds, `data_product_source`, the dictionary seed and `v_data_dictionary`; run it on a PostgreSQL container with the empty `rwb_source_data` schema and its login and prove it creates no table of another service, no extension table and no retired table, and that the four platform library tables match the library DDL template.
2. Prove that a failing statement rolls the whole migration back and leaves `rwb_source_data` without any table of the migration (AC4).
3. Write DataDictionaryConformanceTest and add it after the migration stage; prove it fails on an extra column and a changed type (AC5), ignores the explicitly deferred extension/view fields and retired rows, and compares extension and view rows after their owning migrations create those objects.
4. Write DataProduct, DataProductRepository and DataProductCatalogHandler with the checks for BR2, BR3 and the list values; unit test the checks for X4, X5 and X6, including a bare source name (AC8, AC9, AC11).
5. Connect the handler to the reference-data contract fake for table code `data_product` and test a full load, a refused load and a repeated file against a container database (AC10).
6. Write the test that reads `v_data_dictionary` for `v_ace_account.days_past_due` and `account_ext.dispute_open` after a catalog load.
7. Use MSG-P1-003, MSG-P1-004 and MSG-P1-007 from Error and Message Standard v6; do not use MSG-P1-011 for a repeat load (RD-P1-001).
8. Prove the repeat is a skip (AC6), the migration creates no `v_ace_*` view, and the dictionary retains the 123/1,379 Physical Schema v8 baseline plus the source-map fields; the views belong to RWB-P1-E1069-APP and RWB-P1-E1069-DB.

**Feature flag.** `rwb.p1.data-catalog` from the platform flag library covers the catalog handler; the migration is not behind a flag. With the flag off the handler applies nothing and the caller gets the unavailable answer; rollback is flag off first, then the previous image, and migrations are never reversed (RD-P1-045).

**Done when.** The tests in section 16 pass, the migration runs in DEV and SIT on the `rwb-source-data` sequence, every active column and dictionary row for an existing object matches by name and physical type, the 49 extension fields and 304 view fields are seeded for their owning migrations to compare later, and the approved catalog version has 14 rows in `data_product`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-003 | Catalog row with no system of record, more than one, or no owner | {product} must have exactly one system of record and one named owner. |
| MSG-P1-004 | Catalog file without exactly DP01 to DP14 | The catalog must hold the 14 data products DP01 to DP14. Missing: {products}. |
| MSG-P1-007 | Catalog value outside its list | Row {row}: {field} must be one of {values}. |
| MSG-P4-002 | Role without Reference data C | You cannot {action} here. Your role does not include it. |

MSG-P1-003 uses the exact English text in Error and Message Standard v6. Thai text and any translation change remain with the message-standard owner. MSG-P4-002 is returned by the rwb-case reference-load authorization path, and MSG-P7-002 by its approve operation, not by this P1 handler. When a version has several failures the handler returns all of them in row order. MSG-P1-011 is not raised for a repeated load (RD-P1-001).

### 15. Screens and states

No screen in this story. The pipeline log shows the migration and conformance results. Developers and data stewards read the dictionary through the read model `v_data_dictionary`; the dictionary endpoint comes with RWB-P1-E1064-APP, the catalog entries with RWB-P1-E1016-APP, and SCR-40 Reference data in E8. The catalog screens will reach the service through the gateway-bff composite route (DP-19); no route, screen or screen state is built or asserted here. The states of SCR-40, empty, loading, error and no access, are Not specified in the source documents (CG-ALL-2012); they belong to SCR-40 in E8 and are not built or asserted here.

### 16. Test cases

| Acceptance criteria | Test case |
|---|---|
| AC1, AC4, AC5, AC6, AC8 to AC11, AC13 to AC24 | TC-P1-E1001-APP-10 to TC-P1-E1001-APP-16, TC-P1-E1001-APP-18, TC-P1-E1001-APP-21, TC-P1-E1001-APP-22, TC-E1-001-17, TC-P1-E1001-APP-01 to TC-P1-E1001-APP-09 |
| BR8; section 12.7 | TC-P1-E1001-APP-19 |
| AC2, AC3 and AC7 | Owned by RWB-ITG-E1001-ITG; existing IDs TC-E1-001-02, TC-E1-001-03 and TC-E1-001-07 remain with that story |
| Reference-load authentication, verification and approval | Owned by rwb-case; not tested by this story |

The test case IDs above are the rows of Test Cases v9 for this story.

### 17. Guardrails

- No business value in code: product names, definitions, systems of record, owners and refresh cycles come from the catalog load; the handler reads them as data and never as a constant (DP-07).
- No personal data in logs, tests or prompts. Owner user IDs in DEV and SIT are synthetic test users, and the dictionary rows carry no personal value.
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: this story creates no view over a public table and reads no public table (DP-05, ADR-010).
- No cross-schema read and no cross-schema key: every statement names `rwb_source_data` only, the login `rwb_source_data` holds no grant on any other `rwb_*` schema, and no constraint points at `public` or at another service's schema (DP-01, DP-02).
- Any runtime call to another service uses one hop and a 2 s timeout (DP-11). The transport of the rwb-case call to the P1 handler is Pending under NEW-GAP-F12-1.
- The migration changes no data outside `rwb_source_data`, creates no constraint into schema `public`, never drops a table in PROD and is forward only (DP-15).
- The dictionary reads `sys_objects`, `sys_fields`, `data_product` and `data_product_source`, all in `rwb_source_data`.
- The service publishes no business event on its own topic. The catalog apply writes `rwb.decision.DecisionRecorded.v1` to the shared `rwb.decision-record.v1` topic through the PLT decision-record library; the outbox event carries no personal data (DP-03, RD-P1-008).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record, one read path and one owner | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-01, FEAT-RDF-02 | Pending: L3 process link, owner business analyst, NEW-GAP-S1-3 | CTL-08; Principle 1; D-RCV-35 U1, U4; RD-P1-021; RD-P1-025 | TC-P1-E1001-APP-10 to TC-P1-E1001-APP-16, TC-P1-E1001-APP-18, TC-P1-E1001-APP-21, TC-P1-E1001-APP-22, TC-E1-001-17, TC-P1-E1001-APP-01 to TC-P1-E1001-APP-09 |
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Epic 2, 4; Program, 5.1 | FEAT-RDF-01 | Pending: L3 process link, owner business analyst, NEW-GAP-S1-3 | REQ-RDF-001; D-RCV-35 U1 | TC-P1-E1001-APP-10 |

**Module link.** Pending: source URL for the RWB-SVC-P1 module, owner business analyst, tracked as NEW-GAP-S1-3.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1044-CON | Contract | H build dependency: the per-service Flyway sequence and migration ownership (DP-15) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | Contract | H and C: the reference-data contract and its reference-table handler, through which the catalog is loaded (DP-07) |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | Contract | H and C: the parameters contract, read as data (DP-06) |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library behind the catalog apply (DP-03) |
| RWB-PLT-E1047-CON | Contract | H: the topic naming library (DP-14) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route the catalog screens will use (DP-19) |
| RWB-P1-E1069-DB | ACE DB | Sibling: creates the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` in `rwb_source_data`, whose 49 dictionary fields this story seeds |
| RWB-P1-E1069-APP | App development | Sibling: the 30 read-only ACE views and the view conformance test, on the next sequence after this story (DP-05) |
| RWB-PLT-NF06-DB | ACE DB | The schema split itself: the 19 `rwb_*` schemas, logins and the boundary test; this story is P1's share of it (DP-01, DP-02) |
| RWB-P1-E1015-APP | App development | Writes `data_product_load` and publishes `AceDataReady` and `AceDataLate` on `rwb.source-data.events.v1` |
| RWB-P1-E1064-APP | App development | Builds the dictionary endpoint and the field versions on the read model this story creates |
| RWB-P1-E1016-APP | App development | Builds access control per data product and the catalog entry maintenance on `data_product` and `data_product_access` |

### 19. Out of scope

- The 30 read-only ACE views, `recovery_views.sql` and the view conformance test (RWB-P1-E1069-APP), and their grants and the boundary rule (RWB-P1-E1069-DB).
- The four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` as tables, with their keys, indexes and grants: RWB-P1-E1069-DB. This story seeds and keeps their 49 dictionary fields only.
- Freshness stamp per data product from the ACE batch record, `data_product_load`, `AceDataReady` and `AceDataLate` (RWB-P1-E1015-APP).
- The dictionary endpoint and field versions (RWB-P1-E1064-APP); access control per data product, PDPA masking and the catalog entry screen (RWB-P1-E1016-APP).
- Retention and archive rules (RWB-P1-E1017-APP).
- The P1 account-page read (RWB-P1-E1002-APP) and reconciliation (RWB-P1-E1011-APP) are sibling work; the interaction ledger writer belongs to RWB-P1-E1066-APP and RWB-P1-E1067-APP. P1 has no case-list table, operations, workflow or schedule (RD-P1-024).
- The other 74 tables of the estate, the schemas of the other 18 services and the DB stories that create them (RWB-PLT-NF06-DB).
- The data lake, `lake_copy_watermark` and the decision log copy (DP-17: no data lake; JOB-13 becomes continuous Kafka ingest in rwb-decision). Pre-existing DP-17 handling is not re-litigated here.
- Stage 2 data products for contracts, plans and treatments beyond their catalog rows (REQ-RDF-014, Epic 2; RWB-P1-E2010-APP).

### 20. Remaining delivery steps

- Size: Not specified; owner delivery lead and product owner.
- Epic design sign-off: Pending; owner solution architect and business analyst.
- CON Done: Pending; owner rwb-case contract owner.
- Contract fake published: Pending; owner platform library owner.
- Test data in DEV: Pending; owner QA lead and data steward.
- Apply-handler transport, request, response and table code: Pending, NEW-GAP-F12-1; owner solution architect with the rwb-case service owner.
- Role holding Reference data A for a `data_product` load: Pending, NEW-GAP-S1-1; owner business analyst with compliance.
- Column recording the applied reference version on `data_product`: Pending, NEW-GAP-S1-2; owner data architect.
- Field declaration format and Change Register handoff: Pending, GAP-2537; owner data architect.
- L3 process and module links: Pending, NEW-GAP-S1-3; owner business analyst.
- Core-bank ACE source-system code in `data_product_source`: Pending, NEW-ASM-B3; owner ACE team lead.
- Confirm baseline schema documentation contains `data_product_source`, its three fields and the 124/1,382 minimum: Pending; owner data architect.