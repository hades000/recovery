# Spec gate review, round 5: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 5 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 1 `review/spec-gate-review.md` (FAIL, 2 Medium, 5 Low); round 2 `-2.md` (FAIL, 1 Medium, 1 Low); round 3 `-3.md` (FAIL, 2 Low); round 4 `-4.md` (FAIL, 3 Medium, 1 Low: SG4-01..SG4-04) with `document-gaps-4.md` (DG4-01, DG4-02) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..017, revised 18 Nov 2026), `assumptions.md` (ASM-TE011-01..23), `document-gaps.md` (DGL-01..14), `shared-updates.md`, `gate-response.md` (rounds 1–4), `compliance-validation.md`, `contracts/*.json`, `figma/figma_report.md`, `agent-run-log.md`, `evidence/te011_round4_check.py` and `-output.txt`; the `*.run4.*` copies for comparison |
| Context verified | `AI-SDLC-BUILD-LOG.md` §1 D-RUN-07..D-RUN-13 and the RWB-TE-011 triage event 2026-11-18T00:04:03 ("Match by (object, field); reader parses multi-row INSERT and fails closed …; reference-load path (D-RCV-29) is a seam owned by RWB-E1-043 …") |
| Cross-story input | RWB-E1-001 spec under revision (`output/INC-009-epic-1-RWB-E1-001/specify/spec.md`, 18 Nov 00:12; T10, SPEC-006, SPEC-018; `evidence/is_personal_union_v4.tsv`, `pdpa_v4_vs_ps_v6-output.txt`). RWB-E1-043 spec under revision (`output/INC-008-epic-1-RWB-E1-043/specify/spec.md` SPEC-RWB-E1-043-031; `document-gaps.md` GAP-38; `shared-updates.md`; `gate-response.md` §4) |
| Checked against | Physical Schema v6 (`legacy/06-data/recovery-workbench-physical-schema-v6.sql`; repo copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql`, `cmp` identical 18 Nov 2026); Data Classification and Personal Data Inventory v4, sheet Fields; Decision Log v10 D-RCV-29 (line 78); API Specification v4 (`api/recovery-api-v4.yaml`); ACE schema copy `infra/postgres/schema/01-ace-schema-v1.sql`; `AGENTS.md` §4.6; `aisdlc/.github/rules/pdlc.md` |
| Method | Independent scripts in the reviewer scratchpad (`python -I`, print names and counts only): PS v6 `sys_fields` parsed (1,379 rows, 12 columns); E1-001 union (526) joined; name ambiguity, seed-table personal pairs and `source_field` keys recomputed; the 62 tables of the ACE schema copy compared with the dictionary objects and keys; test roots (`backend/src/test`, `frontend/e2e`, `frontend/src/test`, `frontend/src/modules/recovery`, `infra/mock-oidc`, `infra/temporal`) scanned for personal-name assignments; API v4 schemas scanned for personal-named properties with and without `x-personal-data`. `specify/` grepped for e-mail addresses and runs of 9+ digits; contracts parsed as JSON. |
| Date | 2026-11-18 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL** (blocking)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 3 |

All four round-4 findings are resolved in substance, and both round-4 document gaps are recorded with
correct precedence. No round-1, round-2 or round-3 finding has reopened.

One new Medium finding comes from the (object, field) design that resolved SG4-01:

- **SG5-01.** A fixture position whose object *is* resolved, but to an object the dictionary does not
  describe, is never a finding and never a notice. That covers a SQL target table outside the
  dictionary, a JPA `@Table` on such a table, and an API schema type such as `InteractionRequest`.
  Today, this lets a non-`SYN-` `summary` (DF-INT-011) or `file_name` (DF-DOC-049) pass in a typed
  front-end fixture. Under the protective union it also lets ACE `public.address` rows pass. The
  round-4 required fix 1, written by this reviewer, did not cover this case. The spec applied it as
  written.

Three Low findings remain:

- **SG5-02.** The D-RCV-29 seam is named against RWB-E1-043, which hands the lint-visibility part
  back. No owned open item exists.
- **SG5-03.** SQL forms with no named column position are silently skipped.
- **SG5-04.** Small stale or partial statements.

**Cross-story answer.**

- RWB-E1-001's revised spec now meets SPEC-TE011-017:
  - T10: `is_personal` is a literal in each `INSERT … VALUES` row, with no `UPDATE`.
  - SPEC-006: 526 marks, `data_product.owner_user_id` NULL.
  - SPEC-018: an acceptance condition of zero lint findings, "not waived".
- Under (object, field) matching, the 4,274 false positives of SG4-01 do not arise. The reviewer
  confirmed that all six dictionary and reference seed tables are dictionary objects. The only
  personal pair on them is `data_product.owner_user_id`.
- If RWB-E1-001 seeds the union, all 17 Inventory v4 Restricted fields reach the lint's list.
- Neither cross-story input contradicts the SPEC-TE011-001 reader.

## 2. Disposition of round-4 findings and gaps

| Finding | Severity | Disposition | Evidence (checked against the spec, not against `gate-response.md` alone) |
|---|---|---|---|
| SG4-01 Name-only FIXTURE-FIELD would raise 4,274 findings on E1-001's seed | Medium | **Resolved.** Follow-on defect raised as SG5-01 (new, not a reopen). | **Matching.** SPEC-TE011-008 matches by (object, field), with keys `object_name.field_name`, the `<table>.<column>` of `source_field`, and the API schema with its property (SPEC-TE011-001 "Keys"). **Seed tables.** Reviewer recount: the only personal pair on `sys_fields`, `sys_objects`, `data_product`, `lov_value`, `role` and `permission` under the union is `data_product.owner_user_id`. E1-001 SPEC-006 seeds it NULL. Each of the six tables has its own `sys_fields` rows in PS v6 (17 / 7 / 10 / 7 / 5 / 5), so each is a described object. **Required-fix items.** Fix 3 is TS-TE011-01, which asserts 0 findings on seed rows, 1 on a business row, and exit 2 for an allow entry. Fix 4 is SPEC-TE011-016 (states 1–3). Fix 5 is ASM-TE011-12 (allow list not for permanent artefacts) and SPEC-TE011-011 (no entry may match a migration). Fix 6 is the E1-001 note in `shared-updates.md`. Fix 2, the alternative, was not taken; the reviewer accepts that. **Other claims.** The point-in-time dictionary for migrations (ASM-TE011-21) is consistent with `AGENTS.md` §4.6. The claim of 244 `source_field` keys is confirmed. The 4 log calls use no union name (confirmed). |
| SG4-02 D-RCV-29 reference loads are invisible to a files-only lint | Medium | **Resolved in substance.** The residual hand-off is raised as SG5-02 (Low). | The claim is narrowed to "the dictionary as seeded and changed by migrations" in the spec's classification section, SPEC-TE011-001 "API and limits", SPEC-TE011-016 and `contracts/backend-apis.json`. The "no code change" sentences are now conditional on the migration route. OPEN-NEW-TE011-1 tells RW-COMPLY that a reference-load mark is not seen. The residual-risk table is conditional on E1-001. TC-TE-011-05 is scoped to the migration route. The D-RCV-29 coverage row and T8 are added. A configured dictionary source (SPEC-TE011-001 item 3) gives a code-free way to add a committed export. Fix 3's alternative open item to the D-RCV-29 owner was replaced by a seam, per the orchestrator triage. The seam's named owner does not accept the lint part (SG5-02). |
| SG4-03 Reader skips unrecognised `sys_fields` statements | Medium | **Resolved.** | SPEC-TE011-001 now does the following. R1 reads single-row and multi-row `INSERT … VALUES` by column name. R2 reads `UPDATE … SET is_personal … WHERE field_id = / IN (…)`. An explicit ignored class covers statements that cannot change the list. Every other write fails closed (exit 2, file and line, no SQL text). A duplicate `field_id` across migrations fails closed. An `UPDATE` of an unknown `field_id` fails closed. A `true`→`false` change gives a `PDPA-NOTICE` with the field ID only. The unit-scenario table has one fail-closed case per form. **Deviation accepted:** `ON CONFLICT` fails closed instead of being recognised. This is the safer outcome, and E1-001 T10 uses plain literal `INSERT`s. **PS v6 facts confirmed:** `is_personal boolean NOT NULL DEFAULT false` (line 931); `uk_sys_fields UNIQUE (field_id)` (line 944); the only `ALTER` is `ADD CONSTRAINT fk_sys_fields_object_name` (line 2236). Statements naming `sys_fields` are 1,379 INSERT, 1 CREATE TABLE, 1 CREATE VIEW, 1 ALTER, and 1 + 17 COMMENT ON, so the baseline reads cleanly. |
| SG4-04 Residual parts of SG3-01, SG3-02 and round references | Low | **Resolved.** Small residual text items raised as SG5-04. | SPEC-TE011-003 and ASM-TE011-05 record the 2,584 INSERTs and the 18 Nov pattern scan of 0 / 0 / 0 / 0. The reviewer's round-4 rerun gave the same figures. The classification section cites the PS v6 seed descriptions for DF-DOC-049, -052 and -089 and PDPA Design v2 §1 for DF-DOC-077. The status line, `shared-updates.md` §1–§2, the `compliance-validation.md` header and the round-3 heading of `gate-response.md` now point at rounds 4 and 5. |
| DG4-01 (D-RCV-29 versus story §12/§13/§17) | Gap | **Recorded as DGL-13**, Blocker = No | The precedence reasoning is correct. Decision Log v10 outranks story files v7 on the route. Nothing that outranks the story lifts the files-only rule. The gap is a production-coverage question. The citation of D-RCV-29 (Decision Log v10 line 78) was re-verified. |
| DG4-02 (per-entity classification versus name-based rules) | Gap | **Recorded as DGL-14**, Blocker = No | `sys_fields.object_name` and `source_field` give the object. The reviewer confirmed 390 personal names, 71 of them ambiguous. None of the 18 PS v6 names and none of the 9 Restricted names in the residual-risk table is ambiguous. |

**Regression check, rounds 1–3.** No finding has reopened. The following were re-checked:

- SG-01: precondition 2 "Partly met", residual-risk table, 9 Restricted fields.
- SG-02 and DGL-12: `.gitlab/CODEOWNERS` section `[Recovery module]`, V4/V7/V9.
- SG-03: `is_active` fail-safe in SPEC-TE011-001.
- SG-04: self-scan; `infra/postgres/schema/**` is the only `infra` exclusion.
- SG-05: `AGENTS.md` §6.
- SG-06: mobile grouping 3-3-4 / 2-3-4.
- SG-07: A-07 owner proposal §3a.
- SG2-01: Inventory marks 14 of 18; 509 unmarked; "add marks only".
- SG2-02, SG3-01, SG3-02: citations and the PS v6 rationale.

The counts 18 / 14 / 4 / 509 / 523 / 1,366 / 17 / 9 still agree across `spec.md`, DGL-01,
OPEN-NEW-TE011-1 and `gate-response.md`. The coverage table has 31 rows (`TOTAL_RULES: 31`).

The new `true`→`false` rule applies an unmarking with a notice. This is the round-4 fix as required, and
it does not contradict SG2-01. SG2-01 concerned the open item's direction, which still says "add marks
only".

## 3. New findings

### REVIEW-TE011-SG5-01: FIXTURE-FIELD is silently skipped when the object resolves to something the dictionary does not describe (Medium)

- **Affects:** SPEC-TE011-008 (resolution table and "When no object can be resolved"), ASM-TE011-12,
  ASM-TE011-20, SPEC-TE011-016 (state 2 evidence), unit scenarios "Fixture field (-008)", BR3, AC4.
- **Evidence:**
  1. Under SPEC-TE011-008, SQL always resolves its object: the object is the `INSERT`/`UPDATE` target.
     Java and TypeScript resolve the object from a generated entity name, a JPA `@Table(name = …)` or
     an API schema type. The fallback ("unambiguous name → finding; ambiguous → notice") applies only
     when *no* object resolves. A position whose object resolves to a table or schema that has no
     dictionary rows matches no key. It gives neither a finding nor a notice.
  2. **This story's own merge (state 1).** API Specification v4 defines the following unmarked
     properties:

     | Schema and line | Property | Context |
     |---|---|---|
     | `InteractionRequest` (line 8742) | `summary` | Request body of POST "Record a contact, promise or hand-over" |
     | `TimelineItem` (line 8974) | `summary` | — |
     | `AgentOutput` | `summary` | — |
     | `FieldCaptureItem` | `fileName` | — |

     None of these has `x-personal-data`. Their snake-case objects (`interaction_request`,
     `timeline_item`, `agent_output`, `field_capture_item`) are not dictionary objects. `summary`
     (DF-INT-011) and `file_name` (DF-DOC-049) are two of the 18 PS v6 personal names, and both are
     unambiguous. Under SPEC-TE011-008 row 2 (3), a front-end test fixture typed as
     `components["schemas"]["InteractionRequest"]` with a non-`SYN-` `summary` therefore passes
     silently. The round-4 name-based design caught it.
  3. **Any SQL test fixture into a table the dictionary does not describe passes silently.** For
     example, `INSERT INTO it_customer (first_name) VALUES ('<text>')`, although `first_name` is an
     unambiguous PS v6 name.
  4. **Under the protective union (state 2):**
     - 44 of the 62 tables in the ACE schema copy are neither dictionary objects nor `source_field`
       tables.
     - Among them, `address` holds customer address data in its columns `address`, `city`, `county`,
       `country` and `person_key`. ACE `email` is another.
     - The reviewer counted 12 ACE (table, column) pairs that carry an unambiguous union name but match
       no key.
     - A SQL fixture loading ACE-shaped `public.address` rows with real addresses gives no finding and
       no notice. That is the most likely place for real data to enter a fixture, for example the
       ACE-shaped tables of RWB-E1-065 (SRC-15).
  5. The spec's own assurance does not hold for these positions: "This keeps every PS v6 field and
     every Restricted field checked in JSON and test source" (SPEC-TE011-008). Its log-rule rationale
     ("a missed field leaks data, while a false positive costs a source edit or an allow entry",
     SPEC-TE011-004) applies equally here.
  6. The reviewer's round-4 required fix 1 ("a literal is a finding only when `<t>.<column>` equals
     `object_name.field_name`") caused the gap, and the spec applied that fix as written.
- **Required fix:**
  1. Define the set of **described objects**. It contains:
     - every `sys_fields.object_name`;
     - the table part of every `source_field` of the form `<schema>.<table>.<column>`;
     - the snake case of every API schema that has at least one `x-personal-data` property.
  2. In SPEC-TE011-008, treat a position whose resolved object is **not** a described object as
     unresolved. Apply the existing rule: an unambiguous name is a finding, and an ambiguous name gives
     a `PDPA-NOTICE`.
  3. A described object whose (object, field) pair is not a key stays a non-finding.
  4. The six seed tables are described objects, so the 4,274 false positives do not return.
     TS-TE011-01 still holds.
  5. Add unit scenarios for each case:
     - a SQL `INSERT` into an undescribed table with an unambiguous name (finding);
     - the same with an ambiguous name (notice);
     - `@Table(name = "<undescribed>")` with a setter (finding);
     - a TS fixture typed as an API schema without `x-personal-data`, for example `InteractionRequest`
       with `summary` (finding);
     - `INSERT INTO public.address (address)` with a union test dictionary (finding).
  6. Update ASM-TE011-12 and ASM-TE011-20, and restate the state-2 evidence of SPEC-TE011-016. The
     reviewer's scan of today's test roots found no affected assignment outside SQL held in Java
     strings, which is not a SQL position, so the zero-finding baseline is unchanged.
  7. Record the API v4 conflict as a document gap (see `document-gaps-5.md` DG5-01).

### REVIEW-TE011-SG5-02: The D-RCV-29 seam is named against RWB-E1-043, which returns the lint part; no owned open item exists (Low)

- **Affects:** "Personal data classification used" (the paragraph ending "This conflict is recorded as
  DGL-13"); SPEC-TE011-017 row RWB-E1-043; T8; DGL-13 "Why" and "How"; "Out of scope"; `shared-updates.md`
  OPEN-NEW-TE011-1 ("Route") and the RWB-E1-043 note.
- **Evidence:**
  1. **What the TE-011 spec claims.** "RWB-E1-043 owns guarding `is_personal` changes on load; the
     orchestrator has told its remediation to do so" (SPEC-TE011-017).
  2. **What RWB-E1-043 SPEC-RWB-E1-043-031 builds:**
     - a version log;
     - `changeSummary` audit by field ID;
     - non-author approval by the approver list, with RW-COMPLY proposed.
  3. **What it does not build:**
     - It does not refuse removal of a mark ("Not in the sources, so not built here"; open item).
     - It does not take up lint visibility. It records GAP-38 and, in its `shared-updates.md`, proposes
       the row "RWB-TE-011's lint reads the loaded dictionary versions … Owner RWB-TE-011 owner …
       Before the first dictionary load".
     - It places the dictionary handler with RWB-E1-001.
  4. **What RWB-E1-001 does.** Its revised spec registers only the `data_product` handler (D-RUN-11).
     For `sys_objects` and `sys_fields` it says only "Later changes are reference loads (D-RCV-29)".
  5. **Result.** The part that matters to this lint is how an approved load mark reaches the lint, and
     it has no owner:
     - TE-011 declines it (correctly: story §13/§17 and D-RUN-08).
     - E1-043 assigns it to TE-011.
     - The orchestrator will receive two conflicting shared-update rows.
  6. OPEN-NEW-TE011-1 says that otherwise "RW-COMPLY's marks must reach a migration to be enforced by
     the lint". Decision Log v10 D-RCV-29, which outranks the story file, provides no migration route
     for later dictionary changes.
  7. **Why Low and not Medium.** No dictionary load route exists or is specified by any story today.
     The limit is stated in the spec, DGL-13, T8 and SPEC-TE011-016, and the implementation report must
     repeat it. This is the same pattern as round-1 SG-07 (a hand-off with no owner).
- **Required fix:**
  1. State exactly what RWB-E1-043 SPEC-031 delivers and what it leaves open: removal refusal, lint
     visibility, and the dictionary handler. Make that change in SPEC-TE011-017, the classification
     section, DGL-13 and "Out of scope".
  2. Add a proposed open item to `shared-updates.md` §3:
     - **Owner:** to be assigned by the orchestrator, for example the data architect with RW-COMPLY,
       the owners under D-RCV-29 and DL26.
     - **Blocks:** registration of any dictionary load handler, and release readiness.
     - **Decision:** how an approved `is_personal` change reaches the lint. Options:
       - the dictionary handler writes an R1 export that is committed under code owners and read
         through SPEC-TE011-001 item 3;
       - a human-decided exception to D-RCV-29 under which `is_personal` additions go by migration;
       - explicit human acceptance of the residual risk.
  3. Ask the orchestrator to apply this item in place of RWB-E1-043's row "RWB-TE-011's lint reads the
     loaded dictionary versions".
  4. In OPEN-NEW-TE011-1, point the "Route" sentence to the new item instead of directing RW-COMPLY to
     migrations.

### REVIEW-TE011-SG5-03: SQL fixture statements with no named column position are skipped without a finding or notice (Low)

- **Affects:** SPEC-TE011-008 (SQL row), unit scenarios "Fixture field (-008)".
- **Evidence:**
  1. The SQL positions are `INSERT INTO <t> (<cols>) VALUES …`, `INSERT … (<cols>) SELECT …` and
     `UPDATE <t> SET <c> = …`.
  2. The spec says nothing about other SQL forms:
     - an `INSERT INTO <t> VALUES (…)` with no column list;
     - the data rows of `COPY <t> FROM stdin` or psql `\copy`.
  3. These are common shapes for bulk SQL fixtures. They carry personal values in positions the lint
     cannot name, so FIXTURE-FIELD is skipped without trace. Only FIXTURE-ID patterns still apply.
  4. All 2,584 INSERTs of PS v6 use named column lists, and E1-001 T10 keeps them. A stricter rule
     therefore costs nothing at states 1 and 2.
  5. This gap existed in rounds 1–4 and was not raised then.
- **Required fix:**
  1. In scanned SQL, make a column-less `INSERT` into a table, or a `COPY … FROM stdin` / `\copy`
     block, a FIXTURE-FIELD finding with the field shown as `(columns not named)`. Alternatively, give
     at least a `PDPA-NOTICE` without a value.
  2. Add one unit scenario for each form.

### REVIEW-TE011-SG5-04: Small stale or partial statements (Low)

- **Affects:** `compliance-validation.md` §2 check 2; SPEC-TE011-003; `agent-run-log.md` header;
  SPEC-TE011-001 statement classes.
- **Evidence:**
  1. `compliance-validation.md` check 2 still reads "SPEC IDs are unique (`SPEC-TE011-001..016`)". The
     spec now ends at -017.
  2. SPEC-TE011-003 reads "2,584 INSERT statements: 1,379 into `sys_fields`, 1 multi-row into
     `data_product` and 421 `INSERT … SELECT` into `permission`". These three items total 1,801 and
     read as a full breakdown. The other 783 are `sys_objects` 123, `lov_value` 598, `role` 54 and
     `rule_package` 8 (`te011_round4_check-output.txt`).
  3. The `agent-run-log.md` header still gives `SUCCESS_WITH_WARNING`, `REVIEW_GATE_WARNING`,
     "19 assumptions and 8 clarification rows" and a single-day run. The current set has 23
     assumptions and 10 CLARs. Under D-RUN-09, the Low-only warning was not accepted.
  4. SPEC-TE011-001 says that every statement naming `sys_fields` falls into exactly one of three
     classes. A foreign key from another table, `ALTER TABLE <other> … REFERENCES sys_fields`, names
     the table without writing it. None of the three classes lists it. PS v6 has none.
- **Required fix:**
  1. Correct the range to `001..017`.
  2. Say "including" in SPEC-TE011-003, or give all seven tables.
  3. Mark the header of `agent-run-log.md` as the first run, or update it.
  4. Add "a foreign key that references `sys_fields`" to the ignored class.

## 4. Other checks

| Check | Result |
|---|---|
| Personal data in the artefacts | None. There is no e-mail address apart from the code-owner handle `@scb-ace/…`, and no run of 9 or more digits in `specify/`. Synthetic values only: `SYN-LAST-0001`, `TESTNAME`, `RW-DATASTEW`. The evidence script prints no values. |
| Secrets | None. |
| Contracts | `contracts/backend-apis.json` (updated: inputs, exit code 2 cases, notice lines, fixture matching) and `frontend-integrations.json` parse. `NO_API_CHANGE` is consistent with SPEC-TE011-012 and the status matrix. |
| Authorization and audit | Unchanged and appropriate for a build tool. There is no run-time path. Change control is through code owners (SPEC-TE011-014). |
| Unit Test Applicability | Compliant. Front end is `NOT_APPLICABLE` with evidence. The tool back end is `REQUIRED`, with 80% JaCoCo LINE/BRANCH/METHOD/INSTRUCTION. The reader, fixture and allow-list scenarios cover positive, negative, boundary and error paths. SG5-01 and SG5-03 add scenarios. |
| Cross-story consistency | E1-001 T10, SPEC-006 and SPEC-018 match the SPEC-TE011-017 obligations. E1-001 seeds 1,382 `sys_fields` rows: the 1,379 of PS v6 plus the provisional DF-REF-300..302 with `is_personal` false. These are new IDs, so the order rules raise no duplicate. The 526 union IDs are all PS v6 IDs. E1-043 SPEC-031: see SG5-02. |
| Run decisions | D-RUN-07 is applied: there is no fixed migration number, and the placeholder `V<seq>__RWB-E1-001_<name>.sql` is used. D-RUN-08 is applied: there is no dependency on orders 8 or 9. D-RUN-13 is applied by analogy in the reader's quote-aware pass. |
| Data classification (pdlc stop condition) | The classification source, its residual risk and both RWB-E1-001 outcomes are visible. Fixture coverage of undescribed objects (SG5-01) is the open gap. |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 3]
ROUND_4_DISPOSITION: SG4-01 Resolved (follow-on SG5-01); SG4-02 Resolved in substance (residual hand-off SG5-02, Low); SG4-03 Resolved (ON CONFLICT fails closed instead of being recognised: accepted); SG4-04 Resolved (residual text SG5-04)
ROUND_4_GAPS: DG4-01 recorded as DGL-13 (Blocker = No, precedence correct); DG4-02 recorded as DGL-14 (Blocker = No)
ROUND_1_3_DISPOSITION: SG-01..SG-07, SG2-01, SG2-02, SG3-01, SG3-02 remain Resolved; no regression
NEW_FINDINGS: SG5-01 Medium (resolved-but-undescribed fixture objects skipped silently); SG5-02 Low (D-RCV-29 seam has no accepting owner); SG5-03 Low (column-less INSERT / COPY skipped); SG5-04 Low (stale or partial text)
NEW_DOCUMENT_GAPS: DG5-01 (review/document-gaps-5.md), Blocker = No
CROSS_STORY_RWB-E1-001: Consistent. T10 literal INSERT values and 526 marks satisfy SPEC-TE011-017; all 17 Restricted fields reach the lint if the union is seeded; 0 seed-table false positives under (object, field)
CROSS_STORY_RWB-E1-043: SPEC-RWB-E1-043-031 builds audit, version log and approval only, and returns lint visibility to RWB-TE-011 (GAP-38); the conflicting shared-update rows need one owned open item (SG5-02)
BLOCKING: YES (Medium finding SG5-01)
NEXT_STEP: Technical Specifier remediates SG5-01..SG5-04 and records DG5-01, then a round-6 spec gate (review/spec-gate-review-6.md). The orchestrator reconciles the RWB-E1-043 shared-update row on loaded dictionary versions with the open item that SG5-02 asks for. This review does not start the Implementation Planner.
```
