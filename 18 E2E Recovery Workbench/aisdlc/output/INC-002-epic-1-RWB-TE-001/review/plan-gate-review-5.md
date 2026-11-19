# Plan gate review: RWB-TE-001 (run INC-002-epic-1-RWB-TE-001), round 5

| Field | Value |
|---|---|
| Stage | Compliance Reviewer, plan gate (`planning-execution-gates.md`), round 5 |
| Story | RWB-TE-001 Recovery module folder and boundary test |
| Reviewed | `plan/plan.md` v5, `plan/tasks.md` v5, `plan/data-model.md` v5, `plan/tests/scenarios.md` v5, `plan/assumptions.md`, `plan/document-gaps.md`, `plan/shared-updates.md`, `plan/contracts/backend-apis.json` (revision v2), `plan/contracts/frontend-integrations.json` (v1, unchanged), `plan/agent-run-log.md` ("Round 5" section). The `*.run4` files were used only to compare (line diff v4 → v5). |
| Checked against | Approved spec v4 (`specify/spec.md`, unchanged since spec gate round 5 PASS); plan gate reviews rounds 1–4 (`review/plan-gate-review.md`, `-2.md`, `-3.md`, `-4.md`); `AI-SDLC-BUILD-LOG.md` D-RUN-07, -08, -09, -18, -19; RUN-BRIEF; the code: `TemporalConfig`, `TemporalProperties`, `PdpaPayloadCodec`, `PdpaPayloadCodecTest`, `TemporalAdminController`, `SecurityConfig`, `ProblemFactory`, `ApiExceptionHandler`, `BlobDocumentStore` (`Config`, `BlobProperties`), `AceRecoveryApplication`, `backend/src/main/resources/application.yaml`, `backend/build.gradle.kts`, `backend/gradle/wrapper/gradle-wrapper.properties`, `scripts/dev.ps1`, `.env.example` (key names only; no value read or quoted); the Spring Boot 4.1.2 jars `spring-boot-test` (`TestTypeExcludeFilter`, read with `javap -c`) and `spring-boot-webmvc-test` (`WebMvcTest`, `WebMvcTypeExcludeFilter`, read with `javap`); RWB-E1-042 spec revision 9 (`spec.run8.md`) and revision 10 (`spec.md`) under `aisdlc/output/INC-003-epic-1-RWB-E1-042/specify/`, CLAR-025 and the Impacted Existing Nodes row only |
| Reviewer | Compliance Reviewer agent, started by the orchestrator (Claude Code). Read only; this file is the only file written. |

## 1. Round-4 findings

| Finding | Result | Evidence |
|---|---|---|
| PLAN-017 (Low) `TemporalConfigTest` has no codec key on the isolated environment | **RESOLVED** | `plan.md` v5 line 213: the flag-on cases add `rwb.temporal.codec-key` "set to a key generated in the test (32 bytes from `SecureRandom`, Base64, as `PdpaPayloadCodecTest` does; never read from `.env`)". That matches `PdpaPayloadCodecTest.newKey()` (lines 17–21) and satisfies the constructor check (`PdpaPayloadCodec.java` lines 38–45: non-blank, 16/24/32 bytes). The value is supplied by `withPropertyValues`, which adds a source above the isolated `application.yaml` source, so `${RWB_TEMPORAL_CODEC_KEY:}` (`application.yaml` line 93) no longer leaves the key blank for these cases. The new case "flag on with a blank codec key → context start fails with `rwb.temporal.codec-key is required`" asserts today's behaviour: on the isolated environment the key resolves to empty and `TemporalConfig.pdpaPayloadCodec` (lines 50–53) throws `IllegalStateException("rwb.temporal.codec-key is required when rwb.p3.temporal is on")` (`PdpaPayloadCodec.java` line 40); the asserted text is a substring of it. `plan.md` line 344 is consistent ("`RWB_TEMPORAL_CODEC_KEY` is never read in tests"). |
| PLAN-018 (Low) other Spring contexts read `.env` under `dev.ps1` | **RESOLVED** for the two contexts named. A residual in the slice design is new finding PLAN-021, and the wording of the new rule is new finding PLAN-022. | See §1.1. |
| PLAN-019 (Low) Run 3 could be UP-TO-DATE | **RESOLVED** | TASK-17 (`tasks.md` line 43) runs `./gradlew cleanTest` in `backend/` before Run 3 and notes the start time; its Verification requires `backend/build/test-results/test/` emptied by `cleanTest`, XML files later than the Run 3 start and, where shown, `> Task :test` without `UP-TO-DATE` or `FROM-CACHE`. T-TE001-13 (`scenarios.md` line 55) and `plan.md` line 218 say the same. Against the code: `cleanTest` deletes the `test` task outputs, so `:test` must execute in Run 3. No `gradle.properties` exists in `backend/` and `dev.ps1` calls `./gradlew.bat test` with no `--build-cache` (`dev.ps1` lines 67–73, 114–116), so the build cache is off and `FROM-CACHE` cannot hand back Run 2's XML with fresh file times. `build.gradle.kts` lines 100–108 and `scripts/dev.ps1` stay unchanged (`plan.md` line 118; TASK-18 (1)). |
| PLAN-020 (Low) contract revision and RWB-E1-042 citation | **RESOLVED** | `contracts/backend-apis.json` line 5: revision "v2 (2026-11-18)" with a change note naming the `publishedJavaTypesAfterRelocation.note` change and "used by plan v5". SU-P05 (`shared-updates.md` line 11), PG-04 (`document-gaps.md` line 12), PA-12 (`assumptions.md` line 18) and `plan.md` "Scope" (line 58) cite "RWB-E1-042 spec revision 9 … Clarification Log CLAR-025" with no line number. Revision 9 holds CLAR-025 (`spec.run8.md` line 1134). See observation O-1 on revision 10. |

### 1.1 PLAN-018 against the code

| Check | Result | Evidence |
|---|---|---|
| `TemporalAdminController` kept out of the MVC slice | Yes. `SecurityConfigTest` is now `@WebMvcTest(controllers = <the test-only controller nested in the test class>)`, so `WebMvcTypeExcludeFilter` (`spring-boot-webmvc-test-4.1.2.jar`, field `controllers`, `getComponentIncludes()`) admits no application controller. `rwb.p3.temporal=false` is also pinned in `@WebMvcTest(properties = …)`. Either measure alone keeps `TemporalAdminController` (`@ConditionalOnProperty` `rwb.p3.temporal`, line 44; Temporal constructor arguments, line 57) out under `dev.ps1`. | `plan.md` line 208 |
| Blob `Config` cases independent of `.env` | Yes. They call `new BlobDocumentStore.Config().blobServiceClient(new BlobProperties(…))` directly. `Config` is a package-private static nested class with an implicit constructor (`BlobDocumentStore.java` line 109); `blobServiceClient` is package-private (line 112); `BlobProperties` is a four-component nested record (line 104). The test sits in the same package (`dochub/storage`) after the move, so all are reachable. No context means `RWB_BLOB_CONNECTION_STRING` (`.env.example` line 23) cannot reach the "neither → `IllegalStateException`" case (line 118). | `plan.md` line 215 |
| Isolation rule and TASK-18 check | Added: `plan.md` line 220 ("Rule for every Spring context in this story's tests"), TASK-18 (6) `.env.example` unchanged and (7) the rule per test (`tasks.md` line 44). The rule text does not match the slice design it lists as compliant (PLAN-022). | `plan.md` line 220; `tasks.md` line 44 |
| Other contexts | `ApiExceptionHandlerTest`, `PlatformInfoControllerTest.info()`, `RecoveryFlywayConfigTest`, `TemporalAdminControllerTest` call classes directly; the binding methods and the other runner cases use `ApplicationYamlEnvironment.isolated()`; the four moved tests keep their assertions and start no new context. | `plan.md` lines 206–216 |

## 2. Earlier findings PLAN-001..016 (held)

The v4 → v5 line diff changes only: the revision lines of the four revised files; `plan.md` lines 58, 208, 213, 215, 218, 220 (new) and 344; `tasks.md` lines 10, 43, 44; `scenarios.md` line 55; PA-12; PG-04; SU-P05; the contract `revision`. None of the changed lines reverts an earlier fix.

| Finding | Result | Evidence |
|---|---|---|
| PLAN-001 TASK-13 row | Held | Note N-1 (`tasks.md` lines 46–52). A script count of unescaped `\|` per table row against its header, over all eight current plan Markdown files (fenced blocks skipped, code spans counted), finds no mismatch. Both contract JSON files parse. |
| PLAN-002 `check` wiring | Held | TASK-01 Verification (`tasks.md` line 27) |
| PLAN-003 Run 1 evidence | Held | TASK-17 quotes the BND-5 line from the `RecoveryBoundaryTest` JUnit XML; no `testLogging` edit (`tasks.md` line 43) |
| PLAN-004 "stricter BND-5" | Held | No "stricter" claim about BND-5 in `plan/` v5 |
| PLAN-005 determinism guard | Held | `plan.md` line 187 |
| PLAN-006 violation unit | Held | `data-model.md` §4 intro (line 61) |
| PLAN-007 BND-5 `{module}` | Held | `data-model.md` line 66 |
| PLAN-008 guard in the red task | Held | TASK-09, TASK-11 (`tasks.md` lines 35, 37) |
| PLAN-009 BND-5 fallback | Held | `scenarios.md` line 50 |
| PLAN-010 dry-run baseline | Held | TASK-00, TASK-01 |
| PLAN-011 source version | Held | `tasks.md` line 10: "`plan.md` v5 and `../specify/spec.md` v4" |
| PLAN-012 binding isolation | Held | `plan.md` line 218; T-TE001-12 values unchanged (`scenarios.md` line 54 identical to v4) |
| PLAN-013 fallback branches | Held | `scenarios.md` lines 21, 50; `data-model.md` lines 48, 50 |
| PLAN-014 T-TE001-15 scan | Held | `scenarios.md` line 57 |
| PLAN-015 compile-red ordering | Held | `tasks.md` lines 31, 34, 36, 85 |
| PLAN-016 one-module reading | Held | SU-P05, SU-P06, PG-04, PA-12, `plan.md` line 58 (citation now per PLAN-020) |

## 3. Plan-gate checks

| Check | Result | Evidence |
|---|---|---|
| Structure: front matter status, `## Requirement Logic To Task Coverage`, `## Pre-submit checks`, task schema (Task, Description, Files, Trace, BLOCKED_BY, Verification) | Pass | `plan.md` lines 274–303, 355–364; `tasks.md` lines 24–44, 87–99 |
| Every scope bullet → task | Pass (S-1..S-15) | `tasks.md` lines 54–72 |
| Tests before code | Pass. Red: TASK-01 (assertion), -03, -06, -10 (compile), -09 (assertion); green: TASK-04, -07, -11. Characterization tests TASK-12 explained (PA-07). | `tasks.md` lines 12, 83–85; `plan.md` lines 253–262 |
| SPEC → task → test | Pass for SPEC-001..026 (021 withdrawn) | `plan.md` lines 307–334; `scenarios.md` §5 |
| AC1–AC7, BR1–BR6 coverage | Pass. `TOTAL_RULES: 13`, `TASK_COVERED_RULES: 13`; X7 shown as moved out of scope (D-RCV-52). | `plan.md` lines 278–303, 363 |
| No new dependency | Pass. Round 5 adds only `SecureRandom`/`Base64` (JDK), `@WebMvcTest` attributes and a direct `Config` call; all on the existing test classpath (`build.gradle.kts` lines 68–84). | TASK-00 (2); TASK-18 (2) |
| No migration (D-RUN-07) | Pass. No `V<nnnn>` or `.sql` name in any current plan file. | search of `plan/` |
| Seams only (D-RUN-08) | Pass. SPEC-016 list; SU-P02, SU-P03. | `plan.md` line 56; `shared-updates.md` |
| Coverage gate 80% | Pass. JaCoCo LINE, INSTRUCTION, BRANCH, METHOD ≥ 0.80 on recovery main classes plus tooling (TASK-01, TASK-13); frontend Vitest 80 × 4 inherited (TASK-16). | `plan.md` lines 189–198, 246–251 |
| No skipped or weakened test | Pass. Moved tests keep their assertions; T-TE001-12 values unchanged; the blank-key case asserts existing behaviour; `blobClientOnlyInDocumentsModule` replaced as SPEC-009 / SPEC-026 require. | `tasks.md` line 98 |
| Personal data | None. Class and package names, local placeholder defaults, keys generated in the test; TASK-17 records `.env` key names only. | `plan.md` lines 343–344; `tasks.md` line 43 |
| Attribution | Pass. A search of the current plan files for approv/accept/dispos/human/sign finds no text recording that a human approved, accepted or disposed of anything. Triage is attributed to the orchestrator (Claude Code) (`agent-run-log.md` lines 57, 72). "Approved spec" denotes the spec that passed its gate; "Accepted deviation D-RCV-39/42" cites client decisions; HV-01 is open for a human, not done. | search of `plan/` |

## 4. D-RUN-18 and D-RUN-19

**CONFIRMED.**

- **T-TE001-14** (`scenarios.md` line 56; `plan.md` line 185; contract `note`, `backend-apis.json` line 63; SU-P02, `shared-updates.md` line 8) states that each published list is exact, `access.api` included, and that later stories extend that exact list in their own merge request: RWB-E1-042 for the D-RUN-19 parameter read interface (P4 `access.api`, implemented in P3 `casewf.config`), `MessageResolver` and `CapabilityCheck`; RWB-E1-043 for the D-RUN-18 reference-load SPI. SU-P02 tells them to update the module map entry, `package-info` and the exact expected list in the same merge request; for `access.api` the list stays `ApiError`, `ApiProblemException` until then.
- **Consistency.** D-RUN-18 and D-RUN-19 in `AI-SDLC-BUILD-LOG.md` (lines 244, 262) put both in P4 `access.api`. RWB-E1-042 revision 10 names three new `access.api` types (`MessageResolver`, `CapabilityCheck`, `CatalogParameterReader`, the last being the D-RUN-19 interface) and an additive `ApiProblemException` constructor; T-TE001-14 compares type names only, so the constructor needs no list change. `access` publishes `[api]`, so no module-map change is needed; P3 → P4 is an existing edge.

## 5. Findings

### REVIEW-RWB-TE-001-PLAN-021 — Low — `SecurityConfigTest`: the test-only controller nested in the test class is excluded from component scanning, so `controllers = <nested>` alone never registers it

- **Affects:** `plan.md` "Coverage tests", `SecurityConfigTest` row (line 208); TASK-12; SPEC-024; T-TE001-10; the 403 MSG-P4-002 case.
- **Evidence:**
  - The row names "`@WebMvcTest(controllers = <the test-only controller nested in the test class>)` … with `@Import` of `SecurityConfig` and, as needed, `ApiExceptionHandler` and `ProblemFactory`". The nested controller is not in the `@Import`.
  - `@WebMvcTest` has no import logic for `controllers`: in `spring-boot-webmvc-test-4.1.2.jar` the attribute only feeds `WebMvcTypeExcludeFilter.getComponentIncludes()`, a scan filter.
  - Component scanning comes from `@SpringBootApplication` on `AceRecoveryApplication`, whose `TypeExcludeFilter` consults every registered exclude filter. One of them is Spring Boot's `TestTypeExcludeFilter`. In `spring-boot-test-4.1.2.jar` (`javap -c`), `match` returns true for a class with `@Test` methods (`isTestClass`, `METHOD_ANNOTATIONS`) and, through `getEnclosingClassName()`, for any class nested in such a class. A controller nested in `SecurityConfigTest` is therefore excluded before the `controllers` filter applies.
  - Result: no handler is mapped in the slice. A request with an `RW-` role passes the filter chain (`SecurityConfig` line 70) and reaches the `DispatcherServlet`, which finds no handler. `NoResourceFoundException` is then mapped by `ApiExceptionHandler` (`@RestControllerAdvice`, line 22) to 404 MSG-P4-003. The planned case "`RW-` role but method check denies → 403 MSG-P4-002" cannot pass as designed, because the `@PreAuthorize` it needs sits on the unregistered controller. The 401 cases and the CORS preflight are decided in the filter chain and are not affected.
  - Also, `ProblemFactory` is a `@Component` (`ProblemFactory.java` line 19), which the slice does not scan. `SecurityConfig.recoverySecurity` needs it (`SecurityConfig.java` line 60), so "as needed" is in fact "always".
- **Fix:**
  - State `@Import` of the nested test controller together with `SecurityConfig` and `ProblemFactory`, and `ApiExceptionHandler` where the case needs it.
  - Keep `controllers = <nested controller>`, so that no application controller joins the slice (PLAN-018).
  - Name the controller's `@PreAuthorize` expression that denies an `RW-` role, so the 403 case is fixed in the plan.

### REVIEW-RWB-TE-001-PLAN-022 — Low — The new "every Spring context" rule, and TASK-18 (7) that checks it, cannot be met by the `SecurityConfigTest` slice as designed

- **Affects:** `plan.md` line 220 ("Rule for every Spring context in this story's tests"); `plan.md` line 208; TASK-18 (7) (`tasks.md` line 44); PLAN-018 fix item 3.
- **Evidence:**
  - **What the rule requires.** A context that is not isolated must pin "every key that a `.env.example` variable could change". The rule lists `RWB_P3_TEMPORAL`, `RWB_P3_DROOLS`, `RWB_MIGRATOR_PASSWORD`, `RWB_BLOB_CONNECTION_STRING`, `RWB_TEMPORAL_CODEC_KEY` "and the others … that bind to `rwb.*` or `spring.*` by relaxed binding".
  - **What the slice pins.** The `SecurityConfigTest` slice runs on the normal environment (system environment included). It pins only "every `rwb.security.*` key it uses and `rwb.p3.temporal=false`" (line 208), and line 220 lists it as applied and compliant. No `.env.example` variable maps to `rwb.security.*`.
  - **Keys left unpinned.** `.env.example` can still change `rwb.p3.drools` (line 20), `rwb.flyway.password` (line 8), `rwb.blob.connection-string` (line 23) and `rwb.temporal.codec-key` (line 27) in that environment.
  - **Variables the rule misses.** The qualifier "by relaxed binding" leaves out variables that reach a key only through an `application.yaml` placeholder. For example `RECOVERY_SVC_PASSWORD` (`.env.example` line 9) reaches `spring.datasource.password` through `${RECOVERY_SVC_PASSWORD:}` (`application.yaml` line 14), and its relaxed name `recovery.svc.password` binds nothing.
  - **Effect.** TASK-18 Verification requires every checklist item "ticked with the command output that proves each". Item (7), read as written, fails for the slice. The design itself is sound: no bean or condition in the slice reads those keys. So the checker must either tick an item that does not hold or demand pins that the row does not plan.
- **Fix:**
  - Reword the rule: "pins every key, read by a bean or condition that the context creates, whose value a `.env.example` variable can change, directly by relaxed binding or through an `application.yaml` placeholder".
  - In the `SecurityConfigTest` row, state that its context reads no other such key (only `rwb.security.*` and `rwb.p3.temporal`). Alternatively, pin the remaining keys as well.
  - Make TASK-18 (7) check that wording.

## 6. Observations (not defects)

- **O-1 RWB-E1-042 moved to revision 10 during this round.** The RWB-E1-042 spec at `aisdlc/output/INC-003-epic-1-RWB-E1-042/specify/spec.md` became revision 10 at 05:28:14, a few seconds before plan v5 was written (05:28:31). Revision 9, which the plan cites by number as round 4 asked, is kept as `spec.run8.md` (CLAR-025 at line 1134). In revision 10 CLAR-025 is at line 1155 and still reads the rule the same way: P3 and P4 count as two modules, so the plan goes to the analyst. PG-04, SU-P05 and PA-12 stay correct in substance. If the planner touches those rows for PLAN-021/022, it may add "(revision 9 kept as `spec.run8.md`)" or move the citation to revision 10.
- **O-2 `jwtDecoder` without a network call.** The same row mocks `JwtDecoder` in the slice and also lists "`jwtDecoder` bean built from the properties without a network call". The mock replaces that bean in the slice. The real method is best covered by a direct call (`new SecurityConfig().jwtDecoder(<RecoverySecurityProperties>)`), which the Builder can add without a plan change.
- **O-3 Carried from earlier rounds.** The module code `P2` is hard-coded in the tooling (not a package literal; T-TE001-15 ignores it). Exact fixture line counts depend on how the fixtures are written.

## 7. Document gaps

No new document gap. PLAN-021 and PLAN-022 are plan-internal defects checked against code and library bytecode, not silences or conflicts in the document set. O-1 concerns another story's run output, not the document set. PG-01..PG-04 (all Blocker = No) stand as recorded.

| ID | Document (name, version, section) | Gap or conflict | Second source | Blocker |
|---|---|---|---|---|
| — | none new | — | — | — |

## 8. Result

```text
PREVIOUS_FINDINGS: PLAN-017, -018, -019, -020 RESOLVED (4/4; PLAN-018 residuals recorded as PLAN-021 and PLAN-022); PLAN-001..016 held (16/16)
PLAN_GATE_FINDINGS: REVIEW-RWB-TE-001-PLAN-021, -022 (both Low)
PLAN_REQUIREMENT_COVERAGE_RESULT (reviewer check): CONFIRMED [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0] [CONTRADICTIONS: 0]
D_RUN_18_19_COMPATIBILITY: CONFIRMED (T-TE001-14 and SU-P02 tell RWB-E1-042 and RWB-E1-043 to extend the exact access.api list in their own merge request)
```

Overall status: **FAIL**. Counts: Critical 0, High 0, Medium 0, Low 2. Under D-RUN-09 the orchestrator (Claude Code) has Low findings fixed rather than carried.

REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
