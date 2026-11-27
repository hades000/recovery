# RWB-S9-E7013-APP Hold a partner review

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E7013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S9-O |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E7013-APP-16) |
| Depends on (build) | RWB-S9-E7013-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the review slice of RWB-E7-013 is realigned onto rwb-partner (S9, service wave 4, business wave 4). The one legacy criterion this story owns, AC2, is kept word for word with its origin tag and needs no mock line, because its only dependency is the local decision record; AC1 of the key is owned by RWB-ITG-E7013-ITG and the review behind it is built and tested here. The review reads the partner and its instructions from `rwb_partner`, reads the six points and their action values as reference data at a version, evaluates the rule package in force in rwb-decision, writes one hash-linked decision record before anything is shown as done (DP-03) and answers SCR-34 and SCR-35 through the gateway-bff composite route (DP-19) on the base `/api/recovery/partner/v1` (DP-13). No rule row names a partner review, no operation records one, no list of action values is published and no column carries the outcome, so those values carry the placeholder (GAP-3125; ASM-5438 to ASM-5445). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E7013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 21 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **partner and agency manager (RW-AGENCYMG)** — and as a role that holds the Partner portal write right where the matrix gives another role only the read — I want **the Workbench to run the review of a partner against the six points every partner type is managed on and to record the actions**, so that **partners are placed, paid and measured by rule and the review is on the decision log with the rule version it was judged under**.

This is the application slice of legacy RWB-E7-013, feature FEAT-PRM-10 of module S9 Partner management (FSD S9 A2.10; Epics 3 to 8 Specification v3). It owns:

- the one legacy criterion this slice keeps, AC2, copied word for word with its origin tag; AC1 of the key is owned by RWB-ITG-E7013-ITG;
- the review of a partner against the six points of REQ-S9-001 — selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit — with the observation and the action of each point held as data at a version (FSD S9 A2.10.2; REQ-S9-001);
- the partner facts of the review: `partner` (`partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, `score`) and the instructions placed with the partner on `partner_instruction`, read on this service's own schema (TSD S9 T3.1, DF-PRT-001 to DF-PRT-016);
- the record of the review: one hash-linked entry per review through the local decision-record library, written **before** anything is shown as done, carrying the partner, the six point values, the actions, the rule ID and the package version in force, the reviewer and the instant (DP-03; legacy AC2; BR-S9-010);
- the read of the rule package and of the reference data at their versions, on the owners' contracts, so that no point, no status, no action and no rule version is written in code (DP-06, DP-07 recorded and not claimed; VR-S9-010-1; BR-S9-010);
- the review answer behind SCR-34 Partner list and SCR-35 Placement and allocation through the gateway-bff composite route (DP-19), on base `/api/recovery/partner/v1` (DP-13).

It does not own: AC1 of the legacy key and the cross-service evidence of the review, which are RWB-ITG-E7013-ITG's; the published shapes, the review-entry element, the consumed rows, the rights, the error set and the fakes, which are RWB-S9-E7013-CON's; the six REST operations of the service, which belong to the earlier stories of this service (API-S9-001 to API-S9-006, first in Epic 2 to Epic 6); the monthly scorecard itself (FEAT-PRM-08, RWB-S9-E7011-APP); the approval of partner fees (FEAT-PRM-09, RWB-S9-E7012-APP); the notice on a missed target (FEAT-PRM-11, RWB-S9-E7014-APP); the end of a contract and the recall of the work (FEAT-PRM-12, RWB-S9-E7015-APP); the conduct check and the breach report (FEAT-PRM-13, RWB-S9-E7016-APP); the partner panel and the fee schedule as data (FEAT-PRM-02, RWB-S9-E6030-APP); the case of record and its workflow (rwb-case P3); the rule rows and the central ledger (rwb-decision P7); the roles and the lists of values (rwb-access P4); the documents and the notices (rwb-document P5, rwb-comms P6); and the schema, the migration and the deployment of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

Partners are instructed and paid by email and spreadsheet, and allocation is not based on performance (FSD S9 A1.3, repeated in A2.10.1). The requirement is REQ-S9-001: "Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit", with REQ-S9-007 for the forum the review reports to (FSD S9 Requirements served, Must, E6 and E7). The metric is the module's: placements by scorecard at 100 percent, measured on the decision log and the Workbench records and reviewed monthly (FSD S9 A2.10.1).

A review that is not recorded is a conversation: the placement that follows it, the notice that follows that and the exit that follows the notice all have to point at one decision taken against one version of the rules. The legacy criterion says exactly that — "the system writes the result to the decision log with the rule version" — and stops the act dead when the record cannot be written. Under D-RCV-60 the facts of that act split three ways, and none of them moves:

- **The partner is this service's fact.** `partner` carries the code, the registered name, the type, the panel status, the contract end and the score of the partner, and `partner_instruction` carries the work placed with it (TSD S9 T3.1; DF-PRT-001 to DF-PRT-016). The review reads its own schema and needs no second service to say what the partner is.
- **The rule version is rwb-decision's.** Legacy AC1 asks for the result "with the rule version"; the rule rows and their versions are governed in rwb-decision (P7), so this service evaluates the package in force and records the ID and version on its own entry, exactly as the local-record pattern asks (DP-03).
- **The points are reference data, not constants.** BR-S9-010 forbids any value a business person may change from being written in code. The six points, the statuses the reviewer records and the action list are therefore rows read at a version — and where no list is published, the placeholder stays and the gap is raised rather than a value invented (GAP-3125; ASM-5438, ASM-5442).
- **The review moves nothing else.** The panel status, the contract end, the recall and the notice are separate acts of FEAT-PRM-11, 12 and 13 on their own criteria and rules (R-UNI-25 to R-UNI-29, R-UNI-45). This story records the review and its actions and leaves the partner row exactly as it found it (ASM-5439).

### 3. Preconditions

- RWB-S9-E7013-CON is published and tagged: the review-entry element, the unchanged `partner` and `partner_instruction` elements, the consumed rows, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the act with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-34 and SCR-35 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `partner`, `partner_instruction` and `partner_user` exist in `rwb_partner` from the DB story of this service, with the standard record columns of TSD S9 T3.0, and at least one partner of each `LOV-PARTNER-TYPE` value and one instruction per status of `LOV-INSTR-STATUS` are available as test data (TSD S9 T3.1, T3.2).
- The rule package in force is available at its version, authored, tested and approved in rwb-decision (P7) and loaded here; no source gives a rule row whose event is a partner review, so the review records the package version it evaluated and invents no rule ID (GAP-3125; ASM-5440).
- The reference-data read of rwb-case is published with its fake: `LOV-PARTNER-TYPE`, `LOV-PANEL`, `LOV-INSTRUCTION`, `LOV-INSTR-STATUS` and the six-point list, each with its version; its operation name is Not specified in the source documents (GAP-3125; ASM-5443).
- The scorecard this review reads is the `partner.score` of FEAT-PRM-08, written by RWB-S9-E7011-APP inside this service; the plan carries no H row to that story, so the review builds against a seeded score and treats a missing score as a stated absence (GAP-3125; ASM-5443).
- The service runs as its own login on `rwb_partner`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, on `rwb_decision` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S9-E7013-CON when its tests pass.

### 4. Flow

1. The partner and agency manager opens SCR-34 Partner list and selects a partner, or opens SCR-35 Placement and allocation and selects the partner from a placement (legacy screens table; FSD S9 Screens).
2. The gateway-bff composite route merges the partner answer of this service with the case label of rwb-case and the scorecard block of this service, one hop each, in parallel (DP-19; ASM-5441).
3. `readReviewFacts` reads the partner row (`partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end`, `score`) and the instructions placed with it (`instruction_type`, `status`, `due_at`, `result_code`, `fee_amount`) on `rwb_partner`, read only (TSD S9 T3.1).
4. `loadReviewReference` reads the six points of REQ-S9-001 in their order, the statuses the reviewer may record and the list of actions, each with its version, on the reference-data contract of rwb-case; where a list is not published the value is Not specified in the source documents (GAP-3125; ASM-5438, ASM-5442).
5. `evaluateReviewRules` loads the package version in force from rwb-decision and returns the rule ID and version the review is judged under; the review records the version whether or not a row names the review (GAP-3125; ASM-5440).
6. The manager records, for each of the six points, the observation and the action taken, and confirms the reviewer and the review date; a required value left empty is refused with MSG-GEN-001 (VR-S9-010-1).
7. `recordReview` writes one hash-linked entry through the local library **before any other effect**: the partner reference, the six point values with their action, the rule ID and package version, the reviewer identity and the instant. A failed write changes nothing and returns MSG-P7-003 (DP-03; legacy AC2).
8. The review answer is returned to the composite route with the entry reference, the six points, the actions and the rule version, and SCR-34 and SCR-35 show it as the recorded review of the partner (FSD S9 A2.10.2 step 3).
9. The partner row is not written: `panel_status` and `contract_end` stay as they were, and the review raises no instruction, no notice and no recall — those are FEAT-PRM-11, 12 and 13 on their own criteria and rules (ASM-5439).
10. A repeated submission for the same partner and the same review date is idempotent on its key: the stored answer is returned, one entry exists, and the repeat is recorded as an idempotency hit (R-UNI-40).
11. A role without the Partner portal right of the act is refused before any read of the partner and before any record, with MSG-P4-002 (TSD S9 T6.1; legacy permission table).
12. A conduct breach found during the review is not acted on here: R-UNI-29's suspend, recall and report is the partner conduct story's separate act and is recorded against the review for its evidence (R-UNI-29; ASM-5439).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no entry, no action recorded, no review shown as done, and the partner row is untouched | MSG-P7-003 | AC2, TC-E7-013-02, TC-E7-013-04 |
| X2 | The role does not hold the Partner portal right of the act | 403 before any read and before any record, with the same check on the composite route and on any service identity | MSG-P4-002 | AC3, TC-E7-013-03, TC-E7-013-19 |
| X3 | A required value is absent or invalid: no partner, no point, no status, no reviewer or no review date | The act is refused, nothing is written and the field is named | MSG-GEN-001 (VR-S9-010-1) | AC2 |
| X4 | The reference-data read or the rule-package read does not answer inside 2 s, or its breaker is open | The screen shows no review form, nothing is written and the platform 503 envelope is returned; the read is retried once with jitter on a GET | None (platform envelope) | AC4, AC14, AC15, TC-E7-013-05, TC-E7-013-16, TC-E7-013-17, Section 12.2 |
| X5 | No list is published for the statuses or the actions of a point | The point is shown with its observation and the action value carries the placeholder; the review may be recorded with the placeholder, and the gap is reported | None | AC5, TC-E7-013-06, GAP-3125 |
| X6 | `partner.score` is empty because the monthly scorecard has not run | The performance-review point shows the absence and its date, and the review records that absence; no score is invented | None | AC6, TC-E7-013-07, ASM-5443 |
| X7 | The same partner and review date are submitted twice | One entry per key; the stored answer is returned and the repeat is counted | None | AC7, TC-E7-013-08, R-UNI-40 |
| X8 | The action recorded against a point would change the panel status, send a notice or end the contract | The review records the observation only; the action is refused as out of this story and routed to FEAT-PRM-11, 12 or 13 | None | AC8, TC-E7-013-09, Section 19 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_case` row, a `rwb_decision` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC9, TC-E7-013-10, Section 17, BR6, BR7 |

X1 and X2 are the legacy not-recorded and access paths of this key carried onto the slice; X3 to X8 are the paths the reference data, the scorecard and the target call types add; X9 is the schema and ACE boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S9-E7013-CON, the decision-record stub, the reference-data fake, the rule-version fake and the gateway-bff fake, on its own schema, and needs no live P3 or P7 |
| Negotiable | The activity names, the shape of the review entry and the screen layout are this story's choice; the six points, the lists, the messages, the rule version and the rights are fixed |
| Valuable | A partner is reviewed on the same six points as every other partner type, the actions are recorded, and the result is on the decision log with the rule version it was judged under |
| Estimable | One read step, one reference step, one rule step, one record write, three clients and one screen slice |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on synthetic partners through the contract fakes, plus the refused-right, the missing-value, the empty-score and the forced record-write failure |

### 7. Acceptance criteria

```gherkin
Feature: Hold a partner review

  Background:
    Given the rule package in force and the reference data of the six points are read at their versions
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Not recorded (legacy RWB-E7-013 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Partner portal right not held (story exception X2) (new, D-RCV-60)
    Given the role does not hold the Partner portal right of the act
    When the review is requested
    Then the call is refused with 403 before any read and before any record, and the user sees MSG-P4-002

  Scenario: AC4 Reference data or rule package not answered (story exception X4) (new, D-RCV-60)
    Given the reference-data read or the rule-package read does not answer inside 2 s, or its breaker is open
    When the review form is opened
    Then the screen shows no review form, nothing is written, the platform 503 envelope is returned and the read is retried once with jitter on a GET

  Scenario: AC5 No published list for a point (story exception X5) (new, D-RCV-60)
    Given no list is published for the statuses or the actions of a point
    When the review is recorded for that point
    Then the point is shown with its observation, the action value carries the placeholder, the review may be recorded with the placeholder and the gap is reported

  Scenario: AC6 Empty partner score (story exception X6) (new, D-RCV-60)
    Given partner.score is empty because the monthly scorecard has not run
    When the performance-review point is shown
    Then the point shows the absence and its date, the review records that absence and no score is invented

  Scenario: AC7 Repeat submission (story exception X7) (new, D-RCV-60)
    Given the same partner and review date are submitted twice
    When the second submission arrives
    Then one entry is kept per key, the stored answer is returned and the repeat is counted

  Scenario: AC8 Action out of scope (story exception X8) (new, D-RCV-60)
    Given the action recorded against a point would change the panel status, send a notice or end the contract
    When the action is recorded
    Then the review records the observation only, and the action is refused as out of this story and routed to FEAT-PRM-11, 12 or 13

  Scenario: AC9 Boundary (story exception X9) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a rwb_case row, a rwb_decision row or another service's schema
    When the build runs the boundary test
    Then the grant refuses the statement, the boundary test fails the build and nothing is released

  Scenario: AC10 The review moves nothing else (BR4, BR10 to BR14 and BR17) (new, D-RCV-60)
    Given a review outcome is recorded for a partner
    When the review is recorded
    Then panel_status, contract_end, the recall, the notice and the conduct report are not changed and no rule of R-UNI-25 to R-UNI-29 or R-UNI-45 fires

  Scenario: AC11 No personal data (BR8) (new, D-RCV-60)
    Given a review is recorded
    When the entry, a log or a workflow input is written
    Then no person name, address, contact value or identity number is stored in rwb_partner, the entry, the log or the workflow input

  Scenario: AC12 Refusal as a problem document (BR9) (new, D-RCV-60)
    Given a review act is refused
    When the service answers
    Then the answer is one problem document with a code, the message ID and a correlation reference, and no message text is assembled in code

  Scenario: AC13 Six points, partner and rule version read and not written (BR2, BR3, BR5) (new, D-RCV-60)
    Given the six points, the partner and its instructions are read on their owners' contracts and the rule version is read from rwb-decision
    When the review is recorded
    Then the six points, the partner and its instructions are not written, the rule version is recorded with the entry and no rule ID is invented where no row names the review

  Scenario: AC14 Activity retried or timed out (story exception X4) (new, D-RCV-60)
    Given a synchronous step of the act does not finish inside its 2 s budget or a read is retried
    When the review form is opened or the review is recorded
    Then the read is retried once with jitter on a GET, the platform 503 envelope is returned if it still fails and nothing is written

  Scenario: AC15 Consumed call fails or does not answer (story exception X4) (new, D-RCV-60)
    Given a consumed call of the act fails or does not answer
    When the review is requested
    Then nothing is written, the screen shows no review form and the platform 503 envelope is returned

  Scenario: AC16 Status change the model does not allow is refused (BR9) (new, D-RCV-60)
    Given a status change that the model does not allow is requested for a partner, the allowed changes being Not specified in the source documents (NEWAC-RWB-S9-E7013-APP-AC13)
    When the change is requested
    Then the change is refused as one problem document with a code, the message ID and a correlation reference, and nothing is written
```

The criterion is the legacy AC2 of the key, word for word apart from "decision log" read as "decision record" (DP-03), and is the legacy criterion this slice owns; AC3 to AC16 cover the exception paths of section 5 and the business rules of section 8, each with its test row in section 16; it needs no mock line because its only dependency is the local decision record, which is not a cross-service call, and every value of the legacy text is kept. AC1 of the same key — "Then runs the review against the six points every partner type is managed on, and records the actions / Then the system writes the result to the decision log with the rule version" — is owned by RWB-ITG-E7013-ITG, which carries the cross-service journey of the key in wave 4; the review behind it is built and tested here and is stated in sections 4, 8 and 16. On this story "the action" is the review act of a partner against the six points, and the decision record of DP-03 is the local record in `rwb_partner`, with the `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer | BR ID |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-UNI-25 | Universal rules | All | ANY_ACTIVE | PARTNER_NO_RESPONSE | the partner misses the service level on the portal | Chase once, then recall the work and re-select on the scorecard | PARTNER_RECALLED | Partner and agency manager | Partner Portal | per partner type | BR10 |
| R-UNI-26 | Universal rules | All | ANY_ACTIVE | PARTNER_PANEL_EXIT | the partner leaves the panel or the contract ends | Recall every open case held by that partner and re-select | PARTNER_RECALLED | Partner and agency manager | Partner Portal | 5 working days | BR11 |
| R-UNI-27 | Universal rules | All | ANY_ACTIVE | PARTNER_CONFLICT_DECLARED | the partner declares a conflict of interest | Withdraw the instruction, re-select the next partner on the scorecard | PARTNER_RECALLED | Partner and agency manager | Partner Portal | 2 working days | BR12 |
| R-UNI-28 | Universal rules | All | ANY_ACTIVE | PARTNER_INSOLVENT | the partner enters insolvency | Recall the work, secure the documents and any cash held, stop fee payments | PARTNER_RECALLED | Head of the partner type | Partner Portal, Workbench | same day | BR13 |
| R-UNI-29 | Universal rules | All | ANY_ACTIVE | PARTNER_CONDUCT_BREACH | a conduct or complaint breach is upheld against the partner | Suspend allocation, recall the affected cases, report to the partner review | PARTNER_RECALLED | Partner and agency manager | Partner Portal | same day | BR14 |
| R-UNI-39 | Universal rules | All | ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written | Block the action and raise an incident. No action proceeds unlogged | EXCEPTION_QUEUE | Platform team | Workbench | immediate | BR15 |
| R-UNI-40 | Universal rules | All | ANY_ACTIVE | DUPLICATE_EVENT | the same event arrives twice with the same key | Ignore the second event, record the idempotency hit | RESUME_STATE | Workbench | Workbench | None | BR16 |
| R-UNI-45 | Universal rules | All | PARTNER_RECALLED | PARTNER_RESELECTED | the next partner is selected on the scorecard | Re-issue the instruction and restart the partner clock | ROUTE_D6_REOPEN | Partner and agency manager | Partner Portal | 2 working days | BR17 |

The eight rows are copied character for character, apart from the BR ID in the last column, from the Business Rules and Routing Logic v4. R-UNI-25 to R-UNI-29 and R-UNI-45 are the partner rules of the module: they are the consequences of a review outcome and belong to FEAT-PRM-11 to FEAT-PRM-13, so this story reads them and fires none of them. R-UNI-39 is the record-first rule of the act and R-UNI-40 is the repeat rule. Their owner column names a business role and a system, not a service: "Workbench" is this service, and "Partner Portal" is the external gateway in front of it.

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The review is a decision first: one hash-linked entry per review is written through the local library with the partner, the six point values and their actions, the rule ID and package version, the reviewer and the instant, and a failed write changes nothing and answers MSG-P7-003 | DP-03; TSD S9 T2; R-UNI-39; legacy AC2 | AC2, TC-E7-013-02, TC-E7-013-04 |
| BR2 | The six points are REQ-S9-001's: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit; they are read at a version and never written in code | REQ-S9-001; FSD S9 BR-S9-010; ASM-5438 | AC13, TC-E7-013-15 |
| BR3 | The partner is this service's fact and is read only: `partner` and `partner_instruction` are read on `rwb_partner` and no column of them carries the review or its actions | TSD S9 T3.1, T3.3; ASM-5439 | AC13, TC-E7-013-15 |
| BR4 | The review moves nothing else: `panel_status`, `contract_end`, the recall, the notice and the conduct report are the acts of FEAT-PRM-11 to FEAT-PRM-13 and of R-UNI-25 to R-UNI-29 | Business Rules and Routing Logic v4; ASM-5439 | AC10, TC-E7-013-11 |
| BR5 | The rule version is read from rwb-decision and recorded with the entry; no rule ID is invented where no row names the review | TSD S9 T2; DP-03; GAP-3125 | AC13, TC-E7-013-15 |
| BR6 | The lists of values and the six-point list are reference data read on the owner's contract; a status or an action that has no published list is recorded with the placeholder of X5, not as a value | Template and Rules §R9; ASM-5442 | AC5, TC-E7-013-06 |
| BR7 | No cross-schema join and no foreign key leaves `rwb_partner`; `case_id` and `partner_id` are identifiers of other services' or other modules' facts | DP-01; TSD S9 T3.3 | AC9, TC-E7-013-10 |
| BR8 | No person name, address, contact value or identity number enters `rwb_partner`, the entry, a log or a workflow input; the registered name of the firm is not personal data and every example is synthetic | Template and Rules §R7.2 (s17); FSD S9 A2.10.3.2 | AC11, TC-E7-013-12 |
| BR9 | Every refusal is one problem document with a code, the message ID and a correlation reference, and no message text is assembled in code | VR-S9-010-1; BR-S9-010 | AC12, TC-E7-013-13 |

### 9. State transitions

The service has no case state machine of its own: it acts on the case's events and writes through the decision log (TSD S9 T4). The panel status of a partner is a value of `LOV-PANEL` — ACTIVE, ON_NOTICE, SUSPENDED, EXITED — and **this story writes none of it**: the review records an observation and an action, and the status moves only on the separate acts of the notice and the contract end (ASM-5439).

| From (`partner.panel_status`, read) | The review act | Condition | What this story writes |
|---|---|---|---|
| `ACTIVE` | A review is recorded against the six points | The reviewer holds the right and every required value is present | One entry; the partner row is unchanged |
| `ON_NOTICE` | A review is recorded | The partner is inside its cure period | One entry; the cure period and its clock are not touched |
| `SUSPENDED` | A review is recorded | The suspension has its own reason row | One entry; the suspension is not lifted |
| `EXITED` | A review is recorded | The contract has already ended | One entry as historical evidence; no case is recalled here |
| Any | The record write fails | X1 | Nothing; the partner row and the screen are unchanged |
| Any | The same partner and review date are submitted again | X7 | Nothing new; the stored entry is answered |

| Review step execution | Event | Condition | To |
|---|---|---|---|
| Open | The manager selects the partner | The right and the scope are checked | Reading |
| Reading | The partner, the instructions and the reference data are read | The six points and their versions are in place | Evaluating |
| Reading | A consumed read does not answer inside 2 s | X4 | Closed, nothing written |
| Evaluating | The rule package in force is loaded and the values are confirmed | Every required value is present | Recording |
| Recording | The entry is written | The transaction commits | Recorded |
| Recording | The entry write fails | X1 | Open, nothing changed, MSG-P7-003 |
| Recorded | A repeat arrives for the same key | R-UNI-40 | Recorded; the stored answer is returned |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Partner and agency manager (RW-AGENCYMG) | The primary actor of FSD S9 A2.10.3.3: holds Partner portal CRUDA (TSD S9 T6.1), runs the review and records its actions |
| Litigation officer (RW-LITOFF), enforcement owner (RW-ENFORCE), sale officer (RW-SALEOFF), NPA and asset manager (RW-NPAMGR), debt sale officer (RW-DEBTSALE), guarantee officer (RW-GUARANT) | Partner portal CRU: hold the write right of the act on the partner their work touches, as the legacy permission table lists them under right U |
| Head of Litigation (RW-HEADLIT), Head of Asset Liquidity (RW-HEADASL) | The "also uses" roles of FSD S9 A2.10.3.3; TSD S9 T6.1 gives them RA, so they read and approve and take no U act |
| Partner portal users (PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC) | Partner portal RU: see the review outcome of their own firm and its scope; they never run the bank's review |
| Case owner (RW-CASEOWN), team manager (RW-TEAMMGR), legal counsel (RW-LEGAL) and the remaining read roles | Partner portal R: read the review and its rule version |
| rwb-decision (P7) | Owns the package, the rule rows and the central ledger; this story evaluates the version and records locally |
| rwb-case (P3) | Owns the case, its stage and its timers, and answers the case label on the composite route; this story writes no case fact |
| rwb-access (P4) | Owns the roles, the capability rights and the lists of values this story reads through the guard |

No delegated authority limit applies: the review takes no credit decision and approves no money, and the only approvals in the module are the fee approval of FEAT-PRM-09 and the route approvals of the other modules.

### 11. Data

| BR Field ID | Entity | Owner | Use in this story |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | `partner` | S9, `rwb_partner` | **Read** only: `id`, `partner_code`, `partner_name`, `partner_type`, `panel_status`, `contract_end` and `score`; no column carries the review, a point or an action (ASM-5439) |
| DF-PRT-008 to DF-PRT-016 | `partner_instruction` | S9, `rwb_partner` | **Read** only: `id`, `case_id`, `partner_id`, `instruction_type`, `instructed_at`, `due_at`, `status`, `result_code` and `fee_amount`, as the evidence of the work placed with the partner |
| None: library table | `decision_record` | Platform library in `rwb_partner` | **Write**: one hash-linked review entry per review, before anything else (DP-03) |
| None: library table | `idempotency_key` | Platform library in `rwb_partner` | The key of the repeat (partner and review date) and the answer it holds (R-UNI-40) |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | Not written: the local entry is copied to the central ledger by its owner, and its identifier is not stored here |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | Not read as a table: the package arrives loaded at its version in force (ASM-5440) |
| `LOV-PARTNER-TYPE`, `LOV-PANEL`, `LOV-INSTRUCTION`, `LOV-INSTR-STATUS` | reference data and lists of values | P3 rwb-case (default ruling) | Read at their version; `LOV-PARTNER-TYPE` carries AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC and RAMC, and `LOV-PANEL` carries ACTIVE, ON_NOTICE, SUSPENDED and EXITED (TSD S9 T3.2) |
| The six points and the action list | reference data | P3 rwb-case (default ruling) | Read at their version; the six points are REQ-S9-001's and the action list is Not specified in the source documents (GAP-3125; ASM-5438, ASM-5442) |

No new table, no new column and no migration: the three tables arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in `rwb_partner` by the library's own migration (DP-03). `partner_user` is this service's third table and is not read by this act, because the reviewer is a Workbench user and not a partner portal identity (ASM-5439).

**No personal data.** The entry carries identifiers, point values, action values, a rule version and an instant. No name of a person, address, contact value or identity number enters `rwb_partner`, the entry, a log or a workflow input; the partner's registered name is a firm name and is marked not personal in FSD S9 A2.10.3.2 (BR8).

### 12. Contract

Contract version: Not specified in the source documents (DOR-RWB-S9-E7013-APP-23). The base is /api/recovery/partner/v1.

Contract fake library version: Not specified in the source documents (DOR-RWB-S9-E7013-APP-22).

#### 12.1 REST operations provided

None declared by this story. Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The Ownership Map gives this service exactly six operations — `GET /partners` (API-S9-001), `POST /cases/{caseId}/instructions` (API-S9-002), `GET /partner/instructions` (API-S9-003), `POST /partner/instructions/{instructionId}/accept` (API-S9-004), `POST /partner/instructions/{instructionId}/results` (API-S9-005) and `POST /partner/instructions/{instructionId}/invoices` (API-S9-006) — and none of them records a review: their shapes are the frozen baseline of RWB-S9-AD022-CON, their first-in epics are Epic 2 to Epic 6, and they serve the panel, the instructions, an acceptance, a result and an invoice (TSD S9 T-A.1). The two endpoints of the legacy story are those results and instructions operations, which are the earlier stories' of this service. The review act therefore has no published entry point, and the review read behind SCR-34 and SCR-35 is Not specified in the source documents (GAP-3125; ASM-5441). A build that declares a review operation here fails the absence test of RWB-S9-E7013-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The rule-package and rule-row read; operation name Not specified in the source documents (GAP-3125; ASM-5440) | `/api/recovery/decision/v1` | P7 rwb-decision | The package and the rule-row version in force at the review instant, and any row that names a partner review; read only, faked |
| The reference-data read; operation name Not specified in the source documents (GAP-3125; ASM-5443) | `/api/recovery/case/v1` | P3 rwb-case, as the owner of parameters and reference data (R3 default ruling) | The six points of REQ-S9-001, the status list, the action list and the four lists of TSD S9 T3.2, each with its version; read only, faked |

Each row is one hop with a 2 s timeout, one retry with jitter on a GET and a breaker per downstream (ADR-020, DP-11). Both are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3125; ASM-5440, ASM-5443).

#### 12.3 Events published

None. The service publishes on `rwb.partner.events.v1` and its event set is `InstructionIssued` (EV-20) and `PartnerResultSubmitted` (EV-21), both of which report an instruction or a result and therefore belong to the instruction stories of this service (context pack ownership rows; TSD S9 T5.3). A review issues no instruction and submits no result, so this story declares no producer group, no envelope and no outbox row, and RWB-S9-E7013-CON fails a build that adds one (ASM-5444).

#### 12.4 Events consumed

None. The service listens to the case events of rwb-case on the module's published interfaces, and that subscription belongs to the case alignment of the partner stories (TSD S9 T4, T5.2). The review is started by a person on a screen and needs no event, so this story declares no consumer group, no subscription and no inbox of its own (ASM-5444).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, the service's only one | `rwb-partner` | Owned by the instruction stories of this service; this story registers no workflow, no activity and no durable timer. Workflow ID form: Not specified in the source documents (CG-ALL-12019). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-12019) |
| `readReviewFacts` | Activity, synchronous step of the act | `rwb-partner` | Not a Temporal activity of its own: the read is a service call inside the request, with the same 2 s budget |
| `loadReviewReference` | Synchronous step | `rwb-partner` | The reference-data read and the six-point list with its version |
| `evaluateReviewRules` | Synchronous step | `rwb-partner` | The package in force in; the rule ID and version out |
| `recordReview` | Synchronous step, one transaction | `rwb-partner` | The entry, the reviewer and the answer out, one transaction |

The service has no case state machine of its own and no job (TSD S9 T4; context pack Jobs 0), so the review is a synchronous act whose only durable artefact is the decision record. No source puts the review inside `InstructionWorkflow`, and this story starts no workflow and no child workflow (ASM-5445).

#### 12.6 Schedules

None. The Ownership Map gives S9 no job (context pack ownership rows, Jobs: 0), and FSD S9 A2.10.4.4 declares no background event for the feature. DP-10 is not in this key's pattern set and no Temporal Schedule, no Quartz row and no shared job table is declared (ASM-5445).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `partner` | S9, `rwb_partner` | The partner, its type, its panel status, its contract end and its score; read only here |
| `partner_instruction` | S9, `rwb_partner` | The work placed with the partner; read only here |
| `partner_user` | S9, `rwb_partner` | The partner portal identities of the firm; not read by this act |
| `decision_record` | Platform library in `rwb_partner` | The local hash-linked review entry (DP-03) |
| `idempotency_key` | Platform library in `rwb_partner` | The key of the repeat and the answer it holds |

Not owned and never read as a table: `recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6), `interaction` (P1) and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain, a stopped chain and a hash break | AC2, TC-E7-013-02, -04 |
| rwb-decision rule-version fake | The package at its version in force with no row naming a partner review, and a package with no version in force; the operation name carries the placeholder (GAP-3125; ASM-5440) | TC-E7-013-01 |
| rwb-case reference-data fake | The six points in REQ-S9-001's order with their version, `LOV-PARTNER-TYPE`, `LOV-PANEL`, `LOV-INSTRUCTION` and `LOV-INSTR-STATUS`, an unpublished action list, and no answer inside 2 s; the operation name carries the placeholder (GAP-3125; ASM-5443) | TC-E7-013-01, X4, X5 |
| gateway-bff composite route fake | The merged SCR-34 and SCR-35 answer for a synthetic partner, with the review slice of this service read once | TC-E7-013-01 |
| Authorise stub of the service template | Partner portal right U held, and a caller without it | TC-E7-013-03 |

The fakes are test-only and are replaced by the real services in SIT. The two consumed operation names are placeholders until their owners publish them (GAP-3125; ASM-5440, ASM-5443).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | The rwb-decision rule-package read and the rwb-case reference-data read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-20 and EV-21 are the instruction stories'; the decision record rides the library's shared `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 0 registered | `InstructionWorkflow` is the service's and is not started by this act; no activity, no durable timer and no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.partner`, module `review`; front end `src/modules/recovery/partner/PartnerReview.tsx`, the SCR-34 and SCR-35 fragment this story answers.

**Pattern application** (§R5.5)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the act: the entry commits before the review is answered, and a failed write leaves nothing behind. DP-13 fixes the base of the service and gives the review no operation of its own, because the six operations are the earlier stories'. DP-19 is how the SCR-34 and SCR-35 slice reaches this service, one hop through the gateway. Three patterns the plan does not carry are real dependencies here and are recorded rather than added: DP-06 and DP-07, the reference data of rwb-case (ASM-5443), and DP-04, the rule package of rwb-decision, which is evaluated but whose embedded-kit story is not claimed (ASM-5440).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PartnerReviewService` | Service | Composes the review, checks the right, applies the six points and calls the record |
| `PartnerReader` | Repository | The partner row and its instructions on `rwb_partner`, read only |
| `ReviewReferenceClient` | Client | The six points, the statuses, the actions and the four lists, read at a version with a 2 s budget and a breaker |
| `RuleVersionClient` | Client | The package and rule-row version in force, read once per review |
| `ReviewRecordWriter` | Library adapter | Writes the hash-linked entry before any other effect and refuses the act when the write fails |
| `IdempotencyGuard` | Library adapter | One entry per partner and review date, and the stored answer on a repeat |
| `PartnerReview` | React component | The review slice of SCR-34 and SCR-35, with the six points, their observations and their actions |

**Database and migrations.** No Flyway file. `partner`, `partner_instruction` and `partner_user` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in `rwb_partner` by the library's migration (DP-03). No column is added for the review, because no column of `partner` or `partner_instruction` carries it (ASM-5439).

**Configuration and reference data.**

- The six points of REQ-S9-001, their order, the status list and the action list: reference data with their version, never a constant (ASM-5438, ASM-5442).
- `LOV-PARTNER-TYPE`, `LOV-PANEL`, `LOV-INSTRUCTION` and `LOV-INSTR-STATUS`: TSD S9 T3.2's values, read at their version.
- The capability area "Partner portal" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. `PartnerReader` and `PartnerReviewService` on the seeded partner and instruction data, read only (TC-E7-013-01).
2. `ReviewReferenceClient` against its fake, with the six points, the four lists, the unpublished action list and the unavailable path (TC-E7-013-01, X4, X5).
3. `RuleVersionClient` and the rule-version read, with the unversioned-package path (TC-E7-013-01).
4. `ReviewRecordWriter` against the stub, with the failed-write path and MSG-P7-003 (AC2, TC-E7-013-02, TC-E7-013-04).
5. `IdempotencyGuard` and the repeat path on partner and review date (X7).
6. The right check on the act and on the read, with the refused path and MSG-P4-002 (TC-E7-013-03).
7. The review slice of `PartnerReview` on SCR-34 and SCR-35 through the composite route fake (TC-E7-013-01).
8. The boundary test: no statement outside `rwb_partner`, no `v_ace_*` read, no `rwb_case` row, no `rwb_decision` row and no write to another service's schema (X9, BR7).

**Feature flag.** `rwb.partner.review-v1`, a flag of the platform library; off means the review slice is hidden on SCR-34 and SCR-35 and no entry is written, and the other partner features are unaffected.

**Done when.** The tests of section 16 pass, the review records one entry with its rule version on a synthetic partner in SIT, a failed write changes nothing, a repeat writes once, the six points and their actions come from reference data, no `rwb_case` or `rwb_decision` row and no `v_ace_*` read exists in the build, and SCR-34 and SCR-35 answer through the composite route.

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. | A required value of the review is absent or invalid (X3, VR-S9-010-1) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | A role without the Partner portal right of the act takes it (X2) |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The review entry cannot be written before anything else (X1, AC2) |

The three IDs are those of the legacy message set of this key; the text is the legacy and FSD S9 wording, copied unchanged, and no message is reworded and no new one is added. R-UNI-39's incident is raised by the platform on the same failure and is not a message of this service.

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-34 Partner list | Loading; list; review open; review recorded; refused; not recorded; empty, error and no access: Not specified in the source documents (CG-ALL-12024) | The review slice of the partner list: the partner, its type, its panel status, its score, the six points, their observations and their actions, and the rule version |
| SCR-35 Placement and allocation | Loading; list; review open; review recorded; empty, error and no access: Not specified in the source documents (CG-ALL-12025) | The review of the partner a placement sits with, on the same six points, with the instructions placed with it as evidence |

Both screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case label and this service for the partner and its instructions; this story fixes only its own review answer, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON (ASM-5441). SCR-36 Partner scorecard is FEAT-PRM-08's screen (RWB-S9-E7011-APP) and is not answered here. The review read itself is a placeholder, because no source publishes an operation for it (GAP-3125). The refused, not-recorded, empty-score and unavailable states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-013-01 | AC1 (run by RWB-ITG-E7013-ITG) | Component | The synthetic partner `P-2026-000713` of type AGENCY in panel status ACTIVE with an instruction in status DONE: one decision record with the six points, their actions and the rule version; no value of the six points or of the lists is a constant of the build |
| TC-E7-013-02 | AC2 | Component | The same partner; the decision-record stub stops the chain, so no entry is written and MSG-P7-003 is returned |
| TC-E7-013-03 | Access | Component | A role without the Partner portal right U is refused with MSG-P4-002, and nothing changes |
| TC-E7-013-05 | AC4 (X4) | Component | A reference-data or rule-package read that does not answer inside 2 s, or whose breaker is open, shows no review form, writes nothing and returns the 503 envelope, with one jittered retry on a GET |
| TC-E7-013-06 | AC5 (X5) | Component | A point with no published status or action list is shown with its observation, carries the placeholder and reports the gap |
| TC-E7-013-07 | AC6 (X6) | Component | An empty partner.score shows the absence and its date, is recorded as the absence and invents no score |
| TC-E7-013-08 | AC7 (X7) | Component | A repeat of the same partner and review date keeps one entry, returns the stored answer and counts the repeat |
| TC-E7-013-09 | AC8 (X8) | Component | An action that would change the panel status, send a notice or end the contract is refused and routed to FEAT-PRM-11, 12 or 13, and only the observation is recorded |
| TC-E7-013-10 | AC9 (X9) | Build | A statement or test reaching a v_ace_* view, a rwb_case row, a rwb_decision row or another service's schema fails the build and releases nothing |
| TC-E7-013-11 | AC10 (BR4) | Component | The review changes no panel status, contract end, recall, notice or conduct report and fires no rule of R-UNI-25 to R-UNI-29 or R-UNI-45 |
| TC-E7-013-12 | AC11 (BR8) | Component | The entry, a log and a workflow input carry no person name, address, contact value or identity number |
| TC-E7-013-13 | AC12 (BR9) | Component | A refused review act answers one problem document with a code, the message ID and a correlation reference, with no message text assembled in code |
| TC-E7-013-14 | Harness | Integration | The wave 4 harness environment, fixture layout, synthetic partner and instruction keys, evidence shape, retention and pass or fail gate are read from the harness configuration (GAP-0474) |
| TC-E7-013-04 | Principle 5 | Component | A forced decision-record write failure stops the action with MSG-P7-003 and raises one incident under R-UNI-39 |
| TC-E7-013-15 | AC13 (BR2, BR3, BR5) | Component | Not specified in the source documents (NEWAC-RWB-S9-E7013-APP-AC10) |
| TC-E7-013-16 | AC14 (X4 retry and timeout) | Component | Not specified in the source documents (NEWAC-RWB-S9-E7013-APP-AC11) |
| TC-E7-013-17 | AC15 (X4 consumed call fails) | Component | Not specified in the source documents (NEWAC-RWB-S9-E7013-APP-AC12) |
| TC-E7-013-18 | AC16 (BR9 disallowed status change) | Component | Not specified in the source documents (NEWAC-RWB-S9-E7013-APP-AC13) |
| TC-E7-013-19 | AC3 (X2 on the composite route and on a service identity) | Component | Not specified in the source documents (NEWAC-RWB-S9-E7013-APP-AC3) |

The four IDs are the legacy cases of RWB-E7-013 in their legacy order, with the Level column added: every case runs on the fakes, so every case is `Component`, and the legacy level `System` maps to `Component` because the artefact under test is the act against its contract fakes. The empty-score, the unpublished action list, the repeat and the unavailable-read paths are covered inside TC-E7-013-01 and by the new contract cases of RWB-S9-E7013-CON. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey of the key belongs to the wave 4 harness, whose copy of TC-E7-013-01 takes the `-ITG` suffix.

### 17. Guardrails

- No business value in code: the six points, the status list, the action list, the partner types, the panel states, the instruction lists and the rule versions stay rule rows or reference data read with their version.
- No personal data in `rwb_partner`, in an entry, a workflow input, a log or a prompt: identifiers, point values, action values, a rule version and an instant only; the registered name of the firm is not personal data and every example is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table.
- No read of another service's table: the partner and the instructions are read on `rwb_partner`, the reference data on rwb-case's contract and the package on rwb-decision's; `rwb_partner` is the only schema written.
- The record is written before the review is answered and in its transaction; a failure leaves nothing behind (DP-03, R-UNI-39).
- The review moves nothing else: `panel_status`, `contract_end`, the notice and the recall are FEAT-PRM-11 to FEAT-PRM-13's, and a build that writes the panel status here fails the review (BR4).
- One base, one topic, one queue and one login per service: `/api/recovery/partner/v1`, `rwb.partner.events.v1`, `rwb-partner` and the `rwb_partner` login; this story adds no second topic and no event (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no write to the retired legacy log and no data-lake path.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S9-001 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit (Must, E6) | The six points of the review and their versions | TC-E7-013-01 | FEAT-PRM-10 | Not specified in the source documents (DOR-RWB-S9-E7013-APP-2) |
| REQ-S9-007 | Partner performance, conduct and complaint data are reported to the partner review forum (Must, E7) | The review record and the evidence it leaves for the forum | TC-E7-013-01, TC-E7-013-02 | FEAT-PRM-10 | Not specified in the source documents (DOR-RWB-S9-E7013-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-partner as the owner of the partner and the review | TC-E7-013-01 | FEAT-PRM-10 | Not specified in the source documents (DOR-RWB-S9-E7013-APP-2) |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-E7-013-01 | FEAT-PRM-10 | Not specified in the source documents (DOR-RWB-S9-E7013-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget and breaker | TC-E7-013-01 | FEAT-PRM-10 | Not specified in the source documents (DOR-RWB-S9-E7013-APP-2) |
| ADR-022 | Local decision record plus central ledger | The review entry written before anything else | TC-E7-013-02, TC-E7-013-04 | FEAT-PRM-10 | Not specified in the source documents (DOR-RWB-S9-E7013-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-013, disposition Split (rework); feature FEAT-PRM-10 |
| Legacy criteria | AC2, owned word for word by this story; AC1 is owned by RWB-ITG-E7013-ITG |
| Source text | Legacy RWB-E7-013; FSD S9 Partner management v3 A2.10 and Requirements served; TSD S9 Partner management v2 T2, T3.0 to T3.3, T4, T5.1 to T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-UNI-25 to R-UNI-29, R-UNI-39, R-UNI-40 and R-UNI-45 |
| Test cases | TC-E7-013-01 to TC-E7-013-04 |
| Feature and screens | FEAT-PRM-10, SCR-34 Partner list and SCR-35 Placement and allocation |
| Rules | R-UNI-39 and R-UNI-40 evaluated; R-UNI-25 to R-UNI-29 and R-UNI-45 read and not fired |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- AC1 of the legacy key and the cross-service journey that evidences it: RWB-ITG-E7013-ITG.
- The published shapes, the review-entry element, the consumed rows, the rights, the error set and the fakes: RWB-S9-E7013-CON.
- The six REST operations of the service and the instruction flow behind them: the instruction stories of this service (API-S9-001 to API-S9-006, Epic 2 to Epic 6).
- The monthly scorecard that fills `partner.score`: FEAT-PRM-08, RWB-S9-E7011-APP.
- The approval of partner fees: FEAT-PRM-09, RWB-S9-E7012-APP; the notice on a missed target: FEAT-PRM-11, RWB-S9-E7014-APP; the end of a contract and the recall of the work: FEAT-PRM-12, RWB-S9-E7015-APP; the conduct check and the breach report: FEAT-PRM-13, RWB-S9-E7016-APP.
- The partner panel and the fee schedule as data: FEAT-PRM-02, RWB-S9-E6030-APP; the partner identities through the external gateway: RWB-S9-E2019-APP.
- The case of record, its stage and its timers: rwb-case (P3); the rule rows and the central ledger: rwb-decision (P7); the roles, the rights and the lists of values: rwb-access (P4); the documents and the notices: rwb-document (P5) and rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-34 and SCR-35: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
