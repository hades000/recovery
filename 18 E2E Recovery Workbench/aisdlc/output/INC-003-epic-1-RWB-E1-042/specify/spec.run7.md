---
run_id: INC-003-epic-1-RWB-E1-042
story: RWB-E1-042
title: Central configuration service and parameter catalog
stage: specify
revision: 8 (remediation run 6, answers REVIEW-RWB-E1-042-SPEC-008 findings 149-150 and applies D-RUN-18; D-RUN-07 to D-RUN-18; rebased on RWB-TE-001 spec v4)
previous: spec.run6.md (revision 7, failed spec gate 6 on two Lows); spec.run5.md (revision 6, failed spec gate 5 on six Lows); spec.run4.md (revision 5, failed spec gate 4 on one Medium and seven Lows); spec.run3.md (revision 4); spec.run2.md (revision 3)
prepared: 2026-11-18
author: Technical Specifier (agent run)
status: SUCCESS_WITH_ASSUMPTIONS
---

# Technical Specification: RWB-E1-042 Central configuration service and parameter catalog

| Field | Value |
|---|---|
| Story | RWB-E1-042, Central configuration service and parameter catalog (Enabler, Must) |
| Epic / design module | E1 / P3 Case and workflow (story v7 header); API `x-module` P3 for the read, P4 for loads |
| RUN_ID | `INC-003-epic-1-RWB-E1-042` |
| Build order | 3 of 72, Window 1 (Build Sequence v6). Depends on RWB-E1-044 (order 1) only |
| Source requirement | Traceability Matrix row `BR-RWB-010` / `FR-RWB-010` / RWB-E1-042 (`aisdlc/requirement/Traceability_Matrix.md` lines 33 and 51) and the story file v7 [S-01]; REQ-DRI-010 (story v7 §18) |
| Code base | This repository (`<repo>`), platform baseline `751909e`, **as RWB-TE-001 (Build Sequence v6 order 2) leaves it**: the baseline modules `platform`, `rules`, `workflow`, `documents` are relocated to the 19 design modules before this story (order 3) is built (TE1S SPEC-001 (d), SPEC-022; PRE-7). Nothing from the v2 spec's ACE monorepo layout is assumed |
| Supersedes | Revision 7 (`spec.run6.md`, 18 Nov 2026), revision 6 (`spec.run5.md`, 18 Nov 2026), revision 5 (`spec.run4.md`, 18 Nov 2026), revision 4 (`spec.run3.md`, 18 Nov 2026), revision 3 (`spec.run2.md`, 17 Nov 2026) and `_v2-baseline/specify/spec.md` (16 Nov 2026). What still holds is reused; every change is mapped by finding in `gate-response.md` (Round 1: findings 101-118; Round 2: findings 119-128 and plan inputs P1-P6; Round 3: findings 129-134 and review-3 plan inputs 1-4; Round 4: findings 135-142, review-4 plan inputs 1-6, candidate RV4-DG-01; Round 5: findings 143-148, review-5 plan inputs 1-4; Round 6: findings 149-150, review-6 plan inputs 1-4, D-RUN-18) |
| Status | SUCCESS_WITH_ASSUMPTIONS: every rule is mapped; open items carry labelled assumptions (`assumptions.md`); none blocks planning |

Path abbreviations: `legacy/` is `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/`.
`aisdlc/`, `api/` and `backend/` paths are under `<repo>`. Line numbers are as read on 17 and 18 Nov 2026.
"Build log" is `<repo>/AI-SDLC-BUILD-LOG.md`. "E43S" is the RWB-E1-043 spec revision 4 (in remediation on 18 Nov 2026; the plan re-checks the revision that passes its gate, review-4 plan input 6, review-5 plan input 1) and "E44S" the
RWB-E1-044 spec, both revised in parallel with this one (S-22, S-23). "TE1S" is the RWB-TE-001 spec v4 and its
`shared-updates.md` (S-26). All Java packages below are under `th.co.scb.ace.demo.recovery`; "P3" is the design
module `casewf`, "P4" is `access`, "P2" is `integration`, "P7" is `decision` (TE1S module map).

## 1. Sources

| ID | Document (name, version, section) | Path |
|---|---|---|
| S-01 | User Stories Epic 1 Story Files v7, RWB-E1-042 | `legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-042-central-configuration-service-and-parameter-catalog-v1.md` |
| S-02 | Increment card INC-003 | `aisdlc/docs/increments/INC-003-epic-1-RWB-E1-042.md` |
| S-03 | Decision Log v10, D-RCV-28 (migration naming, `${recoverySchema}`) | `legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` line 77 |
| S-04 | Temporal and Drools Change Register v1 (D-RCV-36), §3.1 | `legacy/16-temporal-and-drools-adoption/recovery-workbench-temporal-and-drools-change-register-v1.md`; working copy `aisdlc/docs/decisions/d-rcv-36-temporal-and-drools.md` lines 78-87 |
| S-05 | Physical Schema v6 | `legacy/06-data/recovery-workbench-physical-schema-v6.sql` (parameter_catalog 1386-1409, parameter_value 1412-1434, reference_version 1437-1467, outbox_event 1206-1225) |
| S-06 | API Specification v4 | `api/recovery-api-v4.yaml` (postAdminReferenceLoads 3167, approve 3214, verify 4961, getAdminParameters 4857, rollback 5004; schemas Parameter, ReferenceLoad, RollbackRequest, Problem) |
| S-07 | Users, Roles and Permissions v4, matrix sheet | `legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v4-xlsx.md` lines 73-110 |
| S-08 | Error and Message Standard v4 | `legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` (Thai status line 19; storage line 56; message rows 68-207) |
| S-09 | RWB-E1-042 Clarification Pack, 10 Nov 2026 ("For review") | `legacy/e1-042-migration-and-clarifications/rwb-e1-042-clarification-pack.md` (same text in `<docset>/E1-042 Migration and Clarifications/`) |
| S-10 | Story files v7, RWB-E1-043 | `legacy/04-user-stories/.../rwb-e1-043-reference-data-service-with-versioned-tables-v2.md` |
| S-11 | Story files v7, RWB-E1-045 | `legacy/04-user-stories/.../rwb-e1-045-multi-product-parameters-for-mortgage-hp-and-ssme-v1.md` |
| S-12 | Build Sequence Epic 1 and Epic 2 v6 | `legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md`; working copy `aisdlc/docs/increments/build-sequence.md` |
| S-13 | Event and Messaging Design v4 | `legacy/05-technical-architecture/recovery-workbench-event-and-messaging-design-v4.md` |
| S-14 | Run decisions D-RUN-07 (migration numbers), D-RUN-08 (dependencies), D-RUN-09 (Lows fixed, not accepted), D-RUN-10 (reference-load endpoint owned by RWB-E1-043), D-RUN-11 (handler registry published by RWB-E1-043), D-RUN-12 (one creating migration per table), D-RUN-13 (schema-prefix lint ignores string literals and comments), D-RUN-15 (RWB-TE-003 stops `ApiExceptionHandler` logging raw exception text; `traceId`), D-RUN-17 (RWB-TE-001 merges before RWB-E1-044; E1-044 built on TE-001 v4's layout), D-RUN-18 (reference-load handler SPI published by P4 `access.api`; no P1 → P3 edge; P3 → P1 reads stay legal, so the §4.3 business-date seam may be filled by a P3 → P1 call; made by the orchestrator, Claude Code, pending ratification by the tech lead); orchestrator triage rows for this story, including "Gate triage (late record)" (item (f), 2026-11-18T00:09:40) | Build log §1 lines 30-36 (D-RUN-07 to -13), 38 (D-RUN-15), 40 (D-RUN-17), 41 (D-RUN-18); timeline line 243; timeline lines 91, 140, 141; `aisdlc/RUN-BRIEF.md` |
| S-15 | Phase 0 standards audit, A-01, A-03, A-04, A-06, A-08 | `aisdlc/evidence/phase0-standards-audit.md` |
| S-16 | Repository code (platform baseline) | `backend/...` paths cited inline |
| S-17 | Recovery Workbench AI engineering standards v2 | `AGENTS.md` |
| S-18 | Repository README, "Decisions taken while setting this up", items 1 and 5 | `README.md` |
| S-19 | Spec gate review `REVIEW-RWB-E1-042-SPEC-003` | `aisdlc/output/INC-003-epic-1-RWB-E1-042/review/spec-gate-review.md` |
| S-20 | v2 build pack (13-row catalog, messages CSV, 10 Nov SQL), reused as input | `aisdlc/output/INC-003-epic-1-RWB-E1-042/_v2-baseline/implement/` |
| S-21 | Spec gate review 2 `REVIEW-RWB-E1-042-SPEC-004` (findings 119-128, plan inputs P1-P6) | `aisdlc/output/INC-003-epic-1-RWB-E1-042/review/spec-gate-review-2.md` |
| S-22 | RWB-E1-043 spec revision 4, in remediation (E43S; IDs below as in revisions 2 to 4, re-checked at plan time, A-28; revision 4 also SPEC-003, SPEC-020, SPEC-025 L13, `shared-updates.md` R16, R24, GAP-51): SPEC-RWB-E1-043-003 (column definitions), -018 (flags), -025 (handler registry), -026 (PARAMETER branch), -027 (rights), -029 (catalog rows), -030 (dispatch); TC-PB-01, TC-FL-01; assumption A-26 | `aisdlc/output/INC-008-epic-1-RWB-E1-043/specify/spec.md`, `assumptions.md` (revisions 2 and 3 read 2026-11-18 00:13; revision 4 read in runs 5 and 6) |
| S-23 | RWB-E1-044 spec (E44S): SPEC-RWB-E1-044-007 (quote-aware, identifier-only schema-prefix lint, D-RUN-13), SPEC-RWB-E1-044-014 as now in force (coverage on RWB-TE-001's one combined bundle; the MAIN/TOOLING split and `recoveryToolingCoverageVerification` are withdrawn, line 375; E1-044's only Gradle edit adds its tooling package's test-output classes to `classDirectories`), SPEC-RWB-E1-044-016 (test-scope tooling package); test T-044-21 | `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/spec.md` v14-7: SPEC-007 line 227, SPEC-014 lines 359-375, SPEC-016 line 398, T-044-21 line 526 (E44S is revised in parallel; the plan re-checks) |
| S-24 | Squad decisions D-RCV-40 (JaCoCo recovery tasks "outside `check`"; test-scope tooling covered at 80%) and D-RCV-43 (2) (tooling class directory added to the recovery JaCoCo tasks) | `aisdlc/docs/decisions/INC-001-decisions.md` lines 87, 90; build log timeline line 120 |
| S-25 | Backend context: decision-log write "synchronous and blocks the action on failure (ADR-009)" (line 152); §14 items 5 and 6 (decision-log entry before the action; method check and access-log entry on every endpoint) | `aisdlc/.github/contexts/backend-context.md` lines 152, 246-247 |
| S-26 | RWB-TE-001 spec v4 (TE1S): SPEC-001 (module skeleton; baseline packages removed), SPEC-004 (module-map rule; `@NamedInterface(..., propagate = false)`), SPEC-020 (coverage, test-scope tooling class directory), SPEC-022 (relocation table; dependency direction (d)), SPEC-023 (property split), SPEC-025 (published lists); field-level matrix line 114 (`casewf` `config.api` reserved for RWB-E1-042); assumptions ASM-01, ASM-03, ASM-04, ASM-09; `shared-updates.md` SU-08 (homes for RWB-E1-042, RWB-E1-043) and SU-14 (direction rule) | `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md`, `assumptions.md`, `shared-updates.md` (as read 2026-11-18) |
| S-27 | Spec gate review 3 `REVIEW-RWB-E1-042-SPEC-005` (findings 129-134, plan inputs 1-4, gap candidates E1042-RV3-DG-01 to -03) | `aisdlc/output/INC-003-epic-1-RWB-E1-042/review/spec-gate-review-3.md` |
| S-28 | Data Classification and Personal Data Inventory v4, Fields sheet, DF-REF-156 and DF-REF-157 ("Staff identifier", personal data "Yes") | `legacy/06-data/recovery-workbench-data-classification-and-personal-data-inventory-v4-xlsx.md` lines 676-677; compare Physical Schema v6 `sys_fields` lines 4345-4346 (`is_personal` false) |
| S-29 | Spec gate review 4 `REVIEW-RWB-E1-042-SPEC-006` (findings 135-142, plan inputs 1-6, gap candidate E1042-RV4-DG-01) | `aisdlc/output/INC-003-epic-1-RWB-E1-042/review/spec-gate-review-4.md` |
| S-30 | Spec gate review 5 `REVIEW-RWB-E1-042-SPEC-007` (findings 143-148, plan inputs 1-4) | `aisdlc/output/INC-003-epic-1-RWB-E1-042/review/spec-gate-review-5.md` |
| S-31 | Spec gate review 6 `REVIEW-RWB-E1-042-SPEC-008` (findings 149-150, plan inputs 1-4) | `aisdlc/output/INC-003-epic-1-RWB-E1-042/review/spec-gate-review-6.md` |

## Change Scope Declaration

Section 2.

| Item | Value |
|---|---|
| Change Type | `NEW_STORY`. No parameter code exists in this repository: in the baseline `backend/src/main/java/.../recovery/` holds only the platform, rules, workflow and documents skeletons, which RWB-TE-001 relocates to the design modules before this story (TE1S SPEC-022 [S-26]), and the migration folder is empty [S-16]. The card's "Implemented" status describes the ACE monorepo pack, not this repository [S-02] |
| UI In Scope | NO. Story v7 §15: "No screen in this story"; SCR-39 is Epic 8 [S-01] |
| Logic In Scope | YES |
| API In Scope | YES (one endpoint: `GET /admin/parameters`) |
| API Impact Type | `NEW_API_REQUIRED` for the code base: `GET /admin/parameters` is implemented for the first time. The OpenAPI file already holds it [S-06]; this spec makes **no change** to `api/recovery-api-v4.yaml`. The three reference-load operations are **not** exposed by this story (D-RUN-10): RWB-E1-043 owns the endpoint and calls this story's published `ParameterLoadHandler` (§11.2). One new internal event is declared as a delta (§11.4) |
| Impacted Existing Nodes | Named at their homes after RWB-TE-001 (TE1S Relocation table [S-26]). **P4 `access` (additive; SU-08 (c), (d); two new published types only, CLAR-025):** new `access.api.MessageResolver` and `access.api.CapabilityCheck`; `access.api.ApiProblemException` gains an additive constructor carrying an HTTP status and a message ID (§10.2; no new type); `access.internal.ApiExceptionHandler.problem` and `access.internal.ProblemFactory` render that form (§10.2; review-3 plan input 4); new `access.internal` interim implementations (`FixedMessageCatalog`, `InterimCapabilityCheck`). **Module map** `backend/src/test/resources/architecture/recovery-modules.yaml`: `config.api` added to the `casewf` `published` list (TE1S field-level matrix line 114; SPEC-004 (d)); `access.api` is already published, and the map has no per-type field (unknown keys fail the loader, TE1S SPEC-003), so the two `access.api` types are recorded in T-TE001-14's expected set. **RWB-TE-001 test T-TE001-14 (extended, finding 136):** its expected public types gain `access.api` `MessageResolver`, `CapabilityCheck` and the `casewf.config.api` types of §12.1, and its expected `casewf` named interfaces gain `config.api`, in the same merge request; nothing is removed from the expected sets and no assertion is relaxed (TC-45). `application.yaml`, `application-local.yaml` (flag, readiness group); `backend/build.gradle.kts` (key generation task; the test-output classes of `architecture.parameters` added to `classDirectories` of RWB-TE-001's combined coverage bundle, §12.11, §14). **Not changed:** `integration.flags.api.RecoveryFlags` and its binding, the per-module property records of TE1S SPEC-023 (the flag binds by `@ConditionalOnProperty`, SU-08 (b)); `integration.internal.PlatformInfoController`; `ApiError`; the existing `ApiError` branch of `ApiExceptionHandler.problem` (its logging is RWB-TE-003's, D-RUN-15); `ApiExceptionHandler.forbidden` and the `SecurityConfig` access-denied handler (the 403 of this story is raised as an `ApiProblemException` carrying its action, SPEC-020); `RecoveryMigrationLintTest` (the new file must pass it **as RWB-E1-044 leaves it**: identifier-only, quote-aware, D-RUN-13, E44S SPEC-RWB-E1-044-007; PRE-6) |
| New Nodes Required | YES: configuration service in P3 `casewf.config` with published types in `casewf.config.api` (story v7 §13 line 237 [S-01]; SU-08 (a)); `MessageResolver` and `CapabilityCheck` with interim implementations in P4 `access` (SU-08 (d)); one migration; the catalog file; the build-check tooling and tests |
| Inherited Existing Behavior | Recovery Flyway bean with the `recoverySchema` placeholder (`RecoveryFlywayConfig`, line 37 in the baseline; `casewf.migration` after RWB-TE-001); migration lint (`RecoveryMigrationLintTest.java:25, 82-84, 94-95`); RFC 7807 Problem through `ProblemFactory` / `ApiExceptionHandler` (README decision 1; `access.internal` after RWB-TE-001); `SecurityConfig` JWT resource server with 401 `MSG-P4-001` for a caller with no RW- role; readiness probes (`application.yaml`, `management.endpoint.health.probes`); Testcontainers PostgreSQL 16 tests (`recoveryIntegrationTest`, tag `recovery-it`) [S-16] |
| Frontend Changes Required | NO |
| Backend Changes Required | YES |

## 3. User story intent interpretation

As a squad member (RW-TRIBE), I want every environment setting and business parameter read from one
configuration service and listed in a catalog with name, type, default, owner, environment and where it
is used, so that a value changes by a checked, approved, dated load and not by a release [S-01 §1, §2].

In this repository that means:

1. A catalog file in the repository is the only place a parameter is defined. The build turns it into
   typed keys, and two build checks stop literals and uncatalogued keys (BR1, BR2).
2. One migration creates (or completes) the two parameter tables and seeds the catalog and version 1 of
   every default (story §4 step 4).
3. `ParameterService` (published in `casewf.config.api`) returns a typed value with its version for a business
   date, per environment, with no restart when a new version starts (BR5, AC11).
4. `ParameterLoadHandler` (published in `casewf.config.api`) validates and applies a `PARAMETER` load, its
   approval by a different person, and its rollback (BR3, BR4). RWB-E1-043's shared reference-load
   endpoint calls it (D-RUN-10); until then nothing exposes it over HTTP.
5. Secrets are listed, never served (BR6). The service is not ready while a required parameter has no
   value and no default (BR7).
6. Work owned by later stories (the reference-load endpoint, decision log, outbox, permission matrix,
   sessions, flag table, ACE business date, message table) is reached through a named seam (§4.3).

## 4. Entry triggers and preconditions

### 4.1 Triggers

| Trigger | Actor | Path |
|---|---|---|
| Catalog change merged | Squad member through reviewed PR; owner reviews [S-01 §4 step 1] | Build (key generation, checks). A new key also needs a migration in the story that adds it |
| Deployment | Flyway (recovery bean) | Migration creates or completes tables and seeds (story §4 step 4) |
| Start-up and every readiness probe | Kubernetes / Spring Boot | `ParameterStartupCheck` (SPEC-016) |
| Value load, approval, rollback | RW-COE or RW-REFADM loads; an approver who is not the author approves; a holder of Reference data U rolls back [S-01 §3, §12] | RWB-E1-043's endpoint calls `ParameterLoadHandler` (SPEC-017). In this story: called in tests only |
| Read | Recovery code (through `ParameterService`); any role with Rules and parameters R (through `GET /admin/parameters`) | SPEC-007, SPEC-011 |

### 4.2 Preconditions (story v7 §3) and how this repository meets them

| # | Precondition [S-01 §3] | In this repository |
|---|---|---|
| PRE-1 | RWB-E1-044 done: the recovery schema exists | The recovery Flyway bean, the placeholder and the lint exist (phase0 A-04). Locally the schema is built from Physical Schema v6 when `RWB_LOAD_REFERENCE_SCHEMA=true` (README); the migration also runs on an empty schema (SPEC-001) |
| PRE-2 | `config/parameter-catalog.csv` in the repository, owned by RW-COE, with the Epic 1 entries incl. `case.entry.dpd` 90, `refdata.cache.ttl-seconds` 300, `caselist.export.maxrows` 10000 | Not present. This story adds it with the 19-row bootstrap set in §12.4 (13 rows from the 10 Nov pack [S-20] plus the six D-RCV-36 keys [S-04]). The full Epic 1 file is absent from the document set (OI-E1-042-003, CLAR-003) |
| PRE-3 | The secret store holds secrets; the catalog lists them only | Rows with `secret=true` have no default and no value row (DB check, SPEC-002); values come from the environment / Key Vault as today (`application.yaml` header comment) |
| PRE-4 | Loaders hold Reference data C (RW-COE, RW-REFADM); approvers hold Reference data A (owner; RW-RISK assumed, DL01) | Enforced on the endpoint, which is RWB-E1-043's (D-RUN-10). Users, Roles and Permissions v4 grants Reference data CRUD to RW-COE and RW-REFADM; **no role** holds Reference data A [S-07 lines 101, 107; S-06 line 3232]. Recorded as CLAR-013 for RWB-E1-043 and RWB-E1-037. This story enforces maker-checker inside the interface regardless of role |
| PRE-5 | The pipeline runs this story's checks on every PR | Both checks are JUnit tests in the `test` task, which `check` runs (SPEC-003, SPEC-004) |
| PRE-6 | (Repository precondition, not in story §3) RWB-E1-044's migration lint is merged | The seed holds module-qualified `used_by` text such as `'recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)'` (§12.4) and `COMMENT ON` text. Today's `RecoveryMigrationLintTest.java:102` strips only `--` comment lines and would flag `recovery.` inside those literals. D-RUN-13 (build log line 36) decides that the schema-prefix lint checks SQL identifiers only and ignores string literals and comments; E44S SPEC-RWB-E1-044-007 delivers that one-pass quote-aware tokenizer, proven by T-044-21. RWB-E1-044 is Build Sequence v6 order 1, before this story (order 3), so this is a dependency on an earlier story (D-RUN-08), not a seam. The seed values are **not** changed to avoid the lint. If this story's branch is cut before RWB-E1-044 merges, TC-15 fails by design and the build waits for RWB-E1-044 |
| PRE-7 | (Repository precondition, not in story §3; finding 129) RWB-TE-001 is merged: the 19 design-module packages, the module map and the relocated classes exist | RWB-TE-001 is Build Sequence v6 order 2, before this story (order 3), so its homes are an earlier-story dependency (D-RUN-08), not a seam. This spec names every class at its TE1S home: `ApiError`, `ApiProblemException` in `access.api`; `ProblemFactory`, `ApiExceptionHandler`, `SecurityConfig` in `access.internal`; `RecoveryFlags` in `integration.flags.api`; `RecoveryFlywayConfig` in `casewf.migration`; no `RecoveryProperties` (TE1S SPEC-022, SPEC-023 [S-26]). TE1S SPEC-022 (g) moves only classes of earlier-merged stories, so this story is planned directly on these homes (SU-08 (e)). If the branch is cut before RWB-TE-001 merges, the plan stops and waits |

### 4.3 Dependencies and seams (D-RUN-08, D-RUN-10)

Only RWB-E1-044 (order 1) and RWB-TE-001 (order 2) precede this story [S-12]; RWB-TE-001 provides the module
homes (PRE-7) and the dependency direction: P3 may depend on P2 and P4, never the reverse (TE1S SPEC-022 (d),
SU-14). Everything else is a seam:
this story builds the interface and, where needed, an interim implementation; the later story fills it
without changing callers.

| Later work | Owner (order) | What RWB-E1-042 builds now | How the seam is filled later |
|---|---|---|---|
| Shared reference-load endpoint (`POST /admin/reference-loads`, `/{loadId}/approve`, `/{loadId}/rollback`), dispatch by table code, capability checks C/A/U, `/verify`, LOV-REF-TABLE | RWB-E1-043 (8), D-RUN-10, D-RUN-11 | The published `ParameterLoadHandler` interface in `casewf.config.api` (load, approve, rollback, find) with all `PARAMETER` validation, versioning, maker-checker, idempotency and refusals as `ApiProblemException` (SPEC-017). **No controller** | RWB-E1-043's `PARAMETER` branch calls `ParameterLoadHandler`, maps the HTTP request to it and returns its result (E43S SPEC-RWB-E1-043-026, -030). **Handler SPI (D-RUN-18):** the reference-load handler SPI that RWB-E1-043's registry calls is published by P4 `access.api`, and P1 and P3 handlers, the `PARAMETER` handler included, implement that P4 type. RWB-E1-043 delivers the SPI (Build Sequence order 8, after this story), so this story cannot implement it now (D-RUN-08); RWB-E1-043 makes the `PARAMETER` handler implement it in P3 `casewf` (on `ParameterLoadHandlerImpl` or a P3 adapter that delegates to `ParameterLoadHandler`), which adds only a P3 → P4 edge that already exists. RWB-E1-043 extends T-TE001-14's `access.api` set for the SPI as A-41 describes. **Consumer direction (finding 141):** the caller sits in P3 (for example `casewf.refdata`, as TE1S SU-08 proposes for RWB-E1-043), never in P4: P3 already depends on P4 (`casewf.config` → `access.api`), so a P4 caller of `casewf.config.api` closes a P3↔P4 cycle that `ModulithTest` rejects (TE1S SU-08, SU-14; D-RCV-11). This matches RWB-E1-043's current triage (build log timeline line 193: its run 3 rebases on SU-08). Until RWB-E1-043 merges, nothing exposes the endpoint. **Flag-off contract (finding 119, SPEC-021):** with `rwb.p3.configservice` off the bean is absent; the consumer obtains it only through `ObjectProvider<ParameterLoadHandler>` (never constructor injection) and, when absent, refuses the `PARAMETER` code itself with a defined problem, today 404 MSG-P4-003 (E43S SPEC-018, -026; TC-PB-01) |
| Access-log entry for `GET /admin/parameters` (backend context §14 item 6 [S-25]) | RWB-E1-039 (28) | Nothing. Story v7 RWB-E1-042 asks for no access-log entry (no "access log" in the story file); the read returns no personal data (SPEC-027) and no secret (SPEC-010). The method check and its refusal are this story's (SPEC-020) | RWB-E1-039 adds the access-log entry for every endpoint, this one included, through its own filter or port; no change to this story's controller is expected |
| Decision log entry `AC-VERS` on approval (API v4 line 3233) | RWB-E1-008 (12) store, RWB-E1-027 (20) writer | `VersionDecisionRecorder`, a **non-published** port in `casewf.config`, called once per approval; interim implementation writes one structured log line with no personal data (SPEC-019) | RWB-E1-027's writer is used by a replacement implementation that also sits in `casewf.config` and calls P7's published `DecisionLogWriter` (P3 depends on P7). A P7 class implementing a P3 interface is avoided: P3 code calls P7 for decisions, so the reverse edge would close a cycle (D-RCV-11; SU-14 direction rule) |
| Outbox publication of `ParameterVersionApproved` | RWB-TE-006 (23) | In-process Spring application event after commit, plus the cache TTL (SPEC-018) | RWB-TE-006 adds the outbox write in the same transaction. Note: `outbox_event.case_seq` is nullable and `UNIQUE (case_seq, idempotency_key)` does not de-duplicate rows with null `case_seq` [S-05 1206-1225] |
| Capability check from the permission matrix; real sessions | RWB-E1-037 (27), RWB-E1-022 (26); contract lint RWB-TE-003 (5) | `CapabilityCheck` interface in P4 `access.api`, used by the method check on `GET /admin/parameters`, naming area and right; interim implementation in `access.internal` reads a grants file for Rules and parameters derived from Users, Roles and Permissions v4 (SPEC-020). P4 is its home because P4 code (`ApiExceptionHandler`, later P4 stories) and P3 code both call it, and P4 may not depend on P3 (SU-08 (d)); P4 code calls no type of `casewf.config.api` | RWB-E1-037 replaces the implementation and deletes the file. TC-E1-042-12 runs then (OI-E1-042-001) |
| Flag table with removal date | RWB-E1-047 (16) | Flag `rwb.p3.configservice`, bound by `@ConditionalOnProperty` on the conditional beans and read by `@Value` in the two always-registered beans (§12.12); no change to `RecoveryFlags` (P2) and no `RecoveryProperties`, which RWB-TE-001 removes (SPEC-021; TE1S SPEC-023; SU-08 (b)) | RWB-E1-047 moves the flag to its table |
| ACE business date (`v_ace_batch_status`) | RWB-E1-069 (10) views; read by RWB-E1-043 [S-10 line 45] | `BusinessDateProvider` interface in `casewf.config.api`; interim implementation in `casewf.config`: today's date in Asia/Bangkok (SPEC-023) | The story that reads the batch-status view replaces the implementation with one in P3 that calls the view owner's published reader in P1 (a P3 → P1 read). Under D-RUN-18 [S-14] this is allowed: the reference-load handler SPI is published by P4 `access.api`, so P1 handlers add no P1 → P3 edge and no P1 ↔ P3 cycle can form (TE1S SPEC-022 (d); D-RCV-11); story file v7 RWB-E1-028 flow step 3 plans the same kind of P3 → P1 read, as D-RUN-18 cites. No P1 → P3 edge is ever added; no class in another module implements this P3 interface. D-RUN-18 settles finding 145 and E43S R24 / GAP-51; it is pending ratification by the tech lead |
| Message table | None assigned (OI-E1-042-004) | `MessageResolver` in P4 `access.api` (called by `ApiExceptionHandler` / `ProblemFactory`, so it cannot sit in P3, SU-08 (d)) with the interim `FixedMessageCatalog` in `access.internal` holding this story's messages, EN and TH (SPEC-022) | A message-table story swaps the implementation |
| Product parameter values (PRODUCT scope) | RWB-E1-045 (31) | Catalog rows only; loads of PRODUCT keys are refused (SPEC-012) | `ProductParameterService` of RWB-E1-045 |
| Readers switching to `ParameterService` (Temporal, Drools) | RWB-E1-071 (35), RWB-E1-072 (36) | Catalog entries with value source ENV for the existing `rwb.*` properties (SPEC-024) | Those stories change their own modules' reads |

## 5. SPEC catalogue

Every SPEC item traces to `FR-RWB-010` (Traceability Matrix line 33). Tests are in §15.

| SPEC ID | Statement | Source | Tests |
|---|---|---|---|
| SPEC-RWB-E1-042-001 | Exactly one migration file `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` in `backend/src/main/resources/db/modulemigration/recovery/`; `<seq>` is the next free four-digit number at merge, assigned by the orchestrator, never fixed in this spec or the plan. Line 1 is `-- Story: RWB-E1-042`. DDL and seed are in this one file. Only `${recoverySchema}` qualifies objects; no `SET search_path`; no GRANT or REVOKE. All DDL is guarded, so it runs on an empty schema and on a schema already built from Physical Schema v6 | D-RCV-28 [S-03]; D-RUN-07, D-RUN-13 [S-14]; `RecoveryMigrationLintTest.java:25, 82-84, 94-95` as changed by E44S SPEC-RWB-E1-044-007 (PRE-6) [S-23]; story v7 §4 step 4, §13 | TC-13, TC-14, TC-15 |
| SPEC-RWB-E1-042-002 | Table shapes follow Physical Schema v6 (`id uuid` PK; `uk_parameter_catalog UNIQUE (param_key)`; `uk_parameter_value`). This story **adds** the columns `parameter_value.load_id uuid`, `content_hash char(64)` and `rollback_reason varchar(400)`; FK `fk_parameter_value_catalog`; the check constraints and indexes of §12.3. A Physical Schema update request is raised (shared-updates.md) | S-05 1386-1434, 1437-1467; story v7 §13 (FK, partial index); pack §3.7 option A; findings 104, 112 | TC-13, TC-14, TC-27 |
| SPEC-RWB-E1-042-003 | `CatalogCompletenessCheck` fails the build naming every key read in recovery main code that the catalog lacks, and every catalog row with no owner, an invalid kind, type or scope, an invalid range, or no default. The default rule exempts `scope=PRODUCT`, `secret=true` and `value_source=ENV` rows; owner, type and range are still required. It also fails a row whose `used_by` does not parse under the §7.1 grammar (entries separated by `;`, finding 130), and a `value_source=ENV` row whose `env_property` names a credential-bearing property under the credential-name rule of §7.1 (split `env_property` on `.` only; the property is refused when any segment, compared case-insensitively, contains one of the substrings `password`, `passwd`, `secret`, `token`, `credential`, `apikey`, `api-key`, `api_key`, `privatekey`, `private-key` or `private_key` (so `rwb.api-key`, `rwb.clientSecret` and `spring.datasource.Password` are refused); there is no allow-list, and a false positive is fixed by renaming the property (the credential-name rule, finding 138)): such a value is catalogued as `secret=true`, `value_source=SECRET` and never served (review-3 plan input 2) | AC3, BR2, BR6; story §13 components; OI-E1-042-007; findings 130; review-3 plan input 2; finding 138 | TC-03, TC-21, TC-41, TC-44 |
| SPEC-RWB-E1-042-004 | `RwbMagicNumberCheck` fails the build on a numeric literal other than 0, 1, -1 in recovery main code, and on a string literal equal to a non-secret catalog default; each finding names the file, the line and the catalog key(s) whose default equals the literal. Test code and generated code are excluded. Literals already in the baseline code are listed in a reviewed baseline file; an unlisted literal or a stale entry fails (ratchet) | AC2, BR1; story §13 components; finding 108 | TC-02, TC-25 |
| SPEC-RWB-E1-042-005 | A Gradle task generates `ParameterKeys` in `casewf.config.api` (one typed `ParameterKey<T>` constant per catalog row, carrying every catalog column of §7.1: kind, type, unit, range, default, scope, required, owner, environments, used by, secret flag, value source, property name, description) from the catalog file before `compileJava`, plus `all()` and `byName(String key, Class<T> type)` (returns `Optional<ParameterKey<T>>`, empty when the key is absent or its type differs; E43S A-26 needs it for the per-code keys). Code reads a value only through `ParameterService` with a generated key. **Single source of catalog metadata (finding 121):** the generated keys are the only catalog metadata any Java code reads: `ParameterService` (flag on and off), `ParameterStartupCheck`, `GET /admin/parameters`, the load checks and both build checks. `parameter_catalog` is the persisted mirror written by migrations for the FK, Physical Schema v6 and SQL consumers; no Java code reads `parameter_catalog.default_value` or any other of its columns. Drift between the two is caught by TC-27 (§12.3); drift between the catalog file and the generated keys is caught by TC-42 (§14, finding 131) | Story v7 §4 step 2, §13 `ParameterKeysGenerator`; pack §4; findings 121, 131 | TC-26, TC-27, TC-04, TC-42 |
| SPEC-RWB-E1-042-006 | The migration seeds every catalog row of §12.4 and, for every GLOBAL, non-secret, `value_source=TABLE` row with a default, one value row per listed environment: version 1, `APPROVED`, `valid_from = 2026-11-02`, author = seed identity `00000000-0000-0000-0000-0000000e1042`, approver NULL, `approved_at = now()`, `load_id` NULL. A self-check in the same file raises an exception if a required GLOBAL non-secret row with a default lacks an approved value for a listed environment | Story v7 §3, §4 step 4, §13; finding 110; assumptions A-04, A-05 | TC-01, TC-13, TC-14, TC-27 |
| SPEC-RWB-E1-042-007 | `ParameterService.get(key, businessDate)` returns `ParameterValue<T>(key, value, versionNo, validFrom, environment)` for the running environment: the `APPROVED` row for (key, environment, product group NULL) with the latest `valid_from` on or before the business date. If none is in force it returns the catalog default of the generated key (SPEC-005) with `versionNo = 0` and `validFrom = null`; with no default it throws `ParameterNotInForceException` | AC1, BR1, BR5; story §12 interface; S-08 MSG-P3-027 ("no version is in force for a table an engine needs") | TC-01, TC-11 |
| SPEC-RWB-E1-042-008 | The environment is `rwb.environment` (DEV, SIT, UAT, PROD). The same key resolves independently per environment | AC8; `application.yaml` `rwb.environment` | TC-08 |
| SPEC-RWB-E1-042-009 | Each instance caches, per (key, environment), the ordered list of approved versions; the date is resolved on read, so a version starts on its `valid_from` with no restart and no refresh. Entries expire after `config.cache.ttl-seconds` (default 60) and are rebuilt on `ParameterVersionApproved` and on a local rollback | AC11, BR5; story §4 step 8, §13 (TTL 60, DL11) | TC-11, TC-28 |
| SPEC-RWB-E1-042-010 | A `secret=true` key is never served: `ParameterService.get` throws `SecretNotServedException`; `GET /admin/parameters` lists the entry (owner, environments, used by) with `valueInForce`, `default`, `versionNo` and `validFrom` absent; no secret value is in a table, log or response | AC9, BR6, X7; story §17 | TC-09 |
| SPEC-RWB-E1-042-011 | `GET /api/recovery/v1/admin/parameters` returns the catalog with the value in force per environment (filters: key prefix, kind, owner, environment); method check Rules and parameters R through `CapabilityCheck` | Story §12; API v4 getAdminParameters | TC-09, TC-31, TC-24, TC-12 (blocked) |
| SPEC-RWB-E1-042-012 | `ParameterLoadHandler.load` takes CSV `key,environment,value` with `validFrom` and the author's user ID; every row is checked (catalog key, loadable key, environment, non-empty, type, range, no duplicate); `validFrom` is not before the business date; the load is refused whole on the first failure; on success every row is written `VALIDATED` with the next version number for its (key, environment), the author, and one `load_id` | AC5, AC6, BR3, X4, X5; story §4 step 6, §12; pack §3.3, §3.6; RWB-E1-043 X3 | TC-05, TC-06, TC-23 |
| SPEC-RWB-E1-042-013 | Idempotency key `(PARAMETER, validFrom, content_hash)`; hash = SHA-256 over the canonical rows (§12.6), stored in `parameter_value.content_hash`. An identical repeat of a load that is `VALIDATED` or `APPROVED` returns the existing load marked `repeat = true` and writes nothing (the endpoint answers 201 with the same body, OI-E1-042-011). Different content for a (key, environment) that already has an `APPROVED` version on or after `validFrom` is refused with 409 MSG-P3-027. Two concurrent identical loads: both may pass the repeat check; the second insert then violates `ux_parameter_value_version_all`. **Transaction boundary (review-3 plan input 1):** `load` does not join a caller's transaction. Its checks and inserts run in one transaction of their own (`TransactionTemplate`, `PROPAGATION_REQUIRES_NEW`), which the insert failure aborts and rolls back in PostgreSQL. The `DataIntegrityViolationException` is caught **outside** that transaction, after its rollback; the re-read by (`validFrom`, `content_hash`) then runs in a second, read-only transaction and returns the existing load with `repeat = true`; if no identical load is found it throws 409 MSG-GEN-004. No savepoint is used. A unique violation never surfaces as a 500 (plan input P3) | Story §12 idempotency; pack §3.6; RWB-E1-043 X4; E43S A-15 (same rule); plan input P3; review-3 plan input 1 | TC-16, TC-17, TC-33 |
| SPEC-RWB-E1-042-014 | `ParameterLoadHandler.approve(loadId, approverUserId)`: all rows must be `VALIDATED`; the approver must not be the author (409 MSG-P7-002, also a DB check); rows become `APPROVED` with approver and time; `valid_to` is recomputed for each affected (key, environment); one `VersionDecisionRecorder` call; one `ParameterVersionApproved` after commit; a concurrent or repeated approval gets 409 MSG-GEN-004. **Transaction rule (finding 125):** the row lock, the checks, the status change, the `valid_to` recomputation and the `VersionDecisionRecorder.recorded(...)` call run in one transaction, in that order, and the recorder is called **before commit**. Recorder implementations join the caller's transaction (`Propagation.MANDATORY`) and throw on failure. Any exception from the recorder rolls the whole approval back: the rows stay `VALIDATED` with their `version` unchanged, no event is published (the listener is `AFTER_COMMIT`) and the cache is not rebuilt. **Problem (finding 132):** the handler catches any `RuntimeException` from `recorded(...)` and throws `ApiProblemException` with MSG-P7-003, HTTP 503, no placeholders, the recorder's exception as cause; thrown inside the transaction, it rolls the approval back. API v4 lists 503 `E503` on approve, and `E503` names MSG-P7-003 for "the decision could not be recorded"; Error and Message Standard v4 line 208 defines MSG-P7-003 "Decision log write failed". `approve` runs in its own transaction (`PROPAGATION_REQUIRES_NEW`), so the result is committed when it returns | AC7, BR4, X6; story §9, §12; API v4 approve (line 3233 AC-VERS; 503 `E503`, line 6028-6029); S-08 line 208; RWB-E1-043 X5; backend context line 152 and §14 item 5 (decision-log write blocks the action on failure, ADR-009) [S-25]; findings 125, 132 | TC-07, TC-20, TC-29, TC-36, TC-38 |
| SPEC-RWB-E1-042-015 | `ParameterLoadHandler.rollback(loadId, reason, userId)`: `reason` non-blank, at most 400 characters; only an `APPROVED` load; every row must have an earlier `APPROVED` version of its (key, environment), else 409 MSG-P3-015 and nothing changes; rows become `ROLLED_BACK` with the reason; `valid_to` is recomputed so the earlier version is in force again. Only an `APPROVED` load can be rolled back (409 MSG-P3-027 otherwise, §8). `rollback` runs in its own transaction (`PROPAGATION_REQUIRES_NEW`); the local cache rebuild runs **after commit** (review-3 plan input 3, §12.8), and other instances see the rollback when their cache entry expires (`config.cache.ttl-seconds`), because no event is published for a rollback until RWB-TE-006 | AC10, X8; story §9, §12; API v4 rollback (`RollbackRequest`); review-3 plan input 3 | TC-10, TC-18, TC-19, TC-37, TC-39 |
| SPEC-RWB-E1-042-016 | `ParameterStartupCheck` is a health indicator in the readiness group. For each required GLOBAL non-secret key listed for the running environment (metadata from the generated keys, SPEC-005) it asks: TABLE source: is an `APPROVED` value **in force on the business date** from `BusinessDateProvider` (the SPEC-007 rule), or, failing that, does the generated key carry a default? ENV source: does the property resolve? It is DOWN, with MSG-P3-032 naming each failing key and the environment, when the answer is no. Orchestrator triage item (f), recorded in the build log as "Gate triage (late record)" (timeline line 140, 2026-11-18T00:09:40), requires that a seeded `valid_from` in the future never fails readiness. That holds by construction: the migration seeds value rows only for keys that have a default (SPEC-006), so the default covers any date before the seeded `valid_from`. A required key with **no** default whose only approved row is future-dated is DOWN until that row is in force, which keeps story v7 BR7 ("a value in force or a default") (finding 123) | AC4, BR7, X3; story §13; triage item (f) [S-14]; findings 110, 123 | TC-04, TC-32 |
| SPEC-RWB-E1-042-017 | `ParameterLoadHandler` is published in `casewf.config.api` (`th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadHandler`; finding 129, SU-08 (a)) with `load`, `approve`, `rollback` and `find(loadId)`, returning `ParameterLoadResult(loadId, table "PARAMETER", validFrom, status, rows, repeat)`. Refusals are thrown as `ApiProblemException` carrying the message ID, HTTP status, placeholders and field of §10.2, so the caller's controller renders them unchanged. An unknown `loadId` throws 404 MSG-P4-003 from `approve` and `rollback`; `find` returns `Optional.empty()` for it and never throws. Each method runs in its own transaction and does not join a caller's (SPEC-013, -014, -015). This story builds no controller for these operations (D-RUN-10) | Story §12 ("this story builds the PARAMETER handler"), §13 `ParameterLoadHandler`; D-RUN-10, D-RUN-11; AGENTS §3.11; findings 103(a), 129, 133 | TC-05, TC-07, TC-10, TC-23, TC-35, TC-40 |
| SPEC-RWB-E1-042-018 | Event `ParameterVersionApproved` (delta, §11.4) is published as an in-process application event after the approval commits; listeners in the same instance rebuild the cache. The outbox write is RWB-TE-006's | Story §12 event; findings 103(b), 116 | TC-28 |
| SPEC-RWB-E1-042-019 | Every approval calls `VersionDecisionRecorder.recorded(decisionCode "AC-VERS", table "PARAMETER", loadId, keys, validFrom, approverUserId)` once, inside the approval transaction before commit (SPEC-014 transaction rule); a recorder failure fails the approval with 503 MSG-P7-003 (finding 132). `VersionDecisionRecorder` is a non-published port in `casewf.config` (§4.3). The interim implementation logs one structured line without any user ID and declares `Propagation.MANDATORY`, so the later implementation (in `casewf.config`, calling RWB-E1-027's P7 `DecisionLogWriter`) writes the decision log in the same transaction. Any implementation must complete its write inside `recorded(...)` (a JPA implementation calls `flush()` there), so its failure surfaces at step 5 as MSG-P7-003 and never first at commit as an unmapped exception (review-4 plan input 5) | API v4 approve ("decision log entry with decision code AC-VERS"); backend context line 152, §14 item 5 [S-25]; findings 103(c), 125, 132 | TC-29 |
| SPEC-RWB-E1-042-020 | The endpoint this story exposes has a method check naming the capability area and right through `CapabilityCheck` (P4 `access.api`, SU-08 (d)); a refusal is 403 MSG-P4-002 with action "read parameters". `CapabilityCheck.require(authentication, area, right, action)` returns `true` when the caller holds the right and otherwise **throws** `new ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", action), null)`. Thrown from the `@PreAuthorize` expression, it is not an `AccessDeniedException`, so the existing `ApiExceptionHandler.problem` handler (`access.internal`) renders it with the action text; `ApiExceptionHandler.forbidden` and the `SecurityConfig` access-denied handler ("do this") are unchanged and still answer for any other denial. `CapabilityCheck.has(authentication, area, right)` returns a boolean with no side effect, for callers that build their own refusal (E43S SPEC-RWB-E1-043-027). The interim implementation (`access.internal`) reads `backend/src/main/resources/access/interim-capability-grants.csv` (§12.10) | AGENTS §3.3; TE1S SPEC-022, SU-08 (d) [S-26]; API v4 `x-capability`; S-07; `ApiProblemException(ApiError, Map, Throwable)`, `ApiExceptionHandler` (code as read 2026-11-18); findings 103(d), 114, 118, 120, 129 | TC-24, TC-12 (blocked) |
| SPEC-RWB-E1-042-021 | Flag `rwb.p3.configservice` (default `false`; `true` in the local profile), bound by `@ConditionalOnProperty(prefix = "rwb.p3", name = "configservice", havingValue = "true")` on this story's conditional beans and read by `@Value("${rwb.p3.configservice:false}")` in the two always-registered beans whose behaviour depends on it (`ParameterServiceImpl`, `ParameterStartupCheck`; §12.12, review-4 plan input 1) (SU-08 (b); no `RecoveryFlags` or property-record change). Off: `ParameterService` serves catalog defaults from the generated keys (`versionNo 0`) and ENV values with no database read; `GET /admin/parameters` is not registered (404); the `ParameterLoadHandler` bean is not registered and no bean of `casewf.config` depends on it, so the application context starts. **Flag-off contract with RWB-E1-043 (finding 119):** (1) consumers obtain the handler only through `ObjectProvider<ParameterLoadHandler>` (or `Optional<ParameterLoadHandler>`), never by constructor injection of the type; (2) when it is absent the consumer refuses the `PARAMETER` code and every `loadId` that only `find` could resolve, with a defined problem, which story v7 §13 "value loads are refused" requires. RWB-E1-043 owns that refusal (D-RUN-10, D-RUN-11): E43S SPEC-RWB-E1-043-026 and -018 answer **404 MSG-P4-003** ("as if the operation were absent", the D-RCV-36 flag rule) and E43S SPEC-030 sends an unresolved `loadId` to the same 404; E43S TC-PB-01 and TC-FL-01 test it. Rows already `VALIDATED` stay `VALIDATED`; nothing is written. If E43S changes the status or message in its own revision, E43S governs and this spec follows by reference (A-28). Story v7 §14 lists no message for this refusal and MSG-P4-003's text is case-oriented (gap E1042-SP-DG-10, CLAR-021) | Story §13 feature flag; story §14 [S-01]; D-RCV-36 flag rule ("endpoints return 404"); AGENTS §3.13; D-RUN-10, D-RUN-11 [S-14]; E43S [S-22]; findings 119 | TC-22 |
| SPEC-RWB-E1-042-022 | Story messages are resolved by message ID through `MessageResolver` (P4 `access.api`); the interim `FixedMessageCatalog` (`access.internal`) holds EN and TH text from Error and Message Standard v4 for the IDs in §10.3 that are not already `ApiError` constants. `ApiExceptionHandler` and `ProblemFactory` (`access.internal`) fill `messageCode`, `messageTh`, `detail` and `field` from the `ApiProblemException` this story raises; no P3 code calls `ProblemFactory` (finding 135). Both seams sit in P4 because `ProblemFactory` calls the resolver and P4 may not depend on P3 (SU-08 (d)) | AGENTS §3.6; S-08; README decision 5; pack §6.2; TE1S SPEC-022 (d), SU-08 (d) [S-26]; findings 109, 129, 135 | TC-30 |
| SPEC-RWB-E1-042-023 | The business date for the load check and for `GET /admin/parameters` comes from `BusinessDateProvider`; interim: the current date in Asia/Bangkok. `ParameterService` callers pass their own business date | Story §12 interface; RWB-E1-043 §3 line 45; `application.yaml` time zone | TC-23, TC-11 |
| SPEC-RWB-E1-042-024 | The six D-RCV-36 keys are catalog rows (§12.4). `temporal.target`, `temporal.namespace` and `drools.kiebase.cache.max` have `value_source=ENV`, naming the existing properties `rwb.temporal.target`, `rwb.temporal.namespace`, `rwb.drools.kiebase-cache-max`; their readers are unchanged in this story. `ParameterService` reads an ENV value through Spring's `Environment` by the property name in the generated key, never by importing another module's properties class (AGENTS §3.11; plan input P2) | D-RCV-36 §3.1 [S-04]; story §13 ("Environment settings come from the environment"); phase0 A-06; finding 108 | TC-26, TC-27 |
| SPEC-RWB-E1-042-025 | Errors are RFC 7807 `Problem` bodies (type, title, status, detail, messageCode, messageTh, field, traceId) as in §10.2, raised through `ApiProblemException`. A decision-recorder failure on approve is 503 MSG-P7-003 (SPEC-014; API v4 `E503`). One exception: a database outage on `GET /admin/parameters` (raised, like every other refusal, as the published `ApiProblemException`, here in its status-only form, §10.2; finding 135) answers 503 with `type`, `title` "Service Unavailable", `status` and `traceId` only, and **no** `messageCode`, because neither message API v4 `E503` names fits a failed read: MSG-GEN-006 promises the request "is queued and will be retried" and MSG-P7-003 says a decision could not be recorded (finding 126; gap E1042-SP-DG-11; CLAR-019). The API v4 `Problem` schema requires none of its fields | API v4 Problem (line 8980, no `required` list); API v4 `E503` (lines 6028-6029); README decision 1; S-08 lines 73, 208; findings 126, 132 | TC-05, TC-06, TC-07, TC-10, TC-18, TC-19, TC-23, TC-29, TC-30, TC-34 |
| SPEC-RWB-E1-042-026 | Module placement on RWB-TE-001's homes (finding 129). Implementation in P3 `th.co.scb.ace.demo.recovery.casewf.config` (package-private where possible); published types in `casewf.config.api`, declared by `package-info.java` with `@NamedInterface(name = "config.api", propagate = false)` and added as `config.api` to the `casewf` `published` list of the module map in the same merge request. `MessageResolver` and `CapabilityCheck` in P4 `access.api` (the only two new P4 types), their interim implementations in `access.internal`; the status-and-message-ID constructor of `ApiProblemException` (`access.api`) and its rendering in `ApiExceptionHandler` / `ProblemFactory` (`access.internal`) are additive P4 changes planned through `access.api`. P3 code never calls `access.internal`; callers of `casewf.config.api` sit in P3 (finding 141). Dependency direction: `casewf.config` depends on `access.api` (P3 → P4), which TE1S already has (`casewf.admin` → `access.api`); no P4 type refers to a P3 type. Other modules use only `casewf.config.api` and `access.api` | Story v7 §13 line 237 [S-01]; TE1S SPEC-001, -004 (d), (e), -022 (d), -025, field-level matrix line 114, SU-08 (a)-(e), SU-14 [S-26]; AGENTS §3.11, §7; D-RCV-11 | Existing `ModulithTest`, `RecoveryBoundaryTest`; T-TE001-14 with its expected sets extended (TC-45) |
| SPEC-RWB-E1-042-027 | No personal data in seed, fixtures, tests or logs: synthetic UUIDs only; no names or IDs in logs; no secret value anywhere. Author, approver and rollback-caller user IDs, and the `created_by` / `updated_by` audit columns of `parameter_catalog` and `parameter_value`, are **personal data** (staff identifiers). For the audit columns the Inventory v4 has no row; its classification of the same columns on other tables (personal "Yes") is applied, the protective reading (gap E1042-SP-DG-17, candidate RV4-DG-01). For author and approver: Personal Data Inventory v4 classifies DF-REF-156 and DF-REF-157 as "Staff identifier", personal "Yes" [S-28], while Physical Schema v6 `sys_fields` carries `is_personal` false for both; the protective reading is applied (gap E1042-SP-DG-15). Consequences here: they are stored only in `parameter_value` (and, for `created_by` / `updated_by`, `parameter_catalog`) and passed only to `VersionDecisionRecorder` (the decision log); they appear in no log line, event payload, exception text, `ParameterLoadResult` or `GET /admin/parameters` response; test UUIDs are synthetic. Display as a name and retention (DL26) are outside this story | Story §17; AGENTS §4.7; S-28; S-05 lines 4345-4346; findings RV3-DG-03, RV4-DG-01, 137 | TC-09, TC-28, TC-29, TC-30, code review |

## Requirement-to-SPEC Logic Coverage

Section 6.

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every changeable business value is a versioned parameter row, never a constant | 004, 005, 006, 007 | DIRECT | Literal check, generated keys, seeded version 1 | COVERED |
| BR2 | Every parameter in use has a catalog entry with owner, type, default, environments, used by | 003, 005 | DIRECT | PRODUCT, secret and ENV rows are exempt from the default rule only; `used_by` is required and parsed by the `;` grammar of §7.1 (finding 130) | COVERED |
| BR3 | A business value changes only through a checked, approved, dated load | 012, 013, 014, 015 | DIRECT | The seed is the reviewed-PR baseline, not a change (A-05) | COVERED |
| BR4 | Author cannot approve; Risk approves where a threshold or limit moves | 014 | DIRECT | Author rule in service and DB. Who holds Reference data A is decided on RWB-E1-043's endpoint and RWB-E1-037's matrix (CLAR-013) | COVERED |
| BR5 | Open decisions keep their version; new decisions use the version in force | 007, 009 | DIRECT | Every read returns `versionNo`; callers record it | COVERED |
| BR6 | Secrets listed in the catalog, held only in the secret store | 010, 002, 003 | DIRECT | `ck_parameter_catalog_secret_default`; no value rows for secrets; an ENV row may not point at a credential-bearing property (review-3 plan input 2) | COVERED |
| BR7 | A service does not start without every required parameter for its environment | 016 | DIRECT | Readiness DOWN, no traffic (AC4 wording); value in force on the business date, else the default (finding 123) | COVERED |
| AC1 | `case.entry.dpd` = 90 PROD v1; read on 2026-12-01 gives 90 and version 1 | 006, 007 | DIRECT | Seed v1 from 2026-11-02. Recording version 1 in the entry decision is the case service's (RWB-E1-018) | COVERED |
| AC2 | Literal 90 in `recovery.casewf.casecreation` fails the build naming file, line, `case.entry.dpd` | 004 | DIRECT | Fixture module (story §13 build step 7) | COVERED |
| AC3 | Code reading `allocation.retry.limit` not in the catalog fails the build naming it; every other key in use is catalogued with owner and default | 003 | DIRECT | Fixture module | COVERED |
| AC4 | Required `refdata.cache.ttl-seconds` with no value and no default in UAT: health fails with MSG-P3-032 naming key and UAT; no traffic | 016, 022 | DIRECT | Readiness group | COVERED |
| AC5 | Load `case.entry.dpd` = 400 PROD refused with MSG-GEN-002 min 1 max 365 | 012, 025 | DIRECT | 422 through the interface | COVERED |
| AC6 | Load "ninety" refused with MSG-P1-002, check "value is not INTEGER" | 012, 025 | DIRECT | 422 through the interface | COVERED |
| AC7 | U-41 loaded version 3 and approves it: refused MSG-P7-002 | 014 | DIRECT | 409; DB check as second guard | COVERED |
| AC8 | `refdata.cache.ttl-seconds` 30 in SIT, 300 in PROD; each environment reads its own | 008, 012, 014 | DIRECT | Table values for an ENVIRONMENT-kind key (CLAR-014) | COVERED |
| AC9 | `ace.db.password` listed with owner, environments, used by; no value returned | 010, 011 | DIRECT | | COVERED |
| AC10 | Version 2 in force, version 1 before it; rollback of v2 makes v1 in force, 90 | 015 | DIRECT | | COVERED |
| AC11 | v2 = 91 PROD from 2026-12-10 approved 2026-12-05: 90 on 12-09, 91 on 12-10, no restart | 007, 009, 014 | DIRECT | Date resolved on read | COVERED |
| X1 | Literal business value: build fails naming file, line, parameter | 004 | DIRECT | | COVERED |
| X2 | Uncatalogued key: build fails naming it | 003 | DIRECT | | COVERED |
| X3 | Required value missing at start-up: not started; health names key; MSG-P3-032 | 016 | DIRECT | "Not started" read as readiness DOWN per AC4 (CLAR-012) | COVERED |
| X4 | Out of range: load refused in full, MSG-GEN-002 | 012 | DIRECT | | COVERED |
| X5 | Wrong type: load refused in full, MSG-P1-002 | 012 | DIRECT | | COVERED |
| X6 | Approver is author: refused, MSG-P7-002 | 014 | DIRECT | | COVERED |
| X7 | Secret asked for through the catalog read: no value | 010 | DIRECT | | COVERED |
| X8 | Rollback: previous version in force; MSG-P3-015 when none | 015 | DIRECT | | COVERED |
| X9 | Role without Rules and parameters R reads the catalog: 403 MSG-P4-002 | 011, 020 | DIRECT | TC-12 Blocked until RWB-E1-022 and RWB-E1-037 (OI-E1-042-001); seam test TC-24 does not close it | COVERED |
| X10 | Version approved before its valid from: current value stays until then; no restart | 009, 014 | DIRECT | | COVERED |
| FL1 | Squad member adds a catalog row through a PR reviewed by the owner | 003, 005 | INHERITED_EXISTING_BEHAVIOR | Merge review (AGENTS §8); CODEOWNERS is RWB-TE-002 | COVERED |
| FL2 | Build generates `ParameterKeys`; code reads only through `ParameterService` | 005, 007 | DIRECT | | COVERED |
| FL3 | Build runs the magic-number and completeness checks | 003, 004 | DIRECT | | COVERED |
| FL4 | Flyway loads catalog rows and defaults | 001, 006 | DIRECT | | COVERED |
| FL5 | RW-COE loads a value version through reference-loads, table PARAMETER | 012, 017, 021 | DIRECT | HTTP path is RWB-E1-043's endpoint calling `ParameterLoadHandler` (D-RUN-10); flag off: refused by that endpoint, 404 MSG-P4-003 (SPEC-021 contract) | COVERED |
| FL6 | Load checks key, type, range, environment, required values; refuse whole | 012 | DIRECT | "Required values": a blank value is refused (MSG-GEN-001) | COVERED |
| FL7 | Owner approves; refused if approver is author | 014 | DIRECT | | COVERED |
| FL8 | New value from valid from; every instance refreshes on the event or after the TTL | 009, 018 | DIRECT | Cross-instance refresh relies on the TTL until RWB-TE-006 | COVERED |
| FL9 | Engines read with version number and record it in decision inputs | 007 | DIRECT | Recording belongs to the engines' stories | COVERED |
| FL10 | Any role with Rules and parameters R reads the catalog through GET | 011, 020 | DIRECT | | COVERED |
| PRE1-PRE5 | Story §3 preconditions | §4.2 | DIRECT | | COVERED |
| ST1 | None -> Load (all checks pass) -> VALIDATED | 012 | DIRECT | | COVERED |
| ST2 | VALIDATED -> Approve (approver is not author) -> APPROVED, in force from valid from | 014 | DIRECT | | COVERED |
| ST3 | APPROVED -> Rollback (earlier approved version exists) -> ROLLED_BACK | 015 | DIRECT | | COVERED |
| AUTH | Story §10 authority (RW-COE, RW-RISK, RW-PLATADM, RW-TRIBE, readers, RW-PHONECOL) plus RW-REFADM as loader (§3) | 020, 014, §16 | DIRECT | Load/approve/rollback rights are checked on RWB-E1-043's endpoint | COVERED |
| CON1 | GET /admin/parameters contract | 011 | DIRECT | | COVERED |
| CON2 | POST reference-loads PARAMETER contract incl. idempotency | 012, 013, 017 | DIRECT | Through the published interface | COVERED |
| CON3 | Approve and rollback contracts | 014, 015, 017, 025 | DIRECT | Through the published interface; approve 503 `E503` with MSG-P7-003 on a recorder failure (finding 132) | COVERED |
| CON4 | Event ParameterVersionApproved | 018 | DIRECT | Payload delta §11.4 | COVERED |
| CON5 | Published interface `ParameterService`, `ParameterValue`, `ParameterKeys` | 005, 007, 026 | DIRECT | `recovery.casewf.config.api`, as story v7 §13 names it, on RWB-TE-001's module homes (A-01, finding 129) | COVERED |
| MSG | Story §14 messages (7) plus MSG-P4-001 | 022, 025 | DIRECT | §10.3 | COVERED |
| GR1 | No business value in code | 004 | DIRECT | | COVERED |
| GR2 | No personal data; no secret value in tables, logs, responses | 010, 027 | DIRECT | Author and approver IDs are personal (Inventory v4 DF-REF-156, -157; protective reading, gap E1042-SP-DG-15): stored and passed to the decision log only | COVERED |
| GR3 | No read of another module's tables; values only through ParameterService | 026 | INHERITED_EXISTING_BEHAVIOR | Modulith verification and the boundary test with RWB-TE-001's module map (TC-45) | COVERED |
| GR4 | A value change needs no deployment; a new parameter needs a reviewed catalog entry | 009, 012, 003 | DIRECT | | COVERED |

## 7. Field-level behavior matrix

### 7.1 Catalog file `backend/src/main/resources/config/parameter-catalog.csv` (build time; changed by PR only)

Header: `key,kind,value_type,unit,min_value,max_value,default_value,scope,required,owner_role,environments,used_by,secret,value_source,env_property,description`.
The first 13 columns and `description` are the 10 Nov pack header [S-20]; `value_source` and
`env_property` are added (story §6, "catalog columns ... can be tuned"; story §13 environment settings; A-03).

| Column | Constraint (checked by `CatalogCompletenessCheck`) | Maps to |
|---|---|---|
| key | Required, unique, `^[A-Za-z][A-Za-z0-9_.-]{0,99}$` | `param_key` |
| kind | `BUSINESS` or `ENVIRONMENT` | `kind` |
| value_type | STRING, INTEGER, DECIMAL, BOOLEAN, DATE, TIME, DURATION, CODE, CODE_LIST or JSON | `value_type` |
| unit | Optional, max 20 | `unit` |
| min_value, max_value | Optional; when present they parse as `value_type`; min <= max | `min_value`, `max_value` |
| default_value | Required except when scope=PRODUCT, secret=true or value_source=ENV; parses and lies in range; empty when secret=true | `default_value` |
| scope | `GLOBAL` or `PRODUCT` | `scope` |
| required | `true` or `false` | `required` |
| owner_role | Required; an RW- role code of Users, Roles and Permissions v4 | `owner_role` |
| environments | Comma list of DEV, SIT, UAT, PROD | `environments` |
| used_by | Required (BR2). One or more entries separated by `;` (finding 130). Each entry is trimmed, non-empty, at most 100 characters and contains no `;` and no line break; the whole field is at most 400 characters. `;` is chosen because no seeded value contains it, while seeded values do contain `,` (`recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)`) and spaces; the pack's comma lists are rewritten with `;` in §12.4. `a;;b`, a leading or trailing `;` or a blank field fail the check | `used_by` (stored as written) |
| secret | `true` or `false`; `true` requires value_source=SECRET | `secret` |
| value_source | `TABLE`, `ENV` or `SECRET` | Generated key only (not a DB column) |
| env_property | Required when value_source=ENV: the Spring property; empty otherwise. Credential-name rule: split `env_property` on `.` only; the property is refused when any segment, compared case-insensitively, contains one of the substrings `password`, `passwd`, `secret`, `token`, `credential`, `apikey`, `api-key`, `api_key`, `privatekey`, `private-key` or `private_key` (so `rwb.api-key`, `rwb.clientSecret` and `spring.datasource.Password` are refused); there is no allow-list, and a false positive is fixed by renaming the property (the credential-name rule, finding 138). Such a value is catalogued `secret=true`, `value_source=SECRET` (review-3 plan input 2) | Generated key only |
| description | Required, max 400 | `description` |

### 7.2 `parameter_catalog`

All columns as Physical Schema v6 lines 1386-1409; written by migrations only, never at run time.
`created_by` of seeded rows = seed identity (a synthetic system UUID, not a person). Editable through the API: none.
`created_by` and `updated_by` are treated as personal data (SPEC-027; gap E1042-SP-DG-17).

### 7.3 `parameter_value`

| Field | On load | On approve | On rollback | Constraint |
|---|---|---|---|---|
| id | `gen_random_uuid()` | | | PK (v6) |
| param_key | CSV `key` | | | FK to `parameter_catalog.param_key` (added) |
| environment | CSV `environment` | | | DEV, SIT, UAT, PROD (check added) |
| param_value | CSV `value`, trimmed | | | NOT NULL, max 400 |
| product_group | NULL (PARAMETER loads are GLOBAL) | | | |
| version_no | max(version_no) of (key, environment, product_group NULL) + 1, over all statuses | | | >= 1; unique with `ux_parameter_value_version_all` |
| valid_from | `validFrom` | | | |
| valid_to | NULL | recomputed (§12.7) | recomputed | NULL or >= valid_from |
| status | `VALIDATED` | `APPROVED` | `ROLLED_BACK` | LOV-VERSION-STATUS values (DF-REF-155) |
| author_user_id | author user ID passed by the caller (the JWT `sub` on RWB-E1-043's endpoint) | | | NOT NULL; personal data (staff identifier, Inventory v4 DF-REF-156; SPEC-027) |
| approver_user_id | NULL | approver user ID | | NULL or <> author (check added); personal data (Inventory v4 DF-REF-157; SPEC-027) |
| approved_at | NULL | `now()` | unchanged | required when APPROVED |
| load_id (added) | one new UUID per load, on every row | | | indexed; NULL only for seeded rows |
| content_hash (added) | SHA-256 hex of the load (§12.6), on every row | | | NULL exactly when load_id is NULL |
| rollback_reason (added) | NULL | | `reason` | required when ROLLED_BACK |
| created_at | default `now()` (seed rows: the migration time) | unchanged | unchanged | NOT NULL default (v6) |
| created_by | the author user ID (the same value as `author_user_id`); seed rows: the seed identity `00000000-0000-0000-0000-0000000e1042` | unchanged | unchanged | personal data, protective reading (SPEC-027, E1042-SP-DG-17) |
| is_active | default `true`, on every row incl. seed rows | unchanged | unchanged | never changed and never read by this story; "in force" comes only from `status` and the dates (SPEC-007, §8) |
| state | NULL | NULL | NULL | unused by this story (`status` is the lifecycle column) |
| version, updated_at, updated_by | defaults | +1, now, approver | +1, now, caller | optimistic lock on `version`; `updated_by` (and `created_by`) personal data, protective reading (SPEC-027, E1042-SP-DG-17) |

### 7.4 `ParameterLoadHandler` inputs (what RWB-E1-043's endpoint passes)

| Input | Required | Rule | Refusal |
|---|---|---|---|
| file content | Yes | UTF-8 CSV per RFC 4180 (a field holding a comma, quote or line break is quoted, as CODE_LIST values such as `servicelevel.required-statuses` need), parsed by the same CSV reader as the catalog file; header exactly `key,environment,value`, at least one data row (review-4 plan input 4) | 422 MSG-GEN-001 `{field}=file` (missing or no rows); 422 MSG-P1-002 `{check}="file is not a CSV with header key,environment,value"` |
| validFrom | Yes | date, not before the business date (equal allowed) | 422 MSG-GEN-001 `{field}=validFrom`; 422 MSG-P3-027 `{check}="valid from is before the business date"` |
| author user ID | Yes | UUID | programming error (`IllegalArgumentException`) |
| loadId (approve, rollback) | Yes | UUID of a PARAMETER load | 404 MSG-P4-003 |
| approver user ID / caller user ID | Yes | UUID | programming error |
| reason (rollback) | Yes | non-blank, at most 400 characters after trim | 422 MSG-GEN-001 `{field}=reason` |

The generic P4 fields `changeRequestRef`, `impactSummary` and `rollbackPlan` (API v4 description of
postAdminReferenceLoads) are not inputs for `PARAMETER`; storing them is RWB-E2-041's (change checklist).

### 7.5 Outputs

- `ParameterLoadResult`: `loadId`, `table` = `PARAMETER`, `validFrom`, `status` (VALIDATED, APPROVED or
  ROLLED_BACK; all rows of a load share it), `rows` = number of value rows, `repeat` (true for an identical
  repeat). It maps one to one onto API v4 `ReferenceLoad` (`id`, `table`, `validFrom`, `status`, `rows`).
- `Parameter` (GET): `key`, `kind`, `type`, `unit`, `min`, `max`, `default`, `scope`, `required`, `owner`,
  `environments[]`, `usedBy[]` (the `used_by` entries split on `;` and trimmed, §7.1), `secret`, `valueInForce`, `versionNo`, `validFrom`. Catalog
  fields come from the generated keys and value fields from `parameter_value` (SPEC-005: one source). For the
  requested environment (query `environment`, else `rwb.environment`) and the business date: TABLE rows give
  the value in force (or the default with `versionNo 0`); ENV rows give the property value only when the
  requested environment is the running one, else absent; PRODUCT rows and secrets have `valueInForce`,
  `versionNo` and `validFrom` absent; secrets also have `default` absent. No author or approver ID is returned
  (SPEC-027).

## 8. Status-transition matrix

| Source status | Event | Condition | Target status | Side effects |
|---|---|---|---|---|
| (none) | Load | every check passes | VALIDATED | rows written with one `load_id` |
| (none) | Load | any check fails | (nothing written) | refusal 409 or 422 |
| any | Approve or rollback | unknown `loadId` | (nothing changed) | 404 MSG-P4-003 |
| (none) | Load | identical repeat of a VALIDATED or APPROVED load | (unchanged) | existing load, `repeat = true` |
| VALIDATED | Approve | approver is not the author; no APPROVED row of the same (key, environment) has `valid_from` >= this load's; `validFrom` not before the business date | APPROVED | `valid_to` recomputed; decision recorder; event after commit; local cache rebuilt |
| VALIDATED | Approve | approver is the author | VALIDATED | 409 MSG-P7-002 |
| VALIDATED | Approve | checks pass but the decision recorder fails | VALIDATED (rolled back) | 503 MSG-P7-003; no event; no cache rebuild |
| VALIDATED | Approve | `validFrom` now before the business date, or an approved version exists on or after it | VALIDATED | 409 MSG-P3-027 |
| APPROVED or ROLLED_BACK | Approve | any | unchanged | 409 MSG-GEN-004 |
| APPROVED | Rollback | every row has an earlier APPROVED version | ROLLED_BACK | `rollback_reason`; `valid_to` recomputed; local cache rebuilt |
| APPROVED | Rollback | some row has no earlier APPROVED version | APPROVED | 409 MSG-P3-015 |
| VALIDATED or ROLLED_BACK | Rollback | any | unchanged | 409 MSG-P3-027 `{check}="only an approved load can be rolled back"` |

Story v7 §9 defines VALIDATED, APPROVED and ROLLED_BACK only. IN_FORCE, SUPERSEDED and REFUSED stay allowed
by the check constraint (DF-REF-155) but are never written here; "in force" is derived from the dates.

## 9. Exceptional-case behavior

| ID | Case | Behavior | Message |
|---|---|---|---|
| X1 | Literal business value in recovery main code | `test` fails; output `path:line: literal <v> matches catalog key <key>` | build output |
| X2 | Key read but not catalogued | `test` fails naming the key and the reading file | build output |
| X3 | Required value missing for the environment | readiness DOWN; details list key and environment | MSG-P3-032 |
| X4 | Value out of range | 422, whole load refused | MSG-GEN-002 `{field}=<key>`, `{min}`, `{max}` |
| X5 | Wrong type; unknown key; key not loadable (secret, PRODUCT, ENV); environment not listed; duplicate row; bad file | 422, whole load refused | MSG-P1-002 `{source}=PARAMETER`, `{date}=<validFrom>`, `{check}` (§12.5) |
| X6 | Approver is the author | 409 | MSG-P7-002 |
| X7 | Secret read | `SecretNotServedException`; GET omits values | none |
| X8 | Rollback with no earlier version | 409, nothing changes | MSG-P3-015 `{table}=PARAMETER` |
| X9 | Caller lacks Rules and parameters R on GET | 403 | MSG-P4-002 `{action}="read parameters"` |
| X10 | Approved before valid from | old value stays until `valid_from`; no restart | none |
| E1 | Empty file, missing input, blank value | 422 | MSG-GEN-001 `{field}` |
| E2 | `validFrom` before the business date | 422 | MSG-P3-027 `{table}=PARAMETER` |
| E3 | Different content where an approved version exists on or after `validFrom` | 409 | MSG-P3-027 |
| E4 | Concurrent or repeated approval | 409 | MSG-GEN-004 |
| E5 | Rollback reason missing, blank or over 400 characters after trim (400 accepted, 401 refused) | 422 | MSG-GEN-001 `{field}=reason` |
| E6 | Unknown `loadId` on approve or rollback (including the `id` of a seeded row, which has no load); `find` returns empty | 404 | MSG-P4-003 (existing `ApiError.NOT_IN_SCOPE`; text is case-oriented, CLAR-021) |
| E7 | Database unavailable on GET (`DataAccessResourceFailureException` or `CannotCreateTransactionException` from the read) | 503, status-only Problem (SPEC-025); no retry is promised or made | none: neither message of API v4 `E503` fits a read: MSG-GEN-006 says the request "is queued and will be retried", MSG-P7-003 is about a decision not recorded (gap E1042-SP-DG-11, CLAR-019) |
| E8 | Nothing in force and no default (caller read) | `ParameterNotInForceException` to the caller | MSG-P3-027 if surfaced over HTTP |
| E9 | No token or no RW- role on GET | 401 (existing `SecurityConfig`) | MSG-P4-001 |
| E10 | Flag off: a `PARAMETER` load, approve or rollback reaches RWB-E1-043's endpoint | Refused by RWB-E1-043 (SPEC-021 contract); nothing written | 404 MSG-P4-003 (E43S SPEC-018, -026; wording gap E1042-SP-DG-10) |
| E11 | Decision recorder fails during approval (any `RuntimeException`) | Approval rolled back; rows stay `VALIDATED` with `version` unchanged; no event; no cache rebuild (SPEC-014) | 503 MSG-P7-003 (API v4 `E503`; Standard v4 line 208; finding 132) |
| E12 | Two identical loads at the same time | One load; the second gets it with `repeat = true` (SPEC-013) | none; 409 MSG-GEN-004 if no identical load is found on re-read |

## 10. Messages and problem mapping

### 10.1 Resolution

`MessageResolver` has two methods, `english(messageId, placeholders)` and `thai(messageId, placeholders)`, each returning a `String`, so it adds no further type to `access.api`. Interim implementation
`FixedMessageCatalog` holds the IDs in §10.3. Thai text status: "Proposed": the business lead drafts and
Legal and Compliance approve (DL10) [S-08 line 19]. Where the 10 Nov pack's Thai differs from the Standard
(MSG-P4-001), the Standard v4 text is used. The Standard says messages are "held in the message table"
[S-08 line 56], and that table does not exist (OI-E1-042-004). Platform messages already in `ApiError`
(MSG-P4-001, -002, -003, MSG-P3-036) stay there (README decision 5).

### 10.2 Problem mapping

`ApiProblemException` (published, `access.api`; TE1S SPEC-022 relocation, SPEC-025 published list, its unit
tests TE1S SPEC-024) gains one additive constructor carrying the HTTP status and the message ID:
`ApiProblemException(HttpStatus status, String messageId, Map<String, String> placeholders, String field, String detail, Throwable cause)`,
with accessors `status()`, `messageId()`, `field()`, `detail()`; `error()` returns null for this form, and the existing
`ApiError` constructor is unchanged. Guards (review-5 plan input 2): `status` is required; `messageId` may be null
only when `status` is 503, and then `placeholders` must be empty and `field` and `detail` null (the status-only
503 of E7); otherwise the constructor throws `IllegalArgumentException`. `detail` is optional (finding 144): when
set, the handler renders it as the Problem `detail` in place of the resolver's EN text, so RWB-E1-043 can return
its multi-failure `detail` (E43S revision 4 SPEC-003, SPEC-025 L13: every failure's text joined by "; ", capped
at 100 with the total; the producer applies the cap) without a further P4 change. This story always passes
`detail` null (its loads refuse on the first failure, §12.5). At plan time the planner lists every caller of
`error()` (today only `ApiExceptionHandler.problem`) so that none dereferences it for this form. The exception's
own message is the message ID (or `"status-only 503"`), never user input. P3 code raises it and never calls
`ProblemFactory`, which stays package-private in `access.internal` (finding 135). `access.internal.ApiExceptionHandler`
turns it into the Problem response; this needs no change to RWB-TE-001. `ParameterLoadHandler` and the parameter
catalog controller throw it, so RWB-E1-043's endpoint renders it with no mapping of its own. HTTP statuses in
this code are `HttpStatus` constants, never numeric literals (plan input P1).

**E7.** The parameter catalog controller (`casewf.config`) catches `DataAccessResourceFailureException` and
`CannotCreateTransactionException` from the read and throws
`new ApiProblemException(HttpStatus.SERVICE_UNAVAILABLE, null, Map.of(), null, null, cause)`. Any other
`DataAccessException` on the read is not caught here and reaches the inherited `unexpected` handler (500), whose
logging RWB-TE-003 fixes under D-RUN-15; this is accepted as inherited behaviour (review-5 plan input 3).

**Handler path (review-3 plan input 4; findings 135, 137).** `ApiExceptionHandler.problem` keeps its existing
branch when `ex.error()` is not null. When `ex.error()` is null it calls `ProblemFactory` (same package):
- with a message ID: `type` `urn:rwb:problem:<id>`, `title` (reason phrase), `status`, `detail` (`ex.detail()`
  when set, else EN from `MessageResolver`), `messageCode`, `messageTh`, `field` when set, `traceId`;
- without a message ID: status-only Problem, `type` `urn:rwb:problem:unavailable`, `title`, `status`,
  `traceId`; no `messageCode` and no `detail` (SPEC-025, CLAR-019).

**Logging of the new branch (finding 137; D-RUN-15).** One WARN line with the message ID (or `none`), the
status, the `traceId` and the cause's class name, plus the fixed safe text "cause suppressed". It never logs
the cause's message, its stack trace, the placeholders, the field value or the `detail` override, and no personal data (SPEC-027); a
cause may echo row values (for example a database constraint detail with a user ID). The existing `ApiError`
branch is not changed here; removing raw exception text from it is RWB-TE-003's (D-RUN-15, Build Sequence
order 5), and this story raises no `ApiError` exception with a cause. RWB-TE-003 is told (`shared-updates.md`) that
`problem` has this second branch, that `error()` is null for it, and that its logging already meets D-RUN-15. TC-30
(unit, in `access.internal`) covers the rendering of every form and the handler's log line; TC-34 (MockMvc, so the
handler runs) asserts the E7 Problem and that the driver exception's message is absent from the captured log.
TC-29 (b) calls the bean directly, so it asserts the exception's fields and that no line logged by
`casewf.config` code holds the cause's message (finding 146).

| Status | When | messageCode | field |
|---|---|---|---|
| 401 | no token or no RW- role on GET (existing) | MSG-P4-001 | |
| 403 | GET refused by `CapabilityCheck` | MSG-P4-002, `{action}="read parameters"` | |
| 404 | unknown `loadId` on approve or rollback | MSG-P4-003 | |
| 409 | author approves; concurrent approval; no earlier version; content conflict or approval after `validFrom`; rollback of a non-approved load | MSG-P7-002; MSG-GEN-004; MSG-P3-015; MSG-P3-027; MSG-P3-027 | |
| 422 | load and rollback validation | MSG-GEN-001, MSG-GEN-002, MSG-P1-002, MSG-P3-027 | the failing input or key |
| 503 | decision recorder fails during approval (E11) | MSG-P7-003 | |
| 503 | database unavailable on GET (E7) | none (status-only Problem, SPEC-025; CLAR-019) | |

### 10.3 Message catalogue for this story (EN and TH from Error and Message Standard v4)

| ID | Used for | Placeholders | Standard v4 line |
|---|---|---|---|
| MSG-P3-032 | readiness: required parameter missing | name, environment | 156 |
| MSG-GEN-002 | value out of range | field, min, max | 69 |
| MSG-P1-002 | load refused at a check | source, date, check | 76 |
| MSG-GEN-001 | required input empty | field | 68 |
| MSG-P7-002 | approver is the author | none | 207 |
| MSG-P3-015 | no earlier version to roll back to | table | 139 |
| MSG-P3-027 | reference-data load check failed; nothing in force | table, check | 151 |
| MSG-GEN-004 | concurrent change | none | 71 |
| MSG-P7-003 | approval not taken: the decision could not be recorded (E11; API v4 `E503`) | none | 208 |
| MSG-P4-001 | 401 (added; missing from story §14) | none | 163 (existing `ApiError.NO_ROLE`) |
| MSG-P4-002 | 403 | action | 164 (existing `ApiError.NOT_PERMITTED`) |
| MSG-P4-003 | 404 unknown `loadId` (from this story's interface); 404 flag-off refusal (raised by RWB-E1-043, E10) | none | 165 (existing `ApiError.NOT_IN_SCOPE`; case-oriented text, CLAR-021) |

API v4 `components/responses/E503` (lines 6028-6029) names MSG-P7-003 and MSG-GEN-006. MSG-P7-003 is used
for the approve 503 (E11), the case the API names it for (finding 132). MSG-GEN-006 (Standard v4 line 73,
"System of record unavailable") is **not** used: its text promises that the request "is queued and will be
retried", and neither a failed approval nor a failed `GET /admin/parameters` is queued or retried here
(finding 126; the conflict between the API's `E503` list and the message text is recorded with both citations
in gap E1042-SP-DG-11, Blocker = No, and the API's MSG-P7-003 is followed). No message in Standard v4 fits a
failed synchronous read (MSG-P3-036 names the workflow service only). The 503 therefore
carries no message ID until the message owner adds one (gap E1042-SP-DG-11, CLAR-019 OPEN with the message
owner); when it is added, it goes into `FixedMessageCatalog` and the E7 handler, with no other change.

The `{check}` and `{action}` fills are English in `messageTh` too; that is the known A-08 gap owned by
RWB-TE-003 and is not widened here.

## 11. API change assessment

### 11.1 Endpoint exposed by this story (already in API Specification v4; base path `/api/recovery/v1`)

| Method and path | operationId | Capability (x-capability) | Success | Errors | Consumer |
|---|---|---|---|---|---|
| GET `/admin/parameters` | getAdminParameters | Rules and parameters, R | 200 `Parameter[]` | 401, 403, 503 | Backend-only in this story (screen SCR-39 is Epic 8) |

### 11.2 Operations served through the published interface, exposed by RWB-E1-043 (D-RUN-10)

| API v4 operation | Capability | Endpoint owner | `ParameterLoadHandler` method | Result -> response |
|---|---|---|---|---|
| POST `/admin/reference-loads` (table `PARAMETER`) | Reference data, C | RWB-E1-043 | `load(content, validFrom, authorUserId)` | `ParameterLoadResult` -> 201 `ReferenceLoad` (also for an identical repeat) |
| POST `/admin/reference-loads/{loadId}/approve` | Reference data, A | RWB-E1-043 | `approve(loadId, approverUserId)` | -> 200 `ReferenceLoad` |
| POST `/admin/reference-loads/{loadId}/rollback` | Reference data, U | RWB-E1-043 | `rollback(loadId, reason, userId)` | -> 200 `ReferenceLoad` |
| (lookup for dispatch by `loadId`) | — | RWB-E1-043 | `find(loadId)` | `Optional<ParameterLoadResult>` |

The capability checks (C, A, U), the multipart parsing and the HTTP status of success are the endpoint's.
Every refusal comes from the interface as an `ApiProblemException` (§10.2). Until RWB-E1-043 merges these
operations are not reachable over HTTP; this story tests them through the interface (§15). With
`rwb.p3.configservice` off the interface is absent and RWB-E1-043 refuses the operations itself (SPEC-021
contract: `ObjectProvider`, 404 MSG-P4-003 per E43S SPEC-018 and -026).

### 11.3 Contract deltas

| Delta | Kind | Action |
|---|---|---|
| None to `api/recovery-api-v4.yaml` | — | No regeneration of `frontend/src/api/schema.d.ts` |
| Identical repeat load answers 201 with the existing body; 409 only for conflicting content | Behaviour the OpenAPI leaves open | OI-E1-042-011 stays open; API owner to record it (shared-updates.md) |
| `required: [file, table, validFrom]`, `format: date`, LOV on `table` | Hardening the OpenAPI lacks | Enforced in the interface; OpenAPI change requested (OI-E1-042-011) |
| Rollback 422 = empty reason (MSG-GEN-001) | Behaviour | Recorded |
| Unknown `loadId` uses MSG-P4-003 | Behaviour | CLAR-021 |
| New published module interface `ParameterLoadHandler`, `th.co.scb.ace.demo.recovery.casewf.config.api` (finding 129) | Internal Java contract | Consumed by RWB-E1-043 (D-RUN-10), which imports it from that package (shared-updates.md) |
| Approve answers 503 `E503` with MSG-P7-003 when the decision cannot be recorded | Behaviour in API v4 (approve lists 503 `E503`) | RWB-E1-043 renders the interface's `ApiProblemException` unchanged (finding 132) |

Backward compatibility: all additive. No existing response changes; `/platform/info` is not changed (the flag
binds by `@ConditionalOnProperty` and is not added to `RecoveryFlags`, SU-08 (b)).

### 11.4 Internal event (delta)

`ParameterVersionApproved` (`casewf.config.api`) is new and absent from Event and Messaging Design v4 [S-13].
Producer: P3 `casewf.config` (approval). Consumer now: the parameter cache of the same instance. Later: the outbox
(RWB-TE-006) and every instance.

| Field | Type | Story v7 §12 | Note |
|---|---|---|---|
| loadId | uuid | added | identifies the load |
| paramKeys | string[] | yes | |
| validFrom | date | yes | |
| versions | `[{paramKey, environment, versionNo}]` | replaces `versionNo` | one load can carry several keys and environments with different version numbers, so one `versionNo` cannot describe it |
| occurredAt | timestamp | added | |

No personal data and no approver ID in the payload. Event catalog update requested (shared-updates.md).

## 12. Backend Specification

### 12.1 Module placement (SPEC-026)

Story v7 §13 names package `recovery.casewf.config`, published types in `recovery.casewf.config.api` and build
checks in `build-tools/rwb-checks` [S-01 line 237]. RWB-TE-001 (order 2, merged before this story, PRE-7)
creates the `casewf` module (P3) and reserves `config.api` for this story (TE1S field-level matrix line 114;
SU-08 (a) [S-26]). Revision 4 placed the service in the baseline `platform` module, which RWB-TE-001 removes;
revision 5 follows the story and RWB-TE-001 (finding 129). Every package below is under
`th.co.scb.ace.demo.recovery`.

| Package | Module | Visibility | Types |
|---|---|---|---|
| `casewf.config.api` | P3 `casewf` | Published: `package-info.java` with `@NamedInterface(name = "config.api", propagate = false)` (TE1S SPEC-004 (d)); `config.api` added to the `casewf` `published` list of `backend/src/test/resources/architecture/recovery-modules.yaml` in the same merge request | `ParameterService`, `ParameterKey<T>`, `ParameterKeys` (generated), `ParameterValue<T>`, `CatalogEntry`, `ParameterNotInForceException`, `SecretNotServedException`, `ParameterLoadHandler`, `ParameterLoadResult`, `ParameterVersionApproved`, `BusinessDateProvider` |
| `casewf.config` | P3 `casewf` | Internal; package-private where possible (no public type directly in the module base package is affected: `casewf.config` is a sub-package, TE1S SPEC-004 (e)) | `ParameterServiceImpl`, `ParameterLoadHandlerImpl`, repositories, load checks, the parameter catalog controller, cache, `ParameterStartupCheck` (health indicator), `CatalogSource` (over `ParameterKeys.all()`), `VersionDecisionRecorder` (non-published port) and its interim implementation, the interim `BusinessDateProvider`, the named schema-limit constants (§12.11) |
| `access.api` | P4 `access` | Published (exists after RWB-TE-001) | Added (the only two new P4 types): `MessageResolver`, `CapabilityCheck`; changed: `ApiProblemException` (additive status-and-message-ID constructor with optional `detail`, §10.2). `ApiError` unchanged |
| `access.internal` | P4 `access` | Internal | Added: `FixedMessageCatalog` (`MessageResolver`), `InterimCapabilityCheck` (grants file); changed: `ApiExceptionHandler.problem` and `ProblemFactory` (rendering and logging of the new form, §10.2). Package-private as TE1S leaves them; called by no P3 code |

Dependency direction (TE1S SPEC-022 (d), SU-14; D-RCV-11): `casewf.config` → `access.api` (P3 → P4, the
edge `casewf.admin` → `access.api` already has) and → `integration.flags.api` only if a later change needs
it (none here). No P4 type refers to a P3 type; nothing outside `casewf` uses `casewf.config` internals.
Other modules read values only through `casewf.config.api` (GR3). The P4 additions are the ones SU-08 (c) and
(d) plan through `access.api`, so the plan touches P3 and P4; AGENTS §7 sends such a plan back to the analyst before any code is written, which is recorded as an open item (CLAR-025, gap E1042-SP-DG-16) and not presumed approved. Callers of `casewf.config.api` sit in P3; P4 code may call no type of it (finding 141). The build checks
stay in `backend/src/test` (not a separate `build-tools/rwb-checks` project), because that is where TE1S keeps
the boundary and lint tests and a new Gradle project is a new build module (A-01).

### 12.2 Published interfaces

Story v7 §12 signatures, unchanged:

```java
// package th.co.scb.ace.demo.recovery.casewf.config.api
public interface ParameterService {
    <T> ParameterValue<T> get(ParameterKey<T> key, LocalDate businessDate);
    <T> ParameterValue<T> get(ParameterKey<T> key, String productGroup, LocalDate businessDate);
    CatalogEntry entry(String key);
}
public record ParameterValue<T>(String key, T value, int versionNo, LocalDate validFrom, String environment) {}
```

Added for D-RUN-10 (story §13 component `ParameterLoadHandler`, "approve and rollback"):

```java
// package th.co.scb.ace.demo.recovery.casewf.config.api  (location published under D-RUN-10; RWB-E1-043 imports it from here)
public interface ParameterLoadHandler {
    String TABLE = "PARAMETER";
    ParameterLoadResult load(InputStream csv, LocalDate validFrom, UUID authorUserId);
    ParameterLoadResult approve(UUID loadId, UUID approverUserId);
    ParameterLoadResult rollback(UUID loadId, String reason, UUID userId);
    Optional<ParameterLoadResult> find(UUID loadId);
}
public record ParameterLoadResult(UUID loadId, String table, LocalDate validFrom, String status, int rows, boolean repeat) {}
```

Seams and generated keys (findings 119, 120, 121, 125; E43S A-26):

```java
// ParameterKeys is generated into casewf.config.api from the catalog file (SPEC-005); it is the only catalog
// metadata Java code reads. Members: one `public static final ParameterKey<T>` constant per catalog row, and
//   public static List<ParameterKey<?>> all()
//   public static <T> Optional<ParameterKey<T>> byName(String key, Class<T> type)   // empty if absent or other type

// package th.co.scb.ace.demo.recovery.access.api  (P4; SU-08 (d))
public interface MessageResolver {
    String english(String messageId, Map<String, String> placeholders);
    String thai(String messageId, Map<String, String> placeholders);
}
// ApiProblemException (existing, access.api) gains:
//   public ApiProblemException(HttpStatus status, String messageId, Map<String, String> placeholders, String field, String detail, Throwable cause)
//   public HttpStatus status(); public String messageId(); public String field(); public String detail();   // error() is null for this form
public interface CapabilityCheck {
    boolean has(Authentication authentication, String area, String right);
    /** true, or throws ApiProblemException(ApiError.NOT_PERMITTED, {action}) */
    boolean require(Authentication authentication, String area, String right, String action);
}
// package th.co.scb.ace.demo.recovery.casewf.config  (not published; §4.3)
interface VersionDecisionRecorder {
    /** Called inside the approval transaction, before commit; implementations use Propagation.MANDATORY and throw on failure. */
    void recorded(String decisionCode, String table, UUID loadId, List<String> keys, LocalDate validFrom, UUID approverUserId);
}
```

`approverUserId` is personal data (SPEC-027); the recorder passes it to the decision log only, and the interim
implementation does not log it.

`ParameterLoadHandlerImpl` is a conditional bean (`@ConditionalOnProperty(prefix = "rwb.p3", name = "configservice", havingValue = "true")`); every other type
above is registered whatever the flag. Consumers inject `ObjectProvider<ParameterLoadHandler>` (SPEC-021).

- The product-group overload of `get` resolves a row for (key, environment, productGroup) first, then the
  GLOBAL row; this story writes no product-group rows. A `scope=PRODUCT` key throws
  `ParameterNotInForceException` (its values are RWB-E1-045's `ProductParameterService`).
- ENV-sourced keys return the converted property value, read through Spring's `Environment` by the property
  name in the generated key (plan input P2), `versionNo 0`, `validFrom null`.
- Type conversion: INTEGER `Integer`, DECIMAL `BigDecimal`, BOOLEAN `Boolean` (`true`/`false`), DATE
  `LocalDate` (ISO), TIME `LocalTime` (`HH:mm`), DURATION `Duration` (ISO-8601), STRING, CODE and JSON
  `String`, CODE_LIST `List<String>` (comma-separated, trimmed).

### 12.3 Migration (SPEC-001, SPEC-002)

File `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, adapted from the 10 Nov pack SQL [S-20]: renamed;
header cites Physical Schema v6, D-RCV-28 and this spec; `V0042` removed. Statements in order:

1. `CREATE TABLE IF NOT EXISTS ${recoverySchema}.parameter_catalog` and `parameter_value`, columns exactly
   as Physical Schema v6.
2. `ALTER TABLE ${recoverySchema}.parameter_value ADD COLUMN IF NOT EXISTS` `load_id uuid`,
   `content_hash char(64)`, `rollback_reason varchar(400)`.
3. Guarded constraint additions (`DO` blocks testing `pg_constraint` by name in `${recoverySchema}`):
   `uk_parameter_catalog` (if absent); `ck_parameter_catalog_scope` (GLOBAL, PRODUCT);
   `ck_parameter_catalog_kind` (BUSINESS, ENVIRONMENT); `ck_parameter_catalog_value_type` (§12.2 list);
   `ck_parameter_catalog_environments` (comma list of DEV, SIT, UAT, PROD);
   `ck_parameter_catalog_secret_default` (a secret has no default); `uk_parameter_value` (if absent);
   `ck_parameter_value_environment`; `ck_parameter_value_status` (VALIDATED, APPROVED, IN_FORCE,
   SUPERSEDED, ROLLED_BACK, REFUSED); `ck_parameter_value_dates`; `ck_parameter_value_version` (>= 1);
   `ck_parameter_value_maker_checker` (approver NULL or <> author); `ck_parameter_value_approved_at`
   (APPROVED and IN_FORCE need `approved_at`); `ck_parameter_value_load_hash` (`(load_id IS NULL) =
   (content_hash IS NULL)`, hash `^[0-9a-f]{64}$`); `ck_parameter_value_rollback_reason` (ROLLED_BACK needs
   a reason); `fk_parameter_value_catalog`.
4. `CREATE [UNIQUE] INDEX IF NOT EXISTS`: `ix_parameter_value_in_force (param_key, environment, valid_from)
   WHERE status = 'APPROVED'`; `ix_parameter_value_load (load_id)`; `ux_parameter_value_version_all
   (param_key, environment, COALESCE(product_group,'*'), version_no)` (the v6 unique key treats NULL product
   groups as distinct); `ux_parameter_value_approved_from (param_key, environment,
   COALESCE(product_group,'*'), valid_from) WHERE status IN ('APPROVED','IN_FORCE')`.
5. `COMMENT ON` tables and columns (as the pack, plus the three new columns).
6. Seed catalog: `INSERT ... ON CONFLICT (param_key) DO NOTHING`, the 19 rows of §12.4.
7. Seed values (SPEC-006): `INSERT ... SELECT ... WHERE NOT EXISTS` a row for (key, environment,
   product_group NULL).
8. Self-check `DO` block (SPEC-006), restricted to rows with `default_value IS NOT NULL`, so a required
   ENV-sourced key without a default (`temporal.target`) does not fail it.

**Drift between the catalog file and `parameter_catalog` (finding 121).** Java code never reads
`parameter_catalog` (SPEC-005), so a drift cannot change what the service serves. It can still leave the
table, its FK target or the seeded defaults behind the file (for example a catalog-file change merged without
the migration a new or changed row needs). TC-27 is the drift check: in `recoveryIntegrationTest` it applies
every migration in the folder to an empty schema and asserts, row for row, that `parameter_catalog` equals
`ParameterKeys.all()` on every mirrored column (key set, kind, value type, unit, min, max, default, scope,
required, owner, environments, used by, secret, description). The seeded value rows are checked against the
§12.4 defaults by TC-13 and by the migration's own self-check. Because every later story that adds catalog rows (for example E43S SPEC-029) runs the same
test, a file change without its migration fails that story's build. A changed default needs a new migration
that updates `parameter_catalog` (a merged migration is never edited, AGENTS §4.6); it does not change an
approved value row, which only a load can change (BR3).

The pack's `ix_parameter_value_lookup` (product-group lookup) is not carried: product values are
RWB-E1-045's. No GRANT: `recovery_svc` gets DML through the default privileges for `rwb_migrator` objects
(`infra/postgres/init/20-grants.sql.inc`).

### 12.4 Bootstrap catalog (19 rows; owners and "used by" are assumptions unless the source column says otherwise)

| key | kind | type | unit | min..max | default | scope | req | owner | value_source (property) | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| case.entry.dpd | BUSINESS | INTEGER | CALENDAR_DAYS | 1..365 | 90 | GLOBAL | yes | RW-COE | TABLE | story v7 Background (owner, range, default), DL16 |
| refdata.cache.ttl-seconds | ENVIRONMENT | INTEGER | SECONDS | — | 300 | GLOBAL | yes | RW-PLATADM | TABLE | story §3, DL11; AC4, AC8 |
| config.cache.ttl-seconds | ENVIRONMENT | INTEGER | SECONDS | — | 60 | GLOBAL | no | RW-PLATADM | TABLE | story §13, DL11 (assumed) |
| caselist.export.maxrows | BUSINESS | INTEGER | COUNT | — | 10000 | GLOBAL | no | RW-COE | TABLE | story §3, DL11 |
| ace.db.password | ENVIRONMENT | STRING | — | — | — | GLOBAL | no | RW-PLATADM | SECRET | AC9, DL26 |
| recon.caselist.tolerance.pct | BUSINESS | DECIMAL | PERCENT | — | 0.00 | GLOBAL | no | RW-COE | TABLE | pack [S-20], DL25 (assumed) |
| caselist.allocation.wait.until | BUSINESS | TIME | TIME_OF_DAY | — | 07:15 | GLOBAL | no | RW-COE | TABLE | pack [S-20] |
| servicelevel.required-statuses | BUSINESS | CODE_LIST | — | — | NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL | GLOBAL | yes | RW-COE | TABLE | pack [S-20], DL22 (assumed) |
| ENTRY_DPD | BUSINESS | INTEGER | DAYS | — | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2 [S-11 line 143] |
| EXCLUSION_LIST | BUSINESS | CODE_LIST | — | — | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2 |
| NOTICE_PERIOD_DAYS | BUSINESS | INTEGER | DAYS | 1..365 | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2; range from pack |
| CURE_PERIOD_DAYS | BUSINESS | INTEGER | DAYS | — | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2 |
| EXPOSURE_BAND_SET | BUSINESS | CODE_LIST | — | — | — | PRODUCT | yes | RW-PRODHEAD | TABLE | RWB-E1-045 BR2 |
| temporal.target | ENVIRONMENT | STRING | — | — | — | GLOBAL | yes | RW-PLATADM | ENV (`rwb.temporal.target`) | D-RCV-36 §3.1 (key) |
| temporal.namespace | ENVIRONMENT | STRING | — | — | rwb-recovery | GLOBAL | no | RW-PLATADM | ENV (`rwb.temporal.namespace`) | D-RCV-36 §3.1 (key; "Namespace" row) |
| temporal.taskqueue.platform | ENVIRONMENT | STRING | — | — | rwb-platform | GLOBAL | no | RW-PLATADM | TABLE | D-RCV-36 §3.1 (key; "Task queues" row) |
| temporal.retention.days | ENVIRONMENT | INTEGER | DAYS | — | 30 | GLOBAL | no | RW-PLATADM | TABLE | D-RCV-36 §3.1 (30, assumed, DL26) |
| drools.kiebase.cache.max | ENVIRONMENT | INTEGER | COUNT | — | 20 | GLOBAL | no | RW-PLATADM | ENV (`rwb.drools.kiebase-cache-max`) | D-RCV-36 §3.1 (20) |
| rules.testcases.min | BUSINESS | INTEGER | COUNT | — | 50 | GLOBAL | no | RW-COE | TABLE | D-RCV-36 §3.1 (50); pack Appendix A |

All rows list environments `DEV,SIT,UAT,PROD`; `secret=false` except `ace.db.password`. Ranges marked "—"
have no source and stay empty (A-08). Seeded value rows: 10 TABLE GLOBAL non-secret rows with a default x 4
environments = 40 rows.

"Used by" (A-07; grammar §7.1, finding 130). The pack's values [S-20] are kept for the first 13 rows, with its
two comma lists rewritten with `;`; the six D-RCV-36 rows use the `casewf` names of RWB-TE-001. These are the
exact catalog-file values and the `usedBy[]` arrays TC-41 expects:

| key | `used_by` in the catalog file | `usedBy[]` |
|---|---|---|
| case.entry.dpd | `recovery.casewf.casecreation` | 1 entry |
| refdata.cache.ttl-seconds | `recovery.casewf.refdata` | 1 entry |
| config.cache.ttl-seconds | `recovery.casewf.config` | 1 entry |
| caselist.export.maxrows | `recovery.casewf.caselist` | 1 entry |
| ace.db.password | `ACE common module` | 1 entry |
| recon.caselist.tolerance.pct | `recovery.dataengine.caselist` | 1 entry |
| caselist.allocation.wait.until | `recovery.casewf.caselist` | 1 entry |
| servicelevel.required-statuses | `recovery.casewf.refdata.product` | 1 entry |
| ENTRY_DPD | `recovery.casewf.casecreation; recovery.casewf.allocation` | 2 entries |
| EXCLUSION_LIST | `recovery.casewf.casecreation; recovery.casewf.allocation` | 2 entries |
| NOTICE_PERIOD_DAYS | `recovery.casewf.timers` | 1 entry |
| CURE_PERIOD_DAYS | `recovery.casewf.timers` | 1 entry |
| EXPOSURE_BAND_SET | `recovery.casewf.allocation` | 1 entry |
| temporal.target, temporal.namespace, temporal.taskqueue.platform | `recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)` | 1 entry each (the comma inside the parentheses is part of the entry) |
| temporal.retention.days | `recovery.casewf.workflow (RWB-E1-070, RWB-E1-071); RWB-E2-039` | 2 entries |
| drools.kiebase.cache.max | `recovery.casewf.rules (RWB-E1-072)` | 1 entry |
| rules.testcases.min | `RWB-E1-073` | 1 entry |

The CSV field is quoted where it contains a comma (RFC 4180), as the pack already does.

### 12.5 Load checks (SPEC-012), in this order; the first failure refuses the whole load

| # | Check | Refusal |
|---|---|---|
| 1 | file content and `validFrom` present | 422 MSG-GEN-001 `{field}` |
| 2 | UTF-8 CSV with header `key,environment,value` and at least one row | 422 MSG-GEN-001 `{field}=file` / MSG-P1-002 `{check}` |
| 3 | `validFrom` not before `BusinessDateProvider.today()` | 422 MSG-P3-027 `{check}="valid from is before the business date"` |
| 4 | per row, in file order: key in the catalog | 422 MSG-P1-002 `{check}="key <k> is not in the catalog"` |
| 5 | key loadable: not secret, not PRODUCT scope, not ENV-sourced | 422 MSG-P1-002 `{check}="key <k> cannot be loaded as a value"` |
| 6 | environment listed in the key's `environments` | 422 MSG-P1-002 `{check}="environment <e> is not listed for <k>"` |
| 7 | value not blank | 422 MSG-GEN-001 `{field}="value of <k>"` |
| 8 | value parses as the type | 422 MSG-P1-002 `{check}="value is not <TYPE>"` (AC6) |
| 9 | value within min..max | 422 MSG-GEN-002 `{field}=<k>`, `{min}`, `{max}` (AC5) |
| 10 | no duplicate (key, environment) in the file | 422 MSG-P1-002 `{check}="duplicate row for <k> <e>"` |
| 11 | identical repeat (SPEC-013) | existing load, `repeat = true` |
| 12 | no APPROVED row of (key, environment) with `valid_from >= validFrom` | 409 MSG-P3-027 `{check}="an approved version from <date> exists for <k> <e>"` |

### 12.6 Canonical form and content hash (SPEC-013)

Each value is stored as loaded, trimmed, after RFC 4180 unquoting (§7.4). The hash input uses the unquoted value, and is the rows sorted by key, then environment, each
line `key|environment|value`, joined with `\n`, UTF-8; SHA-256, lower-case hex.

### 12.7 Validity recomputation (SPEC-014, SPEC-015)

After every approval or rollback, for each affected (key, environment, product_group NULL): order the
APPROVED rows by `valid_from`; each row's `valid_to` is the next row's `valid_from` minus one day; the last
row's `valid_to` is NULL. Rows in other statuses keep `valid_to` NULL. Approval and rollback each run in one
transaction with the load's rows locked (`SELECT ... FOR UPDATE`); the `version` column guards stale writes
(MSG-GEN-004).

**Transaction boundaries (review-3 plan input 1).** `load`, `approve` and `rollback` each start a transaction of
their own (`PROPAGATION_REQUIRES_NEW`, through `TransactionTemplate` in `ParameterLoadHandlerImpl`); none joins a
caller's transaction, so RWB-E1-043's endpoint gets a committed result or an exception, and a caller's own
rollback does not undo an approval already recorded in the decision log. `find` is read-only
(`PROPAGATION_SUPPORTS`). For `load`, the identical-repeat handling of SPEC-013 catches the unique violation
after the load transaction has rolled back and re-reads in a separate read-only transaction.

Approval transaction, in order (SPEC-014, SPEC-019; finding 125): (1) lock the load's rows; (2) the checks of
§8; (3) set `APPROVED`, approver, `approved_at`; (4) recompute `valid_to`; (5) call
`VersionDecisionRecorder.recorded(...)`; (6) publish `ParameterVersionApproved` to the application event
publisher; (7) commit. The event listener runs `AFTER_COMMIT`, so a failure in steps 1-5 or at commit leaves
no event and no cache rebuild. Step 5 is wrapped: any `RuntimeException` from the recorder becomes
`ApiProblemException` MSG-P7-003, HTTP 503, with the recorder's exception as cause, thrown inside the
transaction, which rolls back steps 3-4 (finding 132). An `ApiProblemException` thrown by a check in step 2 is
not wrapped.

### 12.8 Cache and refresh (SPEC-009, SPEC-018)

Per instance, keyed by (key, environment): the list of APPROVED versions. Built lazily; expires after
`config.cache.ttl-seconds` (the generated default 60 while the cache loads itself). On
`ParameterVersionApproved` (`@TransactionalEventListener(AFTER_COMMIT)`) the affected entries are rebuilt. After a
rollback the rebuild also runs **after commit** (review-3 plan input 3): `rollback` publishes an internal,
non-published `ParameterLoadRolledBack` record (package-private in `casewf.config`, published inside the rollback transaction) to the application event
publisher, handled by an `AFTER_COMMIT` listener in the same package, so a rollback that fails at commit leaves the
cache as it was. Other instances see an approval or a rollback only when their cache entry expires
(`config.cache.ttl-seconds`), until RWB-TE-006 adds the outbox (FL8 note in §6).
The cache never holds VALIDATED or ROLLED_BACK rows, and never secrets.

### 12.9 Readiness (SPEC-016)

Health indicator `parameterCatalog`, added to the readiness group
(`management.endpoint.health.group.readiness.include: readinessState,parameterCatalog`). Evaluated at start-up
and on each probe from a result refreshed with the cache. DOWN details (shown to RW-PLATADM only, per the
existing `show-details: when-authorized`): `messageCode` MSG-P3-032 and a list of `{name, environment}`. One
WARN log line per missing key with the EN text. The process keeps running so readiness can recover after a
load (CLAR-012). With the flag off, only defaults and ENV properties are checked.

Rule per required GLOBAL non-secret key listed for the running environment (SPEC-016, finding 123): UP for
that key when (TABLE) an `APPROVED` row is in force on `BusinessDateProvider.today()` or the generated key has a
default, or (ENV) the property resolves. The catalog metadata (required flag, environments, default) comes from
the generated keys only (SPEC-005); the check takes it through a `CatalogSource` bean whose production
implementation returns `ParameterKeys.all()`, so a test can supply a catalog with one default removed (TC-04).
The result is recomputed when the cache refreshes (at most `config.cache.ttl-seconds` later), so a key whose
first approved row becomes in force at a date change turns UP without a restart. Every seeded key has a default
(SPEC-006), so a seeded `valid_from` after the business date never fails readiness (triage item (f), build log
timeline line 140).

### 12.10 Access (SPEC-020)

`GET /admin/parameters` carries
`@PreAuthorize("@capabilityCheck.require(authentication, 'Rules and parameters', 'R', 'read parameters')")`.
On refusal `require` throws `ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", "read parameters"), null)`
(SPEC-020); SpEL rethrows a runtime exception from a bean method unwrapped, so the existing
`ApiExceptionHandler.problem` handler answers 403 MSG-P4-002 "You cannot read parameters here. Your role does not
include it." `ApiError.NOT_PERMITTED` takes the existing `ex.error()` branch of the handler, so the 403 needs no
change to `ApiExceptionHandler` (the message-ID branch of §10.2 is for this story's other messages) and none to
`ApiExceptionHandler.forbidden` or `SecurityConfig` (all `access.internal` after RWB-TE-001). TC-24 asserts the action text, so a
framework change that wraps the exception fails a test instead of silently answering "do this".
`CapabilityCheck` is in P4 `access.api`, its interim implementation `InterimCapabilityCheck` in `access.internal`,
registered under the bean name `capabilityCheck` that the SpEL expression resolves (review-4 plan input 3;
RWB-E1-037 keeps that name when it replaces the implementation, shared-updates.md)
(SU-08 (d); revision 4 had both in `platform`). Interim grants file
`backend/src/main/resources/access/interim-capability-grants.csv` (`role,area,rights`)
holds the "Rules and parameters" column of Users, Roles and Permissions v4 for every RW- role [S-07 lines
76-110], for example RW-COE CRUD, RW-RISK RA, RW-REFADM R, RW-PLATADM R, RW-TRIBE R, RW-AUDIT R,
RW-PHONECOL none. RWB-E1-037 replaces the implementation and deletes the file. The Reference data rights
(C, A, U) are checked on RWB-E1-043's endpoint; Reference data A is held by no role in S-07, and the
assumed grants (RW-RISK, DL01; the parameter owner, story §3) are recorded for RWB-E1-043 and RWB-E1-037
(CLAR-013).

### 12.11 Build checks (SPEC-003, SPEC-004, SPEC-005)

- Both checks are JUnit tests in `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/`, in the
  pattern of `RecoveryMigrationLintTest`, so `./gradlew check` fails on a finding. No new dependency
  (AGENTS §4.4). **Coverage (finding 131):** the logic sits in plain test-scope classes in package
  `th.co.scb.ace.demo.recovery.architecture.parameters` (the plan may rename it): `JavaLiteralTokenizer` (strips
  comments, reads literals), `MagicNumberScanner`, `CatalogFileParser` (the §7.1 rules, including the `used_by`
  grammar and the ENV credential rule) and `CatalogCompletenessRules`. The JUnit classes only call them and
  assert. They are measured in RWB-TE-001's one combined bundle (finding 143): `recoveryCoverageReport` and
  `recoveryCoverageVerification` carry one `BUNDLE` rule, `LINE`, `INSTRUCTION`, `BRANCH` and `METHOD` each at
  0.80 (TE1S SPEC-020 (a) [S-26]), over the recovery main classes plus the test-output class directories of the
  test-scope tooling (TE1S SPEC-020 (b)); `test` execution data only; outside `check` (D-RCV-40 [S-24]). As E44S
  SPEC-RWB-E1-044-014 does for its own tooling package [S-23], the plan adds the test-output classes of
  `architecture.parameters` to `classDirectories` of both tasks, filtered to that package and excluding the JUnit
  classes (`**/*Test.class`, `**/*Test$*.class`, `**/*IT.class`, `**/*IT$*.class`) and fixtures, or states that
  RWB-TE-001's merged filter already takes the package in. No new task, rule, counter or threshold; no
  `recoveryToolingCoverageVerification` (withdrawn, E44S line 375). The `backend/build.gradle.kts` edit is recorded
  in `shared-updates.md`; RWB-TE-001, RWB-E1-044 and this story each add to the same `classDirectories` filter, so the
  plan extends the merged filter and never replaces it (review-6 plan input 1). TC-41, TC-43 and TC-44 are their unit tests.
- Fixture modules for AC2, AC3 and the PRODUCT exemption live under
  `backend/src/test/resources/architecture/fixtures/` (for example `recovery/casewf/casecreation/EntryRule.java`
  with a literal 90; a reader of `ParameterKey.of("allocation.retry.limit", Integer.class)`; a catalog with a
  PRODUCT row and no default). They are not compiled.
- Magic-number baseline `backend/src/test/resources/architecture/magic-number-baseline.csv`
  (`path,literal,count,reason,owner`; each `path` is the class's file at its RWB-TE-001 home, TE1S Relocation
  table), starting with the literals in the code as RWB-TE-001 leaves it: `ApiError` (`access.api`) HTTP status
  codes 401, 403, 404, 503 (protocol, not business); `DroolsRuleEngine` 16 and 0.75f (map sizing);
  `PdpaPayloadCodec` 12, 128, 16, 24, 32 (AES-GCM sizes); `PlatformSmokeWorkflow` 5 and 3 (smoke timeout and
  attempts, owner RWB-E1-071); `WorkflowIds` "rwb-recovery" and "rwb-platform" (equal to the defaults of
  `temporal.namespace` and `temporal.taskqueue.platform`, owner RWB-E1-071). The plan re-derives the exact
  list from the code. A stale or miscounted entry fails.
- This story's own literals (plan input P1): HTTP statuses use `HttpStatus` constants (no numeric literal);
  the schema limits (rollback reason 400 characters, `varchar(400)`; hash length 64, `char(64)`; Physical
  Schema v6 and §12.3) are named constants in `casewf.config`, each added to the baseline file
  in the same pull request with reason "schema limit". No business value is among them.
- `ParameterKeys` generation: a Gradle task in `backend/build.gradle.kts` reads the catalog file and writes
  `build/generated/sources/parameterKeys/th/co/scb/ace/demo/recovery/casewf/config/api/ParameterKeys.java`;
  `compileJava` depends on it. **Coverage exception (finding 131), recorded:** the task's code runs in the Gradle
  build JVM before compilation; it is not in the combined bundle's class directories (main classes and test-scope tooling output),
  and JaCoCo's `test` execution data never sees it, so no counter can measure it. D-RCV-40 keeps coverage verification to the
  recovery classes measured from `test` data and outside `check` [S-24]; it does not reach build-script code.
  The task is kept to a few lines (read rows, write one constant per row), and its output is covered instead:
  TC-42 parses the catalog file with `CatalogFileParser` and asserts that `ParameterKeys.all()` matches it row
  for row on every column (key, kind, type, unit, min, max, default, scope, required, owner, environments,
  `usedBy` entries, secret, value source, property, description), so any generator fault fails `test`;
  TC-26 and TC-27 cover the typed constants and the database copy. The generated class itself is MAIN code
  and counted.
  The catalog sits under `backend/src/main/resources/config/` because the Docker build context is `./backend`
  and copies only `src` (`backend/Dockerfile`; `docker-compose.yml` line 120).

### 12.12 Feature flag (SPEC-021)

`rwb.p3.configservice: ${RWB_P3_CONFIGSERVICE:false}` in `application.yaml`;
`${RWB_P3_CONFIGSERVICE:true}` in `application-local.yaml`. Two mechanisms only (review-4 plan input 1; SU-08 (b)):
`@ConditionalOnProperty(prefix = "rwb.p3", name = "configservice", havingValue = "true")` on the conditional beans
(`ParameterLoadHandlerImpl`, the parameter catalog controller), and `@Value("${rwb.p3.configservice:false}")` read
in the two always-registered beans whose behaviour differs (`ParameterServiceImpl`: defaults and ENV only when
off; `ParameterStartupCheck`: defaults and ENV only when off). No configuration-properties record is added for it. `RecoveryFlags` (`integration.flags.api`), the per-module property records of TE1S SPEC-023
and `/platform/info` are not changed (revision 4's `RecoveryProperties.P3` / `RecoveryFlags` change is withdrawn;
finding 129). The only other story's test this story changes is RWB-TE-001's T-TE001-14, whose expected sets are
extended, not relaxed (§2, TC-45; finding 136). Bean registration by flag state (SPEC-021):

| Bean | Flag on | Flag off |
|---|---|---|
| `ParameterService`, `CatalogSource`, `ParameterStartupCheck`, `BusinessDateProvider`, `VersionDecisionRecorder` (all `casewf.config`); `MessageResolver`, `CapabilityCheck` (`access.internal` implementations) | registered | registered (`ParameterService` serves defaults and ENV values only) |
| `ParameterLoadHandler` | registered | **absent**; no bean of `casewf.config` depends on it; consumers use `ObjectProvider` |
| Parameter catalog controller (`GET /admin/parameters`) | registered | absent (404) |

### 12.13 Logging

Structured logs only; no secret values. No author, approver or caller user ID in any log line, event payload or
exception message (they are personal data, SPEC-027); the interim decision line carries loadId, table, keys,
validFrom and decision code only. Load refusals log the message ID and check, never the file. A recorder failure
is logged once, by the handler's new branch (§10.2): message ID MSG-P7-003, status, `traceId`, cause class and the
fixed text "cause suppressed"; never the cause's message or stack trace (finding 137, D-RUN-15). `created_by` and
`updated_by` values are never logged either (SPEC-027).

### 12.14 Plan inputs (reviews 3 to 6: REVIEW-RWB-E1-042-SPEC-005 to -008)

Carried from review 3 [S-27] for the Implementation Planner, each with where this revision applies it.

| # | Plan input (review 3) | Applied in this spec | Test |
|---|---|---|---|
| 1 | Transaction boundary of `load`: the catch-and-re-read must sit outside the failed transaction; state whether `load` joins a caller's transaction | `load`, `approve`, `rollback` run in their own `REQUIRES_NEW` transactions and never join a caller's; the unique-violation catch is outside the rolled-back load transaction and the re-read runs in a new read-only transaction (SPEC-013, SPEC-017, §12.7). RWB-E1-043 is told (shared-updates.md) | TC-16, TC-33 |
| 2 | No ENV row may point at a credential-bearing property; such keys must be `secret=true` | `CatalogFileParser` refuses an ENV row whose `env_property` has a credential segment (SPEC-003, §7.1) | TC-44 |
| 3 | Cache rebuild after rollback runs after commit; other instances learn of it only through the TTL | `AFTER_COMMIT` rebuild through an internal event; TTL for other instances (SPEC-015, §12.8; FL8 note) | TC-10 |
| 4 | `ApiExceptionHandler.problem` with message-ID constructors: `ex.error()` is null; the handler change belongs to the P4 home | Message-ID branch in `access.internal.ApiExceptionHandler.problem` through `ProblemFactory` and `MessageResolver` (SPEC-022, §10.2) | TC-30 |

Review 4 [S-29] adds six plan inputs, and the orchestrator's triage adds the T-TE001-14 and module-map edits:

| # | Plan input (review 4 / triage) | Applied in this spec | Test |
|---|---|---|---|
| R4-1 | Flag state in always-registered beans: name the mechanism; no `RecoveryFlags` field | `@ConditionalOnProperty` on the conditional beans; `@Value("${rwb.p3.configservice:false}")` in `ParameterServiceImpl` and `ParameterStartupCheck` (SPEC-021, §12.12) | TC-22 |
| R4-2 | MAIN coverage from `test` only: plan unit tests in `test` for the service, checks, validity, hash, cache, startup check, controller and handler | §14: unit tests (Mockito, MVC slice) in `test` for `ParameterServiceImpl`, each §12.5 check, the §12.7 recomputation, the §12.6 hash, the cache, `ParameterStartupCheck`, the parameter catalog controller (incl. E7) and `ParameterLoadHandlerImpl`; the System tests do not count | Plan lists them |
| R4-3 | SpEL bean name `capabilityCheck`; RWB-E1-037 keeps it | §12.10 | TC-24 |
| R4-4 | Load-file quoting: RFC 4180, same reader as the catalog; hash on the unquoted value | §7.4, §12.6 | TC-16 (a CODE_LIST value with commas, loaded twice, gives `repeat = true`) |
| R4-5 | A later JPA recorder flushes inside `recorded(...)` | SPEC-019 | TC-29 (b) contract |
| R4-6 | Re-check RWB-E1-043's revision in force (flag-off refusal, import packages, caller in P3) when the plan is written | §4.3 first seam row; A-28; shared-updates.md | Plan check |
| T-1 | Module map: add `config.api` to the `casewf` `published` list; `access.api` is already published and the map has no per-type field, so the two `access.api` types go into T-TE001-14's expected set (triage item 136) | §2, §12.1, SPEC-026 | TC-45 |
| T-2 | Extend T-TE001-14's expected sets in the same change: public types of `access.api` + `MessageResolver`, `CapabilityCheck`; `casewf.config.api` types of §12.1; `casewf` named interfaces + `config.api`. Extension, not weakening; recorded in shared-updates.md | §2, §12.12 | TC-45 |

Review 5 [S-30] adds four plan inputs:

| # | Plan input (review 5) | Applied in this spec | Test |
|---|---|---|---|
| R5-1 | Re-check against the RWB-E1-043 revision that passes its gate (revision 4 on 18 Nov: imports match `shared-updates.md` §1, flag-off 404 MSG-P4-003 kept); RWB-E1-043 also extends T-TE001-14's `access.api` set (for example `ListOfValuesReader`) in the same way (A-41) | A-28, §4.3 first seam row | Plan check |
| R5-2 | Guard the new constructor; list every caller of `error()` | §10.2 guards; plan lists callers (today `ApiExceptionHandler.problem`) | TC-30 (e) |
| R5-3 | Other data-access failures on GET reach the inherited `unexpected` handler | §10.2 E7: accepted as inherited until RWB-TE-003 (D-RUN-15) | Plan statement |
| R5-4 | TC-10 (b)'s `BEFORE_COMMIT` listener sits in the `casewf.config` test package, because `ParameterLoadRolledBack` is package-private | TC-10 | TC-10 (b) |

Review 6 [S-31] adds four plan inputs:

| # | Plan input (review 6) | Applied in this spec | Test |
|---|---|---|---|
| R6-1 | Three stories edit the same `classDirectories` filter: extend the merged filter, never replace it | §12.11 | Coverage report |
| R6-2 | The rev 7 RWB-TE-003 row of `shared-updates.md` is applied before RWB-TE-003's plan; T-TE003-35 covers the message-ID branch | `shared-updates.md` §1 | RWB-TE-003's T-TE003-35 |
| R6-3 | The RWB-E1-043 revision that passes its gate uses the `detail` argument and adds no P4 change of its own beyond the D-RUN-18 SPI | §10.2; A-48 | Plan check |
| R6-4 | TC-30 (e) also covers a null `status` and a 503 with placeholders | TC-30 (e) | TC-30 |

## 13. Frontend Specification

NOT_APPLICABLE. No screen in this story (story v7 §15); SCR-39 is Epic 8. `GET /admin/parameters` is
backend-only in this story. `frontend/src/api/schema.d.ts` is not regenerated (no OpenAPI change). `/platform/info` is not changed
(§12.12).

## Unit Test Applicability

Section 14.

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | §13 | Story v7 §15; no OpenAPI change; no screen or client call | n/a |
| Backend | YES | REQUIRED | 80% on all four metrics, in JaCoCo counters: lines `LINE`, statements `INSTRUCTION`, branches `BRANCH`, functions `METHOD`, one `BUNDLE` rule in `recoveryCoverageVerification` (TE1S SPEC-020 (a) [S-26]; the four limits are RWB-TE-001's, merged before this story; E44S SPEC-RWB-E1-044-014 makes no change to a counter or threshold [S-23]). The bundle is every main class under `th/co/scb/ace/demo/recovery/**` plus the test-output classes of the test-scope tooling (TE1S SPEC-020 (b)); this story's `architecture.parameters` classes join it as §12.11 states (finding 143). The task stays **outside `check`** (D-RCV-40 [S-24]; build log timeline line 120) and is run by the Implementation Builder as stage evidence (`./gradlew test recoveryCoverageVerification`), with the report attached. It reads `test` execution data only (`executionData(tasks.named("test"))`), so the unit tests in `test` alone must reach 80%: the plan writes Mockito or MVC-slice unit tests for `ParameterServiceImpl`, each §12.5 check, the §12.7 recomputation, the §12.6 hash, the cache, `ParameterStartupCheck`, the parameter catalog controller and `ParameterLoadHandlerImpl` (review-4 plan input 2); the `recovery-it` System tests do not count toward it. The earlier plan input 12 ("add it to `check`") was withdrawn by the gate (finding 124). There is no separate tooling gate: `recoveryToolingCoverageVerification` was withdrawn by RWB-E1-044 (E44S line 375). **Recorded exception:** the `ParameterKeys` Gradle task is build-script code, not in the combined bundle's class directories, so JaCoCo cannot measure it; its output is verified by TC-42, TC-26 and TC-27 (§12.11) | SPEC-001 to SPEC-027 | New service, interface, controller, checks, migration | Positive: every AC path. Negative: every row of §12.5, approval by the author, rollback with no earlier version, empty reason, secret read. Boundary: 1 and 365 accepted, 0 and 366 refused; `validFrom` equal to the business date accepted, one day before refused; reads on `valid_from - 1` and on `valid_from`; readiness for a required key with no default whose only approved row starts the day after the business date (DOWN) and on that date (UP). Error path: database unavailable on GET 503 with no message ID; concurrent approval 409; recorder failure rolls the approval back with 503 MSG-P7-003; unknown loadId 404 on approve and rollback; approve of a non-VALIDATED load 409; rollback of a non-APPROVED load 409; reason 400 accepted, 401 refused; concurrent identical loads give one load; flag off: context starts without `ParameterLoadHandler` |

No measured coverage is claimed here.

## 15. Test scenarios

Levels in this repository: Unit and build checks (`test`); System (`recoveryIntegrationTest`, tag
`recovery-it`: Spring Boot context, Testcontainers PostgreSQL 16 built as the local stack; the
`ParameterLoadHandler` bean is called directly, because no endpoint exposes it until RWB-E1-043; GET through
MockMvc with Spring Security test JWTs carrying synthetic `sub` UUIDs and roles). "U-41" is a synthetic label
for a fixed synthetic UUID. RWB-E1-043 adds the HTTP-level tests of the three load operations. The
interface-level tests here assert to the same depth as an HTTP test would: the `ApiProblemException`'s message
ID, status, placeholders and `field`, the Problem fields rendered by `ApiExceptionHandler` (asserted in TC-30 for each form, since the handler runs only in MVC dispatch), and the database
state after the call (plan input P5). Every user ID in a test is a synthetic UUID generated for the test; none
is logged or asserted in a log line (SPEC-027).

| TC | Covers | Level | Data | Expected | Status |
|---|---|---|---|---|---|
| TC-E1-042-01 | AC1, BR1 | System | seed; PROD context; date 2026-12-01 | 90, versionNo 1 | Ready |
| TC-E1-042-02 | AC2, BR1, X1 | System (build check on fixture module) | fixture `recovery/casewf/casecreation` with literal 90 | check fails naming file, line, `case.entry.dpd` | Ready |
| TC-E1-042-03 | AC3, BR2, X2 | System (build check on fixture module) | fixture reading `allocation.retry.limit` | fails naming `allocation.retry.limit`; the real catalog has zero findings | Ready |
| TC-E1-042-04 | AC4, BR7, X3 | System | UAT context; `refdata.cache.ttl-seconds` UAT value rows deleted; the default is removed at its one source: the test's `CatalogSource` returns `ParameterKeys.all()` with that key's default empty (SPEC-005, §12.9). `parameter_catalog.default_value` is left as seeded, to show that the DB copy is not read | readiness DOWN, MSG-P3-032 with key and UAT | Ready |
| TC-E1-042-05 | AC5, X4 | System (interface) | load `case.entry.dpd,PROD,400` | 422 MSG-GEN-002 min 1 max 365; nothing written | Ready |
| TC-E1-042-06 | AC6, X5 | System (interface) | `case.entry.dpd,PROD,ninety` | 422 MSG-P1-002 "value is not INTEGER" | Ready |
| TC-E1-042-07 | AC7, BR4, X6 | System (interface) | versions 1-2 approved; U-41 loads v3 and approves it | 409 MSG-P7-002; status VALIDATED | Ready |
| TC-E1-042-08 | AC8 | System | 30 approved for SIT; PROD 300; contexts with `rwb.environment` SIT and PROD | 30 and 300 | Ready |
| TC-E1-042-09 | AC9, BR6, X7 | System | GET as RW-COE | `ace.db.password` with owner, environments, usedBy; no value fields | Ready |
| TC-E1-042-10 | AC10, X8; review-3 plan input 3 | System (interface) | v2 approved over v1; rollback with reason; then (b) a rollback inside a test transaction template whose commit is forced to fail | v1 in force, 90; v2 ROLLED_BACK; the cache rebuild happens after commit (read in the same instance returns v1 right after `rollback` returns). (b) The failure is forced **inside the rollback's own `REQUIRES_NEW` transaction** (finding 139): a test-only `@TransactionalEventListener(phase = BEFORE_COMMIT)` on `ParameterLoadRolledBack`, declared in the `th.co.scb.ace.demo.recovery.casewf.config` test package (the event is package-private; review-5 plan input 4) and registered in the test context, throws; `rollback` then throws that exception, the transaction is rolled back, the rows are still `APPROVED` with `version` unchanged and `rollback_reason` NULL, the `AFTER_COMMIT` rebuild did not run, and the cache still serves v2 | Ready |
| TC-E1-042-11 | AC11, BR5, X10, §7.3; finding 149 | System (interface) | business date 2026-12-05; v2 = 91 PROD from 2026-12-10 loaded by one synthetic user, approved by another | 90 on 12-09, 91 on 12-10, same context; after approval each v2 row keeps `created_by` = the author and has `updated_by` = the approver | Ready |
| TC-E1-042-12 | X9 (access) | Access | RW-PHONECOL session from RWB-E1-022; matrix PM-2026.11 from RWB-E1-037 | 403 problem+json MSG-P4-002, action "read parameters", no array, one refusal event | **Blocked** (OI-E1-042-001). Exit: after RWB-E1-037 loads PM-2026.11 and RWB-E1-022 resolves the RW-PHONECOL test identity, run it; Pass only on that evidence |
| TC-E1-042-13 | SPEC-001/002/006; finding 147 | System | empty schema | migration applies; tables, constraints, indexes; 19 + 40 seed rows; every seeded value row has `created_by` and `author_user_id` = the seed identity, `is_active` true, `state` NULL, `created_at` set | Ready |
| TC-E1-042-14 | SPEC-001/002 | System | schema built from Physical Schema v6 (local init) | migration applies; columns and constraints added; no error | Ready |
| TC-E1-042-15 | SPEC-001 | Unit | `RecoveryMigrationLintTest` as RWB-E1-044 leaves it (identifier-only, quote-aware; D-RUN-13, E44S SPEC-RWB-E1-044-007, T-044-21); precondition PRE-6 | passes with the new file, whose `used_by` and `COMMENT ON` literals contain `recovery.` text; seed values unchanged | Ready (after RWB-E1-044 merges) |
| TC-E1-042-16 | SPEC-013; review-4 plan input 4 | System (interface) | same content and validFrom twice; also a file with a quoted CODE_LIST value containing commas | same loadId, `repeat = true`, one set of rows | Ready |
| TC-E1-042-17 | SPEC-013 | System (interface) | different value, same key/env/validFrom as an approved load | 409 MSG-P3-027 | Ready |
| TC-E1-042-18 | SPEC-015 | System (interface) | rollback with blank reason | 422 MSG-GEN-001 field reason | Ready |
| TC-E1-042-19 | SPEC-015 | System (interface) | a key whose only approved version comes from one load; roll that load back | 409 MSG-P3-015 | Ready |
| TC-E1-042-20 | SPEC-014 | System (interface) | two concurrent approvals | one APPROVED, one 409 MSG-GEN-004 | Ready |
| TC-E1-042-21 | SPEC-003 | Unit | fixture catalog with a PRODUCT row and no default | no finding; the same row without owner fails | Ready |
| TC-E1-042-22 | SPEC-021, finding 119 | System | flag off; the test context adds a probe bean that takes `ObjectProvider<ParameterLoadHandler>` (the consumer pattern of the contract) | the application context starts; `getIfAvailable()` returns null; no bean of `casewf.config` depends on `ParameterLoadHandler`; GET 404; `get` returns the default, versionNo 0; readiness evaluates defaults and ENV only. The HTTP refusal (404 MSG-P4-003) is asserted on RWB-E1-043's side by E43S TC-PB-01 and TC-FL-01 | Ready |
| TC-E1-042-23 | SPEC-012/023 | System (interface) | unknown key; empty file; validFrom before the business date | 422 MSG-P1-002; MSG-GEN-001; MSG-P3-027 | Ready |
| TC-E1-042-24 | SPEC-020 seam, findings 120, 129 | System; plus Unit on `access.internal.InterimCapabilityCheck` | GET with a test JWT for a role without Rules and parameters R; unit: `require` with and without the grant, `has` with and without, grants read from `access/interim-capability-grants.csv` | 403 problem+json, `messageCode` MSG-P4-002, `detail` "You cannot read parameters here. Your role does not include it." (not "do this"); unit: `require` returns true or throws `ApiProblemException` with `NOT_PERMITTED` and `action` = the given text; `has` never throws. Does not close TC-12 | Ready |
| TC-E1-042-25 | SPEC-004 | Unit | baseline with a stale entry; code with an unlisted literal | both fail | Ready |
| TC-E1-042-26 | SPEC-005/024 | Unit | generated keys; `rwb.drools.kiebase-cache-max=20` | typed constants; ENV key served from the property | Ready |
| TC-E1-042-27 | SPEC-002/005/006/024, finding 121 (drift check) | System | every migration in the folder applied to an empty schema | `parameter_catalog` equals `ParameterKeys.all()` row for row on every mirrored column (§12.3 drift paragraph; 19 rows in this story, more as later stories add rows); a fixture catalog with one changed default and no migration fails the comparison naming the key and column | Ready |
| TC-E1-042-28 | SPEC-009/018/027 | System (interface) | approval | one event after commit with the §11.4 fields and no user ID; cache rebuilt; no event on refusal | Ready |
| TC-E1-042-29 | SPEC-014/019/025/027, findings 125, 132, 137, 146 | System (interface) | (a) approval with the interim recorder; (b) approval with a test recorder that asserts an active transaction and throws | (a) recorder called once with AC-VERS, inside an active transaction, after the rows are `APPROVED` in that transaction; log line has no user ID. (b) the call throws `ApiProblemException` with `messageId()` MSG-P7-003, `status()` 503, no placeholders, `detail()` null, the recorder's exception as cause; no line logged by `casewf.config` code holds the cause's message (a synthetic marker string holding a synthetic UUID); rendering and the handler's log line are TC-30's (finding 146), because the handler runs only in MVC dispatch; rows still `VALIDATED`, `version` unchanged, `approver_user_id` NULL; no `ParameterVersionApproved`; cache unchanged | Ready |
| TC-E1-042-30 | SPEC-022/025/027; review-3 plan input 4; findings 135, 137, 144, 146; review-5 plan input 2; review-6 plan input 4 | Unit (in `access.internal`) | each §10.3 ID; `ApiExceptionHandler.problem` with (a) an `ApiError` exception, (b) a status-and-message-ID exception with a field, (c) the status-only 503 form, (d) a message-ID exception with a `detail` override (synthetic text "row 2: x; row 5: y"), (e) constructor guards; each of (a)-(d) with a cause whose message is a synthetic marker | EN and TH present with the same placeholders; (a) unchanged rendering; (b) full Problem with `messageCode`, `messageTh`, `field`, `traceId`; (c) `type` `urn:rwb:problem:unavailable`, `status` 503, `traceId`, no `messageCode`; (d) `detail` equals the override, `messageCode` and `messageTh` from the resolver, the override absent from the log; (e) a null `status`; a null `messageId` with status 409; and a null `messageId` with 503 and placeholders, a `detail` or a field: each throws `IllegalArgumentException`; for (b), (c) and (d) one WARN line with message ID (or `none`), status, `traceId`, cause class and "cause suppressed", and the marker absent from the log | Ready |
| TC-E1-042-31 | SPEC-011 | System | filters key prefix, kind, owner, environment | filtered lists; PRODUCT rows without value | Ready |
| TC-E1-042-32 | SPEC-016, finding 123 | System | business date 2026-12-05 (test `BusinessDateProvider`); fixture required TABLE key with no default, one approved row from 2026-12-06; seeded keys with `valid_from` moved to 2026-12-31 | DOWN with MSG-P3-032 naming the fixture key; business date 2026-12-06 → UP after the cache refresh; seeded keys never DOWN (defaults cover them) | Ready |
| TC-E1-042-33 | SPEC-013, plan input P3 | System (interface) | two threads load the same content and `validFrom` at once (latch) | one set of rows; both results carry the same `loadId`; one has `repeat = true`; no 500 | Ready |
| TC-E1-042-34 | SPEC-025, E7, findings 126, 135, 137 | System | GET with the data source failing (connection refused) | 503 problem+json with `status` and `traceId`; no `messageCode`; no text that promises a retry; raised by the controller as the status-only `ApiProblemException` (no P3 call to `ProblemFactory`); the driver exception's message is absent from the captured log | Ready |
| TC-E1-042-35 | SPEC-017, E6, finding 133 | System (interface) | `approve` and `rollback` with (a) a random UUID, (b) the `id` of a seeded `parameter_value` row | 404 MSG-P4-003 for each; nothing changed | Ready |
| TC-E1-042-36 | SPEC-014, §8, finding 133 | System (interface) | load with `validFrom` = business date D; test `BusinessDateProvider` moved to D+1; approve by another user | 409 MSG-P3-027; rows stay `VALIDATED`, `version` unchanged | Ready |
| TC-E1-042-37 | SPEC-015, §8, finding 133 | System (interface) | rollback of (a) a `VALIDATED` load, (b) a `ROLLED_BACK` load | 409 MSG-P3-027 `{check}="only an approved load can be rolled back"`; nothing changed | Ready |
| TC-E1-042-38 | SPEC-014, §8, finding 133 | System (interface) | approve of (a) an `APPROVED` load, (b) a `ROLLED_BACK` load | 409 MSG-GEN-004; nothing changed | Ready |
| TC-E1-042-39 | SPEC-015, E5, finding 133 | System (interface) | rollback reason of 400 characters; another of 401 characters (each after trim; synthetic text) | 400 accepted (`rollback_reason` stored in full); 401 refused 422 MSG-GEN-001 `field` = `reason`, nothing changed | Ready |
| TC-E1-042-40 | SPEC-017, §7.3; findings 133, 149 | System (interface) | `find` with the loadId of a load just made (author a synthetic UUID); `find` with a random UUID | hit: `ParameterLoadResult` equal to the load's result (status, rows, validFrom, `repeat` false); each written row has `created_by` = `author_user_id`, `is_active` true, `state` NULL, `created_at` set; miss: `Optional.empty()`, no exception. No user ID appears in any log assertion (SPEC-027) | Ready |
| TC-E1-042-41 | SPEC-003, BR2, §7.1, finding 130 | Unit (tooling) | (a) the real `parameter-catalog.csv`; (b) fixtures `a;;b`, `a;`, `;a`, blank, an entry of 101 characters, an entry with a line break | (a) every row parses; each `usedBy[]` equals the §12.4 table (e.g. `temporal.retention.days` → [`recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)`, `RWB-E2-039`]; `ENTRY_DPD` → 2 entries); GET returns the same arrays (asserted in TC-09 data). (b) each fails, naming key and column | Ready |
| TC-E1-042-42 | SPEC-005, finding 131 | Unit | the real catalog file parsed by `CatalogFileParser`; `ParameterKeys.all()` | equal row for row on every column (§12.11); a key in one and not the other fails naming it | Ready |
| TC-E1-042-43 | SPEC-004, finding 131 | Unit (tooling) | `JavaLiteralTokenizer` and `MagicNumberScanner` cases: literals in line and block comments, in strings and text blocks, char literals, `0x`/`_`/suffixed numbers, negative literals | comments ignored; string content not read as a number; numbers normalised before matching | Ready |
| TC-E1-042-44 | SPEC-003, BR6, §7.1 credential-name rule; review-3 plan input 2; finding 138 | Unit (tooling) | fixture ENV rows with `env_property` `rwb.ace.db.password`, `spring.datasource.Password`, `rwb.client-secret`, `rwb.api-key`, `rwb.api_key`, `rwb.clientSecret` (camel case), `rwb.privateKey`, `rwb.auth.tokenUrl`, and clean `rwb.temporal.target`, `rwb.drools.kiebase-cache-max` | the eight fail naming key and property; the two clean ones pass; the real catalog passes | Ready |
| TC-E1-042-45 | SPEC-026, findings 129, 136, 141 | Unit (existing boundary tests) | `ModulithTest`, `RecoveryBoundaryTest` and T-TE001-14 of RWB-TE-001, with `config.api` in the `casewf` `published` list and T-TE001-14's expected sets extended in the same change | pass: `casewf.config.api` declares `@NamedInterface(name = "config.api", propagate = false)`; T-TE001-14 finds exactly its SPEC-025 types plus `access.api` `MessageResolver`, `CapabilityCheck` and the eleven `casewf.config.api` types of §12.1, and `casewf` named interfaces `api`, `config.api`, `rules`, `timers`, `workflow`; no P4 type depends on a P3 type; no other module uses `casewf.config` internals. Removing the map entry, or adding a further public type to `access.api`, fails the test | Ready |

## 16. Authority

| Who | What they may do (source) | Enforced where |
|---|---|---|
| RW-COE | Owns the catalog; loads (Reference data C), rolls back (U), reads; approves as parameter owner (assumed A) [S-01 §3, §10; S-07 line 101] | Read: this story. Load, approve, rollback rights: RWB-E1-043's endpoint |
| RW-REFADM | Loads (Reference data C), rolls back (U), reads (Rules and parameters R) [S-01 §3; S-07 line 107] | as above |
| RW-RISK | Approves where a threshold or limit moves (Reference data A, assumed grant, DL01) [S-01 §3, §10]; holds Rules and parameters RA and Reference data R in S-07 line 100 | as above (CLAR-013) |
| Parameter owner (catalog `owner_role`) | Approver per story §3 | RWB-E1-043 / RWB-E1-037 (CLAR-013) |
| Any approver | Must not be the author (BR4) | This story (`ParameterLoadHandler`, DB check) |
| RW-PLATADM | Owns environment settings; reads (Rules and parameters R) [S-01 §10; S-07 line 106] | This story |
| RW-TRIBE | Adds catalog entries through reviewed PRs; reads [S-01 §10] | Merge review; this story |
| Any role with Rules and parameters R | Reads the catalog | This story |
| RW-PHONECOL | No Rules and parameters right; refused [S-07 line 76] | This story (TC-12 blocked) |
| Delegation of authority | Not applicable: a parameter is not a credit decision [S-01 §10] | — |

## 17. Guardrails and controls

- No business value in code (SPEC-004); no new dependency; no personal data in code, fixtures, tests or logs;
  synthetic UUIDs only.
- Personal data (SPEC-027): `author_user_id` and `approver_user_id` are staff identifiers, personal "Yes" in
  Personal Data Inventory v4 (DF-REF-156, -157) [S-28]; Physical Schema v6 says `is_personal` false, and the
  protective reading is applied (gap E1042-SP-DG-15, CLAR-024). `created_by` / `updated_by` and the rollback caller ID are treated the same way (gap E1042-SP-DG-17). They are stored in `parameter_value` and passed
  to the decision log only; never logged, published in an event, put in an exception message, or returned.
- Secrets: listed, never stored or served (SPEC-010, DB check).
- Maker-checker in the interface and the database (SPEC-014).
- Audit: author, approver, times and rollback reason in `parameter_value`; AC-VERS through the recorder seam
  (SPEC-019), written inside the approval transaction (SPEC-014). The access log is RWB-E1-039 (phase0 A-18;
  §4.3 seam row: nothing built here).
- D-RCV-35: Workbench-owned reference data in `recovery`; no `public` read; no source load.
- D-RCV-36: the six keys are catalog rows; no Temporal or Drools call in this story.

## 18. Out of scope

- The shared reference-load endpoint and its dispatch, the other table codes, and `/verify` (RWB-E1-043,
  D-RUN-10, D-RUN-11), including the flag-off refusal of `PARAMETER` (SPEC-021 contract).
- Column definitions per reference table code: keys, grammar and row check are RWB-E1-043's (E43S SPEC-003,
  SPEC-029); values are each table's story's (CLAR-022, finding 127).
- The access-log entry for `GET /admin/parameters` (RWB-E1-039, §4.3).
- Product-specific parameter values and service levels (RWB-E1-045).
- Dated feature flags and the flag table (FEAT-CWC-26, RWB-E1-047).
- The parameter administration screen (Epic 8, FEAT-ADM-01).
- The change checklist and audit report, including `changeRequestRef`, `impactSummary` and `rollbackPlan`
  (RWB-E2-041) [S-01 §19].
- Decision log store and writer (RWB-E1-008, RWB-E1-027); outbox (RWB-TE-006); permission matrix and sessions
  (RWB-E1-037, RWB-E1-022); moving the Temporal and Drools reads to `ParameterService` (RWB-E1-071,
  RWB-E1-072); the message table (unowned).

## Clarification Log

Section 19.

No question is asked in this run (RUN-BRIEF rule 4, L-RCV-03, AGENTS §10.6). Each item carries a labelled
default (`assumptions.md`) and, where it is an open item, a row in `shared-updates.md`. The pack's items stay
open; where the evidence settles an item for this spec, the row says so, but closing the register entry is
the owner's decision (triage decision (e)).

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | OI-E1-042-001; X9; TC-12 | The access test needs RWB-E1-022 sessions and the RWB-E1-037 matrix | TC-12 cannot run in this window | Not asked. Default: Blocked with exit criterion | OPEN (non-blocking) | 011, 020 |
| CLAR-002 | OI-E1-042-002; D-RCV-28 | The two-file names fail the lint | Migration design | Not asked. Settled for this spec by D-RCV-28 and D-RUN-07: one file, number at merge | OPEN in register; settled for this spec | 001 |
| CLAR-003 | OI-E1-042-003; PRE-2 | Full Epic 1 catalog file absent | Later stories add their keys | Not asked. Default: 19-row bootstrap (§12.4); each later story adds its rows by PR and migration | OPEN (non-blocking) | 003, 006 |
| CLAR-004 | OI-E1-042-004; AGENTS §3.6 | No message table | Message source | Not asked. Default: fixed catalog behind `MessageResolver` | OPEN (non-blocking) | 022 |
| CLAR-005 | OI-E1-042-005 | No per-code CSV template register | Only the PARAMETER template is defined here | Not asked. Default: PARAMETER header `key,environment,value` (pack §3.3) | OPEN (non-blocking; RWB-E1-043) | 012 |
| CLAR-006 | OI-E1-042-006; finding 117 | Naming conflicts (`case.entry.dpd` / `case.entry.dpd_threshold` / `ENTRY_DPD`; prescription and tolerance keys) | Two keys for one concept | Not asked. Default: `case.entry.dpd` is the GLOBAL key; `ENTRY_DPD` is RWB-E1-045's product key; the other names are not seeded | OPEN (decision needed) | 006 |
| CLAR-007 | OI-E1-042-007; AC3 | PRODUCT rows have no default | Completeness rule | Not asked. Default: exempt PRODUCT from the default rule (pack recommendation) | OPEN in register; applied | 003 |
| CLAR-008 | OI-E1-042-008; finding 104 | No load-to-rows link | Approve and rollback by loadId | Not asked. Default: pack option A, `load_id` plus `content_hash` and `rollback_reason`; Physical Schema update requested | OPEN (schema owner) | 002, 014, 015 |
| CLAR-009 | OI-E1-042-009 | `recoverySchema` placeholder property | Migration placeholder | Not asked. Settled for this repository by `RecoveryFlywayConfig.java:37` (`placeholders(Map.of("recoverySchema", schema))`); the pack's property is not needed here | OPEN in register; settled for this spec | 001 |
| CLAR-010 | OI-E1-042-010 | PRODUCT targets, DOCUMENT_HUB_PARAMETER, RETENTION_CLASS | Other table codes | Not asked. Outside this story; dispatch is RWB-E1-043's (D-RUN-10, D-RUN-11) | OPEN (RWB-E1-043 and owners) | 017 |
| CLAR-011 | OI-E1-042-011; finding 106 | OpenAPI lacks `required`, `format`, repeat status | Contract hardening | Not asked. Default: enforced in the interface; identical repeat answered 201 with the same body; conflict 409 | OPEN (API owner) | 012, 013 |
| CLAR-012 | X3 vs AC4 | X3 says "does not start"; AC4 says health fails and no traffic | Start-up behaviour | Not asked. Default: readiness DOWN, process up (AC4 is the testable statement) | OPEN (non-blocking) | 016 |
| CLAR-013 | BR4; story §3; S-07; API v4 line 3232 | Reference data A held by no role; owner-per-key and "Risk where a threshold moves" routing undefined | Who may approve | Not asked. Default for RWB-E1-043 and RWB-E1-037: Reference data A to RW-COE (owner) and RW-RISK (DL01); routing not encoded. This story enforces only author <> approver | OPEN (RWB-E1-043, RWB-E1-037, business) | 014 |
| CLAR-014 | Story §13 vs AC8 | §13: environment settings come from the environment; AC8 loads table values for an ENVIRONMENT-kind key | Value source | Not asked. Default: `value_source` column; TABLE unless the setting already comes from a Spring property or the secret store | OPEN (non-blocking) | 024, 012 |
| CLAR-015 | RWB-E1-043 §3 line 45 | Business date source (`v_ace_batch_status`) arrives later | Load check, GET | Not asked. Default: interim Asia/Bangkok date behind `BusinessDateProvider` | OPEN (non-blocking) | 023 |
| CLAR-016 | Story §12 event; finding 116 | One `versionNo` for a multi-key load; event not in the catalog | Payload | Not asked. Default: §11.4 payload | OPEN (event catalog owner) | 018 |
| CLAR-017 | Finding 110 | Seed provenance and in-force date | Seed rows | Not asked. Default: seed identity UUID, approver NULL, valid_from 2026-11-02, baseline approved by the reviewed catalog PR | OPEN (non-blocking) | 006 |
| CLAR-018 | D-RCV-36 §3.1; finding 108 | Six keys lack kind, type, owner, range, required flag | Catalog rows | Not asked. Default: §12.4, owners and used-by labelled assumptions | OPEN (non-blocking) | 024 |
| CLAR-019 | Pack §3.6; finding 126; gap E1042-SP-DG-11 | 503 message ID undecided. The pack's candidate MSG-GEN-006 says the request "is queued and will be retried" (Standard v4 line 73), which is false for a failed read; no other message fits | Problem on outage | Not asked. Default (revision 4): status-only 503 Problem, no message ID, no retry promised (SPEC-025, E7). Revision 5: API v4 `E503` (lines 6028-6029) names MSG-P7-003 and MSG-GEN-006; MSG-P7-003 is used for the approve 503 (finding 132) and neither fits the read; the conflict is recorded in gap E1042-SP-DG-11 with both citations, Blocker = No. Decision needed from the message owner: add a message for an unavailable dependency on a synchronous read whose text promises no retry, or name an existing ID | OPEN (message owner) | 025 |
| CLAR-020 | Story §13 package; plan input 5; phase0 A-01; finding 129 | No `casewf` module in the baseline; the module map is RWB-TE-001's | Package | Not asked. Settled by TE1S SPEC-001, SPEC-022 and SU-08 (a), (e) [S-26]: `casewf.config` with published `casewf.config.api`, as story v7 §13 names it (gap E1042-SP-DG-14) | RESOLVED | 026 |
| CLAR-024 | Story §17; Personal Data Inventory v4 lines 676-677 vs Physical Schema v6 lines 4345-4346; reviewer candidate RV3-DG-03 | Are `author_user_id` and `approver_user_id` personal data? The Inventory says yes (staff identifier); the schema says `is_personal` false | Logging, events, responses, tests | Not asked. Default: personal (protective reading, the Inventory being the PDPA source); SPEC-027 controls. Data protection owner to confirm and the schema owner to correct `is_personal` (gap E1042-SP-DG-15) | OPEN (non-blocking; data protection owner) | 027 |
| CLAR-025 | AGENTS §7 (a plan that touches more than one module "goes back to the analyst before any code is written") and §9; TE1S SU-08 (c), (d); finding 140 | The plan changes P3 `casewf` and P4 `access`: two new `access.api` types (`MessageResolver`, `CapabilityCheck`) and the additive `ApiProblemException` constructor with its rendering | Plan routing | Not asked (AGENTS §10.6, L-RCV-03). Open item to the analyst, citing AGENTS §7: the two-module scope goes to the analyst before any code is written. The spec continues; no analyst approval is claimed. The P4 change is kept to those two types plus the constructor and its rendering (gap E1042-SP-DG-16) | OPEN (analyst; before the build) | 020, 022, 025, 026 |
| CLAR-026 | Personal Data Inventory v4 (no rows for `parameter_catalog` / `parameter_value` `created_by`, `updated_by`) vs the same Inventory's audit columns on other tables (personal "Yes") and Physical Schema v6; candidate RV4-DG-01 | Are the audit columns of the parameter tables personal? | Logging, tests | Not asked. Default: personal (protective reading); data protection owner adds the rows (gap E1042-SP-DG-17) | OPEN (non-blocking; data protection owner) | 027 |
| CLAR-021 | E6, E10; S-08; story v7 §13, §14; gap E1042-SP-DG-10 | No message for an unknown reference load, nor for a load refused because `rwb.p3.configservice` is off (story §13 "value loads are refused"; §14 lists none); MSG-P4-003's text "This case is not in your scope." is case-oriented | 404 text | Not asked. Default: existing MSG-P4-003 for both, the flag-off one raised by RWB-E1-043 (E43S SPEC-018, -026; D-RCV-36 flag rule "404") | OPEN (message owner, RWB-E1-043) | 017, 021, 025 |
| CLAR-022 | RWB-E1-043 v7 §3 line 41 (table codes); RWB-E1-043 v7 §13 line 298 vs line 303 (column definitions); finding 127; gaps E1042-SP-DG-07, E1042-SP-DG-12 | RWB-E1-043 v7 expects this story to serve "the list of reference table codes" (line 41) and to supply the column definitions per table code "from the parameter catalog of RWB-E1-042" (line 303). RWB-E1-043 v7 line 298 says the reference data administrator loads those definitions. Story v7 RWB-E1-042 defines neither (its §12-§13 have no table-code list and no column-definition field; §12.4 of this spec has no such row) | Interface; catalog content | Not asked. Settled for this spec with citations. **Table codes:** not served here; codes and dispatch are RWB-E1-043's (D-RUN-10, D-RUN-11); this story exposes only `ParameterLoadHandler.TABLE = "PARAMETER"`. **Column definitions:** this story does **not** provide them. It provides the mechanism only: the catalog file and its checks (SPEC-003), the generated keys with `byName` (SPEC-005), `ParameterService` (SPEC-007), STRING values up to 400 characters (`param_value varchar(400)`), and `PARAMETER` loads (SPEC-012). **Owner of the definition keys, their grammar and the row check: RWB-E1-043** (E43S SPEC-RWB-E1-043-003: keys `refdata.columns.<code>`, grammar A-34; E43S SPEC-029: 12 rows added to the catalog file and to RWB-E1-043's own migration, default `none`). **Owner of the definition values: each table's story**, loaded by the reference data administrator through the `PARAMETER` branch (RWB-E1-043 v7 line 298; E43S "Seed ownership": DELEGATION_LIMIT RWB-E1-038, ROLE/TEAM/QUEUE RWB-E1-019, PRODUCT_PARAMETER RWB-E1-045, DOCUMENT_TYPE RWB-E1-025, TEMPLATE RWB-E1-046) | OPEN in register (RWB-E1-043 story text to be reworded); settled for this spec | 003, 005, 017 |
| CLAR-023 | Approval after `validFrom` has passed; rollback of a non-approved load | Not in the sources | 409 rules | Not asked. Default: both refused with MSG-P3-027 (§8) | OPEN (non-blocking) | 014, 015 |

## 20. Design evidence and status

No Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5): N/A. No UI in scope. Contract
artefacts (`contracts/backend-apis.json`, `frontend-integrations.json`) are not written: the run's file list
is fixed to seven files, and the one exposed operation is in API v4 unchanged; §11 holds the contract.

```text
MCP_STATUS_SUMMARY: No MCP connected (RUN-BRIEF rule 5); no Figma link; not needed (no UI).
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New configuration service in P3 casewf.config (published casewf.config.api) on RWB-TE-001's module homes, with additive P4 access.api seams; backend only; GET /admin/parameters implemented for the first time; loads served through a published interface that RWB-E1-043 exposes (D-RUN-10); no OpenAPI change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: no parameter code in this repository; GET exists in API v4 but not in code]
REQUIREMENT_COVERAGE_SUMMARY: All 7 BRs, 11 ACs, 10 exception paths, 10 flow steps, 5 preconditions, 3 transitions, authority, 5 contract items, messages and 4 guardrails mapped; TC-12 is blocked by later stories, not by a missing rule.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 57] [COVERED_RULES: 57] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
SPEC_CLARIFICATION_STATUS: OPEN_ITEMS_RECORDED [OPEN_ITEMS: 25] [BLOCKING: 0] [UNBLOCK_ACTION: orchestrator applies shared-updates.md; owners answer the open items; none blocks planning]
```

The two source contradictions (X3 vs AC4; story §13 vs AC8) and the ambiguities are settled by labelled
defaults (CLAR-012, CLAR-014 and the rest) and recorded as document gaps, so they are counted as covered,
not as open contradictions. Revision 4 adds no requirement row; it changes how SPEC-005, -013, -014, -016,
-019, -020, -021, -024 and -025 meet their rows (findings 119-128) and adds TC-32 to TC-34 (tests now
TC-E1-042-01 to -34; TC-12 Blocked). Two further source conflicts found in this round (RWB-E1-043 v7 line 298 vs
303; MSG-GEN-006 wording), one silence (no flag-off refusal message in story §14) and the `README.md`
coverage note that contradicts D-RCV-40 are recorded as gaps E1042-SP-DG-10 to -13, Blocker = No.

Revision 5 (remediation run 3, findings 129-134 of REVIEW-RWB-E1-042-SPEC-005) adds no requirement row. It
moves the service to `casewf.config` / `casewf.config.api` and the two P4 seams to `access.api` on RWB-TE-001's
homes (finding 129; PRE-7; CLAR-020 resolved); fixes the `used_by` grammar (`;`, finding 130); brings the
build-check logic under the tooling coverage gate and records the generator exception (finding 131); answers
a recorder failure with 503 MSG-P7-003 (finding 132); adds TC-35 to TC-45 (tests now TC-E1-042-01 to -45;
TC-12 Blocked; finding 133); carries the four review-3 plan inputs (§12.14); and treats author and approver
IDs as personal data (CLAR-024). Open items: 23 − CLAR-020 + CLAR-024 + CLAR-025 = 24, none blocking. New
gaps E1042-SP-DG-14 to -16 and the extended SP-DG-11 are Blocker = No.

Revision 6 (remediation run 4, findings 135-142 of REVIEW-RWB-E1-042-SPEC-006) adds no requirement row. The
E7 503 and every refusal are raised as the published `ApiProblemException` (status and message ID; status-only
for E7) and rendered by `access.internal.ApiExceptionHandler`; no P3 code calls `ProblemFactory` (135).
T-TE001-14's expected sets are extended with the new published types and named interface (136). The handler's
new branch logs message ID, status, `traceId` and cause class only (137). One credential-name rule (138).
TC-10 (b) forces the failure inside the rollback's own transaction (139). The two-module scope is an open
item to the analyst (CLAR-025, 140). Callers of `casewf.config.api` sit in P3 (141). Housekeeping (142).
Audit columns are treated as personal (CLAR-026, gap E1042-SP-DG-17). Review-4 plan inputs are in §12.14.
Open items: 24 + CLAR-026 = 25 (CLAR-025 reworded, still open), none blocking. Tests stay TC-E1-042-01 to -45.

Revision 7 (remediation run 5, findings 143-148 of REVIEW-RWB-E1-042-SPEC-007) adds no requirement row and no
test. Tooling coverage joins RWB-TE-001's one combined bundle (143). `ApiProblemException`'s new form gains an
optional `detail` and constructor guards, and RWB-TE-003 is told of the new branch (144). The business-date
seam states a no-cycle constraint and defers the route to E43S R24 (145). TC-29 (b) asserts the exception and
`casewf.config` logging only; rendering stays in TC-30 (146). §7.3 lists `created_at`, `created_by`,
`is_active` and `state` (147). Housekeeping (148). Housekeeping (148). Review-5 plan inputs are in §12.14. Open items stay 25.

Revision 8 (remediation run 6, findings 149-150 of REVIEW-RWB-E1-042-SPEC-008, and D-RUN-18) adds no requirement
row and no test. The load-side audit-column assertions move to TC-40 and TC-11 (149); class-set wording, the
E43S revision and the E44S line citations are corrected (150). Under D-RUN-18 the §4.3 business-date seam may be
filled by a P3 → P1 read, and the reference-load handler SPI is P4's (§4.3). Open items stay 25.
