# Plan gate review: RWB-TE-012 (run INC-007-epic-1-RWB-TE-012), round 1

| Field | Value |
|---|---|
| Stage | Compliance Reviewer, plan gate (`planning-execution-gates.md`), round 1 |
| Story | RWB-TE-012 Document storage containers |
| Reviewed | `plan/plan.md` v1, `plan/tasks.md` v1, `plan/data-model.md` v1, `plan/tests/scenarios.md` v1, `plan/assumptions.md` (PA-01 to PA-24), `plan/document-gaps.md` (PG-01 to PG-04), `plan/shared-updates.md`, `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json`, `plan/agent-run-log.md` |
| Checked against | Gated spec `../specify/spec.md` v10 and `../review/spec-gate-review-10.md` (`SPEC_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]`); story file RWB-TE-012 v1 in Epic 1 story files v7 (§13, §15, §16, §19); `RUN-BRIEF.md`; `AGENTS.md` §7 and §9; `aisdlc/.github/rules/planning-execution-gates.md`, `pdlc.md`, `implementation-execution-gates.md`, `traceability-standards.md`; `AI-SDLC-BUILD-LOG.md` D-RUN-06, -07, -08, -09, -17 and -21; RWB-TE-001 plan v7 relocation table; the baseline code the plan cites (`backend/build.gradle.kts:60`, `application.yaml:98-102`, `RecoveryDatabaseIT.java:61`, `.env.example:23-24`, `docker-compose.yml:135`, `README.md:25`, `scripts/dev.ps1`) |
| Reviewer | Compliance Reviewer agent, started by the orchestrator (Claude Code). Read only; this file is the only file written. No test, build, git or Azure command was run; this workspace is not a git repository. |
| Plan stage status | `SUCCESS` in `plan.md` front matter; the plan gate has not previously been run. |

## 1. Findings

| ID | Severity | Location | Evidence | Required fix |
|---|---|---|---|---|
| **PLAN-001** | **High** | `plan.md` lines 160-166 and 78; `tasks.md` TASK-08 (line 34), TASK-18 (line 44), TASK-19 (line 45); `shared-updates.md` §6 and §8 (lines 51-53 and 68) | The plan assigns the Implementation Builder direct edits of the shared Gradle, YAML and local-stack configuration: `backend/build.gradle.kts:60` (TASK-19), `application.yaml` and `application-local.yaml` (TASK-08), `.env.example`, `docker-compose.yml:135` and `scripts/dev.ps1` (TASK-18), plus `README.md` (TASK-19). This run reserves those shared files to the orchestrator (D-RUN-06: "the orchestrator alone writes shared files"; `RUN-BRIEF.md` rule 3; this gate's hard check). `shared-updates.md` carries no proposed row for any of the six configuration/local-stack files; §8 states "Shared files not edited", and the only Builder-edit row is README in §6, which still leaves the builder writing it. `plan.md:78` justifies the file set as files "the story itself names (`[S]` §13, §21)", but story file v7 has 19 sections and no §21, and §13 names none of these files; the sources are SPEC-021 (local stack), SPEC-016 (baseline evolution), SPEC-007/-008/-009 (YAML properties) and the baseline. | Add a `shared-updates.md` section with one exact proposed row per file: path, anchor or line, current value, proposed value, source and the task that consumes it. Recast TASK-08, TASK-18 and TASK-19 to verify the orchestrator-applied state (not to edit it), and add a TASK-00 or TASK-23 check that the builder diff contains none of these files. If the orchestrator intends the builder to edit any of them, record that explicit exception in the plan and the build log; absent that, the builder must not write them. Replace the `[S]` §21 justification with SPEC-021/016 and the baseline. |
| **PLAN-002** | **Medium** | `plan.md` line 230 (`BlobStorageAdapter` row), line 67 (S-11); `tasks.md` TASK-16 (line 42); `tests/scenarios.md` T-TE012-07 (line 29) and T-TE012-18 (line 40) | SPEC-015 says `open()` is "Not gated by readiness". The plan's adapter row says "enforces readiness" without excepting `open()`, and no planned case exercises `open()` while the hub is NOT_READY: T-TE012-07 covers flag-off NOT_READY and readiness unchanged, and T-TE012-18 starts from READY. A builder following the plan could gate `open()` on readiness, and the named tests would not catch it; this would make document reads fail during an outage and would contradict SPEC-015. | State in `plan.md`'s adapter row and S-11: "readiness is enforced on `store()` only; `open()` is not gated by readiness (SPEC-015)". Add a case to T-TE012-07 or T-TE012-18: flag on, probe result NOT_READY, `open()` of a standard or legal ref still downloads (or maps `BLOB_MISSING`), with zero probes, readiness, `checkedAt` and the root status unchanged. Update TASK-15/TASK-16 and `tests/scenarios.md`. |
| **PLAN-003** | **Low** | `plan.md:78`; `tasks.md` TASK-18 (line 44), TASK-03 (line 29), TASK-04 (line 30); `tests/scenarios.md` line 72 | Three traceability/evidence mismatches. (a) `[S]` §21 is cited at `plan.md:78` and `tasks.md:44`, but story file v7 has 19 sections; the local-stack file set is SPEC-021, not a story section. (b) TASK-18/TASK-03's verification lists four deterministic stage-1 runs (local file, placeholder, `-Mode Complete`, accept), while `tests/scenarios.md:72` says TASK-03 reproduces BE-09, -10, -11, -12 and -13; BE-09 (a valid environment paired with the wrong environment file) is not among the four and is only run externally in TASK-22. (c) TASK-04's verification says "the five headings", while the RUNBOOK sections listed in `plan.md:292` and TASK-04 are six (Apply, PROD lock, Extend, Later PROD applies, DEV spike, Report handling). | Correct the `[S]` citations to SPEC-021/016. Add the BE-09 run to TASK-03's evidence list or correct the `tests/scenarios.md` claim. Align TASK-04's heading count with the six sections (or state which five are headings and where the sixth is checked). No behaviour change. |

### 1.1 Finding notes

- **PLAN-001 is the blocking finding.** It is a run-control breach, not a code-design defect: the plan is otherwise specific and buildable, but it tells the builder to write files this run reserves to the orchestrator. The fix is confined to `shared-updates.md` and the three tasks; no requirement or spec change is needed.
- **PLAN-002 is a plan-precision defect.** The spec is correct and unambiguous; the plan's summary sentence and test list do not carry the `open()` exception. No spec change is needed.
- **PLAN-003 is editorial.** It does not change the build or the coverage result; it is raised because the plan gate checks traceability citations and the verification lists, and these three do not match the artifacts they cite.

## 2. Coverage table

| Check | Result | Evidence |
|---|---|---|
| Spec gate input | PASS, 0 Critical / 0 High / 0 Medium / 0 Low | `../review/spec-gate-review-10.md` final line; `plan.md` front matter |
| Spec status and requirement coverage | `SUCCESS`; 37 of 37 rows covered, 0 missing, 0 contradictions | `spec.md` "Status reporting"; `plan.md` `PLAN_REQUIREMENT_COVERAGE_RESULT` |
| `SPEC-001` to `SPEC-023` mapped to tasks | 23 of 23; no orphan SPEC | `plan.md` "SPEC to task map"; `tasks.md` |
| `AC1` to `AC12` mapped to a named test or labelled external/human evidence | 12 of 12 | `tests/scenarios.md` §7 |
| `BR1` to `BR7` mapped to a named test or labelled external/human evidence | 7 of 7 | `tests/scenarios.md` §7 |
| Every spec requirement-logic row mapped | 37 of 37 `COVERED`; 0 `BLOCKED` | `plan.md` "Requirement Logic To Task Coverage"; row-by-row comparison with `spec.md` |
| Scope bullets S-1 to S-14 mapped to tasks | 14 of 14 | `tasks.md` "Scope bullet to task map" |
| Every file named by exact repository path | Pass | `plan.md` "Files added or changed" (62 rows); `tasks.md` note N-1 |
| Backend unit tests and coverage | Required; LINE, INSTRUCTION, BRANCH, METHOD each ≥ 0.80 on the `recovery/**` bundle, per-class ≥ 0.80 under `recovery/dochub/**`, no drop against the TASK-00 snapshot, `test` data only, no exclusion | `plan.md` lines 119 and 331; `tasks.md` TASK-20; SPEC-023 |
| Frontend applicability and coverage | `NOT_APPLICABLE` with evidence, `N/A` counts, no invented zeros | `contracts/frontend-integrations.json`; `plan.md` "Frontend Plan"; `tasks.md` "Frontend Plan"; DGAP-20 |
| External and human-verification items | Labelled as external/human and not executed here: BE-01 to BE-13, DEV/SIT applies, DGAP-03 spike, SIT TCs 01-12, RW-SECADM listing | `plan.md` FTS-03 and HV-01 to HV-03; `tasks.md` TASK-22 and TASK-24; `tests/scenarios.md` §4 to §6 |
| Migration (D-RUN-07) | None; no fixed number and no `V<seq>` file in any plan artifact | `data-model.md` §0; `plan.md` "Upstream readiness"; search of `plan/` |
| New dependency | None; no build dependency or new library | `plan.md` "Work type split" and "One-module check"; TASK-00 and TASK-23 |
| One module (AGENTS.md §7/§9) | Pass under D-RUN-21: P5 `dochub` only, plus repository-level files | `plan.md` "One-module check"; `assumptions.md` PA-20; `document-gaps.md` PG-03 |
| Precondition RWB-TE-001 v7 | Pass: `dochub.api` / `dochub.storage` layout, `recoveryCoverageVerification`, `RecoveryBoundaryTest`, TASK-00 stop rule | RWB-TE-001 plan v7 relocation table; `plan.md` "Upstream readiness"; `tasks.md` TASK-00 |
| Shared Gradle, YAML and local-stack files | **FAIL** — six builder-edited files with no proposed `shared-updates.md` rows | PLAN-001 |
| Test-first execution | Pass: every code task has a red test task immediately before it; no implementation task writes a test after the code | `tasks.md` "Compile-red tasks"; `plan.md` "Execution order" |
| No skipped or weakened test | Pass: no `@Disabled`, `@Ignore`, skip or assumption; deleted baseline test has named successors | `plan.md` "Baseline evolution"; `tests/scenarios.md` T-TE012-14 |
| Security, privacy and audit | Pass on the plan: managed identity only, no key/SAS outside emulator, no personal data, `DOCUMENT_CHANGE_REFUSED` audit, flag-off previous path | `plan.md` "Security, privacy and compliance"; SPEC-014 and SPEC-017 |
| API impact | Pass: `NO_API_CHANGE`; no endpoint added or changed; published Java surface recorded | `contracts/backend-apis.json`; `plan.md` "API change assessment" |
| AGENTS.md §7 and §9 | Named files, tests and migration pass; one-module check passes; the shared-file rule fails as PLAN-001 | `plan.md` "One-module check"; PLAN-001 |
| Document gaps | 23 active spec gaps, DGAP-18 withdrawn; PG-01 to PG-04, all Blocker = No; no new blocker | `plan/document-gaps.md`; `../specify/document-gaps.md` v10 |

## 3. D-RUN checks

| Decision | Result | Evidence |
|---|---|---|
| D-RUN-17: TE-001 merges first; the plan uses the TE-001 v7 `dochub.api` / `dochub.storage` layout | Confirmed. TASK-00 verifies `dochub/api/DocumentStore.java`, `dochub/storage/BlobDocumentStore.java`, `BlobDocumentStoreTest.java`, the module map, `RecoveryBoundaryTest`, the four-counter `recoveryCoverageVerification`, and stops if the merged layout differs. | `plan.md` "Upstream readiness" and "Plan-time verification"; RWB-TE-001 plan v7 relocation table; `tasks.md` TASK-00 |
| D-RUN-21: "one module" means the ACE recovery module | Confirmed. The plan changes P5 `dochub` only; `infra/azure/document-storage/`, `scripts/dev.ps1`, `.env.example`, `docker-compose.yml`, `README.md`, `backend/build.gradle.kts` and `application*.yaml` are repository-level files, not another ACE module. PG-03 records the definition gap; ratification is OPEN-050. No human approval is claimed. | `plan.md` "One-module check"; `assumptions.md` PA-20; `document-gaps.md` PG-03 |
| D-RUN-09: Critical/High/Medium block; a Low-only FAIL is remediated, not accepted | Applied. PLAN-001 is High and PLAN-002 is Medium, so the gate is `FAIL`; PLAN-003 is Low and remains visible for the same remediation round. The orchestrator must re-run the plan stage and this gate. | This review |
| D-RUN-06: the orchestrator alone writes shared files | **Not met by the plan.** PLAN-001. | `plan.md` lines 160-166; `tasks.md` TASK-08, TASK-18, TASK-19; `shared-updates.md` §8 |
| D-RUN-07: no fixed migration number | Confirmed. No migration; no `V<seq>` or four-digit number in the plan artifacts. | `data-model.md` §0; search of `plan/` |
| D-RUN-08: later-story work only as seams | Confirmed. The E1-017 archive container, E1-024 `DocumentStore`/`StoreRequest`/`StoredDocument`, E1-026 endpoint, E1-041 quarantine mover, E1-049 OCR read, E1-032/-054 re-store caller and SCR-44 are seams or out of scope. | `plan.md` "Out of scope and seams"; `tasks.md` TASK-23; `shared-updates.md` §7 |
| D-RUN-19: no parameter-catalog read | Confirmed. TE-012 reads no parameter row; its values are `rwb.dochub.*` configuration, the flag and template parameters. | `plan.md` "Carried plan inputs" and "Configuration properties" |

## 4. Observations (not findings)

- **O-1 `DocumentStorageProperties` n/a rule.** `assumptions.md` PA-21 applies D-RCV-43 (3) ("a coverage report with 0 measurable statements is a PASS with the totals recorded") per class for interfaces and constructor-only classes. The principle is sound; D-RCV-43 (3) is written for the frontend placeholder. The per-class report can state the rationale without a new decision.
- **O-2 T-TE012-09 runner.** The spec names `ApplicationContextRunner` with `ConfigDataApplicationContextInitializer`; the plan's scenario says "with the default status aggregator and HTTP mapper" and does not repeat the runner. The class name and the "no Blob client" clause make the intent clear; the Builder should follow the spec's runner.
- **O-3 `StorageUnavailableException` field.** The plan's published-surface sketch shows the `Reason` enum but not the `String container` field; `data-model.md` §4 carries it. The contract and the data model agree; no change needed.
- **O-4 Template test read path.** `StorageTemplateConformanceTest` reads `../infra/azure/document-storage` from `backend/` with `Path.of`, matching `RecoveryDatabaseIT`'s `../infra/postgres` convention. The folder does not exist yet, so TASK-01 is a runtime red, not a compile red; the plan states this.

## 5. Document gaps

No new document-set gap is raised by this review. The plan carries 23 active spec gaps (DGAP-01 to DGAP-17, DGAP-19 to DGAP-24; DGAP-18 withdrawn) and records PG-01 to PG-04, all Blocker = No. PG-03 (the undefined "module" in AGENTS.md §7/§9) is settled for this build by D-RUN-21; the definition gap remains for the document owners under OPEN-050. No document-set file was edited by this stage.

## 6. Result

```text
PLAN_GATE_FINDINGS: PLAN-001 High (open), PLAN-002 Medium (open), PLAN-003 Low (open)
PLAN_REQUIREMENT_COVERAGE_RESULT (reviewer check): CONFIRMED [TOTAL_RULES: 37] [TASK_COVERED_RULES: 37] [MISSING_TASK_RULES: 0] [CONTRADICTIONS: 0]
SPEC_TO_TASK: 23 of 23 (SPEC-001 to SPEC-023); AC 12 of 12; BR 7 of 7
SCOPE_TO_TASK: 14 of 14 (S-1 to S-14)
BACKEND_COVERAGE_GATE: 80% x4 planned (LINE, INSTRUCTION, BRANCH, METHOD), per-class 80% under recovery/dochub/**, no-drop baseline
FRONTEND_APPLICABILITY: NOT_APPLICABLE with evidence (UI In Scope NO; DGAP-20)
EXTERNAL_AND_HV: labelled, not executed here (BE-01 to BE-13, DEV/SIT applies, SIT TCs, RW-SECADM listing)
MIGRATION_CHECK: PASS (none; no fixed number)
DEPENDENCY_CHECK: PASS (none)
ONE_MODULE_CHECK: PASS under D-RUN-21 (P5 dochub plus repository-level files)
SHARED_FILE_CHECK: FAIL (PLAN-001: six builder-edited shared files, no proposed rows)
D_RUN_17: CONFIRMED (TE-001 v7 layout; TASK-00 stop rule)
D_RUN_21: CONFIRMED (ACE recovery module; PG-03; OPEN-050 ratification pending)
COUNTS: Critical 0, High 1, Medium 1, Low 1
```

Overall status: **FAIL**. Critical 0, High 1, Medium 1, Low 1. The High and Medium findings block the handoff; the Low finding is remediated in the same round (D-RUN-09). This is the automated plan gate result only; it is not the AGENTS.md §9 "Plan approved" sign-off, which stays with the tech lead.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 1] [MEDIUM: 1] [LOW: 1]
