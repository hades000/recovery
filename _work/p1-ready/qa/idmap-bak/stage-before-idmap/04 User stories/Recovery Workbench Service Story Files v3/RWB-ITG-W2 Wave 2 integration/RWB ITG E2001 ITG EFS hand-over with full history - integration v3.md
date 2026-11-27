# RWB-ITG-E2001-ITG EFS hand-over with full history

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- The REC-05 break is read from `/admin/reconciliation/results`; `/admin/data-quality/exceptions` is withdrawn. Finding RWB-ITG-E2001-ITG#1.
- The refused rerun is rwb-case's, not the rwb-source-data job rerun (RD-P1-012); its path stays pending (GAP-2258). Finding #2.
- EFS append keys, answers and repeat counting follow RD-P1-007; freshness reads `LOADED` or `STALE` on the stamp in use (RD-P1-005, RD-P1-041). Findings #3, #4, #8.
- `AceDataReady`, `AceDataLate` and the batch literal `COMPLETED` follow RD-P1-003 and RD-P1-040. Findings #5, #6.
- Run summary read, seed source and contract version corrected (RD-P1-005, RD-P1-011). Findings #7, #9, #10.
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.
- Case creation waits for ALS only; a late DP05 delays only the EFS history, bounded by `handover.hold_until` (interim 09:00, NEW-GAP-D4), and NEW-GAP-L03-2 and the stale-DP05 question are settled (RD-P1-067).

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2001-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Small, fits two weeks; the squad confirms the size at refinement |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP18, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P1-E1069-APP, RWB-P1-E1015-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P3-E2001-APP, RWB-P7-E2001-APP, RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON (not done yet; Day 1 runs against the contract fakes of section 12.8) |
| Contract dependencies | RWB-PLT-E1043-CON, RWB-P3-E1043-CON |
| Contract version | v1 (the /v1 path prefix of every operation in 12.2 and 12.8); the version of each OpenAPI document is Not specified in the source documents (DOR-RWB-ITG-E2001-ITG-23), except rwb-source-data: rwb-source-data.yaml 5.1.0 and rwb-source-data.asyncapi.yaml 5.1.0 with the provider fake of the same version |
| Integration dependencies | RWB-P1-E1069-APP, RWB-P1-E1015-APP, RWB-P2-E2001-APP, RWB-P1-E2001-APP, RWB-P3-E2001-APP, RWB-P7-E2001-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DRI-013, REQ-CHO-001, REQ-CHO-005, REQ-RDF-003) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-005, RD-P1-007, RD-P1-010, RD-P1-011, RD-P1-012, RD-P1-040, RD-P1-041, RD-P1-067 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-001 for the wave 2 integration harness. The legacy story created the case, linked the further account, appended the EFS history and held a stale batch inside one recovery service; this story builds no production endpoint, table, workflow or schedule and owns no table, and proves across gateway-bff, rwb-source-data, rwb-integration, rwb-case, rwb-access and rwb-decision that one AceDataReady starts the hand-over once, that one case, its 16 EFS entries, one local decision record and one central ledger entry are written once, that a stale DP05 holds the step with no case, and that the next good batch creates the two missed business dates with the gap date named — on Day 1 against the contract fakes and against the real services as their stories land. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 32 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **member of the integration and test team (QA)**, I want **a repeatable wave 2 harness that drives the EFS hand-over of one business date through gateway-bff, rwb-source-data, rwb-integration, rwb-case, rwb-access and rwb-decision and records one evidence report per run**, so that **the case is proved to be created once from the ACE data, to carry its 16 EFS history entries and its one decision record, to hold while the ACE batch is stale and to be created on the next good batch — across services, on Day 1 and on every release after**.

This story is the wave 2 integration harness for the legacy key. It builds no production endpoint, table, workflow or schedule and it owns no table. The behaviour it exercises is owned by the app stories of the legacy key: RWB-P1-E1069-APP (the read-only ACE view contract of the 30 `recovery.v_ace_*` views), RWB-P1-E1015-APP (the freshness stamp per data product and `AceDataReady`), RWB-P2-E2001-APP (HandoverService, the group builder and the run summary), RWB-P1-E2001-APP (the EFS history read and the interaction ledger append in `rwb_source_data`), RWB-P3-E2001-APP (case creation, the account link and `CaseCreated`) and RWB-P7-E2001-APP (the local decision record and the central ledger). The harness builds the runner, the fakes, the seeds and the evidence, and it owns the criteria of section 7 that are tagged to it.

### 2. Business rationale

Accounts move from collections to recovery by a weekly transfer today, and the case starts without its collection history. ACE ingests the ALS hand-over and the EFS action history, and the Workbench creates the case the morning after the account reaches 90 days past due, links a further account of the same customer and product group to the open case, and appends the EFS contact and promise history of the collection period so that the case owner can see what happened before day 90. The legacy story did all of this inside one deployable. In the target architecture the same journey is served by six services: rwb-source-data owns the ACE view contract, the freshness stamps and the interaction ledger (DP-18); rwb-integration owns the hand-over step; rwb-case owns the case and the account link; rwb-decision owns the central ledger. A defect at any seam — a ledger append put on the wrong service, a stale stamp that does not hold the step, an entry appended twice for one `efs_record_key`, a case created for an account with no customer row, a gap date lost between two good batches — would only appear with a live case and a live batch, unless the journey is exercised across the services as one flow.

This story is that exercise. It runs the hand-over from the ready batch through the fakes and then through the real services as their app stories land, reproduces the hold, the break and the repeat of the legacy story in the same run, and attaches one evidence report per run keyed by story and business date, so the hand-over can be shown to hold before wave 2 is accepted and after every change. It meets REQ-DRI-013, REQ-CHO-001, REQ-CHO-005 and REQ-RDF-003 at the integration level, and it leaves every business rule, every screen behaviour and every table with the owning stories.

The realignment facts the run proves are DP-18, DP-10 and DP-19. `interaction`, `efs_ledger_outcome` and `reconciliation_result` belong to P1 rwb-source-data in `rwb_source_data`; the legacy story put the ledger append on P7, and the criteria below use P1. JOB-02's Quartz trigger becomes an event-started Temporal step, JOB-02 staying P3's per the Ownership Map while the hand-over step runs in rwb-integration on `AceDataReady`. Any screen read of the case list, the case timeline or the data-quality view is a gateway-bff composite route, and the ACE views are read only by rwb-source-data (DP-05).

### 3. Preconditions

- The six I stories are published and deployed in the SIT environment as they land: RWB-P1-E1069-APP (the read-only ACE view contract), RWB-P1-E1015-APP (the freshness stamp and `AceDataReady`), RWB-P2-E2001-APP (HandoverService, the group builder and the run summary), RWB-P1-E2001-APP (the EFS history read and the interaction append in `rwb_source_data`), RWB-P3-E2001-APP (case creation, the account link and `CaseCreated`) and RWB-P7-E2001-APP (the local decision record and the central ledger).
- gateway-bff is deployed with the composite case-list, case-timeline and data-quality routes of DP-19 available, so a screen read is one gateway answer and not the browser calling each service. The composite route paths and their merge order are Not specified in the source documents (GAP-0388; ASM-0563).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before any I story lands.
- The synthetic seeds of the legacy story exist: account "A-0001" of customer "C-0001", product group "MORTGAGE", in `v_ace_account` at business date 2026-12-14 with 90 days past due; 14 contact rows and 2 promise rows for "A-0001" in `v_ace_efs_action`; account "A-0002" of customer "C-0002", product group "SSME", with open case "RW-2026-000210"; account "A-0003" with no row in `v_ace_customer`; account "A-0004" of the decision-log failure case.
- The ACE batch rows of business dates 2026-12-14, 2026-12-15, 2026-12-16 and 2026-12-17 exist as fixtures: 2026-12-14 COMPLETED at 05:20, 2026-12-15 not COMPLETED by 09:00 on 2026-12-16 with DP05 `STALE`, 2026-12-16 COMPLETED at 05:15 on 2026-12-17.
- Parameter `case.entry.dpd_threshold` = 90, parameter `handover.hold_until` = 09:00 (interim value; the catalog row is pending, NEW-GAP-D4), the product code to product group map and the `efs_ledger_outcome` rows are loaded by their owners through their contracts; the harness holds no copy of any of them.
- An RW-CASEOWN login in scope, a login without Platform administration U, and an RW-DATASTEW login exist in SIT for the reads and the refusal, with their rights read on `GET /api/recovery/access/v1/me/session`.
- Feature `rwb.integration.efs-handover` is on in the harness environment; the harness reads the flag through the platform library and asserts the off state creates no case.
- No build dependency: the harness starts on Day 1 against the fakes, and each fake is replaced by the real service as its I story lands. Its repository, its SIT and UAT environments, its seeding, its per-run evidence format and retention and its pass/fail gate are Not specified in the source documents (GAP-0388; ASM-0563).

### 4. Flow

1. Harness: starts a run for the story and the business date, takes the run lock, and records the build under test, the pack version and the fake or real mode of each of the six services it touches.
2. Harness: takes the ACE view rows and ACE batch rows from the rwb-source-data sandbox seed in real mode (Pending: fixtures for these accounts and dates, owner rwb-source-data tech lead, tracked as NEW-GAP-F04-5), and seeds everything else through the contract of each owning service, or through the fake in fake mode — the accounts "A-0001" to "A-0004", the 14 contact and 2 promise rows of `v_ace_efs_action`, the open case "RW-2026-000210", the ACE batch rows of 2026-12-14 to 2026-12-17, the parameter rows and the `efs_ledger_outcome` rows.
3. Harness: publishes `AceDataReady` for ALS with business date 2026-12-14 and event ID "EVT-SYN-2614-01" into `rwb.source-data.events.v1` (record key `ALS:2026-12-14`, `ce_subject` ALS, payload `sourceSystem`, `businessDate`, `status` COMPLETED, `completedAt`), and records the answer of `GET /api/recovery/source-data/v1/data-products/freshness` for DP01 and DP05.
4. rwb-source-data: reports DP01 and DP05 with `status` `LOADED` and `businessDate` 2026-12-14; the event-started hand-over step starts in rwb-integration on queue `rwb-integration` (DP-10).
5. Harness: reads the case list on `GET /api/recovery/case/v1/cases` and the case on `GET /api/recovery/case/v1/cases/{caseId}`, and asserts one case with status "NEW", entry date 2026-12-15 and days past due at entry 90 for "A-0001".
6. Harness: reads the ledger on `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` and asserts 16 entries with source system "EFS" and the action code of each row, which rwb-source-data holds in its table `interaction`; the harness reads them only through this operation.
7. Harness: consumes `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` and `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, asserts one message of each for the case, and reads the one central ledger entry on `GET /api/recovery/decision/v1/decision-log`.
8. Harness: re-delivers the same `AceDataReady` event ID "EVT-SYN-2614-01" and reruns the step for 2026-12-14, then re-reads the case, the ledger, the case-created event and the central ledger and asserts one case, 16 entries, one event and one ledger entry, with the repeat counted as an idempotency hit in the run summary.
9. Harness: through the fake, holds the ALS batch of 2026-12-15 not COMPLETED and answers DP01 and DP05 `STALE` with `businessDate` 2026-12-14, drives the step for 2026-12-15, and asserts no case, MSG-P1-001 with the stale business date, MSG-P2-007 with a waiting count, and the run summary naming no entry date for 2026-12-15.
10. Harness: delivers `AceDataReady` for business date 2026-12-16 completed at 05:15 on 2026-12-17, drives the step, and asserts cases with entry date 2026-12-17 for the accounts that reached 90 days past due on 2026-12-15 or 2026-12-16 and the gap date 2026-12-15 in the run summary.
11. Harness: drives the account "A-0002" of the open case "RW-2026-000210" and asserts no new case and the account link on `GET /api/recovery/case/v1/cases/{caseId}/accounts`; drives "A-0003" with no customer row and asserts no case and the REC-05 business-key break listing "A-0003".
12. Harness: reads the session of a role without Platform administration U on `GET /api/recovery/access/v1/me/session`, requests the administrative rerun of the entry run on rwb-case (path not specified, GAP-2258), and asserts the refusal with MSG-P4-002 and no change.
13. Harness: runs the boundary check over the 19 per-service schemas and the trace of the run, publishes the evidence report keyed by story id and business date with one row per criterion, the seam each row exercised, the service or fake that answered and the pass or fail result, and releases the run lock.
14. Harness: on any failed criterion, fails the run and names the criterion, the seam and the observed value.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | The same `AceDataReady` event ID arrives twice, or the step is rerun for the same business date | One case, 16 entries and one ledger entry; the repeat is counted as an idempotency hit | None | AC11 |
| X2 | The ACE batch for ALS and business date D is not COMPLETED by 09:00 (`AceDataLate` goes out at 05:30; case creation waits for ALS, and `handover.hold_until` bounds only the wait for EFS history, RD-P1-067) | No case; the step holds; the data products show the stale date; the alert names the waiting count | MSG-P1-001, MSG-P2-007 | AC3, AC10 |
| X3 | The account's `person_key` has no row in `v_ace_customer` | No case for "A-0003"; the REC-05 business-key break lists it; it is tried with the next run | None | AC5 |
| X4 | The decision record cannot be written | No case for "A-0004"; an incident is raised; the account is tried in the next run | MSG-P7-003 | AC7 (driven; owned by RWB-P3-E2001-APP) |
| X5 | The customer already has an open case for the product group | No new case; "A-0002" is linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false | None | AC4 (driven; owned by RWB-P3-E2001-APP) |
| X6 | The step is started again while it runs | The rerun is refused and nothing changes; a rerun request for a business date is an admin operation on the rwb-case base that answers 409 while the workflow for that date runs | MSG-P2-006 | AC8 (driven; owned by RWB-P3-E2001-APP) |
| X7 | A role without the right requests the administrative rerun | Refused before any step starts; nothing changes | MSG-P4-002 | AC13, TC-E2-001-09-ITG, TC-ITG-E2001-06 |
| X8 | A cross-schema read, a FOREIGN KEY between two schemas, a second reader of `recovery.v_ace_*`, or a call deeper than one hop | The run fails and names the schema, the constraint or the hop | None (run report) | AC12 |

X4, X5 and X6 are driven inside the same run so that the seams stay covered, but their criteria stay with the app stories; the harness asserts the seam and does not claim the criterion.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the six I stories are deployed; until then it runs against the §12.8 fakes, with no work order inside another team's lane |
| Negotiable | The seeds, the fakes and the assertions are configuration and data; the criteria are the legacy ones and the four seams this harness adds |
| Valuable | The hand-over is proved to be one journey across six services, with the hold, the break, the link and the repeat the business asked for |
| Estimable | One runner, one fake pack, one seed set, one evidence publisher and one gate |
| Small | Fits one iteration with the owning stories' contract tests |
| Testable | Each of the fourteen `-ITG` test cases of section 16 is one run of the harness and one row of the evidence report |

### 7. Acceptance criteria

```gherkin
Feature: EFS hand-over with full history

  Background:
    Given parameter "case.entry.dpd_threshold" is 90
    Given the ACE batch for ALS with business date 2026-12-14 is COMPLETED at 05:20

  Scenario: AC1 Case from the ACE data (legacy RWB-E2-001 AC1)
    Given the rwb-source-data contract fake serves synthetic account "A-0001" for customer "C-0001", product group "MORTGAGE", reached 90 days past due at business date 2026-12-14
    Given the rwb-source-data contract fake serves 14 contact rows and 2 promise rows for "A-0001" in its collection period
    When the morning case creation runs on 2026-12-15
    Then a case exists with status "NEW", product group "MORTGAGE", entry date 2026-12-15 and days past due at entry 90
    Then the case holds 16 interaction entries with source system "EFS" and the action code of each row
    Then the decision record for the creation holds business date 2026-12-14 in its inputs snapshot
    Then the system publishes caseCreated with business date 2026-12-14

  Scenario: AC3 Late ACE batch (legacy RWB-E2-001 AC3)
    Given the ACE batch for ALS with business date 2026-12-15 is not COMPLETED by 09:00 on 2026-12-16
    When case creation is due
    Then the system creates no case from the data of 2026-12-14
    Then the data products show message MSG-P1-001 with the date 2026-12-14
    Then the system alerts the data steward with message MSG-P2-007

  Scenario: AC5 Customer not in the ACE customer data (legacy RWB-E2-001 AC5)
    Given the rwb-source-data contract fake serves synthetic account "A-0003" reaching 90 days past due with no customer row for its person_key
    When case creation runs
    Then the system creates no case for "A-0003"
    Then the REC-05 business-key break lists "A-0003" for the data steward
    Then "A-0003" is tried again with the next run

  Scenario: AC6 Cases created on the next good batch (legacy RWB-E2-001 AC6)
    Given no case creation ran for business date 2026-12-15
    Given the ACE batch for ALS with business date 2026-12-16 is COMPLETED at 05:15 on 2026-12-17
    When case creation runs
    Then accounts that reached 90 days past due on 2026-12-15 or 2026-12-16 get cases with entry date 2026-12-17
    Then the run summary names the gap date 2026-12-15

  Scenario: AC9 One ready batch drives the hand-over across the services once (new, D-RCV-60)
    Given AceDataReady for ALS with business date 2026-12-14 arrives with event ID "EVT-SYN-2614-01", record key "ALS:2026-12-14" and status "COMPLETED"
    Given rwb-source-data answers GET /api/recovery/source-data/v1/data-products/freshness with DP01 and DP05 at status LOADED and business date 2026-12-14
    When the event-started hand-over step runs in rwb-integration for that business date
    Then rwb-case holds one case with status "NEW", entry date 2026-12-15 and days past due at entry 90
    Then rwb-source-data holds 16 interaction entries for the case with source system "EFS" and the action code of each row, appended through POST /api/recovery/source-data/v1/cases/{caseId}/interactions
    Then each append carries a UUID Idempotency-Key and body idempotencyKey "EFS:<efsRecordKey>" and answers 201, with eventCode PROMISE for the 2 rows with isPtp true and CONTACT for the other 14
    Then the writing service holds one local decision record in the same transaction as the case
    Then rwb-decision holds one central ledger entry, read on GET /api/recovery/decision/v1/decision-log
    Then rwb.case.CaseCreated.v1 is published once on rwb.case.events.v1 with business date 2026-12-14

  Scenario: AC10 A late ALS batch with a stale DP05 holds the step and the next good batch creates the cases (new, D-RCV-60)
    Given the ACE batch for ALS with business date 2026-12-15 is not COMPLETED
    Given GET /api/recovery/source-data/v1/data-products/freshness answers DP01 and DP05 with status STALE and businessDate 2026-12-14
    When the hand-over step is due for business date 2026-12-15
    Then the step holds and creates no case
    Then the data products show message MSG-P1-001 with the date 2026-12-14
    Then exactly one rwb.source-data.AceDataLate.v1 with record key "ALS:2026-12-15" is on rwb.source-data.events.v1, published at 05:30
    Then the system alerts the data steward with message MSG-P2-007 and the run carries a waiting count
    Given the ACE batch for ALS with business date 2026-12-16 is COMPLETED at 05:15 on 2026-12-17
    When the hand-over step runs for business date 2026-12-16
    Then accounts that reached 90 days past due on 2026-12-15 or 2026-12-16 get cases with entry date 2026-12-17
    Then the run summary names the gap date 2026-12-15

  Scenario: AC11 The same event and the step rerun leave one case and one ledger entry (new, D-RCV-60)
    Given the run of AC9 is complete and its AceDataReady event ID is "EVT-SYN-2614-01"
    When the same AceDataReady event ID is delivered a second time and the hand-over step is rerun for business date 2026-12-14
    Then rwb-case still holds one case for "A-0001"
    Then rwb-source-data still holds 16 interaction entries for that case
    Then rwb.case.CaseCreated.v1 is still published once for that case
    Then rwb-decision still holds one central ledger entry for the creation
    Then every repeated append with a new Idempotency-Key and the same body idempotencyKey "EFS:<efsRecordKey>" answers 200 with the existing entry and caseSeq
    Then the hand-over run counts those 200 answers as repeats, rwb-integration counts the view rows folded into one entry, the run summary reports both counts, and rwb-source-data writes no processed_event row for them

  Scenario: AC12 The boundary holds across the 19 per-service schemas and every hop (new, D-RCV-60)
    Given the 19 per-service schemas with their own logins
    When the harness reads every foreign key, every grant and every view definition of the 19 schemas and the trace of the run
    Then no FOREIGN KEY points from one schema to another and no service login holds a write grant on another service's schema
    Then only rwb-source-data selects recovery.v_ace_* and no other schema holds a view or a query text over those views
    Then every call goes one hop to the owner's /api/recovery/<short>/v1 base and answers within 2 s
    Then the local decision record is written in the same transaction as the case and published once on rwb.decision-record.v1

  Scenario: AC13 A role without Platform administration U is refused the administrative rerun (new, D-RCV-60)
    Given the caller holds a role without Platform administration U
    When the caller requests the rwb-case rerun of a business date (path pending, GAP-2258)
    Then the request is refused before any step starts with message MSG-P4-002
    Then nothing changes

  Scenario: AC14 The owning-schema, decision-record and event-start rules hold (new, D-RCV-60)
    Given the 19 per-service schemas, the published contracts and the trace of the run
    When the harness checks BR9, BR10 and BR11 against the owning services
    Then each of the 19 services writes only its own rwb_* schema and holds another service's IDs, never its rows
    Then the decision record is written in the same transaction as the state change and a redelivery is deduped by the inbox
    Then the hand-over is started by AceDataReady as an event-started Temporal step and no Quartz job or shared Quartz table is read or written

  Scenario: AC15 A retried or timed-out activity leaves one case (new, D-RCV-60)
    Given the event-started hand-over step is running for business date 2026-12-14
    When an activity of the step is retried or exceeds its timeout
    Then the run trace names the activity and the retry or timeout
    Then rwb-case still holds one case for "A-0001" and rwb-source-data holds 16 interaction entries for that case

  Scenario: AC16 A consumed call that fails or does not answer creates no partial case (new, D-RCV-60)
    Given the rwb-source-data contract fake fails or does not answer within 2 s the freshness call for business date 2026-12-14
    When the event-started hand-over step runs for business date 2026-12-14
    Then the step holds and creates no case
    Then no interaction entry is appended for the case
    Then the run trace names the failed call and its owning base /api/recovery/source-data/v1

  Scenario: AC17 A status change the case model does not allow is refused (new, D-RCV-60)
    Given a case exists with status "NEW" for "A-0001"
    When a status change that the case model does not allow is requested for that case
    Then the change is refused and the case keeps status "NEW"
```

AC1, AC3, AC5 and AC6 are the legacy criteria owned by this story and are copied word for word from RWB-E2-001 with the origin tag on the scenario line; the two legacy Background lines and the feature line are unchanged. Version 3 changes one status value in AC3 (COMPLETED). AC2, AC4, AC7 and AC8 stay with the app stories of this key and are not restated. AC9 to AC12 are the four seams this harness adds under D-RCV-60, and each one uses only legacy values.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case enters at 90 days past due | DL16; parameter case.entry.dpd_threshold |
| BR2 | One case per customer per product group; a further account of the same customer and product group is linked to the open case | DL17 (assumption: Not specified in the source documents (DOR-RWB-ITG-E2001-ITG-18)); REQ-CHO-005 |
| BR3 | The hand-over set is read from v_ace_account for the ACE business date; the Workbench loads no source file | D-RCV-35 U1; ADR-010; REQ-DRI-013 |
| BR4 | No case is created from a business date whose ACE batch is not COMPLETED | JOB-02; CTL-02; FEAT-CHO-05 |
| BR5 | The EFS contact and promise history of the collection period is read from v_ace_efs_action and appended to the interaction ledger with source system EFS, one entry per efs_record_key | DL29 (assumption: Not specified in the source documents (DOR-RWB-ITG-E2001-ITG-18)); LOV-SOURCE; REQ-CHO-001; R-UNI-40 |
| BR6 | A repeat hand-over for the same account and business date is ignored and counted | R-UNI-40 |
| BR7 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | An account whose person_key has no row in v_ace_customer is held on the REC-05 business-key break and tried with the next run | REC-05; DQ-040; D-RCV-35 U2 |
| BR9 | One owning schema per table and no cross-schema read: each of the 19 services writes its own `rwb_*` schema and holds another service's IDs, never its rows | DP-01, DP-11; ADR-014, ADR-020; Arch v5 slides 29, 45 and 46 |
| BR10 | The decision record is written locally in the same transaction as the state change and published once on `rwb.decision-record.v1`; a redelivery is deduped by the inbox | DP-03, DP-09; ADR-015, ADR-022; Temporal and Drools design slides 11 and 16 |
| BR11 | The hand-over is an event-started Temporal step started by `AceDataReady` with `sourceSystem` ALS and `status` COMPLETED, not a Quartz job; no shared Quartz table is read or written | DP-10; ADR-016; Arch v5 slide 44 |

BR1 to BR8 are copied word for word from the legacy story with their sources. BR9 to BR11 are the realignment rules this harness proves. The harness asserts all eleven against the owning services and the published contracts; it does not re-implement them, and no BR row is changed by this story.

### 9. State transitions

None. This story changes no case status and no case state; the harness drives the hand-over and reads records only, and it adds no transition of its own. The facts below are caused by the owning services and are observed and asserted by the harness.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| `AceDataReady` published for ALS at business date 2026-12-14 | rwb-source-data (P1) | One event on `rwb.source-data.events.v1` with the business date (TC-E2-001-01-ITG, TC-ITG-E2001-01) |
| DP01 and DP05 stamps read, the step started or held | rwb-source-data (P1) and the step in rwb-integration (P2) | A fresh answer and one run, or a stale answer and no case (TC-ITG-E2001-01, TC-ITG-E2001-02) |
| One case with status "NEW", entry date 2026-12-15 and 90 days past due at entry | rwb-case (P3) | One case on the case list and the case read (TC-E2-001-01-ITG, TC-ITG-E2001-01) |
| 16 EFS entries with source system "EFS" and their action codes | rwb-source-data (P1) | 16 entries in `interaction` read through the P1 contract (TC-E2-001-01-ITG, TC-ITG-E2001-01, TC-ITG-E2001-03) |
| One local decision record and one central ledger entry | the writing service, sealed by rwb-decision (P7) | DecisionRecorded once and one entry on `GET /api/recovery/decision/v1/decision-log` (TC-E2-001-10-ITG, TC-ITG-E2001-01, TC-ITG-E2001-03) |
| `CaseCreated` published once with business date 2026-12-14 | rwb-case (P3) | One message on `rwb.case.events.v1` (TC-ITG-E2001-01, TC-ITG-E2001-03) |
| A held run with a stale stamp and a waiting count | rwb-source-data (P1) and the step | MSG-P1-001, MSG-P2-007, no case (TC-E2-001-03-ITG, TC-ITG-E2001-02) |
| Cases with entry date 2026-12-17 and the gap date 2026-12-15 | rwb-case (P3) and the run summary of rwb-source-data (P1) | The two entry dates and the gap date in the run summary (TC-E2-001-06-ITG, TC-ITG-E2001-02) |
| The REC-05 business-key break listing "A-0003" | rwb-source-data (P1) | The break row and the account tried again (TC-E2-001-05-ITG) |
| No new case, the account linked to "RW-2026-000210" | rwb-case (P3) | The account link with linked from 2026-12-15 and is primary false (TC-E2-001-04-ITG) |
| A rerun refused for a role without the right | the rerun operation of rwb-case (path not specified, GAP-2258) with the role data of rwb-access (P4) | MSG-P4-002 and no change (TC-E2-001-09-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery service identity, the hand-over step | Reads the ACE view contract of rwb-source-data and drives case creation and the ledger append (Case record, CU); driven and asserted by the harness |
| SY-CASEWF, case workflow module | Creates the case and the account link, writes the decision record and publishes `CaseCreated` (Case record, CU); driven and asserted by the harness |
| SY-DECLOG, decision log writer | Writes the local decision record; rwb-decision seals the central ledger (Decision log, C); asserted by the harness |
| RW-CASEOWN, case owner | Reads the case, its EFS history and its timeline once allocated (Case record, R); the synthetic user the harness drives |
| RW-DATASTEW, data steward | Receives the late batch alert and reads the run summary and the REC-05 break (Platform administration, R) |
| RW-PLATADM, platform administrator | Requests the administrative rerun (Platform administration, U) |
| QA lead | Owns the harness pack, the seeds, the evidence format and the gate |
| Integration lead | Owns the fake pack, the run of record and the replacement of each fake by its I story |
| Platform administrator | Owns the gateway-bff composite routes and the SIT and UAT booking the run needs |
| No approval applies | The story takes no decision and the harness asserts the decisions of the owning stories |

### 11. Data

The harness owns no table (DP-01, DP-18). It seeds and reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write | Owning schema |
|---|---|---|---|---|
| DF-ACE-001 | v_ace_account | account_key | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-008 | v_ace_account | product_key | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-018 | v_ace_account | days_past_due | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-020 | v_ace_account | total_balance | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-036 | v_ace_account | data_as_of | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-056 | v_ace_customer | person_key | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-108 | v_ace_efs_action | efs_record_key | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-111 | v_ace_efs_action | action_code | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-114 | v_ace_efs_action | contact_at | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-119 | v_ace_efs_action | is_ptp | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-122 | v_ace_efs_action | promise_date | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-ACE-123 | v_ace_efs_action | promise_amount | Read through the P1 contract | rwb_source_data (the ACE view) |
| DF-CAS-002 | recovery_case | case_no | Read through the P3 contract | rwb_case |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 contract | rwb_case |
| DF-CAS-004 | recovery_case | primary_person_key | Read through the P3 contract | rwb_case |
| DF-CAS-005 | recovery_case | status | Read through the P3 contract | rwb_case |
| DF-CAS-013 | recovery_case | entry_date | Read through the P3 contract | rwb_case |
| DF-CAS-014 | recovery_case | dpd_at_entry | Read through the P3 contract | rwb_case |
| DF-CAS-016 | recovery_case | total_outstanding_at_entry | Read through the P3 contract | rwb_case |
| DF-CAS-025 | case_account | case_id | Read through the P3 contract | rwb_case |
| DF-CAS-026 | case_account | account_key | Read through the P3 contract | rwb_case |
| DF-CAS-027 | case_account | is_primary | Read through the P3 contract | rwb_case |
| DF-CAS-028 | case_account | linked_from | Read through the P3 contract | rwb_case |
| DF-INT-002 | interaction | case_id | Read through the P1 contract | rwb_source_data |
| DF-INT-003 | interaction | person_key | Read through the P1 contract | rwb_source_data |
| DF-INT-004 | interaction | occurred_at | Read through the P1 contract | rwb_source_data |
| DF-INT-005 | interaction | channel | Read through the P1 contract | rwb_source_data |
| DF-INT-006 | interaction | direction | Read through the P1 contract | rwb_source_data |
| DF-INT-007 | interaction | action_code | Read through the P1 contract | rwb_source_data |
| DF-INT-008 | interaction | contact_result | Read through the P1 contract | rwb_source_data |
| DF-INT-009 | interaction | promise_amount | Read through the P1 contract | rwb_source_data |
| DF-INT-010 | interaction | promise_date | Read through the P1 contract | rwb_source_data |
| DF-INT-013 | interaction | source_system | Read through the P1 contract | rwb_source_data |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 contract | rwb_decision |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | all fields | Read through the P1 contract | rwb_source_data |
| DF-OPS-178 to DF-OPS-183 | processed_event | all fields | Read through the inbox library in the consumer's own schema | the platform inbox library (owner PLT in the Ownership Map); the table sits in each consuming service's schema |

The legacy story put the ledger append on P7 and read the run summary from the same place. That is not the ownership now: `interaction`, `efs_ledger_outcome` and `reconciliation_result` are P1 rwb-source-data's tables in `rwb_source_data` (DP-18 and the R-PREC default ruling on the interaction ledger); `recovery_case` and `case_account` are P3 rwb-case's in `rwb_case`; `decision_log_entry` is P7 rwb-decision's in `rwb_decision`; `processed_event` is the platform inbox library's, held once per consuming schema. Each of these owners is the one the Ownership Map gives, and the harness reads every one of them through the owner's contract only.

Test data is synthetic. No production case, party, account or EFS row is used, and no personal data is written to a run report.

### 12. Contract

This is an integration story: it publishes nothing and consumes the real contracts. No screen is built by this story; the empty, loading, error and no access states of SCR-02, SCR-04 and SCR-45 are not owned here.

#### 12.1 REST operations provided

None. The harness provides no REST operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The DP01 and DP05 stamps at the business date, fresh or stale (AC9, AC10) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The published product records of the case, read with the required `caseId` (AC9); the run summary is not served here (its read is not specified, GAP-0651) |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data | The REC-05 result rows (`recCode=REC-05`) and their break detail for "A-0003" (AC5); how a break of `listEligibleAccounts` reaches this list is open (GAP-0575) |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The 16 entries with source system "EFS" and the action code of each row (AC1, AC9, AC11) |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The EFS append the hand-over step calls: UUID `Idempotency-Key`, body `idempotencyKey` `EFS:<efsRecordKey>`; 201 first, 200 for the repeat of AC11 |
| POST | Pending: path of the rerun of a business date, tracked as GAP-2258 | P3 rwb-case | The administrative rerun request, refused for a role without the right (TC-E2-001-09-ITG); the step itself is started by `AceDataReady` (DP-10) |
| GET | `/api/recovery/integration/v1/admin/scheduled-jobs` | P2 rwb-integration | The recorded run of the hand-over step: run or held, and the waiting count (AC9, AC10, AC11) |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The case list at the business date: one case, status "NEW", entry date 2026-12-15, or the two cases of 2026-12-17 (AC9, AC10, AC11) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts: product group, status, entry date and days past due at entry (AC1, AC9) |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | P3 rwb-case | The account link of "A-0002" to "RW-2026-000210", linked from 2026-12-15 and is primary false (the cited AC4) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The one central ledger entry for the creation, and one after the duplicate (AC9, AC11) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role and rights of the caller for the refusal of TC-E2-001-09-ITG |

The two interaction operations are P1's under the ruling recorded in the Ownership Map: the interaction ledger is `rwb-source-data`'s (DP-18) and rwb-case reads it through the P1 contract. The case list and the case timeline a screen consumes are read through the gateway-bff composite route of DP-19, owned by RWB-PLT-N001-CON; its path and merge order are Not specified in the source documents (GAP-0388; ASM-0563).

The rerun request for a business date of the entry run is an admin operation on the rwb-case base `/api/recovery/case/v1`, answering 409 with MSG-P2-006 while the workflow for that business date runs. It belongs to P3 rwb-case, and its path is Not specified in the source documents (GAP-2258). The harness drives this refusal only through the criterion owned by RWB-P3-E2001-APP.

#### 12.3 Events published

None. The harness publishes no Kafka event; it replays a captured `AceDataReady` envelope as a test producer into the owner's topic, on the owner's contract.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | Record key `{sourceSystem}:{businessDate}`; payload `sourceSystem`, `businessDate`, `status`, `completedAt`; only the message with `sourceSystem` ALS and `status` COMPLETED drives the step for that business date (AC9, AC10, AC11). `rwb.source-data.AceDataLate.v1`, same key, published at 05:30 when the batch is not COMPLETED (AC10) |
| rwb.case.CaseCreated.v1 | rwb.case.events.v1 | P3 rwb-case | One message per case with business date 2026-12-14, published once and not again on the duplicate (AC1, AC9, AC11) |
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | All 19 services publish it; P7 rwb-decision seals the central ledger | One record for the creation, written locally in the same transaction and deduped in the inbox, so the central ledger holds one entry (BR7, BR10; AC9, AC11) |

The harness consumes these topics as a test consumer with its own group and asserts the records through the owners' reads; it holds no inbox table of its own, gets no production record, and publishes nothing.

#### 12.5 Workflows and activities

| Name | Type | Task queue | What the harness asserts |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case (P3) | rwb-case | One workflow per case on the case id; the harness reads the workflow list and starts none |
| the hand-over step of the legacy journey | Event-started step of the DailyCaseRun chain (DP-10) | rwb-integration | It starts on `AceDataReady` for ALS with `status` COMPLETED and runs once per business date; it holds while the ALS batch is not COMPLETED. A stale DP05 alone does not hold case creation: `GET /efs-history` answers 409 MSG-P1-001 unless DP01 and DP05 are both complete, the run retries every 5 minutes until DP05 is stamped or `handover.hold_until`, then hands over without history and appends the rows when DP05 arrives under the key `EFS:<efsRecordKey>` (RD-P1-067); the harness watches the queue and starts nothing |
| the ledger consumer of `rwb.decision-record.v1` | Consumer inside the service, not a workflow of this story | rwb-decision | One append per decision message, deduped through the inbox; the harness asserts the entry, not the implementation |

The harness starts no workflow and calls no activity. DailyCaseRun itself is P3 rwb-case's per the Ownership Map (an event-started workflow); the hand-over step that this run watches is rwb-integration's.

#### 12.6 Schedules

| Schedule | Cadence | Owner | What the harness reads |
|---|---|---|---|
| JOB-06 morning allocation | 06:30 | P3 rwb-case | The Schedule list of rwb-case, to assert that no Schedule drives JOB-02 and that allocation follows the run; never started |
| JOB-14 chain check | 02:00 | P7 rwb-decision | The last chain-check result over the ledger entry the run produced; never started |

Both are read from the owners' Schedule lists. The harness creates, starts, pauses and deletes none, and it asserts that the hand-over has no Quartz trigger and no Schedule of its own (DP-10).

#### 12.7 Tables owned

None. The harness owns no table and no schema (DP-01). The tables the run proves are `interaction`, `efs_ledger_outcome` and `reconciliation_result` in `rwb_source_data` (P1), `recovery_case` and `case_account` in `rwb_case` (P3) and `decision_log_entry` in `rwb_decision` (P7), each owned by its app story.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-source-data (published provider fake, contract 5.1.0) | `GET /api/recovery/source-data/v1/data-products/freshness`, `GET /api/recovery/source-data/v1/data-products/{productCode}/records`, `GET /api/recovery/source-data/v1/admin/reconciliation/results`, `GET /api/recovery/source-data/v1/efs-history`, `GET` and `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` and the activity fake of `listEligibleAccounts`, with the fixtures of "A-0001", "A-0003", the 16 entries of 2026-12-14, the `LOADED` answer of 2026-12-14 and the `STALE` DP01 and DP05 answer for 2026-12-15 | AC1, AC5, AC9, AC10, AC11; every ledger and freshness read of the run |
| rwb-case (WireMock, from its OpenAPI) | `GET /api/recovery/case/v1/cases`, `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/accounts` with the case of "A-0001", the open case "RW-2026-000210" and the two cases of 2026-12-17 | AC1, AC6, AC9, AC10, AC11 |
| rwb-integration (WireMock, from its OpenAPI) | The hand-over step seam: `GET /api/recovery/integration/v1/admin/scheduled-jobs` with the recorded run of 2026-12-14, the held run of 2026-12-15 and its waiting count | AC9, AC10, AC11 |
| rwb-decision (WireMock, from its OpenAPI) | `GET /api/recovery/decision/v1/decision-log` with one entry for the creation, the one entry of AC11 and the one entry of the decision-log failure case | AC7 (driven), AC9, AC11; TC-E2-001-10-ITG |
| rwb-access (WireMock, from its OpenAPI) | `GET /api/recovery/access/v1/me/session` with the role and rights of the caller for the refusal | TC-E2-001-09-ITG |

The fakes are published from the owning services' OpenAPI documents and are versioned with the harness pack; the fake library version of each fake, including rwb-access, is Not specified in the source documents (DOR-RWB-ITG-E2001-ITG-22). The harness repository, its SIT and UAT environments, its seeding, its per-run evidence format and retention and its pass/fail gate are Not specified in the source documents (GAP-0388; ASM-0563).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 12 consumed, each one hop on the owner's `/api/recovery/<short>/v1` base with a 2 s timeout (DP-11, DP-13) |
| Kafka | 0 published, 3 observed: `rwb.source-data.AceDataReady.v1`, `rwb.case.CaseCreated.v1` and `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` |
| Temporal | 0 started, 3 queues watched: `rwb-case`, `rwb-integration` and `rwb-decision` |
| File | None |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract only; only rwb-source-data reads `recovery.v_ace_*` (D-RCV-60) | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies those patterns add (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON) are delivered by the service and platform stories and are not repeated in the metadata H column, which stays None; DP-01, DP-05, DP-11 and DP-18 add no dependency at all, and the C rows on DP-06 and DP-07 are build-against-the-contract only. The story's real gate is the six I stories: they replace the fakes with the real behaviour, and they gate the done state, not the Day-1 start.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| EfsHandoverJourneyRunner | Test harness | Runs the fourteen `-ITG` cases of §16 in one run per business date, in fake or real mode per service, and stops at the first failed assertion with the trace |
| HandoverClient | Harness adapter | Calls the twelve consumed operations of §12.2 through one hop and records the answer and the elapsed time |
| HandoverEventReplayer | Harness adapter | Replays the captured `AceDataReady` envelope with event ID "EVT-SYN-2614-01", including the duplicate of AC11, and reads `rwb.case.CaseCreated.v1` and `rwb.decision.DecisionRecorded.v1` |
| FakePack | WireMock project | Serves rwb-source-data, rwb-case, rwb-integration, rwb-decision and rwb-access of §12.8 from the published OpenAPI documents |
| HandoverSeedLoader | Service | Seeds the accounts "A-0001" to "A-0004", the 14 contact and 2 promise rows, the open case "RW-2026-000210", the ACE batch rows of the four business dates and the parameter and outcome rows through the owner's contract or the fake; in real mode the ACE view and batch rows come from the rwb-source-data sandbox seed and are not written by the loader |
| CaseAsserter | Assertion | Asserts the one case, its status "NEW", its product group, its entry date, its days past due at entry and the account link |
| LedgerAsserter | Assertion | Asserts the 16 entries, their source system "EFS", their action code and their `efs_record_key`, and that the set does not grow on a repeat |
| SummaryAsserter | Assertion | Asserts the run summary: the counts, the waiting count of a held run and the gap date 2026-12-15 |
| DecisionRecordAsserter | Assertion | Asserts one local record written with the state change and one central ledger entry, and that the entry holds business date 2026-12-14 in its inputs snapshot |
| RefusalAsserter | Assertion | Asserts MSG-P1-001, MSG-P2-007, MSG-P4-002 and MSG-P7-003 by id and rendered text |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference, any FOREIGN KEY between two schemas, any second reader of `recovery.v_ace_*` and any call deeper than one hop |
| RunLock | Service | One run at a time in the harness environment |
| EvidenceReportPublisher | Reporter | Writes the per-run evidence report keyed by story id and business date and attaches it to the release record |
| JourneyGate | Assertion | Passes the run only when every owned criterion passes; fails and names the criterion, the seam and the observed value otherwise |

**Database.** None. The harness owns no schema, runs no Flyway migration and holds no table; seeds and assertions go through the contracts (DP-01).

**Environment and test data.** SIT for the run of record and UAT for the acceptance run, with `rwb.integration.efs-handover` on in both. The data are the synthetic seeds of the legacy story: "A-0001" for customer "C-0001", product group "MORTGAGE", 90 days past due in `v_ace_account` at business date 2026-12-14, with 14 contact rows and 2 promise rows in `v_ace_efs_action`; "A-0002" of customer "C-0002", product group "SSME", with open case "RW-2026-000210"; "A-0003" with no row in `v_ace_customer`; "A-0004" of the decision-log failure case; the ACE batch rows of 2026-12-14 COMPLETED at 05:20, 2026-12-15 not COMPLETED by 09:00 on 2026-12-16, 2026-12-16 COMPLETED at 05:15 on 2026-12-17; parameter `case.entry.dpd_threshold` = 90 and `handover.hold_until` = 09:00; the `efs_ledger_outcome` rows of the copied action codes. Each run starts from the seeded state, so a repeated run is deterministic. The harness repository, its SIT and UAT environments, its seeding, its evidence format and retention and its pass/fail gate are Not specified in the source documents (GAP-0388; ASM-0563).

**Build steps**

1. Build EfsHandoverJourneyRunner and HandoverClient against the published OpenAPI documents of the six services and the gateway-bff routes.
2. Publish FakePack for rwb-source-data, rwb-case, rwb-integration and rwb-decision from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Write HandoverSeedLoader and the seed files for "A-0001" to "A-0004" and the four business dates, with the run lock and the fake or real mode per service.
4. Write HandoverEventReplayer for the ready batch, the duplicate event ID of AC11 and the two consumed events, with a unit test on the captured envelopes.
5. Write CaseAsserter, LedgerAsserter, DecisionRecordAsserter and SummaryAsserter for AC1, AC9 and AC11, with a unit test on fixtures for every asserted field.
6. Write RefusalAsserter for the held run of AC3 and AC10, the break of AC5 and the refusal of TC-E2-001-09-ITG.
7. Write SchemaBoundaryCheck and prove it fails on a planted cross-schema key, a planted cross-schema select and a second `recovery.v_ace_*` reader.
8. Replace each fake with the real service as its I story lands, in the order rwb-source-data, rwb-integration, rwb-case, rwb-decision, and rerun in UAT.
9. Write JourneyGate and EvidenceReportPublisher, and attach the report to the release record for the build under test.

**Feature switch.** `rwb.integration.efs-handover`, the legacy switch of this story: on in SIT and UAT. The harness asserts the off state on the fakes — no case is created, no entry is appended and the step does not start — and asserts that the case table and the ledger are unchanged in that state.

**Done when.** The fourteen `-ITG` test cases of section 16 pass in SIT and UAT with the six I stories in place and not only against the fakes; the evidence report for the run is attached to the release record with the eight owned criteria green; the boundary check passes with no exception; and the held run, the gap date, the break and the duplicate are green with the messages of section 14.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | Data product stale after an incomplete ACE batch | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-007 | Case creation held for an incomplete ACE batch | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | Rerun while the hand-over step runs | {job} is already running. Wait for it to finish before you run it again. |
| MSG-P4-002 | A role without the right requests the administrative rerun | You cannot {action} here. Your role does not include it. |

The harness asserts the message id and the rendered text of each row and never rewrites it. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-02 Case list | Loading | The first call returns the one case of "A-0001" with status "NEW" and entry date 2026-12-15 through the gateway-bff composite route |
| SCR-02 Case list | List | The two cases of entry date 2026-12-17 are listed after the good batch, and the held run of 2026-12-15 adds none |
| SCR-02 Case list | Loading | Not specified in the source documents (CG-ALL-534) |
| SCR-02 Case list | Empty | The empty state of Screen Specifications v1 SCR-02; not owned by this story |
| SCR-02 Case list | Error | Not specified in the source documents (CG-ALL-534) |
| SCR-02 Case list | No access | Not specified in the source documents (CG-ALL-534) |
| SCR-04 Case timeline | Loading | The EFS history of the case reads with source EFS and its 16 entries, through the composite route |
| SCR-04 Case timeline | Filtered | The source filter on EFS narrows to the 16 entries without dropping the action code of a row |
| SCR-04 Case timeline | Empty | Not specified in the source documents (CG-ALL-535) |
| SCR-04 Case timeline | Error | Not specified in the source documents (CG-ALL-535) |
| SCR-04 Case timeline | No access | Not specified in the source documents (CG-ALL-535) |
| SCR-45 Data quality | Held run | The stale stamp, MSG-P1-001 and the REC-05 break listing "A-0003" are shown to the data steward through the composite route |
| SCR-45 Data quality | Loading | The loading state of Screen Specifications v1 SCR-45; not owned by this story |
| SCR-45 Data quality | Empty | Not specified in the source documents (CG-ALL-536) |
| SCR-45 Data quality | Error | Not specified in the source documents (CG-ALL-536) |
| SCR-45 Data quality | No access | Not specified in the source documents (CG-ALL-536) |

The harness builds no screen and renders no page: it asserts the composite route answer the screen consumes, and the screen-level behaviour stays with the P3 and P1 stories. The composite route paths and their merge order are Not specified in the source documents (GAP-0388; ASM-0563).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-001-09-ITG | AC13, Access | Component | As-built regression only: RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |
| TC-E2-001-01-ITG | AC1, BR1, BR3, BR5 | Integration | Synthetic account A-0001 with 14 contact rows and 2 promise rows served by the rwb-source-data contract fake |
| TC-E2-001-02-ITG | AC2 (run by RWB-P2-E2001-APP), BR6 | Integration | Same business date run twice |
| TC-E2-001-03-ITG | AC3, BR4 | Integration | ACE batch for ALS of 2026-12-15 not COMPLETED |
| TC-E2-001-04-ITG | AC4 (run by RWB-P3-E2001-APP), BR2 | Integration | Customer C-0002 with an open SSME case |
| TC-E2-001-05-ITG | AC5, BR8 | Integration | Account A-0003 with no customer row in the rwb-source-data contract fake |
| TC-E2-001-06-ITG | AC6, BR4 | Integration | Good batch on 2026-12-17 after a missed day |
| TC-E2-001-07-ITG | AC7 (run by RWB-P3-E2001-APP), BR7 | Integration | Write of the local decision record in the case transaction forced to fail |
| TC-E2-001-08-ITG | AC8 (run by RWB-P3-E2001-APP) | Integration | Event-started hand-over step running in rwb-integration |
| TC-E2-001-10-ITG | Principle 5 | NFR | Local decision record write forced to fail during a run of 50 synthetic accounts; no case is created without its decision record |
| TC-ITG-E2001-01 | AC9, BR11 | Integration | AceDataReady for ALS at 2026-12-14 with event ID "EVT-SYN-2614-01"; the one case, the 16 entries, the one ledger entry and the one CaseCreated |
| TC-ITG-E2001-02 | AC10 | Integration | ALS batch of 2026-12-15 not COMPLETED with DP05 STALE at business date 2026-12-14, and the good batch of 2026-12-16; the waiting count and the gap date 2026-12-15 |
| TC-ITG-E2001-03 | AC11 | Integration | The same event ID delivered twice and the step rerun for 2026-12-14; one case, 16 entries, one event and one ledger entry |
| TC-ITG-E2001-04 | AC12, BR9, BR10 | Integration | Every foreign key, grant and view definition of the 19 per-service schemas; a planted cross-schema key, a planted cross-schema select, a second `recovery.v_ace_*` reader and a two-hop call |
| TC-ITG-E2001-05 | §12 operations and events | Contract | Every consumed operation of section 12 called against the contract fakes of section 12.8, and every observed event of section 12 checked against its published contract; the harness calls no activity |
| TC-ITG-E2001-06 | AC13 | Integration | Caller holding a role without Platform administration U requests the rwb-case rerun of a business date (path pending, GAP-2258); refused with MSG-P4-002. Changed in version 3 |
| TC-ITG-E2001-07 | AC14, BR9, BR10, BR11 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E2001-ITG-AC14) |
| TC-ITG-E2001-08 | AC15 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E2001-ITG-AC15) |
| TC-ITG-E2001-09 | AC16 | Integration | rwb-source-data contract fake set to fail or not answer within 2 s the freshness call for business date 2026-12-14 |
| TC-ITG-E2001-10 | AC17 | Integration | Case with status "NEW" for "A-0001"; a status change the case model does not allow is requested; the change is refused and the status stays "NEW" |

AC3, AC9, AC10, AC11 and AC13 changed in version 3. Test Cases v9: TC-E2-001-03-ITG, TC-ITG-E2001-01, TC-ITG-E2001-02, TC-ITG-E2001-03, TC-E2-001-09-ITG, TC-ITG-E2001-06.

The `-ITG` cases carry the legacy base id of the legacy test case and add the seam each one exercises across services; the legacy test cases remain the record of the app stories. AC2, AC4, AC7 and AC8 of the legacy key are owned by the app stories of this key — the repeat and the decision-log failure by RWB-P2-E2001-APP and RWB-P3-E2001-APP, the account link by RWB-P3-E2001-APP — and they are not restated here; their `-ITG` cases drive the same seam and do not claim the criterion. The full legacy test, with its Given, When and Then, is in the Test Cases workbook, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the threshold, the hold time, the product map and the copied action codes are rows held by their owners; the harness reads them and never holds a copy.
- No personal data in events, workflow inputs, logs, traces or reports: the seeds are synthetic keys, events carry IDs and facts, and the evidence report holds IDs, action codes, dates, counts and results only.
- ACE data only through the owner's contract or `recovery.v_ace_*` read by rwb-source-data (DP-05); the harness never reads a view and never names an ACE table.
- No cross-schema read and no FOREIGN KEY between two schemas: every read goes through the owner's contract, and SchemaBoundaryCheck fails the run on a violation (DP-01, DP-11).
- No production data and no outside system: the harness calls only the six services and their fakes, never a production endpoint and never WIN, ALS or any other outside system.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner, and every call carries the 2 s timeout.
- The harness owns no table, no endpoint, no screen, no workflow and no schedule (DP-01, DP-10, DP-18); it is test and evidence only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Contract element | Test cases |
|---|---|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the daily ALS batch | Business Requirements Program, section 5.2; Business Requirements Epic 2, section 3.2 | FEAT-CHO-01 | `rwb.source-data.AceDataReady.v1` and the DP01 and DP05 read on `GET /api/recovery/source-data/v1/data-products/freshness` | TC-E2-001-01-ITG, TC-E2-001-02-ITG, TC-ITG-E2001-01, TC-ITG-E2001-02, TC-ITG-E2001-03 |
| REQ-CHO-001 | Case with full contact and promise history | Business Requirements Program, section 5.3; Business Requirements Epic 2, section 3.2 | FEAT-CHO-01 | The 16 entries on `GET` and `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` | TC-E2-001-01-ITG, TC-E2-001-05-ITG, TC-ITG-E2001-01, TC-ITG-E2001-03 |
| REQ-CHO-005 | Workbench is the system of record for case state after hand-over | Business Requirements Program, section 5.3; Business Requirements Epic 2, section 3.2 | FEAT-CHO-04 | `GET /api/recovery/case/v1/cases`, `GET /api/recovery/case/v1/cases/{caseId}` and `rwb.case.CaseCreated.v1` | TC-E2-001-04-ITG, TC-E2-001-07-ITG, TC-E2-001-10-ITG, TC-ITG-E2001-01, TC-ITG-E2001-03 |
| REQ-RDF-003 | EFS history transfers to the case | Business Requirements Program, section 5.1; Business Requirements Epic 2, section 3.2 | FEAT-CHO-05 | The EFS append in `rwb_source_data` through the P1 contract, and the P1 ACE view contract (DP-05, DP-18) | TC-E2-001-03-ITG, TC-E2-001-06-ITG, TC-E2-001-08-ITG, TC-ITG-E2001-02 |

The four requirements keep their legacy BRD section and feature exactly as the legacy story tabs them, and the legacy rule text is unchanged; the contract element names where the integration run sees the requirement.

### 19. Out of scope

- The six I stories and everything they build: RWB-P1-E1069-APP (the read-only ACE view contract), RWB-P1-E1015-APP (the freshness stamp and `AceDataReady`), RWB-P2-E2001-APP (HandoverService, the group builder and the run summary), RWB-P1-E2001-APP (the EFS history read and the interaction append), RWB-P3-E2001-APP (case creation, the account link and `CaseCreated`) and RWB-P7-E2001-APP (the local decision record and the central ledger).
- AC2, AC4, AC7 and AC8 of the legacy key, which stay with the app stories.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-source-data, rwb-integration, rwb-case, rwb-access and rwb-decision, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The neighbouring integration stories of the same business epic: RWB-E2-002 (ACE plan status on the case) and RWB-E2-034 (the interaction ledger on the case and from every channel).

### 20. Remaining delivery steps

- Size the story (squad; DOR-RWB-ITG-E2001-ITG-16).
- Sign the epic design (solution architect).
- Publish the rwb-source-data contract and provider fake 5.1.0 and the other owners' contracts (service teams).
- Load the synthetic test data in SIT and UAT (QA with the owning teams).
- Run the Test Cases v9 rows for the changed AC3, AC9, AC10, AC11 and AC13: TC-E2-001-03-ITG, TC-ITG-E2001-01, TC-ITG-E2001-02, TC-ITG-E2001-03, TC-E2-001-09-ITG, TC-ITG-E2001-06.
- Pending: rerun path of the entry run, owner rwb-case tech lead, tracked as GAP-2258.
- Pending: run summary read, owner rwb-integration tech lead, tracked as GAP-0651.
- Pending: the catalog row of `handover.hold_until`, owner rwb-integration owner with RW-COE, tracked as NEW-GAP-D4; the late EFS history path (RD-P1-067) needs its own test case row (owner: test writer).
- Pending: sandbox fixtures for A-0001 to A-0004 and the four batch dates, owner rwb-source-data tech lead, tracked as NEW-GAP-F04-5.
