# Spec gate review 3: RWB-TE-003, types and contract tests from the API specification

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-003-SG4` (spec gate round 3; follows `REVIEW-RWB-TE-003-SG2` in `spec-gate-review.md` and `REVIEW-RWB-TE-003-SG3` in `spec-gate-review-2.md`) |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Artifact | `aisdlc/output/INC-005-epic-1-RWB-TE-003/specify/` (remediation 2): `spec.md`, `gate-response.md` ("Round 2 remediation"), `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`. Round-1 text compared through `*.run2.md` / `backend-apis.run2.json`. |
| Reviewer | Compliance Reviewer (spec gate), agent run |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 0 Medium, 4 Low (4 in all) |
| Handoff | Not blocked by severity (Low only, `aisdlc/.github/rules/pdlc.md`). The status stays FAIL. Under D-RUN-09 (`AI-SDLC-BUILD-LOG.md` §1) the orchestrator fixes Low findings rather than accepting them, so a re-run of the specifier and a round-4 gate are expected. All four fixes are text changes in `specify/`. |

## 1. What was checked

- **Instructions.** `.claude/agents/compliance-reviewer.md`, adapted by `aisdlc/RUN-BRIEF.md`; `pdlc.md`, `specification-execution-gates.md`, `implementation-execution-gates.md` (IEG), `traceability-standards.md`; contexts `backend-standards.md` (BS-1.1, -1.5, -3.3, -4.6, -7.2), `backend-context.md` §7, `testing-standards.md`.
- **Earlier rounds.** `review/spec-gate-review.md` (SG2-01..12), `review/spec-gate-review-2.md` (SG3-01..06), `review/document-gaps.md`, `review/document-gaps-2.md`. Resolved SG2 findings were not reopened; none is broken by the new text.
- **Dependency spec.** RWB-TE-001 v4 (`INC-002-epic-1-RWB-TE-001/specify/spec.md`, `shared-updates.md`). Verified against the TE-003 text: Field-level matrix (P2 `integration`, published `[api, flags.api]`, later entry `integration` `generated.web`, `generated.model` for RWB-TE-003); SPEC-004 (d) (`propagate = false`) and (g); SPEC-011 (fixture root outside `th.co.scb.ace.demo`); SPEC-020 (a) four limits, (b) tooling class directory, (d) outside `check`, (e) Builder runs `./gradlew test recoveryCoverageVerification`; Backend Unit Test Applicability "No main class is excluded"; SPEC-022 (b) paths unchanged, (d) dependencies `casewf.rules` → `integration.flags.api` and `casewf.admin` → `access.api`, no other; Relocation table (every path in the TE-003 "Baseline paths" rule matches, including `TemporalProperties` public in `casewf.workflow.internal` and `TemporalAdminController` package-private in `casewf.admin`); SPEC-023 property split; SPEC-024; SU-08, SU-09, SU-10.
- **Decisions.** `INC-001-decisions.md` D-RCV-05, -06, -28 (3) ("JaCoCo checks run in recovery-only tasks outside `check`"), -37, -40, -43; `decision-register.md` L-RCV-11, L-RCV-14; `AI-SDLC-BUILD-LOG.md` §1 D-RUN-09..15 (D-RUN-15 at 2026-11-18T00:39 verified word for word against the spec's use of it).
- **Audit.** `aisdlc/evidence/phase0-standards-audit.md` A-03, A-04, A-07, A-08, A-09, A-11, A-15. RWB-TE-011 spec "Scope decisions" A-07 (a)/(b) out of scope: verified.
- **Story sources (read only, document set v14).** Story file v7 RWB-TE-003 v1; RWB-E1-071 v1 (§1, §4 step 9, §5 X6, §10 Authority "Platform administration, U", §12 request body, 409 MSG-GEN-004, right U, §16 TC-E1-071-08); Audit and Logging Design v2 (`05-technical-architecture/recovery-workbench-audit-and-logging-design-v2-docx.md`) §3 and §6.
- **API Specification v4.** `api/recovery-api-v4.yaml`, SHA-256 `535cb465…b891` re-computed: matches. Parsed: 141 operations (E1 73, E2 38, E3 8, E4 10, E5 8, E6 4), 172 component schemas, `area: None` on `getFeatureFlags` and `getMeSession` only. `postAdminWorkflowsSmoke` (line 3107): P3, Platform administration C, E1, description names RW-PLATADM, 202 inline schema `workflowId`, `workflowType`, plus 401, 403, 404, 503. `Problem` (line 8980) has `traceId` (string) and no `required` list. "X-Correlation-Id": 0 occurrences in API v4 and in the converted document set (1,257 files); "correlat": 0 occurrences in the document set.
- **Repository code.** `ApiExceptionHandler.java` (line 35 `log.warn(..., ex.getCause())`, line 52 `log.error(..., ex)`: quoted correctly in SPEC-022), `ProblemFactory.java` (private `traceId()` from Micrometer `Tracer`), `TemporalAdminController.java` (class mapping line 43, condition line 44, smoke lines 89-108, comment "right C" line 91, health `@GetMapping("/temporal/health")` line 65), `backend/build.gradle.kts` (`recoveryClasses`, `recoveryCoverageReport`, `recoveryCoverageVerification` LINE and BRANCH only today; `test` finalised by the report only; `spring-boot-starter-opentelemetry` line 40), `application.yaml` (ECS console format, sampling 1.0), `application-local.yaml` (plain console, export off), `.gitlab-ci.yml` (`backend-unit` line 15 `test recoveryCoverageReport`; `frontend-check` `npm run check`), `README.md` lines 86-87 (coverage note), `frontend/src` (no trace header is sent by the front end).
- **Not re-checked.** The OpenAPI Generator `spring` options page could not be fetched in this run (tool limit). The option names and the `requestMappingMode` default were verified by round 2 (`spec-gate-review-2.md` §1, SG3-03); the spec now makes the plan pin the generator version and re-check every option (OPEN-039 amendment), which is the right control.

## 2. Orchestrator triage for this round

Stated as orchestrator triage (Claude Code, an AI agent). No human acceptance of any finding is recorded here or in the artifact.

| Triage point | Verdict | Evidence |
|---|---|---|
| SG3-01 settled by precedence: coverage verification outside `check` (D-RCV-28 (3), D-RCV-40); metrics of TE-001 v4 SPEC-020; `generated/**` exclusion only with a cited source, else measured with a gap; a CI job is a pipeline change and goes to an open item | **Implemented coherently** (test design for the measured models is Low SG4-01) | SPEC-017 (a)-(f), §3.1 A-09 rows, §11, §14 backend row, §16, T-TE003-30, -36, CLAR-014, ASM-TE003-16, TE003-SG3-DG-03, TE003-SP2-DG-01, OPEN-048 (NEW-TE003-F), `contracts/backend-apis.json` `coverage` all say the same thing: four limits at 0.80, no exclusion, tooling added to the existing task, separate task withdrawn, task neither dependency nor finalizer of `test` or `check`, Builder-run, CI unchanged. No residual "finalizer", "LINE, BRANCH 80%" or `generated/**` exclusion in the remediation-2 spec. |
| A-07 owned by this story: safe exception logging (no raw exception text), `traceId` per API v4 Problem, no `X-Correlation-Id` (gap, Blocker = No) | **In scope and specified** (a source and a scope statement are missing: Low SG4-03) | SPEC-022 removes both raw-text log calls and forbids passing the `Throwable` (correct: SLF4J prints the message of the throwable and of every cause); SPEC-013 ties the 500 body's `traceId` to the log event; T-TE003-35 uses a synthetic sentinel on the `problem` and `unexpected` paths and checks message, arguments, key-values, MDC and throwable. `X-Correlation-Id` not built; TE003-SP2-DG-04 Blocker = No with D-RUN-15. |

## 3. SG3 findings: resolution check

| SG3 | Severity | Resolved? | Verification |
|---|---|---|---|
| 01 | Medium | **Yes** | Item 1 replaced by precedence (orchestrator triage); conflict recorded as TE003-SG3-DG-03 (Blocker = No) and CI wiring sent to OPEN-048. Item 2: four metrics in SPEC-017 (a) and §14. Item 3: no exclusion, protective reading, TE003-SP2-DG-01; IEG "exclusions and rationale" honoured by SPEC-017 (e) ("states 'no exclusion'"). Item 4: tooling directories added to the existing task, as TE-001 v4 SPEC-020 (b) does; `recoveryContractCoverageVerification` withdrawn. The stop-and-report in SPEC-017 (f) and S-1 is the right safety net. |
| 02 | Low | **Yes** | TE-001 v4 cited in the header, PRE-1..PRE-3, CLAR-003; "Baseline paths" rule; every path checked against the TE-001 v4 Relocation table. "Does not exist" corrected in the run log; `compliance-validation.md` §4 now names TE-001 v4. The P3 → P2 edge added by SPEC-014 matches TE-001 v4 SPEC-022 (d) (no cycle). |
| 03 | Low | **Yes** | `useSpringBoot4`, `useJackson3` primary, Boot 3 as F-1a; options and normalizer cited by page and read date, version pinned at plan; Spring Framework 7.0.10 reference cited with ASM-TE003-11 kept and fallback F-1d; base path: class mapping `/api/recovery/v1`, health method `/admin/temporal/health`, both full paths unchanged and asserted in T-TE003-27; SPEC-004 limited to `*Api` interfaces with no class-level mapping, and an unsuppressible supporting class stops the plan. |
| 04 | Low | **Yes** | §7.7 adds cited `holds` and `lacks` rows and a `use` column; SPEC-011 takes the positive role from a `holds` row; the right is always read from API v4. Gaps TE003-SG3-DG-01, -02 recorded, plus TE003-SP2-DG-03 (E1-071 §12 request body, 409, right U; verified at lines 198-202). One wording conflict is left: Low SG4-04 (a). |
| 05 | Low | **Yes in design** | SPEC-001 (b), X-S10, T-TE003-34. The live check's reach depends on the contract context, which is not defined: Low SG4-02. |
| 06 | Low | **Yes** | `apiTooling` listed for plan-gate approval in the OPEN-039 amendment with a reason (lint before generation; TE-001 module-map rule; TE-001 v4 SPEC-011 precedent, verified); fallback kept in ASM-TE003-09 and §7.5. |

## 4. Findings

### REVIEW-RWB-TE-003-SG4-01: Low. The generated-model test does not reach the branches the measured models carry, so the coverage stop in SPEC-017 (f) is predictable

**Affects:** SPEC-RWB-TE-003-017 (c), (f); T-TE003-36; ASM-TE003-16; §14 backend row; §9 S-1; A-09 (coverage part).

**Evidence**
- SPEC-017 (b) measures every class in `integration.generated.model` (correct under the protective reading). API v4 has 172 component schemas plus inline schemas such as the `postAdminWorkflowsSmoke` 202 body, so the generated models are most of the recovery bundle that `recoveryCoverageVerification` measures (today the whole recovery main code is 415 lines, TE-001 v4 Unit Test Applicability baseline).
- SPEC-017 (c) asserts "the not-equal cases (`null`, another type, one changed property)" and sets "each property to a synthetic value". For a model with N properties, the generated `equals` is a chain of N `Objects.equals(...) &&` tests, so JaCoCo counts 2N branches there; an all-equal comparison plus one changed property covers about N + 1 of them. A model with every property set never takes the null branch of the generated `toString` helper. Enum models (`fromValue` with an unknown value) and collection helpers that create the list or map when it is null (`add…Item`, `put…Item`) are not named.
- ASM-TE003-16 states the bundle "still reaches 80% on all four metrics because" this test exercises every model. On the test as written, BRANCH is unlikely to reach 80%, so the planner would stop at S-1 (SPEC-017 (f)) for a reason the spec can remove now. The stop itself is correct and must stay.

**Required fix**
1. Extend SPEC-017 (c) and T-TE003-36: compare against a copy with **each property changed in turn**; exercise a default (all-null) instance for `equals`, `hashCode` and `toString`; for enum models, `fromValue` with every declared value and with an unknown value (expected exception); for collection properties, the add/put helpers on a null and on a non-null collection.
2. Restate ASM-TE003-16 against that test, and have S-1 record the four metrics for `integration/generated/model` separately as well as for the bundle, so a stop can be diagnosed. Keep "no exclusion, no lower limit" and the stop-and-report unchanged.

### REVIEW-RWB-TE-003-SG4-02: Low. The live handler-mapping check is only as wide as the contract context, which the spec does not define

**Affects:** SPEC-RWB-TE-003-001 (b); SPEC-010; §7.4; ASM-TE003-10; T-TE003-34.

**Evidence**
- SPEC-001 (b) lists "every `HandlerMapping` bean" in "the same contract context". §7.4 and ASM-TE003-10 describe that context as a MockMvc context that "holds every production recovery controller, `access.internal.SecurityConfig`, method security and `access.internal.ApiExceptionHandler`", with collaborators stubbed. That reads as a curated slice.
- The guard exists for a later story that adds Spring Data REST (AGENTS §2; audit A-13) or a `RouterFunction` bean. In a slice that loads controllers but not the Spring Data REST auto-configuration or `@Configuration` classes that declare `RouterFunction` beans, those mappings never exist in the test context, and the live check passes without seeing them. T-TE003-34 uses fixture contexts that register the mappings explicitly, so it would stay green while the live check is blind.

**Required fix**
Do one of these in SPEC-001 (b) and §7.4:
- state that the live check runs in a context that loads all recovery main configuration and the auto-configured web MVC mappings present on the classpath (for example `@SpringBootTest` with MockMvc and stubbed external collaborators), and add to T-TE003-34 a live assertion that lists the handler-mapping beans found; or
- add a static check on main classes and the runtime classpath that fails when a `RouterFunction` bean is declared under `th.co.scb.ace.demo.recovery` or a Spring Data REST web dependency is present without an entry in this check, with the same failure text style.

### REVIEW-RWB-TE-003-SG4-03: Low. The A-07 dispositions omit the document-set source on trace IDs and logging, and do not say where the trace begins

**Affects:** SPEC-RWB-TE-003-013, -022; §3.1 A-07 rows; §16; TE003-SP2-DG-04; CLAR-015.

**Evidence**
- Audit and Logging Design v2 (`05-technical-architecture/recovery-workbench-audit-and-logging-design-v2-docx.md`) §3: every request "carries a trace ID from the front end through the service"; §6 lists what is never logged, including personal fields in application logs. This is the document-set source for both A-07 parts. SPEC-022 and SPEC-013 cite only BS-4.6, backend-context §7, AGENTS §4.7 and D-RUN-15, and TE003-SP2-DG-04 says the only correlation field is API v4 `Problem.traceId` without naming the design.
- The front end sends no trace header today (`frontend/src`: no `traceparent` or other trace header), and API v4 declares no request header for one. So the `traceId` that SPEC-013 and SPEC-022 carry starts at the service, not at the front end as the design says. The spec neither states this as inherited behaviour (Spring Boot OpenTelemetry starts a trace per request and continues an incoming W3C trace context if one is sent) nor names the front-end part as out of scope with an owner. The decision not to build `X-Correlation-Id` (D-RUN-15) is unaffected.

**Required fix**
1. Cite Audit and Logging Design v2 §3 and §6 in SPEC-013, SPEC-022, §3.1 (A-07 rows) and TE003-SP2-DG-04.
2. Add to §2 "Inherited Existing Behavior" (or SPEC-013) that the trace starts at the service, or continues an incoming W3C trace context, through the existing OpenTelemetry starter, with no new header and no API change.
3. List front-end trace propagation in §16 as out of scope with an owner and an open item (for example the first screen story or AISDLC-HARDENING), citing the candidate gap TE003-SG4-DG-01 in `review/document-gaps-3.md` (Blocker = No).

### REVIEW-RWB-TE-003-SG4-04: Low. Four internal inconsistencies

**Affects:** SPEC-RWB-TE-003-012, -013; §2; §7.7; `shared-updates.md` §3.2; `gate-response.md` round-1 table; `agent-run-log.md`.

**Evidence**
- (a) SPEC-012 defines a `FIXTURE_ONLY` row as "(a synthetic role)", but §7.7 and ASM-TE003-04 mark the real role `RW-REFADM` as `FIXTURE_ONLY` (used by TC-TE-003-08). The two definitions disagree on what `FIXTURE_ONLY` means.
- (b) T-TE003-35 is labelled "022, 013" and asserts the log event's `traceId` equals the body's, but the SPEC-013 "Tests" cell in §6 and the SPEC-013 row in `shared-updates.md` §3.2 list only T-TE003-26.
- (c) §2 "New Nodes Required" names the test package `recovery.contract` but not the new `ApiExceptionHandlerLoggingTest` under `recovery.access.internal` (listed in §7.5 and `contracts/backend-apis.json`).
- (d) `gate-response.md` round-1 rows SG2-06 and SG2-07 still describe designs that remediation 2 withdrew ("finalizer of `test`", "`**/generated/**` excluded", "new `recoveryContractCoverageVerification`", "`<P2>`", "TE-001's remediated spec did not yet exist"), and `agent-run-log.md` round-1 tables still say "15 assumptions" and "SPEC-RWB-TE-003-001..021", with no marker that they are superseded. A reader of the plan-input chain can take the old text as current.

**Required fix**
- (a) Define `FIXTURE_ONLY` once as "may serve only fixture controllers", whether the role is synthetic or real, and use that wording in SPEC-012, SPEC-020 and §7.7.
- (b) Add T-TE003-35 to the SPEC-013 Tests cell and to its `shared-updates.md` §3.2 row.
- (c) Add the logging test location to §2 "New Nodes Required".
- (d) Mark the round-1 rows SG2-06 and SG2-07 in `gate-response.md` and the round-1 tables in `agent-run-log.md` as "superseded by round 2 remediation", without deleting them.

## 5. Phase-0 audit items owned by this story

| Item | Disposition in the spec | Verdict |
|---|---|---|
| A-03 | In: all-handler method-check test (SPEC-005), plus other handler mappings (SPEC-001 (b)). Out: capability naming and role literals to RWB-E1-022 / RWB-E1-037 (OPEN-040 amendment) | Accepted (reach of SPEC-001 (b): SG4-02) |
| A-04 | Extend `api:generate`; no duplicate (SPEC-006, -007) | Accepted |
| A-07 | In: safe exception logging (SPEC-022, T-TE003-35); `traceId` on the Problem and the log event (SPEC-013). Not built: `X-Correlation-Id` (TE003-SP2-DG-04, Blocker = No; D-RUN-15) | Accepted (source and trace origin: SG4-03) |
| A-08 | In: `messageCode` and `traceId` asserted, `traceId` on 500. Out: 500 message ID (NEW-TE003-B), 400/422 mapping (NEW-TE003-C), `{action}` per language (RWB-E1-022) | Accepted |
| A-09 | In: contract job via `test` and `check` (SPEC-016); coverage on TE-003 code by the existing task, outside `check` (SPEC-017). Out: CI coverage job (NEW-TE003-F), PDPA lint (TE-011), Playwright/axe (TE-010), dependency scan and ZAP (NEW-TE003-D) | Accepted (model test design: SG4-01) |
| A-11 | In: generated `Problem` (SPEC-007). Excepted: `PlatformInfo` / `TemporalHealth` (README decision 6, NEW-TE003-A). Out: ESLint fixture test to TE-001 | Accepted |
| A-15 | Out: first screen story or hardening (NEW-TE003-E) | Accepted |

## 6. Required checks (reviewer instructions)

| Check | Result |
|---|---|
| Authentication and authorization | PASS with SG4-02 (Low). Method-security presence on every annotated handler; access suite per enforced operation with cited roles; area `None` tested as 401; live TC-TE-003-09 kept `BLOCKED` (OPEN-040). |
| Customer and account data protection | PASS. Synthetic fixtures, JWT subjects and log sentinel; report holds operation names only; exception text never logged (SPEC-022). |
| Audit logging | N/A for a sensitive financial action. Application-log content is covered by SPEC-022 (source: SG4-03). |
| KYC, AML, suitability, consent, approval | N/A for a build-tooling story. |
| Frontend integration versioning and error contract | PASS. One type set; `NO_API_CHANGE`; Problem completeness asserted; `traceId` on every Problem. |
| Secrets and environment configuration | PASS. Test JWTs from `spring-security-test`; no secret in fixtures; `rwb.p3.temporal=true` in the contract context only. |
| Test coverage and evidence (planning) | PASS with SG4-01 (Low). Both surfaces REQUIRED; backend four metrics at 80% through the existing task, outside `check`, no exclusion, native report and "no exclusion" statement required in `report.md`; frontend thresholds inherited. |

## 7. Internal consistency (checked)

- SPEC-RWB-TE-003-001..022 each defined once in §6 (22); §3 has 36 rows (5 BR, 8 AC, 8 flow, 8 X, §12, §13 step 2, 4 guardrails, §19), 0 BLOCKED; status lines match.
- Test IDs T-TE003-10..36 all defined in §15 and all referenced by a SPEC; TC-TE-003-01..09 match story v7 §16. Exception: SG4-04 (b).
- Fallbacks named anywhere (F-1a, F-1b, F-1d, F-2, F-3, F-4, the ASM-TE003-09 fallback) all exist in §9 or §7.5.
- Assumptions ASM-TE003-01..17 (17) match the run log's round-2 count; CLAR-001..016 (16) all RESOLVED.
- Open items NEW-TE003-A..F map one to one to proposed OPEN-043..048 (`open-items.md` ends at OPEN-042 today).
- Gap IDs: TE003-SG-DG-01..08, TE003-SG3-DG-01..03 match the review files; TE003-SP-DG-01..06 and TE003-SP2-DG-01, -03, -04 are the specifier's own (SP2-DG-02 withdrawn with a reason). **No gap is marked Blocker = Yes**, and none needs to be: each is settled by BR1, a local decision, D-RUN-15 or the protective reading.
- Traceability: `shared-updates.md` §3.2 has 22 SPEC rows with requirement source, story ref and tests (one omission: SG4-04 (b)); §3.1 row-005 status text is correct for a FAIL (apply §3.1 only, with this gate's result).
- Report counts: 1 PASSED + 72 PENDING (E1) + 68 PENDING (E2-E6) = 141, plus 2 `OUTSIDE_SPECIFICATION`, matching T-TE003-28 and the API v4 parse.

## 8. Gate result

```text
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
SG3 RESOLUTION: 6 of 6 resolved (SG3-05 resolved in design; its reach is SG4-02).
ORCHESTRATOR TRIAGE: SG3-01 precedence implemented coherently; A-07 in scope as directed (D-RUN-15).
DOCUMENT_GAPS: 1 new candidate in review/document-gaps-3.md (TE003-SG4-DG-01), 0 blockers.
NEXT_STEP: Under D-RUN-09 the orchestrator re-runs the Technical Specifier to fix SG4-01..04 (text only), then this gate runs again as review/spec-gate-review-4.md. Do not start the Implementation Planner before that. PRE-1 (RWB-TE-001 merged) still applies after a PASS.
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
```
