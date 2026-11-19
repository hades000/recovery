# Spec gate review, round 3: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 3 (Compliance Reviewer, independent of the author) |
| Round 1 | `review/spec-gate-review.md`: FAIL, 2 Medium, 5 Low. All found Resolved in round 2. Not reopened (no regression found). |
| Round 2 | `review/spec-gate-review-2.md`: FAIL, 1 Medium (SG2-01), 1 Low (SG2-02) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..016), `compliance-validation.md`, `assumptions.md` (ASM-TE011-01..19), `document-gaps.md` (DGL-01..12), `shared-updates.md`, `gate-response.md` (round 2 section), `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `figma/figma_report.md` |
| Checked against | Data Classification and Personal Data Inventory v4, sheet Fields (`legacy/06-data/recovery-workbench-data-classification-and-personal-data-inventory-v4-xlsx.md`); Physical Schema v6, `sys_fields` seed (column `is_personal`) and column comments (repository copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql`); `infra/postgres/schema/01-ace-schema-v1.sql`, `02-ace-tier2-probe.sql`; Personal Data Protection Design v2 (document table "Version 1") §1 (`legacy/10-policy-controls-and-compliance/recovery-workbench-personal-data-protection-design-v2-docx.md`); `AGENTS.md` §4.9; `aisdlc/.github/rules/pdlc.md` |
| Method | Counts recomputed by script, not taken from `gate-response.md`. Inventory v4 Fields sheet parsed row by row (1,366 rows, 1,366 unique IDs). Seed parsed from all 1,379 `INSERT INTO sys_fields` rows; `is_personal` read as the value before `description` (every row matched). Inventory and seed joined on BR Field ID (0 ID-to-name mismatches). The schema folder profiled for `INSERT`, 13-digit runs, Thai mobile and e-mail patterns. `specify/` grepped for e-mail addresses, runs of 9 or more digits and handles. |
| Date | 2026-11-17 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL** (Low findings only; non-blocking)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 2 |

The Medium finding SG2-01 is fixed in substance: the containment claim, the 509 count, the reverse conflict
and the additive-only open item are now correct and verified against the sources. A sentence in DGL-01 still
says the open item is "to align `is_personal` with Inventory v4", and the case for correcting 3 of the 4
Inventory rows is not traced (SG3-02, Low). The SG2-02 edit to the exclusion rationale calls the Physical
Schema v6 copy "schema-only", and `gate-response.md` says each of the three files has "no INSERT (checked)".
The copy holds 2,584 `INSERT` rows, including the `sys_fields` seed that the lint reads (SG3-01, Low).

```text
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
```

## 2. Disposition of round-2 findings

| Round-2 finding | Severity | Disposition | Evidence checked (independently of `gate-response.md`) |
|---|---|---|---|
| SG2-01 Inventory v4 does not mark 4 seed fields; the spec said it did; the open item could remove coverage | Medium | **Partly resolved.** The defect is fixed in substance. What remains is Low, raised as SG3-02. | **Recount.** Inventory v4 Fields sheet: 1,366 rows; "Personal data" = Yes: **523**; Restricted: **17**. Seed `is_personal = true`: **18** (the 18 listed in spec "Resulting list"). Inventory marks **14** of them. DF-DOC-049 `file_name`, DF-DOC-052 `sender_address`, DF-DOC-077 `extracted_fields` and DF-DOC-089 `text_content` are "Not personal" / Internal / No in Inventory v4 (lines 785, 788, 813, 825). Inventory "Yes" fields that the seed does not mark: 523 − 14 = **509**. Of these, 508 are seed rows with `false` and 1 has no seed row (see Observation O-1). The 9 Restricted fields the seed leaves unmarked are exactly the 9 in the spec's residual-risk table, and their categories match (5 Direct identifier, 4 Sensitive). `cif_no` (DF-ACE-055), `contract_no` (DF-ACE-006) and `case_no` (DF-CAS-002) are Inventory "Yes" / Indirect identifier and seed `false`. **Fix point 1** (spec line 148, residual-risk count): done. Line 148 now says "Marks 14 of the 18 seed fields", names the 4 fields and gives 509. Line 177 gives 509. SPEC-TE011-016 uses no count. No "505" or "about" count is left in `specify/`. **Fix point 2** (DGL-01 reverse conflict): mostly done. The 4 rows are named and the fail-safe result is stated. The Physical Schema v6 column comments are not cited, and the rationale traces only `extracted_fields` (SG3-02). **Fix point 3** (OPEN-NEW-TE011-1): done. Marks are added only. Item (c) says "Do not unmark" the 4 fields and asks for their Inventory rows to be corrected. "523 in total against 18 marked" has been removed. A stale "align … with Inventory v4" sentence remains in DGL-01 (SG3-02). **Fix point 4** (`gate-response.md`): done; there is a round-2 section with an SG2-01 row. **PDPA Design v2 §1** quote verified (line 25): "extracted document fields" is Direct identifier / Restricted. |
| SG2-02 Stale gate references and small citation gaps | Low | **Partly resolved.** Points 1 and 2 are resolved. Point 3 was carried out, but the new text misstates one file (SG3-01). | (1) `shared-updates.md` §1 now reads "the latest round in `review/`" and §2 names `spec-gate-review-3.md`. `compliance-validation.md` header lists rounds 1–3 and points to `gate-response.md`. (2) SRC-21 now lists `AGENTS.md` §6. (3) SPEC-TE011-003 and ASM-TE011-05 now name all three files in `infra/postgres/schema/`. `01-ace-schema-v1.sql` has the header "Schema only: no data rows" and 0 `INSERT`. `02-ace-tier2-probe.sql` is DDL only, with 0 `INSERT`. Both are correct. The third file is described as "schema-only", which is wrong (SG3-01). |

Round-1 findings: none regressed. The `.gitlab/CODEOWNERS` / `[Recovery module]` wording, the 9 Restricted
fields, `is_active` fail-safe, the self-scan, the mobile grouping and the A-07 owner proposal are unchanged and
consistent across files.

## 3. New findings

### REVIEW-TE011-SG3-01: The Physical Schema v6 copy is called "schema-only", and `gate-response.md` claims "no INSERT (checked)" (Low)

- **Affects:** SPEC-TE011-003 "Not scanned" (spec.md line 233); ASM-TE011-05; `gate-response.md` round 2,
  row SG2-02.
- **Evidence:**
  1. spec.md line 233 reads "three schema-only files", and ASM-TE011-05 reads "(three schema-only files: …
     the byte-identical Physical Schema v6 copy …)". `gate-response.md` row SG2-02 reads "each is
     schema-only with no INSERT (checked)".
  2. `infra/postgres/schema/03-recovery-physical-schema-v6.sql` has 2,584 `INSERT` statements:
     `sys_fields` 1,379, `lov_value` 598, `permission` 421, `sys_objects` 123, `role` 54,
     `rule_package` 8 and `data_product` 1. Its own header (line 4) reads "… and seed reference data".
     SPEC-TE011-001 itself parses `INSERT INTO sys_fields` rows from this file, so the spec contradicts
     itself.
  3. The exclusion is still sound. The file is a byte-identical copy of a read-only document-set file and
     the dictionary input. On 17 Nov 2026 a scan of it found 0 runs of 13 digits, 0 Thai mobile matches
     and 0 e-mail addresses. Its `INSERT` columns are reference-table columns, not personal field names.
     Only the stated reason is wrong. The claim that it was "checked" is not supported, which matters at a
     bank gate.
- **Required fix:** in SPEC-TE011-003 and ASM-TE011-05, describe the third file as Physical Schema v6, the
  schema plus seed reference data (2,584 `INSERT` rows into `sys_fields`, `lov_value`, `permission`,
  `sys_objects`, `role`, `rule_package` and `data_product`). Say that it is the read-only document-set copy
  and the dictionary input. Base the exclusion on that, and add the 17 Nov 2026 pattern-scan result (no
  13-digit, mobile or e-mail match). Keep "the first two have no INSERT". In `gate-response.md`, correct
  the SG2-02 row: only `01` and `02` are schema-only with no `INSERT`.

### REVIEW-TE011-SG3-02: DGL-01 still says "align `is_personal` with Inventory v4", and the case for correcting 3 of the 4 Inventory rows is untraced (Low)

- **Affects:** `document-gaps.md` DGL-01 (last sentence of "How this stage proceeded"; this text is copied
  into `aisdlc/DOCUMENT-GAPS.md` under `shared-updates.md` §4); spec.md lines 179–181; `shared-updates.md`
  OPEN-NEW-TE011-1 item (c).
- **Evidence:**
  1. DGL-01, "How this stage proceeded", first says "the open item asks Compliance to add marks only and to
     correct those 4 Inventory rows". It then ends: "Open item proposed for Compliance to align
     `is_personal` with Inventory v4 (`shared-updates.md`)". The second sentence repeats the wording that
     SG2-01 flagged, because read literally it would unmark the 4 fields. It contradicts the sentence
     before it. The governing open-item text is now correct, which is why this is Low.
  2. The request to correct the Inventory rows, and the spec's reason for keeping the 4 fields, cite only
     PDPA Design v2 §1 "extracted document fields". That phrase covers DF-DOC-077 `extracted_fields`. It
     does not, on its face, cover `file_name`, `sender_address` or `text_content`. Sources that do support
     these three exist but are not cited. Physical Schema v6 column comments (lines 3286, 3289, 3326):
     "File name as received; personal where it names a customer", "Sender email address for mailbox
     items; masked by role", "OCR text of the page; masked by role on read". The Inventory v4 rows' own
     "Meaning" column has the same text. PDPA Design v2 §1 lists "contact points" as Direct identifier.
     SG2-01 fix point 2 asked DGL-01 to cite the column comments, and it does not.
- **Required fix:**
  1. In DGL-01, replace the last sentence with "Open item proposed for Compliance to add marks from
     Inventory v4 and to correct the 4 Inventory rows (`shared-updates.md` OPEN-NEW-TE011-1)", or delete it.
  2. In DGL-01 and OPEN-NEW-TE011-1 (c), trace each of the 4 fields. `extracted_fields`: PDPA Design v2 §1
     "extracted document fields". `sender_address`: column comment "masked by role", and PDPA Design v2 §1
     "contact points", if the specifier holds that a sender address is a contact point; otherwise label it
     as an assumption. `text_content` and `file_name`: the Physical Schema v6 column comments quoted above,
     which match the Inventory's own Meaning text. Where no source settles a field, label the request as an
     assumption (ASM-TE011-nn) for RW-COMPLY to decide. Apply the same citation to spec.md lines 179–181.

## 4. Regression checks on the round-2 edits

| Check | Result |
|---|---|
| Untraced statements introduced | Two, SG3-01 ("schema-only", "no INSERT (checked)") and SG3-02 (the reason for 3 of the 4 Inventory corrections). All other new text traces: the 14/18, 509, 523, 17 and 9 counts, the 4 field IDs, their Inventory classifications and the PDPA Design v2 §1 quote were all re-derived from source. |
| Invented requirements | None. The additive-only instruction and "do not unmark" are a fail-safe reading of the story contract (story file v1 §12; BR1, AC5), with classification left to DL26. No new lint rule, scan root or behaviour was added. |
| Numbers consistent across files | Yes. 18, 14, 4, 509, 523, 1,366, 17 and 9 agree across spec.md, DGL-01, OPEN-NEW-TE011-1 and `gate-response.md`. The coverage table has 30 rows, matching `TOTAL_RULES: 30`. ASM-TE011-01..19 and DGL-01..12 are consistent between the files that cite them. |
| Stale references | One stale sentence in DGL-01 (SG3-02). Spec status line, `shared-updates.md` §1–§2 and the `compliance-validation.md` header name the current round. |
| Contracts and design evidence | `contracts/backend-apis.json` and `frontend-integrations.json` parse as JSON, are unchanged and match SPEC-TE011-001, -002, -011, -012 and -013. `figma_report.md` is `NOT_REQUIRED` and still correct. |
| Personal data in the artefacts | None. No e-mail address, no run of 9 or more digits and no person's name in `specify/`. `+66` appears only as a pattern prefix. The only handle is the team handle `@scb-ace/techx-recovery-tech-leads`. Synthetic values only (`SYN-LAST-0001`, `TESTNAME`). |
| Secrets | None. |
| Unit Test Applicability | Unchanged and compliant. Front end is `NOT_APPLICABLE` with evidence. Tool back end is `REQUIRED`: 80% JaCoCo LINE, BRANCH, METHOD and INSTRUCTION, with positive, negative, boundary and error scenarios. |

**Observation O-1 (not a finding).** One of the 509 Inventory "Yes" fields the seed does not mark,
DF-REF-273 `payment_match_rule.approved_by` (Staff identifier), has no `sys_fields` row. The
`payment_match_rule` table is not in Physical Schema v6 (`AGENTS.md` §4.9: removed by D-RCV-35/36). The
remaining 508 are seed rows set to `false`. The statement "509 … that the seed does not mark" is true as
worded. OPEN-NEW-TE011-1 (b) can act on only 508 rows. The specifier may wish to say "508 seed rows, plus
DF-REF-273, whose table was removed" when fixing SG3-02. This is optional.

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
ROUND_2_DISPOSITION: SG2-01 Partly resolved (residual Low as SG3-02); SG2-02 Partly resolved (residual Low as SG3-01)
ROUND_1_DISPOSITION: SG-01..SG-07 remain Resolved; no regression
BLOCKING: NO (Low findings only)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
NEXT_STEP: A person records the disposition of SG3-01 and SG3-02 (fix in the specify stage, or accept and carry them to the plan gate). The Implementation Planner may then start; this review does not start it.
```
