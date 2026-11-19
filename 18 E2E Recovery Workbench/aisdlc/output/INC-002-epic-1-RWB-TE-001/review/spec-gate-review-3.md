# Spec gate review, round 3: RWB-TE-001 (INC-002-epic-1-RWB-TE-001)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-001-SPEC-007` |
| Stage | Specification gate, round 3 (re-review after remediation of `REVIEW-RWB-TE-001-SPEC-006`) |
| Artefact | The whole revised set in `specify/`: `spec.md` (v4, 18 Nov 2026), `contracts/backend-apis.json` (v4), `contracts/frontend-integrations.json` (unchanged), `compliance-validation.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `gate-response.md` (with "Round 2"), `agent-run-log.md`. The `*.run2.*` files were used only to compare v3 with v4. |
| Reviewer | Compliance Reviewer (agent run, `.claude/agents/compliance-reviewer.md` adapted by `aisdlc/RUN-BRIEF.md`) |
| Date | 2026-11-18 |
| Baseline | Story files v7 (RWB-TE-001 v1; RWB-E1-028 v2, -039 v1, -042 v1, -043 v2, -071 v1, -072 v1, -073 v1), D-RCV-36 §3.3, D-RCV-35 §8.2, decision register, `AI-SDLC-BUILD-LOG.md` §1 D-RUN-06..-13 and the RWB-TE-001 triage row at 2026-11-17T23:57:10 (orchestrator = Claude Code, an AI agent), `aisdlc/.github/rules/pdlc.md`. Code read on 18 Nov 2026: `backend/src/main` and `backend/src/test` (all 27 recovery main types and 9 test classes), `backend/build.gradle.kts`, `application.yaml`, `spring-modulith-api-2.1.1.jar` and `spring-modulith-core-2.1.1.jar` (`javap`), `frontend/eslint.config.js`, `vite.config.ts`, `tsconfig.json`, `package.json`, `src/auth/auth.tsx`, `.gitlab-ci.yml`, `scripts/dev.ps1`. Run specs consulted: INC-003 (E1-042), INC-005 (TE-003), INC-008 (E1-043). |
| Previous rounds | `review/spec-gate-review.md` (SPEC-005, FAIL H2 M4 L4), `review/spec-gate-review-2.md` (SPEC-006, FAIL L4) |
| MCP | Jira, Confluence, GitLab, Figma: not connected (RUN-BRIEF rule 5). `N/A`; local files used. No git run, no code edited, no other file written. |

## Status

**`FAIL`** (Low findings only; the handoff is not blocked)

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 2 | 033, 034 |

The four round-2 findings (029–032) are resolved. The round-1 resolutions (019–028) still hold after the
v4 changes. The two new findings are Low and concern coordination text only (shared-update rows,
an assumption's stated consequences, and stale identifiers). Neither changes the TE-001 design or its
tests. Under `pdlc.md` the status stays `FAIL`, the findings stay visible, and a human must dispose of
them. The orchestrator is an AI agent and cannot give that disposition (D-RUN-09).

`REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.`

## Earlier findings

### Round 2 (029–032)

| Finding | Severity | Status | Evidence in v4 |
|---|---|---|---|
| 029: SU-08 misses RWB-E1-042 and TE-003 | Low | **Resolved** | `shared-updates.md` SU-08 now has an INC-003 RWB-E1-042 entry with every item the fix asked for: (a) code in `recovery.casewf.config`, published `casewf.config.api` with `@NamedInterface(name = "config.api", propagate = false)` (story v7 E1-042 v1 §13, line 237, matches); (b) `RecoveryProperties` / `RecoveryFlags` replaced by module records and `integration.flags.api`; (c) problem types in `access.api` / `access.internal`, so extending them is a P4 change; (e) the "TE-001 moves it" premise holds only if E1-042 merges first. Item (d) adds the P3↔P4 cycle warning, which I checked: after the move `casewf.admin.TemporalAdminController` imports `ApiError` / `ApiProblemException` (P3 → P4), so a P4 → P3 call is a module cycle. The INC-005 RWB-TE-003 entry gives the new homes of `ApiExceptionHandler`, `ProblemFactory` (`access.internal`) and `TemporalAdminController` (`casewf.admin`), plus `propagate = false` for the generated packages. The INC-008 RWB-E1-043 entry is extended for D-RUN-10/-11, and its claim is accurate: the current INC-008 spec (line 68) puts `ReferenceLoadController` and `ParameterLoadBranch` in P4 `recovery.access.refload`, calling P3 `casewf.refdata.api` and E1-042's handler. The INC-003 spec (SPEC-RWB-E1-042-026) still places everything in `platform`, as SU-08 says. The map needs no schema change for `config.api` / `refdata.api`: both match the `published` item pattern (field matrix, contract `laterEntries`). |
| 030: published packages expose implementation types | Low | **Resolved** | Option (b) taken, with the reasons stated. Temporal and Quartz implementation moves to non-published `casewf.workflow.internal` / `casewf.timers.internal` (Relocation table). Every `@NamedInterface` declares `propagate = false` (SPEC-001 (b)(c)), and the map rule enforces it (SPEC-004 (d), T-TE001-02). I confirmed from the jars that `NamedInterface.propagate` exists with default `true` (`spring-modulith-api-2.1.1`), and that `NamedInterfaces` in `spring-modulith-core-2.1.1` reads `propagate()` when it collects annotated sub-packages. `PdpaPayloadCodec` becomes package-private. That is safe: its only users are `TemporalConfig` (same package) and `PdpaPayloadCodecTest` / `PlatformSmokeWorkflowTest`, which move into the same test package. `PlatformE2ETest` uses only the string `"PlatformSmokeWorkflow"`. `PlatformSmokeWorkflow` and `TimerDueJob` stay public in non-published packages, which is correct: `TemporalAdminController.smoke()` uses the workflow interface from `casewf.admin`, Quartz instantiates `TimerDueJob` reflectively, and both packages are inside P3. The self-found defect is real. `TemporalAdminController`'s constructor takes `TemporalProperties`, which is package-private today (`record TemporalProperties`, line 13). v3 would not have compiled, and v4 makes the record public in the non-published package. SPEC-025 and contract `publishedTypesInitial` list the public types per published package; I checked them against the code. T-TE001-14 tests them. SU-06 and SU-12 tell E1-028 and E1-071. |
| 031: `DroolsRuleEngineTest` strings undercounted | Low | **Resolved** | SPEC-022 (f) names both workbook rows: `Import` (line 97) and `Variables` (line 98, `…RuleOutcome outcome`). A search of `backend/` (excluding `build/`) for `recovery.(platform\|rules\|workflow\|documents)` finds string literals only on those two lines. The other hits are `package` / `import` lines and `.gitlab-ci.yml`'s `**/RecoveryFlywayConfig.java`, a file-name glob that still matches after the move. T-TE001-06 asserts the search is empty after the move. |
| 032: §13 step 7 has no verification step | Low | **Resolved** | SPEC-012 (b) states the local merge gate. I verified it in `scripts/dev.ps1`: `test` runs `Invoke-Gradle test` and then `Invoke-Npm run check`, and each throws on `$LASTEXITCODE -ne 0`. The orchestrator merges only on green ([BLOG] triage row; D-RUN-06). T-TE001-13 is a three-run negative control with uncommitted probes. Run 1 holds an `HttpClient` field in `casewf.internal`; a field is right, because an unused import leaves no bytecode. Run 2 uses `import "@/auth/auth"`. This is better than the round-2 suggestion: `src/auth/auth.tsx` exists, so `typecheck` passes and `lint` fails, and the D-RCV-39 regex `^@/(?!components/ui/\|lib/utils$\|…)` rejects that path. A missing `@/modules/collection/x` would have failed `tsc` first. Run 3 is clean. Host-side blocking is HV-01 with SU-13 and is never claimed as tested. |

### Round 1 (019–028): still hold after v4

| Finding | Still resolved? | Check made on v4 |
|---|---|---|
| 019 relocation | Yes | The Relocation table still covers all 27 main types under `recovery/**` (counted: documents 2, platform api 4, platform internal 8, rules api 5, rules internal 2, workflow api 1, workflow internal 5). The v4 split of `casewf.workflow` / `casewf.timers` into published and `.internal` adds no cross-module edge. SPEC-022 (d) is unchanged and matches the imports: `casewf.rules` → `integration.flags.api` (`DroolsRuleEngine` → `RecoveryFlags`) and `casewf.admin` → `access.api`. Every other edge stays within one module. `TemporalAdminController` → `TemporalProperties` / `PlatformSmokeWorkflow` stays within P3. No package-private type crosses a new package line except `TemporalProperties`, which v4 fixes. I checked `DroolsProperties` (and its nested `Registration`), `DroolsRuleEngine`, `TemporalConfig`, `QuartzTimerScheduler`, `ProblemFactory`, `PlatformConfig`, `RecoveryProperties` and `BlobDocumentStore`. |
| 020 coverage | Yes | SPEC-020, Unit Test Applicability backend row and contract `coverage` are unchanged: whole tree, four counters, no main class excluded, baseline FAIL stated. SPEC-024 now names `casewf.workflow.internal.TemporalConfig`, `TemporalProperties`, which matches the new home. |
| 021 ACs | Yes | AC1–AC7 / X1–X6 rows unchanged. The Flow 6 row is upgraded to DIRECT for the local gate. |
| 022 BND-5 | Yes | `BlobDocumentStore` → `dochub.storage`; `clientPackages` P5 `[storage]` unchanged. T-TE001-13 Run 1 relies on the same rule. |
| 023 BND-6 | Yes | SPEC-003 / -021 / -026 unchanged; `noRecoveryClassNamesAPublicTable` kept. |
| 024 change scope | Yes | `scripts/dev.ps1`, `.gitlab-ci.yml` and the frontend config files are still unchanged. T-TE001-13 probes are uncommitted. New nodes add the two `.internal` sub-packages. |
| 025 ADR | Yes | BR5 still cites REQ-DRI-006 / ADR-010. |
| 026 X7 | Yes | `MOVED_OUT_OF_SCOPE`, SU-05 unchanged. |
| 027 downstream packages | Yes, with a gap in the warning | SPEC-004 (g) and SU-09 are unchanged. SU-09's example destination for E1-072/E1-073 now runs into the dependency direction that v4 documents (new finding 033). |
| 028 identifiers | Yes for the items listed then | `EPIC-001` / `RWB-TE-001`, `TOTAL_RULES: 13` in both files. v4 left new stale version and test-range references (new finding 034). |

## New findings

### REVIEW-RWB-TE-001-033: Low. ASM-01 makes P4 `access` a dependency of every module, but the stated consequences (ASM-01, SU-02, SU-09) name only E1-042/E1-043, while story v7 E1-073 and E1-039 make P4 call P3 and P7

- **Affects:** ASM-01 ("Constraint this creates"), SPEC-022 (d), `shared-updates.md` SU-02 (open-item text) and SU-09 (E1-072 / E1-073 destination).
- **Evidence:**
  - v4 documents that "every module that throws a problem type depends on P4 `access`, so `access` must not depend on such a module, or `ModulithTest` fails on the cycle". It says this "affects RWB-E1-042 and RWB-E1-043" (ASM-01; SPEC-022 (d)). After TE-001, P3 already depends on P4 (`casewf.admin` → `access.api`).
  - Story file v7 RWB-E1-073 v1 §13 (line 321) puts its "endpoints and the package version writes in the P4 package `recovery.accessadmin.rulepackages`". Its load path, scenario runner and dry run "call the published RuleEvaluator and RuleCatalog of RWB-E1-072" (line 317), which live in P3 `recovery.casewf.rules`. That is P4 → P3. SU-09 tells the E1-072 / E1-073 owners to move the package to "for example P4 `access.rulepackages`". That destination gives a P3↔P4 cycle with TE-001's P3 → P4 edge, and SU-09 does not carry the warning that SU-08 gives E1-043 for the same pattern.
  - Story file v7 RWB-E1-039 v1 §13 puts `AccessLogWriter` in P4 `recovery.access.accesslog`, and it "calls the P7 DecisionLogWriter" (P4 → P7). Under ASM-01, any P7 class that throws `ApiProblemException` or uses `ApiError` depends on P4. For example, the decision-log query API-P7-006 that E1-039 §12 cites returns 403 MSG-P4-002 and 503. That gives a P4↔P7 cycle.
  - SU-02 is the open item through which the recovery tech lead confirms the module of the error types. It asks only "Confirm or name the module". It does not say that the chosen module becomes a sink that may depend on no module that throws a problem type. That consequence is the deciding factor for the choice. ASM-01's "Effect if wrong" ("No behaviour changes") understates it.
- **Required fix (text only, no design change in TE-001):**
  1. Extend ASM-01's constraint and SPEC-022 (d) to name RWB-E1-073 (P4 → P3 `RuleEvaluator` / `RuleCatalog`) and RWB-E1-039 (P4 → P7 `DecisionLogWriter`) as known conflicts.
  2. Add to SU-02's open-item text that the module holding `ApiError` / `ApiProblemException` / `ProblemFactory` can depend on no module that uses them. Name the conflicting story placements, so the tech lead decides with that constraint visible.
  3. In SU-09, give E1-072 / E1-073 the same dependency-direction warning as SU-08 gives E1-043. Either drop "P4 `access.rulepackages`" as the example, or qualify it: the P4 endpoints must not call P3 types, or the code goes in a P3 `casewf.rules` sub-package.

### REVIEW-RWB-TE-001-034: Low. Stale version and test-range references after v4

- **Affects:** `shared-updates.md` SU-01 and SU-03; `compliance-validation.md` title.
- **Evidence:**
  - SU-01 (Traceability Matrix rows) still lists tests "T-TE001-01..-12". v4 adds T-TE001-13 (§13 step 7 local gate) and T-TE001-14 (published surface), and the spec's Traceability table cites both and HV-01. The Traceability Manager applies SU-01 as written, so the step 7 trace (`[S] §13 step 7` → SPEC-012 → T-TE001-13 / HV-01) would be lost.
  - SU-03 asks for the card status "specified v3, awaiting spec gate". The spec is v4.
  - `compliance-validation.md` line 1 reads "specification v3", while its own table (line 5) says v4.
- **Required fix:**
  - SU-01: change the test range to "T-TE001-01..-14" and add the HV-01 human-verification row.
  - SU-03: change "v3" to "v4".
  - `compliance-validation.md`: change the title to "specification v4".

## Checks performed

| Check | Result |
|---|---|
| Required spec sections and status lines (`specification-execution-gates.md`) | PASS. All sections present; new "Human verification items" section; `CLARIFICATION_STATUS` counts (2 open items, 9 assumptions, 1 HV) match SU-02, SU-13, ASM-01..-09 and HV-01. |
| Change classification `NEW_STORY`, UI NO, Logic YES, API NO, `NO_API_CHANGE` | PASS. `TemporalAdminController` keeps its paths, `@PreAuthorize`, `@ConditionalOnProperty` and body. The workflow type string `PlatformSmokeWorkflow` (asserted by `PlatformE2ETest` line 86) is the simple name and does not change. |
| BR1–BR6, AC1–AC7, X1–X7 against story v7 | PASS. Unchanged from round 2; `REQUIREMENT_COVERAGE_RESULT` 13/13 agreed. |
| Story §13 step 7 and "Done when" | PASS (local, T-TE001-13); HV-01 open for the host. The "Done when" report part is met by CI `backend-unit` `reports: junit`. |
| D-RCV-36 §3.3 / E1-071 BR1 / E1-028 X10 | PASS. Published `casewf.workflow` holds `WorkflowIds` only; the implementation sits under `recovery.casewf.workflow..` / `recovery.casewf.timers..` as BR1 and X10 read with sub-packages. ASM-09 gives the fallback if E1-071 reads BR1 as a single package. |
| Published surface (BND-3, BR6) | PASS. SPEC-025 equals the code after the move; `propagate = false` makes the map the only source of published packages. |
| Implementable against this repository | PASS. Visibility changes compile by reading (see the 030 and 019 rows). The probes in T-TE001-13 follow the order of `npm run check` (`typecheck && lint && coverage`). |
| Backend / frontend coverage scope and gates (80%, four metrics) | PASS (planned). Unchanged from round 2. |
| Authorization, authentication | N/A for new code. `SecurityConfig` and the `@PreAuthorize` checks move unchanged. Making `TemporalProperties` public exposes the `codecKey` accessor inside P3 only (non-published package). No value is logged or returned; the `codecKey` stays sourced from Key Vault / `.env`. |
| Customer/account data protection, PDPA, personal data | PASS. Class and package names and synthetic values only; the probes contain no data. |
| Audit logging, KYC/AML/consent | N/A. Build-time enabler. |
| Secrets and environment configuration | PASS. Property keys and `application*.yaml` unchanged. |
| Frontend integration and error contract | PASS. `frontend-integrations.json` unchanged and consistent; `ApiError` codes unchanged. |
| No-question rule, assumptions, open items | PASS. ASM-09 has a basis and an effect-if-wrong. The orchestrator triage is cited as Claude Code (an AI agent), not as a human decision (CLAR-015/-016, gate-response Round 2). |
| Downstream coordination (`shared-updates.md`) | Low (033, 034) |
| Design evidence | `NOT_REQUIRED`, which is correct for UI In Scope NO |

## Document gaps found in this review

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why | How this review proceeded |
|---|---|---|---|---|---|---|
| RG3-01 | Story file v7 RWB-E1-073 v1 §13 (P4 `recovery.accessadmin.rulepackages` endpoints; load path calls P3 `RuleEvaluator` / `RuleCatalog`) | Two-way package dependency between P3 and P4. Spring Modulith `verify()` (BND-3, D-RCV-11, D-RCV-42) rejects it as a module cycle. | Story file v7 RWB-E1-072 v1 §13 (line 239): P3 `recovery.casewf.rules` uses tables "owned by the P4 package `recovery.accessadmin.rulepackages`" through published interfaces (P3 → P4) | No (for RWB-TE-001) | TE-001 builds neither story. The owners are later in Build Sequence v6 and must settle it under D-RUN-08. | Reported through finding 033 (SU-09 wording). The E1-072 / E1-073 specifiers should record it in their own `document-gaps.md`. The orchestrator may add it to `aisdlc/DOCUMENT-GAPS.md`. |

DG-01..DG-09 in `specify/document-gaps.md` are unchanged, evidenced and correctly dispositioned.

## Plan inputs (not findings)

1. **T-TE001-14 and the unnamed interface.** Spring Modulith 2.1.1 always adds the unnamed (base-package) interface: `NamedInterfaces.discoverNamedInterfaces` starts from `NamedInterface.unnamed(basePackage)`. Assert on the explicit interfaces (filter `isUnnamed()`), or expect `<<UNNAMED>>` with no public type, which SPEC-004 (e) guarantees. Do not assert an exact set of four.
2. **T-TE001-13 exit codes.** Invoke `powershell -NoProfile -File scripts/dev.ps1 test` and record the process exit code. Inside an existing session, a `throw` ends the script without setting a process exit code. `$LASTEXITCODE` then still holds Gradle's or npm's code, which is non-zero but is not the script's own exit code.
3. **Merge gate versus coverage gate.** `dev.ps1 test` (the orchestrator's merge criterion) runs `test` and `npm run check`, but not `recoveryCoverageVerification`. T-TE001-10 must be shown separately at the code gate (SPEC-020 (e)).
4. **Fixture `package-info` files.** The map rule requires `propagate = false` on every `@NamedInterface`. If it also runs over the fixture roots (TC-TE-001-03, T-TE001-02), declare it in the fixture `package-info` files, except in the fixture that tests the default.
5. **`PdpaPayloadCodec` narrowing.** `TemporalConfig.pdpaPayloadCodec` returns the package-private type. That works with `proxyBeanMethods = false`. Keep the bean method and the class in the same package.
6. Round-2 plan inputs 1–5 and 7 still apply. Plan input 6 is now part of the spec (SPEC-004 (d)).

## Other observations (not findings)

- Story v7 E1-071 line 216 says that the `WorkflowGateway` "applies the PdpaPayloadCodec". The codec is now package-private in `casewf.workflow.internal`, so E1-071's gateway implementation must sit in that package or use the configured `WorkflowClient`. SU-12 states the codec's visibility, which is enough.
- SU-06 asks E1-028 to keep new implementation code out of the published `casewf.timers`. A package-private class there would also be unreachable from other modules. The stricter wording is harmless.

## Status lines

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [COVERED_RULES: 13] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: build-time rules and package relocation without behaviour change]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
PRIOR_FINDINGS: 029-032 RESOLVED (4 of 4); 019-028 STILL RESOLVED (10 of 10)
```
