# Technical Specifier run log - RWB-E1-022

**Run:** `INC-031-epic-1-RWB-E1-022`
**Agent:** Technical Specifier (`.github/agents/specify.agent.md`)
**Story:** RWB-E1-022 Sign-on with SSO, MFA and the first roles
**Module:** P4 Access and administration
**Status:** SUCCESS
**Outputs:** `output/INC-031-epic-1-RWB-E1-022/specify/spec.md`, `output/INC-031-epic-1-RWB-E1-022/specify/compliance-validation.md`

## 1. Preflight classification

| Evidence input | What was read | Result |
|---|---|---|
| Requirement text | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-011); the per-story file; the P4 FSD and TSD | New access capability with no prior SPEC chain |
| Trace chain | `requirement/Traceability_Matrix.md` | `US-RWB-E1-022` exists; no prior `SPEC-*` for this capability |
| Implementation footprint | No ACE source code in this workspace | The story, TSD P4 and API Specification v2 are the evidence; no implemented route to inspect |

**Classification:** `NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED]`; `Frontend Changes Required: YES`; `Backend Changes Required: YES`.

## 2. Questions and answers

The Technical Specifier asks only where the story is ambiguous. Each question below was answered from the story, the architecture, the API specification or the decision log. The full table is in `spec.md` §Clarification Log.

### Q1. Does the MFA check apply to service identities?

**Answer:** No. AC7 expects a 403 role refusal for SY-RULES, not a 401 MFA refusal. NFR-051 applies the same role checks to service identities; the `amr` check applies to `BANK_USER` roles only.

**Source:** Story AC7, BR2, BR6; NFR-051; CLAR-002; SPEC-002, SPEC-010.

### Q2. How does the menu know which areas the session may read?

**Answer:** `GET /me/session` adds an additive `permissions` array (`capabilityArea`, `letters`); the shell filters a menu manifest built from the screen inventory. The matrix table is not read by the front end.

**Source:** Story AC1, §13; API-P4-012; CLAR-004; SPEC-008.

### Q3. Is the session path `/me/session` or `/api/recovery/v1/me/session`?

**Answer:** The API base path applies: `GET /api/recovery/v1/me/session`.

**Source:** API Specification v2, API-P4-012; CLAR-001; SPEC-001.

### Q4. Is the conflict check symmetric when the table lists one direction?

**Answer:** Yes; the resolver tests both directions. The table stores the pair as written.

**Source:** Story BR5, AC6; CLAR-003; SPEC-004.

### Q5. Is `GET /admin/roles` delivered in this story?

**Answer:** Yes; API-P4-007 is first in E1 and the story contract defines its response.

**Source:** Story §12; TSD appendix T-A; CLAR-008; SPEC-009.

## 3. Verification performed

| Check | Result |
|---|---|
| All business rules mapped to SPEC IDs | Pass (8/8) |
| All acceptance criteria mapped | Pass (9/9) |
| All exception paths mapped | Pass (7/7) |
| Frontend/backend unit-test applicability consistent with scope | Pass (both `REQUIRED`, 80%) |
| API impact explicit | Pass (`NEW_API_REQUIRED`; two endpoints; additive field) |
| Design evidence status | Pass (`AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1]`) |
| Clarification log resolved | Pass (10/10) |
| No PII, secrets or production data | Pass |
| Compliance review | `PASS_WITH_WARNINGS` (3 Low) |

The traceability matrix update is deferred to the parent per the authoring guide §3; this run did not modify any shared file.

## 4. Status

```text
SPEC_STATUS: SUCCESS
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED]
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
REVIEW_STATUS: PASS_WITH_WARNINGS [LOW: 3]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
