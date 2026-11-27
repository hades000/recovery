# RWB-P1-AD019-OPS Data quality and reconciliation console

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-AD019-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP10, DP19 |
| Parallel lane | L-P1-C |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: deployment side of the split of RWB-AD-019 for rwb-source-data: the api deployment with the reconciliation result read, the JOB-04 worker on the workflow kit, the gateway-bff route registration for SCR-45, the feature flag `rwb.source-data.reconciliation-run`, the four alert rules, the dashboard and the health checks, the runbook and the rollback (DP05, DP10, DP19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-AD019-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer of rwb-source-data**, I want **the api deployment that serves the reconciliation result read and the worker deployment that runs the JOB-04 reconciliation, the gateway-bff route registration for SCR-45, the feature flag that stops the run and falls the read back to the last completed business date, four alert rules on the run, a dashboard with the health of the read and the worker, a runbook and a rollback**, so that **a break, an orphan, a held case list and a stale data product are seen by the people who must act on them, and a run that goes wrong is stopped and rolled back without changing a row**.

This story deploys what RWB-P1-AD019-APP builds and registers the route the console slice RWB-P3-AD019-APP does not own. It builds no code, no endpoint, no table, no workflow and no screen of its own.

- **The api deployment** serves `GET /api/recovery/source-data/v1/admin/reconciliation/results` (API-P1-003, Platform administration R) on the service base, behind gateway-bff, with the health and readiness probes of the service template.
- **The worker deployment** polls task queue `rwb-source-data` in namespace `rwb-recovery`, registers `ReconciliationWorkflow` with its four activities, and starts the run on `rwb.source-data.AceDataReady.v1`. It creates no Schedule and no job table: the run is event-started and its record is the Temporal visibility record (ASM-0714).
- **The route registration** publishes SCR-45 on gateway-bff as the composite route of RWB-PLT-N001-CON, composed over the three console reads of rwb-case (DP-19). The route calls no operation of rwb-source-data directly; the reconciliation read is reached through rwb-case.
- **The feature flag** `rwb.source-data.reconciliation-run` stops the run when it is off and falls the read back to the last completed business date, with no redeploy.
- **The four alert rules**, the dashboard and the health checks make the run and the read observable; **the runbook and the rollback** make a failure recoverable.

### 2. Business rationale

A break, an orphan or a held case list is only worth computing if someone is told. RWB-P1-AD019-APP writes the result rows, lists the orphans and holds the case list of a date; RWB-P3-AD019-APP renders them on SCR-45. Neither of them deploys, registers a route, watches a queue or wakes a person at the right hour. That is this story.

The legacy arrangement had the opposite problem: the console read an extract and the scheduler console of a shared job table, so the operational picture of the reconciliation lived in the same console as the schedule, and a failed run was a row in a table nobody watched (legacy RWB-AD-019 "Endpoints"; Architecture v5 slide 44). In the target the run is a Temporal workflow and its failures, retries and durations are the platform's own record, so the alerts can be built on the queue and the visibility queries instead of on a table this service would have to write (ASM-0714).

Four operational facts drive the deliverables. **First**, the read is the only surface a caller sees, so the route, the flag and the probes are its controls. **Second**, a held case list is a business event, not only a log line: MSG-P1-012 names the date, the product, the variance and the percent, and the people who receive it are configuration, not code (BR-P1-013). **Third**, a stale data product is E1015's answer and this story only alerts on it, so the alert carries the product and its last complete business date and claims no freshness of its own (MSG-P1-001). **Fourth**, a break never changes a row: the runbook says so before the first rollback step, so nobody repairs a schema or a case while the ACE team is fixing the source (legacy RWB-AD-019 guardrails).

The alert thresholds and the on-call routing are configuration of the platform alert library and of the operations channel, and they are not business values of this story: no number is fixed here beyond the four rules and their fields.

### 3. Preconditions

- RWB-PLT-E1071-CON is published: the Temporal workflow kit, the `rwb-recovery` namespace, the worker deployment template of the service chart, the visibility query and the alert hook of a failed workflow (DP-10).
- RWB-PLT-N001-CON is published: the gateway-bff route contract, with the composite route template, the per-call budget and the error mapping used to register SCR-45 (DP-19).
- RWB-P1-AD019-APP is the story deployed here: the read `GET /admin/reconciliation/results`, `ReconciliationWorkflow` with `runRec01`, `runRec02`, `resolveRec05` and `writeReconciliationResult`, and the consumed `AceDataReady`. Its images carry the read and the worker; this story configures and deploys them.
- RWB-P3-AD019-APP publishes the three console reads behind SCR-45, so the route registered here has owners to call. A route registered before those reads exist answers its per-block error state and is not a failure of this story.
- The platform flag library is available to the chart and to the pods, with the flag `rwb.source-data.reconciliation-run` declared for the service (platform library, default ruling of Template and Rules section R3).
- The platform alert library and the operations channel exist, with the four rule templates of section 13 and the routing groups named by configuration.
- The `rwb_source_data` login and its key-store secret reference exist, so the api and the worker read the views and write their own tables without a credential in a chart value, an image or a log.
- No build dependency: the story is Day 1 by rule, because its H field is None (Template and Rules section R5.7). It deploys images produced by RWB-P1-AD019-APP, and a deployment of an older image is a deployment of an older read, never a partial one.

### 4. Flow

1. Pipeline: build and scan the api image and the worker image of rwb-source-data; the images are the artefact of RWB-P1-AD019-APP and carry no credential.
2. Pipeline: run the chart lint and the environment values check: schema `rwb_source_data`, task queue `rwb-source-data`, namespace `rwb-recovery`, the key-store secret reference and the flag entry per environment.
3. Deployment: apply the api deployment, which serves the read on base `/api/recovery/source-data/v1` and answers its health and readiness probes.
4. Deployment: apply the worker deployment on the same task queue, with the workflow and activity registrations of `ReconciliationWorkflow`; the worker starts no Schedule and writes no job-run table.
5. Deployment: wait for the readiness of both deployments before the flag is switched on in the environment.
6. Route: register SCR-45 on gateway-bff as the composite route of RWB-PLT-N001-CON over the three console reads of rwb-case, with the session check, the short-lived token and the per-call budget of the contract.
7. Flag: with `rwb.source-data.reconciliation-run` on, a consumed `AceDataReady` starts the run; with it off, the event is consumed and the run is not started, and the read serves the last completed business date.
8. Alerts: the four rules of section 13 watch the run and the read, and each one names the business date, the product group or the orphan count and the run, so a recipient knows what to open.
9. Observability: the dashboard shows runs by business date, the result per check and product group, the orphan count, the hold state and the freshness of DP01 as E1015 answers it; the probes show the views, the queue polling and the inbox lag.
10. Runbook: how to read a break from the reconciliation read, how to read an orphan, who to call for an ACE row, and that a break never changes a row and is never repaired in this service.
11. Rollback: redeploy the previous api and worker images and the previous route version, leave the flag off while the run is being withdrawn, and keep every `reconciliation_result` row already written, because the migrations are forward only (ADR-021).
12. Evidence: one deployment record per environment with the image digests, the route version, the flag state, the four alert rules and the probe results.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The key-store secret reference of the login cannot be read | The pods do not start, the deployment fails and the failure is logged without the secret | None | AC1 |
| X2 | The worker cannot reach the Temporal namespace | The worker stops polling, readiness turns not ready and the queue backlog is on the dashboard; no run is lost, because the event stays in the inbox and the workflow starts when polling resumes | None | AC1, AC5 |
| X3 | The reconciliation read fails behind the route | The console block shows its own error state and the other blocks show; the alert names the operation and the environment, not a person | None | AC3 |
| X4 | A run ends FAILED | The failed-run alert fires with the business date, the activity and the run, and the runbook step for a view or a parameter failure is opened | MSG-GEN-006 as the run's own message | AC4 |
| X5 | A case list is HELD for a business date | The hold alert fires with the date, the product group, the variance and the percent, to the groups named by configuration | MSG-P1-012 | AC4 |
| X6 | A data product is past its expected business date | The stale alert fires with the product and its last complete business date, as E1015 answers it; this story stamps nothing | MSG-P1-001 | AC4 |
| X7 | The REC-05 orphan count of a business date is above the configured level | The orphan alert fires with the count, the date and the run; the orphans themselves are read from the reconciliation read | None | AC4 |
| X8 | The flag is switched off while a run is in flight | The run in flight completes or is terminated by the workflow kit policy, no new run starts, and the read falls back to the last completed business date | None | AC3 |
| X9 | A rollback is taken while a run is in flight | The previous images are redeployed, in-flight runs are drained or terminated by the kit, the rows already written stay, and no migration is reversed | None | AC6 |
| X10 | A route version is registered against a read that the environment does not have | The route answers its error state and the deployment record names the missing read; the previous route version is restored | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Configures and deploys the images, the chart, the route, the flag, the alert rules, the dashboard, the probes, the runbook and the rollback of one service |
| Negotiable | The alert thresholds, the routing groups and the dashboard panels are configuration agreed with the operations owner; the four rules and their fields are fixed |
| Valuable | A break, a hold, a stale product and an orphan count reach a person, and a bad run is stopped and rolled back without touching a row |
| Estimable | One chart change, one route registration, one flag entry, four alert rules, one dashboard, one runbook and one rollback test |
| Small | Fits one sprint with its two tests |
| Testable | Each criterion runs in a pipeline against an environment with the platform kit, the route contract and the alert library |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the reconciliation read and the JOB-04 worker

  Background:
    Given the images of the reconciliation read and the JOB-04 worker are built from RWB-P1-AD019-APP
    Given the platform workflow kit, the gateway-bff route contract and the platform flag and alert libraries are available

  Scenario: AC1 The read and the worker are deployed and ready (new, D-RCV-60)
    Given the chart values of the environment with schema rwb_source_data, task queue rwb-source-data and namespace rwb-recovery
    When the api deployment and the worker deployment are applied
    Then the api deployment serves GET /api/recovery/source-data/v1/admin/reconciliation/results and answers its health and readiness probes
    And the worker deployment polls task queue rwb-source-data and registers ReconciliationWorkflow with its four activities
    And the worker creates no Temporal Schedule and writes no job-run table
    And no credential appears in a chart value, an image or a log, because the login is a key-store secret reference

  Scenario: AC2 SCR-45 is registered as the composite route of the console (new, D-RCV-60)
    Given the gateway-bff route contract RWB-PLT-N001-CON and the three console reads of rwb-case
    When the SCR-45 route is registered
    Then the route is the composite route over the three console reads, with the per-call budget of the contract
    And the route calls no operation of rwb-source-data directly, and this service publishes no screen route
    And a route that calls the reconciliation read directly fails the route test

  Scenario: AC3 The flag stops the run and falls the read back (new, D-RCV-60)
    Given the flag rwb.source-data.reconciliation-run in the platform flag library
    When the flag is off and AceDataReady is consumed
    Then no run starts for the business date and the event is recorded as consumed with the run not started
    And the read serves the last completed business date
    When the flag is on and AceDataReady is consumed
    Then the run starts for the business date and the read serves the date asked for
    And the flag is changed with no redeploy of the api or the worker

  Scenario: AC4 The four alert rules fire and name what to open (new, D-RCV-60)
    Given the four alert rules: job failed, stale data product, case list held and REC-05 orphan count above configuration
    When each condition is reached in the environment
    Then the matching rule fires to the routing groups named by configuration
    And the failed-run alert names the business date, the activity and the run
    And the stale alert names the product and its last complete business date as E1015 answers it
    And the hold alert names the date, the product group, the variance and the percent
    And the orphan alert names the count, the date and the run, and carries no business key and no personal data

  Scenario: AC5 The dashboard and the probes show the run and the read (new, D-RCV-60)
    Given the dashboard of the service and the health and readiness probes
    When a business date has run, held or not started
    Then the dashboard shows the runs by business date, the result per check and product group, the orphan count, the hold state and the freshness of DP01 as E1015 answers it
    And the probes show the reachability of the views, the polling of the task queue and the lag of the inbox
    And an unreachable view turns readiness not ready and shows on the dashboard, and no business value is written in a probe

  Scenario: AC6 The runbook and the rollback are in place (new, D-RCV-60)
    Given the runbook of the reconciliation and the two previous image digests of the environment
    When a run is rolled back
    Then the runbook says how to read a break and an orphan from the reconciliation read, and who to call for an ACE row
    And the runbook says that a break never changes a Workbench record or an ACE row and is never repaired in this service
    And the rollback redeploys the previous api and worker images and the previous route version
    And every reconciliation_result row already written stays, and no migration is reversed because the sequence is forward only
```

The six criteria are new and test only the deployment: the two deployments, the route, the flag, the four alerts, the dashboard and the probes, the runbook and the rollback. They copy no legacy criterion, because the legacy story had no deployment of its own and its AC1 to AC3 are the screen and the join of the run to the console, owned by RWB-P1-AD019-APP, RWB-P3-AD019-APP and RWB-ITG-AD019-ITG. No threshold, no volume, no percentage and no currency amount is fixed here: the alert levels and the routing are configuration.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The api deployment and the worker deployment run on the same task queue and the same schema, and neither touches another schema | DP-01, DP-02; Architecture v5 slide 33 |
| BR2 | The run is event-started; the deployment creates no Temporal Schedule, no Quartz object and no job-run table | DP-10; Arch v5 slide 44; ASM-0714 |
| BR3 | SCR-45 is registered only as the composite route of RWB-PLT-N001-CON over the console reads of rwb-case; this service publishes no screen route | DP-19; RWB-P3-AD019-APP section 15 |
| BR4 | With the flag `rwb.source-data.reconciliation-run` off, no run starts and the read serves the last completed business date; the flag changes with no redeploy | Platform flag library (default ruling); RWB-P1-AD019-APP section 13 |
| BR5 | The login is a key-store secret reference; no credential appears in a chart value, an image layer, a log or a prompt | NFR-052; DP-02 |
| BR6 | A break never deletes or changes a Workbench record or an ACE row, and the runbook says so before any recovery step | Legacy RWB-AD-019 guardrails; FSD P1 v3 BR-P1-011-3 |
| BR7 | The stale alert carries the product and its last complete business date as E1015 answers it; this story writes no stamp and infers no freshness | FSD P1 v3 VR-P1-014-1; TSD P1 v3 T3.7 |
| BR8 | The four alert rules and the dashboard read the run from the workflow kit and the read from the service; no rule counts a business value of its own | Arch v5 slide 44; TSD P1 v3 T4 |
| BR9 | An alert carries a business date, a product group, a count, a variance and a percent, and no personal data and no business key | Arch v5 slide 42 notes; DP-09 |
| BR10 | A rollback returns the previous images and the previous route version, keeps the rows already written and reverses no migration, because the per-service sequence is forward only | ADR-021; DP-15 |
| BR11 | The alert levels, the routing groups and the dashboard retention are configuration of the platform libraries, not values of this story | Template and Rules section R7.2 s17; platform alert library |
| BR12 | Every environment deploys the same images with different values; a hand change to a pod, a schema or a route is a defect | Architecture v5 slide 29; ADR-021 |

### 9. State transitions

None in the case model and none in the result: this story changes no case status, no result row and no data product status. The moves it owns are the state of a deployment and of the run surface.

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | The pipeline applies the chart | The images, the values and the secret reference are valid | Deployed, flag off |
| Deployed, flag off | The readiness of both deployments | The probes answer and the worker polls | Ready, run stopped; the read serves the last completed business date |
| Ready, run stopped | The flag is switched on | The event has been consumed for a business date | Running on the next `AceDataReady` |
| Running | The flag is switched off | A run is in flight | The run in flight completes or is terminated by the kit policy; no new run starts |
| Running | A rollback is taken | The previous image digests and route version exist | Rolled back; rows already written stay |
| Rolled back | A fix is merged and redeployed | The pipeline applies the new images | Deployed, flag off, then ready |

The deployment record of each environment carries the moves; this story publishes no Kafka event for them and writes no table row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer of rwb-source-data | Owns the chart values, the two deployments, the route registration, the flag entry, the four alert rules, the dashboard, the runbook and the rollback |
| RW-PLATADM, platform administrator | Switches the flag, reads the run on the job monitor and the dashboard, and asks for a rerun after a fix |
| RW-DATASTEW, data steward and data product owner | Receives the hold and the orphan alerts and reads the two blocks they name; owns no deployment control |
| RW-AUDIT, RW-COMPLY | Read the deployment record and the run history; change nothing |
| rwb-case's route owner | Owns the three console reads the SCR-45 route composes; this story registers the route and calls no read of this service directly |
| Platform workflow owner | Owns the namespace, the worker template and the visibility record the alerts read |
| The key-store administrator | Owns the login secret and its rotation; not a Workbench role |
| No delegation of authority level applies | The deployment takes no credit decision and approves nothing |

### 11. Data

No business field. This story writes no row of a business table, creates no table and no index, and holds no personal data.

| Item | Content |
|---|---|
| Chart values | The schema `rwb_source_data`, the task queue `rwb-source-data`, the namespace `rwb-recovery`, the flag entry, the replica counts and the probe paths of the environment |
| Secret references | The `rwb_source_data` login and its password, as key-store references in both deployments |
| Alert rules | The four rules of section 13, with the fields each rule names and the routing groups by configuration |
| Dashboard | The runs by business date, the result per check and product group, the orphan count, the hold state, the DP01 freshness as E1015 answers it, and the probe results |
| Deployment record | The image digests, the chart version, the route version, the flag state, the four rules and the probe results per environment |

The reconciliation rows themselves (`reconciliation_result`, `case_list_row.publish_status`) are written by RWB-P1-AD019-APP; this story deploys and observes the writer and never writes one. The freshness of DP01 is E1015's and is read for the dashboard as an answer, never stamped.

### 12. Contract

#### 12.1 REST operations provided

None. This story publishes no REST operation of its own: the read `GET /api/recovery/source-data/v1/admin/reconciliation/results` is RWB-P1-AD019-APP's and is deployed by this story, and SCR-45 is the route of RWB-PLT-N001-CON over rwb-case's reads.

#### 12.2 REST operations consumed

None. The deployment calls no service at run time; the alert rules and the dashboard read the workflow kit and the service probes, and the flag is read from the platform library.

#### 12.3 Events published

None. This story publishes no Kafka event; the topic `rwb.source-data.events.v1` and its two events belong to RWB-P1-E1015-APP.

#### 12.4 Events consumed

None. The consumed `rwb.source-data.AceDataReady.v1` is the worker's element, deployed here and specified in RWB-P1-AD019-APP section 12.4; this story adds no consumer and no schema.

#### 12.5 Workflows and activities

None added. The deployed worker registers the one workflow of RWB-P1-AD019-APP, `ReconciliationWorkflow`, with its four activities on task queue `rwb-source-data`; this story configures its deployment, its replica count, its drain policy and its alert hook, and creates no workflow, activity or child workflow.

#### 12.6 Schedules

None new. The run is event-started and this story creates no Schedule and no Quartz object. The service is covered by the platform smoke workflow (JOB-22) of the platform at 06:00, which is a platform Schedule and not this story's (Architecture v5 slide 44).

#### 12.7 Tables owned

None. This story owns no schema and no table (DP-01): `reconciliation_result`, `case_list_row` and `data_product_load` are P1's and are written by RWB-P1-E1001-APP, RWB-P1-E1002-APP and RWB-P1-E1015-APP; the alert rules, the dashboard and the deployment record live in the platform's own stores, outside every `rwb_*` schema.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| Deployment fixture | An environment with the platform workflow kit, the route contract, the flag and alert libraries, and the platform smoke workflow | AC1 to AC6 |
| Alert rule fixtures | One condition per rule: a failed run, a stale product, a held case list and an orphan count above the configured level | AC4 |
| Route fixture | The gateway-bff route contract with the three rwb-case reads behind it, one of them failing | AC2, AC3, X3 |

The fixtures are configuration of the pipeline and the environment; the alert levels and the routing groups are set by the operations owner and are never values of the story.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided by this story | The read it deploys is RWB-P1-AD019-APP's; the route it registers is RWB-PLT-N001-CON's |
| Kafka | None | No event is published or consumed by the deployment |
| Temporal | The deployed worker | The worker deployment that polls `rwb-source-data` and registers `ReconciliationWorkflow`; the run's record is the visibility record |
| File | None | No file is read or written; the legacy lake extract is removed (DP-17) |

### 13. Solution plan

**Deliverables.** The chart values of the two deployments per environment, the key-store secret references, the route registration of SCR-45 in the gateway-bff configuration, the flag entry `rwb.source-data.reconciliation-run`, the four alert rules, one dashboard, the probe configuration, the runbook and the rollback procedure.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 applies in its event-started form: the deployed worker runs JOB-04 from `AceDataReady` and creates no Schedule, because Architecture v5 slide 44 records JOB-04 as an event-triggered workflow and the console's freshness Schedule belongs to rwb-case (ASM-0714). DP-19 applies as the route registration: this story registers SCR-45 over rwb-case's reads and adds no page. DP-05 adds nothing at deployment: the views and the login are RWB-P1-E1069-APP's and RWB-P1-E1069-DB's, and this story only deploys the service that reads them.

**Deployment and configuration**

- Two deployments, one chart: the api deployment serving the reconciliation read, and the worker deployment on task queue `rwb-source-data` in namespace `rwb-recovery`, both with the `rwb_source_data` login from the key store.
- The worker sets a drain policy on rollout, so an in-flight `ReconciliationWorkflow` completes or is terminated by the kit policy and no business date is left half run.
- The probes: liveness on the process, readiness on the view reachability, the queue polling and the inbox lag; a failing probe is visible on the dashboard and never writes a business value.
- The flag `rwb.source-data.reconciliation-run` is declared in the platform flag library per environment; off, no run starts on a consumed event and the read serves the last completed business date.
- The route: SCR-45 registered from the RWB-PLT-N001-CON template over the three console reads of rwb-case, with the per-call budget and the error mapping of the contract, and no direct call to this service from the route.

**Alert rules**

| Rule | Condition | Fields the alert names | Route |
|---|---|---|---|
| Job failed | A `ReconciliationWorkflow` or one of its activities ends FAILED | Business date, activity, run, environment | Operations channel |
| Stale data product | E1015 answers a product past its expected business date | Product code, last complete business date, environment | Operations channel and the data steward group |
| Case list held | MSG-P1-012 is raised for a business date | Business date, product group, variance, percent | Data steward, platform administrator and team manager groups |
| REC-05 orphan count above configuration | The orphan count of a business date is above the configured level | Count, business date, run | Data steward group and the ACE team contact |

The levels, the routing groups and the repeat suppression are configuration of the platform alert library, set by the operations owner, and no number is fixed in this story (BR11).

**Runbook**

1. How to read a break: open the reconciliation read for the business date, read `rec_code`, `product_group`, `source_count`, `workbench_count`, `variance_count`, `variance_pct` and `result`, and the break keys with their days past due.
2. How to read an orphan: the REC-05 block names the table, the column and the key; a key missing in ACE goes to the ACE team, a key held on a Workbench row with no case goes to the case owner.
3. Who to call for an ACE row: the ACE team, through the contact of the data contract, with the business date and the key.
4. What a break never does: it never changes a Workbench record or an ACE row, it is never repaired in this service, and no schema, case or view is edited while the source is being fixed.
5. What to do when a run fails: read the failed activity from the visibility record, check the view, the case list step and the parameter read, and rerun the business date only after the cause is cleared.
6. What to do when the flag is off: the read serves the last completed business date; the business date asked for is not lost and the run starts for it when the flag is back on and the event is delivered again.

**Rollback**

- Redeploy the previous api and worker image digests from the deployment record, and restore the previous route version.
- Switch the flag off before the images are replaced when the run itself is being withdrawn, so no new run starts during the change.
- Keep every `reconciliation_result` row and every `case_list_row.publish_status` already written: the per-service sequence is forward only, and a rollback reverses no migration (ADR-021).
- Drain or terminate in-flight runs by the kit policy, and record the business dates whose runs were affected in the deployment record.

**Build steps**

1. Add the two deployments and the values per environment, with the key-store secret references and the drain policy; prove the readiness of both.
2. Register SCR-45 from the route template over the three rwb-case reads and prove that a route calling this service directly fails.
3. Declare the flag and prove the two behaviours without a redeploy.
4. Add the four alert rules with their fields and routing, and prove each condition fires once.
5. Add the dashboard and the probes and prove that an unreachable view turns readiness not ready.
6. Write the runbook and rehearse the rollback in the test environment, including the case with a run in flight.

**Feature flag.** `rwb.source-data.reconciliation-run`, from the platform flag library. Off: no run starts on a consumed `AceDataReady`, the read serves the last completed business date, and the deployed worker keeps polling so that switching the flag on starts the next run without a redeploy.

**Done when.** The six criteria of section 7 pass in the test environment, the two deployments are ready, the route serves SCR-45 over the rwb-case reads, the flag changes the behaviour without a redeploy, each of the four rules fires once with its fields, the dashboard and the probes show the run and the read, and a rollback leaves every row written and no migration reversed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A case list is held for a business date | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | A data product is past its expected business date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | A run fails on an unavailable view, case list step or parameter read | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A caller without Platform administration R reads the reconciliation read behind the route | You cannot {action} here. Your role does not include it. |

The four texts are copied unchanged from legacy RWB-AD-019 and the platform catalogue; this story changes no wording and invents no message of its own. The alerts carry the same message IDs and the substituted values, and an alert never carries a name, an address or an identity number. A deployment failure has no business message: it is a pipeline result and an entry in the deployment record.

### 15. Screens and states

This story builds no screen and no page component. It registers SCR-45 Data quality on gateway-bff as the composite route of RWB-PLT-N001-CON over the three console reads of rwb-case, and the page itself is RWB-P3-AD019-APP's (DP-19). The states of the route are the contract's Loading, breaks, referential completeness and stale, each block with its own error state, so one failing read never blanks the console.

| Surface | What this story makes visible |
|---|---|
| SCR-45 route | The composite route over the rwb-case reads, with the per-call budget and the error mapping of the contract; no direct call to this service |
| Dashboard | The runs by business date, the result per check and product group, the orphan count, the hold state and the DP01 freshness as E1015 answers it |
| Probes | Liveness, the view reachability, the queue polling and the inbox lag |
| Alert surface | The four rules, each naming the business date, the product group or the orphan count and the run |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-019-03 | AC1, AC2, AC3, AC4, AC5, AC6 | End to end | The deployment fixture: two deployments, the route, the flag in both states, one condition per alert rule, a held date and a stale product, one unreachable view, and a rollback with a run in flight |
| TC-AD-019-04 | AC1, AC3; BR5 | Component | A caller without Platform administration R behind the route, refused with MSG-P4-002, and a deployment whose login secret is missing, which does not start |

The two legacy test case IDs are kept. TC-AD-019-03 is the deployment smoke of the run and the read at end-to-end level, and TC-AD-019-04 is the refusal behind the route at component level; the legacy Covers of AC1 to AC3 are not copied, because the legacy tests are the service behaviour of RWB-P1-AD019-APP and RWB-P3-AD019-APP. TC-AD-019-01 and TC-AD-019-02 belong to the screen slice and appear on RWB-P3-AD019-APP, with their `-ITG` copies on RWB-ITG-AD019-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- One schema and one login per service: both deployments use `rwb_source_data` and touch no other schema (DP-01, DP-02).
- No credential in a chart value, an image layer, a log or a prompt; the login is a key-store secret reference (BR5).
- No business value in the deployment: the alert levels, the routing groups, the replica counts and the retention are configuration, and no build rule may introduce a threshold (BR11).
- No personal data in an alert, a dashboard, a probe or a deployment record: a business date, a product group, a count, a variance and a percent only (BR9).
- ACE data only through the owner's contract or `recovery.v_ace_*` views: the deployed service reads the views on its own login, and the deployment names no `public` table (DP-05, ADR-010).
- The run is event-started: no Schedule, no Quartz object and no job-run table is created by the deployment (BR2).
- A break never changes a row: the runbook states it, and no recovery step edits a case, a view or a schema (BR6).
- Forward only: a rollback returns the images and the route version and reverses no migration (BR10).
- One route for SCR-45, composed over the rwb-case reads; a second route and a direct call from the route are defects (BR3).
- Every environment deploys the same images with different values; a hand change is a defect (BR12).

### 18. Traceability

| Legacy RWB-AD-019 row | Value (verbatim) | Where it lands |
|---|---|---|
| Module | P1 Recovery data engine | Service rwb-source-data, service epic RWB-SVC-P1 |
| Endpoints | No endpoint in this story. The console reads the reconciliation and data quality extract that the reconciliation step of JOB-04 writes, and the freshness stamp in `data_product_load`. The data quality exception endpoint is withdrawn by D-RCV-35 and there is no exception table. | Section 1 and section 12.1: the deployed read is API-P1-003 and the freshness is E1015's; no exception endpoint and no exception table is deployed |
| Screen and states | SCR-45 Data quality: Loading; breaks; referential completeness; stale | Section 15: the route registered here, in those states |
| Permission checks | Platform administration, R: RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Section 10; the guard behind the route is the read's own |
| Validation and messages | MSG-P1-012, MSG-P1-001, MSG-GEN-001, MSG-P4-002 | Section 14: the three that an alert or a refusal carries, texts unchanged |
| Guardrails | No business value in code; no personal data; ACE data only through `recovery.v_ace_*`; a break never deletes or changes a record | Section 17 |
| Test cases | TC-AD-019-01 to TC-AD-019-04 | Section 16: TC-AD-019-03 and TC-AD-019-04 here, the first two on the screen slice |

| Trace | Reference |
|---|---|
| Legacy key | RWB-AD-019, disposition Split (rework), business epic EP08, wave 4, release 30 June 2027 (tentative) |
| Deployed stories | RWB-P1-AD019-APP (the read and the JOB-04 worker), RWB-P3-AD019-APP (the console reads behind SCR-45) |
| Pattern rows | DP-05, DP-10, DP-19 |
| Platform dependencies | RWB-PLT-E1071-CON (workflow kit and worker template), RWB-PLT-N001-CON (route contract), the platform flag library, the platform alert library, the platform smoke workflow JOB-22 |
| External dependencies | None |
| Contract dependencies | None |
| Integration dependencies | None |
| Gaps and assumptions | ASM-0714 (the event-started run and no P1 Schedule) |

### 19. Out of scope

- The reconciliation read, `ReconciliationWorkflow`, its four activities and the result rows: RWB-P1-AD019-APP. This story deploys them and changes none of them.
- The console reads of rwb-case, the annotation of a break key and the gateway-bff page: RWB-P3-AD019-APP.
- The cross-service harness and its `-ITG` evidence: RWB-ITG-AD019-ITG.
- The freshness stamp, `data_product_load` and the two events: RWB-P1-E1015-APP. The views, the login and the grant: RWB-P1-E1069-APP and RWB-P1-E1069-DB. The tables and the migrations: RWB-P1-E1001-APP. The case list build: RWB-P1-E1002-APP. The contract documents and the fakes: RWB-P1-E1011-CON.
- The alert library, the dashboard platform, the namespace and the visibility store: the platform observability and workflow stories, RWB-PLT-OBS and RWB-PLT-WF.
- The interface and job monitor SCR-44 and the job operations of `GET /admin/jobs`: their own stories, RWB-P1-AD018-APP and RWB-P1-E1002-CON.
- The data quality exception endpoint and its table, withdrawn by D-RCV-35: nothing is deployed for them.
- The lake extract, the Power BI data set and any management report: removed or out of scope (DP-17).
- The repair of a break or an orphan at source: the ACE team's and the data steward's work.
- Release windows, deployment slots and the change calendar: the programme's delivery decisions, not this story.
