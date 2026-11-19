---
title: "Spec gate review round 5: RWB-E1-044 (spec v14-5)"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Specification (Compliance Reviewer, spec-gate mode)
round: 5 (round 1 is `spec-gate-review.md`, S01 to S11; round 2 is `spec-gate-review-2.md`, S10 residual and S12 to S15; round 3 is `spec-gate-review-3.md`, S16 to S19; round 4 is `spec-gate-review-4.md`, S20 to S23)
date: 2026-11-18
result: FAIL (0 Critical, 0 High, 0 Medium, 3 Low; Low only, REVIEW_GATE_WARNING applies)
---

# Spec gate review round 5: RWB-E1-044

## 1. Scope

Reviewed, all under `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/`: `spec.md` (v14-5, read in full),
`contracts/backend-apis.json` and `contracts/frontend-integrations.json` (both parse as JSON, `specVersion` `v14-5`),
`assumptions.md`, `document-gaps.md`, `shared-updates.md`, `compliance-validation.md`, `gate-response.md` (round 4
section in full) and `agent-run-log.md` (run 4 entry). The `*.run4.*` copies were used only to see what changed.

Checked against:

- `review/spec-gate-review-4.md` (S20 to S23 and the section 5 observations).
- `AI-SDLC-BUILD-LOG.md` section 1, **D-RUN-17** (2026-11-18T00:55), and the event rows 2026-11-18T00:55:29 (round-4
  result; D-RUN-17; RWB-E1-044 "Gate triage", REMEDIATE: "S20 report 0 unresolved; S21 per D-RUN-17; S22 TE-001
  SPEC-020(b) wins (passed gate, owns the tooling); S23 name the key column; align paths to TE-001 v4; re-gate as
  review-5"), 01:10:10 (usage-limit stop) and 01:13:36 (run 4 resumed). The triage and D-RUN-17 are orchestrator
  (Claude Code) rulings. I checked how they were applied and did not re-open them.
- RWB-TE-001 v4 spec (`aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md`, passed its spec gate in round 5):
  SPEC-020, SPEC-022 and its Relocation table, SPEC-023, SPEC-024, SPEC-025, the Unit Test Applicability backend row,
  T-TE001-10, T-TE001-12. For corroboration only, the RWB-TE-001 plan now on disk (`plan/plan.md` v1, written 01:17,
  not yet through its plan gate): property-split table, coverage gate edit, `casewf/migration/RecoveryFlywayConfigTest`.
- Code and SQL: `platform/internal/RecoveryFlywayConfig.java` (conditional, record first parameter of
  `recoveryFlyway`, `@Bean(initMethod = "migrate")`), `RecoveryProperties.java`, `PlatformConfig.java`,
  `PlatformInfoController.java`, `AceRecoveryApplication.java`; every `@EnableConfigurationProperties` use
  (`PlatformConfig`, `TemporalConfig`, `DroolsProperties`, `BlobDocumentStore`) and no `@ConfigurationPropertiesScan` in
  `backend/src`; `application.yaml` (`hibernate.default_schema: ${rwb.schema}`, `rwb.schema: recovery`, no lazy
  initialization); `backend/build.gradle.kts` (coverage tasks lines 131 to 157, `recoveryIntegrationTest` tag filter);
  `.gitlab-ci.yml` `backend-recovery-it` rules; `infra/postgres/schema/01-ace-schema-v1.sql`;
  `infra/postgres/init/00-roles-and-databases.sh`, `20-grants.sql.inc`; `RecoveryDatabaseIT.java`.
- `aisdlc/RUN-BRIEF.md`; `aisdlc/.github/rules/pdlc.md` (lines 23 to 25), `planning-execution-gates.md` (lines 8, 39 to
  46, 62); `aisdlc/.github/agents/specify.agent.md` (clarification workflow, lines 294 to 303).

No git command was run. No container or build was run in this round. Only this file was written. No question was put to
the user (L-RCV-03).

## 2. Round-4 findings

| Finding | Severity (round 4) | Triage (00:55:29) | Status | Evidence |
|---|---|---|---|---|
| S20 `CONTRADICTIONS: 8` fails the planner's upstream gate | Medium | Report 0 unresolved | **CLOSED** | Status line 640 reads `[MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]` and says the count is of unresolved contradictions, as `planning-execution-gates.md` line 44 and `implementation-execution-gates.md` line 68 read it. A table under it lists the eight settled ones (DG-L01, -L02, -L04, -L05, -L09, -L11, -L12, -L13) with the sources and how each was settled, and line 653 says why DG-L03, -L06, -L07, -L08 and -L10 are gaps, not contradictions. `document-gaps.md` still holds all 13 rows; none is merged or deleted. `compliance-validation.md` "Status lines" row updated to match. The 28 coverage rows (spec lines 101 to 128) match `TOTAL_RULES: 28` |
| S21 MAIN baseline sequencing marked resolved | Low | Per D-RUN-17 | **CLOSED** | SPEC-014 "Baseline and sequencing" records D-RUN-17: E1-044's code gate runs after RWB-TE-001 merges, RWB-TE-001 SPEC-024 lifts the main scope, this story tests only the classes it changes and its tooling, the gate stays at 80% on four counters with no exclusion or waiver, and a bundle below 80% at the code gate is a reported blocker. The baseline figures match RWB-TE-001's Unit Test Applicability backend row. CLAR-011 is now RESOLVED on a recorded decision, so the round-4 objection no longer applies. OI-E044-K is closed in `shared-updates.md`; ASM-E044-07 and the backend main Unit Test Applicability row agree. One citation in the same paragraph is wrong (S26) |
| S22 SEAM-E044-04 and OI-E044-H against RWB-TE-001 SPEC-020 (b) | Low | TE-001 SPEC-020 (b) wins | **CLOSED** | SPEC-014 now gates on RWB-TE-001's one combined `BUNDLE` rule: the whole `recovery/**` main tree plus test-scope tooling, LINE, INSTRUCTION, BRANCH and METHOD at 0.80, `test` execution data, tasks outside `check`. This matches RWB-TE-001 SPEC-020 (a) to (d), its Unit Test Applicability backend row and T-TE001-10. Rule MAIN, rule TOOLING and both TOOLING tasks are withdrawn (the only mentions left are the "Withdrawn" paragraph, SEAM-E044-04 history and closed OI-E044-H). E1-044's only build edit is to add its own tooling package to `classDirectories` of both tasks, or nothing if RWB-TE-001's filter already covers it. The RWB-TE-001 plan's include is `architecture/boundary/**`, so the edit will be needed for an `architecture.migration` package, and the spec allows for that. SEAM-E044-04 names RWB-TE-001 as an upstream dependency and claims none of its scope |
| S23 T-044-17 (f) leaves the key column unnamed | Low | Name the key column | **CLOSED** | T-044-17 (f) uses `account_id bigint REFERENCES public.account(id)` and accepts exactly `42501`. Citations verified: `CREATE TABLE public.account (` at line 16, block closed at line 90, `id bigint not null` at line 43, `pk_account PRIMARY KEY (id)` at line 804. The reason (column resolution before the privilege check once R1 grants USAGE; 42830 and 42703 otherwise) matches the round-4 probe. SPEC-017's BR8 bullet says the same |

Round-4 observations: all handled as text (gate-response round 4, last paragraph), except the `ALTER DEFAULT PRIVILEGES`
one, which belongs to RWB-E1-069 as noted then. Rounds 1 to 3 have no open finding.

## 3. Orchestrator rulings and the RWB-TE-001 v4 layout

| Item | Checked against | Result |
|---|---|---|
| D-RUN-17: TE-001 merges first; E1-044 specified, planned and built against TE-001 v4's layout; code gate after TE-001 merges | Sources and precedence (line 54), Change Scope "Impacted Existing Nodes" and "Inherited Existing Behavior", Dependencies, Trigger table, SPEC-001, SPEC-002, SPEC-011, SPEC-014, SPEC-016, CLAR-008, ASM-E044-01, -19, DG-L06, contracts `packageLayout` | Applied. Every path is the post-TE-001 path: `casewf/migration/RecoveryFlywayConfig.java` (Relocation table: `platform.internal.RecoveryFlywayConfig` to `casewf.migration`, P3, package-private); the `casewf.migration` record of SPEC-023 binding `rwb.schema` and `rwb.flyway.*`; `PlatformInfoController` in `integration.internal` with its own record; `PlatformConfig` and `RecoveryFlags` in P2 `integration.flags`, so T-044-08 rightly drops the `rwb.p3.*` base properties. `RecoveryMigrationLintTest` stays where it is (TE-001 does not move it, SPEC-018 only runs it). No stale `platform.internal` path is used as a target; the remaining mentions are history or "moved from". Neither contract file carries an old path |
| Registration with no condition (SPEC-002) | `RecoveryFlywayConfig.java` (`@ConditionalOnProperty`), the `@EnableConfigurationProperties` pattern, no `@ConfigurationPropertiesScan`, `application.yaml` | Sound. An `@EnableConfigurationProperties` on the conditional class is skipped with it, so a separate unconditional class is required in the case the RWB-TE-001 plan has chosen (registration on `RecoveryFlywayConfig`). The spec covers both cases. The new class is package-private in `casewf.migration`, which is neither a module base package nor a published package, so RWB-TE-001 SPEC-004 (e) and SPEC-025 / T-TE001-14 are unaffected |
| Coverage matches TE-001 SPEC-020 (b) | SPEC-014, Unit Test Applicability (both backend rows), Verification table, ASM-E044-07, CLAR-011, SEAM-E044-04 | Matches. One bundle, four counters, whole main tree with untested classes, test-scope tooling added, test classes excluded, `test` data only, outside `check`, command `./gradlew test recoveryCoverageVerification` (T-TE001-10). Integration coverage is not substituted |
| D-RUN-14 (unchanged from round 4) | SPEC-017, T-044-17 (a) to (e), `20-grants.sql.inc`, `00-roles-and-databases.sh` | Unchanged and still applied as decided. `RecoveryDatabaseIT` has no assertion that R1 or R2 would break |
| D-RUN-07, -08, -09, -13, -14; earlier triage | SEAM-E044-01 to -03, no-waiver ruling, identifiers-only scope, tokenizer, finding multiplicity | Unchanged. No regression found in SPEC-003 to SPEC-013, T-044-01 to T-044-22 or the contracts |

Every ruling is attributed to the orchestrator (Claude Code). No human ruling or disposition is claimed (checked in
`gate-response.md` round 4, `assumptions.md` header, `agent-run-log.md` run 4, SPEC-017). No personal data appears in
the spec set.

## 4. New findings

IDs continue from round 4.

### REVIEW-RWB-E1-044-S24: The rule for merged RWB-TE-001 tests allows only an added `rwb.schema` input, but SPEC-002 and SPEC-003 need more

- **Severity:** Low
- **Affects:** SPEC-002 "Existing tests"; SPEC-003 (where the reporting wrapper sits); Change Scope "Inherited Existing
  Behavior"
- **Evidence:** SPEC-002 says a merged test that binds the migration properties record "without `rwb.schema=recovery`
  gets only that input added … No assertion is changed". Two changes this spec itself requires reach RWB-TE-001 v4's
  tests in other ways:
  1. RWB-TE-001 SPEC-024 requires a `casewf.migration.RecoveryFlywayConfig` test, "configuration built without running
     `migrate`", and T-TE001-12 binds "each new properties record from the existing keys". The RWB-TE-001 plan (not yet
     gated) registers `RecoveryMigrationProperties` with `@EnableConfigurationProperties` on `RecoveryFlywayConfig` and
     binds it in `RecoveryFlywayConfigTest` "from the real `application.yaml`". That is the first case of SPEC-002, so
     E1-044 moves the registration to a new unconditional class. A context built from `RecoveryFlywayConfig` alone then
     no longer registers the record. The test needs the new class added to its configuration, which is not "only that
     input added".
  2. SPEC-003 wraps the migrate call that today is `@Bean(initMethod = "migrate")`, but does not say where the wrapper
     sits. The RWB-TE-001 test calls `recoveryFlyway(...)` directly and never runs `migrate`. If the wrapper puts the
     migrate call inside `recoveryFlyway`, that test runs a migration against a mocked data source.

  "Inherited Existing Behavior" lists the RWB-TE-001 state that must stay green (layout, module map, boundary tests,
  coverage wiring), but not RWB-TE-001's SPEC-024 and T-TE001-12 tests.
- **Failure scenario:** The builder follows SPEC-002 literally. The moved registration breaks the merged binding test,
  and the only allowed change (add `rwb.schema`) does not fix it. The builder then breaks a stated rule, or adds a
  test-side workaround that nobody reviews against a rule. Or the wrapper is put in the factory method, and a merged
  unit test starts to need a database.
- **Required fix:** In SPEC-002 "Existing tests", widen the allowed change to exactly two things, with no assertion
  changed. (a) Add `rwb.schema=recovery` where the test does not already bind it. (b) Add the unconditional registration
  class to the test's configuration where SPEC-002 moves the registration. In SPEC-003, state that `recoveryFlyway(...)`
  still builds and returns the configured Flyway without migrating. The reporting migrate runs only at bean
  initialisation, so a direct call (RWB-TE-001 SPEC-024) never migrates, and T-044-09 can drive the wrapper with a
  mocked `Flyway`. Add RWB-TE-001 SPEC-024 and T-TE001-12 to the RWB-TE-001 state that must stay green.

### REVIEW-RWB-E1-044-S25: The spec makes the E1-044 plan read merged RWB-TE-001 code, which does not exist when the plan stage can start

- **Severity:** Low
- **Affects:** Change Scope "Dependencies"; SPEC-002 ("the E1-044 plan reads it from the merged code"); SPEC-014 ("The
  E1-044 plan records the report produced on the merged RWB-TE-001 code as its baseline"; "If the merged build file
  differs … the E1-044 plan stops"); T-044-08 ("The plan re-checks against the merged RWB-TE-001 code");
  ASM-E044-19
- **Evidence:** D-RUN-17 says E1-044 is "specified, planned and built against TE-001 v4's package layout" and that "its
  code gate runs after TE-001 is merged". It puts a merge-order condition on the code gate only. On 2026-11-18 RWB-TE-001
  is in its Plan stage (build log 00:39:15, 00:50:23, 01:13:36), so nothing is merged. Five places in the spec make the
  E1-044 *plan* depend on merged RWB-TE-001 code: the record class name, which registration case applies, whether the
  coverage filter already covers the tooling package, the baseline report, and the stop-and-report check. The spec does
  not say what the planner does if it runs before that merge, and no build-log row holds the E1-044 plan until
  RWB-TE-001 merges. `planning-execution-gates.md` (lines 39 and 43) forbids final plan outputs while a hard-gate
  precondition is unresolved. AGENTS.md §9 needs the plan to name every file and test.
- **Failure scenario:** The spec passes and the orchestrator starts the E1-044 planner while RWB-TE-001 is still being
  planned or built. The planner cannot read the merged code that the spec points it to. It either stops as `BLOCKED`,
  or it quietly reads RWB-TE-001's plan or spec instead. The second path drops the merged-code check that ASM-E044-19
  depends on, and no one records that it was dropped.
- **Required fix:** In "Dependencies" and ASM-E044-19, say which input the E1-044 plan uses when RWB-TE-001 is not yet
  merged. The suggested reading of D-RUN-17: the plan uses RWB-TE-001 v4 and RWB-TE-001's gated plan for the class
  names, the registration case and the coverage include. The check against merged code (and the baseline report)
  becomes the Implementation Builder's first step, before any E1-044 code, and keeps stop-and-report. Change the
  "plan reads / plan stops / plan records" wording in SPEC-002, SPEC-014 and T-044-08 to match. If the orchestrator
  wants the E1-044 plan held until RWB-TE-001 merges, record that ruling instead and cite it.

### REVIEW-RWB-E1-044-S26: Two references to RWB-TE-001 v4 are inaccurate

- **Severity:** Low
- **Affects:** SPEC-014 "Baseline and sequencing"; Trigger and preconditions, row "module folder and boundary test exist"
- **Evidence:**
  1. SPEC-014 says "RWB-TE-001 SPEC-020 quotes the same figures". RWB-TE-001 SPEC-020 quotes no figures. The baseline
     (LINE 133/415, BRANCH 25/92, INSTRUCTION 686/2174, METHOD 41/135) is in RWB-TE-001's Unit Test Applicability
     backend row.
  2. The Trigger row says RWB-TE-001 provides "the 19 module packages, including `recovery.casewf.migration`".
     `casewf.migration` is not one of the 19 modules. It is a sub-package of P3 `casewf`, and it exists because the
     SPEC-022 Relocation table moves `RecoveryFlywayConfig` there. RWB-TE-001 SPEC-001 creates only
     `recovery.<name>`, `.api` and `.internal`.

  RUN-BRIEF rule 8 requires citations by document and section. A wrong section sends the planner and later reviewers to
  the wrong place.
- **Failure scenario:** A reader checks SPEC-020 for the baseline and does not find it. Or a reader takes
  `casewf.migration` for a map module and expects a `package-info.java` or a map entry for it, which RWB-TE-001 does not
  create.
- **Required fix:** Cite "RWB-TE-001 Unit Test Applicability (backend row)" for the figures. Reword the Trigger row: "the
  19 module packages (RWB-TE-001 SPEC-001) and the `casewf.migration` sub-package that holds `RecoveryFlywayConfig`
  after the SPEC-022 relocation".

## 5. Observations (no change required for this gate)

- **For the E1-044 planner.** The RWB-TE-001 plan (ungated) names the P3 record `RecoveryMigrationProperties(String
  schema, Flyway flyway)`, registered on `RecoveryFlywayConfig`. That is the first case of SPEC-002, so the
  unconditional class is needed. Its tooling include is `th/co/scb/ace/demo/recovery/architecture/boundary/**`, so the
  SPEC-014 edit is needed for an `architecture.migration` package. These names may change at RWB-TE-001's plan gate.
- **`OPEN_ITEMS: 9`.** `specify.agent.md` uses `OPEN_ITEMS` for unanswered CLAR items (step 4). This spec uses it for
  the open-item candidates of other owners and says so on the same line. That reading is also used by the sibling
  RWB-TE-001 (`RESOLVED [OPEN_ITEMS: 2]`). The planner gate reads the CLAR rows (`planning-execution-gates.md` line 8),
  and all 13 are RESOLVED. No change is needed. If the orchestrator wants one meaning across stories, it can rule on it.
- **Run 4 interruption.** The `agent-run-log.md` run 4 entry does not record the usage-limit stop (build log 01:10:10)
  or the resume (01:13:36). The outputs are consistent (all at v14-5 and run 4, with audit copies present), so nothing
  appears to be lost. The build log is the record.
- **CI trigger.** `.gitlab-ci.yml` `backend-recovery-it` runs on changes to `RecoveryFlywayConfig.java`, `db/**` and
  `infra/postgres/**`. The E1-044 merge request touches the first and the last, so the container tests run. A later
  change to only the new registration class or the migration properties record would not trigger them. That is D-RCV-44
  scope, outside this story (D-RCV-05: no CI change here).

## 6. Required checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint in scope (NO_API_CHANGE). The job-monitor read path, TC-E1-044-10 and the §10 read and rerun authority are out of scope by D-RCV-12, with no owner (DG-L10, OI-E044-G). The migration account's rights follow D-RUN-14 exactly. The ACE DBA role, every table privilege in `public`, `CREATE` on `public` and `ADMIN` are declined |
| Customer and account data protection | Pass. Fixtures are synthetic. `rwb_migrator` cannot read ACE tables without `SET ROLE` (T-044-17 (d), (e)). BR8 is L-FK-OUTSIDE in every environment, plus the database refusal against this repository's grants, with the key column now named (T-044-17 (f); S23 closed). The residual `SET ROLE` path is recorded for confirmation (OI-E044-J) |
| Audit logging for sensitive financial actions | Not applicable. There is no case or decision change. The run record is the history table and the MSG-P3-016 ERROR line (ASM-E044-02, OI-E044-A) |
| KYC, AML, suitability, consent, approval | Not in scope |
| Frontend integration versioning and error contract | Not applicable to code (UI out of scope; NO_API_CHANGE). Both contract files parse and are at `v14-5`, with post-TE-001 paths |
| Secrets and environment configuration | Pass. Migrator credentials come from the environment or the key store. The schema pin holds with Flyway on or off, because the registration has no condition (T-044-08). Container passwords are synthetic |
| Test coverage and evidence | Planned on RWB-TE-001's combined bundle (SPEC-020 (a), (b)): 80% LINE, INSTRUCTION, BRANCH and METHOD, whole main tree with untested classes, this story's tooling added, test classes excluded, `test` data only, no waiver. Container tests T-044-10 to T-044-18 are kept apart. Sequencing set by D-RUN-17. The rule for merged tests is S24, and the plan-time inputs are S25 |
| Frontend and backend applicability | Frontend `NOT_APPLICABLE` is justified (story v7 §15; no `frontend/` change). Backend `REQUIRED` on both rows |
| Precedence and invented requirements | No invented financial, regulatory or security requirement. D-RUN-17 and the round-4 triage are applied as orchestrator rulings. All 13 DG rows are Blocker = No, and the status line counts unresolved contradictions (0) |
| Personal data in artefacts | None. Roles are named by title. There are no personal names, IDs or account numbers |

## 7. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 0 | — |
| Low | 3 | S24, S25, S26 |

Round-4 status: S20, S21, S22 and S23 are all **CLOSED**, as the 00:55:29 triage directed. D-RUN-17 is applied: every
E1-044 path, test and contract matches RWB-TE-001 v4's layout, and the coverage gate matches RWB-TE-001 SPEC-020 (b). No
regression was found.

The three new findings are text corrections. S24 sets the allowed changes to merged RWB-TE-001 tests and where the
SPEC-003 wrapper sits. S25 states which input the E1-044 plan uses while RWB-TE-001 is not merged (or records an
orchestrator hold). S26 fixes two cross-references. None of them changes a requirement, a rule, a test ID or the
coverage gate.

`REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.`

Under D-RUN-09 the orchestrator does not accept a Low-only failure. It remediates and re-gates, or sends a Low that
cannot be fixed to the engagement lead.

**Overall: FAIL (Low only: 0C / 0H / 0M / 3L)**
