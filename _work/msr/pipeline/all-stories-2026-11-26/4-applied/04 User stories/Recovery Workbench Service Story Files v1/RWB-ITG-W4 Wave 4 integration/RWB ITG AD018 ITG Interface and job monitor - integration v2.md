# RWB-ITG-AD018-ITG Interface and job monitor

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-AD018-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-AD018-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-018 as the wave 4 integration proof of the interface and job monitor, from the job read and the freshness read through the gateway-bff composite route, the rerun of a failed Workbench job with one Idempotency-Key and its two runs in the job log, and the late EFS batch whose dependent job is recorded WAITING and whose data product shows STALE, never rerun from the Workbench; the three operations and the job state are RWB-P1-AD018-APP's and SCR-44 is a gateway-bff route over them. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-AD018-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof that the interface and job monitor composes rwb-source-data's job read and freshness read behind the gateway-bff route, that a failed Workbench job is rerun exactly once and both runs are in the job log, and that a late or failed ACE batch leaves the dependent job WAITING and its data product STALE and is never rerun from the Workbench**, so that **a failed job is found and rerun the same morning and a late ACE batch is never mistaken for a failed job**.

This story builds the harness and the evidence report, and nothing else. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service. It drives the published operations of the owner, reads the effect through the owner's published reads, counts the owner's events and writes one run report per business date. On Day 1 it runs against a stub generated from the published contract; when RWB-P1-AD018-APP lands, the stub is replaced and the same tests run again.

The legacy key splits one way. **RWB-P1-AD018-APP owns the deliverable**: the job read `GET /api/recovery/source-data/v1/admin/jobs`, the rerun `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun`, the freshness read `GET /api/recovery/source-data/v1/data-products/freshness`, the job log behind the first two, the ACE batch record behind the third, and the `data_product_load` and `reconciliation_result` rows the monitor shows — the Ownership Map puts all three operations on P1 rwb-source-data. **SCR-44 Interface and job monitor is the gateway-bff composite route** over those operations (DP-19, RWB-PLT-N001-CON) and is not built or rendered here: the harness calls the three operations and composes nothing of its own. The harness drives and observes only.

**`v_ace_batch_status` is read only through P1's contract** (DP-05). No service and no harness opens the view, so the last complete ACE business date of a source reaches the monitor as P1's answer and never as a query. **JOB-04 Reconciliation is an event-started workflow in P1** — Architecture v5 slide 44 records it as "event-triggered workflow" on rwb-source-data, started by `AceDataReady` — and **JOB-05 and its five-minute Quartz timer check are retired** in favour of durable timers inside the workflows, so no job in this story is timed by a Quartz entry and nothing here waits on a cron.

The `job_catalog` row itself stays with P2 rwb-integration in the Ownership Map (ASM-0075), while the job read, the rerun and the freshness read are P1's; the Workbench jobs the monitor lists are the job map's Schedules and event-started workflows in their owning services (Arch v5 slide 44), which is why this story reads them through P1's operation only and never through the catalog's table. The outbound actions are P2's `outbound_item` rows and reach the monitor through the same job read, so **rwb-integration is not called by this story**.

### 2. Business rationale

The legacy monitor shows every Workbench job and outbound action with its status, business date, duration and checks, and beside it the last complete ACE business date of each source, so that a failed job is found and rerun the same morning and a late ACE batch is not mistaken for a failed job. The guardrail of the same story carries the half that cannot be repaired afterwards: **no ACE batch is rerun from the Workbench** — ACE ingestion owns the source runs, and the Workbench records the dependent job as WAITING. Two different mornings are written against here. On the first, a reconciliation run fails at 03:00 and nobody sees it until the officers open their queues, so the morning's cases are worked on yesterday's list. On the second, the EFS batch is late or failed, the dependent job does not run, and an administrator who reads that as a failed job reruns the ACE source batch from a Workbench button — double-loading a source that ACE still owns.

Under D-RCV-60 those facts are P1's, and the split matters because a rerun and a late batch are two different facts across two reads and one write. The job read answers what the Workbench jobs did: job ID, business date, status, duration and the result of each check. The freshness read answers what the sources delivered: the last complete ACE business date of each source and the state of the data product built from it. The rerun operation is a write that may only repeat a Workbench job that already ran. A rerun and a late batch look identical on a monitor that carries one status column and no freshness column beside it, and that is exactly the confusion the legacy acceptance criteria separate: AC2 reruns a failed job, AC3 records the dependent job as WAITING and never reruns it.

The pairing of WAITING and STALE is the whole design of the second morning. A job whose source batch is failed or has not arrived is recorded WAITING and not FAILED, because nothing has failed in the Workbench; its data product is flagged STALE with `MSG-P1-001`, which names the product and the business date the data is from, because the readers downstream have to know that what they are about to act on is not today's. A stale product that reaches a route decision as if it were fresh is the failure this story is written against: ACE data is read by every other service through rwb-source-data and never from the views (Arch v5 slide 45, "Who reads ACE's data?"), so the freshness flag P1 sets is the only place where a route decision in rwb-valuation or a case creation in rwb-case can learn that the account facts behind it are a day old. A monitor that showed the product as fresh, or that showed the job as failed and offered a rerun, would turn a known delay into an unknown data defect.

The harness is decoupled the way the services are. Every call is one hop on the owner's base `/api/recovery/source-data/v1` with a 2 s budget (DP-11, DP-13), and ADR-020 makes that the only REST shape allowed. `v_ace_batch_status` is reached through P1's contract and never opened (DP-05), no `rwb_source_data` table is read by the harness or by any other service (DP-01), and the screen the administrator would use is the gateway-bff composite route over the same three calls (DP-19). The rerun carries one Idempotency-Key, so a repeated click answers the same run instead of starting a second one.

Two limits are stated here because they shape the run. The first is that the sources publish the three operations and the legacy data table, but not the response shapes, the job-log field list, the freshness answer's fields, the read path P1 uses for `v_ace_batch_status`, or the messages for a refused rerun and for a batch that is not a Workbench job; the suite therefore asserts through the owners' contracts and records the open point as GAP-0440 and ASM-0632. The second is that AC3's "when the dependent job reaches its schedule" is the legacy wording of an event-started job: under D-RCV-60 JOB-04 starts from `AceDataReady`, so the harness reaches the job's start point through the fixture's batch state and the `AceDataLate` publication of the owner, and asserts the WAITING record and the STALE product rather than a Quartz fire. Release 30 June 2027 stays tentative, and a date is never a condition of this story.

### 3. Preconditions

- RWB-P1-AD018-APP is the I story that owns the deliverable: the job read, the rerun with its Idempotency-Key, the freshness read, the job log, and the WAITING and STALE behaviour of AC3. Its stub answers from Day 1 and is replaced when it lands; until then the run is reported as a stub pass.
- The published contract of P1 rwb-source-data — the three operations of §12.2 — is in the contract registry and deployed in SIT under `/api/recovery/source-data/v1` behind the gateway-bff route, and a stub set is generated from it with its version pinned in the run report.
- The gateway-bff composite route of SCR-44 stands on the platform story RWB-PLT-N001-CON, which DP-19 adds as an H dependency. It is a platform wave delivery that every service and the harness build against, so it is not repeated in the metadata H row of this story, which stays None; the harness calls the three P1 operations directly and does not require the route to compose them in SIT.
- SIT is in place: the task queue `rwb-source-data` in the namespace `rwb-recovery`, and the topic `rwb.source-data.events.v1` with its retry and `.dlt` topics.
- The fixture holds a synthetic job catalog, two business dates and a data product per source as data, not as code: the job view business date 2026-11-30, the reconciliation job `JOB-04` of the job map with a FAILED run on that date, the EFS source batch for 2026-12-01 with status FAILED, the dependent job of that source, and one data product whose freshness is unknown. The job IDs, business dates, batch states and products are read from the fixture and are never written in code.
- The caller set is the harness's own: `RW-PLATADM`, holding Platform administration U and R, as the administrator who reruns the job, and `RW-OFF`, holding no Platform administration right, as the refused caller of AC4.
- No production data is used and no production connection is opened; the suite refuses an environment that is not SIT, and release 30 June 2027 is tentative.
- This story has no build dependency, so it is ready on Day 1 under Template and Rules §R5.7. The one wait is RWB-P1-AD018-APP, which replaces its stub and never blocks the lane.
- The exact response shapes of the job read and the rerun, the field list of the job log, the exact shape of the freshness answer, the path by which P1 reads `v_ace_batch_status`, and the message IDs for a refused rerun and for a batch that is not a Workbench job: Not specified in the source documents (GAP-0440; ASM-0632).

### 4. Flow

1. Harness: loads the fixture — the job catalog entries for business date 2026-11-30, the reconciliation job `JOB-04` with a FAILED run on that date, the EFS batch for 2026-12-01 with status FAILED, the dependent job of that source, a data product per source, one product whose freshness is unknown, the caller `RW-PLATADM` and the refused caller `RW-OFF`. It takes a baseline read of the job list and of the freshness list before it writes anything, opens no production connection, and refuses an environment that is not SIT.
2. Harness: reads `GET /api/recovery/source-data/v1/admin/jobs` for business date 2026-11-30 and asserts every job carries its job ID, business date, status, duration and the result of each check, that the FAILED run of `JOB-04` is among them, and that no field arrives outside the published contract.
3. Harness: reads `GET /api/recovery/source-data/v1/data-products/freshness` and asserts each job that reads ACE carries the last complete ACE business date of its source, and that the business dates of the two answers agree as one monitor view.
4. Harness: asserts the monitor is composed from those two reads in one hop each behind the gateway-bff route (DP-13, DP-19): the probe records the hops and the contract versions, no ACE view is opened and no `rwb_source_data` table is read (DP-01, DP-05).
5. Harness: reruns the failed run of `JOB-04` through `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` as `RW-PLATADM` with one Idempotency-Key, and asserts the answer names the run it started.
6. Harness: reads the job list again and asserts two runs for `JOB-04` — the first FAILED and the second RUNNING or COMPLETE — each with its own business date, duration and check results, so the job log holds both.
7. Harness: repeats the same Idempotency-Key and asserts the same run is answered and that the job list still holds two runs, so no third run was created (AC2).
8. Harness: reads the EFS source batch for business date 2026-12-01 through P1's contract, sees status FAILED with `AceDataLate` published on `rwb.source-data.events.v1`, and asserts the dependent job is recorded WAITING in the job list and carries no new run (AC3).
9. Harness: reads the freshness answer for the dependent product and asserts STALE with `MSG-P1-001` carrying the product and the business date the data is from, and then reads the product whose freshness is unknown and asserts it is never shown fresh: it shows its last known complete ACE business date and the business date of the last refresh, while the other jobs and products still show in the same answer (AC5).
10. Harness: attempts a rerun naming the ACE source batch of 2026-12-01 through the same rerun operation and asserts it is refused, that the refusal names the batch as not a Workbench job, that no run is created and that the dependent job stays WAITING (AC6).
11. Harness: calls `GET /api/recovery/access/v1/me/session` as `RW-OFF`, attempts the rerun and asserts 403 with `MSG-P4-002`, no run created and the job read unchanged run for run; then attempts a rerun with no Idempotency-Key and asserts `MSG-GEN-001` naming the missing field (AC4).
12. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the two runs of `JOB-04`, the WAITING job, the STALE product, the refused batch and the criteria verdicts, and restores the fixture.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | Preflight, AC1 |
| X2 | A rerun is sent without its Idempotency-Key | The rerun is refused and no run is created, so a second click can never start a second run | MSG-GEN-001 | AC2 |
| X3 | A rerun names a job ID that is not in the catalog | The rerun is refused and no run is created; the report names the job ID it was given and the catalog read | Not specified in the source documents (GAP-0440; ASM-0632) | AC6 |
| X4 | A rerun names an ACE source batch instead of a Workbench job | The batch is refused and named as not a Workbench job, no run is created, and the dependent job stays WAITING | Not specified in the source documents (GAP-0440; ASM-0632) | AC6 |
| X5 | A copy of the freshness answer is served beside the owner's, or the monitor reads a snapshot of it | The run fails on AC1 and AC5 and the report names the second source, its business date and the owner's date side by side, because a second copy of a freshness fact is the defect the story exists for | None | AC1, AC5 |
| X6 | A caller without Platform administration U attempts the rerun | The rerun is refused with 403 and the job read is unchanged run for run | MSG-P4-002 | AC4 |
| X7 | A data product has no complete ACE business date for its source | The product is not shown fresh: it carries its last known complete date and the date of its last refresh, and its dependent job is not listed as complete | MSG-P1-001 | AC5 |
| X8 | The consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owner and no fake is put in its place | None | Preflight, AC1 |
| X9 | A consumed call exceeds the 2 s budget or returns a server error | The call is retried once under the suite policy, the evidence report records it, and no assertion is made on data that was not read | None | AC1 to AC6 |
| X10 | A suite step tries to read `recovery.v_ace_batch_status`, `rwb_source_data` or any service schema directly | The step does not exist: the suite is built with no client for a view or a schema, and the pipeline scan fails any change that adds one | None | Section 17 |

X1 to X7 are the monitor failures the legacy story is written against, re-stated on the owner's two reads and one write; X8 to X10 are the harness and cross-service failures that only appear when the run leaves one service. The two refusals of X3 and X4 have no published message: the story names the batch as not a Workbench job and refuses it, and the report asserts the refusal and the absence of a run rather than a message string, with the open point held as GAP-0440 and ASM-0632.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module, needs the published contract of P1 rwb-source-data and its stub from Day 1, owns no schema and no table, and never writes a job row, a batch state or a data product by hand |
| Negotiable | The fixture layout, the job IDs, the business dates, the data products, the report shape and the pass or fail gate are agreed at the wave entry check; the legacy values 2026-11-30, 2026-12-01, EFS, FAILED, MSG-P1-001, MSG-GEN-001 and MSG-P4-002 are the only fixed ones |
| Valuable | Proves across the boundary what one service cannot prove: the monitor is two owner reads and no view, a failed job is rerun once and both runs are logged, a repeated key starts nothing, a late batch is WAITING and STALE rather than failed, and an ACE batch cannot be rerun from the Workbench |
| Estimable | One harness module, one fixture pack, four contract probes, one rerun driver, one stub set and one evidence report |
| Small | Six scenarios over one service and one write; no service code, no schema change, no production flag |
| Testable | Every scenario asserts a contract answer, a run in the job log, a WAITING or STALE fact, an event count or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Interface and job monitor - wave 4 integration harness

  Background:
    Given rwb-source-data is deployed in SIT with its published contract behind the gateway-bff route and the harness runs against its stub from Day 1
    Given the job catalog, the data products and the business dates are held in the fixture as data and no production data is used
    Given the fixture holds business date "2026-11-30" for the job view and the EFS source batch for "2026-12-01" with status "FAILED"

  Scenario: AC1 The monitor is composed from the owner's job read and freshness read (new, D-RCV-60)
    Given the job list and the freshness list for business date "2026-11-30" are read through P1's two published operations, one hop each behind the gateway-bff route
    When the monitor is composed from those two answers
    Then each job carries its job ID, business date, status, duration and the result of each check from the job read
    And each job that reads ACE carries the last complete ACE business date of its source from the freshness read
    And no ACE view is opened and no rwb_source_data table is read by the harness or by any other service

  Scenario: AC2 A failed Workbench job is rerun once and both runs are in the job log (new, D-RCV-60)
    Given the reconciliation job "JOB-04" is in the job list for business date "2026-11-30" with status FAILED
    When it is rerun through POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun with one Idempotency-Key
    Then the job list holds two runs for the job, the first FAILED and the second RUNNING or COMPLETE
    And the same Idempotency-Key repeated answers the same run and creates no third run

  Scenario: AC3 A late ACE batch (legacy RWB-AD-018 AC3)
    Given v_ace_batch_status shows EFS for business date 2026-12-01 with status FAILED
    When the dependent job reaches its schedule
    Then the job is recorded WAITING and is not rerun
    And its data product shows STALE with MSG-P1-001

  Scenario: AC4 A caller without Platform administration U is refused and no run is created (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" whose role holds no Platform administration U
    When the caller reruns the failed job through POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun
    Then the answer is 403 with "MSG-P4-002"
    And no run is created and the job read is unchanged, run for run

  Scenario: AC5 A data product whose freshness is unknown is never shown as fresh (new, D-RCV-60)
    Given the freshness read carries a data product whose source has no complete ACE business date
    When the monitor shows that product
    Then the product is not shown as fresh and it shows its last known complete ACE business date and the business date of the last refresh
    And the other jobs and their sources still show in the same answer

  Scenario: AC6 An ACE source batch is never rerun from the Workbench (new, D-RCV-60)
    Given the EFS source batch for business date "2026-12-01" is FAILED
    When a rerun is attempted through POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun naming that batch
    Then the rerun operation accepts a Workbench job ID only and the batch is refused
    And the refusal names the batch as not a Workbench job
    And the dependent job stays WAITING and no run is created
```

AC3 is the legacy criterion, copied word for word. AC1 and AC2 are the business outcome RWB-P1-AD018-APP has to reach and are asserted here across the service boundary; AC4 to AC6 are the new scenarios the split makes assertable, because the right, the refusal and the guarantee that an ACE batch is never rerun from the Workbench are properties of the seam and not of one service.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every Workbench job shows its job ID, business date, status, duration and the result of each check, and each job that reads ACE shows the last complete ACE business date of its source | RWB-AD-018 AC1 |
| BR2 | A failed Workbench job is rerun from its run book after the cause is fixed, and both runs are in the job log | RWB-AD-018 AC2 |
| BR3 | A late or failed ACE batch leaves the dependent job recorded WAITING and not rerun, and its data product STALE with MSG-P1-001 | RWB-AD-018 AC3 |
| BR4 | **No ACE batch is rerun from the Workbench**: ACE ingestion owns the source runs, and the Workbench records the dependent job as WAITING | RWB-AD-018 guardrail; Architecture v5 slide 32 (Airflow runs the ACE ingestion DAG and says the business date is ready) |
| BR5 | **A late batch is WAITING, not failed**: WAITING is the state of a job whose source has not delivered, FAILED is the state of a run that ran and failed, and only the second may be rerun | RWB-AD-018 AC2 and AC3; the guardrail of the same story |
| BR6 | `v_ace_batch_status` is read only through rwb-source-data's contract, and no service opens the view or reads another service's table | DP-05, DP-01; RWB-AD-018 guardrail; Architecture v5 slide 41 (P1 owns the ACE view contract and freshness) |
| BR7 | The freshness of a data product is P1's single fact: the last complete ACE business date of its source and the state of the product are answered once and never copied | DP-05; Architecture v5 slide 41; Architecture v5 slide 45 (only rwb-source-data reads the 30 ACE views) |
| BR8 | JOB-04 Reconciliation is an event-started workflow in rwb-source-data and JOB-05 is retired, so no job in the monitor is timed by a Quartz entry | Architecture v5 slide 44; ADR-016 |
| BR9 | Every call in the run is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout, and the composite path the screen uses is the gateway-bff route | DP-11, DP-13, DP-19; ADR-020 |
| BR10 | A rerun carries one Idempotency-Key and a repeat of the key answers the same run instead of starting a second, and the right to rerun is Platform administration U | RWB-AD-018 permission checks; DP-13; ADR-020 |

The harness asserts these rules and changes none of them. The job run, the job log, the batch record and the data product are P1's, the right is answered by rwb-access and enforced by P1, and the values in the table are the legacy ones.

### 9. State transitions

| Subject | From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|---|
| Job run | FAILED | RERUN_REQUESTED | the caller holds Platform administration U, the job is a Workbench job and one Idempotency-Key is presented | RUNNING | P1 rwb-source-data, `POST /admin/jobs/{jobId}/rerun`, one new run in the job log |
| Job run | RUNNING | RUN_COMPLETED | every check of the run passes | COMPLETE | P1 rwb-source-data |
| Job run | RUNNING | RUN_FAILED | a check of the run fails | FAILED | P1 rwb-source-data |
| Job | READY | SOURCE_BATCH_NOT_DELIVERED | the ACE batch of its source is FAILED or has not arrived at the job's start point | WAITING | P1 rwb-source-data, the freshness check behind the job |
| Job | WAITING | SOURCE_BATCH_DELIVERED | `AceDataReady` for the business date of the source | READY for its start point | P1 rwb-source-data |
| Data product | FRESH | SOURCE_BATCH_NOT_DELIVERED | the batch of its source is FAILED or not complete | STALE, with MSG-P1-001 | P1 rwb-source-data, `data_product_load` |
| Data product | FRESH or STALE | SOURCE_BATCH_DELIVERED | the batch of its source completes | FRESH at the new last complete ACE business date | P1 rwb-source-data |

The job states are the status the job read answers, and the data product state is the freshness the freshness read answers; neither is written by the harness. The WAITING state is the one the legacy story calls "waiting for the ACE batch" on SCR-44, and it is deliberately not a failure: a run that failed may be rerun, a job that is WAITING may not, which is why the two states sit in different columns of the run report. The fixture carries two business dates for one job: the reconciliation job `JOB-04` has a FAILED run on 2026-11-30, which the run reruns, and a 2026-12-01 start point whose EFS batch is FAILED, which leaves it WAITING. The harness changes no state; every row above is made by P1 through its own operation or its own check, and a state the harness set by hand would prove nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Holds Platform administration U and R; is the caller that reads both reads in AC1 and reruns the failed job in AC2 |
| RW-SECADM, security administrator | Holds Platform administration U and R as well, and is the second role that may rerun a Workbench job |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Hold Platform administration R; they read the monitor and are refused the rerun, which is the read-only half of the legacy permission table |
| RW-OFF, officer without the administration rights | Is the refused caller of AC4 and X6: holds no Platform administration right, so the rerun answers 403 with MSG-P4-002 |
| QA lead | Owns the harness configuration, the fixture data, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the owning service |
| P1 rwb-source-data | Runs the job, holds the job log, the ACE batch record and the data product load, answers the three operations and records a job as WAITING; it makes every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and enforced by the owning service |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-224 to DF-OPS-232 | job_catalog | id, job_id, job_name, owner_role, schedule_text, expected_minutes, alert_after_minutes, first_release | Read through P1's job read only; the row itself stays with P2 rwb-integration (ASM-0075) and is never read from a schema |
| DF-OPS-001 to DF-OPS-008 | data_product_load | id, product_code, source_system, business_date, loaded_at, status, stale_flagged_at | Read through P1's freshness read; STALE and MSG-P1-001 are asserted there |
| DF-ACE-178 to DF-ACE-186 | v_ace_batch_status | source_system, business_date, started_at, completed_at, status, record_count and 3 more | Read only through P1's contract (DP-05); never `recovery.v_ace_batch_status` directly and never from a schema |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | Not specified in the source documents (GAP-0440; ASM-0632) | Read only if P1's job read carries it; the run reads no reconciliation row directly |
| Not specified in the source documents (GAP-0440; ASM-0632) | outbound_item | The outbound action rows shown beside the jobs | P2 rwb-integration's rows, read only through P1's job read; this story does not call rwb-integration |

Field IDs are those in the Logical Data Model and Data Dictionary v9, and the three entities of the legacy data table are the job catalog, the data product load and the ACE batch status. The job catalog row stays with P2 rwb-integration in the Ownership Map, while the job read served by P1 is the operation that answers it; the data product load and the reconciliation result are P1's, and the ACE batch status reaches the monitor only as P1's answer. The harness owns no table and writes no row: the two runs of `JOB-04` are created by the owner's rerun operation, and the WAITING job and the STALE product are made by the owner's freshness check. Every key in the run is synthetic, and no field in the table carries personal data.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/admin/jobs` | P1 rwb-source-data | The jobs of the catalog for the business date, with job ID, business date, status, duration and each check result (AC1, AC2, AC3, AC5, AC6) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Reruns a failed Workbench job with one Idempotency-Key, and refuses a caller, a key and a job that are not allowed (AC2, AC4, AC6) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The last complete ACE business date of each source, the state of each data product and the MSG-P1-001 warning (AC1, AC3, AC5, AC6) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a rerun (AC4) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13), and no operation is invented in this story: each path is the owner's published operation in the Ownership Map. The map also publishes `GET /api/recovery/source-data/v1/admin/data-products` and `GET /api/recovery/source-data/v1/admin/data-contracts` on P1; this run calls neither, because the freshness of a product is read from the freshness operation, which is the one the monitor uses. Where a screen would compose the three calls the path is the gateway-bff composite route (DP-19), and SCR-44 is that route rather than a service operation.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record. In particular it never publishes `AceDataReady`, `AceDataLate` or a batch-ready signal of its own, because the ACE ingestion and the freshness check are P1's and the whole point of AC3 and AC6 is that the Workbench does not cause a source run.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Confirms that the business date was accepted for the sources that delivered, and that the reconciliation job of that date was started; counted once per delivered business date, and observed at zero for the 2026-12-01 EFS path (AC1, AC3) |
| `rwb.source-data.AceDataLate.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Counts the one publication that accompanies the failed or late EFS batch of 2026-12-01, which is the event the 05:30 alarm and the gateway banner stand on, and reads its consumption as the WAITING job and the STALE product (AC3, AC6) |

The harness subscribes to the topic under one consumer group of its own and counts publications. While the stub answers, the two counts are read from the stub's recorded publications and the report says so; with the real P1 in place they are counted on `rwb.source-data.events.v1`. Nothing is replayed: the paths exercised here are single-shot reads and one rerun, and a replay would test P1's inbox rather than the monitor.

#### 12.5 Workflows and activities

None added. The harness observes two workflows on the task queue `rwb-source-data`, both stated in Architecture v5 slide 15 as P1's: **`AceIngestCheck`**, the workflow that checks the freshness of the sources and decides whether a business date is delivered, and **`reconciliation`**, the JOB-04 workflow started by `AceDataReady` in place of the retired Quartz entry (slide 44). It observes them through their effects — the WAITING job and the STALE product on the two reads — and never reads a workflow history, so the run asserts the monitor and not the execution. No workflow, activity, worker or Schedule is created, changed or owned here.

#### 12.6 Schedules

None added. The monitor is a read composition and a rerun, so nothing in this story is on a cron; JOB-05 and its five-minute Quartz timer check are retired in favour of durable timers inside the workflows, and JOB-04 is started by `AceDataReady` rather than by a schedule (Architecture v5 slide 44; Temporal design slide 32, "jobs as Schedules", no Quartz). The harness moves no schedule, starts no job timer and asserts no cron.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): `job_catalog` stays with P2 rwb-integration (ASM-0075), `data_product_load` and `reconciliation_result` are P1's, `v_ace_batch_status` is an ACE view read only by P1, and `outbound_item` is P2's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun`, `GET /data-products/freshness` | The job list for business date 2026-11-30 with the FAILED run of `JOB-04`, then two runs once the rerun is accepted and again two after the repeated key; the WAITING dependent job for 2026-12-01; the freshness answer with the last complete ACE business date, the STALE product with MSG-P1-001 and the unknown-freshness product; a refusal naming the EFS batch as not a Workbench job; MSG-GEN-001 for a rerun without its key |
| Stub for rwb-access | `GET /me/session` | Allows `RW-PLATADM` with Platform administration U and R; refuses `RW-OFF` with 403 and MSG-P4-002 |
| Stub for the gateway-bff composite route | The SCR-44 route over the three P1 operations | Answers one composite read of the monitor by calling the two reads once each, so the hop count of AC1 can be asserted while the route itself is not built here |
| Job and batch fixture | The job catalog entries, the business dates, the ACE batch states and the data products | `JOB-04` reconciliation with a FAILED run on 2026-11-30; the EFS batch for 2026-12-01 at status FAILED with `AceDataLate`; the dependent job and its product; one product whose freshness is unknown; all held as data |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The exact response shapes of the job read and the rerun, the field list of the job log, the exact shape of the freshness answer, the path by which P1 reads `v_ace_batch_status`, and the message IDs for a refused rerun and for a batch that is not a Workbench job are Not specified in the source documents (GAP-0440; ASM-0632).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 4 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.source-data.AceDataReady.v1` counted once per delivered business date and `rwb.source-data.AceDataLate.v1` counted once for the 2026-12-01 EFS path |
| Temporal | None added; `AceIngestCheck` and `reconciliation` on `rwb-source-data` observed through the WAITING job and the STALE product |
| File | None. No file is transferred, parsed or archived; the monitor is two reads, one rerun and one report |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-19 adds one platform H story, RWB-PLT-N001-CON, which is delivered by the platform wave and is therefore not repeated in the metadata H row of this story, which stays None; DP-13 adds nothing, and DP-05 adds nothing because the view is read by P1 and this story only reads P1's answer. The one blocking dependency is the I story RWB-P1-AD018-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JobListProbe | Service | Reads `GET /admin/jobs` for the business date, records the job ID, business date, status, duration and each check result, and compares two reads run for run after the rerun |
| FreshnessProbe | Service | Reads `GET /data-products/freshness`, records the last complete ACE business date of each source, asserts STALE with MSG-P1-001, and asserts that an unknown-freshness product is never shown fresh |
| RerunDriver | Service | Drives `POST /admin/jobs/{jobId}/rerun` as `RW-PLATADM` with one Idempotency-Key, repeats the key, attempts the ACE source batch, and records the answer, the run it names and the refusal |
| BatchStatusProbe | Service | Asserts the EFS batch of 2026-12-01 at status FAILED through P1's contract only, and that the dependent job is WAITING with no new run |
| SessionProbe | Service | Reads `GET /me/session`, confirms the caller's Platform administration rights, and holds the `RW-OFF` refusal |
| StubSet | Fake | The two stubs, the composite-route stub and the job and batch fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per business date keyed by story, with the two runs side by side, the WAITING job, the STALE product, the refused batch, the contract version of each hop, whether the hop was a stub or the owner, and the gate |

**Environment and test data.** SIT, against the stub from Day 1 and the real P1 as RWB-P1-AD018-APP lands, on business dates 2026-11-30 and 2026-12-01, the reconciliation job `JOB-04`, the EFS source batch, one data product per source, one product whose freshness is unknown, the caller `RW-PLATADM` and the refused caller `RW-OFF`. The harness seeds nothing by hand, never writes a job row, a batch state or a data product, and refuses an environment that is not SIT. The exact response shapes of the job read and the rerun, the field list of the job log, the exact shape of the freshness answer, the path by which P1 reads `v_ace_batch_status`, and the message IDs for a refused rerun and for a batch that is not a Workbench job are Not specified in the source documents (GAP-0440; ASM-0632).

**Build steps**

1. Generate the three stubs and the job and batch fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1, X8).
2. Build the JobListProbe and assert AC1's job fields for business date 2026-11-30, including the FAILED run of `JOB-04`.
3. Add the FreshnessProbe for the other half of AC1: the last complete ACE business date of each source, one hop per read, and the hop record that proves no view and no schema was opened (X5, X10).
4. Build the RerunDriver and rerun the failed run with one Idempotency-Key; assert two runs in the job log, the first FAILED and the second RUNNING or COMPLETE (AC2).
5. Add the repeated-key step and assert the same run is answered and no third run exists; add the missing-key step and assert MSG-GEN-001 and no run (X2).
6. Add the BatchStatusProbe and the WAITING path of AC3: the EFS batch FAILED for 2026-12-01 through P1's contract, the dependent job WAITING, no new run, one `AceDataLate` counted, and zero `AceDataReady` for that path.
7. Add the STALE and unknown-freshness paths of AC3 and AC5: the product flagged STALE with MSG-P1-001 naming the product and its date, and the product whose freshness is unknown never shown fresh while the other jobs still show (X7).
8. Add the batch-refusal path of AC6: the rerun naming the EFS batch is refused and named as not a Workbench job, no run is created, and the dependent job stays WAITING (X4); add the unknown job ID of X3 with no run created.
9. Add the SessionProbe and the refusal of AC4: 403 with MSG-P4-002, no run created, and the job read unchanged run for run (X6).
10. Add the EvidenceReport gate and swap the stub for rwb-source-data as RWB-P1-AD018-APP lands, reporting a stub pass as a stub pass.

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-AD018-APP when it lands, and the wave entry check holds a run report keyed by story and business date with the two runs of the job, the WAITING job and the STALE product side by side.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads and owns no message text. MSG-P1-001 is asserted with the product and the business date the data is from when the EFS product of 2026-12-01 is shown STALE (step 9, AC3), and with the last known complete date when a product's freshness is unknown (AC5). MSG-GEN-001 is asserted with the missing field name when a rerun is sent without its Idempotency-Key (step 11, X2). MSG-P4-002 is asserted with the rerun refused for `RW-OFF`, a caller without Platform administration U (step 11, AC4). The message a refused rerun answers for a job ID that is not in the catalog, and the message a rerun answers when it names an ACE source batch instead of a Workbench job, are Not specified in the source documents (GAP-0440; ASM-0632), so those two paths are asserted on the refusal, on the naming of the batch as not a Workbench job and on the absence of a run, never on a message string.

### 15. Screens and states

SCR-44 Interface and job monitor is the legacy screen with the states Running, failed, waiting for the ACE batch and complete, and it is not built or rendered here: the harness calls the two reads and the rerun behind it and composes nothing of its own. The screen is the gateway-bff composite route over the calls of §12.2 (DP-19), and no screen, route or user-interface element is created, changed or tested by this story. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0440; ASM-0632).

| State | Read through | What the run asserts |
|---|---|---|
| Running | P1 job read | The second run of `JOB-04` is RUNNING with its own business date and its duration counted to the read, while the first run stays FAILED beside it |
| Failed | P1 job read | The first run of `JOB-04` on 2026-11-30 is FAILED with the check result that failed, and a rerun is what may follow it |
| Waiting for the ACE batch | P1 job read and freshness read | The dependent job of 2026-12-01 is WAITING with no new run, and its data product is STALE with MSG-P1-001, so the state is a wait and not a failure |
| Complete | P1 job read | Where the fixture's second run completes, the run shows COMPLETE with its duration and every check passing, and the job still carries both runs |
| A refused rerun | rwb-access session read and the rerun answer | 403 with MSG-P4-002, no run created, and the job read unchanged; a batch named instead of a job is refused as not a Workbench job |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-018-01-ITG | AC1 | Integration | The job list and the freshness list for business date 2026-11-30, read once each through P1's operations behind the gateway-bff route, with the hop record and the contract version |
| TC-AD-018-02-ITG | AC2, AC6 | Integration | The FAILED run of `JOB-04`, one rerun with one Idempotency-Key, the repeated key, the batch named instead of a job, and the job list read before and after each attempt |
| TC-AD-018-03-ITG | AC3, AC5 | End to end | The EFS batch of 2026-12-01 at status FAILED, the dependent job WAITING, its product STALE with MSG-P1-001, and a product whose freshness is unknown beside it |
| TC-AD-018-04-ITG | Access; AC4 | Component | A synthetic caller `RW-OFF` without Platform administration U, the rerun refused with 403 and MSG-P4-002, and a rerun sent without its Idempotency-Key answering MSG-GEN-001 |

The legacy test cases TC-AD-018-01 to TC-AD-018-04 are kept as the `-ITG` copies above, with their legacy Covers: AC1 for TC-AD-018-01, AC2 for TC-AD-018-02, AC3 for TC-AD-018-03 and Access for TC-AD-018-04. The full legacy tests, with their Given, When and Then, are in the legacy test case workbook under the same legacy IDs. Legacy AC1 and AC2 stay the build criteria of RWB-P1-AD018-APP and legacy AC3 stays the criterion of that story too; the `-ITG` copies assert the same behaviour across the service boundary, AC5 has no legacy test case of its own in this key and is folded into TC-AD-018-03-ITG, and AC6 is asserted with the batch-refusal steps of TC-AD-018-02-ITG.

### 17. Guardrails

- No business value in code: the job IDs, the business dates 2026-11-30 and 2026-12-01, the batch states, the data products, the caller keys and the report layout are data held in the fixture.
- No personal data in logs, events or reports: every key is synthetic, the events carry IDs and facts only, and no case, party or account field is read by this story.
- ACE data only through the owner's contract: the batch status is read through P1's operation and never from `recovery.v_ace_batch_status`, and no `rwb_source_data` table or any other service's table or schema is opened (DP-01, DP-05).
- One hop and a 2 s budget per call, with a breaker per downstream, so the harness fails where the screen would (DP-11, DP-13, ADR-020).
- No invented operation: only the three P1 operations and the session read of §12.2, and no freshness, job or batch fact is asserted through a read the map does not publish.
- No ACE batch is rerun from the Workbench: the harness never publishes `AceDataReady`, never signals a business date ready and never drives an ACE ingestion path, and the refusal of AC6 is asserted as a failure of the run if a batch run is created.
- SIT only: the suite refuses any other environment, opens no production connection and uses no production data.
- No schema read and no hand-set state: the job run, the WAITING job and the STALE product are made by the owner, and the suite is built with no client for a view or a schema.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script, and a job shown FAILED when its source simply has not delivered is a failure and not a variant.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-AD-018 Interface and job monitor | Recovery Workbench Administration Stories v4, lines 1465 to 1548 | Sections 1, 2, 3, 11, 14 and 19 of this file |
| Legacy AC3, verbatim | The same, lines 1495 to 1499 | Section 7, AC3, marked (legacy RWB-AD-018 AC3) |
| Legacy AC1 and AC2 | The same, lines 1484 to 1493 | Section 7, AC1 and AC2, asserted here across the boundary; the criteria themselves stay with RWB-P1-AD018-APP (section 19) |
| Legacy guardrail, no ACE batch rerun from the Workbench | The same, line 1548 | Sections 1, 2, 8 (BR4, BR5) and 17 |
| Legacy test cases TC-AD-018-01 to TC-AD-018-04, with Covers AC1, AC2, AC3 and Access | The same, lines 1539 to 1546 | Copied as `-ITG` in section 16 |
| Legacy data entities and field IDs: job_catalog, data_product_load, v_ace_batch_status | The same, lines 1502 to 1508 | Section 11 |
| Legacy endpoints, screen, permission checks and messages | The same, lines 1510 to 1537 | Sections 12.2, 15, 10 and 14 |
| The P1 service row: ACE view contract, extension tables, freshness, reconciliation; schema rwb_source_data | Architecture v5 slide 41, text extract line 2884 | Sections 1, 2, 11 and 12.7 |
| The P1 contract: `GET /freshness`, the workflows `AceIngestCheck` and `reconciliation`, the freshness and reconciliation writes, the `AceDataReady` and `AceDataLate` topic | Architecture v5 slide 15, text extract lines 1075 to 1081 | Sections 2, 12.4 and 12.5 |
| The ACE batch ready call, the 05:30 and 07:00 SLA alerts, `AceDataLate` at 05:30, and `AceDataReady` starting JOB-04 | Architecture v5 slide 32, text extract lines 2292 to 2294 | Sections 2, 4 and 9 |
| Event catalogue #26 `AceDataReady` and #27 `AceDataLate` | Architecture v5 slide 43, text extract lines 2952 and 2953 | Section 12.4 |
| JOB-04 reconciliation as an event-triggered workflow on rwb-source-data, and JOB-05 retired in favour of durable timers | Architecture v5 slide 44, text extract lines 2980 and 2981 | Sections 1, 2, 8 (BR8) and 12.6 |
| "Who reads ACE's data?" — only rwb-source-data reads the 30 views, everyone else asks it through REST or an activity | Architecture v5 slide 45, text extract line 3016 | Sections 2 and 8 (BR7) |
| Jobs as Temporal Schedules, no Quartz | Temporal and Drools design slide 32, text extract line 2134 | Section 12.6 |
| Ownership Map v1 table rows for job_catalog, data_product_load, reconciliation_result and outbound_item | Ownership Map v1, with ASM-0075 for the job catalog row | Sections 1, 11 and 12.7 |
| Ownership Map v1 API rows for `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun`, `GET /data-products/freshness`, `GET /admin/data-products` and `GET /me/session` | The same | Section 12.2 |
| DP-05, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application, and the metadata Patterns applied row |
| ADR-016 and ADR-020 | Architecture Decision Records v4, with ADR-016 and ADR-020 as added by Template and Rules v1 §R8.4 | Sections 8, 12.2 and 12.6: Schedules replace Quartz, contract-first REST with one hop and 2 s |
| GAP-0440 and ASM-0632 | This run's gap and assumption registers | Sections 2, 3, 5, 7, 11, 12.8, 13, 14 and 15 |
| Release 30 June 2027 | The legacy story header, line 1469, copied unchanged and marked tentative | The metadata Release row and section 19 |

### 19. Out of scope

- RWB-P1-AD018-CON, RWB-P1-AD018-APP and RWB-P1-AD018-OPS: the build of the job read, the rerun, the freshness read, the job log, the WAITING and STALE behaviour, and their deployment. This story reads the operations and builds none of them.
- rwb-integration: the file runs and outbound items of P2, `interface_config` and `outbound_item`, and `GET /api/recovery/integration/v1/admin/scheduled-jobs`. The outbound actions reach the monitor through P1's job read, and this story does not call rwb-integration.
- The ACE ingestion and its own rerun: the Airflow DAG, the business-date ready call, the fallback poll of the ACE batch record, and every ACE source run. They stay with the bank scheduler and P1's `AceIngestCheck`.
- SCR-44 Interface and job monitor and every gateway-bff composite route: no screen, route or user-interface element is built or tested here.
- The platform stories the patterns add, including RWB-PLT-N001-CON, and the durable timer work of JOB-05's retirement.
- The data quality and reconciliation console of RWB-ITG-AD019-ITG: the same engine, a different story, and the reconciliation results are read there and not here.
- The queue configuration of RWB-ITG-AD014-ITG and the service-level configuration of RWB-ITG-AD015-ITG: the same seam, different stories.
- Any production change: no endpoint, table, workflow, activity, schedule, screen, feature flag or configuration in any service. The harness runs in SIT with synthetic data, and release 30 June 2027 stays tentative.
