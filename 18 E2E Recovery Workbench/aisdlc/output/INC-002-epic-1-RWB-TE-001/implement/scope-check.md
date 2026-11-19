# Scope, guardrail and evidence check: RWB-TE-001 (TASK-18)

Worktree `rwb-wt/RWB-TE-001`, base `8675a5c`. This check was written at TASK-18 (`473f0af`) and
**refreshed for the code gate at `55f1ed4`** (CODE-003): counts and the `eslint.config.js` status are
the final ones. Commands ran from the worktree root; `backend/` commands carry
`JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=%USERPROFILE%\.gradle\uds`.

## (1) Diff touches only the plan's files

`git diff --name-only 8675a5c..HEAD` → 230 entries: 227 under `backend/src/**` (of which 4 are the
`bnd2` review fixtures and `RuleFactsTest` / `CaseEventType`, DEV-05/06), `backend/build.gradle.kts`
(1), `frontend/src/modules/recovery/__tests__/importBoundary.test.ts` (1) and
`frontend/eslint.config.js` (1, DEV-08). Evidence: `backend/scope-diff.txt`.

Shared files edited: `backend/build.gradle.kts` and `frontend/eslint.config.js` (DEV-08, the
SEC-TE001-01 tightening; see `../plan/plan-addendum.md` A-1). No other shared file is touched.

Unchanged against the base (searched in `scope-diff.txt`): `.gitlab-ci.yml`, `scripts/**`,
`application*.yaml`, `backend/src/main/resources/db/**`, `frontend/package.json`,
`frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `.env.example`
→ no diff.

## (2) No new dependency

`./gradlew --offline -q dependencies` for `runtimeClasspath`, `testCompileClasspath` and
`testRuntimeClasspath`, compared with the TASK-00 captures. Only the JVM's
`Picked up JAVA_TOOL_OPTIONS` banner differs; the resolved graphs are identical
(869 / 925 / 1093 lines each). Evidence: `backend/deps-diff.txt`.

## (3) SPEC-016 exclusions

| Item | Check | Result |
|---|---|---|
| `RecoveryAccessGuard` | source search | 0 hits (`backend/scope-diff.txt`) |
| test-only Case record endpoint | `@PostMapping` under `backend/src` | only the existing `TemporalAdminController` smoke endpoint |
| new `MSG-P4-002` use | added lines in main code vs base | none (`backend/scope-greps-2.txt`) |
| BND-6 and `sourceViews` validation | loader carries `sourceViews` opaque; no check added | `ModuleMapLoader.java:65` returns `root.get("sourceViews")` unchanged |
| pipeline change | `.gitlab-ci.yml` in diff | none |

## (4) SPEC-019 guardrails

Maps, fixture classes and failure texts hold class and package names only. No business value,
threshold, route or personal-data field appears in the tooling, fixtures or rule texts: the fixtures
declare field types and empty bodies, the map holds package and client-library names, and the texts
are the SPEC-010 template with class, package and module names. Test data is synthetic; the only key
material is a random AES key generated in-process by `TemporalConfigTest` and
`PdpaPayloadCodecTest`.

## (5) Unit-test results table

See `unit-tests/report.md` (backend 141/141 PASS, frontend 28/28 PASS, UI `NOT_APPLICABLE`), with the
native reports under `backend/coverage/` and `frontend/`. The TASK-18 snapshot was backend 140 /
frontend 25; the current numbers include the review-fix tests (`BoundaryRulesTest` 17,
`importBoundary.test.ts` 18/18).

## (6) `.env.example`

No diff against the base. `dev.ps1` created the worktree's untracked `.env` from it during TASK-17;
the file is not committed.

## (7) Spring contexts in the tests this story adds or edits

| Test | Context | Keys pinned |
|---|---|---|
| `PlatformConfigTest` (binding and flags) | `ApplicationContextRunner` on `ApplicationYamlEnvironment.isolated()` | none needed; no system environment or system-property source |
| `PlatformInfoControllerTest.binds…` | isolated runner | none needed |
| `PlatformInfoControllerTest.info…` | no context; class called directly | n/a |
| `RecoveryFlywayConfigTest.binds…` | isolated runner | none needed |
| `RecoveryFlywayConfigTest.recoveryFlyway…` | no context; `RecoveryFlywayConfig` called directly | n/a |
| `SecurityConfigTest.binds…` | isolated runner | none needed |
| `SecurityConfigTest` MVC slice | `@WebMvcTest` (not isolated) | see below |
| `DroolsPropertiesTest` | isolated runner | none needed |
| `TemporalConfigTest` | isolated runner, explicit `withPropertyValues` (`rwb.p3.temporal`, target, codec key) | codec key generated in the test |
| `TemporalAdminControllerTest` | no context (mocked stubs; `TestWorkflowEnvironment` for smoke) | n/a |
| `ApiExceptionHandlerTest`, `ApiErrorTest`, `BlobDocumentStoreTest`, `WorkflowIdsTest`, `RuleFactsTest` | no context | n/a |

MVC slice table:

| Column | Content |
|---|---|
| (a) Classes created | `@Import`: `SecurityConfigTest.ProbeController`, `SecurityConfig`, `ProblemFactory`, `ApiExceptionHandler`; `controllers = ProbeController`. Registered by these: `RecoverySecurityProperties` (`@EnableConfigurationProperties` on `SecurityConfig`); beans `SecurityFilterChain`, `JwtDecoder` (replaced by `@MockitoBean`); `ProblemFactory(ObjectProvider<Tracer>, JsonMapper)`; `ApiExceptionHandler(ProblemFactory)`. Slice auto-configurations include `WebMvcAutoConfiguration`, the Jackson auto-configuration (`JsonMapper`), `ErrorMvcAutoConfiguration`, `SecurityAutoConfiguration`/`SecurityFilterAutoConfiguration` and the `@WebMvcTest` import list. |
| (b) Keys they read | `rwb.security.issuer`, `rwb.security.jwk-set-uri`, `rwb.security.audience`, `rwb.security.roles-claim`, `rwb.security.cors-origins` (`RecoverySecurityProperties`); `rwb.p3.temporal` (`TemporalAdminController`'s `@ConditionalOnProperty`, though the controller is outside `controllers`); `spring.mvc.*`, `spring.jackson.*`, `server.error.*` from the auto-configurations. No dependency's `spring-configuration-metadata.json` declares a `rwb.` property (4 jars checked: autoconfigure, webmvc, security, jackson → 0 hits). |
| (c) `.env.example`-reachable keys (names only) | `postgres.*`, `rwb.migrator.password`, `recovery.svc.password`, `temporal.svc.password`, `rwb.ace.tier2.probe`, `rwb.load.reference.schema`, `rwb.p3.temporal`, `rwb.p3.drools`, `rwb.blob.connection-string`, `rwb.blob.connection-string-docker`, `rwb.temporal.codec-key` (relaxed forms) |
| (d) Intersection needing a pin | `rwb.p3.temporal`; all `rwb.security.*` keys (defensive: the slice's own properties are fixed regardless of `.env`). Both are pinned in the slice's `properties`. No other intersection exists. |

## Remaining checks

- Old-package search (N-1): no match; the four baseline packages are gone (`backend/task13-old-package-search.log`).
- No test is skipped, disabled or weakened. `blobClientOnlyInDocumentsModule` is replaced by BND-5 as
  SPEC-009 and SPEC-026 require; the moved tests keep their assertions. Two test-only corrections are
  recorded in `deviations.md` DEV-03 and DEV-05.
- TASK-14's e2e half is `BLOCKED` by the run rule; see `deviations.md` DEV-01.
