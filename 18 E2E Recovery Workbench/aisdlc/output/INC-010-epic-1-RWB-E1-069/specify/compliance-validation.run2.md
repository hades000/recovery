# Compliance validation (self-check): INC-010-epic-1-RWB-E1-069, run 2

This is the Technical Specifier's own check of the run-2 spec against `.github/rules/specification-execution-gates.md`, run on 2026-11-18. Run 1's self-check is kept as `compliance-validation.run1.md`; the round-1 gate overturned its rows 3, 6 and 9. The independent gates are `../review/spec-gate-review.md` (round 1, FAIL) and `../review/spec-gate-review-2.md` (round 2).

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Required sections present: Change Scope Declaration, Requirement-to-SPEC Logic Coverage, intent, trigger and preconditions, field matrix, status-transition matrix, exceptional cases, API assessment, Frontend Specification, Unit Test Applicability, Clarification Log, Status lines; plus Out of scope and Data protection | PASS | `spec.md` headings (unnumbered, as the gate rule names them) |
| 2 | Change classification backed by requirement, trace chain and code footprint | PASS | Matrix §3 row 010; no v_ace migration or `sourceViews` in code; [S1] §12, §15 |
| 3 | Every AC clause, BR and story rule maps to a SPEC item **and a test** | PASS | 42 rows (31 AC clauses, 9 BR, §4 step 2, §17); each row names a TC or T ID (REVIEW-109) |
| 4 | Coverage Type and Status values are from the allowed sets | PASS | `DIRECT` / `INHERITED_EXISTING_BEHAVIOR`; `COVERED` |
| 5 | SPEC IDs unique | PASS | SPEC-RWB-E1-069-001..020; none in the matrix today |
| 6 | API impact explicit | PASS | `NO_API_CHANGE`; non-HTTP contracts in `contracts/backend-apis.json` |
| 7 | Unit-test gate: 80% for lines, statements, branches and functions | PASS | LINE, INSTRUCTION, BRANCH, METHOD at 80%, the [T1] SPEC-020 counters, over recovery main plus the tooling packages that hold the new logic (REVIEW-104) |
| 8 | Design evidence | PASS | `NOT_REQUIRED`; `figma/figma_report.md` |
| 9 | No invented requirement; derived items and rulings labelled | PASS | Derived: X8–X11, the BND-6 fallback message, the transient CREATE, the per-view REVOKE, the `RWB_CONFORMANCE_TARGET` switch. Rulings as assumptions with open items: ASM-012 (helper body), ASM-013 (A-02 rulings), ASM-015 (ACE-side grants) |
| 10 | Internal consistency of the grant design | PASS | Both files run the full owner sequence (SPEC-004 steps 5–9; SPEC-006). ACE-side grants are P4(d), supplied locally by SPEC-015(b). Each privilege step was verified on PostgreSQL 16.16 ([E2]) |
| 11 | Banking controls: personal-data classification and controls for the published interface | PASS | SPEC-019: [S16] classification (250 personal, 12 Restricted named), control set and owners per [S9] §3.3 and §12 R5, definer-rights trade-off, tests. Out of scope names RWB-E1-037 and RWB-E1-016. No personal data in any artefact; values are synthetic |
| 12 | Conflicts recorded with two citations and resolved by precedence | PASS | DG-L01..L28, no blocker; the BR6 conflict is DG-L23, the E1-001 hand-over DG-L27 |
| 13 | Migration numbers not fixed (D-RUN-07) | PASS | "Section A file" / "Section B file"; `V<seq>`; versions read from file names at test time. V0002/V0003 appear only when quoting [S1] or [T2] |
| 14 | Dependencies only on existing code or earlier stories (D-RUN-08) | PASS | RWB-E1-044 (1), RWB-TE-001 (2), RWB-E1-001 (9); later work named as out of scope |
| 15 | Shared files not edited | PASS | Proposed rows in `shared-updates.md` |
| 16 | Baseline not duplicated (A-04) | PASS | Extends `RecoveryBoundaryTest`, the [T3] lint, `RecoveryDatabaseIT`; `RecoveryFlywayConfig` unchanged |
| 17 | Traceability rows consistent with the spec, including NFRs | PASS | `shared-updates.md` §1 uses the matrix's §3 columns and the spec's TC table; NFR mapping in `spec.md` |

Result of the self-check: PASS. The independent round-2 gate decides the handoff.
