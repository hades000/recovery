# RWB-P10-E2030-APP Legal document agent in shadow on Epic 1 data [E3c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2030-APP |
| Work type | APP (App development) |
| Size | Not specified in the source documents (DOR-RWB-P10-E2030-APP-16) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Contract version | v1 (base `/api/recovery/agent/v1`, section 12.1) |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP13, DP19 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1058-APP is done (build dependency not yet done) |
| Depends on (build) | RWB-P10-E2030-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-N001-CON, RWB-P10-E1058-APP, RWB-P10-E1061-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P5-E2025-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-007, FR-P10-012, FR-P10-013, FR-P10-014) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E2-030 for rwb-agent. The behaviour of the legacy story does not change: policy "LEGAL_DOC" version "P1" in mode SHADOW, the 9-item checklist of case type "MORTGAGE_CIVIL", sample "LEGAL-S1" version 1 on 50 cases, agreement 0.9200 on 46 of 50 for "DEMAND_NOTICE_PROOF", the 49 scored cases, the review date 2027-03-15, and the refusals MSG-P10-001, MSG-P7-002 and MSG-P4-002. What changes is where each fact lives and how it is reached: the run, the sample, the evaluation run, the score rows and the policy version are rows of schema `rwb_agent` (DP-01); the documents, their checked fields and the checklist are read through the rwb-document contract of RWB-P5-E2025-CON; the case facts through rwb-case and the open legal action through rwb-litigation; the minimum sample and the promotion checks are parameter values of rwb-case (DP-06) and the lists come from its reference-data contract (DP-07); the operations are served on `/api/recovery/agent/v1` (DP-13) behind the gateway-bff route (DP-19); the run facts leave as `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` through the outbox (DP-09). Shadow only: no legal action, document, pack, task or case field is changed and no user-facing endpoint returns the pack. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 24 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the legal document agent built inside rwb-agent and run in mode SHADOW on the Epic 1 litigation cases - one run per sampled case that reads the case through the rwb-case contract, the open legal action through the rwb-litigation contract, the documents with their checked fields and the case-type checklist through the rwb-document contract, assembles the litigation pack and the completeness list with PRESENT, MISSING or DEFECT per item and a reason for every defect, stores the pack on the run in `rwb_agent` and scores agreement per checklist item against the packs the legal officers built, with the promote-or-keep decision loaded as policy version "P2" and approved on `/api/recovery/agent/v1`**, so that **the agent goes to Epic 5 with a known accuracy per pack item, and nothing in the case is touched while the agent is in shadow**.

### 2. Business rationale

A litigation pack that reaches the law firm with a missing or defective document is returned, and the filing waits. From Epic 5 the legal document agent assembles the pack and checks it against the defect list before the officer verifies it (R-LIT-16, R-LIT-17, CTL-19). This story runs the agent in shadow on 50 cases whose packs the officers have already built, scores agreement per checklist item, and records the decision to promote or keep it in shadow as a policy version. It serves REQ-S4-002 - a pack assembled and checked against the document checklist, with missing documents named - and the checklist itself is the case-type document checklist of REQ-DCM-011.

In the legacy delivery the case, the legal action, the documents, the checklist, the sample, the harness and the agent tables sat in one module and one schema: the facts came through the in-process `LegalActionQueryService.listByCase(caseId)` of S4 and `DocumentQueryService.listByCase`, `getFields` and `getChecklist(caseType)` of P5, and the run, the scores and the policy version were written to `recovery.agent_run`, `recovery.agent_evaluation` and `recovery.agent_policy`. The behaviour does not change, so the same nine criteria, policy values and sample are carried onto the service. What changes is the seam:

- The run, the sample, the evaluation run, the score rows, the prompt and the approved policy version are P10 rwb-agent in schema `rwb_agent`, and this story writes only its own (DP-01; BR8).
- The documents, their checked fields and the checklist of a case type are P5 rwb-document and are read through RWB-P5-E2025-CON, one hop with a 2 s budget; no `document`, `document_field` or checklist table of another schema is opened (DP-01; BR8).
- The case facts are P3 rwb-case and the open legal action is S4 rwb-litigation; both are read through their contracts, never through their tables (DP-01).
- The minimum sample of 50 cases and the promotion check list are values of the approved policy and of the rwb-case parameters, read at load time and written in no code (DP-06; BR6).
- LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS, LOV-AGENT-RUN and LOV-SUBJECT-TYPE come from the rwb-case reference-data contract (DP-07; BR9).
- The operations are served on `/api/recovery/agent/v1` and reached through the gateway-bff route; the legacy monolith base is retired (DP-13, DP-19).
- The run facts leave through the outbox and inbox library as CloudEvents on `rwb.agent.events.v1` with its retry and `.dlt` topics, keyed by the case (DP-09; BR10).

The story is shadow only. In mode SHADOW the pack and the completeness list are stored on the run and nowhere else: no pack is filed, no document is requested or changed, no legal action is opened, moved or closed, no task is raised and no case field is written (BR1; section 9). The pack is not published on the topic either; the event carries run facts only (BR10; section 12.3).

The cross-service behaviour of this key - that the pack names only documents the hub serves for the same case, that the run writes nothing in rwb-document, rwb-litigation or rwb-case, and that the scores read back are the ones the harness wrote - is proved against the real services by the wave-2 integration harness, not here; this story carries no integration dependency (I = None) and claims none. It owns the nine legacy criteria AC1 to AC9 and adds none.

### 3. Preconditions

- RWB-P10-E2030-CON is baselined: the run start and run read, the `legal-pack-v1` output members, the consumed boundary shapes, the event contract and the fakes of section 12 exist as a document with its own test cases.
- RWB-P10-E1058-APP is done: the orchestrator, the model gateway client, the prompt and policy store, the sample load, the configuration operations and the admin run read exist in rwb-agent, and a run can be made in mode SHADOW.
- RWB-P10-E1061-CON is baselined: the evaluation start, list and report on `/api/recovery/agent/v1/admin/agent-evaluations`, which this story calls to run and score the sample and does not re-declare.
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters and reference-data client libraries. RWB-PLT-TE006-CON is published: the outbox and inbox library, the relay, the retry topic and the `.dlt` rule. RWB-PLT-N001-CON is published: the gateway-bff route contract and its stub.
- The `rwb_agent` schema baseline exists with the standard record columns and the Flyway history table; the agent tables of TSD P10 Agent runtime v2 T3.1 are created by the migrations of RWB-P10-E1058-APP and RWB-P10-E1061-APP, so this story adds no table and no migration.
- The document checklist of case type "MORTGAGE_CIVIL" is reference data of rwb-document, maintained by RW-REFADM and read through the P5 contract (RWB-P5-E2025-CON; REQ-DCM-011).
- Policy "LEGAL_DOC" version "P1" is approved: mode SHADOW, timeout 60 seconds, allowed tools read_case, read_legal_actions, read_documents, read_document_fields, read_checklist, output schema "legal-pack-v1". Sample "LEGAL-S1" version 1 holds one row per case and checklist item for the 50 cases with expected PRESENT, MISSING or DEFECT.
- Every consumed call is one hop with the 2 s client budget (DP-11, ADR-020); the model call happens inside the run under the 60-second policy budget.

### 4. Flow

1. RW-COE loads sample "LEGAL-S1" version 1 and starts the evaluation of "LEGAL_DOC" through POST `/api/recovery/agent/v1/admin/agent-evaluations`; the harness returns a run in status RUNNING.
2. For each sample case the harness starts one shadow run through AgentRunWorkflow on queue `rwb-agent`: the case facts are read from rwb-case, the open legal action from rwb-litigation, the documents with their masked fields and the 9-item checklist of the case type from rwb-document.
3. The model gateway is called once per case under the 60-second policy budget, with the input assembled from those reads only.
4. The guardrail checks the answer: every checklist item has a status, every document ID belongs to the case, every DEFECT has a reason (BR3, BR4).
5. The pack - document IDs per item - and the completeness list - PRESENT, MISSING or DEFECT per item - are stored in `agent_run.output`; no document, pack, legal action, task or case field changes (BR1).
6. The scorer compares the run with the officers' rows of `agent_sample` and writes one `agent_evaluation` row per checklist item with the agreement rate at four decimals and the sample size (BR5).
7. RW-COE loads policy version "P2" - mode L1 with the conditions to promote, or mode SHADOW with the review date 2027-03-15 - and its evaluation run ID; a proposal is refused when a check fails (MSG-P10-001).
8. RW-RISK approves the version; the approver and the approval date are recorded on the policy row, and a loader who approves their own version is refused (MSG-P7-002).
9. The completion facts of each run are written to the outbox in the same transaction as the run row and relayed as `rwb.agent.AgentRunCompleted.v1` (EV-28).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent names a document that belongs to another case | Check SCHEMA_RULE fails; run status GUARDRAIL_FAILED; scored as wrong for every item | None to a user | AC4 |
| X2 | A checklist item has no status in the answer | Check SCHEMA fails; run status GUARDRAIL_FAILED | None to a user | AC5 |
| X3 | A consumed read is unavailable during a run | Run status TOOL_UNAVAILABLE, fallback true; the case is listed as not run and scored as not run (R-UNI-33) | None to a user | AC6 |
| X4 | Fewer than 50 scored cases and a proposal in mode L1 | The load is refused with 422 and check "sample size at least 50" | MSG-P10-001 | AC7 |
| X5 | Keep shadow without a review date | The load is refused with 422 and check "review date present" | MSG-P10-001 | AC8 |
| X6 | The loader approves their own decision | Refused with 409 | MSG-P7-002 | AC9 |
| X7 | A role without the right | Refused with 403; nothing changes | MSG-P4-002 | AC10 |
| X8 | The model does not answer inside 60 seconds, or the guardrail rejects the answer | Run status TIMED_OUT or GUARDRAIL_FAILED with fallback true and the reason recorded; no second run for the same case and evaluation | None to a user | AC1, AC4, AC5, AC15 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the agent platform, the harness and the run path already built; reads rwb-case, rwb-litigation and rwb-document through their contracts and needs no S4 or P5 workflow |
| Negotiable | Checklist items come from reference data; the minimum sample, the timeout and the promotion conditions are policy and parameter values |
| Valuable | Gives the item accuracy that decides whether the agent assembles packs in Epic 5 |
| Estimable | One prompt, one output schema, one scorer, one proposal validator, two reads added to the run path |
| Small | One developer and one litigation officer for review |
| Testable | Each criterion runs on synthetic fixture cases with known officer packs and contract mocks |

### 7. Acceptance criteria

```gherkin
Feature: Legal document agent in shadow on Epic 1 data [E3c]

  Background:
    Given policy "LEGAL_DOC" version "P1" with mode "SHADOW" and prompt "PR1"
    Given the checklist for case type "MORTGAGE_CIVIL" has 9 items including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF"

  Scenario: AC1 Shadow pack (legacy RWB-E2-030 AC1)
    Given litigation case "RW-2026-000901" with 14 documents and an open legal action
    Given the rwb-document contract mock returns 14 documents for case "RW-2026-000901", their masked field values and the 9-item checklist of case type "MORTGAGE_CIVIL"
    Given the rwb-litigation contract mock returns one open legal action for case "RW-2026-000901"
    Given the rwb-case contract mock returns the case facts of case "RW-2026-000901"
    When the agent runs
    Then a pack listing document IDs for each of the 9 items and a completeness list with PRESENT, MISSING or DEFECT per item are stored on the agent run
    Then no document, legal action, task or case field changes
    Then no user-facing endpoint returns the pack

  Scenario: AC2 Scored (legacy RWB-E2-030 AC2)
    Given 50 shadow packs for sample "LEGAL-S1" version 1
    When the evaluation runs
    Then the system stores agreement with the officers' packs per item with sample size 50
    Then for "DEMAND_NOTICE_PROOF" with 46 agreeing cases the agreement rate is 0.9200

  Scenario: AC3 Promotion proposal (legacy RWB-E2-030 AC3)
    Given the score
    When RW-COE loads policy "LEGAL_DOC" version "P2" with mode "SHADOW", review date 2027-03-15 and the evaluation run ID, and RW-RISK approves it
    Then the system records the decision to keep shadow on version "P2" with the approver and the approval date
    Then the system accepts a proposal with mode "L1" only when every stated condition is met by the evaluation

  Scenario: AC4 A document from another case (legacy RWB-E2-030 AC4)
    Given the model stub names document "D-7001" of case "RW-2026-000902" in the pack of case "RW-2026-000901"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED" and check "SCHEMA_RULE"

  Scenario: AC5 An item without a status (legacy RWB-E2-030 AC5)
    Given the answer has no status for item "MORTGAGE_DEED"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED" and check "SCHEMA"

  Scenario: AC6 The document interface is down (legacy RWB-E2-030 AC6)
    Given the P5 document interface is unavailable for case "RW-2026-000903"
    Given the rwb-document contract mock returns 503 for case "RW-2026-000903"
    When the agent runs
    Then the run holds status "TOOL_UNAVAILABLE" and fallback true
    Then the evaluation lists the case as not run and scores 49 cases

  Scenario: AC7 Too few cases to promote (legacy RWB-E2-030 AC7)
    Given the evaluation scored 49 cases
    When RW-COE loads a proposal with mode "L1"
    Then the system refuses the load with 422 and MSG-P10-001 naming check "sample size at least 50"

  Scenario: AC8 Keep shadow without a review date (legacy RWB-E2-030 AC8)
    When RW-COE loads version "P2" with mode "SHADOW" and no review date
    Then the system refuses the load with 422 and MSG-P10-001 naming check "review date present"

  Scenario: AC9 The loader cannot approve (legacy RWB-E2-030 AC9)
    Given user "coe.user01" loaded version "P2"
    When user "coe.user01" approves it
    Then the system refuses the approval with 409 and MSG-P7-002

  Scenario: AC10 A role without the right (covers X7) (new, D-RCV-60)
    Given a user with role "RW-LITOFF"
    When the user calls POST `/admin/agent-evaluations`
    Then the system refuses the call with 403 and MSG-P4-002
    Then no evaluation run, policy version or score row changes

  Scenario: AC11 States of the run read (empty, in progress, failed) (new, D-RCV-60)
    Given no agent run exists for case "RW-2026-000904" and the evaluation
    When the run of case "RW-2026-000904" is read
    Then the read returns no run and no pack
    Given the agent run of case "RW-2026-000901" has status "RUNNING"
    When the run of case "RW-2026-000901" is read
    Then the read shows the run as in progress and returns no pack
    Given the agent run of case "RW-2026-000901" has status "TIMED_OUT"
    When the run of case "RW-2026-000901" is read
    Then the read shows the run as failed with fallback true and the reason recorded

  Scenario: AC12 Field values are masked before the model call (BR11) (new, D-RCV-60)
    Given the rwb-document contract mock returns field values of case "RW-2026-000901" that are personal data
    When the agent runs
    Then every field value reaches the model call masked

  Scenario: AC13 Minimum sample is data with a version (BR9) (new, D-RCV-60)
    Given the rwb-case parameters contract returns the minimum sample for policy "LEGAL_DOC" version "P2"
    When RW-COE loads policy "LEGAL_DOC" version "P2" with mode "L1"
    Then the load checks the sample size against the parameter value read at load time

  Scenario: AC14 Run facts leave as events (BR10) (new, D-RCV-60)
    Given the agent run of case "RW-2026-000901" completes
    When the completion is written
    Then one CloudEvents 1.0 message "rwb.agent.AgentRunCompleted.v1" is written to "rwb.agent.events.v1" keyed by the case through the outbox
    Then no pack and no completeness list is published

  Scenario: AC15 The model does not answer in time (X8) (new, D-RCV-60)
    Given the model does not answer inside 60 seconds for case "RW-2026-000901"
    When the agent runs
    Then the run holds status "TIMED_OUT" and fallback true with the reason recorded
    Then no second run is made for case "RW-2026-000901" and the evaluation

  Scenario: AC16 No session or an unknown version or evaluation (new, D-RCV-60)
    Given a caller with no session
    When the caller calls GET `/admin/agent-evaluations`
    Then the system refuses the call with 401
    Given a user with a session and an evaluation ID that does not exist
    When the user calls GET `/admin/agent-evaluations/{evaluationId}/report`
    Then the operation answers 404
    Given a user with role "RW-RISK" and a version ID that does not exist
    When the user calls POST `/admin/agent-configs/{versionId}/approve`
    Then the operation answers 404 and no policy row changes

  Scenario: AC17 A repeated write with the same idempotency key (new, D-RCV-60)
    Given POST `/admin/agent-evaluations` was accepted with an Idempotency-Key
    When the same request is sent again with the same Idempotency-Key
    Then the stored answer of the first request is returned
    Then no second evaluation run is created and no other state changes
    When a request with a different body reuses that Idempotency-Key
    Then the request is rejected and nothing changes

  Scenario: AC18 An approved version cannot be approved again (new, D-RCV-60)
    Given policy "LEGAL_DOC" version "P2" is in status APPROVED
    When RW-RISK approves version "P2" again with a new Idempotency-Key
    Then the system refuses the approval with 409 and MSG-GEN-004
    Then the status, the approver and the approval date of version "P2" do not change
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | In SHADOW mode the pack and the completeness list are stored only; no pack, document, legal action, task or case field changes | `agent_policy.autonomy_mode` (new) |
| BR2 | Checklist items come from the document checklist of the case type, read through the rwb-document contract | REQ-DCM-011 |
| BR3 | Every item has a status PRESENT, MISSING or DEFECT, and every DEFECT has a reason | R-LIT-16, R-LIT-17; CTL-19 |
| BR4 | A pack may name only documents of the same case | CTL-19; CTL-11 |
| BR5 | Agreement per item = cases where the agent status equals the officer status / scored cases, four decimals | `agent_evaluation.agreement_rate` (new) |
| BR6 | A promotion to L1 needs at least 50 scored cases; keeping shadow needs a review date; both are policy and parameter values | `agent_policy.review_date` (new); DP-06 |
| BR7 | The loader and the approver are different people | Separation of duty |
| BR8 | rwb-agent writes only `rwb_agent` and reads no table of another service; the case, the legal action, the documents, the fields and the checklist come through their owners' contracts | DP-01; DP-11 |
| BR9 | No business value in code: the 9 items, the minimum sample 50, the review date and the timeout are data with a version | Template and Rules §R7.2 s17; DP-06; DP-07 |
| BR10 | Every run fact leaves as a CloudEvents 1.0 message on `rwb.agent.events.v1`, keyed by the case; the pack and the completeness list are never published | DP-09; DP-14; EV-28 |
| BR11 | Field values read from rwb-document are personal data: each is masked before the model call | Not specified in the source documents (DOR-RWB-P10-E2030-APP-11) |

### 9. State transitions

No case status changes: the story does not move a case into PACK_ASSEMBLY and writes no case field. It moves the run, the evaluation run and the policy version:

| Object | From | Event in the story | To |
|---|---|---|---|
| agent_run | None | The harness starts the run | ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR or TOOL_UNAVAILABLE (LOV-AGENT-RUN) |
| agent_evaluation_run | None | POST `/admin/agent-evaluations` accepted | RUNNING |
| agent_evaluation_run | RUNNING | All sampled cases scored | DONE; FAILED when the harness fails |
| agent_policy | None | A checked policy file loaded | LOADED |
| agent_policy | LOADED | RW-RISK approves a version they did not load | APPROVED; RETIRED when a later version takes effect |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT | Reads the case, the legal actions, the documents, the fields and the checklist through the owners' contracts (Case record R, Litigation R, Documents R, Reference data R) |
| RW-COE | Loads the sample, runs the evaluation, loads the decision version (Rules and parameters CRUD) |
| RW-RISK | Approves the decision version (Rules and parameters A) |
| RW-LITOFF | Supplies the officers' packs for the sample; reads the scores |
| RW-HEADLIT | Reads the scores |
| RW-REFADM | Maintains the document checklist of the case types |

The identity that calls the consumed contracts is the rwb-agent service identity; its name is fixed with the deployment story and is not declared here (DP-02 is not a pattern of this key).

Each REST operation of this story checks the caller's right with the rwb-access authorise check (DP-08) before it runs; a refused call is answered as AC10 and TC-E2-030-10 require.

### 11. Data

| Entity (schema) | Fields (BR Field IDs) | Read or write |
|---|---|---|
| recovery_case | DF-CAS-001 id, DF-CAS-003 product_group, DF-CAS-017 prescription_date | Read through the rwb-case read (P3) |
| legal_action | DF-LEG-001 id, DF-LEG-004 action_type, DF-LEG-014 status | Read through the rwb-litigation read (S4) |
| document | DF-DOC-001 id, DF-DOC-002 case_id, DF-DOC-004 document_type, DF-DOC-010 write_once | Read through the rwb-document read (P5) |
| document_field | DF-DOC-014 field_name, DF-DOC-015 field_value | Read (masked) through the rwb-document read (P5) |
| agent_run (`rwb_agent`) | DF-AGT-036 id, DF-AGT-037 agent_code, DF-AGT-038 agent_version, DF-AGT-041 case_id, DF-AGT-042 subject_id, DF-AGT-043 autonomy_mode, DF-AGT-044 trigger_event, DF-AGT-046 status, DF-AGT-047 fallback, DF-AGT-048 guardrail_result, DF-AGT-049 output (the pack and the completeness list), DF-AGT-051 latency_ms, DF-AGT-052 tokens_in, DF-AGT-053 tokens_out, DF-AGT-054 cost_thb, DF-AGT-056 run_at, DF-AGT-057 evaluation_run_id | Write |
| agent_sample (`rwb_agent`) | DF-AGT-063 sample_code, DF-AGT-064 sample_version, DF-AGT-066 subject_id, DF-AGT-067 label_key, DF-AGT-068 expected_value | Read |
| agent_evaluation (`rwb_agent`) | DF-AGT-087 evaluation_run_id, DF-AGT-089 label_key, DF-AGT-090 sample_size, DF-AGT-094 agreement_rate | Write |
| agent_evaluation_run (`rwb_agent`) | status RUNNING to DONE, requested_by, started_at, finished_at, failure_counts | Write (baselined by RWB-P10-E1061-APP) |
| agent_policy (`rwb_agent`) | DF-AGT-003 policy_version, DF-AGT-008 autonomy_mode, DF-AGT-016 review_date, DF-AGT-017 evaluation_run_id, DF-AGT-018 promotion_conditions, DF-AGT-021 status, DF-AGT-025 approved_by | Write |

Field IDs are those of the Logical Data Model and Data Dictionary; `rwb_agent` holds the eight agent tables of TSD P10 Agent runtime v2 T3.1. No table of another service is read and no row is copied into `rwb_agent` (DP-01). The member names and types beyond these field names are Not specified in the source documents (GAP-0627; ASM-0944).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10). The operations this story uses are those baselined by RWB-P10-E1058-CON and RWB-P10-E1061-CON; this story supplies their behaviour for agent "LEGAL_DOC" and adds no member.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/api/recovery/agent/v1/admin/agent-samples` | Load sample "LEGAL-S1" version 1 (multipart file, agent, sampleCode) | Rules and parameters C, scope applied; errors 401, 403, 422, 503 | Idempotency-Key header |
| POST | `/api/recovery/agent/v1/admin/agent-evaluations` | Start the evaluation of "LEGAL_DOC" on "LEGAL-S1" version 1; 202 AgentEvaluationRun in status RUNNING; 409 MSG-P10-003, 422 MSG-P10-002 | Rules and parameters C, scope applied; errors 401, 403, 409, 422, 503 | Idempotency-Key header |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations` | List the runs with their scores and proposals, as JSON or CSV | Rules and parameters R, scope applied; errors 401, 403, 503 | Not applicable |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report` | Read the report: sample size, agreement per item, failures, cost and latency | Rules and parameters R, scope applied; errors 401, 403, 404, 409 MSG-P10-008, 503 | Not applicable |
| POST | `/api/recovery/agent/v1/admin/agent-configs` | Load policy version "P2" with its mode, review date, evaluation run ID and conditions; 201 in status LOADED | Rules and parameters C, scope applied; errors 401, 403, 409, 422 MSG-P10-001, 503 | Idempotency-Key header |
| POST | `/api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` | Approve the loaded version; 200 with status APPROVED, approvedBy and validFrom; 409 MSG-P7-002 on a self-approval; 409 MSG-GEN-004 on a version already APPROVED | Rules and parameters A, scope applied; errors 401, 403, 404, 409, 503 | Idempotency-Key header |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | Read the prompt and policy versions with their status and dates | Rules and parameters R, scope applied; errors 401, 403, 503 | Not applicable |

Errors: 401 no session, 403 no right (MSG-P4-002), 404 an unknown version or evaluation, 409 a self-approval (MSG-P7-002), an approval of a version already APPROVED (MSG-GEN-004) or a second evaluation of the same sample while one is RUNNING (MSG-P10-003), 422 a failed check (MSG-P10-001) or a sample with no labelled row (MSG-P10-002), 503 the store or a consumed contract unavailable. No operation of this story returns the pack or the completeness list (BR1).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document (RWB-P5-E2025-CON) | AC1, AC4, AC6: the 14 documents of the case with their type and write-once flag | One hop, 2 s |
| GET | `/api/recovery/document/v1/documents/{documentId}/fields` | P5 rwb-document (RWB-P5-E2025-CON) | AC1, AC5: the checked field names and their masked values | One hop, 2 s |
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` | P5 rwb-document (RWB-P5-E2025-CON) | AC1, AC5, AC7: the 9 items of case type "MORTGAGE_CIVIL" including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF" | One hop, 2 s |
| GET | the by-case legal-action read of rwb-litigation | S4 rwb-litigation | AC1: the open legal action of the case and its type; the path is Not specified in the source documents (GAP-0627; ASM-0944) | One hop, 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case (RWB-P3-E2015-CON) | AC1: the case facts of DF-CAS-001, DF-CAS-003 and DF-CAS-017 | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case (RWB-P3-E1042-CON) | AC7, AC8: the minimum scored sample 50 and the promotion check list in force, with their version; the codes are Not specified in the source documents (GAP-0627; ASM-0948) | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | AC1, AC3, AC5: LOV-AGENT, LOV-AUTONOMY, LOV-CONFIG-STATUS, LOV-EVAL-STATUS, LOV-AGENT-RUN and LOV-SUBJECT-TYPE | One hop, 2 s |

Every call is one hop with the 2 s client budget (DP-11, ADR-020), and a failed read maps to run status TOOL_UNAVAILABLE with the reason naming the read (AC6; R-UNI-33). The three P5 paths and the S4 path are named by no source and are fixed against the fake (ASM-0944). The model call is not a consumed operation of this table: it happens inside AgentRunWorkflow under the 60-second policy budget (section 12.5).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | runid, agent, caseid, fallback, outcome |

The event is inserted in the outbox in the same transaction as the run row and relayed by the outbox library of RWB-PLT-TE006-CON (DP-09); it is validated against its registry subject before the relay and a refusal is routed to `.dlt` with an alert. It carries run facts only: the pack, the completeness list, the defect reasons, the document IDs and every personal field stay in `agent_run.output` (BR10; ASM-0953). This story publishes no second event and no pack event.

#### 12.4 Events consumed

None. The runs of the evaluation are started by the harness, not by a topic: the sample is the trigger and the case list comes from `agent_sample`. The two event-triggered run paths of rwb-agent (`CaseCreated`, `DocumentStored`) belong to RWB-P10-E1059-APP, RWB-P10-E1062-APP and RWB-P10-E2029-APP and are not used here.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow, one execution per case and evaluation run, started by the evaluation harness and not by an operation of its own (ASM-0955). Workflow ID: Not specified in the source documents (CG-ALL-2751). Start rule (start or signalWithStart, duplicate-start policy): Not specified in the source documents (CG-ALL-2751) | `rwb-agent` | Input: agent "LEGAL_DOC", case ID, evaluation run ID, policy version "P1", idempotency key. Output: the run in its mode with the pack, the completeness list and the status; the 60-second policy budget then the rule result (R-UNI-32) |
| AssembleLegalPackInputs | Activity | `rwb-agent` | Input: the case, the legal action, the documents with their masked fields and the checklist, read through the P3, S4 and P5 contracts. Output: the masked model input and the item list |
| ScoreLegalPack | Activity | `rwb-agent` | Input: the run and the officers' rows of `agent_sample`. Output: one `agent_evaluation` row per item with the agreement rate at four decimals and the sample size |

The workflow identity, the queue and the 60-second budget are the platform and policy values of Arch v5 slide 16; the activity names are this story's and are accepted by RWB-P10-E2030-CON.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story: the evaluation is started by RW-COE and a run is started by the harness. The legacy Quartz scheduler is retired and DP-10 is not a pattern of this key.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_run | P10 (`rwb_agent`) | One run per case and evaluation with its pack in `output`, its guardrail result, its cost and its status; no column added |
| agent_policy | P10 (`rwb_agent`) | Policy "LEGAL_DOC" versions "P1" and "P2" with mode, review date, evaluation run ID and conditions; written through the operation of RWB-P10-E1058-APP |
| agent_prompt | P10 (`rwb_agent`) | Prompt version "PR1" and the schema reference of "legal-pack-v1"; read only |
| agent_sample | P10 (`rwb_agent`) | Sample "LEGAL-S1" version 1: one row per case and checklist item with its expected status; read only |
| agent_evaluation_run | P10 (`rwb_agent`) | The evaluation of "LEGAL_DOC" on "LEGAL-S1" version 1; no column added |
| agent_evaluation | P10 (`rwb_agent`) | One score row per checklist item with the sample size and the agreement rate; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox, inbox and idempotency envelope of the completion event (DP-09) |

No new table, no migration: the legacy story states "no new table", and every column this story uses exists from RWB-P10-E1058-APP and RWB-P10-E1061-APP, so the Flyway sequence of `rwb_agent` is not extended (DP-15 is not a pattern of this key). `recovery_case`, `legal_action`, `document`, `document_field`, `document_checklist_item`, `parameter_catalog`, `parameter_value`, `reference_row` and `reference_version` belong to P3, S4 and P5 and are read only through their contracts (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document WireMock | The three reads of RWB-P5-E2025-CON | 14 documents for "RW-2026-000901" with their types and the write-once flag, the masked fields, the 9-item checklist of "MORTGAGE_CIVIL"; a 503 for "RW-2026-000903"; a document "D-7001" that belongs to "RW-2026-000902"; an answer beyond 2 s |
| rwb-litigation WireMock | The by-case legal-action read | One open legal action for "RW-2026-000901"; a case with no legal action; an answer beyond 2 s |
| rwb-case WireMock | The case read, the parameters and the lists | The case facts of "RW-2026-000901" to "RW-2026-000903"; the minimum sample 50 and the promotion check list; the six lists; an unknown case and an answer beyond 2 s |
| Model gateway fake (INT-23) | The model call of the run | A valid legal-pack answer for 50 cases; an answer naming document "D-7001" of another case; an answer with no status for "MORTGAGE_DEED"; silence for 61 seconds |
| gateway-bff route stub | The route of RWB-PLT-N001-CON | A pass-through in front of the seven operations, one hop, JSON and CSV media types preserved, the refusal passed through unchanged |

Every fixture is synthetic and holds no personal data; no test calls the real model endpoint. The outbox stub, the access guard stub and the evaluation fixture of RWB-P10-E1061-CON are used but not declared here.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 7 provided by the baseline and used, 7 consumed | The sample load, the three evaluation operations, the two configuration writes and the configuration read; the three document reads, the legal-action read, the case read, the parameters and the lists, one hop and 2 s each |
| Kafka | 1 published, 0 consumed | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` with its retry and `.dlt` topics, keyed by the case ID |
| Temporal | 1 workflow, 2 activities | AgentRunWorkflow with AssembleLegalPackInputs and ScoreLegalPack on the queue `rwb-agent` |
| File | 1 component | The sample file of "LEGAL-S1" version 1 is read once by the sample operation and stored as `agent_sample` rows; no file is written by a run |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.legal` inside rwb-agent (DP-13 base, DP-01 schema).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalPackInputAssembler | Service | Builds the masked input from the case, the legal action, the documents with their fields and the checklist, all through the consumed contracts |
| LegalPackRuleChecks | Service | SCHEMA and SCHEMA_RULE checks: same-case documents, a status per item, a reason per defect; maps a failed read to TOOL_UNAVAILABLE |
| LegalPackScorer | Service | Agreement per checklist item against `agent_sample`, four decimals, with the sample size and the not-run cases listed |
| PromotionProposalValidator | Service | The minimum sample of 50 for L1, the review date for SHADOW, the approver other than the loader |
| legal-pack-v1 output schema and prompt "PR1" | Data | Loaded through POST `/admin/agent-configs`; no business value in code (BR9) |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` | Own schema `rwb_agent`; other services through their contracts | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-28, outbox | Outbox and inbox library; the owner's topic; CloudEvents | H RWB-PLT-TE006-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/agent/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The documents and the checklist are consumed at the boundary of the key with C RWB-P5-E2025-CON, and the legal action and the case read carry no C row of their own because their contracts are published before this lane starts (DP-11; ASM-0944).

**Build steps**

1. Confirm the `legal-pack-v1` schema and prompt "PR1" with the fields of section 11 and load them in DEV.
2. Build LegalPackInputAssembler over the P3, S4 and P5 contract clients with the 2 s budget and the TOOL_UNAVAILABLE mapping (AC1, AC6).
3. Build LegalPackRuleChecks: same-case documents, a status per item, a reason per defect (AC4, AC5).
4. Build LegalPackScorer on a 10-case fixture with known agreement, then on the 50-case sample (AC2).
5. Extend PromotionProposalValidator with the sample minimum, the review date and the separation of duty (AC3, AC7, AC8, AC9).
6. Write the completion event to the outbox in the same transaction as the run row and assert that no pack member is on it.
7. Wire the seven operations through the gateway-bff route and prove the refusals 403, 409 and 422 end to end against the fakes.

**Configuration and reference data.** Policy "LEGAL_DOC" versions "P1" and "P2" loaded by RW-COE and approved by RW-RISK; the checklist of "MORTGAGE_CIVIL" maintained by RW-REFADM; sample "LEGAL-S1" built from the officers' packs. Feature flag `rwb.agent.legal-shadow`: off, an evaluation of "LEGAL_DOC" is refused with 422.

**Done when.** The ten test cases of section 16 pass, the 50-case evaluation is approved as promote or keep, the event carries no pack member, and the fake and contract tests of RWB-P10-E2030-CON pass against the built service.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | The decision version fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | The evaluation is started on an empty sample | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | The same evaluation is already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P10-008 | Evaluation report requested before the evaluation is done (RWB-E1-061) | The evaluation of {agent} on sample {sample} is still running. Open the report when it has finished. |
| MSG-P7-002 | The loader approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | An approval of a version that is already APPROVED | Someone else changed this record. Reload it to see their change. |

MSG-P10-001, MSG-P10-002, MSG-P7-002 and MSG-P4-002 are the legacy messages of RWB-E2-030, copied character for character; MSG-P10-003 is the message of RWB-P10-E1061-CON, quoted because the operation the story uses owns it. MSG-P10-008 and MSG-GEN-004 are quoted from the Error and Message Standard v4. The story adds no message.

### 15. Screens and states

No user screen shows a pack in this story: SCR-46 Agent monitor shows "LEGAL_DOC" in state Shadow with its runs, its fallbacks and the evaluation score, and the scores are read through GET `/admin/agent-evaluations` and its report. The pack and the completeness list stay on the run and are returned by no operation (BR1). The screens are composed through the gateway-bff route of RWB-PLT-N001-CON; the route name and path are Not specified in the source documents (GAP-0627; ASM-0950). The states of SCR-46 empty, loading, error and no access are Not specified in the source documents (CG-ALL-2757).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-030-10 | Access | Contract | RW-LITOFF calls POST `/admin/agent-evaluations`; refused with MSG-P4-002 |
| TC-E2-030-11 | AC1, BR8; boundary of the §12.7 tables | Component | One case and one evaluation: one `agent_run` row; no write outside the §12.7 tables |
| TC-E2-030-12 | AC11 | Component | No run for case "RW-2026-000904"; run "RUNNING"; run "TIMED_OUT" for case "RW-2026-000901" |
| TC-E2-030-13 | AC12, BR11 | Component | Field values of case "RW-2026-000901" masked before the model call |
| TC-E2-030-14 | AC13, BR9 | Component | Minimum sample from the rwb-case parameters contract, read at load time |
| TC-E2-030-15 | AC14, BR10 | Component | Completed run of case "RW-2026-000901" leaves as one event through the outbox |
| TC-E2-030-01 | AC1, BR1, BR2 | Component | Case "RW-2026-000901", 14 documents, 9 checklist items |
| TC-E2-030-02 | AC2, BR5 | Component | Sample "LEGAL-S1" version 1, 50 cases; 46 agree on "DEMAND_NOTICE_PROOF" |
| TC-E2-030-03 | AC3, BR6 | Component | Version "P2" SHADOW with review date 2027-03-15 |
| TC-E2-030-04 | AC4, BR4 | Component | Document "D-7001" of another case in the pack |
| TC-E2-030-05 | AC5, BR3 | Component | No status for "MORTGAGE_DEED" |
| TC-E2-030-06 | AC6, BR8 | Component | A 503 from the rwb-document mock for case "RW-2026-000903" |
| TC-E2-030-07 | AC7, BR6 | Component | 49 scored cases, a proposal in mode L1 |
| TC-E2-030-08 | AC8, BR6 | Component | SHADOW version with no review date |
| TC-E2-030-09 | AC9, BR7 | Component | The loader approves version "P2" |
| TC-E2-030-16 | AC10, X7 | Component | RW-LITOFF calls POST `/admin/agent-evaluations`; refused with 403 and MSG-P4-002; no evaluation run, policy version or score row changes |
| TC-E2-030-17 | AC15, X8 | Component | The model does not answer inside 60 seconds for case "RW-2026-000901"; run TIMED_OUT with fallback true; no second run |
| TC-E2-030-18 | AC16 | Component | A call with no session answers 401; an unknown evaluation report and an unknown version approval answer 404; no row changes |
| TC-E2-030-19 | AC17 | Component | POST `/admin/agent-evaluations` repeated with the same Idempotency-Key returns the stored answer with one evaluation run; the key reused with a different body is rejected |
| TC-E2-030-20 | AC18 | Component | A second approval of APPROVED version "P2" with a new Idempotency-Key; 409 with MSG-GEN-004; the policy row is unchanged |

The legacy cases are kept by ID; the covering step of each is the one of the legacy story and the Given, When and Then are the criteria of section 7. The level is Component because each case runs the service against its contract mocks, and TC-E2-030-10 is Contract because it proves the right on the operation.

### 17. Guardrails

- No business value in code: the 9 checklist items, the minimum sample, the review date and the timeout are data with a version (BR9).
- No personal data in logs, tests, prompts or events; field values are masked before the model call and the masked value only is read.
- No read of another service's tables: the case, the legal action, the documents, the fields and the checklist come through their contracts (BR8).
- The agent never changes a write-once legal document, a pack, a legal action or a case field in shadow (BR1).
- The pack is returned by no operation and published on no topic (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested | Business Requirements Program, section 5.11 | FEAT-AGT-09 | 8.2 Instruct and file | R-LIT-16, R-LIT-17, R-UNI-33 | TC-E2-030-01, TC-E2-030-02, TC-E2-030-03, TC-E2-030-04, TC-E2-030-05, TC-E2-030-06, TC-E2-030-07, TC-E2-030-08, TC-E2-030-09, TC-E2-030-10, TC-E2-030-11, TC-E2-030-12, TC-E2-030-13, TC-E2-030-14, TC-E2-030-15, TC-E2-030-16, TC-E2-030-17, TC-E2-030-18, TC-E2-030-19, TC-E2-030-20 |
| REQ-DCM-011 | The document checklist of a case type is reference data, and every pack is checked against it | Business Requirements Program, section 5.11 | FEAT-AGT-09 | 8.2 Instruct and file | R-LIT-16, CTL-19 | TC-E2-030-01, TC-E2-030-05 |

Both requirements are carried from the legacy story; the second is the requirement the plan assigns to this key. The contract slice is RWB-P10-E2030-CON and the cross-service proof is the wave-2 integration harness, not this story.

### 19. Out of scope

- Pack assembly, retrieval requests and officer verification in the litigation flow (Epic 5, S4).
- Showing a pack to an officer at L1 (Epic 5).
- Extraction for the stage 2 and 3 document types (RWB-P5-E2025-APP).
- The event-triggered run paths of rwb-agent (`CaseCreated`, `DocumentStored`) and the case-output read and feedback of the L1 stories.
- The contract document and its fakes (RWB-P10-E2030-CON), the deployment of the service (the OPS stories of P10) and the integration proof against the real P5, S4 and P3 services.
