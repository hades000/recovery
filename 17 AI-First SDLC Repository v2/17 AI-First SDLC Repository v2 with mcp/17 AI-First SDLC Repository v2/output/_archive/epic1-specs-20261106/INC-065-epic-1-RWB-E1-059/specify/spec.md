# Technical Specification — RWB-E1-059 Case intake agent in shadow [E1b]

| Field | Value |
|---|---|
| Story | RWB-E1-059 — Case intake agent in shadow [E1b] |
| Epic / module | E1 / P10 Agent runtime |
| RUN_ID | `INC-065-epic-1-RWB-E1-059` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-019); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 059 Case intake agent in shadow E1b v1.md` |
| Upstream IDs | BRD-RWB-010; FR-RWB-019; AC-RWB-019; BR-RWB-013; REQ-ACA-005, REQ-ACA-010; US-RWB-E1-059; FEAT-AGT-03; R-UNI-32, R-UNI-40; CTL-11 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen; no case owner sees the shadow output. |
| Logic In Scope | `YES` — event listener, five-tool input assembly, masking, schema and stale-input checks, shadow isolation, scoring and partial-label handling. |
| API In Scope | `YES` — the evaluation endpoints from RWB-E1-058 are reused, but this story adds one additive response field, `unlabeledSubjectIds`, to `AgentEvaluationRun` to satisfy AC7. |
| API Impact Type | `EXISTING_API_CHANGE` |
| Impacted Existing Nodes | `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation` (from RWB-E1-058); `AgentEvaluationRun` response schema. |
| New Nodes Required | `YES` — `IntakeShadowListener`, `IntakeInputAssembler`, `IntakeOutputScorer`, `intake-summary-v1` schema and INTAKE prompt. |
| Inherited Existing Behavior | Agent platform (RWB-E1-058), agent client (RWB-TE-013), case creation and allocation (RWB-E1-018/030), masking (RWB-E1-037), documents and fields (RWB-E1-053), interaction ledger (RWB-E1-066/067). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | In SHADOW mode the output is stored and never shown; nothing on the case changes. | SPEC-RWB-E1-059-005, SPEC-RWB-E1-059-016 | DIRECT | No case, task, queue or decision log write; no user endpoint returns the output. | COVERED |
| BR2 | The agent runs once per case per business date on EV-01 CaseCreated. | SPEC-RWB-E1-059-001, SPEC-RWB-E1-059-006 | DIRECT | Run key `INTAKE:<caseId>:<businessDate>`; event ID check. | COVERED |
| BR3 | Gap types are the enum in the approved output schema, not code. | SPEC-RWB-E1-059-003 | DIRECT | `intake-summary-v1` enum: MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT, STALE_INPUT. | COVERED |
| BR4 | When an input is older than the business date, the answer must include STALE_INPUT. | SPEC-RWB-E1-059-004 | DIRECT | `data_as_of` from the latest COLLINS load; `SCHEMA_RULE` fails a missing flag. | COVERED |
| BR5 | Agreement rate = agreeing cases / labeled cases, 4 decimals. | SPEC-RWB-E1-059-008 | DIRECT | Per gap type; 182/200 = 0.9100. | COVERED |
| BR6 | A run that times out or fails a check is not retried for the same event. | SPEC-RWB-E1-059-007 | DIRECT | Terminal run row; no retry. | COVERED |
| BR7 | Personal fields are masked before the model call. | SPEC-RWB-E1-059-002 | DIRECT | P4 masking on every input value; summary holds tokens only. | COVERED |
| AC1 | 200 cases produce 200 shadow runs with a summary and gap flags; no case, task, queue or decision log change; no output through case endpoints or run list. | SPEC-RWB-E1-059-001, SPEC-RWB-E1-059-002, SPEC-RWB-E1-059-005, SPEC-RWB-E1-059-011 | DIRECT | Mode SHADOW; output only on the run row; run list projection excludes it. | COVERED |
| AC2 | One score row per gap type with agreement, precision, recall and sample size 200; MISSING_DOCUMENT 182 agreeing gives 0.9100; versions on each row. | SPEC-RWB-E1-059-008 | DIRECT | Score read joins versions from the evaluation run. | COVERED |
| AC3 | A new case starts one run with key `INTAKE:<caseId>:2026-11-30`, trigger CaseCreated, mode SHADOW. | SPEC-RWB-E1-059-001 | DIRECT | Listener on EV-01. | COVERED |
| AC4 | A failed run is stored TIMED_OUT, fallback true, not retried; failure count 1. | SPEC-RWB-E1-059-007 | DIRECT | Failure counts on the evaluation run. | COVERED |
| AC5 | A stale COLLINS load gives `data_as_of` 2026-11-28 and STALE_INPUT; an answer without it fails `SCHEMA_RULE`. | SPEC-RWB-E1-059-004 | DIRECT | Check runs in the guardrail. | COVERED |
| AC6 | A repeated CaseCreated event leaves one run for the case and date and counts the repeat. | SPEC-RWB-E1-059-006 | DIRECT | Event ID plus run key. | COVERED |
| AC7 | A sample labeled for 180 of 200 cases scores on 180 and lists the 20 unlabeled cases. | SPEC-RWB-E1-059-009 | DIRECT | Additive `unlabeledSubjectIds` on the evaluation run response. | COVERED |
| AC8 | An empty sample is refused 422 MSG-P10-002. | SPEC-RWB-E1-059-010 | DIRECT | No evaluation or run row. | COVERED |
| X1 | Timeout or guardrail failure on a case. | SPEC-RWB-E1-059-007 | DIRECT | Terminal run; failure counted; no retry. | COVERED |
| X2 | Stale COLLINS load. | SPEC-RWB-E1-059-004 | DIRECT | `data_as_of` stale; STALE_INPUT required. | COVERED |
| X3 | Same CaseCreated event twice. | SPEC-RWB-E1-059-006 | DIRECT | One run; repeat counted. | COVERED |
| X4 | Labels cover fewer cases than the sample. | SPEC-RWB-E1-059-009 | DIRECT | Score on labeled cases; list unlabeled. | COVERED |
| X5 | A user endpoint is asked for shadow output. | SPEC-RWB-E1-059-011, SPEC-RWB-E1-059-016 | DIRECT | Metadata only; no content. | COVERED |
| X6 | Evaluation on an empty sample. | SPEC-RWB-E1-059-010 | DIRECT | 422 MSG-P10-002. | COVERED |
| X7 | Role without the right. | SPEC-RWB-E1-059-012 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **the case intake agent to build a case file summary and flag gaps for every new Epic 1 case in shadow mode**, so that **the agent is scored against the business analysts' review before any case owner sees its output**.

The story adds no screen and changes no case. It turns every CaseCreated event into one shadow run,
stores the summary and gap flags with masking tokens, and scores them per gap type. The agreement rate
is the evidence for the L1 decision in RWB-E2-028 and the report in RWB-E1-061.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | EV-01 `CaseCreated` from the outbox. |
| Preconditions | RWB-E1-058 and RWB-TE-013 done; RWB-E1-030 creates cases and publishes EV-01; approved policy `INTAKE` P1 (SHADOW, timeout 60, floor 0.80, five allowed tools, schema `intake-summary-v1`); approved prompt PR1; sample `INTAKE-S1` v1. |
| Input | Case, accounts, documents, valuations and contact points through the five tools; latest COLLINS load date. |
| Output | One `agent_run` per case and business date with summary, gap flags, status, versions, latency, tokens, cost and `data_as_of`; evaluation run and score rows. |
| Feature flag | `rwb.agent.intake-shadow`. Off: the listener ignores CaseCreated. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `agent_run` | `autonomy_mode` | Policy | System-written | Fixed `SHADOW`. |
| `agent_run` | `trigger_event` | Event | System-written | `CaseCreated`; `EVALUATION` for a harness run. |
| `agent_run` | `idempotency_key` | Listener | System-written | `INTAKE:<caseId>:<businessDate>`, unique. |
| `agent_run` | `output` | Model answer | System-written | Summary ≤1,500 chars with masking tokens; gaps array; confidence. |
| `agent_run` | `data_as_of` | Latest COLLINS load | System-written | Stale date drives STALE_INPUT. |
| `agent_run` | `status`, `fallback` | Guardrail | System-written | `ANSWERED`, `TIMED_OUT`, `GUARDRAIL_FAILED`, `BELOW_FLOOR`. |
| `agent_sample` | `expected_value` | Analyst review | Read-only | `Y`/`N`; null means unlabeled. |
| `agent_evaluation` | `agreement_rate` | Scorer | System-written | 4 decimals; labeled cases only. |
| `agent_evaluation_run` | `status` | Harness | `RUNNING` → `DONE` | One RUNNING per agent/sample/version. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | EV-01 CaseCreated | Flag on; policy in force | `ANSWERED` | Summary and gaps stored; no case change. |
| None | EV-01 CaseCreated | Timeout or guardrail failure | `TIMED_OUT` / `GUARDRAIL_FAILED` / `BELOW_FLOOR` | Fallback true; failure counted; no retry. |
| None | Evaluation started | Sample has labels; none running | `RUNNING` | Evaluation run row. |
| `RUNNING` | Last case scored | No error | `DONE` | Score rows per gap type. |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Timeout or guardrail failure | Terminal run; failure counted; no retry | None to a user |
| X2 | Stale COLLINS load | `data_as_of` stale; STALE_INPUT required; missing flag fails `SCHEMA_RULE` | None to a user |
| X3 | Same CaseCreated event twice | One run; repeat counted | None to a user |
| X4 | Fewer labels than cases | Score on labeled cases; list unlabeled | None to a user |
| X5 | User endpoint asked for shadow output | Metadata only; no content | None to a user |
| X6 | Empty sample | 422; no run rows | MSG-P10-002 |
| X7 | Role without the right | 403; nothing changes | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `EXISTING_API_CHANGE` — one additive response field. |
| Existing endpoints used | `POST /api/recovery/v1/admin/agent-evaluations`, `GET /api/recovery/v1/admin/agent-evaluations`, `GET /api/recovery/v1/admin/agent-runs`. |
| Contract delta | `AgentEvaluationRun` gains `unlabeledSubjectIds` (array of UUID, read-time computed from `agent_sample` rows with null `expected_value`); no persisted column and no change to existing fields. |
| Backward compatibility | Additive; existing clients ignore the new field. |
| Authorization | Rules and parameters C/R for evaluations; Platform administration R for run metadata. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P10-003; 422 MSG-P10-002; 503. |
| Versioning | Additive field; no version bump. The OpenAPI schema is updated in the same change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-019; SPEC-RWB-E1-059-001..016 | New listener, assembler and scorer; additive response projection. | Positive, negative, boundary and error-path tests: event, repeat, timeout, stale input, 180/200 labels, empty sample, access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `IntakeShadowListener` | Listener | Consumes EV-01; calls `AgentOrchestrator` with the run key. |
| `IntakeInputAssembler` | Service | Builds the masked input set from the five tools. |
| `IntakeOutputScorer` | Service | Compares gap flags with labels per gap type. |
| `intake-summary-v1.json` | Rule table | Output schema with the gap-type enum. |
| prompt `INTAKE` PR1 | Rule table | Prompt text loaded through the config endpoint. |

### Package and boundaries

`recovery.agent.intake`. The listener consumes EV-01; the assembler calls P3 `CaseQueryService`
(`getCase`, `getAccounts`, `getContactPoints`), P5 `DocumentQueryService.listByCase` and P1
`CollateralQueryService.listValuations` as `SY-AGENT`. No other module's table is read.

### Data and migration

No migration. Reads: `recovery_case`, `document`, `valuation`, `contact_point`, `agent_sample`.
Writes: `agent_run`, `agent_evaluation_run`, `agent_evaluation`. The summary and gaps live in
`agent_run.output`; `data_as_of` holds the latest COLLINS load date.

### Run and check sequence

1. Resolve the approved policy and prompt in force.
2. Call the five tools; mask every personal value through P4.
3. Call the model with the policy timeout.
4. Guardrail: schema (`intake-summary-v1`), tool list, floor, then `SCHEMA_RULE` for stale input.
5. Write `agent_run` and EV-28 in one transaction; no case write.
6. On repeat: find the run by event ID and run key; return it; count the hit.

### Evaluation and partial labels

The harness runs the agent once per sample case in SHADOW and writes one score row per gap type:
sample size, TP, FP, FN, agreement, precision and recall. A sample row with null `expected_value` is
unlabeled: it is excluded from the counts, and its subject ID is returned in `unlabeledSubjectIds` on
the evaluation run. The score read joins the policy, prompt and model versions from the run.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| `SY-AGENT` | Case record R, Documents R | All |
| `SY-CASEWF` | Publishes CaseCreated | All |
| RW-COE | Rules and parameters CRUD | All |
| RW-RISK | Rules and parameters R | All |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Platform administration R | All |
| RW-CASEOWN | No access to the shadow output | Own |

### Observability, performance and rollback

- Metrics: runs by status, fallback rate, gap flags per type, agreement, cost, latency, repeat count.
- Alerts: no run for a day, timeout spike, fallback rate above 10 percent, stale input spike.
- Performance: one model call per case; 200 cases in the DEV run; 60-second policy timeout.
- Feature flag `rwb.agent.intake-shadow`: off means the listener ignores CaseCreated.
- Rollback: flag off; redeploy the previous tag; no schema change.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-059-01 | AC1, BR1 | System | 200 synthetic cases, 30 Nov–4 Dec | 200 shadow runs; no case, task, queue or decision log change; no output through case endpoints |
| TC-E1-059-02 | AC2, BR5 | System | INTAKE-S1 v1; 182 agreeing MISSING_DOCUMENT | One score row per gap type; agreement 0.9100; versions present |
| TC-E1-059-03 | AC3, BR2 | System | Case RW-2026-000301 created 30 Nov | One run, key `INTAKE:<caseId>:2026-11-30`, trigger CaseCreated, SHADOW |
| TC-E1-059-04 | AC4, BR6 | System | Stub silent for RW-2026-000302 | `TIMED_OUT`, fallback true, no retry, failure count 1 |
| TC-E1-059-05 | AC5, BR4 | System | COLLINS load 28 Nov, business date 30 Nov | `data_as_of` 28 Nov; STALE_INPUT; missing flag fails `SCHEMA_RULE` |
| TC-E1-059-06 | AC6, BR2 | System | Same event ID twice | One run; repeat counted |
| TC-E1-059-07 | AC7, BR5 | System | INTAKE-S1 v2, 180 of 200 labeled | Sample size 180; 20 IDs in `unlabeledSubjectIds` |
| TC-E1-059-08 | AC8 | System | INTAKE-S3 with no rows | 422 MSG-P10-002; no run rows |
| TC-E1-059-09 | X7 | Security | RW-CASEOWN calls evaluations | 403 MSG-P4-002 |
| TC-E1-059-10 | BR7 | System | Synthetic national ID and mobile | Request, run and log hold masking tokens only |
| TC-E1-059-11 | AC1, X5 | System | GET case, timeline and run list after a run | No summary or gap flags returned |
| TC-E1-059-12 | BR5 | Unit | 180 labeled, 182 agreeing, 200 cases | 0.9100; unlabeled excluded |

## Guardrails and out of scope

- No business value in code: gap types, prompt, timeout and floor are approved rows.
- No personal data in logs, tests or prompts; the summary holds masking tokens only.
- No read of another module's table; inputs come through P1, P3 and P5.
- No shadow output in any user-facing response.
- Out of scope: the evaluation report and L1 proposal (RWB-E1-061); showing the summary to the case
  owner (RWB-E2-028, Epic 3); document classification and field extraction (RWB-E1-053, RWB-E1-060).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-005 | Personal data masked in every agent call | Program 5.4 | FEAT-AGT-03 | 06 Take over and own the case | CTL-11 | TC-E1-059-01, 10 |
| REQ-ACA-010 | Agents run under service identities with role checks | Program 5.4 | FEAT-AGT-03 | 06 Take over and own the case | R-UNI-32, R-UNI-40 | TC-E1-059-02..09, 11 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC7; SPEC-009 | Where is the list of unlabeled cases stored or returned? | AC7 cannot be verified without a representation. | Additive `unlabeledSubjectIds` on `AgentEvaluationRun`, computed from `agent_sample` rows with null `expected_value`; no table change. OpenAPI updated. | RESOLVED | SPEC-009 |
| CLAR-002 | AC1, AC2; SPEC-008 | Does the harness run once per case or per sample row? | Run count and cost. | Once per case; scores per gap type. 200 cases give 200 runs even when the sample has four rows per case. | RESOLVED | SPEC-008 |
| CLAR-003 | BR4, AC5; SPEC-004 | Which input date sets `data_as_of`? | Stale check. | The latest COLLINS load date for the case's data products; if it is before the business date, STALE_INPUT is required. | RESOLVED | SPEC-004 |
| CLAR-004 | AC7; SPEC-009 | Is a sample with 180 labels a 180-row or 200-row sample? | Sample size and unlabeled list. | 200 rows, 20 with null `expected_value`; scores use 180, the list uses the 20. | RESOLVED | SPEC-009 |
| CLAR-005 | BR2, AC3, AC6; SPEC-006 | Is the run key the business date or the event ID? | Idempotency. | Both checks: event ID and `INTAKE:<caseId>:<businessDate>`. | RESOLVED | SPEC-006 |
| CLAR-006 | Flow 7; SPEC-015 | Does the evaluation reuse shadow runs or re-run the agent? | Cost and run count. | Re-runs the agent in SHADOW on each sample case, with `evaluation_run_id` set. | RESOLVED | SPEC-015 |
| CLAR-007 | Feature flag; SPEC-013 | What happens when the flag is off? | Event handling. | The listener ignores CaseCreated; no run row, no model call. | RESOLVED | SPEC-013 |
| CLAR-008 | AC1; SPEC-016 | Does the shadow run write a decision log entry? | Audit. | No; the output is not a decision and no case changes. | RESOLVED | SPEC-016 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the build notes or the TSD.
No item changes a business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this shadow agent story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New shadow intake agent; one additive evaluation response field; no screen; evaluation and run endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE] [REASON: additive unlabeledSubjectIds field on AgentEvaluationRun]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 8 acceptance criteria, 7 exception paths and 4 run/evaluation states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
