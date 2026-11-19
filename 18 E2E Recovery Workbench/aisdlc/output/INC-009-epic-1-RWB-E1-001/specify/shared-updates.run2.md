# Shared updates proposed — INC-009-epic-1-RWB-E1-001 (Technical Specifier, revision 2)

RUN-BRIEF rule 3: these rows are for the orchestrator to apply in order. This stage edited no shared
file. New open-item and gap numbers are placeholders (`OPEN-NEW-n`, `DG-NEW-n`); the orchestrator
assigns the next free IDs. Run-1 proposals are in `shared-updates.run1.md`; this file replaces them
(run-1 OPEN-NEW-1 is withdrawn, settled by D-RUN-12).

## 1. `aisdlc/DOCUMENT-GAPS.md` (candidate rows, blockers first)

Full evidence in `output/INC-009-epic-1-RWB-E1-001/specify/document-gaps.md`.

| Local ID → proposed | Document | Gap | Blocker? |
|---|---|---|---|
| GAP-E1001-17 → DG-NEW-1 | RWB-E1-001 story file v7 §13 (DDL vs seed); PS v6 line 820 | DP07 system of record is 139 characters; column `varchar(120)`. Proceeding on `ASM-E1001-13` (widen to 200, text verbatim). | **Yes** |
| GAP-E1001-18 → DG-NEW-2 | PS v6 `sys_fields.is_personal` vs PDPA Inventory v4 | 18 vs 523 personal; 9 Restricted fields unmarked in PS v6; no precedence. Proceeding on `ASM-E1001-14` (protective union, 526). | **Yes** |
| GAP-E1001-19 → DG-NEW-3 | RWB-E1-072 story file v7 (V072_1; FIRST_MATCH) | Re-creates `rule_package`/`rule_package_version`; FIRST_MATCH fails PS v6 CHECK `FIRST`. | No |
| GAP-E1001-20 → DG-NEW-4 | RWB-E1-042 spec rev 3 §12.3 | Three added `parameter_value` columns have no field IDs. | No |
| GAP-E1001-13 → DG-NEW-5 | Story v7 AC10 vs API v4 `ReferenceLoad`, E1-043 SPEC-006, MSG v4 line 85 | MSG-P1-011 (type Error) cannot be carried on a 201 `ReferenceLoad`. | No |
| GAP-E1001-01 → DG-NEW-6 | RWB-E1-001 story v7 §4, §11, AC1, AC6; DL v10 D-RCV-29 | v5 counts; v6 is 93/123/1,379. | No |
| GAP-E1001-08 → DG-NEW-7 | Story v7 §10 vs E1-043 v7 / API v4 | Approver right (U vs A held by no role). | No |
| GAP-E1001-14 → DG-NEW-8 | MSG v4 MSG-P1-003; no message table | Wording conflict; no Thai for the new text; no table. | No |
| GAP-E1001-22 → DG-NEW-9 | Story v7 X8 | Access log is RWB-E1-039's (later). | No |

GAP-E1001-02, -03, -04, -05, -06, -07, -09, -10, -11, -12, -15, -16, -21 are story-local or settled by
D-RUN decisions and can stay in the run folder.

## 2. `aisdlc/docs/open-items.md` (proposed new rows)

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| OPEN-NEW-6 | **Blocker.** Rule on DP07: widen `data_product.system_of_record` (and DF-REF-074) or shorten the Story v7 §13 DP07 text to ≤ 120. Spec proceeds on widening to `varchar(200)`. | RWB-E1-001 | Data architect | Before build of RWB-E1-001 | `GAP-E1001-17`, CLAR-011 |
| OPEN-NEW-7 | **Blocker.** Rule on `sys_fields.is_personal`: PS v6 (18) vs PDPA Inventory v4 (523). Spec proceeds on the protective union (526); any narrowing only by this ruling. Impacts masking (RWB-E1-016, -037) and the PDPA lint (RWB-TE-011). | RWB-E1-001, E1-016, E1-037, TE-011 | Data architect with the DPO (Compliance, DL26) | Before build of RWB-E1-001 | `GAP-E1001-18`, CLAR-012 |
| OPEN-NEW-2 | Who approves a `data_product` catalog load: Story v7 §10 RW-DATASTEW (U); E1-043 and API v4 need Reference data A, held by no role. | RWB-E1-001, E1-043 | Product Owner with the data steward | Before SIT of the catalog load | `GAP-E1001-08`, CLAR-009 |
| OPEN-NEW-3 | RWB-E1-043 registry (D-RUN-11): accept a table code that has a registered handler without a LOV-REF-TABLE value or `refdata.columns` definition, dispatch `validate` at load and `apply` at approval, and carry the handler's findings into the 422 Problem. E1-043 SPEC-002 / GAP-08 currently refuse `data_product`. | RWB-E1-043, E1-001 | RWB-E1-043 spec owner | INC-008 remediation | `GAP-E1001-06`, `-07` |
| OPEN-NEW-4 | RWB-E1-072 V072_1 must not re-create `rule_package` / `rule_package_version` (created by RWB-E1-001 from PS v6, D-RUN-12), and its seed `hit_policy` FIRST_MATCH conflicts with the PS v6 CHECK `FIRST`. | RWB-E1-072, E1-001 | RWB-E1-072 spec owner with the data architect | Before RWB-E1-072 spec | `GAP-E1001-19` |
| OPEN-NEW-5 | Confirm field IDs DF-REF-300..302 for `parameter_value.load_id`, `content_hash`, `rollback_reason` (added by RWB-E1-042), or assign others before RWB-E1-001 merges. | RWB-E1-042, E1-001 | Data architect | Before RWB-E1-001 merge | `GAP-E1001-20` |
| OPEN-NEW-8 | How a repeat `data_product` load carries MSG-P1-011 (Story v7 AC10): 409 Problem from RWB-E1-043, or a message field on `ReferenceLoad` (API change). | RWB-E1-043, E1-001 | RWB-E1-043 spec owner with the API owner | Before SIT | `GAP-E1001-13`, CLAR-013 |
| OPEN-NEW-9 | Local switch coordination (SPEC-010): `RWB_LOAD_REFERENCE_SCHEMA` default `false` at RWB-E1-001 merge; `RWB_LOAD_REFERENCE_VIEWS` stand-in until RWB-E1-069 flips it and applies its Flyway-mode grants; RWB-E1-042 TC-E1-042-14 and the RWB-E1-043 PS v6 baseline IT pin a Flyway target or move to S1 `false`; README wording aligned with RWB-E1-044 SPEC-015. | RWB-E1-001, E1-042, E1-043, E1-044, E1-069 | Recovery tech lead with the orchestrator | Before RWB-E1-001 merge | `GAP-E1001-11` |
| OPEN-NEW-10 | RWB-E1-039 adds an access-log assertion for a refused `table = data_product` load (Story v7 X8). | RWB-E1-039, E1-001 | RWB-E1-039 spec owner | RWB-E1-039 spec | `GAP-E1001-22` |
| OPEN-NEW-11 | RWB-TE-011 lint: match fixture fields by (object, field), so the RWB-E1-001 migration (526 marks as INSERT literals) passes with zero findings; run the lint on the migration once both are merged. | RWB-TE-011, E1-001 | RWB-TE-011 spec owner | Before RWB-E1-001 merge | `GAP-E1001-21` |
| OPEN-NEW-12 | Thai text for the Story v7 wording of MSG-P1-003; a message-table owner. Extend OPEN-005 if preferred. | RWB-E1-001 | BA | Before UAT | `GAP-E1001-14` |
| OPEN-NEW-13 | Update RWB-E1-001 story counts to PS v6 and "version 1.001" to the D-RCV-28 naming. | RWB-E1-001, E1-064, E1-065 | BA | Next story file issue | `GAP-E1001-01`, `-04` |

Existing items touched (no edit): OPEN-005 (Thai), OPEN-017 (D-RCV-34 not in DL v10), OPEN-033
(extension-table names).

## 3. `aisdlc/requirement/Traceability_Matrix.md`

§3 Story trace, replace row 009:

| INC | Story | Business | Functional | Spec / plan / evidence | Status |
|---|---|---|---|---|---|
| 009 | `RWB-E1-001` | `BR-RWB-013` | `FR-RWB-013`; NFR-RWB-005, -006, -008, -009 | `output/INC-009-epic-1-RWB-E1-001/specify/spec.md` | Specified rev 2 — 18 Nov 2026; source `REQ-RDF-001`; SPEC-RWB-E1-001-001..018 (011 retired); spec gate see `review/spec-gate-review-2.md`; Blocker gaps GAP-E1001-17, -18 |

Requirement-to-spec trace rows (for the Traceability Manager):

| Requirement | Story item | SPEC | Test case |
|---|---|---|---|
| REQ-RDF-001 | BR1, BR7, BR9, AC1, AC2, AC5 | SPEC-RWB-E1-001-005, -006, -009, -018 | TC-E1-001-01, -02, -05, -14, -17 |
| REQ-RDF-001 | BR6, BR8, AC1, AC4, AC6 | SPEC-RWB-E1-001-001, -002, -003, -007, -008, -010 | TC-E1-001-01, -04, -06, -15 |
| REQ-RDF-001 | BR2, BR3, BR4, BR5, AC3, AC7–AC11 | SPEC-RWB-E1-001-004, -012 to -015, -017, -018 | TC-E1-001-03, -07 to -10, -12, -13, -16 |
| REQ-RDF-001 | Authority, X8 | SPEC-RWB-E1-001-016 | TC-E1-001-11 |
| NFR-RWB-005, -006, -008, -009 | Security, privacy, observability, operability | SPEC-RWB-E1-001-007, -008, -016, -017, -018 | TC-E1-001-04, -11, -14, -16, -17 |

## 4. `aisdlc/docs/increments/INDEX.md`

Row 009: status `Specified (rev 2)` if spec gate round 2 passes, otherwise `Spec gate FAIL` with the
highest severity; note the two Blocker = Yes gaps.
