---
title: "Test scenarios: RWB-E1-043 Reference data service with versioned tables"
run_id: "INC-008-epic-1-RWB-E1-043"
revision: "v1 (18 Nov 2026): first plan-stage scenario file. Every AC, BR, X row, TC, SEC case and CLAR row of specify/spec.md revision 10 is mapped to a named test and a task. Nothing is renamed, merged or dropped. Remediation run 2 (18 Nov 2026): T-E1-043-22 keeps the 38-key check and T-E1-043-33's System part moves from `ReferenceMigrationIT#catalogRowsMatchTheCatalogFile` to `ReferenceLoadIT#catalogRowsMatchTheCatalogFile` in TASK-15 (PLAN-001); T-E1-043-18 records the explicit `traceId`-absent assertion (PLAN-006). Counts are unchanged."
---

# Test scenarios: RWB-E1-043

Source: `../specify/spec.md` revision 10 (Test scenarios, the 11 TC-E1-043 cases, TC-RB, TC-HD, TC-PB, TC-FL, TC-MG, TC-BR1, TC-TM, TC-RP, TC-FD, TC-DR, TC-BD, TC-CAT and SEC-01..17), story file v7 section 16 and `plan.md` v1. This file maps **every** acceptance criterion, business rule, exception row, test case, security case and clarification to a test ID, a level, a concrete test class and method, and a task.

Levels in this repository: Unit and build checks in the `test` task (`./gradlew test`, no Docker); System in `recoveryIntegrationTest` (`@Tag("recovery-it")`, Spring Boot context, Testcontainers PostgreSQL 16, `./scripts/dev.ps1 it` or `./gradlew recoveryIntegrationTest`). The System tests use the real security filter and `MockMvc` (or `RestAssured` for FTS-E1043-01 in `api-tests/`). Every user ID in a test is a synthetic UUID generated for that test; "U-REF-01", "U-RSK-01" and "U-RSK-02" are labels, not values. No test asserts a real name, ID number, account number or address.

Path legend: `T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`; `TR` = `backend/src/test/resources`.

## 1. Coverage matrix

| Test ID | Source | Covers | Level | Test (class#method) | Task | Status |
|---|---|---|---|---|---|---|
| T-E1-043-01 | TC-E1-043-01 | AC1, BR2, BR3, BR8 | System | `T/casewf/refdata/ReferenceLifecycleIT#versionFourSupersedesVersionThree` | TASK-15 | Ready |
| T-E1-043-02 | TC-E1-043-02 | AC2, BR4, X1 | System | `T/casewf/refdata/ReferenceLoadIT#authorCannotApproveOwnLoad` | TASK-15 | Ready |
| T-E1-043-03 | TC-E1-043-03 | AC3, BR7 | System | `T/casewf/refdata/ReferenceReadIT#twoReadersLogOneLinePerTable` | TASK-15 | Ready |
| T-E1-043-04 | TC-E1-043-04 | AC4, BR5, X2 | System | `T/casewf/refdata/ReferenceLoadIT#rowCheckRefusesNamingRowAndColumn` | TASK-15 | Ready |
| T-E1-043-05 | TC-E1-043-05 | AC5, BR3, BR4 | System | `T/casewf/refdata/ReferenceLifecycleIT#unapprovedFutureVersionNotServed` | TASK-15 | Ready |
| T-E1-043-06 | TC-E1-043-06 | AC6, BR6, X3 | System | `T/casewf/refdata/ReferenceLoadIT#pastValidFromRefused` | TASK-15 | Ready |
| T-E1-043-07 | TC-E1-043-07 | AC7, X4 | System | `T/casewf/refdata/ReferenceLoadIT#identicalRepeatReturnsExistingLoad` | TASK-15 | Ready |
| T-E1-043-08 | TC-E1-043-08 | AC8, X5 | System | `T/casewf/refdata/ReferenceLifecycleIT#concurrentApprovalsOneWins` | TASK-15 | Ready |
| T-E1-043-09 | TC-E1-043-09 | AC9, BR9, X6 | System | `T/casewf/refdata/ReferenceReadIT#noVersionInForceStopsTheRun` | TASK-15 | Ready |
| T-E1-043-10 | TC-E1-043-10 | AC10, BR5, X7 | System | `T/casewf/refdata/ReferenceLoadIT#headerOnlyFileRefused` | TASK-15 | Ready |
| T-E1-043-11 | TC-E1-043-11 | Access, TC7 wording | System | `T/casewf/refdata/ReferenceSecurityIT#caseOwnerLoadRefusedAndAudited` | TASK-15 | Ready |
| T-E1-043-12 | TC-RB-01 | SPEC-024 | System | `T/casewf/refdata/ReferenceLifecycleIT#rollbackRestoresEarlierVersion` | TASK-15 | Ready |
| T-E1-043-13 | TC-RB-02 | SPEC-024 | System | `T/casewf/refdata/ReferenceLifecycleIT#rollbackRefusals` | TASK-15 | Ready |
| T-E1-043-14 | TC-HD-01 | SPEC-025, SPEC-030 | System | `T/casewf/refdata/ReferenceLoadIT#handlerMessagesPassThrough` | TASK-15 | Ready |
| T-E1-043-15 | TC-HD-02 | SPEC-025 | Unit | `T/casewf/refdata/internal/ReferenceTableHandlersTest#duplicateOrParameterHandlerFailsStartup` | TASK-07, TASK-08 | Ready |
| T-E1-043-16 | TC-HD-03 | SPEC-025, D-RUN-11 | System | `T/casewf/refdata/ReferenceLoadIT#dataProductHandlerPath` | TASK-15 | Ready |
| T-E1-043-17 | TC-HD-04 | SPEC-031 | System | `T/casewf/refdata/ReferenceLifecycleIT#changeSummaryAndDictionaryAudit` | TASK-15 | Ready |
| T-E1-043-18 | TC-HD-05 | SPEC-025 | System | `T/casewf/refdata/ReferenceLoadIT#rowKeyAndHandlerDefect` | TASK-15 | Ready |
| T-E1-043-19 | TC-PB-01 | SPEC-026, SPEC-030 | System | `T/casewf/refdata/ReferenceLoadIT#parameterBranchRouting` | TASK-15 | Ready |
| T-E1-043-20 | TC-PB-02 | SPEC-026, SPEC-030; E42S shared-updates row 25 | System | `T/casewf/refdata/ReferenceLoadIT#realParameterHandlerThroughEndpoints` | TASK-15 | Ready |
| T-E1-043-21 | TC-FL-01 | SPEC-018 | System | `T/casewf/refdata/ReferenceFlagIT#contextStartsInEveryFlagCombination` | TASK-15 | Ready |
| T-E1-043-22 | TC-MG-01 | SPEC-001 | System | `T/casewf/refdata/ReferenceMigrationIT#oneEndStateOnEmptyAndPs6`, `#columnsArePhysicalSchemaSix`, `#rerunAppliesNothing`, `#appendOnlyTriggersRefuse`, `#constraintsRefuseBadRows`, `#catalogKeysExist` | TASK-01, TASK-02 | Ready |
| T-E1-043-23 | TC-BR1 | SPEC-002 | System | `T/casewf/refdata/ReferenceLoadIT#ruleCodeAndHolidayRefused` | TASK-15 | Ready |
| T-E1-043-24 | TC-TM-01 | SPEC-032, SPEC-025 | System | `T/casewf/refdata/ReferenceLifecycleIT#datedHandlerFutureVersion` | TASK-15 | Ready |
| T-E1-043-25 | TC-TM-02 | SPEC-032, SPEC-010 | System | `T/casewf/refdata/ReferenceLifecycleIT#outOfOrderApproval` | TASK-15 | Ready |
| T-E1-043-26 | TC-TM-03 | SPEC-024, SPEC-032 | System | `T/casewf/refdata/ReferenceLifecycleIT#rollbackFutureVersion` | TASK-15 | Ready |
| T-E1-043-27 | TC-TM-04 | SPEC-024, SPEC-032 | System | `T/casewf/refdata/ReferenceLifecycleIT#rollbackInForceVersion` | TASK-15 | Ready |
| T-E1-043-28 | TC-TM-05 | SPEC-008, SPEC-024, SPEC-025, SPEC-032 rule 6 | System | `T/casewf/refdata/ReferenceLifecycleIT#currentStateRules` | TASK-15 | Ready |
| T-E1-043-29 | TC-RP-01 | SPEC-006, SPEC-025 L9/L11 | System | `T/casewf/refdata/ReferenceLoadIT#repeatMessageBeforeTheDate` | TASK-15 | Ready |
| T-E1-043-30 | TC-FD-01 | SPEC-015, SPEC-025 L3 | System | `T/casewf/refdata/ReferenceLoadIT#missingTableAndAreaRight` | TASK-15 | Ready |
| T-E1-043-31 | TC-DR-01 | SPEC-008 | System | `T/casewf/refdata/ReferenceLifecycleIT#decisionRecorderFailure` | TASK-15 | Ready |
| T-E1-043-32 | TC-BD-01 | SPEC-019 | Unit | `T/architecture/RecoveryBoundaryTest#refdataApiIsNamed`, `#publishedSurfaceIsExactlyTheSpecifiedTypes`, `#referenceTablesOnlyInRefdata`, `#accessAndIntegrationDoNotDependOnCasewf`, `#dataengineDoesNotDependOnCasewf`, `#fixtureDependencyFailsTheRule` | TASK-05, TASK-06 | Ready |
| T-E1-043-33 | TC-CAT-01 | SPEC-029 | Unit and System | `T/architecture/parameters/ReferenceCatalogRowsTest#catalogHasTheThirtyEightRows`, `ReferenceLoadIT#catalogRowsMatchTheCatalogFile` | TASK-03, TASK-04, TASK-15 | Ready |
| T-E1-043-34 | Unit | SPEC-003, grammar | Unit | `T/casewf/refdata/internal/ReferenceTableColumnsTest#definitionGrammar`, `#noneMeansNoDefinition`, `#malformedDefinition` | TASK-07, TASK-08 | Ready |
| T-E1-043-35 | Unit | SPEC-003, AC4 | Unit | `T/casewf/refdata/internal/ReferenceRowCheckTest#requiredAndTypeFailuresNameRowAndColumn`, `#unknownColumnRefused`, `#duplicateRowKeyRefused`, `#detailIsCappedAtOneHundred`, `#rowKeyIsTheKeyColumns` | TASK-07, TASK-08 | Ready |
| T-E1-043-36 | Unit | SPEC-006 | Unit | `T/casewf/refdata/internal/ContentHasherTest#canonicalFormSortsAndNormalises`, `#unparseableValueIsTrimmedText` | TASK-07, TASK-08 | Ready |
| T-E1-043-37 | Unit | SPEC-015 | Unit | `T/casewf/refdata/internal/ReferenceLoadFileReaderTest#csvQuotedFieldsAndBom`, `#xlsxFirstSheet`, `#shortRowIsUnreadable`, `#headerOnlyHasNoRows` | TASK-07, TASK-08 | Ready |
| T-E1-043-38 | Unit | SPEC-013 | Unit | `T/casewf/refdata/internal/ReferenceRowCacheTest#onlyApprovedIsCached`, `#entryExpiresAfterTtl`, `#approveEvictsTheTable`, `#exceptionIsNotCached` | TASK-09, TASK-10 | Ready |
| T-E1-043-39 | Unit | SPEC-014 | Unit | `T/casewf/refdata/internal/ReaderLogGateTest#repeatWithinTtlIsSuppressed`, `#newLineAfterExpiry` | TASK-09, TASK-10 | Ready |
| T-E1-043-40 | Unit | SPEC-012, SPEC-014 | Unit | `T/casewf/refdata/internal/ReferenceVersionLoggerTest#oneLinePerReaderTableVersionDate`, `#lineHasNoUserOrRowContent`, `#noVersionLogsErrorAndCounter` | TASK-09, TASK-10 | Ready |
| T-E1-043-41 | Unit | SPEC-011, SPEC-032 | Unit | `T/casewf/refdata/internal/ReferenceDataServiceImplTest#versionInForceByDate`, `#validatedAndRolledBackNeverServed`, `#versionsNewestFirstWithRollbackReason` | TASK-09, TASK-10 | Ready |
| T-E1-043-42 | Unit | SPEC-014, SPEC-018 | Unit | `T/casewf/refdata/internal/ReferenceDataReadersImplTest#namePatternAndEnabled` | TASK-09, TASK-10 | Ready |
| T-E1-043-43 | Unit | SPEC-007, SPEC-008 | Unit | `T/casewf/refdata/internal/ReferenceVersionRegistryTest#versionNumberIsMaxPlusOne`, `#repeatReturnsExisting`, `#earlyRepeatBeforeValidFrom`, `#approvedTwinRefused`, `#approveChecks`, `#currentStateApprovalRefusedBeforeDate`, `#validToRecomputation`, `#rollbackRules`, `#recorderFailureIs503`, `#handlerApplyAndRollback`, `#flagOffRefusesWrites` | TASK-11, TASK-12 | Ready |
| T-E1-043-44 | Unit | SPEC-008, SPEC-028 | Unit | `T/casewf/refdata/internal/ReferenceDecisionRecorderTest#mandatoryTransaction`, `#lineHasNoUser`; `ReferenceLoadAuditTest#lineFieldsAndNoUser`, `#doneAndRefused` | TASK-11, TASK-12 | Ready |
| T-E1-043-45 | Unit | SPEC-027 | Unit | `T/casewf/refdata/internal/ReferenceLoadAuthorityTest#areaRightFirst`, `#tableRightPerCode`, `#missingKeyRefuses`, `#unknownCodePassesTableRight`, `#unknownLoadPassesTableRight`, `#refusalIsNotPermittedWithAction`, `#refusalIsAudited` | TASK-13, TASK-14 | Ready |
| T-E1-043-46 | Unit | SPEC-030 | Unit | `T/casewf/refdata/internal/ReferenceLoadDispatcherTest#parameterGoesToTheBranch`, `#handlerAndBuiltInGoToTheRegistry`, `#missingParamsAre422`, `#unknownLoadIdIs404` | TASK-13, TASK-14 | Ready |
| T-E1-043-47 | Unit | SPEC-026 | Unit | `T/casewf/refdata/internal/ParameterLoadBranchTest#loadApproveRollbackRouteToTheHandler`, `#absentBeanIs404`, `#problemPassesThrough`, `#accessListGuardRefuses` | TASK-13, TASK-14 | Ready |
| T-E1-043-48 | Unit | SPEC-015 | Unit | `T/casewf/refdata/internal/ActorIdResolverTest#oidFirstThenSub`, `#noUuidClaimIs401` | TASK-13, TASK-14 | Ready |
| T-E1-043-49 | Unit | SPEC-015, SPEC-016, SPEC-024 | Unit | `T/casewf/refdata/internal/ReferenceLoadControllerTest#load201AndProblem`, `#approve200`, `#rollback200`, `#missingTable422`, `#unknownLoad404`, `#authorApprove409`, `#storeFailure503`, `#idempotencyKeyAccepted` | TASK-13, TASK-14 | Ready |
| SEC-01 | SEC-01 | Method security | System and Unit | `T/casewf/refdata/ReferenceSecurityIT#everyHandlerHasPreAuthorize` (a fixture controller without `@PreAuthorize` fails the same check) | TASK-15 | Ready |
| SEC-02 | SEC-02 | No token, load | System | `T/casewf/refdata/ReferenceSecurityIT#noTokenIs401` | TASK-15 | Ready |
| SEC-03 | SEC-03 | No token, approve | System | `T/casewf/refdata/ReferenceSecurityIT#noTokenIs401` | TASK-15 | Ready |
| SEC-04 | SEC-04 | No token, rollback | System | `T/casewf/refdata/ReferenceSecurityIT#noTokenIs401` | TASK-15 | Ready |
| SEC-05 | SEC-05 | RW-CASEOWN (R only) load | System | `T/casewf/refdata/ReferenceSecurityIT#caseOwnerLoadIs403` | TASK-15 | Ready |
| SEC-06 | SEC-06 | RW-COE on REGION (C, not loader) | System | `T/casewf/refdata/ReferenceSecurityIT#coeOnRegionIs403` | TASK-15 | Ready |
| SEC-07 | SEC-07 | RW-REFADM approve (no A) | System | `T/casewf/refdata/ReferenceSecurityIT#refadmApproveIs403` | TASK-15 | Ready |
| SEC-08 | SEC-08 | RW-COE approve on REGION (not approver) | System | `T/casewf/refdata/ReferenceSecurityIT#coeApproveOnRegionIs403` | TASK-15 | Ready |
| SEC-09 | SEC-09 | RW-CASEOWN rollback | System | `T/casewf/refdata/ReferenceSecurityIT#caseOwnerRollbackIs403` | TASK-15 | Ready |
| SEC-10 | SEC-10 | RW-LEGAL rollback (U, not loader) | System | `T/casewf/refdata/ReferenceSecurityIT#legalRollbackIs403` | TASK-15 | Ready |
| SEC-11 | SEC-11 | RW-RISK (R) PARAMETER load | System | `T/casewf/refdata/ReferenceSecurityIT#riskParameterLoadIs403` | TASK-15 | Ready |
| SEC-12 | SEC-12 | Author with A approves own load | System | `T/casewf/refdata/ReferenceSecurityIT#authorApproveIs409` | TASK-15 | Ready |
| SEC-13 | SEC-13 | Unknown loadId with the right | System | `T/casewf/refdata/ReferenceSecurityIT#unknownLoadIdIs404` | TASK-15 | Ready |
| SEC-14 | SEC-14 | Business date provider fails; cache never holds a non-APPROVED version | System and Unit | `T/casewf/refdata/ReferenceSecurityIT#businessDateFailureIs503`; `ReferenceRowCacheTest#onlyApprovedIsCached` | TASK-15 | Ready |
| SEC-15 | SEC-15 | PARAMETER load with an rwb.refload.* key | System | `T/casewf/refdata/ReferenceSecurityIT#parameterAccessListGuard` | TASK-15 | Ready |
| SEC-16 | SEC-16 | Non-UUID sub and UUID oid; neither UUID | System and Unit | `T/casewf/refdata/ReferenceSecurityIT#actorIdFromOidOrSub`; `ActorIdResolverTest#oidFirstThenSub` | TASK-15 | Ready |
| SEC-17 | SEC-17 | RW-DATASTEW interim A on a test handler; RW-DATASTEW on REGION | System | `T/casewf/refdata/ReferenceSecurityIT#datastewInterimApprove` | TASK-15 | Ready |

All 403 cases also assert `detail` = `MSG-P4-002` with `{action}` = "load reference data", "approve reference data" or "roll back reference data", never "do this" (finding 142; A-45). `ReferenceSecurityIT#refusalDetailCarriesActionText` is the shared assertion helper.

T-E1-043-18 (`ReferenceLoadIT#rowKeyAndHandlerDefect`) asserts the 500 status, the existing `ApiExceptionHandler.unexpected` `ProblemDetail` body (`title`, `status`) and that **no `traceId` member is present**, with nothing written. SPEC-025's `traceId` word is therefore asserted as absent, not satisfied (PG-E1-043-03; R18); the case is not reported as full coverage of that sentence.

## 2. Acceptance criteria

| AC | Statement (short) | Test | Task |
|---|---|---|---|
| AC1 | v4 approved with 5 rows; v3 keeps 4 rows and `valid_to` 2026-11-30; served by date | T-E1-043-01, T-E1-043-12 | TASK-12, TASK-15 |
| AC2 | Author approves own load: MSG-P7-002; stays VALIDATED; previous version served | T-E1-043-02, SEC-12 | TASK-12, TASK-15 |
| AC3 | Case service and allocation engine each log one line per table; no customer identifier | T-E1-043-03 | TASK-10, TASK-15 |
| AC4 | SERVICE_LEVEL row 12 `limit_days` "five": MSG-P3-027 naming row 12 and column; nothing written | T-E1-043-04 | TASK-08, TASK-15 |
| AC5 | LEGAL_PERIOD v2 VALIDATED is not served; v1 served | T-E1-043-05 | TASK-10, TASK-15 |
| AC6 | validFrom 2026-11-24 refused; nothing written | T-E1-043-06 | TASK-12, TASK-15 |
| AC7 | Same REGION file twice: the v5 load; no v6 | T-E1-043-07 | TASK-08, TASK-12, TASK-15 |
| AC8 | Two approvals: one wins, the other MSG-GEN-004 | T-E1-043-08 | TASK-12, TASK-15 |
| AC9 | TEAM with no approved version: run does not start; ERROR with table and date; counter | T-E1-043-09 | TASK-10, TASK-15 |
| AC10 | DOCUMENT_TYPE header only: MSG-GEN-001 rows; nothing written | T-E1-043-10 | TASK-08, TASK-12, TASK-15 |

## 3. Business rules

| BR | Statement (short) | Test | Task |
|---|---|---|---|
| BR1 | 12 codes; the list is data; no rule code; holiday from `v_ace_holiday` | T-E1-043-23, T-E1-043-16 | TASK-04, TASK-08, TASK-15 |
| BR2 | One load = one version, max + 1; never changed after write | T-E1-043-01, T-E1-043-07, T-E1-043-43 | TASK-02, TASK-12 |
| BR3 | Version in force = APPROVED with the latest `valid_from` at or before the business date | T-E1-043-01, T-E1-043-05, T-E1-043-24, T-E1-043-25 | TASK-10, TASK-12 |
| BR4 | Effective only after a non-author approves | T-E1-043-02, T-E1-043-05, SEC-12 | TASK-02, TASK-12 |
| BR5 | Any failed check refuses the load in full | T-E1-043-04, T-E1-043-10, T-E1-043-14 | TASK-08, TASK-12 |
| BR6 | `valid_from` before the business date refused; equal accepted (A-05); open cases keep their version | T-E1-043-06, T-E1-043-01 | TASK-12 |
| BR7 | Every engine logs table and version of every table it reads | T-E1-043-03, T-E1-043-40 | TASK-10 |
| BR8 | Approval sets `valid_to` of the replaced version to the day before | T-E1-043-01, T-E1-043-25 | TASK-12 |
| BR9 | An engine with no version in force does not run | T-E1-043-09, T-E1-043-40 | TASK-10 |

## 4. Exception rows (X) and the state transitions

| X | Case | Test | HTTP and message |
|---|---|---|---|
| X1 | Author approves own load | T-E1-043-02, SEC-12 | 409 MSG-P7-002; stays VALIDATED |
| X2 | Schema or key failure | T-E1-043-04 | 422 MSG-P3-027; every failed row in `detail` |
| X3 | Past `valid_from` | T-E1-043-06 | 422 MSG-P3-027 |
| X4 | Same table, date and hash | T-E1-043-07, T-E1-043-29 | 201 same body; a handler code with a repeat message gives 409 with that message |
| X5 | Concurrent approvals | T-E1-043-08 | 409 MSG-GEN-004 |
| X6 | No version in force | T-E1-043-09 | exception, ERROR line, counter, alert |
| X7 | Header-only file | T-E1-043-10 | 422 MSG-GEN-001 `rows` |

| Transition | Test |
|---|---|
| none to VALIDATED on a load | T-E1-043-01, T-E1-043-07 |
| VALIDATED to APPROVED (non-author, dates, no twin) | T-E1-043-01, T-E1-043-05, SEC-12 |
| VALIDATED stays VALIDATED on a refusal | T-E1-043-02, T-E1-043-28 (a) |
| APPROVED approve is 200 and no change | T-E1-043-43 (`#approveChecks`) |
| APPROVED to ROLLED_BACK, earlier version in force | T-E1-043-12, T-E1-043-27 |
| APPROVED rollback refused with a later approved version | T-E1-043-13, T-E1-043-27 |
| APPROVED rollback refused with no earlier version | T-E1-043-13, T-E1-043-28 (h) |
| ROLLED_BACK rollback is 200 and no change | T-E1-043-13 |
| ROLLED_BACK approve is 409 | T-E1-043-43 (`#approveChecks`) |
| VALIDATED rollback is 409 | T-E1-043-13 |

## 5. Test cases (TC) and SEC

| TC | Test IDs | Task |
|---|---|---|
| TC-E1-043-01..11 | T-E1-043-01..11 | TASK-15 |
| TC-RB-01, TC-RB-02 | T-E1-043-12, T-E1-043-13 | TASK-15 |
| TC-HD-01..05 | T-E1-043-14..18 | TASK-07, TASK-08, TASK-15 |
| TC-PB-01, TC-PB-02 | T-E1-043-19, T-E1-043-20 | TASK-15 |
| TC-FL-01 | T-E1-043-21 | TASK-15 |
| TC-MG-01 | T-E1-043-22 | TASK-01, TASK-02 |
| TC-BR1 | T-E1-043-23 | TASK-15 |
| TC-TM-01..05 | T-E1-043-24..28 | TASK-15 |
| TC-RP-01 | T-E1-043-29 | TASK-15 |
| TC-FD-01 | T-E1-043-30 | TASK-15 |
| TC-DR-01 | T-E1-043-31 | TASK-15 |
| TC-BD-01 | T-E1-043-32 | TASK-05, TASK-06 |
| TC-CAT-01 | T-E1-043-33 | TASK-03, TASK-04, TASK-15 |
| SEC-01..17 | SEC-01..SEC-17 | TASK-13, TASK-14, TASK-15 |

TC7 TC-E1-043-03 and -05 use HOLIDAY fixtures; S7 AC3/AC5 govern (GAP-03). 400 is not tested (GAP-28).

## 6. Clarification rows

| CLAR | Decision | SPEC | Task | Evidence |
|---|---|---|---|---|
| CLAR-001 | Row key is per version, not global | 001 | TASK-01, TASK-02 | T-E1-043-22, T-E1-043-33 |
| CLAR-002 | Rule codes and HOLIDAY refused (no definition) | 002 | TASK-08 | T-E1-043-23 |
| CLAR-003 | Definitions live in the E1-042 catalog and this migration; grammar A-34 | 003, 029 | TASK-03, TASK-04, TASK-08 | T-E1-043-33, T-E1-043-34 |
| CLAR-004 | `validFrom` equal to the business date is accepted | 005 | TASK-12 | T-E1-043-06, T-E1-043-43 |
| CLAR-005 | Repeat load is 201 with the same body | 006 | TASK-08, TASK-12 | T-E1-043-07, T-E1-043-29 |
| CLAR-006 | Business date from E1-042's provider | 017 | TASK-14 | T-E1-043-06, SEC-14 |
| CLAR-007 | Area A through the grants file plus per-table lists | 027 | TASK-14 | SEC-05..08, SEC-17, T-E1-043-45 |
| CLAR-008 | Rollback built here (D-RUN-10) | 024 | TASK-12, TASK-14 | T-E1-043-12, T-E1-043-13 |
| CLAR-009 | Reader-bound service and exception; engines are seams | 012, 014 | TASK-10 | T-E1-043-03, T-E1-043-09 |
| CLAR-010 | Approval after `valid_from` passed is refused (A-17) | 008 | TASK-12 | T-E1-043-28 (e) |
| CLAR-011 | MSG-P3-027 wording from MSG4 | 020 | TASK-14 | T-E1-043-04, T-E1-043-11 |
| CLAR-012 | Handler registry and full contract (D-RUN-11) | 025 | TASK-06, TASK-08, TASK-12, TASK-14 | T-E1-043-14..18, T-E1-043-43 |
| CLAR-013 | The shared endpoint is owned here; PARAMETER is a dispatcher branch (D-RUN-10) | 026, 030 | TASK-14 | T-E1-043-19, T-E1-043-20 |
| CLAR-014 | RW-COE owns no built-in table until named (fail closed) | 027 | TASK-04, TASK-14 | SEC-06 |
| CLAR-015 | Interim audit log; RWB-E1-039 replaces it | 028 | TASK-12, TASK-14 | T-E1-043-11, T-E1-043-44 |
| CLAR-016 | Registry and generic checks here; `sys_fields`/`is_personal` in RWB-E1-064 | 025, 028, 031 | TASK-12, TASK-15 | T-E1-043-17 |
| CLAR-017 | No load may carry an `rwb.refload.*` key | 026, 027, 029 | TASK-14 | SEC-15, T-E1-043-47 |
| CLAR-018 | Actor from `oid`, else `sub`, as a UUID, else 401 | 015, 016, 024 | TASK-14 | SEC-16, T-E1-043-48 |
| CLAR-019 | P3 `casewf.refdata` plus the P4 LOV read and handler SPI; AC-VERS through a local port | 002, 008, 018, 019 | TASK-05, TASK-06, TASK-12, TASK-14 | T-E1-043-32, T-E1-043-31, T-E1-043-21 |
| CLAR-020 | Effective date and version independence; `DATED` versus `CURRENT_STATE` | 024, 025, 032 | TASK-06, TASK-12, TASK-15 | T-E1-043-24..28 |

All 20 rows are `RESOLVED` or `RESOLVED_BY_ASSUMPTION` in the spec; none is `OPEN`. The owner-acceptance items (A-01, A-07, A-08, A-09/A-34, A-16, A-17, A-27, A-31, A-33, A-37, A-38, A-39, A-40, A-41, A-42) stay open and are not treated as answered.

## 7. NFR evidence

| NFR | Test | Task |
|---|---|---|
| NFR-RWB-005 security | SEC-01..17 | TASK-15 |
| NFR-RWB-006 privacy | T-E1-043-03, T-E1-043-40, T-E1-043-44; the no-user-ID assertions | TASK-10, TASK-12 |
| NFR-RWB-008 observability | T-E1-043-03, T-E1-043-09, T-E1-043-44 | TASK-10, TASK-12 |
| NFR-RWB-009 operability | T-E1-043-21 | TASK-14 |

NFR-RWB-001/002/003/004/007/010 are `N/A` or inherited per the spec NFR table; no test is invented for them.

## 8. Exit criteria and human verification

- The plan is complete when every row above has a named class and method, every `recovery-it` class runs with Docker, `./gradlew test recoveryCoverageVerification` exits 0 with four counters at or above 0.80, and `./scripts/dev.ps1 test` and `it` exit 0.
- **Blocked, never reported as passed:**
  - HV-E1043-01: the 12 tables' version 1 approved in SIT (needs RWB-E1-038, -019, -025, -045, -046, Legal; PRODUCT, REGION and EXPOSURE_BAND have no named owner, GAP-43). Exit: each owning story loads and approves its table in SIT and the evidence is recorded.
  - HV-E1043-02: a real RW- identity and the RWB-E1-037 matrix confirm the 403 action text and the audit. Exit: after RWB-E1-022 and RWB-E1-037, run TC-E1-043-11 with a real SIT identity and record the problem body and one REFUSED audit event.
  - HV-E1043-03: RWB-E1-064's `sys_fields` handler refuses an `is_personal` change and a rollback restores no mark (RW-COMPLY open item). Exit: the RWB-E1-064 test evidence is attached; this story has no runtime check.
  - HV-E1043-04: the recovery tech lead ratifies D-RUN-18, D-RUN-19, D-RUN-20 and D-RUN-21 (OPEN-050). Exit: the decision record is signed; otherwise the plan gate records it open.
  - HV-E1043-05: the API owner retags the three operations to P3 and adds the 404/500 rows (GAP-48, GAP-53). Exit: the API v4 update is merged; no code change is needed here.
- **Not tested here:** the `/verify` and `GET /admin/lists` operations (GAP-11, GAP-34); the rule-package endpoints; the screens SCR-39/40/42; the `QueueVersionApplier`; the real business-date view; the decision-log and access-log stores.
