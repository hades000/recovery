# Compliance validation: RWB-E1-043 specify (INC-008-epic-1-RWB-E1-043)

Revision 4, 2026-11-18 (remediation run 3; revisions 1 to 3 kept as `compliance-validation.run1.md`,
`compliance-validation.run2.md` and `compliance-validation.run3.md`). Self-check by the Technical Specifier against
`.github/rules/specification-execution-gates.md`, `AGENTS.md` v2 and the contexts. The independent gates
are `review/spec-gate-review.md` (round 1, FAIL), `review/spec-gate-review-2.md` (round 2, FAIL) and
`review/spec-gate-review-3.md` (round 3, FAIL) and `review/spec-gate-review-4.md` (round 4). Every
round-1 to round-3 finding is mapped in `gate-response.md`.

## 1. Spec validation checklist

| Check | Result | Evidence |
|---|---|---|
| Change Scope Declaration complete, module scope stated | PASS | spec.md §Change Scope Declaration (all code in P3 `casewf.refdata`; one P4 interface; no platform change; two-module scope flagged for the plan gate, AGENTS §7) |
| Requirement-to-SPEC coverage, no BLOCKED row | PASS | 49 rows, all COVERED (48 DIRECT, 1 INHERITED_EXISTING_BEHAVIOR); 16 lines owned elsewhere listed with owner and BS6 order, incl. the HTTP version read and the SIT done-when (gate finding 123) |
| A COVERED row is built and tested | PASS | Each COVERED row names a SPEC and a test (rollback SPEC-024 / TC-RB-01..02; handler contract SPEC-025 / TC-HD-01..05; access-list guard SPEC-026 / SEC-15; audit SPEC-028 / SEC-05..11) |
| Intent, trigger, preconditions | PASS | spec.md §User story intent, §Entry trigger (P1-P6) |
| Field, status-transition, exception matrices | PASS | spec.md sections of those names (handler repeat 409, access-list refusal, handler defect rows added) |
| API change assessment | PASS | 3 operations built (load, approve, rollback), 2 not built with gap; no OpenAPI delta |
| Unit Test Applicability: frontend and backend rows, 80% gate | PASS | spec.md §Unit Test Applicability (SPEC-001..032) |
| Security tests per endpoint (missing method check, wrong capability, audit on refusal, self-granting, actor claim) | PASS | SEC-01..SEC-17; TC-FD-01 (no `table`), TC-BD-01 (dependency direction) |
| SPEC IDs unique and mapped to FR/NFR | PASS | SPEC-RWB-E1-043-001..032; `shared-updates.md` §1 |
| Every backend endpoint has a consumer or is backend-only | PASS | `contracts/frontend-integrations.json` (3 backend-only) |
| NFR applicability stated | PASS | spec.md §NFR applicability (NFR-RWB-001..010) |
| Every statement cites a source or a labelled assumption | PASS | spec.md §0 source tags with version and line; A-01..A-44; AI-orchestrator rulings and triage named as such |
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
| Handler contract with other modules | D-RUN-11; S7-001 §12; S7-019 AC4-AC5; gate findings 120, 132, 133, 136 | SPEC-025 L1-L15 check order (table check before the loader list; repeat before the date check), message pass-through, optional definition, repeat message, effective-date rule; TC-HD-01..05, TC-RP-01, TC-FD-01 |
| Effective date and version independence | S7 BR3; S7-019 BR3, AC2, AC9; DD8; gate finding 132 | SPEC-032, SPEC-024; TC-TM-01..04 |
| No role literal in code | AGENTS §3.2, AUD A-03 | SPEC-027 (grants file and catalog data) |
| No business value as literal | AGENTS §3.2/§4.8, S7 §17 | SPEC-003, 013, 027, 029 |
| No personal data in logs | AGENTS §4.7, BS-4.6, NFR-RWB-006 | SPEC-014, SPEC-028 (conflict with backend context line 138 recorded, GAP-42) |
| Admin-action and refusal audit | BS-4.4; FR-RWB-012; TC7 TC-E1-043-11 | SPEC-028 (interim adapter; RWB-E1-039 seam) |
| Decision log entry for the approval | AGENTS §3.4; API4 AC-VERS | SPEC-008 calls this story's package-private `ReferenceDecisionRecorder` (interim log; 503 MSG-P7-003 on failure; RWB-E1-027 replaces it; GAP-07, GAP-50); TC-DR-01 |
| PDPA classification changes | DL10 D-RCV-29; TE-011 §10; S7-064 §11 | SPEC-031: registry and generic checks only; `is_personal` runtime protection is a stated requirement on RWB-E1-064 with open item R4 (RW-COMPLY) |
| Migration rule | DL10 D-RCV-28; D-RUN-07; D-RUN-12 | SPEC-001 (guarded DDL, `V<seq>__rwb_e1_043_reference_versions.sql`, no schema/role/grant); RWB-E1-001 creates neither table |
| ACE data only through views | D-RCV-35 U4, ADR-010 | SPEC-017 (provider), SPEC-021 |
| No `rule_row` loader or rule table | D-RCV-36, AGENTS §4.9 | SPEC-002, 021 |
| Module boundary | AGENTS §3.11, RWB-TE-001 v4 SPEC-022 (d), SU-08 | SPEC-019 (dependency table, P3 → P4 only, no P3 ↔ P4 cycle, boundary rules, TC-BD-01), SPEC-026 (`ParameterLoadHandler` only), SPEC-025 (SPI in `casewf.refdata.api`), SPEC-031 (no call into P1); latent P1 ↔ P3 risk GAP-51 |
| Feature flag with previous path | AGENTS §3.13 | SPEC-018 (`@ConditionalOnProperty`, module record, `@ConditionalOnExpression`; read side present, write side gated, 404 for an off branch); TC-FL-01 |
| Append-only audit of versions | S7 §17 | SPEC-001 trigger (narrowed, A-33) |
| Test-first, one test per AC | AGENTS §3.10; testing-standards §3 | spec.md §Test scenarios |

## 3. Residual risk carried to the plan gate

- 44 labelled assumptions (A-01..A-44; A-32 withdrawn). A-01, A-07, A-08, A-09/A-34, A-16, A-17, A-27,
  A-31, A-33, A-37..A-42 change behaviour and need owner acceptance; none is accepted (spec.md §Owner
  acceptance).
- The AI-orchestrator rulings D-RUN-08, D-RUN-10, D-RUN-11 (and D-RUN-12, the 2026-11-18 triage) are not
  ratified by a human; nor is the round-3 triage; open item R1 asks the engagement lead.
- 53 document gaps (35 conflicts, 18 missing), none blocking this story. GAP-24 (G-R05) is recorded
  Blocker = No under D-RUN-10 and D-RUN-11.
- Build depends on RWB-E1-042 revision 5's `casewf.config.api` and `access.api` names (A-25), still in
  RWB-E1-042's own gate round (shared update R6 asks it to keep them stable), and on its code being present.
- Two-module scope (P3 plus one P4 interface) goes to the plan gate (AGENTS §7).
- Latent P1 ↔ P3 cycle when RWB-E1-001/-064 handlers and a P3 → P1 business-date reader both exist (GAP-51).
- The access lists cannot be changed by any load; until RWB-E1-037 the only path is a reviewed catalog
  change (A-39; R7).
- If a token carries neither `oid` nor `sub` as a UUID, loads are refused with 401 (A-07; R8).
- A refused load cannot be attributed to an actor until RWB-E1-039 (GAP-42; R9).
- The release SIT exit for the 12 tables depends on later stories; three tables have no named owner
  (GAP-43; R10).
- `is_personal` runtime protection depends on RWB-E1-064 meeting the stated requirement (R3, R4).

Result: READY_FOR_SPEC_GATE.
