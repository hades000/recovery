# RWB-PLT-N010-APP Workflow kit templates and codec server

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N010-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-PLT-WF-B |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-PLT-N010-APP-16) |
| Depends on (build) | RWB-PLT-N010-CON, contract published (DOR-RWB-PLT-N010-APP-21) |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: new platform story for the L3 workflow kit templates and the payload codec server of RWB-PLT-WF, with no legacy story behind it. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (9 resolved, 5 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform engineer**, I want **the eight generic templates of the Temporal L3 workflow kit published as one semantic-versioned library, and a payload codec server that answers POST /decode and POST /encode with AES-GCM keys held in Azure Key Vault and the key version read from the payload metadata**, so that **every Recovery service in waves 1 to 4, and any later workbench on the same cluster, composes approval, notification, document intake, agent run, human task, saga, scheduled job and partner instruction from one reused library, with no business term in an interface and no clear personal data in a workflow history**.

This is new platform key N010 under epic RWB-PLT-WF, and it is the L3 library and the codec server of the five-layer Temporal model of Architecture v5 slide 23 and Temporal and Drools design slide 12. It builds, and nothing else:

- The kit library: Approval (maker-checker, the DoA lookup passed as a parameter), Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job and Partner instruction, as one artefact with one semantic version.
- The interface discipline of the kit: no business term in any template interface, and every business value — a threshold, a DoA band, an SLA duration, a queue code — arriving as a typed parameter of the template input.
- The codec server runtime: decode and encode with AES-GCM, keys in Key Vault, the key version taken from the payload metadata, every enabled version still decodable, a payload without codec metadata refused whole, and no payload or clear personal data in any log.
- The activity boundary: every call to an owner service is one activity on the caller's task queue through the owner's published interface, never REST from workflow code, never a second hop.
- The reuse rules that make the library usable by ACE and by the next workbench: workers pinned by Worker Versioning, `getVersion` for an in-place change, Continue-As-New at stage ends and at least every 28 days, and the codec on every client and every worker.

The workflow platform is shared platform and not one of the 19 services: Template and Rules §R4 has 19 service rows and no platform row, so the platform owns no `rwb_*` schema, no topic, no REST base of its own and no service task queue. What the sources do state is used as it stands: the Temporal namespace rwb-recovery (Architecture v5 slides 8, 9 and 24), the platform task queue `rwb-platform` (Ownership Map JOB-22 and Architecture v5 slide 44), the PLT-owned admin operation POST /admin/workflows/smoke (Ownership Map, delivered by RWB-PLT-E1071-APP), and no data of its own. The rest of the platform identity, the kit version label and the codec key names are Not specified in the source documents (GAP-1439; ASM-2534).

### 2. Business rationale

The monolith had one scheduler table, one payload handling on every path and one approval routine rewritten per screen, so a change of an SLA value or a DoA band was a code change and every team made its own choice of timer, retry and encryption. The target splits Recovery into 19 services and adds a workflow platform shared with ACE (ADR-016, DP-10). If each service writes its own approval, its own SLA timer and its own encryption, the split multiplies the variance by nineteen.

The kit removes that variance once. One Approval template makes the maker-checker rule and the write-the-record-before-it-takes-effect rule (REQ-DRI-005) the same in every service; one Human task template owns the SLA timers every officer task needs; one Saga runner owns the undo-before-the-pivot and retry-after-the-pivot discipline of the long deals of S2, S5, S6 and S7, including the strict wait for the central ledger at a point of no return; one Scheduled job template replaces the Quartz job of every service with one Temporal Schedule per workflow, overlap policy SKIP and a per-business-date idempotency key (Architecture v5 slide 44, ADR-016).

The codec server is the other half of the same decision. The payload codec protects history at rest, but the Temporal Web UI can only show a payload through a codec server, so without one the encryption is a display setting and every history an operator can open becomes clear personal data. One server, AES-GCM, keys in Key Vault, the key version in the metadata and every version still decodable is what makes NFR-045 defensible after the split. The reuse test is the measure of the story: the next workbench takes a namespace, adds the kit and writes only its own domain workflows (Architecture v5 slide 23), which holds only if the library carries no business term.

### 3. Preconditions

- The Temporal cluster, the namespaces and the certificates are fixed by RWB-PLT-E1070-CON: one cluster per environment on ACE AKS, own persistence database, UI, metrics and codec server, version 1.30 or later for Nexus and Worker Versioning, namespace rwb-recovery (Architecture v5 slides 23 and 24).
- The worker, the SDK, the starter and the payload codec are fixed by RWB-PLT-E1071-CON: the worker polls the platform task queue `rwb-platform`, the payload codec registers as the data converter on the client and the worker, and the codec key version is written into the payload metadata.
- The contract version this story builds against is Not specified in the source documents (DOR-RWB-PLT-N010-APP-23) until RWB-PLT-N010-CON publishes its version.
- The decision-record library and its topic are fixed by RWB-PLT-E1027-CON: the record, the state change and the outbox row are one transaction in the caller's schema, and the central ledger is confirmed separately (DP-03).
- The parameters contract is fixed by RWB-PLT-E1042-CON and the reference-data contract by RWB-PLT-E1043-CON: an SLA duration, a threshold and a queue code are read as parameters or reference rows and never compiled into the kit (DP-06, DP-07).
- The Drools kit is fixed by RWB-PLT-E1072-CON: a rule answer carries the rule identifier and the package version, and a rule call happens only inside an activity (DP-04).
- The per-service Flyway sequence is fixed by RWB-PLT-E1044-CON: the kit writes no table of its own, and every row it causes is written by the caller's activity in the caller's schema (DP-15).
- The gateway-bff route contract is fixed by RWB-PLT-N001-CON: the codec server is not published through the edge and the platform offers no staff screen through gateway-bff.
- The namespace, the platform task queue and the codec key are as stated in the assumption row of this story: namespace rwb-recovery, task queue `rwb-platform`, workload identity SY-CASEWF, one AES-GCM codec key per environment in Key Vault.

### 4. Flow

1. Pin the version: read the kit interface of RWB-PLT-N010-CON, fix the semantic version of this release and record it in the manifest with the eight template identifiers and their input and output models.
2. Build the Approval template: maker-checker on two different actors, the DoA lookup injected as a parameter, the decision record written through the RWB-PLT-E1027-CON library before the outcome takes effect, and the approve, return and refuse signals.
3. Build the Human task template: one task subject, one queue code, one SLA duration and one escalation target, all parameters; the SLA timer starts with the task, pauses on the caller's pause signal and resumes from the remaining duration; escalation fires once and the task keeps its history.
4. Build the Saga runner template: an ordered step list, a compensating action declared per step before the pivot, retry until done after the pivot, and, in strict mode, a wait for the central ledger confirmation before the pivot step executes.
5. Build the Scheduled job template: one Temporal Schedule, one workflow type, cron from the caller, overlap policy SKIP, a catch-up window, and an idempotency key derived from the business date so a rerun of the same date has no second effect (DP-10, ADR-016).
6. Build the four instruction templates — Notify, Document intake, Agent run with rule fallback, Partner instruction: each calls the owner service only through one activity of the owner's published interface, one hop, and the agent template adds the 60 s timer after which the rule answer is used.
7. Build the codec server: the decode and encode endpoints of the Temporal codec server protocol, PayloadGuard for the metadata and size checks, CodecKeyResolver for the Key Vault key version, and the log rule that keeps every payload and every clear value out of the log.
8. Publish the library and the server image: tag the version, run the replay gate over recorded histories, register the server behind the platform internal ingress, and hand the pinned version to every wave 1 story that composes a template.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A template interface names a business term, a schema, a topic, a service short or a queue code as a field name | The publication step fails; the template is renamed or the value is made a parameter | MSG-PLT-N010-01 | AC1 |
| X2 | An approval request names the maker as the checker, or the DoA lookup returns no band for the amount | The template waits and does not apply the outcome; the caller's activity records the refusal; no approval takes effect | MSG-PLT-N010-02 | AC2 |
| X3 | The SLA timer fires with no escalation target, or a resume arrives after the timer has already escalated | The task stays escalated, the resume is answered as a no-op, and the caller sees the escalation in the task history | MSG-PLT-N010-03 | AC3 |
| X4 | A step fails before the pivot and its compensation fails too | The compensation is retried with the standard back-off, the saga stops at that step and the incident reaches the platform team | MSG-PLT-N010-04 | AC4 |
| X5 | A Schedule fires while the previous run of the same workflow is open | The overlap policy SKIP drops the new run, one counter is raised, and the run of the next business date is unaffected | MSG-PLT-N010-05 | AC5 |
| X6 | A payload carries no codec metadata, or its metadata names a key version that is not enabled | The whole request is refused and no payload is returned; no key is guessed and no clear read is offered | MSG-PLT-N010-06 | AC7 |
| X7 | A value the story needs is named by no source (platform identity, kit version label, codec key names) | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-1439; ASM-2534) | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds the library and the server only; it calls an owner service through an activity the caller supplies, so it needs no business service to exist |
| Negotiable | The template identifiers, the parameter field names, the escalation policy details and the log fields are open until the version is frozen; the eight templates, the AES-GCM rule and the no-business-term rule are fixed |
| Valuable | Every wave 1 to 4 service composes approval, task, saga, schedule and instruction from one library instead of writing its own, and history stays encrypted end to end |
| Estimable | Eight templates, one codec server, one library manifest, one replay gate and seven acceptance criteria |
| Small | Two sprints for the eight templates and the server, with the replay gate and the negative tests |
| Testable | Each criterion is a template behaviour, a schedule property, an activity boundary or a codec refusal in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the L3 workflow kit templates and the payload codec server

  Background:
    Given the Temporal namespace rwb-recovery and the platform task queue `rwb-platform` of RWB-PLT-E1070-CON and RWB-PLT-E1071-CON
    Given the payload codec, the decision-record library and the Drools kit of RWB-PLT-E1071-CON, RWB-PLT-E1027-CON and RWB-PLT-E1072-CON

  Scenario: AC1 The eight templates are published as one versioned library with a semantic version and no business term in an interface (new, D-RCV-60)
    Given the kit library manifest of the eight templates
    When it is published as one artefact with a semantic version and a pinned worker build
    Then the library declares exactly Approval, Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job and Partner instruction
    Then no template interface, activity name, signal name or field name carries a business term, a schema name, a topic name, a service short or a queue code as an identifier
    Then every business value a template needs arrives as a typed input parameter, and a second release changes the version and never the published one

  Scenario: AC2 The Approval template is maker-checker and takes the DoA lookup as a parameter, and it writes the decision record before the approval takes effect (new, D-RCV-60)
    Given the Approval template with the DoA lookup passed as a parameter
    When an approval request is started
    Then the template refuses an approval where the checker is the maker
    Then it resolves the DoA band through the parameterised lookup and never from a compiled value
    Then it writes the decision record through the decision-record library in one transaction with the caller's change before the approval takes effect, and a failed write leaves the approval not in effect (REQ-DRI-005)

  Scenario: AC3 The Human task template starts SLA timers, pauses and resumes them, and escalates without a business value in code (new, D-RCV-60)
    Given the Human task template with an SLA duration, an escalation target and a queue code passed as parameters
    When a task is created
    Then the SLA timer starts with the task and a pause signal stops the clock and records the paused duration
    Then a resume signal restarts the clock from the remaining duration and never from the full duration
    Then the timer fires once at the due moment, the escalation reaches the escalation target, and the same build takes a different duration and a different target from another caller without a code change

  Scenario: AC4 The Saga runner compensates a completed step before the pivot and retries after it, and waits for the central ledger confirmation in strict mode (new, D-RCV-60)
    Given the Saga runner template with an ordered step list and one pivot declared
    When a step fails before the pivot
    Then each completed step is compensated in reverse order before the saga ends
    When a step fails after the pivot
    Then the step is retried with the standard back-off until it succeeds and it is not compensated
    Then in strict mode the pivot step starts only after the central ledger confirms the decision record of the last pre-pivot step

  Scenario: AC5 The Scheduled job template maps one Temporal Schedule to one workflow with overlap policy SKIP and a per-business-date idempotency key (new, D-RCV-60)
    Given the Scheduled job template registering a caller's Schedule
    When a Schedule is registered for a workflow type and a cron expression
    Then exactly one Schedule exists for that workflow and the template owns no Schedule of its own
    Then the overlap policy is SKIP and a run that fires while the previous run is open is dropped and counted
    Then every run carries an idempotency key that contains the business date, so a rerun of the same business date has no second effect (DP-10, ADR-016)
    Then the catch-up window replays a missed run of a business date and never a second run of a completed one

  Scenario: AC6 The Notify, Document intake, Agent run and Partner instruction templates call the owner service only through an activity, one hop, 2 s timeout (new, D-RCV-60)
    Given the Notify, Document intake, Agent run and Partner instruction templates
    When a template calls an owner service
    Then the call is one activity on the caller's task queue through the activity interface the owner publishes, with a 2 s start-to-close default
    Then the workflow code of the template holds no network call, no database call, no rule call and no clock read
    Then the agent template waits 60 s for the agent answer and then uses the rule answer, and the caller sees which answer was used

  Scenario: AC7 The codec server encrypts and decrypts with the key version from the metadata, refuses a payload without codec metadata whole, keeps every enabled key version decodable and writes no payload to a log (new, D-RCV-60)
    Given the codec server on the platform internal ingress with codec key versions 1, 2 and 3 enabled and version 2 current
    When a caller posts a payload to POST /decode whose metadata names version 1
    Then the server unwraps version 1 in Key Vault and returns the clear payload, and every enabled version stays decodable after a rotation
    When a payload carries no codec metadata or names a version that is not enabled
    Then the whole request is refused with no payload returned, and the refusal names the payload index and the reason
    Then no payload, no clear value and no key material appears in any log, metric or trace, and a payload above the configured size is refused before any unwrap

  Scenario: AC8 Every business rule BR1 to BR11 of section 8 is cited by a criterion and a test case, and no rule is left without a test (new, D-RCV-60)
    Given the eleven business rules BR1 to BR11 of section 8
    When the kit library and the codec server are reviewed against section 8
    Then each rule BR1 to BR11 is cited by at least one criterion of section 7 and one test case of section 16
    Then a rule that is an architecture constraint is proved by the guardrail test TC-PLT-N010-APP-08

  Scenario: AC9 The codec server answers 401, 403 and 404 for its provided operations (new, D-RCV-60)
    Given the codec server with its provided operation Not specified in the source documents (NEWAC-RWB-PLT-N010-APP-AC9)
    When a caller sends a request to a provided operation without valid credentials
    Then the server answers 401 and decodes nothing
    When a caller sends a request to a provided operation without the right to decode
    Then the server answers 403 and decodes nothing
    When a caller asks for a path that is not a provided operation
    Then the server answers 404
```

These criteria are new and test only the kit library and the codec server: this key has no legacy story, no legacy acceptance criterion and no legacy test case, and every value quoted comes from Architecture v5, the Temporal and Drools design or the Ownership Map.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The kit is one versioned library of eight generic templates with no business terms in L1 to L3 interfaces; the platform team owns it and ACE can use it too | Architecture v5 slide 23; Temporal and Drools design slide 12 |
| BR2 | Every business value is a parameter: a threshold, a DoA band, an SLA duration and a queue code are read at start and never compiled | DP-06, DP-07; Architecture v5 slide 23 |
| BR3 | Approval is maker-checker and the DoA lookup is a parameter; the decision record is written before the outcome takes effect, in one transaction with the caller's change | REQ-DRI-005; DP-03; Temporal and Drools design slide 14 |
| BR4 | All I/O sits in activities; workflow code stays deterministic with no network, no database, no rule call and no clock read, and Continue-As-New runs at each stage end and at least every 28 days | Temporal and Drools design slides 13 and 27 |
| BR5 | A saga compensates every completed step before the pivot and retries every step after it; in strict mode the pivot waits for the central ledger confirmation | Temporal and Drools design slide 26; Architecture v5 slide 28 |
| BR6 | One Temporal Schedule per workflow, overlap policy SKIP, a catch-up window, and a per-business-date idempotency key; no Quartz table and no shared job table | DP-10, ADR-016; Architecture v5 slide 44 |
| BR7 | A template calls an owner service through the owner's activity interface only, one hop; the default start-to-close is 2 s, and a step that must run longer declares its own timeout and a heartbeat | DP-11, ADR-020; Architecture v5 slide 11 |
| BR8 | The agent template uses the rule answer after 60 s, so a slow or unavailable agent never holds a case | R-UNI-32; Temporal and Drools design slide 28 |
| BR9 | Every payload is encrypted with AES-GCM and a Key Vault key, the key version is recorded in the payload metadata, and every enabled version stays decodable | Architecture v5 slides 11 and 24; Temporal and Drools design slide 27 |
| BR10 | A payload without codec metadata is refused whole, no key version is guessed and no clear fallback exists; no payload, clear value or key material reaches a log, metric or trace | RWB-PLT-E1071-CON; Temporal and Drools design slide 27 |
| BR11 | A template never writes a business table: every state change, decision record and outbox row is written by the caller's activity in the caller's schema | DP-01, DP-03; Architecture v5 slide 20 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Template written | The eight templates exist in the working tree | In review |
| In review | Interface review closes | No business term, no schema, no topic and no service short appears in an interface | Versioned |
| Versioned | Semantic version published | The manifest carries the version, the eight template identifiers and the pinned worker build | Published |
| Published | Caller pins the version | A service declares the version in its worker build | In use |
| In use | Additive change | A parameter is added with a default and the version rises a minor number | Published |
| In use | Breaking change | A field, a signal or a template identifier changes and the version rises a major number | Superseded |
| Superseded | Every pinned worker upgrades | No worker build pins the old version and the replay gate is green | Retired |
| Published | Key rotation | A new codec key version is enabled and the old versions stay enabled and decodable | Published |

A template is stateless between runs and holds no record of its own, so the table above is the lifecycle of the library version; the runtime states of a run belong to Temporal.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The platform team (owner by default ruling) | Owns the library, the codec server, the version and the key rule; publishes and retires a version |
| Any team, per U3 | May pick this story up; the suggested owner is a suggestion and not a commitment |
| The security administration role RW-SECADM | Confirms the key rule and the log rule; the break-glass decode path itself is RWB-PLT-E2038-APP |
| SCB IT infrastructure | Owns the Key Vault instance, the key lifecycle and the key rotation rehearsal |
| The service teams of waves 1 to 4 | Compose the templates, pin the version and raise a change request; they never fork a template into their own service |

No personal name, no email address and no credential appears in this story or in an example. Where a caller must be named, the story uses a role code or a user identifier only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data held by the kit | None. A template carries the identifiers, codes and times it is given and writes no row of its own | Not specified in the source documents (DOR-RWB-PLT-N010-APP-7) |
| Business data held by the codec server | None. It holds ciphertext in transit, the key version read from the payload metadata, and no clear value after the response | Not specified in the source documents (DOR-RWB-PLT-N010-APP-7) |
| Where a change is written | In the caller's schema, by the caller's activity, in one transaction with the decision record and the outbox row (DP-03) | Not specified in the source documents (DOR-RWB-PLT-N010-APP-7) |
| Key material | An AES-GCM key in Azure Key Vault, one per environment, unwrap only for the platform workload identity SY-CASEWF; never in a values file, a test or a log | Not specified in the source documents (DOR-RWB-PLT-N010-APP-7) |
| Payload metadata | The codec name and the key version, beside the encrypted payload; it names no person and no account | Not specified in the source documents (DOR-RWB-PLT-N010-APP-7) |
| Logs, metrics and traces | The workflow identifier, the run identifier, the template identifier, the version, the operation and the duration; no payload, no clear value and no key | Not specified in the source documents (DOR-RWB-PLT-N010-APP-7) |
| Search attributes | Set by the caller, not by the kit: CaseId, Stage, ProductGroup and QueueCode are the only attributes a run carries | Not specified in the source documents (DOR-RWB-PLT-N010-APP-7) |
| Retention | Fixed by the cluster and the namespace of RWB-PLT-E1070-CON; this story adds no store and no retention rule of its own | Not specified in the source documents (DOR-RWB-PLT-N010-APP-7) |

### 12. Contract

#### 12.1 REST operations provided

| Operation | Protocol | Request | Response | Behaviour | Owner |
|---|---|---|---|---|---|
| POST /decode | Temporal codec server protocol | Namespace, workflow identifier, run identifier and the encoded payloads | The decoded payloads, or a refusal | Unwraps the key version named in each payload metadata, refuses the whole request when a payload carries no metadata or an unknown version, and logs the operation without a payload | PLT |
| POST /encode | Temporal codec server protocol | Namespace, workflow identifier, run identifier and the clear payloads submitted from the Web UI | The encoded payloads with the current key version in the metadata | Encrypts with the current key version of the environment, refuses a clear payload above the configured size, and logs the operation without a payload | PLT |

Both operations are served from the codec server root on the platform internal ingress, on the codec server of RWB-PLT-E1070-CON: they are not under the edge base, they are not published through gateway-bff, and they carry no service segment. The paths are the two operations of the Temporal codec server protocol and are copied as they stand.

#### 12.2 REST operations consumed

None. The kit and the codec server call no REST service: an owner service is reached through the owner's activity interface on the owner's task queue, and Key Vault is reached through the workload identity of the platform and not through a REST contract of this story.

#### 12.3 Events published

None. The platform is shared platform and has no topic of its own; the decision record that a template causes is published by the caller through RWB-PLT-E1027-CON, and the platform publishes no event schema.

#### 12.4 Events consumed

None. A template is started by the caller's API or by the caller's Schedule, and no template consumes a Kafka topic.

#### 12.5 Workflows and activities

| Template | Workflow type | Activities it calls | Timers, signals and policy | Parameters passed by the caller |
|---|---|---|---|---|
| Approval | KitApprovalWorkflow | RecordDecision through RWB-PLT-E1027-CON, then the caller's ApplyOutcome activity | Approval SLA timer; signals approve, return and refuse; maker-checker on two different actors | Approval subject identifier, DoA lookup, DoA band, SLA duration |
| Notify | KitNotifyWorkflow | The caller's Notify activity, which calls the notice owner | Dispatch retry with the standard back-off; one hop, 2 s start-to-close default | Notice template code, recipient reference, dispatch channel, correlation identifier |
| Document intake | KitDocumentIntakeWorkflow | The caller's Accept activity, which calls the document owner, then RecordDecision | Heartbeat on the long step; one hop; a declared start-to-close for the OCR step | Intake channel, document type code, retention code, correlation identifier |
| Agent run with rule fallback | KitAgentRunWorkflow | The caller's RunAgent activity, then EvaluateRules through RWB-PLT-E1072-CON | 60 s timer on the agent answer, then the rule answer; both recorded | Agent policy identifier, rule package code, fallback threshold |
| Human task with SLA timers | KitHumanTaskWorkflow | CreateTask and RecordDecision, both the caller's | SLA timer with pause and resume; escalation timer; escalation signal to the target | Task subject, queue code, SLA duration, escalation target |
| Saga runner | KitSagaRunnerWorkflow | RunStep per step, CompensateStep per completed step, ConfirmLedgerEntry in strict mode | Compensation in reverse order before the pivot; retry until done after it; strict ledger wait at the pivot | Step list, pivot index, strict flag, idempotency seed |
| Scheduled job | KitScheduledJobWorkflow | RunJob, the caller's job body | One Temporal Schedule per workflow, overlap policy SKIP, catch-up window, per-business-date idempotency key | Schedule identifier, cron, business calendar, catch-up window |
| Partner instruction | KitPartnerInstructionWorkflow | IssueInstruction, the caller's, through the partner owner's interface | Instruction SLA timer; result signal; reminder timer | Partner reference, instruction type code, SLA duration, reminder policy |

Eight template workflow types, all published in the namespace rwb-recovery and started on the caller's task queue. The platform's own queue `rwb-platform` carries the platform operations of RWB-PLT-E1071-APP and the stuck-workflow scan JOB-21, and never a caller's business step. The 2 s default of BR7 applies to a synchronous owner call; a long step declares its own start-to-close and a heartbeat.

#### 12.6 Schedules

None. The kit owns no Schedule: the Scheduled job template registers the caller's Schedules through the Temporal Schedule API, with the caller's cron, overlap policy and catch-up window, and the platform's own two Schedules stay with their own stories — JOB-21, the stuck workflow scan every 5 minutes, and JOB-22, the smoke workflow at 06:00, both owned by PLT (Ownership Map).

#### 12.7 Tables owned

None. The platform owns no `rwb_*` schema and no table: the decision record a template causes is written through the RWB-PLT-E1027-CON library into the caller's schema, in one transaction with the caller's change and the caller's outbox row.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Kit fake (RWB-PLT-N010-CON) | The eight template interfaces, the parameter models and the deterministic replay of every template | This story, the wave 1 to 4 services, another workbench |
| Codec fake (RWB-PLT-N010-CON) | POST /decode and POST /encode, including the 401, 403, 413, 422 and 503 refusals | This story, the Web UI test of RWB-PLT-E2038-APP |
| rwb-decision fake (P7) | The decision-record write and the central ledger confirmation | The Approval and Saga runner tests of this story |

The fakes of this section are published by RWB-PLT-N010-CON; this story consumes them and changes none of them.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 codec server operations, POST /decode and POST /encode, on the platform internal ingress | 0 | Temporal codec server protocol, no edge route, no service segment |
| Kafka | 0 | 0 | The platform owns no topic; the caller publishes its decision records |
| Temporal | 8 template workflow types | 0 | One namespace rwb-recovery, activities on the caller's task queue, one hop |
| File | 0 | 0 | No file crosses the kit; documents are reached through the owner's activity |

### 13. Solution plan

**Components**

| Component | Responsibility |
|---|---|
| WorkflowKitLibrary | The manifest, the semantic version, the eight template identifiers, the parameter models and the pinned worker build |
| ApprovalTemplate | Maker-checker, the parameterised DoA lookup, the record-before-effect order and the approve, return and refuse signals |
| HumanTaskTemplate | Task creation, the SLA timer with pause and resume, and one escalation |
| SagaRunnerTemplate | The ordered step list, the compensation before the pivot, the retry after it and the strict ledger wait |
| ScheduledJobTemplate | One Schedule per workflow, overlap policy SKIP, the catch-up window and the per-business-date idempotency key |
| NotifyTemplate | The notify activity boundary, the dispatch retry and the correlation identifier |
| DocumentIntakeTemplate | The intake activity boundary, the heartbeat on the long step and the declared start-to-close |
| AgentRunTemplate | The agent activity, the 60 s timer and the rule fallback that records which answer was used |
| PartnerInstructionTemplate | The instruction activity, the instruction SLA timer and the result signal |
| CodecServerController | POST /decode and POST /encode of the Temporal codec server protocol and the response mapping |
| PayloadGuard | The metadata presence check, the enabled-version check and the size limit, applied before any unwrap |
| CodecKeyResolver | The key version read from the payload metadata and the Key Vault unwrap through SY-CASEWF, with no guessed version |

**Versioning rule.** One semantic version covers the eight templates together. An additive change — a new parameter with a default, a new optional signal — raises the minor number; a change to a field, a signal or a template identifier raises the major number; a fix that changes no interface raises the patch number. A caller pins the version in its worker build and upgrades by Worker Versioning, and a published version is never edited in place.

**Key Vault key rule.** One AES-GCM key per environment in Azure Key Vault, unwrap only for the workload identity SY-CASEWF. The key version is written into the payload metadata at encryption and read from it at decryption; a new version is enabled before it becomes current, every enabled version stays enabled for the retention of the runs that used it, and a retried run reuses the recorded version. No key, key name or secret appears in a values file, a test or a log, and a rotation is rehearsed on a run written under the previous version.

**No business term rule.** No interface of L1 to L3 carries a business term, a schema name, a topic name or a service short: not in a template identifier, an activity name, a signal name, a field name or an example. The library says approval, task, instruction and step, never treatment or write-off; a business value enters only as a typed parameter or as a reference row of RWB-PLT-E1043-CON, and the caller supplies its own activity interface.

**Pattern application.** The metadata row "Patterns applied" reads None, and that is the correct reading of Template and Rules §R5.5: every DP row is keyed to a legacy marker, and N010 has no legacy story, no `recovery.<table>`, no legacy service login, no `rwb.p<n>.` or `rwb.casewf.` topic, no `/api/recovery/v1` base, no Quartz job, no V0001 migration and no screen. The kit is the platform implementation that the 19 service stories apply DP-03, DP-04, DP-06, DP-07, DP-10 and DP-15 against, so no DP dependency is added here; the four platform contracts it builds against are named in section 3.

**Build steps**

1. Write the manifest and the parameter models of the eight templates against the kit interface of RWB-PLT-N010-CON; fix the semantic version of this release.
2. Build the Approval and Human task templates first, because approval and the officer task are the two behaviours every wave 1 service needs.
3. Build the Saga runner and the Scheduled job templates, with the pivot, the compensation order, the strict ledger wait, the overlap policy and the business-date key.
4. Build the Notify, Document intake, Agent run and Partner instruction templates against the owner activity interfaces.
5. Build the codec server: the controller, PayloadGuard, CodecKeyResolver, the two operations and the six refusal codes.
6. Run the replay gate over recorded histories of a reference workflow for every template, and prove the deterministic replay of the codec metadata.
7. Publish the version to the contract registry, put the server image behind the platform internal ingress, and give every wave 1 story the pinned version.
8. Hand the version to RWB-PLT-N010-CON for the fake, and run the negative tests of section 16 before the version is declared in use.

**Done when.** The eight templates are published under one semantic version with no business term in an interface; the codec server answers both protocol operations and every refusal case; a rotation leaves every enabled version decodable; the replay gate is green; and a wave 1 service starts the Approval template against the fake without changing the library.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-PLT-N010-01 | A template interface names a business term, a schema, a topic or a service short | The interface {name} carries a term the kit does not allow. The publication stopped and the version is unchanged. |
| MSG-PLT-N010-02 | An approval names the maker as the checker, or the DoA lookup returns no band | The approval cannot proceed: the checker must differ from the maker, or the amount falls outside the delegated bands. |
| MSG-PLT-N010-03 | A pause or a resume arrives after the SLA timer has escalated | The task is already escalated. The request was recorded and did not change the task. |
| MSG-PLT-N010-04 | A step fails and its retry is exhausted, or a compensation cannot complete | The step {step} did not complete. The saga stopped at that step and the incident was raised. |
| MSG-PLT-N010-05 | A Schedule fires while the previous run is open, or a business-date key already ran | The run was skipped by the overlap policy, or the run of business date {date} already completed. |
| MSG-PLT-N010-06 | A payload carries no codec metadata, names a version that is not enabled, or exceeds the size limit | The payload could not be decoded: codec metadata is missing, the key version is not enabled, or the payload is above the size limit. No payload was returned. |
| MSG-PLT-N010-07 | The Key Vault key is not reachable | The key service did not answer. The request was refused and no payload was returned. |

The seven identifiers are platform messages of this story and not business messages: none names a customer, an account, a case or a business value, and the refusal text of a payload names the payload index and the reason only.

### 15. Screens and states

No screen in this story. The kit is a library and the codec server is a headless endpoint; the only surface a person sees is the Temporal Web UI of RWB-PLT-E1070-APP, where decode is authorised and audited by RWB-PLT-E2038-APP. The states this story exposes are the library version states of section 9 and the codec answers: decoded, refused for missing metadata, refused for an unknown version, refused for size, and refused for an unreachable key.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N010-APP-01 | AC1 | Unit | The manifest: eight template identifiers, one semantic version, a pinned build; a scan of every interface name against the business-term list; a minor and a major version raise on two sample changes |
| TC-PLT-N010-APP-02 | AC2 | Contract | The Approval template against the kit fake and the rwb-decision fake: maker-checker refusal, the parameterised DoA lookup, and a failed record write leaving the approval not in effect |
| TC-PLT-N010-APP-03 | AC3 | Component | The Human task template: start, pause, resume from the remaining duration, one escalation, and the same build under two different durations and targets |
| TC-PLT-N010-APP-04 | AC4 | Integration | The Saga runner under a Temporal test server: failure before the pivot with reverse-order compensation, failure after the pivot with retry, and the strict ledger wait |
| TC-PLT-N010-APP-05 | AC5 | Component | The Scheduled job template: one Schedule per workflow, overlap policy SKIP under a long run, the catch-up window, and a rerun of a completed business date |
| TC-PLT-N010-APP-06 | AC6 | Integration | The four instruction templates against the owner activity fakes: one hop, the 2 s default, no network in workflow code, and the agent 60 s fallback recorded |
| TC-PLT-N010-APP-07 | AC7 | NFR | The codec server: decode of a version 1 payload after a rotation to version 2, the four refusal cases, a size refusal before unwrap, and a log and trace scan that finds no payload and no key |
| TC-PLT-N010-APP-08 | AC8 | Guardrail | A trace scan of BR1 to BR11 of section 8 against sections 7 and 16 |
| TC-PLT-N010-APP-09 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-PLT-N010-APP-AC9) |

### 17. Guardrails

- No business value in code: a threshold, a DoA band, an SLA duration and a queue code arrive as parameters or reference rows, and a compiled business value fails the publication step.
- No personal data in events, workflow history, logs or prompts: every payload is encrypted, the metadata names a key version only, and a payload, a clear value or a key material never reaches a log, a metric or a trace.
- ACE data only through the owner's contract or the recovery.v_ace_* views: the kit reaches no ACE table, and it reaches no service directly — the caller's activity does, through the owner's published interface.
- No key or secret in a values file or a test: the codec key lives in Azure Key Vault, the workload identity SY-CASEWF unwraps it, and a test uses a synthetic key of the test environment only.
- No payload in a log: the codec server logs the operation, the workflow identifier, the run identifier, the payload count, the version and the outcome, and nothing else.
- One hop: a template calls an owner through one activity interface, and an activity never calls a second service.
- Workflow code stays deterministic: no network, no database, no rule call, no clock read and no random; every one of those sits in an activity.
- The published version is never edited: a breaking change raises a major version, the old version stays pinnable until the last worker upgrades, and the replay gate runs on every build.
- Every test payload is synthetic; no production payload is copied into a test, a fixture or an example.

### 18. Traceability

| Source | Element | Test cases | Feature | L3 process |
|---|---|---|---|---|
| Architecture v5 slide 23 | L3 workflow kit as a versioned library of eight templates with no business terms, owned by the platform team, reusable by ACE and by the next workbench | TC-PLT-N010-APP-01, TC-PLT-N010-APP-02 | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) |
| Architecture v5 slides 11, 20 and 24 | The activity interface as the contract, one hop, the 2 s timeout, the decision record in the caller's transaction, the namespace per workbench and the codec on every client and worker | TC-PLT-N010-APP-06, TC-PLT-N010-APP-07 | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) |
| Architecture v5 slide 44 | Schedules replace Quartz: overlap policy SKIP, the catch-up window and the jobs of the owning service | TC-PLT-N010-APP-05 | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) |
| Temporal and Drools design slide 26 | Saga: undo before the pivot, retry after it, strict mode at the point of no return | TC-PLT-N010-APP-04 | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) |
| Temporal and Drools design slides 27 and 28 | Determinism, the rule answer after 60 s, encrypted payloads and no clear personal data in history | TC-PLT-N010-APP-06, TC-PLT-N010-APP-07 | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) |
| ADR-016, DP-03, DP-10 | A reusable Temporal layer with Schedules in place of Quartz, the decision-record library and the workflow through the kit | TC-PLT-N010-APP-02, TC-PLT-N010-APP-04, TC-PLT-N010-APP-05 | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) | Not specified in the source documents (DOR-RWB-PLT-N010-APP-2) |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-N010-CON | Contract | C: the kit interface, the parameter models, the codec protocol document and the fakes this story builds against |
| RWB-PLT-E1070-CON, RWB-PLT-E1071-CON | Contract | C: the cluster, the namespace, the worker, the SDK and the payload codec the templates run on |
| RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | C: the decision-record library, the Drools kit and the parameters and reference data the templates call |
| RWB-PLT-E2038-APP | App development | X: the break-glass decode authorisation and the platform audit of the codec server; this story supplies the protocol and the refusals |
| RWB-PLT-E1071-APP | App development | X: the worker, the smoke workflow and the PLT-owned admin operation POST /admin/workflows/smoke on `rwb-platform` |

### 19. Out of scope

- The Temporal cluster, the namespaces, the certificates, the UI and the ingress: RWB-PLT-E1070-CON and RWB-PLT-E1070-APP.
- The worker, the SDK, the starter, the payload codec registration and the smoke workflow, including POST /admin/workflows/smoke: RWB-PLT-E1071-CON and RWB-PLT-E1071-APP.
- The break-glass decode authorisation, the administrative audit entries and the reconciliation of administrative actions: RWB-PLT-E2038-APP.
- The observability of the platform, its dashboards and its run books: RWB-PLT-E2037-CON and RWB-PLT-E2037-APP.
- The decision-record library itself and the central ledger: RWB-PLT-E1027-CON and the rwb-decision stories.
- The Drools kit, the rule packages and the rule governance: RWB-PLT-E1072-CON and rwb-decision.
- The domain workflows of the 19 services and the stage children of CaseWorkflow: the service stories of waves 1 to 4.
- Business rules, thresholds, DoA bands, SLA values and queue codes: they stay with the caller as parameters, and no such value is fixed here.
sion.
- The domain workflows of the 19 services and the stage children of CaseWorkflow: the service stories of waves 1 to 4.
- Business rules, thresholds, DoA bands, SLA values and queue codes: they stay with the caller as parameters, and no such value is fixed here.
