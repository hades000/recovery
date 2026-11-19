# Technical Specifier run log - RWB-E1-018

**Run:** `INC-040-epic-1-RWB-E1-018`
**Agent:** Technical Specifier (`.github/agents/specify.agent.md`)
**Story:** RWB-E1-018 Case ID issuance and case record v1
**Module:** P3 Case and workflow
**Status:** BLOCKED
**Outputs:** `output/INC-040-epic-1-RWB-E1-018/specify/spec.md`, `output/INC-040-epic-1-RWB-E1-018/specify/compliance-validation.md`

## 1. Preflight classification

| Evidence input | What was read | Result |
|---|---|---|
| Requirement text | `requirement/RecoveryWorkbench_Requirements.md`; the per-story file; the P3 FSD and TSD | New functional flow with no prior SPEC chain |
| Trace chain | `requirement/Traceability_Matrix.md` | `US-RWB-E1-018` exists; no prior `SPEC-*` for this capability |
| Implementation footprint | No ACE source code in this workspace | The story and TSD P3 are the evidence; no implemented route to inspect |

**Classification:** `NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE]`; `Frontend Changes Required: NO`; `Backend Changes Required: YES`.

## 2. Questions and answers

The Technical Specifier asks only where the story is ambiguous. Each question below was answered
from the story, the architecture or the decision log. The full table is in `spec.md` §Clarification
Log.

### Q1. Is `caseNo` in API Specification v2?

**Answer:** No. The story says "see additions"; add optional `caseNo` (max 18, exact match) to `GET /cases`, backward compatible. The OpenAPI file is updated before implementation.

**Source:** Story §12; CLAR-001; SPEC-011.

### Q2. When several accounts are grouped into one case, which account is `is_primary`?

**Answer:** OPEN. The source says only "the account the case was opened on" and gives no selection rule. This changes which account is primary and which contract number later notices use.

**Source:** Story BR2, AC3; data dictionary DF-CAS-027; CLAR-009; SPEC-004.

### Q3. Is a gap in case numbers allowed after a rollback?

**Answer:** Yes; the number was never attached to a visible case. "Never reused" is the rule, not "gapless".

**Source:** Story BR4, AC11; CLAR-003; SPEC-005.

### Q4. What happens when the decision log write fails?

**Answer:** The whole transaction rolls back: no case, links, party or outbox row; the account is retried next run.

**Source:** Story AC10, BR8; CLAR-006; SPEC-008.


## 3. Verification performed

| Check | Result |
|---|---|
| All business rules mapped to SPEC IDs | Pass |
| All acceptance criteria mapped | Pass |
| All exception paths mapped | Pass |
| Frontend/backend unit-test applicability consistent with scope | Pass |
| API impact explicit | Pass |
| Design evidence status (`NOT_REQUIRED`) | Pass |
| Clarification log resolved | Fail (1 open) |
| No PII, secrets or production data | Pass |
| Compliance review | FAIL |

The traceability matrix update is deferred to the parent per the authoring guide §3; this run did not
modify any shared file.

## 4. Status

```text
SPEC_STATUS: BLOCKED
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE]
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 10] [COVERED_RULES: 10] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 1] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]
CLARIFICATION_STATUS: OPEN [OPEN_ITEMS: 1]
REVIEW_STATUS: FAIL [HIGH: 1]
NEXT_STEP: Business analyst to answer CLAR-009 in the data dictionary, then re-run the Technical Specifier.
```
