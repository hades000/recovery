# Compliance validation: RWB-E1-043 specify (INC-008-epic-1-RWB-E1-043)

Revision 2, 2026-11-18 (remediation run 1; revision 1 kept as `compliance-validation.run1.md`).
Self-check by the Technical Specifier against `.github/rules/specification-execution-gates.md`,
`AGENTS.md` v2 and the contexts. The independent gates are `review/spec-gate-review.md` (round 1,
FAIL) and `review/spec-gate-review-2.md` (round 2). Every round-1 finding is mapped in
`gate-response.md`.

## 1. Spec validation checklist

| Check | Result | Evidence |
|---|---|---|
| Change Scope Declaration complete, module scope stated | PASS | spec.md §Change Scope Declaration (P3, P4, platform rows; multi-module flagged for the plan gate, AGENTS §7) |
| Requirement-to-SPEC coverage, no BLOCKED row | PASS | 50 rows, all COVERED (49 DIRECT, 1 INHERITED_EXISTING_BEHAVIOR); 14 lines owned elsewhere listed with owner and BS6 order |
| A COVERED row is built and tested | PASS | Each COVERED row names a SPEC and a test (rollback SPEC-024 / TC-RB-01..02; logging SPEC-014 / TC-03; audit SPEC-028 / SEC-05..11) |
| Intent, trigger, preconditions | PASS | spec.md §User story intent, §Entry trigger (P1-P6) |
| Field, status-transition, exception matrices | PASS | spec.md sections of those names (ROLLED_BACK transitions added) |
| API change assessment | PASS | 3 operations built (load, approve, rollback), 2 not built with gap; no OpenAPI delta |
| Unit Test Applicability: frontend and backend rows, 80% gate | PASS | spec.md §Unit Test Applicability (SPEC-001..031) |
| Security tests per endpoint (missing method check, wrong capability, audit on refusal) | PASS | SEC-01..SEC-14 |
| SPEC IDs unique and mapped to FR/NFR | PASS | SPEC-RWB-E1-043-001..031; `shared-updates.md` §1 |
| Every backend endpoint has a consumer or is backend-only | PASS | `contracts/frontend-integrations.json` (3 backend-only) |
| NFR applicability stated | PASS | spec.md §NFR applicability (NFR-RWB-001..010) |
| Every statement cites a source or a labelled assumption | PASS | spec.md §0 source tags with version and line; A-01..A-36 |
| No TODO or placeholder | PASS | `<seq>` is the D-RCV-28 merge-time token (D-RUN-07), not a placeholder |
| Status lines emitted | PASS | spec.md §Status reporting |
| Design evidence | NOT_REQUIRED | `figma/figma_report.md` (no screen, S7 §15) |
| No personal data, secret or production data | PASS | Synthetic codes and random UUIDs only (SPEC-023); no user ID in log or audit lines (SPEC-014, SPEC-028, A-30) |

## 2. Domain and project controls

| Control | Source | Where met |
|---|---|---|
| Maker-checker | S7 BR4, CTL-08 | SPEC-008 + DB CHECK approver ≠ author (SPEC-001) |
| Method security naming area and right | AGENTS §3.3, BS-3.2 | SPEC-015, 016, 024 (`'Reference data'`, C/A/U); SEC-01 reflection test |
| Least privilege per table, fail closed | S7 §10; API4 approve; gate finding 104 | SPEC-027 (`rwb.refload.loader/approver.<code>`; missing key refuses) |
| No role literal in code | AGENTS §3.2, AUD A-03 | SPEC-027 (grants file and catalog data) |
| No business value as literal | AGENTS §3.2/§4.8, S7 §17 | SPEC-003, 013, 027, 029 |
| No personal data in logs | AGENTS §4.7, BS-4.6, NFR-RWB-006 | SPEC-014, SPEC-028 |
| Admin-action and refusal audit | BS-4.4; FR-RWB-012; TC7 TC-E1-043-11 | SPEC-028 (interim adapter; RWB-E1-039 seam) |
| Decision log entry for the approval | AGENTS §3.4; API4 AC-VERS | SPEC-008 calls RWB-E1-042's `VersionDecisionRecorder` (seam; RWB-E1-027 implements, GAP-07) |
| PDPA classification changes | DL10 D-RCV-29; TE-011 §10; PDPA design v2 | SPEC-031: route, version log, `changeSummary` audit, RW-COMPLY approver list; removal approval is a seam with open item (A-36) |
| Migration rule | DL10 D-RCV-28; D-RUN-07 | SPEC-001 (guarded DDL, `V<seq>__rwb_e1_043_reference_versions.sql`, no schema/role/grant) |
| ACE data only through views | D-RCV-35 U4, ADR-010 | SPEC-017 (provider), SPEC-021 |
| No `rule_row` loader or rule table | D-RCV-36, AGENTS §4.9 | SPEC-002, 021 |
| Module boundary | AGENTS §3.11, RWB-TE-001 | SPEC-019 (boundary test), SPEC-026 (`ParameterLoadHandler` only), SPEC-025 (SPI) |
| Feature flag with previous path | AGENTS §3.13 | SPEC-018 (read side present, write side gated, 404 for an off branch); TC-FL-01 |
| Append-only audit of versions | S7 §17 | SPEC-001 trigger (narrowed, A-33) |
| Test-first, one test per AC | AGENTS §3.10; testing-standards §3 | spec.md §Test scenarios |

## 3. Residual risk carried to the plan gate

- 36 labelled assumptions (A-01..A-36). A-01, A-08, A-09/A-34, A-16, A-17, A-27, A-31, A-33 change
  behaviour and need owner acceptance (spec.md §Owner acceptance).
- 38 document gaps (26 conflicts, 12 missing), none blocking this story. GAP-24 (G-R05) is recorded
  Blocker = No under D-RUN-10 and D-RUN-11 (orchestrator rulings by Claude Code, an AI agent).
- Build depends on RWB-E1-042 revision 3's `platform.api` names (A-25) and code being present.
- Multi-module scope (P3, P4, platform) goes to the plan gate (AGENTS §7).
- RWB-E1-001 must not create `reference_version`/`reference_row` unguarded (shared update, finding 108).
- The `is_personal` removal approval has no source; until RW-COMPLY decides, a removal is governed by
  the dictionary approver list only (SPEC-031; open item).

Result: READY_FOR_SPEC_GATE.
