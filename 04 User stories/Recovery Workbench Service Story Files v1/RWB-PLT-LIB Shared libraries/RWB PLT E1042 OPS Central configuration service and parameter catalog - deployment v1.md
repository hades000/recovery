# RWB-PLT-E1042-OPS Central configuration service and parameter catalog

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: deployment slice split from RWB-E1-042 for the platform library RWB-PLT-LIB; the catalog, the value versions and the five operations stay with RWB-P3-E1042-APP and RWB-P3-E1042-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1042-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-042 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-PLT-LIB-E |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-019) |
| Status | Draft (realignment v1) |

### 1. Story

As a **DevOps engineer of the platform**, I want **the parameters client released as one pinned library version in the service template, its environment name, cache time to live and catalog file held as chart values, the catalog seed and the start-up probe deployed in the right order in each environment, the secret references kept out of the catalog values, the dashboards and alerts for a missing value, a stale cache and a failed refresh, and the runbook for a value load, an approval and a rollback**, so that **a value change needs no release and a missing value stops a deployment instead of a service** (Template and Rules §R6, DP-06).

### 2. Business rationale

A client that is correct in code is not yet safe in a deployment. The legacy story put the catalog seed in a Flyway migration of the same application that read it, so the loader and the values always started together (legacy section 13). In the target the values are served by rwb-case and read by 19 services, each in its own image and its own chart, so three new failure modes appear that no line of client code can close: a service deployed with a library version that drifted from the published contract, a service started before the values it needs exist, and a cache that goes stale without anyone noticing because the refresh event never arrived.

**The division is fixed.** The catalog rows, the value versions, the owning service rwb-case, that service's own decision of which version is in force and its server-side cache, and the five REST operations of the legacy story stay with **RWB-P3-E1042-APP** and **RWB-P3-E1042-CON**, under the REST base `/api/recovery/case/v1`; that story owns the legacy acceptance criteria and executes the legacy test cases `TC-E1-042-01` to `TC-E1-042-12`. This story delivers the **deployment of the parameters client library** — the pinned version, the chart values, the seed order, the probe, the secret references, the alerts and the runbook — for the client that RWB-PLT-E1042-APP builds and RWB-PLT-E1042-CON publishes. It copies no legacy acceptance criterion.

What the deployment adds is the order that the split forces. The catalog must exist before a pod starts, so the chart runs a seed check in front of the rollout and the pod carries a readiness probe on the same check as its start-up; the library version must be one version for all 19 services, so the template pins it and the build fails on a drift; the environment name and the catalog file must be deployment data, so they are chart values and a change needs no rebuild; and a stale cache must be visible, so the library's own metrics feed three alerts rather than a log line nobody reads.

The secrets rule is the one place where the deployment carries a security control rather than a convenience. The catalog lists `ace.db.password` as a secret entry and never holds its value; the chart, the pipeline and the image therefore hold a reference to the key store and never a credential, and a scan of the three finds none. That is the deployment half of REQ-ACA-005; the value itself never leaves the key store.

It supports REQ-DRI-010 and REQ-ACA-005, and it makes the legacy measure observable: zero business values in code, and zero services serving traffic without the values they require.

### 3. Preconditions

- RWB-PLT-E1042-APP is delivered: the client, its cache, its listener, its start-up check and its two build checks.
- RWB-PLT-E1042-CON is published and frozen: the pinned major version, the four consumed operations, the event, the cache and start-up rules and the two build-check contracts.
- RWB-PLT-N004-OPS provides the pipeline template and the Helm chart of every service, into which this story adds the library version, the chart values, the seed job and the probe.
- RWB-PLT-NF04-OPS provides the secrets baseline: the key-store reference shape and the scan that proves no credential sits in a pipeline file, a chart value or an image layer.
- RWB-PLT-N005-OPS provides the dashboards and alerts baseline, into which this story adds the three alerts and the client's panel.
- RWB-PLT-E1044-OPS provides the migration run at service start in each environment, which is the sequence that carries the owner's catalog seed and the inbox table the listener writes.
- RWB-P3-E1042-APP serves the catalog and the values in every environment, with the seed of the catalog in its own Flyway sequence in `rwb_case` (DP-01, DP-15).
- The catalog file `config/parameter-catalog.csv` is in the repository, owned by RW-COE, and lists `case.entry.dpd`, `refdata.cache.ttl-seconds` (30 in SIT, 300 in PROD) and `ace.db.password` as a secret entry.
- The chart value names, the seed-job weight, the probe period and thresholds and the alert thresholds of the library are Not specified in the source documents (GAP-1408; ASM-2455; ASM-2456).
- No build dependency: the story has no build dependency and is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Pipeline: the template pins one library version for every service, for example `parameterClientVersion` with major version 1, and the build compares the version in the chart with the version the service compiles against.
2. Pipeline: the build fails when the two versions differ, naming the service, the chart value and the compiled version.
3. Chart: `RWB_ENV` carries the environment name (DEV, SIT, UAT or PROD), `RWB_PARAMETER_CATALOG` carries the catalog file the service ships, and `RWB_PARAMETER_TTL_KEY` carries the name of the catalog entry that bounds the cache, `refdata.cache.ttl-seconds`.
4. Chart: a bootstrap time to live is set for the window before the first catalog answer, and it is compared with the catalog entry at deployment; once the catalog answers, the catalog entry is the time to live and the chart value is ignored (ASM-2455).
5. Deployment: the `parameter-catalog-seed` job runs as a Helm hook before the rollout (`pre-install,pre-upgrade`, weight -5). It reads the chart's catalog file and calls `GET /api/recovery/case/v1/admin/parameters` to confirm that every key of the file exists in the catalog with an owner and a default for that environment; a missing key fails the release before any pod starts.
6. Deployment: the owner's own Flyway sequence in `rwb_case` carries the authoritative row load; the hook never writes the owner's tables (DP-01).
7. Deployment: the pod starts and the readiness probe reads `/health/parameters`, which is the same check as the start-up check; a required value with no value for the environment fails with MSG-P3-032 and the pod stays out of traffic.
8. Chart: the secret entries, `ace.db.password` among them, are key-store references in the chart and the pipeline; no credential appears in a chart value, a pipeline file, an image layer, a log or a prompt.
9. Observability: the client's own metrics feed one panel and three alerts — a required value missing at start-up (page), a cache line older than its time to live (warning, per key and environment), and a failed refresh or a failed read (warning with the breaker state).
10. Operator: a value change is the runbook — load a version, get it approved, verify it in force, roll back if needed — and every step is a call of the owner's operations, never a change of a chart value or of a database row.
11. Release: a library version is rolled forward and back by the pipeline, and a value version is rolled forward and back by the runbook; both are rehearsed in SIT with the evidence attached to the story.
12. The version in the chart and the version in the client's published contract are compared on every build, and a drift is a failed build rather than a discovery in production.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart pins a library version other than the one the service compiles against | The build fails, naming the service, the chart value and the compiled version | None (build output) | AC1 |
| X2 | A required key has no value for the environment at deployment | The seed hook fails the release before the rollout, or the probe keeps the pod out of traffic; the key and the environment are named | MSG-P3-032 | AC4 |
| X3 | The owner's read is unreachable at deploy time | The seed hook fails the release; a running pod keeps its last known state and raises the failed-read alert | None | AC4, AC5 |
| X4 | A credential is found in a pipeline file, a chart value or an image layer | The scan fails the build and the release is not promoted | None (build output) | AC3 |
| X5 | A cache line is older than its time to live | The stale-cache alert fires for the key and the environment; the next read re-reads the owner | None | AC5 |
| X6 | The approval event is never consumed | The failed-refresh alert fires; the time to live closes the gap at the next read and the version served is still an approved one | None | AC5 |
| X7 | A library rollback leaves a pod on the previous version | The pipeline rolls the deployment back and the drift check proves chart and contract agree again | None | AC6 |
| X8 | A value rollback leaves no earlier version | The owner refuses the rollback and the runbook stops; the value in force does not change | MSG-P3-015 | AC6, AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the client, its contract and the three platform baselines; no service has to be built first |
| Negotiable | The chart value names, the seed weight, the probe period and the alert thresholds are settled with the platform team; the order and the rules are fixed |
| Valuable | A value change needs no release, and a missing value stops a deployment instead of a service |
| Estimable | One pinned version, three chart values, one seed hook, one probe, one panel, three alerts and one runbook |
| Small | Fits one sprint with its rehearsals |
| Testable | Each criterion runs in the pipeline and in SIT against the chart and the fake of section 12.8 |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the parameters client

  Background:
    Given the parameters client library is published at major version 1
    Given the catalog and the values are served by rwb-case under /api/recovery/case/v1
    Given every service is deployed from the service template and its Helm chart

  Scenario: AC1 The library version is pinned and a drift fails the build (new, D-RCV-60)
    Given the template pins parameterClientVersion 1.0.0 for every service
    When a service chart pins 1.1.0 while the service compiles against 1.0.0
    Then the build fails naming the service, the chart value and the compiled version
    When the chart and the compiled version agree
    Then the build passes and the deployed image carries the pinned version

  Scenario: AC2 The environment, the time to live and the catalog file are chart values (new, D-RCV-60)
    Given the chart values RWB_ENV, RWB_PARAMETER_CATALOG and RWB_PARAMETER_TTL_KEY
    When SIT is deployed with RWB_ENV SIT and PROD with RWB_ENV PROD
    Then the client reads the environment name from the chart and reports it in every answer
    Then the time to live is the catalog entry refdata.cache.ttl-seconds, 30 in SIT and 300 in PROD, and the chart value is the bootstrap only
    Then a change of the environment name or of the catalog file needs no rebuild of the image

  Scenario: AC3 The secret references are kept out of the catalog values (new, D-RCV-60)
    Given the catalog lists "ace.db.password" as kind ENVIRONMENT with secret = true
    When the chart, the pipeline and the image are scanned
    Then every secret is a key-store reference and no credential appears in a chart value, a pipeline file, an image layer, a log or a prompt
    Then the catalog carries the entry and no value for it, and the scan reports no secret value in any catalogue row

  Scenario: AC4 The catalog seed runs before the start and the probe holds the pod out of traffic (new, D-RCV-60)
    Given the parameter-catalog-seed job runs as a Helm hook before the rollout
    When a key of the chart's catalog file has no entry, no owner or no default in the catalog for that environment
    Then the hook fails the release before any pod starts
    Given "refdata.cache.ttl-seconds" is required and has no value for UAT
    When the rollout runs in UAT
    Then the readiness probe answers DOWN with MSG-P3-032 naming the key and the environment and the pod takes no traffic
    Then the deployment reports a failed rollout instead of a serving service

  Scenario: AC5 The dashboards and the alerts cover the three failures (new, D-RCV-60)
    Given the client's own metrics on the platform observability path
    When a required value is missing at start-up, a cache line passes its time to live, or a refresh fails
    Then each case raises its own alert with the service, the key and the environment
    Then the panel shows cache age per key, refreshes, failed refreshes and start-up refusals for each environment
    Then the missing-value alert is the only one that pages

  Scenario: AC6 The rollout and the rollback are rehearsed with evidence (new, D-RCV-60)
    Given the library at version 1.0.0 in SIT
    When the pipeline rolls version 1.1.0 out and then rolls it back
    Then each step is recorded with the image, the chart value, the time and the result
    Given a value version 2 of "case.entry.dpd" and a later rollback to version 1
    When the runbook runs in SIT
    Then the client serves 91 with version 2 and then 90 with version 1, and each step is recorded with the load id, the approver role and the time

  Scenario: AC7 The runbook is published and one rehearsal is recorded (new, D-RCV-60)
    Given the runbook for a value load, an approval, a verify and a rollback
    When an operator follows it for a value of "case.entry.dpd"
    Then every step names the owner's operation, the role that may run it and the message of a refusal
    Then the rehearsal of the six-step path is recorded with its evidence and no step changes a chart value or a database row by hand
```

Every criterion above is new and tests only the deployment of the client. No legacy acceptance criterion is copied: the eleven criteria of RWB-E1-042 stay with RWB-P3-E1042-APP, and the legacy test cases `TC-E1-042-01` to `TC-E1-042-12` execute there.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One library version for all 19 services, pinned in the template; a chart that disagrees with the compiled version fails the build | Legacy section 4 step 2; DP-06 |
| BR2 | The environment name, the catalog file and the time-to-live entry are deployment values, so a value change needs no release and no rebuild | Legacy BR3; REQ-DRI-010; ASM-2455 |
| BR3 | The time to live is itself a catalog entry; the chart value is the bootstrap and the catalog entry governs once the owner answers | Legacy section 13; ASM-2455 |
| BR4 | The catalog seed runs before the service starts, and a service without its required values takes no traffic | Legacy BR7; Principle 1 |
| BR5 | Secrets are key-store references: the catalog lists them and the chart, the pipeline and the image hold no value for them | Legacy BR6; DL26; REQ-ACA-005; NFR-052 |
| BR6 | A value change is the operator's load, approval, verify and rollback, never a chart change and never a manual row update | Legacy BR3, BR4; CTL-08 |
| BR7 | A cache older than its time to live, a failed refresh and a missing required value are visible on the platform dashboards and raise their own alert | Legacy section 5 X3; ASM-2456 |
| BR8 | The deployment never writes the owner's tables: the row load is the owner's Flyway sequence in `rwb_case` | DP-01; DP-15 |

### 9. State transitions

The deployment has release states, not case states.

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Seed hook passes | Every key of the catalog file exists with an owner and a default | Rollout started |
| Not deployed | Seed hook fails | A key is missing, has no owner or has no default | Release failed, no pod started |
| Rollout started | Probe ready | Every required value is present for the environment | Serving |
| Rollout started | Probe unready with MSG-P3-032 | A required value has no value for the environment | Rollout failed, the pod takes no traffic |
| Serving | Library roll-forward | The chart and the compiled version agree | Serving on the new version |
| Serving | Library rollback | The pipeline restores the previous chart value | Serving on the previous version |
| Serving | Value load approved and in force | The valid-from date is reached | Serving the new value with no restart |
| Serving | Value rollback approved | An earlier approved version exists | Serving the previous value |
| Serving | Cache older than the time to live, or a failed refresh | None | Alert raised; the value served is still an approved one |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer of the platform | Owns the pinned version, the chart values, the seed hook, the probe, the alerts and the runbook |
| RW-PLATADM, platform administrator | Reads the client's panel and the failed rollout on SCR-44; reruns a release |
| RW-COE | Owns the catalog file and runs a value load |
| RW-RISK | Approves a value version where a threshold or a limit moves |
| RW-AUDIT, RW-COMPLY | Read the release record, the value history and the alert history |
| Key store administrator | Owns the secret entries and their rotation; not a Workbench role |
| No delegation of authority level applies | A parameter is not a credit decision |

### 11. Data

No business field is written by this story. The deployment reads the catalog file from the chart, reads the catalog through the owner's operation and writes a release record with the service, the environment, the image, the chart values, the library version, `startedAt`, `endedAt` and a status of PASSED or FAILED. It reads the secret references from the key store and never their values.

The chart value names, the seed-job weight, the probe period and thresholds, the alert thresholds and the retention of the release record are Not specified in the source documents (GAP-1408; ASM-2455; ASM-2456); the working read of this run is used until the register closes the point. The catalog file holds keys, types, ranges, defaults, owners and environments and no personal data and no secret value.

### 12. Contract

#### 12.1 REST operations provided

None — the deployment provides no REST operation. The client's only HTTP surface inside a pod is the service's own health endpoint, which the probe reads.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the deployment |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The seed hook confirms every key of the chart's catalog file, with its owner and its default, for the environment; a running client reads it for its values |
| POST | `/api/recovery/case/v1/admin/reference-loads` | P3 rwb-case | The runbook's load step and the SIT rehearsal of a value version |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | P3 rwb-case | The approval whose event refreshes the caches; driven by the runbook and the rehearsal |
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | P3 rwb-case | The rollback of a value version in the runbook and the rehearsal |

The deployment calls the read; the three load operations are called by an operator following the runbook. The pipeline holds no credential of its own for them: every call is an operator session with a right from the P4 matrix, and the deployment only records that the step happened.

#### 12.3 Events published

None — the deployment publishes no event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.case.ParameterVersionApproved.v1` | `rwb.case.events.v1` | P3 rwb-case | The pods of every service subscribe through the client's inbox; the deployment's part is the consumer group per service, the topic ACL, the retry topics and the dead-letter alert of the event platform |

The event name follows §R4 naming on the owner's topic and is recorded in ASM-2453; the topic, its ACLs and its retry and dead-letter topics are the event platform's (RWB-PLT-EVT).

#### 12.5 Workflows and activities

None — the seed hook is a Helm hook, the probe is a readiness probe and the refresh is library code; the deployment starts no workflow and no activity.

#### 12.6 Schedules

None — a value load is operator-initiated and the refresh is event-driven; no Schedule is created for the catalog, for the seed or for the alerts.

#### 12.7 Tables owned

None — the deployment owns no table. The catalog and the values are P3 tables in `rwb_case`, and the inbox row the listener writes is the outbox and inbox library object in each service's own schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case parameters fake | `GET /api/recovery/case/v1/admin/parameters` answering the catalog line with the value in force, the version and the valid-from date, and an entry with no value for `ace.db.password`; a missing required value for UAT | The seed hook test, the probe test and the alert tests |
| rwb-case reference-load fake | The three load operations answering 201, 200 and 200 with status ROLLED_BACK, and 409 for a rollback with no earlier version | The runbook rehearsal and the SIT value-version test |
| Approval-event stub | `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1`, one new id and one repeat | The failed-refresh alert test and the library rollback test |
| Key-store stub | The secret references of the chart | The credential scan test |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 4 consumed | The seed hook reads the catalog; the runbook and the rehearsal call the three load operations |
| Kafka | None published, 1 consumed | The pods subscribe to `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1` |
| Temporal | None | No workflow, no activity and no Schedule |
| File | 1, the catalog file | `config/parameter-catalog.csv` travels in the image and the chart and is read by the client's generator and the seed hook, never by a running request |

### 13. Solution plan

**Deliverables.** The pinned library version in the pipeline template, the three chart values with their bootstrap and drift check, the `parameter-catalog-seed` Helm hook, the readiness probe on the client's health check, the key-store references for the secret entries, the panel and the three alerts, the runbook and its rehearsal record.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The seed hook reads the catalog through the owner and writes no row | referred to; the consuming story carries the dependency |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. The version a service records is the one the client answered | referred to; the consuming story carries the dependency |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. This story deploys that client into every chart | referred to; the consuming story carries the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The product-group codes the client resolves are reference rows of the owner | referred to; the consuming story carries the dependency |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. The deployment fixes the consumer group and the topic ACL for the refresh event | referred to; the consuming story carries the dependency |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The read is one hop from the pod with the caller's breaker, and the seed hook uses the same path | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. Every path the chart and the runbook use is a `/api/recovery/case/v1` path | referred to; the consuming story carries the dependency |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library. The deployment subscribes to `rwb.case.events.v1` and creates no topic name of its own | referred to; the consuming story carries the dependency |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The run at service start carries the owner's catalog seed and each service's inbox table | referred to; the consuming story carries the dependency |
| DP-19 | Screen, ace-web | gateway-bff composite route. The panel and SCR-44 are read through the gateway; a value change has no screen of its own | referred to; the consuming story carries the dependency |

**Hardware and software change.** The deployment adds one pinned library to every service image, three chart values per environment, one pre-rollout hook and one readiness probe, and one panel with three alerts on the existing observability path. The catalog row load stays with the owner's Flyway sequence in `rwb_case`, so the deployment creates no table, no seed of its own and no database row. No new hardware is implied: the hook and the probes run in the existing AKS namespaces, and the metrics go to the platform the observability baseline already provides.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Pinned library version | Pipeline template value | One version for all 19 services, compared with the compiled version on every build (BR1) |
| `RWB_ENV`, `RWB_PARAMETER_CATALOG`, `RWB_PARAMETER_TTL_KEY` | Chart values | The environment name, the catalog file and the catalog entry that bounds the cache (BR2, BR3) |
| Bootstrap time to live and its drift check | Chart value and pipeline step | The value used before the first catalog answer, compared with `refdata.cache.ttl-seconds` at deployment (BR3) |
| `parameter-catalog-seed` hook | Helm hook, `pre-install,pre-upgrade`, weight -5 | Confirms every key of the catalog file with an owner and a default before the rollout (BR4) |
| Readiness probe | Chart probe | Reads the client's health check; a missing required value keeps the pod out of traffic with MSG-P3-032 (BR4) |
| Secret references | Chart values and pipeline variables | The key-store reference for each secret entry, and the scan that proves no credential (BR5) |
| Panel and three alerts | Observability assets | Cache age per key, refreshes, failed refreshes, start-up refusals; one page and two warnings (BR7) |
| Runbook and rehearsal record | Document | Load, approve, verify and rollback with the owner's operations, the role and the refusal message (BR6) |

**Build steps**

1. Add the pinned version to the pipeline template and the drift check against the compiled version; prove a mismatch fails the build (AC1).
2. Add the three chart values per environment and the bootstrap of the time to live with its comparison against the catalog entry (AC2).
3. Replace every secret value in the chart and the pipeline with a key-store reference and wire the scan (AC3).
4. Write the seed hook and run it before the rollout in SIT; prove that a missing key, owner or default fails the release (AC4).
5. Wire the readiness probe to the client's health check and prove the UAT case with MSG-P3-032 (AC4).
6. Add the panel and the three alerts and prove each one fires once, with the missing-value alert as the only page (AC5).
7. Write the runbook for load, approve, verify and rollback, with the owner's operations, the roles and the refusal messages (AC7).
8. Rehearse the library roll-forward and rollback, then the value version and its rollback in SIT, and record both (AC6).
9. Hand the release record and the alert routes to the platform administrator and the platform team.

**Done when.** The six test cases of section 16 pass in SIT, a drifted chart fails the build, a release with a missing required value fails before it serves, the three alerts fire in the rehearsal, and the runbook and its evidence are published.

The exact chart value names, the seed-job weight, the probe period and the alert thresholds are Not specified in the source documents (GAP-1408; ASM-2455; ASM-2456); the names and the order above are the working read of this run.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-032 | A required parameter has no value at start-up, in the log and on the probe answer | Parameter {name} has no value for {environment}. The service did not start. |
| MSG-GEN-002 | A loaded value is outside its range, on the owner's load operation | {field} must be between {min} and {max}. |
| MSG-P1-002 | A loaded value has the wrong type or an unknown key, on the owner's load operation | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | The load file is empty, on the owner's load operation | Enter {field}. |
| MSG-P7-002 | The approver is the author, on the owner's approval operation | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | A rollback has no earlier version, on the owner's rollback operation | There is no earlier version of {table} to return to. |
| MSG-P4-002 | A role without the right calls an operation in the runbook | You cannot {action} here. Your role does not include it. |

MSG-P3-032 is shown in the pod's log and on the probe answer, never to a business user; the other six are the owner's and appear in the runbook unchanged. The build findings of the pinned version and of the credential scan carry no message id: they name the service, the chart value and the compiled version, or the file and the line of the finding. Thai text for each message follows decision DL10.

### 15. Screens and states

No new screen. SCR-44 Interface and job monitor shows the release in state Running, Failed or Complete, with the service, the environment, the image, the chart values and the library version, and the platform administrator reruns a failed release from there. The client's panel shows cache age per key, refreshes, failed refreshes and start-up refusals per environment, and the three alerts route to the platform administrator and the platform team. A value change has no screen of its own in this story: SCR-39 Rules and parameters belongs to Epic 8, and until it exists the operator uses the owner's operations through the runbook (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1042-OPS-01 | AC1 | Contract | Chart pinned at 1.0.0 and compiled at 1.1.0, then both at 1.0.0; the drift finding names the service and the chart value |
| TC-PLT-E1042-OPS-02 | AC2 | Component | SIT with `RWB_ENV` SIT and PROD with PROD; `refdata.cache.ttl-seconds` 30 and 300; a changed catalog file with no rebuild |
| TC-PLT-E1042-OPS-03 | AC3 | NFR | Scan of the chart, the pipeline file, the image layers, the logs and the catalog rows for `ace.db.password`; no credential, one key-store reference |
| TC-PLT-E1042-OPS-04 | AC4 | Component | A catalog file key with no owner fails the hook; UAT with no value for `refdata.cache.ttl-seconds` fails the probe with MSG-P3-032 and serves no traffic |
| TC-PLT-E1042-OPS-05 | AC5 | NFR | One missing value, one cache line past its time to live and one failed refresh; three alerts, one page, the panel shows each case |
| TC-PLT-E1042-OPS-06 | AC6, AC7 | Component | The library roll-forward and rollback; the value version 2 to 91 and its rollback to 90 for `case.entry.dpd`; the six-step runbook rehearsal recorded |

The levels are the deployment-side shape: the pipeline pieces are Contract, the chart and hook behaviour is Component, and the scan, the alerts and the cache age are NFR. The legacy test case ids are not reused here; they stay with RWB-P3-E1042-APP.

### 17. Guardrails

- One library version for all 19 services, pinned in the template; a drift is a failed build and never a production discovery.
- No business value and no credential in a chart value, a pipeline file, an image layer, a log or a prompt; every secret is a key-store reference.
- No value in the catalog tables is written by the deployment: the row load is the owner's Flyway sequence in `rwb_case` (DP-01).
- No manual row update and no chart change to move a parameter value: a value changes through the runbook's load, approve, verify and rollback.
- No pod serves traffic without its required values for the environment; the probe reads the same check as the start-up.
- No alert without an owner: the missing-value alert pages the platform administrator, and the two cache alerts go to the platform team.
- No personal data in a release record, an alert or a log; the record holds the service, the environment, the versions and the times only.
- The library adds no REST base, no topic and no task queue of its own, and the deployment invents none for it.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-010 | Parameter catalog and configuration service, versioned, changed without a release | The pinned version and the chart values: a value change is a load, an approval and a rollback with no rebuild | TC-PLT-E1042-OPS-01, TC-PLT-E1042-OPS-02, TC-PLT-E1042-OPS-06 |
| REQ-ACA-005 | Secrets are listed in the catalog and held only in the secret store | Every secret entry is a key-store reference in the chart and the pipeline, and the scan proves no credential in the chart, the pipeline, the image or a log | TC-PLT-E1042-OPS-03 |

| Legacy test cases | Disposition |
|---|---|
| `TC-E1-042-01, TC-E1-042-02, TC-E1-042-03, TC-E1-042-04, TC-E1-042-05, TC-E1-042-06, TC-E1-042-07, TC-E1-042-08, TC-E1-042-09, TC-E1-042-10, TC-E1-042-11, TC-E1-042-12` | executed by RWB-P3-E1042-APP |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1042-APP | App development | The client this story deploys: its cache, listener, start-up check and metrics |
| RWB-PLT-E1042-CON | Contract | The contract that fixes the pinned version, the four operations, the event and the start-up rule |
| RWB-PLT-N004-OPS | DevOps | X: the pipeline template and the Helm chart this story adds the version, the values, the hook and the probe to |
| RWB-PLT-NF04-OPS | DevOps | X: the secrets baseline and the scan this story uses for the secret entries |
| RWB-PLT-N005-OPS | DevOps | X: the dashboards and alerts baseline this story adds the panel and the three alerts to |
| RWB-PLT-E1044-OPS | DevOps | X: the migration run at service start that carries the owner's catalog seed and each service's inbox table |
| RWB-P3-E1042-APP, RWB-P3-E1042-CON | App development, Contract | C: the owner of the catalog, the values and the five operations the deployment reads and the runbook calls |
| RWB-PLT-EVT | Platform epic | X: the topic, its ACLs, the retry topics and the dead-letter alert of the refresh event |

REQ-ACA-005 has no row in legacy section 18; its short text is legacy BR6 and its BRD section is the one the legacy Epic 1 story of the same requirement carries.

### 19. Out of scope

- The catalog rows, the value versions, the owner's Flyway seed and the service that serves them: RWB-P3-E1042-APP.
- The five REST operations and their validation: RWB-P3-E1042-APP and RWB-P3-E1042-CON.
- The client's code, its cache, its listener and its two build checks: RWB-PLT-E1042-APP, and the interface and data contract in RWB-PLT-E1042-CON.
- The pipeline template and the chart themselves: RWB-PLT-N004-OPS, which this story adds values and a hook to.
- The secrets baseline, the key store and its rotation: RWB-PLT-NF04-OPS and the platform.
- The dashboards and alerts baseline: RWB-PLT-N005-OPS, which this story adds one panel and three alerts to.
- The migrations, the drift gate and the run at service start: RWB-PLT-E1044-OPS.
- The topic, its ACLs, the retry topics and the dead-letter topic: RWB-PLT-EVT.
- The administration screen SCR-39 Rules and parameters: Epic 8.
