# Spec gate review, round 2: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review (Compliance Reviewer, independent of the author) |
| Round 1 | `review/spec-gate-review.md`: FAIL, 0 Critical, 0 High, 2 Medium (SG-01, SG-02), 5 Low (SG-03..SG-07) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..016), `compliance-validation.md`, `assumptions.md` (ASM-TE011-01..19), `document-gaps.md` (DGL-01..12), `shared-updates.md`, `gate-response.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `figma/figma_report.md` |
| Checked against | Increment card INC-006; RWB-TE-011 story file v1 (Epic 1 Story Files v7, 28 Oct 2026) §3, §7, §8, §10–§13, §17, §19; Data Classification and Personal Data Inventory v4, sheet Fields; Personal Data Protection Design v2 (document table "Version 1") §1; Physical Schema v6 `sys_fields` seed and column comments (repository copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql`); backend context v2.0 §6; decision register D-RCV-16; `AGENTS.md` §6; Phase 0 standards audit A-07, A-08, A-09; RWB-TE-002 spec (`output/INC-004-epic-1-RWB-TE-002/specify/spec.md`: SPEC-RWB-TE-002-001, -008, -009, "Code owners file", "Validation rules" V4–V9); RWB-TE-003 spec (`output/INC-005-epic-1-RWB-TE-003/specify/spec.md`, A-08 rows, SPEC-RWB-TE-003-013); repository as it stands (`.gitlab-ci.yml`, `infra/`, `backend/src`, `frontend/src`, `frontend/e2e`, `README.md`) |
| Method | Each round-1 finding checked against the source and the repository, not against `gate-response.md`. Counts recomputed from the Inventory v4 table and the seed. Scan roots grepped for e-mail, 13-digit, Thai mobile patterns and every personal field name variant. |
| Date | 2026-11-17 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 1 |

All seven round-1 findings are resolved. The remediation of SG-01 copied a counting premise from round 1's
required fix ("523 'Yes' fields minus the 18 seed fields"). That premise is wrong: Inventory v4 does not
mark 4 of the 18 seed fields as personal. Round 1 did not detect this. The spec now states something
false about the classification sources, and the open item for Compliance could reduce the lint's coverage
if it is followed as written (REVIEW-TE011-SG2-01, Medium). The Medium finding blocks the handoff to the
Implementation Planner until it is fixed and the gate is run again (`spec-gate-review-3.md`), or until a
person records that they accept it (`pdlc.md`, "Human Checkpoints").

## 2. Disposition of round-1 findings

| Round-1 finding | Severity | Disposition | Evidence checked |
|---|---|---|---|
| SG-01 Classification conflict and residual coverage risk understated | Medium | **Resolved** (all five required points). A defect in the same area, which round 1 missed and its fix carried forward, is raised as SG2-01. | (1) DGL-01 now cites PDPA Design v2 §1 and backend context v2.0 §6. Both quotes were verified: PDPA Design v2 line "The field-level inventory is the data classification and personal data inventory workbook", and backend-context §6 "Security and access", "field-level classification in the Personal Data Inventory v4". DGL-01 also states the precedence (story files v7 §12, TE Stories v7 BR1/§12) and names DL26 as the owner. (2) The residual-risk table lists the 9 Restricted fields that are not marked. Recount: the Inventory v4 Fields sheet has 17 Restricted rows; the seed marks 8 of them (DF-ACE-057, -058, -059, -066, -073, -078, DF-INT-011, DF-DOC-015); the other 9 are exactly the 9 listed. The same list is in OPEN-NEW-TE011-1. (3) Precondition 2 now reads "Partly met". (4) A coverage row exists for story §11 Data. Its 11 field IDs match story §11. It names the 4 fields that are covered only once marked. (5) SPEC-TE011-016 qualifies "zero findings" and requires the implementation report to repeat the limit. |
| SG-02 Code-owner file path and format conflict with RWB-TE-002 | Medium | **Resolved** | Spec scope declaration, SPEC-TE011-014, CLAR-007, DGL-12, OPEN-NEW-TE011-5 and the new SRC-23 now name `.gitlab/CODEOWNERS`, section `[Recovery module]`. Checked against the RWB-TE-002 spec: SPEC-RWB-TE-002-001 (GitLab section format); "Code owners file" has a `[Recovery module]` section owned by `@scb-ace/techx-recovery-tech-leads`; the owner register (SPEC-RWB-TE-002-009) lists that handle, so V7 is met; `/tools/pdpa-lint/` starts with `/` and has no wildcard, so V4 is met; no later directory pattern in that section covers it, so V6 is met; it is added in the same merge as the folder, so V9 is met. Neither `.gitlab/` nor `tools/` exists in the repository today, consistent with "RWB-TE-002 … is not built". |
| SG-03 Unlabelled behaviour: inactive rows ignored | Low | **Resolved** | SPEC-TE011-001 now keeps a field "whatever its `is_active` value (fail-safe)", and the Reader unit scenarios include "`is_active = false` row still listed". |
| SG-04 Scan exclusions leave the guardrail and repo-authored files unenforced | Low | **Resolved** | SPEC-TE011-003 applies FIXTURE-ID to `tools/pdpa-lint/**` (self-scan) and narrows the exclusion to `infra/postgres/schema/**`. SPEC-TE011-009 and the test requirements state that every failing ID, mobile and e-mail value is built at run time, with a self-scan unit scenario. Baseline claim re-verified by grep on 17 Nov 2026: the repo-authored `infra/` files (`mock-oidc/config.json`, `postgres/init/*`, `temporal/*`) hold only `local.test` e-mail addresses, no 13-digit number, no Thai mobile pattern and no personal field name. `backend/src`, `frontend/src` and `frontend/e2e` hold the same (3 `local.test` addresses in `platform.spec.ts`). The only personal-name variant in production source, the `fileName` parameter in `DroolsRuleEngine.compile`, is not used in a log call, an exception construction or a text form. The zero-finding expectation in SPEC-TE011-016 holds. |
| SG-05 D-RCV-16 cited beyond its scope | Low | **Resolved** | The preflight, the SPEC-TE011-016 heading and DGL-02 cite `AGENTS.md` §6, which reads "A story with no business ACs is accepted on its business rules and test cases (D-RCV-16)", with D-RCV-16 as the origin. The decision register scopes D-RCV-16 to RWB-E1-044 and RWB-TE-001, as the spec now acknowledges. The Sources table does not list §6 (SG2-02). |
| SG-06 Thai mobile grouping | Low | **Resolved** | SPEC-TE011-009: national `0` + `6/8/9` + 8 digits, grouped 3-3-4. International `+66`/`66` + 9 digits, grouped 2-3-4. ASM-TE011-09 records the false-positive trade-off of the bare `66` prefix and says it can be removed in configuration. The unit scenarios include the separated `+66` 2-3-4 form, built at run time. |
| SG-07 A-07 hand-off has no owner | Low | **Resolved** | `shared-updates.md` §3a asks the orchestrator to change the A-07 owner. It names RWB-TE-003 as the candidate, or `AISDLC-HARDENING`. Verified: audit row A-08 assigns `ApiExceptionHandler` to RWB-TE-003, and the RWB-TE-003 spec changes that class (SPEC-RWB-TE-003-013). OPEN-NEW-TE011-2 and -3 are now "Release readiness", not "Blocks: Nothing". |

## 3. New findings

### REVIEW-TE011-SG2-01: Inventory v4 does not mark 4 seed fields; the spec says it does, and the Compliance open item could remove lint coverage (Medium)

- **Affects:** spec "Personal data classification used" (cross-check row "Inventory v4", line 148;
  residual-risk paragraph, line 177); SPEC-TE011-016 (the count the report must repeat); DGL-01;
  `shared-updates.md` OPEN-NEW-TE011-1; `gate-response.md` row SG-01; SPEC-TE011-001; BR1; CTL-11;
  REQ-RDF-010.
- **Evidence:**
  1. spec.md line 148 says Inventory v4 "Marks every field the seed marks, plus about 505 more". Line 177
     says the seed leaves "about 505" Inventory v4 "Yes" fields unmarked. OPEN-NEW-TE011-1 says "523 in
     total against 18 marked".
  2. In the Inventory v4 Fields sheet, 4 of the 18 fields that the Physical Schema v6 seed marks
     `is_personal = true` have "Personal data" = **No** and classification **Internal**: DF-DOC-049
     `document_intake.file_name`, DF-DOC-052 `document_intake.sender_address`, DF-DOC-077
     `document_intake.extracted_fields` and DF-DOC-089 `document_text.text_content`. Inventory v4 marks
     only 14 of the 18. The unmarked "Yes" fields therefore number 523 − 14 = 509, not about 505.
  3. The conflict therefore runs both ways. DGL-01 records only one direction: fields the Inventory
     marks that the seed does not. It does not record that Inventory v4 classes 4 seed-marked fields as
     not personal.
  4. Inventory v4 also conflicts with other sources on these 4 fields. PDPA Design v2 §1 lists
     "extracted document fields" as Direct identifier / Restricted. The Physical Schema v6 column
     comments read "Sender email address for mailbox items; masked by role", "OCR text of the page;
     masked by role on read" and "File name as received; personal where it names a customer".
  5. OPEN-NEW-TE011-1 asks RW-COMPLY to "Align `sys_fields.is_personal` with Inventory v4". If that is
     followed literally, the 4 fields would be set to `false`. The lint follows the dictionary with no
     code change (BR1, AC5), so OCR page text, sender e-mail addresses, extracted document fields and
     file names would silently leave the lint's coverage.
  6. Root cause: round 1's required fix (SG-01 point 2, "the 523 'Yes' fields minus the 18 seed fields")
     assumed that the seed's 18 fields were a subset of the Inventory's 523. The remediation copied that
     assumption. `gate-response.md` reports "checked against Inventory v4: 17 Restricted, 9 unmarked",
     but that check covered only the Restricted rows, not the containment.
- **Why it matters:** this is the statement of record that Compliance (DL26) will act on. A wrong
  statement about which fields each source marks breaks the "every statement traces" bar in the place
  where the bar matters most. The open item, as worded, could lead a dictionary change to reduce PDPA
  protection for free-text and e-mail fields.
- **Required fix (spec, `document-gaps.md`, `shared-updates.md`, `gate-response.md`; no change to the
  classification source):**
  1. spec.md line 148: replace "Marks every field the seed marks, plus about 505 more" with the true
     statement. Inventory v4 marks 14 of the 18 seed fields, plus 509 fields the seed does not mark. It
     classes DF-DOC-049, DF-DOC-052, DF-DOC-077 and DF-DOC-089 as Internal / not personal. Correct
     "about 505" to 509 on line 177 and in SPEC-TE011-016 wherever the count is used.
  2. DGL-01: add the reverse conflict, citing Inventory v4 (the 4 rows) against the Physical Schema v6
     seed and column comments and PDPA Design v2 §1 ("extracted document fields", Restricted). State that
     the lint keeps the seed marks under the story-contract precedence. The result is fail-safe: it is
     stricter than the Inventory.
  3. OPEN-NEW-TE011-1: make the request additive only ("mark as personal …; do not unmark any field the
     seed marks"). Add a separate request to RW-COMPLY to correct the Inventory v4 rows for the 4
     DF-DOC fields against PDPA Design v2 §1. Correct "523 in total against 18 marked" to "523 marked in
     Inventory v4, 14 of them also in the seed".
  4. In `gate-response.md` (or its successor), record the correction against SG-01.

### REVIEW-TE011-SG2-02: Stale gate references and small source-citation gaps (Low)

- **Affects:** `shared-updates.md` §1 and §2; `compliance-validation.md` header; spec Sources SRC-21;
  SPEC-TE011-003 "Not scanned"; ASM-TE011-05.
- **Evidence:**
  1. `shared-updates.md` §1 ("Status … spec gate per `review/spec-gate-review.md`") and §2 ("Spec gate
     result from `review/spec-gate-review.md`") point the orchestrator at the round-1 FAIL as the gate
     result. `compliance-validation.md` still names only round 1 as the independent gate and does not
     record the remediation.
  2. SPEC-TE011-016 and the preflight now cite `AGENTS.md` §6, but SRC-21 lists `AGENTS.md` §3.9, §4.4,
     §4.7 and §9 only.
  3. SPEC-TE011-003 and ASM-TE011-05 justify excluding `infra/postgres/schema/**` as "the byte-identical
     copy of … Physical Schema v6". The folder also holds `01-ace-schema-v1.sql` and
     `02-ace-tier2-probe.sql`. These are also copies from the document set (`README.md`, layout comment
     "copies from the set"), they are schema only and they contain no `INSERT`. The exclusion is sound,
     but the stated reason covers one of the three files.
- **Required fix:** in `shared-updates.md` §1–§2, point to the latest spec-gate review file, or say "the
  latest `review/spec-gate-review-N.md`". Add a remediation note to `compliance-validation.md`. Add §6 to
  SRC-21. Extend the exclusion rationale in SPEC-TE011-003 and ASM-TE011-05 to the ACE Schema v1 and Tier
  2 probe copies, both schema only.

## 4. Regression checks on the remediation (passed)

| Check | Result |
|---|---|
| Untraced statements introduced by the changes | One, SG2-01 (the containment claim and the 505 count). All other new text traces: SRC-23 (RWB-TE-002 spec) supports every code-owner statement; the residual-risk table matches Inventory v4 row by row; the PDPA Design v2 §1 and backend-context §6 quotes are verbatim. |
| Invented requirements | None. The self-scan, the narrowed `infra` exclusion, the `is_active` fail-safe and the mobile grouping are labelled (ASM-TE011-05, -09) or are applications of story §17 and BR4. No new rule beyond the six in story §12. A-07 is still out of scope, for the reasons accepted in round 1. |
| Consistency between files | spec, `document-gaps.md`, `assumptions.md`, `shared-updates.md` and `gate-response.md` agree on `.gitlab/CODEOWNERS` / `[Recovery module]`, the 9 Restricted fields, the release-readiness labels and the A-07 owner proposal. `contracts/backend-apis.json` is consistent with SPEC-TE011-001, -002, -011, -012 and -013 (no stale `.github/CODEOWNERS` and no `is_active` rule). `frontend-integrations.json` (`NOT_APPLICABLE`) and `figma_report.md` (`NOT_REQUIRED`) are unchanged and still correct. Exceptions: SG2-01 and SG2-02. |
| Requirement-to-SPEC table | 30 rows counted; `TOTAL_RULES: 30` in the status block matches; 5 upstream IDs as stated. |
| Personal data in the artefacts | None. A grep of `specify/` found no e-mail address, no run of 9 or more digits, and no person's name. The only handle is the team handle `@scb-ace/techx-recovery-tech-leads` (L-RCV-12). Synthetic values only (`SYN-LAST-0001`, `TESTNAME`). |
| Secrets | None. |
| Unit Test Applicability | Unchanged and still compliant: front end `NOT_APPLICABLE` with evidence; tool back end `REQUIRED`, 80% JaCoCo LINE/BRANCH/METHOD/INSTRUCTION, with positive, negative, boundary and error scenarios, including the new self-scan, `is_active` and `+66` scenarios. |
| Observation (not a finding) | RWB-TE-002 puts `/.gitlab-ci.yml` in section `[Pipeline gates]` with a placeholder owner (`@role-placeholder/techx-devops-with-scb-it`, OPEN-038). On the host, this story's new CI job will need that section's approval as well. This belongs to RWB-TE-002 and OPEN-038, not to this spec. |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 1]
ROUND_1_DISPOSITION: SG-01 Resolved; SG-02 Resolved; SG-03 Resolved; SG-04 Resolved; SG-05 Resolved; SG-06 Resolved; SG-07 Resolved
BLOCKING: YES (REVIEW-TE011-SG2-01)
NEXT_STEP: Technical Specifier fixes SG2-01 (and SG2-02, or records it as accepted); Compliance Reviewer reruns the spec gate as review/spec-gate-review-3.md before the Implementation Planner starts, unless a person records acceptance of SG2-01.
```
