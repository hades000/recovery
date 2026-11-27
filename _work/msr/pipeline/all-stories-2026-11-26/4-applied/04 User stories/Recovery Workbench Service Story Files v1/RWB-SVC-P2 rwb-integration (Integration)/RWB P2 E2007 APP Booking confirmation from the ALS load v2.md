# RWB-P2-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P2-A |
| Ready to start | After RWB-P2-E1007-APP |
| Depends on (build) | RWB-P2-E2007-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P2-E1007-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E2004-CON, RWB-P3-E2042-CON |
| Integration dependencies | None |
| External dependencies | RWB-P2-E2007-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-CHO-008) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-007 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P2-E2007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT) and a Credit Administration officer (RW-CREDITAD)**, I want **the booked terms of each approved restructure or settlement compared with the account as ACE holds it after the next ALS batch, with one task when the booking is missing or differs**, so that **every approved decision is confirmed as booked in the core bank without a file the Workbench has to load, and no approved treatment waits unnoticed in an operations-waiting state**.

The legacy story put the match, the job, the ACL read, the task texts, the treatment columns and the case move in the P2 Integration module of the monolith. Under D-RCV-60 the work is split by owner, and this story is the rwb-integration part: `BookingMatchService`, `BookingMatchFacts`, the JOB-08 run (`BookingMatchJob`), `TreatmentApprovedListener` and `BookingRunSummaryWriter`; JOB-08 is an event-started workflow of this service and not a Schedule (DP-10; GAP-0657; ASM-1114). The case route state, the task rows and the case-side decision record are rwb-case's, carried by RWB-P3-E2007-APP. The treatment record, its APPROVED to BOOKED state, `booked_at`, the booking difference and the treatment-side decision record are rwb-treatment's, carried by the S2 story of this legacy key. The ACE account and batch-status read is rwb-source-data's, carried by RWB-P1-E2007-APP, because only rwb-source-data reads the `recovery.v_ace_*` views and ACE data (ADR-010, DP-05). The BOOKING_MATCH registry rows and the package version in force are rwb-decision's, carried by RWB-P7-E2007-APP behind RWB-P3-E2042-CON. The authorise decisions around the read of the booked terms and the booking tasks are rwb-access's, carried by RWB-P4-E2007-APP.

What stays here is the decision: which treatments are read, which facts are built, which row of package BOOKING_MATCH decides, what outcome is written back through the owners' contracts, and which task each outcome raises with which text. This story meets REQ-CHO-008 and is measured by REC-03 (approved treatments against bookings, zero after two days).

### 2. Business rationale

The officer books restructures and settlements by hand in ALS (INT-03), and nothing checks today that the booked terms equal the approved terms. ACE ingests the ALS batch and the booked terms appear on the account. The match compares each approved treatment with the account as ACE holds it for the business date once the ACE batch for ALS is COMPLETE, asks for the treatment to be marked booked when the terms match, and raises a task to the officer when the booking is missing or to Credit Administration when the terms differ.

The compared terms, the tolerance and the outcomes are rows of package BOOKING_MATCH (ADR-012; D-RCV-36 T3, T5). The embedded Drools kit evaluates the package for each treatment and account, the result names the row that fired and the package version, and the service holds no comparison code and no rule table of its own (DP-04).

**What the split changes, and why it changes here.**

- **DP-01.** `rwb_integration` holds no copy of a treatment, a case, an account or a task, and no foreign key into another schema. The match reads at run time and writes nothing but its own library rows.
- **DP-03.** The `DecisionLogWriter` of the monolith becomes the local decision-record library: one record per treatment and business date, written in `rwb_integration` in the same local transaction as the outcome, and published as `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`. A decision that cannot be recorded does not proceed (R-UNI-39; CTL-06), so no `markBooked` call leaves the service when the record cannot be written.
- **DP-04.** `RuleEvaluator` becomes the embedded Drools kit of RWB-PLT-E1072-CON with the BOOKING_MATCH package fetched from rwb-decision through the rule-model read and the version-in-force check of RWB-P3-E2042-CON. No second engine runs and no workbook is read here.
- **DP-05.** `AceSourceQuery`, `v_ace_account` and `v_ace_batch_status` disappear from this service. The account facts and the batch-completeness answer are read through the rwb-source-data contract. The TSD P2 Integration v3 T5.2 sentence that P2 reads the views directly is superseded by ADR-010 and DP-05; `rwb_integration` holds no grant on the `recovery` schema (GAP-0657; ASM-1115).
- **DP-06, DP-07.** The grace parameter `booking.missing.grace_loads`, the treatment types and the task codes are rows of rwb-case read through its parameters and reference-data contracts with the version in force; nothing of the sort is written in Java.
- **DP-09.** Every consumed event is deduplicated through the inbox library, and the outcome's record and outbox row are written in the same local transaction.
- **DP-10.** The Quartz job JOB-08 becomes an event-started Temporal workflow on queue `rwb-integration` in namespace `rwb-recovery`, started by `AceDataReady`. No Schedule is created in the target (Arch v5 slides 42 and 44; GAP-0657; ASM-1114).
- **DP-11.** The in-process calls to `TreatmentQuery`, `TreatmentCommands`, `CaseAccounts`, `BatchStatusQuery`, `RuleEvaluator`, `TaskApi` and the reconciliation writer become contract calls with fakes, one hop and a 2 s timeout each.
- **DP-13.** The service's own operation moves on to `/api/recovery/integration/v1`, and the `rwb.integration.events.v1` topic and the `rwb-integration` task queue keep the naming rule.
- **DP-19.** The officer's screens stay SCR-14 Treatment record and SCR-01 My work, served by gateway-bff from rwb-case, rwb-treatment and rwb-access; this story supplies the run and the tasks, never a page.

**Two rulings that this story follows rather than re-opens.** First, JOB-08 and its activities belong to rwb-integration in this realignment, as RWB-P4-E2007-APP and RWB-ITG-E2007-ITG both state, although Architecture v5 slide 44 names rwb-payment as the owner and slides 42 and 43 list rwb-payment, not rwb-integration, among the consumers of `AceDataReady` and `TreatmentApproved` (GAP-0657; ASM-1114). Second, no data lake exists in the target (DP-17), and nothing in this key builds, sends or reads a lake file; the REC-03 result reaches reporting as a row of the reconciliation answer and, from there, as events (ASM-1120).

The legacy story also carried five statements that are not this slice's and are proved elsewhere: the case move on BOOKING_CONFIRMED and SETTLEMENT_BOOKED with the route state and the decision log entry (AC1, RWB-P3-E2007-APP), the ACE batch gate and the missing-booking suppression of AC5 (ACE batch facts from RWB-P1-E2007-APP, proven end to end in RWB-ITG-E2007-ITG), the absence of a second task on the next batch of AC7 (RWB-P3-E2007-APP), the treatment state and the difference column (S2 story of this legacy key), and the refusal of a role without the right (RWB-P4-E2007-APP). This story cites them and builds none of them.

### 3. Preconditions

- RWB-P2-E2007-CON is published: the booking-confirmation contract baseline of this key, with the match request and result shape, the three task codes and their message IDs, the `TreatmentBooked` envelope it relies on, the job administration operations, the error envelope, the idempotency rule and the fakes for rwb-source-data, rwb-case, rwb-decision and rwb-treatment (DP-11).
- RWB-P2-E1007-APP is delivered: the integration base, its controller conventions, its problem-response mapping, its contract-client and idempotency handling, its Temporal worker, its topic and its job catalogue read.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). The library writes the record and publishes `rwb.decision-record.DecisionRecorded.v1` on the service's behalf.
- RWB-PLT-E1072-CON is published: the embedded Drools kit with `RuleResult`, `NoPackageInForce`, first-match semantics and the `KieBaseRegistry` bound of 20 versions (DP-04).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the platform client libraries for the parameters and reference-data contracts of rwb-case (DP-06, DP-07).
- RWB-PLT-TE006-CON is published: the outbox, inbox and idempotency library, with `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` created in `rwb_integration` (DP-09).
- RWB-PLT-E1071-CON is published: the workflow kit, the namespace `rwb-recovery`, the task queue `rwb-integration`, worker versioning and the activity retry policy (DP-10).
- RWB-PLT-N001-CON is published: the gateway-bff composite routes of SCR-14 and SCR-01, which reach rwb-treatment, rwb-case and rwb-access and never this service's run (DP-19).
- RWB-P3-E2004-CON is published: the treatment contract of the case fold, which fixes the approved-not-booked list read, the single treatment read, the mark-booked write and the booking-difference write that this story calls (C dependency; DP-11).
- RWB-P3-E2042-CON is published: the rule-model read `GET /rule-models/{n}/{v}` and the package-version-in-force answer that the BOOKING_MATCH evaluation runs against (C dependency; DP-04).
- RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: the parameters contract carrying `booking.missing.grace_loads` and the reference-data contract carrying the treatment-type and task-code LOV rows (C dependency; DP-06, DP-07).
- Package BOOKING_MATCH version `BKG-2026.12` is in force on the business date, with a RESTRUCTURE row comparing `tdr_flag`, `last_tdr_date` and `principal_outstanding` against `offer_amount` and `interest_rate` against the approved rate, a SETTLEMENT row comparing `settlement_booked_date` and `settlement_booked_amount` against `offer_amount`, and tolerance 0.00 baht (DL25). The rows are loaded, tested, approved and promoted by RWB-E2-042 and RWB-P7-E2007-APP; this story evaluates them and holds no copy (GAP-0657; ASM-1118).
- The ACE batch for ALS with business date D is COMPLETE, as the rwb-source-data freshness answer states it, and the account facts for D carry the booked terms: `tdr_flag`, `last_tdr_date`, `principal_outstanding`, `interest_rate` for a restructure, and `settlement_booked_date` and `settlement_booked_amount` for a settlement, the last two from the Section B columns of RWB-ACE-001 (RWB-P1-E2007-APP; GAP-0657; ASM-1115).
- The parameter `booking.missing.grace_loads` is 1 (one ALS batch after approval) in the rwb-case parameters contract with the version in force.
- Rules R-RES-22 and R-SET-13 are in force for the case move that follows a confirmed booking; this story reads no route row and evaluates no route package.
- The login is the rwb-integration login (DP-02): Not specified in the source documents (GAP-0657; ASM-1113).
- No Schedule is created and none is needed: JOB-08 is an event-started workflow (DP-10; GAP-0657; ASM-1114).

### 4. Flow

1. rwb-source-data publishes `rwb.source-data.AceDataReady.v1` for ALS with business date D; the inbox of `rwb_integration` records the event under its consumer group and `BookingMatchWorkflow` starts on queue `rwb-integration` with the workflow ID prefix `booking-match-`.
2. `BookingMatchWorkflow`: reads the feature flag `rwb.integration.booking-confirmation` from the platform flag library at the start of the run; off ends the run as skipped with no read and no write.
3. `readBookedTerms` activity: asks the rwb-source-data freshness answer for the ALS batch of business date D; a batch that is not COMPLETE ends the run with MSG-P1-001 and no missing-booking task for D, which is the legacy AC5 statement that the integration harness proves end to end.
4. `listApprovedTreatments` activity: reads the approved RESTRUCTURE and SETTLEMENT treatments not yet booked through the rwb-treatment contract, with the treatment types taken from the reference-data LOV rows in force and the grace count taken from `booking.missing.grace_loads`.
5. `readBookedTerms` activity: for each treatment, reads the treatment's case accounts through the rwb-source-data contract at business date D together with the booked terms of each account; no account row is copied and nothing is cached in `rwb_integration`.
6. `evaluateBookingMatch` activity: builds `BookingMatchFacts` for the treatment and each account — the treatment type, the approved terms, the account fields and the business date — and evaluates package BOOKING_MATCH through the embedded kit; the `RuleResult` names the row that fired, the package version, the outcome `BOOKED`, `NO_BOOKING` or `TERMS_DIFFER`, and the difference terms.
7. The workflow: a `NoPackageInForce` answer from the kit ends the run as failed with MSG-P3-027 for package BOOKING_MATCH and the business date, writes no record, marks nothing and raises no task (AC9).
8. The workflow: checks the idempotency record of the treatment ID and business date D through the idempotency library; a treatment already handled for D is skipped with no second record, no second call and no second task (AC6).
9. `applyBookingOutcome` activity, outcome `BOOKED` for every account: writes the local decision record with the fired row, the package version and the booking reference in the same local transaction as its outbox row (DP-03); then calls the mark-booked write of the rwb-treatment contract with the business date and the booking reference (`account_key` + business date, never an account number). rwb-treatment writes `booked_at`, moves the treatment state to BOOKED and emits its own record; rwb-payment publishes exactly one `rwb.payment.TreatmentBooked.v1` for the confirmation, and rwb-case moves the route state by R-RES-22 or R-SET-13 in RWB-P3-E2007-APP.
10. `applyBookingOutcome` activity, outcome `NO_BOOKING` after the grace batches: writes the decision record, leaves the treatment APPROVED and returns the accounts without a booking to the workflow.
11. `applyBookingOutcome` activity, outcome `TERMS_DIFFER`: writes the decision record, then records the difference terms on the treatment through the booking-difference write of the rwb-treatment contract; the treatment stays APPROVED.
12. `raiseBookingTasks` activity: raises one task per treatment through the `raiseTask` operation of the rwb-case contract — `WITH_OPS_BOOKING` or `WITH_OPS_SETTLEMENT` for role RW-RESTRUCT with MSG-P2-011 naming the accounts not booked, or `UNMATCHED_EXCEPTION` for role RW-CREDITAD with MSG-P2-012 naming the term, the booked value and the approved value. One open task per case, task code and treatment; a second run raises none (AC6).
13. `writeRunSummary` activity: writes the run summary (treatments read, booked, missing, differing) and the REC-03 result through the reconciliation write of the rwb-source-data contract, so the data steward's break list shows a treatment missing for the number of days it has been missing (the legacy AC7 evidence).
14. The workflow ends and records its outcome: `COMPLETED`, `FAILED` on the no-package path or `SKIPPED` on the flag or the batch gate. The outbox relay publishes the `DecisionRecorded` events written by the library, and the service publishes nothing of its own on `rwb.integration.events.v1` for this key.
15. A platform administrator may rerun JOB-08 for a business date through `POST /api/recovery/integration/v1/admin/jobs/{jobId}/rerun` under `Idempotency-Key`; a treatment already handled for that date is skipped, and a run still open answers 409 with MSG-P2-006 (AC6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No booking in the next ALS batch for a treatment past the grace count | One task `WITH_OPS_BOOKING` or `WITH_OPS_SETTLEMENT` to RW-RESTRUCT naming the accounts not booked; the treatment stays APPROVED | MSG-P2-011 | AC2, AC4 |
| X2 | A booked term differs from the approved term | The difference is recorded on the treatment through its contract and one task `UNMATCHED_EXCEPTION` goes to RW-CREDITAD | MSG-P2-012 | AC3 |
| X3 | Only some accounts of the case are booked | The treatment stays APPROVED and the task names the accounts without a booking | MSG-P2-011 | AC4 |
| X4 | The ACE batch for ALS with business date D is not COMPLETE | The run ends before any treatment is read; no missing booking is raised for D | MSG-P1-001 | Cross-slice: RWB-P1-E2007-APP and RWB-ITG-E2007-ITG AC5 |
| X5 | JOB-08 runs twice for the same business date | The idempotency record drops the repeat: no second record, no second mark-booked call, no second event and no task | None | AC6 |
| X6 | A booking is still missing on the next batch | No second task; the open task stays and the REC-03 result counts the days | None | Cross-slice: RWB-P3-E2007-APP and the REC-03 answer of RWB-P1-E2007-APP (legacy AC7) |
| X7 | The local decision record cannot be written | Nothing is written and no remote call is made; an incident is raised and the match runs again with the next batch | MSG-P7-003 | AC8 |
| X8 | A role without Platform administration U asks for a rerun | Refused by rwb-access before the handler runs; nothing changes | MSG-P4-002 | Cross-slice: RWB-P4-E2007-APP (TC-E2-007-10) |
| X9 | No BOOKING_MATCH version is IN_FORCE for the business date | `NoPackageInForce`; no treatment marked booked, no difference written, no task raised; the run ends failed and alerts RW-PLATADM | MSG-P3-027 | AC9 |
| X10 | The rwb-treatment, rwb-source-data, rwb-case or rwb-decision contract does not answer inside the budget | One hop, 2 s timeout (DP-11); the activity is retried by the kit policy, the treatment is not marked and the next run for the business date picks the treatment up; the failure is counted on the run summary | MSG-GEN-006 | AC1, in the OPS series |
| X11 | The BOOKING_MATCH model checksum does not match the version in force | The kit refuses the model, the run ends failed, and nothing is marked or raised | MSG-P3-027 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the integration base, the contract baseline of this key and the platform kits; the rwb-treatment, rwb-source-data, rwb-case, rwb-decision and rwb-access answers come from their contract fakes |
| Negotiable | The compared terms, the tolerance, the grace count, the treatment types and the task codes are registry rows, parameters and reference rows; the story fixes only the decision path |
| Valuable | Every approved restructure and settlement is confirmed as booked or raised to the role that can act, with the fired row and the package version on the record |
| Estimable | One event-started workflow, six activities, four consumed contracts, one decision record and one run summary |
| Small | Fits two weeks with its tests |
| Testable | Each owned criterion is one automated test with a fixture; every cross-service answer is stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Booking confirmation from the ALS load

  Background:
    Given package "BOOKING_MATCH" version "BKG-2026.12" is in force with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht
    Given the ACE batch for ALS with business date 2026-12-16 is COMPLETED
    Given the rwb-decision contract mock returns package "BOOKING_MATCH" version "BKG-2026.12" with the RESTRUCTURE and SETTLEMENT rows and tolerance 0.00 baht
    Given the rwb-source-data contract mock returns the ACE batch for ALS with business date 2026-12-16 as COMPLETE

  Scenario: AC2 Booking missing (legacy RWB-E2-007 AC2)
    Given restructure treatment "TRT-SYN-0702" was approved on 2026-12-15
    Given v_ace_account at business date 2026-12-16 shows tdr_flag false for synthetic account "A-0702"
    Given the rwb-treatment contract mock returns restructure treatment "TRT-SYN-0702" approved on 2026-12-15 with state "APPROVED"
    Given the rwb-source-data contract mock returns tdr_flag false for synthetic account "A-0702" at business date 2026-12-16
    When the match runs
    Then the RESTRUCTURE row of package "BOOKING_MATCH" returns the outcome "NO_BOOKING"
    Then the system raises a task "WITH_OPS_BOOKING" for role "RW-RESTRUCT" with message MSG-P2-011
    Then the treatment stays "APPROVED"

  Scenario: AC3 Terms differ (legacy RWB-E2-007 AC3)
    Given restructure treatment "TRT-SYN-0703" was approved with offer amount 1,800,000.00 baht and rate 4.2500 percent
    Given v_ace_account shows tdr_flag true, last TDR date 2026-12-16, principal 1,800,000.00 baht and rate 4.5000 percent for "A-0703"
    Given the rwb-treatment contract mock returns restructure treatment "TRT-SYN-0703" with offer amount 1,800,000.00 baht and rate 4.2500 percent
    Given the rwb-source-data contract mock returns tdr_flag true, last TDR date 2026-12-16, principal 1,800,000.00 baht and rate 4.5000 percent for "A-0703"
    When the match runs
    Then the RESTRUCTURE row of package "BOOKING_MATCH" returns the outcome "TERMS_DIFFER" with approved rate 4.2500 and booked rate 4.5000
    Then the treatment shows the difference: interest rate approved 4.2500, booked 4.5000
    Then a task "UNMATCHED_EXCEPTION" goes to role "RW-CREDITAD" with message MSG-P2-012
    Then the treatment stays "APPROVED"

  Scenario: AC4 Only some accounts booked (legacy RWB-E2-007 AC4)
    Given restructure treatment "TRT-SYN-0704" covers synthetic accounts "A-0704" and "A-0705"
    Given only "A-0704" shows the booking in v_ace_account at business date 2026-12-16
    Given the rwb-treatment contract mock returns restructure treatment "TRT-SYN-0704" with synthetic accounts "A-0704" and "A-0705"
    Given the rwb-source-data contract mock returns the booking for "A-0704" and no booking for "A-0705" at business date 2026-12-16
    When the match runs
    Then the treatment stays "APPROVED"
    Then the task for "RW-RESTRUCT" names account "A-0705" as not booked

  Scenario: AC6 Match run twice (legacy RWB-E2-007 AC6)
    Given JOB-08 marked "TRT-SYN-0701" booked for business date 2026-12-16
    Given the rwb-treatment contract mock returns settlement treatment "TRT-SYN-0701" with state "BOOKED" and booked at 2026-12-16
    Given the rwb-treatment contract mock returns one accepted mark-booked call for business date 2026-12-16
    When JOB-08 is rerun for 2026-12-16
    Then the system publishes no second TreatmentBooked event
    Then the system raises no task

  Scenario: AC8 Decision log write fails on confirmation (legacy RWB-E2-007 AC8)
    Given the decision log store is unavailable
    Given the rwb-treatment contract mock returns settlement treatment "TRT-SYN-0701" with state "APPROVED"
    Given the rwb-treatment contract mock returns no mark-booked call
    When the match finds "TRT-SYN-0701" booked
    Then the treatment stays "APPROVED" and no TreatmentBooked event is published
    Then the system raises an incident with message MSG-P7-003
    Then the match runs again with the next batch

  Scenario: AC9 No BOOKING_MATCH version in force (legacy RWB-E2-007 AC9)
    Given no BOOKING_MATCH version is IN_FORCE on 2026-12-17
    Given the rwb-decision contract mock returns no BOOKING_MATCH version in force on 2026-12-17
    Given the rwb-treatment contract mock returns no mark-booked call and no difference write
    When JOB-08 starts for business date 2026-12-16
    Then NoPackageInForce is thrown with MSG-P3-027 for package "BOOKING_MATCH"
    Then no treatment is marked booked, no difference is written and no task is raised
    Then the run ends as failed and alerts role "RW-PLATADM"
```

The six criteria above are copied unchanged from legacy RWB-E2-007, values included, with one `Given the <service> contract mock returns <x>` line added wherever a cross-service answer is stubbed; no legacy line was removed and no legacy value was changed. The package code, its version and its rows are the registry's values and are cited here, not restated (GAP-0657; ASM-1118). AC2, AC3 and AC4 are proved here in full, because the match outcome and the task text are this story's output. AC6 is proved here at Component level: the idempotency record, the single mark-booked call and the absence of a second task are this workflow's behaviour, while the absence of a second route state move and a second `CaseStateChanged` is RWB-P3-E2007-APP's. AC8 is proved here in the sense that matters for this slice: when the local decision record cannot be written, the mark-booked call is not made at all, so the treatment cannot have changed; the case-side and treatment-side proofs that they did not change are the P3 and S2 stories'. AC9 is proved here, because the package-version-in-force check is evaluated inside this workflow.

The remaining criteria of legacy RWB-E2-007 are not owned here: AC1 (booking confirmed), AC5 (ACE batch not complete) and AC7 (booking still missing on the next batch) are the integration harness's, carried by RWB-ITG-E2007-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Bookings are made by the officer in ALS and confirmed only from the next ACE batch | INT-03; DL12; D-RCV-35 U1 |
| BR2 | A restructure is booked when every account matches the RESTRUCTURE rows of package BOOKING_MATCH: `tdr_flag` true with a last TDR date on or after the approval date and the terms equal | DF-ACE-031; DF-ACE-030; CTL-26; D-RCV-36 T5 |
| BR3 | A settlement is booked when the account matches the SETTLEMENT rows of package BOOKING_MATCH: a settlement booked date on or after the approval date and a booked amount equal to the offer amount | R-SET-13; D-RCV-36 T5 |
| BR4 | The tolerance on amounts and rates is zero in the row of package BOOKING_MATCH in force | DL25 |
| BR5 | A missing booking after the grace batches raises one task to the officer, naming the accounts not booked | REC-03; parameter `booking.missing.grace_loads` |
| BR6 | A difference in terms raises one task to Credit Administration and records the difference on the treatment; the treatment stays APPROVED | REC-03; FEAT-CHO-08 |
| BR7 | A confirmed booking is asked for through the treatment contract; the case move that follows is rwb-case's | R-RES-22, R-SET-13; RWB-P3-E2007-APP |
| BR8 | No missing booking is raised for a business date whose ACE batch for ALS is not COMPLETE; the batch answer is read from the rwb-source-data contract | JOB-08; CTL-02; DP-05; ADR-010 |
| BR9 | A decision that cannot be written to the local decision record does not proceed: no remote call is made and an incident is raised | Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR10 | The match is decided by package BOOKING_MATCH through the embedded kit; the result names the row and the package version, and the story holds no comparison code and no rule table | D-RCV-36 T3, T5; ADR-012; DP-04; GAP-0657; ASM-1118 |
| BR11 | No BOOKING_MATCH version in force is a refusal (`NoPackageInForce`), never a default match | R-UNI-41; D-RCV-36 T7 |
| BR12 | Only rwb-source-data reads the `recovery.v_ace_*` views and ACE data; every account fact of this match arrives through its contract, and `rwb_integration` holds no grant on `recovery` | ADR-010; DP-05; Arch v5 slides 41 and 45; GAP-0657; ASM-1115 |
| BR13 | `rwb_integration` holds no copy of a treatment, a case, an account or a task and no foreign key into another schema; the treatment is written only through rwb-treatment, the task only through rwb-case and the REC-03 result only through rwb-source-data | DP-01; Arch v5 slide 41 |
| BR14 | JOB-08 is an event-started workflow started by `AceDataReady`, not a Schedule; one run per business date and one record per treatment and business date | DP-10; Arch v5 slides 42 and 44; GAP-0657; ASM-1114 |
| BR15 | One open booking or terms task per case, task code and treatment; a repeated run raises none and cancels none | Legacy RWB-E2-007 X5, X6; BR5 and BR6 here |
| BR16 | No data lake and no lake file: the REC-03 result is a row of the reconciliation answer, and reporting reads events | DP-17; Arch v5 slide 37; GAP-0657; ASM-1120 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| `NOT_STARTED` | `AceDataReady` for ALS with date D | The flag is on and the batch for D is COMPLETE | `RUNNING` |
| `NOT_STARTED` | `AceDataReady` for ALS with date D | The flag is off, or the batch for D is not COMPLETE | `SKIPPED`, with MSG-P1-001 on the batch gate |
| `RUNNING` | The treatment list is read and the package is in force | The kit returns a `RuleResult` for each treatment and account | `RUNNING` |
| `RUNNING` | `NoPackageInForce` | No BOOKING_MATCH version in force for D | `FAILED`, with MSG-P3-027 |
| `RUNNING` | Every outcome applied and every task raised | The activities completed or were retried to completion | `COMPLETED` |
| `RUNNING` | The local decision record cannot be written | The library refuses the write | `FAILED` for that treatment, with the run continuing, and the treatment stays APPROVED |
| `COMPLETED` | A rerun for the same business date | The idempotency record holds the treatment and D | The treatment is skipped; the run stays `COMPLETED` with an unchanged count |

The treatment state and the route state are not this story's state machines. The treatment moves from APPROVED to BOOKED in rwb-treatment, asked for by the mark-booked call of step 9 and proved in the S2 story of this legacy key; the route state moves from WITH_OPS_BOOKING or WITH_OPS_SETTLEMENT by R-RES-22 or R-SET-13 in rwb-case, proved in RWB-P3-E2007-APP. A missing or differing booking leaves both unchanged. The state this slice owns is the lifecycle of its own run, its decision record and its idempotency record, and all three are readable from the run summary and the reconciliation answer.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-integration service identity (the rwb-integration login, DP-02) | Runs JOB-08, reads the treatment and ACE facts through their owners' contracts, evaluates the package, writes the local decision record and the REC-03 result, and asks for the booking, the difference and the tasks |
| Decision-record library identity | Writes the local decision record in `rwb_integration` with its hash link and outbox row, and publishes `DecisionRecorded` on `rwb.decision-record.v1` (Decision log, C; DP-03) |
| SY-RULES, the embedded Drools kit | Evaluates package BOOKING_MATCH for each treatment and account and returns the fired row, the outcome, the difference terms and the package version |
| rwb-treatment, through its contract | Owns the treatment record, `booked_at`, the booking difference, the APPROVED to BOOKED state and its own record; this story asks and does not write |
| rwb-case, through its contract | Owns the route state, the task rows and the case-side record; this story asks for one task per outcome |
| rwb-source-data, through its contract | The only reader of the ACE views: supplies the accounts with the booked terms, the batch-completeness answer and the reconciliation write behind REC-03 |
| rwb-decision, through RWB-P3-E2042-CON | Owns the BOOKING_MATCH rows, the package versions and the version in force; this story evaluates them |
| rwb-access, through its contract | Decides the Platform administration U right for the rerun |
| RW-RESTRUCT, restructuring officer | Receives the missing-booking task and books in ALS (Treatment and offer, CRUA) |
| RW-CREDITAD, Credit Administration officer | Receives the differing-terms task (Write-off and posting, CRUA) |
| RW-DATASTEW, data steward | Reads the REC-03 break list |
| RW-PLATADM, platform administrator | Reruns JOB-08 for a business date (Platform administration, U) |

The service runs as the rwb-integration login (DP-02); the login name is Not specified in the source documents (GAP-0657; ASM-1113). No role in this story may raise a booking it did not decide: the outcome is the kit's and the task text is the contract's.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment, through the rwb-treatment contract | id | Read |
| DF-TRT-002 | treatment, through the rwb-treatment contract | case_id | Read |
| DF-TRT-004 | treatment, through the rwb-treatment contract | treatment_type | Read |
| DF-TRT-007 | treatment, through the rwb-treatment contract | offer_amount | Read |
| DF-TRT-012 | treatment, through the rwb-treatment contract | booked_at | Read here; written by rwb-treatment (S2 story) |
| DF-TRT-027 | treatment, through the rwb-treatment contract | interest_rate | Read |
| DF-TRT-028 | treatment, through the rwb-treatment contract | booking_difference | Read here; written by rwb-treatment (S2 story) |
| Standard column | treatment, through the rwb-treatment contract | state | Read here; written by rwb-treatment (S2 story) |
| DF-CAS-026 | case_account, through the rwb-case contract | account_key | Read |
| DF-ACE-001 | v_ace_account, through the rwb-source-data contract | account_key | Read |
| DF-ACE-025 | v_ace_account, through the rwb-source-data contract | interest_rate | Read |
| DF-ACC-009 | v_ace_account, through the rwb-source-data contract | principal_outstanding | Read (Section B, RWB-ACE-001) |
| DF-ACE-031 | v_ace_account, through the rwb-source-data contract | tdr_flag | Read |
| DF-ACE-030 | v_ace_account, through the rwb-source-data contract | last_tdr_date | Read |
| DF-ACE-036 | v_ace_account, through the rwb-source-data contract | data_as_of | Read |
| DF-ACC-030 | v_ace_account, through the rwb-source-data contract | settlement_booked_date | Read (Section B, RWB-ACE-001) |
| DF-ACC-031 | v_ace_account, through the rwb-source-data contract | settlement_booked_amount | Read (Section B, RWB-ACE-001) |
| DF-ACE-178 | v_ace_batch_status, through the rwb-source-data freshness answer | source_system | Read |
| DF-ACE-179 | v_ace_batch_status, through the rwb-source-data freshness answer | business_date | Read |
| DF-ACE-182 | v_ace_batch_status, through the rwb-source-data freshness answer | status | Read |
| DF-ACE-186 | v_ace_batch_status, through the rwb-source-data freshness answer | is_complete | Read |
| DF-REF-002 | rule_row, through the rwb-decision rule-model read | rule_id | Read |
| DF-REF-003 | rule_row, through the rwb-decision rule-model read | rule_version | Read |
| DF-WRK-018 | task, through the rwb-case contract | case_id | Write, through the P3 contract |
| DF-WRK-019 | task, through the rwb-case contract | task_code | Write, through the P3 contract |
| DF-WRK-022 | task, through the rwb-case contract | status | Write, through the P3 contract |
| DF-WRK-023 | task, through the rwb-case contract | owner_role | Write, through the P3 contract |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result, through the rwb-source-data contract | all fields | Write (REC-03), through the P1 contract |
| DF-DEC-001 to DF-DEC-018 | decision_record (library table in `rwb_integration`) | all fields, including the fired rule ID, the package version, the outcome and the booking reference | Write |
| DF-REF-159 to DF-REF-184 | reference_row, through the rwb-case reference-data contract | The treatment-type and task-code rows with the version in force | Read |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The two Section B fields keep their frozen field-gap IDs until the LDM assigns DF-ACE IDs to the 12 added columns. No treatment row, no case row, no ACE row and no task row is copied into `rwb_integration`: the service links to them by business key (`treatmentId`, `caseId`, `account_key`) with no foreign key (DP-01, BR13; GAP-0657; ASM-1115). The matching row and its version are read only through the rule-model read of RWB-P3-E2042-CON; this story reads no `rule_row` column directly, no `drl_source` and no workbook. The only write of this slice is the decision record, its outbox row, the idempotency record and the run summary. The element names of the consumed calls are the contract baseline's and are taken from RWB-P2-E2007-CON when it lands (GAP-0657; ASM-1116).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/admin/jobs/{jobId}/rerun` | Rerun JOB-08 for a business date: starts `BookingMatchWorkflow` for the date named in the request and returns the job state; a treatment already handled for that date is skipped | Platform administration U, scope applied; 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 409 while a run is open (MSG-P2-006), 503 on an unwritable record (MSG-P7-003) | `Idempotency-Key` per job and business date; the stored answer is replayed and no second run starts |

The job catalogue read `GET /admin/scheduled-jobs` and the outbox delivery operations are the integration base's, published in RWB-P2-E1007-CON; this story adds the JOB-08 entry that read returns and nothing else to the surface. The rerun is the operation the legacy story named at `POST /admin/jobs/{jobId}/rerun`; the Ownership Map keeps the generic rerun with P1 (`POST /admin/jobs/{jobId}/rerun`, x-module P1 in API Specification v4), while this realignment makes rwb-payment's JOB-08 a rwb-integration job whose rerun only this service can perform, so the operation is served here for the jobs of this service's catalogue and the conflict is carried (GAP-0657; ASM-1116).

The match itself has no REST surface: it is started by an event and its outcome is read through the treatment, the task list and the reconciliation answer. The request and answer shapes of the rerun, and the run-summary field names, are Not specified in the source documents (GAP-0657; ASM-1116).

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout and a breaker per downstream (DP-11).

| Method | Path or operation | Owner | Contracted use |
|---|---|---|---|
| GET | The approved-not-booked treatment list read of the rwb-treatment contract (RWB-P3-E2004-CON) — Not specified in the source documents (GAP-0657; ASM-1116) | S2 rwb-treatment | The approved RESTRUCTURE and SETTLEMENT treatments not yet booked, with the treatment type, the case and the approved terms |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment type, the state, `offer_amount`, `interest_rate`, `booked_at` and the booking difference |
| POST | The mark-booked write of the rwb-treatment contract (RWB-P3-E2004-CON) — Not specified in the source documents (GAP-0657; ASM-1116) | S2 rwb-treatment | Marks the treatment booked with the business date and the booking reference (`account_key` + business date) |
| PATCH | The booking-difference write of the rwb-treatment contract (RWB-P3-E2004-CON) — Not specified in the source documents (GAP-0657; ASM-1116) | S2 rwb-treatment | Records the difference terms on the treatment |
| GET | The case-account read at a business date of the rwb-source-data contract — Not specified in the source documents (GAP-0657; ASM-1116) | P1 rwb-source-data | The accounts of the case with the booked terms of the business date |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The ALS batch status, business date and `is_complete` behind the gate |
| POST | The reconciliation write of the rwb-source-data contract (REC-03) — Not specified in the source documents (GAP-0657; ASM-1116) | P1 rwb-source-data | Writes the REC-03 result into `reconciliation_result` |
| POST | The `raiseTask` operation of the rwb-case contract (RWB-P3-E2007-APP) — Not specified in the source documents (GAP-0657; ASM-1116) | P3 rwb-case | Opens at most one task per case, task code and treatment, with the owner role and the message ID |
| GET | `/api/recovery/case/v1/reference-data/{lovCode}` | P3 rwb-case | The treatment-type and task-code LOV rows with the version in force (DP-07) |
| GET | `/api/recovery/case/v1/parameters/{key}` | P3 rwb-case | `booking.missing.grace_loads` with the version in force (DP-06) |
| GET | `/api/recovery/decision/v1/rule-models/{n}/{v}` | P7 rwb-decision, published through RWB-P3-E2042-CON | The BOOKING_MATCH model and checksum for the version in force (DP-04) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Platform administration U for the rerun, cached per session |

The treatment list, the mark-booked write, the difference write, the account read and the reconciliation write are the legacy published Java interfaces `TreatmentQuery.approvedNotBooked`, `TreatmentCommands.markBooked`, `TreatmentCommands.recordBookingDifference`, `AccountQuery.forCase` and the reconciliation writer; no source fixes an HTTP path or a JSON shape for any of them, and they are taken from the published contracts of RWB-P3-E2004-CON and RWB-P1-E2007-APP when those land (GAP-0657; ASM-1116). The reference-data and parameter paths follow the shape of RWB-P3-E1043-CON and RWB-P3-E1042-CON and are fixed there, not here. No ACE view is read here and `rwb_integration` holds no grant on `recovery` (GAP-0657; ASM-1115).

#### 12.3 Events published

None by this story's own work. The service's own events on `rwb.integration.events.v1` are `FileDelivered` and `FileFailed`, which belong to the outbound-file stories of this service (RWB-P2-E1007-APP); nothing in this key publishes on that topic.

The local decision-record library publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` from the same transaction as the record it writes, with the fired rule ID, the package version, the outcome, the case ID, the treatment ID and the business date (DP-03). `rwb.payment.TreatmentBooked.v1` (EV-11) is rwb-payment's event and leaves rwb-payment when the treatment is marked booked; this story neither publishes it nor consumes it, and asserts exactly one of them through the treatment contract answer (AC6).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Use in this story |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | P1 rwb-source-data | Starts `BookingMatchWorkflow` for the business date; a duplicate is dropped through `processed_event` |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | `TreatmentApprovedListener` records the approval date used by the match against the booked date; a duplicate is dropped through `processed_event` |

Both subscriptions are deduplicated in the inbox of `rwb_integration`, keyed by the event ID and the consumer group, and neither is a business event of this service. Architecture v5 slides 42 and 43 list rwb-case, rwb-payment, rwb-deviation and rwb-writeoff as the consumers of `AceDataReady` and rwb-comms and rwb-payment as the consumers of `TreatmentApproved`; this story subscribes as an additional consumer for the JOB-08 run this realignment places in rwb-integration, and the added row is carried in the contract (GAP-0657; ASM-1119).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `BookingMatchWorkflow` | Workflow, workflow ID prefix `booking-match-` | `rwb-integration` | Input: source system ALS, business date D. Output: the counts of treatments read, booked, missing, differing, skipped and failed, and the run outcome |
| `readBookedTerms` | Activity | `rwb-integration` | Input: case ID, business date. Output: the batch-completeness answer and the accounts of the case with the booked terms; raises `AceBatchNotComplete` for the gate |
| `listApprovedTreatments` | Activity | `rwb-integration` | Input: the treatment types, the grace count, the business date. Output: the approved treatments not yet booked, with the approved terms and the approval date |
| `evaluateBookingMatch` | Activity | `rwb-integration` | Input: the treatment, the accounts, the business date. Output: the `RuleResult` per account — fired row, package version, outcome and difference terms; raises `NoPackageInForce`, which is non-retryable |
| `applyBookingOutcome` | Activity | `rwb-integration` | Input: the treatment and its `RuleResult`. Output: the decision-record reference and the outcome actually applied; writes the record first, then calls the treatment contract, and makes no call when the record cannot be written |
| `raiseBookingTasks` | Activity | `rwb-integration` | Input: the treatment, the outcome and the accounts without a booking. Output: the task reference or the existing open task; one rwb-case call per treatment |
| `writeRunSummary` | Activity | `rwb-integration` | Input: the run counts and the business date. Output: the REC-03 result reference from the rwb-source-data contract |

The activities carry the retry policy of the workflow kit; `NoPackageInForce` and `AceBatchNotComplete` are non-retryable and end the run. The workflow holds no timer, no signal and no child workflow of its own.

#### 12.6 Schedules

None. JOB-08 Booking confirmation is an event-started workflow started by `AceDataReady`, not a Schedule: no Schedule ID, no cadence and no catch-up window is created by this story (DP-10; Arch v5 slides 42 and 44). Architecture v5 slide 44 names rwb-payment as the owner of JOB-08; this realignment keeps the job with rwb-integration as RWB-P4-E2007-APP and RWB-ITG-E2007-ITG state, and the conflict is carried (GAP-0657; ASM-1114). The `job_catalog` row of JOB-08 is written by RWB-P2-E2007-OPS, not by this story.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| interface_config | `rwb_integration` | P2 (Ownership Map; TSD P2 v3 T3.1) | Read only, for the outbound interface register; this key adds no row |
| outbound_item | `rwb_integration` | P2 (Ownership Map; TSD P2 v3 T3.1) | Not used by this key; named so that the table set of the service is closed |
| job_catalog | `rwb_integration` | P2 (Ownership Map; TSD P2 v3 T3.1) | The JOB-08 entry, written by RWB-P2-E2007-OPS and read by the catalogue operation of the base |
| decision_record | `rwb_integration` | PLT library, created in `rwb_integration` (DP-03) | The local record of each outcome, written first in the transaction |
| outbox_event, outbox_delivery, processed_event, idempotency_key | `rwb_integration` | PLT library, created in `rwb_integration` (DP-09) | The record's outbox row, the inbox of the two consumed events and the run's idempotency record |

This story adds no business table of its own, exactly as the legacy solution plan states: no account data is copied, because the booked terms are read from the owner's contract on each run, and no treatment row is mirrored. `rwb-integration` reads no table of another service and holds no foreign key across services (DP-01); `rwb_integration` holds no grant on the `recovery` schema and no view (DP-05, BR12).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-treatment WireMock | The S2 contract of RWB-P3-E2004-CON | The approved-not-booked list with `TRT-SYN-0701` to `TRT-SYN-0704`; the treatments APPROVED and BOOKED with booked at 2026-12-16; the mark-booked write accepted once per treatment and date, answering 200 unchanged on a repeat; the difference write; one refusal when the record is forced to fail |
| rwb-source-data WireMock | The P1 contract | The ALS batch 2026-12-16 COMPLETE and 2026-12-17 FAILED with MSG-P1-001 on the freshness answer; accounts `A-0701` to `A-0705` with the booked terms, `tdr_flag`, last TDR date, principal and rate; the reconciliation write accepted |
| rwb-case WireMock | The P3 task and reference contracts | `raiseTask` accepting `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` and `UNMATCHED_EXCEPTION` and returning the open task on a repeat; the treatment-type and task-code LOV rows; the grace parameter = 1 |
| rwb-decision WireMock and the kit stub | The registry of RWB-P3-E2042-CON and the embedded kit | Package `BOOKING_MATCH` version `BKG-2026.12` with its RESTRUCTURE and SETTLEMENT rows and checksum; `NoPackageInForce` for 2026-12-17 |
| rwb-access WireMock | The P4 authorise contract | Platform administration U granted to RW-PLATADM, refused to RW-CASEOWN with MSG-P4-002, cached per session |
| Decision-record library stub | RWB-PLT-E1027-CON | A committed record with its outbox row, and the unavailable store of AC8 that must leave the treatment fake uncalled |
| Inbox and idempotency stub | RWB-PLT-TE006-CON | A duplicate `AceDataReady` dropped, and the treatment-and-date idempotency record of AC6 |

Each fake is generated from the owning service's published OpenAPI or AsyncAPI document where one exists, and the drift test fails when a fake answers a shape or an error that RWB-P2-E2007-CON does not declare.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 12 consumed | The rerun provided; the treatment list, the treatment read, the mark-booked write, the difference write, the account read, the freshness answer, the reconciliation write, the task raise, the reference-data read, the parameters read, the rule-model read and the authorise call consumed; one hop, 2 s timeout |
| Kafka | None published by own work, 1 published by the library, 2 consumed | `DecisionRecorded` on `rwb.decision-record.v1` by the library (DP-03); `AceDataReady` and `TreatmentApproved` consumed on their owners' topics (DP-09) |
| Temporal | 1 workflow, 6 activities, no Schedule | `BookingMatchWorkflow` with `readBookedTerms`, `listApprovedTreatments`, `evaluateBookingMatch`, `applyBookingOutcome`, `raiseBookingTasks` and `writeRunSummary` on `rwb-integration`; JOB-08 is event-started |
| File | None | This story reads and writes no file; the Workbench loads no ALS file and no lake file exists (DP-17; GAP-0657; ASM-1120) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `booking`, Java package `th.co.scb.ace.workbench.recovery.integration.booking`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract; this service reads no view | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is applied in its event-started form: JOB-08 is a workflow started by `AceDataReady` and no Schedule is created (GAP-0657; ASM-1114). DP-05 is applied as a prohibition: no ACE view is read here and no grant on `recovery` is held. The build dependency `RWB-P2-E1007-APP` is the same lane's base and is the reason this story is ready only after it.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| BookingMatchWorkflow | Workflow | JOB-08: the run for one business date, the flag and batch gates, the per-treatment loop, the no-package outcome and the run summary |
| BookingMatchService | Service | Turns the `RuleResult` into the outcome booked, missing, partly booked or differing, and orders the record before the remote call |
| BookingMatchFacts | Fact builder | Builds the facts of one treatment and account: treatment type, approved terms, account fields and the business date |
| BookingMatchEvaluator | Service | Calls the embedded kit with the package code, the facts and the date, and surfaces the fired row, the version and `NoPackageInForce` |
| BookingMatchIdempotency | Service | Holds the treatment-and-date idempotency record and skips a repeat without a second call |
| TreatmentApprovedListener | Listener | Consumes `TreatmentApproved` through the inbox and records the approval date used against the booked date |
| BookingRunSummaryWriter | Service | Writes the run summary, the counts and the REC-03 result through the rwb-source-data contract |
| TreatmentClient | Client | The approved-not-booked read, the treatment read, the mark-booked write and the difference write of RWB-P3-E2004-CON |
| SourceDataClient | Client | The case-account and booked-terms read, the freshness answer and the reconciliation write |
| CaseTaskClient | Client | The `raiseTask` operation of the rwb-case contract, one open task per case, task code and treatment |
| DecisionRecordWriter | Library client | Writes the local record with the fired row, the version, the outcome and the booking reference, first in the transaction (DP-03) |
| JobRerunController | Controller | `POST /admin/jobs/{jobId}/rerun` with the validation, the authorise check and the problem mapping |
| AccessCheckClient | Client | The authorise contract for the rerun right, cached per session |

**Database and migrations**

- One migration in the `rwb_integration` sequence: `V2007_1__booking_match.sql` adds the partial index on `decision_record (case_id, decision_code, created_at)` and the index on `idempotency_key (key, created_at)` that the one-record and repeat-run reads use, and includes the library tables `decision_record`, `idempotency_key`, `outbox_event`, `outbox_delivery` and `processed_event` in `rwb_integration` (DP-09, DP-15).
- No business table and no new column on anything but the library tables: the legacy solution plan's "no P2 table" stands, and the treatment columns `interest_rate` and `booking_difference` are on the treatment and are rwb-treatment's (S2 story).
- The run reads no table of another schema and holds no grant on `recovery`; the flight recorder of a run is its Temporal history and the run summary (DP-01, DP-05).

**Configuration and reference data**

- Package BOOKING_MATCH stays a registry of rwb-decision; the version in force per environment is recorded in `config/rule-packages.lock` at build time and read at run time through RWB-P3-E2042-CON. The values in this story are as at 16 November 2026 and are the legacy ones (GAP-0657; ASM-1118).
- `booking.missing.grace_loads` = 1 is read through the rwb-case parameters contract; the tolerance 0.00 baht (DL25) is a column of the row in force, never a value of this service.
- The treatment types RESTRUCTURE and SETTLEMENT and the task codes `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` and `UNMATCHED_EXCEPTION` are read through the rwb-case reference-data contract, with the version in force; no type or code is written in Java (DP-07).
- The legacy feature switch `rwb.integration.booking-confirmation` is kept as the legacy reference; the switch itself is a feature flag of the platform flag library and is read at the start of every run.
- The login is the rwb-integration login (DP-02): Not specified in the source documents (GAP-0657; ASM-1113).

**Build steps**

1. `BookingMatchFacts` and `BookingMatchEvaluator` against the kit stub, with a test per package row, one for `NoPackageInForce` and one for a checksum mismatch; the service holds no comparison code and no rule table (AC9, BR10).
2. `TreatmentClient` and `SourceDataClient` over their contracts, with the approved-not-booked read, the case-account read and the freshness gate; tests for the gate and the account facts (AC2, AC3, AC4).
3. `BookingMatchService` for one account and then for several accounts per case, with the partly booked outcome and the named accounts (AC4).
4. `DecisionRecordWriter` before any remote call, with the rollback path, the incident and the run marked failed for that treatment; AC8.
5. The mark-booked and difference writes and the treatment state read; AC2, AC3.
6. `CaseTaskClient` and the two task paths, with one open task per case, task code and treatment; AC2, AC3, AC4.
7. `BookingMatchIdempotency`, `BookingMatchWorkflow`, the flag gate, the batch gate and the no-package path; AC6, AC9.
8. `BookingRunSummaryWriter` and the REC-03 write, so the data steward's list carries the missing days.
9. `JobRerunController` and `AccessCheckClient`, with the 403, 404, 409 and 503 answers and the stored response under `Idempotency-Key`; AC6.
10. `TreatmentApprovedListener` with the inbox and the duplicate test (GAP-0657; ASM-1119).
11. The contract-fake run of every cross-service answer in isolation, so the story builds before rwb-treatment, rwb-source-data and rwb-case are live (GAP-0657; ASM-1116).

**Done when.** The tests in section 16 pass, REC-03 for a SIT week shows every synthetic approved treatment booked or raised with the fired row and the package version on its record, no comparison code and no rule table exist in the service, `rwb_integration` holds no grant on `recovery`, and the contract tests of RWB-P2-E2007-CON, RWB-PLT-E1027-CON and RWB-PLT-E1072-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-011 | Task text, booking missing | No booking for treatment {treatment} was found in the ALS batch for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | Task text and treatment note, term differs | The booked {term} is {booked}. The approved {term} is {approved}. |
| MSG-P1-001 | ACE batch late or not complete | {product} is from {date}. Today's data is not yet complete. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No BOOKING_MATCH version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P2-006 | Rerun while JOB-08 runs | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-001 | No session on the rerun | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the right reruns JOB-08 | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A consumed contract did not answer | {source} could not be read. Try again in a few minutes. |

The texts are the legacy ones, unchanged, except MSG-P1-001, which takes the FSD P2 Integration v3 wording (`{product} is from {date}. Today's data is not yet complete.`) in place of the legacy `Today's load has not arrived.` (GAP-0657; ASM-1117). For MSG-P3-027 in this story `{check}` is "no package in force" and `{detail}` names the package code BOOKING_MATCH and the business date only, never a case or an account fact. For MSG-P4-002 `{action}` names the action the caller tried — for example "rerun the booking-confirmation job" — and never a case fact. MSG-GEN-006 names the source and the activity, never the payload.

### 15. Screens and states

SCR-14 Treatment record, states approved and booked: the officer sees `booked_at` or the booking difference with each term approved and booked. The officer and the Credit Administration officer see their tasks on SCR-01 My work. Both screens are served by the gateway-bff composite route (DP-19) from rwb-case, rwb-treatment and rwb-access, one hop each; this story supplies the values behind the treatment state and the tasks and renders no page. SCR-29 Posting, which shows the confirmation for all bookings, comes in Epic 4. The operator view of the run is the `job_catalog` row and the run summary, deployed and alerted by RWB-P2-E2007-OPS; the screen fields, the field-level masking and the route specification of SCR-14 and SCR-01 are Not specified in the source documents (GAP-0657; ASM-1116).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-10 | Access | Component | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun for JOB-08; refused with MSG-P4-002 |
| TC-E2-007-01 | AC1, BR1, BR3, BR7, BR10 | End to end | Synthetic settlement booked 2026-12-16 at 650,000.00 baht |
| TC-E2-007-02 | AC2, BR5 | End to end | Restructure with tdr_flag false in v_ace_account |
| TC-E2-007-03 | AC3, BR2, BR4, BR6 | End to end | Rate 4.5000 booked against 4.2500 approved |
| TC-E2-007-04 | AC4, BR2 | End to end | Two accounts, one booked |
| TC-E2-007-05 | AC5, BR8 | End to end | ACE batch failed for 2026-12-17 |
| TC-E2-007-06 | AC6 | End to end | JOB-08 rerun for 2026-12-16 |
| TC-E2-007-07 | AC7, BR5 | End to end | Booking missing on two batches |
| TC-E2-007-08 | AC8, BR9 | End to end | Decision log store stopped |
| TC-E2-007-09 | AC9, BR11 | End to end | No BOOKING_MATCH version in force on 2026-12-17 |
| TC-E2-007-11 | Principle 5 | NFR | Decision log write forced to fail on markBooked; treatment stays APPROVED, no event |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR.

This story runs TC-E2-007-02, TC-E2-007-03, TC-E2-007-04, TC-E2-007-06, TC-E2-007-08, TC-E2-007-09, TC-E2-007-10 and TC-E2-007-11 against its own workflow with the contract fakes: the match, the task raise, the idempotency record and the no-package path at Component level inside the End-to-end case, and the access refusal at its own endpoint. TC-E2-007-01, TC-E2-007-05 and TC-E2-007-07 are cited for the legacy key and are proved end to end in RWB-ITG-E2007-ITG, with the case and treatment halves in RWB-P3-E2007-APP and the S2 story. The `-ITG` copies of these cases are not here; they belong to RWB-ITG-E2007-ITG.

### 17. Guardrails

- No business value in code: the compared terms, the tolerance, the grace count, the treatment types and the task codes are rows of package BOOKING_MATCH, parameters and reference data of their owners. The service holds no threshold, no rate and no amount.
- No personal data in logs, tests, workflow inputs, history or prompts. The booking reference holds the `account_key`, not the account number, and every fixture is synthetic (`TRT-SYN-0701` to `TRT-SYN-0704`, `A-0701` to `A-0705`, `RW-2026-000701`).
- No read of another service's table and no direct ACE read: the accounts, the booked terms and the batch answer come only through the rwb-source-data contract, the treatment only through the rwb-treatment contract, the task only through the rwb-case contract, the package only through the rwb-decision rule-model read (DP-01, DP-04, DP-05; GAP-0657; ASM-1115).
- `rwb_integration` holds no foreign key into another schema and no grant on `recovery`; the service links to the treatment, the case and the account by business key only.
- No comparison code and no rule table: package BOOKING_MATCH decides, through the embedded kit, and the result names the row and the version. The package is loaded, tested and approved through RWB-E2-042; this story never reads `drl_source` or a workbook.
- No call to ALS: the match reads only what ACE holds for the completed batch, through the owner of the ACE read.
- The decision record is written first, in the same local transaction as its outbox row; a failed write makes no remote call and raises an incident (R-UNI-39, BR9).
- One run per business date and one record per treatment and business date; a repeat is skipped by the idempotency record and raises no second task (BR14, BR15).
- No data lake artefact is built, sent or read by this key (DP-17).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next day's ALS load | Epic 2, 3.2; Program, 5.3 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39, R-UNI-41 | TC-E2-007-01 to TC-E2-007-11 |

The supporting measures of this story are REC-03 (approved treatments against bookings, zero after two days) and the freshness rule of the ACE batch answer; the requirement ID is the legacy one and this story adds none of its own. The rule IDs R-RES-22 and R-SET-13 are the case-move rules that follow a confirmation and are evaluated in rwb-case; the match itself is decided by the rows of package BOOKING_MATCH, and the row IDs are the registry's (GAP-0657; ASM-1118).

### 19. Out of scope

- The case route state, the task rows, the case timeline and the case-side decision record: rwb-case (RWB-P3-E2007-APP), with the contract baseline RWB-P2-E2007-CON.
- The treatment record, its APPROVED to BOOKED state, `booked_at`, the booking difference and the treatment-side record: rwb-treatment (the S2 story of this legacy key).
- The ACE account and batch-status reads, the freshness product and the reconciliation answer behind REC-03: rwb-source-data (RWB-P1-E2007-APP and RWB-P1-E1069-APP).
- The BOOKING_MATCH rows, the package versions, the authoring, the approval and the rollback: rwb-decision (RWB-P7-E2007-APP, RWB-E2-042 and RWB-E1-073).
- The authorise decisions behind the booked-terms read and the booking tasks: rwb-access (RWB-P4-E2007-APP).
- The deployment, the JOB-08 registration, the chart, the alerts, the dashboards and the runbook: RWB-P2-E2007-OPS.
- The end-to-end proof of these values across the services: RWB-ITG-E2007-ITG.
- Posting a settlement booking to ALS from the Workbench and the SCR-29 Posting screen: FEAT-PAY-06, Epic 4.
- Payment matching to the plan or the settlement: JOB-07 and FEAT-OCC-10, Epic 2.
- The data lake, the Power BI extract and the COLLINS decision feed: removed by D-RCV-18 and DP-17; nothing in this key builds or sends a lake file (GAP-0657; ASM-1120).
