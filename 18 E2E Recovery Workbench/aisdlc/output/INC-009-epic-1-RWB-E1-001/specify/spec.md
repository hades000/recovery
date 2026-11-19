# Technical Specification — RWB-E1-001 Recovery tables for the 14 data products

| Field | Value |
|---|---|
| Story | RWB-E1-001 — Recovery tables for the 14 data products |
| Epic / module | E1 (release 30 November 2026) / P1 Recovery data engine |
| RUN_ID | `INC-009-epic-1-RWB-E1-001` |
| Revision | 4 — remediation run 3 of spec gate round 3 (`../review/spec-gate-review-3.md`, findings 025–026). Revision 3 text kept in `spec.run3.md`, revision 2 in `spec.run2.md`, revision 1 in `spec.run1.md`; finding-by-finding answers in `gate-response.md` §§"Round 2" and "Round 3" |
| Source requirement | Story file v7 (15 Nov 2026), `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md`; increment card `docs/increments/INC-009-epic-1-RWB-E1-001.md` |
| Upstream IDs | REQ-RDF-001; FEAT-RDF-01, FEAT-RDF-02; `BR-RWB-013` / `FR-RWB-013` (Traceability Matrix §3, row 009); NFR-RWB-005, -006, -008, -009 (Canonical Requirements v2.0 §NFR); TC-E1-001-01 to TC-E1-001-12 |
| Governing decisions | D-RCV-35 (U1–U5) and D-RCV-36 (change register A.5, A.7, row 18, T5); ADR-010; D-RCV-28 and D-RCV-29 (Decision Log v10); run decisions D-RUN-07, -08, -11, -12, -13 and D-RUN-18, -19, -20, -21 (`AI-SDLC-BUILD-LOG.md` decisions table, cited by decision ID). Every D-RUN is an **orchestrator (Claude Code, an AI agent) run decision, not a human ruling**; ratification of D-RUN-18..21 is OPEN-050; RWB-E1-001 Specification Rulings v2 and Pre-build Rulings v2 (both status Proposed) |
| Status | Revised for spec gate round 4. **Two Blocker = Yes document gaps** (`GAP-E1001-17` DP07 width, `GAP-E1001-18` `is_personal`) are carried on labelled assumptions `ASM-E1001-13` and `ASM-E1001-14`. A human ruling is required **before build (the merge of this story's migration)**; it stops nothing earlier, and no AI triage is that ruling |
| Prepared | 2026-11-18 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer spec gate rounds 1–3 (`../review/spec-gate-review.md`, `-2.md`, `-3.md`). No human approval of this revision is claimed |

## Sources and how they are cited

Short names used below. All `requirement/legacy/` paths are in the read-only document set
`17 AI-First SDLC Repository v2/requirement/legacy/`.

| Short name | Document (version) | Path |
|---|---|---|
| Story v7 | RWB-E1-001 story file v1 inside Epic 1 Story Files v7 | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md` |
| PS v6 | Recovery Workbench Physical Schema v6 (16 Nov 2026) | `06-data/recovery-workbench-physical-schema-v6.sql` (byte-identical copy in `infra/postgres/schema/03-recovery-physical-schema-v6.sql`) |
| PDPA v4 | Recovery Workbench Data Classification and Personal Data Inventory v4 (Fields tab, Key) | `06-data/recovery-workbench-data-classification-and-personal-data-inventory-v4-xlsx.md` |
| DL v10 | Recovery Workbench Decision Log v10 | `01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` (D-RCV-28 line 77, D-RCV-29 line 78) |
| D-RCV-36 CR | D-RCV-36 Temporal and Drools change register | `aisdlc/docs/decisions/d-rcv-36-temporal-and-drools.md` (§3.2, T5, A.5, A.7, row 18) |
| D-RCV-35 | D-RCV-35 ACE DB alignment | `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md` (§3.3) |
| D-RUN | Run decisions D-RUN-07 to D-RUN-13 and D-RUN-18 to D-RUN-21 | `AI-SDLC-BUILD-LOG.md` decisions table, cited by **decision ID and timestamp only, never by build-log line number** (the append-only timeline moves its rows). Every one was made by Claude Code, the orchestrator (an AI agent), not by a human; none is ratified |
| D-RUN-18…21 detail | D-RUN-18: the reference-load handler SPI is published by P4 `access.api`; no P1 → P3 edge. D-RUN-19: parameter reads outside P3 go through a P4 `access.api` read interface implemented in P3 `casewf.config`. D-RUN-20: the P4 SPI is for handlers outside the registry's module; `PARAMETER` is a dispatcher branch calling `casewf.config.api` inside P3. D-RUN-21: "touches one module" means the ACE module (recovery) | `AI-SDLC-BUILD-LOG.md` decisions table, D-RUN-18/-19/-20/-21 rows (2026-11-18 04:55, 05:10, 05:34, 05:36). Ratification by the recovery tech lead is OPEN-050 and is **not** claimed |
| Rulings v2 / PBR v2 | RWB-E1-001 Specification Rulings v2; RWB-E1-001 Pre-build Rulings v2 (both Proposed) | `01-decisions-and-governance/recovery-workbench-rwb-e1-001-specification-rulings-v2.md`, `…-pre-build-rulings-v2.md` |
| MSG v4 | Error and Message Standard v4 | `07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| API v4 | API Specification v4 | `api/recovery-api-v4.yaml` (repo copy): `/admin/reference-loads` line 3167, approve line 3214, `ReferenceLoad` line 8832 |
| BS v6 | Build Sequence Epic 1 and Epic 2 v6 | `11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` (orders 1, 3, 8, 9, 10, 28, 36) |
| REQ v2.0 | Recovery Workbench canonical requirements v2.0 (16 Nov 2026), NFR table | `17 AI-First SDLC Repository v2/requirement/RecoveryWorkbench_Requirements.md` lines 229–238 |
| E1-0nn v7 | Other story files in Epic 1 Story Files v7 (E1-039, E1-042, E1-043, E1-072) | same folder as Story v7 |
| Sibling specs | Cited by section or row ID, never by line. **E1-043** (INC-008, **revision 10**, passed its spec gate round 10, `review/spec-gate-review-10.md`): SPEC-001, -002, -003, -006, -016, -018, -019, -025, -026, -027, -028, -029, -030, -031, -032, and `shared-updates.md` §3.1 (forward contract to this story) and §3.2 (to RWB-E1-064). **E1-042** (INC-003, **revision 13**, passed round 12): §4.3 seams table, §10.2, §12.2, §12.3, §12.14 R7-1, CLAR-025/-027. **E1-044** (INC-001, spec **v14-7**): SPEC-007 (lint rules; D-RUN-13), SPEC-015, T-044-21. **RWB-TE-001** (INC-002, spec **v4**, passed its gate): SPEC-004 (e), -022 (d), -023, -025, T-TE001-14. **E1-069** (INC-010): SPEC-015 (a) and (c) and review 107. **TE-011** (INC-006): SPEC-TE011-001 dictionary reader and the (object, field) fixture matching announced from its spec gate round 4 | `aisdlc/output/INC-0nn-*/specify/spec.md` |
| Baseline code | Repository as of 17 Nov 2026, named by its **post-RWB-TE-001-v4 package** where TE-001 relocates it: `casewf.migration.RecoveryFlywayConfig`, `access.internal.ApiExceptionHandler`, `access.api.ApiProblemException`; unchanged: `RecoveryMigrationLintTest`, `RecoveryDatabaseIT`, `infra/postgres/init/10-load-ace-database.sh`, `20-grants.sql.inc`, `docker-compose.yml`, `.env.example`, `application.yaml`, `README.md` (TE-001 SPEC-022 and its relocation table) | `backend/src/main/java/th/co/scb/ace/demo/recovery/`, `backend/src/test/java/…/recovery/`, `infra/postgres/`, repository root |

**Counting method.** A Python parser read PS v6 lines 1–6130: every `CREATE TABLE` block, every
single-line `INSERT INTO sys_objects` / `sys_fields` statement (quote-aware) and every
`CREATE OR REPLACE VIEW recovery.v_ace_*`. Scripts and outputs, all run with `python -I`:
`evidence/count_v6.py` (counts, conformance), `evidence/lint_v6.py` (297 `'public.…'` literals),
`evidence/pdpa_v4_vs_ps_v6.py` (personal-data comparison and seed widths; list output
`evidence/is_personal_union_v4.tsv`).

| Measure | PS v6 | Story v7 (= Physical Schema v5) | Created by this migration (D-RUN-12) | Schema after this migration |
|---|---|---|---|---|
| Tables | 93 = 89 Workbench + 4 extension | 92 = 88 + 4 | 89 (93 minus the 4 of `T8`) | 93 |
| Foreign keys / indexes | 92 / 112 | — | 91 / 111 (minus `fk_reference_row_version_id`, `ix_reference_row_version_id`) | 92 / 112 plus what E1-042 and E1-043 add to their own tables |
| CHECK constraints / append-only triggers (PS v6 set) | 3 / 2 | — | 3 / 2 | 3 / 2 plus E1-042 and E1-043 additions |
| `sys_objects` rows | 123 = 93 tables + 30 views (99 with a product, 24 without) | 122 | 123 | 123 |
| `sys_fields` rows | 1,379 = 1,075 tables + 304 views | 1,366 | 1,382 = 1,379 + 3 provisional (`ASM-E1001-17`) | 1,382 |
| Conformance C1 (columns → fields, non-standard) | 1,047 / 1,047 | — | — | 1,050 / 1,050 (adds the 3 E1-042 columns) |
| Conformance C2 (table fields → columns) | 1,075 / 1,075 | 1,062 | — | 1,078 / 1,078 |
| Seeds `lov_value` / `role` / `permission` | 598 / 54 / 421 | — | 598 / 54 / 421 | same |
| `parameter_catalog` rows added here | — (E1-042's table) | — | 2 (`rwb.refload.loader.data_product`, `rwb.refload.approver.data_product`; `ASM-E1001-12` closed, SPEC-019) | E1-042's rows plus these 2 |
| `is_personal = true` | 18 | — | 526 (`ASM-E1001-14`) | 526 |

The 28-row difference between 1,075 and 1,047 is the seven standard columns of each extension table,
which PS v6 records in `sys_fields`. PS v6 minus v5 = {`rule_package`, `rule_package_version`}; v5
minus v6 = {`payment_match_rule`} (D-RCV-36 CR A.7, row 18).

## v2 baseline delta

No `_v2-baseline` folder exists for this story. Revision 3 changes against revision 2 (`spec.run2.md`);
revision 2 changed against run 1 (`spec.run1.md`):

| Area | Revision 2 | Revision 3 | Driver |
|---|---|---|---|
| Migration number | Number assigned at merge only; one fixed object set | unchanged | D-RUN-07; finding 004 |
| Tables created | 89; the 4 tables of E1-042 and E1-043 are not created, their dictionary rows stay | unchanged | D-RUN-12; GAP-16; finding 004 |
| `data_product.system_of_record` | `varchar(200)`, DF-REF-074 `physical_type` aligned | unchanged | Finding 001; Blocker gap 17 |
| `is_personal` | Protective union with PDPA v4 (526) | unchanged; the 26 PS-v6-only fields are now listed and the two staff-identifier fields named for the ruling (`GAP-E1001-18`) | Finding 002, 020; Blocker gap 18 |
| Handler seam | E1-043 table-code handler registry; this story registers `data_product`; **stated requirement on E1-043** that no column definition or LOV row is needed | **Re-based on E1-043 revision 10**: this story's `data_product` handler implements the P4 `access.api.ReferenceTableHandler` SPI (D-RUN-18); `PARAMETER` is a dispatcher branch (D-RUN-20); E1-043's own rev 10 SPEC-025 makes the column definition optional and needs two catalog keys, which this story supplies; no requirement is left on E1-043 (SPEC-019) | Finding 014 |
| Repeat load (AC10) | "Writes nothing"; MSG-P1-011 on the response is a gap with E1-043 (201 with the same body) | AC10 **COVERED**: `repeatMessage` gives MSG-P1-011 at L9, 409 Problem, nothing written (E1-043 rev 10 SPEC-025 L9, SPEC-006 rule 1); deviation from a 201 body recorded | Finding 005; 014 |
| X8 / audit | Access test only | 403 test + one REFUSED `REFERENCE_LOAD_AUDIT` line (E1-043 SPEC-028) + access-log seam (RWB-E1-039) + inherited approval controls | Finding 006; 022 |
| Local start | Named switches, defaults and test stages; views-only stand-in; E1-069 hand-off | unchanged; E1-069 SPEC-015 (a) and (c) staleness named in OPEN-NEW-9 | Finding 007; 023 |
| Messages | E1-042 `MessageResolver` seam | unchanged seam, re-cited to E1-042 revision 13; AC9 `{values}` restored to the story wording | Finding 008; 015 |
| `rule_package` seed | Excluded on Story v7 §12/§13 seed list + E1-072 v7; conflict recorded | unchanged | Finding 009; GAP-19 |
| SOR rules | Closed forms F1–F3, labelled `ASM-E1001-09` | F3 becomes a **grammar** (one qualifier shape, no second source), not a three-value list | Finding 010; 021 |
| C3 types | `character(n)` added | `char(n)` is the canonical form, from catalog `bpchar(n)`; DF-REF-301 seeded `char(64)` | Finding 011; 019 |
| Link keys | 18 | unchanged | Finding 012 |
| NFR / PBR v2 | Mapped; cited | unchanged | Finding 013 |
| SPEC-011 lint | Retired: lint is E1-044's (SPEC-007, T-044-21) | unchanged | D-RUN-13 |
| E1-042 added columns | Provisional field IDs DF-REF-300..302; `character(64)` | `char(64)`; citations to E1-042 revision 13 §12.3 | GAP-20; `ASM-E1001-17`; finding 019 |
| T8 counts | "57 `sys_fields` rows" | **53** `sys_fields` rows (4 + 53 = 57 comment statements) | Finding 018 |
| E1-043 asks | Unanswered (dictionary handler, LOV-REF-TABLE correction) | Answered: both withdrawn by E1-043 revision 10; the dictionary owner is RWB-E1-064; the LOV seed stays PS v6 (SPEC-019, `GAP-E1001-23`) | Finding 017 |
| Blocker wording | "before build" / "before the planner" in different places | One statement: before build (the merge of this story's migration) | Finding 024 |
| New | — | `GAP-E1001-23` (dictionary-owner direction), `GAP-E1001-24` (no rollback for `data_product`), `ASM-E1001-20`; SPEC-019 added | Findings 014, 017, 023 |

Revision 4 changes only the two Low findings of round 3 against revision 3 (`spec.run3.md`); no design
decision, blocker or coverage claim changes:

| Area | Revision 3 | Revision 4 | Driver |
|---|---|---|---|
| `parameter_catalog` row shape and reader | `used_by` = `recovery.dataengine`; the contract file omitted `used_by`, `secret` and `value_source` | One row shape everywhere: `used_by` = `recovery.casewf.refdata (RWB-E1-043)` (the only reader, E1-043 rev 10 `ReferenceLoadAuthority`), `secret=false`, `value_source=TABLE`; P1 `dataengine` stated as not a reader; contract file and TC-20 aligned | Finding 025 |
| MSG v4 placeholders | K0-H/K0-R named `{check}` only; K4/K5 named `{field}` and `{values}` only | `{table}` = `data_product` in K0-H/K0-R, `{row}` = the 1-based data row in K4/K5, with the rendered texts stated and asserted | Finding 026 |

## Assumptions

Full list with evidence in `assumptions.md`. Those that shape the design:

| ID | Assumption (short) | Gap | Blocker |
|---|---|---|---|
| `ASM-E1001-13` | **DP07 business text is kept verbatim; `data_product.system_of_record` is widened to `varchar(200)` and DF-REF-074 `physical_type` to `varchar(200)`.** | `GAP-E1001-17` | **Yes** |
| `ASM-E1001-14` | **`is_personal` is seeded as the protective union: `true` where PS v6 says true or PDPA v4 says "Personal data = Yes" (526 rows); never weakened.** The 26 PS-v6-only fields stay `false` because neither source marks them; DF-REF-288/-289 are named in the ruling ask. | `GAP-E1001-18` | **Yes** |
| `ASM-E1001-01` | Dictionary and table set are PS v6 (D-RCV-36 row 18), with the D-RUN-12 creation split. | `GAP-E1001-01` | No |
| `ASM-E1001-02` | `<seq>` is assigned by the orchestrator at merge (D-RUN-07). | `GAP-E1001-02` | No |
| `ASM-E1001-05` | `DataProductCatalogHandler` implements E1-043 revision 10's P4 `access.api.ReferenceTableHandler` SPI (D-RUN-18), with Story v7 §12's three methods verbatim and E1-043's defaults (SPEC-019). | `GAP-E1001-07` | No |
| `ASM-E1001-07` | Local switch design of SPEC-010. | `GAP-E1001-11` | No |
| `ASM-E1001-15` | AC10: the repeat is answered by E1-043's L9 with 409 MSG-P1-011 from `repeatMessage`, nothing written; a 201 body with a message field is not needed. | `GAP-E1001-13` | No |
| `ASM-E1001-17` | Three provisional field IDs DF-REF-300..302 for the columns E1-042 adds to `parameter_value`; DF-REF-301 `physical_type` is `char(64)`. | `GAP-E1001-20` | No |
| `ASM-E1001-20` | `supportsRollback()` is `false` (the SPI default): Story v7 defines no rollback for `data_product`, so a wrongly approved catalog is corrected by a later `valid_from`. | `GAP-E1001-24` | No |

`L-RCV-03`: no question was asked. Gaps are in `document-gaps.md`; proposed shared rows in `shared-updates.md`.

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — Story v7 §15: "No screen in this story". |
| Logic In Scope | `YES` — catalog validation (BR2, BR3, BR5, list values), versioned apply, conformance and seed-integrity tests. |
| API In Scope | `YES` — the catalog load uses the existing `POST /admin/reference-loads` and its approve operation (API v4), owned and built by RWB-E1-043 (D-RUN-10, D-RUN-11). No endpoint, request or response schema is added or changed. |
| API Impact Type | `NO_API_CHANGE` — the repeat is answered by a 409 `Problem` carrying MSG-P1-011 (E1-043 rev 10 SPEC-025 L9), which API v4's `E409` already describes; no message field is added to `ReferenceLoad`. |
| Impacted Existing Nodes | `backend/src/main/resources/db/modulemigration/recovery/` (adds this story's file after the E1-042 and E1-043 files); `backend/src/main/resources/config/parameter-catalog.csv` (the two `rwb.refload.*.data_product` rows of SPEC-019); `infra/postgres/init/10-load-ace-database.sh`, `docker-compose.yml`, `.env.example`, `application.yaml` (`rwb.flyway.enabled`), `README.md` "Local versus target", migration-folder `README.md` (SPEC-010); `RecoveryDatabaseIT` (container mode, SPEC-010); E1-043 `ReferenceTableHandlers` (the bean is collected by type; no E1-043 code change); E1-042 `FixedMessageCatalog` (four message IDs added, SPEC-015). |
| New Nodes Required | `YES` — `V<seq>__rwb_e1_001_recovery_schema.sql`; nested module `dataengine` with `api/` and `internal/catalog` (`DataProduct`, `DataProductRepository`, `DataProductCatalogHandler`); the `parameter_catalog` upsert block in the migration (SPEC-019); `DataDictionaryConformanceTest`; `SeedIntegrityIT`; `RecoverySchemaMigrationIT` (tag `recovery-it`); flag `rwb.p1.data-catalog`. |
| Inherited Existing Behavior | `casewf.migration.RecoveryFlywayConfig` (history table `flyway_schema_history_recovery` in schema `recovery`, `${recoverySchema}`, `baselineOnMigrate(true)`, baseline `0`, `createSchemas(false)`, clean disabled); migration lint (E1-044, incl. D-RUN-13 literal rule); `20-grants.sql.inc` default privileges; `access.internal.ApiExceptionHandler` 403 → MSG-P4-002 and 404 → MSG-P4-003; E1-042 `access.api.MessageResolver`; E1-043 endpoint, method checks, content hash, maker-checker, dispatch (SPEC-019). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` — migration, entity, repository, handler and its registration, flag, local-switch scripts, tests. |
| Module scope (for the plan gate) | One ACE (recovery) module. Code in P1 `dataengine` (`api/`, `internal/catalog`); imports only P4 `access.api` types (SPI, `MessageResolver`, `ApiProblemException`, `ApiError`); no `casewf` import, so no P1 → P3 edge (D-RUN-18). Under D-RUN-21 (orchestrator run decision, not a human ruling; ratification OPEN-050) "touches one module" in AGENTS §7 and §9 means the ACE module, so the plan does not go back to the analyst. No common or collection module is touched. |

## Requirement-to-SPEC Logic Coverage

Status values: `COVERED`; `COVERED (ASM)` = covered on a labelled assumption whose gap is Blocker = Yes
(the rule is implemented and tested; the human ruling may change seed data only); `PARTIAL` = part of
the statement depends on another story's open decision, named in the notes.

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every table and view column has exactly one dictionary row with field ID, types, source and meaning. | 006, 009 | DIRECT | 1,382 rows; conformance on tables (Flyway history table excluded, `ASM-E1001-16`); view columns are E1-069's (BR9). | COVERED |
| BR2 | Workbench data is held in the 14 data products DP01–DP14. | 004, 006, 013 | DIRECT | Seed 14 rows; load must hold exactly DP01–DP14 (K1). | COVERED |
| BR3 | One system of record in the stated form and one named owner per product. | 004, 013, 018 | DIRECT | Closed forms F1–F3 (`ASM-E1001-09`); owner user ID required; DP07 seed fits only under `ASM-E1001-13`. | COVERED (ASM) |
| BR4 | Catalog values are a versioned load; a load with any exception is refused in full. | 013, 014 | DIRECT | `validate` writes nothing; `apply` is one transaction; versioning is E1-043's. | COVERED |
| BR5 | A multi-source product names ACE and its sources; a bare source name is refused. | 013 | DIRECT | F1/F2 require `ACE (ingested from …)`; per-product source lists not machine-checked (`ASM-E1001-09`). | COVERED |
| BR6 | Parameterised schema, one migration per story, forward only. | 001, 002, 008 | DIRECT | `${recoverySchema}` only; lint is E1-044's (D-RUN-13). | COVERED |
| BR7 | Personal fields carry `is_personal = true` so masking (RWB-E1-016) and the PDPA lint (RWB-TE-011) can read them. | 002 (T10), 006, 018 | DIRECT | Not "PS v6 as written" (run 1): seeded as the protective union of PS v6 and PDPA v4, 526 rows incl. all 17 Restricted fields, as literal INSERT values with no `UPDATE` (T10); tests TC-E1-001-14 and TC-E1-001-17 (TE-011 lint, zero findings). No later load can remove a mark: E1-043's `sys_fields` handler (RWB-E1-064) refuses any `is_personal` change and never writes the column (E1-043 SPEC-031; SPEC-019 item 10). | COVERED (ASM) |
| BR8 | No constraint into `public`; ACE links are `varchar(255)` keys with no FK. | 003 | DIRECT | 18 link columns listed; 0 FKs on them; 0 constraints into `public`. | COVERED |
| BR9 | The migration seeds the dictionary for tables and the 30 views before the views exist. | 006, 002 | DIRECT | 30 view objects, 304 view fields; no view created. | COVERED |
| AC1 | Schema deployed: table set, removed tables absent, no constraint into public, business keys, conformance. | 002, 003, 009, 010 | DIRECT | Counts per the counting table. | COVERED |
| AC2 | `v_data_dictionary` returns the stated rows for `v_ace_account.days_past_due` and `account_ext.dispute_open`. | 005, 006 | DIRECT | View per Story v7 §12 / Rulings v2 R2. | COVERED |
| AC3 | After the catalog load, 14 rows with the stated DP01, DP03 and DP06 values. | 013, 014, 017, 019 | DIRECT | End-to-end through the E1-043 endpoint (BS v6 order 8, earlier): L1–L12 pass, L13 calls `validate`, approval calls `apply` (SPEC-019). | COVERED |
| AC4 | A failing statement rolls the whole migration back; no successful history row. | 007 | DIRECT | One transaction. | COVERED |
| AC5 | Conformance test fails on a column with no dictionary row and on a type mismatch, with the stated texts. | 009 | DIRECT | Texts fixed; `char(n)` is the canonical form. | COVERED |
| AC6 | A re-run applies nothing and leaves counts unchanged. | 008 | DIRECT | 123 / 1,382. | COVERED |
| AC7 | Two systems of record (DP06) and no owner (DP11) refuse the load with MSG-P1-003 for both. | 013, 015 | DIRECT | All findings reported; neither defect is a K0 finding (SPEC-013), so `messageCode` is MSG-P1-003. | COVERED |
| AC8 | 13 rows without DP09 refuse the load with MSG-P1-004 naming DP09. | 013, 015 | DIRECT | — | COVERED |
| AC9 | Owner role and refresh cycle outside their lists refuse the load with two MSG-P1-007 texts. | 013, 015 | DIRECT | Both texts exactly as Story v7 AC9; LOV-ROLE resolved through `role` (`ASM-E1001-10`) for the check only. | COVERED |
| AC10 | The same file again writes nothing and the response carries MSG-P1-011. | 014, 015, 019 | DIRECT | `repeatMessage` → L9 answers 409 `Problem` MSG-P1-011 (E1-043 SPEC-025 L9), nothing written, any business date. The 409 form is recorded as a deviation (`GAP-E1001-13`, Blocker No). | COVERED |
| AC11 | A bare source name ("CCMS") refuses the load with the MSG-P1-003 text. | 013, 015 | DIRECT | Fails F1–F3. | COVERED |
| X1–X3 | Migration failure, conformance failure, re-run. | 007, 008, 009 | DIRECT | Pipeline log only. | COVERED |
| X4–X7 | Catalog refusals and repeat file. | 013, 014, 015 | DIRECT | X4 single-defect cases in TC-18/19; X7 message as AC10. | COVERED |
| X8 / TC-E1-001-11 | A role without Reference data C gets 403 with MSG-P4-002; the refusal is in the access log. | 016, 019 | INHERITED + SEAM | 403/MSG-P4-002, nothing written, and one REFUSED `event=REFERENCE_LOAD_AUDIT` line with `table = data_product` (E1-043 SPEC-028) asserted here; the persistent access-log entry is RWB-E1-039's (BS v6 order 28, later; D-RUN-08), `GAP-E1001-22`. | COVERED (403 + interim audit); access log = seam |
| §10 Authority | RW-REFADM loads (C); RW-DATASTEW confirms; pipeline identity migrates. | 014, 016, 019 | DIRECT + INHERITED | Approver right conflict `GAP-E1001-08`; the loader and approver lists are the two catalog keys this story supplies (SPEC-019); maker-checker MSG-P7-002 and AC-VERS decision log inherited from E1-043/API v4. | COVERED |
| §12 Contract | View columns; handler interface; 422/403 responses; idempotency; migration trigger/restart. | 005, 012–015, 019 | DIRECT | Handler implements the P4 SPI (D-RUN-18); registration and dispatch are E1-043's (SPEC-019). | COVERED |
| §13 Solution plan | Components, database, feature flag, build steps 1–7. | 001–010, 012–019 | DIRECT | Path, package and message table per repo seams (`GAP-E1001-10`, `-14`). | COVERED |
| §17 Guardrails | No business value in code; no personal data; no ACE table read; no constraint into public; dictionary reads only recovery tables. | 003, 005, 017, 019 | DIRECT | F3 is a grammar, not a value list, so a catalog reword is not a code change. | COVERED |
| §19 Out of scope | `v_ace_*` views, grants and view conformance (E1-069); freshness (E1-015); access/masking (E1-016); retention (E1-017); Stage 2; dictionary endpoint (E1-064). | 002, 010 | DIRECT | Excluded; views-only local stand-in retired by E1-069 (SPEC-010). | COVERED |
| NFR-RWB-005 Security | Method security, audit. | 016 | INHERITED | Endpoint checks are E1-043's; migration as `rwb_migrator` only (ADR-010). | COVERED |
| NFR-RWB-006 Privacy | PDPA classification; no personal data. | 006, 017, 018 | DIRECT | BR7 union; synthetic UUIDs only. | COVERED (ASM) |
| NFR-RWB-008 Observability | Logs per job. | 007 | DIRECT | Failing statement in the Flyway log (X1). | COVERED |
| NFR-RWB-009 Operability | Flag-off path; rollback by tag. | 008, 017, 019 | DIRECT | Flag off → handler bean absent → `data_product` is an unknown code (422 MSG-P3-027, E1-043 SPEC-025); forward-only migration. | COVERED |
| NFR-RWB-001..004, -007, -010 | Availability, performance, throughput, recovery, accessibility, retention. | — | NOT_APPLICABLE | No runtime read path with a target, no screen, no retained record class in this story (retention is RWB-E1-017). | N/A |

## User story intent interpretation

Create the recovery schema's tables and the data dictionary as one forward-only migration taken from
PS v6, publish the dictionary as a view, and let the reference data administrator load the catalog of
the 14 data products as versioned reference data that is refused in full on any error. The story
creates no screen, reads no ACE table and creates no `v_ace_*` view (Story v7 §15, §17, §19).

## Entry trigger and preconditions

| Trigger | Preconditions |
|---|---|
| Recovery Flyway runs at application start (`casewf.migration.RecoveryFlywayConfig`, `initMethod = "migrate"`) when `rwb.flyway.enabled=true`. | Schema `recovery` exists (DBA; `createSchemas(false)`); extension `pgcrypto` exists; `rwb_migrator` holds DDL; the E1-044 lint passes; **the E1-042 and E1-043 migrations are already applied** (BS v6 orders 3 and 8 precede 9; D-RUN-12), so `parameter_catalog`, `parameter_value`, `reference_version` and `reference_row` exist. |
| `POST /admin/reference-loads` with `table = data_product`, then approve (API v4; E1-043). | E1-043 revision 10 built (its endpoint, dispatcher, registry and checks); this story's `parameter_catalog` rows present (`rwb.refload.loader.data_product`, `rwb.refload.approver.data_product`); flag `rwb.p1.data-catalog` on, so the handler bean exists and E1-043 collects it by the P4 SPI type; caller holds Reference data C (load) and the approver holds A (approver right still `GAP-E1001-08`). E1-043's own checks L1–L12 run first (E1-043 SPEC-025); no `refdata.columns.data_product` exists, so L12 is skipped (SPEC-019). |
| Query of `v_data_dictionary` by a developer or data steward. | Read access to schema `recovery` (Story v7 §3). |

## Detailed design

### SPEC-RWB-E1-001-001 Migration file identity

- Location `backend/src/main/resources/db/modulemigration/recovery/` (RUN-BRIEF local stack facts;
  Story v7 §13 `db/migration/recovery` superseded, `GAP-E1001-10`).
- Name `V<seq>__rwb_e1_001_recovery_schema.sql`; line 1 exactly `-- Story: RWB-E1-001`; no
  `-- Fix:` line. `<seq>` is the next four-digit number in merge order, **assigned by the orchestrator at
  merge**; no spec, plan or file fixes it (D-RUN-07; DL v10 D-RCV-28; `ASM-E1001-02`). The E1-044 lint
  requires a contiguous sequence from V0001.
- The file's content is fixed (SPEC-002) and does not depend on its number. Tests identify the
  migration by script name and `success = true` in `flyway_schema_history_recovery`, never by a version
  literal. Story v7's "Flyway version 1.001" and "V0001" are read as "this migration" (`GAP-E1001-04`).

### SPEC-RWB-E1-001-002 Derivation from Physical Schema v6

The migration body is PS v6 lines 16–6130 in file order, transformed as follows and nothing else:

| # | PS v6 content | Treatment | Basis |
|---|---|---|---|
| T1 | Lines 10–12 `CREATE SCHEMA IF NOT EXISTS recovery`, `SET search_path TO recovery`, `CREATE EXTENSION IF NOT EXISTS pgcrypto` | Removed | `createSchemas(false)`; lint L-SEARCH-PATH (E1-044); extension is an environment precondition |
| T2 | Every reference to a recovery object | Qualified `${recoverySchema}.<name>`; no literal schema outside string literals and comments | D-RCV-28; D-RUN-13 |
| T3 | Line 2156 `CREATE VIEW v_data_dictionary` | Replaced by SPEC-005 | Story v7 §12; Rulings v2 R2 |
| T4 | Lines 3516–3531 `data_product` seed | Replaced by the SPEC-006 values | `ASM-E1001-04` |
| T5 | Lines 5340–5348 `rule_package` seed (8 rows) | Not carried | `ASM-E1001-03`; `GAP-E1001-19` |
| T6 | From line 6131 (`-- ACE source views. Section A ships as V0002…`): `ace_to_date`, `ace_to_boolean`, `ace_mask_value`, the 30 `v_ace_*` views, the commented grants (line 6823) | Not carried | Story v7 §3, §12 "Includes", §19 (RWB-E1-069) |
| T7 | Any `GRANT` / `REVOKE` | None | Lint L-GRANT (E1-044); `20-grants.sql.inc` default privileges |
| T8 | Objects of tables an earlier-merged story creates: `CREATE TABLE parameter_catalog` (line 1386), `parameter_value` (1413), `reference_version` (1437), `reference_row` (1471); `fk_reference_row_version_id` (line 2242); `ix_reference_row_version_id` (line 2347); the 4 `COMMENT ON TABLE` (lines 2426–2429) and the 53 `COMMENT ON COLUMN` statements on those four tables | Not carried. Their 4 `sys_objects` and **53** `sys_fields` rows **are** carried (4 + 53 = the 57 comment statements; finding 018 correction). The FKs from `retention_rule`, `document_type`, `document_checklist_item` and `document_hub_parameter` to `reference_version` (lines 2228, 2244, 2245, 2248) **are** carried: they belong to this story's tables and the target exists | D-RUN-12; E1-042 spec revision 13 §12.3; E1-043 spec revision 10 SPEC-001 |
| T9 | Line 820 `system_of_record varchar(120) NOT NULL`; the `sys_fields` row DF-REF-074 (`physical_type` `varchar(120)`) | `varchar(200)` in both. A ruling that widens must also update Logical Data Model and Data Dictionary v8 line 561 (DF-REF-074, length 120) — cited in `GAP-E1001-17` | `ASM-E1001-13` (Blocker gap 17) |
| T10 | `is_personal` value in the `sys_fields` seed | Set per SPEC-006 (protective union), **written as the literal `true` / `false` in the `is_personal` position of each `INSERT INTO ${recoverySchema}.sys_fields (<column list>) VALUES (...)` row**, keeping PS v6's named column list. No `UPDATE ... SET is_personal` statement (single or bulk `WHERE field_id IN (...)`) appears in the migration, so the RWB-TE-011 PDPA lint, which parses INSERT values by column name (TE-011 spec SPEC-TE011-001), reads every mark | `ASM-E1001-14` (Blocker gap 18); orchestrator cross-story input from RWB-TE-011 spec gate round 4 |
| T11 | — (addition) | Three `sys_fields` rows for the E1-042 columns (SPEC-006) | `ASM-E1001-17` |

No `IF NOT EXISTS`, `DROP`, `CONCURRENTLY` or data outside `${recoverySchema}` is added (Story v7
§17). The file does not guard against objects that already exist: the T8 list is the complete set of
pre-existing objects, so an unexpected duplicate fails the migration (AC4) rather than being skipped.

### SPEC-RWB-E1-001-003 Table set, constraints and business keys

- Creates the 89 PS v6 tables not in T8, including `data_product`, `sys_objects`, `sys_fields`,
  `lov_value`, `role`, `permission`, `rule_package`, `rule_package_version`, `decision_log`,
  `interaction` and the extension tables `party_ext`, `contact_point_ext`, `account_ext`,
  `valuation_ext` (D-RCV-35 U3; names under OPEN-033). With T8 the schema then holds the 93 PS v6
  tables (D-RCV-36 CR A.7).
- None of the 20 tables named in AC1, and no `payment_match_rule` (D-RCV-36 T10).
- 91 foreign keys (PS v6 §"References between tables" from line 2182, minus T8), all between recovery
  tables; 111 indexes; the 3 CHECK constraints (`rule_package.hit_policy`, `rule_package_version.status`,
  `contact_point_ext.contact_type`); `refuse_change()` and the triggers `tr_declog_append_only` and
  `tr_interaction_append_only` (line 2389); the `COMMENT ON` statements from line 2398 minus T8.
- No constraint references schema `public` (PS v6 has none). The 18 ACE link columns are
  `varchar(255)` and take part in no foreign key (BR8): `account_key` on `account_ext`,
  `case_account`, `case_entry_exclusion`, `case_list_row`, `debt_sale_account`; `person_key` on
  `case_party`, `document`, `interaction`, `notice`, `party_ext`, `signature_request`;
  `recovery_case.primary_person_key`; `asset_key` on `asset_sale`, `listing`; `contact_key` on
  `contact_point_ext`, `interaction`; `proceeds.payment_code`; `valuation_ext.valuation_key` (primary key,
  no FK). Derived from the PS v6 `varchar(255)` columns before line 6131; the 19th such column,
  `document_intake.file_name`, is not a link.

### SPEC-RWB-E1-001-004 `data_product` table

As PS v6 line 815 except T9: `id uuid PRIMARY KEY DEFAULT gen_random_uuid()`, `product_code
varchar(25) NOT NULL` with `uk_data_product UNIQUE (product_code)`, `product_name varchar(80) NOT NULL`,
`definition varchar(400) NOT NULL`, **`system_of_record varchar(200) NOT NULL`** (`ASM-E1001-13`),
`owner_role varchar(20) NOT NULL`, `owner_user_id uuid`, `refresh_cycle varchar(10) NOT NULL`,
`expected_by varchar(20)`, `valid_from date NOT NULL`, and the seven standard columns. Story v7 §13
names `product_code` as primary key; PS v6 governs because Story v7 §11 counts 10 fields DF-REF-070
to 079 including `id` (`GAP-E1001-09`). `fk_sys_objects_data_product` references `data_product
(product_code)`; `sys_objects.data_product` is nullable (Rulings v2 R1; PBR v2 §2 Q1). `data_product`
rows are inserted before `sys_objects` (PS v6 line 3516).

### SPEC-RWB-E1-001-005 `v_data_dictionary`

Created by the migration, reading only `sys_fields`, `sys_objects` and `data_product`:

```sql
CREATE VIEW ${recoverySchema}.v_data_dictionary AS
SELECT o.object_name AS entity, f.field_name AS field, f.field_id, f.data_type, f.physical_type,
       f.is_mandatory, f.lov_code, f.references_object, f.source_system, f.source_field,
       f.is_personal, o.data_product, o.system_of_record AS entity_system_of_record,
       p.system_of_record AS product_system_of_record, p.refresh_cycle, p.owner_role,
       p.owner_user_id, f.late_behavior, f.interface_id, f.description
FROM ${recoverySchema}.sys_fields f
JOIN ${recoverySchema}.sys_objects o ON o.object_name = f.object_name
LEFT JOIN ${recoverySchema}.data_product p ON p.product_code = o.data_product AND p.is_active
WHERE f.is_active AND o.is_active;
```

Columns per Story v7 §12; `owner_role` from `data_product` and the two system-of-record columns per
Rulings v2 R2 §3.3 and PBR v2 §3 Q2. The PS v6 view (`f.owner_role`) is not used (`GAP-E1001-03`).

### SPEC-RWB-E1-001-006 Seed rows

| Table | Rows | Source |
|---|---|---|
| `data_product` | 14: DP01–DP14 with code, name, definition, system of record, refresh cycle and expected-by exactly as the Story v7 §13 seed table (verbatim, including the 139-character DP07 value); `owner_role = 'RW-DATASTEW'`; `owner_user_id` NULL; `valid_from = DATE '2026-11-30'` | Story v7 §13; `ASM-E1001-04`, `-13` |
| `sys_objects` | 123 as PS v6 (93 tables incl. the 4 of T8, 30 views; 24 with NULL `data_product`) | PS v6; D-RCV-36 |
| `sys_fields` | 1,379 as PS v6 (DF-EXT-001..049, DF-REF-274..299, the 304 `DF-ACE-*` view fields), with T9 and T10 applied; plus 3 provisional rows: `DF-REF-300` `parameter_value.load_id` (`UUID`, `uuid`), `DF-REF-301` `parameter_value.content_hash` (`TEXT`, `char(64)`), `DF-REF-302` `parameter_value.rollback_reason` (`TEXT`, `varchar(400)`); source system `Workbench`; `is_personal` false; descriptions from E1-042 spec revision 13 §7 field matrix, each prefixed "Provisional field ID (RWB-E1-001 ASM-E1001-17)." | PS v6; D-RCV-36 CR A.5; `ASM-E1001-17`; E1-042 revision 13 §12.3 |
| `sys_fields.is_personal` | `true` for exactly the 526 field IDs in `evidence/is_personal_union_v4.tsv` (14 true in both sources, 4 true in PS v6 only, 508 "Personal data = Yes" in PDPA v4 only), including all 17 PDPA v4 Restricted fields (12 Direct identifier, 5 Sensitive); `false` for the other 856. The value is the literal in each row's INSERT (T10), never a later `UPDATE` | `ASM-E1001-14` |
| `lov_value` | 598 as PS v6 (from line 4684) | DL v10 D-RCV-29; E1-043 revision 10 §"Seed ownership" |
| `role` | 54 as PS v6 (from line 5284) | DL v10 D-RCV-29 |
| `permission` | 421 as PS v6 (from line 5350) | DL v10 D-RCV-29 |
| `delegation_limit` | 0 | DL v10 D-RCV-29; Rulings v2 R3; PBR v2 §4 Q3 |
| `rule_package`, `rule_package_version` | 0 | `ASM-E1001-03` |
| Every other table | 0 | Story v7 §11 |

No seed row carries personal data. Owner user IDs exist only in environment load files (synthetic
users in DEV and SIT, Story v7 §3).

**The marks cannot be removed by a later load (finding 017).** `sys_fields` is written by this
migration only. Later dictionary changes are reference loads (DL v10 D-RCV-29) handled by RWB-E1-064's
`sys_fields` handler, whose stated protective requirement (E1-043 revision 10 SPEC-031; its
`shared-updates.md` §3.2 item 3) refuses any file that changes `is_personal` and never writes the column
in `apply` or `onRolledBack`; its approver list is RW-COMPLY (E1-043 A-36, inferred). A mark can
therefore change only by a reviewed migration (a change to this story's file before merge, or a later
story's file), which is a human-reviewed pull request. The governed path for changing a mark is open
item OPEN-NEW-7 with RW-COMPLY, linked to E1-043 R4 (`GAP-E1001-18`, `GAP-E1001-23`).

### SPEC-RWB-E1-001-007 Atomic migration

The file runs in one PostgreSQL transaction (Flyway default; SPEC-002 forbids non-transactional
statements). If any statement fails, Flyway logs the failing statement (NFR-RWB-008), no object or row
of the migration remains, and `flyway_schema_history_recovery` has no row with `success = true` for it
(AC4, X1). The E1-042 and E1-043 objects applied earlier are untouched. A restart applies the whole
file again (Story v7 §12 "Restart").

### SPEC-RWB-E1-001-008 Re-run and checksum

A second `migrate` applies nothing; `sys_objects` stays at 123 and `sys_fields` at 1,382 (AC6, X3). A
changed checksum on the applied file fails Flyway validation (Story v7 §12; AGENTS §4.6).

### SPEC-RWB-E1-001-009 `DataDictionaryConformanceTest`

Runs against the Flyway-built schema (SPEC-010) and compares `information_schema.columns` for every
base table in `${recoverySchema}` except Flyway's own history table `flyway_schema_history_recovery`
(created by `RecoveryFlywayConfig` in the same schema; not a Workbench table; `ASM-E1001-16`) with the
`sys_fields` rows whose `object_name` is that table:

| Check | Pass condition | Failure text (Story v7 AC5) |
|---|---|---|
| C1 column → field | Every column except the seven standard columns has exactly one `sys_fields` row: 1,050 of 1,050. | `<table>.<column> has no data dictionary entry` |
| C2 field → column | Every `sys_fields` row on a table names an existing column: 1,078 of 1,078. | `<field_id> has no column <table>.<field>` (`ASM-E1001-11`) |
| C3 type | For each pair, the normalised column type equals `physical_type`: `varchar(n)`, `char(n)` (catalog `bpchar`; PostgreSQL records both `char(n)` and `character(n)` as `bpchar(n)`, so the test normalises to `char(n)`), `numeric(p,s)`, `integer`, `bigint`, `smallint`, `boolean`, `date`, `timestamptz`, `uuid`, `text`, `jsonb`, arrays as `<type>[]`. An unlisted type fails as a mismatch. | `<field_id> physical type <expected> expected, <actual> found` |

Every failure is reported. Views are out of scope (BR9; RWB-E1-069). Proof fixtures on a throwaway
container schema, never in the migration folder: an extra `account_ext.branch_code` column (C1),
`account_ext.dispute_open` altered to `text` (C3), and a `char(64)` column matched to a `char(64)`
`physical_type` (C3 pass; DF-REF-301 and the 9 PS v6 `char(n)` rows use the same form).

### SPEC-RWB-E1-001-010 Local switch from the reference load to a Flyway-built schema

Today `RWB_LOAD_REFERENCE_SCHEMA` defaults to `true` in `.env.example`, `docker-compose.yml`
(`${RWB_LOAD_REFERENCE_SCHEMA:-true}`) and `10-load-ace-database.sh`, so PS v6 (tables and views) is
loaded at init; recovery Flyway then baselines at `0` and, once this story's file exists, fails on
"relation already exists" (X9). `application.yaml` fixes `rwb.flyway.enabled: true` with no
environment override. This story makes the following change, effective at its merge:

| Switch | Values | Default after this story | Owner of later change |
|---|---|---|---|
| S1 `RWB_LOAD_REFERENCE_SCHEMA` (init) | `true`: load all of PS v6 (unchanged behaviour). `false`: create schema and extension only | **`false`** in `.env.example`, `docker-compose.yml` (`${RWB_LOAD_REFERENCE_SCHEMA:-false}`) and the script default | RWB-E1-069 may retire `true` |
| S2 `RWB_LOAD_REFERENCE_VIEWS` (init, new) | Read only when S1=`false`. `true`: run PS v6 from the line `-- ACE source views. Section A ships as V0002…` to end of file, preceded by `SET search_path TO recovery;` as PS v6 line 11 does, with the same `ON_ERROR_STOP` strictness as S1 (Tier 2 probe rule). The PS v6 file is read, never edited. `false`: no views | **`true`** (views-only stand-in for V0002/V0003) | **RWB-E1-069** flips it to `false` and removes the branch when its view migrations merge (hand-off below) |
| S3 `RWB_FLYWAY_ENABLED` (application, new mapping) | `rwb.flyway.enabled: ${RWB_FLYWAY_ENABLED:true}` in `application.yaml` | `true` | — |

Valid combinations: S1=`false` with S3=`true` (default: Flyway builds every table; views come from S2);
S1=`true` only with S3=`false` (reference browsing; the application starts without recovery Flyway).
S1=`true` with S3=`true` is refused: `10-load-ace-database.sh` prints that recovery Flyway must be off
in reference mode (README), and the application fails fast on the first migration (X9). `20-grants.sql.inc`
is unchanged: in views-only mode it sets the view owner and grants exactly as in reference mode, and its
`ALTER DEFAULT PRIVILEGES FOR ROLE rwb_migrator` gives `recovery_svc` DML on the tables Flyway creates.
An existing local volume keeps its old contents: README tells developers to run
`./scripts/dev.ps1 reset` and then `up` after this story merges.

Test stages and schemas:

| Stage | Schema it runs against |
|---|---|
| `./scripts/dev.ps1 test` (unit, Modulith, lint) | No database |
| `RecoverySchemaMigrationIT` (new, `recovery-it`) | S1=`false`, S2=`false`: empty schema; Flyway applies E1-042, E1-043 and this migration. Proves AC1, AC2 (synthetic owner fixture), AC4, AC5, AC6, T6/T8 (no `v_ace_*`, no `ace_to_date`; the four T8 tables exist exactly once) |
| `RecoveryDatabaseIT` (existing) | Moves from S1=`true` to S1=`false`, S2=`true`. Every assertion is kept: 30 `v_ace_*` views, 0 visible `public` tables, views read-only and owned by `ace_view_owner`, the baseline row `version = '0'` (`ASM-E1001-18`), decision log append-only (now the trigger from this migration), identity split |
| `DataDictionaryConformanceTest`, `SeedIntegrityIT` | Same container as `RecoverySchemaMigrationIT` |
| Earlier stories' ITs that run recovery Flyway on an S1=`true` container (E1-042 TC-E1-042-14; E1-043 PS v6 baseline test) | Must pin their run to the migrations merged before this story (Flyway target) or move to S1=`false`, so they keep proving the guarded DDL without meeting this file. Coordination item OPEN-NEW-9; no assertion is removed |
| `./scripts/dev.ps1 e2e` and the local stack | Defaults: S1=`false`, S2=`true`, S3=`true` |

Hand-off to RWB-E1-069 (answers REVIEW-RWB-E1-069-107 from this side): when V0002/V0003 merge, E1-069
sets S2 default `false`, deletes the S2 branch, applies its Flyway-mode grants (E1-069 SPEC-015(a)), and
runs the `RecoveryDatabaseIT` view and grant assertions against Flyway-created views. Until then the
S2 stand-in is the only source of the 30 views locally. E1-069 decides whether S1=`true` survives. The
README "Local versus target" row "Recovery schema" becomes "Flyway (E1-042, E1-043, E1-001
migrations); PS v6 view section at init until RWB-E1-069 (`RWB_LOAD_REFERENCE_VIEWS`)", and the
migration-folder README text is aligned with E1-044 SPEC-015 (OPEN-NEW-9). Two points of E1-069
SPEC-015 are stale against this design and are named in OPEN-NEW-9: (i) its (a) says E1-069 flips
`RWB_LOAD_REFERENCE_SCHEMA` to `false`, while this story flips it at its own merge (S1) and E1-069 only
decides whether reference mode survives; (ii) its (c) says the `RecoveryDatabaseIT` version-`0` baseline
assertion is "replaced", while this story keeps it in the S2 stage (`ASM-E1001-18`) and E1-069 keeps it
in the same stage. `ASM-E1001-07`, `GAP-E1001-11`.

### SPEC-RWB-E1-001-011 (retired)

Run 1 changed `RecoveryMigrationLintTest` to ignore string literals. D-RUN-13 makes that rule part of
the lint owned by RWB-E1-044 (its SPEC-007; test T-044-21 proves `INSERT INTO
${recoverySchema}.sys_fields (source_field) VALUES ('public.account.account_key')` passes and
`public.` identifiers fail). This story changes no lint code and inherits the rule. The ID is not
reused.

### SPEC-RWB-E1-001-012 Module, entity and repository

- New nested module `th.co.scb.ace.demo.recovery.dataengine` with `api/` and `internal/` (P1 name per
  the RWB-TE-001 module map). Story v7 §13 package `recovery.dataengine.catalog` maps to
  `dataengine.internal.catalog` (`GAP-E1001-10`).
- `DataProduct` (JPA entity on `${recoverySchema}.data_product`) and `DataProductRepository` (find all
  active, find by `product_code`). No other module reads `data_product` directly (AGENTS §3.11).
- Module dependencies, named by the package that publishes each type **after RWB-TE-001 v4** (its
  SPEC-022 relocation table; there is no `platform` package any more): `dataengine` → P4 `access.api`
  (`ReferenceTableHandler` and the other SPI records, `MessageResolver`, `ApiProblemException`,
  `ApiError`). It imports nothing from `recovery.casewf..`, so no P1 → P3 edge exists (D-RUN-18;
  E1-043 revision 10 SPEC-019 rule (3)). No dependency in the other direction; `ModulithTest.verify()`
  passes. The Flyway configuration is `casewf.migration.RecoveryFlywayConfig` (TE-001 SPEC-022) and is
  not a dependency of this module.

### SPEC-RWB-E1-001-013 `DataProductCatalogHandler`: the handler and its checks

`DataProductCatalogHandler` is a Spring bean of the P4 type `recovery.access.api.ReferenceTableHandler`
(published under D-RUN-18; E1-043 revision 10 SPEC-025). Story v7 §12's three methods are implemented
verbatim, plus the SPI defaults this story relies on (`ASM-E1001-05`, `ASM-E1001-20`):

| Method | This story | Called by E1-043 |
|---|---|---|
| `tableCode()` | `"data_product"` | At start-up, to build the `tableCode → handler` map (SPEC-025 *Registration*) |
| `validate(ReferenceLoadFile)` | Checks K0–K5 below, writes nothing, returns `ValidationReport` | At load, check L13, after L1–L12 (SPEC-025) |
| `apply(UUID loadId, ReferenceLoadFile, LocalDate validFrom)` | SPEC-014 | In the approve transaction (SPEC-008 / SPEC-025 *Approve*) |
| `keyColumns()` | `List.of("product_code")` | For `row_key` and `content_hash` (SPEC-025) |
| `repeatMessage(ReferenceLoadFile)` | `HandlerMessage("MSG-P1-011", {source = "data product catalog", date = validFrom})` | At L9, before the valid-from check (SPEC-006 rule 1) |
| `dating()` | `Dating.CURRENT_STATE` (PS v6 `uk_data_product`; GAP-54 in E1-043) | Approval refused while `validFrom` is after the business date (SPEC-032 rule 6) |
| `supportsRollback()` | `false` (the SPI default; Story v7 defines no rollback) | A rollback of a `data_product` load is refused 409 (E1-043 SPEC-024 rule 7); `GAP-E1001-24` |
| `changeSummary` | `List.of()` (the default) | Audit/version log; no field list is needed |

E1-043 supplies the `ReferenceLoadFile` (its `columns` and `rows` from the CSV/XLSX) and reads the
`ValidationReport`; it never calls this story's repository, entity or any `casewf` type. All findings
are returned in this order: file-level checks (K0-H, K1), then rows in file order, each row's K0-R, K2,
K3, K4, K5.

| Check | Level | Rule | Message |
|---|---|---|---|
| K0-H | File (row 0) | The header is exactly `product_code, product_name, definition, system_of_record, owner_role, owner_user_id, refresh_cycle, expected_by`, each column once, in this order | MSG-P3-027, `{table}` = `data_product`, `{check}` = "the header must hold the 8 catalog columns" |
| K1 | File (row 0) | The set of non-empty `product_code` values equals DP01–DP14, each once; an unknown code is refused by the same check | MSG-P1-004, `{products}` = missing codes ascending |
| K0-R | Row | Each of `product_code`, `product_name`, `definition`, `owner_role`, `refresh_cycle` has a value, and every value fits its column width (SPEC-004) | Empty value: MSG-GEN-001 `{field}`; too long: MSG-P3-027, `{table}` = `data_product`, `{check}` = "value too long for {column}" |
| K2 | Row | `system_of_record` matches F1–F3 below. **An empty value is this check, not K0** (Story v7 X4) | MSG-P1-003, `{product}` = code |
| K3 | Row | `owner_user_id` has a value and is a UUID. **An empty value is this check, not K0** (Story v7 X4) | MSG-P1-003 |
| K4 | Row | `owner_role` is an active `role.role_code` (LOV-ROLE, `ASM-E1001-10`) | MSG-P1-007, `{row}` = the 1-based data row (header excluded), `{field}` = `owner_role`, `{values}` = **the role codes in LOV-ROLE** (Story v7 AC9 verbatim) |
| K5 | Row | `refresh_cycle` is a value of LOV-REFRESH in `sort_order` (PS v6 lines 5035–5038: DAILY 1, WEEKLY 2, MONTHLY 3, ON_CHANGE 4) | MSG-P1-007, `{row}` = the 1-based data row (header excluded), `{field}` = `refresh_cycle`, `{values}` = "DAILY, WEEKLY, MONTHLY, ON_CHANGE" (AC9 verbatim) |

**K0's required set is explicit (finding 016).** K0 requires the five columns above and the header;
`system_of_record` and `owner_user_id` are excluded, because Story v7 X4 and AC7 give their absence
MSG-P1-003 (K2, K3). K0 never suppresses a later check for the same row: a row with two defects reports
both. The single-defect cases are therefore unambiguous: DP11 with no owner (every other value valid)
yields exactly one finding, K3 MSG-P1-003, and the Problem's `messageCode` is MSG-P1-003; DP06 with an
empty system of record yields exactly one finding, K2 MSG-P1-003, and `messageCode` is MSG-P1-003
(TC-E1-001-18, -19). `expected_by` is optional and only width-checked.

**Structure checks are this handler's because there is no column definition.** E1-043's
`refdata.columns.data_product` key is optional (SPEC-025 item 4); this story seeds none (SPEC-019), so
E1-043's L12 is skipped and no generic `:R` or type check can preempt K2 or K3.

System-of-record forms (BR3, BR5). **Labelled assumption `ASM-E1001-09`**: derived from the 14 Story
v7 §13 seed values, AC3, AC7 and AC11; no document states a grammar. `S` = a source name: one or more
upper-case letters or digits (seed: ALS, SCBPDM, EFS, CCMS, SVAF, AMIS, RPS, LIT, WIN, COLLINS, GL) or
the phrase `the core bank`. `L` = `S`, or `S and S`, or `S, S, … and S`. `Q` = free text without `;`,
`(` or `)`. `Q3` = free text without `;`, `(` or `)`, and without any name of the `S` list.

| Form | Pattern (whole value, single spaces) | Seed rows that use it |
|---|---|---|
| F1 | `ACE (ingested from L)` | DP01, DP02, DP05, DP06, DP11, DP13 |
| F2 | `ACE (ingested from L) for Q, with Q held in the Recovery Workbench` | DP04, DP07 |
| F3 | `Recovery Workbench`, optionally followed by ` document hub` or by `, with Q3` | DP03, DP08, DP09, DP10, DP12, DP14 |

F3 is a **grammar, not a value list** (finding 021): the three seed texts are examples of its two
qualifier shapes, so a steward who rewords DP10's qualifier through a catalog load (BR4) is accepted
while a second source is still refused. Every seed value matches exactly one form (unit test over the
14 seed rows). Negative cases, each refused with MSG-P1-003: `CCMS` (AC11); `ACE (ingested from CCMS);
SVAF` (AC7 two systems); `ACE (ingested from CCMS) and CCMS`; `Recovery Workbench and ACE`;
`Recovery Workbench, with SVAF`; `ACE (ingested from )`; `ACE (ingested from ccms)`; `ACE (ingested
from CCMS) (ingested from SVAF)`; `Workbench`; an empty value (K2). Row numbers count data rows from 1.

### SPEC-RWB-E1-001-014 `DataProductCatalogHandler.apply` and idempotency

- Called by RWB-E1-043 in the approve transaction, only when `validFrom` is on or before the business
  date (E1-043 SPEC-032 rule 6; `dating()` = `CURRENT_STATE`). It writes the 14 rows in one transaction,
  matched by `product_code`, with the file values and `data_product.valid_from` = the load's `validFrom`,
  increments `version`, sets `updated_at` and `updated_by`; returns 14. Any failure rolls back all 14
  (BR4). No row is inserted or deleted after the seed (`ASM-E1001-08`). Story v7 flow step 10 is the
  source for writing at approval.
- Repeat: `repeatMessage` returns MSG-P1-011, so E1-043's L9 — before the valid-from check, for any
  business date — finds the version with the same `(table, validFrom, content_hash)` and answers
  **409 `Problem`** with `messageCode` MSG-P1-011 and `{source}` = "data product catalog",
  `{date}` = valid from; nothing is written, `validate` and `apply` are not called (E1-043 revision 10
  SPEC-025 L9 and SPEC-006 rule 1; AC10, X7). The text is Story v7 §14 / MSG v4 line 85 and MSG v4
  types it as Error, which fits 409. The departure from a 201 body carrying the message is recorded as
  `GAP-E1001-13` (Blocker No): Story v7 AC10 names no status and API v4 `ReferenceLoad` has no message
  field, so the 409 `Problem` carries MSG-P1-011 without an API change.
- A file equal to the version in force under a **different** `validFrom` is not a repeat for this
  handler: `validate` compares nothing with the stored rows, so such a file is a normal load (the new
  version is refused only if its `validFrom` is before the business date or an APPROVED version already
  has that date, E1-043 SPEC-005/-006). The narrower repeat definition is part of `GAP-E1001-13`.

### SPEC-RWB-E1-001-015 Refusal response and messages

A refused load returns HTTP 422 `application/problem+json` (API v4 `E422`, `Problem`). The handler does
not build the Problem: it returns a `ValidationReport` of `RowCheckFailure(messageCode, placeholders,
column)` rows, and E1-043 raises `ApiProblemException` through the E1-042 additive constructor (message
ID, status, placeholders, field) so that the Problem's text is resolved by `MessageResolver` (E1-042
revision 13 SPEC-022; E1-043 SPEC-025 L13): `messageCode` = the first finding's ID (SPEC-013 order);
`detail` = every finding text in order (AC7 shows DP06 and DP11; AC9 shows rows 4 and 5). E1-043 renders
the first failure and the detail and never remaps a handler ID to MSG-P3-027. A repeat is 409
(SPEC-014).

Messages are added to E1-042's interim `FixedMessageCatalog` (EN and TH), not held in this module:

| ID | English (Story v7 §14) | Thai |
|---|---|---|
| MSG-P1-003 | `{product} must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner.` | MSG v4 line 77 Thai (written for the older English text); status Proposed (`GAP-E1001-14`, OPEN-005) |
| MSG-P1-004 | `The catalog must hold the 14 data products DP01 to DP14. Missing: {products}.` | MSG v4 line 78 |
| MSG-P1-007 | `Row {row}: {field} must be one of {values}.` | MSG v4 line 81 |
| MSG-P1-011 | `The {source} load for {date} is already complete or running. It was not run again.` | MSG v4 line 85 |

MSG-P1-007's two rendered texts are Story v7 AC9 verbatim (finding 015): `Row 4: owner_role must be one
of the role codes in LOV-ROLE.` (K4, `{values}` = "the role codes in LOV-ROLE" — the 54 role codes are
not listed to the caller) and `Row 5: refresh_cycle must be one of DAILY, WEEKLY, MONTHLY, ON_CHANGE.`
(K5). `{row}` is the 1-based data row (header excluded), the same number as `RowCheckFailure.row`;
K4 and K5 return it in their own placeholders because E1-043 passes a handler's placeholders through
unchanged (SPEC-025 L13) and injects none. K0-H and K0-R return `{table}` = `data_product`, so
MSG-P3-027 renders `The data_product load was refused: the header must hold the 8 catalog columns.
The version in force is unchanged.` (K0-H) or `The data_product load was refused: value too long for
{column}. The version in force is unchanged.` (K0-R, `{column}` replaced by the failing column;
MSG v4 line 151 for both). MSG-GEN-001 and MSG-P3-027 are already E1-042/E1-043 catalog entries. Story v7 §13 step 6 asks
for "the message table"; none exists in PS v6, and E1-042 owns the seam that a later message-table
story replaces (`GAP-E1001-14`). README decision 5 is not cited for this (finding 008). Tests assert
`messageCode`, the English text and that the Thai text is non-empty.

### SPEC-RWB-E1-001-016 Authority and inherited controls

- Load right: the endpoint's method check (Reference data C) is RWB-E1-043's. TC-E1-001-11:
  RW-DATASTEW (Reference data `RU` in the PS v6 permission seed) calling the load with
  `table = data_product` gets 403 `Problem` with MSG-P4-002 (`ApiExceptionHandler`), and
  `data_product` and `reference_version` are unchanged. RW-REFADM holds `CRUD` (PS v6) and may load.
  The table right itself is E1-043's `rwb.refload.loader.data_product` list, which this story seeds
  (SPEC-019).
- Audit (Story v7 X8 "the refusal is in the access log"): this story asserts the 403, MSG-P4-002,
  nothing written, **and one REFUSED `event=REFERENCE_LOAD_AUDIT` line** with `operation = LOAD`,
  `table = data_product`, `outcome = REFUSED`, `messageCode = MSG-P4-002`, `traceId`, and no user ID,
  row content or personal data — the interim line E1-043 writes for every load, including refusals
  (E1-043 revision 10 SPEC-027 *Refusal* and SPEC-028). The persistent access log is RWB-E1-039's
  (BS v6 order 28, after this story; its X6 writes an `AC-DENY` entry for a refusal). Under D-RUN-08
  this story names the seam; the access-log assertion for `table = data_product` is added to
  RWB-E1-039's tests (`GAP-E1001-22`, OPEN-NEW-10). No log line in this story carries personal data.
- Approval: Story v7 §10 has RW-DATASTEW confirm (U); API v4 (line 3214) and E1-043 require Reference
  data A, held by no role in PS v6 (`GAP-E1001-08`, OPEN-NEW-2). Inherited controls on approval, not
  rebuilt here: maker-checker, the approver is not the loader (409 MSG-P7-002, API v4 approve
  description; E1-043); the approval decision-log entry with decision code `AC-VERS` (API v4 approve
  description; deferred by E1-043 to RWB-E1-027, E1-043 GAP-07). The end-to-end approval in TC-E1-001-03
  uses the approver E1-043 implements (E1-043 uses a synthetic approver fixture, its A-08).
- The migration runs as `rwb_migrator` (ADR-010); `recovery_svc` has DML only.

### SPEC-RWB-E1-001-017 Feature flag, registration and guardrails

- `rwb.p1.data-catalog` (default `false`; `true` in the local profile). On: the
  `DataProductCatalogHandler` bean exists and E1-043's `ReferenceTableHandlers` collects it by the P4
  type `access.api.ReferenceTableHandler` at start-up, so `data_product` is a handler code. Off: no bean,
  so E1-043 sees an unknown code and refuses the load with 422 MSG-P3-027 "table code is not a reference
  table" (E1-043 revision 10 SPEC-025 item 1, SPEC-002) — the previous code path, since E1-043 has no
  built-in `data_product`. The migration and the view are not behind the flag (Story v7 §13). Flag
  removal follows RWB-E1-047 (BS v6 order 16).
- The 404 MSG-P4-003 paths are E1-043's and this story neither implements nor tests them: E1-043's own
  branch flag (`rwb.p3.refdata-versions`, its SPEC-018 and SPEC-025 L5) and the `PARAMETER` branch's
  `ObjectProvider<ParameterLoadHandler>` (its SPEC-026). This story's flag has one effect only: whether
  its bean exists (422 above, not 404).
- No product value, owner, role or refresh cycle as a code literal except the 14 codes DP01–DP14 that
  BR2 fixes and the F1–F3 patterns. Message texts live in the resolver catalog.
- No class names an ACE `public` table. No personal data in tests, fixtures or logs; owner user IDs in
  tests are random UUIDs.

### SPEC-RWB-E1-001-018 Seed integrity checks

`SeedIntegrityIT` (tag `recovery-it`, SPEC-010 container) asserts after the migration:

1. Seed fits column (finding 001): for every `data_product` row, `length(col) <=` the declared width of
   each `varchar` column, read from `information_schema.columns`, and the DP07 `system_of_record`
   equals the Story v7 §13 text exactly (139 characters). The same check runs as a unit test over the
   seed SQL before any container, so a too-long literal fails `./scripts/dev.ps1 test`.
2. BR7 (finding 002): `sys_fields.is_personal = true` for exactly the 526 IDs of
   `evidence/is_personal_union_v4.tsv` (copied into the test resources as a fixture of field IDs only),
   which includes every PDPA v4 "Direct identifier" (12) and "Sensitive" (5) field, among them
   DF-ACE-003, -041, -053, -060, -061, -116 and DF-EXT-002, -003, -004; and `false` for all others.
3. The three provisional rows of `ASM-E1001-17` exist with the stated types.
4. Static seed check (unit test over the migration file, no database): every `sys_fields` row is a
   plain single- or multi-row `INSERT ... (<column list>) VALUES (...)` with `is_personal` given as the
   literal `true` or `false`; the file contains no `UPDATE` of `sys_fields`; the set of field IDs with
   the literal `true` equals the 526 of the fixture list.

**Acceptance condition (RWB-TE-011 PDPA lint).** The migration file passes the RWB-TE-011 PDPA lint
with **zero findings**, both as a dictionary source (all 526 marks read, including the 17 PDPA v4
Restricted fields) and as a scanned file. This relies on the TE-011 change, announced by the
orchestrator from TE-011 spec gate round 4, that matches fixture fields by (object, field) rather than
by field name alone, so the dictionary seed's own columns (`field_name`, `description` and the other
`sys_fields` / `sys_objects` columns, which hold metadata and no personal values) raise no false
finding. If the TE-011 lint is not yet merged when this story is built, the check runs when it is
(merge-order dependency `GAP-E1001-21`, OPEN-NEW-11); the condition is not waived and no lint rule is
weakened to pass it.

### SPEC-RWB-E1-001-019 Contract with RWB-E1-043 revision 10

RWB-E1-043 (BS v6 order 8, earlier; D-RUN-08) owns the endpoint, the registry, the dispatch and the
checks that run before a handler. The registry that collects and calls the handlers stays in P3
`casewf.refdata.internal` (E1-043 SPEC-019, SPEC-025). This story conforms to revision 10 and **asks it
for nothing**:

| # | What E1-043 revision 10 provides | What this story provides |
|---|---|---|
| 1 | The SPI `access.api.ReferenceTableHandler` (P4, D-RUN-18) with `tableCode`, `validate`, `apply` and the defaults `keyColumns`, `repeatMessage`, `supportsRollback`, `onRolledBack`, `changeSummary`, `dating` (SPEC-025) | One Spring bean of that type, `DataProductCatalogHandler`, behind `rwb.p1.data-catalog` (SPEC-013, -014, -017) |
| 2 | Checks L1–L12 before `validate` (L13) and `apply` in the approve transaction (SPEC-008, SPEC-025) | `validate` (K0–K5, writes nothing) and `apply` (14 rows, one transaction) |
| 3 | A handler code needs no `LOV-REF-TABLE` row (D-RUN-11; SPEC-025) | No LOV change: the PS v6 `lov_value` seed stays as it is (finding 017) |
| 4 | `refdata.columns.<code>` is optional; absent → L12 is skipped (SPEC-025 item 4) | No `refdata.columns.data_product` row, so no generic `:R` check can preempt K2/K3 (finding 014) |
| 5 | Two `parameter_catalog` rows per handler code, in `config/parameter-catalog.csv` and the owning story's migration (SPEC-025 item 2; SPEC-029) | Both rows, `INSERT ... ON CONFLICT (param_key) DO NOTHING` in this migration: `rwb.refload.loader.data_product` = `RW-REFADM` (S7-001 X8) and `rwb.refload.approver.data_product` = `RW-DATASTEW` (S7-001 flow step 9), both CODE_LIST, BUSINESS, GLOBAL, `required=false`, DEV,SIT,UAT,PROD, owner RW-RISK, `used_by` = `recovery.casewf.refdata (RWB-E1-043)`, `secret=false`, `value_source=TABLE`, `env_property` empty (the one row shape below; E1-043 SPEC-025 item 2; its A-40 for the two default lists) |
| 6 | Flag off: a code with no handler bean is unknown → 422 MSG-P3-027 (SPEC-025 item 1, SPEC-002). The 404 MSG-P4-003 paths are its own branch flag (SPEC-025 L5, SPEC-018) and the `PARAMETER` `ObjectProvider` (SPEC-026) | Nothing beyond SPEC-017 |
| 7 | `PARAMETER` is a dispatcher branch, not an SPI handler (D-RUN-20; SPEC-025, -026, -030) | No `PARAMETER` bean; a bean for `PARAMETER` fails start-up (E1-043 SPEC-025) |
| 8 | A handler `repeatMessage` is answered at L9 with 409 and its message, nothing written, any business date (SPEC-006 rule 1, SPEC-025 L9) | `repeatMessage` = MSG-P1-011 (SPEC-014) |
| 9 | `CURRENT_STATE`: approval refused 409 MSG-P3-027 while `validFrom` is after the business date; `apply` runs on the date (SPEC-032 rule 6) | `dating()` = `CURRENT_STATE`; `apply` writes `data_product.valid_from` |
| 10 | The `sys_fields` handler and the `is_personal` protection are RWB-E1-064's (SPEC-031; `shared-updates.md` §3.2) | Nothing; SPEC-006 states no load can change a mark |

**One `parameter_catalog` row shape (finding 025).** Both rows share one shape; every field except
`param_key`, `default_value` and `description` carries the same value:
`kind=BUSINESS`, `value_type=CODE_LIST`, `scope=GLOBAL`, `required=false`, `owner_role=RW-RISK`,
`environments=DEV,SIT,UAT,PROD`, `used_by=recovery.casewf.refdata (RWB-E1-043)`, `secret=false`,
`value_source=TABLE`, `unit`, `min_value`, `max_value` and `env_property` empty, and their own
`default_value` (`RW-REFADM` loader,
`RW-DATASTEW` approver) and `description` (row-specific, required, at most 400 characters). The reader
is E1-043's P3 `ReferenceLoadAuthority`, which reads
`rwb.refload.loader.<code>` / `rwb.refload.approver.<code>` through `ParameterService` (E1-043
SPEC-027). P1 `dataengine` reads neither key at runtime, so `used_by` names P3 only: there is no P1
reader and no seam to record (D-RUN-08). The `used_by` entries follow E1-042 §7.1 (`;`-separated,
each at most 100 characters), and `secret` is the PS v6 `parameter_catalog` column.

Because E1-043 revision 10 and this spec agree on the route, AC3 and AC7–AC11 are **not** marked
PARTIAL (finding 014 step 5): their unit tests run with this story, and their end-to-end tests run
against E1-043 once it merges, through the endpoint in the table above.

**The other two run decisions ask nothing of this story.** D-RUN-19 governs parameter reads by modules
outside P3 through a P4 `access.api` read interface implemented in P3 `casewf.config`; this handler
reads no `parameter_catalog` key at runtime (the two rows are seed data consumed by E1-043's registry
and authority), so D-RUN-19 adds no edge here. D-RUN-21 reads "touches one module" in AGENTS §7 and §9
as the ACE module (recovery): this story's code sits in P1 `dataengine` and imports P4 `access.api`
(types only), which is one recovery module, so the plan-gate rule passes; the reading is the
orchestrator's, and ratification by the tech lead is OPEN-050 and is not claimed here.

Two earlier asks from RWB-E1-043 to this story are **withdrawn by its revision 10** (its
`shared-updates.md` §3, "Withdrawn from revision 2"): the data-dictionary handler for `sys_objects` /
`sys_fields` (owner RWB-E1-064) and the LOV-REF-TABLE seed correction (not needed). Neither is
outstanding; the residual dictionary-owner direction (E1-064 v7 §12 says its loader is *called by* the
reference data service, while E1-043 SPEC-031 and this SPEC have the handler call its own loader) is
recorded as `GAP-E1001-23` (Blocker No) against RWB-E1-064, which E1-043 also records as its GAP-40.
The `parameter_catalog` rows are the same ones E1-043's SPEC-025 item 2 asks for; they must be merged
with E1-042's generator (BS v6 order 3) and before the first `data_product` load.

## Field-level behaviour matrix

| Object | Field | Source | Create / update | Rule |
|---|---|---|---|---|
| `data_product` | `product_code` | Seed, load file | Seed insert; never changed by load | DP01–DP14 (K1); unique |
| `data_product` | `product_name`, `definition` | Seed, load file | Seed; updated by `apply` | Required; ≤ 80 / 400 (K0-R) |
| `data_product` | `system_of_record` | Seed, load file | Seed; updated by `apply` | F1–F3 (K2); absence → MSG-P1-003 (not K0); ≤ 200 (K0-R, `ASM-E1001-13`) |
| `data_product` | `owner_role` | Seed, load file | Seed `RW-DATASTEW`; updated by `apply` | Active role code (K4); AC9 text |
| `data_product` | `owner_user_id` | Load file | NULL in seed; set by `apply` | Required by K3; absence → MSG-P1-003 (not K0); synthetic in DEV/SIT |
| `data_product` | `refresh_cycle` | Seed, load file | Seed; updated by `apply` | LOV-REFRESH (K5) |
| `data_product` | `expected_by` | Seed, load file | Seed; updated by `apply` | Optional; ≤ 20 (K0-R width only) |
| `data_product` | `valid_from` | Load request | Seed 2026-11-30; set by `apply` | From the load's valid from |
| `data_product` | standard columns | System | `version` +1, `updated_at`, `updated_by` on `apply` | — |
| `sys_objects`, `sys_fields` | all | Migration | Seed only | Later changes are reference loads (D-RCV-29) through E1-043; the `sys_fields` handler is RWB-E1-064's and never changes `is_personal` (E1-043 SPEC-031) |
| `sys_fields` | `is_personal` | Migration | Seed per union | `ASM-E1001-14`; no load path changes it (SPEC-006) |
| `v_data_dictionary` | all | View | Read only | SPEC-005 |

## Status-transition matrix

| Object | From | Event | To | Source |
|---|---|---|---|---|
| Recovery schema (Flyway) | E1-042 and E1-043 migrations applied (and baseline `0` where the S2 stand-in exists) | This migration applied | its history row `success = true` | Story v7 §9 |
| Recovery schema (Flyway) | as above | Migration fails | unchanged; no success row | AC4 |
| Data product catalog | seed (version 1) | Load approved and applied | `version` +1, 14 rows updated | Story v7 §9; E1-043 |
| Data product catalog | version in force | Same file loaded (same `validFrom`, same hash) | unchanged; 409 MSG-P1-011, nothing written | AC10 (`repeatMessage`; E1-043 SPEC-025 L9) |
| Data product catalog | version in force | Load refused | unchanged | AC7–AC9, AC11 |

No case status changes (Story v7 §9).

## Exceptional-case behaviour

| ID | Case | Behaviour | Evidence |
|---|---|---|---|
| X1 | Statement fails in the migration | Rollback; failing statement in the log; no success row | SPEC-007 |
| X2 | Column without dictionary row, field without column, or type mismatch | Conformance test fails with the C1–C3 texts | SPEC-009 |
| X3 | Migration already applied | Nothing applied | SPEC-008 |
| X4 | No / two / bare system of record, or no owner | 422, MSG-P1-003 per product, nothing written; the message is the `messageCode` even when it is the file's only defect | SPEC-013, -015 |
| X5 | Not exactly DP01–DP14 | 422, MSG-P1-004 naming the missing codes | SPEC-013, -015 |
| X6 | Owner role or refresh cycle outside its list | 422, MSG-P1-007 per row and field, AC9 texts | SPEC-013, -015 |
| X7 | Same file again (same `validFrom`, same hash) | Nothing written; 409 `Problem` with MSG-P1-011 | SPEC-014; E1-043 SPEC-025 L9 |
| X8 | Caller without Reference data C | 403, MSG-P4-002; one REFUSED `REFERENCE_LOAD_AUDIT` line; persistent access log is the RWB-E1-039 seam | SPEC-016 |
| X9 | S1=`true` with recovery Flyway on | Refused by configuration; documented invalid combination | SPEC-010 |
| X10 | Flag `rwb.p1.data-catalog` off | No handler bean; `data_product` is an unknown code → 422 MSG-P3-027, nothing written (the 404 MSG-P4-003 paths are E1-043's own) | SPEC-017, -019 |
| X11 | Catalog file with a wrong header, a missing value or a value longer than its column | 422, MSG-GEN-001 (empty value) or MSG-P3-027 with `{table}` = `data_product` (header or width), nothing written | SPEC-013 K0-H/K0-R; SPEC-015 |

## API change assessment

No endpoint, schema or response is added or changed. The story uses `POST /admin/reference-loads`
(`postAdminReferenceLoads`, x-module P4, Reference data C) and `/{loadId}/approve` (Reference data A),
both owned and built by RWB-E1-043 (D-RUN-10, D-RUN-11). `table` is a free string, so `data_product`
needs no API change. The repeat is a 409 `Problem` (API v4 `E409`) carrying MSG-P1-011, so
`ReferenceLoad` (line 8832: `id`, `table`, `validFrom`, `status`, `rows`) needs no message field and
`GAP-E1001-13` is settled without an API change. API v4 names "ReferenceTableLoader" for P5 tables and
Story v7 §12 names `ReferenceTableHandler`; E1-043 revision 10 publishes
`access.api.ReferenceTableHandler` (D-RUN-18), which this story implements (`GAP-E1001-07`).
Contracts: `contracts/backend-apis.json`.

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | Story v7 §15 | No screen, route, component or i18n key. | None. |
| Backend | YES — migration, `dataengine` catalog classes, handler bean on the P4 SPI, two catalog rows, seed checks | REQUIRED | 80% lines, branches, statements and functions on `th.co.scb.ace.demo.recovery.dataengine` | SPEC-001 to -010, -012 to -019; AC1–AC11; BR1–BR9 | K0–K5, F1–F3, the apply transaction, flag-gated registration and the seed-width check are hand-written logic. JUnit 5 with AssertJ; JaCoCo. | Each of K0-H, K0-R, K1–K5 and F1–F3 has a pass and a fail case (AC7, AC8, AC9, AC11 data from Story v7 §16, plus the SPEC-013 negative list and the two single-defect cases TC-18/19); K0-H and K0-R assert the exact MSG-P3-027 texts with `{table}` = `data_product` ("The data_product load was refused: the header must hold the 8 catalog columns. The version in force is unchanged." and "The data_product load was refused: value too long for definition. The version in force is unchanged."); K4 and K5 assert the AC9 fixture texts with `{row}` = 4 and 5; every Story v7 §13 seed value matches exactly one form; all findings in order; `validate` writes nothing; `apply` rolls back all rows on failure; the bean is absent when the flag is off and is collected by E1-043 when on; seed values fit their columns; `repeatMessage` returns MSG-P1-011 with both placeholders. |

Separately required integration tests (tag `recovery-it`): `RecoverySchemaMigrationIT`,
`DataDictionaryConformanceTest`, `SeedIntegrityIT`, the moved `RecoveryDatabaseIT`, and the end-to-end
load tests through the E1-043 endpoint. They are not replaced by unit tests.

## Test scenarios

| Test case | AC / BR | Level | Expected (this spec) | Runs when |
|---|---|---|---|---|
| TC-E1-001-01 | AC1, BR1, BR6, BR8 | IT | 93 tables after all migrations, this migration created 89 and none of the T8 four; none of the 20 removed tables; no `payment_match_rule`; 0 constraints into `public`; the 18 link columns `varchar(255)` in no FK; conformance 1,050/1,050 and 1,078/1,078; no `v_ace_*` view from this migration | This story |
| TC-E1-001-02 | AC2, BR1 | IT | DF-ACE-018 row as AC2 with `product_system_of_record` "ACE (ingested from ALS)", DAILY, RW-DATASTEW, synthetic owner UUID; DF-EXT-028 row as AC2 | This story |
| TC-E1-001-03 | AC3, BR2, BR3, BR5 | Unit + E2E | 14 rows; DP01, DP03, DP06 values as AC3 | Unit now; E2E through E1-043 (earlier story) |
| TC-E1-001-04 | AC4 | IT | Copy of the migration with a failing `valuation_ext` statement on a throwaway schema: none of its objects, no success row, E1-042/E1-043 objects intact | This story |
| TC-E1-001-05 | AC5, BR1 | IT | Both AC5 texts; `char(64)` pass case (DF-REF-301 and the 9 PS v6 `char(n)` rows) | This story |
| TC-E1-001-06 | AC6 | IT | Second migrate applies 0; 123 / 1,382 unchanged | This story |
| TC-E1-001-07 | AC7 | Unit + E2E | 422, MSG-P1-003 for DP06 and DP11; `messageCode` = MSG-P1-003 | as TC-03 |
| TC-E1-001-08 | AC8 | Unit + E2E | 422, MSG-P1-004 "Missing: DP09." | as TC-03 |
| TC-E1-001-09 | AC9 | Unit + E2E | 422, two MSG-P1-007 texts **verbatim**: "Row 4: owner_role must be one of the role codes in LOV-ROLE." and "Row 5: refresh_cycle must be one of DAILY, WEEKLY, MONTHLY, ON_CHANGE.", with `{row}` = 4 and 5 (1-based data row, header excluded) in the handler's placeholders; no role code listed to the caller | as TC-03 |
| TC-E1-001-10 | AC10 | E2E | Second load: same `validFrom` and hash → 409 `Problem`, `messageCode` MSG-P1-011 with `{source}` = "data product catalog" and `{date}` = the valid from; no new `reference_version`; `data_product` rows and `version` unchanged | after E1-043 |
| TC-E1-001-11 | X8 | E2E (access) | RW-DATASTEW: 403, MSG-P4-002, nothing written; one REFUSED `event=REFERENCE_LOAD_AUDIT` line with `operation=LOAD`, `table=data_product`, `outcome=REFUSED`, `messageCode=MSG-P4-002`, no user ID and no personal data; the access-log entry is asserted in RWB-E1-039 | after E1-043 |
| TC-E1-001-12 | AC11 | Unit + E2E | 422, MSG-P1-003 for DP06 "CCMS" | as TC-03 |
| TC-E1-001-13 | BR3, SPEC-018(1) | Unit + IT | Every seed value fits its column; DP07 verbatim (139) | This story |
| TC-E1-001-14 | BR7, SPEC-018(2) | IT | 526 `is_personal = true` exactly as the fixture list | This story |
| TC-E1-001-15 | SPEC-010 | IT | `RecoveryDatabaseIT` passes in S1=`false`, S2=`true` with every existing assertion | This story |
| TC-E1-001-16 | SPEC-017, -019 | Unit | Flag off: no handler bean, so E1-043's registry has no `data_product` entry (422 path); flag on: the bean exists and is collected by the P4 type; no `PARAMETER` bean; a second bean for `data_product` fails start-up | This story |
| TC-E1-001-17 | BR7, SPEC-018(4), T10 | Unit + CI lint | `is_personal` only as INSERT literals (no `UPDATE sys_fields`), 526 `true`; RWB-TE-011 PDPA lint over the migration: zero findings | This story (lint part once RWB-TE-011 is merged) |
| TC-E1-001-18 | AC7, X4, SPEC-013 K3 | Unit | A file whose only defect is DP11 with no `owner_user_id`: exactly one finding, MSG-P1-003; `messageCode` = MSG-P1-003; 422; nothing written | This story |
| TC-E1-001-19 | AC7, X4, SPEC-013 K2 | Unit | A file whose only defect is DP06 with an empty `system_of_record`: exactly one finding, MSG-P1-003; `messageCode` = MSG-P1-003; 422; nothing written | This story |
| TC-E1-001-20 | SPEC-019 item 5 | Unit + IT | The two `parameter_catalog` rows exist in `config/parameter-catalog.csv` and after the migration with the one row shape of SPEC-019 item 5, including `used_by` = `recovery.casewf.refdata (RWB-E1-043)`, `secret=false`, `value_source=TABLE`; no `refdata.columns.data_product` row and no `LOV-REF-TABLE` row for `data_product` | This story |

All test data is synthetic (random UUIDs, no names or account numbers).

## Guardrails and out of scope

- Out of scope (Story v7 §19): the 30 `v_ace_*` views, helper functions, grants and the view
  conformance test (RWB-E1-069); freshness (RWB-E1-015); access per data product, PDPA masking and the
  catalog entry screen (RWB-E1-016); retention (RWB-E1-017); Stage 2 products; the dictionary endpoint
  and field versions (RWB-E1-064). Also not here: rule package content (E1-072 v7 §13), `delegation_limit`
  content (RWB-E1-038), the persistent access log (RWB-E1-039), the message table (no owner yet), and
  the `sys_fields` dictionary handler (RWB-E1-064, `GAP-E1001-23`).
- Not rebuilt (phase0 audit A-04): `casewf.migration.RecoveryFlywayConfig`, the lint,
  `20-grants.sql.inc`, `access.api.ApiError` / `access.internal.ProblemFactory` and
  `access.api.ApiProblemException`, `access.api.MessageResolver` (TE-001 v4 SPEC-022).
- Never: a literal schema name, `SET search_path`, `GRANT`, a constraint into `public`, a read of an
  ACE table, a `DROP` in the migration, editing the migration after merge, editing the PS v6 file.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Story v7 AC1, AC6, §11; PS v6; D-RCV-36 CR A.7 | v5 counts vs PS v6. | Test expectations. | D-RCV-36 (tier 1): PS v6 (`ASM-E1001-01`). | RESOLVED | 003, 006, 008, 009 |
| CLAR-002 | DL v10 D-RCV-28; D-RCV-34; D-RUN-07 | Migration number. | File name. | Assigned at merge (D-RUN-07). | RESOLVED | 001 |
| CLAR-003 | README; `RecoveryFlywayConfig`; `RecoveryDatabaseIT`; E1-069 review 107 | Local switch to Flyway. | Local start, ITs. | Switches S1–S3 and the E1-069 hand-off (`ASM-E1001-07`). | RESOLVED | 010 |
| CLAR-004 | DL v10 D-RCV-29; Story v7 §12–§13; E1-072 v7 | Which seeds belong here? | Seed sections. | Dictionary, `data_product`, LOV, role, permission; no rule packages (`ASM-E1001-03`). | RESOLVED | 006 |
| CLAR-005 | Story v7 §13; PS v6 seed; Rulings v2 R4 | Three `data_product` seed versions. | Seed values. | Story v7 §13 (`ASM-E1001-04`). | RESOLVED | 006 |
| CLAR-006 | Story v7 §12; Rulings v2 R2; PS v6 line 2156 | View columns. | AC2. | Story v7 §12 and R2. | RESOLVED | 005 |
| CLAR-007 | Story v7 §3, §12; D-RUN-11, -18, -20; E1-043 rev 10 SPEC-025 | Handler seam owner and contract. | Registration, SPI type. | E1-043 publishes the P4 `access.api.ReferenceTableHandler` SPI (D-RUN-18); this story implements it as a bean; `PARAMETER` is a dispatcher branch (D-RUN-20); E1-043 asks nothing of this story (SPEC-019). | RESOLVED | 013, 014, 017, 019 |
| CLAR-008 | Lint; PS v6 literals; D-RUN-13 | 297 `'public.…'` literals. | Merge. | Lint ignores literals (E1-044 SPEC-007). | RESOLVED | 011 (retired) |
| CLAR-009 | Story v7 §10; E1-043; API v4 line 3214 | Who approves a `data_product` load? | E2E approval. | Open item OPEN-NEW-2. | OPEN (non-blocking) | 016 |
| CLAR-010 | Story v7 §14; MSG v4 line 77 | MSG-P1-003 wording and Thai. | Message text. | Story v7 English; MSG v4 Thai as Proposed (OPEN-005). | RESOLVED | 015 |
| CLAR-011 | Story v7 §13 DDL vs seed; PS v6 line 820; LDM v8 line 561 | DP07 is 139 characters for `varchar(120)`: widen or shorten? | Seed, DDL, DF-REF-074. | No precedence rule (same document). Proceeding on `ASM-E1001-13` (widen to 200). Ruling needed from the data architect (OPEN-NEW-6) **before build (the merge of this story's migration)**. | OPEN (Blocker = Yes gap 17) | 004, 006, 018 |
| CLAR-012 | Story v7 BR7; PS v6 `is_personal`; PDPA v4; PDPA Design v2 line 31 | Which source decides `is_personal`? | 508 seed flags. | No precedence rule; the inventory pointer is a strong but incomplete default (26 PS-v6-only fields have no inventory row). Proceeding on `ASM-E1001-14` (protective union, 526). Ruling needed from the data architect with the DPO (OPEN-NEW-7) **before build (the merge of this story's migration)**. | OPEN (Blocker = Yes gap 18) | 006, 018 |
| CLAR-013 | Story v7 AC10; API v4 `ReferenceLoad`; MSG v4 line 85; E1-043 rev 10 SPEC-025 L9, SPEC-006 | How does a repeat response carry MSG-P1-011? | AC10 message clause. | Answered by E1-043 rev 10: `repeatMessage` → 409 `Problem` with MSG-P1-011, nothing written. No API change (`GAP-E1001-13`, Blocker No). | RESOLVED | 014, 015 |

`CLARIFICATION_STATUS: RESOLVED_WITH_OPEN_ITEMS` — CLAR-011 and CLAR-012 are Blocker = Yes document
gaps carried on labelled assumptions; a human ruling is required before build (the merge of this
story's migration). No question was asked (L-RCV-03).

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); sources read from the document set.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: One recovery migration from Physical Schema v6 (89 tables, dictionary, seeds, v_data_dictionary), the data product catalog handler implementing the P4 handler SPI of RWB-E1-043 revision 10, seed and conformance tests, and the local switch to a Flyway-built schema; no screen; no API change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NO_API_CHANGE] [REASON: uses the existing reference-load endpoint owned by RWB-E1-043 with table data_product]
REQUIREMENT_COVERAGE_SUMMARY: 9 business rules, 11 ACs, exception groups, authority, contract, plan, guardrails, out of scope and NFRs mapped in 33 rows.
REQUIREMENT_COVERAGE_RESULT: FAILURE [TOTAL_RULES: 33] [COVERED_RULES: 32] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 2] — 29 rows covered unconditionally and 3 on the Blocker = Yes assumptions (BR3, BR7, NFR-RWB-006); 1 row NOT_APPLICABLE with reasons; the 2 contradictions are GAP-E1001-17 and -18, unresolved by precedence.
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED_WITH_OPEN_ITEMS [OPEN_ITEMS: 3 (CLAR-011, CLAR-012 Blocker = Yes; CLAR-009 non-blocking)]
NEXT_STEP: Spec gate round 4 (review/spec-gate-review-4.md). No human resolution is claimed for GAP-E1001-17 or GAP-E1001-18; both stay Blocker = Yes until a human ruling is recorded before build (OPEN-NEW-6, OPEN-NEW-7).
```
