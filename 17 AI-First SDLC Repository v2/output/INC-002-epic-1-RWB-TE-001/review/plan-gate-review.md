# Plan gate review (gate 1): RWB-TE-001 (INC-002-epic-1-RWB-TE-001)

| Field | Value |
|---|---|
| Review type | PLAN GATE REVIEW (planning stage), first run |
| Story | RWB-TE-001 (Jira `TB0001-1235`) |
| Reviewer | Compliance Reviewer (agent run), 2026-11-09 |
| Artifacts reviewed | `plan/plan.md`, `plan/tasks.md`, `plan/data-model.md`, `plan/tests/scenarios.md`, `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json` (both valid JSON); against `specify/spec.md`, `specify/contracts/*.json`, `review/spec-gate-review*.md`; `docs/increments/INC-002-epic-1-RWB-TE-001.md`; `requirement/Traceability_Matrix.md` (rows 111, 122, 125, 141); `docs/decisions/INC-001-decisions.md` (D-RCV-36..43); `docs/open-items.md` (OPEN-021..024) |
| ACE evidence (read-only) | `ace-monorepo` `develop` 96b0d1c6: `frontend/eslint.config.js`, `frontend/package.json`, `frontend/tsconfig*.json`, `frontend/vite.config.ts`, `frontend/.prettierignore`, `.gitignore`, `nx.json`, root `package.json` (workspaces `frontend`, `backend`, `packages/*`; eslint 9.39.5 in lockfile), `.gitlab-ci.yml`, `Dockerfile`, `backend/build.gradle.kts` (plugins incl. `checkstyle`; `azure-storage-blob` on main), `backend/config/checkstyle/checkstyle.xml` (severity `error`), `AppConfig.java` (`@EnableJpaRepositories(basePackages = "th.co.scb.ace.demo")`), `ModulithTest.java`; Gradle cache `org.jacoco.agent` 0.8.14 |
| Overall status | **FAIL** |
| Blocking | **YES**: two Medium findings (REVIEW-RWB-TE-001-021, -022) |

## Human dispositions recorded (not re-litigated)

| Item | Disposition | Check result |
|---|---|---|
| Spec gate 3 Low findings REVIEW-RWB-TE-001-001, -003, -019 | Accepted by the human starting the planner, 2026-11-09 (stale text, no scope change) | Recorded in `plan.md:37-47` with `FAIL` kept visible. Consistent. |
| PRE-1 Product Owner spec approval | PENDING | `plan.md:30`, `tasks.md:14`, `:132`; card line 152 "Not approved". Not treated as approved. |
| PRE-2 OPEN-023 (ACE tech lead: vitest, @vitest/coverage-v8, JaCoCo, shared files) | PENDING | `plan.md:31`; OPEN-023 still open in `docs/open-items.md:24`. TASK-00 (`tasks.md:29`) stops with `BLOCKED` if any of PRE-1..4 lacks decision and date; every build task depends on it via TASK-01. Not treated as approved. |

## Findings

| ID | Severity | Location | Maps to | Issue | Required fix |
|---|---|---|---|---|---|
| REVIEW-RWB-TE-001-021 | Medium | `plan.md:151`; `tasks.md:54`, `:56`; `plan/contracts/frontend-integrations.json:75`; ACE `frontend/eslint.config.js:13-15`, `.gitignore` | TASK-14, -15, -17; SPEC-015, -018, -020; T-TE001-08 | The Vitest `lcov` reporter writes `frontend/coverage/recovery/lcov-report/` with JavaScript files (`prettify.js`, `sorter.js`, `block-navigation.js`). ESLint's global ignores are only `dist/**`, `build/**`, `node_modules/**`, and `js.configs.recommended` applies to every `.js` file with no browser globals for `.js`, so `eslint:lint` (`eslint .`, inferred by `@nx/eslint/plugin`) will report `no-undef` and other errors on them. `test` and `eslint:lint` are siblings in `check.dependsOn`, so the failure appears on any second local run and can race in CI. `.prettierignore` covers `coverage`; ESLint and `.gitignore` do not, so every developer also gets an untracked `frontend/coverage/`. The plan only handles this for the Builder ("copy, then delete the folder"), which does not protect CI or the ACE team. | Choose one and state it in TASK-14/-15 and the frontend contract: (a) use reporters `text`, `json-summary`, `lcovonly` (no HTML/JS output); or (b) add `"coverage/**"` to the first ESLint `ignores` entry (the same line TASK-14 already edits) and list it in PRE-2. Add to TASK-17 verification: run `npx nx run frontend:check` twice in a row with the coverage folder present; both green. |
| REVIEW-RWB-TE-001-022 | Medium | `tasks.md:36`, `:46`; `plan.md:212`; ACE `backend/build.gradle.kts:10` (`checkstyle`), `backend/config/checkstyle/checkstyle.xml:25`, `:62-66`, `:333-358`; `.gitlab-ci.yml` (`nx affected -t check`) | TASK-02, -04, -06, -07, -12; SPEC-012, -018; HV-1 | ACE applies the Gradle `checkstyle` plugin with severity `error` (LineLength 100, Indentation 4, CustomImportOrder, PackageName, AbbreviationAsWordInName). `checkstyleMain`/`checkstyleTest` run under Gradle `check`, which is what the CI `test` job runs through Nx (`backend:check`). The plan verifies only `./gradlew test`, `compileJava`, `compileTestJava`; no task runs checkstyle. The 58 `package-info.java`, the loader, the rule factory (long SPEC-004/-010 failure strings), and the fixtures can pass every planned check and still fail the MR pipeline. The plan would then report T-TE001-06 green while CI is red. | Add `./gradlew checkstyleMain checkstyleTest` (or `npx nx run backend:check`) to TASK-02 and TASK-12 verification, saving the output to `implement/backend/`; record pre-existing ACE checkstyle failures as blockers per the implementation gate rule (do not fix them silently). In TASK-04/-06 note that failure-text literals must respect LineLength 100 (split with string concatenation or a text block), and that `checkstyle` suppressions are not an option. No checkstyle config change. |
| REVIEW-RWB-TE-001-023 | Low | `plan.md:165`, `:168`; `plan/contracts/frontend-integrations.json:54-55`; `tasks.md:55` | TASK-14, -16; SPEC-014 (i), (ii); T-TE001-07 | The planned regex forbids only imports that *start with* `../`. `./../hooks/cfsc/x`, `./sub/../../pages/x` and a bare `..` are not matched, so a recovery file can leave the folder through a relative path that starts with `./`. SPEC-014 (i) allows `./...` only for "same folder or below", which these are not. | Forbid any `..` path segment: for example prefix the regex with `(?:^|/)\.\.(?:/|$)|` alongside the existing `@/` branch. Add `./../x` and `..` to `forbidden.ts` in TASK-16 and to `regexCheckedAgainst` in the contract. |
| REVIEW-RWB-TE-001-024 | Low | `tasks.md:38` | TASK-04; SPEC-003, -017 | TASK-04 says "SnakeYAML `SafeConstructor`/`LoadSettings`". `LoadSettings` is in snakeyaml-engine (`org.snakeyaml.engine`), which the plan-time classpath check did not find. Only `org.yaml:snakeyaml` 2.7 is present (`plan.md:66`). A Builder that follows the text could add a dependency outside the approved footprint (SPEC-017: no new backend library). | Change the wording to SnakeYAML 2.x: `new Yaml(new SafeConstructor(loaderOptions))` with `LoaderOptions.setAllowDuplicateKeys(false)`, so duplicate YAML keys are also rejected. State that no snakeyaml-engine dependency is added. |
| REVIEW-RWB-TE-001-025 | Low | `tasks.md:41`, `:43`; `plan.md:133`; `tests/scenarios.md:9` | TASK-07, -09; SPEC-007, -011; TC-TE-001-03 | (1) TASK-09 asserts that "a dependency cycle between two fixture modules through published packages fails", but TASK-07 creates only `bnd3.broken` and `bnd3.fixed`, so the cycle fixture is not planned. (2) `ApplicationModules.of("…recoveryfixture.bnd3.<case>", …)` makes the direct sub-packages *top-level* modules. Neither task says the fixture copies the real layout: a closed root `@ApplicationModule`, nested `@ApplicationModule` modules, and `api` packages with `@NamedInterface`. Real main code has no classes, so `ModulithTest` cannot show that nested-module enforcement works. TC-TE-001-03 is the only proof, and a flat fixture would not prove the configuration SPEC-001 ships. | In TASK-07 add `recoveryfixture.bnd3.cycle` and state that each BND-3 fixture set has the SPEC-001 shape (closed root package-info, nested `@ApplicationModule` package-infos, `api` `@NamedInterface`, `internal` plain), with one class per module. In TASK-09, assert that Modulith detects the nested modules (for example by module count or name) before calling `verify()`. If it does not, stop per SPEC-007. |
| REVIEW-RWB-TE-001-026 | Low | `plan.md:31`, `:68`, `:117`; `tasks.md:29`, `:41`, `:64`; `CLAUDE.md` "Two repositories, one story" | TASK-00, -07, -20; SPEC-011; PRE-2 / OPEN-023 | The fixture root `th.co.scb.ace.recoveryfixture` is outside both `th.co.scb.ace.demo` and the module's namespace. CLAUDE.md limits Builder edits to "the module's paths, plus shared files that the approved plan names explicitly". The plan's reason is sound and verified: `AppConfig` `@EnableJpaRepositories(basePackages = "th.co.scb.ace.demo")` would scan fixture repositories. But the new top-level package is in the ACE team's namespace and is not in the PRE-2 list that the ACE tech lead approves, nor in the TASK-20 notice. | Add `backend/src/test/java/th/co/scb/ace/recoveryfixture/**` (test scope only, with the reason) to PRE-2, the TASK-00 file list and OPEN-023, and to the TASK-20 ACE-team announcement. No design change. |
| REVIEW-RWB-TE-001-027 | Low | `tasks.md:54` (TASK-15 command and verification) | TASK-15; SPEC-017 | `frontend` is an npm workspace of the root `package.json`. npm 7+ detects the workspace root when it runs inside a workspace folder, so `npm install --package-lock-only` and `npm ci` run in `frontend/` may act on the root lockfile and leave `frontend/package-lock.json` unchanged. The verification "`npm ci` succeeds … in `frontend/`" would then pass without proving anything. ACE does keep that file up to date (last changed 2026-11-03 with the root lockfile), so SPEC-017 wants it updated. | Name a command that is checked to update `frontend/package-lock.json` (for example run with workspace-root detection disabled, `--workspaces=false`, from `frontend/`). Change the verification to: `git diff --stat frontend/package-lock.json` shows `vitest`/`@vitest/coverage-v8` entries, and no other top-level dependency changes in either lockfile. |
| REVIEW-RWB-TE-001-028 | Low | `docs/increments/INC-002-epic-1-RWB-TE-001.md` (whole file), `requirement/Traceability_Matrix.md` (whole file) | Traceability; TASK-20 | The planner's edits turned both files from CRLF to LF line endings. `git diff --stat` shows 313 and 852 changed lines where the real change is 5 and 8 lines (`git diff --ignore-cr-at-eol`). This hides the trace change from reviewers and will conflict with other branches. The content itself is correct: TASK-00..20 are in rows 111, 122, 125 and 141, and "Plan … Not approved" is on card line 152. | Restore CRLF line endings in both files, keeping the content edits, before commit. |

## Checks with no finding

| Check | Result |
|---|---|
| Upstream readiness | Spec `status: SUCCESS`, `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`, `REQUIREMENT_COVERAGE_RESULT … MISSING_RULES: 0 … CONTRADICTIONS: 0`. CLAR-001..012 are all RESOLVED and each has a resulting SPEC. |
| SPEC-RWB-TE-001-001..020 → TASK | 20/20 mapped (`tasks.md:84-105`); each mapped task has a verification. |
| Spec Requirement-to-SPEC coverage rows | 17/17 in `plan.md:196-214`, with correct `Coverage Type` values; none `BLOCKED`. Exception rows X-B1..X-B7, X-F1, X7 and CLAR carry-forward are mapped (`plan.md:216-218`). No rule weakened: BND-4 includes ACE `model`/`repository` (CLAR-001 A), the BND-5 name-boundary rule and its 16 libraries match D-RCV-41, the allow-list matches D-RCV-39, and BND-3 is Modulith-only (D-RCV-42). |
| Scope bullets → tasks | S1–S19 each map to tasks (`plan.md:81-101`). |
| `BLOCKED_BY` DAG | Every task has `BLOCKED_BY` (`NONE` only for TASK-00). Checked by hand: 00→01→{02,03,11,13}; 03→04→{05,06}; {03,04}→07; {06,07}→08; 07→09; {02,06}→10; {05,08,09,10,11}→12; 13→{14,15}→16→17; {12,17}→{18,19}→20. No cycle; the diagram matches the table. |
| Unit-test gates per surface | Backend REQUIRED: JaCoCo `recoveryCoverageVerification`, 80% LINE/INSTRUCTION/BRANCH/METHOD, native XML/HTML (TASK-11, -12). Frontend REQUIRED: `@vitest/coverage-v8`, 80% on all four metrics, `json-summary` and `lcov` (TASK-15, -17), expected 0/0 `PASS` as printed (D-RCV-43 (3)). Separate rows, no combined average (TASK-19). Unit-test tasks are `BLOCKED_BY` their implementation tasks. |
| D-RCV-36 exclusions | No `RecoveryAccessGuard`, endpoint, TC-TE-001-08 or MSG-P4-002 task; TASK-18 greps the diff. API Tester and FAT are `NOT_APPLICABLE`, with human-verification gaps HV-1 and HV-2 visible. |
| Shared-file list vs SPEC-017 | Plan (`plan.md:119`, `:147-158`), PRE-2, TASK-00 and both contracts list the same files: `backend/build.gradle.kts`, `frontend/package.json`, `frontend/eslint.config.js`, `frontend/tsconfig.app.json`, new `frontend/vitest.config.ts`, `package-lock.json`, `frontend/package-lock.json`. No `testImplementation` line (classpath check run). `nx.json`, root `package.json`, `.gitlab-ci.yml` and `ModulithTest.java` are unchanged. See -021 (possible ESLint ignore line) and -026 (fixture root) for additions. |
| Fixture root `th.co.scb.ace.recoveryfixture` | Technically sound. It is outside `th.co.scb.ace.demo` (JPA repository scan base in `AppConfig`) and outside `th.co.scb.ace.demo.recovery` (SPEC-011). `ModulithTest` excludes test classes. Process point only: see -026. |
| Tooling package `th.co.scb.ace.demo.recovery.architecture` | Matches spec (test classes under the recovery package in `src/test`). Main-class import uses `DoNotIncludeTests`, so module-map rule (a) never sees it. JaCoCo includes it and excludes `*Test`/`*Test$*`, so fixtures fall outside both filters. Consistent with SPEC-020. |
| ESLint `regex` form | ESLint 9.39.5 (root lockfile) supports `patterns[].regex`. Text-based matching agrees with SPEC-014 and D-RCV-39. ACE config has no type-aware parser options, so linting excluded fixtures through the Node API does not hit parse errors. Bypass gap: see -023. |
| vitest 4.1.12 pin | Peer `vite ^6‖^7‖^8` fits ACE `vite ^8.0.4`. `@vitest/coverage-v8` is pinned to the same version, with `--save-exact`. Subject to PRE-2. |
| JaCoCo 0.8.14 | Present in the Gradle cache; supports the Java 21 toolchain. Tasks stay outside `check` (D-RCV-28 (3)). The agent side effect on `testE2E` is disclosed and the durations are recorded. |
| BND-5 fixture library | `com.azure:azure-storage-blob` is a main `implementation` dependency, so a real `com.azure.storage` type is on the test classpath. No new dependency. |
| PII, secrets, production data | None in plan outputs; fixtures hold class and package names only. TASK-18 scans the diff. |
| Authorization, audit, KYC/AML, consent | N/A (no runtime path, D-RCV-36). |
| Design evidence | `NOT_REQUIRED` (UI NO); `components.md` correctly omitted. |

## Required checks summary

| Check | Result |
|---|---|
| Authentication / authorization | N/A (D-RCV-36) |
| Customer / account data protection | PASS |
| Audit logging | N/A |
| KYC/AML/suitability/consent/approval | N/A |
| Frontend integration versioning / error contract | N/A for API; lint contract consistent except -023 |
| Secrets and environment configuration | PASS |
| Plan requirement coverage | 17/17 rows, 20/20 SPEC |
| Unit-test gates planned | PASS (both surfaces, 80%, native reports); CI-parity gaps -021, -022 |
| Traceability | PASS on content; -028 formatting |
| Approval preconditions | PASS: PRE-1..PRE-4 pending and enforced by TASK-00 |

## Status lines

```text
REVIEW_STATUS: FAIL
REVIEW_TYPE: PLAN_GATE_REVIEW
RUN_ID: INC-002-epic-1-RWB-TE-001
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 2] [LOW: 6]
REVIEW_BLOCKING: YES [REASON: Medium findings REVIEW-RWB-TE-001-021 (coverage HTML JS linted by eslint:lint) and -022 (checkstyle under backend check not verified)]
NEXT_STEP: Human records remediation or explicit acceptance of REVIEW-RWB-TE-001-021 and -022 (and disposition of Low -023..-028); after remediation, re-run Implementation Planner and the plan gate review. PRE-1 (Product Owner spec approval) and PRE-2 (OPEN-023) remain pending before FDA plan approval. This review does not start Implementation Builder.
```
