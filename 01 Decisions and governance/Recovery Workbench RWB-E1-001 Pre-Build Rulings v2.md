# RWB-E1-001 Pre-Build Rulings - Best-Answer Set

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Document | Recovery Workbench RWB-E1-001 Pre-Build Rulings v2 |
| Superseded by | Counts superseded by D-RCV-35 (section 0) |
| Scope | The four source conflicts in RWB-E1-001 found by the specification re-run of 10 November 2026, ruled for the initial phase (nothing built); re-based on Physical Schema v5 and D-RCV-35 (section 0) |
| Status | Proposed - best-answer set for the specification gate. The full paste-ready pack (seed table, corrected view SQL, line-by-line edit schedule) is Recovery Workbench RWB-E1-001 Specification Rulings v2.md |
| Decision owner | Recovery tech lead with the data architect |
| Amends | D-RCV-29 (delegation_limit seed wording) |
| Related | D-RCV-28; D-RCV-35; DL43 (open, needed 2026-11-21); DL41 (ruled); DL18 (open, needed 2026-11-30); Story Defects register v2 rows 10 and 11 |

Because nothing is built, the calculus is to fix root causes in the source documents now: deferring a constraint or carrying an overloading forward costs nothing today but compounds once RWB-E1-003 through E1-013 consume the schema.

## 0. Re-base note for v2

This version re-bases the best-answer set on Physical Schema v5 and D-RCV-35 (U1 to U5). The copy-table counts it was written against - 44 tables, 533 fields, 108 `sys_objects` and 1,256 `sys_fields` - are superseded. The schema is 92 tables, 30 `recovery.v_ace_*` views, 122 `sys_objects` and 1,366 `sys_fields`, with no copy or load tables left in it.

The four answers and their reasoning stand. Q4 (= R4 in the Specification Rulings) holds: the 14 definitions are seeded from the Conceptual Data Model v6 Data products tab, and the systems of record become "ACE (ingested from X)" - for example "ACE (ingested from ALS)" for DP01 - because ACE is the store the Workbench reads. Where the later sections still quote the v4 counts, they are the record of the 10 November re-run. The full paste-ready pack is **Recovery Workbench RWB-E1-001 Specification Rulings v2.md**.

## 1. Rulings at a glance

| Question | Initial-phase best answer | Beats the minimal answer because |
|---|---|---|
| Q1 - FK vs catalog | D (new option) - make sys_objects.data_product nullable, set the 33 operational rows to NULL, keep the FK | Fixes the real defect (overloaded column) from day one instead of deferring a knowingly-broken reference |
| Q2 - NULL owner_role | 1 - the view takes owner_role from data_product, plus full section-12 alignment of the view in one pass | No consumers exist yet, so align the view to the contract completely, not just one column |
| Q3 - delegation_limit seed | 3, amended | Already the root-cause answer; the real content belongs to RWB-E1-038 |
| Q4 - missing definitions | 1 - definitions from the CDM v6 Data products tab | Already the root-cause answer; the text is one-to-one for all 14 products |

## 2. Q1 - best: fix the overloading, keep the FK

The evidence supports the model correction better than deferral:

- LDM DF-REF-091 already anticipates it. Its own meaning text reads: "Data product the object belongs to, **DP01 to DP14 or None**". The Mandatory = Yes flag is the inconsistent part.
- Nothing is lost by emptying the 33 rows. For all 33, subject_area already equals data_product (OPS/AGT/RPT) - the subject_area column is the legitimate home for that classification.
- The story's own text survives unchanged. Section 13's "inserts the data_product seed rows before the sys_objects rows" and the FK statement both remain true. The 68-FK count in flow step 2 (and defect-register row 10, which records "68 FKs matching Physical Schema v4") stays accurate - deferring the FK would have silently changed it to 67.
- Every AC holds. AC1 (44 tables), AC3/AC8 (14 catalog rows), AC6 (108/1,256 after the count correction in section 6), and D-RCV-29's completeness counts. D-RCV-29 needs one wording amendment: "data_product empty for the 33 operational entities, which carry OPS/AGT/RPT in subject_area."

Required edits (details in clauses 1.1-1.8 of the Specification Rulings pack):

1. LDM v6 -> v7: DF-REF-091 -> Optional, and the Entities tab drops OPS/AGT/RPT from the Data product column (they stay in Subject area).
2. Physical Schema v4 -> v5: sys_objects.data_product varchar(10) nullable; FK fk_sys_objects_data_product retained as declared.
3. Story section 13: the seed statement becomes "75 sys_objects rows carry a data product; 33 operational entities leave it empty."
4. Migration order unchanged: catalog rows -> sys_objects -> sys_fields.

## 3. Q2 - best: one full view alignment, not one line

The view takes owner_role from data_product - but do the whole reconciliation in one pass, since nobody consumes the view yet:

```sql
-- align to story section 12 exactly
o.system_of_record AS entity_system_of_record,   -- add (missing today)
p.system_of_record AS product_system_of_record,  -- add (missing today)
p.owner_role,                                    -- replace f.owner_role
```

One naming decision to make now while it costs nothing: section 12 calls the flags `mandatory` and `personal`; the view exposes `is_mandatory` / `is_personal`. Update section 12 to the view's names (it matches every other physical column); either is fine, but it must be one set, not two.

## 4. Q3 - best: no placeholder rows, ever

Already the root-cause fix:

- The 24 rows are `decision_code = 'ALL'`, which is not in LOV-DECISION (D1-D9 plus X1-X7). They are a placeholder grid, not a subset of the 95-limit matrix.
- RWB-E1-038 is the content owner: it loads DOA-2026.11 - 218 rows from the 95 matrix limits (109 MORTGAGE + 109 SSME) - with limit_version and regulation_item properly populated.
- Chapter 8 limits (the 12 HIRE_PURCHASE/UNSECURED rows) "load when supplied (DL18)" per the matrix; they cannot be invented for a baseline.

Pre-build extras while editing:

- Delete the 24 stray inserts from Physical Schema v5 entirely - do not just comment them in the migration; the source file is what the next story copies.
- Amend D-RCV-29: remove delegation_limit from the seed list. The story's flow step 3 never mentioned it anyway, so this re-aligns the ruling with the story rather than diverging from it.
- RWB-E1-043's AC2 fixture (24 rows) stays valid as a version-mechanism test, but its rows should carry limit_version/regulation_item values so it is shape-consistent with real loads.
- RWB-E1-038 section 13 says its migration "adds" limit_version/regulation_item - but v4 already declares them. Correct E1-038 to say the columns come from V0001 and the story's migration adds only the lookup index ix_delegation_lookup, which is not yet in the schema file.

## 5. Q4 - best: seed the definitions, keep NOT NULL

Sourced from the CDM v6 Data products tab (v5 when first ruled); all 14 fit varchar(400) (longest 154 characters, DP02). The mapping is one-to-one for the 14 products - the non-one-to-one case is only on the Subject areas tab, so no composition rule is needed.

Pre-build extras:

- Correct story section 13's DDL outlier to `definition varchar(400) not null` (matching the LDM and the schema).
- Have each product's business owner approve the wording on record.

## 6. The pre-build clean-up bundle

These four fall out of the same documents and should not be left for the squad to trip over:

| # | Issue | Best fix |
|---|---|---|
| 1 | AC1 says 413 of 413 fields; AC6 says sys_objects 41 / sys_fields 413 | 413 is actually the S2T mapping total (110 inbound + 303 Workbench). The 44 tables hold 533 business fields (499 on the 41 tables + 7 sys_objects + 17 sys_fields + 10 data_product) and sys_fields holds 1,256. So AC1 -> "533 of 533", AC6 -> "108 / 1,256" |
| 2 | data_product.valid_from is NOT NULL but the section 13 seed table has no date column | Add it; seed with the AC3/AC10 catalog date 2026-11-20 so seed and first load agree |
| 3 | Story says product_code varchar(4); LDM and v4 say varchar(25) | Correct the story (and the duplicated DDL text in RWB-E1-064 section 13 and RWB-E1-016 section 13) to varchar(25) |
| 4 | RWB-E1-064 still claims it creates data_product and adds the four sys_fields columns that v4 already declares | V0001 owns the DDL; E1-064 owns the content load and sys_field_version. Remove the duplicate migration text before it becomes a real tick-order conflict |

## 7. Decision text to record

> **D-RCV-34 (proposed):** On the specification-gate re-run of 10 November 2026 against Physical Schema v4: (1) sys_objects.data_product is nullable and empty for the 33 operational entities (OPS/AGT/RPT carry them in subject_area); FK fk_sys_objects_data_product is created in V0001. DF-REF-091 becomes Optional. (2) v_data_dictionary takes owner_role from data_product and adds entity_system_of_record and product_system_of_record; section 12 renamed to the view's column names. (3) delegation_limit is not seeded by V0001; the 24 placeholder rows are removed; content is owned by RWB-E1-038 loading DOA-2026.11 (218 rows) through RWB-E1-043, amending D-RCV-29. (4) data_product.definition stays NOT NULL; the 14 definitions are seeded from the CDM v6 Data products tab and repeated in the catalog load. (5) AC1 corrected to 533/533 conformance fields; AC6 corrected to 108/1,256 rows; valid_from seeded 2026-11-20; product_code length corrected to varchar(25).

## 8. Fallback

If the gate prefers the already-ruled artifacts untouched, the minimal deployable set (previous memo) was C / 1 / 3 / 1 - but it leaves a knowingly-broken reference, a stale view contract, duplicate DDL in E1-064 and wrong AC counts, each trivial to avoid today and non-trivial once other stories depend on the migration. Since we are in the initial phase, take the bundle above as a single specification-gate amendment now.
