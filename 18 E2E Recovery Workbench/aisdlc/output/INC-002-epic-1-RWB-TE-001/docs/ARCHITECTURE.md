---
title: "RWB-TE-001 Recovery module and boundary test — architecture"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED against branch tip 55f1ed4"
---

# Architecture — recovery module boundary

This document describes the structure the story builds, not a new runtime design. The recovery
module of ACE is one Spring Modulith application module (`th.co.scb.ace.demo.recovery`) that contains
19 nested design modules. Everything here is enforced at build time.

## 1. Context

| Fact | Value | Source |
|---|---|---|
| Parent service | ACE service, one repository, one front end | AGENTS.md §2; ADR v3 (ADR-002) |
| Recovery root package | `th.co.scb.ace.demo.recovery` | D-RCV-02 |
| Design modules | 19: `P1..P10`, `S1..S9` | [S] §13; D-RCV-02; L-RCV-14 |
| Application module | `@ApplicationModule(displayName = "Recovery")` in `recovery/package-info.java` | SPEC-001 (a) |
| Boundary mechanism | Spring Modulith 2.1.1 `verify()` + ArchUnit 1.5.1 rules built from the module map | SPEC-004..-010 |
| Runtime code added | None: existing classes relocated; no new runtime component | spec v4, Change Scope Declaration |

The module is a **modular monolith** ([S] §13; CTX-CONSTRAINT-002). A module is reachable only
through its published packages or an application event. No module reads another module's tables, and
no recovery class calls a system of record directly (REQ-DRI-006; ADR-010).

## 2. The module map

**DOC ID:** DOC-RWB-TE-001-005 · **Maps to:** SPEC-RWB-TE-001-002, SPEC-RWB-TE-001-025, TASK-02, CODE-RWB-TE-001-002

`backend/src/test/resources/architecture/recovery-modules.yaml` is the single source of module
names, packages, published packages, client packages and client libraries (BR6; D-RCV-37). It is a
test resource: it is not packaged in the application jar and cannot affect runtime.

```yaml
rootPackage: th.co.scb.ace.demo.recovery
modules:
  - { code: P3, name: casewf, published: [api, rules, timers, workflow], clientPackages: [] }
  # … 18 more modules
external:
  - { name: common,     rootPackage: th.co.scb.ace.demo.common,     published: [api] }
  - { name: collection, rootPackage: th.co.scb.ace.demo.collection, published: [api] }
clientLibraries: [java.net.http, com.azure.storage, …]   # 16 entries, D-RCV-41
```

| Code | Module | Published packages | Client packages |
|---|---|---|---|
| P1 | `dataengine` | `api` | — |
| P2 | `integration` | `api`, `flags.api` | `adapter` |
| P3 | `casewf` | `api`, `rules`, `timers`, `workflow` | — |
| P4 | `access` | `api` | — |
| P5 | `dochub` | `api` | `storage` |
| P6 | `comms` | `api` | — |
| P7 | `decision` | `api` | — |
| P8 | `payments` | `api` | — |
| P9 | `reporting` | `api` | — |
| P10 | `agent` | `api` | `client` |
| S1 | `valuation` | `api` | — |
| S2 | `treatment` | `api` | — |
| S3 | `guarantee` | `api` | — |
| S4 | `litigation` | `api` | — |
| S5 | `asset` | `api` | — |
| S6 | `debtsale` | `api` | — |
| S7 | `writeoff` | `api` | — |
| S8 | `deviation` | `api` | — |
| S9 | `partner` | `api` | — |

**Map fields.** `rootPackage` (exactly one, valid Java package); `modules[].code`
(`^(P([1-9]|10)|S[1-9])$`, unique); `modules[].name` (`^[a-z][a-z0-9]*$`, unique; the module package
is `rootPackage.name`); `modules[].published` (relative sub-package names, unique per module, never
`internal` or under it); `modules[].clientPackages` (relative names; may name a package that does not
exist yet, which is a permission); `external[]` (`name`, `rootPackage`, `published`; exactly `common`
and `collection`); `clientLibraries` (non-empty, unique, 16 entries). The optional top-level
`sourceViews` key is accepted unvalidated and carried opaque for RWB-E1-069; any other unknown key
fails (SPEC-003). Each published entry is published **alone**: its sub-packages are not published
unless listed (`propagate = false`, SPEC-004 (d)).

## 3. Module skeleton and published surfaces

**DOC ID:** DOC-RWB-TE-001-006 · **Maps to:** SPEC-RWB-TE-001-001, SPEC-RWB-TE-001-022, SPEC-RWB-TE-001-025, AC3, TASK-11, CODE-RWB-TE-001-010, CODE-RWB-TE-001-011

Every map module has three `package-info.java` files:

| Package | Annotation | Meaning |
|---|---|---|
| `recovery.<name>` | `@ApplicationModule(displayName = …)` | The nested module boundary. No public type sits directly here. |
| `recovery.<name>.api` | `@NamedInterface(name = "api", propagate = false)` | The module's published interface. |
| `recovery.<name>.internal` | none | Implementation. No other module may use it. |

Additional published sub-packages carry
`@NamedInterface(name = "<relative package>", propagate = false)`: `casewf.rules`,
`casewf.timers`, `casewf.workflow`, `integration.flags.api`. Implementation sub-packages carry no
`@NamedInterface`: `casewf.admin`, `casewf.migration`, `casewf.workflow.internal`,
`casewf.timers.internal`. `dochub.storage` is a client package, not a published one.

`propagate = false` is deliberate and load-bearing. Spring Modulith 2.1.1 defaults it to `true`,
which would publish every sub-package of a published package without a map entry — including
`casewf.workflow.internal` ([S] §13; finding 030; ASM-09). With `false`, the published surface is
exactly the map's list (BR6).

**The published surface today (exact, asserted by `RecoveryBoundaryTest`):**

| Published package | Public types |
|---|---|
| `casewf.rules` | `RuleEngine` (+ nested `RuleCompilationException`), `RuleInput`, `RuleOutcome`, `RuleResult`, `CompiledRulePackage` |
| `casewf.timers` | `TimerScheduler` (+ nested `TimerDue`) |
| `casewf.workflow` | `WorkflowIds` |
| `integration.flags.api` | `RecoveryFlags` |
| `access.api` | `ApiError`, `ApiProblemException` |
| `dochub.api` | `DocumentStore` (+ nested `StoredDocument`, `DocumentImmutableException`) |

All other `api` packages — including `casewf.api` and `integration.api` — exist with their
annotated `package-info.java` but hold no type yet. `DroolsRuleEngine` and `DroolsProperties` stay
package-private in `casewf.rules`; `PdpaPayloadCodec` became package-private and
`TemporalProperties` became public inside the non-published `casewf.workflow.internal`
(SPEC-022 (c)).

### Relocation performed

| Baseline package | New home |
|---|---|
| `recovery.platform.api` / `.internal` | split across P2 `integration` (`flags`, `internal`), P3 `casewf.timers` / `casewf.migration`, P4 `access` |
| `recovery.rules.api` / `.internal` | P3 `casewf.rules` |
| `recovery.workflow.api` / `.internal` | P3 `casewf.workflow`, `casewf.workflow.internal`, `casewf.admin` |
| `recovery.documents.api` / `.internal` | P5 `dochub.api`, `dochub.storage` |

Signatures, bean names, conditions, endpoint paths and behaviour are unchanged; only `package` and
`import` lines changed, plus the two visibility changes and the `RecoveryProperties` split into four
module-local records (SPEC-022, SPEC-023). After the move the only cross-module type edges are
`casewf.rules → integration.flags.api` (`DroolsRuleEngine` → `RecoveryFlags`) and
`casewf.admin → access.api` (`TemporalAdminController` → `ApiError`, `ApiProblemException`); there is
no cycle.

## 4. Boundary rules BND-1..BND-5

**DOC ID:** DOC-RWB-TE-001-007 · **Maps to:** SPEC-RWB-TE-001-004..-010, BR1–BR6, AC1–AC5, AC7, TASK-06, TASK-07

All rules are built from the map by `BoundaryRules.all(map)` and run in `RecoveryBoundaryTest` on
main classes imported with `DO_NOT_INCLUDE_TESTS`. Failure text is the build-log template of
SPEC-010: `Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application
event.` One line per distinct violation; all violations of a rule appear in one run.

| Rule | What it forbids | What is allowed | Enforcement |
|---|---|---|---|
| **BND-1** collection | a recovery class depending on a `collection` class | only the exact package `th.co.scb.ace.demo.collection.api` and its listed published packages (**exact package match**; sub-packages of a published package are not allowed) | `BoundaryRules.bnd1`; ArchUnit, `allowEmptyShould(true)` (D-RCV-19) |
| **BND-2** common | a recovery class depending on a `common` class | only the exact package `th.co.scb.ace.demo.common.api` and its listed published packages (same exact-match rule) | `BoundaryRules.bnd2`; `allowEmptyShould(true)` |
| **BND-3** recovery → recovery | a class using another nested module's `internal` package or type, or a dependency cycle | the target module's published packages, or an application event | unchanged `ModulithTest.modulesRespectTheirBoundaries` (`ApplicationModules.of(AceRecoveryApplication.class).verify()`); D-RCV-11, D-RCV-42 |
| **BND-4** entities and repositories | a class using an entity (`@jakarta.persistence.Entity`) or a Spring Data `Repository` that is not in its own module | an entity or repository declared in the same module | `BoundaryRules.bnd4`; D-RCV-38 |
| **BND-5** client libraries | a class outside its module's `clientPackages` depending on one of the 16 listed client libraries | the library inside the using module's `clientPackages` (`integration.adapter`, `dochub.storage`, `agent.client`) | `BoundaryRules.bnd5`; REQ-DRI-006, ADR-010, D-RCV-41 |

**BND-5 name matching.** An entry matches a class only on a name boundary — the class equals the
entry, or starts with `entry.` or `entry$`. So `java.net.URL` matches `java.net.URL` but not
`java.net.URLEncoder`; `java.net.Socket` does not match `java.net.SocketTimeoutException`; nested
classes such as `VendorClient$Session` match their outer entry. BND-5 **replaced** the literal
baseline test `blobClientOnlyInDocumentsModule`; the only listed-library user in main code today is
`BlobDocumentStore` (`com.azure.storage`) in `dochub.storage`, which the rule permits.

### The module-map rule (SPEC-004)

This rule runs first and fails before BND-1/2/4/5 when the code and the map disagree:

| Check | Failure when |
|---|---|
| (a) every package under the root that holds a class, directly or below, is a map module | `package {package} is not in the module map` |
| (b) every map module exists (has its `package-info`) | a listed module has no package |
| (c) no type other than `package-info` sits in the root package | a type is in the root |
| (d) every `@NamedInterface` package is listed in `published`, and every listed published package that exists is annotated `@NamedInterface` with `propagate = false` | one side disagrees; the text names the package and the side |
| (e) no public type directly in a module base package `recovery.<name>` | `public type {class} in module base package {package}; move it to a published package or internal` |
| (f) no type-level `@NamedInterface` under the root | `type-level @NamedInterface on {class}; …` |

A package-private type in a module base package passes. A public type in an unlisted sub-package of
a published package (for example `casewf.workflow.internal`) passes this rule and stays internal to
its module.

### Fixtures

`backend/src/test/java/th/co/scb/ace/boundaryfixture/**` holds ten worlds, each with an architecture
`package-info` tree. Eight worlds have a fixture map under
`backend/src/test/resources/architecture/fixtures/` (nine map files, because `bnd5` has a second map
`bnd5-nop2.yaml`); `bnd3fail` and `bnd3cycle` are read by Spring Modulith directly. Worlds: `passing`,
`bnd1`, `bnd2`, `bnd4`, `bnd5` (+ `bnd5-nop2.yaml`), `vendorx`, `mapbad`, `bnd3fail`, `bnd3pass`,
`bnd3cycle`. Fixtures use
the acceptance-criteria class names (`SampleService`, `CollectorRepository`, `DecisionLogRepository`,
`DecisionLogWriter`, `RecoveryCaseEntity`, `vendorx`) and hold class and package names only — no
business value, no personal data. They live outside `th.co.scb.ace.demo`, so neither the real
`RecoveryBoundaryTest` nor `ModulithTest` sees them.

## 5. BND-3 and the Modulith seam

**DOC ID:** DOC-RWB-TE-001-008 · **Maps to:** SPEC-RWB-TE-001-007, BR3, AC3, TASK-08

BND-3 is not reimplemented. It is Spring Modulith's `verify()` over the real application, which
fails on a dependency into another module's non-published type and on a module cycle, and counts
event types as type dependencies (D-RCV-11). The story proves the same behaviour on fixtures through
`ModulithFixtureTest`:

| Fixture world | Expected |
|---|---|
| `bnd3fail` | `verify()` throws; the message names `DecisionLogRepository` (Modulith's own text) |
| `bnd3pass` | `verify()` passes; `DecisionLogWriter` is reachable through the fixture's `writer` named interface |
| `bnd3cycle` | `verify()` throws on the cycle |

**Accepted deviation D-RCV-42.** AC3 asked the failure to identify BND-3 as the broken rule. The
story returns Spring Modulith's own failure text instead; the recovery tech lead accepted this on
2026-11-09. `ModulithFixtureTest` asserts the dependency and the type name, not a bespoke prefix. See
`COMPLIANCE.md` §5.

## 6. Build-time versus runtime boundary

**DOC ID:** DOC-RWB-TE-001-009 · **Maps to:** SPEC-RWB-TE-001-012, SPEC-RWB-TE-001-018, TASK-13, TASK-17

| Aspect | This story |
|---|---|
| Enforcement point | Test and build time only: JUnit 5 in the `test` task and ESLint in `npm run check`. |
| Runtime guard | None. No filter, interceptor, aspect, `@PreAuthorize` or feature flag is added. A violation is stopped at the merge gate, not at runtime; host-side enforcement by GitLab is HV-01 and remains open. |
| Runtime path | Unchanged. The two relocated controllers keep their paths, method security and bodies; `SecurityConfig` keeps `/api/recovery/**` → `HOLDS_WORKBENCH_ROLE` and `anyRequest().denyAll()`. |
| Database | No migration, no table, no view. `RecoveryFlywayConfig` moves package only; its bean, schema placeholder and history table are unchanged. |
| Data | No business field is read or written. The module map is the only data artefact. |
| Failure behaviour | A violation fails the build with the rule, class and dependency; it does not throw at runtime. |
| Local merge gate | `./scripts/dev.ps1 test` exits non-zero on a real violation (T-TE001-13, three-run negative control). The orchestrator merges only on exit 0 (D-RUN-06). |
| Host-side merge blocking | **Not verified here.** That the GitLab project blocks a merge whose pipeline fails is human-verification item HV-01 and is never reported as tested. |
| Rollback | Revert the merge request. No data, configuration or runtime state to unwind. |

## 7. Frontend import rule

**DOC ID:** DOC-RWB-TE-001-010 · **Maps to:** SPEC-RWB-TE-001-013..-015, AC6, TASK-15, CODE-RWB-TE-001-016

The rule is D-RCV-39, implemented as ESLint `no-restricted-imports` in `frontend/eslint.config.js`
for `src/modules/recovery/**/*.{ts,tsx}`.

| Import form | Result |
|---|---|
| `./sibling`, `./casewf/child` | allowed |
| `@/modules/recovery/**` | allowed |
| `@/components/ui/**`, `@/lib/utils` | allowed |
| `@/utils/*` (not `cfsc*`) | allowed |
| `@/contexts/ApiClientContext`, `@/api/schema` | allowed |
| `@/modules/collection/worklist/WorkList` | **rejected** (AC6) |
| `../../collection/worklist/WorkList` | **rejected** (AC6 relative form) |
| any other `@/…` outside the allow-list | **rejected** |
| any specifier containing a `..` path segment, including one hidden behind an allowed prefix (`@/components/ui/../../modules/collection/...`) | **rejected** (SEC-TE001-01 fix) |

`frontend/src/modules/recovery/__tests__/importBoundary.test.ts` loads the real config through the
ESLint Node API and lints in-memory sources at
`src/modules/recovery/caselist/BoundaryFixture.tsx`; no fixture file exists on disk, so no ignore,
`tsconfig` or coverage exclusion is needed. It has 18 cases: 11 rejected and 7 allowed. The 15 cases
in the gated spec are unchanged; three `..` bypass forms were added by the security fix (plan
addendum A-3). No new dependency: ESLint 9.39.5 and its types are already present.

**Accepted deviation D-RCV-39.** AC6 named a `no-collection-import` rule; the repository has no
`src/modules/collection` and uses the `@/` alias, so the rule is the inherited
`no-restricted-imports` allow-list and the import is written `@/modules/collection/worklist/WorkList`
(or the `../../` form). Both forms are in the rejected set.

## 8. Deliberate seams (out of scope)

These are named so a later story does not mistake their absence for a defect: `RecoveryAccessGuard`
and TC-TE-001-08 (RWB-E1-022, D-RCV-52); pipeline changes (D-RCV-05); code owners (RWB-TE-002);
OpenAPI types and contract tests (RWB-TE-003); common and collection internals (DL05 option A); the
integration adapter pattern (RWB-E1-007); the agent client (RWB-TE-013); BND-6 and `sourceViews`
validation (RWB-E1-069); `RuleEngine` / `TimerScheduler` signature alignment with D-RCV-36 §3.3
(RWB-E1-072, RWB-E1-028); CI wiring of the coverage verification (A-09 → RWB-TE-003/RWB-TE-011).
