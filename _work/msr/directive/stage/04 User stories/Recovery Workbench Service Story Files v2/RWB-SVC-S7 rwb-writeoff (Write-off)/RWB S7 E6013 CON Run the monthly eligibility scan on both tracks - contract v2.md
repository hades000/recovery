# RWB-S7-E6013-CON Run the monthly eligibility scan on both tracks - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Contract version | `/api/recovery/writeoff/v1` (path version v1); the document version is Not specified in the source documents (DOR-RWB-S7-E6013-CON-23) |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S7-E6013-CON-16) |
| Depends on (build) | None |
| Contract dependencies | The four consumed rows of AC3 (rwb-case and rwb-source-data; see section 13) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the monthly scan of rwb-writeoff, split from RWB-E6-013. It fixes the one scan operation on `/api/recovery/writeoff/v1` (DP-13), the `ScanRequest` and `WriteOffScan` elements, the `WriteOff` element with the field IDs DF-FIN-010 to DF-FIN-020 and their required list, the consumed rows of the rwb-case case list and case-move answer, the rwb-source-data batch-status and balance reads, the rwb-decision package read, the decision-record element of DP-03, the rights of TSD S7 T6.1, the fakes and the absence tests. TSD S7 T3.2 publishes no list of values and the service owns no scan table, and DP-04, DP-05, DP-09 and DP-10 are not in the plan's pattern set although the step evaluates a package, reads ACE facts, consumes an event and runs from a Schedule. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S7-E6013-CON-L278, X20 RWB-S7-E6013-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 7 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Tribe lead and squad members (RW-TRIBE)**, I want **the published contract baseline of the monthly scan of rwb-writeoff — the scan operation on `/api/recovery/writeoff/v1`, the request and answer elements, the `WriteOff` element, the four consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-27 and the wave 4 harness build against one fixed, testable contract on Day 1, and a property, a consumed row or an answer shape can never drift between rwb-writeoff, rwb-case, rwb-source-data and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy scan of RWB-E6-013 crossed four boundaries at once: the case list, the ACE batch status and balances, the rule version and a screen. The target splits them: rwb-case owns the case and its route states, rwb-source-data owns the ACE batch status and the balances, rwb-decision owns the WO package, and rwb-writeoff owns the write-off row and the run of a cut-off date. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the properties of the request and the answer, the eleven properties of `WriteOff` with their required list, the case-list and case-move rows, the batch-status and balance rows, the package row and the record of the decision.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition and the ACE facts are consumed on the owner's contract only (ASM-5004). No ACE view and no ACE table is read by this service: the FSD field names are carried as the source field names that the rwb-source-data contract returns, and the contract fields and the freshness response are confirmed with P1 before the wave 4 system test (GAP-1792).

Three points are carried as gaps and assumptions rather than decided quietly: the plan's C row is None while the step consumes four rows, and DP-04 is absent from the pattern set although the WO package is evaluated (ASM-5004, ASM-5005); the ACE data-ready event the step consumes needs the inbox of DP-09 and the JOB-16 Schedule needs the kit of DP-10, and neither row is in the plan (ASM-5006, ASM-5008); and no table or list of values publishes the scan's own answer or the write-off state vocabulary (ASM-5009).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `write_off` is S7's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `proceeds` is P8's. This document never declares another service's table or operation as its own.
- The rwb-case case-list row and case-move answer, the rwb-source-data batch-status and balance rows and the rwb-decision package row are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3017; ASM-5004).
- The outbox and inbox library of DP-09 is the platform dependency of the service's topic and of the consumed ACE data-ready event; the plan's H row for this key does not carry it (ASM-5006).
- The workflow kit's Scheduled job template of DP-10 is the platform dependency of the JOB-16 Schedule; the plan's H row does not carry it either (ASM-5008).
- The WO package and its rows for R-WO-01 to R-WO-04 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-writeoff for this step: the scan operation with its request and answer elements, its rights and its error responses.
2. Fix the `ScanRequest` and `WriteOffScan` elements: `cutOffDate` and `taxCriteriaVersion` in, `id`, `cutOffDate`, `eligible`, `heldOut` and `status` out, as API Specification v5 and TSD S7 T-A.2 publish them, with the requiredness the sources do not give.
3. Fix the `WriteOff` element: the eleven properties of DF-FIN-010 to DF-FIN-020, their types, their lengths and the required list API Specification v5 publishes.
4. Fix the consumed rows: the case-list read and the case-move answer of rwb-case, the batch-status and balance reads of rwb-source-data, and the package read of rwb-decision, marking with the placeholder what the sources do not give.
5. Record the decision-record element of DP-03, written before the rows change.
6. Record the rights of the operation, the naming baseline, the Schedule that triggers the run and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the absence of a published event.
9. Tag the baseline and hand it to RWB-S7-E6013-APP, SCR-27 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC4 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC5 |
| X5 | A property is declared that the sources do not publish, for example a scan row, a state list or a tax threshold | The review fails the baseline and the absence test fails the build | None | AC2, AC5, AC7 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event of this step or a second topic | The absence test fails the build | None | AC7 |
| X8 | The rights of the operation are not the ones TSD S7 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices and the published owner contracts of rwb-case, rwb-source-data and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operation, the base, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S7-E6013-APP, SCR-27 and the wave 4 harness on Day 1, and the rwb-case, rwb-source-data and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and ten contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the monthly scan of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case is P3, of every v_ace_* view is P1 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The scan operation is declared on the writeoff base with its shapes and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /write-off-scans with a ScanRequest body in and a WriteOffScan answer of status 201, under the base /api/recovery/writeoff/v1 and owned by rwb-writeoff
    Then the create declares the Idempotency-Key header and the repeated key answering the run it created, and declares no path parameter
    Then the answers 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition, as TSD S7 T-A.2 gives the error set of API-S7-001
    Then no operation of the committee decision, the pack, the posting or the post charge-off sale is declared by this document

  Scenario: AC2 The request, answer and write-off elements are fixed and no list of values is invented (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with API Specification v5, TSD S7 T3.1 and T3.2
    Then the ScanRequest element declares cutOffDate of format date and taxCriteriaVersion of type string, and nothing else
    Then the WriteOffScan element declares id of format uuid, cutOffDate of format date, eligible and heldOut of type integer and status of type string, and nothing else
    Then the WriteOff element declares the eleven properties of DF-FIN-010 to DF-FIN-020: id, caseId, decisionLogId, amount, taxCriteriaMet, committeeDate, postedDate, responsibilityCenter, costCenter, glProduct and recoveredAfter
    Then the required list of the WriteOff element is the one API Specification v5 publishes: id, caseId, amount, taxCriteriaMet and recoveredAfter
    Then responsibilityCenter, costCenter and glProduct keep their maximum length of 10
    Then the document declares no enumeration, because TSD S7 T3.2 publishes no list of values, and the missing vocabulary is carried as a gap (GAP-3017; ASM-5009)
    Then no property is added for a scan row, a held-out reason, a balance, a rule row or a tax threshold

  Scenario: AC3 The consumed rows of rwb-case and rwb-source-data are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case-list read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the account link, the case state and the balance key
    Then the case-move answer is declared as consumed from P3 rwb-case, with the move POPULATION_PROPOSED or SCAN_HELD carrying the rule ID and its version
    Then the ACE batch status is declared as consumed from P1 rwb-source-data, with the source ALS, the status and the business date, and the balance with the as-of date of the product
    Then the operation names of the two case rows and the two source-data rows are Not specified in the source documents (GAP-3017; ASM-5004, ASM-4888) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property and no grant on any rwb_* schema of another owner, including v_ace_batch_status
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rwb-decision row, the rights and the error envelope are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with rwb-decision as the owner of the rule rows and with TSD S7 T-A.1 and T6.1
    Then the package read is declared as consumed from P7 rwb-decision, with the WO package, its version, its 51 rules over 27 states, the tax criteria and the reference data of the two tracks, and its operation name is Not specified in the source documents (GAP-3017; ASM-5005)
    Then the document declares no rule row, no threshold and no tax criterion as a property, and the criteria are read from the package
    Then the operation declares the capability area Write-off and posting with right C and the scope applied
    Then RW-WRITEOFF holds CRU and RW-CREDITAD holds CRUA on the capability area, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA, and every other role and every SY-* service identity of TSD S7 T6.1 holds R
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and the scan answer has no table (new, D-RCV-60)
    Given the decision and data sections of the baseline
    When they are compared with the library schema, TSD S7 T3.1 and the ownership rows of S7
    Then one decision record is declared per rule outcome with the case reference, the write-off reference, the rule ID, the package version in force, the inputs reference with the business date of the batch and the as-of date of the balance, the cut-off date, the outcome, the case move and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the write_off rows change, and a failed write leaves them unchanged with MSG-P7-003
    Then the record carries no rule row, no threshold as a literal and no personal data
    Then the answer properties id, eligible, heldOut and status are declared as answered from the run and its rows, because write_off carries no cut-off date and no scan reference and S7 owns one table only (ASM-5009)
    Then the absent scan table is named as a gap and the document declares no table of this service beyond write_off, decision_record, idempotency_key and outbox_event

  Scenario: AC6 The seven fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case-list fake answers the case list of the stage with 210 cases in SCAN_DUE, a case that has left the list and the two moves accepted and refused
    Then the rwb-source-data fakes answer the batch status of source ALS as COMPLETED with its business date, an absent load, a load for another source, and the balance of the 210 cases with as-of date "2026-11-30" and a stale product
    Then the rwb-decision fake answers the WO package at its version with R-WO-01 to R-WO-04 and the tax criteria version published and absent
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 answer
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline, the trigger and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and are consumed only through their contracts
    Then the trigger is declared as the JOB-16 Temporal Schedule monthly on the third working day and as the ACE data-ready event of rwb-source-data for source ALS, and nothing is registered by this story
    Then the document declares no event published by this step and no second topic, and it names WriteOffApproved (EV-24) as the approval story's
    Then the absence test fails a build that adds a published event, a second topic, a Schedule registration, a v_ace_* read or a scan table (ASM-5006, ASM-5008, ASM-5009)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6013-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word. The two tracks the legacy AC2 names are not re-defined here: the element section declares no per-track property and the two tracks stay rule facts of the WO package (ASM-5007).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The population is rwb-writeoff's, and the contract declares the fields, the required list and the optionality of the `WriteOff` element only | TSD S7 T3.1; API Specification v5, `WriteOff`; context pack ownership row (table `write_off`) |
| BR2 | The decision record is declared as an element written before the rows change, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy AC1 and AC3 |
| BR3 | The ACE batch status and the balances stay with rwb-source-data: the contract declares the reads as consumed, declares no `v_ace_*` property and describes no ACE table read | DP-05 as a prohibition; FSD S7 A2.1.2; ASM-5004 |
| BR4 | The case list and the case move are consumed and not written: the contract declares the two rows and declares no `recovery_case` property and no case row write | ASM-4888; TSD S7 T4 |
| BR5 | No event of this step is declared: `WriteOffApproved` (EV-24) is the approval story's, and the outbox and inbox library of DP-09 is recorded as an absent H row | ASM-5006; TSD S7 T5.3 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; no other operation is declared on this base by this story | TSD S7 T-A.2 |
| BR7 | No list of values is published for this module, so the document declares no enumeration and no state value as a constant | TSD S7 T3.2 (empty); ASM-5009 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, a state and a rule version only | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR11 | The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR12 | The rule rows of R-WO-01 to R-WO-04, the tax criteria and the two tracks are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; FSD S7 A2.1.3.1; ASM-5005, ASM-5007 |
| BR13 | The trigger is declared and not registered: the JOB-16 Temporal Schedule in rwb-writeoff on the 3rd working day, which also tests the ACE batch-complete condition, and the ACE data-ready event are named as the run's trigger, and this story creates neither; no Quartz table, connection or job is used | Batch and Scheduling Design v5, JOB-16; ASM-5006, ASM-5008; GAP-1801 |

**Coverage.** BR1 to BR13 have no criterion and no test in this story; the mapping to acceptance criteria and §16 test cases is Not applied until a new AC8 is added in section 7 with its §16 row (NEWAC-RWB-S7-E6013-CON-AC8).

### 9. State transitions

The lifecycle of this document, not of a write-off:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the three elements, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-27, the wave 4 harness and the owners of rwb-case, rwb-source-data and rwb-decision accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional answer field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the required list changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC5 and AC7 fail: a scan table, a state list, a `v_ace_*` view, a `recovery_case` property or a published event | In review |

The state machine the document describes is the app story's and rwb-case's: `SCAN_DUE`, `POPULATION_PROPOSED` and `SCAN_HELD` are route states of rwb-case (TSD S7 T4). This baseline fixes the vocabulary of the request and the answer and moves no case and no row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the four consumed rows, the absent DP-04 and DP-05 rows, the absent DP-09 inbox and the absent DP-10 schedule kit |
| Consuming teams (the app story, SCR-27, the wave 4 harness and the owners of rwb-case, rwb-source-data, rwb-decision, rwb-access and rwb-document) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library, the outbox and inbox library and the Scheduled job template this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

Each operation's authorisation is checked through the rwb-access authorise check (DP-08); the rights named in AC4 are those of TSD S7 T6.1 and are not re-declared here.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Request element | `cutOffDate` of format date and `taxCriteriaVersion` of type string, as API Specification v5 and TSD S7 T-A.2 publish them | Not specified in the source documents (DOR-RWB-S7-E6013-CON-7) |
| Answer element | `id` of format uuid, `cutOffDate` of format date, `eligible` and `heldOut` of type integer and `status` of type string | Not specified in the source documents (DOR-RWB-S7-E6013-CON-7) |
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `caseId`, `decisionLogId`, `amount`, `taxCriteriaMet`, `committeeDate`, `postedDate`, `responsibilityCenter`, `costCenter`, `glProduct` and `recoveredAfter` | DF-FIN-010 to DF-FIN-020 |
| Required list | `id`, `caseId`, `amount`, `taxCriteriaMet` and `recoveredAfter`, as API Specification v5 publishes them; the request and the answer publish no required list, so the baseline copies them as the source gives them | Not specified in the source documents (DOR-RWB-S7-E6013-CON-7) |
| Lengths | `responsibilityCenter`, `costCenter` and `glProduct` at a maximum length of 10, as the source gives them | Not specified in the source documents (DOR-RWB-S7-E6013-CON-7) |
| Lists | None: TSD S7 T3.2 publishes no list of values for this module (ASM-5009) | Not specified in the source documents (DOR-RWB-S7-E6013-CON-7) |
| Personal data | None: no field of this section is personal data (BR8) | Not specified in the source documents (DOR-RWB-S7-E6013-CON-11) |
| Parameters and reference data | The rule-package version and the tax criteria version, read from rwb-decision as reference data under DP-06 and DP-07; no parameter is declared here | Not specified in the source documents (DOR-RWB-S7-E6013-CON-20) |
| Event data | None of this step: no event is declared (§12.3) | Not specified in the source documents (DOR-RWB-S7-E6013-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the rows change (DP-03) | DF-DEC-001 to DF-DEC-018 |
| Case, batch and balance facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3, the ALS batch status and the balance of the P1 product, read only through the rwb-source-data reads faked in §12.8 and never written, copied or joined here | DF-CAS-001 to DF-CAS-023 |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), a scan table and the later stories' data | Not specified in the source documents (DOR-RWB-S7-E6013-CON-7) |
| Consumed fields with no source | The operation names of the four consumed rows and the field IDs of the ACE batch status: Not specified in the source documents (GAP-3017; ASM-5004, ASM-4888) | Not specified in the source documents (DOR-RWB-S7-E6013-CON-7) |

The field-level types of the added elements are settled in the baseline review; this story fixes the property names, the required list and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-off-scans` | ScanRequest in, WriteOffScan of status 201 out, the run of the cut-off date with its eligible and held-out counts (API-S7-001) | Write-off and posting, right C, scope applied | `Idempotency-Key` header |

The operation answers 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14, as TSD S7 T-A.2 gives the error set of API-S7-001. `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) is RWB-S7-E6018-APP's and is not declared here.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case-list read of the write-off stage (operation name Not specified in the source documents (GAP-3017; ASM-5004)) | `/api/recovery/case/v1` | P3 rwb-case | The open cases of the stage for a cut-off date: case reference, case number, product group, account link, state and balance key; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3017; ASM-4888)) | rwb-case (P3) | P3 rwb-case | The move `POPULATION_PROPOSED` or `SCAN_HELD` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The ACE batch status of source ALS, and the balance of the account (operation names Not specified in the source documents (GAP-3017; ASM-5004)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The status of the ALS load for the cut-off date with its business date, and the balance with the as-of date of the product; faked |
| The WO rule-package read in force (operation name Not specified in the source documents (GAP-3017; ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-01 to R-WO-04 among its 51 rules over 27 states, the tax criteria and the two tracks; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3017; ASM-5004).

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (event `EV-24`, `writeOffId`, `caseId`, `amount`, consumed by posting), which the approval story RWB-S7-E6018-APP publishes when the committee approves; the scan approves nothing. This baseline therefore declares no event published by this step, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that will relay EV-24 is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5006).

#### 12.4 Events consumed

None of this story's own. The step consumes the ACE data-ready event of rwb-source-data for source ALS — the target form of `EV-26 AceDataReady`, whose consumer list in the monolith catalogue names "write-off scan (JOB-16)" — and this baseline declares it as the run's second trigger in §12.6 rather than as a subscription of the operation, with the event name following the naming rule and published in no source document (GAP-3017; ASM-5006). The `ProceedsMatched` subscription that the connection matrix gives row S7 belongs to the post-charge-off recovery story RWB-S7-E6027-APP. The inbox that receives an event is the platform library of DP-09, which the plan's H row does not hold.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case in the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` | The stage that hosts the scan; its input, its signals and its outcome for the parent are declared, not built |
| `runMonthlyScan` | Activity, the one scan step | `rwb-writeoff` | The cut-off date, the case list and the batch status in; the rule ID with its package version, the proposed and held-out cases, the row set and the case moves out |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice. No workflow and no activity is registered by this story. The workflow ID form and the start rule of `WriteOffWorkflow`, including its duplicate-start policy, are Not specified in the source documents (CG-ALL-10848; DOR-RWB-S7-E6013-CON-8). `runMonthlyScan` is not in Temporal Catalog v1, so its name stays a target design choice. The two tracks and the write-off tax criteria are held as one versioned rule package; the scan reports the package version it applied. The criteria and the track names are Not specified in the source documents (GAP-1469). The criteria version is recorded on every account, and the scan opens only on a published version (GAP-1803). The package code and its promotion date are Not specified in the source documents (GAP-1802); the scan and each decision record the package code and rule version, and the criteria and rules are read from that package through the rwb-decision contract. Whether `runMonthlyScan` is a pivot, and the timeout and retry policy of its wait for the ledger acknowledgement, are Not specified in the source documents (GAP-2018). The split of the write-off states from the case state held by rwb-case is an open question with the P3 owner (GAP-1800): the write-off states stay in `WriteOffWorkflow`, the stage publishes its outcome for the parent, and no state has two writers.

#### 12.6 Schedules

One Temporal Schedule is declared as the run's trigger and is not registered here: the target of the legacy job JOB-16, "Monthly, 3rd working day, on the ACE batch-complete record for ALS" (Batch and Scheduling Design v5, JOB-16), firing on queue `rwb-writeoff` in namespace `rwb-recovery` and starting `runMonthlyScan` with the cut-off date. The ACE data-ready event of rwb-source-data for source ALS is declared as the second trigger, because R-WO-01 tests the ALS load. The schedule ID, the hour and the definition of the third working day are Not specified in the source documents (GAP-3017; ASM-5008); the Scheduled job kit of DP-10 would add `RWB-PLT-E1071-CON` and the pattern set does not carry it. This baseline declares no Quartz row, no shared job table and no batch table.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of a case, its fields, its required list and its state column; the table the answer's counts are derived from |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `proceeds` (P8), a scan table and the later stories' data are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01). The absent scan table is declared as a gap: the answer's `id`, `eligible`, `heldOut` and `status` have no column in `write_off` and S7 owns one table only (ASM-5009).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-list fake | The case list of the stage with 210 cases in `SCAN_DUE`, `RC-2026-000701` among them, with the balance key; a case that has left the list | AC1, AC3, AC6 |
| rwb-case case-move fake | The moves `POPULATION_PROPOSED` and `SCAN_HELD` accepted, and a move refused | AC3, AC6 |
| rwb-source-data batch-status fake | The status of the ALS load as `COMPLETED` with its business date, an absent load, a load for another source, and no answer beyond 2 s | AC3, AC6 |
| rwb-source-data balance fake | The balance of the 210 cases with as-of date `2026-11-30`, a stale product with its date, and an unreadable answer | AC3, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-01 to R-WO-04, the tax criteria version published and absent, and the two tracks | AC2, AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000701`, in its scan state | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners confirm them (GAP-3017; ASM-5004, ASM-5005, ASM-4888).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /write-off-scans` on `/api/recovery/writeoff/v1`; the case-list read and move answer, the batch-status and balance reads and the package read; one hop, 2 s |
| Kafka | 0 published, 1 consumed declared as a trigger | No event of this step; the ACE data-ready event of rwb-source-data for source ALS; `WriteOffApproved` (EV-24) is the approval story's |
| Temporal | 1 workflow, 1 activity and 1 Schedule declared, 0 registered | `WriteOffWorkflow`, `runMonthlyScan` and the JOB-16 Schedule on `rwb-writeoff` |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no row, no balance and no package. What it publishes is one OpenAPI 3.1 document, nine contract tables and seven fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the rows change. DP-13 moves the base and nothing else. DP-19 sits behind SCR-27, whose screen model is the edge contract's. DP-04, DP-05, DP-09 and DP-10 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the ACE facts as consumed data products and never views, the inbox as an absent library row, and the Schedule as a declared trigger rather than a registered one (GAP-3017; ASM-5004, ASM-5005, ASM-5006, ASM-5008).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON`, the Drools kit row `RWB-PLT-E1072-CON` and a second Drools kit row whose key is Not specified in the source documents (CG-ALL-10846), and the Scheduled job kit `RWB-PLT-E1071-CON`. The four consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the operation and validate the additive rule of AC1 in the pipeline.
2. Write the `ScanRequest`, `WriteOffScan` and `WriteOff` elements, the required list and the lengths of AC2, with the placeholder where a type is unstated.
3. Record the two rwb-case rows and the two rwb-source-data rows of AC3 with their owner, their budget and their placeholders.
4. Record the rwb-decision row, the rights and the error envelope of AC4.
5. Record the decision-record element of AC5, the answer's derivation from the run and the absent scan table.
6. Publish the seven fakes of AC6 and the drift test.
7. Record the naming baseline, the trigger and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-writeoff-v1.yaml`, the three elements, the contract README rows for the four consumed rows and their placeholders, the declared trigger and the seven fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the ten contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-27 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The contract describes the R-WO-03 hold of the scan, which the app story raises when Finance has not published the tax criteria version | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the rows change | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The incident that R-WO-02 raises on an absent ALS load has no message ID in any source and is not bound to one here (GAP-3017).

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its loading and scan states through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the population, its counts and its state, rwb-case for the case and its route state and rwb-source-data for the batch status and its business date; this baseline fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives the states "Scan; proposed; in committee; approved": the scan state is this step's, the proposed state belongs to RWB-S7-E6015-APP, the in-committee state to RWB-S7-E6017-APP and the approved state to RWB-S7-E6018-APP. The refusal, not-recorded and held states read the messages of section 14 on the same route. The empty, error and no-access states of SCR-27 are Not specified in the source documents (CG-ALL-10854); the loading state is the one named above.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-013-01 | AC1, AC3 | Contract | The 210-case list, the `COMPLETED` ALS load and the balances; the contract half answers the operation, the case-list row and the two source-data rows |
| TC-E6-013-02 | AC2, AC3 | Contract | Case `RC-2026-000701` at `SCAN_DUE`; the contract half answers the three elements and the `POPULATION_PROPOSED` move shape |
| TC-E6-013-03 | AC5, AC7 | Contract | The decision-record stub stopped and an absent scan table; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-E6-013-04 | AC4 | Contract | A role without the Write-off and posting right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 422 of the envelope |
| TC-E6-013-05 | AC4, AC5 | Contract | RW-WRITEOFF holds CRU and RW-CREDITAD holds CRUA; the contract half answers the rights and the decision element |
| TC-S7-E6013-CON-01 | AC1 | Contract | The document validates; the operation, the base, the `Idempotency-Key` and the six error answers are present |
| TC-S7-E6013-CON-02 | AC2 | Contract | `ScanRequest`, `WriteOffScan` and `WriteOff` validate with their properties, the required list, the three lengths and no enumeration |
| TC-S7-E6013-CON-03 | AC3, AC4 | Contract | The four consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case` and no-rule-row boundary |
| TC-S7-E6013-CON-04 | AC5, AC6 | Contract | The decision-record element matches the library schema; the seven fakes match the document and a drifted fake fails the build |
| TC-S7-E6013-CON-05 | AC7 | Contract | The naming baseline, the tables owned, the declared trigger and the absence of a published event, a second topic and a registered Schedule |
| TC-S7-E6013-CON-06 | AC7 | Contract | The tables of §12.7 are the owned tables only; a table or a foreign key out of the schema fails the build |

The five legacy cases are those of RWB-E6-013 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6013-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S7-E6013-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the eligibility condition, the tax criteria, the cut-off date, the third working day, the two tracks and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, a state and a rule version only, and every example is synthetic.
- The batch status and the balances stay with rwb-source-data and the case with rwb-case: the document declares no `v_ace_*` path, no `recovery_case` property, no case row write and no ACE table read (BR3, BR4).
- The money stays with rwb-payment: the document declares no posting, no proceeds and no settlement property.
- The schedule stays declarative: this story registers no Schedule and creates no Quartz row and no job table.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library, the outbox library and the Scheduled job template come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-001 | Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks; the contract fixes the operation, the elements and the consumed rows on which the scan is built (FSD S7 Requirements served); the split plan carries no requirement id for this slice (GAP-3017) | The three elements and the four consumed rows | TC-E6-013-01, TC-E6-013-02, TC-S7-E6013-CON-01, TC-S7-E6013-CON-02, TC-S7-E6013-CON-03 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6013-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as the approval story's | TC-S7-E6013-CON-05 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The JOB-16 Schedule declared as the trigger | TC-S7-E6013-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S7-E6013-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S7-E6013-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-013, disposition Split (rework); feature FEAT-WOF-01 |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S7-E6013-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-013; FSD S7 Write-off and recovery v3 A2.1 and Requirements served; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; API Specification v5, `ScanRequest`, `WriteOffScan` and `WriteOff`; Business Rules and Routing Logic v4 rows R-WO-01 to R-WO-04; Batch and Scheduling Design v5, JOB-16 |
| Test cases | The five legacy cases as the contract half, and the five new contract cases TC-S7-E6013-CON-01 to -05 |
| Feature and screens | FEAT-WOF-01, SCR-27 Write-off proposal |
| Rules | R-WO-01 to R-WO-04, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the operation, the evaluation of R-WO-01 to R-WO-04, the decision record, the `write_off` rows and the case-move answer: RWB-S7-E6013-APP.
- The case of record, its route states, the case list and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-4888).
- The ACE batch status and the balance products: rwb-source-data (P1) (ASM-5004).
- The authoring, testing, approval and versioning of the WO package and of the rule rows: rwb-decision (P7) (ASM-5005).
- The committee decision operation API-S7-002 and `WriteOffApproved` (EV-24): RWB-S7-E6018-APP.
- The per-account tax record (RWB-S7-E6014-APP), the pack (RWB-S7-E6015-APP), the removal (RWB-S7-E6016-APP), the committee routing (RWB-S7-E6017-APP) and the posting to the close (RWB-S7-E6021-APP to RWB-S7-E6025-APP).
- The scan table the answer implies and the list of values TSD S7 T3.2 does not publish: no source gives them (ASM-5009).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
