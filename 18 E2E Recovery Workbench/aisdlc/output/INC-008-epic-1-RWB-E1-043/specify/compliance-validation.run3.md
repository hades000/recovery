# Compliance validation: RWB-E1-043 specify (INC-008-epic-1-RWB-E1-043)

Revision 3, 2026-11-18 (remediation run 2; revisions 1 and 2 kept as `compliance-validation.run1.md`
and `compliance-validation.run2.md`). Self-check by the Technical Specifier against
`.github/rules/specification-execution-gates.md`, `AGENTS.md` v2 and the contexts. The independent gates
are `review/spec-gate-review.md` (round 1, FAIL), `review/spec-gate-review-2.md` (round 2, FAIL) and
`review/spec-gate-review-3.md` (round 3). Every round-1 and round-2 finding is mapped in
`gate-response.md`.

## 1. Spec validation checklist

| Check | Result | Evidence |
|---|---|---|
| Change Scope Declaration complete, module scope stated | PASS | spec.md §Change Scope Declaration (P3, P4, platform rows; multi-module flagged for the plan gate, AGENTS §7) |
| Requirement-to-SPEC coverage, no BLOCKED row | PASS | 48 rows, all COVERED (47 DIRECT, 1 INHERITED_EXISTING_BEHAVIOR); 15 lines owned elsewhere listed with owner and BS6 order, incl. the HTTP version read and the SIT done-when (gate finding 123) |
| A COVERED row is built and tested | PASS | Each COVERED row names a SPEC and a test (rollback SPEC-024 / TC-RB-01..02; handler contract SPEC-025 / TC-HD-01..05; access-list guard SPEC-026 / SEC-15; audit SPEC-028 / SEC-05..11) |
| Intent, trigger, preconditions | PASS | spec.md §User story intent, §Entry trigger (P1-P6) |
| Field, status-transition, exception matrices | PASS | spec.md sections of those names (handler repeat 409, access-list refusal, handler defect rows added) |
| API change assessment | PASS | 3 operations built (load, approve, rollback), 2 not built with gap; no OpenAPI delta |
| Unit Test Applicability: frontend and backend rows, 80% gate | PASS | spec.md §Unit Test Applicability (SPEC-001..031) |
| Security tests per endpoint (missing method check, wrong capability, audit on refusal, self-granting, actor claim) | PASS | SEC-01..SEC-17 |
| SPEC IDs unique and mapped to FR/NFR | PASS | SPEC-RWB-E1-043-001..031; `shared-updates.md` §1 |
| Every backend endpoint has a consumer or is backend-only | PASS | `contracts/frontend-integrations.json` (3 backend-only) |
| NFR applicability stated | PASS | spec.md §NFR applicability (NFR-RWB-001..010) |
| Every statement cites a source or a labelled assumption | PASS | spec.md §0 source tags with version and line; A-01..A-40; AI-orchestrator rulings named as such |
| No ratification or acceptance claimed | PASS | spec.md §Owner acceptance lists D-RUN-08, -10, -11, -12 and the 2026-11-18 triage as not ratified; A-31's revision-2 acceptance wording removed (gate finding 122); open item R1 to the engagement lead |
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
| No self-granting of access lists | Gate finding 122; S7-037 BR3 | SPEC-026: any `rwb.refload.*` key in a PARAMETER load → 422 MSG-P1-002 before RWB-E1-042 is called (SEC-15); change by reviewed catalog change until RWB-E1-037 (A-39) |
| Actor identity | Gate finding 127; BS-3.2 | SPEC-015 `ActorIdResolver` (`oid`, else `sub`, as UUID; else 401); SEC-16; RWB-E1-022 seam |
| Handler contract with other modules | D-RUN-11; S7-001 §12; S7-019 AC4-AC5; gate finding 120 | SPEC-025 L1-L14 check order, message pass-through, optional definition, repeat message; TC-HD-01..05 |
| No role literal in code | AGENTS §3.2, AUD A-03 | SPEC-027 (grants file and catalog data) |
| No business value as literal | AGENTS §3.2/§4.8, S7 §17 | SPEC-003, 013, 027, 029 |
| No personal data in logs | AGENTS §4.7, BS-4.6, NFR-RWB-006 | SPEC-014, SPEC-028 (conflict with backend context line 138 recorded, GAP-42) |
| Admin-action and refusal audit | BS-4.4; FR-RWB-012; TC7 TC-E1-043-11 | SPEC-028 (interim adapter; RWB-E1-039 seam) |
| Decision log entry for the approval | AGENTS §3.4; API4 AC-VERS | SPEC-008 calls RWB-E1-042's `VersionDecisionRecorder` (seam; RWB-E1-027 implements, GAP-07) |
| PDPA classification changes | DL10 D-RCV-29; TE-011 §10; S7-064 §11 | SPEC-031: registry and generic checks only; `is_personal` runtime protection is a stated requirement on RWB-E1-064 with open item R4 (RW-COMPLY) |
| Migration rule | DL10 D-RCV-28; D-RUN-07; D-RUN-12 | SPEC-001 (guarded DDL, `V<seq>__rwb_e1_043_reference_versions.sql`, no schema/role/grant); RWB-E1-001 creates neither table |
| ACE data only through views | D-RCV-35 U4, ADR-010 | SPEC-017 (provider), SPEC-021 |
| No `rule_row` loader or rule table | D-RCV-36, AGENTS §4.9 | SPEC-002, 021 |
| Module boundary | AGENTS §3.11, RWB-TE-001 | SPEC-019 (boundary test), SPEC-026 (`ParameterLoadHandler` only), SPEC-025 (SPI), SPEC-031 (no call into P1) |
| Feature flag with previous path | AGENTS §3.13 | SPEC-018 (read side present, write side gated, 404 for an off branch); TC-FL-01 |
| Append-only audit of versions | S7 §17 | SPEC-001 trigger (narrowed, A-33) |
| Test-first, one test per AC | AGENTS §3.10; testing-standards §3 | spec.md §Test scenarios |

## 3. Residual risk carried to the plan gate

- 40 labelled assumptions (A-01..A-40). A-01, A-07, A-08, A-09/A-34, A-16, A-17, A-27, A-31, A-33,
  A-37..A-40 change behaviour and need owner acceptance; none is accepted (spec.md §Owner acceptance).
- The AI-orchestrator rulings D-RUN-08, D-RUN-10, D-RUN-11 (and D-RUN-12, the 2026-11-18 triage) are not
  ratified by a human; open item R1 asks the engagement lead.
- 44 document gaps (29 conflicts, 15 missing), none blocking this story. GAP-24 (G-R05) is recorded
  Blocker = No under D-RUN-10 and D-RUN-11.
- Build depends on RWB-E1-042 revision 4's `platform.api` names (A-25) and code being present.
- Multi-module scope (P3, P4, platform) goes to the plan gate (AGENTS §7).
- The access lists cannot be changed by any load; until RWB-E1-037 the only path is a reviewed catalog
  change (A-39; R7).
- If a token carries neither `oid` nor `sub` as a UUID, loads are refused with 401 (A-07; R8).
- A refused load cannot be attributed to an actor until RWB-E1-039 (GAP-42; R9).
- The release SIT exit for the 12 tables depends on later stories; three tables have no named owner
  (GAP-43; R10).
- `is_personal` runtime protection depends on RWB-E1-064 meeting the stated requirement (R3, R4).

Result: READY_FOR_SPEC_GATE.
