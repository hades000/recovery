---
title: "Technical Specification — RWB-E1-069 Read-only ACE source views, grants and boundary rule"
run_id: "INC-010-epic-1-RWB-E1-069"
story: "RWB-E1-069"
revision: "run 4 (remediation of spec gate round 3, REVIEW-RWB-E1-069-122..124: coverage-scope wording, RWB-TE-001 re-baselined on v4, OI-069-A scope); run 3 kept as spec.run3.md and run 2 as spec.run2.md"
status: "SUCCESS"
---

# Technical Specification — RWB-E1-069 Read-only ACE source views, grants and boundary rule

| Field | Value |
|---|---|
| Story | RWB-E1-069. Epic E1. Module P1 Recovery data engine. Feature FEAT-RDF-01. Priority Must. |
| RUN_ID | `INC-010-epic-1-RWB-E1-069` |
| Increment card | `aisdlc/docs/increments/INC-010-epic-1-RWB-E1-069.md`. Build order 10 of 72 ([S14] Build Sequence v6). |
| Source requirement | [S1] Story RWB-E1-069 v1, Epic 1 Story Files v7, 15 Nov 2026 |
| Upstream IDs | REQ-RDF-002, REQ-DRI-006 → BR-RWB-013 → FR-RWB-013 (`aisdlc/requirement/Traceability_Matrix.md` §3 row 010). D-RCV-35 U1 and U4. ADR-010. DL43. |
| Depends on (D-RUN-08) | Earlier stories in [S14]: RWB-E1-044 (order 1; lint structure and seams, D-RUN-14 migration-account rights, [T3] v14-7), RWB-TE-001 (order 2; module map, loader, coverage counters, [T1] v4), RWB-E1-001 (order 9; the migration that seeds the tables and dictionary, [T2] Revision 4). External: RWB-ACE-001 (ACE team; Section B only, DL43). |
| Blocks | RWB-E1-002, RWB-E1-016, RWB-E1-018 |
| Gate | Round 1 FAIL (`../review/spec-gate-review.md`), round 2 FAIL (`../review/spec-gate-review-2.md`) and round 3 FAIL, Low-only (`../review/spec-gate-review-3.md`). This revision answers every round-3 finding (`gate-response.md`, Round 3); the orchestrator runs round 4 as `../review/spec-gate-review-4.md`. |
| Prepared | 2026-11-18, Technical Specifier (agent run, remediation run 3). The D-RUN-14 ruling is the orchestrator's decision, not a human approval; its ratification is open (OI-069-M, proposed OPEN-051). |

## Sources

Paths marked `legacy/` are relative to `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/`.

| Tag | Document, version | Path |
|---|---|---|
| S1 | Story RWB-E1-069 v1, Epic 1 Story Files v7, 15 Nov 2026 | `legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-069-read-only-ace-source-views-grants-and-boundary-rule-v1.md` |
| S2 | Recovery Workbench ACE Source Views v1 | `legacy/15-ace-db-alignment/recovery-workbench-ace-source-views-v1.sql` |
| S3 | Recovery Workbench Physical Schema v6, 16 Nov 2026 | `legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| S4 | ACE Team Stories v1, story RWB-ACE-001 | `legacy/04-user-stories/recovery-workbench-ace-team-stories-v1.md` |
| S5 | Story RWB-E1-001 v1, Epic 1 Story Files v7 | `legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md` |
| S6 | RWB-E1-001 Specification Rulings v2 | `legacy/01-decisions-and-governance/recovery-workbench-rwb-e1-001-specification-rulings-v2.md` |
| S7 | Architecture Decision Records v3, ADR-010 | `legacy/05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md` |
| S8 | Decision Log v10 (DL43) | `legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| S9 | Client decision D-RCV-35, ACE DB alignment | `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md` |
| S10 | D-RCV-28, D-RCV-34, D-RCV-37 | `aisdlc/docs/decisions/INC-001-decisions.md` |
| S11 | Build Notes Epic 1 v6 | `legacy/04-user-stories/recovery-workbench-build-notes-epic-1-v6.md` |
| S12 | Environment and Deployment Design v4 | `legacy/05-technical-architecture/recovery-workbench-environment-and-deployment-design-v4-docx.md` |
| S13 | Security and Access Design v4 | `legacy/05-technical-architecture/recovery-workbench-security-and-access-design-v4-docx.md` |
| S14 | Build Sequence Epic 1 and Epic 2 v6 | `legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` |
| S15 | ACE Schema PostgreSQL v1 | `legacy/15-ace-db-alignment/ace-schema-postgresql-v1.sql` |
| S16 | Data Classification and Personal Data Inventory v4 | `legacy/06-data/recovery-workbench-data-classification-and-personal-data-inventory-v4-xlsx.md` |
| S17 | Client decision D-RCV-36 (change register A.7, row 18) | `aisdlc/docs/decisions/d-rcv-36-temporal-and-drools.md` |
| S18 | Non-Functional Specification v3 | `legacy/03-requirements-and-specifications/recovery-workbench-non-functional-specification-v3-docx.md` |
| S19 | AI-SDLC build log, §1 decisions D-RUN-07, D-RUN-12 and D-RUN-14 (orchestrator decisions; D-RUN-14 ratification open) | `AI-SDLC-BUILD-LOG.md` |
| C1 | backend-context (CONTEXT-20261116) | `aisdlc/.github/contexts/backend-context.md` |
| C2 | backend-standards (BS-*) | `aisdlc/.github/contexts/backend-standards.md` |
| C3 | testing-standards | `aisdlc/.github/contexts/testing-standards.md` |
| E1 | Phase 0 standards audit (A-02, A-04) | `aisdlc/evidence/phase0-standards-audit.md` |
| E2 | PostgreSQL 16.16 probes run by this stage (throwaway `postgres:16.16-alpine` containers, removed after use) | `agent-run-log.md` § "Run 2 probe evidence", § "Run 3 probe evidence" |
| R1 | Repository README ("Local versus target"; "Decisions taken while setting this up" 1–7) | `README.md` |
| T1 | RWB-TE-001 spec, revision **v4** (the PASS state, spec gate review-5; SPEC-RWB-TE-001-002 module map, -003 loader with the opaque `sourceViews`, -020 coverage counters, -021 withdrawn to E1-069, -022 relocation, -023 property binding, -024 coverage tests) | `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md` |
| T2 | RWB-E1-001 spec, **Revision 4** (the PASS state; counting table; T6, T7, T10; SPEC-006, SPEC-010; ASM-E1001-14, -17, -18; GAP-E1001-18; review-4) | `aisdlc/output/INC-009-epic-1-RWB-E1-001/specify/spec.md` |
| T3 | RWB-E1-044 spec, **v14-7** (the PASS state; SPEC-016 seams; SPEC-017 and T-044-17 under D-RUN-14; OI-E044-I, -J) | `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/spec.md` |

**Code baseline, read only (audit A-04).** Under `backend/src/`: `main/java/th/co/scb/ace/demo/recovery/platform/internal/RecoveryFlywayConfig.java`; `test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryBoundaryTest.java`; `test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java`; `test/java/th/co/scb/ace/demo/recovery/RecoveryDatabaseIT.java`; `PlatformInfoController.java`; `main/resources/application.yaml`; `main/resources/db/modulemigration/recovery/README.md`. Also `backend/build.gradle.kts`, `.env.example`, `docker-compose.yml`, `infra/postgres/init/` (`00-roles-and-databases.sh`, `10-load-ace-database.sh`, `20-grants.sql.inc`) and `infra/postgres/schema/02-ace-tier2-probe.sql`. Earlier stories relocate some of these ([T1] SPEC-022 moves `RecoveryFlywayConfig` to `recovery.casewf.migration`; [T3] SPEC-016 moves the lint into a test-scope tooling package). This spec names the class, not the package.

## User story intent interpretation

The recovery module reads ACE source data only through 30 `recovery.v_ace_*` views, and only with SELECT. Section A has 16 views and 177 fields over tables ACE holds today. Section B has 14 views and 127 fields over the tables RWB-ACE-001 adds ([S1] §1, §2, §11; [S9] U1, U4; [S7] ADR-010).

The boundary is enforced twice:
- **In the catalog.** `ace_view_owner` owns the views. `recovery_svc` holds SELECT on the views and nothing in `public`. PUBLIC holds nothing.
- **In the build.** BND-6 fails the build when a recovery class names a `public` table ([S1] BR8).

The story owns no business row, endpoint or screen ([S1] §9, §12, §15). It delivers two migrations, one conformance test class, the hardened BND-6 rule, the `sourceViews` key, the two lint seams that [T3] hands to it, and the local switch to Flyway mode that [T2] hands to it.

## Change Scope Declaration

| Item | Value |
|---|---|
| Change Type | `NEW_STORY`. Matrix §3 row 010: "No current spec/plan". No v_ace migration, conformance test or `sourceViews` exists in the code. |
| UI In Scope | NO. [S1] §15: "No screen in this story". |
| Logic In Scope | YES. Grants, the read boundary, helper functions, BND-6, conformance checks, lint seams, local init mode. |
| API In Scope | NO. [S1] §12: "No endpoint and no event". |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `RecoveryBoundaryTest` (BND-6), the [T3] lint (`isAllowedQualifier`, L-GRANT, L-KEY-DUP), `RecoveryDatabaseIT` (moved to Flyway mode), `RecoverySchemaMigrationIT` from [T2] (exclusion assertions evaluated at the version of the RWB-E1-001 migration), `infra/postgres/init/20-grants.sql.inc` and `10-load-ace-database.sh` (Flyway-mode branch), `.env.example`, `docker-compose.yml`, `README.md` "Local versus target", the migration-folder README. |
| New Nodes Required | YES: the Section A file, the Section B file, `ViewConformanceTest`, the `sourceViews` key and its reader, the BND-6 detector in the [T1] boundary tooling package, a test-scope `RecoveryFlywayTestSupport` factory that clears the bean's init method (SPEC-018), fixtures. |
| Inherited Existing Behavior | `RecoveryFlywayConfig` settings (C2 BS-2.3); the D-RUN-14 rights of `rwb_migrator` delivered by [T3] v14-7 in `20-grants.sql.inc`; the D-RCV-28 lint for every other statement and story; `PlatformInfoController` and `visiblePublicTables` = 0; BND-1..5 and the determinism rules; the extension tables, dictionary rows and `v_data_dictionary` created by the RWB-E1-001 migration ([T2] Revision 4). |
| Frontend Changes Required | NO. `frontend/src/modules/recovery/api/platform.ts` reads an unchanged response. |
| Backend Changes Required | YES: SQL migrations, test classes, test-scope tooling, a test resource, local init and configuration defaults. No main-source Java class changes. |

## Entry trigger and preconditions

- **Trigger.** The pipeline `migrate` step at deployment (RWB-E1-044). Locally, Flyway runs at application start and in the `recovery-it` tests ([S1] §12; `RecoveryFlywayConfig`).
- **P1.** The RWB-E1-001 migration (build order 9) is applied: recovery tables, the four extension tables, dictionary rows and `v_data_dictionary` ([S1] §3; [S5]; [T2] Revision 4 SPEC-006). It does not carry the views or the three helper functions ([T2] Revision 4 table T6: "Not carried. RWB-E1-069 owns them"). Build-order dependency (order 9 before 10). Its version is read from its file name at test time; D-RUN-12 keeps its table set to the tables no earlier story creates.
- **P2.** ACE `public` holds the 21 Tier 1 tables ([S1] §11; verified against [S15]). OPEN-035 (existing open item) asks the ACE team to confirm they are at the baseline head in DEV and SIT; it remains open and is Blocker = No for the spec (an environment precondition, checked by check 1; `shared-updates.md` §2).
- **P3.** The roles `ace_view_owner` (NOLOGIN) and `recovery_svc` exist ([S1] §3). This story creates no role (DG-L09). Locally `00-roles-and-databases.sh` creates them.
- **P4. Rights of the migration account (D-RUN-14) and ACE DBA preconditions for DEV, SIT and PROD.** [S1] §3 gives the migration account "the ACE DBA role for the release window". That role is declined ([T3] v14-7 SPEC-017; D-RCV-35 U3, U4; ADR-010). Orchestrator decision D-RUN-14 ([S19]; logged 2026-11-18T00:31) gives `rwb_migrator` exactly two rights for the ACE views and no other right in `public`:
  - (a) `USAGE ON SCHEMA public`, with **no** table privilege (no SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES or TRIGGER on any `public` relation). USAGE resolves the `public.<table>` name in `CREATE VIEW`; verified on PostgreSQL 16.16 ([E2] run 3): the view is created without any table privilege;
  - (b) `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE` (`ADMIN` false), for `ALTER VIEW ... OWNER TO ace_view_owner` only. PostgreSQL lets a role change an object's owner only to a role it can SET ROLE to; `INHERIT FALSE` means the owner's SELECT on ACE tables never reaches the migration account ([E2] run 3: `has_table_privilege` false for every `public` relation and a direct read is refused; the FK/`REFERENCES` refusal is T-044-17's (f), [T3] v14-7).
  - It never holds the ACE DBA role, a table privilege in `public`, `CREATE` on `public`, `ADMIN` on `ace_view_owner`, or any other role membership. The SELECT grants to `ace_view_owner` stay with the ACE DBA and are not in these files.
  - (c) Ownership of schema `recovery`, or the right to grant CREATE on it, for the transient `USAGE, CREATE` grant the owner change needs (without CREATE: `permission denied for schema recovery`, [E2]; DG-L12).
  - (d) Outside the migration and done by the ACE DBA ([S9] §8.2; [S4] flow step 5, §10, §12 step 4): `USAGE ON SCHEMA public` and SELECT on the 21 Tier 1 tables for `ace_view_owner`; SELECT on the 14 Tier 2 tables with RWB-ACE-001; `REVOKE ALL ON SCHEMA public FROM PUBLIC`. See SPEC-004 and DG-L22.
  - (e) [T3] v14-7 delivers (a) and (b) in `infra/postgres/init/20-grants.sql.inc` as the local stand-in (its SPEC-017). E1-069 relies on them and does not repeat them; its SEAM-E044-02 still fails any `GRANT ... TO rwb_migrator` in a `rwb_e1_069` file. T-044-17 remains the test that owns (a) and (b), so this story does not weaken it; SPEC-008 check 5 re-asserts them as a precondition of the E1-069 files.
  - (a)–(b) are D-RUN-14's two rights. **Who applies them in SIT, UAT and PROD** stays [T3] v14-7 OI-E044-I; this spec does not answer that question and claims no ownership of it. Proposed open item OI-069-A carries **only (c)–(d)** to the ACE DBA and the environment owner. OI-069-M (proposed OPEN-051) asks the recovery tech lead to ratify D-RUN-14. Until it is ratified the spec applies D-RUN-14 as the orchestrator's decision and claims no human approval (DG-L29).
- **P5.** The module map `backend/src/test/resources/architecture/recovery-modules.yaml` and its loader exist, delivered by RWB-TE-001 (order 2). The loader carries the optional top-level `sourceViews` key unvalidated ([T1] SPEC-003). E1-069 adds the key and its validation (ASM-006).
- **P6.** The [T3] lint structure exists: a rule registry, `isAllowedQualifier(statement, qualifier)` as the single qualifier extension point, and seams SEAM-E044-01 and -02 owned by E1-069 ([T3] v14-7 SPEC-016). See ASM-011.
- **P7.** Section B only: RWB-ACE-001 is deployed ([S1] §3; [S8] DL43). Locally the Tier 2 probe with its grant stand-in (SPEC-015) takes its place ([R1] "Local versus target"). The external dependency is DG-L16, Blocker = No.

## Backend Specification

### Specification items

| SPEC ID | Specification | Source |
|---|---|---|
| `SPEC-RWB-E1-069-001` | **Section A file.** `V<seq>__rwb_e1_069_ace_source_views.sql` in `backend/src/main/resources/db/modulemigration/recovery/`. Line 1 is `-- Story: RWB-E1-069`. No `SET search_path`, no `CREATE SCHEMA` (the [S2] line 23 statement is not carried; `createSchemas(false)`). Every recovery object is written `${recoverySchema}.<name>`. `<seq>` is assigned at merge (D-RUN-07). No environment name. Contents in order: the schema-wide PUBLIC revoke (SPEC-004 step 1), the helper functions (SPEC-002), the 16 views (SPEC-003), the grant block (SPEC-004 steps 2–11). | [S1] §4 steps 1–2, §12; [S10] D-RCV-28; C2 BS-2.3; RUN-BRIEF D-RUN-07; DG-L04, DG-L15 |
| `SPEC-RWB-E1-069-002` | **Helper functions.** `${recoverySchema}.ace_to_date(text) RETURNS date`, `${recoverySchema}.ace_to_boolean(text) RETURNS boolean` and `${recoverySchema}.ace_mask_value(text) RETURNS text`, each `CREATE OR REPLACE`, `LANGUAGE sql`, `IMMUTABLE`, with the [S2] `COMMENT ON FUNCTION` text. `ace_to_boolean` and `ace_mask_value` are carried from [S2] lines 49–86 unchanged (verified correct on PG 16, [E2]). `ace_to_date` **must meet the behaviour in the BR6 table below, not the [S2] body**, because the [S2] body raises on well-formed impossible dates (DG-L23; ASM-012). The function must never raise for any `text` input and must not depend on `DateStyle`. | [S1] BR6; [S2] lines 29–30 (intent), 31–43 (defective body); [T2] T6; DG-L02, DG-L23 |
| `SPEC-RWB-E1-069-003` | **The 16 Section A views (A1–A16).** Copied from [S2] lines 94–452. Only the `recovery.` qualifier changes, to `${recoverySchema}.`. Every `public.<table>` qualifier stays. Created with `CREATE OR REPLACE VIEW` and without `security_invoker` (PostgreSQL default false), so table access is checked against the owner (the ADR-010 design, [S2] lines 16–21). No other `v_ace_*` view is created. No PK, no FK. Verbatim evidence: after removing comments and blank lines, [S2] lines 94–711 equal [S3] lines 6204–6821 (524 lines; Section A 313, Section B 211) and the helpers equal [S3] lines 6141–6196 ([E2]; confirmed by round-1 review). | [S1] §4 step 1, §12; AC1; [S7] ADR-010 |
| `SPEC-RWB-E1-069-004` | **Section A grant block** (order below). Only recovery-side objects and roles. No GRANT or REVOKE on schema `public` or on a `public` table; no `GRANT ... ON ALL TABLES` (the single `ON ALL TABLES` statement is the REVOKE from PUBLIC, run before any view exists). The migration account holds exactly the D-RUN-14 rights of P4(a)–(b) and creates the views through its own ownership; it never SELECTs a `public` table. | [S1] §12, BR2, BR3; [S9] §8.2; [S7] ADR-010; [S19] D-RUN-14; [T3] v14-7 SPEC-017; DG-L11, DG-L12, DG-L22, DG-L29 |
| `SPEC-RWB-E1-069-005` | **Section B file.** `V<seq>__rwb_e1_069_ace_tier2_views.sql`, header rules as SPEC-001. It merges only after RWB-ACE-001 is deployed in every environment main deploys to, because `outOfOrder(false)` and one history table make a present version impossible to skip and apply later (DG-L20; OI-069-D). Here the probe stands in (ASM-005). | [S1] §4 steps 7–8, §13 step 7, BR9; `RecoveryFlywayConfig` |
| `SPEC-RWB-E1-069-006` | **The 14 Section B views (B1–B14) and their grants.** Copied from [S2] lines 461–711 with the SPEC-003 rules. The grant block runs SPEC-004 steps 5–11 for the 14 views (idempotent USAGE re-assertion, transient `USAGE, CREATE`, per-view revoke, SELECT grant while the migration account owns the view, owner change, final revoke); the helpers and their EXECUTE grants are already in place from Section A. It omits SPEC-004 step 1: by then the 16 Section A views are owned by `ace_view_owner`, so a schema-wide `REVOKE ... ON ALL TABLES` fails with `permission denied for table v_ace_*` ([E2] run 3); the per-view revoke removes PUBLIC and the default-privilege entries instead. The file grants nothing on a Tier 2 table (RWB-ACE-001 does, [S4] flow step 5; [S9] §8.2). | [S1] §4 step 7, §12; AC3; REVIEW-102; [E2] |
| `SPEC-RWB-E1-069-007` | **Extension tables verified, not created.** `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` ship in the RWB-E1-001 migration ([S1] §4 step 1; [S5]; [T2] Revision 4 SPEC-003, SPEC-006). Neither E1-069 file creates or alters them. SPEC-011 proves their shape. | DG-L01 |
| `SPEC-RWB-E1-069-008` | **`ViewConformanceTest`**, the single host for the conformance checks (REVIEW-116). `backend/src/test/java/th/co/scb/ace/demo/recovery/ViewConformanceTest.java` (package per [T1] module layout if it moves; the plan names it), `@Tag("recovery-it")`. It hosts SPEC-008 to SPEC-011, SPEC-017, SPEC-019 and SPEC-020. Checks, session roles and connection input are set out below. | [S1] §4 step 4, §12, §13, §14; X1, X3, X4, X5; C3; ASM-004 |
| `SPEC-RWB-E1-069-009` | **Access tests (AC2).** Assertions below. | [S1] AC2, BR2, BR3, X5 |
| `SPEC-RWB-E1-069-010` | **Dictionary tests (AC5, AC6).** Assertions below, including the totals ([T2] Revision 4 seeds 1,382 `sys_fields` and 1,078 table fields) and the values asserted where sources disagree. | [S1] AC5, AC6, BR5; [S3]; [S17]; [T2] Revision 4 SPEC-006, ASM-E1001-14, -17; DG-L05 |
| `SPEC-RWB-E1-069-011` | **Extension-table tests (AC7, BR7).** Assertions below, including the seven standard record columns. | [S1] AC7, BR7, X7, §13; [S3] lines 2087–2150; [T2] counting table |
| `SPEC-RWB-E1-069-012` | **BND-6 hardening.** Extends `RecoveryBoundaryTest` (A-04). The detector and the table-to-view map live in the [T1] test-scope boundary tooling package, so the coverage gate measures them. Rule below. | [S1] AC8, BR8, X6, §13, §14; E1 A-02; [T1] SPEC-021 (withdrawn to E1-069) |
| `SPEC-RWB-E1-069-013` | **Module map `sourceViews`** and its validation. Structure and rules below. | [S1] §4 step 5, §11, §13, BR9; [S10] D-RCV-37; [T1] SPEC-002, SPEC-003 |
| `SPEC-RWB-E1-069-014` | **Lint seams SEAM-E044-01 and SEAM-E044-02**, implemented in the [T3] lint. Rules below. | [T3] SPEC-016; [S9] §3.2, §8.2; [S7] ADR-010; [S10] D-RCV-28; DG-L03 |
| `SPEC-RWB-E1-069-015` | **Local mode switch and stand-ins** (hand-over from [T2] Revision 4 SPEC-010; REVIEW-103, -107, -118). The S1 switch is owned by RWB-E1-001; E1-069 takes the S2 `RWB_LOAD_REFERENCE_VIEWS` switch, states S3 and makes the view files the only local source of the 30 views. Details below. | [T2] Revision 4 SPEC-RWB-E1-001-010, ASM-E1001-07, -18; [R1] "Local versus target"; [S4] flow step 5; [S19] D-RUN-14 |
| `SPEC-RWB-E1-069-016` | **No API, UI or main-code change.** `PlatformInfoController` stays as it is and must stay green under BND-6 (ASM-013). | [S1] §12, §15; [R1] decision 6 |
| `SPEC-RWB-E1-069-017` | **Flyway history and re-run (AC1, AC3).** Assertions below. The version-`0` baseline row exists only while [T2]'s S2 views-only stand-in is on; after E1-069 flips S2 to false the schema is empty at init and no baseline row is written ([T2] Revision 4 ASM-E1001-18). | [S1] AC1, AC3; REVIEW-109(a), -118(4) |
| `SPEC-RWB-E1-069-018` | **X2 negative test**, driven through the bean's own Flyway configuration obtained without its `initMethod` (SPEC-018 mechanism). Details below. | [S1] AC3, §5 X2; REVIEW-105, -121(c) |
| `SPEC-RWB-E1-069-019` | **Data protection of the published interface.** Classification, controls and tests below. | [S16]; [S9] §3.3, §12 R5; [S2] lines 16–21; [S1] §17, §19; REVIEW-108 |
| `SPEC-RWB-E1-069-020` | **Helper-function tests (BR6).** Positive and negative cases below. | [S1] BR6; [E2]; REVIEW-101 |

### SPEC-002: required behaviour of `ace_to_date` (BR6)

Input is trimmed (`btrim`). The result is a date only when the trimmed text matches one of three exact shapes **and** names a real calendar date with year 1 or later. Every other input, including NULL, returns NULL. The function never raises.

| Shape | Interpretation | Example inputs → result |
|---|---|---|
| `^\d{4}-\d{2}-\d{2}$` | ISO `YYYY-MM-DD` | `2026-02-28` → 2026-02-28; `' 2026-02-28 '` → 2026-02-28; `2024-02-29` → 2024-02-29; `2025-02-29`, `2026-02-30`, `2026-13-01`, `2026-00-10`, `0000-01-01` → NULL |
| `^\d{8}$` | `YYYYMMDD` | `20260228` → 2026-02-28; `20261345`, `20250229`, `00000000` → NULL |
| `^\d{2}/\d{2}/\d{4}$` | `DD/MM/YYYY` | `28/02/2026` → 2026-02-28; `29/02/2024` → 2024-02-29; `31/02/2026`, `01/13/2026` → NULL |
| anything else | — | NULL, `''`, `'   '`, `garbage`, `2026-2-28`, `2026/02/28`, `2026-02-28 10:00`, `12345678901` → NULL |

Why the [S2] body fails this ([E2], PostgreSQL 16.16): `'2026-02-30'::date`, `to_date('20261345','YYYYMMDD')`, `to_date('31/02/2026','DD/MM/YYYY')` and `'0000-01-01'::date` each raise `date/time field value out of range`; `to_date('00000000','YYYYMMDD')` returns `0001-01-01 BC` instead of NULL.

*Non-normative note.* A body that met every row of the table on PostgreSQL 16.16, both as literal calls and through a view over rows, and under `DateStyle` `ISO`, `SQL, DMY` and `German`, is: normalise each shape to an ISO string with `substr`, then return `iso::date` only when `pg_input_is_valid(iso, 'date')` is true ([E2]; `pg_input_is_valid` exists from PostgreSQL 16). The builder may use any body that passes SPEC-020.

### SPEC-004: Section A grant block, in order

Run as the migration account (`rwb_migrator`), which owns schema `recovery` (P4(c)) and holds exactly the D-RUN-14 rights (P4(a)–(b)). Every step below was run in sequence on PostgreSQL 16.16, in one session and one transaction ([E2] run 3).

1. `REVOKE ALL ON ALL TABLES IN SCHEMA ${recoverySchema} FROM PUBLIC` ([S1] §12 "PUBLIC holds nothing"). Run **before any `v_ace_*` view exists**: at this point it covers the recovery tables, which the migration account owns. Run after Section A's views exist it fails with `permission denied for table v_ace_<name>`, because `ace_view_owner` owns them ([E2] run 3); that is why the Section B file omits it and why this statement must stay first. A REVOKE only; no `GRANT ... ON ALL TABLES` (DG-L11).
2. Create the three helpers (SPEC-002). They are owned by the migration account.
3. `REVOKE ALL ON FUNCTION ${recoverySchema}.ace_to_date(text), ${recoverySchema}.ace_to_boolean(text), ${recoverySchema}.ace_mask_value(text) FROM PUBLIC, ace_view_owner`.
4. `GRANT EXECUTE ON FUNCTION` the same three `TO recovery_svc`. PostgreSQL checks EXECUTE on a function called inside a view against the **caller**, not the view owner ([E2]), so `recovery_svc` needs it and `ace_view_owner` does not (BR2; ASM-003).
5. `GRANT USAGE ON SCHEMA ${recoverySchema} TO recovery_svc`.
6. `GRANT USAGE, CREATE ON SCHEMA ${recoverySchema} TO ace_view_owner`. Transient. The owner change needs CREATE on the schema for the new owner; USAGE keeps the step identical in every environment ([E2]; DG-L12). Both are revoked at step 11.
7. Create the 16 views (SPEC-003), as the migration account. USAGE on `public` resolves the source names; no table privilege is needed and none is held ([E2] run 3).
8. For each view: `REVOKE ALL ON ${recoverySchema}.<view> FROM PUBLIC, recovery_svc, ace_view_owner`. Removes default-privilege grants (X8: [E2] showed a new view getting `recovery_svc=arwd` from `20-grants.sql.inc` lines 56–57).
9. For each view: `GRANT SELECT ON ${recoverySchema}.<view> TO recovery_svc`. **Before** the owner change, while the migration account still owns the view: after `ALTER VIEW ... OWNER TO ace_view_owner`, a member with `INHERIT FALSE` is refused (`permission denied for table <view>`, [E2] run 3). The grant stays valid after the owner change; PostgreSQL rewrites its grantor.
10. For each view: `ALTER VIEW ${recoverySchema}.<view> OWNER TO ace_view_owner`. Allowed because the migration account may SET ROLE to the owner (P4(b)); no SELECT on any `public` table is used.
11. `REVOKE USAGE, CREATE ON SCHEMA ${recoverySchema} FROM ace_view_owner`. After this `ace_view_owner` holds neither USAGE nor CREATE on `recovery`, and the views still work: a view's table access needs no schema right of the owner ([E2]; ASM-002 verified).

**Not in the recovery migration (DG-L22).** [S1] §12 lists `GRANT USAGE ON SCHEMA public TO ace_view_owner` and `GRANT SELECT ON public.<21 tables> TO ace_view_owner`, "run as the ACE schema owner". These statements act on ACE's schema and are carried by the ACE DBA's grant script, not by a recovery migration: [S9] §8.2 puts "The SELECT grant for the recovery role on the listed tables" in RWB-ACE-001 and gives E1-069 only "the grant to the recovery service identity and the revoke from PUBLIC"; [S4] flow step 5, §10 and §12 step 4 have the ACE DBA grant the view-owner role on the listed tables; the [T3] lint admits `public.` only inside `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*` (SEAM-E044-01, orchestrator triage). [E2] showed that without the Tier 1 grant the views are created but every read as `recovery_svc` fails with `permission denied for table account` (REVIEW-103), so the grant is precondition P4(d), checked by SPEC-009, and supplied locally by SPEC-015.

### SPEC-008: checks, session roles and connection input

| # | Check | Session role | Failure text |
|---|---|---|---|
| 1 | **Compile and read.** Every `v_ace_*` view in `recovery` returns from `SELECT * FROM ${recoverySchema}.<view> LIMIT 1` without error. The view count is exact: 16 when only the Section A file is present, 30 when the Section B file is present. Running as `recovery_svc` also proves the SELECT and EXECUTE grants. | `recovery_svc` | "`<view>` does not compile: `<database error>`" ([S1] §5 X1, §14) |
| 2 | **Constraints.** No `pg_constraint` row in `recovery` has `confrelid` outside `recovery`, and no constrained column's type lives outside `recovery` or `pg_catalog`. | migration account | "`<conname>` references `<schema>.<table>`; no constraint in recovery may reference another schema" |
| 3 | **Dictionary.** Each `v_ace_*` view has one `sys_objects` row; each of its columns has exactly one `sys_fields` row; every such row has a non-null `is_personal` (SPEC-019). | migration account | "`<view>.<column>` has no data dictionary entry" |
| 4 | **Privileges.** `recovery_svc` has no USAGE on `public`, no privilege on any `public` relation, and no INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES or TRIGGER on any `v_ace_*` view. Checked with `has_*_privilege` from the migration account, which can resolve `public` names; run in a `recovery_svc` session the same calls raise `permission denied for schema public` ([E2] run 3, REVIEW-120). The direct-read refusal (`permission denied for schema public`, SQLSTATE 42501) stays in the `recovery_svc` session. | migration account | "recovery_svc holds `<priv>` on `<object>`; the recovery role reads the views only" |
| 5 | **Migration-account rights (D-RUN-14).** On the same container: `has_schema_privilege('rwb_migrator','public','USAGE')` is true and `'CREATE'` false; the count of `public` relations on which `has_table_privilege('rwb_migrator', oid, 'SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER')` is true is 0; `pg_auth_members` holds one row for `ace_view_owner`/`rwb_migrator` with `inherit_option = false`, `set_option = true`, `admin_option = false`; `rolsuper`, `rolcreaterole`, `rolcreatedb` and `rolbypassrls` are false. This is the D-RUN-14 precondition [T3] v14-7 T-044-17 owns; E1-069 re-asserts it and does not weaken it. | superuser (catalog) | "the migration account holds more than the D-RUN-14 rights; RWB-E1-044 T-044-17 owns this assertion" |

- **Failing fixture per check** ([S1] §13 step 4), Testcontainers only, added after migration on a throwaway container and never in the migration folder: an unreadable view (a view over a dropped synthetic column), the FK `fk_case_account_account_key` to `public.account`, a column `legacy_bucket` on a copy of `v_ace_account` with no `sys_fields` row, and `GRANT INSERT ON ${recoverySchema}.v_ace_account TO recovery_svc`.
- **Run scope.** The Testcontainers run executes checks 1–5 and the fixtures. **External mode** (`RWB_CONFORMANCE_TARGET=external`) executes checks 1–4 only: read-only, no fixture, no write, no check 5 (the migration account's rights are the environment owner's, and T-044-17 owns them locally). SPEC-009's assertions are the Testcontainers run; in external mode check 4 reports the same catalog facts (REVIEW-121(a)).
- **Connection input (ASM-004).** When `RWB_CONFORMANCE_TARGET=external` is set, the test connects to `RWB_DB_URL` as `RWB_DB_USER` with `RECOVERY_SVC_PASSWORD` (check 1) and as `RWB_MIGRATOR_USER` with `RWB_MIGRATOR_PASSWORD` (checks 2–4), the names `application.yaml` already uses, supplied as pipeline variables. Otherwise it starts the Testcontainers database of SPEC-015. No credential is written in code.

### SPEC-009: access assertions (AC2)

All assertions below are the Testcontainers run (ASM-004); external mode runs SPEC-008 checks 1–4 only.

- **As `recovery_svc` (direct-read assertions):** `SELECT` from `v_ace_account` returns the synthetic row inserted by the test as superuser; `SELECT` from `public.account` fails with SQLSTATE 42501 and message `permission denied for schema public` ([E2] exact text); `INSERT`, `UPDATE`, `DELETE` on `v_ace_account` each fail with 42501 (`permission denied for view v_ace_account`, [E2]).
- **As the migration account (catalog assertions, SPEC-008 check 4):** `has_schema_privilege('recovery_svc','public','USAGE')`, `has_table_privilege('recovery_svc','public.account','SELECT')` and `has_table_privilege('recovery_svc','recovery.v_ace_account','INSERT')` are false. In a `recovery_svc` session the same `has_table_privilege` call raises 42501 instead of returning false, so it is not run there ([E2] run 3, REVIEW-120).
- **`ace_view_owner`:** owns exactly the 16 (then 30) views; holds SELECT on each of the 21 Tier 1 tables (then also the 14 Tier 2 tables) named in [S1] §11/§12; holds no INSERT, UPDATE or DELETE on any of them; holds no USAGE or CREATE on `recovery`, no EXECUTE on the three helpers, and no privilege on any other `recovery` relation (BR2).
- **`rwb_no_grant`:** a test role created by the fixture with LOGIN and USAGE on `recovery` only. `SELECT` on `v_ace_account` fails with 42501 (`permission denied for view v_ace_account`, [E2]) and `has_table_privilege` is false.
- The message assertion for `public.account` holds wherever P4(d) is in place; a mismatch on the text alone is reported as P4(d) not met (DG-L13).

### SPEC-010: dictionary assertions (AC5, AC6)

| Measure | Asserted value | Alternative in sources | Why this value |
|---|---|---|---|
| `v_data_dictionary` total objects / fields | **123 / 1,382** | 122 / 1,366 in [S1] AC5 and TC-05, and in [S16] header ("1366 fields in 122 entities"); 123 / 1,379 in [S3] Physical Schema v6 | The RWB-E1-001 migration seeds [S3] Physical Schema v6 plus three provisional field rows DF-REF-300..302 for the columns RWB-E1-042 adds to `parameter_value` ([T2] Revision 4 SPEC-006; ASM-E1001-17), so 1,379 + 3 = 1,382. [S17] D-RCV-36 row 18 makes v6 replace v5 and A.7 states v6 holds 93 tables; D-RCV-36 is tier 1 under the RUN-BRIEF precedence, above story files v7. DG-L05. |
| Table fields | **1,078**, of which **49** on the four extension tables | 1,062 / 49 in [S1] AC5; 1,075 / 49 in [S3] | Same reason: 1,075 + the three `parameter_value` columns = 1,078 ([T2] Revision 4 SPEC-006, ASM-E1001-17). DG-L05. |
| `v_ace_*` objects / fields | **30 / 304**, Section A **177** (DF-ACE-001..177), Section B **127** (DF-ACE-178..304); per-view ranges as [S1] §11 | none | All sources agree. The three provisional rows are DF-REF, not DF-ACE, so the view counts do not move. |
| Extension fields | **49**, DF-EXT-001..049 | none | [S1] AC7, §11. |

- Each view has a one-to-one match between catalog columns and `sys_fields` rows (check 3).
- AC6: `v_data_dictionary` for entity `v_ace_account`, field `days_past_due` returns field ID `DF-ACE-018`, data type `NUMBER`, physical type `integer`, source system `ACE`, source field `public.account.delay_days`, data product `DP01`, refresh cycle `DAILY` ([S3] line 5843 and line 3626, per round-1 review). A synthetic ACE account `ACC0000017` with `delay_days` 95 reads back as `days_past_due` 95 through the view.
- If the RWB-E1-001 migration ships other totals after its own gate, this test asserts what that file seeds and the plan records the change; the AC5 view counts (30/304/177/127/49) never change.

### SPEC-011: extension-table assertions (AC7, BR7)

| Table | Columns | Primary key | Business columns | Other checks |
|---|---|---|---|---|
| `party_ext` | 12 | `person_key varchar(255)` | `vulnerable`, `deceased_override`, `bankruptcy`, `fraud_flag` | — |
| `contact_point_ext` | 14 | `contact_key varchar(255)` | `contact_type`, `consent_given`, `consent_at`, `verified_at`, `failed_count`, `source` | `ck_contact_point_ext_type` allows PHONE, EMAIL, ADDRESS |
| `account_ext` | 9 | `account_key varchar(255)` | `dispute_open` | — |
| `valuation_ext` | 14 | `valuation_key varchar(255)` | `accepted`, `accepted_at`, `accepted_by`, `valuer_partner_id`, `stale_flag`, `age_days` | — |

- **BR7 standard record columns** on each of the four tables, with type, nullability and default: `is_active boolean NOT NULL DEFAULT true`, `state varchar(40)`, `version integer NOT NULL DEFAULT 1`, `created_at timestamptz NOT NULL DEFAULT now()`, `created_by uuid`, `updated_at timestamptz NOT NULL DEFAULT now()`, `updated_by uuid` ([S3] lines 2087–2150; [T2] line 38 names the same seven).
- The exact column set per table equals the table above (key + business columns + seven standard columns); 49 columns in all, matched by 49 `sys_fields` rows DF-EXT-001..049.
- No business column has the same name as a column of the ACE table it extends (BR7 "never a copy"), checked against the column list of the corresponding `v_ace_*` view (`v_ace_customer`, `v_ace_contact`, `v_ace_account`, `v_ace_valuation`).
- No FK on the four tables references schema `public`.
- A second `party_ext` row for synthetic `P0000123` fails with 23505 on `party_ext_pkey`; exactly one row remains.

### SPEC-012: the BND-6 rule

**Detection.** The rule scans recovery main sources (`src/main/java/th/co/scb/ace/demo/recovery/**`), each file whole with comments removed, so it catches:
- (a) `public.<ident>` with optional spaces and quotes (`"public"."account"`, `public . account`) in string literals, text blocks and concatenations spanning lines;
- (b) JPA `@Table`, `@SecondaryTable`, `@JoinTable` with `schema = "public"`;
- (c) SQL in `@Query`, `@NamedNativeQuery`, `@NamedQuery` and string arguments to `JdbcTemplate` or `JdbcClient`;
- (d) an unqualified ACE source-table name after `FROM`, `JOIN`, `UPDATE`, `INTO` or `TABLE` inside a string literal, text block or concatenation. The keyword matches case-insensitively; the table identifier matches **case-sensitively in lower case**, or quoted (`"account"`). So JPQL entity names such as `select p from Payment p join p.account a` do not match (ASM-013). The ACE source-table set is derived at test time from the `public.<name>` qualifiers in the E1-069 migration files; recovery tables, derived from the `CREATE TABLE` statements of the recovery migrations, are excluded (today only `hearing` is in both, round-1 review).

**Allowed names.** All 30 names in `sourceViews` (SPEC-013), read from the module map, never written in the test.

**Not flagged (ASM-013).** Identifiers qualified with `information_schema.` or `pg_catalog.`, and the literal `'public'` used as a catalog filter value. This keeps `PlatformInfoController` green.

**Failure message.** [S1] §14: "Boundary rule BND-6 broken: `<SimpleClassName>` reads public.`<table>`. Read recovery.`<view>` instead." `<view>` comes from a table-to-view map derived at test time from the view bodies in the E1-069 migration files: the view whose top-level `FROM` names the table, otherwise the views that `JOIN` it, joined with " or ". Examples from [S2]: `phone`, `email`, `address` → `v_ace_contact`; `bot_holiday` → `v_ace_holiday`; `bucket_log_snapshot` → `v_ace_bucket_log`; `pod_receipt` → `v_ace_pod`. For a table no view reads, the message ends "Read a recovery.v_ace_* view instead." (**derived**, not in [S1] §14; REVIEW-115).

**Fixtures** (test sources, package `th.co.scb.ace.demo.recovery.dataengine.internal` from the [T1] module skeleton, ASM-007): `AccountReader` with `select delay_days from public.account` fails naming `AccountReader` and `public.account`; the same class reading `recovery.v_ace_account` passes; a native `@Query` `select delay_days from public.account` fails; unqualified `select delay_days from account` fails; `FROM "account"` fails; JPQL `select p from Payment p join p.account a` passes; a copy of the `PlatformInfoController` `information_schema` query filtered on `'public'` passes; `@Table(schema = "public", name = "account")` fails.

**Where it runs.** The default `test` task.

### SPEC-013: `sourceViews`

```yaml
sourceViews:
  sectionA: [v_ace_account, v_ace_payment, v_ace_customer, v_ace_contact, v_ace_ca_relation,
             v_ace_aa_relation, v_ace_collateral, v_ace_asset, v_ace_efs_action, v_ace_efs_action_code,
             v_ace_efs_assignment, v_ace_bucket_log, v_ace_product, v_ace_branch, v_ace_holiday, v_ace_plan]
  sectionB: [v_ace_batch_status, v_ace_valuation, v_ace_collateral_detail, v_ace_npa_asset, v_ace_npa_sale,
             v_ace_lawsuit, v_ace_hearing, v_ace_pod, v_ace_write_off, v_ace_score, v_ace_party_product,
             v_ace_credit_decision, v_ace_esign, v_ace_iam_group]
```

All 30 names are added at once ([S1] §4 step 5 governs; DG-L28), in [S1] §11 / [S2] order. A reader in the [T1] boundary tooling package validates the key (the [T1] loader keeps carrying it as an opaque value) and fails, naming the file and field path, when: either list is missing; a name breaks `^v_ace_[a-z0-9_]+$`; a name repeats across both lists; `sectionA` does not hold 16 names or `sectionB` 14.

**Rules against the migration folder** (REVIEW-106), so the build is green both between the two merges and after:
1. Every `v_ace_*` view any recovery migration creates is listed in `sourceViews`.
2. The set created by the Section A file equals `sectionA`.
3. If the Section B file is present, the set it creates equals `sectionB`; if it is absent, no `sectionB` name is created by any file.
4. BND-6 allows all 30 names in both states. A class that reads a Section B view before it exists fails at run time, and BR9 keeps such features behind their flags.

Changes to the key go through the data architect and the recovery tech lead ([S1] §10, §19).

### SPEC-014: lint seams in the [T3] lint

- **SEAM-E044-01 (`public` qualifier).** `isAllowedQualifier(statement, qualifier)` additionally returns true for `public` **only** when the statement is `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_<name>` (orchestrator triage; [T3] SPEC-016). It never applies to L-FK-OUTSIDE, GRANT, REVOKE, ALTER or any other statement. E1-069 replaces the [T3] T-044-02 seam-marker fixture with its own: the view statement passes; `SELECT a.id FROM public.t a`, `GRANT SELECT ON public.t TO x`, `CREATE VIEW ${recoverySchema}.v_other AS SELECT ... FROM public.t` and `REFERENCES public.t(id)` fail.
- **SEAM-E044-02 (L-GRANT, L-KEY-DUP).** Scoped to files whose key is `rwb_e1_069`:
  - L-KEY-DUP admits exactly two non-fix files for the key, named `…__rwb_e1_069_ace_source_views.sql` and `…__rwb_e1_069_ace_tier2_views.sql`. A third file, or another name, fails.
  - L-GRANT admits `GRANT` and `REVOKE` whose object is `SCHEMA ${recoverySchema}`, `${recoverySchema}.<object>`, `FUNCTION ${recoverySchema}.<fn>(…)` or (REVOKE only) `ALL TABLES IN SCHEMA ${recoverySchema}`, and whose grantees are only `recovery_svc`, `ace_view_owner` or PUBLIC. A grant on `public`, `GRANT ... ON ALL TABLES`, any other grantee, or a GRANT/REVOKE in a file of any other key fails.
  - **Lint impact of D-RUN-14 (REVIEW-117).** None of the two files contains `SET ROLE` or a role-membership grant: the migration account's two rights come from [T3] v14-7's local init (P4(e)), and E1-069 restates neither. `GRANT ... TO rwb_migrator` in a `rwb_e1_069` file fails L-GRANT (fixture), `ALTER VIEW ... OWNER TO ace_view_owner` is not a GRANT and is admitted, and the only `ON ALL TABLES` statement is the REVOKE of SPEC-004 step 1 (admitted, REVOKE only). SEAM-E044-01 is unchanged.
  - The exception data (key, the two file-name suffixes, grantee list) is held in one test resource, `backend/src/test/resources/db/recovery-migration-lint-exceptions.yaml`, read by the rules, not written in rule code.
- Fixtures: another key with `GRANT SELECT ON ${recoverySchema}.t TO recovery_svc` fails; key `rwb_e1_069` with a third file fails; `GRANT ... TO rwb_migrator` in a `rwb_e1_069` file fails.

### SPEC-015: local mode switch and stand-ins

**(a) Who owns which switch** ([T2] Revision 4 SPEC-010; REVIEW-118(1)–(3)). RWB-E1-001 owns **S1**: `RWB_LOAD_REFERENCE_SCHEMA` defaults to `false` in `.env.example`, `docker-compose.yml` (`${RWB_LOAD_REFERENCE_SCHEMA:-false}`) and the `10-load-ace-database.sh` fallback, effective at its merge. E1-069 does not flip S1 again; it decides whether reference mode survives and keeps it as an untested opt-in (`rwb.flyway.enabled=false`), as [T2] allows. RWB-E1-001 owns **S3**: `rwb.flyway.enabled: ${RWB_FLYWAY_ENABLED:true}` in `application.yaml`; E1-069 relies on `true` and changes nothing there. E1-069 owns **S2** `RWB_LOAD_REFERENCE_VIEWS` (new in [T2] Revision 4, default `true`, views-only stand-in that runs the Physical Schema v6 view section at init): this story flips the default to `false`, deletes the branch from `10-load-ace-database.sh`, and states the consequences. The flip ships **in the same merge as the Section A file**: until both land, S2 is the only local source of the 30 views; from that merge on, init creates none, so Flyway is the only source and the 16-view assertions of SPEC-008/SPEC-017 are unambiguous:
- the 30 views come only from the two E1-069 files, so the schema is empty at init and Flyway writes **no** version-`0` baseline row ([T2] ASM-E1001-18; DG-L30);
- `RWB_ACE_TIER2_PROBE` stays `true`;
- the README "Local versus target" row becomes "Flyway (E1-042, E1-043, E1-001, E1-069 migrations)" with no view stand-in, and the migration-folder README names RWB-E1-069 (not RWB-E1-001) as the owner of the view files (DG-L18);
- developers run `./scripts/dev.ps1 reset` once, because init scripts run only on an empty volume.

**(b) Flyway-mode init** (`RWB_LOAD_REFERENCE_SCHEMA=false`, `RWB_LOAD_REFERENCE_VIEWS=false`), standing in for the ACE DBA (P4) and for the RWB-ACE-001 grant step:
- keep: `ALTER SCHEMA recovery OWNER TO rwb_migrator` (satisfies P4(c)); `REVOKE ALL ON SCHEMA public FROM PUBLIC`; `GRANT USAGE ON SCHEMA public TO ace_view_owner`; the `recovery_svc` and sequence grants and default privileges; `GRANT USAGE, CREATE ON SCHEMA recovery TO ace_view_owner` (line 7) — each E1-069 file revokes both at its last step (SPEC-004 step 11), so the end state is BR2's;
- **D-RUN-14 rights are not repeated here.** `GRANT USAGE ON SCHEMA public TO rwb_migrator` and `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE` are delivered by [T3] v14-7 SPEC-017 in `20-grants.sql.inc`, after the `REVOKE ALL ON SCHEMA public FROM PUBLIC` line. E1-069 relies on them (P4(a)–(b)); if either is missing, the Section A file fails at `CREATE VIEW` or `ALTER VIEW` and SPEC-008 check 5 names it;
- `GRANT SELECT ON public.<each of the 21 Tier 1 tables, by name> TO ace_view_owner` (P4(d); [S1] §11);
- when `RWB_ACE_TIER2_PROBE=true`: `GRANT SELECT ON public.<each of the 14 probe tables, by name> TO ace_view_owner` (stand-in for [S4] flow step 5; REVIEW-103);
- default privileges for functions name `recovery_svc` only: today `20-grants.sql.inc` line 61 also names `ace_view_owner`, which would give it EXECUTE on every later function the migration account creates and breach BR2; the helpers of SPEC-004 step 3 are covered either way;
- not in this mode: `GRANT SELECT ON ALL TABLES IN SCHEMA public` (line 12; the named grants replace it), any grant option on a `public` table to `rwb_migrator`, any other role membership for `rwb_migrator`, and any `GRANT` in a recovery migration.

Reference mode keeps the current statements; its breadth is a local deviation (ASM-008). Where the branch lives (a psql variable in `20-grants.sql.inc` or the step of `10-load-ace-database.sh` that now owns S2) is the plan's choice.

**(c) Integration tests in Flyway mode.**
- `RecoveryDatabaseIT` moves to S1=`false` with the probe on and, after this story, S2=`false`; every assertion is kept: 30 views and 0 public tables visible to the service, 42501 on `public.account`, views read-only and owned by `ace_view_owner`, the append-only decision log, the Temporal/recovery identity separation. Its version-`0` baseline-row assertion moves with the S2 stage: on the empty schema there is no baseline row ([T2] Revision 4 ASM-E1001-18 names this outcome). It is replaced by the per-file history assertion of SPEC-017 (one success row for each applied file, no `version = '0'` row), which is stronger, so no coverage is lost. DG-L30 records the one wording difference from [T2] ("no assertion removed").
- `ViewConformanceTest` uses the same container definition.
- `RecoverySchemaMigrationIT` ([T2]) keeps its assertions "no `v_ace_*` view and no function `ace_to_date` after the RWB-E1-001 migration"; E1-069 makes it evaluate them at that file's version (Flyway built through `RecoveryFlywayTestSupport` with `target` set to it, SPEC-018), because a full migration now creates both (ASM-014).

### SPEC-017: Flyway history and re-run (AC1, AC3)

Versions are read at test time from the file names in the migration folder (D-RUN-07); no number is written in the test.
- After migrating to the Section A version: `flyway_schema_history_recovery` holds exactly one `success = true` row for the RWB-E1-001 file and one for the Section A file, Section A after the RWB-E1-001 file by `installed_rank`, and **no `version = '0'` row** (the schema is empty at init once [T2]'s S2 stand-in is off, [T2] Revision 4 ASM-E1001-18); 16 `v_ace_*` views exist.
- Re-run: a second `migrate()` reports `migrationsExecuted = 0`, the history is unchanged, and `recovery` still holds 16 `v_ace_*` views.
- After the full migration: one `success = true` row for the Section B file after the Section A row; 30 views, 30 of 30 return a row as `recovery_svc` (check 1); after Section B, `ace_view_owner` holds no USAGE or CREATE on `recovery`, owns exactly 30 views, and holds no EXECUTE on the helpers (REVIEW-102).

### SPEC-018: X2 negative test (AC3)

- **Mechanism (REVIEW-121(c), -122).** `RecoveryFlywayTestSupport`, in test sources in the same package as the package-private `RecoveryFlywayConfig` (so it can import it), is a `BeanDefinitionRegistryPostProcessor` that clears `initMethodName` on the `recoveryFlyway` bean definition before instantiation. The test context therefore starts without running `migrate()`, and the test gets the **real** `Flyway` bean with the bean's own configuration; it then calls `Flyway.configure().configuration(bean.getConfiguration()).target(...)`. No setting is copied or restated, and `RecoveryFlywayConfig` stays unchanged. This is needed because a failure inside the bean's `initMethod` would stop the context. The class is **outside the unit coverage bundle** (IT-only): its only callers are the `recovery-it` tests T-E1-069-13 and T-E1-069-16, and both coverage tasks take execution data from the `test` task only (`backend/build.gradle.kts` lines 130-160; [T1] v4 SPEC-020(c)), so no unit-coverage target is claimed for it.
- **Main case.** A fresh Flyway-mode container with the probe applied and its grants, then `DROP TABLE public.valuation` as superuser (no object depends on it). Migrate to the Section A version, then migrate fully. Assert: a `FlywayException` whose cause has SQLSTATE 42P01 and whose message contains `public.valuation` and `does not exist` (PostgreSQL quotes the name, `relation "public.valuation" does not exist`, [E2]; [S1] AC3 writes it unquoted, DG-L26); 16 `v_ace_*` views, none of the 14 Section B names; no `success = true` row for the Section B file; the 16 Section A views still return rows as `recovery_svc`.
- **Probe-off case.** `RWB_ACE_TIER2_PROBE=false`: the same steps fail first on B1 with `relation "public.ace_batch_run" does not exist`, with the same end-state assertions.
- "Features stay behind their flags" ([S1] AC3) has no feature yet; the consuming stories own their flags (Out of scope).

### SPEC-019: data protection of the published interface

**Classification.** The classification of record is [S16] Data Classification and Personal Data Inventory v4, Fields tab: of the 304 DF-ACE fields, 250 are personal (232 Confidential, 6 Internal staff identifiers, 12 Restricted) and 54 are Internal non-personal. The 12 Restricted fields: DF-ACE-003 `v_ace_account.account_name`, -041 `v_ace_account.special_memo`, -053 `v_ace_payment.comments`, -057 `v_ace_customer.first_name`, -058 `last_name`, -059 `date_of_birth`, -060 `deceased_date`, -061 `deceased_flag`, -066 `spouse_name`, -073 `id_no_masked`, -078 `v_ace_contact.contact_value`, -116 `v_ace_efs_action.comments`. [S3] `sys_fields.is_personal` flags only 9 DF-ACE fields as personal. [T2] Revision 4 seeds the protective union of [S3] and [S16]: `true` for 526 fields in the whole dictionary (ASM-E1001-14; its own Blocker = Yes gap GAP-E1001-18), and every one of the 250 personal DF-ACE fields is among them, including all nine [S3] flags (057, 058, 059, 066, 072, 073, 074, 078, 079); the other 54 DF-ACE fields stay `false`. The residual mismatch between [S3]'s 9 and [S16]'s 250 is DG-L24 (owner: data architect with RWB-E1-001; OI-069-J).

**Controls and owners** ([S9] §3.3 and §12 R5: "the grant plus E1-037 plus the audit log"):
| Control | Where | Owner |
|---|---|---|
| Read only through the views; `recovery_svc` SELECT only | SPEC-004, -006, -009 | this story |
| Identity number never in clear: `v_ace_customer` exposes `id_no_masked` (`ace_mask_value`) and `id_no_last4` only, never `identification_number` | [S2] lines 190–191; [S1] §17 | this story (verbatim view) |
| Phone, email and address in clear in `v_ace_contact.contact_value`, masked copy in `contact_value_masked` | [S9] §3.3; [S2] lines 198–234 | this story exposes; display masking RWB-E1-037 |
| Display masking at the API | [S1] §19; [S16] Key tab | RWB-E1-037 |
| Every read of a personal field logged (PII access log) | [S9] §3.3; [S16] Key tab; NFR-042 | RWB-E1-016 |
| Definer rights: views run with `ace_view_owner`'s table privileges, so any ACE row-level security must be applied inside the view | [S2] lines 20–21 | recorded for the security review (OI-069-H) |

**Tests (part of `ViewConformanceTest`).** No `v_ace_*` view has `security_invoker=true` in `reloptions`; `v_ace_customer` has no column `identification_number` or `id_no`; for a synthetic identification value `X000000005678` the view returns `id_no_masked` = `*********5678` and `id_no_last4` = `5678`; check 3 asserts `is_personal` is non-null on all 304 view rows, `true` for the 250 [S16]-personal DF-ACE fields (which include the nine [S3] flags 057, 058, 059, 066, 072, 073, 074, 078, 079 and all 12 Restricted fields) and `false` for the 54 [S16] non-personal fields. The whole-dictionary count of 526 is [T2]'s assertion (TC-E1-001-14), not this story's. All test data is synthetic ([S1] §17; NFR-045).

### SPEC-020: helper-function tests (BR6)

Run on PostgreSQL 16 (`postgres:16.16-alpine`) after the Section A file:
- **`ace_to_date`, literal calls:** every row of the SPEC-002 table, asserting the exact result (date or NULL) and that no call raises.
- **Through a view:** synthetic `public.payment` rows with `pay_date` `2026-02-28`, `2026-02-30`, `20261345`, `31/02/2026`, `garbage` and NULL; `SELECT * FROM ${recoverySchema}.v_ace_payment` as `recovery_svc` succeeds; `payment_date` is 2026-02-28 for the first row and NULL for the other five ([S2] line 152 is the only `ace_to_date` call).
- **DateStyle:** under `SET DateStyle = 'SQL, DMY'` and `'German'`, `20260228`, `28/02/2026` and `2026-02-28` still give 2026-02-28.
- **`ace_to_boolean`:** `Y`, `' y '`, `yes`, `TRUE`, `1` → true; `N`, `no`, `False`, `0` → false; `''`, NULL, `maybe`, `2` → NULL ([E2]).
- **`ace_mask_value`:** `0000005678` → `******5678`; `abc` → `***`; `a@x.co` → `a***@x.co`; `''` and NULL → NULL ([E2]).
- `has_function_privilege` is true for `recovery_svc` and false for `ace_view_owner` and `rwb_no_grant` on all three.

## Data protection summary

See SPEC-019. The story stores no personal data and writes none. It publishes a read interface that carries 250 personal fields, 12 of them Restricted, to one service identity, under the control set of [S9] §12 R5. No personal data appears in this spec, its tests or its fixtures: `ACC0000017`, `P0000123` and `X000000005678` are synthetic ([S1] §17; RUN-BRIEF rule 7).

## Out of scope

From [S1] §19 and D-RUN-08 seams:
- Masking at the API and display masking: RWB-E1-037.
- The PII access log for reads of personal fields: RWB-E1-016.
- The rest of the module map (module entries, rules BND-1..5): RWB-TE-001.
- The Tier 2 tables, the 12 new ACE columns, the ACE-side grants and the PUBLIC revoke on `public`: RWB-ACE-001 and the ACE DBA (P4(d)).
- The feature flags of features that read a Section B view: the consuming stories.
- Any change to the frozen 30-view list or a view body: the data architect and the recovery tech lead ([S1] §19). The `ace_to_date` body is the one deviation, recorded as OI-069-G.
- DML grants for `recovery_svc` on Workbench tables in SIT and above ([S1] BR3 gives them to the RWB-E1-001 migration): DG-L25, OI-069-I.
- Wiring `recoveryCoverageVerification` into CI: RWB-TE-003/TE-011 ([T1] SPEC-020).
- The `is_personal` ruling for the 26 PS-v6-only fields and the three provisional field IDs DF-REF-300..302: RWB-E1-001's Blocker = Yes gaps GAP-E1001-17 and GAP-E1001-18 (ASM-E1001-13, -14, -17). This story asserts what that file seeds and does not rule on them.

## Field-level behavior matrix

No user-entered field. The read interface is the views; columns are cited, not copied ([S1] §11; [S2] view bodies).

| Object | Source of each column | Editable | Constraint |
|---|---|---|---|
| 16 Section A views (177 fields, DF-ACE-001..177) | [S2] A1–A16 over the 21 Tier 1 tables | No (SELECT only) | No PK or FK. Text dates through `ace_to_date`, Y/N through `ace_to_boolean`, both NULL rather than error (SPEC-002, -020). `v_ace_customer` exposes the identity number only as `id_no_masked` and `id_no_last4`; its other personal fields are in clear (SPEC-019). |
| 14 Section B views (127 fields, DF-ACE-178..304) | [S2] B1–B14 over the 14 Tier 2 tables | No | Same rules. Created only after RWB-ACE-001 (BR9). |
| `v_ace_account.days_past_due` | `public.account.delay_days` ([S2] A1; DF-ACE-018) | No | integer |
| 4 extension tables (49 fields, DF-EXT-001..049) | The RWB-E1-001 migration; shape per SPEC-011 | Written by later stories | 1:1 on the ACE key, `varchar(255)`, no FK to `public` |
| `sourceViews` | [S1] §11 | Data architect and recovery tech lead | 16 + 14 names; SPEC-013 rules |

## Status-transition matrix

No case status changes ([S1] §9). Schema states:

| Source state | Condition | Target state |
|---|---|---|
| `recovery` at the RWB-E1-001 file's version | Section A file applied | 3 helpers, 16 views, Section A grants, one success row |
| `recovery` at the RWB-E1-001 file's version | Section A file fails (X1) | Transaction rolled back; no view from the run; the earlier objects unchanged |
| Section A applied | Section B file applied after RWB-ACE-001 | 30 views, one more success row |
| Section A applied | Section B file applied without a Tier 2 table (X2) | Rolled back; 16 views unchanged; no Section B success row |
| Any applied version | `migrate` again | `migrationsExecuted = 0`; nothing changes |

## Exceptional-case behavior

| ID | Trigger | Behaviour | Check | SPEC |
|---|---|---|---|---|
| X1 | A Section A view does not compile | Migration rolls back; log names the view and column | Check 1; fixture | 003, 008 |
| X2 | Section B applied without `public.valuation` | Fails with `relation "public.valuation" does not exist`; 16 views unchanged | SPEC-018 | 005, 006, 018 |
| X3 | A recovery constraint references `public` | Check 2 fails; merge blocked | Fixture FK | 008 |
| X4 | A view column has no `sys_fields` row | Check 3 fails naming `v_ace_account.legacy_bucket` | Fixture | 008, 010 |
| X5 | `recovery_svc` holds a `public` privilege or a write on a view | Check 4 fails naming it | Fixture grant | 004, 008, 009 |
| X6 | A recovery class names a `public` table | BND-6 fails the build | Fixtures | 012 |
| X7 | Second extension row for one ACE key | 23505 on `party_ext_pkey`; first row kept | IT | 011 |
| X8 (derived) | Default privilege grants DML on a new view | Removed by the per-view REVOKE before the owner change ([E2]) | Check 4 | 004 |
| X9 (derived) | Dirty ACE text date (impossible date) | `ace_to_date` returns NULL; the read succeeds | SPEC-020 | 002, 020 |
| X10 (derived) | Missing ACE-side grant (P4(d)) | Views are created; reads as `recovery_svc` fail with `permission denied for table <t>` ([E2]) | Check 1 | 004, 015 |
| X11 (derived) | `public.` or GRANT in another story's migration | Lint fails | SPEC-014 fixtures | 014 |
| X12 (derived) | The migration account holds more than D-RUN-14 (an ACE table privilege, a `public` write, an inheriting membership) | Check 5 fails; [T3] T-044-17 also fails | Check 5 | 008 |

## API change assessment

| Item | Value |
|---|---|
| Impact type | `NO_API_CHANGE` ([S1] §12) |
| Contract delta | None. `contracts/backend-apis.json` records the non-HTTP contracts. |
| Backward compatibility | `GET /api/recovery/v1/platform/info` unchanged; `visiblePublicTables` stays 0. |

## Frontend Specification

No frontend change. UI In Scope = NO ([S1] §15); no API delta. Per-screen design documentation is N/A.

## Requirement-to-SPEC Logic Coverage

Each AC is split into its clauses (REVIEW-109). Coverage Type is `DIRECT` or `INHERITED_EXISTING_BEHAVIOR`; Status is `COVERED` or `BLOCKED`.

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| AC1.1 | Extension tables present | 007, 011 | INHERITED_EXISTING_BEHAVIOR | Created by the RWB-E1-001 migration, verified here (DG-L01); TC-07 | COVERED |
| AC1.2 | 16 Section A views created, 16 of 16 compile | 001, 003, 008 | DIRECT | Check 1; TC-01 | COVERED |
| AC1.3 | One-row select from each of 16 returns | 008 | DIRECT | Check 1 as `recovery_svc`; TC-01 | COVERED |
| AC1.4 | No other `v_ace_*` view | 008, 013 | DIRECT | Exact count; SPEC-013 rule 2; TC-01 | COVERED |
| AC1.5 | One history row for Section A after the RWB-E1-001 file | 017 | DIRECT | TC-01 | COVERED |
| AC1.6 | Re-run: already applied, still 16 | 017 | DIRECT | TC-01 | COVERED |
| AC2.1 | `recovery_svc` selects rows from `v_ace_account` | 004, 009 | DIRECT | TC-02 | COVERED |
| AC2.2 | `public.account` → 42501 "permission denied for schema public" | 009, 015 | DIRECT | Text depends on P4(d) (DG-L13); TC-02 | COVERED |
| AC2.3 | Insert, update, delete on the view → 42501 | 009 | DIRECT | TC-02 | COVERED |
| AC2.4 | Three `has_*_privilege` checks false | 009 | DIRECT | Run in the migration-account session (REVIEW-120); TC-02 | COVERED |
| AC2.5 | `ace_view_owner` owns 16, SELECT on 21 Tier 1, no IUD | 004, 009, 015 | DIRECT | Tier 1 grant is P4(d) (DG-L22); TC-02 | COVERED |
| AC2.6 | `rwb_no_grant` cannot select | 009 | DIRECT | TC-02 | COVERED |
| AC3.1 | 14 Section B views compile; 30 = 16 + 14; 30 of 30 compile | 005, 006, 008 | DIRECT | TC-03 | COVERED |
| AC3.2 | One-row select from each of 30 | 008, 017 | DIRECT | As `recovery_svc`; needs Tier 2 grant (SPEC-015); TC-03 | COVERED |
| AC3.3 | One history row for Section B after Section A | 017 | DIRECT | TC-03 | COVERED |
| AC3.4 | Without `public.valuation`: fails naming the relation; no Section B view; 16 unchanged | 018 | DIRECT | Message quoted by PG (DG-L26); TC-03 | COVERED |
| AC3.5 | Section B features stay behind flags | 018 | INHERITED_EXISTING_BEHAVIOR | No such feature exists yet; owners are consuming stories (Out of scope) | COVERED |
| AC4.1 | No constraint names a table or type outside `recovery`; 0 rows | 008 | DIRECT | Check 2; TC-04 | COVERED |
| AC4.2 | Fixture FK fails with the [S1] message; merge blocked | 008 | DIRECT | Failing check blocks the pipeline; TC-04 | COVERED |
| AC5.1 | Totals by source system (122 / 1,366 in [S1]) | 010 | DIRECT | Asserts 123 / 1,382 per [T2] Revision 4 (Physical Schema v6 plus 3 provisional rows); DG-L05 | COVERED |
| AC5.2 | 30 objects, 304 fields, 177 + 127 | 010 | DIRECT | TC-05 | COVERED |
| AC5.3 | Table fields (1,062 in [S1]), 49 on extension tables | 010 | DIRECT | Asserts 1,078 and 49; DG-L05 | COVERED |
| AC5.4 | One `sys_objects` row per view, one `sys_fields` row per column | 008, 010 | DIRECT | Check 3; TC-05 | COVERED |
| AC5.5 | `legacy_bucket` fixture fails with the [S1] message | 008 | DIRECT | TC-05 | COVERED |
| AC6 | DF-ACE-018 attributes; `ACC0000017` returns 95 | 003, 010 | DIRECT | TC-06 | COVERED |
| AC7.1 | Four tables: column counts, PKs, check constraint | 011 | DIRECT | TC-07 | COVERED |
| AC7.2 | 49 columns, 49 fields DF-EXT-001..049; no FK to `public` | 010, 011 | DIRECT | TC-07 | COVERED |
| AC7.3 | Duplicate `P0000123` → 23505, one row | 011 | DIRECT | TC-07 | COVERED |
| AC8.1 | `AccountReader` on `public.account` fails; on the view passes | 012 | DIRECT | TC-08 | COVERED |
| AC8.2 | Native query on `public.account` fails | 012 | DIRECT | TC-08 | COVERED |
| AC8.3 | Allowed names read from the module map | 012, 013 | DIRECT | TC-08, T-12 | COVERED |
| BR1 | Read only through 30 SELECT-only views; nothing loaded or copied | 003, 006, 009, 012 | DIRECT | TC-01, -03, -08 | COVERED |
| BR2 | `ace_view_owner` owns, SELECT on ACE tables, writes nothing, no other right in `recovery` | 004, 006, 009, 015, 017 | DIRECT | TC-01, -02, T-14 | COVERED |
| BR3 | `recovery_svc` SELECT on views only; nothing in `public`; PUBLIC nothing; no view write | 002, 004, 008, 009 | DIRECT | DML on Workbench tables belongs to the RWB-E1-001 migration (DG-L10, DG-L25); TC-02 | COVERED |
| BR4 | No constraint outside `recovery`; ACE link is `varchar(255)` | 007, 008, 011 | DIRECT | TC-04, -07 | COVERED |
| BR5 | `sys_objects` and `sys_fields` per view and column | 008, 010 | DIRECT | TC-05 | COVERED |
| BR6 | `ace_to_date`, `ace_to_boolean` return NULL rather than fail | 002, 020 | DIRECT | Required behaviour, not the [S2] body (DG-L23); TC-06, T-09, T-10 | COVERED |
| BR7 | Extension tables: decisions not copies; 1:1; seven standard columns | 007, 011 | DIRECT | TC-07 | COVERED |
| BR8 | BND-6; allow-list from the module map | 012, 013, 016 | DIRECT | TC-08 | COVERED |
| BR9 | Section B after its ACE table; later Flyway sequence | 005, 006, 013, 018 | DIRECT | DG-L20; TC-03 | COVERED |
| §4 step 2 | No environment name; `${recoverySchema}`; role names | 001, 014 | DIRECT | T-11 | COVERED |
| §17 guardrails | View list and roles as data; synthetic data; forward-only; identity number never in clear | 001, 005, 013, 019 | DIRECT | T-15 | COVERED |

**NFR mapping** ([S18] Non-Functional Specification v3; matrix NFR IDs are context-only today): NFR-045 synthetic data in DEV — DIRECT (SPEC-019, -020 fixtures). NFR-054 the pipeline blocks personal data in code and tests — DIRECT (no personal data in any fixture). NFR-039 party identifiers masked — partial: identity number masked in the view (SPEC-019); display masking RWB-E1-037. NFR-040 data minimisation — partial: only the 304 frozen fields are exposed ([S1] §19). NFR-042 every read logged — out of scope, RWB-E1-016. NFR-027 roll back by redeploying the previous tag — N/A: forward-only migrations ([S1] §17; C2 BS-2.3); a fault is fixed by a corrective file with `-- Fix:` (D-RCV-28).

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | SPEC-016 | No screen ([S1] §15); `platform.ts` reads an unchanged response. | N/A |
| Backend | YES | REQUIRED | 80% for **LINE, INSTRUCTION (statements), BRANCH and METHOD (functions)**, bundle level, by JaCoCo `recoveryCoverageVerification`, over all recovery main classes plus the two test-scope tooling class directories that the [T1] and [T3] includes name (the [T1] boundary tooling package, which holds the BND-6 detector, table-to-view map and `sourceViews` reader; and the [T3] lint tooling package, which holds the seam changes). Execution data from the `test` task only. Same counters as [T1] v4 SPEC-020 / T-TE001-10. In addition, each new or changed tooling class **in those directories** reaches 80% on all four counters in the report. `RecoveryFlywayTestSupport` is deliberately **outside** the bundle and carries no unit-coverage claim: it is test-scope, its only callers are the `recovery-it` tests T-E1-069-13 and T-E1-069-16, and the `test`-task execution data does not cover them (REVIEW-122). | SPEC-002, -012..-015, -018, -020 | No main class changes; the new unit-measured logic is test-scope tooling and SQL. SQL behaviour is proved by `recovery-it` tests, which are not counted toward unit coverage ([T1] v4 SPEC-020 (c)). | `./gradlew test recoveryCoverageVerification` passes; report saved as evidence. |

| Test case | Level | Covers | SPEC |
|---|---|---|---|
| TC-E1-069-01 | recovery-it | AC1, BR1, BR2 | 001, 003, 007, 008, 015, 017 |
| TC-E1-069-02 | recovery-it | AC2, BR3 (and BR2) | 002, 004, 009, 015 |
| TC-E1-069-03 | recovery-it | AC3, BR1, BR9 | 005, 006, 008, 015, 017, 018 |
| TC-E1-069-04 | recovery-it | AC4, BR4 | 008 |
| TC-E1-069-05 | recovery-it | AC5, BR5 | 008, 010 |
| TC-E1-069-06 | recovery-it | AC6, BR6 | 003, 010, 020 |
| TC-E1-069-07 | recovery-it | AC7, BR7 | 007, 011 |
| TC-E1-069-08 | unit (`test`) | AC8, BR8 | 012, 013, 016 |
| T-E1-069-09 | recovery-it | BR6 literal calls, `ace_to_boolean`, `ace_mask_value`, function privileges | 002, 020 |
| T-E1-069-10 | recovery-it | BR6 through `v_ace_payment`; DateStyle | 002, 020 |
| T-E1-069-11 | unit | Lint seams SEAM-E044-01/02, §4 step 2 | 001, 014 |
| T-E1-069-12 | unit | `sourceViews` validation and migration-folder rules | 013 |
| T-E1-069-13 | recovery-it | X2 probe-off case | 018 |
| T-E1-069-14 | recovery-it | BR2 end state after Section B | 006, 017 |
| T-E1-069-15 | recovery-it | Data protection checks | 019 |
| T-E1-069-16 | recovery-it | Flyway-mode `RecoveryDatabaseIT`; `RecoverySchemaMigrationIT` at the RWB-E1-001 file's version; the D-RUN-14 rights (check 5) | 008, 015 |
| T-E1-069-17 | unit | Connection-input switch (`RWB_CONFORMANCE_TARGET`) with a stubbed environment | 008 |
| T-E1-069-18 | build | `./gradlew test recoveryCoverageVerification`, four counters ≥ 80% | Unit Test Applicability |

All `recovery-it` tests run on `postgres:16.16-alpine`, not PostgreSQL 17 (DG-L14). API testing: N/A. Functional UI testing: N/A.

## Clarification Log

`CLARIFICATION_STATUS: NOT_REQUIRED`

Every conflict is settled by the RUN-BRIEF precedence (D-RCV-35/36 → ADR v3 → Decision Log v10 → story files v7 → older) or a documented default, or by an orchestrator decision applied as recorded (D-RUN-14 in DG-L29; the sibling-spec hand-over in DG-L27 and DG-L30), and recorded in `document-gaps.md` (DG-L01..L30, no blocker). Rulings that need owner confirmation are assumptions with proposed open items (`assumptions.md`; `shared-updates.md` OI-069-A..M, OPEN-035). No question is asked (L-RCV-03).

## Status

- `MCP_STATUS_SUMMARY: No Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); the story has no UI, so no design evidence is needed.`
- `MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]`
- `CHANGE_CLASSIFICATION_SUMMARY: A new story with backend database, grant, helper-function, build-rule and local-init logic only; no UI and no API.`
- `CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: no prior SPEC for RWB-E1-069; migrations, grants, BND-6 and local Flyway mode only]`
- `REQUIREMENT_COVERAGE_SUMMARY: 31 AC clauses, 9 business rules, the step-2 rule and the guardrails are each mapped to a SPEC item and a test; AC5 totals assert what the RWB-E1-001 migration seeds (123 / 1,382 / 1,078 / 49) with the source deviations recorded (DG-L05).`
- `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 42] [COVERED_RULES: 42] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]`
  - Source contradictions are document gaps DG-L01..L30, settled by precedence, a default, or a recorded orchestrator decision; none is left open in the spec.
- `SPEC_DEPENDENCY_REVISIONS: RWB-E1-044 v14-7 (review-7 PASS); RWB-E1-001 Revision 4 (review-4 PASS); RWB-TE-001 v4 (review-5 PASS)`
- `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]`
