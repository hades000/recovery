# RWB-P10-E2032-INF TDR offer-suggestion model through the model gateway [E3e]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2032-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | L-P10-G |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-032 for rwb-agent. The suggestion call moves from an in-process client to the Enterprise AI private endpoint INT-23 across a network boundary, and the run completion moves onto the service's own topic, so this key needs a path, an identity, a topic with its retry and `.dlt` topics, a queue, a measured budget and a pipeline gate that the monolith never had. This story provisions and configures only: the private path and egress allow-list to INT-23 with TLS and mTLS, the service login and the secret handling for the model gateway, the topic `rwb.agent.events.v1` with the producer ACL, the Temporal task queue `rwb-agent` in namespace `rwb-recovery`, the 60-second and 2-second budgets as measured platform requirements, capacity and alarms for agent runs, and the CI/CD gates. It creates no table, no business value and no invented resource name. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the private network path and the egress allow-list to the Enterprise AI private endpoint (INT-23) with TLS and mTLS, the rwb-agent service login with its secrets and credential handling for the model gateway, the Kafka topic `rwb.agent.events.v1` with its retry and `.dlt` topics and the producer ACL of rwb-agent, the Temporal task queue `rwb-agent` in namespace `rwb-recovery` with its worker identity, the 60-second model-call budget and the 2-second client budget measured as platform requirements, capacity and alarms for agent runs, and the CI/CD gates of the service**, so that **the TDR suggestion call leaves the cluster only through one approved private path, the statuses of a run reach the topic that rwb-decision, rwb-document and rwb-deviation read, and a timeout or a burst is seen and alerted before an officer sees a missing suggestion**.

### 2. Business rationale

The legacy key RWB-E2-032 was written inside one monolith: `ModelGatewayClient` called the Enterprise AI endpoint from the same process, the run row and the decision log entry were written in the same schema, and the run completion never left the database. In the target the model is reached on a private endpoint of the SCB tenant, outside the cluster, and the run completion is a Kafka message on the service's own topic (Arch v5 slides 8, 16 and 41; TSD P10 v2 T5.1). That is three new infrastructure facts the monolith did not need: a network path with a certificate on both sides, an identity that holds the secret of that path, and a topic with a producer right and a dead-letter route.

The target also fixes the two waits that decide whether a suggestion is useful. An agent must answer inside 60 seconds, after which the rule result is used and the case still routes (NFR-010; Arch v5 slide 35: "rwb-agent: 60 s, or the rule result is used"). Every other hop of the service keeps the 2-second client budget of ADR-020. Today neither is measured on the platform: a call that hangs is seen only as a slow screen, and a burst of runs is seen only when the treatment screen stops answering. This story makes both measurable and alertable.

Without the path the call cannot be made at all. Without the identity and the secret handling, the path cannot be authenticated and a certificate ends up in a chart value. Without the topic and its `.dlt`, a run that completed is invisible to the three consuming services and a bad payload is lost silently. Without the budget and the alarms, the fallback of R-UNI-32 is invisible and a capacity problem is diagnosed from complaints.

This story creates no `rwb_*` table, no business value and no bucket of its own: policies, prompts and samples are rows of `rwb_agent` (`agent_policy`, `agent_prompt`, `agent_sample`, TSD P10 v2 T3.1), and no source names a Blob container for agent artefacts (GAP-0635; ASM-0990).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), and the service follows the §R4 naming: schema `rwb_agent`, REST base `/api/recovery/agent/v1`, topic `rwb.agent.events.v1`, task queue `rwb-agent`, login per service, Java package `th.co.scb.ace.workbench.recovery.agent`.
- The ACE AKS cluster, the shared Azure App Gateway and the platform service mesh are in force, with the workload identity mechanism of the platform, so no credential sits in a file, a chart or a repository (Arch v5 slides 7 and 8).
- The Enterprise AI private endpoint (INT-23) exists in the SCB tenant and its certificate authority is known to the platform; its host, port and certificate subject are Not specified in the source documents (GAP-0635; ASM-0988).
- The Kafka event platform and the schema registry are available (RWB-PLT-EVT, RWB-PLT-N008-INF), because a produced payload is validated against its subject before the outbox relay publishes it (DP-09; DP-14).
- The Temporal cluster runs namespace `rwb-recovery` with one task queue per service, and the worker of each service polls only its own queue (§R4; Temporal and Drools design slide 11).
- The decision-record library and the outbox library of RWB-PLT-E1027-CON and RWB-PLT-TE006-CON are the platform components whose secrets and destinations this story configures; this story does not build them.
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in lane L-P10-G.

### 4. Flow

1. Open the private network path from the rwb-agent pods to the Enterprise AI private endpoint (INT-23) in each environment, with TLS on the wire and mTLS to the endpoint, and record the destination as a reviewed entry of the egress allow-list.
2. Provision the rwb-agent service login on schema `rwb_agent` with grants on its own schema only, and the service identity the pods run as.
3. Create the Key Vault entries the model gateway needs — the client certificate and key, and the endpoint reference — and wire them to the workload identity through the platform secret mechanism, so no literal value reaches a values file, a chart template, a log or a dashboard.
4. Provision the topic `rwb.agent.events.v1` with its retry topic and its `.dlt` topic, its partitions and retention as reviewed environment values, and grant rwb-agent the producer right on the topic and its retry topic only.
5. Register the payload subjects of EV-28 in the schema registry with BACKWARD compatibility, so the producer validates before the relay publishes.
6. Provision the Temporal task queue `rwb-agent` in namespace `rwb-recovery`, and the worker identity and the concurrency the worker may use on it.
7. Make the two budgets measurable: a platform metric and an alarm on the 60-second model call, and a platform metric and an alarm on the 2-second client budget of the service's REST calls.
8. Size the pods for a burst of agent runs, record the request and limit per environment, and set the alarms on queue backlog, run throughput, fallback rate and error rate.
9. Add the CI/CD gates of the service: the chart and policy checks, the identity and secret checks, the topic and subject checks, the contract tests of the four fakes, and the boundary scan that fails a build reading another schema or naming another service's topic.
10. Hand the endpoint reference, the topic names and the queue to RWB-P10-E2032-APP and RWB-P10-E2032-CON, and the metrics and alarms to the operations stories of the service epic.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A pod calls a destination outside the egress allow-list | The network policy drops the call; the attempt is counted and alerted and the run holds status "TOOL_UNAVAILABLE" or "MODEL_ERROR" | None | AC1 |
| X2 | The mTLS handshake to INT-23 fails: the certificate is missing, expired or not issued by the platform authority | The model call fails before any request body is sent; the run holds MODEL_ERROR with fallback true and nothing is written as a suggestion | None | AC1, AC2 |
| X3 | A secret, a key or a certificate body appears in a values file, a chart template, a log or a dashboard | The pipeline secret scan fails the build or the release, and the entry is rotated | None | AC2 |
| X4 | A produced EV-28 payload fails its registry subject, or the topic is unreachable | The message is refused before the relay and routed to the `.dlt` topic with an alert; the outbox row stays until the relay succeeds | None | AC3 |
| X5 | A producer outside rwb-agent attempts to write to `rwb.agent.events.v1` | The ACL refuses the write and the attempt is alerted | None | AC3 |
| X6 | The worker polls a queue that is not its own, or the queue is missing in the namespace | The worker does not start, the readiness check fails and the deployment does not roll out | None | AC4 |
| X7 | The model call exceeds the 60-second budget, or a client call exceeds the 2-second budget | The alarm fires with the endpoint and the caller named, and the run records TIMED_OUT with fallback true | None | AC5 |
| X8 | A burst of agent runs raises the queue backlog and the pod saturation | The alarm fires, the worker scales as configured and the run continues when capacity returns; no run is dropped silently | None | AC6 |
| X9 | A gate is bypassed, or a build names another schema or another service's topic | The pipeline refuses the merge and the boundary scan names the file and the string | None | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Provisions a path, an identity, secrets, a topic, a queue, metrics and gates; no application code is built here and no in-lane story blocks it |
| Negotiable | The retention, the partition count, the heap values, the ports and the alarm thresholds are environment values settled with the platform team, not story decisions |
| Valuable | Makes the INT-23 call possible and authenticated, makes the run completion reach its three consumers, and makes the fallback of R-UNI-32 visible before an officer notices |
| Estimable | One path and its allow-list, one login and one identity, two Key Vault entries, one topic with two related topics and a producer grant, one queue and one worker identity, two budgets with their alarms, one sizing decision and five pipeline gates |
| Small | Fits one sprint with the provisioning and gate checks |
| Testable | Every criterion tests an artefact: a handshake, a dropped call, a secret scan, a refused write, a `.dlt` route, an alarm, a load test and a gate run |

### 7. Acceptance criteria

```gherkin
Feature: Infrastructure for the TDR offer-suggestion model in rwb-agent

  Background:
    Given the ACE AKS cluster, the platform service mesh, Key Vault and the Kafka platform are in force
    Given the service naming rule of section R4 of the template is in force

  Scenario: AC1 The private path to INT-23 is one hop with TLS and mTLS (new, D-RCV-60)
    Given the egress allow-list of the rwb-agent pods in each environment
    When the allowed destinations are inspected and a model call is made
    Then the Enterprise AI private endpoint (INT-23) is allowed, one hop, on the reviewed port, and no other outside destination is reachable
    Then the connection uses TLS, and the endpoint presents a certificate the platform certificate authority trusts and rwb-agent presents its client certificate
    Then a call to a destination outside the list is dropped, counted and alerted, and the run records the mapped status with fallback true
    Then the path is provisioned per environment and the destination is a reviewed entry and not a template constant

  Scenario: AC2 The service login and the gateway secrets are held in Key Vault only (new, D-RCV-60)
    Given the rwb-agent service login and the workload identity of the environment
    When the pods start and call the model gateway
    Then the login has grants on schema rwb_agent only, and holds no right on another schema
    Then the client certificate, its key and the endpoint reference are read from Key Vault by the workload identity at run time
    Then no secret, key or certificate body appears in a values file, a chart template, a log, a config map or a dashboard, and the pipeline secret scan fails the build when one does
    Then the rotation of the certificate and of the endpoint reference is a Key Vault operation with no rebuild of the service

  Scenario: AC3 The agent topic and its two related topics exist with a producer ACL (new, D-RCV-60)
    Given the Kafka platform of the environment
    When the topics and the ACLs are inspected
    Then rwb.agent.events.v1 exists with its retry topic and its .dlt topic, with the reviewed partitions and retention
    Then rwb-agent holds the producer right on rwb.agent.events.v1 and on its retry topic only, and a producer outside rwb-agent is refused
    Then the payload subjects of rwb.agent.AgentRunCompleted.v1 and of rwb.decision-record.DecisionRecorded.v1 are registered with BACKWARD compatibility
    Then a payload that fails its subject is routed to the .dlt topic with an alert and the outbox row is kept until the relay succeeds
    Then no topic name outside the rwb.<short>.events.v1 pattern of the service is created by this story

  Scenario: AC4 The Temporal queue and the worker identity are its own (new, D-RCV-60)
    Given the Temporal cluster with namespace rwb-recovery
    When the worker of rwb-agent starts
    Then the task queue rwb-agent exists in namespace rwb-recovery and the worker polls that queue only
    Then the worker identity is the service identity of rwb-agent and holds no right on another service's queue
    Then a worker pointed at a queue outside the namespace, or at a queue that does not exist, fails the readiness check and does not roll out
    Then the concurrency and the poller count of the worker are reviewed values per environment and not template constants

  Scenario: AC5 The two budgets are measured and alerted (new, D-RCV-60)
    Given the platform metrics and alarms of the environment
    When a model call exceeds 60 seconds and a client call exceeds 2 seconds
    Then the 60-second model budget fires an alarm naming the endpoint and the agent code, and the run records TIMED_OUT with fallback true
    Then the 2-second client budget of the service's REST calls fires an alarm naming the caller and the operation
    Then both budgets are recorded as measured platform requirements with their target and their measurement point, and their exact alarm thresholds are Not specified in the source documents (GAP-0635; ASM-0989)
    Then the 60-second value is read from the policy row at run time and is not written in a chart value or a config map

  Scenario: AC6 Capacity and alarms cover a burst of agent runs (new, D-RCV-60)
    Given the reviewed request and limit of the rwb-agent pods and the scaling rule of its worker
    When a load test runs a burst of agent runs on the queue
    Then no pod is killed for memory or CPU and the backlog returns to its baseline inside the reviewed time
    Then alarms fire on queue backlog, run throughput, fallback rate and error rate, each with an owner role and a runbook entry
    Then the sizing figures and the alarm thresholds are reviewed values per environment, and their numbers are Not specified in the source documents (GAP-0635; ASM-0991)

  Scenario: AC7 The pipeline gates hold the boundary (new, D-RCV-60)
    Given the CI/CD pipeline of rwb-agent
    When a change is merged
    Then the pipeline runs the chart and policy checks, the identity and secret checks, the topic and subject checks, the contract tests against the four fakes and the boundary scan
    Then the boundary scan fails a build that reads another service's schema or names another service's topic or base
    Then the contract test step runs against the fakes of this key and not against a shared environment
    Then a failing gate blocks the merge and names the file and the violated rule
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The only outside destination of rwb-agent is the Enterprise AI private endpoint (INT-23), one hop, with TLS and mTLS | Arch v5 slide 16; TSD P10 v2 T5.1 |
| BR2 | One login per service with grants on its own schema only; one workload identity per service | DP-02; §R4 |
| BR3 | Every secret, key and certificate comes from Key Vault through the workload identity and never from a file, a chart value, a config map, a log or a dashboard | Template and Rules §R7.2 s17 |
| BR4 | The topic follows the §R4 pattern `rwb.<short>.events.v1` with a retry topic and a `.dlt` topic, and only its owner produces to it | §R4; DP-09; DP-14 |
| BR5 | The task queue is `rwb-agent` in namespace `rwb-recovery`, and a worker polls only its own queue | §R4; Temporal and Drools design slide 11 |
| BR6 | The model call answers inside 60 seconds and then the rule result is used; every other REST hop keeps the 2 s client budget | NFR-010; R-UNI-32; DP-11; ADR-020 |
| BR7 | Every payload is validated against its registry subject before the relay, with BACKWARD compatibility | Arch v5 slide 42; DP-09 |
| BR8 | This story creates no `rwb_*` table, no business value and no bucket: policies, prompts and samples are rows of `rwb_agent` | TSD P10 v2 T3.1; GAP-0635 |
| BR9 | Capacity and alarm values are reviewed environment values and never template constants | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not provisioned | Path opened | The egress entry, the TLS and mTLS handshake and the reviewed port are in place | Reachable |
| Reachable | Identity and secrets wired | The Key Vault entries are read by the workload identity and the handshake succeeds | Ready |
| Ready | Topic and queue created | The topic, its two related topics, its subjects and the queue exist | Ready (producing) |
| Ready (producing) | A subject drift or a secret rotation | The registry subject changes incompatibly, or the certificate is rotated | Degraded or Ready (rotated) |
| Degraded | A policy, identity or certificate check fails after a platform change | The egress list, the grant or the certificate drifts | Degraded; the environment is not marked ready |
| Degraded | The drift is corrected | The reviewed value is restored and the checks pass | Ready |

These are the states of the environment of this service, not of a case, a run or a treatment. No `rwb_agent` table and no run status is changed by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the egress allow-list, the login, the Key Vault entries, the topic, the queue, the sizing, the alarms and the pipeline gates |
| ACE platform team | Owns the cluster, the service mesh, Key Vault, the certificate authority, the Kafka platform, the schema registry and the Temporal cluster this story configures against |
| Security | Approves the egress entry, the identity grants, the secret references and the producer ACL |
| The rwb-agent owner team | Confirms the sizing and the budgets after the load test, and consumes the endpoint reference, the topic and the queue |
| Platform administrator (RW-PLATADM) | Rotates the certificate, extends the retention when the requirement changes and acts on an alarm |
| ACE database administrator | Confirms that the rwb-agent login holds grants on `rwb_agent` only |
| RW-SECADM | Holds the break-glass right on the secret material and approves a rotation record |

The login name, the Key Vault entry names, the certificate subject, the endpoint host and port, the partition count, the retention and the alarm thresholds are Not specified in the source documents (GAP-0635; ASM-0988, ASM-0989, ASM-0990, ASM-0991); this story fixes their shape and leaves the values to the environment configuration.

### 11. Data

| Item | Content |
|---|---|
| Network | The egress allow-list of the rwb-agent pods: the INT-23 private endpoint, one hop, reviewed port, TLS and mTLS; no other outside destination |
| Identity | The rwb-agent service login on schema `rwb_agent`; the workload identity the pods run as |
| Key Vault entries | The client certificate and key of the model gateway call, and the endpoint reference; read by the workload identity at run time |
| Topic | `rwb.agent.events.v1` with its retry topic and its `.dlt` topic; producer right for rwb-agent only; reviewed partitions and retention |
| Registry subjects | `rwb.agent.AgentRunCompleted.v1` and `rwb.decision-record.DecisionRecorded.v1`, BACKWARD compatibility |
| Queue | `rwb-agent` in namespace `rwb-recovery`, with the worker identity and the reviewed concurrency |
| Sizing and alarms | Request and limit per environment, the scaling rule of the worker, and the alarms on backlog, throughput, fallback rate, error rate, the 60-second model budget and the 2-second client budget |
| Gates | Chart and policy checks, identity and secret checks, topic and subject checks, the contract tests of the four fakes and the boundary scan |

The topology holds no business data and no personal data. The endpoint host and port, the certificate subject, the Key Vault entry names, the partition count, the retention periods, the sizing figures and the alarm thresholds are Not specified in the source documents (GAP-0635; ASM-0988, ASM-0989, ASM-0990, ASM-0991) and are reviewed values per environment. No Blob container is named for agent artefacts by any source: the policies, the prompts and the samples are rows of `agent_policy`, `agent_prompt` and `agent_sample` in `rwb_agent` (BR8).

### 12. Contract

#### 12.1 REST operations provided

None. This story exposes no API, no operator endpoint and no cache read. The health and readiness endpoints are cluster-internal and belong to the operations stories of the service epic.

#### 12.2 REST operations consumed

None as a business operation. The path to the Enterprise AI private endpoint is a platform route configured here; the call that runs on it is declared in RWB-P10-E2032-CON and consumed by RWB-P10-E2032-APP. The path to rwb-source-data, rwb-treatment, rwb-case and rwb-decision is opened by the platform egress rule and adds no call of its own.

#### 12.3 Events published

None by this story as code. The topic `rwb.agent.events.v1`, its retry topic and its `.dlt` topic, the producer right of rwb-agent and the registry subjects of EV-28 and of the record event are provisioned here and declared in RWB-P10-E2032-CON. The payload is written by RWB-P10-E2032-APP.

#### 12.4 Events consumed

None. This story provisions no consumer group for rwb-agent and reads no message; the service consumes no topic for this key.

#### 12.5 Workflows and activities

None created. The task queue `rwb-agent` in namespace `rwb-recovery`, the worker identity and the worker concurrency are provisioned here; AgentRunWorkflow and its four activities belong to RWB-P10-E2032-APP and to the baseline RWB-P10-E1058-CON.

#### 12.6 Schedules

None. The suggestion is request-driven and no Temporal Schedule is created, changed or owned by this story (Arch v5 slide 44 names no job for an agent suggestion).

#### 12.7 Tables owned

None. This story creates no `rwb_*` table, no column and no index and issues no migration; the login and its grants on `rwb_agent` are the whole database part of the deliverable.

#### 12.8 Contract fakes

None deployed. The four fakes of this key — rwb-treatment, rwb-decision, rwb-case and the model gateway — run in the pipeline and are declared in RWB-P10-E2032-CON; this story only wires the contract test step that calls them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided or consumed | The egress path to INT-23 and to the four owner services is a platform route; the operations on it belong to RWB-P10-E2032-CON and RWB-P10-E2032-APP |
| Kafka | 1 topic with 2 related topics | `rwb.agent.events.v1`, its retry topic and its `.dlt` topic, with the producer right of rwb-agent and two registry subjects |
| Temporal | 1 task queue | `rwb-agent` in namespace `rwb-recovery`, with the worker identity and the reviewed concurrency; no workflow is created here |
| File | None | This story reads and writes no file and creates no bucket or container |

### 13. Solution plan

**Deliverables.** `infra/network/egress.yaml` (the allow-list entry of INT-23 and the drop rule), `infra/identity/rwb-agent-login.json` (the login, its grants on `rwb_agent` and the workload identity), `infra/keyvault/entries.md` (the client certificate, its key and the endpoint reference, with the rotation), `infra/kafka/agent-topic.yaml` (the topic, the retry topic, the `.dlt` topic, the producer ACL and the two subjects), `infra/temporal/agent-queue.yaml` (the queue, the namespace and the worker identity), `infra/observability/budgets.yaml` (the 60-second and 2-second budgets with their metrics and alarms), `infra/sizing/agent-runs.yaml` (the request, the limit and the scaling rule) and `pipeline/gates.yaml` (the five gates).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON for the app story; the registry subject is wired here |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | none here; the app story holds the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | none here |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story; the topic and the producer ACL are provisioned here |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none here; the budgets are measured here |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | none here; the route belongs to the app story |

DP-09 is the pattern this story serves: the topic, its retry and `.dlt` topics, the producer right and the two registry subjects are provisioned here, and the payload is written by the app story. DP-11 is served by the measured budgets of AC5. DP-02 is served by the login and the workload identity of AC2. No other pattern adds work here; no table, no Schedule and no business value is created.

**Build steps**

1. Write the egress entry and the drop rule, and test a call to INT-23 and a call to an unlisted destination (AC1, X1).
2. Create the login and the workload identity with grants on `rwb_agent` only, and verify that another schema is refused (AC2, X3).
3. Create the Key Vault entries and wire them to the workload identity; test a valid, an expired and an unissued client certificate (AC2, X2).
4. Provision the topic, the retry topic, the `.dlt` topic and the producer ACL; test a refused foreign producer and a `.dlt` route (AC3, X4, X5).
5. Register the two registry subjects with BACKWARD compatibility and test a payload that fails its subject (AC3, X4).
6. Provision the queue and the worker identity in namespace `rwb-recovery`, and test a worker pointed at a foreign queue (AC4, X6).
7. Wire the two budget metrics and their alarms, with the policy value of 60 seconds read at run time and not from a chart value (AC5, X7).
8. Size the pods, run the burst load test, record the reviewed values and set the four alarms with their runbook entries (AC6, X8).
9. Add the five pipeline gates and run them once on a change that names another schema and another service's topic (AC7, X9).
10. Hand the endpoint reference, the topic names and the queue to the app and contract stories of this key, and the metrics and alarms to the operations stories.

**Done when.** The path is one hop and authenticated in all three environments, no secret sits outside Key Vault, the topic and its two related topics exist with the producer right of rwb-agent only, the queue and the worker identity are the service's own, both budgets fire their alarms in a test, the burst load test passes inside the reviewed values, and the five gates block a boundary violation.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| None | A path, identity, secret, topic, queue, budget, sizing or gate check fails | No business message is produced. The provisioning check or the pipeline fails with the resource name and the violated rule, and the platform administrator or the build owner acts on it. |

This story adds no message ID. The business messages of the capability keep their identifiers and texts from the legacy story: MSG-P10-007 (no suggestion), MSG-P7-003 (the decision could not be recorded), MSG-P4-002 (a role without the right) and MSG-GEN-001 (an empty required field). The infrastructure reports a condition to the operator, never to a workbench user.

### 15. Screens and states

None. There is no screen in this story. The operator-facing surfaces are the environment provisioning check, the egress and ACL views, the Key Vault rotation record, the load-test report and the alarm page with its runbook entries; the agent screen SCR-14 and the agent monitor belong to RWB-P10-E2032-APP and to the monitor story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E2032-INF-01 | AC1 | NFR | DEV, SIT and UAT egress lists; a handshake to INT-23 with a valid, an expired and an unissued client certificate; a call to an unlisted destination |
| TC-P10-E2032-INF-02 | AC2 | NFR | The login grants on `rwb_agent` only; a read of another schema refused; the Key Vault read by the workload identity; the secret scan of the chart, the values and the logs |
| TC-P10-E2032-INF-03 | AC3 | Component | The topic, its retry and `.dlt` topics, a foreign producer refused, a payload failing its subject routed to `.dlt`, and the two registry subjects |
| TC-P10-E2032-INF-04 | AC4 | Component | The queue in namespace `rwb-recovery`, a worker on its own queue, and a worker pointed at a foreign queue that fails readiness |
| TC-P10-E2032-INF-05 | AC5 | NFR | A model call of 61 seconds and a client call over 2 seconds; the two alarms and the run recorded as TIMED_OUT with fallback true |
| TC-P10-E2032-INF-06 | AC6 | NFR | A burst load test on the queue; no pod killed for memory or CPU; the four alarms with their runbook entries |
| TC-P10-E2032-INF-07 | AC7 | Integration | A change that reads another schema and names another service's topic; the five gates and the block of the merge |

### 17. Guardrails

- No business value in a policy, a values file or a config map: the model code and version, the schema limits, the timeout, the mode and the review date stay rows of `agent_policy`, and the 60 seconds is read at run time (BR6, BR9).
- No personal data in a topic message, a log, an alarm payload or a test fixture: identifiers and facts only, and the inputs snapshot stays inside the record.
- One login, one workload identity and one producer right; no other service's identity holds a grant on the agent topic or on the service's secrets (BR2, BR4).
- No secret, key or certificate body in a file, a chart value, a config map, a log or a dashboard; everything comes from Key Vault through the workload identity (BR3).
- The only outside destination is INT-23; the egress list is a reviewed entry and a call outside it is dropped and alerted (BR1).
- No `rwb_*` table, no migration, no bucket and no Schedule is created here; the storage of the agent artefacts is the `rwb_agent` tables (BR8).
- The registry subjects are BACKWARD compatible, and a breaking change is a new version of the payload with the consumers' agreement (BR7).
- Every fixture and every load-test payload is synthetic; no production account, payment, model answer or record is used.

### 18. Traceability

| Requirement ID | Requirement (short) | Infrastructure element | Test cases |
|---|---|---|---|
| REQ-CHO-006 | A treatment record holds every offer's type, terms, approval and outcome | The path and the topic that make the suggestion and the run completion reach their owners | TC-P10-E2032-INF-01, TC-P10-E2032-INF-03 |
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | The record subject and the topic that carry the decision record and the run facts | TC-P10-E2032-INF-03 |
| NFR-010 | An agent answers within 60 seconds, after which the rule result is used | The 60-second model budget with its metric and alarm, and the policy value read at run time | TC-P10-E2032-INF-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The one-hop egress list and the measured 2-second client budget | TC-P10-E2032-INF-01, TC-P10-E2032-INF-05 |
| D-RCV-60 DP-09, DP-14 | Kafka with outbox, inbox and CloudEvents; one topic per service | The topic, its retry and `.dlt` topics, the producer ACL and the registry subjects | TC-P10-E2032-INF-03 |
| D-RCV-60 DP-01, DP-02 | One schema and one login per service | The login on `rwb_agent` and the boundary scan gate | TC-P10-E2032-INF-02, TC-P10-E2032-INF-07 |

### 19. Out of scope

- The operation, the mode gate, the guardrail, the record write, the outbox and the screen (RWB-P10-E2032-APP).
- The contract shapes of the operation, the record, the event payload and the fakes (RWB-P10-E2032-CON).
- The whole agent runtime, its other agents, the evaluation harness and the monitor, and their infrastructure (RWB-P10-E1058-APP, RWB-P10-E1058-CON, RWB-P10-E1060-APP, RWB-P10-E1063-APP).
- The Kafka platform, the schema registry, the Temporal cluster, Key Vault, the certificate authority and the service mesh as platform products (RWB-PLT-EVT, RWB-PLT-N008-INF, RWB-PLT-LIB).
- The `rwb_agent` schema design, its tables and its migrations (the database stories of the service epic and RWB-P10-E1058-APP).
- The Helm values, the readiness signal, the dashboards, the alerts of the application and the runbook, which are held by the operations stories of the service epic; this story provisions the platform alarms of AC5 and AC6 only.
- The TDR model itself and the Enterprise AI endpoint beyond the private path (the TDR team and Enterprise AI).
- The endpoint host and port, the certificate subject, the Key Vault entry names, the partition count, the retention, the sizing figures and the alarm thresholds, which are Not specified in the source documents (GAP-0635; ASM-0988, ASM-0989, ASM-0990, ASM-0991).
