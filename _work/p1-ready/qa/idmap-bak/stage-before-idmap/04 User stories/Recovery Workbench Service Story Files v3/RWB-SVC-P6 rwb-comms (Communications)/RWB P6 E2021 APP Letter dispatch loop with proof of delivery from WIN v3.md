# RWB-P6-E2021-APP Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Proof results are read on `GET /proof-of-delivery?businessDate=` of rwb-source-data, which writes nothing, and rwb-comms appends the proof entry; they are no longer rows of rwb-integration or of an unnamed path (RD-P1-007; findings #1, #3).
- The three ledger entries (dispatch, held, proof) are specified on the case-scoped append with headers, keys, answers and failure handling (RD-P1-001, RD-P1-007; findings #2, #5).
- The consent fact is named as the DP02 records read, and the fakes are the rwb-source-data provider fake 5.1.0 (RD-P1-005, RD-P1-011; findings #4, #6).
- RD-P1-041 changes no criterion: this story reads no freshness status of its own.
- Pending: proof read timing (GAP-2096), the decision point (NEW-GAP-F14-5), second pod rows (NEW-GAP-F14-8), a row with no callback date (NEW-GAP-F14-9) and the WIN status mapping (NEW-GAP-D3). The dispatch and delivery reference and keys are ruled (RD-P1-064; NEW-GAP-S10-16 and NEW-GAP-F14-2 closed).
- Finishing pass: ledger entries follow RD-P1-064 (barcode reference, `LETTER` keys, sole appender); test case IDs of Test Cases v9 applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

| Item | Value |
|---|---|
| Story key | RWB-P6-E2021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-021 |
| Legacy disposition | Split (rework) |
| Size | Sized by the squad at refinement; not specified in the source documents (DOR-RWB-P6-E2021-APP-16) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Readiness decisions | RD-P1-001; RD-P1-005; RD-P1-007; RD-P1-011; RD-P1-041, RD-P1-064 |
| Parallel lane | L-P6-A |
| Ready to start | After RWB-P6-E1052-APP, RWB-P6-E1055-APP |
| Dependency state | Not done: RWB-P6-E1052-APP and RWB-P6-E1055-APP (build) and RWB-P6-E2021-OPS (external); the build waits for them |
| Depends on (build) | RWB-P6-E2021-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P6-E1052-APP, RWB-P6-E1055-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P7-E2014-CON, RWB-P1-E1066-CON, RWB-P1-E1055-APP, RWB-P1-E2021-APP; rwb-source-data.yaml 5.1.0 (API Specification v7) with provider fake 5.1.0 |
| Contract version | Consumed P1 contract rwb-source-data.yaml 5.1.0; version of the rwb-comms contract Not specified in the source documents (DOR-RWB-P6-E2021-APP-23) |
| Integration dependencies | rwb-integration: transport and retry of the JOB-10 WIN file (GAP-2106) |
| External dependencies | RWB-P6-E2021-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-010, FR-P6-013, FR-P6-015, FR-P6-016, FR-P6-017, FR-P6-018, FR-P6-019, FR-P6-020, FR-P6-021, FR-P6-022, FR-P6-027, FR-P6-028, FR-P6-029, FR-P6-030, FR-P6-031, FR-P6-036) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-021 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E2021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 40 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, proof-of-delivery read, ledger entries, consent read and fakes aligned with RD-P1-001, 005, 007 and 011. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **every approved notice of rwb-comms checked against the conduct rules, written to the WIN dispatch file through the integration service, served from the proof of delivery returned for its barcode, and readable on the rwb-comms contract with its dispatch and its proof**, so that **the notice period is counted from proof of delivery and not from printing, and a letter is never written to a WIN file while a contact stop or a legal hold is in force**.

### 2. Business rationale

A notice period counted from the print date can be challenged, and a letter sent to a customer under a contact stop is a conduct breach. In the target that loop is not one monolith transaction: rwb-comms owns the notice and its dispatch facts in `rwb_comms`, rwb-case owns the legal hold, the case scope, the queue transfer and the NOTICE_PERIOD timer, rwb-deviation owns the contact stop of X1 and X2, rwb-decision owns the approval and the central decision ledger, rwb-source-data owns the interaction ledger, rwb-document owns the letter body, and rwb-integration owns the WIN file window and the file runs (Architecture v5 slides 17, 41 and 44; TSD P6 v2 T1 and T5.1). The conduct check therefore reads facts from four owners on their contracts and writes its result through the local decision-record library, and the dispatch and delivery facts are published so that the case, the reporting read model and the ledger follow without a table read.

This story is the rwb-comms app slice of legacy RWB-E2-021 and it owns the eight legacy criteria that the service itself can satisfy: AC3 undelivered, AC6 proof window expires, AC7 legal hold, AC8 template withdrawn, AC9 decision log write fails, AC10 repeated request, AC11 notice outside the caller's scope and AC12 notice type missing. Legacy AC1 (dispatch), AC2 (proof back), AC4 (contact stop blocks the letter) and AC5 (consent withdrawn does not stop a statutory notice) are end-to-end journeys across five services and belong to `RWB-ITG-E2021-ITG`; they are named in section 19 and are not copied here.

The decoupling is the one the target fixes: the notice, the dispatch file reference and the proof dates are `rwb_comms` rows (DP-01); the decision record goes through the local library and the shared topic (DP-03); the proof facts of ACE reach this service through the owner's contract and never through a `v_ace_*` read of our own (DP-05); the statutory notice type list, the delivery-result codes and the eligible states are reference data of rwb-case (DP-07); the dispatch and delivery facts are published to the outbox in the same transaction (DP-09); the 16:00 run is a Temporal Schedule and a workflow, not a Quartz row (DP-10); every cross-service call is one hop with a 2 s budget (DP-11); the base is `/api/recovery/comms/v1` (DP-13); the ledger entry is rwb-source-data's and is written through its contract (DP-18); and the screens reach the answer through the gateway-bff composite route (DP-19). It serves REQ-OCC-003, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010, carries CTL-15 and CTL-16, and gives the FSD P6 measure "notices with proof of delivery, 100 percent" its service-side evidence.

### 3. Preconditions

- RWB-P6-E1052-APP is done: the notice is generated from an approved template, the `notice` row exists with `notice_type`, `template_id`, `party_id` and `document_id`, and NoticeGenerated is published on `rwb.comms.events.v1`.
- RWB-P6-E1055-APP is done: the proof-of-delivery capture design is settled — the barcode, the result code vocabulary of LOV-DELIVERY and the mapping of the WIN result codes are agreed with the WIN owner through rwb-integration.
- RWB-P6-E2021-CON is published: the two operations on base `/api/recovery/comms/v1`, the dispatch file contract with rwb-integration, the dispatch fields on `notice`, the hold reasons, the two event envelopes and the fakes, so this story builds against a fixed contract on Day 1.
- The `rwb_comms` baseline is in place from RWB-P6-E1046-APP and RWB-P6-E1052-APP: `notice`, `template`, `merge_field` and the library objects `outbox_event`, `processed_event`, `idempotency_key` exist, and the per-service Flyway sequence runs (DP-15).
- The decision-record library and the shared topic `rwb.decision-record.v1` are live, with the RWB-PLT-E1027-CON contract (DP-03); the outbox and inbox library is live with RWB-PLT-TE006-CON (DP-09); the Temporal workflow kit and the `rwb-recovery` namespace are live with RWB-PLT-E1071-CON (DP-10).
- The reference-data contract of rwb-case is live (RWB-P3-E1043-CON, DP-07) for LOV-NOTICE, LOV-DELIVERY, LOV-SENT-TYPE, the statutory notice type list and the proof window, and the parameters of the service are read as data.
- The D7.1 demand and recall approval contract of rwb-decision is live (RWB-P7-E2014-CON): a notice reaches state Approved only through that approval, and this story reads the answer and never approves.
- The dispatch-eligible notice states are set to Approved (`rwb.comms.dispatch.eligible-states` = APPROVED) and the proof window is the 7 days of R-LIT-08, both as data and not as code. The arithmetic of the 7-day window on the sent date is Not specified in the source documents (GAP-1091; ASM-2039).
- The WIN dispatch file (INT-14) has a layout, an acknowledgement and an owning operation that this story can call; they are Not specified in the source documents (GAP-1089; ASM-2037). The INT-15 proof results are read from rwb-source-data on `GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=` of `rwb-source-data.yaml` 5.1.0 (RD-P1-007).
- The cross-service answers this story needs are available as contract fakes from the first run: the approval answer of rwb-decision (RWB-P7-E2014-CON), the case read with legal hold, queue and scope of rwb-case, the contact-stop answers of rwb-deviation, the ACE facts of rwb-source-data and the WIN file answer of rwb-integration.
- The letter body and the addressee are not read here at all: they stay in rwb-document and rwb-source-data, and the dispatch file carries a document reference and the barcode, never a name or an address.
- No build dependency outside rwb-comms and the platform contracts: the H rows in the metadata table are the contract baseline, the two prior app stories and the platform contracts; the C rows never block the build (Template and Rules §R5.7).

### 4. Flow

1. A litigation officer requests a notice with `POST /api/recovery/comms/v1/cases/{caseId}/notices` and an Idempotency-Key; the generation of RWB-P6-E1052-APP runs and the answer is the Notice in state Generated (but API-P6-001 keeps its purpose of generating the notice from the approved template).
2. The litigation officer approves the notice on SCR-18 through the decision point of S4 rwb-litigation (operation path Not specified in the source documents (GAP-2093)); the approval itself is held in the ApprovalWorkflow of P7 rwb-decision (RWB-P7-E2014-CON), and the notice reaches state Approved.
3. At 16:00 on the business date the Temporal Schedule of this service starts `NoticeDispatchWorkflow` on task queue `rwb-comms` for the JOB-10 run, with the business date as the workflow input and no personal data in it.
4. The workflow runs its first step, the proof-window step: every notice in state Sent whose sent date is past the 7-day proof window of R-LIT-08 becomes Unserved with delivery status PENDING, one decision record is written for each, and no NOTICE_PERIOD timer is asked of rwb-case.
5. The workflow selects the notices in an eligible state (`rwb.comms.dispatch.eligible-states` = APPROVED) for the business date, one page at a time, and for each one runs the conduct check in this order: legal hold of the case, open contact stop of X1 or X2, state of the template version, and consent of the postal channel with the statutory rule.
6. A notice that fails the check is held: the hold reason is written on the `notice` row (`CONTACT_STOP_X1`, `LEGAL_HOLD`, `TEMPLATE_WITHDRAWN`), the notice is not written to the dispatch file, the decision record is written through the library with the rule (R-LIT-04, R-LIT-05, R-UNI-20), the ledger entry of rwb-source-data carries conduct check BLOCKED, and rwb-case receives the routing or the task with the message of section 14.
7. A notice that passes is written to the dispatch file of the business date through the file contract of rwb-integration (INT-14), with conduct check PASSED on the ledger entry and the statutory-consent note when consent is withdrawn and the notice type is statutory (R-UNI-10).
8. The WIN acknowledgement for the file returns the barcode and the sent date for each notice; the workflow writes `barcode`, `sent_date`, `sent_type` and `dispatch_file_id` on the notice, moves it to Sent, writes the ledger entry naming the barcode and publishes `rwb.comms.NoticeDispatched.v1` on `rwb.comms.events.v1`.
9. The proof results are read on `GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=` (read timing and business date Not specified in the source documents (GAP-2096)); the read writes nothing in rwb-source-data. A row is matched to the notice by barcode as a delivery-result fact of INT-15; rwb-comms appends one proof entry for the matched `podKey` on the ledger, and after the 201 or 200 answer a DELIVERED result sets `callback_date` and `delivery_status` DELIVERED, moves the notice to Delivered and publishes `rwb.comms.NoticeDelivered.v1`, and rwb-case starts the NOTICE_PERIOD timer from the call-back date under R-LIT-07.
10. A REFUSED or UNDELIVERABLE result sets Unserved with that delivery status, writes the decision record under R-LIT-09, writes the ledger entry, publishes `rwb.comms.NoticeDelivered.v1` with the result, and asks rwb-case for the transfer of the case to its owner's queue with reason NOTICE_UNSERVED and for MSG-P6-008. On a delivered notice rwb-case starts the NOTICE_PERIOD timer from the callback date on NoticeDelivered; the Unserved path is this transfer call and starts no timer.
11. A notice whose decision record cannot be written does not proceed: the state is unchanged, the notice is not written to the file, the run record shows MSG-P7-003 and an incident is raised under R-UNI-39.
12. A litigation officer reads the notice with `GET /api/recovery/comms/v1/notices/{noticeId}`, and SCR-18 shows the state, the sent date, the barcode, the call-back date and the proof result; the ledger timeline on SCR-04 shows each entry with its conduct check result.
13. A repeat of the POST with the same Idempotency-Key returns the first notice with status 201, and a GET for a notice outside the caller's scope answers 404 with MSG-P4-003.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | WIN returns Refused or Undeliverable | Notice Unserved; case to the owner's queue with the reason | MSG-P6-008 | AC3 |
| X2 | An open X1 or X2 deviation has the contact stop on | Notice held; case to the deviation owner | MSG-P6-001 | AC13; end-to-end owned by RWB-ITG-E2021-ITG (legacy AC4) |
| X3 | Consent for the postal channel is withdrawn | A statutory notice is still sent | None | AC14 (legacy AC5 is owned by RWB-ITG-E2021-ITG) |
| X4 | No proof 7 days after sending | Notice Unserved; notice period not started | MSG-P6-008 | AC6 |
| X5 | A legal hold is on the case | Notice held; nothing sent | MSG-P3-004 | AC7 |
| X6 | The template of an approved notice is withdrawn before dispatch | Notice held | MSG-P6-003 | AC8 |
| X7 | The decision log write fails for a held or unserved notice | Notice unchanged; retried on the next run; incident raised | MSG-P7-003 | AC9 |
| X8 | POST repeated with the same Idempotency-Key | The first notice is returned | None | AC10 |
| X9 | GET for a notice outside the caller's scope | Refused | MSG-P4-003 | AC11 |
| X10 | POST with no notice type | Refused | MSG-GEN-001 | AC12 |
| X11 | The ledger append fails or is refused | The notice state is not advanced and no event is written; a failed call is retried with the same keys | None | AC19, AC20 |
| X12 | The proof-of-delivery or consent read gives no answer | No notice changes on a proof with no row; a missing consent answer never passes the check | None | AC21, AC22 |

X2 and X3 remain exception paths of the legacy key; their criteria are end-to-end and are owned by `RWB-ITG-E2021-ITG`. This story still raises the two outcomes in its own code, because the conduct check that produces them is the one built here (see AC9 for the X2 fact reaching the check).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E2021-CON, the two prior rwb-comms app stories and the platform contract libraries. The approval, the case read, the contact stop, the ACE facts and the WIN file are contract fakes from the first run |
| Negotiable | The proof window, the statutory notice type list, the eligible states, the delivery-result codes and the hold reasons are data rows and parameters; the story fixes the conduct order and the state path |
| Valuable | Every letter carries a conduct result, the notice state follows the proof and not the print, and the notice period starts only from a call-back date |
| Estimable | Two endpoints, one conduct-check service, one workflow with three activities and a proof-window step, one Schedule and one outbox path |
| Small | Fits one sprint with its tests, as the app slice of the legacy key |
| Testable | Each criterion in section 7 runs as one automated test against the contract fakes, and the end-to-end path is proven by `RWB-ITG-E2021-ITG` |

### 7. Acceptance criteria

```gherkin
Feature: Letter dispatch loop with proof of delivery from WIN — the rwb-comms slice

  Background:
    Given the dispatch-eligible notice states are "APPROVED"
    Given the proof window is 7 days
    Given notice "N-0101" for case "RC-2026-000321" is "Approved" with notice type "DEMAND" and template "DEMAND-SSME" "TH" version 1 Approved
    Given case "RC-2026-000321" has no legal hold and no open deviation

  Scenario: AC3 Undelivered (legacy RWB-E2-021 AC3)
    Given the rwb-decision contract mock returns the decision record for decision code "D7.1" and rule "R-LIT-09" on notice "N-0101"
    Given the rwb-case contract mock returns case "RC-2026-000321" with its owner queue and accepts the transfer with reason "NOTICE_UNSERVED"
    Given notice "N-0101" is "Sent" on 2026-12-15
    When the proof-of-delivery read of 2026-12-21 returns a row with barcode "RR223344556TH" and delivery status "UNDELIVERABLE"
    Then notice "N-0101" is "Unserved" with delivery status "UNDELIVERABLE"
    Then one decision record exists with decision code "D7.1" and rule "R-LIT-09"
    Then the system transfers case "RC-2026-000321" to its owner's queue with reason "NOTICE_UNSERVED"
    Then the owner sees MSG-P6-008 naming "DEMAND" and "UNDELIVERABLE"
    Then the task "NOTICE_UNSERVED" has the due date Not specified in the source documents (GAP-2218) and the case owner role from the SERVICE_LEVEL reference row
    Then the system starts no notice period timer
    Then one proof entry is appended on POST /api/recovery/source-data/v1/cases/{caseId}/interactions with eventCode "LETTER", idempotencyKey "LETTER-RC-2026-000321-<yyyyMMdd of callbackDate>-{u}", where {u} is the UUID version 5 of {pod_key} in the RFC 9562 URL namespace, and externalRef the barcode of the row; its deliveryStatus for "UNDELIVERABLE" is Pending (NEW-GAP-D3)

  Scenario: AC6 Proof window expires (legacy RWB-E2-021 AC6)
    Given the rwb-decision contract mock returns the decision record for rule "R-LIT-08" on notice "N-0102"
    Given the rwb-case contract mock returns no "NOTICE_PERIOD" timer for case "RC-2026-000654"
    Given notice "N-0102" for case "RC-2026-000654" is "Sent" with sent date 2026-12-15 and no proof returned
    Given notice "N-0103" for case "RC-2026-000655" is "Sent" with sent date 2026-12-16 and no proof returned
    When the proof-window workflow runs on 2026-12-22
    Then notice "N-0102" is "Unserved" with delivery status "PENDING"
    Then one decision record exists for "N-0102" with rule "R-LIT-08"
    Then the system starts no notice period timer for case "RC-2026-000654"
    Then notice "N-0103" stays "Sent"

  Scenario: AC7 Legal hold stops dispatch (legacy RWB-E2-021 AC7)
    Given the rwb-case contract mock returns case "RC-2026-000321" with legal hold true
    Given case "RC-2026-000321" has legal hold true
    When the dispatch workflow runs on 2026-12-14
    Then notice "N-0101" is "Held" with hold reason "LEGAL_HOLD" and is not in the WIN file
    Then the case record shows MSG-P3-004
    Then one ledger entry is appended with eventCode "LETTER", conductCheck "BLOCKED", the hold reason "LEGAL_HOLD" in its summary, no deliveryStatus and no externalRef

  Scenario: AC8 Template withdrawn after approval (legacy RWB-E2-021 AC8)
    Given the rwb-case contract mock returns the task raised to the litigation officer team with MSG-P6-003 for notice "N-0101"
    Given template "DEMAND-SSME" "TH" version 1 was withdrawn on 2026-12-13
    When the dispatch workflow runs on 2026-12-14
    Then notice "N-0101" is "Held" with hold reason "TEMPLATE_WITHDRAWN" and is not in the WIN file
    Then the system raises a task to the litigation officer team with MSG-P6-003
    Then one ledger entry is appended with conductCheck "BLOCKED" and "TEMPLATE_WITHDRAWN" in its summary, with no deliveryStatus and no externalRef

  Scenario: AC9 Decision log write fails on a held notice (legacy RWB-E2-021 AC9)
    Given the rwb-deviation contract mock returns the open deviation "X2" with contact stop on for case "RC-2026-000321"
    Given the rwb-decision contract mock returns the decision store unavailable for notice "N-0101"
    Given case "RC-2026-000321" has an open deviation "X2" with contact stop on
    Given the decision record store is unavailable
    When the dispatch workflow runs on 2026-12-14
    Then notice "N-0101" stays "Approved" and is not in the WIN file
    Then the workflow step result shows MSG-P7-003 for "N-0101"
    Then the system raises an incident under rule R-UNI-39
    Then no ledger entry is appended for "N-0101"

  Scenario: AC10 Repeated request (legacy RWB-E2-021 AC10)
    Given "LIT-0101" sent POST /cases/RC-2026-000321/notices with notice type "RECALL" and Idempotency-Key "a1b2c3d4-0001"
    When the same request is sent again with Idempotency-Key "a1b2c3d4-0001"
    Then the response is the first notice with status 201
    Then case "RC-2026-000321" has one RECALL notice

  Scenario: AC11 Notice outside the caller's scope (legacy RWB-E2-021 AC11)
    Given the rwb-case contract mock returns the case of notice "N-0200" with an owner and a queue outside the caller's scope
    Given notice "N-0200" belongs to a case outside the scope of "LIT-0101"
    When "LIT-0101" sends GET /notices/N-0200
    Then the response is status 404 with MSG-P4-003

  Scenario: AC12 Notice type missing (legacy RWB-E2-021 AC12)
    Given "LIT-0101" holds RW-LITOFF and case "RC-2026-000321" is in scope
    When "LIT-0101" sends POST /cases/RC-2026-000321/notices with no notice type
    Then the response is status 422 with MSG-GEN-001 naming "notice type"

  Scenario: AC13 An open X1 or X2 deviation has the contact stop on: notice held, case to deviation owner (X2 of section 5) (new, D-RCV-60)
    Given case "RC-2026-000321" has an open X1 or X2 deviation with the contact stop on
    When "LIT-0101" sends POST /cases/RC-2026-000321/notices
    Then the notice is held, the case goes to the deviation owner and the response carries MSG-P6-001
    Then one ledger entry is appended with conductCheck "BLOCKED", the reason "CONTACT_STOP_X1" in its summary, no deliveryStatus and no externalRef

  # AC14 to AC18 are added by this story and have no legacy origin.

  Scenario: AC14 Postal consent withdrawn, statutory notice still sent (X3 of section 5) (new, D-RCV-60)
    Given case "RC-2026-000321" has consent for the postal channel withdrawn
    Given notice "N-0101" is a notice of type "DEMAND" in the statutory notice list
    When the dispatch workflow runs on 2026-12-14
    Then notice "N-0101" is not held for the withdrawn consent and is written to the WIN file
    Then the consent fact is the consentStatus "WITHDRAWN" answered by GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}
    Then after the WIN acknowledgement one dispatch entry is appended with idempotencyKey "LETTER-RC-2026-000321-<yyyyMMdd of sent date>-{notice record uuid}", sourceRef "INT-14 WIN", channel "LETTER", direction "OUTBOUND", conductCheck "PASSED", deliveryStatus "SENT", externalRef equal to the barcode and the statutory-consent note in its summary

  Scenario: AC15 Architecture constraints hold (BR11 to BR19) (new, D-RCV-60)
    Given the notice, its dispatch file reference and its proof dates are stored
    When the dispatch workflow and the proof-window step run
    Then the rows are written and read in rwb_comms only and no other service's table is read
    Then the state change and its outbox row are written in one transaction
    Then the dispatch run and the proof-window step run as a Temporal Schedule and a workflow
    Then the eligible states, proof window and statutory notice types are read from rwb-case reference data
    Then the dispatch file and every event carry a document reference, a barcode and dates and no name, address or account number

  Scenario: AC16 Error answers 401 and 403 of the provided operations (new, D-RCV-60)
    Given "LIT-0101" sends POST /cases/RC-2026-000321/notices without credentials
    Then the response is status 401 with message Not specified in the source documents (NEWAC-RWB-P6-E2021-APP-AC16)
    Given "RW-CASEOWN" sends POST /cases/RC-2026-000321/notices
    Then the response is status 403 with MSG-P4-002

  Scenario: AC17 Activity retry and timeout (new, D-RCV-60)
    Given a cross-service call of the decision check takes longer than its 2 s budget
    When the dispatch workflow runs on 2026-12-14
    Then notice "N-0101" stays "Approved" and is not in the WIN file
    Then the activity retry count is Not specified in the source documents (NEWAC-RWB-P6-E2021-APP-AC17)

  Scenario: AC18 Status change the model does not allow is refused (new, D-RCV-60)
    Given notice "N-0101" is "Unserved"
    When a status change to a state the notice model does not allow is requested
    Then the change is refused and notice "N-0101" stays "Unserved"
    Then the refusal reason is Not specified in the source documents (NEWAC-RWB-P6-E2021-APP-AC18)

  Scenario: AC19 The ledger append fails and is retried (new, RD-P1-001, RD-P1-007)
    Given notice "N-0101" passed the conduct check and the rwb-source-data provider fake answers 503 to the first append and 201 to the next
    When the dispatch workflow appends the dispatch entry
    Then the notice state is not advanced and no event is written until an append is answered 201 or 200
    Then the retry sends the same Idempotency-Key header, idempotencyKey and body, and the case ledger holds one entry
    TC: TC-P6-E2021-APP-06 (Test Cases v9)

  Scenario: AC20 The ledger refuses the append (new, RD-P1-007)
    Given the rwb-source-data provider fake answers 422 MSG-GEN-001 with field "/conductCheck", or 409 MSG-PLT-N009-05
    When the dispatch workflow appends the entry
    Then the notice keeps its state, no event is written, the key is not changed to force a second entry and the run records the refused call
    TC: TC-P6-E2021-APP-07 (Test Cases v9)

  Scenario: AC21 The proof-of-delivery read gives no row (new, RD-P1-007; GAP-0579)
    Given the proof-of-delivery read answers 200 with no row, or 503
    When the workflow reads the proof of the business date
    Then notice "N-0101" stays "Sent", no proof entry is appended and no NoticeDelivered is written
    TC: TC-P6-E2021-APP-08 (Test Cases v9)

  Scenario: AC22 The consent read cannot be answered (new, BR14)
    Given GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId} answers 503
    When the dispatch workflow runs the conduct check for "N-0101"
    Then the check does not pass, the notice is not written to the WIN file, stays "Approved" and no ledger entry is appended
    TC: TC-P6-E2021-APP-09 (Test Cases v9)
```

The eight criteria above are the legacy criteria of RWB-E2-021 that the rwb-comms service itself satisfies, copied line for line with the origin tag on each scenario and one mock line added where the criterion names a fact of another owner; version 3 restates the proof trigger of AC3 on the published read and adds ledger assertions to AC3, AC7, AC8, AC9, AC13 and AC14 and the new AC19 to AC22 (TC: TC-P6-E2021-APP-06, TC-P6-E2021-APP-07, TC-P6-E2021-APP-08, TC-P6-E2021-APP-09, TC-P6-E2021-APP-01, TC-P6-E2021-APP-02, TC-P6-E2021-APP-03, TC-P6-E2021-APP-04, TC-E2-021-31, TC-P6-E2021-APP-05 (Test Cases v9)). Legacy AC1 (dispatch), AC2 (proof back), AC4 (contact stop blocks the letter) and AC5 (consent withdrawn does not stop a statutory notice) are not copied: they are end-to-end journeys and belong to `RWB-ITG-E2021-ITG`, which also carries their wording, including the phrase "does not writ notice" of legacy AC4 exactly as the legacy story writes it. The paths in the criteria are the paths of the operations as the legacy names them; the base of this service is `/api/recovery/comms/v1` (DP-13). The two notice operations, POST /cases/{caseId}/notices and GET /notices/{noticeId}, stay with this service and RWB-P6-E1052-APP with their Litigation rights; SCR-33 Template approval stays with the template stories; the offer view of FEAT-COM-01 for LINE OA and HOME.SCB is not served by these operations.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every letter is checked before it is written to the WIN file, and the result is on the ledger entry | REQ-OCC-005; FEAT-OCC-05 |
| BR2 | A contact stop from X1 or X2 holds the notice and routes the case to the deviation owner | R-LIT-05; CTL-16 |
| BR3 | A legal hold stops every outbound action | R-UNI-20 |
| BR4 | Withdrawn consent removes the channel from the contact plan, and statutory notices continue | R-UNI-10; REQ-OCC-006; CTL-16 |
| BR5 | The notice period starts from the delivery date on the proof | R-LIT-07; CTL-15 |
| BR6 | A refused, returned or undeliverable letter records the result and queues an alternate service method | R-LIT-09 |
| BR7 | No proof inside the proof window marks the notice unserved, and the notice period does not start | R-LIT-08 |
| BR8 | A withdrawn template holds the notice | R-LIT-04 |
| BR9 | A held or unserved result that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR10 | Which notice types are statutory is a list held as reference data | Principle 1; LOV-NOTICE |
| BR11 | The notice, its dispatch file reference and its proof dates are `rwb_comms` rows; no other service reads them and this service reads no other service's table (DP-01) | Architecture v5 slide 17; DP-01 |
| BR12 | The dispatch and delivery facts are written to the outbox in the same transaction as the state change and relayed with the CloudEvents envelope; the case, the reporting read model and the ledger follow from the events and not from a call made for them (DP-09) | Architecture v5 slides 42 and 43 notes; DP-09 |
| BR13 | The 16:00 run and the proof-window step are a Temporal Schedule and a workflow in this service; no Quartz row, no shared job table and no batch table is read (DP-10) | Architecture v5 slide 44 (JOB-10, JOB-11); DP-10 |
| BR14 | Every cross-service call is one hop with a 2 s budget, and a missing answer never decides an allow or a pass of the conduct check (DP-11) | ADR-020; DP-11 |
| BR15 | The eligible states, the proof window, the statutory notice types and the delivery-result codes are reference data of rwb-case read with the version in force; no value is written in code (DP-07) | FSD P6 A2.5 BR-P6-005; TSD P6 T3.2; DP-07 |
| BR16 | The ledger entry is rwb-source-data's and is written through its contract; the decision record is written through the local library; the case status, the transfer and the NOTICE_PERIOD timer are rwb-case's, driven by the facts this story sends (DP-03, DP-18) | R-PREC default ruling; DP-03; DP-18 |
| BR17 | The case status moves of the legacy story are P3's: this story holds the notice and sends the facts; R-DEV-01 and R-UNI-20 are applied by rwb-case on the DELIVERY_FAILED and PROOF_WINDOW_EXPIRED facts | R-DEV-01; R-UNI-20; TSD P6 T4 |
| BR18 | Alternate and substituted service methods are out of scope: R-LIT-10 and R-LIT-11 are Epic 5, and this story only records the unserved outcome and the reason | R-LIT-10; R-LIT-11; legacy section 19 |
| BR19 | The letter body and the addressee stay in rwb-document and rwb-source-data; the dispatch file and every event carry a document reference, a barcode and dates, never a name, an address or an account number | Architecture v5 slides 42 and 43 notes; Template and Rules §R7.2 s17 |
| BR20 | The conduct check and the consent check are one versioned rule package, governed in rwb-decision and evaluated in this service; the package name is Not specified in the source documents (GAP-1610), and its first version is approved by the conduct and QA officer | Program BRD v5 REQ-OCC-005 and REQ-OCC-006; FSD P6 A2.5 BR-P6-005; Architecture v5 slide 14 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Generated | The D7.1 approval of rwb-decision is granted | The approval answer names the notice and the approved template version | Approved |
| Approved | The 16:00 run reaches the notice and the conduct check passes | No legal hold, no open X1 or X2 contact stop, the template version is still Approved, and the consent gate is passed or the notice type is statutory | Sent (after the WIN acknowledgement names the barcode and the sent date) |
| Approved | The 16:00 run reaches the notice and the conduct check blocks | Hold reason CONTACT_STOP_X1, LEGAL_HOLD, TEMPLATE_WITHDRAWN or the pending-proof reason | Held |
| Held | The hold is lifted and the next run passes the check | The blocking fact is cleared through its owner (rwb-case for the hold, rwb-deviation for the stop, rwb-comms for the template version) | Approved, and then Sent on the same run |
| Sent | A proof result DELIVERED arrives for the barcode | The call-back date is present | Delivered (the NOTICE_PERIOD timer is rwb-case's, started from the call-back date under R-LIT-07) |
| Sent | A proof result REFUSED or UNDELIVERABLE arrives | The result is one of the two | Unserved (delivery status set, R-LIT-09, DELIVERY_FAILED to rwb-case) |
| Sent | The 16:00 run finds no proof inside the proof window | The sent date is past the 7-day window of R-LIT-08 | Unserved with delivery status PENDING and no notice period timer |

The gates on the Approved to Sent edge are the four checks of the conduct order in section 4, step 5, applied with the reference data listed in BR15. The NOTICE_PERIOD timer, the case status and the queue transfer are not state of this service: they are rwb-case's, started or applied on the facts this story publishes and sends (BR16, BR17). A held notice keeps its Approved state in the sense of the eligible-state parameter and is excluded by its hold reason, so a rerun never writes it to a second file for the same business date.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the matrix of TSD P6 T6.1: requests a notice (right C), reads it with its dispatch and proof (right R) |
| RW-LEGAL, legal counsel | Litigation RA in TSD P6 T6.1: reads the notice and approves the template version that the conduct check reads (rights R and A) |
| RW-CASEOWN, case owner | Litigation R in TSD P6 T6.1: reads the notice and the proof of the case |
| RW-TEAMMGR, team manager | Litigation R in TSD P6 T6.1: reads the notices of the team's cases |
| RW-PLATADM, platform administrator | Litigation R in TSD P6 T6.1: reads the notices and operates the run through the Schedules and the run view; the run and the rerun are deployed by RWB-P6-E2021-OPS |
| rwb-comms service identity | Runs the Schedule and the workflow, reads its own `rwb_comms` rows, writes the notice state and the dispatch fields, and writes the outbox rows (DP-02) |
| Decision-record library identity | Writes the local decision record for a held or an unserved notice and relays it on `rwb.decision-record.v1` (DP-03) |

The legacy story also names RW-ENFORCE (Litigation CRU in T6.1), RW-CONDUCT and RW-HEADLIT; their rights are read from the same matrix and are not restated here. The matrix of TSD P6 T6.1 is the only source used for the letters above.

The authorise contract of rwb-access (DP-08) is not in this story's pattern set: the capability area and the right of each operation are declared in RWB-P6-E2021-CON and enforced at gateway-bff, which asks rwb-access, so no P4 dependency is declared here. The scope test of AC11 then needs a case-scope fact inside this service, and no dependency in this story provides one: the scope source and the shape of the local guard are Not specified in the source documents (GAP-1092; ASM-2040).

### 11. Data

| BR Field ID | Entity in `rwb_comms` | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Write on create, read |
| DF-LEG-016 | notice | case_id | Write on create, read |
| DF-LEG-017 | notice | document_id | Write on create, read |
| DF-LEG-018 | notice | notice_type | Write on create, read |
| DF-LEG-019 | notice | sent_date | Write on the WIN acknowledgement, read |
| DF-LEG-020 | notice | barcode | Write on the WIN acknowledgement, read |
| DF-LEG-021 | notice | callback_date | Write on the proof result, read |
| DF-LEG-022 | notice | delivery_status | Write on the proof result, read |
| DF-LEG-023 | notice | sent_type | Write on the WIN acknowledgement, read |
| DF-LEG-030 | notice | party_id | Write on create, read |
| DF-LEG-031 | notice | template_id | Write on create, read |
| DF-LEG-032 | notice | hold_reason | Write on a held notice, read |
| DF-LEG-033 | notice | dispatch_file_id | Write when the notice enters a dispatch file, read |
| DF-LEG-034 | notice | dispatch_attempts | Write on every file selection, read |
| Standard column | notice | state | Write on every state move, read |
| Standard column | notice | version, updated_at, updated_by | Write, for the optimistic lock of the workflow step |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code, rule, case, notice, decided at, hash chain | Write |
| DF-INT-005, DF-INT-011, DF-INT-012 | ledger entry, through the rwb-source-data contract | channel, summary, conduct_check | Write through the contract, never a table |
| DF-CAS-020 | recovery_case, through the rwb-case contract | legal_hold | Read through the contract, never a table |
| DF-CAS-038, DF-CAS-043, DF-CAS-044 | deviation, through the rwb-deviation contract | deviation_code, contact_stop, cleared_at | Read through the contract, never a table |
| DF-EXT-015 | consent of a postal contact point, through `GET /data-products/DP02/records` of rwb-source-data | `consentStatus` (GIVEN, WITHDRAWN, UNKNOWN) | Read through the contract, never a table |
| DF-WRK-030 | timer, owned by rwb-case | timer_type | Not read and not written; the NOTICE_PERIOD timer is rwb-case's |

The dispatch file reference is `notice.dispatch_file_id` (DF-LEG-033), which points at the outbound item of rwb-integration (P2) and never at a row of `rwb_integration`; `dispatch_attempts` counts the times the notice was selected for a file. The indexes are `ix_notice_barcode` on `notice (barcode)`, `ix_notice_sent_date` on `notice (sent_date, state)` for the proof-window step and `ix_notice_case_id` on `notice (case_id)` for the case read; the legacy index `ix_notice_state_sent` is replaced by `ix_notice_sent_date`, because the window step filters on the sent date and the state together. The migration is one per-service Flyway step in `rwb_comms` (DP-15). No personal data is written to `rwb_comms`: no name, no address, no identity number and no account number is a column of `notice`; the key to the party held in rwb-source-data is Not specified in the source documents (CG-ALL-6537), and the addressee is resolved in rwb-source-data and rwb-document at the moment the letter is produced. Field IDs are those in the Logical Data Model and Data Dictionary. The proof of delivery is held on the notice row as barcode, callback_date and delivery_status (DF-LEG-020 to DF-LEG-022), with no separate proof table; a separate table is settled only if a DB story needs it. This service applies a proof to its notice by barcode and reads the proof rows through the rwb-source-data contract, never through a v_ace_* view; which system writes v_ace_pod is not decided by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The shapes are those fixed in RWB-P6-E2021-CON; this story implements them and adds no path.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/notices` | API-P6-001: generate a notice from the approved template and return it, 201 with the Notice | Litigation, right C, scope applied | Idempotency-Key header, kept 24 hours |
| GET | `/notices/{noticeId}` | API-P6-002: read a notice with its dispatch and its proof of delivery, 200 with the Notice | Litigation, right R, scope applied | Not applicable |

Errors: 401 Not specified in the source documents (DOR-RWB-P6-E2021-APP-8); 403 the role lacks the Litigation right (MSG-P4-002); 404 the case or the notice is absent or out of scope (MSG-P4-003); 409 the template is not approved (MSG-P6-005) or a notice of this type is already in progress (MSG-P3-005); 422 a field fails validation (MSG-GEN-001); 503 the decision was not recorded (MSG-P7-003). The Notice body carries `id`, `caseId`, `documentId`, `noticeType`, `sentDate`, `barcode`, `callbackDate`, `deliveryStatus` and `sentType` as the legacy story names them, and the exact response field list and types are Not specified in the source documents (GAP-1094; ASM-2042).

Request: NoticeRequest with `noticeType` required, `partyId` defaulting to the borrower and `language` defaulting to TH, as the legacy story states and as RWB-P6-E1052-CON fixes it.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | reference-data read of LOV-NOTICE, LOV-DELIVERY, LOV-SENT-TYPE, the statutory notice type list and the proof window | P3 rwb-case, on RWB-P3-E1043-CON | The four checks of the conduct order and the result-code mapping; read with the version in force (DP-07) |
| POST | the D7.1 demand and recall approval of RWB-P7-E2014-CON | P7 rwb-decision | The approval answer that moves the notice to Approved; this story reads the answer and never approves |
| GET | case read of RWB-P6-E2021-CON for the case facts of the conduct check and the scope test | P3 rwb-case | `legal_hold`, owner and queue for the scope test; faked. The scope source and the shape of this read are Not specified in the source documents (GAP-1092; ASM-2040) |
| GET | active contact stops of RWB-P6-E2021-CON | S8 rwb-deviation | The open X1 and X2 contact stops of the case; faked |
| POST | the case facts this story sends: DELIVERY_FAILED, PROOF_WINDOW_EXPIRED and the queue transfer with NOTICE_UNSERVED | P3 rwb-case | The case move and the NOTICE_PERIOD timer, which are rwb-case's (BR17) |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data (RWB-P1-E1066-CON; RWB-P1-E2021-APP letter rules) | The dispatch, held and proof entries (DP-18); header `Idempotency-Key`; 201, 200, 409, 422, 503 |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records?caseId=` | P1 rwb-source-data (RWB-P1-E2021-APP) | The postal contact point and its `consentStatus`; no address is answered |
| POST | the dispatch file of rwb-integration | P2 rwb-integration | INT-14 out; faked. The operation names, the columns and the acknowledgement are Not specified in the source documents (GAP-1089; ASM-2037) |
| GET | `/api/recovery/source-data/v1/proof-of-delivery?businessDate=` | P1 rwb-source-data (RWB-P1-E1055-APP) | `ProofOfDeliveryAnswer`; rows matched to the notice by barcode; writes nothing; 401, 403, 422, 503; read timing Not specified in the source documents (GAP-2096) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream. No row reads a table and no row reads a `v_ace_*` view: the ACE proof rows and the contact points reach this service through the owner's contract (DP-05, DP-18).

**Ledger entries (RD-P1-007; RD-P1-064).** Every entry: eventCode `LETTER`, occurredAt, actorType `SERVICE`, actorRef `rwb-comms`, idempotencyKey (at most 120), channel `LETTER`, direction `OUTBOUND`; the case is addressed by its uuid, and the case number in the key is that of the rwb-case case read. Dispatch: key `LETTER-<caseNo>-<yyyyMMdd of sent date>-<noticeId>`, sourceRef `INT-14 WIN`, conductCheck `PASSED`, deliveryStatus `SENT`, externalRef the WIN barcode, summary naming the notice type and barcode (and the statutory-consent note where it applies). Held: key `LETTER-<caseNo>-<yyyyMMdd>-<notice record uuid>`, conductCheck `BLOCKED`, the reason in the summary, no deliveryStatus and no externalRef. Delivery: one per matched `podKey`, externalRef the row `barcode`, else its `noticeRef` (a row with neither gets no entry and is logged as unmatched), occurredAt the `callbackDate` at 00:00 Asia/Bangkok, key `LETTER-<caseNo>-<yyyyMMdd of callbackDate>-<u>` with `<u>` the UUID version 5 of `podKey` in the RFC 9562 URL namespace, sourceRef the notice reference (at most 60), deliveryStatus from the row; appended only by rwb-comms. A new header key with a stored business key is answered 200 with the stored entry. On 503 MSG-P1-022 rwb-comms does not commit its action, or retries with the same header key and business key. The notice state is advanced only after a 201 or 200 answer (R-UNI-33). `NoticeDispatched` and `NoticeDelivered` carry `ce_idempotencykey` equal to the key of the same action. Pending: the mapping of WIN `delivery_status` to SENT, DELIVERED, READ, FAILED (NEW-GAP-D3; interim: the values of the RWB-P6-E1055-APP fixture); the occurredAt of a row with no callback date (NEW-GAP-F14-9); a second pod row with a different podKey for a delivered barcode (NEW-GAP-F14-8); the decision point of the dispatch and delivered-proof decision records (NEW-GAP-F14-5).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | P6 | caseId | notice ID, barcode, sent date |
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | P6 | caseId | notice ID, delivered at, status |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 | caseId | decision code D7.1, rule ID (R-LIT-04, R-LIT-05, R-LIT-08, R-LIT-09, R-UNI-20), notice ID, decided at, record reference, business date |

All three are written to the outbox in the same transaction as the state change and relayed with the CloudEvents 1.0 envelope by the outbox relay of the platform (DP-09). `NoticeDelivered` is published for the Delivered, the Refused and the Undeliverable outcome, as the legacy story states; the consumers are rwb-case, rwb-litigation, rwb-guarantee and the reporting read model, as the event catalogue names them.

Proof-of-delivery capture depends, through rwb-source-data, on the Section B view v_ace_pod, which is unconfirmed until RWB-ACE-001 lands (GAP-1608). Proof-of-delivery capture stays behind its feature flag until the view is available. The fallback (proof entered by hand against the barcode) is to be agreed with the litigation business owner by a date Not specified in the source documents (GAP-1608).

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | Takes note of the case and the deviation code so the next 16:00 run holds the notices of that case when the deviation carries the contact stop; deduped through the inbox |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | Takes note that the stop is cleared so a held notice is eligible again; deduped through the inbox |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | Takes note of a case that closes or moves so the run skips it and the held notices of a closed case are left as they are; deduped through the inbox |

None of the three is a decision input on its own: the conduct check reads the live facts of its owner at the moment it runs, and the events only keep the local picture current between runs, which is what protects the loop when an event arrives after a run has started. The consumers are not a second source of truth and no event carries personal data.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| NoticeDispatchWorkflow | Workflow, one run per business date, workflow ID from the business date and the run kind | `rwb-comms` | Runs the proof-window step, selects the eligible notices, runs the conduct check for each, hands the file to integration and waits for the acknowledgement and the proof results on a durable timer |
| generateLetter | Activity, in rwb-document | `rwb-document` | Produces the letter from the approved template version when the notice does not hold a document yet |
| decisionApproval | ApprovalWorkflow, child workflow of NoticeDispatchWorkflow, in rwb-decision | `rwb-decision` | The D7.1 approval of a notice, held in P7 ApprovalWorkflow with the notice as its source; the litigation officer's decision point is the S4 rwb-litigation decision point (operation path Not specified in the source documents (GAP-2093)); the workflow waits for the answer and never approves on its own; while the approval is open the notice is not written to the file (GAP-2093) |
| deliverFile | Activity, in rwb-integration | `rwb-integration` | Writes the notices of the run to the WIN dispatch file (INT-14) and returns the file reference and the acknowledgement |
| conductCheck | Activity, in rwb-comms | `rwb-comms` | The four checks of section 4, step 5, returning passed or blocked with the reason and the rule ID |
| recordDecision | Activity, in rwb-comms through the library | `rwb-comms` | Writes the local decision record and its outbox row; a failure fails the step and the notice does not proceed |

The workflow input is the business date, the run kind and the page cursor; it carries no notice body, no addressee and no personal data. The waiting for a proof result is a durable timer inside the workflow and not a Schedule.

#### 12.6 Schedules

| Name | Cron | Overlap policy | Catch-up | Registers |
|---|---|---|---|---|
| The JOB-10 notice dispatch run | 16:00 on every business day | SKIP | The window the workflow kit fixes | Starts NoticeDispatchWorkflow on task queue `rwb-comms` in namespace `rwb-recovery` with the business date |

The Schedule is a Temporal Schedule of this service through RWB-PLT-E1071-CON (DP-10); it is not a Quartz row and not a row of a shared job table. The bank Airflow opens the WIN file window and the handoff from the window to this Schedule is Not specified in the source documents (GAP-1095; ASM-2043).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | The notice, its dispatch fields and its proof dates; the state machine of section 9 |
| template | P6 (rwb_comms) | The template version the conduct check reads; written by RWB-P6-E1046-APP and RWB-P6-E1052-APP |
| merge_field | P6 (rwb_comms) | The merge catalogue; read only here |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The held and unserved decision entries of the conduct check (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | Outbox, inbox and idempotency objects (DP-09) |

Not owned and never read: `recovery_case`, `task` and `timer` (P3), `deviation` (S8), `decision_log_entry` (P7), `document` (P5), `interaction` (P1), `outbound_item` and `interface_config` (P2). The letter body, the addressee, the ledger, the case state and the timer are reached through the contracts of their owners, and no foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-decision approval fake (RWB-P7-E2014-CON) | The D7.1 approval answer | Granted for notice `N-0101` with template `DEMAND-SSME` TH version 1, returned for notice `N-0101` with decision code D7.1; a refused answer; a delayed answer beyond 2 s |
| rwb-decision record fake | The local decision-record library and the shared topic | A healthy chain and outbox; a stopped chain for AC9 and TC-E2-021-14 |
| rwb-case fake | The case read, the case facts and the scope read | Case `RC-2026-000321` with no legal hold and no open deviation; legal hold true for AC7; no NOTICE_PERIOD timer for `RC-2026-000654`; a case of another owner and queue for AC11; a delayed answer beyond 2 s |
| rwb-deviation fake | The active contact stops | No stop for the background case; X1 with contact stop on; X2 with contact stop on for AC9 |
| rwb-source-data provider fake 5.1.0 (RD-P1-011) | The DP02 contact-and-consent rows, the proof-of-delivery read and the ledger append | The postal contact point with consentStatus WITHDRAWN for the statutory case; proof rows DELIVERED, REFUSED and UNDELIVERABLE for barcode `RR223344556TH`, a no-row answer; ledger 201, 200, 409, 422 and 503 |
| rwb-integration WIN fake | The dispatch file and its acknowledgement | The INT-14 file for business date 2026-12-14 and its acknowledgement with barcode `RR223344556TH` and sent date 15122026; a missing acknowledgement |

The fakes are derived from the published contracts of RWB-P6-E2021-CON, and the drift test of that story fails a build in which a fake and the document disagree.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 9 consumed | The notice request and read provided; reference data, approval, case read, contact stops, case facts, ledger append, consent read, the WIN file and the proof read consumed; one hop, 2 s |
| Kafka | 3 published, 3 consumed | NoticeDispatched, NoticeDelivered and DecisionRecorded published; DeviationRaised, DeviationCleared and CaseStateChanged consumed |
| Temporal | 1 workflow, 3 activities and 1 child workflow | NoticeDispatchWorkflow with conductCheck, deliverFile and generateLetter, and the decision approval child |
| File | 2 | The INT-14 WIN dispatch file out through rwb-integration; the INT-15 proof result in, read on the proof-of-delivery read of rwb-source-data (timing GAP-2096) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, modules `dispatch` and `notices`, Java packages `th.co.scb.ace.workbench.recovery.comms.dispatch` and `...comms.notices`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies here as a prohibition with one exception of direction: this service reads no `v_ace_*` view and no ACE row, and the proof rows that the legacy story reads from `v_ace_pod` reach it through `GET /proof-of-delivery` of `rwb-source-data.yaml` 5.1.0, matched to the notice by barcode (timing GAP-2096). The WIN file and its acknowledgement stay with rwb-integration (ASM-2037).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeController | Controller | `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}` with validation, the Idempotency-Key and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| NoticeService | Service | Creates and reads the notice, orders the state moves and refuses a read outside the caller's scope |
| ConductCheckService | Service | The four checks in order — legal hold, contact stop, template state, consent with the statutory rule — returning passed or blocked with the reason and the rule ID |
| DispatchSelection | Service | Selects the eligible notices of the business date, pages them, and writes `dispatch_file_id` and `dispatch_attempts` in the same transaction |
| WinFileClient | Adapter | The file contract of rwb-integration: the dispatch file of the business date and its acknowledgement |
| CaseFactClient | Adapter | The case read, the scope read and the case facts this story sends, on the rwb-case contract |
| DeviationClient | Adapter | The active contact stops of the case on the rwb-deviation contract |
| LedgerClient | Adapter | The ledger append and the proof-of-delivery and consent reads on `rwb-source-data.yaml` 5.1.0 |
| ProofWindowStep | Workflow step | The first step of the run: a Sent notice past the 7-day window becomes Unserved with delivery status PENDING under R-LIT-08 |
| DeliveryResultHandler | Service | Applies DELIVERED, REFUSED and UNDELIVERABLE: the notice state, the dates, the decision record, the ledger entry and the events |
| ReferenceCatalog | Service | Reads LOV-NOTICE, LOV-DELIVERY, LOV-SENT-TYPE, the statutory notice type list and the proof window with the version in force; no value in code |
| NoticeDispatchWorkflowImpl | Workflow | The run, its ordering, its durable timer for the proof and its compensation when a step fails |

**Database and migrations**

- Writes `notice`, `template`, `merge_field`, the local decision record and the library objects, all in schema `rwb_comms`; reads no other schema.
- Migration in this story: `V2021_1__notice_dispatch.sql` adds `sent_type`, `dispatch_file_id` and `dispatch_attempts` when the baseline of RWB-P6-E1052-APP does not hold them yet, the hold reason value set as a check constraint on `hold_reason`, and the three indexes of section 11. No column carries a name, an address or an account number.
- No row of `template` or `merge_field` is written here: the template catalogue is RWB-P6-E1046-APP and the template approval is RWB-P6-E1052-APP.

**Configuration and reference data**

- `rwb.comms.dispatch.eligible-states` = APPROVED, as data.
- The proof window: 7 days under R-LIT-08, read from reference data with its version; the arithmetic on the sent date is Not specified in the source documents (GAP-1091; ASM-2039).
- The statutory notice type list: DEMAND, RECALL, STATUTORY_SALE_NOTICE and GUARANTOR_NOTICE as LOV-NOTICE holds them, with the statutory flag as data owned by the business; this story reads it (BR10).
- The delivery-result code map from the WIN result codes to LOV-DELIVERY as data, not as code, with the mapping agreed under RWB-P6-E1055-APP.
- The feature switch `rwb.comms.win-dispatch-loop`, read as a parameter: off means the run starts no dispatch and holds the notices with the pending-proof reason, never writes a file.
- The hold reason vocabulary is fixed by RWB-P6-E2021-CON: CONTACT_STOP_X1, LEGAL_HOLD, TEMPLATE_WITHDRAWN and the pending reason.

**Build steps**

1. NoticeController and NoticeService over the two operations, the Idempotency-Key and the scope refusal; tests for AC10, AC11 and AC12.
2. CaseFactClient, DeviationClient and ReferenceCatalog with the four reads and their fakes; the conduct order of section 4, step 5; a test per branch.
3. ConductCheckService with the four checks and the reason and rule returned; tests for AC7 and AC8 and the statutory branch of the consent gate.
4. recordDecision and the fail-closed path: a failed record leaves the notice unchanged and the run record shows MSG-P7-003; test for AC9 and TC-E2-021-14.
5. ProofWindowStep in the workflow, with the boundary of the 6-day and the 7-day notice; test for AC6.
6. WinFileClient and DispatchSelection: the file of the business date, the acknowledgement that sets the barcode and the sent date, and `dispatch_attempts`; test for the dispatch path behind the fake.
7. DeliveryResultHandler for the three results with the decision record, the ledger entry and the two events; test for AC3.
8. NoticeDispatchWorkflowImpl with the ordering, the durable proof timer and the rerun rule, and the Schedule of 16:00; the contract-fake run of the whole loop before the real services are live.

**Feature switch.** `rwb.comms.win-dispatch-loop`, read as a parameter; off refuses to dispatch closed and holds the notices.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E2021-CON stay green, and a SIT week shows every notice of the 16:00 run with a conduct result, every notice of the file with a barcode and a sent date, every unserved notice with its decision entry and no NOTICE_PERIOD timer asked for it, and no letter of the file carrying a name or an address.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-008 | A notice is refused, undeliverable or has no proof in the window | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. |
| MSG-P6-001 | A contact stop blocks the letter | Contact with this customer is stopped for {reason}. |
| MSG-P3-004 | A legal hold or deviation blocks the letter | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P6-003 | The template was withdrawn before dispatch | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-004 | WIN acknowledged the notice | {notice} was sent for registered mail on {date}. |
| MSG-P6-005 | The template of the notice is not approved | Not specified in the source documents (GAP-1096; ASM-2044) |
| MSG-P3-005 | A notice of this type is already in progress for the case | Not specified in the source documents (GAP-1096; ASM-2044) |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Litigation right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The notice is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-001 | Notice type missing | Enter {field}. |

MSG-P6-008, MSG-P6-001, MSG-P3-004, MSG-P6-003, MSG-P6-004, MSG-P7-003, MSG-P4-003 and MSG-GEN-001 are copied unchanged from the legacy story. MSG-P4-002 is the platform refusal message of the authorise contract. MSG-P6-005 and MSG-P3-005 are named by the legacy contract of the POST and their text is not given by the legacy story or the P6 extracts, so the placeholder stands until their owner publishes it.

### 15. Screens and states

SCR-18 Notice approval, built in RWB-E2-014 and served through the gateway-bff composite route (DP-19), shows the states this story sets:

| State | What the user sees and does |
|---|---|
| Sent | Sent date and barcode; the litigation officer waits for proof |
| Delivered | Callback date and the notice period end date from the timer |
| Unserved | The result and MSG-P6-008; the litigation officer chooses an alternate service method on the case (R-LIT-10, Epic 5) |
| Held | The hold reason (CONTACT_STOP_X1, LEGAL_HOLD or TEMPLATE_WITHDRAWN) and the message of section 14 that goes with it; nothing is in the dispatch file |
| Empty | Not specified in the source documents (CG-ALL-6555) |
| Loading | Not specified in the source documents (CG-ALL-6555) |
| Error | Not specified in the source documents (CG-ALL-6555) |
| No access | Not specified in the source documents (CG-ALL-6555) |

SCR-04 Case timeline shows each ledger entry with its conduct check result, read from rwb-source-data through the composite route. States of SCR-04: empty, loading, error and no access, each Not specified in the source documents (CG-ALL-6554). SCR-44 Batch and job monitor shows the 16:00 run, its file, its acknowledgement and its rerun, and it reads the workflow and the run records of this service and not a Quartz row. States of SCR-44: empty, loading, error and no access, each Not specified in the source documents (CG-ALL-6556). The screen field list, the composite route specification and the field-level masking of the screens belong to RWB-PLT-N001-CON and to the stories that own each screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-021-01 | AC1 (run by RWB-ITG-E2021-ITG), BR1 | End to end | N-0101 Approved; acknowledgment RR223344556TH; legacy AC1 is owned by RWB-ITG-E2021-ITG, and this story answers the rwb-comms half behind the fakes |
| TC-E2-021-02 | AC2 (run by RWB-ITG-E2021-ITG), BR5 | End to end | INT-15 DELIVERED, call-back 18122026; legacy AC2 is owned by RWB-ITG-E2021-ITG |
| TC-P6-E2021-APP-01 | AC3, BR6 | End to end | INT-15 UNDELIVERABLE |
| TC-E2-021-04 | AC4 (run by RWB-ITG-E2021-ITG), BR2 | End to end | Open X1 with contact stop; legacy AC4 is owned by RWB-ITG-E2021-ITG, and AC9 proves the X2 fact reaching the check here |
| TC-E2-021-05 | AC5 (run by RWB-ITG-E2021-ITG), BR4, BR10 | End to end | Postal consent WITHDRAWN, DEMAND notice; legacy AC5 is owned by RWB-ITG-E2021-ITG |
| TC-P6-E2021-APP-10 | AC6, BR7 | End to end | N-0102 sent 2026-12-15 and N-0103 sent 2026-12-16; proof-window workflow on 2026-12-22 |
| TC-P6-E2021-APP-02 | AC7, BR3 | End to end | Legal hold true |
| TC-P6-E2021-APP-03 | AC8, BR8 | End to end | DEMAND-SSME TH v1 withdrawn 2026-12-13 |
| TC-P6-E2021-APP-04 | AC9, BR9 | End to end | Open X2 with stop; decision record store stubbed unavailable |
| TC-P6-E2021-APP-11 | AC10 | End to end | POST repeated with one Idempotency-Key |
| TC-P6-E2021-APP-12 | AC11 | End to end | N-0200 outside scope |
| TC-P6-E2021-APP-13 | AC12 | End to end | POST with no notice type |
| TC-E2-021-13 | Access | Component | RW-CASEOWN sends POST /cases/{caseId}/notices; refused with MSG-P4-002 |
| TC-E2-021-14 | Principle 5 | NFR | Decision record write forced to fail on 10 unserved results; no notice changes |
| TC-E2-021-15 | §12 operations, events and activities | Contract | Mocks of rwb-case, rwb-decision and rwb-deviation; POST and GET of notices; events on rwb.comms.events.v1 |
| TC-E2-021-16 | §12.7 tables | Component | Each table of section 12.7 is written and read only by its owner; no foreign key crosses a service boundary |
| TC-E2-021-17 | BR11 | Component | Notice, dispatch file reference and proof dates written and read in rwb_comms only |
| TC-E2-021-18 | BR12 | Component | State change and outbox row written in one transaction; event carries the CloudEvents envelope |
| TC-E2-021-19 | BR13 | Component | Dispatch run and proof-window step run as a Temporal Schedule and a workflow; no Quartz row or shared job table read |
| TC-E2-021-20 | BR14 | NFR | Each cross-service call is one hop with a 2 s budget; a missing answer never allows a letter |
| TC-E2-021-21 | BR15 | Component | Eligible states, proof window and statutory notice types read from rwb-case reference data with the version in force |
| TC-E2-021-22 | BR16 | Contract | Ledger entry written through the rwb-source-data contract; decision record written through the local library |
| TC-E2-021-23 | BR17 | Contract | Case status move and NOTICE_PERIOD timer applied by rwb-case from the DELIVERY_FAILED and PROOF_WINDOW_EXPIRED facts |
| TC-E2-021-24 | BR18 | Component | Alternate and substituted service methods not offered; only the unserved outcome and reason are recorded |
| TC-E2-021-25 | BR19 | Component | Dispatch file and events carry document reference, barcode and dates; no name, address or account number |
| TC-P6-E2021-APP-05 | AC14, BR4 | Component | Postal consent WITHDRAWN, DEMAND notice; statutory notice still sent |
| TC-E2-021-27 | AC15, BR11 to BR19 | Component | Guardrail and boundary check; evidence in TC-E2-021-17 to TC-E2-021-25 |
| TC-E2-021-28 | AC16 | Component | 401 without credentials; 403 with RW-CASEOWN on POST /cases/{caseId}/notices |
| TC-E2-021-29 | AC17, BR14 | NFR | Cross-service call past its 2 s budget; activity retry and timeout |
| TC-E2-021-30 | AC18 | Component | Status change not allowed by the notice model is refused |
| TC-E2-021-31 | AC13 | Component | Open X1 or X2 deviation with contact stop on; notice held, case to deviation owner, MSG-P6-001 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR. The fourteen legacy cases keep their legacy order and their legacy data; TC-E2-021-15 and TC-E2-021-16 are added for section 12, and TC-E2-021-17 to TC-E2-021-25 for BR11 to BR19. TC-E2-021-01, -02, -04 and -05 are kept here because the rwb-comms half of each runs in this service, and their end-to-end evidence is owned by `RWB-ITG-E2021-ITG`, which carries the -ITG copies.

Version 3: rows that cite `TC-P6-E2021-APP-` identifiers are this story's rows of Recovery Workbench Test Cases v9. Where a shared legacy identifier now names another story's case there, this story's identifier replaces it, and cases run by one identifier are joined in one row.

### 17. Guardrails

- No business value in code: the proof window, the statutory notice type list, the eligible states, the hold reason vocabulary and the delivery-result code map are data rows and parameters read with the version in force.
- No personal data in events, logs, workflow inputs, tests or prompts: notice IDs, case IDs, barcodes, dates, result codes and business dates only. The notice body and the addressee stay in rwb-document and rwb-source-data, and the dispatch file carries a document reference and a barcode.
- No read of another service's tables and no `v_ace_*` read of this service: the case hold, the contact stop, the consent, the ledger and the proof rows arrive on the owner's contract (DP-01, DP-05, DP-18).
- ACE data only through the owner's contract or the owner's views: the ACE proof rows of the legacy story are read from the rwb-source-data proof-of-delivery read, and no SQL of this service names an ACE view.
- The conduct check runs inside the same transaction that selects the notice for the file, so a stop raised after the check reaches the next run and never a second file.
- A held or unserved result that cannot be recorded does not proceed: the state is unchanged, the file is not written and the incident is raised (R-UNI-39).
- Every outbound event and the decision record are written to the outbox in the same transaction as the state change and carry IDs and facts only (DP-09, DP-03).
- One base, one topic, one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; no story in this key declares another service's base or topic as its own (DP-13, DP-14).
- One hop and 2 s on every call; a timeout never passes the conduct check and never returns a notice as clean (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-P6-E2021-APP-01, TC-P6-E2021-APP-10, TC-P6-E2021-APP-11, TC-P6-E2021-APP-12, TC-P6-E2021-APP-13 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05, FEAT-OCC-06 | 16 Manage risk, control and compliance | R-LIT-05, R-UNI-20, R-LIT-04, R-UNI-39 | TC-E2-021-04, TC-P6-E2021-APP-02, TC-P6-E2021-APP-03, TC-P6-E2021-APP-04, TC-E2-021-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05 | 16 Manage risk, control and compliance | R-UNI-10 | TC-E2-021-05 |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-LIT-07, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-P6-E2021-APP-01, TC-E2-021-13 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-021, disposition Split (rework) |
| Legacy criteria owned here | AC3, AC6, AC7, AC8, AC9, AC10, AC11, AC12, each tagged (legacy RWB-E2-021 ACn) |
| Legacy criteria owned by RWB-ITG-E2021-ITG | AC1, AC2, AC4, AC5 |
| Test cases | TC-E2-021-01 to TC-E2-021-25: TC-01 to TC-14 in the legacy order, TC-15 and TC-16 for section 12, TC-17 to TC-25 for BR11 to BR19 |
| Decoupling patterns | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-016 (reusable Temporal layer, Schedules replace Quartz), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership) |
| Rules | R-DEV-01, R-LIT-04, R-LIT-05, R-LIT-07, R-LIT-08, R-LIT-09, R-LIT-10, R-LIT-11, R-UNI-10, R-UNI-20, R-UNI-39 |

The supporting features of the legacy key — FEAT-OCC-01 (generate a letter), FEAT-OCC-02 (dispatch and proof), FEAT-OCC-05 (conduct check) and FEAT-ILG-07 (dispatch outcomes to the ledger) — are answered here for the rwb-comms slice and by the other services for their own slices, and this story changes none of their designs.

### 19. Out of scope

- Legacy AC1 (dispatch), AC2 (proof back), AC4 (contact stop blocks the letter) and AC5 (consent withdrawn does not stop a statutory notice): end-to-end journeys owned by `RWB-ITG-E2021-ITG`. The legacy AC4 wording, including the phrase "does not writ notice", is copied there and not here.
- Notice generation: RWB-P6-E1052-APP and RWB-P6-E1052-CON. This story consumes the notice it creates.
- Proof-of-delivery capture design with WIN: RWB-P6-E1055-APP, its contract `RWB-P6-E1055-CON` and its deployment story. This story applies the design and the result-code map.
- SMS and LINE dispatch through NSS and LINE OA: RWB-P6-E2022-APP, RWB-P6-E2022-CON and RWB-P6-E2022-OPS.
- The NOTICE_PERIOD timer, the case status, the queue transfer and the legal hold: rwb-case (P3). This story sends the facts and reads the answers.
- The WIN file window, the file runs and the outbound items: rwb-integration (P2, DP-16). This story calls the file contract and stores only the reference.
- The ACE proof rows, the contact points and the ledger: rwb-source-data (P1, DP-05, DP-18). This story reads and writes through that contract and never through a view of its own.
- The approval itself, the approval levels and the central decision ledger: rwb-decision (P7), with the D7.1 screen in RWB-P7-E2014-APP.
- Alternate service methods and substituted service (R-LIT-10, R-LIT-11, Epic 5).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
- The deployment, the dashboards, the alerts and the runbook of this capability: RWB-P6-E2021-OPS.
- The contract documents, the dispatch file schema and the fakes as published artefacts: RWB-P6-E2021-CON.

### 20. Remaining delivery steps

- Size, contract version and epic design sign-off: Not specified / Pending. Owner: squad, contract owner and solution architect.
- RWB-P6-E2021-CON v3 baselined and rwb-source-data provider fake 5.1.0 published: Pending. Owner: contract owners.
- DP02 records right, proof-of-delivery read right and Case record C for the rwb-comms identity: Pending. Owner: platform administrator.
- Settle GAP-2096, NEW-GAP-F14-5, F14-8, F14-9 and NEW-GAP-D3, and update the ledger-key test data in Test Cases v9: Pending. Owner: solution architect, contract owners and test lead.
- Test case rows in Test Cases v9 and synthetic data in DEV: Pending. Owner: QA.
