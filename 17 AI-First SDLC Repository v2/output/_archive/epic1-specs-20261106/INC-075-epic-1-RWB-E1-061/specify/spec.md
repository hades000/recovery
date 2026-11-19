# Technical Specification — RWB-E1-061 Intake agent evaluation and L1 proposal [E2a]

| Field | Value |
|---|---|
| Story | RWB-E1-061 — Intake agent evaluation and L1 proposal [E2a] |
| Epic / module | E1 / P10 Agent runtime |
| RUN_ID | `INC-075-epic-1-RWB-E1-061` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-019); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 061 Intake agent evaluation and L1 proposal E2a v1.md` |
| Upstream IDs | BRD-RWB-010; FR-RWB-019; AC-RWB-019; BR-RWB-013; REQ-DRI-010, REQ-DRI-011; US-RWB-E1-061; FEAT-AGT-07; R-UNI-32; DL11 |
| Status | `SUCCESS` — CLAR-001 resolved by decision D-RCV-33 (2026-11-06) |
| Regated | 2026-11-06 — Technical Specifier re-run after the grammar ruling and the API-spec media-type update |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen; the report is read and exported through the API. |
| Logic In Scope | `YES` — report aggregation, export, L1 proposal presence checks, condition checks, minimum sample and approval separation. |
| API In Scope | `YES` — new `GET /admin/agent-evaluations/{evaluationId}/report`, with `application/json`, `text/csv` and `application/pdf` representations. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `agent_evaluation_run`, `agent_evaluation`, `agent_run` (read); `agent_policy` (adds `evaluation_run_id`, `promotion_conditions`, `watch_measures`, `fallback_rule`); `AgentEvaluationController`. |
| New Nodes Required | `YES` — `EvaluationReportService`, `EvaluationReportExporter`, `PromotionProposalValidator`; report operation on `AgentEvaluationController`. |
| Inherited Existing Behavior | Intake shadow evaluation (RWB-E1-059), agent platform and policy loader (RWB-E1-058), decision log (RWB-E1-027), masking (RWB-E1-037), migrations (RWB-E1-044). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | An L1 proposal names one DONE evaluation run, the conditions, the fallback and the measures to watch. | SPEC-RWB-E1-061-004, SPEC-RWB-E1-061-005 | DIRECT | Four fields on `agent_policy`; all required for mode L1. | COVERED |
| BR2 | Every stated condition is checked against the scores of the named run before the version is stored. | SPEC-RWB-E1-061-006 | DIRECT (PROPOSED) | Proposed condition grammar; CLAR-001 open. | COVERED |
| BR3 | The minimum sample for an autonomy step is 200 cases (assumed; loader schema). | SPEC-RWB-E1-061-007 | DIRECT | Value in the policy JSON schema version. | COVERED |
| BR4 | Cost per case = total cost / runs, 4 decimals; latency percentiles include timeouts at 60,000 ms. | SPEC-RWB-E1-061-014 | DIRECT | `BigDecimal`; percentile over all runs. | COVERED |
| BR5 | The fallback of an L1 agent is the rule result. | SPEC-RWB-E1-061-004 | DIRECT | `fallback_rule` = `R-UNI-32`. | COVERED |
| BR6 | The loader and the approver are different people. | SPEC-RWB-E1-061-009 | DIRECT | Reuse the RWB-E1-058 check; 409 MSG-P7-002. | COVERED |
| AC1 | The report holds sample size 200, agreement per gap type, failure counts 7/3/2, total cost 412.6000, cost per case 2.0630, median 4,100 ms, p95 9,800 ms and the versions; no personal field. | SPEC-RWB-E1-061-001, SPEC-RWB-E1-061-002, SPEC-RWB-E1-061-010, SPEC-RWB-E1-061-014 | DIRECT | Aggregation from run and score rows. | COVERED |
| AC2 | P2 with L1, evaluation run, conditions, fallback and measures is stored LOADED; P1 stays in force until approval. | SPEC-RWB-E1-061-004, SPEC-RWB-E1-061-008, SPEC-RWB-E1-061-015 | DIRECT | `agent_policy` fields; effective dating. | COVERED |
| AC3 | A report on a RUNNING evaluation is refused 409 MSG-P10-008. | SPEC-RWB-E1-061-001, SPEC-RWB-E1-061-013 | DIRECT | Status check before aggregation. | COVERED |
| AC4 | An L1 proposal without measures is refused 422 MSG-P10-001 naming "measures to watch present". | SPEC-RWB-E1-061-004 | DIRECT | Presence check. | COVERED |
| AC5 | A score below a stated condition refuses the load 422 MSG-P10-001 naming the gap type and score. | SPEC-RWB-E1-061-006 | DIRECT (PROPOSED) | Proposed grammar; CLAR-001 open. | COVERED |
| AC6 | A sample below 200 is refused 422 MSG-P10-001 naming "sample size at least 200". | SPEC-RWB-E1-061-007 | DIRECT | Count runs in the evaluation. | COVERED |
| AC7 | The loader cannot approve the proposal: 409 MSG-P7-002. | SPEC-RWB-E1-061-009 | DIRECT | Separation of duty. | COVERED |
| X1 | Report requested while RUNNING. | SPEC-RWB-E1-061-001, SPEC-RWB-E1-061-013 | DIRECT | 409 MSG-P10-008. | COVERED |
| X2 | Proposal missing conditions, fallback or measures. | SPEC-RWB-E1-061-004 | DIRECT | 422 MSG-P10-001. | COVERED |
| X3 | Scores do not meet a stated condition. | SPEC-RWB-E1-061-006 | DIRECT (PROPOSED) | 422 naming the gap type and score. | COVERED |
| X4 | Sample size below 200. | SPEC-RWB-E1-061-007 | DIRECT | 422 naming the minimum. | COVERED |
| X5 | Loader approves own proposal. | SPEC-RWB-E1-061-009 | DIRECT | 409 MSG-P7-002. | COVERED |
| X6 | Role without the right. | SPEC-RWB-E1-061-011 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **the evaluation report of the case intake agent and the proposal to run it at autonomy level 1, built from the stored shadow results**, so that **the risk and model risk officer approves the step to L1 on measured results**.

The story turns the stored shadow runs into one report and one versioned policy row. It adds no
screen. The report is counts and rates only; the proposal is stored `LOADED` and changes nothing until
RW-RISK approves it and its `valid_from` date arrives.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `GET /admin/agent-evaluations/{evaluationId}/report`; `POST /admin/agent-configs` with mode L1; `POST /admin/agent-configs/{versionId}/approve`. |
| Preconditions | RWB-E1-059 evaluation run on `INTAKE-S1` v1 is DONE with 200 labeled cases; policy `INTAKE` P1 (SHADOW) in force; RW-COE holds Rules and parameters C; RW-RISK holds A. |
| Input | Stored `agent_run`, `agent_evaluation_run`, `agent_evaluation`; the proposed policy file. |
| Output | Report JSON/CSV/PDF; policy version P2 `LOADED`, then `APPROVED` on the valid-from date. |
| Feature flag | `rwb.agent.promotion`. Off: a policy with mode L1 is refused 422. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `agent_evaluation_run` | `status` | Harness | Read-only | Report only when `DONE`. |
| `agent_evaluation_run` | `total_cost_thb`, `p95_latency_ms`, `failure_counts` | Harness | Read-only | Report inputs. |
| `agent_evaluation` | `agreement_rate`, `precision_value`, `recall_value`, `sample_size` | Scorer | Read-only | Per gap type. |
| `agent_policy` | `autonomy_mode` | Proposal file | `SHADOW` → `L1` on approval | Only `L1` triggers the proposal checks. |
| `agent_policy` | `evaluation_run_id` | Proposal file | System-written | Must name a DONE run. |
| `agent_policy` | `promotion_conditions` | Proposal file | System-written | jsonb; grammar proposed in SPEC-006 (CLAR-001). |
| `agent_policy` | `watch_measures` | Proposal file | System-written | jsonb; presence required. |
| `agent_policy` | `fallback_rule` | Proposal file | System-written | `R-UNI-32`. |
| `agent_policy` | `status` | Load | `LOADED` → `APPROVED` | Loader ≠ approver. |
| `agent_policy` | `valid_from` | Proposal file | System-written | P1 remains in force until this date. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | L1 proposal loaded | All checks pass | `LOADED` | Conditions, fallback, measures and run ID stored. |
| None | L1 proposal loaded | A check fails | No row | 422 MSG-P10-001; version in force unchanged. |
| `LOADED` | Approved by RW-RISK | Approver ≠ loader | `APPROVED` | Effective on `valid_from`; P1 retired from that date. |
| `LOADED` | Approved by the loader | Same user | No change | 409 MSG-P7-002. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Report on a RUNNING evaluation | 409; no report | MSG-P10-008 |
| X2 | Missing conditions, fallback or measures | 422; no row | MSG-P10-001 |
| X3 | Score below a stated condition | 422 naming gap type and score | MSG-P10-001 |
| X4 | Sample below 200 | 422 naming the minimum | MSG-P10-001 |
| X5 | Loader approves own proposal | 409; stays LOADED | MSG-P7-002 |
| X6 | Role without the right | 403; nothing changes | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoint | `GET /api/recovery/v1/admin/agent-evaluations/{evaluationId}/report` (API-P10-008). |
| Existing endpoints used | `POST /admin/agent-configs` (API-P10-003); `POST /admin/agent-configs/{versionId}/approve` (API-P10-004). |
| Contract delta | The report endpoint supports `application/json`, `text/csv` and `application/pdf`; `api.yaml` currently declares JSON only. The CSV/PDF are representations of the same object, not a second endpoint. |
| Backward compatibility | New endpoint; config and approval responses unchanged. |
| Authorization | Rules and parameters R for the report; C for the load; A for approval. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 unknown run; 409 not DONE (MSG-P10-008); 422 MSG-P10-001; 503. |
| Versioning | New endpoint; additive representations; no version bump. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-019; SPEC-RWB-E1-061-001..015 | New report service, exporter and proposal validator. | Positive, negative, boundary and error-path tests: 200-run fixture, RUNNING refusal, missing measures, condition breach, 199/200 sample, self-approval, access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `AgentEvaluationController` | Controller | Adds the report operation. |
| `EvaluationReportService` | Service | Aggregates runs and scores into the report. |
| `EvaluationReportExporter` | Service | Writes CSV and PDF from the same report object. |
| `PromotionProposalValidator` | Service | BR1..BR3 checks inside `AgentConfigService` for mode L1. |

### Package and boundaries

`recovery.agent.eval.report`; policy checks in `recovery.agent.config`. Reads only P10 tables and the
P7 decision log is not involved. No other module's table is read.

### Data and migration

`V10_004__policy_promotion.sql` adds `evaluation_run_id` uuid, `promotion_conditions` jsonb,
`watch_measures` jsonb and `fallback_rule` varchar(20) to `agent_policy` (all already in the logical
data model, DF-AGT-017..020). Reads `agent_run`, `agent_evaluation_run`, `agent_evaluation`.

### Report

- Sample size: count of `agent_run` rows with the evaluation run ID.
- Agreement per gap type: from `agent_evaluation`.
- Failure counts: from `failure_counts` (TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR).
- Total cost: sum of `agent_run.cost_thb`; cost per case = total / runs, 4 decimals.
- Median and p95 latency: computed over all runs; a timeout counts at 60,000 ms.
- Versions: policy, prompt and model from the evaluation run.
- No personal field; the report holds counts and rates only.

### Proposal checks (approved as D-RCV-33)

1. `autonomy_mode = L1`.
2. `evaluation_run_id` names a run with status `DONE`.
3. `sample_size >= 200` (value in the policy JSON schema version).
4. `promotion_conditions`, `watch_measures` and `fallback_rule = "rule result per R-UNI-32"` are
   present.
5. The single condition clause is evaluated against the run's per-gap-type agreement scores; a
   breach refuses the proposal naming the gap type and value (MSG-P10-001 class).
6. On success, store `LOADED`; P1 remains in force until approval.

Approved condition grammar (D-RCV-33, 2026-11-06): `promotion_conditions` holds exactly one clause
form, `{"metric":"AGREEMENT_RATE","operator":"GTE","threshold":<number>` in 0..1 with at most two
decimals`,"scope":"EVERY_LABEL_KEY"}` — in prose, "agreement at least <threshold> for every gap
type". Any other metric, operator, scope or a second clause is refused at load. `watch_measures`
hold rows for `ACCEPTANCE_RATE` (GTE), `CORRECTION_RATE` (GTE) and `FALLBACK_RATE` (LTE) with their
thresholds; they are stored and reported, and do not gate the proposal. The form is the one the
FSD P10 fixture states ("agreement at least 0.85 for every gap type", fallback "rule result per
R-UNI-32", watch measures acceptance, correction rate, fallback rate below 0.10).

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-COE | Rules and parameters CRUD | All |
| RW-RISK | Rules and parameters A; read | All |
| RW-AUDIT | Rules and parameters R | All |
| `SY-RULES` | Rules and parameters R | All |

### Observability, performance and rollback

- Metrics: reports generated, report latency, proposal loads, condition failures, approvals.
- Alerts: report generation failure, repeated condition failure, self-approval attempt.
- Performance: the report reads one evaluation run's rows; target under 2 seconds (NFR-008) for a
  200-run sample.
- Feature flag `rwb.agent.promotion`: off refuses mode L1 with 422.
- Rollback: flag off; redeploy the previous tag; the added columns are nullable.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-061-01 | AC1, BR4 | System | EV-INTAKE-001, 200 runs, 412.6000 baht | Sample 200; counts 7/3/2; 2.0630; 4,100/9,800; versions; no personal field |
| TC-E1-061-02 | AC2, BR1, BR5 | System | Policy P2 L1 with all three parts | Stored LOADED; P1 in force until approval |
| TC-E1-061-03 | AC3 | System | EV-INTAKE-002 RUNNING | 409 MSG-P10-008 |
| TC-E1-061-04 | AC4, BR1 | System | L1 policy without measures | 422 MSG-P10-001 "measures to watch present" |
| TC-E1-061-05 | AC5, BR2 | System | NO_CONTACT_POINT 0.8150 | 422 naming "NO_CONTACT_POINT 0.8150 below 0.85" |
| TC-E1-061-06 | AC6, BR3 | System | EV-INTAKE-003 sample 150 | 422 naming "sample size at least 200" |
| TC-E1-061-07 | AC7, BR6 | System | Loader approves own P2 | 409 MSG-P7-002 |
| TC-E1-061-08 | X6 | Security | RW-CASEOWN requests the report | 403 MSG-P4-002 |
| TC-E1-061-09 | AC1 | System | `Accept: text/csv` and `application/pdf` | Same figures as JSON |
| TC-E1-061-10 | AC2 | System | Approval with valid-from 2026-12-15 | P2 effective on the date; P1 retired |
| TC-E1-061-11 | BR4 | Unit | 200 runs, one 60,000 ms timeout | p95 includes 60,000; cost per case 4 decimals |

## Guardrails and out of scope

- No business value in code: conditions, measures and the minimum sample are row/schema values.
- No personal data in logs, tests or the report; counts and rates only.
- No read of another module's table.
- A proposal never changes the mode in force before approval and its valid-from date.
- Out of scope: showing the intake summary to case owners at L1 (RWB-E2-028); changing an autonomy
  level from a screen (FEAT-AGT-12, Epic 3); the committee meeting and minutes.

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | Program 5.7 | FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32 | TC-E1-061-01..06, 09..11 |
| REQ-DRI-011 | Every versioned table has valid-from/to, author and approver | Program 5.7 | FEAT-AGT-07 | 06 Take over and own the case | None | TC-E1-061-02, 07, 08, 10 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR2, AC2, AC5; SPEC-006 | What is the machine-checkable grammar of `promotion_conditions` and `watch_measures`? The story gives prose ("agreement at least 0.85 for every gap type") but `jsonb` needs a schema the validator can evaluate and test. | Without a grammar the condition check cannot be implemented generally; a hard-coded single sentence would violate the no-hard-coding rule. | **Ruled 2026-11-06 as D-RCV-33:** the promotion grammar is restricted to exactly one clause form per version — `{"metric":"AGREEMENT_RATE","operator":"GTE","threshold":<number>,"scope":"EVERY_LABEL_KEY"}` ("agreement at least <threshold> for every gap type"); any other metric, operator, scope or a second clause is refused at load. `watch_measures` hold ACCEPTANCE_RATE (GTE), CORRECTION_RATE (GTE) and FALLBACK_RATE (LTE) rows for reporting and do not gate. The form is the FSD P10 AC-ALT-P10-007-01 fixture. With the restricted grammar, AC5's 0.8150 for a gap type refuses the proposal naming the gap type and value (TC-E1-061-05). | `RESOLVED` | SPEC-006 |
| CLAR-002 | Contract; SPEC-003 | The report endpoint supports JSON, CSV and PDF; `api.yaml` declares JSON only. | Export and client generation. | Add `text/csv` and `application/pdf` to the 200 response; one endpoint, three representations. | RESOLVED | SPEC-003 |
| CLAR-003 | AC1; SPEC-002 | Is sample size the score row's `sample_size` or the run count? | Report denominator. | Count `agent_run` rows with the evaluation run ID; cross-check with the score sample sizes. | RESOLVED | SPEC-002 |
| CLAR-004 | BR4, AC1; SPEC-014 | The evaluation run stores p95 but not median; where does median come from? | Report value. | Compute both percentiles from `agent_run.latency_ms`; a timeout counts at 60,000 ms. | RESOLVED | SPEC-014 |
| CLAR-005 | BR3; SPEC-007 | Where is the minimum sample 200 held? | Loader check. | A value in the policy JSON schema version used by the loader, per story §13. | RESOLVED | SPEC-007 |
| CLAR-006 | AC2; SPEC-008 | Does loading P2 change the mode in force? | Behaviour before approval. | No; P1 stays in force until RW-RISK approves P2 and its valid-from date arrives. | RESOLVED | SPEC-008 |
| CLAR-007 | AC1; SPEC-010 | Does the report contain any personal field? | PDPA. | No; counts, rates, cost and versions only. | RESOLVED | SPEC-010 |
| CLAR-008 | X3, AC5; SPEC-006 | What does a condition failure name? | Error detail. | The gap type and the measured value against the threshold. | RESOLVED | SPEC-006 |
| CLAR-009 | BR4; SPEC-014 | Is cost per case divided by runs or cases? | Report value. | By runs (200), giving 2.0630 for 412.6000. | RESOLVED | SPEC-014 |

`CLARIFICATION_STATUS: RESOLVED` — no open items. The grammar is approved as D-RCV-33 and the
report representations are in API Specification v2.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this report story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New evaluation report endpoint and L1 policy proposal checks; no screen; three report representations.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new report endpoint plus CSV/PDF representations]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 7 acceptance criteria, 6 exception paths and 4 policy states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Start the Implementation Planner on this specification.
```
