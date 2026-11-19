---
title: "Data model: RWB-TE-011 PDPA lint for code, tests and logs"
run_id: "INC-006-epic-1-RWB-TE-011"
story: "RWB-TE-011"
revision: "v2 (18 Nov 2026): remediation of plan-gate round 1 findings PLAN-001..PLAN-006; source plan.md v2 and spec run 12. No requirement, SPEC or scope change."
---

# Data model: RWB-TE-011

**No database change.** No table, column, view, index, migration or persisted record is added or changed (D-RUN-07 not exercised). This story writes no `V<seq>__rwb_te_011_*.sql` and no file under `backend/src/main/resources/db/`. The "data" is the read-only dictionary input, the tool's two configuration files, the generated rules file and the records the tool passes between its components. No field holds personal data.

## 1. Generated `pdpa-rules.yaml`

Written on every run that completes the dictionary, before scanning; under `P/build/pdpa-rules.yaml`; not committed; deterministic (byte-identical for the same inputs). Entries are sorted by `name`, then `fieldId` (a `null` `fieldId` sorts last), rules are in the fixed order below, and there is no timestamp. `generatedFrom.dictionary` is the baseline followed by each migration file in Flyway order.

```yaml
generatedFrom:
  dictionary:
    - infra/postgres/schema/03-recovery-physical-schema-v6.sql
    - backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_001_baseline.sql
  api: api/recovery-api-v4.yaml
rules:
  - PDPA-LOG-FIELD
  - PDPA-LOG-ENTITY
  - PDPA-EXCEPTION
  - PDPA-TOSTRING
  - PDPA-FIXTURE-FIELD
  - PDPA-FIXTURE-ID
fields:
  - name: last_name
    fieldId: DF-ACE-058
    object: v_ace_customer
    dataType: TEXT
    keys:
      - [v_ace_customer, last_name]
      - [customer, surname]
    unambiguousName: true
    variants: [last_name, lastName, getLastName]
apiPersonalNames: [capture_latitude, capture_longitude, extracted_value, field_value, summary]
entityTypes: [ContactEntity, ContactView, CustomerEntity, CustomerView]
```

Notes:

- One `fields` entry per personal field. A dictionary row carries `fieldId`, `object`, `dataType` and its keys; an API-only pair carries `fieldId: null`, `object` = snake case of the schema name and `dataType: TEXT`.
- `keys` holds `(object_name, field_name)` first, then `(table, column)` from a `source_field` of the form `<schema>.<table>.<column>`, then the API pair. Keys are de-duplicated and sorted after the first.
- `variants` is snake case, camel case and `get` + Pascal case of the field name.
- `unambiguousName` is computed over **every** dictionary row with that `field_name` (personal or not), not over API pairs.
- `entityTypes` is Pascal case of the object name with a leading `v_ace_` removed, plus each configured suffix (`Entity`, `View`), sorted and de-duplicated.
- `apiPersonalNames` is the snake case of every property with `x-personal-data: true`, sorted.

## 2. Internal model (the tool's records and seams)

Package `th.co.scb.ace.tools.pdpa`. Types are package-private unless the test package needs them. The Builder keeps these names and responsibilities; the method bodies are free within the spec.

| Type | Responsibility and key members |
|---|---|
| `PdpaLint` | `main(String[])`: parse options, call `PdpaLintStep.run`, print the report, return the exit code |
| `PdpaLintStep` | `Result run(Options)`: config, layout, reader, generator, scope, scanners, allow list, corrective rules, report |
| `cli.CliOptions` | Parsed options and defaults; unknown option and a missing value give a configuration error |
| `config.LintConfig` | Immutable records for every section of §3, including the nested `FixtureIdPattern` record (`name`, compiled `forms`, optional `checksum`, optional domain exemptions) and its nested `Checksum` and `DomainExemptions` records; no new top-level type |
| `config.ConfigLoader` | `LintConfig load(Path file)`; exact error texts of §5 |
| `config.RepositoryLayout` | `Path repoRoot`, `Path migrationFolder`, `Path config`, `Path rulesOut`, `Path allowList`; reads `rwb.flyway.location` from `backend/src/main/resources/application.yaml` |
| `dictionary.PersonalField` | `fieldId`, `objectName`, `fieldName`, `dataType`, `sourceField`, `active`, `personal`, `keys`, `unambiguousName` |
| `dictionary.Dictionary` | `personalFields()`, `byFieldId()`, `at(Path migration)` snapshots, `describes(object, field)`, `isPersonal(object, field)`, `isUnambiguous(name)`, `apiPersonalNames()` |
| `dictionary.PersonalFieldReader` | `ReadResult read(Path baseline, List<Path> migrations, List<Path> files)`; R1, R2, ignored, fail closed, order, notices, snapshots |
| `dictionary.ApiSpecificationReader` | `ApiReadResult read(Path yaml)`; `x-personal-data` pairs and names |
| `dictionary.RuleGenerator` | `RulesFile generate(Dictionary)` |
| `sql.SqlStatement` | `startLine`, `text`, offsets, and the value slots a classifier fills |
| `sql.SqlSplitter` | `List<SqlStatement> split(String text)`; quote-aware single pass; located `SqlSyntaxException` |
| `sql.SqlTarget` | `table`, `column`, `tableLiteral`, `columnLiteral` |
| `sql.SqlValueSlot` | `target`, `start`, `end`, `isDefault`, `literal` |
| `scan.ScannedFile` | `Path relative`, `Set<FileClass> classes`, `String text`, line index |
| `scan.ScanScope` | `List<ScannedFile> files()`, `List<Root> roots()`, `List<Exclusion> exclusions()`, `List<Root> lintFixtures()`, probe check, `ScopeSummary` counts |
| `scan.SourceLexer` | `List<Token> lex(String text)`; kinds: identifier, string, text block, template-literal part, comment, punctuation; template `${…}` expressions are code |
| `scan.SourceIndex` | Declarations (field, parameter, local, record component, `var`), type members, `@Table(name = …)`, `schema.d.ts` schemas |
| `scan.LogScanner` | `List<Finding> scan(ScannedFile, SourceIndex, Dictionary)` for LOG-FIELD, LOG-ENTITY, EXCEPTION, TOSTRING and the masking exemption |
| `scan.SqlFixtureScanner` | `ScanResult scan(ScannedFile, Dictionary)`; classes 1–4, positions, `(columns not named)`, `(statement not recognised)`, `(DML in procedural body)`, slots |
| `scan.FixturePositionScanner` | Java and TypeScript positions and their object resolution |
| `scan.JsonFixtureScanner` | JSON key values with line numbers and `fixtureObjects` |
| `scan.FixtureIdMatcher` | `List<TextMatch> matches(String text)`; reads the configured `FixtureIdPattern` list, applies each compiled form, then the optional checksum and domain exemptions; pattern name, start, end, line; holds no pattern, weight, domain or TLD |
| `scan.Finding` | `rule`, `file`, `line`, `field`, `token`, `target` (nullable `SqlTarget` list for a procedural body) |
| `scan.Notice` | One of the four kinds, with its file, line, field or field id and corrective file |
| `scan.Rule` | The six rule IDs |
| `allow.AllowEntry` | `rule`, `path`, `line`, `pattern`, `owner`, `reason`, `expires` |
| `allow.AllowList` | `List<Finding> apply(List<Finding>, LocalDate runDate)`; returns findings plus the expired lines; validation before scanning |
| `changes.GitRunner` | `boolean resolve(String ref)`, `String mergeBase(String target)`, `List<String> changedFiles(String base)`; a fake records calls |
| `changes.ProcessGitRunner` | The `GitRunner` implementation that runs `git merge-base` and `git diff --name-only --diff-filter=AMR` in the repository root and returns their results; the only type that starts a process |
| `changes.ChangedFileList` | `Decision decide(String target, String branch)`; no git call unless built |
| `scan.CorrectiveMigrations` | `Result apply(List<Finding>, List<MigrationFile>, ChangedFileList.Decision)`; conditions (a)–(e) |
| `report.Report` | `String render(...)`, `int exitCode()`; sorting, lines, counts, scope lines |
| `report.RulesFileWriter` | `void write(Path, RulesFile)`; LF, UTF-8, sorted, no timestamp |

`Finding.target` for a procedural body is the set of readable written tables (SPEC-TE011-018 (d)). A finding with no readable table carries an empty list; the corrective rule treats an empty list as "no table write required" except for a `DEFAULT` whose table is a placeholder, which is never accepted.

## 3. `P/pdpa-lint.yaml` (production content)

The file is the production configuration; code owners review it (SPEC-TE011-014, -015). Keys are fixed by this plan. `roots[n]`, `exclusions[n]`, `lintFixtureRoots[n]` and `roots[n].except[n]` are the `{config key}` values in the messages. A root's `except` globs are printed as exclusions with their own keys.

```yaml
# tools/pdpa-lint/pdpa-lint.yaml
# Story: RWB-TE-011. Owned by /tools/pdpa-lint/ (SPEC-TE011-014).
# No personal field name, personal object name, prefix, FIXTURE-ID pattern name, form,
# check-digit weight, example domain or reserved TLD is hard-coded in the tool (SPEC-TE011-015);
# sys_fields and its columns are the reader's rule vocabulary. The three FIXTURE-ID patterns are
# defined below.
dictionary:
  baseline: infra/postgres/schema/03-recovery-physical-schema-v6.sql
  migrationFolder: backend/src/main/resources/db/modulemigration/recovery
  files: []
api:
  specification: api/recovery-api-v4.yaml
allowList: tools/pdpa-lint/pdpa-allow.yaml
scan:
  roots:
    - class: production
      glob: backend/src/main/java/th/co/scb/ace/demo/recovery/**/*.java
    - class: production
      glob: frontend/src/modules/recovery/**/*.{ts,tsx}
      except:
        - frontend/src/modules/recovery/**/__tests__/**
        - frontend/src/**/*.test.{ts,tsx}
    - class: seeds
      glob: backend/src/main/resources/db/modulemigration/recovery/**/*.sql
    - class: tests
      glob: backend/src/test/**/*.{java,sql,json}
    - class: tests
      glob: backend/src/test/resources/**
    - class: tests
      glob: frontend/src/modules/recovery/__tests__/**
    - class: tests
      glob: frontend/src/**/*.test.{ts,tsx}
    - class: tests
      glob: frontend/src/test/**
    - class: tests
      glob: frontend/e2e/**/*.{ts,json}
    - class: infra
      glob: infra/**
    - class: tool
      glob: tools/pdpa-lint/**
  exclusions:
    - infra/postgres/schema/**
    - frontend/src/api/schema.d.ts
    - "**/node_modules/**"
    - "**/build/**"
    - "**/dist/**"
    - "**/coverage/**"
  lintFixtureRoots:
    - backend/src/test/resources/migration-lint/**
fixtures:
  syntheticPrefix: "SYN-"
  fixtureIdPatterns:
    - name: thai_national_id
      forms:
        - '(?<!\d)\d{13}(?!\d)'
        - '(?<!\d)\d-\d{4}-\d{5}-\d{2}-\d(?!\d)'
      checksum:
        digitCount: 13
        weights: [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        modulus: 11
        subtractFrom: 11
        resultModulus: 10
    - name: thai_mobile
      forms:
        - '(?<!\d)0[689]\d{8}(?!\d)'
        - '(?<!\d)0[689]\d[ -]\d{3}[ -]\d{4}(?!\d)'
        - '(?<!\d)\+66[ -]?[689]\d{8}(?!\d)'
        - '(?<!\d)\+66[ -]?[689]\d[ -]\d{3}[ -]\d{4}(?!\d)'
        - '(?<!\+)(?<!\d)66[ -]?[689]\d{8}(?!\d)'
        - '(?<!\+)(?<!\d)66[ -]?[689]\d[ -]\d{3}[ -]\d{4}(?!\d)'
    - name: email
      forms:
        - '(?i)(?<![A-Z0-9._%+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![A-Z0-9.-])'
      exemptDomains:
        - example.com
        - example.net
        - example.org
      exemptDomainSuffixes:
        - .test
        - .example
        - .invalid
        - .localhost
  fixtureObjects: []
source:
  javaLoggerNames: [log, logger, LOG, LOGGER]
  tsLoggerNames: []
  exceptionTypes: []
  maskingHelpers: []
  entitySuffixes: [Entity, View]
changedFiles:
  targetBranch: develop-recovery
  protectedBranches: [main, develop]
```

Behaviour of the keys:

- Globs use Git-style semantics, not `java.nio.file.PathMatcher` literally: `**` matches **zero or more** path segments, `*` matches within one segment, `{a,b}` is an alternative and `?` one character, all matched against `/`-normalised repository-relative paths. A file directly under a root matches (`recovery/package-info.java` and `recovery/V<seq>__...sql`), and so does a nested file. This is the intended reading of the spec's `**/*.java` and `**/*.sql`; Java's own `**/` would skip the top-level file and the top-level migration. UT-TE011-12 pins both cases.
- `dictionary.migrationFolder` must equal the folder derived from `rwb.flyway.location`; the property is the single source (SPEC-TE011-003). A different path, a missing property, a placeholder or a non-`classpath:` value gives exit 2.
- `dictionary.files` may list further committed dictionary files in recognised forms (none by default).
- `scan.roots[].class` is one of `production`, `seeds`, `tests`, `infra`, `tool`. A file in the lint-fixture class is classified there only; otherwise the union of every matching root's rules applies. `roots[].except` carries the production root's documented exclusions (`__tests__/**` and `*.test.*`), so those files fall to the tests class; each `except` glob is printed as an exclusion with key `roots[n].except[m]`.
- `scan.exclusions` may not match any file or probe path in the migration folder. `infra/postgres/schema/**` is excluded because it holds the three read-only copies, including the dictionary input; `frontend/src/api/schema.d.ts` is generated and read only to recognise entity types.
- `scan.lintFixtureRoots` must lie under a test root's fixed prefix. A root outside them gives exit 2.
- `fixtures.fixtureIdPatterns` is the only definition of the three patterns. Each has a unique `name`, one or more Java regular-expression `forms`, and optional `checksum` and domain exemption lists. A duplicate name, an empty `forms`, a form that does not compile, or a checksum whose `digitCount` is not `weights.length + 1` gives exit 2 with `configuration invalid: fixtures.fixtureIdPatterns[n]: {problem}`. A match is reported with the pattern name. Removing a form, or changing a weight, an exempt domain or a reserved TLD, changes the next run with no code change (ASM-TE011-08..10; CLAR-003); UT-TE011-32 and UT-TE011-33 pin the bare-`66` and reserved-TLD changes.
- `fixtures.fixtureObjects` maps a path glob to a dictionary object for JSON fixtures (empty by default).
- `source.maskingHelpers` is empty in production until the common module publishes its interface (OPEN-024).
- `source.entitySuffixes` defaults to `Entity`, `View`.
- `changedFiles.targetBranch` and `changedFiles.protectedBranches` drive the list decision of SPEC-TE011-013.

## 4. `P/pdpa-allow.yaml` (production content)

A YAML sequence of entries. Every entry has `rule` (one of the six), `path` (glob from the repository root), exactly one of `line` (positive integer) or `pattern` (regular expression matched against the source line), `owner` (non-empty), `reason` (non-empty) and `expires` (`YYYY-MM-DD`, inclusive in Asia/Bangkok). An invalid entry gives exit 2 with its 1-based index. An entry whose `path` glob would match a file in the recovery migration folder gives exit 2; the check uses the folder's two probe paths so it holds while the folder has no `.sql` file. UT-TE011-35 tests an exact path with a temporary migration file present and a broad `**/*.sql` against the empty-folder probes.

Production content (no finding is excused at this merge):

```yaml
# tools/pdpa-lint/pdpa-allow.yaml
# Story: RWB-TE-011. The list is empty: no finding is excused at this merge.
# An entry whose path matches the recovery migration folder is invalid (SPEC-TE011-011).
[]
```

## 5. Output contract, exit codes and value-level rules

### 5.1 Lines

One line per unexcused finding, sorted by file, line, rule, field:

```text
{rule}: {file}:{line} uses personal field {field}. Remove it or use the masking helper.
```

`{file}` is repository-relative with `/` separators. `{field}` is the dictionary field name; when the matched token differs, the token follows in parentheses, for example `last_name (lastName)`. For a SQL form the field may be `(columns not named)`, `(statement not recognised)` or `(DML in procedural body)`.

An expired entry that matches a finding adds, after all finding lines of that run:

```text
allow entry expired: {rule} {path} since {date}
```

The four notice kinds, after the findings and sorted the same way:

```text
PDPA-NOTICE: {field_id} unmarked at {file}:{line}
PDPA-NOTICE: {file}:{line} object not resolved for {field}; add a fixtureObjects entry or a typed receiver
PDPA-NOTICE: {file}:{line} seeds {field}, marked personal by a later migration
PDPA-NOTICE: {file}:{line} {rule} {field} corrected by {corrective file}
```

Four counts, in this order:

```text
PDPA-COUNT: unmarked {n}
PDPA-COUNT: unresolved {n}
PDPA-COUNT: later mark {n}
PDPA-COUNT: corrected {n}
```

Scope lines, after the counts, in this order:

```text
PDPA-SCOPE: exclusion {config key} {glob} excludes {n} files
PDPA-SCOPE: lint fixtures {config key} {glob} holds {n} files
PDPA-SCOPE: class {class} {n} files
PDPA-SCOPE: changed-file list against {target}: {n} files
PDPA-SCOPE: changed-file list not built: target {target}, branch {name}
```

Class counts appear for `production`, `seeds`, `tests`, `infra`, `tool` and `lint-fixtures`, in that order. No line contains a value, a source line or SQL text.

### 5.2 Exit codes and error lines (one line, nothing else printed)

| Code | Meaning | Lines |
|---|---|---|
| 0 | No unexcused finding; notices allowed | the normal report |
| 1 | At least one unexcused finding | the normal report |
| 2 | Configuration or input error | exactly one of the lines below |

```text
configuration not readable: {file}
configuration invalid: {config key}: {problem}
configuration error: unknown option {name}
dictionary source not readable: {file}
dictionary statement not supported: {file}:{line}
duplicate sys_fields field_id: {field_id} at {file}:{line}
unknown sys_fields field_id: {field_id} at {file}:{line}
dictionary is empty
api specification not readable: {file}
allow entry invalid: entries[{n}]: {problem}
allow entry on a migration: entries[{n}]
scan configuration excludes the migration folder: {config key}
lint-fixture root outside the test roots: {config key}
migration folder does not match rwb.flyway.location: {config key}
corrective migration names unknown file: {file}:2
changed-file list: target branch {name} not found
changed-file list: no merge base with {name}
changed-file list: branch not determined
source not parsable: {file}:{line}
```

The texts fixed by the spec are reproduced exactly (`dictionary statement not supported`, `scan configuration excludes the migration folder`, `lint-fixture root outside the test roots`, `migration folder does not match rwb.flyway.location`, `corrective migration names unknown file`, the three changed-file lines). The other lines are plan choices (PA-TE011-05, -07).

### 5.3 Check digit and patterns

The three patterns are the labelled defaults in `fixtures.fixtureIdPatterns` of §3, not code constants (CLAR-003; ASM-TE011-08..10; SPEC-TE011-009, -015). The matcher compiles each `forms` entry, then applies the optional `checksum` and domain exemptions.

- `thai_national_id`: accepted shapes are `(?<!\d)\d{13}(?!\d)` and `(?<!\d)\d-\d{4}-\d{5}-\d{2}-\d(?!\d)`. With the 13 digits `d1..d13`, `d13 = (11 - (sum over i = 1..12 of d_i * (14 - i)) mod 11) mod 10`; the `checksum` entry holds `digitCount: 13`, the twelve weights `13..2`, `modulus: 11`, `subtractFrom: 11` and `resultModulus: 10`. Not adjacent to another digit. An invalid check digit is not a finding. Removing the dashed form in configuration disables that shape (UT-TE011-31).
- `thai_mobile`: six configured forms — national `0[689]` + 8 digits, contiguous or grouped 3-3-4 with `-` or space; international `+66` + the same 9 digits, contiguous or grouped 2-3-4; and the bare `66` form of each, which cannot start after `+`. Not adjacent to another digit. Removing the two bare-`66` forms in configuration disables that shape while `+66` still matches (ASM-TE011-09; UT-TE011-32).
- `email`: the configured case-insensitive form matches a local part, `@` and a domain. A domain equal to, or a subdomain of, an `exemptDomains` entry is not a finding, and neither is one ending in an `exemptDomainSuffixes` entry (`.test`, `.example`, `.invalid`, `.localhost` by default). Changing the suffix list changes the next run (UT-TE011-33).
- The pattern name is the `{field}` printed for a FIXTURE-ID finding.

### 5.4 Corrective migration

- Line 1 of the original `O` and of the corrective `C` is `-- Story: <key>`. Line 2 of `C` starts `-- Fix:` and has a non-empty reason; every token matching `V[0-9]{4}__[A-Za-z0-9_]+\.sql` names a file, and each must exist in the folder (else exit 2 at `{file}:2`).
- `C` accepts a finding in `O` only when (a) `C`'s sequence is greater, (b) the line-1 story keys are equal, (c) line 2 names `O`, (d) `C` writes the finding's target table (and, for a `DEFAULT` on a literal column, changes that column's default), and (e) `O` is not on the changed-file list, where that list is built.
- Target tables are those of SPEC-TE011-018 (d). A placeholder column needs the table write alone; a placeholder table is never accepted. A finding with no target table needs no write and still needs (a), (b), (c) and (e).
- The rules apply only to files in the recovery migration folder. A `-- Fix:` line elsewhere is not parsed.

## 6. Tool Gradle build and the CI job

### 6.1 `P/settings.gradle.kts`

```kotlin
rootProject.name = "pdpa-lint"
```

### 6.2 `P/build.gradle.kts` (shape)

```kotlin
plugins {
    java
    application
    jacoco
}

group = "th.co.scb.ace.tools"
version = "0.1.0"

java {
    toolchain { languageVersion = JavaLanguageVersion.of(21) }
}

repositories { mavenCentral() }

val junitVersion = "6.0.3"
val assertjVersion = "3.27.7"
val snakeYamlVersion = "2.6"
val jacksonVersion = "3.1.7"

dependencies {
    implementation("org.yaml:snakeyaml:$snakeYamlVersion")
    implementation("tools.jackson.core:jackson-core:$jacksonVersion")
    testImplementation("org.junit.jupiter:junit-jupiter:$junitVersion")
    testImplementation("org.assertj:assertj-core:$assertjVersion")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher:$junitVersion")
}

val repositoryRoot = layout.projectDirectory.dir("../..").asFile

application { mainClass = "th.co.scb.ace.tools.pdpa.PdpaLint" }

tasks.test {
    useJUnitPlatform()
    workingDir = repositoryRoot
    finalizedBy(tasks.jacocoTestReport)
}

tasks.jacocoTestReport {
    executionData(tasks.test.get())
    reports {
        xml.required = true
        html.required = true
    }
}

tasks.jacocoTestCoverageVerification {
    executionData(tasks.test.get())
    violationRules {
        rule {
            limit { counter = "LINE"; minimum = "0.80".toBigDecimal() }
            limit { counter = "BRANCH"; minimum = "0.80".toBigDecimal() }
            limit { counter = "METHOD"; minimum = "0.80".toBigDecimal() }
            limit { counter = "INSTRUCTION"; minimum = "0.80".toBigDecimal() }
        }
    }
}

tasks.check { dependsOn(tasks.jacocoTestCoverageVerification) }

val pdpaLint by tasks.registering(JavaExec::class) {
    group = "verification"
    description = "Runs the PDPA lint over the repository."
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass = "th.co.scb.ace.tools.pdpa.PdpaLint"
    workingDir = repositoryRoot
    shouldRunAfter(tasks.check)
    val changedFrom = providers.gradleProperty("pdpaLint.changedFrom").orNull
    val branch = providers.gradleProperty("pdpaLint.branch").orNull
    if (changedFrom != null) {
        args("--changed-files-from-git", changedFrom, "--branch", branch ?: "")
    }
}
```

`application` is used for the main class and the install distribution; the build never calls `git` itself.

The four limits are one rule with no `element = "CLASS"`, so JaCoCo applies them to the tool bundle (all `P/src/main` classes together), not to each class. TASK-32 records the aggregate counters and also reviews every class; any class below 0.80 gets another test. No production class is excluded and no limit is lowered (PLAN-005 fix).

### 6.3 `.gitlab-ci.yml` job (added after `frontend-check`; existing jobs unchanged)

```yaml
pdpa-lint:
  stage: verify
  image: eclipse-temurin:21-jdk
  variables:
    GIT_DEPTH: "0"
    PDPA_LINT_TARGET_BRANCH: develop-recovery
  cache: { key: gradle, paths: [.gradle-home/] }
  before_script:
    - command -v git >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq --no-install-recommends git)
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH
    - if: $CI_COMMIT_TAG
  script:
    - set -o pipefail
    - |
      if [ -n "$CI_COMMIT_TAG" ]; then
        ./backend/gradlew --no-daemon -p tools/pdpa-lint clean check pdpaLint 2>&1 | tee tools/pdpa-lint/build/pdpa-lint-console.log
      else
        TARGET="${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-$PDPA_LINT_TARGET_BRANCH}"
        BRANCH="${CI_MERGE_REQUEST_SOURCE_BRANCH_NAME:-$CI_COMMIT_BRANCH}"
        git update-ref -d "refs/remotes/origin/$TARGET" || true
        git fetch --no-tags origin "+refs/heads/$TARGET:refs/remotes/origin/$TARGET" || true
        ./backend/gradlew --no-daemon -p tools/pdpa-lint clean check pdpaLint \
          "-PpdpaLint.changedFrom=origin/$TARGET" "-PpdpaLint.branch=$BRANCH" \
          2>&1 | tee tools/pdpa-lint/build/pdpa-lint-console.log
      fi
  artifacts:
    when: always
    paths:
      - tools/pdpa-lint/build/pdpa-rules.yaml
      - tools/pdpa-lint/build/pdpa-lint-console.log
      - tools/pdpa-lint/build/reports/
    reports: { junit: tools/pdpa-lint/build/test-results/test/*.xml }
```

The job is in every branch, tag and merge request pipeline the file creates. It has no `needs:` and no `workflow:` change. A failed fetch leaves the target unresolved, so the tool fails closed where the list is built instead of reading a stale ref.

## 7. Test fixture trees (`X/trees/`)

`LintHarness` copies one tree into `@TempDir`, copies the real `api/recovery-api-v4.yaml` beside it, writes `tools/pdpa-lint/pdpa-lint.yaml` by loading the real production file and replacing only `dictionary`, `api`, `allowList`, `fixtures` and `changedFiles`, writes the default synthetic dictionary unless the tree supplies `dictionary/baseline.sql`, and runs the step. `X` is `tools/pdpa-lint/src/test/resources`; each row lists the files relative to `X/trees/<tree>/`.

| Tree | Files | Used by |
|---|---|---|
| `tc01-log-field-java` | `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/SampleService.java` | ST-TE011-01 |
| `tc02-log-entity` | `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/SampleEntityLog.java` | ST-TE011-02 |
| `tc03-fixture-id` | `backend/src/test/resources/fixtures/case.json` (a `SYN-` placeholder under `idNoMasked`; rewritten at run time) | ST-TE011-03 |
| `tc04-fixture-field` | `backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_099_seed.sql`, `dictionary/baseline.sql` | ST-TE011-04 |
| `tc05-dictionary-r2` | `dictionary/baseline.sql`, `backend/src/main/resources/db/modulemigration/recovery/V0002__rwb_e1_099_mark.sql`, `backend/src/main/java/th/co/scb/ace/demo/recovery/access/internal/SampleAccount.java` | ST-TE011-05 |
| `tc05-dictionary-r1` | the same files, with the marking row as a multi-row `INSERT` | ST-TE011-05 |
| `tc06-allow` | `backend/src/test/resources/fixtures/legacy-seed.sql`, `pdpa-allow.yaml` (entry expiring 2026-11-30) | ST-TE011-06 |
| `tc07-log-field-ts` | `frontend/src/modules/recovery/caserecord/CaseRecord.tsx` | ST-TE011-07 |
| `tc08-masking` | `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/MaskedLog.java`; the test sets `maskingHelpers` | ST-TE011-08 |
| `tc09-exception` | `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/SampleThrow.java` | ST-TE011-09 |
| `tc10-tostring` | `backend/src/main/java/th/co/scb/ace/demo/recovery/dochub/api/ContactEntity.java`, `ContactRecord.java` | ST-TE011-10 |
| `ts01-seed-tables` | `backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_099_baseline.sql`; the test copies the real Physical Schema v6 and API v4 as inputs | ST-TE011-11 |
| `ts02-point-in-time` | two migrations `V0001__rwb_e1_099_a.sql`, `V0002__rwb_e1_099_b.sql`, `backend/src/test/resources/fixtures/point-in-time.sql` | ST-TE011-12 |
| `ts03-source-field` | `dictionary/baseline.sql` (row `v_ace_customer.last_name` with source `public.customer.surname`), `backend/src/test/resources/fixtures/legacy-customer.sql` | ST-TE011-13 |
| `ts04-unresolved` | `dictionary/baseline.sql` (adds a non-personal `summary` row and `recovery_case.status`), `dictionary/union.sql` (adds `address.address`), `backend/src/test/resources/fixtures/it-customer.sql`, `backend/src/test/resources/fixtures/address.sql`, `frontend/src/modules/recovery/__tests__/requestFixture.ts` | ST-TE011-14 |
| `ts05-columns-not-named` | `backend/src/test/resources/fixtures/columns-not-named.sql`, `backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_099_copy.sql` | ST-TE011-15 |
| `ts06-corrective` | `backend/src/main/resources/db/modulemigration/recovery/V0003__rwb_e1_042_seed.sql` (line 1 `-- Story: RWB-E1-042`); the test writes each `C` variant at run time | ST-TE011-16 |
| `ts07-sql-classes` | `dictionary/baseline.sql`, `backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_099_classes.sql`, `backend/src/test/resources/fixtures/sql/class1.sql`, `class2.sql`, `class3-do.sql`, `class3-function.sql`, `class4.sql`, `columns-not-named.sql`, `defaults.sql`, `execute-format.sql` | ST-TE011-17 |
| `ts08-lint-fixtures` | `backend/src/test/resources/migration-lint/t22-n11/V0001__rwb_e1_044_ok.sql`, `t22-n12/V0001__rwb_e1_044_ok.sql`, `t22-n13/V0001__rwb_e1_044_ok.sql`, `t20-searchpath-fail/V0001__rwb_e1_044_ok.sql`, `t21-source-field/V0001__rwb_e1_044_ok.sql`, `t03-fix-unknown/V0002__rwb_e1_044_fix.sql`, `backend/src/test/resources/other-sql/t22-n11/V0001__rwb_e1_044_ok.sql` | ST-TE011-18 |
| `ts09-git` | none committed; `TestRepository` builds the repository | ST-TE011-19 |

Every file under a tree is small and synthetic. Table names are `case_note`, `team_assignment`, `listing`, `it_customer`, `address`; column names are `description`, `owner_role`, `status`, `first_name`, `surname`. No tree stores a value that matches a FIXTURE-ID pattern.

## 8. `scripts/dev.ps1` (changed block)

`pdpa-lint` joins `ValidateSet`. A new helper and the two switch changes:

```powershell
function Invoke-PdpaLint {
  param([switch]$WithToolTests)
  $branch = (Invoke-Native { & git -C $Root rev-parse --abbrev-ref HEAD 2>$null } | Select-Object -First 1)
  if (-not $branch) { throw "pdpa lint: current branch not determined" }
  $branch = "$branch".Trim()
  $tasks = if ($WithToolTests) { @("check", "pdpaLint") } else { @("pdpaLint") }
  Invoke-Native {
    & (Join-Path $Root "backend\gradlew.bat") -p (Join-Path $Root "tools\pdpa-lint") @tasks "-PpdpaLint.changedFrom=develop-recovery" "-PpdpaLint.branch=$branch" 2>&1 | ForEach-Object { "$_" }
  }
  if ($LASTEXITCODE -ne 0) { throw "pdpa lint failed" }
}

"test" {
  Invoke-Gradle @("test")
  Invoke-PdpaLint -WithToolTests
  Invoke-Npm @("run", "check")
}
"pdpa-lint" { Invoke-PdpaLint }
```

`ValidateSet` gains `"pdpa-lint"`; the synopsis gains its example line. No other command changes. `git` runs from `$Root`; a detached checkout returns `HEAD`, which the tool rejects with `changed-file list: branch not determined` (exit 2).

## 9. `.gitlab/CODEOWNERS` (one line added)

In section `[Recovery module]`, in the same change as `P`:

```text
/tools/pdpa-lint/ @scb-ace/techx-recovery-tech-leads
```

The line is anchored and has no wildcard (TE-002 validator V4), the handle is in `.gitlab/codeowners-register.yaml` (V7), and the pattern matches the tool's files (V9). Nothing else in the file changes.

## 10. Test data rules

- The default synthetic dictionary (written by `LintHarness`) marks `first_name`, `last_name`, `cif_no`, `id_no_masked`, `date_of_birth`, `contact_value`, `summary`, `field_value`, `id_no_last4` and `contact_value_masked` on objects `v_ace_customer`, `v_ace_contact`, `interaction`, `document_field` and `recovery_case`, and adds `recovery_case.status` personal and `listing.status` non-personal for the ambiguity cases.
- Failing FIXTURE-ID values are generated by `TestValues` with a fixed seed at run time; none is stored in a tree, a source file or an evidence file.
- No real name, address, account number, identifier, credential or production value appears anywhere in the tool, its tests, its fixtures or its output.
