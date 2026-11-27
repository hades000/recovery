# RWB-S8-E7009-CON Match a complaint to the preceding contact - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7009-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S8-E7009-CON-16); the squad sizes it at refinement |
| Contract version | v1, path `/api/recovery/deviation/v1` and file `openapi/rwb-deviation-v1.yaml` |
| Depends on (build) | `RWB-PLT-E1027-CON`, `RWB-PLT-N001-CON` (section 13 pattern table) |
| Contract dependencies | P1 rwb-source-data contact read `/api/recovery/source-data/v1`; P7 rwb-decision rule-package read `/api/recovery/decision/v1` (class C, section 12.2) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the complaint-to-contact match of rwb-deviation, split from RWB-E7-009. It fixes the match branch of the published `PATCH /deviations/{deviationId}` (API-S8-002) on `/api/recovery/deviation/v1` (DP-13) with the `DeviationOutcome` request and the `Deviation` answer of TSD S8 T-A.2, the `Deviation`, `DeviationRequest` and `DeviationOutcome` elements over the columns of DF-CAS-036 to DF-CAS-045, the optional complaint and contact references with their placeholders, the consumed rows of the rwb-source-data contact read and the rwb-decision package read, the decision-record element of DP-03, the rights of TSD S8 T6.1, the fakes and the absence tests. DP-04, DP-05, DP-09 and DP-18 are not in the plan's pattern set although the step evaluates a package, reads a contact and owns a topic; the plan's C row is empty although the baseline declares two consumed rows; no source publishes the match references or the match outcome set; and no requirement row traces to FEAT-DVF-09 (GAP-3069; ASM-5211, ASM-5212, ASM-5213, ASM-5214, ASM-5215, ASM-5217). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S8-E7009-CON-L116, HELD-RWB-S8-E7009-CON-L222, X20 RWB-S8-E7009-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 11 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the complaint-to-contact match of rwb-deviation — the match branch of the deviation-outcome operation on `/api/recovery/deviation/v1`, the deviation, raise and outcome elements with their required flags, the optional complaint and contact references, the two consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-08 and the wave 4 harness build against one fixed, testable contract on Day 1, and a reference, a consumed row or an answer shape can never drift between rwb-deviation, rwb-source-data, rwb-decision and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy complaint-to-contact match of RWB-E7-009 crossed four boundaries at once: the case of record, the contact that caused the complaint, the rule version in force and a screen, and it named two endpoints that carry every deviation action of the module with no element published for any of them. The target splits them: rwb-case owns the case and its route states, rwb-source-data owns the contact points and the interaction ledger, rwb-decision owns the DEV package, and rwb-deviation owns the deviation row, its stage and the record of the match. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_deviation`, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with its retry and `.dlt` topics, task queue `rwb-deviation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.deviation` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition.

Five points are carried as gaps and assumptions rather than decided quietly: the complaint and contact references and the match outcome set have no published name, format or value set (ASM-5212); the plan's C row is None while the baseline declares two consumed rows, and DP-04, DP-05, DP-09 and DP-18 are absent from the pattern set (ASM-5213, ASM-5214, ASM-5215); the match rides one published operation and has no path of its own (ASM-5211); the Conduct and QA officer holds R only on the case record while the feature needs U (ASM-5216); and no requirement row traces to FEAT-DVF-09 (ASM-5217).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `deviation` is S8's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view and the contact points are P1's, `document` is P5's, `notice` is P6's and `payment` is P8's. This document never declares another service's table or operation as its own.
- The two operations are published: TSD S8 T-A.1 gives API-S8-001 `POST /cases/{caseId}/deviations` and API-S8-002 `PATCH /deviations/{deviationId}` with their access and idempotency rules, and T-A.2 gives the error set as 401, 403, 404, 409, 422 and 503 with the request and answer elements. The match branch is declared inside API-S8-002 and needs no new path; what the sources do not give are the match references and the outcome set (GAP-3069; ASM-5211, ASM-5212).
- The rwb-source-data contact row and the rwb-decision package row are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3069; ASM-5213, ASM-5214).
- The DEV package and its rows R-DEV-01 to R-DEV-22 over 9 states are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `deviation` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration. The match references have no column in it (ASM-5212).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the match branch of the OpenAPI 3.1 document of rwb-deviation for API-S8-002: the operation with its request and answer elements, the match properties, the rights and the error responses.
2. Fix the `Deviation` element over the columns of DF-CAS-036 to DF-CAS-045 and the `DeviationOutcome` and `DeviationRequest` elements with their published properties of TSD S8 T-A.2.
3. Fix the optional complaint and contact references and the match outcome of the request, marking with the placeholder what the sources do not give.
4. Fix the consumed rows: the contact read of rwb-source-data and the package read of rwb-decision with its version.
5. Record the decision-record element of DP-03, written before the match is answered.
6. Record the rights of the operation, the naming baseline and the rule that no value is a constant of the code; record the lists of TSD S8 T3.2 as they stand.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the shapes, the scope, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the absence of a published and of a consumed event.
9. Tag the baseline and hand it to RWB-S8-E7009-APP, to the other deviation stories that share the two operations, to SCR-08 and to the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC6 |
| X5 | The match references or the outcome set are declared as an enumeration taken from no source | The vocabulary test fails the build: no source publishes either | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event published by this step, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of the operation are not the ones TSD S8 T6.1 and T-A.1 give the deviation outcome | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S8 appendices, the API Specification and the published owner contracts of rwb-source-data and rwb-decision only |
| Negotiable | The names of the match properties and the example values are settled in the baseline review; the base, the operations, the rights, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S8-E7009-APP, the other deviation stories that share the two operations, SCR-08 and the wave 4 harness on Day 1, and the rwb-source-data and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, four fakes and eleven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the complaint-to-contact match of rwb-deviation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of deviation is S8, of recovery_case and timer is P3, of every v_ace_* view and the contact points is P1, and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The deviation-outcome operation is declared with its match branch and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-deviation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares PATCH /deviations/{deviationId} as API-S8-002 with a DeviationOutcome body in and a Deviation answer of status 200, under the base /api/recovery/deviation/v1 and owned by rwb-deviation
    Then it declares POST /cases/{caseId}/deviations as API-S8-001 with a DeviationRequest body in and a Deviation answer, with the Idempotency-Key header, and names the raise stories of the module as its builders
    Then the match branch is declared inside API-S8-002 as the action the request carries, with no second path, and the outcome branch of RETURNED, RE_ROUTED and CASE_ENDED is named as the clearance stories'
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no operation of the screening, the clearance or the breach path is declared by this document

  Scenario: AC2 The deviation, raise and outcome elements and the match properties are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S8 T3.1, T3.2 and T-A.2, and with the API Specification v5
    Then the Deviation element declares the ten columns of DF-CAS-036 to DF-CAS-045: id, caseId, deviationCode, raisedAt, raisedBy, pausedState, handlerUserId, contactStop, clearedAt and outcome
    Then the required flags are id, caseId, deviationCode, raisedAt, raisedBy, pausedState and contactStop, and the other properties are optional
    Then the lists are LOV-DEVIATION X1 to X7, LOV-RAISED-BY SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, and LOV-DEV-OUTCOME RETURNED, RE_ROUTED and CASE_ENDED, copied from TSD S8 T3.2 and published unchanged
    Then the DeviationOutcome request declares the outcome and the note of the API Specification v5 and the optional complaint reference and contact reference of the match, with their value format and the match outcome set carrying the placeholder Not specified in the source documents (GAP-3069; ASM-5211, ASM-5212)
    Then the DeviationRequest element declares the deviationCode, the reason and the documentIds and no match property
    Then no property is added for a contact value, a rule row, an ACE extract or a case state

  Scenario: AC3 The consumed rows of rwb-source-data and rwb-decision are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the contact read is declared as consumed from P1 rwb-source-data, with the contact point of the case party, its channel, its time and the interaction it belongs to
    Then the package read is declared as consumed from P7 rwb-decision, with the DEV package, its version and its R-DEV-01 to R-DEV-22 over 9 states
    Then the operation names of the two rows are Not specified in the source documents (GAP-3069; ASM-5213, ASM-5214) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no timer property, no rule_row property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S8 T-A.1, T-A.2 and T6.1
    Then both operations declare Case record right U with the scope applied, on API-S8-001 and API-S8-002 as T-A.1 gives them
    Then RW-CASEOWN holds CRU and RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE and RW-GUARANT hold RU, and they are the twelve identities the legacy permission table's eight roles and its four further holders resolve to
    Then RW-CONDUCT holds R and needs the operation's right U to record the match, and the conflict is recorded (ASM-5216)
    Then every other role and every PT-* and SY-* identity of TSD S8 T6.1 holds R or U as the matrix gives it
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and written before the match is answered (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S8 T2
    Then one decision record is declared per match with the case reference, the deviation reference and code X1, the complaint reference, the contact reference, the package version in force, the match outcome and the matched-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the answer leaves the service, and a failed write leaves everything unchanged with MSG-P7-003
    Then the record carries no rule row, no contact value and no personal data, and the contact reference is declared as a key and not as a contact value

  Scenario: AC6 The four fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-source-data contact fake answers the preceding contact of the case party and a case with no such contact
    Then the rwb-decision fake answers the DEV package at its version with R-DEV-01 to R-DEV-22
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-08 answer before and after the match
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_deviation, the login is rwb_deviation, the base is /api/recovery/deviation/v1, the topic is rwb.deviation.events.v1 with its retry and .dlt topics, the queue is rwb-deviation in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.deviation
    Then the tables named as owned are deviation and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic and no Schedule, and it names EV-06 DeviationRaised and EV-07 DeviationCleared as the raise and clearance stories' and the service's job list as empty
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule or a v_ace_* read (ASM-5215)

  Scenario: AC8 Each rule BR1 to BR14 is covered by a criterion and a test (new, D-RCV-60)
    Given the business rules table of section 8
    When each rule is checked against the criteria of section 7 and the test cases of section 16
    Then each of BR1 to BR14 names at least one criterion (AC1 to AC7) and one test case (TC-S8-E7009-CON-01 to -05) in its Covered by column
    Then the proposed test of this criterion is Not specified in the source documents (NEWAC-RWB-S8-E7009-CON-AC8)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S8-E7009-APP and copy no criterion of the legacy story, whose two criteria stay with the app story word for word. The match records a conduct fact: no deviation state moves, no clock resumes and no event is declared here (ASM-5212, ASM-5215).

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The deviation row is rwb-deviation's, and the contract declares the fields and the required flags on the `Deviation`, `DeviationRequest` and `DeviationOutcome` elements only | TSD S8 T3.1, T-A.2; context pack ownership rows (table `deviation`) | AC2; TC-S8-E7009-CON-02 |
| BR2 | The match record is declared as an element written before the answer, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S8 T2; legacy AC1 and AC2 | AC5; TC-S8-E7009-CON-04 |
| BR3 | The contact stays with rwb-source-data: the contract declares the contact read as consumed, declares no contact value, no contact property and no `v_ace_*` property, and describes no write to a P1 table | DP-05, DP-18; context pack connection matrix row S8; ASM-5213 | AC3; TC-S8-E7009-CON-03 |
| BR4 | The package is rwb-decision's: the contract declares the package read as consumed and declares no rule row, no threshold and no rule ID as a property set | ASM-5214 | AC3; TC-S8-E7009-CON-03 |
| BR5 | No event of this step is declared: EV-06 and EV-07 are the raise and clearance stories' and the outbox library of DP-09 is recorded as an absent H row | ASM-5215; Event and Messaging Design v5; TSD S8 T5.3 | AC7; TC-S8-E7009-CON-05 |
| BR6 | API-S8-001 declares the `Idempotency-Key` and stores its answer; API-S8-002 declares it not applicable, so a repeat is matched on the deviation and complaint references | TSD S8 T-A.2 | AC1; TC-S8-E7009-CON-01 |
| BR7 | The complaint reference, the contact reference and the match outcome are declared as the match's own and carry a placeholder, because no source publishes a name, a format or a value set | ASM-5212; FSD S8 A2.18.3.2; TSD S8 T3.1, T3.2 | AC2; TC-S8-E7009-CON-02 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, a code, dates, a reference and a package version only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S8 T6.2 | AC6; TC-S8-E7009-CON-04 |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 | AC7; TC-S8-E7009-CON-05 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) | AC2; TC-S8-E7009-CON-02 |
| BR11 | The document lists only operations owned by rwb-deviation; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 | AC1; TC-S8-E7009-CON-01 |
| BR12 | The match is a branch of the one published deviation-outcome operation and not a second path; the outcome branch of the same operation is named as the clearance stories' | TSD S8 T-A.1; ASM-5211 | AC1; TC-S8-E7009-CON-01 |
| BR13 | The rights of the match are the case-record right the permission table gives: U, held by the eight legacy roles and by RW-DEBTSALE, RW-GUARANT, SY-CASEWF and SY-DATALOAD | TSD S8 T6.1, T-A.1; legacy permission table of RWB-E7-009; ASM-5216, ASM-5208 | AC4; TC-S8-E7009-CON-03 |
| BR14 | The states `DEV_WITH_OWNER` and `DEV_RESOLVED` are declared as the vocabulary of the answer and of the DEV machine, and move no deviation | ASM-5212; TSD S8 T4; Business Rules and Routing Logic v4 row R-DEV-09 | AC2; TC-S8-E7009-CON-02 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operations, the elements, the match properties, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the other deviation stories that share the two operations, SCR-08, the wave 4 harness and the owners of rwb-source-data, rwb-decision, rwb-case and rwb-access accept the document and the fakes | Baselined |
| Baselined | The match references and the outcome set are confirmed | The business lead replaces the placeholders inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional match note | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a reference becomes an enumeration over an unconfirmed set | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a contact value, a second path, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's: `DEV_WITH_OWNER` and `DEV_RESOLVED` are states of the DEV machine of TSD S8 T4 and the States sheet of the Business Rules and Routing Logic v4, `DEV_FLAGGED` is the raise stories' start state, R-DEV-18 resumes the clock on clearance, and the match moves no state of its own. This baseline fixes the vocabulary and the answer shape and moves no deviation.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-deviation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the confirmed match references and outcome set, and the correction of the plan rows the baseline consumes, including the two consumed rows and the absent DP-04, DP-05, DP-09 and DP-18 rows |
| Business lead | Confirms the names, the formats and the outcome set of the match that replace the placeholders |
| Consuming teams (the app story, the other deviation stories, SCR-08, the wave 4 harness and the owners of rwb-source-data, rwb-decision, rwb-case and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field and no contact value is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-deviation login (DP-02)" and is not part of this baseline.

The rwb-access authorise check is DP-08; its operation name is Not specified in the source documents (DOR-RWB-S8-E7009-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Deviation element | The ten columns of DF-CAS-036 to DF-CAS-045: `id`, `caseId`, `deviationCode`, `raisedAt`, `raisedBy`, `pausedState`, `handlerUserId`, `contactStop`, `clearedAt` and `outcome` | BR1 |
| Raise element | `DeviationRequest`: `deviationCode`, `reason` and `documentIds`, with no match property | BR1 |
| Outcome element | `DeviationOutcome`: `outcome`, `note` and the optional complaint reference and contact reference of the match | BR7; BR12 |
| Required flags | `id`, `caseId`, `deviationCode`, `raisedAt`, `raisedBy`, `pausedState` and `contactStop` on the deviation element, and `id` is read-only as the API Specification v5 gives it; the other properties optional | BR1; BR10 |
| Lists | LOV-DEVIATION X1 to X7, LOV-RAISED-BY SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, and LOV-DEV-OUTCOME RETURNED, RE_ROUTED and CASE_ENDED, copied from TSD S8 T3.2 and published unchanged. The reference-data contract is DP-06 and DP-07; the parameters they read are Not specified in the source documents (DOR-RWB-S8-E7009-CON-20) | BR14 |
| Event data | None of this step: no event is declared (§12.3) | BR5 |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the answer (DP-03) | BR2 |
| Case, timer and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` and DF-WRK-027 to DF-WRK-036 of `timer` in P3, and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here | BR3; BR4 |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view and the contact points (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8) | BR3; BR4; BR9 |
| Consumed fields with no source | The operation names of the contact read and the package read, the names and formats of the two references and the match outcome set: Not specified in the source documents (GAP-3069; ASM-5212, ASM-5213, ASM-5214) | BR3; BR4; BR7 |

The field-level types, lengths and required flags of the added element properties are settled in the baseline review; this story fixes the element names, the required flags of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/deviations/{deviationId}` (API-S8-002) | `DeviationOutcome` in, `Deviation` of status 200 out, carrying the state `DEV_WITH_OWNER`, the outcome and the decision-record reference of the match | Case record, right U, scope applied | Not applicable |
| POST | `/cases/{caseId}/deviations` (API-S8-001) | `DeviationRequest` in, `Deviation` out, carrying the code, the raise source and the contact stop; declared here and built by the raise stories of the module | Case record, right U, scope applied | `Idempotency-Key` header |

API-S8-002 answers 400, 401, 403 with MSG-P4-002, 404 for a deviation that is not on the case, 409 for a deviation that is not an open X1, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The paths, the operation IDs, the element names, the rights and the error codes are published in TSD S8 T-A.1 and T-A.2; the match properties and the outcome set carry the placeholder (GAP-3069; ASM-5211, ASM-5212). The outcome branch of the same operation, the screening and the breach path belong to other stories of the module and none of them is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The contact read (operation name Not specified in the source documents (GAP-3069; ASM-5213)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The contact point of the case party with its channel, its time and the interaction it belongs to; the ledger is P1's by the default ruling; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3069; ASM-5214)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEV package at its version, with R-DEV-01 to R-DEV-22 over 9 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The two rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3069; ASM-5213, ASM-5214).

#### 12.3 Events published

None. The service owns the topic `rwb.deviation.events.v1` and its event set carries EV-06 `DeviationRaised` (`caseId`, `deviationCode`, `raisedBy`, consumed by Timers and Communications for the contact stop) and EV-07 `DeviationCleared` (`caseId`, `deviationCode`, `outcome`, consumed by Timers and Communications), both belonging to the raise and clearance steps of the stage (Event and Messaging Design v5; TSD S8 T5.3). A match changes no deviation state and lifts no stop, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays the events is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5215).

#### 12.4 Events consumed

None. The service listens to rwb-case events on the connection matrix's column P3 (context pack connection matrix, row S8: events from P3, REST and events to P1, Temporal and events to P10), and none of them belongs to the match: the trigger is the officer's confirmation on SCR-08, and the FSD declares no background event for the feature (FSD S8 A2.18.4.4). This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per deviation, can start at any time on a case, continues-as-new with the case stage | `rwb-deviation` | The stage that hosts the match step; its signals and its outcome for the parent are declared, not built. The Workflow ID form and the duplicate-start policy are Not specified in the source documents (CG-ALL-11674) |
| `recordComplaintMatch` | Activity, the one match step of the stage | `rwb-deviation` | The deviation reference, the complaint reference, the contact reference and the package version in; the record reference and the match outcome out |

No child workflow for the case and none for the money exists in this service, and the service owns one workflow and no job in the context pack's ownership rows. The activity name is a target design choice, and the step runs from the officer's confirmation. No activity is registered by this story.

#### 12.6 Schedules

None. The match is an officer-driven step; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The service's job list is empty in the context pack's ownership rows, and the escalation timer of R-DEV-20 and the screening run are other stories'.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | The deviation X1 to X7 of a case, its code, its raise facts, its handler, its stop and its outcome; the table the answer element is drawn from and the row a match does not change |
| decision_record | PLT library, created in `rwb_deviation` | The local hash-linked decision record of the match (DP-03) |
| idempotency_key | PLT library, created in `rwb_deviation` | The key of the raise operation and the answer it holds; the match declares none |
| outbox_event | PLT library, created in `rwb_deviation` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view and the contact points (P1), `document` (P5), `notice` (P6) and `payment` (P8) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data contact fake | The contact record of the preceding interaction for the case party, and a case with no such contact | AC1, AC3, AC6 |
| rwb-decision rule-package fake | The DEV package at its version in force with R-DEV-01 to R-DEV-22 over 9 states | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-08 answer for the deviation of `RW-2026-000502`, before and after the match | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the contact read and the package read carry the placeholder until their owners confirm them (GAP-3069; ASM-5213, ASM-5214).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | API-S8-001 and API-S8-002 on `/api/recovery/deviation/v1`; the contact read and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; EV-06 and EV-07 are the raise and clearance stories', and the decision record is the library's on `rwb.decision-record.v1` and not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `DeviationWorkflow` and `recordComplaintMatch` on `rwb-deviation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no deviation and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and four fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the match is answered. DP-13 moves the base of the legacy paths and gives the deviation-outcome operation its home. DP-19 sits behind SCR-08, whose screen model is the edge contract's. DP-04, DP-05, DP-09 and DP-18 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the contact as another service's data and never a view, the outbox as an absent library row rather than an event of this step, and the ledger as P1's by the default ruling (GAP-3069; ASM-5213, ASM-5214, ASM-5215).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, and the Drools kit rows `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON` that a rule evaluation would add. The two consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the match branch of API-S8-002 and validate the additive rule of AC1 in the pipeline.
2. Write the `Deviation` element with its ten properties and seven required flags, the `DeviationRequest` element and the lists of AC2.
3. Write the `DeviationOutcome` element with the match properties and their placeholders.
4. Record the contact row and the package row of AC3 with their owner, their budget and their placeholders.
5. Record the rights and the error envelope of AC4.
6. Record the decision-record element of AC5 and validate it against the library schema.
7. Publish the four fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-deviation-v1.yaml`, the three elements, the contract README rows for the two consumed rows and their placeholders, and the four fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the eleven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the other deviation stories, SCR-08 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | The contract describes the raised state from which the match is taken, raised by the raise story of the module and not by this operation | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required field of a request is absent or invalid, a match reference among them, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the case record right U the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the match is answered | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-08 Deviation queue in its list state, before and after the match, through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviation, its handler and the recorded match, and rwb-case for the case and its route state; this baseline fixes the rwb-deviation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives SCR-08 "Loading; list" and SCR-06 Raise deviation "Form; saved": the raise form is the raise stories' and neither screen is described as a matching screen, so the place of the match action on SCR-08 is Not specified in the source documents (GAP-3069; ASM-5211). The refusal, not-a-complaint, no-contact and not-recorded states read the messages of section 14 on the same route. The states of SCR-08 are loading and list in the legacy table; its empty, error and no access states are Not specified in the source documents (CG-ALL-11678). The states of SCR-06 empty, loading, error and no access are Not specified in the source documents (CG-ALL-11677).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-009-01 | AC1, AC3 | Contract | The open X1 deviation of `RW-2026-000502` on the fake; the contract half answers the operation, the contact row and the package row |
| TC-E7-009-02 | AC2, AC5 | Contract | The deviation element and the outcome request; the contract half answers the ten properties, the lists, the match placeholders and the decision element |
| TC-E7-009-03 | AC4 | Contract | A role without the right U and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E7-009-04 | AC5, AC7 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S8-E7009-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the match branch, the `Idempotency-Key` rule and the seven error answers are present |
| TC-S8-E7009-CON-02 | AC2 | Contract | The three elements validate with their ten, three and four properties, the seven required flags, the three lists and the match placeholders |
| TC-S8-E7009-CON-03 | AC3, AC4 | Contract | The two consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case`, no-contact-value and no-rule-row boundary; the rights |
| TC-S8-E7009-CON-04 | AC5, AC6 | Contract | The decision-record element matches the library schema; the four fakes match the document and a drifted fake fails the build |
| TC-S8-E7009-CON-05 | AC7 | Contract | The naming baseline, the tables owned and the absence of a published event, a consumed event, a second topic and a Schedule |
| TC-S8-E7009-CON-06 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-S8-E7009-CON-AC8) |
| TC-S8-E7009-CON-07 | AC7 | Contract | Boundary of the four tables of §12.7 (deviation, decision_record, idempotency_key, outbox_event) with no foreign key out of the schema (DP-01) |

The four legacy cases are those of RWB-E7-009 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S8-E7009-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The seven cases `TC-S8-E7009-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the match condition, the deviation code, the states, the right, the match outcome set and the package version stay rule rows and reference data, never a schema default, an enumeration member or a constant of the code.
- No personal data and no contact value in a schema, an example or a fake: identifiers, a code, dates, a reference and a package version only, and every example is synthetic.
- The contact stays with rwb-source-data: the document declares no contact value property, no `v_ace_*` path, no `v_ace_*` property and no ACE table read (BR3).
- The case stays with rwb-case: the document declares no `recovery_case` property, no case row write and no case state write.
- The rule rows stay with rwb-decision: the document declares no rule row, no threshold and no rule ID set.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-deviation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule or a Quartz row.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-DVF-09 | The requirement this feature serves is Not specified in the source documents (GAP-3069; ASM-5217): TSD S8 T8 maps every REQ-DVH and REQ-S8 row to FEAT-DVH-01, FEAT-DVF-01 or a placeholder | The match branch of API-S8-002, the three elements and the two consumed rows | TC-E7-009-01, TC-E7-009-02, TC-S8-E7009-CON-01, TC-S8-E7009-CON-02 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-S8-E7009-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as a later story's | TC-S8-E7009-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-S8-E7009-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S8-E7009-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-009, disposition Split (rework); feature FEAT-DVF-09 |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S8-E7009-APP; this baseline copies none of them |
| Source text | Legacy RWB-E7-009; FSD S8 Deviation handling v3 A2.18, A2.18.2, A2.18.3 and A2.18.4; TSD S8 Deviation handling v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; API Specification v5 elements Deviation, DeviationRequest and DeviationOutcome; Business Rules and Routing Logic v4 row R-DEV-09 |
| Test cases | The four legacy cases as the contract half, and the five new contract cases TC-S8-E7009-CON-01 to -05 |
| Feature and screens | FEAT-DVF-09, SCR-08 Deviation queue |
| Rules | R-DEV-01 to R-DEV-22 governed in rwb-decision; no row expresses the match (ASM-5214) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the match branch, the evaluation, the decision record and the answer: RWB-S8-E7009-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3). The contact points, the interaction ledger and EFS: rwb-source-data (P1), whose rows this baseline declares as consumed and faked (ASM-5213).
- The authoring, testing, approval and versioning of the DEV package and of the rule rows: rwb-decision (P7) (ASM-5214).
- The names, the formats and the outcome set of the match references: the business lead confirms them at the baseline review and the placeholder stands until then (GAP-3069; ASM-5212).
- The outcome branch of the same operation and the clearance of the deviation: the clearance stories of the module.
- The screening that proposes X1 and the L1 agent: the E1 and E2 stories of the module. The raise operation's behaviour: RWB-S8-E7001-APP to RWB-S8-E7007-APP.
- The override review: RWB-S8-E7008-APP. The breach path of a contact sent while a block is on: RWB-S8-E7010-APP.
- The gateway-bff composite route and the screen field list of SCR-08: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
