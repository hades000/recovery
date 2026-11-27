# RWB-P6-E2013-APP Approval routing with the delegation of authority table

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P6-K |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E2013-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-007, REQ-APD-008, REQ-APD-009, REQ-APD-010, REQ-APD-011) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-013 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E2013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **approver, for example the Head of Litigation (RW-HEADLIT)**, I want **one notice the moment an approval passes its service level or is passed up for want of a holder, worded with the decision and the case it concerns, delivered through the ACE notification path and readable with the role it went to and the time it was sent**, so that **no item waits unseen and the person who now has to decide is told once, and never twice about the same breach**.

Inside `rwb-comms` this is the notification capability of the legacy story RWB-E2-013:

- Service `rwb-comms`, schema `rwb_comms`, REST base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with event names `rwb.comms.<Event>.v1`, Temporal task queue `rwb-comms` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.comms`.
- One deliverable and nothing else: the escalation notification. On the approval facts of an escalation or of a pass-up for want of a holder, the service renders MSG-P7-011 from its template, writes one `notice` row, hands the message to the ACE notification path, and publishes the notice facts.
- The router, the `ApprovalWorkflow` of the workflow kit, the approve, refuse and return operations, the item's move and the decision records stay in `rwb-decision` (P7, RWB-P7-E2013-APP and RWB-P7-E2013-CON). The case status, the approval task and the service level timer projection stay in `rwb-case` (P3, RWB-P3-E2013-APP). The delegation of authority table and the authorise answer stay in `rwb-access` (P4, RWB-P4-E2013-APP and RWB-P4-E1038-APP). The service level, the timer and the escalation clock stay with RWB-P3-E1028-APP.
- The item is moved by `rwb-decision`. This story only notifies: it changes no approval, no task, no timer and no case status, it holds no copy of a level, a limit or a holder, and it reads no table of another service.
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1220; ASM-2178); this story uses the phrase "the rwb-comms login (DP-02)" and never the shared monolith login.

The legacy behaviour carried into the communications service is unchanged: the same message text with the decision and the case number, the same single telling of the new approver on a service level breach, the same telling on a pass-up for want of a holder, the same refusal to tell anybody when there is nobody to tell, and the same hold when the template of the message is withdrawn.

### 2. Business rationale

Approval and authority governance is an audit finding: approvals today are given by e-mail, sometimes above the approver's limit or by the person who prepared the decision, and the person who should have decided often learns of the item only when somebody telephones. The decision side of that finding is routed by the delegation of authority table in `rwb-decision`, and the case side is put in `WAITING_APPROVAL` by `rwb-case`; neither of them can speak. This story is the voice of the control: when an item passes its service level and moves to the escalation role, or when a level has nobody on it and the item passes up at once, the approver who now holds it is told in words that name the decision and the case. Without that notice the escalation exists on a screen that nobody has open, and the measure decisions within the delegation of authority cannot reach its target of 100 percent.

Under Architecture v5 the approval is the `ApprovalWorkflow` of the workflow kit on `rwb-decision`, routed by the DoA table of `rwb-access`, and `rwb-comms` owns notices, templates, merge fields and proof of delivery (slides 14, 17 and 41). The realignment changes the mechanism, not the business rule:

1. The in-process call that told the new approver inside the monolith becomes the notice of `rwb-comms`, rendered from a template and sent on the ACE notification path that slide 17 gives this service.
2. The `TimerBreached` of JOB-05 and the P7 escalation listener of the monolith become one consumed fact: `rwb-decision` re-publishes `ApprovalRequested` with the escalation level raised and the new due time when the durable timer of the approval breaches, and this service consumes it through the inbox of DP-09.
3. The decision log writer of another module becomes the local decision-record library of DP-03, written in the same transaction as the notice, and published on `rwb.decision-record.v1`.
4. The parameter rows that name the route role and the escalation role stay `rwb-case`'s and are read by `rwb-decision`; this story receives the resolved role in the approval facts and never resolves a level, a limit or a holder of its own.
5. The reference lists of channel, template state and notice type are read through the reference-data contract of DP-07, and the notice read inherits the guard and the authorise contract of DP-08.

This story meets REQ-APD-007 and REQ-APD-011 on the notification side and carries the notification half of REQ-APD-001, REQ-APD-003, REQ-APD-004, REQ-APD-005, REQ-APD-008, REQ-APD-009 and REQ-APD-010; it puts the telling half of CTL-04 and CTL-05 in place and leaves the deciding half where the other slices put it.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P7-E2013-CON | The published approval contract: the approval read with its level, limit version, route role, status, due time and escalation level; the `ApprovalRequested` event on `rwb.decision.events.v1`, re-published with the escalation level raised; and the contract fakes. Which fields of an approval event this service consumes is Not specified in the source documents (GAP-1220; ASM-2178), and the fact set this story assumes is that of ASM-2182 |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the notice |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): `rwb.approval.route.D7.1.area`=LITIGATION, `rwb.approval.route.D7.1.role`=RW-LITOFF, `rwb.approval.route.D7.1.escalation-role`=RW-HEADLIT and `rwb.approval.route.D7.1.service-level`=1 working day (assumed; DL22), read by `rwb-decision` and never resolved here |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): LOV-CHANNEL, LOV-NOTICE, the template states and the notice states, with the version in force |
| RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The guard library and the `rwb-access` authorise contract (DP-08): the cached permission decision behind the notice read, refusing with MSG-P4-002 |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one escalation fact handled once, and the send retried from the outbox |
| RWB-PLT-E1071-CON | The workflow kit in namespace `rwb-recovery` (DP-10): the durable timer of `ApprovalWorkflow` on `rwb-decision` is the clock; this story starts no workflow |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19); no screen of this story is served through it |

Business preconditions carried from RWB-E2-013:

- Delegation version DOA-2026.11 is in force and the lookup returns the lowest covering level (legacy RWB-E1-038). In the target the table is `rwb-access` (P4) and the lookup is its DoA-limits contract; holders and substitutes are named test users in SIT and UAT (DL18). This story reads none of it.
- Service level for a limit-based approval: `rwb.approval.service-level.default`=3 working days (assumed from the 3 working day approval timers in R-RES-10 and R-SET-05; DL22); for D7.1 notices 1 working day.
- Capability area per decision code: D5 and D6.x Treatment and offer, D7.x Litigation, D8.2 and D8.3 Asset and disposal, D8.4 Debt sale, D9.x Write-off and posting (parameters `rwb.approval.area.<code>`); these are read by `rwb-decision`.
- The template of the escalation notice is Approved for Legal and current on the business date, and it carries the message ID MSG-P7-011 with the two placeholders `{decision}` and `{caseNo}`. The template code of the escalation notice is Not specified in the source documents (GAP-1220; ASM-2178).
- The channel of the escalation notice is one of the LOV-CHANNEL values and the ACE notification path serves it (Architecture v5 slide 17: SMS and LINE on the ACE notification path); the channel value chosen for this template is Not specified in the source documents (GAP-1220; ASM-2178).
- The escalation roles are parameter rows of `rwb-case` read by `rwb-decision` under the R-PREC default ruling; for D7.1 notices the route role is RW-LITOFF and the escalation role RW-HEADLIT, and both arrive in the approval facts.
- The ACE notification path is reachable from this service under its own service identity, with the addressing of a role and of a user reference. How a role code and a user reference become a delivery address on that path is Not specified in the source documents (GAP-1220; ASM-2178), and the addressing this story assumes is that of ASM-2183.

### 4. Flow

1. `rwb-decision` (P7): the durable timer of the `ApprovalWorkflow` breaches at the due time of the approval, the router moves the item one level up, or to the escalation role for a role-routed item, restarts the timer with the new due time, and publishes `rwb.decision.ApprovalRequested.v1` on `rwb.decision.events.v1` for the same approval reference with the escalation level raised by one and the new due time. The decision record with final call ESCALATED is `rwb-decision`'s.
2. `rwb-comms` `EscalationNoticeListener`: reads the event into the inbox of DP-09, deduplicates by event ID (R-UNI-40), and passes the approval facts to `EscalationNoticeService`: approval reference, case ID and case number, decision code, capability area, the routed role or holder, the approval level, the limit version, the escalation level and the due time.
3. `EscalationNoticeService`: decides whether the fact is a telling. An event whose escalation level is zero and which names no covering role or holder is not a telling; an event that repeats an approval reference and an escalation level already notified is not a telling (BR13; ASM-2184). Nothing else is filtered: the item's own move, its status and its case are not this service's to judge.
4. `EscalationNoticeService`: reads the template of the escalation notice with the version in force, reads LOV-CHANNEL and the notice states through the reference-data contract of DP-07, and resolves the merge values `{decision}` and `{caseNo}` from the approval facts. The merge field set is that of TSD P6 T3.1 `merge_field`, and no value of a level, a limit or a holder is merged, because this service holds none.
5. A template that is withdrawn, or has no Approved version current on the business date, holds the notice with hold reason `TEMPLATE_WITHDRAWN` and raises MSG-P6-003 to the owner of the template; nothing is handed to the notification path (VR-P6-001-1; R-LIT-04; ASM-2185).
6. `EscalationNoticeService`, one `RecordAndApply` transaction in `rwb_comms`: the `notice` row is written with notice kind `ESCALATION`, the approval reference, the escalation level, the recipient role, the template code and version, the merged message, the channel, the state Generated and `sent_at` empty; the local decision record of DP-03 is written with decision code D7.1, rule R-UNI-30, the approval reference, the escalation level and final call ESCALATED; the outbox rows for `rwb.comms.NoticeGenerated.v1` and for the send are written; and the unique key of the notice kind, the approval reference and the escalation level makes a second notice for the same level impossible (BR13).
7. The outbox relay of the platform hands the merged message to the ACE notification path for the recipient role, addressed by the path. The path accepting the message sets `sent_at` at the acceptance time, moves the notice to Sent and publishes `rwb.comms.NoticeDispatched.v1` in the same transaction.
8. The path returning unavailable leaves the notice as it is, with `sent_at` empty, records MSG-GEN-006 naming the notification path, and leaves the outbox row to its retry; the retry that succeeds sends once and sets `sent_at` once. A retry of a message the path already accepted is refused by the path's own idempotency, and no second send happens.
9. The approved approver reads the notice with `GET /api/recovery/comms/v1/notices/{noticeId}` and sees the message, the recipient role, the approval reference, the escalation level, the template code and the sent time; the read is guarded by the authorise decision of DP-08 and refused with MSG-P4-002 and MSG-P4-003 as section 14 states.
10. An internal caller may also ask for the notice to be produced with `POST /api/recovery/comms/v1/cases/{caseId}/messages` and an Idempotency-Key; the answer is 202 with the notice reference and the same one-notice-per-level rule applies, so a repeated request returns the first notice.
11. Nothing in this story changes the case, the task, the timer or the approval: the case stays `WAITING_APPROVAL`, the task of the covering level stays open, and the new due time is `rwb-decision`'s and `rwb-case`'s to keep.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The service level passes with no action | One notice is rendered and sent to the escalation role; the item, its task and its case are not touched | MSG-P7-011 | AC1 |
| X2 | The same timer-breach fact is delivered again, or replayed from the topic | No second notice and no second send; the inbox dedupe and the one-notice-per-level key both hold | None | AC3 |
| X3 | A level has no holder and no substitute, and the item passes up at once | No notice is addressed to the empty level; one notice is addressed to the covering level that received the item | MSG-P7-011 | AC4 |
| X4 | No delegation row covers the decision and product, so the item is held with no approver named | No notice is produced, because the facts name nobody; the hold and the incident stay `rwb-decision`'s | MSG-P7-010 (produced by `rwb-decision`) | AC4 |
| X5 | The template of the escalation notice is withdrawn or has no Approved version | The notice is held with hold reason `TEMPLATE_WITHDRAWN`; nothing is sent; a task with MSG-P6-003 goes to the owner of the template | MSG-P6-003 | AC5 |
| X6 | The ACE notification path returns unavailable | The notice stays with `sent_at` empty and the outbox retries; the retry that succeeds sends once | MSG-GEN-006 | AC6 |
| X7 | The local decision record cannot be written | Nothing is written: no notice row, no outbox row, no send, and the event stays on the topic for redelivery | MSG-P7-003 | AC1, TC-E2-013-16 |
| X8 | The caller holds no right for the notice read, or the notice is outside the caller's scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; nothing is returned | MSG-P4-002, MSG-P4-003 | AC2, TC-E2-013-15 |
| X9 | The message cannot be rendered because a merge value of the approval facts is absent | Nothing is written and nothing is sent; the incident names the approval reference and the template code | MSG-GEN-006 | AC1 |
| X10 | An approval is approved, refused or returned instead of escalating | No escalation fact is published for it, so no notice is produced and nothing is sent | None | AC1 |

A stale `notice` row at commit, matched on its `version` column, is MSG-GEN-004 and the event is retried, never applied twice; the notice, its decision record and its outbox rows are always written together, so a notice cannot exist without its record and a send cannot be asked for a notice that was not recorded.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the approval contract of RWB-P7-E2013-CON, the platform contract libraries of its DP table and the fakes; no approval, case or delegation behaviour is rebuilt here |
| Negotiable | The template code, the channel, the recipient roles and the message text are data or parameters; the story fixes only the one-notice-per-level rule and the hold and retry behaviour |
| Valuable | The approver who now holds an escalated item is told once, with the decision and the case, and no item waits unseen |
| Estimable | One consumer, one notice service, one template and merge read, one outbox send path, two operations, one migration |
| Small | Fits one sprint with its tests; it is the notification slice of the legacy key |
| Testable | Each of the seven criteria in section 7 runs as one automated test against the contract fakes, with a fixed clock at the due time |

### 7. Acceptance criteria

```gherkin
Feature: Approval routing with the delegation of authority table — the rwb-comms escalation notice

  Background:
    Given the environment is SIT
    Given delegation version "DOA-2026.11" is in force with holder "U-9201" at L6, "U-9203" at L4 and "U-9213" holding RW-HEADLIT
    Given test users "U-9211" and "U-9212" hold RW-LITOFF and test user "U-9210" holds RW-RESTRUCT
    Given the template of the escalation notice is Approved and current and carries the message ID "MSG-P7-011"

  Scenario: AC1 An escalation is told to the new approver (new, D-RCV-60)
    Given a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12"
    Given approval "A-2" for decision D7.1, area "LITIGATION", is WAITING with role RW-LITOFF and due at 09:00 on 15 December 2026
    Given the rwb-decision contract mock returns approval "A-2" re-published for case "RW-2026-000123" with decision D7.1, area "LITIGATION", route role RW-HEADLIT, escalation level 1 and due at 09:00 on 16 December 2026
    When rwb-decision publishes ApprovalRequested for "A-2" with escalation level 1 on rwb.decision.events.v1 at 09:00 on 15 December 2026
    Then one notice is written for approval "A-2" at escalation level 1 addressed to role RW-HEADLIT
    Then the notice carries the message "{decision} on case {caseNo} passed its service level and is now with you for approval." with "{decision}" = "D7.1" and "{caseNo}" = "RW-2026-000123"
    Then the notice records decision D7.1, area "LITIGATION", escalation level 1 and the new due time 09:00 on 16 December 2026
    Then the message is handed once to the ACE notification path for role RW-HEADLIT
    Then one decision record exists with decision code "D7.1", rule "R-UNI-30", approval "A-2", escalation level 1 and final call "ESCALATED"
    Then rwb.comms.NoticeGenerated.v1 and rwb.comms.NoticeDispatched.v1 are written to the outbox in the same transaction as the notice

  Scenario: AC2 The notice is readable with its recipients and its sent time (new, D-RCV-60)
    Given the notice of AC1 was written at 09:00 on 15 December 2026 and the ACE notification path accepted it at 09:00 on 15 December 2026
    Given the rwb-access contract mock returns the authorise answer allowing role RW-HEADLIT to read the notice
    When an authorised reader sends GET /api/recovery/comms/v1/notices/{noticeId} for the notice of AC1
    Then the response is status 200 with the message, recipient role "RW-HEADLIT", approval reference "A-2", decision D7.1, escalation level 1 and sent time 09:00 on 15 December 2026
    Then the response carries the template code and version and the channel that the template holds
    Then the response carries the case number "RW-2026-000123" and carries no case status, no task and no timer, which are rwb-case's
    Then no approval, no task and no case status changes in this story

  Scenario: AC3 A repeated breach gives one notice per approval and escalation level (new, D-RCV-60)
    Given the notice of AC1 exists for approval "A-2" at escalation level 1
    When the same ApprovalRequested fact for "A-2" at escalation level 1 is delivered a second time
    Then no second notice is written and no second message is handed to the ACE notification path
    When rwb-decision publishes ApprovalRequested for "A-2" with escalation level 2 and its own due time at the next breach
    Then exactly one further notice is written for "A-2" at escalation level 2, addressed to the role the approval facts name
    Then the two notices of approval "A-2" are one per escalation level and each has its own decision record

  Scenario: AC4 A level with nobody on it is never addressed (new, D-RCV-60)
    Given the L6 row for SSME has no holder and no substitute
    Given the rwb-decision contract mock returns approval "A-2" for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routed to the L5 holder at once with reason "NO_HOLDER" for L6
    When rwb-decision publishes ApprovalRequested for "A-2" for the item that passed L6
    Then no notice is addressed to L6 and no notice names a holder at L6
    Then exactly one notice is written, addressed to the covering level that received the item
    Then the routing entry that records reason "NO_HOLDER" for L6 is rwb-decision's and this story writes none

  Scenario: AC5 A withdrawn template holds the notice and sends nothing (new, D-RCV-60)
    Given the template of the escalation notice is Withdrawn on 13 December 2026 and no later version is Approved
    Given the rwb-decision contract mock returns approval "A-2" re-published for case "RW-2026-000123" with escalation level 1 and due at 09:00 on 16 December 2026
    When rwb-decision publishes ApprovalRequested for "A-2" at escalation level 1 on 15 December 2026
    Then the notice is "Held" with hold reason "TEMPLATE_WITHDRAWN" and nothing is handed to the ACE notification path
    Then MSG-P6-003 names the template code and a task is raised to the owner of the template
    Then the item stays with role RW-HEADLIT, because rwb-decision moved it and this story only notifies

  Scenario: AC6 An unavailable notification path still sends exactly once (new, D-RCV-60)
    Given the ACE notification path returns "unavailable" for the first send of the notice of AC1
    Given the rwb-decision contract mock returns approval "A-2" re-published for case "RW-2026-000123" with escalation level 1 and due at 09:00 on 16 December 2026
    When rwb-decision publishes ApprovalRequested for "A-2" at escalation level 1 and the send fails
    Then the notice exists with sent_at empty and its outbox row is pending
    Then MSG-GEN-006 naming the notification path is recorded for the failed attempt
    When the ACE notification path accepts the message on the outbox retry
    Then exactly one send happens, sent_at is the time of that send, and the notice is "Sent"
    Then no second notice is written for approval "A-2" at escalation level 1

  Scenario: AC7 The notice carries no personal data (new, D-RCV-60)
    Given the notice of AC1 and the notice of AC3 and their event payloads
    When the notice rows, the merged message, the two event payloads and the log entries of this story are inspected
    Then they carry the case number, the decision code, the approval reference, the escalation level, the role code, the user reference, the template code and dates only
    Then no name, no e-mail address, no mobile number, no national identity number and no account number appears in any of them
    Then the delivery address of the recipient is resolved by the ACE notification path and is not stored in rwb_comms
```

These seven criteria are new for the rwb-comms slice of RWB-E2-013 and are the notification criteria of the key; the values are the legacy values of RWB-E2-013 AC1, AC2 and AC11 — case `RW-2026-000123`, decision D7.1, area LITIGATION, rule `R-LIT-03` version `LIT-2026.12`, due 09:00 on 15 December 2026, escalation level 1, new due time 09:00 on 16 December 2026, roles RW-LITOFF and RW-HEADLIT, users `U-9201`, `U-9203` and `U-9213`, approval `A-2` — and no new business value is introduced. `acs` is empty for this story: no legacy criterion is owned verbatim here, because every legacy criterion of the key changes a level, an approval, a case or a decision record, and those changes belong to the other slices. The wording of MSG-P7-011 is the legacy wording with its two placeholders; the criteria assert that wording and no other.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every escalation of an approval, and every pass-up for want of a holder, is told to the approver who now has the item; the item itself is moved by `rwb-decision` and this service only notifies | REQ-APD-007; REQ-APD-011; R-UNI-30 |
| BR2 | A decision with no amount limit routes to the role named in its route parameters, for D7.1 notices RW-LITOFF, and escalates to RW-HEADLIT; both roles arrive in the approval facts and are not resolved here | REQ-APD-001; Parameters `rwb.approval.route.*`; DL22 |
| BR3 | The approver who is told must hold the A letter in the decision's capability area and be the holder or substitute of the required level, or hold the route role; the check is `rwb-access`'s and is inherited by the notice read through the guard | Permission matrix; CTL-04; DP-08 |
| BR4 | A person may not approve a decision they proposed or prepared, so a notice is never addressed to the preparer; the refusal itself is `rwb-decision`'s | Admin and access model, section 6.2; CTL-05 |
| BR5 | An approval above the caller's level is refused and sent to the level that covers it; the re-request that follows is a new approval fact and is told once | REQ-APD-004; R-UNI-15 |
| BR6 | A change from the recommendation needs a coded reason, and refuse and return need a reason; none of those answers escalates, so none produces a notice | REQ-APD-005; R-UNI-14; CTL-07 |
| BR7 | An approval not answered inside its service level escalates one level up, or to the escalation role, and the case does not move; this story tells the new approver and changes neither | REQ-APD-007; R-UNI-30; R-UNI-42 |
| BR8 | A level with no holder and no substitute passes the item one level up at once, and no notice is ever addressed to the empty level | REQ-APD-011 |
| BR9 | Levels L1 to L3 approve by committee resolution and the entry records the resolution reference, the date and the members present; the telling of a committee level is addressed to its recording holder as the approval facts name it | REQ-APD-008 |
| BR10 | The limit, the rule version and the approver are written with every approval; this story writes none of them and reads the approval level and the limit version only to carry them on its notice | REQ-APD-009 |
| BR11 | A decision that no limit covers is held and raises an incident, and no approver is named, so no notice is produced | Delegation of authority matrix, rule 8; AC14 of the legacy story |
| BR12 | An approval outcome that cannot be written to the decision log does not take effect, and a notice that cannot be recorded does not exist: the notice row, its decision record and its outbox rows commit together or not at all | Principle 5; R-UNI-39 |
| BR13 | One notice per approval and per escalation level: the inbox dedupe and the unique key of the notice kind, the approval reference and the escalation level make a second notice for the same level impossible | This story; R-UNI-40 |
| BR14 | The message text is the template's and not the code's: MSG-P7-011 is the message ID, the template carries the wording and the two placeholders, and a withdrawn template holds the notice | FSD P6 v3 VR-P6-001-1; BR-P6-001; R-LIT-04 |
| BR15 | The channel of the notice is a value of LOV-CHANNEL on the template row and the send goes through the ACE notification path; no channel, template code or notice state is written in code | Architecture v5 slide 17; TSD P6 v2 T3.1 and T3.2; BR-P6-001 |
| BR16 | The notice and its send facts are `rwb_comms` rows; no other service reads them and this service reads no other service's table, no `approval` row and no `delegation_limit` row | Architecture v5 slide 41; DP-01 |
| BR17 | No personal data in the notice, the template merge values, the events, the trail or the logs: role codes, user references, the case number, the decision code and dates only, and the delivery address is the path's | Template and Rules §R7.2 s17; Architecture v5 slides 42 and 43 |
| BR18 | When the notification path is unavailable the notice is kept with `sent_at` empty and the outbox retries; the retry that succeeds sends once and sets `sent_at` once | DP-09; FSD P6 v3 AC-EXC-P6-003-03 and AC-EXC-P6-008-03 |

### 9. State transitions

The states below are the states of a notice of this story. The approval, the task, its timer and the case are not state of this service and are named only so the boundary is visible.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | ApprovalRequested arrives with escalation level 1 or more | The template is Approved and current and the facts name a covering role or holder | Generated, with `sent_at` empty and the outbox row written |
| Generated | The ACE notification path accepts the message | The path answers accepted | Sent, with `sent_at` set and `NoticeDispatched` published |
| Generated | The path returns unavailable | The answer is unavailable | Generated, with `sent_at` still empty, the error recorded and the outbox row pending |
| Generated | The outbox retry succeeds | The path accepts on a retry | Sent, with `sent_at` set once and one send only |
| Absent | ApprovalRequested arrives with escalation level 1 or more | The template is Withdrawn, or no version is Approved on the date | Held with hold reason `TEMPLATE_WITHDRAWN`, with no send |
| Held | A later version of the template is Approved, and the fact is the same level | The one-notice-per-level key has no notice for that level in Sent | Generated, and then Sent on the same run |
| Absent | ApprovalRequested arrives with escalation level 0 and names no covering role or holder | The item was held with no limit, or the facts name nobody | Absent: no notice is produced |
| Any | A repeat of the same approval reference and escalation level | The inbox or the unique key holds the notice | Unchanged: no second notice and no second send |

The approval itself moves WAITING to WAITING with the next level or the escalation role, and the case stays `WAITING_APPROVAL`; both are `rwb-decision`'s and `rwb-case`'s and this story changes neither (BR1, BR7).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-HEADLIT, Head of Litigation, and RW-LITOFF, litigation officer | Receive the notice of a D7.x item at the role the approval facts name, and read it with its recipient role and its sent time |
| Holders and substitutes of levels L4 to L6, named by `rwb-decision` | Receive the notice of a limit-based item that escalated to their level |
| Recording holder of levels L1 to L3 | Receives the notice of a committee level; the resolution and its members present stay `rwb-decision`'s |
| A role with the Litigation right R and the case in scope | Reads a notice through `GET /api/recovery/comms/v1/notices/{noticeId}`, as API-P6-002 fixes the access |
| A role with the Case record right C and the case in scope | Asks for a notice with `POST /api/recovery/comms/v1/cases/{caseId}/messages`, as API-P6-008 fixes the access |
| The `rwb-comms` service identity | Consumes the escalation fact, reads its own `rwb_comms` rows, writes the notice and the outbox, and hands the message to the ACE notification path (DP-02) |
| The decision-record library identity | Writes the local decision record of the notice and publishes it on `rwb.decision-record.v1` (DP-03) |
| RW-AUDIT | Reads the notice fact through the decision record; it calls no operation of this story |
| `rwb-decision` | Owns the router, the `ApprovalWorkflow`, the escalation and the item's move; this story has no authority over any of them |

The authorisation decision is taken by `rwb-access` (Recovery roles as data, scope and masking in `rwb_access`) and is consumed as the cached permission decision that the guard library of DP-08 holds; the refusal shape stays 403 with MSG-P4-002 and 404 with MSG-P4-003. The escalation roles are parameter rows of `rwb-case` read by `rwb-decision`; this story neither holds nor resolves them. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1220; ASM-2178); the story refers to "the rwb-comms login (DP-02)".

### 11. Data

| BR Field ID | Entity in `rwb_comms` | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | `notice` | id | Write |
| DF-LEG-016 | `notice` | case_id | Write |
| DF-LEG-018 | `notice` | notice_type (the notice kind of this story) | Write |
| DF-LEG-019 | `notice` | sent_date | Write on the acceptance of the send |
| DF-LEG-030 | `notice` | party_id | Not written: an approver is a role and a user reference, never a party |
| DF-LEG-031 | `notice` | template_id | Write |
| DF-LEG-032 | `notice` | hold_reason | Write on a held notice |
| DF-LEG-034 | `notice` | dispatch_attempts | Write on every send attempt |
| (assumed column) | `notice` | approval_ref, escalation_level, recipient_role, recipient_user_ref, template_code, template_version, sent_at, message_text | Write; the columns are Not specified in the source documents (GAP-1222; ASM-2180) |
| DF-REF-045 to DF-REF-051 | `template` | id, template_code, template_version, language, body_ref, approved_by_legal | Read |
| DF-REF-065, DF-REF-066, DF-REF-067 | `template` | valid_from, channel, notice_type | Read |
| DF-REF-252 to DF-REF-260 | `merge_field` | merge_code, source_entity, source_field, field_id, is_required, personal_data, catalog_version, valid_from | Read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | decision code, rule, approval reference, escalation level, final call, decided at, hash chain | Write |
| DF-DEC-032 to DF-DEC-053 | `approval` (P7) | approval reference, case, decision code, capability area, route role, approval level, limit version, status, due time, escalation level | Read through the `rwb-decision` contract, never a table |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_comms` | the `NoticeGenerated`, `NoticeDispatched`, `DecisionRecorded` and send rows | Write |

No row of `approval`, `decision_log_entry` or `delegation_limit` is copied into `rwb_comms`: the approval is `rwb-decision`'s (P7) and the delegation table is `rwb-access`'s (P4), and their fields arrive only as facts in the approval event and in the approval read. No row of `recovery_case`, `task`, `timer` or `queue` is read or written. Field IDs are those in the Logical Data Model and Data Dictionary v9; the notice columns this story needs for the escalation kind have no field ID in TSD P6 v2 T3.1 and are written from the assumed shape of section 12.1, which is Not specified in the source documents (GAP-1222; ASM-2180).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-comms` (P6); base `/api/recovery/comms/v1`. Both paths are the ones the legacy module and TSD P6 v2 T-A.1 carry (API-P6-002 and API-P6-008); this story fills the notice with the escalation kind and adds no third path. The request and response field set of the escalation notice is Not specified in the source documents (GAP-1222; ASM-2180).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/notices/{noticeId}` | API-P6-002: read a notice with its message, its recipient role, its approval reference, its escalation level, its template and its sent time; 200 with the Notice | Litigation, right R, scope applied through the guard of DP-08 | Not applicable, read only |
| POST | `/cases/{caseId}/messages` | API-P6-008: produce the escalation notice for the approval facts of the request and hand it to the ACE notification path; 202 with the notice reference | Case record, right C, scope applied | Idempotency-Key header, kept 24 hours |

The Notice body carries `id`, `caseId`, `caseNo`, `noticeKind` (`ESCALATION`), `approvalRef`, `decisionCode`, `capabilityArea`, `escalationLevel`, `recipientRole`, `recipientUserRef`, `templateCode`, `templateVersion`, `channel`, `messageText`, `state` and `sentAt`. The MessageRequest body carries `approvalRef`, `escalationLevel`, `recipientRole`, `recipientUserRef`, `templateCode` and `channel`.

Errors: 401 no session; 403 the role lacks the right (MSG-P4-002); 404 the notice or the case is absent or out of scope (MSG-P4-003); 409 the template is withdrawn (MSG-P6-003) or the level was already notified, in which case the first notice is returned with 200; 422 a required field is missing (MSG-GEN-001); 503 the decision was not recorded (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set.

The notice kind `ESCALATION`, the state values and the hold reason `TEMPLATE_WITHDRAWN` are values of the reference lists of DP-07 and of this service's own vocabulary, not constants of the code; the value sets are Not specified in the source documents (GAP-1220; ASM-2178).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/approvals/{approvalId}` | P7 rwb-decision, on RWB-P7-E2013-CON | The approval facts the notice is rendered from: case, decision code, capability area, route role or holder, approval level, limit version, escalation level, due time and status; faked, one hop, 2 s timeout (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access, on RWB-P4-E1037-CON | The cached role, scope and right decision behind the notice read and the message request (DP-08); faked |

The parameters contract of `rwb-case` (DP-06, RWB-P3-E1042-CON) and the reference-data contract of `rwb-case` (DP-07, RWB-P3-E1043-CON) are read in process through their client libraries and not over REST; the escalation role and the new due time arrive in the approval facts and are never resolved here. The contract dependency recorded on the story is RWB-P7-E2013-CON; the platform and published contracts the DP table adds are listed in section 13 and carried in the gap of GAP-1223.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` (EV-13) | `rwb.comms.events.v1` | P6 | caseId | notice ID, case ID, case number, notice kind `ESCALATION`, decision code, approval reference, escalation level, template code and version, recipient role, generated at |
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | P6 | caseId | notice ID, case ID, notice kind, approval reference, escalation level, recipient role, channel, sent at |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library, published by this service | entryId | the hash-chained record of the notice: decision code D7.1, rule R-UNI-30, approval reference, escalation level, final call ESCALATED, decided at |

All three are written to the outbox in the same transaction as the notice and relayed with the CloudEvents 1.0 envelope by the outbox relay of the platform (DP-09). `NoticeGenerated` is consumed by `rwb-decision` and `NoticeDispatched` by `rwb-reporting`, as the event catalogue names them (Architecture v5 slide 42). No event carries a name, an e-mail address, a mobile number or an account number.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision.ApprovalRequested.v1` (EV-09) | `rwb.decision.events.v1` | P7 rwb-decision | `EscalationNoticeListener`: inbox dedupe by event ID, then `EscalationNoticeService` for the escalation level and the covering role the event names |

The escalation reaches this service as the same `ApprovalRequested` event re-published with the escalation level raised by one and the new due time, and a pass-up for want of a holder reaches it as the same event with reason `NO_HOLDER` and the covering level. No `ApprovalEscalated` event is invented and `TimerBreached` (EV-19) stays a legacy reference, because the breach is now a durable timer inside the approval workflow; this reading is the assumption of ASM-2179 and the conflict it settles is GAP-1221.

#### 12.5 Workflows and activities

None of this story's own. The handler is a Kafka consumer with the inbox of DP-09 and not a workflow; the durable service level timer that breaches is `ApprovalWorkflow`'s on `rwb-decision` and is neither started nor signalled here; the send retry is the outbox relay's and not a workflow retry. The `Notify` and `Approval` templates of the workflow kit stay on the queue of the service that runs them, and this story registers nothing on the `rwb-comms` queue.

#### 12.6 Schedules

None. The escalation clock is a durable timer inside `ApprovalWorkflow` on `rwb-decision` and JOB-05 is a legacy reference only; this story starts no Schedule and polls nothing.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `notice` | P6 (`rwb_comms`) | The escalation notice, its recipient, its approval reference, its escalation level, its send state and its send time |
| `template` | P6 (`rwb_comms`) | Read only: the template of the escalation notice, its version, its channel and its state |
| `merge_field` | P6 (`rwb_comms`) | Read only: the merge catalogue the message is rendered from |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The record of the notice and its final call ESCALATED (DP-03) |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_comms` | Outbox, inbox and idempotency objects (DP-09) |

Not owned and never read: `approval` and `decision_log_entry` (P7), `delegation_limit`, `role` and `permission` (P4), `recovery_case`, `task`, `timer` and `parameter_value` (P3). The approval arrives on its contract, the authorise answer on the guard, and the parameters and the reference lists in process; no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision approval WireMock | RWB-P7-E2013-CON | Approval "A-2" for case `RW-2026-000123` at D7.1, area LITIGATION; the re-published request for "A-2" with escalation level 1, role RW-HEADLIT and due 09:00 on 16 December 2026; the same fact replayed; escalation level 2; the SSME item routed to L5 with reason `NO_HOLDER`; a held item with no approver named; the approval read for the same approval |
| rwb-access authorise fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The allow answer for role RW-HEADLIT, the refusal for a role without the Litigation right, and a notice of a case out of scope |
| decision-record fake | RWB-PLT-E1027-CON | The record append and the hash chain, and a forced failure for the 503 case |
| reference-data and parameters fakes | RWB-P3-E1043-CON, RWB-P3-E1042-CON | LOV-CHANNEL, LOV-NOTICE and the notice state and template state lists with their versions; the template of the escalation notice Approved and then Withdrawn for AC5; the route and escalation role rows of the D7.1 decision |
| ACE notification path stub | The platform path of Architecture v5 slide 17 | Accepted for AC1; unavailable for the first attempt of AC6 and accepted on the retry; a repeated accept of the same message refused by the path's own idempotency |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 2 | `GET /notices/{noticeId}` and `POST /cases/{caseId}/messages` provided; the approval read and the authorise decision consumed, one hop and 2 s |
| Kafka | Published 3 event types, consumed 1 | `rwb.comms.events.v1` and `rwb.decision-record.v1` published; `rwb.decision.events.v1` consumed |
| Temporal | None | The timer is `ApprovalWorkflow`'s on `rwb-decision`; this story registers no workflow, activity or Schedule |
| File | None | No file input and no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `notices/escalation`, Java package `th.co.scb.ace.workbench.recovery.comms.escalation`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy in-process call this slice replaces is the monolith's telling of the new approver inside `ApprovalEscalationListener`; under DP-11 that becomes a published notice fact and a template, and the mockable boundary is the approval contract RWB-P7-E2013-CON plus the ACE notification path stub. DP-10 is where the escalation clock went: JOB-05 and its `TimerBreached` become the durable timer of `ApprovalWorkflow` on `rwb-decision`, so this story runs no Schedule and no workflow of its own and the DP-10 row is carried by the P7 slice. DP-08 is the guard the notice read inherits: the read carries the Litigation R right, the message request the Case record C right, and the cached permission decision comes from the guard library against the authorise contract. DP-19 is not built here: no screen is served by this story, because the notice reaches the approver through the ACE notification path of slide 17 and the approval queue SCR-10 is `rwb-decision`'s; the approver's work list is served by the gateway-bff composite route of RWB-PLT-N001-CON and this story adds no route to it (ASM-2187). DP-06 and DP-07 are read in process and never resolved into a level, a limit or a holder by this service.

The platform H dependencies of the DP table and the C dependencies of the published contracts of other services are not in the plan's H and C lists for this story, which name None and RWB-P7-E2013-CON; they are the dependencies the DP table adds and they are recorded in GAP-1223 and ASM-2181. None of them blocks the build beyond Day 1: they are platform contracts of waves 0 and 1 and the platform's published contract of `rwb-access`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| EscalationNoticeListener | Kafka consumer with the inbox | Reads `ApprovalRequested`, deduplicates by event ID, and hands the approval facts to the notice service |
| NoticeController | Controller | `GET /notices/{noticeId}` with the guard, the scope and the problem mapping for 401, 403, 404 and 503 |
| MessageController | Controller | `POST /cases/{caseId}/messages` with the Idempotency-Key, the validation and the 202 answer |
| EscalationNoticeService | Service | Decides whether a fact is a telling, orders the template read, the render, the hold, the record and the outbox in one transaction, and enforces one notice per approval and escalation level |
| TemplateCatalog | Service | Reads the template of the escalation notice, its version and its channel, and the reference lists of DP-07 with the version in force; refuses a Withdrawn template with MSG-P6-003 |
| MergeFieldResolver | Service | Renders the message from the template and the merge fields, with `{decision}` and `{caseNo}` taken from the approval facts and no other value |
| ApprovalFactClient | Adapter | The approval read of RWB-P7-E2013-CON, one hop with a 2 s timeout and a breaker |
| AccessCheckClient | Client | The cached authorise decision of DP-08 behind the two operations |
| NotificationPathClient | Adapter | Hands the merged message to the ACE notification path for the recipient role, with the path's idempotency key, and maps the answer to accepted or unavailable |
| NoticeRepository | Repository | `notice` in `rwb_comms`, with the optimistic lock and the unique key of the notice kind, the approval reference and the escalation level |
| DecisionRecordWriter | Service | Writes the local decision record and its outbox row in the same transaction as the notice (DP-03) |

**Database and migrations**

- Writes `notice`, the local decision record and the library objects, all in schema `rwb_comms`; reads `template` and `merge_field` and no other schema.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V2013_1__comms_escalation_notice.sql` adds the notice columns of section 11 that the baseline of RWB-P6-E1046-APP and RWB-P6-E1052-APP does not hold — the approval reference, the escalation level, the recipient role and user reference, the template code and version, the message text and `sent_at` — plus the unique key `ux_notice_escalation ON notice (approval_ref, escalation_level, notice_type) WHERE notice_type = 'ESCALATION'`, so one notice per approval and level is a constraint and not only a check (BR13).
- Update the notice with `WHERE id = ? AND version = ?`; zero rows updated means the record changed (MSG-GEN-004).
- No row of `template` or `merge_field` is written here: the template catalogue and the template approval are RWB-P6-E1046-APP and RWB-P6-E1052-APP.

**Configuration and reference data**

- The template code of the escalation notice is a row of this service's `template` catalogue with the message ID MSG-P7-011, the two placeholders and the channel; the code and the channel value are Not specified in the source documents (GAP-1220; ASM-2178).
- LOV-CHANNEL, LOV-NOTICE and the template and notice state lists are read through the reference-data contract of DP-07 with the version in force (RWB-P3-E1043-CON); no channel, state or notice type is a constant in code.
- The escalation roles are parameter rows of `rwb-case` (`rwb.approval.route.D7.1.role`=RW-LITOFF, `rwb.approval.route.D7.1.escalation-role`=RW-HEADLIT, `rwb.approval.route.D7.1.service-level`=1 working day, assumed; DL22), read by `rwb-decision` through DP-06 and received here in the approval facts; this story holds no default and resolves no level.
- The outbox retry policy is the platform's (RWB-PLT-TE006-CON); the retry limit and the backoff are Not specified in the source documents (GAP-1220; ASM-2178), and the retry behaviour this story assumes is that of ASM-2186.
- The template owner who receives the MSG-P6-003 task on a withdrawal is Not specified in the source documents (GAP-1220; ASM-2178).

**Build steps**

1. `NoticeRepository` and the migration, with the unique key of the notice kind, the approval reference and the escalation level; test that a second notice for the same level is refused by the constraint.
2. `EscalationNoticeListener` with the inbox, the dedupe by event ID and the decision of what is a telling; tests for AC3 and AC4 and the not-a-telling cases of X4 and X10.
3. `TemplateCatalog`, `MergeFieldResolver` and the render of MSG-P7-011 with `{decision}` and `{caseNo}`; tests for AC1 and AC5.
4. `DecisionRecordWriter` and the fail-closed transaction: a failed record leaves no notice and no outbox row and the event is redelivered; tests for AC1 and TC-E2-013-16.
5. `NotificationPathClient` and the outbox send path: accepted sets `sent_at`, unavailable keeps the notice with `sent_at` empty and the send happens once on the retry; tests for AC6.
6. `NoticeController` and `MessageController` with the guard of DP-08, the scope, the Idempotency-Key and the error mapping; tests for AC2 and TC-E2-013-15.
7. `ApprovalFactClient` over the approval read with the 2 s timeout and the breaker, and the contract-fake run of the whole fact in isolation before the approval story is live.
8. The privacy test: the notice, the merged message, the two event payloads and the log entries carry no name, e-mail address, mobile number, national identity number or account number; test for AC7.

**Feature switch.** `rwb.comms.escalation-notice`, read as a parameter through DP-06: off means the listener consumes the fact into the inbox and writes no notice and sends nothing, while the approval, its escalation and its move keep running in `rwb-decision`; the switch never blocks the approval itself. The legacy flag `rwb.decision.approval-routing` stays a legacy reference and is the P7 slice's.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P7-E2013-CON stay green, and a SIT day shows one notice per escalated approval and escalation level, one send with `sent_at` set, no notice addressed to a level with nobody on it, a held notice with MSG-P6-003 for a withdrawn template, one send after the retry when the path was unavailable, and no personal data in any notice, event or log.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-011 | An item escalates, or a level passes it up for want of a holder | {decision} on case {caseNo} passed its service level and is now with you for approval. | This story, in the template and the merged notice |
| MSG-P6-003 | The template of the escalation notice is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. | This story, on the held notice |
| MSG-GEN-006 | The notification path is unavailable, or a merge value is absent | Not specified in the source documents (GAP-1220; ASM-2178) | This story, on the send and the render |
| MSG-P7-003 | The local decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the notice transaction |
| MSG-P4-002 | The role holds no right for the notice read or the message request | You cannot {action} here. Your role does not include it. | This story, through the guard of DP-08 |
| MSG-P4-003 | The notice or the case is outside the caller's scope | This case is not in your scope. | This story, through the guard of DP-08 |

MSG-P7-011 and MSG-P6-003 are copied unchanged from the legacy story and FSD P6 v3 VR-P6-001-1; MSG-P7-003, MSG-P4-002 and MSG-P4-003 are the platform messages the authorise contract and the decision-record library carry. The text of MSG-GEN-006 is named by the P6 extracts for an unavailable path and is not written out in any source this story may read, so the placeholder stands. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. The escalation notice reaches the approver through the ACE notification path of Architecture v5 slide 17 and is read through the operation of section 12.1; the approval queue SCR-10 and the decision screen SCR-11 are `rwb-decision`'s, and the gateway-bff composite route of DP-19 is not extended by this story.

| Where | State | What the approver sees |
|---|---|---|
| The notification path | Sent | The merged message naming the decision and the case, in the channel the template holds |
| The notice read | Sent | The message, the recipient role, the approval reference, the escalation level, the template and the sent time |
| The notice read | Generated, `sent_at` empty | The notice is recorded and the send is pending; nothing has reached the approver yet |
| The notice read | Held, `TEMPLATE_WITHDRAWN` | The hold reason and MSG-P6-003; nothing was sent, and the item is already with the new approver |
| SCR-10 Approval queue (P7) | List | The escalated item itself, with decision, case, amount, level, limit version and the new due time; this story feeds none of that screen's fields |

The screen field list, the composite route specification and the field-level masking belong to RWB-PLT-N001-CON and to the stories that own each screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-013-01 | AC1, BR2 | Component | Synthetic demand notice under R-LIT-03; the routing and the routed role are the rwb-decision contract fake's |
| TC-E2-013-02 | AC1, AC3, BR7 | Component | Approval timer breached at 09:00 next day; one notice at escalation level 1 and one at level 2 |
| TC-E2-013-03 | AC1, BR1 | Contract | Delegation versions DOA-2026.11 and DOA-2027.01; the version is a fact of the approval read, not a lookup here |
| TC-E2-013-04 | AC2, BR1 | Component | D6.4 Mortgage at 2.4 million baht; the recipient role and the sent time on the notice read |
| TC-E2-013-05 | AC2, BR3, BR10 | Contract | L6 holder approving; the approval level and the limit version on the notice, and the guard on the read |
| TC-E2-013-06 | AC1, BR4 | Contract | Preparer who is also a substitute; the notice is addressed to the routed role and never to the preparer, and the refusal is the contract fake's |
| TC-E2-013-07 | AC1, BR5 | Contract | Principal changed to 120 million baht; the covering level is a fact of the re-published request |
| TC-E2-013-08 | AC1, BR6 | Contract | Refuse without and with a reason; neither answer escalates, so no notice is produced |
| TC-E2-013-09 | AC1, BR6 | Contract | Return with a question; no escalation and no notice |
| TC-E2-013-10 | AC1, BR6 | Contract | Change without a reason code; the refusal is the contract fake's and no notice follows |
| TC-E2-013-11 | AC4, BR8 | Component | SSME L6 row with no holder; one notice to the covering level and none to L6 |
| TC-E2-013-12 | AC2, BR9 | Contract | L3 committee approval with resolution PARC-2026-14; the notice read names the recording holder as the approval facts name it |
| TC-E2-013-13 | AC3, BR12 | Contract | Holder and substitute at once; the inbox dedupe and the one-notice-per-level key give one notice |
| TC-E2-013-14 | AC4, BR11 | Component | Hire purchase with no delegation rows; the held item names no approver and takes no notice |
| TC-E2-013-15 | Access | Component | A role without the Litigation right reads the notice and is refused with MSG-P4-002; a notice out of scope is 404 with MSG-P4-003 |
| TC-E2-013-16 | Principle 5 | NFR | The decision-record write forced to fail on an escalation notice; no notice, no outbox row and no send, and the event is redelivered |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The whole legacy set is kept because the rwb-comms slice carries the key's notification evidence; the tests whose rule lives in `rwb-decision`, `rwb-access` or `rwb-case` use this story's notice assertions and the contract fake for the rest. The `-ITG` copies are RWB-ITG-E2013-ITG and are not written here.

### 17. Guardrails

- No business value in code: the template code, the channel, the message text, the escalation roles, the levels and the due times are template rows, reference-data rows or parameters of another service; nothing of them is a constant here.
- No personal data in the notice, the template merge values, the events, the workflow inputs, the trail, the tests or the prompts: role codes, user references, the case number, the decision code, the approval reference and dates only, and the delivery address is resolved by the ACE notification path and never stored.
- No read of another service's tables (DP-01): the approval arrives on its contract, the authorise answer on the guard, the reference lists and parameters in process; no `approval`, `decision_log_entry`, `delegation_limit`, `recovery_case`, `task` or `timer` row is copied into `rwb_comms`.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all.
- One notifier and no mover: this story changes no approval, no task, no timer and no case status; the item, its case and its due time stay with `rwb-decision` and `rwb-case`, so a notice can never move a case.
- No notice without its record: the notice, its decision record and its outbox rows commit in one transaction, and a failure changes nothing and leaves the event for redelivery (R-UNI-39).
- One notice per approval and escalation level: the inbox dedupe and the unique key make a second notice and a second send impossible, and the notification path's own idempotency protects the retry.
- One base, one topic, one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; no story in this key declares another service's base or topic as its own (DP-13, DP-14).
- One hop and 2 s on every call, with a breaker per downstream; a missing answer never produces a notice from a guessed level or role (DP-11).
- The switch removes the notification without a schema rollback and never blocks the approval itself.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-001 | Route to the approver named by the delegation table | Epic 2, 3.7; Program, 5.7 | FEAT-APD-01, FEAT-APD-10 | 17 Run the decision center | BR2 | TC-E2-013-01, TC-E2-013-04 |
| REQ-APD-003 | Accept, change, reject or return, each recorded | Epic 2, 3.7; Program, 5.7 | FEAT-APD-02, FEAT-APD-03, FEAT-APD-04 | 17 Run the decision center | BR6 | TC-E2-013-05, TC-E2-013-08, TC-E2-013-09 |
| REQ-APD-004 | Above the limit refused and raised, no silent approval | Epic 2, 3.7; Program, 5.7 | FEAT-APD-05 | 17 Run the decision center | BR5 | TC-E2-013-06, TC-E2-013-07 |
| REQ-APD-005 | Override needs a coded reason | Epic 2, 3.7; Program, 5.7 | FEAT-APD-07 | 17 Run the decision center | BR6 | TC-E2-013-10 |
| REQ-APD-007 | Unanswered approval escalates to the named role | Epic 2, 3.7; Program, 5.7 | FEAT-APD-06 | 17 Run the decision center | BR1, BR7 | TC-E2-013-02 |
| REQ-APD-008 | Committee decision recorded with members present | Epic 2, 3.7; Program, 5.7 | FEAT-APD-07 | 17 Run the decision center | BR9 | TC-E2-013-12 |
| REQ-APD-009 | Limit, rule version and approver written with every approval | Epic 2, 3.7; Program, 5.7 | FEAT-APD-11 | 17 Run the decision center | BR10, BR12 | TC-E2-013-05, TC-E2-013-13, TC-E2-013-16 |
| REQ-APD-010 | Open items keep the delegation version they were decided under | Epic 2, 3.7; Program, 5.7 | FEAT-APD-10 | 17 Run the decision center | BR3 | TC-E2-013-03, TC-E2-013-14 |
| REQ-APD-011 | Routing escalates rather than stalls with no person in a role | Epic 2, 3.7; Program, 5.7 | FEAT-APD-06 | 17 Run the decision center | BR8 | TC-E2-013-11 |

| Legacy reference | Where it is kept |
|---|---|
| The new approver is told on a service level breach, with MSG-P7-011 | Sections 1, 2, 4, 7, 14 |
| The one-level pass-up for want of a holder, and its message | Sections 4, 5, 7 (AC4), 8 (BR8) |
| Escalation level 1, the new due time, roles RW-LITOFF and RW-HEADLIT, users U-9201, U-9203 and U-9213, approval A-2 | Background and AC1 of section 7 |
| MSG-P6-003 and the withdrawn template hold | Sections 4, 5, 7 (AC5), 14 |
| MSG-P7-003, MSG-P4-002, MSG-P4-003, MSG-GEN-006 | Section 14, exception paths |
| Rule IDs R-LIT-04, R-UNI-30, R-UNI-39, R-UNI-40, R-UNI-42, CTL-04, CTL-05 | Sections 2, 4, 5, 8, 9 |
| Legacy key RWB-E2-013, story RWB-P6-E2013-APP, contract RWB-P7-E2013-CON | Metadata, sections 3, 12 |
| Test cases TC-E2-013-01 to TC-E2-013-16 | Section 16 |
| Decoupling patterns DP01, DP03, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-P7-E2013-APP and RWB-P7-E2013-CON the router, the `ApprovalWorkflow`, the endpoints and the decision records; RWB-P3-E2013-APP the case status, the approval task and the timer; RWB-P4-E2013-APP the authorise answer; RWB-P4-E1038-APP the delegation table as versioned data; RWB-P3-E1028-APP the service levels, timers and escalation; and RWB-ITG-E2013-ITG the cross-service harness.

### 19. Out of scope

- The router, the `ApprovalWorkflow` of the workflow kit, the approve, refuse and return operations, the approval queue SCR-10, the item's move, the escalation entry and the approval's decision records: RWB-P7-E2013-APP, with the contract, the event schemas and the fakes in RWB-P7-E2013-CON, and the deployment in RWB-P7-E2013-OPS.
- The case status `WAITING_APPROVAL`, the decision task, the preparer task and the timer projection on the case: RWB-P3-E2013-APP.
- The delegation of authority table as versioned data, its load, its approval and its rollback: RWB-P4-E1038-APP.
- The authorise answer and the A letter behind the notice read and the message request: RWB-P4-E2013-APP, and the guard and authorise contract RWB-P4-E1037-CON.
- The service levels, the timers and the escalation clock: RWB-P3-E1028-APP. JOB-05 and `TimerBreached` are legacy references only.
- The route and escalation role parameters and the capability area per decision code, which are `rwb-case` parameter rows under the R-PREC default ruling.
- The template catalogue, the template approval and the withdrawal of a template version: RWB-P6-E1046-APP and RWB-P6-E1052-APP. This story reads the template and the merge fields and writes neither.
- The customer-facing SMS, LINE and letter dispatch with proof of delivery: RWB-P6-E2021-APP and RWB-P6-E2022-APP. This story's channel is the internal notification of an approver and not a customer contact.
- The gateway-bff composite route, the officer inbox push and the screens: RWB-PLT-N001-CON, with the approval queue in `rwb-decision` and the decision screen SCR-11 in RWB-E2-014.
- The integration harness and the `-ITG` copies of the test cases: RWB-ITG-E2013-ITG.
- The committee pack screen SCR-12 (Epic 4), the recommendation read (Epic 4) and the monthly override reason report (Epic 8).
- The names of level holders and substitutes (DL18) and the service level values (DL22), which are data of their owners.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: an OPS story of this legacy key.
