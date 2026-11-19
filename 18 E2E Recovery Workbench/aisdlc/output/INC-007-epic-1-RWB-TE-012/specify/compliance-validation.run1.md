# Compliance validation — RWB-TE-012 specification (specifier self-check)

| Field | Value |
|---|---|
| Artifact | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` |
| Stage | Technical Specifier self-check before the spec gate |
| Date | 2026-11-17 |
| Independent gate review | `output/INC-007-epic-1-RWB-TE-012/review/spec-gate-review.md` (Compliance Reviewer, general-purpose subagent) |

## 1. Required spec structure (`.github/rules/specification-execution-gates.md`)

| Item | Present | Where |
|---|---|---|
| Change Scope Declaration with all fields | Yes | spec.md "Change Scope Declaration" |
| Requirement-to-SPEC Logic Coverage, DIRECT / INHERITED, COVERED / BLOCKED | Yes, 28 rows, 0 blocked | spec.md |
| User story intent | Yes | spec.md |
| Entry trigger and preconditions | Yes | spec.md |
| Field-level matrix | Yes (properties, StoreRequest, BlobRef, metadata, audit event, health detail) | spec.md |
| Status-transition matrix | Yes (readiness only; story §9 has no status change) | spec.md |
| Exceptional-case behaviour | Yes, X1–X10 plus three | spec.md |
| API change assessment | Yes, NO_API_CHANGE | spec.md; `contracts/backend-apis.json` |
| Unit Test Applicability, one frontend and one backend row | Yes | spec.md |
| Frontend Specification / Backend Specification | Yes | spec.md |
| Clarification Log (CLAR schema) | Yes, 12 rows, RESOLVED | spec.md |
| Status lines | Yes | spec.md "Status reporting" |

## 2. Rule checks

| Check | Result | Evidence |
|---|---|---|
| Every statement cites a source with name and version, or is a labelled assumption | Pass | "Sources cited" table; `assumptions.md` ASM-TE012-01 to -19 |
| Container names, retention, access tier and encryption taken from the document set, not from code | Pass | Names from story v7, D-RCV-31, FSD P5 v3; retention from story (assumed, DL26); tier, encryption, redundancy, region recorded as DGAP-05, -06, -07, -13 with no invented value |
| Baseline code treated as baseline: adds and corrections stated, nothing duplicated | Pass | spec.md "Baseline" |
| No new dependency (AGENTS.md §4.4) | Pass | ASM-TE012-16 |
| No credential in code or configuration (AGENTS.md §4.1; story §17) | Pass with recorded local exception | SPEC-007, SPEC-017 (published Azurite key, DEV only, `.env`) |
| No personal data (RUN-BRIEF rule 7) | Pass | UUID names; synthetic examples; audit carries staff subject and IDs only |
| Module boundaries (BND-5, Modulith) | Pass | SPEC-008, SPEC-010; DGAP-02 |
| No migration (D-RUN-07) | Pass | No table or column (story §13 "Database") |
| Later-story work named as seams (D-RUN-08) | Pass | SPEC-019 |
| Tests before code; 80% line and branch | Pass | SPEC-018; Unit Test Applicability |
| Feature flag returns the previous path when off (AGENTS.md §3.13) | Pass | Off: no client built, writes refused; there is no earlier caller path (zero callers) |
| No question to the user (L-RCV-03) | Pass | Clarification Log; assumptions |
| Shared files untouched (RUN-BRIEF rule 3) | Pass | `shared-updates.md` |
| README items 1–7 not re-reported | Pass | `document-gaps.md` header |
| MCP | N/A | No Jira, Confluence, GitLab or Figma MCP (RUN-BRIEF rule 5) |
| Design evidence | NOT_REQUIRED | No UI |

## 3. Known limits carried to the plan

- System tests TC-TE-012-01 to -12 need the SIT storage account; locally they are `PENDING_ENVIRONMENT`.
- AC9 "no document row" and the HTTP 409/503 mappings are verified in RWB-E1-024 / RWB-E1-026 (SPEC-019, DGAP-17).
- Template format is an assumption (ASM-TE012-03).

## 4. Gate result

`review/spec-gate-review.md`: **FAIL**, 0 Critical, 1 High, 5 Medium, 5 Low. Handoff to the Implementation Planner is blocked until a human resolves or accepts the findings and this stage and its review are rerun.
