# Compliance validation (self-check): INC-010-epic-1-RWB-E1-069

This is the Technical Specifier's own check of its work against `.github/rules/specification-execution-gates.md`, run on 2026-11-17. The independent spec gate is recorded separately in `../review/spec-gate-review.md`.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | `spec.md` holds every required section: Change Scope Declaration, Requirement-to-SPEC Logic Coverage, intent, trigger and preconditions, field matrix, status-transition matrix, exceptional cases, API assessment, Unit Test Applicability | PASS | `spec.md` headings |
| 2 | The change classification is backed by three inputs: the requirement, the trace chain and the code footprint | PASS | Trace matrix row 010 says "No current spec/plan". The code has no v_ace migration and no `sourceViews` key. The story §12 and §15 say there is no API and no screen. |
| 3 | Every AC (8) and BR (9) maps to at least one SPEC item | PASS | Coverage table: 20 rows, all COVERED |
| 4 | SPEC IDs are unique | PASS | The trace matrix holds no `SPEC-RWB-E1-069-*` today. This run adds 001..016. |
| 5 | The API impact is explicit | PASS | `NO_API_CHANGE`. `contracts/backend-apis.json` lists the non-HTTP contracts. |
| 6 | Frontend and backend unit-test applicability agree with the scope | PASS | Frontend NO, NOT_APPLICABLE. Backend YES, REQUIRED, with an 80% gate on lines and branches. |
| 7 | Design evidence | PASS | `NOT_REQUIRED`; `figma/figma_report.md` |
| 8 | No invented requirement | PASS, with labels | Derived items are labelled as such and none is presented as a story requirement: X8 and X9, the A-02 decisions, ASM-002, -003 and -009, the transient CREATE grant and the per-view REVOKE. |
| 9 | Banking controls | PASS | No personal data. Synthetic keys `ACC0000017` and `P0000123` come from the story. `v_ace_customer` exposes only `id_no_masked` and `id_no_last4`. The read boundary is enforced in the catalog and in the build. |
| 10 | Conflicts are recorded with two citations and resolved by precedence | PASS | `document-gaps.md`: DG-L01..L21, no blocker |
| 11 | Shared files are not edited | PASS | All proposed rows are in `shared-updates.md` |
| 12 | Baseline is not duplicated (A-04) | PASS | SPEC-012 and SPEC-014 extend `RecoveryBoundaryTest` and `RecoveryMigrationLintTest`, and SPEC-015 extends `RecoveryDatabaseIT`. `RecoveryFlywayConfig` is not changed. |
| 13 | Traceability rows | PROPOSED | They are in `shared-updates.md` §1. The Traceability Manager or the orchestrator applies them. |

Result of the self-check: PASS.

**The independent spec gate returned FAIL** (`../review/spec-gate-review.md`). It raised 3 High, 6 Medium and 7 Low findings. Two of them overturn rows of this self-check:
- Finding 101 means BR6 is not covered when the verbatim helper is used.
- Finding 109 means row 3 ("20 of 20 COVERED") is overstated.

The handoff is blocked until a human remediates the findings and the gate is re-run, or a human explicitly accepts them.
