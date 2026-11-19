# Shared updates requested: RWB-E1-043 specify (INC-008-epic-1-RWB-E1-043)

The Technical Specifier does not edit shared files (RUN-BRIEF rule 3). The orchestrator applies these
rows in order. Date 2026-11-17.

## 1. `aisdlc/requirement/Traceability_Matrix.md`

Replace the INC-008 row in the increment trace:

| 008 | `RWB-E1-043` | `BR-RWB-011` | `FR-RWB-011` | `output/INC-008-epic-1-RWB-E1-043/specify/spec.md` (current 17 Nov 2026); `plan/plan.md` historical | Specified — spec re-baselined to schema `recovery`, D-RCV-35/36; spec gate see `review/spec-gate-review.md`; plan not started |

Add the SPEC trace (CTX `CTX-BACKEND-RWB-V2`, `CTX-PROJECT-RWB-V2` CTX-FEAT-012; US `RWB-E1-043`; TASK and later columns empty):

| SPEC ID | FR/NFR | Story refs |
|---|---|---|
| SPEC-RWB-E1-043-001 | FR-RWB-011 | §13 Database, BR2, §17 |
| SPEC-RWB-E1-043-002 | FR-RWB-011 | BR1, §11 DF-REF-028/029 |
| SPEC-RWB-E1-043-003 | FR-RWB-011 | BR5, X2, AC4, §13 step 2 |
| SPEC-RWB-E1-043-004 | FR-RWB-011 | X7, AC10 |
| SPEC-RWB-E1-043-005 | FR-RWB-011 | BR6, X3, AC6 |
| SPEC-RWB-E1-043-006 | FR-RWB-011 | X4, AC7, §12 idempotency |
| SPEC-RWB-E1-043-007 | FR-RWB-011 | BR2, flow 3–4, AC1 |
| SPEC-RWB-E1-043-008 | FR-RWB-011, NFR-RWB-005 | BR4, X1, AC2, AC5, §12 approve |
| SPEC-RWB-E1-043-009 | FR-RWB-011 | X5, AC8 |
| SPEC-RWB-E1-043-010 | FR-RWB-011 | BR8, AC1 |
| SPEC-RWB-E1-043-011 | FR-RWB-011 | BR3, AC1, AC5, §9 |
| SPEC-RWB-E1-043-012 | FR-RWB-011, NFR-RWB-008 | BR9, X6, AC9 |
| SPEC-RWB-E1-043-013 | FR-RWB-011 | §13 cache, §17 |
| SPEC-RWB-E1-043-014 | FR-RWB-011, NFR-RWB-006, NFR-RWB-008 | BR7, AC3 |
| SPEC-RWB-E1-043-015 | FR-RWB-011, NFR-RWB-005 | §12 load, TC-E1-043-11 |
| SPEC-RWB-E1-043-016 | FR-RWB-011, NFR-RWB-005 | §10, §12 approve |
| SPEC-RWB-E1-043-017 | FR-RWB-011 | §3 business date |
| SPEC-RWB-E1-043-018 | NFR-RWB-009 | §13 feature flag |
| SPEC-RWB-E1-043-019 | FR-RWB-011 | §13 done-when, §17 |
| SPEC-RWB-E1-043-020 | FR-RWB-011 | §14 |
| SPEC-RWB-E1-043-021 | FR-RWB-011 | BR1, §12, §17 |
| SPEC-RWB-E1-043-022 | FR-RWB-011 | §13 done-when |
| SPEC-RWB-E1-043-023 | NFR-RWB-006 | §17 |

## 2. `aisdlc/docs/increments/INDEX.md`

Row 008: status `Specified`, result per the spec gate (`review/spec-gate-review.md`).

## 3. `aisdlc/docs/open-items.md`

- OPEN-036: E1-043 half — spec re-baselined to schema `recovery` on 2026-11-17 (`specify/spec.md`); plan still historical. Keep open until the plan is re-baselined.
- New items (IDs assigned by the orchestrator):

| Item | Story | Owner | Needed by | Source |
|---|---|---|---|---|
| Name the handler interface for table codes other modules own (PARAMETER, P5 codes, `data_product`, TEMPLATE) — E1-001, E1-013, E1-016/017, E1-025, E1-040/041, E1-046 expect one "from RWB-E1-043" under 4 names | RWB-E1-043, RWB-E1-001 | BA / solution architect | Before RWB-E1-001 specify | GAP-08 |
| Name the owner and behaviour of reference-table rollback (`/rollback`, ROLLED_BACK) and verify | RWB-E1-043, RWB-E1-019, RWB-E1-042 | BA | Before RWB-E1-019 | GAP-10, GAP-11 |
| Grant Reference data A to the approver role (S7 §10 assumes RW-RISK) | RWB-E1-037 | Risk / access owner | Before RWB-E1-043 SIT exit | GAP-14 |
| Correct the LOV-REF-TABLE seed (remove ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER, HOLIDAY) | RWB-E1-001 | Data owner | RWB-E1-001 V0001 | GAP-04 |
| Supply column definitions for each of the 12 reference tables | owning stories (E1-019, E1-025, E1-038, E1-045, E1-046, ...) | BA / table owners | Before SIT loads of version 1 | GAP-13 |
| Confirm the single business-date rule over `v_ace_batch_status` | RWB-E1-043 | ACE batch owner | Plan gate | GAP-12, A-01 |
| Add the AC-VERS decision log entry on approval once the writer exists | RWB-E1-027 | E1-027 owner | RWB-E1-027 | GAP-07 |
| Engine stories call `ReferenceDataService.rows` at start and stop on `NoVersionInForceException` | RWB-E1-018, -020, -028 | Those owners | Their specify | A-02 |
| Assign `<seq>` for `V<seq>__rwb_e1_043_reference_versions.sql` and confirm order against RWB-E1-001 V0001 | RWB-E1-043 | Orchestrator / tech lead | Merge | GAP-02, GAP-15 |

## 4. `aisdlc/DOCUMENT-GAPS.md`

Candidate rows GAP-01 to GAP-19 are in `specify/document-gaps.md` (no blockers for this story; GAP-08
likely blocks RWB-E1-001). Number them `DG-nnn` with "Raised by: INC-008 specify GAP-xx".
