# RWB-S8-E2012-APP Manual transfer and reassignment screen with reason

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E2012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-S8-G |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2012-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to REQ-WKM-003, REQ-WKM-007, REQ-WKM-008, REQ-CWC-010, REQ-CWC-016) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the deviation side of RWB-E2-012 is split out onto rwb-deviation (S8). The transfer itself, its endpoint, its reason-code and cap checks, the assignment swap and the `CaseTransferred` publication stay with the primary slice in rwb-case (RWB-P3-E2012-APP); this story owns the open-deviation answer the move and the SCR-05 panel read, the deviation panel itself behind the gateway-bff composite route, the decision record written against the deviation when the case moves, and the handler rule R-DEV-02 and R-DEV-03 keep. The read is published on `/api/recovery/deviation/v1` (DP-13) and the service's two events on `rwb.deviation.events.v1` (DP-09, DP-14); `deviation` is the only table this service writes (DP-01). The plan's build list is empty although the DP table adds platform contract rows, the read operation of the P3 slice is not a row of the Ownership Map, and the fifteen legacy test case ids are carried by both slices (GAP-3091, -3, -8; ASM-5280, -3, -8). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S8-E2012-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **the transfer screen to show the open deviation of the case, with the rule that refuses the move while it is open, and the deviation to keep the handler its own rule named after the case has moved**, so that **a hand-off is one action with a record and never silently takes a case away from the owner a deviation put on it**.

Inside `rwb-deviation` this is the deviation side of the manual move:

- Service `rwb-deviation`, schema `rwb_deviation`, REST base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with event names `rwb.deviation.<Event>.v1`, Temporal task queue `rwb-deviation` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.deviation` (context pack).
- The read `GET /api/recovery/deviation/v1/cases/{caseId}/deviations`, one call per case: the open deviations with their code, handler, paused state, contact stop, raised-at, return point and rule ID (DP-13). It is the answer the P3 move names in its own section 12 and the answer the SCR-05 deviation panel renders (GAP-3093; ASM-5282).
- The deviation panel of SCR-05 behind the gateway-bff composite route: what is open, who holds it, why the move is refused, and what happens to the panel after the move or the clear (DP-19).
- The `CaseTransferred` (EV-04) handler on task queue `rwb-deviation`: it records the move against the deviation and keeps the handler that R-DEV-02 and R-DEV-03 named, because BR10 says an open deviation holds the case with its own owner (DP-10).
- The local decision record of DP-03 for that step, hash-chained in `rwb_deviation` and published on `rwb.decision-record.v1`; a failed write leaves the deviation and the panel as they were.
- Inbox idempotency on the event ID and the outbox relay of `DeviationRaised` and `DeviationCleared` through the library of DP-09 (DP-09, DP-14).
- The transfer reason list `LOV-TRANSFER-REASON` read on the reference-data contract of rwb-case, with its version (DP-07), so R02 Customer deceased and R05 Legal referral are data and not code.
- The per-service Flyway sequence of `rwb_deviation` for this story's own need, with no shared `recovery` migration (DP-15).

It does not own: the transfer endpoint `POST /cases/{caseId}/transfer` and its reason-code, cap, team, hold, scope and version checks; the assignment swap; the `CaseTransferred` publication; and the queue and case screens beyond the deviation panel (the primary slice RWB-P3-E2012-APP in rwb-case). Nor the `recovery_case`, `queue`, `assignment` and `timer` tables (P3), the TRANSFER package rows, their authoring, approval and versions (rwb-decision, P7), the roles and rights (rwb-access, P4), or the contract surface with its OpenAPI and fakes (the CON stories of this service and of P3).

### 2. Business rationale

The legacy objective is unchanged: a case changes hands by one action, with a coded reason and a record, and a case that a deviation holds is not moved from the owner the deviation named (RWB-E2-012 §2, §8 BR10; REQ-WKM-003, REQ-WKM-007, REQ-CWC-010, REQ-CWC-016). Audit found debtors who met the criteria were not transferred to the responsible unit (CTL-03), and a refusal that shows only a rule ID is the same failure in another shape: the manager must see which deviation holds the case and who holds it.

D-RCV-60 changes who answers, not what the manager sees:

- **The refusal has two owners.** The TRANSFER row "TRF-010" refuses a move while a deviation is open, and the fact it reads is the deviation, which is this service's. rwb-case may not read `deviation` (DP-01) and names a one-hop read of this service instead, so the answer is published here and faked for the P3 build (DP-11; GAP-3093).
- **The panel is a composite, not a page.** SCR-05 was one ace-web screen; after the split gateway-bff composes it, and the deviation fragment is the part this service contributes, with its own states and messages (DP-19).
- **The owner stays with the deviation.** BR10 survives the split unchanged: an accepted move recorded against an open deviation keeps the handler R-DEV-02 or R-DEV-03 named, and the panel shows the case's new queue and owner beside it, so custody of the case and ownership of the deviation are never confused.
- **The record comes first.** The monolith writes the decision log before the case changes (TSD S8 T2); the local decision record of DP-03 keeps that order per service, and a failed write changes nothing.
- **No personal data anywhere.** The panel and the answer carry identifiers, codes and instants only: no name, address, identity number or contact value enters the read, the record, an event or a log (section 17).

Wave needs no conflict row here: business epic EP02 sits in wave 2 by the W-MAP and the service sits in wave 2 in Arch v5, so the two agree. Only the plan's empty build list and the platform rows of the DP table are recorded (GAP-3091; ASM-5280).

### 3. Preconditions

- `RWB-P3-E2012-CON` is published and tagged: the transfer operation, the `TransferRequest` and `Assignment` schemas, the reason list reference, the refusal codes, `CaseTransferred` and the fakes, including the deviation fake this story replaces (C dependency; DP-11).
- The platform contract stories the DP table names are published with their stubs: the local decision record and `rwb.decision-record.v1` (DP-03), the embedded Drools kit and the package reader (DP-04), the reference-data client (DP-07), the outbox, inbox and idempotency library (DP-09), the workflow kit (DP-10), the topic-naming library (DP-14), the per-service Flyway baseline (DP-15) and the gateway-bff composite route (DP-19). The plan carries no build dependency on this key, so the story starts on Day 1 against those baselines and the fakes; the rows are tracked, not blocking (GAP-3091; ASM-5280).
- `deviation` exists in `rwb_deviation` with DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0, created by the DB story of this service; this story adds no table and no column (GAP-3096; ASM-5285).
- Package TRANSFER version "TRF-2026.12" is in force on the business date, and row "TRF-010" refuses a move while a deviation is open; the rows are authored and approved in rwb-decision and never here (DP-04; legacy §3).
- `LOV-TRANSFER-REASON` is readable on the reference-data contract of rwb-case at its version, with R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue; the values are the legacy assumed set pending DL23 (GAP-3097; ASM-5286).
- The receive routes for `CaseTransferred` (EV-04) and for the case status and legal-hold changes exist on the service inbox; the last two carry no published event name and are faked (GAP-3095; ASM-5284).
- The person holds Case record R in rwb-access (RW-TEAMMGR, RW-CAPACITY, RW-CASEOWN and the deviation handlers hold RU or R, TSD S8 T6.1), the case is in their scope, and no delegation of authority level applies: a move changes who works the case, not what is owed.
- The login is the rwb-deviation login (DP-02): one login, one pool, grants on `rwb_deviation` only; a statement on `rwb_case` fails at the grant and in the boundary test (DP-01).

### 4. Flow

1. The team manager opens SCR-05 for one case of SCR-03, or for up to 50 cases selected on SCR-07, at business date 2026-12-15; gateway-bff composes the screen (DP-19).
2. The screen asks this service once per case: `GET /api/recovery/deviation/v1/cases/{caseId}/deviations`, one hop with a 2 s budget and a breaker (DP-11, DP-13).
3. The operation authorises the call through the rwb-access contract, right R on Case record, scope applied, and answers 401, 403 with MSG-P4-002, 404 and 503 in the platform envelope; a refused authorisation refuses the read and never widens it.
4. The repository selects the `deviation` rows of the case with `cleared_at` empty; a cleared row is history and is not part of the answer.
5. The answer carries, per open deviation: code X1 to X7, handler, paused state, contact stop, raised-at, return point, the rule ID that put it there (R-DEV-02 to R-DEV-06) and the package version; no personal field and no free text (section 17).
6. The screen renders the deviation panel: the codes, the handler of each, the paused state and the "Contact stopped" mark, with the refusal of the move as MSG-P3-033 naming the TRANSFER rule the case read returned, or MSG-P3-027 when no TRANSFER version is in force (legacy §15; MSG text in section 14).
7. With no open deviation the panel is empty and the form carries the reason list read on `LOV-TRANSFER-REASON` with its version (DP-07); the reason codes are rendered as data and never frozen into the client.
8. The manager confirms a target queue or owner, a reason code and a note; the front end sends one `POST /api/recovery/case/v1/cases/{caseId}/transfer` per case to rwb-case, which runs the move, the rule evaluation, the cap and team checks and the assignment swap (primary slice; C RWB-P3-E2012-CON).
9. On an accepted move rwb-case publishes `rwb.case.CaseTransferred.v1`; this service receives it on the inbox and starts the transfer branch of `DeviationWorkflow` on task queue `rwb-deviation` with the event ID as the workflow ID (DP-10).
10. `applyCaseTransfer`: the branch reads the open deviations of the case again and keeps the handler each row already holds, because R-DEV-02 and R-DEV-03 name the deviation owner and BR10 keeps the case with that owner; the panel shows the case's new queue and owner beside the unchanged handler (legacy BR10).
11. `recordDeviationMove`: in one `rwb_deviation` transaction and as the last step before commit, the decision record is written with the rule ID, the package version, the reason code, the from and to queue and owner and the event ID; the inbox row marks the event processed.
12. A repeated event ID is ignored as an idempotency hit, and the same `Idempotency-Key` on a raise or a clear answers the response it already gave (R-UNI-40). The deviation's own state, paused state, contact stop, raised-at and return point are never changed by a move.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case has an open deviation and the TRANSFER row "TRF-010" refuses the move | The panel names rule "TRF-010" and the code that holds the case; nothing changes in this service | MSG-P3-033 | AC1, AC4 |
| X2 | No TRANSFER version is in force on the business date | The panel names the package check and no fallback decision is shown | MSG-P3-027 | AC1 |
| X3 | No open deviation on the case | The panel is empty and the form is offered with the reason list at its version | None | AC2, AC6 |
| X4 | Two deviations are open on one case | Both rows are answered and the panel names both; the move is refused while either is open | MSG-P3-033 | AC4 |
| X5 | The deviation was cleared | The row is history and not part of the open answer; the panel shows it cleared with its outcome | None | AC6 |
| X6 | The rwb-access answer refuses the read | 403 before any row is read, and nothing changes | MSG-P4-002 | AC9 |
| X7 | The same `CaseTransferred` event ID arrives twice | Second ignored and counted; one record | None | AC7 |
| X8 | The decision record cannot be written | The transaction rolls back, the inbox row stays unprocessed and the panel is unchanged | MSG-P7-003 | AC8 |
| X9 | The case read, or the reference-data read, does not answer inside 2 s | The panel shows the case side without the deviation fragment and the move is never taken on an unread deviation | None | Section 17 |
| X10 | A statement, a test or a component reaches a `rwb_case` row or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17 |

X1, X3, X4, X5 and X7 restate the legacy exception rows X2 and the screen states of legacy §15 for this slice; X2 is legacy X11 and X8 is legacy X9. The legacy rows that belong to the move itself — no reason code (MSG-P3-001), the cap (MSG-P3-002), the team check R-UNI-18, the legal hold (MSG-P3-005), the parallel request (MSG-GEN-004) and the bulk summary (MSG-P3-035) — are answered by rwb-case and are not restated here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against `RWB-P3-E2012-CON` and its fake, the platform stubs of DP-03, DP-07, DP-09, DP-10 and DP-19, and synthetic `deviation` rows; no live P3, P4 or P7 is needed |
| Negotiable | The shape of the deviation answer, the panel layout and the decision code per outcome are this story's choice; the codes, the handler rules, the messages and the columns are fixed |
| Valuable | A refused move shows its cause and its holder, and an accepted move never quietly reassigns a deviation |
| Estimable | One read operation, one screen fragment, one event branch, one activity pair, the record and the inbox row |
| Small | Fits one sprint with its tests on the fakes |
| Testable | Component and contract tests on synthetic cases, a browser test of the panel through the composite route, and the boundary test |

### 7. Acceptance criteria

```gherkin
Feature: Manual transfer and reassignment screen with reason

  Background:
    Given the business date is 2026-12-15
    Given TRANSFER package version "TRF-2026.12" is in force, and row "TRF-010" refuses a move while a deviation is open
    Given user "U-TM-01" holds RW-TEAMMGR for team "MTG-BKK"
    Given case "RW-2026-000401" in queue "MTG-BKK-CO" owned by "U-CO-01", status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Given queue "LIT-BKK-01" uses "ROUND_ROBIN" with a caseload cap of 150 and owners "U-LO-01" with 80 cases and "U-LO-02" with 95 cases, next in turn "U-LO-02"

  Scenario: AC1 The panel shows the open deviation and the refusal (new, D-RCV-60)
    Given case "RW-2026-000402" with deviation "X1" open and owned by the complaint officer under rule "R-DEV-02", paused state "WITH_FCR_OFFICER" and contact stop true
    When "U-TM-01" opens SCR-05 for the case
    Then the deviation panel shows code "X1", handler "complaint officer", paused state "WITH_FCR_OFFICER", contact stop true and rule "R-DEV-02"
    Then the panel shows the refusal of the move as MSG-P3-033 naming rule "TRF-010"
    Then the case keeps queue "MTG-BKK-CO", owner "U-CO-01", status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01

  Scenario: AC2 Only open deviations are answered (new, D-RCV-60)
    Given case "RW-2026-000402" has deviation "X1" open and deviation "X7" cleared with outcome "RETURNED"
    When the move reads the deviations of the case
    Then the answer holds exactly one deviation, code "X1", handler "complaint officer", paused state "WITH_FCR_OFFICER" and return point "WITH_FCR_OFFICER"
    Then no answer holds the cleared code "X7"

  Scenario: AC3 The answer carries no personal data (new, D-RCV-60)
    Given case "RW-2026-000402" has deviation "X1" open
    When the read answers for the case
    Then the answer holds the case reference, the deviation reference, the code, the handler, the paused state, the contact-stop flag, the raised-at instant, the return point, the rule ID and the package version
    Then the answer holds no name, address, identity number, contact value or free text

  Scenario: AC4 Two open deviations on one case (new, D-RCV-60)
    Given case "RW-2026-000403" has deviation "X1" open under rule "R-DEV-02" and deviation "X3" open under rule "R-DEV-03" with contact stop true
    When "U-TM-01" opens SCR-05 for the case
    Then the panel names both codes, each with its own handler and its own rule
    Then the panel shows the refusal of the move as MSG-P3-033 naming rule "TRF-010"

  Scenario: AC5 An accepted move keeps the handler the deviation rule named (new, D-RCV-60)
    Given the rwb-case contract mock returns the transfer of case "RW-2026-000402" accepted to queue "LIT-BKK-01" with owner "U-LO-02" and reason "R05"
    When the CaseTransferred event for the case arrives on the inbox
    Then the deviation keeps code "X1", paused state "WITH_FCR_OFFICER", contact stop true and handler "complaint officer"
    Then the panel shows queue "LIT-BKK-01" and owner "U-LO-02" beside that handler
    Then one decision record holds rule "R-DEV-02", package version "TRF-2026.12", reason "R05", the from owner "U-CO-01", the to owner "U-LO-02" and the event ID

  Scenario: AC6 A cleared deviation no longer holds the case (new, D-RCV-60)
    Given case "RW-2026-000402" had deviation "X1" open and the clear was processed with outcome "RETURNED"
    When "U-TM-01" opens SCR-05 for the case
    Then the panel shows no open deviation and offers the form with the reason codes of LOV-TRANSFER-REASON at its version
    Then the cleared deviation is shown as history with outcome "RETURNED" and its return point "WITH_FCR_OFFICER"

  Scenario: AC7 A repeated event is processed once (new, D-RCV-60)
    Given the CaseTransferred event "EV-04-000901" for case "RW-2026-000402" was processed
    When the same event ID arrives again
    Then one decision record exists for the event
    Then the repeat is counted and the deviation row is unchanged

  Scenario: AC8 The record cannot be written (new, D-RCV-60)
    Given the local decision-record stub is stopped and answers MSG-P7-003
    When the CaseTransferred event for case "RW-2026-000402" is processed
    Then the transaction rolls back, the inbox row stays unprocessed and the deviation row is unchanged
    Then no event is published and the panel is unchanged
    Then the failure is visible as MSG-P7-003 on the attempt

  Scenario: AC9 Role without the right (new, D-RCV-60)
    Given a caller whose role does not hold Case record R
    When the caller reads the deviations of case "RW-2026-000402"
    Then the call is refused with 403 and MSG-P4-002 before any row is read
    Then the deviation row is unchanged
```

The nine criteria are new: this slice owns no legacy criterion, because the split gives the thirteen criteria of RWB-E2-012 to the primary slice in rwb-case (`acs` is empty on this slice), and each criterion here tests only the deliverable of the title — the deviation answer, the panel and the handler rule. Every value in the scenarios — the business date, the package version, the rule IDs, the case and queue IDs, the cap of 150, the reason codes, the deviation codes, the outcome words, the paused state and the message IDs — is copied character for character from RWB-E2-012 §7, §8, §14 and §15 and from TSD S8 T3.2, T4 and T6.1; no value is invented.

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DEV-01 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | Workbench | Same day |
| R-DEV-02 | Deviations | X1 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X1 | Assign to the complaint officer | DEV_WITH_OWNER | Complaint officer | Workbench | None |
| R-DEV-03 | Deviations | X2, X3 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X2,X3) | Assign to the specialist; Legal joins X3 for the estate claim | DEV_WITH_OWNER | Hardship and vulnerability specialist | Workbench | None |
| R-DEV-18 | Deviations | X1 to X7 | DEV_RESOLVED | CLOCK_RESUMED | Any | Resume the stage clock and return the case | RESUMED | Previous owner | Workbench | None |

The four rows are copied character for character from FSD S8 A2.2.3.1, A2.4.3.1 and the DEVIATION machine of TSD S8 T4. R-DEV-04 to R-DEV-06 assign X4 to X7 to their named owners; their text is Not specified in the source documents (GAP-3094; ASM-5283). The owner column is a business role, not a service.

| ID | Rule | Source |
|---|---|---|
| BR1 | A manual move needs a reason code from LOV-TRANSFER-REASON, read at its version from the reference data of rwb-case | Legacy BR1; REQ-WKM-003; REQ-CWC-010; DP-07 |
| BR2 | A move the TRANSFER package refuses is not made, and the refusing rule ID is shown; this service names the deviation that holds the case beside it | Legacy BR2, BR10; RWB-E2-012 AC2 |
| BR3 | A case with an open deviation stays with the owner the deviation rule named; an accepted move records the move and keeps that handler | Legacy BR10; R-DEV-02; R-DEV-03 |
| BR4 | The open-deviation answer carries the code, handler, paused state, contact stop, raised-at, return point and rule ID only; no personal field | Template and Rules v1 §R7.2 s17 |
| BR5 | A cleared deviation is history and is not part of the open answer; it keeps its outcome and its return point | Legacy BR6; TSD S8 T3.1 (`cleared_at`, `outcome`); LOV-DEV-OUTCOME |
| BR6 | The deviation state, paused state, contact stop, raised-at and return point are never changed by a move | Legacy BR6; R-UNI-18; R-UNI-46 |
| BR7 | A case under a legal hold is not moved; the panel names the hold and the refusal | Legacy BR7; R-UNI-20 |
| BR8 | A step that cannot be written to the decision record changes nothing and answers MSG-P7-003 | Legacy BR8; DP-03; TSD S8 T2 |
| BR9 | A repeated `CaseTransferred` event ID is processed once, and a repeated request with the same `Idempotency-Key` answers what it already answered | Legacy BR9; R-UNI-40 |
| BR10 | Neither this service nor the screen reads another service's table: the case, queue and assignment come on the rwb-case contract, the package from rwb-decision, the right from rwb-access | DP-01, DP-04, DP-11 |
| BR11 | No person name, contact value, address or identity number enters the deviation row, the answer, a decision record, a log or an event | Template and Rules v1 §R7.2 s17 |

### 9. State transitions

This story changes no case status and no case state; it reads the deviation and records a move against it.

| From (`deviation.state`) | Event | Condition | To |
|---|---|---|---|
| DEV_WITH_OWNER, or no change | A `CaseTransferred` is processed for the case | The row is open | Unchanged: `handler_user_id`, `paused_state`, `contact_stop`, `raised_at` and the return point all stay as they were |
| DEV_RESOLVED or RESUMED | The clear path has run and the row holds `cleared_at` | The row is history | Unchanged; the row leaves the open answer |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | `CaseTransferred` arrives | The event ID is new | Applying |
| Waiting | The same event ID arrives again | Inbox hit (BR9) | Waiting, counted |
| Applying | The decision record is written | The transaction commits | Waiting for the next event |
| Applying | The record write fails (BR8) | X8 | Waiting, the inbox row unprocessed, nothing changed |

The deviation machine of TSD S8 T4 (22 rules over 9 states) is untouched by this story; R-DEV-01, R-DEV-02, R-DEV-03 and R-DEV-18 keep working as the FSD states them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Team manager (RW-TEAMMGR) | Opens SCR-05 and reads the deviation panel of the cases in the team's scope (TSD S8 T6.1; the move itself is P3's) |
| Capacity and workforce planner (RW-CAPACITY) | Reassigns cases for capacity and reads the same panel |
| Case owner (RW-CASEOWN) | Raises and clears the deviation whose response feeds the panel; holds CRU on the case record |
| Complaint officer (RW-COMPLAIN), Hardship and vulnerability specialist (RW-SPECIAL), Fraud investigator (RW-FRAUD), Legal counsel (RW-LEGAL) | Hold the deviation the rules named and see it on the panel; hold RU or R on the case record |
| rwb-case (P3) | Owns the move, its checks and the `CaseTransferred` event; reads the open deviations here |
| rwb-decision (P7) | Owns the TRANSFER package, its rows, their order and their versions; this story evaluates nothing |
| rwb-access (P4) | Owns the roles and the Case record right checked on the read |
| Solution architect | Confirms the read operation and its shape, which the sources do not publish (GAP-3093; GAP-3095) |

No delegation of authority level applies: a transfer moves work, not money (legacy §10).

### 11. Data

| BR Field ID | Table | Owner | Use in this story |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` | S8, `rwb_deviation` | **Read** for the open answer; **write** only the standard record columns and the row the move is recorded against; no column is added |
| None: library table | `decision_record` | Platform library in `rwb_deviation` | The hash-linked record of the move against the deviation (DP-03) |
| None: library table | `outbox_event`, `inbox_event` | Platform library in `rwb_deviation` | The two event rows and the processed `CaseTransferred` ID (DP-09) |
| DF-CAS-001, DF-CAS-005, DF-CAS-007, DF-CAS-009, DF-CAS-010, DF-CAS-011, DF-CAS-019, DF-CAS-020 | `recovery_case` | P3 rwb-case | The case reference, status, route state, owner, queue, team, deviation flag and legal hold; consumed on the contract, never written |
| DF-WRK-001, DF-WRK-004, DF-WRK-006, DF-WRK-007, DF-WRK-039, DF-WRK-040 | `queue`, `assignment` | P3 rwb-case | The target queue, its team, its method, its cap and the assignment with `transfer_reason_code`; named, never written |
| DF-REF-002, DF-REF-281, DF-REF-282, DF-REF-296 to DF-REF-298 | `rule_row`, `rule_package_version` | P7 rwb-decision | The TRANSFER rows and the version in force; read through the package, never written |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | The central ledger; rwb-decision copies the local record, this story does not write it |

`deviation` carries no transfer reason, no rule ID and no rule-version column (TSD S8 T3.1), so the reason code, the rule ID and the package version of a move live in the decision record only (GAP-3096; ASM-5285). The lists are reference data read at their version: `LOV-DEVIATION` and `LOV-DEV-OUTCOME` from TSD S8 T3.2, and `LOV-TRANSFER-REASON` with R01 to R06 on the rwb-case reference-data contract (DP-07; GAP-3097).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). The read is the operation the P3 slice of this legacy key names; the two write operations are the service's and are unchanged by this story (GAP-3093; ASM-5282).

| Method | Path | Shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/deviations` | `DeviationSummary` list out: deviation reference, code, handler, paused state, contact stop, raised-at, return point, rule ID and package version; `[]` when nothing is open | Case record, right R, scope applied | Not applicable |
| POST | `/cases/{caseId}/deviations` | `DeviationRequest` in, `Deviation` out (API-S8-001) | Case record, right U, scope applied | `Idempotency-Key` header |
| PATCH | `/deviations/{deviationId}` | `DeviationOutcome` in, `Deviation` out (API-S8-002) | Case record, right U, scope applied | Not applicable |

All three answer 401, 403 with MSG-P4-002, 404, 409, 422 and 503 in the platform error envelope; the exact shapes, the error list and the fakes are the CON story's of this service. The GET is the only operation this story builds.

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The transfer of the case and the assignment it answers (C `RWB-P3-E2012-CON`); operation `POST /cases/{caseId}/transfer` under `/api/recovery/case/v1` | P3 rwb-case | The move the screen performs; the accepted or refused answer the panel reflects |
| The case record read; operation name Not specified in the source documents (GAP-3092; ASM-5281) | P3 rwb-case | Queue, owner, team, status, route state, deviation flag and legal hold shown beside the deviation |
| The reference-data read of `LOV-TRANSFER-REASON` (DP-07); operation name Not specified in the source documents (GAP-3092; ASM-5281) | P3 rwb-case | The six reason codes R01 to R06 with their version |
| The package and rule-in-force read (DP-04); operation name Not specified in the source documents (GAP-3092; ASM-5281) | P7 rwb-decision | The TRANSFER version in force, so the panel can name it and answer MSG-P3-027 |
| The authorise call on Case record R; operation name Not specified in the source documents (GAP-3092; ASM-5281) | P4 rwb-access | The right and the scope of the read |
| The case-facts read (DP-05); operation name Not specified in the source documents (GAP-3092; ASM-5281) | P1 rwb-source-data | The case facts the panel shows, with their freshness stamp |

All six are one hop with a 2 s budget and a breaker, and none retries inside the step (DP-11, ADR-020). Only the first is a row of the plan's C list, which holds `RWB-P3-E2012-CON` alone.

#### 12.3 Events published

| Event | Topic | Data | Consumers |
|---|---|---|---|
| `DeviationRaised` (EV-06, `rwb.deviation.DeviationRaised.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, code, raised-at, paused state, contact-stop flag, rule ID and package version; no personal data | rwb-case, rwb-comms and rwb-reporting (connection matrix column S8) |
| `DeviationCleared` (EV-07, `rwb.deviation.DeviationCleared.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, outcome, cleared-at, rule ID and package version; no personal data | rwb-case, rwb-comms and rwb-reporting |

The two ids are the events the Ownership Map gives S8 and the two names TSD S8 T5.3 publishes; this story adds none and does not republish `CaseTransferred`, which is rwb-case's (EV-04).

#### 12.4 Events consumed

| Event | Owner | Use |
|---|---|---|
| `CaseTransferred` (EV-04, `rwb.case.CaseTransferred.v1`) | P3 rwb-case | Records the move against the deviation and keeps the handler the deviation rule named (BR3) |
| The case status and legal-hold changes; event names Not specified in the source documents (GAP-3095; ASM-5284) | P3 rwb-case | Keeps the panel's hold and status reading aligned with the case |

The S8 row of the connection matrix names an event subscription to P3 and publishes no event name for it; the second group is declared against the placeholder and faked.

#### 12.5 Workflows and activities

| Name | Type | Queue | Element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, started at any time, child of `CaseWorkflow`, parent close policy ABANDON, continues-as-new | `rwb-deviation` in namespace `rwb-recovery` | Hosts the transfer branch (DP-10) |
| `readOpenDeviations` | Activity, the query step | `rwb-deviation` | The case reference in; the open rows and the rule that holds each out |
| `applyCaseTransfer` | Activity | `rwb-deviation` | The `CaseTransferred` fact in; the kept handler and the outcome out |
| `recordDeviationMove` | Activity, the RecordAndApply step | `rwb-deviation` | The decision record and the inbox row in one transaction |

The workflow is the one the Ownership Map gives S8; the three activity names are this story's and sit on the same queue. The read used by the screen is served by the operation, not by an activity.

#### 12.6 Schedules

None. The Ownership Map gives S8 no job and the trigger here is an event; no Quartz row and no shared job table is added (DP-10 is applied as an event-driven branch, not as a Schedule).

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | The rows the open answer is built from and the row a move is recorded against |
| `decision_record` | Platform library in `rwb_deviation` | The local record of the move (DP-03) |
| `outbox_event`, `inbox_event` | Platform library in `rwb_deviation` | The two published events and the processed `CaseTransferred` ID |

`recovery_case`, `queue`, `assignment`, `timer`, `decision_log_entry`, `rule_row` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves `rwb_deviation` (DP-01).

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| rwb-case transfer fake (`RWB-P3-E2012-CON`) | An accepted move to `LIT-BKK-01` with owner U-LO-02; a refusal at TRF-010; a version conflict | AC1, AC5 |
| rwb-case case-read fake | Case in `MTG-BKK-CO` with `U-CO-01`, status IN_PROGRESS, route state WITH_FCR_OFFICER; a held case; a moved case | AC1, AC5 |
| rwb-case reference-data fake | `LOV-TRANSFER-REASON` R01 to R06 at its version | AC6 |
| rwb-decision package fake | TRANSFER at `TRF-2026.12`; `NoPackageInForce` | AC1, AC5 |
| rwb-access authorise fake | A granted Case record R; a refused one | AC9 |
| rwb-source-data data-product fake | The case facts with a fresh stamp; a stale stamp | Section 5 X9 |
| Local decision-record stub (DP-03) | A healthy chain; a stopped chain answering MSG-P7-003 | AC8 |
| Inbox and outbox stubs (DP-09) | A processed `CaseTransferred`; a repeat; a failing relay | AC7, AC8 |
| gateway-bff composite route fake (DP-19) | The merged SCR-05 answer with the deviation fragment for a synthetic case | AC1, AC4, AC6 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 6 consumed | The deviation read and the two unchanged write operations on `/api/recovery/deviation/v1`; the rwb-case transfer and case read, the reference-data and rwb-decision reads, the rwb-access authorise and the rwb-source-data read; one hop, 2 s |
| Kafka | 2 published, 2 consumed | `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1`; `CaseTransferred` and the case status and hold changes; the decision record rides the library's `rwb.decision-record.v1` and is not this service's event |
| Temporal | 1 workflow and 3 activities | `DeviationWorkflow` with `readOpenDeviations`, `applyCaseTransfer` and `recordDeviationMove` on `rwb-deviation`; no Schedule |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Deliverables.** The deviation read on `/api/recovery/deviation/v1`, the SCR-05 deviation panel with its four states, the `CaseTransferred` branch of `DeviationWorkflow` with its three activities, the decision record and the inbox row, the two event relays, and the per-service Flyway sequence of `rwb_deviation`.

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>`, "recovery schema" | Owner's schema `rwb_deviation`; no other service's table is read | None |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H `RWB-PLT-E1072-CON`; C `RWB-P7-E1073-CON` |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract | None |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H `RWB-PLT-E1043-CON`; C `RWB-P3-E1043-CON` |
| DP-09 | Application event, EV-nn, outbox | Outbox, inbox and idempotency library, owner topic, CloudEvents | H `RWB-PLT-TE006-CON` |
| DP-10 | Quartz, JOB-nn | Event-started workflow through the workflow kit | H `RWB-PLT-E1071-CON` |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | None (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-14 | `rwb.p<n>.` and `rwb.casewf.` topic names | `rwb.deviation.events.v1` through the naming library | H `RWB-PLT-E1047-CON` |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_deviation` | H `RWB-PLT-E1044-CON` |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

The eight H rows are platform contract rows; the plan's build list for this key is empty and therefore stays empty in the metadata, and the rows are tracked, not blocking (GAP-3091; ASM-5280). DP-11 keeps the one class C dependency the plan gives, `RWB-P3-E2012-CON`; DP-04 and DP-07 also add a C row each, which the metadata does not carry.

**Build steps.** (1) Build the repository query for the open rows and the `DeviationSummary` map, with the field allow-list of BR4. (2) Publish `GET /cases/{caseId}/deviations` with the authorise call and the error mapping. (3) Build the panel with its states: open, refused, cleared history, empty. (4) Wire the `CaseTransferred` consumer and the `DeviationWorkflow` branch with its three activities. (5) Keep the handler of each open row and record the move with the rule ID and the package version, in one transaction with the inbox row. (6) Relay `DeviationRaised` and `DeviationCleared` through the outbox. (7) Fold the story's schema need into the per-service Flyway sequence, with no shared `recovery` migration. (8) Prove AC1 to AC9 on the fakes and run the boundary test.

**Feature flag.** `rwb.s8.transfer-panel`. Off: the panel shows no deviation fragment and the read answers 404 to the composite route, while the two write operations keep working.

**Done when.** AC1 to AC9 pass at component and contract level on the fakes, the panel renders the open, refused, cleared and empty states through the composite route, a repeated `CaseTransferred` writes once, a failed record changes nothing, and the boundary test shows no `rwb_case` statement and no `v_ace_*` read.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | A manual transfer without a reason (the primary slice's path, named for traceability) | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner, or every owner of the target queue, at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Case closed or under a legal hold | This case cannot move to {state} from {current}. |
| MSG-P3-027 | No TRANSFER package version in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-033 | A TRANSFER rule refuses the move, and the panel names the deviation beside it | Rule {rule} does not allow this transfer. |
| MSG-P3-035 | A selection with refusals | {done} of {total} cases were moved. The others show the reason on their row. |
| MSG-GEN-004 | Two moves of one case at once | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-005 | Move saved | Saved. |
| MSG-P4-002 | A role without Case record R | You cannot {action} here. Your role does not include it. |

The text is RWB-E2-012 §14 and FSD S8 A2.1.3.1, copied unchanged; no message is reworded and none is added. For MSG-P3-027 the {check} value is "package in force" and the {detail} names the package code TRANSFER and the business date only. The {rule} value of MSG-P3-033 is the rule ID the case read returned.

### 15. Screens and states

| Screen | State | What this story answers |
|---|---|---|
| SCR-05 Transfer case | Form | The deviation fragment: codes, handlers, paused state and contact stop of the open deviations; empty when nothing is open |
| SCR-05 Transfer case | Refused | The deviation fragment beside MSG-P3-033 naming the rule and the deviation that holds the case, or MSG-P3-027 |
| SCR-05 Transfer case | Saved | The deviation fragment after the move: the case's new queue and owner, and the handler the deviation rule kept |
| SCR-03 Case record | Read only; on hold | The same open-deviation answer, read for the case banner |
| SCR-07 Team queues | List | The selection of up to 50 cases the screen is opened from; this story answers per case |
| SCR-09 Exception queue | List | Not used by this story; a refused move is not queued |

SCR-05 is a gateway-bff composite route (DP-19): the route owns the path and the merge order, rwb-case contributes the form, the case read and the move, and this service contributes the deviation fragment only. The panel never renders a rule row or a deviation text of another service; it renders codes, IDs and message IDs. The fragment's own layout is Not specified in the source documents (GAP-3094; ASM-5283).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-012-01 | AC5, AC3 | Component | RW-2026-000402 moved to LIT-BKK-01 with owner U-LO-02, reason R05, TRANSFER version TRF-2026.12 |
| TC-E2-012-02 | AC1, AC4 | Contract | RW-2026-000402 with X1 open under R-DEV-02; row TRF-010 refuses |
| TC-E2-012-03 | AC2, AC4 | Component | Ten cases read once each; the open rows only |
| TC-E2-012-04 | AC1, AC2 | Component | A refused request leaves the panel answer as it was |
| TC-E2-012-05 | AC1, AC5 | Component | Owner U-CO-04 at 150 of 150; the deviation row unchanged |
| TC-E2-012-06 | AC5 | Component | U-CO-09 in team SME-NTH, reason R04; handler kept |
| TC-E2-012-07 | AC1 | Component | RW-2026-000403 with legal hold true; the panel names HELD_LEGAL |
| TC-E2-012-08 | AC7 | Component | Two parallel requests for one case; one CaseTransferred |
| TC-E2-012-09 | AC7 | Component | The same event ID and the same Idempotency-Key twice |
| TC-E2-012-10 | AC8 | Component | Decision-record store stopped |
| TC-E2-012-11 | AC4 | Component | Ten cases, two under a legal hold; each row read on its own |
| TC-E2-012-12 | AC1, AC4 | Component | Both LIT-BKK-01 owners at 150 |
| TC-E2-012-13 | AC9 | Component | RW-CASEOWN without Case record R reads the deviations; 403 with MSG-P4-002 |
| TC-E2-012-14 | AC8 | NFR | Decision record write forced to fail; deviation row, inbox row and outbox unchanged |
| TC-E2-012-15 | AC1, AC6 | Component | No TRANSFER version in force on 2026-12-20; the panel answers MSG-P3-027 |

The fifteen ids are the legacy cases of RWB-E2-012 in their legacy order, carried as the proof of this slice, with the Covers column naming the criterion of this story that each one exercises at the level this slice runs. The same fifteen ids are also carried by the primary slice RWB-P3-E2012-APP, which exercises the move itself at End to end and NFR; the duplication is registered once (GAP-3098; ASM-5287). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same id. No `-ITG` copy belongs to this story: it has no class I dependency.

### 17. Guardrails

- No business value in code: the reason codes, the deviation codes, the handler rules, the cap and the rule rows are reference data or package rows, read with their version.
- No personal data in the answer, the deviation row, a decision record, an event, a workflow input, a log or a prompt: identifiers, codes, instants and a rule version only. The panel renders no free text of the case.
- ACE data and case data only through the owner's contract: no `v_ace_*` view, no `rwb_case` statement and no other service's schema (DP-01, DP-05, DP-11).
- One evaluator per service and one package registry: this story evaluates no TRANSFER row, it reads the version in force only to name it (DP-04; ADR-017). A missing version is never a default decision (R-UNI-41).
- One base, one topic, one queue and one login per service; this story adds no second topic and no Schedule (DP-13, DP-14).
- A read that does not answer inside 2 s leaves the panel without the deviation fragment and never lets a move proceed on an unread deviation; a refused authorisation refuses the read rather than widening it.
- The decision record is written before the commit and in the same transaction as the inbox row; a failure rolls both back.

### 18. Traceability

| Legacy | Owner after the split | This story |
|---|---|---|
| RWB-E2-012 AC1 to AC13 | The primary slice RWB-P3-E2012-APP in rwb-case (`acs` is empty here) | AC1 to AC9 prove the deviation answer, the panel and the handler rule on the fakes |
| RWB-E2-012 BR10 and AC2 (a move refused while a deviation is open) | Both: P3 refuses and names the rule; S8 supplies the fact | AC1, AC4 |
| RWB-E2-012 §15 SCR-05 and its four states | The primary slice owns the screen; this story owns the deviation fragment | AC1, AC4, AC5, AC6 |
| RWB-E2-012 §14 messages | The primary slice owns the texts; this story renders MSG-P3-033, MSG-P3-027 and MSG-P4-002 | Section 14 |
| RWB-E2-012 TC-E2-012-01 to -15 | Both slices carry the ids (GAP-3098) | The fifteen at Component and NFR level |
| RWB-E2-012 §12 transfer endpoint and §13 solution plan | The primary slice | Not restated; named in sections 1 and 19 |

| Source | What it supplies |
|---|---|
| REQ-WKM-003, REQ-WKM-007, REQ-WKM-008, REQ-CWC-010, REQ-CWC-016 | A move with a coded reason, a reallocation inside the team, the history on the case, and every decision logged with its rule and version |
| RWB-E2-012 §1 to §19 | BR10 and its rules, AC2, the message texts, the screen states, the reason codes and the legacy tests |
| FSD S8 A2.1, A2.2, A2.4, A2.6 and A2.9; TSD S8 T2, T3.0 to T3.2, T4, T5.3, T6.1 and T-A.1 | R-DEV-01 to R-DEV-03, R-DEV-18, the `deviation` columns and lists, two open deviations on one case, the two events, the rights and the two write operations |
| Context pack S8, the connection matrix and the Ownership Map | The schema, base, topic, queue, the two events, the one owned table, the workflow and the listeners |
| Split plan, slice RWB-S8-E2012-APP | H, C, I, X, the lane, the wave and the release |
| RWB-P3-E2012-APP §12 | The read `GET /cases/{caseId}/deviations` this service must publish for the move (GAP-3093) |

### 19. Out of scope

- The transfer endpoint `POST /cases/{caseId}/transfer`, its reason-code, cap, team, hold, scope and version checks, the assignment swap and the `CaseTransferred` publication: the primary slice of this legacy key in rwb-case.
- The transfer screen beyond the deviation fragment: the form, the target queue or owner picker, the at-cap warning, the bulk runner and the summary (the primary slice, DP-19).
- The TRANSFER package rows, their authoring, approval, promotion and rollback (rwb-decision, P7), and the reference data of `LOV-TRANSFER-REASON` (rwb-case, P3).
- The raise and clear paths themselves, the screening agent, the low-confidence review, the two-deviation handling rule and the other six deviation codes each with its own story of this service.
- The roles, rights and delegation of authority (rwb-access, P4); the notices (rwb-comms, P6); the documents (rwb-document, P5).
- The schema, migration, login, deployment, observability and pipeline of `rwb_deviation` beyond this story's own Flyway sequence (the DB, INF and OPS stories of this legacy key).
- Any change to a legacy file, to a master, or to built Epic 1 code.
