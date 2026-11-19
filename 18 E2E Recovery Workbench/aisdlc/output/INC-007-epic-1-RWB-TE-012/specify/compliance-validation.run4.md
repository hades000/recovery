# Compliance validation — RWB-TE-012 specification (specifier self-check)

| Field | Value |
|---|---|
| Artifact | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` v4 |
| Stage | Technical Specifier self-check before spec gate round 4 (remediation run 3) |
| Date | 2026-11-18 |
| Round 1 gate | `review/spec-gate-review.md`: FAIL (0 Critical, 1 High, 5 Medium, 5 Low). The orchestrator (Claude Code) ran that gate; v1 of this file wrongly said the specifier spawned it (corrected, SG-07) |
| Round 2 gate | `review/spec-gate-review-2.md`: FAIL (0 Critical, 0 High, 2 Medium, 4 Low); Compliance Reviewer spawned by this specifier run |
| Round 3 gate | `review/spec-gate-review-3.md`: FAIL (0 Critical, 0 High, 1 Medium, 7 Low); Compliance Reviewer spawned by this specifier run. Triage by the orchestrator (Claude Code), logged at 04:54 (D-RUN-09) |
| Round 4 gate | `review/spec-gate-review-4.md` |
| Previous versions | `compliance-validation.run1.md` (v1), `.run2.md` (v2), `.run3.md` (v3) |

## 1. Required spec structure (`.github/rules/specification-execution-gates.md`)

| Item | Present | Where |
|---|---|---|
| `Status:` line | Yes, `Status: SUCCESS` | spec.md line 3 |
| Change Scope Declaration with all fields; New Nodes Required YES/NO | Yes, "YES" then the list (template, parameter files, `RUNBOOK.md`, `dochub` types) | spec.md "Change Scope Declaration" |
| Requirement-to-SPEC Logic Coverage | Yes, 37 rows, 37 covered, 0 blocked; Coverage Type only `DIRECT` or `INHERITED_EXISTING_BEHAVIOR`, Status only `COVERED`; FR-RWB-007, REQ-DCM-002/-003, NFR-029, NFR-053, CTL-09, CTL-12 have own rows | spec.md |
| `CONTRADICTIONS` | Bare number, 0; counting rule stated (only unresolved contradictions; precedence-settled conflicts listed as DGAP rows) | spec.md coverage summary and "Status reporting" |
| User story intent; entry trigger and preconditions | Yes; precondition "RWB-TE-001 merged" | spec.md |
| Field-level matrix | Yes (properties incl. `readiness-recheck-seconds`, BlobRef, BlobWriteRequest, StoredBlob, metadata, audit event, health detail incl. `identities`) | spec.md |
| Status-transition matrix | Yes (readiness, with single-flight and freshness rows) | spec.md |
| Exceptional-case behaviour | Yes, X1–X10 plus five | spec.md |
| API change assessment | Yes, NO_API_CHANGE; published Java surface recorded | spec.md; `contracts/backend-apis.json` v4 |
| Unit Test Applicability | Yes, one frontend and one backend row; four counters | spec.md |
| Frontend / Backend Specification | Yes, SPEC-001 to -023; tests T-TE012-01 to -17 | spec.md |
| Clarification Log | Yes, 23 rows, RESOLVED | spec.md |
| Status lines | Yes | spec.md "Status reporting" |

## 2. Rule checks

| Check | Result | Evidence |
|---|---|---|
| Every statement cites a source or is a labelled assumption | Pass | "Sources cited"; `assumptions.md` ASM-TE012-01 to -31 |
| Every number states its source | Pass | `timeout-seconds` 10 from story §13 and AC10; `readiness-recheck-seconds` 30 assumed (ASM-TE012-30); SPEC-009 "Numbers and where they come from" |
| AC10 bound when the hub is not READY | Pass | SPEC-009 single-flight probe with a `timeout-seconds` deadline; T-TE012-17 |
| Placement per the predecessor's module map | Pass | `dochub.api`, `dochub.storage` per RWB-TE-001 v4 SPEC-009, -022, -025; SPEC-016, -022 |
| Baseline evolved, not duplicated (A-04) | Pass | Evolution map: each baseline element has one successor; no second adapter |
| Carried tests not weakened | Pass | T-TE012-14 maps each RWB-TE-001 SPEC-024 assertion to a successor |
| Later-story contracts conformed to, seams named (D-RUN-08) | Pass | SPEC-010, -019; `shared-updates.md` §7 (E1-017 DGAP-22, E1-054 DGAP-23) |
| Coverage per RWB-TE-001 v4 SPEC-020, outside `check`, no exclusion | Pass | SPEC-023; Unit Test Applicability |
| Health flag-off behaviour sourced; no storage call on health reads | Pass | SPEC-009, -020; DGAP-21; ASM-TE012-20 |
| Template format and PROD lock | Pass with recorded gaps | SPEC-001 (format reason), SPEC-004 (runbook step: owner, approver, evidence); DGAP-09, DGAP-24 |
| Tests do not depend on `.env` or commit a key | Pass | SPEC-018 "How tests set the profile and the emulator string": runtime-generated keys, explicit properties |
| Local stack and existing `.env` upgrade | Pass | SPEC-021; T-TE012-13; Builder evidence step |
| No new dependency (AGENTS.md §4.4) | Pass | ASM-TE012-16; virtual threads are JDK 21; Jackson, Testcontainers, Mockito already present |
| No credential in code or configuration | Pass with recorded local exception | SPEC-017 (published Azurite key, `.env` / `.env.example` only); tests generate their own keys |
| No personal data | Pass | UUIDs; synthetic test data; audit carries staff subject and IDs only |
| No migration (D-RUN-07) | Pass | No table or column |
| Feature flag returns the previous path when off (AGENTS.md §3.13) | Pass | Off: no client, store and open refused, root health unchanged (SPEC-008, -020) |
| No question to the user (L-RCV-03) | Pass | Clarification Log; assumptions |
| Shared files untouched | Pass | `shared-updates.md` v4 (11 open items) |
| Document gaps evidenced, blockers only where no precedence rule settles | Pass | `document-gaps.md`: 23 active rows (DGAP-01 to -17, -19 to -24), DGAP-18 withdrawn, 0 blockers |
| MCP | N/A | None connected |
| Design evidence | NOT_REQUIRED | No UI |

## 3. Known limits carried to the plan

- System tests TC-TE-012-01 to -12 need the SIT storage account; locally `PENDING_ENVIRONMENT`.
- AC9 "no document row" and the HTTP 409/503 mappings are verified in RWB-E1-024 / RWB-E1-026 (SPEC-019, DGAP-17).
- Early DEV spike for versioning next to the legal policy (DGAP-03).
- README "Decisions taken" row and `RUNBOOK.md` are plan-gate items (SPEC-004, -017).
- Template format is an assumption (ASM-TE012-03, DGAP-09); environment values for the template come from the platform team (open item).

## 4. Gate result

Round 4: `SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 2] [LOW: 5]` (`review/spec-gate-review-4.md`). SG-18, -19, -20, -22 to -25 and TE012-SG3-DG-01 FIXED; SG-21 PARTIAL (now SG-30). New: SG-26 and SG-27 (Medium), SG-28 to SG-32 (Low). No new review-level gap; DGAP-23 and -24 accepted. Medium findings remain, so the run stops for orchestrator triage. No human acceptance recorded.
