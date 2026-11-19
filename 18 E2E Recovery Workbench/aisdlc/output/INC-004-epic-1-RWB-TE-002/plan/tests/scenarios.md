---
title: "Test scenarios: RWB-TE-002 Code owners for the recovery module"
run_id: "INC-004-epic-1-RWB-TE-002"
story: "RWB-TE-002"
revision: "v1 (18 Nov 2026): first test scenario map for this repository, written by the continuation of the interrupted plan run; source `plan.md` v2 and the spec test list UT-01..UT-26."
---

# Test scenarios: RWB-TE-002

Every acceptance criterion, business rule, exception path, SPEC requirement and story test case maps to a named test below, or to an open human-verification item where only the ACE host can show the result. Test path: `C` = `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners`. All tests are JUnit 5, tag `codeowners`, in the `test` source set, so `gradlew test` runs them inside `./scripts/dev.ps1 test`. On the host they also run in `codeowners-validation`. "Fixture" means a file or tree written to `@TempDir`; "live" means the repository file or working tree. No test is skipped, disabled or weakened.

## 1. Acceptance criteria (story file v7 RWB-TE-002 v1 §7)

| AC | Test ID(s) | Named test or HV item | Expected | Task |
|---|---|---|---|---|
| AC1 clause 1 | UT-13 | `OwnershipResolverTest.recoveryMainPathNeedsRecoveryTeam` | A recovery main path returns `[Recovery module]` with `@scb-ace/techx-recovery-tech-leads` only | TASK-02, TASK-04, TASK-05 |
| AC1 clause 2 | HV-01 | Host MR with an outside-squad approval | Merge stays blocked; host shows code-owner review required. `OPEN — NOT_TESTED_HERE` | TASK-11 |
| AC2 | UT-16; HV-02 | `OwnershipResolverTest.commonModulePathNeedsAceTeam` | A common module path returns `[Common module]` with `@scb-ace/ace-team`; the host shows the same reviewer | TASK-02, TASK-04, TASK-05; TASK-11 |
| AC3 required part | UT-17 | `OwnershipResolverTest.bothModulesNeedBothTeams` | Recovery and common paths together return both sections | TASK-02, TASK-04, TASK-05 |
| AC3 blocked part | HV-03 | Host MR across both modules, recovery owner approves | Blocked until an ACE-team member also approves. `OPEN — NOT_TESTED_HERE` | TASK-11 |
| AC4 | UT-15; HV-02 | `OwnershipResolverTest.frontendMigrationAndMapPathsNeedRecoveryTeam` | Front-end, migration and module map paths all return `[Recovery module]`; the host lists the same owner | TASK-02, TASK-04, TASK-05; TASK-11 |
| AC5 | HV-04 | Host MR where the author approves their own change | Approval not counted; a second team member is needed. `OPEN — NOT_TESTED_HERE` | TASK-11 |
| AC6 | HV-05 | Host MR with a new commit after approval | Approvals removed; review required again. `OPEN — NOT_TESTED_HERE` | TASK-11 |
| AC7 local part | UT-07 | `CodeOwnersValidationTest.ownerNotInTheRegisterIsRejected` | `line {n}: owner @scb-ace/recovery-leads-typo not found`; validation fails | TASK-01, TASK-04 |
| AC7 host part | HV-07 | Host pipeline with the typo handle, and owner existence plus write access | The job fails and the merge is blocked; every owner exists with write access. `OPEN — NOT_TESTED_HERE` | TASK-11 |
| X1 | HV-01 | Host MR with only a non-owner approval | Merge stays blocked. `OPEN — NOT_TESTED_HERE` | TASK-11 |
| X2 | UT-16; HV-02 | As AC2 | ACE team section required; host shows it | TASK-02, TASK-04, TASK-05; TASK-11 |
| X3 | UT-17; HV-03 | As AC3 | Both sections; host blocks until both approve | TASK-02, TASK-04, TASK-05; TASK-11 |
| X4 | HV-04 | As AC5 | The author's approval does not count | TASK-11 |
| X5 | HV-05 | As AC6 | New commit dismisses approvals | TASK-11 |
| X6 | UT-07; HV-07 | As AC7 | Exact build text locally; the host job fails | TASK-01, TASK-04; TASK-11 |
| X7 | HV-06 | Host MR where a non-owner squad member approves | Merge refused; no MSG-P4-002 is shown. `OPEN — NOT_TESTED_HERE` | TASK-11 |

## 2. Business rules (story file v7 RWB-TE-002 v1 §8)

| BR | Tests |
|---|---|
| BR1 Recovery back end, test and migration folders | UT-13, UT-14, UT-26 |
| BR2 Recovery front end folder and module map | UT-15, UT-26 |
| BR3 Common module folder | UT-10 (reserved warning), UT-16 |
| BR4 Code owners file owned by both teams | UT-18, UT-23 |
| BR5 Last matching pattern decides | UT-06 (shadowing), UT-19 |
| BR6 Host merge rules | HV-01, HV-03, HV-04, HV-05 (host only; not claimed locally) |
| BR7 Team names are file values | UT-18, UT-23 |

## 3. Spec test list (UT-01..UT-26)

| ID | Covers | Named test (class.method) | Data | Expected | Task |
|---|---|---|---|---|---|
| UT-01 | V1, X9 | `CodeOwnersValidationTest.malformedLineIsASyntaxError`; `CodeOwnersValidationTest.missingFileFailsClosed` | Fixture with `[A] @x` and a missing file; valid register | `line {n}: syntax error` on that line; the missing file returns `.gitlab/CODEOWNERS not found` and fails | TASK-01, TASK-04 |
| UT-02 | V2 | `CodeOwnersValidationTest.entryOutsideASectionIsRejected` | Fixture entry before any header | `line {n}: entry outside a section` | TASK-01, TASK-04 |
| UT-03 | V3 | `CodeOwnersValidationTest.patternWithoutOwnerIsRejected` | Fixture `/x/` with no owner | `line {n}: pattern /x/ has no owner` | TASK-01, TASK-04 |
| UT-04 | V4 | `CodeOwnersValidationTest.unsupportedPatternsAreRejected` | Fixture `x/`, `/x/*.java`, `/x/**/y/` | `unsupported pattern` for each | TASK-01, TASK-04 |
| UT-05 | V5 | `CodeOwnersValidationTest.duplicatePatternInOneSectionIsRejected` | Fixture `/x/` twice in one section; `/x/` in two sections; a file under `x/` | Error for the first case only; the second case has no V5 finding | TASK-01, TASK-04 |
| UT-06 | V6, BR5 | `CodeOwnersValidationTest.shadowedPatternIsRejected` | Fixture `/a/b/` then `/a/`; and `/a/` then `/a/b/`; files under `a/b/` | Shadowed error in the first order only; no V6 in the second | TASK-01, TASK-04 |
| UT-07 | V7, AC7, X6 | `CodeOwnersValidationTest.ownerNotInTheRegisterIsRejected` | Fixture recovery path owned by `@scb-ace/recovery-leads-typo`; register without it | `line {n}: owner @scb-ace/recovery-leads-typo not found`; validation fails | TASK-01, TASK-04 |
| UT-08 | V8, §17 | `CodeOwnersValidationTest.ownerThatIsNotATeamIsRejected` | Fixture owners `@someone`, `someone@example.test` | `is not a team` for each | TASK-01, TASK-04 |
| UT-09 | V9 | `CodeOwnersValidationTest.patternThatMatchesNoFileIsRejected` | Fixture pattern to a missing folder; pattern to an empty folder | `matches no file` for each | TASK-01, TASK-04 |
| UT-10 | V10, BR3 | `CodeOwnersValidationTest.reservedPatternThatMatchesNoFileIsAWarning` | Fixture reserved pattern with no file; valid other pattern | Warning only; validation passes | TASK-01, TASK-04 |
| UT-11 | V11, placeholders | `CodeOwnersValidationTest.malformedRegisterIsRejected` | Register missing a field; bad status; duplicate handle; a `PLACEHOLDER` owner | `register: ...` errors for the first three; a placeholder warning | TASK-01, TASK-04 |
| UT-12 | All rules, flow 1 | `CodeOwnersValidationTest.liveFileAndRegisterPass` | Live `.gitlab/CODEOWNERS` with the substitution and the live register, after P1 | No `ERROR`; warnings list the reserved common pattern and the two placeholders | TASK-02, TASK-04, TASK-05, TASK-06 |
| UT-13 | AC1 clause 1, BR1 | `OwnershipResolverTest.recoveryMainPathNeedsRecoveryTeam` | Live file; `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/AllocationService.java` | `[Recovery module]` to `@scb-ace/techx-recovery-tech-leads` only | TASK-02, TASK-04, TASK-05 |
| UT-14 | BR1 | `OwnershipResolverTest.recoveryTestE2eMigrationAndModulePathsNeedRecoveryTeam` | Live file; one path each in recovery test, e2e test and migration; TE-001 module paths `dochub/storage/BlobDocumentStore.java`, `casewf/workflow/internal/TemporalConfig.java`, `casewf/migration/RecoveryFlywayConfig.java` and `casewf/rules/DroolsRuleEngineTest.java` | `[Recovery module]` to the recovery team for each, and no other section | TASK-02, TASK-04, TASK-05 |
| UT-15 | AC4, BR2 | `OwnershipResolverTest.frontendMigrationAndMapPathsNeedRecoveryTeam` | Live file; `frontend/src/modules/recovery/caselist/CaseListPage.tsx`, `backend/src/main/resources/db/modulemigration/recovery/V9999__rwb_te_002_resolver_fixture.sql`, `backend/src/test/resources/architecture/recovery-modules.yaml` | `[Recovery module]` for all three; the migration string is never written to disk | TASK-02, TASK-04, TASK-05 |
| UT-16 | AC2, BR3, X2 | `OwnershipResolverTest.commonModulePathNeedsAceTeam` | Live file; `backend/src/main/java/th/co/scb/ace/demo/common/ExampleService.java` | `[Common module]` to `@scb-ace/ace-team` | TASK-02, TASK-04, TASK-05 |
| UT-17 | AC3, X3 | `OwnershipResolverTest.bothModulesNeedBothTeams` | Live file; the paths of UT-13 and UT-16 together | Both sections required | TASK-02, TASK-04, TASK-05 |
| UT-18 | BR4, BR7 | `OwnershipResolverTest.controlFilesNeedBothTeams` | Live file; `.gitlab/CODEOWNERS`, `.gitlab/codeowners-register.yaml`, `.gitlab/host-settings.md`, a validator class path | The three BR4 control files return both control sections (both teams); the validator class returns `[Recovery module]` and `[Code owners control ACE team]`, so both teams are present through the recovery test package and the ACE control section. Section names differ without regard to case; owner sets do not overlap. | TASK-02, TASK-04, TASK-05 |
| UT-19 | BR5 | `OwnershipResolverTest.specificPatternWinsWithinASection` | Fixture general then specific pattern, different owners | Specific owner wins for a path under it; general owner for a sibling | TASK-01, TASK-04 |
| UT-20 | §12 idempotency; unowned | `OwnershipResolverTest.resolverIsIdempotentAndLeavesUnownedPathsAlone` | Live file; same input twice; `README.md` | Equal results; `README.md` returns no section | TASK-02, TASK-04, TASK-05 |
| UT-21 | A-10, SPEC-015 | `MergeRequestTemplateTest.templateHasTheEightHeadingsInOrder` | Live `.gitlab/merge_request_templates/Default.md` | File exists; all eight headings present in order | TASK-03, TASK-06 |
| UT-22 | A-05, SPEC-016 | `AgentsContextPathsTest.everySectionFivePathExists` | Live `AGENTS.md` | Every back-quoted path in the §5 table exists from the repository root | TASK-03, TASK-06 |
| UT-23 | V12, BR4, BR7, SG-013 | `CodeOwnersValidationTest.duplicateSectionNameIsRejected` | Fixture A `[Code owners control]` then `[code owners CONTROL]`, each valid; fixture B `[Recovery module]` and `[Recovery module ]`; fixture C two distinct names | A `line {n}: duplicate section code owners CONTROL` and fails; B one duplicate error; C no V12 finding | TASK-01, TASK-04 |
| UT-24 | SPEC-013 job definition, flow 2 | `PipelineDefinitionTest.validationJobIsDefinedAsSpecified` | Live `.gitlab-ci.yml` parsed with SnakeYAML | Job `codeowners-validation` exists; `stage: verify`; script `./gradlew --no-daemon codeOwnersTest codeOwnersCoverageVerification` from `backend`; JUnit report `backend/build/test-results/codeOwnersTest/*.xml`; no `rules:` key | TASK-03, TASK-07 |
| UT-25 | SPEC-017, SG-014 | `OwnershipResolverTest.pipelineGateFilesNeedThePipelineRole` | Live file; `backend/build.gradle.kts`, `backend/settings.gradle.kts`, `backend/gradle/wrapper/gradle-wrapper.properties`, `frontend/package.json`, `frontend/vite.config.ts`, `scripts/dev.ps1` | `[Pipeline gates]` to `@role-placeholder/techx-devops-with-scb-it` for each | TASK-02, TASK-04, TASK-05 |
| UT-26 | BR1, BR2, story §17, SPEC-002, -003 | `OwnershipResolverTest.everyRecoveryTestFileResolvesToTheRecoveryTeam` | Live file and working tree. (A) `RecoveryBoundaryTest.java`, `ModulithTest.java`, `recovery-modules.yaml`. (B) Every regular file under `backend/src/test/resources/architecture/` and under `backend/src/test/java/` except `th/co/scb/ace/demo/common/`. (C) `frontend/eslint.config.js` | (A) and (B) include `[Recovery module]` with the recovery team; codeowners package files also return `[Code owners control ACE team]`; (B) finds at least one file under `architecture/fixtures/` and the fixture-root pattern; (C) returns `[Recovery module]` and `[Pipeline gates]`; the live file contains no `{te001FixtureRoot}` token | TASK-02, TASK-04, TASK-05 |

## 4. Plan-level checks

| Check | Command or method | Expected | Task |
|---|---|---|---|
| Coverage gate | `cd backend; ./gradlew codeOwnersTest codeOwnersCoverageVerification` | Exit 0; LINE, BRANCH, INSTRUCTION and METHOD each at or above 0.80; native XML and HTML saved | TASK-08 |
| Guardrails and scope | `git diff --stat develop-recovery...HEAD`; PII and dependency scans; live validation | Only the plan files; no `common/` or `main/` file; no personal data; no dependency; HV items open | TASK-09 |
| Merge gate | `powershell -NoProfile -File scripts/dev.ps1 test` | Exit 0; UT-01..UT-26 in the JUnit XML; frontend 80% thresholds pass | TASK-10 |
| Handoff | `implement/handoff.md` review | Exact local state; 11 HV rows open; no human approval | TASK-11 |

## 5. SPEC to test

| SPEC | Tests |
|---|---|
| 001 | UT-01..UT-06, UT-12 |
| 002 | UT-13, UT-14, UT-26 |
| 003 | UT-15, UT-26 |
| 004 | UT-10, UT-16 |
| 005 | UT-18, UT-23 |
| 006 | HV-01, HV-03, HV-07 (host only) |
| 007 | UT-13..UT-20 |
| 008 | UT-01..UT-12, UT-23 |
| 009 | UT-07, UT-11 |
| 010 | HV-04 (host only) |
| 011 | HV-05 (host only) |
| 012 | HV-01..HV-05 (host only) |
| 013 | UT-24 (definition); TASK-10 (local run); HV-07 (pipeline run) |
| 014 | TASK-08 (executed evidence); HV-07 (pipeline gate) |
| 015 | UT-21 |
| 016 | UT-22 |
| 017 | UT-11, UT-12, UT-25 |
| 018 | HV-01..HV-11 (open) |
| 019 | TASK-09 diff checks (not a test) |

## 6. Test class map

| Class | UT IDs | Task |
|---|---|---|
| `C/CodeOwnersValidationTest.java` | UT-01, UT-02, UT-03, UT-04, UT-05, UT-06, UT-07, UT-08, UT-09, UT-10, UT-11, UT-12, UT-23 | TASK-01, TASK-02, TASK-04, TASK-05, TASK-06 |
| `C/OwnershipResolverTest.java` | UT-13, UT-14, UT-15, UT-16, UT-17, UT-18, UT-19, UT-20, UT-25, UT-26 | TASK-01, TASK-02, TASK-04, TASK-05 |
| `C/MergeRequestTemplateTest.java` | UT-21 | TASK-03, TASK-06 |
| `C/AgentsContextPathsTest.java` | UT-22 | TASK-03, TASK-06 |
| `C/PipelineDefinitionTest.java` | UT-24 | TASK-03, TASK-07 |

## 7. Human verification (open; never reported as passed here)

Owner of every row: the ACE team repository administrator with the recovery tech lead (story §3, §4 step 3; D-RCV-50). Unblock: OPEN-038 answered and HC-01..HC-08 applied; tracked by `PROP-OI-2`. Test MRs change fixture files only and are closed unmerged (story §17).

| ID | Covers | Steps on the ACE host | Expected | Status |
|---|---|---|---|---|
| HV-01 | AC1 clause 2, X1, BR6 | MR changing a recovery Java file; an outside-squad member approves | Merge blocked; code-owner review required | OPEN — NOT_TESTED_HERE |
| HV-02 | AC1 clause 1, AC2, AC4, flow 4-5 | MRs as UT-13, UT-15, UT-16 | Host lists the same sections and owners as the resolver | OPEN — NOT_TESTED_HERE |
| HV-03 | AC3, X3, flow 7 | MR changing one recovery and one common file; a recovery owner approves | Blocked until an ACE-team member approves | OPEN — NOT_TESTED_HERE |
| HV-04 | AC5, X4 | A recovery owner opens and approves their own MR | Approval not counted; a second member is needed | OPEN — NOT_TESTED_HERE |
| HV-05 | AC6, X5 | Push a commit to an approved MR | Approvals removed; review required again | OPEN — NOT_TESTED_HERE |
| HV-06 | X7, TC-TE-002-08 | A non-owner squad member approves | Merge refused; no MSG-P4-002 (story §16) | OPEN — NOT_TESTED_HERE |
| HV-07 | AC7 host part, X6, HC-06, HC-08, flow 2 and flow 6 pipeline run, SPEC-013 and SPEC-014 run | (1) MR with the file as specified; (2) MR with `@scb-ace/recovery-leads-typo`; (3) owner existence and write access | (1) Job passes, JUnit attached, coverage at or above 80%; (2) job fails and the merge is blocked; (3) every owner exists with write access | OPEN — NOT_TESTED_HERE |
| HV-08 | BR4, BR7 | MR changing `.gitlab/CODEOWNERS`; one team approves | Blocked until the other team approves | OPEN — NOT_TESTED_HERE |
| HV-09 | A-10, HC-07 | Open a new MR | Description pre-filled with the eight headings | OPEN — NOT_TESTED_HERE |
| HV-10 | Story §2 measure | Monthly MR report on recovery paths | 100% merged with code-owner approval | OPEN — NOT_TESTED_HERE |
| HV-11 | SPEC-017 | Before host adoption | No `@role-placeholder/` handle left in the file or register | OPEN — NOT_TESTED_HERE |

## 8. Story test cases (TC mapping)

A UT match is a partial local check; the TC passes only when its HV item passes. TC-TE-002-08 follows story §16, which ranks above Test Cases v7 (RUN-BRIEF precedence; SP-DG-06).

| Story TC | Covers | Local test | Host item |
|---|---|---|---|
| TC-TE-002-01 | AC1, BR1, BR6 | UT-13 | HV-01 |
| TC-TE-002-02 | AC2, BR3 | UT-16 | HV-02 |
| TC-TE-002-03 | AC3, BR6 | UT-17 | HV-03 |
| TC-TE-002-04 | AC4, BR2 | UT-15 | HV-02 |
| TC-TE-002-05 | AC5, BR6 | none (host only) | HV-04 |
| TC-TE-002-06 | AC6, BR6 | none (host only) | HV-05 |
| TC-TE-002-07 | AC7, BR7 | UT-07 | HV-07 |
| TC-TE-002-08 | Access | none (host only) | HV-06 |
