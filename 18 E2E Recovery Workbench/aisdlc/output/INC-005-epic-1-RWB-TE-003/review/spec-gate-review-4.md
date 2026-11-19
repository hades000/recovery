# Spec gate review 4: RWB-TE-003, types and contract tests from the API specification

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-003-SG5` (spec gate round 4; follows `REVIEW-RWB-TE-003-SG2` in `spec-gate-review.md`, `-SG3` in `spec-gate-review-2.md` and `-SG4` in `spec-gate-review-3.md`) |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Artifact | `aisdlc/output/INC-005-epic-1-RWB-TE-003/specify/` (remediation 3): `spec.md`, `gate-response.md` ("Round 3 remediation"), `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`. Remediation-2 text compared through `*.run3.md` / `backend-apis.run3.json`. |
| Reviewer | Compliance Reviewer (spec gate), agent run |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 0 Medium, 2 Low (2 in all) |
| Handoff | Not blocked by severity (Low only, `aisdlc/.github/rules/pdlc.md`). The status stays FAIL. Under D-RUN-09 (`AI-SDLC-BUILD-LOG.md` §1) the orchestrator fixes Low findings rather than accepting them, so a specifier re-run and a round-5 gate are expected. Both fixes are text changes in `specify/`. |

## 1. What was checked

- **Instructions.** `.claude/agents/compliance-reviewer.md`, adapted by `aisdlc/RUN-BRIEF.md`; `specification-execution-gates.md`, `pdlc.md`; the SG4 required fixes in `review/spec-gate-review-3.md`.
- **Diff.** `spec.md` against `spec.run3.md`; `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `gate-response.md`, `compliance-validation.md`, `agent-run-log.md` against their `*.run3.md`; `contracts/backend-apis.json` against `backend-apis.run3.json` (changes: round label, `handler_mapping_test`, `generated_model_test`, `headers.trace`, `coverage.spike_record`; all consistent with the spec). `contracts/frontend-integrations.json` unchanged and still correct.
- **Sources.** Story files v7, RWB-TE-003 v1 (§15 "No screen in this story", §16, §17, §19); Audit and Logging Design v2 (`05-technical-architecture/recovery-workbench-audit-and-logging-design-v2-docx.md`) §3 first bullet and §6 second bullet: the quotes in SPEC-013, TE003-SP2-DG-04, TE003-SG4-DG-01 and NEW-TE003-G match the text. API Specification v4 (`api/recovery-api-v4.yaml`): no trace request header. `frontend/src`: no `traceparent` or other trace header sent (only `traceId` read from Problem bodies). `backend/src/main/resources/application.yaml`: tracing sampling 1.0, OTLP endpoint, no propagation override (so the Spring Boot default W3C propagation that ASM-TE003-18 assumes applies); `application-local.yaml`: export off. `build.gradle.kts` line 40 `spring-boot-starter-opentelemetry`. `ApiExceptionHandler.java` lines 35 and 52 and `TemporalAdminController.java` lines 43, 44, 65, 89 unchanged since round 3. No `RouterFunction`, `HandlerMapping` or Spring Data REST in `backend/src/main` or `build.gradle.kts` (so SPEC-001 (c) "empty today" holds).
- **Dependency spec and decisions.** RWB-TE-001 v4 `spec.md` not changed since round 3 (file time 00:33, before review-3); D-RUN-15 (2026-11-18T00:39) read again: unchanged and applied correctly; D-RUN-16, D-RUN-17 do not affect this spec. `open-items.md` still ends at OPEN-042, so OPEN-043..049 are free.

## 2. Orchestrator triage for this round

Stated as orchestrator triage (Claude Code, an AI agent). No human acceptance of any finding is recorded here or in the artifact.

| Triage point | Verdict | Evidence |
|---|---|---|
| Coverage outside `check` by precedence (D-RCV-28 (3), D-RCV-40); generated code measured, no exclusion | **Still coherent** after the round-3 edits | SPEC-017 (a)-(f), §14, T-TE003-30, -36, ASM-TE003-16, `backend-apis.json` `coverage` (exclusions "none", `in_check` false), CLAR-014. The stop-and-report on a shortfall is kept. |
| A-07 owned by this story (D-RUN-15); no `X-Correlation-Id` | **Still coherent**; source and trace origin now stated | SPEC-013, SPEC-022, §3.1 A-07 rows, §16, TE003-SP2-DG-04, `backend-apis.json` `headers`. |
| D-RUN-09: any finding, Low included, means another fix round | Applied | §8 below. |

## 3. SG4 findings: resolution check

| SG4 | Severity | Resolved? | Verification |
|---|---|---|---|
| 01 | Low | **Yes** | SPEC-017 (c) now covers each property changed in turn and set to `null` in turn in both directions, `null` / other type / self, a default (all-null) instance for `equals`, `hashCode` and `toString`, enum `fromValue` for every value and an unknown value, `add…Item` / `put…Item` on null and non-null collections, models found by reflection. That covers the `&&` chain of the generated `equals`, the null branch of the `toString` helper, the enum loop and the collection-creation branches. T-TE003-36 matches. ASM-TE003-16 restated against that test. SPEC-017 (f), §9 S-1 and `backend-apis.json` `spike_record` record the four metrics for the bundle and for `integration/generated/model`. "No exclusion, no lower limit" and the stop-and-report are unchanged. |
| 02 | Low | **Partly** | The second option was taken: SPEC-001 (c) adds a static check, §7.4 says the context is a slice, (b) writes the beans it found to the report. Reason for the choice (a full context needs a database `test` does not have; OPEN-007, D-RCV-44) is sound. Two problems remain: the escape list does not check what the spec and `gate-response.md` say it checks, and only one of the three conditions has a failing fixture (SG5-01). The new failure path is missing from §11, §12 and §14 (SG5-02 (a)). |
| 03 | Low | **Yes** | Audit and Logging Design v2 §3 and §6 cited in SPEC-013, SPEC-022, §3.1 (A-07 rows), CLAR-015 and TE003-SP2-DG-04. §2 "Inherited Existing Behavior" and SPEC-013 state that the trace starts at the service or continues an incoming W3C trace context through the existing OpenTelemetry starter, no new header, no API change (ASM-TE003-18; S-4 tests both cases; fallback F-4). §16 puts front-end propagation out of scope with owner (first Epic 1 screen story or AISDLC-HARDENING), open item NEW-TE003-G (proposed OPEN-049) and gap TE003-SG4-DG-01 (Blocker = No), recorded in `specify/document-gaps.md` under the reviewer's ID with the reason. |
| 04 | Low | **Yes, with one residue** | (a) `FIXTURE_ONLY` defined once in SPEC-012, SPEC-020, §7.7 and ASM-TE003-04; but §10 still says "synthetic `FIXTURE_ONLY` rows" (SG5-02 (c)). (b) T-TE003-35 is in the SPEC-013 Tests cell and its `shared-updates.md` §3.2 row. (c) `access.internal.ApiExceptionHandlerLoggingTest` is in §2 "New Nodes Required". (d) Round-1 rows SG2-06 and SG2-07 in `gate-response.md` and the round-1 sections and counts in `agent-run-log.md` are marked superseded and kept. |

## 4. Findings

### REVIEW-RWB-TE-003-SG5-01: Low. The SPEC-001 (c) escape list does not check that a listed source is loaded, and only one of the three conditions is tested

**Affects:** SPEC-RWB-TE-003-001 (b), (c); T-TE003-34; §7.5 (`handlerMappingSources`); `gate-response.md` "Round 3 remediation" row SG4-02.

**Evidence**
- `spec.md` §6 SPEC-001 (c): "The story that adds such a source makes the contract context load it, so (b) checks it, and adds the source to the list `handlerMappingSources` … a listed source passes (c)." Nothing in (b) or (c) verifies that a listed source is loaded by the contract context. A later story that lists its `RouterFunction` configuration or adds Spring Data REST, but does not load it into the slice, passes (c), and (b) never sees those mappings. That is the blind spot SG4-02 described, moved to the next story. The failure text "is not loaded by the contract context" names a condition the check never tests.
- `gate-response.md` "Round 3 remediation", row SG4-02, describes the check as failing "unless the source is in `handlerMappingSources` (empty today) and loaded by the contract context". The spec does not say that. A planner reading the gate response would expect a check the spec does not define.
- (c) has three conditions: a recovery `@Bean` returning `RouterFunction` or a `HandlerMapping`; a recovery class implementing `HandlerMapping`, `RouterFunction` or `HandlerFunction`; Spring Data REST web on the classpath. T-TE003-34 (c) has a failing fixture only for "a `@Bean RouterFunction` method". The other two conditions are tested only negatively (the live run passes with an empty list). The Spring Data REST condition uses a fixed class name, so a fixture cannot make it fail unless that class name is a parameter, as the root package already is.

**Required fix**
1. In SPEC-001 (c), make a listed source pass only when the contract context loads it: for example, each `handlerMappingSources` entry names the bean (or the `HandlerMapping` bean it creates), and the test fails `handler mapping source {source} is listed but not loaded by the contract context` when (b) did not find that bean. Then make the `gate-response.md` SG4-02 row match the spec wording.
2. Extend T-TE003-34 (c) with one failing fixture per condition: a `@Bean` method returning a `HandlerMapping`; a fixture class implementing `RouterFunction` (or `HandlerFunction` or `HandlerMapping`); and the classpath condition run with a fixture class name passed as a parameter (the live run keeps `org.springframework.data.rest.webmvc.RepositoryRestHandlerMapping`). Add a case for item 1: a listed source whose bean the fixture context does not hold fails.

### REVIEW-RWB-TE-003-SG5-02: Low. Five inconsistencies introduced or left by the round-3 edits

**Affects:** SPEC-RWB-TE-003-001 (c), -015, -019; §10; §11; §12; §14 backend row; T-TE003-28; `shared-updates.md` §4; `agent-run-log.md` title.

**Evidence**
- (a) SPEC-001 (c) adds the failure text `handler mapping source {source} is not loaded by the contract context`, but §12 has no exception row for it (X-S10 covers (b) only), the §11 row "Handler-mapping check" cites "Text per SPEC-001 (b)" only, and the §14 backend Test Acceptance Criteria list "Handler mappings: URL mapping and router function … fail; primary mapping and actuator pass" with no static-check case. Every other failure text in §6 has a §12 row (X1-X8, X-S1..X-S13).
- (b) SPEC-001 (b) now writes "the list of handler-mapping beans it found (name and class) to the contract report". SPEC-015 defines the report content (operation rows, totals, input SHA-256) and does not include that list, and T-TE003-28 checks "141 + 2 rows, totals, SHA-256". SPEC-019 requires a byte-identical report, so the list's order must also be defined.
- (c) §10 row "Fixture matrix row" says "synthetic `FIXTURE_ONLY` rows for fixture controllers". SPEC-020 says `FIXTURE_ONLY` "means one thing everywhere in this spec … whether its role is synthetic or real", and §7.7 has the real role `RW-REFADM` in a `FIXTURE_ONLY` row. §10 keeps the old meaning SG4-04 (a) removed.
- (d) `shared-updates.md` §4 preamble: "Raised by = INC-005 specify remediation 1 or 2 as marked; Found = 2026-11-17, or 2026-11-18 for remediation 2 rows". The new row TE003-SG4-DG-01 is marked "remediation 3, from gate round 3", so the rule gives the orchestrator neither a Raised-by value (the gap was raised by gate round 3, `review/spec-gate-review-3.md` SG4-03) nor a Found date for it.
- (e) `agent-run-log.md` title still reads "(remediation 1 and 2)" although the file now holds the round-3 section and the header field marks 18 assumptions "after round 3".

**Required fix**
- (a) Add an X-S row to §12 for the SPEC-001 (c) text (and the SG5-01 "listed but not loaded" text), cite SPEC-001 (b), (c) in the §11 row, and add the static-check cases to the §14 backend Test Acceptance Criteria.
- (b) Add the handler-mapping list (name, class, sorted by bean name) to the SPEC-015 report content and to T-TE003-28.
- (c) Reword the §10 row to "cited source for `PRODUCTION` rows; `FIXTURE_ONLY` rows (synthetic or real role) for fixture controllers only".
- (d) Extend the §4 preamble: remediation 3 rows are raised by "INC-005 spec gate round 3" (as marked) and found 2026-11-18.
- (e) Correct the `agent-run-log.md` title to cover remediations 1 to 3.

## 5. Phase-0 audit items owned by this story

| Item | Disposition in the spec | Verdict |
|---|---|---|
| A-03 | In: all-handler method-check test (SPEC-005); other handler mappings (SPEC-001 (b), (c)). Out: capability naming and role literals to RWB-E1-022 / RWB-E1-037 (OPEN-040 amendment) | Accepted (reach of (c): SG5-01) |
| A-04 | Extend `api:generate`; no duplicate (SPEC-006, -007) | Accepted |
| A-07 | In: safe exception logging (SPEC-022, T-TE003-35); `traceId` on the Problem and the log event (SPEC-013), sources Audit and Logging Design v2 §3 and §6; trace starts at the service (ASM-TE003-18). Out: front-end propagation (NEW-TE003-G, TE003-SG4-DG-01). Not built: `X-Correlation-Id` (TE003-SP2-DG-04; D-RUN-15) | Accepted |
| A-08 | In: `messageCode` and `traceId` asserted, `traceId` on 500. Out: 500 message ID (NEW-TE003-B), 400/422 mapping (NEW-TE003-C), `{action}` per language (RWB-E1-022) | Accepted |
| A-09 | In: contract job via `test` and `check` (SPEC-016); coverage on TE-003 code by the existing task, outside `check`, no exclusion (SPEC-017). Out: CI coverage job (NEW-TE003-F), PDPA lint (TE-011), Playwright/axe (TE-010), dependency scan and ZAP (NEW-TE003-D) | Accepted |
| A-11 | In: generated `Problem` (SPEC-007). Excepted: `PlatformInfo` / `TemporalHealth` (README decision 6, NEW-TE003-A). Out: ESLint fixture test to TE-001 | Accepted |
| A-15 | Out: first screen story or hardening (NEW-TE003-E) | Accepted |

## 6. Required checks (reviewer instructions)

| Check | Result |
|---|---|
| Authentication and authorization | PASS with SG5-01 (Low). Method-security presence on every handler; access suite per enforced operation with cited roles; `FIXTURE_ONLY` refused for production controllers; area `None` tested as 401; live TC-TE-003-09 kept `BLOCKED` (OPEN-040). |
| Customer and account data protection | PASS. Synthetic fixtures, JWT subjects and log sentinel; report holds operation names only; exception text never logged (SPEC-022; Audit and Logging Design v2 §6). |
| Audit logging | N/A for a sensitive financial action. Application-log content covered by SPEC-022. |
| KYC, AML, suitability, consent, approval | N/A for a build-tooling story. |
| Frontend integration versioning and error contract | PASS. One type set; `NO_API_CHANGE`; Problem completeness asserted; `traceId` on every Problem; no new header. |
| Secrets and environment configuration | PASS. Test JWTs from `spring-security-test`; no secret in fixtures; `rwb.p3.temporal=true` in the contract context only. |
| Test coverage and evidence (planning) | PASS. Both surfaces REQUIRED; backend four metrics at 80% by the existing task, outside `check`, no exclusion; model test now designed to reach the generated branches; model and bundle metrics recorded separately at S-1. |

## 7. Internal consistency (checked)

- SPEC-RWB-TE-003-001..022 each defined once in §6 (22); §3 has 36 rows, 0 BLOCKED; §18 status lines match (36 / 36).
- Test IDs T-TE003-10..36 all defined in §15 and each referenced by a SPEC; T-TE003-35 now on SPEC-013 and SPEC-022 in §6 and in `shared-updates.md` §3.2; TC-TE-003-01..09 match story v7 §16. Exception: SG5-02 (b) (T-TE003-28 scope).
- Fallbacks named anywhere (F-1a, F-1b, F-1d, F-2, F-3, F-4, the ASM-TE003-09 fallback) all exist in §9 or §7.5.
- Assumptions ASM-TE003-01..18 (18) match the run log's round-3 count and the header of `assumptions.md`; ASM-TE003-18 is cited by §2, SPEC-013, §9 S-4 and `backend-apis.json`.
- Open items NEW-TE003-A..G map one to one to proposed OPEN-043..049; `shared-updates.md` §1 says "NEW-TE003-A..G"; `assumptions.md` footer says the same.
- Gap IDs: TE003-SG-DG-01..08, TE003-SG3-DG-01..03 and TE003-SG4-DG-01 (reviewer IDs; the last recorded by the specifier because `review/document-gaps-3.md` was never written, with that reason stated); TE003-SP-DG-01..06 and TE003-SP2-DG-01, -03, -04 are the specifier's own (SP2-DG-02 withdrawn with a reason). The same IDs appear in spec, `document-gaps.md`, `shared-updates.md` §4 and `gate-response.md`. **No gap is marked Blocker = Yes**, and none needs to be.
- CLAR-001..016 (16) all RESOLVED; CLAR-015 updated for the trace origin.
- Report counts: 1 PASSED + 72 PENDING (E1) + 68 PENDING (E2-E6) = 141, plus 2 `OUTSIDE_SPECIFICATION`, unchanged.
- `shared-updates.md` §3.1 status text is correct for a FAIL (apply §3.1 only, with this gate's result).

## 8. Gate result

```text
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
SG4 RESOLUTION: 3 of 4 resolved (SG4-01, -03, -04; SG4-04 (a) has a residue in §10, SG5-02 (c)); SG4-02 partly resolved (SG5-01).
ORCHESTRATOR TRIAGE: coverage precedence and A-07 scope (D-RUN-15) still implemented coherently.
DOCUMENT_GAPS: 0 new candidates (no review/document-gaps-4.md); 0 blockers.
NEXT_STEP: Under D-RUN-09 the orchestrator re-runs the Technical Specifier to fix SG5-01 and SG5-02 (text only), then this gate runs again as review/spec-gate-review-5.md. Do not start the Implementation Planner before that. PRE-1 (RWB-TE-001 merged) still applies after a PASS.
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
```
