# Plan gate review (gate 2): RWB-TE-001 (INC-002-epic-1-RWB-TE-001)

| Field | Value |
|---|---|
| Review type | PLAN GATE RE-REVIEW (planning stage), gate 2 |
| Story | RWB-TE-001 (Jira `TB0001-1235`) |
| Reviewer | Compliance Reviewer (agent run), 2026-11-09 |
| Prior report | `review/plan-gate-review.md` (gate 1: FAIL, Medium -021, -022; Low -023..-028) |
| Human instruction | 2026-11-09: fix -021..-027 as proposed (021 `lcovonly`; 022 checkstyle in TASK-02/-12; 023 forbid `..`, "normalise the path before the regex"; 024 `LoaderOptions` + `SafeConstructor`; 025 `bnd3.cycle` + nested layout + module-detection assertion; 026 fixture root in OPEN-023 / PRE-2, TASK-00, TASK-20; 027 `npm install -D --save-exact ... -w frontend` and check both lockfiles). -028 fixed by the planner. |
| Artifacts reviewed | Working-tree diff (`git diff --ignore-cr-at-eol`) of `plan/plan.md`, `plan/tasks.md`, `plan/tests/scenarios.md`, `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json` (both valid JSON), `docs/open-items.md`; full `tasks.md` TASK-07, -09, -12, -15, -16, -17; `plan.md` §coverage; `specify/spec.md` SPEC-014, -015; HEAD commit 8de8f95 for the card and matrix |
| ACE evidence (read-only) | `ace-monorepo` `develop` 96b0d1c6: `backend/build.gradle.kts:10`, `:39-40` (checkstyle 13.5.0), `backend/config/checkstyle/checkstyle.xml` (LineLength 100, PackageName `^[a-z]+(\.[a-z][a-z0-9]*)*$`, AbbreviationAsWordInName length 0, MissingJavadocType), root `package.json:26-30` (workspaces), `frontend/package-lock.json` (standalone lockfile, `name: frontend`), `.gitlab-ci.yml:38-63` (`npm ci` at root) |
| Overall status | **FAIL** |
| Blocking | **YES**: one Medium finding (REVIEW-RWB-TE-001-029) |

## Human dispositions recorded (not re-litigated)

| Item | Disposition | Check result |
|---|---|---|
| Spec gate 3 Low -001, -003, -019 | Accepted 2026-11-09 | Still recorded in `plan.md` with `FAIL` visible. |
| PRE-1 Product Owner spec approval | PENDING | Unchanged; enforced by TASK-00. |
| PRE-2 OPEN-023 | PENDING | Still open in `docs/open-items.md:24`, now also lists `frontend/vitest.config.ts` and the fixture root. TASK-00 stops with `BLOCKED` while it lacks a decision and date. Not treated as approved. |
| Plan gate 1 record | — | `plan.md:49-62` records gate 1 `FAIL`, the instruction, and the fix per finding. Consistent. |

## Gate 1 finding disposition

| ID | Sev. | Disposition | Evidence |
|---|---|---|---|
| REVIEW-RWB-TE-001-021 | Medium | **RESOLVED** | Reporters `text`, `json-summary`, `lcovonly` in `plan.md:167`, `tasks.md:54`, `contracts/frontend-integrations.json:75`, `:88-92`. No `lcov` (HTML) reporter left anywhere in plan/tasks/scenarios/contracts. TASK-17 (`tasks.md:56`) runs `frontend:check` twice with `--skip-nx-cache` and checks the coverage folder has no `.js`/`.html`; evidence path corrected to `coverage/recovery/lcov.info` (written by `lcovonly`). T-TE001-08 updated (`scenarios.md:20`). |
| REVIEW-RWB-TE-001-022 | Medium | **RESOLVED** | `checkstyleMain` in TASK-02 (`tasks.md:36`), `checkstyleTest` in TASK-07 (`:41`), both (or `nx run backend:check`) in TASK-12 (`:46`) with output saved and pre-existing failures reported, not fixed. LineLength note in TASK-04/-06; `plan.md:149` and risk row `:264`; T-TE001-06 (`scenarios.md:18`); backend contract `checkstyle`. Version 13.5.0 matches ACE `build.gradle.kts:40`. Fixture package names (`recoveryfixture`, `bnd3`) pass ACE `PackageName`. |
| REVIEW-RWB-TE-001-023 | Low | **RESOLVED** (one gap, see -030) | Regex `(?:^|/)\.\.(?:/|$)|^@/(?!…)` in `plan.md:181` and contract `:54`. Re-checked with node using ESLint's flags (`iu`): all 14 forbidden cases (incl. `./../x`, `./sub/../../x`, `@/modules/recovery/../cfsc/x`, `..`) match; all allowed cases (incl. `./sibling`, `./sub/x`, `./a..b`, `react`, `@scope/pkg`) do not. **On the "normalise" intent**: `no-restricted-imports` matches import text only and has no normalisation hook; normalising would need a custom rule or a resolver plugin (a new dependency, outside SPEC-017). Rejecting every `..` segment closes every climb-out path, which is what normalising was meant to achieve. It is stricter than a normalised check only for in-folder forms such as `./sub/../x`, which T-TE001-07 does not list as allowed and which SPEC-014 leaves to the plan ("patterns are a plan detail; the T-TE001-07 cases are the acceptance"). It does not weaken SPEC-014. The deviation from the literal wording is stated openly in `plan.md:184`. Meets the intent; FDA should note it when approving the plan. |
| REVIEW-RWB-TE-001-024 | Low | **RESOLVED** | `tasks.md:38`, `plan.md:148`, backend contract `yamlParsing`: `new Yaml(new SafeConstructor(options))` with `LoaderOptions.setAllowDuplicateKeys(false)`; `LoadSettings` explicitly excluded. In SnakeYAML 2.x `Yaml(BaseConstructor)` takes its loading config from the constructor, so the duplicate-key setting applies. No new dependency. |
| REVIEW-RWB-TE-001-025 | Low | **RESOLVED** | TASK-07 (`tasks.md:41`) adds `bnd3.cycle` (`a.api` ↔ `b.api`) and requires each BND-3 set to copy the real layout (closed `recovery` `@ApplicationModule`, nested `@ApplicationModule`, `api` `@NamedInterface("api")`, plain `internal`). TASK-09 (`:43`) asserts nested modules by name before each `verify()` and stops per SPEC-007 if not detected. `plan.md:147`, TC-TE-001-03 (`scenarios.md:9`) and backend contract `bnd3Fixtures` agree. |
| REVIEW-RWB-TE-001-026 | Low | **RESOLVED** | Fixture root `th.co.scb.ace.recoveryfixture` (test scope, with reason) is in `docs/open-items.md:24` OPEN-023, PRE-2 `plan.md:31`, TASK-00 `tasks.md:29`, TASK-20 notice `tasks.md:64`, backend contract `fixtureRootApproval`. |
| REVIEW-RWB-TE-001-027 | Low | **NOT RESOLVED**: superseded by new Medium REVIEW-RWB-TE-001-029 | The planner applied the human's command exactly, plus a safe stop if `frontend/package-lock.json` is unchanged. Reviewer check shows that stop will always fire (see -029). |
| REVIEW-RWB-TE-001-028 | Low | **RESOLVED** | Committed in 8de8f95: `docs/increments/INC-002-epic-1-RWB-TE-001.md` 157/157 lines CRLF, `requirement/Traceability_Matrix.md` 426/426 CRLF. `git diff HEAD~1 --stat` and `--ignore-cr-at-eol` now both give 5 and 8 changed lines. `docs/open-items.md` diff is 1 line (endings kept). |

## New findings

| ID | Severity | Location | Maps to | Issue | Required fix |
|---|---|---|---|---|---|
| REVIEW-RWB-TE-001-029 | Medium | `tasks.md:54` (TASK-15 command and stop rule); `plan.md:170`; `contracts/frontend-integrations.json:93` | TASK-15, -16, -17, -18..-20; SPEC-015, -017; REVIEW-RWB-TE-001-027 | `npm install -D --save-exact … -w frontend` from the workspace root writes only the root `package-lock.json`. npm does not read or write a lockfile inside a workspace folder. Reproduced on 2026-11-09 in a scratch workspace shaped like ACE (root `workspaces: ["frontend"]`, standalone `frontend/package-lock.json`, npm 12.2.1, CI uses `node:22` with npm 10, same behaviour): after the command the root lockfile had the new package and `frontend/package-lock.json` was byte-identical (same md5, 0 matches). So TASK-15's rule "if `frontend/package-lock.json` is unchanged, stop and report" will always fire. The frontend chain (TASK-15 → 16 → 17) and the gate tasks 18–20 cannot finish without another planner run. SPEC-017 requires both lockfiles to be updated. The stop rule is safe, but the plan cannot be carried out as written. | Keep the human's root command, then add a second planned step in TASK-15, `plan.md:170` and the contract: from `frontend/`, `npm install --package-lock-only --workspaces=false`. In the same scratch workspace this updated `frontend/package-lock.json` with the new package and left the root lockfile as the first command wrote it. Keep the existing `git diff --stat` / `grep -c '"node_modules/vitest"'` checks on both files. Keep the stop rule for the case where the second step still leaves the file unchanged. The human who gave the -027 instruction should confirm the added step. |
| REVIEW-RWB-TE-001-030 | Low | `tasks.md:55` (TASK-16 `forbidden.ts`); `plan.md:193`; `scenarios.md:19` | TASK-16; SPEC-014 (ii); T-TE001-07; REVIEW-RWB-TE-001-023 | The gate 1 fix asked for `./../x` **and** a bare `..` in `forbidden.ts`. `plan.md:184` and the contract (`regexCheckedAgainst`) both say bare `..` is forbidden, but `forbidden.ts` has 10 imports and none of them is `..`. That case is checked only by the planner's node run, not by the ESLint fixture test that is the acceptance. | Add `..` (for example `import x from "..";`) as an 11th line of `forbidden.ts` in TASK-16, `plan.md:193` and T-TE001-07 (`scenarios.md:19`: "11 imports"). |

## Regression and consistency checks (no finding)

| Check | Result |
|---|---|
| Stale text after fixes | No `lcov` (HTML) reporter, `lcov-report`, `LoadSettings`, `--package-lock-only` (old form), "7 imports" for `forbidden.ts`, or "14 cases" left. `allowed.ts` stays at 7 imports. TASK-15's "copy reports, then delete the folder" does not conflict with TASK-17's second run, because deletion happens after the evidence is copied. |
| SPEC-RWB-TE-001-001..020 → TASK | 20/20 still mapped in `tasks.md`; each with verification. |
| Requirement-to-SPEC rows | 17/17 in `plan.md:212-230`, all `COVERED`, Coverage Types unchanged; exception rows unchanged. |
| `BLOCKED_BY` DAG | No `BLOCKED_BY` cell changed in the diff; same acyclic graph as gate 1 (00→01→{02,03,11,13}; 03→04→{05,06}; {03,04}→07; {06,07}→08; 07→09; {02,06}→10; {05,08,09,10,11}→12; 13→{14,15}→16→17; {12,17}→{18,19}→20). |
| Unit-test gates per surface | Backend REQUIRED: JaCoCo 80% LINE/INSTRUCTION/BRANCH/METHOD, native XML/HTML (TASK-11, -12). Frontend REQUIRED: v8 80% on all four metrics, `json-summary` + `lcovonly` native reports, 0/0 `PASS` recorded as printed (TASK-15, -17). Separate rows, no combined average (TASK-19). Unit-test tasks still `BLOCKED_BY` their implementation tasks. |
| Checkstyle reach | ACE `MissingJavadocType`/`MissingJavadocMethod` (scope protected) and `AbbreviationAsWordInName` (length 0) also apply to test sources, so names such as `BND1Fixture` or public types without Javadoc would fail `checkstyleTest`. TASK-07/-12 already require a clean run, so the Builder will find these. No plan change needed. |
| D-RCV-36 exclusions, PII/secrets, auth/audit/KYC | Unchanged from gate 1: PASS / N/A. |
| Shared-file list | Plan, PRE-2, TASK-00, OPEN-023 and both contracts agree (now including `frontend/vitest.config.ts` and the fixture root). No ESLint `ignores` or `.gitignore` edit, so the -021 option (a) adds no shared file. |

## Required checks summary

| Check | Result |
|---|---|
| Authentication / authorization | N/A (D-RCV-36) |
| Customer / account data protection | PASS |
| Audit logging | N/A |
| KYC/AML/suitability/consent/approval | N/A |
| Frontend integration versioning / error contract | N/A for API; lint contract consistent except -030 |
| Secrets and environment configuration | PASS |
| Plan requirement coverage | 17/17 rows, 20/20 SPEC |
| Unit-test gates planned | PASS (both surfaces, 80%, native reports) |
| Executability | FAIL: -029 (TASK-15 stop will always fire) |
| Traceability | PASS (-028 resolved) |
| Approval preconditions | PASS: PRE-1..PRE-4 pending and enforced by TASK-00 |

## Status lines

```text
REVIEW_STATUS: FAIL
REVIEW_TYPE: PLAN_GATE_REVIEW
RUN_ID: INC-002-epic-1-RWB-TE-001
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 1]
REVIEW_BLOCKING: YES [REASON: Medium REVIEW-RWB-TE-001-029 (root `npm install -w frontend` never updates frontend/package-lock.json, so the TASK-15 stop always fires)]
NEXT_STEP: Human records remediation or explicit acceptance of REVIEW-RWB-TE-001-029 (and disposition of Low -030); after remediation, re-run Implementation Planner and the plan gate review (gate 3). Gate 1 findings -021..-026 and -028 are resolved; -027 is carried into -029. PRE-1 (Product Owner spec approval) and PRE-2 (OPEN-023) remain pending before FDA plan approval. This review does not start Implementation Builder.
```
