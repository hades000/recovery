# RWB-S8-E7008-CON Review an override - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7008-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S8-E7008-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | Rule-package read of rwb-decision at `/api/recovery/decision/v1` (section 12.2), faked |
| Integration dependencies | None |
| Contract version | API Specification v5, path version /v1 |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the override review of rwb-deviation, split from RWB-E7-008. It fixes the review branch of the published `PATCH /deviations/{deviationId}` (API-S8-002) on `/api/recovery/deviation/v1` (DP-13) with the `DeviationOutcome` request of the API Specification v5 (`outcome`, `note`) and the `Deviation` answer, the ten properties and seven required flags of the deviation element over DF-CAS-036 to DF-CAS-045, the outcome list LOV-DEV-OUTCOME, the reason riding `note`, the package read of rwb-decision at its version in force, the decision-record element of DP-03 with the rule ID and the package version, the rights of TSD S8 T6.1, the fakes and the absence tests. No source defines the override as a record of S8, gives the reason a field or publishes a deviation-list read; the plan's C row is empty while the package read is consumed; the primary role holds R only; and no requirement row traces to FEAT-DVF-08 (GAP-3067; ASM-5202, ASM-5203, ASM-5204, ASM-5205, ASM-5206, ASM-5207, ASM-5210). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S8-E7008-CON-L29, X20 RWB-S8-E7008-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 8 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the override review of rwb-deviation — the review branch of the deviation-outcome operation on `/api/recovery/deviation/v1`, the deviation and outcome elements with their required flags and lists, the reason carried by `note`, the package read as a consumed row, the decision-record element with the rule ID and the package version, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-08 and the wave 4 harness build against one fixed, testable contract on Day 1, and an outcome value, a consumed row or an answer shape can never drift between rwb-deviation, rwb-decision and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy override review of RWB-E7-008 crossed four boundaries at once: the deviation of the case, the rule version in force, the outcome it records and a screen, and it named two endpoints that carry every deviation action of the module with no element published for the review. The target splits them: rwb-case owns the case, its states and the clock, rwb-decision owns the DEVIATION package and its 22 rules, and rwb-deviation owns the deviation row, its stage and the record of the review. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_deviation`, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with its retry and `.dlt` topics, task queue `rwb-deviation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.deviation` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition.

Six points are carried as gaps and assumptions rather than decided quietly: the override is the open deviation record and not an entity of its own (ASM-5202); the reason has no published field and rides `note` (ASM-5203); the plan's C row is None although one consumed row is declared, and DP-04, DP-05, DP-07, DP-08 and DP-09 are absent from the pattern set (ASM-5204, ASM-5206); the review records, it does not clear, so no `cleared_at` property and no stop-lift is declared (ASM-5205); the primary role holds R only while both operations declare U (ASM-5207); and no requirement row traces to FEAT-DVF-08 (ASM-5210).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `deviation` is S8's, `recovery_case` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `payment` is P8's. This document never declares another service's table or operation as its own.
- The two operations are published: TSD S8 T-A.1 gives API-S8-001 `POST /cases/{caseId}/deviations` and API-S8-002 `PATCH /deviations/{deviationId}` with their access and idempotency rules, T-A.2 gives the request and answer elements with the error set 401, 403, 404, 409, 422 and 503, and the API Specification v5 publishes `Deviation`, `DeviationRequest` and `DeviationOutcome`. The review branch is declared inside API-S8-002 and needs no new path.
- The rwb-decision package row is published with its fake, so the consumed row names a real owner document; it is not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3067; ASM-5204).
- The DEVIATION package and its rows R-DEV-01 to R-DEV-22 over 9 states are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `deviation` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration. The reason has no column in it (ASM-5203).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the review branch of the OpenAPI 3.1 document of rwb-deviation for API-S8-002: the operation with its request and answer elements, the review properties, the right and the error responses.
2. Fix the `Deviation` element over the columns of DF-CAS-036 to DF-CAS-045, with its seven required flags and the lists of TSD S8 T3.2 published unchanged.
3. Fix the `DeviationOutcome` request: `outcome` over LOV-DEV-OUTCOME and `note`, and record that `note` carries the forum's reason because no source gives the reason a field of its own.
4. Record that the override is the open deviation record and that the baseline declares no override entity, no second path and no new column.
5. Record the consumed row: the DEVIATION package read of rwb-decision at its version in force, with its placeholder operation name.
6. Record the decision-record element of DP-03, written before the review is answered, with the rule ID that fired and the package version.
7. Record the rights of the operation, the naming baseline, the boundary and the rule that no value is a constant of the code.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the shapes, the lists, the scope, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the absence of a published and of a consumed event.
10. Tag the baseline and hand it to RWB-S8-E7008-APP, to the other deviation stories that share the two operations, to SCR-08 and to the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC6 |
| X5 | The outcome list or a deviation state is declared as a code enumeration taken from no source | The vocabulary test fails the build: the list is LOV-DEV-OUTCOME and nothing else | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a timer row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event published by this step, a consumed event, a second topic, a Schedule or a `cleared_at` write | The absence test fails the build | None | AC7 |
| X8 | The rights of the operation are not the ones TSD S8 T6.1 and T-A.1 give the deviation outcome | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S8 appendices, the API Specification and the published owner contract of rwb-decision only |
| Negotiable | The example values and the internal record shape are settled in the baseline review; the base, the operations, the right, the lists, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S8-E7008-APP, the other deviation stories that share the two operations, SCR-08 and the wave 4 harness on Day 1, and the rwb-decision team on the same day |
| Estimable | One OpenAPI document, nine contract tables, three fakes and eleven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the override review of rwb-deviation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of deviation is S8, of recovery_case and timer is P3, and of every v_ace_* view, decision_log_entry and rule_row is P1 or P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The deviation-outcome operation is declared with its review branch and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-deviation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares PATCH /deviations/{deviationId} as API-S8-002 with a DeviationOutcome body in and a Deviation answer of status 200, under the base /api/recovery/deviation/v1 and owned by rwb-deviation
    Then the review branch is declared inside API-S8-002 as the action the request carries, with no second path and no override path of its own
    Then it declares POST /cases/{caseId}/deviations as API-S8-001 with a DeviationRequest body in and a Deviation answer, with the Idempotency-Key header, and names the raise stories of the module as its builders
    Then API-S8-002 declares no Idempotency-Key and a repeat is matched on the deviation reference and the outcome
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no operation of the screening, the clearance, the breach path or a deviation-list read is declared by this document

  Scenario: AC2 The deviation and outcome elements, their required flags and their lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S8 T3.0, T3.1, T3.2 and T-A.2, and with the API Specification v5
    Then the Deviation element declares the ten columns of DF-CAS-036 to DF-CAS-045: id, caseId, deviationCode, raisedAt, raisedBy, pausedState, handlerUserId, contactStop, clearedAt and outcome
    Then the required flags are id, caseId, deviationCode, raisedAt, raisedBy, pausedState and contactStop, id is read-only, and the other properties are optional
    Then the lists are LOV-DEVIATION X1 to X7, LOV-RAISED-BY SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, and LOV-DEV-OUTCOME RETURNED, RE_ROUTED and CASE_ENDED, copied from TSD S8 T3.2 and published unchanged
    Then the DeviationOutcome request declares outcome over LOV-DEV-OUTCOME and the note string of the API Specification v5, and the note is declared as the field that carries the forum's reason
    Then the document declares no property, field ID or enumeration for the reason, no override entity, no override property and no second outcome set, and the reason's name and value format carry the placeholder Not specified in the source documents (GAP-3067; ASM-5202, ASM-5203)
    Then the document declares no property for a contact value, a rule row, an ACE extract, a case state or a cleared_at write

  Scenario: AC3 The package read is declared as consumed and the facts stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the package read is declared as consumed from P7 rwb-decision, with the DEVIATION package, its version and its R-DEV-01 to R-DEV-22 over 9 states
    Then the operation name of the row is Not specified in the source documents (GAP-3067; ASM-5204) and the row carries the placeholder and a fake
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no timer property, no rule_row property and no grant on any rwb_* schema of another owner
    Then the row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)
    Then the case move is declared on the parent-child workflow edge and not as a REST row

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S8 T-A.1, T-A.2 and T6.1
    Then both operations declare Case record right U with the scope applied
    Then RW-CASEOWN holds CRU and RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE and RW-GUARANT hold RU, and they are the twelve identities the legacy permission table's eight roles and its four further holders resolve to
    Then RW-RISK, RW-CONDUCT and RW-COE hold R and need the operation's right U to record a review, and the conflict is recorded (ASM-5207, ASM-5208)
    Then every other role and every PT-* and SY-* identity of TSD S8 T6.1 holds R or U as the matrix gives it
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and written before the review is answered (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S8 T2
    Then one decision record is declared per review with the case reference, the deviation reference and code, the rule ID that fired, the package version in force, the reason, the outcome, the from state and the to state
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the answer leaves the service, and a failed write leaves everything unchanged with MSG-P7-003
    Then the rule IDs recorded are R-DEV-09, R-DEV-10 and R-DEV-22 only, and R-DEV-11 is named as the X3 path's row on INSURANCE_SETTLED
    Then the record carries no rule row, no personal data and no contact value

  Scenario: AC6 The three fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-decision package fake answers the DEVIATION package at its version with R-DEV-01 to R-DEV-22
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-08 answer before and after the review
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_deviation, the login is rwb_deviation, the base is /api/recovery/deviation/v1, the topic is rwb.deviation.events.v1 with its retry and .dlt topics, the queue is rwb-deviation in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.deviation
    Then the tables named as owned are deviation and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic, no Schedule and no cleared_at property
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule, a v_ace_* read or a case write (ASM-5205, ASM-5206)

  Scenario: AC8 Each business rule BR1 to BR14 is covered by a criterion or a test (new, D-RCV-60)
    Given the business rules of section 8
    When each rule is compared with the criteria of section 7 and the test rows of section 16
    Then each of BR1 to BR14 names a criterion of this section or a test row of section 16
    Then a rule that is an architecture constraint names the guardrail or boundary test that covers it
    Then no rule of section 8 is left without a criterion or a test
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S8-E7008-APP and copy no criterion of the legacy story, whose two criteria stay with the app story word for word. The review records an outcome and a reason: no case closes, no clock resumes and no event is declared here (ASM-5202, ASM-5205, ASM-5206).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The deviation row is rwb-deviation's, and the contract declares the fields, the required flags and the lists on the `Deviation` and `DeviationOutcome` elements only | TSD S8 T3.1, T3.2, T-A.2; context pack ownership rows (table `deviation`) |
| BR2 | The review record is declared as an element written before the answer, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S8 T2; legacy AC1 and AC2 |
| BR3 | No event of this step is declared: EV-06 and EV-07 are the raise and clearance stories' and the outbox library of DP-09 is recorded as an absent H row | ASM-5206; Event and Messaging Design v5; TSD S8 T5.3 |
| BR4 | The package is rwb-decision's: the contract declares the package read as consumed and declares no rule row, no threshold and no rule ID set as a property | ASM-5204; TSD S8 T4 |
| BR5 | The override is the open deviation record: the baseline declares no override entity, no override path, no override column and no second outcome set | ASM-5202; FSD S8 A2.17.3.2; TSD S8 T3.1 |
| BR6 | The reason rides the `note` of the request and is recorded in the decision record; the document declares no reason property, field ID or list | ASM-5203; API Specification v5 `DeviationOutcome` |
| BR7 | The review records and does not clear: the document declares no `cleared_at` property, no contact-stop write, no timer property and no clock resume | ASM-5205; FSD S8 A2.6, A2.17.2 |
| BR8 | API-S8-002 declares no `Idempotency-Key`, so a repeat is matched on the deviation reference and the outcome; API-S8-001 declares the header and stores its answer | TSD S8 T-A.2 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, dates, a list value, a rule ID, a package version and a reason text only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S8 T6.2 |
| BR10 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR12 | The document lists only operations owned by rwb-deviation; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11; context pack ownership rows (2 REST operations) |
| BR13 | The rights of the review are the case-record right U the permission table gives, held by the twelve identities of T6.1, and the primary role's R is recorded as a conflict rather than widened | TSD S8 T6.1, T-A.1; legacy permission table of RWB-E7-008; ASM-5207, ASM-5208 |
| BR14 | The states `DEV_WITH_OWNER`, `DEV_RESOLVED`, `DEV_REROUTE` and `CASE_ENDED` are declared as the vocabulary of the answer and of the DEV machine and move no deviation by themselves | ASM-5205; TSD S8 T4; Business Rules and Routing Logic v4 rows R-DEV-09, R-DEV-10, R-DEV-11, R-DEV-22 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the reason, the consumed row, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the other deviation stories that share the two operations, SCR-08, the wave 4 harness and the owners of rwb-decision, rwb-case and rwb-access accept the document and the fakes | Baselined |
| Baselined | The reason field is confirmed | The business lead replaces the placeholder inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional reason code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or an outcome becomes a set the list does not hold | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1, AC3 and AC7 fail: an override entity, a second path, a `v_ace_*` view, a `recovery_case` property, a `cleared_at` property, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's: `DEV_WITH_OWNER` is the state the review reads, `DEV_RESOLVED` and `DEV_REROUTE` are the states R-DEV-09, R-DEV-10 and R-DEV-22 give, `CASE_ENDED` follows `INSURANCE_SETTLED` on R-DEV-11 and belongs to the X3 path, and R-DEV-18 resumes the clock on clearance. This baseline fixes the vocabulary and the answer shape and moves no deviation.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-deviation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the confirmed reason field and the correction of the plan rows the baseline consumes, including the consumed row and the absent DP-04, DP-05, DP-07, DP-08 and DP-09 rows |
| Business lead | Confirms the reason that replaces the placeholder, and the reading of the override as the open deviation record |
| Consuming teams (the app story, the other deviation stories, SCR-08, the wave 4 harness and the owners of rwb-decision, rwb-case and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-deviation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Deviation element | The ten columns of DF-CAS-036 to DF-CAS-045: `id`, `caseId`, `deviationCode`, `raisedAt`, `raisedBy`, `pausedState`, `handlerUserId`, `contactStop`, `clearedAt` and `outcome` | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |
| Raise element | `DeviationRequest`: `deviationCode`, `reason` and `documentIds`, with no review property | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |
| Outcome element | `DeviationOutcome`: `outcome` over LOV-DEV-OUTCOME and `note`, which carries the forum's reason | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |
| Required flags | `id`, `caseId`, `deviationCode`, `raisedAt`, `raisedBy`, `pausedState` and `contactStop` on the deviation element, with `id` read-only; the other properties optional | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |
| Lists | LOV-DEVIATION X1 to X7, LOV-RAISED-BY SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, and LOV-DEV-OUTCOME RETURNED, RE_ROUTED and CASE_ENDED, copied from TSD S8 T3.2 and published unchanged | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |
| Event data | None of this step: no event is declared (§12.3) | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the answer, with the rule ID and the package version (DP-03) | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |
| Case, timer and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` and DF-WRK-027 to DF-WRK-036 of `timer` in P3, and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8) | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |
| Consumed field with no source | The operation name of the package read and the name, the field ID and the value format of the reason: Not specified in the source documents (GAP-3067; ASM-5203, ASM-5204) | Not specified in the source documents (DOR-RWB-S8-E7008-CON-7) |

The field-level types, lengths and required flags of the declared elements are those of the API Specification v5 and TSD S8 T3.1; this story fixes the element names, the required flags of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/deviations/{deviationId}` (API-S8-002) | `DeviationOutcome` in, `Deviation` of status 200 out, carrying the recorded outcome, the state and the decision-record reference of the review | Case record, right U, scope applied | `Idempotency-Key` header |
| POST | `/cases/{caseId}/deviations` (API-S8-001) | `DeviationRequest` in, `Deviation` out, carrying the code, the raise source and the contact stop; declared here and built by the raise stories of the module | Case record, right U, scope applied | `Idempotency-Key` header |

API-S8-002 answers 400, 401, 403 with MSG-P4-002, 404 for a deviation that is not on the case, 409 for a deviation that is not open at `DEV_WITH_OWNER`, 422 with MSG-GEN-001 for a missing or unlisted outcome, and 503, each with the error envelope and one message ID of section 14. The paths, the operation IDs, the element names, the rights and the error codes are published in TSD S8 T-A.1 and T-A.2 and the API Specification v5; the review branch, the meaning of `note` and the fact that no deviation-list read is published carry the placeholder (GAP-3067; ASM-5202, ASM-5203, ASM-5206). The outcome branch of the same operation, the screening and the breach path belong to other stories of the module and none of them is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The rule-package read in force (operation name Not specified in the source documents (GAP-3067; ASM-5204)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEVIATION package at its version, with R-DEV-01 to R-DEV-22 over 9 states, read once per review; faked |

The row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). It is a contract dependency of class C that the plan's C row does not carry, and the S8 row of the connection matrix carries no P7 edge although the default ruling gives the rule package registry to rwb-decision; the absence is recorded (GAP-3067; ASM-5204).

#### 12.3 Events published

None. The service owns the topic `rwb.deviation.events.v1` and its event set carries EV-06 `DeviationRaised` (`caseId`, `deviationCode`, `raisedBy`, consumed by Timers and Communications for the contact stop) and EV-07 `DeviationCleared` (`caseId`, `deviationCode`, `outcome`, consumed by Timers and Communications), both belonging to the raise and clearance steps of the stage (Event and Messaging Design v5; TSD S8 T5.3). A review sets the outcome and the state the rule gives, lifts no stop and closes no case, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays the events is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5206).

#### 12.4 Events consumed

None. The service listens to rwb-case, rwb-source-data and rwb-agent events on the connection matrix's columns P3, P1 and P10 (context pack connection matrix, row S8), and none of them belongs to the review: the trigger is the officer's confirmation on SCR-08, and the FSD declares no background event for the feature (FSD S8 A2.17.4.4). This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per deviation, can start at any time on a case, continues-as-new with the case stage | `rwb-deviation` | The stage that hosts the review step; its signals and its outcome for the parent are declared, not built |
| `recordDeviationReview` | Activity, the one review step of the stage | `rwb-deviation` | The deviation reference, the outcome, the reason and the package version in; the record reference, the state and the outcome out |
| the stage outcome for the parent | Parent-child workflow edge to `CaseWorkflow` | `rwb-case` | The deviation state and the outcome as the stage result; no REST row is declared for the case move |

Start rule of `DeviationWorkflow` per Temporal Catalog v1: an agent or officer flags the deviation (EV-06 starts screening), or universal rules R-UNI-04 to 09 fire. Workflow ID form: Not specified in the source documents (CG-ALL-11645). Duplicate-start policy: Not specified in the source documents (CG-ALL-11645).

No child workflow for the case and none for the money exists in this service, and the service owns one workflow and no job in the context pack's ownership rows. The activity name is a target design choice, and the step runs from the officer's confirmation. No activity is registered by this story.

#### 12.6 Schedules

None. The review is an officer-driven step; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The service's job list is empty in the context pack's ownership rows, and the escalation timer of R-DEV-20, the clearance and the screening run are other stories'.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | The deviation X1 to X7 of a case, its code, its raise facts, its handler, its stop, its state and its outcome; the table the answer element is drawn from |
| decision_record | PLT library, created in `rwb_deviation` | The local hash-linked decision record of the review (DP-03) |
| idempotency_key | PLT library, created in `rwb_deviation` | The key of the raise operation and the answer it holds; the review declares none |
| outbox_event | PLT library, created in `rwb_deviation` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6) and `payment` (P8) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision rule-package fake | The DEVIATION package at its version in force with R-DEV-01 to R-DEV-22 over 9 states | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-08 answer for the open deviations of `RW-2026-000502`, before and after the review | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation name of the package read carries the placeholder until its owner confirms it (GAP-3067; ASM-5204).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | API-S8-001 and API-S8-002 on `/api/recovery/deviation/v1`; the package read of rwb-decision; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; EV-06 and EV-07 are the raise and clearance stories', and the decision record is the library's on `rwb.decision-record.v1` and not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `DeviationWorkflow` and `recordDeviationReview` on `rwb-deviation`; the stage outcome to `CaseWorkflow` on `rwb-case`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no deviation and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and three fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the review is answered. DP-13 moves the base of the legacy paths and gives the deviation-outcome operation its home. DP-19 sits behind SCR-08, whose screen model is the edge contract's. DP-04, DP-05, DP-07, DP-08 and DP-09 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, ACE data is declared as a prohibition, the lists are published as values of TSD S8 T3.2 and not as a reference-data contract, the access guard is a template capability, and the outbox is an absent library row rather than an event of this step (GAP-3067; ASM-5204, ASM-5206).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, and the Drools kit row `RWB-PLT-E1072-CON` that a rule evaluation would add. The package row is a C dependency and is recorded as the contract dependency in the metadata table.

**Deliverables and build steps**

1. Write the review branch of API-S8-002 and validate the additive rule of AC1 in the pipeline.
2. Write the `Deviation` element with its ten properties and seven required flags, the `DeviationRequest` element and the lists of AC2.
3. Record the `DeviationOutcome` element with `outcome` and `note`, and the statement that `note` carries the reason with its placeholder.
4. Record the package row of AC3 with its owner, its budget and its placeholder, and the parent-child edge of the case move.
5. Record the rights and the error envelope of AC4, with the primary role's R as a recorded conflict.
6. Record the decision-record element of AC5 and validate it against the library schema.
7. Publish the three fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-deviation-v1.yaml`, the three elements, the contract README rows for the consumed row and its placeholder, and the three fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the eleven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the other deviation stories, SCR-08 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | The contract describes the raised state from which the review is taken, raised by the raise story of the module and not by this operation | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required field of a request is absent or invalid, the outcome among them, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the case record right U the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the review is answered | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-08 Deviation queue in its list state, before and after the review, through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviations, their handlers and the recorded outcome, and rwb-case for the case and its route state; this baseline fixes the rwb-deviation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives SCR-08 "Loading; list" and SCR-06 Raise deviation "Form; saved": the raise form is the raise stories'. SCR-06 states empty, loading, error and no access: Not specified in the source documents (CG-ALL-11649). SCR-08 states empty, error and no access: Not specified in the source documents (CG-ALL-11650); its loading state is given above.

No source publishes a deviation-list read, so the list the screen shows has no operation and carries the placeholder (GAP-3067; ASM-5206); and neither screen is described as a review screen, so the place of the review action on SCR-08 is Not specified in the source documents (GAP-3067; ASM-5202). The refusal, not-open, bad-outcome and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-008-01 | AC1, AC2 | Contract | The open deviation `X3` of `RW-2026-000502` on the fake; the contract half answers the operation, the elements, the lists and the reason placeholder |
| TC-E7-008-02 | AC2, AC5 | Contract | The deviation element and the outcome request; the contract half answers the ten properties, the lists, the decision element and the MSG-P7-003 path |
| TC-E7-008-03 | AC4 | Contract | A role without the right U and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E7-008-04 | AC5, AC7 | Contract | The decision-record stub stopped; the contract half answers the failed-write path and the absence tests |
| TC-S8-E7008-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the review branch, the `Idempotency-Key` rule and the seven error answers are present |
| TC-S8-E7008-CON-02 | AC2 | Contract | The two elements validate with their ten and two properties, the seven required flags, the three lists, the `note` reason and its placeholder |
| TC-S8-E7008-CON-03 | AC3 | Contract | The consumed package row and its placeholder; the no-`v_ace_*`, no-`recovery_case`, no-timer, no-rule-row boundary; the case move on the workflow edge |
| TC-S8-E7008-CON-04 | AC4, AC5 | Contract | The rights, the twelve holders of U, the primary role's R, the error envelope and the decision-record element against the library schema |
| TC-S8-E7008-CON-05 | AC6, AC7 | Contract | The three fakes match the document and a drifted fake fails the build; the naming baseline, the tables owned and the absence of an event, a second topic and a Schedule |
| TC-S8-E7008-CON-06 | AC7 | Contract | The four owned tables of §12.7 at their boundary; no foreign key and no read or write of recovery_case, timer, decision_log_entry, rule_row, v_ace_* views, document, notice or payment |
| TC-S8-E7008-CON-07 | AC8 | Contract | Each of BR1 to BR14 is named by a criterion or a test row, and a rule that is an architecture constraint names its guardrail or boundary test; no rule of section 8 is left without either |

The four legacy cases are those of RWB-E7-008 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S8-E7008-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The seven cases `TC-S8-E7008-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the review conditions, the deviation codes, the outcome list, the states, the right and the package version stay rule rows and reference data, never a schema default, an enumeration member taken from no source or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, dates, a list value, a rule ID, a package version and a reason text only, and every example is synthetic.
- The case stays with rwb-case: the document declares no `recovery_case` property, no case row write and no case state write.
- The rule rows stay with rwb-decision: the document declares no rule row, no threshold and no rule ID set.
- The review records and does not clear: no `cleared_at` property, no contact-stop write, no timer property and no clock resume is declared (BR7).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-deviation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule, a Quartz row or an override entity.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-DVF-08 | The requirement this feature serves is Not specified in the source documents (GAP-3067; ASM-5210): TSD S8 T8 maps every REQ-DVH and REQ-S8 row to FEAT-DVH-01, FEAT-DVF-01 or a placeholder | The review branch of API-S8-002, the two elements and the package row | TC-E7-008-01, TC-E7-008-02, TC-S8-E7008-CON-01, TC-S8-E7008-CON-02 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-S8-E7008-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as a later story's | TC-S8-E7008-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The package row with its budget and breaker | TC-S8-E7008-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S8-E7008-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-008, disposition Split (rework); feature FEAT-DVF-08 |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S8-E7008-APP; this baseline copies none of them |
| Source text | Legacy RWB-E7-008; FSD S8 Deviation handling v4 A2.17, A2.17.2, A2.17.3 and A2.17.4; TSD S8 Deviation handling v3 T0.2, T2, T3.0, T3.1, T3.2, T4, T5.3, T6.1 and T-A; API Specification v5 elements `Deviation` and `DeviationOutcome`; Business Rules and Routing Logic v4 rows R-DEV-09, R-DEV-10, R-DEV-11 and R-DEV-22 |
| Test cases | The four legacy cases as the contract half, and the five new contract cases TC-S8-E7008-CON-01 to -05 |
| Feature and screens | FEAT-DVF-08, SCR-08 Deviation queue |
| Rules | R-DEV-01 to R-DEV-22 governed in rwb-decision; R-DEV-09, R-DEV-10 and R-DEV-22 fire on the review and R-DEV-11 on the X3 path |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the review branch, the evaluation, the decision record and the answer: RWB-S8-E7008-APP.
- The case of record, its states, the parent `CaseWorkflow` and the clock: rwb-case (P3).
- The authoring, testing, approval and versioning of the DEVIATION package and of the rule rows: rwb-decision (P7), whose row this baseline declares as consumed and faked (ASM-5204).
- The name, the field ID and the value format of the reason: the business lead confirms them at the baseline review and the placeholder stands until then (GAP-3067; ASM-5203).
- The clearance of the deviation, the stop lift, `cleared_at`, the clock resume of R-DEV-18 and the route reopen of R-DEV-19: FEAT-DVH-06 and the clearance and route stories.
- The deviation-list read of SCR-08: no operation is published by any source and the placeholder stands (GAP-3067; ASM-5206).
- The screening that proposes a deviation and the L1 agent: the E1 and E2 stories of the module. The raise operation's behaviour: RWB-S8-E7001-APP to RWB-S8-E7007-APP. The breach path: RWB-S8-E7010-APP.
- The gateway-bff composite route and the screen field list of SCR-08: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
