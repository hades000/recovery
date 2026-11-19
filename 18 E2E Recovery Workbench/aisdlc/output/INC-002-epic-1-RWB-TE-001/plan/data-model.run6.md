---
title: "Data model: RWB-TE-001"
run_id: "INC-002-epic-1-RWB-TE-001"
revision: "v6 (18 Nov 2026): plan gate round 5 findings PLAN-021..022 fixed; v5 kept as *.run5.md, v4 as *.run4.md, v3 as *.run3.md, v2 as *.run2.md, v1 as *.run1.md"
---

# Data model: RWB-TE-001

No database change. No table, column, view, migration or persisted record is added or changed (D-RUN-07 not exercised). The "data" of this story is the module map, the package declarations, the fixture worlds, the failure texts and the four configuration records. No field holds personal data.

## 1. Module map (`backend/src/test/resources/architecture/recovery-modules.yaml`)

Schema and initial content: `../specify/contracts/backend-apis.json` `CON-RWB-TE-001-001` (spec v4), used unchanged. Java model in `ModuleMap.java` (test scope):

| Record | Components | Source key |
|---|---|---|
| `ModuleMap` | `String source` (file name, for error text), `String rootPackage`, `List<Module> modules`, `List<External> external`, `List<String> clientLibraries`, `Object sourceViews` (raw, may be `null`) | top level |
| `Module` | `String code`, `String name`, `List<String> published`, `List<String> clientPackages` | `modules[i]` |
| `External` | `String name`, `String rootPackage`, `List<String> published` | `external[i]` |

Derived values (methods, no stored state): module package `rootPackage + "." + name`; published package `modulePackage + "." + entry`; client package `modulePackage + "." + entry`; `moduleOf(pkg)` returns the module whose package equals `pkg` or is a prefix followed by `.`.

Initial published lists (SPEC-025): `integration` `[api, flags.api]`; `casewf` `[api, rules, timers, workflow]`; every other module `[api]`. Client packages: `integration` `[adapter]`, `dochub` `[storage]`, `agent` `[client]`. External: `common` and `collection`, each `[api]`. 16 client libraries as the contract.

## 2. Package declarations (main code, SPEC-001)

| Package (under `th.co.scb.ace.demo.recovery`) | `package-info.java` content | Count |
|---|---|---|
| root (existing) | `@ApplicationModule(displayName = "Recovery")`, unchanged | 1 (kept) |
| `<name>` for each of the 19 modules | `@ApplicationModule` | 19 |
| `<name>.api` | `@NamedInterface(name = "api", propagate = false)` | 19 |
| `<name>.internal` | Javadoc only, no annotation (no class file is produced; PA-03) | 19 |
| `casewf.rules`, `casewf.timers`, `casewf.workflow` | `@NamedInterface(name = "rules" / "timers" / "workflow", propagate = false)` | 3 |
| `integration.flags.api` | `@NamedInterface(name = "flags.api", propagate = false)` | 1 |
| `casewf.workflow.internal`, `casewf.timers.internal`, `casewf.admin`, `casewf.migration`, `integration.flags`, `access.internal`, `dochub.storage` | none (packages hold only relocated classes) | 0 |

New: 61. Deleted: the 8 `package-info.java` of `platform`, `platform.api`, `rules`, `rules.api`, `workflow`, `workflow.api`, `documents`, `documents.api`. Module codes are not annotation values; the map holds them (BR6).

## 3. Fixture worlds (test scope, SPEC-011)

Root `th.co.scb.ace.boundaryfixture` (PA-01). Each world `W` has `W.recovery` (fixture recovery root), and where needed `W.collection`, `W.common`. Fixture map `backend/src/test/resources/architecture/fixtures/<world>.yaml` has `rootPackage: th.co.scb.ace.boundaryfixture.<world>.recovery`, `external` common and collection at `…<world>.common` / `…<world>.collection` with `published: [api]`, and only the modules the world needs. Every module base package has `package-info.java` with `@ApplicationModule`; every published package `@NamedInterface(name = <entry>, propagate = false)` unless stated. Paths below are relative to `<world>.recovery` unless they start with `collection`, `common` or another top-level fixture package.

| World | Map modules (code name: published / client) | Classes and what each shows | Expected |
|---|---|---|---|
| `passing` | P2 integration: api / adapter; P3 casewf: api, workflow / —; P7 decision: api / — | `casewf.internal.SampleService` calls interface `common.api.CustomerLookup` (AC2); `casewf.internal.RecoveryCaseEntity` (`@Entity`) and `casewf.internal.RecoveryCaseRepository extends Repository<RecoveryCaseEntity, Long>` used by `casewf.internal.CaseLoader` (same module); `integration.adapter.PartnerHttpAdapter` with `java.net.http.HttpClient` and `com.azure.storage.blob.BlobClient` fields (AC5 passing half); `casewf.CaseModuleSupport` package-private in a base package; `casewf.workflow.WorkflowPort` (published interface); `casewf.workflow.internal.WorkflowRunner` public in an unlisted sub-package of a published package | Every rule passes (MAP, BND-1, -2, -4, -5) |
| `bnd1` | P3 casewf: api | `casewf.internal.SampleService` and `casewf.internal.SampleReport` each have a field of type `collection.internal.CollectorRepository` (plain class); `collection.api.CollectorLookup` exists | BND-1: two lines, one per class (AC1, T-TE001-04) |
| `bnd2` | P3 casewf: api | `casewf.internal.SampleService` uses `common.internal.CustomerCache` | BND-2: one line |
| `bnd4` | P2 integration: api; P3 casewf: api | `casewf.internal.RecoveryCaseEntity` (`@Entity`), `casewf.internal.RecoveryCaseRepository extends Repository<…>`; `integration.internal.CaseExportJob` uses both; `integration.internal.LegacyLoanReader` uses `collection.internal.CollectorEntity` (`@Entity`, outside the recovery root, under the external `collection` root); `integration.internal.ArchiveReader` uses `th.co.scb.ace.boundaryfixture.bnd4.legacy.ArchivedLoanEntity` (`@Entity`, outside every map module and every external root) | BND-4: exactly four lines (AC4, the external-root entity, and `ArchiveReader` → `ArchivedLoanEntity` ending `Use th.co.scb.ace.boundaryfixture.bnd4.legacy.api or an application event.`, the target-package convention); none for `RecoveryCaseRepository` → Spring Data `Repository` |
| `bnd5` | listed in this order: P10 agent: api / client; P3 casewf: api; P2 integration: api / adapter (P2 is last and another module's client package comes first, so the test shows the BND-5 text does not depend on map order) | `clientLibraries` of the fixture map: `java.net.http`, `java.net.URL`, `com.azure.storage`, `th.co.scb.ace.boundaryfixture.bnd5.vendor.VendorClient`. `casewf.internal.SampleService` with `HttpClient` field; `casewf.internal.BlobUser` with `BlobClient` field; `casewf.internal.UrlHelper` uses `java.net.URLEncoder`, `java.net.SocketTimeoutException`, `java.net.URI`, `java.net.URL`; `casewf.internal.VendorUser` uses nested `vendor.VendorClient$Session`; `integration.adapter.PartnerHttpAdapter` with `HttpClient` and `BlobClient` | exactly four BND-5 lines, each ending `Use integration.api or an application event.`: `SampleService` → `HttpClient`, `BlobUser` → `BlobClient`, `UrlHelper` → `java.net.URL`, `VendorUser` → `VendorClient$Session`; no line for `URLEncoder`, `SocketTimeoutException`, `URI` or `PartnerHttpAdapter` (AC5, T-TE001-09) |
| `bnd5` with `bnd5-nop2.yaml` | P10 agent: api / client; P3 casewf: api (no P2) | the `bnd5` classes, evaluated against this second map | exactly six BND-5 lines: the four `casewf` origins of AC5 (`SampleService` → `java.net.http.HttpClient`, `BlobUser` → `com.azure.storage.blob.BlobClient`, `UrlHelper` → `java.net.URL`, `VendorUser` → `…bnd5.vendor.VendorClient$Session`), each ending `Use casewf.api or an application event.` (no P2: the origin's own module), and two `integration.adapter.PartnerHttpAdapter` lines (→ `java.net.http.HttpClient`, → `com.azure.storage.blob.BlobClient`), each ending `Use th.co.scb.ace.boundaryfixture.bnd5.recovery.integration.adapter.api or an application event.` (`integration` is in no module of this map, so the origin's package fills `{module}`) |
| `vendorx` | P3 casewf: api | `vendorx.VendorFeed` (package not in the map); no class under `collection` or `common` | MAP: `package th.co.scb.ace.boundaryfixture.vendorx.recovery.vendorx is not in the module map` (AC7); BND-1 and BND-2 pass with no external classes (T-TE001-03) |
| `mapbad` | P3 casewf: api, events, timers; P7 decision: api; P8 payments: api (no package) | (1) no `payments` package; (2) `RootHelper` in the root package; (3) `casewf.spi` has `@NamedInterface(name = "spi", propagate = false)` but is not listed; (4) `casewf.events.CaseEvent` exists, `casewf.events` has no `@NamedInterface`; (5) `tools.gen.Generator` only (no class directly in `tools`); (6) `casewf.CaseFacade` public in a base package; (7) `casewf.internal.ExposedHelper` has type-level `@NamedInterface`; (8) `casewf.timers` has `@NamedInterface(name = "timers")` with `propagate` at its default (the one fixture that keeps the default, R3-4) | MAP: exactly eight lines, texts 1–8 of §4 |
| `bnd3fail` | no map (Modulith only) | `recovery` `@ApplicationModule`; nested `recovery.integration` and `recovery.decision` `@ApplicationModule` (R2-5); `decision.writer.DecisionLogWriter` (`@NamedInterface(name = "writer", propagate = false)`); `decision.internal.DecisionLogRepository`; `integration.internal.CaseSync` uses `DecisionLogRepository` | `verify()` throws; message names `DecisionLogRepository` (AC3) |
| `bnd3pass` | P2 integration: api; P7 decision: api, writer | As `bnd3fail`, but `CaseSync` uses `DecisionLogWriter` | `verify()` passes; MAP passes on the same classes (published list equals `@NamedInterface`, BR6) |
| `bnd3cycle` | no map | As `bnd3pass`, plus `integration.api.CaseEvents` (`@NamedInterface(name = "api", propagate = false)`) used by `decision.internal.DecisionLogService` | `verify()` throws on the cycle `integration` → `decision` → `integration` (D-RCV-11, T-TE001-16) |

The real `RecoveryBoundaryTest` and `ModulithTest` never see these classes: `ClassFileImporter` with `DO_NOT_INCLUDE_TESTS` on `th.co.scb.ace.demo.recovery`, and `ApplicationModules.of(AceRecoveryApplication.class)` on `th.co.scb.ace.demo`. Fixture field types are only declarations; no fixture is instantiated, so no network or storage call happens.

## 4. Failure texts (build log, SPEC-004, SPEC-010)

`{class}` and `{dependency}` are fully qualified class names (nested with `$`); `{package}` a fully qualified package (ASM-08). **Violation:** for BND-1, -2, -4 and -5, one distinct (origin class, target class) pair per rule; several accesses from one class to the same target (field, call, parameter) give one line, and a nested origin class counts as its own class. For the module-map rule, one distinct (check, package or class) pair. Each violation gives exactly one line; all lines of a rule come from one evaluation. The line counts in `tests/scenarios.md` use this definition. For BND-4, the Spring Data types in `org.springframework.data..` are not themselves repositories (a fixture repository extending `Repository` raises nothing).

| # | Rule | Text | Source |
|---|---|---|---|
| — | BND-1, -2, -4 | `Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event.` with `{module}` the target's map or external name; for a target under no map module and no external root, `{module}` is the target's package (PA-04) | SPEC-010 |
| — | BND-5 | same template; `{module}` is the name of the map module with code `P2` (the integration module: outbound data leaves through the integration adapters, AGENTS.md v2 §4 rule 3), so the line reads `… Use integration.api or an application event.`; a map with no `P2` module prints the origin class's own module name, and an origin class in no map module prints the origin's package (the BND-4 convention for a target outside every module). The value does not depend on the order of the map. Tested: the P2 value by `clientLibraryOutsideClientPackageBreaksBnd5` (`bnd5`), and both fallbacks by `bnd5TextWithoutP2UsesTheOriginModule` (`bnd5-nop2`: four origin-module lines and two origin-package lines, exact count). The target-package convention of BND-1, -2 and -4 is tested by the `bnd4` line for `ArchivedLoanEntity`; BND-1 and BND-2 select targets under an external root only, so the package value can occur only in BND-4 and BND-5 (PA-04) | SPEC-010 |
| 1 | MAP (b) | `module {name} ({code}) in the module map has no package {package}` | SPEC-004 (b); text PA-04 |
| 2 | MAP (c) | `type {class} in root package {package}; only package-info is allowed` | SPEC-004 (c); text PA-04 |
| 3 | MAP (d) | `package {package} has @NamedInterface but is not in the published list of module {name}` | SPEC-004 (d); text PA-04 |
| 4 | MAP (d) | `published package {package} of module {name} has no @NamedInterface` | SPEC-004 (d); text PA-04 |
| 5 | MAP (a) | `package {package} is not in the module map` | SPEC-004 (a) |
| 6 | MAP (e) | `public type {class} in module base package {package}; move it to a published package or internal` | SPEC-004 (e) |
| 7 | MAP (f) | `type-level @NamedInterface on {class}; declare published packages in package-info and the module map` | SPEC-004 (f) |
| 8 | MAP (d) | `@NamedInterface on {package} must declare propagate = false; list each published sub-package in the module map` | SPEC-004 (d) |
| — | Loader | `{file}: {fieldPath}: {problem}`, for example `recovery-modules.yaml: modules[2].code: duplicate value P3` | SPEC-003; PA-04 |
| — | BND-3 | Spring Modulith's own text (D-RCV-42) | SPEC-007 |

## 5. Configuration records (SPEC-023)

Keys and defaults are those of `backend/src/main/resources/application.yaml` today; no key is added, renamed or removed.

| Record (pp) | Prefix | Components | Default from `application.yaml` (placeholder default) |
|---|---|---|---|
| `integration.flags.RecoveryFlagProperties` | `rwb.p3` | `boolean temporal`, `boolean drools` | `false`, `false` |
| `integration.internal.PlatformInfoProperties` | `rwb` | `String environment`, `String schema` | `DEV`, `recovery` |
| `casewf.migration.RecoveryMigrationProperties` | `rwb` | `String schema`, `Flyway flyway(boolean enabled, String url, String user, String password, String location)` | `recovery`; `true`, `jdbc:postgresql://localhost:5433/ace`, `rwb_migrator`, empty, `classpath:db/modulemigration/recovery` |
| `access.internal.RecoverySecurityProperties` | `rwb.security` | `String issuer`, `String jwkSetUri`, `String audience`, `String rolesClaim`, `List<String> corsOrigins` | `http://localhost:8090/entra`, `http://localhost:8090/entra/jwks`, `api://rwb-recovery`, `roles`, `[http://localhost:5173]` |

These are the placeholder defaults in `application.yaml` on 18 Nov 2026 (local stand-ins, no secret; `password` is empty). They are the values `RecoveryProperties` binds today, so T-TE001-12 asserting them shows the split binds the same keys. The tests read them on an environment with no system environment or system-property source (`plan.md` "Binding isolated from the process environment"), so the values hold under `./scripts/dev.ps1 test`, which imports `.env` (where `.env.example` sets both flags `true` and a migrator password). `DroolsProperties` (`rwb.drools.kiebase-cache-max`, default 20) and `TemporalProperties` (`rwb.temporal.*`) are unchanged by the split.
