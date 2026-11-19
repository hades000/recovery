---
title: "Spec gate review round 6: RWB-E1-044 (spec v14-6)"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Specification (Compliance Reviewer, spec-gate mode)
round: 6 (round 1 is `spec-gate-review.md`, S01 to S11; round 2 is `spec-gate-review-2.md`, S10 residual and S12 to S15; round 3 is `spec-gate-review-3.md`, S16 to S19; round 4 is `spec-gate-review-4.md`, S20 to S23; round 5 is `spec-gate-review-5.md`, S24 to S26)
date: 2026-11-18
result: FAIL (0 Critical, 0 High, 0 Medium, 2 Low; Low only, REVIEW_GATE_WARNING applies)
---

# Spec gate review round 6: RWB-E1-044

## 1. Scope

Reviewed, all under `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/`: `spec.md` (v14-6; every line changed since
`spec.run5.md` read in full, plus Change Scope, Dependencies, Trigger table, SPEC-001 to SPEC-003, SPEC-014, Unit Test
Applicability, Verification table, Clarification Log and Status read again in full), `contracts/backend-apis.json` and
`contracts/frontend-integrations.json` (both parse as JSON, `specVersion` `v14-6`, no other change), `assumptions.md`,
`document-gaps.md` (unchanged since run 5), `shared-updates.md`, `compliance-validation.md`, `gate-response.md` (round 4
and round 5 sections in full) and `agent-run-log.md` (run 5 entry). The `*.run5.*` copies were used to see exactly what
changed.

Checked against:

- `review/spec-gate-review-5.md` (S24 to S26 and the section 5 observations).
- `AI-SDLC-BUILD-LOG.md`: section 1 **D-RUN-17** (2026-11-18T00:55) and **D-RUN-09**; event rows 2026-11-18T00:55:29
  (D-RUN-17; RWB-E1-044 "Gate triage", REMEDIATE: "S20 report 0 unresolved; S21 per D-RUN-17; S22 TE-001 SPEC-020(b)
  wins (passed gate, owns the tooling); S23 name the key column; align paths to TE-001 v4; re-gate as review-5"),
  01:10:10, 01:13:00, 01:13:36. These are orchestrator (Claude Code) rulings. I checked how they were applied and did not
  re-open them.
- RWB-TE-001 v4 spec (`aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md`): Change Scope "New Nodes Required",
  SPEC-001 (c), SPEC-004 (d), SPEC-020, SPEC-022 and its Relocation table (`platform.internal.RecoveryFlywayConfig` to
  `casewf.migration`, P3, `pp`), SPEC-023, SPEC-024, SPEC-025, the Unit Test Applicability backend row, T-TE001-12.
  For corroboration only, the RWB-TE-001 plan on disk (`plan/plan.md`, `data-model.md` §5, `tasks.md` TASK-10, -12,
  `tests/scenarios.md` T-TE001-12). It has no plan-gate review yet (`review/` holds spec-gate reviews only).
- Code spot-checks for the changed text: `platform/internal/RecoveryFlywayConfig.java` (`@ConditionalOnProperty`,
  `@Bean(initMethod = "migrate")`, properties as the first parameter, `configuration.load()` returned without a migrate
  call); every `@EnableConfigurationProperties` use (`PlatformConfig`, `TemporalConfig`, `DroolsProperties`,
  `BlobDocumentStore`) and no `@ConfigurationPropertiesScan` in `backend/src`; `application.yaml`
  (`hibernate.default_schema: ${rwb.schema}`, `rwb.schema: recovery`, no lazy initialisation);
  `backend/build.gradle.kts` lines 131 to 160 (today LINE and BRANCH only, as SPEC-014 and RWB-TE-001 SPEC-020 (a) say).
- `aisdlc/RUN-BRIEF.md`; `aisdlc/evidence/resume-after-usage-limit.md` (RWB-E1-044 row).

No git command was run. No container or build was run. Only this file was written. No question was put to the user
(L-RCV-03).

## 2. Round-5 findings

| Finding | Severity (round 5) | Status | Evidence |
|---|---|---|---|
| S24 Rule for merged RWB-TE-001 tests too narrow; SPEC-003 wrapper placement | Low | **CLOSED** | SPEC-002 "Existing tests" (line 156) lists the RWB-TE-001 tests that bind the record or build `recoveryFlyway` (T-TE001-12 and the SPEC-024 `RecoveryFlywayConfig` test, both quoted correctly from RWB-TE-001 v4 lines 191 and 277) and allows exactly two changes with no assertion changed: add `rwb.schema=recovery`; add the unconditional registration class to the test configuration. Anything else is stop-and-report. SPEC-003 (line 165) states that `recoveryFlyway(...)` builds and returns the configured `Flyway` and never calls `migrate`; the wrapped migrate runs only at bean initialisation. That matches today's factory (`return configuration.load();`) and the RWB-TE-001 plan's direct-call test ("`migrate` never called"). Change Scope "Inherited Existing Behavior" now adds the SPEC-024 tests to the RWB-TE-001 state that must stay green |
| S25 Plan made to read merged RWB-TE-001 code | Low | **CLOSED, with one residual sentence (S27)** | Dependencies (line 75) now reads D-RUN-17 as a merge-order and code-gate condition only: the plan works from RWB-TE-001 v4 and RWB-TE-001's plan once that plan has passed its gate, and a **builder's first step** checks the merged code and records the baseline, keeping stop-and-report. SPEC-002 (lines 144, 147, 149), SPEC-014 (lines 377, 383), T-044-08 and ASM-E044-19 say the same. One sentence in SPEC-014 line 369 still makes the plan decide from "RWB-TE-001's merged filter" (S27) |
| S26 Two inaccurate references to RWB-TE-001 v4 | Low | **CLOSED in `spec.md`** | SPEC-014 line 379 cites RWB-TE-001's Unit Test Applicability backend row for LINE 133/415, BRANCH 25/92, INSTRUCTION 686/2174, METHOD 41/135 (verified at RWB-TE-001 line 160) and notes SPEC-020 quotes none. The Trigger row (line 90) calls `recovery.casewf.migration` a sub-package that the SPEC-022 relocation creates under module `casewf`, not one of the 19 module packages. The new `compliance-validation.md` row for S26 cites the wrong RWB-TE-001 phrase for this (S28) |

Round-5 observations: handled as stated in `gate-response.md` round 5. The SPEC-002 first-case bullet now notes the
RWB-TE-001 plan's choice and that it is not yet gated. Rounds 1 to 4 have no open finding.

## 3. Orchestrator rulings and regression check

| Item | Checked against | Result |
|---|---|---|
| D-RUN-17: TE-001 merges first; E1-044 specified, planned and built against TE-001 v4's layout; code gate after TE-001 merges | Dependencies, SPEC-001, -002, -011, -014, -016, T-044-08, CLAR-008, ASM-E044-01, -19, contracts `packageLayout` | Still applied. No path changed in run 5. The new plan-input reading (TE-001 v4 plus TE-001's gated plan; merged-code check at the builder's first step) puts no merge-order condition on the plan and keeps the condition on the code gate, as D-RUN-17 states it. It is the reading round 5 offered as its first fix, so no new ruling is needed |
| 00:55:29 triage (S20 to S23, alignment) | Status line 641 and the settled-contradiction table; SPEC-014; T-044-17 (f); SPEC-017 BR8 bullet | Unchanged since round 5 (diff empty for these lines). S20 to S23 stay closed |
| D-RUN-14 | SPEC-017 R1 and R2, T-044-17 (a) to (f), OI-E044-I, OI-E044-J, DG-L13 | Unchanged (no diff in SPEC-017, T-044-17, `document-gaps.md`, OI rows) |
| Coverage gate (RWB-TE-001 SPEC-020 (a) to (d)) | SPEC-014, Unit Test Applicability, Verification table | Unchanged: one combined `BUNDLE` rule, four counters at 0.80, whole main tree, test-scope tooling added, `test` data only, outside `check`, no exclusion or waiver. Integration coverage is not substituted |
| D-RUN-07, -08, -09, -13; earlier triage | SEAM-E044-01 to -04, no-waiver ruling, identifiers-only scope, tokenizer, finding multiplicity | Unchanged. No regression in SPEC-004 to SPEC-013, SPEC-015 to SPEC-017, T-044-01 to T-044-22 or the contracts |

Every ruling is attributed to the orchestrator (Claude Code); no human ruling or disposition is claimed (`gate-response.md`
round 5, `agent-run-log.md` run 5, `assumptions.md` header). No personal data appears in the spec set.

## 4. New findings

IDs continue from round 5.

### REVIEW-RWB-E1-044-S27: SPEC-014 still has the plan decide the build-file edit from RWB-TE-001's merged filter

- **Severity:** Low
- **Affects:** SPEC-014 "What E1-044 changes in `build.gradle.kts`", first bullet (spec line 369); TASK planning for the
  `build.gradle.kts` edit; residual of S25
- **Evidence:** Line 369 ends: "If RWB-TE-001's merged filter already takes in this package, no edit is needed; the plan
  states which applies." Round 5 (S25) named "whether the coverage filter already covers the tooling package" as one of
  the five plan-time inputs tied to merged code, and asked for the "plan reads / plan stops / plan records" wording in
  SPEC-014 to change. Run 5 changed lines 377 and 383 but not this sentence. Dependencies (line 75) now says the plan
  works from RWB-TE-001 v4 and its gated plan, so the two places disagree on where this one input comes from. The
  RWB-TE-001 plan (not yet gated) includes `th/co/scb/ace/demo/recovery/architecture/boundary/**`, so for an
  `architecture.migration` package the answer from the plan is "edit needed".
- **Failure scenario:** The planner reads SPEC-014 alone, cannot see a merged filter, and either leaves the edit
  undecided (AGENTS §9 needs the plan to name every file) or treats it as a blocker that the Dependencies paragraph says
  does not exist.
- **Required fix:** Reword the sentence to match Dependencies: "The plan states which applies from RWB-TE-001's gated
  plan (its tooling include); the builder's first step confirms it against the merged `build.gradle.kts` and stops and
  reports on a mismatch (Dependencies, ASM-E044-19)." No other change.

### REVIEW-RWB-E1-044-S28: Two slips in the companion files

- **Severity:** Low
- **Affects:** `compliance-validation.md` row "Coverage baseline citation; `casewf.migration` is a sub-package" (line 55);
  `shared-updates.md` card row 001 (line 17)
- **Evidence:**
  1. The `compliance-validation.md` row supports "`casewf.migration` is a sub-package" with the RWB-TE-001 Change Scope
     phrase "published sub-packages that receive relocated types". `casewf.migration` is not published: RWB-TE-001
     SPEC-025 lists the published packages that hold types as `casewf.rules`, `casewf.timers`, `casewf.workflow`,
     `integration.flags.api`, `access.api` and `dochub.api`, and SPEC-001 (c) gives `@NamedInterface` only to the first
     four of those besides the `api` packages. `casewf.migration` (like `casewf.admin`) is an unpublished sub-package of
     `casewf`. `spec.md` itself does not call it published, so the error is only in the self-check evidence.
  2. `shared-updates.md` row 001 reads "remediation run 4, spec v14-6". v14-6 is remediation run 5 (spec front matter,
     `gate-response.md` round 5, line 45 of the same file).
- **Failure scenario:** A planner or reviewer who follows the self-check citation takes `casewf.migration` for a
  published package and adds a `@NamedInterface` and a map entry for it. RWB-TE-001 SPEC-004 (d) then fails on the
  module map, or the package's public types become callable from other modules. The run label sends the orchestrator
  to the wrong run when it applies the card row.
- **Required fix:** (1) Cite the RWB-TE-001 SPEC-022 Relocation table (`casewf.migration`, P3, `pp`) and SPEC-025 (not in
  the published list) for the sub-package statement, and drop the "published sub-packages" quote. (2) Change "remediation
  run 4" to "remediation run 5" in `shared-updates.md` row 001.

## 5. Observations (no change required for this gate)

- **For the orchestrator: E1-044 plan start condition.** Dependencies makes the E1-044 plan wait for RWB-TE-001's plan
  to pass its gate. On 18 Nov 2026 no RWB-TE-001 plan-gate review exists. The build log has a queue row for RWB-TE-002
  on the same condition (00:59:53) but none for RWB-E1-044. A matching "QUEUED until the RWB-TE-001 plan passes its gate"
  row would make the hold visible.
- **For the orchestrator: build-log record of runs 4 and 5.** The log has no row for RWB-E1-044 run 4 DONE, the
  round-5 gate result or a round-5 triage. `gate-response.md` round 5 and the run-5 `agent-run-log.md` entry say the
  orchestrator's "2026-11-18T00:55 instruction" allowed this stage one more round (review-6). The logged 00:55:29 triage
  row says only "re-gate as review-5". D-RUN-09 alone justifies fixing Low findings and re-gating, so nothing in the spec
  depends on that wording, but the log should carry the rows.
- **For the E1-044 planner: the direct-call test and the compact-constructor check.** The RWB-TE-001 plan's
  `RecoveryFlywayConfigTest` calls `recoveryFlyway(...)` directly, so it builds the migration properties record in code
  rather than binding it. If it builds the record with a schema other than `recovery`, a compact-constructor check
  (SPEC-002 first option) would throw in that test, and neither permitted change covers it, so the build would stop and
  report. The `@Validated` option of SPEC-002 runs at binding only and avoids this. The plan should check the test's
  inputs when it picks the option.
- **For the E1-044 builder: start condition.** The builder's first step checks merged RWB-TE-001 code. If the builder
  were started before that merge, the check finds no `casewf.migration` package and the stop-and-report path applies,
  so the failure is visible, not silent.

## 6. Required checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint in scope (NO_API_CHANGE). Job-monitor read path, TC-E1-044-10 and the §10 read and rerun authority are out of scope by D-RCV-12 (DG-L10, OI-E044-G). Migration-account rights follow D-RUN-14 exactly; the ACE DBA role, table privileges in `public`, `CREATE` on `public` and `ADMIN` are declined |
| Customer and account data protection | Pass. Fixtures synthetic. `rwb_migrator` cannot read ACE tables without `SET ROLE` (T-044-17 (d), (e)). BR8 is L-FK-OUTSIDE plus the database refusal against this repository's grants (T-044-17 (f)). Residual `SET ROLE` path recorded (OI-E044-J) |
| Audit logging for sensitive financial actions | Not applicable. No case or decision change. The run record is the history table and the MSG-P3-016 ERROR line (ASM-E044-02, OI-E044-A) |
| KYC, AML, suitability, consent, approval | Not in scope |
| Frontend integration versioning and error contract | Not applicable to code (UI out of scope; NO_API_CHANGE). Both contract files parse, at `v14-6`, with post-TE-001 paths |
| Secrets and environment configuration | Pass. Migrator credentials from the environment or key store. Schema pin holds with Flyway on or off (unconditional registration, T-044-08). Container passwords synthetic |
| Test coverage and evidence | Planned on RWB-TE-001's combined bundle (SPEC-020 (a), (b)): 80% LINE, INSTRUCTION, BRANCH, METHOD, whole main tree with untested classes, this story's tooling added, test classes excluded, `test` data only, no waiver. Container tests T-044-10 to T-044-18 kept apart. Merged RWB-TE-001 tests stay green with two named, non-weakening changes (S24 closed). Baseline recorded at the builder's first step. The plan-time source of the build-file edit is S27 |
| Frontend and backend applicability | Frontend `NOT_APPLICABLE` justified (story v7 §15; no `frontend/` change). Backend `REQUIRED` on both rows |
| Precedence and invented requirements | No invented financial, regulatory or security requirement. D-RUN-17, D-RUN-14 and the triage rows are applied as orchestrator rulings. All 13 DG rows are Blocker = No; status line counts unresolved contradictions (0) |
| Personal data in artefacts | None. Roles named by title; no personal names, IDs or account numbers |

## 7. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 0 | — |
| Low | 2 | S27, S28 |

Round-5 status: S24 and S26 are **CLOSED**. S25 is **CLOSED** except one sentence, carried as S27. The S20 to S23
resolutions, D-RUN-14 and D-RUN-17 still hold, and no regression was found in the spec's requirements, rules, test IDs,
contracts or coverage gate.

Both new findings are text corrections: one sentence in SPEC-014 (S27), and one citation and one run label in the
companion files (S28). Neither changes a requirement, a rule, a test or the coverage gate.

`REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.`

Under D-RUN-09 the orchestrator does not accept a Low-only failure. It remediates and re-gates, or sends a Low that
cannot be fixed to the engagement lead.

**Overall: FAIL (Low only: 0C / 0H / 0M / 2L)**
