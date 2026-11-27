# RWB-S4-E5021-APP File a bankruptcy petition

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-V |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5021-APP-16) |
| Depends on (build) | RWB-S4-E5021-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract version (build) | Not specified in the source documents (DOR-RWB-S4-E5021-APP-23) |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E5-021 for rwb-litigation (S4). The bankruptcy petition is a legal action of action type `BANKRUPTCY_PETITION` of LOV-LEGAL-TYPE, opened, checked, taken to the approver at D7.5 and filed through the firm on base `/api/recovery/litigation/v1` (DP-13); the decision is written through the local decision-record library before the legal action changes (DP-03); the two screens are read through the gateway-bff composite route (DP-19). The case route state, the approval and the firm instruction stay with rwb-case, rwb-decision and rwb-partner, and are consumed and faked. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 19 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **enforcement owner (RW-ENFORCE)**, I want **the bankruptcy petition recorded as a legal action of action type `BANKRUPTCY_PETITION` on the case, warned before the claim expires, taken to the approver at D7.5 and, once approved, filed through the firm with the filing date, the court name and the court references written on the legal action — with one decision record written before any of it moves —**, so that **a petition reaches court in six days instead of twenty-one, and the case of record, the delegation of authority and the law-firm panel stay with the services that own them**.

This story owns the legal action of the petition and the evaluation of R-LIT-58, and nothing else:

- the three legal-action operations of TSD S4 T-A on base `/api/recovery/litigation/v1`: API-S4-002 create, API-S4-003 read and API-S4-004 patch, keeping their legacy operation IDs (DP-13);
- the `legal_action` row of schema `rwb_litigation` with its columns DF-LEG-001 to DF-LEG-014 and the petition as one value of `action_type`, `BANKRUPTCY_PETITION` of LOV-LEGAL-TYPE (TSD S4 T3.1 and T3.2);
- the warning on the claim expiry and the filing fact (`filed_date`, `court_name`, `black_case_no`, `lawsuit_no`, `claim_amount`) written on the row when the firm confirms the filing;
- the evaluation of R-LIT-58 from `ENFORCEMENT_DECISION` on `PETITION_PROPOSED`, and the one decision record it writes through the local decision-record library, with the rule ID and the version in force, before the legal action changes (DP-03, legacy AC1 and AC3);
- the call that takes the petition to the approver at D7.5 on the approval contract of rwb-decision, and the call that answers the case move to rwb-case; both are consumed and faked.

It does not own the case, the approval, the pack, the notice or the panel. `recovery_case` and its route state are rwb-case's (P3), and the route state `BANKRUPTCY_PETITION` that R-LIT-58 moves a case to is a **case** route state of rwb-case, not the status of this service's legal action. The approval item, its delegation level and its clock are rwb-decision's (P7). The pack documents, their checklist and their custody are rwb-document's (P5). The demand notice that precedes the petition is rwb-comms's (P6). The panel, the firm instruction and the firm's result are rwb-partner's (S9) and, inside this service, `RWB-S4-E5009-APP`'s. No component of this story writes a `recovery_case`, `document`, `decision_log_entry`, `rule_row`, `partner` or `notice` row, and none reads a `v_ace_*` view.

### 2. Business rationale

A bankruptcy petition is the last enforcement step before write-off, and it is the step the legacy process loses control of: litigation takes 21 days to file, packs are incomplete and law-firm progress is not tracked (FSD S4 v3 A2.21.1). The legacy story wrote the action, the approval and the case move in one process against one `recovery` schema, and the decision log entry alongside them. In the target the same step is cut in four: the legal action, its court fields and the filing fact are litigation's; the case, its route state and the case clock are the case of record's; the approval and the delegation table are the decision centre's; and the firm, its instruction and its result are the partner service's.

This story is the litigation slice. It opens the legal action with `action_type = BANKRUPTCY_PETITION`, evaluates R-LIT-58 — from `ENFORCEMENT_DECISION`, on `PETITION_PROPOSED`, "enforcement exhausted and the bankruptcy test is met", action "route the petition to the approver at D7.5", to `BANKRUPTCY_PETITION`, owner "Approver at D7.5", 5 working days (Business Rules and Routing Logic v4; TSD S4 T4) — and writes the decision record of that answer before the row changes. A failed write changes nothing and the officer sees MSG-P7-003: that is legacy AC3, and it is the DP-03 pattern applied in the place the legacy `DecisionLogWriter` sat (TSD S4 T2, "writes the decision log entry before any change").

Three facts are no longer this service's to reach, and the story is built so that it cannot reach them. The case row, the route state `BANKRUPTCY_PETITION` and the case clock are rwb-case's: this service evaluates the rule, announces the route fact to rwb-case on the case contract and accepts the answer; it writes no case row (BR3). The approval is rwb-decision's: the petition is taken to the approver on the approval contract, the DoA level and the 5-working-day clock are answered there, and the approval child workflow runs on the decision service's queue (BR2). The firm instruction is rwb-partner's and `RWB-S4-E5009-APP`'s: this story asks for the instruction and records the filing the firm reports back; the instruction, its pack and its lifecycle are not built here (BR1, section 19).

The legacy in-process writes are retired rather than restated. No component of this story writes `recovery_case`, `document`, `decision_log_entry`, `rule_row`, `partner` or `notice`, and the old monolith API base is not served by any path of this service (DP-13). The reference list values of `action_type` and `status` are read with their version in force, never written in code (TSD S4 T3.2, BR6). The two screens are read through the gateway-bff composite route (DP-19, BR7), and no screen calls an owner service directly.

It serves FEAT-LIT-21 "File a bankruptcy petition", it carries the FSD S4 measure "litigation turnaround, 6 days" by putting the approval, the instruction and the filing on one tracked legal action, and it holds the legacy prerequisite FEAT-APD-01 by consuming the approval contract rather than re-implementing the delegation table. The three legacy criteria AC1, AC2 and AC3 belong to this story and are copied word for word in section 7. The requirement identifiers of the key are absent from the legacy master and from the Epics 3 to 8 specification, so the story traces to the feature until the PRD adds them (GAP-1886; ASM-3101).

### 3. Preconditions

- `RWB-S4-E5021-CON` is published: the three operations on `/api/recovery/litigation/v1`, the `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` schemas with the petition sub-shape, the error envelope, the `Idempotency-Key` rule and the fake. This story builds against it on Day 1 (it is the first build dependency of the story).
- The `legal_action` table exists in schema `rwb_litigation` with the columns DF-LEG-001 to DF-LEG-014 of TSD S4 T3.1 and the standard columns of T3.0; no new table and no new column is created by this story.
- The local decision-record library and the shared record format of DP-03 are live (`RWB-PLT-E1027-CON`), and the record it writes is hash-linked on the shared topic `rwb.decision-record.v1`. It is in this story's build list, and the story builds against its fake until the platform contract story publishes.
- The approval contract of rwb-decision, `RWB-P7-E2013-CON` "Approval routing with the delegation of authority table", is published and faked. It is **not** in this story's dependency rows: the metadata of the plan carries no contract dependency, and the absence of the row is recorded as GAP-1885 with ASM-4687. The operation that raises an approval item is not published by that contract at all, which is recorded as GAP-1889 with ASM-4688.
- The case contract of rwb-case that reads the case route state and answers the route fact, and the partner contract of rwb-partner that asks for a firm instruction, are published and faked. Neither is in this story's dependency rows, and neither operation is named by a source: both carry the placeholder `Not specified in the source documents (GAP-1885; ASM-4687)`.
- The gateway-bff composite route `RWB-PLT-N001-CON` serves SCR-19 Litigation workspace and SCR-20 Enforcement workspace; it is in the build list (DP-19), so the two read surfaces are available from Day 1.
- LOV-LEGAL-TYPE (`NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION`) and LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) of TSD S4 T3.2 are read as values in force with their version, on the reference data of rwb-case. DP-07 is not in this story's pattern set and the read carries no dependency row either (GAP-1885; ASM-4687).
- The caller holds a Workbench role with a Litigation right on the operation it calls (TSD S4 T6.1). DP-08 is not in this story's pattern set: the declared right is enforced at the edge for the screen path, and the right on the write paths is this story's design.
- The service runs as its own login on schema `rwb_litigation` (DP-01, DP-02); it holds no grant on another `rwb_*` schema and no `v_ace_*` grant.
- The FSD S4 v3 and the TSD S4 v2 this story reads are In review with an empty sign-off table, and neither this story nor its contract half is signed off. The run of D-RCV-60 has no human approval step, so both stories carry Status Draft (realignment v1) and the missing approval is recorded rather than waited for (GAP-2834; ASM-4658).

### 4. Flow

1. The enforcement owner opens SCR-19 Litigation workspace for a case after judgment, through the gateway-bff composite route (DP-19), and the workspace answers the legal actions of the case on `GET /legal-actions/{legalActionId}` of base `/api/recovery/litigation/v1` (API-S4-003): `action_type`, `status`, `court_name`, `claim_amount`, `law_firm_id`, `filed_date` and the court references.
2. The officer opens the petition on `POST /cases/{caseId}/legal-actions` (API-S4-002) with `LegalActionRequest`: `actionType = BANKRUPTCY_PETITION`, `claimAmount`, `courtName`, and `lawFirmId` where the panel already selected the firm.
3. `LegalActionValidator` checks the case reference, the value of `actionType` against LOV-LEGAL-TYPE, the required fields of the petition and the caller's scope. A failed check answers 422 or 404 and nothing is written.
4. `PetitionWarningCheck` raises the MSG-S4-002 warning with the date when the claim expiry carried by the case read falls inside the filing window. It is a warning and it blocks nothing: the filing window itself is a reference row, never code.
5. `PetitionDecisionWriter` evaluates R-LIT-58 with the rule package in force — the case route state from the case read must be `ENFORCEMENT_DECISION`, the event is `PETITION_PROPOSED`, and the bankruptcy test and the enforcement-exhausted test are versioned reference rows, never code — and writes one decision record through the local decision-record library **before** the legal action changes: the rule ID `R-LIT-58`, the version in force, the inputs reference, the answer `BANKRUPTCY_PETITION` and the decision code read from LOV-DECISION.
6. `LegalActionWriter` writes, in one `rwb_litigation` transaction, the `legal_action` row with status `OPEN`, `action_type = BANKRUPTCY_PETITION`, `claim_amount`, `court_name`, `law_firm_id` where it was given, plus the idempotency row of the request. No other owner's row is written.
7. `PetitionApprovalClient` takes the petition to the approver at D7.5 on the approval contract of `RWB-P7-E2013-CON`: the case reference, the legal action reference, the decision code, the capability area, the product group, the amount used for the limit, `sourceType` and `sourceRef`, the rule ID and its version, and the `Idempotency-Key`. One hop, a 2 s timeout and a breaker per downstream. The operation that raises the item is Not specified in the source documents (GAP-1889; ASM-4688).
8. rwb-decision answers the D7.5 decision: granted, refused, or delayed past the service level. The approval child workflow on queue `rwb-decision` holds the 5 working days of R-LIT-58; this service holds no timer for it and reads the answer (GAP-1888; ASM-3103).
9. `CaseRouteClient` announces the route fact to rwb-case — `BANKRUPTCY_PETITION`, rule `R-LIT-58`, version in force, legal action and case references — and accepts the answer. rwb-case writes the case and its route state; this service writes no case row and evaluates no case rule (BR3). The operation name is Not specified in the source documents (GAP-1885; ASM-4687).
10. On a granted answer, `FirmInstructionClient` asks rwb-partner for the firm instruction of the petition on the partner contract; the instruction, its pack, its lifecycle and its result are `RWB-S4-E5009-APP`'s and the partner stories'. The answer of the instruction request is consumed and faked (GAP-1885; ASM-4687).
11. When the firm confirms the filing, the officer records it on `PATCH /legal-actions/{legalActionId}` (API-S4-004) with `LegalActionUpdate`: `filedDate`, `courtName`, `blackCaseNo`, `lawsuitNo` and `claimAmount`. The row keeps status `OPEN` until the filing date is written and moves to `FILED` in the same transaction; no further decision record is written for a pure fact update, and the update is idempotent on its `Idempotency-Key`.
12. A repeated create with the same case, action type and claim amount, or with the same `Idempotency-Key`, writes nothing and sends no second approval request; the repeat is counted under R-UNI-40.
13. SCR-19 and SCR-20 read the legal action and its states from this service through the composite route, read only, next to the case route state of rwb-case and the approval of rwb-decision.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The request carries no `actionType`, no `claimAmount`, or a value of `actionType` that is not in LOV-LEGAL-TYPE | The answer is 422 and nothing is read beyond the validator; no decision record and no row | MSG-GEN-001 | AC1 |
| X2 | The case ID names no case in the caller's scope, or the legal action ID names no row | The answer is 404 and nothing is written; an out-of-scope case cannot be told from a missing one | None | AC1 |
| X3 | The legal action is not in status `OPEN`, or `actionType` is not a value of LOV-LEGAL-TYPE | The answer is 409 and nothing changes | None | AC1 |
| X4 | The claim expiry carries the case inside the filing window | The MSG-S4-002 warning is shown with the date, and the filing is not blocked; the prescription date is a fact of the case of record | MSG-S4-002 | AC1 |
| X5 | The case route state is not `ENFORCEMENT_DECISION` when the petition is proposed | R-LIT-58 does not fire; the answer is 409, nothing is written and no approval is requested | None | AC2 |
| X6 | A role without the Litigation right records, reads or patches the petition | Refused before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1 |
| X7 | The local decision-record write fails | The transaction writes nothing: the legal action keeps its previous status and its empty filing facts, no approval is requested and no case fact leaves the service | MSG-P7-003 | AC3 |
| X8 | The approval is refused at D7.5 | The legal action keeps status `OPEN`, no filing fact is written and no firm instruction is asked; the refusal and its reason are on the decision record, and the case move on R-LIT-60 is rwb-case's, not this story's | None | AC2 |
| X9 | The approval, the case or the partner contract does not answer inside 2 s, or its breaker is open | The legal action keeps what it wrote, because that fact is true and this service's own; the answer is 503 with the platform error envelope and the hand-off is re-run by repeating the same `Idempotency-Key` | None | AC1 |
| X10 | The case answer refuses the route fact | The legal action keeps what it wrote, the refusal is recorded for the case owner and the caller reads the answer of the case contract unchanged; this service does not move the case itself | None | AC2 |
| X11 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S4-E5021-CON`, the decision-record library and the composite route; the approval, case and partner contracts are consumed and faked, and the three missing dependency rows are recorded (GAP-1885) |
| Negotiable | The bankruptcy test, the filing window, the D7.5 approver role and the list values are versioned reference data; the story fixes the behaviour and the shapes, not the values |
| Valuable | The petition reaches the approver and the firm on one tracked legal action with a decision record before it moves, which is the 21-day to 6-day turnaround of the module |
| Estimable | Three operations, one validator, one warning check, one rule evaluation, one library write, one repository write, three clients and one read-only screen fragment |
| Small | Fits two weeks with its tests, as the primary slice of the legacy key |
| Testable | Each of the three criteria of section 7 is one end-to-end test with the cross-service answers stubbed in the contract fakes; the contract half is tested in `RWB-S4-E5021-CON` |

### 7. Acceptance criteria

```gherkin
Feature: File a bankruptcy petition, in rwb-litigation

  Background:
    Given the petition legal action "LA-2026-000701" exists on case "RC-2026-000701" with action type "BANKRUPTCY_PETITION"
    Given the rule package of R-LIT-58 is in force at its version, and LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are read with their version in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 File a bankruptcy petition (legacy RWB-E5-021 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-decision contract mock returns the approval request for "LA-2026-000701" at D7.5
    Given the rwb-partner contract mock returns the instruction accepted for "LA-2026-000701"
    When the user acts on the screen
    Then takes the petition to the approver and files it through the firm
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-LIT-58 (legacy RWB-E5-021 AC2)
    Given a case in state ENFORCEMENT_DECISION
    Given the rwb-case contract mock returns the case state "ENFORCEMENT_DECISION" for "RC-2026-000701"
    Given the rwb-decision contract mock returns the approval request for "LA-2026-000701" at D7.5
    When petition proposed
    Then route the petition to the approver at D7.5
    Then the case moves to BANKRUPTCY_PETITION

  Scenario: AC3 Not recorded (legacy RWB-E5-021 AC3)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 A component, a statement or a test that reaches another rwb_* schema, a v_ace_* view or an ACE table is refused and fails the build (new, D-RCV-60)
    Given a component, a statement or a test reads or writes another rwb_* schema, a v_ace_* view or an ACE table
    When the boundary test runs in the pipeline
    Then the grant refuses the statement, the boundary test fails the build and nothing is released

  Scenario: AC5 The business rules BR1, BR2, BR4, BR5, BR6 and BR7 hold (new, D-RCV-60)
    Given the petition legal action of the Background is taken to the approver and filed
    When the action runs and the same request is sent again with the same Idempotency-Key
    Then the petition is one legal_action row, the decision is written before the row changes, no v_ace_* view or other rwb_* schema is read, the repeat writes once, the values are those of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS, and no personal data is stored

  Scenario: AC6 The provided operations answer 401, 403 and 404 where the contract names them (new, D-RCV-60)
    Given a request to a provided operation of this service without valid credentials, from a role without the Litigation right, or for a case or legal action outside the caller's scope
    When the request is sent
    Then the answer is 401, 403 or 404 as the contract of RWB-S4-E5021-CON names it, and nothing is written

  Scenario: AC7 A replayed write with the same Idempotency-Key writes once (new, D-RCV-60)
    Given a write with an Idempotency-Key that has already been answered
    When the same write is replayed with that Idempotency-Key
    Then nothing is written again, no second approval request is sent and the repeat is counted

  Scenario: AC8 A retried or timed-out activity writes once and is re-run by the same key (new, D-RCV-60)
    Given an activity of section 12.5 is retried or times out
    When the hand-off is re-run by repeating the same Idempotency-Key
    Then the legal action is written once and the hand-off completes without a second effect

  Scenario: AC9 A consumed call that fails or does not answer leaves the legal action as it wrote it (new, D-RCV-60)
    Given the approval, case or partner contract does not answer, or its breaker is open
    When the action is taken
    Then the answer is 503 and the legal action keeps what it wrote

  Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
    Given the legal action is not in status OPEN
    When a status change is requested
    Then the answer is 409 and nothing changes
```

These three criteria are the legacy criteria of RWB-E5-021, copied word for word except the decision-log wording of AC1 and AC3, which reads decision record (CG-ALL-9546): not one other legacy line is reworded, shortened or renumbered, and every value of the source (`ENFORCEMENT_DECISION`, `BANKRUPTCY_PETITION`, D7.5, MSG-P7-003) is kept character for character. The only additions are the origin tag on each `Scenario:` line and, inside AC1 and AC2, one `Given` line per cross-service answer that a source does not give in process: the approval request of rwb-decision, the case route state of rwb-case and the firm instruction of rwb-partner are answered by their contract fakes, all other lines and all values unchanged. The case route state `BANKRUPTCY_PETITION` of AC2 is a route state of the case of record, moved by rwb-case on the announcement of this service (BR3); the status of the legal action itself is `OPEN` until the filing date is written (section 9). The contract half of these surfaces is tested in `RWB-S4-E5021-CON`, and the end-to-end journey across the three services is not claimed here. AC4 is new under D-RCV-60, is not a legacy criterion and proves exception X11 (section 5).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR8 (R-LIT-58) | Litigation · D7 · from `ENFORCEMENT_DECISION` · event `PETITION_PROPOSED` · condition "enforcement exhausted and the bankruptcy test is met" · action "route the petition to the approver at D7.5" · to `BANKRUPTCY_PETITION` · owner "Approver at D7.5" · channel "Workbench, Committee View" · service level 5 working days | Business Rules and Routing Logic v4 (R-LIT-58); TSD S4 T4 |
| BR1 | The petition is a `legal_action` row of this service: `action_type` takes the value `BANKRUPTCY_PETITION` of LOV-LEGAL-TYPE, and the court fields and the filing facts are written on that row and nowhere else | TSD S4 T3.1, T3.2; Architecture v5 slide 41 (S4 owns legal actions); legacy Data block |
| BR2 | The decision is written before the legal action changes: one record through the local decision-record library, with the rule ID and the version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); Architecture v5 slide 28 (R-UNI-39); legacy AC1 and AC3 |
| BR3 | The case move is answered, not written: `BANKRUPTCY_PETITION` is a route state of rwb-case and this service announces the route fact with the rule and its version and accepts the answer; no `recovery_case` row is written and no case rule is evaluated here | R-LIT-58; `ownership.json` (`recovery_case` owner P3); Architecture v5 slide 41 |
| BR4 | No ACE read: this story reads no `v_ace_*` view, no ACE table and no other `rwb_*` schema, and its login holds no such grant | DP-01, DP-05 as a prohibition; Architecture v5 slide 29 (grants per schema, `rwb.litigation` refused on `rwb_payment`) |
| BR5 | The same request twice, or the same `Idempotency-Key` twice, writes once, sends no second approval request and counts the repeat | R-UNI-40; TSD S4 T-A.1 (API-S4-002 `Idempotency-Key` header) |
| BR6 | Closed vocabulary: `action_type` and `status` take only the values of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS in force, read with their version; the bankruptcy test and the filing window are versioned reference rows and are never written in code | TSD S4 T3.2; FSD S4 A2.21.3.1 (BR-S4-021); Template and Rules section R7.2 (s17) |
| BR7 | No personal data: the row, the decision record, the log and every call carry identifiers, list values, dates and amounts only; no name, address, identity number or account number enters this service | TSD S4 T3.1; Architecture v5 slides 42 and 43 notes |
| BR9 (R-LIT-56) | From `DEFERRAL_RECORDED`, on `REVIEW_DATE_REACHED`, the case returns to the enforcement decision; the petition is proposed from that state, never from a deferral | Business Rules and Routing Logic v4 (R-LIT-56) |
| BR10 (R-LIT-57) | From `DEFERRAL_RECORDED`, on `ENFORCEMENT_EXHAUSTED` with a second deferral and no asset traced, the case routes to write-off at D9; R-LIT-58 is the other exit of enforcement exhaustion and is the one this story evaluates | Business Rules and Routing Logic v4 (R-LIT-57) |
| BR11 (R-UNI-39) | An action whose decision cannot be recorded does not proceed and nothing moves | Business Rules and Routing Logic v4 (R-UNI-39); legacy AC3 |
| BR12 (R-UNI-40) | The same event or the same request twice produces one effect, and the repeat is counted | Business Rules and Routing Logic v4 (R-UNI-40) |

The bankruptcy test that R-LIT-58's condition names has no definition in any source read for this key, so it is evaluated as a versioned reference rule row set and never as code: the placeholder `Not specified in the source documents (GAP-1890; ASM-3105)` stands in the configuration of section 13 and in the rule's own row.

### 9. State transitions

This story moves the status of its own legal action, and announces a route fact of the case. The two are different objects and are never used one for the other.

**`legal_action.status`** — the values of LOV-LEGAL-STATUS (TSD S4 T3.2), moved by this service:

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The petition is opened on API-S4-002 | `actionType = BANKRUPTCY_PETITION`, the request validates and the decision record is written | `OPEN` |
| `OPEN` | The petition is proposed and R-LIT-58 fires | The case route state is `ENFORCEMENT_DECISION` and the bankruptcy test is met | `OPEN`, with the approval requested at D7.5 and the decision record written |
| `OPEN` | The filing is recorded on API-S4-004 | `filedDate` is written and the court references are present | `FILED` |
| `OPEN` | The approval is refused at D7.5 | The refusal and its reason are on the decision record | `OPEN`; no filing fact, no firm instruction, and the case move on R-LIT-60 is rwb-case's |
| `FILED` | The judgment is recorded | `judgmentDate` and `judgmentAmount` are written | `JUDGMENT` |
| `JUDGMENT` | Enforcement opens | The enforcement step is recorded | `ENFORCING` |
| `ENFORCING` or `FILED` | The case is closed or the action withdrawn | The closing step of the case of record | `CLOSED` or `WITHDRAWN` |

The status of a petition refused before filing has no value in LOV-LEGAL-STATUS that names a refusal, so the row keeps `OPEN` and the refusal lives on the decision record: the value is `Not specified in the source documents (GAP-1890; ASM-3105)`.

**The case route state `BANKRUPTCY_PETITION`** is rwb-case's, and this story only announces it (BR3):

| From (rwb-case) | Rule | To (rwb-case) | Owner of the move |
|---|---|---|---|
| `ENFORCEMENT_DECISION` | R-LIT-58, on `PETITION_PROPOSED`, the bankruptcy test met | `BANKRUPTCY_PETITION` | rwb-case, on the announcement of this service |
| `BANKRUPTCY_PETITION` | R-LIT-59, on `PETITION_APPROVED` | `OFFICIAL_RECEIVER_CLAIM` | rwb-case with the partner stories (`RWB-S4-E5009-APP`) |
| `BANKRUPTCY_PETITION` | R-LIT-60, on `PETITION_REJECTED` | `TO_WRITE_OFF` | rwb-case with the write-off stories |

Neither the case row nor its route state is read as a table or written here; the case read and the announcement of 12.2 are the only paths by which the route state moves (GAP-1885; ASM-4687).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA (TSD S4 T6.1): opens, reads and patches the petition, and records the filing |
| RW-ENFORCE, enforcement owner | Litigation CRU: opens, reads and patches the petition in scope; the primary role of FSD S4 A2.21 |
| RW-LEGAL, legal counsel | Litigation RA: reads the petition and its facts; approves nothing here, because the approval is rwb-decision's |
| RW-TEAMMGR, RW-CASEOWN, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read the petition and its facts only |
| RW-PRODHEAD and RW-HEADLIT | Litigation RA: read, and the acknowledgement right the matrix gives the product head and the Head of Litigation |
| PT-LAWFIRM, law firm user | Partner gateway, Litigation RU on the rows of its own instructed cases; it never calls this service directly and never opens or patches a legal action |
| rwb-litigation service identity | Validates, evaluates R-LIT-58, writes the decision record and the row, and calls the approval, case and partner contracts; it holds no grant on another schema and no `v_ace_*` grant |
| rwb-decision (P7) service identity | Owns the approval item, the delegation row and the 5-working-day clock of D7.5; answers granted or refused |
| rwb-case (P3) service identity | Owns the case of record and the route state `BANKRUPTCY_PETITION`; answers the route fact |
| rwb-partner (S9) service identity | Owns the panel, the firm instruction and the firm's result; answers the instruction request |

The rights above are the rows of TSD S4 T6.1 and nothing wider. The approver at D7.5 that R-LIT-58 routes to holds its right in rwb-decision and rwb-access, not here; the role code of that approver is `Not specified in the source documents (GAP-1890; ASM-3105)`. The declared right of each operation is checked by the rwb-access authorise check of DP-08 at the edge for the screen path and as the guard of each write path before any change. A refusal keeps MSG-P4-002 and changes nothing.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Write on create; read as the reference of every call and answer |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Write on create; read and sent on the approval, case and partner calls |
| DF-LEG-003 | legal_action (S4, `rwb_litigation`) | law_firm_id | Write when the panel already selected the firm; read |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Write, `BANKRUPTCY_PETITION` of LOV-LEGAL-TYPE |
| DF-LEG-005 | legal_action (S4, `rwb_litigation`) | lawsuit_no | Write on the filing step |
| DF-LEG-006 | legal_action (S4, `rwb_litigation`) | black_case_no | Write on the filing step |
| DF-LEG-007 | legal_action (S4, `rwb_litigation`) | red_case_no | Read at judgment; not written by this story |
| DF-LEG-008 | legal_action (S4, `rwb_litigation`) | court_name | Write on create and on the filing step |
| DF-LEG-009 | legal_action (S4, `rwb_litigation`) | claim_amount | Write on create; the amount the D7.5 limit is read against |
| DF-LEG-010 | legal_action (S4, `rwb_litigation`) | filed_date | Write on the filing step; its presence moves the status to `FILED` |
| DF-LEG-011 | legal_action (S4, `rwb_litigation`) | judgment_date | Read only |
| DF-LEG-012 | legal_action (S4, `rwb_litigation`) | judgment_amount | Read only |
| DF-LEG-013 | legal_action (S4, `rwb_litigation`) | lit_status | Read only; the court status that arrives from LIT through COLLINS and rwb-source-data |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Write, against LOV-LEGAL-STATUS (`OPEN`, then `FILED`) |
| Standard columns | legal_action (S4, `rwb_litigation`) | state, version, created_at, created_by, updated_at, updated_by, is_active | Written by the service identity (TSD S4 T3.0) |
| DF-DEC-003, DF-DEC-004, DF-DEC-005, DF-DEC-008, DF-DEC-012, DF-DEC-016, DF-DEC-017, DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule ID, rule version, inputs reference, final call, decided at, the two hashes | Write through the local library, before the legal action changes |
| DF-DEC-032 to DF-DEC-053 | approval (P7, `rwb_decision`) | the approval item the petition raises: case, decision code, capability area, level, limit version, product group, amount, preparer, due time, source type and reference, rule and version | Sent on the approval call and stored nowhere here |

Field IDs are those of TSD S4 v2 T3.1, the approval field IDs of the Logical Data Model and Data Dictionary v9, and the standard columns of TSD S4 T3.0. **No new table, no new column and no migration:** `legal_action` arrives with the S4 schema of this service and its contract story `RWB-S4-E5021-CON` publishes the DDL template, which the service's own Flyway applies (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's migration (DP-03).

**Not written, not read as a table, and named here so that a reviewer can check the absence:** `recovery_case` and its route state DF-CAS-* (P3 rwb-case), `document` and the pack DF-DOC-* (P5 rwb-document), `decision_log_entry` and `rule_row` DF-DEC-001 to DF-DEC-018 and DF-REF-001 to DF-REF-015 of the central ledger (P7 rwb-decision), `partner` (S9 rwb-partner), `notice` (P6 rwb-comms), `hearing` DF-LEG-024 to DF-LEG-029 (S4, untouched by a petition) and every `v_ace_*` view (P1 rwb-source-data). `legal_action.case_id`, `law_firm_id` and the approval references are identifiers, not foreign keys across schemas (DP-01, BR4).

**No personal data.** The row this story writes carries identifiers, list values, dates and one amount. The borrower, the guarantor, the address and the identity number never enter `rwb_litigation`: they are held by ACE and reached only through rwb-source-data by the services that need them, and they are not logged here and not put on any call.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | Open the petition: the legal action of action type `BANKRUPTCY_PETITION` and the decision record of R-LIT-58 (TSD S4 T-A.2) | Litigation C, scope applied | `Idempotency-Key` header required; the answer is stored and a repeat returns it |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | Read the legal action with its pack, instruction, hearings and judgment (TSD S4 T-A.2) | Litigation R, scope applied | Not applicable |
| API-S4-004 | PATCH | `/legal-actions/{legalActionId}` | Record the filing, the judgment or an enforcement step on the legal action (TSD S4 T-A.2) | Litigation U, scope applied | `Idempotency-Key` header required |

The three operations and their IDs, rights and error sets are those of TSD S4 T-A.1 and T-A.2; they keep their legacy IDs and differ only in the base, which DP-13 renames. Errors: 401 no session (message ID: Not specified in the source documents (DOR-RWB-S4-E5021-APP-17)); 403 no right (MSG-P4-002); 404 unknown or out-of-scope reference (message ID: Not specified in the source documents (DOR-RWB-S4-E5021-APP-17)); 409 a status or an action type that refuses the step, or a case that is not in `ENFORCEMENT_DECISION` (message ID: Not specified in the source documents (DOR-RWB-S4-E5021-APP-17)); 422 a missing or invalid field (MSG-GEN-001); 503 the decision-record library or a consumed contract unavailable (message ID: Not specified in the source documents (DOR-RWB-S4-E5021-APP-17)). The request and answer shapes are declared by `RWB-S4-E5021-CON`, which this story consumes as its first build dependency.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| The approval request and its answer of `RWB-P7-E2013-CON`, base `/api/recovery/decision/v1` | P7 rwb-decision | Takes the petition to the approver at D7.5 and reads the granted, refused or delayed answer. The operation that raises an item is Not specified in the source documents (GAP-1889; ASM-4688); the 5-working-day clock of R-LIT-58 is the approval workflow's (GAP-1888; ASM-3103) |
| The case read and the route fact of rwb-case, operation Not specified in the source documents (GAP-1885; ASM-4687) | P3 rwb-case | Reads the case route state, the product group and the claim expiry the warning shows, and announces `BANKRUPTCY_PETITION` with rule R-LIT-58 and its version; accepts the answer |
| The firm instruction request of rwb-partner, operation Not specified in the source documents (GAP-1885; ASM-4687) | S9 rwb-partner | Asks for the instruction of the approved petition; the instruction, its pack and its result are `RWB-S4-E5009-APP`'s and the partner stories' |
| The reference-data read of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS, `RWB-P3-E1043-CON` | P3 rwb-case | The two list codes at their version in force (DP-07, declared here although the pattern is not in this story's set) |

Every row is one hop with a 2 s timeout and a breaker per downstream (ADR-020). The approval, case and partner rows carry the missing dependency of GAP-1885 and are built against their fakes; the reference-data row belongs to the same gap. No operation of another service is declared as provided here (BR1).

#### 12.3 Events published

None. The service topic `rwb.litigation.events.v1` carries `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` in the event catalogue (Architecture v5 slides 19 and 43), and this story publishes none of them: DP-09 is not in its pattern set, so it adds no outbox row and no producer, and the catalogue assigns no story to `LawsuitFiled`, so whether a filed bankruptcy petition raises it is not settled by any source read here — the assignment is carried as GAP-1887 with ASM-3102. The decision record is written through the local decision-record library of DP-03, which publishes `DecisionRecorded` (event 08) on the shared `rwb.decision-record.v1`; that element is the library's and this service declares no payload of its own.

#### 12.4 Events consumed

None. The approval answer and the case answer are synchronous answers of their contracts, not topics, and the partner answer is the answer of the instruction request; so this story subscribes to no topic, holds no consumer and uses no inbox of its own. The two events that Architecture v5 slide 19 gives rwb-litigation as input, `NoticeDelivered` and `PartnerResultSubmitted`, belong to the demand-notice and firm-result stories of this service and are not consumed here.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| LitigationWorkflow | Workflow, one run per case stage, the S4 child of CaseWorkflow | `rwb-litigation` | Started by CaseWorkflow on rwb-case; holds the stage, its durable timers on a court date and its signals (Temporal design slide 13) |
| openPetition | Activity | `rwb-litigation` | The validator, the R-LIT-58 evaluation and the row write of steps 2 to 6 |
| recordDecision | Activity through the library | `rwb-litigation` | The local decision record and its outbox row, written before the change (DP-03) |
| submitForApproval | Activity | `rwb-litigation` | The approval call to rwb-decision and the answer it returns |
| announceCaseRoute | Activity | `rwb-litigation` | The route fact `BANKRUPTCY_PETITION` to rwb-case and its answer |
| recordFiling | Activity | `rwb-litigation` | The filing fact of API-S4-004 and the status move to `FILED` |
| petitionApproval | Child workflow, owner rwb-decision | `rwb-decision` | The D7.5 approval and its 5-working-day clock, built against its fake (GAP-1888; ASM-3103) |

The workflow name is fixed by the Temporal and Drools design (`LitigationWorkflow` on `rwb-litigation`, "LIT 79" in the stage list); the petition step is a step of that workflow and not a workflow of its own, and no activity is registered by a contract document. The child workflow's own type on the decision service is named only as "Decision: child: approval" in the service contract of Architecture v5 slide 19, and no source gives its type name, its workflow ID or its queue registration beyond `rwb-decision` (GAP-1888; ASM-3103). The workflow ID form, the start call and the duplicate-start policy of LitigationWorkflow are Not specified in the source documents (CG-ALL-9538). The approval request shape of submitForApproval is the consumed stub of the P7 fake until RWB-P7-E2013-CON publishes the raise (GAP-1889; ASM-3103).

#### 12.6 Schedules

None. The petition is proposed when the enforcement owner acts, and R-LIT-58's 5 working days is the durable timer of the approval child workflow on `rwb-decision`, not a Temporal Schedule of this service and not a Quartz job. No Schedule of Architecture v5 slide 44 is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (rwb_litigation) | The petition row, its court fields, its filing facts and its status DF-LEG-014 |
| decision_record | PLT library, created in `rwb_litigation` | The hash-linked record of the R-LIT-58 answer, written before the change (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the create and of the patch, with the stored answer |

Not owned and never written: `recovery_case` and its route state (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7), `partner` (S9), `notice` (P6). Not owned and untouched by a petition: `hearing` and `legal_action`'s judgment columns, which this story reads only. No `v_ace_*` view and no ACE table is read (BR4).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision approval WireMock (RWB-P7-E2013-CON) | The D7.5 item for `LA-2026-000701` at the level the delegation table gives, granted, refused with a reason, and delayed beyond 2 s | AC1, AC2, X8, X9 |
| rwb-case WireMock | Case `RC-2026-000701` at route state `ENFORCEMENT_DECISION` with its product group and claim expiry, the route fact `BANKRUPTCY_PETITION` accepted, the refusal of a route fact from another state, and a delayed answer | AC2, X5, X10 |
| rwb-partner WireMock | The instruction of `LA-2026-000701` accepted with the firm reference, and a refusal for a firm outside the panel | AC1, X9 |
| decision-record library stub (RWB-PLT-E1027-CON) | A healthy chain with its outbox row, and a stopped chain for the fail-closed test | AC1, AC3 |
| reference-data WireMock | LOV-LEGAL-TYPE and LOV-LEGAL-STATUS at their version in force, and the bankruptcy-test and filing-window rows at theirs | AC1, AC2, X4 |
| gateway-bff composite route fake (RWB-PLT-N001-CON) | The merged SCR-19 and SCR-20 answer for `RC-2026-000701`, with the legal action read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and `RWB-S4-E5021-CON` or against the approval, case and partner documents is a build failure.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | API-S4-002, API-S4-003 and API-S4-004 provided; the approval, the case read and route fact, the firm instruction and the reference data consumed; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story; `DecisionRecorded` is the library's element (12.3) |
| Temporal | 1 workflow, 5 activities, 1 child workflow, no Schedule | LitigationWorkflow, its five activities and the approval child on `rwb-decision` |
| File | None | No file is read, built or delivered here; the pack is rwb-document's and this story touches none of it |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `petition`, Java package `th.co.scb.ace.workbench.recovery.litigation.petition`; front end `src/modules/recovery/litigation/Petition.tsx`, the fragment SCR-19 and SCR-20 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1`; the three operations keep API-S4-002, API-S4-003 and API-S4-004 | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the pattern that carries legacy AC1's "writes the result to the decision log with the rule version" and legacy AC3's fail-closed behaviour. DP-13 renames the base and keeps the operation IDs, which is why the legacy endpoint block of RWB-E5-021 names two of the three operations and this story serves all three. DP-19 covers the two screens only, and the screen model and the merge order stay with the edge contract.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows that the metadata also carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, and nothing else. Three consumed contracts have no row at all: the approval `RWB-P7-E2013-CON` (P7), the case contract that reads the route state and answers it (P3) and the partner instruction contract (S9). DP-07's reference-data read and DP-08's declared right are in the same position; the five are recorded once as GAP-1885 with ASM-4687. The story builds against their fakes on Day 1 and no C dependency blocks the build (Template and Rules section R5.7 rule 2).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalActionController | Controller | API-S4-002, API-S4-003 and API-S4-004 with the problem mapping for 401, 403, 404, 409, 422 and 503 |
| LegalActionValidator | Service | The case and the caller's scope, the `actionType` value of LOV-LEGAL-TYPE, the required petition fields and the status the step needs |
| PetitionWarningCheck | Service | The claim expiry of the case against the filing window, and the MSG-S4-002 warning with the date; it blocks nothing |
| RuleEvaluation | Service through the embedded Drools kit | R-LIT-58 on the case route state and the two tests in force; the version is pinned and recorded |
| PetitionDecisionWriter | Library adapter | One hash-linked record with the rule ID and the version in force, before any change; refuses the request when the write fails (DP-03) |
| LegalActionWriter | Repository | The `legal_action` row, its status and the idempotency row, in one `rwb_litigation` transaction |
| PetitionApprovalClient | Client | The approval call of rwb-decision, one hop, 2 s, breaker, no retry of its own |
| CaseRouteClient | Client | The case read and the route fact `BANKRUPTCY_PETITION` to rwb-case, one hop, 2 s, breaker |
| FirmInstructionClient | Client | The firm instruction request to rwb-partner, one hop, 2 s, breaker; the instruction itself is not built here |
| LitigationWorkflow | Workflow | The stage on `rwb-litigation` and its petition step |
| Petition | React component | Shows the legal action, its status, the filing facts and the approval state on SCR-19 and SCR-20, read only, with the refusal and failure states |

**Database and migrations.** The schemas named in this section (rwb_case, rwb_comms, rwb_decision, rwb_document, rwb_partner) are owned by other services and are never written here; this service owns `rwb_litigation` only (section 12.7). No Flyway file. `legal_action` arrives with the S4 schema and the DDL template of `RWB-S4-E5021-CON`; the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). The index set of `legal_action` is `Not specified in the source documents (GAP-1890; ASM-3105)`; this story needs a lookup by `case_id` for the workspace read and by `id` for the two single-row operations, and creates no index of its own beyond what the contract template declares.

**Configuration and reference data.**

- The bankruptcy test and the enforcement-exhausted test of R-LIT-58, as versioned reference rule rows of the business, read with their version. Their content is `Not specified in the source documents (GAP-1890; ASM-3105)`.
- The filing window behind MSG-S4-002, as a versioned reference row. Its value is `Not specified in the source documents (GAP-1890; ASM-3105)`.
- LOV-LEGAL-TYPE and LOV-LEGAL-STATUS at their version in force (TSD S4 T3.2).
- The decision code of the D7.5 petition decision, read as a value of LOV-DECISION at its version in force.
- The 2 s budget and the single hop are the platform rule of ADR-020 and not a value of this story.

**Build steps**

1. Build `LegalActionValidator` and `LegalActionWriter` over the `legal_action` row and the contract fake; test AC1 and X1 to X3.
2. Build `PetitionWarningCheck` with the filing window and the claim-expiry warning; test X4.
3. Build `RuleEvaluation` and `PetitionDecisionWriter` against the library fake, with the stopped chain; test AC2 and AC3.
4. Build `PetitionApprovalClient` against the approval fake, with the 2 s budget, the breaker, the refusal and the delayed answer; test AC1, X8 and X9.
5. Build `CaseRouteClient` against the case fake, with the route fact, the refusal and the delayed answer; test AC2, X5 and X10.
6. Build `FirmInstructionClient` against the partner fake and the filing step of API-S4-004; test AC1.
7. Build `Petition` and read the legal action through the composite route fake; test AC1.
8. Add the boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision`, `rwb_document`, `rwb_partner` or `rwb_comms`; test BR4.

**Feature flag.** `rwb.litigation.petition-v1`, read as a flag of the platform library; off means the petition create answers 404 and the enforcement workspace shows no petition action, while the read and patch of an existing legal action are unaffected.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-S4-E5021-CON` stay green, the boundary test runs in the pipeline, and a SIT week shows one petition per legal action, one approval per petition, one route fact per approved petition, one filing fact per filing, no write of a case, document, ledger or notice row from this service, and no `v_ace_*` read in its logs.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, and the pack check that raises it is the pack story of this service (REQ-S4-002 and REQ-S4-003), so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim expiry of the case falls inside the filing window (X4) | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of the request is missing (X1) | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the Litigation right of the operation (X6) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action changes (X7, AC3) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five texts are the legacy wording of RWB-E5-021 section 14 and are copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the field it names. `MSG-S4-001` is authored by the pack stories of this service and is carried here because it is the message set of the key; this story raises it on no path. `MSG-S4-002` carries the claim expiry date read from the case of record, and the filing window behind it is `Not specified in the source documents (GAP-1890; ASM-3105)`. A downstream that does not answer (X9) and a reference that is not found (X2) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-19 Litigation workspace | Loading | Not specified in the source documents (CG-ALL-9547) |
| SCR-19 Litigation workspace | Empty | Not specified in the source documents (CG-ALL-9547) |
| SCR-19 Litigation workspace | Error | Not specified in the source documents (CG-ALL-9547) |
| SCR-19 Litigation workspace | No access | Not specified in the source documents (CG-ALL-9547) |
| SCR-19 Litigation workspace | Pack | The petition with its action type, claim amount and court, the pack of the case read from rwb-document, and the claim-expiry warning |
| SCR-19 Litigation workspace | Instructed | The petition approved at D7.5 and the firm instruction asked, with the approval level and its due date |
| SCR-19 Litigation workspace | Filed | The filing date, the court name and the black case number on the legal action, and the status `FILED` |
| SCR-19 Litigation workspace | Hearing | The hearings of the legal action, read only, from the hearing story of this service |
| SCR-19 Litigation workspace | Judgment | The judgment date and amount, read only |
| SCR-19 Litigation workspace | Not recorded | MSG-P7-003, and the legal action unchanged with no approval requested |
| SCR-19 Litigation workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-19 Litigation workspace | Failed | The answer of a refused approval with its reason, or a 503 when a consumed contract did not answer; the legal action keeps what it wrote |
| SCR-20 Enforcement workspace | Requested | The enforcement step whose decision point is the petition: the case route state `ENFORCEMENT_DECISION` and the petition proposed from it |
| SCR-20 Enforcement workspace | Seized | The writ and seizure of the case, read only; not this story's step |
| SCR-20 Enforcement workspace | Auctioned | The LED auction result, read only; not this story's step |
| SCR-20 Enforcement workspace | Closed | The closed enforcement, read only; not this story's step |
| SCR-20 Enforcement workspace | Empty | Not specified in the source documents (CG-ALL-9548) |
| SCR-20 Enforcement workspace | Loading | Not specified in the source documents (CG-ALL-9548) |
| SCR-20 Enforcement workspace | Error | Not specified in the source documents (CG-ALL-9548) |
| SCR-20 Enforcement workspace | No access | Not specified in the source documents (CG-ALL-9548) |

The six SCR-19 states and the four SCR-20 states are the ones the legacy screen block of RWB-E5-021 gives, copied unchanged: SCR-19 carries pack, instructed, filed, hearing and judgment, and SCR-20 carries requested, seized, auctioned and closed. The petition appears on SCR-19 from the moment the pack is opened and on SCR-20 in its requested state, where the petition is proposed from `ENFORCEMENT_DECISION`; neither screen moves the case, and the route state of the case of record stays rwb-case's (BR3). The route merges this service's answer with the case of rwb-case and the approval of rwb-decision; the route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`, not here. The empty, loading, error and no-access states of each screen are Not specified in the source documents (CG-ALL-9547); the refusal of a role without the Litigation right keeps MSG-P4-002 as in the Refused state.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-021-01 | AC1 | End to end | Petition `LA-2026-000701` on case `RC-2026-000701`, action type `BANKRUPTCY_PETITION`, claim 2,400,000.00; the approval fake granted at D7.5; the partner fake accepting the instruction; the filing recorded with its date and court number |
| TC-E5-021-02 | AC2 | End to end | Case `RC-2026-000701` at route state `ENFORCEMENT_DECISION`; `PETITION_PROPOSED`; the bankruptcy test met at its version; the case fake answering the route fact `BANKRUPTCY_PETITION`; the rule ID and version in the decision record |
| TC-E5-021-03 | AC3 | End to end | The decision-record library stubbed to stop the chain; the legal action unchanged, no approval requested and MSG-P7-003 on the screen |
| TC-E5-021-04 | Access | Component | A role without the Litigation right sends API-S4-002 and reads API-S4-003; refused with MSG-P4-002 and nothing written |
| TC-E5-021-05 | Principle 5 | NFR | A forced decision-record write failure on 10 petitions; no legal action changes, no approval leaves the service and the incident is raised under R-UNI-39 |
| TC-E5-021-06 | Section 12 operations, events and activities | Contract | The three operations of API-S4-002, API-S4-003 and API-S4-004, their events and the activities of section 12.5 checked against `RWB-S4-E5021-CON` and the Temporal catalog; any drift fails the build |
| TC-E5-021-07 | Section 12.7 tables | Boundary | Statements against `legal_action`, `decision_record` and `idempotency_key` only; a statement on any other table fails the build |
| TC-E5-021-08 | AC4 | Boundary | A component statement reaching `rwb_case`, a `v_ace_*` view or an ACE table; the grant refuses it and the build fails |
| TC-E5-021-09 | AC5 | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC5) | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC5) |
| TC-E5-021-10 | AC6 | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC6) | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC6) |
| TC-E5-021-11 | AC7 | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC7) | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC7) |
| TC-E5-021-12 | AC8 | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC8) | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC8) |
| TC-E5-021-13 | AC9 | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC9) | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC9) |
| TC-E5-021-14 | AC10 | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC10) | Not specified in the source documents (NEWAC-RWB-S4-E5021-APP-AC10) |

The five identifiers are the legacy identifiers of RWB-E5-021 in their legacy order, with their legacy covers and their legacy data. The legacy level `System` of the first three maps to `End to end` here, because the behaviour they prove crosses the case, the decision centre and the partner; the access case `-04` keeps the legacy `Access` cover at `Component`, and the forced-failure case `-05` keeps the legacy `Principle 5` cover at `NFR`. The contract half of every surface they touch is tested in `RWB-S4-E5021-CON` and the cross-service journey is not claimed here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the bankruptcy test, the enforcement-exhausted test, the filing window, the list values and the decision code are data with a version; no role, list value, state name or amount appears in Java.
- No personal data in logs, tests, workflow inputs or prompts: the row carries identifiers, list values, dates and one amount, and the customer's identity never enters this service or its history.
- ACE data only through the owner's contract or the owner's `v_ace_*` views: no component of this story reads an ACE view or an ACE table, and the service identity holds no `v_ace_*` grant (BR4).
- No read of another service's tables and no cross-schema join: the case, the approval, the pack, the firm and the notice are reached only on their contracts and their fakes (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; a hand-off is re-run by repeating the same `Idempotency-Key` and never by a silent resend.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the request with nothing changed (DP-03, R-UNI-39, MSG-P7-003).
- No event, no topic, no outbox row, no Schedule and no timer of this service: the petition's 5 working days is the approval workflow's clock on `rwb-decision` (12.3, 12.4, 12.6).
- The two screens are read only; SCR-19 posts the petition and the filing through the operations of section 12.1 and SCR-20 is a read.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Screens | Test cases |
|---|---|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-1886; ASM-3101) | The petition is taken to the approver and filed through the firm, and the result is recorded with its rule version | Epics 3 to 8 specification, E5 S4 row; FSD S4 v3 A2.21 | FEAT-LIT-21 | 08 Litigate and enforce | R-LIT-58, R-LIT-56, R-LIT-57, R-UNI-39, R-UNI-40, BR1 to BR7 | SCR-19, SCR-20 | TC-E5-021-01, TC-E5-021-02, TC-E5-021-03 |
| FEAT-LIT-21 | File a bankruptcy petition | Business Rules and Routing Logic v4 (R-LIT-58) | FEAT-LIT-21 | 08 Litigate and enforce | R-LIT-58 | SCR-19, SCR-20 | TC-E5-021-01 to TC-E5-021-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-021, disposition Split (rework) |
| Legacy criteria | AC1, AC2 and AC3, owned by this story and copied word for word in section 7 |
| Legacy test cases | TC-E5-021-01 to TC-E5-021-05, kept in legacy order |
| Requirement | The legacy master of RWB-E5-021 and the Epics 3 to 8 specification carry no REQ identifier for this feature, so the story traces to FEAT-LIT-21 until the Epics 3 to 8 PRD adds the identifiers (GAP-1886) |
| Contract half | RWB-S4-E5021-CON: the three operations, the petition shape, the error envelope, the `Idempotency-Key` rule, the `legal_action` columns and the fakes |
| Sibling slice | RWB-S4-E5009-APP and the partner stories: the firm instruction, its pack and its result |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The case of record, its route state `BANKRUPTCY_PETITION`, the case clock and the case decision record: rwb-case (P3), and the case-side story of this legacy family.
- The approval item, the delegation of authority table, the approver at D7.5 and the 5-working-day clock: rwb-decision (P7), `RWB-P7-E2013-CON` and `RWB-P7-E2013-APP`. The operation that raises an approval item is not published there (GAP-1889).
- The firm instruction itself, its pack, its lifecycle and the firm's result: `RWB-S4-E5009-APP` and rwb-partner (S9); this story asks for the instruction and records the filing.
- The pack, its documents, its checklist and its custody: rwb-document (P5) and the pack stories of this service, which also raise MSG-S4-001 when an item is missing.
- The demand and recall notice that precedes the petition: rwb-comms (P6) and the notice stories.
- The contract document itself: `RWB-S4-E5021-CON`.
- R-LIT-59 and R-LIT-60, the approved petition to the official receiver and the rejected petition to write-off: the partner stories and the write-off stories, with the case moves in rwb-case.
- The court status that arrives from LIT through COLLINS and rwb-source-data, and the hearings, judgment and enforcement steps of the same legal action: the sibling S4 stories; this story only reads their columns.
- The roles, rights, scope and masking data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-19 and SCR-20: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, its flag, its dashboards, its alerts and its runbook: its own OPS story.
- The cross-service journey of the petition across rwb-litigation, rwb-case and rwb-decision with live owners: the wave 3 integration harness.
