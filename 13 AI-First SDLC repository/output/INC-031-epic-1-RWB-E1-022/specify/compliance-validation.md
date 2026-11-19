# Compliance validation - RWB-E1-022 specification

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-022-SPEC-001` |
| Artifact | `output/INC-031-epic-1-RWB-E1-022/specify/spec.md` |
| Stage | Specification gate |
| Reviewer | Compliance Reviewer (agent run) |
| Date | 2026-11-04 |
| Overall status | `PASS` |
| Blocking findings | 0 Critical, 0 High, 0 Medium |
| Warnings | 3 Low |

## 1. Scope of review

The review checked the specification against the source story `RWB-E1-022`, the P4 FSD and TSD, API
Specification v2, the users/roles/permissions matrix, the error and message standard, the screen
inventory and navigation, the design system and the label standard. The context files named in the
authoring guide (`.github/contexts/`) are not present in this workspace; the standards file
`13 AI-First SDLC repository/AGENTS.md` was used instead.

## 2. Findings

| ID | Severity | Area | Finding | Evidence | Remediation | Owner | Status |
|---|---|---|---|---|---|---|---|
| REVIEW-RWB-E1-022-001 | Low | API contract | `GET /me/session` needs an additive `permissions` array for the menu, beyond the v2 `Session` schema. | Spec CLAR-004; API-P4-012 | Merge the additions-file delta into the OpenAPI contract before the planner fixes the front-end types. | API owner | Recorded 2026-11-06 |
| REVIEW-RWB-E1-022-002 | Low | Security | The MFA exemption for `NON_HUMAN_ACTOR` sessions is inferred from AC7 and NFR-051, not stated as a rule. | Story AC7, BR2, BR6; CLAR-002 | Confirm the exemption with the security architect and record it in the decision log before SIT. | Security architect | Recorded 2026-11-06 |
| REVIEW-RWB-E1-022-003 | Low | Design evidence | There is no screen specification or prototype for the ACE shell session line and no-role page; the design system, navigation table and label standard are the evidence. | Screen inventory; design system; label standard | Add the shell states to the screen specification before build, or accept the design-system composition in the design review. | UX lead | Recorded 2026-11-06 |

No Critical, High or Medium findings were found.

## 3. Checks performed

| Check | Result | Evidence |
|---|---|---|
| Authentication and authorization | Pass | Entra ID SSO; `amr` must contain `mfa` for bank users; every endpoint declares a capability area and right; 403 MSG-P4-002. |
| Customer and account data protection | Pass | Access events carry the Entra object ID, role codes and versions only; no name, e-mail or case data. |
| Audit logging | Pass | AC-SIGN and AC-DENY to the ACE audit and SOC log; RWB-E1-039 adds the decision log sink. |
| Separation of duty | Pass | `role_conflict` checked at sign-in; `ANY_BUSINESS_ROLE` covers the security-administrator conflict. |
| API contract | Pass with warning | Two endpoints from the v2 contract; one additive `permissions` field recorded for the additions file. |
| Error handling | Pass | MSG-P4-001/002/005/006 and MSG-GEN-006; refusals logged; no data on refusal. |
| Test coverage | Pass | Frontend and backend `REQUIRED` at 80%; 12 system, security and unit scenarios. |
| Traceability | Pass | 8 BRs, 9 ACs and 7 exception paths mapped to SPEC-001..017; US-RWB-E1-022 linked. |
| Secrets and configuration | Pass | No secret; `rwb.access.required-amr` and group names are parameters/data; no local credential. |
| Design evidence | Pass with warning | `DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1]`; no Figma claimed. |
| No-assumption policy | Pass | CLAR-001..010 resolved; CLAR-002 and CLAR-004 are labelled design resolutions. |
| Operational readiness | Pass | Sign-in and refusal metrics, conflict alerts, run book and feature flag specified. |

## 4. Traceability check

| Chain | Result |
|---|---|
| `US-RWB-E1-022` -> `SPEC-RWB-E1-022-001..017` | Pass |
| Business rules -> SPEC rows | Pass (8/8) |
| Acceptance criteria -> SPEC rows | Pass (9/9) |
| Exception paths -> SPEC rows | Pass (7/7) |
| Test IDs | Seeded; execution evidence is a later stage |

The parent merges the traceability rows per the authoring guide §3; this run did not modify
`requirement/Traceability_Matrix.md`.

## 5. Unit test applicability check

| Surface | Declared | Review |
|---|---|---|
| Frontend | `YES` / `REQUIRED` / 80% | Accepted. New `SessionBanner`, `AccessRequestPage` and menu filter. |
| Backend | `YES` / `REQUIRED` / 80% | Accepted. New resolver, access check, interceptor, publisher and repository. |

The 80% gate is planned, not claimed. Actual execution and native reports belong to the
Implementation Builder and are checked at the code gate.

## 6. Recommendation

Proceed to the Implementation Planner after the human specification review. The open warnings do not
block the technical handoff.

```text
REVIEW_STATUS: PASS
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 3]
REVIEW_GATE: Specification gate
REVIEW_GATE_DECISION: Proceed to human review and the Implementation Planner; warnings carry forward.
NEXT_STEP: Start the Implementation Planner on this specification.
```


## 8. Re-validation — gate 002 (2026-11-06)

Compliance Reviewer re-run. The first run's findings are dispositioned below; the specification is unchanged in substance. Findings marked Recorded stay tracked with their owners and the decision-log dates; the affected values remain data or configuration and none is hard-coded. No blocking finding remains.

| Finding | Severity | Short description | Owner | Gate-002 disposition |
|---|---|---|---|---|
| REVIEW-RWB-E1-022-001 | Low | `GET /me/session` needs an additive `permissions` array for the menu, beyond the v2 `Session` schema. | API owner | Recorded 2026-11-06 — confirmation owned by API owner; the value stays data/configuration, the specification hard-codes nothing, and the item carries into the build hand-over. |
| REVIEW-RWB-E1-022-002 | Low | The MFA exemption for `NON_HUMAN_ACTOR` sessions is inferred from AC7 and NFR-051, not stated as a rule. | Security architect | Recorded 2026-11-06 — confirmation owned by Security architect; the value stays data/configuration, the specification hard-codes nothing, and the item carries into the build hand-over. |
| REVIEW-RWB-E1-022-003 | Low | There is no screen specification or prototype for the ACE shell session line and no-role page; the design syst | UX lead | Recorded 2026-11-06 — confirmation owned by UX lead; the value stays data/configuration, the specification hard-codes nothing, and the item carries into the build hand-over. |

REVIEW_G2_STATUS: PASS
