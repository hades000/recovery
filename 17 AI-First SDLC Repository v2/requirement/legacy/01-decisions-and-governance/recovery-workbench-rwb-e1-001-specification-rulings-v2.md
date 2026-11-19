<!-- source: 01 Decisions and governance/Recovery Workbench RWB-E1-001 Specification Rulings v2.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `01 Decisions and governance/Recovery Workbench RWB-E1-001 Specification Rulings v2.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-001 Specification Rulings

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Document | Recovery Workbench RWB-E1-001 Specification Rulings v2 |
| Superseded by | Counts superseded by D-RCV-35 (section 0) |
| Scope | The four source conflicts in RWB-E1-001 found by the specification re-run of 10 November 2026 against Recovery Workbench Physical Schema v4.sql, plus the conformance corrections that ride with them; re-based on Physical Schema v5 and D-RCV-35 (section 0) |
| Status | Proposed - for approval at the specification gate before RWB-E1-001 enters build. v2 re-bases the counts and the systems of record on D-RCV-35; the rulings are unchanged |
| Decision owner | Recovery tech lead with the data architect (the same owner that took D-RCV-29) |
| Amends | D-RCV-29 |
| Related | D-RCV-28; D-RCV-35; DL43 (open, needed 2026-11-21); DL41 (ruled); DL18 (open, needed 2026-11-30); Story Defects register v2 rows 10 and 11 |
| Sources examined | Recovery Workbench Physical Schema v4.sql; Logical Data Model and Data Dictionary v6.xlsx; Conceptual Data Model v5.xlsx; Data Ownership and Stewardship v2.xlsx; Reference Data and Lists of Values v3.xlsx; Delegation of Authority Matrix v2.xlsx; Decision Log v8.xlsx; stories RWB-E1-001, RWB-E1-016, RWB-E1-038, RWB-E1-043, RWB-E1-064; Build Notes Epic 1 v4 |

Because RWB-E1-001 has not been built, each ruling fixes the root cause in the source document rather than deferring a defect. Nothing in this pack changes a runtime code decision; every edit is a document, DDL or seed-data change.

## 0. Re-base note for v2

This version carries the four rulings into Physical Schema v5 and the ACE read path. The copy-table counts this document was written against - 44 tables, 533 conformance fields, 108 `sys_objects` and 1,256 `sys_fields` - are superseded by D-RCV-35 (U1 to U5). The schema is now 92 tables, 30 `recovery.v_ace_*` views, 122 `sys_objects` and 1,366 `sys_fields`, and the 20 copy, load and tracker tables have left it.

The rulings R1 to R4 and their reasoning stand. R1, R3 and R4 are applied in Physical Schema v5, and R4 seeds its 14 definitions from the Conceptual Data Model v6. Systems of record are re-worded "ACE (ingested from X)", because ACE is the store the Workbench reads. Where sections 2 and 6 to 10 still quote the v4 counts, they are the record of the 10 November re-run, not the live figures.

## 1. Rulings at a glance

| # | Conflict | Ruling | Key effect |
|---|---|---|---|
| R1 | 33 sys_objects rows carry AGT/OPS/RPT, which the 14-row data_product catalog cannot hold | sys_objects.data_product becomes nullable; the 33 operational rows are seeded with NULL; fk_sys_objects_data_product is created in V0001 | The FK ships on day one; AC1, AC3, AC6, AC8 and D-RCV-29 counts all hold |
| R2 | v_data_dictionary returns owner_role NULL, failing AC2 | The view reads owner_role from data_product, per story section 12; both system_of_record views are added in the same pass | The physical schema was the defect, not the story |
| R3 | All 24 delegation_limit baseline rows violate NOT NULL limit_version and regulation_item | delegation_limit is empty in V0001; the 24 placeholder rows are removed; content is owned by RWB-E1-038 loading DOA-2026.11 through RWB-E1-043 | The migration deploys; the router never sees invented rows |
| R4 | data_product.definition is NOT NULL but no source supplied values | Seed the 14 definitions from the Conceptual Data Model v6 Data products tab; correct the story DDL to not null | No schema change; RWB-E1-016 AC2 and RWB-E1-064 get a populated catalog |

## 2. Ruling 1 - sys_objects.data_product is nullable; the FK stays

### 2.1 Conflict

Physical Schema v4 line 2639 declares fk_sys_objects_data_product, yet 33 of the 108 sys_objects seed rows carry values (OPS 22, AGT 8, RPT 3) that are outside the 14-row data_product catalog required by AC3 and AC8.

### 2.2 Evidence

- Physical Schema v4 lines 4183ff seed 108 sys_objects rows: 75 carry DP01 to DP14, 33 carry OPS, AGT or RPT.
- The LDM v6 Entities tab assigns exactly the same 108 entities to the same distribution, so this is deliberate modelling across two documents, not a seed typo.
- For all 33 rows, subject_area equals data_product (OPS/AGT/RPT). The column is carrying two kinds of code: a product code for 75 rows and a subject-area code for 33.
- The Conceptual Data Model v5 defines exactly 14 data products; its Subject areas tab maps OPS, AGT and RPT to the subject areas Loads and operations, Agent runtime and Reporting.
- LOV-DATA-PRODUCT (Reference Data v3) holds exactly 14 values.
- The LDM meaning text of DF-REF-091 already reads "DP01 to DP14 **or None**"; the Mandatory = Yes flag is the inconsistent part.
- Nothing is lost by emptying the 33 rows: subject_area is the legitimate home for that classification.

### 2.3 Ruling

sys_objects.data_product becomes nullable. V0001 seeds 75 sys_objects rows with a product and the 33 operational rows with NULL. FK fk_sys_objects_data_product is created in V0001, as story section 13 already states, so the constraint ships from day one. This is the model correction; it replaces the smaller deviation of deferring the FK (previous recommendation C) and is cheaper before build than after it.

**Status:** applied in Physical Schema v5. `sys_objects.data_product` is nullable and the 33 operational rows carry NULL; `fk_sys_objects_data_product` is created in V0001.

### 2.4 Edits

| # | Document and location | Current | Change |
|---|---|---|---|
| 1.1 | Physical Schema v4 -> issue v5, sys_objects DDL (lines 1065-1082) | `data_product varchar(10) NOT NULL` | `data_product varchar(10)` (nullable) |
| 1.2 | v5, sys_objects seed block (lines 4183ff) | 33 rows carry `'OPS'`, `'AGT'` or `'RPT'` | Replace the fourth value with `NULL` on those 33 rows; add the comment: `-- Operational entities (loads, agents, reporting) carry no data product; subject_area keeps OPS/AGT/RPT (D-RCV-34).` |
| 1.3 | v5, line 2639 | fk_sys_objects_data_product | Unchanged - the FK is kept and created in V0001 |
| 1.4 | LDM v6 -> issue v7, Fields tab, DF-REF-091 | Mandatory = Yes | Mandatory = No; meaning text gains "; the operational entities of OPS, AGT and RPT carry no product" |
| 1.5 | LDM v7, Entities tab | 33 entity rows show OPS/AGT/RPT in the Data product column | Blank the Data product value on those 33 rows (subject area unchanged) |
| 1.6 | Conceptual Data Model v5 -> optional reissue, Subject areas tab rows 19-21 | "Loads and operations", "Agent runtime", "Reporting" name OPS/AGT/RPT in the Data products column | Remove those three tokens so subjects no longer masquerade as product codes |
| 1.7 | RWB-E1-001 story, section 13, Database paragraph | "Adds a foreign key from sys_objects.data_product to data_product.product_code; the migration inserts the data_product seed rows before the sys_objects rows." | Sentence stays; append: "sys_objects.data_product is nullable: the 75 product entities name DP01 to DP14; the 33 operational entities of OPS, AGT and RPT leave it empty (D-RCV-34)." |
| 1.8 | RWB-E1-001 story, section 11, row DF-REF-091 | "Create and write 108 rows; read" | Annotate: "Create and write 108 rows (75 with a product, 33 empty); read" |

## 3. Ruling 2 - v_data_dictionary reads owner_role from data_product

### 3.1 Conflict

The view takes `f.owner_role` (line 2543), but all 1,256 sys_fields inserts use a 12-column list that never populates owner_role, so AC2's expected "RW-DATASTEW" returns NULL.

### 3.2 Evidence

- Story section 12 has always mapped owner_role to data_product - the view differs from the story, not the other way round.
- data_product.owner_role is NOT NULL and is seeded RW-DATASTEW for every product.
- LDM DF-REF-107 (sys_fields.owner_role) is Mandatory = No and is loaded later by RWB-E1-064 as a per-field attribute; it is not the AC2 source.
- The current view also omits product_system_of_record and entity_system_of_record, which section 12 names.

### 3.3 Ruling

The view is corrected in one pass, since no consumer exists yet: owner_role from data_product, plus the two system-of-record columns, plus the four sys_fields attributes that RWB-E1-064 will need. Section 12 adopts the view's column names (is_mandatory, is_personal) so there is one naming set.

Replace v_data_dictionary in v5 with:

```sql
CREATE VIEW v_data_dictionary AS
SELECT o.object_name      AS entity,
       f.field_name       AS field,
       f.field_id,
       f.data_type,
       f.physical_type,
       f.is_mandatory,
       f.lov_code,
       f.references_object,
       f.source_system,
       f.source_field,
       f.is_personal,
       f.late_behavior,
       f.interface_id,
       f.description,
       o.data_product,
       o.system_of_record AS entity_system_of_record,
       p.system_of_record AS product_system_of_record,
       p.refresh_cycle,
       p.owner_role,
       p.owner_user_id
FROM sys_fields f
JOIN sys_objects o ON o.object_name = f.object_name
LEFT JOIN data_product p ON p.product_code = o.data_product AND p.is_active
WHERE f.is_active AND o.is_active;
```

### 3.4 Edits

| # | Document and location | Change |
|---|---|---|
| 2.1 | Physical Schema v5, lines 2529-2551 | Replace the view with the block above |
| 2.2 | RWB-E1-001 story, section 12 contract table | Replace with: entity, data_product, entity_system_of_record from sys_objects; field, field_id, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, late_behavior, interface_id, description from sys_fields; product_system_of_record, refresh_cycle, owner_role, owner_user_id from data_product |
| 2.3 | Build Notes Epic 1, step on the view ("The schema file has no definition for that view, so you write it.") | Replace with: "v_data_dictionary is held in Physical Schema v4 lines 2529-2551; copy it with the D-RCV-34 corrections (p.owner_role and the two system_of_record columns)." |

## 4. Ruling 3 - delegation_limit is empty in the baseline

### 4.1 Conflict

All 24 `INSERT INTO delegation_limit` rows in Physical Schema v4 (lines 6628-6651) omit limit_version and regulation_item, both NOT NULL (lines 883-884), so every row raises a not-null violation and the transaction discards the schema.

### 4.2 Evidence

| Source | Rows | What it represents |
|---|---:|---|
| Physical Schema v4 seed | 24 | Placeholder grid: decision 'ALL' x levels L1-L6 x 4 product groups |
| Delegation of Authority Matrix v2 | 95 | The real limits, by regulation item, decision and level; no product_group column |
| RWB-E1-038 load DOA-2026.11 | 218 | 95 limits x 2 products (109 MORTGAGE + 109 SSME), with limit_version and regulation_item |
| RWB-E1-043 AC2 fixture | 24 | A version-mechanism test fixture, not the production matrix |

- decision_code 'ALL' is not a value of LOV-DECISION (D1 to D9 with sub-decisions, X1 to X7), so the placeholders are invalid before the two missing columns are even considered.
- Twelve of the 24 rows are HIRE_PURCHASE and UNSECURED; the matrix states chapter 8 limits "load when supplied (DL18)" and lists them as open.
- Matrix "How it applies" rule 11: each limit is a row with a version, valid from and valid to and the approver; a change is a data load approved by Risk.
- The E1-001 story's own flow step 3 never names delegation_limit - only D-RCV-29 does.

### 4.3 Ruling

delegation_limit is empty in V0001. The 24 placeholder rows are deleted from the schema, not commented out. Content is owned by RWB-E1-038, which loads DOA-2026.11 (95 limits -> 218 rows) through RWB-E1-043, approved by RW-RISK, with limit_version and regulation_item from the matrix; the chapter 8 product-group rows follow when Risk supplies them (DL18). D-RCV-29 is amended to remove delegation_limit from the baseline seed list, which re-aligns the ruling with the story rather than diverging from it.

**Status:** applied in Physical Schema v5. `delegation_limit` holds no baseline rows and the 24 placeholder rows are removed from the schema.

### 4.4 Edits

| # | Document and location | Change |
|---|---|---|
| 3.1 | Physical Schema v5, lines 6628-6651 | Delete the 24 INSERT statements entirely |
| 3.2 | Decision Log, D-RCV-29 | Amend: delegation_limit is not part of the V0001 seed (superseded by D-RCV-34 clause (c)) |
| 3.3 | RWB-E1-001 story, section 13, Configuration and reference data | Append: "delegation_limit holds no baseline rows; its content is loaded as version DOA-2026.11 through RWB-E1-043 by RWB-E1-038 (D-RCV-34)." |
| 3.4 | RWB-E1-038 story, header Depends on | Add RWB-E1-001 (section 3 already requires the table to exist) |
| 3.5 | RWB-E1-038 story, section 13, Database bullet | Rewrite: "delegation_limit is created with all its columns by V0001 (limit_version varchar(20) not null, regulation_item varchar(10) not null, applies_when and the four derived-limit columns). This story's migration creates only the lookup index ix_delegation_lookup on (decision_code, regulation_item, product_group, approval_level, valid_from) where is_active - that index is not in Physical Schema v4." |
| 3.6 | RWB-E1-043 story, AC2 fixture note (and its row in Test Cases v5) | Note that the 24 DELEGATION_LIMIT fixture rows carry limit_version DOA-2026.11 and a regulation_item value, so the load passes the row schema of the real table |

## 5. Ruling 4 - the 14 definitions are seeded from the CDM

### 5.1 Conflict

data_product.definition is varchar(400) NOT NULL (Physical Schema v4 line 984; LDM DF-REF-073 Mandatory = Yes). The story section 13 DDL reads `definition varchar(400)` with no not null, and its seed table carries no definition column, so the seed cannot be written against the schema as declared.

### 5.2 Evidence

- The Conceptual Data Model v5 Data products tab holds 14 rows, one per product, with a "What it holds" description; Data Ownership and Stewardship v2 repeats the same 14. The mapping is one-to-one for the products; the non-one-to-one case is only on the Subject areas tab.
- Longest description is 143 characters, well inside varchar(400).
- BRD REQ-RDF-011 requires a catalog entry stating its definition; RWB-E1-016 AC2 returns definition; RWB-E1-064 owns the formal definitions. Leaving the column nullable would push a null into those two stories and need a later migration to restore NOT NULL.

### 5.3 Ruling

definition stays NOT NULL. V0001 seeds the 14 definitions from the Conceptual Data Model Data products tab (v5 when this ruling was taken, v6 at issue); the catalog load repeats them. The story DDL outlier is corrected to match the LDM and the schema. Each product owner approves its wording at the gate.

**Status:** applied in Physical Schema v5. The 14 definitions are seeded from Conceptual Data Model v6, which carries the same 14 products and the same one-to-one mapping; the seed table below carries the CDM v6 names, definitions and systems of record word for word.

### 5.4 Edits

| # | Document and location | Change |
|---|---|---|
| 4.1 | RWB-E1-001 story, section 13 seed table | Replace the four-column table with the six-column table below |
| 4.2 | RWB-E1-001 story, section 13, Database sentence | `definition varchar(400) not null`; `product_code varchar(25)`; `valid_from date not null` seeded 2026-11-20 |
| 4.3 | Physical Schema v5 | No change - definition NOT NULL already stands |
| 4.4 | RWB-E1-064 story, section 13 | `product_code varchar(4)` -> `varchar(25)` wherever E1-064 names it |

**Paste-ready seed table for story section 13** (name, definition and system of record copied from the Conceptual Data Model v6 Data products tab; product owners approve):

| Code | Name | Definition | System of record | Refresh cycle | Valid from |
|---|---|---|---|---|---|
| DP01 | Account and arrears | Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments | ACE (ingested from ALS) | DAILY | 2026-11-20 |
| DP02 | Customer and party | Customers, guarantors, co-borrowers and heirs, identity masked to the last four, contact points, consent and flags for vulnerability, death and bankruptcy | ACE (ingested from SCBPDM and the core bank) | DAILY | 2026-11-20 |
| DP03 | Case and ownership | The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations | Recovery Workbench | DAILY | 2026-11-20 |
| DP04 | Treatment and offers | Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome | Recovery Workbench for the treatment; ACE (ingested from the core bank) for the restructure plan | DAILY | 2026-11-20 |
| DP05 | Contact and promises | Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS | ACE (ingested from EFS) | DAILY | 2026-11-20 |
| DP06 | Collateral and assets | Collateral, appraisals, assets held after repossession or transfer, listings and sale results | ACE (ingested from CCMS, SVAF, AMIS and RPS) | WEEKLY | 2026-11-20 |
| DP07 | Legal events and cases | Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement | ACE (ingested from LIT and WIN) for the court record and the proof of delivery; Workbench for notices and enforcement | DAILY | 2026-11-20 |
| DP08 | Partner performance | Partners on the panel, work placed with each, results, fees and scorecards | Recovery Workbench | DAILY | 2026-11-20 |
| DP09 | Debt sale | Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs | Recovery Workbench | DAILY | 2026-11-20 |
| DP10 | Documents and extracted fields | Documents against the case, the fields read from them, retention class and custody of originals | Recovery Workbench document hub | DAILY | 2026-11-20 |
| DP11 | Scores and route economics | Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions | ACE (ingested from COLLINS) | DAILY | 2026-11-20 |
| DP12 | Decision log | One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome | Recovery Workbench | DAILY | 2026-11-20 |
| DP13 | Money and closure | Payments and proceeds matched to the case, write-off postings and recovery after charge-off | ACE (ingested from ALS and GL) | DAILY | 2026-11-20 |
| DP14 | Reference data | Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned | Recovery Workbench | DAILY | 2026-11-20 |

## 6. Conformance corrections that ride with these rulings

| # | Document and location | Current | Change | Basis |
|---|---|---|---|---|
| 5.1 | RWB-E1-001 story, AC1 | "the conformance test reports 413 of the 413 fields of these tables matched by name and physical type" | "533 of the 533 fields of these tables" | The 44 tables hold 533 business fields (499 on the 41 business tables + 7 sys_objects + 17 sys_fields + 10 data_product). 413 is the Source to Target Mapping count (110 inbound + 303 Workbench fields) |
| 5.2 | RWB-E1-001 story, AC6 | "the row counts of sys_objects (41) and sys_fields (413) are unchanged" | "sys_objects (108) and sys_fields (1,256)" | D-RCV-29 |
| 5.3 | Build Notes Epic 1 v4 -> v5, step "Insert the dictionary rows..." | "One row in sys_objects for each of the 41 entities, and one row in sys_fields for each of the 413 fields, with the values taken from Source to Target Mapping v3.xlsx" | Rewrite: 108 sys_objects rows (75 with a product, 33 empty) and 1,256 sys_fields rows, values as held in the Logical Data Model v6 and Physical Schema v4; keep "Insert the 14 data_product rows before the sys_objects rows" | Lines 27 and 29 of the current notes contradict each other |
| 5.4 | RWB-E1-064 story, section 13 Database bullet | Says this story creates data_product, sys_field_version, data_contract and adds the four sys_fields attribute columns | Rewrite: "V0001 already creates data_product, data_product_access, data_contract, sys_field_version and the four sys_fields attribute columns. This story owns the content: the dictionary attribute load and the field versions." | Those tables exist in v4 at lines 984, 1002, 1042, 1084-1101, 1113 |
| 5.5 | RWB-E1-064 story, section 13 | `product_code varchar(4) primary key` | `varchar(25)` | LDM DF-REF-071 and v4 line 982 |
| 5.6 | RWB-E1-016 story, section 13 | `data_product_access ... product_code varchar(4)` | `varchar(25)` | LDM DF-REF-081 and v4 line 1004 |
| 5.7 | Test Cases v5, Story test cases tab | Rows TC-E1-001-01 and TC-E1-001-06 data that cite the 41/413 counts | Correct to 533 conformance fields and 108/1,256 row checks | Same basis as 5.1 and 5.2 |

## 7. Consolidated change schedule

| # | Change | Owner |
|---|---|---|
| 1 | Issue Physical Schema v5 with the edits in 1.1, 1.2, 2.1, 3.1, 5.4 and the seed-table note in 4.2 context | Data architect |
| 2 | Issue LDM v7 with 1.4 and 1.5 | Data architect with steward |
| 3 | Record D-RCV-34 in the Decision Log and mark D-RCV-29 amended under clause (c) | Decision owner |
| 4 | Update the five stories (R1, R2, R3, R4, 5.x edits) in RWB-E1-001, E1-016, E1-038, E1-043, E1-064 | Business analyst |
| 5 | Approve the 14 definition texts and the section 12 naming decision at the gate | Product owners with the BA |
| 6 | Update Build Notes Epic 1 to v5 (2.3 and 5.3) | Squad lead |
| 7 | Reissue the Entity Relationship Diagram when convenient (v4): sys_objects -> data_product stays; the 33 operational entities show no product | Optional |
| 8 | Implement at build: V0001 order data_product (14 rows) -> sys_objects (108) -> sys_fields (1,256); nothing else changes in the story's build steps | P1 squad |

## 8. Decision-log entry to record

> **D-RCV-34** | Ruled on the four source conflicts in RWB-E1-001 (specification re-run of 10 November 2026 against Physical Schema v4): (a) sys_objects.data_product becomes nullable; V0001 seeds 108 sys_objects rows, 75 with a product, the 33 operational entities of OPS, AGT and RPT empty, and creates fk_sys_objects_data_product; DF-REF-091 becomes optional. (b) v_data_dictionary reads owner_role from data_product, adds entity_system_of_record and product_system_of_record, keeps references_object, late_behavior, interface_id and description; section 12 of RWB-E1-001 adopts the view's column names. (c) delegation_limit is not seeded by V0001; the 24 placeholder rows that violate NOT NULL limit_version and regulation_item are removed; content is owned by RWB-E1-038, loading DOA-2026.11 (218 rows from the 95 matrix limits) through RWB-E1-043, approved by RW-RISK, chapter 8 product rows following DL18; D-RCV-29 amended accordingly. (d) data_product.definition stays NOT NULL; the 14 definitions seeded by V0001 come from the CDM v5 Data products tab and are repeated in the catalog load; the story DDL is corrected to not null and product_code varchar(25), valid_from 2026-11-20. (e) AC1 corrected to 533 of 533 conformance fields for the 44 tables; AC6 corrected to sys_objects 108 and sys_fields 1,256. (f) RWB-E1-064 creates no DDL - V0001 already creates data_product, data_product_access, data_contract, sys_field_version and the four sys_fields attribute columns; E1-064 owns content and versions. (g) RWB-E1-038's migration adds only ix_delegation_lookup, and its Depends on gains RWB-E1-001. | **2026-11-10** | Recovery tech lead with the data architect (specification gate ruling) | What it means: V0001 builds from Physical Schema v5 as written; delegation content arrives by reference load before the 30 November release; the DQ, sandbox, catalog and dictionary stories read one dictionary and one catalog in the shape above.

## 9. Effect on the acceptance criteria

| Criterion | Effect |
|---|---|
| AC1 Schema deployed | Wording only: 44 tables unchanged; conformance figure 413 -> 533 |
| AC2 Dictionary published | Passes as written once R2 ships the corrected view |
| AC3 One system of record | Unchanged - data_product holds exactly 14 rows |
| AC4 Failed migration leaves no partial schema | Unchanged |
| AC5 Conformance failure | Unchanged |
| AC6 Repeated migration | Counts corrected to 108 / 1,256 |
| AC7 Two systems of record refused | Unchanged |
| AC8 Missing product refused | Unchanged - still exactly DP01 to DP14 |
| AC9, AC10 | Unchanged |

## 10. Verification steps for V0001

These steps are re-based on Physical Schema v5 and D-RCV-35; the v4 figures (44 tables, 108 / 1,256, 533 of 533) no longer apply.

1. Build V0001 from Physical Schema v5; run on an empty PostgreSQL container with `recoverySchema = recovery`. Then apply V0002 (Tier 1 views) and, once RWB-ACE-001 lands, V0003 (Tier 2 views).
2. Assert: 92 tables in schema recovery and, after V0002 and V0003, 30 `recovery.v_ace_*` views; sys_objects holds 122 rows (92 tables and 30 views), of which 98 name a product and 24 (OPS 13, AGT 8, RPT 3) hold NULL; sys_fields holds 1,366 rows; data_product holds 14 rows with definition, owner_role and valid_from populated; delegation_limit holds 0 rows; fk_sys_objects_data_product exists; no constraint in schema recovery references a table in schema public.
3. Assert the view: for v_ace_account.days_past_due - DF-ACE-018, NUMBER, integer, source ACE, source field public.account.delay_days, product DP01 with system of record "ACE (ingested from ALS)", refresh DAILY, owner role RW-DATASTEW.
4. Run DataDictionaryConformanceTest and assert 1,366 of 1,366 sys_fields rows match their table or view column by name and physical type; run the view conformance test (every `v_ace_*` view compiles; the recovery role cannot read a public table directly or write to any table).
5. Reapply in SIT; assert no change (Flyway skips version 1.001).

## 11. Fallback if the gate refuses the model change

If the gate wanted the absolute smallest edit to the already-ruled documents, the minimal set was: drop the FK (previous recommendation C), correct the view, leave delegation_limit to E1-038, and seed the definitions. That is still deployable but ships a knowingly-broken reference, a stale view contract, duplicate DDL in E1-064 and wrong AC counts. Nothing is built yet, so the root-cause set above costs the same and removes all four follow-on defects.
