# RWB-S5-E3022-CON Serve the statutory notice and prove delivery - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3022-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S5-E3022-CON-16) |
| Contract version | v1, the /v1 base of every consumed path in section 12.2 |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the statutory notice step of rwb-asset, split from RWB-E3-022. It fixes the notice element of the stage answer, the notice and dispatch fields the step reads from rwb-comms (API-P6-001 and API-P6-002), the proof-of-delivery row of rwb-source-data, the failed notice task element and the two case moves of rwb-case, the decision-record element of DP-03, the closed lists and the fakes. It claims no REST operation, because the Ownership Map gives this legacy key none, and it publishes no event, because EV-22 `AssetTakenOn` belongs to the take-on stories (`GAP-2853`; `ASM-4722`, `ASM-4723`). The five consumed rows are class C in fact while the plan's C row is None (`GAP-2854`; `ASM-4721`). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3022-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the statutory notice step of rwb-asset — the notice element of the stage answer, the notice request and read rows of rwb-comms, the proof-of-delivery row of rwb-source-data, the case state, the two moves and the failed notice task of rwb-case, the decision-record element, the closed lists and the fakes**, so that **the app story, the notice team, the proof team, the case team and the wave 2 harness build against one fixed, testable contract on Day 1 and a notice field, a delivery status, a task due date or an answer shape can never drift between rwb-asset, rwb-comms, rwb-source-data and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy notice step of RWB-E3-022 crossed four boundaries at once: the officer's screen, the notice and its dispatch, the WIN proof of delivery and the case state. The target splits them, and each boundary becomes a contract another team builds against: rwb-comms owns the notice and its proof fields, rwb-source-data owns the `v_ace_pod` read, rwb-case owns the route states and the task, and rwb-asset owns the step, its decision record and the answer. The baseline must therefore be fixed before the app story starts.

The baseline also fixes the naming that the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset` (Architecture v5 slide 19 notes). It records that rwb-asset holds no `v_ace_pod` and no `v_ace_contact` grant and no grant on `rwb_case` or `rwb_comms` (Architecture v5 slides 29, 37 and 45), so DP-05 is declared as a prohibition.

Three points are carried as gaps and assumptions rather than decided quietly: the notice, the address and the proof have no rwb-asset column, list or operation, because they are P6's and P1's (`GAP-2852`), this legacy key owns no REST operation although the legacy story lists two (`GAP-2853`), and the trigger, the task-creation operation and the confirmed-address field have no published specification (`GAP-2854`).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `notice` is P6's, `recovery_case` and `task` are P3's, `document` is P5's, `asset_sale` and `listing` are S5's, `decision_log_entry` and `rule_row` are P7's, and every `v_ace_*` view is P1's. This document never declares another service's table or operation as its own (`GAP-2852`; `ASM-4720`).
- The rwb-comms notice rows (API-P6-001 and API-P6-002), the rwb-source-data proof read and the rwb-case state and move rows are published with their fakes, so each consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (`GAP-2853`, `GAP-2854`; `ASM-4721`, `ASM-4722`).
- The DISPOSAL rule package and its rule rows for R-DIS-04 and R-DIS-05 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- This baseline declares shapes and creates no table, no column and no migration; the library objects `decision_record` and `idempotency_key` arrive with the platform library's migration in `rwb_asset` (DP-03).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive document of rwb-asset for this step: the notice element of the stage answer, its states, its rule inputs and its error set, with no operation of its own.
2. Fix the notice request and read rows of rwb-comms, with the notice type, the sent date, the barcode, the delivery status and the `Idempotency-Key`, and mark the fields the sources do not give with the placeholder.
3. Fix the rwb-source-data proof row with its ten fields and its freshness stamp, and mark it as the only home of the WIN proof.
4. Fix the rwb-case rows: the case state read, the two moves and the failed notice task element with its due date.
5. Record the decision-record element of DP-03, written before the answer leaves the service.
6. Record the closed vocabulary of the notice, delivery-status and sent-type lists, the naming baseline and the rule that no value is a constant of the code.
7. Publish the nine tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `notice` write, the drift between a fake and the document, and the absence of an event and of an operation of this key.
9. Tag the baseline and hand it to RWB-S5-E3022-APP, the screens of rwb-comms and rwb-case and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body of a declared element fails schema validation | The build fails on the schema lint; a deployed consumer answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field of the notice element or of a consumed row is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A notice type, delivery status or sent type outside its list appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares a `notice` property of its own, a `v_ace_pod` or `v_ace_contact` path, a `recovery_case` or `task` write, or an operation of this key | The review fails the baseline and the absence test fails the build | None | AC6, AC7 |
| X7 | The document declares a published or consumed event, a topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of the step are not the ones TSD S5 T6.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner documents of rwb-comms, rwb-source-data and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the consumed operations, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S5-E3022-APP, the notice and case screens and the wave 2 harness on Day 1, and the rwb-comms, rwb-source-data and rwb-case teams on the same day |
| Estimable | One additive document, one stage-answer element, nine contract tables, seven fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the statutory notice step of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of notice is P6, of recovery_case and task is P3, of document is P5, of asset_sale and listing is S5 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The notice element of the stage answer is declared with its states and its rule inputs (new, D-RCV-60)
    Given the additive document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 and AsyncAPI 3 schema rules of the platform
    Then it validates with no error and no property of a consumed row is redefined
    Then the stage answer declares the outcome NoticeProved, NoticeFailed or NoticeReserved, the noticeId, the barcode, the delivery status, the callback date, the rule ID with its package version, the case move and the failed notice task request
    Then each outcome names the state of the case the move carries, and no outcome declares an asset field
    Then the element declares no address, no contact value and no person name, and a schema test fails any personal data property
    Then the element is additive within major version 1 and a removal or a rename needs a new major version

  Scenario: AC2 The notice rows of rwb-comms are declared as consumed and the notice stays there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the rwb-comms contract and with TSD P6 T3.1 and T3.2
    Then POST /cases/{caseId}/notices (API-P6-001) is declared as consumed from P6 rwb-comms with the case reference, the notice type of LOV-NOTICE, the addressee role and the Idempotency-Key, answering noticeId, the sent date, the barcode and the dispatch state
    Then GET /notices/{noticeId} (API-P6-002) is declared as consumed from P6 with the dispatch and proof-of-delivery fields it publishes
    Then the document declares no notice table, no notice column and no template property of its own, and the boundary test fails a build that adds one
    Then the call is one hop with a 2 s budget, a breaker and no retry of its own, and the request declares the Idempotency-Key while the read declares none

  Scenario: AC3 The proof-of-delivery row of rwb-source-data is declared and v_ace_pod stays there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the rwb-source-data read and Architecture v5 slides 29, 37 and 45
    Then GET /proof-of-delivery?businessDate= is declared as consumed from P1 rwb-source-data with pod_key, account_key, notice_ref, sent_date, barcode, callback_date, delivery_status, sent_type, source_system and data_as_of
    Then the row records that the freshness stamp and the WIN batch gate are the owner's, and that a stale or gated answer carries no delivery
    Then the document declares no v_ace_pod path, no v_ace_contact path and no grant on any rwb_* schema or ACE view, and the boundary test fails a build that adds one
    Then the matching of the proof row to the notice on notice_ref and barcode is declared with its no-match state

  Scenario: AC4 The rwb-case rows, the two moves and the failed notice task are declared (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with rwb-case as the owner of recovery_case and task and with TSD S5 T4 and T6.1
    Then the case state read is declared as consumed with the case reference and the route state ASSET_PENDING_TAKE_ON or FAILED_NOTICE_QUEUE
    Then the move FAILED_NOTICE_QUEUE and the move ASSET_PENDING_TAKE_ON are declared with the rule ID and its version, and the failed notice task element is declared with the case, the notice reference, the reason and a due date the reference data holds
    Then the operation name of the move and task answer is Not specified in the source documents (GAP-2854; ASM-4721) and the row carries the placeholder
    Then the document declares no recovery_case property, no task property and no write of a case or task row from rwb-asset
    Then a repeated request with the same Idempotency-Key describes no second notice and no second task

  Scenario: AC5 The decision-record element, the rights and the fakes answer the document (new, D-RCV-60)
    Given the decision section, the access section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per notice outcome with the case reference, the noticeId, the barcode, the delivery status, the rule ID, the package version in force, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the answer leaves the service, and a failed write answers MSG-P7-003 with nothing changed
    Then the rwb-comms fake answers the statutory notice, the re-issued notice, a refusal and no answer beyond 2 s; the rwb-source-data fake answers a delivered proof, an undeliverable proof, a stale product, a closed gate and no row
    Then the rwb-case fake answers both states, both accepted moves, a refused move and the created task with its due date; the rwb-decision fake answers the DISPOSAL package at its version, and the decision-record stub answers a healthy and a stopped chain
    Then the rights are declared as Asset and disposal R for the reads and CRUA for the officer's act on the failed notice task, as TSD S5 T6.1 gives them
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None and a reason where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the tables named as owned are the library objects decision_record and idempotency_key, and notice, recovery_case, task, document, decision_log_entry, rule_row, asset_sale, listing and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then 12.1 records None with the reason that this legacy key owns no REST operation, and names GET /assets/{assetId} as API-S5-002 of RWB-S5-E3019-CON and POST /assets/{assetId}/valuations as API-S5-003 of rwb-valuation under ASM-0043
    Then the document declares no operation of another owner as provided

  Scenario: AC7 No event is published or consumed and no Schedule is declared (new, D-RCV-60)
    Given the event and schedule sections of the baseline
    When they are compared with Architecture v5 slide 19 and slide 43 row 22
    Then 12.3 records None and states that EV-22 AssetTakenOn on rwb.asset.events.v1 belongs to the take-on stories and is not published by this step
    Then 12.4 records None and states that JudgmentRecorded, AuctionResult and ProceedsMatched are the service's consumed events and none of them is a notice fact
    Then 12.6 records None and states that the re-appraisal monthly run record belongs to RWB-S5-E3026-APP
    Then the absence test fails a build that adds a producer, a consumer, a second topic, a Quartz row or a Schedule to this step

  Scenario: AC8 Each rule BR1 to BR11 is declared in the document or checked by a guardrail or boundary test (new, D-RCV-60)
    Given the business rules of section 8
    When each rule is compared with the document and with the criterion that covers it
    Then each rule is declared in the document or enforced by a guardrail or boundary test
    Then a rule with no criterion or no test fails the build

  Scenario: AC9 A consumed call that fails or does not answer within its time budget yields no outcome and no write (new, D-RCV-60)
    Given a consumed call of the baseline fails or gives no answer within its time budget
    When the stage answer is built from that call
    Then the answer declares no outcome, no case move and no failed notice task, and the decision record is not written
    Then the call is not retried by this step and the breaker records the failure
```

These nine criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E3022-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The notice element of the stage answer is rwb-asset's and carries references only: `noticeId`, the barcode, the delivery status and the rule version, never a notice field and never an address | Architecture v5 slide 41; TSD S5 T5.2; TSD P6 T3.1; `GAP-2852`; `ASM-4720` |
| BR2 | The decision record is declared as an element written before the answer leaves the service, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S5 T2; legacy RWB-E3-022 AC1 and AC4 |
| BR3 | The WIN proof stays with rwb-source-data: the contract declares the proof row as consumed, and declares no `v_ace_pod` path, no `v_ace_contact` path and no ACE table read of rwb-asset | DP-05; Architecture v5 slides 29, 37 and 45; `GAP-2854` |
| BR4 | The case move, the route states and the failed notice task are declared as answers and not as writes: no `recovery_case` property and no `task` property are declared | Ownership Map (recovery_case and task owner P3); `GAP-2852` |
| BR5 | The notice stays with rwb-comms: the two operations are declared as consumed and faked, and no template, dispatch-file or call-back property is declared here | TSD P6 T3.1 and T3.2; DP-16 for the file |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; TSD S5 T-A.2 |
| BR7 | The vocabulary is closed: `LOV-NOTICE`, `LOV-DELIVERY` and `LOV-SENT-TYPE` are published as the owners' enumerations and no list value is a constant of the code | TSD P6 T3.2; FSD S5 BR-S5-004 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, codes and dates only, and the address of the notice is referenced by its contact key | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR11 | This legacy key declares no REST operation of its own: the document lists the five consumed rows and fixes no operation of this step | Ownership Map; `GAP-2853` |

Coverage of each rule by a criterion and a test case: BR1 by AC1, AC2 with TC-E3-022-01; BR2 by AC2, AC5 with TC-E3-022-04; BR3 by AC2, AC3, AC4 with TC-S5-E3022-CON-02; BR4 by AC2, AC4 with TC-E3-022-02; BR5 by AC1, AC2 with TC-E3-022-01; BR6 by AC2, AC3, AC4 with TC-S5-E3022-CON-02; BR7 by AC5 with TC-S5-E3022-CON-03; BR8 by AC1, AC5 with TC-E3-022-06; BR9 by AC6, AC7 with TC-S5-E3022-CON-04; BR10 by AC5 with TC-S5-E3022-CON-03; BR11 by AC6, AC7 with TC-S5-E3022-CON-04 (DOR-RWB-S5-E3022-CON-4); BR1 to BR11 by AC8 with TC-S5-E3022-CON-06.

### 9. State transitions

The lifecycle of this document, not of a notice:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The stage answer, the five consumed rows, the lists and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the notice and case screens, the wave 2 harness and the rwb-comms, rwb-source-data, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new optional field of the answer or of a fake | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC6 and AC7 fail: a `notice` property, a `v_ace_*` path, a case or task write, an operation of this key, an event or a Schedule | In review |

The notice-serving machine the document describes is the app story's: the case moves from `ASSET_PENDING_TAKE_ON` to `FAILED_NOTICE_QUEUE` under R-DIS-04 and back under R-DIS-05, and this baseline fixes the element and the states and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, the notice and case screens, the wave 2 harness and the owners of rwb-comms, rwb-source-data, rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an element, a consumed row or a fake |

The per-service login behind the security scheme is named "the rwb-asset login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | BR Field ID | Content |
|---|---|---|
| Stage-answer element | BR1 | The outcome NoticeProved, NoticeFailed or NoticeReserved; `noticeId`; the barcode; the delivery status of `LOV-DELIVERY`; the callback date; the rule ID with its package version; the case move; the failed notice task request |
| Failed notice task element | BR4 | The case reference, the notice reference, the reason, the due date that the reference data holds, and the assignee role |
| Notice rows consumed | BR5 | `POST /cases/{caseId}/notices` (API-P6-001) and `GET /notices/{noticeId}` (API-P6-002) of rwb-comms, with the notice type of `LOV-NOTICE` and the dispatch fields P6 publishes |
| Proof row consumed | BR3 | `pod_key`, `account_key`, `notice_ref`, `sent_date`, `barcode`, `callback_date`, `delivery_status`, `sent_type`, `source_system` and `data_as_of` of the rwb-source-data read |
| Case rows consumed | BR4 | The route state and the two moves, and the created task of rwb-case |
| Lists | BR7 | `LOV-NOTICE`, `LOV-DELIVERY` and `LOV-SENT-TYPE`, published as the owners' enumerations and read as reference data at their version; the reference-data contract is DP-06 and DP-07, and the parameters read are Not specified in the source documents (DOR-RWB-S5-E3022-CON-20) |
| Decision record | BR2 | DF-DEC-001 to DF-DEC-018 through the local library, written before the answer leaves the service (DP-03) |
| ACE facts not declared | BR3 | `v_ace_pod` (DF-ACE-251 to DF-ACE-260) and `v_ace_contact` are P1's, read only through the owner's read and never declared, copied or joined here |
| Not declared here | BR4 | `notice` (P6), `recovery_case` and `task` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7), `asset_sale` and `listing` (S5, the sale and pricing stories') |
| Consumed fields with no source | BR11 | The operation name of the case-move and task answer, and the field that carries the confirmed address: Not specified in the source documents (`GAP-2854`; `ASM-4721`) |

The field-level types, lengths and required flags of the declared elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the additive rule of BR10. **No new table, no new column and no new operation** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. This legacy key owns no REST operation. The Ownership Map gives rwb-asset six operations (`GET /assets`, `GET /assets/{assetId}`, `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings`, `POST /listings/{listingId}/rounds`) and none of them is a notice operation, so this baseline declares the stage answer and the consumed rows and claims no path. The two operations the legacy story lists are `GET monolith-base/assets/{assetId}` — API-S5-002, declared on `/api/recovery/asset/v1` by RWB-S5-E3019-CON under DP-13 — and `POST monolith-base/assets/{assetId}/valuations` — API-S5-003, which belongs to rwb-valuation under the Ownership Map ruling ASM-0043. Neither is declared here (`GAP-2853`; `ASM-4722`).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `POST /cases/{caseId}/notices` (API-P6-001) | `/api/recovery/comms/v1` | P6 rwb-comms | The statutory sale notice request: the case reference, the notice type of `LOV-NOTICE`, the addressee role and the `Idempotency-Key`; the answer carries `noticeId`, the sent date, the barcode and the dispatch state; faked |
| `GET /notices/{noticeId}` (API-P6-002) | `/api/recovery/comms/v1` | P6 rwb-comms | The notice with its dispatch and proof-of-delivery fields; faked |
| `GET /proof-of-delivery?businessDate=` | `/api/recovery/source-data/v1` | P1 rwb-source-data | The WIN proof of delivery of the business date with its freshness stamp and its batch gate; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the case reference; faked |
| The case-move answer with the failed notice task request (operation name Not specified in the source documents (`GAP-2854`; `ASM-4721`)) | rwb-case (P3) | P3 rwb-case | The move `FAILED_NOTICE_QUEUE` or `ASSET_PENDING_TAKE_ON` with the rule ID and its version, and the failed notice task with its due date; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as `GAP-2853` and `GAP-2854` with `ASM-4721` and `ASM-4722`.

#### 12.3 Events published

None. EV-22 `AssetTakenOn` on `rwb.asset.events.v1` is the service's catalogue event and is published by the take-on stories (Architecture v5 slide 19 OUT and slide 43 row 22); this step publishes no event, because a notice outcome is a case move and a decision record and changes no asset. A build that declares a producer here fails the absence test of AC7 (`GAP-2853`; `ASM-4723`).

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them is a notice, a proof of delivery or a case state; the step is started by the take-on fact and by the re-issue signal the parent forwards. This baseline declares no consumer group, no subscription and no inbox of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` | The stage that hosts the notice step; its signals and its outcome for the parent are declared, not built |
| `serveStatutoryNotice` | Activity, the one notice step | `rwb-asset` | The case and the notice fact in; the `noticeId`, the barcode, the delivery status, the rule ID with its package version, the case move and the task request out |
| `FailedNoticeTask` | Human task of the workflow kit with an SLA | `rwb-asset` | The task request element of AC4, with its reason and its due date |

No child workflow for the case and none for the notice exists in this service. The step's trigger is the take-on fact of a case in `ASSET_PENDING_TAKE_ON` or the re-issue signal forwarded on task queue `rwb-asset`; the `v_ace_pod` read and the WIN file belong to rwb-source-data (P1) and rwb-comms (P6), and the confirmed address is a contact key of the rwb-comms repository (`GAP-2854`). The activity name and the task name are target design choices; no activity is registered by this story. Workflow ID form: Not specified in the source documents (CG-ALL-9719). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-9719).

#### 12.6 Schedules

None. The step runs from the take-on fact and from the re-issue signal the parent forwards; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the notice outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated notice request and the answer it holds |

`notice` (P6), `recovery_case` and `task` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7), `asset_sale` and `listing` (S5, later stories') and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms notice WireMock | The statutory notice `N-000622` for case `RC-2026-000622` with barcode `RR123456789TH` and sent date 2026-11-20; the re-issued notice `N-000623`; a refusal for a withdrawn template; a 5xx and no answer beyond 2 s | AC2, AC5 |
| rwb-source-data proof WireMock | A delivered proof for `RR123456789TH` with `callback_date` 2026-11-23; an undeliverable proof; a stale product with its date; a closed batch gate; no row for the date; an unreadable answer | AC3, AC5 |
| rwb-case state and move WireMock | The states `ASSET_PENDING_TAKE_ON` and `FAILED_NOTICE_QUEUE`; both accepted moves; a refused move; the created task with its due date | AC4, AC5 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-04 and R-DIS-05 | AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| Platform error-envelope fake | The 400, 401, 403 with MSG-P4-002, 404, 409, 422 and 503 answers of the consumed rows | AC5 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000622` | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation name of the move and task answer is derived from the published documents and carries the placeholder until its owner confirms it (`GAP-2854`; `ASM-4721`).

Every Given and test-data line of section 16 is written against these contract fakes, and the proof data is read only through the rwb-source-data proof WireMock; no criterion or test reads a `v_ace_*` view directly (CG-ALL-9724).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 5 consumed | The notice request and read of rwb-comms, the proof read of rwb-source-data, the case state read and the move and task answer of rwb-case; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 activity and 1 human task declared, 0 registered | `AssetDisposalWorkflow`, `serveStatutoryNotice` and `FailedNoticeTask` on `rwb-asset`; no Schedule |
| File | None | No file element is declared; the WIN registered-mail file is rwb-comms' through the rwb-integration adapter (DP-16) |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no notice, no case, no task and no rule package. What it publishes is one additive document, one stage-answer element, nine contract tables and seven fakes.

**Deliverables.** The additive fragment of `openapi/rwb-asset-v1.yaml` that carries the stage answer, the element descriptions of the five consumed rows in the contract README with their placeholders, the vocabulary of the three lists as the owners' enumerations, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_pod` path, no `v_ace_contact` path and no grant on any other owner's schema, because rwb-asset holds none (`GAP-2854`; `ASM-4724`). DP-13 fixes the base the two legacy endpoints live on and nothing else. DP-19 is behind SCR-21 and SCR-22, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, and this step needs no outbox because it publishes nothing (`ASM-4723`).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. The five consumed rows are C dependencies in fact and not in the metadata row (`GAP-2853`, `GAP-2854`; `ASM-4721`, `ASM-4722`).

**Build steps**

1. Write the stage-answer element and its three outcomes, and validate the additive rule of AC1.
2. Record the two rwb-comms rows of AC2 with their owner, their budget and the `Idempotency-Key` rule.
3. Record the rwb-source-data proof row of AC3 with its ten fields, its freshness stamp, its gate and the no-match state.
4. Record the rwb-case rows of AC4: the state read, the two moves and the failed notice task element with its due date and its placeholder.
5. Record the decision-record element of AC5 and validate it against the library schema.
6. Publish the seven fakes and the drift test.
7. Record the naming baseline and the boundary of AC6, then the absence tests of AC7.
8. Tag the baseline and collect the consumer sign-off.

**Done when.** The document validates in the pipeline, the four new contract tests and the drift test pass, the fakes answer every consumed path, and the app story, the notice and case screens and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the step declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the answer leaves the service | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The WIN proof-of-delivery data product is stale or gated (VR-S5-004-1); the check is rwb-source-data's and this service holds no ACE batch status read | {product} is from {date}. Today's load has not arrived. |

The six message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged, except MSG-P1-001, whose text is copied from Error and Message Standard v4 (`CG-ALL-9721`); no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and the check itself belongs to rwb-source-data (`GAP-2854`; `ASM-4724`).

### 15. Screens and states

The baseline serves no screen of its own. The legacy feature names SCR-21 Asset list and SCR-22 Asset record, both reached through the gateway-bff composite route (DP-19), and neither carries a notice state; the notice and its delivery status are shown by rwb-comms' own screen and the case route state with the failed notice task by rwb-case's worklist. What this baseline fixes is the shape of the element that the composite route reads from rwb-asset for those screens, and the refusal, not-recorded and stale-data states the app story answers with the messages of section 14.

SCR-21 Asset list: loading as Screen Specifications v1 gives it for that screen; its empty, error and no access states: Not specified in the source documents (CG-ALL-9726). SCR-22 Asset record: its empty, loading, error and no access states: Not specified in the source documents (CG-ALL-9727).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-022-01 | AC1, AC2 | Contract | Case `RC-2026-000622` and notice `N-000622`; the contract half answers the stage answer and the notice request and read |
| TC-E3-022-02 | AC2, AC4 | Contract | The `UNDELIVERABLE` proof row; the contract half answers the move shape `FAILED_NOTICE_QUEUE` and the failed notice task element |
| TC-E3-022-03 | AC3, AC4 | Contract | The re-issued notice `N-000623`; the contract half answers the proof row and the move shape `ASSET_PENDING_TAKE_ON` |
| TC-E3-022-04 | AC2, AC5 | Contract | The decision-record stub stopped and a malformed request; the contract half answers the MSG-P7-003 path and the 400 of the envelope |
| TC-E3-022-05 | AC5 | Contract | RW-SALEOFF holds CRUA and a role without the right is refused; the contract half answers the rights and the 403 with MSG-P4-002 |
| TC-E3-022-06 | AC1, AC5 | Contract | A forced failure of the record write and a stale data product; the contract half answers the no-change rule and the absence tests |
| TC-S5-E3022-CON-01 | AC1, AC6 | Contract | The document validates; the stage answer, its three outcomes and the naming baseline are present |
| TC-S5-E3022-CON-02 | AC2, AC3, AC4 | Contract | The five consumed rows and their placeholders; the no-`v_ace_*` and no-`notice` boundary; the `Idempotency-Key` rule |
| TC-S5-E3022-CON-03 | AC5 | Contract | The seven fakes match the document and a drifted fake fails the build; the vocabulary test of the three lists |
| TC-S5-E3022-CON-04 | AC6, AC7 | Contract | 12.1 records None with API-S5-002 and API-S5-003 named as others'; the absence test for an event, a topic and a Schedule |
| TC-S5-E3022-CON-05 | AC5 | Contract | Boundary of the two tables of 12.7, `decision_record` and `idempotency_key`, owned by the library in `rwb_asset`; no other table and no foreign key leaves the schema (DP-01) |
| TC-S5-E3022-CON-06 | AC8 | Contract | The rule table BR1 to BR11; each rule is declared in the document or enforced by a guardrail or boundary test, and a rule with no test fails the build |
| TC-S5-E3022-CON-07 | AC9 | Contract | A consumed call that fails or does not answer within its time budget; the contract half answers the failed-call state with no outcome, case move or task, and no decision record written |

The six legacy cases are the legacy cases of RWB-E3-022 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E3022-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S5-E3022-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the notice types, the delivery statuses, the sent types, the hold reasons, the two-working-day target and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes and dates only, and the address of the notice is referenced by its contact key; every example is synthetic.
- The notice stays with rwb-comms, the proof with rwb-source-data and the case and the task with rwb-case: the document declares no `notice` property, no case or task write, no `v_ace_*` path and no ACE table read (BR3, BR4, BR5).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- This key claims no operation: the document describes the five consumed rows as consumed and faked, never as provided (DP-11; BR11).
- No retired element is reintroduced: the absence tests fail a build that declares a producer, a consumer, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| No requirement id for this feature | The TSD S5 T8 map carries REQ-S5-001 to REQ-S5-005 for FEAT-AST-01 and REQ-S5-006 to REQ-S5-010 for FEAT-AST-08, and none of them covers FEAT-AST-04; REG-20 is the regulatory anchor and REQ-OCC-006 with NFR-044 the constraint (Business Requirements Program v5) (`GAP-2854`; `ASM-4725`) | The stage answer, the five consumed rows and the fakes | TC-E3-022-01, TC-S5-E3022-CON-01, TC-S5-E3022-CON-02 |
| REQ-OCC-006 | Statutory notices continue when a channel consent is withdrawn (NFR-044) | The notice request declares the statutory notice type and no channel suppression | TC-E3-022-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-S5-E3022-CON-02 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and its no-change rule | TC-S5-E3022-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-022, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S5-E3022-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the seven new contract cases TC-S5-E3022-CON-01 to -07 |
| Feature and screens | FEAT-AST-04; SCR-21 Asset list and SCR-22 Asset record as the legacy feature names them, with no notice state declared; the empty, error and no access states of SCR-21 and the empty, loading, error and no access states of SCR-22: Not specified in the source documents (DOR-RWB-S5-E3022-CON-10) |
| Rules | R-DIS-04 and R-DIS-05, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the stage answer, the evaluation of R-DIS-04 and R-DIS-05, the decision record, the hold, the task request and the moves: RWB-S5-E3022-APP.
- The notice row, its template, its generation, its dispatch and the WIN call-back: rwb-comms (P6) (`GAP-2852`).
- The ACE proof-of-delivery and contact views, the batch gate and the freshness stamp: rwb-source-data (P1) (`GAP-2854`).
- The case of record, its route states, the failed notice task row and the parent `CaseWorkflow`: rwb-case (P3), whose answer this baseline declares as consumed and faked.
- The asset record, its take-on routes and its own reads: RWB-S5-E3019-APP, RWB-S5-E3020-APP and RWB-S5-E3021-APP, whose `GET /assets/{assetId}` this baseline names and does not declare.
- The valuations of the asset: rwb-valuation (S1) under API-S5-003 and ASM-0043.
- The notice document, its custody and its retention: rwb-document (P5).
- The authoring, testing, approval and versioning of the DISPOSAL package and of the rule rows of R-DIS-04 and R-DIS-05: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
