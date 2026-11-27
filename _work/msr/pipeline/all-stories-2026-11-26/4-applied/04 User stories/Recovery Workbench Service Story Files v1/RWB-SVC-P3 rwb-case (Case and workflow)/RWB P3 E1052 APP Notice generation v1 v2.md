# RWB-P3-E1052-APP Notice generation v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1052-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-052 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P3-Q |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E1052-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-OCC-001) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-052 for rwb-case; templates, merge fields, rendering and dispatch stay with rwb-comms (P6). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E1052-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, and as the **rwb-case service** behind the case task, I want **a notice requested from the case task in one step — rwb-case sending the case ID, the notice type, the case party key and the language to the rwb-comms contract, and then writing the answer back onto the case as one notice reference, one timeline entry and one decision record, with a held notice opening one case task for the case owner and a delivered notice recorded from the event**, so that **a letter is requested without re-keying the case facts and the case shows exactly what was generated or held, while the template, the merge, the PDF, the dispatch and the proof of delivery stay with the services that own them**.

### 2. Business rationale

Notices are typed by hand from the core bank screens, so a wrong amount or address on a notice can void the notice period and delay litigation. The legacy story answers that by generating the letter from the Legal-approved template with the case data merged, and it serves REQ-OCC-001 and control CTL-14. The need does not change in the target: a demand, a recall and a guarantor notice still have to be produced from an approved template, and the case still has to show which notice went out, on which template version and on what decision.

What changes is where each part of that capability lives. The **template catalog, the Approved check, the merge of every merge code, the party name and address, the PDF render, the footer, the write-once document, the dispatch to the field and the proof of delivery are rwb-comms' (P6) and rwb-document's (P5)**: the Ownership Map gives `notice`, `template` and `merge_field` to P6 and `document` to P5, and Architecture v5 slide 41 names notices, templates, merge fields and proof of delivery as P6's own. **rwb-case owns the case-side half**: the case fact set it sends, the case task that raises the request, the notice reference the case keeps, the timeline entry, the decision record and the delivery fact the case records from the event. rwb-case holds no template, merges no value, stores no PDF and reads no ACE view (DP-01, DP-05). The legacy in-process `NoticeApi.generate` call from the case module becomes **one hop on the rwb-comms contract inside a CaseWorkflow activity, with a 2 s timeout (DP-11)**, and the two event ends become **the outbox and inbox of the service (DP-09)**.

The split is what keeps the two services independent and it is why this story is a secondary slice of a split legacy key: a template change, a renderer change or a dispatch change reaches the case through one answer and one event, and never through a template table, a merge value or a document row. It also keeps the promise the notice relies on — that the case shows what was generated or held — without the case holding a second copy of the letter or of the address.

The legacy test cases of this key are kept in section 16 with their identifiers unchanged, and the end-to-end proof across rwb-case, rwb-comms, rwb-document, rwb-source-data and rwb-decision sits with RWB-ITG-E1052-ITG of the same legacy key.

### 3. Preconditions

- RWB-P6-E1052-CON is published: the notice resources `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}` on base `/api/recovery/comms/v1`, the Notice answer with `noticeId`, `documentId`, `noticeType`, `personKey`, `templateId`, `templateVersion`, `state`, `holdReason` and `messageCodes`, the state values and the hold reasons as data, the `rwb.comms.events.v1` schemas of NoticeGenerated, NoticeDispatched and NoticeDelivered (EV-13, EV-14, EV-15), the error envelope, the `Idempotency-Key` rule with its stored answer and the contract fake. This story builds against that contract and its fake and never against a notice table (DP-01, DP-11).
- The `rwb_case` schema baseline and the case of record exist from the Epic 1 case story (RWB-P3-E1018-APP): `recovery_case`, `case_party`, `task`, `interaction` and the outbox, inbox and idempotency objects.
- The parameters contract and the reference-data contract of rwb-case are published, with the client library, so the notice types, the task code and the case-side switch are read as data and never written in code (DP-07).
- The case task model carries the request task and the hold task as task rows, with their task codes, element type, discretion and status values held as reference data (DP-07).
- The platform contract stories that the pattern table of section 13 names — the decision-record library of DP-03, the reference-data library of DP-07, the outbox and inbox library of DP-09, the migration conventions of DP-15 and the gateway-bff route of DP-19 — are held by the platform stories and are not repeated in the metadata rows, which carry only the contract dependency of this legacy key (GAP-0754; ASM-1375).
- The gateway-bff composite route is published for the case record, the case documents screen and the task list (DP-19).
- The business date is the service business date of rwb-case; the legacy calendar values are not carried over.
- No other CON story is required: the metadata row "Depends on (build)" is None and the lane is Day 1 against the P6 contract fake.
- The login is the rwb-case login (DP-02): Not specified in the source documents (GAP-0753; ASM-1374).

### 4. Flow

1. rwb-case: the litigation officer, or the case owner, opens the request task of the case on SCR-01 My work through the gateway-bff composite route, which calls `GET /api/recovery/case/v1/me/tasks` on rwb-case (DP-19).
2. rwb-case: the officer completes the task through `PATCH /api/recovery/case/v1/tasks/{taskId}` with the notice type and the party key of the case; the endpoint checks the caller's right, the scope of the case and that the notice type is in the notice-type list read through the reference-data contract (DP-07).
3. rwb-case: reads the party links of the case from `case_party`. A party key that is not on the case is refused before any call, with MSG-P4-003 (AC5).
4. rwb-case: builds the request from the case facts it already holds — the case ID, the notice type, the case party key, the language and the business date — and builds the `Idempotency-Key` from the case ID, the notice type, the party key and the business date. No name, address, identity number, balance or any other merge value is read or sent: the merge is P6's.
5. rwb-case: the `RequestNotice` activity calls `POST /api/recovery/comms/v1/cases/{caseId}/notices` on the rwb-comms contract with the request and the key, one hop with a 2 s timeout and a breaker; the call sits inside the workflow activity, so the answer is in the workflow history and a replay reuses it (DP-11).
6. rwb-comms: answers the notice — `noticeId`, `state` Generated or Held, `documentId`, `holdReason` and `templateVersion`. rwb-comms and rwb-document do the Approved check, the merge, the render, the footer and the write-once PDF; rwb-case receives a reference and a state, never a merged value and never a document body.
7. rwb-case: the `RecordAndApply` activity applies the answer in one `rwb_case` transaction — the notice reference, the notice state as a notice fact, the template code and the template version, the document reference and the hold reason on the case row; one timeline entry for the request and its answer; one decision record with decision code "D7.1", the template code and version and the business date; and the task moves to DONE (DP-03).
8. rwb-case: a Held answer — `holdReason` POSTAL_ADDRESS or TEMPLATE_WITHDRAWN, as the source carries them — additionally opens exactly one case task with the task code "Complete notice data" for the case owner, and leaves the case status and the case route state unchanged (AC2).
9. rwb-case: a repeated request on the same business date sends the same `Idempotency-Key`, returns the first notice and writes nothing a second time: no second notice reference, no second timeline entry, no second decision record and no second task (AC3).
10. rwb-comms: publishes `rwb.comms.NoticeDelivered.v1` (EV-15) on `rwb.comms.events.v1` when the proof of delivery is in; the case inbox consumes it once and records the delivery fact on the case timeline (AC4, DP-09).
11. rwb-case: a time-out or a refusal from rwb-comms writes nothing at all — no notice reference, no timeline entry, no decision record and no task — and the request task stays OPEN for a retry under the same key (AC6).
12. Case officer: SCR-03 Case record, SCR-30 Case documents and SCR-01 My work show the notice reference, its state, the template version, the delivery fact and the hold task, all read through the gateway-bff composite route; the notice itself, its PDF and its dispatch stay on the rwb-comms and rwb-document screens' own answers.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | rwb-comms does not answer inside 2 seconds, or is unavailable | No notice reference, no timeline entry, no decision record and no task; the request task stays OPEN and the activity is retried under the same `Idempotency-Key` | MSG-GEN-006 | AC6 |
| X2 | rwb-comms refuses because the template has no Approved version | Nothing is written on the case; the request task stays OPEN with the message of the answer and the officer re-requests when Legal approves a version | MSG-P6-005 | AC1, AC6 |
| X3 | rwb-comms answers a held notice, POSTAL_ADDRESS or TEMPLATE_WITHDRAWN | The notice reference and its held state are recorded; exactly one case task "Complete notice data" is opened; the case status and route state are unchanged | MSG-P6-007 for POSTAL_ADDRESS, MSG-P6-003 for TEMPLATE_WITHDRAWN | AC2 |
| X4 | The same request arrives a second time on the same business date | The first notice is returned from the stored answer and the case keeps one notice reference, one timeline entry, one decision record and one task | None | AC3 |
| X5 | The party key is not a party on the case | Refused before any call; nothing is written and rwb-comms is not called | MSG-P4-003 | AC5 |
| X6 | The caller's role has no Litigation C right | Refused at the endpoint with 403 before any write and before any call | MSG-P4-002 | AC7 |
| X7 | The local decision-record write fails | The transaction rolls back: no notice reference, no timeline entry and no task; the request task stays OPEN | MSG-P7-003 | AC8 |
| X8 | A duplicate `NoticeDelivered` event arrives | The inbox drops it: no second timeline entry and no other write | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the RWB-P6-E1052-CON fake: the notice answer, the held answers and the delivered event are stubbed, so no P6 build is waited for; the platform kits are held by their platform stories |
| Negotiable | The notice types, the task codes, the hold reasons and the case-side switch are data; the story fixes the case-side behaviour, not the values |
| Valuable | The litigation officer reaches a notice from the case task without re-keying, and the case shows exactly what was generated or held and on which template version |
| Estimable | One client, one step with two activities, one repository set, one migration and three read endpoints |
| Small | Fits two weeks with its tests |
| Testable | Each of the eight criteria of section 7 is one automated test; every cross-service value is stubbed in the P6 fake |

### 7. Acceptance criteria

```gherkin
Feature: Notice generation v1 (rwb-case side)

  Background:
    Given case "RW-2026-000123" has product group "MORTGAGE" and party "P-0001" with party_role "BORROWER"
    Given the notice-type list carries "DEMAND", "RECALL" and "GUARANTOR_NOTICE"
    Given the task code "Complete notice data" is loaded as a task row of the case model
    Given the business date is 2026-11-25

  Scenario: AC1 A completed task generates a notice and records it on the case (new, D-RCV-60)
    Given the rwb-comms contract mock returns notice "N-0001" in state "Generated" with template version 2 and document "DOC-0001"
    When the litigation officer completes the notice task of case "RW-2026-000123" for notice type "DEMAND", party key "P-0001" and language "TH"
    Then rwb-case calls POST /cases/{caseId}/notices once with case "RW-2026-000123", notice type "DEMAND", party key "P-0001", language "TH" and an Idempotency-Key built from the case ID, the notice type, the party key and the business date
    Then the case holds notice reference "N-0001" in state "Generated" with template version 2 and document "DOC-0001"
    Then one timeline entry names notice "N-0001" and its answer
    Then one decision record names decision code "D7.1", the template code and template version 2
    Then the request task is "DONE"
    Then the case status and the case route state are unchanged

  Scenario: AC2 A held answer opens one case task and leaves the case unchanged (new, D-RCV-60)
    Given the rwb-comms contract mock returns notice "N-0002" in state "Held" with hold reason "POSTAL_ADDRESS", no document and template version 2
    When the litigation officer completes the notice task of case "RW-2026-000123" for notice type "DEMAND"
    Then the case holds notice reference "N-0002" in state "Held" with hold reason "POSTAL_ADDRESS"
    Then exactly one case task with task code "Complete notice data" is open for the case owner of "RW-2026-000123"
    Then the case status and the case route state are unchanged
    Then no document reference is recorded on the case

  Scenario: AC3 A repeated request returns the first notice and opens no second task (new, D-RCV-60)
    Given the rwb-comms contract mock returned notice "N-0001" in state "Generated" with template version 2 and document "DOC-0001"
    Given notice "N-0001" was requested for case "RW-2026-000123", notice type "DEMAND", party key "P-0001" on 2026-11-25
    When the same request is made again for 2026-11-25
    Then rwb-case sends the same Idempotency-Key and the answer returns notice "N-0001"
    Then the case holds one notice reference, one timeline entry and one decision record for the request
    Then no second task is opened and the case status is unchanged

  Scenario: AC4 NoticeDelivered is recorded once and a duplicate is ignored (new, D-RCV-60)
    Given notice "N-0001" is recorded on case "RW-2026-000123" in state "Generated"
    Given rwb.comms.NoticeDelivered.v1 arrives for notice "N-0001" with delivered_at 2026-11-27
    When the case inbox consumes the event
    Then one timeline entry records the delivery of notice "N-0001" on 2026-11-27
    Then the notice state of the case is not changed by the event
    When the same event arrives a second time
    Then no second timeline entry and no other write is made

  Scenario: AC5 A party that is not on the case is refused with no call (new, D-RCV-60)
    Given party key "P-0999" is not a party on case "RW-2026-000123"
    When the notice task is completed for party key "P-0999"
    Then the request is refused with MSG-P4-003 before any call
    Then rwb-comms is not called and no notice reference, timeline entry or decision record is written

  Scenario: AC6 A time-out from rwb-comms leaves the task open with nothing written (new, D-RCV-60)
    Given the rwb-comms contract mock does not answer inside 2 seconds
    When the litigation officer completes the notice task of case "RW-2026-000123" for notice type "RECALL"
    Then no notice reference, no document reference, no timeline entry and no decision record is written
    Then the request task stays "OPEN" and the officer sees MSG-GEN-006
    Then the retry sends the same Idempotency-Key

  Scenario: AC7 A role without the right is refused (new, D-RCV-60)
    Given user "U-9001" holds RW-REFADM, which has no Litigation C right
    Given the rwb-access contract mock returns no Litigation C right for role "RW-REFADM"
    When "U-9001" completes the notice task of case "RW-2026-000123"
    Then the call is refused with status 403 and MSG-P4-002
    Then rwb-comms is not called and nothing is written

  Scenario: AC8 A failed decision record leaves no notice reference (new, D-RCV-60)
    Given the rwb-comms contract mock returns notice "N-0003" in state "Generated" with template version 2 and document "DOC-0002"
    Given the local decision-record store is unavailable
    When the litigation officer completes the notice task of case "RW-2026-000123"
    Then the transaction rolls back and the case holds no notice reference and no timeline entry
    Then the request task stays "OPEN" and the officer sees MSG-P7-003
```

AC1 to AC8 are new for the rwb-case slice. This story owns no legacy criterion of RWB-E1-052: the legacy AC1 to AC6, AC8 and AC9 are owned by RWB-P6-E1052-APP, the legacy AC7 by RWB-ITG-E1052-ITG, and the end-to-end proof of the generated notice, its PDF and its delivery sits with the harness of the same legacy key. The legacy criteria are not copied here; the eight above test only the case-side deliverable of this title.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One notice request per case, notice type, case party key and business date; the key of the request is built from those four values and the answer of the first call is returned for the rest of the business date | R-UNI-40; legacy AC6; the `Idempotency-Key` rule of RWB-P6-E1052-CON |
| BR2 | rwb-case sends facts only — case ID, notice type, party key, language and business date — and never a value it merged. No name, address, identity number, balance or other merge value is sent, stored or logged | DP-01, DP-05; Template and Rules §R7.2 s17; legacy BR10 |
| BR3 | A held notice always opens exactly one case task with the task code "Complete notice data" for the case owner, and it never blocks the case: the case status and the case route state are unchanged | legacy AC3 and AC4; MSG-P6-007, MSG-P6-003 |
| BR4 | The notice state is read from the rwb-comms answer and kept as a notice fact of the case; it is never a case status and never a case route state, so no case state transition is created by this story | DF-CAS-005 status; DF-CAS-007 route_state; RWB-P6-E1052-CON state values |
| BR5 | The notice reference and the decision record commit together in one transaction; a failed decision-record write leaves no notice reference and no timeline entry | Principle 5; R-UNI-39; DP-03; legacy AC5 |
| BR6 | The delivery fact is recorded from the event only, through the inbox of the case, once per notice; rwb-case writes no delivery fact of its own and reads no delivery table and no ACE view | EV-15; DP-09; legacy BR11 |
| BR7 | rwb_case stores no template, no PDF and no address, and reads no template, merge-field or document table: rwb-case holds no foreign key into `rwb_comms` and no copy of a notice row | DP-01; Ownership Map (notice, template, merge_field P6; document P5) |
| BR8 | A party key that is not on the case is refused before any call with MSG-P4-003, and a role without the Litigation C right is refused at the endpoint with MSG-P4-002; neither path writes anything | legacy AC8 and the legacy permission block; DP-19 route |

### 9. State transitions

No case status and no case route state changes in this story. The two small machines below are the notice request and the request task.

| From | Event | Condition | To |
|---|---|---|---|
| None | Notice requested from the request task | The party key is on the case and rwb-comms answers Generated | REQUESTED, then GENERATED |
| None | Notice requested from the request task | rwb-comms answers Held with POSTAL_ADDRESS or TEMPLATE_WITHDRAWN | REQUESTED, then HELD |
| REQUESTED | Time-out or refusal from rwb-comms | No answer, or an error answer, inside the 2 s budget | REQUESTED; nothing is written and the request is retried under the same key |
| GENERATED or HELD | The same request on the same business date | The stored answer of the first call exists | unchanged |

| From | Event | Condition | To |
|---|---|---|---|
| None | A held notice is applied | The answer carries POSTAL_ADDRESS or TEMPLATE_WITHDRAWN and no open task of that code exists for the case | OPEN |
| OPEN | The case owner completes the task | The missing data is supplied and a new request is answered Generated | DONE |
| OPEN | The request is answered Generated on a retry | The first answer had been held | CANCELED |

| From | Event | Condition | To |
|---|---|---|---|
| Any case status | A notice reference, a notice state or a delivery fact is written | The notice facts are case facts, not states | unchanged |
| Any case route state | A notice reference, a notice state or a delivery fact is written | The route state belongs to the routing rules of the case | unchanged |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Runs the notice step; reads the case and its parties; calls the rwb-comms contract; writes the notice facts, the timeline entry, the decision record and the case tasks |
| rwb-comms (P6) service identity, the comms identity | Owns the notice, the template, the merge fields, the PDF request to rwb-document and the proof of delivery; answers the request and publishes the events |
| RW-LITOFF, litigation officer | Holds Litigation C and Litigation R; completes the notice request task and reads the notice facts of the case in scope |
| RW-CASEOWN, case owner | Holds Litigation R and Case record CRU; receives the task "Complete notice data" and supplies the missing data |
| RW-LEGAL, Legal counsel | Holds Litigation RA and Documents CRUA; approves and withdraws the template versions the answer depends on, in the P6 stories |
| RW-TEAMMGR, team manager | Holds Litigation R; reads the notice facts and the hold tasks of the team in scope |
| RW-REFADM | Holds no Litigation C right; refused on the task completion with MSG-P4-002 |
| rwb-access guard behind the endpoint (RWB-PLT-E1037-CON, RWB-P4-E1037-CON) | Answers the right and the scope of every call; the story reads no access table |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |

The per-service login name is Not specified in the source documents (GAP-0753; ASM-1374); the story names it "the rwb-case login (DP-02)" until it is agreed, and names the counterpart "the comms identity" from the legacy authority block.

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status (never changed by this story) | Read |
| DF-CAS-007 | recovery_case | route_state (never changed by this story) | Read |
| DF-CAS-009 | recovery_case | owner_user_id, the owner the hold task is raised to | Read |
| DF-CAS-031 | case_party | case_id | Read |
| DF-CAS-032 | case_party | party_id, the case party key the request carries | Read |
| DF-CAS-033 | case_party | party_role | Read |
| Not specified in the source documents (GAP-0749; ASM-1370) | recovery_case | notice_ref, notice_state, notice_hold_reason, notice_template_code, notice_template_version, notice_document_id, notice_delivered_at (seven new columns of this story) | Write |
| DF-WRK-018 | task | case_id | Read |
| DF-WRK-019 | task | task_code (the request task and "Complete notice data") | Read and write |
| DF-WRK-022 | task | status (OPEN, DONE, CANCELED) | Write |
| DF-WRK-023 | task | owner_role, RW-CASEOWN on the hold task | Write |
| DF-WRK-024 | task | due_at of the hold task | Write |
| DF-WRK-025 | task | completed_at | Write |
| DF-WRK-026 | task | outcome_code | Write |
| DF-INT-002 | interaction (the case timeline projection) | case_id | Write |
| DF-INT-004 | interaction | occurred_at | Write |
| DF-INT-006 | interaction | direction, OUTBOUND for the request and the delivery | Write |
| DF-INT-013 | interaction | source_system, WORKBENCH | Write |
| DF-INT-014 | interaction | event_code of the timeline entry | Write |
| DF-INT-016 | interaction | actor_ref of the caller or the service | Write |
| DF-INT-018 | interaction | idempotency_key of the request | Write |
| DF-INT-028 | interaction | delivery_status of the delivery entry | Write |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) | all fields, with decision code "D7.1" | Write |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | The case-side notice switch | Read |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | The notice-type list, the task code and the task model values | Read |
| DF-LEG-015 to DF-LEG-034 | notice (rwb_comms, owner P6) | id, state, hold reason, template, document | Read through the rwb-comms contract only; never a table read and never a copy |
| DF-REF-045 to DF-REF-069 | template (rwb_comms, owner P6) | template code and version | Read through the rwb-comms answer only |
| DF-REF-252 to DF-REF-260 | merge_field (rwb_comms, owner P6) | the merge code catalog and its values | Not read: the merge is P6's |
| DF-DOC-001 to DF-DOC-011 | document (rwb_document, owner P5) | the generated PDF | Not read and not written: only the document reference arrives in the answer |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The seven notice columns of `recovery_case` have no field ID in that version, so the row carries the placeholder and one combined gap row: the story needs the reference, the state, the hold reason, the template code and version, the document reference and the delivery date on the case so that the case shows what was generated or held. No copy of a notice row, no merged value, no PDF and no address is written into `rwb_case`, and no foreign key crosses a schema (DP-01). `interaction` is the case timeline projection behind the timeline read; the ledger itself is rwb-source-data's under the Ownership Map ruling.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3). No new path is added by this story: the request task, the case facts and the next action are served by the existing operations and this story writes the rows behind them.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/me/tasks` (API-P3-008) | The caller's open tasks, including the notice request task and the hold task | Case record R, scope applied | Not applicable |
| PATCH | `/tasks/{taskId}` (API-P3-009) | Complete the notice request task with the notice type and the party key; the path that raises the request | Case record U, scope applied | Not applicable |
| GET | `/cases/{caseId}` (API-P3-002) | The case facts the request is built from: the case number, the product group, the status and the notice facts of the answer | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/next-action` (API-P3-016) | The next action and its due date after the request is answered or held | Case record R, scope applied | Not applicable |

Response fields follow the case CON story: the task `id`, `taskCode`, `status`, `ownerRole`, `dueAt`, `completedAt`, `outcomeCode`; the case `id`, `caseNo`, `productGroup`, `status`, `routeState`, `noticeRef`, `noticeState`, `noticeTemplateVersion`, `noticeDeliveredAt`. The notice fields are an additive change to the case answer within major version 1: the field list of the case CON story stays valid, the new properties are optional, and a consumer of the previous version keeps working (GAP-0749; ASM-1370). Errors: 401 no session (MSG-P4-001), 403 no Case record right (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 409 the task is not in a state that may be completed, 422 an invalid request field (MSG-GEN-001), 503 a store that does not answer.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/comms/v1/cases/{caseId}/notices` (API-P6-001) | rwb-comms (P6) | The notice request of AC1: the case ID, the notice type, the party key, the language and the business date, with the `Idempotency-Key`; built against RWB-P6-E1052-CON and its fake | One hop, 2 s (DP-11) |
| GET | `/api/recovery/comms/v1/notices/{noticeId}` (API-P6-002) | rwb-comms (P6) | The re-read of the notice answer for a retry of a request that wrote nothing, and the answer the case shows when the first call left no stored answer | One hop, 2 s (DP-11) |

Both rows are consumed only, never provided, and the answer fields are those of the Notice resource of RWB-P6-E1052-CON. The request field names beyond the legacy generation request are Not specified in the source documents apart from the contract baseline (GAP-0750; ASM-1371); rwb-case sends exactly the case ID, the notice type, the party key, the language and the business date and nothing else.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | caseId | decision record reference, decision code "D7.1", template code and template version, notice reference, business date |

The record is written by the local decision-record library in the same transaction as the notice reference, the timeline entry and the task state, and is relayed with the CloudEvents envelope (DP-03, DP-09). `rwb.case.CaseStateChanged.v1` is not published, because no case state changes in this story. The decision code is the one the source carries for generation; the final call and the outcome value that the case-side record should name are Not specified in the source documents (GAP-0750; ASM-1371).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | P6 rwb-comms | The case inbox: one table hit on `processed_event`, one timeline entry per notice, and no write on a duplicate (AC4) |

The consumer is rwb-case, as the event catalogue records for EV-15. The payload carries the notice reference, the delivered date and the channel only; no name, address or identity number is in the event and none is written by the case.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Carries the notice step of the case from the task to the answer, and the delivery fact from the event |
| Notify (workflow kit template) | Workflow template of the kit | `rwb-case` | The notice step: raises the request, waits for the answer within the 2 s budget, keeps the request task open on a hold, a refusal or a time-out, and holds the delivery wait |
| RequestNotice | Activity | `rwb-case` | Builds the request and the `Idempotency-Key` and calls the rwb-comms operation with one hop, a 2 s timeout and a breaker; records the answer in the workflow history |
| RecordAndApply | Activity | `rwb-case` | Writes the notice facts, the timeline entry, the decision record and the task state in one transaction, and opens the hold task on a held answer |

The step runs inside the workflow, not in a request thread, so a retry reuses the recorded answer and never sends a second notice. That the request is a REST call from a `rwb-case` activity rather than an event-only exchange is the reading of the contract; Architecture v5 slide 13 lists P3 as a listener of P6 and slide 17 gives rwb-comms `POST /notices` as an accepted REST operation, so the direction is recorded as a conflict and assumed here (GAP-0752; ASM-1373).

#### 12.6 Schedules

None. The notice request is raised from a case task and the delivery fact arrives on an event; no Schedule, no cron entry and no polling job is registered by this story (DP-10).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The story adds the seven notice columns and writes them with the case row; the status and the route state are read only |
| case_party | P3 (rwb_case) | The party links the request is validated against; read only |
| task | P3 (rwb_case) | The request task and the hold task "Complete notice data" |
| interaction | P3 (rwb_case) as the case timeline projection | The timeline entries of the request and the delivery; the ledger itself is rwb-source-data's under the Ownership Map ruling |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_case` | Outbox, inbox and idempotency objects of the published record and the consumed event (DP-09) |
| decision_record | PLT library, created in `rwb_case` | The local hash-linked decision record of every notice request (DP-03) |

`notice`, `template` and `merge_field` are P6's tables in `rwb_comms`, and `document` is P5's in `rwb_document`; none of them is read or written here, no foreign key crosses a schema and no view over them is created (DP-01). `decision_log_entry` is a rwb-decision table and is reached only through its topic and its contract.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-comms WireMock | The P6 contract of RWB-P6-E1052-CON | notice "N-0001" in state "Generated" with template version 2 and document "DOC-0001"; notice "N-0002" in state "Held" with hold reason "POSTAL_ADDRESS" and no document; notice "N-0003" in state "Held" with hold reason "TEMPLATE_WITHDRAWN"; a 422 refusal with MSG-P6-005 for a template with no Approved version; a replayed answer for the same `Idempotency-Key`; a delayed answer beyond 2 s; the `NoticeDelivered` fixture for notice "N-0001" with delivered_at 2026-11-27 |
| rwb-access WireMock | The platform guard contract behind the endpoint | `POST /authorise` granting Litigation C and Case record U, and refusing them for RW-REFADM (AC7) |
| gateway-bff composite route (WireMock) | The DP-19 route of SCR-01, SCR-03 and SCR-30 | The merged case, task and notice-fact answers, including the held state with its hold reason and the delivery fact |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 2 consumed | The task, case and next-action reads and the task completion provided; the two rwb-comms notice operations consumed; one hop, 2 s |
| Kafka | 1 published, 1 consumed | `rwb.decision-record.v1` published; `rwb.comms.events.v1` consumed |
| Temporal | 1 workflow, 2 activities | CaseWorkflow with the kit Notify step; RequestNotice and RecordAndApply |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `noticerequest`, Java package `th.co.scb.ace.workbench.recovery.case.noticerequest`; front end fragment `src/modules/recovery/case/NoticeFacts.tsx`, the read-only part of the case screens that shows the notice reference, its state and its delivery fact.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependencies this table adds are held by the platform contract stories and are not repeated in the metadata rows, which carry only the contract dependency of this legacy key, RWB-P6-E1052-CON (GAP-0754; ASM-1375). DP-19 is applied to the screen reads of section 15 and adds the platform route story, held the same way. DP-05 resolves to no ACE read at all: the party key is already on `case_party`, and every merged value stays with rwb-comms (ADR-010).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeRequestService | Service | Validates the notice type against the reference list, checks the party key on `case_party`, builds the request and the `Idempotency-Key`, and decides between a request, a replay and a refusal |
| NoticeClient | Client | Calls the two rwb-comms operations with one hop, the 2 s timeout and a breaker; never retries on its own, so the workflow kit owns the retry (DP-11) |
| NoticeTaskHandler | Service | Answers `PATCH /tasks/{taskId}` for the request task, reads `GET /me/tasks`, and opens exactly one hold task with the task code "Complete notice data" |
| NoticeDeliveryHandler | Consumer | Consumes `rwb.comms.NoticeDelivered.v1` through the inbox and writes one timeline entry per notice, once |
| DecisionRecordClient | Library adapter | Writes the local decision record with decision code "D7.1", the template code and version and the notice reference, in the same transaction (DP-03) |
| TimelineWriter | Service | Writes the request entry and the delivery entry on `interaction` with the event code, the actor and the idempotency key |
| NoticeReferenceRepository | Repository | Reads and writes the notice columns of `recovery_case` in schema rwb_case only |
| NoticeFacts | React component | Shows the notice reference, its state, the template version, the hold reason and the delivery fact on SCR-03, SCR-30 and SCR-01, read only |

**Database and migrations**

- Migration `V1052_1__notice_reference.sql` in the rwb-case Flyway sequence (DP-15) adds `notice_ref` varchar(40), `notice_state` varchar(20), `notice_hold_reason` varchar(30), `notice_template_code` varchar(60), `notice_template_version` integer, `notice_document_id` varchar(60) and `notice_delivered_at` timestamp to `recovery_case`. The seven columns are the combined gap row of section 11 (GAP-0749; ASM-1370).
- One unique index `ux_notice_request ON recovery_case (id, notice_ref)` so a notice reference is recorded once per case, and one timeline index `ix_case_timeline_notice ON interaction (case_id, event_code, occurred_at)` for the read of AC4.
- One partial unique index `ux_task_open_code ON task (case_id, task_code) WHERE status IN ('OPEN','IN_PROGRESS')` so a repeated held answer cannot open a second task; the two open statuses are the values of the task-status list, and the task code itself is reference data, not a constant.
- No new table, no foreign key into `rwb_comms` and no view over a P6 or P5 table (DP-01).

**Configuration and reference data**

- The notice-type list with DEMAND, RECALL and GUARANTOR_NOTICE as the codes the source carries, through the reference-data contract of rwb-case (DP-07).
- The task code "Complete notice data" and the request task code as task rows of the case model, with their element type, discretion and status values; the element-type and discretion values the source does not give are Not specified in the source documents (GAP-0751; ASM-1372).
- The hold reasons POSTAL_ADDRESS and TEMPLATE_WITHDRAWN are read from the rwb-comms answer and matched against the hold reasons of RWB-P6-E1052-CON; they are never written in code.
- The case-side switch is a parameter read through the parameters contract; its key and default are Not specified in the source documents (GAP-0753; ASM-1374).

**Build steps**

1. `NoticeReferenceRepository` and the migration with the seven columns, the unique index and the timeline index; tests for AC1 and AC3.
2. `NoticeClient` against the rwb-comms WireMock, with the 2 s timeout, the breaker and the stored-answer replay; tests for AC1, AC3 and AC6.
3. `NoticeRequestService` with the notice-type check, the party check and the key build; tests for AC5 and AC6.
4. `NoticeTaskHandler` with the completion path and the single hold task; tests for AC2, AC3 and AC7.
5. `RecordAndApply` with the notice facts, `TimelineWriter` and `DecisionRecordClient` in one transaction, and the rollback path; tests for AC1 and AC8.
6. `NoticeDeliveryHandler` on the inbox with the duplicate drop; test for AC4.
7. The kit Notify step inside CaseWorkflow and the retry of a failed request; test for AC6.
8. The read-only `NoticeFacts` fragment and the composite-route contract test; test for AC1 and AC2.

**Feature switch.** The legacy flag name `rwb.comms.notice-generation` stays with rwb-comms and is not renamed or reused here. The rwb-case switch is a parameter read through the parameters contract: off means the case side raises no request and the request task shows that the notice request is switched off. The key is Not specified in the source documents (GAP-0753; ASM-1374).

**Done when.** The tests in section 16 pass, the RWB-P6-E1052-CON contract tests stay green, every notice reference on a case has one timeline entry and one decision record that names the template code and version, no case holds a template, a merged value or a PDF, and RWB-ITG-E1052-ITG can drive the journey through the contract fakes of this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | rwb-comms refuses because the template has no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-007 | A held notice names a required value that is empty, for example the postal address | {notice} for case {case} is on hold. {field} has no value on the case. |
| MSG-P6-003 | A held notice names a withdrawn template | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The local decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The rwb-comms answer carries it because the account data product is older than the business date; rwb-case relays the code and never rewords it | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P4-002 | The role has no Litigation C right for the task completion | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The party key is not a party on the case, or the case is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | rwb-comms does not answer inside the 2 s budget | {system} is not available. Your request is queued and will be retried. |

MSG-P6-005, MSG-P6-007, MSG-P6-003, MSG-P7-003, MSG-P1-001, MSG-P4-002 and MSG-P4-003 are copied unchanged from RWB-E1-052 section 14; MSG-GEN-006 is the platform message text of the contract baseline RWB-P6-E1052-CON, where the same time-out condition is described. For MSG-GEN-006, `{system}` is "rwb-comms". MSG-P6-005 is the refusal of the P6 answer and this story shows it, it does not raise it; the same holds for MSG-P6-007, MSG-P6-003 and MSG-P1-001, whose raiser is rwb-comms.

### 15. Screens and states

| Screen | What this story shows | States |
|---|---|---|
| SCR-03 Case record | The notice reference, its state, the template code and version, the hold reason and the delivery date of the case | Loading; read only; held with its hold reason; delivered |
| SCR-30 Case documents | The notice as a generated document reference on the case, with the document the P6 answer names and the delivery fact when the event has arrived | Generated; Held; Delivered |
| SCR-01 My work | The notice request task and the hold task "Complete notice data" for the case owner, with the due date | Open; overdue; done |

All three are served by the gateway-bff composite route, which calls rwb-case for the case, the notice facts and the tasks, and rwb-comms for the notice row itself and its PDF, one hop each, and merges the answers into the screen model (DP-19). No screen calls an owner service directly and no screen writes. SCR-18 Notice approval belongs to another story and is not served here; the field-level mapping of the composite route, its masking and its timeout budget belong to RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-052-11 | AC4, BR6 | End to end | `NoticeDelivered` fixture for notice "N-0001" on case "RW-2026-000123", and a notice with no delivery event |
| TC-E1-052-01 | AC1, BR1, BR2, BR4 | End to end | Case "RW-2026-000123" Mortgage, party "P-0001", notice "N-0001" Generated, template version 2, document "DOC-0001" |
| TC-E1-052-02 | AC1, AC6, BR2 | End to end | The rwb-comms mock refuses with MSG-P6-005 for a template with no Approved version; nothing is written on the case |
| TC-E1-052-03 | AC2, BR3 | End to end | The rwb-comms mock answers Held with hold reason "POSTAL_ADDRESS" and no document |
| TC-E1-052-04 | AC2, BR3 | End to end | The rwb-comms mock answers Held with hold reason "TEMPLATE_WITHDRAWN" |
| TC-E1-052-05 | AC8, BR5 | End to end | Decision-record store stubbed unavailable on the request path |
| TC-E1-052-06 | AC3, BR1 | End to end | The same request twice on 2026-11-25 with the same `Idempotency-Key` |
| TC-E1-052-07 | AC1, BR2 | End to end | The rwb-comms answer carries MSG-P1-001 for the account data product with a data date older than the business date; the case relays the code unchanged |
| TC-E1-052-08 | AC5, BR8 | End to end | Party key "P-0999" not on case "RW-2026-000123" |
| TC-E1-052-09 | AC7 (Access), BR8 | Component | The caller holds RW-REFADM without Litigation C; the guard stub refuses with MSG-P4-002 |
| TC-E1-052-10 | AC8, BR5 (Principle 5) | NFR | Decision-record write forced to fail during the request of 20 notices; no notice reference is stored for any of them |

The eleven cases are the legacy cases of this key, kept in the legacy order and under their legacy identifiers; legacy level System maps to End to end, Access to Component and Resilience to NFR. Each row is asserted twice in the run: once against the case-side behaviour of this story with the P6 fake, and once end to end across the services in RWB-ITG-E1052-ITG, which holds the `-ITG` copy of each case; the stale-batch proof itself (legacy AC7) sits with that harness. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the notice types, the task codes, the hold reasons, the status values and the case-side switch are reference data or parameters read through the contracts of rwb-case; no template code, no merge code and no timeout is a constant.
- No personal data in rwb_case, in events or in logs: no name, no address, no identity number and no account number is read, sent, stored or logged by this story; the payloads carry IDs, codes, dates and a document reference only, and the workflow payloads pass the codec.
- The template, the merge, the PDF, the footer, the dispatch and the proof of delivery belong to rwb-comms and rwb-document; rwb-case holds no template and no PDF, merges no value, reads no template, merge-field or document table and holds no foreign key into another schema (DP-01).
- One hop: rwb-case calls the rwb-comms contract once per request with a 2 s timeout and a breaker, and never calls a second service to complete the same request (DP-11, ADR-020).
- One writer of the notice: the notice row is written by rwb-comms only; the case writes the notice reference and its facts, and a correction is a new request, never an edit of the notice.
- The decision record is written in the same transaction as the notice reference; a failed write leaves no reference and no timeline entry (R-UNI-39).
- Delivery is recorded from the event only, once per notice through the inbox; rwb-case writes no delivery fact of its own and reads no ACE view (DP-05, ADR-010).
- Every outbound record is written to the outbox in the same transaction as the change it records, and the consumed event passes the inbox (DP-09).
- The notice state is a case fact, never a case status or a route state; a screen that shows it writes nothing.
- The identifier of the notice and the identifier of the document are carried as references; no document body, no barcode image and no addressee is stored.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data, requested and tracked on the case | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-14 | 8.1 Prepare pre-litigation; 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-UNI-39, R-UNI-40 | TC-E1-052-01 to TC-E1-052-11 |
| D-RCV-60 split of RWB-E1-052 | The case-side half of notice generation: the request from the case task, the notice reference, the timeline entry, the decision record and the delivery fact; the template, the merge, the render and the dispatch stay with rwb-comms and rwb-document | Decision log, D-RCV-60; Template and Rules §R5.5, §R6 and §R7 | FEAT-DRI-14 | 8.1 Prepare pre-litigation; 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-052-01, TC-E1-052-03, TC-E1-052-05, TC-E1-052-11 |

The requirement ID of this key is REQ-OCC-001 and it is the only requirement ID the story carries; FEAT-DRI-14, the two L3 processes and the four rules are the legacy trace of RWB-E1-052, and the PRD reference stays Pending (C1) until the Epic 1 PRD is realigned. The rules R-LIT-03 and R-LIT-04 govern the template choice and the withdrawn-template hold, which rwb-comms applies; this story carries them so that the legacy trace of the key stays whole, and it evaluates neither of them.

### 19. Out of scope

- The template catalog, the Approved check, the withdrawn-template hold, the merge of every merge code, the party name and address, the PDF render and its footer: rwb-comms (P6), RWB-P6-E1046-APP and RWB-P6-E1052-APP.
- The write-once document store and the generated document itself: rwb-document (P5).
- Dispatch to the field, the WIN file and the proof of delivery capture: the dispatch stories of RWB-E1-055 and RWB-E2-021, and RWB-P6-E5002-APP.
- Approval of demand and recall notices before dispatch (legacy RWB-E2-014).
- The person-facing endpoint that requests a notice outside the case task (legacy RWB-E2-021).
- The customer, contact, account and delivery data products and their ACE views: rwb-source-data (P1); this story reads none of them.
- The central decision ledger, its seal and its read: rwb-decision (P7).
- The end-to-end proof of the journey across the five services: RWB-ITG-E1052-ITG.
- The full read-only case record view and the case timeline screen: RWB-P3-E1023-APP and RWB-P3-E2016-APP.
- The rights, the roles and the scope data themselves (P4 access stories), and the composite route of the three screens (RWB-PLT-N001-CON).
- The deployment of this capability: chart values, queue provisioning, dashboards and the runbook.
