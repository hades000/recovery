# TASK-00 pre-flight: RWB-TE-002 (read only)

Worktree `rwb-wt/RWB-TE-002`, branch `feature/RWB-TE-002-code-owners`. Start: `f36991a`; `git merge --ff-only develop-recovery` moved it to `7bee04d` (RWB-E1-044 merge recorded). 18 Nov 2026.

| # | Check | Command / method | Result |
|---|---|---|---|
| 1 | Spec status | `specify/spec.md` line 13 | `Status` = `SUCCESS` (SU-P01 already applied). PASS |
| 2 | RWB-TE-001 outputs on the branch | directory listing | `backend/src/test/resources/architecture/recovery-modules.yaml` present; `architecture/fixtures/` holds 9 files (`bnd1.yaml` .. `vendorx.yaml`); `backend/src/test/java/th/co/scb/ace/boundaryfixture/` holds 92 files; `â€¦/recovery/architecture/boundary/` holds `BoundaryRules`, `ModuleMap`, `ModuleMapLoader` and tests; 19 module packages under `â€¦/demo/recovery/` (access, agent, asset, casewf, comms, dataengine, debtsale, decision, deviation, dochub, guarantee, integration, litigation, partner, payments, reporting, treatment, valuation, writeoff). PASS. `{te001FixtureRoot}` = `th/co/scb/ace/boundaryfixture` (merged path equals PA-01). Codeowners package name differs from `â€¦architecture.boundary`: no conflict. |
| 3 | SnakeYAML on test classpaths | `gradlew --offline -q dependencies --configuration testCompileClasspath` / `testRuntimeClasspath` | both exit 0; `org.yaml:snakeyaml:2.6` in both. PASS |
| 4 | Files under the UT-26 (B) scope | listing | `architecture/`: `recovery-modules.yaml` + `fixtures/*` only: all owned by the spec block. `backend/src/test/java/`: only `th/co/scb/ace/boundaryfixture/` and `th/co/scb/ace/demo/{recovery,e2e}/` plus `ModulithTest.java`: all owned. Top-level `backend/src/test/resources/` folders: `architecture`, `flyway-fixtures`, `migration-lint`. R-3 recorded: `flyway-fixtures/` and `migration-lint/` (RWB-E1-044) are not owned by the block and are outside UT-26 scope (PROP-OI-4). No stop on the current base. R-2 (RWB-E1-042) analysed below. |
| 5 | `recoveryCoverage*` class include | `backend/build.gradle.kts` lines 130-178 | main `recovery/**` + test `architecture/boundary/**` + test `architecture/migration/**` (E1-044). Codeowners classes are **separate**: measured only by `codeOwnersCoverage*`. Not edited. |
| 6 | Baseline | `.gitlab/` | absent (`Test-Path .gitlab` = False). Baseline full `gradlew test` not re-run: the orchestrator's time box allows one full run at the final tip (TASK-10); `develop-recovery` 7bee04d is the post-merge tip of RWB-E1-044 whose merge evidence is in `INC-001-epic-1-RWB-E1-044/`. Recorded as deviation DEV-02. |

## Untracked folder from the earlier opencode run

`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners/` held the four TASK-01 stubs (every method throws `UnsupportedOperationException("TASK-04")`, signatures as `data-model.md` Â§1.1) and `CodeOwnersValidationTest` (UT-01..UT-11, UT-23 plus `registerProblemsFailClosed` for the X8 texts) and `OwnershipResolverTest` (UT-19). Each assertion was checked against `data-model.md` Â§1.3/Â§1.4 and `tests/scenarios.md`; they are kept and are re-run red by this Builder before any logic (red log `backend/red-task01-03.txt`). The earlier run's logs were moved to `implement/_superseded-opencode/` and are not evidence.

## RWB-E1-042 paths (merged into `develop-recovery` before this story, SU-P04)

`git diff --name-only develop-recovery...feature/RWB-E1-042-parameter-catalog`, non-`aisdlc/` paths, grouped; "Pattern" is the spec-block line that owns them.

| Path (group) | Owned? | Pattern | In UT-26 scope? |
|---|---|---|---|
| `backend/src/main/java/th/co/scb/ace/demo/recovery/**` (41 files: `access/â€¦`, `casewf/config/â€¦`) | Yes | `/backend/src/main/java/th/co/scb/ace/demo/recovery/` | No |
| `backend/src/test/java/th/co/scb/ace/demo/recovery/**` (30 files incl. `architecture/parameters/â€¦`, `casewf/config/â€¦`) | Yes | `/backend/src/test/java/th/co/scb/ace/demo/recovery/` | Yes (B) |
| `backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_042_parameter_catalog_and_seed.sql` | Yes | `/backend/src/main/resources/db/modulemigration/recovery/` | No |
| `backend/src/test/resources/architecture/fixtures/parameter-checks/**` | Yes | `/backend/src/test/resources/architecture/fixtures/` | Yes (B) |
| `backend/src/test/resources/architecture/recovery-modules.yaml` (edited) | Yes | file pattern | Yes (A, B) |
| `backend/src/test/resources/architecture/magic-number-baseline.csv` | **No** | none: the block owns only `architecture/recovery-modules.yaml` and `architecture/fixtures/` | **Yes (B): UT-26 will fail after E1-042 merges** |
| `backend/src/main/resources/config/parameter-catalog.csv` | No | none | No (main resources; not tested) |
| `backend/src/main/resources/access/interim-capability-grants.csv` | No | none | No |
| `backend/src/main/resources/application.yaml`, `application-local.yaml` | No | none (PA-06, deliberately unowned) | No |
| `backend/build.gradle.kts` (edited) | Yes | `[Pipeline gates]` `/backend/build.gradle.kts` | No |

See `deviations.md` DEV-01 and `document-gaps.md` IM-DG-01: no line was added to the exact spec block; UT-26 is not weakened, so it names `magic-number-baseline.csv` as unowned once E1-042 is merged.
