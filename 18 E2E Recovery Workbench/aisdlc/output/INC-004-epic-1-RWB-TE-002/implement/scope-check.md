# TASK-09 security, privacy, guardrail and scope check

Branch `feature/RWB-TE-002-code-owners`, tip `ae61b08` (code), base `develop-recovery` `7bee04d`. Commands run from the worktree root on 18 Nov 2026.

| # | Check | Command | Result |
|---|---|---|---|
| 1 | Only plan files changed | `git diff --stat develop-recovery...HEAD` | 16 files: `.gitlab-ci.yml`, the four `.gitlab/` files, `AGENTS.md`, `backend/build.gradle.kts`, four helper classes and five test classes in `…/recovery/architecture/codeowners/`. 1480 insertions, 5 deletions (the five AGENTS.md §5 cells). PASS |
| 1b | No out-of-scope path | `git diff --name-only … \| ? { $_ -match '^(backend/src/main/\|frontend/\|scripts/\|infra/\|api/)' }` | empty. No `common/` or `collection/` file. PASS |
| 1c | CI diff | `git diff … -- .gitlab-ci.yml` | adds only the `codeowners-validation` job; no removed line; no browser runner. PASS |
| 2 | Personal data / secrets | `Select-String` over every changed file for e-mail, `+66`, 13-digit number, `password\|secret\|token\|apikey =` | One hit only: `someone@example.test` in `CodeOwnersValidationTest.java` lines 186 and 191, the UT-08 synthetic negative value (`.test` reserved domain), allowed by the plan; it is not in the live file or register. No person's name anywhere; owners are group or role handles. PASS |
| 3 | No dependency added | `git diff … -- backend/build.gradle.kts` filtered for removed lines and `implementation\|testImplementation\|dependencies` | no match: the `dependencies { }` block is untouched; SnakeYAML 2.6 already on both test classpaths (preflight #3). `./gradlew dependencies` before/after diff not re-run: the build file diff is append-only below the dependency block (DEV-03). PASS |
| 4 | No endpoint / method security / host token | `Select-String` for `@RestController\|@PreAuthorize\|@RequestMapping` | none. No host API is called. PASS |
| 5 | No RWB-TE-001 file edited; no collection/common file | diff list (#1) | none of TE-001's files appears. `recoveryCoverage*` tasks unchanged. PASS |
| 6 | HV items not claimed | `handoff.md` | HV-01..HV-11 all `OPEN — NOT_TESTED_HERE`. PASS |
| 7 | No skipped or weakened test | `Select-String` for `@Disabled\|@Ignore\|assumeTrue\|Assumptions.` | none. All 28 codeowners tests run (JUnit XML: 0 skipped). PASS |
