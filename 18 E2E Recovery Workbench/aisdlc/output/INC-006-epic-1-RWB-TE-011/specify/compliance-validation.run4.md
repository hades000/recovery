# Compliance validation — RWB-TE-011 specification (specifier self-check)

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Artifact | `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` (SPEC-TE011-001..016) |
| Prepared by | Technical Specifier, 2026-11-17 |
| Purpose | Checklist of `.github/rules/specification-execution-gates.md` "Spec Validation Checklist" and the banking controls, before the gate |
| Independent gate | Compliance Reviewer, rounds kept in `output/INC-006-epic-1-RWB-TE-011/review/`: `spec-gate-review.md` (round 1), `spec-gate-review-2.md` (round 2), `spec-gate-review-3.md` (round 3); responses in `specify/gate-response.md` |

## 1. Banking and domain controls against source requirements

| Control | Source | Where in the spec | Result |
|---|---|---|---|
| No personal data in code, test fixtures or logs | NFR-054 (NFR Specification v3); `AGENTS.md` §4.7; BS-4.6 | SPEC-TE011-004..-009, -013 | Specified as a blocking pipeline job |
| Synthetic data in development | NFR-045; `AGENTS.md` §3.9; testing standards §2 | SPEC-TE011-008 (`SYN-` prefix), -009 (ID/mobile/e-mail) | Specified |
| Masking by role not bypassed through logs | REQ-RDF-010, REQ-ACA-005 (Business Requirements Program v4 §6.7, §6.9); CTL-11 (Controls Catalog v3) | SPEC-TE011-004..-007, -010 | Specified; run-time masking stays in RWB-E1-037 |
| Classification owned by Compliance, not by code | DL26 (Decision Log v10); story BR1 | SPEC-TE011-001, -015 | Specified; classification differences recorded as DGL-01, not resolved by this stage |
| The lint never discloses the value it finds | Story BR7; §17 | SPEC-TE011-012; every TC asserts it | Specified |
| Exceptions are time-boxed and owned | Story BR6; §17 | SPEC-TE011-011 | Specified; invalid entry fails closed |
| Change control on lint configuration | Story §10; L-RCV-12 | SPEC-TE011-014 | Specified; depends on RWB-TE-002 |
| Fails closed on missing input | ASM-TE011-03 | SPEC-TE011-001, status matrix | Specified |
| No database read; files only | Story §13, §17 | SPEC-TE011-001, Backend Specification | Specified |

## 2. Spec Validation Checklist (specification-execution-gates.md)

| # | Check | Result |
|---|---|---|
| 1 | spec.md and this file re-read | Done |
| 2 | Traceability matrix updated with unique SPEC IDs | Not edited (RUN-BRIEF rule 3); row 006 proposed in `shared-updates.md`. SPEC IDs are unique (`SPEC-TE011-001..016`). |
| 3 | Every SPEC entry linked to requirements | Done: Requirement-to-SPEC Logic Coverage, 30 rows, 0 BLOCKED |
| 4 | Screen table | Not applicable: no screen (story §15) |
| 5 | Design evidence source recorded | `figma/figma_report.md`: NONE, NOT_REQUIRED |
| 6 | Data models and contracts | `contracts/backend-apis.json` (NO_API_CHANGE plus the file/CLI contract) and `contracts/frontend-integrations.json` (NOT_APPLICABLE) parse as JSON; file contracts in spec "Data model" |
| 7 | API impact decision | `NO_API_CHANGE`, with evidence |
| 8 | Banking controls re-validated | Section 1 |
| 9 | Classification against requirement, trace chain, footprint | `NEW_STORY`: no trace chain (matrix row 006), no `tools/` folder, CI has 3 jobs |
| 10 | Zero unmapped business-rule lines | 7 flow steps, BR1–BR7, X1–X11, AC1–AC10, §10, §11, §12, §13, §17 and the upstream IDs all mapped |
| 11 | Intent, triggers, preconditions, constraints, transitions, exceptions preserved | Sections "User story intent", "Entry trigger and preconditions", "Status-transition matrix", "Exceptional-case behavior" |
| 12 | Gaps reported | `document-gaps.md` DGL-01..12, no blocker; `assumptions.md` ASM-TE011-01..19 |

## 3. Data protection scan of the outputs

- No real name, national ID, account, contract or mobile number, address or e-mail of a person appears in
  any file of this stage. The only identifiers are field names, synthetic placeholders (`SYN-LAST-0001`,
  `TESTNAME` from AC4) and the reserved-domain rule. Values that would match a FIXTURE-ID pattern are
  specified as generated at run time (SPEC-TE011-009).
- No secret, token or credential.

## 4. Points the gate should look at

| Point | Spec position |
|---|---|
| A-07 placed out of scope | "Scope decisions on the orchestrator notes"; open items proposed |
| Production classification narrower than the story Background | "Personal data classification used"; DGL-01 |
| TC-TE-011-11 cannot pass locally | SPEC-TE011-014; ASM-TE011-17 |
| Strict rule for DATE/NUMBER personal fields | SPEC-TE011-008; DGL-08 |
