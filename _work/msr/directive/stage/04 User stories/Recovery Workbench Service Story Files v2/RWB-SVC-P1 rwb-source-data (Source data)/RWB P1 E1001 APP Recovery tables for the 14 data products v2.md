# RWB-P1-E1001-APP Recovery tables for the 14 data products

SCB Collections and Recovery. Henka Group, 22 November 2026.
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
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Service baseline (preconditions) | The six platform CON contracts RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-E1047-CON and RWB-PLT-N001-CON, with RWB-PLT-NF06-DB, are the service baseline; build against them and their fakes. The metadata row stays None and Ready to start stays Day 1 |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Contract version | rwb-case.yaml version 5.0.0 (Recovery Workbench API Specification v5), which holds `/admin/reference-loads` under `/api/recovery/case/v1` |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-029, FR-P1-031) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-001 is realigned into rwb-source-data. The built migration `V0001__rwb_e1_001_recovery_schema.sql` and the 92-table estate with its dictionary are kept as built; this story carries P1's share of that estate into the service's own schema `rwb_source_data` (DP-01, DP-15), keeps the one data product catalog and the one data dictionary that describe all 14 data products, seeds the 49 extension-table dictionary fields, and leaves the four extension tables to RWB-P1-E1069-DB, the 30 views and their grants to RWB-P1-E1069-APP and RWB-P1-E1069-DB, freshness to RWB-P1-E1015-APP and the dictionary endpoint to RWB-P1-E1064-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P1-E1001-APP-L241, X20 RWB-P1-E1001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (35 resolved, 59 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **P1's 18 tables, the 14 data product rows and the data dictionary that covers the 92 tables and the 30 read-only ACE views held in the rwb-source-data service's own schema, with one system of record and one owner per data product**, so that **every Workbench record has one home, every data product has one accountable owner and one read path, and the catalog and the dictionary stay one catalog and one dictionary after the 92-table estate is split across the 19 services**.

The legacy story built the estate as one schema. D-RCV-60 keeps the behaviour and moves the ownership:

- **Kept as built:** the migration `V0001__rwb_e1_001_recovery_schema.sql` and the 92 tables it creates in schema `recovery` are the as-built baseline. This story does not rewrite them (Template and Rules §R6, "Must change"; U2).
- **The new work is the schema split:** every service now writes its own schema `rwb_<name>` with its own login and its own Flyway sequence, forward only (DP-01, DP-02, DP-15; Arch v5 slides 29, 41 and 45). P1's share lands in `rwb_source_data`; the tables of the other services land with their owners' DB stories. No service reads another service's tables (DP-01); a call goes to the owner's contract, one hop, 2 s timeout (DP-11).
- **One catalog, one dictionary, one home:** `data_product` (14 rows), `sys_objects` (122 rows), `sys_fields` (1,366 rows), `sys_field_version`, `data_contract` and the read model `v_data_dictionary` stay together in `rwb_source_data`, because one dictionary that describes 14 data products cannot be split away from the tables it describes, and because a second service reading them would be a cross-schema read.
- **The four extension tables are P1's but are not created here.** `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` live in `rwb_source_data` and are delivered by the sibling DB story **RWB-P1-E1069-DB**, the DB and grant slice of RWB-E1-069. This story seeds and keeps their 49 dictionary fields (DF-EXT-001 to DF-EXT-049) and creates none of the four tables.
- **The other 75 tables do not land in this schema.** Of the 92 tables, P1 owns 18: 17 have `rwb_source_data` as their target, of which 13 are created by this story and the four extension tables by RWB-P1-E1069-DB, and the 18th, `lake_copy_watermark`, has no target (DP-17). The 75 that remain are the 74 tables of the other services, which sit in their owners' schemas, and `lake_copy_watermark`; this story reads none of them.
- **Bases and names:** REST base `/api/recovery/source-data/v1`, login and schema `rwb_source_data`, topic `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.sourcedata` (DP-02, DP-13, DP-14; Arch v5 slides 29 and 41). This story provides no REST operation and publishes no event; §12 says which story does.
- **Screens:** through the gateway-bff composite route (DP-19). No screen is in this story.

### 2. Business rationale

The Workbench holds no copy of source data. ACE ingests ALS, SCBPDM, EFS, COLLINS, CCMS, SVAF, AMIS, RPS, LIT, WIN, GL, NLEADS, EasyApp and Entra ID, and the Workbench reads what it needs through the 30 `recovery.v_ace_*` views (D-RCV-35 U1 and U4, ADR-010). The estate RWB-E1-001 built holds the 88 Workbench tables, the four extension tables that hold a Workbench decision about an ACE record, the metadata registry that holds the data dictionary as data, and the catalog of the 14 data products DP01 to DP14. Each data product then has exactly one system of record, written "ACE (ingested from X)" for source data, "Recovery Workbench" for Workbench records, or one sentence naming both where the product holds both, and one named owner, as REQ-RDF-001 requires. The measure it serves is "the ACE batch is complete when the Workbench reads it on 99 percent of days", because the dictionary and the catalog are what every later read and every freshness stamp are resolved against.

**What D-RCV-60 changes.** Not the rationale, and not the estate: the built migration is the as-built baseline and stays as built. What changes is the ownership boundary inside the same ACE database. The 92 tables were one schema; they are now 19 `rwb_*` schemas, one per service, each with its own login, its own Flyway sequence and its own grants, and each checked by a boundary test that fails the build on a cross-schema reference (DP-01, DP-02, DP-15; Arch v5 slides 29, 41 and 45). This story is P1's share of that move: the 14 data products, the dictionary that describes them and the tables P1 writes.

**Why the catalog and the dictionary stay with P1.** They are the one place where a number, a field or a freshness stamp is resolved to a data product and an owner (REQ-RDF-001, REQ-RDF-011). Split across 19 schemas they would answer 19 ways, and every other service reading them would be a cross-schema read the boundary rule forbids. Held in `rwb_source_data` they stay one catalog and one dictionary, reachable by contract and by the dictionary read model, with no second copy anywhere.

**Why the extension tables arrive with a separate story.** The four extension tables are P1's data, but their DDL, keys, indexes and grants belong to the DB slice RWB-P1-E1069-DB, which also carries the grants and the boundary rule of RWB-E1-069. This story therefore seeds their dictionary rows and creates none of them: the dictionary is complete before the tables exist, exactly as the built baseline seeded the view fields before the views existed.

**What the split does not change.** The Workbench still holds no copy of source data; P1 still reads ACE only through the 30 `recovery.v_ace_*` views (DP-05, ADR-010); and P1 now additionally holds no grant on any other `rwb_*` schema and creates no constraint that points at one.

### 3. Preconditions

- RWB-PLT-E1044-CON is in place: Flyway runs in the rwb-source-data pipeline and takes the schema name of the service's own schema from configuration. The legacy parameter `recoverySchema = recovery` and the built `V0001__rwb_e1_001_recovery_schema.sql` are the as-built baseline and are not re-opened.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are in place: the reference-data contract of rwb-case accepts a validated load for a table code and calls the handler that the owning service provides for it.
- The DEV and SIT databases of the ACE service exist, the schema `rwb_source_data` exists with its login, and the pipeline service identity may run migrations in that schema only (DP-02, DP-15).
- The reference data administrator (RW-REFADM) holds Reference data C. The person who queries the dictionary read model has read access to it in DEV or SIT.
- The catalog load file for the 14 data products is prepared from the seed table in section 13, with an owner user ID for each product in that environment (synthetic test users in DEV and SIT).
- RWB-PLT-E1027-CON (the local decision-record library), RWB-PLT-E1047-CON (topic naming) and RWB-PLT-N001-CON (the gateway-bff composite route) are in place.
- The four extension tables are delivered by RWB-P1-E1069-DB in the same schema; this story creates none of them and the conformance test accounts for that (AC1, AC5).
- The 30 `recovery.v_ace_*` views are not created here. RWB-P1-E1069-APP ships the 16 Section A views and RWB-P1-E1069-DB the grants and the boundary rule, on the next Flyway sequences after this story (DP-05).

### 4. Flow

1. Pipeline: runs this story's Flyway file in DEV on `rwb-source-data`'s own sequence, after the service baseline (DP-15).
2. Migration: creates P1's 13 tables in `rwb_source_data` (section 11), their indexes, the append-only trigger on `interaction`, and the catalog table `data_product`, in one transaction. It creates none of the four extension tables (RWB-P1-E1069-DB does). The append-only trigger on `decision_log_entry` belongs to rwb-decision (P7), and is not created here.
3. Migration: inserts the 14 `data_product` rows, then the 122 `sys_objects` rows and the 1,366 `sys_fields` rows (section 13), and creates the read model `v_data_dictionary` in `rwb_source_data`.
4. Migration: adds `fk_sys_objects_data_product` inside `rwb_source_data`; `sys_objects.data_product` is nullable, so the 24 operational objects of OPS, AGT and RPT carry no product.
5. Pipeline: runs the dictionary conformance test, which compares every column of the tables present in `rwb_source_data` with `sys_fields` in both directions, ignoring the 7 standard columns, and fails on any column with no dictionary row or any dictionary row of that schema with no column or a different physical type. The 49 DF-EXT-001 to DF-EXT-049 rows are checked as dictionary rows and are compared with a column once RWB-P1-E1069-DB has created the four extension tables.
6. Pipeline: repeats steps 1 to 5 in SIT.
7. Reference data administrator: loads the data product catalog file with table code `data_product` through the reference data contract of rwb-case (`POST /api/recovery/case/v1/admin/reference-loads`), naming the owner user ID of each product for the environment.
8. System: `DataProductCatalogHandler.validate` checks the file: 14 products DP01 to DP14, each with one system of record written "ACE (ingested from X)", "Recovery Workbench" or one sentence naming both, one owner role from LOV-ROLE, one owner user ID and one refresh cycle. The handler implements the reference-data contract's reference-table handler for table code `data_product`; it is a library implementation, not a new endpoint of this service.
9. Data steward: confirms the load as owner of the catalog through the reference data change process (the rwb-case reference-data contract, DP-07).
10. System: `DataProductCatalogHandler.apply` writes the 14 rows in `rwb_source_data` in one transaction with the valid from date, writes its local decision record in the same transaction and publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` through its outbox (DP-03).
11. Developer or data steward: queries `v_data_dictionary` for entity `v_ace_account` and field `days_past_due`.
12. System: returns field ID DF-ACE-018, data type NUMBER, physical type integer, source system ACE, source field `public.account.delay_days`, data product DP01, system of record "ACE (ingested from ALS)", refresh cycle DAILY and the owner of DP01.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A statement in the split migration fails | The transaction rolls back; `rwb_source_data` is left with none of the tables of that migration; the pipeline stage fails with the statement named | None (pipeline log) | AC4 |
| X2 | A table column exists with no sys_fields row, or a sys_fields row has no column or a different physical type | The conformance test fails and names the schema, the table, the column and the field ID | None (pipeline log) | AC5 |
| X3 | The migration runs again on a schema where it is already applied | Flyway skips it; no table or row changes | None | AC6 |
| X4 | A catalog row names no system of record, two systems of record, a bare source name such as "CCMS", or no owner user ID | The whole load is refused; no row is written | MSG-P1-003 | AC11 |
| X5 | The catalog file does not hold exactly the 14 products DP01 to DP14 | The whole load is refused | MSG-P1-004 | AC8 |
| X6 | A catalog row names an owner role or refresh cycle outside its list | The whole load is refused | MSG-P1-007 | AC9 |
| X7 | The same catalog file is loaded again | Nothing is written; the load is reported as already done | MSG-P1-011 | AC10 |
| X8 | A role without Reference data C loads the catalog | 403 Problem response; the refusal is in the access log | MSG-P4-002 | AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the Flyway sequence (RWB-PLT-E1044-CON) and the reference-data contract (RWB-PLT-E1043-CON, RWB-P3-E1043-CON); every later read, the case list, freshness and the dictionary story build on this one |
| Negotiable | The catalog values (names, definitions, owners, refresh cycles) are data in a load file; the story fixes the tables and the checks |
| Valuable | Gives every Workbench record one home in one service's schema, every data product one accountable owner, and one dictionary and one catalog for all 14 products after the split |
| Estimable | One migration on the service's own sequence, one read model, one conformance test, one reference-handler implementation |
| Small | Can be finished in two weeks or less with its tests, once RWB-P1-E1069-DB has created the four extension tables |
| Testable | Each criterion below is one automated test |

### 7. Acceptance criteria

```gherkin
Feature: Recovery tables for the 14 data products

  Scenario: AC1 Schema deployed (legacy RWB-E1-001 AC1)
    Given the migration V0001__rwb_e1_001_recovery_schema.sql and the parameter recoverySchema = "recovery"
    When the pipeline applies it in DEV and then in SIT
    Then the recovery schema in each environment holds 92 tables: the 88 Workbench tables and the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext
    Then it holds none of the tables that left the schema: loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory and tracker_row
    Then no constraint in schema recovery references a table in schema public
    Then every link to an ACE record is a varchar(255) business key with no foreign key: account_key, person_key, asset_key, payment_code and contact_key
    Then the conformance test reports 1,062 of the 1,062 table fields matched by name and physical type
    Then the 30 recovery.v_ace_* views ship separately in RWB-E1-069 and add their 304 fields to the dictionary

  Scenario: AC4 Failed migration leaves no partial schema (legacy RWB-E1-001 AC4)
    Given a copy of the migration in which the statement creating table valuation_ext fails
    When the pipeline applies it in DEV
    Then the pipeline stage fails and names the failing statement
    Then the recovery schema holds none of the tables of that migration
    Then the Flyway history has no successful row for version 1.001

  Scenario: AC5 Column without a dictionary entry fails the build (legacy RWB-E1-001 AC5)
    Given a branch that adds the column account_ext.branch_code with no sys_fields row
    When the conformance test runs in the pipeline
    Then the test fails with "account_ext.branch_code has no data dictionary entry"
    Then a sys_fields row DF-EXT-028 whose column is changed to type text fails the test with "DF-EXT-028 physical type boolean expected, text found"

  Scenario: AC6 Repeated migration has no effect (legacy RWB-E1-001 AC6)
    Given the migration version 1.001 already applied in SIT
    When the pipeline runs again in SIT
    Then Flyway reports version 1.001 as already applied
    Then the row counts of sys_objects (122) and sys_fields (1,366) are unchanged

  Scenario: AC8 Catalog with a missing product is refused (legacy RWB-E1-001 AC8)
    Given a catalog load file with 13 rows and no row for DP09
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-004 naming "DP09"
    Then the system writes no row

  Scenario: AC9 Value outside its list (legacy RWB-E1-001 AC9)
    Given the rwb-case reference-data contract mock returns LOV-ROLE without the role code "DP_OWNER"
    Given a catalog load file in which row 4 (DP04) names owner role "DP_OWNER" and row 5 (DP05) names refresh cycle "HOURLY"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-007 "Row 4: owner_role must be one of the role codes in LOV-ROLE." and "Row 5: refresh_cycle must be one of DAILY, WEEKLY, MONTHLY, ON_CHANGE."

  Scenario: AC10 Same catalog file loaded again (legacy RWB-E1-001 AC10)
    Given the catalog version loaded on 2026-11-30 is in force
    When the reference data administrator loads the same file again
    Then the system writes nothing
    Then the response carries MSG-P1-011 "The data product catalog load for 2026-11-30 is already complete or running. It was not run again."

  Scenario: AC11 Source named on its own is refused (legacy RWB-E1-001 AC11)
    Given a catalog load file in which DP06 names system of record "CCMS"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-003 "DP06 must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner."
    Then no row is written and the version in force stays in use

  Scenario: AC12 Role without Reference data C is refused (from TC-E1-001-11) (new, D-RCV-60)
    Given a user with role RW-DATASTEW who does not hold Reference data C
    When the user calls POST /admin/reference-loads with table data_product
    Then the system refuses the call with 403 and MSG-P4-002 "You cannot {action} here. Your role does not include it."
    Then the refusal is written to the access log

  Scenario: AC13 Personal fields are flagged in the dictionary (BR7) (new, D-RCV-60)
    Given the migration is applied in DEV on an empty rwb_source_data schema
    When the conformance test reads sys_fields
    Then every sys_fields row for a personal field holds is_personal = true

  Scenario: AC14 Dictionary is seeded before the views exist (BR9) (new, D-RCV-60)
    Given the migration is applied in DEV before any recovery.v_ace_* view migration has run
    When the conformance test reads sys_objects and sys_fields
    Then sys_objects holds 122 rows and sys_fields holds 1,366 rows, including the 304 view fields

  Scenario: AC15 A service's field declaration reaches the one dictionary (GAP-2537) (new, D-RCV-60)
    Given a service's field declaration carried as a build artefact of its story and handed to the one dictionary seed through the Change Register
    When the conformance test compares the declaration with the seeded sys_fields rows
    Then every declared field row is matched, and an unmatched row fails the test
    Then the declaring service neither writes rwb_source_data nor reads it at run time
```

**Target reading.** Every Given, When and Then above is the legacy line, value for value, with its origin tag. The only addition is one `Given` on AC9 that stubs the rwb-case reference-data contract the load reads LOV-ROLE from; no legacy line is changed or dropped. What changes is the schema each assertion now runs in:

- **AC1.** The as-built `recovery` schema keeps its 92 tables as built and is not rewritten. In the target each of those tables sits in exactly one `rwb_*` schema: P1's 13 in `rwb_source_data`, the four extension tables in the same schema once RWB-P1-E1069-DB has run, 74 in the schemas of the other services, and `lake_copy_watermark` with no target (DP-17). The assertion "no constraint references schema public" becomes the boundary rule of the split: no constraint points at `public` and none points at another `rwb_*` schema. The 92-table count, the twenty tables that left, the rule on the five business keys and the 304 view fields are unchanged, and the 1,062-field count stays the count of the estate: the dictionary this story seeds holds all 1,366 rows, the conformance test compares the tables present in `rwb_source_data` with them, and the estate reaches 1,062 of 1,062 matched only when RWB-P1-E1069-DB has created the four extension tables and the 74 tables of the other services are matched in their owners' schemas. The 30 `recovery.v_ace_*` views stay in schema `recovery` and are read only by `rwb-source-data` (DP-05, ADR-010).
- **AC4.** The failing statement is the one that creates a table of this story's split migration; the rollback leaves `rwb_source_data` without any table of that migration and the Flyway history without a successful row for the version this story applies. The 1.001 line of the built baseline stays as built.
- **AC5.** The conformance test compares `information_schema.columns` of `rwb_source_data` with `sys_fields`; the message texts, the table name and the field IDs are unchanged.
- **AC6.** The repeated version is the one this story applies on `rwb-source-data`'s own sequence; the counts 122 and 1,366 are unchanged.
- **AC8, AC9, AC10 and AC11.** The handler, the checks, the messages and the row counts are unchanged; the rows are written in `data_product` in `rwb_source_data`, and the refusal leaves the version in force untouched. AC9's added `Given` is the only stub line: it answers LOV-ROLE from the rwb-case reference-data contract fake (DP-07, C RWB-P3-E1043-CON) and every legacy value of the criterion is kept.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every table column and every view column in the recovery estate has exactly one row in the data dictionary, with its BR Field ID, types, source system and meaning | Logical Data Model and Data Dictionary; sys_fields |
| BR2 | Workbench data is held in the 14 data products DP01 to DP14 | REQ-RDF-001; sys_objects.data_product |
| BR3 | Each data product has exactly one system of record, written "ACE (ingested from X)" for source data, "Recovery Workbench" for Workbench records, or, where the product holds both, one sentence that names ACE with its sources and the Recovery Workbench; and one named owner | REQ-RDF-001; D-RCV-35 U1 |
| BR4 | The catalog values are a versioned data load, changed without a code release; a load with an exception is refused in full | Principle 1; DT02; CTL-08 |
| BR5 | Where a product is fed by several sources (DP06, DP07, DP13), its one system of record names ACE and every source it ingests; a bare source name is refused because no source reaches the Workbench except through ACE | D-RCV-35; ADR-010 |
| BR6 | Schema names come from parameters; one migration per story; forward only in PROD | RWB-E1-044 |
| BR7 | Personal fields carry is_personal = true in the dictionary so masking (RWB-E1-016) can read them | sys_fields.is_personal; CTL-11 |
| BR8 | The recovery estate holds no copy of source data. No constraint references a table in schema public, and a link to an ACE record is a varchar(255) business key with no foreign key | D-RCV-35 U4; ADR-010; Data Tier Map section 1 |
| BR9 | The baseline migration seeds the dictionary for the tables and the 30 views before the views exist; the view columns are matched from the second view migration onward by the view conformance test of RWB-E1-069 | D-RCV-29 amended; RWB-E1-069 |

Where each rule lives in the target: nothing in the rule text changes, and the IDs are kept. BR1, BR2 and BR7 are answered inside `rwb_source_data` by `sys_objects`, `sys_fields` and `data_product`, and BR1 now runs table by table in the owning schema instead of over one schema. BR3, BR4 and BR5 are answered by `data_product` in `rwb_source_data` through the rwb-case reference-data contract (DP-07); the catalog rows never move. BR6 is answered twice: the legacy `recoverySchema` parameter stays with the as-built baseline, and each service's own schema name now comes from its own Flyway configuration (DP-02, DP-15). BR8 becomes the boundary rule of the split as well as of the estate: no constraint points at `public`, and none points at another `rwb_*` schema (DP-01). BR9 is unchanged in substance: this story seeds the 1,366 dictionary rows, including the 49 extension-table fields and the 304 view fields, before RWB-P1-E1069-DB creates the four extension tables and before the view migrations run, so the conformance test has a complete dictionary to compare against.

### 9. State transitions

None. This story does not change a case status. It moves two versions: the Flyway sequence of `rwb_source_data`, from its baseline to the first version this story applies on it (DP-15), and the version of the data product catalog, from none to the first loaded version. The Flyway version 1.001 of the built `recovery` schema stays as built and is not moved.

| From | To | Trigger |
|---|---|---|
| rwb_source_data at its baseline, no P1 table of this story | rwb_source_data at the version this story applies, 13 tables and the dictionary seed | The pipeline applies this story's migration in DEV, then in SIT |
| Catalog version none | Catalog version 2026-11-30 in force | The 14 rows are applied in one transaction and the version becomes current |
| Catalog version 2026-11-30 in force | Catalog version 2026-11-30 in force (no change) | The same file is loaded again; nothing is written and the answer is MSG-P1-011 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Pipeline service identity (rwb-source-data pipeline) | Runs the service's migration and the conformance test in DEV and SIT, in `rwb_source_data` only |
| RW-REFADM, reference data administrator | Loads the catalog file (Reference data C) |
| RW-DATASTEW, data steward and data product owner | Confirms the catalog version as its owner (Reference data U); cannot load it (no Reference data C) |
| Developers and the data steward in DEV and SIT | Query the dictionary read model `v_data_dictionary` with read access to it |
| Any role without Reference data C | Refused with MSG-P4-002 on the catalog load |

No approval level from the delegation of authority applies. Every "who" in this table is a role code; the roles, their permissions and the separation-of-duty conflicts are held as data in rwb-access (P4) and reached through its authorise contract, not by a table read (DP-01, DP-08).

### 11. Data

Table per owning schema, from the Ownership Map only. P1 owns 18 tables: 13 are created in `rwb_source_data` by this story, the four extension tables also land in `rwb_source_data` but are created by RWB-P1-E1069-DB, and the 18th, `lake_copy_watermark`, has no target (DP-17).

| # | Table | Schema | BR Field IDs | Fields | Read or write in this story |
|---:|---|---|---|---|---|
| 1 | data_product | rwb_source_data | DF-REF-070 to DF-REF-079 | all 10 fields | Create and write 14 rows; read |
| 2 | data_product_access | rwb_source_data | DF-REF-080 to DF-REF-086 | all 7 fields | Create (table only); read |
| 3 | data_product_load | rwb_source_data | DF-OPS-001 to DF-OPS-009 | all 9 fields | Create (table only); the stamp is written by RWB-P1-E1015-APP |
| 4 | data_contract | rwb_source_data | DF-OPS-010 to DF-OPS-020 | all 11 fields | Create (table only); read |
| 5 | sys_objects | rwb_source_data | DF-REF-087 to DF-REF-093 | all 7 fields | Create and write 122 rows; read |
| 6 | sys_fields | rwb_source_data | DF-REF-094 to DF-REF-110 | all 17 fields | Create and write 1,366 rows; read |
| 7 | sys_field_version | rwb_source_data | DF-REF-111 to DF-REF-115 | all 5 fields | Create (table only); read |
| 8 | case_list_row | rwb_source_data | DF-RPT-001 to DF-RPT-019 | all 19 fields | Create (table only); read |
| 9 | reconciliation_result | rwb_source_data | DF-OPS-118 to DF-OPS-129 | all 12 fields | Create (table only); read |
| 10 | dp_treatment | rwb_source_data | DF-TRT-034 to DF-TRT-051 | all 18 fields | Create (table only); read |
| 11 | dp_guarantee_claim | rwb_source_data | DF-TRT-052 to DF-TRT-061 | all 10 fields | Create (table only); read |
| 12 | interaction | rwb_source_data | DF-INT-001 to DF-INT-038 | all fields of the ledger | Create (table only) with its append-only trigger; read |
| 13 | efs_ledger_outcome | rwb_source_data | DF-REF-128 to DF-REF-131 | all 4 fields | Create (table only); read |
| 14 | party_ext | rwb_source_data | DF-EXT-001 to DF-EXT-005 (DF-EXT-006 to DF-EXT-012 are the standard columns) | the 5 business fields; 12 in all | Dictionary fields only: seed the 12 rows. The table is created by RWB-P1-E1069-DB |
| 15 | contact_point_ext | rwb_source_data | DF-EXT-013 to DF-EXT-019 (DF-EXT-020 to DF-EXT-026 are the standard columns) | the 7 business fields; 14 in all | Dictionary fields only: seed the 14 rows. The table is created by RWB-P1-E1069-DB |
| 16 | account_ext | rwb_source_data | DF-EXT-027 to DF-EXT-028 (DF-EXT-029 to DF-EXT-035 are the standard columns) | the 2 business fields; 9 in all | Dictionary fields only: seed the 9 rows. The table is created by RWB-P1-E1069-DB |
| 17 | valuation_ext | rwb_source_data | DF-EXT-036 to DF-EXT-042 (DF-EXT-043 to DF-EXT-049 are the standard columns) | the 7 business fields; 14 in all | Dictionary fields only: seed the 14 rows. The table is created by RWB-P1-E1069-DB |
| 18 | lake_copy_watermark | none | DF-OPS-130 to DF-OPS-135 | all 6 fields | No target (DP-17): not re-created, and its 6 dictionary rows are the legacy record of a removed table. Its DDL is kept in Physical Schema v7 `rwb_source_data.sql` with a retirement note, and the P1 DB story drops the table (GAP-0114) |

Field IDs are those in the Logical Data Model and Data Dictionary and in Physical Schema v7. Table names are the physical names in Physical Schema v7; `v_data_dictionary` is a read-model view, not an LDM v9 or Data Classification v5 entity. The 92 tables hold 1,062 fields: 1,013 on the 88 Workbench tables, including the 34 of data_product, sys_objects and sys_fields, and 49 on the four extension tables. The 30 views add 304 fields, so the dictionary holds 122 objects and 1,366 fields. Target count: 93 tables, being the 87 Workbench tables and the 6 platform library tables of the Ownership Map v1 sheet Tables; the 92 tables above are the version 6 monolith count that the physical schema work replaces. The Ownership Map v1 sheet Tables governs ownership for all of them.

**The other 75 tables.** The 74 tables of the other services sit in their owners' schemas: rwb_case, rwb_decision, rwb_access, rwb_document, rwb_comms, rwb_payment, rwb_reporting, rwb_agent, rwb_integration, rwb_valuation, rwb_treatment, rwb_guarantee, rwb_litigation, rwb_asset, rwb_debtsale, rwb_writeoff, rwb_deviation and rwb_partner; the 75th, `lake_copy_watermark`, has no target (DP-17). This story creates none of them, reads none of them and holds no grant on any of them (DP-01). The 979 fields of the legacy count cover all 85 Workbench tables other than data_product, sys_objects and sys_fields, P1's own among them, and every one of those field rows is in the 1,366 dictionary rows this story seeds, which is the one place where the split does not follow the tables.

Ruled 2026-11-06 as D-RCV-29 and amended by D-RCV-35: the baseline migration seeds the full recovery dictionary, 122 `sys_objects` rows and 1,366 `sys_fields` rows, as held in Recovery Workbench Physical Schema v7.sql, so the dictionary is complete before the views exist and the conformance test can run. The 108 objects and 1,256 fields of the v4 copy schema are superseded. `delegation_limit` holds no baseline rows; its content is loaded as version DOA-2026.11 through RWB-E1-043 by RWB-E1-038 (D-RCV-34), and in the target it is loaded through the rwb-case reference-data contract into `rwb_access`. Later dictionary changes are reference loads through the same contract (D-RCV-28).

### 12. Contract

#### 12.1 REST operations provided

None. This story provides no REST operation. The data product, freshness and dictionary endpoints of the service belong to RWB-P1-E1064-APP (the dictionary and the data product read), RWB-P1-E1015-APP (freshness) and RWB-P1-E1016-APP (catalog entry maintenance), and this key has no CON story that would add one here. The catalog load reaches this service as a reference-table handler of the rwb-case reference-data contract (DP-07), not as an endpoint of this service.

#### 12.2 REST operations consumed

None at run time. The catalog load is invoked in process against the reference-data contract's handler for table code `data_product`; this service calls no REST operation of another service in this story, and it reads no ACE table (DP-05).

#### 12.3 Events published

None. This story produces no business event. The decision that a catalog version was applied is written as a local decision record through the decision-record library and published as `DecisionRecorded` on `rwb.decision-record.v1` (DP-03); that is a library write, not an event of this story, and the central ledger is rwb-decision's. DP-14 fixes the naming of the service topic `rwb.source-data.events.v1` with the events `AceDataReady` and `AceDataLate` (05:30); those belong to RWB-P1-E1015-APP and RWB-P1-E1011-APP, and this story publishes none of them.

#### 12.4 Events consumed

None. A catalog load is a synchronous reference load; no event starts it.

#### 12.5 Workflows and activities

None. No Temporal workflow or activity is in this story: `AceIngestCheck`, `reconciliation`, `listEligibleAccounts` and `snapshot(page)` belong to RWB-P1-E1015-APP, RWB-P1-E1011-APP and RWB-P1-E1002-APP on task queue `rwb-source-data` in namespace `rwb-recovery`.

#### 12.6 Schedules

None. The migration runs on a deployment and the catalog load on a reference load; no Temporal Schedule is created or changed here (DP-10 is not in this story's pattern set).

#### 12.7 Tables owned

| Table | Schema | Owner (Ownership Map) | This story |
|---|---|---|---|
| data_product | rwb_source_data | P1 | Creates; writes the 14 seed rows and the loaded version |
| data_product_access | rwb_source_data | P1 | Creates; read only here |
| data_product_load | rwb_source_data | P1 | Creates; read only here |
| data_contract | rwb_source_data | P1 | Creates; read only here |
| sys_objects | rwb_source_data | P1 | Creates; writes 122 rows |
| sys_fields | rwb_source_data | P1 | Creates; writes 1,366 rows |
| sys_field_version | rwb_source_data | P1 | Creates; read only here |
| case_list_row | rwb_source_data | P1 | Creates; read only here |
| reconciliation_result | rwb_source_data | P1 | Creates; read only here |
| dp_treatment | rwb_source_data | P1 | Creates; read only here |
| dp_guarantee_claim | rwb_source_data | P1 | Creates; read only here |
| interaction | rwb_source_data | P1 | Creates with its append-only trigger; read only here |
| efs_ledger_outcome | rwb_source_data | P1 | Creates; read only here |
| party_ext, contact_point_ext, account_ext, valuation_ext | rwb_source_data | P1 | Dictionary fields only; the four tables are created by RWB-P1-E1069-DB |
| lake_copy_watermark | none | P1 | No target (DP-17): not re-created |
| the 74 tables of the other services | their owners' schemas | P2, P3, P4, P5, P6, P7, P8, P9, P10, S1 to S9 | **Never read.** No grant, no join, no constraint, no view (DP-01) |

The other 14 service schemas of the estate (P2, P5, P6, P9, P10 and S1 to S9) are never read by rwb-source-data, and rwb-source-data writes nothing outside `rwb_source_data`. Database access uses the login `rwb_source_data`, which holds grants on its own schema and SELECT on the 30 `recovery.v_ace_*` views and on nothing else (DP-02, DP-05; Arch v5 slide 29). The split mechanics, the login and schema names and the extension-table delivery boundary are recorded as GAP-0557 with ASM-0794 to ASM-0798.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| Parameters contract fake (RWB-PLT-E1042-CON, RWB-P3-E1042-CON) | The parameters contract of rwb-case | Any parameter the catalog handler needs, read as data and never as a constant (DP-06) |
| Reference-data contract fake (RWB-PLT-E1043-CON, RWB-P3-E1043-CON) | The reference-data contract of rwb-case, including the reference-table handler for table code `data_product` | Every load, refusal and repeat of AC8, AC9, AC10 and AC11 from Day 1 (DP-07) |
| Decision-record library fake (RWB-PLT-E1027-CON) | The local decision-record library and `rwb.decision-record.v1` | The decision record written in the same transaction as the 14 rows (DP-03) |
| Topic naming fake (RWB-PLT-E1047-CON) | The naming library | The service topic name is resolved by the library and never typed in code (DP-14) |
| Flyway sequence fake (RWB-PLT-E1044-CON) | The per-service Flyway sequence | The migration runs on the service's own sequence in a container database, forward only (DP-15) |
| gateway-bff composite route fake (RWB-PLT-N001-CON) | The edge composite route | The route the catalog screens will use, built before the screens exist (DP-19) |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No endpoint in this story; the catalog load is a reference-data contract handler (DP-07) |
| Kafka | None published | None consumed | One library write of `DecisionRecorded` on `rwb.decision-record.v1` (DP-03); the service topic `rwb.source-data.events.v1` is named but not produced here (DP-14) |
| Temporal | None | None | No workflow, activity or schedule; queue `rwb-source-data` is not used by this story |
| File | 1 | 0 | The catalog load file for table code `data_product`, read through the reference-data contract handler in the request; no claim-check store |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata.catalog`, with the published types in `...sourcedata.catalog.api`. Service base `/api/recovery/source-data/v1`, schema and login `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data` (not used by this story). The migration sits on the service's own Flyway sequence, `rwb-source-data`'s pipeline (DP-15).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `V<seq>__rwb_p1_e1001_data_products.sql` (sequence number fixed at merge under D-RCV-28) | Flyway migration (the split migration) | Creates P1's 13 tables in `rwb_source_data`, their indexes and the append-only trigger on `interaction`, creates `data_product` and the read model `v_data_dictionary`, and inserts the 122 `sys_objects` rows, the 1,366 `sys_fields` rows and the 14 `data_product` seed rows. Creates none of the four extension tables: those are RWB-P1-E1069-DB's |
| DataDictionaryConformanceTest | Test (pipeline) | Compares `information_schema.columns` of `rwb_source_data` with `sys_fields` in both directions, ignoring the 7 standard columns; reports the tables present and names any column without a dictionary row and any dictionary row without a column or with a different physical type |
| DataProduct | Entity | Maps `data_product` in `rwb_source_data` |
| DataProductRepository | Repository | Reads and writes `data_product` in `rwb_source_data`; no statement names another schema |
| DataProductCatalogHandler | Published interface implementation | Implements the reference-table handler of the rwb-case reference-data contract for table code `data_product`: `validate` writes nothing, `apply` writes the whole file in one transaction and writes the local decision record with it |

**Database**

- Creates P1's 13 tables in `rwb_source_data` (section 11) and nothing else: no `loan_account`, `account_payment`, `party`, `contact_point`, `collateral`, `account_collateral`, `collections_history`, `party_product`, `valuation`, `score`, `asset`, `load_run`, `dq_exception`, `dq_rule`, `source_field_map`, `source_code_map`, `interface_run`, `interface_signoff`, `tracker_inventory` or `tracker_row`, and no `lake_copy_watermark` (DP-17). The names `loan_account`, `account_payment`, `contact_point`, `account_collateral`, `collections_history`, `load_run`, `dq_exception`, `dq_rule`, `source_field_map`, `source_code_map`, `interface_run`, `interface_signoff`, `tracker_inventory` and `tracker_row` are not LDM v9 or Data Classification v5 entities or fields; the story names them only as exclusions.
- Creates `data_product` with product_code varchar(25) primary key, product_name varchar(80) not null, definition varchar(400) not null, system_of_record varchar(120) not null, owner_role varchar(20) not null, owner_user_id uuid, refresh_cycle varchar(10) not null with values DAILY, WEEKLY, MONTHLY and ON_CHANGE, expected_by varchar(20), valid_from date not null and the 7 standard columns.
- Creates `v_data_dictionary` in `rwb_source_data`, joining `sys_fields` to `sys_objects` on object_name and left joining `data_product` on product_code where the product is active, returning active rows only. It reads no ACE table and no other service's table. It is a read-model view object recorded here by this story, not an LDM v9 or Data Classification v5 entity.
- Adds `fk_sys_objects_data_product`; `sys_objects.data_product` is nullable, so the 98 product objects name DP01 to DP14 and the 24 operational objects of OPS (13), AGT (8) and RPT (3) leave it empty. The 24 placeholder rows of `delegation_limit` are not seeded.
- The migration inserts the `data_product` rows before the `sys_objects` rows, in one transaction.
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
| DP10 | Documents and extracted fields | Documents against the case, the fields read from them, retention class and custody of originals | Recovery Workbench document hub | ON_CHANGE | As it changes | 2026-11-30 |
| DP11 | Scores and route economics | Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions | ACE (ingested from COLLINS) | DAILY | 08:00 | 2026-11-30 |
| DP12 | Decision log | One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome | Recovery Workbench | ON_CHANGE | As it changes | 2026-11-30 |
| DP13 | Money and closure | Payments and proceeds matched to the case, write-off postings and recovery after charge-off | ACE (ingested from ALS and GL) | DAILY | 08:00 | 2026-11-30 |
| DP14 | Reference data | Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned | Recovery Workbench, with the ACE lists read through the views | ON_CHANGE | As it changes | 2026-11-30 |

Owner role RW-DATASTEW for every product; owner user IDs per environment.

**Build steps**

The naming rule of D-RCV-28 (2026-11-05) is kept: a Flyway file is named `V<seq>__<story>_<name>.sql` with a four-digit sequence taken in merge order, line 1 is `-- Story: <story key>`, and the file is applied on the owning service's sequence (DP-15). The RWB-E1-001 baseline `V0001__rwb_e1_001_recovery_schema.sql` stays as built; this story's file is `V<seq>__rwb_p1_e1001_data_products.sql`, next free sequence at merge, in `rwb-source-data`'s pipeline. Each service schema has one V0001 baseline on its own sequence, and the view file follows the source V0002 and V0003 sections (GAP-0112).

1. Write the split migration from Physical Schema v7: P1's 13 tables in `rwb_source_data`, plus `data_product` with its 14 seed rows and `v_data_dictionary`; run it on an empty PostgreSQL container with the service's schema only, and prove it creates no table of another service, none of the four extension tables and no `lake_copy_watermark`.
2. Prove that a failing statement rolls the whole migration back and leaves `rwb_source_data` without any table of the migration (AC4).
3. Write DataDictionaryConformanceTest and add it to the pipeline after the migration stage; prove it fails on an extra column and on a changed type (AC5), prove it names no unmatched dictionary row for `rwb_source_data`, and prove the 49 DF-EXT-001 to DF-EXT-049 rows are in the dictionary and are compared with a column once RWB-P1-E1069-DB has created the four tables.
4. Write DataProduct, DataProductRepository and DataProductCatalogHandler with the checks for BR2, BR3 and the list values; unit test the checks for X4, X5 and X6, including a bare source name (AC8, AC9, AC11).
5. Connect the handler to the reference-data contract fake for table code `data_product` and test a full load, a refused load and a repeated file against a container database (AC10).
6. Write the test that reads `v_data_dictionary` for `v_ace_account.days_past_due` and `account_ext.dispute_open` after a catalog load.
7. Add messages MSG-P1-003, MSG-P1-004, MSG-P1-007 and MSG-P1-011 to the message table with English and Thai text.
8. Prove the repeat is a skip and the counts stay at 122 and 1,366 (AC6), and confirm the migration creates no `v_ace_*` view: those are RWB-P1-E1069-APP's and RWB-P1-E1069-DB's.

**Feature flag.** `rwb.p1.data-catalog`, from the platform flag library. The flag covers the catalog handler; the migration is not behind a flag.

**Done when.** The tests in section 16 pass, the migration runs clean in DEV and SIT on `rwb-source-data`'s own sequence, the conformance test reports every column of `rwb_source_data` matched by name and physical type with no unmatched dictionary row of that schema, the 49 DF-EXT-001 to DF-EXT-049 rows are in the dictionary and are matched once RWB-P1-E1069-DB has created the four extension tables, and the catalog version for SIT holds 14 rows in `rwb_source_data`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-003 | Catalog row with no system of record, more than one, a bare source name, or no owner | {product} must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner. |
| MSG-P1-004 | Catalog file without exactly DP01 to DP14 | The catalog must hold the 14 data products DP01 to DP14. Missing: {products}. |
| MSG-P1-007 | Catalog value outside its list | Row {row}: {field} must be one of {values}. |
| MSG-P1-011 | Same catalog file loaded again | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without Reference data C | You cannot {action} here. Your role does not include it. |

Thai text for each new message follows DL10 and is in the additions file. DL10 is still open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed, so the Thai text follows them as assumed. The IDs and texts are the legacy ones, character for character; MSG-P4-002 is now raised by the guard library of rwb-access, so the refusal is identical in every service.

### 15. Screens and states

No screen in this story. The pipeline log shows the migration and conformance results. Developers and data stewards read the dictionary through the read model `v_data_dictionary`; the dictionary endpoint comes with RWB-P1-E1064-APP, the catalog entries with RWB-P1-E1016-APP, and SCR-40 Reference data in E8. The catalog screens will reach the service through the gateway-bff composite route (DP-19); no route, screen or screen state is built or asserted here. The states of SCR-40, empty, loading, error and no access, are Not specified in the source documents (CG-ALL-2012); they belong to SCR-40 in E8 and are not built or asserted here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-001-01 | AC1, BR1, BR6, BR8 | End to end | Empty DEV and SIT schemas; schema parameter "recovery"; a branch that adds a foreign key to public.account |
| TC-E1-001-02 | AC2, BR1 | End to end | Dictionary from the migration; catalog with a synthetic owner for DP01 (run by RWB-ITG-E1001-ITG) |
| TC-E1-001-03 | AC3, BR2, BR3, BR5 | End to end | Catalog file of 14 rows from the seed table (run by RWB-ITG-E1001-ITG) |
| TC-E1-001-04 | AC4 | End to end | Migration copy with a failing CREATE TABLE valuation_ext |
| TC-E1-001-05 | AC5, BR1 | End to end | Branch with account_ext.branch_code; changed type on DF-EXT-028 |
| TC-E1-001-06 | AC6 | End to end | SIT schema at version 1.001 |
| TC-E1-001-07 | AC7, BR3, BR4 | End to end | Catalog file with DP06 naming two systems and DP11 with no owner (run by RWB-ITG-E1001-ITG) |
| TC-E1-001-08 | AC8, BR2, BR4 | End to end | Catalog file of 13 rows without DP09 |
| TC-E1-001-09 | AC9, BR4 | End to end | Catalog file with owner role DP_OWNER and refresh cycle HOURLY |
| TC-E1-001-10 | AC10, BR4 | End to end | Same catalog file loaded twice |
| TC-E1-001-11 | Access | Component | RW-DATASTEW calls POST /admin/reference-loads with table data_product; refused with MSG-P4-002 |
| TC-E1-001-12 | AC11, BR3, BR5 | End to end | Catalog file with DP06 naming "CCMS" |
| TC-E1-001-13 | BR8; section 12.7 | End to end | Split migration in DEV on an empty schema; each table of section 12.7 checked in its owning schema, and no grant, join, constraint or view on the 74 tables of the other services |
| TC-E1-001-14 | AC12 | Component | RW-DATASTEW calls POST /admin/reference-loads with table data_product; refused with 403 and MSG-P4-002 |
| TC-E1-001-15 | AC13, BR7 | End to end | Migration applied in DEV on an empty schema; sys_fields rows for personal fields |
| TC-E1-001-16 | AC14, BR9 | End to end | Migration applied in DEV before any recovery.v_ace_* view migration |
| TC-E1-001-17 | AC15, BR1 | Component | A service's field declaration handed over through the Change Register, compared with the seeded sys_fields rows; one declared row left unmatched; file format Not specified in the source documents (GAP-2537) |

The 12 legacy TC IDs, their Covers and their Data are kept in legacy order and character for character, so a row still names AC2, AC3 or AC7 where the legacy named it: those three criteria sit with other slices of this key and are not in this story's gherkin. The legacy Level "System" maps to "End to end" and "Access" maps to "Component", because the access test now exercises the guard library and the access contract fake in one component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; TC-E1-001-12 to TC-E1-001-17 are not yet in that tab. TC-E1-001-02, TC-E1-001-03 and TC-E1-001-07 are the legacy rows for AC2, AC3 and AC7, which sit with other slices of this key; this story does not own those criteria. RWB-ITG-E1001-ITG owns AC2, AC3 and AC7 and runs those three test cases; the note "run by" in their Data cells is the only addition to the legacy Data.

### 17. Guardrails

- No business value in code: product names, definitions, systems of record, owners and refresh cycles come from the catalog load; the handler reads them as data and never as a constant (DP-07).
- No personal data in logs, tests or prompts. Owner user IDs in DEV and SIT are synthetic test users, and the dictionary rows carry no personal value.
- ACE data only through the owner's contract or the `recovery.v_ace_*` views: this story creates no view over a public table and reads no public table (DP-05, ADR-010).
- No cross-schema read and no cross-schema key: every statement names `rwb_source_data` only, the login `rwb_source_data` holds no grant on any other `rwb_*` schema, and no constraint points at `public` or at another service's schema (DP-01, DP-02).
- One hop and 2 s timeout on every call to another service, and none is made at run time in this story (DP-11).
- The migration changes no data outside `rwb_source_data`, creates no constraint into schema `public`, never drops a table in PROD and is forward only (DP-15).
- The dictionary reads only `sys_objects`, `sys_fields` and `data_product`, all in `rwb_source_data`.
- The service publishes no event of its own; the only message it causes is the library write of `DecisionRecorded` on `rwb.decision-record.v1`, which carries no personal data (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record, one read path and one owner | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-01, FEAT-RDF-02 | All recovery processes | CTL-08; Principle 1; D-RCV-35 U1, U4 | TC-E1-001-01 to TC-E1-001-17 |
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Epic 2, 4; Program, 5.1 | FEAT-RDF-01 | All recovery processes | REQ-RDF-001; D-RCV-35 U1 | TC-E1-001-03 |

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
- The case list and its reconciliation tables in use (RWB-P1-E1002-APP, RWB-P1-E1011-APP), and the interaction ledger's writer (RWB-P1-E1066-APP, RWB-P1-E1067-APP).
- The other 74 tables of the estate, the schemas of the other 18 services and the DB stories that create them (RWB-PLT-NF06-DB).
- The data lake, `lake_copy_watermark` and the decision log copy (DP-17: no data lake; JOB-13 becomes continuous Kafka ingest in rwb-decision). Pre-existing DP-17 handling is not re-litigated here.
- Stage 2 data products for contracts, plans and treatments beyond their catalog rows (REQ-RDF-014, Epic 2; RWB-P1-E2010-APP).
