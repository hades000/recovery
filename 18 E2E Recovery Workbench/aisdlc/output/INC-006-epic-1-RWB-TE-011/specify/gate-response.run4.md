# Gate response — RWB-TE-011 spec gate, round 1

RUN_ID `INC-006-epic-1-RWB-TE-011`, remediation 1, 2026-11-17. Each finding in `review/spec-gate-review.md`
(FAIL: 0 Critical, 0 High, 2 Medium, 5 Low) is mapped to the change that resolves it. The re-review is
`review/spec-gate-review-2.md`. The classification source did not change: the story contract stays.

| Finding | Severity | Change made | Where |
|---|---|---|---|
| SG-01 | Medium | (1) DGL-01 now cites PDPA Design v2 §1 (Inventory named as "the field-level inventory"), backend context v2.0 §6 and story §11, and states the precedence: the story files v7 contract (§12; TE Stories v7 BR1/§12) over non-story sources, with DL26 as the decision owner. (2) The "Consequence" paragraph is replaced by "Residual risk": a table of the 9 Inventory v4 Restricted fields the seed leaves unmarked (checked against Inventory v4: 17 Restricted, 9 unmarked), plus the other unmarked "Yes" fields. The list is copied into OPEN-NEW-TE011-1, now a release-readiness item. (3) Precondition 2 is set to "Partly met". (4) A coverage row for story §11 Data is added (30 rows). (5) SPEC-TE011-016 now says that "zero findings" is measured against the dictionary as it is, and that the implementation report must repeat this. | spec.md: "Personal data classification used", "Entry trigger and preconditions", SPEC-TE011-016, coverage table, status block; document-gaps.md DGL-01; shared-updates.md OPEN-NEW-TE011-1 |
| SG-02 | Medium | The code-owner file is now `.gitlab/CODEOWNERS`, the file the RWB-TE-002 spec delivers (SPEC-RWB-TE-002-001; L-RCV-12), added as source SRC-23. The entry `/tools/pdpa-lint/ @scb-ace/techx-recovery-tech-leads` goes in section `[Recovery module]`. The owner is already in `.gitlab/codeowners-register.yaml` (V7). The pattern is anchored with no wildcard (V4) and lands in the same merge as `tools/pdpa-lint/` so that V9 passes. | spec.md: Change Scope Declaration, preflight, SPEC-TE011-014, CLAR-007, SRC-23; DGL-12; OPEN-NEW-TE011-5 |
| SG-03 | Low | Rule removed. Every field stays in the list whatever its `is_active` value (fail-safe), and a unit scenario asserts it. | spec.md SPEC-TE011-001; test requirements (Reader) |
| SG-04 | Low | PDPA-FIXTURE-ID now runs on `tools/pdpa-lint/**` (self-scan). Every failing ID, mobile and e-mail value in the tool's tests is built at run time, and a self-scan test is added. The `infra` exclusion is narrowed to `infra/postgres/schema/**`; the rest of `infra/` is scanned for fixtures. Grep evidence shows the zero-finding baseline holds (only `local.test` e-mails; no 13-digit number; no personal-field literal). | spec.md SPEC-TE011-003, -009, -016; test requirements; ASM-TE011-05 |
| SG-05 | Low | The spec now cites `AGENTS.md` §6 as the general rule, with D-RCV-16 as its origin. | spec.md preflight, SPEC-TE011-016 heading; DGL-02 |
| SG-06 | Low | The grouping is now defined per form: national `0` + 9 digits as 3-3-4; `+66`/`66` + 9 digits as 2-3-4. The false-positive trade-off of the bare `66` prefix is recorded. A unit scenario covers the separated `+66` form, built at run time. | spec.md SPEC-TE011-009; test requirements; ASM-TE011-09 |
| SG-07 | Low | RWB-TE-003 is named as the candidate owner of A-07 (it already changes `ApiExceptionHandler` under A-08), with `AISDLC-HARDENING` as the alternative. OPEN-NEW-TE011-2 and -3 are marked as release-readiness items. A new section 3a asks the orchestrator to change the A-07 owner in the Phase 0 audit. | spec.md "Scope decisions"; shared-updates.md OPEN-NEW-TE011-2/-3, section 3a |

# Gate response — round 2

Round 2 (`review/spec-gate-review-2.md`): FAIL, 0 Critical, 0 High, 1 Medium, 1 Low. All round-1 findings
were marked Resolved. Re-review: `review/spec-gate-review-3.md`.

| Finding | Severity | Change made | Where |
|---|---|---|---|
| SG2-01 | Medium | Checked against Inventory v4: it marks 14 of the 18 seed fields. It classes DF-DOC-049, -052, -077 and -089 as "Not personal" / Internal, and the unmarked "Yes" fields number 509. The statement and the count are corrected, and the reverse conflict is recorded in DGL-01 and in the spec. OPEN-NEW-TE011-1 now asks Compliance to add marks only, not to unmark the 4 fields, and to correct their Inventory rows. The lint keeps the 4 fields (fail-safe). | spec.md "Personal data classification used"; DGL-01; shared-updates.md OPEN-NEW-TE011-1 |
| SG2-02 | Low | The review references in `shared-updates.md` and `compliance-validation.md` now point to the round files. `AGENTS.md` §6 is added to SRC-21. The `infra/postgres/schema/**` exclusion now names all three files; the first two have no INSERT (checked); see round 3 for the correction on the third. | shared-updates.md; compliance-validation.md; spec.md SRC-21, SPEC-TE011-003; ASM-TE011-05 |

# Gate response — round 3 (Low findings only; not re-reviewed)

Round 3 (`review/spec-gate-review-3.md`): FAIL, 0 Critical, 0 High, 0 Medium, 2 Low. This triggers
REVIEW_GATE_WARNING. Both Low findings were fixed in the text after round 3. No round 4 was run, so the
fixes have not been reviewed.

| Finding | Severity | Change made | Where |
|---|---|---|---|
| SG3-01 | Low | The wrong rationale "schema-only" is corrected. `03-recovery-physical-schema-v6.sql` holds seed INSERTs, including the `sys_fields` seed that the lint reads. It is excluded because it is a read-only copy and the lint's own input, not a test fixture. The round-2 response line is corrected too. | spec.md SPEC-TE011-003; ASM-TE011-05; this file |
| SG3-02 | Low | DGL-01 now says "reconcile … by adding marks only", which matches OPEN-NEW-TE011-1. Support for keeping the 4 fields now cites the seed descriptions in Physical Schema v6 `sys_fields`: DF-DOC-049 "personal where it names a customer"; DF-DOC-052 and DF-DOC-089 "masked by role". It also cites PDPA Design v2 §1 for DF-DOC-077. | document-gaps.md DGL-01; shared-updates.md OPEN-NEW-TE011-1 |
