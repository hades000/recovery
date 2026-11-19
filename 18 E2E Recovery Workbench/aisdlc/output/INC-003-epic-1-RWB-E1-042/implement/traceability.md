# Traceability: CODE units to tasks, SPEC and requirements

Run `INC-003-epic-1-RWB-E1-042`. `CODE-nn` is one implementation unit (a file group); `TASK-nn` the
plan task that created it; `SPEC-nnn` the spec section; `REQ` the requirement-logic rows of
`specify/spec.md` that the unit serves; `TC` the test cases of `plan/tests/scenarios.md`.

| CODE | Unit | TASK | SPEC | REQ | TC |
|---|---|---|---|---|---|
| CODE-01 | `casewf/config/CsvRows.java` | 02, 19 | 003, 012 | BR2, BR3 | TC-41, TC-05..-07 |
| CODE-02 | `architecture/parameters/JavaLiteralTokenizer.java`, `MagicNumberScanner.java` | 02 | 004 | AC2, BR1, GR1 | TC-02, TC-25, TC-43 |
| CODE-03 | `architecture/parameters/CatalogFileParser.java`, `CatalogRow.java` | 02 | 003, 005 | BR2, BR6 | TC-41, TC-44 |
| CODE-04 | `main/resources/config/parameter-catalog.csv` | 03 | 003, 005, 024 | BR1, BR2, FL1 | TC-41, TC-42, TC-27 |
| CODE-05 | `architecture/parameters/CatalogCompletenessRules.java`, `MagicNumberBaseline.java`, `magic-number-baseline.csv`, fixture corpus | 04, 05 | 003, 004, 005 | AC2, AC3, BR2, BR6, GR1 | TC-02, TC-03, TC-21, TC-25, TC-44 |
| CODE-06 | `casewf/config/api/ParameterKey.java` | 07 | 005 | BR1, CON5 | TC-26, TC-42 |
| CODE-07 | `backend/build.gradle.kts` — `generateParameterKeys` | 07 | 005, 024 | BR1, CON5 | TC-42, TC-26, TC-27 |
| CODE-08 | generated `ParameterKeys` (11 constants, `all()`, `byName`) | 07 | 005 | BR1, CON5 | TC-42, TC-26 |
| CODE-09 | `casewf/config/package-info.java`, `casewf/config/api/package-info.java`, `RecoveryBoundaryTest`, `recovery-modules.yaml` | 08, 09 | 026 | GR3, CON5 | TC-45 |
| CODE-10 | `casewf/config/api/ParameterService.java`, `ParameterValue.java`, `CatalogEntry.java`, `ParameterNotInForceException.java`, `SecretNotServedException.java`, `BusinessDateProvider.java` | 09 | 007, 017, 023, 026 | BR5, CON5 | TC-01, TC-11, TC-45 |
| CODE-11 | `casewf/config/api/ParameterLoadHandler.java`, `ParameterLoadResult.java`, `ParameterVersionApproved.java` | 09 | 017, 018 | CON2..CON4, FL5 | TC-05, TC-28, TC-35 |
| CODE-12 | `access/api/MessageResolver.java`, `CapabilityCheck.java`, `CatalogParameterReader.java` | 09 | 020, 022, 026 | MSG, GR3 | TC-24, TC-45, TC-46 |
| CODE-13 | `access/api/ApiProblemException.java` (new form), `access/internal/ProblemFactory.java`, `ApiExceptionHandler.java` | 11 | 022, 025, 027 | MSG, GR2 | TC-30 |
| CODE-14 | `access/internal/FixedMessageCatalog.java` | 11 | 022 | MSG | TC-30 |
| CODE-15 | `access/internal/InterimCapabilityCheck.java`, `main/resources/access/interim-capability-grants.csv` | 13 | 020 | AUTH, X9 | TC-24 |
| CODE-16 | `db/modulemigration/recovery/V0001__rwb_e1_042_parameter_catalog_and_seed.sql` | 15 | 001, 002, 006 | BR1, FL4 | TC-13, TC-14, TC-15, TC-27 |
| CODE-17 | `casewf/config/ParameterServiceImpl.java` | 17 | 007, 008, 010, 022, 023, 024 | AC1, AC9, BR5, BR6 | TC-01, TC-09, TC-11, TC-26 |
| CODE-18 | `casewf/config/ParameterValues.java` | 17 | 005, 007 | BR1 | TC-06, TC-26 |
| CODE-19 | `casewf/config/ParameterCache.java` | 17 | 009, 018 | AC11, BR5, FL8 | TC-11, TC-28 |
| CODE-20 | `casewf/config/CatalogSource.java`, `InterimBusinessDateProvider.java` | 17 | 005, 016, 023 | BR7 | TC-04, TC-32 |
| CODE-21 | `casewf/config/ParameterCatalogController.java`, `CatalogParameterView.java` | 17 | 011, 020, 025 | AC9, CON1, FL10 | TC-09, TC-24, TC-31, TC-34 |
| CODE-22 | `casewf/config/ParameterStartupCheck.java` | 17 | 016 | AC4, BR7, X3 | TC-04, TC-32 |
| CODE-23 | `casewf/config/CatalogParameterReaderImpl.java` | 17 | 023, 026 | GR3 | TC-46 |
| CODE-24 | `casewf/config/ParameterValueEntity.java`, `ParameterValueRepository.java` | 17 | 002, 007, 011, 013..015 | CON2 | TC-13, TC-27 |
| CODE-25 | `casewf/config/ParameterLoadValidator.java` | 19 | 012, 014, 015 | AC5, AC6, AC7, BR3, BR4 | TC-05, TC-06, TC-18, TC-23, TC-36, TC-39 |
| CODE-26 | `casewf/config/ParameterContentHash.java` | 19 | 013 | BR3, AC8 | TC-16, TC-17, TC-33 |
| CODE-27 | `casewf/config/ParameterValidity.java` | 19 | 014, 015 | AC10, ST2, ST3 | TC-07, TC-10, TC-11, TC-19 |
| CODE-28 | `casewf/config/ParameterLoadHandlerImpl.java` | 19 | 012..019 | AC5..AC10, ST1..ST3, CON2..CON4 | TC-05..-07, -10, -16..-20, -28, -29, -33, -35..-40 |
| CODE-29 | `casewf/config/VersionDecisionRecorder.java`, `InterimVersionDecisionRecorder.java`, `ParameterLoadRolledBack.java` | 19 | 019, 027 | GR2 | TC-29 |
| CODE-30 | `casewf/config/ParameterSchemaLimits.java`, `main/resources/application.yaml`, `application-local.yaml` | 17, 19, 21 | 004, 014, 021 | GR1, X10 | TC-22, TC-25 |

Every row is traceable to a `TASK-*` in `plan/tasks.md`, a `SPEC-*` in `specify/spec.md` and at least
one `TC-E1-042-*` in `plan/tests/scenarios.md`.
