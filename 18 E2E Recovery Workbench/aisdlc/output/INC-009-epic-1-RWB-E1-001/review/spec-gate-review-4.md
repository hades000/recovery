# Spec gate review, round 4: RWB-E1-001 Recovery tables for the 14 data products

| Item | Value |
|---|---|
| RUN_ID | `INC-009-epic-1-RWB-E1-001` |
| Gate | SPEC GATE (Compliance Reviewer, round 4) |
| Reviewed | `specify/spec.md` (revision 4), `assumptions.md`, `document-gaps.md`, `compliance-validation.md`, `shared-updates.md`, `gate-response.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`; against round 3 (`review/spec-gate-review-3.md`, findings 025–026) and the run-3 backups `*.run3.*` |
| Instructions | `.claude/agents/compliance-reviewer.md`; `aisdlc/RUN-BRIEF.md`; repository `AGENTS.md` |
| Precedence applied | D-RCV-35/36, then ADR v3, then Decision Log v10, then story files v7, then older maps and drafts (RUN-BRIEF) |
| Cross-story source of truth | RWB-E1-043 **revision 10** (`INC-008-epic-1-RWB-E1-043/specify/spec.md`), read live at SPEC-025 items 1–4 and L9/L12/L13, SPEC-027 (`ReferenceLoadAuthority`, table-right keys), SPEC-029 (catalog row conventions), SPEC-031, SPEC-032, the SPI records and `shared-updates.md` §3.1 item 5; Message Standard v4 lines 81 and 151; RWB-E1-042 revision 13 §7.1/§7.2; PS v6 lines 1386–1409 and 3164 |
| Run decisions checked | D-RUN-07 to D-RUN-13 and D-RUN-18 to D-RUN-21, `AI-SDLC-BUILD-LOG.md` decisions table. All were taken by the orchestrator (Claude Code, an AI agent); none carries a human approval. Ratification of D-RUN-18..21 is OPEN-050 |
| Sibling specs checked | E1-043 INC-008 revision 10; E1-042 INC-003 revision 13; TE-001 INC-002 v4; E1-044 INC-001 v14-7; E1-069 INC-010; TE-011 INC-006 current |
| Excluded | README "Decisions taken while setting this up" items (known, not re-reported); findings 001–024, re-checked only for reopening |
| Date | 18 November 2026 |

## Overall status

**STATUS: PASS**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

Both round-3 Lows (025, 026) are resolved against the live sources. No earlier finding is reopened.
No design decision, blocker statement or coverage claim changed. No new REVIEW-* ID is raised.

## Round-3 findings: disposition

| Round-3 finding | Severity | Round-4 verdict | Basis |
|---|---|---|---|
| REVIEW-RWB-E1-001-025 `parameter_catalog.used_by` and the row shape | Low | **Resolved** | SPEC-019 item 5 and its "One `parameter_catalog` row shape" paragraph now name `used_by` = `recovery.casewf.refdata (RWB-E1-043)`, state `secret=false` and `value_source=TABLE`, and state that P1 `dataengine` reads neither key at runtime. The live E1-043 revision 10 SPEC-027 puts `ReferenceLoadAuthority` in P3 `casewf.refdata.internal` and has it read `rwb.refload.loader.<code>` / `rwb.refload.approver.<code>` through `ParameterService`, with a missing key or empty value refusing; its SPEC-029 uses the same catalog-row conventions (`BUSINESS`, `GLOBAL`, `required=false`, `secret=false`, `value_source=TABLE`, `used_by` `recovery.casewf.refdata`). One row shape is now in SPEC-019, the contract file and TC-E1-001-20. No P1 reader and no seam exist, so no D-RUN-08 dependency is added |
| REVIEW-RWB-E1-001-026 MSG v4 `{table}` / `{row}` placeholders | Low | **Resolved** | K0-H and K0-R state `{table}` = `data_product`; K4 and K5 state `{row}` = the 1-based data row (header excluded). SPEC-015 quotes both rendered MSG-P3-027 texts and both AC9 texts, X11 states `{table}` = `data_product`, the backend unit-test acceptance criteria assert the four rendered texts, and TC-E1-001-09 asserts `{row}` = 4 and 5. MSG v4 line 151 contains `{table}` and line 81 contains `{row}`; E1-043 revision 10's `RowCheckFailure.row` is the 1-based data row with the header excluded (`0` = whole file), and SPEC-025 L13 passes a handler's own placeholders through unchanged |

## Independent verification against the live sources

| Claim in revision 4 | Result |
|---|---|
| The reader of the two keys is E1-043's P3 `ReferenceLoadAuthority`, not P1 `dataengine` | **Confirmed in the live E1-043 revision 10.** SPEC-027 defines `ReferenceLoadAuthority` (`casewf.refdata.internal`, bean `referenceLoadAuthority`) for every method check and reads the table right from `rwb.refload.loader.<code>` / `rwb.refload.approver.<code>` through `ParameterService`; SPEC-029 lists E1-043's own 38 rows with `used_by` `recovery.casewf.refdata`. No P1 code reads these keys |
| One row shape: `kind=BUSINESS`, `value_type=CODE_LIST`, `scope=GLOBAL`, `required=false`, `owner_role=RW-RISK`, `DEV,SIT,UAT,PROD`, `used_by` as above, `secret=false`, `value_source=TABLE`, `env_property` empty | **Confirmed against E1-043 revision 10 `shared-updates.md` §3.1 item 5** (exactly two rows, CODE_LIST, BUSINESS, GLOBAL, required=false, DEV,SIT,UAT,PROD, `secret=false`, owner RW-RISK) and SPEC-025 item 2 (two keys per handler code, with `RW-REFADM` / `RW-DATASTEW` defaults per its A-40). `CODE_LIST`, `BUSINESS` and `GLOBAL` are valid under E1-042 revision 13 §7.1 and the PS v6 check lists |
| The two fields `value_source` and `env_property` belong in the row shape | **Confirmed as catalog-file fields, not DB columns.** E1-042 revision 13 §7.1 lists the CSV header with `value_source` and `env_property` and marks both "Generated key only (not a DB column)"; §7.2 maps CSV `key` to `param_key`. SPEC-019 cites §7.1 and names `secret` as the PS v6 `parameter_catalog` column, so the shape makes no false schema claim |
| PS v6 supports the DB half of the shape | **Confirmed.** `parameter_catalog` (lines 1386–1409) has `kind`, `value_type`, `unit`, `min_value`, `max_value`, `default_value`, `scope`, `required`, `owner_role`, `environments`, `used_by varchar(400)`, `secret boolean NOT NULL DEFAULT false` and `description varchar(400) NOT NULL`; line 3164 defines `used_by` as "Modules and stories that read the parameter". The value `recovery.casewf.refdata (RWB-E1-043)` parses under E1-042 §7.1 (one `;`-free entry, 36 characters, under 100) and matches the seeded story-qualified convention |
| `parameter_catalog` rows also go in `config/parameter-catalog.csv` and this migration | **Confirmed.** E1-043 revision 10 SPEC-025 item 2 and §3.1 item 5 require the catalog file plus `INSERT ... ON CONFLICT (param_key) DO NOTHING` in the owning story's migration; E1-043 SPEC-029 says the same for its own rows. TC-E1-001-20 now asserts both artefacts to one shape |
| MSG-P3-027 renders `The {table} load was refused: {check}. The version in force is unchanged.` | **Confirmed** at MSG v4 line 151 |
| MSG-P1-007 renders `Row {row}: {field} must be one of {values}.` | **Confirmed** at MSG v4 line 81 |
| `{row}` = 1-based data row, header excluded | **Confirmed** twice: E1-043 revision 10 `RowCheckFailure.row` ("1-based data row (header excluded); `0` means the file as a whole") and Story v7 AC9 line 149, where data row 4 is DP04 and row 5 is DP05 |
| K4/K5 and K0-H/K0-R must supply their own placeholders | **Confirmed.** E1-043 SPEC-025 L13 returns the first failure's `messageCode`, `placeholders` and `field` as given and renders `detail` from every failure; it injects no placeholder of its own |
| The AC9 rendered texts are still Story v7 verbatim | **Confirmed** at Story v7 line 151; revision 4 adds the `{row}` statement, not new text |
| `contracts/backend-apis.json` parses and states the same thing | **Confirmed.** Parsed with Python's `json` with duplicate keys rejected: revision 4, `one_row_shape` matches SPEC-019 item 5, `rows` are the two keys with `RW-REFADM` / `RW-DATASTEW`, and `messages_registered.placeholders` states the same `{table}` / `{row}` values. `contracts/frontend-integrations.json` also parses (`ui_in_scope: NO`) |
| K0-R's example text uses a real over-width column | **Confirmed.** `definition` is `varchar(400)` in SPEC-004, so "value too long for definition" is a valid example of the K0-R `{check}` |

## No design, blocker or coverage statement changed

The full line diff of revision 4 against `spec.run3.md` contains only:

- the Revision, Status, Approval and NEXT_STEP metadata lines;
- the new "Revision 4 changes only the two Low findings" paragraph and its two-row delta table;
- the K0-H, K0-R, K4 and K5 message cells (the two placeholders only);
- the SPEC-015 placeholder paragraph and its two rendered MSG-P3-027 texts;
- the X11 expected column;
- the unit-test acceptance criteria sentence, TC-E1-001-09 and TC-E1-001-20.

No table, column, constraint, seed, view, flag, migration, authority, audit, error-contract, gap or
coverage row changed. The same holds for the other revised files: `assumptions.md` changed only its
header and the two affected rows (`ASM-E1001-06`, `ASM-E1001-19`); `document-gaps.md` only its header;
`compliance-validation.md` its header and the round-3 section; `shared-updates.md` its header and the
trace row 009 status; `gate-response.md` a new round-3 section; `agent-run-log.md` a new run section;
`backend-apis.json` the revision, the `parameter_catalog_rows` object and the two placeholder
statements.

In particular, unchanged and still correct:

- `GAP-E1001-17` and `GAP-E1001-18` stay Blocker = Yes on `ASM-E1001-13` and `ASM-E1001-14`; the
  ruling is still required **before build (the merge of this story's migration)** and no human ruling
  is recorded or claimed;
- CLAR-011 and CLAR-012, the spec Status, `shared-updates` OPEN-NEW-6 / OPEN-NEW-7 and the
  `compliance-validation` statement of the two blockers;
- the AC/BR coverage statuses, the coverage counts (33 rows, 29 unconditional, 3 on assumptions, 1
  NOT_APPLICABLE, 2 contradictions), and the frontend `NOT_APPLICABLE` / backend `REQUIRED` 80% gates.

## Earlier findings: no reopening

| Earlier finding | Round-4 check |
|---|---|
| 014 handler contract | Unchanged and still conformant: P4 `access.api.ReferenceTableHandler`, P3 registry, optional `refdata.columns.data_product`, two catalog keys, `PARAMETER` dispatcher branch, flag-off 422. Adding catalog metadata creates no P1 → P3 import |
| 015 AC9 owner-role text | Unchanged: `{values}` = "the role codes in LOV-ROLE", K5 = the four refresh values, both quoted verbatim; `{row}` is added as a placeholder, not a change to the text |
| 016 K0 split | Unchanged: K0-H/K0-R required set, `system_of_record` and `owner_user_id` excluded, K0 never suppresses K2/K3; TC-18/19 are still single-defect cases |
| 017 dictionary load and `is_personal` | Unchanged: SPEC-006 and SPEC-019 items 3/10 still state that no load can remove a mark and that RWB-E1-064 owns the handler |
| 018 / 019 counts and `char(64)` | Unchanged: 53 `sys_fields` rows, 4 + 53 = 57 comments, `char(64)` for DF-REF-301 |
| 020 blocker gap records | Unchanged: the 26 fields, DF-REF-288/-289, GAP-17's LDM v8 citation and GAP-18's Design v2 citation |
| 021 SOR grammar | Unchanged: F1–F3, with F3 a grammar |
| 022 audit | Unchanged: one REFUSED `event=REFERENCE_LOAD_AUDIT` line in TC-11 and the RWB-E1-039 seam |
| 023 cross-references | Unchanged: post-TE-001 v4 packages, E1-042 rev 13, E1-043 rev 10, E1-044 v14-7, TE-001 v4, E1-069 note |
| 024 blocker scope and D-RUN status | Unchanged: one "before build (the merge of this story's migration)" statement; D-RUN-18..21 remain orchestrator decisions with ratification OPEN-050 |

## Verified correct (no finding)

- **The row shape is one shape, not one shape for the CSV and another for the table.** SPEC-019 says
  `secret` is the PS v6 column and cites E1-042 §7.1 for `value_source` and `env_property`; TC-20
  asserts the shape in the catalog file and the columns that exist after the migration. The contract
  file's `one_row_shape` and `rows` carry the same values.
- **`used_by` names the reader, not the seeder.** RWB-E1-001 inserts both keys but reads neither at
  runtime; E1-043's `ReferenceLoadAuthority` reads both through `ParameterService`. The story suffix
  is the optional form the round-3 review allowed and matches E1-042's seeded convention.
- **K0-H/K0-R render through MSG-P3-027 with `{table}` = `data_product`.** That is the load's table
  code, the same value E1-043 uses for its own MSG-P3-027 checks; the handler supplies it because
  E1-043 passes handler placeholders through unchanged.
- **K4/K5 render row 4 and row 5 for the AC9 fixture.** The story's own "row 4 (DP04), row 5 (DP05)"
  confirms the 1-based data-row convention, so the test texts and `RowCheckFailure.row` agree.
- **Contract file and JSON.** Revision 4 parses with duplicate keys rejected; no dangling references
  to the old `recovery.dataengine` `used_by` remain outside the labelled revision-3 history column.
- **No personal data in the revised artefacts.** The new text contains module and story names, message
  text, catalog field names and synthetic role defaults only; test owner IDs remain random UUIDs.
- **Shared files untouched by this review.** Only this review file is written; the specifier's
  proposals remain in `shared-updates.md` for the orchestrator.

## Gate checklist

| Check | Result |
|---|---|
| Every round-3 finding resolved against the live source | PASS (025, 026) |
| No Critical, High, Medium or Low finding remains | PASS |
| No earlier finding reopened (001–024) | PASS |
| Every requirement traced to a cited source or labelled assumption | PASS (no tracing row changed) |
| No invented requirement | PASS (the two fixes restate the MSG v4 texts and the E1-043 row contract) |
| Authentication and authorization | PASS (E1-043 method checks and access-list keys unchanged; loader/approver keys now attributed to the reader) |
| Customer and account data protection | PASS (526 union unchanged; no load can change a mark; no personal data in the new text) |
| Audit logging | PASS (unchanged: 403 plus one REFUSED audit line; E1-039 seam) |
| Error contract consistency | PASS (MSG-P3-027 and MSG-P1-007 rendered from MSG v4 with the required placeholders; no remap) |
| Secrets and environment configuration | PASS (no secret added; `secret=false` and `value_source=TABLE`; no credential-bearing field) |
| Dependencies only on earlier stories / repo (D-RUN-08) | PASS (E1-043 revision 10 is BS v6 order 8; E1-064 is a later seam; no P1 reader) |
| Migration number placeholder (D-RUN-07) | PASS (unchanged) |
| Blocker = Yes gaps sound, visible, protective | PASS (GAP-17, GAP-18; no human ruling claimed) |
| New gaps Blocker = No with evidence | PASS (GAP-23, GAP-24; no new gap) |
| Frontend / backend applicability | PASS (frontend NOT_APPLICABLE per Story v7 §15; backend REQUIRED) |
| Unit-test 80% gates planned per required surface | PASS (backend planned at 80% lines, branches, statements and functions; frontend N/A) |
| Test coverage and evidence planned | PASS (a pass and a fail case for K0-H/K0-R/K1–K5/F1–F3; TC-09/TC-20 now assert the corrected values) |
| No personal data | PASS |
| Shared files untouched | PASS |

## Blocking statement

STATUS: PASS. The two round-3 Lows are resolved and independently verified against RWB-E1-043
revision 10, Message Standard v4 and Physical Schema v6. No design, blocker or coverage statement
changed; no earlier finding is reopened; no new finding is raised.

Independently of this review, `GAP-E1001-17` and `GAP-E1001-18` remain Blocker = Yes on
`ASM-E1001-13` and `ASM-E1001-14`. A human ruling is required before build (the merge of this story's
migration); no AI triage, and no part of this review, is that ruling. No human ruling is recorded.

SPEC_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
