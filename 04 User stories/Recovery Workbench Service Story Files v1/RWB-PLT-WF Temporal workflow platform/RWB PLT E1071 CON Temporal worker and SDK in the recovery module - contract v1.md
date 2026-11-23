# RWB-PLT-E1071-CON Temporal worker and SDK in the recovery module - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1071-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-071 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-014, FR-PLT-015, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-071 for the workflow platform epic; the contract freezes the WorkflowGateway, the workflow-ID and task-queue conventions, the payload-codec metadata and the smoke workflow and admin operation, published on Day 1 with a fake, and every value is kept from the legacy story. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the workflow worker contract (any service team)**, I want **the WorkflowGateway interface, the workflow-ID and task-queue convention, the payload codec contract, the smoke workflow contract and the admin operation published on Day 1 with a fake**, so that **every service builds and tests its workflows without a cluster**.

This is the contract story of legacy key RWB-E1-071 under epic RWB-PLT-WF. It publishes the worker surface of the shared platform — the interface, the conventions, the codec metadata, the smoke workflow and its admin operation — as a contract document with a fake and a contract test. It owns no schema, no topic and no service base: the platform is shared platform, its namespace is the specified `rwb-recovery`, and every business value behind the surface stays with the owning service.

### 2. Business rationale

Without one published worker contract each squad invents its own queue, workflow ID, codec and start-up checks, and the first clear payload in a history is found in production. The legacy story fixed the worker inside one deployable module, where a convention held because one team wrote all the workflows. In the target there are 19 services, each running its own worker on its own queue, so the conventions have to be published before the first service builds: one gateway, one codec, one set of IDs, one smoke path.

The contract is what makes DP-11 and DP-13 real for the workflow surface. A caller starts or signals a workflow through the published WorkflowGateway and never imports a Temporal type, so a change of SDK, of cluster endpoint or of codec never reaches a business module. The payload contract is what makes NFR-045 defensible after the split: the codec metadata is declared, the key reference is declared, and a payload without metadata is refused rather than stored in clear. The contract does not decide any business value; it freezes only the shapes and the names that the app story and Epic 3 build against.

### 3. Preconditions

- RWB-PLT-E1070-CON is published: the cluster contract of namespace `rwb-recovery`, with the frontend endpoint, the mTLS certificate, the Web UI and the codec server. This contract references it and never republishes it.
- RWB-PLT-E1027-CON is published: the DecisionLogApi of the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). The smoke workflow's one activity is specified against that interface, not against a schema.
- RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-E1047-CON are published: the parameters, reference-data and naming contracts the conventions are expressed in (DP-06, DP-07, DP-14).
- The parameter names are fixed by the legacy story and kept: temporal.target, temporal.namespace, temporal.taskqueue.platform and temporal.retention.days, with the flag `rwb.p3.temporal`.
- The contract is Draft (realignment v1) and is frozen only when every consuming story passes its contract test. No approval is required to publish a Draft.
- The platform login, the platform queue row in the Ownership Map and the admin base are Not specified in the source documents (GAP-1443; ASM-2538). The contract publishes the working read of ASM-2538 and is corrected by a new version when the Wave 0 Service Catalog fixes them.

### 4. Flow

1. The contract author writes the WorkflowGateway interface: start(workflowType, workflowId, input) returning the run ID, and signal(workflowId, signal, payload), with one typed exception and no Temporal type in either signature.
2. The author writes the workflow-ID and task-queue conventions: platform-smoke-{yyyymmdd} for the platform smoke, case-{caseId} from Epic 3, `rwb-platform` for the platform smoke and health, and `rwb-<short>` per service.
3. The author writes the payload-codec contract: the AES-GCM algorithm, the Key Vault key reference, the key version in the payload metadata, and the refusal of a payload without metadata.
4. The author writes the smoke workflow contract: one activity, the decision code PLATFORM_SMOKE, the 60-second completion and the statement that no case row and no ACE row is read.
5. The author writes the admin operation contract: `POST /admin/workflows/smoke` with its request, response, errors and idempotency, and the observation that its owner is PLT in the Ownership Map.
6. The fake gateway and the fake worker are generated from the same source as the document, so the document, the tables and the fake cannot drift.
7. The contract test runs against the fake: the interfaces, the conventions, the codec refusal, the smoke workflow shape, the admin operation and the versioning rule.
8. The document and the fake are published as v1 to the contract registry, and RWB-PLT-E1071-APP, RWB-PLT-E2037-APP, RWB-PLT-E2038-APP and the Epic 3 services pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | The contract is read without the cluster contract it references | The review stops: the endpoint, the namespace and the mTLS identity are declared as references to RWB-PLT-E1070-CON and are never restated here | Review finding, no message id |
| X2 | A consumer starts a workflow with a workflow ID that is already RUNNING | The published rule returns the running execution; no second run and no second activity | None |
| X3 | A payload is handed to the codec without codec metadata | The codec refuses the payload; nothing is written to a history | Review finding, no message id |
| X4 | The admin operation is called while the flag `rwb.p3.temporal` is off | The operation is not registered and the answer is 404, as published | None |
| X5 | A consumer asks for a breaking change to an interface or a convention | The change raises v2 and deprecates v1 in place of editing v1 | None |
| X6 | A value the consumers need is named by no source: the platform login, the queue row, the admin base, the build-ID format and the codec key name | The value is published as the working read of the assumption, with the placeholder where it stays open, and the gap stays open | Not specified in the source documents (GAP-1443; ASM-2538) |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and a fake; builds nothing, starts no workflow, reads no business data, depends on nothing |
| Negotiable | The codec metadata field names, the exception type name and the fake's transport are open until the version is frozen; the conventions and the interface are fixed |
| Valuable | RWB-PLT-E1071-APP, the platform successors and every Epic 3 service start on Day 1 against the fake, without a cluster |
| Estimable | One interface, two conventions, one codec metadata block, one smoke workflow, one admin operation, one fake and one contract test |
| Small | One sprint for the document, the fake and the contract test |
| Testable | Each criterion is a schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Temporal worker and SDK in the recovery module - contract

  Background:
    Given the platform worker contract is published as v1 at status Draft
    Given the platform is shared platform and owns no schema, no topic and no service base

  Scenario: AC1 The WorkflowGateway interface is published and leaks no Temporal type (new, D-RCV-60)
    Given the WorkflowGateway interface in the package recovery.casewf.workflow
    When the interface is validated
    Then it declares start(workflowType, workflowId, input) returning the run ID and signal(workflowId, signal, payload)
    Then neither signature, nor the WorkflowRun record, imports or returns a Temporal type
    Then an unreachable frontend is published as one typed exception carrying MSG-P3-036

  Scenario: AC2 The workflow-ID and task-queue conventions are published (new, D-RCV-60)
    Given the convention section of the document
    When it is read against the platform and the services
    Then the workflow ID is platform-smoke-{yyyymmdd} for the platform smoke and case-{caseId} from Epic 3
    Then the task queue is `rwb-platform` for the platform smoke and health and `rwb-<short>` per service
    Then a repeated start with the same workflow ID returns the running execution and never starts a second run

  Scenario: AC3 The codec contract declares the algorithm, the key reference and the key version, and refuses a payload without metadata (new, D-RCV-60)
    Given the payload-codec section of the document
    When a payload is encoded and then decoded through the published contract
    Then the metadata declares AES-GCM, the Key Vault key reference and the key version
    Then a payload without codec metadata is refused and no clear value reaches a history
    Then no key, no key name in clear and no personal data appears in the document, the examples or the fake

  Scenario: AC4 The smoke workflow contract declares one activity, the decision code and the completion bound (new, D-RCV-60)
    Given the smoke workflow section of the document
    When it is compared with the app story and the fake
    Then PlatformSmokeWorkflow declares exactly one activity, PlatformSmokeActivity
    Then the activity writes decision code PLATFORM_SMOKE through the DecisionLogApi before the workflow completes
    Then the workflow completes within 60 seconds, reads no case row, no ACE row and no business table, and carries workflow ID platform-smoke-{yyyymmdd}

  Scenario: AC5 The admin operation contract is published (new, D-RCV-60)
    Given the admin operation section of the document
    When it is validated
    Then it declares POST /admin/workflows/smoke with the optional request { workflowId }, the WorkflowRun response of workflowId, runId, workflowType, status, taskQueue and startedAt, and errors 401, 403, 404, 409 and 503 with MSG-P4-001, MSG-P4-002, MSG-GEN-004 and MSG-P3-036
    Then it declares Platform administration U as the authority and the workflow ID as the idempotency key
    Then the operation names PLT as its owner in the Ownership Map

  Scenario: AC6 The fake answers every contract test and a breaking change raises v2 (new, D-RCV-60)
    Given the fake gateway and the fake worker
    When the contract test is run
    Then the fake answers a start, a duplicate start, a signal, an unreachable frontend, a payload without metadata and the flag-off 404
    Then the interfaces, the conventions, the codec declaration and the admin operation in the tables equal those in the document and in the fake
    Then a breaking change raises v2 and marks v1 deprecated, and no consumer sees an edited v1
```

These six criteria are new and test only the contract baseline: no legacy acceptance criterion is repeated here, every value is taken from the legacy story, Architecture v5, the Temporal and Drools design or the Ownership Map character for character, and the platform values that no source names are published as the working read of ASM-2538.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The WorkflowGateway is the only way a module starts or signals a workflow; no caller imports a Temporal type or builds a stub of its own | DP-11; Architecture v5 slide 11 (typed activity and workflow interface in a contract jar) |
| BR2 | The codec is the only payload path: every payload carries AES-GCM, the key reference and the key version in its metadata, and a payload without metadata is refused | NFR-045; Architecture v5 slides 23 and 35 |
| BR3 | The conventions are fixed and versioned: platform-smoke-{yyyymmdd}, case-{caseId} from Epic 3, `rwb-platform` and `rwb-<short>` | DP-10; Architecture v5 slides 20, 23 and 24 |
| BR4 | The contract carries no business value: no threshold, band, limit, reason code or decision outcome appears in an interface, a convention or an example | Template and Rules §R7.2 s17 |
| BR5 | The fake is test-only: it is published with the contract, is pinned by the consumers, and never ships in a runtime artefact | Architecture v5 slide 11 (contract tests run in every build) |
| BR6 | Versioning: a breaking change raises a new version and deprecates the old one; a published version is never edited in place | Template and Rules §R7.2; Architecture v5 slide 11 |
| BR7 | The contract names no service shard and no schema: it names the platform, the queue and the interface, and every business table stays with its owner | DP-01; Architecture v5 slides 20 and 29 |
| BR8 | The platform queue is the working read of the assumption: `rwb-platform` is published because JOB-22 places PlatformSmokeWorkflow there and Template and Rules §R4 has no platform row, and the Wave 0 Service Catalog and the Ownership Map replace it when they name it | JOB-22; Architecture v5 slide 44; ASM-2538 |

### 9. State transitions

The contract itself has three states, and it publishes one runtime transition for a caller:

| Object | From | Event | To |
|---|---|---|---|
| Contract version | Draft | The consuming stories pass their contract tests | Published |
| Contract version | Published | The consumers pin the version and no change is open | Frozen |
| Contract version | Published or Frozen | A breaking change is needed | A new version; the old one is deprecated, never edited |
| Workflow start | None | A start with an unknown workflow ID | RUNNING, and the run ID is returned |
| Workflow start | RUNNING | A start with the same workflow ID | RUNNING, and the same running execution is returned with no second run |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the conventions, the codec declaration and the fake |
| The platform owner of the workflow layer | Approves a version freeze and a breaking change |
| The service teams of the 19 services | Read the contract, confirm the queue and the ID their service will use, raise a change request |
| The ACE Common team | Owns the identity and the key path the codec references and never republishes them here |
| RWB-PLT-E1071-APP and the platform successors | Consume the interface, the conventions and the fake; pin the version |
| No delegation of authority level applies | A worker contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or the fake. Where a caller must be named, the example uses a user identifier or a role code only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes names, shapes, conventions, codes and status values only |
| Payload fields declared | The codec metadata only: the algorithm, the key reference and the key version; the payload body stays opaque to the contract |
| WorkflowRun fields | workflowId, runId, workflowType, status, taskQueue, startedAt |
| Personal data in examples | None. The workflow IDs are synthetic and carry a date, a case identifier or a counter; no name, no national identifier and no account number |
| Tables named | None. The contract names no `rwb_*` table and no schema, and the smoke writes no table of its own |
| Retention | The retention value stays the parameter temporal.retention.days; the contract states that a closed workflow leaves visibility after that value and holds no data of its own |

### 12. Contract

#### 12.1 REST operations provided

Owner PLT, taken from the Ownership Map. The operation is published on the platform and not inside a service base.

| Method | Path | Purpose | Access | Errors | Idempotency |
|---|---|---|---|---|---|
| POST | `/admin/workflows/smoke` | Run PlatformSmokeWorkflow on demand and return its run | Platform administration, right U | 401 (MSG-P4-001); 403 no Platform administration U (MSG-P4-002); 404 flag off; 409 the workflow ID already completed (MSG-GEN-004); 503 Temporal unreachable (MSG-P3-036) | Workflow ID |

Request: body optional, { workflowId: string }, default platform-smoke-{yyyymmdd} in the server time zone. Response: 200 WorkflowRun with workflowId, runId, workflowType, status, taskQueue and startedAt. The host, the admin base and the platform login of the operation are Not specified in the source documents (GAP-1443; ASM-2538); the path and the owner are taken from the Ownership Map.

#### 12.2 REST operations consumed

None. This contract consumes no operation: it publishes the interface, the conventions, the codec declaration and the admin operation, and it names the contracts it references without calling them.

#### 12.3 Events published

None. The platform publishes no topic of its own. The decision record that the smoke activity writes travels on `rwb.decision-record.v1` through the library of RWB-PLT-E1027-CON, whose type owner is P7; this contract declares the code PLATFORM_SMOKE and no event schema.

#### 12.4 Events consumed

None. The worker consumes no topic and the smoke workflow waits on its one activity.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract declares |
|---|---|---|---|
| WorkflowGateway | Published interface | `rwb-platform` | start(workflowType, workflowId, input) returning the run ID; signal(workflowId, signal, payload); one typed exception carrying MSG-P3-036 |
| PlatformSmokeWorkflow | Workflow | `rwb-platform` | One activity, then complete within 60 seconds; workflow ID platform-smoke-{yyyymmdd}; no case row and no ACE row |
| PlatformSmokeActivity | Activity | `rwb-platform` | Writes decision code PLATFORM_SMOKE through the DecisionLogApi before the workflow completes, and returns the build ID |

The contract publishes the two Temporal interfaces as a contract jar and nothing else: a consumer imports the interface, never a workflow implementation, and never a Temporal type.

#### 12.6 Schedules

None. The JOB-22 Schedule is declared by RWB-PLT-E1071-APP section 12.6; the contract states only that a platform Schedule starts PlatformSmokeWorkflow at 06:00 on `rwb-platform` with overlap SKIP and a catch-up window, and creates none.

#### 12.7 Tables owned

None. The contract owns no `rwb_*` schema and no table, and it names no table of another owner.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Fake gateway (this story) | start, a duplicate start that returns the running execution, a signal, and the unreachable frontend exception with MSG-P3-036 | RWB-PLT-E1071-APP, RWB-PLT-E2037-APP, RWB-PLT-E2038-APP |
| Fake worker (this story) | The PlatformSmokeWorkflow and PlatformSmokeActivity shapes, the PLATFORM_SMOKE decision code and the 60-second completion, with the flag-off 404 | RWB-PLT-E1071-APP and the Epic 3 workflow tests |

The fakes answer from the published document rather than from copied payloads, so a change of interface or convention shows up as a contract-test failure in every consumer.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation (`POST /admin/workflows/smoke`, owner PLT) | 0 | OpenAPI 3.1, one problem envelope, `Idempotency-Key` carried as the workflow ID |
| Kafka | 0 | 0 | The contract declares no topic and no event schema; the decision record belongs to the P7 library and `rwb.decision-record.v1` |
| Temporal | 1 interface (WorkflowGateway) and 1 workflow (PlatformSmokeWorkflow) with its activity | 0 | Published as a contract jar in namespace `rwb-recovery`, on task queue `rwb-platform` |
| File | 0 | 0 | No file is declared |

### 13. Solution plan

**Deliverables.** `workflow-gateway.yaml` (the interface and the WorkflowRun record), the convention section (workflow IDs and task queues), the codec metadata declaration, `platform-smoke.yaml` (the workflow and its activity, the decision code and the completion bound), `admin-workflows.yaml` (the admin operation), the fake gateway, the fake worker and the contract test.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; the contract names no table and no schema | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the smoke activity is specified against the DecisionLogApi | H RWB-PLT-E1027-CON (of the app story) |
| DP-06 | Parameters, casewf.config | The parameter names the conventions read are published, and their values stay with the parameters contract | H RWB-PLT-E1042-CON (of the app story) |
| DP-07 | Reference data, LOV | The decision code PLATFORM_SMOKE is a LOV-DECISION value; the list is referenced, never copied | H RWB-PLT-E1043-CON (of the app story) |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; the Schedule row is named here and declared by the app story | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout; the gateway is the one published interface of the workflow surface | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` for the services; the platform operation sits on its own path with no service base | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library, referenced and not republished | H RWB-PLT-E1047-CON (of the app story) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the contract owns no migration | H RWB-PLT-E1044-CON (of the app story) |
| DP-19 | Screen, ace-web | gateway-bff composite route; the contract exposes no screen path | H RWB-PLT-N001-CON (of the app story) |

The pattern that matters most for a contract is DP-11: the gateway is the one published interface of the workflow surface, so an in-process call becomes a typed call across the platform boundary with a 2 s budget and one hop, and every Temporal detail stays behind it. DP-10 is applied by naming the platform Schedule and its queue instead of a Quartz job, and DP-13 by publishing the admin operation on its own path with no service base and no repetition of the monolith path.

**Build steps**

1. Write `workflow-gateway.yaml` with the two operations, the WorkflowRun record and the one typed exception; prove no Temporal type appears in either signature.
2. Write the convention section: the two workflow-ID patterns, the platform queue, the per-service queue pattern, the duplicate-start rule and the build-ID rule.
3. Write the codec declaration: AES-GCM, the key reference, the key version in the metadata, the refusal rule and the statement that no key appears in the document or a test.
4. Write `platform-smoke.yaml` with the workflow, its one activity, the decision code, the 60-second completion and the no-case-row and no-ACE-row rule.
5. Write `admin-workflows.yaml` with the request, the response, the five error answers, the authority and the idempotency key, and record PLT as the owner.
6. Generate the fake gateway and the fake worker from the same source as the tables, so document, tables and fakes cannot drift, plus the personal-data scan over every example.
7. Publish v1 to the contract registry, notify RWB-PLT-E1071-APP, RWB-PLT-E2037-APP, RWB-PLT-E2038-APP and the Epic 3 services, and record the version they pin.

**Done when.** The document validates, every convention and every interface matches the tables and the fakes, the codec refusal and the duplicate-start rule are asserted, and the contract test of this story is green in the build.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P3-036 | The workflow service is unreachable or refuses a start | The workflow service is not available. Try again in a few minutes. | 503 of the admin operation, and the one typed exception of the gateway |
| MSG-P3-032 | A required parameter has no value at start-up | Parameter {name} has no value for {environment}. The service did not start. | Start-up failure, published and not raised by the contract itself |
| MSG-P4-002 | A role without Platform administration U calls the admin operation | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-001 | No session, or the session has expired | Existing message catalogue entry; its text is not restated in the source documents | 401 |
| MSG-GEN-004 | The same workflow ID has already completed | Existing message catalogue entry; its text is not restated in the source documents | 409 |

No identifier is renumbered by the realignment. The refusal of a payload without codec metadata is a contract rule and not a user message: it fails the encoder or the decoder and writes nothing, so it carries no message identifier.

### 15. Screens and states

No screen in this story, and the contract declares none. The admin operation is the surface a platform administration screen would call; the smoke run states it publishes are Not run, Running, Completed and Failed, and the screen itself, if one is built, belongs to the platform observability work and not to this contract.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1071-CON-01 | AC1 | Contract | The gateway document: two operations, the WorkflowRun record, the typed exception, and the no-Temporal-type assertion on both signatures |
| TC-PLT-E1071-CON-02 | AC2 | Contract | The convention section compared with the platform queue, the Epic 3 case pattern and the duplicate-start rule |
| TC-PLT-E1071-CON-03 | AC3 | Contract | The codec declaration: AES-GCM, the key reference, the key version; a round trip; a payload without metadata refused; a scan for a key in clear |
| TC-PLT-E1071-CON-04 | AC4 | Component | `platform-smoke.yaml` and the fake worker: one activity, decision code PLATFORM_SMOKE, 60 seconds, no case row and no ACE row |
| TC-PLT-E1071-CON-05 | AC5 | Contract | `admin-workflows.yaml`: the request, the response, the five error answers, Platform administration U and the workflow-ID idempotency key |
| TC-PLT-E1071-CON-06 | AC6 | Component | The fake gateway and the fake worker answering every contract test; the table-to-document equality; a breaking change raising v2 |

### 17. Guardrails

- One published interface for the workflow surface: no caller imports a Temporal type, builds its own stub or starts a workflow outside the gateway.
- The codec is the only payload path: the metadata carries the algorithm, the key reference and the key version, and a payload without metadata is refused; no key, no key name in clear and no personal data appears in the document, the examples or the fakes.
- No business value in the contract: thresholds, bands, limits, reason codes and decision outcomes stay with the owner or the parameters.
- No personal data in examples: workflow IDs are synthetic and carry a date, a case identifier or a counter only.
- No schema and no table in the contract: the platform owns no `rwb_*` schema, and every business table stays with its owner (DP-01).
- The fake is test-only and is pinned by the consumers; it never ships in a runtime artefact.
- The monolith base is never republished: the admin operation sits on its own platform path (DP-13).
- The contract is versioned: a breaking change raises v2 and deprecates v1 in place of editing v1.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-DRI-010 | Every threshold, limit and name is a versioned parameter | Business Requirements Epic 1, 3.2; Program, 5.1 and 5.7; R-UNI-38 | TC-PLT-E1071-CON-02, TC-PLT-E1071-CON-03 |
| REQ-DRI-005 | No action proceeds if its decision entry cannot be written | Business Requirements Epic 1, 3.7; R-UNI-39 | TC-PLT-E1071-CON-04 |
| REQ-DRI-007 | A failed start reaches a named owner; a retry is safe | Business Requirements Epic 1, 3.2; Program, 5.2; R-UNI-40 | TC-PLT-E1071-CON-05, TC-PLT-E1071-CON-06 |
| NFR-045 | No clear personal data in a workflow history, a log, an event or a test | Non-functional requirements, security and PDPA | TC-PLT-E1071-CON-03 |
| ADR-016 | A reusable Temporal layer, and Schedules replace Quartz | Architecture Decision Records, ADR-016; DP-10 | TC-PLT-E1071-CON-02, TC-PLT-E1071-CON-05 |
| DP-10, DP-11, DP-13 | Schedule instead of Quartz; one hop through a published interface; no monolith base | Template and Rules §R5.5; Architecture v5 slides 11, 20, 23, 24 and 27 | TC-PLT-E1071-CON-02, TC-PLT-E1071-CON-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1071-APP | App development | H consumer: implements the gateway, the worker lifecycle, the codec, the smoke workflow, the Schedule and the admin operation against this contract and its fakes |
| RWB-PLT-E1070-CON | Contract | The cluster contract this contract references for the endpoint, the namespace and the mTLS identity |
| RWB-PLT-E1027-CON | Contract | The DecisionLogApi the smoke activity is specified against |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | The parameters, reference-data, naming, Flyway and edge contracts the conventions are expressed in |
| RWB-PLT-E2037-APP, RWB-PLT-E2038-APP | App development | Consumers: the observability and run books, and the codec server and admin audit, both pinned to this contract |
| RWB-PLT-TE001-APP | App development | X: the module boundary tests that enforce the package rule this contract declares |
| RWB-E2-037, RWB-E2-038, RWB-E2-039, RWB-E2-040 | Legacy Epic 2 keys | Successors of the legacy scope left out of this contract; each is realigned by its own story |

### 19. Out of scope

- The implementation of the gateway, the worker, the codec, the smoke workflow and the Schedule (RWB-PLT-E1071-APP).
- The cluster, the namespace, the certificates and the Web UI (RWB-PLT-E1070-CON and RWB-PLT-E1070-APP).
- The workflow kit templates and the codec server (RWB-PLT-N010-APP and RWB-PLT-N010-CON).
- The decision-record library and its schema (RWB-PLT-E1027-CON, RWB-P7-E1027-CON).
- The case workflows and the case task queue of Epic 3, and the case-{caseId} convention beyond the name it publishes here.
- The observability, codec-server and admin-audit surfaces (RWB-PLT-E2037-APP, RWB-PLT-E2038-APP).
- The Quartz scheduler and the retired RWB-TE-007 scope.
