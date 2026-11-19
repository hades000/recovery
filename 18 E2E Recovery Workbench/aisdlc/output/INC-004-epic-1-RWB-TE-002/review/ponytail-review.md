# Ponytail review: RWB-TE-002 code owners

Scope: `git diff develop-recovery...feature/RWB-TE-002-code-owners` (tip `ae61b08`, 16 files, +1480/-5), read with the connected code in the worktree `rwb-wt/RWB-TE-002`. Checked against `specify/spec.md` (V1-V12, SPEC-013/014), `plan/plan.md` and `implement/implementation-report.md`.

Load assumed: a test-scope validator that runs once per pipeline and once per local `gradlew test`, on a file of about 50 lines. No runtime code, no users, no concurrency. Scale and speed are not a concern at this size.

What this change does: It adds a GitLab code owners file, a small register of the allowed owner teams, a host-settings record and an MR template. It adds test-scope Java helpers that parse the code owners file, check it against twelve rules (V1-V12) and work out which teams must approve a path, plus 28 tests, a `codeOwnersTest` Gradle task with an 80% coverage gate and one CI job that runs them. It also fixes the six context paths in the AGENTS.md section 5 table.

## Must fix

1. **An empty owner register lets any team through** (`backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners/CodeOwnersValidator.java:L107`)
   - **What this is:** Rule V7 says every owner in CODEOWNERS must be listed in the register (AC7). This line checks it.
   - **Problem:** The check is skipped when the register holds no owners (`!handles.isEmpty() &&`). A register of `owners: []` is well formed, so it raises no register error either. Concrete case: set `owners: []` and put `@any-group/any-team` on a line in CODEOWNERS; `validate` returns no ERROR and the job passes. The control fails open, against V7.
   - **Fix:** Skip the "not found" check only when the register already failed, not when it is empty: replace `!handles.isEmpty()` with `register.problems().isEmpty()`. The existing `registerProblemsFailClosed` cases all carry a register problem, so they keep their exact messages. Add one test: register `owners: []` plus an entry owned by `@scb-ace/ace-team` gives `line 2: owner @scb-ace/ace-team not found`.
   - **If we skip it:** One MR that empties the register makes the owner check pass for any group, and nothing in the pipeline says so.

## Nice to have

2. **A `..` in a pattern can fool the "matches a file" rule** (`CodeOwnersValidator.java:L142-L144`, used at `L146-L149`)
   - **What this is:** `supported` decides which patterns are allowed (V4); `matchesAFile` then checks the pattern points at a real file (V9).
   - **Problem:** V4 does not forbid `..`. `/backend/../AGENTS.md` resolves to `AGENTS.md` on disk, so V9 passes, but GitLab never matches that pattern, so AGENTS.md would have no owner on the host while the check is green.
   - **Fix:** Add `&& !pattern.contains("/../")` to `supported` (it then reports `unsupported pattern`). One condition, no new rule text needed.
   - **If we skip it:** Low odds; a typo or a clever edit could leave a file unowned on the host with a passing check.

3. **Local `gradlew test` can skip the code owners checks after a file is deleted** (`backend/build.gradle.kts:L188-L195`, `L200`, `L207-L209`)
   - **What this is:** The six governance files are declared as task inputs, so Gradle reruns the tests when one of them changes.
   - **Problem:** V9 and UT-26 also depend on other repository files. Delete `scripts/dev.ps1` or `frontend/playwright.config.ts` locally and `gradlew test` is UP-TO-DATE, so V9 does not report the dead pattern. CI starts from a clean `build/`, so the pipeline still catches it.
   - **Fix:** On `codeOwnersTest` only, add `outputs.upToDateWhen { false }`, or accept it as is since CI covers it.
   - **If we skip it:** A developer may see green locally and red in the pipeline. No wrong merge.

## Checked and not a finding

- Parser (V1, V2), duplicate section (V12, case-insensitive), duplicate pattern per section block (V5), shadowing (V6, same section, later directory pattern), owner form (V8), reserved pattern warning (V10), register reading (V11, SafeConstructor YAML, fail closed): logic matches the spec table, and each rule has a positive and a negative test.
- Resolver: last match per section, union across sections, file order. Matches GitLab semantics for the restricted syntax V4 allows.
- CODEOWNERS content: control files and the codeowners package need both teams; `/frontend/eslint.config.js` needs recovery and pipeline sections (UT-26 C).
- Gradle: JaCoCo applies to the new `Test` task; both JaCoCo tasks use `codeOwnersTest` execution data; verification depends on the test task (SPEC-014). The codeowners tests also run in `backend-unit` via `test`; this is by spec (SPEC-013 (1)) and costs a few seconds.
- Placeholder owners (`@role-placeholder/...`) on `.gitlab-ci.yml`, `build.gradle.kts` and AGENTS.md give no real approval on GitLab until replaced. This is a recorded decision (register `PLACEHOLDER`, validator WARNING, HC-08, OPEN-038), not a finding.
- Merge fact (not a finding): `backend/src/test/resources/architecture/magic-number-baseline.csv` from RWB-E1-042 will be reported unowned by UT-26 until a CODEOWNERS line is added after that merge (IM-SU-01).
- Build evidence: 28 codeowners tests pass, coverage 95.7/95.8/96.8/100; full `dev.ps1 test` passes at `ae61b08`.

Verdict: Fix 1 before merge.
Not checked: the host side (HC-01..HC-08, HV items) and a real GitLab pipeline run; both are out of scope here by spec.
