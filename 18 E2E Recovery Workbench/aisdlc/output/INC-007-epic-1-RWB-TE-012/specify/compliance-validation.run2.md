# Compliance validation — RWB-TE-012 specification (specifier self-check)

| Field | Value |
|---|---|
| Artifact | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` v2 |
| Stage | Technical Specifier self-check before spec gate round 2 |
| Date | 2026-11-18 |
| Round 1 gate | `review/spec-gate-review.md`: FAIL (0 Critical, 1 High, 5 Medium, 5 Low). The orchestrator (Claude Code) ran that gate; v1 of this file wrongly said the specifier spawned it (corrected, SG-07) |
| Round 2 gate | `review/spec-gate-review-2.md`, Compliance Reviewer spawned by this specifier run as a general-purpose subagent |
| Previous version | `compliance-validation.run1.md` |

## 1. Required spec structure (`.github/rules/specification-execution-gates.md`)

| Item | Present | Where |
|---|---|---|
| `Status:` line | Yes, `Status: SUCCESS` | spec.md line 3 |
| Change Scope Declaration with all fields; New Nodes Required YES/NO | Yes, "YES" then the list | spec.md "Change Scope Declaration" |
| Requirement-to-SPEC Logic Coverage | Yes, 36 rows, 0 blocked; FR-RWB-007, REQ-DCM-002/-003, NFR-029, NFR-053, CTL-09, CTL-12 have own rows | spec.md |
| User story intent; entry trigger and preconditions | Yes; precondition "RWB-TE-001 merged" | spec.md |
| Field-level matrix | Yes (properties, BlobRef, BlobWriteRequest, StoredBlob, metadata, audit event, health detail) | spec.md |
| Status-transition matrix | Yes (readiness) | spec.md |
| Exceptional-case behaviour | Yes, X1–X10 plus five | spec.md |
| API change assessment | Yes, NO_API_CHANGE; published Java surface recorded | spec.md; `contracts/backend-apis.json` |
| Unit Test Applicability | Yes, one frontend and one backend row; four counters | spec.md |
| Frontend / Backend Specification | Yes, SPEC-001 to -023 | spec.md |
| Clarification Log | Yes, 17 rows, RESOLVED | spec.md |
| Status lines | Yes | spec.md "Status reporting" |

## 2. Rule checks

| Check | Result | Evidence |
|---|---|---|
| Every statement cites a source or is a labelled assumption | Pass | "Sources cited"; `assumptions.md` ASM-TE012-01 to -27 |
| Placement per the predecessor's module map | Pass | `dochub.api`, `dochub.storage` per RWB-TE-001 v4 SPEC-009, -022, -025; SPEC-016, -022 |
| Baseline evolved, not duplicated (A-04) | Pass | Evolution map: each baseline element has one successor; no second adapter |
| Carried tests not weakened | Pass | T-TE012-14 maps each RWB-TE-001 SPEC-024 assertion to a successor; T-TE001-14 list replaced as a published-surface change (SPEC-022) |
| Later-story contracts conformed to, seams named (D-RUN-08) | Pass | SPEC-010, -019; `shared-updates.md` §7 |
| Coverage per RWB-TE-001 v4 SPEC-020, outside `check`, no exclusion | Pass | SPEC-023; Unit Test Applicability |
| Health flag-off behaviour sourced; no storage call on health reads | Pass | SPEC-009, -020; DGAP-21; ASM-TE012-20 |
| Local stack and existing `.env` upgrade | Pass | SPEC-021; T-TE012-13; Builder evidence step |
| No new dependency (AGENTS.md §4.4) | Pass | ASM-TE012-16 |
| No credential in code or configuration | Pass with recorded local exception | SPEC-017 (published Azurite key, `.env` / `.env.example` only, behind `rwb.dochub.storage.emulator`) |
| No personal data | Pass | UUIDs; synthetic test data; audit carries staff subject and IDs only |
| No migration (D-RUN-07) | Pass | No table or column |
| Feature flag returns the previous path when off (AGENTS.md §3.13) | Pass | Off: no client, store and open refused, root health unchanged (SPEC-020) |
| No question to the user (L-RCV-03) | Pass | Clarification Log; assumptions |
| Shared files untouched | Pass | `shared-updates.md` |
| Document gaps evidenced, blockers only where no precedence rule settles | Pass | `document-gaps.md`: 20 active rows, DGAP-18 withdrawn, 0 blockers |
| MCP | N/A | None connected |
| Design evidence | NOT_REQUIRED | No UI |

## 3. Known limits carried to the plan

- System tests TC-TE-012-01 to -12 need the SIT storage account; locally `PENDING_ENVIRONMENT`.
- AC9 "no document row" and the HTTP 409/503 mappings are verified in RWB-E1-024 / RWB-E1-026 (SPEC-019, DGAP-17).
- Early DEV spike for versioning next to the legal policy (DGAP-03).
- README "Decisions taken" row is a plan-gate item (SPEC-017).
- Template format is an assumption (ASM-TE012-03).

## 4. Gate result

Recorded in `spec.md` "Status reporting" and `gate-response.md` after `review/spec-gate-review-2.md`.
