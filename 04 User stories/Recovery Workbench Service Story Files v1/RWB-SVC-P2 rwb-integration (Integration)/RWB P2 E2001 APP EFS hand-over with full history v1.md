# RWB-P2-E2001-APP EFS hand-over with full history

SCB Collections and Recovery. Henka Group, 22 November 2026.
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
| Legacy key | RWB-E2-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP18, DP19 |
| Parallel lane | L-P2-A |
| Ready to start | After RWB-P2-E1007-APP |
| Depends on (build) | RWB-P2-E2001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P2-E1007-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P1-E1015-CON |
| Integration dependencies | None |
| External dependencies | RWB-P2-E2001-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-001 for rwb-integration. The legacy story created the case, linked the further account, appended the EFS history and held a stale batch inside one recovery service; this story builds the hand-over step of that journey in rwb-integration — the listener, the group builder, the calls to the owners and the run summary — and leaves case creation and the account link with rwb-case, the EFS history read and the interaction ledger with rwb-source-data, and the central ledger with rwb-decision. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the hand-over step of the morning run to take the ACE hand-over of the business date, group it by customer and product group, ask rwb-case to create or link the case, ask rwb-source-data to append the EFS contact and promise history it holds for the account, and record its own run summary**, so that **the case starts the morning after the account reaches 90 days past due with what happened before day 90, and every run of the step is repeatable, holdable and provable without reading code**.

This story is one of the four app stories of the legacy key. The accepted split, stated by RWB-ITG-E2001-ITG and fixed by the Ownership Map (ASM-1088), is: **RWB-P1-E2001-APP** owns the EFS history read and the interaction ledger append in `rwb_source_data`; **this story** owns `HandoverService`, `HandoverGroupBuilder`, `HandoverSummaryWriter` and `AceDataReadyListener`; **RWB-P3-E2001-APP** owns case creation, the account link and `CaseCreated`; **RWB-P7-E2001-APP** owns the local decision record and the central ledger. JOB-02 stays with rwb-case, while the hand-over step runs here, event-started on `AceDataReady`.

### 2. Business rationale

Accounts move from collections to recovery by a weekly transfer today, and the case starts without its collection history. ACE ingests the ALS hand-over and the EFS action history (D-RCV-35 U1). This story creates the case each morning from the account rows ACE holds for the business date, links a further account of the same customer and product group to the open case, and appends the EFS contact and promise history to the interaction ledger. It holds case creation while the ACE batch for the business date is incomplete, so no case is built from stale data. It meets REQ-CHO-001, REQ-CHO-005, REQ-DRI-013 and REQ-RDF-003 and is measured by CTL-01 and REC-01 (accounts at 90 days past due against open cases, zero unexplained).

The legacy story did all of it inside one deployable: three view reads, two in-process interfaces, a Quartz job and one database. Under D-RCV-60 the same journey is six services and four owners, and this slice is the step that sequences them. That makes the slice's own value precise: it is the only place that decides *which* accounts are taken for a business date, *how* they are grouped, *when* the run must hold, and *what* the run summary says. Every one of those is a decision of the hand-over, not of the case, the ledger or the central log — and each is recorded so that a held morning and a repeated morning are both explainable afterwards.

**What the split changes, and why it changes here.**

- **DP-01.** `rwb_integration` holds no copy of a case, an account, a party or an interaction, and no foreign key into another schema. The step links to them by business key (`account_key`, `person_key`, `caseId`) and reads them only through their owners' contracts.
- **DP-03.** The `DecisionLogWriter` of the monolith becomes the local decision-record library: the run's own decision — run, hold or partial — is written as one record with the legacy decision code "D6 entry", the business date, the freshness answer of DP01 and DP05 and the counts, in `rwb_integration` in the same local transaction as the run summary, and published as `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` for the central ledger in rwb-decision. The case-creation record itself stays rwb-case's, written in its own transaction (RWB-P3-E2001-APP).
- **DP-05.** `AceSourceQuery` and every `v_ace_*` read leave this slice. Only rwb-source-data reads the thirty `recovery.v_ace_*` views (ADR-010; Arch v5 slides 8, 9, 15 and 41; ASM-1089). The candidates, the person keys, the freshness stamps and the EFS rows behind the append come through its contract, one hop, 2 s (DP-11). `rwb_integration` holds no grant on `recovery`.
- **DP-06 and DP-07.** The threshold `case.entry.dpd_threshold` = 90, the hold time `handover.hold_until` = 09:00 and the product code to product group map are parameters and reference data of rwb-case, read through its contracts with the version in force; nothing is a constant in this service.
- **DP-09.** The consumed `AceDataReady` is deduped in the inbox (`processed_event`) on `EV-26:ALS:<businessDate>`; this slice publishes no business event of its own.
- **DP-10.** The legacy `HandoverJob` Quartz trigger becomes an event-started Temporal step on the queue `rwb-integration` in the namespace `rwb-recovery`. JOB-02 itself stays rwb-case's (`DailyCaseRun`, Arch v5 slide 44), and JOB-03 allocation follows it there.
- **DP-18.** The interaction ledger is rwb-source-data's. The step asks for the append; it writes no ledger row and holds no ledger table.
- **DP-19.** The case list, the case timeline and the data-quality view the case owner and the data steward read are gateway-bff composite routes, never a browser call to this service.

**What this slice does not decide.** The status, entry date and days past due at entry of a case, the account link, and `CaseCreated` are rwb-case's. The sixteen EFS entries, their action codes and their `efs_record_key` dedupe are rwb-source-data's. The central ledger entry is rwb-decision's. This story calls each of them once per account and records what came back.

### 3. Preconditions

- RWB-P2-E2001-CON is published: the activity contract of the hand-over step, the `HandoverSummary` shape, the intake of `AceDataReady`, the consumed elements of the P1, P3 and P7 contracts, the error envelope, the idempotency keys and the fakes.
- RWB-P2-E1007-APP is delivered: the integration base of rwb-integration, its controller and client conventions, its problem-response mapping, its Temporal worker and its `rwb_integration` migration sequence.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameter and reference-data client libraries with which this service reads rwb-case's values (DP-06, DP-07).
- RWB-PLT-TE006-CON is published: the outbox and inbox library with `processed_event`, `idempotency_key`, `outbox_event`, `outbox_delivery`, the retry topic and the `.dlt` topic (DP-09).
- RWB-PLT-E1071-CON is published: the workflow kit, the task queue `rwb-integration`, worker versioning and the payload codec (DP-10).
- RWB-PLT-N001-CON is published: the gateway-bff composite routes that serve SCR-02 case list, SCR-04 case timeline and SCR-45 data quality (DP-19).
- RWB-P1-E1015-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: the freshness stamp and `AceDataReady` of rwb-source-data, and the parameter and reference-data contracts of rwb-case. These are contract dependencies and never block the build.
- The ACE batch rows and the synthetic seeds of the legacy story exist in the test environment: account "A-0001" of customer "C-0001", product group "MORTGAGE", at 90 days past due in the ACE data of business date 2026-12-14 with 14 contact rows and 2 promise rows; account "A-0002" of customer "C-0002", product group "SSME", with open case "RW-2026-000210"; account "A-0003" with no customer row; account "A-0004" of the decision-record failure case.
- Parameter `case.entry.dpd_threshold` = 90, parameter `handover.hold_until` = 09:00 and the product code to product group map are loaded by rwb-case and read through its contracts. Their row identifiers in `parameter_value` and `reference_row` are Not specified in the source documents (GAP-0651; ASM-1094).
- Feature `rwb.integration.efs-handover` is on in DEV, SIT and UAT; the switch itself is a feature flag of the platform flag library.
- The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0651; ASM-1087).

### 4. Flow

1. rwb-source-data publishes `AceDataReady` for ALS with business date D on `rwb.source-data.events.v1`, once the ACE batch record for ALS and D is COMPLETE.
2. `AceDataReadyListener`: accepts the message through the inbox on the key `EV-26:ALS:<D>`; a redelivery raises the hit count and starts no second run. Only the ALS source starts this step.
3. `EfsHandoverWorkflow`: starts with workflow ID `efs-handover-<D>`, takes the run lock `handover-run:<D>` in `idempotency_key`, and stops at once with a refusal when the lock is held by another run for D (AC8).
4. `readFreshness`: reads the DP01 Account and arrears stamp and the DP05 Contact and promises stamp at business date D through the rwb-source-data contract; if either is STALE the step holds (step 12) and creates no case.
5. `readParameters`: reads `case.entry.dpd_threshold` (90) and `handover.hold_until` (09:00) through the rwb-case parameter contract, and the product code to product group map through the rwb-case reference-data contract, each with the version in force.
6. `listCandidates`: reads the accounts of business date D at or above the threshold with no open case link, through the rwb-source-data contract, and the person key of each through the same contract. An account whose person key has no customer row is left out and listed for the next run.
7. `HandoverService`: for each candidate calls the inbox key `handover:<account_key>:<D>`; a repeat is skipped and counted in the run summary (AC2).
8. `HandoverGroupBuilder`: groups the remaining accounts by primary `person_key` and product group, using the product map; one group is one case or one link.
9. `createOrLinkCase`: for each group calls the rwb-case case-creation operation once with the group, the business date D, the entry date D+1, the days past due at entry, the total outstanding at entry and the account to be primary. rwb-case writes its own decision record first, then creates the case with status New or links the further accounts to the open case for the person and product group, and publishes `CaseCreated` in its own transaction (AC4; RWB-P3-E2001-APP).
10. rwb-case answers with the case reference, the created-or-linked outcome and the account links; a decision-record failure is answered as a failure for that group and is carried into the run summary with MSG-P7-003 (AC7).
11. `appendEfsHistory`: for a case that is new or was found open, calls the rwb-source-data interaction append once per account with the account key, the business date D and source system EFS; rwb-source-data reads the `v_ace_efs_action` rows of the collection period, keeps the action codes that are in `efs_ledger_outcome`, and appends one entry per `efs_record_key`, returning the written and skipped counts (RWB-P1-E2001-APP).
12. `writeRunSummary`: on a held run, records the held outcome with the stale data product, the stale business date, the count of waiting accounts, MSG-P1-001 for the data product and MSG-P2-007 for the data steward, and names no entry date; on a good run, records the counts (accounts read, cases created, accounts linked, interaction entries appended, repeats, held, gap dates) and the REC-01 result through the rwb-source-data contract.
13. `recordRunDecision`: writes one local decision record with decision code "D6 entry", the business date, the freshness answer of DP01 and DP05, the counts and the outcome, in `rwb_integration`, and the library publishes `DecisionRecorded` on `rwb.decision-record.v1`; the record write and the run summary commit together, and a failed record write fails the run with MSG-P7-003 and an incident.
14. `EfsHandoverWorkflow`: releases the run lock, answers the `HandoverSummary` of §12.5, and ends. A gap business date is carried into the next good run, so a missed morning is named and not silently absorbed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same business date is run twice, or the same `AceDataReady` is redelivered | No second case or link; the repeat is counted in the run summary (R-UNI-40) | None | AC2 |
| X2 | The ACE batch for ALS and business date D is not COMPLETE by 09:00 | The step does not run a good morning: the data products show the stale date, the run holds with the waiting count, the data steward is alerted, and the cases are created on the next good business date | MSG-P1-001, MSG-P2-007 | AC3 (driven; owned by RWB-P1-E2001-APP) |
| X3 | The account's `person_key` has no row in the ACE customer data | The account is not taken; the REC-05 business-key break lists the `account_key` and it is tried with the next run | None | AC5 (driven; owned by RWB-P1-E2001-APP) |
| X4 | The decision record of the case creation fails inside rwb-case | No case is created for that group; an incident is raised; the group is tried in the next run and the run summary carries MSG-P7-003 | MSG-P7-003 | AC7 |
| X5 | The customer already has an open case for the product group | The account is linked to that case; no new case | None | AC4 |
| X6 | The step is started again while it runs for the same business date | The second start is refused: the run lock `handover-run:<D>` is held and the answer is 409 | MSG-P2-006 | AC8 |
| X7 | A role without the right requests the administrative rerun | Refused by the rwb-source-data rerun operation before any step starts; nothing changes | MSG-P4-002 | TC-E2-001-09 |
| X8 | rwb-source-data, rwb-case or rwb-access does not answer inside the 2 s budget | One hop, no retry on a 4xx, retry with jitter on a 5xx; the run ends as partial with the unanswered call named, and the accounts it covered are tried in the next run | MSG-GEN-006 | TC-E2-001-10, the CON contract tests |
| X9 | The run's own decision record cannot be written | The run summary and the record roll back together; the run ends as failed with an incident and no `DecisionRecorded`; the next delivery starts a fresh run | MSG-P7-003 | TC-E2-001-10 |
| X10 | A feature flag `rwb.integration.efs-handover` is off | The listener is not deployed, so no step starts and no case, link or entry is written | None | RWB-P2-E2001-OPS |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published CON story, the six platform contracts and the integration base; the P1, P3 and P7 answers come from their contract fakes |
| Negotiable | The threshold, the hold time, the product map and the copied action codes are rows of their owners; the story fixes only the behaviour of the step |
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

  Scenario: AC2 Repeat run (legacy RWB-E2-001 AC2)
    Given the run for business date 2026-12-14 created the case for "A-0001"
    Given the rwb-case contract mock returns that one case already exists for "A-0001" and holds no open case for its customer and product group
    Given the rwb-source-data contract mock returns 16 interaction entries already appended for that case with source system "EFS"
    When case creation runs again for business date 2026-12-14
    Then the system creates no second case and no interaction entry is added
    Then the run summary shows 1 repeat for "A-0001"

  Scenario: AC4 Account linked to the open case (legacy RWB-E2-001 AC4)
    Given customer "C-0002" has open case "RW-2026-000210" for product group "SSME"
    Given synthetic account "A-0002" of "C-0002", product group "SSME", reaches 90 days past due on 2026-12-14
    Given the rwb-source-data contract mock returns "A-0002" at 90 days past due at business date 2026-12-14 with customer "C-0002" and product group "SSME"
    Given the rwb-case contract mock returns open case "RW-2026-000210" for customer "C-0002" and product group "SSME" and records the account link with linked from 2026-12-15 and is primary false
    When case creation runs
    Then the system creates no new case
    Then the system links "A-0002" to "RW-2026-000210" with linked from 2026-12-15 and is primary false

  Scenario: AC7 Decision log write fails (legacy RWB-E2-001 AC7)
    Given the decision log store is unavailable
    Given the rwb-case contract mock returns the decision-record failure of "A-0004" with no case created for it
    Given the rwb-source-data contract mock returns no interaction entry appended for "A-0004"
    When case creation runs for "A-0004"
    Then the system creates no case for "A-0004"
    Then the system raises an incident and the run summary carries message MSG-P7-003
    Then the system takes "A-0004" in the next run

  Scenario: AC8 Second start refused (legacy RWB-E2-001 AC8)
    Given JOB-02 is running for business date 2026-12-14
    Given the rwb-source-data contract mock returns that the administrative rerun of JOB-02 reaches the hand-over step for business date 2026-12-14
    Given the rwb-integration contract mock returns the run lock held for business date 2026-12-14
    When a platform administrator requests a rerun of JOB-02
    Then the response is 409 with message MSG-P2-006
```

The four criteria are the legacy criteria this slice owns, copied word for word with the origin tag on the scenario line and the legacy Background unchanged. Every cross-service part is replaced by a contract-mock Given so the criterion is provable without the other services; no legacy value is changed and no legacy line is dropped.

**Why these four.** AC2 is the step's own idempotency and its own run summary. AC4 is the step's grouping and its call to the case-creation contract, since the decision "this account belongs to the customer's open case for the product group" is taken here from the person key and the product map before rwb-case writes the link. AC7 is the step's blocking rule: the run stops for that group and the run summary carries MSG-P7-003, which is this slice's output. AC8 is the step's refusal: P1's rerun operation is the door, and the run lock of this step is what answers 409.

AC1 (case from the ACE data), AC3 (late ACE batch), AC5 (customer not in the ACE customer data) and AC6 (cases created on the next good batch) stay with the app stories of this legacy key that own the facts they assert, and RWB-ITG-E2001-ITG proves them across the services. The inputs this step hands over — the candidate set, the grouping, the counts — are asserted here at Component level through the fakes of those criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case enters at 90 days past due | DL16; parameter case.entry.dpd_threshold |
| BR2 | One case per customer per product group; a further account of the same customer and product group is linked to the open case | DL17; REQ-CHO-005 |
| BR3 | The hand-over set is read for the ACE business date; the Workbench loads no source file | D-RCV-35 U1; ADR-010; REQ-DRI-013 |
| BR4 | No case is created from a business date whose ACE batch is not COMPLETE | JOB-02; CTL-02; FEAT-CHO-05 |
| BR5 | The EFS contact and promise history of the collection period is appended to the interaction ledger with source system EFS, one entry per `efs_record_key` | DL29; LOV-SOURCE; REQ-CHO-001; R-UNI-40 |
| BR6 | A repeat hand-over for the same account and business date is ignored and counted | R-UNI-40 |
| BR7 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR8 | An account whose `person_key` has no customer row is held on the REC-05 business-key break and tried with the next run | REC-05; DQ-040; D-RCV-35 U2 |
| BR9 | Only rwb-source-data reads the thirty `recovery.v_ace_*` views; this step reads the candidates, the person keys, the freshness stamps and the EFS history only through its contract, one hop, with a 2 s budget | ADR-010; DP-05; DP-11; Arch v5 slides 8, 9, 15 and 41 |
| BR10 | The hand-over is an event-started Temporal step on `AceDataReady`, not a Quartz job and not JOB-02; no shared job table and no Schedule is used, and JOB-02 stays with rwb-case | DP-10; ADR-016; Arch v5 slide 44 |
| BR11 | The case, the account link, `CaseCreated` and the case-creation decision record are written only by rwb-case; the interaction entries and the EFS outcome list only by rwb-source-data; the central ledger only by rwb-decision. This story asks and never writes | Arch v5 slide 41; DP-01; DP-18 |
| BR12 | The run summary has no table of this service: the counts are the activity result, one local decision record with decision code "D6 entry" and the REC-01 row written through the rwb-source-data contract | DP-01; DP-03; legacy section 12 |
| BR13 | The step is reached only through gateway-bff composite routes for SCR-02, SCR-04 and SCR-45, never directly from the browser | DP-19 |

BR1 to BR8 are the legacy rules with their sources. BR9 to BR13 are the realignment rules this slice must obey; each one is forced by the ownership of the facts the legacy story held in one database.

### 9. State transitions

The two case transitions of the legacy story are rwb-case's: a case enters at New when `CaseCreated` is written with days past due at or above 90 and no open case for the customer and product group, and an account linked to an open case leaves the case status unchanged. This story causes both through the case-creation contract and changes neither.

The state this slice owns is the run:

| From | Event | Condition | To |
|---|---|---|---|
| Not started | `AceDataReady` for ALS accepted by the inbox | The event key is new and the flag is on | Started |
| Started | Run lock taken | No other run holds `handover-run:<D>` | Running |
| Running | DP01 or DP05 STALE at D | The hold time has not passed | Held |
| Running | Every group answered | The groups are created or linked and the EFS appends answered | Completed |
| Running | A group fails on the decision record | rwb-case answers the record failure | Partial, with an incident and MSG-P7-003 |
| Held | The next good `AceDataReady` | The next business date is COMPLETE and fresh | Started, with the gap date carried |
| Completed, Partial or Held | Run lock released | The run summary and its record are committed | Not started, for the next business date |
| Started | The lock is already held for D | A second start arrives | Refused, 409 with MSG-P2-006 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-integration service identity, the hand-over step | Reads the P1 contract, the rwb-case parameters and reference data and the rwb-access session check; calls the case-creation contract and the EFS append; writes its own inbox, run lock, run summary and local decision record (Case record, C; Treatment and offer, none) |
| SY-CASEWF, case workflow module | Creates the case and the account link, writes the case-creation decision record and publishes `CaseCreated` (Case record, CU) |
| SY-DECLOG, decision log writer | Writes the local decision record of the run and, through the library, publishes `DecisionRecorded`; rwb-decision seals the central ledger (Decision log, C) |
| RW-CASEOWN, case owner | Reads the case and its history once allocated (Case record, R) |
| RW-DATASTEW, data steward | Receives the held-run alert and reads the run summary and the REC-05 break (Platform administration, R) |
| RW-PLATADM, platform administrator | Requests the administrative rerun of JOB-02 through the rwb-source-data operation (Platform administration, U) |
| The platform flag library | Owns the `rwb.integration.efs-handover` flag and its per-environment value |

The service runs as the rwb-integration login (DP-02), carried as a secret reference and never as a literal. The login name is Not specified in the source documents (GAP-0651; ASM-1087).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 | v_ace_account, through the rwb-source-data contract | account_key | Read |
| DF-ACE-008 | v_ace_account, through the rwb-source-data contract | product_key | Read |
| DF-ACE-018 | v_ace_account, through the rwb-source-data contract | days_past_due | Read |
| DF-ACE-020 | v_ace_account, through the rwb-source-data contract | total_balance | Read |
| DF-ACE-036 | v_ace_account, through the rwb-source-data contract | data_as_of | Read |
| DF-ACE-056 | v_ace_customer, through the rwb-source-data contract | person_key | Read |
| DF-ACE-108 | v_ace_efs_action, through the rwb-source-data contract | efs_record_key | Requested here; read and kept by rwb-source-data (P1 story) |
| DF-ACE-111 | v_ace_efs_action, through the rwb-source-data contract | action_code | Requested here; read and filtered by rwb-source-data (P1 story) |
| DF-ACE-114 | v_ace_efs_action, through the rwb-source-data contract | contact_at | Requested here; read by rwb-source-data (P1 story) |
| DF-ACE-119 | v_ace_efs_action, through the rwb-source-data contract | is_ptp | Requested here; read by rwb-source-data (P1 story) |
| DF-ACE-122 | v_ace_efs_action, through the rwb-source-data contract | promise_date | Requested here; read by rwb-source-data (P1 story) |
| DF-ACE-123 | v_ace_efs_action, through the rwb-source-data contract | promise_amount | Requested here; read by rwb-source-data (P1 story) |
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
| DF-OPS-118 to DF-OPS-129 | reconciliation_result, through the rwb-source-data contract | All fields of the REC-01 result of the run | Requested here; written by rwb-source-data (P1 story) |
| DF-OPS-178 to DF-OPS-183 | processed_event (library table in `rwb_integration`) | All fields of the inbox record: consumer, key, CloudEvents id, hit count, last seen | Write |

Field IDs are those in the Logical Data Model and Data Dictionary v8. `rwb_integration` holds no ACE row, no case row, no interaction row and no reconciliation row: the service links by business key (`account_key`, `person_key`, `caseId`) and holds no foreign key into another schema (DP-01, BR11). The only rows this story writes are the inbox, the run lock and stored keys, the run's own outbox rows through the library, and the run decision record.

**Run summary element.** One object per run, and no table of its own (ASM-1091):

| Element | Content |
|---|---|
| businessDate | The ACE business date of the run, D |
| outcome | `COMPLETED`, `HELD` or `PARTIAL` |
| accountsRead | The candidate rows returned at or above the threshold and below the open-case filter |
| groupsBuilt | The groups of the run, by person and product group |
| casesCreated | The groups rwb-case answered as created |
| accountsLinked | The accounts rwb-case answered as linked to an open case |
| interactionEntriesWritten, interactionEntriesSkipped | The counts the EFS append answered |
| repeats | The accounts skipped by the inbox key, one repeat per account and business date |
| held | The stale data product, its business date and the waiting account count |
| gapDates | The business dates skipped since the last good run |
| failures | One row per group that failed, with the message id |

### 12. Contract

#### 12.1 REST operations provided

None. The hand-over step is started by an event and answers an activity, not a REST call; this slice adds no path to the base `/api/recovery/integration/v1`. The recorded run of the step is read on the integration base's existing `GET /api/recovery/integration/v1/admin/scheduled-jobs` of RWB-P2-E1007-APP, which is the baseline's operation over `job_catalog`; this story adds no row to that catalogue because the step is not a Schedule, and it provides no summary endpoint, because the summary is the activity result, the local decision record and the REC-01 row (ASM-1091, ASM-1096). The activity contract itself is declared in RWB-P2-E2001-CON.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | rwb-source-data (P1) | The DP01 and DP05 stamps at business date D, fresh or stale (AC2, AC4) | One hop, 2 s (DP-11) |
| GET | The eligible-account read of the rwb-source-data contract (legacy `AccountQuery.findAtOrAboveDpd`) | rwb-source-data (P1) | The accounts of business date D at or above the threshold with no open case link | One hop, 2 s (DP-11) |
| GET | The customer read of the rwb-source-data contract | rwb-source-data (P1) | The `person_key` and the customer of each candidate, and the absence of a row for a candidate (AC4) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | rwb-source-data (P1) | The EFS history append for one account, source system EFS, idempotent on `efs_record_key`; answers written and skipped counts (AC2, AC4) | One hop, 2 s (DP-11) |
| POST | The reconciliation-result write of the rwb-source-data contract | rwb-source-data (P1) | The REC-01 result of the run: business date, counts and the unexplained difference (BR12) | One hop, 2 s (DP-11) |
| POST | The case-creation operation of the rwb-case contract (legacy `CaseCreation.createOrLink`) | rwb-case (P3) | Creates the case with status New and entry date D+1, or links the further accounts to the open case for the person and product group; answers the case reference, the created-or-linked outcome and the links (AC2, AC4, AC7) | One hop, 2 s (DP-11) |
| GET | The parameter read of the rwb-case contract | rwb-case (P3) | `case.entry.dpd_threshold` = 90 and `handover.hold_until` = 09:00, with the version in force (DP-06) | One hop, 2 s (DP-11) |
| GET | The reference-data read of the rwb-case contract | rwb-case (P3) | The product code to product group map, with the version in force (DP-07) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | rwb-source-data (P1) | The administrative rerun of JOB-02 that reaches this step; the step refuses a second concurrent run for the business date and answers 409 (AC8). This service calls nothing here; the row fixes the seam the refusal depends on | One hop, 2 s (DP-11) |

The eligible-account read, the customer read and the reconciliation-result write are named by their legacy Java interfaces only. Their paths, query parameters and JSON field names are Not specified in the source documents (GAP-0651; ASM-1090); the two paths that a source does give are used as published. The case-creation operation is named by its legacy interface `CaseCreation.createOrLink`; the Ownership Map publishes no create path for rwb-case, so its path is Not specified in the source documents (GAP-0651; ASM-1090). No call chains: every row is one hop to the owner's `/api/recovery/<short>/v1` base with a 2 s budget and no retry on a 4xx.

#### 12.3 Events published

None on `rwb.integration.events.v1` by this story's own work: `FileDelivered` and `FileFailed` are the outbound-file events of the integration base, RWB-P2-E1007-APP. The local decision-record library publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` from the same transaction as the run summary, with decision code "D6 entry", the business date, the freshness answer and the counts (DP-03, H RWB-PLT-E1027-CON; ASM-1092). `rwb.case.CaseCreated.v1` is published by rwb-case, not here.

#### 12.4 Events consumed

| Event type | Topic | Owner | Use |
|---|---|---|---|
| rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | P1 rwb-source-data | Starts the step for ALS and the business date D, once per key `EV-26:ALS:<D>`; the legacy EV-26 of the story |

The message is accepted through the inbox `processed_event` on the key `EV-26:ALS:<businessDate>`; a duplicate raises the hit count and starts no run (R-UNI-40, AC2). A message that fails the CloudEvents envelope, carries no business date or names a source other than ALS is routed to `.dlt` with an alert and starts nothing (DP-09). The payload is rwb-source-data's and this story reads only the source, the business date and the batch state.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| EfsHandoverWorkflow | Workflow, one execution per business date, workflow ID `efs-handover-<businessDate>` | `rwb-integration` | Input: business date, source ALS, the CloudEvents id. Output: the `HandoverSummary` of §11 |
| acceptAceDataReady | Activity | `rwb-integration` | Input: the event envelope. Output: accepted or repeat, with the inbox key; the listener's record of the intake |
| readFreshness | Activity | `rwb-integration` | Input: business date. Output: the DP01 and DP05 stamp answers, fresh or stale |
| listCandidates | Activity | `rwb-integration` | Input: business date, threshold. Output: the candidate rows and the excluded count, with no customer row |
| buildGroups | Activity | `rwb-integration` | Input: the candidates and the product map. Output: the groups by person key and product group |
| createOrLinkCase | Activity | `rwb-integration` | Input: one group. Output: the case reference, the created-or-linked outcome and the links; a record failure is a non-retryable class |
| appendEfsHistory | Activity | `rwb-integration` | Input: case id, account key, business date. Output: the written and skipped counts |
| writeRunSummary | Activity | `rwb-integration` | Input: the counts and the outcome. Output: the REC-01 row answered by rwb-source-data and the summary of §11 |
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

No business table is added. `interface_config`, `outbound_item` and `job_catalog` stay the integration base's and this story writes no row in them; `job_catalog` holds no run of an event-started step (ASM-1091). `interaction`, `efs_ledger_outcome` and `reconciliation_result` are rwb-source-data's in `rwb_source_data`; `recovery_case` and `case_account` are rwb-case's in `rwb_case`; `decision_log_entry` is rwb-decision's in `rwb_decision` (DP-01, DP-18; BR11).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 contract | `GET /data-products/freshness` fresh at 2026-12-14 and stale for DP05 at 2026-12-15; the eligible-account read returning "A-0001" to "A-0004" and the excluded "A-0003"; the customer read with and without a row; `POST /cases/{caseId}/interactions` answering 16 written and 0 skipped, then 0 written and 16 skipped; the reconciliation write; the rerun operation answering 409 with MSG-P2-006 while the step holds the lock |
| rwb-case WireMock | The P3 contract and its parameters and reference data | The case-creation operation answering created, then linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false, then the decision-record failure of AC7; the parameter read returning 90 and 09:00; the reference-data read returning the product map |
| rwb-decision WireMock | The P7 contract | The central ledger read showing one entry for the run and none for the failed group (AC7) |
| Decision-record library stub | RWB-PLT-E1027-CON | A committed record and its outbox row, and the unavailable-store case that must leave the run summary uncommitted (X9) |
| rwb-access WireMock | The P4 contract | The session check that grants the step its service rights and refuses the rerun to a role without Platform administration U (TC-E2-001-09) |
| gateway-bff composite route stub | The edge route of RWB-PLT-N001-CON | The SCR-02, SCR-04 and SCR-45 routes that read the case, the timeline and the data-quality view; this story registers no screen (DP-19) |

The fakes are published from the owning services' OpenAPI documents and are versioned with the CON baseline.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 9 consumed | Freshness, candidates, customer, EFS append, reconciliation write and the rerun seam on P1; case creation, parameters and reference data on P3; one hop each, 2 s timeout, GET retried once with jitter |
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
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract; this service has no view of its own | none |
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
| HandoverService | Service | The freshness hold, the candidate set, the per-account key, the calls to rwb-case and rwb-source-data, the counts and the outcome |
| HandoverGroupBuilder | Service | Groups the candidates by primary `person_key` and product group with the product map; one group is one case or one link |
| HandoverSummaryWriter | Service | Builds the `HandoverSummary`, asks rwb-source-data for the REC-01 row and hands the summary to the decision record |
| RunLock | Service | Takes and releases `handover-run:<D>` in `idempotency_key`; a held lock refuses the second start with 409 |
| SourceDataClient | Client | Freshness, candidates, customers, the EFS append and the reconciliation write on the P1 contract (DP-05) |
| CaseContractClient | Client | The case-creation operation and the account links on the P3 contract; a record failure is a non-retryable class |
| ParameterClient, ReferenceDataClient | Client | The threshold, the hold time and the product map through the client libraries (DP-06, DP-07) |
| DecisionRecordWriter | Library client | Writes the run record with decision code "D6 entry" in the same local transaction as the run summary; a failure fails the run (DP-03) |

**Database and migrations.** One migration in the rwb-integration sequence, `V2001_1__handover_library_tables.sql`: it includes the library objects `processed_event`, `idempotency_key`, `decision_record`, `outbox_event` and `outbox_delivery` in `rwb_integration` and adds the partial index on `processed_event (consumer, idempotency_key)` and on `idempotency_key (endpoint, idempotency_key)` that the intake and the run lock use (DP-09, DP-15). No business table, no column on `interface_config`, `outbound_item` or `job_catalog`, and no foreign key into another schema.

**Configuration and reference data.**

- `case.entry.dpd_threshold` = 90 and `handover.hold_until` = 09:00 are parameters of rwb-case, read through its contract with the version in force; neither is a constant, a value file entry or a default in code.
- The product code to product group map is reference data of rwb-case, read through its contract with the version in force.
- The EFS action codes copied at hand-over are rows of `efs_ledger_outcome` in `rwb_source_data`, applied by rwb-source-data inside its append; this service names none of them.
- The feature flag `rwb.integration.efs-handover` keeps the legacy name as the reference and is a flag of the platform library; off means no listener, so no step starts.

**Build steps**

1. `AceDataReadyListener` and the inbox key `EV-26:ALS:<D>`, with a duplicate and a malformed-envelope test (AC2).
2. `EfsHandoverWorkflow` and `RunLock`, with the refused second start of AC8 and the replay of a redelivered event.
3. `readFreshness` and the hold decision, with a fresh and a stale answer per data product.
4. `SourceDataClient` over the P1 contract for the candidates, the customers and the append, one test per answer class.
5. `HandoverGroupBuilder` with one and two accounts per customer and product group, and an account with no customer row.
6. `CaseContractClient` over the P3 contract: created, linked to "RW-2026-000210" with linked from 2026-12-15 and is primary false, and the record failure of AC7.
7. `HandoverSummaryWriter` for the completed, held and partial outcomes, with the repeat count of AC2 and the gap dates.
8. `DecisionRecordWriter` with decision code "D6 entry", the freshness answer and the counts, and the rollback path of X9.
9. The contract-fake run of every cross-service answer in isolation, so the story builds before rwb-source-data, rwb-case and rwb-decision are built.
10. The metrics and the run-summary series the operations story of this legacy key deploys: accounts read, cases created, accounts linked, repeats, held, gap dates.

**Done when.** The tests in section 16 pass, the step is started once per business date from `AceDataReady`, AC2, AC4, AC7 and AC8 are green against the fakes, the run writes one local decision record and one REC-01 row, `rwb_integration` holds no foreign key into another schema and no grant on `recovery`, and the contract tests of RWB-P2-E2001-CON and RWB-PLT-E1027-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product is stale at the business date of the run | {product} is from {date}. Today's data is not yet complete. |
| MSG-P2-007 | Case creation is held for an incomplete ACE batch | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-P7-003 | The decision record of a group or of the run cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-006 | A second start or rerun while the step runs the business date | {job} is already running. Wait until it ends before you run it again. |
| MSG-P4-002 | A role without the right requests the rerun | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A source contract did not answer inside the budget | {source} could not be read. Try again in a few minutes. |

MSG-P1-001 uses the wording of FSD P2 Integration v3 (the legacy story carries an older wording of the same message); the divergence is recorded and not repaired here (GAP-0651; ASM-1093). Every other text is the legacy text unchanged. An alert and a run record carry counts, business dates, data product codes and message ids only, never an account holder, a contact point or an amount.

### 15. Screens and states

No new screen. The step builds no page and renders nothing:

| Screen | State | What the case owner or the data steward sees |
|---|---|---|
| SCR-02 Case list | Loading, list | The case of the morning appears with status New and entry date D+1 once rwb-case has answered; a held morning adds none. Read through the gateway-bff composite route |
| SCR-04 Case timeline | Loading, filtered | The EFS history of the case with source system EFS, appended by rwb-source-data on the step's request. Read through the composite route |
| SCR-45 Data quality | Held run | The stale data product with MSG-P1-001, the waiting count with MSG-P2-007 and the REC-05 break. Read through the composite route |

The screen values are the owners': the case list and the timeline are rwb-case's reads over the rwb-source-data ledger, and the data-quality view is rwb-source-data's. This story supplies the held-run and repeat counts that the composite route merges into SCR-45 (DP-19). The route paths, the merge order and the field-level masking are Not specified in the source documents (GAP-0651; ASM-1087).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-001-09 | Access | Component | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |
| TC-E2-001-01 | AC1, BR1, BR3, BR5 | End to end | Synthetic account A-0001 with 14 contact rows and 2 promise rows in v_ace_efs_action |
| TC-E2-001-02 | AC2, BR6 | End to end | Same business date run twice |
| TC-E2-001-03 | AC3, BR4 | End to end | ACE batch for ALS of 2026-12-15 not COMPLETE |
| TC-E2-001-04 | AC4, BR2 | End to end | Customer C-0002 with an open SSME case |
| TC-E2-001-05 | AC5, BR8 | End to end | Account A-0003 with no row in v_ace_customer |
| TC-E2-001-06 | AC6, BR4 | End to end | Good batch on 2026-12-17 after a missed day |
| TC-E2-001-07 | AC7, BR7 | End to end | Decision log store stopped |
| TC-E2-001-08 | AC8 | End to end | JOB-02 running |
| TC-E2-001-10 | Principle 5 | NFR | Decision log write forced to fail during a run of 50 synthetic accounts; no case is created without its entry |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR.

This story runs TC-E2-001-02, TC-E2-001-04, TC-E2-001-07 and TC-E2-001-08 at Component level against its step with the contract fakes: the repeat, the link, the record failure and the refused second start are this slice's behaviour and are provable with the P1, P3 and P7 answers stubbed. TC-E2-001-01, TC-E2-001-03, TC-E2-001-05 and TC-E2-001-06, and the access test TC-E2-001-09, are cited for the legacy key and belong to the app stories that own their facts — the case and its history (RWB-P3-E2001-APP and RWB-P1-E2001-APP), the held morning (RWB-P1-E2001-APP) and the break (RWB-P1-E2001-APP); RWB-ITG-E2001-ITG copies them with the `-ITG` suffix and proves them across the services. TC-E2-001-10 is cited at NFR level: the blocking half is proved here, because a failed record write leaves the run summary uncommitted and the case-creation fake uncalled, and the 50-account proof is the NFR story's.

### 17. Guardrails

- No business value in code: the threshold, the hold time, the product map, the copied action codes and the retry intervals are rows of their owners and values of the environment.
- No personal data in logs, tests, workflow inputs, the run summary or the decision record: the step handles `account_key`, `person_key`, counts and codes, and the EFS history stays in rwb-source-data.
- No read of another service's table and no ACE view: candidates, customers, freshness, the EFS history and the REC-01 row come only through the rwb-source-data contract; the case only through the rwb-case contract; the parameters and the product map only through their contracts (DP-01, DP-05, DP-11).
- `rwb_integration` holds no foreign key into another schema, no copy of a case, an account, an interaction or a reconciliation row, and no grant on `recovery` (ADR-014).
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
- The EFS history read, the `efs_ledger_outcome` filter, the interaction entries and the REC-01 row in `rwb_source_data`: RWB-P1-E2001-APP.
- The central decision ledger and its hash chain: RWB-P7-E2001-APP.
- The freshness stamp per data product and `AceDataReady`: RWB-P1-E1015-APP and the rwb-source-data stories of this legacy key.
- The read-only ACE view contract, its grants and the boundary rule: RWB-P1-E1069-APP.
- JOB-02 `DailyCaseRun`, JOB-03 allocation and JOB-06 rebalancing: rwb-case.
- The administrative rerun operation `POST /admin/jobs/{jobId}/rerun`: rwb-source-data; this story only refuses a second concurrent run.
- The contract of the step, its summary shape and its fakes: RWB-P2-E2001-CON.
- The chart, the Flyway step, the topic subscription, the alerts, the dashboards and the runbook: RWB-P2-E2001-OPS.
- The cross-service proof of the whole journey and the boundary check over the nineteen schemas: RWB-ITG-E2001-ITG.
- Any direct read of an ACE view, any read of the interaction, case or reconciliation table, and any same-day hand-over event (DL06).
