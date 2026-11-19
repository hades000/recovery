# Spec gate re-review (gate 3): RWB-TE-001 (INC-002-epic-1-RWB-TE-001)

| Field | Value |
|---|---|
| Review type | SPEC GATE RE-REVIEW (gate 3, specification stage) |
| Story | RWB-TE-001 (Jira `TB0001-1235`) |
| Reviewer | Compliance Reviewer (agent run), 2026-11-09 |
| Prior reports | `review/spec-gate-review.md` (gate 1), `review/spec-gate-review-2.md` (gate 2: REVIEW-RWB-TE-001-015 Medium, -016..-018 Low) |
| Tech-lead rulings applied | 2026-11-09: 015 hand-define the frontend `test` target in `frontend/package.json` (no `nx.json` / root `package.json` change); 017 TE-001 always edits `backend/build.gradle.kts` to add the test-tooling class directory to the recovery JaCoCo tasks; 018 add OPEN items. Recorded as D-RCV-43 and OPEN-021..024. |
| Artifacts reviewed | `specify/spec.md`, `specify/compliance-validation.md`, `specify/contracts/backend-apis.json`, `specify/contracts/frontend-integrations.json`, `docs/decisions/INC-001-decisions.md` (D-RCV-38..43, next-free line), `docs/open-items.md` (OPEN-021..024), `docs/increments/INC-002-epic-1-RWB-TE-001.md`, `requirement/Traceability_Matrix.md` rows 111, 122, 125, 141, 338 |
| ACE evidence (read-only) | `ace-monorepo` `develop` 96b0d1c6: `frontend/package.json` (no `test` script; `nx.targets.check.dependsOn` = `vite:build`, `check-format`, `eslint:lint`, `typecheck`), `nx.json` (plugins `@nx/gradle`, `@nx/js/typescript`, `@nx/vite/plugin` without a test option, `@nx/eslint/plugin`; no `@nx/vitest`), root `package.json` (`nx` 24.0.3, no `@nx/vitest`), `backend/build.gradle.kts` (no `jacoco`) |
| Overall status | **FAIL** |
| Blocking | **NO**: one Low finding only (REVIEW-RWB-TE-001-019); `REVIEW_GATE_WARNING` applies |

## Disposition of gate 2 findings

| Finding | Sev. | Disposition | Evidence |
|---|---|---|---|
| REVIEW-RWB-TE-001-015 | Medium | **Resolved** | SPEC-015 states Nx 24 infers no `test` target, `@nx/vitest` is not registered, and the target (`vitest run --coverage`) is hand-defined in `frontend/package.json` `nx.targets` and added to `check` `dependsOn`, with no `nx.json`, root `package.json` or CI change; the plan proves one `test` target with `npx nx show project frontend` (`spec.md:156`). SPEC-017 lists the edit (`spec.md:158`); Impacted Nodes too (`spec.md:35`). Contract `wiring` matches (`frontend-integrations.json:34`). D-RCV-40 now defers wiring to D-RCV-43, and D-RCV-43 (1) matches (`INC-001-decisions.md:76`, `:79`). ACE evidence confirms the premise: `frontend/package.json` has no `test` script, so no package-script target collides, and `nx.json` has no vitest plugin. |
| REVIEW-RWB-TE-001-016 | Low | **Resolved** (one residual line, see REVIEW-019 (3)) | SPEC-020 states the expected result: `PASS` with 0/0 totals recorded as printed plus the file list, and the rule proven by T-TE001-07 (`spec.md:161`). D-RCV-43 (3) and contract `coverage` match (`frontend-integrations.json:35`). The Frontend Unit Test Applicability row was not updated (`spec.md:135`). |
| REVIEW-RWB-TE-001-017 | Low | **Resolved** | SPEC-017 says `backend/build.gradle.kts` is always edited, creating the tasks if RWB-E1-044 has not, and adding the test-tooling class directory in either order (`spec.md:158`). SPEC-020 (`spec.md:161`), the Backend applicability row (`spec.md:136`), Impacted Nodes (`spec.md:35`), contract `addedBy` (`backend-apis.json:382`) and D-RCV-43 (2) match. No conditional "only if E1-044 has not merged" text remains for `build.gradle.kts`; the only remaining condition is the `testImplementation` line, which is a separate, correctly conditional item. The RWB-E1-044 planner is named in D-RCV-43 "who must act". |
| REVIEW-RWB-TE-001-018 | Low | **Resolved** | OPEN-021 (BA story text: D-RCV-36, -37, -39, -42, -05), OPEN-022 (Context Updater: FS-1.2, frontend-context §Host), OPEN-023 (ACE tech lead: `vitest`, `@vitest/coverage-v8`, JaCoCo, shared files incl. `backend/build.gradle.kts`, needed before plan approval), OPEN-024 (ACE team: common and collection roots) are in `docs/open-items.md:22-25` with stories, owner, needed-by and links. `spec.md:266` references them. |

REVIEW-RWB-TE-001-001 and -003 (Low, superseded spec) stay open and visible as recorded in `compliance-validation.md` §3.

## New findings

| ID | Severity | Location | Maps to | Issue | Required fix |
|---|---|---|---|---|---|
| REVIEW-RWB-TE-001-019 | Low | `compliance-validation.md:21`, `compliance-validation.md:66`, `spec.md:135` | REVIEW-015, -016 residuals; D-RCV-43 | Three stale lines left by the remediation. (1) The checklist row "Decisions applied" lists `-36..-42` and omits D-RCV-43, which the spec header (`spec.md:19`) and SPEC-015/-017/-020 now cite. (2) The gate 1 disposition of REVIEW-010 still reads "Fixed: ... inferred `@nx/vite` `test` target", with no note that REVIEW-015 / D-RCV-43 replaced it. A reader of §4 sees the wrong wiring stated as the fix. (3) The Frontend Unit Test Applicability row does not carry the expected 0/0 `PASS` result that gate 2 REVIEW-016 asked to state there; it is only in SPEC-020. No contradiction, but the row is what the Implementation Builder reads at the hard gate. | (1) Change to `-36..-43`. (2) Append "(item 4 superseded by REVIEW-015: hand-defined target, D-RCV-43)" to the REVIEW-010 status. (3) Add to the Frontend row: "expected `PASS` with 0 measurable statements recorded as printed (SPEC-020, D-RCV-43 (3)); the rule is proven by T-TE001-07". Text-only; no re-ruling needed. |

## Consistency checks (no finding)

| Check | Result |
|---|---|
| Stale references to an inferred `test` target | None in `spec.md`, the contracts, D-RCV-40/-43, open items, card or matrix. Only `compliance-validation.md:66` (REVIEW-019 (2)). |
| Conditional `build.gradle.kts` edits | None remain. `compliance-validation.md:27` "JaCoCo plugin if RWB-E1-044 has not added it" concerns the plugin dependency, not the file edit, and is accurate. |
| Spec ↔ contracts ↔ D-RCV-38..43 | Consistent: wiring, coverage scope, `addedBy`, allow-list, client libraries, decision references. `INC-001-decisions.md:35` gives next free D-RCV-44. |
| Spec ↔ increment card | Card status "Spec gates 1 and 2 FAIL ...; REVIEW-004..018 remediated (D-RCV-38..43), gate 3 pending" (`INC-002...md:151`); review folder link (`:142`). Consistent. |
| Spec ↔ Traceability Matrix | Row 141 "D-RCV-36..43; spec gate 3 pending"; row 338 "gates 1-2 FAIL ..., REVIEW-004..018 remediated; gate 3 pending"; SPEC ranges in rows 111, 122, 125 match the spec Traceability table. Consistent. |
| Status block (`spec.md:270-279`) | `CONTRADICTIONS: 0` is now accurate (the REVIEW-015 contradiction is gone). `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]` is correct: OPEN-021..024 are owner actions outside the run, not open clarifications. Front matter and header `SUCCESS` consistent. |
| Hand-defined target in ACE | No `test` script in `frontend/package.json` and no vitest plugin in `nx.json`, so exactly one `test` target results. The target's working directory (`frontend/`) is a plan detail; `npx nx show project frontend` is the planned proof. |
| 0/0 frontend threshold | With no measurable statements, the V8/Istanbul summary reports 100% or `Unknown`, neither below 80, so the threshold check does not fail. The spec records this as the expected result rather than claiming a figure. |
| PII, secrets, production data | None. |
| Authorization, audit, KYC/AML | N/A (D-RCV-36). |
| Design evidence | `NOT_REQUIRED` (UI NO). |

## Required checks summary

| Check | Result |
|---|---|
| Authentication / authorization | N/A (D-RCV-36) |
| Customer / account data protection | PASS |
| Audit logging | N/A |
| KYC/AML/suitability/consent/approval | N/A |
| Frontend integration versioning / error contract | N/A for API; lint contract and runner wiring consistent |
| Secrets and environment configuration | PASS |
| Requirement-to-SPEC coverage | 6/6 BRs |
| Unit-test gates planned | PASS: native JaCoCo and `@vitest/coverage-v8` at 80%, both surfaces REQUIRED, wiring and merge order settled (D-RCV-43) |
| Traceability | PASS |
| Open-items tracking | PASS (OPEN-021..024) |

## Status lines

```text
REVIEW_STATUS: FAIL
REVIEW_TYPE: SPEC_GATE_RE_REVIEW
RUN_ID: INC-002-epic-1-RWB-TE-001
GATE2_FINDINGS: [RESOLVED: 4] [NOT_RESOLVED: 0] (REVIEW-RWB-TE-001-015..018; 016 residual line in 019)
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1]
REVIEW_BLOCKING: NO [REASON: Low-only findings (REVIEW-RWB-TE-001-019)]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
NEXT_STEP: Human disposition of REVIEW-RWB-TE-001-019 (three text edits, or explicit acceptance), plus earlier Low findings -001 and -003. Specification approval by the gate owner, and OPEN-023 (ACE tech lead approval) before plan approval. Then a human starts Implementation Planner; this review does not start it.
```
