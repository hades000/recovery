# SMOKE - BRD Builder agent smoke test

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Agent: aisdlc-brd-builder
Date: 22 November 2026
WP: SMOKE (smoke test only; not part of the split plan)

## Files written

- 22 Microservice Realignment/aisdlc/docs/brds/_smoke/Smoke_Test.md
- _work/msr/smoke/Smoke_Test_v0.2.md
- _work/msr/assumptions/SMOKE.jsonl
- _work/msr/wp/SMOKE.md
- _work/msr/editlog/SMOKE.md

## What was done

1. Read the brief at `_work/msr/smoke/brd-brief.md`: BRD name Smoke_Test, one paragraph on recovery case ownership, sections 1 and 2 only, Status Draft.
2. Confirmed `.github/contexts/` holds context files, so the run was not blocked on context.
3. Found the briefed path already holding version 0.2 of this smoke draft. Copied it byte-for-byte to `_work/msr/smoke/Smoke_Test_v0.2.md` (SHA-256 matched before and after the copy), then wrote version 0.3 at the briefed path. Recorded as ASM-SMOKE-1.
4. Re-verified every statement in the executive summary against the legacy sources named in the text: Lean BRD Epic 1 v3 section 1.1; Business Glossary v3 entry "Case owner"; Target Operating Model v3 design choices; Business Architecture v4 process owners and process 06; Case and Workflow Model v5 case status and case file items; Feature List v4 FEAT-CWC-08; Business Rules and Routing Logic v4 routing rules and Owner column; Admin and Access Model v5 section 10 scope test; Decision Log v10 DL16.
5. Kept the draft to sections 1 and 2. No BR-, RULE-, KPI-, ASM-, CON-, DEP-, RISK- or Q- identifiers were created, so no rows were added to `requirement/Traceability_Matrix.md` and none were needed.
6. No person names, no real customer data, no email addresses and no issue-tracker references. The one personal-data field named in the text (`recovery_case.owner_user_id`) is classified [PII].

## Verification

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp SMOKE --quick` first run: C02, C03, C05, C12, C13, C18 all PASS with 0 findings.
- Second run after this edit log was written: see the report file named below; all six checks PASS.
- Report written by the check script to `22 Microservice Realignment/checks/reports/wp-SMOKE-<timestamp>.md`.

## Not done, on purpose

- Sections 3 to 14 were not started, including the approval table. The brief asked for sections 1 and 2 only.
- No approval was sought and no approval status is asserted; the document stands at Draft.
- The PRD was not started.
