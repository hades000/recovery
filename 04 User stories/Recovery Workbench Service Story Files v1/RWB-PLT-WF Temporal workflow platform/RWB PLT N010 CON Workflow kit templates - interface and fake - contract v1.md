# RWB-PLT-N010-CON Workflow kit templates - interface and fake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N010-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N010 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform contract story for the workflow kit interface, the codec server protocol and their fakes, with no legacy story behind it. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the workflow kit interface**, I want **the eight template interfaces, their typed parameter models and the payload codec server protocol published on Day 1 as one versioned interface artefact with a working fake**, so that **every Recovery service in waves 1 to 4, and any later workbench, builds and tests its approval, task, saga, schedule, notification, intake, agent and partner-instruction steps against one frozen set of interface names, parameter fields and protocol codes before the kit library exists**.

This is the contract story of new platform key N010 under epic RWB-PLT-WF. It publishes, for the L3 layer of Architecture v5 slide 23 and Temporal and Drools design slide 12:

- The kit interface document and its jar: the eight template interfaces, the input and output model of each, the signals each accepts and the activity interface each requires of its caller.
- The typed parameter models: every business value — a threshold, a DoA band, an SLA duration, a queue code — arrives as a typed field of a template input and never as a constant of the library.
- The codec server protocol document: POST /decode and POST /encode of the Temporal codec server protocol, with the request and response models and the 401, 403, 413, 422 and 503 answers.
- The kit fake and the codec fake: a deterministic implementation of the eight templates and both protocol operations, including every refusal case, so that a consumer can build before the library and the server exist.
- The version rule and the contract test: a breaking change raises a new version, v1 is never edited in place, and the test fails the build on a drift of a name, a field or a code.

The workflow platform is shared platform and not one of the 19 services: Template and Rules §R4 has 19 service rows and no platform row, so the platform owns no `rwb_*` schema, no topic, no REST base of its own and no service task queue. What the sources do state is used as it stands: the Temporal namespace rwb-recovery (Architecture v5 slides 8, 9 and 24), the platform task queue `rwb-platform` (Ownership Map JOB-22 and Architecture v5 slide 44) and the PLT-owned admin operation POST /admin/workflows/smoke (Ownership Map), all as the working read of the assumption. The rest of the platform identity, the version label of the kit and the codec key names are Not specified in the source documents (GAP-1439; ASM-2534).

### 2. Business rationale

The kit only pays for itself if it is frozen before nineteen services build against it. A template whose input model changes after the first consumer pins it breaks a worker build in a wave that is already running, and a codec protocol that leaves the refusal codes to the implementation turns every decode failure into a different answer in every environment. Publishing the interface first, with a fake, is what lets RWB-PLT-N010-APP build against a fixed target and lets the wave 1 services plan their workers without waiting for the library.

The contract also carries the rule that makes the library reusable. A workbench other than Recovery takes the kit only if an interface carries no business term, so the published document is also the test of that rule: if a field name says treatment or write-off, the version fails the review. The same document fixes the two boundaries that cannot be left to a team — the DoA lookup as a parameter of approval rather than a table of the kit, and the codec metadata as the only source of the key version — because both decide whether a decision record and a workflow history are defensible in an audit.

The measurement is simple: a wave 1 service compiles against the published jar and passes its contract tests against the fake without a change to the interface, and a key rotation is answered by the protocol document and the codec fake rather than by a code change.

### 3. Preconditions

- The Temporal namespace rwb-recovery and the L1 and L2 layers are fixed by RWB-PLT-E1070-CON: one cluster per environment on ACE AKS, own persistence database, UI, metrics and codec server, version 1.30 or later, namespace rwb-recovery (Architecture v5 slides 23 and 24).
- The semantic-versioning rule of the kit is fixed: one version covers the eight templates together, a breaking change raises the major number, and a published version is never edited in place (Architecture v5 slide 23).
- The codec server protocol is the Temporal codec server protocol: POST /decode and POST /encode, the request and response models of that protocol, and the payload metadata that carries the codec name and the key version.
- The payload encryption rule is fixed: AES-GCM with a key in Azure Key Vault, one key per environment, the key version recorded in the payload metadata, every enabled version decodable (Architecture v5 slides 11 and 24).
- The activity interface rule is fixed: each service publishes a typed activity interface on its own task queue, and a caller imports only the interface (Architecture v5 slide 23, L4).
- The decision-record library is the only way a template causes a business record: the record is written by the caller in the caller's schema (DP-03, RWB-PLT-E1027-CON).
- The platform task queue and the platform identity are as the assumption row of this story reads: namespace rwb-recovery, task queue `rwb-platform`, workload identity SY-CASEWF, codec key in Key Vault.
- No approval is required to publish a Draft contract: the interface is published at status Draft (realignment v1) and is frozen when the consuming stories pass their contract tests.

### 4. Flow

1. Write the interface document: the eight template interfaces, the input and output model of each, the signals and the activity interface each requires, with one section per template.
2. Write the parameter models as typed fields, and mark each field with the source of its value: a parameter identifier of RWB-PLT-E1042-CON, a reference row of RWB-PLT-E1043-CON, or an identifier the caller owns.
3. Generate the jar from the document: one interface per template, one input model, one output model, one signal set and one required activity interface, with no implementation.
4. Write the codec server protocol document: the two operations, the request and response models, the metadata field and the five refusal codes with their triggers.
5. Add the lint rules: no business term, no schema name, no topic name and no service short in any identifier; a semantic version on the artefact; every parameter field typed.
6. Build the kit fake from the document: the eight templates with deterministic replay, every signal answered, every activity stubbed, and the codec fake with both operations and all five refusals.
7. Publish v1 to the contract registry, notify RWB-PLT-N010-APP and the wave 1 to 4 services, and record the version each consumer pins.
8. Run the contract test against the fake on every change: a drift of a name, a field or a code fails the build, and a breaking change raises v2 and deprecates v1.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An interface identifier, a field name or an example carries a business term, a schema name, a topic name or a service short | The lint step fails the build and the version is not published | MSG-PLT-N010-11 | AC1 |
| X2 | A parameter model carries a literal business value instead of a typed field | The review rejects the change; the value becomes a typed field or a reference row | MSG-PLT-N010-12 | AC2 |
| X3 | A protocol operation is published without its request model, its response model or one of the five codes | The lint step fails the build; the protocol document is not published | MSG-PLT-N010-13 | AC3 |
| X4 | The fake answers a case with a different result on a second run of the same input | The determinism step fails the build; the fake is corrected, never the test | MSG-PLT-N010-14 | AC4 |
| X5 | A consumer needs a breaking change | v2 is raised, v1 is marked deprecated and stays pinnable, and no consumer sees an edited v1 | MSG-PLT-N010-15 | AC5 |
| X6 | A value the consumer needs is named by no source (platform task queue, version label, key names) | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-1439; ASM-2534) | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, a jar and two fakes; builds no runtime, reads no business data, depends on no service |
| Negotiable | The field names of the parameter models, the signal names and the example values are open until v1 is frozen; the eight templates, the protocol and the no-business-term rule are fixed |
| Valuable | RWB-PLT-N010-APP and every wave 1 to 4 service start on Day 1 against a frozen interface and a deterministic fake |
| Estimable | One interface document, one jar, one protocol document, two fakes and one contract test |
| Small | One sprint for the document, the jar, the fakes and the lint rules |
| Testable | Each criterion is a lint rule, a schema assertion, a fake behaviour or a contract-test failure in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the workflow kit interface, the codec server protocol and their fakes

  Background:
    Given the kit is one versioned library of eight generic templates with no business term in an interface
    Given the codec server speaks the Temporal codec server protocol

  Scenario: AC1 The kit interface document and jar are published as a versioned artefact with the eight template interfaces and no business term (new, D-RCV-60)
    Given the kit interface artefact to be published
    When it is published with a semantic version
    Then it declares the interfaces of Approval, Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job and Partner instruction
    Then every interface declares one input model, one output model, its signals and the activity interface it requires of its caller
    Then no identifier, field name or example carries a business term, and the jar and the document name the same version

  Scenario: AC2 The template parameter models are typed and versioned and every business value arrives as a parameter (new, D-RCV-60)
    Given the template parameter models of the eight templates
    When they are reviewed against the parameter and reference-data contracts
    Then every business value is a typed field: a threshold, a DoA band, an SLA duration and a queue code each arrive as a field of the input model
    Then each field names its source: a parameter identifier, a reference row or an identifier the caller owns
    Then a change to a field is a version change, and no literal business value appears in the document, the jar or an example

  Scenario: AC3 The codec server protocol declares both operations, the models and the five answers (new, D-RCV-60)
    Given the codec server protocol document
    When it is validated
    Then it declares POST /decode and POST /encode with a request model and a response model for each
    Then it declares 401 when the caller is not authenticated, 403 when the caller is not authorised to decode, 413 when a payload is above the size limit, 422 when codec metadata is missing or the key version is not enabled, and 503 when the key service does not answer
    Then it states that the key version is read from the payload metadata and that no payload appears in a log

  Scenario: AC4 The fake implements the eight templates and both codec operations, with deterministic replay and every refusal case (new, D-RCV-60)
    Given the kit fake and the codec fake generated from the published artefacts
    When the same input is replayed twice
    Then the fake returns the same output, the same signal order and the same timestamps, and a template that waits on a signal answers the signal it is given
    Then the codec fake answers both operations for an enabled key version and returns the 401, 403, 413, 422 and 503 refusal cases on demand
    Then the fake answers an activity through the caller's stub and never calls a real service

  Scenario: AC5 The contract test fails on a breaking change and raises a new version, and v1 is never edited in place (new, D-RCV-60)
    Given the published v1 interface and its contract test
    When a field is removed, a field type changes, a signal changes or a refusal code changes
    Then the contract test fails the build and the change is refused against v1
    Then the change is published as v2, v1 is marked deprecated and stays pinnable, and a consumer sees the version it pinned until it upgrades

  Scenario: AC6 The published interface names no schema, no topic and no service short, and the platform task queue is the working read (new, D-RCV-60)
    Given the published v1 interface names and the platform identity of this story
    When every identifier, field and example is scanned
    Then no identifier contains a schema name, a topic name or a service short, and no interface names a queue of its own
    Then the platform task queue `rwb-platform` and the namespace rwb-recovery are carried as the working read of the assumption, with the gap and the assumption cited, and a change to either is a v2 publication
```

These criteria are new and test only the interface and the fake: this key has no legacy story, no legacy acceptance criterion and no legacy test case, and every value quoted comes from Architecture v5, the Temporal and Drools design or the Ownership Map.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The kit is one versioned library of eight generic templates with no business term in L1 to L3 interfaces | Architecture v5 slide 23; Temporal and Drools design slide 12 |
| BR2 | Every business value is a typed parameter or a reference row: a threshold, a DoA band, an SLA duration and a queue code are never a constant | DP-06, DP-07; Architecture v5 slide 23 |
| BR3 | An interface declares one input model, one output model, its signals and the activity interface it requires; the caller supplies the activity implementation | Architecture v5 slide 23, L4 |
| BR4 | The codec server speaks the Temporal codec server protocol: POST /decode and POST /encode, the key version from the payload metadata, no clear fallback | Architecture v5 slides 11 and 24 |
| BR5 | The refusal set is fixed: 401, 403, 413, 422 and 503, each with one trigger and one meaning | Temporal codec server protocol; RWB-PLT-E1071-CON |
| BR6 | The fake is deterministic: the same input gives the same output, the same signal order and the same timestamps, and it calls no real service | Template and Rules §R7.2 s16 |
| BR7 | A breaking change raises a new version and deprecates the old one; a published version is never edited in place | Template and Rules §R8.2; Architecture v5 slide 23 |
| BR8 | The platform owns no schema, no topic, no REST base of its own and no service task queue; the namespace rwb-recovery, the platform task queue and the smoke operation are used as the sources state them | Template and Rules §R4; Ownership Map |
| BR9 | No personal data in an example, a model or a fake fixture: identifiers, codes and times only | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Interface written | The eight template interfaces and both protocol operations exist in the working tree | In review |
| In review | Review closes | No business term, no schema, no topic and no service short; every parameter field typed | Published |
| Published | v1 frozen | The first consumer passes its contract test against the fake | Frozen |
| Frozen | Additive change | A field is added with a default and the minor number rises | Published |
| Frozen | Breaking change | A field, a type, a signal or a code changes and v2 is published | Deprecated |
| Deprecated | Last consumer upgrades | No consumer pins the old version | Retired |
| Published | Contract test runs | The document, the jar and the fake agree | Published |

This table is the lifecycle of the published contract. It has no runtime state: a template run belongs to Temporal and a codec request belongs to the server, and neither is a state of this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the interface document, the jar, the protocol document and the two fakes |
| The platform team | Owns the version rule, approves a breaking change and a freeze, and retires a version |
| The service teams of waves 1 to 4 | Read the interface, pin a version, raise a change request; they never edit the document or fork an interface |
| The architecture review | Accepts the eight template names, the activity interface rule and the protocol |
| The security administration role RW-SECADM | Confirms the key-version rule and the no-payload-in-a-log rule of the protocol document |
| SCB IT infrastructure | Owns the Key Vault instance and the key versions the protocol document names |
| No delegation of authority level applies | An interface contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, the jar, the fake or an example. Where a caller must be named, the example uses a user identifier or a role code only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes interface names, model fields, signal names and protocol codes; no customer, account, case or document value appears |
| Business data in the fake | None. Every fixture is synthetic, with identifiers, codes and times only |
| Key material | None in the document or the fake: the protocol names the key version and the Key Vault unwrap, and it holds no key, no key name and no secret |
| Payload in an example | None. The protocol examples show a ciphertext placeholder and the metadata field, never a clear payload |
| Parameter values | None fixed. A parameter field names its source — a parameter identifier, a reference row or an identifier the caller owns — and carries no value |
| Field identifiers | None owned. Every field is an interface field of this contract or a field of the caller's activity interface |
| Retention | None. The document keeps no data; a workflow history and its retention belong to RWB-PLT-E1070-CON |

### 12. Contract

#### 12.1 REST operations provided

| Operation | Request model | Response model | Answers | Owner |
|---|---|---|---|---|
| POST /decode | CodecDecodeRequest: namespace, workflow identifier, run identifier, encoded payloads | CodecDecodeResponse: decoded payloads | 200, 401, 403, 413, 422, 503 | PLT |
| POST /encode | CodecEncodeRequest: namespace, workflow identifier, run identifier, clear payloads | CodecEncodeResponse: encoded payloads with the current key version in the metadata | 200, 401, 403, 413, 422, 503 | PLT |

Both operations are served from the codec server root on the platform internal ingress, on the codec server of RWB-PLT-E1070-CON: they are not under the edge base, they are not published through gateway-bff, and they carry no service segment. The paths and the request shape are the two operations of the Temporal codec server protocol and are copied as they stand.

#### 12.2 REST operations consumed

None. This contract calls no REST service: the kit reaches an owner through the caller's activity interface, and the protocol document describes the server that a caller calls and not a client of this story.

#### 12.3 Events published

None. The platform owns no topic. A template causes a decision record through the caller, and the caller's library publishes it under RWB-PLT-E1027-CON; this contract publishes no event schema.

#### 12.4 Events consumed

None. A template is started by the caller's API or the caller's Schedule, and this contract consumes no Kafka topic.

#### 12.5 Workflows and activities

| Template interface | Input model | Output model | Signals | Activity interface it requires |
|---|---|---|---|---|
| ApprovalTemplate | ApprovalInput: subject reference, DoA lookup, DoA band, SLA duration, maker set, checker set | ApprovalResult: outcome, deciding user, decided at | approve, return, refuse, pause, resume | DecisionRecordActivity (RWB-PLT-E1027-CON) and the caller's ApplyOutcomeActivity |
| NotifyTemplate | NotifyInput: template code, recipient reference, channel code, correlation identifier, dispatch window | NotifyResult: notice reference, dispatched at, proof reference | cancel | The caller's NotifyActivity, which calls the notice owner |
| DocumentIntakeTemplate | IntakeInput: intake channel, document type code, retention code, correlation identifier | IntakeResult: document reference, checksum, stored at | abandon | The caller's AcceptDocumentActivity, which calls the document owner |
| AgentRunTemplate | AgentRunInput: policy reference, rule package code, fallback threshold, correlation identifier | AgentRunResult: answer source, rule reference, answered at | cancel | The caller's RunAgentActivity and EvaluateRulesActivity (RWB-PLT-E1072-CON) |
| HumanTaskTemplate | TaskInput: task subject reference, queue code, SLA duration, escalation target, correlation identifier | TaskResult: completing user, outcome code, completed at | complete, pause, resume, escalate | The caller's CreateTaskActivity and RecordDecisionActivity |
| SagaRunnerTemplate | SagaInput: step list, pivot index, strict flag, idempotency seed | SagaResult: completed steps, compensated steps, pivot reached, closed at | abort | The caller's RunStepActivity, CompensateStepActivity and ConfirmLedgerActivity |
| ScheduledJobTemplate | ScheduleInput: schedule identifier, cron, business calendar reference, catch-up window, idempotency seed | RunResult: business date, run outcome, completed at | skip, force | The caller's RunJobActivity |
| PartnerInstructionTemplate | InstructionInput: partner reference, instruction type code, SLA duration, reminder policy, correlation identifier | InstructionResult: instruction reference, result code, received at | result, cancel | The caller's IssueInstructionActivity, which calls the partner owner |

Eight template interfaces and their required activity interfaces. An activity interface is declared here as the caller's obligation and is implemented by the caller on its own task queue; this contract publishes no activity implementation and no queue of its own.

#### 12.6 Schedules

None. This contract owns no Schedule and registers none: the Scheduled job template declares the Schedule parameters and the caller registers the Schedule at run time.

#### 12.7 Tables owned

None. The platform owns no `rwb_*` schema and no table; a record caused by a template is written by the caller's activity through RWB-PLT-E1027-CON in the caller's schema.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Kit fake (this story) | The eight template interfaces, the parameter models, every signal and the deterministic replay | RWB-PLT-N010-APP, the wave 1 to 4 services, another workbench |
| Codec fake (this story) | POST /decode and POST /encode, the metadata rule and the 401, 403, 413, 422 and 503 refusals | RWB-PLT-N010-APP, the Web UI test of RWB-PLT-E2038-APP |
| rwb-decision fake (P7) | The decision-record write and the central ledger confirmation the Approval and Saga runner interfaces require | The kit fake and the Approval and Saga runner tests |

The kit fake answers an activity through the caller's stub and never through a copied payload, so a change to a caller's activity interface shows up as a contract-test failure in that caller.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 codec server operations, POST /decode and POST /encode, on the platform internal ingress | 0 | Temporal codec server protocol; five refusal codes |
| Kafka | 0 | 0 | The platform owns no topic |
| Temporal | 8 template interfaces | 0 | One namespace rwb-recovery; each interface declares the activity interface it requires |
| File | 0 | 0 | No file crosses the kit |

### 13. Solution plan

**Deliverables.** `workflow-kit-api.md` (the eight template interfaces with their input and output models, signals and required activity interfaces), `workflow-kit-api.jar` (the same interfaces as types), `codec-server-protocol.md` (the two operations, the models, the metadata field and the five answers), the kit fake, the codec fake and the contract test.

**Components**

| Component | Responsibility |
|---|---|
| InterfaceDocument | The eight template interfaces, the model fields, the signals and the required activity interfaces |
| InterfaceJar | The same interfaces as generated types, with the semantic version and no implementation |
| ParameterModelSet | The typed parameter fields and the source of each value |
| ProtocolDocument | POST /decode and POST /encode, the request and response models and the five answers |
| KitFake | The eight templates, deterministic replay, every signal and a stub for every required activity |
| CodecFake | Both protocol operations, the metadata rule, the size limit and the five refusals |
| ContractTest | The drift test over the document, the jar and the fake, and the breaking-change check |

**Versioning rule.** One semantic version covers the interface document, the jar and the two fakes together. An additive field with a default raises the minor number; a removed or retyped field, a changed signal or a changed refusal code raises the major number; a wording fix raises the patch number. v1 is frozen at the first consumer and is never edited; a change is always a new version.

**Pattern application.** The metadata row "Patterns applied" reads None: N010 is a new platform key with no legacy marker, so no Template and Rules §R5.5 row is applied here. DP-03, DP-06 and DP-07 appear in section 18 only as the library contracts its parameter models point at, and this contract adds no dependency of its own; it is a CON story and starts on Day 1.

**Build steps**

1. Write the interface document with one section per template and one table of fields per model.
2. Generate the jar from the document and prove that the generated types and the documented fields agree.
3. Write the parameter models with the source of each value, and mark every field that comes from a parameter or a reference row.
4. Write the protocol document with both operations, the models, the metadata field and the five answers.
5. Add the lint rules: no business term, no schema name, no topic name, no service short, one semantic version, every field typed.
6. Build the kit fake and the codec fake, with the deterministic replay and the refusal cases.
7. Write the contract test and prove that a removed field, a retyped field, a changed signal and a changed code each fail the build.
8. Publish v1, notify the consumers, record the pinned version, and publish v2 in place of any breaking change.

**Done when.** The document, the jar and the fakes carry one version; every lint rule passes; the contract test is green on v1 and red on each of the four breaking changes; and a consumer answers every case of section 16 against the fake without a real service.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-PLT-N010-11 | An identifier, a field or an example carries a business term, a schema, a topic or a service short | The interface {name} carries a term the kit does not allow. The publication stopped and the version is unchanged. |
| MSG-PLT-N010-12 | A parameter model carries a literal value instead of a typed field | The field {name} carries a value instead of a source. Name the parameter, the reference row or the caller's identifier. |
| MSG-PLT-N010-13 | A protocol operation is published without a model or without one of the five answers | The operation {name} is incomplete: {missing} is not declared. The protocol document is not published. |
| MSG-PLT-N010-14 | The fake returns a different result on a replayed input | The fake is not deterministic for {case}. The build stopped and the fake was not published. |
| MSG-PLT-N010-15 | A breaking change is proposed against a frozen version | The change to {field} breaks version {version}. Publish it as a new major version; the published version is never edited. |
| MSG-PLT-N010-16 | The contract test finds a drift between the document, the jar and the fake | The document, the jar and the fake disagree on {element}. The build stopped. |

The six identifiers are contract messages of this story and not business messages: none names a customer, an account, a case or a business value.

### 15. Screens and states

No screen in this story, and the document declares none: it publishes an interface, a protocol and two fakes. The states it fixes are the version states of section 9 and the protocol answers of section 12.1, and the only surface a person sees is the Temporal Web UI of RWB-PLT-E1070-APP, where decode is authorised and audited by RWB-PLT-E2038-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N010-CON-01 | AC1 | Contract | The document and the jar: eight template interfaces, one version, one input and one output model each, the signals and the required activity interfaces; a business-term scan of every identifier |
| TC-PLT-N010-CON-02 | AC2 | Contract | The parameter models: a threshold, a DoA band, an SLA duration and a queue code as typed fields, each with its source, and a sample field change raising the version |
| TC-PLT-N010-CON-03 | AC3 | Contract | The protocol document: both operations, the request and response models, the metadata field and the 401, 403, 413, 422 and 503 triggers |
| TC-PLT-N010-CON-04 | AC4 | Component | The kit fake replayed twice with the same input, every signal answered, and the codec fake on both operations with all five refusals |
| TC-PLT-N010-CON-05 | AC5 | Component | The contract test on a removed field, a retyped field, a changed signal and a changed code; v1 frozen and v2 published in place of the change |
| TC-PLT-N010-CON-06 | AC6 | Contract | The published names of v1 scanned for a schema, a topic and a service short; the namespace rwb-recovery and the platform task queue `rwb-platform` carried as the working read with the gap and the assumption cited |

### 17. Guardrails

- No business value in the interface: a threshold, a DoA band, an SLA duration and a queue code are typed fields with a named source, and a literal value fails the lint step.
- No personal data in an example, a model or a fixture: identifiers, codes and times only, and a synthetic fixture that carries a name fails the build.
- ACE data only through the owner's contract or the recovery.v_ace_* views: this contract publishes no ACE read and names no ACE view in an interface.
- No key or secret in the document, the jar or a test: the protocol names the key version and the Key Vault unwrap, and a key never appears in a file.
- No payload in a log: the protocol document states the rule for the server, and an example shows a ciphertext placeholder only.
- No schema name, no topic name and no service short in an identifier: the caller supplies its own activity interface and its own queue.
- The published version is never edited: a breaking change raises a new major version, and the old version stays pinnable until the last consumer upgrades.
- The fake is deterministic and calls no real service; a fake that needs a live service is not published.
- The platform identity is cited, not invented: the namespace and the task queue come from the assumption row and a change to either is a new version.

### 18. Traceability

| Source | Element | Test cases |
|---|---|---|
| Architecture v5 slide 23 | The L3 kit as a versioned library of eight generic templates with no business terms, owned by the platform team | TC-PLT-N010-CON-01, TC-PLT-N010-CON-06 |
| Architecture v5 slide 23, L4 | A typed activity interface published per service on its own task queue; the caller imports only the interface | TC-PLT-N010-CON-01, TC-PLT-N010-CON-02 |
| Architecture v5 slides 11 and 24 | The codec with AES-GCM and Key Vault keys, the codec server for the UI, the key version in the payload metadata | TC-PLT-N010-CON-03, TC-PLT-N010-CON-04 |
| Temporal and Drools design slide 12 | The eight templates named one by one and the layer the platform owns | TC-PLT-N010-CON-01 |
| DP-06, DP-07 | Parameters and reference data as the source of a business value | TC-PLT-N010-CON-02 |
| DP-03 | The decision record written by the caller through the library, in the caller's schema | TC-PLT-N010-CON-02, TC-PLT-N010-CON-04 |
| Template and Rules §R5.7 and §R8.2 | A contract story is Day 1; a published version is never edited and a breaking change is a new version | TC-PLT-N010-CON-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-N010-APP | App development | C: implements the eight templates and the codec server against this contract and its fakes |
| RWB-PLT-E1070-CON, RWB-PLT-E1071-CON | Contract | C: the namespace, the codec server and the payload codec this contract's protocol document describes |
| RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | C: the decision-record library, the Drools kit and the parameters and reference data the interfaces require |
| RWB-PLT-E2038-APP | App development | X: the break-glass decode authorisation and the platform audit that sit in front of the decode operation |
| The service stories of waves 1 to 4 | App development | C: the consumers that pin the version and implement the activity interfaces this contract declares |

### 19. Out of scope

- The implementation of the eight templates and of the codec server: RWB-PLT-N010-APP.
- The Temporal cluster, the namespaces, the certificates and the UI: RWB-PLT-E1070-CON and RWB-PLT-E1070-APP.
- The payload codec registration in the client and the worker: RWB-PLT-E1071-CON and RWB-PLT-E1071-APP.
- The break-glass decode authorisation and the audit of an administrative action: RWB-PLT-E2038-APP.
- The decision-record library, the central ledger and the Drools kit: RWB-PLT-E1027-CON and RWB-PLT-E1072-CON.
- The activity implementations of the 19 services: the service stories of waves 1 to 4.
- Business rules, thresholds, DoA bands, SLA values and queue codes: they stay with the caller as parameters, and no such value is fixed here.
