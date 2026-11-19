---
title: "Test scenarios: RWB-E1-042"
run_id: "INC-003-epic-1-RWB-E1-042"
revision: "v1 (18 Nov 2026): first test scenario map for this run, matching plan.md v1, tasks.md v1 and specify/spec.md revision 13 §15."
---

# Test scenarios: RWB-E1-042

Source: `../specify/spec.md` §15 (TC-E1-042-01 to TC-E1-042-46) and §12.14 (plan inputs). This file maps **every** acceptance criterion, business rule, exception row, flow row, transition, contract item, message and guardrail to a test ID, a level, a concrete test class and a task. Nothing is renamed, merged or dropped.

Levels in this repository: Unit and build checks in the `test` task (`./gradlew test`, no Docker); System in `recoveryIntegrationTest` (`@Tag("recovery-it")`, Spring Boot context, Testcontainers PostgreSQL 16, `./scripts/dev.ps1 it` or `./gradlew recoveryIntegrationTest`). The `ParameterLoadHandler` bean is called directly in the System tests because no endpoint exposes it until RWB-E1-043; the assertions are to the same depth an HTTP test would use (message ID, status, placeholders, `field`, database state; plan input P5). Every user ID in a test is a synthetic UUID generated for that test; "U-41" is such a label and is not a real identifier.

Path legend: `T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`.

## 1. Coverage matrix

| Test ID | TC | Covers | Level | Test (class#method) | Task | Status |
|---|---|---|---|---|---|---|
| T-E1-042-01 | TC-E1-042-01 | AC1, BR1 | System | `T/casewf/config/ParameterConfigIT#prodContextReadsSeedVersionOne` | TASK-20 | Ready |
| T-E1-042-02 | TC-E1-042-02 | AC2, BR1, X1 | Unit (build check, fixture) | `T/architecture/parameters/RwbMagicNumberCheckTest#literalNinetyFailsNamingFileLineAndKey` | TASK-04 | Ready |
| T-E1-042-03 | TC-E1-042-03 | AC3, BR2, X2; SPEC-003 (a)-(i) | Unit (build check, fixtures) | `T/architecture/parameters/CatalogCompletenessCheckTest#readsOfAnUncataloguedKeyFail` plus `#readerCallCases`, `#nonLiteralAndRefusedForms`, `#mapAndOptionalGetAreNotKeyReads`, `#exemptImplementationIsSkipped` | TASK-04 | Ready |
| T-E1-042-04 | TC-E1-042-04 | AC4, BR7, X3 | Unit and System | `T/casewf/config/ParameterStartupCheckTest#downWhenNoValueInForceAndNoDefault` and `ParameterConfigIT#readinessDownNamesKeyAndEnvironment` | TASK-16, TASK-20 | Ready |
| T-E1-042-05 | TC-E1-042-05 | AC5, X4 | Unit and System (interface) | `T/casewf/config/ParameterLoadValidatorTest#outOfRangeRefusesWithGen002` and `ParameterConfigIT#loadOutOfRangeIsRefusedWhole` | TASK-18, TASK-20 | Ready |
| T-E1-042-06 | TC-E1-042-06 | AC6, X5 | Unit and System (interface) | `ParameterLoadValidatorTest#wrongTypeRefusesWithP1002` and `ParameterConfigIT#loadWrongTypeIsRefusedWhole` | TASK-18, TASK-20 | Ready |
| T-E1-042-07 | TC-E1-042-07 | AC7, BR4, X6 | Unit and System (interface) | `ParameterLoadHandlerTest#authorCannotApprove` and `ParameterConfigIT#authorApproveIsRefused` | TASK-18, TASK-20 | Ready |
| T-E1-042-08 | TC-E1-042-08 | AC8 | System | `ParameterConfigIT#eachEnvironmentResolvesItsOwnValue` | TASK-20 | Ready |
| T-E1-042-09 | TC-E1-042-09 | AC9, BR6, X7 | Unit and System | `ParameterServiceTest#secretIsNeverServed` and `ParameterConfigIT#secretIsListedWithoutValue` | TASK-16, TASK-20 | Ready |
| T-E1-042-10 | TC-E1-042-10 | AC10, X8, §7.3 | Unit and System (interface) | `ParameterValidityTest#recomputeMakesTheEarlierVersionInForce` and `ParameterConfigIT#rollbackRestoresTheEarlierVersion` (a) and `#rollbackRebuildsOnlyAfterCommit` (b) | TASK-18, TASK-20 | Ready |
| T-E1-042-11 | TC-E1-042-11 | AC11, BR5, X10 | Unit and System | `ParameterCacheTest#aVersionStartsOnItsValidFromWithNoRestart` and `ParameterConfigIT#futureVersionStartsOnItsDate` | TASK-16, TASK-20 | Ready |
| T-E1-042-12 | TC-E1-042-12 | X9 (live access) | Access (live identity and matrix) | No automated class: a session from RWB-E1-022 and matrix PM-2026.11 from RWB-E1-037 are needed. Run `ParameterCatalogControllerTest#refusalCarriesTheActionText` as the seam only | — | **Blocked** (`OI-E1-042-001`). Exit: after RWB-E1-037 loads PM-2026.11 and RWB-E1-022 resolves the RW-PHONECOL test identity, run the live check (403 problem+json, MSG-P4-002, action "read parameters", no array, one refusal event) and record the evidence. Pass only on that evidence; never reported as passed here |
| T-E1-042-13 | TC-E1-042-13 | SPEC-001/002/006 | System | `T/casewf/config/ParameterMigrationIT#emptySchemaGetsTablesConstraintsIndexesAndSeed` | TASK-14 | Ready |
| T-E1-042-14 | TC-E1-042-14 | SPEC-001/002 | System | `ParameterMigrationIT#physicalSchemaSixGetsTheAdditions` | TASK-14 | Ready |
| T-E1-042-15 | TC-E1-042-15 | SPEC-001 | Unit (lint) | `T/architecture/RecoveryMigrationLintTest#migrationsFollowTheRecoveryRules` (`[E1-044]`, unchanged) | TASK-15 | Ready after RWB-E1-044 merges (PRE-6) |
| T-E1-042-16 | TC-E1-042-16 | SPEC-013 | Unit and System (interface) | `ParameterContentHashTest#quotedCodeListHashesOnTheUnquotedValue` and `ParameterLoadHandlerTest#identicalRepeatReturnsTheExistingLoad` and `ParameterConfigIT#identicalRepeatWritesNothing` | TASK-18, TASK-20 | Ready |
| T-E1-042-17 | TC-E1-042-17 | SPEC-013 | Unit and System (interface) | `ParameterLoadHandlerTest#differentContentWhereApprovedExistsIs409` and `ParameterConfigIT#conflictingContentIsRefused` | TASK-18, TASK-20 | Ready |
| T-E1-042-18 | TC-E1-042-18 | SPEC-015 | Unit and System (interface) | `ParameterLoadValidatorTest#blankReasonIsRefused` and `ParameterConfigIT#blankRollbackReasonIsRefused` | TASK-18, TASK-20 | Ready |
| T-E1-042-19 | TC-E1-042-19 | SPEC-015 | Unit and System (interface) | `ParameterLoadHandlerTest#rollbackWithNoEarlierVersionIsRefused` and `ParameterConfigIT#rollbackWithNoEarlierVersionChangesNothing` | TASK-18, TASK-20 | Ready |
| T-E1-042-20 | TC-E1-042-20 | SPEC-014 | Unit and System (interface) | `ParameterLoadHandlerTest#secondConcurrentApprovalIsRefused` and `ParameterConfigIT#concurrentApprovalsGiveOneApprovedAndOne409` | TASK-18, TASK-20 | Ready |
| T-E1-042-21 | TC-E1-042-21 | SPEC-003 | Unit (build check, fixture) | `T/architecture/parameters/CatalogCompletenessCheckTest#productRowWithoutDefaultPassesAndWithoutOwnerFails` | TASK-04 | Ready |
| T-E1-042-22 | TC-E1-042-22 | SPEC-021, findings 119, 152, 155, 158 | System | `ParameterConfigIT#flagOffStillStartsAndRefusesParameterLoads` (probe bean, test-only `ParameterLoadBranch` adapter, flag on and off) and `ParameterConfigIT#flagOnLoadsThroughTheAdapter` | TASK-20 | Ready |
| T-E1-042-23 | TC-E1-042-23 | SPEC-012, SPEC-023 | Unit and System (interface) | `ParameterLoadValidatorTest#unknownKeyEmptyFileAndPastValidFrom` and `ParameterConfigIT#unknownKeyEmptyFileAndPastValidFrom` | TASK-18, TASK-20 | Ready |
| T-E1-042-24 | TC-E1-042-24 | SPEC-020 seam, findings 120, 129 | Unit and System | `T/access/internal/InterimCapabilityCheckTest#requireAndHas` plus `T/casewf/config/ParameterCatalogControllerTest#refusalCarriesTheActionText` plus `ParameterConfigIT#readWithoutTheRightIsRefused` | TASK-12, TASK-16, TASK-20 | Ready (does not close TC-12) |
| T-E1-042-25 | TC-E1-042-25 | SPEC-004 | Unit (build check) | `RwbMagicNumberCheckTest#staleBaselineEntryFails` and `#unlistedLiteralFails` | TASK-04 | Ready |
| T-E1-042-26 | TC-E1-042-26 | SPEC-005, SPEC-024 | Unit | `ParameterKeysGenerationTest#typedConstantsExist` and `ParameterServiceTest#envKeyIsServedFromTheProperty` | TASK-06, TASK-16 | Ready |
| T-E1-042-27 | TC-E1-042-27 | SPEC-002/005/006/024, finding 121 | Unit and System | `ParameterKeysGenerationTest#generatedKeysMatchTheCatalogFile` (unit) and `ParameterMigrationIT#catalogTableEqualsTheGeneratedKeys` and `CatalogCompletenessCheckTest#changedDefaultWithoutMigrationIsReported` | TASK-06, TASK-14 | Ready |
| T-E1-042-28 | TC-E1-042-28 | SPEC-009/018/027 | Unit and System (interface) | `ParameterLoadHandlerTest#oneEventAfterCommitAndNoneOnRefusal` and `ParameterCacheTest#eventRebuildsTheEntry` and `ParameterConfigIT#approvalPublishesOneEventWithNoUserId` | TASK-18, TASK-16, TASK-20 | Ready |
| T-E1-042-29 | TC-E1-042-29 | SPEC-014/019/025/027, findings 125, 132, 137, 146 | Unit and System (interface) | `ParameterLoadHandlerTest#interimRecorderIsCalledOnceInsideTheTransaction` (a) and `#recorderFailureIs503AndRollsBack` (b) plus `ParameterConfigIT#recorderFailureLeavesRowsValidated` | TASK-18, TASK-20 | Ready |
| T-E1-042-30 | TC-E1-042-30 | SPEC-022/025/027, findings 135, 137, 144, 146 | Unit (`access.internal`) | `T/access/internal/ApiExceptionHandlerTest#apiErrorBranchUnchanged` (a), `#messageIdFormRendersEveryField` (b), `#statusOnly503HasNoMessageCode` (c), `#detailOverrideReplacesTheEnglishText` (d), `#constructorGuards` (e); `T/access/internal/MessageResolverTest#everyMessageResolvesInEnglishAndThai` | TASK-10 | Ready |
| T-E1-042-31 | TC-E1-042-31 | SPEC-011 | Unit and System | `ParameterCatalogControllerTest#filtersAndProductRowsWithoutValue` and `ParameterConfigIT#filtersByPrefixKindOwnerEnvironment` | TASK-16, TASK-20 | Ready |
| T-E1-042-32 | TC-E1-042-32 | SPEC-016, finding 123 | Unit and System | `ParameterStartupCheckTest#futureOnlyRowWithoutDefaultIsDownUntilItsDate` and `ParameterConfigIT#futureSeedNeverFailsReadiness` | TASK-16, TASK-20 | Ready |
| T-E1-042-33 | TC-E1-042-33 | SPEC-013, plan input P3 | System (interface) | `ParameterConfigIT#twoConcurrentIdenticalLoadsGiveOneLoadAndOneRepeat` | TASK-20 | Ready |
| T-E1-042-34 | TC-E1-042-34 | SPEC-025, E7, findings 126, 135, 137 | Unit and System | `ParameterCatalogControllerTest#databaseFailureIsAStatusOnly503` and `ParameterConfigIT#databaseOutageHasNoMessageCodeAndNoRetryText` | TASK-16, TASK-20 | Ready |
| T-E1-042-35 | TC-E1-042-35 | SPEC-017, E6, finding 133 | System (interface) | `ParameterConfigIT#unknownLoadIdIs404ForApproveAndRollback` (a) random UUID, (b) a seeded `parameter_value.id` | TASK-20 | Ready |
| T-E1-042-36 | TC-E1-042-36 | SPEC-014, §8, finding 133 | Unit and System (interface) | `ParameterLoadValidatorTest#validFromBeforeTheBusinessDateIsRefused` and `ParameterConfigIT#approvalAfterTheBusinessDateMovedIsRefused` | TASK-18, TASK-20 | Ready |
| T-E1-042-37 | TC-E1-042-37 | SPEC-015, §8, finding 133 | System (interface) | `ParameterConfigIT#onlyAnApprovedLoadCanBeRolledBack` (VALIDATED and ROLLED_BACK) | TASK-20 | Ready |
| T-E1-042-38 | TC-E1-042-38 | SPEC-014, §8, finding 133 | System (interface) | `ParameterConfigIT#approveOfAnApprovedOrRolledBackLoadIsRefused` | TASK-20 | Ready |
| T-E1-042-39 | TC-E1-042-39 | SPEC-015, E5, finding 133 | Unit and System (interface) | `ParameterLoadValidatorTest#reasonAtFourHundredIsAcceptedAndFourHundredAndOneIsRefused` and `ParameterConfigIT#rollbackReasonBoundary` | TASK-18, TASK-20 | Ready |
| T-E1-042-40 | TC-E1-042-40 | SPEC-017, §7.3, findings 133, 149 | System (interface) | `ParameterConfigIT#findHitsAndMissesAndAuditColumns` | TASK-20 | Ready |
| T-E1-042-41 | TC-E1-042-41 | SPEC-003, BR2, §7.1, finding 130 | Unit (tooling) | `T/architecture/parameters/CatalogFileParserTest#realCatalogParsesAndUsedBySplits` (a) and `#usedByGrammarRejectsBrokenValues` (b) | TASK-01 | Ready |
| T-E1-042-42 | TC-E1-042-42 | SPEC-005, finding 131 | Unit | `ParameterKeysGenerationTest#generatedKeysMatchTheCatalogFile` | TASK-06 | Ready |
| T-E1-042-43 | TC-E1-042-43 | SPEC-004, finding 131 | Unit (tooling) | `T/architecture/parameters/JavaLiteralTokenizerTest#commentsStringsTextBlocksAndChars` and `MagicNumberScannerTest#numericNormalisation` | TASK-01 | Ready |
| T-E1-042-44 | TC-E1-042-44 | SPEC-003, BR6, §7.1 credential rule, finding 138 | Unit (tooling) | `CatalogFileParserTest#credentialBearingPropertiesAreRefused` and `CatalogCompletenessCheckTest#credentialRuleAppliesToEveryEnvRow` | TASK-01, TASK-04 | Ready |
| T-E1-042-45 | TC-E1-042-45 | SPEC-026, findings 129, 136, 141 | Unit (existing boundary tests) | `T/architecture/RecoveryBoundaryTest#publishedSurfaceIsExactlyTheSpecifiedTypes` (`[TE-001]`, extended) and `th.co.scb.ace.demo.ModulithTest#modulesRespectTheirBoundaries` | TASK-08, TASK-09 | Ready |
| T-E1-042-46 | TC-E1-042-46 | SPEC-026, SPEC-023, GR3, D-RUN-19, findings 151, 156 | Unit | `T/casewf/config/CatalogParameterReaderImplTest#delegatesAndThrowsJdkTypesOnly` and `#twoArgumentGetUsesTheProviderDate` | TASK-16 | Ready |

46 test IDs, one per spec TC; TC-E1-042-12 is `Blocked` with its exit criterion and is the only row not `Ready`.

## 2. Acceptance-criterion map (no gaps)

| AC | Test IDs | AC | Test IDs |
|---|---|---|---|
| AC1 | T-E1-042-01 | AC7 | T-E1-042-07 |
| AC2 | T-E1-042-02 | AC8 | T-E1-042-08 |
| AC3 | T-E1-042-03 | AC9 | T-E1-042-09 |
| AC4 | T-E1-042-04 | AC10 | T-E1-042-10 |
| AC5 | T-E1-042-05 | AC11 | T-E1-042-11 |
| AC6 | T-E1-042-06 | — | — |

## 3. Business rule, exception and flow map

| Row | Test IDs |
|---|---|
| BR1 | T-E1-042-01, -02, -25, -26 |
| BR2 | T-E1-042-03, -41, -42 |
| BR3 | T-E1-042-05, -06, -16, -17 |
| BR4 | T-E1-042-07, -20, -29 |
| BR5 | T-E1-042-01, -11, -28 |
| BR6 | T-E1-042-09, -44 |
| BR7 | T-E1-042-04, -32 |
| X1, X2 | T-E1-042-02, T-E1-042-03 |
| X3, X4, X5 | T-E1-042-04, -05, -06, -23, -32 |
| X6, X7, X8 | T-E1-042-07, -09, -10, -19 |
| X9 | T-E1-042-24 (seam); T-E1-042-12 Blocked (live) |
| X10 | T-E1-042-11 |
| FL1 to FL4 | T-E1-042-41, -42, -02, -03, -13 |
| FL5 to FL7 | T-E1-042-05, -06, -16, -22, -07 |
| FL8 to FL10 | T-E1-042-11, -28, -26, -24 |
| ST1 to ST3 | T-E1-042-05, -16, -07, -11, -19 |
| PRE1 to PRE5 | T-E1-042-13, -14, -15 |
| CON1 to CON5 | T-E1-042-09, -31, -16, -17, -33, -35 to -39, -28, -42, -45 |
| AUTH | T-E1-042-07, -24 |
| MSG | T-E1-042-24, -29, -30 |
| GR1 to GR4 | T-E1-042-02, -25, -09, -29, -30, -40, -45, -46, -16, -41 |

## 4. Negative and boundary cases carried explicitly

- **Boundary values:** `case.entry.dpd` 1 and 365 accepted, 0 and 366 refused (`ParameterLoadValidatorTest`); rollback reason 400 accepted and 401 refused after trim (`ParameterLoadValidatorTest`, `ParameterConfigIT`); empty file, one-row file and a wrong header (`ParameterLoadValidatorTest`).
- **Refused forms of the reader-call rule:** non-literal first argument, `::` method reference, `var` local from a reader name, a name declared with two types in one file (`CatalogCompletenessCheckTest`).
- **Not key reads:** `Map.get(key)`, `Optional.get()`, a `get(` on any other receiver (`CatalogCompletenessCheckTest`).
- **Time:** a version approved before its `valid_from` leaves the earlier value in force until that date with no restart (`ParameterCacheTest`, `ParameterConfigIT`); a seeded `valid_from` in the future never fails readiness while the key has a default (`ParameterStartupCheckTest`, `ParameterConfigIT`).
- **Concurrency:** two identical loads at once give one set of rows and one `repeat = true` with no 500 (`ParameterConfigIT`); two approvals give one `APPROVED` and one 409 `MSG-GEN-004` (`ParameterLoadHandlerTest`, `ParameterConfigIT`).
- **Transaction boundaries:** a forced failure inside the rollback's own transaction leaves the rows `APPROVED` with `version` unchanged and the cache still serving v2 (`ParameterConfigIT`, with a `BEFORE_COMMIT` listener in the `casewf.config` test package); a recorder failure leaves the rows `VALIDATED` with no event and no cache rebuild (`ParameterLoadHandlerTest`, `ParameterConfigIT`).
- **Privacy:** no log line, event, exception message or response holds a user ID or a secret; `TC-29`, `TC-30`, `TC-34`, `TC-40` assert the absence, and `TASK-25` greps the diff.

## 5. Verification commands

| Level | Command | Evidence |
|---|---|---|
| Unit and build checks | `./gradlew test` (in `backend/`, with `$env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"`) | `backend/build/test-results/test/`, `implement/unit-tests/report.md` |
| Coverage | `./gradlew test recoveryCoverageVerification` | `backend/build/reports/jacoco/recoveryCoverageReport.xml` and HTML |
| System | `./scripts/dev.ps1 it` (or `./gradlew recoveryIntegrationTest`) | `backend/build/test-results/recoveryIntegrationTest/`, `implement/backend/it.log` |
| Merge gate | `powershell -NoProfile -File scripts/dev.ps1 test` | `implement/merge-gate.log` with the exit code |
| Live access | manual, after RWB-E1-022 and RWB-E1-037 | `T-E1-042-12` exit criterion; `OI-E1-042-001` |

## 6. Not planned, and why

| Item | Why |
|---|---|
| Playwright or browser test | No screen, route or component (UI In Scope NO) |
| REST Assured or `api-tests/` for the three load operations | No HTTP path until RWB-E1-043 (D-RUN-10); the interface tests assert the same depth |
| OpenAPI contract test | `api/recovery-api-v4.yaml` does not change; RWB-TE-003 owns the contract lint |
| ArchUnit cross-check of the reader-call rule | Optional in the spec (R10-2) and not adopted; the source-level rule and its unit cases carry the requirement |
| Test for `ParameterKeys` generator internals | Build-script code outside the measured bundle; its output is covered by T-E1-042-42, -26 and -27 (A-38) |
