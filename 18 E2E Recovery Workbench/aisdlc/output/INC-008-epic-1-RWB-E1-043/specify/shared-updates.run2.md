# Shared updates requested: RWB-E1-043 specify (INC-008-epic-1-RWB-E1-043)

Revision 2, 2026-11-18 (remediation run 1; revision 1 kept as `shared-updates.run1.md`). The Technical
Specifier does not edit shared files (RUN-BRIEF). The orchestrator applies these rows in order.

## 1. `aisdlc/requirement/Traceability_Matrix.md`

Replace the INC-008 row in the increment trace:

| 008 | `RWB-E1-043` | `BR-RWB-011` | `FR-RWB-011` (REQ-DRI-011, REQ-CWC-006; R-UNI-38, CTL-08, REQ-CWC-016) | `output/INC-008-epic-1-RWB-E1-043/specify/spec.md` (revision 2, 18 Nov 2026) | Specified — remediation run 1; spec gate see `review/spec-gate-review-2.md`; plan not started |

SPEC trace (CTX `CTX-BACKEND-RWB-V2`, `CTX-PROJECT-RWB-V2` CTX-FEAT-012; US `RWB-E1-043`; TASK and later
columns empty). REQ-CWC-006 has no canonical FR in REQ-RWB-002 §12; it is traced to FR-RWB-011 by
content (GAP-29).

| SPEC ID | FR/NFR | Story refs |
|---|---|---|
| SPEC-RWB-E1-043-001 | FR-RWB-011, NFR-RWB-010 | §13 Database, BR2, §17 |
| SPEC-RWB-E1-043-002 | FR-RWB-011 | BR1, §11 DF-REF-028/029 |
| SPEC-RWB-E1-043-003 | FR-RWB-011 | BR5, X2, AC4, §13 step 2 |
| SPEC-RWB-E1-043-004 | FR-RWB-011 | X7, AC10 |
| SPEC-RWB-E1-043-005 | FR-RWB-011 | BR6 (R-UNI-38), X3, AC6 |
| SPEC-RWB-E1-043-006 | FR-RWB-011 | X4, AC7, §12 idempotency |
| SPEC-RWB-E1-043-007 | FR-RWB-011 | BR2, AC1 |
| SPEC-RWB-E1-043-008 | FR-RWB-011, NFR-RWB-005 | BR4 (CTL-08), X1, AC2, AC5, §12 approve |
| SPEC-RWB-E1-043-009 | FR-RWB-011 | X5, AC8 |
| SPEC-RWB-E1-043-010 | FR-RWB-011 | BR8, AC1 |
| SPEC-RWB-E1-043-011 | FR-RWB-011 | BR3 (R-UNI-38), AC1, AC5, §9 |
| SPEC-RWB-E1-043-012 | FR-RWB-011, NFR-RWB-008 | BR9, X6, AC9 |
| SPEC-RWB-E1-043-013 | FR-RWB-011 | §13 cache, §17 |
| SPEC-RWB-E1-043-014 | FR-RWB-011, NFR-RWB-006, NFR-RWB-008 | BR7 (REQ-CWC-016), AC3 |
| SPEC-RWB-E1-043-015 | FR-RWB-011, NFR-RWB-005 | §12 load, TC-E1-043-11 |
| SPEC-RWB-E1-043-016 | FR-RWB-011, NFR-RWB-005 | §10, §12 approve |
| SPEC-RWB-E1-043-017 | FR-RWB-011 | §3 business date |
| SPEC-RWB-E1-043-018 | NFR-RWB-009 | §13 feature flag |
| SPEC-RWB-E1-043-019 | FR-RWB-011 | §13 done-when, §17 |
| SPEC-RWB-E1-043-020 | FR-RWB-011 | §14 |
| SPEC-RWB-E1-043-021 | FR-RWB-011 | BR1, §17 |
| SPEC-RWB-E1-043-022 | FR-RWB-011 | §13 done-when |
| SPEC-RWB-E1-043-023 | NFR-RWB-006 | §17 |
| SPEC-RWB-E1-043-024 | FR-RWB-011, NFR-RWB-005 | §9 rollback |
| SPEC-RWB-E1-043-025 | FR-RWB-011 (REQ-CWC-006) | §13 step 7; D-RUN-11 |
| SPEC-RWB-E1-043-026 | FR-RWB-011 | §13 step 7; D-RUN-10 |
| SPEC-RWB-E1-043-027 | NFR-RWB-005 | §10 |
| SPEC-RWB-E1-043-028 | FR-RWB-012, NFR-RWB-005, NFR-RWB-008 | TC-E1-043-11 |
| SPEC-RWB-E1-043-029 | FR-RWB-011 | §13 step 2 |
| SPEC-RWB-E1-043-030 | FR-RWB-011 | §13 step 7; D-RUN-10, D-RUN-11 |
| SPEC-RWB-E1-043-031 | FR-RWB-011, NFR-RWB-006 | DL10 D-RCV-29 |

## 2. `aisdlc/docs/increments/INDEX.md`

Row 008: status `Specified (revision 2)`, result per `review/spec-gate-review-2.md`.

## 3. `aisdlc/docs/open-items.md`

- OPEN-036: E1-043 half — spec revision 2 on 2026-11-18; plan still historical. Keep open until the plan
  is re-baselined.
- Close or replace revision 1's rows "Name the handler interface" (settled by D-RUN-11) and "Name the
  owner of reference-table rollback" (built here, D-RUN-10).
- New items (IDs assigned by the orchestrator). Owners are roles; nothing here names a person.

| Item | Story | Owner | Needed by | Source |
|---|---|---|---|---|
| **RWB-E1-001 (required action, gate finding 108).** V0001 must not create `reference_version` or `reference_row` with plain `CREATE TABLE`, and must not create `uk_reference_row UNIQUE (row_key)`. Either leave both tables to RWB-E1-043, or create them with `CREATE TABLE IF NOT EXISTS` and no unique key on `row_key` alone; `UNIQUE (version_id, row_key)` is RWB-E1-043's. Its data-dictionary rows and conformance tests must expect the per-version key. RWB-E1-043 merges first (BS6 orders 8, 9); numbers at merge (D-RUN-07); DL10's "V0001" for E1-001 is a recorded gap (GAP-15) | RWB-E1-001 | RWB-E1-001 owner | RWB-E1-001 plan | Physical Schema v6 lines 8, 1437, 1471-1483; S7 §13; DL10 D-RCV-28; GAP-01, GAP-25 |
| RWB-E1-001 registers `data_product` as a `ReferenceTableHandler` bean (package `recovery.casewf.refdata.api`, not P4; GAP-36) and adds its catalog rows `refdata.columns.data_product`, `rwb.refload.loader.data_product`, `rwb.refload.approver.data_product` (its approver: E1-001 CLAR-009). Its gate finding 003 is answered by D-RUN-11 | RWB-E1-001 | RWB-E1-001 owner | RWB-E1-001 plan | D-RUN-11; SPEC-025, 029 |
| RWB-E1-001 registers the data-dictionary handler for `sys_objects`/`sys_fields` (DL10 D-RCV-29), uses `changeSummary` to report `is_personal` changes by field ID, and sets `rwb.refload.approver.<dictionary code>` = `RW-COMPLY` | RWB-E1-001 | RWB-E1-001 owner with RW-COMPLY | RWB-E1-001 plan | SPEC-031; A-36; GAP-37 |
| Decide whether removing an `is_personal` mark needs an approval beyond the dictionary approver list (none is defined in Personal Data Protection Design v2, the inventory v4 or DL26) | RWB-E1-001, RWB-TE-011 | RW-COMPLY with the data architect | Before the first dictionary load | SPEC-031; orchestrator input 2026-11-18 |
| RWB-TE-011's lint reads the loaded dictionary versions as well as the schema seed | RWB-TE-011 | RWB-TE-011 owner | Before the first dictionary load | S7 TE-011 §12; GAP-38 |
| RWB-E1-019 implements `ReferenceTableHandler` for QUEUE and QUEUE_MEMBER: `ReferenceTableCheck` becomes `validate`; `QueueVersionApplier` becomes `apply` and `onRolledBack` (`supportsRollback = true`); its build step 5 (rollback endpoint) is replaced by RWB-E1-043's endpoint; it sets `rwb.refload.approver.queue` (RW-TEAMMGR per its flow step 4) and adds the QUEUE_MEMBER keys | RWB-E1-019 | RWB-E1-019 owner | RWB-E1-019 specify | G-R01, G-R02; SPEC-024, 025 |
| RWB-E1-042: (a) confirm the names of revision 3 at its gate; (b) add a by-name lookup to generated `ParameterKeys` (A-26); (c) consider aligning repeat approve/rollback with RWB-E1-043 §12 (200 same body) on the shared endpoint (GAP-35); (d) note that RWB-E1-043 adds Reference data rows to the interim grants file and 38 catalog rows | RWB-E1-042 | RWB-E1-042 owner | RWB-E1-042 gate | D-RUN-10; SPEC-026, 027, 029 |
| Load Reference data A for the approver roles (RW-RISK; RW-COE for PARAMETER; RW-TEAMMGR for QUEUE; RW-SECADM, RW-COMPLY per RWB-E1-037) in the permission matrix and replace the interim grants | RWB-E1-037 | Risk / access owner | Before RWB-E1-043 SIT exit | GAP-14, GAP-22; A-08 |
| Accept the default loader and approver lists, and name RW-COE's tables if any | RWB-E1-043 | Access owner; Risk | Plan gate | A-31; GAP-19 |
| Person-level separation of duty (RW-REFADM vs RW-RISK) in the role assignment check | RWB-E1-022 | E1-022 owner | RWB-E1-022 | S7 §10; S7-022 SOD-2026.11 |
| Replace `LoggingReferenceLoadAudit` with the access log (AC-DENY on 403) | RWB-E1-039 | E1-039 owner | RWB-E1-039 | SPEC-028; GAP-26 |
| Implement `VersionDecisionRecorder` for reference-table approvals (AC-VERS) | RWB-E1-027 | E1-027 owner | RWB-E1-027 | GAP-07 |
| Replace RWB-E1-042's interim `BusinessDateProvider` with the `v_ace_batch_status` rule (latest complete date) | Story reading the view after RWB-E1-069 | Tech lead; ACE batch owner | Before SIT | A-01; GAP-12 |
| Engines read through `ReferenceDataReaders.forReader("<component>")` at start and expiry, stop on `NoVersionInForceException`, and record the version used with each decision (BR6) | RWB-E1-018, -020, -028; RWB-E1-072 (SY-RULES) | Those owners | Their specify | A-02; S7 §10 |
| Name the owner of `GET /admin/lists/{listCode}` and the RW-AUDIT read of versions | RWB-E1-043 / BA | BA | Before RWB-E1-025 | GAP-34 |
| List the reference load result in the daily data quality report | RWB-E1-011 | E1-011 owner | RWB-E1-011 | GAP-33 |
| Supply the column definition values for each of the 12 tables (A-34 grammar, ≤ 400 characters) | owning stories (E1-019, E1-025, E1-038, E1-045, E1-046, ...) | Table owners | Before SIT loads of version 1 | GAP-13, GAP-30 |
| Correct the LOV-REF-TABLE seed (remove ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER, HOLIDAY) | RWB-E1-001 | Data owner | RWB-E1-001 V0001 | GAP-04 |
| MSG-P4-003 wording for an unknown load; 400 vs 422 in REQ §10 | Message / API owners | BA | Next document set | GAP-27, GAP-28 |
| Owner acceptance of A-01, A-08, A-09, A-16, A-17, A-27, A-31, A-33, A-34 | RWB-E1-043 | BA, Risk, tech lead, access owner | Plan gate | Gate finding 116 |
| Plan gate decision on the multi-module scope (P3, P4, platform) | RWB-E1-043 | Tech lead / analyst | Plan gate | AGENTS §7; gate finding 118 |
| Assign `<seq>` for `V<seq>__rwb_e1_043_reference_versions.sql` before RWB-E1-001's file | RWB-E1-043 | Orchestrator | Merge | D-RUN-07; GAP-15 |

## 4. `aisdlc/DOCUMENT-GAPS.md`

Candidate rows GAP-01 to GAP-38 are in `specify/document-gaps.md` (no blocker for this story). Number
them `DG-nnn` with "Raised by: INC-008 specify GAP-xx"; GAP-20 to GAP-29 also carry "spec gate review 1
G-R01..G-R10". GAP-24 (G-R05) is Blocker = No under D-RUN-10 and D-RUN-11.
