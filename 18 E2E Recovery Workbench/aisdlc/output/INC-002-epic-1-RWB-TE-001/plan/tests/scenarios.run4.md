---
title: "Test scenarios: RWB-TE-001"
run_id: "INC-002-epic-1-RWB-TE-001"
revision: "v4 (18 Nov 2026): plan gate round 3 findings PLAN-012..016 fixed; v3 kept as *.run3.md, v2 as *.run2.md, v1 as *.run1.md"
---

# Test scenarios: RWB-TE-001

Every acceptance criterion, business rule, SPEC requirement and spec test ID maps to a named test below. Test paths: `T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`; fixture worlds as `../data-model.md` §3; texts as §4. All backend tests are JUnit 5, untagged, in the `test` task; the frontend test runs in `npm run check`. Data is synthetic: class and package names, local placeholder defaults, generated keys. No test is skipped, disabled or weakened.

T-TE001-15 and T-TE001-16 are plan-level additions (PA-08), requested for the spec test list in `../shared-updates.md` SU-P01.

## 1. Acceptance criteria (story file v7 RWB-TE-001 v1 §7)

| AC | Spec test | Named test (class.method) | World / input | Expected | Task |
|---|---|---|---|---|---|
| AC1 | TC-TE-001-01 | `BoundaryRulesTest.collectionInternalDependencyBreaksBnd1` | `bnd1` | Two lines; one is `Rule BND-1 broken: th.co.scb.ace.boundaryfixture.bnd1.recovery.casewf.internal.SampleService depends on th.co.scb.ace.boundaryfixture.bnd1.collection.internal.CollectorRepository. Use collection.api or an application event.` | TASK-06, -07 |
| AC2 | TC-TE-001-02 | `BoundaryRulesTest.commonApiDependencyPassesEveryRule` | `passing` | MAP, BND-1, -2, -4, -5 report no violation | TASK-06, -07 |
| AC3 | TC-TE-001-03 | `ModulithFixtureTest.internalDependencyBetweenModulesFailsVerify`; `ModulithFixtureTest.publishedWriterDependencyPassesVerify` | `bnd3fail`; `bnd3pass` | `verify()` throws, message names `DecisionLogRepository` (Modulith text, D-RCV-42); `verify()` passes | TASK-08 |
| AC3 (map side) | TC-TE-001-03 | `BoundaryRulesTest.publishedWriterMatchesTheFixtureMap` | `bnd3pass` | MAP passes: `decision.writer` listed and annotated (BR6) | TASK-06, -07 |
| AC4 | TC-TE-001-04 | `BoundaryRulesTest.foreignEntityAndRepositoryBreakBnd4` | `bnd4` | Exactly four BND-4 lines (none for `RecoveryCaseRepository` → Spring Data `Repository`): `CaseExportJob` → `RecoveryCaseEntity` (`Use casewf.api …`), `CaseExportJob` → `RecoveryCaseRepository`, `LegacyLoanReader` → `CollectorEntity` (`Use collection.api …`), `ArchiveReader` → `ArchivedLoanEntity` (`Use th.co.scb.ace.boundaryfixture.bnd4.legacy.api or an application event.`, target outside every module and external root) | TASK-06, -07 |
| AC5 | TC-TE-001-05 | `BoundaryRulesTest.clientLibraryOutsideClientPackageBreaksBnd5` | `bnd5` | Exactly four BND-5 lines (`data-model.md` §4 violation definition), each ending `Use integration.api or an application event.` although P2 is listed last in the fixture map: `SampleService` → `java.net.http.HttpClient`, `BlobUser` → `com.azure.storage.blob.BlobClient`, `UrlHelper` → `java.net.URL`, `VendorUser` → `…bnd5.vendor.VendorClient$Session`; none for `integration.adapter.PartnerHttpAdapter` | TASK-06, -07 |
| AC6 | TC-TE-001-06 | `importBoundary.test.ts` › "rejects `@/modules/collection/worklist/WorkList`", "rejects `../../collection/worklist/WorkList`" | in-memory source, `src/modules/recovery/caselist/BoundaryFixture.tsx` | exactly one message with `ruleId === "no-restricted-imports"` each (D-RCV-39 deviation) | TASK-15 |
| AC7 | TC-TE-001-07 | `BoundaryRulesTest.packageMissingFromTheMapFails` | `vendorx` | One MAP line ending `recovery.vendorx is not in the module map` | TASK-06, -07 |
| X7 | TC-TE-001-08 | none (moved to RWB-E1-022, D-RCV-52) | — | TASK-18 checks it is not built | TASK-18 |

## 2. Business rules

| BR | Tests |
|---|---|
| BR1 collection boundary | TC-TE-001-01; `BoundaryRulesTest.emptyExternalRootsPass` (T-TE001-03); `BoundaryRulesTest.allViolationsOfARuleInOneRun` (T-TE001-04); `RecoveryBoundaryTest.bnd1CollectionBoundary` |
| BR2 common boundary | TC-TE-001-02; `BoundaryRulesTest.commonInternalDependencyBreaksBnd2`; T-TE001-03; `RecoveryBoundaryTest.bnd2CommonBoundary` |
| BR3 recovery to recovery | TC-TE-001-03; `ModulithFixtureTest.cycleBetweenModulesFailsVerify` (T-TE001-16); `ModulithTest.modulesRespectTheirBoundaries` (existing, unchanged); `BoundaryRulesTest.mapViolationsAreAllReported` (T-TE001-02); `RecoveryBoundaryTest.publishedSurfaceIsExactlyTheSpecifiedTypes` (T-TE001-14) |
| BR4 entities and repositories | TC-TE-001-04; `RecoveryBoundaryTest.bnd4EntitiesAndRepositoriesStayInTheirModule` |
| BR5 client libraries | TC-TE-001-05; `BoundaryRulesTest.clientLibraryMatchesOnANameBoundary` (T-TE001-09); `BoundaryRulesTest.matchesClientLibraryTable`; `RecoveryBoundaryTest.bnd5ClientLibrariesOnlyInClientPackages`; T-TE001-13 run 1 |
| BR6 map is the only source | TC-TE-001-07; `ModuleMapLoaderTest` (T-TE001-01); `BoundaryRulesTest.toolingHoldsNoRecoveryPackageLiteral` (T-TE001-15); every world runs the same `BoundaryRules.all` on its own map |

## 3. Spec test list

| Spec test | Named test(s) | Cases | Expected | Task |
|---|---|---|---|---|
| T-TE001-01 | `ModuleMapLoaderTest`: `loadsAValidMap`, `loadsTheRealMap`, `carriesSourceViewsUnvalidated`, `missingFileNamesTheFile`, `invalidYamlNamesTheFile`, `duplicateYamlKeyIsRejected`, `missingRequiredFieldNamesThePath`, `emptyPublishedIsRejected`, `duplicateCodeIsRejected`, `duplicateNameIsRejected`, `badCodePatternIsRejected`, `badNamePatternIsRejected`, `badPackagePatternIsRejected`, `internalAsPublishedIsRejected` (`internal`, `internal.x`), `unknownTopLevelKeyIsRejected`, `unknownNestedKeyIsRejected`, `externalMustBeCommonAndCollection`, `clientLibrariesMustBeNonEmptyAndUnique` | inline YAML in `@TempDir`; real map | valid ones load (real map: 19 modules, published lists of `data-model.md` §1; `sourceViews` returned as given); each error message starts with the file name and contains the field path | TASK-03, -04 |
| T-TE001-02 | `BoundaryRulesTest.mapViolationsAreAllReported`; `BoundaryRulesTest.mapRuleAcceptsPackagePrivateBaseTypeAndUnlistedSubPackage` | `mapbad` (8 cases of `data-model.md` §3); `passing` | exactly texts 1–8 of §4, one each; `passing`: `casewf.CaseModuleSupport` (package-private) and `casewf.workflow.internal.WorkflowRunner` (public, unlisted sub-package) raise nothing | TASK-06, -07 |
| T-TE001-03 | `BoundaryRulesTest.emptyExternalRootsPass` | `vendorx` (no collection or common classes) | BND-1 and BND-2 pass (`allowEmptyShould(true)`) | TASK-06, -07 |
| T-TE001-04 | `BoundaryRulesTest.allViolationsOfARuleInOneRun` | `bnd1` | both lines (`SampleService`, `SampleReport`) in one `EvaluationResult` | TASK-06, -07 |
| T-TE001-05 | `RecoveryBoundaryTest`: `moduleMapRule`, `bnd1CollectionBoundary`, `bnd2CommonBoundary`, `bnd4EntitiesAndRepositoriesStayInTheirModule`, `bnd5ClientLibrariesOnlyInClientPackages`, `everyMapModuleHasApiAndInternalPackageInfo`, `workflowImplementationsAreDeterministic` (retargeted), `determinismRuleSelectsTheSmokeWorkflowImpl` (guard: the selection includes `PlatformSmokeWorkflow$Impl`), `noRecoveryClassNamesAPublicTable` (unchanged) | real main classes, real map | all pass after TASK-11; red before (TASK-09 evidence) | TASK-09, -11 |
| T-TE001-06 | `./gradlew test` (whole suite incl. `ModulithTest`, `RecoveryMigrationLintTest`, moved tests); old-package search | — | exit 0; the search of `../tasks.md` note N-1 finds nothing | TASK-13 |
| T-TE001-07 | `importBoundary.test.ts`: 8 "rejects …" cases, 7 "allows …" cases | SPEC-015 sets | rejected: one `no-restricted-imports` message each; allowed: none | TASK-15 |
| T-TE001-08 | `npm run check`; `npm run build` | — | exit 0; coverage ≥ 80 on lines, statements, branches, functions | TASK-16 |
| SPEC-010 fallback (plan) | `BoundaryRulesTest.bnd5TextWithoutP2UsesTheOriginModule` | `bnd5` classes with map `bnd5-nop2.yaml` (no P2) | exactly six BND-5 lines: the four `casewf` origins of AC5 (`SampleService` → `java.net.http.HttpClient`, `BlobUser` → `com.azure.storage.blob.BlobClient`, `UrlHelper` → `java.net.URL`, `VendorUser` → `…bnd5.vendor.VendorClient$Session`), each ending `Use casewf.api or an application event.` (no P2: the origin's own module), and two `integration.adapter.PartnerHttpAdapter` lines (→ `java.net.http.HttpClient`, → `com.azure.storage.blob.BlobClient`), each ending `Use th.co.scb.ace.boundaryfixture.bnd5.recovery.integration.adapter.api or an application event.` (`integration` is in no module of this map, so the origin's package fills `{module}`) | TASK-06, -07 |
| T-TE001-09 | `BoundaryRulesTest.clientLibraryMatchesOnANameBoundary`; `BoundaryRulesTest.matchesClientLibraryTable` | `bnd5` `UrlHelper`, `VendorUser`; table of (entry, name, expected) incl. `java.net.URL`/`java.net.URLEncoder` false, `java.net.URL`/`java.net.URL` true, `java.net.http`/`java.net.http.HttpClient` true, `…VendorClient`/`…VendorClient$Session` true, `java.net.Socket`/`java.net.SocketTimeoutException` false | `URLEncoder`, `SocketTimeoutException`, `URI` pass; `java.net.URL` and `VendorClient$Session` fail | TASK-06, -07 |
| T-TE001-10 | `./gradlew test recoveryCoverageVerification` | — | exit 0; LINE, INSTRUCTION, BRANCH, METHOD each ≥ 0.80 over recovery main classes plus tooling | TASK-01 (red), TASK-13 (green) |
| T-TE001-11 | `./gradlew recoveryIntegrationTest` (`RecoveryDatabaseIT`); `./gradlew e2eTest` (`PlatformE2ETest`) | Docker; local stack | exit 0; `/platform/info`, `/admin/temporal/health`, smoke answer as before | TASK-14 |
| T-TE001-12 | `PlatformConfigTest.bindsFlagsFromApplicationYaml`; `PlatformInfoControllerTest.bindsEnvironmentAndSchemaFromApplicationYaml`; `RecoveryFlywayConfigTest.bindsSchemaAndFlywayFromApplicationYaml`; `SecurityConfigTest.bindsSecurityFromApplicationYaml`; `DroolsPropertiesTest.bindsCacheMaxFromApplicationYaml` | `application.yaml` on `ApplicationYamlEnvironment.isolated()` (no system environment or system-property source, so `.env` imported by `dev.ps1` cannot change the result; `plan.md` "Binding isolated from the process environment") | the `application.yaml` placeholder defaults of `data-model.md` §5, under both `./gradlew test` (TASK-13) and `./scripts/dev.ps1 test` (TASK-17 Run 3) (`temporal=false`, `drools=false`; `DEV`, `recovery`; flyway `true`, `jdbc:postgresql://localhost:5433/ace`, `rwb_migrator`, empty password, `classpath:db/modulemigration/recovery`; security issuer, JWKS URI, audience, `roles`, `[http://localhost:5173]`; cache max 20) | TASK-10 (red), TASK-11 (green) |
| T-TE001-13 | Negative control, three runs of `powershell -NoProfile -File scripts/dev.ps1 test` | probes of `tasks.md` TASK-17 | Run 1 exit ≠ 0, with the BND-5 line for `BoundaryProbe` quoted from the JUnit XML report `backend/build/test-results/test/TEST-th.co.scb.ace.demo.recovery.architecture.RecoveryBoundaryTest.xml` (with default Gradle test logging the console shows only the failed test name); Run 2 exit ≠ 0 with `no-restricted-imports` on `BoundaryProbe.tsx`; Run 3 exit 0 with `.env` imported by `dev.ps1` (created from `.env.example` if missing) and the five T-TE001-12 methods passed in the JUnit XML; no probe committed | TASK-17 |
| T-TE001-14 | `RecoveryBoundaryTest.publishedSurfaceIsExactlyTheSpecifiedTypes` | real main classes; `ApplicationModules.of(AceRecoveryApplication.class)` | (a) public top-level and nested types per published package equal `contracts/backend-apis.json` `publishedJavaTypesAfterRelocation`; (b) for module `casewf`, the named interfaces with `!isUnnamed()` have names within `{api, rules, timers, workflow}` and include `rules`, `timers`, `workflow` (R3-1, PA-05); (c) no type of those named interfaces is in `casewf.workflow.internal` or `casewf.timers.internal`. Each list is exact, `access.api` included; later stories extend the exact list in their own merge request (RWB-E1-042 for the D-RUN-19 parameter read interface, `MessageResolver` and `CapabilityCheck`; RWB-E1-043 for the D-RUN-18 reference-load SPI; `shared-updates.md` SU-P02) | TASK-09, -11 |
| T-TE001-15 (plan) | `BoundaryRulesTest.toolingHoldsNoRecoveryPackageLiteral` | source files of `T/architecture/boundary/` except `*Test.java` | after the `package` line, `import` lines and comments are removed, no string literal and no annotation value contains `th.co.scb.ace.demo.recovery` (BR6, SPEC-003 "no package literal"). The scanner is checked by `BoundaryRulesTest.packageLiteralScanSeesLiteralsOnly` on inline samples: a sample with `"th.co.scb.ace.demo.recovery.casewf"` in a string literal is reported; a sample with the same name only in its `package` line, an `import` and a comment is not | TASK-06, -07 |
| T-TE001-16 (plan) | `ModulithFixtureTest.cycleBetweenModulesFailsVerify` | `bnd3cycle` | `verify()` throws on the cycle (D-RCV-11) | TASK-08 |

## 4. SPEC-024 coverage and characterization tests

Scenarios per class: `../plan.md` "Coverage tests". Named classes: `ApiErrorTest`, `ApiExceptionHandlerTest`, `SecurityConfigTest`, `PlatformConfigTest`, `PlatformInfoControllerTest`, `RecoveryFlywayConfigTest`, `TemporalAdminControllerTest`, `TemporalConfigTest`, `WorkflowIdsTest`, `BlobDocumentStoreTest`, `DroolsPropertiesTest`. They assert today's behaviour at the new homes (PA-07) and are measured by T-TE001-10. Key expectations: 401 MSG-P4-001 without a token and without an `RW-` role; 403 MSG-P4-002 on an `AccessDeniedException`; 404 MSG-P4-003; 503 MSG-P3-036 when Temporal is unavailable; legal Blob overwrite raises `DocumentImmutableException`.

## 5. SPEC to test

| SPEC | Tests |
|---|---|
| 001 | T-TE001-05 (`everyMapModuleHasApiAndInternalPackageInfo`, `moduleMapRule`) |
| 002 | T-TE001-01 (`loadsTheRealMap`), T-TE001-05 |
| 003 | T-TE001-01, T-TE001-15 |
| 004 | TC-TE-001-07, T-TE001-02, T-TE001-05 |
| 005 | TC-TE-001-01, T-TE001-03, -04 |
| 006 | TC-TE-001-02, T-TE001-03, `commonInternalDependencyBreaksBnd2` |
| 007 | TC-TE-001-03, T-TE001-16, T-TE001-06 (`ModulithTest`) |
| 008 | TC-TE-001-04 |
| 009 | TC-TE-001-05, T-TE001-09, T-TE001-05 |
| 010 | TC-TE-001-01, -04, -05, -07, T-TE001-04 (exact text asserted); `bnd5TextWithoutP2UsesTheOriginModule` (both BND-5 fallbacks); TC-TE-001-04 `ArchivedLoanEntity` line (target-package convention) |
| 011 | every fixture test above |
| 012 | T-TE001-13; HV-01 (human, not tested) |
| 013 | T-TE001-08 |
| 014 | T-TE001-07 |
| 015 | TC-TE-001-06, T-TE001-07 |
| 016 | TASK-18 scope check (not a test) |
| 017 | TASK-18 dependency check (not a test) |
| 018 | T-TE001-06, -08, -11 |
| 019 | TASK-18 guardrail review of fixtures, maps and texts |
| 020 | T-TE001-08, -10 |
| 021 | withdrawn; `noRecoveryClassNamesAPublicTable` kept unchanged |
| 022 | T-TE001-05, -06, -11, -14 |
| 023 | T-TE001-12 |
| 024 | T-TE001-10 with §4 classes |
| 025 | T-TE001-05, -14 |
| 026 | T-TE001-05 |

## 6. Human verification

| ID | Item | Why not tested here |
|---|---|---|
| HV-01 | GitLab blocks a merge request whose pipeline fails (project setting "Pipelines must succeed") | No GitLab connection in this run (RUN-BRIEF rule 5); open item SU-13 of the spec. Never reported as tested. |
