# Shared updates proposed — INC-009-epic-1-RWB-E1-001 (Technical Specifier)

RUN-BRIEF rule 3: these rows are for the orchestrator to apply in order. This stage edited no shared
file. New open-item and gap numbers are placeholders (`OPEN-NEW-n`, `DG-NEW-n`); the orchestrator
assigns the next free IDs (the register ends at OPEN-042 and DG-003 today).

## 1. `aisdlc/requirement/Traceability_Matrix.md`

§3 Story trace, replace row 009:

| INC | Story | Business | Functional | Spec / plan / evidence | Status |
|---|---|---|---|---|---|
| 009 | `RWB-E1-001` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-009-epic-1-RWB-E1-001/specify/spec.md` | Specified — spec 17 Nov 2026; source `REQ-RDF-001`; SPEC-RWB-E1-001-001..017; spec gate see `review/spec-gate-review.md` |

Requirement-to-spec trace rows (for the Traceability Manager):

| Requirement | Story item | SPEC | Test case |
|---|---|---|---|
| REQ-RDF-001 | BR1, BR7, BR9, AC1, AC2, AC5 | SPEC-RWB-E1-001-005, -006, -009 | TC-E1-001-01, -02, -05 |
| REQ-RDF-001 | BR6, BR8, AC1, AC4, AC6 | SPEC-RWB-E1-001-001, -002, -003, -007, -008, -010, -011 | TC-E1-001-01, -04, -06 |
| REQ-RDF-001 | BR2, BR3, BR4, BR5, AC3, AC7–AC11 | SPEC-RWB-E1-001-004, -012 to -015, -017 | TC-E1-001-03, -07 to -10, -12 |
| REQ-RDF-001 | Authority, X8 | SPEC-RWB-E1-001-016 | TC-E1-001-11 |

## 2. `aisdlc/docs/open-items.md` (proposed new rows)

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| OPEN-NEW-1 | Sequence the recovery migrations: V0001 = RWB-E1-001 (DL v10 D-RCV-28); RWB-E1-042, RWB-E1-043 and RWB-E1-072 must not re-create tables or dictionary rows that Physical Schema v6 puts in V0001 (`parameter_catalog`, `parameter_value`, `reference_version`, `reference_row`, `rule_package`, `rule_package_version`, DF-REF-296 to 299). | RWB-E1-001, E1-042, E1-043, E1-072 | Recovery tech lead with the orchestrator | Before the first recovery migration merges | INC-009 spec `GAP-E1001-16` |
| OPEN-NEW-2 | Who approves a `data_product` catalog load: Story v7 §10 says RW-DATASTEW confirms (U); E1-043 v7 and API v4 need Reference data A, held by no role. | RWB-E1-001, E1-043 | Product Owner with the data steward | Before SIT of the catalog load | INC-009 spec `GAP-E1001-08`, CLAR-009 |
| OPEN-NEW-3 | RWB-E1-043 to publish the `ReferenceTableHandler` seam (Story v7 §12 signature) and the load→validate / approve→apply calls. | RWB-E1-043, E1-001 | RWB-E1-043 spec owner | INC-008 re-spec | INC-009 spec `GAP-E1001-07` |
| OPEN-NEW-4 | Thai text for the Story v7 wording of MSG-P1-003; a message table owner (none in Physical Schema v6). Extend OPEN-005 if preferred. | RWB-E1-001 | BA | Before UAT | INC-009 spec `GAP-E1001-14` |
| OPEN-NEW-5 | Update RWB-E1-001 story counts to Physical Schema v6 (93/123/1,379/1,075) and "version 1.001" to the D-RCV-28 file version; update E1-064/E1-065 references to 122/1,366. | RWB-E1-001, E1-064, E1-065 | BA | Next story file issue | INC-009 spec `GAP-E1001-01`, `-04` |

Existing items touched (no edit, for cross-reference): OPEN-005 (Thai), OPEN-017 (D-RCV-34 not in DL
v10), OPEN-033 (extension-table names before V0001 merge).

## 3. `aisdlc/DOCUMENT-GAPS.md` (candidate rows)

All Blocker = No. Full evidence in `output/INC-009-epic-1-RWB-E1-001/specify/document-gaps.md`.

| Local ID → proposed | Document | Gap | Blocker? |
|---|---|---|---|
| GAP-E1001-16 → DG-NEW-1 | RWB-E1-042, E1-043, E1-072 story files v7 | Own migrations create tables also in Physical Schema v6 / V0001. | No (orchestration) |
| GAP-E1001-01 → DG-NEW-2 | RWB-E1-001 story v7 §4, §11, AC1, AC6; DL v10 D-RCV-29 | v5 counts; v6 is 93/123/1,379/1,075 (D-RCV-36). Extends README decision 7. | No |
| GAP-E1001-02 → DG-NEW-3 | Squad D-RCV-34; migration merge-order map | V0003 vs DL v10 D-RCV-28 V0001. | No |
| GAP-E1001-03 → DG-NEW-4 | Physical Schema v6 `v_data_dictionary` and `data_product` seed | Lag Story v7 §12/§13 and Rulings v2 R2. | No |
| GAP-E1001-07 → DG-NEW-5 | RWB-E1-043 story v7 | No `ReferenceTableHandler` seam although E1-001 depends on it. | No |
| GAP-E1001-08 → DG-NEW-6 | RWB-E1-001 story v7 §10 vs E1-043 v7 / API v4 | Approver right (U vs A held by no role). | No |
| GAP-E1001-12 → DG-NEW-7 | `RecoveryMigrationLintTest` (BS-2.6) | Flags `'public.…'` string data in 297 dictionary rows. | No |
| GAP-E1001-14 → DG-NEW-8 | Error and Message Standard v4 MSG-P1-003; no message table | Wording conflict; no Thai; no table. | No |

Rows GAP-E1001-04, -05, -06, -09, -10, -11, -13 and -15 are story-local and can stay in the run folder
unless the orchestrator prefers them in the register.

## 4. `aisdlc/docs/increments/INDEX.md`

Row 009: status `Specified` once the spec gate passes (or `Spec gate FAIL` with the highest severity).
