# Compliance validation — RWB-E1-042 specification (v2)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-002` |
| Artifact | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` |
| Stage | Specification gate |
| Reviewer | Compliance Reviewer (agent run) |
| Date | 2026-11-16 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-001` (2026-11-04), kept in the archived spec run |
| Overall status | `PASS` |
| Blocking findings | 0 Critical, 0 High, 0 Medium |
| Warnings | 3 Low (carried, non-blocking) |

## 1. Scope of review

The specification was checked against:

- `.github/contexts/project-context.md` §4, §5, §11, §13–§15; `backend-context.md` §4, §9;
  `backend-standards.md` BS-2, BS-3; `testing-standards.md` §7.
- `.github/rules/requirement-standards.md`, `traceability-standards.md`,
  `specification-execution-gates.md`, `security-quality-standards.md`, `architectural-standards.md`,
  `pdlc.md`.
- The v7 story `RWB-E1-042`, the P3 FSD v4, the P3 TSD v3, API Specification v4, Physical Schema v6,
  the message standard v4 and the users, roles and permissions v4.
- Decision Log v10, D-RCV-28, D-RCV-35, D-RCV-36, the decision register and the increment card.

## 2. Findings

| ID | Severity | Area | Finding | Evidence | Disposition |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-042-001` | Low | Configuration | Two cache TTL keys with different defaults appear in the story. | Story §3, §13 | Both are catalog rows; the spec keeps them separate. Not blocking. |
| `REVIEW-RWB-E1-042-002` | Low | Approval | No role holds Reference data A in the permission matrix; the story assumes the owner and RW-RISK. | Story §3; DL01 | Load the grant through RWB-E1-037; approver named at the plan gate. Not blocking. |
| `REVIEW-RWB-E1-042-003` | Low | Approval | The per-story Product Owner / FDA signature is not a Jira comment. | Spec header; GAP-006 | Source-set approval 16 Nov 2026; plan gate records the name. Not blocking. |

No Critical, High or Medium finding. The v2 re-baseline introduces no new finding.

## 3. Checks performed

| Check | Result | Evidence |
|---|---|---|
| Change classification | PASS | `NEW_STORY`, UI NO, Logic YES, API YES / `NEW_API_REQUIRED`. |
| Requirement-to-SPEC coverage | PASS | 7 BRs and 11 ACs mapped; 0 `BLOCKED`; exception paths X1–X10 mapped. |
| Unique SPEC IDs | PASS | `SPEC-RWB-E1-042-001..012`, each defined once. |
| Story AC match | PASS | AC1, AC4–AC11 in the v7 story; the AC2/AC3 removal of 4 Nov 2026 is not re-opened. |
| Schema and migration | PASS | `${recoverySchema}`, `V0042__rwb_e1_042_parameter_catalog_and_seed.sql`, D-RCV-28. |
| D-RCV-35 impact | PASS | No inbound load, no source copy; parameter catalog is Workbench reference data. |
| D-RCV-36 impact | PASS | Six new parameters are catalog rows, not literals; no Temporal/Drools call in this story. |
| API contract | PASS | `GET /admin/parameters` and the `PARAMETER` reference-load handler; API Specification v4; no OpenAPI delta. |
| Authorization | PASS | Rules and parameters R (read), Reference data C (load), A (approve), U (rollback); 401/403/409/422 defined. |
| PDPA / data protection | PASS | No personal data field. `ace.db.password` is listed as a secret with no value. |
| Audit logging | PASS | Approval, rollback and value change write the decision log and the interaction ledger. |
| Secrets | PASS | `secret=true` rows never return `valueInForce`; value stays in the secret store. |
| Error contract | PASS | `MSG-P3-032`, `MSG-GEN-002`, `MSG-P1-002`, `MSG-P7-002`, `MSG-P3-015`, `MSG-P4-002`; exact wording. |
| Unit-test applicability | PASS | Backend YES / REQUIRED, 80% JaCoCo; frontend NO / NOT_APPLICABLE (no UI). |
| Test evidence | PASS | Migration pack `tests/test_migrations.sh` and `evidence/migration-test-output.txt` preserved. |
| Design evidence | N/A | `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` (UI NO). |
| Context conflicts | PASS | No conflict; D-RCV-47 is marked superseded in the decision register. |
| No-question rule | PASS | Four assumptions recorded; no question asked. |
| PII / secret scan | PASS | No personal data, credential or production data in the output. |

## 4. Preserved implementation validation

The 10 November 2026 pack is consistent with the v2 baseline:

- The SQL uses `${recoverySchema}` and schema `recovery`, not `ace` and not `rwb_`.
- The consolidated `V0042` file satisfies the D-RCV-28 one-file-per-story rule; the split
  `V042_1`/`V042_2` files are review copies and are not committed.
- The migration is guarded against the V0001 baseline (`CREATE TABLE IF NOT EXISTS`, `DO` blocks,
  `CREATE INDEX IF NOT EXISTS`).
- `spring.flyway.placeholders.recoverySchema=${RWB_SCHEMA}` is the correct property.
- The test output records the clean install, re-run, baseline overlap, negative cases and the
  deployment guard.
- `TC-E1-042-12` is `Blocked` (403 path arrives with E1-022/E1-037), not `Failed`; no mocked role.

## 5. Gate decision

`SPEC_GATE: PASS` — the specification is ready for the Implementation Planner. The three Low findings
are recorded and non-blocking. The implementation pack may be used as the build baseline; the plan
must not rewrite the SQL.

```text
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 18] [COVERED_RULES: 18] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new configuration capability]
```
