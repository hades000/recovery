# RWB-PLT-NF02-APP Shared library baseline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-NF02-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | NF |
| Release | None (new story) |
| Legacy key | NF-02 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-LIB-B |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform story for the shared library baseline, moved from legacy NF-02 with no impact on business behaviour; the baseline is published once as versioned artefacts and the service template pins one version. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member building one of the 19 Recovery services (RW-TRIBE)**, I want **the shared library baseline — logging and tracing, authentication and authorisation, RBAC, error handling and configuration — published to the package registry with versioning and usage examples**, so that **every service starts from the same tested libraries and no team rebuilds them**.

This is the app story of legacy key NF-02 under epic RWB-PLT-LIB. The behaviour of the legacy key is moved with no impact: no business behaviour changes, and no service, schema, topic, queue, schedule or screen is created by this story. What the story delivers is the baseline itself. The libraries are the ones every one of the 19 services builds from — every service comes from the service template and the shared libraries (Architecture v5 slide 20) — so the baseline is published once as versioned artefacts and the service template pins one version of the set.

The story covers:

- The five areas of the baseline, as the legacy description lists them: logging and tracing, authentication and authorisation, RBAC, error handling, and configuration.
- The published artefacts of each area: the package, its source, its software bill of materials and checksum, its changelog and a usage example a squad can copy.
- The pin: one version of the baseline held by the service template, and a build that fails when a service resolves to a different version.
- The behaviour the helpers fix: one trace context carried across REST, Kafka and Temporal; a token validated and a scope and delegation check asked of the access owner; a problem detail written in one shape; a configuration read from the environment and the secret store and never from code.
- The negative proof: the baseline holds no business value, writes no table, publishes no event, starts no workflow and carries no personal data in a log or a trace.

The baseline is shared platform: it is not one of the 19 services and it has no service short name, so it owns no schema, no topic, no task queue and no REST base of its own. The registry coordinates, the module list and the baseline version are Not specified in the source documents (GAP-1417; ASM-2478); section 13 carries the assumption in force until the platform review.

### 2. Business rationale

The legacy description of NF-02 is one sentence: share the common libraries — logging and tracing, authentication and authorisation, RBAC, error handling and configuration — publish them to the package registry with versioning and usage examples. It is a delivery statement, not a business rule, and the realignment keeps it that way: nothing a customer or an officer sees changes because of this story.

What changes is the cost and the risk of the split. One monolith had one logging configuration, one access guard, one error shape and one configuration loader. Nineteen services, each with its own repository, its own pipeline and its own squad, will each write those four things again unless something prevents it — and nineteen slightly different implementations of a trace header, an error body or an authorisation check is exactly how a microservice estate drifts away from the standards it claims to follow. The architecture's answer is the one already stated for the target: every service comes from the service template and the shared libraries (Architecture v5 slide 20). This story makes that sentence true for the non-functional half of it.

The standards the baseline carries are fixed by the architecture and not by this story: one trace across REST, Kafka and Temporal (Architecture v5 slides 6, 22 and 49, W3C Trace Context); every call encrypted and identified both ways and every action authorised on role, scope and delegation inside the service (slide 35); errors as RFC 9457 problem details and an idempotency key on every command (slide 11); no personal data in events, workflow payloads or logs (slides 11 and 35). Publishing them once, versioned, with a usage example, is what lets wave 0 finish before wave 1 starts: the nine Epic 1 services then inherit the baseline instead of negotiating it nine times.

### 3. Preconditions

- Wave 0 is the platform wave: the service template, the contract libraries and the platform pieces are built once and every later epic adds only its own services (Architecture v5 slide 38).
- Every service is built from the service template and the shared libraries, with outbox, inbox, Temporal worker, codec, OpenTelemetry and contract tests as the template's fixed parts (Architecture v5 slides 20 and 38).
- The call standards the helpers implement are fixed by Architecture v5 slide 11: HTTPS/JSON with mesh mutual TLS, OpenAPI 3.1 with `/v1` in the path, Kafka with CloudEvents 1.0 in binary mode and a `traceparent` header, Temporal over gRPC with a typed activity and workflow interface, a 2 s timeout, an idempotency key on every POST and RFC 9457 problem details on every error.
- The security baseline the helpers implement is fixed by Architecture v5 slide 35: a short-lived user JWT from the edge, a workload identity on every service-to-service call, role, scope and delegation checked on every action from the access owner's data, and no personal data in events, workflow payloads or logs.
- The trace standard is fixed by Architecture v5 slides 6, 22 and 49: OpenTelemetry with W3C Trace Context, one trace across REST, Kafka and Temporal, and the `traceparent` carried on the event headers.
- The access contract that the authorisation helper calls is published by the access owner's contract story, and the object-level decision stays with the owner service (Architecture v5 slide 35, OWASP API1).
- The package registry exists as a platform capability and the service template consumes the baseline from it; the registry coordinates, the module list and the baseline version are Not specified in the source documents (GAP-1417; ASM-2478).
- No approval is required to start: the story is Draft (realignment v1) and the baseline is published against the assumptions of section 13 until the platform review.

### 4. Flow

1. The platform library team fixes the baseline scope from the legacy description: logging and tracing, authentication and authorisation, RBAC, error handling and configuration, and records the module list and the one baseline version in the release note.
2. Each module is built and tested on its own: the trace and log instrumentation, the token validation and the authorisation call, the role and scope helper, the problem detail writer, the idempotency key helper and the configuration loader.
3. Each module is published as a versioned package with its source, its software bill of materials, its checksum, its changelog entry and a usage example, in one baseline release.
4. The service template is wired to the baseline: one pinned version, and the build resolves exactly that version for every service it generates.
5. A squad generates its service from the template; the pinned version arrives with the generated build file and the squad does not choose a library version of its own.
6. A service that overrides the pin, or resolves a different version by a transitive path, fails the build with the pinned and resolved versions named in the failure message.
7. A new baseline version is published only through the same steps, and a consuming service moves by changing the pin in the template and passing the build; there is no floating range anywhere.
8. Each release carries the record that makes it auditable: the version, the artefacts, the checksums, the changelog, the usage examples and the trace, log, error and configuration behaviour the version fixes.
9. The baseline itself runs nowhere: it is a set of packages, a pin in the template and a set of examples, so it opens no connection, publishes no event and starts no workflow of its own.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | A service resolves a baseline version other than the pinned one | The build fails and names the pinned and the resolved version; nothing is deployed | MSG-PLT-NF02-01 |
| X2 | A baseline module is published without its bill of materials, its checksum, its changelog entry or a usage example | The release is refused at the registry gate and the module is not consumable | MSG-PLT-NF02-02 |
| X3 | A module is found to carry a business value, a business rule or a tenant-specific setting | The change is refused at review; the value moves to the owning service, a parameter or the configuration | MSG-PLT-NF02-03 |
| X4 | A log record or a span attribute is found to carry personal data | The helper is corrected, the record is purged under the owning service's retention and a defect is raised against the module | MSG-PLT-NF02-04 |
| X5 | The authorisation helper cannot reach the access owner's contract | The action is refused, not allowed: the helper fails closed and the failure is logged without any business data | MSG-PLT-NF02-05 |
| X6 | A configuration key is missing or holds a placeholder value at start-up | The service fails to start with the key named; no default business value is substituted | MSG-PLT-NF02-06 |
| X7 | A new version is published but a consuming service has not moved its pin | The service keeps building on its pinned version; the drift is reported to the template owner and the service is never moved by force | MSG-PLT-NF02-07 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a package set and a pin; it has no build dependency, no contract dependency and needs no service to be finished |
| Negotiable | The module split inside each area, the registry coordinates, the package names and the example set are open until the platform review |
| Valuable | Every service starts from one tested baseline instead of nineteen local copies of logging, authorisation, errors and configuration |
| Estimable | Five areas, one baseline release, one pin in the template, one example per area |
| Small | One sprint for the five areas, the release and the template wiring |
| Testable | Each criterion is a contract, component or NFR assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Shared library baseline published and pinned for the 19 services

  Background:
    Given the baseline covers logging and tracing, authentication and authorisation, RBAC, error handling and configuration
    Given the service template generates every one of the 19 services

  Scenario: AC1 The baseline set is published as versioned packages with source, bill of materials, checksum, changelog and a usage example (new, D-RCV-60)
    Given the baseline modules of the five areas
    When the baseline release is published
    Then each module is published as a versioned package under one baseline version
    Then each package carries its source, its software bill of materials, its checksum and a changelog entry
    Then each area has a usage example that a squad can copy into a generated service
    Then the release note names the module list and the version, and no package is published without all four artefacts

  Scenario: AC2 The service template consumes exactly one pinned version and the build fails on drift (new, D-RCV-60)
    Given a service generated from the service template
    When the build resolves the baseline
    Then it resolves exactly the one pinned version and no floating range is allowed anywhere in the generated build file
    Then a service that overrides the pin, directly or through a transitive path, fails the build with the pinned and the resolved version named
    Then moving to a new baseline version happens only by changing the pin in the template and passing the build

  Scenario: AC3 Logging and tracing carry one W3C trace context across REST, Kafka and Temporal and no personal data (new, D-RCV-60)
    Given a service built with the baseline logging and tracing module
    When a request arrives over REST and leads to a Kafka publish and a Temporal activity
    Then one W3C trace context is created on the request and propagated to the event headers and to the workflow and activity context
    Then the log records and span attributes carry the trace and span identifiers, the service identifier, the operation, the status and the duration
    Then no log record and no span attribute carries a name, an email address, an account number, an amount or document content
    Then the trace is readable end to end in the platform observability stack
    Then a propagated context that fails the format check is replaced by a new one and the rejection is counted

  Scenario: AC4 The authentication and RBAC helpers validate the token and ask the access owner for scope and delegation (new, D-RCV-60)
    Given a service built with the baseline authentication and authorisation module
    When an action is attempted
    Then the user token is validated and the workload identity of the caller is checked before the action runs
    Then the helper calls the access owner's authorise contract for the role, the scope and the delegation band of that action
    Then the object-level decision itself stays with the owning service and the helper never substitutes for it
    Then an unreachable or refusing access owner makes the action fail closed
    Then no token, no role claim and no business data appear in a log, a trace or an error body

  Scenario: AC5 The error handling module provides the RFC 9457 problem detail and the idempotency key helpers (new, D-RCV-60)
    Given a service built with the baseline error handling module
    When an action fails or a command is repeated
    Then every error is written as one RFC 9457 problem detail with its type, title, status, detail and trace identifier, and no stack trace and no internal path
    Then every command POST carries an idempotency key and a repeated key returns the first result instead of a second effect
    Then the shape is identical across the 19 services because it comes from the baseline and not from a local class
```

These criteria are new and test only the baseline deliverable: no legacy acceptance criterion exists for NF-02, the story changes no business behaviour, and every standard named here comes from Architecture v5 slides 11, 20, 22, 35 and 49. The registry coordinates, the module list and the baseline version are Not specified in the source documents (GAP-1417; ASM-2478).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The baseline is versioned, published as one set and pinned by the service template; a service never chooses a version of its own and no floating range is allowed | Architecture v5 slides 20 and 38; legacy NF-02 description |
| BR2 | The baseline carries no business value and no business rule: thresholds, bands, limits, rates, dates and reference values live in the owning service, a parameter or the configuration | Architecture v5 slide 20; Template and Rules section 17 guardrails |
| BR3 | No personal data in a log record, a span attribute, a metric label or an event: identifiers, codes, status and duration only | Architecture v5 slides 11 and 35 |
| BR4 | One trace context across REST, Kafka and Temporal, in the W3C format, carried on the event headers and on the workflow and activity context | Architecture v5 slides 6, 22 and 49 |
| BR5 | Authorisation is object-level and belongs to the owning service; the baseline helper validates the token and asks the access owner for role, scope and delegation, and fails closed | Architecture v5 slide 35, OWASP API1 |
| BR6 | Every error is one RFC 9457 problem detail with the trace identifier, and every command carries an idempotency key | Architecture v5 slide 11 |
| BR7 | Configuration is read from the environment and the secret store, never from code and never with a business default substituted for a missing key | Architecture v5 slides 11 and 35 |
| BR8 | NF-02 is a Moved (no impact) key: the baseline changes no business behaviour, and no service, schema, topic, queue, schedule or screen is created by this story | Change Register v1, NF-02 row; Template and Rules section R6 |

### 9. State transitions

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Baseline release | DRAFT | The five areas pass their module tests and the four artefacts exist for every package | PUBLISHED | The version is consumable and the template may pin it |
| Baseline release | PUBLISHED | A later baseline version is published | SUPERSEDED | The old version stays consumable so a service that has not moved still builds |
| Baseline release | SUPERSEDED | The retention of the old version ends and no service pins it | RETIRED | The version is removed from the registry and the drift report confirms no consumer is left |
| Consumer pin (in the template) | UNPINNED | The template pins one baseline version | PINNED | Every generated service resolves that version |
| Consumer pin | PINNED | The resolved version differs from the pinned version | DRIFTED | The build fails and names both versions; the service is never moved by force |
| Consumer pin | DRIFTED | The pin is restored or the pin is moved on purpose with the build passing | PINNED | The build is green again |
| Authorisation decision | UNCHECKED | The helper validates the token and the access owner answers | ALLOWED or REFUSED | The action runs or is refused; the decision is not cached beyond the access owner's own policy version |
| Authorisation decision | UNCHECKED | The access owner is unreachable | REFUSED | The action fails closed and the failure is logged without business data |

A published version is never withdrawn while a service still pins it; a retired version is only retired after the drift report shows no consumer. The pin belongs to the template and not to a service, so a service cannot sit in DRIFTED without a build failure.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The platform library team (any team, per U3) | Builds, tests and publishes the baseline, and owns its versioning and its changelog |
| The service template owner | Pins the baseline version in the template and moves the pin, with the build as the gate |
| The consuming squads of the 19 services | Generate their service from the template, use the usage examples and raise a change request against the baseline instead of a local override |
| The access owner (rwb-access) | Owns role, scope, masking and delegation data and the authorise contract the helper calls; the baseline only calls it |
| The security architecture reviewer | Confirms that the trace, log, authorisation and error behaviour of a baseline version meets the architecture standards |
| The ACE Common team | Owns sign-in, the user token and the audit and personal-data log path the helpers use |
| No delegation of authority decision is made in the baseline | A delegation band is the access owner's data and the owning service's decision, never a value in a shared library |

No personal name, no email address and no credential appears in the baseline, in its usage examples, in a test or in a log. A user, a workload and a service are identifiers and role or scope codes only.

### 11. Data

| Item | Value |
|---|---|
| Package metadata | Package name, baseline version, module name, checksum, software bill of materials reference, changelog entry and usage example path |
| Release note | The module list of the five areas, the version, the artefact list and the behaviour the version fixes; no business value |
| Log record shape fixed by the helper | Trace identifier, span identifier, service identifier, operation, status, duration, message code. Nothing else |
| Span attributes fixed by the helper | The same identifiers and the call type; identifiers and codes only |
| Business data | None. The baseline stores, caches and logs no customer, account, case, document, notice, payment, legal-action or decision value |
| Personal data | None, in any record the helpers write: no name, no email address, no account number, no amount, no document content |
| Configuration keys read by the helper | The key names, their source (environment or secret store) and their shape; the values belong to the environment, not to the package |
| Tables owned | None. The baseline owns no schema and no table |
| Data at rest | None. The baseline runs nowhere; it is a package set, a pin and a set of examples |

### 12. Contract

**12.1 REST operations provided**

None. The baseline provides no REST operation and publishes no API document: it is a package set. The operations that the 19 services publish with it are theirs and are defined in each service's own contract story.

**12.2 REST operations consumed**

None at runtime. The authorisation helper calls the access owner's published authorise operation from inside the consuming service, so that call is the consuming service's contract dependency and not this story's; this story defines only how the helper makes it (token validated, workload identity attached, 2 s timeout, fail closed).

**12.3 Events published**

None. The baseline has no topic and publishes no event; the trace context it propagates travels on the headers of the events the consuming services publish.

**12.4 Events consumed**

None. The baseline consumes no event of its own; it supplies the instrumentation with which a consuming service consumes its own events.

**12.5 Workflows and activities**

None. The baseline starts no Temporal workflow and polls no task queue; it supplies the interceptor that carries one trace context into the workflow and activity context of the workflows a consuming service runs.

**12.6 Schedules**

None. The baseline owns no Schedule.

**12.7 Tables owned**

None. The baseline owns no `rwb_*` schema and no table, and it defines no outbox, inbox or idempotency table — those are library objects created in each service's own schema by that service's database story.

**12.8 Contract fakes**

| Fake | Serves | Used by |
|---|---|---|
| Access owner contract fake | The authorise operation the helper calls | The scope and delegation component test, including the refusal, the unreachable and the malformed answer variants |
| Edge route contract fake | The problem detail shape of a refused or failed request | The error handling contract test |
| Event schema registry fake | The event headers of a published event, including the trace context header | The Kafka trace propagation test |
| Temporal test environment | A workflow and an activity context | The Temporal trace propagation test |
| Registry gate stub | The release gate that refuses a package without its bill of materials, checksum, changelog entry or usage example | The publishing contract test |

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The baseline has no runtime surface of its own: it supplies the interceptor and the problem detail writer that the consuming service uses on its own operations |
| Kafka | 0 | 0 | No topic and no consumer group of its own; it supplies the header propagation that the consuming service uses on its own topic |
| Temporal | 0 | 0 | No task queue of its own; it supplies the interceptor for the context of the workflows a consuming service runs |
| File | 0 | 0 | No file is read or written by the baseline |

The baseline creates no service, no schema, no topic, no queue, no schedule and no screen: it is a versioned package set, a pin in the service template and a set of usage examples (ASM-2480).

### 13. Solution plan

**Deliverables.** One baseline release of versioned packages for the 19 services, covering logging and tracing, authentication and authorisation, RBAC, error handling and configuration; the service-template wiring that pins exactly one version; and a usage example for each area that a generated service can copy. The release note names the module list and the version.

**Module split (illustrative, fixed at the platform review).** The five areas are published as separately versionable modules under one baseline version, so a defect in one area can be corrected without moving the whole pin:

| Area | What the module fixes |
|---|---|
| Logging and tracing | The structured log record shape, the OpenTelemetry instrumentation for REST, Kafka and Temporal, the W3C trace context propagation, and the redaction rule that keeps personal data out of records and attributes |
| Authentication and authorisation | Token validation for the user token and the workload identity, and the authorise call to the access owner with the 2 s timeout and the fail-closed rule |
| RBAC | The role, scope and delegation helper that reads the access owner's answer and exposes it to the consuming service's own check, without deciding the object itself |
| Error handling | The RFC 9457 problem detail writer with the trace identifier, the error map, and the idempotency key helper for commands |
| Configuration | The configuration loader over the environment and the secret store, with the startup failure on a missing key and no business default |

**Pattern application.** None. The decoupling patterns of Template and Rules section R5.5 are applied by the consuming stories — the trace, error and authorisation helpers are the shared mechanism they build against — so this story adds no pattern row and no dependency of its own.

**Build steps**

1. Fix the scope from the legacy description and record the module list and the one baseline version in the release note: logging and tracing, authentication and authorisation, RBAC, error handling and configuration.
2. Build each module with its unit tests, including the redaction test that fails on personal data in a record or an attribute, and the fail-closed test of the authorisation helper.
3. Publish the set as one versioned release: package, source, software bill of materials, checksum, changelog entry and usage example per module, all four artefacts present or the registry gate refuses the release.
4. Wire the service template to the release: one pinned version, the generated build file carrying it, and a drift check that fails the build when the resolved version differs.
5. Prove the trace propagation with the instrumentation test rig: one request, one Kafka event and one Temporal activity share one W3C trace context, and the context survives a malformed header.
6. Prove the authorisation behaviour against the access owner's fake: the scope and delegation answers, the refusal, the unreachable case and the malformed answer, with no token and no business data in a log or a span.
7. Publish the five usage examples and confirm that a service generated from the template builds green against the pin without any local copy of a helper.
8. Record the release in the changelog with the version, the artefacts and the standards it fixes, and hand the pin to the template owner.

**Assumptions in force.** The registry coordinates, the module list and the baseline version are Not specified in the source documents (GAP-1417; ASM-2478). Until the platform review, the read in force is that the platform registry publishes the baseline as one versioned set, that the set covers the five areas the legacy description lists, and that the service template pins one version of that set (ASM-2478; ASM-2479). A different registry or a different module split changes coordinates and file paths, not the criteria of section 7.

**Done when.** The baseline release exists with all four artefacts per module, the template resolves exactly one pinned version and fails on drift, one trace context is proven across REST, Kafka and Temporal with no personal data in any record, the authorisation helper asks the access owner and fails closed, the problem detail and idempotency key helpers are in use, and a service generated from the template builds green against the pin.

### 14. Validation and messages

The baseline provides no runtime operation, so these are the pipeline and library messages a squad meets when it consumes the baseline. The published text of each is Not specified in the source documents (GAP-1417; ASM-2478); the identifier and the behaviour are what this story fixes.

| ID | When | Message | Result |
|---|---|---|---|
| MSG-PLT-NF02-01 | A service resolves a baseline version other than the pinned one | Names the pinned version and the resolved version and the path that resolved it | Build fails, nothing is deployed |
| MSG-PLT-NF02-02 | A baseline module is published without its bill of materials, checksum, changelog entry or usage example | Names the module and the missing artefact | Release refused at the registry gate |
| MSG-PLT-NF02-03 | A module is found to carry a business value or a business rule | Names the module and the value, without repeating the value in the log | Change refused at review |
| MSG-PLT-NF02-04 | A record or an attribute is found to carry personal data | Names the module, the field and the rule that failed; the value itself is never printed | Test fails, defect raised |
| MSG-PLT-NF02-05 | The access owner is unreachable or answers outside its contract | Problem detail with the trace identifier and the operation, with no token and no business data | Action refused, fail closed |
| MSG-PLT-NF02-06 | A configuration key is missing or holds a placeholder at start-up | Names the key and its source | Service fails to start |
| MSG-PLT-NF02-07 | A published version is not adopted by a consuming service | Names the service, its pinned version and the published version | Drift report to the template owner |

Every runtime error a consuming service writes through the baseline is an RFC 9457 problem detail carrying the trace identifier, with no stack trace and no internal path.

### 15. Screens and states

None. The baseline has no screen, no state and no route of its own; it is a package set, a pin and a set of examples. What it fixes for the screens of the 19 services is only the shape of what a screen receives when something fails — one problem detail with the trace identifier — and the rule that no screen error reveals a token, an internal path or a personal value.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-NF02-APP-01 | AC1 | Contract | A release of the five areas: each module published under one version with source, bill of materials, checksum, changelog entry and usage example; the registry gate refuses a package that lacks one of the four; the release note names the module list and the version |
| TC-PLT-NF02-APP-02 | AC2 | Contract | A service generated from the template: exactly one pinned version resolved; an override and a transitive upgrade both fail the build with both versions named; the pin moved on purpose passes |
| TC-PLT-NF02-APP-03 | AC3 | Component | One request leading to one Kafka event and one Temporal activity: one W3C trace context on all three; a malformed inbound header replaced and counted; the redaction test fails on a name, an email address, an account number, an amount and document content in a record or an attribute |
| TC-PLT-NF02-APP-04 | AC4 | Component | The access owner fake: allowed, refused, unreachable and malformed answers; the scope and delegation band read from the answer; fail closed on the last two; no token, no role claim and no business data in a log, a span or an error body |
| TC-PLT-NF02-APP-05 | AC5 | NFR | Repeated commands under load: every error is one RFC 9457 problem detail with the trace identifier and no stack trace; a repeated idempotency key returns the first result with no second effect; the shape is identical across the template-generated services |

No test in this story is an integration copy: the baseline is exercised against fakes and a test environment, never against a live service, and no `-ITG` variant belongs to it.

### 17. Guardrails

- No business values in code: thresholds, bands, limits, rates, dates and rule versions live in the owning service, a parameter or the configuration, never in a shared library.
- No personal data in a log record, a span attribute, a metric label, an event or a workflow payload: identifiers, codes, status and duration only.
- ACE data only through the owner's contract or a `v_ace_*` view read by the source-data service; the baseline reads no database at all.
- One trace context across REST, Kafka and Temporal, in the W3C format, and the trace identifier on every problem detail.
- Object-level authorisation stays with the owning service; the helper validates the token, asks the access owner and fails closed.
- Configuration is read from the environment and the secret store; no credential, key or token is committed to a package, an example or a test.
- Every published package carries its software bill of materials and checksum, so a build can prove what it consumed.
- The baseline creates no service, schema, topic, queue, schedule or screen, and it changes no business behaviour (Moved, no impact).

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| NF-02 legacy trace | Shared library baseline | Legacy NF-02 (no requirement ID) | TC-PLT-NF02-APP-01 ... -05 |

No requirement identifier exists for NF-02: the legacy key is a delivery task with no requirement row of its own, and the standards it carries are the architecture standards named in section 8. The row above is the trace for the key itself.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-N004-OPS | DevOps | Service pipeline template and Helm chart: pins exactly one baseline version and carries the drift check |
| RWB-PLT-NF01-OPS | DevOps | Repository and pipeline baseline: the repositories and pipelines that consume the pin |
| RWB-PLT-NF04-OPS | DevOps | Secrets and configuration baseline: the environment and secret store the configuration module reads |
| RWB-PLT-N005-OPS | DevOps | Platform dashboards and alerts baseline: reads the traces and metrics the logging and tracing module emits |
| RWB-PLT-E1047-APP, RWB-PLT-E1047-CON | App development, Contract | The feature flag library in the same epic, published beside this baseline and composed by the same template |
| RWB-PLT-E1072-APP, RWB-PLT-E1072-CON | App development, Contract | The Drools runtime and rule package library in the same epic, published beside this baseline |
| RWB-PLT-TE006-APP, RWB-PLT-TE006-CON | App development, Contract | The outbox and retry library in the same epic, which uses the idempotency key and trace helpers of this baseline |
| RWB-PLT-N001-CON | Contract | The route contract whose problem detail shape the error handling module writes |
| RWB-P4-E1037-CON | Contract | The authorise contract of the access owner that the RBAC helper calls |
| The 19 services (rwb-source-data, rwb-integration, rwb-case, rwb-access, rwb-document, rwb-comms, rwb-decision, rwb-payment, rwb-reporting, rwb-agent, rwb-valuation, rwb-treatment, rwb-guarantee, rwb-litigation, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-deviation, rwb-partner) | All work types | Consumers: each is generated from the template with the pinned baseline and inherits logging and tracing, authentication and authorisation, RBAC, error handling and configuration from it |

### 19. Out of scope

- The service template itself, its structure, its generated build file and its pipeline: RWB-PLT-N004-OPS and RWB-PLT-NF01-OPS.
- The environment, the secret store and the configuration values of each environment: RWB-PLT-NF04-OPS.
- The dashboards, alerts and SLOs that read the traces and metrics the baseline emits: RWB-PLT-N005-OPS.
- The feature flag library, the Drools runtime and rule package library and the outbox and retry library: RWB-PLT-E1047-APP, RWB-PLT-E1047-CON, RWB-PLT-E1072-APP, RWB-PLT-E1072-CON, RWB-PLT-TE006-APP and RWB-PLT-TE006-CON.
- The database schemas and logins, the outbox, inbox and idempotency tables in each service schema: the database and migration stories.
- The role, scope, masking and delegation data and the authorise decision: the access owner (rwb-access) and the owning services.
- Sign-in, multi-factor authentication and the audit and personal-data log path: ACE Common owns them.
- The API documents, events, topics, workflows and screens of the 19 services: each service's own contract and app stories.
- Any business rule, threshold, band, limit, rate, date or reference value: the owning service, a parameter or the configuration.
