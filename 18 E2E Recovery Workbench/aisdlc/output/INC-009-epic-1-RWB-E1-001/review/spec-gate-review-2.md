# Spec gate review, round 2: RWB-E1-001 Recovery tables for the 14 data products

| Item | Value |
|---|---|
| RUN_ID | `INC-009-epic-1-RWB-E1-001` |
| Gate | SPEC GATE (Compliance Reviewer, round 2) |
| Reviewed | `specify/spec.md` (revision 2), `assumptions.md`, `document-gaps.md`, `compliance-validation.md`, `shared-updates.md`, `contracts/backend-apis.json`, `evidence/` (`pdpa_v4_vs_ps_v6.py` and output, `is_personal_union_v4.tsv`, `count_v6*`, `lint_v6*`); against round 1 (`review/spec-gate-review.md`, findings 001 to 013) and `specify/gate-response.md`; run-1 copies `*.run1.*` |
| Instructions | `.claude/agents/compliance-reviewer.md`; `aisdlc/RUN-BRIEF.md`; repository `CLAUDE.md`, `AGENTS.md` |
| Precedence applied | D-RCV-35/36, then ADR v3, then Decision Log v10, then story files v7, then older maps and drafts (RUN-BRIEF) |
| Run decisions checked | D-RUN-07 to D-RUN-13, `AI-SDLC-BUILD-LOG.md` §1 and timeline rows of 2026-11-17T23:26 to 2026-11-18T00:04. All seven were taken by the orchestrator (Claude Code, an AI agent); none carries a human approval |
| Sibling specs checked (state on disk at review time) | E1-043 INC-008 `spec.md` (00:09) and `shared-updates.md`, `document-gaps.md`, `gate-response.md`; E1-042 INC-003 `spec.md` (revision 4, 00:18); E1-044 INC-001 `spec.md`; E1-069 INC-010 `spec.md`; TE-011 INC-006 `spec.md` (00:18); TE-001 INC-002 `spec.md` |
| Excluded | README "Decisions taken while setting this up" items (known, not re-reported) |
| Date | 18 November 2026 |

## Overall status

**STATUS: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 1 |
| Medium | 3 |
| Low | 7 |

**GATE RESULT: BLOCKED.** One High and three Medium findings block the handoff to the Implementation
Planner. Separately, and whatever the outcome of this review, the two Blocker = Yes document gaps
(`GAP-E1001-17`, `GAP-E1001-18`) still need a human ruling (OPEN-NEW-6, OPEN-NEW-7). No human has
given one. The orchestrator that triaged them is an AI agent, and this review is not a human
disposition either.

Round 1 is largely remediated: 11 of 13 findings are resolved and verified, and 1 is resolved with a
residual Low. Finding 003 (handler seam) is **not resolved**: the revised spec and the current RWB-E1-043
spec contradict each other on the registry contract (REVIEW-RWB-E1-001-014).

## Reviewer verification (independent, `python -I`)

The reviewer wrote a read-only check and ran it with `python -I`. The script was kept in the session
scratchpad and is not written to the run folder. It read Physical Schema v6, PDPA Inventory v4 and
`evidence/is_personal_union_v4.tsv`. Results:

| Claim in the spec | Result |
|---|---|
| PS v6 `sys_fields` 1,379, `is_personal = true` 18; Inventory v4 Fields tab 1,366 rows, 523 "Personal data = Yes" | Confirmed |
| Union of PS v6 `true` or Inventory v4 "Yes" = 526: 14 both, 4 PS v6 only, 508 Inventory v4 only | Confirmed; the TSV equals the recomputed set |
| Field IDs join correctly between the two sources | Confirmed: 1,353 shared IDs, **0** entity or field name mismatches. No Inventory v4 (entity, field) maps to a different PS v6 ID. The TSV names match PS v6 |
| All 17 Inventory v4 Restricted fields (12 Direct identifier, 5 Sensitive) are in the union | Confirmed (DF-ACE-003, -041, -053, -057, -058, -059, -060, -061, -066, -073, -078, -116; DF-DOC-015; DF-EXT-002, -003, -004; DF-INT-011) |
| IDs in only one source | PS v6 only: 26 (DF-REF-274..299, the `rule_package*`, `rule_row` and `rule_test_case` fields added by D-RCV-36). Inventory v4 only: 13 (DF-REF-261..273, `payment_match_rule`, removed) |
| T8: 4 tables; only `fk_reference_row_version_id` and `ix_reference_row_version_id` sit on them; FKs at lines 2228, 2244, 2245, 2248 target `reference_version` | Confirmed: 91 FKs and 111 indexes are created. No PS v6 seed or other statement touches the four tables |
| T8: "57 `sys_fields` rows" on the four tables | **Not confirmed: 53.** 57 is the comment count (4 table plus 53 column comments) (REVIEW-018) |
| DP07 Story v7 §13 `system_of_record` is 139 characters; all other seed values fit | Confirmed (evidence output reproduced; DP04 97 is the next longest) |
| 18 ACE link columns `varchar(255)` plus `document_intake.file_name` | Confirmed (19 `varchar(255)` table columns) |
| No PS v6 `v_ace_*` view references a recovery table (needed for the S2 views-only init in SPEC-010) | Confirmed |
| LOV-REFRESH sort order DAILY 1, WEEKLY 2, MONTHLY 3, ON_CHANGE 4 (AC9 text order) | Confirmed (PS v6 lines 5035 to 5038) |
| `char(n)` in PS v6 `sys_fields.physical_type` is written `char(64)` (8) and `char(7)` (1) | Confirmed. The spec seeds DF-REF-301 as `character(64)` (REVIEW-019) |
| MSG v4 lines 68, 77, 78, 81, 85, 151; API v4 approve (409 MSG-P7-002, `AC-VERS`); BS v6 orders 1, 3, 6, 8, 9, 10, 13, 16, 28, 36 | Confirmed |
| E1-042 adds `parameter_value.load_id uuid`, `content_hash char(64)`, `rollback_reason varchar(400)` | Confirmed in E1-042 spec revision 4 §12.3 (the spec cites revision 3) |
| E1-043 `reference_version` / `reference_row` use only PS v6 columns | Confirmed (E1-043 SPEC-001), so C1 needs only the three E1-042 provisional rows |

## Round-1 findings: disposition

| Round-1 finding | Severity | Round-2 verdict | Basis |
|---|---|---|---|
| 001 DP07 139 > `varchar(120)` | High | **Resolved** | Recorded as GAP-E1001-17 (Blocker = Yes) with two citations. Labelled ASM-E1001-13. T9 changes the DDL and DF-REF-074 together. A seed-fits unit and IT check is added (SPEC-018(1), TC-13). The Blocker is sound (see the Blocker assessment below). Residual citation gap: REVIEW-020 |
| 002 BR7 vs PDPA v4 | High | **Resolved, with a residual Low** | GAP-E1001-18 (Yes), ASM-E1001-14, union 526 (verified above), TC-14 and TC-17. BR7 is no longer "PS v6 as written". Residual: 26 unclassified PS v6 fields not addressed (REVIEW-020) |
| 003 Handler seam / coverage | High | **Not resolved** | Re-raised as REVIEW-RWB-E1-001-014 (High). The spec's stated "requirement on E1-043" contradicts E1-043 SPEC-025, -027, -029 and -003 as they now stand |
| 004 Ordering / rule (b) | Medium | **Resolved** | Rule (b) and the V0001 wording are removed (D-RUN-07). T8 lists the exact skipped objects (verified) and SPEC-002 "nothing else" now holds. Count slip: REVIEW-018 |
| 005 MSG-P1-011 | Medium | **Resolved** | Citation corrected (MSG v4 line 85, type Error). AC10 is PARTIAL with GAP-E1001-13, ASM-E1001-15 and OPEN-NEW-8. The contract file states the open point. `NO_API_CHANGE` is now consistent |
| 006 X8 access log / approval audit | Medium | **Resolved** | The 403 path and "nothing written" are asserted. The access log is a named seam to RWB-E1-039 (BS v6 order 28, D-RUN-08). Inherited maker-checker and `AC-VERS` are traced. Improvement: REVIEW-022 |
| 007 Local Flyway switch | Medium | **Resolved** | SPEC-010 names S1, S2 and S3, their files, defaults, invalid combination, test stages, reset and the E1-069 hand-off. Verified against `10-load-ace-database.sh`, `docker-compose.yml` line 28, `.env.example` line 16 and `application.yaml` line 79. Sibling staleness: REVIEW-023 |
| 008 Messages | Medium | **Resolved** | README decision 5 citation removed. E1-042 `MessageResolver` / `FixedMessageCatalog` seam verified (E1-042 SPEC-022). Package naming: REVIEW-023 |
| 009 `rule_package` seed | Medium | **Resolved** | The basis is Story v7 lines 240 and 252 and E1-072 v7. The E1-072 table and CHECK conflict is recorded as GAP-E1001-19 and OPEN-NEW-4 |
| 010 SOR grammar | Low | **Resolved** | F1 to F3 are labelled ASM-E1001-09, with negative cases. New design concern: REVIEW-021 |
| 011 `char(n)` | Low | **Resolved** | `character(n)` added. New inconsistency: REVIEW-019 |
| 012 Link keys | Low | **Resolved** | 18 columns, verified |
| 013 NFR / PBR v2 | Low | **Resolved** | NFR-RWB-005, -006, -008, -009 mapped, the rest N/A with reasons (REQ v2.0 lines 229 to 238 verified). PBR v2 cited |

## Assessment of the two Blocker = Yes gaps

The orchestrator's triage set both gaps to Blocker = Yes. The orchestrator is Claude Code, an AI agent.
All four specify artefacts say so (`assumptions.md` line 9, `document-gaps.md` line 10,
`gate-response.md` lines 8 and 9).

| Test | GAP-E1001-17 (DP07 width) | GAP-E1001-18 (`is_personal`) |
|---|---|---|
| **Sound**: evidence and correct use of Blocker = Yes | Yes. The conflict is inside Story v7 §13 (DDL `varchar(120)` vs the 139-character seed). PS v6 line 820 and Logical Data Model v8 line 561 (DF-REF-074 `varchar(120)`, not cited) agree with the DDL but carry an older text. The only shorter wording in the set (Specification Rulings v2 R4 line 205, status Proposed) contains ";", which BR3, AC7 and F2 treat as two systems of record. No precedence rule or documented default yields a text that fits and passes BR3. Blocker = Yes is correct | Yes, conservatively. PS v6 (adopted by D-RCV-36 row 18) and Inventory v4 disagree on 512 fields. Personal Data Protection Design v2 line 31 ("The field-level inventory is the data classification and personal data inventory workbook") and backend context line 129 point to the inventory. Read alone, that could support Blocker = No with the inventory governing. It does not settle the 4 PS-v6-only marks or the 26 fields the inventory does not list, and classification belongs to Compliance (DL26). Holding a change to 508 masking flags for a human ruling is the protective choice. The gap row should cite the pointer and say why it is not treated as a default (REVIEW-020) |
| **Visible** | Yes: spec header Status, the Assumptions table, coverage status `COVERED (ASM)`, CLAR-011, the status block, `shared-updates.md` DG-NEW-1 and OPEN-NEW-6 marked **Blocker**, and the contract file. Stage wording is inconsistent (REVIEW-024) | Yes: same places, plus CLAR-012, DG-NEW-2, OPEN-NEW-7 marked **Blocker**, and the impact on E1-016, E1-037 and TE-011 named |
| **Protective** | Yes. The business text stays verbatim. Widening is non-destructive and can be reverted before merge. The seed-fits test guards either ruling outcome. No personal-data impact | Yes for the fields both sources classify. The mark is a superset of both sources and never lower than either. Marks are INSERT literals that TE-011's reader parses (TE-011 SPEC-TE011-001 R1, multi-row accepted, fail closed on others; verified in the current TE-011 spec). Zero TE-011 findings is an acceptance condition. Gaps: (a) the 26 PS-v6-only fields stay `false` without comment. Two of them, DF-REF-288 `rule_package_version.author` and DF-REF-289 `.approver`, are user IDs that the inventory consistently classes as "Staff identifier, Personal data = Yes" elsewhere (DF-REF-156/157, -166/167, -273) (REVIEW-020). (b) ASM-E1001-14 says the set may be narrowed "only by that ruling", but no control or owner in this spec enforces that against later dictionary loads (REVIEW-017) |

Conclusion: both gaps and their labelled assumptions are sound, visible and protective enough to carry
the spec. They do not replace the human ruling, and nothing in the run presents them as approved.

## Findings

### REVIEW-RWB-E1-001-014: High. The registry contract contradicts RWB-E1-043; `data_product` loads are still refused, so AC3 and AC7 to AC11 cannot be reached (round-1 finding 003 not resolved)

- **Maps to:** SPEC-RWB-E1-001-013, -014, -015, -016, -017; ASM-E1001-05, -12, -19; OPEN-NEW-3; `contracts/backend-apis.json` `registry_registration.requirement_on_E1_043`; AC3, AC7, AC8, AC9, AC10, AC11, X4 to X7, TC-E1-001-03, -07 to -12; FR-RWB-013.
- **Evidence:** SPEC-017 and OPEN-NEW-3 make it a "requirement on E1-043" that a registered handler code is accepted "without needing a `LOV-REF-TABLE` value or a `refdata.columns.<code>` definition". ASM-E1001-19 says K0 exists "because E1-043 holds no column definition for `data_product`". The current E1-043 spec (INC-008, written before this revision) says otherwise:
  - SPEC-025 (lines 452 to 460): "generic checks (SPEC-003 column definition and row check …) run first; only if they pass, `validate` runs". "A handler code needs no LOV-REF-TABLE row … but needs a column definition and the loader and approver keys of SPEC-029, supplied by the owning story; without them the load is refused."
  - SPEC-027 (lines 492 to 498): table right from `rwb.refload.loader.<code>` / `rwb.refload.approver.<code>`; "A missing key or empty value refuses."
  - SPEC-029 (line 532): "A handler code's three keys come with its owning story."
  - SPEC-003 (lines 238 to 249): the generic row check refuses a missing required value with 422 MSG-P3-027 before any handler runs.
  - E1-043 `shared-updates.md` line 65 asks this story to add `refdata.columns.data_product`, `rwb.refload.loader.data_product` and `rwb.refload.approver.data_product`.

  This spec adds none of the three keys and does not answer E1-043's shared update. Under D-RUN-11 the registry and its rules are E1-043's (BS v6 order 8, earlier), and D-RUN-08 makes this story conform.
- **Failure scenario:** with E1-043 built as specified, RW-REFADM's AC3 load of `table = data_product` is refused with 403 (no `rwb.refload.loader.data_product`), or with 422 MSG-P3-027 (no column definition). `DataProductCatalogHandler.validate` never runs, so none of the MSG-P1-003, -004 or -007 paths of AC7 to AC9 and AC11 can be observed. If a column definition is added naively with `:R` on `owner_user_id` or `system_of_record`, AC7 (DP11, no owner) and X4 (no system of record) return MSG-P3-027 from the generic check instead of MSG-P1-003, and DP06's finding is never produced. TC-E1-001-11 would pass for the wrong reason (missing key, not the missing right).
- **Remediation:** conform to E1-043 SPEC-025, -027 and -029, or get the orchestrator to reconcile both specs and record the outcome in both:
  1. Add the three catalog rows for `data_product` by the same route E1-043 uses: catalog file rows plus migration rows, with the definition value loaded or defaulted before the first table load.
  2. Give the column definition (8 columns; `product_code` as `K`). Mark `:R` only where an empty value must not be reported as MSG-P1-003, so that X4 and AC7 still come from the handler.
  3. Name the loader list (RW-REFADM) and the approver list. The approver is still GAP-E1001-08 / OPEN-NEW-2: E1-043 needs area right A plus the list, and RW-DATASTEW holds no A.
  4. Correct ASM-E1001-19 and SPEC-017, OPEN-NEW-3 and the contract file. Say which checks (K0) move to E1-043's generic check.
  5. Mark AC3 and AC7 to AC11 PARTIAL until both specs agree.

### REVIEW-RWB-E1-001-015: Medium. AC9's owner-role message text was changed from the story's wording (regression from run 1, unrecorded)

- **Maps to:** SPEC-RWB-E1-001-013 (K4), SPEC-015; AC9, X6; TC-E1-001-09.
- **Evidence:** Story v7 AC9 (line 151) requires "Row 4: owner_role must be one of the role codes in LOV-ROLE." Run 1 K4 set `{values}` = "the role codes in LOV-ROLE" (`spec.run1.md` line 314). Revision 2 K4 sets `{values}` = "active role codes in sort order", which yields a list of the 54 PS v6 role codes. Neither `gate-response.md` nor any gap or assumption records the change, and TC-E1-001-09 asserts only "two MSG-P1-007 texts".
- **Failure scenario:** the AC9 test written to the story text fails, or it is written to the spec text and AC9 is silently not met. The response also lists every role code to the caller.
- **Remediation:** restore the AC9 wording, or record the deviation as a gap with a basis. Make TC-E1-001-09 assert both AC9 texts verbatim. The K5 wording, "DAILY, WEEKLY, MONTHLY, ON_CHANGE", already matches the LOV-REFRESH `sort_order` (verified).

### REVIEW-RWB-E1-001-016: Medium. K0 "required value" overlaps K2 and K3, so an empty system of record or a missing owner can lead with MSG-GEN-001 instead of MSG-P1-003

- **Maps to:** SPEC-RWB-E1-001-013 (K0, K2, K3, negative-case list), SPEC-015 (`messageCode` = first finding, file-level first); ASM-E1001-19; AC7, AC11, X4; field-level matrix rows `system_of_record`, `owner_user_id`.
- **Evidence:** Story v7 X4 says a row that "names no system of record … or no owner user ID" is refused with MSG-P1-003. AC7 expects MSG-P1-003 "for DP06 and for DP11" (DP11 has no owner). K0 reports "Missing value: MSG-GEN-001" for "every required value". The field matrix marks `owner_user_id` "Required in the file (K3)". The negative list says an empty system of record is "also K0". SPEC-015 takes `messageCode` from the first finding with file-level findings first, but the spec does not say whether K0 is file-level or per row, or whether K0 stops K2 and K3 for that row.
- **Failure scenario:** a file whose only defect is DP11 without an owner returns `messageCode` MSG-GEN-001, so X4 is not met. AC7's detail carries an extra MSG-GEN-001 entry, or DP11's MSG-P1-003 is missing if K0 stops the row. The tests cannot be written unambiguously.
- **Remediation:** state the K0 required set explicitly and exclude `system_of_record` and `owner_user_id`, whose absence is MSG-P1-003 by X4. Say whether K0 is file-level. Add the single-defect cases (DP11 no owner only; DP06 empty system of record only), each expecting MSG-P1-003 as `messageCode`. Align with the E1-043 generic check in REVIEW-014.

### REVIEW-RWB-E1-001-017: Medium. Cross-story asks from RWB-E1-043 are unanswered, including the dictionary-load handler that would govern later `is_personal` changes

- **Maps to:** ASM-E1001-14 ("fields may only be removed by that ruling"), GAP-E1001-18, OPEN-NEW-7; SPEC-006 (`lov_value` seed); `shared-updates.md` §2; §19 out-of-scope list; BR7; NFR-RWB-006.
- **Evidence:** E1-043 `shared-updates.md` line 66 and SPEC-031 (lines 544 to 559) assign this story a data-dictionary handler for `sys_objects` / `sys_fields`, with `changeSummary` reporting `is_personal` changes and `rwb.refload.approver.<dictionary code>` = RW-COMPLY (its A-36). Its line 67 opens an item on whether removing an `is_personal` mark needs further approval. RWB-E1-064 v7 (BS v6 order 13, later) owns a `DataDictionaryLoader` for loads with table `sys_fields` (story lines 50, 51, 174, 230), so the two documents disagree on the owner. E1-043 `shared-updates.md` line 81 also asks this story to correct the LOV-REF-TABLE seed (remove ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER, HOLIDAY). This spec seeds the 598 PS v6 `lov_value` rows unchanged and mentions none of these asks. DL v10 D-RCV-29, quoted in Story v7 §11, says later dictionary changes are reference loads.
- **Failure scenario:** the 526 marks of ASM-E1001-14 can be narrowed by a later dictionary load. This spec names no owner, approver or audit for that path, so the "only by that ruling" protection is unenforced and unowned. E1-043 and E1-064 may each wait for the other or for this story.
- **Remediation:** answer each E1-043 ask in `document-gaps.md` and `shared-updates.md`:
  - **Dictionary handler.** Decline it with a citation to RWB-E1-064 v7 (later; D-RUN-08 seam) and record the E1-043 vs E1-064 ownership conflict as a gap and open item. Or accept it with a basis. Either way, name who enforces the approval of an `is_personal` removal (RW-COMPLY, E1-043 A-36) and link it to OPEN-NEW-7.
  - **LOV-REF-TABLE.** Seed it as PS v6 with a recorded reason, or correct it with a basis.

### REVIEW-RWB-E1-001-018: Low. T8 and the self-check say 57 `sys_fields` rows on the four T8 tables; PS v6 has 53

- **Maps to:** SPEC-RWB-E1-001-002 (T8), `compliance-validation.md` §2 ("4 + 57 dictionary rows"), `gate-response.md` row 004.
- **Evidence:** PS v6 has 53 `INSERT INTO sys_fields` rows whose `object_name` is one of the four tables (reviewer count, also by `grep -c`). 57 is the number of comment statements (4 + 53). The totals 1,379 / 1,382 are unaffected.
- **Remediation:** correct to 53 in all three places.

### REVIEW-RWB-E1-001-019: Low. DF-REF-301 `physical_type` `character(64)` breaks the PS v6 convention `char(64)`; C3's canonical form is ambiguous

- **Maps to:** SPEC-RWB-E1-001-006 (provisional rows), SPEC-009 (C3), ASM-E1001-17; AC5; TC-E1-001-05.
- **Evidence:** All 9 PS v6 `char` fields record `physical_type` as `char(n)` (for example DF-REF-170 `reference_version.content_hash` `char(64)`, line 4359). SPEC-006 seeds DF-REF-301 as `character(64)`. SPEC-009 lists "`character(n)` (catalog `bpchar`, written `char(n)` in DDL)", and its fixture matches "`character(64)` column … to `char(64)`".
- **Failure scenario:** whichever canonical form the normaliser emits, either the 9 PS v6 rows or DF-REF-301 fail C3, and C1/C2 1,050 / 1,078 are not reached.
- **Remediation:** seed DF-REF-301 as `char(64)`, and state that C3 normalises catalog `bpchar(n)` to `char(n)`.

### REVIEW-RWB-E1-001-020: Low. Blocker gap records are incomplete: unclassified fields, an uncited third source and an uncited classification pointer

- **Maps to:** GAP-E1001-17, GAP-E1001-18; ASM-E1001-13, -14; OPEN-NEW-6, -7; BR7.
- **Evidence:**
  - (a) 26 PS v6 fields (DF-REF-274..299) have no Inventory v4 row and keep the PS v6 value `false`. Among them, DF-REF-288 `rule_package_version.author` and DF-REF-289 `.approver` are user IDs, a pattern Inventory v4 classes "Staff identifier, Personal data = Yes" (DF-REF-156/157, -166/167, -273).
  - (b) GAP-17 does not cite Logical Data Model and Data Dictionary v8 line 561 (DF-REF-074 `varchar(120)`, length 120). A ruling to widen must also update that document.
  - (c) GAP-18 does not cite Personal Data Protection Design v2 line 31, which names the inventory as the field-level classification, or explain why it is not a documented default.
- **Remediation:**
  - (a) List the 26 fields in GAP-18 and OPEN-NEW-7 for classification. Either mark DF-REF-288 and -289 `true` under the protective rule with a stated basis, or record why not.
  - (b) and (c) Add the citations and the reasoning to the gap rows.

### REVIEW-RWB-E1-001-021: Low. F3 turns three catalog sentences into code literals, against BR4 and §17

- **Maps to:** SPEC-RWB-E1-001-013 (F3), SPEC-017 (literal exemption), ASM-E1001-09; BR4; Story v7 §17, §6 "Negotiable"; AGENTS.md §3.2, §4.8.
- **Evidence:** F3 accepts only `Recovery Workbench`, `Recovery Workbench document hub` or `Recovery Workbench, with the ACE lists read through the views`, the exact DP03/DP10/DP14 seed texts. BR4 says catalog values are "changed without a code release". §17 says systems of record "come from the catalog load". SPEC-017 exempts "the F1–F3 patterns" from the no-literal rule without a cited basis. Round 1 asked for closed forms, but F1 and F2 are grammars, while F3 is a value list.
- **Failure scenario:** a data steward rewording DP10's system of record through a load (BR4) is refused until a code release.
- **Remediation:** express F3 as a grammar (for example `Recovery Workbench` optionally followed by a qualifier that names no other source), or hold the accepted qualifiers as reference data. Keep the negative cases. Record the basis in ASM-E1001-09.

### REVIEW-RWB-E1-001-022: Low. X8: the earlier story's interim refusal audit is not used, and GAP-22 says no logging exists

- **Maps to:** SPEC-RWB-E1-001-016; GAP-E1001-22; X8; TC-E1-001-11; NFR-RWB-005.
- **Evidence:** E1-043 SPEC-028 (BS v6 order 8, earlier) writes an interim `event=REFERENCE_LOAD_AUDIT` line for every load, including refusals (`outcome` REFUSED, `table`, `messageCode`, no user ID). RWB-E1-039 later replaces it with the access log. GAP-E1001-22 cites "`ApiExceptionHandler` (no logging)" as the evidence that nothing exists.
- **Remediation:** have TC-E1-001-11 also assert one REFUSED `REFERENCE_LOAD_AUDIT` event with `table = data_product` and no personal data. Keep the E1-039 access-log seam. Correct GAP-22's evidence.

### REVIEW-RWB-E1-001-023: Low. Stale cross-references to sibling specs

- **Maps to:** SPEC-RWB-E1-001-010, -012, -015; Sources table; OPEN-NEW-9.
- **Evidence:**
  - (a) SPEC-012 makes `dataengine` depend on `platform.api` (`MessageResolver`, `ApiProblemException`). TE-001 (BS v6 order 2) SPEC-022 removes the `platform` package. `ApiProblemException` moves to `access.api`, `RecoveryFlags` to `integration.flags.api`, and `RecoveryFlywayConfig` to `casewf.migration` (TE-001 spec lines 211 to 216).
  - (b) E1-042 is cited as "spec rev 3". The current file is revision 4.
  - (c) E1-069 SPEC-015 (a) and (c) still say E1-069 flips `RWB_LOAD_REFERENCE_SCHEMA` and that the version-`0` baseline assertion is replaced. This spec flips S1 at its own merge, adds S2 and keeps the baseline row (ASM-E1001-18). OPEN-NEW-9 names the coordination but not these two points.
- **Remediation:** name modules by their published package after TE-001, or "the package that publishes X". Update the revision citations. Add (c) explicitly to OPEN-NEW-9.

### REVIEW-RWB-E1-001-024: Low. Blocker scope and the status of run decisions are stated inconsistently

- **Maps to:** spec Status and CLAR-011, -012 ("before build"); status block `NEXT_STEP` ("before the Implementation Planner"); `shared-updates.md` OPEN-NEW-6, -7 ("Before build"); GAP-E1001-12, -16 ("Settled by D-RUN-12/13").
- **Evidence:**
  - Different places say the human ruling stops the planner and say it stops the build.
  - D-RUN-10 to D-RUN-13 are orchestrator (AI) decisions with no human approval (`AI-SDLC-BUILD-LOG.md` timeline 23:47 and 23:49). They are not in the RUN-BRIEF precedence. The spec cites them as settling gaps without saying so, although it does label the AI triage of GAP-17 and GAP-18.
- **Remediation:** use one statement of what the two Blocker gaps stop. The ASMs change seed values only, so "before build (merge of this story's migration)" is consistent with OPEN-NEW-6 and -7. Label D-RUN-10 to -13 in the Sources table as orchestrator (AI) run decisions, not human rulings.

## Verified correct (no finding)

- The DP07 fix, the union, T8, link keys and counts, as tabulated under "Reviewer verification".
- TE-011 compatibility. The current TE-011 SPEC-TE011-001 reads single- and multi-row `INSERT INTO sys_fields (<columns>) VALUES …` with a schema-qualified target. It matches values by column name and fails closed on bulk `UPDATE` and other writes. It matches fixtures by (object, field) (TE-011 spec lines 235 to 238 and 397). This spec's T10 and SPEC-018(4) fit that reader. TE-011 is BS v6 order 6 (earlier), so the acceptance condition depends on an earlier story (D-RUN-08).
- SPEC-010 S2 init is workable. The PS v6 view section references only `public` tables and helper functions, so it compiles before Flyway creates the recovery tables. `20-grants.sql.inc` runs in both modes (`10-load-ace-database.sh`).
- Messages via E1-042 `MessageResolver` / `FixedMessageCatalog` (E1-042 SPEC-022); MSG v4 texts and types cited correctly.
- API: `NO_API_CHANGE` is consistent with the contract file. API v4 approve requires Reference data A and gives 409 MSG-P7-002, and approval writes `AC-VERS`. The inherited controls are traced to E1-043.
- **Unit-test gates planned:** Frontend `NOT_APPLICABLE` (Story v7 §15, no screen). Backend `REQUIRED`: 80% lines, branches, statements and functions on `th.co.scb.ace.demo.recovery.dataengine`, with pass and fail cases per K0 to K5 and F1 to F3. Integration tests (`recovery-it`) are kept separately and are not substituted. This meets `implementation-execution-gates.md` for a spec review.
- No personal data in any specify artefact. The union TSV holds field IDs and column names only, and test owner IDs are random UUIDs.
- Shared files untouched; proposals are in `shared-updates.md`. The DP07 text and the story's English message texts are kept verbatim.
- The AI-agent nature of the triage is disclosed in `assumptions.md`, `document-gaps.md` and `gate-response.md`, and no artefact claims a human approval.

## Gate checklist

| Check | Result |
|---|---|
| Every requirement traced to a cited source or labelled assumption | FAIL (014: AC3, AC7 to AC11 rest on a contract the owning story contradicts; 015: AC9 text) |
| No invented requirement | PASS (SOR grammar labelled; F3 literal concern Low 021) |
| Authentication and authorization | FAIL (014: loader and approver keys missing, so the load right cannot work as specified; approver right still GAP-E1001-08) |
| Customer and account data protection | PASS with residuals (union verified; 017 Medium on the narrowing control; 020 Low on unclassified fields) |
| Audit logging | PASS (seam to E1-039; inherited `AC-VERS`; improvement Low 022) |
| Error contract consistency | FAIL (015, 016) |
| Secrets and environment configuration | PASS (SPEC-010; no secrets) |
| Dependencies only on earlier stories / repo (D-RUN-08) | FAIL (014: does not conform to the earlier story's registry; 017 unanswered asks) |
| Migration number placeholder (D-RUN-07) | PASS |
| Blocker = Yes gaps sound, visible, protective | PASS (see assessment; Lows 020, 024) |
| Unit-test 80% gates planned per surface | PASS |
| Test coverage and evidence planned | PASS, except AC9 (015), AC7/X4 single-defect cases (016), X8 interim audit (022) |
| No personal data | PASS |

## Blocking statement

STATUS: FAIL. REVIEW-RWB-E1-001-014 (High) and -015, -016, -017 (Medium) block the handoff to the
Implementation Planner. The Technical Specifier must:

- reconcile the registry contract with RWB-E1-043 (or obtain a recorded orchestrator reconciliation
  reflected in both specs);
- restore the AC9 text;
- define the K0 required set; and
- answer RWB-E1-043's shared updates.

The Low findings 018 to 024 are also to be fixed (D-RUN-09). A third round (`spec-gate-review-3.md`)
is required.

Independently of this review, GAP-E1001-17 and GAP-E1001-18 remain Blocker = Yes until a human ruling
is recorded (OPEN-NEW-6, OPEN-NEW-7). No AI triage, including this review, is that ruling.
