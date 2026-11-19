# Compliance validation — RWB-E1-032 specification (re-run)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-032-GATE-002` |
| Artifact | `output/INC-068-epic-1-RWB-E1-032/specify/spec.md` |
| Stage | Specification gate |
| Reviewer | Compliance Reviewer (agent re-run) |
| Date: first run | 2026-11-04 |
| Date: re-run | 2026-11-06 |
| Overall status | `PASS` |
| Blocking findings | 0 |
| Open findings | 0 |

## 1. Reason for the re-run

The first gate (2026-11-04, `FAIL`) was blocked by one High finding (CLAR-008): nothing defined how
a low-confidence document stored in `rwb-docs` moves to the write-once container after a person
confirms a legal type. Decision **D-RCV-31** (2026-11-06, solution architect with Compliance,
specification gate ruling) rules the mechanism: on confirmation of a write_once type, the confirm
step re-stores the file through the published `DocumentStorage.store` interface into
`rwb-docs-legal` at `{caseId}/{documentId}/v{docVersion}`, moves `storage_ref`, writes a DOCATT
audit entry naming the container, the confirmed type and the confirming user, and keeps the
standard-container object for evidence under the `rwb-docs` versioning policy; the write refuses
with MSG-GEN-006 when the immutability policy is absent. No blob is written except through
`DocumentStorage` (RWB-TE-012). The ruling is carried into spec BR4, the field matrix and the
type-confirmation behaviour.

## 2. First-run findings and their disposition

| ID | Severity | Finding (short) | Disposition | Status |
|---|---|---|---|---|
| REVIEW-RWB-E1-032-001 | Low | Story /contract endpoint names `/attach` and `/intake-items` vs `/resolve` and `/review-items`. | Recorded per API-P5-010 and API-P5-013 in the first-run spec (CLAR-001). | Resolved (2026-11-04) |
| REVIEW-RWB-E1-032-002 | Low | 032 and 054 define different shapes for the review queue endpoints. | One endpoint with `kind`/`reason`; `caseId` on resolve; recorded in CLAR-002/003 of the first run. | Resolved (2026-11-04) |
| REVIEW-RWB-E1-032-003 | Low | `CASE_NO_PATTERN`/`ACCOUNT_NO_PATTERN` assumed under DL21. | Adopted as go-live baseline data rows (`RW-[0-9]{4}-[0-9]{6}`, `[0-9]{10}`) loaded through the parameter catalog by the reference data administrator; DL21 owner confirmation is carried at the interface-inventory sign-off; the matcher reads them as data. | Recorded 2026-11-06 |
| REVIEW-RWB-E1-032-004 | Low | Product Owner approver is TBC (GAP-006). | Recorded at the specification gate 2026-11-06: acting approver is the exercise owner; the name is entered in the increment card before the approval signature (GAP-006 tracking). | Recorded 2026-11-06 |
| REVIEW-RWB-E1-032-005 | High | The move of a confirmed legal document to write-once storage is not defined (CLAR-008, CTL-12, NFR-029). | Ruled as D-RCV-31; the mechanism, audit entry, refusal path and test now carry in the spec (BR4, AC10, SPEC-RWB-E1-032-005). | Resolved 2026-11-06 |

## 3. Re-run checks

| Check | Result | Evidence |
|---|---|---|
| Authentication and authorization | Pass | Documents R for reads; Documents C with case scope for attach; items with no candidate only for scope ALL; 403 MSG-P4-002/MSG-P4-003. |
| Customer and account data protection | Pass | Account numbers and OCR text are never logged; field values masked by role; test accounts are synthetic; no production data. |
| Audit logging | Pass | DOCATT entry carries the classifier, confidence and match method before the document is stored, and, per D-RCV-31, the container, type and confirming user on the legal re-store; DocumentStored in the same transaction. |
| Write-once control (CTL-12, NFR-029) | Pass | The legal file is written only into `rwb-docs-legal` through the immutability-policed container; the re-store goes through `DocumentStorage.store`; overwrite and delete are refused and audited (AC2 and D-RCV-31). |
| Error handling | Pass | All five held outcomes, duplicate link, low-confidence store, concurrency and decision-log failure are specified; the missing-immutability-policy refusal now covers the re-store path. |
| Test coverage | Pass | Frontend and backend REQUIRED at 80%; 17 system, security and resilience scenarios; the legal re-store adds the confirm → re-store → overwrite-refused coverage. |
| Traceability | Pass | `REQ-DCM-007` mapped to SPEC IDs and TC-E1-032-01..17; no orphan. |
| Secrets and configuration | Pass | No secrets; patterns and threshold are parameters; no business value in code. |
| Design evidence | Pass | UI In Scope YES; SCR-31 and SCR-30 screen specifications and prototype cited; `DESIGN_EVIDENCE_STATUS: AVAILABLE`. |
| No-assumption policy | Pass | `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`; the storage mechanism is a recorded decision (D-RCV-31). |

## 4. Recommendation

**Proceed to the Implementation Planner.** The write-once control is now fully specified with its
audit evidence and test.

```text
REVIEW_STATUS: PASS
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0 open, 5 closed with disposition]
REVIEW_GATE: Specification gate
REVIEW_GATE_DECISION: Passed; ready for the Implementation Planner.
NEXT_STEP: Start the Implementation Planner on output/INC-068-epic-1-RWB-E1-032/specify/spec.md.
```
