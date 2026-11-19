# CODE to TASK, SPEC and requirement map: RWB-E1-044

| CODE | Unit | TASK | SPEC | AC / BR |
|---|---|---|---|---|
| CODE-E044-001 | `T architecture/migration/MigrationLexer.java` (one quote-aware pass, three views) | TASK-01, -02 | 007 | AC5; D-RCV-28 (2) |
| CODE-E044-002 | `T architecture/migration/ParsedMigrationFile.java` | TASK-02 | 007, 004 | — |
| CODE-E044-003 | `T architecture/migration/MigrationStatement.java` | TASK-02 | 007 | — |
| CODE-E044-004 | `T architecture/migration/LexProblem.java` | TASK-02 | 007, 004 | — |
| CODE-E044-005 | `T architecture/migration/MigrationFinding.java` (format and multiplicity) | TASK-02 | 004 | AC5, AC6 |
| CODE-E044-006 | `T architecture/migration/MigrationRule.java` + `MigrationRules.java` (one registry, 15 rules) | TASK-02, -04 | 016 | — |
| CODE-E044-007 | `T architecture/migration/FolderContext.java` | TASK-02 | 005, 010 | ASM-E044-05 |
| CODE-E044-008 | `T architecture/migration/MigrationLint.java` (list every entry, fail closed) | TASK-03, -04 | 004, 010 | AC5, AC6, AC7 |
| CODE-E044-009 | `T architecture/migration/rule/NameRule.java` | TASK-04 | 005 | AC6 |
| CODE-E044-010 | `T .../rule/UndoRule.java` | TASK-04 | 005 | AC7 |
| CODE-E044-011 | `T .../rule/RepeatableRule.java` | TASK-04 | 005 | AC7 |
| CODE-E044-012 | `T .../rule/SequenceGapRule.java` + `SequenceDuplicateRule.java` | TASK-04 | 005 | AC6 |
| CODE-E044-013 | `T .../rule/HeaderRule.java` + `HeaderMultiRule.java` | TASK-04 | 006 | AC6 |
| CODE-E044-014 | `T .../rule/KeyDuplicateRule.java` + `FixLine2Rule.java` + `FixNoBaseRule.java` | TASK-04 | 006 | AC6 |
| CODE-E044-015 | `T .../rule/SearchPathRule.java` | TASK-04 | 007 | AC5 |
| CODE-E044-016 | `T .../rule/LiteralSchemaRule.java` (single `isAllowedQualifier`, no `public` exception) | TASK-04 | 007, 016 | AC5; SEAM-E044-01 |
| CODE-E044-017 | `T .../rule/ForeignKeyOutsideRule.java` | TASK-04 | 008 | BR8 |
| CODE-E044-018 | `T .../rule/GrantRule.java` | TASK-04 | 009 | — |
| CODE-E044-019 | `T .../rule/LexRule.java` | TASK-04 | 007 | AC5 |
| CODE-E044-020 | `T architecture/migration/SchemaSnapshot.java`, `SchemaSnapshotReader.java`, `SchemaComparator.java`, `SchemaDifference.java` | TASK-05, -06 | 012 | AC2; BR7 |
| CODE-E044-021 | `R casewf/migration/MigrationPropertiesConfig.java` (unconditional registration) | TASK-07, -08 | 002 | AC3; A-17 |
| CODE-E044-022 | `R casewf/migration/RecoveryMigrationProperties.java` (`@Validated`, `@NotNull`, `@Pattern`) | TASK-07, -08 | 002 | AC3; A-17 |
| CODE-E044-023 | `R casewf/migration/RecoveryMigrationRunner.java` (MSG-P3-016 and version) | TASK-09, -10 | 003 | AC4, AC8 |
| CODE-E044-024 | `R casewf/migration/RecoveryFlywayConfig.java` (inherited settings, `validateOnMigrate(true)`, factory never migrates, runner bean) | TASK-08, -10 | 001, 002, 003 | AC1, AC3, AC4, AC7 |
| CODE-E044-025 | `backend/build.gradle.kts` (migration tooling in both JaCoCo tasks) | TASK-13 | 014 | — |
| CODE-E044-026 | `infra/postgres/init/20-grants.sql.inc`, `00-roles-and-databases.sh` (D-RUN-14 rights) | TASK-11, -12 | 017 | BR8 |
| CODE-E044-027 | `T casewf/migration/RecoveryMigrationIT.java` (one container class, T-044-10..-18) | TASK-11, -14 | 011, 012, 013, 017 | AC1..AC9 |
| CODE-E044-028 | `backend/src/test/resources/migration-lint/**` (55 folders at merge `b1d7424`; first written as 50. Orchestrator correction 19 Nov 2026, CONF-E044-08. REVIEW-001 adds 6 more) | TASK-03 | 010 | AC5, AC6 |
| CODE-E044-029 | `backend/src/test/resources/flyway-fixtures/**` | TASK-11, -14 | 011 | AC1..AC9 |
| CODE-E044-030 | `backend/src/main/resources/db/modulemigration/recovery/README.md` | TASK-16 | 015 | A-19 |
| CODE-E044-031 | `docs/stories/RWB-E1-044/story.md`, `plan.md` | TASK-16 | 015 | A-19 |

Test classes (excluded from the coverage bundle by name): `MigrationLexerTest`,
`RecoveryMigrationLintTest`, `SchemaComparatorTest`, `MigrationPropertiesConfigTest`,
`RecoveryMigrationRunnerTest`, `RecoveryMigrationIT`, and the one allowed edit to
`RecoveryFlywayConfigTest`.

No `frontend/` and no `api/` unit exists: UI In Scope NO and `NO_API_CHANGE`.
