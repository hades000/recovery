# Spec gate review, round 6: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 6 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 1 `review/spec-gate-review.md` (FAIL, 2 Medium, 5 Low); round 2 `-2.md` (FAIL, 1 Medium, 1 Low); round 3 `-3.md` (FAIL, 2 Low); round 4 `-4.md` (FAIL, 3 Medium, 1 Low) with `document-gaps-4.md`; round 5 `-5.md` (FAIL, 1 Medium, 3 Low: SG5-01..SG5-04) with `document-gaps-5.md` (DG5-01) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..017, revised 18 Nov 2026 after round 5), `assumptions.md` (ASM-TE011-01..25), `document-gaps.md` (DGL-01..15), `shared-updates.md`, `gate-response.md` (rounds 1–5), `compliance-validation.md`, `contracts/*.json`, `figma/figma_report.md`, `agent-run-log.md`, `evidence/te011_round5_check.py` and `-output.txt`; the `*.run5.*` copies for comparison |
| Context verified | `AI-SDLC-BUILD-LOG.md` §1 D-RUN-07..D-RUN-15 and the RWB-TE-011 triage event 2026-11-18T00:35:10 ("SG5-02 settled: runtime protection of is_personal on a dictionary load is an RWB-E1-064 seam (dictionary handler owner, D-RUN-08); the TE-011 lint covers committed SQL, fixtures and logs only") |
| Cross-story input | RWB-E1-064 story file v1, Story Files v7 (`legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-064-data-dictionary-for-the-14-data-products-v1.md`); RWB-E1-001 spec under revision (`output/INC-009-epic-1-RWB-E1-001/specify/spec.md`, 18 Nov 00:12, HELD by the 00:33 triage); RWB-E1-043 spec revision 3 and `document-gaps.md` GAP-38 (`output/INC-008-epic-1-RWB-E1-043/specify/`, 18 Nov 00:45); for SG6-01 also the RWB-E1-042 spec (`output/INC-003-epic-1-RWB-E1-042/specify/spec.md`, 00:51) and the RWB-TE-003 spec (`output/INC-005-epic-1-RWB-TE-003/specify/spec.md`, 00:53) |
| Checked against | Physical Schema v6 (`legacy/06-data/recovery-workbench-physical-schema-v6.sql`; repo copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql`); API Specification v4 (`api/recovery-api-v4.yaml`); Build Sequence v6 (`aisdlc/docs/increments/build-sequence.md`, orders 1–13); Decision Log v10 D-RCV-29; `AGENTS.md` §4.6; `aisdlc/.github/rules/pdlc.md` |
| Method | Independent script in the reviewer scratchpad (`python -I`, prints names and counts only). One quote-aware pass split the PS v6 copy into 4,070 statements. All 2,584 INSERTs were parsed, including the multi-line `data_product` INSERT and the 421 `INSERT … SELECT` into `permission`. The described pairs, keys and name ambiguity were recomputed for state 1 (PS v6, 18 marks) and state 2 (the E1-001 union, 526 marks). The API v4 properties were recomputed. Every scan root of SPEC-TE011-003 that holds tests, fixtures or infrastructure was scanned: 22 files, which is wider than the specifier's 16. Each was checked for personal-name positions holding a string, number or boolean literal. Flagged lines were read with their values masked. `specify/` was grepped for e-mail addresses and runs of 9 or more digits. The contracts were parsed as JSON. |
| Date | 2026-11-18 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL** (Low findings only)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 4 |

**Round 5.** SG5-01 (Medium) is resolved. SG5-02, SG5-03 and SG5-04 are resolved, and DG5-01 is recorded as DGL-15 with Blocker = No. Each was checked against `spec.md` and the other artefacts themselves, not only against `gate-response.md`. No finding from rounds 1–4 has reopened.

**The orchestrator's round-5 triage is applied soundly:**

- **SG5-01, made per (object, field) pair.** The specifier's deviation is stricter than the reviewer's per-object fix. The reviewer confirmed that it costs nothing on the seed tables: every column of every PS v6 seed INSERT is described on its own table, `rule_package` included, so 0 columns are undescribed. Without it, 20 API properties would be skipped under the union (19 of them with an unambiguous name). The deviation is accepted.
- **SG5-02.** The source supports placing the seam on RWB-E1-064. Its story file v1 defines the `sys_fields` load through POST /admin/reference-loads (flow steps 2–3) and the `DataDictionaryLoader` interface (§12). It lists DF-REF-105 `is_personal` as **Read** (§11). Build Sequence v6 puts the story at order 13, after this story (order 6). D-RUN-08 therefore makes it a seam. The open item OPEN-NEW-TE011-7 is owned (RW-COMPLY), and the lint's claim is limited to committed SQL, fixtures and logs throughout.
- **SG5-03.** It fails closed as a finding, as directed.
- **SG5-04.** The stale text is fixed.
- **DG5-01.** It is recorded with Blocker = No, and the protective reading of `summary` is specified and tested: TS-TE011-04 (b) to (d).

The four new findings are all Low:

- **SG6-01.** The spec's evidence and its "no known file is affected" claim look only at today's tree. Orders 1–5 merge migrations and fixtures before this lint. RWB-E1-042, at order 3, specifies a migration with `INSERT … ON CONFLICT`, `INSERT … SELECT … WHERE NOT EXISTS` and a `DO` block. The spec does not say how the SQL fixture scanner treats those forms, DML inside a dollar-quoted body is skipped without a notice, and a finding in a migration merged before this lint has no remedy.
- **SG6-02.** An exclusion in `pdpa-lint.yaml` can cover the migration folder. That bypasses the "never excused" rule without an owner, a reason, an expiry date or a notice.
- **SG6-03.** Under the per-pair rule, the expected result of TS-TE011-01 depends on dictionary set-up that the test does not state.
- **SG6-04.** Stale cross-story text remains: ASM-TE011-22, the A-07 items that D-RUN-15 superseded, and the request to RWB-E1-043, which revision 3 has already met with its own open item R4.

**Cross-story answer.**

- **RWB-E1-001** (spec of 00:12, held) still meets SPEC-TE011-017 under the per-pair rule:
  - T10 writes `is_personal` as INSERT literals, with no `UPDATE`.
  - SPEC-006 seeds 526 marks.
  - `data_product.owner_user_id` is NULL. It is the only personal pair on the seed tables, and it is a described key.
  - DF-REF-300..302 describe the three `parameter_value` columns that RWB-E1-042 adds, as non-personal.
  - The acceptance condition is zero lint findings, "not waived".
- **RWB-E1-043, revision 3**, has corrected GAP-38 ("nothing asked of RWB-TE-011"). It names the RWB-E1-064 `sys_fields` handler as the place to protect `is_personal`, and it proposes its own open item R4 for RW-COMPLY (SG6-04).
- **RWB-E1-064, story file v1**, matches the specifier's citations: flow steps 2–3, §11 DF-REF-105 Read, BR8, BR9, §12 and order 13. A field that a load adds (its AC4, DF-ACE-204) takes the table default `is_personal = false` and is not visible to the lint. DGL-13 covers this case: the lint sees neither the new row nor any mark on it.

## 2. Disposition of round-5 findings and gap

| Finding | Severity | Disposition | Evidence (checked against the spec, not against `gate-response.md` alone) |
|---|---|---|---|
| SG5-01 Fixture field on an object outside the dictionary gives no finding | Medium | **Resolved.** The per-pair deviation is accepted. A test-precision follow-on is raised as SG6-03 (new, not a reopen). | **Rule.** SPEC-TE011-008 ("Described pairs") resolves a position only when the dictionary describes the pair. A described pair is a `sys_fields` row, a `source_field` `<table>.<column>`, or an `x-personal-data` property. Every other position is unresolved and goes to the name rule. The rule covers the three cases: no object, an object outside the dictionary, and an undescribed field. It is repeated in ASM-TE011-12, ASM-TE011-20, T6 and `contracts/backend-apis.json` "fixtureMatching". **Today's reach.** The reviewer recount gives 4 API properties with a PS v6 personal name on undescribed schemas: `InteractionRequest.summary`, `TimelineItem.summary`, `AgentOutput.summary` and `FieldCaptureItem.fileName`. All four are unambiguous. **Under the union.** The recount gives 390 personal names, 319 of them unambiguous and 71 ambiguous, and 754 keys. 165 API properties with a personal name sit on undescribed schemas. 20 sit on described schemas with no row for their pair (19 unambiguous). A per-object rule would have skipped those 20, so the stricter rule is justified. **Seed tables.** The reviewer parsed all 2,584 PS v6 INSERTs, including the multi-line `data_product` statement and `INSERT … SELECT` into `permission`. 0 columns are undescribed on their own table, on all 7 seeded tables. Under the union, the only personal key on those tables is `data_product.owner_user_id`. TS-TE011-01 therefore holds on the real RWB-E1-001 file. **Required-fix items.** Fix 1 (described set) is applied per pair. Fix 2 (unresolved, then the name rule) is applied. Fix 3 is applied: a described non-personal pair (`listing.status`) gives no finding and no notice (unit scenarios). Fix 4 is applied (SPEC-TE011-008; TS-TE011-01). Fix 5 is applied: TS-TE011-04 (a) to (e), plus unit scenarios for `@Table` on an undescribed table and for an undescribed field on a described object. Fix 6 is applied (ASM-TE011-12 and -20; SPEC-TE011-016 state evidence). Fix 7 is DGL-15. **Baseline.** In state 1 the reviewer's wider scan finds 0 positions with a personal name. In state 2 it finds 0 positions with an unambiguous name and 1 with an ambiguous name: `status` at `frontend/src/modules/recovery/__tests__/render.tsx:23`, a default parameter, which gives a notice and no finding. The specifier's one upper-bound candidate, `final_call` at `RecoveryDatabaseIT.java:110`, sits inside a Java string literal (read with values masked), so it is not a SQL position. The mock-oidc keys (`name`, `sub`, `preferred_username`, `roles`, `aud`) and `email` are not personal names in either state. |
| SG5-02 The D-RCV-29 seam had no owner that accepted it | Low | **Resolved.** The residual stale cross-story text is raised in SG6-04. | **Orchestrator settlement applied:** <br>• RWB-E1-064 owns the dictionary handler, and protecting `is_personal` is its seam. This is stated in the classification section, SPEC-TE011-001 "API and limits", SPEC-TE011-017, T8, the D-RCV-29 coverage row, CLAR-010, "Out of scope", DGL-13 and `contracts/backend-apis.json`. <br>• RW-COMPLY owns OPEN-NEW-TE011-7, with the RWB-E1-064 owner. It lists the round-5 options and blocks registration of a `sys_fields` handler and release readiness. <br>• The spec states exactly what RWB-E1-043 SPEC-031 does and does not deliver. <br>• OPEN-NEW-TE011-1 "Route" now points to OPEN-NEW-TE011-7. <br>• The orchestrator note asks for one item in place of RWB-E1-043's former row. <br>**Source check.** The RWB-E1-064 v1 citations are correct (see §1). **Deviation accepted:** the triage assigned the owner (RW-COMPLY) instead of leaving it to the orchestrator. |
| SG5-03 SQL with no named column is skipped silently | Low | **Resolved.** | **Rule.** SPEC-TE011-008 "Other rules" makes these a PDPA-FIXTURE-FIELD finding with the field `(columns not named)`: a column-less `INSERT … VALUES` or `INSERT … SELECT` holding a literal other than `NULL`/`DEFAULT`, and any `COPY … FROM` or `\copy … from`. `INSERT … DEFAULT VALUES`, a column-less `INSERT … SELECT` with no literal, and `COPY … TO` are not findings. For `sys_fields`, the reader's exit 2 takes precedence. The rule also appears in T9, TS-TE011-05 (a) to (d), the unit scenarios, ASM-TE011-25 and the contract. **Recount.** The PS v6 copy has 0 column-less INSERTs and 0 `COPY` statements, and the scan roots hold no `.sql` file today. The "known files" claim does not yet cover earlier stories (SG6-01). |
| SG5-04 Small stale or partial statements | Low | **Resolved.** | (1) `compliance-validation.md` check 2 reads `SPEC-TE011-001..017`, and check 12 reads DGL-01..15 and ASM-TE011-01..25. (2) SPEC-TE011-003 gives all seven tables: 1,379 / 598 / 421 / 123 / 54 / 8 / 1, 2,584 in all. The reviewer's parse gives the same counts. (3) The `agent-run-log.md` header gives the current status, 25 assumptions, 11 CLARs and both run dates, and marks the first-run `REVIEW_GATE_WARNING` as superseded under D-RUN-09. (4) A foreign key referencing `sys_fields` is in the ignored class, with a unit scenario. The reviewer recount finds 0 such keys in PS v6. |
| DG5-01 API v4 marks `Interaction.summary` but not the request and timeline `summary` | Gap | **Recorded as DGL-15**, Blocker = No | The citations are correct (API v4 lines 7741, 8742, 8974; PS v6 DF-INT-011). The protective reading is specified: unresolved positions with an API personal name in an API-typed position are findings even when the name is ambiguous (SPEC-TE011-002, -008; ASM-TE011-24; CLAR-011). It is tested by TS-TE011-04 (b) to (d). Alignment of the marks is proposed as OPEN-NEW-TE011-8 for the API owner with RW-COMPLY. |

**Regression check, rounds 1–4.** No finding has reopened. The following were re-checked:

- SG-01: precondition 2 is "Partly met"; the residual-risk table lists the 9 Restricted fields.
- SG-02 and DGL-12: `.gitlab/CODEOWNERS` section `[Recovery module]`; validator rules V4, V7 and V9.
- SG-03: the `is_active` fail-safe (SPEC-TE011-001 "Order rules").
- SG-04: the self-scan; `infra/postgres/schema/**` is the only `infra` exclusion.
- SG-05: `AGENTS.md` §6.
- SG-06: mobile grouping 3-3-4 and 2-3-4.
- SG-07: open items for A-07 (now superseded, SG6-04).
- SG2-01: "add marks only"; the counts 14 of 18 and 509.
- SG2-02, SG3-01, SG3-02: citations and the PS v6 rationale.
- SG4-01: (object, field) matching; no allow entry on a migration; point-in-time dictionary.
- SG4-02: claim narrowed.
- SG4-03: the R1/R2 reader, the ignored class, fail closed; `ON CONFLICT` on `sys_fields` fails closed.
- SG4-04: the INSERT breakdown and the pattern scan.

The counts 18 / 14 / 4 / 509 / 523 / 1,366 / 17 / 9 / 526 still agree across `spec.md`, DGL-01, OPEN-NEW-TE011-1 and `gate-response.md`. The coverage table has 31 rows (`TOTAL_RULES: 31`).

## 3. New findings

### REVIEW-TE011-SG6-01: Earlier stories merge SQL before this lint; the scanner's handling of their SQL forms is unspecified, and a finding in an already-merged migration has no remedy (Low)

- **Affects:** SPEC-TE011-008 (SQL position table; "Known files: none is affected"), SPEC-TE011-016 states (1) and (2), ASM-TE011-25 ("no known file is affected"), T3, the unit scenarios "Fixture field (-008)", and `shared-updates.md`, which has notes for RWB-E1-001, -043, -064 and -065 only.
- **Evidence:**
  1. **Build order.** Build Sequence v6 orders RWB-E1-044 (1), RWB-TE-001 (2), RWB-E1-042 (3), RWB-TE-002 (4) and RWB-TE-003 (5) before this story (6). Under D-RUN-06 the orchestrator merges in build order. When this lint first runs on `develop-recovery`, the migration folder and test roots will therefore already hold what those stories merge. The spec's evidence for states (1) and (2) is today's tree (no `.sql` file). State (2) speaks of "files merged between orders 6 and 9", which leaves out orders 1–5.
  2. **RWB-E1-042's migration.** The RWB-E1-042 spec (INC-003, 18 Nov 00:51), migration steps 6–8, specifies:
     - `INSERT ... ON CONFLICT (param_key) DO NOTHING` for the catalog;
     - `INSERT ... SELECT ... WHERE NOT EXISTS` for the value rows;
     - a self-check `DO` block.

     SPEC-RWB-E1-042-006 seeds `parameter_value` with "author = seed identity". `author_user_id` is DF-REF-156, which is personal under the union (Inventory v4 "Staff identifier") and `false` in PS v6. The RWB-E1-043 spec also adds `INSERT ... ON CONFLICT (param_key) DO NOTHING` rows (SPEC-029). RWB-TE-003 (order 5) commits synthetic `ContractFixtures`. Its SPEC-020 requires them to be synthetic but does not require the `SYN-` prefix.
  3. **The scanner's handling is unspecified.** SPEC-TE011-008 lists three SQL position forms. T3 says that a "Source file the lint cannot parse" gives exit 2. The spec does not say what the fixture scanner does with any other SQL statement on a table other than `sys_fields`: DDL, `COMMENT ON`, an `ON CONFLICT` or `RETURNING` tail, or a `WHERE` on `INSERT … SELECT`. Throughout, the spec's stance is to fail closed, and `ON CONFLICT` on `sys_fields` already gives exit 2. A reader of the spec could therefore implement any of these forms as exit 2. No unit scenario pins the behaviour.
  4. **DML inside a dollar-quoted body is skipped silently.** The quote-aware pass of SPEC-TE011-001, which the fixture scanner shares (Backend Specification), treats a `DO $$ … $$` or function body as a string. An `INSERT INTO t (first_name) VALUES ('…')` inside such a body is therefore never a FIXTURE-FIELD position. It gives no finding and no notice, and only FIXTURE-ID applies. For `sys_fields` a `DO` block fails closed, but other tables have no rule. This is the same kind of silent skip that SG5-03 closed for column-less SQL.
  5. **No remedy in a merged migration.** Suppose a migration merged at orders 1–5 holds a FIXTURE-FIELD or FIXTURE-ID finding, or a form read as exit 2. It cannot be edited (`AGENTS.md` §4.6), it cannot carry an allow entry (SPEC-TE011-011), and the point-in-time notice covers only marks added later (SPEC-TE011-008). This story's own merge would then never pass "zero findings". The only escape left is a scan exclusion (SG6-02).
  6. **Why Low.** Under the 18 PS v6 names, RWB-E1-042's seed columns carry no personal name, and the `author_user_id` seed gives only a T7 notice at RWB-E1-001's merge. A reasonable parser tolerates an `ON CONFLICT` tail. The defect is an unverified claim and an unspecified behaviour, not a known failure.
- **Required fix:**
  1. In SPEC-TE011-008, state the fixture scanner's handling of SQL statements that are not positions. They are skipped for FIXTURE-FIELD, never exit 2, and FIXTURE-ID still scans their literals. The `INSERT` position forms accept an `ON CONFLICT … DO NOTHING`/`DO UPDATE` tail, a `RETURNING` tail and a `WHERE` on `INSERT … SELECT`. Add one unit scenario each, on a table other than `sys_fields`.
  2. For DML inside a `DO` block or function body on a scanned table, either read the body for positions or print a `PDPA-NOTICE` with file and line only. Add a unit scenario.
  3. Correct state (2) to "every file merged after the 18 Nov 2026 evidence and before RWB-E1-001 (orders 1–8)". In state (1), require the implementation run to cover the migrations and fixtures of orders 1–5 as merged.
  4. Say what happens if a migration merged before this lint has a finding. For example: this story's merge is blocked, and the orchestrator records a decision. Neither a scan exclusion nor an allow entry may be used. Correct "Known files" in SPEC-TE011-008 and the risk in ASM-TE011-25 accordingly.
  5. In `shared-updates.md`, add a note for the RWB-E1-044 and RWB-E1-042 planners (and RWB-TE-003 for its fixtures). Every `INSERT` names its columns. There is no `COPY`. No seeded value sits in a PS v6 personal pair unless it is `NULL` or `SYN-`. There is no FIXTURE-ID match. Committed fixtures use `SYN-` values in personal positions.

### REVIEW-TE011-SG6-02: A scan exclusion can cover the migration folder, bypassing "the allow list never excuses a migration" with no owner, reason, expiry or notice (Low)

- **Affects:** SPEC-TE011-003 ("Scan roots and exclusions are configuration"), SPEC-TE011-011, SPEC-TE011-015, SPEC-TE011-016 state (2), SPEC-TE011-017 (RWB-E1-001 row), and the configuration validation in the unit scenarios.
- **Evidence:**
  1. The spec makes migrations unexcusable:
     - SPEC-TE011-011: "The allow list never excuses a migration"; any matching entry gives exit 2.
     - SPEC-TE011-016 state (2): "No allow entry may be used for it".
     - SPEC-TE011-017: RWB-E1-001 passes "with no allow-list entry for its migration".
  2. SPEC-TE011-003 and SPEC-TE011-015 put scan roots and exclusions in `pdpa-lint.yaml`. Nothing stops an exclusion glob that covers `backend/src/main/resources/db/modulemigration/recovery/**`, or one migration file. Nothing stops the "Seeds and migrations" root being removed or narrowed.
  3. An exclusion is a permanent, silent excuse:
     - it has no `owner`, `reason` or `expires`;
     - it prints no notice;
     - it leaves no trace in the output.

     That is weaker than the allow-list entry the spec forbids. Code owners review the change (SPEC-TE011-014), but the allow list is reviewed in the same way, and the spec still bars it for migrations.
  4. SG6-01 item 5 makes this route likely: when a merged migration cannot pass, an exclusion is the only working fix.
- **Required fix:**
  1. Add a configuration rule. An exclusion that matches any file in the recovery migration folder, or a scan configuration without that folder as a root, is invalid: exit 2, naming the configuration key.
  2. Print the exclusions in force and the number of files each one excludes in the run output and the CI artifact. Print no paths of personal data and no values.
  3. Add unit scenarios for an exclusion on the migration folder (exit 2) and a missing migration root (exit 2).

### REVIEW-TE011-SG6-03: TS-TE011-01 does not state the dictionary set-up that its zero-finding result now depends on (Low)

- **Affects:** TS-TE011-01, and SPEC-TE011-016 ("the implementation stage … runs the lint on a synthetic, E1-001-shaped migration under a test dictionary").
- **Evidence:**
  1. Under the per-pair rule, a seed-table position is resolved only if the dictionary describes that column on that table. This applies to `sys_fields.description`, `sys_objects.description`, `data_product.owner_role` and the like.
  2. TS-TE011-01 marks `description`, `owner_role`, `field_name` and `source_system` personal on synthetic business objects. It asserts 0 findings on the `sys_fields`, `sys_objects` and `data_product` rows.
  3. Suppose its test dictionary is the synthetic migration alone, with no non-personal rows that describe those seed tables' own columns. Then those columns are undescribed. The four names are then personal on every row that carries them, so they are unambiguous, and every seed row is a finding. The test would fail against a correct implementation.
  4. The test passes only if the dictionary also holds the self-describing rows, from the PS v6 baseline or in the synthetic migration. The spec does not say which. The real RWB-E1-001 file does describe its own columns: the reviewer found 0 undescribed seed columns.
- **Required fix:**
  1. State that the TS-TE011-01 dictionary includes non-personal rows describing every column that the synthetic seed INSERTs use. Either name the PS v6 baseline as the first source, or list the self-describing rows in the synthetic migration.
  2. Add the negative variant. A seed-table column that has no describing row and carries an unambiguous personal name gives one finding. This proves that the per-pair rule also applies to seed tables.

### REVIEW-TE011-SG6-04: Stale text after D-RUN-15 and after RWB-E1-043 revision 3 (Low)

- **Affects:**
  - ASM-TE011-22 (Risk column);
  - spec "Scope decisions on the orchestrator notes" rows A-07 (a) and (b), and "Out of scope";
  - `shared-updates.md` OPEN-NEW-TE011-2, OPEN-NEW-TE011-3, §3a, the note to RWB-E1-043 and the note to the orchestrator;
  - SPEC-TE011-017, RWB-E1-043 row;
  - DGL-13 "How";
  - `compliance-validation.md` §4 row 1.
- **Evidence:**
  1. **ASM-TE011-22** says "RWB-E1-043 guards unmarking on the load route (SPEC-TE011-017)". SPEC-TE011-017 now says that RWB-E1-043 "does not refuse removal of a mark", and that the guard is the RWB-E1-064 seam.
  2. **D-RUN-15** (`AI-SDLC-BUILD-LOG.md` §1, 2026-11-18T00:39) assigns A-07 to RWB-TE-003. It also decides that `X-Correlation-Id` is not built and is recorded as a gap. The RWB-TE-003 spec (00:53) has taken A-07 into scope, citing D-RUN-15. This spec, revised at 00:42, still does the following:
     - It proposes the A-07 owner change (§3a).
     - It proposes OPEN-NEW-TE011-2, with owner "Orchestrator to assign", and OPEN-NEW-TE011-3, "Decide the header and the owning story".
     - It lists "A-07 placed out of scope; open items proposed" as a point for the gate.

     Applied as written, these rows would create open items for questions that are already decided.
  3. **RWB-E1-043 revision 3** (`document-gaps.md`, 00:45) has corrected GAP-38: "nothing asked of RWB-TE-011". It has removed its "lint reads the loaded dictionary versions" row. It proposes its own open item R4 for RW-COMPLY with the data architect: "Decide which governed path may change an `is_personal` mark", blocking RWB-E1-064. It adds a forward note, §3.2, requiring the `sys_fields` handler to refuse any change to `is_personal` and never to write it. This spec still does the following:
     - SPEC-TE011-017 and DGL-13 say that the orchestrator "has told RWB-E1-043 to correct GAP-38 and to point its shared-update row at OPEN-NEW-TE011-7".
     - The note to RWB-E1-043 asks for that replacement.
     - OPEN-NEW-TE011-7 question (1) duplicates R4.

     The orchestrator would receive two open items for the same decision.
- **Required fix:**
  1. Correct the risk text of ASM-TE011-22. The guard is the RWB-E1-064 seam (OPEN-NEW-TE011-7); RWB-E1-043 does not guard.
  2. Cite D-RUN-15 in "Scope decisions" and "Out of scope". Withdraw OPEN-NEW-TE011-2, OPEN-NEW-TE011-3 and §3a, or mark them superseded by D-RUN-15 and RWB-TE-003. Update `compliance-validation.md` §4 to match.
  3. Record that RWB-E1-043 revision 3 has corrected GAP-38. Replace the note to RWB-E1-043 and the note to the orchestrator with a request to merge OPEN-NEW-TE011-7 and RWB-E1-043 R4 into one item owned by RW-COMPLY. The merged item keeps this story's question (2): how an approved change reaches a committed file the lint reads. Align the RWB-E1-064 note with RWB-E1-043's §3.2 forward note: refuse any `is_personal` change and never write it.

## 4. Other checks

| Check | Result |
|---|---|
| Personal data in the artefacts | None found. No e-mail address apart from the code-owner handle `@scb-ace/…`, and no run of 9 or more digits in `specify/`. Only synthetic values are used: `SYN-LAST-0001`, `TESTNAME`, `RW-DATASTEW`. The evidence script prints names and counts only. |
| Secrets | None. |
| Contracts | `contracts/backend-apis.json` and `frontend-integrations.json` parse. "fixtureMatching", `columnsNotNamedField`, the three notice lines and the exit codes match SPEC-TE011-008 and SPEC-TE011-012. `NO_API_CHANGE` is consistent with the status matrix. |
| Authorization and audit | Unchanged and appropriate for a build tool. There is no run-time path. Change control is through code owners (SPEC-TE011-014). SG6-02 is a configuration-validation gap, not an access gap. |
| Unit Test Applicability | Compliant. The front end is `NOT_APPLICABLE` with evidence. The tool back end is `REQUIRED`, with an 80% JaCoCo gate on LINE, BRANCH, METHOD and INSTRUCTION. SG6-01, SG6-02 and SG6-03 add scenarios. |
| Evidence script (`te011_round5_check.py`) | Its figures are reproduced by the reviewer's independent parse. It walks fewer roots (16 files) and matches only string literals. The reviewer's wider scan of 22 files, with number and boolean literals included, gives the same zero-finding result in both states. |
| Run decisions | D-RUN-07 is applied (`V<seq>__…`; no number fixed). D-RUN-08 is applied (seams on RWB-E1-064 and RWB-E1-001 obligations; no dependency on a later story). D-RUN-09 is applied in the run log. D-RUN-13 is applied in the shared quote-aware pass. D-RUN-15 is not yet reflected (SG6-04). |
| Data classification (pdlc stop condition) | The classification source, the residual risk, both RWB-E1-001 outcomes and the load-route limit are visible. No open data-classification blocker belongs to this story. |
| Document gaps | No new document gap. The findings above concern this spec and other runs' specs, not the document set. `review/document-gaps-6.md` is not written. |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
ROUND_5_DISPOSITION: SG5-01 Resolved (per-pair deviation accepted; test-precision follow-on SG6-03); SG5-02 Resolved (orchestrator settlement applied soundly: RWB-E1-064 seam, OPEN-NEW-TE011-7 owned by RW-COMPLY; residual stale cross-story text in SG6-04); SG5-03 Resolved (fail closed as a finding; earlier-story forms in SG6-01); SG5-04 Resolved
ROUND_5_GAPS: DG5-01 recorded as DGL-15 (Blocker = No; unmarked summary properties treated as personal and tested)
ROUND_1_4_DISPOSITION: SG-01..SG-07, SG2-01, SG2-02, SG3-01, SG3-02, SG4-01..SG4-04 remain Resolved; no regression
NEW_FINDINGS: SG6-01 Low (orders 1-5 merge SQL first; SQL forms outside the position list and DML in DO bodies unspecified; no remedy for a finding in a pre-lint migration); SG6-02 Low (scan exclusion can cover the migration folder); SG6-03 Low (TS-TE011-01 dictionary set-up unstated under the per-pair rule); SG6-04 Low (ASM-TE011-22, D-RUN-15 and RWB-E1-043 rev 3 staleness; overlapping open items)
NEW_DOCUMENT_GAPS: none
CROSS_STORY_RWB-E1-001: Consistent under the per-pair rule. T10 literal INSERT values, 526 marks, owner_user_id NULL; 0 undescribed seed columns; DF-REF-300..302 describe parameter_value columns as non-personal
CROSS_STORY_RWB-E1-043: Revision 3 corrected GAP-38 (nothing asked of RWB-TE-011) and proposes open item R4, which overlaps OPEN-NEW-TE011-7 (SG6-04)
CROSS_STORY_RWB-E1-064: Story file v1 confirms the seam: sys_fields load via DataDictionaryLoader, is_personal (DF-REF-105) Read, order 13
BLOCKING: NO (Low findings only, per pdlc.md); under D-RUN-09 the orchestrator does not accept a Low-only failure
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
NEXT_STEP: A human disposition of SG6-01..SG6-04 is required (pdlc.md). Under D-RUN-09 the orchestrator re-runs the Technical Specifier to fix them and requests spec gate round 7 (review/spec-gate-review-7.md), or sends any Low it cannot fix to the engagement lead. The orchestrator should also merge OPEN-NEW-TE011-7 with RWB-E1-043 R4. This review does not start the Implementation Planner.
```
