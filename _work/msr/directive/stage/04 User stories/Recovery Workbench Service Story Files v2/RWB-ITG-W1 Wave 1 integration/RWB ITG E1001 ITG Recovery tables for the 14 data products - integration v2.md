# RWB-ITG-E1001-ITG Recovery tables for the 14 data products — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1001-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Wave conflict | Wave 1 kept over the Architecture v5 wave 2 for rwb-payment (one conflict per service and business epic). The wave plan records rwb-payment delivery in wave 1 under its service epic, and the rwb-payment service wave governs its later stories. Release unchanged and tentative. Wave reviewed at the verification loop. |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-001 |
| Legacy disposition | Must change |
| Build status | In build |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP11, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P1-E1001-APP, RWB-P4-E1001-APP, RWB-P7-E1001-APP, RWB-P8-E1001-APP |
| Contract dependencies | Not specified in the source documents (DOR-RWB-ITG-E1001-ITG-21) |
| Service baseline (platform contracts, named in preconditions) | RWB-PLT-E1044-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-N001-CON |
| Field-row handover and login | Login: rwb-decision login (DP-02). Field rows are declared as a build artefact of RWB-P1-E1001-APP, proved by the conformance test. Migration file and sequence fixed at merge under D-RCV-28. Constraint and index names follow the platform naming convention with the section 13 read paths as leading columns. Field IDs of the standard columns: Not specified in the source documents (GAP-1279). |
| Integration dependencies | RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP, RWB-P8-E1001-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-005, FR-PLT-006, FR-PLT-007) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-001 is realigned. The built migration and its 92-table estate are kept, and this wave-1 integration story proves that the estate now spans the 19 per-service `rwb_*` schemas while the dictionary, the data product catalog and the read paths still work end to end against the real services. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 56 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **test lead of the integration harness (RW-TRIBE)**, I want **a wave-1 integration run that proves the 92 tables of the 14 data products resolve one owning `rwb_*` schema each across the 19 services, and that the data dictionary, the data product catalog and the read paths still work end to end against the real services**, so that **the schema split of RWB-E1-001 is accepted with evidence before wave 1 leaves integration, and no later wave builds on a table estate that only works in a single recovery schema**.

### 2. Business rationale

RWB-E1-001 put 92 tables (the 88 Workbench tables and the four extension tables of DF-EXT-001 to DF-EXT-049), 122 `sys_objects` rows and 1,366 `sys_fields` rows into one recovery schema with the read model `v_data_dictionary` and the catalog `data_product`. That estate is built and stays built. The 92 is the version 6 monolith count, which the split replaces; the Ownership Map sheet Tables governs ownership of the 93 target tables: 87 Workbench tables and 6 platform library tables. What changes is where it lives: each of the 19 services now writes its own schema `rwb_<name>` with its own login and its own Flyway sequence (DP-01, DP-02, DP-15), and no service reads another service's tables (DP-11: a contract, one hop, 2 s timeout). The split is delivered by RWB-PLT-NF06-DB and the per-service DB stories; this story does not build it. The view SQL, the three helper functions and the conformance test are rwb-source-data's application slice; the login, grants, view owner and four extension tables are its database slice; and the 19-login proof is this story's wave 1 integration slice.

What nothing else proves is that the estate still behaves as one dictionary and one catalog after the split. The dictionary is a read model over `sys_objects`, `sys_fields` and `data_product`, which the Ownership Map keeps together in rwb-source-data; the catalog is a versioned data load that enters through the rwb-case reference-data contract (DP-07), is applied by the rwb-source-data handler, is authorised by rwb-access (DP-06 to DP-07 boundary) and leaves one hash-chained entry in the rwb-decision ledger (DP-03). Three services, one transaction each, no shared table. If the wiring or the naming drifts, it fails here, in SIT, with a named assertion — before a case officer reads a case through a contract that no longer matches the dictionary.

The measure this run serves is the one the legacy story serves: the ACE batch is complete when the Workbench reads it on 99 percent of days, and every read and every freshness stamp is resolved against this dictionary and this catalog. The run is part of the integration harness RWB-ITG-W1J01-ITG and follows its topology, its run lock and its report.

### 3. Preconditions

- The nine wave-1 services are deployed to SIT from their own pipelines, each with its own schema and login, and each schema carries its own Flyway baseline (DP-15, RWB-PLT-E1044-CON).
- The migrated SIT data set exists: the 14 `data_product` seed rows, the 122 `sys_objects` rows and the 1,366 `sys_fields` rows, carried from the built RWB-E1-001 migration and replayed into the owning schema by the per-service DB stories.
- The 30 `recovery.v_ace_*` views exist in the ACE database and are readable by the rwb-source-data login only (DP-05).
- The reference data administrator (RW-REFADM) holds Reference data C in SIT, and a reader login may query the dictionary read model of rwb-source-data.
- The catalog load file for the 14 data products exists as a fixture, with table code `data_product`, the three legacy system-of-record strings and synthetic owner user IDs for SIT.
- The integration harness holds its run lock, its Kafka topics and its Temporal namespace `rwb-recovery` in SIT.
- No build dependency and no contract dependency: the run executes against the deployed services, their real contracts and their real schemas. Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Harness: takes the SIT run lock, reads `/health` on the nine wave-1 services and records each service's Flyway version and schema name.
2. Harness: reads `information_schema.tables` for the 19 `rwb_*` schemas and builds the table-to-schema resolution for the 92 tables of the estate.
3. Harness: compares the resolution with the estate list of the legacy story and fails on a missing table, a duplicated table name in two schemas, or one of the twenty tables that left the estate.
4. Harness: queries the dictionary read model `v_data_dictionary` in rwb-source-data for entity `v_ace_account` and field `days_past_due`, and for entity `account_ext` and field `dispute_open`, and records the owning schema and owning service beside every row.
5. Harness: posts the catalog fixture to rwb-case on `POST /api/recovery/case/v1/admin/reference-loads` with table code `data_product`, valid from 2026-11-30, as the reference data administrator.
6. rwb-case: asks rwb-access on `POST /api/recovery/access/v1/authorise` for Reference data C with the caller's role and scope before it accepts the load.
7. rwb-case: forwards the accepted load to rwb-source-data; `DataProductCatalogHandler.validate` refuses or accepts the whole file and writes nothing.
8. rwb-source-data: `DataProductCatalogHandler.apply` writes the 14 rows of DP01 to DP14 in one transaction in `rwb_source_data` and returns the row count; the service writes its local decision record in the same transaction and publishes `rwb.decision.DecisionRecorded.v1` through its outbox.
9. rwb-decision: appends one entry to the central ledger from `rwb.decision-record.v1`; the harness reads it back on `GET /api/recovery/decision/v1/decision-log`.
10. Harness: reads the dictionary again and asserts the 14 rows, the three system-of-record strings of DP01, DP03 and DP06 and their refresh cycles.
11. Harness: posts the same catalog file a second time and asserts that nothing is written and that the ledger holds exactly one entry for the load.
12. Harness: exercises the read paths on the migrated SIT data through the owners' contracts: `GET /api/recovery/source-data/v1/accounts/{id}` and `GET /api/recovery/payment/v1/cases/{caseId}/payments`.
13. Harness: runs the boundary test over the 19 schemas, every foreign key, every grant and every view definition.
14. Harness: publishes the run report, releases the lock and hands the report to the wave-1 exit review.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A table of the estate sits in no schema, in two schemas, or a table that left the estate is found | The run fails and names each table and schema pair | None (run report) | AC12 |
| X2 | A service cannot reach another service, or a call exceeds the 2 s budget | The step fails and the report names the caller, the callee, the operation and the elapsed time | None (run report) | AC13, AC14 |
| X3 | The catalog row names no system of record, two systems, a bare source name, or no owner user ID | The whole load is refused; the run asserts the refusal and the message | MSG-P1-003 | AC7 |
| X4 | The catalog file does not hold exactly the 14 products DP01 to DP14 | The whole load is refused | MSG-P1-004 | AC3 |
| X5 | A catalog row names an owner role or a refresh cycle outside its list | The whole load is refused | MSG-P1-007 | AC3 |
| X6 | The same catalog file is posted again | Nothing is written, the answer is the repeat message, and the ledger keeps one entry | MSG-P1-011 | AC15 |
| X7 | A caller without Reference data C posts the load | rwb-access refuses, rwb-case answers 403 and the refusal is in the access log | MSG-P4-002 | AC13 |
| X8 | A cross-schema foreign key, a read of another service's table, or a second reader of the ACE views is found | The boundary test fails and names the constraint, the query or the grant | None (run report) | AC14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency and no contract dependency; it runs against the deployed wave-1 services in SIT and their real contracts |
| Negotiable | The fixtures, the assertion order and the report shape are settled inside the harness; the 92 tables, the 14 products and the three system-of-record strings are fixed by the legacy story and are not changed here |
| Valuable | It is the only place where the split estate is seen as one dictionary, one catalog and one set of read paths across services |
| Estimable | One suite, four fixtures, one boundary test, one run order and one report |
| Small | Fits one sprint with the wave-1 services already deployed |
| Testable | One assertion per criterion; a failing assertion names the service, the schema and the object |

### 7. Acceptance criteria

```gherkin
Feature: The 92-table estate of the 14 data products across the 19 service schemas

  Background:
    Given the nine wave-1 services are deployed to SIT with their own rwb_* schemas and their own Flyway baselines
    Given the 92 tables of the estate are the 88 Workbench tables and the four extension tables
    Given the integration harness holds the SIT run lock and the real services answer, no contract fake is used

  Scenario: AC2 Dictionary published (legacy RWB-E1-001 AC2)
    Given the data dictionary and the data product seed loaded by the migration, and the catalog loaded for DP01
    When a developer queries v_data_dictionary for entity "v_ace_account" and field "days_past_due"
    Then the row holds field ID "DF-ACE-018", data type "NUMBER", physical type "integer"
    Then source system "ACE", source field "public.account.delay_days"
    Then data product "DP01", system of record "ACE (ingested from ALS)", refresh cycle "DAILY", owner role "RW-DATASTEW" and the owner user ID of DP01
    Then the row for entity "account_ext" and field "dispute_open" holds field ID "DF-EXT-028", data type "BOOLEAN", physical type "boolean", source system "Workbench" and data product "DP01"

  Scenario: AC3 One system of record (legacy RWB-E1-001 AC3)
    Given a catalog load file with the 14 rows DP01 to DP14, each with one system of record and one owner user ID
    When the reference data administrator loads it with valid from 2026-11-30
    Then data_product holds 14 rows
    Then each row has a definition, exactly one system of record and one owner user ID
    Then DP01 names system of record "ACE (ingested from ALS)" and refresh cycle "DAILY"
    Then DP03 names system of record "Recovery Workbench" and refresh cycle "ON_CHANGE"
    Then DP06 names system of record "ACE (ingested from CCMS, SVAF, AMIS and RPS)", refresh cycle "WEEKLY" and expected by "MON 08:00"

  Scenario: AC7 Catalog row with two systems of record is refused (legacy RWB-E1-001 AC7)
    Given a catalog load file in which DP06 names system of record "ACE (ingested from CCMS); SVAF"
    Given DP11 has no owner user ID
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-003 for DP06 and for DP11
    Then data_product keeps the rows of the version in force

  Scenario: AC12 Every one of the 92 tables resolves to exactly one owning schema (new, D-RCV-60)
    Given the 19 rwb_* schemas created by their own Flyway baselines
    When the harness reads information_schema.tables for the 19 schemas
    Then it finds 92 tables, the 88 Workbench tables and the four extension tables party_ext, contact_point_ext, account_ext and valuation_ext
    Then each of the 92 tables sits in exactly one schema and no table name sits in two schemas
    Then it finds none of the 20 tables that left the estate: loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory and tracker_row
    Then rwb_source_data holds data_product, sys_objects and sys_fields and no other schema holds a table of those three names
    When the harness queries v_data_dictionary for entity "v_ace_account" and field "days_past_due"
    Then the row names the owning schema rwb_source_data and the owning service rwb-source-data beside field ID "DF-ACE-018"
    Then the row names the owning schema rwb_source_data and the owning service rwb-source-data beside field ID "DF-EXT-028"
    Then a table of rwb_case read the same way names rwb_case and rwb-case, and so on for every schema of the estate

  Scenario: AC13 The catalog load runs end to end across three services and the ledger (new, D-RCV-60)
    Given the reference data administrator holds Reference data C in SIT
    Given the catalog fixture of the 14 data products with table code data_product and valid from 2026-11-30
    When the administrator posts it to rwb-case on POST /api/recovery/case/v1/admin/reference-loads
    Then rwb-case asks rwb-access on POST /api/recovery/access/v1/authorise for Reference data C and the answer is granted
    Then rwb-case forwards the load to rwb-source-data and DataProductCatalogHandler.validate accepts the whole file
    Then DataProductCatalogHandler.apply writes the 14 rows of DP01 to DP14 in one transaction in rwb_source_data and returns the row count 14
    Then rwb-source-data writes its local decision record and publishes rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1
    Then rwb-decision holds one ledger entry for the load and GET /api/recovery/decision/v1/decision-log returns it
    Then the load answer carries no error message and data_product holds 14 rows

  Scenario: AC14 The boundary holds across the 19 schemas (new, D-RCV-60)
    Given the 19 schemas and their own logins
    When the boundary test reads every foreign key, every grant and every view definition of the 19 rwb_* schemas
    Then no foreign key points from one rwb_* schema to another and no constraint references a table in schema public
    Then no service login holds a write grant on another service's schema
    Then the only object that selects recovery.v_ace_* sits in rwb_source_data and it selects the 30 views
    Then no other schema holds a view or a query text over a recovery.v_ace_* view
    Then a call from one service to another goes to the owner's base with a timeout of 2 s and never to a schema

  Scenario: AC15 The same catalog file loaded twice writes nothing the second time (new, D-RCV-60)
    Given the load of AC13 is complete and its content hash is the version in force
    When the reference data administrator posts the same file again
    Then the answer carries MSG-P1-011 and no data_product row changes
    Then rwb-decision still holds exactly one ledger entry for the load
    Then data_product still holds 14 rows and one version in force for 2026-11-30
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every table column and every view column in the recovery estate has exactly one row in the data dictionary, with its BR Field ID, types, source system and meaning | Logical Data Model and Data Dictionary; sys_fields |
| BR2 | Workbench data is held in the 14 data products DP01 to DP14 | REQ-RDF-001; sys_objects.data_product |
| BR3 | Each data product has exactly one system of record, written "ACE (ingested from X)" for source data, "Recovery Workbench" for Workbench records, or, where the product holds both, one sentence that names ACE with its sources and the Recovery Workbench; and one named owner | REQ-RDF-001; D-RCV-35 U1 |
| BR4 | The catalog values are a versioned data load, changed without a code release; a load with an exception is refused in full | Principle 1; DT02; CTL-08 |
| BR5 | Where a product is fed by several sources (DP06, DP07, DP13), its one system of record names ACE and every source it ingests; a bare source name is refused because no source reaches the Workbench except through ACE | D-RCV-35; ADR-010 |
| BR8 | The recovery estate holds no copy of source data. No constraint references a table in schema public, and a link to an ACE record is a varchar(255) business key with no foreign key | D-RCV-35 U4; ADR-010; Data Tier Map section 1 |
| BR10 | Each of the 92 tables has exactly one owning `rwb_*` schema and exactly one writing login; a table name appears in one schema only, and the dictionary read model names the owning schema and the owning service of every object | DP-01; Arch v5 slides 20, 41 and 45 |
| BR11 | Services talk to each other by contract, not by table: no cross-schema foreign key, no read of another service's tables, one hop with a 2 s timeout, and the boundary test fails the build on any violation | DP-01, DP-11; ADR-014, ADR-020; Arch v5 slide 45 |
| BR12 | Every service writes its decision record locally in the same transaction as its state change and publishes it through its outbox to `rwb.decision-record.v1`; the inbox dedupes, so one load leaves one ledger entry and a repeated load leaves none | DP-03, DP-09; ADR-015, ADR-022; Temporal and Drools design slide 16 |

BR6, BR7 and BR9 of the legacy story are not re-proven here: BR6 (schema names from parameters, one migration per story) belongs to RWB-PLT-NF06-DB and the per-service DB stories, BR7 (personal fields flagged in the dictionary) belongs to the dictionary and masking stories, and BR9 (the baseline seeds the dictionary before the views exist) belongs to RWB-P1-E1064-APP and the view story. The IDs and their texts are unchanged in the legacy story, and the copied test cases keep their legacy Covers values, so a row still names BR6, BR7 or BR9 where the legacy named it; the run proves the part of that rule in scope and the owning story proves the rest.

### 9. State transitions

None for case status: this story changes no `recovery_case` row and takes no business decision. The states the run asserts are:

| From | To | Trigger |
|---|---|---|
| Service baseline not applied | Service baseline applied | Each service's Flyway baseline runs in its own schema before the run |
| Catalog version none | Catalog version 2026-11-30 in force | The 14 rows are applied in one transaction and the version becomes current |
| Catalog version 2026-11-30 in force | Catalog version 2026-11-30 in force (no change) | The same file is posted again; nothing is written and the answer is MSG-P1-011 |
| Ledger without the load | Ledger with one entry for the load | `rwb.decision.DecisionRecorded.v1` is consumed once; a repeated load adds no entry |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, integration and test roles | Start a run, read the report, change a fixture through a reviewed pull request |
| RW-REFADM, reference data administrator | Posts the catalog load (Reference data C) |
| RW-DATASTEW, data steward and data product owner | Confirms the catalog version as its owner (Reference data U); cannot load it |
| RW-PLATADM, platform administrator | Books the SIT slot, restores the migrated data set after the run |
| Role without Reference data C | Refused with MSG-P4-002 on the catalog load, asserted as an expected refusal |

No approval level from the delegation of authority applies; the run takes no business decision.

### 11. Data

Table per owning schema, from the Ownership Map only. Every read of another service's data in this story is read through the owner's contract; the dictionary is read through the owner's read model. The schema table below lists tables by owning schema, not fields, so its rows carry no BR Field ID; the field-level rows with their IDs are in the second table. `v_data_dictionary` is the view `rwb_source_data.v_data_dictionary` over `sys_fields`, `sys_objects` and `data_product` (Physical Schema v7 README). `information_schema`, `pg_constraint` and `pg_views` are database catalogs read by the harness, not Workbench entities, and carry no BR Field ID.

| Schema | Service | Tables of the estate in this schema | Read in this run |
|---|---|---|---|
| rwb_source_data | P1 rwb-source-data | data_product, sys_objects, sys_fields, sys_field_version, data_contract, data_product_access, data_product_load, party_ext, contact_point_ext, account_ext, valuation_ext, interaction, efs_ledger_outcome, reconciliation_result, dp_treatment, dp_guarantee_claim | Read through the owner's contract; the dictionary read model `v_data_dictionary` is read as published by the owner |
| rwb_case | P3 rwb-case | recovery_case, case_account, case_party, case_entry_exclusion, queue, queue_member, queue_measure, task, timer, assignment, parameter_catalog, parameter_value, reference_row, reference_version, lov_value | Read through the owner's contract; the load enters through `POST /api/recovery/case/v1/admin/reference-loads` |
| rwb_decision | P7 rwb-decision | decision_log_entry, approval, rule_package, rule_package_version, rule_row, rule_test_case | Read through the owner's contract on `GET /api/recovery/decision/v1/decision-log` |
| rwb_access | P4 rwb-access | role, permission, delegation_limit, masking_rule, role_conflict (exactly these five authority tables; lov_value sits in rwb_case, the four rule tables in rwb_decision and partner_user in rwb_partner, which supersedes the module view of TSD P4 v3) | Called on `POST /api/recovery/access/v1/authorise`; no table read |
| rwb_payment | P8 rwb-payment | the proceeds, matching, fee and booking tables of the module | Read through the owner's contract on the case payments operation |
| the other fourteen schemas | P2, P5, P6, P9, P10, S1 to S9 | their own tables of the 92 | Not read here; each is asserted to exist and to belong to one owner only |

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-070 to DF-REF-079 | data_product | all 10 fields | Read 14 rows; written only by the owner's handler through the load |
| DF-REF-087 to DF-REF-093 | sys_objects | all 7 fields | Read 122 rows |
| DF-REF-094 to DF-REF-110 | sys_fields | all 17 fields | Read 1,366 rows |
| DF-EXT-001 to DF-EXT-049 | party_ext, contact_point_ext, account_ext, valuation_ext | all 49 fields | Read, through the dictionary |
| DF-CAS, DF-WRK, DF-TRT, DF-LEG, DF-PRT, DF-SAL, DF-INT, DF-DOC, DF-DEC, DF-FIN, DF-REF, DF-OPS, DF-RPT and DF-AGT prefixes | the 85 other Workbench tables | 979 fields | Read as object and field rows of the dictionary; no row of these tables is read |
| DF-ACE-018 | v_ace_account.days_past_due | one field | Read through the dictionary read model |
| DF-EXT-028 | account_ext.dispute_open | one field | Read through the dictionary read model |

The 92 tables hold 1,062 fields and the 30 views add 304, so the dictionary holds 122 objects and 1,366 fields; the run asserts those counts once, from the dictionary, not from the tables.

**Shape of the rwb_decision tables (GAP-1280).** `rule_row` is built with the 21 fields that the LDM fields sheet lists (DF-REF-001 to DF-REF-015, DF-REF-052 to DF-REF-054 and DF-REF-296 to DF-REF-298). No `rule_test_case.package_version_id` is created. `approval.case_id` and `approval.delegation_limit_id` are kept as values with no foreign key (DP-01), and the five foreign keys of the schema stay inside rwb_decision.

**Field lists held as placeholders (GAP-1512).** The field lists, types and keys of `data_contract`, `dp_treatment`, `dp_guarantee_claim` and `efs_ledger_outcome` are placeholders in this version: Not specified in the source documents (GAP-1512). They are fixed at the technical specification review before wave 2. The Stage 2 copies `dp_treatment` and `dp_guarantee_claim` are not spent before the contracts, plans and treatments events exist.

The dictionary carries 122 `sys_objects` rows: 98 name a data product and 24 carry none, the 13 OPS objects, the 8 AGT objects and the 3 RPT objects. The per-service DB stories assign each of those 24 operational objects to its service schema (GAP-0333). The object-by-object assignment is Not specified in the source documents (GAP-0333; ASM-0427). The run therefore asserts the owning schema of the 92 tables and of every object that names a data product, and records the 24 as an open list to be resolved by the DB stories; it does not fail on them.

### 12. Contract

This is an integration story: it publishes nothing and consumes the real contracts.

#### 12.1 REST operations provided

None (integration story; no operation is published).

#### 12.2 REST operations consumed

Owner from the Ownership Map; base per service (DP-13).

| Method | Path | Owner | Use in the run |
|---|---|---|---|
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | The catalog load with table code `data_product`; the entry point of AC13 |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Reference data C check for the caller, called by rwb-case; granted and refused answers |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The one ledger entry of the load and the absence of a second one |
| GET | `/api/recovery/source-data/v1/accounts/{id}` | P1 rwb-source-data | A read path over the extension tables after the split |
| GET | `/api/recovery/payment/v1/cases/{caseId}/payments` | P8 rwb-payment | A read path of a wave-2 service over the same case, on the migrated data |

Every call goes to the owner's base, one hop, with a 2 s timeout, and none of them names another service's schema.

#### 12.3 Events published

None (no business event is produced by this story; the events asserted are in 12.4).

#### 12.4 Events consumed

The run consumes and asserts the events of the services it exercises; it produces none.

| Event | Topic | Owner | What the run asserts |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | The business date and the freshness summary arrive once per business date, with the CloudEvents 1.0 envelope and no personal data |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 | One message per load with the rule and version reference, the final call and the decided time, keyed so the ledger keeps the order |
| `rwb.source-data.AceDataReady.v1` (any message on the topic) | `rwb.source-data.events.v1` | P1 | The topic name, the record key and the envelope of the owner's topic are the ones the wave-1 services subscribe to; the retry and `.dlt` topics exist |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AceIngestCheck | Workflow, started by `AceDataReady` | `rwb-source-data` | Business date in; freshness and completeness summary out; the run reads its result before it loads the catalog |
| the ledger consumer of `rwb.decision-record.v1` | Consumer inside the service, not a workflow of this story | `rwb-decision` | One append per decision message, deduped through the inbox; the run asserts the entry, not the implementation |

No workflow is started by the harness itself; the harness observes the two queues it depends on.

#### 12.6 Schedules

| Schedule | Cadence | Owner | What the run touches |
|---|---|---|---|
| Chain check | 02:00, `rwb-decision` (JOB-14) | P7 | The run reads the last chain-check result and asserts that it covers the ledger entry the load produced; it never starts the schedule |

No schedule is created or changed by this story.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

The rwb-source-data contract fake supplies the Given and test-data lines that read ACE views or extension tables. For every other read and call, the ITG run replaces the contract fake with the real service: rwb-access stub v1 (Users Roles and Permissions v5, sheet Authorise contract, A7) and the rwb-case, rwb-decision, rwb-payment and rwb-source-data contract fakes. Published contract fake library version: Not specified in the source documents (DOR-RWB-ITG-E1001-ITG-22).

Contract version the story builds against: version 5.0.0 of rwb-access.yaml, rwb-case.yaml, rwb-decision.yaml, rwb-payment.yaml and rwb-source-data.yaml in Recovery Workbench API Specification v5.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 5 consumed | Catalog load, authorise, decision log and two read paths; one hop, 2 s timeout |
| Kafka | 0 published, 3 observed | `rwb.source-data.AceDataReady.v1`, `rwb.decision.DecisionRecorded.v1` and the owner topic `rwb.source-data.events.v1` |
| Temporal | 2 queues touched, 1 workflow observed | `rwb-source-data` (AceIngestCheck), `rwb-decision` (ledger consumer and chain check) |
| File | None | The catalog fixture is read by the harness by hand, not by a file interface |

**Topic retry and sizing (GAP-2062).** The target for every topic is retry at 1 min, 10 min and 1 h, then `.dlt` with an alert. Only `rwb.payment.events.v1` is sized in the architecture (12 partitions, replication factor 3, 7 days retention; Architecture v5 slide 22). Its 12 partitions are read as the default partition count until RWB-PLT-EVT sets the count per service with the owning services. The per-topic sizing of the other topics stays an open point.

### 13. Solution plan

**Deliverable.** The wave-1 estate and catalog suite of the integration harness RWB-ITG-W1J01-ITG, folder `itg/wave1`, package `<ACE base package>.recovery.itg.wave1`. It is not deployed as a service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| EstateResolutionTest | Test | Reads `information_schema` for the 19 schemas and resolves every one of the 92 tables to one schema; fails on a missing table, a duplicated name or a table that left the estate |
| DictionaryContractTest | Test | Queries the dictionary read model for the two legacy rows and for the owning schema and service of every object; asserts the 122 objects and 1,366 fields once |
| CatalogLoadJourney | Test | Posts the fixture to rwb-case, follows the authorise answer, the handler result, the local decision record, the published event and the ledger entry |
| CatalogRepeatTest | Test | Posts the same file again and asserts MSG-P1-011, no write and one ledger entry |
| BoundaryTest | Test | Reads every foreign key, grant and view definition of the 19 schemas; fails the build on a cross-schema foreign key, a write grant outside the owner, a table read across services or a second reader of `recovery.v_ace_*` |
| RunReport | Service | Publishes the report per assertion with the service, the schema and the object named |

**Fixtures**

| Fixture | Content |
|---|---|
| catalog-2026-11-30.csv | The 14 rows DP01 to DP14 of the legacy seed table, the three system-of-record strings of DP01, DP03 and DP06, the refresh cycles DAILY, ON_CHANGE and WEEKLY, expected by 08:00, as it changes and MON 08:00, synthetic SIT owner user IDs |
| catalog-two-systems.csv | DP06 with "ACE (ingested from CCMS); SVAF" and DP11 without an owner user ID, for AC7 |
| catalog-bare-source.csv | DP06 with a bare "CCMS", for the legacy refusal |
| estate-92.csv | The estate list: the 88 Workbench tables, the four extension tables and the 20 tables that left |
| V<seq>__rwb_p4_e1001_access_schema.sql | rwb_access baseline migration. The four-digit sequence is taken at merge in the rwb-access pipeline and is later than every service-baseline version, never 0001 of the legacy line. |

**Migrated SIT data.** The migrated data set of the wave-1 DB stories: the 14 `data_product` seed rows, the 122 `sys_objects` rows and the 1,366 `sys_fields` rows, each in its owning schema, plus a case with one account and one payment for the two read paths. The harness owns no data; it restores the set after the run.

**Topology.** All nine wave-1 services plus rwb-payment run in SIT from their own pipelines, with their own schemas, logins, topics and task queues, and their real contracts. No WireMock, no stub, no seed injected into a table by the harness: a write happens only through an owner's operation, so the run proves the operations and not the tables.

**Boundary test.** One query against `information_schema` and `pg_constraint` per schema plus the view definitions of `pg_views`, and one grant review of `information_schema.role_table_grants`. The single cross-schema read allowed is the read-only grant on the rwb-source-data dictionary read model: it is the published dictionary, not a business table, and it is the one exception DP-01 accepts for a read model.

**Run order.** Lock, health and Flyway versions, estate resolution, dictionary rows, catalog journey, ledger assertion, repeat, read paths, boundary, report, unlock. The run stops at the first failed stage and the report names the stage.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON (held by the service stories) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON (held by the service stories) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON (held by the service stories) |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON (held by the service stories) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON (held by the service stories) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON (held by the platform edge story) |

The story carries no H and no C dependency: DP-03, DP-06, DP-07, DP-14, DP-15 and DP-19 resolve to contract work inside the service stories, and this run only observes their result. DP-11 resolves to the one-hop rule the boundary test asserts.

**Build steps**

1. Write the estate list fixture and EstateResolutionTest; prove it fails on a table in two schemas and on a table that left the estate.
2. Write the schema version and health step of the run.
3. Write DictionaryContractTest for the two legacy rows and for the owning schema and service of every object.
4. Write CatalogLoadJourney and prove it fails when the rwb-access answer is refused.
5. Add the ledger assertion and the local decision-record assertion.
6. Write CatalogRepeatTest and move it inside the journey so one run proves AC13 and AC15 in order.
7. Write BoundaryTest and prove it fails on a planted cross-schema foreign key, a planted cross-schema select and a second `recovery.v_ace_*` reader.
8. Add the run to the wave-1 exit gate and run it on the wave-1 build.

**Done when.** Every assertion of section 16 passes on the wave-1 build in SIT, the report names the 19 schemas and the 92 tables, the catalog load and the repeat are proven in one run, the boundary test passes with no exception beyond the dictionary read model, and the 24 operational objects of section 11 are recorded for the DB stories.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-003 | Catalog row with no system of record, more than one, or no owner | {product} must have exactly one system of record and one named owner. |
| MSG-P1-004 | Catalog file without exactly DP01 to DP14 | The catalog must hold the 14 data products DP01 to DP14. Missing: {products}. |
| MSG-P1-007 | Catalog value outside its list | Row {row}: {field} must be one of {values}. |
| MSG-P1-011 | Same catalog file loaded again | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without Reference data C | You cannot {action} here. Your role does not include it. |

The run asserts these texts as the services return them; it never restates them in a fixture. The report findings are for the release team and are not part of the message standard.

### 15. Screens and states

No screen in this story. The report is read by the wave-1 exit review. The dictionary is read through the owner's read model and the catalog screen and the dictionary endpoint belong to other stories; nothing is rendered here and no screen state is asserted.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-001-11-ITG | Access | Integration | RW-DATASTEW calls `POST /api/recovery/case/v1/admin/reference-loads` with table data_product; refused with MSG-P4-002 |
| TC-E1-001-01-ITG | AC1, BR1, BR6, BR8 (run by RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP or RWB-P8-E1001-APP) | Contract | Empty SIT schemas at their baselines; schema parameter; a planted foreign key into schema public |
| TC-E1-001-02-ITG | AC2, BR1 | Integration | Dictionary from the migrated set; catalog loaded for DP01 |
| TC-E1-001-03-ITG | AC3, BR2, BR3, BR5 | End to end | Catalog fixture of 14 rows from the legacy seed table, posted to rwb-case and applied by rwb-source-data |
| TC-E1-001-04-ITG | AC4 (run by RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP or RWB-P8-E1001-APP) | Integration | A service baseline stopped part way in SIT; its schema left without the tables of that baseline |
| TC-E1-001-05-ITG | AC5, BR1 (run by RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP or RWB-P8-E1001-APP) | Integration | A column with no dictionary row and a changed physical type on DF-EXT-028, added in a branch |
| TC-E1-001-06-ITG | AC6 (run by RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP or RWB-P8-E1001-APP) | Integration | SIT schemas at their applied baseline; the run repeats the baseline step |
| TC-E1-001-07-ITG | AC7, BR3, BR4 | Integration | Catalog fixture with DP06 naming two systems and DP11 with no owner |
| TC-E1-001-08-ITG | AC8, BR2, BR4 (run by RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP or RWB-P8-E1001-APP) | Integration | Catalog fixture of 13 rows without DP09 |
| TC-E1-001-09-ITG | AC9, BR4 (run by RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP or RWB-P8-E1001-APP) | Integration | Catalog fixture with owner role DP_OWNER and refresh cycle HOURLY |
| TC-E1-001-10-ITG | AC10, BR4 (run by RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP or RWB-P8-E1001-APP) | Integration | The same catalog file posted twice in one run |
| TC-E1-001-12-ITG | AC11, BR3, BR5 (run by RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP or RWB-P8-E1001-APP) | Integration | Catalog fixture with DP06 naming "CCMS" |
| TC-ITG-E1001-01 | AC12, BR10 | Integration | The 19 schemas; the estate list of 92 tables; the 20 tables that left; the rwb_access baseline migration `V<seq>__rwb_p4_e1001_access_schema.sql`, asserted to have a version later than every service-baseline version and never 0001 of the legacy line |
| TC-ITG-E1001-02 | AC13, BR12 | End to end | Catalog fixture; RW-REFADM with Reference data C; the ledger read after the load |
| TC-ITG-E1001-03 | AC14, BR10, BR11 | Contract | Every foreign key, grant and view definition of the 19 schemas; a planted cross-schema key, a planted cross-schema select and a second `recovery.v_ace_*` reader |
| TC-ITG-E1001-04 | AC15, BR12 | Integration | The catalog fixture posted twice; the ledger count after the second post |

The ACs of this legacy key that this story does not own are owned by RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP and RWB-P8-E1001-APP and are re-exercised here only inside the end-to-end run.

### 17. Guardrails

- No business value in code or in a fixture beyond the legacy seed: the product names, definitions, systems of record, owners and refresh cycles are read from the catalog load, and the fixture copies the legacy seed table.
- No personal data in logs, reports, events or prompts: the run uses the masked SIT data set and the report holds table, schema, operation and message identifiers only.
- No read of another service's table: the run reads through the owners' contracts, and the one read model it reads is the published dictionary (DP-01, DP-11).
- The run never writes a table directly: a write happens only through the owner's operation, so a broken operation cannot be hidden by a seed.
- The boundary test is never relaxed per environment; a violation is fixed in the service that caused it.
- The run never touches UAT or production and never starts a Schedule.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record, one read path and one owner | The 14 `data_product` rows through the reference-data contract; the dictionary read model over `data_product`, `sys_objects` and `sys_fields`; the owning schema and service of every object | TC-ITG-E1001-01, TC-ITG-E1001-02, TC-E1-001-02-ITG, TC-E1-001-03-ITG, TC-E1-001-07-ITG, TC-E1-001-12-ITG |
| REQ-RDF-014 | Stage-2 data products for contracts, plans and treatments, each with one system of record | DP04 and DP14 rows of the catalog and their `data_product` and `sys_fields` rows in the dictionary | TC-ITG-E1001-01, TC-E1-001-03-ITG |
| ADR-014 | Schema and login per service in ACE PostgreSQL | The 19 schemas, their logins and the boundary test | TC-ITG-E1001-01, TC-ITG-E1001-03, TC-E1-001-01-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed operations and the elapsed-time assertion | TC-ITG-E1001-02, TC-ITG-E1001-03 |
| ADR-022 | Local decision record plus central ledger | The local record, `rwb.decision.DecisionRecorded.v1` and the one ledger entry | TC-ITG-E1001-02, TC-ITG-E1001-04 |

### 19. Out of scope

- The DB split work itself: RWB-PLT-NF06-DB and the per-service DB stories, including which schema holds the 24 operational objects (GAP-0333).
- The physical schema files, `recovery_views.sql` and the per-service Flyway files.
- The dictionary endpoint, field versions and data contracts with each system owner (RWB-P1-E1064-APP).
- The catalog screen and the catalog entry maintenance (the platform edge and reference-data screen stories).
- Every service's own build, including RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP and RWB-P8-E1001-APP.
- The 30 read-only ACE views and their grants (the view story), and the freshness stamp per data product.
- Retention and archive rules, and the stage-2 data products beyond their catalog rows.
