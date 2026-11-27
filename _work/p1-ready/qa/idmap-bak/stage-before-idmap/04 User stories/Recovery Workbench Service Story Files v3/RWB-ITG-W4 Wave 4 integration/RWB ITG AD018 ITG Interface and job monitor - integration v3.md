# RWB-ITG-AD018-ITG Interface and job monitor

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Job read, rerun answers and codes aligned to rwb-source-data.yaml 5.1.0: run uuid, 202, MSG-PLT-N009-03 in place of MSG-GEN-001, 404 and 409 refusals, new AC10 (findings #1, #2, #4, #5).
- JOB-04 start, event key and payload, and freshness status LOADED or STALE aligned to RD-P1-040, RD-P1-003 and RD-P1-041 (#3, #6, #7, #8).
- P1 job set only; outbound actions out of this run; run-record tables of RD-P1-020 (#4, #12); retry rule for the POST (#14); contract and fake versions pinned (#11).
- Two points left pending: the run type that waits on the EFS batch (NEW-GAP-F06-2) and the carrier of MSG-P1-001 (NEW-GAP-F06-3) (#6, #9).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.

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
| Size | Set by the squad at refinement |
| Depends on (build) | RWB-P1-AD018-APP (not done; stubbed on Day 1) |
| Contract dependencies | RWB-P1-AD018-CON, RWB-P1-E1015-CON |
| Integration dependencies | RWB-P1-AD018-APP |
| External dependencies | None |
| Contract version | rwb-source-data.yaml 5.1.0 and rwb-source-data.asyncapi.yaml 5.1.0 (API Specification v7) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-024, RD-P1-040, RD-P1-041 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-018 as the wave 4 integration proof of the interface and job monitor, from the job read and the freshness read through the gateway-bff composite route, the rerun of a failed Workbench job with one Idempotency-Key and its two runs in the job log, and the late EFS batch whose dependent job is recorded WAITING and whose data product shows STALE, never rerun from the Workbench; the three operations and the job state are RWB-P1-AD018-APP's and SCR-44 is a gateway-bff route over them. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-AD018-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 7 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; job monitor harness aligned to the published job, event and freshness contracts.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof that the interface and job monitor composes rwb-source-data's job read and freshness read behind the gateway-bff route, that a failed Workbench job is rerun exactly once and both runs are in the job log, and that a late or failed ACE batch leaves the dependent job WAITING and its data product STALE and is never rerun from the Workbench**, so that **a failed job is found and rerun the same morning and a late ACE batch is never mistaken for a failed job**.

This story builds the harness and the evidence report, and nothing else. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service. It drives the published operations of the owner, reads the effect through the owner's published reads, counts the owner's events and writes one run report per business date. On Day 1 it runs against a stub generated from the published contract; when RWB-P1-AD018-APP lands, the stub is replaced and the same tests run again.

The legacy key splits one way. **RWB-P1-AD018-APP owns the deliverable**: the job read `GET /api/recovery/source-data/v1/admin/jobs`, the rerun `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun`, the freshness read `GET /api/recovery/source-data/v1/data-products/freshness`, the job log behind the first two, the ACE batch record behind the third, and the `data_product_load` and `reconciliation_result` rows the monitor shows — the Ownership Map puts all three operations on P1 rwb-source-data. **SCR-44 Interface and job monitor is the gateway-bff composite route** over those operations (DP-19, RWB-PLT-N001-CON) and is not built or rendered here: the harness calls the three operations and composes nothing of its own. The harness drives and observes only. SCR-44 states (empty, loading, error, no access): Not specified in the source documents (DOR-RWB-ITG-AD018-ITG-10).

**`v_ace_batch_status` is read only through P1's contract** (DP-05). No service and no harness opens the view, so the last complete ACE business date of a source reaches the monitor as P1's answer and never as a query. **JOB-04 Reconciliation is `ReconciliationWorkflow` in P1** (workflow ID `recon-{businessDate}`), started by `AceIngestCheck` as a child workflow after the ALS batch is stamped; rwb-source-data does not consume its own `AceDataReady` (RD-P1-040) — and **JOB-05 and its five-minute Quartz timer check are retired** in favour of durable timers inside the workflows, so no job in this story is timed by a Quartz entry and nothing here waits on a cron.

The `job_catalog` row itself stays with P2 rwb-integration in the Ownership Map (ASM-0075), and P1 reads it through `GET /api/recovery/integration/v1/admin/scheduled-jobs`. The job read and the rerun of P1 list and rerun **only the runs of rwb-source-data**: `AceIngestCheck`, `ReconciliationWorkflow` (type `JOB-04`), `Stage2ProductWorkflow` and `RetentionRunWorkflow` (RD-P1-012). Runs of other services' jobs and the outbound actions of rwb-integration are not in the P1 job read; the cross-service monitor is a gateway-bff composite over each owner's read (NEW-GAP-A1), and this run does not assert them, so **rwb-integration is not called by this story**.

### 2. Business rationale

The legacy monitor shows every Workbench job and outbound action with its status, business date, duration and checks, and beside it the last complete ACE business date of each source, so that a failed job is found and rerun the same morning and a late ACE batch is not mistaken for a failed job. The guardrail of the same story carries the half that cannot be repaired afterwards: **no ACE batch is rerun from the Workbench** — ACE ingestion owns the source runs, and the Workbench records the dependent job as WAITING. Two different mornings are written against here. On the first, a reconciliation run fails at 03:00 and nobody sees it until the officers open their queues, so the morning's cases are worked on yesterday's list. On the second, the EFS batch is late or failed, the dependent job does not run, and an administrator who reads that as a failed job reruns the ACE source batch from a Workbench button — double-loading a source that ACE still owns.

Under D-RCV-60 those facts are P1's, and the split matters because a rerun and a late batch are two different facts across two reads and one write. The job read answers what the Workbench jobs did: job ID, business date, status, duration and the result of each check. The freshness read answers what the sources delivered: the last complete ACE business date of each source and the state of the data product built from it. The rerun operation is a write that may only repeat a Workbench job that already ran. A rerun and a late batch look identical on a monitor that carries one status column and no freshness column beside it, and that is exactly the confusion the legacy acceptance criteria separate: AC2 reruns a failed job, AC3 records the dependent job as WAITING and never reruns it.

The pairing of WAITING and STALE is the whole design of the second morning. A job whose source batch is failed or has not arrived is recorded WAITING and not FAILED, because nothing has failed in the Workbench; its data product is flagged STALE with `MSG-P1-001`, which names the product and the business date the data is from, because the readers downstream have to know that what they are about to act on is not today's. A stale product that reaches a route decision as if it were fresh is the failure this story is written against: ACE data is read by every other service through rwb-source-data and never from the views (Arch v5 slide 45, "Who reads ACE's data?"), so the freshness status P1 sets (`LOADED` or `STALE`) is the only place where a route decision in rwb-valuation or a case creation in rwb-case can learn that the account facts behind it are a day old. A monitor that showed the product as fresh, or that showed the job as failed and offered a rerun, would turn a known delay into an unknown data defect.

The harness is decoupled the way the services are. Every call is one hop on the owner's base `/api/recovery/source-data/v1` with a 2 s budget (DP-11, DP-13), and ADR-020 makes that the only REST shape allowed. `v_ace_batch_status` is reached through P1's contract and never opened (DP-05), no `rwb_source_data` table is read by the harness or by any other service (DP-01), and the screen the administrator would use is the gateway-bff composite route over the same three calls (DP-19). The rerun carries one Idempotency-Key, so a repeated click replays the stored 202 answer instead of starting a second run.

Two points shape the run. The first is that the job read, the rerun and the freshness read are fixed by rwb-source-data.yaml 5.1.0 (RD-P1-005, RD-P1-012), which closes the open shapes of GAP-0440: the job list, the `Job` fields, the rerun answers and their message codes. The second is that AC3's "when the dependent job reaches its schedule" is the legacy wording of a workflow-started job: nothing waits on a cron, a run whose mapped sources are not all `COMPLETED` is recorded WAITING (RD-P1-020 E), and the harness reaches that point through the fixture's batch state. Pending: which P1 run type reads the product fed by the EFS source, and so records WAITING for the EFS batch of 2026-12-01, owner solution architect, tracked as NEW-GAP-F06-2. Release 30 June 2027 stays tentative, and a date is never a condition of this story.

### 3. Preconditions

- RWB-P1-AD018-APP is the I story that owns the deliverable: the job read, the rerun with its Idempotency-Key, the freshness read, the job log, and the WAITING and STALE behaviour of AC3. Its stub answers from Day 1 and is replaced when it lands; until then the run is reported as a stub pass.
- rwb-source-data.yaml 5.1.0 and rwb-source-data.asyncapi.yaml 5.1.0 are in the contract registry and deployed in SIT under `/api/recovery/source-data/v1` behind the gateway-bff route. The fakes are the published ones of `fakes/rwb-source-data/5.1.0/`: the job operations from RWB-P1-AD018-CON, the freshness read and the AceDataReady and AceDataLate samples from RWB-P1-E1015-CON (RD-P1-011). Their version is pinned in the run report.
- The gateway-bff composite route of SCR-44 stands on the platform story RWB-PLT-N001-CON, which DP-19 adds as an H dependency. It is a platform wave delivery that every service and the harness build against, so it is not repeated in the metadata H row of this story, which stays None; the harness calls the three P1 operations directly and does not require the route to compose them in SIT.
- SIT is in place: the task queue `rwb-source-data` in the namespace `rwb-recovery`, and the topic `rwb.source-data.events.v1` with its retry and `.dlt` topics.
- The fixture holds a synthetic job catalog, two business dates and the data products as data, not as code: the job view business date 2026-11-30 with its ACE batches `COMPLETED`, a FAILED run of type `JOB-04` on that date with its run uuid, the EFS source batch for 2026-12-01 with status FAILED, a WAITING run, one data product never stamped, and one stamped earlier whose source has no completed batch for the expected date. Run ids, business dates, batch states and products are read from the fixture and are never written in code.
- The caller set is the harness's own: `RW-PLATADM`, holding Platform administration U and R and Case record R (the right of the freshness read), as the administrator who reruns the job, and `RW-OFF`, holding no Platform administration right, as the refused caller of AC4.
- No production data is used and no production connection is opened; the suite refuses an environment that is not SIT, and release 30 June 2027 is tentative.
- This story has no build dependency, so it is ready on Day 1 under Template and Rules §R5.7. The one wait is RWB-P1-AD018-APP, which replaces its stub and never blocks the lane.
- The response shapes are those of rwb-source-data.yaml 5.1.0: `JobPage {items, page, size, total}`, `Job`, `Problem` and `DataProductFreshness` (RD-P1-004, RD-P1-005, RD-P1-012). The harness defines no shape of its own.

### 4. Flow

1. Harness: loads the fixture — the job catalog entries for business date 2026-11-30, the FAILED run of type `JOB-04` on that date, the EFS batch for 2026-12-01 with status FAILED, the WAITING run, the data products including the never-stamped one, the caller `RW-PLATADM` and the refused caller `RW-OFF`. It takes a baseline read of the job list and of the freshness list before it writes anything, opens no production connection, and refuses an environment that is not SIT.
2. Harness: reads `GET /api/recovery/source-data/v1/admin/jobs?from=2026-11-30&to=2026-11-30` and asserts one item per run ordered by `startedAt` descending, each with `id`, `type`, `businessDate`, `status`, `runNo`, `durationMinutes` and, for `JOB-04`, `checks` keyed REC-01, REC-02 and REC-05 with `expected`, `actual` and `passed`; that the FAILED run of `JOB-04` is among them; that only the four P1 run types appear; and that no field arrives outside the published contract.
3. Harness: reads `GET /api/recovery/source-data/v1/data-products/freshness` and asserts one entry per product with `productCode` and `status` (`LOADED` or `STALE`), `businessDate` (null only for a never-stamped product), and that the `lastAceBusinessDate` of the job read and the business dates of the freshness answer agree as one monitor view.
4. Harness: asserts the monitor is composed from those two reads in one hop each behind the gateway-bff route (DP-13, DP-19): the probe records the hops and the contract versions, no ACE view is opened and no `rwb_source_data` table is read (DP-01, DP-05).
5. Harness: reruns the failed run through `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun`, where `{jobId}` is the run uuid, as `RW-PLATADM` with a UUID `Idempotency-Key` and no body, and asserts 202 with a new `Job` of status PENDING and `runNo` one higher.
6. Harness: reads the job list again and asserts two runs of type `JOB-04` for 2026-11-30 — `runNo` 1 still FAILED and `runNo` 2 PENDING, RUNNING or COMPLETE — so the job log holds both.
7. Harness: repeats the same Idempotency-Key on the same path within 24 hours and asserts the stored 202 answer is replayed with the same run `id` and that the job list still holds two runs (AC2).
8. Harness: reads through P1's contract that the EFS batch for business date 2026-12-01 has not completed, sees one `rwb.source-data.AceDataLate.v1` with record key `EFS:2026-12-01` on `rwb.source-data.events.v1` and no `AceDataReady` with that key, and asserts the dependent run is recorded WAITING in the job list with no new run (AC3). Pending: which P1 run type reads the product fed by the EFS source, and so records WAITING for the EFS batch of 2026-12-01, owner solution architect, tracked as NEW-GAP-F06-2.
9. Harness: reads the freshness answer for the dependent product and asserts `status` STALE with the `businessDate` of its last stamp, and then reads the never-stamped product and asserts `status` STALE with `businessDate` null, while the other products and jobs still show in the same answer (AC3, AC5). Pending: how MSG-P1-001 reaches the monitor, as `DataProductFreshness` of rwb-source-data.yaml 5.1.0 has no message member, owner rwb-source-data contract owner, tracked as NEW-GAP-F06-3.
10. Harness: attempts to rerun the ACE source batch of 2026-12-01 through the same operation, with a uuid that is no P1 run, and asserts 404 `MSG-P4-003`, no run created and the dependent run still WAITING (AC6). An ACE batch has no run uuid in the job log, so the operation cannot address it.
11. Harness: calls `GET /api/recovery/access/v1/me/session` as `RW-OFF`, attempts the rerun and asserts 403 with `messageCode` `MSG-P4-002`, no run created and the job read unchanged run for run; then, as `RW-PLATADM`, attempts a rerun with no `Idempotency-Key` and asserts 400 with `messageCode` `MSG-PLT-N009-03` (AC4).
12. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the two runs of `JOB-04`, the WAITING run, the STALE product, the refused rerun attempts and the criteria verdicts, and restores the fixture.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | Preflight, AC1 |
| X2 | A rerun is sent with no, a blank or a non-UUID Idempotency-Key | 400 and no run is created, so a second click can never start a second run | MSG-PLT-N009-03 | AC4 |
| X3 | A rerun names a uuid that is no P1 run | 404 and no run is created; the report names the id it sent | MSG-P4-003 | AC6 |
| X4 | A rerun is attempted for an ACE source batch | The batch has no run uuid, so the attempt answers 404, no run is created and the dependent run stays WAITING | MSG-P4-003 | AC6 |
| X5 | A copy of the freshness answer is served beside the owner's, or the monitor reads a snapshot of it | The run fails on AC1 and AC5 and the report names the second source, its business date and the owner's date side by side, because a second copy of a freshness fact is the defect the story exists for | None | AC1, AC5 |
| X6 | A caller without Platform administration U attempts the rerun | The rerun is refused with 403 and the job read is unchanged run for run | MSG-P4-002 | AC4 |
| X7 | A data product has no complete ACE batch for the expected date | The product reads STALE: with the business date of its last stamp, or with `businessDate` null when never stamped | MSG-P1-001 (carrier pending, NEW-GAP-F06-3) | AC3, AC5 |
| X8 | The consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owner and no fake is put in its place | None | Preflight, AC1 |
| X9 | A consumed call exceeds the 2 s budget or returns a server error | A GET is retried once under the suite policy and recorded; the rerun POST is not retried automatically; no assertion is made on data that was not read | None | AC9 |
| X10 | A suite step tries to read `recovery.v_ace_batch_status`, `rwb_source_data` or any service schema directly | The step does not exist: the suite is built with no client for a view or a schema, and the pipeline scan fails any change that adds one | None | AC7 |
| X11 | A rerun names a run that is not FAILED, or a run of the same type and business date is PENDING or RUNNING | 409 and no run is created | MSG-P1-011 | AC10 |
| X12 | A rerun is sent while the ACE batch of the run's business date is not `COMPLETED` | 409 and no run is created | MSG-P1-001 | AC10 |
| X13 | A used Idempotency-Key is sent on another run path | 409 and no run is created | MSG-PLT-N009-05 | AC10 |

X1 to X7 are the monitor failures the legacy story is written against, re-stated on the owner's two reads and one write; X8 to X10 are the harness and cross-service failures that only appear when the run leaves one service; X11 to X13 are the refusals of the published rerun contract. Every refusal is `application/problem+json` and the message code is read from `messageCode` (RD-P1-004).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module, needs the published contract of P1 rwb-source-data and its stub from Day 1, owns no schema and no table, and never writes a job row, a batch state or a data product by hand |
| Negotiable | The fixture layout, the job IDs, the business dates, the data products, the report shape and the pass or fail gate are agreed at the wave entry check; the legacy values 2026-11-30, 2026-12-01, EFS, FAILED, MSG-P1-001 and MSG-P4-002 and the platform codes of the rerun contract are the only fixed ones |
| Valuable | Proves across the boundary what one service cannot prove: the monitor is two owner reads and no view, a failed job is rerun once and both runs are logged, a repeated key starts nothing, a late batch is WAITING and STALE rather than failed, and an ACE batch cannot be rerun from the Workbench |
| Estimable | One harness module, one fixture pack, four contract probes, one rerun driver, one stub set and one evidence report |
| Small | Can be finished in two weeks or less with its tests: nine scenarios over one service and one write; no service code, no schema change, no production flag |
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
    Then the job read answers one item per run ordered by startedAt descending, each with id, type, businessDate, status, runNo and durationMinutes, and each JOB-04 run with checks REC-01, REC-02 and REC-05
    And only runs of type AceIngestCheck, JOB-04, Stage2ProductWorkflow and RetentionRunWorkflow are listed
    And each job that reads ACE carries lastAceBusinessDate, and each product of the freshness read carries status LOADED or STALE with its businessDate
    And no ACE view is opened and no rwb_source_data table is read by the harness or by any other service

  Scenario: AC2 A failed Workbench job is rerun once and both runs are in the job log (new, D-RCV-60)
    Given the run of type "JOB-04" with run uuid "00000000-0000-4000-8000-000000000018" is in the job list for business date "2026-11-30" with status FAILED and runNo 1
    Given the ACE batch for "2026-11-30" is COMPLETED and no run of type "JOB-04" for that date is PENDING or RUNNING
    When RW-PLATADM posts /api/recovery/source-data/v1/admin/jobs/00000000-0000-4000-8000-000000000018/rerun with no body and Idempotency-Key "9f2c6b1a-3d47-4e8a-9c10-5b7e2a4d8f31"
    Then the answer is 202 with a new Job of type "JOB-04", businessDate "2026-11-30", status PENDING and runNo 2
    And the job list holds two runs, runNo 1 still FAILED and runNo 2 PENDING, RUNNING or COMPLETE
    And the same Idempotency-Key repeated on the same path within 24 hours replays the stored 202 answer with the same run id and creates no third run

  Scenario: AC3 A late ACE batch (legacy RWB-AD-018 AC3)
    Given the rwb-source-data contract fake (§12.8) answers that the EFS source batch for business date "2026-12-01" has status "FAILED"
    When the dependent job reaches its schedule
    Then the job is recorded WAITING and is not rerun
    And its data product shows STALE with MSG-P1-001

  Scenario: AC4 A caller without Platform administration U is refused and no run is created (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" whose role holds no Platform administration U
    When the caller reruns the failed job through POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun
    Then the answer is 403 with a problem body whose messageCode is "MSG-P4-002"
    And no run is created and the job read is unchanged, run for run
    When RW-PLATADM sends the same rerun with no Idempotency-Key header
    Then the answer is 400 with messageCode "MSG-PLT-N009-03" and no run is created

  Scenario: AC5 A data product whose freshness is unknown is never shown as fresh (new, D-RCV-60)
    Given the freshness read carries one data product that was never stamped and one whose source has no completed batch for the expected business date but was stamped for an earlier date
    When the monitor reads those two products
    Then the never-stamped product answers status STALE with businessDate null
    And the earlier-stamped product answers status STALE with the businessDate and loadedAt of its last stamp
    And neither product answers status LOADED
    And the other products and jobs still show in the same answers

  Scenario: AC6 An ACE source batch is never rerun from the Workbench (new, D-RCV-60)
    Given the EFS source batch for business date "2026-12-01" is FAILED
    When RW-PLATADM posts /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun with the uuid "00000000-0000-4000-8000-0000000000ee", which is no P1 run, for that batch
    Then the answer is 404 with a problem body whose messageCode is "MSG-P4-003"
    And no operation of the contract accepts a source system or an ACE batch as the thing to rerun
    And the dependent job stays WAITING, no run is created and no ACE batch is started

  Scenario: AC7 A suite step cannot read the ACE view or a service schema directly (new, D-RCV-60)
    Given the suite is built with no client for recovery.v_ace_batch_status, rwb_source_data or any other service schema
    When the pipeline scans a change that adds a direct read of one of them
    Then the scan fails that change and no step reads the view or the schema

  Scenario: AC8 JOB-04 is a child of the ingest check and JOB-05 is not in the monitor (new, D-RCV-60, RD-P1-040)
    Given the job list for business date "2026-11-30" is read through P1's job read
    When the harness checks the jobs in that answer
    Then the reconciliation run has type "JOB-04" and workflowId "recon-2026-11-30", the child that AceIngestCheck starts after the ALS stamp
    And no item has type "JOB-05" and no CaseListBuildWorkflow run is listed

  Scenario: AC9 A consumed call that fails or does not answer is retried once and never asserted on (new, D-RCV-60)
    Given a consumed call to P1's contract exceeds the 2 s budget or returns a server error
    When the harness makes the call under the suite retry policy
    Then a GET is retried once and the evidence report records the retry
    And a rerun POST is not retried automatically, and any manual repeat of it carries the same Idempotency-Key
    And no assertion is made on data that was not read

  Scenario: AC10 A rerun the published contract refuses creates no run (new, RD-P1-012)
    Given a run with status COMPLETE, and a FAILED run whose ACE batch for its business date is not COMPLETED
    When RW-PLATADM posts a rerun of the COMPLETE run with a new Idempotency-Key
    Then the answer is 409 with messageCode "MSG-P1-011"
    When RW-PLATADM posts a rerun of the second run with another new Idempotency-Key
    Then the answer is 409 with messageCode "MSG-P1-001"
    When the Idempotency-Key accepted in AC2 is sent on another run path
    Then the answer is 409 with messageCode "MSG-PLT-N009-05"
    And the job list holds the same runs after the three calls as before them
```

AC3 is the legacy criterion, copied word for word. In it, STALE is the `status` of the freshness read, and WAITING is the `status` of the dependent run in the job read; the harness asserts both against the fake until the dependent run type is named. Pending: which P1 run type reads the product fed by the EFS source, and so records WAITING for the EFS batch of 2026-12-01, owner solution architect, tracked as NEW-GAP-F06-2. Pending: how MSG-P1-001 reaches the monitor, as `DataProductFreshness` of rwb-source-data.yaml 5.1.0 has no message member, owner rwb-source-data contract owner, tracked as NEW-GAP-F06-3. AC1 and AC2 are the business outcome RWB-P1-AD018-APP has to reach and are asserted here across the service boundary; AC4 to AC6 and AC10 are the new scenarios the split makes assertable, because the right, the refusal and the guarantee that an ACE batch is never rerun from the Workbench are properties of the seam and not of one service.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Every Workbench job shows its job ID, business date, status, duration and the result of each check, and each job that reads ACE shows the last complete ACE business date of its source | RWB-AD-018 AC1 | AC1 |
| BR2 | A failed Workbench job is rerun from its run book after the cause is fixed, and both runs are in the job log | RWB-AD-018 AC2 | AC2 |
| BR3 | A late or failed ACE batch leaves the dependent job recorded WAITING and not rerun, and its data product STALE with MSG-P1-001 | RWB-AD-018 AC3 | AC3 |
| BR4 | **No ACE batch is rerun from the Workbench**: ACE ingestion owns the source runs, and the Workbench records the dependent job as WAITING | RWB-AD-018 guardrail; Architecture v5 slide 32 (Airflow runs the ACE ingestion DAG and says the business date is ready) | AC6 |
| BR5 | **A late batch is WAITING, not failed**: WAITING is the state of a job whose source has not delivered, FAILED is the state of a run that ran and failed, and only the second may be rerun | RWB-AD-018 AC2 and AC3; the guardrail of the same story | AC3, AC6 |
| BR6 | `v_ace_batch_status` is read only through rwb-source-data's contract, and no service opens the view or reads another service's table | DP-05, DP-01; RWB-AD-018 guardrail; Architecture v5 slide 41 (P1 owns the ACE view contract and freshness) | AC1, AC7 |
| BR7 | The freshness of a data product is P1's single fact: the last complete ACE business date of its source and the state of the product are answered once and never copied | DP-05; Architecture v5 slide 41; Architecture v5 slide 45 (only rwb-source-data reads the 30 ACE views) | AC1, AC5 |
| BR8 | JOB-04 is `ReconciliationWorkflow`, started by `AceIngestCheck` as a child workflow after the ALS stamp, and JOB-05 is retired, so no job in the monitor is timed by a Quartz entry | RD-P1-040; Architecture v5 slide 44; ADR-016 | AC8 |
| BR9 | Every call in the run is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s timeout, and the composite path the screen uses is the gateway-bff route | DP-11, DP-13, DP-19; ADR-020 | AC1, AC9 |
| BR10 | A rerun is of a FAILED run only, keyed by run uuid, with no body and a UUID Idempotency-Key; it answers 202 and a replay returns the stored answer; the right to rerun is Platform administration U | RD-P1-001; RD-P1-012; RWB-AD-018 permission checks | AC2, AC4, AC10 |

The harness asserts these rules and changes none of them. The job run, the job log, the batch record and the data product are P1's, the right is taken from the platform session and enforced by P1 with MSG-P4-002 on refusal, and the values in the table are the legacy ones. The run status is a closed set of five values, PENDING, RUNNING, COMPLETE, FAILED and WAITING, one row per attempt; the freshness answer is served by P1 rwb-source-data and owned by RWB-P1-E1015-CON, with no field of it restated.

### 9. State transitions

| Subject | From | Event | Condition | To | Owner of the change |
|---|---|---|---|---|---|
| Job run | FAILED | RERUN_REQUESTED | the caller holds Platform administration U, the ACE batch of the run's business date is COMPLETED, no run of the type and date is PENDING or RUNNING, and a UUID Idempotency-Key is sent | a new run PENDING, `runNo` + 1; the FAILED run is unchanged | P1 rwb-source-data, `POST /admin/jobs/{jobId}/rerun` |
| Job run | RUNNING | RUN_COMPLETED | every check of the run passes | COMPLETE | P1 rwb-source-data |
| Job run | RUNNING | RUN_FAILED | a check of the run fails | FAILED | P1 rwb-source-data |
| Job run | PENDING | SOURCE_BATCH_NOT_COMPLETE | a source mapped to a product the run reads is not COMPLETED | WAITING | P1 rwb-source-data, the job runner (RD-P1-020 E) |
| Job run | WAITING | SOURCE_BATCH_COMPLETED | every mapped source is COMPLETED | RUNNING | P1 rwb-source-data, the job runner |
| Data product | LOADED | STALE_CHECK | no stamp for the expected date at the product's `expected_by`, or a source of the product reads FAILED | STALE; MSG-P1-001 | P1 rwb-source-data, `data_product_load` (RD-P1-041) |
| Data product | LOADED or STALE | SOURCE_BATCH_COMPLETED | every source of the product is COMPLETED for the date | LOADED, a new stamp for that date | P1 rwb-source-data |

The job states are the status the job read answers, and the data product state is the freshness the freshness read answers; neither is written by the harness. The WAITING state is the one the legacy story calls "waiting for the ACE batch" on SCR-44, and it is deliberately not a failure: a run that failed may be rerun, a job that is WAITING may not, which is why the two states sit in different columns of the run report. The fixture carries two business dates for one job: the reconciliation job `JOB-04` has a FAILED run on 2026-11-30, which the run reruns, and a run for 2026-12-01 that stays WAITING while the EFS batch is FAILED. The harness changes no state; every row above is made by P1 through its own operation or its own check, and a state the harness set by hand would prove nothing.

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
| DF-OPS-224 to DF-OPS-232 | job_catalog | id, job_id, job_name, owner_role, schedule_text, expected_minutes, alert_after_minutes, first_release | P1 lists the Workbench jobs it owns from its own job map and the ACE batch record; a catalog field is read through P2 rwb-integration's contract only (ASM-0075), never by table or schema |
| DF-OPS-001 to DF-OPS-008 | data_product_load | id, product_code, source_system, business_date, loaded_at, status, stale_flagged_at | Read through P1's freshness read; STALE and MSG-P1-001 are asserted there |
| DF-ACE-178 to DF-ACE-186 | v_ace_batch_status | source_system, business_date, started_at, completed_at, status, record_count and 3 more | Read only through P1's contract (DP-05); never `recovery.v_ace_batch_status` directly and never from a schema |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | Results of REC-01 and REC-02 | Not read directly: the run sees them only as the `checks` of the `JOB-04` run in P1's job read |
| DF-OPS-233 onwards (`job_run`, `job_run_check`; RD-P1-020) | job_run, job_run_check (P1) | job_type, business_date, run_no, status, started_at, finished_at, duration_minutes, rerun_of_id; one check row per check code | Read through P1's job read only; never read from a schema |
| Not applicable | outbound_item (P2) | The outbound action rows | Not read and not asserted: the P1 job read lists P1 runs only (RD-P1-012); the cross-service monitor is outside this run (NEW-GAP-A1) |

Field IDs are those in the Logical Data Model and Data Dictionary v9, and the three entities of the legacy data table are the job catalog, the data product load and the ACE batch status. The job catalog row stays with P2 rwb-integration in the Ownership Map, while the job read served by P1 lists the runs of the jobs P1 owns and a catalog field is read through P2 rwb-integration's contract only; the data product load and the reconciliation result are P1's, and the ACE batch status reaches the monitor only as P1's answer. The harness owns no table and writes no row: the two runs of `JOB-04` are created by the owner's rerun operation, and the WAITING run is written by the owner's job runner and the STALE product by `AceIngestCheck`. Every key in the run is synthetic, and no field in the table carries personal data. Reference data: lists and parameters are read only through the published reference-data contract (DP-06, DP-07), and the parameter names are Not specified in the source documents (DOR-RWB-ITG-AD018-ITG-20). Until P1 publishes the answer schemas, the answer fields are Not specified in the source documents (GAP-0440); once they are published, the harness asserts each answer field by field from the published contract.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/admin/jobs` | P1 rwb-source-data | `JobPage` of P1 runs, query `type`, `status`, `from`, `to`, `page`, `size` (default 50, maximum 200); `from` and `to` default to the last 7 days, so the run sends them (AC1, AC2, AC3, AC5, AC8) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Reruns a FAILED run by run uuid, no body, header `Idempotency-Key`; 202 `Job`; 400 MSG-PLT-N009-03, 403 MSG-P4-002, 404 MSG-P4-003, 409 MSG-P1-011, MSG-P1-001 or MSG-PLT-N009-05, 503 MSG-GEN-006 (AC2, AC4, AC6, AC10) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | `DataProductFreshness[]`: `productCode`, `status` (LOADED or STALE), nullable `businessDate`, `sourceExtractedAt`, `loadedAt`, `staleSince`; needs Case record R (AC1, AC3, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a rerun (AC4) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13), and no operation is invented in this story: each path is the owner's published operation in the Ownership Map. The map also publishes `GET /api/recovery/source-data/v1/admin/data-products` and `GET /api/recovery/source-data/v1/admin/data-contracts` on P1; this run calls neither, because the freshness of a product is read from the freshness operation, which is the one the monitor uses. Where a screen would compose the three calls the path is the gateway-bff composite route (DP-19), and SCR-44 is that route rather than a service operation.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record. In particular it never publishes `AceDataReady`, `AceDataLate` or a batch-ready signal of its own, because the ACE ingestion and the freshness check are P1's and the whole point of AC3 and AC6 is that the Workbench does not cause a source run.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Record key `{sourceSystem}:{businessDate}`, `ce_subject` = sourceSystem; data `sourceSystem`, `businessDate`, `status`, `completedAt`. One per source system and business date once COMPLETED; counted at zero for key `EFS:2026-12-01` (AC1, AC3) |
| `rwb.source-data.AceDataLate.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Same key and data, `completedAt` null where no batch completed. Published at most once per source and business date, at once for a FAILED batch, else at 05:30; counted once for `EFS:2026-12-01` (AC3) |

The harness subscribes to the topic under one consumer group of its own and counts publications. While the stub answers, the two counts are read from the stub's recorded publications and the report says so; with the real P1 in place they are counted on `rwb.source-data.events.v1`. Nothing is replayed: the paths exercised here are single-shot reads and one rerun, and a replay would test P1's inbox rather than the monitor.

#### 12.5 Workflows and activities

None added. The harness observes two workflows on the task queue `rwb-source-data`, both stated in Architecture v5 slide 15 as P1's: **`AceIngestCheck`**, the workflow that checks the freshness of the sources and decides whether a business date is delivered, and **`ReconciliationWorkflow`** (activity `reconciliation`, JOB-04), which `AceIngestCheck` starts as a child workflow after the ALS stamp; it waits for the rwb-case allocation until `caselist.allocation.wait.until` (RD-P1-040). It observes them through their effects — the WAITING job and the STALE product on the two reads — and never reads a workflow history, so the run asserts the monitor and not the execution. No workflow, activity, worker or Schedule is created, changed or owned here.

#### 12.6 Schedules

None added. The monitor is a read composition and a rerun, so nothing in this story is on a cron; JOB-05 and its five-minute Quartz timer check are retired in favour of durable timers inside the workflows, and JOB-04 is started by `AceIngestCheck` as its child rather than by a schedule (RD-P1-040) (Architecture v5 slide 44; Temporal design slide 32, "jobs as Schedules", no Quartz). The harness moves no schedule, starts no job timer and asserts no cron.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): `job_catalog` stays with P2 rwb-integration (ASM-0075), `data_product_load` and `reconciliation_result` are P1's, `v_ace_batch_status` is an ACE view read only by P1, and `outbound_item` is P2's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| `fakes/rwb-source-data/5.1.0/` (RWB-P1-AD018-CON, RWB-P1-E1015-CON) | `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun`, `GET /data-products/freshness`, AceDataReady and AceDataLate samples | The job list with the FAILED `JOB-04` run, then two runs after the 202 and after the replayed key; the WAITING run for 2026-12-01; freshness with a LOADED, a STALE and a never-stamped product; 400, 403, 404, 409 and 503 problem bodies with the codes of §14 |
| Stub for rwb-access | `GET /me/session` | Allows `RW-PLATADM` with Platform administration U and R; refuses `RW-OFF` with 403 and MSG-P4-002 |
| Stub for the gateway-bff composite route | The SCR-44 route over the three P1 operations | Answers one composite read of the monitor by calling the two reads once each, so the hop count of AC1 can be asserted while the route itself is not built here |
| Job and batch fixture | The job catalog entries, the business dates, the ACE batch states and the data products | The FAILED `JOB-04` run on 2026-11-30; the EFS batch for 2026-12-01 at status FAILED with its AceDataLate; the WAITING run and the STALE product; one never-stamped product; all held as data behind the rwb-source-data fake, never set in an ACE view |
| Stub for rwb-integration | `GET /admin/scheduled-jobs` | Consumed by rwb-source-data for the job metadata, not by the harness; used where the real P1 runs before rwb-integration is live |

Each fake is generated from the published contract of its owner and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The consumed versions are rwb-source-data.yaml 5.1.0 and rwb-source-data.asyncapi.yaml 5.1.0.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 4 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.source-data.AceDataReady.v1` counted once per source system and business date and `rwb.source-data.AceDataLate.v1` counted once for key `EFS:2026-12-01` |
| Temporal | None added; `AceIngestCheck` and `ReconciliationWorkflow` on `rwb-source-data` observed through the WAITING job and the STALE product |
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
| FreshnessProbe | Service | Reads `GET /data-products/freshness`, records `status`, `businessDate` and `loadedAt` per product, asserts STALE for the dependent product, and asserts that a never-stamped product answers STALE with `businessDate` null and is never LOADED |
| RerunDriver | Service | Drives `POST /admin/jobs/{jobId}/rerun` with the run uuid as `RW-PLATADM` with a UUID Idempotency-Key, replays it, drives the 404 and 409 refusals, and records status, `messageCode` and the run `id` |
| BatchStatusProbe | Service | Asserts the EFS batch of 2026-12-01 at status FAILED through P1's contract only, and that the dependent job is WAITING with no new run |
| SessionProbe | Service | Reads `GET /me/session`, confirms the caller's Platform administration rights, and holds the `RW-OFF` refusal |
| StubSet | Fake | The two stubs, the composite-route stub and the job and batch fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per business date keyed by story, with the two runs side by side, the WAITING job, the STALE product, the refused batch, the contract version of each hop, whether the hop was a stub or the owner, and the gate |

**Environment and test data.** SIT, against the stub from Day 1 and the real P1 as RWB-P1-AD018-APP lands, on business dates 2026-11-30 and 2026-12-01, the reconciliation job `JOB-04`, the EFS source batch, the data products including one never stamped, the caller `RW-PLATADM` and the refused caller `RW-OFF`. The harness seeds nothing by hand, never writes a job row, a batch state or a data product, and refuses an environment that is not SIT. Response shapes and message codes are those of rwb-source-data.yaml 5.1.0. Until RWB-P1-AD018 is released there is no P1 rerun operation (NEW-ASM-X4).

**Build steps**

1. Generate the three stubs and the job and batch fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1, X8).
2. Build the JobListProbe and assert AC1's job fields for business date 2026-11-30, including the FAILED run of `JOB-04`.
3. Add the FreshnessProbe for the other half of AC1: the last complete ACE business date of each source, one hop per read, and the hop record that proves no view and no schema was opened (X5, X10).
4. Build the RerunDriver and rerun the FAILED run by its uuid with one Idempotency-Key; assert 202, `runNo` 2 and two runs in the job log (AC2).
5. Add the replayed-key step and assert the stored 202 answer and no third run; add the missing-key step and assert 400 MSG-PLT-N009-03 and no run (X2); add the three 409 refusals of AC10 (X11 to X13).
6. Add the BatchStatusProbe and the WAITING path of AC3: the EFS batch FAILED for 2026-12-01 through P1's contract, the run WAITING, no new run, one AceDataLate and zero AceDataReady counted for key `EFS:2026-12-01` (NEW-GAP-F06-2 names the run type).
7. Add the STALE and never-stamped paths of AC3 and AC5: `status` STALE with the last stamp's `businessDate`, and STALE with `businessDate` null for the never-stamped product, while the other products still show (X7).
8. Add the batch-refusal path of AC6: a rerun with a uuid that is no P1 run answers 404 MSG-P4-003, no run is created and the dependent run stays WAITING (X3, X4).
9. Add the SessionProbe and the refusal of AC4: 403 with MSG-P4-002, no run created, and the job read unchanged run for run (X6).
10. Add the EvidenceReport gate and swap the stub for rwb-source-data as RWB-P1-AD018-APP lands, reporting a stub pass as a stub pass.

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-AD018-APP when it lands, and the wave entry check holds a run report keyed by story and business date with the two runs of the job, the WAITING job and the STALE product side by side.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-PLT-N009-03 | Error (400) | Platform code: Idempotency-Key missing, blank or not a UUID (RD-P1-001) |
| MSG-PLT-N009-05 | Error (409) | Platform code: key reused with another request or in flight |
| MSG-P1-011 | Error (409) | Run is not FAILED, or a run of the same type and date is open (text in the Error and Message Standard) |
| MSG-P4-003 | Error (404) | Unknown run or a run that is not a P1 run (text in the Error and Message Standard) |
| MSG-GEN-006 | Error (503) | Store unavailable (text in the Error and Message Standard) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the status and `messageCode` of the problem body (RD-P1-004) and owns no message text. MSG-P1-001 is asserted on the 409 of a rerun whose ACE batch is not COMPLETED (AC10); on the freshness side the harness asserts `status` STALE (AC3, AC5). Pending: how MSG-P1-001 reaches the monitor, as `DataProductFreshness` of rwb-source-data.yaml 5.1.0 has no message member, owner rwb-source-data contract owner, tracked as NEW-GAP-F06-3. MSG-PLT-N009-03 is asserted when a rerun is sent without its Idempotency-Key (step 11, X2), MSG-P4-002 for `RW-OFF` (step 11, AC4), and MSG-P4-003 for a rerun naming no P1 run (step 10, X3, X4). The legacy MSG-GEN-001 for a missing key is replaced by MSG-PLT-N009-03 (RD-P1-001).

### 15. Screens and states

SCR-44 Interface and job monitor is the legacy screen with the states Running, failed, waiting for the ACE batch and complete, and it is not built or rendered here: the harness calls the two reads and the rerun behind it and composes nothing of its own. The screen is the gateway-bff composite route over the calls of §12.2 (DP-19), and no screen, route or user-interface element is created, changed or tested by this story. The gateway-bff route is registered and its alerts set by RWB-P1-AD018-OPS, RWB-P1-AD018-APP serves the reads and RWB-P1-AD018-CON publishes them. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0440; ASM-0632). The alert thresholds, panel baselines, channel names, replica counts, resource sizes and retention of the monitor are held per environment in the values file and confirmed with the operations owner at the wave 4 readiness review; the 15-minute alert target of NFR-068 is kept.

| State | Read through | What the run asserts |
|---|---|---|
| Running | P1 job read | The second run of `JOB-04` is RUNNING with its own business date and `durationMinutes` null, while the first run stays FAILED beside it |
| Failed | P1 job read | The first run of `JOB-04` on 2026-11-30 is FAILED with the check result that failed, and a rerun is what may follow it |
| Waiting for the ACE batch | P1 job read and freshness read | The dependent run of 2026-12-01 is WAITING with no new run, and its data product reads `status` STALE, so the state is a wait and not a failure |
| Complete | P1 job read | Where the fixture's second run completes, the run shows COMPLETE with its duration and every check passing, and the job still carries both runs |
| Pending | P1 job read | The new run of a rerun answers PENDING in the 202; what the screen shows for it is Not specified in the source documents (GAP-2163) |
| A refused rerun | rwb-access session read and the rerun answer | 403 MSG-P4-002, 404 MSG-P4-003 or a 409 of AC10, no run created and the job read unchanged |
| Empty | Not specified in the source documents (CG-ALL-954) | Not specified in the source documents (CG-ALL-954) |
| Loading | Not specified in the source documents (CG-ALL-954) | Not specified in the source documents (CG-ALL-954) |
| Error | Not specified in the source documents (CG-ALL-954) | Not specified in the source documents (CG-ALL-954) |
| No access | Not specified in the source documents (CG-ALL-954) | Not specified in the source documents (CG-ALL-954) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-018-01-ITG | AC1 | Integration | The job list and the freshness list for business date 2026-11-30, read once each through P1's operations behind the gateway-bff route, with the hop record and the contract version |
| TC-AD-018-02-ITG | AC2, AC6 | Integration | The FAILED `JOB-04` run, one rerun with one Idempotency-Key, the replayed key, a uuid that is no P1 run, and the job list read before and after each attempt |
| TC-AD-018-03-ITG | AC3, AC5 | End to end | The EFS batch of 2026-12-01 at status FAILED, the dependent job WAITING, its product STALE with MSG-P1-001, and a product whose freshness is unknown beside it |
| TC-AD-018-04-ITG | Access; AC4 | Component | A synthetic caller `RW-OFF` without Platform administration U, the rerun refused with 403 MSG-P4-002, and a rerun sent without its Idempotency-Key answering 400 MSG-PLT-N009-03 |
| TC-AD-018-05-ITG | AC7; BR6 | Not specified in the source documents (NEWAC-RWB-ITG-AD018-ITG-AC7) | A pipeline scan of a change that adds a direct read of `recovery.v_ace_batch_status`, `rwb_source_data` or another service schema |
| TC-AD-018-06-ITG | AC8; BR8 | Not specified in the source documents (NEWAC-RWB-ITG-AD018-ITG-AC8) | The job list for business date 2026-11-30 read through P1's job read, with JOB-04 and JOB-05 checked in the answer |
| TC-AD-018-07-ITG | AC9; X9 | Not specified in the source documents (NEWAC-RWB-ITG-AD018-ITG-AC9) | A consumed call of P1 that exceeds the 2 s budget or returns a server error, under the suite retry policy |
| TC-AD-018-10-ITG, TC-AD-018-01-ITG, TC-AD-018-02-ITG, TC-AD-018-04-ITG, TC-AD-018-08-ITG, TC-AD-018-03-ITG, TC-AD-018-09-ITG, TC-AD-018-06-ITG, TC-AD-018-07-ITG | AC10, and the changed assertions of AC1, AC2, AC4, AC5, AC6, AC8, AC9 | Integration | Values of section 7 |

The legacy test cases TC-AD-018-01 to TC-AD-018-04 are kept as the `-ITG` copies above, with their legacy Covers: AC1 for TC-AD-018-01, AC2 for TC-AD-018-02, AC3 for TC-AD-018-03 and Access for TC-AD-018-04. The full legacy tests, with their Given, When and Then, are in the legacy test case workbook under the same legacy IDs. Legacy AC1 and AC2 stay the build criteria of RWB-P1-AD018-APP and legacy AC3 stays the criterion of that story too; the `-ITG` copies assert the same behaviour across the service boundary, AC5 has no legacy test case of its own in this key and is folded into TC-AD-018-03-ITG, and AC6 is asserted with the batch-refusal steps of TC-AD-018-02-ITG.

### 17. Guardrails

- No business value in code: the job IDs, the business dates 2026-11-30 and 2026-12-01, the batch states, the data products, the caller keys and the report layout are data held in the fixture.
- No personal data in logs, events or reports: every key is synthetic, the events carry IDs and facts only, and no case, party or account field is read by this story.
- ACE data only through the owner's contract: the batch status is read through P1's operation and never from `recovery.v_ace_batch_status`, and no `rwb_source_data` table or any other service's table or schema is opened (DP-01, DP-05).
- One hop and a 2 s budget per call, with a breaker per downstream, so the harness fails where the screen would (DP-11, DP-13, ADR-020).
- No invented operation: only the three P1 operations and the session read of §12.2, at rwb-source-data.yaml 5.1.0,, and no freshness, job or batch fact is asserted through a read the map does not publish.
- No ACE batch is rerun from the Workbench: the harness never publishes `AceDataReady`, never signals a business date ready and never drives an ACE ingestion path, and the refusal of AC6 is asserted as a failure of the run if a batch run is created.
- SIT only: the suite refuses any other environment, opens no production connection and uses no production data.
- No schema read and no hand-set state: the job run, the WAITING job and the STALE product are made by the owner, and the suite is built with no client for a view or a schema.
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script, and a job shown FAILED when its source simply has not delivered is a failure and not a variant.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-AD-018 Interface and job monitor | Recovery Workbench Administration Stories v3, lines 1465 to 1548 | Sections 1, 2, 3, 11, 14 and 19 of this file |
| Legacy AC3, verbatim | The same, lines 1495 to 1499 | Section 7, AC3, marked (legacy RWB-AD-018 AC3) |
| Legacy AC1 and AC2 | The same, lines 1484 to 1493 | Section 7, AC1 and AC2, asserted here across the boundary; the criteria themselves stay with RWB-P1-AD018-APP (section 19) |
| Legacy guardrail, no ACE batch rerun from the Workbench | The same, line 1548 | Sections 1, 2, 8 (BR4, BR5) and 17 |
| Legacy test cases TC-AD-018-01 to TC-AD-018-04, with Covers AC1, AC2, AC3 and Access | The same, lines 1539 to 1546 | Copied as `-ITG` in section 16 |
| Legacy data entities and field IDs: job_catalog, data_product_load, v_ace_batch_status | The same, lines 1502 to 1508 | Section 11 |
| Legacy endpoints, screen, permission checks and messages | The same, lines 1510 to 1537 | Sections 12.2, 15, 10 and 14 |
| The P1 service row: ACE view contract, extension tables, freshness, reconciliation; schema rwb_source_data | Architecture v5 slide 41, text extract line 2884 | Sections 1, 2, 11 and 12.7 |
| The P1 contract: `GET /freshness`, the workflows `AceIngestCheck` and `reconciliation`, the freshness and reconciliation writes, the `AceDataReady` and `AceDataLate` topic | Architecture v5 slide 15, text extract lines 1075 to 1081 | Sections 2, 12.4 and 12.5 |
| The ACE batch ready call, the 05:30 and 07:00 SLA alerts, `AceDataLate` at 05:30, and `AceDataReady` starting JOB-04 (the in-service start is the child workflow of RD-P1-040) | Architecture v5 slide 32, text extract lines 2292 to 2294 | Sections 2, 4 and 9 |
| Event catalogue #26 `AceDataReady` and #27 `AceDataLate` | Architecture v5 slide 43, text extract lines 2952 and 2953 | Section 12.4 |
| JOB-04 reconciliation as an event-triggered workflow on rwb-source-data, and JOB-05 retired in favour of durable timers | Architecture v5 slide 44, text extract lines 2980 and 2981 | Sections 1, 2, 8 (BR8) and 12.6 |
| "Who reads ACE's data?" — only rwb-source-data reads the 30 views, everyone else asks it through REST or an activity | Architecture v5 slide 45, text extract line 3016 | Sections 2 and 8 (BR7) |
| Jobs as Temporal Schedules, no Quartz | Temporal and Drools design slide 32, text extract line 2134 | Section 12.6 |
| Ownership Map v1 table rows for job_catalog, data_product_load, reconciliation_result and outbound_item | Ownership Map v1, with ASM-0075 for the job catalog row | Sections 1, 11 and 12.7 |
| Ownership Map v1 API rows for `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun`, `GET /data-products/freshness`, `GET /admin/data-products` and `GET /me/session` | The same | Section 12.2 |
| DP-05, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application, and the metadata Patterns applied row |
| ADR-016 and ADR-020 | Architecture Decision Records v4, with ADR-016 and ADR-020 as added by Template and Rules v1 §R8.4 | Sections 8, 12.2 and 12.6: Schedules replace Quartz, contract-first REST with one hop and 2 s |
| GAP-0440 and ASM-0632 | Closed and changed by RD-P1-012: job read, rerun answer (202), job list per run and job-log fields | Sections 2, 3, 5, 7, 12 and 14 |
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

### Remaining delivery steps

- Size the story at refinement (squad).
- Epic design sign-off (solution architect).
- Build and release RWB-P1-AD018-APP and publish the AD018-CON and E1015-CON fakes at 5.1.0 (rwb-source-data squad).
- Name the run type that records WAITING for a failed EFS batch (solution architect, NEW-GAP-F06-2).
- Rule how MSG-P1-001 reaches the monitor (rwb-source-data contract owner, NEW-GAP-F06-3).
- Load the synthetic fixture in SIT (test data owner).
- Add the test case rows for AC10 and the changed assertions in Test Cases v9 and the Requirements Traceability Matrix (test writer).
