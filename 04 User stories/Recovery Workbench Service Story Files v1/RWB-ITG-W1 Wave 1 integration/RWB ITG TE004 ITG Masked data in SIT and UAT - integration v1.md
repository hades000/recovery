# RWB-ITG-TE004-ITG Masked data in SIT and UAT — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-TE-004 for the wave-1 integration epic. The monolith loader that refilled one `recovery` schema becomes a tool outside the ACE services that fills the 19 per-service schemas of the ACE database table by table, verifies every `is_personal` column in every schema before a single-step staging swap, and records its run in its own `tools.masked_copy_load` table; the reader path is the case contract of rwb-case with the masking policy of rwb-access, and no service reads another service's tables (DP-01, DP-08). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE004-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP08, DP13, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1065-APP, RWB-PLT-TE004-APP, RWB-P1-E1069-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019) |
| Status | Draft (realignment v1) |

### 1. Story

As a **QA integration engineer**, I want **the masked copy of RWB-TE-004 loaded and verified across the 19 per-service schemas of the ACE database in SIT and UAT — each table filled into the schema of the service that owns it, every `is_personal` column scanned in every schema before the swap, one staging-to-live swap per environment, and the masked case read back through the contracts of rwb-case, rwb-source-data and rwb-access**, so that **SIT and UAT run at production volume and with production data shapes while no customer value is exposed, and the masked copy is proven on the schema-per-service estate that will run it rather than on the single `recovery` schema of the monolith**.

### 2. Business rationale

SIT and UAT must show that loads, allocation, reconciliation and reports work at production volume and with production data shapes, which synthetic data does not prove. NFR-045 allows masked copies in user acceptance and forbids production data in development; the bank's PII service produces the masked copy under the Compliance masking rules, and RWB-TE-004 loads it into SIT and UAT only, refuses any copy that still holds a personal value, and keeps dates, keys and row counts unchanged so counts and reconciliations behave as in production.

In the target the store is no longer one `recovery` schema. The ACE database holds one schema and one login per service, with no cross-schema joins, views or foreign keys, and a boundary test in every build fails on any cross-schema reference (Arch v5 slides 29 and 41, ADR-014). The masked copy therefore lands table by table in 19 schemas `rwb_<name>`, each table in the schema of the service that owns it (DP-01), and the property the legacy story called "the same token joins" is no longer a join inside one schema: it is proven through each service's own contract — a case read on rwb-case, a customer and an account read on rwb-source-data — with the masking applied by rwb-access on the reader path (DP-08). The loader stays outside the ACE services, as the legacy story already required, and is a tool with its own `tools.masked_copy_load` table, so it never becomes a service that reads service schemas at runtime.

None of that is proven by any single service story. A table that lands in the wrong schema, a schema that is swapped while another is refused, a verifier that stops at the first schema, a mask that does not apply to the reader, and a copy that reaches DEV are all failures that only appear across the 19 schemas and the four contracts. This story builds and runs that proof in SIT and UAT, and it publishes no operation of its own.

### 3. Preconditions

- The ACE database holds the 19 Recovery schemas with one login each: `rwb_case`, `rwb_decision`, `rwb_access`, `rwb_deviation`, `rwb_valuation`, `rwb_treatment`, `rwb_guarantee`, `rwb_litigation`, `rwb_asset`, `rwb_debtsale`, `rwb_writeoff`, `rwb_document`, `rwb_comms`, `rwb_payment`, `rwb_partner`, `rwb_integration`, `rwb_source_data`, `rwb_reporting` and `rwb_agent`, each at the same Flyway version as the extract (Arch v5 slide 29; RWB-PLT-NF06-DB and the per-service DB stories).
- Each service login holds grants on its own schema only and no grant on any other schema, so a table written into the wrong schema is refused by the database and not only by the tool (Arch v5 slide 29; RWB-P1-E1069-APP for the boundary rule).
- RWB-PLT-TE004-APP is done: the masked-copy loader, the manifest validator, the masking verifier and the load-report writer exist as a build module outside the ACE service, with properties `rwb.maskedcopy.allowed-environments=SIT,UAT` and `rwb.maskedcopy.intake-container` per environment.
- RWB-P1-E1065-APP is done: the `is_personal` tags in `sys_fields` and the personal-data patterns of the synthetic-data verifier are available to the loader (DP-05, `sys_fields` is P1's).
- RWB-P1-E1069-APP is done: the ACE view contract, the boundary test and the data-dictionary surface exist, and the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` are in P1's schema (DP-05).
- The PII service delivers the masked extract per environment to the SIT or UAT intake container with a manifest: extract ID, business date, masking rule version and row count per table. The PII service is outside the source set and outside this story; its extract contract is Not specified in the source documents (GAP-0379; ASM-0547).
- The extract in hand is "PII-SIT-20261120" for business date 2026-11-19, with masking rule version "MASK-2026.11" in force (RWB-TE-004 sections 7 and 16).
- rwb-access answers the authorise call and holds the test roles used by SIT and UAT, with their masking policy rows in `masking_rule` (P4) and their letters as data (DP-08).
- The environment lists, the product groups and the masking reference rows are reference data read through rwb-case's reference-data contract, never values in the loader (DP-07).
- The table-to-schema map is Not specified in the source documents (GAP-0379; ASM-0547); under ASM-0547 the loader builds it from the Ownership Map and the per-service DB stories.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The integration run is written on Day 1 against the three integration stories and is run when they are in SIT; a fake is never used in their place.

### 4. Flow

1. Pipeline: reads the target environment, the intake container and the service list from configuration, and refuses to start when the environment is not SIT or UAT.
2. Harness: runs the preflight of section 13 — the 19 schemas and logins exist at the extract's Flyway version, the loader module is present, the reference lists resolve through the rwb-case contract, and P4 answers the authorise call; a missing element stops the run before any file is read.
3. Loader: reads the manifest and checks the extract ID against `tools.masked_copy_load`, the masking rule version against the version in force, and the schema version against every target schema.
4. Loader: runs the CTL-02 load checks on each file — business date, structure, control totals (row count per table), keys — with the manifest's 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903.
5. Loader: builds its table-to-schema map from the Ownership Map and the per-service DB stories (ASM-0547): `recovery_case`, `case_account` and `case_party` into `rwb_case`; `interaction`, `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext`, `sys_fields` and the other P1 tables into `rwb_source_data`; `document_field` and the other document tables into `rwb_document`; and every remaining table into the schema of its owner.
6. Loader: loads the files into a staging schema per target schema in one run, checks that the foreign keys resolve inside each schema, and holds the swap until every schema has passed.
7. MaskingVerifier: scans every column tagged `is_personal` in every one of the 19 staging schemas — not only `interaction` and `document_field` — for values that look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number or an email address.
8. Pipeline: on a verifier or load failure in any one schema, refuses the whole load, leaves the previous copy in every schema and reports the schema and the check that failed.
9. Loader: on success, swaps the staging schema for the live schema in one step per environment and writes the run to `tools.masked_copy_load`: extract ID, environment, business date, masking rule version, rows per table per schema and check results.
10. Harness: reads the masked case back through `GET /api/recovery/case/v1/cases/{caseId}` as a SIT test user of RW-TRIBE, with the authorise call of rwb-access in between, and reads the customer and the account of that case on rwb-source-data.
11. Harness: asserts that the same person token observed on the case read is the one on the customer read and the account read, that no service read touched another service's tables, and that no `is_personal` value in any schema is clear.
12. Harness: repeats the load of extract "PII-SIT-20261120" and asserts the skip with the earlier load named, starts a second load while the first runs and asserts the refusal with MSG-P2-006, and confirms the DEV guard before reading any file.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A personal column holds a value that looks personal in any of the 19 schemas | Load refused in full; the previous copy stays in every schema; the report names the schema, the table and the column | MSG-P1-002 | AC2 |
| X2 | Row count differs from the manifest in one schema | Load refused in full; the previous copy stays in every schema; the report names the schema and the check | MSG-P1-002 | AC3 |
| X3 | The target environment is DEV or PROD | Load refused before reading any file | MSG-P1-002 | AC5 |
| X4 | The same extract ID is loaded again | Load skipped; the report shows the earlier load from `tools.masked_copy_load` | None | AC1 |
| X5 | The manifest's masking rule version is not the version in force | Load refused in full | MSG-P1-002 | AC1 |
| X6 | A second load starts while one runs in the same environment | Second start refused by the per-environment lock | MSG-P2-006 | AC1 |
| X7 | A table maps to no owning schema, or to two schemas | Preflight stops the run; no schema is loaded and no swap happens | None | AC3 |
| X8 | A reader without the case right calls the masked case | rwb-access refuses the authorise call and the read answers 403 | MSG-P4-002 | AC5 |
| X9 | A service tries to read another service's tables | The database refuses the statement, and the boundary test of RWB-P1-E1069-APP fails the build | None | AC4 |

X1 to X6 are the exception paths of the legacy story carried onto the 19 schemas; X7 and X9 are the schema-per-service paths the monolith did not have (DP-01); X8 is the reader path of DP-08 in testable form.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test project of its own; it needs the loader module, the 19 schemas, the extract and the four contracts, and it owns no schema and no service code |
| Negotiable | Fixture size, wait intervals, report layout and check order are configuration; the masking rule version, the extract ID, the business date, the counts and the message IDs are fixed by the legacy story |
| Valuable | Proves across 19 schemas and four contracts what no single service story can prove: every table in its owner's schema, every personal column verified, one swap, all-or-nothing failure, no cross-schema read |
| Estimable | One test project, five test classes, three fixtures, one fault step, one repeat and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a row per schema, a run row in `tools.masked_copy_load`, a refusal, a response and a boundary-test result |

### 7. Acceptance criteria

```gherkin
Feature: Masked data in SIT and UAT, proven across the 19 per-service schemas

  Background:
    Given masking rule version "MASK-2026.11" is in force
    Given extract "PII-SIT-20261120" for business date 2026-11-19 has a manifest with masking rule version "MASK-2026.11"
    Given the manifest lists 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903, with row counts per product
    Given the 19 per-service schemas of the ACE database exist with one login each

  Scenario: AC1 One run fills every table into its owner's schema and swaps once per environment (new, D-RCV-60)
    Given the loader maps each manifest table to its owning schema from the Ownership Map and the per-service DB stories
    When the masked copy is loaded into SIT
    Then recovery_case, case_account and case_party land in rwb_case, interaction, party_ext, contact_point_ext, account_ext and valuation_ext land in rwb_source_data, document_field lands in rwb_document, and every other table lands in the schema of its owner
    Then the count per table and per product equals the manifest: case_account 28,119 against Mortgage 12,256, Hire purchase 12,960 and SSME 2,903
    Then no table is written into a schema whose login has no grant on it, and the loads of the 19 schemas are held in staging until every schema has passed
    Then the staging schemas are swapped for the live schemas in one step and the run is recorded in tools.masked_copy_load with extract ID, environment, business date, masking rule version and rows per table per schema
    When extract "PII-SIT-20261120" is loaded into SIT again
    Then the system skips the load and the report names the load of 2026-11-20 from tools.masked_copy_load
    When a second load into SIT starts while one runs
    Then the system refuses the second start with MSG-P2-006 and the first load is unaffected

  Scenario: AC2 Every is_personal column in every schema is verified before the swap (new, D-RCV-60)
    Given interaction row 4,512 of the extract holds a 13-digit value with a valid national ID check digit in summary
    When the copy is verified before the swap in SIT
    Then the verifier scans every column tagged is_personal in all 19 staging schemas, including sys_fields.is_personal as the tag source
    Then the system refuses the load in full with MSG-P1-002 and check "unmasked value in interaction.summary"
    Then the report names the schema rwb_source_data, the table interaction, the column summary and the row 4,512
    Then the previous SIT copy stays in use in every one of the 19 schemas and no schema is swapped

  Scenario: AC3 A failure in any one schema refuses the load in all 19 schemas (new, D-RCV-60)
    Given the case_account file holds 28,118 rows while the manifest lists 28,119
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "Control totals case_account 28,118 against 28,119"
    Then the report names the schema rwb_case and the check, and no other schema reports success
    Then the previous SIT copy stays in use in every one of the 19 schemas, including the 18 schemas whose own files passed
    When the load is retried with the corrected file
    Then the whole load runs again from the preflight and no staging schema of the refused run is reused

  Scenario: AC4 The same token joins through the contracts, never through a cross-schema join (new, D-RCV-60)
    Given the masked copy is loaded in UAT
    When a test user reads the case through GET /api/recovery/case/v1/cases/{caseId}
    Then the case read returns the case with its parties and accounts, and each person reference is a token, not a clear value
    When the same test user reads the customer through GET /api/recovery/source-data/v1/customers/{id} with the person reference of that case
    And reads the account through GET /api/recovery/source-data/v1/accounts/{id} with the account reference of that case
    Then the token returned on the case read is the token returned on the customer read and on the account read
    Then every read is one hop to the owning service and no service read another service's tables
    Then the boundary test of RWB-P1-E1069-APP passes, and a query that joins rwb_case to rwb_source_data is refused by the database and by the build

  Scenario: AC5 SIT and UAT only, and the mask holds on the reader path (new, D-RCV-60)
    Given the target environment is DEV
    When the masked copy load starts
    Then the system refuses it with MSG-P1-002 and check "masked copies load only into SIT and UAT"
    Then the system reads no file and writes no schema
    Given the masked copy is loaded in UAT and masking rule version "MASK-2026.11" is in force
    When a test user of RW-TRIBE reads a masked case through the gateway-bff composite route to GET /api/recovery/case/v1/cases/{caseId}
    Then rwb-access answers the authorise call and the masking policy of rwb-access masks every is_personal field of the response
    Then no national ID number, Thai mobile number or email address is present in the response, and the freshness read of GET /api/recovery/source-data/v1/data-products/freshness names the business date 2026-11-19
    When test user "U-6104" holds a role without the case right and calls the same path
    Then rwb-access refuses and the answer is 403 with MSG-P4-002
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; SIT and UAT use masked copies only | NFR-045; CTL-11 |
| BR2 | Every field tagged personal is masked or tokenized under the masking rules in force | Masking rules reference table; DL26; `sys_fields.is_personal` |
| BR3 | A copy with any personal value left in it is refused in full | CTL-11; DQ check "Refuse the load" |
| BR4 | Dates and keys are not masked; counts equal the manifest | CTL-02; REC-01, REC-02 |
| BR5 | The same customer gets the same token in every table and every schema, so the contracts return one token | Mapping rule "Personal data" (s2t.txt); RWB-TE-004 BR5 |
| BR6 | With no masking rule loaded, every personal field is replaced by a token | DL26 ("every personal field stays masked") |
| BR7 | One schema and one login per service; a table is written only into its owner's schema, and no service reads another service's tables, views or foreign keys | Arch v5 slides 29 and 41; ADR-014; DP-01 |
| BR8 | The loader is a tool outside the ACE services, runs only in SIT and UAT, loads into staging and swaps in one step, and records the run in its own `tools.masked_copy_load` table | RWB-TE-004 section 13; DP-01 |
| BR9 | A failure in any one of the 19 schemas refuses the whole load and leaves the previous copy in every schema | This story; ASM-0548 |
| BR10 | A reader sees the masked case through the owner's contract with the masking policy of rwb-access applied; no service applies the mask by reading another service's masking table | DP-08; Arch v5 slides 14 and 41 |

### 9. State transitions

None for a case status. This story changes no case status; it changes the state of the masked copy load in the pipeline.

| Item | States |
|---|---|
| Load run | Not started, preflight, running, verifying, swapped, refused, skipped |
| Schema in the run | Staging, verified, swapped; on any failure, discarded and the previous live schema untouched |
| Masked copy of an environment | Previous copy in use, new copy in staging, new copy in use; never a mixed estate |
| `tools.masked_copy_load` row | Written once per run: Loaded, Refused or Skipped, with the check results |
| Extract ID | Unseen, loaded, or already loaded (a repeat is skipped) |
| Boundary test | Pass (no cross-schema reference), or fail with the offending reference named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the harness, the fixtures, the fault step and the run report |
| Platform administrator (RW-PLATADM) | Starts the load in SIT or UAT; owns the intake containers and the environment lock |
| Compliance and PDPA officer (RW-COMPLY) | Owns the masking rules and their version (DL26) and receives a refused-load report |
| Tribe lead and squad members (RW-TRIBE) | Run SIT and UAT tests on the masked copy with their test users' rights |
| Data load identity (SY-DATALOAD) | The identity the loader runs under in SIT and UAT; grants on the staging schemas of the run only |
| Service teams (P1, P3, P4 and each per-service DB story) | Own their schema, their grants, their contract and the tables the loader fills |
| ACE database administrator | Owns the 19 schemas, the 19 logins and the staging schemas of each environment |
| No role | May read another service's tables, run a copy in DEV or PROD, or swap one schema on its own |

The fault step of AC2 and AC3 runs on a test extract in SIT only; it injects a value into the extract file before the load and never writes to a service schema directly.

### 11. Data

| BR Field ID | Entity | Schema (owner) | Field | Read or write |
|---|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | `rwb_case` (P3) | all fields | Write (staging), read |
| DF-CAS-024 to DF-CAS-029 | `case_account` | `rwb_case` (P3) | all fields | Write (staging), read |
| DF-CAS-030 to DF-CAS-035 | `case_party` | `rwb_case` (P3) | all fields | Write (staging), read |
| DF-INT-001 to DF-INT-013 | `interaction` | `rwb_source_data` (P1) | all fields | Write (staging), read |
| DF-DOC-012 to DF-DOC-017 | `document_field` | `rwb_document` (P5) | all fields | Write (staging), read |
| DF-EXT-001 to DF-EXT-012 | `party_ext` | `rwb_source_data` (P1) | all fields | Write (staging), read |
| DF-EXT-013 to DF-EXT-026 | `contact_point_ext` | `rwb_source_data` (P1) | all fields | Write (staging), read |
| DF-REF-105 | `sys_fields` | `rwb_source_data` (P1) | `is_personal` | Read |
| DF-REF-101 to DF-REF-104 | `reference_row`, `reference_version` | `rwb_case` (P3) | list code, value, version | Read (through the contract) |
| Not stated in RWB-TE-004 | `masking_rule` | `rwb_access` (P4) | rule version in force | Read (through the contract) |
| None | `tool_run` in schema `tools` | the loader (outside the 19 services) | extract ID, environment, business date, masking rule version, result | Write, read |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-TE-004; `account_ext` and `valuation_ext` are P1's four extension tables and load the same way (DP-05), and the field IDs of the extract's remaining tables are the table's own dictionary entries.

The per-schema table list the loader must fill is Not specified in the source documents (GAP-0379; ASM-0547). The manifest is per table and not per owning service, no source maps the tables of the extract to the 19 schemas, and the PII service's extract contract is outside the source set. Under ASM-0547 the loader builds the table-to-schema map from the Ownership Map and the per-service DB stories, and every table of the extract resolves to exactly one schema.

The harness owns no schema and no table of a service. It writes tables only through the loader in SIT and UAT staging schemas, reads them back through the four contracts of section 12.2, and records its own run in `tools.masked_copy_load`.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test project and the loader a tool outside the ACE services; neither provides a REST operation, and the names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` — are not used by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The masked case read of a SIT or UAT test user: parties, accounts and tokens |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The case right and the masking policy check of the reader, and the refusal of a role without the right |
| GET | `/api/recovery/source-data/v1/customers/{id}` | P1 rwb-source-data | The customer reference of the case, with the token |
| GET | `/api/recovery/source-data/v1/accounts/{id}` | P1 rwb-source-data | The account reference of the case, with the owner token |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The freshness of the loaded copy, business date 2026-11-19 |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The environment lists, the product groups and the masking reference rows (DP-07) |

Every call is one hop to the owning service on its own base with the 2 s client budget (DP-11, DP-13); the harness calls no service through another service. The reader reaches the case through the gateway-bff composite route (DP-19).

The table-to-schema map and the PII extract contract are Not specified in the source documents (GAP-0379; ASM-0547); the map is held as configuration of the loader (ASM-0547) and no operation of the PII service is called by this story.

#### 12.3 Events published

None. The loader is a tool outside the services and publishes no business event; the run is recorded in `tools.masked_copy_load`, and no event is produced for a load, a swap or a refusal.

#### 12.4 Events consumed

None. The harness waits on no topic: the load is synchronous in the pipeline, its result is the `tools.masked_copy_load` row, and the reader assertions are made against the contracts of 12.2. The case and source-data events that other stories assert are out of scope here.

#### 12.5 Workflows and activities

None. No Temporal workflow, activity or Nexus operation is started or awaited: the loader is a batch tool of the pipeline and not a service worker, and the two service task queues it would otherwise use — `rwb-case` and `rwb-source-data` — are exercised only through their REST contracts.

#### 12.6 Schedules

None. The masked copy load is a manual pipeline stage started by the platform administrator for SIT or UAT and is not a scheduled job and not in the production job list (RWB-TE-004 section 12). It is not registered in `rwb-integration` and no Schedule is created or moved.

#### 12.7 Tables owned

None. The harness owns no table and no schema. The loader's own run table `tools.masked_copy_load` lives in schema `tools`, outside the 19 service schemas, and is P1's tool table (RWB-PLT-TE004-APP); `rwb_integration` is not written by this story.

#### 12.8 Contract fakes

None. This is the integration level: the real P3, P1 and P4 services, the real ACE schemas and the real extract replace the contract fakes of the app stories. The PII service is an outside system that supplies a file; it is not faked and not called over a service contract.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 6 | The case read, the authorise call, the customer and account reads, the freshness read and the reference-list read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | None | The loader publishes no event and the harness listens to no topic |
| Temporal | None | None | No workflow, no activity, no Schedule; `rwb-case` and `rwb-source-data` are called over REST only |
| File | None | 1 file set per environment | The masked extract files and their manifest from the PII service in the SIT or UAT intake container |

### 13. Solution plan

**Deliverables.** One test project `integration/recovery-w1/masked-copy`, with the five test classes `MultiSchemaLoadIT`, `PersonalColumnScanIT`, `AllOrNothingIT`, `TokenThroughContractsIT` and `EnvironmentAndReaderIT`, the extract fixtures, the fault step and the run report writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight, run order, report and exit code |
| SchemaMap | Configuration | The table-to-schema map from the Ownership Map and the per-service DB stories (ASM-0547) |
| LoadDriver | Service | Starts the loader for the environment and reads the `tools.masked_copy_load` row of the run |
| SchemaProbe | Service | Asserts the row counts, the keys and the grants of each of the 19 schemas against the manifest |
| PersonalColumnScan | Service | Injects the value of interaction row 4,512 into the test extract, runs the verifier and asserts the refusal and the untouched schemas |
| AllOrNothingProbe | Service | Cuts the case_account file to 28,118 rows, asserts the refusal in all 19 schemas and the retry from the preflight |
| TokenProbe | Service | Compares the token of the case read with the customer read and the account read, and asserts that no cross-schema query is possible |
| ReaderProbe | Service | Calls the case path as RW-TRIBE and as a role without the right, through the authorise call, and asserts the masking and MSG-P4-002 |
| ReportWriter | Service | One row per test case, with the schema, the table, the check and the evidence |

**Database.** None of its own. The loader writes the staging schemas of the run and `tools.masked_copy_load`; the harness writes nothing into a service schema and never reads one directly (DP-01).

**Configuration and reference data**

- The environment, the intake container, the 19 schema names and the loader module, all as configuration.
- The table-to-schema map (ASM-0547) and the manifest of extract "PII-SIT-20261120".
- The masking rule version "MASK-2026.11", read as reference data through the rwb-case contract (DP-07), with the authoritative rows in `masking_rule` (P4).
- The product groups Mortgage, Hire purchase and SSME and the environment lists, read through the same contract.
- The 2 s client budget, the per-environment lock and the report layout.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, `account_ext` | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C and X dependencies the DPs name stay with the service, platform and operations stories this harness proves; this story carries no H, C or X dependency and its I list names the three stories whose behaviour it exercises (Template and Rules §R5.4: I never blocks a build).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Masked extract SIT | Extract "PII-SIT-20261120", business date 2026-11-19, MASK-2026.11, 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960, SSME 2,903 | AC1, AC3, TC-TE-004-01-ITG, TC-TE-004-03-ITG |
| Injected personal value | The same extract with a 13-digit value with a valid check digit in `interaction.summary` row 4,512 | AC2, TC-TE-004-02-ITG |
| Short case_account file | The same extract with 28,118 rows in the case_account file | AC3, TC-TE-004-03-ITG |
| Second copy of the extract | The same extract ID delivered twice, and a second start while one runs | AC1, TC-TE-004-05-ITG, TC-TE-004-07-ITG |
| Masking rule versions | Manifests with MASK-2026.11 and MASK-2026.10 | AC1, TC-TE-004-06-ITG |
| Role set | RW-TRIBE and a test role without the case right, test user "U-6104" | AC5, TC-TE-004-08-ITG |

**Run order.** Preflight; the DEV guard (AC5, first part); the SIT load of the full extract with the schema probes (AC1); the repeat and the second start (AC1); the injected value (AC2); the short file and the retry (AC3); the UAT load and the token reads through the three contracts (AC4); the reader checks as RW-TRIBE and as the role without the right (AC5); cleanup of the staging schemas of failed runs. A failing step stops the run and the report names the criterion, the schema, the check and the evidence.

**Done when.** The 13 test cases of section 16 pass, extract "PII-SIT-20261120" is loaded in SIT and in UAT with 28,119 case accounts and one `tools.masked_copy_load` row per environment, the verifier has scanned every `is_personal` column in all 19 schemas, a failure in one schema has refused the whole load with the previous copy intact in all 19, and the token of the case read matches the customer and account reads with no cross-schema query possible.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | The masked copy is refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P2-006 | A load starts while one runs | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P4-002 | A test user without the right reads the copy | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-TE-004; the story adds no message text. Report lines of the harness are for developers and are not part of the message standard. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the harness renders nothing. The platform administrator and the squads read the load report in the pipeline, and a test user sees the masked copy through the normal SIT and UAT screens, which reach the case through the gateway-bff composite route and the case contract of rwb-case (DP-19). Personal fields appear as tokens or masked values on those screens, with the mask applied by rwb-access (DP-08). The states the harness observes are the load, schema and copy states of section 9.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-004-01-ITG | legacy AC1, BR2, BR4, BR5 | Integration | Masked extract PII-SIT-20261120 with 28,119 case accounts, loaded into the 19 schemas of SIT |
| TC-TE-004-02-ITG | legacy AC2, BR3 | Integration | Injected value with a valid check digit in interaction row 4,512 of the test extract |
| TC-TE-004-03-ITG | legacy AC3, BR4 | Integration | case_account file with 28,118 rows against the manifest's 28,119 |
| TC-TE-004-04-ITG | legacy AC4, BR1 | Integration | Target environment DEV, with the loader pointed at the SIT intake container |
| TC-TE-004-05-ITG | legacy AC5 | Integration | Extract PII-SIT-20261120 loaded into SIT twice |
| TC-TE-004-06-ITG | legacy AC6, BR6 | Integration | Manifest with MASK-2026.10 against MASK-2026.11 in force |
| TC-TE-004-07-ITG | legacy AC7 | Integration | Two loads into SIT at once, on the per-environment lock |
| TC-TE-004-08-ITG | legacy Access, BR10 | Integration | SIT test user "U-6104" with a role without the case right; 403 with MSG-P4-002 |
| TC-ITG-TE004-01 | AC1, BR4, BR7, BR8 | Integration | One run over the 19 schemas: table-to-schema map, manifest totals, one swap per environment and the tools.masked_copy_load row |
| TC-ITG-TE004-02 | AC2, BR2, BR3 | Integration | Every is_personal column in all 19 schemas scanned; interaction row 4,512 refused with MSG-P1-002 |
| TC-ITG-TE004-03 | AC3, BR3, BR9 | End to end | case_account at 28,118 rows; the whole load refused and the previous copy intact in all 19 schemas, then the retry |
| TC-ITG-TE004-04 | AC4, BR5, BR7 | Integration | Case, customer and account reads compared for one token; the boundary test and a refused cross-schema join |
| TC-ITG-TE004-05 | AC5, BR1, BR10 | End to end | DEV guard refused before any file; UAT reader masked through the gateway-bff route and the authorise call |

The legacy acceptance criteria of RWB-TE-004 are owned by RWB-PLT-TE004-APP, the app story of the same legacy key, and are re-exercised here end to end across the 19 schemas; the legacy test case IDs are kept as ITG copies with the suffix `-ITG`, and the new criteria AC1 to AC5 carry TC-ITG-TE004-01 to TC-ITG-TE004-05.

### 17. Guardrails

- No business value in code: the masking rules and their version belong to Compliance, the allowed environments are properties, and the product groups and environment lists are reference data read through the rwb-case contract (DP-07).
- No personal data in logs, events, workflow inputs, fixtures or the report: the run record holds counts, totals, schema names and check names, never a value, and the test extracts are built from masked or synthetic data.
- Each table is written only into its owner's schema and no service reads another service's tables, views or foreign keys (DP-01); the boundary test is part of the run and a cross-schema reference fails it (RWB-P1-E1069-APP).
- The loader stays a tool outside the ACE services and never becomes a runtime dependency of a service; it runs only in SIT and UAT, and no copy is made from SIT or UAT to another environment.
- One swap per environment, and never a partial estate: a failure in any schema refuses the whole load and leaves the previous copy in every schema (BR9, ASM-0548).
- The verifier scans every `is_personal` column in every schema before the swap — not the two tables the legacy story named — so a new personal column in a new service is covered by construction (ASM-0548).
- The mask is applied by rwb-access on the reader path and is asserted on the contract response, never by reading `masking_rule` from a service schema (DP-08).
- The harness never uses production data and never points at a production namespace.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | The 19 schemas and logins, `tools.masked_copy_load`, the case read and the authorise call, the reference-list read | TC-TE-004-01-ITG, TC-TE-004-04-ITG, TC-ITG-TE004-01, TC-ITG-TE004-03, TC-ITG-TE004-05 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | `masking_rule` (P4) through the authorise call, the case read and the gateway-bff composite route, the customer and account reads | TC-TE-004-02-ITG, TC-TE-004-08-ITG, TC-ITG-TE004-02, TC-ITG-TE004-04, TC-ITG-TE004-05 |

### 19. Out of scope

- The masked-copy loader, its manifest validator, its masking verifier and its load-report writer (RWB-PLT-TE004-APP); this story exercises them and owns none of them.
- The 19 schemas, the 19 logins and their grants (RWB-PLT-NF06-DB and the per-service DB stories).
- The ACE view contract, the extension tables and the boundary test (RWB-P1-E1069-APP); this story exercises the boundary rule and owns none of it.
- The `is_personal` tags and the synthetic-data patterns (RWB-P1-E1065-APP).
- The masking policy, the roles and the authorise decision (RWB-P4-E1037-APP); the case contract and its reference data (RWB-P3-CON stories); the customer, account and freshness contracts (RWB-P1-CON stories).
- The PII service, which the bank runs and which produces the extract and its manifest; its extract contract is outside the source set (GAP-0379) and no external dependency is carried for it.
- The masking rule values per field and per role (DL26, Compliance) and masking on the screens themselves (RWB-E1-037).
- Synthetic data in DEV (RWB-E1-065) and the masked debt sale data tape (FEAT-DBS-03, Epic 5).
