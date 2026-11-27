# RWB-S8-E7010-APP Handle a contact sent while a block is on

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S8-U |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S8-E7010-APP-16) |
| Depends on (build) | RWB-S8-E7010-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract build status | RWB-S8-E7010-CON: Not started |
| Contract fake library version | Not specified in the source documents (DOR-RWB-S8-E7010-APP-22) |
| Contract version | Not specified in the source documents (DOR-RWB-S8-E7010-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the breach slice of RWB-E7-010 is realigned onto rwb-deviation (S8, service wave 2, business wave 4). The two legacy criteria of this key are kept word for word with their origin tag and only the `Given the <service> contract mock returns <x>` lines are added. The breach path is a branch of `DeviationWorkflow` on task queue `rwb-deviation`: it reads the outbound contact of the case from the interaction ledger of rwb-source-data (default ruling R3, DP-18) and the open deviation that holds the contact stop, records one breach entry through the local decision-record library before any change (DP-03), sets its handler and its clock and answers the parent with no clock change. It declares no REST operation, because the two operations of this service are RWB-S8-E7001-APP's, the breach read behind SCR-08 is reached through the gateway-bff composite route (DP-19) on base `/api/recovery/deviation/v1` (DP-13), and no event exists for a breach because EV-06 and EV-07 belong to the same earlier story. No rule row in the DEV or the UNIVERSAL set names a contact sent while a stop is on, no column of `deviation` carries a breach, its handler or its clock, the interaction-ledger read is unpublished, RW-CONDUCT holds R only on Case record while FSD S8 names it primary, and the service level is set with DL22 (GAP-3070; ASM-5218 to ASM-5225). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E7010-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 14 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Conduct and QA officer (RW-CONDUCT)** — and as the case role that holds the write right where the matrix gives the conduct officer a read — I want **the Workbench to open the breach path when a message has gone out against a contact stop**, so that **the breach has a named handler and a clock and the result is on the decision record with the rule version it was judged under**.

This story owns:

- the two legacy criteria of RWB-E7-010 (AC1 and AC2), copied verbatim with their origin tag, and the rule, message and screen behaviour they depend on;
- the `contactBreach` branch of `DeviationWorkflow` on task queue `rwb-deviation` in namespace `rwb-recovery`, as the always-on child of `CaseWorkflow` started at any time (context pack Temporal slides 5, 8 and 13);
- the read of the outbound contact of the case on the interaction ledger of rwb-source-data and the read of the open deviation whose `contact_stop` is true (ASM-5218, ASM-5220);
- the breach entry: one record per breach, written through the local decision-record library **before** anything else, carrying the deviation, the interaction, the channel, the sent-at instant, the rule ID and the package version in force (DP-03; legacy AC1 and AC2);
- the breach handler and the breach clock: the Conduct and QA officer as handler, the deviation service level as the clock and the team manager as the escalation point on breach (R-DEV-20, ASM-5221);
- the stage answer to rwb-case: the breach reference, the rule IDs with their versions and `NO_CLOCK_CHANGE`, because the deviation that holds the stop has already paused the stage clock and a breach moves neither the case nor its timers (R-UNI-30, ASM-5220);
- the read-only breach slice of SCR-08 behind the gateway-bff composite route (DP-19), on the service base `/api/recovery/deviation/v1` (DP-13).

It does not own: the published shapes, the breach-entry element, the consumed rows, the rights, the error set and the fakes (RWB-S8-E7010-CON); the two operations of the service and the raise of the deviation itself (RWB-S8-E7001-APP); the blocking of an outbound contact when a stop is in force (FEAT-OCC-06, rwb-comms P6, already built in Epic 2); the matching of a complaint to the preceding contact (RWB-S8-E7009-APP); the case of record, its route state, its contact hold and its timers (rwb-case P3); the interaction ledger and its contact values (rwb-source-data P1); the DEV rule rows and their versions (rwb-decision P7); the rights and the lists of values (rwb-access P4); and the schema, migration and deployment of this service (the DB, INF and OPS stories of this key).

### 2. Business rationale

The objective, the problem and the metric are the module's and do not move: complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events were handled case by case with no clock, and the metric is the deviations closed within the service level, targeted as set with DL22, measured on the decision log and the Workbench records and reviewed monthly (FSD S8 A2.19.1). The requirement is REQ-DVH-011, "The full deviation flows with their approvers, contact stops and return points run end to end", with REQ-DVH-004 for the stops it depends on (Program BRD v4; FSD S8 Requirements served).

A contact stop is only worth the paper it is written on if a message that goes out against it is caught, attributed and clocked. Epic 2 already blocks the send (FEAT-OCC-06, rwb-comms, "Stops the send, records the reason and leaves the message unsent when a stop applies"), so what is missing is the Workbench side of a stop that did not hold. What D-RCV-60 changes is who owns each fact of that breach:

- **The contact is a ledger fact of rwb-source-data.** The interaction ledger is one entry per contact, letter, promise, payment or hand-over, and R3 gives it to rwb-source-data by default ruling (DP-18), with `channel`, `direction`, `occurred_at`, `conduct_check` and `delivery_status` on it (LDM v8 `interaction`, DF-INT-004, DF-INT-005, DF-INT-006, DF-INT-012, DF-INT-028). This service reads it on the owner's contract and never as a table (ASM-5218).
- **The stop is a deviation fact of this service.** `contact_stop` is a column of `deviation` (DF-CAS-043), set true for X1 to X3 by R-DEV-01 and R-UNI-04 to R-UNI-06, so this service is the only one that can say whether a stop was in force at the instant of the contact (ASM-5220).
- **The breach is a decision, so it is recorded.** Legacy AC1 asks for the result in the decision log with the rule version and legacy AC2 stops the action when the log cannot be written; R-UNI-39 says the same in the rules ("Block the action and raise an incident. No action proceeds unlogged"). The record is written through the local library in one transaction, before anything else (DP-03).
- **The case does not move and neither does its clock.** A breach is a conduct fact on a case that a deviation has already paused; R-UNI-30 keeps the case still when a service level is breached and the one-clock rule of R-DEV-01 keeps the prescription clock running. This step therefore adds a handler and a clock and answers the parent with no clock change (ASM-5220).
- **The clock is a rule fact, not a constant.** R-DEV-20's timer column carries 10 working days and FSD S8 A2.19.1 sets the target with DL22, so the length is read from the rule row or the reference data at its version and never written in code (ASM-5221).

No business value moves: the deviation codes, the conduct-check values, the service level and the escalation point stay rule rows or reference data read with their version.

### 3. Preconditions

- RWB-S8-E7010-CON is published and tagged: the breach-entry element, the consumed ledger row, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-08 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The interaction-ledger read of rwb-source-data is published with its fake: the outbound contacts of a case with their channel, their sent-at instant, their `conduct_check` and their `delivery_status`. Its operation name is Not specified in the source documents (GAP-3070; ASM-5218).
- `deviation` exists in `rwb_deviation` from the DB story of this service with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0; at least one row of the case carries `contact_stop` true from the X1 to X3 stories (DF-CAS-043).
- The DEV package and the UNIVERSAL package are in force at their versions, with R-DEV-20 among the 22 DEV rules over 9 states and R-UNI-39 and R-UNI-30 in the 50 universal rules; they are authored, tested and approved in rwb-decision (P7) and loaded here (TSD S8 T4; Business Rules and Routing Logic v4; ASM-5222).
- The rwb-case workflow boundary is available for the fake: the case reference, its route state and the open deviation arrive as child-workflow input, and the outcome is the child result the parent applies. No source publishes a REST operation that moves a case state on behalf of a stage (context pack Temporal slides 5 and 13; ASM-5220).
- The lists of values this step reads — `LOV-CONDUCT` with PASSED, BLOCKED and NOT_APPLICABLE, `LOV-CHANNEL`, `LOV-DIRECTION` and `LOV-SEND-STATUS` — are reference data with their version, read on the owner's contract and never written in code (LDM v8; ASM-5224).
- The service runs as its own login on `rwb_deviation` and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, on `rwb_source_data.interaction` or on a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S8-E7010-CON when its tests pass.

### 4. Flow

1. A message goes out on a case that carries an open deviation with `contact_stop` true. The block of FEAT-OCC-06 did not hold, and the contact is one entry of the interaction ledger with `direction` outbound and a `conduct_check` that is not PASSED (LDM v8 DF-INT-006, DF-INT-012).
2. The case router of rwb-case signals the case's `DeviationWorkflow` on queue `rwb-deviation`; the signal carries the case reference and the interaction reference. No REST call is made and no table is read on the request path (context pack connection matrix row P3 to S8; ASM-5220).
3. The `contactBreach` branch starts: `readBreachFacts` reads the outbound contact from the interaction ledger of rwb-source-data, one hop and 2 s, and the open deviations of the case from `rwb_deviation` (ASM-5218, ASM-5220).
4. The branch pairs the contact with the deviation whose `contact_stop` is true and whose `raised_at` is before the contact's `occurred_at`. Where more than one deviation qualifies, the earliest open one is used and the pairing is recorded (ASM-5220).
5. `evaluateBreachRules` loads the package versions in force and evaluates the conduct-check condition of the ledger against the stop, R-UNI-39 for the record-first rule and R-DEV-20 for the clock. No rule row of either package names a contact sent while a block is on, so the breach is recorded against the two rule IDs and the condition that fired (ASM-5222).
6. `recordAndApplyBreach` writes one breach entry through the local library **before any other effect**: the case reference, the deviation reference, the interaction reference, the channel, the sent-at instant, the rule IDs with their package versions, the handler and the clock start. A failed write stops the step with nothing changed and MSG-P7-003 (DP-03; legacy AC1 and AC2).
7. The handler is the Conduct and QA officer (FSD S8 A2.19.3.3) and the clock is the deviation service level of R-DEV-20's timer column; the escalation point on breach is the team manager, who is the rule's owner column (ASM-5221).
8. The contact stop stays in force. This story never lifts it: R-UNI-44's lift is the conduct officer's separate act and belongs to the case and its route, not to the breach path.
9. The branch answers the parent: the breach reference, the deviation reference, the rule IDs with their versions and `NO_CLOCK_CHANGE`. rwb-case records the breach against the open deviation and leaves the case, its clocks and its `timer` rows as they are (ASM-5220).
10. Beyond the service level the durable timer of the branch fires: R-DEV-20 escalates to the team manager and reports the breach, and the case still does not move (R-UNI-30).
11. The conduct and QA officer reads the breach on SCR-08 through the composite route, read only, with its handler, its clock and its entry (DP-19; ASM-5223).
12. A repeated signal for the same interaction is idempotent: one entry per interaction reference, and a repeat answers the entry it already wrote without writing or escalating again.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no breach entry, no handler, no clock, no answer to the parent, and the case is untouched | MSG-P7-003 | AC2, TC-E7-010-02, TC-E7-010-04 |
| X2 | The role does not hold the Case record right of the act | 403 before any read of the ledger and before any record; the unattended branch runs under the service identity with the same check | MSG-P4-002 | AC4, TC-E7-010-03, TC-E7-010-06 |
| X3 | A required value is absent or invalid: no deviation reference, no interaction reference, no channel or no sent-at | The branch refuses the breach, writes nothing and names the field | MSG-GEN-001 (VR-S8-019-1) | AC1 |
| X4 | The outbound contact does not answer inside 2 s, or its breaker is open | The breach is not opened, the branch retries on the workflow's own schedule and nothing is written; the caller sees the platform 503 envelope | None (platform envelope) | AC1 |
| X5 | No open deviation of the case carries `contact_stop` true, or the contact is not outbound | No breach: the branch ends and records that no stop was in force at the instant of the contact | None | AC1 |
| X6 | The contact's `conduct_check` is PASSED, or the `delivery_status` shows the message was not sent | FEAT-OCC-06 held, so no breach path opens and nothing is written | None | AC1 |
| X7 | The same interaction is signalled twice | One entry per interaction reference; the repeat answers the entry it already wrote and counts the repeat | None | AC1, AC3, TC-E7-010-05 |
| X8 | The package has no version in force for R-DEV-20 or R-UNI-39 | The branch waits, the breach is not opened and the case is unchanged; no clock is taken on an unversioned service level | None | AC1 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `rwb_source_data.interaction` row, a `rwb_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5, TC-E7-010-07, Section 17, BR5, BR6 |

X1 and X2 are the legacy not-recorded and access paths of this key carried onto the slice; X3 to X8 are the paths the ledger read, the stop and the target call types add; X9 is the schema and ACE boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S8-E7010-CON, the decision-record stub, the interaction-ledger fake, the case-workflow fake and the gateway-bff fake, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity names, the pairing rule between contact and deviation and the shape of the breach entry are this story's choice; the rules, the messages, the screens, the clock source and the handler are fixed |
| Valuable | A message that goes out against a stop is caught, attributed to its deviation, given a handler and a clock and recorded once with the rule version it was judged under |
| Estimable | One workflow branch, three activities, one record write, one durable timer, two clients and one read-only screen slice |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on a synthetic case through the contract fakes, plus the no-stop, the passed-check, the refused-right, the repeat and the forced record-write failure |

### 7. Acceptance criteria

```gherkin
Feature: Handle a contact sent while a block is on

  Background:
    Given the DEV and UNIVERSAL rule packages are in force at their versions and carry R-DEV-20, R-UNI-30 and R-UNI-39
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Handle a contact sent while a block is on (legacy RWB-E7-010 AC1)
    Given the rwb-source-data contract mock returns the outbound contact "INT-2026-000901" of case "RW-2026-000710" on channel "SMS" at "2026-12-11T09:30:00Z" with conduct_check "BLOCKED"
    Given the rwb-deviation contract mock returns deviation "DEV-2026-000710" of code "X1" on case "RW-2026-000710" with contact_stop true and state "DEV_WITH_OWNER"
    Given the rwb-decision contract mock returns the DEV and UNIVERSAL packages at their versions in force with R-DEV-20 and R-UNI-39
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the breach path when a message goes out against a contact stop
    Then the system writes the result to the local decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E7-010 AC2)
    Given the local decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The same interaction signalled twice writes one entry (new, D-RCV-60)
    Given the idempotency key of the interaction "INT-2026-000901" already answers an entry of the breach
    When the same interaction is signalled a second time
    Then the repeat answers the entry it already wrote and counts the repeat

  Scenario: AC4 A role without the Case record right is refused before any read (new, D-RCV-60)
    Given the role does not hold the Case record right of the act
    When the breach act is taken on a contact that went out against a stop
    Then the system answers 403 with MSG-P4-002 before any read of the ledger and before any record is written

  Scenario: AC5 A statement outside rwb_deviation or a read of ACE data is refused and fails the build (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view or another service's schema
    When the boundary test runs
    Then the grant refuses the statement and the build fails

  Scenario: AC6 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change that the model does not allow is requested on the breach
    When the breach act is taken
    Then the system refuses the change and writes nothing

  Scenario: AC7 No person name, contact value, address or identity number enters the breach record (new, D-RCV-60)
    Given a breach is recorded for the interaction INT-2026-000901
    When the entry, the log, a workflow input or an event is written
    Then none of them holds a person name, contact value, address or identity number

  Scenario: AC8 A contact that does not answer inside 2 s is retried and nothing is written (new, D-RCV-60)
    Given the outbound contact does not answer inside 2 s
    When the breach branch runs
    Then the breach is not opened, the branch retries on the workflow's own schedule and nothing is written

  Scenario: AC9 A consumed call that fails writes nothing and answers the 503 envelope (new, D-RCV-60)
    Given the breaker of the outbound contact is open
    When the breach branch runs
    Then nothing is written and the caller sees the platform 503 envelope
```

AC3 to AC9 are new under D-RCV-60, and AC3, AC4 and AC5 cover X7, X2 and X9. The two criteria are the legacy criteria of RWB-E7-010 with their origin tag added and the decision-log line reworded to the local decision record of DP-03; otherwise the repeated `Then`, the wording of `the user acts on the screen`, `opens the breach path when a message goes out against a contact stop` and `the local decision record cannot be written` all stand. AC1's cross-service parts are mocked, so it carries the three `Given the <service> contract mock returns <x>` lines, and those are the only additions; AC2 has no cross-service part and is copied with nothing added. On this story "the action" is the breach act on a contact that went out against a stop, and "the screen" is the breach slice of SCR-08 behind the composite route. What the legacy lines describe now happens in three places: rwb-source-data holds the contact, rwb-deviation holds the stop and writes the entry, and rwb-decision holds the packages and the central ledger. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_deviation`, with the `decision_log_entry` ledger of rwb-decision behind it. The case number, the deviation reference and the interaction reference in the mock lines are synthetic test data and no source value (section 16).

### 8. Business rules

| Rule | BR ID | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-DEV-01 | BR2 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | Workbench, the Workbench document hub | same day |
| R-DEV-20 | BR7 | Deviations | X1 to X7 | DEV_WITH_OWNER | SLA_BREACHED | time in DEV_WITH_OWNER exceeds the deviation service level | Escalate to the team manager and report the breach | DEV_WITH_OWNER | Team manager | Workbench | 10 working days |
| R-UNI-10 | BR4 | Universal rules | All | ANY_ACTIVE | CONSENT_WITHDRAWN | the customer withdraws consent for a channel | Remove that channel from the contact plan, keep the statutory notices | HELD_CONDUCT | Conduct and QA officer | Workbench | same day |
| R-UNI-30 | BR4 | Universal rules | All | ANY_ACTIVE | SLA_BREACHED | time in the current state exceeds the service level | Raise the breach to the named escalation point. The case does not move | ESCALATED | Team manager | Workbench | per state |
| R-UNI-39 | BR1 | Universal rules | All | ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | the decision log entry cannot be written | Block the action and raise an incident. No action proceeds unlogged | EXCEPTION_QUEUE | Platform team | Workbench | immediate |
| R-UNI-44 | Not specified in the source documents (DOR-RWB-S8-E7010-APP-4) | Universal rules | All | HELD_CONDUCT | CONTACT_STOP_LIFTED | the conduct officer lifts the stop | Resume contact on the permitted channels | RESUME_STATE | Conduct and QA officer | Workbench | None |

The six rows are the rows of the Business Rules and Routing Logic v4, copied character for character, with the BR ID column added here. No rule row names a contact sent against a stop, so the story evaluates R-UNI-39 and R-DEV-20 and invents no ID (GAP-3070). This story evaluates R-UNI-39 for the record-first rule and R-DEV-20 for its clock; it reads R-DEV-01 as the rule that set the stop it tests, reads R-UNI-30 and R-UNI-10 as the case rules that keep the case still, and never fires R-UNI-44, because lifting a stop is a separate act. Their owner column names a business role and a system, not a service: "Workbench" is this service and its stage, and the "Workbench document hub" is rwb-document (P5).

| ID | Rule | Source |
|---|---|---|
| BR1 | The breach is a decision first: one entry per breach is written through the local library, with the deviation, the interaction, the channel, the sent-at instant, the rule IDs and the package versions, and a failed write changes nothing and answers MSG-P7-003 | DP-03; TSD S8 T2; R-UNI-39; legacy AC1 and AC2 |
| BR2 | The stop is this service's and the contact is not: `deviation.contact_stop` (DF-CAS-043) decides whether a stop was in force, and the contact arrives on the interaction-ledger contract of rwb-source-data with `direction`, `occurred_at`, `channel` and `conduct_check` | Context pack ownership rows; LDM v8 DF-CAS-043, DF-INT-004 to DF-INT-012; R3 default ruling; DP-18 |
| BR3 | A breach opens only where an outbound contact exists, its `conduct_check` is not PASSED and an open deviation of the same case carries `contact_stop` true with a `raised_at` before the contact | FSD S8 A2.19.2; LDM v8 LOV-CONDUCT (PASSED, BLOCKED, NOT_APPLICABLE); REQ-DVH-004 |
| BR4 | The case does not move and no clock changes: `recovery_case`, its route state, its contact hold and its `timer` rows are rwb-case's, and the answer to the parent is `NO_CLOCK_CHANGE` | R-UNI-30; Architecture v5 slides 8 and 13; ASM-5220 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_deviation`; `case_id` and the deviation and interaction references are identifiers of other services' facts | DP-01; TSD S8 T3.3 |
| BR6 | ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and no contact value, number or address reaches it — only the ledger entry and its identifiers | DP-05, DP-11; TSD S8 T5.2 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: the service level of the clock, the escalation point, the conduct-check list and the package versions | FSD S8 BR-S8-019; legacy Guardrails |
| BR8 | The breach is idempotent per interaction reference: one entry, one clock and one escalation, and a repeat answers the entry that exists | TSD S8 T-A.2; Architecture v5 slide 11 |
| BR9 | No person name, contact value, address or identity number enters `rwb_deviation`, the entry, a log, a workflow input or an event; the interaction reference and the channel are not personal data | Template and Rules §R7.2 (s17); LDM v8 (contact values masked) |

| BR | Covered by |
|---|---|
| BR1 | AC1, AC2 |
| BR2 | AC1 |
| BR3 | AC1 |
| BR4 | AC1 |
| BR5 | AC5 |
| BR6 | AC5 |
| BR7 | AC1 |
| BR8 | AC3 |
| BR9 | AC7 |

### 9. State transitions

The case route state and the `deviation.state` of the 9-state DEVIATION machine are not moved by this story: the breach is carried on its own entry, and the deviation that holds the stop stays where its own flow put it (BR4, ASM-5219). What this story owns is the breach path and its record.

| From (`deviation.state`, read) | The breach act | Condition | What this story writes |
|---|---|---|---|
| `DEV_WITH_OWNER` | A contact goes out against the stop | `contact_stop` true, outbound, `conduct_check` not PASSED, `raised_at` before `occurred_at` | One breach entry, its handler and its clock; the deviation row is unchanged |
| `DEV_FLAGGED` | A contact goes out against the stop | The stop was set by R-DEV-01 and the owner assignment has not run yet | One breach entry, and the pairing is recorded against the flagged deviation |
| `DEV_RESOLVED` | A contact goes out after the outcome | `contact_stop` still true at the instant of the contact | One breach entry, because the stop was in force when the message left |
| Any | A contact with `conduct_check` PASSED | FEAT-OCC-06 held | Nothing; the branch ends |
| Any | No open deviation with the stop, or an inbound contact | No stop in force | Nothing; the branch ends and records the reason |
| Any | The same interaction signalled twice | The entry exists | Nothing written; the existing entry is answered |

| Breach path step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A contact-breach signal arrives for the case | The package versions are read | Reading |
| Reading | The ledger and the deviation are read | A stop was in force at the instant of the contact | Evaluating |
| Reading | No stop, or a passed check | X5, X6 | Closed, nothing written |
| Evaluating | R-UNI-39 and the conduct condition hold | The clock is taken from R-DEV-20 | Recording |
| Recording | The entry is written | The transaction commits | Clocked |
| Recording | The entry write fails | X1 | Waiting, nothing changed, MSG-P7-003 |
| Clocked | The durable timer fires | The service level has run | Escalated to the team manager; the case does not move |

The breach states are the entry's own and no state value of the DEVIATION machine or of the case is added by this story (ASM-5219, ASM-5220).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Conduct and QA officer (RW-CONDUCT) | The primary actor of FSD S8 A2.19.3.3: holds the breach, its handler and its clock, and reads SCR-08. TSD S8 T6.1 gives this role R on Case record only, so the write right is the conflict of AC2 and of section 17 (GAP-3070; ASM-5224) |
| Case owner (RW-CASEOWN) | Case record CRUA: the role that holds the write right under the matrix and takes the act where the conduct officer only reads |
| Complaint officer (RW-COMPLAIN), hardship and vulnerability specialist (RW-SPECIAL) | Case record RU: hold the deviation whose stop the breach tests (R-DEV-02, R-DEV-03) |
| Team manager (RW-TEAMMGR) | Case record R: receives the escalation and the breach report of R-DEV-20 |
| Compliance and PDPA officer (RW-COMPLY) | Case record R: the "also uses" role of FSD S8 A2.19.3.3 |
| Platform team (R-UNI-39, owner column) | Receives the incident when the record cannot be written; no case right is used for it |
| rwb-case (P3) | Owns the case of record, its route state, its contact hold and its timers, and applies the stage answer this story returns |
| rwb-source-data (P1) | Owns the interaction ledger and the contact values behind it; this story reads the entry, never a contact point |
| rwb-decision (P7) | Owns the DEV and UNIVERSAL packages, their rule rows and the central ledger; this story evaluates them and records locally |
| rwb-access (P4) | Owns the roles, the capability rights and the lists of values this story reads through the guard |

No delegated authority limit applies: a breach takes no credit decision and approves nothing, and the only approval in the module is the insurance claim of X3, which is not this story's.

### 11. Data

| BR Field ID | Entity | Owner | Use in this story |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` | S8, `rwb_deviation` | **Read** only: `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at`, `outcome` and `state`. No column of it carries the breach, its handler or its clock, so this story writes none of them (ASM-5219) |
| None: library table | `decision_record` | Platform library in `rwb_deviation` | **Write**: one hash-linked breach entry per breach, before anything else (DP-03) |
| None: library table | `idempotency_key`, `outbox_event` | Platform library in `rwb_deviation` | The interaction key and the answer it holds; the outbox object exists as a library row and this step writes no event row to it (§12.3) |
| DF-INT-001, DF-INT-002, DF-INT-004 to DF-INT-006, DF-INT-012, DF-INT-028 | `interaction` | P1 rwb-source-data | Not read as a table: the outbound contact arrives on the owner's contract with its case, its sent-at instant, its channel, its direction, its conduct check and its delivery state (ASM-5218) |
| DF-WRK-027 to DF-WRK-036 | `timer` | P3 rwb-case | Not read as a table and not written: the clocks are rwb-case's and this story changes none of them (ASM-5220) |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | Not written: the local entry is copied to the central ledger by its owner, and its identifier is not stored here |
| DF-REF-001 to DF-REF-015 | `rule_row` | P7 rwb-decision | Not read as a table: the two packages arrive loaded at their versions in force (ASM-5222) |
| `LOV-CONDUCT`, `LOV-CHANNEL`, `LOV-DIRECTION`, `LOV-SEND-STATUS` | reference data and lists of values | P3 rwb-case (default ruling) | Read at their version; `LOV-CONDUCT` carries PASSED, BLOCKED and NOT_APPLICABLE and the condition of BR3 tests it (ASM-5224) |

No new table, no new column and no migration: the table arrives with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_deviation` by the library's own migration (DP-03).

Entity groups the FSD requires of rwb-deviation, stated as product requirements and not as physical tables: the breach entry of this story, a shadow screening run with its mode, a score row per code with precision, recall and sample size, a contact stop that stays in force until it is lifted, an agent feedback row, and a breach record for a contact sent against a stop. Physical tables are set by the Ownership Map (GAP-1819).

**No personal data.** The entry carries identifiers, a channel code, an instant, a rule version and a state. No name, address, contact value or identity number enters `rwb_deviation`, the entry, a log or a workflow input; the ledger keeps the contact point masked and only its entry identifier reaches this service (BR9).

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). The two operations of the service are other stories' of the same service: `POST /cases/{caseId}/deviations` (API-S8-001, Case record U) and `PATCH /deviations/{deviationId}` (API-S8-002, Case record U) belong to RWB-S8-E7001-APP, and the Ownership Map gives S8 no third operation. The breach act therefore arrives as a signal on the running workflow, and the read of the breach state behind SCR-08 is Not specified in the source documents and carries the placeholder (GAP-3070; ASM-5223). A build that declares a breach operation here fails the absence test of RWB-S8-E7010-CON.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of the outbound contacts of a case from the interaction ledger; operation name Not specified in the source documents (GAP-3070; ASM-5218) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The contact the breach tests: its reference, case, `occurred_at`, `channel`, `direction`, `conduct_check` and `delivery_status` (DF-INT-001, -002, -004 to -006, -012, -028); read only, faked |

The row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020, DP-11). It is a contract dependency of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3070; ASM-5218). No ACE view or ACE table is read by this story; the boundary test fails the build on a view read or an ACE table read (GAP-1816).

#### 12.3 Events published

None. The service publishes on `rwb.deviation.events.v1` and its event set is `DeviationRaised` (`rwb.deviation.DeviationRaised.v1`, EV-06) and `DeviationCleared` (`rwb.deviation.DeviationCleared.v1`, EV-07), both of which belong to the raise and the resolution of a deviation and therefore to RWB-S8-E7001-APP (Event and Messaging Design v5 EV-06 and EV-07; TSD S8 T5.3). A breach raises no deviation and clears none — the deviation that holds the stop was raised when the stop was applied — so this story declares no producer group, no envelope and no outbox row, and RWB-S8-E7010-CON fails a build that adds one (ASM-5223).

#### 12.4 Events consumed

None. The service listens to the rwb-case case events on the router row of the connection matrix (context pack, row S8: an event subscription to P3), and that subscription belongs to the case alignment of the deviation stories. The breach arrives as a signal on the running child workflow from the case router, which is Temporal on the parent-and-child boundary and not a Kafka subscription of its own (ASM-5220). The service consumes no rwb-comms event: the matrix gives S8 no row to P6, which is the reason the contact is read on the ledger and not received as an event (GAP-3070; ASM-5218).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, started at any time, child of `CaseWorkflow`, parent close policy ABANDON, continues-as-new | `rwb-deviation` | Hosts the `contactBreach` branch; its input is the case reference and the interaction reference, and its outcome is the stage answer |
| `contactBreach` | Branch of `DeviationWorkflow` (not a separate catalogued workflow) | `rwb-deviation` | The path from the contact-breach signal to the entry, the handler, the clock and the answer |
| `readBreachFacts` | Activity | `rwb-deviation` | The ledger read and the deviation read; the pairing of contact and stop out |
| `evaluateBreachRules` | Activity | `rwb-deviation` | The packages in force in; the rule IDs, their versions and the condition that fired out |
| `recordAndApplyBreach` | Activity | `rwb-deviation` | The entry, the handler, the clock start and the stage answer out, one transaction |
| `breachClock` | Durable timer of the branch, the wait of R-DEV-20 | `rwb-deviation` | The service level of the rule row with its version; the expiry is the escalation |

The stage answer carries the case reference, the deviation reference, the breach reference, the rule IDs with their versions and `NO_CLOCK_CHANGE`. The activity and branch names are a target design choice fixed by no source document, and no child workflow of this service is created.

Open question (GAP-1818): the three sources name the raise, clear and read paths differently. This story fixes only POST /cases/{caseId}/deviations, PATCH /deviations/{deviationId} and the clear operation. The synchronous read of the case-record deviation query is left open, with its owner Not specified in the source documents (GAP-1818), and is to be settled in RWB-S8-E7010-CON before the screen is built.

Workflow ID form and start rule of `DeviationWorkflow` (CG-ALL-11684): the workflow ID form is Not specified in the source documents (CG-ALL-11684), and the start or signalWithStart choice and the duplicate-start policy are Not specified in the source documents (CG-ALL-11684).

#### 12.6 Schedules

None. The Ownership Map gives S8 no job (context pack ownership rows, Jobs: 0), and FSD S8 A2.19.4.4 declares no background event for this feature. The breach clock is a durable Temporal timer inside the branch, not a Schedule, not a Quartz row and not a shared job table; DP-10 is not in this key's pattern set (ASM-5221).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | The deviation of the case, its code, its raise facts, its handler, its `contact_stop` and its state; this story reads it and writes no column of it |
| `decision_record` | Platform library in `rwb_deviation` | The local hash-linked breach entry (DP-03) |
| `idempotency_key` | Platform library in `rwb_deviation` | The key of the repeated signal and the answer it holds |
| `outbox_event` | Platform library in `rwb_deviation` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case`, `queue`, `assignment` and `timer` (P3), `interaction` and every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `rule_row` and `decision_log_entry` (P7). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data interaction-ledger fake | An outbound SMS contact of case `RW-2026-000710` at `2026-12-11T09:30:00Z` with `conduct_check` BLOCKED and `delivery_status` sent; the same contact with `conduct_check` PASSED; an inbound contact; no answer inside 2 s; the operation name carries the placeholder (GAP-3070; ASM-5218) | AC1, X4, X6 |
| rwb-deviation deviation fake | The deviation `DEV-2026-000710` of code X1 with `contact_stop` true at `DEV_WITH_OWNER`, the same at `DEV_FLAGGED` and at `DEV_RESOLVED`, and a deviation with `contact_stop` false | AC1, X5 |
| rwb-decision package fake | The DEV package at its version in force with R-DEV-20 and the UNIVERSAL package with R-UNI-30 and R-UNI-39; a package with no version in force | AC1, X8 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC1, AC2, X1 |
| rwb-case workflow fake | The case at `WITH_FCR_OFFICER` with its open deviation, an accepted `NO_CLOCK_CHANGE` answer, and a refused answer | AC1, X7 |
| gateway-bff composite route fake | The merged SCR-08 answer for the case, with the breach slice of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The ledger operation name is a placeholder until rwb-source-data publishes it (GAP-3070; ASM-5218).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 1 consumed | The read of the outbound contacts of the case from rwb-source-data; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-06 and EV-07 belong to RWB-S8-E7001-APP; the decision record rides the library's shared `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 3 activities and 1 durable timer | `DeviationWorkflow` and its `contactBreach` branch on `rwb-deviation`, with `readBreachFacts`, `evaluateBreachRules`, `recordAndApplyBreach` and the breach clock; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.deviation`, module `breach`; front end `src/modules/recovery/deviation/DeviationBreach.tsx`, the SCR-08 fragment this story answers, read only.

**Pattern application** (§R5.5)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the entry commits before the handler and the clock, and a failed write leaves nothing behind. DP-13 fixes the base of the service and gives the breach no element of its own, because its two operations belong to RWB-S8-E7001-APP. DP-19 is how the SCR-08 breach slice reaches this service, one hop through the gateway. Two patterns the plan does not carry are real dependencies here and are recorded rather than added: DP-18, the interaction ledger of rwb-source-data (ASM-5218), and DP-07, the lists of values read from their owner at a version (ASM-5224). DP-09 is absent and rightly so, because this step publishes nothing (ASM-5223).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationWorkflow` breach branch | Workflow | Receives the contact-breach signal, hosts the clock, applies the idempotency key and reports the answer to the parent |
| `readBreachFacts` | Activity | Reads the ledger entry and the open deviation, pairs them by case and by time, and refuses the breach where no stop was in force |
| `evaluateBreachRules` | Activity | Evaluates R-UNI-39 and the conduct-check condition, takes the clock from R-DEV-20 and returns the rule IDs with their versions |
| `recordAndApplyBreach` | Activity | Writes the breach entry and its idempotency row in one transaction and returns the handler, the clock and the answer |
| `BreachEntryWriter` | Library adapter | Writes the hash-linked entry before any other effect and refuses the step when the write fails |
| `InteractionClient` | Client | The ledger read of rwb-source-data, one hop, 2 s, breaker, no retry of its own |
| `DeviationReader` | Repository | The open deviations of the case and their `contact_stop`, read on this schema |
| `BreachClock` | Durable timer | The service level of R-DEV-20 with its version, and the escalation of R-UNI-30 |
| `DeviationBreach` | React component | Shows the breach, its handler and its clock on SCR-08, read only |

**Database and migrations.** No Flyway file. `deviation` arrives with the DB story of this service, and `decision_record`, `idempotency_key` and `outbox_event` are library objects created in `rwb_deviation` by the library's migration (DP-03). No column is added for the breach, its handler or its clock, because no column of `deviation` carries them and the interaction stays with its owner (ASM-5219).

**Configuration and reference data.**

- The deviation service level of the clock and the escalation point: R-DEV-20's timer column and owner column, read from the package at its version (ASM-5221).
- Open decision DL22 sets the deviation service level and is still open; its assumptions are ASM-1162, ASM-1304, ASM-2217 and ASM-2569. The clock uses R-DEV-20's 10 working days until DL22 closes.
- `LOV-CONDUCT` and the conduct-check condition: reference data with their version, never a constant (ASM-5224).
- Parameters and reference data of this story are read through the owners' contracts under DP-06 and DP-07: the deviation service level, the escalation point, `LOV-CONDUCT`, `LOV-CHANNEL`, `LOV-DIRECTION` and `LOV-SEND-STATUS` (ASM-5221, ASM-5224).
- The capability area "Case record" and its rights: access rows of rwb-access, read through the guard (ASM-5224).
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The `contactBreach` branch and its input record on `rwb-deviation`, registered as a branch of the stage child of `CaseWorkflow`, with the signal, the idempotency key and the durable timer.
2. `InteractionClient` against its fake, with the 2 s budget, the breaker and the unavailable path (AC1, X4).
3. `DeviationReader` and the pairing of contact and stop, with the no-stop and the inbound paths (AC1, X5, X6).
4. `evaluateBreachRules` over the two packages in force, with R-UNI-39, R-DEV-20 and the unversioned-package path (AC1, X8).
5. `BreachEntryWriter` against the stub, with the failed-write path and MSG-P7-003 (AC2, X1).
6. `recordAndApplyBreach` with the entry, the handler, the clock and the answer to the parent, and the repeat path (AC1, X7).
7. The read-only breach slice of `DeviationBreach` on SCR-08 through the composite route fake (AC1).
8. The boundary test: no statement outside `rwb_deviation`, no `v_ace_*` read, no read of the interaction ledger of rwb-source-data (P1) and no write to the case of rwb-case (P3) (X9, BR5, BR6).

**Feature flag.** `rwb.deviation.contact-breach-v1`, a flag of the platform library; off means the branch ends without an entry, the breach does not appear on SCR-08 and the X1 to X3 flows are unaffected.

**Done when.** The tests of section 16 pass, the branch opens a breach on a synthetic case in SIT, the entry carries its rule version, the clock escalates at the service level, a passed check and a case with no stop open nothing, a repeated signal writes once, a forced entry failure changes nothing, no ledger row of rwb-source-data (P1), no case row of rwb-case (P3) and no ACE view read exists in the build, and SCR-08 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | Carried from the legacy message set of RWB-E7-010: it confirms the raise of a deviation and the handler it went to, and is raised by RWB-S8-E7001-APP, not by this step | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required value of the breach is absent or invalid, for example no interaction reference or no channel (X3, VR-S8-019-1) | Enter {field}. |
| MSG-P4-002 | A role without the Case record right takes the act, or the conduct officer tries the write the matrix does not give the role (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The breach entry cannot be written before anything else (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set of this key; the text is the legacy and FSD S8 wording, copied unchanged, and no message is reworded and no new one is added. MSG-S8-001 is carried because the legacy table of RWB-E7-010 lists it. R-UNI-39's incident is raised by the platform on the same failure and is not a message of this service.

### 15. Screens and states

| Screen | States | What this story answers |
|---|---|---|
| SCR-08 Deviation queue | Loading; list; breach open; breach escalated; empty; error; no access: Not specified in the source documents (CG-ALL-11692; DOR-RWB-S8-E7010-APP-10) | The breach slice of the queue: the deviation it belongs to, the contact, the channel, the sent-at instant, the handler, the clock and the rule version, read only |
| SCR-06 Raise deviation | Form; saved; empty; loading; error; no access: Not specified in the source documents (CG-ALL-11691; DOR-RWB-S8-E7010-APP-10) | No part: the raise and its saved state belong to RWB-S8-E7001-APP, and a breach raises no deviation |

Both screens are the edge contract's (DP-19) and the composite route also calls rwb-case for the case, its owner and its timers; this story fixes only its own breach answer, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON (ASM-5223). The breach read itself is a placeholder, because no source publishes an operation for it (GAP-3070). The escalated, refused, not-recorded and unavailable states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-010-01 | AC1 | Component | The synthetic case `RW-2026-000710` with deviation `DEV-2026-000710` at `DEV_WITH_OWNER` and contact `INT-2026-000901` on SMS with `conduct_check` BLOCKED; one entry, the handler, the clock and `NO_CLOCK_CHANGE` asserted |
| TC-E7-010-02 | AC2 | Component | The decision-record stub stopped; no entry, no handler, no clock, no answer and MSG-P7-003 |
| TC-E7-010-03 | AC2, X2 | Component | A role without the Case record right, and the conduct officer's R right on the write; 403 with MSG-P4-002 and no ledger read |
| TC-E7-010-05 | AC3, X7 | Component | A repeated signal of one interaction writes no second entry; the repeat answers the entry it already wrote and counts the repeat |
| TC-E7-010-06 | AC4, X2 | Component | A role without the Case record right is refused with 403 and MSG-P4-002 before any ledger read or record |
| TC-E7-010-07 | AC5, X9 | Component | A statement outside rwb_deviation or a v_ace_* read is refused by the grant and fails the build |
| TC-E7-010-04 | AC2, X1 | Component | A forced decision-record write failure stops the action with MSG-P7-003 and leaves the case and its timers unchanged |
| TC-E7-010-12 | §12 | Component | Every operation, event and activity of section 12 run against the contract fakes of RWB-S8-E7010-CON; expected results Not specified in the source documents (DOR-RWB-S8-E7010-APP-12) |
| TC-E7-010-13 | §12.7 | Component | Boundary values of each table of section 12.7 under ASM-3438; the values are Not specified in the source documents (DOR-RWB-S8-E7010-APP-12) |
| TC-E7-010-08 | AC6 | Component | Not specified in the source documents (NEWAC-RWB-S8-E7010-APP-AC10) |
| TC-E7-010-09 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S8-E7010-APP-AC7) |
| TC-E7-010-10 | AC8, X4 | Component | Not specified in the source documents (NEWAC-RWB-S8-E7010-APP-AC8) |
| TC-E7-010-11 | AC9, X4 | Component | Not specified in the source documents (NEWAC-RWB-S8-E7010-APP-AC9) |

The first four IDs are the legacy cases of RWB-E7-010 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`, and the legacy level `System` maps to `Component` because the artefact under test is the branch against its contract fakes. The no-stop, the passed-check, the repeat and the unversioned-package paths are covered inside TC-E7-010-01 and by the new contract cases of RWB-S8-E7010-CON. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the service level of the clock, the escalation point, the conduct-check lists and the package versions stay rule rows or reference data read with their version.
- No personal data in `rwb_deviation`, in an entry, a workflow input, a log or a prompt: identifiers, a channel code, an instant, a rule version and a state only, and the ledger keeps the contact point masked.
- ACE data and the ledger only through the owner's contract: no `v_ace_*` view, no ACE table, no `interaction` row and no other service's schema (BR5, BR6).
- The case, its route state, its contact hold and its timers stay with rwb-case: this story writes no case row, no timer row and no case state (BR4).
- One base, one topic, one queue and one login per service; this story adds no second topic, no event and no Schedule (DP-13, DP-14).
- The record is written before the change and in its transaction; a failure leaves nothing behind (DP-03, R-UNI-39).
- The stop is never lifted here: lifting it is R-UNI-44's separate act on the case, and a breach build that lifts a stop fails the review.
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no `recovery_log` write and no data-lake path.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-DVH-011 | The full deviation flows with their approvers, contact stops and return points run end to end (Must, E7) | The breach path of a contact sent against a stop, its entry, its handler and its clock | TC-E7-010-01, TC-E7-010-02 |
| REQ-DVH-004 | Contact stops apply automatically for a dispute or complaint, a vulnerable or hardship case, and a deceased customer (Must, E2) | The `contact_stop` condition the breach tests, and the stop that stays in force | TC-E7-010-01 |
| ADR-013 | 19 services inside ACE | rwb-deviation as the owner of the deviation and the breach | TC-E7-010-01 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-E7-010-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed ledger row with its budget and breaker | TC-E7-010-01 |
| ADR-022 | Local decision record plus central ledger | The breach entry written before anything else | TC-E7-010-02, TC-E7-010-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-010, disposition Split (rework); feature FEAT-DVF-10 |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Source text | Legacy RWB-E7-010; FSD S8 Deviation handling v3 A2.19 and Requirements served; TSD S8 Deviation handling v2 T2, T3.0 to T3.3, T4, T5.2, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-DEV-01, R-DEV-20, R-UNI-10, R-UNI-30, R-UNI-39 and R-UNI-44; LDM and Data Dictionary v8 `deviation`, `interaction` and `LOV-CONDUCT`; Event and Messaging Design v5 EV-06 and EV-07; Program BRD v4 REQ-DVH-004 and REQ-DVH-011 |
| Test cases | TC-E7-010-01 to TC-E7-010-04 |
| Feature and screens | FEAT-DVF-10, SCR-08 Deviation queue and SCR-06 Raise deviation |
| Rules | R-DEV-20 and R-UNI-39 evaluated; R-DEV-01, R-UNI-10, R-UNI-30 and R-UNI-44 read |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes, the breach-entry element, the consumed ledger row, the rights, the error set and the fakes: RWB-S8-E7010-CON.
- The raise of a deviation, its outcome and the two operations of this service: RWB-S8-E7001-APP and the X1 to X7 stories.
- The matching of a complaint to the preceding contact: RWB-S8-E7009-APP.
- The block of an outbound contact when a stop is in force and the conduct check before every send: FEAT-OCC-06 and FEAT-OCC-05, rwb-comms (P6), built in Epic 2.
- The lift of a contact stop and the return of the case to its paused state: R-UNI-44 and the deviation resolution stories, with rwb-case.
- The case of record, its route state, its contact hold and its `timer` rows: rwb-case (P3); the interaction ledger and the contact values: rwb-source-data (P1).
- The DEV and UNIVERSAL packages, their rule rows and the central ledger: rwb-decision (P7); the roles, the capability rights and the lists of values: rwb-access (P4).
- The partner conduct breach of R-UNI-29 and the partner review forum: S9 rwb-partner and the partner stories.
- The gateway-bff composite route and the screen field list of SCR-08: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
