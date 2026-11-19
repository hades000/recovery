# Proposed shared-file updates — INC-006-epic-1-RWB-TE-011 (specify)

This stage does not edit shared files (RUN-BRIEF rule 3). The orchestrator applies these rows in order.
Open-item IDs are left for the orchestrator to assign (the latest seen was OPEN-042; other runs work in
parallel).

## 1. `aisdlc/requirement/Traceability_Matrix.md`, row 006

| Field | Current | Proposed |
|---|---|---|
| Story | RWB-TE-011 | unchanged |
| Requirement | BR-RWB-013 / FR-RWB-013 | unchanged; add REQ-RDF-010, REQ-ACA-005, NFR-054 (PDPA part), NFR-045, CTL-11 |
| Spec | No current spec/plan | `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` — SPEC-TE011-001..017 |
| Test cases | — | TC-TE-011-01..11 (TC-11 `BLOCKED` until RWB-TE-002 and OPEN-038) |
| Status | — | Specified; spec gate per the latest round in `review/` (rounds 1–5: `spec-gate-review.md`, `-2.md` … `-5.md`; round 6 `spec-gate-review-6.md` after the round-5 remediation of 18 Nov 2026) |

## 2. `aisdlc/docs/increments/INC-006-epic-1-RWB-TE-011.md`, "Card status"

| Field | Proposed |
|---|---|
| Specification | Done 17 Nov 2026 — `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` |
| Compliance review | Spec gate result from the latest round in `review/` (round 5 `spec-gate-review-5.md`: FAIL, 1 Medium, 3 Low, remediated 18 Nov 2026; round 6 `spec-gate-review-6.md`) |
| Test cases in story | 11 (TC-TE-011-01..11, Test Cases v7 "Live"); the card's "0" follows Technical Enabler Stories v7 (DGL-02) |

## 3. `aisdlc/docs/open-items.md`, proposed new items

| Proposed ID | Item | Owner | Source | Blocks |
|---|---|---|---|---|
| OPEN-NEW-TE011-1 | Reconcile `sys_fields.is_personal` with Inventory v4 and PDPA Design v2 §1 (which names the Inventory as the field-level inventory), by **adding** marks only. (a) Mark first the 9 Inventory v4 Restricted fields the seed leaves unmarked: DF-ACE-003 `account_name`, DF-ACE-041 `special_memo`, DF-ACE-053 `comments`, DF-ACE-116 `comments`, DF-ACE-060 `deceased_date`, DF-ACE-061 `deceased_flag`, DF-EXT-002 `vulnerable`, DF-EXT-003 `deceased_override`, DF-EXT-004 `bankruptcy`. (b) Then the other Inventory v4 "Yes" fields the seed does not mark (509 in all, including the 9), for example `cif_no`, `contract_no`, `case_no`. (c) Do not unmark DF-DOC-049 `file_name`, DF-DOC-052 `sender_address`, DF-DOC-077 `extracted_fields`, DF-DOC-089 `text_content`: the seed marks them personal, with descriptions "personal where it names a customer" (DF-DOC-049) and "masked by role" (DF-DOC-052, DF-DOC-089), and PDPA Design v2 §1 classes extracted document fields (DF-DOC-077) as direct identifiers; correct their Inventory v4 rows (now "Not personal" / Internal) instead. **Route:** the lint reads committed dictionary rows only (the dictionary as seeded and changed by migrations, plus any configured committed export), with no code change in the lint. A committed row reaches the lint when it uses a recognised form (an `INSERT` row, or `UPDATE … SET is_personal = true WHERE field_id = '<id>'` / `IN (…)`; SPEC-TE011-001). A mark made by a D-RCV-29 dictionary load (RWB-E1-064's handler, through RWB-E1-043's pipeline) changes the database only and is **not** seen by the lint (DGL-13). If RWB-E1-001's baseline migration seeds the protective union (`ASM-E1001-14`, pending the human ruling on `GAP-E1001-18`), items (a) and (b) close at its merge. Otherwise, how a later mark reaches a committed file the lint reads is decided under OPEN-NEW-TE011-7. | RW-COMPLY (DL26) | DGL-01; spec "Personal data classification used" | Not the TE-011 build; release-readiness item, because until it closes the production lint does not cover these fields |
| OPEN-NEW-TE011-2 | `ApiExceptionHandler` logs the raw exception (`log.error(..., ex)`, and the cause on `warn`), so exception text can reach application logs (Audit and Logging Design v2 §6; BS-4.6). Exception text from the persistence layer can carry column values. Not in RWB-TE-011 scope (static build check with no runtime path, story §13). Candidate owner: RWB-TE-003 (INC-005), which already changes `ApiExceptionHandler` under audit A-08; otherwise an `AISDLC-HARDENING` change. | Orchestrator to assign; solution architect / TechX tech leads | Phase 0 audit A-07 (a) | Release readiness (close before release); not the TE-011 build |
| OPEN-NEW-TE011-3 | Correlation ID: no MDC entry and no `X-Correlation-Id` handling. Audit and Logging Design v2 §3 asks for a trace ID end to end; the header is not in API Specification v4. Decide the header and the owning story; candidate owner as for OPEN-NEW-TE011-2. | Orchestrator to assign; solution architect | Phase 0 audit A-07 (b) | Release readiness; not the TE-011 build |
| OPEN-NEW-TE011-4 | Confirm the lint defaults: example e-mail domains, Thai mobile pattern, national ID check-digit algorithm, synthetic prefix `SYN-`. | RW-COMPLY with TechX tech leads | DGL-07; ASM-TE011-08..10 | Nothing; defaults are configuration |
| OPEN-NEW-TE011-5 | RWB-TE-011 adds `/tools/pdpa-lint/ @scb-ace/techx-recovery-tech-leads` to section `[Recovery module]` of `.gitlab/CODEOWNERS` (delivered by RWB-TE-002, SPEC-RWB-TE-002-001), in the same merge as the tool so that validator V9 passes. RWB-TE-002 owners to note it. | TechX tech leads | DGL-12; SPEC-TE011-014 | TC-TE-011-11 (also OPEN-038) |
| OPEN-NEW-TE011-6 | Name and publish the common module's masking helper; then add it to the lint's `maskingHelpers` configuration. | Common module owner | DGL-06; OPEN-024 | Production use of AC8 behaviour |
| OPEN-NEW-TE011-7 | **Protect `is_personal` marks against a later dictionary load (RWB-E1-064 seam).** Decision Log v10 D-RCV-29 sends later dictionary changes through reference loads. RWB-E1-064 owns the dictionary load handler (`DataDictionaryLoader`; its story file v1 §11 lists `is_personal` DF-REF-105 as Read); RWB-E1-043 provides the load pipeline (version log, change summary by field ID, non-author approval; SPEC-RWB-E1-043-031). The RWB-TE-011 lint covers committed SQL migrations, fixtures and log statements only, and does not police run-time loads (story §13, §17). Decide: (1) whether a dictionary load may change `is_personal` at all, and whether it may remove a mark; (2) how an approved `is_personal` change reaches a committed file the lint reads. Options for (2): the handler writes an `INSERT … VALUES` export committed under code owners and read through SPEC-TE011-001 item 3; `is_personal` changes go by migration as an agreed exception to D-RCV-29; or explicit acceptance of the residual risk. | RW-COMPLY (Compliance, DL26); with the RWB-E1-064 owner (data architect / RW-DATASTEW) | DGL-13; review SG5-02; orchestrator triage 2026-11-18T00:35 | Registration of a `sys_fields` load handler (RWB-E1-064); release readiness. Not the TE-011 build |
| OPEN-NEW-TE011-8 | Align the `x-personal-data` marks of API Specification v4 with the dictionary: `Interaction.summary` is marked, `InteractionRequest.summary` and `TimelineItem.summary` (and `AgentOutput.summary`) are not, although DF-INT-011 `interaction.summary` is personal. Until aligned, the lint treats them as personal (SPEC-TE011-008). | API owner with RW-COMPLY (DL26) | DGL-15 (review DG5-01) | Nothing; the lint already treats them as personal |

Note for the RWB-E1-001 specifier (no new open item; the orchestrator has already passed it on, triage
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

Note for the RWB-E1-043 specifier (no new open item; the orchestrator has already told you, triage
2026-11-18T00:35): RWB-TE-011 (build order 6) does not read loaded dictionary versions. Story §13 and §17
forbid a database read, and D-RUN-08 bars an earlier story from depending on later work. Please correct
GAP-38 and replace your shared-update row "RWB-TE-011's lint reads the loaded dictionary versions" with a
reference to OPEN-NEW-TE011-7. Your SPEC-RWB-E1-043-031 (version log, change summary, approval) stays as
it is; protecting `is_personal` on load is the RWB-E1-064 seam.

Note for the RWB-E1-064 specifier (order 13; no new open item beyond OPEN-NEW-TE011-7): your
`DataDictionaryLoader` is where a load could change `is_personal`. Your story file lists it as Read
(DF-REF-105), so refuse a load row that changes it unless OPEN-NEW-TE011-7 decides otherwise. If the
decision is a committed export, write it as `INSERT INTO sys_fields (…) VALUES (…)` rows with literal
`field_id`, `object_name`, `field_name` and `is_personal`; the lint reads it as a configured source with no
code change (SPEC-TE011-001 item 3).

Note for the orchestrator: the two shared-update rows conflict (RWB-E1-043's "lint reads loaded
versions" and this stage's decline). Apply OPEN-NEW-TE011-7 in place of RWB-E1-043's row.

Note for the RWB-E1-065 specifier (no new open item): RWB-E1-065 BR9 allows a clear identity number in
ACE-shaped tables, which this lint fails under BR4 unless the value is generated at run time or carries
an allow entry (DGL-09).

## 3a. `aisdlc/evidence/phase0-standards-audit.md`, row A-07 (owner change)

Phase 0 audit row A-07 names RWB-TE-011 as owner. This spec puts A-07 out of scope (spec "Scope
decisions on the orchestrator notes"). Proposed: change the A-07 Owner to "RWB-TE-003 (candidate) or
AISDLC-HARDENING; see OPEN-NEW-TE011-2/-3", or record the reassignment in the run README. The PDPA part
of A-09 stays with RWB-TE-011 (SPEC-TE011-013).

## 4. `aisdlc/DOCUMENT-GAPS.md`

Add DGL-01..DGL-15 from `output/INC-006-epic-1-RWB-TE-011/specify/document-gaps.md`, all Blocker = No. DGL-13 and DGL-14 are the review's DG4-01 and DG4-02 (`review/document-gaps-4.md`); DGL-15 is DG5-01 (`review/document-gaps-5.md`). Record each once.

## 5. `aisdlc/docs/increments/INDEX.md`, row 006

Status "Specified"; Spec result from the spec gate.
