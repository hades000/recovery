# RWB-ITG-E2014-ITG Approval screen for D7.1 demand and recall notices

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-014 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E2014-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2014-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P6-E1052-APP, RWB-P7-E2014-APP, RWB-P6-E2014-APP, RWB-P4-E2014-APP, RWB-P3-E2014-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-APD-002, REQ-APD-006) |
| Status | Draft (realignment v1) |

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that takes a generated D7.1 demand notice through the composite decision screen, an approval, a change of variant and a rejection, and through the refusals that protect the decision**, so that **the first decision in the Workbench with a person approving is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production screen, endpoint, table, workflow or schedule, it serves no production operation, it owns no table and it starts no workflow. The real behaviour is owned by the I stories RWB-P6-E1052-APP (notice generation from the current Approved template and its version), RWB-P7-E2014-APP (the D7.1 approval, the decision record and the approve and refuse checks), RWB-P6-E2014-APP (notice approve, regenerate and hold), RWB-P4-E2014-APP (authorise, role and scope) and RWB-P3-E2014-APP (case facts, case state and the case-owner task), and those stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-014 journey crosses more than one service: rwb-comms holds the notice, its template and its version, rwb-decision holds the approval and the decision record, rwb-access answers the authorisation check, and rwb-case holds the case, the case facts with their business date, the case state and the queue that receives a rejected notice. A demand fee notice sent with a wrong amount or a wrong address can void the notice period and delay litigation, and today notices are checked on paper with no record of who approved what. Until the services are exercised together through the gateway, the program cannot show that the notice seen by the approver is the notice that is approved, that the inputs behind it are inside their age limits, and that only an approved version reaches the 16:00 dispatch run.

The harness gives one repeatable run per business date that proves the composite decision route composes the item one hop at a time inside the 2 s budget, that the decision record is written before the notice changes state, that a change of variant and a rejection both route through the notice contract, and that a failure in one service leaves the notice and the approval unchanged. It meets REQ-APD-002 and REQ-APD-006 at the integration level and leaves every business rule, every screen behaviour and every message where the owning stories put them. The measure it supports is unchanged: notices sent with an approval entry, target 100 percent.

### 3. Preconditions

- The five I stories are published and deployed in the SIT environment: RWB-P6-E1052-APP (notice generation from the current Approved template, with its version and rule), RWB-P7-E2014-APP (D7.1 approval routing, approve and refuse, the decision record), RWB-P6-E2014-APP (approve, regenerate and hold on the notice), RWB-P4-E2014-APP (authorise for role RW-LITOFF and the Litigation rights) and RWB-P3-E2014-APP (case facts with business dates, case state and the case-owner task).
- gateway-bff is deployed with the composite route of DP-19 available for the decision screen. The gateway-bff composite decision-screen route path and its merge order: Not specified in the source documents (GAP-0398; ASM-0573).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before the I stories land.
- Templates DEMAND-MTG (TH version 2), the variant DEMAND-MTG-B and RECALL-MTG are Approved, and the input age parameters `rwb.decision.input-age-days.TOTAL_BALANCE` = 1 day and `rwb.decision.input-age-days.POSTAL_ADDRESS` = 30 days, and the reference data LOV-OVERRIDE-REASON with the values TEMPLATE_VARIANT and WRONG_PARTY, are loaded by the owning stories and read by the harness through their contracts (DP-06, DP-07).
- The harness environment, its synthetic seeding, its evidence format and its retention: Not specified in the source documents (GAP-0398; ASM-0573).

### 4. Flow

1. Harness: seeds case RW-2026-000123 with product group MORTGAGE and the ACE-sourced case facts of business date 13 December 2026, the demand notice N-0201 generated at 08:10 on 14 December 2026 from template DEMAND-MTG TH version 2 under rule R-LIT-03 version LIT-2026.12 by preparer U-9211, and the approval A-0201 in state WAITING for role RW-LITOFF, all through the owning contracts or the §12.8 fakes.
2. Harness: opens the composite decision item for A-0201 through gateway-bff as approver U-9212 at 10:00 on 14 December 2026.
3. Harness: asserts the item carries the notice content of N-0201, the case facts with the business date of each input, the postal address masked per the masking rules, rule R-LIT-03 and its version, template DEMAND-MTG and version 2, preparer U-9211, and state Ready.
4. Harness: approves, then asserts the decision record with the inputs reference, rule version, template version, approver and time, the notice in state Approved, the case out of Waiting approval, the eligibility of the notice for the 16:00 dispatch run, and MSG-P7-004.
5. Harness: repeats the item on a second seeded approval and changes the variant to DEMAND-MTG-B with the coded reason TEMPLATE_VARIANT, then asserts the new notice version is the one approved, final call APPROVED_CHANGED, and that only the approved version is eligible for the 16:00 run.
6. Harness: repeats the item on a third seeded approval and rejects it with a reason, then asserts the notice in state Held with reason REFUSED_BY_APPROVER, one task with the reason in the case owner's queue, and final call REFUSED.
7. Harness: forces each failure of §5 through the fakes, asserts the status, the message and that the notice and the approval did not move, then returns the fake to its healthy answer and repeats the answer.
8. Harness: asserts the 16:00 eligibility from the notice state and the approval only; it does not call rwb-integration and does not prove delivery.
9. Harness: writes one run report per business date, keyed by story and business date; the report format and retention are Not specified in the source documents (GAP-0398; ASM-0573).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | The approver prepared the notice | A direct approve or refuse by preparer U-9211 returns 409 and the approval stays WAITING | MSG-P7-002 | TC-E2-014-04-ITG |
| X2 | An input is past its age limit | The item is state Stale input; a direct approve returns 409 and the notice stays Generated | MSG-P7-006 | TC-E2-014-05-ITG |
| X3 | The template was withdrawn after generation | 409; the notice is held under R-LIT-04 and nothing is approved | MSG-P6-003 | TC-E2-014-06-ITG |
| X4 | Reject without a reason | 422 for field reason; the notice stays Generated and no task is raised | MSG-GEN-001 | TC-E2-014-07-ITG |
| X5 | A change of variant without a coded reason | 422; no new notice version exists and nothing is approved | MSG-P7-005 | TC-E2-014-08-ITG |
| X6 | Another approver decided the item first | 409; the item reloads in state Decided showing approver U-9214 | MSG-GEN-004 | TC-E2-014-09-ITG |
| X7 | The user holds no Litigation right for the decision | 403 on a direct call; the composite route hides the approve and reject actions | MSG-P4-002 | TC-E2-014-11-ITG |
| X8 | The decision record cannot be written | 503; the notice stays Generated, the approval stays WAITING and the retry after the fake recovers decides once | MSG-P7-003 | TC-E2-014-12-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the five I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the synthetic seeding and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The first Workbench decision with a person approving is evidenced across services rather than per service |
| Estimable | One harness project, one journey specification, one fake pack and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Approval screen for D7.1 demand and recall notices - wave 2 integration harness

  Background:
    Given the environment is SIT
    Given demand notice "N-0201" for case "RW-2026-000123" was generated at 08:10 on 14 December 2026 from template "DEMAND-MTG" "TH" version 2 under rule "R-LIT-03" version "LIT-2026.12", prepared by "U-9211"
    Given its approval "A-0201" is WAITING for role RW-LITOFF
    Given the case facts carry the total balance from the ACE account data of business date 13 December 2026 and the postal address of the addressee
    Given the input age limits are 1 day for "TOTAL_BALANCE" and 30 days for "POSTAL_ADDRESS"

  Scenario: AC1 The composite decision item through gateway-bff (new, D-RCV-60)
    Given the harness calls the composite decision screen route at "Not specified in the source documents (GAP-0398; ASM-0573)" for approval "A-0201"
    When gateway-bff composes the answer from rwb-decision, rwb-comms, rwb-case and rwb-access
    Then the route returns the notice content of "N-0201", the case facts with each input's business date, the postal address masked, rule "R-LIT-03" version "LIT-2026.12", template "DEMAND-MTG" version 2, preparer "U-9211" and state "Ready"
    And every call in the composition is one hop with the 2 s budget
    And no service reads another service's schema
    And the run report holds one trace spanning the gateway and each owning service

  Scenario: AC2 Approve, the record first and the notice in the 16:00 run (new, D-RCV-60)
    Given approver "U-9212" holds RW-LITOFF and did not prepare "N-0201"
    When "U-9212" approves "A-0201" at 10:00 on 14 December 2026
    Then one decision record exists with the inputs reference and each input's business date, rule "R-LIT-03" version "LIT-2026.12", template "DEMAND-MTG" version 2, approver "U-9212" and decided at 10:00
    And notice "N-0201" is in state "Approved"
    And case "RW-2026-000123" leaves "Waiting approval"
    And the notice is eligible for the 16:00 dispatch run and the run report shows it
    And the answer carries MSG-P7-004

  Scenario: AC3 A change of variant and a rejection both route through the notice contract (new, D-RCV-60)
    Given "U-9212" opens "A-0201" at 10:00 on 14 December 2026
    When "U-9212" picks template variant "DEMAND-MTG-B" with coded reason "TEMPLATE_VARIANT" and approves
    Then rwb-comms returns a new notice version from "DEMAND-MTG-B" and that version is the one approved
    And one decision record exists with final call "APPROVED_CHANGED", the proposed template "DEMAND-MTG", the chosen "DEMAND-MTG-B" and the reason code "TEMPLATE_VARIANT"
    And only the approved version is eligible for the 16:00 dispatch run
    When "U-9212" rejects "A-0201" with reason "Addressee is a guarantor; a guarantor notice is needed"
    Then the notice is held with reason "REFUSED_BY_APPROVER" and one task with the reason is in the case owner's queue
    And the decision record shows final call "REFUSED" with the reason

  Scenario: AC4 Failure isolation and the refusals (new, D-RCV-60)
    Given the total balance on a second notice comes from business date 11 December 2026, above the 1 day limit
    When the harness approves that stale-input approval through the approval contract
    Then the response is 409 with MSG-P7-006 and the notice stays "Generated"
    When template "DEMAND-MTG" version 2 is withdrawn at 09:30 on 14 December 2026 and the item is opened
    Then the response is 409 with MSG-P6-003 and the notice is held under R-LIT-04
    When preparer "U-9211" calls approve directly
    Then the response is 409 with MSG-P7-002 and the approval stays "WAITING"
    When "U-9212" rejects with an empty reason
    Then the response is 422 with MSG-GEN-001 for field "reason" and no task is raised
    When "U-9212" approves with variant "DEMAND-MTG-B" and no reason code
    Then the response is 422 with MSG-P7-005 and no new notice version exists
    When another approver "U-9214" approved "A-0201" at 10:01 and "U-9212" approves at 10:02 from a screen loaded at 10:00
    Then the response is 409 with MSG-GEN-004 and the item reloads in state "Decided" showing "U-9214"
    When the decision log write is forced to fail
    Then the response is 503 with MSG-P7-003 and the notice stays "Generated"
    When every fake returns its healthy answer and the same approve is repeated
    Then one decision record exists and the notice is in state "Approved"
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the I stories. The dispatch itself is out of scope: the harness asserts eligibility for the 16:00 window and never calls rwb-integration.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Demand and recall notices are approved through approval routing before dispatch; only an Approved notice is dispatched | REQ-APD-006; CTL-14 |
| BR2 | The approver sees the notice, the inputs with their age, the rule and the template version on one screen | REQ-APD-002 |
| BR3 | The person who prepared the notice may not approve or reject it | CTL-05; Admin and access model, section 6.2 |
| BR4 | An input past its age limit blocks the decision until refreshed | VR-P7-023-3; MSG-P7-006; parameters rwb.decision.input-age-days.* |
| BR5 | A notice is generated only from the current Approved template; a withdrawn template holds the notice | R-LIT-03; R-LIT-04 |
| BR6 | A change of template variant needs a coded reason and uses only an Approved variant of the same notice type and product | R-UNI-14; CTL-07; LOV-OVERRIDE-REASON |
| BR7 | A rejection needs a reason and returns the case to the case owner's queue | FEAT-APD-04 |
| BR8 | A decision that cannot be written to the decision log does not take effect | Principle 5; R-UNI-39 |

The harness asserts these rules against the owning services; it re-implements none of them. No BR row is changed by this story.

### 9. State transitions

The states below are the states the harness observes. The harness changes no case status, no approval state and no notice state itself; every transition is caused by a call to the owning service.

| From | Event | Condition | To |
|---|---|---|---|
| Case In progress | Recommendation routed for approval | Notice generated under R-LIT-03 | Waiting approval |
| Case Waiting approval | Approver accepts, or changes and accepts | Not the preparer; inputs inside their limits; template current; decision record written | In progress |
| Case Waiting approval | Approver rejects | Reason given; decision record written | In progress, with a task in the case owner's queue |
| Approval WAITING | Approve, change and approve, or refuse | The checks of §5 pass | DECIDED, with final call APPROVED, APPROVED_CHANGED or REFUSED |
| Notice Generated | Notice approved | Decision record written | Approved |
| Notice Generated | Notice refused | Decision record written | Held, reason REFUSED_BY_APPROVER |
| Notice Generated | Template withdrawn | R-LIT-04 | Held |

A refused or failed call leaves the approval in WAITING and the notice where it was.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF Litigation officer | The role the harness drives: approves, changes the variant or rejects D7.1 notices they did not prepare (Litigation A) |
| RW-LEGAL Legal counsel | Also holds Litigation A for D7.1; used by the preparer case, where the preparer holds it and still may not decide |
| RW-HEADLIT Head of Litigation | Receives escalated D7.1 notices and decides them (Litigation A) |
| RW-CASEOWN Case owner | Receives the task of a rejected notice; may not approve (Litigation R) |
| SY-CASEWF | The case workflow that causes the router to be called when the notice is generated |

No approval level from the delegation of authority applies in this story: a D7.1 notice carries no amount limit, and delegation item 2.1.3 (delay of legal action) does not apply to issuing a notice. Authorisation is answered by rwb-access through POST /authorise.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Read through the rwb-comms contract |
| DF-LEG-016 | notice | case_id | Read through the rwb-comms contract |
| DF-LEG-017 | notice | document_id | Read through the rwb-comms contract |
| DF-LEG-018 | notice | notice_type | Read through the rwb-comms contract |
| DF-CAS-002 | recovery_case | case_no | Read through the rwb-case contract |
| DF-CAS-003 | recovery_case | product_group | Read through the rwb-case contract |
| DF-ACE-020 | v_ace_account | total_balance | Read through the rwb-case contract, with its business date (ACE data held by rwb-source-data) |
| DF-ACE-078 | v_ace_contact | contact_value | Read masked through the rwb-case contract |
| DF-DEC-046 | approval | status | Read through the rwb-decision contract |
| DF-DEC-043 | approval | terms | Read through the rwb-decision contract |
| DF-DEC-053 | approval | decision_log_id | Read through the rwb-decision contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the rwb-decision contract |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read through the rwb-decision contract |

Test data is synthetic: notice N-0201, case RW-2026-000123, approvals A-0201 and its two repeats, and the synthetic users U-9211, U-9212 and U-9214. No production case, party or notice is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/approvals/{approvalId}` | P7 rwb-decision | The approval, its state, the rule and its version, and the source reference to the notice |
| POST | `/api/recovery/decision/v1/approvals/{approvalId}/approve` | P7 rwb-decision | Approve, or change the variant and approve; returns the decision record |
| POST | `/api/recovery/decision/v1/approvals/{approvalId}/refuse` | P7 rwb-decision | Refuse with a reason; returns the decision record |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | The notice, its state, its type, its template version and its document reference |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case, the case state and the case facts with the business date of each input |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and Litigation right check used by the composite route and by the direct calls |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decision records of the approval, the change and the refusal |

The composite decision screen route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0398; ASM-0573). The notice is approved and held through the rwb-decision approval operations, which call the notice owner; the harness does not call a notice approval path of its own.

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.comms.NoticeGenerated.v1 | rwb.comms.events.v1 | P6 rwb-comms | The generated notice and its template version are announced within 5 minutes of the seed call, so the approval is seen to follow a real generation |
| rwb.decision.ApprovalRequested.v1 | rwb.decision.events.v1 | P7 rwb-decision | One approval request exists for A-0201 and reaches the officer inbox path through gateway-bff |
| rwb.decision.ApprovalDecided.v1 | rwb.decision.events.v1 | P7 rwb-decision | One decision is announced per approval, with the final call, and none is announced for a refused call |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The decision record of the approval, the change and the refusal reaches the ledger within 5 minutes of the call |

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity. The ApprovalWorkflow of the workflow kit and the notice dispatch workflow are started by the owning stories; the harness observes their effect through state, events and the decision record only.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow. The 16:00 dispatch run (JOB-10) is the owning stories' schedule and is not started by the harness.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-comms | GET /notices/{noticeId}, NoticeGenerated | Notice N-0201 in state Generated, DEMAND-MTG TH version 2, document reference present; a new version from DEMAND-MTG-B on regenerate; Held REFUSED_BY_APPROVER on hold; withdrawn template returning MSG-P6-003 |
| rwb-decision | GET /approvals/{approvalId}, approve, refuse, GET /decision-log, ApprovalRequested, ApprovalDecided | Approval A-0201 WAITING for RW-LITOFF with rule R-LIT-03 version LIT-2026.12; a decision record with final call APPROVED, APPROVED_CHANGED or REFUSED; 409 for the preparer, a stale input and a decided item; 422 for an empty reason and an uncoded change; a forced write failure for the 503 case |
| rwb-access | POST /authorise | Allow RW-LITOFF and RW-LEGAL for Litigation A on D7.1; refuse a role without the right with MSG-P4-002 |
| rwb-case | GET /cases/{caseId}, case state and the case-owner task | Case RW-2026-000123, product group MORTGAGE, total balance of business date 13 December 2026 and a stale copy of 11 December 2026, postal address masked, state Waiting approval, one task raised on refusal |

The fakes are replaced by the real service as each I story lands, contract by contract. The harness environment, its synthetic seeding and the evidence format and retention: Not specified in the source documents (GAP-0398; ASM-0573).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Seven consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.comms.NoticeGenerated.v1, rwb.decision.ApprovalRequested.v1, rwb.decision.ApprovalDecided.v1 and rwb.decision-record.DecisionRecorded.v1; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity or Nexus operation |
| File | No | Reads no file itself; the notice document is asserted through the notice's document reference and never opened |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the five I stories.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| DecisionScreenClient | Harness adapter | Calls the gateway-bff composite decision route and the seven consumed operations of §12.2 with the Idempotency-Key header where the operation requires one |
| FakePack | WireMock project | Serves rwb-comms, rwb-decision, rwb-access and rwb-case from the published OpenAPI documents and AsyncAPI documents of §12.8 |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference in the trace, so a service never reads another service's tables |
| InputAgeCheck | Assertion | Reads the age limit of each input and asserts the business date on the item, including the stale total balance of 11 December 2026 against the 1 day limit |
| DecisionOrderCheck | Assertion | Asserts the decision record exists before the notice changes state, and that the record carries the inputs reference, rule version, template version, approver, time and final call |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0398; ASM-0573) |

**Environment and test data**

- Environment: SIT, one namespace, the owning services deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment, seeding and evidence: Not specified in the source documents (GAP-0398; ASM-0573).
- Data: synthetic case RW-2026-000123, demand notice N-0201 generated at 08:10 on 14 December 2026, approval A-0201 WAITING for RW-LITOFF, the sequence approvals of the change and the refusal, preparer U-9211, approvers U-9212 and U-9214, the total balance of business date 13 December 2026 with the stale 11 December 2026 copy, the address masked, reason codes TEMPLATE_VARIANT and WRONG_PARTY, and the 16:00 window. No production record is copied.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and DecisionScreenClient against the published OpenAPI documents of the owning services and the gateway-bff route contract.
2. Publish FakePack for the four owning services from the same documents and prove the harness runs green from Day 1 on the fakes.
3. Add the composite decision item assertion of AC1, including the 2 s per-call budget, the masked address and the SchemaBoundaryCheck.
4. Add the approve journey of AC2 with DecisionOrderCheck, asserting the decision record before the notice state moves and the 16:00 eligibility.
5. Add the change and the refusal journeys of AC3, then the InputAgeCheck and the refusals of AC4 with the stale 11 December 2026 input.
6. Add the concurrent decision and the decision-log failure of AC4, then the repeat after the fake recovers, and prove nothing moved in each case.
7. Replace each fake with the real service as its I story lands, contract by contract, keeping the same assertions.
8. Publish the run report per business date and add the pass/fail gate agreed with QA; the gate definition: Not specified in the source documents (GAP-0398; ASM-0573).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.decision.notice-approval` from the legacy solution plan: with the switch off the composite route offers no approve or reject action and no notice becomes Approved, and with it on the journey of §7 runs to its end.

**Done when:** the journey runs green against the five deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-002 | The preparer opens or acts on the item | You prepared this decision, so you cannot approve it. |
| MSG-P7-006 | An input is past its age limit | {input} is {days} days old, past its limit. Refresh it before you decide. |
| MSG-P6-003 | The template was withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-005 | Change of variant without a coded reason | Enter the reason you are not following the recommendation. |
| MSG-GEN-001 | Reject without a reason | Enter {field}. |
| MSG-GEN-004 | Another approver decided first | Someone else changed this record. Reload it to see their change. |
| MSG-P7-004 | Approved | Approved. The case moves to {state}. |
| MSG-P7-003 | Entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the Litigation right for D7.1 | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values; it does not own the message text. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-10 Approval queue | List | The D7.1 decision item of A-0201 is returned for role RW-LITOFF with its notice type and due time |
| SCR-11 Decision screen | Ready | The notice content, the case facts with each input's business date, the masked address, the rule and version, the template and version and the preparer are returned; approve, change and reject are offered |
| SCR-11 Decision screen | Stale input | The answer carries MSG-P7-006 for the stale total balance, approve is not offered, and a direct approve is refused |
| SCR-11 Decision screen | Decided | The outcome, the approver and the time are returned and no action is offered |
| SCR-18 Notice approval | Generated | The panel returns the notice waiting for a decision, with its template version |
| SCR-18 Notice approval | Approved | The notice shows as approved and waiting for the 16:00 dispatch run |
| SCR-18 Notice approval | Held | The notice shows as held with the reason, and the case-owner task is reported |

The harness opens no screen and renders no page; it asserts the composite route answer that the screen consumes. Screen-level behaviour remains with the owning APP stories. The harness environment and the evidence detail: Not specified in the source documents (GAP-0398; ASM-0573).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-014-01-ITG | AC1, BR1; ITG AC2 | Integration | Synthetic demand notice N-0201 from DEMAND-MTG version 2 |
| TC-E2-014-02-ITG | AC2, BR6; ITG AC3 | Integration | Variant DEMAND-MTG-B with reason TEMPLATE_VARIANT |
| TC-E2-014-03-ITG | AC3, BR7; ITG AC3 | Integration | Rejection with a reason |
| TC-E2-014-04-ITG | AC4, BR3; ITG AC4 | Integration | Preparer who also holds RW-LEGAL |
| TC-E2-014-05-ITG | AC5, BR4; ITG AC4 | Integration | Total balance from a load 3 days old |
| TC-E2-014-06-ITG | AC6, BR5; ITG AC4 | Integration | Template withdrawn after generation |
| TC-E2-014-07-ITG | AC7, BR7; ITG AC4 | Integration | Rejection with an empty reason |
| TC-E2-014-08-ITG | AC8, BR6; ITG AC4 | Integration | Variant change with no reason code |
| TC-E2-014-09-ITG | AC9; ITG AC4 | Integration | Two litigation officers deciding one item |
| TC-E2-014-10-ITG | AC10, BR2; ITG AC1 | Integration | Decision screen content check |
| TC-E2-014-11-ITG | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E2-014-12-ITG | Principle 5; ITG AC4 | NFR | The decision log write forced to fail during an approval; the notice stays Generated |

The AC column in Covers is the legacy AC of RWB-E2-014 that the copy is derived from; the ITG AC is the criterion of §7 that the copy asserts at integration level. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the input age limits, the override reasons, the templates and their variants, the route role and the 16:00 window are data held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: the postal address is masked in every answer the harness reads, the reason text is not logged, and the harness uses synthetic parties and stores IDs, business dates and assertions only.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never a production endpoint and never WIN; it does not dispatch, and it proves no delivery.
- The harness changes nothing: it approves, changes and refuses only through the owning contracts, and it never writes a notice state, an approval state or a decision record itself.
- Only an approved notice version is eligible for dispatch: the harness asserts eligibility from the notice state and the approval, and fails the run when a changed version other than the approved one is eligible.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-002 | Recommendation, reasons, inputs and limit on one screen | Business Requirements Program, section 5.7; Epic 2, section 3.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR2, BR4 | TC-E2-014-05-ITG, TC-E2-014-10-ITG |
| REQ-APD-006 | Demand and recall notices approved through approval routing | Business Requirements Program, section 5.7; Epic 2, section 3.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR1, BR3, BR5, BR6, BR7, BR8 | TC-E2-014-01-ITG to TC-E2-014-04-ITG, TC-E2-014-06-ITG to TC-E2-014-09-ITG, TC-E2-014-11-ITG, TC-E2-014-12-ITG |

### 19. Out of scope

- The five I stories and everything they own: RWB-P6-E1052-APP, RWB-P7-E2014-APP, RWB-P6-E2014-APP, RWB-P4-E2014-APP and RWB-P3-E2014-APP, and every screen, endpoint, table, rule and workflow they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-comms, rwb-decision, rwb-access and rwb-case, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- Dispatch to WIN, proof of delivery and the notice period (RWB-E2-021).
- Guarantor notices and statutory notices (Epic 5).
- Approval of decisions with an amount limit on SCR-11 (Epic 3).
- Template authoring and the Legal approval of templates (RWB-E1-034, RWB-E1-046).
