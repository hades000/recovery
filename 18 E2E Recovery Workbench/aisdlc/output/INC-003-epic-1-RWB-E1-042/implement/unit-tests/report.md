# Unit and build-check results (TASK-22)

Run `INC-003-epic-1-RWB-E1-042` · **figures of record: tip `25c8f94`** (code-gate round 2; see
`../code-gate-fix/README.md`).

## Results table (tip `25c8f94`)

| Surface | Changes | Unit tests | Statements (`LINE`) | Branches (`BRANCH`) | Functions (`METHOD`) | Instructions (`INSTRUCTION`) | Result |
|---|---|---|---|---|---|---|---|
| Backend | YES | REQUIRED — 388 unit and build-check tests, 0 failures, 0 skipped | 2579/2833 = **91.0 %** | 1289/1594 = **80.9 %** | 552/576 = **95.8 %** | 14045/15482 = **90.7 %** | **PASS** (all four ≥ 0.80) |
| Frontend | NO | NOT_APPLICABLE | N/A | N/A | N/A | N/A | **NOT_APPLICABLE** — story v7 §15 "No screen in this story"; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SCREENS: 0]`; `api/recovery-api-v4.yaml` and `frontend/src/api/schema.d.ts` unchanged; no file under `frontend/` changed. `npm run check` still runs in the merge gate and passes (28 tests, 91.89 % statements) to prove no regression. |

JaCoCo reports no `CLASS`/`COMPLEXITY` limits; the repository's gate is the four counters above in
one `BUNDLE` rule (`recoveryCoverageVerification`, RWB-TE-001 SPEC-020 (a)), outside `check`
(D-RCV-40).

## Commands and exit codes (tip `25c8f94`)

| Command | Exit | Evidence |
|---|---|---|
| `./gradlew clean`, then `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 test` | 0 | `implement/code-gate-fix/round2/clean.log`, `implement/code-gate-fix/round2/dev-test.log` — Gradle `test` 388 tests, 0 failures, 0 skipped; `npm run check` 28 tests passed, statements 91.89 % |
| `./gradlew recoveryCoverageVerification` | 0 | `implement/code-gate-fix/round2/coverage-verification.log`; native report copied to `implement/code-gate-fix/round2/recoveryCoverageReport.xml` |
| `./gradlew recoveryIntegrationTest` | 0 | `implement/code-gate-fix/round2/it-full.log` — 59 container tests (`ParameterConfigIT` 33 + `$FlagOff` 4, `ParameterMigrationIT` 4, `RecoveryMigrationIT` 12, `RecoveryDatabaseIT` 6), 0 failures, 0 skipped |
| counts from the native XML | — | `implement/code-gate-fix/test-and-coverage-counts.txt` |

**Superseded.** This file first recorded the TASK-22 run before the pre-merge reviews: 377 unit
tests; LINE 2543/2803 = 90.7 %, BRANCH 1267/1564 = 81.0 %, METHOD 543/572 = 95.0 %, INSTRUCTION
13845/15333 = 90.3 %; 46 container tests (`implement/backend/coverage.log`, `implement/backend/it.log`,
`implement/merge-gate.log`). The `74e4ccb` figures (386 unit, 54 container) are superseded too, and
so are the `9056ed2` figures (same unit and coverage figures, 55 container tests, `implement/code-gate-fix/*.log`).
Only the `25c8f94` figures above are of record.

The `-ExecutionPolicy Bypass` flag is needed because the workstation blocks unsigned scripts; the
policy, not the script, is the cause (recorded in `deviations.md` and the merge-gate log).

## Package rows (for information; tip `25c8f94`, same native XML)

| Package | LINE | BRANCH |
|---|---|---|
| `casewf.config` | 541/636 = 85.1 % | 262/369 = 71.0 % |
| `casewf.config.api` | 97/99 = 98.0 % | 19/26 = 73.1 % |
| `architecture.parameters` (test-scope tooling, in the bundle) | measured inside the same BUNDLE rule | — |

The bundle counters are the gate; no package is excluded, no threshold is lowered and no production
file is omitted from the denominator.

## Test classes added

Build checks: `JavaLiteralTokenizerTest`, `MagicNumberScannerTest`, `CatalogFileParserTest`,
`CatalogCompletenessCheckTest`, `RwbMagicNumberCheckTest`, `ParameterKeysGenerationTest`.
Service: `ParameterServiceTest`, `ParameterCacheTest`, `ParameterStartupCheckTest`,
`ParameterCatalogControllerTest`, `CatalogParameterReaderImplTest`, `ParameterLoadValidatorTest`,
`ParameterContentHashTest`, `ParameterValidityTest`, `ParameterLoadHandlerTest`.
Access: `ApiExceptionHandlerTest` (extended with TC-30), `MessageResolverTest`,
`InterimCapabilityCheckTest`.
Container: `ParameterMigrationIT`, `ParameterConfigIT`.

## Test-case coverage

TC-E1-042-01, -02, -03, -04, -05, -06, -07, -08, -09, -10, -11, -13, -14, -15, -16, -17, -18, -19,
-20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -38, -39,
-40, -41, -42, -43, -44, -45, -46 are executed. **TC-E1-042-12 stays Blocked** (`OI-E1-042-001`: a
live RW-PHONECOL identity from RWB-E1-022 and the PM-2026.11 matrix from RWB-E1-037); the seam it
covers runs as `ParameterCatalogControllerTest#refusalCarriesTheActionText` and
`ParameterConfigIT#readWithoutTheRightIsRefused`, and TC-12 is **not** reported as passed.
