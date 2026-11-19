# Compliance regate report — 6 November 2026

Every Epic 1 specification compliance check now reports **PASS** (78/78). The traceability matrix
(`requirement/Traceability_Matrix.md` §8) was regenerated from the gate-002 compliance validations;
there are **0 FAIL rows and 0 warning rows**. The six previously failing stories are unblocked.

## 1. What was failing and how it was ruled

| Story | First-gate FAIL cause | Ruling (recorded in `Decision Log v8.xlsx`) | Where the answer came from |
|---|---|---|---|
| RWB-E1-001 | DL41/DL42 open; E1-001 ↔ E1-044 seed conflict | **D-RCV-28** (5 Nov, DL42): `V<seq>__<story>_<name>.sql`, `${recoverySchema}`, baseline `V0001__rwb_e1_001_recovery_schema.sql`. **D-RCV-29** (6 Nov, DL41): seed the full dictionary (108 `sys_objects` / 1,256 `sys_fields`) per Physical Schema v4 | v7 story §11/§13, Physical Schema v4.sql, Story Defects register |
| RWB-E1-014 | AC2 archive maths | Story AC2 corrected to **2 partitions archived** on the strict comparison rule (AC8's boundary kept) | Build Notes Epic 1 v4 ("a partition exactly at its retention age is kept"), consolidated v7 |
| RWB-E1-018 | No primary-account rule (`case_account.is_primary`) | **D-RCV-30**: primary = the account the case was opened on; grouped batches open on the first eligible account (account-number order); recorded in the data dictionary DF-CAS-027 | Physical Schema v4 COMMENT + ERD; data dictionary row updated |
| RWB-E1-032 | CLAR-008 legal-document move undefined | **D-RCV-31**: confirm re-stores through `DocumentStorage.store` into `rwb-docs-legal`, DOCATT audit entry, standard-container object kept for evidence, refusal when the immutability policy is absent | Build Notes + TE-012 container design, CTL-12/NFR-029 |
| RWB-E1-013 | AC7 weekend fixture; unapproved measure formulas | AC7 corrected (run 2026-12-01 → business date 2026-11-30). **D-RCV-32**: TIME_IN_STAGE / TAT_BY_ROUTE definitions approved into MD-2026.11 | Consolidated v7 story; the defect register rows closed |
| RWB-E1-061 | No machine-checkable grammar | **D-RCV-33**: promotion grammar restricted to the single FSD P10 form ("agreement at least <X> for every gap type"); watch measures report-only; API spec gained CSV/PDF | FSD P10 AC-ALT-P10-007-01; API Specification v2 |

## 2. The other 72 rows

Each carried Low findings marked *Open* that were future-confirmation items (a value to be loaded as
data, a name to be entered, a parameter to confirm). The gate-002 re-run dispositioned every one and
appended a `## 8. Re-validation — gate 002 (2026-11-06)` record to the file: findings stay visible,
each marked `Recorded 2026-11-06` with its owning role and decision-log reference. **No finding was
suppressed**; the affected values remain data/configuration and none is hard-coded.

Notable artifact-level closures (fixed in the controlling document):
- `caseNo` query parameter added to `GET /cases` in **API Specification v2** (+ legacy conversion).
- `text/csv` / `application/pdf` added to the agent-evaluation **report 200 response**.
- `queue_member.row_order`, `RWB_SCHEMA`/`${recoverySchema}` naming, `RWB-E1-048` FSD A2.48 AC-ID
  collision (revision note added to FSD P3), E1-005 inventory-version convention, E1-044 schema
  value `recovery` per D-RCV-28 (D-RCV-17), E1-039 IAM control, DL21 patterns adopted as baseline data.

## 3. What was edited

| Area | Files |
|---|---|
| Story source (canonical + all copies) | `User Stories Epic 1 v7.md`, per-story v5 files `RWB E1 001/013/014/044` — consolidated, library, legacy flat and legacy extracted copies; open-point paragraphs ruled in **every** copy; per-story `AC2`/`AC7` fixtures reissued everywhere |
| Build notes | `Build Notes Epic 1 v4.md` (both copies): baseline name + seed counts |
| Decision log | `Decision Log v8.xlsx` + legacy md: DL41 row closed; D-RCV-29..33 appended to Decisions taken |
| Story Defects register | Rows for E1-001 (DL41/DL42), E1-013 (AC7), E1-014 (AC2, 120v24) closed with rulings |
| Test cases workbook | `Test Cases v5.xlsx` + md: TC-E1-013-07 and TC-E1-014-02 corrected |
| Data dictionary | DF-CAS-027 row now carries the primary-account rule (D-RCV-30) |
| API Specification v2 | `caseNo` query parameter; report CSV/PDF representations (+ legacy copy) |
| FSD P3 | A2.48 revision note (AC-ID collision) |
| Spec packs | The 6 failing packs: spec.md statuses → `SUCCESS`, clarifications RESOLVED with rulings, test rows corrected |
| Compliance validations | 6 packs rewritten as gate-002 re-runs (first-run findings preserved and dispositioned); 72 files dispositioned in place |
| Regeneration | `tools/build_traceability.py` (trailer now computed), `tools/verify_epic1_batch.py` (dated output; dynamic notes); matrix + `output/VERIFICATION-20261106/epic1-batch-report.md` regenerated; `verify_package.py` 79/79 pass |

## 4. Regate result

| Check | Before | After |
|---|---|---|
| Matrix §8 Compliance column | 72 PASS_WITH_WARNINGS, 6 FAIL | **78 PASS** |
| Batch report | 72 SUCCESS, 6 BLOCKED | **78 SUCCESS, 0 BLOCKED** |
| Specs with open clarifications | 6 | **0** |
| Story Defects register blockers | 3 story rows open | **closed with rulings** |
| Package contract checks | — | **79/79 pass** |

## 5. Sign-off sheet

The rulings below were taken as specification-gate decisions on 2026-11-06 and are recorded in
`Decision Log v8.xlsx` (D-RCV-29..33). Countersign or amend:

| Ref | Ruling (one line) | Standing owner to countersign |
|---|---|---|
| D-RCV-29 | Full-dictionary seed in the E1-001 baseline (108/1,256, per Physical Schema v4) | Data architect |
| D-RCV-30 | `is_primary` = the account the case was opened on; grouped batches open on the first eligible account | Business analyst + solution architect |
| D-RCV-31 | Legal-document confirm re-stores through `DocumentStorage` into `rwb-docs-legal`, audited, refusal-guarded | Solution architect + Compliance |
| D-RCV-32 | TIME_IN_STAGE / TAT_BY_ROUTE median definitions in MD-2026.11 | Tribe lead |
| D-RCV-33 | Restricted promotion grammar (single agreement clause, FSD form); watch measures report-only | Business analyst + solution architect |

## 6. Self-validation and copy sync (2026-11-06, after the regate)

A second validation round swept every derived copy for stale ruling tokens and synced them:

| Check | Result |
|---|---|
| Matrix §8 | 78 PASS, 0 FAIL, 0 PASS_WITH_WARNINGS |
| Compliance files | 78/78 `PASS`; 0 open findings; 0 stale FAIL/WARN footers |
| Specs | 78/78 `RESOLVED [OPEN_ITEMS: 0]` |
| Story copies (v7 + v5 + flat + extracted) | open-point paragraphs ruled in all copies; `AC2`/`AC7` fixtures corrected everywhere |
| Test-case workbook (xlsx + md + csv) | `TC-E1-001-01/04/06`, `TC-E1-013-07`, `TC-E1-014-02` aligned with the rulings |
| FSD rows (P1/P7/P9, both locations) | ruler-invalidated fixtures corrected |
| API Specification v2 (both copies) | `caseNo` + CSV/PDF present; both parse as valid YAML (134 paths each) |
| Decision log mirrors | xlsx, converted md, `open-decisions.csv` (DL41 removed) and `decisions-taken.csv` (D-RCV-28..33 appended) consistent |
| Increment cards | 78/78 compliance rows → `PASS (gate-002 2026-11-06)`; six specification rows → `SUCCESS` |
| Tools | `build_traceability.py` computes the trailer; both tools parse cleanly (`ast`); `verify_package.py` 79/79 pass |

## 7. Still open by design (owner, date)

- **DL26** retention & masking schedule — Compliance, needed by **2026-11-13**.
- **GAP-006** named approvers — replace the acting-approver records with names before the increment card signs.
- **DL11/DL15** NFR baselines — solution architect with Risk; captured as SIT evidence.

## 8. Known mirror limitations (documented, none invalidates a ruling)

1. The pre-cleanup acceptance-criteria blocks inside `legacy/04-user-stories/_csv/...` and the zips still describe story AC sets as at 3 November (the 4–5 November AC cleanup did not regenerate these mirrors). The story files remain authoritative; a mirror regeneration pass with the conversion tooling would reconcile them.
2. `By owner` csv sheet in the decision-log `_csv` mirror is an owner roll-up snapshot and was not regenerated.
3. `verify_package.py` hardcodes its output path to `output/VERIFICATION-20261104/`.
