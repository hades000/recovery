# Security review: RWB-TE-002 code owners

- Diff: `git diff develop-recovery...feature/RWB-TE-002-code-owners` (tip `ae61b08`), 16 files, +1480/-5
- Method: the `security-review` skill did not start. It needs the session working directory to be a git repository, and the session root (`Recovery Workbench SharePoint Set v14`) is not one. I reviewed the diff by hand against the same criteria, and also checked the full branch tree for sensitive paths that the diff leaves unowned.
- Scope checked: CODEOWNERS coverage of sensitive paths, the validator and resolver helpers (path traversal, pattern handling, fail-open behaviour), file writes and process execution in tests, the CI job and Gradle block, and personal data or credentials in the files.

## Findings

### F1. High: a root `/CODEOWNERS` or `/docs/CODEOWNERS` silently replaces `.gitlab/CODEOWNERS`, and neither path is owned
- File: `.gitlab/CODEOWNERS` lines 24-33 (the two "Code owners control" sections protect only `/.gitlab/CODEOWNERS`).
- Exploit: GitLab reads the first CODEOWNERS file it finds, in this order: `/CODEOWNERS`, then `/docs/CODEOWNERS`, then `/.gitlab/CODEOWNERS`. An MR that adds a root `CODEOWNERS` matches no owned pattern, so it needs only the generic single non-author approval (HC-03/HC-04). It does not need ACE team plus recovery tech leads. Once it merges, the new file replaces every rule in `.gitlab/CODEOWNERS`, and that includes the dual-team self-protection (BR7). The validator does not catch this either, because it only ever parses `.gitlab/CODEOWNERS`.
- Fix:
  - Add `/CODEOWNERS` and `/docs/CODEOWNERS` to both "Code owners control" sections, and list them under `reservedPatterns` in the register so that V10 reports a WARNING and not an ERROR.
  - Add a `@Tag("codeowners")` test that fails if either file exists in the repository.

### F2. High: the security and migration settings file is unowned
- File: `backend/src/main/resources/application.yaml` (not in `.gitlab/CODEOWNERS`; explicitly deferred in plan.md:158, PA-06; `OwnershipResolverTest.java:167` asserts that unlisted paths have no owner).
- Exploit: this file sets `recovery.security.issuer` (line 85, OIDC issuer), the Flyway migrator datasource and its credential variable (lines 78-83), and the migration `location` (line 83). An MR could point the issuer at an identity provider the attacker controls (authentication bypass), or move `location` away from `db/modulemigration/recovery`. The owned migration folder would then be bypassed and the DDL would run with migrator rights. That MR needs only one generic approval, and the recovery tech leads, who own `SecurityConfig.java` and `RecoveryFlywayConfig.java`, are not required to approve it. `application-local.yaml` has the same gap.
- Fix: add `/backend/src/main/resources/application.yaml` and `/backend/src/main/resources/application-local.yaml` to `[Recovery module]` and to a section that the ACE team owns, because the file is shared. Alternatively, record a signed-off risk acceptance against PA-06 before the host settings are applied.

### F3. Medium: placeholder owners leave the CI file, build scripts, Gradle wrapper and agent instructions without code-owner approval, and the validator passes anyway
- Files:
  - `.gitlab/CODEOWNERS` lines 35-55 (`[Repository standards]` and `[Pipeline gates]`)
  - `.gitlab/codeowners-register.yaml` lines 14-23 (`status: PLACEHOLDER`)
  - `CodeOwnersValidator.java` lines 55-58 (placeholder reported only as a WARNING)
- Exploit: `@role-placeholder/...` groups do not exist on the host. GitLab ignores owners that are not valid. When a section has no eligible approver, its code-owner rule is not enforced. So `.gitlab-ci.yml`, `build.gradle.kts`, `gradlew`, `gradle/wrapper/gradle-wrapper.jar` (supply chain), `AGENTS.md`, `CLAUDE.md` and `.claude/` change with one generic approval. That includes changes that turn off the `codeowners-validation` job or the coverage gate. HC-08 in `host-settings.md` says placeholders must be replaced first, but nothing enforces that, and the pipeline stays green while they remain.
- Fix:
  - Make PLACEHOLDER an ERROR outside this run, for example with a validator flag set in CI, or a CI rule that fails on protected or default-branch pipelines while any PLACEHOLDER remains.
  - Make HC-08 a blocking precondition for HC-02 in `host-settings.md`.
  - Until the handles are replaced, add `@scb-ace/ace-team` as a second owner on the `[Pipeline gates]` entries, so that at least one valid group must approve.

### F4. Medium: the container build file is unowned
- File: `backend/Dockerfile` and `backend/.dockerignore` (not in `.gitlab/CODEOWNERS`, and not in the spec's out-of-scope list at spec.md:537).
- Exploit: a change to the base image, an added `RUN curl | sh`, or a `.dockerignore` change that copies `.env` or build secrets into the image needs only a generic approval.
- Fix: add `/backend/Dockerfile` and `/backend/.dockerignore` to `[Pipeline gates]`. This should be done together with the F3 fix, so that the section has a valid owner.

### F5. Low: test fixtures for the migration-lint and Flyway gates are unowned
- Files: `backend/src/test/resources/migration-lint/`, `backend/src/test/resources/flyway-fixtures/` (plan.md:356, R-3, PROP-OI-4).
- Exploit: weakening a fixture, for example deleting a `*-fail` case, makes the D-RCV-44 migration gate's tests pass vacuously, without recovery tech lead approval.
- Fix: add both folders to `[Recovery module]`, as PROP-OI-4 already proposes.

### F6. Low: the owner-existence check fails open when the register's owner list is empty
- File: `CodeOwnersValidator.java` line 107 (`!handles.isEmpty() && ...`); `OwnerRegister.java` lines 73-78.
- Exploit: `owners: []` is valid YAML. It produces no register problem, `handles` is empty, and every owner handle in CODEOWNERS is then accepted without a check (V11 is skipped). An MR could empty the register and add any handle. The register is owned by both teams, which limits the risk.
- Fix: report `owners is empty` as an ERROR in `OwnerRegister.read`, and drop the `handles.isEmpty()` short-circuit.

### F7. Low: patterns are not contained to the repository root
- File: `CodeOwnersValidator.java` lines 142-148 (`supported` allows `..`; `matchesAFile` resolves without normalising).
- Exploit: a pattern such as `/backend/../../outside/` passes V4. It also passes V9 when the target exists outside the checkout, because the validator reads only metadata (existence checks and a directory walk). GitLab treats the line as a pattern that matches nothing, so a reviewer can think a path is owned when it is not. Nothing is written or executed, which is why this is rated Low.
- Fix: reject any pattern that contains a `..` or `.` segment in `supported()`. In `matchesAFile`, normalise `target` and require `target.startsWith(root.normalize())`.

### F8. Low: CI cache shared across jobs, and an image tag that is not pinned
- File: `.gitlab-ci.yml` lines 33-36 (new `codeowners-validation` job: `cache: { key: gradle }`, `image: eclipse-temurin:21-jdk`).
- Exploit:
  - Cache: the job shares the `gradle` cache key with `backend-unit`. A pipeline on an MR branch can write poisoned Gradle artifacts that a later pipeline restores. This only works if "separate caches for protected branches" is turned off on the host.
  - Image: the floating tag can change under the job.
- Fix: confirm that separate protected-branch caches are on, and add the check to `host-settings.md`. Pin the image by digest. The job uses no secrets, no `services`, no privileged mode and no variables beyond the global ones, so no secrets exposure was found.

## Checked with no finding
- Process execution: no tests or helpers use `ProcessBuilder`, `Runtime.exec` or `git`.
- File writes: every write in the tests goes under JUnit `@TempDir` (`CodeOwnersValidationTest.java` lines 401-423). Tests against the real repository only read files.
- YAML loading: `OwnerRegister.java` line 63 uses `SafeConstructor`, so there is no arbitrary-type deserialisation.
- Regular expressions: `TEAM`, `UNSUPPORTED` and `HEADER` are linear and have no catastrophic backtracking. Wildcards are rejected, so no glob is interpreted.
- Gradle block: it declares inputs and JaCoCo tasks only. There are no downloads, no `exec` and no credential use.
- CODEOWNERS self-protection: `.gitlab/CODEOWNERS`, the register and `host-settings.md` each need approval from both the ACE team and the recovery tech leads (lines 24-33). This is correct, apart from the precedence gap in F1.
- Personal data and credentials: the diff contains no names of people, e-mail addresses, tokens or passwords. The owner handles are group names only. `application.yaml` (outside the diff) uses only environment-variable placeholders.
- `AGENTS.md`: the change only corrects context-file paths. It adds no instructions.

## Verdict

FAIL: 0 Critical, 2 High, 2 Medium, 4 Low (8 findings in total). F1 and F2 must be fixed, or formally accepted with a named owner, before the host settings HC-01 to HC-08 are applied.
