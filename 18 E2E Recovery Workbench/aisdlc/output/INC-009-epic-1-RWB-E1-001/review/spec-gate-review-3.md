# Spec gate review, round 3: RWB-E1-001 Recovery tables for the 14 data products

| Item | Value |
|---|---|
| RUN_ID | `INC-009-epic-1-RWB-E1-001` |
| Gate | SPEC GATE (Compliance Reviewer, round 3) |
| Reviewed | `specify/spec.md` (revision 3), `assumptions.md`, `document-gaps.md`, `compliance-validation.md`, `shared-updates.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `evidence/` (`pdpa_v4_vs_ps_v6.py` and output, `is_personal_union_v4.tsv`, `count_v6*`, `lint_v6*`); against round 2 (`review/spec-gate-review-2.md`, findings 001 to 024) and `specify/gate-response.md`; run-2 copies `*.run2.*` |
| Instructions | `.claude/agents/compliance-reviewer.md`; `aisdlc/RUN-BRIEF.md`; repository `AGENTS.md` |
| Precedence applied | D-RCV-35/36, then ADR v3, then Decision Log v10, then story files v7, then older maps and drafts (RUN-BRIEF) |
| Cross-story source of truth | RWB-E1-043 **revision 10** (`INC-008-epic-1-RWB-E1-043/specify/spec.md`), read live at SPEC-001, -002, -003, -006, -019, -024, -025, -026, -027, -028, -029, -030, -031, -032 and `shared-updates.md` section 3, section 3.1, section 3.2. RWB-E1-042 revision 13, RWB-TE-001 v4, RWB-E1-044 v14-7, RWB-E1-069 SPEC-015, RWB-TE-011 current spec |
| Run decisions checked | D-RUN-07 to D-RUN-13 and D-RUN-18 to D-RUN-21, `AI-SDLC-BUILD-LOG.md` decisions table and timeline. All were taken by the orchestrator (Claude Code, an AI agent); none carries a human approval. Ratification of D-RUN-18..21 is OPEN-050 |
| Sibling specs checked | E1-043 INC-008 revision 10; E1-042 INC-003 revision 13; TE-001 INC-002 v4; E1-044 INC-001 v14-7; E1-069 INC-010; TE-011 INC-006 current (round 12) |
| Excluded | README "Decisions taken while setting this up" items (known, not re-reported) |
| Date | 18 November 2026 |

## Overall status

**STATUS: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 2 |

All eleven round-2 findings (014 to 024) are resolved and verified. No Critical, High or Medium
finding remains. The two new Lows (025, 026) do not automatically block the handoff.

The two Blocker = Yes document gaps (`GAP-E1001-17`, `GAP-E1001-18`) remain exactly as before, on
`ASM-E1001-13` and `ASM-E1001-14`: a **human** ruling is required **before build (the merge of this
story's migration)**. No human ruling has been recorded, and nothing in this review is one.

## Reviewer verification (independent, `python -I`)

The reviewer read Physical Schema v6, PDPA Inventory v4, the story file and the current sibling specs,
and re-ran the counts. The verification script stayed in the session scratchpad and is not written to
the run folder.

| Claim in revision 3 | Result |
|---|---|
| T8: 53 `sys_fields` rows on the four earlier-story tables | **Confirmed.** `parameter_catalog` 15 + `parameter_value` 12 + `reference_version` 22 + `reference_row` 4 = 53; 4 `COMMENT ON TABLE` + 53 `COMMENT ON COLUMN` = 57 comments. `reference_row`'s PS v6 `UNIQUE (row_key)` and `fk_reference_row_version_id` are not carried (E1-043 owns both) |
| 26 PS-v6-only fields DF-REF-274..299 have no PDPA v4 row | **Confirmed**: 26, exactly the five `rule_package`, seventeen `rule_package_version`, three `rule_row` and one `rule_test_case` fields named in `GAP-E1001-18`; all stay `false` |
| `is_personal`: 18 PS v6 `true`, 523 PDPA v4 "Yes", 526 seeded | **Confirmed for the seeded set.** 14 true in both, 4 PS-v6-only, 508 PDPA-only within PS v6. The TSV equals the recomputed set exactly (526 IDs, all present in PS v6). The raw 18 + 523 - 14 = 527 includes `DF-REF-273` `payment_match_rule.approved_by`, whose table D-RCV-36 removes; 526 is correct (see the note below) |
| DP07 system of record is 139 characters; DP04 97 is next | **Confirmed** |
| 9 PS v6 `char(n)` fields: eight `char(64)`, one `char(7)`; DF-REF-301 `char(64)` | **Confirmed**; `character(n)` and `char(n)` both record as `bpchar(n)` |
| 18 ACE link columns `varchar(255)` plus `document_intake.file_name`; 4 FKs target `reference_version` | **Confirmed** (19 `varchar(255)` table columns; FKs at PS v6 lines 2228, 2244, 2245, 2248) |
| LOV-REFRESH `sort_order` DAILY 1, WEEKLY 2, MONTHLY 3, ON_CHANGE 4 (PS v6 5035-5038); seeds 598 / 54 / 421 | **Confirmed** |
| E1-043 revision 10 publishes the SPI, keeps the registry in P3, makes `refdata.columns.<code>` optional, requires two catalog keys, and makes `PARAMETER` a dispatcher branch | **Confirmed in the live text.** SPEC-025: `access.api.ReferenceTableHandler`; registry in `casewf.refdata.internal`; item 4 optional definition with L12 skipped; item 2 two catalog keys; (PARAMETER) is not an SPI handler (SPEC-025, -026, -030; D-RUN-20). SPEC-002/025 item 1: no bean -> 422 MSG-P3-027. SPEC-027: table right reads `rwb.refload.loader.<code>` / `rwb.refload.approver.<code>` through `ParameterService`; missing key refuses. SPEC-031: the `sys_fields` handler is E1-064's and refuses any `is_personal` change |
| Post-TE-001 packages: `casewf.migration.RecoveryFlywayConfig`, `access.api.ApiProblemException`, `access.internal.ApiExceptionHandler` | **Confirmed** against TE-001 v4 SPEC-022 relocation table |
| E1-069 SPEC-015 (a) still says E1-069 flips `RWB_LOAD_REFERENCE_SCHEMA`; (c) still says the version-`0` baseline assertion is replaced | **Confirmed** (E1-069 spec lines 255 and 269); both are named in OPEN-NEW-9 |
| E1-042 revision 13 adds `parameter_value.load_id uuid`, `content_hash char(64)`, `rollback_reason varchar(400)`; `FixedMessageCatalog` is in `access.internal` | **Confirmed** |
| TE-011 still matches fixture fields by (object, field) | **Confirmed in its current spec** (round 12): SPEC-TE011-008 and the scan-class table; the round-4 citation is historical provenance, not a stale contract |
| D-RUN-18..21 are orchestrator decisions, not ratified | **Confirmed**: decisions table rows of 2026-11-18 04:55, 05:10, 05:34 and 05:36, each "orchestrator (Claude Code)"; OPEN-050 is the tech-lead ratification item |

## Round-2 findings: disposition

| Round-2 finding | Severity | Round-3 verdict | Basis |
|---|---|---|---|
| 014 Handler contract contradicts E1-043; `data_product` loads refused | High | **Resolved** | Re-based on E1-043 revision 10. The live text confirms the P4 `access.api.ReferenceTableHandler` (D-RUN-18), the P3 `casewf.refdata` registry, optional `refdata.columns.<code>` (L12 skipped, so K2/K3 keep MSG-P1-003), the two `parameter_catalog` keys supplied here, `PARAMETER` as a dispatcher branch (D-RUN-20), and flag off -> 422 unknown code. SPEC-019 asks E1-043 for nothing. SPEC-012 imports only P4; E1-043 SPEC-019 rule (3) forbids a `dataengine` -> `casewf` edge, and none is created. The earlier "requirement on E1-043" survives only in the historical revision-2 column. AC3 and AC7 to AC11 are reachable and stay COVERED |
| 015 AC9 owner-role text changed | Medium | **Resolved** | K4 `{values}` = "the role codes in LOV-ROLE"; K5 = "DAILY, WEEKLY, MONTHLY, ON_CHANGE"; SPEC-015 quotes both rendered texts; TC-E1-001-09 asserts them verbatim and that no role code is listed to the caller. Story v7 AC9 line 151 matches |
| 016 K0 overlaps K2/K3 | Medium | **Resolved** | K0 split: K0-H (file header: the eight columns, once, in order) and K0-R (the five required columns plus every width); `system_of_record` and `owner_user_id` excluded, their absence is K2/K3 MSG-P1-003; K0 never suppresses K2/K3; TC-E1-001-18 (DP11 no owner) and -19 (DP06 empty system of record) are single-defect cases with MSG-P1-003 as `messageCode` |
| 017 E1-043 asks unanswered; a dictionary load could remove the 526 marks | Medium | **Resolved** | Both E1-043 asks are withdrawn by its revision 10 (`shared-updates.md` section 3 "Withdrawn from revision 2"; section 3.1 item 6: no LOV change, rows to add/remove none). The dictionary handler belongs to RWB-E1-064 (SPEC-031; section 3.2). The guard is placed there: refuse any `is_personal` change, never write the column in `apply` or `onRolledBack`, approver RW-COMPLY (A-36, inferred). This spec states no load can change a mark; the residual direction conflict is `GAP-E1001-23` (No) with OPEN-NEW-7 / -14 |
| 018 57 vs 53 `sys_fields` rows | Low | **Resolved** | 53 in SPEC-002 T8, the revision-delta row, `compliance-validation`, `shared-updates` and the contract file; 4 + 53 = 57 comments. Independently recounted |
| 019 `character(64)` vs `char(64)` | Low | **Resolved** | DF-REF-301 seeded `char(64)`; C3 states the `bpchar(n)` normalisation to `char(n)`; the pass fixture matches `char(64)` to `char(64)`; the nine PS v6 `char` rows pass |
| 020 Blocker gap records incomplete | Low | **Resolved** | All 26 PS-v6-only fields are listed in GAP-18 with DF-REF-288/-289 named, and OPEN-NEW-7 carries the range and both staff-identifier asks. GAP-17 cites Logical Data Model and Data Dictionary v8 line 561 (verified: DF-REF-074, `varchar(120)`) and says a widening must update it. GAP-18 cites PDPA Design v2 line 31 (verified) and explains why the inventory pointer is not a default: it would remove 4 PS v6 marks and has no row for 26 fields, and classification belongs to Compliance (DL26). ASM-E1001-14 states the two fields stay `false` and why |
| 021 F3 is a code value list | Low | **Resolved** | F3 is now `Recovery Workbench`, optionally ` document hub` or `, with Q3`, where Q3 excludes `;`, `(` , `)` and any name of the S list. The three seed texts are examples; the negative cases `Recovery Workbench and ACE` and `Recovery Workbench, with SVAF` are refused. ASM-E1001-09 records the basis; SPEC-017's literal exemption admits only DP01-DP14 and the F1-F3 patterns |
| 022 X8 interim refusal audit unused; GAP-22 evidence wrong | Low | **Resolved** | TC-E1-001-11 asserts one REFUSED `event=REFERENCE_LOAD_AUDIT` line with `operation=LOAD`, `table=data_product`, `outcome=REFUSED`, `messageCode=MSG-P4-002`, `traceId`, no user ID and no personal data (E1-043 SPEC-027 *Refusal*, SPEC-028). GAP-22 now says the interim line exists and that `ApiExceptionHandler` renders the Problem but writes no access log. The persistent access log stays the RWB-E1-039 seam (OPEN-NEW-10) |
| 023 Stale cross-references | Low | **Resolved** | SPEC-012 names the post-TE-001-v4 packages: P1 `dataengine` -> P4 `access.api` (`ReferenceTableHandler`, SPI records, `MessageResolver`, `ApiProblemException`, `ApiError`), no `platform` package; `RecoveryFlywayConfig` is `casewf.migration`; no `casewf` import. E1-042 is revision 13, E1-043 revision 10, E1-044 v14-7, TE-001 v4. E1-069 SPEC-015 (a) and (c) are stated in SPEC-010 and OPEN-NEW-9 |
| 024 Blocker scope and D-RUN status inconsistent | Low | **Resolved** | One statement everywhere: the human ruling is needed **before build (the merge of this story's migration)** and stops nothing earlier (spec Status, CLAR-011/-012, status block, assumptions, GAP-17/-18, `shared-updates` OPEN-NEW-6/-7, `compliance-validation`). D-RUN-07..13 and -18..21 are labelled orchestrator (Claude Code, an AI agent) run decisions, not human rulings; ratification of -18..21 is OPEN-050 and is not claimed |

## Assessment of the two Blocker = Yes gaps

The position is unchanged from round 2 and remains sound.

| Test | GAP-E1001-17 (DP07 width) | GAP-E1001-18 (`is_personal`) |
|---|---|---|
| **Sound** | Yes. The conflict is inside Story v7 section 13: `varchar(120)` in the DDL against a 139-character seed. PS v6 line 820 and Logical Data Model v8 line 561 agree with the DDL but carry an older text. The only shorter wording (Specification Rulings v2 R4, Proposed) contains ";", which BR3, AC7 and F2 treat as two systems. No precedence rule or documented default yields a text that fits and passes BR3 | Yes, conservatively. PS v6 and PDPA v4 disagree on 512 fields. The Design v2 line 31 pointer would let the inventory govern, but it would remove 4 PS v6 marks and has no row for 26 PS v6 fields; classification belongs to Compliance (DL26). Holding the change for a human ruling is protective. The 526 count is correct for the seeded set; the excluded `DF-REF-273` belongs to the removed `payment_match_rule` |
| **Visible** | Yes: spec Status, the ASM table, coverage status `COVERED (ASM)`, CLAR-011, the status block, `shared-updates.md` DG-NEW-1 / OPEN-NEW-6 marked **Blocker**, the contract file | Yes: same places, plus CLAR-012, DG-NEW-2, OPEN-NEW-7 marked **Blocker**, and the impact on E1-016, E1-037, TE-011 and E1-064 named |
| **Protective** | Yes. The business text stays verbatim; widening is non-destructive; the seed-fits unit and IT check guards either outcome; no personal-data impact | Yes. The 526 set is a superset of both sources, never lower; the marks are INSERT literals the TE-011 (object, field) reader parses; no load can change a mark (E1-043 SPEC-031); the 26 unclassified fields and the two staff identifiers are named for the ruling |
| **Human ruling recorded?** | **No** | **No** |

No human ruling may be inferred from this review. The review is an AI gate, not a human disposition.

## New gaps from revision 3

| Local ID | Gap | Blocker? | Evidence and why |
|---|---|---|---|
| `GAP-E1001-23` | E1-064 v7 section 12 says its `DataDictionaryLoader` is "called by the reference data service"; E1-043 revision 10 SPEC-031 has E1-064 register an `access.api.ReferenceTableHandler` that adapts its own loader, and E1-043 never calls P1 code | **No** | E1-064 is BS v6 order 13, after this story; D-RUN-08 makes it a seam. E1-043 revision 10 already assigns the handler to E1-064 and withdraws its earlier request to this story. The direction affects a later story, not this one. Recorded in GAP-23, OPEN-NEW-7 / -14 |
| `GAP-E1001-24` | Story v7 section 12 and section 19 define three handler methods and no rollback; E1-043 revision 10 SPEC-024 provides a generic rollback | **No** | The story is silent, so the SPI default `supportsRollback = false` applies and no behaviour is invented. E1-043 SPEC-024 rule 7 refuses with 409 MSG-P3-027. The consequence (a wrongly approved catalog waits for a later `validFrom`) is recorded for the BA in GAP-24 and OPEN-NEW-15 |

No further gap candidate was found. The revision-3 claim that the 26 PS-v6-only fields stay `false` is
a labelled assumption on a Blocker gap, not a silent default.

## Findings

| ID | Severity | Summary | Maps to |
|---|---|---|---|
| REVIEW-RWB-E1-001-025 | Low | `parameter_catalog` `used_by` names `recovery.dataengine`, but E1-043's P3 `ReferenceLoadAuthority` reads the keys; the spec and contract file state different row shapes | SPEC-019 item 5; `contracts/backend-apis.json`; TC-E1-001-20 |
| REVIEW-RWB-E1-001-026 | Low | K0-H/K0-R and K4/K5 do not state the `{table}` and `{row}` placeholders their MSG v4 texts contain | SPEC-013, SPEC-015, X11, TC-E1-001-09 |

No new gap candidate: `GAP-E1001-23` and `GAP-E1001-24` are already recorded as Blocker = No with
evidence above.

### REVIEW-RWB-E1-001-025: Low. The `parameter_catalog` `used_by` names `recovery.dataengine`, but the reader is E1-043's P3 registry; the contract file states a different row shape

- **Maps to:** SPEC-RWB-E1-001-019 item 5; `contracts/backend-apis.json` `registry_registration.parameter_catalog_rows`; TC-E1-001-20; E1-043 revision 10 SPEC-027.
- **Evidence:** SPEC-019 item 5 says both rows are "used by `recovery.dataengine`". The same spec, in the paragraph after its item table, says "this handler reads no `parameter_catalog` key at runtime (the two rows are seed data consumed by E1-043's registry and authority)". The keys are read by `ReferenceLoadAuthority` in P3 `casewf.refdata` through `ParameterService` (E1-043 SPEC-027: the caller's role must intersect `rwb.refload.loader.<code>` / `rwb.refload.approver.<code>`). PS v6's column comment defines `used_by` as "Modules and stories that read the parameter". The contract file's `parameter_catalog_rows` omits `used_by` and `secret`, while E1-043's `shared-updates.md` section 3.1 item 5 requires `secret=false`. The DDL default covers `secret=false`, but the three artefacts do not state one row shape.
- **Failure scenario:** the catalog records a module that never reads the key and omits the module that does; TC-E1-001-20, written to the stated values, asserts the wrong metadata. No build failure (E1-042's `CatalogCompletenessCheck` only parses the `used_by` grammar), so the defect would survive to the code gate.
- **Remediation:** set `used_by` = `recovery.casewf.refdata` (optionally `(RWB-E1-043)`) in SPEC-019 item 5, state `secret=false` / `value_source=TABLE` in the row shape, align the contract file's `parameter_catalog_rows`, and update TC-E1-001-20 to the same values.

### REVIEW-RWB-E1-001-026: Low. The new checks' placeholder sets do not state `{table}` for MSG-P3-027 or `{row}` for MSG-P1-007

- **Maps to:** SPEC-RWB-E1-001-013 K0-H, K0-R, K4, K5; SPEC-015; X11; TC-E1-001-09; E1-043 revision 10 SPEC-025 L13.
- **Evidence:** MSG v4 line 151 renders MSG-P3-027 as "The {table} load was refused: {check}. The version in force is unchanged." K0-H and K0-R name only `{check}`. MSG v4 line 81 renders MSG-P1-007 as "Row {row}: {field} must be one of {values}." K4 and K5 name `{field}` and `{values}` but not `{row}`. E1-043 SPEC-025 L13 passes "the handler's own message ID and placeholders"; `RowCheckFailure` carries a `row` field, but neither spec says the registry injects it as a placeholder.
- **Failure scenario:** a wrong header or an over-width value renders with an empty or literal `{table}`; a row 4 role failure renders without its row number. The AC9 test written to the story text fails, or is written to a spec text that omits the row, and the structural X11 text is never asserted with a table.
- **Remediation:** state `{table}` = "data_product" in K0-H and K0-R, and `{row}` = the 1-based data row in K4 and K5 (or state that E1-043 fills `{row}` from `RowCheckFailure.row` and `{table}` from the load). Add the exact K0-H/K0-R failure text to the unit-test acceptance criteria and the AC9 text to TC-E1-001-09.

## Verified correct (no finding)

- **Handler contract (014).** The P4 SPI, P3 registry, optional column definition, two catalog keys, `PARAMETER` dispatcher branch, `CURRENT_STATE` dating, `supportsRollback = false`, empty `changeSummary` and flag-off 422 are all in E1-043 revision 10 as cited. The flag-off 404 paths belong to E1-043's own branch flag and its `ParameterHandler` `ObjectProvider`, not this story. No requirement is left on E1-043 and no P1 -> P3 edge is created.
- **T8 (018) and the migration split (D-RUN-12).** 89 tables created, 91 FKs, 111 indexes, 4 `sys_objects` and 53 `sys_fields` carried, 93 / 123 / 1,382 after; the four `reference_version` FKs are carried and the one `reference_row` FK and index are not.
- **`char(n)` (019).** `char(64)` is the PS v6 form and the C3 canonical form; DF-REF-301 is `char(64)`.
- **SOR grammar (021).** All 14 seed texts match exactly one form; the nine negative cases are well chosen. F3 is a grammar, so a catalog reword is not a code release.
- **Audit (022).** The interim E1-043 line is real and the persistent log is correctly left to RWB-E1-039.
- **Packages (023).** Post-TE-001 names are correct; no `platform` reference remains; E1-069's two stale points are named in OPEN-NEW-9.
- **Blocker wording (024).** One "before build (the merge of this story's migration)" statement is used everywhere; D-RUN-18..21 are credited to the orchestrator and marked unratified (OPEN-050).
- **Messages.** AC9 texts are the story's verbatim; the resolver seam is E1-042 revision 13; MSG-P1-003's Thai is correctly labelled Proposed.
- **Test gates.** Frontend `NOT_APPLICABLE` (Story v7 section 15, no screen); backend `REQUIRED` at 80% lines, branches, statements and functions, with pass and fail cases for K0 to K5 and F1 to F3 and separate `recovery-it` integration tests. This meets `implementation-execution-gates.md` for a spec review.
- **No personal data** in any specify artefact. The union TSV holds field IDs and column names only; test owner IDs are random UUIDs.
- **Shared files untouched.** Proposals are in `shared-updates.md`; this review wrote only this file.
- **The 526 count.** The TSV exactly equals PS v6 `true` plus PDPA v4 "Yes" restricted to PS v6 fields. The raw 527 includes `DF-REF-273`, whose `payment_match_rule` table D-RCV-36 removes; the spec's 526 is right. A sentence naming that exclusion in GAP-18 would make the arithmetic transparent, but the count itself is correct.

## Gate checklist

| Check | Result |
|---|---|
| Every requirement traced to a cited source or labelled assumption | PASS (014 resolved; AC9 texts restored; K0/K2/K3 split) |
| No invented requirement | PASS (SOR grammar labelled; F3 a grammar; K0-H/K0-R labelled `ASM-E1001-19`) |
| Authentication and authorization | PASS (E1-043 method checks, loader/approver keys, approver right still `GAP-E1001-08` / OPEN-NEW-2) |
| Customer and account data protection | PASS (526 union verified; 26 unclassified fields named; no load can change a mark; Lows 025/026 are not data-protection findings) |
| Audit logging | PASS (403 + one REFUSED `REFERENCE_LOAD_AUDIT` line; E1-039 seam) |
| Error contract consistency | PASS with Low 026 (`{table}` / `{row}` placeholders) |
| Secrets and environment configuration | PASS (SPEC-010; no secrets) |
| Dependencies only on earlier stories / repo (D-RUN-08) | PASS (E1-043 revision 10 is BS v6 order 8; E1-064 is a later seam) |
| Migration number placeholder (D-RUN-07) | PASS |
| Blocker = Yes gaps sound, visible, protective | PASS (GAP-17, GAP-18; no human ruling) |
| New gaps Blocker = No with evidence | PASS (GAP-23, GAP-24) |
| Unit-test 80% gates planned per surface | PASS |
| Test coverage and evidence planned | PASS except the Low 026 placeholder text |
| No personal data | PASS |

## Blocking statement

STATUS: FAIL. All eleven round-2 findings are resolved and independently verified. No Critical, High
or Medium finding remains. The two Lows (025, 026) are non-blocking and must stay visible for human
disposition.

Independently of this review, `GAP-E1001-17` and `GAP-E1001-18` remain Blocker = Yes on
`ASM-E1001-13` and `ASM-E1001-14`. A human ruling is required before build (the merge of this story's
migration). No AI triage, and no part of this review, is that ruling. No human ruling is recorded.

REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]

