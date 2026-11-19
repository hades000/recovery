# Compliance validation — RWB-E1-061 specification (re-run)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-061-GATE-002` |
| Artifact | `output/INC-075-epic-1-RWB-E1-061/specify/spec.md` |
| Stage | Specification gate |
| Reviewer | Compliance Reviewer (agent re-run) |
| Date: first run | 2026-11-04 |
| Date: re-run | 2026-11-06 |
| Overall status | `PASS` |
| Blocking findings | 0 |
| Open findings | 0 |

## 1. Reason for the re-run

The first gate (2026-11-04, `FAIL`) was blocked by one High finding: `promotion_conditions` and
`watch_measures` are jsonb with no machine-checkable grammar, so BR2 and AC5 could not be
implemented and tested generally without breaking the no-hard-coding rule. Decision **D-RCV-33**
(2026-11-06, business analyst with the solution architect, specification gate ruling) restricts the
grammar to the FSD P10 fixture form: exactly one promotion condition clause per version —
`{"metric":"AGREEMENT_RATE","operator":"GTE","threshold":<number>,"scope":"EVERY_LABEL_KEY"}` —
"agreement at least <threshold> for every gap type"; any other metric, operator, scope or second
clause is refused at load. `watch_measures` hold ACCEPTANCE_RATE, CORRECTION_RATE and
FALLBACK_RATE rows for reporting and do not gate. With the restricted grammar AC5's 0.8150 gap-type
score refuses the proposal, naming the gap type and value (TC-E1-061-05). The API Specification v2
now carries `text/csv` and `application/pdf` on the report endpoint's 200 response, as CLAR-002
required.

## 2. First-run findings and their disposition

| ID | Severity | Finding (short) | Disposition | Status |
|---|---|---|---|---|
| REVIEW-RWB-E1-061-001 | High | No machine-checkable grammar for the promotion conditions (CLAR-001). | Ruled as D-RCV-33: the single restricted clause form, anchored in FSD P10 AC-ALT-P10-007-01; carried into the proposal checks, the guardrails and SPEC-006; AC5 refusal testable. | Resolved 2026-11-06 |
| REVIEW-RWB-E1-061-002 | Low | The report endpoint supports CSV and PDF; `api.yaml` declared JSON only. | The 200 response of `/admin/agent-evaluations/{evaluationId}/report` now includes `text/csv` and `application/pdf` in API Specification v2 and its legacy conversion (2026-11-06). | Resolved 2026-11-06 |
| REVIEW-RWB-E1-061-003 | Low | Named Product Owner and FDA are TBC (GAP-006). | Recorded at the specification gate 2026-11-06: acting approver is the exercise owner; names are entered in the increment card before the approval signature (GAP-006 tracking). | Recorded 2026-11-06 |

## 3. Re-run checks

| Check | Result | Evidence |
|---|---|---|
| Authentication and authorization | Pass | Rules and parameters R/C/A; 403 MSG-P4-002 tested. |
| Customer and account data protection | Pass | The report holds counts and rates only; no personal field. |
| Audit logging | Pass | Read-only report; the policy version carries loader, approver, conditions and measures; the frozen/valid-dated rows are the record. |
| Approval controls | Pass | Loader ≠ approver; 409 MSG-P7-002; P1 in force until approval. |
| Separation of duty | Pass | RW-COE loads, RW-RISK approves. |
| API contract | Pass | New report endpoint; JSON plus the CSV/PDF representations now in API Specification v2. |
| Error handling | Pass | RUNNING refusal, missing measures, condition breach (with the D-RCV-33 refusal path), sample minimum and self-approval specified. |
| Test coverage | Pass | Backend unit tests at 80%; 11 system, security and unit scenarios; the condition-check tests are final on the restricted grammar (TC-E1-061-05 spec.) |
| Traceability | Pass | 6 BRs, 7 ACs and 6 exception paths mapped to SPEC-001..015; US-RWB-E1-061 linked. |
| Secrets and configuration | Pass | No secret; the threshold, measures and sample minimum are row/schema values; no business value in code. |
| Design evidence | Pass (not required) | `UI In Scope: NO`; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`. |
| No-assumption policy | Pass | `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`; the grammar is a recorded decision (D-RCV-33) anchored in the FSD. |
| Operational readiness | Pass | Metrics, alerts, feature flag and rollback specified. |

## 4. Recommendation

**Proceed to the Implementation Planner.** The rule schema is loadable, checkable and testable
as written; nothing is hard-coded.

```text
REVIEW_STATUS: PASS
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0 open, 3 closed with disposition]
REVIEW_GATE: Specification gate
REVIEW_GATE_DECISION: Passed; ready for the Implementation Planner.
NEXT_STEP: Start the Implementation Planner on output/INC-075-epic-1-RWB-E1-061/specify/spec.md.
```
