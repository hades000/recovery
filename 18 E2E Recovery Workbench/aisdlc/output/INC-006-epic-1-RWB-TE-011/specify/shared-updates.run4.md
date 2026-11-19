# Proposed shared-file updates — INC-006-epic-1-RWB-TE-011 (specify)

This stage does not edit shared files (RUN-BRIEF rule 3). The orchestrator applies these rows in order.
Open-item IDs are left for the orchestrator to assign (the latest seen was OPEN-042; other runs work in
parallel).

## 1. `aisdlc/requirement/Traceability_Matrix.md`, row 006

| Field | Current | Proposed |
|---|---|---|
| Story | RWB-TE-011 | unchanged |
| Requirement | BR-RWB-013 / FR-RWB-013 | unchanged; add REQ-RDF-010, REQ-ACA-005, NFR-054 (PDPA part), NFR-045, CTL-11 |
| Spec | No current spec/plan | `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` — SPEC-TE011-001..016 |
| Test cases | — | TC-TE-011-01..11 (TC-11 `BLOCKED` until RWB-TE-002 and OPEN-038) |
| Status | — | Specified; spec gate per the latest round in `review/` (`spec-gate-review.md`, `-2.md`, `-3.md`) |

## 2. `aisdlc/docs/increments/INC-006-epic-1-RWB-TE-011.md`, "Card status"

| Field | Proposed |
|---|---|
| Specification | Done 17 Nov 2026 — `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` |
| Compliance review | Spec gate result from the latest round in `review/` (`spec-gate-review-3.md`) |
| Test cases in story | 11 (TC-TE-011-01..11, Test Cases v7 "Live"); the card's "0" follows Technical Enabler Stories v7 (DGL-02) |

## 3. `aisdlc/docs/open-items.md`, proposed new items

| Proposed ID | Item | Owner | Source | Blocks |
|---|---|---|---|---|
| OPEN-NEW-TE011-1 | Reconcile `sys_fields.is_personal` with Inventory v4 and PDPA Design v2 §1 (which names the Inventory as the field-level inventory), by **adding** marks only. (a) Mark first the 9 Inventory v4 Restricted fields the seed leaves unmarked: DF-ACE-003 `account_name`, DF-ACE-041 `special_memo`, DF-ACE-053 `comments`, DF-ACE-116 `comments`, DF-ACE-060 `deceased_date`, DF-ACE-061 `deceased_flag`, DF-EXT-002 `vulnerable`, DF-EXT-003 `deceased_override`, DF-EXT-004 `bankruptcy`. (b) Then the other Inventory v4 "Yes" fields the seed does not mark (509 in all, including the 9), for example `cif_no`, `contract_no`, `case_no`. (c) Do not unmark DF-DOC-049 `file_name`, DF-DOC-052 `sender_address`, DF-DOC-077 `extracted_fields`, DF-DOC-089 `text_content`: the seed marks them personal, with descriptions "personal where it names a customer" (DF-DOC-049) and "masked by role" (DF-DOC-052, DF-DOC-089), and PDPA Design v2 §1 classes extracted document fields (DF-DOC-077) as direct identifiers; correct their Inventory v4 rows (now "Not personal" / Internal) instead. The lint follows the dictionary with no code change. | RW-COMPLY (DL26) | DGL-01; spec "Personal data classification used" | Not the TE-011 build; release-readiness item, because until it closes the production lint does not cover these fields |
| OPEN-NEW-TE011-2 | `ApiExceptionHandler` logs the raw exception (`log.error(..., ex)`, and the cause on `warn`), so exception text can reach application logs (Audit and Logging Design v2 §6; BS-4.6). Exception text from the persistence layer can carry column values. Not in RWB-TE-011 scope (static build check with no runtime path, story §13). Candidate owner: RWB-TE-003 (INC-005), which already changes `ApiExceptionHandler` under audit A-08; otherwise an `AISDLC-HARDENING` change. | Orchestrator to assign; solution architect / TechX tech leads | Phase 0 audit A-07 (a) | Release readiness (close before release); not the TE-011 build |
| OPEN-NEW-TE011-3 | Correlation ID: no MDC entry and no `X-Correlation-Id` handling. Audit and Logging Design v2 §3 asks for a trace ID end to end; the header is not in API Specification v4. Decide the header and the owning story; candidate owner as for OPEN-NEW-TE011-2. | Orchestrator to assign; solution architect | Phase 0 audit A-07 (b) | Release readiness; not the TE-011 build |
| OPEN-NEW-TE011-4 | Confirm the lint defaults: example e-mail domains, Thai mobile pattern, national ID check-digit algorithm, synthetic prefix `SYN-`. | RW-COMPLY with TechX tech leads | DGL-07; ASM-TE011-08..10 | Nothing; defaults are configuration |
| OPEN-NEW-TE011-5 | RWB-TE-011 adds `/tools/pdpa-lint/ @scb-ace/techx-recovery-tech-leads` to section `[Recovery module]` of `.gitlab/CODEOWNERS` (delivered by RWB-TE-002, SPEC-RWB-TE-002-001), in the same merge as the tool so that validator V9 passes. RWB-TE-002 owners to note it. | TechX tech leads | DGL-12; SPEC-TE011-014 | TC-TE-011-11 (also OPEN-038) |
| OPEN-NEW-TE011-6 | Name and publish the common module's masking helper; then add it to the lint's `maskingHelpers` configuration. | Common module owner | DGL-06; OPEN-024 | Production use of AC8 behaviour |

Note for the RWB-E1-065 specifier (no new open item): RWB-E1-065 BR9 allows a clear identity number in
ACE-shaped tables, which this lint fails under BR4 unless the value is generated at run time or carries
an allow entry (DGL-09).

## 3a. `aisdlc/evidence/phase0-standards-audit.md`, row A-07 (owner change)

Phase 0 audit row A-07 names RWB-TE-011 as owner. This spec puts A-07 out of scope (spec "Scope
decisions on the orchestrator notes"). Proposed: change the A-07 Owner to "RWB-TE-003 (candidate) or
AISDLC-HARDENING; see OPEN-NEW-TE011-2/-3", or record the reassignment in the run README. The PDPA part
of A-09 stays with RWB-TE-011 (SPEC-TE011-013).

## 4. `aisdlc/DOCUMENT-GAPS.md`

Add DGL-01..DGL-12 from `output/INC-006-epic-1-RWB-TE-011/specify/document-gaps.md`, all Blocker = No.

## 5. `aisdlc/docs/increments/INDEX.md`, row 006

Status "Specified"; Spec result from the spec gate.
