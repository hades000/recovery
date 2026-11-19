# Plan gate review: RWB-TE-001 (run INC-002-epic-1-RWB-TE-001), round 4

| Field | Value |
|---|---|
| Stage | Compliance Reviewer, plan gate (`planning-execution-gates.md`), round 4 |
| Story | RWB-TE-001 Recovery module folder and boundary test |
| Reviewed | `plan/plan.md` v4, `plan/tasks.md` v4, `plan/data-model.md` v4, `plan/tests/scenarios.md` v4, `plan/assumptions.md`, `plan/document-gaps.md`, `plan/shared-updates.md`, `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json`, `plan/agent-run-log.md` ("Round 4" section). The `*.run3` files were used only to compare. |
| Checked against | Approved spec v4 (`specify/spec.md`, spec gate round 5 PASS); round 1–3 reviews (`review/plan-gate-review.md`, `-2.md`, `-3.md`); `AI-SDLC-BUILD-LOG.md` D-RUN-07, -08, -09, -18, -19; RUN-BRIEF; the code: `scripts/dev.ps1`, `.env.example` (key names only), `backend/src/main/resources/application.yaml`, `backend/build.gradle.kts`, `backend/gradle/wrapper/gradle-wrapper.properties`, the baseline classes `TemporalConfig`, `PdpaPayloadCodec`, `TemporalProperties`, `TemporalAdminController`, `PlatformInfoController`, `BlobDocumentStore`; the Spring Boot 4.1.2 jars `spring-boot-test` and `spring-boot` and the Gradle 9.9.1 `gradle-testing-jvm` jar (read with `javap`); RWB-E1-042 spec revision 9 (`aisdlc/output/INC-003-epic-1-RWB-E1-042/specify/spec.md`, D-RUN-18/19 and CLAR-025 only) |
| Reviewer | Compliance Reviewer agent, started by the orchestrator (Claude Code). Read only; this file is the only file written. |

## 1. Round-3 findings

| Finding | Result | Evidence |
|---|---|---|
| PLAN-012 (Medium) binding tests read `.env` under `./scripts/dev.ps1 test` | **RESOLVED** for the five T-TE001-12 tests. Residuals recorded as PLAN-018 (other test contexts not covered) and PLAN-019 (Run 3 evidence) | See §1.1. |
| PLAN-013 (Low) fallback branches not asserted | **RESOLVED** | `bnd5TextWithoutP2UsesTheOriginModule` now asserts exactly six lines, including the two `PartnerHttpAdapter` origin-package lines ending `…bnd5.recovery.integration.adapter.api or an application event.` (`tests/scenarios.md` line 50; `data-model.md` line 50). The `bnd4` world adds `ArchiveReader` → `bnd4.legacy.ArchivedLoanEntity`, outside every module and external root; AC4 now expects exactly four lines, one with the target-package text (`data-model.md` line 48; `scenarios.md` line 21). This agrees with spec v4 TC-TE-001-04 ("an entity outside the recovery root … BND-4 fails on both") and SPEC-008. `data-model.md` §4 (line 66) and PA-04 (`assumptions.md` line 10) now state exactly what is tested. The SPEC-010 rows name both tests (`plan.md` line 316; `scenarios.md` line 77). |
| PLAN-014 (Low) T-TE001-15 could not pass | **RESOLVED** | `scenarios.md` line 57: the scan removes the `package` line, `import` lines and comments, then checks only string literals and annotation values. Self-test `packageLiteralScanSeesLiteralsOnly` proves it fires on a literal and ignores the `package`, `import` and comment cases. TASK-06 lists the self-test (`tasks.md` line 32). The self-test samples sit in `BoundaryRulesTest`, which the scan excludes (`*Test.java`). |
| PLAN-015 (Low) compile-red ordering | **RESOLVED** | BLOCKED_BY: TASK-05 ← TASK-04, TASK-08 ← TASK-07, TASK-10 ← TASK-08 and TASK-09 (`tasks.md` lines 31, 34, 36). The graph is redrawn (lines 76–81). The note at line 85 says compile-red tasks (03, 06, 10) run directly before their green tasks (04, 07, 11) with no task in between. |
| PLAN-016 (Low) one-module reading unsettled | **RESOLVED** | SU-P05 asks the orchestrator (Claude Code) to settle one reading for every story; SU-P06 requests an open item for the tech lead (`shared-updates.md` lines 11–12). Gap PG-04 / GC-1 recorded, Blocker = No (`document-gaps.md` line 12). PA-12 kept and annotated (`assumptions.md` line 18). `plan.md` "Scope" points to them (line 58). One citation in SU-P05 and PG-04 is stale (PLAN-020). |

### 1.1 PLAN-012 against the code

| Check | Result | Evidence |
|---|---|---|
| Why the round-3 design failed | Confirmed. `dev.ps1` runs `Initialize-EnvFile` and `Import-EnvFile` before the command switch (lines 86–87). `Import-EnvFile` sets each `.env` entry as a process environment variable (lines 44–49). `test` then runs `Invoke-Gradle @("test")` (line 115), and the test JVM inherits that environment. `.env.example` sets `RWB_P3_TEMPORAL`, `RWB_P3_DROOLS`, `RWB_MIGRATOR_PASSWORD`, `RWB_BLOB_CONNECTION_STRING` and `RWB_TEMPORAL_CODEC_KEY` (lines 8, 19, 20, 23, 27; values not quoted). It sets no `SPRING_PROFILES_ACTIVE` and no `RWB_OIDC_*`, `RWB_CORS_ORIGINS` or `RWB_ENVIRONMENT`. | `scripts/dev.ps1`; `.env.example` |
| Placeholders the binding tests depend on | `rwb.p3.temporal: ${RWB_P3_TEMPORAL:false}`, `rwb.p3.drools: ${RWB_P3_DROOLS:false}`, `rwb.flyway.password: ${RWB_MIGRATOR_PASSWORD:}` (lines 76, 77, 82). Every other bound key has a literal or a placeholder with a default. `application.yaml` is a single YAML document, and there is no `application.yaml` in `backend/src/test/resources`, so `new ClassPathResource("application.yaml")` resolves to the main file. "The first source" returned by the loader is the whole file. | `backend/src/main/resources/application.yaml`; `backend/src/test/resources` holds `architecture/` only |
| The mechanism binds the defaults | Yes, under both `./gradlew test` and `./scripts/dev.ps1 test`. (1) Spring Boot 4.1.2 has `ApplicationContextRunner(Supplier<ConfigurableApplicationContext>)` (`javap` on `spring-boot-test-4.1.2.jar`). (2) `AbstractApplicationContextRunner` calls `contextFactory.get()`, then `configureContext`: parent, class loader, `TestPropertyValues.applyTo(context)`, bean registrations, initializers, configurations. It never replaces the environment, so the `setEnvironment` call in the supplier stays in force. `withPropertyValues` adds its own source on top, which the flag cases need. (3) `AnnotationConfigApplicationContext.setEnvironment` also passes the environment to its reader and scanner, so conditions see it. (4) `org.springframework.boot.env.YamlPropertySourceLoader.load(String, Resource)` exists in `spring-boot-4.1.2.jar`. (5) With the `systemEnvironment` and `systemProperties` sources removed, no source holds `RWB_*` either as a placeholder name or as a relaxed-binding alias such as `RWB_P3_TEMPORAL` → `rwb.p3.temporal`. Each `${…:default}` therefore resolves to its default through the Binder's `PropertySourcesPlaceholdersResolver`. | `plan.md` line 218; TASK-10 (`tasks.md` line 36) |
| Assertions unchanged | Yes. The T-TE001-12 expected values in `scenarios.md` v4 line 54 equal those in `scenarios.run3.md`: `temporal=false`, `drools=false`; `DEV`, `recovery`; flyway `true`, URL, `rwb_migrator`, empty password, location; the five security values; cache max 20. The wording is pinned to "the `application.yaml` placeholder defaults". | `scenarios.md` line 54; `data-model.md` line 89 |
| `.env.example` not edited | Yes. `plan.md` line 218 says so, and no plan file table lists it. TASK-18 (1) limits the diff to the files in `plan.md`. | `plan.md` lines 97–118; `tasks.md` line 44 |
| Verification under `dev.ps1` | Planned: TASK-17 Run 3 records the five methods as passed with `.env` imported, and TASK-13 points to it (`tasks.md` lines 39, 43). Run 3 may not execute the tests itself (PLAN-019). | `tasks.md` |
| `SecurityConfigTest` MVC-slice pinning claim | True for the keys it names. No `.env.example` key maps to `rwb.security.*`, and `@WebMvcTest(properties = …)` adds inlined test properties that outrank environment variables. Incomplete for the slice as a whole: the slice also reads `rwb.p3.temporal` (PLAN-018). | `plan.md` line 208 |

## 2. Earlier findings PLAN-001..011 (held)

| Finding | Result | Evidence |
|---|---|---|
| PLAN-001 TASK-13 row | Held | Note N-1 (`tasks.md` lines 46–52). A script count of unescaped `\|` per table row against the header, over all eight plan Markdown files, finds no mismatch. Both contract JSON files parse. |
| PLAN-002 `check` wiring | Held | TASK-01 Verification (`tasks.md` line 27) |
| PLAN-003 Run 1 evidence | Held | TASK-17 names the `RecoveryBoundaryTest` JUnit XML path; no `testLogging` edit (`tasks.md` line 43) |
| PLAN-004 "stricter BND-5" | Held | The only "stricter" hit in `plan/` v4 is PA-05, which is unrelated |
| PLAN-005 determinism guard | Held | `plan.md` line 187 |
| PLAN-006 violation unit | Held | `data-model.md` §4 intro |
| PLAN-007 BND-5 `{module}` | Held | `data-model.md` line 66 |
| PLAN-008 guard in the red task | Held | TASK-09 description and red Verification; TASK-11 Trace and Verification (`tasks.md` lines 35, 37) |
| PLAN-009 BND-5 fallback | Held, and its residual (PLAN-013) is resolved | above |
| PLAN-010 dry-run baseline | Held | TASK-00 and TASK-01 Verification |
| PLAN-011 source version | Held | `tasks.md` line 10: "`plan.md` v4 and `../specify/spec.md` v4" |

## 3. Plan-gate checks

| Check | Result | Evidence |
|---|---|---|
| Structure: status lines, `## Requirement Logic To Task Coverage`, `## Pre-submit checks`, task schema (Task, Description, Files, Trace, BLOCKED_BY, Verification) | Pass | `plan.md` lines 272–301, 355–362; `tasks.md` lines 24–44, 87–99 |
| Every scope bullet → task | Pass (S-1..S-15) | `tasks.md` lines 54–72 |
| Tests before code | Pass. Red runs: TASK-01 (assertion), -03, -06, -10 (compile), -09 (assertion). Green: TASK-04, -07, -11. Characterization tests TASK-12 explained (PA-07). | `tasks.md` lines 12, 83–85 |
| SPEC → task → test | Pass for SPEC-001..026 (021 withdrawn). The new helper and both fallback tests are traced. | `plan.md` lines 305–332; `scenarios.md` §5 |
| AC1–AC7, BR1–BR6 coverage | Pass. `TOTAL_RULES: 13`, `TASK_COVERED_RULES: 13`. X7 is shown as moved out of scope (D-RCV-52), as in earlier rounds. | `plan.md` lines 276–301, 361 |
| No new dependency | Pass. `YamlPropertySourceLoader` (spring-boot), `StandardEnvironment` and `AnnotationConfigApplicationContext` (Spring Framework), `ApplicationContextRunner` (spring-boot-test) are already on the test classpath. `spring-boot-starter-webmvc-test` and `-security-test` are already declared (`build.gradle.kts` lines 74, 76). | TASK-00 (2); TASK-18 (2) |
| No migration (D-RUN-07) | Pass. No `V*.sql` or migration number in any plan file. | grep of `plan/` |
| Seams only (D-RUN-08) | Pass. SPEC-016 list; SU-P02, SU-P03. | `plan.md` line 56; `shared-updates.md` |
| Coverage gate 80% | Pass. Backend: JaCoCo LINE, INSTRUCTION, BRANCH, METHOD ≥ 0.80 (TASK-01, TASK-13). Frontend: inherited Vitest 80 × 4 (TASK-16). The new `testsupport` helper is test scope and outside the include, as intended. | `plan.md` lines 189–198, 242–249 |
| No skipped or weakened test | Pass. Assertions are unchanged (§1.1). `blobClientOnlyInDocumentsModule` is replaced as SPEC-009 and SPEC-026 require. | `tasks.md` line 98 |
| Personal data | None. Class and package names, local placeholder defaults, generated keys; `.env` values are never recorded (TASK-17 records key names only). | `tasks.md` line 43 |
| Attribution | Pass. No text records that a human approved, accepted or disposed of anything. Triage is attributed to the orchestrator (Claude Code) (`agent-run-log.md` Round 4). "Accepted deviation D-RCV-39/42" cites client decisions, not a sign-off recorded by this stage. | grep of `plan/` for approv/accept/dispos/human |

## 4. D-RUN-18 and D-RUN-19

**CONFIRMED.**

- **T-TE001-14.** It states that each published list is exact, `access.api` included. Later stories extend that list in their own merge request: RWB-E1-042 for the D-RUN-19 parameter read interface (P4 `access.api`, implemented in P3 `casewf.config`), `MessageResolver` and `CapabilityCheck`; RWB-E1-043 for the D-RUN-18 reference-load SPI. Sources: `scenarios.md` line 56; `plan.md` line 185; contract `publishedJavaTypesAfterRelocation.note` (`backend-apis.json` line 63); SU-P02 (`shared-updates.md` line 8).
- **Consistency with the decisions.** This matches D-RUN-18 ("published by P4 (`access.api`)") and D-RUN-19 ("read interface published by P4 (`access.api`) and implemented in P3 `casewf.config`") in `AI-SDLC-BUILD-LOG.md`. It also matches RWB-E1-042 spec revision 9, which adds `access.api.MessageResolver` and `access.api.CapabilityCheck` (Impacted Existing Nodes row).
- **No map change needed.** `access` publishes `[api]`, so the new types need no module-map change. P3 → P4 is an existing edge.

## 5. Findings

### REVIEW-RWB-TE-001-PLAN-017 — Low — `TemporalConfigTest` cannot create the codec bean on the isolated environment: no codec key is supplied

- **Affects:** `plan.md` "Coverage tests", `TemporalConfigTest` row (line 213) and "Security, privacy and compliance" (line 342); TASK-12; SPEC-024; T-TE001-10.
- **Evidence:**
  - The row runs the context on `ApplicationYamlEnvironment.isolated()` with `withPropertyValues` `rwb.p3.temporal=true` and a loopback target. It expects "stubs, codec, client … and worker factory beans are created".
  - `TemporalConfig.pdpaPayloadCodec` builds `new PdpaPayloadCodec(properties.codecKey(), …)` (`TemporalConfig.java` lines 50–53). The constructor throws `IllegalStateException` when the key is null or blank (`PdpaPayloadCodec.java` lines 38–41).
  - On the isolated environment, `rwb.temporal.codec-key: ${RWB_TEMPORAL_CODEC_KEY:}` (`application.yaml` line 93) resolves to empty. `plan.md` line 342 confirms "`RWB_TEMPORAL_CODEC_KEY` stays empty in tests".
  - So the context fails to start under both `./gradlew test` and `./scripts/dev.ps1 test`, and the stated expectation cannot hold. Under the round-3 design the `.env` key (generated by `Initialize-EnvFile`, `dev.ps1` lines 34–41) reached the context through relaxed binding under `dev.ps1` only, which hid the gap there.
- **Fix:** Add `rwb.temporal.codec-key=<key generated in the test>` to the `withPropertyValues` of the flag-on case, as `PdpaPayloadCodecTest` already does (`SecureRandom` 32 bytes, Base64). Never take the value from `.env`. State it in the row. Optionally add a case asserting that a blank key fails context start with the `rwb.temporal.codec-key is required` message; that is today's behaviour, so no assertion is weakened.

### REVIEW-RWB-TE-001-PLAN-018 — Low — Two Spring test contexts can still read `.env` keys under `dev.ps1`: the `SecurityConfigTest` MVC slice and the `BlobDocumentStoreTest` `Config` cases

- **Affects:** `plan.md` line 208 (`SecurityConfigTest`), line 215 (`BlobDocumentStoreTest`), line 218 (isolation paragraph); TASK-12; TASK-17 Run 2/3; SPEC-012 (b), SPEC-024; round-3 PLAN-012 fix item 2.
- **Evidence:**
  - **MVC slice.**
    - The slice pins only `rwb.security.*` and claims ".env cannot change it". It names no `controllers` attribute, only "a test-only controller nested in the test class".
    - A `@WebMvcTest` with no `controllers` scans every `@Controller` under the application's base package. That includes `TemporalAdminController`, which is `@ConditionalOnProperty(name = "rwb.p3.temporal", havingValue = "true")` (`TemporalAdminController.java` line 44) and needs `WorkflowServiceStubs` and `WorkflowClient` (line 57).
    - `.env.example` line 19 sets `RWB_P3_TEMPORAL`. Under `dev.ps1` the controller joins the slice and the context fails for the missing Temporal beans; under `./gradlew test` it does not. This is the PLAN-012 failure class again.
    - It is only avoided if the Builder happens to restrict `controllers`. A Builder who instead mocks `JdbcTemplate` for `PlatformInfoController` (line 24) gets a slice that passes only under `./gradlew test`.
  - **Blob `Config`.**
    - The row lists "`Config`: connection string, endpoint with credential, neither → `IllegalStateException`" with no mechanism. `Config.blobServiceClient` throws when both values are blank (`BlobDocumentStore.java` lines 111–118).
    - If these cases run on an `ApplicationContextRunner` with the default environment, `RWB_BLOB_CONNECTION_STRING` (`.env.example` line 23) binds to `rwb.blob.connection-string` by relaxed binding. The "neither" case then fails only under `dev.ps1`.
  - **Scope of the isolation rule.** Line 218 makes isolation mandatory only for the five binding tests and the other runner cases of `PlatformConfigTest` and `TemporalConfigTest`.
  - TASK-17 Run 2 ("Gradle green") would catch either failure, but only at the end of the build, after TASK-13 has passed.
- **Fix:**
  - State `@WebMvcTest(controllers = <the nested test controller>)` with `@Import` of `SecurityConfig`, `ApiExceptionHandler` and `ProblemFactory` as needed, and pin `rwb.p3.temporal=false` in its `properties`.
  - State that the Blob `Config` cases call `new BlobDocumentStore.Config().blobServiceClient(new BlobProperties(…))` directly, or run on `ApplicationYamlEnvironment.isolated()`.
  - Add one rule to the isolation paragraph and a TASK-18 check: every test that starts a Spring context uses `ApplicationYamlEnvironment.isolated()` or pins in `properties` every key whose `.env.example` variable could change it.

### REVIEW-RWB-TE-001-PLAN-019 — Low — TASK-17 Run 3 may not run the backend tests: Gradle does not track environment variables, so `:test` is UP-TO-DATE after Run 2

- **Affects:** `tasks.md` TASK-17 Verification (line 43) and TASK-13 (line 39); `tests/scenarios.md` T-TE001-12 and T-TE001-13 (lines 54–55); `plan.md` line 218 ("TASK-17 Run 3 runs the suite through `./scripts/dev.ps1 test` and records the five binding tests as passed"); SPEC-012 (b).
- **Evidence:**
  - The wrapper is Gradle 9.9.1 (`gradle-wrapper.properties`). In `gradle-testing-jvm-9.9.1.jar`, `org.gradle.api.tasks.testing.Test.getEnvironment()` carries `@org.gradle.api.tasks.Internal` (`javap -v`), so environment variables are not task inputs.
  - `build.gradle.kts` lines 100–108 declare no input for the environment. Run 2 removes the backend probe and runs `:test` to green. Run 3 removes only the frontend probe, so its backend inputs equal Run 2's and `:test` is UP-TO-DATE.
  - The JUnit XML that TASK-17 reads for Run 3 is then Run 2's output. The same applies to any `dev.ps1 test` run straight after TASK-13's `./gradlew test` on unchanged code: the tests would not run with `.env` at all.
  - The plan therefore credits evidence to a run that may not have produced it, and has no check that the tests actually executed with `.env` imported.
- **Fix:**
  - Before Run 3 (or before whichever run is the `.env` evidence), delete `backend/build/test-results/test` or run `./gradlew cleanTest`, so `:test` must execute.
  - Record the Gradle line that shows `> Task :test` executed (not `UP-TO-DATE` or `FROM-CACHE`) and the XML file times after the run start.
  - Alternatively, name Run 2 as the `.env` evidence and record the same proof for it. `scripts/dev.ps1` stays unchanged.

### REVIEW-RWB-TE-001-PLAN-020 — Low — Stale version and citation: contract revision not raised, and the RWB-E1-042 citation has no revision and a moved line

- **Affects:** `plan/contracts/backend-apis.json` line 5; `shared-updates.md` SU-P05 (line 11); `document-gaps.md` PG-04 (line 12); RUN-BRIEF rule 8.
- **Evidence:**
  - **Contract revision.** `backend-apis.json` changed in round 4: the `publishedJavaTypesAfterRelocation.note` now carries the D-RUN-18/19 extension rule (line 63, compared with `backend-apis.run3.json`). Its `revision` is still `"v1 (2026-11-18)"`, the same as the round-3 file, while plan, tasks, data-model and scenarios moved to v4. A reader cannot tell which contract text the v4 plan relies on. The round-2 finding PLAN-011 (stale source version) was the same kind of defect.
  - **RWB-E1-042 citation.** SU-P05 and PG-04 cite "`aisdlc/output/INC-003-epic-1-RWB-E1-042/specify/spec.md`, line 1103" with no revision. That spec is now revision 9, where CLAR-025 is at line 1134. Line 1103 holds CLAR-025 only in revision 8 (`spec.run7.md`).
- **Fix:** Raise the contract `revision` (for example "v4 (2026-11-18): note on later-story extensions, D-RUN-18/19") or add a change note. In SU-P05 and PG-04, cite "RWB-E1-042 spec revision 9, Clarification Log CLAR-025", with no line number or with line 1134.

## 6. Observations (not defects)

- **`.env.example` not listed in TASK-18.** TASK-18 (1) names the files that must not change but not `.env.example`. The general rule "diff touches only the files in `plan.md`" covers it. Naming it would make the PLAN-012 condition visible in the evidence.
- **Hard-coded module code `P2` in tooling.** Unchanged from round 2. It is not a package literal and T-TE001-15 ignores it.
- **Exact fixture line counts.** They still depend on fixture authoring (rounds 2 and 3). The new `bnd4` and `bnd5-nop2` lines follow the same violation definition (`data-model.md` §4).

## 7. Document gaps

No new document gap. The round-3 candidate GC-1 is now recorded by the plan as PG-04 (Blocker = No), with both citations; PLAN-020 asks for its RWB-E1-042 citation to carry the revision.

| ID | Gap | Citation 1 | Citation 2 | Blocker |
|---|---|---|---|---|
| — | none new | — | — | — |

## 8. Result

```text
PREVIOUS_FINDINGS: PLAN-012..016 RESOLVED (5/5; PLAN-012 residuals recorded as PLAN-018 and PLAN-019); PLAN-001..011 held (11/11)
PLAN_GATE_FINDINGS: REVIEW-RWB-TE-001-PLAN-017, -018, -019, -020 (all Low)
PLAN_REQUIREMENT_COVERAGE_RESULT (reviewer check): CONFIRMED [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0] [CONTRADICTIONS: 0]
PLAN_012_MECHANISM: CONFIRMED (isolated StandardEnvironment + YamlPropertySourceLoader + ApplicationContextRunner(Supplier) binds the application.yaml placeholder defaults under ./gradlew test and ./scripts/dev.ps1 test; assertions unchanged; .env.example not edited)
D_RUN_18_19_COMPATIBILITY: CONFIRMED (T-TE001-14 wording tells RWB-E1-042 and RWB-E1-043 to extend the exact access.api list in their own merge request)
```

Overall status: **FAIL**. Counts: Critical 0, High 0, Medium 0, Low 4. Under D-RUN-09 the orchestrator (Claude Code) fixes Low findings rather than carrying them.

REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
