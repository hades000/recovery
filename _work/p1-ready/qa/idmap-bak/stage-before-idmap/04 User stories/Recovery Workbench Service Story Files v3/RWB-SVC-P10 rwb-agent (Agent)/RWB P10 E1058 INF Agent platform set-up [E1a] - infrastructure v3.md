# RWB-P10-E1058-INF Agent platform set-up [E1a]

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1058-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-058 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP08, DP09, DP11, DP13, DP15, DP19, DP20 |
| Readiness decisions | RD-P1-008 |
| Parallel lane | L-P10-B |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P10-E1058-INF-16); the squad sizes at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E1058-CON (build status Not started; fake library version not recorded as published, DOR-RWB-P10-E1058-INF-22; contract version v1, base path /api/recovery/agent/v1, DP-13) |
| Platform prerequisites | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON (DP-03, DP-06, DP-07, DP-09, DP-19); P3 contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON; and the published contract of the P4 authorise call (contract ID: Not specified in the source documents (GAP-2404)). Delivery prerequisites of the service template, not per-story blockers; the story stays Day 1 |
| Integration dependencies | None |
| External dependencies | None |
| Reference data | Parameters: the 60 second model budget and the 2 second client budget read from the policy row at run time; reference-data contract and catalog keys Not specified in the source documents (DOR-RWB-P10-E1058-INF-20) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-024, FR-P10-025) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- The decision event type reads `rwb.decision.DecisionRecorded.v1`; the topic `rwb.decision-record.v1` is unchanged (RD-P1-008).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-058 for rwb-agent. The legacy platform ran in one process against one schema: the model endpoint was called by an in-process client, the prompt and policy store was a table of the same schema, and the run completion never left the database. The service needs a private path and an identity to the Enterprise AI endpoint, its own schema and login, its own topic with a producer right and a dead-letter route, its own Temporal task queue, and a measured budget for the two waits that decide whether an agent is useful. This story provisions and configures only: the private path and the egress allow-list to INT-23 (INT-23, as in the Epic 2 key of this service), the Key Vault entries of the service login and of the gateway secrets, the topic `rwb.agent.events.v1` with its retry and `.dlt` topics and the producer ACL of rwb-agent, the Temporal task queue `rwb-agent` in namespace `rwb-recovery` with its worker identity and concurrency, the PostgreSQL schema `rwb_agent` with its login, the capacity and the alarms of a run, and the CI/CD gates. It creates no table, no business value and no invented resource name. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As an **infrastructure engineer**, I want **the private network path and the egress allow-list to the Enterprise AI private endpoint INT-23 with TLS and mTLS, the Key Vault entries of the rwb-agent service login and of the model-gateway secrets wired to the workload identity, the PostgreSQL schema `rwb_agent` and its login with grants on that schema only, the Kafka topic `rwb.agent.events.v1` with its retry and `.dlt` topics and the producer ACL of rwb-agent, the Temporal task queue `rwb-agent` in namespace `rwb-recovery` with its worker identity and concurrency, the 60 second model budget and the 2 second client budget measured as platform requirements, capacity and alarms for a burst of agent runs, and the CI/CD gates of the service**, so that **every model call leaves the cluster through one approved private path, every run reaches the topic its consumers read, every evaluation finds the schema it needs, and a timeout, a refused producer or a burst is seen and alerted before an officer notices a missing answer or a stalled evaluation**.

### 2. Business rationale

The legacy story needed none of this. `ModelGatewayClient` called the Enterprise AI endpoint from the same process on a permitted network, the prompt and policy store was a table of the shared `recovery` schema, the run row and its event were written by the same deployment, and the evaluation harness ran in the same JVM. In the target the model is reached on a private endpoint of the SCB tenant, outside the cluster (Arch v5 slides 8 and 16; TSD P10 v2 T5.1), the store and the run are rows of the service's own schema (DP-01, DP-15), the run completion is a Kafka message on the service's own topic with three consuming services (Arch v5 slide 43), and the run itself is a workflow on the service's own task queue (Arch v5 slide 16; Temporal and Drools design slide 11). Each of those is an infrastructure fact the monolith did not have:

- A network path with a certificate on both sides, and an egress list that admits one destination and drops the rest.
- An identity that holds the secret of that path, and a schema login that holds grants on `rwb_agent` only.
- A topic with a producer right for its owner, a registry subject for its payload, a retry topic and a dead-letter route.
- A task queue with a worker identity, a concurrency and a scaling rule, so a burst of runs is absorbed instead of dropped.
- Two measured budgets: the 60 second model call, after which the rule result is used and the case still routes (NFR-010; Arch v5 slide 35), and the 2 second client budget of every other hop (ADR-020).

Without the path the call cannot be made at all. Without the identity and the Key Vault entries the path cannot be authenticated and a certificate ends up in a chart value. Without the topic and its `.dlt`, a finished run is invisible to rwb-decision, rwb-document and rwb-deviation and a bad payload is lost silently. Without the queue and its worker identity, a run submitted by a calling step never starts and the caller's fallback fires for the wrong reason. Without the budgets and the alarms, the fallback of R-UNI-32 is invisible and a capacity problem is diagnosed from complaints.

This story creates no `rwb_*` table, no business value, no bucket and no Schedule: the policies, the prompts, the samples, the runs, the evaluations and the feedback are rows of `rwb_agent` (DP-01; ASM-0851), and no source names a Blob container for agent artefacts.

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), and the service follows the §R4 naming: schema `rwb_agent`, base `/api/recovery/agent/v1`, topic `rwb.agent.events.v1`, task queue `rwb-agent`, one login per service, Java package `th.co.scb.ace.workbench.recovery.agent`.
- The ACE AKS cluster, the shared Azure App Gateway and the platform service mesh are in force with the workload identity mechanism of the platform, so no credential sits in a file, a chart or a repository (Arch v5 slides 7 and 8).
- The Enterprise AI private endpoint INT-23 exists in the SCB tenant and its certificate authority is known to the platform; its host, port and certificate subject are Not specified in the source documents (GAP-0608; ASM-0854).
- The ACE PostgreSQL server is available, and the ACE database administrator can create a schema and a login; the name of the login is Not specified in the source documents (GAP-0606; ASM-0848).
- The Kafka event platform and the schema registry are available (RWB-PLT-EVT), because a produced payload is validated against its subject before the outbox relay publishes it (DP-09).
- The Temporal cluster runs namespace `rwb-recovery` with one task queue per service, and the worker of each service polls only its own queue (Temporal and Drools design slide 11).
- The decision-record library, the outbox library and the access guard library of RWB-PLT-E1027-CON, RWB-PLT-TE006-CON and RWB-PLT-E1037-CON are the platform components whose secrets and destinations this story configures; this story does not build them.
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in lane L-P10-B.

### 4. Flow

1. Open the private network path from the rwb-agent pods to the Enterprise AI private endpoint INT-23 in each environment, with TLS on the wire and mTLS to the endpoint, and record the destination as a reviewed entry of the egress allow-list with a default drop.
2. Create the PostgreSQL schema `rwb_agent` and the service login with grants on that schema only, and confirm that the login holds no right on another schema and no cross-schema foreign key is possible.
3. Create the Key Vault entries the service needs - the login secret reference, the client certificate and its key for the model gateway, and the endpoint reference - and wire them to the workload identity through the platform secret mechanism, so no literal value reaches a values file, a chart template, a log or a dashboard.
4. Provision the topic `rwb.agent.events.v1` with its retry topic and its `.dlt` topic, its partitions and retention as reviewed environment values, and grant rwb-agent the producer right on the topic and on its retry topic only.
5. Register the payload subject of `rwb.agent.AgentRunCompleted.v1` and of `rwb.decision.DecisionRecorded.v1` in the schema registry with BACKWARD compatibility, so the producer validates before the relay publishes.
6. Provision the Temporal task queue `rwb-agent` in namespace `rwb-recovery`, and the worker identity, the concurrency, the poller count and the activity timeouts the worker may use on it.
7. Make the two budgets measurable: a platform metric and an alarm on the 60 second model call inside the workflow, and a platform metric and an alarm on the 2 second client budget of every REST hop of the service.
8. Size the pods for a burst of agent runs and for a burst of evaluation runs, record the request and limit per environment, and set the alarms on queue backlog, run throughput, fallback rate, error rate and the `.dlt` count.
9. Add the CI/CD gates of the service: the chart and policy checks, the identity and secret checks, the topic and subject checks, the contract tests against the fakes of RWB-P10-E1058-CON, and the boundary scan that fails a build reading another schema or naming another service's topic or base.
10. Hand the endpoint reference, the login reference, the topic names and the queue to RWB-P10-E1058-APP and RWB-P10-E1058-CON, and the metrics and alarms to RWB-P10-E1058-OPS.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A pod calls a destination outside the egress allow-list | The network policy drops the call; the attempt is counted and alerted and the run holds status MODEL_ERROR or TOOL_UNAVAILABLE with fallback true | None | AC1 |
| X2 | The mTLS handshake to INT-23 fails: the certificate is missing, expired or not issued by the platform authority | The model call fails before any request body is sent; the run holds MODEL_ERROR with fallback true and nothing is written as an answer | None | AC1, AC2 |
| X3 | A secret, a key or a certificate body appears in a values file, a chart template, a log or a dashboard | The pipeline secret scan fails the build or the release, and the entry is rotated | None | AC2 |
| X4 | The login of the service is missing, or holds a grant on another schema | The provisioning check fails and the release is not marked ready; the grant is corrected by the database administrator | None | AC3 |
| X5 | A produced EV-28 payload fails its registry subject, or the topic is unreachable | The message is refused before the relay and routed to the `.dlt` topic with an alert; the outbox row stays until the relay succeeds | None | AC4 |
| X6 | A producer outside rwb-agent attempts to write to `rwb.agent.events.v1` | The ACL refuses the write and the attempt is alerted | None | AC4 |
| X7 | The worker polls a queue that is not its own, or the queue is missing in the namespace | The worker does not start, the readiness check fails and the deployment does not roll out | None | AC5 |
| X8 | The model call exceeds the 60 second budget, or a client call exceeds the 2 second budget | The alarm fires with the endpoint, the agent code and the caller named, and the run records TIMED_OUT or the failed read with fallback true | None | AC6 |
| X9 | A burst of runs or evaluations raises the queue backlog and the pod saturation | The alarm fires, the worker scales as configured and the run continues when capacity returns; no run is dropped silently | None | AC7 |
| X10 | A gate is bypassed, or a build names another schema, another service's topic or another service's base | The pipeline refuses the merge and the boundary scan names the file and the string | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions a path, an identity, a schema login, secrets, a topic, a queue, metrics and gates; no application code is built here and no in-lane story blocks it |
| Negotiable | The retention, the partition count, the heap values, the ports, the concurrency and the alarm thresholds are environment values settled with the platform team, not story decisions |
| Valuable | Makes the INT-23 call possible and authenticated, makes a run reach its three consumers, makes the evaluation find its schema, and makes the fallback of R-UNI-32 visible before an officer notices |
| Estimable | One path and its allow-list, one schema and one login, three Key Vault entries, one topic with two related topics and a producer grant, one queue and one worker identity, two budgets with their alarms, one sizing decision and five pipeline gates |
| Small | Fits one sprint with the provisioning and the gate checks |
| Testable | Every criterion tests an artefact: a handshake, a dropped call, a secret scan, a refused grant, a refused write, a `.dlt` route, an alarm, a load test and a gate run |

### 7. Acceptance criteria

```gherkin
Feature: Infrastructure for the rwb-agent platform in wave 1

  Background:
    Given the ACE AKS cluster, the platform service mesh, Key Vault, the ACE PostgreSQL server and the Kafka platform are in force
    Given the service naming rule of section R4 of the template is in force
    Given the release date 30 November 2026 is tentative

  Scenario: AC1 The private path to INT-23 is one hop with TLS and mTLS (new, D-RCV-60)
    Given the egress allow-list of the rwb-agent pods in each environment
    When the allowed destinations are inspected and a model call is made
    Then the Enterprise AI private endpoint INT-23 is allowed, one hop, on the reviewed port, and no other outside destination is reachable
    Then the connection uses TLS, and the endpoint presents a certificate the platform certificate authority trusts and rwb-agent presents its client certificate
    Then a call to a destination outside the list is dropped, counted and alerted, and the run records the mapped status with fallback true
    Then an expired, missing or unissued client certificate fails the call before any request body is sent
    Then the destination is a reviewed entry per environment and never a template constant

  Scenario: AC2 The login secret and the gateway secrets are held in Key Vault only (new, D-RCV-60)
    Given the rwb-agent service login and the workload identity of the environment
    When the pods start and call the model gateway
    Then the login secret, the client certificate, its key and the endpoint reference are read from Key Vault by the workload identity at run time
    Then no secret, key or certificate body appears in a values file, a chart template, a log, a config map or a dashboard, and the pipeline secret scan fails the build when one does
    Then the rotation of the certificate, of the login secret and of the endpoint reference is a Key Vault operation with no rebuild of the service
    Then the login secret is referenced by name only and no literal password exists in the pipeline, the chart or the environment

  Scenario: AC3 The schema rwb_agent and its login are provisioned with grants on that schema only (new, D-RCV-60)
    Given the ACE PostgreSQL server and the ACE database administrator
    When the schema and the login are provisioned
    Then schema rwb_agent exists with its Flyway history table and the ownership of the service login
    Then the login holds the rights the migration and the runtime need on rwb_agent only, and a read or a write on another schema is refused
    Then a foreign key from rwb_agent to another schema is refused by the boundary check and by the pipeline gate
    Then the connection pool of the login has a reviewed cap per environment and the provisioning check names it

  Scenario: AC4 The agent topic and its two related topics exist with a producer ACL (new, D-RCV-60)
    Given the Kafka platform and the schema registry of the environment
    When the topics and the ACLs are inspected
    Then rwb.agent.events.v1 exists with its retry topic and its .dlt topic, with the reviewed partitions and retention
    Then rwb-agent holds the producer right on rwb.agent.events.v1 and on its retry topic only, and a producer outside rwb-agent is refused and alerted
    Then the payload subjects of rwb.agent.AgentRunCompleted.v1 and of rwb.decision.DecisionRecorded.v1 are registered with BACKWARD compatibility
    Then a payload that fails its subject is routed to the .dlt topic with an alert and the outbox row is kept until the relay succeeds
    Then no topic name outside the rwb.<short>.events.v1 pattern of the service is created by this story

  Scenario: AC5 The Temporal queue and the worker identity are the service's own (new, D-RCV-60)
    Given the Temporal cluster with namespace rwb-recovery
    When the worker of rwb-agent starts
    Then the task queue rwb-agent exists in namespace rwb-recovery and the worker polls that queue only
    Then the worker identity is the service identity of rwb-agent and holds no right on another service's queue
    Then a worker pointed at a queue outside the namespace, or at a queue that does not exist, fails the readiness check and does not roll out
    Then the concurrency, the poller count and the activity timeouts of the worker are reviewed values per environment and not template constants

  Scenario: AC6 The two budgets are measured and alerted (new, D-RCV-60)
    Given the platform metrics and alarms of the environment
    When a model call exceeds 60 seconds and a client call exceeds 2 seconds
    Then the 60 second model budget fires an alarm naming the endpoint and the agent code, and the run records TIMED_OUT with fallback true
    Then the 2 second client budget of the service's REST calls fires an alarm naming the caller and the operation
    Then both budgets are recorded as measured platform requirements with their target and their measurement point, and their exact alarm thresholds are Not specified in the source documents (GAP-0608; ASM-0854)
    Then the 60 second value is read from the policy row at run time and is not written in a chart value or a config map

  Scenario: AC7 Capacity and alarms cover a burst of runs and of evaluations (new, D-RCV-60)
    Given the reviewed request and limit of the rwb-agent pods and the scaling rule of its worker
    When a load test runs a burst of agent runs and a burst of evaluation runs on the queue
    Then no pod is killed for memory or CPU and the backlog returns to its baseline inside the reviewed time
    Then alarms fire on queue backlog, run throughput, fallback rate, error rate and the .dlt count, each with an owner role and a runbook entry
    Then the sizing figures and the alarm thresholds are reviewed values per environment, and their numbers are Not specified in the source documents (GAP-0608; ASM-0854)

  Scenario: AC8 The pipeline gates hold the boundary (new, D-RCV-60)
    Given the CI/CD pipeline of rwb-agent
    When a change is merged
    Then the pipeline runs the chart and policy checks, the identity and secret checks, the schema-grant check, the topic and subject checks, the contract tests against the fakes of RWB-P10-E1058-CON, and the boundary scan
    Then the boundary scan fails a build that reads another service's schema, names another service's topic or base, or writes a personal field into a payload
    Then the contract test step runs against the fakes of this key and not against a shared environment
    Then a failing gate blocks the merge and names the file and the violated rule

  Scenario: AC9 Each business rule BR1 to BR9 in section 8 is evidenced by a criterion, a guardrail or a boundary test (new, D-RCV-60)
    Given the delivered chart, environment values, topic, queue and provisioning artefacts of rwb-agent
    When the evidence of the business rules in section 8 is inspected
    Then BR1 is evidenced by AC1, BR2 by AC3, BR3 by AC2, BR4 by AC4, BR5 by AC5 and BR6 by AC6
    Then BR7 is evidenced by AC4, with every payload validated against its registry subject before the relay with BACKWARD compatibility
    Then BR8 is evidenced by the artefacts creating no table of their own, no business value, no bucket and no Schedule
    Then BR9 is evidenced by AC7 and by capacity and alarm values held as reviewed environment values per environment and never as template constants
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The only outside destination of rwb-agent is the Enterprise AI private endpoint INT-23, one hop, with TLS and mTLS; every other destination is dropped and alerted | Arch v5 slide 16; TSD P10 v2 T5.1 |
| BR2 | One schema and one login per service: the login holds grants on `rwb_agent` only, and no foreign key crosses a schema | DP-01; DP-02; §R4 |
| BR3 | Every secret, key, certificate and login comes from Key Vault through the workload identity and never from a file, a chart value, a config map, a log or a dashboard | Template and Rules §R7.2 s17 |
| BR4 | The topic follows the §R4 pattern `rwb.<short>.events.v1` with a retry topic and a `.dlt` topic, and only its owner produces to it | §R4; DP-09; DP-14 |
| BR5 | The task queue is `rwb-agent` in namespace `rwb-recovery`, and a worker polls only its own queue | §R4; Temporal and Drools design slide 11 |
| BR6 | The model call answers inside 60 seconds and then the rule result is used; every other REST hop keeps the 2 s client budget | NFR-010; R-UNI-32; DP-11; ADR-020 |
| BR7 | Every payload is validated against its registry subject before the relay, with BACKWARD compatibility | Arch v5 slide 42; DP-09 |
| BR8 | This story creates no table of its own, no business value, no bucket and no Schedule: the schema objects are created by the migration job of the service, and the agent artefacts are rows of `rwb_agent` | DP-15; ASM-0851 |
| BR9 | Capacity and alarm values are reviewed environment values and never template constants; the replica counts, resource requests and limits, probe paths and timings, start-up and rollout windows, and the alert thresholds and their windows are Not specified in the source documents (GAP-0609) and are set per environment at review; the blue-green mechanism is Not specified in the source documents (GAP-0609) | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not provisioned | Schema and login created | The schema exists and the login holds grants on it only | Ready (data) |
| Not provisioned | Path opened | The egress entry, the TLS and mTLS handshake and the reviewed port are in place | Reachable |
| Reachable | Identity and secrets wired | The Key Vault entries are read by the workload identity and the handshake succeeds | Ready (boundary) |
| Ready (data), Ready (boundary) | Topic and queue created | The topic, its two related topics, its subjects and the queue exist | Ready (producing) |
| Ready (producing) | A subject drift or a secret rotation | The registry subject changes incompatibly, or the certificate is rotated | Degraded or Ready (rotated) |
| Degraded | A policy, grant, identity or certificate check fails after a platform change | The egress list, the grant, the login or the certificate drifts | Degraded; the environment is not marked ready |
| Degraded | The drift is corrected | The reviewed value is restored and the checks pass | Ready |

These are the states of the environment of this service, not of a case or a run. No `rwb_agent` row and no run status is changed by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the egress allow-list, the login, the Key Vault entries, the topic, the queue, the sizing, the alarms and the pipeline gates |
| ACE platform team | Owns the cluster, the service mesh, Key Vault, the certificate authority, the Kafka platform, the schema registry and the Temporal cluster this story configures against |
| Security | Approves the egress entry, the identity grants, the secret references and the producer ACL |
| ACE database administrator | Creates schema `rwb_agent`, the service login and its grants, and confirms that no grant exists on another schema |
| The rwb-agent owner team | Confirms the sizing, the concurrency and the budgets after the load test, and consumes the endpoint reference, the topic and the queue |
| Platform administrator (RW-PLATADM) | Rotates the certificate, extends the retention when the requirement changes and acts on an alarm |
| RW-SECADM | Holds the break-glass right on the secret material and approves a rotation record |

The login name, the Key Vault entry names, the certificate subject, the endpoint host and port, the partition count, the retention, the pool cap, the sizing figures and the alarm thresholds are Not specified in the source documents (GAP-0606, GAP-0608; ASM-0848, ASM-0854); this story fixes their shape and leaves the values to the environment configuration.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Network | The egress allow-list of the rwb-agent pods: the INT-23 private endpoint, one hop, reviewed port, TLS and mTLS; every other outside destination dropped and alerted | BR1 |
| Identity | The rwb-agent login (DP-02) on schema `rwb_agent`; the workload identity the pods run as; the Temporal worker identity | BR2 |
| Key Vault entries | The login secret reference, the client certificate and key of the model gateway call, and the endpoint reference; read by the workload identity at run time | BR3 |
| Schema | `rwb_agent`, created by the ACE database administrator and migrated by the service's own Flyway sequence, whose first file is V10_001__agent_runtime.sql for the six agent tables and whose later migrations take the next numbers of the sequence; the agent tables and the library objects of section 12.7 of RWB-P10-E1058-CON | BR2; BR8 |
| Topic | `rwb.agent.events.v1` with its retry topic and its `.dlt` topic; producer right for rwb-agent only; reviewed partitions and retention; EV-28 AgentRunCompleted is the only member of the family the sources name; any further member is Not specified in the source documents (GAP-0607) | BR4 |
| Registry subjects | `rwb.agent.AgentRunCompleted.v1` and `rwb.decision.DecisionRecorded.v1`, BACKWARD compatibility | BR7 |
| Queue | `rwb-agent` in namespace `rwb-recovery`, with the worker identity, the concurrency, the poller count and the activity timeouts | BR5 |
| Sizing and alarms | Request and limit per environment, the scaling rule of the worker, and the alarms on backlog, throughput, fallback rate, error rate, `.dlt` count, the 60 second model budget and the 2 second client budget | BR6; BR9 |
| Gates | Chart and policy checks, identity and secret checks, schema-grant check, topic and subject checks, the contract tests of the key's fakes and the boundary scan | BR1; BR2; BR3; BR4; BR7 |

The topology holds no business data and no personal data. The endpoint host and port, the certificate subject, the Key Vault entry names, the partition count, the retention, the pool cap, the sizing figures and the alarm thresholds are Not specified in the source documents (GAP-0608; ASM-0854) and are reviewed values per environment, recorded at the build and never template constants (BR9). No Blob container is named for agent artefacts by any source: the policies, the prompts, the samples, the runs and the evaluations are rows of `rwb_agent` (BR8).

### 12. Contract

#### 12.1 REST operations provided

None. This story exposes no API, no operator endpoint and no cache read. The health and readiness endpoints are cluster-internal and belong to RWB-P10-E1058-OPS.

#### 12.2 REST operations consumed

None as a business operation. The path to the Enterprise AI private endpoint is a platform route configured here; the call that runs on it is declared in RWB-P10-E1058-CON and written by RWB-P10-E1058-APP. The routes to rwb-case, rwb-document and rwb-access are opened by the platform egress rule and add no call of their own.

#### 12.3 Events published

None by this story as code. The topic `rwb.agent.events.v1`, its retry topic and its `.dlt` topic, the producer right of rwb-agent and the registry subjects of EV-28 and of the record event are provisioned here and declared in RWB-P10-E1058-CON; the payload is written by RWB-P10-E1058-APP.

#### 12.4 Events consumed

None. This story provisions no consumer group for rwb-agent and reads no message; the consumers of this key's events are rwb-decision, rwb-document and rwb-deviation, and their groups are theirs.

#### 12.5 Workflows and activities

None created. The task queue `rwb-agent` in namespace `rwb-recovery`, the worker identity, the concurrency, the poller count and the activity timeouts are provisioned here; AgentRunWorkflow and its six activities belong to RWB-P10-E1058-APP and are declared in RWB-P10-E1058-CON.

#### 12.6 Schedules

None. This story creates no Temporal Schedule and changes none: the Arch v5 job map names no job for the agent platform (slide 44), a run is started by a calling step and an evaluation by a user request.

#### 12.7 Tables owned

None. This story creates no table, no column and no index and issues no migration; the schema, the login and its grants are the whole database part of the deliverable. The agent tables are created by the migration job of the service, and their keys are declared in RWB-P10-E1058-CON (ASM-0856).

#### 12.8 Contract fakes

None deployed. The fakes of this key - rwb-case, rwb-document, rwb-access, rwb-decision, the gateway-bff route, the model gateway, the decision-record library and the outbox - run in the pipeline and are declared in RWB-P10-E1058-CON; this story only wires the contract test step that calls them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided or consumed | The egress path to INT-23 and to the owner services is a platform route; the operations on it belong to RWB-P10-E1058-CON and RWB-P10-E1058-APP |
| Kafka | 1 topic with 2 related topics | `rwb.agent.events.v1`, its retry topic and its `.dlt` topic, with the producer right of rwb-agent and two registry subjects |
| Temporal | 1 task queue | `rwb-agent` in namespace `rwb-recovery`, with the worker identity and the reviewed concurrency; no workflow is created here |
| File | None | This story reads and writes no file and creates no bucket or container |

### 13. Solution plan

**Deliverables.** `infra/network/egress.yaml` (the allow-list entry of INT-23 and the drop rule), `infra/identity/rwb-agent-login.json` (the schema, the login, its grants and the workload identity), `infra/keyvault/entries.md` (the login secret, the client certificate and key, the endpoint reference and the rotation), `infra/kafka/agent-topic.yaml` (the topic, the retry topic, the `.dlt` topic, the producer ACL and the two subjects), `infra/temporal/agent-queue.yaml` (the queue, the namespace, the worker identity, the concurrency and the activity timeouts), `infra/observability/budgets.yaml` (the 60 second and 2 second budgets with their metrics and alarms), `infra/sizing/agent-runs.yaml` (the request, the limit and the scaling rule) and `pipeline/gates.yaml` (the five gates).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | none here; the registry subject is wired here |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | none here; the app story holds the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | none here |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | none here; the route to it is opened here |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story; the topic and the producer ACL are provisioned here |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none here; the budgets are measured here |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story; the schema and the login are provisioned here |
| DP-19 | Screen, ace-web | gateway-bff composite route | none here; the route belongs to the app and deployment stories |
| DP-20 | Agent client | rwb-agent contract | none here; the queue that carries the run is provisioned here |

DP-09 is the pattern this story serves most directly: the topic, its retry and `.dlt` topics, the producer right and the two registry subjects are provisioned here and written by the app story. DP-11 is served by the measured budgets of AC6. DP-02 is served by the login and the workload identity of AC2 and AC3. DP-15 is served by the schema and its Flyway history of AC3. No other pattern adds work here; no table, no Schedule and no business value is created.

**Build steps**

1. Write the egress entry and the drop rule, and test a call to INT-23 and a call to an unlisted destination (AC1, X1).
2. Create the schema and the login with grants on `rwb_agent` only, and verify that another schema is refused and that a cross-schema foreign key fails the gate (AC3, X4).
3. Create the Key Vault entries and wire them to the workload identity; test a valid, an expired and an unissued client certificate, and run the secret scan (AC2, X2, X3).
4. Provision the topic, the retry topic, the `.dlt` topic and the producer ACL; test a refused foreign producer and a `.dlt` route (AC4, X5, X6).
5. Register the two registry subjects with BACKWARD compatibility and test a payload that fails its subject (AC4, X5).
6. Provision the queue, the worker identity and the worker concurrency in namespace `rwb-recovery`, and test a worker pointed at a foreign queue (AC5, X7).
7. Wire the two budget metrics and their alarms, with the 60 second value read from the policy row at run time and not from a chart value (AC6, X8).
8. Size the pods, run the two burst load tests, record the reviewed values and set the five alarms with their runbook entries (AC7, X9).
9. Add the five pipeline gates and run them once on a change that names another schema and another service's topic (AC8, X10).
10. Hand the endpoint reference, the login reference, the topic names and the queue to the app and contract stories of this key, and the metrics and alarms to RWB-P10-E1058-OPS.

**Done when.** The path is one hop and authenticated in all three environments, no secret sits outside Key Vault, the schema and the login exist with grants on `rwb_agent` only, the topic and its two related topics exist with the producer right of rwb-agent only, the queue and the worker identity are the service's own, both budgets fire their alarms in a test, the two burst load tests pass inside the reviewed values, and the five gates block a boundary violation.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| None | A path, identity, secret, schema, grant, topic, queue, budget, sizing or gate check fails | No business message is produced. The provisioning check or the pipeline fails with the resource name and the violated rule, and the platform administrator or the build owner acts on it. |

This story adds no message ID. The business messages of the capability keep their identifiers and texts from the legacy story and are declared in RWB-P10-E1058-CON: MSG-P10-001, MSG-P10-002, MSG-P10-003, MSG-P7-002, MSG-GEN-004, MSG-P4-002 and MSG-GEN-001. The infrastructure reports a condition to the operator, never to a workbench user.

### 15. Screens and states

None. There is no screen in this story. SCR-46 states: empty: Not specified in the source documents (CG-ALL-2533); loading: Not specified in the source documents (CG-ALL-2533); error: Not specified in the source documents (CG-ALL-2533); no access: Not specified in the source documents (CG-ALL-2533). The operator-facing surfaces are the environment provisioning check, the egress and ACL views, the Key Vault rotation record, the load-test report and the alarm page with its runbook entries. The agent monitor screen SCR-46 and its dashboard belong to RWB-P10-E1063-APP, and the agent screens themselves are out of scope here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E1058-INF-01 | AC1, BR1 | NFR | The DEV, SIT and UAT egress lists; a handshake to INT-23 with a valid, an expired and an unissued client certificate; a call to an unlisted destination |
| TC-P10-E1058-INF-02 | AC2, BR3 | NFR | The Key Vault read of the login secret, the certificate and the endpoint reference by the workload identity; the secret scan of the chart, the values and the logs; a certificate rotation |
| TC-P10-E1058-INF-03 | AC3, BR2 | NFR | Schema `rwb_agent` and its Flyway history; the login grants on that schema only; a read of another schema refused; a cross-schema foreign key refused by the gate; the pool cap |
| TC-P10-E1058-INF-04 | AC4, BR4, BR7 | Integration | The topic, its retry and `.dlt` topics, a foreign producer refused, a payload failing its subject routed to `.dlt`, and the two registry subjects |
| TC-P10-E1058-INF-05 | AC5, BR5 | Integration | The queue in namespace `rwb-recovery`, a worker on its own queue, and a worker pointed at a foreign queue that fails readiness |
| TC-P10-E1058-INF-06 | AC6, BR6 | NFR | A model call of 61 seconds and a client call over 2 seconds; the two alarms and the run recorded as TIMED_OUT with fallback true |
| TC-P10-E1058-INF-07 | AC7 | NFR | Two burst load tests on the queue; no pod killed for memory or CPU; the five alarms with their runbook entries |
| TC-P10-E1058-INF-08 | AC8 | Integration | A change that reads another schema, names another service's topic and writes a personal field; the five gates and the block of the merge |
| TC-P10-E1058-INF-09 | AC9, BR8, BR9 | Integration | The delivered chart, environment values and provisioning artefacts inspected for no table of their own, no business value, no bucket and no Schedule, and for capacity and alarm values held per environment and not as template constants; the evidence of BR1 to BR7 traced to AC1 to AC6 |

### 17. Guardrails

- No business value in a policy, a values file or a config map: the model code and version, the timeout, the floor, the tool list and the price stay rows of `agent_policy`, and the 60 seconds is read at run time (BR6, BR9).
- No personal data in a topic message, a log, an alarm payload or a test fixture: identifiers and facts only, and the masked inputs stay inside the run and the record.
- One login, one workload identity, one worker identity and one producer right; no other service's identity holds a grant on the agent topic, the agent queue or the service's secrets (BR2, BR4).
- No secret, key, certificate or login password in a file, a chart value, a config map, a log or a dashboard; everything comes from Key Vault through the workload identity (BR3).
- The only outside destination is INT-23; the egress list is a reviewed entry and a call outside it is dropped and alerted (BR1).
- No `rwb_*` table, no migration, no bucket and no Schedule is created here; the storage of the agent artefacts is the `rwb_agent` tables (BR8).
- The registry subjects are BACKWARD compatible, and a breaking change is a new version of the payload with the consumers' agreement (BR7).
- Every fixture and every load-test payload is synthetic; no production account, document, model answer or record is used.

### 18. Traceability

| Requirement ID | Requirement (short) | Infrastructure element | Test cases |
|---|---|---|---|
| REQ-ACA-010 | Agents run under service identities with the same role checks as people | The rwb-agent login and workload identity, the worker identity and the producer right | TC-P10-E1058-INF-02, TC-P10-E1058-INF-04, TC-P10-E1058-INF-05 |
| REQ-ACA-005 | Personal data masked by role in every agent call | The private path and the boundary request that carries the masked inputs only; no personal field in a payload or a log | TC-P10-E1058-INF-01, TC-P10-E1058-INF-02 |
| REQ-DRI-010 | Every threshold, limit and name is versioned and changed without a code release | The 60 second budget read from the policy row at run time and the reviewed environment values | TC-P10-E1058-INF-06 |
| NFR-010 | An agent answers within 60 seconds, after which the rule result is used | The 60 second model budget with its metric and alarm | TC-P10-E1058-INF-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The one-hop egress list and the measured 2 second client budget | TC-P10-E1058-INF-01, TC-P10-E1058-INF-06 |
| D-RCV-60 DP-09, DP-14 | Kafka with outbox, inbox and CloudEvents; one topic per service | The topic, its retry and `.dlt` topics, the producer ACL and the two registry subjects | TC-P10-E1058-INF-04 |
| D-RCV-60 DP-01, DP-02, DP-15 | One schema and one login per service, migrated by the service's own sequence | The schema `rwb_agent`, the login and its grants, the boundary scan gate | TC-P10-E1058-INF-03, TC-P10-E1058-INF-08 |
| ASM-0850 | The run is a workflow on the service's own queue with the 60 second budget, and every other hop keeps 2 s | The queue, the worker identity, the concurrency and the two budgets | TC-P10-E1058-INF-05, TC-P10-E1058-INF-06 |

### 19. Out of scope

- The operations, the gateway client, the store, the guardrail, the harness and the workflow (RWB-P10-E1058-APP).
- The contract shapes of the operations, the schema keys, the event payloads and the fakes (RWB-P10-E1058-CON).
- The chart, the pipeline, the migration job, the configuration and secrets injection, the probes, the dashboards, the alerts of the application and the runbook (RWB-P10-E1058-OPS).
- The `rwb_agent` schema design, its tables and its migrations: they belong to RWB-P10-E1058-APP and to the later P10 stories; this story provisions the schema and the login only.
- The four other agent keys of the service and the TDR offer-suggestion key, with their own endpoints, topics and queues.
- The Kafka platform, the schema registry, the Temporal cluster, Key Vault, the certificate authority and the service mesh as platform products (RWB-PLT-EVT, RWB-PLT-LIB, RWB-PLT-WF).
- The Enterprise AI model, its answer shape and its own platform, beyond the private path and the request this story carries.
- The endpoint host and port, the certificate subject, the Key Vault entry names, the login name, the partition count, the retention, the pool cap, the sizing figures and the alarm thresholds, which are Not specified in the source documents (GAP-0606, GAP-0608; ASM-0848, ASM-0854).
