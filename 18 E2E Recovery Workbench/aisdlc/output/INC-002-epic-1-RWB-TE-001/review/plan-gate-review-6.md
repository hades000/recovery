# Plan gate review: RWB-TE-001 (run INC-002-epic-1-RWB-TE-001), round 6

| Field | Value |
|---|---|
| Stage | Compliance Reviewer, plan gate (`planning-execution-gates.md`), round 6 |
| Story | RWB-TE-001 Recovery module folder and boundary test |
| Reviewed | `plan/plan.md` v6, `plan/tasks.md` v6, `plan/data-model.md` v6, `plan/tests/scenarios.md` v6, `plan/assumptions.md`, `plan/document-gaps.md`, `plan/shared-updates.md`, `plan/contracts/backend-apis.json` (revision v2, byte-identical to `backend-apis.run5.json`), `plan/contracts/frontend-integrations.json` (v1, unchanged), `plan/agent-run-log.md` ("Round 6" section, lines 89–100). The `*.run5` files were used only to compare (line diff v5 → v6). |
| Checked against | Approved spec v4 (`specify/spec.md`, unchanged since spec gate round 5 PASS); plan gate reviews rounds 1–5 (`review/plan-gate-review.md`, `-2.md` to `-5.md`); `AI-SDLC-BUILD-LOG.md` decisions D-RUN-07, -08, -09, -18, -19, -21 and timeline rows of 18 Nov 2026 05:36:54; `aisdlc/docs/open-items.md` OPEN-050; `AGENTS.md` §7, §9; RUN-BRIEF; the code: `SecurityConfig`, `ProblemFactory`, `ApiExceptionHandler`, `ApiError`, `TemporalAdminController`, `PlatformInfoController`, `RecoveryProperties`, `PlatformConfig`, `AceRecoveryApplication`, `backend/src/main/resources/application.yaml` (placeholder names only), `backend/build.gradle.kts`, `.env.example` (key names only; no value read into this report or quoted); Spring Boot 4.1.2 jars read with `javap` and `unzip`: `spring-boot-test` (`TestTypeExcludeFilter`), `spring-boot-webmvc-test` (`WebMvcTest`, `AutoConfigureWebMvc`, `AutoConfigureMockMvc`, `WebMvcTypeExcludeFilter`, `.imports` files), `spring-boot-security-test` (`AutoConfigureMockMvc.imports`), `spring-boot-jackson` (`AutoConfigureJson.imports`); RWB-E1-042 spec revision 11 (`aisdlc/output/INC-003-epic-1-RWB-E1-042/specify/spec.md`) and revision 9 (`spec.run8.md`), CLAR-025 rows only |
| Reviewer | Compliance Reviewer agent, started by the orchestrator (Claude Code). Read only; this file is the only file written. |

## 1. Round-5 findings

The v5 → v6 line diff changes only: the revision lines of `plan.md`, `tasks.md`, `data-model.md`, `scenarios.md`; `plan.md` lines 58, 208, 220; `tasks.md` lines 10, 44; PA-12 (`assumptions.md` line 18); PG-04 (`document-gaps.md` line 12); SU-P05, SU-P06 (`shared-updates.md` lines 11–12); the new "Round 6" section of `agent-run-log.md`. The contract is unchanged.

| Finding | Result | Evidence |
|---|---|---|
| PLAN-021 (Low) nested test controller not scanned | **RESOLVED** (all three fix items). A new defect in the chosen probe path is recorded as PLAN-023. | `plan.md` v6 line 208: (1) `@WebMvcTest(controllers = SecurityConfigTest.ProbeController.class)` with `@Import({SecurityConfigTest.ProbeController.class, SecurityConfig.class, ProblemFactory.class, ApiExceptionHandler.class})`, with the reason stated (Spring Boot 4.1.2 `TestTypeExcludeFilter`; `controllers` is only a scan include filter). Re-checked in the jars: `TestTypeExcludeFilter.match` tests `isTestClass` (JUnit `@Testable` and related annotations) and recurses through `getEnclosingClassName()`; `WebMvcTypeExcludeFilter` holds `controllers` only as a field read by `getComponentIncludes()`. `@Import` registers the nested class directly, so the exclude filter no longer applies. (2) `controllers` stays set, so `TemporalAdminController` (`@ConditionalOnProperty` `rwb.p3.temporal`, line 44; Temporal constructor arguments, line 57) and `PlatformInfoController` (`JdbcTemplate`, line 24) stay out. (3) The method check is named: `@PreAuthorize("hasAuthority('RW-PLATADM')")`; roles become authorities with no prefix (`SecurityConfig.java` Javadoc lines 37–39, converter lines 95–106), and `@EnableMethodSecurity` is on `SecurityConfig` (line 46). `ProblemFactory` is a `@Component` (`ProblemFactory.java` line 19) that `recoverySecurity` needs (`SecurityConfig.java` line 60) and is now always imported. After the relocation `ProblemFactory`, `ApiExceptionHandler` and `SecurityConfig` share `access.internal` with the test (`plan.md` Relocation table, lines 149–150), so the package-private class literals compile. `RecoverySecurityProperties` is registered by `@EnableConfigurationProperties` on `SecurityConfig` (`plan.md` line 165), so importing `SecurityConfig` binds it. |
| PLAN-022 (Low) rule wider than the slice design | **RESOLVED** (all three fix items). A residual in the evidence method is recorded as PLAN-024. | (1) `plan.md` line 220 rewords the rule as round 5 proposed: keys "read by a bean or condition the context creates and whose value a `.env.example` variable can change, directly by relaxed binding or through an `application.yaml` placeholder", with the `RECOVERY_SVC_PASSWORD` → `spring.datasource.password` example; keys no bean reads need no pin. (2) The "Applied" sentence of line 220 states that the `SecurityConfigTest` slice reads only `rwb.security.*` and `rwb.p3.temporal`, both pinned, and creates no `DataSource`, Flyway, Drools, Temporal or Blob bean. (3) TASK-18 (7) (`tasks.md` line 44) checks that wording through the (a)–(d) table and is ticked when (d) has no unpinned entry. |

### 1.1 Can TASK-18 (7) be ticked from evidence?

| Step of `plan.md` line 220 "How the Builder lists the keys" | Evidence available | Result |
|---|---|---|
| (a) classes the context creates | `@Import` list and `controllers` value are in the test source. The slice auto-configurations are in the `.imports` files: `AutoConfigureWebMvc.imports` and `AutoConfigureMockMvc.imports` in `spring-boot-webmvc-test-4.1.2.jar`, `AutoConfigureMockMvc.imports` in `spring-boot-security-test-4.1.2.jar`, and `AutoConfigureJson.imports` in `spring-boot-jackson-4.1.2.jar` (pulled in because `AutoConfigureWebMvc` is meta-annotated with `@AutoConfigureJson`). The last is not a test jar; the `debug=true` condition report alternative covers it. | Obtainable. However, the definition leaves out classes that the listed classes register, such as `RecoverySecurityProperties` (PLAN-024). |
| (b) keys those classes read | The grep `@ConfigurationProperties\|@ConditionalOnProperty\|@Value\|getProperty` over the (a) sources. For the slice that is `SecurityConfig`, `ProblemFactory`, `ApiExceptionHandler`, `ProbeController`; none contains a match (after the relocation `SecurityConfig` carries `@EnableConfigurationProperties`, which the pattern does not match). | Obtainable, but it yields no `rwb.security.*` key, unlike the "Applied" result (PLAN-024). |
| (c) `.env.example`-reachable keys | 13 key names in `.env.example`, in relaxed form, plus 16 placeholders in `application.yaml` (lines 12–100). Names only. | Obtainable. The `spring.*` key in (c) is `spring.datasource.password`; no slice auto-configuration creates a `DataSource`. No `.env.example` key reaches `rwb.security.*` (those placeholders use variables that `.env.example` does not define). |
| (d) intersection with pins | `rwb.p3.temporal`, pinned in `@WebMvcTest(properties = …)`. | Tick holds for this slice. |

So the tick is reachable and correct for the one non-isolated context. As written, however, the method would not by itself produce the (b) row that the plan reports (see PLAN-024).

## 2. One-module settlement

| Check | Result | Evidence |
|---|---|---|
| PA-12 cites D-RUN-21 | Yes | `assumptions.md` line 18 cites "build decision D-RUN-21 (`AI-SDLC-BUILD-LOG.md` decisions table, 18 Nov 2026 05:36, the orchestrator (Claude Code))". `AI-SDLC-BUILD-LOG.md` line 44: D-RUN-21, 2026-11-18T05:36, "touches one module" in AGENTS.md §7 and §9 means the ACE module (recovery); made by the orchestrator (Claude Code), with tech-lead ratification an open item. Timeline line 294 (05:36:54) records that it settles TE-001 PLAN-016/PA-12 and E1-042 CLAR-025. |
| SU-P05 marked applied | Yes | `shared-updates.md` line 11: "**Status: applied** by build decision D-RUN-21 … (ACE module, recovery)". |
| SU-P06 cites OPEN-050 (tech lead, pending ratification) | Yes | `shared-updates.md` line 12: "**Status: applied** as open item OPEN-050 … (owner: recovery tech lead, the AGENTS.md §9 'Plan approved' owner; pending ratification), which also covers D-RUN-18..21". `open-items.md` line 40, section "Open": OPEN-050 "Ratify or replace" D-RUN-18 to D-RUN-21 and "Define 'module' … at source (gap PG-04/GC-1)"; owner "Recovery tech lead (AGENTS.md §9 Plan approved owner)"; raised in INC-002 plan SU-P05/SU-P06. `AGENTS.md` line 155: Plan approved owner is the tech lead. |
| PG-04 / GC-1 kept with Blocker = No | Yes | `document-gaps.md` line 12: Blocker "No"; "The gap stays open at source until OPEN-050 is closed." |
| Wording matches sources, no human approval recorded | Yes | `plan.md` line 58, PA-12, PG-04, SU-P05/P06 and `agent-run-log.md` line 91 all attribute D-RUN-21 and the triage to the orchestrator (Claude Code) and describe OPEN-050 as "pending ratification". No text says the tech lead or any person approved, ratified or accepted D-RUN-21. PA-12's "Impact if wrong" column keeps the design-module outcome open ("If the tech lead replaces D-RUN-21 under open item OPEN-050 …"). The RWB-E1-042 spec revision 11 (`spec.md` line 555 and rows R7-3, R9-3) now applies D-RUN-21 the same way and also treats it as not ratified, so the two stories agree. |

## 3. Earlier findings PLAN-001..020 (held)

None of the changed lines reverts an earlier fix.

| Finding | Result | Evidence |
|---|---|---|
| PLAN-001 table rows | Held | Script count of unescaped `\|` per table row against its header over the eight current plan Markdown files (fenced blocks skipped): 0 mismatches. Both contract JSON files parse. |
| PLAN-002 `check` wiring; PLAN-010 dry-run baseline | Held | TASK-00, TASK-01 unchanged |
| PLAN-003 Run 1 evidence; PLAN-019 Run 3 freshness | Held | TASK-17 (`tasks.md` line 43) unchanged: JUnit XML quote, `cleanTest` before Run 3 |
| PLAN-004 "stricter BND-5" | Held | No such claim in `plan/` v6 |
| PLAN-005 determinism guard; PLAN-008 guard in the red task; PLAN-015 compile-red ordering | Held | `plan.md` line 187; `tasks.md` lines 31, 34–37, 85 unchanged |
| PLAN-006, -007 violation unit, BND-5 `{module}` | Held | `data-model.md` §4 unchanged apart from the revision line |
| PLAN-009, -013 fallback branches | Held | `scenarios.md` lines 21, 50 unchanged |
| PLAN-011 source version | Held | `tasks.md` line 10: "`plan.md` v6 and `../specify/spec.md` v4" |
| PLAN-012 binding isolation | Held | `plan.md` line 218 and `scenarios.md` line 54 unchanged |
| PLAN-014 T-TE001-15 scan | Held | `scenarios.md` line 57 unchanged |
| PLAN-016 one-module reading | Held, now settled | §2 above |
| PLAN-017 codec key in `TemporalConfigTest` | Held | `plan.md` line 213 unchanged |
| PLAN-018 other contexts and `.env` | Held | `controllers` still limited and `rwb.p3.temporal=false` still pinned (line 208); Blob `Config` cases still called directly (line 215) |
| PLAN-020 contract revision and citation | Held | Contract unchanged (v2); citations by revision number kept |

## 4. Plan-gate checks

| Check | Result | Evidence |
|---|---|---|
| Structure: front matter status, `## Requirement Logic To Task Coverage`, `## Pre-submit checks`, task schema (Task, Description, Files, Trace, BLOCKED_BY, Verification) | Pass | `plan.md` and `tasks.md` sections unchanged from v5; TASK-18 keeps all six columns |
| Every scope bullet → task | Pass (S-1..S-15) | `tasks.md` lines 54–72 |
| Tests before code | Pass. Red TASK-01, -03, -06, -09, -10; green TASK-04, -07, -11; characterization TASK-12 (PA-07) | `tasks.md` lines 12, 83–85 |
| SPEC → task → test | Pass for SPEC-001..026 (021 withdrawn) | `plan.md` traceability section; `scenarios.md` §5 |
| AC1–AC7, BR1–BR6 coverage | Pass, 13/13 | `plan.md` line 363: `PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]` |
| No new dependency | Pass. Round 6 adds only annotations and a nested test controller; `spring-boot-starter-webmvc-test` and `spring-boot-starter-security-test` are already test dependencies (`build.gradle.kts` lines 74, 76) | TASK-00 (2), TASK-18 (2) |
| No migration (D-RUN-07) | Pass. No `V<nnnn>` or `.sql` name in any current plan file | search of `plan/` |
| Seams only (D-RUN-08) | Pass | SPEC-016 list; SU-P02, SU-P03 unchanged |
| Coverage gate 80% | Pass. JaCoCo LINE, INSTRUCTION, BRANCH, METHOD ≥ 0.80 on recovery main classes plus tooling; Vitest 80 × 4 inherited | `plan.md` lines 189–198, 246–251; TASK-01, -13, -16 |
| No skipped or weakened test | Pass. No `@Disabled` or skip; moved tests keep their assertions | `plan.md` line 178; `tasks.md` line 98 |
| Personal data | None. Synthetic roles (`RW-TEST`, `RW-PLATADM`), class and package names, test-generated keys; `.env.example` key names only | search of `plan/` for e-mail, 13-digit and phone patterns: none |
| Attribution | Pass. A search of the current plan files for approv / accept / dispos / human / sign / ratif finds no text recording that a human approved, accepted, ratified or disposed of anything. "Plan approved" names the AGENTS.md §9 gate and its owner; "pending ratification" is open. Triage is attributed to the orchestrator (Claude Code) (`agent-run-log.md` line 91). | search of `plan/` |

## 5. D-RUN-18 and D-RUN-19

**CONFIRMED.** T-TE001-14 (`scenarios.md` line 56, unchanged), `plan.md` line 185 and SU-P02 (`shared-updates.md` line 8) state that each published list is exact, `access.api` included (`ApiError`, `ApiProblemException` until a later story adds its type). They also state that later stories extend that exact list in their own merge request: RWB-E1-042 for the D-RUN-19 parameter read interface (P4 `access.api`, implemented in P3 `casewf.config`), `MessageResolver` and `CapabilityCheck`; RWB-E1-043 for the D-RUN-18 reference-load SPI. SU-P02 asks them to update the module map entry, `package-info` and the exact expected list in the same merge request. RWB-E1-042 revision 11 (`spec.md` line 84) names exactly those three new `access.api` types plus an additive `ApiProblemException` constructor, which a type-name comparison does not affect. `access` already publishes `api`; P3 → P4 is an existing edge. Both decisions stay possible.

## 6. Findings

### REVIEW-RWB-TE-001-PLAN-023 — Low — `SecurityConfigTest` probe path `/test/probe` is outside `/api/recovery/**`, so `anyRequest().denyAll()` refuses it and the planned 200 case cannot pass

- **Affects:** `plan.md` "Coverage tests", `SecurityConfigTest` row (line 208); TASK-12; SPEC-024; T-TE001-10.
- **Evidence:**
  - The row maps `ProbeController` to `GET /test/probe` and plans "token with role `RW-TEST` only … on `/test/probe` → 403 MSG-P4-002; token with `RW-PLATADM` → 200".
  - `SecurityConfig.recoverySecurity` (`SecurityConfig.java` lines 66–71), which the relocation moves without a behaviour change (`plan.md` line 150), permits `OPTIONS /**` and `/actuator/health/**`, `/actuator/info`. It requires `RW-PLATADM` for `/actuator/**`, applies `HOLDS_WORKBENCH_ROLE` to `/api/recovery/**`, and ends with `.anyRequest().denyAll()`. `/test/probe` matches only `anyRequest()`.
  - **200 case.** With an `RW-PLATADM` token the `AuthorizationFilter` denies the request before the `DispatcherServlet`. The `accessDeniedHandler` (lines 74–76) writes 403 `NOT_PERMITTED` (`ApiError.java` line 22, MSG-P4-002) because the principal holds an `RW-` role. The planned 200 assertion fails.
  - **403 case.** The `RW-TEST` case returns 403 MSG-P4-002 for the same URL-rule reason, not because `@PreAuthorize("hasAuthority('RW-PLATADM')")` denied it. The case therefore does not exercise the method check it was written for. That path runs through `AuthorizationDeniedException` (an `AccessDeniedException`) into `ApiExceptionHandler.forbidden` (lines 39–42), and the probe's package is inside the advice's `basePackages` (line 22).
  - **CORS cases.** The CORS source is registered only for `/api/**` (`SecurityConfig.java` line 115). A preflight sent to `/test/probe` would get no CORS headers for the configured origin either, so "configured origin allowed" also needs a path under `/api/`. The row does not name the preflight path.
- **Fix:**
  - Map `ProbeController` under `/api/recovery/` (for example `GET /api/recovery/v1/test/probe`). The URL rule then lets any `RW-` role through, and the `@PreAuthorize` check decides 403 versus 200.
  - State that the CORS preflight cases use that path or another path under `/api/`.
  - The 401 cases are unchanged by the move (anonymous → entry point; no `RW-` role → `NO_ROLE`).

### REVIEW-RWB-TE-001-PLAN-024 — Low — The key-listing method (a)/(b) omits classes that the imported classes register, so the evidence table built as written does not show the `rwb.security.*` keys the plan reports

- **Affects:** `plan.md` line 220 "How the Builder lists the keys" (a) and (b); TASK-18 (7) (`tasks.md` line 44).
- **Evidence:**
  - **Step (a) is incomplete.** It defines the classes the context creates as "the `@Import` list, the `controllers` value and the slice's auto-configurations". `RecoverySecurityProperties` is in none of these. It is registered by `@EnableConfigurationProperties` on `SecurityConfig` (`plan.md` line 165).
  - **The grep in (b) misses it.** Step (b) greps the (a) sources for `@ConfigurationProperties\|@ConditionalOnProperty\|@Value\|getProperty`. Over `SecurityConfig`, `ProblemFactory`, `ApiExceptionHandler` and `ProbeController` it finds nothing: `@EnableConfigurationProperties` does not match `@ConfigurationProperties`, because the `@` is followed by `Enable`.
  - **Contradiction with the plan.** The "Applied" sentence of the same paragraph says the slice reads `rwb.security.*` "through `RecoverySecurityProperties`". A checker who follows the method literally gets a (b) row that contradicts the plan's stated result.
  - **The same gap applies elsewhere.** It would also miss any key read by a `@Bean` return type or a nested `@Configuration` of an imported class.
  - **Auto-configuration source.** Step (a) points to the `.imports` files "in the Spring Boot test jars", but the slice also pulls `AutoConfigureJson.imports` from `spring-boot-jackson-4.1.2.jar`, which is not a test jar. Step (b) names no source for "the property prefixes of the auto-configurations".
  - **Effect.** For this slice the final tick in (d) is still right: no `.env.example` key reaches `rwb.security.*`. The flaw is in the method, which can under-collect.
- **Fix:**
  - In (a), add the classes registered by the listed classes: `@EnableConfigurationProperties` values, `@Bean` method return types and nested `@Configuration` classes.
  - In (b), add `@EnableConfigurationProperties` to the grep pattern, or grep the registered `@ConfigurationProperties` records as well.
  - In (a), say "the `.imports` files the slice annotations reach (including `AutoConfigureJson`)", or make the `debug=true` condition report the primary source.
  - In (b), take auto-configuration prefixes from `META-INF/spring-configuration-metadata.json` of the jars that hold them.

## 7. Observations (not defects)

- **O-1 RWB-E1-042 citation.** The plan cites the RWB-E1-042 spec "revision 9" at the path `spec.md`. That file is now revision 11 (written 05:41), and revision 9 is kept as `spec.run8.md`. Revision 11 applies D-RUN-21 and records CLAR-025 as settled but not ratified (OPEN-050), so the citation, which names a revision, stays accurate for what revision 9 said. When the planner next touches PG-04, SU-P05 or PA-12, it may add "(revision 9 kept as `spec.run8.md`; revision 11 applies D-RUN-21)".
- **O-2 `rwb.p3.temporal` in (b).** The "Applied" sentence counts `rwb.p3.temporal` as read by the slice through the `TemporalAdminController` condition. `controllers` keeps that class out of the scan, so the condition is never evaluated. Pinning it is harmless defence in depth.
- **O-3 Redundant import.** `ApiExceptionHandler` is a `@RestControllerAdvice`, which `WebMvcTypeExcludeFilter` already includes by default (`ControllerAdvice` in `getDefaultIncludes`). The explicit `@Import` is redundant but harmless; Spring keeps the scanned definition.
- **O-4 Carried.** O-2 of round 5 (`jwtDecoder` best covered by a direct call) and O-3 of round 5 (module code `P2` in tooling; fixture line counts) stand.

## 8. Document gaps

No new document gap. PLAN-023 and PLAN-024 are plan-internal defects checked against the code and the Spring Boot 4.1.2 jars, not silences or conflicts in the document set. PG-01..PG-04 (all Blocker = No) stand as recorded; PG-04 is now carried to the document owners by OPEN-050.

| ID | Document (name, version, section) | Gap or conflict | Second source | Blocker |
|---|---|---|---|---|
| — | none new | — | — | No |

## 9. Result

```text
PREVIOUS_FINDINGS: PLAN-021 RESOLVED, PLAN-022 RESOLVED (2/2; new residuals recorded as PLAN-023 and PLAN-024); PLAN-001..020 held (20/20)
ONE_MODULE_SETTLEMENT: CONFIRMED (PA-12 cites D-RUN-21; SU-P05 applied; SU-P06 applied as OPEN-050, tech lead, pending ratification; PG-04/GC-1 Blocker = No; no human approval recorded)
PLAN_GATE_FINDINGS: REVIEW-RWB-TE-001-PLAN-023, -024 (both Low)
PLAN_REQUIREMENT_COVERAGE_RESULT (reviewer check): CONFIRMED [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0] [CONTRADICTIONS: 0]
D_RUN_18_19_COMPATIBILITY: CONFIRMED (T-TE001-14 and SU-P02 tell RWB-E1-042 and RWB-E1-043 to extend the exact access.api list in their own merge request)
```

Overall status: **FAIL**. Counts: Critical 0, High 0, Medium 0, Low 2. Under D-RUN-09 the orchestrator (Claude Code) has Low findings fixed rather than carried.

REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
