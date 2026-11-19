---
title: "Test scenarios: RWB-E1-001 Recovery tables for the 14 data products"
run_id: "INC-009-epic-1-RWB-E1-001"
story: "RWB-E1-001"
revision: "v1 (18 Nov 2026): first plan-stage scenario file. Every AC, BR, exception row, test case, NFR and CLAR row of specify/spec.md revision 4 is mapped to a named test and a task. Nothing is merged, renamed or dropped."
---

# Test scenarios: RWB-E1-001

Source: `../specify/spec.md` revision 4 ("Test scenarios" TC-E1-001-01..-20, the AC/BR coverage table),
Story v7 §16 (TC-E1-001-01..-12 and TC-E1-001-11), `plan.md` v1 and `data-model.md` § 15.

Levels in this repository: **Unit** and static checks in the `test` task (`./gradlew test`, no Docker);
**System** in `recoveryIntegrationTest` (`@Tag("recovery-it")`, Spring Boot context, Testcontainers
PostgreSQL 16.16, `./scripts/dev.ps1 it`); **API Tester** against the local stack (`api-tests/`).
Every user ID is a synthetic UUID generated for its test; no test asserts a real name, ID number,
account number or address. No test result is claimed at plan time.

Path legend: `T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`; `TR` =
`backend/src/test/resources`.

## 1. Coverage matrix

| Test ID | Source | Covers | Level | Test (class#method) | Task | Status |
|---|---|---|---|---|---|---|
| T-E1001-01 | TC-E1-001-01 | AC1, BR1, BR6, BR8 | System | `T/dataengine/internal/catalog/RecoverySchemaMigrationIT#schemaHoldsNinetyThreeTablesAndThisFileCreatedEightyNine`, `#removedTablesAreAbsent`, `#noConstraintReferencesPublic`, `#theEighteenLinkColumnsAreVarchar255WithNoForeignKey` | TASK-02, TASK-03 | Ready |
| T-E1001-02 | TC-E1-001-02 | AC2, BR1 | System | `RecoverySchemaMigrationIT#viewReturnsTheAc2Rows`; `T/dataengine/internal/catalog/DataProductCatalogLoadIT#viewReturnsAc2RowsAfterCatalogLoad` | TASK-02, TASK-03, TASK-14 | Ready |
| T-E1001-03 | TC-E1-001-03 | AC3, BR2, BR3, BR5 | System + API | `DataProductCatalogLoadIT#validLoadIsValidatedThenAppliedOnApproval` | TASK-14 | Ready (ASM for the DP07/BR3 text) |
| T-E1001-04 | TC-E1-001-04 | AC4 | System | `RecoverySchemaMigrationIT#failedStatementLeavesNoObjectAndNoSuccessRow` | TASK-02, TASK-03 | Ready |
| T-E1001-05 | TC-E1-001-05 | AC5, BR1 | System | `T/architecture/dictionary/DataDictionaryConformanceTest#c1EveryColumnHasOneField`, `#c2EveryFieldHasOneColumn`, `#c3PhysicalTypesMatch`, `#proofFixturesFailWithTheAc5Texts` | TASK-02, TASK-03 | Ready |
| T-E1001-06 | TC-E1-001-06 | AC6 | System | `RecoverySchemaMigrationIT#rerunAppliesNothing` | TASK-02, TASK-03 | Ready |
| T-E1001-07 | TC-E1-001-07 | AC7, BR3, BR4, X4 | System + API | `DataProductCatalogLoadIT#twoDefectsAreBothReported` | TASK-14 | Ready (ASM) |
| T-E1001-08 | TC-E1-001-08 | AC8, BR2, BR4, X5 | System + API | `DataProductCatalogLoadIT#missingProductNamesDp09` | TASK-14 | Ready |
| T-E1001-09 | TC-E1-001-09 | AC9, BR4, X6 | System + API | `DataProductCatalogLoadIT#ac9TwoVerbatimTexts` | TASK-14 | Ready |
| T-E1001-10 | TC-E1-001-10 | AC10, BR4, X7 | System + API | `DataProductCatalogLoadIT#repeatReturns409MsgP1011AndWritesNothing` | TASK-14 | Ready |
| T-E1001-11 | TC-E1-001-11 | X8, authority | System + API | `DataProductCatalogLoadIT#dataStewardGets403MsgP4002AndOneRefusedAuditLine` | TASK-14 | Ready (seam: persistent log) |
| T-E1001-12 | TC-E1-001-12 | AC11, BR3, BR5, X4 | System + API | `DataProductCatalogLoadIT#bareSourceRefused` | TASK-14 | Ready (ASM) |
| T-E1001-13 | TC-E1-001-13 | BR3, SPEC-018 (1) | Unit + System | `T/architecture/dictionary/DictionarySeedShapeTest#dataProductSeedFitsItsColumns`, `#dp07IsVerbatim`; `T/dataengine/internal/catalog/SeedIntegrityIT#seedFitsColumnWidths` | TASK-01, TASK-02, TASK-03 | Ready (ASM — Blocker = Yes) |
| T-E1001-14 | TC-E1-001-14 | BR7, SPEC-018 (2) | System | `SeedIntegrityIT#personalMarksEqualTheFixture` | TASK-02, TASK-03 | Ready (ASM — Blocker = Yes) |
| T-E1001-15 | TC-E1-001-15 | SPEC-010 | System | `T/RecoveryDatabaseIT#serviceSeesAllThirtyAceViewsAndNoPublicTable`, `#directReadOfAnAceTableFailsInTheCatalog`, `#aceViewsAreReadOnlyForTheService`, `#recoveryFlywayBaselinedItsOwnHistoryTable`, `#decisionLogIsAppendOnly`, `#temporalAndRecoveryIdentitiesAreSeparated` | TASK-12, TASK-13, TASK-16 | Ready |
| T-E1001-16 | TC-E1-001-16 | SPEC-017, -019 | Unit | `T/dataengine/internal/catalog/DataProductCatalogSettingsTest#beanExistsWhenFlagOn`, `#noBeanWhenFlagOff`, `#noParameterHandlerBean` | TASK-08, TASK-09 | Ready |
| T-E1001-17 | TC-E1-001-17 | BR7, SPEC-018 (4), T10 | Unit + CI lint | `DictionarySeedShapeTest#everySysFieldsRowIsAnInsertWithALiteralIsPersonal`, `#noUpdateOfSysFields`, `#trueFieldIdsEqualTheFiveHundredTwentySixFixture`; TASK-18 runs the RWB-TE-011 lint (conditional) | TASK-01, TASK-03, TASK-18 | Ready (ASM; lint conditional on TE-011 merge) |
| T-E1001-18 | TC-E1-001-18 | AC7, X4, SPEC-013 K3 | Unit + API | `T/dataengine/internal/catalog/DataProductCatalogHandlerTest#singleDefectNoOwnerGivesExactlyOneMsgP1003`; `DataProductCatalogLoadIT#singleDefectNoOwnerIs422` | TASK-06, TASK-07, TASK-14 | Ready |
| T-E1001-19 | TC-E1-001-19 | AC7, X4, SPEC-013 K2 | Unit + API | `DataProductCatalogHandlerTest#singleDefectEmptySystemOfRecordGivesExactlyOneMsgP1003`; `DataProductCatalogLoadIT#singleDefectEmptySystemOfRecordIs422` | TASK-06, TASK-07, TASK-14 | Ready |
| T-E1001-20 | TC-E1-001-20 | SPEC-019 item 5 | Unit + System | `T/architecture/dictionary/ParameterCatalogRowsTest#csvHasTheTwoRowsWithOneShape`, `#migrationInsertsTheTwoRowsOnConflictDoNothing`, `#noRefdataColumnsOrLovRefTableRow`, `#noValueRow`; the load IT proves the authority reads both keys | TASK-10, TASK-11, TASK-14 | Ready |
| T-E1001-21 | SPEC-013 K0-H | X11, SPEC-013 | Unit | `DataProductCatalogHandlerTest#headerMustHoldTheEightCatalogColumns`, `#headerTextRendersMsgP3027` | TASK-06, TASK-07 | Ready |
| T-E1001-22 | SPEC-013 K0-R | X11, SPEC-013 | Unit | `DataProductCatalogHandlerTest#requiredValuesAndWidths`, `#k0RTextRendersMsgP3027` | TASK-06, TASK-07 | Ready |
| T-E1001-23 | SPEC-013 K1 | AC8, X5, SPEC-013 | Unit | `DataProductCatalogHandlerTest#unknownOrDuplicateCodeIsRefusedByTheSameCheck`, `#missingProductIsNamedAscending` | TASK-06, TASK-07 | Ready |
| T-E1001-24 | SPEC-013 K2, ASM-E1001-09 | BR3, BR5, AC11 | Unit | `T/dataengine/internal/catalog/SystemOfRecordGrammarTest#f1Passes`, `#f2Passes`, `#f3GrammarAcceptsARewordedQualifier`, `#theCoreBankIsASource`, `#negativesAreRefused`, `#everySeedValueMatchesExactlyOneForm` | TASK-06, TASK-07 | Ready (ASM) |
| T-E1001-25 | SPEC-014 | BR4, AC3, AC10 | Unit + System | `T/dataengine/internal/catalog/DataProductCatalogApplyTest#applyUpdatesAllFourteenAndReturnsFourteen`, `#applySetsValidFromAndStandardColumns`, `#missingProductThrowsAndNothingIsSaved`; `DataProductCatalogLoadIT#applyRollsBackWhenAProductDisappears` | TASK-06, TASK-07, TASK-14 | Ready |
| T-E1001-26 | SPEC-015 | AC7, AC9, AC11, X11 | Unit | `T/access/internal/DataProductMessagesTest#fourIdsResolveEnglishAndThai`, `#fourRenderedTextsAreExact` | TASK-04, TASK-05 | Ready |
| T-E1001-27 | SPEC-017, X10 | NFR-RWB-009 | System | `DataProductCatalogLoadIT#flagOffGives422MsgP3027` | TASK-14 | Ready |
| T-E1001-28 | SPEC-002, T1/T2/T5..T11 | BR1, BR6, BR9 | Unit | `T/architecture/dictionary/MigrationDerivationTest#tableSetIsPhysicalSchemaV6MinusTheFour`, `#columnsMatchPhysicalSchemaV6`, `#foreignKeysAndIndexesMatch`, `#t8ObjectsAreNotCreatedButTheirDictionaryRowsAre`, `#noIfNotExistsDropGrantOrSearchPath`, `#noLiteralSchemaOutsideStringsAndComments` | TASK-01, TASK-03 | Ready |
| T-E1001-29 | SPEC-005 | AC2 | Unit | `MigrationDerivationTest#viewIsTheSpecifiedDefinition` | TASK-01, TASK-03 | Ready |
| T-E1001-30 | SPEC-002 T6 | BR9, AC1 | System | `RecoverySchemaMigrationIT#noAceViewOrHelperFunctionFromThisMigration` | TASK-02, TASK-03 | Ready |
| T-E1001-31 | SPEC-002 T8 | AC1, AC4 | System | `RecoverySchemaMigrationIT#earlierStoryObjectsAreIntact`, `#theFourTablesExistExactlyOnce` | TASK-02, TASK-03 | Ready |
| T-E1001-32 | SPEC-019 item 4 | AC3 | Unit | `ParameterCatalogRowsTest#noRefdataColumnsOrLovRefTableRow` | TASK-10, TASK-11 | Ready |
| T-E1001-33 | SPEC-010 S1/S2 | NFR-RWB-009, X9 | System | `RecoveryDatabaseIT` (moved stage) and the TASK-13 script read-back; the invalid S1=true + S3=true combination is documented and refused | TASK-12, TASK-13, TASK-16 | Ready |

## 2. Acceptance criteria

| AC | Verdict | Test(s) | Notes |
|---|---|---|---|
| AC1 | COVERED | T-E1001-01, -05, -28, -30, -31 | 93 tables (89 created here), the 4 T8 tables once, the 20 removed tables and `payment_match_rule` absent, 0 constraints into `public`, 18 link columns `varchar(255)` with no FK, conformance 1,050/1,078 |
| AC2 | COVERED | T-E1001-02, -29 | DF-ACE-018 and DF-EXT-028 rows; the owner UUID comes from the synthetic catalog load |
| AC3 | COVERED | T-E1001-03, -25 | 14 rows; DP01/DP03/DP06 values; approve writes; version +1 |
| AC4 | COVERED | T-E1001-04, -31 | The failing-`valuation_ext` copy leaves no object and no success row; E1-042/E1-043 objects intact |
| AC5 | COVERED | T-E1001-05 | Both AC5 texts; the `char(64)` pass |
| AC6 | COVERED | T-E1001-06 | Second migrate applies 0; 123/1,382 |
| AC7 | COVERED | T-E1001-07, -18, -19 | Two MSG-P1-003 findings; `messageCode` MSG-P1-003; single-defect cases |
| AC8 | COVERED | T-E1001-08, -23 | "Missing: DP09."; no row |
| AC9 | COVERED | T-E1001-09, -26 | The two verbatim texts with `{row}` 4 and 5 |
| AC10 | COVERED | T-E1001-10 | 409 MSG-P1-011, nothing written (`GAP-E1001-13`, Blocker No) |
| AC11 | COVERED | T-E1001-12, -24 | "CCMS" refused with MSG-P1-003; version in force unchanged |

## 3. Business rules

| BR | Verdict | Test(s) | Notes |
|---|---|---|---|
| BR1 | COVERED | T-E1001-01, -05, -13, -28 | Every column has one field, every table field has one column, types match; 1,382 rows |
| BR2 | COVERED | T-E1001-03, -08 | 14 rows DP01–DP14; K1 refuses any other set |
| BR3 | COVERED (ASM) | T-E1001-03, -07, -12, -24 | Grammar F1–F3; DP07 fits only under `ASM-E1001-13` (`GAP-E1001-17`, Blocker = Yes) |
| BR4 | COVERED | T-E1001-07..-10, -25 | `validate` writes nothing; `apply` one transaction; a refusal writes nothing |
| BR5 | COVERED | T-E1001-12, -24 | `ACE (ingested from …)` required; a bare source refused |
| BR6 | COVERED | T-E1001-28, -33 | `${recoverySchema}` only; one migration; forward only |
| BR7 | COVERED (ASM) | T-E1001-14, -17 | 526 literals; no `UPDATE`; TE-011 lint conditional (`GAP-E1001-18`, Blocker = Yes) |
| BR8 | COVERED | T-E1001-01 | 0 constraints into `public`; 18 link columns |
| BR9 | COVERED | T-E1001-28, -30 | 30 view objects + 304 fields seeded; no view created |

## 4. Exception rows (X) and the state transitions

| X | Test(s) | Expected |
|---|---|---|
| X1 migration failure | T-E1001-04 | Rollback; the failing statement in the Flyway log; no success row |
| X2 conformance failure | T-E1001-05 | Both AC5 texts; a proof fixture for each direction |
| X3 re-run | T-E1001-06 | Nothing applied; counts unchanged |
| X4 no/two/bare system or no owner | T-E1001-07, -12, -18, -19 | 422 MSG-P1-003 per product; `messageCode` = MSG-P1-003 even as the only defect |
| X5 not exactly DP01–DP14 | T-E1001-08, -23 | 422 MSG-P1-004 naming the missing codes |
| X6 owner role or refresh cycle outside its list | T-E1001-09 | 422 MSG-P1-007 per row and field, AC9 texts |
| X7 same file again | T-E1001-10 | 409 `Problem` MSG-P1-011; no new version; rows unchanged |
| X8 caller without Reference data C | T-E1001-11 | 403 MSG-P4-002; one REFUSED `REFERENCE_LOAD_AUDIT` line; persistent log is E1-039's |
| X9 S1=true with Flyway on | T-E1001-33 | Refused by configuration; documented invalid combination |
| X10 flag off | T-E1001-27 | No bean; 422 MSG-P3-027; nothing written |
| X11 wrong header, empty required value, over-width | T-E1001-21, -22, -26 | 422 MSG-GEN-001 or MSG-P3-027 with `{table}=data_product`; nothing written |

State transitions (spec): the schema goes from E1-042/E1-043 applied to this migration's history row
`success = true` (or unchanged with no row on failure); the catalog goes from seed version 1 to version
2 on an approved apply, and stays unchanged on a refusal or a repeat. Covered by T-E1001-03, -04, -06,
-10, -25.

## 5. Test cases (TC) and SEC

| TC | Test(s) | Level | Status |
|---|---|---|---|
| TC-E1-001-01 | T-E1001-01 | System | Ready |
| TC-E1-001-02 | T-E1001-02 | System | Ready |
| TC-E1-001-03 | T-E1001-03 | System + API | Ready (ASM for BR3) |
| TC-E1-001-04 | T-E1001-04 | System | Ready |
| TC-E1-001-05 | T-E1001-05 | System | Ready |
| TC-E1-001-06 | T-E1001-06 | System | Ready |
| TC-E1-001-07 | T-E1001-07 | System + API | Ready |
| TC-E1-001-08 | T-E1001-08 | System + API | Ready |
| TC-E1-001-09 | T-E1001-09 | System + API | Ready |
| TC-E1-001-10 | T-E1001-10 | System + API | Ready |
| TC-E1-001-11 | T-E1001-11 | System (access) + API | Ready (interim audit; persistent log is E1-039's seam) |
| TC-E1-001-12 | T-E1001-12 | System + API | Ready |
| TC-E1-001-13 | T-E1001-13 | Unit + System | Ready (ASM) |
| TC-E1-001-14 | T-E1001-14 | System | Ready (ASM) |
| TC-E1-001-15 | T-E1001-15 | System | Ready |
| TC-E1-001-16 | T-E1001-16 | Unit | Ready |
| TC-E1-001-17 | T-E1001-17 | Unit + lint | Ready (lint conditional on TE-011) |
| TC-E1-001-18 | T-E1001-18 | Unit + API | Ready |
| TC-E1-001-19 | T-E1001-19 | Unit + API | Ready |
| TC-E1-001-20 | T-E1001-20 | Unit + System | Ready |

Security cases in this story's scope: the 403 refusal (T-E1001-11), the audit line (same), the flag-off
previous path (T-E1001-27), and no personal data in any log or fixture (TASK-18). Authentication and
maker-checker are E1-043's and are referenced, not rebuilt.

## 6. Clarification rows

| CLAR | Status in spec | Test / task consequence |
|---|---|---|
| CLAR-001 | RESOLVED | PS v6 counts; T-E1001-28, T-E1001-14/17 |
| CLAR-002 | RESOLVED | `<seq>` at merge; no test fixes a number (TASK-19) |
| CLAR-003 | RESOLVED | S1–S3; T-E1001-15, -33 |
| CLAR-004 | RESOLVED | Seed ownership; T-E1001-28, T-E1001-14/17 |
| CLAR-005 | RESOLVED | Story v7 §13 seed values; T-E1001-03, -13 |
| CLAR-006 | RESOLVED | View columns; T-E1001-02, -29 |
| CLAR-007 | RESOLVED | P4 SPI; T-E1001-16, T-E1001-25 |
| CLAR-008 | RESOLVED | Lint ignores literals (E1-044); T-E1001-28 |
| CLAR-009 | OPEN (non-blocking) | Who approves: E1-043's interim A row for RW-DATASTEW; T-E1001-03, -11 use it; OPEN-NEW-2 |
| CLAR-010 | RESOLVED | MSG-P1-003 text; T-E1001-26 |
| CLAR-011 | **OPEN (Blocker = Yes, GAP-E1001-17)** | DP07 width; T-E1001-13 is ready on `ASM-E1001-13`; the merge waits for the human ruling (TASK-19, OPEN-NEW-6) |
| CLAR-012 | **OPEN (Blocker = Yes, GAP-E1001-18)** | `is_personal`; T-E1001-14, -17 are ready on `ASM-E1001-14`; the merge waits for the human ruling (TASK-19, OPEN-NEW-7) |
| CLAR-013 | RESOLVED | Repeat is 409 MSG-P1-011; T-E1001-10 |

No clarification is converted into a silent assumption: CLAR-011 and CLAR-012 remain open on labelled
assumptions, and CLAR-009 remains open and non-blocking.

## 7. NFR evidence

| NFR | Test(s) | Evidence |
|---|---|---|
| NFR-RWB-005 Security | T-E1001-11, -27; TASK-18 | 403 MSG-P4-002; audit line; migration as `rwb_migrator`; no `GRANT`; no `public` constraint |
| NFR-RWB-006 Privacy | T-E1001-14, -17; TASK-18 | 526 marks as literals; synthetic UUIDs; no PII in fixtures or logs (`ASM-E1001-14`, Blocker = Yes) |
| NFR-RWB-008 Observability | T-E1001-04, -11 | The failing statement is in the Flyway log; the refusal is in the REFUSED audit line |
| NFR-RWB-009 Operability | T-E1001-15, -16, -27, -33 | Flag-off previous path; S1–S3; forward-only migration; release note |
| NFR-RWB-001..004, -007, -010 | TASK-18 (exclusion) | No runtime read path with a target, no screen and no retained record class in this story |

## 8. Exit criteria and human verification

Unit exit: `./gradlew test` green and `recoveryCoverageVerification` at 80 × 4 (TASK-15). System exit:
`./gradlew recoveryIntegrationTest` green (TASK-16). Merge exit: `./scripts/dev.ps1 test` and
`./scripts/dev.ps1 e2e` green (TASK-17), TASK-18 complete, TASK-19 satisfied.

| Human item | Owner | Status |
|---|---|---|
| The human ruling on GAP-E1001-17 (DP07 width) and GAP-E1001-18 (`is_personal` set) is recorded before the merge | Data architect; data architect with the DPO | OPEN — blocking the merge, not the branch; OPEN-NEW-6, -7 |
| The DEV/SIT catalog files carry a real owner user ID per product | RW-DATASTEW / RW-REFADM | OPEN — outside the repository; tests use synthetic UUIDs |
| D-RUN-12, D-RUN-18 and D-RUN-21 are ratified | Recovery tech lead | OPEN — OPEN-050 |
| RWB-E1-039 adds the persistent access-log assertion | RWB-E1-039 owner | OPEN, later story |
| The TE-011 PDPA lint reports zero findings once both are merged | RWB-TE-011 owner | Conditional — never waived |
