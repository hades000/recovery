# RWB-E2-030 Legal document agent in shadow on Epic 1 data [E3c]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-030 |
| Epic | E3, release 31 January 2027 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-09 Run the legal document agent in shadow |
| Requirement IDs | REQ-S4-002 |
| BRD section | Business Requirements Program, section 5.11 |
| L3 process | 8.2 Instruct and file |
| Decision | D7.2 |
| Priority | Should |
| Depends on | RWB-E1-058, RWB-E2-025, RWB-E1-061 |
| Status | Ready for build |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the legal document agent to assemble litigation packs and completeness lists in shadow on real Epic 1 cases, scored against the packs the legal officers built**, so that **the agent goes to Epic 5 with a known accuracy per pack item**.

## 2. Business rationale

A litigation pack that reaches the law firm with a missing or defective document is returned, and the filing waits. From Epic 5 the legal document agent assembles the pack and checks it against the defect list before the officer verifies it (R-LIT-16, R-LIT-17, CTL-19). This story runs the agent in shadow on 50 cases whose packs the officers have already built, scores agreement per checklist item, and records the decision to promote or keep it in shadow as a policy version. It serves REQ-S4-002: a pack assembled and checked against the document checklist, with missing documents named.

## 3. Preconditions

- RWB-E1-058 is done: platform, sample loader and evaluation harness.
- RWB-E2-025 is done: court filings, hearing notices, judgments, contracts and mortgage documents are classified and their fields extracted.
- RWB-E1-061 is done: the policy loader checks a promotion proposal against its evaluation.
- The document checklist per case type is loaded as reference data (RWB-E1-040).
- Approved policy "LEGAL_DOC" version "P1": mode SHADOW, timeout 60 seconds, allowed tools read_case, read_legal_actions, read_documents, read_document_fields, read_checklist; output schema "legal-pack-v1".
- Sample "LEGAL-S1" version 1: for 50 Epic 1 litigation cases, the officers' pack, one row per case and checklist item with expected status PRESENT, MISSING or DEFECT.

## 4. Flow

1. RW-COE: loads sample "LEGAL-S1" and starts the evaluation of "LEGAL_DOC" through POST /admin/agent-evaluations.
2. System: for each sample case, runs the agent in shadow: reads the case, the legal action, the documents with their fields and the checklist for the case type.
3. System: checks the answer: every checklist item has a status, every document ID belongs to the case, and every DEFECT has a reason.
4. System: stores the pack (document IDs per item) and the completeness list on the agent run; nothing is shown to a user and no document, pack or legal action changes.
5. System: scores agreement with the officers' pack per checklist item and stores it with sample size.
6. RW-COE: reads the scores and loads policy version "P2": mode L1 with conditions to promote, or mode SHADOW with a review date to keep shadow.
7. RW-RISK: approves the version; the decision and its date are recorded on the policy row.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent names a document that belongs to another case | Check SCHEMA_RULE fails; run GUARDRAIL_FAILED; scored as wrong for every item | None to a user | AC4 |
| X2 | A checklist item has no status in the answer | Check SCHEMA fails | None to a user | AC5 |
| X3 | The document interface is unavailable during a run | Run status TOOL_UNAVAILABLE, fallback true; the case is scored as not run and listed (R-UNI-33) | None to a user | AC6 |
| X4 | Fewer than 50 scored cases | A promotion to L1 is refused; keeping shadow is allowed | MSG-P10-001 | AC7 |
| X5 | Keep shadow without a review date | Load refused | MSG-P10-001 | AC8 |
| X6 | The loader approves their own decision | Refused with 409 | MSG-P7-002 | AC9 |
| X7 | A role without the right | Refused with 403 | MSG-P4-002 | TC-E2-030-10 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the platform and harness; reads S4 and P5 data through their interfaces; no S4 workflow is needed |
| Negotiable | Checklist items come from reference data; the minimum sample and conditions are policy values |
| Valuable | Gives the item accuracy that decides whether the agent assembles packs in Epic 5 |
| Estimable | One prompt, one output schema, one scorer, one proposal |
| Small | One developer and one litigation officer for review |
| Testable | Each criterion runs on fixture cases with known officer packs |

## 7. Acceptance criteria

```gherkin
Feature: Legal document agent in shadow on Epic 1 data [E3c]

  Background:
    Given policy "LEGAL_DOC" version "P1" with mode "SHADOW" and prompt "PR1"
    Given the checklist for case type "MORTGAGE_CIVIL" has 9 items including "LOAN_CONTRACT", "MORTGAGE_DEED" and "DEMAND_NOTICE_PROOF"

  Scenario: AC1 Shadow pack
    Given litigation case "RW-2026-000901" with 14 documents and an open legal action
    When the agent runs
    Then a pack listing document IDs for each of the 9 items and a completeness list with PRESENT, MISSING or DEFECT per item are stored on the agent run
    Then no document, legal action, task or case field changes
    Then no user-facing endpoint returns the pack

  Scenario: AC2 Scored
    Given 50 shadow packs for sample "LEGAL-S1" version 1
    When the evaluation runs
    Then the system stores agreement with the officers' packs per item with sample size 50
    Then for "DEMAND_NOTICE_PROOF" with 46 agreeing cases the agreement rate is 0.9200

  Scenario: AC3 Promotion proposal
    Given the score
    When RW-COE loads policy "LEGAL_DOC" version "P2" with mode "SHADOW", review date 2027-03-15 and the evaluation run ID, and RW-RISK approves it
    Then the system records the decision to keep shadow on version "P2" with the approver and the approval date
    Then the system accepts a proposal with mode "L1" only when every stated condition is met by the evaluation

  Scenario: AC4 A document from another case
    Given the model stub names document "D-7001" of case "RW-2026-000902" in the pack of case "RW-2026-000901"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED" and check "SCHEMA_RULE"

  Scenario: AC5 An item without a status
    Given the answer has no status for item "MORTGAGE_DEED"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED" and check "SCHEMA"

  Scenario: AC6 The document interface is down
    Given the P5 document interface is unavailable for case "RW-2026-000903"
    When the agent runs
    Then the run holds status "TOOL_UNAVAILABLE" and fallback true
    Then the evaluation lists the case as not run and scores 49 cases

  Scenario: AC7 Too few cases to promote
    Given the evaluation scored 49 cases
    When RW-COE loads a proposal with mode "L1"
    Then the system refuses the load with 422 and MSG-P10-001 naming check "sample size at least 50"

  Scenario: AC8 Keep shadow without a review date
    When RW-COE loads version "P2" with mode "SHADOW" and no review date
    Then the system refuses the load with 422 and MSG-P10-001 naming check "review date present"

  Scenario: AC9 The loader cannot approve
    Given user "coe.user01" loaded version "P2"
    When user "coe.user01" approves it
    Then the system refuses the approval with 409 and MSG-P7-002
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | In SHADOW mode the pack and completeness list are stored only; no pack, document or legal action changes | agent_policy.autonomy_mode (New) |
| BR2 | Checklist items come from the document checklist for the case type | Reference table document checklist; REQ-DCM-011 |
| BR3 | Every item has a status PRESENT, MISSING or DEFECT, and every DEFECT has a reason | R-LIT-16, R-LIT-17; CTL-19 |
| BR4 | A pack may name only documents of the same case | CTL-19; CTL-11 |
| BR5 | Agreement per item = cases where the agent status equals the officer status / scored cases, 4 decimals | agent_evaluation.agreement_rate (New) |
| BR6 | A promotion to L1 needs at least 50 scored cases (assumed); keeping shadow needs a review date | agent_policy.review_date (New) |
| BR7 | The loader and the approver are different people | Separation of duty, center of excellence analyst and risk and model risk officer |

## 9. State transitions

None. This story does not change a case status and does not move a case into PACK_ASSEMBLY. It writes agent runs, one evaluation run (RUNNING to DONE) and one policy version (LOADED to APPROVED).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT | Reads case, legal actions, documents, fields and checklist (Case record R, Litigation R, Documents R, Reference data R) |
| RW-COE | Loads the sample, runs the evaluation, loads the decision version (Rules and parameters CRUD) |
| RW-RISK | Approves the decision version (Rules and parameters A) |
| RW-LITOFF | Supplies the officers' packs for the sample; reads scores through the export |
| RW-HEADLIT | Reads scores through the export |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-LEG-001 | legal_action | id | Read |
| DF-LEG-004 | legal_action | action_type | Read |
| DF-LEG-014 | legal_action | status | Read |
| DF-DOC-001 | document | id | Read |
| DF-DOC-002 | document | case_id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-010 | document | write_once | Read |
| DF-DOC-014 | document_field | field_name | Read |
| DF-DOC-015 | document_field | field_value | Read (masked) |
| DF-AGT-036 | agent_run | id | Write |
| DF-AGT-037 | agent_run | agent_code | Write |
| DF-AGT-038 | agent_run | agent_version | Write |
| DF-AGT-041 | agent_run | case_id | Write |
| DF-AGT-042 | agent_run | subject_id | Write |
| DF-AGT-043 | agent_run | autonomy_mode | Write |
| DF-AGT-044 | agent_run | trigger_event | Write |
| DF-AGT-046 | agent_run | status | Write |
| DF-AGT-047 | agent_run | fallback | Write |
| DF-AGT-048 | agent_run | guardrail_result | Write |
| DF-AGT-049 | agent_run | output | Write |
| DF-AGT-051 | agent_run | latency_ms | Write |
| DF-AGT-052 | agent_run | tokens_in | Write |
| DF-AGT-053 | agent_run | tokens_out | Write |
| DF-AGT-054 | agent_run | cost_thb | Write |
| DF-AGT-056 | agent_run | run_at | Write |
| DF-AGT-057 | agent_run | evaluation_run_id | Write |
| DF-AGT-063 | agent_sample | sample_code | Read |
| DF-AGT-064 | agent_sample | sample_version | Read |
| DF-AGT-066 | agent_sample | subject_id | Read |
| DF-AGT-067 | agent_sample | label_key | Read |
| DF-AGT-068 | agent_sample | expected_value | Read |
| DF-AGT-087 | agent_evaluation | evaluation_run_id | Write |
| DF-AGT-089 | agent_evaluation | label_key | Write |
| DF-AGT-090 | agent_evaluation | sample_size | Write |
| DF-AGT-094 | agent_evaluation | agreement_rate | Write |
| DF-AGT-003 | agent_policy | policy_version | Write |
| DF-AGT-008 | agent_policy | autonomy_mode | Write |
| DF-AGT-016 | agent_policy | review_date | Write |
| DF-AGT-017 | agent_policy | evaluation_run_id | Write |
| DF-AGT-018 | agent_policy | promotion_conditions | Write |
| DF-AGT-021 | agent_policy | status | Write |
| DF-AGT-025 | agent_policy | approved_by | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/agent-samples**, **POST /api/recovery/v1/admin/agent-evaluations**, **GET /api/recovery/v1/admin/agent-evaluations** (new, RWB-E1-058): agent "LEGAL_DOC", sample "LEGAL-S1"; Rules and parameters C and R; errors 401, 403, 409 (MSG-P10-003), 422 (MSG-P10-001, MSG-P10-002), 503.

**POST /api/recovery/v1/admin/agent-configs** and **POST /api/recovery/v1/admin/agent-configs/{versionId}/approve** (new): the promote or keep version; Rules and parameters C and A; errors 409 (MSG-P7-002, MSG-GEN-004), 422 (MSG-P10-001).

**Output schema "legal-pack-v1":** items (array of {itemCode from the checklist, status PRESENT, MISSING or DEFECT, documentIds, defectReason}), confidence.

**Interfaces called:** S4 LegalActionQueryService.listByCase(caseId); P5 DocumentQueryService.listByCase, getFields and getChecklist(caseType); all as SY-AGENT. A call that fails returns TOOL_UNAVAILABLE (R-UNI-33).

**Event published:** EV-28 AgentRunCompleted.

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/legal/`, Java package `recovery.agent.legal`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalPackInputAssembler | Service | Builds masked inputs from the case, legal actions, documents, fields and checklist |
| LegalPackRuleChecks | Service | SCHEMA_RULE checks: same-case documents, defect reasons, all items present |
| LegalPackScorer | Service | Agreement per checklist item for the harness |
| legal-pack-v1.json, prompt LEGAL_DOC PR1 | Rule table | Output schema and prompt, loaded through the configuration endpoint |
| PromotionProposalValidator | Service | Extended with the review date rule for SHADOW decisions |

**Database:** no new table. Writes agent_run, agent_evaluation_run, agent_evaluation and agent_policy; reads agent_sample.

**Configuration and reference data:** policy LEGAL_DOC P1 (minimum sample 50) loaded by RW-COE and approved by RW-RISK; checklist reference data maintained by RW-REFADM; sample LEGAL-S1 built from the officers' packs.

**Build steps**
1. Write the output schema and the prompt; load them in DEV.
2. Build LegalPackInputAssembler over the S4 and P5 interfaces (AC1).
3. Build LegalPackRuleChecks (AC4, AC5) and the TOOL_UNAVAILABLE path (AC6).
4. Build LegalPackScorer on a 10-case fixture with known agreement (AC2).
5. Extend PromotionProposalValidator for the sample minimum and the review date (AC3, AC7, AC8, AC9).

**Feature flag:** `rwb.agent.legal-shadow`. Off: evaluations of LEGAL_DOC are refused with 422.

**Done when:** the tests in section 16 pass and the 50-case evaluation is approved as promote or keep.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-001 | The decision version fails a check | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. |
| MSG-P10-002 | Evaluation on an empty sample | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P7-002 | Loader approves own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No user screen shows a pack in this story. SCR-46 Agent monitor shows LEGAL_DOC in state Shadow with its runs, fallbacks and the evaluation score. Scores are exported through GET /admin/agent-evaluations.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-030-01 | AC1, BR1, BR2 | System | Case RW-2026-000901, 14 documents, 9 checklist items |
| TC-E2-030-02 | AC2, BR5 | System | Sample LEGAL-S1 version 1, 50 cases; 46 agree on DEMAND_NOTICE_PROOF |
| TC-E2-030-03 | AC3, BR6 | System | Version P2 SHADOW with review date 2027-03-15 |
| TC-E2-030-04 | AC4, BR4 | System | Document D-7001 of another case in the pack |
| TC-E2-030-05 | AC5, BR3 | System | No status for MORTGAGE_DEED |
| TC-E2-030-06 | AC6 | System | P5 interface down for case RW-2026-000903 |
| TC-E2-030-07 | AC7, BR6 | System | 49 scored cases, proposal L1 |
| TC-E2-030-08 | AC8, BR6 | System | SHADOW version with no review date |
| TC-E2-030-09 | AC9, BR7 | System | Loader coe.user01 approves P2 |
| TC-E2-030-10 | Access | Access | RW-LITOFF calls POST /admin/agent-evaluations; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: checklist items, minimum sample and review date are data.
- No personal data in logs, tests or prompts; field values are masked before the model call.
- No read of another module's tables; legal actions and documents come through the S4 and P5 interfaces.
- The agent never changes a write-once legal document or a pack.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested | Business Requirements Program, section 5.11 | FEAT-AGT-09 | 8.2 Instruct and file | R-LIT-16, R-LIT-17, R-UNI-33 | TC-E2-030-01, TC-E2-030-02, TC-E2-030-03, TC-E2-030-04, TC-E2-030-05, TC-E2-030-06, TC-E2-030-07, TC-E2-030-08, TC-E2-030-09, TC-E2-030-10 |

## 19. Out of scope

- Pack assembly, retrieval requests and officer verification in the litigation flow (Epic 5, S4).
- Showing packs to officers at L1 (Epic 5).
- Extraction for the stage 2 and 3 document types (RWB-E2-025).
