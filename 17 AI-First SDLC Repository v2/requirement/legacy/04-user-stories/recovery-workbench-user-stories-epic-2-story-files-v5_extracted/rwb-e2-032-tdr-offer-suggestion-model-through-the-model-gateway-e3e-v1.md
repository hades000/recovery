<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 032 TDR offer suggestion model through the model gateway E3e v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 032 TDR offer suggestion model through the model gateway E3e v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-032 TDR offer-suggestion model through the model gateway [E3e]

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-032 |
| Epic | E2, release 31 December 2026 |
| Module | P10 Agent runtime |
| Feature | FEAT-AGT-10 Expose the TDR offer-suggestion model through the gateway |
| Requirement IDs | REQ-CHO-006, REQ-DRI-001 |
| BRD section | Business Requirements Epic 2, section 3.10; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D5 |
| Priority | Could |
| Depends on | RWB-E1-058, RWB-E2-004, RWB-E1-027 |
| Status | Ready for build |

## 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the TDR team's offer-suggestion model called through the model gateway so the treatment record carries its suggestion when the model exists**, so that **one gateway serves every model the Workbench uses and every suggestion is recorded with its model version**.

## 2. Business rationale

The restructuring officer builds each restructure offer by hand from the balance, the arrears and the payment history. If the TDR team's offer-suggestion model is in service, its suggestion appears on the treatment record and is recorded with the model version (REQ-DRI-001), so the treatment record holds what was suggested next to what was offered (REQ-CHO-006). If the model is not in service, the gateway returns no suggestion and the officer works as today. The officer decides the offer in every case.

## 3. Preconditions

- RWB-E1-058 is done: ModelGatewayClient, agent_policy and agent_run exist.
- RWB-E2-004 is done: the treatment record exists and the P3 treatment service calls P10 when a restructure treatment is opened.
- RWB-E1-027 is done: the P7 DecisionLogWriter is available.
- A policy row "TDR_OFFER" exists. Until the TDR team deploys the model, it has mode OFF and review date 2027-02-28 (assumed; DL33). When deployed, a new version with mode L1, the model code and version, the output schema "tdr-offer-v1" and timeout 60 seconds is loaded by RW-COE and approved by RW-RISK.

## 4. Flow

1. Restructuring officer: opens a restructure treatment on case "RW-2026-001001" on SCR-14 Treatment record.
2. P3 treatment service: calls ModelSuggestionClient.suggestOffer with the case ID and treatment ID.
3. System: reads the TDR_OFFER policy in force; if the mode is OFF, returns no suggestion and makes no call.
4. System: reads the account balance, arrears and the last 12 months of payments through the P3 interface and masks personal fields.
5. System: calls the model through ModelGatewayClient with the policy timeout, and checks the answer against "tdr-offer-v1".
6. System: writes one decision log entry (decision D5, model version, suggestion, final call SUGGESTION_RECORDED) and one agent run row.
7. System: returns the suggestion and the decision log entry ID to the treatment service.
8. Restructuring officer: sees the suggestion on SCR-14 with the model code and version, and builds the offer.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The model is not in service (mode OFF) | No call, no decision log entry; the treatment shows the message | MSG-P10-007 | AC2 |
| X2 | The model does not answer within 60 seconds | Run TIMED_OUT; no suggestion; no decision log entry; treatment continues (R-UNI-32) | MSG-P10-007 | AC4 |
| X3 | The answer fails the output schema | Run GUARDRAIL_FAILED; no suggestion | MSG-P10-007 | AC5 |
| X4 | The decision log write fails | No suggestion returned; run kept without a decision link; incident raised (R-UNI-39) | MSG-P7-003 | AC6 |
| X5 | The same treatment asks again | The first suggestion is returned; no second call (R-UNI-40) | None to a user | AC7 |
| X6 | The treatment type is not RESTRUCTURE | No call; no suggestion | None to a user | AC8 |
| X7 | A role without the right reads the agent runs | Refused with 403 | MSG-P4-002 | TC-E2-032-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the gateway (RWB-E1-058) and is called by the treatment service (RWB-E2-004); it ships with mode OFF if the model is not built |
| Negotiable | The model, its version, the inputs and the review date are policy values |
| Valuable | Puts a recorded suggestion on the treatment record without a second integration path |
| Estimable | One interface, one schema, one decision log mapping |
| Small | Under one week |
| Testable | Each criterion runs against a stub of the TDR model |

## 7. Acceptance criteria

```gherkin
Feature: TDR offer-suggestion model through the model gateway [E3e]

  Background:
    Given restructure treatment "T-1001" is open on case "RW-2026-001001"
    Given the account has principal outstanding 1,250,000.00 baht and 120 days past due

  Scenario: AC1 Exposed
    Given the model deployed by the TDR team with policy "TDR_OFFER" version "P2", mode "L1" and model version "TDR-OFFER-1.0"
    When the gateway calls it
    Then the suggestion returns with 84 installments of 18,900.00 baht and model version "TDR-OFFER-1.0"
    Then one agent run row and one decision log entry with decision "D5", model version "TDR-OFFER-1.0" and final call "SUGGESTION_RECORDED" are written

  Scenario: AC2 Not available
    Given the model not yet built and policy "TDR_OFFER" version "P1" with mode "OFF" and review date 2027-02-28
    When the treatment service asks for a suggestion
    Then the gateway stub returns no suggestion and makes no model call
    Then SCR-14 shows MSG-P10-007 and no decision log entry is written
    Then GET /admin/agent-configs shows version "P1" with review date 2027-02-28

  Scenario: AC3 Logged
    Given a suggestion on treatment "T-1001"
    When the record is read
    Then the decision log entry linked to the suggestion holds model version "TDR-OFFER-1.0", the inputs reference and the suggested terms
    Then SCR-14 shows "Suggested by TDR_OFFER, version TDR-OFFER-1.0"

  Scenario: AC4 The model does not answer
    Given the TDR model stub does not answer for 61 seconds
    When the treatment service asks for a suggestion
    Then the agent run holds status "TIMED_OUT" and fallback true
    Then no suggestion and no decision log entry exist and SCR-14 shows MSG-P10-007

  Scenario: AC5 An answer that fails the schema
    Given the model returns installments -12
    When the guardrail runs
    Then the agent run holds status "GUARDRAIL_FAILED" with check "SCHEMA" and no suggestion is returned

  Scenario: AC6 The decision cannot be recorded
    Given the decision log writer fails
    When the model answers
    Then the system returns no suggestion and the treatment service receives DecisionNotRecordedException with MSG-P7-003
    Then the agent run has no decision log entry ID

  Scenario: AC7 The same treatment asks twice
    Given a suggestion was recorded for treatment "T-1001"
    When the treatment service asks again for "T-1001"
    Then the first suggestion and its decision log entry ID return and no second model call is made

  Scenario: AC8 Not a restructure
    Given treatment "T-1002" has type "SETTLEMENT"
    When the treatment service asks for a suggestion
    Then the system makes no model call and no suggestion returns
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The TDR model is reached only through ModelGatewayClient on the private endpoint | DL33; integration INT-23 |
| BR2 | Mode OFF returns no suggestion and makes no call; the review date is held on the policy row | agent_policy.autonomy_mode, review_date (New) |
| BR3 | A suggestion is returned only after its decision log entry is written | Principle 5; R-UNI-39; CTL-06 |
| BR4 | A timeout or a failed check gives no suggestion and the treatment continues | R-UNI-32 |
| BR5 | One suggestion per treatment; the key is "TDR_OFFER:<treatmentId>" | R-UNI-40 |
| BR6 | The model is called only for treatment type RESTRUCTURE | treatment.treatment_type |
| BR7 | The suggestion is advice; the officer builds and submits the offer | Agent catalog, settlement and restructure agent; R-RES-09, R-RES-10 |

## 9. State transitions

None. This story does not change a case status or a treatment status. It writes an agent run and, when a suggestion is returned, one decision log entry.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT | Reads the suggestion on SCR-14 (Treatment and offer R) |
| RW-CASEOWN | Reads the suggestion on SCR-14 (Treatment and offer R) |
| SY-CASEWF | Calls ModelSuggestionClient from the treatment service |
| SY-AGENT | Reads the account and payments (Case record R, Treatment and offer R) |
| SY-DECLOG | Writes the entry |
| RW-COE, RW-RISK | Load and approve the TDR_OFFER policy (Rules and parameters C and A) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-ACC-009 | v_ace_account | principal_outstanding | Read (Section B, RWB-ACE-001) |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-025 | v_ace_account | interest_rate | Read |
| DF-ACE-045 | v_ace_payment | payment_date | Read |
| DF-ACE-046 | v_ace_payment | payment_amount | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (through the P7 DecisionLogWriter) |
| DF-AGT-008 | agent_policy | autonomy_mode | Read |
| DF-AGT-004 | agent_policy | model_code | Read |
| DF-AGT-005 | agent_policy | model_version | Read |
| DF-AGT-006 | agent_policy | output_schema_ref | Read |
| DF-AGT-012 | agent_policy | timeout_seconds | Read |
| DF-AGT-016 | agent_policy | review_date | Read |
| DF-AGT-036 | agent_run | id | Write |
| DF-AGT-037 | agent_run | agent_code | Write |
| DF-AGT-040 | agent_run | model_version | Write |
| DF-AGT-041 | agent_run | case_id | Write |
| DF-AGT-042 | agent_run | subject_id | Write |
| DF-AGT-043 | agent_run | autonomy_mode | Write |
| DF-AGT-045 | agent_run | idempotency_key | Write |
| DF-AGT-046 | agent_run | status | Write |
| DF-AGT-047 | agent_run | fallback | Write |
| DF-AGT-048 | agent_run | guardrail_result | Write |
| DF-AGT-049 | agent_run | output | Write |
| DF-AGT-051 | agent_run | latency_ms | Write |
| DF-AGT-056 | agent_run | run_at | Write |
| DF-AGT-058 | agent_run | decision_log_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Published interface**

```java
package recovery.agent.api;

public interface ModelSuggestionClient {
    Optional<OfferSuggestion> suggestOffer(UUID caseId, UUID treatmentId) throws DecisionNotRecordedException;
}

public record OfferSuggestion(UUID agentRunId, UUID decisionLogEntryId, String modelCode, String modelVersion,
                              int installments, BigDecimal monthlyAmountThb, BigDecimal interestRate,
                              BigDecimal confidence) {}
```

**Decision log mapping:** case_id; decision_code "D5"; model_version; agent_version null; inputs_ref = masked inputs snapshot; recommendation = the suggestion; final_call "SUGGESTION_RECORDED"; actions = {"treatmentId", "agentRunId"}.

**External call:** INT-23 through ModelGatewayClient; request: model code, masked inputs, output schema "tdr-offer-v1"; per request.

**GET /api/recovery/v1/admin/agent-runs** (api.yaml): runs of TDR_OFFER with outcome and fallback; Platform administration R.

**GET /api/recovery/v1/admin/agent-configs** (new, RWB-E1-058): shows the TDR_OFFER version, mode and review date; Rules and parameters R.

**Events:** EV-28 AgentRunCompleted published; no event consumed.

**Idempotency:** "TDR_OFFER:<treatmentId>".

## 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/tdr/`, Java package `recovery.agent.tdr`; interface in `recovery.agent.api`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ModelSuggestionClient | Published interface | Called by the P3 treatment service |
| TdrSuggestionService | Service | Mode check, inputs, gateway call, checks, decision log write, run row |
| TdrInputAssembler | Service | Account, arrears and 12 months of payments through the P3 interface, masked |
| tdr-offer-v1.json | Rule table | Output schema: installments 1 to 360, monthly amount above 0, interest rate 0 to 30, confidence |
| TreatmentSuggestionPanel | React component | On SCR-14: the suggestion with model code and version, or MSG-P10-007 |

**Database:** no new table; writes agent_run.

**Configuration and reference data:** TDR_OFFER policy P1 (mode OFF, review date 2027-02-28) loaded by RW-COE and approved by RW-RISK; P2 when the TDR team deploys the model.

**Build steps**
1. Write the output schema and the P1 policy file; load them in DEV.
2. Build TdrSuggestionService with the mode OFF path (AC2, AC8).
3. Add the gateway call, the schema check and the timeout path against a stub (AC1, AC4, AC5).
4. Add the decision log write before return and the idempotent repeat (AC3, AC6, AC7).
5. Build TreatmentSuggestionPanel for SCR-14.

**Feature flag:** `rwb.agent.tdr-suggestion`. Off: suggestOffer returns empty with no call.

**Done when:** the tests in section 16 pass with mode OFF in SIT; the AC1 test passes against the stub until the TDR model is deployed.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-007 | No suggestion: model not in service, timeout or failed check | No offer suggestion is available for this treatment. The TDR model is not in service. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-14 Treatment record (states draft, submitted, approved, booked, broken) gains a suggestion area in the draft state: suggestion shown (terms, model code and version) or not available (MSG-P10-007). The officer edits the offer fields as before; the suggestion is not copied into them.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-032-01 | AC1, BR1, BR3 | System | Treatment T-1001, stub answer 84 installments of 18,900.00 baht |
| TC-E2-032-02 | AC2, BR2 | System | Policy TDR_OFFER P1 mode OFF, review date 2027-02-28 |
| TC-E2-032-03 | AC3 | System | Suggestion recorded on T-1001 |
| TC-E2-032-04 | AC4, BR4 | System | Stub silent for 61 seconds |
| TC-E2-032-05 | AC5, BR4 | System | Answer with installments -12 |
| TC-E2-032-06 | AC6, BR3 | System | Decision log writer fails |
| TC-E2-032-07 | AC7, BR5 | System | Second request for T-1001 |
| TC-E2-032-08 | AC8, BR6 | System | Treatment T-1002 of type SETTLEMENT |
| TC-E2-032-09 | Access | Access | RW-RESTRUCT calls GET /admin/agent-runs; refused with MSG-P4-002 |
| TC-E2-032-10 | Principle 5 | Resilience | Decision log write forced to fail after the model answers; no suggestion; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: model code, version, schema limits and review date are data.
- No personal data in logs, tests or the model request; account numbers are masked.
- No read of another module's tables; the account and treatment come through the P3 interface.
- The suggestion is never written into the offer fields or the treatment status.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record holds every offer's type, terms, approval and outcome | Business Requirements Program, section 5.3 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-32, R-UNI-40 | TC-E2-032-02, TC-E2-032-04, TC-E2-032-05, TC-E2-032-07, TC-E2-032-08 |
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-032-01, TC-E2-032-03, TC-E2-032-06, TC-E2-032-09, TC-E2-032-10 |

## 19. Out of scope

- Building or training the TDR model (TDR team, outside the Workbench).
- The settlement and restructure agent proposing plan terms (shadow from Epic 2 and live from Epic 3, per the agent catalog).
- Affordability and plan calculation (ACE restructure calculator, R-RES-06).
