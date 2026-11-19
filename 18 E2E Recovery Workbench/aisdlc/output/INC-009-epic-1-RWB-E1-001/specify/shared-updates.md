# Shared updates proposed — INC-009-epic-1-RWB-E1-001 (Technical Specifier, revision 4)

RUN-BRIEF rule 3: these rows are for the orchestrator to apply in order. This stage edited no shared
file. New open-item and gap numbers are placeholders (`OPEN-NEW-n`, `DG-NEW-n`); the orchestrator
assigns the next free IDs. Run-3 proposals are in `shared-updates.run3.md`; this file replaces them.
Revision 4 changes only findings 025 and 026 of spec gate round 3 and proposes no new shared row: the
`parameter_catalog` row shape and the MSG v4 placeholders are story-local. Two run-2 proposals are
**withdrawn** because RWB-E1-043 revision 10 answers them: OPEN-NEW-3 (registry acceptance of a handler
code) and OPEN-NEW-8 (how a repeat carries MSG-P1-011). No proposal claims a human decision; every
D-RUN cited is an orchestrator (Claude Code, an AI agent) run decision.

## 1. `aisdlc/DOCUMENT-GAPS.md` (candidate rows, blockers first)

Full evidence in `output/INC-009-epic-1-RWB-E1-001/specify/document-gaps.md`.

| Local ID → proposed | Document | Gap | Blocker? |
|---|---|---|---|
| GAP-E1001-17 → DG-NEW-1 | RWB-E1-001 story file v7 §13 (DDL vs seed); PS v6 line 820; Logical Data Model and Data Dictionary v8 line 561 | DP07 system of record is 139 characters; column `varchar(120)` in the story DDL, PS v6 and LDM v8. Proceeding on `ASM-E1001-13` (widen to 200, text verbatim). A widening ruling must also update LDM v8 line 561. | **Yes** |
| GAP-E1001-18 → DG-NEW-2 | PS v6 `sys_fields.is_personal` vs PDPA Inventory v4; Personal Data Protection Design v2 line 31 | 18 vs 523 personal; 9 Restricted fields unmarked in PS v6; no precedence. The inventory pointer (Design v2 line 31) is strong but incomplete: it would remove 4 PS v6 marks and has no row for 26 PS v6 fields (DF-REF-274..299), so it is not a documented default for the whole set. Proceeding on `ASM-E1001-14` (protective union, 526); DF-REF-288/-289 named for the ruling. | **Yes** |
| GAP-E1001-19 → DG-NEW-3 | RWB-E1-072 story file v7 (V072_1; FIRST_MATCH) | Re-creates `rule_package`/`rule_package_version`; FIRST_MATCH fails PS v6 CHECK `FIRST`. | No |
| GAP-E1001-20 → DG-NEW-4 | RWB-E1-042 spec revision 13 §12.3 | Three added `parameter_value` columns have no field IDs. | No |
| GAP-E1001-13 → DG-NEW-5 | Story v7 AC10 vs API v4 `ReferenceLoad`, E1-043 revision 10 SPEC-025 L9 / SPEC-006 | **Answered**: `repeatMessage` → 409 `Problem` MSG-P1-011, nothing written. Residual: 409 instead of a message in a 201 body; repeat defined by `(table, validFrom, hash)`. | No (close the row) |
| GAP-E1001-01 → DG-NEW-6 | RWB-E1-001 story v7 §4, §11, AC1, AC6; DL v10 D-RCV-29 | v5 counts; v6 is 93/123/1,379. | No |
| GAP-E1001-08 → DG-NEW-7 | Story v7 §10 vs E1-043 v7 / API v4 | Approver right (U vs A held by no role); E1-043 rev 10 adds interim A for RW-DATASTEW (its A-08). | No |
| GAP-E1001-14 → DG-NEW-8 | MSG v4 MSG-P1-003; no message table | Wording conflict; no Thai for the new text; no table. | No |
| GAP-E1001-22 → DG-NEW-9 | Story v7 X8 | Persistent access log is RWB-E1-039's; an interim REFUSED `REFERENCE_LOAD_AUDIT` line exists (E1-043 SPEC-028). | No |
| GAP-E1001-23 → DG-NEW-10 | RWB-E1-064 v7 §12 vs RWB-E1-043 revision 10 SPEC-031 | Dictionary seam direction; E1-043 rev 10 withdrew its request that RWB-E1-001 own the `sys_fields` handler. | No |
| GAP-E1001-24 → DG-NEW-11 | RWB-E1-001 v7 §12/§19 vs E1-043 SPEC-024 | No rollback for `data_product`; a wrongly approved catalog is corrected only by a later `validFrom`. | No |

GAP-E1001-02, -03, -04, -05, -06, -07, -09, -10, -11, -12, -15, -16, -21 are story-local, closed or
settled by D-RUN decisions and can stay in the run folder. GAP-E1001-06 is **closed** by E1-043
revision 10 (no LOV-REF-TABLE row needed).

## 2. `aisdlc/docs/open-items.md` (proposed new rows)

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| OPEN-NEW-6 | **Blocker (human ruling).** Rule on DP07: widen `data_product.system_of_record` (and DF-REF-074, plus Logical Data Model and Data Dictionary v8 line 561) or shorten the Story v7 §13 DP07 text to ≤ 120. Spec proceeds on widening to `varchar(200)`. Until ruled, the spec and its migration must not be merged. | RWB-E1-001 | Data architect | **Before build (the merge of this story's migration)** | `GAP-E1001-17`, CLAR-011 |
| OPEN-NEW-7 | **Blocker (human ruling).** Rule on `sys_fields.is_personal`: PS v6 (18) vs PDPA Inventory v4 (523), the 26 PS-v6-only fields (DF-REF-274..299, including DF-REF-288 `author` and DF-REF-289 `approver`, user IDs the inventory classes as personal elsewhere), and the governed path that may change a mark (RW-COMPLY, DL26; E1-043 R4). Spec proceeds on the protective union (526); the 26 fields stay `false`; any narrowing only by this ruling. Impacts masking (RWB-E1-016, -037) and the PDPA lint (RWB-TE-011). | RWB-E1-001, E1-016, E1-037, TE-011, E1-064 | Data architect with the DPO (Compliance, DL26) | **Before build (the merge of this story's migration)** | `GAP-E1001-18`, `GAP-E1001-23`, CLAR-012 |
| OPEN-NEW-2 | Who approves a `data_product` catalog load: Story v7 §10 RW-DATASTEW (U); E1-043 and API v4 need Reference data A, held by no role in PS v6. E1-043 rev 10 adds an interim A row for RW-DATASTEW (its A-08). | RWB-E1-001, E1-043 | Product Owner with the data steward | Before SIT of the catalog load | `GAP-E1001-08`, CLAR-009 |
| OPEN-NEW-3 | **Withdraw (answered).** RWB-E1-043 revision 10 SPEC-025 already accepts a registered handler code without a LOV-REF-TABLE row and with an optional `refdata.columns.<code>` definition, and dispatches `validate` at load and `apply` at approval. No action. | RWB-E1-043, E1-001 | — | — | `GAP-E1001-06` (closed), finding 014 |
| OPEN-NEW-4 | RWB-E1-072 V072_1 must not re-create `rule_package` / `rule_package_version` (created by RWB-E1-001 from PS v6, D-RUN-12), and its seed `hit_policy` FIRST_MATCH conflicts with the PS v6 CHECK `FIRST`. | RWB-E1-072, E1-001 | RWB-E1-072 spec owner with the data architect | Before RWB-E1-072 spec | `GAP-E1001-19` |
| OPEN-NEW-5 | Confirm field IDs DF-REF-300..302 for `parameter_value.load_id`, `content_hash`, `rollback_reason` (added by RWB-E1-042), or assign others before RWB-E1-001 merges. | RWB-E1-042, E1-001 | Data architect | Before RWB-E1-001 merge | `GAP-E1001-20` |
| OPEN-NEW-8 | **Withdraw (answered).** E1-043 revision 10 SPEC-025 L9 answers a handler repeat with 409 MSG-P1-011 before the valid-from check, nothing written; `ReferenceLoad` is unchanged. Residual difference from Story v7 AC10 (409 vs a 201 body carrying the message) recorded as `GAP-E1001-13`, Blocker No. | RWB-E1-043, E1-001 | — | — | `GAP-E1001-13`, CLAR-013, finding 014 |
| OPEN-NEW-9 | Local switch coordination (SPEC-010): `RWB_LOAD_REFERENCE_SCHEMA` default `false` at RWB-E1-001 merge; `RWB_LOAD_REFERENCE_VIEWS` stand-in until RWB-E1-069 flips it and applies its Flyway-mode grants; RWB-E1-042 TC-E1-042-14 and the RWB-E1-043 PS v6 baseline IT pin a Flyway target or move to S1 `false`; README wording aligned with RWB-E1-044 SPEC-015. **Two E1-069 points to reconcile:** E1-069 SPEC-015 (a) says E1-069 flips `RWB_LOAD_REFERENCE_SCHEMA` (this story flips it at its own merge), and (c) says the `RecoveryDatabaseIT` version-`0` baseline assertion is replaced (this story keeps it in the S2 stage, `ASM-E1001-18`). | RWB-E1-001, E1-042, E1-043, E1-044, E1-069 | Recovery tech lead with the orchestrator | Before RWB-E1-001 merge | `GAP-E1001-11`, finding 023 |
| OPEN-NEW-10 | RWB-E1-039 adds a persistent access-log assertion (AC-DENY) for a refused `table = data_product` load (Story v7 X8); RWB-E1-001 asserts the interim REFUSED `REFERENCE_LOAD_AUDIT` line meanwhile. | RWB-E1-039, E1-001 | RWB-E1-039 spec owner | RWB-E1-039 spec | `GAP-E1001-22`, finding 022 |
| OPEN-NEW-11 | RWB-TE-011 lint: match fixture fields by (object, field), so the RWB-E1-001 migration (526 marks as INSERT literals) passes with zero findings; run the lint on the migration once both are merged. | RWB-TE-011, E1-001 | RWB-TE-011 spec owner | Before RWB-E1-001 merge | `GAP-E1001-21` |
| OPEN-NEW-12 | Thai text for the Story v7 wording of MSG-P1-003; a message-table owner. Extend OPEN-005 if preferred. | RWB-E1-001 | BA | Before UAT | `GAP-E1001-14` |
| OPEN-NEW-13 | Update RWB-E1-001 story counts to PS v6 and "version 1.001" to the D-RCV-28 naming; state in the story that a repeat is 409 MSG-P1-011 and that no rollback exists for the catalog. | RWB-E1-001, E1-064, E1-065 | BA | Next story file issue | `GAP-E1001-01`, `-04`, `-13`, `-24` |
| OPEN-NEW-14 | Name the owner who enforces the approval of an `is_personal` removal in the dictionary (RW-COMPLY per E1-043 A-36) and ratify the protective rule that no load may change a mark; align RWB-E1-064's seam direction with E1-043 SPEC-031. | RWB-E1-064, E1-043, E1-001 | RW-COMPLY (Compliance), with the E1-064 owner | Before the first dictionary load | `GAP-E1001-23`; E1-043 R4; TE011 §10; DL26 |
| OPEN-NEW-15 | Decide whether `data_product` needs rollback (E1-043 SPEC-024). Story v7 defines none, so the SPI default `supportsRollback = false` applies and a wrongly approved catalog waits for a later `validFrom`. | RWB-E1-001 | BA with the catalog owner | Before UAT | `GAP-E1001-24`, `ASM-E1001-20` |
| OPEN-NEW-16 | **Ratify or reject D-RUN-18, -19, -20 and -21** (orchestrator run decisions, not human rulings). D-RUN-18/-20 govern this story's handler home (P4 `access.api`) and the `PARAMETER` branch; a rejection reopens the SPI placement and the checks this spec relies on. This is E1-043's R24/R1 row seen from this story; keep one owner. | RWB-E1-001, E1-043, E1-042, TE-001 | Recovery tech lead (OPEN-050) | Before RWB-E1-001 plan | D-RUN-18..21; SPEC-019; finding 024 |

Existing items touched (no edit): OPEN-005 (Thai), OPEN-017 (D-RCV-34 not in DL v10), OPEN-033
(extension-table names), OPEN-050 (ratification of D-RUN-18..21). Revision 4 adds no open item and
changes none of these.

## 3. `aisdlc/requirement/Traceability_Matrix.md`

§3 Story trace, replace row 009:

| INC | Story | Business | Functional | Spec / plan / evidence | Status |
|---|---|---|---|---|---|
| 009 | `RWB-E1-001` | `BR-RWB-013` | `FR-RWB-013`; NFR-RWB-005, -006, -008, -009 | `output/INC-009-epic-1-RWB-E1-001/specify/spec.md` | Specified rev 4 — 18 Nov 2026; source `REQ-RDF-001`; SPEC-RWB-E1-001-001..010, 012..019 (011 retired); spec gate round 3 `FAIL` 0/0/0/2 (`review/spec-gate-review-3.md`), Lows 025/026 fixed in rev 4, round 4 pending; Blocker gaps GAP-E1001-17, -18 (human ruling before build) |

Requirement-to-spec trace rows (for the Traceability Manager):

| Requirement | Story item | SPEC | Test case |
|---|---|---|---|
| REQ-RDF-001 | BR1, BR7, BR9, AC1, AC2, AC5 | SPEC-RWB-E1-001-005, -006, -009, -018 | TC-E1-001-01, -02, -05, -14, -17 |
| REQ-RDF-001 | BR6, BR8, AC1, AC4, AC6 | SPEC-RWB-E1-001-001, -002, -003, -007, -008, -010 | TC-E1-001-01, -04, -06, -15 |
| REQ-RDF-001 | BR2, BR3, BR4, BR5, AC3, AC7, AC9–AC11 | SPEC-RWB-E1-001-004, -012 to -015, -017, -018, -019 | TC-E1-001-03, -07 to -10, -12, -13, -16, -18, -19, -20 |
| REQ-RDF-001 | AC8, X4–X7 | SPEC-RWB-E1-001-013, -014, -019 | TC-E1-001-07, -08, -10, -18, -19 |
| REQ-RDF-001 | Authority, X8 | SPEC-RWB-E1-001-016, -019 | TC-E1-001-11 |
| NFR-RWB-005, -006, -008, -009 | Security, privacy, observability, operability | SPEC-RWB-E1-001-007, -008, -016, -017, -018 | TC-E1-001-04, -11, -14, -16, -17 |

## 4. `aisdlc/docs/increments/INDEX.md`

Row 009: status `Specified (rev 4)` if spec gate round 4 passes, otherwise `Spec gate FAIL` with the
highest severity; note the two Blocker = Yes gaps (a human ruling is needed before build).
