# Compliance validation — RWB-E1-018 specification (re-run)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-018-GATE-002` |
| Artifact | `output/INC-040-epic-1-RWB-E1-018/specify/spec.md` |
| Stage | Specification gate |
| Reviewer | Compliance Reviewer (agent re-run) |
| Date: first run | 2026-11-04 |
| Date: re-run | 2026-11-06 |
| Overall status | `PASS` |
| Blocking findings | 0 |
| Open findings | 0 |

## 1. Reason for the re-run

The first gate (2026-11-04, `FAIL`) was blocked by one High finding: no source stated which account
is `is_primary` when several accounts are grouped into one case. Decision **D-RCV-30**
(2026-11-06) rules it: `is_primary` is true for exactly the account the case was opened on;
for a grouped batch the group's first eligible account in account-number order opens the case; later
linked accounts never take primary. The wording comes from the Physical Schema v4 column comment and
is now recorded in the data dictionary for `DF-CAS-027` and in the decision log. The API
Specification v2 was updated with the optional `caseNo` query parameter on `GET /cases` before
implementation, as CLAR-001 required.

## 2. First-run findings and their disposition

| ID | Severity | Finding (short) | Disposition | Status |
|---|---|---|---|---|
| REVIEW-RWB-E1-018-001 | High | No primary-account rule for a grouped case. | Recorded as D-RCV-30 in the decision log and the data dictionary (DF-CAS-027); the spec carries the rule and the deterministic first-eligible-account clause in BR2/AC3 and the field matrix. | Resolved 2026-11-06 |
| REVIEW-RWB-E1-018-002 | Low | `caseNo` missing from API Specification v2. | The optional `caseNo` query parameter was added to `GET /cases` in API Specification v2 and its legacy conversion copy on 2026-11-06; no version bump, additive and backward compatible, as the spec stated. | Resolved 2026-11-06 |
| REVIEW-RWB-E1-018-003 | Low | Named Product Owner and FDA are TBC (GAP-006). | Recorded at the specification gate 2026-11-06: acting approver is the exercise owner; named approvers are entered in the increment card before the specification approval is signed (tracked under GAP-006, `docs/increments`). | Recorded 2026-11-06 |

## 3. Re-run checks

| Check | Result | Evidence |
|---|---|---|
| Authentication and authorization | Pass | Case read requires Case record R with scope; 403 MSG-P4-002; 404 MSG-P4-003; the job runs as SY-CASEWF. |
| Customer and account data protection | Pass | No personal data in logs, events or tests; cases are named by case number only. |
| Audit logging | Pass | Decision log entry D6 / CASE_CREATED is the last step before commit; a failure rolls the case back. |
| Approval controls | N/A | No approval decision in this story; exclusion rows and threshold are approved through RWB-E1-029 and RWB-E1-042. |
| Separation of duty | N/A | No approval action. |
| API contract | Pass | `EXISTING_API_CHANGE` delivered as specified: the optional `caseNo` query parameter is now in API Specification v2 with its legacy conversion; the two path endpoints match v2. |
| Error handling | Pass | MSG-P1-001, MSG-P7-003, MSG-P3-025, MSG-P4-002/003; refusal and retry paths specified. |
| Test coverage | Pass | Backend unit tests at 80%; 14 system, security, resilience and unit scenarios; frontend `NOT_APPLICABLE` with evidence. |
| Traceability | Pass | 10 BRs, 12 ACs and 9 exception paths mapped to SPEC-001..015; US-RWB-E1-018 linked. |
| Secrets and configuration | Pass | No secret; threshold, exclusion reasons, bands and status list are data. |
| Design evidence | Pass (not required) | `UI In Scope: NO`; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`. |
| No-assumption policy | Pass | `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`; the primary-account rule is a recorded decision with source and owner (D-RCV-30). |
| Operational readiness | Pass | Job record, SCR-02/03, metrics, alerts, feature flag and rollback specified. |

## 4. Recommendation

**Proceed to the Implementation Planner.** The primary-account rule is recorded with its source; the
API contract delta is in the OpenAPI file as required.

```text
REVIEW_STATUS: PASS
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0 open, 3 closed with disposition]
REVIEW_GATE: Specification gate
REVIEW_GATE_DECISION: Passed; ready for the Implementation Planner.
NEXT_STEP: Start the Implementation Planner on output/INC-040-epic-1-RWB-E1-018/specify/spec.md.
```
