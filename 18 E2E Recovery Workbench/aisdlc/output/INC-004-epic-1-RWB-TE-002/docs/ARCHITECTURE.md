---
title: "RWB-TE-002 Code owners for the recovery module — architecture"
run_id: "INC-004-epic-1-RWB-TE-002"
story: "RWB-TE-002"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED — code gate PENDING_ORCHESTRATOR; no approval recorded (D-RUN-09)"
---

# Architecture — RWB-TE-002

All paths are from the repository root at `feature/RWB-TE-002-code-owners` @ `d018cf7` (first written at `ae61b08`; review remediation D-RUN-25 and code gate round 1 since). The Java
package is `th.co.scb.ace.demo.recovery.architecture.codeowners` in the **test** source set
(`backend/src/test/java/...`); it is build tooling, not application code, and no main-source class
changes. Pattern follows the inherited `RecoveryMigrationLintTest` (spec "Inherited Existing
Behavior").

## 1. Components

**DOC ID:** DOC-RWB-TE-002-005 · **Maps to:** SPEC-RWB-TE-002-001, -007, -008, -009; TASK-04; CODE-TE002-01..04

| CODE | Class | Role | SPEC |
|---|---|---|---|
| CODE-TE002-01 | `CodeOwnersFile` (records `Entry`, `Section`, `Problem`) | Parses `.gitlab/CODEOWNERS` (`parse(Path)`, `parse(List<String>)`) into sections and entries with line numbers; a missing file fails closed | 001, 007, 008 |
| CODE-TE002-02 | `OwnerRegister` (records `Owner`, `ReservedPattern`) | Reads `.gitlab/codeowners-register.yaml` with SnakeYAML (already on the test classpath; no new dependency); reports V11 problems | 009 |
| CODE-TE002-03 | `CodeOwnersValidator` (records `Finding`, enum `Level`) | Runs V1–V12 over file, register and working tree; collects every finding; fails on any `ERROR` | 008 |
| CODE-TE002-04 | `OwnershipResolver` | Pure function: parsed file + changed paths → required sections and owners | 007 |

Data flow: `CODEOWNERS` + register + working tree → parser/reader → validator findings (test
assertion) ; `CODEOWNERS` + changed paths → resolver → `{section → owners}` (test assertion). Nothing
reads a database, a network or a token.

## 2. Validation rules

**DOC ID:** DOC-RWB-TE-002-006 · **Maps to:** SPEC-RWB-TE-002-001, -004, -008, -009; AC7, X6; BR4, BR5, BR7; CODE-TE002-01..03; UT-01..UT-12, UT-23

| Rule | Check | Level | Message | Test |
|---|---|---|---|---|
| V1 | Line is a header `[Name]` or an entry | ERROR | `line {n}: syntax error` | UT-01 (`malformedLineIsASyntaxError`, `missingFileFailsClosed`) |
| V2 | Entry inside a section | ERROR | `line {n}: entry outside a section` | UT-02 |
| V3 | Entry has an owner | ERROR | `line {n}: pattern {p} has no owner` | UT-03 |
| V4 | Pattern anchored, no `* ? [ ! \`, no `.`, `..` or empty (`//`) path segment and no `:` (ponytail Nice 2, security F7, code gate CODE1-001) | ERROR | `line {n}: unsupported pattern {p}` | UT-04, `dotSegmentPatternsAreRejected`, `emptySegmentAndColonPatternsAreRejected` |
| V5 | No duplicate pattern in a section block (DEV-05) | ERROR | `line {n}: duplicate pattern {p} in section {s}` | UT-05 |
| V6 | No pattern shadowed by a later directory pattern (BR5) | ERROR | `line {n}: pattern {p} is shadowed by later pattern {q} in section {s}` | UT-06 |
| V7 | Owner listed in the register (AC7); skipped only when the register already has a V11 problem, so `owners: []` fails closed (ponytail Must 1, F6) | ERROR | `line {n}: owner {team} not found` | UT-07, `emptyOwnerListStillChecksEveryOwner` |
| V8 | Owner is a group `@name/name` (story §17) | ERROR | `line {n}: owner {o} is not a team` | UT-08 |
| V9 | Non-reserved pattern matches a file under the repository root (target normalised; outside the root counts as no match, CODE1-001) | ERROR | `line {n}: pattern {p} matches no file` | UT-09, `patternResolvingOutsideTheRootMatchesNoFile` |
| V10 | Reserved pattern matches no file | WARNING | `line {n}: reserved pattern {p} matches no file ({basis})` | UT-10 |
| V11 | Register well-formed | ERROR | `register: {problem}` | UT-11, `registerProblemsFailClosed` (X8 texts) |
| V12 | Section names unique, trimmed, case-insensitive | ERROR | `line {n}: duplicate section {s}` | UT-23 |
| — | `PLACEHOLDER` / `ASSUMED` owner | WARNING / INFO | `owner {o} is a placeholder for {role} ({openItem})` / `owner {o} is assumed ({openItem})` | UT-12 |

UT-12 (`liveFileAndRegisterPass`) runs all rules on the live file: no `ERROR`; warnings for the
reserved common pattern, the reserved `/CODEOWNERS` and `/docs/CODEOWNERS` (each in two sections) and the two placeholders.
`noHigherPrecedenceCodeOwnersFileExists` fails if either `/CODEOWNERS` or `/docs/CODEOWNERS` exists (security F1). V9 uses the working tree (in CI: tracked files).
The host check "owner exists and has write access" is not built here: it needs a host API and token
(HC-08, HV-07); when built in ACE it must fail closed without its token (ASM-TE002-06).

## 3. Resolver semantics

**DOC ID:** DOC-RWB-TE-002-007 · **Maps to:** SPEC-RWB-TE-002-002, -003, -004, -005, -007, -017; AC1 cl.1, AC2, AC3, AC4; BR1–BR5; CODE-TE002-04; UT-13..UT-20, UT-25, UT-26

- A directory pattern (trailing `/`) matches a path that starts with it (leading `/` removed); a file
  pattern matches the equal path. A `.\`-prefixed or backslash path is normalised first (PA-13;
  UT-20 extra assertion, DEV-06).
- Per section, the **last** matching entry decides (BR5, UT-19). Each returned section needs one
  approval from one of its owners; a path in several sections needs each section (ASM-TE002-11).
- A path with no match returns no section (`README.md`, UT-20). Same input twice → same result
  (story §12 idempotency, UT-20).
- UT-26 walks the live tree: every file under `backend/src/test/java/` recovery folders and under
  `backend/src/test/resources/architecture/` must resolve to `[Recovery module]` →
  `@scb-ace/techx-recovery-tech-leads`. Its failure message lists every unowned path (DEV-04). After
  RWB-E1-042 was merged in (`a3af237`) it listed `backend/src/test/resources/architecture/magic-number-baseline.csv`;
  the D-RUN-25 addendum line A1 (`../implement/plan-addendum.md`) fixed it at `c740d25`.
  `addendumPathsHaveOwners` checks the other addendum paths (F1, F2, F4).

## 4. Build and CI wiring

**DOC ID:** DOC-RWB-TE-002-008 · **Maps to:** SPEC-RWB-TE-002-013, -014; Flow 2, Flow 6; TASK-07, TASK-08; CODE-TE002-08; UT-24; DEV-07

`backend/build.gradle.kts` (appended block, no dependency line changed — DEV-03):

| Task | Definition |
|---|---|
| `codeOwnersTest` | `Test`; test source set classes and runtime classpath; `includeTags("codeowners")`; inputs = the six governance files (`.gitlab/CODEOWNERS`, register, host settings, MR template, `AGENTS.md`, `.gitlab-ci.yml`); `outputs.upToDateWhen { false }` (ponytail Nice 3: UT-26 and V9 read the whole tree; guard test `codeOwnersTestIsNeverUpToDate`); finalized by the report |
| `test` | gains the same six input files, so a CODEOWNERS-only edit re-runs `test` (`../implement/backend/task07-verification.txt`) |
| `codeOwnersCoverageReport` | JaCoCo, `executionData(codeOwnersTest)`, classes `.../codeowners/**` minus `*Test`; XML to `build/reports/jacoco/codeOwnersCoverageReport.xml`, plus HTML |
| `codeOwnersCoverageVerification` | Same scope; minimum 0.80 LINE, BRANCH, INSTRUCTION, METHOD |

The codeowners classes are measured only by these tasks; `recoveryCoverage*` is unchanged.
`check --dry-run` lists no codeowners task (the tag tests already run inside `test`).

`.gitlab-ci.yml` job `codeowners-validation`: `stage: verify`, image `eclipse-temurin:21-jdk`, own cache key `gradle-codeowners` (security F8), script
`cd backend && ./gradlew --no-daemon codeOwnersTest codeOwnersCoverageVerification`, JUnit report
`backend/build/test-results/codeOwnersTest/*.xml`, artifact path
`backend/build/reports/jacoco/codeOwnersCoverageReport/`, no `rules:` key (runs on every pipeline).
UT-24 checks this **definition**; the job has never run (no GitLab runner; HV-07). DEV-07: the XML
report is written outside the artifact folder, so the artifact keeps the HTML only (follow-up
IM-SU-02).

## 5. Governance files

**DOC ID:** DOC-RWB-TE-002-009 · **Maps to:** SPEC-RWB-TE-002-005, -009, -015, -016; A-05, A-10; TASK-05, TASK-06; CODE-TE002-06, -07; UT-18, UT-21, UT-22

| File | Content | Test |
|---|---|---|
| `.gitlab/codeowners-register.yaml` | 4 owners (`handle`, `role`, `source`, `status`, `openItem`): two `ASSUMED` team handles, two `PLACEHOLDER` role handles, all `OPEN-038`; three reserved patterns (common root, OPEN-024; `/CODEOWNERS` and `/docs/CODEOWNERS`, security F1, D-RUN-25). No person, membership or e-mail | UT-07, UT-11, UT-12 |
| `.gitlab/host-settings.md` | HC-01..HC-08, status `OPEN — NOT_APPLIED_HERE` | — (HV items) |
| `.gitlab/merge_request_templates/Default.md` | Headings in order: Story key, Plan file, Acceptance criteria covered, Coding tool used, AI first-pass review summary, Reviewer, Test results, AISDLC trailers; names no person | UT-21 |
| `AGENTS.md` §5 | Five context paths now `aisdlc/.github/contexts/...`; coding-standard cell names `backend-standards.md` / `frontend-standards.md`; no other text changed | UT-22 |

The three control files sit in two sections with distinct names (BR4, V12), so a change needs both
teams (UT-18; host effect HV-08).
