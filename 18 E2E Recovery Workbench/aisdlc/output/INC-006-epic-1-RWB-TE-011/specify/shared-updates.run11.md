# Proposed shared-file updates — INC-006-epic-1-RWB-TE-011 (specify)

This stage does not edit shared files (RUN-BRIEF rule 3). The orchestrator applies these rows in order.
Open-item IDs are left for the orchestrator to assign (the latest seen was OPEN-042; other runs work in
parallel).

## 1. `aisdlc/requirement/Traceability_Matrix.md`, row 006

| Field | Current | Proposed |
|---|---|---|
| Story | RWB-TE-011 | unchanged |
| Requirement | BR-RWB-013 / FR-RWB-013 | unchanged; add REQ-RDF-010, REQ-ACA-005, NFR-054 (PDPA part), NFR-045, CTL-11 |
| Spec | No current spec/plan | `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` — SPEC-TE011-001..018 |
| Test cases | — | TC-TE-011-01..11 (TC-11 `BLOCKED` until RWB-TE-002 and OPEN-038) |
| Status | — | Specified; spec gate per the latest round in `review/` (rounds 1–7: `spec-gate-review.md`, `-2.md` … `-7.md`; round 8 `spec-gate-review-8.md`: FAIL, 6 Low; round 9 `spec-gate-review-9.md`: FAIL, 4 Low; round 10 `spec-gate-review-10.md`: FAIL, 3 Low; round 11 `spec-gate-review-11.md` after the round-10 remediation of 18 Nov 2026) |

## 2. `aisdlc/docs/increments/INC-006-epic-1-RWB-TE-011.md`, "Card status"

| Field | Proposed |
|---|---|
| Specification | Done 17 Nov 2026 — `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` |
| Compliance review | Spec gate result from the latest round in `review/` (round 7 `spec-gate-review-7.md`: FAIL, 1 Medium, 3 Low; round 8 `spec-gate-review-8.md`: FAIL, 6 Low; round 9 `spec-gate-review-9.md`: FAIL, 4 Low; round 10 `spec-gate-review-10.md`: FAIL, 3 Low; all remediated 18 Nov 2026; round 11 `spec-gate-review-11.md`) |
| Test cases in story | 11 (TC-TE-011-01..11, Test Cases v7 "Live"); the card's "0" follows Technical Enabler Stories v7 (DGL-02) |

## 3. `aisdlc/docs/open-items.md`, proposed new items

| Proposed ID | Item | Owner | Source | Blocks |
|---|---|---|---|---|
| OPEN-NEW-TE011-1 | Reconcile `sys_fields.is_personal` with Inventory v4 and PDPA Design v2 §1 (which names the Inventory as the field-level inventory), by **adding** marks only. (a) Mark first the 9 Inventory v4 Restricted fields the seed leaves unmarked: DF-ACE-003 `account_name`, DF-ACE-041 `special_memo`, DF-ACE-053 `comments`, DF-ACE-116 `comments`, DF-ACE-060 `deceased_date`, DF-ACE-061 `deceased_flag`, DF-EXT-002 `vulnerable`, DF-EXT-003 `deceased_override`, DF-EXT-004 `bankruptcy`. (b) Then the other Inventory v4 "Yes" fields the seed does not mark (509 in all, including the 9), for example `cif_no`, `contract_no`, `case_no`. (c) Do not unmark DF-DOC-049 `file_name`, DF-DOC-052 `sender_address`, DF-DOC-077 `extracted_fields`, DF-DOC-089 `text_content`: the seed marks them personal, with descriptions "personal where it names a customer" (DF-DOC-049) and "masked by role" (DF-DOC-052, DF-DOC-089), and PDPA Design v2 §1 classes extracted document fields (DF-DOC-077) as direct identifiers; correct their Inventory v4 rows (now "Not personal" / Internal) instead. **Route:** the lint reads committed dictionary rows only (the dictionary as seeded and changed by migrations, plus any configured committed export), with no code change in the lint. A committed row reaches the lint when it uses a recognised form (an `INSERT` row, or `UPDATE … SET is_personal = true WHERE field_id = '<id>'` / `IN (…)`; SPEC-TE011-001). A mark made by a D-RCV-29 dictionary load (RWB-E1-064's handler, through RWB-E1-043's pipeline) changes the database only and is **not** seen by the lint (DGL-13). If RWB-E1-001's baseline migration seeds the protective union (`ASM-E1001-14`, pending the human ruling on `GAP-E1001-18`), items (a) and (b) close at its merge. Otherwise, which governed path may change a mark is decided under RWB-E1-043 open item R4 (owner RW-COMPLY), which also carries how a later mark reaches a committed file the lint reads. | RW-COMPLY (DL26) | DGL-01; spec "Personal data classification used" | Not the TE-011 build; release-readiness item, because until it closes the production lint does not cover these fields |
| OPEN-NEW-TE011-2 | **Withdrawn (superseded by D-RUN-15).** A-07, `ApiExceptionHandler` logging the raw exception text, is assigned to RWB-TE-003, which stops that logging and carries the Problem `traceId`. No open item is needed. | — | Phase 0 audit A-07 (a); D-RUN-15 | — |
| OPEN-NEW-TE011-3 | **Withdrawn (superseded by D-RUN-15).** `X-Correlation-Id` is not built, because no source names it. The orchestrator records it as a document gap. The `traceId` part goes with A-07 to RWB-TE-003. | — | Phase 0 audit A-07 (b); D-RUN-15 | — |
| OPEN-NEW-TE011-4 | Confirm the lint defaults: example e-mail domains, Thai mobile pattern, national ID check-digit algorithm, synthetic prefix `SYN-`. | RW-COMPLY with TechX tech leads | DGL-07; ASM-TE011-08..10 | Nothing; defaults are configuration |
| OPEN-NEW-TE011-5 | RWB-TE-011 adds `/tools/pdpa-lint/ @scb-ace/techx-recovery-tech-leads` to section `[Recovery module]` of `.gitlab/CODEOWNERS` (delivered by RWB-TE-002, SPEC-RWB-TE-002-001), in the same merge as the tool so that validator V9 passes. RWB-TE-002 owners to note it. | TechX tech leads | DGL-12; SPEC-TE011-014 | TC-TE-011-11 (also OPEN-038) |
| OPEN-NEW-TE011-6 | Name and publish the common module's masking helper; then add it to the lint's `maskingHelpers` configuration. | Common module owner | DGL-06; OPEN-024 | Production use of AC8 behaviour |
| OPEN-NEW-TE011-7 | **Withdrawn: merged into RWB-E1-043 open item R4** (owner RW-COMPLY; blocks RWB-E1-064; due before the first dictionary load). R4 decides which governed path may change an `is_personal` mark in `sys_fields`. The orchestrator keeps R4 as the single open item. Please carry this story's question in R4: how an approved `is_personal` change reaches a committed file the lint reads. The options are a committed `INSERT … VALUES` export read through SPEC-TE011-001 item 3, a change by migration as an agreed exception to D-RCV-29, or explicit acceptance of the residual risk. | — | DGL-13; review SG5-02, SG6-04; orchestrator triage 2026-11-18T01:02 | — |
| OPEN-NEW-TE011-8 | Align the `x-personal-data` marks of API Specification v4 with the dictionary: `Interaction.summary` is marked, `InteractionRequest.summary` and `TimelineItem.summary` (and `AgentOutput.summary`) are not, although DF-INT-011 `interaction.summary` is personal. Until aligned, the lint treats them as personal (SPEC-TE011-008). | API owner with RW-COMPLY (DL26) | DGL-15 (review DG5-01) | Nothing; the lint already treats them as personal |

Note for the RWB-E1-001 specifier (no new open item; first raised in the orchestrator's triage
2026-11-18T00:04; spec SPEC-TE011-017):

1. Seed `sys_fields` (including the protective classification of `ASM-E1001-14`) as single-row or
   multi-row `INSERT … VALUES` with literal `field_id`, `object_name`, `field_name` and `is_personal`, with
   `is_personal` set in the row. Do not apply marks with a bulk `UPDATE`, `ON CONFLICT`, `INSERT … SELECT`
   or `COPY`: the lint fails closed on those (SPEC-TE011-001).
2. The merge request must pass `pdpa-lint` with zero findings and with no allow-list entry for the
   migration (entries on a migration are invalid, SPEC-TE011-011). Fixture matching is by (object, field),
   so the dictionary and reference seed columns (`field_name`, `description`, `source_system`,
   `owner_role`) raise nothing; the only personal pair on those six tables under the union is
   `data_product.owner_user_id`, which must stay `NULL` or carry a `SYN-` value.
3. Insert each `field_id` once across all migrations (a duplicate fails the lint closed).

Note for the RWB-E1-043 specifier: none needed. Revision 3 corrected GAP-38 ("nothing asked of
RWB-TE-011"), and its §3.2 item 5 matches this spec: the lint covers committed SQL, fixtures and logs and
is not a run-time check. This stage's OPEN-NEW-TE011-7 is withdrawn in favour of your open item R4.

Note for the RWB-E1-064 specifier (order 13; no new open item): this follows RWB-E1-043 §3.2. Your
`DataDictionaryLoader` is where a load could change `is_personal`. Your story file lists it as Read
(DF-REF-105). `validate` refuses a file whose `is_personal` differs from the value in force (422
MSG-P1-002, "is_personal cannot be changed by a load"), and `apply` and `onRolledBack` never write
`is_personal`. Which governed path may change a mark is decided by RWB-E1-043 open item R4 (RW-COMPLY). If
R4 chooses a committed export, write it as `INSERT INTO sys_fields (…) VALUES (…)` rows with literal
`field_id`, `object_name`, `field_name` and `is_personal`. The lint then reads it as a configured source
with no code change (SPEC-TE011-001 item 3).

Note for the orchestrator: keep the single open item RWB-E1-043 R4. Do not open OPEN-NEW-TE011-7. Add
this story's question to R4, as in the OPEN-NEW-TE011-7 row.

Note for the RWB-E1-065 specifier (no new open item): RWB-E1-065 BR9 allows a clear identity number in
ACE-shaped tables, which this lint fails under BR4 unless the value is generated at run time or carries
an allow entry (DGL-09).

## 3a. `aisdlc/evidence/phase0-standards-audit.md`, row A-07 (owner change)

**Withdrawn (superseded by D-RUN-15).** The orchestrator has already assigned A-07 to RWB-TE-003 and
recorded that `X-Correlation-Id` is not built. No change is proposed here. The PDPA part of A-09 stays
with RWB-TE-011 (SPEC-TE011-013).

## 3b. Note to the planners of build orders 1–5 (RWB-E1-044, RWB-TE-001, RWB-E1-042, RWB-TE-002, RWB-TE-003)

To the orchestrator: please pass rules 1–4 and 6 on to the planners of orders 2–5 (RWB-TE-001,
RWB-E1-042, RWB-TE-002, RWB-TE-003), because every migration and fixture these stories merge is scanned
when RWB-TE-011 merges (order 6; SPEC-TE011-017, -018; review SG6-01, SG7-01, SG7-02). **RWB-E1-044 is
not asked anything** (orchestrator triage 2026-11-18T04:54; review SG8-05). Item 5 is information about
how this lint treats its files, not a request.

1. Every SQL `INSERT` names its columns. Use no `COPY … FROM` or `\copy`, and no `MERGE` or `CALL`.
   Inside a `DO` block, use no `INSERT`, `UPDATE`, `MERGE` or `COPY … FROM`. Use no `EXECUTE` other than a string
   literal, or `format(<string literal>, …)`, whose text is DDL of class 2 in SPEC-TE011-008 (not
   `CREATE TABLE … AS`, `ALTER ROLE`, `ALTER DATABASE` or `ALTER SYSTEM`). Any other statement in a `DO`
   or function body, such as `CALL` or `COPY … FROM`, is a finding. In `format`, use only `%I`
   placeholders, except for the comment text of `COMMENT ON … IS`; any other specifier (`%s`, `%L`, in
   any form such as `%2$L`) elsewhere is a finding, so a check-constraint value is written literally. **To the RWB-E1-042 planner:** write each of the 16 step-3 constraint guards as
   `IF NOT EXISTS (SELECT 1 FROM pg_constraint …) THEN ALTER TABLE … ADD CONSTRAINT …; END IF;`, with the
   DDL run directly, not built by concatenation. The statement forms the lint accepts are listed in
   SPEC-TE011-008 "SQL statement classes". `ON CONFLICT … DO NOTHING`, `RETURNING` and
   `INSERT … SELECT … WHERE NOT EXISTS` are accepted.
2. A value in a pair that Physical Schema v6 marks personal is `NULL` or starts with `SYN-`. Fixtures use
   `SYN-` values in personal positions.
3. No value matches a FIXTURE-ID pattern: a 13-digit number with a valid Thai ID check digit, a Thai
   mobile number, or an e-mail address outside the example domains. Such a value is generated at run time.
4. Once a migration is merged, the only remedy for a finding in it is a corrective migration under the
   same story key (D-RCV-28; `AGENTS.md` §3.7). It takes the next `<seq>`, and its line 2 is
   `-- Fix: <reason>; corrects V<seq>__<…>.sql`. No allow entry and no exclusion can excuse a migration.
5. For information only (RWB-E1-044). Its lint fixtures under `backend/src/test/resources/migration-lint/` are in this lint's
   lint-fixture class. They get FIXTURE-ID only, on the raw text, so their deliberately malformed and
   out-of-class SQL is not parsed and never gives exit 2. RWB-E1-044's Flyway fixtures under
   `backend/src/test/resources/flyway-fixtures/` are test fixtures, checked with every rule. If one of
   them gives a finding at RWB-TE-011's merge, RWB-TE-011's implementation run records it and handles it
   by a reviewed configuration change (SPEC-TE011-003). **Nothing is asked of RWB-E1-044**: this story
   adapts to its specification v14-7 (SPEC-TE011-003; SRC-31).
6. A migration cannot seed a literal into a NOT NULL non-text column that is personal at that point, for
   example `parameter_value.author_user_id` under the protective union. The owner of such a seed raises
   it before planning (DGL-08).

By their specifications, the production SQL of orders 2–5 meets rules 1–4 (order 1 adds none), with RWB-E1-042's step-3
guard form still to be fixed by its planner (rule 1). RWB-E1-044's fixtures are handled by rule 5
(SRC-30, SRC-31; SPEC-TE011-008 "Known files"). This section is a request to the orchestrator; it records
no hand-off. RWB-E1-042's `author_user_id` seed becomes personal under the protective union and then
gives a notice, not a finding (T7).

## 4. `aisdlc/DOCUMENT-GAPS.md`

Add DGL-01..DGL-15 from `output/INC-006-epic-1-RWB-TE-011/specify/document-gaps.md`, all Blocker = No. DGL-13 and DGL-14 are the review's DG4-01 and DG4-02 (`review/document-gaps-4.md`); DGL-15 is DG5-01 (`review/document-gaps-5.md`). Record each once.

## 5. `aisdlc/docs/increments/INDEX.md`, row 006

Status "Specified"; Spec result from the spec gate.
