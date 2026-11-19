# Compliance validation — RWB-E1-020 specification

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-020-SPEC-001` |
| Artifact | `output/INC-043-epic-1-RWB-E1-020/specify/spec.md` |
| Stage | Specification gate |
| Reviewer | Compliance Reviewer (agent run) |
| Date | 2026-11-04 |
| Overall status | `PASS` |
| Blocking findings | 0 Critical, 0 High, 0 Medium |
| Warnings | 4 Low (1 resolved) |

## 1. Scope of review

The review checked the specification against:

- `.github/contexts/project-context.md`, `backend-context.md`, `testing-standards.md`.
- `.github/rules/requirement-standards.md`, `traceability-standards.md`,
  `specification-execution-gates.md`, `security-quality-standards.md`, `architectural-standards.md`,
  `pdlc.md`.
- The source story `RWB-E1-020` and the worked example v6.
- The API specification, logical data model, business rules, error/message standard, test strategy
  and controls catalogue.
- The decision log and the intake gap report.

## 2. Findings

| ID | Severity | Area | Finding | Evidence | Remediation | Owner | Status |
|---|---|---|---|---|---|---|---|
| REVIEW-RWB-E1-020-001 | Low | Traceability / version | The spec initially used the worked example v6; the per-story file v5 is the canonical story file and has the same headings plus guardrails, traceability and out of scope. | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 020 Allocation and assignment engine v1 v1.md`; worked example v6; consolidated v7 | Resolved: the spec now cites the per-story file and reproduces its guardrails, traceability and out-of-scope sections. The version gap remains a programme-level gap (GAP-001) for the other stories. | Business analyst | Resolved |
| REVIEW-RWB-E1-020-002 | Low | Reference data | The queue codes `RWB-EXC`, `DEV-HANDLER`, the cap 150 and `ROUND_ROBIN` are example values. The spec treats them as data, but the go-live values are not confirmed. | Story §3, §4; DL22, DL23 | Load the approved values as parameters and confirm before go-live; the spec does not hard-code them. | Centre of excellence | Recorded 2026-11-06 |
| REVIEW-RWB-E1-020-003 | Low | Determinism | The spec fixes the case processing order (`created_at`, then `case_id`) as an implementation decision. The source story does not state the order. | Spec CLAR-009; story §4.2 | Record the order in the job run log and confirm it does not change the round-robin outcome in SIT. | Tech lead | Recorded 2026-11-06 |
| REVIEW-RWB-E1-020-004 | Low | Performance | The 15-minute target for 3,110 cases is assumed (DL11), not an approved NFR. | Story §13 "Done when"; NFR-013, NFR-019; DL11 | Confirm the target or record the SIT result as the baseline. | Solution architect | Recorded 2026-11-06 |
| REVIEW-RWB-E1-020-005 | Low | Approval | The named approvers are `TBC`. The technical review can pass, but the human specification approval cannot be signed. | Spec header; EPIC-001 approval table; GAP-006 | Name the Product Owner and FDA before the specification approval. | Product Owner | Recorded 2026-11-06 |

No Critical, High or Medium findings were found.

## 3. Checks performed

| Check | Result | Evidence |
|---|---|---|
| Authentication and authorization | Pass | Every job/service action names the role and right; `SY-CASEWF`, `SY-RULES`, `SY-DECLOG`, `RW-TEAMMGR`, `RW-CASEOWN`, `RW-PLATADM`, `RW-REFADM`; rerun requires Platform administration U; 403 MSG-P4-002. |
| Customer and account data protection | Pass | The job reads case/queue data; no personal data is written to logs; the decision log carries IDs, not PII. PDPA masking applies to the case read endpoint, not to the job. |
| Audit logging | Pass | Every allocation, overflow, exception, deviation and skip is recorded; the decision log write is the last step and blocks the action on failure; rule ID and version are recorded. |
| Approval controls | Pass | No approval decision in this story; the allocation table version is approved by the Shared operations process owner (RWB-E1-029). |
| Separation of duty | N/A | No approval action. |
| Frontend integration contract | N/A | UI out of scope; no contract delta. |
| API contract | Pass | `NO_API_CHANGE`; existing case read and job rerun endpoints reused; no new version. |
| Error handling | Pass | MSG-P3-011, 012, 013; MSG-P1-001; MSG-P4-002; rollback on log failure; 403/404/409/503 on the rerun. |
| Test coverage | Pass | Backend unit tests required with 80% lines/statements/branches/functions; positive, negative, boundary and error-path tests; 15 system/security scenarios; frontend `NOT_APPLICABLE` with evidence. |
| Traceability | Pass | 9 BRs, 13 ACs, 10 exception paths and 4 state transitions mapped to SPEC IDs; `SPEC` IDs unique; `US-RWB-E1-020` linked; no orphan in the seeded range. |
| Secrets and configuration | Pass | No secrets; queue codes and caps are reference data; no hard-coded business values. |
| Design evidence | Pass (not required) | `UI In Scope: NO`; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`. |
| No-assumption policy | Pass with warnings | CLAR-001..009 resolved; the case order is the only implementation decision and is recorded. |
| Operational readiness | Pass | Job record, monitor, metrics, alerts, run book, feature flag and rollback are specified. |

## 4. Traceability check

| Chain | Result |
|---|---|
| `CTX-FEATURE-003` → `BRD-RWB-003` → `FR-RWB-005` → `US-RWB-E1-020` → `SPEC-RWB-E1-020-001..028` | Pass |
| `BR-RWB-002..005` → `SPEC-005..014` | Pass |
| `REQ-CWC-007..009, 016` → `FR-RWB-005` → `SPEC-005..017` | Pass |
| `AC1..AC13` → `SPEC` rows | Pass |
| `X1..X10` → `SPEC` rows | Pass |
| `TEST` IDs | Seeded as `TC-E1-020-01..15`; execution evidence is a later stage |

The matrix update is recorded in `requirement/Traceability_Matrix.md`; the spec IDs are unique in the
seeded range.

## 5. Unit test applicability check

| Surface | Declared | Review |
|---|---|---|
| Frontend | `NO` / `NOT_APPLICABLE` | Accepted. No screen, component, route, state or label change; SCR-02 and SCR-09 display existing fields. |
| Backend | `YES` / `REQUIRED` / 80% | Accepted. New job, service, evaluator, assignment engine, repositories and summary builder; test scenarios cover the changed behaviour. |

The 80% gate is planned, not claimed. Actual execution and native reports belong to the
Implementation Builder and are checked at the code gate.

## 6. Recommendation

**Proceed to the Implementation Planner** after the human specification review. The four open
warnings do not block the technical handoff. The Product Owner and FDA must name the approvers before
the specification approval is signed; the business analyst must confirm the remaining story versions
before the Epic 1 plan is approved.

```text
REVIEW_STATUS: PASS
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
REVIEW_GATE: Specification gate
REVIEW_GATE_DECISION: Proceed to human review and the Implementation Planner; warnings carry forward.
NEXT_STEP: Start the Implementation Planner on this specification.
```


## 8. Re-validation — gate 002 (2026-11-06)

Compliance Reviewer re-run. The first run's findings are dispositioned below; the specification is unchanged in substance. Findings marked Recorded stay tracked with their owners and the decision-log dates; the affected values remain data or configuration and none is hard-coded. No blocking finding remains.

| Finding | Severity | Short description | Owner | Gate-002 disposition |
|---|---|---|---|---|
| REVIEW-RWB-E1-020-002 | Low | The queue codes `RWB-EXC`, `DEV-HANDLER`, the cap 150 and `ROUND_ROBIN` are example values. The spec treats th | Centre of excellence | Recorded 2026-11-06 — decision DL22 (Service levels per case state; owner Business lead; needed by 2026-11-13); DL23 (Caseload cap and queue rules; owner Product owner; needed by 2026-11-13). |
| REVIEW-RWB-E1-020-003 | Low | The spec fixes the case processing order (`created_at`, then `case_id`) as an implementation decision. The sou | Tech lead | Recorded 2026-11-06 — confirmation owned by Tech lead; the value stays data/configuration, the specification hard-codes nothing, and the item carries into the build hand-over. |
| REVIEW-RWB-E1-020-004 | Low | The 15-minute target for 3,110 cases is assumed (DL11), not an approved NFR. | Solution architect | Recorded 2026-11-06 — decision DL11 (Non-functional targets; owner Solution architect with Risk; needed by 2026-11-05). |
| REVIEW-RWB-E1-020-005 | Low | The named approvers are `TBC`. The technical review can pass, but the human specification approval cannot be s | Product Owner | Recorded 2026-11-06 — confirmation owned by Product Owner; the value stays data/configuration, the specification hard-codes nothing, and the item carries into the build hand-over. |

REVIEW_G2_STATUS: PASS
