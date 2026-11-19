---
title: "Specification: RWB-E1-044 Database migrations versioned with parameterized schema names"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
increment: INC-001 (build order 1 of 72, Build Sequence v6)
spec_version: v14-7 (remediation run 6 after spec gate round 6; run 4 applied orchestrator decision D-RUN-17; v14-1 kept as `spec.run1.md`, v14-2 as `spec.run2.md`, v14-3 as `spec.run3.md`, v14-4 as `spec.run4.md`, v14-5 as `spec.run5.md`, v14-6 as `spec.run6.md`)
date: 2026-11-18
status: SUCCESS (pending spec gate round 7, `../review/spec-gate-review-7.md`)
---

# RWB-E1-044 Specification

What changed, finding by finding, is in `gate-response.md` (round 1: v14-1 to v14-2; round 2: v14-2 to v14-3; round 3: v14-3 to v14-4, including D-RUN-14; round 4: v14-4 to v14-5, including D-RUN-17; round 5: v14-5 to v14-6; round 6: v14-6 to v14-7). The earlier versions are kept in `spec.run1.md` to `spec.run6.md`.

## Sources and precedence

Paths are relative to `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/` unless they start with `aisdlc/` or a repository path.

| Ref | Document (name, version, section) | Path |
|---|---|---|
| S-STORY | User story RWB-E1-044, story files v7, §1–§19 | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md` |
| S-E069 | User story RWB-E1-069, story files v7 (§3 preconditions, §4 flow 1, §10 authority; Section A views, grants) | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-069-read-only-ace-source-views-grants-and-boundary-rule-v1.md` |
| S-E056 | User story RWB-E1-056, story files v7 (`GET /admin/jobs` from `job_catalog`) | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-056-run-books-and-monitoring-for-every-epic-1-job-v1.md` |
| S-DL10 | Recovery Workbench Decision Log v10, row D-RCV-28 (DL42): naming, header, fix line, schema `recovery` via `${recoverySchema}`, "RWB-E1-044 ships no production migration file" | `01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| S-SQREG | Squad decision register, `INC-001-decisions.md` and `decision-register.md`: D-RCV-05, -12, -28 parts (1)–(4), -40, -43, -44, -48; L-RCV-03, L-RCV-07 | `aisdlc/docs/decisions/` |
| S-D35 | Client decision D-RCV-35 ACE DB alignment change register v1 (§2 U3, U4; §3.2 Section A views ship with RWB-E1-069) | `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md` (working copy of `15-ace-db-alignment/recovery-workbench-ace-db-alignment-change-register-v1.md`) |
| S-ACE1 | ACE Team Stories v1, RWB-ACE-001 (§3 preconditions, §4 flow 5, authority table: the ACE DBA applies the grant) | `04-user-stories/recovery-workbench-ace-team-stories-v1.md` |
| S-ADR3 | Architecture Decision Records v3, ADR-002, ADR-010 | `05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md` |
| S-ENV4 | Environment and Deployment Design v4, §5 (two-migration rule; "Schema names are parameters"; ACE read role table) | `05-technical-architecture/recovery-workbench-environment-and-deployment-design-v4-docx.md` |
| S-PS6 | Physical Schema v6, header, function bodies (lines 2390, 6145, 6163, 6185), Section A (`FROM public.account …`) and the commented grant block (from line 6822) | `06-data/recovery-workbench-physical-schema-v6.sql` |
| S-API4 | API Specification v4, `GET /admin/jobs` (`getAdminJobs`, `x-module: P1`) | `05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| S-EMS4 | Error and Message Standard v4, MSG-P3-016, MSG-P4-002 | `07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| S-FSD | FSD P3 Case and Workflow v4, A2.24 (FEAT-CWC-24) | `03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v6_extracted/recovery-workbench-fsd-p3-case-and-workflow-v4.md` |
| S-BRP | Business Requirements Program v4, §5.1 (REQ-RDF-001, REQ-RDF-014) | `03-requirements-and-specifications/recovery-workbench-business-requirements-program-v4-docx.md` |
| S-NFR | Non-functional specification v3, NFR-027, NFR-052 | `03-requirements-and-specifications/recovery-workbench-non-functional-specification-v3-docx.md` |
| S-BSEQ | Build Sequence Epic 1 and Epic 2 v6 (E1-044 = 1, E1-069 = 10, E1-056 = 18) | `11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` |
| S-RUN | RUN-BRIEF (precedence, D-RUN-07, D-RUN-08); build log (D-RUN-07, D-RUN-08, D-RUN-09, D-RUN-13, D-RUN-14, D-RUN-17; orchestrator triage 2026-11-17T23:40 on round 1, 2026-11-18T00:01 on round 2, 2026-11-18T00:28 on round 3 and 2026-11-18T00:55 on round 4) | `aisdlc/RUN-BRIEF.md`; `<repo>/AI-SDLC-BUILD-LOG.md` |
| S-TE001 | Technical specification RWB-TE-001 v4 (passed its spec gate): SPEC-020 (coverage tasks), SPEC-022 and its Relocation table (package layout), SPEC-023 (property binding split), SPEC-024 (coverage tests), T-TE001-10, T-TE001-12 | `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md` |
| S-ASV1 | ACE Source Views v1, grant block (line 727: `ALTER VIEW recovery.v_ace_account OWNER TO :ace_view_owner`) | `15-ace-db-alignment/recovery-workbench-ace-source-views-v1.sql` |
| S-TC7 | Test Cases v7, TC-ACE-001-04 ("AC4 Read grant only"; the ACE DBA applies the table grants) | `09-testing-and-quality/recovery-workbench-test-cases-v7-xlsx.md`; also ACE Team Stories v1 test table |
| S-AUD | Phase 0 standards audit, A-01, A-04, A-07, A-17, A-19 | `aisdlc/evidence/phase0-standards-audit.md` |
| S-BS | Backend standards BS-2.1–2.9, BS-4.5, BS-4.6, BS-7.2 | `aisdlc/.github/contexts/backend-standards.md` |
| S-TS | Testing standards §6 coverage rules | `aisdlc/.github/contexts/testing-standards.md` |
| S-GATES | Specification and implementation execution gates | `aisdlc/.github/rules/specification-execution-gates.md`, `implementation-execution-gates.md` |
| S-AGENTS | `AGENTS.md` §2, §3.6, §3.7, §4.5, §4.6, §4.7, §6, §7 | `<repo>/AGENTS.md` |
| S-V2 | 10 Nov 2026 spec (history; CLAR-001 A, CLAR-002 A, CLAR-004 A reused) | `aisdlc/output/INC-001-epic-1-RWB-E1-044/_v2-baseline/specify/spec.md` |

**Precedence** (RUN-BRIEF): D-RCV-35/36 > ADR v3 > Decision Log v10 > story files v7 > older maps and drafts.

- Where story v7 conflicts with Decision Log v10 D-RCV-28, Decision Log v10 is applied (DG-L01).
- D-RCV-28 parts (2) literal-schema scope, (3) Testcontainers and JaCoCo tasks and (4) Flyway's own message for a refused clean are **not** in Decision Log v10. They are in the squad register (S-SQREG, `INC-001-decisions.md`, row D-RCV-28, status Active). The squad register is not named in the RUN-BRIEF precedence list. This spec applies it where it details the Decision Log v10 row of the same ID and where story v7 is silent or lower. That choice is labelled ASM-E044-11. The one place it overrides story text (refused clean) is recorded as DG-L11.
- ADR v3 ADR-010 and D-RCV-35 rank above Decision Log v10. They require views over ACE `public` tables, shipped as a recovery migration by RWB-E1-069. The D-RCV-28 lint, as this story ships it, rejects that text. The conflict is DG-L09. Its resolution is a seam owned by RWB-E1-069 (SPEC-016).
- RWB-E1-069 v7 §3 says the recovery migration account holds the ACE DBA role "(RWB-E1-044)". D-RCV-35 U3 and ADR v3 ADR-010 rank above story files v7. This story declines that role (SPEC-017; DG-L13). Orchestrator decision D-RUN-14 gives the migration account exactly two narrower rights instead: `USAGE ON SCHEMA public` with no table privilege, and membership of `ace_view_owner` with `INHERIT FALSE, SET TRUE` (SPEC-017).
- Orchestrator decision D-RUN-17 (build log §1, 2026-11-18T00:55) orders RWB-TE-001 before RWB-E1-044 in wave A. This spec is therefore written against RWB-TE-001 v4's package layout (S-TE001 SPEC-022, SPEC-023) and coverage wiring (S-TE001 SPEC-020), and E1-044's code gate runs after RWB-TE-001 is merged. Build Sequence v6 lists no dependency between orders 1 and 2, and RWB-TE-001 adds no migration, so migration numbering is unaffected.

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `ENHANCEMENT_LOGIC_ONLY` |
| UI In Scope | NO |
| Logic In Scope | YES |
| API In Scope | NO |
| API Impact Type | NO_API_CHANGE |
| Impacted Existing Nodes | Paths as they are after RWB-TE-001 is merged (D-RUN-17; S-TE001 SPEC-022 Relocation table, SPEC-023): `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/migration/RecoveryFlywayConfig.java` (P3; moved there from `platform/internal/` by RWB-TE-001); the `casewf.migration` properties record that RWB-TE-001 SPEC-023 creates to bind `rwb.schema` and `rwb.flyway.*` (schema pin, SPEC-002; its class name is set by RWB-TE-001's plan and code, and this spec calls it the **migration properties record**); `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java` (logic moves to the test-scope tooling package, SPEC-016; RWB-TE-001 does not move it); `backend/src/main/resources/db/modulemigration/recovery/README.md`; `backend/build.gradle.kts` (the class directories of the coverage tasks only, SPEC-014); `infra/postgres/init/20-grants.sql.inc` (the two D-RUN-14 migrator rights in the local stack, SPEC-017) and the role comments in `infra/postgres/init/00-roles-and-databases.sh` (comment text only, SPEC-017) |
| New Nodes Required | YES. Main scope: at most one package-private, unconditional configuration class in `casewf.migration` that registers the migration properties record, needed only if RWB-TE-001 registers that record from the conditional `RecoveryFlywayConfig` (SPEC-002). Test scope: the migration-lint and schema-comparator tooling classes (SPEC-016, SPEC-012), their unit tests, one container test class, and lint and Flyway fixture folders. Also story and plan convention files (SPEC-015) |
| Inherited Existing Behavior | Recovery Flyway bean settings: own history table `flyway_schema_history_recovery`, `outOfOrder(false)`, `baselineVersion("0")`, `baselineOnMigrate(true)`, `cleanDisabled(true)`, `createSchemas(false)`, `validateMigrationNaming(true)`, placeholder `recoverySchema`. Also the migrator data-source selection, the baseline migration lint rules, the `recoveryIntegrationTest` task, `RecoveryDatabaseIT` (S-AUD A-04; S-SQREG D-RCV-28, D-RCV-48), and RWB-TE-001's merged state, which must stay green: the 19-module package layout, the module map with `RecoveryBoundaryTest` and `ModulithTest`, the `recoveryCoverageReport` / `recoveryCoverageVerification` wiring of S-TE001 SPEC-020, and the S-TE001 SPEC-024 coverage tests (for example T-TE001-12 and the `RecoveryFlywayConfig` configuration test), changed only as SPEC-002 "Existing tests" allows |
| Frontend Changes Required | NO |
| Backend Changes Required | YES |

**Classification evidence.** A prior trace chain exists: S-V2, and Traceability Matrix v2.0 §3 row 001 (RWB-E1-044 to BR-RWB-013 / FR-RWB-013). The code already holds the Flyway bean and the lint (S-AUD A-04). This story changes rules and checks only. It adds no route, screen or endpoint.

**Production migration file.** None. Decision Log v10 D-RCV-28 and story v7 §13 both say RWB-E1-044 "ships no production migration file". No `<seq>` is fixed in this spec (D-RUN-07). Every `V<seq>__…` file named below is a test fixture under `backend/src/test/resources/`, never in `db/modulemigration/recovery/`. Fixtures need concrete numbers because the lint checks contiguity from `V0001` (ASM-E044-14).

**Dependencies (D-RUN-08, D-RUN-17).** This spec depends on code in this repository (the Flyway bean, the lint, `RecoveryDatabaseIT`, `infra/postgres/init/`, the JaCoCo tasks) and, by orchestrator decision D-RUN-17, on RWB-TE-001 v4 merged before it: its package relocation (S-TE001 SPEC-022), property binding split (SPEC-023), coverage wiring (SPEC-020) and coverage tests (SPEC-024). D-RUN-17 makes RWB-TE-001 an earlier merge for this story, so D-RUN-08 is met. D-RUN-17 sets the merge order and a condition on E1-044's code gate only, so the E1-044 plan is written from RWB-TE-001 v4 and RWB-TE-001's plan once that plan has passed its gate; it does not wait for RWB-TE-001's code. **Builder's first step (before any E1-044 change):** check the merged RWB-TE-001 code against every point this spec relies on (the package of `RecoveryFlywayConfig`, the migration properties record, its registration, the keys it binds, the coverage wiring of SPEC-020, the tests of SPEC-024) and record the coverage baseline (SPEC-014). If the merged code differs, the build stops and reports it to the orchestrator; it does not rebuild RWB-TE-001's work (ASM-E044-19). The migrator rights of D-RUN-14 are added by this story to the local init (SPEC-017); in SIT, UAT and PROD the environment owner applies them (OI-E044-I). Work owned by later stories is named as a seam in SPEC-016 and SPEC-017 and is out of scope.

## Intent

Every change to schema `recovery` is a versioned, checksummed, forward-only Flyway migration. It names the schema only as `${recoverySchema}`, carries its story key, and is checked by a build-time lint and a container test before merge (S-STORY §1, §8 BR1–BR8; S-DL10 D-RCV-28; S-BRP REQ-RDF-001, REQ-RDF-014).

## Trigger and preconditions

| Trigger or precondition | Condition | Source |
|---|---|---|
| Service start, whatever the value of `rwb.flyway.enabled` | `rwb.schema` binds to exactly `recovery`, or start fails (SPEC-002) | S-DL10 D-RCV-28; S-AUD A-17 |
| Service start with `rwb.flyway.enabled=true` (default) | Schema `recovery` exists and is owned by `rwb_migrator` (`createSchemas(false)`). Migrator credentials come from the environment or the key store | S-ADR3 ADR-010; S-BS BS-4.5; S-NFR NFR-052; `infra/postgres/init/` |
| `./scripts/dev.ps1 test` (Gradle `test`) | None. The lint and the comparator unit tests need no database | S-SQREG D-RCV-05, D-RCV-28 (3) |
| `./scripts/dev.ps1 it` (Gradle `recoveryIntegrationTest`, tag `recovery-it`) | Docker is available. The task fails, not skips, without Docker | S-SQREG D-RCV-28 (3), D-RCV-44 |
| Story §3: recovery tables defined in LDM and Physical Schema v6 | Satisfied by the documents. No table is created by this story | S-STORY §3; S-PS6 |
| Story §3: module folder and boundary test exist (RWB-TE-001) | Satisfied by RWB-TE-001, merged before this story (D-RUN-17): the 19 module packages (S-TE001 SPEC-001), the sub-package `recovery.casewf.migration` that the SPEC-022 relocation creates under module `casewf` to receive `RecoveryFlywayConfig` (it is not one of the 19 module packages), the module map and the map-driven boundary rules. E1-044's changes keep `RecoveryBoundaryTest` and `ModulithTest` green | S-TE001 SPEC-001, SPEC-022; D-RUN-17 |
| Story §3: migration account and read-only drift account in the key store | Migration account: inherited (`rwb.flyway.user`, SPEC-001). Read-only drift account: out of scope (D-RCV-05; SPEC-017) | S-STORY §3; S-SQREG D-RCV-05 |
| Story §3: `RWB_SCHEMA` set per environment | Replaced by the pin to `recovery` (SPEC-002; DG-L01) | S-DL10 D-RCV-28 |
| Story §3: deployment slots booked (DL35) | Outside the repository. No code or test applies | S-STORY §3 |

## Requirement-to-SPEC Logic Coverage

Coverage Type names the main source of each row. "Restated" and "out of scope by decision" are given in Implementation Notes.

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| AC1 / BR1 / BR5 | A pending migration applies once. Version and checksum are recorded in `flyway_schema_history_recovery`. A rerun applies nothing | SPEC-001, SPEC-011 | INHERITED_EXISTING_BEHAVIOR | Bean behaviour exists. The container proof is new (T-044-10) | COVERED |
| AC2 / BR7 / X1 | Drift between the migration result and a target fails with MSG-P3-016 naming `<schema>.<table>.<column>` | SPEC-012 | DIRECT | Restated: container-to-container comparison before every MR (CLAR-001) | COVERED |
| AC2 / BR7 (real SIT/UAT/PROD, flag `rwb.p3.migration-drift-gate`); story §3 read-only account for the drift check | Drift check against real environments, gating deployment | SPEC-017 | DIRECT | Out of scope by decision: parked by D-RCV-05; CLAR-001 A (S-V2). DG-L02 | COVERED |
| AC3 / BR2 | The schema comes from a parameter. The same file produces the table in schema `recovery` in two databases | SPEC-001, SPEC-002, SPEC-007, SPEC-011 | DIRECT | Restated: value fixed to `recovery` (Decision Log v10 D-RCV-28; story §13). `RWB_SCHEMA=rwb_case` not applied (CLAR-003) | COVERED |
| AC4 / BR5 / X2 | An applied migration edited later fails validation. MSG-P3-016 names the version. The service does not start | SPEC-001, SPEC-003, SPEC-011 | DIRECT | `validateOnMigrate(true)` made explicit. The version is mandatory (SPEC-003) | COVERED |
| AC5 / BR2 / X3 | A literal schema qualifier fails the build with MSG-P3-016 naming file and line | SPEC-004, SPEC-007, SPEC-010 | DIRECT | Rule scope from squad register D-RCV-28 (2) | COVERED |
| AC6 / BR3 / X4 | Two non-fix files with the same key, or a file with no key, fail the build naming both files and the key | SPEC-004, SPEC-006, SPEC-010 | DIRECT | Second-non-fix and line-1 checks are inherited. The finding format is new | COVERED |
| AC7 / BR4 / X5 | Clean is refused, undo files are refused, forward only | SPEC-001, SPEC-005, SPEC-011, SPEC-013 | INHERITED_EXISTING_BEHAVIOR | `cleanDisabled(true)` exists. The refused clean shows Flyway's own message (squad register D-RCV-28 (4); DG-L11). The L-UNDO rule ID is new | COVERED |
| AC8 / X6 | A migration that fails part way rolls back fully. The failure is recorded. The service does not start | SPEC-003, SPEC-011 | DIRECT | Restated: the record is the ERROR log with MSG-P3-016 and the version. No failed history row remains on PostgreSQL (CLAR-006; DG-L03) | COVERED |
| AC8 (job monitor display) | The run shows "failed" on the job monitor | SPEC-017 | DIRECT | Out of scope by decision D-RCV-12. No receiving story is named (DG-L10; OI-E044-G) | COVERED |
| AC9 / X7 | Two instances starting together apply a pending migration exactly once. Both start | SPEC-011 | INHERITED_EXISTING_BEHAVIOR | Flyway's PostgreSQL lock. The proof is new (T-044-16) | COVERED |
| BR6 | Own history table | SPEC-001 | INHERITED_EXISTING_BEHAVIOR | `HISTORY_TABLE` constant | COVERED |
| BR8 | No FK into `public`. The lint names the file | SPEC-008, SPEC-010 | DIRECT | Dedicated rule L-FK-OUTSIDE, the control in every environment. T-044-17 proves the database refusal against this repository's catalog grants only: under D-RUN-14 `rwb_migrator` has `USAGE` on `public` but no table privilege, and its `ace_view_owner` membership is `INHERIT FALSE`, so it holds no `REFERENCES` on an ACE table. An environment that gives the migration account a table privilege in `public` would accept the FK (DG-L13) | COVERED |
| D-RCV-28 (1) (Decision Log v10 and squad register) | Name, contiguous seq, one non-fix per key, fix rule, no `R__` | SPEC-005, SPEC-006 | INHERITED_EXISTING_BEHAVIOR | Duplicate-seq, multi-key-line and fix-without-base findings are new | COVERED |
| D-RCV-28 (2) (squad register) | Literal schema in object-name positions, qualified types, bare `SCHEMA`; `SET search_path` in every form | SPEC-007 | DIRECT | Search-path forms widened (SPEC-007). The ADR-010 conflict is DG-L09, with a seam (SPEC-016) | COVERED |
| Decision Log v10 D-RCV-28; story v7 §13 | Schema `recovery` in every environment; story §13 "no per-environment override" | SPEC-002 | DIRECT | Closes audit A-17 with `rwb.flyway.enabled` true or false: the pin is on the binding of the migration properties record in `casewf.migration`, registered with no condition, not on the Flyway bean (T-044-08) | COVERED |
| D-RUN-13 (build log) | The schema-prefix lint checks SQL identifiers only. It ignores string literals and comments (`--`, `/* */`) | SPEC-007, SPEC-008 | DIRECT | New compared with the baseline lint. One quote-aware tokenizer pass (orchestrator triage on S12), so a quote or comment opener inside another token cannot hide code. Physical Schema v6 holds 297 `'public.…'` dictionary literals that RWB-E1-001 seeds (T-044-21, T-044-22) | COVERED |
| D-RCV-48 (squad register) | First recovery migrate on a non-empty schema baselines at 0 and applies `V0001` | SPEC-001, SPEC-011 | INHERITED_EXISTING_BEHAVIOR | Settings exist. The full proof is new (T-044-18). The register text says schema `ace` (DG-L12) | COVERED |
| NFR-027 | Rollback by redeploying the previous tag | SPEC-013 | DIRECT | `*:future` default and `outOfOrder(false)` | COVERED |
| NFR-052 / BS-4.5 | Migration account credentials stay outside the repository | SPEC-001 | INHERITED_EXISTING_BEHAVIOR | No change | COVERED |
| Story §10: pipeline migration account | Applies migrations with the migration database account from the key store; not a Workbench role | SPEC-001 | INHERITED_EXISTING_BEHAVIOR | `rwb.flyway.user` / `password` from the environment or key store | COVERED |
| Story §10: RW-PLATADM runs deployments | Deployment is a pipeline action outside this repository | SPEC-017 | DIRECT | No Workbench endpoint in this story, so no method-security check applies (AGENTS §3.3 applies to endpoints) | COVERED |
| Story §10: RW-PLATADM reruns a failed migration job; reads runs on SCR-44. RW-DATASTEW and RW-AUDIT read runs | Role-based access to migration runs | SPEC-017 | DIRECT | Out of scope by decision D-RCV-12. No receiving story is named (DG-L10) | COVERED |
| Story §12 `GET /admin/jobs?type=MIGRATION`; `MigrationRunRecorder`; §14 MSG-P4-002; §15 SCR-44; §16 TC-E1-044-10 | Record and read migration runs; refuse a role without Platform administration R | SPEC-017 | DIRECT | Out of scope by decision D-RCV-12. No receiving story is named (DG-L10; OI-E044-G) | COVERED |
| Story §14 MSG-P3-016 | Drift, checksum mismatch, lint failure, refused clean or undo, failed migration | SPEC-003, SPEC-004, SPEC-012, SPEC-013 | DIRECT | ID and parameters only (CLAR-004). Refused clean uses Flyway's message (DG-L11) | COVERED |
| Audit A-19 | The first story sets the story and plan file convention | SPEC-015 | DIRECT | ASM-E044-08 | COVERED |
| ADR v3 ADR-010; D-RCV-35 U4; Env v4 §5 (Section A views over `public` ship as a recovery migration with RWB-E1-069) | A recovery migration must be able to create `v_ace_*` views over ACE `public` tables | SPEC-016 | DIRECT | Seam owned by RWB-E1-069 (D-RUN-08; orchestrator triage). Not built here. DG-L09; OI-E044-F | COVERED |
| RWB-E1-069 v7 §3 (attributed to RWB-E1-044) | The recovery migration account holds "the ACE DBA role for the release window", to grant on schema `public` and set a view owner | SPEC-017 | DIRECT | The ACE DBA role is declined (story v7 §3, §10; D-RCV-35 U3, U4; ADR v3 ADR-010; RWB-ACE-001 v1; RWB-E1-069 v7 §10). In its place, orchestrator decision D-RUN-14 gives exactly two rights: `USAGE ON SCHEMA public` with no table privilege, and `ace_view_owner` membership `WITH INHERIT FALSE, SET TRUE`, added to the local init by this story. DG-L13; OI-E044-I; OI-E044-J | COVERED |

## Backend Specification

### SPEC-RWB-E1-044-001 Recovery Flyway bean (extend, do not duplicate)

- Change `RecoveryFlywayConfig` where RWB-TE-001 puts it: package `th.co.scb.ace.demo.recovery.casewf.migration` (P3, package-private), the story v7 §13 home (S-TE001 SPEC-022 Relocation table; D-RUN-17). Every inherited setting listed under Change Scope Declaration stays (S-AUD A-04; S-SQREG D-RCV-28, D-RCV-48; S-BS BS-2.3).
- Add `validateOnMigrate(true)` explicitly. Story §12 sets it. Flyway's default is the same, so behaviour is unchanged and the intent becomes visible.
- Leave `ignoreMigrationPatterns` at Flyway's default (`*:future`). A previous tag then starts against a database that holds a later version (NFR-027, SPEC-013).
- Data-source selection stays as is: the migrator account when `rwb.flyway.user` is set, otherwise the main data source. Credentials come from the environment or the key store only (BS-4.5, NFR-052).
- The story §13 Java package `recovery.casewf.migration` exists once RWB-TE-001 is merged, so this story creates no package of its own for the bean. The migration resource folder stays `db/modulemigration/recovery` (inherited; the story's `recovery/src/main/resources/db/migration/recovery` is not used). DG-L06 records the folder difference.

### SPEC-RWB-E1-044-002 Schema pinned to `recovery`, whether or not Flyway is enabled

**Reason.** `application.yaml` binds `rwb.schema: recovery`, but relaxed binding lets the environment variable `RWB_SCHEMA` override it (S-AUD A-17: "Nothing pins `rwb.schema` to `recovery`"). Decision Log v10 D-RCV-28 says the schema "is recovery in every environment". Story v7 §13 says "no per-environment override". The value is used outside Flyway too: `hibernate.default_schema: ${rwb.schema}` in `application.yaml`, and `PlatformInfoController` (P2 `integration.internal` after RWB-TE-001) reads it through its own record (S-TE001 SPEC-023). So the pin cannot depend on the recovery Flyway bean, which is `@ConditionalOnProperty(name = "rwb.flyway.enabled", …, matchIfMissing = true)` and can be switched off with `RWB_FLYWAY_ENABLED=false`.

**Where the check runs.** On binding of the **migration properties record**, not on creation of `recoveryFlyway`. RWB-TE-001 SPEC-023 replaces `platform.internal.RecoveryProperties` with package-private records per module. The record in `casewf.migration` binds `rwb.schema` and `rwb.flyway.*` for `RecoveryFlywayConfig`, with the same keys and defaults. Its class name is a RWB-TE-001 plan detail; the E1-044 plan takes it from RWB-TE-001's gated plan, and the builder's first step confirms it in the merged code (ASM-E044-19).

- **Registration with no condition.** `@EnableConfigurationProperties` on a class that carries `@ConditionalOnProperty` is skipped together with that class when the condition is false. So the migration properties record must be registered by a package-private `@Configuration(proxyBeanMethods = false)` class in `casewf.migration` that has no condition. This spec calls it `MigrationPropertiesConfig`; the name is the plan's choice.
  - If RWB-TE-001 registers the record on `RecoveryFlywayConfig` (as its plan, not yet gated on 18 Nov 2026, proposes), E1-044 moves the `@EnableConfigurationProperties` to the new class.
  - If RWB-TE-001 already registers it from an unconditional class in `casewf.migration`, that class is used and nothing is added.
  - The plan states which case applies, from RWB-TE-001's gated plan. The builder's first step confirms it in the merged code and stops and reports on a mismatch. This repository registers every properties type with `@EnableConfigurationProperties` on a configuration class and uses no `@ConfigurationPropertiesScan` (`PlatformConfig.java`, `TemporalConfig.java`, `DroolsProperties.java`, `BlobDocumentStore.java`, read 18 Nov 2026).
- **Bound on every start.** A configuration-properties bean is a non-lazy singleton, and `application.yaml` sets no `spring.main.lazy-initialization`. So the record is bound at context refresh even when no other bean consumes it, whatever `rwb.flyway.enabled` is.
- **The check (Bean Validation at binding; orchestrator triage of round 6).** The migration properties record carries `@Validated`, and its `schema` component carries `@NotNull` and `@Pattern(regexp = "recovery")` (the whole value must match, case-sensitive, so null, blank and any other value fail). `spring-boot-starter-validation` is already an `implementation` dependency (`backend/build.gradle.kts` line 44). Spring Boot validates the record after binding it; a violation becomes a `BindValidationException` inside its configuration-properties bind failure, and context refresh fails. The service serves no request and runs no migration. The constraint is on `schema` only, so no nested value is read.
- **Why not a compact-constructor check.** A constructor check would also run when code builds the record directly. RWB-TE-001's `RecoveryFlywayConfigTest` does that: it calls `recoveryFlyway(...)` directly with a record it builds (RWB-TE-001 plan v1, `plan.md` "Coverage tests" row `casewf/migration/RecoveryFlywayConfigTest.java`; S-TE001 SPEC-024 "configuration built without running `migrate`"). Neither the RWB-TE-001 plan nor its spec states the schema value that test passes, so it cannot be shown that the test uses only `recovery`. Bean Validation runs only when Spring binds the record, so building it in code is unaffected. The compact-constructor option of v14-6 is withdrawn.
- The constraint message names the property `rwb.schema` and D-RCV-28 (for example `rwb.schema must be recovery (D-RCV-28)`); Spring's field error adds the rejected value. It holds no credential.
- **One check, in the migration module.** RWB-TE-001 SPEC-023 also binds `rwb.schema` in the P2 `integration.internal` record for `PlatformInfoController`. That record is not checked again: the start has already failed when the P3 record refuses the value. The check belongs to P3 `casewf.migration`, the module that owns migrations (story v7 §13).
- `RecoveryFlywayConfig` keeps reading the schema from the record and so gets the pinned value. The record stays the first parameter of `recoveryFlyway` (it is today, as `RecoveryProperties`).
- **Existing tests.** The plan lists every RWB-TE-001 test that binds the migration properties record or builds the `recoveryFlyway` bean, from RWB-TE-001's gated plan: for example T-TE001-12 ("bind each new properties record from the existing keys") and the S-TE001 SPEC-024 `RecoveryFlywayConfig` configuration test ("configuration built without running `migrate`"). The builder's first step confirms the list in the merged code. Such a test may get exactly two changes, and no assertion is changed, so no test is weakened: (1) the input `rwb.schema=recovery` is added where the test binds the record without it, the value `application.yaml` binds today; (2) the unconditional registration class is added to the test's configuration (for example its `withUserConfiguration`) where the test relied on `RecoveryFlywayConfig` to register the record. A merged test that would need any other change is a stop-and-report to the orchestrator. These tests stay green (Change Scope, Inherited Existing Behavior).

**Message.** The error is a start-up configuration error, not a user message. No message ID applies (ASM-E044-03).

**Test.** T-044-08 covers both values of `rwb.flyway.enabled` (Tests section).

### SPEC-RWB-E1-044-003 Migration failure reported as MSG-P3-016

- The migrate call made when the bean is initialised is wrapped so that it can report. Today it is `@Bean(initMethod = "migrate")`.
- **The factory method never migrates.** `recoveryFlyway(...)` builds and returns the configured `Flyway` bean and does not call `migrate`. The wrapped migrate runs only when the container initialises the bean (its init method, or an initialiser the plan names). So a test that calls `recoveryFlyway(...)` directly, such as the S-TE001 SPEC-024 `RecoveryFlywayConfig` configuration test, still runs no migration.
- When it throws a `FlywayException`, the bean logs **one** ERROR line with message ID `MSG-P3-016` and parameters `schema=recovery` and `object=<…>`. It then rethrows, so the application context fails and the service does not start (S-STORY X2, X6; S-EMS4 MSG-P3-016).
- `object` is set as follows:

| Failure | `object` | Mandatory | Where the version comes from |
|---|---|---|---|
| Validation failure on an applied migration: checksum mismatch, applied file missing, lower version pending under `outOfOrder(false)` | The version or versions concerned, comma-separated | Yes | Flyway's validate result: the invalid-migration entries and their versions (`validateWithResult()`) |
| Migration that fails part way | The version of the failed migration | Yes | The failed migration is rolled back on PostgreSQL and stays pending, so it is the first pending version in `info()` after the failure |
| Failure with no version: connection refused, lock timeout, missing schema | `recoveryFlyway` | — | Fallback only for these |

- The Flyway calls named in the table are the expected public API of the resolved Flyway 12.4.0 (ASM-E044-12). The plan may use another public Flyway API that yields the same version. T-044-09, T-044-12 and T-044-14 are the acceptance.
- Code holds the message ID and parameters only, with no message text (S-AGENTS §3.6; CLAR-004 A in S-V2).
- **What is logged.**
  - The bean's own ERROR line holds only the message ID and the two parameters. It holds no SQL and no credentials (S-BS BS-4.6).
  - The rethrown exception is logged by Spring when the context fails. It carries Flyway's own message. For a failed migration, that message includes the failing SQL statement.
  - This is accepted, not redacted. Recovery migrations hold DDL and reference data only, never personal data (S-AGENTS §4.7; S-STORY §17). The password is a separate property and is not part of the JDBC URL (ASM-E044-12).
  - Audit A-07 (log masking) is owned by RWB-TE-011 and is not built here.
- A refused `clean()` is not wrapped. It shows Flyway's own message (squad register D-RCV-28 (4); DG-L11).

### SPEC-RWB-E1-044-004 Lint finding format

- Every lint finding is one line: `MSG-P3-016 schema=recovery object=<file>:<line> rule=<RULE-ID> <detail>`.
- The line number is 1-based. It is 0 for file-level rules such as naming, sequence and duplicates.
- The test fails listing all findings, not only the first (S-STORY X3, AC5, AC6; ASM-E044-04).
- Rule IDs: `L-NAME`, `L-UNDO`, `L-REPEATABLE`, `L-SEQ-GAP`, `L-SEQ-DUP`, `L-HEADER`, `L-HEADER-MULTI`, `L-KEY-DUP`, `L-FIX-NO-BASE`, `L-FIX-LINE2`, `L-SEARCH-PATH`, `L-LITERAL-SCHEMA`, `L-FK-OUTSIDE`, `L-GRANT`, `L-LEX` (15 rules; L-LEX is new in v14-3, SPEC-007).

**Finding multiplicity (new in v14-4, spec gate S17).** For the line-level rules, a finding is identified by (rule, file, line, key). One identity gives exactly **one** finding, however many clauses or positions of the rule match it. Different identities give separate findings.

| Rule | Key | Examples |
|---|---|---|
| L-LITERAL-SCHEMA | The disallowed schema name, as PostgreSQL resolves it: an unquoted name folded to lower case, a quoted name as written without its quotes | `CREATE TABLE public.x` matches items 1 and 4 and gives **one** finding. `FROM public.a JOIN public.b` on one line gives one finding. `public.a` and `ace.b` on one line give two. `SCHEMA public` and `public.t` on one line give one |
| L-FK-OUTSIDE | The qualifier after `REFERENCES`, resolved as above | Two `REFERENCES public.…` clauses on one line give one finding |
| L-SEARCH-PATH, L-GRANT | None | At most one finding per line |
| L-LEX | The offset of the unterminated opener | One finding per unterminated opener, on the opener's line |

- L-LITERAL-SCHEMA and L-FK-OUTSIDE are separate rules, so the same text can give one finding under each (SPEC-008).
- The line of a finding is the line of the matched schema name (or of the opener for L-LEX), not the start line of the statement.
- The detail of L-LITERAL-SCHEMA is `literal schema <name>`; of L-FK-OUTSIDE it is as in SPEC-008. Tests assert rule, file and line, and the key where two findings share a line.
- The file-level rules (line 0) report as SPEC-005 and SPEC-006 state.

### SPEC-RWB-E1-044-005 File-level naming rules (D-RCV-28 (1))

| Rule | Check | Status |
|---|---|---|
| L-NAME | Name matches `^V(\d{4})__(rwb_[a-z0-9]+_\d{3})_[a-z0-9_]+\.sql$` | Inherited |
| L-REPEATABLE | Any `R__*.sql` fails | Inherited |
| L-UNDO | Any `U*.sql` fails with its own rule ID. Today it falls into L-NAME | New |
| L-SEQ-DUP | Two files with the same `<seq>` fail, naming both | New. Today it is reported as a gap |
| L-SEQ-GAP | Sequences must be contiguous `0001..N` | Inherited |

Any non-`.sql` file other than `README.md` in the folder is reported under L-NAME (ASM-E044-05).

### SPEC-RWB-E1-044-006 Header and story-key rules

| Rule | Check | Status |
|---|---|---|
| L-HEADER | Line 1 equals `-- Story: <KEY>`, where `<KEY>` is derived from the file name (`rwb_e1_044` gives `RWB-E1-044`) | Inherited |
| L-HEADER-MULTI | A second `-- Story:` line anywhere in the file fails | New |
| L-KEY-DUP | At most one non-fix file per key. The finding names both files and the key | Inherited; the finding format is new |
| L-FIX-LINE2 | A file whose line 2 starts with `-- Fix:` must give a non-empty reason | New |
| L-FIX-NO-BASE | A fix file needs exactly one non-fix file of the same key with a lower `<seq>` | New |

### SPEC-RWB-E1-044-007 Literal-schema and search-path rules (squad register D-RCV-28 (2))

**Text preparation: one quote-aware tokenizer pass** (orchestrator triage on S12).

Comments and strings are never removed by separate passes or by separate regular expressions. A comment opener inside a string, or a quote inside a comment, would then hide real code: for example `VALUES ('/*');` on line 2, `CREATE TABLE public.x …` on line 3 and `-- */` on line 4. Instead, one tokenizer reads the raw file once, left to right. At each position outside a token it checks the openers below in table order and takes the first that matches. Inside a token only that token's own end and escapes are recognised.

| Token | Opens with | Ends with | Recognised inside |
|---|---|---|---|
| Line comment | `--` | End of line | Nothing |
| Block comment | `/*` | The matching `*/`. Nesting is counted, as in PostgreSQL: `/* a /* b */ public.x */` is one comment | Only `/*` and `*/`, for the nesting count |
| Escape string | `E'` or `e'`, where the `E` does not continue an identifier | `'` | `''` and `\'` are escaped quotes; `\\` is an escaped backslash |
| Standard string | `'`, including the `U&'`, `B'`, `X'` and `N'` prefixed forms | `'` not followed by `'` | `''` is an escaped quote. A backslash is an ordinary character (`standard_conforming_strings` is on by default) |
| Quoted identifier | `"` (also `U&"`) | `"` not followed by `"` | `""` is an escaped quote |
| Flyway placeholder | `${` | `}` | Nothing. `${recoverySchema}` is identifier text, never a dollar quote |
| Dollar-quoted body | `$tag$`, where the tag is empty or matches `[A-Za-z_][A-Za-z0-9_]*`, and the `$` does not continue an identifier. `$1` is a parameter, not a quote | The next literal occurrence of the same `$tag$`. The end is found first, as PostgreSQL does | The body is tokenized again with these same rules, bounded by its end (below) |
| Code | Anything else | — | — |

- **Dollar-quoted bodies are code.** Every dollar-quoted body in Physical Schema v6 is a function body (lines 2390, 6145, 6163, 6185), that is, executable SQL. D-RUN-13 exempts string literals, and a `public.` reference in a function body is a schema reference, not data. So the body is scanned: its identifiers are checked, and its own comments and strings are treated as above (ASM-E044-15).
- **The body end always wins.** A comment or quote left open inside a body ends at the body's closing `$tag$`, as in PostgreSQL. Nothing inside a body can hide text after the body.
- **Unterminated token (L-LEX, new).** A string, escape string, quoted identifier, block comment or dollar-quoted body still open at end of file gives one finding `rule=L-LEX`, `unterminated <kind>`, on the line of its opener. The opener is then treated as one code character and tokenizing resumes after it, so the rest of the file is still checked by every rule. PostgreSQL would reject such a file too. L-LEX stops a stray opener from hiding the rest of the file from the lint (ASM-E044-16).

The pass produces three views of the file. Each keeps the line structure: every blanked character becomes a space and every newline is kept, so line numbers stay correct.

| View | Comments | String literals | Quoted identifiers | Dollar delimiters | Dollar bodies | Used by |
|---|---|---|---|---|---|---|
| (a) Code text | Blanked | Kept | Kept | Kept | Kept, with their own comments blanked | L-SEARCH-PATH, L-GRANT |
| (b) Identifier text | Blanked | Blanked, quotes included | Kept | Blanked | Kept as code, with their own comments and strings blanked | L-LITERAL-SCHEMA, L-FK-OUTSIDE |
| (c) Statements | Cut from the identifier text (b): blanked | Blanked, as in (b) | Kept, as in (b) | Blanked, as in (b) | Kept as code, as in (b), and never split | L-LITERAL-SCHEMA (statement context for `isAllowedQualifier`, SPEC-016); L-GRANT (statement start, SPEC-009) |

- Views (a) and (b) have the same length as the raw file, character for character, so an offset means the same position in every view.
- Statements (c) are offset ranges over the identifier text (b), keeping those offsets. They are cut at the `;` tokens that the tokenizer found at top level only, never at a `;` inside a comment, string, quoted identifier or dollar body (a dollar body's text is code in (b), so the cut points come from the token list, not from a search of the text).
- A statement's start line, first word and kind (for example `CREATE VIEW`, `CREATE OR REPLACE VIEW`, `GRANT`) are read from (b) over its range: the first non-blank characters of the range. A leading comment, string or `-- …` line therefore never supplies the statement kind or the start line. A range with no non-blank character in (b), such as the text after the last `;` or between two adjacent `;` tokens, is not a statement.
- A rule that needs the code text of a statement (L-GRANT) reads the same offset range in (a). Each match keeps its own line (SPEC-004).
- L-HEADER, L-HEADER-MULTI and L-FIX-LINE2 read the raw lines, because the header lines are comments by design.

**Identifiers only (D-RUN-13).** The schema-prefix rules L-LITERAL-SCHEMA and L-FK-OUTSIDE check SQL identifiers only. They ignore string literals and comments (`--` and `/* */`). Two sources support this:

- Build log D-RUN-13: "A literal is not a schema reference".
- Physical Schema v6 holds 297 lines with a `'public.…'` literal, in the `sys_fields` dictionary rows (from line 5826). RWB-E1-001 seeds those rows, and each value is data, not a schema reference.

This agrees with squad register D-RCV-28 (2), where schema names inside string literals are "an accepted gap left to code review". It differs from the baseline lint in two ways, both marked New:

- The baseline lint skips only whole lines that start with `--`, so a trailing `--` comment or a `/* */` comment that names a schema fails today.
- The baseline lint does not strip strings, so `'public.account'` fails today.

The baseline could not hide code, because it removed nothing but whole comment lines. Removing comments and strings can hide code, which is why the one-pass tokenizer above and its adversarial test T-044-22 are required.

L-SEARCH-PATH is not a schema-prefix rule. It runs on the code text (a), where strings are kept (below).

**L-SEARCH-PATH.** D-RCV-28 (2) says "any `SET search_path` fails in every form". The rule runs on the code text (a): comments blanked, string literals kept. It fails on any occurrence of the identifier `search_path`, quoted or not, in any case. That is a superset of every form, including:

| Form | Status |
|---|---|
| `SET search_path …` | Inherited |
| `SET LOCAL search_path …`, `SET SESSION search_path …` | New |
| `SELECT set_config('search_path', …)` | New (inside a string, so it runs on the code text, where strings are kept) |
| `ALTER ROLE … SET search_path …`, `ALTER DATABASE … SET search_path …`, `ALTER FUNCTION … SET search_path …` | New |
| `RESET search_path` | New (fails too, as the rule matches the identifier) |

**L-LITERAL-SCHEMA.** It fails any of the following unless the qualifier is `${recoverySchema}`, `information_schema` or `pg_catalog`:

1. A qualified name in an object-name position. That is the name after `TABLE`, `VIEW`, `MATERIALIZED VIEW`, `SEQUENCE`, `INDEX … ON`, `TRIGGER … ON`, `FUNCTION`, `PROCEDURE`, `TYPE`, `DOMAIN`, `REFERENCES`, `FROM`, `JOIN`, `INTO`, `UPDATE`, `TRUNCATE`, `COMMENT ON <kind>` or `OWNED BY`. Quoted identifiers (`"rwb_case".t`) count.
2. A qualified type: after `::`, after `AS` inside `CAST(`, and as a column data type in a column definition.
3. A bare schema name after `SCHEMA`.
4. Inherited: `recovery.`, `ace.` or `public.` followed by an identifier anywhere in the identifier text (b), so identifiers only, including those inside dollar-quoted bodies (D-RUN-13). This is folded into the same rule ID, so the qualifier decision is made in one place (SPEC-016).

Items 1 to 4 are ways of finding a disallowed schema name. They are not separate findings: the rule reports once per (file, line, schema name), whichever items match (SPEC-004, finding multiplicity).

The position list is the minimum. The plan may extend it but not narrow it (ASM-E044-06).

This replaces the story §13 approach of matching names from `sys_objects`. That table does not exist until RWB-E1-001, and Decision Log v10 D-RCV-28 and the squad register take precedence (DG-L01).

**Consequence (DG-L09).** Under this rule, `CREATE VIEW ${recoverySchema}.v_ace_account AS … FROM public.account a` fails. That is the text that ADR v3 ADR-010, D-RCV-35 and Physical Schema v6 Section A need. This story ships the rule as D-RCV-28 defines it (orchestrator triage, logged in AI-SDLC-BUILD-LOG.md). The narrow exception is a seam owned by RWB-E1-069 (SPEC-016). No placeholder for the ACE schema is invented: Env v4 §5 says "Schema names are parameters", but no source names one.

### SPEC-RWB-E1-044-008 No foreign key outside the recovery schema (BR8)

- L-FK-OUTSIDE fails `REFERENCES <qualifier>.<table>` when the qualifier is not `${recoverySchema}`. The detail is `BR8 foreign key outside recovery schema` (S-STORY BR8; S-ADR3 ADR-010; S-D35 U4).
- An unqualified `REFERENCES` passes. It resolves to `recovery` through Flyway's default schema and the migrator's `search_path`.
- A qualified `REFERENCES <qualifier>.<table>` whose qualifier is not `${recoverySchema}` **is** reported under both rules: one L-FK-OUTSIDE finding and one L-LITERAL-SCHEMA finding, on the line of the qualifier (SPEC-004). The one exception follows from the L-LITERAL-SCHEMA allow-list: a qualifier `information_schema` or `pg_catalog` gives the L-FK-OUTSIDE finding only.
- The SPEC-016 seam exception never applies to this rule.

### SPEC-RWB-E1-044-009 GRANT and REVOKE (inherited)

- L-GRANT keeps the baseline ban (S-BS BS-2.5, BS-2.6). It now runs on the code text (SPEC-007), so a GRANT inside a comment no longer fails. It fails when GRANT or REVOKE is the first word of a line (inherited) or of a statement (new, so `SELECT 1; GRANT …` on one line is caught). The statement's first word is read as SPEC-007 view (c) states, so a leading comment never hides or supplies it.
- RWB-E1-069 v7 and Env and Deployment Design v4 §5 put grants inside a migration. Grants that name `public` also fail L-LITERAL-SCHEMA (items 3 and 4). That conflict is recorded as DG-L05 and left to RWB-E1-069 (SPEC-016, seam SEAM-E044-02).

### SPEC-RWB-E1-044-010 Lint testability and fixtures

- The lint takes a folder and returns the findings. The production test scans `src/main/resources/db/modulemigration/recovery`. The fixture tests scan folders under `backend/src/test/resources/migration-lint/`.
- Each rule in SPEC-004 has at least one failing fixture and one passing fixture. Each test asserts the exact rule ID, file and line.
- The production-folder test stays green on the empty folder (README only).
- Fixtures use synthetic table and column names and no personal data (RUN-BRIEF rule 7).

### SPEC-RWB-E1-044-011 Container proof of Flyway behaviour

**Database.**

- A new test class tagged `@Tag("recovery-it")` runs in `recoveryIntegrationTest`.
- It builds PostgreSQL `postgres:16.16-alpine` from `infra/postgres/init`, as `RecoveryDatabaseIT` does, with `RWB_LOAD_REFERENCE_SCHEMA=false`.
- Init then creates the roles (`rwb_migrator`, `recovery_svc`, `ace_view_owner`). It loads ACE schema v1 into `public`, creates an empty schema `recovery` owned by `rwb_migrator`, revokes `public` from everyone, and gives `ace_view_owner` USAGE on `public` and SELECT on its tables (`10-load-ace-database.sh`, `20-grants.sql.inc`). After this story it also gives `rwb_migrator` the two D-RUN-14 rights and nothing else in `public` (SPEC-017).
- Passwords are synthetic test values passed as container environment, as in `RecoveryDatabaseIT`.
- AC2 and AC3 need two databases, so they use two such containers.

**Flyway under test.**

- Every case builds Flyway through `RecoveryFlywayConfig#recoveryFlyway`, so the production settings are the ones tested. A Spring context does this, for example `ApplicationContextRunner` with `RecoveryFlywayConfig` and the class that registers the migration properties record (SPEC-002). Both are package-private in `casewf.migration`, so the container test class is in the test package `th.co.scb.ace.demo.recovery.casewf.migration`.
- Only `rwb.flyway.location` is set to a fixture folder under `backend/src/test/resources/flyway-fixtures/`.
- `rwb.flyway.url`, `user` and `password` select `rwb_migrator`, as in production.
- Cases that assert MSG-P3-016 or a failed start (T-044-12, T-044-13 lower-version part, T-044-14) assert on the context failure and the captured log.

**Fixtures.** Fixture names follow D-RCV-28 and use key `rwb_e1_044`. The cases are T-044-10 to T-044-18 in the Tests section.

### SPEC-RWB-E1-044-012 Drift comparison (AC2 and BR7, restated)

**Tooling.** Two test-scope parts:

- `SchemaSnapshotReader` reads one database. For schema `recovery` it lists the tables, the columns with data type and nullability, the constraints, the indexes and the views, from `information_schema` and `pg_catalog`. It maps catalog rows into a snapshot value. The mapping takes row data, so unit tests can feed it rows in memory. Only the JDBC query call needs a database.
- `SchemaComparator` is pure logic. It compares two snapshots and formats each difference as `MSG-P3-016 schema=recovery object=recovery.<table>.<column>`, or with the constraint, index or view name.

**Tests.**

- T-044-19 (unit) covers the comparison and the row mapping: added, missing and changed column, constraint, index and view, and equal snapshots.
- T-044-15 (container) applies the same fixtures to two clean databases and adds column `note_x` by hand to table `queue` in one. It asserts exactly one difference, naming `recovery.queue.note_x`.

**Not built.** There is no real-environment comparison, no read-only account and no flag `rwb.p3.migration-drift-gate` (D-RCV-05, D-RCV-44; CLAR-001 A in S-V2; SPEC-017).

### SPEC-RWB-E1-044-013 Forward only and rollback by previous tag (NFR-027)

- `clean()` is refused with Flyway's own message, and no object changes (squad register D-RCV-28 (4); DG-L11).
- A database that holds a later version than the files on the classpath (a previous tag) validates and starts, with nothing applied (`*:future` default).
- With `outOfOrder(false)`, a pending file with a lower version than the highest applied one fails validation. It is reported as in SPEC-003, with the version.

### SPEC-RWB-E1-044-014 Coverage gate (80%, no waiver) on RWB-TE-001's combined recovery bundle

**Scope (D-RUN-17; orchestrator triage on S22).** RWB-TE-001 is merged before this story. After it, `recoveryCoverageReport` and `recoveryCoverageVerification` in `backend/build.gradle.kts` measure one combined backend bundle (S-TE001 SPEC-020; its Unit Test Applicability backend row; T-TE001-10):

- every main class under `th/co/scb/ace/demo/recovery/**` (the `recoveryClasses` file set, the whole tree, untested classes included), plus
- the test-output class directory of the test-scope boundary tooling, excluding test classes, `RecoveryBoundaryTest` and fixtures (S-TE001 SPEC-020 (b));
- with one `BUNDLE` rule: LINE, INSTRUCTION, BRANCH and METHOD, each `COVEREDRATIO` at least 0.80 (S-TE001 SPEC-020 (a)). These are lines, statements, branches and functions in the gate terms (S-GATES; S-BS BS-7.2).

**What E1-044 changes in `build.gradle.kts`.** A shared file, so the plan names it (D-RCV-40). One edit only:

- Add the test-output class directory of this story's tooling package (SPEC-016) to `classDirectories` of both tasks, filtered to that package and excluding the JUnit classes (`**/*Test.class`, `**/*Test$*.class`, `**/*IT.class`, `**/*IT$*.class`) and any fixture class, in the same way RWB-TE-001 adds its own tooling. If RWB-TE-001's tooling include already takes in this package, no edit is needed. The plan states which case applies from RWB-TE-001's gated plan (its tooling include; RWB-TE-001 plan v1, not yet gated on 18 Nov 2026, includes only `th/co/scb/ace/demo/recovery/architecture/boundary/**` in `tasks.md` TASK-01, which does not take in this package). The builder's first step confirms the case against the merged `build.gradle.kts` and stops and reports on a mismatch (Dependencies; ASM-E044-19).
- No new task, no new rule, no change to a counter or threshold, and no class excluded. Execution data stays `test` (unit tests). The tasks stay outside `check` (D-RCV-28 (3), D-RCV-40), as today.
- The classes this story changes (`RecoveryFlywayConfig`, the migration properties record, any configuration class SPEC-002 adds) are in the main tree, so the bundle already measures them.
- Integration or container coverage does not replace unit coverage (S-GATES). That is why SPEC-012 splits the comparator so that unit tests reach its logic.
- **Evidence.** The implementation quotes the four bundle counters from `reports/jacoco/recoveryCoverageReport.xml`. It also quotes, for information only, the package rows of this story's tooling package and of `casewf.migration` from the same report. Those rows are not a separate gate.

**Withdrawn from v14-4.** The split into rule MAIN and rule TOOLING (orchestrator triage on S18) is replaced by the orchestrator triage on S22 (build log 2026-11-18T00:55): RWB-TE-001 SPEC-020 (b) wins, because RWB-TE-001 passed its spec gate and owns that wiring. `recoveryToolingCoverageVerification` and `recoveryToolingCoverageReport` are not built.

**If the merged build file differs from RWB-TE-001 v4 SPEC-020** (for example a counter or the tooling directory is missing), found at the builder's first step (Dependencies), the build stops and reports it to the orchestrator. It does not rebuild RWB-TE-001's wiring (ASM-E044-19).

**Baseline and sequencing (D-RUN-17; OI-E044-K closed).** The 17 Nov 2026 report `backend/build/reports/jacoco/recoveryCoverageReport.xml` totals LINE 133/415 (32.0%), BRANCH 25/92 (27.2%), INSTRUCTION 686/2174 (31.6%) and METHOD 41/135 (30.4%), from classes this story does not change. RWB-TE-001's Unit Test Applicability backend row quotes the same counts (SPEC-020 quotes no figures). D-RUN-17 settles the sequencing: E1-044's code gate runs after RWB-TE-001 is merged, and RWB-TE-001 SPEC-024 lifts the recovery main scope (RWB-TE-001 expects its own gate to pass once SPEC-024 lands).

- This story therefore writes tests for the classes it changes and for its own tooling only (Unit Test Applicability). It writes no test for a class it does not change.
- The gate stays at 80% on all four counters, with no exclusion and no waiver (orchestrator triage on S03).
- The builder's first step, before any E1-044 change, runs `recoveryCoverageReport` on the merged RWB-TE-001 code and records it as the baseline. The plan does not need that report.
- If the combined bundle is below 80% at E1-044's code gate, the implementation reports a blocker. It never excludes a class, lowers a threshold, narrows the class set or shows the gate as passing (implementation execution gates).

### SPEC-RWB-E1-044-015 Documentation and convention (audit A-19)

- **Migration-folder README.** Update `db/modulemigration/recovery/README.md`:
  - List the rule IDs in SPEC-004, the MSG-P3-016 finding format and the finding multiplicity rule.
  - Say that L-LITERAL-SCHEMA item 1 matches positions lexically, so an alias or record qualifier after `FROM` or `INTO` (for example `EXTRACT(YEAR FROM a.created_at)` or PL/pgSQL `SELECT … INTO NEW.id`) is reported. This fails closed, and a later rule change may refine it (ASM-E044-06).
  - Name the RWB-E1-069 seam (SPEC-016).
  - Reword "When RWB-E1-001 ships V0001 to V0003" so that it fixes no numbers (D-RUN-07). The `RWB_LOAD_REFERENCE_SCHEMA=false` instruction stays, tied to the merge of the baseline and the view migrations (DG-L04, DG-L07).
- **Story and plan convention.**
  - `docs/stories/RWB-E1-044/story.md` holds the story key, a link to the story v7 path and this spec, and the restated ACs.
  - `docs/stories/RWB-E1-044/plan.md` is written by the Implementation Planner.
  - Both are in the code repository (S-AGENTS §6, §7; ASM-E044-08).

### SPEC-RWB-E1-044-016 Lint structure, extension point and RWB-E1-069 seam

**Structure.**

- The lint moves out of `RecoveryMigrationLintTest` into a dedicated test-scope tooling package, for example `th.co.scb.ace.demo.recovery.architecture.migration`, beside `RecoveryMigrationLintTest` and RWB-TE-001's boundary tooling (which RWB-TE-001 puts under `recovery/architecture/`, S-TE001 Components table). It must be a package of its own, so the coverage filter of SPEC-014 can name it. Test scope is outside RWB-TE-001's module-map rule, which reads main classes only (S-TE001 SPEC-004, SPEC-011). The package name is the plan's choice. It holds tooling classes only; JUnit tests may share the package, and SPEC-014 excludes them by name.
- `MigrationLint` scans a folder and returns findings (SPEC-004, SPEC-010).
- A parsed file model holds the name, the raw lines, and the three views from the single tokenizer pass: the code text, the identifier text and the statements with their start lines (SPEC-007). The tokenizer is one class, built once per file, so every rule reads the same token boundaries. Its unterminated-token results feed L-LEX.
- Each rule ID in SPEC-004 is one implementation of a single rule interface (`ruleId()`, `check(file, folderContext)`).
- All rules are listed in **one** ordered registry. Adding a rule is one new class plus one registry entry, and no other rule changes.
- `RecoveryMigrationLintTest` stays as the JUnit entry point for the production folder and the fixtures.

**Single extension point for the qualifier decision.** L-LITERAL-SCHEMA decides whether a qualifier is allowed in one named method, for example `isAllowedQualifier(statement, qualifier)`. It gets the whole statement, so a later rule can depend on the statement kind. Today it returns true only for `${recoverySchema}`, `information_schema` and `pg_catalog`. No exception for `public` is built (orchestrator triage on S01).

**Seams (D-RUN-08). Out of scope here; owners are later stories in Build Sequence v6, except SEAM-E044-04, whose owner RWB-TE-001 is merged before this story (D-RUN-17).**

| Seam | Owner | What the owner adds | Basis |
|---|---|---|---|
| SEAM-E044-01 | RWB-E1-069 (build order 10) | A narrow exception in `isAllowedQualifier`: `public` is allowed **only** inside a `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*` statement. It never applies to L-FK-OUTSIDE or to any other statement kind. E1-069 also adds its own passing and failing fixtures | ADR v3 ADR-010, D-RCV-35 and Env v4 §5 outrank Decision Log v10 (RUN-BRIEF precedence), so the exception is legitimate when E1-069 adds it. DG-L09; OI-E044-F |
| SEAM-E044-02 | RWB-E1-069 | Resolution of the Section A grants and of two non-fix files per key. The grants are `GRANT USAGE ON SCHEMA public …`, `GRANT SELECT ON public.account, …` and the revoke from PUBLIC (Physical Schema v6 commented grant block from line 6822; Env v4 §5; D-RCV-35 U4 "the grant they need"). They hit three shipped rules, not one: L-GRANT; L-LITERAL-SCHEMA item 3 (bare `SCHEMA public`); and L-LITERAL-SCHEMA item 4 (`public.` identifiers). The two files per key hit L-KEY-DUP. SEAM-E044-01 stays as triaged and does not cover grant statements: any allowance for them is part of the OI-E044-B resolution. One route the sources already show keeps the grants on `public` out of the recovery migration: the ACE DBA applies them (RWB-ACE-001 v1 §4 flow 5; RWB-E1-069 v7 §10). E1-044 does not choose between the routes. It also does not supply the privilege that a table grant on `public` needs: the SELECT grants to `ace_view_owner` stay with the ACE DBA, and the migration account gets only the two D-RUN-14 rights (SPEC-017; DG-L13) | DG-L05; DG-L13; OI-E044-B; OI-E044-I |
| SEAM-E044-03 | None named | Job-monitor parts (SPEC-017) | D-RCV-12; DG-L10; OI-E044-G |
| SEAM-E044-04 | RWB-TE-001 (merged **before** this story, D-RUN-17; an upstream dependency now, not a later-story seam) | Nothing more. RWB-TE-001 SPEC-020 already gives `recoveryCoverageReport` / `recoveryCoverageVerification` the four counters at 0.80 (a) and one combined bundle of the whole recovery main tree plus its test-scope tooling (b); its SPEC-024 lifts the main scope. E1-044 builds on that wiring and adds only its own tooling directory to the same two tasks (SPEC-014). v14-4 said the opposite (RWB-TE-001 to add its tooling to new E1-044 TOOLING tasks). That conflicted with RWB-TE-001 SPEC-020 (b), its Unit Test Applicability backend row and T-TE001-10 (spec gate round 4, S22). The orchestrator triage on S22 ruled that RWB-TE-001 SPEC-020 (b) wins. OI-E044-H is closed | S-TE001 SPEC-020, SPEC-024, T-TE001-10; S-SQREG D-RCV-43 (2); D-RUN-17; orchestrator triage 2026-11-18T00:55 |

T-044-02 contains a **seam-marker fixture**: `CREATE VIEW ${recoverySchema}.v_ace_x AS SELECT a.id FROM public.t a`, with synthetic names. It must give L-LITERAL-SCHEMA, which shows that this story ships D-RCV-28 as written. When RWB-E1-069 adds SEAM-E044-01, it replaces this fixture with its own pass and fail fixtures. That is a rule change made by the owning story, not a weakened test.

### SPEC-RWB-E1-044-017 Out of scope, declined, and the migration-account rights for the ACE views

| Item | Basis | Owner |
|---|---|---|
| `MigrationRunRecorder`; `GET /api/recovery/v1/admin/jobs?type=MIGRATION` with version, checksum and drift result; SCR-44 migration-run display; AC8 "failed" on the job monitor; TC-E1-044-10 (RW-CASEOWN refused with MSG-P4-002); story §10 read and rerun authority for RW-PLATADM, RW-DATASTEW and RW-AUDIT | D-RCV-12 (squad register, Active): deferred "to the story that builds the job monitor". CLAR-002 A (S-V2) says the same. No story is named | **None named.** No receiving story is inferred (orchestrator triage on S02). DG-L10; OI-E044-G |
| Drift check against real SIT, UAT and PROD; read-only account; flag `rwb.p3.migration-drift-gate` | D-RCV-05 (parked); CLAR-001 A (S-V2) | Parking lot (D-RCV-05). DG-L02 |
| Deployment run by RW-PLATADM | Pipeline action outside this repository | Not applicable in this repository |
| ACE-only items: D-RCV-45 `db-migrate` guard, H2 skip, Jenkins step | No counterpart here (`README.md`, local-versus-target table) | ACE port (ASM-E044-09; OI-E044-D) |
| ACE DBA role for the recovery migration account, or any table privilege in `public` (SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER), or an `ace_view_owner` membership that inherits. RWB-E1-069 v7 §3 names RWB-E1-044 as its source ("so it can grant on schema `public` and set a view owner") | **Declined.** (1) Story RWB-E1-044 v7 §3 and §10 name only a migration account from the key store, with no DBA role. (2) ADR v3 ADR-010 Decision gives SELECT on the ACE tables to one dedicated view-owner role and SELECT on the views to the service identity; its driver is "A boundary the database enforces". (3) D-RCV-35 U3 keeps the Workbench out of ACE's DDL ("Existing ACE tables are never altered by the Workbench"), and U4 forbids a foreign key into ACE. A migration account holding the ACE DBA role could do both, and the database would no longer refuse them. (4) RWB-ACE-001 v1 (§4 flow 5; authority table), Test Cases v7 TC-ACE-001-04 and RWB-E1-069 v7 §10 give the table grants on `public` to the ACE DBA. Precedence: D-RCV-35 and ADR v3 rank above story files v7. The two narrower rights that the views do need are granted below (D-RUN-14) | The SELECT grants to `ace_view_owner` stay with the ACE DBA (D-RUN-14). Who applies the D-RUN-14 rights outside this repository: environment owner, OI-E044-I. DG-L13 |

Until an owner is named, a migration run is visible in `flyway_schema_history_recovery` and in the MSG-P3-016 ERROR line (SPEC-003).

**Migration-account rights for the ACE views (orchestrator decision D-RUN-14).** The orchestrator (Claude Code) decided D-RUN-14 on 2026-11-18T00:31, recorded in AI-SDLC-BUILD-LOG.md §1, to resolve RWB-E1-069 spec gate finding 117, which conflicted with this SPEC-017 as it stood in v14-3. This stage applies the decision. It does not make it, and no human ruling is claimed.

`rwb_migrator` gets exactly two rights for the ACE views, and no other right in `public`:

| Right | Statement (local init) | Why it is needed |
|---|---|---|
| R1 | `GRANT USAGE ON SCHEMA public TO rwb_migrator;` with **no** table privilege | The RWB-E1-069 view migration runs as `rwb_migrator` and must resolve `public.<table>` names in `CREATE VIEW ${recoverySchema}.v_ace_* AS … FROM public.<table>` |
| R2 | `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE;` (`ADMIN` stays false) | Env and Deployment Design v4 §5 (line 124): `ace_view_owner` "owns the 16 views", and the Section A migration "creates or confirms" the roles. ACE Source Views v1 grant block (line 727) transfers ownership with `ALTER VIEW … OWNER TO :ace_view_owner`. PostgreSQL 16 lets a role change an object's owner only to a role it can `SET ROLE` to, so `SET TRUE` is needed. `INHERIT FALSE` means `rwb_migrator` does not use `ace_view_owner`'s SELECT on ACE tables unless it runs `SET ROLE` |

- Still declined (table above): the ACE DBA role, SELECT or any write or `REFERENCES` on a `public` table, `CREATE` on `public`, `ADMIN` on `ace_view_owner`, and any other role membership.
- **BR8 holds in the database with these rights.** `rwb_migrator` holds no `REFERENCES` on an ACE table (R1 is USAGE only; R2 does not inherit), so an FK into `public` that names the referenced table's key is refused as `rwb_migrator` with SQLSTATE `42501` (T-044-17 (f)). With R1, PostgreSQL resolves the referenced columns before it checks the privilege, so a non-key column gives `42830` and an unknown column `42703` instead; the test therefore names the key. `ace_view_owner` holds SELECT only and does not own the recovery tables, so `SET ROLE ace_view_owner` does not allow it either.
- **Residual risk, recorded for the confirmation (OI-E044-J).** With `SET TRUE`, a recovery migration could run `SET ROLE ace_view_owner` and read ACE tables directly. No lint rule shipped here refuses `SET ROLE`. AGENTS.md §3.12 (read ACE data only through `recovery.v_ace_*` views) and code review are the control. Whether a lint rule should refuse `SET ROLE` outside the RWB-E1-069 view statements is part of OI-E044-J. A blanket ban would not work: once a view is owned by `ace_view_owner`, `rwb_migrator` (with `INHERIT FALSE`) is no longer its owner, so a later migration that changes a Section A view needs `SET ROLE ace_view_owner`.
- **Where the rights are applied.** In this repository: E1-044 adds R1 and R2 to `infra/postgres/init/20-grants.sql.inc`, after the `REVOKE ALL ON SCHEMA public FROM PUBLIC` line, as the local stand-in for the environment owner. The role comments that say only `ace_view_owner` reads ACE (`00-roles-and-databases.sh`, the `rwb_migrator` and `ace_view_owner` lines of the role list at lines 8 to 13; `20-grants.sql.inc` line 9) are reworded to say that `rwb_migrator` also holds USAGE on `public` and a non-inheriting `ace_view_owner` membership. The existing `GRANT USAGE, CREATE ON SCHEMA recovery TO ace_view_owner` (line 7), which the owner change needs, stays. They are not in a recovery migration: a GRANT fails L-GRANT (SPEC-009), and granting role membership needs a privilege that `rwb_migrator` must not hold. In SIT, UAT and PROD the environment owner applies them (OI-E044-I).
- **Confirmation.** D-RUN-14 asks the recovery tech lead to confirm. That is open-item candidate OI-E044-J. Until it is confirmed, this spec applies D-RUN-14 as the orchestrator's decision.
- **Test.** T-044-17 proves both rights exist, that `INHERIT` is false, that `rwb_migrator` holds no privilege on any `public` table, and the database refusal of an FK into `public`.

## Restated acceptance criteria (D-RCV-28 and recorded rulings applied)

| AC | Restatement used for tests | Why restated |
|---|---|---|
| AC1 | Fixture `V0001__rwb_e1_044_add_queue.sql` (line 1 `-- Story: RWB-E1-044`) applies once. Its version, as Flyway records it, and its checksum are in `flyway_schema_history_recovery`. A second migrate applies nothing | V12 and the `RWB_SCHEMA` background conflict with D-RCV-28 (DG-L01) |
| AC2 | See SPEC-012 | D-RCV-05; CLAR-001 |
| AC3 | The same fixture creates `recovery.timer` in two clean databases. The classpath resource is identical and the recorded checksums are equal | Schema fixed to `recovery` |
| AC4 | `V0001` applied, then the file changed: migrate fails validation, the ERROR `MSG-P3-016` line names that version, and the context does not start | Naming |
| AC5 | Fixture line 2 `CREATE INDEX ix_a ON recovery.queue (team_code)` gives `MSG-P3-016 … object=<file>:2 rule=L-LITERAL-SCHEMA` | Line 1 is the header under D-RCV-28 |
| AC6 | Two non-fix files with key `rwb_e1_028` give one L-KEY-DUP finding naming both files and `RWB-E1-028` | Naming |
| AC7 | `clean()` is refused with Flyway's message. A `U0001__…sql` file gives L-UNDO | Squad register D-RCV-28 (4); DG-L11 |
| AC8 | A fixture whose second statement references a missing table: the first statement's object is absent, there is no history row for that version, the ERROR `MSG-P3-016` line names the version, and the context does not start | PostgreSQL transactional DDL (CLAR-006). The job monitor is out of scope (SPEC-017) |
| AC9 | Two contexts migrate concurrently with one pending fixture: one history row for the version, and both start | Naming |

## Field matrix (configuration)

| Field | Source | Rule | Validation |
|---|---|---|---|
| `rwb.schema` | `application.yaml` | Must equal `recovery` | SPEC-002: checked when the migration properties record in `casewf.migration` binds (registered with no condition), whatever `rwb.flyway.enabled` is |
| `rwb.flyway.enabled` | `application.yaml` | Default `true`; inherited | — |
| `rwb.flyway.url` / `user` / `password` | Environment or key store | Never in the repository | BS-4.5, NFR-052 |
| `rwb.flyway.location` | `application.yaml` | `classpath:db/modulemigration/recovery`. Overridden only in container tests (SPEC-011) | Inherited |
| History table | Code constant | `flyway_schema_history_recovery` | BR6 |
| Placeholder | Code | `recoverySchema` = `rwb.schema` | Decision Log v10 D-RCV-28 |

## Status-transition matrix

| From | Event | To | Record |
|---|---|---|---|
| (no history table, non-empty schema) | First migrate | Baseline row at version 0, then `V0001` and later applied | History table (D-RCV-48; T-044-18) |
| (no history table, empty schema) | First migrate | Migrations applied, no baseline row | History table |
| Pending | Migrate succeeds | Applied (history row with checksum) | History table |
| Pending | Migrate fails part way | Pending (rolled back, no row) | ERROR log MSG-P3-016 with the version (SPEC-003) |
| Applied | File checksum changed | Validation failed; service does not start | ERROR log MSG-P3-016 with the version |

No case status changes (S-STORY §9).

## Exceptions

| ID | Condition | Behaviour | Message | Spec / Test |
|---|---|---|---|---|
| X1 | Schema difference | Comparator reports each object | MSG-P3-016 | SPEC-012 / T-044-15, T-044-19 |
| X2 | Applied file edited | Validation fails, start stops | MSG-P3-016 with the version | SPEC-003 / T-044-12 |
| X3 | Literal schema | Lint fails with file and line | MSG-P3-016 | SPEC-007 / T-044-02 |
| X4 | Duplicate or missing key | Lint fails | MSG-P3-016 | SPEC-006 / T-044-03 |
| X5 | Clean or undo | Clean refused (Flyway's message, DG-L11); undo file fails the lint | Flyway's message / MSG-P3-016 | SPEC-005, SPEC-013 / T-044-04, T-044-13 |
| X6 | Fails part way | Rollback, ERROR log, start stops | MSG-P3-016 with the version | SPEC-003 / T-044-14 |
| X7 | Two instances | One applies, the other finds nothing pending | None | SPEC-011 / T-044-16 |
| — | `rwb.schema` is not `recovery`, with Flyway enabled or disabled | Start fails with a configuration error at properties binding | None (ASM-E044-03) | SPEC-002 / T-044-08 |
| — | Search path set in any form | Lint fails | MSG-P3-016 | SPEC-007 / T-044-20 |
| — | Unterminated string, quoted identifier, block comment or dollar-quoted body | Lint fails (L-LEX); the rest of the file is still checked | MSG-P3-016 | SPEC-007 / T-044-22 |

## Tests

| Test | Level | Covers | Assertion |
|---|---|---|---|
| T-044-01 | Unit (lint fixtures) | SPEC-005 | L-NAME, L-UNDO, L-REPEATABLE, L-SEQ-DUP and L-SEQ-GAP each fail on their fixture and pass on a compliant one |
| T-044-02 | Unit | SPEC-007, SPEC-016, AC5 | Each listed position, each qualified type and a bare schema fail. `${recoverySchema}`, `information_schema`, `pg_catalog`, commented-out text and a string literal pass. A dollar-quoted body is scanned. The seam-marker view fixture fails with L-LITERAL-SCHEMA |
| T-044-03 | Unit | SPEC-006, AC6 | L-HEADER, L-HEADER-MULTI, L-KEY-DUP (both files named), L-FIX-LINE2, L-FIX-NO-BASE |
| T-044-04 | Unit | SPEC-005, AC7 | `U0001__rwb_e1_044_x.sql` gives L-UNDO |
| T-044-05 | Unit | SPEC-008, BR8 | `REFERENCES public.account(id)` gives exactly one L-FK-OUTSIDE and one L-LITERAL-SCHEMA finding on its line. `REFERENCES pg_catalog.t(id)` gives one L-FK-OUTSIDE finding only. `REFERENCES ${recoverySchema}.t(id)` and an unqualified reference pass |
| T-044-06 | Unit | SPEC-004 | Finding text format, 1-based line, all findings listed |
| T-044-07 | Unit | SPEC-010 | The production folder (README only) passes |
| T-044-08 | Unit | SPEC-002, audit A-17 | **Test configuration (every case).** `new ApplicationContextRunner().withUserConfiguration(MigrationPropertiesConfig.class, RecoveryFlywayConfig.class)`, where `MigrationPropertiesConfig` stands for the unconditional class that registers the migration properties record (SPEC-002; the real class name comes from RWB-TE-001's gated plan and is confirmed by the builder in the merged code). The test class is in `th.co.scb.ace.demo.recovery.casewf.migration`, because both configuration classes are package-private there (S-TE001 SPEC-022 Relocation table: `RecoveryFlywayConfig` to `casewf.migration`, package-private). No `application.yaml` is loaded, and no `DataSource` or `DataSourceProperties` bean exists. **No base properties.** After RWB-TE-001 SPEC-023 the migration properties record binds only `rwb.schema` and `rwb.flyway.*`. `PlatformConfig`, `RecoveryFlags` and the `rwb.p3.*` keys move to P2 `integration.flags` and are not loaded, so the `rwb.p3.temporal` and `rwb.p3.drools` base properties that v14-4 needed for `PlatformConfig.recoveryFlags` are dropped. The check reads `schema` only (SPEC-002), so an unbound nested value cannot raise a `NullPointerException` in the failing cases. Checked against RWB-TE-001 v4 SPEC-022 and SPEC-023 and against today's `RecoveryFlywayConfig.java` (`@ConditionalOnProperty`, properties as the first parameter of `recoveryFlyway`) and `PlatformConfig.java` (the `@EnableConfigurationProperties` pattern). The builder's first step re-checks it against the merged RWB-TE-001 code (ASM-E044-19). Each case adds only its own `rwb.schema` and `rwb.flyway.enabled` (case 3 through the environment instead). **Failing cases (1) to (4)** each assert: `assertThat(context).hasFailed()`; the cause chain of `context.getStartupFailure()` holds a `ConfigurationPropertiesBindException` for the migration properties record; the root cause's message names `rwb.schema`, the value found and `D-RCV-28` (root cause `BindValidationException` from the `@Validated` constraint, SPEC-002; its message holds the field error on `schema` with the rejected value and the constraint message); and the chain holds no `NullPointerException`, no `FlywayException` and no `NoSuchBeanDefinitionException`. No bean is queried in a failed context. (1) `rwb.flyway.enabled=false`, `rwb.schema=rwb_case`: the record is bound although `RecoveryFlywayConfig` is skipped, which proves the registration has no condition. (2) `rwb.flyway.enabled=true`, `rwb.schema=rwb_case`: the failure is the binding failure, before `recoveryFlyway` is built. The record is the first parameter of `recoveryFlyway` (SPEC-002), so it is bound before the `DataSource` parameter is resolved; with no `DataSource` bean in the runner, any other order would show a `NoSuchBeanDefinitionException`, which the assertion forbids. (3) The A-17 case through relaxed binding: `RWB_FLYWAY_ENABLED=false` and `RWB_SCHEMA=rwb_case`, supplied by a `withInitializer` that replaces the environment's `systemEnvironment` property source with a `SystemEnvironmentPropertySource` of the same name over a synthetic map (the real process environment is not changed, and `rwb.schema` and `rwb.flyway.enabled` are not also set as property values, which would take precedence). (4) `rwb.flyway.enabled=false`, `rwb.schema=` (blank); the message names `rwb.schema` and `D-RCV-28`. **Starting case (5)** `rwb.flyway.enabled=false`, `rwb.schema=recovery`: `assertThat(context).hasNotFailed()`; the context holds exactly one bean of the migration properties record type, and its schema is `recovery`; and no `Flyway` bean exists. The remaining combination, Flyway enabled with `recovery`, needs a database: `RecoveryDatabaseIT` and T-044-10 start it **Direct construction case (6)**, plain unit, no context: building the record in code with `schema` `rwb_case`, blank and null (nested value null) throws nothing, so code and tests that build the record directly, such as RWB-TE-001's `RecoveryFlywayConfigTest`, are unaffected by the pin (SPEC-002). RWB-TE-001's `RecoveryFlywayConfigTest` and T-TE001-12 methods stay green with at most the two changes SPEC-002 "Existing tests" allows |
| T-044-09 | Unit | SPEC-003, SPEC-001 | With Flyway mocked: a validation failure logs one ERROR `MSG-P3-016` naming the version from the validate result. A failed migration names the first pending version. A failure with no version uses `recoveryFlyway`. Each rethrows. The success path logs no error. Both data-source branches are covered |
| T-044-10 | Container | AC1 | Applies once, checksum recorded, rerun applies nothing |
| T-044-11 | Container | AC3 | Two databases; `recovery.timer` exists in both; equal checksums |
| T-044-12 | Container | AC4 | A changed file fails validation. The ERROR line names the version. The context fails |
| T-044-13 | Container | AC7, SPEC-013 | `clean()` refused, object count unchanged. Previous-tag start passes. A lower pending version fails, naming its version |
| T-044-14 | Container | AC8 | First statement rolled back, no history row, ERROR MSG-P3-016 names the version, context fails |
| T-044-15 | Container | AC2, SPEC-012 | Exactly one difference: `recovery.queue.note_x` |
| T-044-16 | Container | AC9 | Concurrent migrate from two contexts: one history row, both start |
| T-044-17 | Container | BR8, SPEC-017 (D-RUN-14) | The container is built from `infra/postgres/init` with this story's `20-grants.sql.inc` change. **Rights (as the superuser, from the catalog).** (a) R1: `has_schema_privilege('rwb_migrator', 'public', 'USAGE')` is true and `has_schema_privilege('rwb_migrator', 'public', 'CREATE')` is false. (b) R2: `pg_auth_members` holds exactly one row with `member = 'rwb_migrator'::regrole`, and it has `roleid = 'ace_view_owner'::regrole`, `inherit_option = false`, `set_option = true`, `admin_option = false`. (c) `rwb_migrator` has `rolsuper`, `rolcreaterole`, `rolcreatedb` and `rolbypassrls` all false (no DBA role). (d) No table privilege in `public`: the count of `pg_class` rows in namespace `public` with `relkind` in `r`, `p`, `v`, `m`, `f` for which `has_table_privilege('rwb_migrator', oid, 'SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER')` is true is 0. `has_table_privilege` counts inherited privileges, so 0 also shows that `INHERIT` is false in effect: `ace_view_owner`'s SELECT does not reach `rwb_migrator`. **Behaviour (connected as `rwb_migrator`).** (e) `SELECT count(*) FROM public.account` fails with SQLSTATE `42501`, without `SET ROLE`. (f) A fixture `CREATE TABLE ${recoverySchema}.fk_probe (account_id bigint REFERENCES public.account(id));`, applied through the recovery Flyway bean as `rwb_migrator`, fails in the database with exactly SQLSTATE `42501`, and no history row is written for it. The referenced column is named and is the key: `public.account` comes from ACE schema v1 loaded by init, with `id bigint not null` and `pk_account PRIMARY KEY (id)` (`infra/postgres/schema/01-ace-schema-v1.sql`: line 43, inside the `CREATE TABLE public.account` block of lines 16 to 90, and line 804). With R1 granting USAGE on `public`, PostgreSQL resolves the referenced columns before it checks the `REFERENCES` privilege, so only a key target reaches the privilege check: a non-key column would give `42830` and an unknown column `42703`. The assertion accepts `42501` only, never any error. The test fails loudly if the local grants change. **Scope:** this proves the refusal against this repository's catalog grants only. In an environment where the migration account holds a table privilege in `public` (for example the ACE DBA role that RWB-E1-069 v7 §3 assumes, declined in SPEC-017), the database would accept the FK. L-FK-OUTSIDE (T-044-05) is the control in every environment. The fixture folder is outside the lint's production scan |
| T-044-18 | Container | D-RCV-48, SPEC-001 | `recovery` made non-empty with a synthetic table and no history table, then migrate with fixture `V0001`: a baseline row at version 0 and `V0001` applied above it |
| T-044-19 | Unit | SPEC-012 | Comparator: added, missing and changed column, constraint, index and view each give one finding in the MSG-P3-016 format. Equal snapshots give none. Snapshot mapping from in-memory catalog rows |
| T-044-20 | Unit | SPEC-007, SPEC-009 | L-SEARCH-PATH fails each form in the SPEC-007 table, including `set_config('search_path', …)`. L-GRANT fails GRANT and REVOKE at line start and at statement start (`SELECT 1; GRANT …`), and passes `-- GRANT …` and `/* REVOKE … */`. A compliant file passes |
| T-044-21 | Unit | SPEC-007, SPEC-008, D-RUN-13 | **Positive (passes, no finding):** `INSERT INTO ${recoverySchema}.sys_fields (source_field) VALUES ('public.account.account_key');`, a literal with a doubled quote (`'it''s public.account'`), `E'public.branch'`, a trailing `-- reads public.account` comment and a multi-line `/* public.product */` comment. **Negative (fails):** `SELECT a.id FROM public.account a` (L-LITERAL-SCHEMA), a `"public".account` quoted identifier (L-LITERAL-SCHEMA) and `REFERENCES public.account(id)` (L-FK-OUTSIDE and L-LITERAL-SCHEMA), each reported on the right line when a literal or comment with a schema prefix is on an earlier line. All names are synthetic |
| T-044-22 | Unit | SPEC-004 (multiplicity), SPEC-007, SPEC-008, SPEC-016, D-RUN-13, orchestrator triage on S12 and S17 | Adversarial tokenizer cases in the tables below. Each case is its own fixture file in its own folder, with line 1 `-- Story: RWB-E1-044` and a valid name. The test asserts the **complete** finding list (rule, file, line), counted by the SPEC-004 multiplicity rule (one L-LITERAL-SCHEMA finding per file, line and schema name, whichever items match), so a missing or an extra finding fails. It also asserts the statement view (S1 below). All names are synthetic |

**T-044-22 cases.** Negative cases: a real `public.` reference after an opener inside another token must still be found.

| Case | Fixture text (from line 2) | Expected findings |
|---|---|---|
| N1 `'/*'` in a literal | L2 `INSERT INTO ${recoverySchema}.t (v) VALUES ('/*');` L3 `CREATE TABLE public.x (id int);` L4 `-- */` | L-LITERAL-SCHEMA at :3 |
| N2 `'--'` in a literal, code after it | L2 `INSERT INTO ${recoverySchema}.t (v) VALUES ('--'); CREATE TABLE public.x (id int);` | L-LITERAL-SCHEMA at :2 |
| N3 `''` escape before an opener | L2 `INSERT INTO ${recoverySchema}.t (v) VALUES ('it''s /*');` L3 `CREATE TABLE public.x (id int);` L4 `-- */` | L-LITERAL-SCHEMA at :3 |
| N4 `E'…'` with `\'` | L2 `INSERT INTO ${recoverySchema}.t (v) VALUES (E'\'--'); CREATE TABLE public.x (id int);`. A lexer without escape strings ends the literal at `\'` and reads the rest of the line as a comment | L-LITERAL-SCHEMA at :2 |
| N5 Quoted identifier holding `--` | L2 `CREATE TABLE ${recoverySchema}."a--b" (id int); CREATE TABLE public.x (id int);` | L-LITERAL-SCHEMA at :2 |
| N6 `--` inside a `$$` body | L2 `CREATE FUNCTION ${recoverySchema}.f() RETURNS int LANGUAGE sql AS $$ SELECT 1 -- $$; CREATE TABLE public.x (id int);`. The body ends at the second `$$` | L-LITERAL-SCHEMA at :2 |
| N7 `/*` inside a `$tag$` body | L2 `CREATE FUNCTION ${recoverySchema}.g() RETURNS int LANGUAGE sql AS $fn$ SELECT 1 /* $fn$;` L3 `CREATE TABLE public.x (id int);` L4 `-- */` | L-LITERAL-SCHEMA at :3 |
| N8 `'` left open inside a `$$` body | L2 `DO $$ BEGIN PERFORM '''; END $$;` L3 `CREATE TABLE public.x (id int);`. The body end closes the literal | L-LITERAL-SCHEMA at :3; no L-LEX |
| N9 `public.` inside a dollar body | L2 `CREATE FUNCTION ${recoverySchema}.h() RETURNS int LANGUAGE sql AS $$` L3 `-- reads the source` L4 `SELECT a.id FROM public.t a` L5 `$$;` | L-LITERAL-SCHEMA at :4 |
| N10 Placeholder is not a dollar quote | L2 `CREATE TABLE ${recoverySchema}.t (id int); CREATE TABLE public.x (id int);` | Exactly one L-LITERAL-SCHEMA at :2 (for `public.x`), none for `${recoverySchema}` |
| N11 Unterminated literal | L2 `INSERT INTO ${recoverySchema}.t (v) VALUES ('abc);` L3 `CREATE TABLE public.x (id int);` | L-LEX at :2; L-LITERAL-SCHEMA at :3 |
| N12 Unterminated block comment | L2 `/* not closed` L3 `CREATE TABLE public.x (id int);` | L-LEX at :2; L-LITERAL-SCHEMA at :3 |
| N13 Unterminated dollar body | L2 `DO $q$ BEGIN NULL; END;` L3 `CREATE TABLE public.x (id int);` | L-LEX at :2; L-LITERAL-SCHEMA at :3 |
| N14 Search path after a literal opener | L2 `INSERT INTO ${recoverySchema}.t (v) VALUES ('--'); SET search_path TO x;` | L-SEARCH-PATH at :2 |
| N15 Qualified `REFERENCES` after a `'--'` literal (new in v14-4, S17) | L2 `INSERT INTO ${recoverySchema}.t (v) VALUES ('--'); CREATE TABLE ${recoverySchema}.c (t_id int REFERENCES public.t(id));` | Exactly two: L-FK-OUTSIDE at :2 and L-LITERAL-SCHEMA at :2 (schema `public`) |

Where a case's `public.` name matches more than one L-LITERAL-SCHEMA item (`CREATE TABLE public.x` matches items 1 and 4; `FROM public.t a` in N9 matches items 1 and 4), the expected result is **one** finding, by the SPEC-004 multiplicity rule.

Statement-view case (asserted on the parsed file model, not on findings):

| Case | Fixture text (from line 2) | Expected statements |
|---|---|---|
| S1 Leading comments do not supply the statement kind (new in v14-4, S17) | L2 `/* CREATE VIEW v */ -- GRANT x` L3 `CREATE TABLE ${recoverySchema}.t (id int); INSERT INTO ${recoverySchema}.t (id) VALUES (1);` | Exactly two statements. The first starts at line 3 and its kind is `CREATE TABLE` (not `CREATE VIEW`, not `GRANT`). The second starts at line 3 with kind `INSERT`. No finding at all (no L-GRANT) |

Positive cases: no finding at all.

| Case | Fixture text (from line 2) | Why it matters |
|---|---|---|
| P1 Nested block comment | L2 `/* outer /* inner */ public.x */` L3 `SELECT 1;` | A lexer that does not count nesting ends the comment early and reports `public.x` |
| P2 String inside a dollar body | L2 `CREATE FUNCTION ${recoverySchema}.f() RETURNS text LANGUAGE sql AS $$ SELECT 'public.x' $$;` | Strings inside a body are data (D-RUN-13) |
| P3 `$` inside a string inside a body | L2 `CREATE FUNCTION ${recoverySchema}.f(p text) RETURNS boolean LANGUAGE sql AS $$ SELECT p ~ '^\d{8}$' $$;` | The pattern shape of Physical Schema v6 `ace_to_date` (line 6145): a `$` inside a string does not open or close a dollar quote, and gives no L-LEX |

`RecoveryDatabaseIT.recoveryFlywayBaselinedItsOwnHistoryTable` stays as it is. T-044-18 adds the second half of D-RCV-48 ("applies `V0001`").

**Story test cases to spec tests.**

| Story v7 §16 | Spec tests | Note |
|---|---|---|
| TC-E1-044-01 (AC1) | T-044-10 | V12 restated to the `V0001` fixture (DG-L01) |
| TC-E1-044-02 (AC2) | T-044-15, T-044-19 | SIT container restated to a container-to-container check (D-RCV-05) |
| TC-E1-044-03 (AC3) | T-044-11, T-044-08 | `RWB_SCHEMA=rwb_case` restated to `recovery` |
| TC-E1-044-04 (AC4) | T-044-12, T-044-09 | — |
| TC-E1-044-05 (AC5) | T-044-02, T-044-06 | — |
| TC-E1-044-06 (AC6) | T-044-03 | — |
| TC-E1-044-07 (AC7) | T-044-13, T-044-04 | There is no PROD profile here. Clean is disabled in every profile (inherited) |
| TC-E1-044-08 (AC8) | T-044-14, T-044-09 | The job-monitor part is out of scope (SPEC-017) |
| TC-E1-044-09 (AC9) | T-044-16 | — |
| TC-E1-044-10 (Access) | None | Out of scope, no owner named (SPEC-017; DG-L10; OI-E044-G) |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | UI In Scope NO. Story v7 §15 says "No new screen in this story". SCR-44 is out of scope (SPEC-017). No file under `frontend/` changes | — |
| Backend (main): changed classes `RecoveryFlywayConfig`, the migration properties record and any configuration class the plan adds (all in `casewf.migration`); measured over the whole recovery main scope | YES | REQUIRED | 80% LINE, INSTRUCTION, BRANCH, METHOD on the one combined backend bundle of `recoveryCoverageVerification` (RWB-TE-001 SPEC-020 (a) and (b)): every main class under `th/co/scb/ace/demo/recovery/**`, untested classes included, plus the test-scope tooling of RWB-TE-001 and of this story, from `test` execution data (SPEC-014) | SPEC-001, -002, -003, -014 | Logic added: schema pin on properties binding with unconditional registration, failure reporting with version. The main scope was below 80% on 17 Nov 2026 for classes this story does not change; RWB-TE-001 SPEC-024 lifts it before this story's code gate (D-RUN-17; SPEC-014). No class excluded, no waiver | Tests T-044-08 and T-044-09. Positive: start with `recovery`. Negative: wrong or blank schema, with `rwb.flyway.enabled` true and false. Error path: each failure kind in SPEC-003. Branch: both data sources. All four bundle counters at or above 80% |
| Backend (test-scope tooling): migration lint and schema comparator | YES | REQUIRED | Same gate: the same combined bundle of `recoveryCoverageVerification`, into which this story adds its tooling package's test-output classes, JUnit classes excluded (SPEC-014) | SPEC-004 to -010, -012, -016 | New logic: 15 rules, the one-pass tokenizer, statement split, comparison. D-RCV-40 and D-RCV-43 (2) precedent; S-TS §6; RWB-TE-001 SPEC-020 (b); orchestrator triage on S03 (no waiver) and S22 (one combined bundle). The package row of the tooling package is quoted as information (SPEC-014) | Tests T-044-01 to T-044-07 and T-044-19 to T-044-22. Every rule ID has a failing and a passing fixture. Every tokenizer state (each token kind, nesting, escapes, unterminated at end of file, body end inside a body) is reached. Boundary: line 1 versus line 2, `0001` start, empty folder. Error path: unreadable or non-`.sql` file. All four bundle counters at or above 80% |

**Verification beyond unit tests** (kept separately, S-GATES):

| Check | Level | When | Evidence |
|---|---|---|---|
| T-044-10 to T-044-18 | Container (`recoveryIntegrationTest`) | Before every MR that touches `db/modulemigration/recovery/**` or `RecoveryFlywayConfig` (D-RCV-44) | Test report attached to implementation evidence |
| `build.gradle.kts` coverage wiring | Build | `./scripts/dev.ps1 test`, then `./gradlew test recoveryCoverageVerification` (the RWB-TE-001 T-TE001-10 command) | The one `BUNDLE` rule fails below 80% on any of LINE, INSTRUCTION, BRANCH or METHOD; `recoveryCoverageReport.xml` lists this story's tooling package among the measured classes; its package row and the `casewf.migration` row are quoted as information |
| `infra/postgres/init/20-grants.sql.inc` (D-RUN-14) | Container (T-044-17) | `./scripts/dev.ps1 it` | Both migrator rights present, `INHERIT` false, no table privilege in `public`, FK into `public` refused |
| README and story/plan files | Review | Code gate | Content matches SPEC-004, SPEC-015 and SPEC-016 |

## API Change Assessment

- No endpoint is added or changed (NO_API_CHANGE).
- `GET /api/recovery/v1/admin/jobs` exists in API Specification v4 (`getAdminJobs`, `x-module: P1`, "List Workbench jobs and outbound files with status"). Its `type` parameter is a free string, and the operation does not describe migration runs.
- The migration-run part of story §12 is out of scope with no named owner (SPEC-017; DG-L10). See `contracts/backend-apis.json`.
- No backward-compatibility impact.

## Frontend Specification

N/A. UI In Scope = NO. Story v7 §15 says "No new screen in this story". The SCR-44 migration-run display is out of scope with no named owner (SPEC-017). `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`.

## Not applicable in this repository (carried to the ACE port)

The ACE-specific D-RCV-45 `db-migrate` guard, the H2 skip and the Jenkins step have no counterpart here. There is no H2, no `db-migrate` profile, no ACE core Flyway and no Jenkins (`README.md`, local-versus-target table). They are recorded as ASM-E044-09 and open-item candidate OI-E044-D.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC2, BR7, story §13 flag | Real-environment drift gate, read-only account, flag | Scope of the drift check | Settled from sources: CLAR-001 A as recorded in S-V2; D-RCV-05, D-RCV-44. Container-to-container comparison before every MR | RESOLVED | SPEC-012, SPEC-017 |
| CLAR-002 | AC8 (monitor), §10, §12 endpoint, §15, TC-E1-044-10 | Job-monitor parts: who builds them? | Deferred surfaces | Settled from sources: D-RCV-12 puts them out of this story's scope "to the story that builds the job monitor". No story is named and none is inferred (orchestrator triage on S02). DG-L10; OI-E044-G | RESOLVED (out of scope; owner open as OI-E044-G) | SPEC-017 |
| CLAR-003 | AC1–AC9 background, §12 | `RWB_SCHEMA=rwb_case`, `${schema}`, V12–V18 names versus D-RCV-28 | Test data and configuration | Precedence: Decision Log v10 D-RCV-28 over story v7. Restated in the restated-AC table | RESOLVED | SPEC-002, SPEC-011 |
| CLAR-004 | §14 MSG-P3-016 | Message text in code? | Logging and lint output | CLAR-004 A in S-V2; AGENTS §3.6: ID and parameters only | RESOLVED | SPEC-003, SPEC-004 |
| CLAR-005 | `<seq>` for this story | Which number does E1-044 take? | Production file | None. Decision Log v10 D-RCV-28 and story §13 say E1-044 ships no production migration. Numbers are assigned at merge (D-RUN-07) | RESOLVED | Change Scope Declaration |
| CLAR-006 | AC8, X6 | "History records version 17 as failed" versus PostgreSQL transactional DDL | Failure record | Assumption ASM-E044-02: the ERROR log with MSG-P3-016 and the version is the record. DG-L03 | RESOLVED (assumption) | SPEC-003 |
| CLAR-007 | AC7, X5, §14 | Message on a refused clean | Message | Squad register D-RCV-28 (4): Flyway's own message. Story v7 says MSG-P3-016: DG-L11, ASM-E044-11 | RESOLVED (assumption on register precedence) | SPEC-013 |
| CLAR-008 | Story §13 package | `recovery.casewf.migration` versus `platform.internal` | Class location | Orchestrator decision D-RUN-17: RWB-TE-001 merges first and moves `RecoveryFlywayConfig` to `casewf.migration` (S-TE001 SPEC-022). E1-044 changes it there (ASM-E044-01). The resource folder stays `db/modulemigration/recovery` (DG-L06) | RESOLVED (decision) | SPEC-001 |
| CLAR-009 | A-17 | Message for a wrong schema value; where the pin runs | Error type; Flyway-off mode | ASM-E044-03: configuration error, no message ID. The pin runs on the binding of the migration properties record in `casewf.migration`, registered by a class with no condition, so it holds with `rwb.flyway.enabled` true or false (orchestrator triage on S13; layout per D-RUN-17) | RESOLVED (assumption on the message) | SPEC-002 |
| CLAR-010 | A-19 | Story and plan file location | Convention | ASM-E044-08 | RESOLVED (assumption) | SPEC-015 |
| CLAR-011 | Coverage | INSTRUCTION and METHOD counters; test-scope tooling in the measured set; one combined bundle or one rule per class set; main-scope baseline below 80% | Gate evidence; plan test list | SPEC-014: the combined bundle of RWB-TE-001 SPEC-020 (a) and (b), four counters at 0.80, this story's tooling added to it; no waiver (orchestrator triage on S03); RWB-TE-001 SPEC-020 (b) wins over the v14-4 per-set split (orchestrator triage on S22, 2026-11-18T00:55). Baseline: orchestrator decision D-RUN-17 runs E1-044's code gate after RWB-TE-001 is merged, and RWB-TE-001 SPEC-024 lifts the main scope; this story tests only the classes it changes and its tooling. OI-E044-K is closed by D-RUN-17 | RESOLVED (decision and triage) | SPEC-014 |
| CLAR-012 | ADR-010, D-RCV-35, Env v4 §5 versus D-RCV-28 lint | How does a recovery view migration reference ACE `public`? | Lint rule L-LITERAL-SCHEMA | Ship D-RCV-28 as written. The narrow exception is a seam owned by RWB-E1-069 (orchestrator triage on S01). DG-L09; OI-E044-F | RESOLVED (seam) | SPEC-007, SPEC-016 |
| CLAR-013 | RWB-E1-069 v7 §3; story v7 §3, §10; BR8 | Does E1-044 give the migration account the ACE DBA role that RWB-E1-069 v7 §3 attributes to it? | Migrator privilege; scope of the database refusal of an FK into `public` | Settled from sources, per the orchestrator triage on S15: the ACE DBA role is declined (D-RCV-35 U3 and U4, ADR v3 ADR-010, story v7 §3 and §10, RWB-ACE-001 v1, RWB-E1-069 v7 §10; precedence puts D-RCV-35 and ADR v3 above story files v7). Amended by orchestrator decision D-RUN-14 (2026-11-18T00:31): the migration account gets exactly `USAGE ON SCHEMA public` with no table privilege and `ace_view_owner` membership `WITH INHERIT FALSE, SET TRUE`, added to the local init by this story. DG-L13; OI-E044-I; OI-E044-J (recovery tech lead to confirm) | RESOLVED (DBA role declined; two rights per D-RUN-14; route outside this repository open as OI-E044-I, confirmation as OI-E044-J) | SPEC-016, SPEC-017 |

No question was put to the user (L-RCV-03). Assumptions are in `assumptions.md`. Candidate open items are in `shared-updates.md`.

## Status

- `MCP_STATUS_SUMMARY: No Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); none is needed for a backend-only story.`
- `MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]`
- `CHANGE_CLASSIFICATION_SUMMARY: Existing Flyway bean and lint are extended; test-scope tooling added; no UI or API change.`
- `CHANGE_CLASSIFICATION_RESULT: ENHANCEMENT_LOGIC_ONLY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: baseline Flyway bean and lint exist (audit A-04); rules and checks change]`
- `REQUIREMENT_COVERAGE_SUMMARY: 28 rows: 9 ACs, 8 BRs, D-RCV-28 (1)(2), D-RUN-13, D-RCV-48, NFR-027, NFR-052, story §3/§10/§12/§14/§15/§16 lines, A-17, A-19, the ADR-010 view need and the RWB-E1-069 v7 §3 DBA-role line are mapped; job-monitor and real-environment drift parts are mapped to SPEC-017 as out of scope by D-RCV-12 and D-RCV-05; the DBA role is declined in SPEC-017 (DG-L13), and the migration account gets exactly the two D-RUN-14 rights.`
- `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 28] [COVERED_RULES: 28] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]` The count is of **unresolved** contradictions, as the planning and implementation gates read it (S-GATES). Eight source contradictions are recorded and settled; none is open, and none is a blocker. They are listed below and in `document-gaps.md`, and none of their rows is deleted or merged.

| Settled contradiction | Sources in conflict | How it was settled |
|---|---|---|
| DG-L01 | Story v7 (`RWB_SCHEMA` `rwb_case`, `${schema}`, `V12__…`) against Decision Log v10 D-RCV-28 | RUN-BRIEF precedence: Decision Log v10 over story files v7. ACs restated |
| DG-L02 | Story v7 BR7 and §13 (drift gate against real environments) against squad register D-RCV-05 and D-RCV-44 | Recorded decisions D-RCV-05 and D-RCV-44; CLAR-001 A. Container-to-container check; real-environment part out of scope |
| DG-L04 | Migration numbers fixed differently by Decision Log v10, Physical Schema v6, story files v7 and D-RCV-34 | D-RCV-28 (`<seq>` in merge order) and orchestrator decision D-RUN-07 (numbers assigned at merge). E1-044 fixes no number |
| DG-L05 | RWB-E1-069 v7, Env v4 §5 and D-RCV-35 U4 (grants and two files per key in a recovery migration) against D-RCV-28 and BS-2.5, BS-2.6 | Orchestrator triage on S01 and S14: the lint ships as D-RCV-28 defines it; resolution is seam SEAM-E044-02, owned by RWB-E1-069 (OI-E044-B) |
| DG-L09 | ADR v3 ADR-010, D-RCV-35, Env v4 §5 and Physical Schema v6 Section A (views over `public`) against the D-RCV-28 lint | Orchestrator triage on S01: ship D-RCV-28 as written; the narrow exception is seam SEAM-E044-01, owned by RWB-E1-069 (OI-E044-F) |
| DG-L11 | Story v7 X5, AC7, §14 (MSG-P3-016 for a refused clean) against squad register D-RCV-28 (4) | The register row is applied as the detail of Decision Log v10 D-RCV-28 (ASM-E044-11): Flyway's own message |
| DG-L12 | Squad register D-RCV-48 (schema `ace`) against Decision Log v10 D-RCV-28 (schema `recovery`) | Precedence: Decision Log v10 and L-RCV-07 (D-RCV-47 superseded). T-044-18 uses `recovery` |
| DG-L13 | RWB-E1-069 v7 §3 (ACE DBA role for the migration account, attributed to E1-044) against RWB-E1-044 v7 §3 and §10, RWB-E1-069 v7 §10, RWB-ACE-001 v1, ADR v3 ADR-010 and D-RCV-35 U3, U4 | Precedence (D-RCV-35 and ADR v3 over story files v7) and the orchestrator triage on S15: the DBA role is declined. Orchestrator decision D-RUN-14: exactly two narrower rights (SPEC-017) |

DG-L03 (story against tool behaviour), DG-L06, DG-L07 and DG-L08 (repository and history text) and DG-L10 (a source that is silent) are gaps, not contradictions.
- `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]`
- `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 9]` Every CLAR item (CLAR-001 to CLAR-013) is resolved. The 9 open items are the candidates in `shared-updates.md` that other owners must answer: OI-E044-A, -B, -C, -D, -E, -F, -G, -I and -J. None blocks this specification or its plan, because each is either outside this story's scope or already applied here as a recorded decision (D-RUN-14 for OI-E044-I and -J). OI-E044-H is closed by the orchestrator triage on S22, and OI-E044-K by orchestrator decision D-RUN-17.
