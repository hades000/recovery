# Agent run log — RWB-E1-013 Baseline measures

| Field | Value |
|---|---|
| RUN_ID | `INC-042-epic-1-RWB-E1-013` |
| Story | RWB-E1-013 — Baseline measures |
| Agent role | Technical Specifier |
| Date | 2026-11-04 |
| Outcome | `BLOCKED` — CLAR-002 (AC7 business date) and CLAR-003 (median definitions) are open |

## 1. Sources read

| Source | Use |
|---|---|
| `output/SPEC-AUTHORING-GUIDE.md` | Required sections, status lines and no-invention rules. |
| `output/INC-043-epic-1-RWB-E1-020/specify/spec.md` | Structure only. |
| `docs/prds/recovery-workbench-fsd-p9-reporting-v2.md` | FSD P9 A2.1; AC-P9-001-01..06; roles and field catalog. |
| `requirement/legacy/05-technical-architecture/recovery-workbench-tsd-p9-reporting-v2.md` | T2/T3 `measure_definition`, `measure_snapshot`, `measure_publish`; T5 INT-19; T6 RBAC; T-A. |
| `requirement/legacy/04-user-stories/.../RWB E1 013 Baseline measures v1.md` | Primary story, ACs, rules, contract, tests, guardrails. |
| `requirement/legacy/04-user-stories/recovery-workbench-build-notes-epic-1-v4.md` (RWB-E1-013) | Implementation guidance for the six steps. |
| `requirement/legacy/04-user-stories/recovery-workbench-story-defects-epic-1-epic-2-and-enablers-v2-xlsx.md` | AC3/AC7 business-date defect. |
| `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` | `POST /admin/reference-loads`; `GET /admin/jobs`; `POST /admin/jobs/{jobId}/rerun`. |
| `requirement/legacy/06-data/recovery-workbench-logical-data-model-and-data-dictionary-v6-xlsx.md` | DF-RPT fields; `approved_by` is a UUID. |
| `requirement/legacy/06-data/recovery-workbench-physical-schema-v4.sql` | Table shapes; missing unique index and trigger. |
| `requirement/legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v3-docx.md` | MSG-GEN-001/006, MSG-P1-001, MSG-P4-002, MSG-P9-001/003. |
| `requirement/legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v3-xlsx.md` | RW-TRIBE, RW-REFADM, RW-BIANAL, RW-DATASTEW, RW-FINANCE, RW-PLATADM rights. |
| `requirement/legacy/07-screens-and-experience/recovery-workbench-screen-inventory-and-navigation-v2-xlsx.md` | SCR-44 first in E2. |
| `requirement/legacy/05-technical-architecture/recovery-workbench-batch-and-scheduling-design-v2-docx.md` | JOB-15 nightly 01:30. |
| `requirement/legacy/05-technical-architecture/recovery-workbench-interface-specifications-v2.md` | INT-19 hold and retry. |
| `.github/contexts/backend-context.md`, `testing-standards.md` | Module boundaries; 80% unit gate. |
| `output/INC-024-epic-1-RWB-E1-014/specify/spec.md`, `output/INC-023-epic-1-RWB-E1-056/specify/spec.md` | SCR-44 is E2; job rerun and monitor pattern. |

## 2. Work performed

1. Read the story, FSD A2.1, TSD T2/T3, the build notes, the defect register and the API spec.
2. Built the coverage table for 7 business rules, 8 acceptance criteria, 5 exception paths and the access path.
3. Classified the change: new nightly backend job and definition load; no UI; no API contract delta.
4. Found two behaviour-affecting gaps: the AC7 business-date contradiction (already in the defect register) and the undefined `TIME_IN_STAGE`/`TAT_BY_ROUTE` formulas; recorded CLAR-002 and CLAR-003 as open.
5. Specified the definition load, effective dating, six calculators, snapshot idempotency, baseline freeze and catch-up, INT-19 extract and hold/resend.
6. Wrote 10 system, security and unit scenarios, including the frozen trigger, module boundary and PDPA check.
7. Checked that no shared file was modified.

## 3. Decisions and assumptions

| ID | Decision / assumption | Basis |
|---|---|---|
| A-001 | JOB-15 processes the previous business date; AC7's 2026-11-28 fixture is inconsistent with the 2026-11-30 run. | Story flow, AC3, build notes; defect register. |
| A-002 | The baseline is caught up by the first good run after a failed load, in addition to the current date. | AC6; build notes step 3. |
| A-003 | JOB-15 writes no decision log entry; the P4 load record, frozen snapshot and job record are the audit trail. | Story §12; build notes; FSD generic step is boilerplate. |
| A-004 | `SY-DATALOAD` runs JOB-15 and the INT-19 write; the grant is confirmed under CLAR-006. | RWB-E1-007 outbound identity; TSD T6.2. |
| A-005 | The `measure_definition` load is in force from `valid_from` on success; the row-level approver is the control and the story specifies no separate P4 approve action. | AC1; story §3/§7; build notes step 2. |
| A-006 | The extract is one CSV per business date with a header and trailer, and includes the frozen baseline rows unchanged. | AC3; build notes step 8; INT-19. |
| A-007 | The `measure_snapshot` unique index uses `COALESCE` on the nullable dimension columns. | Story §13; TSD T3.1 nullable columns. |
| A-008 | `measure_publish` is not created in this story; it belongs to E2-009. | TSD T3; story solution plan (two tables). |

## 4. Open items

| CLAR | Question | Why it blocks |
|---|---|---|
| CLAR-002 | Which business date does the 2026-11-30 01:30 run process? AC7 says 2026-11-28, which is a Saturday and not the previous business date. | The AC7 fixture and the baseline catch-up cannot be tested unambiguously. |
| CLAR-003 | What is the approved formula and population for `TIME_IN_STAGE` and `TAT_BY_ROUTE`? | Two of the six published measures cannot be implemented or tested without inventing the definition. |

## 5. Status

```text
RUN_STATUS: BLOCKED
COVERAGE: 7 BR / 8 AC / 5 X + access mapped; 0 missing
CLARIFICATIONS: 2 open, 6 resolved
NEXT_STEP: Business analyst to rule CLAR-002 (AC7 business date) and CLAR-003 (median definitions), then re-run the Technical Specifier.
```
