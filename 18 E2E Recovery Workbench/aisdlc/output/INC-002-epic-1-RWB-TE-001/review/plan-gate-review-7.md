# Plan gate review: RWB-TE-001 (run INC-002-epic-1-RWB-TE-001), round 7

| Field | Value |
|---|---|
| Stage | Compliance Reviewer, plan gate (`planning-execution-gates.md`), round 7 |
| Story | RWB-TE-001 Recovery module folder and boundary test |
| Reviewed | `plan/plan.md` v7, `plan/tasks.md` v7, `plan/data-model.md` v7, `plan/tests/scenarios.md` v7, `plan/assumptions.md`, `plan/document-gaps.md`, `plan/shared-updates.md`, `plan/contracts/backend-apis.json` (revision v2, byte-identical to `backend-apis.run6.json`), `plan/contracts/frontend-integrations.json` (v1, unchanged), `plan/agent-run-log.md` ("Round 7" section, lines 101–112). The `*.run6` files were used only to compare (line diff v6 → v7). |
| Checked against | Approved spec v4 (`specify/spec.md`, unchanged since spec gate round 5 PASS); plan gate reviews rounds 1–6 (`review/plan-gate-review.md`, `-2.md` to `-6.md`); `AI-SDLC-BUILD-LOG.md` decisions D-RUN-07, -08, -09, -18, -19, -21 and timeline rows 293–294; `aisdlc/docs/open-items.md` OPEN-050 (line 40, section "Open"); `AGENTS.md` §7, §9 (line 155); RUN-BRIEF; the code: `SecurityConfig`, `ApiExceptionHandler`, `ProblemFactory`, `ApiError`, `RecoveryProperties` (all still in `platform/` today, as the plan's relocation table expects), `backend/src/main/resources/application.yaml` (placeholder names only), `backend/build.gradle.kts`, `.env.example` (key names only; no value read into this report or quoted); Spring Boot 4.1.2 jars read with `javap` and `unzip`: `spring-boot-webmvc-test` (`WebMvcTest` meta-annotations, `AutoConfigureWebMvc.imports`, `AutoConfigureMockMvc.imports`, `spring-configuration-metadata.json`, `additional-spring-configuration-metadata.json`), `spring-boot-security-test` (`AutoConfigureMockMvc.imports`), `spring-boot-security-oauth2-resource-server` (`WebMvcTest.imports`, `spring-configuration-metadata.json`), `spring-boot-jackson` (`AutoConfigureJson.imports`, `spring-configuration-metadata.json`), `spring-boot-webmvc` and `spring-boot-security` (metadata files present) |
| Reviewer | Compliance Reviewer agent, started by the orchestrator (Claude Code). Read only; this file is the only file written. |

## 1. Round-6 findings

The v6 → v7 line diff changes only: the revision lines of `plan.md`, `tasks.md`, `data-model.md`, `scenarios.md`; `plan.md` lines 58, 208, 220; `tasks.md` lines 10, 44; PA-12 (`assumptions.md` line 18); PG-04 (`document-gaps.md` line 12); SU-P05 (`shared-updates.md` line 11); the new "Round 7" section of `agent-run-log.md`. `data-model.md` and `scenarios.md` change only in their revision lines. The contract is unchanged.

| Finding | Result | Evidence |
|---|---|---|
| PLAN-023 (Low) probe path outside `/api/recovery/**` | **RESOLVED** (all three fix items) | `plan.md` v7 line 208: (1) `ProbeController` has `GET /api/recovery/v1/test/probe`, and the row states why: the URL rule `HOLDS_WORKBENCH_ROLE` lets any `RW-` role through and the method check decides 403 or 200; a path outside would hit `anyRequest().denyAll()`. (2) The CORS preflight cases use `OPTIONS /api/recovery/v1/test/probe`, and the row notes that the CORS source covers `/api/**` only. (3) The 401 cases are unchanged. Re-checked against the code, which the relocation moves without a behaviour change (`plan.md` line 150): `SecurityConfig.java` lines 66–71 (`OPTIONS /**` permitted, `/api/recovery/**` → `HOLDS_WORKBENCH_ROLE`, `anyRequest().denyAll()`), line 115 (`registerCorsConfiguration("/api/**", …)`), lines 72–76 (entry point → `NO_ROLE`; `accessDeniedHandler` → `NOT_PERMITTED` only when the principal holds an `RW-` role, else `NO_ROLE`). Walking each planned case: no token → anonymous fails `HOLDS_WORKBENCH_ROLE` → entry point → 401 MSG-P4-001; token without an `RW-` role → `accessDeniedHandler` → 401 MSG-P4-001 (`ApiError.java` line 17); `RW-TEST` → passes the URL rule, `@PreAuthorize("hasAuthority('RW-PLATADM')")` throws `AuthorizationDeniedException` (an `AccessDeniedException`) inside the `DispatcherServlet`, and `ApiExceptionHandler.forbidden` (`ApiExceptionHandler.java` lines 39–42) returns 403 MSG-P4-002 (`ApiError.java` line 22), because the probe's package `th.co.scb.ace.demo.recovery.access.internal` is inside the advice's `basePackages` (line 22); `RW-PLATADM` → both checks pass → 200; preflight from a configured origin → the CORS filter answers it on the `/api/**` source; other origin → rejected. `@EnableMethodSecurity` stays on `SecurityConfig` (line 46). Every planned assertion can now pass, and the 403 case exercises the method check it was written for. |
| PLAN-024 (Low) key-listing method omits registered classes | **RESOLVED** (all four fix items) | `plan.md` v7 line 220 "How the Builder lists the keys": (1) (a) now adds "the classes those register (`@EnableConfigurationProperties` values, `@Bean` method return types, nested `@Configuration` classes)". (2) (b) greps `@ConfigurationProperties\|@EnableConfigurationProperties\|@ConditionalOnProperty\|@Value\|getProperty` "with each `@ConfigurationProperties` record found that way grepped as well". (3) Auto-configurations come "primarily from the condition evaluation report of one local run with `debug=true`", cross-checked against "the `.imports` files the slice annotations reach, wherever they sit (for example `AutoConfigureJson.imports` in `spring-boot-jackson`, not a test jar)". (4) Auto-configuration prefixes come from `META-INF/spring-configuration-metadata.json` of the jars that hold them. TASK-18 (7) (`tasks.md` line 44) repeats (a) and (b) in the same terms. The "Applied" sentence now names `@EnableConfigurationProperties` on `SecurityConfig` as the source of `rwb.security.*`, and calls `rwb.p3.temporal` a defence-in-depth pin (round-6 O-2). |

### 1.1 Does the method now find `rwb.security.*`, and can TASK-18 (7) be ticked from evidence?

| Step of `plan.md` line 220 | What the Builder gets for the `SecurityConfigTest` slice | Result |
|---|---|---|
| (a) classes the context creates | `@Import`: `ProbeController`, `SecurityConfig`, `ProblemFactory`, `ApiExceptionHandler`; `controllers`: `ProbeController`. Registered by them: `RecoverySecurityProperties` (`@EnableConfigurationProperties` on `SecurityConfig`, `plan.md` line 165), `SecurityFilterChain` and `JwtDecoder` (`@Bean` return types, `SecurityConfig.java` lines 59–60, 83–84). Auto-configurations: `@WebMvcTest` is meta-annotated with `@ImportAutoConfiguration`, `@AutoConfigureWebMvc` and `@AutoConfigureMockMvc` (read with `javap`). It therefore reaches `WebMvcTest.imports` in `spring-boot-security-oauth2-resource-server-4.1.2.jar` (`OAuth2ResourceServerAutoConfiguration`, `OAuth2ResourceServerWebSecurityAutoConfiguration`), `AutoConfigureWebMvc.imports` and `AutoConfigureMockMvc.imports` in `spring-boot-webmvc-test`, `AutoConfigureMockMvc.imports` in `spring-boot-security-test`, and `AutoConfigureJson.imports` in `spring-boot-jackson`. The resource-server starter is on the classpath (`build.gradle.kts` line 43). The v7 wording "wherever they sit", with the `debug=true` report as the primary source, covers all of them. | Obtainable and complete |
| (b) keys those classes read | The extended grep over `SecurityConfig` matches `@EnableConfigurationProperties`. The follow-up grep over `RecoverySecurityProperties` matches `@ConfigurationProperties` with prefix `rwb.security` (five keys, `plan.md` line 165). `ProblemFactory`, `ApiExceptionHandler` and `ProbeController` match nothing (`ProblemFactory.java`, `ApiExceptionHandler.java` read in full). Auto-configuration prefixes are available: `spring-configuration-metadata.json` is present in `spring-boot-webmvc`, `spring-boot-webmvc-test`, `spring-boot-security`, `spring-boot-security-oauth2-resource-server` and `spring-boot-jackson`, and it includes condition-only keys from the additional metadata (for example `spring.test.mockmvc.webdriver.enabled`). | `rwb.security.*` is now found, matching the "Applied" sentence |
| (c) `.env.example`-reachable keys | 13 key names in `.env.example` (relaxed form), plus the `application.yaml` placeholders (lines 12–100). Names only. The only `spring.*` key reached is `spring.datasource.password` (through `RECOVERY_SVC_PASSWORD`). No `.env.example` key reaches `rwb.security.*`: its placeholders use OIDC and CORS variables that `.env.example` does not define. No `.env.example` key reaches `spring.security.oauth2.resourceserver.*`: `application.yaml` has no such placeholder. | Obtainable |
| (d) intersection with pins | No slice auto-configuration reads `spring.datasource.*`; `rwb.security.*` and `rwb.p3.temporal` are pinned in `@WebMvcTest(properties = …)`. No unpinned entry. | Tick holds and is evidenced |

## 2. One-module settlement

| Check | Result | Evidence |
|---|---|---|
| PA-12 cites D-RUN-21 | Yes | `assumptions.md` line 18 cites "build decision D-RUN-21 (`AI-SDLC-BUILD-LOG.md` decisions table, 18 Nov 2026 05:36, the orchestrator (Claude Code))". `AI-SDLC-BUILD-LOG.md` line 44: D-RUN-21, 2026-11-18T05:36, "touches one module" means the ACE module (recovery). Timeline line 294 states that it settles TE-001 PLAN-016/PA-12 and E1-042 CLAR-025, with OPEN-050 "for tech-lead ratification of D-RUN-18..21". |
| SU-P05 and SU-P06 applied | Yes | `shared-updates.md` line 11 (SU-P05): "**Status: applied** by build decision D-RUN-21". Line 12 (SU-P06): applied as open item OPEN-050 (owner: recovery tech lead; pending ratification). |
| OPEN-050 pending ratification | Yes | `open-items.md` line 40, section "Open" (line 7): "Ratify or replace" D-RUN-18 to D-RUN-21 and define "module" at source (gap PG-04/GC-1); owner "Recovery tech lead (AGENTS.md §9 Plan approved owner)"; due "Before the first of these stories merges". `AGENTS.md` line 155: the Plan approved owner is the tech lead. |
| PG-04 / GC-1 Blocker = No | Yes | `document-gaps.md` line 12: Blocker "No"; "The gap stays open at source until OPEN-050 is closed." |
| No human approval recorded | Yes | `plan.md` line 58, PA-12, PG-04, SU-P05/P06 and `agent-run-log.md` lines 98 and 104 attribute D-RUN-21 and the triage to the orchestrator (Claude Code). OPEN-050 is described as "pending ratification". The only v7 change in this area adds the citation note "revision 9 kept as `spec.run8.md`, revision 11 applies D-RUN-21" (round-6 O-1), which records no approval. |

## 3. Earlier findings PLAN-001..022 (held)

None of the changed lines reverts an earlier fix.

| Finding | Result | Evidence |
|---|---|---|
| PLAN-001 table rows | Held | Script count of unescaped `\|` per table row against its header, over the eight current plan Markdown files (fenced blocks skipped): 0 mismatches. Both contract JSON files parse. |
| PLAN-002 `check` wiring; PLAN-010 dry-run baseline | Held | TASK-00, TASK-01 unchanged |
| PLAN-003 Run 1 evidence; PLAN-019 Run 3 freshness | Held | TASK-17 and T-TE001-13 (`scenarios.md` line 55) unchanged |
| PLAN-004 "stricter BND-5" | Held | No such claim in `plan/` v7 |
| PLAN-005, -008, -015 determinism guard and red ordering | Held | `plan.md` line 187; `tasks.md` task table and dependency graph unchanged |
| PLAN-006, -007 violation unit, BND-5 `{module}` | Held | `data-model.md` changes only in its revision line |
| PLAN-009, -013 fallback branches | Held | `scenarios.md` changes only in its revision line |
| PLAN-011 source version | Held | `tasks.md` line 10: "`plan.md` v7 and `../specify/spec.md` v4" |
| PLAN-012 binding isolation | Held | `plan.md` line 218; T-TE001-12 (`scenarios.md` line 54) unchanged |
| PLAN-014 T-TE001-15 scan | Held | `scenarios.md` line 57 unchanged |
| PLAN-016 one-module reading | Held, settled | §2 above |
| PLAN-017 codec key in `TemporalConfigTest` | Held | `plan.md` line 213 unchanged |
| PLAN-018 other contexts and `.env` | Held | `controllers` still limited and `rwb.p3.temporal=false` still pinned (line 208); Blob `Config` cases still called directly (line 220) |
| PLAN-020 contract revision and citation | Held | Contract v2 unchanged |
| PLAN-021 nested controller in `@Import` | Held | `plan.md` line 208 keeps `@Import({SecurityConfigTest.ProbeController.class, SecurityConfig.class, ProblemFactory.class, ApiExceptionHandler.class})` with `controllers` set |
| PLAN-022 rule wording and TASK-18 (7) | Held | `plan.md` line 220 rule sentence unchanged; TASK-18 (7) keeps the same tick condition |

## 4. Plan-gate checks

| Check | Result | Evidence |
|---|---|---|
| Structure: front matter (`status: "SUCCESS"`), `## Requirement Logic To Task Coverage` (line 274), `## Pre-submit checks` (`tasks.md` line 87), task schema (Task, Description, Files, Trace, BLOCKED_BY, Verification) | Pass | Sections unchanged; TASK-18 keeps all six columns |
| Every scope bullet → task | Pass (S-1..S-15) | `tasks.md` lines 54–72 |
| Tests before code | Pass. Red TASK-01, -03, -06, -09, -10; green TASK-04, -07, -11; characterization TASK-12 (PA-07) | `tasks.md` line 12; `plan.md` line 256 |
| SPEC → task → test | Pass for SPEC-001..026 (021 withdrawn) | `plan.md` "SPEC to task map" (line 305); `scenarios.md` §5 |
| AC1–AC7, BR1–BR6 coverage | Pass, 13/13 | `plan.md` line 363: `PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]` |
| No new dependency | Pass. Round 7 changes only a test path and the evidence method. `spring-boot-starter-webmvc-test`, `spring-boot-starter-security-test` (`build.gradle.kts` lines 74, 76) and the resource-server starter (line 43) already exist. | TASK-00 (2), TASK-18 (2) |
| No migration (D-RUN-07) | Pass. No `V<nnnn>__`, `V<seq>` or `.sql` name in any current plan file | search of `plan/` |
| Seams only (D-RUN-08) | Pass | SPEC-016 list; SU-P02, SU-P03 unchanged |
| Coverage gate 80% | Pass. JaCoCo LINE, INSTRUCTION, BRANCH, METHOD ≥ 0.80 on recovery main classes plus tooling; Vitest 80 × 4 inherited | `plan.md` lines 49, 91, 195, 248–251; TASK-01, -13; T-TE001-10 |
| No skipped or weakened test | Pass. No `@Disabled`, `@Ignore`, skip or assumption; moved tests keep their assertions | search of `plan/`; `tasks.md` line 98 |
| Personal data | None. Synthetic roles (`RW-TEST`, `RW-PLATADM`), class and package names, test-generated keys; `.env.example` and `application.yaml` cited by key name only | search of `plan/` for e-mail, 13-digit, phone and `+66` patterns: none |
| Attribution | Pass. A search of the current plan files for approv / accept / dispos / human / sign / ratif finds no text recording that a human approved, accepted, ratified or disposed of anything. "Plan approved" names the AGENTS.md §9 gate and its owner; HV-01 is "open for a human"; OPEN-050 is "pending ratification". The round-6 triage is attributed to the orchestrator (Claude Code) (`agent-run-log.md` line 104). | search of `plan/` |

## 5. D-RUN-18 and D-RUN-19

**CONFIRMED.** T-TE001-14 (`scenarios.md` line 56), `plan.md` line 185 and SU-P02 (`shared-updates.md` line 8) are unchanged. They state that each published list is exact, `access.api` included (`ApiError`, `ApiProblemException`), and that "later stories extend the exact list in their own merge request". The named cases are RWB-E1-042 (the D-RUN-19 parameter read interface in P4 `access.api`, implemented in P3 `casewf.config`, plus `MessageResolver` and `CapabilityCheck`) and RWB-E1-043 (the D-RUN-18 reference-load SPI in `access.api`). SU-P02 asks those stories to update the module map entry, the `@NamedInterface` `package-info` and the exact expected list in the same merge request. `access` already publishes `api`, and P3 → P4 is an existing edge (`casewf.admin` → `access.api`, `plan.md` relocation paragraph), so both decisions stay possible. The test-only `ProbeController` lives in test sources, so it does not enter the main-class published surface that T-TE001-14 compares.

## 6. Findings

None. No new finding is raised in round 7.

## 7. Observations (not defects)

- **O-1 `/actuator/health` in the slice.** `plan.md` line 208 expects `/actuator/health` "open". `@WebMvcTest` maps no actuator endpoint, so the request passes the URL rule (`SecurityConfig.java` line 68) and then gets 404 from MVC. `ApiExceptionHandler` does not apply, because its `basePackages` selector excludes the resource handler. The Builder should assert "not 401 and not 403", not 200. The plan's wording already permits this.
- **O-2 Round-6 auto-configuration list.** The round-6 review's step (a) evidence listed four `.imports` files and missed `WebMvcTest.imports` in `spring-boot-security-oauth2-resource-server-4.1.2.jar`, which `@WebMvcTest` reaches through `@ImportAutoConfiguration`. The v7 method covers it ("wherever they sit", with the `debug=true` report as the primary source). Its prefix `spring.security.oauth2.resourceserver.*` is not reachable from `.env.example`, so the conclusion is unchanged.
- **O-3 Framework `@Import`s.** Step (a) does not list classes that framework `@Enable*` annotations import, such as `@EnableMethodSecurity`. Spring Security's configuration reads no Spring Boot property, so the omission does not affect (d) for this slice.
- **O-4 Build log.** `AI-SDLC-BUILD-LOG.md` has no timeline row yet for plan gate round 6 of RWB-TE-001 or for its triage. The last RWB-TE-001 rows are 292–293, for round 5. `agent-run-log.md` line 104 records that triage as the orchestrator's (Claude Code). The orchestrator can add both rows when it logs this round. This is not a plan defect, because the plan stage does not write that file.
- **O-5 Carried.** Round-5 O-2 (`jwtDecoder` best covered by a direct call, since a mocked `JwtDecoder` replaces the bean in the slice) and round-5 O-3 (module code `P2` in tooling; fixture line counts) stand.

## 8. Document gaps

No new document gap. Round 7 rechecked the plan against the code and the Spring Boot 4.1.2 jars and found no silence or conflict in the document set. PG-01..PG-04 (all Blocker = No) stand as recorded. PG-04 is carried to the document owners by OPEN-050.

| ID | Document (name, version, section) | Gap or conflict | Second source | Blocker |
|---|---|---|---|---|
| — | none new | — | — | No |

## 9. Result

```text
PREVIOUS_FINDINGS: PLAN-023 RESOLVED, PLAN-024 RESOLVED (2/2); PLAN-001..022 held (22/22)
ONE_MODULE_SETTLEMENT: CONFIRMED (PA-12 cites D-RUN-21; SU-P05 applied; SU-P06 applied as OPEN-050, tech lead, pending ratification; PG-04/GC-1 Blocker = No; no human approval recorded)
KEY_LISTING_METHOD: CONFIRMED (finds rwb.security.* through @EnableConfigurationProperties -> RecoverySecurityProperties; TASK-18 (7) tickable from evidence)
PLAN_GATE_FINDINGS: none
PLAN_REQUIREMENT_COVERAGE_RESULT (reviewer check): CONFIRMED [TOTAL_RULES: 13] [TASK_COVERED_RULES: 13] [MISSING_TASK_RULES: 0] [CONTRADICTIONS: 0]
D_RUN_18_19_COMPATIBILITY: CONFIRMED (T-TE001-14 and SU-P02 tell RWB-E1-042 and RWB-E1-043 to extend the exact access.api list in their own merge request)
```

Overall status: **PASS**. Counts: Critical 0, High 0, Medium 0, Low 0.

This is the automated plan gate result only. It is not the AGENTS.md §9 "Plan approved" sign-off, which stays with its owner (the tech lead). OPEN-050 stays open for ratification of D-RUN-18 to D-RUN-21.

PLAN_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
