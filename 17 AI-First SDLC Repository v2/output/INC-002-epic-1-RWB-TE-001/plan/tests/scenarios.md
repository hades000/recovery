# Test scenarios — RWB-TE-001

Acceptance is the story business rules plus its test cases (D-RCV-16, TS-RCV-7). All scenarios are unit or build level. API Tester and Functional Automation Test: `NOT_APPLICABLE` (API NO, UI NO). Human verification gaps HV-1, HV-2 are in `plan.md` §Functional Test Scenarios.

| ID | Covers | Level | Test class / command | Data (synthetic) | Expected | TASK |
|---|---|---|---|---|---|---|
| TC-TE-001-01 | BR1, X-B1 | Unit (fixture) | `RecoveryBoundaryRulesTest` | Fixture recovery class → collection non-published class | BND-1 fails; text names both classes | 07, 08 |
| TC-TE-001-02 | BR2 | Unit (fixture) | `RecoveryBoundaryRulesTest` | Fixture class → common `api` interface; plus breaking case → common non-published (X-B2) | Passing case passes; breaking case fails BND-2 | 07, 08 |
| TC-TE-001-03 | BR3, X-B3, Flow 8 | Unit (fixture) | `RecoveryModulithFixtureTest` | `bnd3.broken`: module imports another's `internal`; `bnd3.fixed`: `writer` package `@NamedInterface` and in fixture map; `bnd3.cycle`: `a.api` ↔ `b.api`; all three copy the real nested-module layout | Nested modules detected by name first; `verify()` fails on `broken` (Modulith text) and on `cycle`; passes on `fixed` | 07, 09 |
| TC-TE-001-04 | BR4, X-B4 | Unit (fixture) | `RecoveryBoundaryRulesTest` | Other recovery module `@Entity` + repository; `@Entity` outside fixture root; own-module entity | First two fail BND-4; own-module passes | 07, 08 |
| TC-TE-001-05 | BR5, X-B5 | Unit (fixture) | `RecoveryBoundaryRulesTest` | `java.net.http.HttpClient`, `com.azure.storage` type in `casewf` and in `integration.adapter` | Fails in `casewf`; passes in `integration.adapter` | 07, 08 |
| TC-TE-001-07 | BR6, X-B6 | Unit (fixture) | `RecoveryBoundaryRulesTest` | Package `vendorx` absent from fixture map | Fails: `package … vendorx is not in the module map` | 07, 08 |
| T-TE001-01 | SPEC-003, X-B7 | Unit | `ModuleMapLoaderTest` | Valid map; missing file; invalid YAML; missing field; duplicate code; duplicate name; bad pattern; `internal` published; unknown field; missing external | One pass; each error names file and field | 04, 05 |
| T-TE001-02 | SPEC-004 (a)–(f) | Unit (fixture) | `RecoveryBoundaryRulesTest` | Map module without package; class in root; `@NamedInterface` package not in map; published package without annotation; classes only in sub-package of unmapped package; public class in base package; type-level `@NamedInterface` | Each fails with its SPEC-004 text; non-public base-package class passes | 07, 08 |
| T-TE001-03 | SPEC-005, -006, CLAR-011 | Unit (fixture) | `RecoveryBoundaryRulesTest` | Fixture map whose common/collection roots have no classes | Rules pass (`allowEmptyShould`) | 07, 08 |
| T-TE001-04 | SPEC-010, Flow 7 | Unit (fixture) | `RecoveryBoundaryRulesTest` | Two violations of one rule | Both reported in one run; exact SPEC-010 text | 07, 08 |
| T-TE001-05 | SPEC-001, -004, -012 | Unit | `RecoveryBoundaryTest` | Real main classes, real map | Passes | 02, 10 |
| T-TE001-06 | SPEC-018 | Build | `./gradlew checkstyleMain checkstyleTest test` | Whole ACE suite | Checkstyle clean; green, incl. `ModulithTest`; second run same result | 12 |
| T-TE001-07 | SPEC-014, -015, X-F1 | Unit (Vitest) | `importBoundary.test.ts` | `forbidden.ts` (11 imports, incl. `./../x`, `./sub/../../x`, `@/modules/recovery/../cfsc/x`, bare `..`), `allowed.ts` (7 imports) | One `no-restricted-imports` error per forbidden line; none in allowed | 14, 15, 16 |
| T-TE001-08 | SPEC-013..-015, -018, -020 | Build | `npx nx run frontend:check` | — | Green on two consecutive runs; fixtures not linted/compiled/bundled; no HTML/JS in coverage folder (`lcovonly`); coverage `PASS`, 0/0 recorded as printed | 17 |
| T-TE001-09 | SPEC-009 | Unit (fixture) | `RecoveryBoundaryRulesTest` | `casewf` uses `java.net.URLEncoder`, `java.net.SocketTimeoutException`, `java.net.URL`, nested class of a listed class | First two pass; last two fail BND-5 | 07, 08 |
| T-TE001-10 | SPEC-020 | Build | `./gradlew recoveryCoverageReport recoveryCoverageVerification` after `test` | — | Report covers `ModuleMapLoader`, `ModuleMap`, `RecoveryBoundaryRules`; 80% LINE/INSTRUCTION/BRANCH/METHOD pass | 11, 12 |

TC-TE-001-06 does not exist in the story and is not used. TC-TE-001-08 moved to RWB-E1-022 (D-RCV-52).
