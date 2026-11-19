# Spec gate review: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-003` |
| Gate | Specification gate (fresh review under D-RUN-05) |
| Artifact under review | `output/INC-003-epic-1-RWB-E1-042/_v2-baseline/specify/spec.md`, `compliance-validation.md`, `assumptions.md` (16 Nov 2026, written for the real ACE monorepo) |
| Baseline | Document set v14: increment card INC-003, Epic 1 story files v7, ADR v3, Decision Log v10, D-RCV-35, D-RCV-36, Physical Schema v6, API Specification v4, the E1-042 clarification folder (read only) |
| Repository | `<repo>` at commit `c22ee73` (platform baseline `751909e`); `aisdlc/evidence/phase0-standards-audit.md` |
| Reviewer | Compliance Reviewer (agent run), 2026-11-17 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-002` (16 Nov 2026, PASS). That review is not repeated here; it passed the spec against the ACE monorepo layout and missed the items below. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 4 | Blocks the handoff to the Implementation Planner |
| Medium | 7 | Blocks the handoff |
| Low | 7 | Visible; human disposition required |

The spec is not ready for planning. Its migration design contradicts itself and the repository's lint.
It drops two acceptance criteria that are in story v7. It treats behaviour from later stories as
existing. It also says that all open items are resolved, which is not true.
The parts that hold are the story intent, BR1 to BR7, the read contract, the exception paths and the
authority model. The Technical Specifier should revise the spec, not rewrite it.

## Answers to the specific checks

**1. One migration file, and who owns the seed rows.**
- The spec contradicts itself. Its re-baseline table (spec.md:26) requires one file,
  `V0042__rwb_e1_042_parameter_catalog_and_seed.sql`. Its "Data and migration" section
  (spec.md:200-207) requires two files, `V042_1__parameter_catalog.sql` and `V042_2__parameter_seed.sql`.
- The two-file design breaks D-RCV-28 (Decision Log v10, "Decisions taken", D-RCV-28). It also fails
  this repository's lint:
  - `RecoveryMigrationLintTest.java:25` rejects the name pattern.
  - `RecoveryMigrationLintTest.java:94-95` reports a "second non-fix file for story".
- The seed rows belong to **RWB-E1-042**, inside its single migration. Evidence:
  - Story v7 RWB-E1-042, §3 (line 39): the catalog seed file is owned by RW-COE with the Epic 1 entries.
  - Story v7 RWB-E1-042, §4 step 4 (line 49): Flyway loads the catalog rows and the default values.
  - Story v7 RWB-E1-042, §13 (line 257): the seed is generated from the catalog file.
  - RWB-E1-043 v7 §3 (line 41) needs RWB-E1-042 to be done and already serving `refdata.cache.ttl-seconds`.
  - RWB-E1-043 BR1 (line 162) does not list `PARAMETER` among its table codes.
  - Physical Schema v6 seeds no `parameter_catalog` rows.
  - BR7 needs the required values to exist at the first start.
- `aisdlc/docs/architecture/migration-merge-order-map.md:25-26` says seed rows are RWB-E1-043
  reference loads. That is a squad map, so it ranks below story v7 (DOC-GAP-04).

**2. A fixed migration number.**
- Yes. The spec names `V0042` (spec.md:26). `compliance-validation.md:46,67,80` endorses it, and
  says "the plan must not rewrite the SQL".
- D-RCV-28 takes `<seq>` at merge. `RecoveryMigrationLintTest.java:82-84` requires a contiguous
  sequence from V0001. The migration folder is empty today
  (`backend/src/main/resources/db/modulemigration/recovery/README.md:14`), so `V0042` would fail with
  "sequence gap, expected V0001".
- The squad merge-order map plans `V0042` for RWB-E1-033 (`migration-merge-order-map.md:66`).

**3. Plan-level details from the ACE monorepo.** These are listed under "Plan inputs" at the end. They
are not findings.

## Findings

### High

| ID | Severity | Finding | Evidence | Fix required |
|---|---|---|---|---|
| `REVIEW-RWB-E1-042-101` | High | **The migration design contradicts itself and does not conform to D-RCV-28 or the repository lint.** The re-baseline table requires one file, `V0042`, with `${recoverySchema}`. The detailed design requires two files, `V042_1` and `V042_2`, with a Flyway `${schema}` placeholder "(RWB-E1-044)". A planner works from the detailed section. `${schema}` is not defined in this repository: the recovery Flyway bean defines only `recoverySchema`. The spec fixes the number `V0042` instead of taking it at merge, and `compliance-validation.md` forbids rewriting the 10 Nov SQL. That SQL cites Physical Schema v4 as its source and carries the `V0042` name. Maps to SPEC-001, BR1. | spec.md:26, :200-207, :74 ("`RWB_SCHEMA`"); compliance-validation.md:46, :67-68, :79-80; Decision Log v10, D-RCV-28; `backend/.../platform/internal/RecoveryFlywayConfig.java:37`; `backend/src/test/.../RecoveryMigrationLintTest.java:25, :82-84, :94-95`; migration folder `README.md:7-16`; `_v2-baseline/implement/sql/V0042__...sql:10`; `migration-merge-order-map.md:66` | Replace both passages with one rule. The spec must require: one migration file `V<seq>__rwb_e1_042_<name>.sql`, with `<seq>` the next free four-digit number at merge and no fixed number. Line 1 is `-- Story: RWB-E1-042`. DDL and seed are in the same file. The file uses only `${recoverySchema}`. The DDL is guarded, because the tables already exist from Physical Schema v6 locally and later from the RWB-E1-001 baseline. Remove "the plan must not rewrite the SQL". The 10 Nov pack is input to be adapted (renamed, source updated to Physical Schema v6), not a frozen artefact. |
| `REVIEW-RWB-E1-042-102` | High | **AC2 and AC3 are not mapped.** Story v7 §7 has AC2 (hard-coded value caught) and AC3 (catalog complete) as Gherkin scenarios, and the increment card lists 11 ACs. The spec says they were removed on 4 Nov 2026 and maps only AC1 and AC4 to AC11. Its own status line says "9 acceptance criteria", while `compliance-validation.md` says 11 were mapped. TC-E1-042-02 and -03 were downgraded from System to Unit and traced to BRs only. | Story v7 RWB-E1-042 §7 lines 97-108, §16 lines 300-301; INC-003 card "Acceptance criteria" AC1-AC11; spec.md:88-99, :269-270, :314; compliance-validation.md:43, :45 | Add AC2 and AC3 rows to the coverage table, mapped to SPEC-004 and SPEC-003. Restore TC-02 and TC-03 to the story's System level, using fixture modules as story §13 build step 7 says. Delete the "AC cleanup" note and correct the counts. |
| `REVIEW-RWB-E1-042-103` | High | **Behaviour from later stories is presented as existing.** The spec lists "P4 reference-load and approval pattern (RWB-E1-043)" and the "ACE access check" as inherited behaviour. It sends `ParameterVersionApproved` through the outbox publisher "with retry and idempotency" and writes a decision log entry "through the P4 pattern (RWB-E1-043)". In Build Sequence v6 every one of these comes after RWB-E1-042 (order 3). The repository has none of them; the backend holds only the `platform`, `rules`, `workflow` and `documents` skeletons. The planner cannot tell what this story must build and what it may stub. | spec.md:74, :111, :229-230, :249-250; Build Sequence v6 (`docs/increments/build-sequence.md`): RWB-E1-043 order 8 (depends on RWB-E1-042), RWB-E1-008 decision log store 12, RWB-E1-047 flags 16, RWB-TE-006 outbox 23, RWB-E1-022 26, RWB-E1-037 27; RWB-E1-043 card main flow 1-6; API v4 `postAdminReferenceLoadsLoadidApprove` ("writes a decision log entry with decision code AC-VERS"); phase0 audit A-03, A-06 | For each dependency, state what RWB-E1-042 builds now and through which seam. (a) Who builds the P4 `reference-loads` controller and the approve and rollback endpoints in this story's window. One option is a table-code registry that holds only `PARAMETER`, which RWB-E1-043 extends (clarification pack §3.1). (b) Cache refresh before RWB-TE-006: an in-process application event plus the TTL, with the outbox write added when the publisher exists. (c) The decision-log entry (AC-VERS) before RWB-E1-008. (d) The method check before RWB-E1-022 and RWB-E1-037. Mark TC-E1-042-12 as `Blocked` with its exit criterion (OI-E1-042-001). |
| `REVIEW-RWB-E1-042-104` | High | **Approve and rollback cannot find a `PARAMETER` load.** The endpoints are keyed by `{loadId}`. `parameter_value` has no `load_id` in Physical Schema v6, and the `PARAMETER` handler writes `parameter_value` directly with no `reference_version` row. The spec does not say how a load and its rows are linked, so AC7 (author cannot approve) and AC10 (rollback) cannot be built as specified. The clarification pack raised this as OI-E1-042-008, and the spec dropped it. | Story v7 §12 line 217; API v4 `/admin/reference-loads/{loadId}/approve`, `/rollback`; Physical Schema v6 lines 1413-1434 (`parameter_value`), 1437-1467 (`reference_version.load_id`); E1-042 Clarification Pack §3.3 (line 311), §3.7 (lines 394-400), §7 OI-E1-042-008 | Choose and specify the link, for example `load_id uuid` on `parameter_value`, indexed and added in this story's migration (pack option A). Record it as an assumption with a Physical Schema update request. Add approve and rollback by `loadId` to the field matrix and the tests. |

### Medium

| ID | Severity | Finding | Evidence | Fix required |
|---|---|---|---|---|
| `REVIEW-RWB-E1-042-105` | Medium | **The clarification status is wrong.** The spec says the pack's `OI-E1-042-*` items "are carried in the Clarification Log below" and reports `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`. The log holds CLAR-001 to CLAR-008, and none of them is an OI item. The pack lists 11 open items, and at least eight bear on the spec: 001, 002, 003, 004, 006, 007, 008 and 011. The specification gates forbid SUCCESS while a rule is ambiguous. | spec.md:39-40, :291-305, :317; E1-042 Clarification Pack §7 (lines 564-578); `.github/rules/specification-execution-gates.md:92-109` | Bring each OI item into the Clarification Log with a status. Where it is open, give an assumption with its basis and add the matching row to `shared-updates.md` for `docs/open-items.md`. OI-E1-042-009 is resolved by `RecoveryFlywayConfig.java:37`; say so. Set the status line to match. |
| `REVIEW-RWB-E1-042-106` | Medium | **Load idempotency and the rollback request are missing from the contract section.** The story requires idempotency on table, valid-from date and content hash, and says a repeat returns the existing load. API v4 requires a `RollbackRequest` body (`reason`) and documents 409 and 422 with MSG-P3-027, and 409 with MSG-P3-022. The spec's error list has none of these and does not define the repeat behaviour, but it still claims "no contract delta". | Story v7 §12 line 215; API v4 `postAdminReferenceLoads` description and responses, `postAdminReferenceLoadsLoadidRollback` (`RollbackRequest`, 422); spec.md:163-167; Clarification Pack §3.6 (lines 379-383), OI-E1-042-011 | Specify the idempotency key and where the hash is held (`parameter_value` has no `content_hash`). Specify the repeat status (201 with the same body, or 409), the rollback reason and its 422, and which of the generic P4 fields (`changeRequestRef`, `impactSummary`, `rollbackPlan`) apply to `PARAMETER` or are deferred to RWB-E2-041. |
| `REVIEW-RWB-E1-042-107` | Medium | **`CatalogCompletenessCheck` fails a correct catalog.** The spec says the check "fails on a missing key, owner or default". It also defines the five RWB-E1-045 product parameters in the catalog with scope PRODUCT, and those have no default by design. | spec.md:190, :221-223; `_v2-baseline/implement/config/parameter-catalog.csv` rows 10-14; RWB-E1-045 v7 BR2 (line 143); Clarification Pack OI-E1-042-007 (line 458) | Exempt `scope = PRODUCT` from the default rule. Owner, type and range are still required. Add a fixture with a product-scope row. |
| `REVIEW-RWB-E1-042-108` | Medium | **The six D-RCV-36 parameters are under-specified, and the repository's existing literals are not addressed (phase0 A-06).** D-RCV-36 §3.1 names the keys and some values. The spec adds owners and "used by" values as fact without marking them as assumptions, and gives no kind, type, required flag or range. The preserved 13-row CSV does not contain these keys, yet the spec says the pack "fits the v2 baseline". The spec also drops story §13's rule: "Environment settings come from the environment and the secret store; only their catalog entries are in the tables". That leaves the value source for `temporal.target` undefined. The repository already holds `rwb.temporal.namespace: rwb-recovery`, `rwb.drools.kiebase-cache-max: 20` (commented "parameter drools.kiebase.cache.max") and `rwb.temporal.target` as configuration literals, and A-06 assigns them to this story. | spec.md:24, :39, :42-51, :60; D-RCV-36 §3.1 (`docs/decisions/d-rcv-36-temporal-and-drools.md:78-79, :87`); story v7 §13 (line 263); `backend/src/main/resources/application.yaml:90-97`; phase0 audit A-06 (line 24); AGENTS.md §3.2, §4.8, §4.10 | For each of the six keys, define kind, type, unit, range, required flag and value source. Mark owners and "used by" as assumptions. State what this story does with the existing `rwb.*` literals: either it adds ENVIRONMENT catalog entries whose values come from the environment, or it moves the reads to `ParameterService`. Say how `RwbMagicNumberCheck` treats the baseline code, so the first build is not red or silently exempt. |
| `REVIEW-RWB-E1-042-109` | Medium | **The message source is undefined.** The spec cites seven message IDs but not how text is resolved. Physical Schema v6 has no message table, and LOV-REF-TABLE has no `MESSAGE` code. The repository holds platform messages in `ApiError` (README decision 5), and AGENTS §3.6 requires messages from the message table by rule ID. The API `Problem` carries `messageTh`. MSG-P4-001 is used by the 401 path but is missing from story §14. | spec.md:143-156, :166; Physical Schema v6 (no `CREATE TABLE` for messages); `README.md` "Decisions taken while setting this up" item 5; AGENTS.md §3.6; Clarification Pack §6.1-6.2 (lines 513-556), OI-E1-042-004 | Specify the resolver for this story: the fixed catalog behind one seam (pack §6.2), or an extension of the `ApiError` pattern. Specify the EN and TH source and its status (proposed, pending DL10), and add MSG-P4-001. Record the missing message table as an open item. |
| `REVIEW-RWB-E1-042-110` | Medium | **The seed's provenance and in-force date are undefined, and the inherited seed stops the service starting.** The preserved seed writes version 1 as `APPROVED`, with a nil-UUID author, no approver, and `valid_from = 2026-11-30`. Under the spec's own rules, no required parameter is in force before 30 Nov 2026: the value is the approved version with the latest `valid_from` on or before the business date, and the default is used only for non-required keys. `ParameterStartupCheck` would therefore fail readiness in DEV and SIT today (17 Nov). The spec also does not say how a Flyway-loaded `APPROVED` row squares with BR3 and BR4 (approved, maker-checker). | `_v2-baseline/implement/sql/V0042__...sql:436-452` (lines 444, 446-449); spec.md:123, :213-216, :187; story v7 BR3, BR4, BR7 | Define the seed version: a system author identity (not a personal ID), approval semantics (a baseline approved by the reviewed catalog PR, recorded as such), a `valid_from` rule that cannot postdate the first deployment, and the business date the startup check uses. |
| `REVIEW-RWB-E1-042-111` | Medium | **SPEC IDs are referenced but never defined.** The spec maps rules to `SPEC-RWB-E1-042-001` to `-012`, and in one row to `-014`, but has no section that states what each SPEC item is. Tasks cannot be traced to them. `compliance-validation.md` says each is "defined once". | spec.md:81-97, :174; compliance-validation.md:44; `.github/rules/traceability-standards.md:10, :33`; `specification-execution-gates.md:38, :47` | Add a SPEC catalogue (ID, statement, source rule or AC, test case) and fix the 001..014 reference. |

### Low

| ID | Severity | Finding | Evidence | Fix required |
|---|---|---|---|---|
| `REVIEW-RWB-E1-042-112` | Low | The field matrix says `param_key` is the primary key. Physical Schema v6 has `id uuid` as the primary key with `param_key` unique. The FK from `parameter_value` and the partial index are additions that v6 does not contain. | spec.md:121, :200-205; Physical Schema v6 lines 1386-1409, 1413-1434 (no FK or index on either table) | Follow v6 (`id` PK, `uk_parameter_catalog`). List the FK and indexes as this story's additions and raise a Physical Schema update request. |
| `REVIEW-RWB-E1-042-113` | Low | The out-of-scope list names the wrong story for the change checklist and audit report. | spec.md:289 (RWB-E1-048); story v7 §19 line 333 and INC-003 card (RWB-E2-041) | Use RWB-E2-041. |
| `REVIEW-RWB-E1-042-114` | Low | The authority table omits RW-REFADM as a loader. The parameter owner as approver appears only in CLAR-002. | spec.md:234-241; story v7 §3 line 41 | Add RW-REFADM (Reference data C) and the owner-approver row. |
| `REVIEW-RWB-E1-042-115` | Low | The source requirement path does not resolve. `requirement/RecoveryWorkbench_Requirements.md` is not in the workspace; FR-RWB-010 is only in `Traceability_Matrix.md`. | spec.md:8; `aisdlc/requirement/` (Context, README, Traceability_Matrix only) | Cite the Traceability Matrix row and the story file v7. |
| `REVIEW-RWB-E1-042-116` | Low | `ParameterVersionApproved` is a new internal event that the event catalog does not contain, yet the spec says "Contract delta: None". | spec.md:164, :229; story v7 §12 line 219 ("new internal event, see additions"); Event and Messaging Design v4 (0 occurrences) | Declare the event (payload, producer, consumers) as a delta and raise the catalog update. |
| `REVIEW-RWB-E1-042-117` | Low | Parameter naming conflicts are not dispositioned. The spec seeds `case.entry.dpd` and the product-scope `ENTRY_DPD` side by side without stating how they relate (`case.entry.dpd_threshold` is the third name). | spec.md:208, :221; Clarification Pack OI-E1-042-006 (line 573), Appendix A; DL16 | State that `case.entry.dpd` is the GLOBAL key and `ENTRY_DPD` the product key (RWB-E1-045), and record the conflict as an open item. |
| `REVIEW-RWB-E1-042-118` | Low | Carried from `REVIEW-RWB-E1-042-002`: no role holds Reference data A. API v4 states this on the approve operation. RW-RISK is an assumed grant. | API v4 `postAdminReferenceLoadsLoadidApprove` description; story v7 §3 line 41 (DL01) | Keep as an assumption; the grant is loaded through RWB-E1-037. |

## Checks performed

| Check | Result | Evidence |
|---|---|---|
| Change classification (`NEW_STORY`; UI NO; Logic YES; API YES / `NEW_API_REQUIRED`) | PASS | spec.md:62-75; no frontend change; endpoints exist in `api/recovery-api-v4.yaml:4857, :5004` |
| Requirement coverage, BR1-BR7 | PASS | spec.md:81-87 |
| Requirement coverage, AC1-AC11 | **FAIL** | 102 |
| Migration naming, count and placeholder (D-RCV-28, lint) | **FAIL** | 101 |
| Implementable in this repository as specified | **FAIL** | 103, 104, 108, 110 |
| API contract completeness | **FAIL** | 104, 106, 116 |
| Authorization | PASS with Low | Read: Rules and parameters R. Load: Reference data C. Approve: Reference data A. Rollback: Reference data U (API v4 `x-capability`). Findings 114 and 118. |
| PDPA / personal data | PASS | No personal field; DF-REF-132 to DF-REF-158 are all `is_personal = false` (Physical Schema v6 lines 4321-4347). The synthetic user "U-41" only. |
| Secrets | PASS | BR6; `secret = true`, `valueInForce` absent; the secret value stays in the secret store. |
| Audit logging | Depends on finding 103 | Author, approver and times are in `parameter_value`. The AC-VERS decision log entry depends on RWB-E1-008. |
| Error contract | **FAIL** | 106, 109 |
| Unit-test applicability (frontend NO / N/A; backend YES / 80%) | PASS | spec.md:169-174. Coverage verification is not yet in `check` (`README.md`), which is a plan input. |
| D-RCV-35 impact | PASS | Workbench-owned reference data; no `public` read; no inbound load. |
| D-RCV-36 impact | **FAIL** | 108 |
| Traceability (unique SPEC IDs) | **FAIL** | 111 |
| No-question rule | PASS | No question was asked; assumptions recorded. |

## Plan inputs (not spec findings)

These are ACE-monorepo details in the spec, the 10 Nov pack or the baseline plan that the
Implementation Planner must translate to this repository:

1. **Migration folder:** `backend/src/main/resources/db/modulemigration/recovery/`, not
   `recovery/src/main/resources/db/migration/recovery/` (pack §2.6). The file name must match
   `^V(\d{4})__(rwb_[a-z0-9]+_\d{3})_[a-z0-9_]+\.sql$` (`RecoveryMigrationLintTest.java:25`). The
   baseline plan's path with `V0042` (`_v2-baseline/plan/plan.md:46, :80`) must change.
2. **Placeholder:** `RecoveryFlywayConfig` sets `recoverySchema` from `rwb.schema`, and Spring Boot's
   Flyway is disabled (`application.yaml:25-26`). `spring.flyway.placeholders.recoverySchema=${RWB_SCHEMA}`
   (pack §2.2, OI-E1-042-009) does not apply.
3. **Local schema:** while `RWB_LOAD_REFERENCE_SCHEMA=true`, Physical Schema v6 already creates
   `parameter_catalog` and `parameter_value`, owned by `rwb_migrator` (`infra/postgres/init/10-load-ace-database.sh:31-32`,
   `20-grants.sql.inc:19-23`). Flyway baselines at version 0. The guarded DDL must be proved both on
   that schema and on an empty schema.
4. **Migration tests:** replace `tests/test_migrations.sh` (a Docker script) with Testcontainers tests
   tagged `recovery-it` (`recoveryIntegrationTest`, PostgreSQL 16). Keep the pack's negative cases.
5. **Packages:** the code goes in `th.co.scb.ace.demo.recovery.<module>`, not `recovery.casewf.config`.
   The `casewf` mapping comes from the RWB-TE-001 module map (phase0 A-01). One module only (AGENTS §7).
6. **Build checks and generators:** `build-tools/rwb-checks` and the PowerShell tools
   (`Generate-ParameterSeed.ps1`, `Assemble-V0042.ps1`) become Gradle Kotlin DSL tasks or unit-test
   checks, following the `RecoveryMigrationLintTest` pattern. `config/parameter-catalog.csv` does not
   exist in `<repo>` yet.
7. **Feature flag:** add `rwb.p3.configservice` in the `RecoveryFlags` / `RecoveryProperties.P3` /
   `@ConditionalOnProperty` pattern until RWB-E1-047 delivers the flag table (A-06).
8. **Security:** `SecurityConfig` uses `@EnableMethodSecurity` with role authorities. The capability
   check by area and right is RWB-TE-003 / RWB-E1-037 work (A-03).
9. **Errors:** RFC 7807 `Problem` through `ProblemFactory` and `ApiExceptionHandler` (README decision 1;
   A-08).
10. **Health:** readiness probes are enabled (`application.yaml:44-47`). `ParameterStartupCheck`
    belongs in the readiness group.
11. **Outbox:** `outbox_event` exists in Physical Schema v6 (line 1206) with
    `UNIQUE (case_seq, idempotency_key)`. A parameter event has no case. Check that `case_seq` accepts
    null before writing to it.
12. **Coverage:** `recoveryCoverageVerification` is wired but not yet part of `check` (`README.md`).
    The first story's code is meant to add it.
13. **Gradle on this workstation** needs `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=...` (RUN-BRIEF).
14. **OpenAPI:** `api/recovery-api-v4.yaml` already has all four operations. No regeneration of
    `frontend/src/api/schema.d.ts` is needed for this story.

## Gate decision

```text
SPEC_GATE: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 4] [MEDIUM: 7] [LOW: 7]
BLOCKING: YES (High and Medium findings block the handoff to the Implementation Planner)
NEXT_STEP: Technical Specifier revises spec.md for findings 101-111, then this gate re-runs (spec-gate-review-2.md).
```
