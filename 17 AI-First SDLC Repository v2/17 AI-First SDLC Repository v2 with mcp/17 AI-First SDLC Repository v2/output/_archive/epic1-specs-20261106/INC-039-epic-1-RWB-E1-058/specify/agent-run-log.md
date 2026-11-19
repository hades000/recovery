# Technical Specifier run log - RWB-E1-058

**Run:** `INC-039-epic-1-RWB-E1-058`
**Agent:** Technical Specifier (`.github/agents/specify.agent.md`)
**Story:** RWB-E1-058 Agent platform set-up [E1a]
**Module:** P10 Agent runtime
**Status:** SUCCESS
**Outputs:** `output/INC-039-epic-1-RWB-E1-058/specify/spec.md`, `output/INC-039-epic-1-RWB-E1-058/specify/compliance-validation.md`

## 1. Preflight classification

| Evidence input | What was read | Result |
|---|---|---|
| Requirement text | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-019); the per-story file; the P10 FSD and TSD | New platform capability with no prior SPEC chain |
| Trace chain | `requirement/Traceability_Matrix.md` | `US-RWB-E1-058` exists; no prior `SPEC-*` for P10 |
| Implementation footprint | No ACE source code in this workspace | The story, TSD and build notes are the evidence |

**Classification:** `NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED]`; `Frontend Changes Required: NO`; `Backend Changes Required: YES`.

## 2. Questions and answers

The Technical Specifier asks only where the story is ambiguous. Each question below was answered
from the story, the build notes, the architecture or the decision log. The full table is in
`spec.md` §Clarification Log.

### Q1. Does `POST /admin/agent-evaluations` answer 201 or 202?

**Answer:** 202 per story §12 and the build notes; `api.yaml` says 201 and is corrected as a
documentation defect.

**Source:** Story §12; build notes step 9; CLAR-001; SPEC-019.

### Q2. Do score rows carry the policy, prompt and model versions?

**Answer:** The versions live on `agent_evaluation_run`; the score read joins them so each returned
score row carries them. No duplicate columns.

**Source:** TSD T3; story AC4; CLAR-002; SPEC-017.

### Q3. What is `bodyHash` for a POLICY version?

**Answer:** Add `agent_policy.body_hash` and populate it from the canonical policy file; prompt
hashes stay unchanged.

**Source:** Story §12; TSD T3; CLAR-003; SPEC-024.

### Q4. Does the harness run once per sample row or per subject?

**Answer:** Once per distinct subject, then score per label key. This reconciles AC4, RWB-E1-059
(200 cases) and RWB-E1-060 (one run per document).

**Source:** Story AC4; build notes; CLAR-004; SPEC-017.

### Q5. Where do agent-specific parameters with no column live?

**Answer:** `agent_policy.config` (jsonb), loaded and approved with the policy. TSD T3 needs the
column added.

**Source:** Story §13; TSD T3; CLAR-007; SPEC-024.

## 3. Verification performed

| Check | Result |
|---|---|
| All business rules mapped to SPEC IDs | Pass |
| All acceptance criteria mapped | Pass |
| All exception paths mapped | Pass |
| Frontend/backend unit-test applicability consistent with scope | Pass |
| API impact explicit | Pass |
| Design evidence status (`NOT_REQUIRED`) | Pass |
| Clarification log resolved | Pass (all resolved) |
| No PII, secrets or production data | Pass |
| Compliance review | PASS_WITH_WARNINGS |

The traceability matrix update is deferred to the parent per the authoring guide §3; this run did not
modify any shared file.

## 4. Status

```text
SPEC_STATUS: SUCCESS
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED]
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 11] [COVERED_RULES: 11] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
REVIEW_STATUS: PASS_WITH_WARNINGS [LOW: 3]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
