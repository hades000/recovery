# RWB-P3-E2024-APP Field app photos and bills into the document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2024-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-P3-AJ |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2024-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-DCM-013) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the case-side slice of RWB-E2-024 is written for `rwb-case` on schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, queue `rwb-case`, against the contract baseline RWB-P5-E2024-CON. Status Draft because no approval of the realigned story is recorded (GAP-2223; ASM-3660). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **field collector who syncs a visit and the case owner who chases what the visit did not deliver**, I want **the case a capture is checked against — its number, its status, its entry date, its stage and its route — the answer that the case is mine because I hold a task or an assignment on it, and one task on the case when a required document is still missing after a sync**, so that **an inspection is accepted only against its own case with that case's own entry date, and nothing the visit was supposed to produce is lost because a document did not arrive**.

Inside `rwb-case` this is the case-side slice of legacy RWB-E2-024: the case context and the one record the field-capture path of the document hub stands on.

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- The slice delivers four answers and one record. The answers are the `Case` resource of `GET /api/recovery/case/v1/cases/{caseId}` — case number, status, entry date `DF-CAS-013`, stage code `DF-CAS-006`, route code `DF-CAS-008` and the caller's task and assignment; the case-scope answer taken from the `rwb-access` authorise contract; the stage and route keys the checklist is read by; and the `DOCUMENT_CHECKLIST` version in force as reference data. The record is the task raised when a required document is still missing after a sync.
- The capture is not here: the upload, the manifest, the limits, the scan, the OCR, the extraction, the bill threshold and SCR-30 are `rwb-document`'s (RWB-P5-E2024-APP), the rights and the scope policy are `rwb-access`'s (RWB-P4-E2024-APP), and the field app is the field app's.
- The entry date is answered once as the comparison date of the capture-time-before-entry-date check (legacy BR3); the age limit is measured by the hub from the receipt time, so this service answers a date and never a limit.
- The task and the assignment that make a case `OWN` are this service's rows, so the scope evidence is resolved here while the scope policy stays `rwb-access`'s. The checklist items are the hub's; this service holds only the checklist *version* as a `reference_version` row and the stage and route that select the items.
- The service writes the task as one `task` row and one DP-03 entry in one transaction, and publishes no event of its own: `rwb.case.events.v1` stays the case baseline's.

### 2. Business rationale

Inspection photos and utility bills are sent today by chat or carried back to the office, the date and place of a visit cannot be shown when it is questioned, and a checklist meant to be completed during the visit is found to be incomplete only when someone asks the borrower again. The legacy story put the capture into the intake path of the document hub. This slice supplies the three things that path cannot invent for itself — the case a capture belongs to, the entry date the capture time is compared with, and the answer that the collector is entitled to the case at all — and closes the loop the legacy story left open: when a sync leaves a required document missing, the case gets one task and one timeline entry, so the missing deed is chased on the case instead of in a chat.

The story carries controls CTL-11 (position and photos of a home are personal data) and the evidence expectation of R-DIL-22 (`checklist, photographs and bills captured` before the asset unlock decision), L3 process 13 Manage documents and correspondence, and feature FEAT-DCM-21. It meets REQ-DCM-013 on the case side.

The realignment changes the mechanism, not the rule: DP-01 and DP-11 turn `CaseDirectory.findById` into the published case operation of this service in `rwb_case` (one hop, 2 s timeout, a fake, no copied case row); DP-11 turns the ACE common access check into the `rwb-access` authorise contract as data while the task and the assignment stay `rwb_case` rows; DP-07 answers the checklist version as reference data and leaves the items to the hub; DP-06, DP-07 and DP-03 make the task a `task` row whose code, owner role and due date are data, recorded through the local decision-record library in the same transaction and published on `rwb.decision-record.v1`; DP-09 consumes `rwb.document.DocumentStored.v1` through the inbox, deduplicated by event ID; DP-15 and DP-19 give one migration in this service's Flyway sequence and the composite route to the screens.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E1018-CON | The published contract of `GET /api/recovery/case/v1/cases/{caseId}` and the `Case` resource this slice answers from, with its fake. That resource is published with twelve fields and does not name the stage code or the route code, although the field range it cites (DF-CAS-001 to DF-CAS-023) covers both: Not specified in the source documents (GAP-2223; ASM-3657) |
| RWB-P3-E1043-CON | The reference-data contract of this service, which serves the `DOCUMENT_CHECKLIST` version in force and the lists `LOV-TASK-STATUS`, `LOV-ELEMENT`, `LOV-DISCRETION`, `LOV-ROLE` and `LOV-SOURCE`; no list value is typed in code (DP-07) |
| RWB-P3-E1042-CON | The parameters contract and client library of this service, which resolves the due-date parameter of the checklist task; no number is written in code (DP-06) |
| RWB-P4-E1037-CON | The `rwb-access` authorise contract and its fake, which answers the case-scope question for capability area `DOCUMENTS`, right `C` and the case as the object reference. The request and response shape of the call is Not specified in the source documents (GAP-2223; ASM-3657) |
| RWB-P5-E2024-CON | The published field-capture baseline this slice is tested against: case `RW-2026-000501` with entry date `2026-10-02` and a field inspection task for `FC-01`, the ten-item inspection (eight `INSPECTION_PHOTO`, two `UTILITY_BILL`) synced at `2026-12-15 14:20` at `13.7563` and `100.5018`, the offline capture at `2026-12-14 10:05`, the entry-date refusal of legacy AC8, and case `RW-2026-000502` where `FC-01` has no task |
| The document hub's checklist read | `GET /api/recovery/document/v1/cases/{caseId}/document-checklist` (API-P5-008, owner P5 `rwb-document`) answers the required document types of a case with their present counts, one hop and a 2 s timeout (DP-11). The story that publishes that baseline is not named in the sources (GAP-2223; ASM-3658) |
| `rwb.decision-record.v1` and the local library | The decision-record library of DP-03, so the checklist task and its record commit in one transaction |
| gateway-bff composite route | The route of DP-19 that carries the case record and the case timeline to the screens, with the 2 s timeout of DP-11 |

Business preconditions carried from RWB-E2-024:

- The collector holds a task on the case, so the case is in `OWN` scope; a case with no task and no assignment for the caller is outside the scope and is answered 404 with MSG-P4-003 (FSD P4 v3 AC-EXC-P4-004-01).
- The case in the tests is the legacy deed in lieu case at stage `DEED_IN_LIEU` with entry date `2026-10-02`, so the checklist of R-DIL-22 (`WITH_FIELD_INSPECTION`) is the one read here.
- The checklist version label `CHK-2026.11` is a test value only: Not specified in the source documents (GAP-2223; ASM-3659).
- Every refusal names the case and the action only, never a customer field, a document, a position or a file name (legacy section 17; CTL-11).

### 4. Flow

1. Field collector: opens the case in the field app and starts a capture batch; the app asks the Workbench for the case context.
2. `CaseContextController`, through the gateway-bff composite route (DP-19): serves `GET /api/recovery/case/v1/cases/{caseId}` — case number, status, entry date `DF-CAS-013`, stage code `DF-CAS-006`, route code `DF-CAS-008` and the caller's open task and current assignment.
3. `CaseScopeResolver`: for area `DOCUMENTS` and right `C`, calls `POST /api/recovery/access/v1/authorise` on `rwb-access` with the caller, the case, the area, the right and the case activity that makes it `OWN` (DP-11, one hop, 2 s timeout, breaker). `rwb-access` answers allowed or refused: 403 MSG-P4-002 for a right the role does not carry, 404 MSG-P4-003 for a case outside the scope, and this service adds no second policy check.
4. The field app: sends the batch to the document hub with the case in the path; the comparison date of the capture-time-before-entry-date check is the entry date of step 2, `2026-10-02`, and the age limit is measured by the hub from the receipt time.
5. `ChecklistVersionReader`: answers the `DOCUMENT_CHECKLIST` version in force through the reference-data contract (DP-07) — label, state and valid-from — so the hub resolves the required item of the case's stage and route against one version.
6. The document hub: stores the accepted captures through its own store, satisfies the item of each stored type, and publishes `rwb.document.DocumentStored.v1` once per accepted item.
7. `DocumentStoredListener`, through the inbox of DP-09: records the event ID once, ignores a repeat, and reads the case checklist through API-P5-008 — one hop, 2 s timeout.
8. `ChecklistTaskRaiser`: when the answer still lists a required type, raises one `task` — element type `HUMAN_TASK`, discretion `REQUIRED`, status `OPEN`, the task code read from reference data naming the missing type and the checklist version, the owner role read from reference data, and the due date from the parameter in force (DP-06, DP-07).
9. `DecisionRecordWriter`, in the same transaction as the task: writes the DP-03 entry with the case, the rule reference, the missing type, the checklist version and the task reference, and publishes on `rwb.decision-record.v1` through the outbox.
10. Case owner: opens `GET /api/recovery/case/v1/cases/{caseId}/timeline` and sees the task as a `TASK` item with actor `SY-CASEWF`, source system `WORKBENCH` and its time, beside the document items the hub composes; once the document is on the case, the owner completes the task through the task API with the outcome code read from reference data.

A task that cannot be recorded is not raised (step 9, R-UNI-39); a checklist answer that does not arrive leaves the case unchanged with the reason in the log, rather than a task without evidence (step 7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case does not exist | 404; no task, no record, no data | MSG-P4-003 | AC4 |
| X2 | The case exists but the caller holds no task and no assignment on it | The scope answer is refused and the case read returns 404; nothing is raised | MSG-P4-003 | AC4 |
| X3 | The role does not carry Documents `C` | 403 from the authorise answer, naming the action and the area; the batch is not accepted | MSG-P4-002 | AC3 |
| X4 | The authorise call does not answer within 2 s or meets an open breaker | The case context is not served; the app may retry the same request; nothing is raised | MSG-GEN-006 | AC3 |
| X5 | The checklist answer does not answer within 2 s | No task is raised, nothing changes, and the reason is in the log; the event stays in the inbox | MSG-GEN-006 | AC6 |
| X6 | The checklist lists no required type for the stage and route | The answer is empty and no task is raised; the case is unchanged | None | AC5, AC6 |
| X7 | A required type is still missing after the sync | One `OPEN` task with the missing type in its code, and one decision-record entry | None | AC6, AC7 |
| X8 | The same `DocumentStored` event is redelivered, or the sync is resent | The inbox ignores the repeat; the open task is unchanged and no second task is raised | None | AC8 |
| X9 | The decision record cannot be written | The task is not raised, nothing changes, and an incident is raised | MSG-P7-003 | AC6, TC-E2-024-17 |
| X10 | The earlier task is completed and a later sync still leaves the type missing | One new task is raised for that type, because the earlier one is closed | None | AC8 |

A refusal, a timeout and a failed record all leave the case, its tasks and its decision record as they were; only a checklist answer that names a required type and a committed record produce a task.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the case baseline RWB-P3-E1018-CON, the reference-data and parameters contracts of this service, the `rwb-access` authorise contract and RWB-P5-E2024-CON, each with a fake; no other Epic 2 story is needed |
| Negotiable | The task code, owner role, discretion, due date and checklist version are data rows; the story fixes the answers and the one task |
| Valuable | A capture is accepted only against its own case and entry date, and a document the visit did not produce becomes a task on the case before anyone asks the borrower again |
| Estimable | Two read operations used, one authorise call, one checklist read, one task raise with its record, one index migration |
| Small | Fits one week with its tests, because the upload, the scan, the OCR, the checklist items and the screens are other stories' |
| Testable | Every criterion in section 7 is one test case in section 16; the case, the task, the checklist and the document event come from contract fakes |

### 7. Acceptance criteria

```gherkin
Feature: Case context, case scope and the missing-document task for field app captures

  Background:
    Given the environment is SIT
    Given case "RW-2026-000501" with entry date 2026-10-02, status "IN_PROGRESS" and stage "DEED_IN_LIEU", and a field inspection task for field collector "FC-01" with role RW-FIELDCOL
    Given the rwb-access contract mock returns allowed for "FC-01" on area "DOCUMENTS", right "C" and scope "OWN" for case "RW-2026-000501"
    Given the rwb-document contract mock returns the document checklist of case "RW-2026-000501" with checklist version "CHK-2026.11", "INSPECTION_PHOTO" present and "SETTLEMENT_AGREEMENT" required and missing
    Given the rwb-document contract mock returns document "DOC-0501-01" of type "INSPECTION_PHOTO" for case "RW-2026-000501", stored at 2026-12-15 14:20
    Given the reference-data contract returns LOV-TASK-STATUS with "OPEN", LOV-ELEMENT with "HUMAN_TASK", LOV-DISCRETION with "REQUIRED" and LOV-SOURCE with "WORKBENCH"
    Given the parameters contract returns the checklist task due-date parameter in force

  Scenario: AC1 The case context of a capture (new, D-RCV-60)
    When "FC-01" reads GET /api/recovery/case/v1/cases/{caseId} for case "RW-2026-000501" before the batch is sent
    Then the answer is 200 with case number "RW-2026-000501", status "IN_PROGRESS", entry date 2026-10-02, stage code "DEED_IN_LIEU" and the route code of the case
    Then the answer carries the field inspection task of "FC-01" with status "OPEN" and element type "HUMAN_TASK"
    Then the answer carries no customer field, no document, no file and no position

  Scenario: AC2 The case entry date is the comparison date of a capture (new, D-RCV-60)
    Given the rwb-document contract mock refuses the item captured at 2026-10-01 09:00 with MSG-GEN-003 naming "Capture time" and "Case entry date"
    When the refusal is resolved against the case answer of this service
    Then the case answer carries entry date 2026-10-02 and no other date is offered for the comparison
    Then the refusal names 2026-10-02 as the case entry date
    Then no case row, no task and no document is changed by the refusal

  Scenario: AC3 A collector with a task holds the case in scope (new, D-RCV-60)
    Given "FC-01" holds the field inspection task on case "RW-2026-000501" and an assignment from 2026-10-02 with reason "ALLOCATION"
    When the case context is resolved for area "DOCUMENTS", right "C" and case "RW-2026-000501"
    Then the answer is allowed with scope "OWN" and the case in scope
    Then the activity that makes the case "OWN" is the open task and the open assignment of "FC-01", and no other case is returned
    Then the call to POST /api/recovery/access/v1/authorise carries the case, the area and the right and no customer field

  Scenario: AC4 A case with no task and no assignment is refused (new, D-RCV-60)
    Given case "RW-2026-000502" where "FC-01" holds no task and no assignment
    When "FC-01" reads GET /api/recovery/case/v1/cases/{caseId} for case "RW-2026-000502"
    Then the response is 404 with message MSG-P4-003
    Then the authorise answer for that case is refused and no case data is returned
    Then no task is raised and no decision record is written for "RW-2026-000502"

  Scenario: AC5 The checklist keys and the checklist version (new, D-RCV-60)
    When the case answer of "RW-2026-000501" is read by the document hub
    Then the answer carries stage code "DEED_IN_LIEU" and the route code of the case, the two keys the checklist is read by
    Then the reference-data answer carries the DOCUMENT_CHECKLIST version "CHK-2026.11" in force with its state and its valid-from date
    Then no checklist item row is written in rwb_case: the items stay in the document hub's document_checklist_item

  Scenario: AC6 A required document still missing raises one case task (new, D-RCV-60)
    Given the sync of 2026-12-15 14:20 stored ten documents and rwb.document.DocumentStored.v1 is consumed for document "DOC-0501-01"
    When the checklist answer of the case still lists "SETTLEMENT_AGREEMENT" as required and missing
    Then one task exists on case "RW-2026-000501" with element type "HUMAN_TASK", discretion "REQUIRED", status "OPEN" and the owner role read from reference data
    Then the task code names the missing type "SETTLEMENT_AGREEMENT" and the checklist version "CHK-2026.11", read from reference data
    Then the task due date is the value of the parameter in force and no due date is written in code
    Then one decision-record entry is written in the same transaction as the task

  Scenario: AC7 The task appears on the case timeline (new, D-RCV-60)
    Given the case timeline of "RW-2026-000501" is read through GET /api/recovery/case/v1/cases/{caseId}/timeline
    When the task of AC6 is "OPEN"
    Then one item of type "TASK" shows the task with actor "SY-CASEWF", source system "WORKBENCH" and its created time
    Then the document items of the timeline are the document hub's and the ledger's, and this service writes no document item

  Scenario: AC8 A repeated sync or a repeated event raises no second task (new, D-RCV-60)
    Given the task of AC6 is "OPEN" on case "RW-2026-000501" for the type "SETTLEMENT_AGREEMENT"
    When the same rwb.document.DocumentStored.v1 event is delivered again and the officer resends the same ten client file IDs
    Then no second task exists and the first task is unchanged
    Then the inbox holds the event ID once and the duplicate is ignored
```

These eight criteria are the ones this slice owns and all are new under D-RCV-60, because a secondary slice owns no legacy criterion: legacy AC1 to AC15 of RWB-E2-024 are carried by `rwb-document` (RWB-P5-E2024-APP) against RWB-P5-E2024-CON and the legacy access answer by `rwb-access` (RWB-P4-E2024-APP). The legacy test cases are kept here in section 16 against this slice's assertions, so nothing the legacy story proves is lost. The shared values are the legacy ones unchanged: case `RW-2026-000501` with entry date `2026-10-02`, collector `FC-01` with role `RW-FIELDCOL`, the ten-file inspection of `2026-12-15 14:20` at `13.7563` and `100.5018`, the offline capture at `2026-12-14 10:05`, the entry-date refusal of `2026-10-01 09:00` against `2026-10-02`, and case `RW-2026-000502` with no task for `FC-01`. The authorise request and response shape, the stage and route fields of the case answer, the checklist version label and the task data are not in the sources: Not specified in the source documents (GAP-2223; ASM-3657), (GAP-2223; ASM-3658), (GAP-2223; ASM-3659).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A capture belongs to the case named in the request: the case number, status, entry date and stage and route are read from the case row of `rwb_case`, and no case is matched, created or changed on this path | Legacy RWB-E2-024 BR6; FEAT-DCM-21 |
| BR2 | A capture is accepted only for a case the collector is entitled to: the scope answer comes from `rwb-access` on the caller's task or open assignment, and a case with neither is answered 404 with MSG-P4-003 | Legacy AC12 and X7; FSD P4 v3 AC-EXC-P4-004-01; TSD P3 v3 T6.1 |
| BR3 | The case entry date `DF-CAS-013` is the comparison date of the capture-time-before-entry-date check; the age limit is measured by the document hub from the receipt time and is not answered here | Legacy BR3; DF-CAS-013; CAPTURE_MAX_AGE_DAYS |
| BR4 | The document checklist is read by the case's stage code and route code, and the checklist version in force is a `reference_version` row answered through the reference-data contract | REQ-DCM-011; DF-REF-243; TSD P3 v3 T3.1 |
| BR5 | The required document types and their present counts are the document hub's `document_checklist_item` and `case_document_check`; no checklist item row is written or copied in `rwb_case` | TSD P5 v2 T3.1; Ownership Map (P5) |
| BR6 | A required document still missing after a sync raises one `OPEN` task, only one per case and missing type: a redelivered event or a resent sync raises nothing, and a new task comes only after the earlier one is closed | Legacy X1 and AC4; R-UNI-40 |
| BR7 | The task and its decision-record entry commit in one transaction, so a task that cannot be recorded is not raised | Legacy BR10 and X12; Principle 5; R-UNI-39; DP-03 |
| BR8 | The task is visible on the case timeline as a `TASK` item with its actor, source system and time, and the timeline shows the documents the hub stored without this service copying them | REQ-OCC-008; FEAT-WKM-08; TSD P3 v3 API-P3-003 |
| BR9 | No personal data on this path: the case context carries the case and not the customer, and a position, a file name, a bill value and a photo never enter the task, the record or a log line | Legacy BR9; CTL-11; DL26 |

Target-service statements that make the rules hold in `rwb-case`:

- BR1 is one read of `recovery_case` by `id`, keyed by the case in the path; the case number is the value the case was created with (RWB-P3-E1018-APP). BR2 is one call on the authorise contract with the case and the caller's activity; the letters and the policy are rows of `rwb_access`, and a missing row is a refusal, never a default allow.
- BR3 is the presence of `entryDate` in the answer and nothing else: with no age limit and no clock here, the check cannot be duplicated with a different value. BR4 is the `reference_version` read for table code `DOCUMENT_CHECKLIST` under the valid-from rule, with the status list `LOV-VERSION-STATUS`.
- BR5 is an absence: a test asserts that no `document_checklist_item` and no `case_document_check` row is created in `rwb_case`. BR6 is the partial unique index `ux_task_case_code_open ON task (case_id, task_code) WHERE status = 'OPEN'` plus inbox deduplication, so it holds against both a redelivered event and a resent sync.
- BR7 is one transaction of the `task` row and the DP-03 entry, with the DP-09 idempotency key on the internal raise. BR8 is the task read of the timeline: the document items are composed from the hub's read, so this service writes no document item.
- BR9 is a check on the writer: it writes the case, the missing type code, the checklist version and the task reference, and a test scans the text for any part of a position, a file name or a bill value.

### 9. State transitions

None for the case. This story changes no case status, stage or route: the case context is read and the task is the only row written.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The checklist answer names a required type and the record commits | No `OPEN` task exists for the case and that type | `OPEN`, with the owner role and due date of the data |
| `OPEN` | The document of the missing type is stored on the case | The case owner completes the task through the task API | `DONE`, with the outcome code of the reference data |
| `OPEN` | The case owner starts the chase | None | `IN_PROGRESS` |
| `OPEN` or `IN_PROGRESS` | The case closes | The closure reason is recorded by the case | `CANCELED` |
| `DONE` or `CANCELED` | A later sync leaves the same type missing again | No `OPEN` task exists for the case and that type | `OPEN`, a new task row |

The task states are the `LOV-TASK-STATUS` values read as reference data. The case state machine is the case baseline's (R-UNI-01 to R-UNI-50) and this story moves nothing in it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| `RW-FIELDCOL` Field collector | Reads the case context of a case they hold a task or an assignment on (Case record `R`) and sends its captures through the document hub (Documents `C`) |
| `RW-CASEOWN` Case owner | Reads the context and the timeline (`CRU`) and receives and completes the missing-document task (`CRU`) |
| `RW-RESTRUCT` Restructuring officer (FCR) | Reads the context and the captured documents on deed in lieu cases (`RU`) |
| `RW-PHONECOL` Phone collector | Reads only (`R`); holds no Documents `C` and cannot send a capture |
| `RW-TEAMMGR` Team manager | Reads the case record and the timeline (`R`) and reassigns the task (queue and allocation `CRUA`) |
| `SY-CASEWF` Case workflow module | Service identity: writes the task and its record, and reads the case and the checklist answer |
| `SY-OCR` OCR and extraction pipeline | Reads the case context of a case it extracts for (`R`) |

The rights and the scope policy are `rwb-access`'s and are not restated here. The owner role of the task is read from reference data and is not fixed by this story: Not specified in the source documents (GAP-2223; ASM-3659).

### 11. Data

| BR Field ID | Table in `rwb_case` | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` | id | Read |
| DF-CAS-002 | `recovery_case` | case_no | Read |
| DF-CAS-005 | `recovery_case` | status | Read |
| DF-CAS-006 | `recovery_case` | stage_code, the first checklist key | Read |
| DF-CAS-008 | `recovery_case` | route_code, the second checklist key | Read |
| DF-CAS-013 | `recovery_case` | entry_date, the comparison date of the capture check | Read |
| DF-WRK-009 to DF-WRK-016 | `assignment` | id, case_id, task_id, assignee_user_id, assigned_at, ended_at, reason, rule_id | Read, only as the scope activity of the caller |
| DF-WRK-017 to DF-WRK-026 | `task` | id, case_id, task_code, element_type, discretion, status, owner_role, due_at, completed_at, outcome_code | Write, the missing-document task |
| DF-REF-159 to DF-REF-168 | `reference_version` | id, table_code, version_no, version_label, valid_from, valid_to, status, author_user_id, approver_user_id, approved_at | Read, the `DOCUMENT_CHECKLIST` version in force |
| DF-REF-132 to DF-REF-146 | `parameter_catalog` | param_key, kind, value_type, unit, min_value, max_value, default_value, scope, required, owner_role, environments, used_by, secret, description | Read, the due-date parameter |
| DF-REF-147 to DF-REF-158 | `parameter_value` | param_key, environment, param_value, product_group, version_no, valid_from, valid_to, status | Read, the value in force |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the entry of the task raise: decision code, rule reference, case, missing type, checklist version, task reference, time | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_case` | No row is written by this story; the table is the library's and the case baseline's events use it | None |
| (idempotency) | `idempotency_key` | the stored answer of the internal task raise | Write |

`document_checklist_item`, `case_document_check`, `document`, `document_intake` and `document_field` are the document hub's (P5) and `interaction` is `rwb-source-data`'s (P1): none is read as a table here, and the checklist and document items arrive through the owners' operations (DP-01). The `Case` resource of RWB-P3-E1018-CON does not name `stageCode` and `routeCode` although its field range covers them: Not specified in the source documents (GAP-2223; ASM-3657). Field IDs are those in the Logical Data Model and Data Dictionary v8 and TSD P3 v3 T3.1.

### 12. Contract

#### 12.1 REST operations provided

None new. The case context and the case timeline are served through operations of the case baseline RWB-P3-E1018-CON on base `/api/recovery/case/v1`, owner P3 `rwb-case`; this slice adds no path, no query parameter and no response field, and decides the following behind them:

| Method | Path | API ID | Purpose in this story | Authorization | Errors |
|---|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | API-P3-002 | The case context of a capture: case number, status, entry date, stage code, route code and the caller's task and assignment | Case record `R`, scope applied through the authorise contract | 401; 403 MSG-P4-002; 404 MSG-P4-003; 503 MSG-GEN-006 |
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | API-P3-003 | The `TASK` item of the missing-document task, composed with the other sources of the timeline | Case record `R`, scope applied | 401; 403 MSG-P4-002; 404 MSG-P4-003; 503 MSG-GEN-006 |

The `Case` resource and the `TimelinePage` shape are the baseline's (RWB-P3-E1018-CON, RWB-P3-E1023-CON); the stage code `DF-CAS-006` and the route code `DF-CAS-008` this slice needs are Not specified in the source documents as named fields of that resource (GAP-2223; ASM-3657). The field app uses this operation and no second one: an app-specific path would be a second contract for one resource.

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` | RWB-P4-E1037-CON | The case-scope answer for area `DOCUMENTS`, right `C` and the case as the object reference, with the caller's open task or assignment as the `OWN` activity; one hop, 2 s timeout, breaker. The request and response shape is Not specified in the source documents (GAP-2223; ASM-3657) |
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` | P5 `rwb-document` | API-P5-008; the story that publishes this baseline is not named in the sources (GAP-2223; ASM-3658) | The required document types of the case with their present counts, read once per consumed `DocumentStored` event; one hop, 2 s timeout, and a failed read raises no task |

The reference-data read of DP-07 and the parameters read of DP-06 are this service's own contracts (RWB-P3-E1043-CON, RWB-P3-E1042-CON) and are served inside the service without a hop; this slice is their consumer for the five lists and one parameter it names, and no list value and no number is typed in code.

#### 12.3 Events published

None for this slice. The task is read from the task API and from the case timeline, and this service publishes no event when it raises a task, so the six event types of `rwb.case.events.v1` — `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseAllocationFailed.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.case.TimerBreached.v1` — stay exactly the set the case baseline publishes. The decision-record entry is published by the DP-03 library on `rwb.decision-record.v1` and is not an event of this service's topic.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` (the legacy DocumentStored, EV-16) | `rwb.document.events.v1`, through the inbox of DP-09 | P5 `rwb-document` | One per accepted capture: the trigger of the checklist read of step 8. Deduplicated by event ID; the payload carries no position, no file name and no bill value and none of them is copied into the task or the record |

No other event is consumed: the sync itself is a request on the document hub, and the task is raised from the checklist answer of the hub, not from a case event.

#### 12.5 Workflows and activities

None. This story starts no workflow, registers no activity and signals none. `CaseWorkflow` (workflow ID `case-{caseId}`, task queue `rwb-case` in namespace `rwb-recovery`) is Epic 3 work (ADR-011) and is not used here; the task raise is a synchronous transaction of the service.

#### 12.6 Schedules

None for this story. No Temporal Schedule, no `JOB-nn` and no clock belongs to this path: the only time value here is the due date of the task, which is a parameter row.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `recovery_case` | P3 (`rwb_case`) | The case context: id, case_no, status, stage_code, route_code, entry_date — read only |
| `task` | P3 (`rwb_case`) | The missing-document task: written once per case and missing type, read by the timeline |
| `assignment` | P3 (`rwb_case`) | The scope activity of the caller: read only |
| `reference_version` | P3 (`rwb_case`) | The `DOCUMENT_CHECKLIST` version in force: read only |
| `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | The due-date parameter of the task: read only |
| decision-record library table | PLT library, created in `rwb_case` | The entry of the task raise, in the same transaction as the task |
| `processed_event`, `idempotency_key` | PLT library, created in `rwb_case` | The inbox row of the document event and the idempotency key of the raise (DP-09) |

`document`, `document_checklist_item`, `case_document_check`, `document_intake` (P5), `interaction` (P1), `role`, `permission` and `masking_rule` (P4) are other services' and are never queried here (DP-01); the checklist and the documents arrive through the owners' operations and the scope answer through the authorise contract.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access authorise WireMock | RWB-P4-E1037-CON | Allowed with scope `OWN` for `FC-01` on `RW-2026-000501`; refused 403 MSG-P4-002 for a role without Documents `C`; refused 404 MSG-P4-003 for `RW-2026-000502`; a forced 2 s timeout |
| document hub checklist WireMock | P5 `rwb-document`, API-P5-008 | The checklist of `RW-2026-000501` with `CHK-2026.11`, `INSPECTION_PHOTO` present and `SETTLEMENT_AGREEMENT` required and missing; an empty checklist; a forced timeout |
| case baseline fake | RWB-P3-E1018-CON | The `Case` resource of the two cases with entry date `2026-10-02`, stage `DEED_IN_LIEU` and the field inspection task of `FC-01` |
| reference-data fixture | this story's test data | `LOV-TASK-STATUS`, `LOV-ELEMENT`, `LOV-DISCRETION`, `LOV-ROLE`, `LOV-SOURCE` and the `DOCUMENT_CHECKLIST` version `CHK-2026.11` |
| parameters fixture | this story's test data | The due-date parameter in force, so no number is in code |
| Kafka `DocumentStored` fixture | `rwb.document.events.v1` | The event for document `DOC-0501-01` and its redelivery for AC8 |
| decision-record fake | RWB-PLT-E1027-CON | The entry write and the publish on `rwb.decision-record.v1`, including a forced failure for TC-E2-024-17 |
| field-capture baseline | RWB-P5-E2024-CON | The ten-item inspection, the offline capture, the entry-date refusal and the two cases, so the case side is tested before the hub is in the environment |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (2 baseline operations used), consumed 2 | The case read and the timeline on `/api/recovery/case/v1`; the authorise call and the checklist read consumed |
| Kafka | Published 0, consumed 1 | `rwb.document.DocumentStored.v1` through the inbox; the decision record on `rwb.decision-record.v1` is the library's |
| Temporal | 0 | No workflow, no activity, no Schedule and no task-queue use in this slice |
| File | None | No file is read or written here: the file, the scan and the store are the document hub's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `case/context`, Java package `th.co.scb.ace.workbench.recovery.case.context`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Every pattern in the metadata has an instance here: DP-01 is the read of `recovery_case`, `assignment`, `task`, `reference_version` and the parameter rows in `rwb_case`; DP-03 the entry of the task raise; DP-06 the due-date parameter; DP-07 the five lists and the checklist version; DP-09 the inbox and the idempotency key (no outbox row, because this slice publishes no event); DP-11 the authorise call and the checklist read with their fakes; DP-15 the one index migration; DP-19 the composite route.

This secondary slice adds no build dependency of its own (metadata H = None): the platform contracts the DP rows name are pulled by the rwb-case baseline stories RWB-P3-E1018-CON and RWB-P3-E1043-CON and the service's platform work, so the story is Day 1 and builds against RWB-P3-E1018-CON and RWB-P5-E2024-CON with their fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseContextController | REST controller | The two operations of 12.1, RFC 9457 problem responses with their message IDs, and the scope application of every read |
| CaseContextService | Service | The case context of a capture: the case row, the caller's task and assignment, the stage and route keys and the entry date |
| CaseScopeResolver | Client | The authorise call of 12.2 with area `DOCUMENTS`, right `C` and the `OWN` activity; one hop, 2 s timeout, breaker, and a refusal never cached as an allow |
| ChecklistVersionReader | Client | The `DOCUMENT_CHECKLIST` version in force through the reference-data contract, and the five lists this slice names |
| DocumentStoredListener | Kafka consumer with the inbox | The document event, deduplicated by event ID, reading the case checklist once per event |
| ChecklistTaskRaiser | Service | The one `task` of a missing required type: code, owner role, discretion and due date from data, and the unique open-task rule |
| DecisionRecordWriter | Service | The DP-03 entry of the task raise, in the same transaction, with the case, missing type, checklist version and task reference |
| CaseTimelineComposer | Service | The `TASK` item on the timeline, with actor `SY-CASEWF` and source system `WORKBENCH` |

**Database and migrations**

- One migration in the per-service Flyway sequence (DP-15): `V2024_1__checklist_task.sql`.
- Constraint `ux_task_case_code_open ON task (case_id, task_code) WHERE status = 'OPEN'`, so a redelivered event or a resent sync cannot open a second task for one missing type (BR6).
- Index `ix_task_case_status ON task (case_id, status)` for the timeline read and the activity lookup, and `ix_assignment_case_assignee ON assignment (case_id, assignee_user_id)` for the scope evidence.
- No new table and no new column beyond those two indexes and the constraint: `task`, `assignment` and `recovery_case` exist in the case baseline.
- The checklist version and the parameter are read through the contracts; no local copy is created.

**Configuration and reference data**

- The `DOCUMENT_CHECKLIST` version in force is read from `reference_version`, never configured; the label `CHK-2026.11` in the tests is Not specified in the source documents (GAP-2223; ASM-3659).
- The task code, the owner role and the discretion of the task are data rows: Not specified in the source documents (GAP-2223; ASM-3659).
- The due date is the parameter value in force through DP-06; the parameter key and its value are Not specified in the source documents (GAP-2223; ASM-3659).
- The decision code of the raise is read from the decision-code list of the ledger: Not specified in the source documents (GAP-2223; ASM-3659).
- No feature flag of this slice's own: a case that cannot be read or authorised must not accept a capture, so the case context has no off state. The legacy flag `rwb.dochub.field-capture` stays the document hub's.

**Build steps**

1. `CaseContextController` and the problem responses on the two operations, with the 401, 403, 404 and 503 shapes; unit test the 404 of MSG-P4-003 for a case outside the scope.
2. `CaseContextService` over the `Case` resource with the entry date, stage code, route code and the caller's task and assignment; contract test AC1, AC2 and AC5 against the case baseline fake.
3. `CaseScopeResolver` against the authorise fake, including the timeout and the open breaker; component test AC3, AC4 and the access case TC-E2-024-16.
4. `ChecklistVersionReader` over the reference-data fixture and the due-date parameter over the parameters fixture; test that a new checklist version is served as data with no code change.
5. `DocumentStoredListener` with the inbox and the checklist read, then `ChecklistTaskRaiser` with the unique open-task rule: component test the redelivery of AC8, the timeout of X5, one task per missing type, no task for a stage with no checklist, and a new task after the earlier one closes (X10).
6. `DecisionRecordWriter` in the same transaction as the task, and the forced failure of TC-E2-024-17: no task, no entry, MSG-P7-003 and an incident.
7. `CaseTimelineComposer` with the `TASK` item, and the contract-fake run of the whole path against RWB-P5-E2024-CON and the case baseline, so the story builds before the hub and `rwb-access` are in the environment.

**Done when.** The tests in section 16 pass; a capture for case `RW-2026-000501` is answered with entry date `2026-10-02` and the case in `OWN` scope, a capture for `RW-2026-000502` is answered 404 MSG-P4-003 with nothing raised, a sync that leaves `SETTLEMENT_AGREEMENT` missing raises exactly one `OPEN` task with its decision-record entry, the task shows on the timeline as a `TASK` item, and no position, file name or bill value appears in the task, the record or a log line.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-003 | The case does not exist, or the caller holds no task and no assignment on it | This case is not in your scope. | This story, on the case read and the scope application |
| MSG-P4-002 | The caller's role does not carry Documents `C` | You cannot {action} here. Your role does not include it. | `rwb-access`, carried unchanged |
| MSG-GEN-006 | The authorise call or the checklist read does not answer | {system} is not available. Your request is queued and will be retried. | This story, on the two client calls |
| MSG-P7-003 | The decision record of the task raise cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the record writer |
| MSG-GEN-002 | A required value of the case read is missing from the request | {field} must be between {min} and {max}. | This story, on the path and query validation |

Every request-level error is an RFC 9457 problem response with `messageId`, `detail` carrying the text with its placeholders filled and the capability area where one applies, and `instance` naming the request. A refusal names the case and the action only: no customer field, no document, no position and no file name is in any message. Thai text for each message follows decision DL10. The message IDs and their text are the legacy ones, carried unchanged from RWB-E2-024 section 14.

### 15. Screens and states

| Screen | State | What this story supplies |
|---|---|---|
| SCR-03 Case record | Ready | The case number, status, entry date, stage and route, and the collector's task, so the field app has the context a capture is checked against |
| SCR-04 Case timeline | List | The `TASK` item of the missing-document task with actor `SY-CASEWF`, source system `WORKBENCH` and its time, newest first |
| SCR-04 Case timeline | Missing document | The task item links to the checklist the hub renders; this story writes no document item |
| SCR-04 Case timeline | Denied | The problem response of MSG-P4-003 when the case is outside the caller's scope, with no item and no case data |
| SCR-30 Case documents | List | Nothing beyond the case it is read for: the captures, the checklist panel and the position are the document hub's |

No screen is built here. The screens belong to the case record view (RWB-P3-E1023-APP, RWB-P3-E2016-APP) and the document hub (SCR-30, RWB-P5-E1026-APP), served through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON); the field app screens are the field app's and are not in this or any Workbench story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-024-16 | AC3, AC4, BR2 | Component | `FC-01` with the field inspection task on `RW-2026-000501` is allowed with scope `OWN`; `FC-01` with no task and no assignment on `RW-2026-000502` is refused 404 MSG-P4-003 and nothing is raised |
| TC-E2-024-17 | AC6, BR7 | NFR | The decision record forced to fail during a sync of three files: no task raised, no entry, MSG-P7-003, an incident raised |
| TC-E2-024-01 | AC1, AC2, AC5, AC7, BR1, BR4 | Contract | Case `RW-2026-000501`, entry date `2026-10-02`, stage `DEED_IN_LIEU`, checklist version `CHK-2026.11`, ten stored documents and one `OPEN` task on the timeline |
| TC-E2-024-02 | AC1, BR1 | Component | The context read before the batch: case number, status `IN_PROGRESS`, entry date `2026-10-02`, the task of `FC-01`, and no customer field |
| TC-E2-024-03 | AC5, AC6, BR4, BR5 | Contract | A utility bill stored for the case satisfies the `UTILITY_BILL` item: no task is raised for it and no checklist row is written in `rwb_case` |
| TC-E2-024-04 | AC6, AC7, AC8, BR6 | Component | The same `DocumentStored` event for `DOC-0501-01` delivered twice: one task, one decision-record entry, one inbox row |
| TC-E2-024-05 | AC8, BR6 | Component | Six of ten items received, then all ten: one task per missing type and no duplicate for the six |
| TC-E2-024-06 | AC1, AC2, BR1, BR3 | Contract | A photo with no position: the case answer is unchanged and the entry date is still `2026-10-02` |
| TC-E2-024-07 | AC2, BR3 | Contract | The sync received at `2026-12-15 14:20`; the answer carries the entry date and no clock, so the skew check stays the hub's |
| TC-E2-024-08 | AC2, BR3 | Contract | A capture at `2026-10-01 09:00` against entry date `2026-10-02`: the refusal names `2026-10-02` and no case row changes |
| TC-E2-024-09 | AC2, BR3 | Contract | Captures 31 days and 30 days before the sync: the answer carries the entry date only and the age boundary is asserted in RWB-P5-E2024-APP |
| TC-E2-024-10 | AC1, AC5, BR1 | Component | A HEIC file refused by the hub: the case context is unaffected and the checklist read still runs |
| TC-E2-024-11 | AC1, AC6, BR5 | Component | An EICAR file quarantined by the hub: no item is satisfied, so the task for the missing type is raised |
| TC-E2-024-12 | AC2, AC4, BR2 | Component | Case `RW-2026-000502` where `FC-01` holds no task: 404 MSG-P4-003 on the read and nothing raised |
| TC-E2-024-13 | AC5, AC6, BR5 | Contract | A bill field at confidence 0.5500 in review: the `UTILITY_BILL` item counts as present and no task is raised |
| TC-E2-024-14 | AC1, AC3, BR1 | Contract | A manifest of three items and two files refused with 422 by the hub: the case context and the scope answer are unaffected |
| TC-E2-024-15 | AC6, AC8, BR6 | Contract | 51 files refused with 413: nothing is stored, so every missing required type raises one task and no type gets two |

The legacy level System maps to Contract or Component, Access to Component and Resilience to NFR, and each case asserts only this slice's answers and its one record. No case ID carries the `-ITG` suffix here: the integration copy of the set is RWB-ITG-E2024-ITG, which proves the same facts across `rwb-case`, `rwb-document`, `rwb-access` and `rwb-decision` with real services, and the `-ITG` copies belong to that story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the case status, stage and route values, the task code, the owner role, the discretion, the task status, the source system, the checklist version and the due date are data rows read through DP-06 and DP-07; the Java code holds none of them.
- No personal data in logs, events, tests, workflow history or prompts: the context carries the case and not the customer, and the task and record carry the case, the missing type, the checklist version and the task reference; a test scans both for any part of a position, a file name or a bill value.
- The position, the photo and the file stay with the document hub: this service receives no coordinate, no file name and no bill value, and holds no copy of a document.
- No read of another service's tables and no cross-schema read (DP-01): `document`, `document_checklist_item`, `case_document_check`, `document_intake`, `interaction`, `role`, `permission` and `masking_rule` are never queried here.
- ACE data only through the owner's contract or a `v_ace_*` view of this service; this story reads no ACE view at all, because the case row it reads is its own.
- A task is never raised without its decision record, and the two commit in one transaction (R-UNI-39, BR7).
- A missing answer from `rwb-access` or from the hub is a refusal or a no-op, never a default allow and never a task without evidence; the authorise answer is not cached as an allow across a case.
- Idempotency twice over: the inbox deduplicates the document event by event ID, and `ux_task_case_code_open` keeps one open task per case and missing type.
- The case context has no off switch, because a capture that cannot be tied to its case must not be accepted; the legacy capture flag stays the document hub's.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-21 | 13 Manage documents and correspondence | BR1 to BR9; R-DIL-22, R-UNI-39, R-UNI-40 | TC-E2-024-01 to TC-E2-024-17 |

| Legacy reference | Where it is kept |
|---|---|
| Case `RW-2026-000501`, entry date `2026-10-02`, collector `FC-01` with role `RW-FIELDCOL`, case `RW-2026-000502` with no task | Background, AC1 to AC4, AC8, sections 3, 12.8, 16 |
| The entry-date rule of legacy BR3 and the refusal of legacy AC8 | Sections 1, 7 (AC2), 8 (BR3), 16 |
| The scope rule of legacy AC12 and X7, and the task that makes a case `OWN` | Sections 1, 4, 5 (X2), 8 (BR2), 10, 16 |
| The checklist values of R-DIL-22 and the missing checklist document | Sections 1, 3, 7 (AC5, AC6), 8 (BR4, BR5), 16 |
| MSG-P4-002, MSG-P4-003, MSG-GEN-006, MSG-P7-003 | Section 14 and the exception paths |
| The ten-file inspection values `2026-12-15 14:20`, `13.7563`, `100.5018` and the offline capture at `2026-12-14 10:05` | Background, sections 7 and 16 |
| Legacy key RWB-E2-024, legacy AC1 to AC15 and TC-E2-024-01 to TC-E2-024-17 | Metadata, section 7 note, section 16 |
| Story RWB-P3-E2024-APP, contract RWB-P5-E2024-CON, case baseline RWB-P3-E1018-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The capture itself: the upload, the manifest and its matching, the file-count and size limits, the virus scan, the OCR, the classification, the extraction, the bill threshold and the review queue (`rwb-document`, RWB-P5-E2024-APP, RWB-P5-E2024-CON, RWB-P5-E1024-APP, RWB-P5-E1053-APP, RWB-P5-E1054-APP).
- The checklist rows and the completeness check: `document_checklist_item`, `case_document_check` and the checklist panel (`rwb-document`, P5).
- The rights, the scope policy, the masking answer and the access entry of the capture path (`rwb-access`, RWB-P4-E2024-APP, RWB-P4-E1037-CON).
- The field app itself and its offline store, and agency field teams reaching the Workbench through the external gateway (DL03; FEAT-PRM-15, Epic 7).
- The inspection task, the checklist rule of R-DIL-22 and the asset unlock rule (FEAT-TRT-15, Epic 3), which this story gives a document trail but does not execute.
- The repossessed vehicle photo standard (CTL-38, Epic 7).
- The case record view and the case timeline screens themselves (RWB-P3-E1023-APP, RWB-P3-E2016-APP), which this story feeds and does not build.
- The reference load path of this service — the `DOCUMENT_CHECKLIST` load, its approval, verification and rollback (RWB-P3-E1043-APP) — and the parameters administration (RWB-P3-E1045-APP).
- The task API's completion path (`PATCH /api/recovery/case/v1/tasks/{taskId}`, API-P3-009), which is the case record and task story's.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this path (an OPS story of this legacy key).
