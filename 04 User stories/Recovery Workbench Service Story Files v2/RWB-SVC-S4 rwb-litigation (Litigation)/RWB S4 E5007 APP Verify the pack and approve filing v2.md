# RWB-S4-E5007-APP Verify the pack and approve filing

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-H |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5007-APP-16) |
| Depends on (build) | RWB-S4-E5007-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract version | v1 (base `/api/recovery/litigation/v1`, DP-13) |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Requirement trace | Not specified in the source documents (GAP-2769) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E5-007 for rwb-litigation (S4). The pack of a case is verified against the defect list and the filing is authorised on the legal action of the pack, on base `/api/recovery/litigation/v1` (DP-13), with R-LIT-16, R-LIT-04 and R-LIT-11 evaluated in the service and one decision record written before anything moves through the local decision-record library (DP-03); the two screens are read through the gateway-bff composite route (DP-19). The case, its tasks and timers, the pack documents and defect list, the notice and its template status, the approval item at D7 and the firm selection stay with rwb-case, rwb-document, rwb-comms, rwb-decision and the sibling story, and are consumed and faked (GAP-2765, GAP-2766; ASM-4599, ASM-4600). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 18 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the pack of a case verified against the defect list, the filing authorised, and the notice-withdrawn hold and the prescription-warning escalation of R-LIT-04, R-LIT-11 and R-LIT-16 evaluated on one tracked legal action — with one decision record written before any of it moves —**, so that **a case reaches court in six days with a complete pack, and the case, its tasks and timers, the pack documents, the notice, the approval and the firm stay with the services that own them**.

This story owns the legal action of the pack and three rule evaluations, and nothing else:

- the three legal-action operations of TSD S4 T-A on base `/api/recovery/litigation/v1`: API-S4-002 create, API-S4-003 read and API-S4-004 patch, keeping their legacy operation IDs (DP-13);
- the `legal_action` row of schema `rwb_litigation` with its columns DF-LEG-001 to DF-LEG-014, the pack's action as one value of `action_type` (`NOTICE` or `CIVIL_CASE` of LOV-LEGAL-TYPE) and its status against LOV-LEGAL-STATUS (TSD S4 T3.1 and T3.2);
- the evaluation of R-LIT-16 (every defect list item present, present the pack for verification, to `PACK_VERIFIED`), of R-LIT-04 (template withdrawn, hold generation and raise a task to the litigation officer, to `NOTICE_BLOCKED`) and of R-LIT-11 (prescription warning at 90 days or fewer, Head of Litigation approves substituted service or filing where the law allows, to `PACK_ASSEMBLY`), and the one decision record each writes through the local decision-record library with the rule ID and the version in force (DP-03, legacy AC1, AC2 and AC3);
- the filing authorisation that R-LIT-23 reads on `PACK_APPROVED`, announced to rwb-case; the firm selection R-LIT-23 then performs is `RWB-S4-E5008-APP`'s;
- the consumed calls to rwb-document (the pack and the defect list), rwb-comms (the notice and its template status), rwb-case (the case state, the task, the timer and prescription date, the route fact) and rwb-decision (the D7 approval item of R-LIT-11), all faked.

It does not own the case, its tasks or its timers (rwb-case, P3), the pack documents, the checklist and the defect list (rwb-document, P5), the notice, its template and its dispatch (rwb-comms, P6), the decision ledger, the delegation table and the approval item (rwb-decision, P7), the firm selection and instruction (`RWB-S4-E5008-APP`), or the notice approval operation API-S4-001, which is first in E2. No component of this story writes a `recovery_case`, `task`, `timer`, `notice`, `document`, `decision_log_entry` or `rule_row` row, and none reads a `v_ace_*` view (GAP-2765, GAP-2766; ASM-4599, ASM-4600).

### 2. Business rationale

Litigation takes 21 days to file, packs are incomplete and law-firm progress is not tracked (FSD S4 v3 A1.3, A2.7.1). The legacy story wrote the pack verification, the notice hold, the task, the prescription escalation and the decision log entry in one process against one `recovery` schema and one API base. In the target the same act is cut in five: the legal action of the pack and its rule answers are litigation's; the pack documents and the defect list are the document hub's; the notice and its template status are the communications service's; the case, its route state, its task and its timers are the case of record's; and the credit for the approval is the decision centre's.

This story is the litigation slice. The officer verifies the pack, and R-LIT-16 fires when every defect list item is present: it presents the pack for verification and moves the case to `PACK_VERIFIED`; the officer then authorises the filing on the same legal action, which is the `PACK_APPROVED` fact R-LIT-23 reads before the firm is selected (`RWB-S4-E5008-APP`). R-LIT-04 holds the generation when the template of the notice is withdrawn and raises the task a person must work; R-LIT-11 escalates to the Head of Litigation when 90 days or fewer remain to prescription, because the legal deadline never pauses. Each answer is written as a decision record before the legal action or the case fact changes, so a failed write changes nothing and the officer sees MSG-P7-003 — legacy AC4, and the DP-03 pattern applied where the legacy `DecisionLogWriter` sat (TSD S4 T2, "writes the decision log entry before any change").

Three facts are no longer this service's to reach, and the story is built so that it cannot reach them. The case, its route state, its task and its timers are rwb-case's: this service evaluates the rule, announces the route fact and the task on the case contract and accepts the answer; it writes no case, task or timer row (BR3). The pack and its defect list are rwb-document's: the defect-list result arrives as an answer, never as a table read (BR4). The notice and its template status are rwb-comms's, and the approval item at D7 with its delegation table is rwb-decision's (BR2, BR5).

The legacy in-process writes are retired rather than restated: no `recovery_case`, `task`, `timer`, `notice`, `document`, `decision_log_entry` or `rule_row` row is written here, and the monolith API base is not served by any path of this service (DP-13). The list values of `action_type` and `status` are read with their version in force, never written in code (BR6). The two screens are read through the gateway-bff composite route (DP-19, BR7).

It serves FEAT-LIT-07 "Verify the pack and approve filing" and the module requirement REQ-S4-003 "The litigation officer verifies the pack against the defect list before filing is approved", and it carries the FSD measure "litigation turnaround, 6 days" by putting the verification, the hold and the escalation on one tracked legal action. The legacy story master carries no requirement ID, so the story traces to REQ-S4-003 and to FEAT-LIT-07 until the PRD adds the identifiers (GAP-2769; ASM-4603). Its four legacy criteria are copied word for word in section 7.

### 3. Preconditions

- `RWB-S4-E5007-CON` is published: the three operations on `/api/recovery/litigation/v1`, the `LegalActionRequest`, `LegalAction`, `LegalActionUpdate` and pack-verification elements, the error envelope, the `Idempotency-Key` rule and the fakes. This story builds against it on Day 1, and it is the first build dependency.
- The `legal_action` table exists in schema `rwb_litigation` with the columns DF-LEG-001 to DF-LEG-014 of TSD S4 T3.1 and the standard columns of T3.0; no new table and no new column is created by this story.
- The local decision-record library and the shared record format of DP-03 are live (`RWB-PLT-E1027-CON`); the record is hash-linked on the shared topic `rwb.decision-record.v1`. The story builds against the library's fake until the platform contract story publishes.
- The gateway-bff composite route `RWB-PLT-N001-CON` serves SCR-18 Notice approval and SCR-19 Litigation workspace (DP-19), so both read surfaces are available from Day 1.
- The pack and defect-list read of rwb-document (P5), the notice and template-status read of rwb-comms (P6), the case read with its task raise and its prescription fact (P3) and the D7 approval item of rwb-decision (P7) are published and faked. **None of the four is in this story's dependency rows** and no source names their operations; every one carries `Not specified in the source documents (GAP-2765; ASM-4599)` (GAP-2766, GAP-2768; ASM-4599, ASM-4602).
- LOV-LEGAL-TYPE (`NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION`) and LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) of TSD S4 T3.2 are read as values in force on the reference data of rwb-case. DP-07 is not in this story's pattern set and the read carries no dependency row either (GAP-2765; ASM-4599).
- The caller holds a Workbench role with the Litigation right of the operation it calls (TSD S4 T6.1, legacy permission block). DP-08 is not in this story's pattern set: the declared right of the screen path is enforced at the edge and the right of the write paths is this story's design.
- The service runs as its own login on schema `rwb_litigation` (DP-01, DP-02); it holds no grant on another `rwb_*` schema and no `v_ace_*` grant.

### 4. Flow

1. The litigation officer opens SCR-19 Litigation workspace for a case in `PACK_ASSEMBLY` through the gateway-bff composite route (DP-19), and reads the legal action of the pack on `GET /legal-actions/{legalActionId}` of base `/api/recovery/litigation/v1` (API-S4-003): `action_type`, `status`, `court_name`, `claim_amount`, `law_firm_id`, `filed_date` and the court references. Personal data classification of these fields: Not specified in the source documents (DOR-RWB-S4-E5007-APP-11).
2. `PackReadClient` asks rwb-document for the pack and its defect-list result: the pack reference, the document list, the checklist version and the missing items. The operation is Not specified in the source documents (GAP-2765; ASM-4599).
3. `NoticeStateClient` asks rwb-comms for the notice of the case and its template status (`current` or `withdrawn`) with the template version. The operation is Not specified in the source documents (GAP-2765; ASM-4599).
4. `PackValidator` checks the case reference, the caller's scope and the state the step needs. A failed check answers 404, 409 or 422 and nothing is written.
5. `TemplateWithdrawnCheck` evaluates R-LIT-04 when the template status is `withdrawn`: it holds generation, writes the decision record and raises the task to the litigation officer on the case contract. A missing defect item raises MSG-S4-001 and blocks the approval (VR-S4-007-1).
6. `PackVerificationDecisionWriter` evaluates R-LIT-16 against the defect-list result — every item present is the only condition, and the checklist rows are versioned reference data, never code — and writes one decision record through the local decision-record library **before** the legal action changes: the rule ID `R-LIT-16`, the version in force, the inputs reference, the outcome and the decision code.
7. `LegalActionWriter` writes, in one `rwb_litigation` transaction, the `legal_action` facts of the verification (the pack reference and the defect-list result reference against the contract element of `RWB-S4-E5007-CON`) and the idempotency row of the request. When the officer rejects the pack at verification, R-LIT-21 fires instead: the pack returns for rework and the case moves back to `PACK_ASSEMBLY`.
8. `CaseRouteClient` announces the route fact to rwb-case — `PACK_VERIFIED` on R-LIT-16, `PACK_ASSEMBLY` on R-LIT-04 for the hold or on R-LIT-21 for the rejection, `NOTICE_BLOCKED` on R-LIT-04 — with the rule ID, the version and the legal action reference, and accepts the answer. rwb-case writes the case, its task and its timer; this service writes none of them (BR3). The operation names are Not specified in the source documents (GAP-2765; ASM-4599).
9. The officer authorises the filing on `PATCH /legal-actions/{legalActionId}` (API-S4-004) with the authorisation element of `RWB-S4-E5007-CON`: the approval code, the rule ID and its version, the pack reference, the `Idempotency-Key`. One decision record is written before the change, and the `PACK_APPROVED` fact is announced to rwb-case; the firm selection on R-LIT-23 is `RWB-S4-E5008-APP`'s and is not made here.
10. The prescription path: the case read of rwb-case carries the prescription date and the days remaining. When 90 days or fewer remain, `PrescriptionWarningCheck` shows MSG-S4-002 with the date and R-LIT-11 fires: one decision record is written and an approval item is raised at D7 for the Head of Litigation on the rwb-decision contract, with the case reference, the legal action reference, the decision code, the capability area, the product group, the amount used for the limit, the rule ID and its version. The delegation level and the clock are rwb-decision's.
11. On a granted answer, the officer records the filing authorisation as allowed and the `PACK_ASSEMBLY` route fact is announced to rwb-case, which moves the case. On a refused answer the legal action keeps what it wrote and no route fact leaves the service.
12. A repeated authorisation with the same `Idempotency-Key`, or the same verification twice, writes once, sends no second decision record and no second approval item, and the repeat is counted under R-UNI-40.
13. SCR-18 and SCR-19 read the legal action and its states from this service through the composite route, read only, next to the case route state of rwb-case, the pack of rwb-document and the notice of rwb-comms. Screen states for SCR-18 and SCR-19: an empty state when the case has no legal action (text Not specified in the source documents (DOR-RWB-S4-E5007-APP-10)); a loading state while the composite route answers; an error state on the 401, 404, 409 and 503 answers (message IDs Not specified in the source documents (CG-ALL-9139)); a no-access state on the 403 answer with MSG-P4-002.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field of the request is absent or invalid, or a value falls outside LOV-LEGAL-TYPE or LOV-LEGAL-STATUS | The answer is 422 and nothing is read beyond the validator; no decision record and no row | MSG-GEN-001 | AC1 |
| X2 | The case ID or the legal action ID names no object in the caller's scope | The answer is 404 and nothing is written; an out-of-scope case cannot be told from a missing one | None | AC1 |
| X3 | The legal action is not in the status the step needs, or the case route state is not `PACK_ASSEMBLY` | The answer is 409, nothing changes and no route fact is announced | None | AC1 |
| X4 | One or more defect list items are missing when the officer tries to approve the filing | The approval is refused, the missing items are named and the pack returns for rework under R-LIT-21; no decision record of the approval is written | MSG-S4-001 | AC1 |
| X5 | The template of the notice is `withdrawn` | R-LIT-04 holds the generation, the decision record is written, the task is raised to the litigation officer and the case moves to `NOTICE_BLOCKED` | None | AC2 |
| X6 | The claim expiry of the case falls inside 90 days | The MSG-S4-002 warning is shown with the date, and the action is not blocked by the warning itself | MSG-S4-002 | AC3 |
| X7 | A role without the Litigation right verifies or authorises the filing | Refused before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, AC2, AC3 |
| X8 | The local decision-record write fails | The transaction writes nothing: the legal action keeps its previous facts, no task is raised, no approval item is raised and no route fact leaves the service | MSG-P7-003 | AC4 |
| X9 | A consumed contract does not answer inside 2 s, or its breaker is open | The legal action keeps what it wrote, because that fact is true and this service's own; the answer is 503 with the platform error envelope and the hand-off is re-run by repeating the same `Idempotency-Key` | None | AC1 |
| X10 | The case answer refuses the route fact or the task raise | The legal action keeps what it wrote, the refusal is recorded for the case owner and the caller reads the answer of the case contract unchanged; this service does not move the case itself | None | AC2, AC3 |
| X11 | The Head of Litigation refuses the substituted service or the filing at D7 | No route fact leaves the service, the legal action keeps its facts and the refusal and its reason are on the decision record; the prescription clock keeps running on the case | None | AC3 |
| X12 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5 (BR8) |

**Messages.** The message IDs of this story and their English wording are those of the FSD character for character; the Thai wording, the field-level text of MSG-GEN-001 and the approver stay with the message work that DL10 names (GAP-1748).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S4-E5007-CON`, the decision-record library and the composite route; the four consumed owners are faked, and the absent dependency rows are recorded (GAP-2765, GAP-2766) |
| Negotiable | The defect list, the template-status values, the D7 delegation level and the list values are versioned reference data; the story fixes the behaviour and the shapes, not the values |
| Valuable | The pack is verified and the filing authorised on one tracked legal action with a decision record before it moves, which is the 21-day to 6-day turnaround of the module, and the hold and the prescription escalation are no longer a spreadsheet |
| Estimable | Three operations, one validator, three rule evaluations, one library write per answer, one repository write, four clients and one read-only screen fragment |
| Small | Fits two weeks with its tests, as the primary slice of the legacy key |
| Testable | Each of the four criteria of section 7 is one end-to-end test with the cross-service answers stubbed in the contract fakes; the contract half is tested in `RWB-S4-E5007-CON` |

### 7. Acceptance criteria

```gherkin
Feature: Verify the pack and approve filing, in rwb-litigation

  Background:
    Given the legal action "LA-2026-000704" of the pack exists on case "RC-2026-000704"
    Given the rule package of R-LIT-04, R-LIT-11 and R-LIT-16 is in force at its version, and LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are read with their version in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Verify the pack and approve filing (legacy RWB-E5-007 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-document contract mock returns the pack with every defect list item present for "RC-2026-000704"
    Given the rwb-case contract mock returns the case state "PACK_ASSEMBLY" for "RC-2026-000704"
    When the user acts on the screen
    Then lets the litigation officer confirm the pack and authorize the filing
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-LIT-04 (legacy RWB-E5-007 AC2)
    Given a case in state NOTICE_GENERATED
    Given the rwb-comms contract mock returns template status "withdrawn" for notice "NT-2026-000704"
    Given the rwb-case contract mock returns the case state "NOTICE_GENERATED" for "RC-2026-000704"
    When template withdrawn
    Then hold generation and raise a task to the litigation officer
    Then the case moves to NOTICE_BLOCKED

  Scenario: AC3 Rule R-LIT-11 (legacy RWB-E5-007 AC3)
    Given a case in state NOTICE_UNSERVED
    Given the rwb-case contract mock returns "90" prescription days remaining for "RC-2026-000704"
    Given the rwb-decision contract mock returns the approval of the Head of Litigation granted for "LA-2026-000704"
    When prescription warning
    Then head of Litigation approves substituted service or filing where the law allows
    Then the case moves to PACK_ASSEMBLY

  Scenario: AC4 Not recorded (legacy RWB-E5-007 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Schema boundary (new, D-RCV-60)
    Given a component, a statement or a test that reads another `rwb_*` schema, a `v_ace_*` view or an ACE table
    When the boundary test runs in the pipeline
    Then the grant refuses the statement, the build fails and nothing is released

  Scenario: AC6 A consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-case contract mock does not answer for "RC-2026-000704"
    When the officer confirms the pack and authorizes the filing
    Then the legal action keeps what it wrote, the answer is 503 with the platform error envelope and the hand-off is re-run by repeating the same `Idempotency-Key`

  Scenario: AC7 A status change the model does not allow is refused (new, D-RCV-60)
    Given the legal action "LA-2026-000704" is not in the status the step needs
    When the officer confirms the pack and authorizes the filing
    Then the answer is 409, nothing changes and no route fact is announced

  Scenario: AC8 Error answers of the provided operations (new, D-RCV-60)
    Given a call to API-S4-002, API-S4-003 or API-S4-004 without a valid credential
    When the call is made
    Then the answer is 401 with the platform error envelope and nothing is written
    Given a call to API-S4-002, API-S4-003 or API-S4-004 by a role without the Litigation right
    When the call is made
    Then the answer is 403 with MSG-P4-002 and nothing is written
    Given a call to API-S4-003 for a legal action that does not exist
    When the call is made
    Then the answer is 404 with the platform error envelope

  Scenario: AC9 Replay of a write with the same idempotency key (new, D-RCV-60)
    Given the legal action `LA-2026-000704` has been written by a call with an `Idempotency-Key`
    When the same call is repeated with the same `Idempotency-Key`
    Then the legal action is written once, the answer is the same as the first answer and the repeat is counted

  Scenario: AC10 Retry or timeout of an activity (new, D-RCV-60)
    Given an activity of the pack verification times out before its answer is received
    When the activity is retried
    Then the legal action is written once, the decision record is written once and no second task or approval item is raised

  Scenario: AC11 Rules BR1, BR2, BR4, BR5, BR6 and BR7 hold in the write path (new, D-RCV-60)
    Given the verification or the filing authorisation of `LA-2026-000704` is written
    When the write path is checked
    Then the decision record is written before the legal action changes, the result is written on the `legal_action` row only, and no document, notice, approval, case or personal-data field is written
    Then `action_type` and `status` take only the values of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS in force, with their version
```

These four criteria (AC1 to AC4) are the legacy criteria of RWB-E5-007, copied word for word, except that the term 'decision log' now reads 'decision record' in AC1 and AC4 (CG-ALL-9149) (AC5 to AC11 are the criteria this story adds): no other legacy line is reworded, shortened or renumbered, and every value of the source (`NOTICE_GENERATED`, `NOTICE_UNSERVED`, `PACK_ASSEMBLY`, `NOTICE_BLOCKED`, MSG-S4-001, MSG-P7-003) is kept character for character. The only additions are the origin tag on each `Scenario:` line, the criteria AC5 to AC11 and, inside the criteria whose cross-service part is mocked, one `Given` line per answer no source gives in process: the pack of rwb-document, the case state of rwb-case, the template status of rwb-comms and the D7 approval of rwb-decision are answered by their contract fakes, every other line and every value unchanged. The case route states of AC2 and AC3 are route states of the case of record, moved by rwb-case on the announcement of this service (BR3); the status of the legal action itself stays `OPEN` until a filing date is written (section 9). The contract half of these surfaces is tested in `RWB-S4-E5007-CON`, and the end-to-end journey across the four services is not claimed here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| R-LIT-04 | Litigation · D7 · from `NOTICE_GENERATED` · event `TEMPLATE_WITHDRAWN` · condition "template_status = withdrawn" · action "hold generation and raise a task to the litigation officer" · to `NOTICE_BLOCKED` · owner "Litigation officer" · channel "Workbench, the Workbench document hub" · service level 1 working day | Business Rules and Routing Logic v4 (R-LIT-04); FSD S4 A2.7.3.1; TSD S4 T4 |
| R-LIT-11 | Litigation · D7 · from `NOTICE_UNSERVED` · event `PRESCRIPTION_WARNING` · condition "prescription_days_remaining <= 90" · action "Head of Litigation approves substituted service or filing where the law allows" · to `PACK_ASSEMBLY` · owner "Head of Litigation" · channel "Workbench, Workbench scheduler" · service level "to the prescription date" | Business Rules and Routing Logic v4 (R-LIT-11); FSD S4 A2.7.3.1; TSD S4 T4 |
| R-LIT-16 | Litigation · D7 · from `PACK_ASSEMBLY` · event `PACK_COMPLETE` · condition "every defect list item present" · action "present the pack to the litigation officer for verification" · to `PACK_VERIFIED` · owner "Litigation officer" · channel "Document Hub, CCMS, LHS, the Workbench document hub" · service level 2 working days | Business Rules and Routing Logic v4 (R-LIT-16); FSD S4 A2.7.3.1; TSD S4 T4 |
| R-LIT-21 | From `PACK_VERIFIED`, on `OFFICER_REJECTED_PACK`, the pack returns to the legal document agent for rework and the case moves to `PACK_ASSEMBLY`; the rejecting act is on the same screen and announces no approval | Business Rules and Routing Logic v4 (R-LIT-21); FSD S4 A2.4.3.1 |
| R-LIT-23 | From `PACK_VERIFIED`, on `PACK_APPROVED` with `verified_at` set, the firm is selected by rule from the panel and the case moves to `FIRM_SELECTION`; this story writes the `PACK_APPROVED` fact and announces it, and the selection is `RWB-S4-E5008-APP`'s | Business Rules and Routing Logic v4 (R-LIT-23); FSD S4 A2.8.3.1 |
| BR1 | The legal action of the pack is a `legal_action` row of this service: `action_type` takes the value `NOTICE` or `CIVIL_CASE` of LOV-LEGAL-TYPE, and the verification and the filing authorisation are written on that row and nowhere else | TSD S4 T3.1, T3.2; Architecture v5 slide 41 (S4 owns legal actions); legacy Data block |
| BR2 | The decision is written before the legal action changes: one record per rule answer through the local decision-record library, with the rule ID and the version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2; R-UNI-39; legacy AC1 and AC4 |
| BR3 | The case, its route state, its task and its timers are answered, not written: this service announces the route fact and the task raise with the rule and its version and accepts the answer; no `recovery_case`, `task` or `timer` row is written and no case rule is evaluated here | R-LIT-16, R-LIT-04, R-LIT-11; Architecture v5 slide 4 (P3 case and workflow); FSD S4 existing capability check (stages and sentries from P3); GAP-2766; ASM-4600 |
| BR4 | The pack, its documents and the defect list are rwb-document's: the defect-list result and the checklist version arrive as an answer and are never read as a table, and no `document` row is written here | DP-01, DP-11; Architecture v5 slide 4 (P5 document hub); GAP-2765; ASM-4599 |
| BR5 | The notice and its template status are rwb-comms's and the approval item at D7 with its delegation table is rwb-decision's; this service reads the status, writes the decision record and raises the item, and approves nothing itself | Architecture v5 slide 4 (P6, P7); TSD S4 T5.2; GAP-2766; ASM-4600 |
| BR6 | Closed vocabulary: `action_type` and `status` take only the values of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS in force, read with their version; the checklist rows, the template-status values and the 90-day threshold are versioned reference data and are never written in code | TSD S4 T3.2; FSD S4 A2.7.3.1 (BR-S4-007); Template and Rules section R7.2 (s17) |
| BR7 | No personal data: the row, the decision record, the log and every call carry identifiers, list values, dates and amounts only; no name, address, identity number or account number enters this service | TSD S4 T3.1; Architecture v5 slides 42 and 43 notes |
| BR8 | No ACE read and no cross-schema read: the service holds no `v_ace_*` grant and no grant on another `rwb_*` schema, and its login refuses such a statement | DP-01, DP-05 as a prohibition; Architecture v5 slide 29 |
| R-UNI-39 | An action whose decision cannot be recorded does not proceed and nothing moves | Business Rules and Routing Logic v4 (R-UNI-39); legacy AC4 |
| R-UNI-40 | The same event or the same request twice produces one effect, and the repeat is counted | Business Rules and Routing Logic v4 (R-UNI-40) |

The 90-day threshold of R-LIT-11 and the checklist rows of R-LIT-16 are named by the rules and defined by no source read for this key, so they are read as versioned reference rows of the business and never as code: the placeholder `Not specified in the source documents (GAP-2767; ASM-4601)` stands in the configuration of section 13.

**Coverage of the rules.** The rule rows R-LIT-04, R-LIT-11, R-LIT-16, R-LIT-21, R-LIT-23, R-UNI-39 and R-UNI-40 take their identifier from the source rule and carry no BR ID, by the source's own numbering. The rules are covered as follows: BR1 by AC1 and TC-E5-007-01; BR2 by AC1, AC4, TC-E5-007-01 and TC-E5-007-04; BR4 by AC1 and TC-E5-007-01; BR5 by AC2, AC3, TC-E5-007-02 and TC-E5-007-03; BR6 by the Background and X1, tested by TC-E5-007-01; BR7 and BR8 by AC5 and TC-E5-007-08; BR1, BR2, BR4, BR5, BR6 and BR7 by AC11 and TC-E5-007-14.

### 9. State transitions

This story moves the status of its own legal action and announces route facts of the case. The two are different objects and are never used one for the other.

**`legal_action.status`** — the values of LOV-LEGAL-STATUS (TSD S4 T3.2), moved by this service:

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The legal action of the pack is opened on API-S4-002 | `actionType` is `NOTICE` or `CIVIL_CASE`, the request validates and the decision record is written | `OPEN` |
| `OPEN` | The pack is verified on API-S4-004 | R-LIT-16 fires, every defect list item is present and the decision record is written | `OPEN`, with the `PACK_VERIFIED` route fact announced |
| `OPEN` | The filing is authorised on API-S4-004 | R-LIT-16's verification stands and the decision record is written | `OPEN`, with the `PACK_APPROVED` route fact announced |
| `OPEN` | The filing date is written | `filedDate` is present | `FILED` |
| `FILED` | The judgment is recorded | `judgmentDate` and `judgmentAmount` are written | `JUDGMENT` |
| `JUDGMENT` | Enforcement opens | The enforcement step is recorded | `ENFORCING` |
| `ENFORCING` or `FILED` | The case is closed or the action withdrawn | The closing step of the case of record | `CLOSED` or `WITHDRAWN` |

The verification and the filing authorisation have **no value in LOV-LEGAL-STATUS that names them**, and `legal_action` has no column that stores them, so the row keeps `OPEN` and the two facts live on the decision record and on the case route state: the field and the value are `Not specified in the source documents (GAP-2767; ASM-4601)`.

**The case route states** are rwb-case's, and this story only announces them (BR3):

| From (rwb-case) | Rule and event | To (rwb-case) | Owner of the move |
|---|---|---|---|
| `NOTICE_GENERATED` | R-LIT-04, on `TEMPLATE_WITHDRAWN` | `NOTICE_BLOCKED` | rwb-case, on the announcement of this service |
| `NOTICE_UNSERVED` | R-LIT-11, on `PRESCRIPTION_WARNING` at 90 days or fewer | `PACK_ASSEMBLY` | rwb-case, on the announcement of this service, once the Head of Litigation approves |
| `PACK_ASSEMBLY` | R-LIT-16, on `PACK_COMPLETE` | `PACK_VERIFIED` | rwb-case, on the announcement of this service |
| `PACK_VERIFIED` | R-LIT-21, on `OFFICER_REJECTED_PACK` | `PACK_ASSEMBLY` | rwb-case, on the announcement of this service |
| `PACK_VERIFIED` | R-LIT-23, on `PACK_APPROVED` | `FIRM_SELECTION` | rwb-case, on the announcement of this service; the selection is `RWB-S4-E5008-APP`'s |

Neither the case row nor its route state is read as a table or written here; the case answer and the announcement of 12.2 are the only paths by which the route state moves (GAP-2765; ASM-4599).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA and C on the operations of the pack (TSD S4 T6.1, legacy permission block): opens, reads, verifies and authorises the filing; the primary role of FSD S4 A2.7 |
| RW-ENFORCE, enforcement owner | Litigation C and CRU: opens and reads the legal action of the pack in scope |
| RW-LEGAL, legal counsel | Litigation RA: reads the pack verification and its facts |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Litigation RA: reads, and holds the acknowledgement right of the matrix |
| RW-HEADLIT, Head of Litigation | Litigation RA: reads here; it **approves** the substituted service or the filing of R-LIT-11 inside rwb-decision, not in this service |
| RW-TEAMMGR, RW-CASEOWN, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read the legal action and its facts only |
| rwb-litigation service identity | Validates, evaluates R-LIT-04, R-LIT-11 and R-LIT-16, writes the decision record and the row, and calls the document, comms, case and decision contracts; it holds no grant on another schema and no `v_ace_*` grant |
| rwb-document (P5) service identity | Owns the pack, the checklist and the defect list; answers the pack read |
| rwb-comms (P6) service identity | Owns the notice and its template; answers the notice and template-status read |
| rwb-case (P3) service identity | Owns the case of record, the route states, the task and the timer; answers the route fact and the task raise |
| rwb-decision (P7) service identity | Owns the approval item at D7, the delegation table and its clock; answers granted, refused or delayed |

The rights above are the rows of TSD S4 T6.1 and of the legacy permission block, and nothing wider. The role code of the D7 approver that R-LIT-11 routes to is `Head of Litigation` and its right is held in rwb-decision and rwb-access, not here. DP-08 is not in this story's pattern set: the declared right of the screen path is enforced at the edge and the guard on the write paths is this story's design. A refusal keeps MSG-P4-002 and changes nothing.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Write on create; read as the reference of every call and answer |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Write on create, as a `varchar(255)` business key with no foreign key (DP-01); read and sent on every consumed call |
| DF-LEG-003 | legal_action (S4, `rwb_litigation`) | law_firm_id | Read on the pack screen; the firm is selected by `RWB-S4-E5008-APP` |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Write, `NOTICE` or `CIVIL_CASE` of LOV-LEGAL-TYPE |
| DF-LEG-005 to DF-LEG-008 | legal_action (S4, `rwb_litigation`) | lawsuit_no, black_case_no, red_case_no, court_name | Read; the filing facts are written by the filing story of this service |
| DF-LEG-009 | legal_action (S4, `rwb_litigation`) | claim_amount | Read; the amount the pack and the D7 limit are read against |
| DF-LEG-010 | legal_action (S4, `rwb_litigation`) | filed_date | Read; its presence moves the status to `FILED` |
| DF-LEG-011, DF-LEG-012 | legal_action (S4, `rwb_litigation`) | judgment_date, judgment_amount | Read only |
| DF-LEG-013 | legal_action (S4, `rwb_litigation`) | lit_status | Read only; the court status that arrives from LIT through rwb-source-data |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Write, against LOV-LEGAL-STATUS; it stays `OPEN` until a filing date is written |
| Standard columns | legal_action (S4, `rwb_litigation`) | state, version, created_at, created_by, updated_at, updated_by, is_active | Written by the service identity (TSD S4 T3.0) |
| DF-DEC-003, DF-DEC-004, DF-DEC-005, DF-DEC-008, DF-DEC-012, DF-DEC-016, DF-DEC-017, DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule ID, rule version, inputs reference, final call, decided at, the two hashes | Write through the local library, before the legal action changes |
| DF-WRK-017 to DF-WRK-026 | task (P3, `rwb_case`) | the task raised by R-LIT-04 | Sent on the case contract and stored nowhere here |
| DF-WRK-027 to DF-WRK-036 | timer (P3, `rwb_case`) | the prescription timer of R-LIT-11 | Sent on the case contract and stored nowhere here |
| DF-LEG-015 to DF-LEG-023 | notice (P6, `rwb_comms`) | the notice of the case, its template status and its version | Read on the comms contract only |
| Pack and defect list (P5, `rwb_document`) | document | the pack reference, the document list, the checklist version and the missing items | Read on the document contract only |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | case route state, product group, prescription date and days remaining | Read on the case contract only |
| DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | decision_log_entry and rule_row (P7, `rwb_decision`) | the central ledger and the rule rows of R-LIT-04, R-LIT-11 and R-LIT-16 | Governed and read in rwb-decision; stored nowhere here |

Field IDs are those of TSD S4 v2 T3.1, the legacy data block and the standard columns of TSD S4 T3.0. **No new table, no new column and no migration:** `legal_action` arrives with the S4 schema and the DDL template of `RWB-S4-E5007-CON`, which the service's own Flyway applies (DP-15); `decision_record` and `idempotency_key` are library objects created in `rwb_litigation` by the library's migration (DP-03).

**Terms.** The legacy term 'decision log' in the legacy data block means the decision record of this section; section 7 reads 'decision record' in AC1 and AC4 (CG-ALL-9149).

**Not written, not read as a table, and named here so that a reviewer can check the absence:** `recovery_case`, `task` and `timer` (P3 rwb-case), `document` and the pack (P5 rwb-document), `notice` (P6 rwb-comms), `decision_log_entry` and `rule_row` (P7 rwb-decision), `hearing` and the judgment columns of `legal_action` (S4, the sibling stories'), and every `v_ace_*` view (P1 rwb-source-data). `legal_action.case_id`, `law_firm_id` and the approval references are identifiers, not foreign keys across schemas (DP-01, BR8). The legacy data block gave `recovery_case`, `task`, `timer`, `notice` and `decision_log_entry` as this story's own tables; only `legal_action` is S4's in the Ownership Map, and the difference is recorded (GAP-2766; ASM-4600).

**No personal data.** The row this story writes carries identifiers, list values, dates and one amount. The borrower, the guarantor, the address and the identity number never enter `rwb_litigation`: they are held by ACE and reached only through rwb-source-data by the services that need them, and they are not logged here and not put on any call.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | Open the legal action of the pack, and its decision record (TSD S4 T-A.2) | Litigation C, scope applied | `Idempotency-Key` header required; the answer is stored and a repeat returns it |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | Read the legal action with its pack, instruction, hearings and judgment (TSD S4 T-A.2) | Litigation R, scope applied | Not applicable |
| API-S4-004 | PATCH | `/legal-actions/{legalActionId}` | Record the verification of the pack, the filing authorisation, a filing, a judgment or an enforcement step (TSD S4 T-A.2) | Litigation U, scope applied | `Idempotency-Key` header required |

The three operations and their IDs, rights and error sets are those of TSD S4 T-A.1 and T-A.2; they keep their legacy IDs and differ only in the base, which DP-13 renames. Errors: 401 no session (message ID Not specified in the source documents (CG-ALL-9139)); 403 no right (MSG-P4-002); 404 unknown or out-of-scope reference (message ID Not specified in the source documents (CG-ALL-9139)); 409 a status or a case state that refuses the step (message ID Not specified in the source documents (CG-ALL-9139)); 422 a missing or invalid field (MSG-GEN-001) or a missing defect item; 503 the decision-record library or a consumed contract unavailable (message ID Not specified in the source documents (CG-ALL-9139)). API-S4-001 `POST /notices/{noticeId}/approve` is named by the legacy endpoint block of RWB-E5-007, is first in E2 and belongs to the notice story of this service; it is **not** declared here, and the R-LIT-04 hold of this story approves no notice — it blocks the generation (GAP-2766; ASM-4600). The request and answer shapes are declared by `RWB-S4-E5007-CON`, the first build dependency of this story.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| The pack and defect-list read, operation Not specified in the source documents (GAP-2765; ASM-4599), base `/api/recovery/document/v1` | P5 rwb-document | The pack reference, the document list, the checklist version and the missing items the verification and MSG-S4-001 read |
| The notice and template-status read, operation Not specified in the source documents (GAP-2765; ASM-4599), base `/api/recovery/comms/v1` | P6 rwb-comms | The notice of the case, its template status (`current` or `withdrawn`) and the template version of R-LIT-04 |
| The case read, the task raise and the route fact, operation Not specified in the source documents (GAP-2765; ASM-4599), base `/api/recovery/case/v1` | P3 rwb-case | The case route state, the product group, the prescription date and days remaining; the task raised by R-LIT-04; the route facts `NOTICE_BLOCKED`, `PACK_ASSEMBLY`, `PACK_VERIFIED` and `PACK_APPROVED` |
| The approval item of `RWB-P7-E2013-CON`, base `/api/recovery/decision/v1` | P7 rwb-decision | The D7 approval of the substituted service or the filing under R-LIT-11; the delegation level and the clock are the approval's (operation of the raise Not specified in the source documents (GAP-2765; ASM-4599)) |
| The reference-data read of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS, `RWB-P3-E1043-CON` | P3 rwb-case | The two list codes at their version in force; DP-07 is not in this story's pattern set and the row carries the same gap |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). None of the first four rows is in this story's dependency rows, and no source names their operations: the four are recorded once with GAP-2765 and ASM-4599, and the story builds against their fakes on Day 1. No operation of another service is declared as provided here (BR1).

#### 12.3 Events published

None. The service topic `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14) carries `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` in the event catalogue, and this story publishes none of them: DP-09 is not in its pattern set, so it adds no outbox row and no producer, and no catalogue entry assigns the pack verification or the filing authorisation to an event. The decision record is written through the local decision-record library of DP-03, which relays `DecisionRecorded` (event 08) on the shared `rwb.decision-record.v1`; that element is the library's and this service declares no payload of its own.

#### 12.4 Events consumed

None. The template withdrawal of R-LIT-04 and the prescription warning of R-LIT-11 arrive as synchronous answers of the comms and case contracts (12.2), not as topics: DP-09 is not in this story's pattern set, so this story subscribes to no topic, holds no consumer group and uses no inbox, and it registers no Schedule and no timer of its own — the prescription clock is the case's (GAP-2768; ASM-4602).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| LitigationWorkflow | Workflow, one run per case stage, the S4 child of CaseWorkflow | `rwb-litigation` | The stage that hosts the pack verification, the hold and the escalation; its signals and its outcome for the parent are declared, not built (Temporal design slide 13) |
| verifyPack | Activity | `rwb-litigation` | The pack read, R-LIT-16 and the row write of steps 2 to 7 |
| recordDecision | Activity through the library | `rwb-litigation` | The local decision record and its outbox row, written before the change (DP-03) |
| raiseOfficerTask | Activity | `rwb-litigation` | The task of R-LIT-04 raised on the case contract |
| announceCaseRoute | Activity | `rwb-litigation` | The route fact of 12.2 to rwb-case and its answer |
| authoriseFiling | Activity | `rwb-litigation` | The filing authorisation of step 9 and the `PACK_APPROVED` fact |
| prescriptionApproval | Child workflow, owner rwb-decision | `rwb-decision` | The D7 approval of R-LIT-11 and its clock, built against its fake (GAP-2765; ASM-4599) |

The workflow name is fixed by the Temporal and Drools design (`LitigationWorkflow` on `rwb-litigation`, "LIT 79" in the stage list); the pack step is a step of that workflow and not a workflow of its own, and no activity is registered by a contract document. The child workflow's type name on the decision service is named by no source and is carried as Not specified in the source documents (GAP-2765; ASM-4599). The workflow ID form and the duplicate-start policy of LitigationWorkflow are Not specified in the source documents (CG-ALL-9141); the Temporal Catalog v1 start row reads: Litigation route approved (R-LIT-01), or a restructure or settlement plan breaks (R-LIT-02). The template status is read synchronously on the rwb-comms answer and the prescription date and days remaining on the rwb-case answer; no topic, consumer or Schedule is held in this service. The task raise and the timers stay with rwb-case; the owner of the 1-working-day and 2-working-day service levels is Not specified in the source documents (GAP-2768).

#### 12.6 Schedules

None. The verification and the authorisation happen when the officer acts, and the prescription timer and the 1-working-day service level of R-LIT-04 are durable timers of the case and of the approval child workflow, not Temporal Schedules of this service and not Quartz jobs. No Schedule of Architecture v5 slide 44 is owned, moved or registered here (GAP-2768; ASM-4602).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The legal action of the pack, its action type, its facts and its status DF-LEG-014 |
| decision_record | PLT library, created in `rwb_litigation` | The hash-linked record of each rule answer, written before the change (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the create and of the patch, with the stored answer |

Not owned and never written: `recovery_case`, `task` and `timer` (P3), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7). Not owned and untouched by this step: `hearing` and the judgment columns of `legal_action`, which this story reads only. No `v_ace_*` view and no ACE table is read (BR8).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document pack fake | The pack of `RC-2026-000704` with every defect list item present; a pack with one missing item; a delayed answer | AC1, X4, X9 |
| rwb-comms notice fake | Notice `NT-2026-000704` with template status `current` and `withdrawn`, each with its template version | AC2, X5 |
| rwb-case case fake | Case `RC-2026-000704` at `PACK_ASSEMBLY`, `NOTICE_GENERATED` and `NOTICE_UNSERVED`, with 90 and 91 prescription days remaining; the task raise accepted and refused; each route fact accepted and refused; a delayed answer | AC1, AC2, AC3, X3, X10 |
| rwb-decision approval fake | The D7 item for `LA-2026-000704` granted, refused with a reason, and delayed beyond 2 s | AC3, X11 |
| decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain with its outbox row, and a stopped chain for the fail-closed test | AC1, AC4 |
| gateway-bff composite route fake (`RWB-PLT-N001-CON`) | The merged SCR-18 and SCR-19 answer for `RC-2026-000704` | AC1 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and `RWB-S4-E5007-CON` or against the document, comms, case and decision documents is a build failure. Every fake answer of the four consumed owners is derived from the published document and carries the placeholder until its owner confirms it (GAP-2765; ASM-4599).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 5 consumed | API-S4-002, API-S4-003 and API-S4-004 provided; the pack, the notice, the case with its task and route fact, the approval item and the reference data consumed; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story; `DecisionRecorded` is the library's element (12.3) |
| Temporal | 1 workflow, 5 activities, 1 child workflow, no Schedule | `LitigationWorkflow`, its five activities and the approval child on `rwb-decision` |
| File | None | No file is read, built or delivered here; the pack is rwb-document's and this story touches none of it |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `pack`, Java package `th.co.scb.ace.workbench.recovery.litigation.pack`; front end `src/modules/recovery/litigation/PackApproval.tsx`, the fragment SCR-19 embeds and SCR-18 reads, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1`; the three operations keep API-S4-002, API-S4-003 and API-S4-004 | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 carries legacy AC1's "writes the result to the decision log with the rule version" and legacy AC4's fail-closed behaviour, and it is the only pattern of the three that adds a write. DP-13 renames the base and keeps the operation IDs, which is why the legacy endpoint block of RWB-E5-007 names two of the three operations and this story serves all three. DP-19 covers the two screens only; the screen model, the merge order and the route path stay with the edge contract.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the metadata also carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, and nothing else. Five consumed surfaces have no row at all: the pack of rwb-document, the notice and template status of rwb-comms, the case with its task and route fact of rwb-case, the D7 approval of rwb-decision, and the reference data of rwb-case. They are recorded once with GAP-2765 with ASM-4599, and the story builds against their fakes on Day 1; no C dependency blocks the build (Template and Rules section R5.7 rule 2).

**Out of this baseline.** The notice approval operation `POST /api/recovery/v1/notices/{noticeId}/approve` (API-S4-001, Litigation A, E2) is not served by this story and stays with the E2 notice story; the pack step approves no notice, and R-LIT-04 only blocks the generation (GAP-2771).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalActionController | Controller | API-S4-002, API-S4-003 and API-S4-004 with the problem mapping for 401, 403, 404, 409, 422 and 503 |
| PackValidator | Service | The case and the caller's scope, the `actionType` value of LOV-LEGAL-TYPE, the required fields and the case state the step needs |
| PackReadClient | Client | The pack and defect-list answer of rwb-document, one hop, 2 s, breaker; never a document table read (BR4) |
| NoticeStateClient | Client | The notice and template-status answer of rwb-comms, one hop, 2 s, breaker |
| TemplateWithdrawnCheck | Service | R-LIT-04 and the task raise; it holds the generation and blocks nothing that is not a generation |
| PrescriptionWarningCheck | Service | The 90-day condition of R-LIT-11 and the MSG-S4-002 warning with the date read from the case |
| RuleEvaluation | Service through the embedded Drools kit | R-LIT-04, R-LIT-11, R-LIT-16 and R-LIT-21 on the answers and the reference rows in force; the version is pinned and recorded |
| PackDecisionWriter | Library adapter | One hash-linked record per rule answer, before any change; refuses the request when the write fails (DP-03) |
| LegalActionWriter | Repository | The `legal_action` facts of the verification and the authorisation, and the idempotency row, in one `rwb_litigation` transaction |
| CaseRouteClient | Client | The case read, the task raise and the route fact to rwb-case, one hop, 2 s, breaker |
| ApprovalClient | Client | The D7 approval item of R-LIT-11 to rwb-decision, one hop, 2 s, breaker |
| LitigationWorkflow | Workflow | The stage on `rwb-litigation` and its pack step |
| PackApproval | React component | Shows the legal action, the pack and defect list, the template hold and the approval state on SCR-18 and SCR-19, read only, with the refusal and failure states |

**Database and migrations.** No Flyway file. `legal_action` arrives with the S4 schema and the DDL template of `RWB-S4-E5007-CON`; the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). The index set of `legal_action` is `Not specified in the source documents (GAP-2767; ASM-4601)`; this story needs a lookup by `case_id` for the workspace read and by `id` for the two single-row operations.

**Schema ownership.** This service writes only `rwb_litigation`. `rwb_case` is owned by rwb-case (P3), `rwb_document` by rwb-document (P5), `rwb_comms` by rwb-comms (P6) and `rwb_decision` by rwb-decision (P7); each is read or announced to through its contract and is never written here (BR3, BR4, BR5, BR8).

**Configuration and reference data.**

- The checklist rows and the version of the defect list behind R-LIT-16 and MSG-S4-001, as versioned reference rows of the business, read with their version. Their content is `Not specified in the source documents (GAP-2767; ASM-4601)`.
- The 90-day threshold of R-LIT-11, as a versioned reference row. Its value is `Not specified in the source documents (GAP-2767; ASM-4601)`; the rule row states 90.
- The template-status values `current` and `withdrawn` of R-LIT-04, read as values in force of the communications service.
- LOV-LEGAL-TYPE and LOV-LEGAL-STATUS at their version in force (TSD S4 T3.2), and the decision code of the verification and of the authorisation, read as values of LOV-DECISION at its version in force.
- The 2 s budget and the single hop are the platform rule of ADR-020 and not a value of this story.

**Build steps**

1. Build `PackValidator` and `LegalActionWriter` over the `legal_action` row and the contract fake; test AC1 and X1 to X3.
2. Build `PackReadClient` and the verification path with `RuleEvaluation` and `PackDecisionWriter` against the library fake; test AC1 and AC4.
3. Build `NoticeStateClient` and `TemplateWithdrawnCheck`, with the task raise on the case fake; test AC2 and X5.
4. Build `PrescriptionWarningCheck` and `ApprovalClient` against the approval fake, with the granted, refused and delayed answers; test AC3, X6 and X11.
5. Build `CaseRouteClient` with each route fact, its refusal and its delayed answer; test AC1, AC2, AC3 and X10.
6. Build the rejection path of R-LIT-21 and its `PACK_ASSEMBLY` announcement; test X4.
7. Build `PackApproval` and read the legal action through the composite route fake; test AC1.
8. Add the boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_document`, `rwb_comms` or `rwb_decision`; test BR8.

**Feature flag.** `rwb.litigation.pack-approval-v1`, read as a flag of the platform library; off means the verification and the authorisation answer 404 and the pack screen shows no approval action, while the read of an existing legal action is unaffected.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-S4-E5007-CON` stay green, the boundary test runs in the pipeline, and a SIT week shows one decision record per rule answer, one task per withdrawn template, one route fact per answer, no write of a case, task, timer, document, notice or ledger row from this service, and no `v_ace_*` read in its logs.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | One or more defect list items are missing when the filing is approved (X4, VR-S4-007-1) | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The prescription date of the case falls inside 90 days (X6, R-LIT-11) | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of the request is missing or invalid (X1) | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the Litigation right of the operation (X7) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action changes (X8, AC4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five texts are the legacy wording of RWB-E5-007 section 14 and the FSD S4 A2.7.3.1 message set, copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the field it names and `MSG-S4-001` with the missing item. The 90-day window behind `MSG-S4-002` is a versioned reference row whose content is `Not specified in the source documents (GAP-2767; ASM-4601)`; the date itself is the case's. A downstream that does not answer (X9) and a reference that is not found (X2) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it writes and what it holds, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-18 Notice approval | Generated | The generated notice of the case with its template version, and the pack the verification reads |
| SCR-18 Notice approval | Approved | The filing authorisation recorded on the legal action, read only here |
| SCR-18 Notice approval | Sent | The notice dispatched by the communications service, read only |
| SCR-18 Notice approval | Delivered | The delivery proof of the communications service, read only |
| SCR-18 Notice approval | Unserved | The notice unserved, with MSG-S4-002 and the prescription date, and the R-LIT-11 escalation available |
| SCR-18 Notice approval | Empty | Not specified in the source documents (CG-ALL-9150) |
| SCR-18 Notice approval | Loading | Not specified in the source documents (CG-ALL-9150) |
| SCR-18 Notice approval | Error | Not specified in the source documents (CG-ALL-9150) |
| SCR-18 Notice approval | No access | Not specified in the source documents (CG-ALL-9150) |
| SCR-19 Litigation workspace | Pack | The pack, the defect-list result with its missing items, the template status and the verification with R-LIT-16 |
| SCR-19 Litigation workspace | Instructed | The filing authorised and the `PACK_APPROVED` fact announced; the firm is selected by `RWB-S4-E5008-APP` |
| SCR-19 Litigation workspace | Filed | The filing date and the court references, read only here |
| SCR-19 Litigation workspace | Hearing | The hearings of the legal action, read only, from the hearing story of this service |
| SCR-19 Litigation workspace | Judgment | The judgment date and amount, read only |
| SCR-19 Litigation workspace | Not recorded | MSG-P7-003, and the legal action unchanged with no task and no route fact |
| SCR-19 Litigation workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-19 Litigation workspace | Held | The R-LIT-04 hold of SCR-18: the generation held, the case at `NOTICE_BLOCKED` and the task raised to the litigation officer |
| SCR-19 Litigation workspace | Failed | The answer of a refused approval with its reason, or a 503 when a consumed contract did not answer; the legal action keeps what it wrote |
| SCR-19 Litigation workspace | Empty | Not specified in the source documents (CG-ALL-9151) |
| SCR-19 Litigation workspace | Loading | Not specified in the source documents (CG-ALL-9151) |
| SCR-19 Litigation workspace | Error | Not specified in the source documents (CG-ALL-9151) |
| SCR-19 Litigation workspace | No access | Not specified in the source documents (CG-ALL-9151) |

The five SCR-18 states and the five SCR-19 states are the ones the legacy screen block of RWB-E5-007 gives, copied unchanged: SCR-18 carries generated, approved, sent, delivered and unserved, and SCR-19 carries pack, instructed, filed, hearing and judgment. The four message and hold states below them are the states of the exception paths of section 5. Neither screen moves the case: rwb-case moves it on the announced fact (BR3), and the route merges this service's answer with the pack of rwb-document, the notice of rwb-comms and the case of rwb-case. The route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-007-01 | AC1 | End to end | Legal action `LA-2026-000704` on case `RC-2026-000704`, action type `NOTICE`, claim 1,800,000.00; the pack fake with every defect list item present; the verification and the filing authorisation each with a decision record and the rule ID with its version |
| TC-E5-007-02 | AC2 | End to end | Case `RC-2026-000704` at `NOTICE_GENERATED`; notice `NT-2026-000704` with template status `withdrawn`; the task raised on the case fake; the route fact `NOTICE_BLOCKED` and R-LIT-04 in the decision record |
| TC-E5-007-03 | AC3 | End to end | Case `RC-2026-000704` at `NOTICE_UNSERVED` with 90 prescription days remaining; the approval fake granting the Head of Litigation answer; the route fact `PACK_ASSEMBLY` and R-LIT-11 in the decision record |
| TC-E5-007-04 | AC4 | End to end | The decision-record library stubbed to stop the chain; the legal action unchanged, no task raised, no approval item and MSG-P7-003 on the screen |
| TC-E5-007-05 | Access | Component | A role without the Litigation right sends API-S4-002 and API-S4-004 and reads API-S4-003; refused with MSG-P4-002 and nothing written |
| TC-E5-007-06 | Principle 5 | NFR | A forced decision-record write failure on 10 verifications; no legal action changes, no task and no approval leave the service |
| TC-E5-007-07 | Section 12 operations, events and activities | Contract | API-S4-002, API-S4-003 and API-S4-004 with their events and activities, checked against the published contract of `RWB-S4-E5007-CON` |
| TC-E5-007-08 | AC5, BR7, BR8 and the section 12.7 tables | Component | Statements against each table of section 12.7, against each `v_ace_*` view and each other `rwb_*` schema, and the fields of the decision record, the log and the calls checked for name, address, identity number and account number; the grant refuses each statement and the build fails |
| TC-E5-007-09 | AC6 | Component | rwb-case contract mock does not answer for `RC-2026-000704`; answer 503 with the platform error envelope; the legal action keeps what it wrote and the hand-off re-runs with the same `Idempotency-Key` |
| TC-E5-007-10 | AC7 | Component | legal action `LA-2026-000704` is not in the status the step needs; answer 409; nothing changes and no route fact is announced |
| TC-E5-007-11 | AC8 | Component | API-S4-002, API-S4-003 and API-S4-004 called without a credential and by a role without the Litigation right; API-S4-003 called for a legal action that does not exist; answers 401, 403 with MSG-P4-002 and 404; nothing written |
| TC-E5-007-12 | AC9 | Component | Legal action `LA-2026-000704` written by one call with an `Idempotency-Key`; the same call repeated with the same key; one effect and the repeat counted |
| TC-E5-007-13 | AC10 | Component | Pack verification activity timed out before its answer and then retried; one legal action row, one decision record, no second task or approval item |
| TC-E5-007-14 | AC11, BR1, BR2, BR4, BR5, BR6, BR7 | Component | Guardrail: verification and filing authorisation written on the `legal_action` row only, after the decision record; LOV values read with their version; no personal data in the row, decision record, log or call |

The six identifiers are the legacy identifiers of RWB-E5-007 in their legacy order, with their legacy covers and their legacy data. The legacy block gives no level, so the level of each case follows the artefact it exercises: the behaviour cases are `End to end` because they cross the document hub, the communications service, the case and the decision centre; the access case `-05` keeps the legacy `Access` cover at `Component`, and the forced-failure case `-06` keeps the legacy `Principle 5` cover at `NFR`. The contract half of every surface they touch is tested in `RWB-S4-E5007-CON` and the cross-service journey is not claimed here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the checklist rows, the template-status values, the 90-day threshold, the list values and the decision codes are data with a version; no role, list value, state name or amount appears in Java.
- No personal data in logs, tests, workflow inputs or prompts: the row carries identifiers, list values, dates and one amount, and the customer's identity never enters this service or its history.
- ACE data only through the owner's contract or the owner's `v_ace_*` views: no component of this story reads an ACE view or an ACE table, and the service identity holds no `v_ace_*` grant (BR8).
- No read of another service's tables and no cross-schema join: the pack, the notice, the case, the task, the timer and the ledger are reached only on their contracts and their fakes (DP-01, BR3, BR4, BR5).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; a hand-off is re-run by repeating the same `Idempotency-Key` and never by a silent resend.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the request with nothing changed (DP-03, R-UNI-39, MSG-P7-003).
- No event, no topic, no outbox row, no Schedule and no timer of this service: the prescription clock and the R-LIT-04 service level are the case's and the approval's (12.3, 12.4, 12.6).
- The two screens are read only; SCR-19 posts the verification and the authorisation through the operations of section 12.1 and SCR-18 is a read of the notice and the pack.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Screens | Test cases |
|---|---|---|---|---|---|---|---|
| REQ-S4-003 | The litigation officer verifies the pack against the defect list before filing is approved (FSD S4 requirements served) | Epics 3 to 8 specification, E5 S4 row; FSD S4 v3 A2.7 | FEAT-LIT-07 | 08 Litigate and enforce | R-LIT-04, R-LIT-11, R-LIT-16, R-LIT-21, R-UNI-39, R-UNI-40, BR1 to BR8 | SCR-18, SCR-19 | TC-E5-007-01 to TC-E5-007-06 |
| No requirement ID in the legacy master (GAP-2769; ASM-4603) | The legacy story of RWB-E5-007 carries no REQ identifier, so the story traces to REQ-S4-003 and to FEAT-LIT-07 until the PRD adds the identifiers | Epics 3 to 8 specification, E5 S4 row | FEAT-LIT-07 | 08 Litigate and enforce | R-LIT-04, R-LIT-11, R-LIT-16 | SCR-18, SCR-19 | TC-E5-007-01 to TC-E5-007-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-007, disposition Split (rework) |
| Legacy criteria | AC1, AC2, AC3 and AC4, owned by this story and copied word for word in section 7 |
| Legacy test cases | TC-E5-007-01 to TC-E5-007-06, kept in legacy order |
| Requirement | REQ-S4-003 of FSD S4; the legacy master carries none (GAP-2769) |
| Contract half | RWB-S4-E5007-CON: the three operations, the pack and authorisation elements, the error envelope, the `Idempotency-Key` rule, the `legal_action` columns and the fakes |
| Sibling slice | RWB-S4-E5008-APP: the firm selection of R-LIT-23 and the instruction |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The case of record, its route states, the task of R-LIT-04 and the prescription timer: rwb-case (P3), and the case-side stories of this legacy family (GAP-2766).
- The pack, its documents, the checklist and the defect list, and MSG-S4-001 as an authored message: rwb-document (P5) and the pack stories of this service; this story consumes the result.
- The notice, its template and its dispatch, and the approval of a notice through API-S4-001: rwb-comms (P6) and the E2 notice story of this service (GAP-2766).
- The approval item at D7, the delegation of authority table and its clock: rwb-decision (P7) and `RWB-P7-E2013-CON`.
- The firm selection of R-LIT-23, the panel, the instruction and the firm's result: `RWB-S4-E5008-APP` and rwb-partner (S9).
- The filing itself, the court receipt, the hearings, the judgment and the enforcement steps of the same legal action: the sibling S4 stories.
- The contract document itself: `RWB-S4-E5007-CON`.
- The roles, rights, scope and masking data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-18 and SCR-19: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, its flag, its dashboards, its alerts and its runbook: its own OPS story.
- The cross-service journey of the pack across rwb-litigation, rwb-document, rwb-comms, rwb-case and rwb-decision with live owners: the wave 3 integration harness.
