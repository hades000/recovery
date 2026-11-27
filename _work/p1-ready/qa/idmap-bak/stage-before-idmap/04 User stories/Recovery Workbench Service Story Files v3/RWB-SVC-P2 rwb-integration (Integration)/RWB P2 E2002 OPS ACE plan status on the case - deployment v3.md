# RWB-P2-E2002-OPS ACE plan status on the case - deployment

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004.

| Item | Value |
|---|---|
| Story key | RWB-P2-E2002-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-16) |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P2-F |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (path prefix /api/recovery/integration/v1); the contract version tag is not specified in the source documents (DOR-RWB-P2-E2002-OPS-23) |
| Integration dependencies | None |
| External dependencies | None |
| Open decisions | DL11 (ASM-0553, ASM-0703, ASM-1051, ASM-1104); DL14 (ASM-0189, ASM-5687); each assumption confirmed by the programme directive |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-019) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-002 for rwb-integration. This document deploys the plan-status operation of this key: the chart and its values, the Flyway statement, the ACE endpoint and the two settings, the trigger wiring, the flag, five dashboard series, the alert set of the key and the runbook. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E2002-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 25 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **Platform administrator** (RW-PLATADM), I want **the plan-status operation of rwb-integration deployed on the service's own worker and task queue, with the ACE common module endpoint, the batch size and the timeout as environment values, behind the platform flag, with five dashboard series, the alert set of the key and a runbook**, so that **a caller always gets either a live status inside a bounded budget or a bounded refusal it can fall back from, and a rota can see and act on the three conditions that stop it**.

The legacy story assumed a nightly step and a screen that read ACE inside the monolith, and nobody had to know where the plan came from. In the target the plan read is one operation of this service, called by rwb-case's plan-status step and by the gateway-bff composite route (DP-11, DP-19), and the daily step is rwb-case's. So the deployment is where the boundary becomes real: the ACE endpoint per environment, the batch of 500, the 2,000 ms budget, the breaker, the flag and the honest observation of a read that is not allowed to fail silently.

This story deploys and proves the deployment only. It builds no controller, no validator and no client: those are RWB-P2-E2002-APP, against the baseline of RWB-P2-E2002-CON. It writes no case row and stores no plan: the stored status is rwb-case's. What it owns is the release: the chart and its values, the schema statement, the ACE connectivity, the two settings, the flag, the five series, the alert set and the runbook.

### 2. Business rationale

A plan status is read on three paths at once: the case record screen through the composite route, the nightly step of rwb-case, and the integration harness. Each of them fails in a different way if the deployment is wrong. A wrong ACE endpoint fails every read and every nightly step keeps every stored value, which looks like a quiet day. A timeout that is longer than the caller's budget makes the caller time out while this service is still waiting, so the answer is a 504 from the edge instead of a 503 with a message. A batch size that is larger than ACE accepts turns one read into one error for the whole case. And a flag left off in an environment serves stored values that nobody labels as stored.

The deployment therefore carries the state of the read as data. Five series answer what a rota asks: how many answers were live, how many had no plan, how many carried a code outside the list, how many were refused or unavailable and with which class, and how long a call took against the budget. Four alerts are wired, each with one runbook entry: three carry a message ID (MSG-GEN-006, MSG-P4-002, MSG-P4-003) and one carries the unknown status code and its count, because the legacy story gives no message for an unknown code. The fifth condition of the key — no RESTRUCTURE version in force — is named in the mapping with its owners, because this service never evaluates a package and cannot see it (ADR-023).

The release also fixes the two settings where they belong. The batch size and the timeout are read at run time through the rwb-case parameters contract (DP-06), so a change needs no rebuild and no release; the endpoint, the breaker and the thresholds are values files of the environment. Nothing is hard-coded, and nothing in this key adds a table: the schema statement exists to prove that the read writes nothing (DP-01, DP-15).

### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB).
- The integration base of RWB-P2-E1007-APP and RWB-P2-E2001-APP is deployed in the environment: the worker on the task queue of the service, the namespace `rwb-recovery`, the payload codec, the health surface and the base `/api/recovery/integration/v1` behind gateway-bff.
- The Temporal workflow kit, the namespace `rwb-recovery` and the build ID provider exist (RWB-PLT-WF, RWB-PLT-E1071-CON). This key creates no Schedule of its own.
- The platform flag library is available and the flag `rwb.integration.ace-plan-status` is registered for this service (RWB-PLT-E1047-CON; R-PREC default ruling on feature flags).
- The `rwb_integration` schema and its Flyway sequence exist, with the outbox, inbox, delivery and idempotency objects created by the service baseline and the DB story of the service (RWB-PLT-E1044-CON).
- The plan-status operation of RWB-P2-E2002-CON is published, with its answer, its refusals and its read-only rule, and its fakes answer every consumed read.
- The ACE common module publishes `RestructurePlanQuery` in SIT and UAT (INT-34; DL14), and the environment either reaches that endpoint or, where ACE SIT is not yet published, the stub of the contract baseline.
- The parameter rows `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 are in force in the rwb-case parameters (assumed; DL11), and LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED and BROKEN is loaded (RW-COE).
- The platform error envelope and the message catalogue are in force, so an alert can carry a message ID.
- The environments DEV, SIT and UAT exist; the wave 2 release deploys to DEV, SIT and UAT, and the production values are a later promotion of the same artefacts.
- The topics of this service already exist: `rwb.integration.events.v1` with its retry and `.dlt` topics, and the shared `rwb.decision-record.v1` (RWB-PLT-EVT, RWB-PLT-TE006-CON). This release adds no topic and registers no consumer group.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The pipeline builds the service image and the contract jar, runs the unit, component and contract tests of RWB-P2-E2002-CON and RWB-P2-E2002-APP, scans the image and the dependencies, and publishes one chart version.
2. The chart deploys the service worker with its own login, the namespace `rwb-recovery`, the task queue of the service, the payload codec and the build ID of the release.
3. The API step confirms that `GET /api/recovery/integration/v1/cases/{caseId}/plan-status` answers through gateway-bff in the environment, with the authorise contract of rwb-access reachable and the case, reference-data and parameter contracts of rwb-case replaced by the real services where they are deployed.
4. The ACE connectivity step confirms the endpoint of the environment, the certificate and the network path, and records whether the environment answers from ACE or from the contract stub.
5. The setting step confirms that `rwb.ace.plan.batch-size` and `rwb.ace.plan.timeout-ms` are read from the rwb-case parameters with the version in force, that the values in force are 500 and 2000, and that a change of the version is picked up without a redeploy.
6. The schema step confirms that the release applies no migration of its own, that the library objects exist in `rwb_integration` and that the service login holds no grant on `recovery`.
7. The trigger step confirms the calling paths: rwb-case's plan-status activity reaches the operation on the task queue of rwb-case, and gateway-bff reaches it for the case record; no P2 Schedule exists, and none is created by the release.
8. The flag step sets `rwb.integration.ace-plan-status` from the values of the environment and confirms that the answer, and the ACE call, follow it.
9. The dashboards are published with the five series and the environment, the release and the build ID as dimensions.
10. The alert set is wired: four rules — three carrying MSG-GEN-006, MSG-P4-002 and MSG-P4-003 and one carrying the unknown status code and its count — each with its runbook entry, and the fifth row of the mapping is published with its owners and its route.
11. A smoke step reads one synthetic case in DEV and checks that the answer carries a plan reference, a status from the list, its date and `live` true, that a second call answers the same values and writes nothing, and that the stored fallback on the screen comes from rwb-case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The chart render, the image pull or a migration job fails | The deployment stays unready and the pipeline stops; no traffic to the new version | None | AC1 |
| X2 | The release would apply a migration that adds a table, a column or an index | The schema step fails the release: this key adds none, and a migration that does is refused | None | AC2 |
| X3 | The service login holds a grant on `recovery`, or on another `rwb_*` schema | The schema step fails the release and names the grant | None | AC2 |
| X4 | The ACE endpoint is wrong or unreachable in an environment | Every read answers 503 with MSG-GEN-006, the unavailable series rises and the alert pages; no value is invented | MSG-GEN-006 | AC3, AC5 |
| X5 | The timeout in force is longer than the caller's budget | The budget check fails the release, because a caller must receive a 503 and not an edge timeout | MSG-GEN-006 | AC3 |
| X6 | The batch size in force is larger than ACE accepts | The read fails for the whole case; the setting is a parameter row, so it is corrected without a release, and the failure series names the batch class | MSG-GEN-006 | AC3, AC5 |
| X7 | The flag is off in an environment and the operation still calls ACE | The flag step fails the release, because off means no outside call | None | AC4 |
| X8 | A P2 Schedule for the plan status is created by the release, or by an operator | The trigger step fails the release; the daily step is rwb-case's and a second run over the same cases is not allowed | None | AC4 |
| X9 | The worker stops while a request is in flight | The caller receives its own timeout and retries; the read writes nothing, so no repair is needed | MSG-GEN-006 | AC6 |
| X10 | A read answers a code outside LOV-PLAN-STATUS | The unknown-status series rises and the alert fires; the code is answered unchanged and never stored here | None | AC5, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the workflow kit, the flag library and the published contract; no application code is built here |
| Negotiable | Replica counts, resource sizes, thresholds, the endpoint, the breaker values and the retention are environment values |
| Valuable | Makes the read observable and bounded before the release, so a failing ACE read cannot look like a quiet day |
| Estimable | One chart, one API step, one connectivity step, one setting step, one schema step, one trigger step, one flag step, five series, five mapping rows and four runbook entries |
| Small | Fits one sprint with the runbook |
| Testable | Every criterion tests an artefact: the chart renders, the schema is unchanged, the settings are read as data, the paths are wired, the alerts fire on a synthetic metric, the runbook entry is followed |

### 7. Acceptance criteria

```gherkin
Feature: Deployment of the ACE plan status operation for rwb-integration

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the namespace is rwb-recovery and the task queue of rwb-integration is rwb-integration
    Given the target environment is SIT

  Scenario: AC1 The service and the plan-status operation are deployed with the rwb-integration login (new, D-RCV-60)
    Given the rwb-integration chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the deployment declares the rwb-integration login and no other service's credential
    Then GET /api/recovery/integration/v1/cases/{caseId}/plan-status answers through gateway-bff in each environment
    Then the readiness probe reports healthy only after the first successful poll and the first successful authorise call, and the liveness probe writes nothing

  Scenario: AC2 The schema is unchanged and the login holds no grant on recovery (new, D-RCV-60)
    Given the rwb_integration schema, its Flyway sequence and the library objects of the service baseline
    When the schema step runs
    Then the release applies no migration of its own and adds no table, no column and no index
    Then the outbox, inbox, delivery and idempotency objects exist in rwb_integration
    Then the service login holds no grant on recovery and no grant on another rwb_ schema
    Then a release that would add a table or a column fails the schema step and names the migration

  Scenario: AC3 The ACE endpoint, the batch size and the timeout are configuration (new, D-RCV-60)
    Given the values file of an environment and the parameters rwb.ace.plan.batch-size and rwb.ace.plan.timeout-ms
    When the setting step runs
    Then the ACE endpoint, its certificate reference and the breaker values come from the values file of the environment
    Then the batch size and the timeout are read at run time through the rwb-case parameters contract with the version in force
    Then the values in force are 500 and 2000, and a new parameter version is picked up without a redeploy
    Then the timeout in force is not longer than the budget the caller declares, and a longer value fails the release
    Then no batch size, timeout, endpoint or threshold appears in the image as a constant

  Scenario: AC4 The trigger paths are wired and no P2 Schedule exists (new, D-RCV-60)
    Given the plan-status step of rwb-case and the composite route of the case record
    When the trigger step runs
    Then rwb-case's activity reaches the operation with the case reference only, one hop, on a 2 s client budget
    Then gateway-bff reaches the operation for the case record and merges it with the stored answer of rwb-case
    Then no Schedule of rwb-integration is created, and the daily step and its activity stay on rwb-case
    Then the flag rwb.integration.ace-plan-status is read from the platform flag library, and off means no ACE call and a live false answer
    Then the release records whether the environment answers from the ACE common module endpoint or from the contract stub

  Scenario: AC5 The five series and the five mapping rows carry the read (new, D-RCV-60)
    Given the published dashboard, the alert rules and the runbook of the deployment
    When a live answer, a no-plan answer, an unknown code, an unavailable ACE and a refused caller are simulated
    Then the dashboard shows the live answers, the no-plan answers, the unknown codes, the unavailable and refused answers by class, and the call duration against the budget
    Then each series carries the environment, the release and the build ID as dimensions
    Then four alerts fire: three with MSG-GEN-006, MSG-P4-002 and MSG-P4-003, and the unknown-status alert with the code and the count, each linking one runbook entry
    Then the fifth row of the mapping names the no-package-in-force refusal with its owners rwb-case and rwb-decision and states that this release raises no alert for it, because the read never evaluates a package
    Then no series, alert payload or runbook entry carries an account number, a decoded payload or a personal value

  Scenario: AC6 The runbook covers the read and the rollback keeps the answer whole (new, D-RCV-60)
    Given the published runbook and the alert rules
    When an operator follows the entry for an unavailable ACE, for an unknown code and for a refused caller
    Then each entry names the symptom, the check, the owner role and the recovery step, and names rwb-case and the ACE team where the case side or ACE is the owner
    Then a rollback redeploys the previous chart version with its own build ID and pauses the flag during the rollback
    Then no repair script exists, because the read writes nothing and a repeat answers the same values

  Scenario: AC7 Each business rule BR1 to BR13 of section 8 holds for the release, or is held by the guardrail or boundary test that names it (new, D-RCV-60)
    Given the rendered chart, the values files, the release record, the dashboard, the alert rules and the runbook
    When the release is checked against the rules of section 8
    Then BR1: the worker polls only the task queue of rwb-integration in the namespace rwb-recovery and carries the rwb-integration login only
    Then BR2: every worker carries the build ID of its release with worker versioning enabled, and a new build takes new requests while the old build drains
    Then BR3: the release creates no Schedule and no workflow
    Then BR4: the release writes rwb_integration only, adds no table and no column, and holds no grant on recovery
    Then BR5: the ACE endpoint, the certificate, the breaker and the thresholds come from values files, the batch size and the timeout are parameter rows read through their owner, and none is a constant
    Then BR6: with the platform flag off there is no ACE call and the answer is live false, and no service table holds the switch
    Then BR7: every alert carries a message ID and the agreed text and links one runbook entry
    Then BR8: replicas, resources, thresholds, the endpoint, the breaker and the flag come from values files and the flag library
    Then BR9: series, alert payloads and the runbook carry no account number, no name and no decoded payload
    Then BR10: a failing release does not replace a working one, and a rollback keeps one build serving with the flag paused while the two builds change over
    Then BR11: the read has the same budget in every environment, and a timeout longer than the caller's budget fails the release
    Then BR12: a condition this service cannot observe is named with its owner and has no alert
    Then BR13: until the P1 break operation is published, a plan-status break is listed from the run summary of DailyCaseRun and rwb-case writes no break row
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one task queue, one login: the worker polls the task queue of `rwb-integration` in the namespace `rwb-recovery` and carries the rwb-integration login only | Arch v5 slides 24 and 41; DP-02; DP-10 |
| BR2 | Every worker carries the build ID of its release and worker versioning is enabled, so a new build takes new requests while the old build drains | Temporal and Drools design slide 27; RWB-PLT-E1071-CON |
| BR3 | This release creates no Schedule and no workflow: the daily plan-status step and its activity are rwb-case's, and a second daily run over the same cases is not allowed | Arch v5 slide 44; DP-10; RWB-P3-E2002-APP |
| BR4 | The release writes `rwb_integration` only, adds no table and no column, and holds no grant on `recovery` | DP-01; DP-15; ADR-010 |
| BR5 | The ACE endpoint, the certificate, the breaker and the thresholds are values files; the batch size and the timeout are parameter rows read through their owner; none is a constant | DP-06; FSD P2 Integration v3 BR-P2-007 |
| BR6 | The flag is the platform flag library's; off means no ACE call and a live false answer, and the switch is never a service table | R-PREC default ruling; Ownership Map `feature_flag` |
| BR7 | Every alert carries a message ID and the agreed text and links one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | No environment value is hard-coded: replicas, resources, thresholds, the endpoint, the breaker and the flag come from values files and the flag library | Template and Rules §R7.2 s17 |
| BR9 | Dashboard series, alert payloads and the runbook carry counts, case references, plan references, status codes, message IDs and build IDs only, never an account number, a name or a decoded payload | Arch v5 slide 42 (PDPA) |
| BR10 | A failing release never replaces a working one; a rollback keeps one build serving and the flag paused while the two builds change over | Temporal and Drools design slide 27; DP-10 |
| BR11 | The read is bounded by the same budget in every environment: a timeout longer than the caller's budget is a defect of the release, not a tuning value | Legacy 2 s budget; DP-11 |
| BR12 | A condition this service cannot observe is named with its owner rather than given a false alert | AC5; the split of RWB-P2-E2002-APP |
| BR13 | Until the P1 break operation is published, a plan-status break is listed from the run summary of DailyCaseRun and rwb-case writes no break row | GAP-0772 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the contract tests pass | Deploying |
| Deploying | Worker registered and probes healthy | The worker polls its queue only and the authorise call succeeds | Ready |
| Ready | API step passed | The operation answers through gateway-bff and the contracts are reachable | Serving |
| Serving | Flag off | `rwb.integration.ace-plan-status` is off in the environment | Stored only |
| Stored only | Flag on | The flag is on and ACE is reachable | Serving |
| Serving | ACE unavailable | The endpoint, the certificate or the network fails | Serving (degraded) |
| Serving (degraded) | ACE reachable | The next call answers inside the budget | Serving |
| Serving | Release superseded | A new chart version passes the tests | Rolling |
| Rolling | All workers on the new build | The old build drains its open requests | Serving |
| Any | A failing release or a failed step | The previous release stays in force and the pipeline stops | Previous state |

These are states of the release, not of a case: no case status and no route state moves in this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the connectivity, the setting, schema and trigger steps, the dashboards and the runbook |
| Platform administrator | Owns the namespace, the worker versioning policy, the flag library registration and the operator view |
| Platform event owner | Owns the topics and the schema registry; this release adds none |
| Release manager | Approves the promotion of one artefact and may block it on a failed check |
| On-call operator | Runs the runbook entries and opens an incident when the read is unavailable or an unknown code persists |
| RW-COE, centre of excellence analyst | Receives the parameter and reference-data questions, because the two settings and LOV-PLAN-STATUS are its rows |
| The ACE team | Owns the endpoint, the certificate and the interface the release points at |
| RW-CASEOWN and RW-RESTRUCT | Consume the answer; they are the users the alerts protect, not operators of this release |
| RW-REFADM | Holds no Case record right; the refusal the release wires as MSG-P4-002 |

The worker runs as the rwb-integration service identity (DP-02), carried by the chart as a secret reference and never as a literal name. The identity name is Not specified in the source documents (GAP-0656; ASM-1110).

The assumptions of this story under GAP-0656 (ASM-1110, ASM-1111, ASM-1112) are confirmed by the programme directive: the identity and environment values with no Schedule and no migration; the trigger wiring with the ACE-or-stub record and the corrected harness row; and the five series, four alerts, the named no-package row and the four runbook entries. Every threshold and endpoint is an environment value and never code.

### 11. Data

| Item | Content | BR Field ID |
|---|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, namespace, task queue, build ID, flag value, ACE endpoint and certificate reference, breaker values, alert thresholds | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-7) |
| ACE call settings | `rwb.ace.plan.batch-size` and `rwb.ace.plan.timeout-ms`, read at run time through the rwb-case parameters with the version in force; 500 and 2000 are the values in force | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-7) |
| Calling paths | rwb-case's plan-status activity, one hop, on its own queue, calling this service's per-case plan-status read once per case inside the readPlanStatus activity in batches of `rwb.ace.plan.batch-size`; gateway-bff for the case record; no Schedule and no workflow of this service | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-7) |
| Schema | `rwb_integration` with the library objects of the baseline; no table, no column and no index added; no grant on `recovery` | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-7) |
| Dashboard series | Live answers; no-plan answers; unknown status codes; unavailable and refused answers by class; call duration against the budget | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-7) |
| Alerts | Four rules, each with one runbook entry, and one mapping row naming a condition this service cannot observe | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-7) |
| Runbook entries | ACE unavailable; unknown status code; refused caller; stored fallback and no-package-in-force routing | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-7) |
| Secrets | The service login secret, the ACE client certificate, the contract client credentials and the Temporal mTLS material, all from the platform secret store | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-7) |
| Test data | The synthetic case "RW-2026-000310" with account "A-0310" and plan "TDR-SYN-0310" in DEV and SIT only; the fixture owner is Not specified in the source documents (GAP-0656; ASM-1112) | Not specified in the source documents (DOR-RWB-P2-E2002-OPS-7) |

The deployment topology (cluster names, node pools, replica counts, resource sizes, zone spread and ingress class) belongs to each environment and is set by the platform team in its values file; the chart exposes every one of them as a value, and this story fixes only their names and the rule that they are never hard-coded.

**Probes.** Readiness answers healthy only after the worker has polled its queue once, the codec is attached and one authorise call has succeeded; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe calls the ACE common module, so a slow ACE never takes the pod out of service and never hides the degradation from the alert. The paths and timings are values of the environment.

### 12. Contract

#### 12.1 REST operations provided

None of its own. The plan-status operation is provided by RWB-P2-E2002-APP and documented in RWB-P2-E2002-CON; this story deploys it and declares no path. The probes are cluster-internal and are not part of the API surface.

#### 12.2 REST operations consumed

None of its own. The deployment needs no REST client: the operation's own clients call the case, reference-data, parameter and authorise contracts inside the request, and the pipeline calls the platform registry and the secret store only.

#### 12.3 Events published

None of its own. The release publishes no event type: `rwb.integration.events.v1` carries FileDelivered and FileFailed, which belong to the outbound-file stories of this service, and this key publishes nothing because a read takes no decision.

#### 12.4 Events consumed

None. The release registers no consumer group and subscribes to no topic. The service topic and the shared `rwb.decision-record.v1` exist before the release and are used by other stories of the service.

#### 12.5 Workflows and activities

None of this key. The worker this release deploys registers the workflows and activities of the integration base (RWB-P2-E1007-APP) and none for the plan status: `PlanStatusStep` and its `readPlanStatus` activity are registered on rwb-case's own worker, and this operation answers inside the request. The integration harness lists a plan-status step on `rwb-integration`; that row conflicts with the sibling story and with the job map and is carried in the gap row (GAP-0656; ASM-1111).

**Build ID and versioning.** The build ID is the one the workflow kit supplies for the release commit; worker versioning is enabled and a new build takes new requests while the old build drains.

#### 12.6 Schedules

None. The release creates no Schedule of this service. The legacy plan-status step of JOB-02 runs inside the event-started DailyCaseRun of rwb-case, and the release confirms that no P2 Schedule exists for it (DP-10; BR3). The state of the daily run is rwb-case's to observe; this release observes only the read that the run calls.

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| interface_config, outbound_item, job_catalog | rwb_integration | P2 (Ownership Map; Arch v5 slide 41; TSD P2 v3 T3.1) | Not written and not read by this release; no row is added, because the ACE endpoint is a deployment value |
| outbox_event, processed_event, outbox_delivery, idempotency_key | rwb_integration | PLT library, created in `rwb_integration` (DP-09) | Present from the service baseline; the release confirms they exist and writes none |

The release applies no migration of its own: the `rwb_integration` baseline and the library objects are created by the DB story of the service (DP-15), and a migration that adds a table, a column or an index fails the schema step (BR4). No grant on `recovery` and no grant on another service's schema is requested by the chart.

#### 12.8 Contract fakes

None deployed. The contract mocks of the case, access and decision contracts are in-process test doubles of the contract and app stories, and the ACE common module stub is a test double of the pipeline. Where the ACE common module SIT endpoint is not yet published, the deployment records that the environment answers from the stub of the contract baseline, and the setting step keeps the two cases apart so that no environment believes it is reading ACE when it is not.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | The operation is deployed, not declared here; probes are cluster-internal |
| Kafka | 0 published, 0 consumed | No topic and no consumer group is created by this release |
| Temporal | None of this key | The worker is the base's; no workflow, no activity and no Schedule is created for the plan status |
| File | None | The values files and the recorded histories are pipeline inputs, not runtime data; one outside interface call is configured, not declared |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | The release writes `rwb_integration` only and holds no grant on `recovery` | none |
| DP-03 | DecisionLogWriter, decision log | The decision-record library ships in the image and publishes nothing for a read | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | The embedded kit ships in the image; this release evaluates no package and carries no rule data | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The release configures the ACE common module endpoint and no view access | none |
| DP-06 | Parameters, casewf.config | The two settings are parameter rows read at run time; the environment values are values files | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | The status list is read through the rwb-case reference-data contract at run time | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | The library objects are confirmed present; the release publishes nothing | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | The namespace, the task queue and the build ID come from the workflow kit; no Schedule is created | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | The operation's clients keep the 2 s budget; the deployment adds no path | none |
| DP-13 | `/api/recovery/v1` | The deployed base is `/api/recovery/integration/v1` | none |
| DP-15 | V0001 baseline, migration | The per-service Flyway sequence is applied by the baseline; this release adds no migration | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff serves the runtime path; the deployment registers no route of its own | H RWB-PLT-N001-CON |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-integration/` overlay | Deployment, config map, secret references, probes, task queue and namespace, flag reference, build ID, ACE endpoint reference, breaker values |
| `helm/rwb-integration/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, flag value, ACE endpoint and certificate reference, breaker values, alert thresholds, build ID, environment |
| Pipeline stage | Build, unit, component and contract tests, image and dependency scan, chart publish, promotion |
| API step | The operation answers through gateway-bff and the authorise call succeeds |
| ACE connectivity step | The endpoint, the certificate and the network path of the environment, and whether ACE or the stub answers |
| Setting step | The two parameters read with the version in force, their values, and the budget check |
| Schema step | No migration, the library objects present, and the grant check on `recovery` |
| Trigger step | The two calling paths wired, no P2 Schedule, the flag behaviour |
| Flag step | `rwb.integration.ace-plan-status` set from the environment and the answer checked against it |
| Dashboards | The five series of section 11 |
| Alerts | Four rules and five mapping rows: three rules carry a message ID, one carries the unknown status code, and the fifth row names a condition with its owners and no wiring |
| Runbook | Four entries: ACE unavailable; unknown status code; refused caller; stored fallback and no-package-in-force routing |

**Alert mapping**

| Message ID | Condition | Alert | Route |
|---|---|---|---|
| MSG-GEN-006 | The unavailable answer rate, or the p95 duration against the budget, crosses its threshold for an environment | ACE-read alert naming the source, the budget, the p95 and the build ID | Platform on-call, page |
| MSG-P4-002 | The 403 rate crosses its threshold | Right-refusal alert naming the role code and the operation, never the caller | Platform on-call and the access owner, ticket |
| MSG-P4-003 | The 404 rate for a case reference crosses its threshold | Scope-refusal alert naming the count and the release; a persistent rise is a routing or scope defect, not a read defect | Platform on-call, ticket |
| None (unknown code) | The unknown-status count is above zero for an environment | Unknown-status alert naming the code and the count, so the list owner can act | Business on-call (RW-COE) and the ACE team, page |
| MSG-P3-027 | No RESTRUCTURE version is in force on a business date | No alert is raised by this release: the condition is visible to rwb-case and rwb-decision, which own the evaluation, and the route is RW-COE | Business on-call (RW-COE) through the case side, no wiring in this release |

The unknown-status row carries no message ID because the legacy story gives no message for an unknown code (legacy X3, message "None"); the alert text is therefore a template of the platform catalogue with the code and the count, and it invents no business value. The fifth row is published so that an operator looking for the no-package-in-force condition finds where it lives and who owns it, rather than a false alert on a service that never evaluates a package (BR12).

**Rollback.** A release that fails a check is not promoted. A release already promoted is rolled back by redeploying the previous chart version with its own build ID, which keeps the old build serving its open requests until they finish. The flag is set off during the rollback where the new release changed the ACE endpoint, so that no request is sent to an endpoint the old build does not know, and it is set back on once one build serves the queue. No repair script exists: the read writes nothing, a repeat answers the same values, and the stored fallback on the screen is rwb-case's and was never removed.

**Feature switch.** `rwb.integration.ace-plan-status`, kept as the legacy reference of the switch and read from the platform flag library. On: the operation calls ACE and answers live. Off: no ACE call is made and the answer is 200 with `live` false, so every caller uses the stored value and the screen shows the stored status. The flag is never a value of a service table, and its value is read at the start of every request so that a change needs no redeploy.

**Done when.** The chart renders for DEV, SIT and UAT, the operation answers through gateway-bff, the ACE endpoint and the certificate are confirmed per environment, the two settings are read as parameter rows with the values 500 and 2000, the schema step proves that no migration and no grant is added, no P2 Schedule exists, the flag governs the ACE call, the five series and the alert set are published, and the four runbook entries are reviewed by the on-call rota.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-006 | The ACE common module or a consumed read did not answer inside the budget | {system} is not available. Try again in a few minutes. |
| MSG-P4-001 | No session, or the person holds no Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A case outside the caller's scope, or unknown | This case is not in your scope. |
| MSG-P2-008 | The stored plan status is shown because the live answer is not available | The ACE plan status is from {date}. Today's status was not returned. |
| MSG-P7-003 | The decision record of a route move could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No RESTRUCTURE version is in force on a business date | The {table} load was refused: {check}. The version in force is unchanged. |

The business texts are copied unchanged from the legacy story and the platform catalogue; the deployment adds the alert routing and the runbook link, never a new wording. MSG-GEN-006, MSG-P4-001, MSG-P4-002 and MSG-P4-003 are the operation's own and are the ones this release wires or runs; MSG-P2-008, MSG-P7-003 and MSG-P3-027 belong to the case side and are listed because the key's criteria carry them. An alert carries the message ID, the counts, the case reference, the code and the build ID, never an account number and never a decoded payload.

### 15. Screens and states

The deployment has no screen of its own. Its operator-facing surfaces are the pipeline run view, the release view, the dashboard of the five series, the Schedule view of the workflow kit for the rwb-case Schedule it does not own, the job catalogue read of the service baseline and the runbook. The operator view is behind Entra ID: RW-PLATADM operates and RW-AUDIT reads. SCR-44 Interface and job monitor is not used as a new screen, because this key adds no interface row and no job row. Screen Specifications v1 gives SCR-44 the states Running, failed and complete. For the four states of the v3 rule: empty is Not specified in the source documents (DOR-RWB-P2-E2002-OPS-10); loading is Not specified in the source documents (DOR-RWB-P2-E2002-OPS-10); error wording is Not specified in the source documents (DOR-RWB-P2-E2002-OPS-10); no access: access is Platform administration, checked on every request, and an action outside the role's permission shows MSG-P4-002 "You cannot {action} here. Your role does not include it."

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2002-OPS-01 | AC1 | NFR | The chart renders for DEV, SIT and UAT with a pinned digest, the rwb-integration login reference and the operation reachable |
| TC-P2-E2002-OPS-02 | AC2 | Component | No migration, no table, no column and no index added; the library objects present; no grant on `recovery`; a release that adds a table refused |
| TC-P2-E2002-OPS-03 | AC3 | Component | The endpoint, the certificate and the breaker from the values file; the two settings read as parameter rows with 500 and 2000; a longer timeout refused |
| TC-P2-E2002-OPS-04 | AC4 | NFR | The two calling paths, no P2 Schedule, the flag on and off, and the ACE-or-stub record of the environment |
| TC-P2-E2002-OPS-05 | AC5 | NFR | The five series and the five mapping rows, with four alerts firing and the fifth row naming its owners and no wiring |
| TC-P2-E2002-OPS-06 | AC6 | NFR | The four runbook entries followed, and a rollback that keeps one build serving with the flag paused |
| TC-P2-E2002-OPS-07 | AC2 | Component | Boundary of the section 12.7 tables: interface_config, outbound_item and job_catalog untouched; the four library tables present and unwritten; a migration adding a table refused (ASM-3438) |
| TC-P2-E2002-OPS-08 | AC7 | Component | BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 and BR13 checked one by one on the rendered chart, the values files, the release record, the dashboard, the alert rules and the runbook, including a new build beside a draining build, the flag off, a longer timeout and a failing release |

The levels follow the platform taxonomy: a schema or configuration check is Component, a release or operational check is NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. This story writes no `-ITG` copy: the cross-service proof of the key is RWB-ITG-E2002-ITG's.

### 17. Guardrails

- No business value in a values file: the status codes, the package code, the rule IDs and the message text are rows of the reference data, the registry and the catalogue, never a deployment value.
- No personal data and no account number in logs, dashboard series, alert payloads, the runbook or the recorded runs: counts, case references, plan references, status codes, message IDs, role codes and build IDs only.
- One login per service and one task queue per service: the release carries the rwb-integration login and polls only its own queue (DP-02, DP-10).
- The release writes `rwb_integration` only and holds no grant on `recovery` or on another `rwb_*` schema (DP-01, DP-15, BR4).
- No secret is written into a values file, a chart template, a dashboard or the runbook; the login, the ACE certificate and the contract credentials come from the platform secret store.
- The release pins the image digest, the chart version and the build ID; a rebuild between environments is not allowed, and a failing check never replaces a working release.
- No Schedule and no workflow is created for the plan status: the daily step stays with rwb-case, and a second daily run fails the review (BR3).
- The flag is the platform library's and its value is read at the start of every request; off means no outside call, not a cached answer.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module | The operation deployed, the ACE endpoint and the budget | TC-P2-E2002-OPS-01, TC-P2-E2002-OPS-03 |
| REQ-CHO-002 | Plan status change visible on the case | The flag, the live answer series and the stored fallback routing | TC-P2-E2002-OPS-04, TC-P2-E2002-OPS-05 |
| D-RCV-60 DP-05 | The ACE plan comes from the published interface, not from a view | No view access and no grant on `recovery`; the endpoint and certificate of the environment | TC-P2-E2002-OPS-02, TC-P2-E2002-OPS-03 |
| D-RCV-60 DP-10 | The daily step is rwb-case's; no P2 Schedule exists | The trigger step and the Schedule statement | TC-P2-E2002-OPS-04 |
| D-RCV-60 DP-15 | The per-service Flyway sequence owns the schema | The schema step and the no-migration rule | TC-P2-E2002-OPS-02 |
| ADR-023 | Observability per service | Five series, four alerts and four runbook entries | TC-P2-E2002-OPS-05, TC-P2-E2002-OPS-06 |

### 19. Out of scope

- The operation, the ACE client, the validation and the access check as code (RWB-P2-E2002-APP).
- The contract documents and the fakes (RWB-P2-E2002-CON); this story deploys and checks the baseline, it does not author it.
- The stored plan status, its date, the route state, the rule evaluation, the task, the timer and the decision record (RWB-P3-E2002-APP, RWB-P7-E2002-APP).
- The daily step of JOB-02 and its observation (RWB-P3-E2002-APP); this release observes the read the step calls and nothing else.
- The rule packages and their versions (RWB-P3-E2042-APP), and the no-package-in-force alert, which belongs to the case side and rwb-decision.
- The roles, the scope and the rights data (RWB-P4-E2002-APP).
- The ACE endpoint itself, its certificate and its availability, which are the ACE team's.
- The Temporal cluster, the namespace, worker versioning and the codec server as platform components (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The topic provisioning and the schema registry (RWB-PLT-EVT, RWB-PLT-TE006-CON); this release adds no topic and registers no consumer.
- The real cross-service proof of the journey (RWB-ITG-E2002-ITG).
- The exact cluster topology, node pools, replica counts and probe timings; they are set per environment by the platform team.
- The gateway-bff composite route and every screen; the deployment registers no route of its own.
