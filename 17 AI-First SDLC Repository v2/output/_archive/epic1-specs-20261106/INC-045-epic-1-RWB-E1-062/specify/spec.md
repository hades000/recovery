# Technical Specification — RWB-E1-062 Deviation screening agent in shadow [E2b]

| Field | Value |
|---|---|
| Story | RWB-E1-062 — Deviation screening agent in shadow [E2b] |
| Epic / module | E1 / P10 Agent runtime |
| RUN_ID | `INC-045-epic-1-RWB-E1-062` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-019); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 062 Deviation screening agent in shadow E2b v1.md` |
| Upstream IDs | BRD-RWB-010; FR-RWB-019; AC-RWB-019; BR-RWB-013; REQ-DVH-001, REQ-DVH-003, REQ-DVH-007; US-RWB-E1-062; FEAT-DVH-01, FEAT-DVH-04, FEAT-DVH-08, FEAT-AGT-08; R-DEV-02..R-DEV-06; R-UNI-40; LOV-DEVIATION |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen; no case owner or handler sees a proposal. |
| Logic In Scope | `YES` — event listeners, masked input assembly, schema and rule checks, owner-role resolution, review marking, shadow isolation and scoring. |
| API In Scope | `NO` — no new or changed REST contract. The story reuses the RWB-E1-058 evaluation endpoints and `GET /admin/agent-runs`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation` (from RWB-E1-058); `agent_policy.config` (design extension); P3 case and rule interfaces; P5 documents; P7 interaction ledger. |
| New Nodes Required | `YES` — `ScreeningShadowListener`, `ScreeningInputAssembler`, `ScreeningOwnerResolver`, `ScreeningRuleChecks`, `ScreeningScorer`, `screening-v1` schema and SCREENING prompt. |
| Inherited Existing Behavior | Agent platform (RWB-E1-058), agent client (RWB-TE-013), case events (RWB-E1-018/030), interaction ledger (RWB-E1-066/067), documents and fields (RWB-E1-053), rules (RWB-E1-029), masking (RWB-E1-037). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | In SHADOW mode the agent raises nothing: no deviation record, clock pause or contact stop. | SPEC-RWB-E1-062-007, SPEC-RWB-E1-062-015 | DIRECT | The listener never calls the S8 deviation service; `deviation_open` unchanged. | COVERED |
| BR2 | A proposal carries a code from LOV-DEVIATION, reasons, source references and a confidence. | SPEC-RWB-E1-062-003 | DIRECT | `screening-v1` schema; code list X1..X7. | COVERED |
| BR3 | The owner role is read from R-DEV-02..R-DEV-06; a code with no row maps to RW-TEAMMGR and is marked unmapped. | SPEC-RWB-E1-062-004 | DIRECT | `ScreeningOwnerResolver`; fallback role and marker. | COVERED |
| BR4 | An X1 proposal names the latest interaction in the 30 days before the complaint. | SPEC-RWB-E1-062-005 | DIRECT | 30 days from `agent_policy.config.lookback_days`; check `SCHEMA_RULE`. | COVERED |
| BR5 | Proposals below the floor are marked review and scored separately. | SPEC-RWB-E1-062-006, SPEC-RWB-E1-062-010 | DIRECT | Marker in output; `review_count` on the evaluation run. | COVERED |
| BR6 | Precision and recall per code use proposals at or above the floor against Y/N labels. | SPEC-RWB-E1-062-010 | DIRECT | Review proposals excluded from TP/FP/FN. | COVERED |
| BR7 | One run per case per triggering event. | SPEC-RWB-E1-062-008 | DIRECT | Key `SCREENING:<caseId>:<eventId>`; unique key. | COVERED |
| AC1 | 200 cases produce 200 shadow runs with proposed codes, reasons and source refs; no deviation, no contact stop, no user endpoint. | SPEC-RWB-E1-062-001, SPEC-RWB-E1-062-002, SPEC-RWB-E1-062-007, SPEC-RWB-E1-062-015 | DIRECT | Mode SHADOW; output stored on the run only. | COVERED |
| AC2 | One score row per code X1..X7 with precision, recall and sample size 200; X6 18/2/6 gives 0.9000 and 0.7500. | SPEC-RWB-E1-062-010 | DIRECT | `agent_evaluation` per code; 4 decimals. | COVERED |
| AC3 | A new DEATH_CERTIFICATE document starts one shadow run with trigger `DocumentStored`. | SPEC-RWB-E1-062-001 | DIRECT | EV-16 listener; run key from event ID. | COVERED |
| AC4 | X4 carries owner role RW-FRAUD from R-DEV-04; an unmapped code gets RW-TEAMMGR and `unmapped`. | SPEC-RWB-E1-062-004 | DIRECT | Rule evaluator `ownerFor`; fallback. | COVERED |
| AC5 | X1 names the 2026-11-25 outbound call before the 2026-11-27 complaint; a missing preceding contact fails `SCHEMA_RULE`. | SPEC-RWB-E1-062-005 | DIRECT | Latest interaction in the 30-day window. | COVERED |
| AC6 | X2 with confidence 0.72 is marked `review` and excluded from precision/recall. | SPEC-RWB-E1-062-006, SPEC-RWB-E1-062-010 | DIRECT | Floor 0.80; `review_count`. | COVERED |
| AC7 | A repeated EV-16 event ID leaves one run and counts the repeat. | SPEC-RWB-E1-062-008 | DIRECT | Event ID plus run key. | COVERED |
| AC8 | Code X9 fails `SCHEMA`; run `GUARDRAIL_FAILED`, fallback true. | SPEC-RWB-E1-062-003, SPEC-RWB-E1-062-009 | DIRECT | Schema enum X1..X7. | COVERED |
| AC9 | A 61-second silence gives `TIMED_OUT` and no retry for the event. | SPEC-RWB-E1-062-009 | DIRECT | Policy timeout; failure counted. | COVERED |
| X1 | Code outside X1..X7. | SPEC-RWB-E1-062-003, SPEC-RWB-E1-062-009 | DIRECT | `GUARDRAIL_FAILED`, `SCHEMA`. | COVERED |
| X2 | Proposal below the floor. | SPEC-RWB-E1-062-006 | DIRECT | `review` marker. | COVERED |
| X3 | X1 names no preceding contact while one exists in 30 days. | SPEC-RWB-E1-062-005 | DIRECT | `SCHEMA_RULE` fails the run. | COVERED |
| X4 | Same event twice. | SPEC-RWB-E1-062-008 | DIRECT | One run; repeat counted. | COVERED |
| X5 | Proposed code has no owner row. | SPEC-RWB-E1-062-004 | DIRECT | RW-TEAMMGR; `unmapped`. | COVERED |
| X6 | Agent times out. | SPEC-RWB-E1-062-009 | DIRECT | `TIMED_OUT`; not retried. | COVERED |
| X7 | Role without the right. | SPEC-RWB-E1-062-013 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **the deviation screening agent to propose X1 to X7 with reasons from case data, call notes and documents, in shadow on Epic 1 cases**, so that **the Epic 2 and Epic 3 deviation flags start from an agent with measured precision and recall per deviation type**.

The story adds no screen and raises no deviation. It turns two existing events into shadow runs, stores
the proposals with their would-be owner roles, and scores them against the analysts' review. The
measured precision and recall per code are the evidence for the L1 segment decision in RWB-E2-029.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | EV-01 `CaseCreated` and EV-16 `DocumentStored` from the outbox. |
| Preconditions | RWB-E1-058 and RWB-TE-013 done; approved policy `SCREENING` P1 (SHADOW, timeout 60, floor 0.80, allowed tools read_case/read_interactions/read_documents/read_document_fields, output schema `screening-v1`); approved prompt PR1; R-DEV-02..R-DEV-06 loaded; sample `SCREEN-S1` v1 with 200 cases × 7 codes. |
| Input | Case, interaction ledger entries (180-day window), documents and their fields, open deviations, rule rows. |
| Output | One `agent_run` per event with proposals, owner roles, markers, confidence, latency, tokens and cost; one evaluation run and score rows per code. |
| Feature flag | `rwb.agent.screening-shadow`. Off: both listeners ignore their events. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `agent_run` | `autonomy_mode` | Policy | System-written | Fixed `SHADOW` in this story. |
| `agent_run` | `trigger_event` | Event | System-written | `CaseCreated` or `DocumentStored`. |
| `agent_run` | `idempotency_key` | Listener | System-written | `SCREENING:<caseId>:<eventId>`, unique. |
| `agent_run` | `output` | Model answer | System-written | `screening-v1`: proposals with code, reasons, source refs, `precedingContactId`, confidence, `ownerRole`, `unmapped`, `review`. |
| `agent_run` | `status`, `fallback` | Guardrail | System-written | `ANSWERED`, `GUARDRAIL_FAILED`, `TIMED_OUT`, `BELOW_FLOOR`. |
| `agent_evaluation_run` | `review_count` | Scorer | System-written | Count of proposals below the floor. |
| `agent_evaluation` | `label_key` | Code | System-written | X1..X7. |
| `agent_evaluation` | `precision_value`, `recall_value` | Scorer | System-written | 4 decimals; review proposals excluded. |
| `agent_policy` | `config` | Policy file | Read-only | `lookback_days` 30, `ledger_window_days` 180. |
| `recovery_case` | `deviation_open` | Case | Read-only | Must stay false; no write. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | EV-01 or EV-16 | Flag on; policy in force | `agent_run` `ANSWERED` | Output stored; no case change. |
| None | EV-01 or EV-16 | Schema or rule check fails | `GUARDRAIL_FAILED` | Fallback true; failure counted. |
| None | EV-01 or EV-16 | Timeout | `TIMED_OUT` | Fallback true; no retry. |
| None | Evaluation started | Sample has labels; none running | `RUNNING` | Evaluation run row. |
| `RUNNING` | Last code scored | No error | `DONE` | Score rows and `review_count`. |

This story changes no case status and never fires R-DEV-01.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Code outside X1..X7 | `SCHEMA`; `GUARDRAIL_FAILED`; fallback true | None to a user |
| X2 | Proposal below floor 0.80 | Stored with `review`; scored separately | None to a user |
| X3 | X1 without a preceding contact when one exists in 30 days | `SCHEMA_RULE`; run fails | None to a user |
| X4 | Same event ID twice | One run; repeat counted | None to a user |
| X5 | No owner row for a code | `RW-TEAMMGR`; `unmapped` | None to a user |
| X6 | Timeout | `TIMED_OUT`; no retry | None to a user |
| X7 | Role without the right | 403; nothing changes | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/admin/agent-evaluations`, `GET /api/recovery/v1/admin/agent-evaluations`, `GET /api/recovery/v1/admin/agent-runs`. |
| Contract delta | None. The proposals are inside `agent_run.output` and are not returned by any user-facing endpoint; the evaluation response already carries score rows. |
| Backward compatibility | Unchanged. |
| Authorization | Rules and parameters C/R for evaluations; Platform administration R for run metadata. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P10-003; 422 MSG-P10-002; 503. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-019; SPEC-RWB-E1-062-001..016 | New listeners, assembler, owner resolver, rule checks and scorer. | Positive, negative, boundary and error-path tests: both events, both codes, 30-day boundary, floor boundary, unmapped code, X9, timeout, repeat event, access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ScreeningShadowListener` | Listener | Consumes EV-01 and EV-16; calls the orchestrator with the run key. |
| `ScreeningInputAssembler` | Service | Builds masked inputs: case, ledger (180 days), documents and fields. |
| `ScreeningOwnerResolver` | Service | Adds the owner role from R-DEV-02..R-DEV-06 to each proposal. |
| `ScreeningRuleChecks` | Service | Schema and `SCHEMA_RULE` checks: code list, X1 preceding contact. |
| `ScreeningScorer` | Service | Precision and recall per code; counts review proposals. |
| `screening-v1.json`, prompt `SCREENING` PR1 | Rule table | Output schema and prompt loaded through the configuration endpoint. |

### Package and boundaries

`recovery.agent.screening`. The listener consumes the outbox through the P3/P5 event contracts; the
assembler calls P3 `CaseQueryService`, P7 `InteractionLedgerReader`, P5 `DocumentQueryService` and P3
`RuleEvaluator`. No table of another module is read.

### Data and migration

`V10_005__evaluation_review_count.sql` adds `review_count` (integer) to `agent_evaluation_run`. Reads:
`recovery_case` (`id`, `product_group`, `region_code`, `deviation_open`), `deviation` (`deviation_code`),
`interaction` (`id`, `occurred_at`, `channel`, `summary`), `document` (`id`, `document_type`),
`document_field` (`field_name`, `field_value`), `rule_row` (`rule_id`, `owner_role`), `agent_sample`.
Writes: `agent_run`, `agent_evaluation_run`, `agent_evaluation`. No deviation, task, timer or contact
stop is written.

### Input and checks

- Ledger window: `agent_policy.config.ledger_window_days` (180).
- X1 look-back: `agent_policy.config.lookback_days` (30) before the complaint's `occurred_at`.
- Proposal schema: `code` in X1..X7; `reasons` array; `sourceRefs` array of interaction/document IDs;
  `precedingContactId` required for X1; `confidence` 0..1.
- Check order: `SCHEMA` (shape and code list) then `SCHEMA_RULE` (X1 preceding contact); the first
  failure sets `GUARDRAIL_FAILED` and fallback true.
- A code already open on the case is not proposed again; the open-deviation read is by code.
- Owner role: `RuleEvaluator.ownerFor("Deviations", "OWNER_ASSIGNED", code)`; no row gives
  `RW-TEAMMGR` and `unmapped = true`.
- Below floor: `review = true`; excluded from precision/recall and counted in `review_count`.

### Transaction and events

One transaction per event: insert `agent_run`, insert the EV-28 outbox row. The evaluation run is
separate: create RUNNING, score each sample case, write score rows, set DONE. A repeated event finds the
existing run by event ID and run key and counts the hit; it makes no second model call.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| `SY-AGENT` | Case record R, Documents R | All |
| `SY-RULES` | Rules and parameters R | All |
| RW-COE | Rules and parameters CRUD | All |
| RW-RISK, RW-CONDUCT | Rules and parameters R | All |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Platform administration R | All |

### Observability, performance and rollback

- Metrics: runs by trigger and status, proposals per code, review count, unmapped count, precision and
  recall per code, latency, tokens, cost.
- Alerts: guardrail spike, timeout spike, no runs for a day, fallback rate above 10 percent.
- Performance: 200 shadow cases in the DEV run; each run bounded by the 60-second policy timeout.
- Feature flag `rwb.agent.screening-shadow`: off means both listeners ignore their events.
- Rollback: flag off; redeploy the previous tag; the `review_count` column is nullable.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-062-01 | AC1, BR1 | System | 200 synthetic cases with notes and documents | 200 shadow runs; no deviation; `deviation_open` false; no contact stop |
| TC-E1-062-02 | AC2, BR6 | System | SCREEN-S1 v1; X6 18/2/6 | One score row per code; 0.9000 and 0.7500 |
| TC-E1-062-03 | AC3 | System | Case RW-2026-000401, DEATH_CERTIFICATE | One run, key `SCREENING:<caseId>:<eventId>`, trigger `DocumentStored` |
| TC-E1-062-04 | AC4, BR3 | System | X4 on RW-2026-000402; one unmapped code | RW-FRAUD; unmapped gets RW-TEAMMGR and `unmapped` |
| TC-E1-062-05 | AC5, BR4 | System | Call 2026-11-25, complaint 2026-11-27 | X1 names the call; missing contact fails `SCHEMA_RULE` |
| TC-E1-062-06 | AC6, BR5 | System | X2 confidence 0.72 | `review`; counted in `review_count`, not in precision/recall |
| TC-E1-062-07 | AC7, BR7 | System | EV-16 for D-1001 twice | One run; repeat counted |
| TC-E1-062-08 | AC8, BR2 | System | Stub returns X9 | `GUARDRAIL_FAILED`, `SCHEMA`, fallback true |
| TC-E1-062-09 | AC9 | System | Stub silent 61 s | `TIMED_OUT`; no retry |
| TC-E1-062-10 | X7 | Security | RW-CASEOWN calls evaluations | 403 MSG-P4-002 |
| TC-E1-062-11 | BR4, AC5 | Unit | Look-back boundary at 29, 30 and 31 days | 29/30 accepted; 31 fails `SCHEMA_RULE` |
| TC-E1-062-12 | BR1 | System | Query every user-facing endpoint after a run | No proposal returned |

## Guardrails and out of scope

- No business value in code: codes, owner roles, floor, look-back and window are approved rows.
- No personal data in logs, tests or prompts; interaction summaries and document fields are masked.
- No read of another module's table; ledger, case, documents and rules come through their interfaces.
- The agent never calls the S8 deviation service in shadow mode.
- Out of scope: showing proposals and L1 on one segment (RWB-E2-029); raising, routing and clearing a
  deviation (RWB-E2-015); the full deviation flows (Epic 7).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Program 5.15 | FEAT-DVH-01, FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-40 | TC-E1-062-01..03, 06..12 |
| REQ-DVH-003 | Each code routes to its named owner; an unmapped code goes to the team manager | Program 5.15 | FEAT-DVH-04 | 11 Handle customer care and deviations | R-DEV-02..06 | TC-E1-062-04 |
| REQ-DVH-007 | A complaint is matched to the contact before it | Program 5.15 | FEAT-DVH-08 | 11 Handle customer care and deviations | None | TC-E1-062-05, 11 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4; SPEC-005 | Where are the 30-day look-back and 180-day ledger window stored? TSD `agent_policy` has no column. | Check window and input volume. | `agent_policy.config` jsonb (`lookback_days` 30, `ledger_window_days` 180), loaded and approved with the policy; TSD T3 update required (F-02). | RESOLVED | SPEC-005, SPEC-012 |
| CLAR-002 | X3; SPEC-005 | Does a `SCHEMA_RULE` failure on one proposal fail the whole run or only that proposal? | Whether other proposals are kept. | The whole run fails per RWB-E1-058 BR4: the first failed check sets `GUARDRAIL_FAILED` and fallback true; no partial output is used. | RESOLVED | SPEC-005, SPEC-009 |
| CLAR-003 | §11; SPEC-011 | What does "a code already open is not proposed again" mean? | Suppression. | If an open deviation of the same code exists on the case, that code is omitted from the proposals. | RESOLVED | SPEC-011 |
| CLAR-004 | AC5; SPEC-005 | Which timestamp anchors the 30-day window? | Boundary. | The `occurred_at` of the interaction the X1 proposal cites as the complaint; if the source is a document, its received date. | RESOLVED | SPEC-005 |
| CLAR-005 | AC4; SPEC-004 | Where is the owner role stored? | Output shape. | In each proposal inside `agent_run.output`; no new column. | RESOLVED | SPEC-004 |
| CLAR-006 | BR5, BR6; SPEC-010 | Are review proposals scored? | Precision/recall denominator. | No; they are counted in `review_count` and excluded from TP/FP/FN. | RESOLVED | SPEC-010 |
| CLAR-007 | X5; SPEC-004 | Which codes are unmapped when five rule rows cover seven codes? | Fallback role. | Runtime lookup; any code with no row gets `RW-TEAMMGR` and `unmapped`. The two codes are data-dependent, not fixed in code. | RESOLVED | SPEC-004 |
| CLAR-008 | Feature flag; SPEC-014 | What happens when the flag is off? | Event handling. | Both listeners ignore their events; no run row, no model call. | RESOLVED | SPEC-014 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the TSD or the rule table.
No item changes a business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this shadow agent story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New shadow screening agent on the existing agent platform; no screen or contract change; evaluation endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: event-driven shadow runs and scoring with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 9 acceptance criteria, 7 exception paths and 5 run/evaluation states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
