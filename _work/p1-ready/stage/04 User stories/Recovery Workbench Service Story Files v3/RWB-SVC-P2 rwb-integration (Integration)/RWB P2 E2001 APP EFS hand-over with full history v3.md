# RWB-P2-E2001-APP EFS hand-over with full history

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Size | Set by the squad at refinement (DOR-RWB-P2-E2001-APP-16) |
| Legacy key | RWB-E2-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP18, DP19 |
| Readiness decisions | RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-008, RD-P1-010, RD-P1-012, RD-P1-022, RD-P1-040, RD-P1-041, RD-P1-011, RD-P1-064, RD-P1-066, RD-P1-067 |
| Parallel lane | L-P2-A |
| Ready to start | After RWB-P2-E1007-APP (not done yet) and RWB-P2-E2001-OPS (not done yet) |
| Depends on (build) | RWB-P2-E2001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P2-E1007-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P1-E1015-CON, RWB-P1-E1066-CON (ledger append), and the `GET /efs-history` fragment and `listEligibleAccounts` types of rwb-source-data |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) and asyncapi/rwb-source-data.asyncapi.yaml 5.1.0; RWB-P2-E2001-CON v1 (the `/v1` path of the contract) |
| Integration dependencies | None |
| External dependencies | RWB-P2-E2001-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-019) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-001 for rwb-integration. The legacy story created the case, linked the further account, appended the EFS history and held a stale batch inside one recovery service; this story builds the hand-over step of that journey in rwb-integration — the listener, the group builder, the calls to the owners and the run summary — and leaves case creation and the account link with rwb-case, the EFS history read and the interaction ledger with rwb-source-data, and the central ledger with rwb-decision. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E2001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 41 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

- D-RCV-60 finishing pass: RD-P1-004, RD-P1-064, RD-P1-066, RD-P1-067; requests S8-stories-0412, W2-tests-3490; Test Cases v9 mappings.
- D-RCV-60 finishing pass, reconciliation: the AC22 test row states the durable-timer retry and the late append (RD-P1-067).

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- Candidates, person keys, product group and breaks come from the `listEligibleAccounts` output that `DailyCaseRun` passes; the REST candidate, candidate-fact and customer reads and the product map are removed (RD-P1-010; findings #1, #3).
- The history is read with `GET /efs-history` and appended one row per call with the fixed mapping; written and skipped are counted from 201 and 200; the REC-01 write and the P1 job rerun are removed (RD-P1-007, RD-P1-012, RD-P1-022; findings #4, #5, #7).
- `AceDataReady` starts the step only for `sourceSystem` ALS and `status` COMPLETED, other sources are acknowledged and ignored; `DecisionRecorded` type, freshness states and payload handling corrected (RD-P1-003, RD-P1-008, RD-P1-040, RD-P1-041; findings #8, #9, #10, #12).
- X11, X12 and AC21 to AC24 added (finding #11).
- Open: how the candidates reach the step (GAP-3374) and who applies the action-code filter (GAP-3375) (findings #2, #6).

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the hand-over step of the morning run to take the ACE hand-over of the business date, group it by customer and product group, ask rwb-case to create or link the case, read the EFS contact and promise history of the account from rwb-source-data and append it to the interaction ledger one entry at a time, and record its own run summary**, so that **the case starts the morning after the account reaches 90 days past due with what happened before day 90, and every run of the step is repeatable, holdable and provable without reading code**.

This story is one of the four app stories of the legacy key. The accepted split, stated by RWB-ITG-E2001-ITG and fixed by the Ownership Map (ASM-1088), is: **RWB-P1-E2001-APP** owns the EFS history read and rwb-source-data owns the interaction ledger the rows are appended to; **this story** owns `HandoverService`, `HandoverGroupBuilder`, `HandoverSummaryWriter` and `AceDataReadyListener`; **RWB-P3-E2001-APP** owns case creation, the account link and `CaseCreated`; **RWB-P7-E2001-APP** owns the local decision record and the central ledger. JOB-02 stays with rwb-case, while the hand-over step runs here, event-started on `AceDataReady`.

### 2. Business rationale

Accounts move from collections to recovery by a weekly transfer today, and the case starts without its collection history. ACE ingests the ALS hand-over and the EFS action history (D-RCV-35 U1). This story creates the case each morning from the account rows ACE holds for the business date, links a further account of the same customer and product group to the open case, and appends the EFS contact and promise history to the interaction ledger. It holds case creation while the ACE batch for the business date is incomplete, so no case is built from stale data. It meets REQ-CHO-001, REQ-CHO-005, REQ-DRI-013 and REQ-RDF-003 and is measured by CTL-01 and REC-01 (accounts at 90 days past due against open cases, zero unexplained).

The legacy story did all of it inside one deployable: three view reads, two in-process interfaces, a Quartz job and one database. Under D-RCV-60 the same journey is six services and four owners, and this slice is the step that sequences them. That makes the slice's own value precise: it is the only place that decides *which* accounts are taken for a business date, *how* they are grouped, *when* the run must hold, and *what* the run summary says. Every one of those is a decision of the hand-over, not of the case, the ledger or the central log — and each is recorded so that a held morning and a repeated morning are both explainable afterwards.

**What the split changes, and why it changes here.**

- **DP-01.** `rwb_integration` holds no copy of a case, an account, a party or an interaction, and no foreign key into another schema. The step links to them by business key (`account_key`, `person_key`, `caseId`) and reads them only through their owners' contracts.
- **DP-03.** The `DecisionLogWriter` of the monolith becomes the local decision-record library: the run's own decision — run, hold or partial — is written as one record with the legacy decision code "D6 entry", the business date, the freshness answer of DP01 and DP05 and the counts, in `rwb_integration` in the same local transaction as the run summary, and published as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for the central ledger in rwb-decision. The case-creation record itself stays rwb-case's, written in its own transaction (RWB-P3-E2001-APP).
- **DP-05.** `AceSourceQuery` and every `v_ace_*` read leave this slice. Only rwb-source-data reads the thirty `recovery.v_ace_*` views (ADR-010; Arch v5 slides 8, 9, 15 and 41; ASM-1089). The candidates, the person keys, the product group and the breaks are the output of activity `listEligibleAccounts`, which `DailyCaseRun` of rwb-case calls and passes to this step (RD-P1-010); the freshness stamps, the EFS history and the ledger append are one-hop calls of this step to rwb-source-data, 2 s (DP-11). `rwb_integration` holds no grant on `recovery`.
- **DP-06 and DP-07.** Read case.entry.dpd_threshold = 90 from rwb-case. The hand-over cut-off defaults to 09:00 pending the catalog row and value (GAP-3286). The product group of a candidate is the ACE `product_category` carried by the `listEligibleAccounts` output, and no product code map is applied (RD-P1-010).
- **DP-09.** The consumed `AceDataReady` is deduped in the inbox (`processed_event`) on `EV-26:ALS:<businessDate>`; this slice publishes no business event of its own.
- **DP-10.** The legacy `HandoverJob` Quartz trigger becomes an event-started Temporal step on the queue `rwb-integration` in the namespace `rwb-recovery`. JOB-02 itself stays rwb-case's (`DailyCaseRun`, Arch v5 slide 44), and JOB-03 allocation follows it there.
- **DP-18.** The interaction ledger is rwb-source-data's. The step calls the append once per history row; it writes no ledger table and holds none (RD-P1-007).
- **DP-19.** The case list, the case timeline and the data-quality view the case owner and the data steward read are gateway-bff composite routes, never a browser call to this service.

**What this slice does not decide.** The status, entry date and days past due at entry of a case, the account link, and `CaseCreated` are rwb-case's. The EFS history read, the ledger and its business-key dedupe are rwb-source-data's. The central ledger entry is rwb-decision's. This story calls the owners and records what came back.

### 3. Preconditions

- RWB-P2-E2001-CON is published: the activity contract of the hand-over step, the `HandoverSummary` shape, the intake of `AceDataReady`, the consumed elements of the P1, P3 and P7 contracts, the error envelope, the idempotency keys and the fakes.
- RWB-P2-E1007-APP is delivered: the integration base of rwb-integration, its controller and client conventions, its problem-response mapping, its Temporal worker and its `rwb_integration` migration sequence.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameter and reference-data client libraries with which this service reads rwb-case's values (DP-06, DP-07).
- RWB-PLT-TE006-CON is published: the outbox and inbox library with `processed_event`, `idempotency_key`, `outbox_event`, `outbox_delivery`, the retry topic and the `.dlt` topic (DP-09).
- RWB-PLT-E1071-CON is published: the workflow kit, the task queue `rwb-integration`, worker versioning and the payload codec (DP-10).
- RWB-PLT-N001-CON is published: the gateway-bff composite routes that serve SCR-02 case list, SCR-04 case timeline and SCR-45 data quality (DP-19).
- rwb-source-data publishes rwb-source-data.yaml 5.1.0 with `GET /data-products/freshness`, `GET /efs-history` and `POST /cases/{caseId}/interactions`, and the `listEligibleAccounts` types (`EligibleAccountsRequest`, `EligibleAccountsPage`) in its contract jar (RD-P1-005, RD-P1-007, RD-P1-010).
- Pending: the contract that carries the `EligibleAccountsPage` output from `DailyCaseRun` to this step, and whether this step or rwb-case drives case creation (RWB-P3-E2001-APP reads a candidate page of rwb-integration); owner solution architect, tracked as GAP-3374. Until it is settled the step is built against an `EligibleAccountsPage` fixture.
- RWB-P1-E1015-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: the freshness stamp and `AceDataReady` of rwb-source-data, and the parameter and reference-data contracts of rwb-case. These are contract dependencies and never block the build.
- The rwb-source-data contract fake (§12.8, path `fakes/rwb-source-data/5.1.0/`) and the `EligibleAccountsPage` fixture hold the synthetic facts, and the rwb-case contract fake holds the case seed; no ACE view or extension table is seeded for this story: account "A-0001" with personKey of customer "C-0001", productGroup "MORTGAGE", 90 days past due at business date 2026-12-14 with 14 contact rows and 2 promise rows of history; account "A-0002" of customer "C-0002", productGroup "SSME", with open case "RW-2026-000210"; account "A-0003" with no customer row, answered in `breaks[]`; account "A-0004" of the decision-record failure case.
- Read case.entry.dpd_threshold = 90 through rwb-case. The interim hand-over cut-off is 09:00 (GAP-3286). Their row identifiers in `parameter_value` and `reference_row` are Not specified in the source documents (GAP-0651; ASM-1094).
- Feature `rwb.integration.efs-handover` is on in DEV, SIT and UAT; the switch itself is a feature flag of the platform flag library.
- The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0651; ASM-1087).

### 4. Flow

1. rwb-source-data publishes `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1`, once per source system and business date when the batch is COMPLETED, with Kafka key `{sourceSystem}:{businessDate}` (for example `ALS:2026-12-14`) and payload `sourceSystem`, `businessDate`, `status`, `completedAt` (RD-P1-003).
2. `AceDataReadyListener`: accepts the message through the inbox on the key `EV-26:ALS:<D>`; a redelivery raises the hit count and starts no second run. Only an event with `sourceSystem` ALS and `status` COMPLETED starts this step; an event of another source system is acknowledged and ignored (RD-P1-040).
3. `EfsHandoverWorkflow`: starts with workflow ID `efs-handover-<D>`, takes the run lock `handover-run:<D>` in `idempotency_key`, and stops at once with a refusal when the lock is held by another run for D (AC8).
4. readFreshness reads the DP01 and DP05 stamps for D through the P1 freshness contract. A stale DP01 holds case entry. A stale DP05 does not hold case creation: /efs-history itself enforces the DP01 and DP05 gate (step 11).
5. readParameters reads case.entry.dpd_threshold (90). The catalog row and value for handover.hold_until are Pending, owner rwb-integration with RW-COE (GAP-3286). The interim cut-off is 09:00 Asia/Bangkok.
6. `listCandidates`: takes the candidates of business date D and the `breaks[]` of the `listEligibleAccounts` output that `DailyCaseRun` passes (fields `accountKey`, `productGroup`, `daysPastDue`, `totalBalance`, `personKey` and the exclusion facts); it calls no P1 candidate or customer read. rwb-source-data applies no exclusion and no open-case filter: those and the grouping are the caller's (rwb-case and this step), and how the two split them is part of GAP-3374. An account in `breaks[]` is not taken and is listed for the next run (RD-P1-010).
7. `HandoverService`: for each candidate calls the inbox key `handover:<account_key>:<D>`; a repeat is skipped and counted in the run summary (AC2). The source of the repeat count is Not specified in the source documents (GAP-2463), to be confirmed at the RWB-P2-E2001-CON contract review.
8. `HandoverGroupBuilder`: groups the remaining accounts by primary `person_key` and the candidate's `productGroup`; one group is one case or one link.
9. `createOrLinkCase`: for each group calls the rwb-case case-creation operation once with the group, the business date D, the entry date D+1, the days past due at entry, the total outstanding at entry and the account to be primary. rwb-case writes its own decision record first, then creates the case with status New or links the further accounts to the open case for the person and product group, and publishes `CaseCreated` in its own transaction (AC4; RWB-P3-E2001-APP).
10. rwb-case answers with the case reference (the case uuid used as `caseId`, with the case number as display value; RD-P1-023), the created-or-linked outcome and the account links; a decision-record failure is answered as a failure for that group and is carried into the run summary with MSG-P7-003 (AC7).
11. `appendEfsHistory`: for a case that is new or was found open, calls `GET /efs-history?accountKey={accountKey}&businessDate=D` once per account and then `POST /cases/{caseId}/interactions` once per returned row, with a new UUID `Idempotency-Key` header per row (reused on a retry of that row) and the body: `eventCode` CONTACT, or PROMISE when `isPtp`; `occurredAt` = `contactAt`; `actionCode`; `contactResult` RIGHT_PARTY when `isRpc`, else empty; `promiseAmount`; `promiseDate`; `actorType` SERVICE; `actorRef` `rwb-integration`; `sourceRef` `EFS v_ace_efs_action`; `idempotencyKey` `EFS:<efsRecordKey>`. A 201 counts as written and a 200 as skipped (RD-P1-007). Pending: which component keeps only the action codes of `efs_ledger_outcome` (GAP-3375). On 409 MSG-P1-001, wait on a durable timer and retry every five minutes until DP05 is stamped for D or handover.hold_until. At the cut-off hand over without history; the hand-over run appends late rows when DP05 arrives, using the same EFS:<efsRecordKey> business key. No separate completeness check is built.
12. `writeRunSummary`: on a held run, records the held outcome with the stale data product, the stale business date, the count of waiting accounts, MSG-P1-001 for the data product and MSG-P2-007 for the data steward, and names no entry date; on a good run, records the counts (accounts read, cases created, accounts linked, interaction entries appended, repeats, held, gap dates) and no reconciliation result: REC-01 is run by `ReconciliationWorkflow` of rwb-source-data (RD-P1-022).
13. `recordRunDecision`: writes one local decision record with the decision code read as data from LOV-DECISION (legacy name "D6 entry"), the business date, the freshness answer of DP01 and DP05, the counts and the outcome, in `rwb_integration`, and the library publishes `DecisionRecorded` on `rwb.decision-record.v1`; the record write and the run summary commit together, and a failed record write fails the run with MSG-P7-003 and an incident. The DecisionRecorded payload fields are owned by RWB-PLT-E1027-CON; their element names are Not specified in the source documents (GAP-1332) and are confirmed before the wave 2 build.
14. `EfsHandoverWorkflow`: releases the run lock, answers the `HandoverSummary` of §12.5, and ends. A gap business date is carried into the next good run, so a missed morning is named and not silently absorbed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same business date is run twice, or the same `AceDataReady` is redelivered | No second case or link; the repeat is counted in the run summary (R-UNI-40); its count source and key format are Not specified in the source documents (GAP-2463; GAP-0590) | None | AC2 |
| X2 | The ACE batch for ALS and business date D is not COMPLETED by 09:00 (`AceDataLate` goes out at 05:30; how 09:00 applies after it is pending, GAP-3401) | The step does not run a good morning: the data products show the stale date, the run holds with the waiting count, the data steward is alerted, and the cases are created on the next good business date | MSG-P1-001, MSG-P2-007 | AC13 (driven here; AC3 owned by RWB-P1-E2001-APP) |
| X3 | The account's `person_key` has no row in the ACE customer data | The account arrives in `breaks[]` of the `listEligibleAccounts` output, not as a candidate; it is not taken and is tried with the next run | None | AC14 (TC-E2-001-18); AC5 (owned by RWB-P1-E2001-APP; driven here) |
| X4 | The decision record of the case creation fails inside rwb-case | No case is created for that group; an incident is raised; the group is tried in the next run and the run summary carries MSG-P7-003 | MSG-P7-003 | AC7 |
| X5 | The customer already has an open case for the product group | The account is linked to that case; no new case | None | AC4 |
| X6 | The step is started again while it runs for the same business date | The second start is refused: the run lock `handover-run:<D>` is held and the answer is 409 | MSG-P2-006 | AC8 |
| X7 | A role without the right requests the administrative rerun | Refused by the rerun operation on the rwb-case base before any step starts; nothing changes | MSG-P4-002 | AC9 (TC-E2-001-09) |
| X8 | rwb-source-data, rwb-case or rwb-access does not answer inside the 2 s budget | One hop, no retry on a 4xx, retry with jitter on a 5xx; the run ends as partial with the unanswered call named, and the accounts it covered are tried in the next run | MSG-GEN-006 | AC10 (TC-E2-001-11, the CON contract tests) |
| X9 | The run's own decision record cannot be written | The run summary and the record roll back together; the run ends as failed with an incident and no `DecisionRecorded`; the next delivery starts a fresh run | MSG-P7-003 | AC11 (TC-E2-001-10) |
| X10 | A feature flag `rwb.integration.efs-handover` is off | The listener is not deployed, so no step starts and no case, link or entry is written | None | AC12 (TC-E2-001-12; RWB-P2-E2001-OPS deploys the flag) |
| X11 | GET /efs-history returns 409 MSG-P1-001 because DP01 or DP05 is incomplete for D | Retry every five minutes on a durable timer. If DP05 is still incomplete at 09:00, hand over without history and append late rows when DP05 arrives, once per EFS:<efsRecordKey> | MSG-P1-001 | AC22 |
| X12 | `POST /cases/{caseId}/interactions` answers 503 MSG-P1-022 after the retries | The rows already written stay; the run ends as partial with the failure row; a repeat of a written row answers 200 and is counted as skipped | MSG-P1-022 | AC23 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published CON story, the six platform contracts and the integration base; the P1, P3 and P7 answers come from their contract fakes and the candidates from an `EligibleAccountsPage` fixture (GAP-3374) |
| Negotiable | The threshold, the hold time and the copied action codes are rows of their owners; the story fixes only the behaviour of the step |
| Valuable | Each case starts the morning after day 90 with its collection history, and a held or repeated morning is explainable |
| Estimable | One listener, one workflow, seven activities, one group builder, one summary writer, five contract clients |
| Small | Fits two weeks with its tests |
| Testable | Each owned criterion is one automated test; every cross-service answer is stubbed at Component level |

### 7. Acceptance criteria

```gherkin
Feature: EFS hand-over with full history

  Background:
    Given parameter "case.entry.dpd_threshold" is 90
    Given the ACE batch for ALS with business date 2026-12-14 is COMPLETED at 05:20
    Given the rwb-source-data freshness fake answers DP01 and DP05 with status LOADED and businessDate 2026-12-14

  Scenario: AC2 Repeat run (legacy RWB-E2-001 AC2)
    Given the run for business date 2026-12-14 created the case for "A-0001"
    Given the rwb-case contract mock returns that one case already exists for "A-0001" and holds no open case for its customer and product group
    Given the rwb-source-data contract fake returns 16 rows for "A-0001" on GET /efs-history and answers 200 with the existing entry to each of the 16 appends, their business keys "EFS:<efsRecordKey>" being in the ledger
    When case creation runs again for business date 2026-12-14
    Then the system creates no second case and no interaction entry is added
    Then the run summary shows 1 repeat for "A-0001", interactionEntriesWritten 0 and interactionEntriesSkipped 16

  Scenario: AC4 Account linked to the open case (legacy RWB-E2-001 AC4)
    Given customer "C-0002" has open case "RW-2026-000210" for product group "SSME"
    Given synthetic account "A-0002" of "C-0002", product group "SSME", reaches 90 days past due on 2026-12-14
    Given the EligibleAccountsPage fixture for business date 2026-12-14 holds the candidate accountKey "A-0002", daysPastDue 90, productGroup "SSME" and the personKey of customer "C-0002"
    Given the rwb-case contract mock returns open case "RW-2026-000210" for customer "C-0002" and product group "SSME" and records the account link with linked from 2026-12-15 and is primary false
    When case creation runs
    Then the system creates no new case
    Then the system links "A-0002" to "RW-2026-000210" with linked from 2026-12-15 and is primary false

  Scenario: AC7 Decision log write fails (legacy RWB-E2-001 AC7)
    Given the decision record store is unavailable
    Given the rwb-case contract mock returns the decision-record failure of "A-0004" with no case created for it
    Given the rwb-source-data contract fake records every GET /efs-history and every append
    When case creation runs for "A-0004"
    Then the system creates no case for "A-0004"
    Then the system raises an incident and the run summary carries message MSG-P7-003
    Then no GET /efs-history call and no append is made for "A-0004"
    Then the system takes "A-0004" in the next run

  Scenario: AC8 Second start refused (legacy RWB-E2-001 AC8)
    Given EfsHandoverWorkflow is running for business date 2026-12-14
    Given the rwb-case contract mock returns that the administrative rerun of EfsHandoverWorkflow reaches the hand-over step for business date 2026-12-14
    Given the rwb-integration contract mock returns the run lock held for business date 2026-12-14
    When a platform administrator requests a rerun of EfsHandoverWorkflow
    Then the response is 409 with message MSG-P2-006

  Scenario: AC9 Rerun refused for a role without the right (exception X7) (new, D-RCV-60)
    Given the rwb-case contract mock refuses the administrative rerun for a role without Platform administration
    When a role without Platform administration requests a rerun of EfsHandoverWorkflow
    Then the request is refused with message MSG-P4-002
    Then no step starts and nothing changes

  Scenario: AC10 Source does not answer inside the budget (exception X8) (new, D-RCV-60)
    Given the rwb-case contract mock does not answer inside the 2 s budget for the account group of the run
    When case creation runs for business date 2026-12-14
    Then the call is one hop, with no retry on a 4xx answer and a retry with jitter on a 5xx answer
    Then the run ends as PARTIAL with the unanswered call named and message MSG-GEN-006
    Then the accounts it covered are tried in the next run

  Scenario: AC11 Run decision record cannot be written (exception X9) (new, D-RCV-60)
    Given the run decision record cannot be written
    When the run writes its summary
    Then the run summary and the record roll back together
    Then the run ends as failed with an incident and no DecisionRecorded event is published
    Then the next delivery starts a fresh run

  Scenario: AC12 Feature flag off (exception X10) (new, D-RCV-60)
    Given the feature flag rwb.integration.efs-handover is off
    When AceDataReady is delivered for ALS with business date 2026-12-14
    Then no listener is deployed and no step starts
    Then no case, account link or EFS entry is written

  Scenario: AC13 ACE batch not COMPLETED by 09:00 (exception X2) (new, D-RCV-60)
    Given the ACE batch for ALS with business date 2026-12-15 is not COMPLETED at 09:00
    When the hand-over step is due for business date 2026-12-15
    Then the step does not run a good morning and the data products show the stale date
    Then the run holds with the waiting count and the data steward is alerted
    Then the run summary carries message MSG-P1-001 and MSG-P2-007
    Then the cases are created on the next good business date

  Scenario: AC14 Account with no customer row is left for the next run (exception X3) (new, D-RCV-60)
    Given the EligibleAccountsPage fixture for business date 2026-12-14 holds "A-0003" only in breaks[] because its person key has no customer row
    When case creation runs for business date 2026-12-14
    Then the system does not take "A-0003" and asks for no case or account link for it
    Then the step writes no REC-05 result; the break belongs to rwb-source-data
    Then the system tries "A-0003" again in the next run

  Scenario: AC15 Activity timed out and retried (exception X8) (new, D-RCV-60)
    Given the rwb-source-data contract fake does not answer GET /efs-history inside the 2 s budget
    When the hand-over activity runs for business date 2026-12-14
    Then the activity is retried with jitter on a 5xx answer and is not retried on a 4xx answer
    Then the run ends as PARTIAL with the unanswered call named and message MSG-GEN-006
    Then the accounts it covered are tried in the next run

  Scenario: AC16 Hand-over data comes only from the published surface of rwb-source-data (rule BR9) (new, D-RCV-60)
    Given the EligibleAccountsPage fixture holds the candidates and person keys of business date 2026-12-14
    Given the rwb-source-data contract fake serves GET /data-products/freshness and GET /efs-history
    When the hand-over step runs for business date 2026-12-14
    Then the step calls rwb-source-data only for freshness, EFS history and the ledger append, one hop each with a 2 s budget, and calls no candidate, candidate-fact, customer or reconciliation-write operation
    Then the step reads no "recovery.v_ace_*" view

  Scenario: AC17 Hand-over is an event-started step (rule BR10) (new, D-RCV-60)
    Given the feature flag rwb.integration.efs-handover is on
    When AceDataReady is delivered for ALS with business date 2026-12-14
    Then the hand-over starts as a Temporal step from that event
    Then no Quartz job, JOB-02 run, shared job table or Schedule is used to start it

  Scenario: AC18 The step asks the owners and writes none of their facts (rule BR11) (new, D-RCV-60)
    Given the rwb-case, rwb-source-data and rwb-decision contract mocks are in place
    When case creation runs for business date 2026-12-14
    Then the case, the account link, CaseCreated and the case-creation decision record are left to rwb-case
    Then the ledger and the EFS outcome list are left to rwb-source-data, to which the step only appends, and the central ledger to rwb-decision
    Then the step writes none of them itself

  Scenario: AC19 Run summary has no table of its own (rule BR12) (new, D-RCV-60)
    Given the run for business date 2026-12-14 has handled its accounts
    When the run writes its summary
    Then the counts are the activity result and no run summary table is written
    Then one local decision record is written with the decision code read as data from LOV-DECISION
    Then no reconciliation result is written by the step

  Scenario: AC20 Step not reachable directly from the browser (rule BR13) (new, D-RCV-60)
    Given the step is exposed through gateway-bff composite routes for SCR-02, SCR-04 and SCR-45
    When a browser calls the step directly
    Then the call is refused
    Then the step is reached only through those composite routes

  Scenario: AC21 One append per history row with the fixed mapping (new, RD-P1-007)
    Given rwb-case answers case "RW-2026-000211" with its case uuid for "A-0001"
    Given GET /efs-history for "A-0001" and business date 2026-12-14 returns 16 rows, 2 of them with isPtp true
    Given the ledger holds none of their business keys
    When the append runs
    Then 16 calls of POST /cases/{caseId}/interactions are made, each with its own UUID Idempotency-Key header
    And 14 carry eventCode CONTACT and 2 carry eventCode PROMISE with promiseAmount and promiseDate
    And every body carries occurredAt = contactAt, actorType SERVICE, actorRef "rwb-integration", sourceRef "EFS v_ace_efs_action" and idempotencyKey "EFS:<efsRecordKey>"
    And each answers 201, and the run summary shows interactionEntriesWritten 16 and interactionEntriesSkipped 0
    And the filter by efs_ledger_outcome is not asserted here (pending GAP-3375)

  Scenario: AC22 The history read refuses for an incomplete batch (new, RD-P1-010)
    Given GET /efs-history for "A-0001" answers 409 with messageCode MSG-P1-001
    When the append runs for the case of "A-0001"
    Then the run waits on a durable timer and retries the history read every five minutes through the cut-off
    And at 09:00 the hand-over completes without history if DP05 is still unstamped
    And when DP05 arrives the run appends each row once under EFS:<efsRecordKey>

  Scenario: AC23 The ledger cannot be written (new, RD-P1-007)
    Given GET /efs-history returns 16 rows and the 5th append answers 503 with messageCode MSG-P1-022 on every attempt
    When the append runs
    Then the 4 entries already written stay and the run ends as PARTIAL with MSG-P1-022 in the failures of the run summary
    And a later run counts those 4 rows as skipped from their 200 answers and appends the remaining 12

  Scenario: AC24 Another source or an unfinished batch starts nothing (new, RD-P1-040)
    Given rwb.source-data.AceDataReady.v1 arrives with sourceSystem "EFS" and status "COMPLETED"
    When the listener receives it
    Then it is acknowledged, no workflow starts and nothing is written to the dead-letter topic
    And an AceDataReady with sourceSystem "ALS" and a status other than "COMPLETED" starts no workflow
```

AC2, AC4, AC7 and AC8 are the legacy criteria this slice owns, with the origin tag on the scenario line and the legacy Background unchanged; they are copied from the legacy text, except that legacy job and decision-log wording now reads EfsHandoverWorkflow and decision record store. AC9 to AC12 cover the exception paths X7 to X10 of section 5, AC21 to AC24 cover the history read, the append and the event filter ruled by RD-P1-007, RD-P1-010 and RD-P1-040, AC13 to AC15 cover X2, X3 and X8, and AC16 to AC20 cover BR9 to BR13; none of these carries an origin tag, since they are not legacy criteria. Every cross-service part is replaced by a contract-mock Given so the criterion is provable without the other services; no legacy value is changed and no legacy line is dropped.

**Why these four.** AC2 is the step's own idempotency and its own run summary. AC4 is the step's grouping and its call to the case-creation contract, since the decision "this account belongs to the customer's open case for the product group" is taken here from the person key and the product group before rwb-case writes the link. AC7 is the step's blocking rule: the run stops for that group and the run summary carries MSG-P7-003, which is this slice's output. AC8 is the step's refusal: the rerun operation of rwb-case is the door (path pending, GAP-2258), and the run lock of this step is what answers 409.

AC1 (case from the ACE data), AC3 (late ACE batch), AC5 (customer not in the ACE customer data) and AC6 (cases created on the next good batch) stay with the app stories of this legacy key that own the facts they assert, and RWB-ITG-E2001-ITG proves them across the services. The inputs this step hands over — the candidate set, the grouping, the counts — are asserted here at Component level through the fakes of those criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case enters at 90 days past due | DL16 (ASM-1094, ASM-5264); parameter case.entry.dpd_threshold |
| BR2 | One case per customer per product group; a further account of the same customer and product group is linked to the open case | DL17 (no assumption: Not specified in the source documents (DOR-RWB-P2-E2001-APP-18)); REQ-CHO-005 |
| BR3 | The hand-over set is read for the ACE business date; the Workbench loads no source file | D-RCV-35 U1; ADR-010; REQ-DRI-013; DL06 (ASM-0189, ASM-2559, ASM-2608, ASM-2776) |
| BR4 | No case is created from a business date whose ACE batch is not COMPLETED | JOB-02; CTL-02; FEAT-CHO-05 |
| BR5 | The EFS contact and promise history of the collection period is appended to the interaction ledger with source system EFS, one entry per `efs_record_key` | DL29 (no assumption: Not specified in the source documents (DOR-RWB-P2-E2001-APP-18)); LOV-SOURCE; REQ-CHO-001; R-UNI-40 |
| BR6 | A repeat hand-over for the same account and business date is ignored and counted | R-UNI-40 |
| BR7 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | An account whose `person_key` has no customer row is held on the REC-05 business-key break and tried with the next run | REC-05; DQ-040; D-RCV-35 U2 |
| BR9 | Only rwb-source-data reads the thirty `recovery.v_ace_*` views; the candidates and person keys reach this step as the `listEligibleAccounts` output, and the freshness stamps and the EFS history are read only through the rwb-source-data contract, one hop, with a 2 s budget | ADR-010; DP-05; DP-11; Arch v5 slides 8, 9, 15 and 41 |
| BR10 | The hand-over is an event-started Temporal step on `AceDataReady`, not a Quartz job and not JOB-02; no shared job table and no Schedule is used, and JOB-02 stays with rwb-case | DP-10; ADR-016; Arch v5 slide 44 |
| BR11 | The case, the account link, `CaseCreated` and the case-creation decision record are written only by rwb-case; the interaction entries and the EFS outcome list only by rwb-source-data; the central ledger only by rwb-decision. This story asks and never writes | Arch v5 slide 41; DP-01; DP-18 |
| BR12 | The run summary has no table of this service: the counts are the activity result, and one local decision record with the decision code read as data from LOV-DECISION (legacy name "D6 entry"; exact value to be confirmed with RW-COE). REC-01 is run by rwb-source-data, not written by this step | DP-01; DP-03; legacy section 12 |
| BR13 | The step is reached only through gateway-bff composite routes for SCR-02, SCR-04 and SCR-45, never directly from the browser | DP-19 |

BR1 to BR8 are the legacy rules with their sources. BR9 to BR13 are the realignment rules this slice must obey; each one is forced by the ownership of the facts the legacy story held in one database.

### 9. State transitions

The two case transitions of the legacy story are rwb-case's: a case enters at New when `CaseCreated` is written with days past due at or above 90 and no open case for the customer and product group, and an account linked to an open case leaves the case status unchanged. This story causes both through the case-creation contract and changes neither.

The state this slice owns is the run:

| From | Event | Condition | To |
|---|---|---|---|
| Not started | `AceDataReady` for ALS accepted by the inbox | The event key is new and the flag is on | Started |
| Started | Run lock taken | No other run holds `handover-run:<D>` | Running |
| Running | DP01 not LOADED for D | The hold time has not passed | Held |
| Running | Every group answered | The groups are created or linked and the EFS appends answered | Completed |
| Running | A group fails on the decision record | rwb-case answers the record failure | Partial, with an incident and MSG-P7-003 |
| Held | The next good `AceDataReady` | The next business date is COMPLETED and DP01 is LOADED | Started, with the gap date carried |
| Completed, Partial or Held | Run lock released | The run summary and its record are committed | Not started, for the next business date |
| Started | The lock is already held for D | A second start arrives | Refused, 409 with MSG-P2-006 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-integration service identity, the hand-over step | Reads P1 freshness and EFS history, the rwb-case parameters and reference data and the rwb-access session check; calls the case-creation contract and the ledger append (`Case record` right C on the append); writes its own inbox, run lock, run summary and local decision record (Case record, C; Treatment and offer, none) |
| SY-CASEWF, case workflow module | Creates the case and the account link, writes the case-creation decision record and publishes `CaseCreated` (Case record, CU) |
| SY-DECLOG, decision log writer | Writes the local decision record of the run and, through the library, publishes `DecisionRecorded`; rwb-decision seals the central ledger (Decision log, C) |
| RW-CASEOWN, case owner | Reads the case and its history once allocated (Case record, R) |
| RW-DATASTEW, data steward | Receives the held-run alert and reads the run summary and the REC-05 break (Platform administration, R) |
| RW-PLATADM, platform administrator | Requests the administrative rerun of JOB-02 through the rerun operation of rwb-case, whose path is pending (GAP-2258) (Platform administration, U) |
| The platform flag library | Owns the `rwb.integration.efs-handover` flag and its per-environment value |

The service runs as the rwb-integration login (DP-02), carried as a secret reference and never as a literal. The login name is Not specified in the source documents (GAP-0651; ASM-1087).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 | v_ace_account, through the rwb-source-data contract | account_key | Read |
| DF-ACE-010 | v_ace_account, through the `listEligibleAccounts` output | product_category (the productGroup of the candidate) | Read |
| DF-ACE-018 | v_ace_account, through the rwb-source-data contract | days_past_due | Read |
| DF-ACE-020 | v_ace_account, through the rwb-source-data contract | total_balance | Read |
| DF-ACE-036 | v_ace_account, through the rwb-source-data contract | data_as_of | Read |
| DF-ACE-056 | v_ace_customer, through the rwb-source-data contract | person_key | Read |
| DF-ACE-108 | v_ace_efs_action, through the rwb-source-data contract | efs_record_key | Read through GET /efs-history and appended by this step |
| DF-ACE-111 | v_ace_efs_action, through the rwb-source-data contract | action_code | Read through GET /efs-history; the efs_ledger_outcome filter is pending (GAP-3375) |
| DF-ACE-114 | v_ace_efs_action, through the rwb-source-data contract | contact_at | Read through GET /efs-history and appended by this step |
| DF-ACE-119 | v_ace_efs_action, through the rwb-source-data contract | is_ptp | Read through GET /efs-history and appended by this step |
| DF-ACE-122 | v_ace_efs_action, through the rwb-source-data contract | promise_date | Read through GET /efs-history and appended by this step |
| DF-ACE-123 | v_ace_efs_action, through the rwb-source-data contract | promise_amount | Read through GET /efs-history and appended by this step |
| DF-CAS-002 | recovery_case, through the rwb-case contract | case_no | Read here; written by rwb-case (P3 story) |
| DF-CAS-003 | recovery_case, through the rwb-case contract | product_group | Requested here; written by rwb-case (P3 story) |
| DF-CAS-004 | recovery_case, through the rwb-case contract | primary_person_key | Requested here; written by rwb-case (P3 story) |
| DF-CAS-005 | recovery_case, through the rwb-case contract | status | Read here; written by rwb-case (P3 story) |
| DF-CAS-013 | recovery_case, through the rwb-case contract | entry_date | Requested here; written by rwb-case (P3 story) |
| DF-CAS-014 | recovery_case, through the rwb-case contract | dpd_at_entry | Requested here; written by rwb-case (P3 story) |
| DF-CAS-016 | recovery_case, through the rwb-case contract | total_outstanding_at_entry | Requested here; written by rwb-case (P3 story) |
| DF-CAS-025 | case_account, through the rwb-case contract | case_id | Requested here; written by rwb-case (P3 story) |
| DF-CAS-026 | case_account, through the rwb-case contract | account_key | Requested here; written by rwb-case (P3 story) |
| DF-CAS-027 | case_account, through the rwb-case contract | is_primary | Requested here; written by rwb-case (P3 story) |
| DF-CAS-028 | case_account, through the rwb-case contract | linked_from | Requested here; written by rwb-case (P3 story) |
| DF-INT-002 | interaction, through the rwb-source-data contract | case_id | Requested here; written by rwb-source-data (P1 story) |
| DF-INT-003 | interaction, through the rwb-source-data contract | person_key | Requested here; written by rwb-source-data (P1 story) |
| DF-INT-004 | interaction, through the rwb-source-data contract | occurred_at | Requested here; written by rwb-source-data (P1 story) |
| DF-INT-005 | interaction, through the rwb-source-data contract | channel | Requested here; written by rwb-source-data (P1 story) |
| DF-INT-006 | interaction, through the rwb-source-data contract | direction | Requested here; written by rwb-source-data (P1 story) |
| DF-INT-007 | interaction, through the rwb-source-data contract | action_code | Requested here; written by rwb-source-data (P1 story) |
| DF-INT-008 | interaction, through the rwb-source-data contract | contact_result | Requested here; written by rwb-source-data (P1 story) |
| DF-INT-009 | interaction, through the rwb-source-data contract | promise_amount | Requested here; written by rwb-source-data (P1 story) |
| DF-INT-010 | interaction, through the rwb-source-data contract | promise_date | Requested here; written by rwb-source-data (P1 story) |
| DF-INT-013 | interaction, through the rwb-source-data contract | source_system | Requested here; written by rwb-source-data (P1 story) |
| DF-DEC-001 to DF-DEC-018 | decision_record (library table in `rwb_integration`) | All fields of the run's own decision record: decision code, business date, the freshness answer of DP01 and DP05, the counts, the outcome and the incident reference | Write |
| DF-OPS-178 to DF-OPS-183 | processed_event (library table in `rwb_integration`) | All fields of the inbox record: consumer, key, CloudEvents id, hit count, last seen | Write |

Field IDs are those in the Logical Data Model and Data Dictionary v9. `rwb_integration` holds no ACE row, no case row, no interaction row: the service links by business key (`account_key`, `person_key`, `caseId`) and holds no foreign key into another schema (DP-01, BR11). The only rows this story writes are the inbox, the run lock and stored keys, the run's own outbox rows through the library, and the run decision record.

**Personal data.** The EFS history rows are read, mapped and appended inside one activity and are never stored, logged or placed in a workflow input or history; the candidate payloads of `listEligibleAccounts` pass the payload codec (AES-GCM, RD-P1-010). Personal-data fields carried by this story are `person_key` (DF-ACE-056) and `account_key` (DF-ACE-001), and the groups of the run summary, which carry `person_key` by person and product group. The alert and the run record carry counts, business dates, data product codes and message ids only (section 14). `decision_record` is a library table of the platform library (section 12.7), not an entity of the Logical Data Model v9 or Data Classification v5; it carries the counts, the outcome and the freshness answers of the run (DF-DEC-001 to DF-DEC-018).

**Run summary element.** One object per run, and no table of its own (ASM-1091). Its elements are the activity result of the run, not stored fields, so they carry no BR Field ID (BR12):

| Element | Content |
|---|---|
| businessDate | The ACE business date of the run, D |
| outcome | `COMPLETED`, `HELD` or `PARTIAL` |
| accountsRead | The candidates of the `listEligibleAccounts` output passed to the step |
| groupsBuilt | The groups of the run, by person and product group |
| casesCreated | The groups rwb-case answered as created |
| accountsLinked | The accounts rwb-case answered as linked to an open case |
| interactionEntriesWritten, interactionEntriesSkipped | The appends answered 201 and the appends answered 200 |
| repeats | The accounts skipped by the inbox key, one repeat per account and business date |
| held | The stale data product, its business date and the waiting account count |
| gapDates | The business dates skipped since the last good run |
| failures | One row per group that failed, with the message id |

### 12. Contract

#### 12.1 REST operations provided

None. The hand-over step is started by an event and answers an activity, not a REST call; this slice adds no path to the base `/api/recovery/integration/v1`. The recorded run of the step is read on the integration base's existing `GET /api/recovery/integration/v1/admin/scheduled-jobs` of RWB-P2-E1007-APP, which is the baseline's operation over `job_catalog`; this story adds no row to that catalogue because the step is not a Schedule, and it provides no summary endpoint, because the summary is the activity result and the local decision record (ASM-1091, ASM-1096). The activity contract itself is declared in RWB-P2-E2001-CON.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | rwb-source-data (P1) | The stamp in use of DP01 and DP05, `status` LOADED or STALE (AC2, AC13) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/efs-history?accountKey=&businessDate=` | rwb-source-data (P1) | The EFS history of one account up to the business date, one account per call; 409 MSG-P1-001 when the gate is not COMPLETE; caller the rwb-integration workload identity (AC21, AC22) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | rwb-source-data (P1) | One `InteractionRequest` per history row; header `Idempotency-Key` (UUID); body `idempotencyKey` `EFS:<efsRecordKey>`; 201 new, 200 existing, 409 MSG-PLT-N009-05, 503 MSG-P1-022 (AC21, AC23) | One hop, 2 s (DP-11) |
| POST | The case-creation operation of the rwb-case contract (legacy `CaseCreation.createOrLink`) | rwb-case (P3) | Creates the case with status New and entry date D+1, or links the further accounts to the open case for the person and product group; answers the case reference, the created-or-linked outcome and the links (AC2, AC4, AC7) | One hop, 2 s (DP-11) |
| GET | The parameter read of the rwb-case contract | rwb-case (P3) | `case.entry.dpd_threshold` = 90 and `handover.hold_until` = 09:00, with the version in force (DP-06) | One hop, 2 s (DP-11) |
| GET | The reference-data read of the rwb-case contract | rwb-case (P3) | LOV-DECISION for the decision code of the run record (DP-07) | One hop, 2 s (DP-11) |

The candidates are not a REST read: activity `listEligibleAccounts` on task queue `rwb-source-data` is called only by `DailyCaseRun` of rwb-case, and its `EligibleAccountsPage` output (`candidates[]`, `breaks[]`) is passed to this step; the carrier is Pending (GAP-3374). `GET /entry-candidates` and `GET /entry-candidate-facts` are withdrawn (RD-P1-010). There is no reconciliation-result write: `/admin/reconciliation/results` is read only (RD-P1-022). This service calls no rwb-source-data job operation: the rerun of JOB-02 is rwb-case's, path pending (GAP-2258; RD-P1-012). The case-creation operation is named by its legacy interface `CaseCreation.createOrLink`; the Ownership Map publishes no create path for rwb-case, so its path is Not specified in the source documents (GAP-0651; ASM-1090). Errors of rwb-source-data are `application/problem+json` with the shared `Problem` schema (RD-P1-004). No call chains: every row is one hop to the owner's `/api/recovery/<short>/v1` base with a 2 s budget and no retry on a 4xx.

#### 12.3 Events published

None on `rwb.integration.events.v1` by this story's own work: `FileDelivered` and `FileFailed` are the outbound-file events of the integration base, RWB-P2-E1007-APP. The local decision-record library publishes `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` from the same transaction as the run summary, with decision code "D6 entry", the business date, the freshness answer and the counts (DP-03, H RWB-PLT-E1027-CON; ASM-1092). `rwb.case.CaseCreated.v1` is published by rwb-case, not here.

#### 12.4 Events consumed

The service shares consumer group rwb-integration.rwb.source-data.events.v1 and one listener across its source-data event workflows, including JOB-08. It has READ on the main topic, READ and WRITE on retry topics and WRITE on the dead-letter topic (RD-P1-066).

| Event type | Topic | Owner | Use |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | Starts the step only for `sourceSystem` ALS and `status` COMPLETED and business date D, once per key `EV-26:ALS:<D>`; Kafka key `{sourceSystem}:{businessDate}`; payload `sourceSystem`, `businessDate`, `status`, `completedAt`; the legacy EV-26 of the story |

The message is accepted through the inbox `processed_event` on the key `EV-26:ALS:<businessDate>`; a duplicate raises the hit count and starts no run (R-UNI-40, AC2). An event of another source system, or with a status other than COMPLETED, is acknowledged and ignored (AC24). A message that fails the CloudEvents envelope or carries no business date is routed to `.dlt` with an alert and starts nothing (DP-09). `rwb.source-data.AceDataLate.v1` is not consumed here.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| EfsHandoverWorkflow | Workflow, one execution per business date, workflow ID `efs-handover-<businessDate>` | `rwb-integration` | Input: business date, source ALS, the CloudEvents id. Output: the `HandoverSummary` of §11 |
| acceptAceDataReady | Activity | `rwb-integration` | Input: the event envelope. Output: accepted or repeat, with the inbox key; the listener's record of the intake |
| readFreshness | Activity | `rwb-integration` | Input: business date. Output: the DP01 and DP05 stamps in use, each LOADED or STALE with its `businessDate` |
| listCandidates | Activity | `rwb-integration` | Input: the `EligibleAccountsPage` output passed by `DailyCaseRun` (carrier pending, GAP-3374). Output: the candidate rows and the `breaks[]` accounts left for the next run; no call is made |
| buildGroups | Activity | `rwb-integration` | Input: the candidates. Output: the groups by person key and product group |
| createOrLinkCase | Activity | `rwb-integration` | Input: one group. Output: the case reference, the created-or-linked outcome and the links; a record failure is a non-retryable class |
| appendEfsHistory | Activity | `rwb-integration` | Input: case id (uuid), account key, business date. Reads `GET /efs-history` and appends one row per call; Output: the written (201) and skipped (200) counts; no history row leaves the activity |
| writeRunSummary | Activity | `rwb-integration` | Input: the counts and the outcome. Output: the summary of §11 |
| recordRunDecision | Activity | `rwb-integration` | Input: the summary. Output: the local decision record and its outbox row; a failure fails the run (DP-03) |

The retry policy is the workflow kit's: initial interval 1 s, back-off 2, three attempts, with the 4xx answers of the case-creation and append calls classified as non-retryable except a 409, which is treated as a repeat. The workflow input and its history carry business dates, business keys, counts and codes only.

#### 12.6 Schedules

None. The step has no Schedule and no Quartz trigger: it is started by `AceDataReady` (DP-10; Arch v5 slide 44). JOB-02 case creation and JOB-03 allocation are rwb-case's and are not started, read or paused here.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| processed_event | rwb_integration | PLT library, created in `rwb_integration` | The inbox of `AceDataReady`: consumer, key `EV-26:ALS:<D>`, CloudEvents id, hit count |
| idempotency_key | rwb_integration | PLT library, created in `rwb_integration` | The run lock `handover-run:<D>` and the per-account keys `handover:<account_key>:<D>` |
| decision_record | rwb_integration | PLT library, created in `rwb_integration` | The run's own decision record, decision code "D6 entry" (DP-03) |
| outbox_event, outbox_delivery | rwb_integration | PLT library, created in `rwb_integration` | The row the decision-record library writes and the relay publishes on its behalf |

No business table is added. `interface_config`, `outbound_item` and `job_catalog` stay the integration base's and this story writes no row in them; `job_catalog` holds no run of an event-started step (ASM-1091). `interaction`, `efs_ledger_outcome` and `reconciliation_result` are rwb-source-data's in `rwb_source_data` and this story writes none of them directly; `recovery_case` and `case_account` are rwb-case's in `rwb_case`; `decision_log_entry` is rwb-decision's in `rwb_decision` (DP-01, DP-18; BR11).

#### 12.8 Contract fakes

Use the rwb-source-data provider fake 5.1.0 at fakes/rwb-source-data/5.1.0/ (RD-P1-011).

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock (`fakes/rwb-source-data/5.1.0/`) | The P1 contract | `GET /data-products/freshness` LOADED at 2026-12-14 and DP05 STALE at 2026-12-15; `GET /efs-history` 200 with 16 rows, 409 MSG-P1-001, 503 MSG-GEN-006; `POST /cases/{caseId}/interactions` 201, 200 for an existing business key and 503 MSG-P1-022 |
| `EligibleAccountsPage` fixture | The `listEligibleAccounts` output (RD-P1-010) | Candidates "A-0001", "A-0002", "A-0004" for 2026-12-14 and "A-0003" in `breaks[]` |
| rwb-case WireMock | The P3 contract and its parameters and reference data | The case-creation operation answering created, then linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false, then the decision-record failure of AC7; the parameter read returning 90 and 09:00; the reference-data read returning LOV-DECISION; the rerun request on the rwb-case base answering 409 with MSG-P2-006 while the workflow for the business date runs |
| rwb-decision WireMock | The P7 contract | The central ledger read showing one entry for the run and none for the failed group (AC7) |
| Decision-record library stub | RWB-PLT-E1027-CON | A committed record and its outbox row, and the unavailable-store case that must leave the run summary uncommitted (X9) |
| rwb-access WireMock | The P4 contract | The session check that grants the step its service rights and refuses the rerun to a role without Platform administration U (TC-E2-001-09) |
| gateway-bff composite route stub | The edge route of RWB-PLT-N001-CON | The SCR-02, SCR-04 and SCR-45 routes that read the case, the timeline and the data-quality view; this story registers no screen (DP-19) |

The fakes are published from the owning services' OpenAPI documents and are versioned with the CON baseline.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | Freshness, EFS history and ledger append on P1; case creation, parameters and reference data on P3; one hop each, 2 s timeout, GET retried once with jitter |
| Kafka | 0 published by this service's own work, 1 published by the library, 1 consumed | `rwb.source-data.events.v1` consumed with the inbox; `rwb.decision-record.v1` carries `DecisionRecorded` for the run record; `rwb.integration.events.v1` is not used by this slice |
| Temporal | 1 workflow, 9 activities | `EfsHandoverWorkflow` on the queue `rwb-integration` in the namespace `rwb-recovery`, one execution per business date |
| File | None | No file is read or written; ACE data arrives through the P1 contract and never as a file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `handover`, Java package `th.co.scb.ace.workbench.recovery.integration.handover`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_integration`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract (freshness, EFS history) and the `listEligibleAccounts` output; this service has no view of its own | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, the owner's topic, the retry topic and `.dlt` | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Event-started Temporal step through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data; the step appends through its contract | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

RWB-P3-E1042-CON, RWB-P3-E1043-CON and RWB-P1-E1015-CON are other services' contract stories, so they sit in the contract-dependency row and never block the build.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AceDataReadyListener | Listener | Consumes `AceDataReady` for ALS through the inbox, starts `EfsHandoverWorkflow` once per business date, routes a malformed message to `.dlt` |
| EfsHandoverWorkflow | Workflow | The order of the step, the run lock, the hold decision, the gap dates and the summary; no business rule in workflow code |
| HandoverService | Service | The freshness hold, the candidate set from the passed output, the per-account key, the calls to rwb-case and rwb-source-data, the counts and the outcome |
| HandoverGroupBuilder | Service | Groups the candidates by primary `person_key` and the candidate's `productGroup`; one group is one case or one link |
| HandoverSummaryWriter | Service | Builds the `HandoverSummary`, and hands the summary to the decision record |
| RunLock | Service | Takes and releases `handover-run:<D>` in `idempotency_key`; a held lock refuses the second start with 409 |
| SourceDataClient | Client | Freshness, the EFS history read and the per-row ledger append on the P1 contract (DP-05) |
| CaseContractClient | Client | The case-creation operation and the account links on the P3 contract; a record failure is a non-retryable class |
| ParameterClient, ReferenceDataClient | Client | The threshold, the hold time and LOV-DECISION through the client libraries (DP-06, DP-07) |
| DecisionRecordWriter | Library client | Writes the run record with decision code "D6 entry" in the same local transaction as the run summary; a failure fails the run (DP-03) |

**Database and migrations.** One migration in the rwb-integration sequence, `Vnnnn__handover_library_tables.sql` (nnnn is the next free number of the service's own sequence, V0001 to Vnnnn, when the migration is merged; Service Template Specification v1 §3.1): it includes the library objects `processed_event`, `idempotency_key`, `decision_record`, `outbox_event` and `outbox_delivery` in `rwb_integration` and adds the partial index on `processed_event (consumer, idempotency_key)` and on `idempotency_key (endpoint, idempotency_key)` that the intake and the run lock use (DP-09, DP-15). No business table, no column on `interface_config`, `outbound_item` or `job_catalog`, and no foreign key into another schema.

**Configuration and reference data.**

- Read case.entry.dpd_threshold = 90 from rwb-case. Confirm the handover.hold_until catalog row and value (GAP-3286); the interim cut-off is 09:00 Asia/Bangkok.
- No product code map is held: the product group is the `productGroup` of the candidate (RD-P1-010).
- The EFS action codes copied at hand-over are rows of `efs_ledger_outcome` in rwb-source-data's schema, this service names none of them, and the component that applies them to the per-row append is Pending (GAP-3375).
- The feature flag `rwb.integration.efs-handover` keeps the legacy name as the reference and is a flag of the platform library; off means no listener, so no step starts.

**Build steps**

1. `AceDataReadyListener` and the inbox key `EV-26:ALS:<D>`, with a duplicate and a malformed-envelope test (AC2).
2. `EfsHandoverWorkflow` and `RunLock`, with the refused second start of AC8 and the replay of a redelivered event.
3. `readFreshness` and the hold decision, with a LOADED and a STALE answer for DP01 and DP05.
4. `SourceDataClient` over the P1 contract for freshness, the EFS history and the per-row append, one test per answer class, and the candidate intake over the `EligibleAccountsPage` fixture.
5. `HandoverGroupBuilder` with one and two accounts per customer and product group, and an account with no customer row.
6. `CaseContractClient` over the P3 contract: created, linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false, and the record failure of AC7.
7. `HandoverSummaryWriter` for the completed, held and partial outcomes, with the repeat count of AC2 and the gap dates.
8. `DecisionRecordWriter` with decision code "D6 entry", the freshness answer and the counts, and the rollback path of X9.
9. The contract-fake run of every cross-service answer in isolation, so the story builds before rwb-source-data, rwb-case and rwb-decision are built.
10. The metrics and the run-summary series the operations story of this legacy key deploys: accounts read, cases created, accounts linked, repeats, held, gap dates.

**Done when.** The tests in section 16 pass, the step is started once per business date from `AceDataReady`, AC2, AC4, AC7 and AC8 are green against the fakes, the run writes one local decision record, `rwb_integration` holds no foreign key into another schema and no grant on `recovery`, and the contract tests of RWB-P2-E2001-CON and RWB-PLT-E1027-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product is stale at the business date of the run | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-007 | Case creation is held for an incomplete ACE batch | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-P7-003 | The decision record of a group or of the run cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | A second start or rerun while the step runs the business date | {job} is already running. Wait for it to finish before you run it again. |
| MSG-P4-002 | A role without the right requests the rerun | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A source contract did not answer inside the budget | {system} is not available. Try again in a few minutes. |
| MSG-P1-022 | The ledger append answers 503 | The text is that of Error and Message Standard v6, carried in the failures row of the run summary |

MSG-P1-001 and MSG-P2-006 use the wording of the Error and Message Standard v4 (the legacy story carries older wording of these messages). Every other text is the legacy text unchanged. An alert and a run record carry counts, business dates, data product codes and message ids only, never an account holder, a contact point or an amount.

### 15. Screens and states

No new screen. The step builds no page and renders nothing:

| Screen | State | What the case owner or the data steward sees |
|---|---|---|
| SCR-02 Case list | Loading, list | The case of the morning appears with status New and entry date D+1 once rwb-case has answered; a held morning adds none. Read through the gateway-bff composite route |
| SCR-02 Case list | Empty | Not specified in the source documents (CG-ALL-3029) |
| SCR-02 Case list | Error | Not specified in the source documents (CG-ALL-3029) |
| SCR-02 Case list | No access | Not specified in the source documents (CG-ALL-3029) |
| SCR-04 Case timeline | Loading, filtered | The EFS history of the case with source system EFS, appended by rwb-source-data on the step's request. Read through the composite route |
| SCR-04 Case timeline | Empty | Not specified in the source documents (CG-ALL-3030) |
| SCR-04 Case timeline | Error | Not specified in the source documents (CG-ALL-3030) |
| SCR-04 Case timeline | No access | Not specified in the source documents (CG-ALL-3030) |
| SCR-45 Data quality | Held run | The stale data product with MSG-P1-001, the waiting count with MSG-P2-007 and the REC-05 break. Read through the composite route |
| SCR-45 Data quality | Empty | Not specified in the source documents (CG-ALL-3031) |
| SCR-45 Data quality | Loading | Not specified in the source documents (CG-ALL-3031) |
| SCR-45 Data quality | Error | Not specified in the source documents (CG-ALL-3031) |
| SCR-45 Data quality | No access | Not specified in the source documents (CG-ALL-3031) |

The screen values are the owners': the case list and the timeline are rwb-case's reads over the rwb-source-data ledger, and the data-quality view is rwb-source-data's. This story supplies the held-run and repeat counts that the composite route merges into SCR-45 (DP-19). The route paths, the merge order and the field-level masking are Not specified in the source documents (GAP-0651; ASM-1087).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-001-09 | Access, AC9 | Component | RW-CASEOWN calls the rerun operation on the rwb-case base; refused with MSG-P4-002 |
| TC-E2-001-01 | Run by RWB-P3-E2001-APP and RWB-P1-E2001-APP; BR1, BR3, BR5 | End to end | Synthetic account A-0001 with 14 contact rows and 2 promise rows of the EFS history served by the rwb-source-data contract fake (§12.8) |
| TC-E2-001-02, TC-P2-E2001-APP-01 | AC2, BR6 | End to end | Same business date run twice |
| TC-E2-001-03 | Run by RWB-P1-E2001-APP; BR4 | End to end | ACE batch for ALS of 2026-12-15 not COMPLETED |
| TC-E2-001-04, TC-P2-E2001-APP-02 | AC4, BR2 | End to end | Customer C-0002 with an open SSME case |
| TC-E2-001-05 | Run by RWB-P1-E2001-APP; BR8 | End to end | Account A-0003 answered in `breaks[]` of the `listEligibleAccounts` output |
| TC-E2-001-06 | Run by RWB-P1-E2001-APP and RWB-P3-E2001-APP; BR4 | End to end | Good batch on 2026-12-17 after a missed day |
| TC-E2-001-07 | AC7, BR7 | End to end | Decision record store stopped |
| TC-E2-001-08 | AC8 | End to end | EfsHandoverWorkflow running |
| TC-E2-001-10 | Principle 5, AC11 | NFR | Decision record write forced to fail during a run of 50 synthetic accounts; no case is created without its entry |
| TC-P2-E2001-APP-04 | AC10, BR9; the operations, events and activities of section 12 | Contract | rwb-case contract fake does not answer inside the 2 s budget; one hop, no retry on a 4xx answer, retry with jitter on a 5xx answer; the run ends PARTIAL with MSG-GEN-006 |
| TC-E2-001-12 | AC12, BR10 | Component | Feature flag rwb.integration.efs-handover off; no listener is deployed, so no case, link or entry is written |
| TC-E2-001-13 | BR11; the tables of section 12.7 | Component | Boundary values of each table of section 12.7: processed_event, idempotency_key, decision_record, outbox_event and outbox_delivery (ASM-3438) |
| TC-P2-E2001-APP-10 | AC19, BR12 | Component | One decision record with the decision code read as data from LOV-DECISION (legacy name "D6 entry"); no reconciliation write is called |
| TC-E2-001-15 | AC20, BR13 | Component | A browser call to the step is refused; the step is reached only through gateway-bff composite routes for SCR-02, SCR-04 and SCR-45 |
| TC-P2-E2001-APP-07 | AC15, X8 | Contract | rwb-source-data contract fake: timeout, a 5xx answer and a 4xx answer on the EFS history read; one hop, retry with jitter on a 5xx only; the run ends PARTIAL with MSG-GEN-006 |
| TC-P2-E2001-APP-05 | AC13, X2 | Component | ACE batch for ALS of 2026-12-15 not COMPLETED at 09:00; the hold and messages MSG-P1-001 and MSG-P2-007 through the P1 fake |
| TC-P2-E2001-APP-06 | AC14, X3, BR8 | Component | `EligibleAccountsPage` fixture with A-0003 in `breaks[]`; no case or link is requested for it, and it is read again on the next run |
| TC-P2-E2001-APP-08 | AC16, BR9 | Component | Run for business date 2026-12-14 against the fixture and the P1 fake; only freshness, EFS history and append are called; no recovery.v_ace_* view is read |
| TC-E2-001-20 | AC17, BR10 | Component | Flag rwb.integration.efs-handover on; AceDataReady for ALS of 2026-12-14 starts the Temporal step; no Quartz job, JOB-02 run, shared job table or Schedule is used |
| TC-P2-E2001-APP-09 | AC18, BR11 | Component | Run for business date 2026-12-14 with the rwb-case, rwb-source-data and rwb-decision contract fakes; the step writes no case, account link, CaseCreated, interaction entry, EFS outcome list or central ledger entry |
| TC-P2-E2001-APP-11 | AC21, BR5 | Contract | 16 history rows, 2 promises; one append per row with the fixed mapping; 201 counted as written |
| TC-P2-E2001-APP-12 | AC22, X11 | Component | efs-history 409 MSG-P1-001; retry every five minutes on a durable timer; at 09:00 hand-over completes without history; late rows appended once when DP05 arrives. The Test Cases v9 row still states the earlier PARTIAL outcome (change requested from the test owner) |
| TC-P2-E2001-APP-13 | AC23, X12 | Component | 503 MSG-P1-022 on the 5th append; 4 written, PARTIAL; the next run counts 4 skipped |
| TC-P2-E2001-APP-14 | AC24 | Component | AceDataReady for EFS and for ALS not COMPLETED; no workflow, no dead letter |
| TC-P2-E2001-APP-03 | AC7 | End to end | AC7 Decision log write fails (legacy RWB-E2-001 AC7) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR.

This story runs TC-E2-001-02, TC-E2-001-04, TC-E2-001-07 and TC-E2-001-08 at Component level against its step with the contract fakes: the repeat, the link, the record failure and the refused second start are this slice's behaviour and are provable with the P1, P3 and P7 answers stubbed. TC-E2-001-01, TC-E2-001-03, TC-E2-001-05 and TC-E2-001-06, and the access test TC-E2-001-09, are cited for the legacy key and belong to the app stories that own their facts — the case and its history (RWB-P3-E2001-APP and RWB-P1-E2001-APP), the held morning (RWB-P1-E2001-APP) and the break (RWB-P1-E2001-APP); RWB-ITG-E2001-ITG copies them with the `-ITG` suffix and proves them across the services. TC-E2-001-10 is cited at NFR level: the blocking half is proved here, because a failed record write leaves the run summary uncommitted and the case-creation fake uncalled, and the 50-account proof is the NFR story's.

### 17. Guardrails

- No business value in code: the threshold, the hold time, the copied action codes and the retry intervals are rows of their owners and values of the environment.
- No personal data in logs, tests, workflow inputs, the run summary or the decision record: the step handles `account_key`, `person_key`, counts and codes, and an EFS history row is held only in the memory of the append activity and is never stored, logged or placed in workflow payloads.
- No read of another service's table and no ACE view: freshness, the EFS history and the append go only through the rwb-source-data contract and the candidates arrive as the `listEligibleAccounts` output; the case only through the rwb-case contract; the parameters and reference data only through their contracts (DP-01, DP-05, DP-11).
- `rwb_integration` holds no foreign key into another schema, no copy of a case, an account or an interaction row, and no grant on `recovery` (ADR-014).
- The step writes no case, no account link, no interaction entry, no `CaseCreated` and no central ledger entry; it asks their owners (BR11).
- The run summary, the run lock and the inbox are the only rows this slice writes, and a failed decision record leaves them uncommitted (DP-03, DP-09).
- No Schedule, no Quartz table and no shared job table: the step is event-started (DP-10).
- The feature flag is read from the platform flag library per environment; no environment value is hard-coded and no secret appears in a value file or a log.
- Every example and fixture is synthetic; no production case, party, account or EFS row is used.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the daily ALS batch and is read through the ACE data path | Program 5.2; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | R-UNI-40 | TC-E2-001-01, TC-E2-001-02, TC-E2-001-04 |
| REQ-CHO-001 | Case with full contact and promise history | Program 5.3; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-04, TC-E2-001-07, TC-E2-001-10 |
| REQ-CHO-005 | Workbench is the system of record for case state after hand-over | Program 5.3; Epic 2 3.2 | FEAT-CHO-04 | 6.1 Take over the case at 90 days past due | R-UNI-39 | TC-E2-001-07, TC-E2-001-08, TC-E2-001-10 |
| REQ-RDF-003 | EFS history transfers to the case | Program 5.1; Epic 2 3.2 | FEAT-CHO-05 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-02, TC-E2-001-03, TC-E2-001-06 |
| ADR-010 | Only rwb-source-data reads the thirty ACE views | Program 5.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | R-UNI-40 | TC-E2-001-01, TC-E2-001-05 |
| ADR-016 | Event-started workflows replace Quartz; no shared job table | Epic 2 3.2 | FEAT-CHO-05 | 6.1 Take over the case at 90 days past due | None | TC-E2-001-03, TC-E2-001-08 |

### 19. Out of scope

- The case creation, the account link, the status, entry date and days past due at entry, and `CaseCreated`: RWB-P3-E2001-APP.
- The EFS history read, the `efs_ledger_outcome` filter, the interaction ledger in `rwb_source_data`: RWB-P1-E2001-APP and the ledger stories of rwb-source-data. The REC-01 result: `ReconciliationWorkflow` of RWB-P1-E1011-APP.
- The central decision ledger and its hash chain: RWB-P7-E2001-APP.
- The freshness stamp per data product and `AceDataReady`: RWB-P1-E1015-APP and the rwb-source-data stories of this legacy key.
- The read-only ACE view contract, its grants and the boundary rule: RWB-P1-E1069-APP.
- JOB-02 `DailyCaseRun`, JOB-03 allocation and JOB-06 rebalancing: rwb-case.
- The administrative rerun operation of JOB-02: rwb-case, path pending (GAP-2258); this story only refuses a second concurrent run. The rwb-source-data job operations serve only rwb-source-data runs (RD-P1-012).
- The contract of the step, its summary shape and its fakes: RWB-P2-E2001-CON.
- The chart, the Flyway step, the topic subscription, the alerts, the dashboards and the runbook: RWB-P2-E2001-OPS.
- The cross-service proof of the whole journey and the boundary check over the nineteen schemas: RWB-ITG-E2001-ITG.
- Any direct read of an ACE view, any read of the interaction, case or reconciliation table, and any same-day hand-over event (DL06).

### Remaining delivery steps

- Settle how the `listEligibleAccounts` output reaches the hand-over step and which service drives case creation, and align RWB-P3-E2001-APP (GAP-3374; solution architect).
- Settle which component applies the `efs_ledger_outcome` action-code filter (GAP-3375; data architect with the solution architect).
- Confirm handover.hold_until (GAP-3286, rwb-integration owner with RW-COE); publish the rwb-case rerun path (GAP-2258) and case-creation path (GAP-0651).
- Publish the efs-history fragment, the provider fake of rwb-source-data 5.1.0 and the ledger append contract at pinned versions (service contract owner).
- Size the story at refinement and obtain epic design sign-off (squad lead, solution architect).
- Add the new test cases in Test Cases v9 and load test data in DEV (test lead).
