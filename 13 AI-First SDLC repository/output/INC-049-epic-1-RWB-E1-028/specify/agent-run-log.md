# Technical Specifier run log - RWB-E1-028

**Run:** `INC-049-epic-1-RWB-E1-028`
**Agent:** Technical Specifier (`.github/agents/specify.agent.md`)
**Story:** RWB-E1-028 Service levels, timers, escalation and prescription dates
**Module:** P3 Case and workflow
**Status:** SUCCESS
**Outputs:** `output/INC-049-epic-1-RWB-E1-028/specify/spec.md`, `output/INC-049-epic-1-RWB-E1-028/specify/compliance-validation.md`

## 1. Preflight classification

| Evidence input | What was read | Result |
|---|---|---|
| Requirement text | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-007); the per-story file; the P3 FSD A2.11-A2.13 context and TSD P3 T3.1/T5.3 | New backend timing capability with no prior SPEC chain |
| Trace chain | `requirement/Traceability_Matrix.md` | `US-RWB-E1-028` exists; no prior `SPEC-*` for this capability |
| Implementation footprint | No ACE source code in this workspace | The story, TSD P3 and the API timer schema are the evidence |

**Classification:** `NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE]`; `Frontend Changes Required: NO`; `Backend Changes Required: YES`.

## 2. Questions and answers

### Q1. Does a timer start on case creation with status NEW?

**Answer:** No; the SERVICE_LEVEL timer starts on CaseAllocated, CaseTransferred or CaseStateChanged.
CaseCreated starts only the PRESCRIPTION timer.

**Source:** Story §4; CLAR-001; SPEC-001, SPEC-007.

### Q2. Does the working-day count include the start day?

**Answer:** No; the start day is day 0. AC1 and AC11 fix the boundaries.

**Source:** Story AC1, AC11; CLAR-002; SPEC-003, SPEC-004.

### Q3. Is the prescription warning 180 working or calendar days?

**Answer:** Calendar days; 2028-03-15 − 180 = 2027-09-17. The value is a parameter.

**Source:** Story AC3, §3; CLAR-003; SPEC-006.

### Q4. Where is a missing service level or legal period recorded?

**Answer:** On SCR-09 with MSG-P3-026; no timer or date is invented.

**Source:** Story AC4, AC5; CLAR-004; SPEC-002, SPEC-006.

### Q5. Does this story add the timer due date to SCR-03?

**Answer:** No; SCR-03 carries the prescription date from RWB-E1-023; the timer panel is RWB-E2-015. The
read endpoint is delivered here.

**Source:** Story §15; CLAR-005; SPEC-014.

### Q6. Does a breach move the case?

**Answer:** No; R-UNI-30 and AC2 keep the queue and owner.

**Source:** Story BR3, AC2; CLAR-006; SPEC-005.

### Q7. How is the pause duration counted?

**Answer:** By working days in the pause window; AC10 expects 2 working days for 2026-12-02 to 2026-12-04.

**Source:** Story AC10; CLAR-007; SPEC-011.

## 3. Verification performed

| Check | Result |
|---|---|
| All business rules mapped to SPEC IDs | Pass (9/9) |
| All acceptance criteria mapped | Pass (11/11) |
| All exception paths mapped | Pass (9/9) |
| Frontend/backend unit-test applicability consistent with scope | Pass (frontend NOT_APPLICABLE with evidence; backend REQUIRED, 80%) |
| API impact explicit | Pass (`NO_API_CHANGE`) |
| Design evidence status (`NOT_REQUIRED`) | Pass |
| Clarification log resolved | Pass (all resolved) |
| No PII, secrets or production data | Pass (case numbers only) |
| Compliance review | PASS_WITH_WARNINGS |

The traceability matrix update is deferred to the parent per the authoring guide §3; this run did not
modify any shared file.

## 4. Status

```text
SPEC_STATUS: SUCCESS
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE]
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
REVIEW_STATUS: PASS_WITH_WARNINGS [LOW: 3]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
