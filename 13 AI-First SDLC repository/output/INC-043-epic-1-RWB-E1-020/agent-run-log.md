# Technical Specifier run log — RWB-E1-020

**Run:** `INC-043-epic-1-RWB-E1-020`
**Agent:** Technical Specifier (`.github/agents/specify.agent.md`)
**Story:** RWB-E1-020 Allocation and assignment engine v1
**Module:** P3 Case and workflow
**Status:** SUCCESS
**Outputs:** `output/INC-043-epic-1-RWB-E1-020/specify/spec.md`,
`output/INC-043-epic-1-RWB-E1-020/specify/compliance-validation.md`

## 1. Preflight classification

| Evidence input | What was read | Result |
|---|---|---|
| Requirement text | `requirement/RecoveryWorkbench_Requirements.md` FR-RWB-005; the worked example v6; the Epic 1 build sequence | New functional flow: a daily allocation job, rule evaluation, assignment, overflow, exception, deviation, decision log, events |
| Trace chain | `requirement/Traceability_Matrix.md` | `US-RWB-E1-020` exists; no prior `SPEC-*` for this capability |
| Implementation footprint | No ACE source code in this workspace | Cannot verify implemented routes/services; the story and TSD P3 are the evidence |

**Classification:** `NEW_STORY`; `UI In Scope: NO`; `Logic In Scope: YES`; `API In Scope: NO`;
`API Impact Type: NO_API_CHANGE`; `Frontend Changes Required: NO`; `Backend Changes Required: YES`.

## 2. Questions and answers

The Technical Specifier asks only where the story is ambiguous. Each question below was answered
from the story, the architecture or the decision log. The full table is in `spec.md` §Clarification
Log.

### Q1. Is the allocation table version `ALLOC-2026.11` approved?

**Answer:** Yes. It is loaded and approved under DL24; the version is reference data, not a code
constant.

**Source:** Story §3, §4.4; Decision Log v8 (DL24).

**Verification:** The story names the version and the approval; the reference data service (RWB-E1-043)
holds it; the rule load (RWB-E1-029) validates it. No contradiction.

### Q2. Are `RWB-EXC` and `DEV-HANDLER` the approved queue codes?

**Answer:** They are the assumed values under DL23. The spec treats them as parameters
(`allocation.exception.queue.code`, `allocation.deviation.queue.code`), not code. Confirm before
go-live.

**Source:** Story §3, §4.3, X2, X4; RWB-E1-042 parameter catalogue; DL23.

**Verification:** The story uses the codes; the parameter catalogue holds them; the decision log says
the values are placeholders. The spec records the assumption.

### Q3. Is JOB-03 scheduled after JOB-02 and complete by 07:00?

**Answer:** Yes. JOB-03 starts after JOB-02 completes for the business date and must complete by 07:00
Asia/Bangkok.

**Source:** Story §4.1, §12; Batch and Scheduling Design v2; NFR-013, NFR-019.

**Verification:** The story contract, the batch design and the NFR agree. If JOB-02 has not completed,
JOB-03 waits and the job monitor shows MSG-P1-001.

### Q4. Does the allocation job need a new API?

**Answer:** No. The job is scheduled. The existing `GET /cases/{caseId}` reads the result and
`POST /admin/jobs/{jobId}/rerun` reruns it. No contract delta.

**Source:** API Specification v2; story §12; spec API change assessment.

**Verification:** The API spec has both paths; the story uses them; no new endpoint is required.

### Q5. Is the decision log write synchronous before commit?

**Answer:** Yes. The write is the last step before commit; a failure rolls back the allocation.

**Source:** Story §4.7, BR7; ADR-009; CTL-06; RWB-E1-027.

**Verification:** The story, the ADR and the control agree. The spec makes the rollback explicit.

### Q6. What if a queue has no overflow queue?

**Answer:** The case goes to the exception queue `RWB-EXC` with reason `NO_OVERFLOW_QUEUE`; status
stays `NEW`.

**Source:** Story AC13, X9; BR4; spec SPEC-011, SPEC-012.

**Verification:** AC13 and X9 agree. The exception queue is a parameter.

### Q7. Are the cap 150 and `ROUND_ROBIN` fixed?

**Answer:** No. They are data values; the example uses 150 and `ROUND_ROBIN` as test fixtures. The
queue table holds `assignment_method` and `capacity_cap`.

**Source:** Story BR2, BR3; DF-WRK-006, DF-WRK-007; LOV-ASSIGN; DL23.

**Verification:** The data model and the story agree. The spec prohibits hard-coding.

### Q8. What are the event names and payloads?

**Answer:** `CaseAllocated` (EV-02: caseId, queueId, ownerId, ruleId, ruleVersion) and
`CaseAllocationFailed` (EV-03: caseId, reason, ruleGap).

**Source:** Story §12; Event and Messaging Design v2; outbox TE-006.

**Verification:** The story and the event design agree. The outbox writes in the same transaction.

### Q9. In what order does the job process cases?

**Answer:** Ascending `created_at`, then `case_id`, recorded in the job run log. This is an
implementation decision for deterministic replay; the acceptance criteria are per case and do not
depend on the order.

**Source:** Story §4.2 (selects every NEW case whose last allocation date is before the business
date); no explicit order in the source.

**Verification:** The decision does not change any AC outcome; it is recorded as an implementation
note and a Low review finding.

## 3. Verification performed

| Check | Result |
|---|---|
| All 9 business rules mapped to SPEC IDs | Pass |
| All 13 acceptance criteria mapped | Pass |
| All 10 exception paths mapped | Pass |
| All 4 state transitions mapped | Pass |
| Frontend/backend unit-test applicability consistent with scope | Pass |
| API impact explicit (`NO_API_CHANGE`) | Pass |
| Design evidence status (`NOT_REQUIRED`) | Pass |
| Clarification log resolved | Pass (9/9) |
| Traceability matrix updated with unique SPEC IDs | Pass |
| No PII, secrets or production data | Pass |
| Compliance review | `PASS_WITH_WARNINGS`, 0 Critical/High/Medium, 4 Low + 1 resolved |

## 4. Status

```text
SPEC_STATUS: SUCCESS
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE]
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
REVIEW_STATUS: PASS_WITH_WARNINGS [LOW: 4]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
