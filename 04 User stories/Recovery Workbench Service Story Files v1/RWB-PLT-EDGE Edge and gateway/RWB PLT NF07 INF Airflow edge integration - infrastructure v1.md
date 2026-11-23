# RWB-PLT-NF07-INF Airflow edge integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-NF07-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-EDGE |
| Wave | 0 |
| Business epic | NF |
| Release | None (new story) |
| Legacy key | NF-07 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-EDGE-D |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform story for the edge between the bank's Airflow scheduler and Recovery, moved from legacy NF-07 with no impact on the behaviour of the chain. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **platform team that runs the edge between the bank's scheduler and Recovery**, I want **the bank's Airflow to reach Recovery only through published REST APIs with a dedicated workload identity, and to run the cross-system overnight chain, the two file windows, the report extracts and the cutover and backfill through those APIs**, so that **the schedule keeps working after the split without any database job, schema read or shared credential, and the case list is still ready by 07:00**.

This is the edge story of legacy key NF-07 under epic RWB-PLT-EDGE. The behaviour of the legacy key is moved with no impact: the overnight chain, the 16:00 WIN file window, the debt-buyer file window per lot, the report extracts and the cutover and backfill runs all stay as they are. What changes is the edge itself. In the monolith these steps ran as jobs inside the application, on the application's own database connection. In the target, the bank's Airflow sits outside the AKS cluster (Architecture v5 slide 9) and reaches Recovery only through the published REST operations of the owning services, with a workload identity and no schema access.

The story covers:

- The network path and the identity by which Airflow reaches Recovery, and the rule that no other path is opened.
- The four call groups: the business-date-ready call to rwb-source-data followed by the wait for DailyCaseRun; the WIN 16:00 and debt-buyer file windows at rwb-integration; the report extracts at rwb-reporting; the cutover and backfill calls to the owning services.
- The idempotency, timeout, retry and alerting rules of those calls, and the runbook.
- The negative proof: Airflow holds no database login, produces no Kafka record, reads no `rwb_*` table and reaches no pod directly.

The scheduler is shared platform and not one of the 19 services: it owns no schema, no topic and no task queue, and per-case work stays in Temporal. This story creates no business table, publishes no event and runs no workflow; it has no build dependency and starts on Day 1.

### 2. Business rationale

The overnight chain is the clock the whole Workbench runs on. The case list must be on screen by 07:00 on the latest completed ACE batch (NFR-013), the daily rebalancing must be complete before the working day starts (NFR-019), and the WIN registered-mail window opens at 16:00 (Architecture v5 slide 16). Today those steps are jobs inside one application, so they can reach the database directly and nobody has to agree how an external scheduler is identified. After the split that shortcut is exactly the boundary the realignment forbids: one schema and one login per service, and no component outside a service reads its tables (DP-01, DP-02).

This story removes the shortcut without changing the business clock. Airflow keeps the cross-system chain, because the bank is moving from Control-M to Airflow and the chain spans systems that no single service owns (Architecture v5 slide 5). It calls the owning service's API instead of the database: rwb-source-data for the business date and the freshness of each data product, rwb-integration for the two file windows, rwb-reporting for the extracts, and the owning services for cutover and backfill. Every POST carries an `Idempotency-Key`, so a retried task cannot create a second run; a late batch delays the chain and raises an alert and never starts a Workbench load (NFR-015).

The story also protects the service SLOs. A scheduler that holds a database connection can starve a service's capped pool; a scheduler that calls an API consumes a bounded request and a 2 s timeout like any other client. That is what keeps the 07:00 commitment and the 16:00 window credible without giving the scheduler privileges inside any schema.

### 3. Preconditions

- The scheduler placement is fixed by Architecture v5 slide 9: Airflow is the bank's enterprise scheduler, replacing Control-M, it sits outside the cluster, and it calls Recovery APIs only and never reads `rwb_*` schemas.
- The five duties of the chain are fixed by the same note: (1) the ACE ingestion DAG; (2) the last task tells rwb-source-data the business date is ready and then waits for DailyCaseRun; (3) it opens the WIN and debt-buyer file windows; (4) it triggers report extracts in rwb-reporting; (5) it runs cutover loads and backfills.
- The owner operations named by the architecture are fixed: rwb-source-data accepts `POST /business-days/{date}/ready` from Airflow and serves `GET /freshness`; rwb-reporting accepts `POST /reports/{id}/run` from Airflow; rwb-integration owns the WIN window at 16:00 and the buyer files per lot (Architecture v5 slides 15, 16 and 20).
- The REST contract rules are fixed: OpenAPI 3.1 with `/v1` in the path, a user JWT from the BFF plus workload identity, a 2 s timeout, a GET retried once with jitter, an `Idempotency-Key` on every POST and RFC 9457 problem details (Architecture v5 slide 11).
- The no-load rule is fixed: the Workbench runs no inbound load; work starts when ACE records the batch for that source and business date as complete in `v_ace_batch_status` (Program BRD, section 6.3 note; NFR-015).
- The availability and recovery targets that apply to the chain are fixed: 99.9 percent in business hours, 99.5 percent outside them, with the RPO and RTO following the ACE recovery objectives (NFR-020 to NFR-023).
- The exact scheduler product, version and tenancy, the DAG names, the identity method, the timeout and retry values, the wait mechanism for DailyCaseRun and the file-window operation are Not specified in the source documents (GAP-1396; ASM-2432); section 13 carries the assumption that is in force until the scheduling design review.
- No approval is required to start: the story is Draft (realignment v1) and the settings are frozen at the scheduling design review before wave 0 exit.

### 4. Flow

1. The platform team provisions the path: a dedicated service principal for Airflow in each environment, the network route to the shared App Gateway, the HTTP connection with its secret reference and the certificate trust, and the alert route to the platform on-call rota.
2. The ACE ingestion DAG runs outside Recovery and loads the source systems into the ACE database. Recovery takes no part in it and reads nothing from it directly.
3. The last task of that DAG calls `POST /api/recovery/source-data/v1/business-days/{date}/ready` on rwb-source-data with an `Idempotency-Key` built from the environment, the business date and the run id, and with the workload identity in the token.
4. The DAG then waits for DailyCaseRun, which runs on the rwb-case task queue as a Temporal Schedule started by the business-date-ready fact. The wait is bounded; when DailyCaseRun does not reach a terminal state inside the bound, the DAG task fails and alerts.
5. At 16:00 the WIN window DAG calls rwb-integration to open the registered-mail file window; the debt-buyer window runs per lot when a lot is awarded. Each call carries the business date, the interface and the lot where one applies, and an `Idempotency-Key`, so a second task for the same window returns the first result instead of opening a second one.
6. The report-extract DAG calls rwb-reporting to run each extract with the business date; a repeat for the same date and report returns the first run.
7. The cutover and backfill DAGs call the owning services' published operations only, in business-date order, and are started by hand with a named approver.
8. Every call is traced with the run id, the DAG id, the task id and the business date; a failed call is retried with backoff, and after three failures the run stops, alerts and stays resumable from the failed task.
9. The evidence for the run is the service's own record and trace, not a scheduler log line: Airflow holds no copy of the data and no business value beyond the identifiers it passes.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | The ACE batch for the source and business date is late or failed | The chain does not start the dependent task; the case list shows the last completed business date and the alert names the source and the date | MSG-PLT-NF07-02 |
| X2 | The business-date-ready call fails after its retries | The run stops at that task, alerts the platform on-call rota, and is resumed from the same task after the cause is cleared; the repeat call is safe because of the `Idempotency-Key` | MSG-PLT-NF07-01 |
| X3 | DailyCaseRun does not reach a terminal state inside the wait bound | The waiting task fails, alerts, and the next run does not start a second DailyCaseRun for the same business date | MSG-PLT-NF07-01 |
| X4 | The 16:00 window is missed, or the call is refused | The window call is retried; if it is still refused, the run alerts and the missed window is recorded on the interface, and rwb-integration's own exception path takes over | MSG-PLT-NF07-01 |
| X5 | A task repeats after a partial success (a duplicate ready call or a duplicate extract run) | The owner returns the first result; no second run, no second file and no second extract is created | MSG-PLT-NF07-03 |
| X6 | The workload identity expires, is revoked or is used from an unapproved network | The call is refused with 401 or 403 and the run alerts; the credential is rotated and the run resumed | MSG-PLT-NF07-01 |
| X7 | A backfill or cutover run is started without the named approver | The run is refused before its first call; cutover and backfill are the only manual runs and they carry an approval record | MSG-PLT-NF07-01 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions the path, the identity and the runbook; it builds no service behaviour and needs no service to be finished |
| Negotiable | Product, DAG names, timeout and retry values and the wait mechanism are open until the scheduling design review |
| Valuable | The overnight chain, the 16:00 window and the 07:00 case list keep working after the split, without a database job |
| Estimable | One service principal, one connection, four call groups, one wait, one runbook |
| Small | One sprint for the path, the four call groups and the negative tests |
| Testable | Each criterion is an integration or NFR assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Airflow edge integration for the cross-system chain

  Background:
    Given Airflow is the bank's enterprise scheduler and sits outside the AKS cluster
    Given the Recovery services are reached only through their published REST operations

  Scenario: AC1 Airflow reaches Recovery only through published REST APIs with a workload identity (new, D-RCV-60)
    Given the Airflow service principal and the network path of this story
    When the path is tested from the scheduler
    Then every call answers on the published /api/recovery/<service>/v1 operation of the owning service
    Then Airflow holds no database login, opens no connection to the ACE PostgreSQL server and reads no rwb_* table
    Then Airflow produces no Kafka record and reaches no pod or service address directly
    Then a call from another identity, another network range or without a token is refused with 401 or 403

  Scenario: AC2 The business-date-ready call is idempotent and the DAG waits for DailyCaseRun (new, D-RCV-60)
    Given the last task of the ACE ingestion DAG for a business date
    When it calls POST /api/recovery/source-data/v1/business-days/{date}/ready with an Idempotency-Key
    Then rwb-source-data accepts the call once and the repeat for the same business date returns the first result with no second run
    Then the DAG waits for DailyCaseRun to reach a terminal state before the next task starts
    Then the wait is bounded and a wait that exceeds the bound fails the task and alerts
    Then a late or failed ACE batch delays the chain and raises an alert, and starts no Workbench load (NFR-015)

  Scenario: AC3 The two file windows are opened through rwb-integration (new, D-RCV-60)
    Given the WIN window at 16:00 and the debt-buyer window per lot
    When each window task calls rwb-integration
    Then the call carries the business date, the interface and the lot where one applies, and an Idempotency-Key
    Then a repeat of the same window returns the first result and opens no second window
    Then a missed or refused window is retried, alerted and recorded on the interface, and rwb-integration's exception path takes over

  Scenario: AC4 Report extracts and cutover or backfill runs use the published operations (new, D-RCV-60)
    Given the report-extract DAG and the cutover and backfill DAGs
    When they call rwb-reporting and the owning services
    Then each extract run carries the business date and is idempotent per business date and report
    Then cutover and backfill run only with a named approver and an approval record, in business-date order
    Then no run writes to a service schema directly or reuses another service's operation

  Scenario: AC5 Every call is bounded, retried, traced and alerted to a named owner rota (new, D-RCV-60)
    Given a call that is slow, refused or failing
    When the timeout is reached
    Then the call is retried with backoff up to the configured limit, and after three failures the run stops, alerts and stays resumable from the failed task
    Then every run is traceable by run id, DAG id, task id, business date and the owning service's trace
    Then no DAG parameter, log line or payload carries a customer name, an account number or any personal data

  Scenario: AC6 The runbook covers rerun, backfill and cutover, and the chain meets the 07:00 and 16:00 commitments (new, D-RCV-60)
    Given the runbook and the rehearsed runs
    When an operator follows it for a rerun, a backfill and a cutover
    Then each step names the role that performs it, the call it makes, the expected result and the check that proves it
    Then a rehearsed run shows the case list available by 07:00 on the latest completed ACE batch and the WIN window open at 16:00 (NFR-013, NFR-019)
    Then the runbook holds no credential and no personal data, and it is stored with the platform runbooks
```

These six criteria are new and test only the deliverable in the title: the edge path, the identity, the four call groups, the failure handling and the runbook. The behaviour of legacy key NF-07 is moved with no impact and no legacy acceptance criterion is repeated here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Airflow calls Recovery APIs only: no database login, no schema read, no Kafka producer, no direct pod access | Arch v5 slide 9 note; DP-01, DP-02 |
| BR2 | Airflow sits outside the cluster and enters through the shared App Gateway with a dedicated workload identity per environment | Arch v5 slides 8, 9 and 11 |
| BR3 | Every POST carries an `Idempotency-Key`; a repeat returns the first result and creates no second run, file or extract | Arch v5 slide 11 |
| BR4 | Per-case work stays in Temporal; Airflow runs the cross-system chain, the file windows, the extracts and the cutover and backfill | Arch v5 slide 9; DP-10 |
| BR5 | A late ACE batch delays the chain and alerts; it never starts a Workbench load, catch-up job or staging table | NFR-015 |
| BR6 | No personal data appears in a DAG parameter, a log line, a trace attribute or a call payload; identifiers and business dates only | Arch v5 slide 35; Template and Rules §R7.2 s17 |
| BR7 | Every call has a bounded timeout and retries with backoff; three failures stop the run, alert the platform on-call rota and leave the run resumable | NFR-025, NFR-026 read at the edge |
| BR8 | The chain succeeds when the case list is available by 07:00 on the latest completed ACE batch and the WIN window opens at 16:00 | NFR-013, NFR-019; Arch v5 slide 16 |

### 9. State transitions

None in the services: this story changes no business state and approves nothing. What it has is the run state of a DAG task, described here so that the tests of AC2 to AC5 have something to assert.

| From | Event | Condition | To |
|---|---|---|---|
| Created | The DAG run starts | The business date is set and the identity is valid | Running |
| Running | The business-date-ready call succeeds | rwb-source-data accepted the call or returned the first result | Waiting for DailyCaseRun |
| Waiting for DailyCaseRun | DailyCaseRun reaches a terminal state | Inside the wait bound | Succeeded for that task |
| Waiting for DailyCaseRun | The wait bound is reached | DailyCaseRun is still running | Failed, with an alert |
| Running or Waiting for DailyCaseRun | A call fails | The retries are exhausted | Failed, then Retried from the same task |
| Failed | The operator resumes after the cause is cleared | The repeat call is idempotent | Running |
| Running | The operator stops the run | A named approver records the reason | Cancelled, and the next run starts from the business date that is not yet complete |
| Succeeded for that task | The next task starts | The business date is unchanged | Running |

The transition owner is the Airflow runtime, not a Recovery service. The cutover and backfill runs are the only manual transitions and they carry an approval record. The exact wait mechanism and the exact retry values are Not specified in the source documents (GAP-1396; ASM-2432).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns this story, the service principal, the connection, the DAG wiring and the runbook |
| The bank's scheduling team | Owns the Airflow tenancy, the DAG runtime and the ingestion DAG; admits the Recovery DAGs into it |
| ACE platform team | Owns the App Gateway, the network path and the certificate trust; admits the scheduler's address range |
| Security architecture | Approves the identity method, the network path, the secret handling and the no-schema-access boundary |
| The owner of rwb-source-data | Publishes the business-date-ready and freshness operations; confirms the idempotency of the ready call |
| The owner of rwb-integration | Publishes the file-window call and owns the window exception path |
| The owner of rwb-reporting | Publishes the extract-run operation and confirms its idempotency per date and report |
| Platform on-call rota | Receives the alerts and runs the runbook |
| Cutover and backfill approver | Approves a manual run and records the reason; no delegation of authority level applies, because this is an operational run and not a credit decision |

The scheduler product, version and tenancy, the DAG names, the identity method, the timeout and retry values, the wait mechanism and the file-window operation are Not specified in the source documents (GAP-1396; ASM-2432). They are agreed at the scheduling design review and section 13 carries the assumption in force until then.

### 11. Data

| Item | Value |
|---|---|
| Values passed | Business date, environment, run id, DAG id, task id, report id, interface id and lot id where one applies |
| Values never passed | A customer name, a national identifier, an account number, a document body, a decision outcome or any other business value |
| Data stored at the edge | The run record and the task log of the scheduler; no business data, no copy of a file and no extract output |
| Data read from Recovery | The API response of each call; the scheduler does not read a database, a topic or a blob directly |
| File content | The file itself never travels through the scheduler: rwb-integration writes it and rwb-document or the buyer channel holds it, and the scheduler passes only the interface, the business date and the lot |
| Retention of the run record | The scheduler's own retention in the bank's platform; it is not a business record and it holds identifiers only |
| Personal data | None in a DAG parameter, a log line, a trace attribute or a payload |
| Credential | The service principal secret or certificate in the platform vault, read by the Airflow connection; never in a DAG file, an image or a log |

The exact payload of the file-window call and the exact wait contract of DailyCaseRun are Not specified in the source documents (GAP-1396; ASM-2432); the calls carry identifiers and the business date only, and the payload is fixed at the owner's contract review.

### 12. Contract

**12.1 REST operations provided**

None. Recovery provides no new operation for this story: the scheduler consumes operations owned by rwb-source-data (P1), rwb-integration (P2) and rwb-reporting (P9). The edge itself is not a service and publishes no path of its own.

**12.2 REST operations consumed**

| Operation | Provider | Why this story needs it | Pattern |
|---|---|---|---|
| POST /api/recovery/source-data/v1/business-days/{date}/ready | rwb-source-data (P1) | The last task of the ACE ingestion DAG tells rwb-source-data the business date is ready | DP-11 |
| GET /api/recovery/source-data/v1/data-products/freshness | rwb-source-data (P1) | The chain and the runbook read which source and business date are complete before a dependent task starts | DP-05, DP-11 |
| POST /api/recovery/reporting/v1/reports/{reportId}/run | rwb-reporting (P9) | The report-extract DAG triggers an extract for the business date | DP-11 |
| The rwb-integration file-window call that opens the WIN 16:00 window and the debt-buyer window per lot | rwb-integration (P2) | The two fixed-window file transfers run through rwb-integration | DP-11, DP-16 |

Architecture v5 slides 9, 15, 16 and 20 name these calls and the callers. The Ownership Map has a row for `GET /data-products/freshness` (P1) but no row for the business-date-ready call, the extract-run call or the file-window call; the providers above are the services the architecture gives the capability, and the exact path and payload of each are Not specified in the source documents (GAP-1396; ASM-2432). Each call is made once per business date, carries an `Idempotency-Key` when it is a POST, and follows the REST contract of Architecture v5 slide 11.

**12.3 Events published**

None. The scheduler publishes no business event. The business-date-ready fact becomes a Temporal start of DailyCaseRun inside rwb-case; the scheduler holds no topic and no producer.

**12.4 Events consumed**

None. Airflow consumes no Kafka event; it calls the API and waits. A service that reacts to an event reacts inside its own consumer group, not at the edge.

**12.5 Workflows and activities**

None in this story. The per-case and business workflows stay in Temporal on the owner's task queue (`rwb-case` for DailyCaseRun, `rwb-integration` for the file activities, `rwb-reporting` for the extract activity); the scheduler is a client of the API and never a worker, and DP-10 is not applied to this legacy key.

**12.6 Schedules**

The scheduler is Airflow, outside the cluster; it is not a Temporal Schedule and this story creates none. The chain it runs is:

| Run | Trigger | What it does | Owner of the work |
|---|---|---|---|
| ACE ingestion DAG | Overnight, outside Recovery | Loads the source systems into the ACE database; Recovery takes no part | The bank's scheduling team with ACE |
| Business date ready and wait | Last task of the ingestion DAG | Calls rwb-source-data, then waits for DailyCaseRun | This story, with rwb-source-data and rwb-case |
| WIN file window | 16:00 each business day | Opens the registered-mail window through rwb-integration | This story, with rwb-integration |
| Debt-buyer file window | Per lot, when a lot is awarded | Opens the buyer-file window through rwb-integration | This story, with rwb-integration |
| Report extracts | The bank's reporting timetable | Triggers each extract through rwb-reporting | This story, with rwb-reporting |
| Cutover and backfill | One-off, approved | Calls the owning services' published operations in business-date order | This story, with the owning services |

The boundary is the one Architecture v5 slide 9 draws: the scheduler runs the cross-system chain, the file windows, the extracts and the one-off loads; business schedules that belong to a service (case creation, allocation, rebalancing, rule promotion, write-off scan, retention) stay in that service's Temporal Schedule under DP-10 and never move into Airflow.

**12.7 Tables owned**

None. The scheduler owns no `rwb_*` table, no view and no login. It reads no table of any service and it creates no staging table, because the Workbench runs no inbound load (NFR-015).

**12.8 Contract fakes**

None. This story adds no service contract and therefore no fake; the tests of section 16 run against the owner fakes published by the rwb-source-data, rwb-integration and rwb-reporting contract stories, and against a scheduler test instance with the same connection and identity settings as production.

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 4 call groups (business date, freshness, extract run, file window) | Published owner operations only, workload identity, `Idempotency-Key` on every POST, bounded timeout and retry |
| Kafka | 0 | 0 | The scheduler never produces or consumes an event |
| Temporal | 0 | 0 | It waits for DailyCaseRun; it does not start a workflow and is not a worker |
| File | 0 direct | 2 windows opened through rwb-integration | The WIN window at 16:00 and the buyer window per lot; the file bytes never pass through the scheduler |

### 13. Solution plan

**Deliverables.** The Airflow service principal and its credential reference, the network route and the certificate trust, the HTTP connection profile, the four DAG task groups with their operators and `Idempotency-Key` templates, the wait task for DailyCaseRun, the retry and alert configuration, the cutover and backfill DAGs with their approval gate, the dashboard panel for the chain, the runbook, and the test evidence of section 16.

**Settings in force**

| Setting | Value |
|---|---|
| Scheduler | The bank's Airflow, outside the AKS cluster; the product, version and tenancy are Not specified in the source documents (GAP-1396; ASM-2432) |
| Identity | One service principal per environment, OAuth 2.0 client credentials, with a token audience of the shared App Gateway |
| Network path | From the scheduler's approved range to the shared App Gateway only; no route to the ACE PostgreSQL server and none to a pod address |
| Call style | REST over HTTPS, one hop, 2 s service timeout, 60 s task timeout, three retries with exponential backoff and jitter |
| Idempotency | `Idempotency-Key` = environment + business date + run id (+ report id or lot id where one applies) on every POST |
| Wait for DailyCaseRun | A bounded poll of the case service's run status every 60 s; the exact mechanism is Not specified in the source documents (GAP-1396; ASM-2432) |
| Alerting | Three failed retries, a wait that exceeds its bound, a missed window and a refused credential all alert the platform on-call rota |
| Secrets | In the platform vault, read by the Airflow connection; rotation tested once |
| Approval gate | Cutover and backfill runs require a named approver and an approval record before the first call |
| Tracing | Run id, DAG id, task id, business date, owning service and the service trace id, with no personal data |
| Runbook | Provision, run, rerun, resume, backfill, cutover, rotate and break-glass, each step with its role |

**Pattern application.** None of the decoupling-pattern markers of Template and Rules §R5.5 appears in this platform story: it introduces no legacy table, no legacy login, no legacy topic name, no legacy task queue and no legacy API base, so no DP row is applied and the metadata row "Patterns applied" reads None. The patterns the chain does exercise are applied by the stories that own them: DP-01 and DP-02 by every service schema and login, DP-10 by the Temporal Schedules that replace the Quartz jobs, DP-11 by the REST contract with a mock, DP-16 by the rwb-integration contract for the file windows, and DP-19 by the gateway-bff route the scheduler's calls pass through.

**Build steps**

1. Create the service principal per environment, write the credential to the platform vault, and grant it only the owner operations of section 12.2.
2. Open the network path from the scheduler's range to the shared App Gateway; prove that the database host and the pod range are unreachable from the scheduler.
3. Build the HTTP connection with the certificate trust, the timeout and the retry policy, and the `Idempotency-Key` template.
4. Build the business-date-ready task and the wait task, with the bound and the failure path of X3.
5. Build the two file-window tasks and the extract-run tasks, each idempotent per business date.
6. Build the cutover and backfill DAGs behind the approval gate.
7. Turn on the run record, the trace and the dashboard panel, and route the alerts to the platform on-call rota.
8. Run the negative tests: no token, another identity, another network range, a repeat ready call, a repeat extract, a refused window, an expired credential.
9. Rehearse a full chain in the test environment against the owner fakes, then against the services in SIT; record the time the case list becomes available and the time the window opens.
10. Rehearse a rerun, a resume from a failed task, a backfill and a cutover; time them, write the runbook and hand over.

**Done when.** The scheduler reaches every owner operation through the gateway with its own identity, all five negative tests fail closed, a full chain runs green in SIT with the case list available by 07:00 and the 16:00 window open, the rerun, resume, backfill and cutover are rehearsed and documented, and the dashboard and the alerts are live on the platform rota.

### 14. Validation and messages

| ID | When | Message | Raised to |
|---|---|---|---|
| MSG-PLT-NF07-01 | A call fails after its retries, or the wait for DailyCaseRun exceeds its bound | The {dag} task {task} for business date {date} failed at {service}: {reason}. The run is held at this task and can be resumed. | Platform on-call rota |
| MSG-PLT-NF07-02 | The ACE batch for a source and business date is late or failed | The {source} batch for {date} has not completed. The chain is held and the case list keeps the last completed business date. | Platform on-call rota and the data steward |
| MSG-PLT-NF07-03 | A task repeats after a partial success | The {operation} for business date {date} was already accepted. The first result is returned and no second run is created. | The run record only |

The three identifiers are new for this platform story; they are technical run messages and carry no business value. The calls they describe keep the message identifiers of the owner services when an owner refuses a call, and the scheduler never rewrites an owner message.

### 15. Screens and states

No screen in this story. The visible effects are the case list being available by 07:00 on the latest completed ACE batch, the freshness of each data product shown on the case list, and the WIN window opening at 16:00. The scheduler's own UI is the bank's Airflow UI and is not in the scope of the Workbench; the run state of section 9 is what an operator sees there, and the runbook is what they follow.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-NF07-INF-01 | AC1 | Integration | The scheduler's identity and network path; calls to all four owner operations; negative tests with no token, another identity and another range; an assertion that the database host and the pod range are unreachable |
| TC-PLT-NF07-INF-02 | AC2 | Integration | A business date D; one ready call and its repeat; the wait for DailyCaseRun with a terminal and a timed-out case; a late ACE batch |
| TC-PLT-NF07-INF-03 | AC3 | Integration | The WIN window at 16:00 and a buyer window for one lot; one call and its repeat; a refused window and its alert |
| TC-PLT-NF07-INF-04 | AC4 | Integration | One extract for business date D and its repeat; a cutover run with and without the approval record; a backfill in business-date order |
| TC-PLT-NF07-INF-05 | AC5 | Component | A slow call, a refused call and a failing call; three retries with backoff; the alert and the resume from the failed task; a trace with run, DAG, task and business date |
| TC-PLT-NF07-INF-06 | AC6 | NFR | A rehearsed full chain in SIT: the time the case list becomes available against 07:00, the time the window opens against 16:00, and the rerun, backfill and cutover timings |
| TC-PLT-NF07-INF-07 | AC5 | NFR | A personal-data scan of the DAG parameters, the run record, the logs and the trace attributes; a secret scan of the DAG files and the connection profile |

### 17. Guardrails

- The scheduler calls APIs only: no database login, no schema read, no Kafka producer and no direct pod access, and the path is tested from the outside.
- No business value is hard-coded in a DAG: the business date, the interface, the report and the lot are parameters, and every reference value stays with its owner.
- No personal data in a DAG parameter, a log line, a trace attribute or a payload; identifiers and business dates only.
- Every POST carries an `Idempotency-Key`, so a retried task can never create a second run, file or extract.
- Every call is bounded and retried with backoff, and three failures stop the run and alert a named rota rather than looping silently.
- No Workbench load window and no staging table: a late ACE batch delays the chain and alerts (NFR-015).
- Per-case work stays in Temporal; the scheduler never starts a case workflow and never becomes a worker.
- The credential lives in the platform vault, is rotated, and never appears in a DAG file, an image or a log.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| NFR-013 | The case list is available by 07:00 on the latest completed ACE batch, and every case list states the business date and load time of the batches behind it | Program, 6.3 | None | R-UNI-01 | TC-PLT-NF07-INF-02, TC-PLT-NF07-INF-06 |
| NFR-015 | The Workbench holds no load window; a late ACE batch delays the case list and raises an alert rather than starting a load | Program, 6.3 | None | None | TC-PLT-NF07-INF-02 |
| NFR-019 | The daily rebalancing job completes before the working day starts, by 07:00 | Program, 6.3 | None | None | TC-PLT-NF07-INF-02, TC-PLT-NF07-INF-06 |
| NFR-025 | A system of record outage queues the outbound action and retries on a schedule, and does not lose it | Program, 6.4 | None | None | TC-PLT-NF07-INF-05 |
| NFR-026 | An interface failure after the retry limit moves the item to an exception queue with a task for a named owner | Program, 6.4 | None | None | TC-PLT-NF07-INF-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-N001-CON | Contract | The edge route contract the scheduler's calls pass through |
| RWB-PLT-N001-APP | App development | The gateway that admits the scheduler's identity and applies the timeout and the problem details |
| rwb-source-data contract story (service epic RWB-SVC-P1) | Contract | Publishes the business-date-ready and freshness operations this story consumes |
| rwb-integration contract story (service epic RWB-SVC-P2) | Contract | Publishes the file-window call and owns the window exception path (DP-16) |
| rwb-reporting contract story (service epic RWB-SVC-P9) | Contract | Publishes the extract-run operation this story consumes |
| RWB-PLT-N007-INF | Infrastructure | The partner edge; partners never use the scheduler's path |

### 19. Out of scope

- The ACE ingestion DAG itself and the ACE batch: ACE owns the load and the batch-status record.
- The Temporal business schedules that replace the Quartz jobs: case creation, allocation, rebalancing, rule promotion, write-off scan and retention stay with their services (DP-10).
- The owner services' operations, payloads and data: rwb-source-data, rwb-integration, rwb-reporting and the other owners publish them in their own contract stories.
- The WIN and debt-buyer interfaces themselves, the file formats and the transfer channel: rwb-integration owns them.
- The scheduler product, tenancy and upgrade: the bank's scheduling team owns them.
- The cutover plan and the business sign-off of a cutover or a backfill: the cutover plan owns them, and this story only provides the approved runs.
- Any screen, any business rule and any business value.
