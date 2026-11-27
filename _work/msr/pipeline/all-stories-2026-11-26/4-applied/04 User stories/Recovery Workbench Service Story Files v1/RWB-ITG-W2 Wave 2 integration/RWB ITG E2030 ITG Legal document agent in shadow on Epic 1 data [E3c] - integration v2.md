# RWB-ITG-E2030-ITG Legal document agent in shadow on Epic 1 data [E3c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2030-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P5-E2025-APP, RWB-P10-E2030-APP, RWB-P5-E2030-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-011) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-030 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E2030-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the shadow run of the legal document agent over the packs our officers built for 50 Epic 1 cases proven end to end across rwb-agent and rwb-document, with the pack, the agreement per checklist item and the keep-shadow decision in one evidence pack attached to the wave 2 release**, so that **the agent reaches Epic 5 with a known accuracy per pack item that the agent runtime, the document hub and the case record all describe for the same case on the same business date**.

This story builds the harness, its contract fakes, its seed pack, its evidence pack and its pass or fail gate. It builds no production endpoint, no screen, no table and no migration. Nothing it writes is deployed to a service.

No single app story can prove the journey. RWB-P10-E2030-APP can prove that a sample is loaded, that an evaluation over it runs and is scored, that the agreement per checklist item is stored with its sample size, and that a policy version is loaded, checked and approved with its approver and date. RWB-P5-E2030-APP can prove that the checklist for a case type is served as reference data and that the documents of a case are returned with their fields. RWB-P5-E2025-APP can prove that the fields of the stage 2 and 3 document types — court filings, hearing notices, judgments, contracts and mortgage documents — are extracted and readable. What only their agreement proves is the thing the business is being asked to accept: that the 50 packs of sample "LEGAL-S1" are assembled from the documents and the checklist of the same case, that every item carries exactly one status, that the score of 0.9200 per item is computed from those same packs, and that the version which records the decision to keep shadow names that evaluation and that approver. A changed checking rule, a checklist item served for the wrong case type, a document read that returns another case's paper or a score computed over a different sample each passes its own story and breaks the journey; only this story runs all of them as one.

### 2. Business rationale

RWB-E2-030 split into two app stories and this integration story. RWB-P10-E2030-APP builds the legal document agent inside rwb-agent: the prompt and the output schema, the input assembly, the SCHEMA and SCHEMA_RULE checks, the TOOL_UNAVAILABLE path, the scorer, the promotion-proposal validator and the policy version with its approval. RWB-P5-E2030-APP builds the document checklist per case type as reference data and the case document reads the agent needs. Neither of them can prove, alone, that a pack assembled from one case is scored against the checklist of that case type, that a wrong document is refused before it is scored, or that the number the committee is shown comes from the packs the officers actually built. That proof is this story.

The chain the business relies on is the one the harness walks: the "LEGAL-S1" version 1 sample of 50 officer-built packs is loaded; the agent runs in shadow over the real Epic 1 cases of that sample; the agreement is computed per checklist item against what the officers put in each pack; and the decision to keep shadow or promote is recorded as a policy version with its approver and its date. Throughout, the pack never reaches a user and never changes a document, a legal action or a case. A litigation pack that reaches the law firm with a missing or defective document is returned and the filing waits; this journey is how the bank learns, before Epic 5, whether the agent would have assembled that pack correctly.

The legacy story cites REQ-S4-002, and the split plan assigns REQ-DCM-011 to this integration story: a document checklist per case type is held as reference data so that a missing document is visible. That requirement is the spine of the harness — the 9 items of "MORTGAGE_CIVIL" are read from the document hub and every score is per item — and no other requirement id is added here.

Architecture v5 changes the path, not the business. In the monolith the agent client, the sample, the evaluation and the pack sat in one deployment and one schema. In the target:

- every document, field and checklist item enters the pack through a published contract; no service reads another service's tables and the harness reads no schema at all (DP-01);
- the minimum sample of 50, the review-date rule and the mode a proposal is checked against are parameters and policy values seeded as data, so a change is a load and not a release (DP-06);
- the checklist per case type and the statuses PRESENT, MISSING and DEFECT are reference data served by rwb-case's reference-data contract, which is how REQ-DCM-011 is met (DP-07);
- the run event and the two document events are CloudEvents on the owner's topics, with an outbox on the producer and an inbox on the consumer, so a duplicate never counts twice (DP-09);
- every path is on the owner's base `/api/recovery/<short>/v1`, never the monolith base (DP-13);
- the journey runs through the gateway-bff composite route the monitor and the export use, so a routing defect fails the harness before a score is quoted to a committee (DP-19).

The measure is the journey evidence: for each owned criterion, one pass or fail with the sample rows, the pack and its completeness list, the run status and fallback flag, the agreement rows with their sample size, the policy version with its mode, review date, approver and approval date, and the message of each refusal, all captured in one report that can be re-run for any build.

### 3. Preconditions

- Policy "LEGAL_DOC" version "P1" with mode SHADOW, prompt "PR1" and a timeout of 60 seconds, with the allowed tools read_case, read_legal_actions, read_documents, read_document_fields and read_checklist and output schema "legal-pack-v1" (legacy section 3).
- Sample "LEGAL-S1" version 1 holds 50 Epic 1 litigation cases, one row per case and checklist item with the expected status PRESENT, MISSING or DEFECT (legacy section 3).
- Case type "MORTGAGE_CIVIL" holds 9 checklist items including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF" (legacy sections 3 and 7).
- Litigation case "RW-2026-000901" holds 14 documents and an open legal action; case "RW-2026-000902" holds document "D-7001", the document the model stub names in the wrong pack (legacy AC1, AC4).
- Case "RW-2026-000903" runs with the P5 document interface unavailable, so the run holds TOOL_UNAVAILABLE and the case is listed as not run and 49 of the 50 are scored (legacy AC6).
- 46 of the 50 sample cases agree on "DEMAND_NOTICE_PROOF", which is agreement rate 0.9200 (legacy AC2).
- The keep-shadow version "P2" carries review date 2027-03-15 and the evaluation run ID, and "coe.user01" is the loader who may not approve it (legacy AC3, AC9).
- The three integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-P10-E2030-APP (rwb-agent: the sample load, the evaluation, the agreement scoring, the policy version and its approval), RWB-P5-E2030-APP (rwb-document: the checklist reference data and the case documents) and RWB-P5-E2025-APP (rwb-document: the fields extracted from the stage 2 and 3 document types).
- The wave 2 harness environment (SIT) with the gateway route for `/api/recovery/*`, the topics `rwb.agent.events.v1` and `rwb.document.events.v1`, the task queue `rwb-agent` and the model stub. Not specified in the source documents (GAP-0412; ASM-0587): the harness environment and its seeding, the LEGAL-S1 version 1 fixture, the 9-item MORTGAGE_CIVIL fixture, the model-stub behaviours, the P5-down control, the evidence format and its retention, and the pass and fail gate.
- The feature switch `rwb.agent.legal-shadow` is on in the harness profile (legacy section 13), and synthetic cases and masked field values only enter the harness, the seed pack and the evidence (legacy section 17).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date and the versions of the three contracts it is about to exercise.
2. Harness: seeds the 9-item checklist of case type "MORTGAGE_CIVIL" and the "LEGAL-S1" version 1 sample of 50 Epic 1 litigation cases, one row per case and checklist item carrying PRESENT, MISSING or DEFECT, with the policy fixture LEGAL_DOC P1 in mode SHADOW and prompt PR1.
3. Harness: calls the P4 session operation against the rwb-access fake and records the role, the scope and the Rules and parameters right the journey runs under.
4. Harness: subscribes to `rwb.agent.events.v1` and `rwb.document.events.v1` with its own consumer group before the first run, so the run window opens before the sample is used.
5. Harness: loads the sample through `POST /api/recovery/agent/v1/admin/agent-samples` and records the sample code, its version and the number of rows the service accepted.
6. Harness: starts the evaluation of "LEGAL_DOC" through `POST /api/recovery/agent/v1/admin/agent-evaluations`, then reads `GET /api/recovery/agent/v1/admin/agent-evaluations` until the evaluation run leaves RUNNING and reaches DONE inside the run window, recording the evaluation run ID.
7. Harness: reads `GET /api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report` and asserts one row per checklist item with sample size 50, and 0.9200 for "DEMAND_NOTICE_PROOF" with 46 agreeing cases against the officers' packs.
8. Harness: runs the guardrail cases — the pack of case "RW-2026-000901" naming "D-7001" of case "RW-2026-000902", and an answer with no status for item "MORTGAGE_DEED" — and asserts status GUARDRAIL_FAILED with check SCHEMA_RULE and with check SCHEMA, then the RW-LITOFF refusal of the evaluation start with 403 and MSG-P4-002.
9. Harness: runs the 49-case evaluation with the P5 document interface down for case "RW-2026-000903" and asserts status TOOL_UNAVAILABLE with fallback true, the case listed as not run, and a sample size of 49.
10. Harness: loads policy version "P2" with mode SHADOW, review date 2027-03-15 and the evaluation run ID through `POST /api/recovery/agent/v1/admin/agent-configs`, records the refusals of 422 with MSG-P10-001 for the L1 proposal over 49 scored cases and for the SHADOW version without a review date, approves "P2" as RW-RISK through `POST /api/recovery/agent/v1/admin/agent-configs/{versionId}/approve`, and records the 409 with MSG-P7-002 when "coe.user01" approves their own version.
11. Harness: reads the policy back through the approval answer and the evaluation report and asserts version "P2", mode SHADOW, review date 2027-03-15, the evaluation run ID, the approver role RW-RISK and the approval date.
12. Harness: writes the per-scenario evidence into one run report keyed by story key and business date, evaluates the gate, attaches the report to the wave 2 release record, releases the lock and restores the seed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent names a document that belongs to another case | Check SCHEMA_RULE fails; the run holds GUARDRAIL_FAILED and is scored as wrong for every item | None to a user | AC4 |
| X2 | A checklist item has no status in the answer | Check SCHEMA fails; the run holds GUARDRAIL_FAILED | None to a user | AC5 |
| X3 | The document interface is unavailable during a run | Run status TOOL_UNAVAILABLE and fallback true; the case is scored as not run and listed (R-UNI-33) | None to a user | AC6 |
| X4 | Fewer than 50 scored cases | A promotion to L1 is refused; keeping shadow is allowed | MSG-P10-001 | AC7 |
| X5 | Keep shadow without a review date | The load is refused | MSG-P10-001 | AC8 |
| X6 | The loader approves their own decision | The approval is refused with 409 | MSG-P7-002 | AC9 |
| X7 | A role without the right starts an evaluation | Refused with 403 | MSG-P4-002 | TC-E2-030-10-ITG |
| X8 | The seed pack cannot be loaded (a case without one row per checklist item, the checklist absent, the policy fixture missing, the counts off) | The run refuses to start and names the missing seed item; no scenario is reported | None | All |
| X9 | The evaluation does not leave RUNNING inside the run window | The scenario is reported as not run and the gate stays Failed; no score is quoted | None | AC2, AC3 |
| X10 | The evidence pack cannot be attached to the release record | The run is marked failed and the local evidence file is kept for rerun | None | All |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the three published contracts or their fakes, the checklist and sample fixtures and the model stub; it builds no service feature and has no build dependency |
| Negotiable | The scenarios, the 9 checklist items, the 50 sample rows, the score, the review date and the policy fixture are data files, never code |
| Valuable | The shadow journey is proven once across two services, with the pack, the score and the keep-shadow decision in one evidence pack |
| Estimable | One journey runner, one fake set, one fixture pack, three assertion helpers, one evidence collector, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a fixed Given, When and Then and a recorded pass or fail in the report |

### 7. Acceptance criteria

```gherkin
Feature: Legal document agent in shadow on Epic 1 data [E3c]

  Background:
    Given policy "LEGAL_DOC" version "P1" with mode "SHADOW" and prompt "PR1"
    Given the checklist for case type "MORTGAGE_CIVIL" has 9 items including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF"

  Scenario: AC1 The shadow pack (new, D-RCV-60)
    Given litigation case "RW-2026-000901" with 14 documents and an open legal action
    When the harness starts the evaluation of "LEGAL_DOC" for the case and the run completes
    Then a pack listing document IDs for each of the 9 items and a completeness list with PRESENT, MISSING or DEFECT per item are stored on the agent run
    Then no document, legal action, task or case field changes
    Then no user-facing operation returns the pack

  Scenario: AC2 The score per checklist item (new, D-RCV-60)
    Given 50 shadow packs for sample "LEGAL-S1" version 1
    When the evaluation runs
    Then the report stores agreement with the officers' packs per item with sample size 50
    Then for "DEMAND_NOTICE_PROOF" with 46 agreeing cases the agreement rate is 0.9200

  Scenario: AC3 The keep-shadow proposal (new, D-RCV-60)
    Given the 50-case evaluation has reached status "DONE" with the score of AC2
    When RW-COE loads policy "LEGAL_DOC" version "P2" with mode "SHADOW", review date 2027-03-15 and the evaluation run ID, and RW-RISK approves it
    Then version "P2" holds mode "SHADOW", review date 2027-03-15 and the evaluation run ID, with the approver and the approval date recorded
    Then a proposal with mode "L1" is accepted only when every stated condition is met by the evaluation

  Scenario: AC4 A document from another case (new, D-RCV-60)
    Given the model stub names document "D-7001" of case "RW-2026-000902" in the pack of case "RW-2026-000901"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED" and check "SCHEMA_RULE"
    Then the case is scored as wrong for every item

  Scenario: AC5 An item without a status (new, D-RCV-60)
    Given the answer has no status for item "MORTGAGE_DEED"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED" and check "SCHEMA"

  Scenario: AC6 The document interface is down (new, D-RCV-60)
    Given the P5 document interface is unavailable for case "RW-2026-000903"
    When the agent runs
    Then the run holds status "TOOL_UNAVAILABLE" and fallback true
    Then the evaluation lists the case as not run and scores 49 cases

  Scenario: AC7 Too few cases to promote (new, D-RCV-60)
    Given the evaluation scored 49 cases
    When RW-COE loads a proposal with mode "L1"
    Then the load is refused with 422 and MSG-P10-001 naming check "sample size at least 50"

  Scenario: AC8 Keep shadow without a review date (new, D-RCV-60)
    When RW-COE loads version "P2" with mode "SHADOW" and no review date
    Then the load is refused with 422 and MSG-P10-001 naming check "review date present"

  Scenario: AC9 The loader cannot approve (new, D-RCV-60)
    Given user "coe.user01" loaded version "P2"
    When user "coe.user01" approves it
    Then the approval is refused with 409 and MSG-P7-002
```

No legacy acceptance criterion is owned by this story: the nine above are new and test only the integration deliverable, using the legacy values of RWB-E2-030 and no other. The access case of section 16 sits beside them because a harness has no screen on which a refusal could be seen.

### 8. Business rules

| ID | Rule | Source | Proved by |
|---|---|---|---|
| BR1 | In SHADOW mode the pack and the completeness list are stored only; no pack, document or legal action changes | agent_policy.autonomy_mode | AC1 |
| BR2 | Checklist items come from the document checklist held for the case type | The document checklist reference table; REQ-DCM-011 | AC1 |
| BR3 | Every item has a status PRESENT, MISSING or DEFECT, and every DEFECT has a reason | R-LIT-16, R-LIT-17; CTL-19 | AC1, AC5 |
| BR4 | A pack may name only documents of the same case | CTL-19; CTL-11 | AC4 |
| BR5 | Agreement per item = the cases where the agent status equals the officer status / the scored cases, at 4 decimals | agent_evaluation.agreement_rate | AC2 |
| BR6 | A promotion to L1 needs at least 50 scored cases (assumed); keeping shadow needs a review date | agent_policy.review_date and the assumed minimum sample of 50 | AC7, AC8 |
| BR7 | The loader and the approver are different people | Separation of duty | AC9 |

The rules are unchanged by the split. The harness asserts them across the service boundaries and restates none of them in code: the 9 items, the three statuses, the minimum sample, the review date and the mode are seeded data.

### 9. State transitions

None for the case. This story does not change a case status and does not move a case into PACK_ASSEMBLY; the harness asserts that no status, task or field moves because of a pack. It writes agent runs, one evaluation run from RUNNING to DONE and one policy version from LOADED to APPROVED.

The agent run carries the status rwb-agent gives it, and the harness asserts only the three the legacy story names: the completed run behind a scored pack, "GUARDRAIL_FAILED" with check SCHEMA_RULE or SCHEMA, and "TOOL_UNAVAILABLE" with fallback true for a run whose document interface was down. The policy version carries one mode, SHADOW or L1, with its review date and its approver.

The harness adds a run state of its own only: Not started, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT | Reads the case, the legal actions, the documents, the fields and the checklist; writes the run, the pack and the completeness list through rwb-agent's own contract, never through the harness |
| RW-COE | Loads the sample, starts the evaluation, loads the decision version (Rules and parameters CRUD) |
| RW-RISK | Approves the decision version (Rules and parameters A) |
| RW-LITOFF | Supplies the officers' packs for the sample; reads the scores through the export; refused the evaluation start and the version load |
| RW-HEADLIT | Reads the scores through the export |
| Integration lead | Agrees the fake set, the model stub and the run window with the two service owners |
| QA lead | Owns the seed pack, the evidence format and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision; the approval it exercises is the policy approval of RW-RISK |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 case operation |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 case operation |
| DF-CAS-017 | recovery_case | prescription_date | Read through the P3 case operation |
| DF-LEG-001 | legal_action | id | Read by rwb-agent under its read_legal_actions tool; the harness reads the stored run, never the litigation table |
| DF-LEG-004 | legal_action | action_type | Read by rwb-agent under its read_legal_actions tool; the harness reads the stored run |
| DF-LEG-014 | legal_action | status | Read by rwb-agent under its read_legal_actions tool; the open legal action of AC1 is asserted from the run |
| DF-DOC-001 | document | id | Read through the P5 document and checklist operations |
| DF-DOC-002 | document | case_id | Read through the P5 case document operation; the same-case check of AC4 |
| DF-DOC-004 | document | document_type | Read through the P5 document operation |
| DF-DOC-010 | document | write_once | Read through the P5 document operation |
| DF-DOC-014 | document_field | field_name | Read through the P5 document operation |
| DF-DOC-015 | document_field | field_value | Read through the P5 document operation, masked |
| DF-AGT-036, DF-AGT-037, DF-AGT-038 | agent_run | id, agent_code, agent_version | Written by rwb-agent through its own contract; read through the P10 agent-run operation |
| DF-AGT-041, DF-AGT-042, DF-AGT-043, DF-AGT-044 | agent_run | case_id, subject_id, autonomy_mode, trigger_event | Written by rwb-agent; read through the P10 agent-run operation |
| DF-AGT-046, DF-AGT-047, DF-AGT-048 | agent_run | status, fallback, guardrail_result | Written by rwb-agent; read through the P10 agent-run operation (AC4, AC5, AC6) |
| DF-AGT-049, DF-AGT-051, DF-AGT-052, DF-AGT-053, DF-AGT-054 | agent_run | output, latency_ms, tokens_in, tokens_out, cost_thb | Written by rwb-agent; the pack and the completeness list of AC1 are read from output through the P10 agent-run operation |
| DF-AGT-056, DF-AGT-057 | agent_run | run_at, evaluation_run_id | Written by rwb-agent; read through the P10 agent-run operation, and the run ID links each pack to its score |
| DF-AGT-063, DF-AGT-064, DF-AGT-066 | agent_sample | sample_code, sample_version, subject_id | Written on the P10 sample load; read back through the P10 sample and report operations |
| DF-AGT-067, DF-AGT-068 | agent_sample | label_key, expected_value | Written on the P10 sample load; the 50 cases with one row per case and checklist item are this fixture (AC2) |
| DF-AGT-087, DF-AGT-089, DF-AGT-090, DF-AGT-094 | agent_evaluation | evaluation_run_id, label_key, sample_size, agreement_rate | Written by rwb-agent; read through the P10 evaluation and report operations (AC2, AC6, AC7) |
| DF-AGT-003, DF-AGT-008, DF-AGT-016, DF-AGT-017, DF-AGT-018 | agent_policy | policy_version, autonomy_mode, review_date, evaluation_run_id, promotion_conditions | Written through POST /admin/agent-configs; read back through the approval answer and the report (AC3, AC7, AC8) |
| DF-AGT-021, DF-AGT-025 | agent_policy | status, approved_by | Written through the approve operation; read back through the approval answer (AC3, AC9) |

The harness owns no table in any schema (DP-01) and runs no migration: no schema, no table, no view and no seed table is created by this story. Every value above is read or written through the operations of section 12, and the evidence holds identifiers, statuses, message ids, rates and timestamps only, never personal data. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/agent/v1/admin/agent-samples` | P10 rwb-agent | Loads sample "LEGAL-S1" version 1 with its 50 cases and one row per case and checklist item (AC1, AC2) |
| POST | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | Starts the evaluation of "LEGAL_DOC" over the sample and returns the evaluation run ID the version will name (AC2, AC6, AC7) |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | Reads the evaluation state RUNNING or DONE and its run ID, so the gate waits on the service and not on a timer (AC2, AC6) |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations/{evaluationId}/report` | P10 rwb-agent | Reads the agreement per checklist item, the sample size, the cases listed as not run and the version the score belongs to (AC2, AC3, AC6) |
| POST | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | Loads version "P2" with mode SHADOW, review date 2027-03-15 and the evaluation run ID; 422 with MSG-P10-001 on a failed check (AC3, AC7, AC8) |
| POST | `/api/recovery/agent/v1/admin/agent-configs/{versionId}/approve` | P10 rwb-agent | Approves as RW-RISK and records the approver and the approval date; 409 with MSG-P7-002 for the loader (AC3, AC9) |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | Reads the run of each sample case: status, fallback flag, guardrail result, agent version and evaluation run ID (AC1, AC4, AC5, AC6) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case a pack is assembled for, its product group and its prescription date (AC1) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | Reads the 14 documents of case "RW-2026-000901" and the case each document belongs to, for the same-case assertion of AC4 |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | Reads one document with its type, its write-once flag and its fields, masked (AC1, AC4) |
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` | P5 rwb-document | Reads the 9-item checklist of case type "MORTGAGE_CIVIL" that the pack is scored against (AC1, AC2) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout, and every POST carries an If-Match and a key per write. The P4 session operation of flow step 3 is called against the rwb-access fake only and is not a production path of this story, so it is not one of the eleven rows above.

#### 12.3 Events published

None. The harness publishes no Kafka event on a production topic; its evidence goes to the release record through the pipeline.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Closes the run window for each sample case and gives the run ID, the status, the guardrail result and the fallback flag before the run is read (DP-09) |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | Confirms that the 14 documents of case "RW-2026-000901" reached the topic inside the run window, so the document read is taken on a settled state |
| `rwb.document.DocumentFieldsExtracted.v1` | `rwb.document.events.v1` | P5 rwb-document | Confirms that the fields the agent reads were extracted and offered to consumers, alongside the P5 document read of 12.2 (DP-09) |

The harness consumes with its own consumer group and never reads a producer's outbox, inbox or schema. A duplicate is expected and deduplicated on the harness side, so a re-run of the same business date is deterministic.

#### 12.5 Workflows and activities

`AgentRunWorkflow` on queue `rwb-agent` is observed, not built: the run has a 60 s limit and then the rule result (R-UNI-32), and the harness asserts which of the two the run ended on through the status and the fallback flag. The agent call to the model stub, the guardrail checks and the storage of the pack belong to RWB-P10-E2030-APP.

The harness starts no workflow, adds no activity and writes no schedule.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow; the 60 s limit inside `AgentRunWorkflow` is the owner's and is only observed.

#### 12.7 Tables owned

None. The harness owns no table in any schema (DP-01) and runs no migration; it reads and writes through the operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-agent | The seven P10 operations of 12.2 | OpenAPI of P10 | The sample load, the evaluation start and its read (RUNNING then DONE, sample size 50 then 49), the report with one row per item and 0.9200 for "DEMAND_NOTICE_PROOF", the version load and the approval with the approver and the date, 409 with MSG-P7-002 for "coe.user01", 422 with MSG-P10-001 naming "sample size at least 50" and naming "review date present", and the runs with GUARDRAIL_FAILED, check SCHEMA_RULE, check SCHEMA and TOOL_UNAVAILABLE with fallback true; keeps the request journal for the If-Match and ordering assertions |
| WireMock rwb-document | The three P5 operations of 12.2 | OpenAPI of P5 | The 14 documents of case "RW-2026-000901" with their fields masked, "D-7001" belonging to case "RW-2026-000902", the 9-item checklist of "MORTGAGE_CIVIL" including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF", the 46-of-50 cases of AC2 and the P5-down case "RW-2026-000903" of AC6 |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases/{caseId}` | OpenAPI of P3 | The litigation case, its product group and its prescription date |
| WireMock rwb-access | The P4 session operation | OpenAPI of P4 | The session and the Case record right of RW-COE, RW-RISK and RW-LITOFF, and the RW-LITOFF refusal of the evaluation start with MSG-P4-002 |
| Model stub | The model call the legal document agent makes | The rwb-agent model profile, not in this workspace | A pack per case: "D-7001" of another case in the pack of "RW-2026-000901" for AC4, no status for "MORTGAGE_DEED" for AC5, and a valid pack for each of the 50 sample cases so the score can be computed; masking tokens in place of field values |

Each fake is replaced by the real service as its integration dependency lands, without a change to the scenarios. Not specified in the source documents (GAP-0412; ASM-0587): the fake set, the concrete fixture values, the model stub, the harness environment and the evidence format.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 11 consumed, one hop on the owner's base with the 2 s timeout; the P4 session operation is called against the fake only |
| Kafka | 3 events consumed on `rwb.agent.events.v1` and `rwb.document.events.v1`; none published |
| Temporal | Observed only: `AgentRunWorkflow` on queue `rwb-agent` with the 60 s limit and the rule result of R-UNI-32; no workflow, activity or schedule added |
| File | None |

### 13. Solution plan

**Package.** Folder `integration/recovery-agent-legal` in the ACE repository, package `<ACE base package>.recovery.integration.agentlegal`. Not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The harness owns no table and reads no schema; every document, field and checklist item in the evidence arrives through a P5 or P3 operation, never from `rwb_document` or `rwb_agent` |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The minimum sample of 50, the review-date rule and the mode a proposal is checked against are seeded parameters, so a change is a parameter load and not a harness release |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The 9 items of "MORTGAGE_CIVIL" and the statuses PRESENT, MISSING and DEFECT are seeded reference data, never values in the harness code (REQ-DCM-011) |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | The harness subscribes with its own consumer group and asserts the three events, never a producer's table; a duplicate never counts twice |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 uses the owner's base, so the harness never calls a monolith base |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the monitor and the export use, on the same bases, so a routing defect fails the harness before a score is quoted |

The platform H dependencies in the table (H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the three I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date and holds the run lock |
| FakeRegistry | Configuration | WireMock mappings for rwb-agent, rwb-document, rwb-case and rwb-access, one set per contract version, plus the model stub selection |
| LegalFixturePack | Data | The "LEGAL-S1" version 1 sample of 50 cases with one row per case and item, the 9-item "MORTGAGE_CIVIL" checklist, the policy fixture LEGAL_DOC P1 and P2, the 14 documents of case "RW-2026-000901" and the four seeded cases, per scenario |
| PackAssertion | Service | Compares the pack and the completeness list per item with the fixture, and asserts that no document, legal action, task or case field changed and that no user-facing operation returns the pack |
| AgreementAssertion | Service | Compares the agreement per item, the sample size 50 and the rate 0.9200 for "DEMAND_NOTICE_PROOF" with the fixture |
| ProposalAssertion | Service | Loads the version, approves it, and checks the mode, the review date, the evaluation run ID, the approver and the date, and the message of each refusal |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with the pack, the run statuses and fallback flags, the agreement rows, the version and its approver |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached to the release record |

**Environment and test data.** SIT, the wave 2 harness profile, one business date, the "LEGAL-S1" version 1 sample and synthetic litigation cases only. The seeded values are the legacy section 3 and section 7 values — the policy LEGAL_DOC P1 in mode SHADOW with prompt PR1, the 9 items of "MORTGAGE_CIVIL", the 50 cases, cases "RW-2026-000901", "RW-2026-000902" and "RW-2026-000903", 46 of 50 at 0.9200 and review date 2027-03-15; no other value is added. A run starts from the seeded state, so a repeated run is deterministic and produces the same report. Not specified in the source documents (GAP-0412; ASM-0587): the environment, the seed pack, the model stub and the evidence format.

**Build steps**

1. Write LegalFixturePack with the policy, the 9-item checklist, the 50 sample rows, the four cases and the score; test that a bad seed stops the run (X8).
2. Write FakeRegistry with the four WireMock mapping sets and the model stub, and prove the harness runs green on the fakes alone from Day 1.
3. Write JourneyRunner for AC1: load the sample, start the evaluation, read the run and assert the pack and the completeness list, and that no document, legal action, task or case field moved.
4. Add AC2 with the report read: one row per item, sample size 50 and 0.9200 on "DEMAND_NOTICE_PROOF".
5. Add AC4 and AC5 with the foreign document and the missing status, asserting GUARDRAIL_FAILED with each check name, and the RW-LITOFF refusal of X7.
6. Add AC6 and AC7 with the P5-down control and the 422 on the L1 proposal, then AC8 and AC9 with the SHADOW version without a review date and the loader's own approval.
7. Add AC3 with the version load and the RW-RISK approval, then write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record and rerun the nine scenarios on the release build.

**Feature switch.** `rwb.agent.legal-shadow` is on in the harness profile, as the legacy story sets it. Off, evaluations of LEGAL_DOC are refused with 422 and the harness reports the journey as not applicable rather than as passed. The harness itself is a pipeline stage selected by the run profile, not by a business flag.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all nine owned scenarios and the 0.9200 score, the keep-shadow decision is recorded as version "P2" with its approver and its approval date, and each fake has been replaced by the real service where its I story has landed in SIT. The fixture pack and the evidence sign-off wait for the values of the gap and assumption rows cited in sections 3, 12.8, 13 and 15.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | The decision version fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | Evaluation on an empty sample | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P7-002 | Loader approves own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The harness asserts these messages and never rewrites them. Its own report text is for the release team and is not part of the message standard.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-46 Agent monitor | Shadow | "LEGAL_DOC" in state Shadow with its runs, its fallbacks and the evaluation score; the export through `GET /admin/agent-evaluations` |

The monitor is where a reader would look, so the harness drives the operations behind it: the runs of the sample cases with their statuses and fallback flags, the evaluation row with sample size 50 and 0.9200 on "DEMAND_NOTICE_PROOF", and the version "P2" with its mode, review date, approver and approval date. No screen is built by this story; SCR-46 belongs to RWB-P10-E2031-ITG and to the agent runtime stories. Not specified in the source documents (GAP-0412; ASM-0587): the export format and the retention of the evidence.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-030-10-ITG | Access | Component | RW-LITOFF calls POST /api/recovery/agent/v1/admin/agent-evaluations; refused with 403 and MSG-P4-002 |
| TC-E2-030-01-ITG | AC1, BR1, BR2, BR3 | Integration | Case RW-2026-000901, 14 documents, 9 checklist items |
| TC-E2-030-02-ITG | AC2, BR5 | Integration | Sample LEGAL-S1 version 1, 50 cases; 46 agree on DEMAND_NOTICE_PROOF |
| TC-E2-030-03-ITG | AC3, BR6 | Integration | Version P2 SHADOW with review date 2027-03-15 |
| TC-E2-030-04-ITG | AC4, BR4 | Integration | Document D-7001 of case RW-2026-000902 in the pack of RW-2026-000901 |
| TC-E2-030-05-ITG | AC5, BR3 | Integration | No status for MORTGAGE_DEED |
| TC-E2-030-06-ITG | AC6, BR1 | Integration | P5 interface down for case RW-2026-000903; 49 scored |
| TC-E2-030-07-ITG | AC7, BR6 | Integration | 49 scored cases, proposal L1 |
| TC-E2-030-08-ITG | AC8, BR6 | Integration | SHADOW version with no review date |
| TC-E2-030-09-ITG | AC9, BR7 | Integration | Loader coe.user01 approves P2 |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the app story's case, run across the three contracts and the model stub. The app stories keep the unit and component copies of the same cases. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the 9 checklist items, the three statuses, the minimum sample of 50, the review date and the mode are data in the seed pack or the reference tables, never values in the harness.
- No personal data in events, workflow inputs, logs, evidence or the model call. Field values are masked before the model sees them and the seed holds synthetic litigation cases only.
- No read of another service's tables and no schema of the harness's own: every read and write goes through the operations of 12.2, and the harness runs no migration (DP-01).
- A pack never changes a legal document, a legal action or a case: the harness asserts that the document, the write-once flag, the legal action and the case fields are identical before and after the run.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.
- The harness never runs against UAT or production, and a value that must change changes in the seed pack through a reviewed change, never by an exception in a scenario.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-011 | A document checklist per case type is held as reference data so that a missing document is visible | Business Requirements Epic 1 v5, section 4; Program v4, section 5.5 | FEAT-AGT-09 | 8.2 Instruct and file | R-LIT-16, R-LIT-17, R-UNI-33 | TC-E2-030-01-ITG, TC-E2-030-02-ITG, TC-E2-030-03-ITG, TC-E2-030-04-ITG, TC-E2-030-05-ITG, TC-E2-030-06-ITG, TC-E2-030-07-ITG, TC-E2-030-08-ITG, TC-E2-030-09-ITG, TC-E2-030-10-ITG |

### 19. Out of scope

- Pack assembly, retrieval requests and officer verification in the litigation flow (Epic 5, S4). The harness proves what a pack would contain, not what a case does with it.
- Showing packs to officers at L1 (Epic 5).
- Extraction for the stage 2 and 3 document types (RWB-E2-025); the harness stages the extracted fields through RWB-P5-E2025-APP and asserts none of the extraction itself.
- Production code of any service in the journey: the agent runtime, the checks, the scorer, the proposal validator, the checklist reference data and the document reads belong to their own stories, and the monitor belongs to RWB-P10-E2031-ITG.

The harness, the fakes and the evidence pack cover the items above only as a caller or a consumer would see them; building any of them is out of scope for this story.
