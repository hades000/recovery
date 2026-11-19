# Compliance Review — Plan Gate — RWB-E1-043

- RUN_ID: `INC-009-epic-1-RWB-E1-043`
- Story: `RWB-E1-043` — Reference data service with versioned tables
- Gate: Implementation Planner automatic Compliance Reviewer invocation (plan gate). Not a spec review (spec.md is cross-referenced only, as ground truth) and not a code review (no implementation exists yet).
- Reviewer: Compliance Reviewer (`.github/agents/reviewer.agent.md`)
- Date: 2026-11-10
- REVIEW_STATUS: **FAIL** (Low-only; see `REVIEW_GATE_WARNING` below — does not automatically block)
- Findings: `[CRITICAL:0] [HIGH:0] [MEDIUM:0] [LOW:1]`

## Artifacts reviewed

| Artifact | Role |
|---|---|
| `output/INC-009-epic-1-RWB-E1-043/specify/spec.md` | Ground truth, cross-reference only (not re-reviewed) |
| `output/INC-009-epic-1-RWB-E1-043/plan/plan.md` | Primary subject |
| `output/INC-009-epic-1-RWB-E1-043/plan/tasks.md` | Primary subject |
| `output/INC-009-epic-1-RWB-E1-043/plan/data-model.md` | Primary subject |
| `output/INC-009-epic-1-RWB-E1-043/plan/contracts/backend-apis.json` | Primary subject |
| `output/INC-009-epic-1-RWB-E1-043/plan/contracts/frontend-integrations.json` | Primary subject |
| `output/INC-009-epic-1-RWB-E1-043/plan/tests/scenarios.md` | Primary subject |

Context also applied: `.github/contexts/project-context.md`, `domain-context.md`, `backend-context.md`, `backend-standards.md`; `.github/rules/security-quality-standards.md`, `architectural-standards.md`, `traceability-standards.md`, `environment-standards.md`, `versioning-standards.md`, `pdlc.md`, `planning-execution-gates.md`; `docs/decisions/INC-001-decisions.md` (D-RCV-02, -18, -28, -34, -36, -40, -41), `docs/architecture/decisions/ADR-RCV-001-recovery-api-style.md`, `docs/architecture/migration-merge-order-map.md`.

`ace-monorepo/` is not checked out in this workspace; all package/class/migration-path references in the plan are design-time projections and are reviewed for internal consistency and consistency with cited decisions/ADRs, not against a live codebase (per task brief; consistent with CTX-GAP-020 in `project-context.md`).

## Required Checks — assessment

**Authentication and authorization.** All four endpoints consistently map 401→MSG-P4-001 and 403→MSG-P4-002, tied to the "Reference data C/A/R" rights from spec.md §Security and authority (`contracts/backend-apis.json`, plan.md §Authorization, tasks.md TASK-13). The rollback endpoint's authorization ("Reference data A, by analogy with approve") is explicitly marked inferred and tied to IMPL-NOTE-01 rather than asserted as settled — adequate disclosure. Enforcement depends on RWB-E1-022 (`RecoveryAccessGuard`), not yet `SUCCESS`; see "Cross-story dependencies" below. No issue beyond Finding 1.

**Customer and account data protection.** Reference data in scope (PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD, HOLIDAY, PRODUCT_PARAMETER — data-model.md §4) is configuration/table data, not customer or account records. No PII fields appear in `reference_version`/`reference_row`. All test fixtures in `tests/scenarios.md` are explicitly labeled synthetic. No issue.

**Audit logging for sensitive financial actions.** `reference_version` itself carries `author_user_id`, `approver_user_id`, `approved_at` as an append-only (status/approver/approved_at/valid_to only) data-layer audit trail (data-model.md §1, trigger `reject_reference_version_change`). `ReferenceVersionLogger` (TASK-12, TC-E1-043-03) logs one line per table per engine-start cycle, explicitly excluding row-level and party-ID data (CLAR-007, BR7/AC3). Adequate.

**KYC/AML/suitability/consent/approval controls when in scope.** The approval control here is maker-checker (approver ≠ author, enforced by both a CHECK constraint and TASK-08 logic; optimistic locking for concurrent approvals, AC8/X5). DELEGATION_LIMIT approval authority is tied to `doa.txt` rule 11 (RW-RISK), consistent with CLAR-001/DL01. Adequately scoped; no KYC/AML/suitability/consent dimension applies to reference-data versioning.

**Frontend integration versioning and error contract consistency.** `frontend-integrations.json` correctly declares `NOT_APPLICABLE` with citations to spec.md's Change Scope Declaration (`Frontend Changes Required: NO`) and `CHANGE_CLASSIFICATION_RESULT: [UI_IN_SCOPE: NO]`. Accepted per this check's own `NOT_APPLICABLE` allowance — no frontend tasks, screens, or coverage demanded. Backend error-contract consistency is otherwise sound across EP-01..EP-03; see Finding 1 for one inconsistency on EP-04.

**Secrets and environment configuration.** `refdata.cache.ttl-seconds` is externalized via `ConfigurationService` (RWB-E1-042), not hardcoded (data-model.md §4, PRE-5). No secrets, credentials, or hardcoded environment values appear in any reviewed artifact.

**Test coverage and evidence (plan-stage: verify planned, not executed).** `contracts/backend-apis.json` §coverage and plan.md §Unit Test Applicability both specify the backend gate as REQUIRED, 80% line/statement/branch/function via recovery-only JaCoCo tasks (`recoveryCoverageReport`/`recoveryCoverageVerification`, D-RCV-40), scoped to `casewf/refdata/**`, enforced at TASK-20. Frontend is accepted `NOT_APPLICABLE` with no demanded unit tests or coverage report, per this check's own allowance. `tests/scenarios.md` maps all 14 (12 spec + 2 planner-added) scenarios to concrete test classes, synthetic data, and tasks; every unit-test task is `BLOCKED_BY` its implementation task (tasks.md §Pre-submit checks). Planned evidence is adequate for a plan-gate review.

**Frontend/backend applicability verification.** Verified independently: frontend `NOT_APPLICABLE` is evidence-backed (spec.md Change Scope Declaration, not merely "no task"); backend is `REQUIRED` and planned to the 80% gate. No exemption is based only on missing tooling or conflicting scope. Consistent with `implementation-execution-gates.md`.

## Traceability check (SPEC-RWB-E1-043-011/-012/-013/-014 drift correction)

Verified directly (not relying on tasks.md's self-report): grepped every plan artifact (`plan.md`, `tasks.md`, `data-model.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `tests/scenarios.md`) for `SPEC-RWB-E1-043-011|012|013|014`.

- **No file asserts any of these as a real, individually-scoped SPEC-ID mapping.** The only three occurrences (plan.md:170, tasks.md:91, tasks.md:107) are the disclaiming notes themselves, explicitly naming all four IDs as *unmapped with a stated reason* — not claims of coverage.
- `contracts/backend-apis.json`'s rollback endpoint (EP-RWB-E1-043-04) correctly cites `"spec.md §Feature flag and rollback"` and `"CLAR-008"` in its `specRefs`, not a fabricated `SPEC-014`. Its `note` field explicitly restates the non-fabrication rationale.
- Confirmed the drift originates in spec.md itself, not in the plan: spec.md's own "Requirement-to-SPEC Logic Coverage" table never ties `-011..-014` to a BR/AC/X row (only the Unit Test Applicability table's range notation implies them), and CLAR-008's "Resulting SPEC-*" column names "SPEC-014" without tying it to a defined section (spec.md line 269) — the plan correctly declines to propagate this as a real ID.

**Result: correction applied consistently. No finding.**

## Cross-story dependency treatment (RWB-E1-044, RWB-E1-042, RWB-E1-022)

All three are gated as PRE-4/PRE-5/PRE-6 in plan.md §Plan approval preconditions, each with: a named owner, an honest "PENDING to verify" state description (including the RWB-E1-044 INDEX.md-vs-spec.md status conflict, stated rather than hidden), a concrete verification artifact, and a corresponding Risk-table row with mitigation and task. TASK-RWB-E1-043-01 requires Builder to re-verify each directly against `develop` and **stop with `NEXT_STEP`** rather than stub the missing interface — this is the correct treatment for a plan-stage artifact describing work that depends on code outside this story. RWB-E1-022 is additionally flagged as an *undeclared* dependency in the increment card, with an explicit escalation to Context Updater/human at TASK-21. A fourth, related dependency (RWB-TE-001's `casewf` package skeleton) is independently and correctly verified as already `SUCCESS` and already satisfied (plan.md §Plan-time verification, cross-checked directly against `docs/increments/INDEX.md` and `output/INC-002-epic-1-RWB-TE-001/plan/`), so it is rightly not gated as a precondition.

**Result: treatment is adequate. No finding.**

## IMPL-NOTE-01 (rollback field-level inference beyond CLAR-008)

The inference (clearing the superseded version's `valid_to` on rollback) is flagged consistently and traceably in four places: plan.md §Plan-time verification/§Risks, `tasks.md` TASK-09/TASK-13/TASK-17, `contracts/backend-apis.json` EP-RWB-E1-043-04 (both in the endpoint description and its `note` field), and `tests/scenarios.md` TC-E1-043-13 — each stating it is a planner inference beyond CLAR-008's literal endpoint-reuse answer and requires FDA/Technical Specifier confirmation before Builder treats it as final, and instructing the PR/MR description to name it explicitly. This is sufficient, redundant-by-design flagging that cannot be missed downstream.

**Result: flagging is sufficient. No finding.**

## Findings

### REVIEW-RWB-E1-043-PLAN-001 — Low

**Title:** Rollback endpoint error contract has an unresolved overlap between its 404 and 422 conditions.

**Location:** `output/INC-009-epic-1-RWB-E1-043/plan/contracts/backend-apis.json`, endpoint `EP-RWB-E1-043-04` (`POST /api/recovery/v1/admin/reference-loads/{loadId}/rollback`), `errors` array.

**Finding:** The endpoint lists both:
- `404 MSG-P4-003`, `when: "loadId does not resolve to an APPROVED version."`
- `422 MSG-P3-027`, `when: "Version is not in an APPROVED state."`

These two conditions describe the same underlying case — a `loadId` that resolves to an existing `reference_version` row whose status is not `APPROVED` — without any stated rule for which status code applies when. By contrast, the analogous approve endpoint (`EP-RWB-E1-043-02`) uses a single `404 MSG-P4-003` for its equivalent "does not resolve to a VALIDATED version" condition, with no overlapping 422. Builder has no documented basis to implement this consistently, and the two test scenarios that exercise rollback (`TC-E1-043-13`) only cover the success path, so this ambiguity would not be caught by the planned test set either.

**Affected:** `SPEC-RWB-E1-043-005`/`-010` (by analogy, approval/rollback status-transition behaviour); `spec.md §Feature flag and rollback`; `TASK-RWB-E1-043-09`, `TASK-RWB-E1-043-13`, `TASK-RWB-E1-043-17`.

**Severity rationale:** Low — confined to one edge case of one of four endpoints; does not affect the story's core design, data model, authorization model, or coverage plan; resolvable by Builder choosing one consistent rule, but should be resolved explicitly (ideally by FDA/Technical Specifier alongside the IMPL-NOTE-01 confirmation already pending) rather than left to arbitrary implementation choice.

**Recommendation:** Before TASK-09/TASK-13 are coded, pick one rule (e.g., 404 only when no `reference_version` row resolves to `loadId` at all; 422 when a row resolves but its status is not `APPROVED`) and update `contracts/backend-apis.json` and `tasks.md` TASK-09's error-handling description accordingly. Add a negative-path assertion to `TC-E1-043-13` or a new scenario covering "rollback attempted on a VALIDATED/ROLLED_BACK version."

## Overall status

```
REVIEW_STATUS: FAIL
[CRITICAL:0] [HIGH:0] [MEDIUM:0] [LOW:1]
BLOCKING: NO (Low-only)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
```

Per `.github/rules/pdlc.md`: this is a Low-only result. The `FAIL` status is preserved (not relabelled `PASS`) because a finding exists; it does not automatically block the handoff, and `REVIEW_GATE_WARNING` is emitted verbatim above. Independent stage hard gates (80% coverage, required unit tests) remain binding at Builder stage regardless of this result. Finding `REVIEW-RWB-E1-043-PLAN-001` must remain visible through plan approval and Builder handoff until a human records remediation or explicit acceptance; if accepted without a code change to the contract, the accepted disposition must stay visible in the next gate's review the same way `REVIEW-RWB-E1-043-001/-002/-003` were carried forward from the spec gate into this plan.

## Summary for the handoff record

- 3 cross-story dependency gates (RWB-E1-044, RWB-E1-042, RWB-E1-022): adequately handled, not re-flagged.
- IMPL-NOTE-01 rollback inference: adequately and redundantly flagged, not re-flagged.
- SPEC-RWB-E1-043-011/-012/-013/-014 drift correction: verified applied consistently across all 7 reviewed artifacts, no stray individual-ID claim found.
- 1 new Low finding: rollback endpoint 404/422 overlap (`REVIEW-RWB-E1-043-PLAN-001`).
- No Critical, High, or Medium findings. No frontend demands made against the `NOT_APPLICABLE` UI scope. No secrets, PII, or hardcoded production data found in any reviewed artifact.
