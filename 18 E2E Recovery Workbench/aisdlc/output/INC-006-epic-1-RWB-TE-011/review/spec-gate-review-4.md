# Spec gate review, round 4: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 4 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 1 `review/spec-gate-review.md` (FAIL, 2 Medium, 5 Low); round 2 `-2.md` (FAIL, 1 Medium, 1 Low); round 3 `-3.md` (FAIL, 2 Low: SG3-01, SG3-02) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..016), `assumptions.md` (ASM-TE011-01..19), `document-gaps.md` (DGL-01..12), `shared-updates.md`, `gate-response.md` (rounds 1–3), `compliance-validation.md`, `contracts/*.json` |
| Cross-story input | RWB-E1-001 re-specification in progress, `output/INC-009-epic-1-RWB-E1-001/`: `specify/spec.md` (17 Nov 23:48), `review/spec-gate-review.md` finding REVIEW-RWB-E1-001-002, `specify/evidence/pdpa_v4_vs_ps_v6.py`, `-output.txt` and `is_personal_union_v4.tsv` (17 Nov 23:56, "ASM-E1001-14 (protective union)", 526 fields). RWB-E1-043 spec (`output/INC-008-epic-1-RWB-E1-043/specify/spec.md` SPEC-015). |
| Checked against | Physical Schema v6 (`legacy/06-data/recovery-workbench-physical-schema-v6.sql`; repo copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql`, `cmp` identical 18 Nov 2026); Data Classification and Personal Data Inventory v4, sheet Fields (`legacy/06-data/...-inventory-v4-xlsx.md`); Decision Log v10, D-RCV-29 (`legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` line 78); `AGENTS.md` §4.6; `aisdlc/.github/rules/pdlc.md` |
| Method | Independent script (reviewer scratchpad, `python -I`): all 2,584 `INSERT` statements in PS v6 parsed (single-row, multi-row and `INSERT … SELECT`); `sys_fields` joined to Inventory v4 by BR Field ID; the E1-001 protective union rebuilt (PS v6 `true` OR Inventory "Personal data" = Yes) and compared with E1-001's `is_personal_union_v4.tsv`; every seed-table column name compared with the union's field names; pattern scan of the PS v6 copy for 13-digit runs, the dashed ID form, Thai mobile forms and e-mail addresses. `specify/` grepped for e-mail addresses and runs of 9+ digits; contracts parsed as JSON. |
| Date | 2026-11-18 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL** (blocking)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 1 |

SG3-01 and SG3-02 are resolved in substance. Two small parts of their required fixes were not carried
out, and these are kept as one Low finding (SG4-04). No round-1 or round-2 finding has reopened.

The cross-story check finds three new Medium gaps. Each one comes from how this spec's design behaves
once RWB-E1-001 seeds the dictionary:

- **SG4-01.** Under E1-001's protective classification, FIXTURE-FIELD matches by name across tables
  and would raise 4,274 findings on E1-001's own baseline migration.
- **SG4-02.** Decision Log v10 D-RCV-29 sends later dictionary changes through reference loads, which
  a files-only lint never sees.
- **SG4-03.** The dictionary reader does not fail closed on `sys_fields` statements it does not
  recognise.

**Cross-story answer.** All 17 Inventory v4 Restricted fields have `sys_fields` rows in PS v6. All 17
are in E1-001's 526-field union. If E1-001's V0001 seeds that union as single-row `INSERT`s, this
lint's rule set covers every Restricted field. That condition is not yet guaranteed:

- E1-001's `spec.md` still says BR7 is "Seeded from PS v6 as written" (line 99). ASM-E1001-14 exists
  only in its evidence files.
- The coverage would block E1-001's merge (SG4-01).
- A union applied by bulk `UPDATE` would be skipped silently (SG4-03).
- Any later mark made by reference load is invisible (SG4-02).

Without the union, the 9 Restricted fields listed in the spec stay unchecked. Under D-RCV-29,
OPEN-NEW-TE011-1 then has no route to close that gap.

## 2. Disposition of round-3 findings

| Finding | Severity | Disposition | Evidence (checked independently of `gate-response.md`) |
|---|---|---|---|
| SG3-01 "schema-only" rationale for the PS v6 copy | Low | **Resolved in substance; residual folded into SG4-04.** | SPEC-TE011-003 (spec.md lines 233–236) and ASM-TE011-05 now say the copy "holds reference and dictionary seed INSERTs, including the `sys_fields` seed that is the lint's input", and base the exclusion on its being a read-only copy, the lint's input, and not a fixture. The `gate-response.md` round-2 row now limits "no INSERT (checked)" to the first two files. **Not done:** the required fix also asked for the INSERT count and the 17 Nov pattern-scan result. Neither was added. The reviewer re-ran the scan on 18 Nov 2026: 2,584 `INSERT` statements; 0 runs of 13 digits, 0 dashed IDs, 0 Thai mobile matches, 0 e-mail addresses. The exclusion is therefore safe, but the spec does not record the evidence for it. |
| SG3-02 stale "align" sentence in DGL-01; 3 of 4 Inventory corrections untraced | Low | **Resolved in DGL-01 and OPEN-NEW-TE011-1; residual folded into SG4-04.** | DGL-01's last sentence now reads "reconcile `is_personal` with Inventory v4 by adding marks only". DGL-01 and OPEN-NEW-TE011-1 (c) trace each field. The quotes were verified against PS v6 `sys_fields` lines 4455, 4458 and 4495: DF-DOC-049 "personal where it names a customer"; DF-DOC-052 and DF-DOC-089 "masked by role". DF-DOC-077 traces to PDPA Design v2 §1 "extracted document fields". **Not done:** the required fix said "Apply the same citation to spec.md lines 179–181". spec.md lines 179–181 still justify all 4 fields with PDPA Design v2 §1 alone. |

**Regression check, rounds 1–2.** No finding has reopened. The `.gitlab/CODEOWNERS` entry, section
`[Recovery module]` and validator rules V4/V7/V9 are unchanged and consistent (SPEC-014, DGL-12,
OPEN-NEW-TE011-5). Other items checked:

- `is_active` fail-safe (SPEC-001).
- FIXTURE-ID self-scan (SPEC-003, -009).
- Mobile grouping (SPEC-009, ASM-09).
- `AGENTS.md` §6 citation.
- A-07 owner proposal (§3a).
- The counts 18 / 14 / 4 / 509 / 523 / 1,366 / 17 / 9 still agree across spec.md, DGL-01,
  OPEN-NEW-TE011-1 and `gate-response.md`.
- The coverage table still has 30 rows (`TOTAL_RULES: 30`).

## 3. New findings

### REVIEW-TE011-SG4-01: Under the E1-001 protective classification, FIXTURE-FIELD raises 4,274 findings on E1-001's own baseline migration, and the allow list cannot exempt a merged migration (Medium)

- **Affects:** SPEC-TE011-003 (row "Seeds and migrations"), SPEC-TE011-008, ASM-TE011-12,
  SPEC-TE011-016 ("Done when … zero findings"), SPEC-TE011-011 (allow list).
- **Evidence:**
  1. SPEC-TE011-008 and ASM-TE011-12 match "by field name, not by table … matching by name across
     tables". SPEC-TE011-003 applies FIXTURE-FIELD to
     `backend/src/main/resources/db/modulemigration/recovery/**/*.sql`.
  2. E1-001's evidence `is_personal_union_v4.tsv` (header: "seeded is_personal=true under
     ASM-E1001-14 (protective union)") marks 526 fields. These have 390 distinct field names, and 71 of
     them are also names of non-personal fields. Examples: `status` is Yes on DF-CAS-005
     `recovery_case` and No on DF-SAL-008 `listing`. Others are `amount`, `reason`, `description`,
     `source_system`, `owner_role` and `field_name` (DF-DOC-014).
  3. E1-001 SPEC-RWB-E1-001-006 seeds `sys_fields` (1,379), `sys_objects` (123) and `data_product`
     (14) in V0001. Three column names in those seeds equal personal field names in the union:
     - `sys_fields`: `field_name`, `description` and `source_system`, with 1,379 non-`SYN-` literals
       each.
     - `sys_objects`: `description`, with 123 literals.
     - `data_product`: `owner_role`, with 14 literals (`'RW-DATASTEW'`).

     That gives **4,274 FIXTURE-FIELD findings** in one file.
  4. RWB-TE-011 is build order 6 and E1-001 is build order 9. The `pdpa-lint` job has no `rules:`
     filter (SPEC-013), so E1-001 cannot merge green.
  5. The only escape route the spec gives is an allow-list entry. Such an entry must carry an `expires`
     date (BR6, SPEC-011), but a merged migration can never be edited (`AGENTS.md` §4.6). The entry
     would expire and fail every pipeline again. The likely workarounds are to unmark generic names in
     the dictionary or to use broad `pattern` entries, and either one weakens coverage. Restricted
     fields carry generic names too, for example `comments` (DF-ACE-053, DF-ACE-116).
  6. The same name-only matching applies LOG-FIELD and EXCEPTION to bare identifiers such as
     `status`, `amount`, `reason` and `ruleId`. SPEC-TE011-016 does not say what baseline is expected
     once the dictionary grows.
- **Required fix:**
  1. Scope SQL matching by object. In SQL (`INSERT INTO <t>`, `UPDATE <t>`), a literal is a finding
     only when `<t>.<column>` equals `object_name.field_name` of a personal field. `sys_fields`
     carries `object_name`, so this needs no new source. Keep name-only matching for JSON and
     Java/TS, where the table is unknown, and state that choice.
  2. Alternatively, add a configured exclusion list: dictionary and reference seed tables (`sys_fields`,
     `sys_objects`, `lov_value`, `role`, `permission`, `data_product`) are exempt from FIXTURE-FIELD
     but still scanned by FIXTURE-ID.
  3. Add a system test with a synthetic, E1-001-shaped seed migration and a dictionary that marks
     `description` and `owner_role`. Assert 0 FIXTURE-FIELD findings on the dictionary and reference
     seed rows, and a finding on a business-table row.
  4. Restate SPEC-TE011-016 so that the zero-finding baseline must also hold after E1-001 merges under
     the protective union.
  5. Update ASM-TE011-12's risk text. State that the allow list is not the route for permanent
     artefacts such as merged migrations.
  6. Add a note for the E1-001 specifier in `shared-updates.md`.

### REVIEW-TE011-SG4-02: Decision Log v10 D-RCV-29 makes later dictionary changes reference loads, which the files-only lint cannot see; "picks up any field with no code change" does not hold (Medium)

- **Affects:** "Personal data classification used" (spec.md lines 182–183: "The lint picks up any field
  with no code change once Compliance marks it `is_personal = true`"); OPEN-NEW-TE011-1 ("The lint
  follows the dictionary with no code change"); DGL-01; SPEC-TE011-001; TC-TE-011-05; precondition 2.
- **Evidence:**
  1. Decision Log v10 D-RCV-29 (line 78) reads "Later dictionary changes are reference loads through
     RWB-E1-043". E1-001's spec agrees (line 394: `sys_objects`, `sys_fields` "Later changes are
     reference loads (D-RCV-29)").
  2. RWB-E1-043 SPEC-015 receives a reference load as a multipart upload into the database. It is not
     a repository file.
  3. SPEC-TE011-001 reads only the PS v6 copy, the migration folder and the API specification, and
     "never reads a database" (story §13, §17).
  4. A mark that Compliance adds the D-RCV-29 way therefore never reaches the lint.
  5. TC-TE-011-05 proves AC5 through a migration `UPDATE`, which is not the route D-RCV-29 prescribes.
  6. The PS v6 `LOV-REF-TABLE` seed has 25 codes and none of them is a dictionary code, so even the
     load route is undefined (see `document-gaps-4.md` DG4-01).
  7. Decision Log v10 outranks story files v7 (RUN-BRIEF precedence), and DGL-01 does not consider it.
  8. Consequence: if E1-001 does not seed the protective union in V0001, the 9 Restricted fields in
     the spec's residual-risk table stay unchecked. Closing OPEN-NEW-TE011-1 by the decided route
     would not change that, and the green lint would hide it.
- **Required fix:**
  1. Record the conflict (DG4-01).
  2. State in the spec that marks added by reference load are not visible to the lint.
  3. Specify how they become visible without a database read. Either:
     - add a configured dictionary source in SPEC-TE011-001, such as an approved dictionary load or
       export file committed under code owners, read after the migrations; or
     - raise an open item to the D-RCV-29 owner (recovery tech lead with the data architect) to route
       `is_personal` changes through a migration.
  4. Correct the "no code change" sentences in spec.md and OPEN-NEW-TE011-1. Tell RW-COMPLY in
     OPEN-NEW-TE011-1 that its marks must reach that source.
  5. Make the residual-risk paragraph conditional on E1-001. If V0001 seeds the protective union
     (ASM-E1001-14), items (a) and (b) close at E1-001's merge. Otherwise they stay open until the new
     route exists.

### REVIEW-TE011-SG4-03: The dictionary reader skips `sys_fields` statements it does not recognise, so marks can be lost silently (Medium)

- **Affects:** SPEC-TE011-001, ASM-TE011-03, reader unit scenarios.
- **Evidence:**
  1. SPEC-TE011-001 recognises only two statement forms:
     - `INSERT INTO [${recoverySchema}.]sys_fields (<columns>) VALUES (...)`
     - `UPDATE … SET is_personal = true|false WHERE field_id = '<id>'`
  2. It fails closed only for a missing or unparsable file or an empty union. It does not say what
     happens to other forms that write `sys_fields`, for example:
     - multi-row `VALUES (...), (...)`;
     - `UPDATE … WHERE field_id IN (...)` or `WHERE object_name = …`;
     - `INSERT … ON CONFLICT … DO UPDATE`;
     - `INSERT … SELECT`;
     - `DELETE`.
  3. E1-001 must apply 508 extra marks to PS v6 rows that it otherwise copies "and nothing else"
     (E1-001 SPEC-002). A single `UPDATE … WHERE field_id IN (…)` is a natural way to do it. The lint
     would ignore that statement and keep the 18-field list. The 9 Restricted fields would then stay
     unchecked while the build stays green.
  4. ASM-TE011-03's own rationale ("a silent pass would defeat BR1") applies here.
  5. "A later statement … overrides an earlier one" also lets a later source unmark a field silently,
     although the spec's policy is "add marks, never remove them".
- **Required fix:**
  1. Extend SPEC-TE011-001 to recognise multi-row `VALUES`, `WHERE field_id IN (…)` and
     `ON CONFLICT … DO UPDATE SET is_personal`.
  2. Fail closed (exit 2, file and line only) on any other statement that writes `sys_fields` and
     that the reader cannot interpret.
  3. Print a notice (field ID only) when a later source sets `is_personal = false` for a field that an
     earlier source marked `true`, so that code owners see the unmarking.
  4. Add reader unit scenarios for each form and for the fail-closed path.
  5. Add a note for E1-001 in `shared-updates.md` to keep its seed in a form the lint reads.

### REVIEW-TE011-SG4-04: Residual parts of SG3-01 and SG3-02, and round references (Low)

- **Affects:** SPEC-TE011-003, ASM-TE011-05; spec.md lines 179–181; status line (spec.md line 24);
  `shared-updates.md` §1–§2; `compliance-validation.md` header.
- **Evidence:** See §2. In addition, the status line still says the round-3 fixes were "not
  re-reviewed". `shared-updates.md` §2 names `spec-gate-review-3.md` as the latest round.
- **Required fix:**
  1. Add to SPEC-TE011-003 and ASM-TE011-05: "2,584 INSERT statements; pattern scan 18 Nov 2026: 0
     13-digit, 0 dashed ID, 0 Thai mobile, 0 e-mail".
  2. In spec.md lines 179–181, cite the PS v6 seed descriptions for DF-DOC-049, -052 and -089, as
     DGL-01 does.
  3. Point the status line, `shared-updates.md` and `compliance-validation.md` at round 4, and add a
     round-4 section to `gate-response.md`.

## 4. Other checks

| Check | Result |
|---|---|
| Personal data in the artefacts | None. No e-mail address and no run of 9 or more digits in `specify/`. Synthetic values only (`SYN-LAST-0001`, `TESTNAME`). |
| Secrets | None. |
| Contracts | `contracts/backend-apis.json` and `frontend-integrations.json` parse; unchanged; `NO_API_CHANGE` consistent. |
| Authorization / audit | Unchanged and appropriate for a build tool: no run-time path; change control via code owners (SPEC-014). |
| Unit Test Applicability | Compliant. Front end `NOT_APPLICABLE` with evidence; tool back end `REQUIRED`, 80% JaCoCo LINE/BRANCH/METHOD/INSTRUCTION with positive, negative, boundary and error scenarios. The SG4-01 and SG4-03 fixes add scenarios to this table. |
| Data classification (pdlc stop condition) | Classification source is stated and the residual risk is visible, but the route by which the classification changes later (D-RCV-29) is not handled (SG4-02). |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 3] [LOW: 1]
ROUND_3_DISPOSITION: SG3-01 Resolved in substance; SG3-02 Resolved in substance; residual text items carried as SG4-04 (Low)
ROUND_1_2_DISPOSITION: SG-01..SG-07, SG2-01, SG2-02 remain Resolved; no regression
CROSS_STORY_RWB-E1-001: All 17 Inventory v4 Restricted fields are covered only if E1-001 V0001 seeds the 526-field protective union as rows the reader parses; SG4-01, SG4-02, SG4-03 must be fixed for that to hold and for E1-001 to merge
BLOCKING: YES (Medium findings)
NEXT_STEP: Technical Specifier remediates SG4-01..SG4-04 (and records DG4-01, DG4-02), then a round-5 spec gate. Coordinate SG4-01/SG4-03 notes with the RWB-E1-001 re-specification. This review does not start the Implementation Planner.
```
