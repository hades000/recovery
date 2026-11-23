# RWB-P3-E2009-APP Steering dashboard v1 data set

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2009-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P3-AC |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P9-E2009-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-017, FR-P3-018, FR-P3-040) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-009 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **Tribe lead (RW-TRIBE)**, I want **the case facts that the steering dashboard counts — every open case with its product group, status, stage, route, queue and entry date, read at the 2026-12-15 cut-off from rwb_case, filterable by product group and reconcilable to the case list the teams work from, with the decision count of the day taken from the decision log and never from a copy**, so that **the steering committee reads the same numbers the teams work with**.

### 2. Business rationale

The steering committee receives numbers counted by hand that differ from what the teams see in their queues. The dashboard measures are computed in rwb-reporting (P9) from the facts the owning services publish: cases by stage, queue and age, decisions logged, treatments, letters sent and agent acceptance. This story delivers the rwb-case half — the case fact at a cut-off, the case list count it is compared with, and the product filter — on top of the case and queue rows that rwb-case already owns, and it removes the INT-19 extract: there is no data lake, so the facts reach rwb-reporting through the case events the service already publishes (DP-17).

The reconciliation is the control: the sum of the stage facts for a business date must equal the open case count of the case list at the same cut-off, with tolerance zero, or the publish is held by the P9 measure run. The decision count is the number of decision log entries decided that day, read from the decision log and never from a separate count (NFR-065). It serves REQ-WKM-009 and REQ-WKM-006 and the controls BR2, BR3 and BR7.

### 3. Preconditions

- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), so every case state change this story counts has its decision record on the same topic rwb-reporting projects.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case and its client library (DP-07). The product group, stage and queue values are read as data with the version in force; no Java enum of them exists.
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions in schema `rwb_case` (DP-15).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery` (DP-10). The kit is used by the 01:30 measure run in rwb-reporting, not by this read.
- RWB-PLT-N001-CON is published: the gateway-bff composite route behind which SCR-02 Case list and SCR-37 Steering dashboard are served (DP-19). The route detail for SCR-37 is Not specified in the source documents (GAP-0731; ASM-1292).
- RWB-P9-E2009-CON is published: the measure, snapshot and publish contract of rwb-reporting, with its fake. It is a contract dependency and does not block the build.
- The case CON story RWB-P3-E1018-CON published the case resource and the six `rwb.case.events.v1` event schemas. This story adds no event type and no payload field; it fixes the fact dimensions that are already on the case events.
- The synthetic day 2026-12-15 exists in `rwb_case`: 240 open cases, 1,412 decision log entries decided that day, 38 treatments and 95 notices sent. The 2026-12-15 cut-off of the case list is 06:52 (FSD P3 v4 A2.18).
- The reader holds a role with Case record R and a scope, or reads only the teams and products in their scope.
- The login is the rwb-case login: Not specified in the source documents (GAP-0731; ASM-1291).

### 4. Flow

1. rwb-case: a case is created, allocated, transferred or moved to a new stage on business date 2026-12-15. In one `rwb_case` transaction the service writes the case row, the stage or queue change and the case event to its outbox (DP-01).
2. The case event carries the fact dimensions the dashboard groups by: `caseId`, `caseNo`, `productGroup`, `status`, `stageCode`, `routeCode`, `queueId` and `entryDate`. No personal data travels with it.
3. rwb-reporting (P9): consumes `rwb.case.events.v1` into its case-fact projection, keyed by `caseId`, for the measure run that follows (DP-17). There is no data lake and no INT-19 extract in the target.
4. The 2026-12-15 cut-off for the case list is 06:52. A case that changes after the cut-off belongs to the next day's facts and does not change the facts of 2026-12-15.
5. The data steward or the reconciliation step reads the open case count at the cut-off from `GET /api/recovery/case/v1/cases` with the cut-off date 2026-12-15: 240 open cases with their fact rows.
6. gateway-bff: checks the session and calls rwb-case, one hop and 2 s timeout (DP-11, DP-13). rwb-case calls the rwb-access authorise contract (cached) for Case record R, applies the caller's scope, and returns the rows.
7. The same read with `productGroup=MORTGAGE` returns the 140 Mortgage rows of the day, and the count with them.
8. rwb-reporting: at 01:30 on 2026-12-16 the measure run computes `CASES_BY_STAGE` for 2026-12-15 from its case-fact projection; the sum of the stage rows is 240, equal to the case list count at the 06:52 cut-off.
9. The measure run reads the decision count of the day from the decision log (1,412 entries decided on 2026-12-15) and writes `DECISIONS_LOGGED`; no separate count is kept, and rwb-case holds no copy of the decision rows.
10. Where the two case totals differ (239 against 240), the reconciliation names both counts and the business date. The publish hold, the SCR-37 display and the alert are the P9 slice of this legacy key; the ITG slice proves the wired behaviour end to end.
11. The reader sees the same numbers on SCR-02 Case list (owner rwb-case) and on SCR-37 Steering dashboard (owner rwb-reporting), each with its business date.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fact-bearing state change commits after the 2026-12-15 cut-off | The facts of 2026-12-15 do not change; the change belongs to the facts of the next business date | None | AC2 |
| X2 | The sum of the stage facts differs from the case list count at the cut-off | Both counts are returned with the business date; the publish hold, the previous day and the alert are raised by the P9 measure run | MSG-P9-002 | AC4 |
| X3 | The read asks for a business date with no open case in scope | The read returns an empty page with count 0 and the list shows the empty state; no zero is written as a measure by rwb-case | None | AC2, AC8 |
| X4 | The caller's scope excludes a product group | Rows outside the scope are absent and the count is the count in scope; nothing outside the scope is returned | None | AC8 |
| X5 | A role without Case record R reads the facts | Refused with 403 by the rwb-access authorise check behind the endpoint | MSG-P4-002 | TC-E2-009-10 |
| X6 | rwb-access does not answer inside the REST budget | One hop, 2 s timeout (DP-11); the read is refused and is never served unscoped | None | TC-E2-009-10 |
| X7 | A source product of the measure set is stale on 2026-12-15 | The previous day is shown with its date; carried by the P9 slice (AC5) | MSG-P1-001 | AC5 |

AC1 (refresh), AC3 and AC7 (agent rates), AC5 (stale source), AC6 (dates in the wrong order) and AC9 (rerun of a published day) are cited in the flow and this table but are not owned here: AC1, AC5, AC6 and AC9 sit in the P9 slice of this legacy key and AC3 and AC7 in the agent slice. The three criteria in section 7 are the ones this story owns.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the platform contract stories and the P9 CON. The authorise answer and the decision count come from their contract fakes |
| Negotiable | The fact fields are reference-data values with a version; the story fixes the behaviour, not the numbers |
| Valuable | One set of case facts for the committee and the teams, from the service that owns the cases |
| Estimable | One read, one product filter, one count, one index and one contract fake set |
| Small | Fits in one week with its tests |
| Testable | Every owned criterion runs against the synthetic day of 2026-12-15 with known answers; every cross-service answer is stubbed in a contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Steering dashboard v1 data set

  Background:
    Given definition version "MD-2026.12" is in force with measures "CASES_BY_STAGE", "CASES_BY_QUEUE_AGE", "DECISIONS_LOGGED", "TREATMENTS", "LETTERS_SENT", "AGENT_ACCEPTANCE" and "AGENT_OVERRIDE"
    Given the synthetic day 2026-12-15 holds 240 open cases, 1,412 decision log entries, 38 treatments and 95 notices sent

  Scenario: AC2 Reconciles (legacy RWB-E2-009 AC2)
    Given the case list shows 240 open cases at the 2026-12-15 cut-off
    Given the rwb-decision contract mock returns 1,412 decision log entries decided on 2026-12-15
    When JOB-15 runs at 01:30 on 2026-12-16
    Then the sum of "CASES_BY_STAGE" for 2026-12-15 is 240
    Then "DECISIONS_LOGGED" for 2026-12-15 is 1,412, the count of decision log entries decided that day

  Scenario: AC4 Counts do not match (legacy RWB-E2-009 AC4)
    Given the case list shows 240 open cases at the 2026-12-15 cut-off
    Given the case facts read for the dashboard total 239
    Given the rwb-reporting contract mock returns no published snapshot for 2026-12-15 and the latest published day 2026-12-14
    When JOB-15 runs at 01:30 on 2026-12-16
    Then no snapshot rows and no extract are published for 2026-12-15
    Then SCR-37 shows 2026-12-14 as the latest day with MSG-P9-002 naming 239, 240 and 2026-12-15
    Then an alert goes to the Reporting and BI analyst and the data steward

  Scenario: AC8 Filter by product (legacy RWB-E2-009 AC8)
    Given the measures for 2026-12-15 are published and the case list shows 140 open Mortgage cases at the cut-off
    Given the rwb-reporting contract mock returns the published measures for 2026-12-15
    When a product head sends GET /reports/measures?measure=CASES_BY_STAGE&product=MORTGAGE&from=2026-12-15&to=2026-12-15
    Then the response holds only rows with product "MORTGAGE"
    Then their sum is 140
```

In this slice AC8 is exercised through the case-fact read `GET /api/recovery/case/v1/cases?cutOffDate=2026-12-15&productGroup=MORTGAGE`, whose 140 rows are the ones the P9 measure rows for "MORTGAGE" are checked against; the measures endpoint, the Power BI extract and the published measure rows are the P9 slice. In AC4 this slice owns the two counts and their difference; the hold, the SCR-37 message, the extract and the alert are the P9 slice. The measure codes and `JOB-15` are written as the legacy story has them; the transport that carries the facts and the decision count to the 01:30 run is read in ASM-1294.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Steering measures are computed from Workbench records and the decision log, never from a separate count | NFR-065; REQ-WKM-009 |
| BR2 | The dashboard case count equals the case list count at the same cut-off, or the publish is held | REQ-WKM-006; DL25 (tolerance zero) |
| BR3 | Agent acceptance is accepted recommendations over all recommendations, and override is overridden over all, per agent and version | NFR-066; DF-DEC-007, DF-DEC-013 |
| BR4 | A measure is shown with its business date and freshness stamp; stale data shows its date | MSG-P1-001 rule; FEAT-RPT-08 |
| BR5 | Each value is shown beside the frozen baseline of 2026-11-27 | REQ-WKM-009; RWB-E1-013 BR2 |
| BR6 | A rate with no runs in the denominator is not computed | NFR-066 |
| BR7 | Every query applies the role's scope | CTL-09 |
| BR8 | A queue snapshot is published only when the depth of each queue equals the case list count for that queue at the same time; a difference holds the snapshot and names the check | FSD P3 v4 A2.18 AC-ALT-P3-018-02 |

BR3 and BR6 are owned by the agent slice; they are listed because the measure set of this legacy key carries them. BR8 is the queue-measure wording of the same control and is written by the queue-measure story, not by this one.

### 9. State transitions

None. This story does not change a case status. It fixes how the case facts of a business date are read at a cut-off and how they reconcile to the case list. The publish status of a business date (published or held) is set by the P9 measure run.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login) | Serves the case facts and the count at the cut-off; reads only schema `rwb_case`; applies the caller's scope |
| rwb-access authorise check | Grants or refuses Case record R and the scope before a read |
| RW-TRIBE, Tribe lead and squad members | Reads SCR-37 and the measures (Reporting R); the screen and the measure set are the P9 slice |
| RW-PRODHEAD, product head | Reads the product-filtered facts and SCR-37 (Reporting R) |
| RW-TEAMMGR, team manager | Reads the facts for the teams in scope (Reporting R) |
| RW-BIANAL, Reporting and BI analyst | Builds the Power BI report; receives the hold alert (Reporting CRUD); the report and the alert are the P9 slice |
| RW-DATASTEW, data steward | Receives the hold alert and reads the reconciliation of the two counts (Reporting CRU) |
| RW-FINANCE, Finance and CFO delegate | Reads SCR-37 (Reporting R); P9 slice |
| RW-REFADM, reference data administrator | Loads the steering definitions and the product, stage and queue reference values (Reference data C) |

The per-service login name is Not specified in the source documents (GAP-0731; ASM-1291); the story names it "the rwb-case login" until it is agreed.

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-008 | recovery_case | route_code | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-REF-181 to DF-REF-184 | reference_row (through the reference-data contract) | product group, stage and queue values in force | Read |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The open case set of a business date is the set of `recovery_case` rows whose `closed_date` is null or later than the cut-off; the fact rows are read at the cut-off and never recomputed afterwards. No source row is copied into `rwb_case` and no column is added for a reporting value.

The decision count of 1,412 is the count of `decision_log_entry` rows decided on the business date (DF-DEC-016 `decided_at`), owned by rwb-decision. rwb-case holds no copy of it: the count reaches the dashboard through the decision-record topic projected in rwb-reporting, and this story's tests stub it with the rwb-decision contract fake.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases` | Case list and case facts at a cut-off: one row per open case with product group, status, stage, route, queue, entry date and closed date, plus the row count; filters `cutOffDate`, `productGroup`, `stage`, `queueId`, `status` | Case record R, scope applied | Not applicable |
| GET | `/queues/{queueId}/cases` | The same case facts for one queue, used for the queue dimension of the dashboard | Queue and allocation R, scope applied | Not applicable |

The case-fact response shape (field names, the ageing band and the dimension codes) and the cut-off rule are Not specified in the source documents (GAP-0731; ASM-1290). Until they are agreed, the read reuses the `GET /cases` resource of the case CON story with the filters above and returns the fields already defined for the case resource: `id`, `caseNo`, `productGroup`, `status`, `stageCode`, `routeCode`, `queueId`, `entryDate`, `closedDate`, and `totalCount`. Errors: 401 no session, 403 no Case record R (MSG-P4-002), 422 a date or filter that cannot be read, 503 store down.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Role, scope and Case record R check before a read (TC-E2-009-10) | One hop, 2 s (DP-11) |

The count of decision log entries is not read by rwb-case: it reaches the dashboard through the decision-record topic that rwb-reporting projects, and this story's tests stub it with the rwb-decision contract fake.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 | caseId | caseId, caseNo, productGroup, status, entryDate, businessDate |
| `rwb.case.CaseAllocated.v1` (EV-02) | `rwb.case.events.v1` | P3 | caseId | caseId, queueId, ownerUserId, stageCode, businessDate |
| `rwb.case.CaseTransferred.v1` (EV-04) | `rwb.case.events.v1` | P3 | caseId | caseId, queueId, fromQueueId, teamCode, businessDate |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | caseId | caseId, status, stageCode, routeCode, queueId, businessDate |

No event type is added and no payload field is renamed: the four types above are the fact carriers of the dashboard, and the story is done only when each one carries the dimensions in the table. Each is written to the outbox in the same transaction as the state change and relayed with the CloudEvents envelope; no personal data is carried.

#### 12.4 Events consumed

None. This story adds no consumer; the case router of rwb-case is owned by the case stories.

#### 12.5 Workflows and activities

None. The case fact is a synchronous read at the cut-off; the 01:30 measure run is a Temporal Schedule in rwb-reporting (P9), not in rwb-case.

#### 12.6 Schedules

None in rwb-case. The legacy JOB-15 schedule becomes a Temporal Schedule on task queue `rwb-reporting` in the P9 slice; rwb-case adds no Schedule and no nightly job.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | Read at the cut-off: case number, product group, status, stage, route, queue, entry date, closed date |
| queue | P3 (rwb_case) | Read for `queue_code` and `team_code` |

No table is added and no column changes. The only database change is one read index for the cut-off query (section 13). `queue_measure` is P3's and is written by the queue-measure story of RWB-E1-030, not here. rwb-case reads no table of another service and holds no foreign key across services (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R and refusing it for a role without the right |
| rwb-decision WireMock | The P7 contract | The decision count fixture of 1,412 entries decided on 2026-12-15 (AC2) |
| rwb-reporting WireMock | The P9 contract behind RWB-P9-E2009-CON | The published measure set for 2026-12-15 and the held day with 2026-12-14 as the latest published day (AC4, AC8) |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | `GET /cases` and `GET /queues/{queueId}/cases` provided; authorise consumed; one hop, 2 s timeout |
| Kafka | 4 published, 0 consumed | `rwb.case.events.v1`: CaseCreated, CaseAllocated, CaseTransferred, CaseStateChanged carry the fact dimensions |
| Temporal | None | No workflow, activity or Schedule in rwb-case for this story |
| File | None | This story reads and writes no file, and there is no data lake extract |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `casefacts`, Java package `th.co.scb.ace.workbench.recovery.case.casefacts`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 applies to the legacy JOB-15 reference only: the schedule becomes a Temporal Schedule in rwb-reporting, and rwb-case adds none. DP-17 applies by removing the INT-19 extract — the case facts leave rwb-case on `rwb.case.events.v1` into rwb-reporting, and this story needs no lake data, so no DP-17 gap is raised. DP-19 applies to the SCR-02 and SCR-37 reads behind the gateway-bff composite route, whose SCR-37 detail is a gap (ASM-1292).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseFactQueryService | Service | Builds the open case set of the cut-off from `recovery_case` and `queue`; applies the product, stage, queue and status filters; returns the rows and the count |
| CaseFactRepository | Repository | Reads `recovery_case` and `queue` in schema `rwb_case` only; no join to another schema |
| CaseFactController | Controller | `GET /cases` and `GET /queues/{queueId}/cases` with the filters, the scope and the count |
| FactDimensionCatalog | Service | Reads the product group, stage and queue values and their version through the reference-data contract; no Java enum of them |
| ScopeFilter | Service | Applies the caller's scope from the rwb-access answer to every fact row and to the count |
| AccessCheckClient | Client | Calls the rwb-access authorise contract (cached) before a read |
| CaseFactEventAssembler | Service | Builds the four case events with the fact dimensions on the existing payloads; no new type and no renamed field |

**Database and migrations**

- No table and no column is added. The facts are read from `recovery_case` and `queue`.
- One migration: `V2009_1__case_fact_read_index.sql` adds the index `ix_case_fact_cutoff ON recovery_case (product_group, queue_id, stage_code, closed_date)`, so the cut-off query of 240 cases and the product filter run inside the screen budget.
- The index is created in schema `rwb_case` through the per-service Flyway sequence (DP-15).

**Configuration and reference data**

- Product group, stage and queue values are read through the reference-data contract of rwb-case with the version in force (DP-07). The product filter of AC8 uses the `LOV-PRODUCT` value `MORTGAGE` as data, never as a constant.
- The 06:52 cut-off of 2026-12-15 and the 01:30 measure run belong to the measure set in rwb-reporting (P9); rwb-case takes the cut-off as a caller parameter.
- The queue-measure dimensions of `queue_measure` (DF-RPT-020 to DF-RPT-030) are Not specified in the source documents (GAP-0731; ASM-1293) and are not written by this story.

**Build steps**

1. CaseFactRepository and CaseFactQueryService over `recovery_case` and `queue`, with the open case set of the cut-off; tests for AC2 at 240 and for the empty set.
2. The product, stage, queue and status filters, with the count returned beside the rows; tests for AC8 at 140 MORTGAGE rows.
3. FactDimensionCatalog over the reference-data contract, so the filter values are data with a version; test the refusal when no version is in force.
4. CaseFactController with the access check, the scope filter and the two paths; test TC-E2-009-10 for the refusal with MSG-P4-002.
5. The `V2009_1` read index and the migration check (DP-15); re-run the cut-off query on the SIT volume.
6. CaseFactEventAssembler over the four existing case events, with a contract test that each carries productGroup, status, stageCode, routeCode, queueId and entryDate and no personal field.
7. Contract-fake run of every cross-service answer (authorise, decision count, published measures) so the story builds before the other services exist.

**Feature switch.** None on the read: a fact row exists when the case row exists, and the endpoint is behind the gateway-bff route and the access check. The legacy switch `rwb.reporting.steering` is the P9 slice's and is not reused here.

**Done when.** The tests in section 16 pass, the two counts agree at 240 on the synthetic day, the MORTGAGE filter returns 140, the four case events carry the fact dimensions, and the contract tests of RWB-P9-E2009-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P9-002 | The case fact total differs from the case list count at the cut-off | The case count on the dashboard ({count}) does not match the case list ({listCount}) for {date}. The publish is held. |
| MSG-P1-001 | A source of the measure set is stale | {product} is from {date}. Today's load has not arrived. |

MSG-P9-002 and MSG-P1-001 are raised in the P9 slice; this story returns the counts and the business date that they name.

### 15. Screens and states

SCR-02 Case list (module P3, owner rwb-case) carries the case facts this story serves: case number, product, status, stage, queue, entry date and age, with the queue filter.

| State | What the user sees and does |
|---|---|
| Loading | Skeleton rows while `GET /api/recovery/case/v1/cases` returns |
| List | One row per open case at the cut-off, with the count of the filtered list above it |
| Filtered | Rows for the chosen product group, stage, queue and status; the count follows the filter, for example 140 Mortgage cases |
| Empty | The empty state with a zero count; no row is invented |

SCR-37 Steering dashboard is the P9 slice's screen. The gateway-bff composite route serves both screens, one hop each, and merges the answers into the screen model; its SCR-37 detail and the field-level masking of any personal field are Not specified in the source documents (GAP-0731; ASM-1292).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-009-01 | AC1, BR1, BR4 | End to end | Synthetic day 2026-12-15 |
| TC-E2-009-02 | AC2, BR1, BR2 | End to end | 240 open cases; 1,412 decision log entries |
| TC-E2-009-03 | AC3, BR3 | End to end | case-intake 1.2.0: 200 recommendations, 170 accepted, 30 overridden |
| TC-E2-009-04 | AC4, BR2 | End to end | Case list 240, case facts 239 |
| TC-E2-009-05 | AC5, BR4 | End to end | Notice product dated 2026-12-14 |
| TC-E2-009-06 | AC6 | End to end | from 2026-12-15, to 2026-12-01 |
| TC-E2-009-07 | AC7, BR6 | End to end | deviation-screen 0.9.0 with no runs |
| TC-E2-009-08 | AC8, BR7 | End to end | Filter MORTGAGE |
| TC-E2-009-09 | AC9, BR5 | End to end | JOB-15 rerun for 2026-12-15 |
| TC-E2-009-10 | Access | Component | PT-LAWFIRM calls GET /reports/measures; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. TC-E2-009-01, -03, -05, -06, -07 and -09 are kept for the traceability of the P9 and agent slices; in this story they are read only as the neighbouring tests of the same day.

### 17. Guardrails

- No business value in code: the product group, stage, queue and status values are reference data with a version; the cut-off and the measure codes are the measure set's, not this service's.
- No personal data in the case facts, events or logs: the facts carry case number, product group, status, stage, route, queue and dates only. No name, address, contact point or identity number is read, logged or published.
- No read of another service's tables and no ACE view: the facts come from `rwb_case` only, the authorise answer from rwb-access, and the decision count from the decision log's owner. The `rwb_case` schema holds no foreign key into another schema.
- Every case event is written to the outbox in the same transaction as the state change and carries IDs and facts only.
- SCR-02 and SCR-37 show the same facts: nothing is counted by hand and no separate count is kept.
- A fact of a business date is never rewritten after its cut-off; a later change belongs to the next business date.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-009 | Steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-OCC-12, FEAT-RPT-03, FEAT-RPT-08 | 15 Manage performance, data and AI | None; NFR-065 and NFR-066 apply | TC-E2-009-01, TC-E2-009-03, TC-E2-009-05, TC-E2-009-06, TC-E2-009-07, TC-E2-009-09, TC-E2-009-10 |
| REQ-WKM-006 | Queue counts and ageing reported daily and reconciled to the case list | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-RPT-08 | 15 Manage performance, data and AI | None; DL25 applies | TC-E2-009-02, TC-E2-009-04, TC-E2-009-08 |

### 19. Out of scope

- The measure definitions, the seven calculators, the snapshots, the publish hold, the extract and SCR-37 (the P9 slice of this legacy key).
- The Power BI data set and its 07:30 refresh (the P9 slice).
- Agent acceptance and override rates and the agent runs they count (the agent slice of this legacy key).
- Queue measures and service level breaches for team managers (RWB-E1-030).
- The agent monitoring dashboard with latency and cost (RWB-E2-031).
- Benefit realisation against the baseline (FEAT-RPT-06, Epic 6).
- Regulatory returns (FEAT-RPT-07, Epic 8).
- The end-to-end wiring of the measure run to the case events (the ITG slice of this legacy key).
