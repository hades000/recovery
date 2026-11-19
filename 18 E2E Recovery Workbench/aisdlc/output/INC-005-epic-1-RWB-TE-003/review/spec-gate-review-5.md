# Spec gate review 5: RWB-TE-003, types and contract tests from the API specification

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-003-SG6` (spec gate round 5; follows `-SG2` in `spec-gate-review.md`, `-SG3` in `spec-gate-review-2.md`, `-SG4` in `spec-gate-review-3.md` and `-SG5` in `spec-gate-review-4.md`) |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Artifact | `aisdlc/output/INC-005-epic-1-RWB-TE-003/specify/` (remediation 4): `spec.md`, `gate-response.md` ("Round 4 remediation"), `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`. Remediation-3 text compared through `*.run4.md` / `backend-apis.run4.json`. |
| Reviewer | Compliance Reviewer (spec gate), agent run |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 0 Medium, 1 Low (1 in all) |
| Handoff | Not blocked by severity (Low only, `aisdlc/.github/rules/pdlc.md`). The status stays FAIL. Under D-RUN-09 (`AI-SDLC-BUILD-LOG.md` §1) the orchestrator fixes Low findings rather than accepting them, so a specifier re-run and a round-6 gate are expected. The fix is a text change in `specify/`. |

## 1. What was checked

- **Instructions.** `.claude/agents/compliance-reviewer.md` (spec gate), adapted by `aisdlc/RUN-BRIEF.md`; `specification-execution-gates.md`; `pdlc.md`; the SG5 required fixes in `review/spec-gate-review-4.md`.
- **Diff.** `spec.md` against `spec.run4.md` (changes: header and status, SPEC-001 (c), SPEC-015, §7.5 row, §10 fixture-matrix row, §11 handler-mapping row, §12 X-S14 and X-S15, §14 backend criteria, T-TE003-28, T-TE003-34, §18 NEXT_STEP). `shared-updates.md`, `gate-response.md`, `compliance-validation.md`, `agent-run-log.md` against their `*.run4.md`; `contracts/backend-apis.json` against `backend-apis.run4.json` (round label, `handler_mapping_test`, new `report_handler_mappings`; both files parse as JSON). `assumptions.md` and `document-gaps.md` were not changed this round (no `*.run4.md`, as the run log's backup list says); `contracts/frontend-integrations.json` unchanged and still correct.
- **Sources.** Story files v7, RWB-TE-003 v1 (§17: the report "holds operation names only", read as the no-personal-data guardrail; the bean-name list in the report keeps to it). API Specification v4 (`api/recovery-api-v4.yaml`) unchanged. `backend/src/main` and `backend/build.gradle.kts`: still no `RouterFunction`, `HandlerMapping`, `HandlerFunction` or Spring Data REST, so "today no source is detected, the list is empty" holds. No file under `backend/src` or `frontend/src` changed since review 4.
- **Dependency spec and decisions.** RWB-TE-001 v4 `spec.md` unchanged (file time 00:33); `INC-001-decisions.md` unchanged; build log D-RUN-09..17, no new D-RUN entry. `open-items.md` still ends at OPEN-042, so OPEN-043..049 are free.

## 2. Orchestrator triage for this round

Stated as orchestrator triage (Claude Code, an AI agent). No human acceptance of any finding is recorded here or in the artifact.

| Triage point | Verdict | Evidence |
|---|---|---|
| Coverage outside `check` by precedence (D-RCV-28 (3), D-RCV-40); generated code measured, no exclusion | **Still coherent**; round-4 edits did not touch it | SPEC-017, §14 backend row (scope and "outside `check`" text unchanged), `backend-apis.json` `coverage`, TE003-SG3-DG-03, TE003-SP2-DG-01. |
| A-07 owned by this story (D-RUN-15); no `X-Correlation-Id` | **Still coherent**; unchanged | SPEC-013, SPEC-022, §3.1, `backend-apis.json` `headers`, TE003-SP2-DG-04, `shared-updates.md` §5 and §6. |
| D-RUN-09: any finding, Low included, means another fix round | Applied | §5 below. |

## 3. SG5 findings: resolution check

| SG5 | Severity | Resolved? | Verification |
|---|---|---|---|
| 01 | Low | **Partly** | Item 1 met: each `handlerMappingSources` entry holds `source`, `story`, `mappingBean`; a listed source passes only when (b) found a `HandlerMapping` bean of that name, else `... is listed but not loaded by the contract context` (SPEC-001 (c), §7.5, X-S15, `backend-apis.json`); the `gate-response.md` round-3 SG4-02 row now carries a round-4 correction note. Item 2 mostly met: classpath marker is a parameter; (c1) `@Bean` returning `HandlerMapping`, (c2) class implementing `RouterFunction`, (c3) fixture marker, (c4) listed-not-loaded, (c5) listed-and-loaded, live pass. Two residues: the round-3 failing fixture for a `@Bean` returning `RouterFunction` was replaced, not kept, and the not-listed text still names "not loaded" (SG6-01). |
| 02 | Low | **Yes** | (a) §11 row cites SPEC-001 (b), (c); §12 X-S14 and X-S15 added; §14 backend criteria list the static-check cases. (b) SPEC-015 report content and T-TE003-28 include the handler-mapping list, bean name and class, sorted by bean name (SPEC-019 byte identity kept); `backend-apis.json` `report_handler_mappings` matches. (c) §10 row reads "`FIXTURE_ONLY` rows (synthetic or real role) for fixture controllers only". (d) `shared-updates.md` §4 preamble gives Raised by "INC-005 spec gate round 3" (SG4-03) and Found 2026-11-18 for remediation 3 rows; TE003-SG4-DG-01 is the only such row. (e) `agent-run-log.md` title reads "remediations 1 to 4", with a round-4 section. |

## 4. Findings

### REVIEW-RWB-TE-003-SG6-01: Low. SPEC-001 (c) not-listed text still says "not loaded", and the `@Bean RouterFunction` failing fixture was dropped

**Affects:** SPEC-RWB-TE-003-001 (c); §12 X-S14; §14 backend Test Acceptance Criteria; T-TE003-34 (c1)-(c3); `gate-response.md` "Round 4 remediation" row SG5-01.

**Evidence**
- (a) `spec.md` §12 X-S14: the condition is that a detected source "is not listed in `handlerMappingSources`", but the text is `handler mapping source {source} is not loaded by the contract context` (same in SPEC-001 (c) "A detected source that is not listed fails: ..." and T-TE003-34 (c1)-(c3)). Now that round 4 gives "listed but not loaded" its own text (X-S15), the not-listed text states a cause the check does not test: a source that the contract context does load, but that nobody listed, fails with a message saying it is not loaded. `review/spec-gate-review-4.md` SG5-01 named this mismatch ("names a condition the check never tests"); the round-4 edit kept it for the not-listed case. These are exact texts the tests assert, so the planner and builder will copy them.
- (b) `spec.run4.md` T-TE003-34 (c) had a failing fixture for "a `@Bean RouterFunction` method". `spec.md` T-TE003-34 (c1) replaces it with "a `@Bean` method returning a `HandlerMapping`", and §14 lists the same three cases. The first condition of SPEC-001 (c) has two return types ("`RouterFunction` or a `HandlerMapping`"), and SPEC-001 (b) names functional routes as one reason for the check. A static check that tested only `HandlerMapping`-assignable return types would now pass every T-TE003-34 case. SG5-01 item 2 asked to extend the fixtures, not swap one.

**Required fix**
1. Give the not-listed case a text that names its cause, for example `handler mapping source {source} is not listed in handlerMappingSources`, in SPEC-001 (c), §12 X-S14 and T-TE003-34 (c1)-(c3). Keep X-S15 as it is. Leave the round-3 history rows in `gate-response.md` alone; state the change in the new round's row.
2. Restore the failing fixture for a `@Bean` method returning `RouterFunction` in T-TE003-34 (c), alongside (c1), and add it to the §14 backend static-check list.

## 5. Internal consistency (checked)

- SPEC-RWB-TE-003-001..022 defined once each in §6 (22); §3 has 36 rows, 0 BLOCKED; §18 `REQUIREMENT_COVERAGE_RESULT` 36 / 36; §3 unchanged since remediation 3.
- Test IDs T-TE003-10..36 all defined in §15; every T-TE003 ID cited in `spec.md`, `shared-updates.md`, `gate-response.md`, `assumptions.md`, `compliance-validation.md` and `backend-apis.json` is defined. SPEC-001 Tests cell (T-TE003-10, -11, -34) matches `shared-updates.md` §3.2. T-TE003-28 stays on SPEC-015, T-TE003-34 on SPEC-001 (b), (c).
- §12 rows X1-X8 and X-S1..X-S15 are contiguous; X-S14 and X-S15 cite 001 (c); `compliance-validation.md` and `gate-response.md` cite X-S14 and X-S15 correctly. No other file counts the X-S rows.
- ASM-TE003-01..18: 18 rows in `assumptions.md`, cited set across files is exactly 01..18; run log says 18 (unchanged).
- NEW-TE003-A..G: same set in spec, `assumptions.md`, `shared-updates.md` §1 (OPEN-043..049), `backend-apis.json`, `gate-response.md`.
- Gap IDs: TE003-SG-DG-01..08, TE003-SP-DG-01..06, TE003-SG3-DG-01..03, TE003-SP2-DG-01, -03, -04, TE003-SG4-DG-01 all have rows in `document-gaps.md` and `shared-updates.md` §4; TE003-SP2-DG-02 appears once, as withdrawn. No gap is Blocker = Yes, and none needs to be.
- Fallbacks cited (F-1a, F-1b, F-1d, F-2, F-3, F-4) all exist in §9.
- Report counts unchanged: 1 PASSED + 72 PENDING (E1) + 68 PENDING (E2-E6) = 141, plus 2 `OUTSIDE_SPECIFICATION`.
- Status lines: spec header, `compliance-validation.md`, `shared-updates.md` §3.1 and §3.3, and §18 NEXT_STEP all point at review-5. `assumptions.md` and `document-gaps.md` titles still say "remediation 3", which is correct because neither changed this round.
- Note, not a finding: the `mappingBean` examples in SPEC-001 (c) (`routerFunctionMapping`, `repositoryRestHandlerMapping`) are illustrations. `routerFunctionMapping` is the Spring MVC bean name. The Spring Data REST name could not be checked here (the library is not on the classpath or in the local Gradle cache). A wrong name fails safe (X-S15), so the story that adds Spring Data REST should take the name from the library.

## 6. Gate result

```text
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
SG5 RESOLUTION: SG5-02 resolved (all five parts); SG5-01 partly resolved (SG6-01: not-listed text and the dropped @Bean RouterFunction fixture).
ORCHESTRATOR TRIAGE: coverage precedence (D-RCV-28 (3), D-RCV-40) and A-07 scope (D-RUN-15) still implemented coherently.
DOCUMENT_GAPS: 0 new candidates (no review/document-gaps-5.md); 0 blockers.
NEXT_STEP: Under D-RUN-09 the orchestrator re-runs the Technical Specifier to fix SG6-01 (text only), then this gate runs again as review/spec-gate-review-6.md. Do not start the Implementation Planner before that. PRE-1 (RWB-TE-001 merged) still applies after a PASS.
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1]
```
