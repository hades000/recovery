# Technical Specification — RWB-E1-001 Recovery tables for the 14 data products

| Field | Value |
|---|---|
| Story | RWB-E1-001 — Recovery tables for the 14 data products |
| Epic / module | E1 (release 30 November 2026) / P1 Recovery data engine |
| RUN_ID | `INC-009-epic-1-RWB-E1-001` |
| Revision | 2 — remediation run 1 of spec gate round 1 (`../review/spec-gate-review.md`, findings 001–013). Run-1 text kept in `spec.run1.md`; finding-by-finding answers in `gate-response.md` |
| Source requirement | Story file v7 (15 Nov 2026), `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md`; increment card `docs/increments/INC-009-epic-1-RWB-E1-001.md` |
| Upstream IDs | REQ-RDF-001; FEAT-RDF-01, FEAT-RDF-02; `BR-RWB-013` / `FR-RWB-013` (Traceability Matrix §3, row 009); NFR-RWB-005, -006, -008, -009 (Canonical Requirements v2.0 §NFR); TC-E1-001-01 to TC-E1-001-12 |
| Governing decisions | D-RCV-35 (U1–U5) and D-RCV-36 (change register A.5, A.7, row 18, T5); ADR-010; D-RCV-28 and D-RCV-29 (Decision Log v10); run decisions D-RUN-07, -08, -11, -12, -13 (`AI-SDLC-BUILD-LOG.md` decisions table); RWB-E1-001 Specification Rulings v2 and Pre-build Rulings v2 (both status Proposed) |
| Status | Revised for spec gate round 2. **Two Blocker = Yes document gaps** (`GAP-E1001-17` DP07 width, `GAP-E1001-18` `is_personal`) are carried on labelled assumptions `ASM-E1001-13` and `ASM-E1001-14`; both need a human ruling before build |
| Prepared | 2026-11-18 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer spec gate round 2 (`../review/spec-gate-review-2.md`) |

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
| D-RUN | Run decisions D-RUN-07 to D-RUN-13 | `AI-SDLC-BUILD-LOG.md` decisions table (lines 30–36) |
| Rulings v2 / PBR v2 | RWB-E1-001 Specification Rulings v2; RWB-E1-001 Pre-build Rulings v2 (both Proposed) | `01-decisions-and-governance/recovery-workbench-rwb-e1-001-specification-rulings-v2.md`, `…-pre-build-rulings-v2.md` |
| MSG v4 | Error and Message Standard v4 | `07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| API v4 | API Specification v4 | `api/recovery-api-v4.yaml` (repo copy): `/admin/reference-loads` line 3167, approve line 3214, `ReferenceLoad` line 8832 |
| BS v6 | Build Sequence Epic 1 and Epic 2 v6 | `11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` (orders 1, 3, 8, 9, 10, 28, 36) |
| REQ v2.0 | Recovery Workbench canonical requirements v2.0 (16 Nov 2026), NFR table | `17 AI-First SDLC Repository v2/requirement/RecoveryWorkbench_Requirements.md` lines 229–238 |
| E1-0nn v7 | Other story files in Epic 1 Story Files v7 (E1-039, E1-042, E1-043, E1-072) | same folder as Story v7 |
| Sibling specs | E1-044 (INC-001, revised, SPEC-007/-011/-015, T-044-21); E1-042 (INC-003, revision 3, SPEC-001/-002/-022, §12.3); E1-043 (INC-008, run 1 under remediation, SPEC-001/-002/-003/-006); E1-069 (INC-010, run 1, SPEC-015; review 107, 109); TE-011 (INC-006, SPEC-TE011-001 dictionary reader; orchestrator cross-story input from its spec gate round 4, `review/spec-gate-review-4.md`) | `aisdlc/output/INC-0nn-*/specify/spec.md` |
| Baseline code | Repository as of 17 Nov 2026 | `RecoveryFlywayConfig`, `RecoveryMigrationLintTest`, `RecoveryDatabaseIT`, `ApiExceptionHandler`, `infra/postgres/init/10-load-ace-database.sh`, `20-grants.sql.inc`, `docker-compose.yml`, `.env.example`, `application.yaml`, `README.md` |

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
| `is_personal = true` | 18 | — | 526 (`ASM-E1001-14`) | 526 |

The 28-row difference between 1,075 and 1,047 is the seven standard columns of each extension table,
which PS v6 records in `sys_fields`. PS v6 minus v5 = {`rule_package`, `rule_package_version`}; v5
minus v6 = {`payment_match_rule`} (D-RCV-36 CR A.7, row 18).

## v2 baseline delta

No `_v2-baseline` folder exists for this story. Revision 2 changes against run 1 (`spec.run1.md`):

| Area | Run 1 | Revision 2 | Driver |
|---|---|---|---|
| Migration number | "`0001` if first", rule (b) | Number assigned at merge only; one fixed object set | D-RUN-07; finding 004 |
| Tables created | All 93 | 89; the 4 tables of E1-042 and E1-043 are not created, their dictionary rows stay | D-RUN-12; GAP-16; finding 004 |
| `data_product.system_of_record` | `varchar(120)` | `varchar(200)`, DF-REF-074 `physical_type` aligned | Finding 001; Blocker gap 17 |
| `is_personal` | PS v6 as written (18) | Protective union with PDPA v4 (526) | Finding 002; Blocker gap 18 |
| Handler seam | Assumed published by E1-043 | E1-043 table-code handler registry; this story registers `data_product` | D-RUN-11; finding 003 |
| Repeat load (AC10) | MSG-P1-011 "not an error" | Writes nothing (verified); the message on the response is a gap with E1-043 | Finding 005 |
| X8 / audit | Access test only | 403 test + access-log seam (RWB-E1-039) + inherited approval controls | Finding 006 |
| Local start | Flyway off on the reference path (no mechanism) | Named switches, defaults and test stages; views-only stand-in; E1-069 hand-off | Finding 007 |
| Messages | Fixed text in code citing README decision 5 | E1-042 `MessageResolver` seam | Finding 008 |
| `rule_package` seed | Excluded on D-RCV-29 | Excluded on Story v7 §12/§13 seed list + E1-072 v7; conflict recorded | Finding 009; GAP-19 |
| SOR rules | SOR-1..4, unlabelled | Closed forms F1–F3, labelled `ASM-E1001-09` | Finding 010 |
| C3 types | no `char(n)` | `character(n)` added | Finding 011 |
| Link keys | 16 | 18 (adds `valuation_ext.valuation_key`, `recovery_case.primary_person_key`) | Finding 012 |
| NFR / PBR v2 | not mapped / not cited | Mapped; cited | Finding 013 |
| SPEC-011 lint | This story changes the lint | Retired: lint is E1-044's (SPEC-007, T-044-21) | D-RUN-13 |
| New | — | E1-042 added columns get provisional field IDs; Flyway history table excluded from conformance; catalog file structure check K0 | GAP-20; `ASM-E1001-17`, `-19` |

## Assumptions

Full list with evidence in `assumptions.md`. Those that shape the design:

| ID | Assumption (short) | Gap | Blocker |
|---|---|---|---|
| `ASM-E1001-13` | **DP07 business text is kept verbatim; `data_product.system_of_record` is widened to `varchar(200)` and DF-REF-074 `physical_type` to `varchar(200)`.** | `GAP-E1001-17` | **Yes** |
| `ASM-E1001-14` | **`is_personal` is seeded as the protective union: `true` where PS v6 says true or PDPA v4 says "Personal data = Yes" (526 rows); never weakened.** | `GAP-E1001-18` | **Yes** |
| `ASM-E1001-01` | Dictionary and table set are PS v6 (D-RCV-36 row 18), with the D-RUN-12 creation split. | `GAP-E1001-01` | No |
| `ASM-E1001-02` | `<seq>` is assigned by the orchestrator at merge (D-RUN-07). | `GAP-E1001-02` | No |
| `ASM-E1001-05` | The handler contract is the Story v7 §12 method set; the registry and its type names are E1-043's (D-RUN-11). | `GAP-E1001-07` | No |
| `ASM-E1001-07` | Local switch design of SPEC-010. | `GAP-E1001-11` | No |
| `ASM-E1001-15` | AC10: "writes nothing" verified; the response follows E1-043; MSG-P1-011 on the response waits on E1-043/API. | `GAP-E1001-13` | No |
| `ASM-E1001-17` | Three provisional field IDs DF-REF-300..302 for the columns E1-042 adds to `parameter_value`. | `GAP-E1001-20` | No |

`L-RCV-03`: no question was asked. Gaps are in `document-gaps.md`; proposed shared rows in `shared-updates.md`.

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — Story v7 §15: "No screen in this story". |
| Logic In Scope | `YES` — catalog validation (BR2, BR3, BR5, list values), versioned apply, conformance and seed-integrity tests. |
| API In Scope | `YES` — the catalog load uses the existing `POST /admin/reference-loads` and its approve operation (API v4), owned and built by RWB-E1-043 (D-RUN-10, D-RUN-11). No endpoint, request or response schema is added or changed. |
| API Impact Type | `NO_API_CHANGE` — the MSG-P1-011 response gap (`GAP-E1001-13`) is routed to E1-043 / the API owner, not changed here. |
| Impacted Existing Nodes | `backend/src/main/resources/db/modulemigration/recovery/` (adds this story's file after the E1-042 and E1-043 files); `infra/postgres/init/10-load-ace-database.sh`, `docker-compose.yml`, `.env.example`, `application.yaml` (`rwb.flyway.enabled`), `README.md` "Local versus target", migration-folder `README.md` (SPEC-010); `RecoveryDatabaseIT` (container mode, SPEC-010); E1-043 handler registry (registration); E1-042 `FixedMessageCatalog` (four message IDs added, SPEC-015). |
| New Nodes Required | `YES` — `V<seq>__rwb_e1_001_recovery_schema.sql`; nested module `dataengine` with `api/` and `internal/catalog` (`DataProduct`, `DataProductRepository`, `DataProductCatalogHandler`); `DataDictionaryConformanceTest`; `SeedIntegrityIT`; `RecoverySchemaMigrationIT` (tag `recovery-it`); flag `rwb.p1.data-catalog`. |
| Inherited Existing Behavior | `RecoveryFlywayConfig` (history table `flyway_schema_history_recovery` in schema `recovery`, `${recoverySchema}`, `baselineOnMigrate(true)`, baseline `0`, `createSchemas(false)`, clean disabled); migration lint (E1-044, incl. D-RUN-13 literal rule); `20-grants.sql.inc` default privileges; `ApiExceptionHandler` 403 → MSG-P4-002; E1-042 `MessageResolver`; E1-043 endpoint, method checks, content hash, maker-checker. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` — migration, entity, repository, handler and its registration, flag, local-switch scripts, tests. |

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
| BR7 | Personal fields carry `is_personal = true` so masking (RWB-E1-016) and the PDPA lint (RWB-TE-011) can read them. | 002 (T10), 006, 018 | DIRECT | Not "PS v6 as written" (run 1): seeded as the protective union of PS v6 and PDPA v4, 526 rows incl. all 17 Restricted fields, as literal INSERT values with no `UPDATE` (T10); tests TC-E1-001-14 and TC-E1-001-17 (TE-011 lint, zero findings). | COVERED (ASM) |
| BR8 | No constraint into `public`; ACE links are `varchar(255)` keys with no FK. | 003 | DIRECT | 18 link columns listed; 0 FKs on them; 0 constraints into `public`. | COVERED |
| BR9 | The migration seeds the dictionary for tables and the 30 views before the views exist. | 006, 002 | DIRECT | 30 view objects, 304 view fields; no view created. | COVERED |
| AC1 | Schema deployed: table set, removed tables absent, no constraint into public, business keys, conformance. | 002, 003, 009, 010 | DIRECT | Counts per the counting table. | COVERED |
| AC2 | `v_data_dictionary` returns the stated rows for `v_ace_account.days_past_due` and `account_ext.dispute_open`. | 005, 006 | DIRECT | View per Story v7 §12 / Rulings v2 R2. | COVERED |
| AC3 | After the catalog load, 14 rows with the stated DP01, DP03 and DP06 values. | 013, 014, 017 | DIRECT | End-to-end through the E1-043 endpoint (BS v6 order 8, earlier). | COVERED |
| AC4 | A failing statement rolls the whole migration back; no successful history row. | 007 | DIRECT | One transaction. | COVERED |
| AC5 | Conformance test fails on a column with no dictionary row and on a type mismatch, with the stated texts. | 009 | DIRECT | Texts fixed; `character(n)` added. | COVERED |
| AC6 | A re-run applies nothing and leaves counts unchanged. | 008 | DIRECT | 123 / 1,382. | COVERED |
| AC7 | Two systems of record (DP06) and no owner (DP11) refuse the load with MSG-P1-003 for both. | 013, 015 | DIRECT | All findings reported. | COVERED |
| AC8 | 13 rows without DP09 refuse the load with MSG-P1-004 naming DP09. | 013, 015 | DIRECT | — | COVERED |
| AC9 | Owner role and refresh cycle outside their lists refuse the load with two MSG-P1-007 texts. | 013, 015 | DIRECT | LOV-ROLE resolved through `role` (`ASM-E1001-10`). | COVERED |
| AC10 | The same file again writes nothing and the response carries MSG-P1-011. | 014, 015 | DIRECT + DEPENDENCY | "Writes nothing" asserted end-to-end. The message on the response is not expressible in API v4 `ReferenceLoad`, and E1-043 answers a repeat with 201 and the same body (`GAP-E1001-13`, `ASM-E1001-15`). | PARTIAL |
| AC11 | A bare source name ("CCMS") refuses the load with the MSG-P1-003 text. | 013, 015 | DIRECT | Fails F1–F3. | COVERED |
| X1–X3 | Migration failure, conformance failure, re-run. | 007, 008, 009 | DIRECT | Pipeline log only. | COVERED |
| X4–X7 | Catalog refusals and repeat file. | 013, 014, 015 | DIRECT | X7 message as AC10. | COVERED |
| X8 / TC-E1-001-11 | A role without Reference data C gets 403 with MSG-P4-002; the refusal is in the access log. | 016 | INHERITED + SEAM | 403/MSG-P4-002 and nothing written asserted here; the access-log entry is RWB-E1-039's (BS v6 order 28, later; D-RUN-08), `GAP-E1001-22`. | COVERED (403); access log = seam |
| §10 Authority | RW-REFADM loads (C); RW-DATASTEW confirms; pipeline identity migrates. | 014, 016 | DIRECT + INHERITED | Approver right conflict `GAP-E1001-08`; maker-checker MSG-P7-002 and AC-VERS decision log inherited from E1-043/API v4. | COVERED |
| §12 Contract | View columns; handler interface; 422/403 responses; idempotency; migration trigger/restart. | 005, 012–015 | DIRECT | Handler registered in the E1-043 registry. | COVERED |
| §13 Solution plan | Components, database, feature flag, build steps 1–7. | 001–010, 012–018 | DIRECT | Path, package and message table per repo seams (`GAP-E1001-10`, `-14`). | COVERED |
| §17 Guardrails | No business value in code; no personal data; no ACE table read; no constraint into public; dictionary reads only recovery tables. | 003, 005, 017 | DIRECT | — | COVERED |
| §19 Out of scope | `v_ace_*` views, grants and view conformance (E1-069); freshness (E1-015); access/masking (E1-016); retention (E1-017); Stage 2; dictionary endpoint (E1-064). | 002, 010 | DIRECT | Excluded; views-only local stand-in retired by E1-069 (SPEC-010). | COVERED |
| NFR-RWB-005 Security | Method security, audit. | 016 | INHERITED | Endpoint checks are E1-043's; migration as `rwb_migrator` only (ADR-010). | COVERED |
| NFR-RWB-006 Privacy | PDPA classification; no personal data. | 006, 017, 018 | DIRECT | BR7 union; synthetic UUIDs only. | COVERED (ASM) |
| NFR-RWB-008 Observability | Logs per job. | 007 | DIRECT | Failing statement in the Flyway log (X1). | COVERED |
| NFR-RWB-009 Operability | Flag-off path; rollback by tag. | 008, 017 | DIRECT | Flag off → handler unregistered; forward-only migration. | COVERED |
| NFR-RWB-001..004, -007, -010 | Availability, performance, throughput, recovery, accessibility, retention. | — | NOT_APPLICABLE | No runtime read path with a target, no screen, no retained record class in this story (retention is RWB-E1-017). | N/A |

## User story intent interpretation

Create the recovery schema's tables and the data dictionary as one forward-only migration taken from
PS v6, publish the dictionary as a view, and let the reference data administrator load the catalog of
the 14 data products as versioned reference data that is refused in full on any error. The story
creates no screen, reads no ACE table and creates no `v_ace_*` view (Story v7 §15, §17, §19).

## Entry trigger and preconditions

| Trigger | Preconditions |
|---|---|
| Recovery Flyway runs at application start (`RecoveryFlywayConfig`, `initMethod = "migrate"`) when `rwb.flyway.enabled=true`. | Schema `recovery` exists (DBA; `createSchemas(false)`); extension `pgcrypto` exists; `rwb_migrator` holds DDL; the E1-044 lint passes; **the E1-042 and E1-043 migrations are already applied** (BS v6 orders 3 and 8 precede 9; D-RUN-12), so `parameter_catalog`, `parameter_value`, `reference_version` and `reference_row` exist. |
| `POST /admin/reference-loads` with `table = data_product`, then approve (API v4; E1-043). | E1-043 built with its table-code handler registry (D-RUN-11); flag `rwb.p1.data-catalog` on, so the `data_product` handler is registered; caller holds Reference data C (load) or the approver right E1-043 implements (`GAP-E1001-08`). |
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
| T8 | Objects of tables an earlier-merged story creates: `CREATE TABLE parameter_catalog` (line 1386), `parameter_value` (1413), `reference_version` (1437), `reference_row` (1471); `fk_reference_row_version_id` (line 2242); `ix_reference_row_version_id` (line 2347); the 4 `COMMENT ON TABLE` (lines 2426–2429) and the 53 `COMMENT ON COLUMN` statements on those four tables | Not carried. Their 4 `sys_objects` and 57 `sys_fields` rows **are** carried. The FKs from `retention_rule`, `document_type`, `document_checklist_item` and `document_hub_parameter` to `reference_version` (lines 2228, 2244, 2245, 2248) **are** carried: they belong to this story's tables and the target exists | D-RUN-12; E1-042 spec rev 3 §12.3; E1-043 spec SPEC-001 |
| T9 | Line 820 `system_of_record varchar(120) NOT NULL`; the `sys_fields` row DF-REF-074 (`physical_type` `varchar(120)`) | `varchar(200)` in both | `ASM-E1001-13` (Blocker gap 17) |
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
| `sys_fields` | 1,379 as PS v6 (DF-EXT-001..049, DF-REF-274..299, the 304 `DF-ACE-*` view fields), with T9 and T10 applied; plus 3 provisional rows: `DF-REF-300` `parameter_value.load_id` (`UUID`, `uuid`), `DF-REF-301` `parameter_value.content_hash` (`TEXT`, `character(64)`), `DF-REF-302` `parameter_value.rollback_reason` (`TEXT`, `varchar(400)`); source system `Workbench`; `is_personal` false; descriptions from E1-042 spec rev 3 §7 field matrix, each prefixed "Provisional field ID (RWB-E1-001 ASM-E1001-17)." | PS v6; D-RCV-36 CR A.5; `ASM-E1001-17` |
| `sys_fields.is_personal` | `true` for exactly the 526 field IDs in `evidence/is_personal_union_v4.tsv` (14 true in both sources, 4 true in PS v6 only, 508 "Personal data = Yes" in PDPA v4 only), including all 17 PDPA v4 Restricted fields (12 Direct identifier, 5 Sensitive); `false` for the other 856. The value is the literal in each row's INSERT (T10), never a later `UPDATE` | `ASM-E1001-14` |
| `lov_value` | 598 as PS v6 (from line 4684) | DL v10 D-RCV-29; E1-043 spec "Seed ownership" |
| `role` | 54 as PS v6 (from line 5284) | DL v10 D-RCV-29 |
| `permission` | 421 as PS v6 (from line 5350) | DL v10 D-RCV-29 |
| `delegation_limit` | 0 | DL v10 D-RCV-29; Rulings v2 R3; PBR v2 §4 Q3 |
| `rule_package`, `rule_package_version` | 0 | `ASM-E1001-03` |
| Every other table | 0 | Story v7 §11 |

No seed row carries personal data. Owner user IDs exist only in environment load files (synthetic
users in DEV and SIT, Story v7 §3).

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
| C3 type | For each pair, the normalised column type equals `physical_type`: `varchar(n)`, `character(n)` (catalog `bpchar`, written `char(n)` in DDL), `numeric(p,s)`, `integer`, `bigint`, `smallint`, `boolean`, `date`, `timestamptz`, `uuid`, `text`, `jsonb`, arrays as `<type>[]`. An unlisted type fails as a mismatch. | `<field_id> physical type <expected> expected, <actual> found` |

Every failure is reported. Views are out of scope (BR9; RWB-E1-069). Proof fixtures on a throwaway
container schema, never in the migration folder: an extra `account_ext.branch_code` column (C1),
`account_ext.dispute_open` altered to `text` (C3), and a `character(64)` column matched to
`char(64)` (C3 pass).

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
migration-folder README text is aligned with E1-044 SPEC-015 (OPEN-NEW-9). `ASM-E1001-07`,
`GAP-E1001-11`.

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
- Module dependencies: `dataengine` → E1-043's published registry types (`recovery.casewf.refdata.api`
  or the package E1-043 publishes) and → `platform.api` (`MessageResolver`, `ApiProblemException`). No
  dependency in the other direction (D-RUN-11 "dependencies one way"); `ModulithTest.verify()` passes.

### SPEC-RWB-E1-001-013 `DataProductCatalogHandler.validate`

Implements the handler contract that RWB-E1-043 publishes for its table-code registry (D-RUN-11), with
the Story v7 §12 method set: `tableCode()` returns `"data_product"`; `validate(file)` checks every row
and writes nothing; `apply(loadId, file, validFrom)` writes all rows in one transaction and returns the
row count. Type names (`ReferenceTableHandler`, `ReferenceLoadFile`, `ValidationReport` in Story v7
§12) follow E1-043's published names (`ASM-E1001-05`). Because E1-043 holds no column definition for
`data_product` (its SPEC-003 covers 12 codes), structure checks are this handler's. All findings are
returned in this order: file-level, then rows in file order.

| Check | Rule | Message (MSG v4 ID) |
|---|---|---|
| K0 | Header is exactly `product_code, product_name, definition, system_of_record, owner_role, owner_user_id, refresh_cycle, expected_by` (Story v7 §13 seed columns plus the owner); every required value present; each value within its column width (SPEC-004) | Missing value: MSG-GEN-001 `{field}`; other structure failure: MSG-P3-027 `{check}` (`ASM-E1001-19`) |
| K1 | The set of `product_code` values equals DP01–DP14, each once | MSG-P1-004, `{products}` = missing codes ascending |
| K2 | `system_of_record` matches one of F1–F3 below | MSG-P1-003, `{product}` = code |
| K3 | `owner_user_id` is present and a UUID | MSG-P1-003 |
| K4 | `owner_role` is an active `role.role_code` (LOV-ROLE, `ASM-E1001-10`) | MSG-P1-007, `{field}` = `owner_role`, `{values}` = active role codes in sort order |
| K5 | `refresh_cycle` is an active `LOV-REFRESH` value (PS v6 lines 5035–5038) | MSG-P1-007, `{values}` = the list in sort order |

System-of-record forms (BR3, BR5). **Labelled assumption `ASM-E1001-09`**: derived from the 14 Story
v7 §13 seed values, AC3, AC7 and AC11; no document states a grammar. `S` = a source name: one or more
upper-case letters or digits (seed: ALS, SCBPDM, EFS, CCMS, SVAF, AMIS, RPS, LIT, WIN, COLLINS, GL) or
the phrase `the core bank`. `L` = `S`, or `S and S`, or `S, S, … and S`. `Q` = free text without `;`,
`(` or `)`.

| Form | Pattern (whole value, single spaces) | Seed rows that use it |
|---|---|---|
| F1 | `ACE (ingested from L)` | DP01, DP02, DP05, DP06, DP11, DP13 |
| F2 | `ACE (ingested from L) for Q, with Q held in the Recovery Workbench` | DP04, DP07 |
| F3 | `Recovery Workbench`, or `Recovery Workbench document hub`, or `Recovery Workbench, with the ACE lists read through the views` | DP03, DP08, DP09, DP10, DP12, DP14 |

Every seed value matches exactly one form (unit test over the 14 seed rows). Negative cases, each
refused with MSG-P1-003: `CCMS` (AC11); `ACE (ingested from CCMS); SVAF` (AC7 two systems); `ACE
(ingested from CCMS) and CCMS`; `Recovery Workbench and ACE`; `ACE (ingested from )`; `ACE (ingested
from ccms)`; `ACE (ingested from CCMS) (ingested from SVAF)`; `Workbench`; an empty value (also K0).
Row numbers count data rows from 1.

### SPEC-RWB-E1-001-014 `DataProductCatalogHandler.apply` and idempotency

- Called by RWB-E1-043 when the load version is approved (Story v7 §4 steps 9–10; E1-043 registry).
- In one transaction, updates the 14 rows matched by `product_code` with the file values and
  `valid_from`, increments `version`, sets `updated_at` and `updated_by`; returns 14. Any failure rolls
  back all 14 (BR4). No row is inserted or deleted after the seed (`ASM-E1001-08`).
- Repeat detection is E1-043's (content hash over canonical rows, E1-043 SPEC-006): an identical
  repeat is answered without calling `validate` or `apply` again, so nothing is written (AC10, X7). The
  response is E1-043's (`ASM-E1001-15`): today 201 with the same `ReferenceLoad` body. MSG-P1-011
  (`{source}` = "data product catalog", `{date}` = valid from; text Story v7 §14 / MSG v4 line 85) is
  registered in the resolver so that E1-043 can return it once `GAP-E1001-13` is ruled (409 Problem, the
  API v4 `E409` response, fits MSG v4's type "Error"; a message field on `ReferenceLoad` would be an API
  change).

### SPEC-RWB-E1-001-015 Refusal response and messages

A refused load returns HTTP 422 `application/problem+json` (API v4 `E422`, `Problem`) raised as
`ApiProblemException` through the E1-042 additive constructor (message ID, status, placeholders,
field) so that `ProblemFactory` resolves the text through `MessageResolver` (E1-042 spec rev 3
SPEC-022): `messageCode` = the first finding's ID (file-level before row-level); `detail` = every
finding text in order (AC7 shows DP06 and DP11; AC9 shows rows 4 and 5). How E1-043 carries the
handler's report into that exception is E1-043's (registry contract).

Messages are added to E1-042's interim `FixedMessageCatalog` (EN and TH), not held in this module:

| ID | English (Story v7 §14) | Thai |
|---|---|---|
| MSG-P1-003 | `{product} must name one system of record, written ACE (ingested from X) or Recovery Workbench, or both where the product holds both, and one named owner.` | MSG v4 line 77 Thai (written for the older English text); status Proposed (`GAP-E1001-14`, OPEN-005) |
| MSG-P1-004 | `The catalog must hold the 14 data products DP01 to DP14. Missing: {products}.` | MSG v4 line 78 |
| MSG-P1-007 | `Row {row}: {field} must be one of {values}.` | MSG v4 line 81 |
| MSG-P1-011 | `The {source} load for {date} is already complete or running. It was not run again.` | MSG v4 line 85 |

MSG-GEN-001 and MSG-P3-027 (K0) are already E1-042/E1-043 catalog entries. Story v7 §13 step 6 asks
for "the message table"; none exists in PS v6, and E1-042 owns the seam that a later message-table
story replaces (`GAP-E1001-14`). README decision 5 is not cited for this (finding 008). Tests assert
`messageCode`, the English text and that the Thai text is non-empty.

### SPEC-RWB-E1-001-016 Authority and inherited controls

- Load right: the endpoint's method check (Reference data C) is RWB-E1-043's. TC-E1-001-11:
  RW-DATASTEW (Reference data `RU` in the PS v6 permission seed) calling the load with
  `table = data_product` gets 403 `Problem` with MSG-P4-002 (`ApiExceptionHandler`), and
  `data_product` and `reference_version` are unchanged. RW-REFADM holds `CRUD` (PS v6) and may load.
- Access log (Story v7 X8 "the refusal is in the access log"): the access log is built by
  RWB-E1-039 (BS v6 order 28, after this story; its X6 writes an `AC-DENY` entry for a refusal). Under
  D-RUN-08 this story asserts the 403 and names the seam; the access-log assertion for
  `table = data_product` is added to RWB-E1-039's tests (`GAP-E1001-22`, OPEN-NEW-10). No log line in
  this story carries personal data.
- Approval: Story v7 §10 has RW-DATASTEW confirm (U); API v4 (line 3214) and E1-043 require Reference
  data A, held by no role in PS v6 (`GAP-E1001-08`, OPEN-NEW-2). Inherited controls on approval, not
  rebuilt here: maker-checker, the approver is not the loader (409 MSG-P7-002, API v4 approve
  description; E1-043); the approval decision-log entry with decision code `AC-VERS` (API v4 approve
  description; deferred by E1-043 to RWB-E1-027, E1-043 GAP-07). The end-to-end approval in TC-E1-001-03
  uses the approver E1-043 implements (E1-043 uses a synthetic approver fixture, its A-08).
- The migration runs as `rwb_migrator` (ADR-010); `recovery_svc` has DML only.

### SPEC-RWB-E1-001-017 Feature flag, registration and guardrails

- `rwb.p1.data-catalog` (default `false`; `true` in the local profile). On: `DataProductCatalogHandler`
  is a bean and is registered in E1-043's table-code registry. Off: not registered, so E1-043 refuses
  `table = data_product` as an unknown code (the previous path; E1-043 SPEC-002). The migration and the
  view are not behind the flag (Story v7 §13). Flag removal follows RWB-E1-047 (BS v6 order 16).
- Requirement on E1-043 (D-RUN-11; OPEN-NEW-3): a code with a registered handler is accepted and
  dispatched to that handler for `validate` at load and `apply` at approval, without needing a
  `LOV-REF-TABLE` value or a `refdata.columns.<code>` definition; E1-043 still records the version,
  hash and maker-checker. If E1-043's registry instead requires a `LOV-REF-TABLE` value, `data_product`
  is added by a `LOV-REF-TABLE` reference load, not by changing the PS v6 seed (`ASM-E1001-12`).
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

## Field-level behaviour matrix

| Object | Field | Source | Create / update | Rule |
|---|---|---|---|---|
| `data_product` | `product_code` | Seed, load file | Seed insert; never changed by load | DP01–DP14 (K1); unique |
| `data_product` | `product_name`, `definition` | Seed, load file | Seed; updated by `apply` | Required; ≤ 80 / 400 (K0) |
| `data_product` | `system_of_record` | Seed, load file | Seed; updated by `apply` | F1–F3 (K2); ≤ 200 (K0, `ASM-E1001-13`) |
| `data_product` | `owner_role` | Seed, load file | Seed `RW-DATASTEW`; updated by `apply` | Active role code (K4) |
| `data_product` | `owner_user_id` | Load file | NULL in seed; set by `apply` | Required in the file (K3); synthetic in DEV/SIT |
| `data_product` | `refresh_cycle` | Seed, load file | Seed; updated by `apply` | LOV-REFRESH (K5) |
| `data_product` | `expected_by` | Seed, load file | Seed; updated by `apply` | Optional; ≤ 20 (K0) |
| `data_product` | `valid_from` | Load request | Seed 2026-11-30; set by `apply` | From the load's valid from |
| `data_product` | standard columns | System | `version` +1, `updated_at`, `updated_by` on `apply` | — |
| `sys_objects`, `sys_fields` | all | Migration | Seed only | Later changes are reference loads (D-RCV-29) |
| `sys_fields` | `is_personal` | Migration | Seed per union | `ASM-E1001-14` |
| `v_data_dictionary` | all | View | Read only | SPEC-005 |

## Status-transition matrix

| Object | From | Event | To | Source |
|---|---|---|---|---|
| Recovery schema (Flyway) | E1-042 and E1-043 migrations applied (and baseline `0` where the S2 stand-in exists) | This migration applied | its history row `success = true` | Story v7 §9 |
| Recovery schema (Flyway) | as above | Migration fails | unchanged; no success row | AC4 |
| Data product catalog | seed (version 1) | Load approved and applied | `version` +1, 14 rows updated | Story v7 §9; E1-043 |
| Data product catalog | version in force | Same file loaded | unchanged | AC10 (`ASM-E1001-15`) |
| Data product catalog | version in force | Load refused | unchanged | AC7–AC9, AC11 |

No case status changes (Story v7 §9).

## Exceptional-case behaviour

| ID | Case | Behaviour | Evidence |
|---|---|---|---|
| X1 | Statement fails in the migration | Rollback; failing statement in the log; no success row | SPEC-007 |
| X2 | Column without dictionary row, field without column, or type mismatch | Conformance test fails with the C1–C3 texts | SPEC-009 |
| X3 | Migration already applied | Nothing applied | SPEC-008 |
| X4 | No / two / bare system of record, or no owner | 422, MSG-P1-003 per product, nothing written | SPEC-013, -015 |
| X5 | Not exactly DP01–DP14 | 422, MSG-P1-004 naming the missing codes | SPEC-013, -015 |
| X6 | Owner role or refresh cycle outside its list | 422, MSG-P1-007 per row and field | SPEC-013, -015 |
| X7 | Same file again | Nothing written; response per E1-043 (`GAP-E1001-13`) | SPEC-014 |
| X8 | Caller without Reference data C | 403, MSG-P4-002; access-log entry is the RWB-E1-039 seam | SPEC-016 |
| X9 | S1=`true` with recovery Flyway on | Refused by configuration; documented invalid combination | SPEC-010 |
| X10 | Flag `rwb.p1.data-catalog` off | `data_product` refused by E1-043 as an unknown code | SPEC-017 |
| X11 | Catalog file with a wrong header, a missing value or a value longer than its column | 422, MSG-GEN-001 or MSG-P3-027, nothing written | SPEC-013 K0 |

## API change assessment

No endpoint, schema or response is added or changed. The story uses `POST /admin/reference-loads`
(`postAdminReferenceLoads`, x-module P4, Reference data C) and `/{loadId}/approve` (Reference data A),
both owned and built by RWB-E1-043 (D-RUN-10, D-RUN-11). `table` is a free string, so `data_product`
needs no API change. `ReferenceLoad` (line 8832: `id`, `table`, `validFrom`, `status`, `rows`) has no
message field; AC10's message is therefore recorded as `GAP-E1001-13` for E1-043 / the API owner rather
than changed here. API v4 names "ReferenceTableLoader" for P5 tables and Story v7 §12 names
`ReferenceTableHandler`; the registry's names are E1-043's (`GAP-E1001-07`). Contracts:
`contracts/backend-apis.json`.

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | Story v7 §15 | No screen, route, component or i18n key. | None. |
| Backend | YES — migration, `dataengine` catalog classes, handler registration, seed checks | REQUIRED | 80% lines, branches, statements and functions on `th.co.scb.ace.demo.recovery.dataengine` | SPEC-001 to -010, -012 to -018; AC1–AC11; BR1–BR9 | K0–K5, F1–F3, the apply transaction, flag-gated registration and the seed-width check are hand-written logic. JUnit 5 with AssertJ; JaCoCo. | Each of K0–K5 and F1–F3 has a pass and a fail case (AC7, AC8, AC9, AC11 data from Story v7 §16, plus the SPEC-013 negative list); every Story v7 §13 seed value matches exactly one form; all findings in order; `validate` writes nothing; `apply` rolls back all rows on failure; handler absent when the flag is off; seed values fit their columns. |

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
| TC-E1-001-05 | AC5, BR1 | IT | Both AC5 texts; `character(64)` pass case | This story |
| TC-E1-001-06 | AC6 | IT | Second migrate applies 0; 123 / 1,382 unchanged | This story |
| TC-E1-001-07 | AC7 | Unit + E2E | 422, MSG-P1-003 for DP06 and DP11 | as TC-03 |
| TC-E1-001-08 | AC8 | Unit + E2E | 422, MSG-P1-004 "Missing: DP09." | as TC-03 |
| TC-E1-001-09 | AC9 | Unit + E2E | 422, two MSG-P1-007 texts (DP_OWNER, HOURLY) | as TC-03 |
| TC-E1-001-10 | AC10 | E2E | Second load: same `ReferenceLoad.id`, no new `reference_version`, `data_product` rows and `version` unchanged; response asserted as E1-043 specifies (`ASM-E1001-15`) | after E1-043 |
| TC-E1-001-11 | X8 | E2E (access) | RW-DATASTEW: 403, MSG-P4-002, nothing written; access-log entry asserted in RWB-E1-039 | after E1-043 |
| TC-E1-001-12 | AC11 | Unit + E2E | 422, MSG-P1-003 for DP06 "CCMS" | as TC-03 |
| TC-E1-001-13 | BR3, SPEC-018(1) | Unit + IT | Every seed value fits its column; DP07 verbatim (139) | This story |
| TC-E1-001-14 | BR7, SPEC-018(2) | IT | 526 `is_personal = true` exactly as the fixture list | This story |
| TC-E1-001-15 | SPEC-010 | IT | `RecoveryDatabaseIT` passes in S1=`false`, S2=`true` with every existing assertion | This story |
| TC-E1-001-16 | SPEC-017 | Unit | Flag off: no handler bean; flag on: registered for `data_product` | This story |
| TC-E1-001-17 | BR7, SPEC-018(4), T10 | Unit + CI lint | `is_personal` only as INSERT literals (no `UPDATE sys_fields`), 526 `true`; RWB-TE-011 PDPA lint over the migration: zero findings | This story (lint part once RWB-TE-011 is merged) |

All test data is synthetic (random UUIDs, no names or account numbers).

## Guardrails and out of scope

- Out of scope (Story v7 §19): the 30 `v_ace_*` views, helper functions, grants and the view
  conformance test (RWB-E1-069); freshness (RWB-E1-015); access per data product, PDPA masking and the
  catalog entry screen (RWB-E1-016); retention (RWB-E1-017); Stage 2 products; the dictionary endpoint
  and field versions (RWB-E1-064). Also not here: rule package content (E1-072 v7 §13), `delegation_limit`
  content (RWB-E1-038), the access log (RWB-E1-039), the message table (no owner yet).
- Not rebuilt (phase0 audit A-04): `RecoveryFlywayConfig`, the lint, `20-grants.sql.inc`,
  `ApiError`/`ProblemFactory`, `MessageResolver`.
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
| CLAR-007 | Story v7 §3, §12; D-RUN-11 | Handler seam owner. | Registration. | E1-043 registry; this story registers (`ASM-E1001-05`). | RESOLVED | 013, 014, 017 |
| CLAR-008 | Lint; PS v6 literals; D-RUN-13 | 297 `'public.…'` literals. | Merge. | Lint ignores literals (E1-044 SPEC-007). | RESOLVED | 011 (retired) |
| CLAR-009 | Story v7 §10; E1-043; API v4 line 3214 | Who approves a `data_product` load? | E2E approval. | Open item OPEN-NEW-2. | OPEN (non-blocking) | 016 |
| CLAR-010 | Story v7 §14; MSG v4 line 77 | MSG-P1-003 wording and Thai. | Message text. | Story v7 English; MSG v4 Thai as Proposed (OPEN-005). | RESOLVED | 015 |
| CLAR-011 | Story v7 §13 DDL vs seed; PS v6 line 820 | DP07 is 139 characters for `varchar(120)`: widen or shorten? | Seed, DDL, DF-REF-074. | No precedence rule (same document). Proceeding on `ASM-E1001-13` (widen to 200). Ruling needed from the data architect (OPEN-NEW-6). | OPEN (Blocker = Yes gap 17) | 004, 006, 018 |
| CLAR-012 | Story v7 BR7; PS v6 `is_personal`; PDPA v4 | Which source decides `is_personal`? | 508 seed flags. | No precedence rule. Proceeding on `ASM-E1001-14` (protective union). Ruling needed from the data architect with the DPO (OPEN-NEW-7). | OPEN (Blocker = Yes gap 18) | 006, 018 |
| CLAR-013 | Story v7 AC10; API v4 `ReferenceLoad`; MSG v4 line 85; E1-043 SPEC-006 | How does a repeat response carry MSG-P1-011? | AC10 message clause. | E1-043 / API owner (OPEN-NEW-8); this story asserts "writes nothing" (`ASM-E1001-15`). | OPEN (non-blocking) | 014 |

`CLARIFICATION_STATUS: RESOLVED_WITH_OPEN_ITEMS` — CLAR-011 and CLAR-012 are Blocker = Yes document
gaps carried on labelled assumptions; a human ruling is required before build. No question was asked
(L-RCV-03).

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); sources read from the document set.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: One recovery migration from Physical Schema v6 (89 tables, dictionary, seeds, v_data_dictionary), the data product catalog handler registered with RWB-E1-043, seed and conformance tests, and the local switch to a Flyway-built schema; no screen; no API change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NO_API_CHANGE] [REASON: uses the existing reference-load endpoint owned by RWB-E1-043 with table data_product]
REQUIREMENT_COVERAGE_SUMMARY: 9 business rules, 11 ACs, exception groups, authority, contract, plan, guardrails, out of scope and NFRs mapped in 33 rows.
REQUIREMENT_COVERAGE_RESULT: PARTIAL [TOTAL_RULES: 33] [COVERED_RULES: 28] [COVERED_ON_BLOCKER_ASSUMPTION: 3 (BR3, BR7, NFR-RWB-006)] [PARTIAL: 1 (AC10)] [NOT_APPLICABLE: 1] [MISSING_RULES: 0] [CONTRADICTIONS: 2 unresolved by precedence, Blocker = Yes (GAP-E1001-17, -18)]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED_WITH_OPEN_ITEMS [OPEN_ITEMS: 4 (CLAR-011, CLAR-012 Blocker = Yes; CLAR-009, CLAR-013 non-blocking)]
NEXT_STEP: Spec gate round 2 (review/spec-gate-review-2.md); human ruling on GAP-E1001-17 and GAP-E1001-18 before the Implementation Planner.
```
