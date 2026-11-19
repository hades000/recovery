---
title: "Data model: RWB-TE-002 Code owners for the recovery module"
run_id: "INC-004-epic-1-RWB-TE-002"
story: "RWB-TE-002"
revision: "v1 (18 Nov 2026): first data model for this repository, written by the continuation of the interrupted plan run; source `plan.md` v2."
---

# Data model: RWB-TE-002

No database change. No table, column, view, migration or persisted record is added or changed (D-RUN-07 not exercised). The "data" of this story is the code owners file, the owner register, the host configuration record, the MR template and the test-scope records that parse, validate and resolve them. No field holds personal data.

## 1. Test-scope model, grammar and messages

Package `th.co.scb.ace.demo.recovery.architecture.codeowners` under `backend/src/test/java/`, beside `RecoveryMigrationLintTest` and `RecoveryBoundaryTest`. It is test scope only: no main-source class, no jar entry.

### 1.1 Types

| Type | Members | Meaning |
|---|---|---|
| `CodeOwnersFile` | `Section`, `Entry`, `Problem`, `sections()`, `entries()`, `problems()` | Parsed `.gitlab/CODEOWNERS`, with 1-based line numbers |
| `OwnerRegister` | `Owner`, `ReservedPattern`, `owners()`, `reservedPatterns()`, `problems()` | Parsed `.gitlab/codeowners-register.yaml` |
| `CodeOwnersValidator` | `Level`, `Finding`, `validate(...)`, `failed(...)`, `repositoryRoot()` | Rules V1-V12 and the placeholder notes |
| `OwnershipResolver` | `resolve(...)` | SPEC-007 pure resolver |

Exact signatures:

```java
final class CodeOwnersFile {
    record Section(String name, int line) {}
    record Entry(String pattern, List<String> owners, int line, String section) {}
    record Problem(int line, String reason) {}
    static CodeOwnersFile parse(Path file);
    static CodeOwnersFile parse(List<String> lines);
    List<Section> sections();
    List<Entry> entries();
    List<Problem> problems();
}

final class OwnerRegister {
    record Owner(String handle, String role, String source, String status, String openItem) {}
    record ReservedPattern(String pattern, String basis) {}
    static OwnerRegister read(Path file);
    List<Owner> owners();
    List<ReservedPattern> reservedPatterns();
    List<String> problems();
}

final class CodeOwnersValidator {
    enum Level { ERROR, WARNING, INFO }
    record Finding(Level level, int line, String message, String pattern, String owner) {}
    static List<Finding> validate(Path repoRoot, Path codeOwners, Path register);
    static boolean failed(List<Finding> findings);
    static Path repositoryRoot();
}

final class OwnershipResolver {
    static Map<String, Set<String>> resolve(CodeOwnersFile file, Collection<String> changedPaths);
}
```

`Entry.section` is the enclosing section name; `null` means an orphan entry (V2). `Finding.line` is `0` for a register finding. `Finding.pattern` and `Finding.owner` are `null` when the rule does not name one. Lists are immutable and in file order.

### 1.2 Parser grammar

Read with `Files.readAllLines(file, UTF_8)`; line numbers are 1-based. For each line:

1. Strip trailing whitespace. A blank line or a line whose first non-blank character is `#` is skipped.
2. A line that starts with `[` must match `^\[([^\[\]]+)\]$` after trimming; otherwise it is `Problem(line, "syntax error")` (V1). The captured name is trimmed and becomes the current section.
3. A line that starts with `^` is `Problem(line, "syntax error")` (V1).
4. Any other line is an entry: split on whitespace. The first token is the pattern; the remaining tokens are the owners, possibly none. If no section is open, the entry is `Problem(line, "entry outside a section")` (V2) and takes no further rule.
5. A line that is a valid entry is kept even when its pattern or owner is later rejected by V3-V12, so that every finding carries its line.

`parse(Path)` throws `IllegalStateException("CODEOWNERS not found: " + file)` only when called directly on a missing file; `CodeOwnersValidator` checks existence first and returns the X9 finding.

### 1.3 Messages

The exact texts below are asserted by the tests. `{n}` is the 1-based line, `{p}` and `{q}` are patterns as written, `{s}` is a section name after trimming, `{o}` is an owner as written, `{team}` is an owner as written, `{role}` and `{openItem}` come from the register.

| Rule | Level | Exact message |
|---|---|---|
| V1 | ERROR | `line {n}: syntax error` |
| V2 | ERROR | `line {n}: entry outside a section` |
| V3 | ERROR | `line {n}: pattern {p} has no owner` |
| V4 | ERROR | `line {n}: unsupported pattern {p}` |
| V5 | ERROR | `line {n}: duplicate pattern {p} in section {s}` |
| V6 | ERROR | `line {n}: pattern {p} is shadowed by later pattern {q} in section {s}` |
| V7 | ERROR | `line {n}: owner {team} not found` |
| V8 | ERROR | `line {n}: owner {o} is not a team` |
| V9 | ERROR | `line {n}: pattern {p} matches no file` |
| V10 | WARNING | `line {n}: reserved pattern {p} matches no file ({basis})` |
| V11 | ERROR | `register: {problem}` |
| V12 | ERROR | `line {n}: duplicate section {s}` |
| Placeholder | WARNING | `owner {o} is a placeholder for {role} ({openItem})` |
| Assumed | INFO | `owner {o} is assumed ({openItem})` |
| X8, missing register | ERROR | `register: codeowners-register.yaml not found` |
| X8, unreadable register | ERROR | `register: codeowners-register.yaml is not readable: {io}` |
| X8, invalid YAML | ERROR | `register: invalid YAML: {problem}` |
| X8, root not a map | ERROR | `register: root is not a map` |
| X8, owners missing | ERROR | `register: owners is missing` |
| X8, owner not a map | ERROR | `register: owners[{i}] is not a map` |
| X8, owner field missing | ERROR | `register: owners[{i}] field {name} is missing` |
| X8, bad status | ERROR | `register: owners[{i}] status {value} is not one of ASSUMED, PLACEHOLDER, CONFIRMED` |
| X8, duplicate handle | ERROR | `register: owners[{i}] handle {value} is listed twice` |
| X8, reserved not a map | ERROR | `register: reservedPatterns[{i}] is not a map` |
| X8, reserved field missing | ERROR | `register: reservedPatterns[{i}] field {name} is missing` |
| X9, missing file | ERROR | `.gitlab/CODEOWNERS not found` |

Findings are ordered register problems first, then codeowners findings by line and, within a line, V1 to V12. `failed(findings)` is true when any finding is `ERROR`. A `WARNING` or `INFO` never fails validation.

### 1.4 Rule semantics

| Rule | Check |
|---|---|
| V1 | A line that starts with `[` but is not a lone `[Name]`, or starts with `^`, is a syntax error. |
| V2 | An entry before any section header is an orphan. It gets V2 only. |
| V3 | An entry with no owner token is rejected. |
| V4 | A pattern must start with `/` and contain none of `*`, `?`, `[`, `!`, `\`. A pattern that fails V4 gets no V5-V10 finding. |
| V5 | The same pattern string twice in one section is rejected. The same pattern in two different sections is allowed. |
| V6 | A pattern is shadowed when a later directory pattern in the same section covers it: a file pattern `p` when `p` without its leading `/` starts with `q` without its leading `/`; a directory pattern `p` when `p` without its leading `/` starts with `q` without its leading `/`. The later pattern must be a directory pattern. A duplicate pattern is reported by V5 only; V6 compares distinct patterns. |
| V7 | Every owner that passes V8 must be a `handle` in the register. If the register has no valid owners, V7 is skipped because V11 already fails. |
| V8 | An owner must match `^@[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$`. An owner that fails V8 gets no V7 finding. |
| V9 | Resolve the pattern against `repoRoot`: a file pattern is a regular file; a directory pattern is a directory with at least one regular file under it. A reserved pattern is skipped and handled by V10. |
| V10 | A pattern listed in `reservedPatterns` that matches no file is a warning with that entry's `basis`. |
| V11 | Register problems are listed in 1.3. A malformed owner is left out of `owners()`; the rest of the register is still read. Unknown YAML keys are ignored (PA-11). |
| V12 | Section names are compared after trimming and without regard to letter case. The later header is reported with its trimmed name. |
| Notes | One placeholder or assumed note per register owner, in register order; `PLACEHOLDER` is `WARNING`, `ASSUMED` is `INFO`. |

### 1.5 Resolver semantics (SPEC-007)

Input: a parsed `CodeOwnersFile` and repository-relative changed paths. Each path uses `/` separators; a backslash is normalised to `/` and a leading `./` is removed (PA-13).

For every path and every section, find the last entry in that section whose pattern matches. A directory pattern (one ending `/`) matches when the path starts with the pattern without its leading `/`; a file pattern matches when the path equals it without its leading `/`. Add the owners of the matched entry to that section's set. Union owners across paths; keep file order for sections and owner order within a line. A section with no match for any path is absent. Orphan entries never match.

Output: `LinkedHashMap<String section, Set<String> owners>`. Same input gives the same output (UT-20). The resolver is pure: no file system access, no clock, no random source.

### 1.6 Repository root and live inputs

`CodeOwnersValidator.repositoryRoot()` is `Path.of("").toAbsolutePath().getParent()`, and it checks that `.gitlab-ci.yml` exists there (PA-10). Gradle runs tests with `backend/` as the working directory, as `RecoveryMigrationLintTest` already assumes. Live validation reads `.gitlab/CODEOWNERS` and `.gitlab/codeowners-register.yaml` from that root.

### 1.7 Coverage scope (SPEC-014)

`codeOwnersCoverageVerification` measures the test source set's output classes under `th/co/scb/ace/demo/recovery/architecture/codeowners/`, excluding `**/*Test.class` and `**/*Test$*.class`. The four helper classes are measured; the five test classes are not. `sourceDirectories` is `sourceSets.test.get().java.srcDirs`. Execution data comes from `codeOwnersTest`. Limits are 0.80 for LINE, BRANCH, INSTRUCTION and METHOD. `recoveryCoverageReport` and `recoveryCoverageVerification` are not edited.

## 2. `.gitlab/CODEOWNERS` (exact content)

Line 276 of the spec block is the only substitution: `{te001FixtureRoot}` becomes `th/co/scb/ace/boundaryfixture`, the backend fixture root of RWB-TE-001 plan v7 (`F = backend/src/test/java/th/co/scb/ace/boundaryfixture`, TE-001 PA-01). TASK-00 confirms it on the merged code. Nothing else changes.

```text
# RWB-TE-002 code owners, GitLab format (L-RCV-12). Paths and owner handles only.
# Owner handles and their status are in .gitlab/codeowners-register.yaml (OPEN-038).
# Within a section the last matching pattern wins (BR5): general paths first, specific paths last.
# A file matched in several sections needs one approval from each of those sections.

[Common module]
/backend/src/main/java/th/co/scb/ace/demo/common/ @scb-ace/ace-team

[Recovery module]
/backend/src/main/java/th/co/scb/ace/demo/recovery/ @scb-ace/techx-recovery-tech-leads
/backend/src/test/java/th/co/scb/ace/demo/recovery/ @scb-ace/techx-recovery-tech-leads
/backend/src/test/java/th/co/scb/ace/demo/e2e/ @scb-ace/techx-recovery-tech-leads
/backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java @scb-ace/techx-recovery-tech-leads
/backend/src/test/java/th/co/scb/ace/boundaryfixture/ @scb-ace/techx-recovery-tech-leads
/backend/src/main/resources/db/modulemigration/recovery/ @scb-ace/techx-recovery-tech-leads
/backend/src/test/resources/architecture/recovery-modules.yaml @scb-ace/techx-recovery-tech-leads
/backend/src/test/resources/architecture/fixtures/ @scb-ace/techx-recovery-tech-leads
/frontend/src/modules/recovery/ @scb-ace/techx-recovery-tech-leads
/frontend/e2e/ @scb-ace/techx-recovery-tech-leads
/api/recovery-api-v4.yaml @scb-ace/techx-recovery-tech-leads
/frontend/src/api/schema.d.ts @scb-ace/techx-recovery-tech-leads
/frontend/eslint.config.js @scb-ace/techx-recovery-tech-leads

[Code owners control ACE team]
/.gitlab/CODEOWNERS @scb-ace/ace-team
/.gitlab/codeowners-register.yaml @scb-ace/ace-team
/.gitlab/host-settings.md @scb-ace/ace-team
/backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners/ @scb-ace/ace-team

[Code owners control recovery]
/.gitlab/CODEOWNERS @scb-ace/techx-recovery-tech-leads
/.gitlab/codeowners-register.yaml @scb-ace/techx-recovery-tech-leads
/.gitlab/host-settings.md @scb-ace/techx-recovery-tech-leads

[Repository standards]
/AGENTS.md @role-placeholder/solution-architect-with-tech-leads
/CLAUDE.md @role-placeholder/solution-architect-with-tech-leads
/.claude/ @role-placeholder/solution-architect-with-tech-leads
/aisdlc/.github/ @role-placeholder/solution-architect-with-tech-leads
/.gitlab/merge_request_templates/ @role-placeholder/solution-architect-with-tech-leads

[Pipeline gates]
/.gitlab-ci.yml @role-placeholder/techx-devops-with-scb-it
/backend/build.gradle.kts @role-placeholder/techx-devops-with-scb-it
/backend/settings.gradle.kts @role-placeholder/techx-devops-with-scb-it
/backend/gradle/ @role-placeholder/techx-devops-with-scb-it
/backend/gradlew @role-placeholder/techx-devops-with-scb-it
/backend/gradlew.bat @role-placeholder/techx-devops-with-scb-it
/frontend/package.json @role-placeholder/techx-devops-with-scb-it
/frontend/package-lock.json @role-placeholder/techx-devops-with-scb-it
/frontend/vite.config.ts @role-placeholder/techx-devops-with-scb-it
/frontend/tsconfig.json @role-placeholder/techx-devops-with-scb-it
/frontend/eslint.config.js @role-placeholder/techx-devops-with-scb-it
/frontend/playwright.config.ts @role-placeholder/techx-devops-with-scb-it
/scripts/dev.ps1 @role-placeholder/techx-devops-with-scb-it
```

## 3. `.gitlab/codeowners-register.yaml` (exact content)

```yaml
# Owner register for .gitlab/CODEOWNERS (RWB-TE-002). The local source of valid owners.
# No person, no membership, no e-mail. A handle changes only by an MR approved by both teams (BR7).
owners:
  - handle: "@scb-ace/techx-recovery-tech-leads"
    role: "TechX recovery tech leads (recovery tech lead plus the squad developers, D-RCV-21)"
    source: "Story Files v7, RWB-TE-002 section 3"
    status: ASSUMED
    openItem: OPEN-038
  - handle: "@scb-ace/ace-team"
    role: "ACE team"
    source: "Story Files v7, RWB-TE-002 section 3"
    status: ASSUMED
    openItem: OPEN-038
  - handle: "@role-placeholder/solution-architect-with-tech-leads"
    role: "Repository standards file owner: solution architect with the tech leads"
    source: "Engineering Practices v5 section 10; AI Assisted Development Approach v1 section 3"
    status: PLACEHOLDER
    openItem: OPEN-038
  - handle: "@role-placeholder/techx-devops-with-scb-it"
    role: "Pipeline gates owner: TechX DevOps with SCB IT"
    source: "Engineering Practices v5 section 10"
    status: PLACEHOLDER
    openItem: OPEN-038
reservedPatterns:
  - pattern: "/backend/src/main/java/th/co/scb/ace/demo/common/"
    basis: "BR3; DL05; RWB-TE-001 common root th.co.scb.ace.demo.common; OPEN-024"
```

## 4. `.gitlab/host-settings.md` (exact content)

```md
# Host configuration record: RWB-TE-002 code owners

Status: `OPEN — NOT_APPLIED_HERE`. No ACE GitLab host is connected in this run (RUN-BRIEF hard rule 5).

Owner of every row: the ACE team repository administrator with the recovery tech lead (story §3, §4 step 3; D-RCV-50). Apply HC-01..HC-08 on the ACE GitLab project, then run HV-01..HV-11 and record the MR link and result for each item. No row is applied here; no HV item is passed.

GitLab setting names are the specifier's mapping of story §12 under L-RCV-12 (ASM-TE002-10). The administrator confirms each name on the target tier (OPEN-038).

| ID | GitLab setting | Value | Branches | Source | Verified by |
|---|---|---|---|---|---|
| HC-01 | Repository > Protected branches: allowed to push and merge | No one (changes arrive by MR) | `main`, `develop-recovery`, `develop` | Story §12 "Require a pull request"; L-RCV-13 | HV-01 |
| HC-02 | Protected branch: code owner approval required | On | Same | Story §12 "require review from code owners"; BR6 | HV-01, HV-03 |
| HC-03 | Merge request approvals: required approvals | 1 | Same | Story §12 "1 approval" | HV-01 |
| HC-04 | Approval settings: prevent approval by author | On | Project | Story §12 "the author's approval does not count"; AC5 | HV-04 |
| HC-05 | Approval settings: when a commit is added, remove all approvals | On | Project | Story §12 "dismiss stale approvals"; AC6 | HV-05 |
| HC-06 | Merge checks: pipelines must succeed | On | Project | Story §4 step 6 (a failed check blocks); Engineering Practices v5 §7 gates block merge | HV-07 |
| HC-07 | Default MR description template | `Default` | Project | SPEC-015; A-10 | HV-09 |
| HC-08 | Groups for every `ASSUMED` handle exist with at least write (Developer) access to the project; `PLACEHOLDER` handles replaced first | Per register | Project | Story §12 "every owner exists and has write access"; §3 | HV-07, HV-11 |

"Allowed to merge" roles are not set by this story: D-RCV-50 and Engineering Practices v5 §4.2 decide who merges; the administrator applies them.
```

## 5. `.gitlab/merge_request_templates/Default.md` (exact content)

```md
## Story key

## Plan file

## Acceptance criteria covered

## Coding tool used

## AI first-pass review summary

## Reviewer

The reviewer is named on the merge request by the host's approval record. This template holds no person.

## Test results

## AISDLC trailers

The story commits carry `AISDLC-Run: <RUN_ID>` and `AISDLC-Plan: <plan path>`.
```

## 6. `backend/build.gradle.kts` addition (exact text)

Append after `recoveryCoverageVerification` (line 160). Nothing above it changes. No dependency is added. The three new tasks are not wired into `check`; only the existing `test` task gets the extra input declaration (PA-03).

```kotlin
// ---------------------------------------------------------------------------------------------
// RWB-TE-002 code owners validation (SPEC-013, SPEC-014). Defined here, run on the host.
//   codeOwnersTest                  JUnit tag "codeowners", also run by `test`
//   codeOwnersCoverageReport        JaCoCo report for the codeowners package
//   codeOwnersCoverageVerification  80% LINE, BRANCH, INSTRUCTION, METHOD
// ---------------------------------------------------------------------------------------------
val repositoryRoot = requireNotNull(rootDir.parentFile) { "RWB-TE-002: backend/ must sit in the repository root" }

val codeOwnersGovernanceInputs = files(
	repositoryRoot.resolve(".gitlab/CODEOWNERS"),
	repositoryRoot.resolve(".gitlab/codeowners-register.yaml"),
	repositoryRoot.resolve(".gitlab/host-settings.md"),
	repositoryRoot.resolve(".gitlab/merge_request_templates/Default.md"),
	repositoryRoot.resolve("AGENTS.md"),
	repositoryRoot.resolve(".gitlab-ci.yml")
)

val codeOwnersTest by tasks.registering(Test::class) {
	description = "RWB-TE-002 code owners and governance tests (@Tag codeowners)."
	group = "verification"
	inputs.files(codeOwnersGovernanceInputs)
	testClassesDirs = sourceSets.test.get().output.classesDirs
	classpath = sourceSets.test.get().runtimeClasspath
	useJUnitPlatform { includeTags("codeowners") }
	finalizedBy("codeOwnersCoverageReport")
}

tasks.named<Test>("test") {
	inputs.files(codeOwnersGovernanceInputs)
}

val codeOwnersClasses = files(sourceSets.test.get().output.classesDirs.map {
	fileTree(it) {
		include("th/co/scb/ace/demo/recovery/architecture/codeowners/**")
		exclude("**/*Test.class", "**/*Test\$*.class")
	}
})

val codeOwnersCoverageReport by tasks.registering(JacocoReport::class) {
	description = "JaCoCo report for the RWB-TE-002 codeowners package."
	group = "verification"
	executionData(tasks.named("codeOwnersTest").get())
	classDirectories.setFrom(codeOwnersClasses)
	sourceDirectories.setFrom(sourceSets.test.get().java.srcDirs)
	reports {
		xml.required = true
		xml.outputLocation = layout.buildDirectory.file("reports/jacoco/codeOwnersCoverageReport.xml")
		html.required = true
	}
}

val codeOwnersCoverageVerification by tasks.registering(JacocoCoverageVerification::class) {
	description = "Fails below 80% line, branch, instruction or method coverage on the RWB-TE-002 codeowners package."
	group = "verification"
	dependsOn(tasks.named("codeOwnersTest"))
	executionData(tasks.named("codeOwnersTest").get())
	classDirectories.setFrom(codeOwnersClasses)
	sourceDirectories.setFrom(sourceSets.test.get().java.srcDirs)
	violationRules {
		rule {
			limit { counter = "LINE"; minimum = "0.80".toBigDecimal() }
			limit { counter = "BRANCH"; minimum = "0.80".toBigDecimal() }
			limit { counter = "INSTRUCTION"; minimum = "0.80".toBigDecimal() }
			limit { counter = "METHOD"; minimum = "0.80".toBigDecimal() }
		}
	}
}
```

## 7. `.gitlab-ci.yml` addition (exact text)

Add after `frontend-check` and before `backend-recovery-it`. Same flow style as the existing jobs. No `rules:` key: the job runs on every pipeline (story §12 trigger). The job is defined here and run on the host (HV-07); this repository has no GitLab runner.

```yaml
codeowners-validation:
  stage: verify
  image: eclipse-temurin:21-jdk
  cache: { key: gradle, paths: [.gradle-home/] }
  script:
    - cd backend && ./gradlew --no-daemon codeOwnersTest codeOwnersCoverageVerification
  artifacts:
    when: always
    reports: { junit: backend/build/test-results/codeOwnersTest/*.xml }
    paths: [backend/build/reports/jacoco/codeOwnersCoverageReport/]
```

## 8. Evidence and test data

- Fixtures are synthetic file trees under `@TempDir`; no fixture is written into `.gitlab/`, `backend/src/main/` or the migration folder.
- The only owner handle used to prove AC7/X6 is the synthetic typo `@scb-ace/recovery-leads-typo` (story AC7). It is never added to the register or the live file.
- The resolver inputs of UT-13..UT-18, UT-20, UT-25 and UT-26 are synthetic path strings; UT-15's `V9999__rwb_te_002_resolver_fixture.sql` is never written to disk and fixes no migration number (D-RUN-07).
- No person, real e-mail address, membership, token or credential appears in any file, test or report. The UT-08 negative values `@someone` and `someone@example.test` are synthetic test data, not a person or a real address. The host settings record names roles only.
- TASK-08 evidence: `implement/backend/coverage/codeOwnersCoverageReport.xml`, its HTML folder, and the `implement/unit-tests/report.md` table with one backend row and one frontend `NOT_APPLICABLE` row.
