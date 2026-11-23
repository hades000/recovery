<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 062 Deviation screening agent in shadow E2b v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 062 Deviation screening agent in shadow E2b v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-062 Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-062 |
| Epic | E1, release 30 November 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-DVH-01 Flag a deviation X1 to X7 on the case; FEAT-DVH-04 Route the deviation to the named owner; FEAT-DVH-08 Review a flagged deviation below the confidence threshold; FEAT-AGT-08 Run the deviation screening agent at L1 |
| Requirement IDs | REQ-DVH-001, REQ-DVH-003, REQ-DVH-007 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, section 5.15 |
| L3 process | 11 Handle customer care and deviations |
| Decision | X1 to X7 |
| Priority | Must |
| Depends on | RWB-E1-058, RWB-TE-013 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the deviation screening agent to propose X1 to X7 with reasons from case data, call notes and documents, in shadow on Epic 1 cases**, so that **the Epic 2 and Epic 3 deviation flags start from an agent with measured precision and recall per deviation type**.

## 2. Business rationale

A dispute, a death, a fraud sign or a lost contact found late means contact that should have stopped, or a case worked on the wrong route. The screening agent reads the case, the interaction ledger and the documents at entry and when a document arrives, and proposes deviations with reasons. In Epic 1 the proposals are stored only, scored against the business analysts' review and shown to nobody. The story measures detection from case data, call notes and documents (REQ-DVH-001), the named owner each code would route to (REQ-DVH-003) and the contact that preceded a complaint (REQ-DVH-007).

## 3. Preconditions

- RWB-E1-058 and RWB-TE-013 are done.
- Approved agent_policy "SCREENING" version "P1": mode SHADOW, timeout 60 seconds, confidence floor 0.80, allowed tools read_case, read_interactions, read_documents, read_document_fields, and output schema "screening-v1" with codes from LOV-DEVIATION (X1 to X7).
- Approved prompt "SCREENING" version "PR1".
- Rule rows R-DEV-02 to R-DEV-06 are loaded, so the owner role of each code is data.
- Labeled sample "SCREEN-S1" version 1: the business analysts' review of 200 Epic 1 cases, one row per case and code with expected value Y or N.

## 4. Flow

1. SY-CASEWF or P5: writes EV-01 CaseCreated for a new case, or EV-16 DocumentStored for a document on an open case.
2. System (ScreeningShadowListener): calls the orchestrator for agent "SCREENING" with key "SCREENING:<caseId>:<eventId>".
3. System: reads the case, the interaction ledger entries, the documents and their fields as SY-AGENT, masks personal fields and calls the model.
4. System: checks the answer: each proposal has a code in X1 to X7, reasons, source references and a confidence.
5. System: asks the rules component which owner role each proposed code routes to (R-DEV-02 to R-DEV-06) and stores it with the proposal.
6. System: marks proposals below the confidence floor as "review"; stores everything on the agent run in mode SHADOW. No deviation record, contact stop or clock change is made.
7. RW-COE: starts the evaluation of "SCREENING" on sample "SCREEN-S1".
8. System: compares proposals at or above the floor with the labels and stores precision and recall per deviation code, with the count of review proposals.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The answer has a code outside X1 to X7 | Check SCHEMA fails; run GUARDRAIL_FAILED; fallback true | None to a user | AC8 |
| X2 | A proposal is below the confidence floor 0.80 | Stored with marker "review"; scored separately | None to a user | AC6 |
| X3 | An X1 proposal names no preceding contact while the ledger holds one in the 30 days before | Check SCHEMA_RULE fails for that proposal | None to a user | AC5 |
| X4 | The same event arrives twice | One run per case and event (R-UNI-40) | None to a user | AC7 |
| X5 | A proposed code has no owner row in R-DEV-02 to R-DEV-06 | Owner role stored as RW-TEAMMGR and the proposal marked "unmapped" | None to a user | AC4 |
| X6 | The agent times out | Run TIMED_OUT, counted, not retried | None to a user | AC9 |
| X7 | A role without the right | Refused with 403 | MSG-P4-002 | TC-E1-062-10 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the platform and client only; no S8 component is called, because nothing is raised in shadow |
| Negotiable | Codes, owner mapping, floor and the 30-day look-back are data values |
| Valuable | Gives the error rate per deviation type that decides the L1 segment in RWB-E2-029 |
| Estimable | Two event listeners, one prompt, one output schema, one scorer |
| Small | Two weeks for one developer and one analyst |
| Testable | Each criterion runs with synthetic cases, call notes and documents |

## 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent in shadow [E2b]

  Background:
    Given agent "SCREENING" has approved policy "P1" with mode "SHADOW", confidence floor 0.80 and prompt "PR1"
    Given rule rows R-DEV-02 to R-DEV-06 are in force

  Scenario: AC1 Shadow flags
    Given 200 cases with their call notes and documents
    When the agent runs
    Then each run stores its proposed codes with reasons and source references in mode "SHADOW"
    Then no deviation record exists, deviation_open stays false on every case and no contact stop is set
    Then no user-facing endpoint returns a proposal

  Scenario: AC2 Compared
    Given the business analysts' flags for the same 200 cases in sample "SCREEN-S1" version 1
    When the comparison runs
    Then one score row per code X1 to X7 holds precision, recall and sample size 200
    Then for X6 with 18 true positives, 2 false positives and 6 false negatives precision is 0.9000 and recall is 0.7500

  Scenario: AC3 A new document starts a run
    Given open case "RW-2026-000401" receives a document of type "DEATH_CERTIFICATE"
    When EV-16 DocumentStored is processed
    Then one shadow run exists with key "SCREENING:<caseId>:<eventId>" and trigger "DocumentStored"

  Scenario: AC4 The owner role comes from the rule rows
    Given the agent proposes X4 for case "RW-2026-000402"
    When the proposal is stored
    Then it holds owner role "RW-FRAUD" from rule R-DEV-04
    Then the system stores a proposed code with no owner row with owner role "RW-TEAMMGR" and marker "unmapped"

  Scenario: AC5 A complaint names the contact before it
    Given case "RW-2026-000403" has an outbound call on 2026-11-25 and a complaint note on 2026-11-27
    When the agent proposes X1
    Then the proposal names the interaction of 2026-11-25 as the preceding contact
    Then an X1 proposal without a preceding contact, when one exists in the 30 days before, fails check "SCHEMA_RULE"

  Scenario: AC6 A low-confidence proposal is marked for review
    Given the agent proposes X2 with confidence 0.72
    When the proposal is stored
    Then it holds marker "review"
    Then the evaluation counts it under "review" and not in precision or recall

  Scenario: AC7 A repeated event
    Given EV-16 for document "D-1001" on case "RW-2026-000401" was processed
    When the same event ID arrives again
    Then one run exists for the case and event and the repeat is counted (R-UNI-40)

  Scenario: AC8 A code outside the list
    Given the model stub returns code "X9"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED", check "SCHEMA" and fallback true

  Scenario: AC9 Timeout
    Given the model stub does not answer for 61 seconds
    When the agent runs for case "RW-2026-000404"
    Then the run holds status "TIMED_OUT" and is not retried for that event
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | In SHADOW mode the screening agent raises nothing: no deviation record, no clock pause, no contact stop | agent_policy.autonomy_mode (New); R-DEV-01 is not fired |
| BR2 | A proposal carries a code from LOV-DEVIATION, reasons, source references and a confidence | LOV-DEVIATION; deviation.deviation_code |
| BR3 | The owner role of a code is read from R-DEV-02 to R-DEV-06; a code with no row maps to the team manager and is marked unmapped | R-DEV-02, R-DEV-03, R-DEV-04, R-DEV-05, R-DEV-06; REQ-DVH-003 |
| BR4 | An X1 proposal names the latest interaction in the 30 days before the complaint (30, assumed; held in the policy) | REQ-DVH-007; interaction.occurred_at |
| BR5 | Proposals below the floor are marked review and scored separately | agent_policy.confidence_floor (New); FEAT-DVH-08 |
| BR6 | Precision and recall per code use proposals at or above the floor against Y and N labels | agent_evaluation (New) |
| BR7 | One run per case per triggering event | R-UNI-40 |

## 9. State transitions

None. This story does not change a case status and raises no deviation. In shadow, the rule R-DEV-01 (ANY_STATE, DEVIATION_FLAGGED, to DEV_FLAGGED) is never fired. It writes agent runs and one evaluation run (RUNNING to DONE).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT | Reads case, interactions, documents and fields (Case record R, Documents R) |
| SY-RULES | Evaluates R-DEV-02 to R-DEV-06 for the owner role |
| RW-COE | Loads the sample, starts the evaluation, reads scores (Rules and parameters CRUD) |
| RW-RISK, RW-CONDUCT | Read scores (Rules and parameters R) |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read run metadata (Platform administration R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-038 | deviation | deviation_code | Read (open deviations, so a code already open is not proposed again) |
| DF-INT-001 | interaction | id | Read |
| DF-INT-004 | interaction | occurred_at | Read |
| DF-INT-005 | interaction | channel | Read |
| DF-INT-011 | interaction | summary | Read (masked) |
| DF-DOC-001 | document | id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-014 | document_field | field_name | Read |
| DF-DOC-015 | document_field | field_value | Read (masked) |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-010 | rule_row | owner_role | Read |
| DF-AGT-036 | agent_run | id | Write |
| DF-AGT-037 | agent_run | agent_code | Write |
| DF-AGT-038 | agent_run | agent_version | Write |
| DF-AGT-039 | agent_run | prompt_version | Write |
| DF-AGT-040 | agent_run | model_version | Write |
| DF-AGT-041 | agent_run | case_id | Write |
| DF-AGT-042 | agent_run | subject_id | Write |
| DF-AGT-043 | agent_run | autonomy_mode | Write |
| DF-AGT-044 | agent_run | trigger_event | Write |
| DF-AGT-045 | agent_run | idempotency_key | Write |
| DF-AGT-046 | agent_run | status | Write |
| DF-AGT-047 | agent_run | fallback | Write |
| DF-AGT-048 | agent_run | guardrail_result | Write |
| DF-AGT-049 | agent_run | output | Write |
| DF-AGT-050 | agent_run | confidence | Write |
| DF-AGT-051 | agent_run | latency_ms | Write |
| DF-AGT-052 | agent_run | tokens_in | Write |
| DF-AGT-053 | agent_run | tokens_out | Write |
| DF-AGT-054 | agent_run | cost_thb | Write |
| DF-AGT-056 | agent_run | run_at | Write |
| DF-AGT-063 | agent_sample | sample_code | Read |
| DF-AGT-064 | agent_sample | sample_version | Read |
| DF-AGT-066 | agent_sample | subject_id | Read |
| DF-AGT-067 | agent_sample | label_key | Read |
| DF-AGT-068 | agent_sample | expected_value | Read |
| DF-AGT-087 | agent_evaluation | evaluation_run_id | Write |
| DF-AGT-089 | agent_evaluation | label_key | Write |
| DF-AGT-090 | agent_evaluation | sample_size | Write |
| DF-AGT-091 | agent_evaluation | true_positive | Write |
| DF-AGT-092 | agent_evaluation | false_positive | Write |
| DF-AGT-093 | agent_evaluation | false_negative | Write |
| DF-AGT-095 | agent_evaluation | precision_value | Write |
| DF-AGT-096 | agent_evaluation | recall_value | Write |
| DF-AGT-070 | agent_evaluation_run | id | Write |
| DF-AGT-077 | agent_evaluation_run | status | Write |
| DF-AGT-083 | agent_evaluation_run | failure_counts | Write |
| DF-AGT-085 | agent_evaluation_run | review_count | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Events consumed:** EV-01 CaseCreated and EV-16 DocumentStored (documentId, caseId, type, source); idempotent on event ID.

**Event published:** EV-28 AgentRunCompleted (runId, agent "SCREENING", caseId, outcome, fallback).

**Output schema "screening-v1":** proposals (array of {code in X1..X7, reasons (array of strings, masked), sourceRefs (interaction or document IDs), precedingContactId (X1 only), confidence}).

**Interfaces called:** P3 CaseQueryService.getCase, P7 InteractionLedgerReader.list(caseId, from, to), P5 DocumentQueryService.listByCase and getFields, P3 RuleEvaluator.ownerFor(routeSet "Deviations", event "OWNER_ASSIGNED", deviationCode); all as SY-AGENT or SY-RULES.

**POST /api/recovery/v1/admin/agent-evaluations** and **GET /api/recovery/v1/admin/agent-evaluations** (new, RWB-E1-058): agent "SCREENING", sample "SCREEN-S1"; Rules and parameters C and R; errors 401, 403, 409 (MSG-P10-003), 422 (MSG-P10-002), 503.

**GET /api/recovery/v1/admin/agent-runs** (api.yaml): metadata only; Platform administration R.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/screening/`, Java package `recovery.agent.screening`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ScreeningShadowListener | Listener | Consumes EV-01 and EV-16; calls the orchestrator with the run key |
| ScreeningInputAssembler | Service | Builds masked inputs: case, ledger entries of the last 180 days, documents and fields |
| ScreeningOwnerResolver | Service | Adds the owner role from the rule rows to each proposal |
| ScreeningRuleChecks | Service | Adds SCHEMA_RULE checks: code list, preceding contact for X1 |
| ScreeningScorer | Service | Precision and recall per code; counts review proposals |
| screening-v1.json, prompt SCREENING PR1 | Rule table | Output schema and prompt, loaded through the configuration endpoint |

**Database:** migration `V10_005__evaluation_review_count.sql` adds review_count integer to agent_evaluation_run. Writes agent_run, agent_evaluation_run and agent_evaluation; reads agent_sample.

**Configuration and reference data:** policy SCREENING P1 (floor 0.80, look-back 30 days, ledger window 180 days) loaded by RW-COE and approved by RW-RISK; LOV-DEVIATION and rule rows R-DEV-02 to R-DEV-06 maintained by the center of excellence.

**Build steps**
1. Write the output schema and prompt; load them in DEV.
2. Build ScreeningInputAssembler with masked ledger summaries (AC1).
3. Build ScreeningShadowListener for both events with idempotency (AC3, AC7, AC9).
4. Build ScreeningOwnerResolver over the rules component (AC4).
5. Build ScreeningRuleChecks for the code list and the preceding contact (AC5, AC8).
6. Build ScreeningScorer with the review split (AC2, AC6).

**Feature flag:** `rwb.agent.screening-shadow`. Off: both listeners ignore their events.

**Done when:** the tests in section 16 pass and a DEV run over 200 synthetic cases gives one score row per code.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-002 | Evaluation on an empty sample | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Same evaluation already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. No case owner or handler sees a proposal. RW-COE reads scores through GET /admin/agent-evaluations.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-062-01 | AC1, BR1 | System | 200 synthetic cases with call notes and documents |
| TC-E1-062-02 | AC2, BR6 | System | Sample SCREEN-S1 version 1; X6 counts 18, 2, 6 |
| TC-E1-062-03 | AC3 | System | Case RW-2026-000401, DEATH_CERTIFICATE document |
| TC-E1-062-04 | AC4, BR3 | System | X4 proposal on case RW-2026-000402; one unmapped code |
| TC-E1-062-05 | AC5, BR4 | System | Call 2026-11-25, complaint note 2026-11-27 |
| TC-E1-062-06 | AC6, BR5 | System | X2 proposal with confidence 0.72 |
| TC-E1-062-07 | AC7, BR7 | System | EV-16 for document D-1001 twice |
| TC-E1-062-08 | AC8, BR2 | System | Model stub returns code X9 |
| TC-E1-062-09 | AC9 | System | Model stub silent 61 seconds |
| TC-E1-062-10 | Access | Access | RW-CASEOWN calls GET /admin/agent-evaluations; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: codes, owner roles, floor and look-back are data rows.
- No personal data in logs, tests or prompts; call note summaries are masked before the model call.
- No read of another module's tables; ledger, case, documents and rules come through their interfaces.
- The agent never calls the S8 deviation service in shadow mode.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-DVH-01, FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-40 | TC-E1-062-01, TC-E1-062-02, TC-E1-062-03, TC-E1-062-06, TC-E1-062-07, TC-E1-062-08, TC-E1-062-09, TC-E1-062-10 |
| REQ-DVH-003 | Each code routes to its named owner; an unmapped code goes to the team manager | Business Requirements Program, section 5.15 | FEAT-DVH-04 | 11 Handle customer care and deviations | R-DEV-02, R-DEV-03, R-DEV-04, R-DEV-05, R-DEV-06 | TC-E1-062-04 |
| REQ-DVH-007 | A complaint is matched to the contact before it | Business Requirements Program, section 5.15 | FEAT-DVH-08 | 11 Handle customer care and deviations | None | TC-E1-062-05 |

## 19. Out of scope

- Showing proposals to the owner and raising the deviation at L1 on one segment (RWB-E2-029).
- Raising, routing and clearing a deviation (RWB-E2-015, S8).
- The full deviation flows (Epic 7).
