# Technical Specification — RWB-E1-001 Recovery tables for the 14 data products

| Field | Value |
|---|---|
| Story | RWB-E1-001 — Recovery tables for the 14 data products |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-010-epic-1-RWB-E1-001` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-001); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 001 Recovery tables for the 14 data products v1.md` |
| Upstream IDs | REQ-RDF-001; FEAT-RDF-01, FEAT-RDF-02; US-RWB-E1-001; CTL-08; DT02; DL41 ruled 2026-11-06 (D-RCV-29); DL42 ruled 2026-11-05 (D-RCV-28) |
| Status | `SUCCESS` — CLAR-001, CLAR-002 and CLAR-005 are resolved by the D-RCV-28/D-RCV-29 rulings |
| Prepared | 2026-11-04 |
| Regated | 2026-11-06 — Technical Specifier re-run after the decision-log rulings; clarifications resolved |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The pipeline log and `v_data_dictionary` are the only surfaces; story §15. |
| Logic In Scope | `YES` — schema creation, metadata seed, conformance test, catalog validation and apply. |
| API In Scope | `NO` — no new or changed endpoint. The catalog uses the existing P4 `POST /api/recovery/v1/admin/reference-loads` with `table = data_product`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | Flyway migration chain (RWB-E1-044); reference data service (RWB-E1-043); `sys_objects`, `sys_fields` (new); `data_product` (new); `v_data_dictionary` (new). |
| New Nodes Required | `YES` — `V0001__rwb_e1_001_recovery_schema.sql`, `DataDictionaryConformanceTest`, `DataProduct`, `DataProductRepository`, `DataProductCatalogHandler`. |
| Inherited Existing Behavior | Flyway naming and schema parameter (RWB-E1-044); `ReferenceTableHandler` contract and load/approve flow (RWB-E1-043); LOV-ROLE and LOV-REFRESH values. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every table and column has one dictionary row with BR Field ID, types, source and meaning. | SPEC-RWB-E1-001-002, 003, 007 | DIRECT | `sys_objects` and `sys_fields` are seeded by the migration; the conformance test compares both directions. | COVERED |
| BR2 | Recovery data is held in the 14 data products DP01 to DP14. | SPEC-RWB-E1-001-004, 015 | DIRECT | `data_product` holds one row per product; `sys_objects.data_product` is a foreign key. | COVERED |
| BR3 | Each data product has exactly one system of record and one named owner. | SPEC-RWB-E1-001-005, 016 | DIRECT | `system_of_record` is a single value; `owner_role` and `owner_user_id` are required on the catalog load. | COVERED |
| BR4 | Catalog values are a versioned data load; a file with an exception is refused whole. | SPEC-RWB-E1-001-005, 006, 010, 011 | DIRECT | `validate` writes nothing; `apply` runs in one transaction. | COVERED |
| BR5 | Where entities name more than one source (DP06, DP07, DP13), the catalog names one accountable system. | SPEC-RWB-E1-001-004, 016 | DIRECT | Seed values follow story §13; the DP06/DP07/DP13 choices are assumed under DL12. | COVERED |
| BR6 | Schema names come from parameters; one migration per story; forward only in production. | SPEC-RWB-E1-001-001, 014 | DIRECT | `${recoverySchema}` is `recovery` in every environment (D-RCV-28); baseline `V0001__rwb_e1_001_recovery_schema.sql`; no destructive change. | COVERED |
| BR7 | Personal fields carry `is_personal = true` so masking can read them. | SPEC-RWB-E1-001-013 | DIRECT | `sys_fields.is_personal` is populated by the dictionary seed. | COVERED |
| AC1 | The migration creates 44 tables and `loan_account` has 24 fields; the conformance test compares the full dictionary. | SPEC-RWB-E1-001-001, 002, 007 | RULE_LEVEL | Old AC1 was removed at the AC cleanup (4 November 2026); its substance is rule-level BR1 with exceptions X1, X2 and X3. The AC set follows the cleaned story (AC2, AC3, AC7–AC10). | COVERED |
| AC2 | `v_data_dictionary` returns DF-ACC-014 with types, source, product, refresh and owner. | SPEC-RWB-E1-001-003, 017 | DIRECT | The view joins `sys_fields`, `sys_objects` and `data_product`. | COVERED |
| AC3 | A 14-row catalog load writes 14 products, each with one source and owner; DP06 is CCMS/WEEKLY. | SPEC-RWB-E1-001-004, 006, 016 | DIRECT | `DataProductCatalogHandler.apply` writes all rows in one transaction. | COVERED |
| AC7 | A catalog row with two sources or no owner is refused whole. | SPEC-RWB-E1-001-005, 010 | DIRECT | MSG-P1-003 per failing row; no write. | COVERED |
| AC8 | A catalog with 13 rows and no DP09 is refused whole. | SPEC-RWB-E1-001-005, 010 | DIRECT | MSG-P1-004 names the missing products. | COVERED |
| AC9 | An owner role or refresh cycle outside its list is refused whole. | SPEC-RWB-E1-001-005, 010 | DIRECT | MSG-P1-007 with row number and allowed values. | COVERED |
| AC10 | The same catalog file loaded again writes nothing. | SPEC-RWB-E1-001-006, 011 | DIRECT | Content hash match returns MSG-P1-011. | COVERED |
| X1 | A migration statement fails. | SPEC-RWB-E1-001-008 | DIRECT | Rollback; pipeline names the statement. | COVERED |
| X2 | A column or type has no matching dictionary row. | SPEC-RWB-E1-001-007 | DIRECT | Conformance failure. | COVERED |
| X3 | The migration runs again. | SPEC-RWB-E1-001-009 | DIRECT | Flyway skip. | COVERED |
| X4 | A catalog row has no/multiple source or no owner. | SPEC-RWB-E1-001-005 | DIRECT | MSG-P1-003. | COVERED |
| X5 | The catalog does not hold DP01 to DP14. | SPEC-RWB-E1-001-005 | DIRECT | MSG-P1-004. | COVERED |
| X6 | A value is outside its list. | SPEC-RWB-E1-001-005 | DIRECT | MSG-P1-007. | COVERED |
| X7 | The same catalog file is loaded again. | SPEC-RWB-E1-001-011 | DIRECT | MSG-P1-011. | COVERED |
| X8 | A role without Reference data C loads the catalog. | SPEC-RWB-E1-001-012 | DIRECT | 403; MSG-P4-002; access log. | COVERED |

> **AC cleanup (4 November 2026):** the development-process criteria removed from story §7 are not mapped here. The remaining acceptance criteria are those in the current story. Old AC1 (schema deployed, 413/413 conformance) was removed at the cleanup; its substance is covered by BR1 and exceptions X1, X2 and X3, and the criteria numbering skips the removed IDs (AC2, AC3, AC7–AC10 remain).

> **Regate (6 November 2026):** the seed count and the seed mechanism are ruled (D-RCV-29); the migration name and placeholder are ruled (D-RCV-28). The dictionary seed is the full 108 `sys_objects` / 1,256 `sys_fields` set from Physical Schema v4.

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **the recovery tables for the 14 data products created in the ACE database, with a data dictionary and one system of record and one owner per data product**, so that **every later load has one target table and one accountable owner**.

This is a schema-and-metadata enabler. It creates the 41 product tables, the dictionary metadata and the product catalog; it creates no screen and no runtime endpoint. Later stories load the tables, and RWB-E1-064 exposes the dictionary through the API. The catalog is loaded through the existing reference-data path, not by a new endpoint.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | ACE pipeline deployment to DEV, then SIT. |
| Preconditions | RWB-E1-044 done (Flyway and `${recoverySchema}`); RWB-E1-043 done (`ReferenceTableHandler`); DEV/SIT databases exist; pipeline identity may migrate the recovery schema; RW-REFADM holds Reference data C; the catalog file carries a synthetic owner per product. |
| Input | `V0001__rwb_e1_001_recovery_schema.sql`; `sys_objects`/`sys_fields` seed (108 objects, 1,256 fields, D-RCV-29); 14-row `data_product` catalog file. |
| Output | 44 tables, 68 foreign keys, 76 indexes, append-only triggers, `v_data_dictionary`, the full dictionary seed (D-RCV-29) and 14 product rows. |
| Feature flag | `rwb.p1.data-catalog` covers the catalog handler. The migration is not behind a flag. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `data_product` | `product_code` | Seed DP01–DP14 | Catalog load | Unique; `varchar(25)` per TSD T3.1 and the physical schema (story says `varchar(4)`; see CLAR-004). |
| `data_product` | `product_name`, `definition` | Seed | Catalog load | Required. |
| `data_product` | `system_of_record` | Seed | Catalog load | Exactly one value; no semicolon list. |
| `data_product` | `owner_role` | Seed `RW-DATASTEW` | Catalog load | Must be in LOV-ROLE. |
| `data_product` | `owner_user_id` | Null in seed | Catalog load | Required by the load; one synthetic user per environment. |
| `data_product` | `refresh_cycle` | Seed | Catalog load | LOV-REFRESH: DAILY, WEEKLY, MONTHLY, ON_CHANGE. |
| `data_product` | `expected_by` | Seed | Catalog load | Free text; `08:00` daily, Monday `08:00` weekly (DL11, assumed). |
| `data_product` | `valid_from` | Load parameter | Catalog load | Required; one version in force per date. |
| `sys_objects` | `object_name` | Migration seed | Pipeline only | Unique; `data_product` foreign key. |
| `sys_fields` | `field_id`, `object_name`, `field_name` | Migration seed | Pipeline only | Unique per object and field; `field_id` is the BR Field ID. |
| `sys_fields` | `data_type`, `physical_type` | Migration seed | Pipeline only | Conformance test compares `physical_type` with `information_schema`. |
| `sys_fields` | `is_personal` | Migration seed | Pipeline only | True for every personal field; read by RWB-E1-016 and RWB-TE-004. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| No recovery schema | Pipeline applies 0001 | Migration succeeds | Schema at Flyway 0001 | 44 tables, metadata, catalog seed, view. |
| Flyway version 0001 | Pipeline applies 0001 | Checksum unchanged | Flyway 0001 | No table or row change. |
| No catalog version | RW-REFADM load + RW-DATASTEW confirm | 14 valid rows | First catalog version in force | 14 `data_product` rows. |
| Catalog version N | Same file hash loaded | Hash equals version in force | Catalog version N | MSG-P1-011; no write. |
| Catalog version N | New valid file | All checks pass | Catalog version N+1 | Previous version valid-to set to day before. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Migration statement fails | Whole migration rolls back; pipeline names the statement; no Flyway success row. | Pipeline log |
| X2 | Column without dictionary row, or physical type differs | Conformance test fails and names table, column and field ID. | Pipeline log |
| X3 | Migration already applied | Flyway skips; counts unchanged. | Flyway history |
| X4 | Catalog row with no/multiple source or no owner | Whole load refused; no row written. | MSG-P1-003 |
| X5 | Catalog not exactly DP01–DP14 | Whole load refused; missing products named. | MSG-P1-004 |
| X6 | Owner role or refresh cycle outside its list | Whole load refused; row and allowed values named. | MSG-P1-007 |
| X7 | Same catalog file again | No write; reported as already done. | MSG-P1-011 |
| X8 | Caller without Reference data C | 403; refusal in access log. | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/admin/reference-loads` (P4) with `table = data_product`; `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve` (P4). |
| Contract delta | None. The response is `ReferenceLoad`; the refusal is a 422 Problem with MSG-P1-003, MSG-P1-004 or MSG-P1-007. |
| Backward compatibility | Unchanged. |
| Authorization | Reference data C to load; Reference data U to confirm as owner; pipeline identity for the migration. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P1-011; 422 MSG-P1-003/004/007; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; the pipeline log and SQL view are the only surfaces. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-001; SPEC-RWB-E1-001-001..020 | New migration, conformance test, entity, repository and reference handler. | Positive, negative, boundary and error-path tests: 44 tables; 24 `loan_account` fields; 108/108 and 1,256/1,256 conformance; missing column; wrong type; repeat migration; each catalog refusal; repeat file; 403. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `V0001__rwb_e1_001_recovery_schema.sql` | Flyway migration | Creates 41 product tables, `sys_objects`, `sys_fields`, `data_product`, 68 FKs, 76 indexes, append-only triggers, `v_data_dictionary`; seeds 108 object and 1,256 field dictionary rows (D-RCV-29) and the 14 product rows. |
| `DataDictionaryConformanceTest` | Pipeline test | Compares `information_schema.columns` with `sys_fields` both ways, ignoring the 7 standard columns. |
| `DataProduct` | Entity | Maps `data_product`. |
| `DataProductRepository` | Repository | Reads and writes `data_product`. |
| `DataProductCatalogHandler` | Published interface implementation | `ReferenceTableHandler` for `data_product`: validate, apply. |

### Data and migration

- Creates the 41 data-product tables of the physical schema subset, plus `sys_objects`, `sys_fields` and `data_product` = 44 tables.
- `loan_account` has DF-ACC-001..021 and DF-ACC-029..031 (24 fields) plus the 7 standard columns. DF-ACC-029..031 are `dispute_open`, `settlement_booked_date` and `settlement_booked_amount` per TSD T3.1.
- `data_product.product_code` is `varchar(25)` with a unique constraint; the story's `varchar(4)` is a narrower duplicate (CLAR-004).
- Migration is one transaction. `data_product` is inserted before `sys_objects` because of the foreign key.
- The seed count is ruled (D-RCV-29, 2026-11-06): the migration seeds the full dictionary — 108 `sys_objects` and 1,256 `sys_fields` rows as held in Physical Schema v4 — so the dictionary is complete before the tables exist; later dictionary changes are reference loads through RWB-E1-043 (D-RCV-28).

### Rules

1. Validate the whole catalog file before writing: 14 products, one source, one owner, list values.
2. Apply all 14 rows in one transaction with the valid-from date.
3. Refuse the whole file on any row error; never write a partial catalog.
4. The conformance test fails the build on an extra column, a missing dictionary row or a physical-type mismatch.
5. A repeated file with the same content hash is reported and writes nothing.

### Transaction and events

- Migration: one database transaction; Flyway records version 0001 only on success.
- Catalog apply: one transaction for all 14 rows; a failure rolls back all rows.
- No event is published. The reference load response is the record of the change.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| ACE pipeline identity | Run migration and conformance test | DEV, SIT |
| RW-REFADM | Reference data C — load catalog | All |
| RW-DATASTEW | Reference data U — confirm catalog as owner | All |
| Developer / data steward | Read `v_data_dictionary` | DEV, SIT |
| Any other role | None | 403 MSG-P4-002 |

No personal data is written; owner user IDs are synthetic test users in DEV and SIT.

### Observability and operations

- Pipeline log: migration stage, failing statement, conformance result.
- Flyway history: version 0001, checksum, applied date.
- Catalog load: `ReferenceLoad` id, table, valid-from, status, row count.
- No runtime job, metric or alert in this story.

### Performance

- Migration and conformance test run inside the pipeline timeout; the conformance scan is over `information_schema` for the recovery schema only.
- No runtime query path; the dictionary view is read by developers and RWB-E1-064.

### Feature flag and rollback

- `rwb.p1.data-catalog` covers the handler. Off: the catalog load is refused; the schema remains.
- The migration is not behind a flag. Rollback is forward-only: a failed migration rolls back; an applied migration is not edited. A bad catalog version is superseded by the previous version through the reference-data rollback path.

### No UI change

No screen. SCR-40 Reference data arrives in E8; the dictionary endpoint arrives in RWB-E1-064.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-001-01 | BR1, BR6 | System | Empty DEV/SIT schema; `recoverySchema = recovery` | 44 tables; 24 `loan_account` fields; 108/108 and 1,256/1,256 conformance |
| TC-E1-001-02 | AC2, BR1 | System | Dictionary seed; DP01 catalog | DF-ACC-014 with NUMBER/integer, ALS source, DELAY_DAYS, DP01, DAILY, RW-DATASTEW, owner |
| TC-E1-001-03 | AC3, BR2, BR3, BR5 | System | 14-row catalog | 14 rows; one source and owner each; DP06 CCMS/WEEKLY |
| TC-E1-001-04 | X1 | System | Migration copy with failing `valuation` create | Stage fails; no tables; no Flyway success |
| TC-E1-001-05 | X2 | System | Extra `branch_code`; changed DF-ACC-021 type | Test fails with both messages |
| TC-E1-001-06 | X3 | System | SIT at 0001 | Flyway skip; 108/1,256 dictionary unchanged |
| TC-E1-001-07 | AC7, X4 | System | DP06 "CCMS; SVAF"; DP11 no owner | Whole load refused; MSG-P1-003 for both |
| TC-E1-001-08 | AC8, X5 | System | 13 rows, no DP09 | Whole load refused; MSG-P1-004 names DP09 |
| TC-E1-001-09 | AC9, X6 | System | DP04 `DP_OWNER`; DP05 `HOURLY` | Whole load refused; MSG-P1-007 rows 4 and 5 |
| TC-E1-001-10 | AC10, X7 | System | Same file twice | No write; MSG-P1-011 |
| TC-E1-001-11 | X8 | Security | RW-DATASTEW loads catalog | 403; MSG-P4-002; access log |
| TC-E1-001-12 | BR1, BR7 | Unit | Dictionary seed | Every personal field has `is_personal = true` |

## Guardrails

- No business value in code: product names, sources, owners and cycles come from the catalog file.
- No personal data in logs, tests or prompts; DEV/SIT owners are synthetic.
- No read of another module's tables; the dictionary reads only `sys_objects`, `sys_fields` and `data_product`.
- The migration changes nothing outside the recovery schema and never drops a table in production.

## Out of scope

- Freshness stamp (RWB-E1-015), access control and PDPA masking (RWB-E1-016), retention (RWB-E1-017).
- Stage 2 data products (REQ-RDF-014, Epic 2).
- The dictionary endpoint, field versions and data contracts (RWB-E1-064).
- The reference-data screen SCR-40 (Epic 8).

## Traceability

| Requirement ID | Requirement (short) | Feature | Rules | Test cases |
|---|---|---|---|---|
| REQ-RDF-001 | 14 data products, one system of record and one owner each | FEAT-RDF-01, FEAT-RDF-02 | CTL-08; DT02; DL12; D-RCV-28; D-RCV-29 | TC-E1-001-01..12 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR2, AC1, SPEC-002, 015 | Does the migration seed 41 `sys_objects` and 413 `sys_fields`, or 108 and 1,256? | The seed count and the dictionary conformance assertions. | **Ruled 2026-11-06 as D-RCV-29:** the baseline seeds the full recovery dictionary — 108 `sys_objects` and 1,256 `sys_fields` rows as held in Physical Schema v4 — so the dictionary is complete before the tables exist; supersedes the working recommendation A (41/413). | `RESOLVED` | SPEC-002, 015 |
| CLAR-002 | BR6; SPEC-001, 014 | Is the migration `V1_001__recovery_schema.sql` with `${recoverySchema}`, or `V1__rwb_e1_001_baseline.sql` with `${schema}`/`RWB_SCHEMA`? | The file name and placeholder; Flyway apply order. | **Ruled 2026-11-05 as D-RCV-28:** `V0001__rwb_e1_001_recovery_schema.sql` with `${recoverySchema}`; the schema is `recovery` in every environment; RWB-E1-044 ships no production migration file. | `RESOLVED` | SPEC-001, 014 |
| CLAR-003 | AC1; SPEC-001 | AC1 gives `loan_account` DF-ACC-029..031, but story §11 assigns DF-ACC-022..028 to `account_payment`. | The `loan_account` column set. | TSD T3.1 defines DF-ACC-029..031 as `dispute_open`, `settlement_booked_date`, `settlement_booked_amount` on `loan_account`. | `RESOLVED` | SPEC-001 |
| CLAR-004 | AC1, AC3; SPEC-004 | Story §13 says `data_product.product_code varchar(4)`; TSD T3.1 and the physical schema say `varchar(25)`. | Column width only; DP01–DP14 fit both. | Use `varchar(25)` per the data model; record the story text as a Low defect. | `RESOLVED` | SPEC-004 |
| CLAR-005 | BR1, BR2; SPEC-002 | E1-001 §4 inserts `sys_objects`/`sys_fields` in the migration; E1-044 §13 says those seed rows move to reference loads, not migrations. | Whether the dictionary exists at first deploy and whether the conformance test can pass. | **Ruled 2026-11-06 as D-RCV-29 with D-RCV-28:** the initial seed rows ship with the RWB-E1-001 baseline; the E1-044 story §12/§13 was corrected on 2026-11-06; later dictionary changes are reference loads through RWB-E1-043. | `RESOLVED` | SPEC-002 |
| CLAR-006 | AC1; SPEC-001 | AC1 says 44 tables; flow step 2 says 43 tables plus `data_product`. | Table count only. | 44 = 41 product tables + `sys_objects` + `sys_fields` + `data_product`. | `RESOLVED` | SPEC-001 |

`CLARIFICATION_STATUS: RESOLVED` — no open items. The D-RCV-28 and D-RCV-29 rulings are recorded in the
decision log and carried into the story, this spec and the re-run compliance validation.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New schema and metadata capability; no UI or API contract change; existing P4 reference-load endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new recovery schema, dictionary seed and catalog handler]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 7 acceptance criteria and 8 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Start the Implementation Planner on this specification.
```
