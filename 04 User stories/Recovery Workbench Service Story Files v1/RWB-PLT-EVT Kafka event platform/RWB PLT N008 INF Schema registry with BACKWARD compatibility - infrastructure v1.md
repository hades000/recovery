# RWB-PLT-N008-INF Schema registry with BACKWARD compatibility

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N008-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-EVT |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N008 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-EVT-B |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform story for RWB-PLT-EVT, legacy key N008. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the JSON Schema registry configured with one subject per event type and BACKWARD compatibility enforced at registration and in every build**, so that **the 19 services can evolve their event schemas without breaking a consumer and every published event is validated against a registered schema**.

### 2. Business rationale

Events are the cross-service contract of the Recovery workbench: a producer publishes a fact and every other service reacts to it without a call chain. The contract for a topic is the AsyncAPI 3.0 document of its producing service; the store of the schemas behind that document is the JSON Schema registry (Arch v5 slide 11). BACKWARD compatibility is the rule that lets a producer add a field while every consumer that reads the older shape keeps working, and it is the reason the 19 services may be delivered in four waves without freezing the event shapes on day one.

The topic set this registry serves is the catalogue of RWB-PLT-N002-INF, 19 service topics plus the shared decision-record topic. The event name carries the major version (`rwb.<short>.<Event>.v1`), so a consumer reads the version from the envelope and a breaking change is visible on the wire rather than buried in a payload diff (DP-14; Arch v5 slides 42 and 43).

The registry is also the build gate. A schema that is not registered, or is not backward compatible with the version in force, fails the pipeline before merge, so a contract error is found in CI and not in a production incident. The registry holds schema metadata only. It is a platform capability with no business entity, no business value and no business data, and this story therefore publishes no message and owns no table of a service.

### 3. Preconditions

- The topic catalogue of RWB-PLT-N002-INF exists: the 19 service topics `rwb.<short>.events.v1`, their retry and dead-letter topics, and the shared topic `rwb.decision-record.v1`.
- The registry product and its hosting follow the decision recorded for this story. Arch v5 slide 21 lists the schema registry among the items to confirm with the ACE platform team, so this story works against the recorded assumption and gap rather than a settled product choice: Not specified in the source documents (GAP-1397; ASM-2433).
- The build identity and the run-time identity of each service exist, so registration can be attributed to one service and audited.
- The AsyncAPI 3.0 documents of the topics exist under the ownership of the service CON stories; this story references them and never edits them.
- No build dependency: the story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Take the event catalogue and its 20 topics from RWB-PLT-N002-INF, with the producing service of each event type.
2. Choose one subject per event type, so that an event type maps to exactly one schema line rather than a topic-wide blob.
3. Set BACKWARD compatibility as the registry default for the whole catalogue, so a new subject inherits the rule without a local choice.
4. Register the current schema of every event type of the catalogue as version 1 of its subject, and record the checksum and the owning AsyncAPI document.
5. Wire the registry into the build: a schema lint job and the AsyncAPI reference check that resolves every message of every document to a registered subject.
6. Wire the registry into the producer and consumer libraries, so a payload is validated against its subject before the outbox relay publishes it and a cached schema is used at run time when the registry is not reachable.
7. Set the access policy per service: a service writes only its own subjects, every service reads the catalogue, and every registration is written to the audit trail.
8. Publish the versioning and deprecation runbook: when a new major version is required, how a minor version is deprecated, and when a subject is retired.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A new schema version breaks BACKWARD compatibility | The registration is refused and the previous version stays in force | MSG-PLT-N008-01 | AC2 |
| X2 | A produced schema has no subject in the registry | The build fails before merge and the artefact is not published | MSG-PLT-N008-02 | AC4 |
| X3 | A producer payload fails validation against its subject | The record is not published; it stays in the outbox with an alert until the payload or the schema is corrected | None | AC4 |
| X4 | A subject name does not match its event type and topic | The CI check fails and the subject is not created | MSG-PLT-N008-02 | AC1 |
| X5 | The registry is not reachable during a build or at run time | The build stops rather than guessing a schema; a running service validates against the last cached schema and raises an alert | MSG-PLT-N008-03 | AC4 |
| X6 | A schema declares a property that names a person, an address, an identity number or a contact point | The review refuses the schema and no subject version is created | MSG-PLT-N008-04 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the topic catalogue and the AsyncAPI documents of the services only |
| Negotiable | The compatibility rule, the subject-per-event-type rule and the build gate are fixed by the architecture; the product and the subject names are settled with the platform team |
| Valuable | Unblocks every producing service in every wave, because a service can add a field without a consumer break and a breaking change is caught before merge |
| Estimable | One subject list, one policy file, one build gate, one AsyncAPI check, one access policy and one runbook |
| Small | Fits one sprint for the platform team, with the catalogue import and the gate |
| Testable | Every criterion is checked against the registry, the gate output and the access decisions, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Schema registry with BACKWARD compatibility for the event catalogue

  Background:
    Given the topic catalogue of RWB-PLT-N002-INF is in force
    Given the registry applies BACKWARD compatibility to every subject

  Scenario: AC1 Every event type has one subject and one registered JSON Schema (new, D-RCV-60)
    Given the event catalogue of the Recovery services
    When the subject list of the registry is read
    Then every event type of the catalogue has exactly one subject
    Then every subject names its topic and its producing service
    Then every subject holds a JSON Schema that validates against the JSON Schema meta-schema
    Then the compatibility level of every subject is BACKWARD

  Scenario: AC2 A backward-compatible change is accepted and a breaking change is refused (new, D-RCV-60)
    Given a subject with a version in force
    When a new version only adds an optional property
    Then the registry accepts the version and the previous version stays readable
    When a new version removes a required property, renames a property, narrows a type or adds a required property
    Then the registry refuses the version with MSG-PLT-N008-01
    Then the version in force does not change

  Scenario: AC3 The event type version and the subject version agree (new, D-RCV-60)
    Given an event type published as rwb.<short>.<Event>.v1
    When the ce_type value is compared with the subject version
    Then the major version in the ce_type value equals the registered major version
    When the two do not agree
    Then the contract check fails with MSG-PLT-N008-01
    Then a breaking change is registered only under a new major version and a new event type version

  Scenario: AC4 The registry is the build gate (new, D-RCV-60)
    Given a service build in the pipeline
    When the build runs the schema gate
    Then every produced schema is validated against its subject in the registry
    Then every AsyncAPI document is checked against its subjects
    When a schema is unregistered or not backward compatible
    Then the build fails with MSG-PLT-N008-02 and the change cannot be merged

  Scenario: AC5 Access to the registry is authenticated per service (new, D-RCV-60)
    Given an authenticated service identity
    When the service registers a schema under its own subject
    Then the write is accepted and written to the audit trail
    When an anonymous caller or another service writes the subject
    Then the write is refused and audited

  Scenario: AC6 No personal data in a registered schema (new, D-RCV-60)
    Given a schema submitted for registration
    When its property names are checked
    Then no property names a person, an address, an identity number or a contact point
    Then a schema with such a property is refused with MSG-PLT-N008-04
    Then an event carries identifiers and business facts only
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One subject per event type, named `<topic>-<Event>`, so the subject of an event type is derived from its topic and its event name and never invented locally | Arch v5 slides 42 and 43 notes; ASM-2433 |
| BR2 | The compatibility level of every subject is BACKWARD: a new version may add an optional property and may not remove, rename, retype or newly require one | Arch v5 slide 11 contract row (JSON Schema registry, backward compatible) |
| BR3 | A breaking change is a new major version and a new event type version; the previous major version stays in force until its event type is retired | Arch v5 slides 42 and 43 notes; DP-14 |
| BR4 | The ce_type value carries the major version of the event type, so a consumer reads the version from the envelope | Arch v5 slide 22 (ce_type example) |
| BR5 | One AsyncAPI 3.0 document per topic is the contract, and every message of that document references a registered subject | Arch v5 slide 11 (AsyncAPI 3.0 per topic) |
| BR6 | The build validates every produced schema and every AsyncAPI document against the registry; a merge without a green gate is not possible | Arch v5 slide 11 notes; Template and Rules §R7.2 s17 |
| BR7 | Access is least privilege and audited: a service writes only its own subjects and reads the catalogue; every registration is attributed and logged | Arch v5 slide 21 (topics with their own ACLs and schema subjects) |
| BR8 | The registry holds metadata only: schema documents, versions, checksums and references. It holds no business value, no business data and no rule, which stay in the parameters, the reference data, the service tables and the rule packages | Template and Rules §R7.2 s17; Arch v5 slide 22 payload rule |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Schema submitted | The schema validates and the BACKWARD check against the version in force passes | Registered |
| Draft | Schema submitted | The compatibility check fails | Rejected |
| Rejected | Corrected schema submitted | A new version passes the compatibility check | Registered |
| Registered | Gate consumes the version | The build gate and the AsyncAPI check pass and the version is used by a release | In force |
| In force | Additive change registered | A new version passes BACKWARD and the previous version stays readable | In force (new version) |
| In force | Breaking change requested | The architecture approves a new major version | Draft (new major version) |
| In force | A newer version is in force | The consumers have moved to the newer version | Superseded |
| Superseded | Event type withdrawn | The event type leaves the catalogue and no consumer reads it | Retired |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns the registry configuration, the subject list, the gate and the runbook |
| ACE platform team | Owns the registry product, its hosting and the compatibility level of the platform |
| Service teams | Own the subjects of their own event types and publish the AsyncAPI document that references them |
| Architecture | Approves a new major version and any weakening of the compatibility level |
| Security | Approves the access policy and the audit trail of the registry |
| Data steward | Confirms that no registered schema declares a personal-data property |

The registry product, the hosting and the subject naming are Not specified in the source documents (GAP-1397; ASM-2433); this story fixes the compatibility rule, the subject-per-event-type rule and the build gate, and works against the recorded assumption for the product and the names.

### 11. Data

The registry stores schema metadata, never business data.

| Field | Content | Filled by |
|---|---|---|
| subject | The subject of one event type, derived from its topic and its event name | Registration |
| event type | The event name with its major version, as carried in ce_type | Service team |
| topic | The topic of the event type in the catalogue | Service team |
| producer | The producing service, from the Ownership Map | Service team |
| schema version | The version of the subject, with the major version of the event type | Registration |
| compatibility | The compatibility level of the subject, BACKWARD for every subject | Policy |
| checksum | The checksum of the registered schema document | Registration |
| registered at | The timestamp and the identity of the registration | Registry |
| AsyncAPI reference | The document and message pointer that references the subject | Service team |

The event types that must be registered, taken from the event catalogue (Arch v5 slides 42 and 43, including the rows marked +):

| Service | Topic | Event types |
|---|---|---|
| P3 rwb-case | `rwb.case.events.v1` | CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged, TimerBreached |
| P7 rwb-decision | `rwb.decision.events.v1` | ApprovalRequested, ApprovalDecided, RulePackageInForce |
| P4 rwb-access | `rwb.access.events.v1` | AccessPolicyChanged, DoaLimitChanged |
| S8 rwb-deviation | `rwb.deviation.events.v1` | DeviationRaised, DeviationCleared |
| P1 rwb-source-data | `rwb.source-data.events.v1` | AceDataReady, AceDataLate |
| P9 rwb-reporting | `rwb.reporting.events.v1` | ReportPublished |
| P10 rwb-agent | `rwb.agent.events.v1` | AgentRunCompleted |
| P2 rwb-integration | `rwb.integration.events.v1` | FileDelivered, FileFailed |
| P5 rwb-document | `rwb.document.events.v1` | DocumentStored, DocumentFieldsExtracted |
| P6 rwb-comms | `rwb.comms.events.v1` | NoticeGenerated, NoticeDispatched, NoticeDelivered |
| P8 rwb-payment | `rwb.payment.events.v1` | TreatmentBooked, PaymentMissed, ProceedsMatched |
| S9 rwb-partner | `rwb.partner.events.v1` | InstructionIssued, PartnerResultSubmitted |
| S1 rwb-valuation | `rwb.valuation.events.v1` | RouteDecided |
| S2 rwb-treatment | `rwb.treatment.events.v1` | TreatmentApproved, TreatmentClosed |
| S3 rwb-guarantee | `rwb.guarantee.events.v1` | GuaranteeClaimFiled, GuaranteeClaimSettled |
| S4 rwb-litigation | `rwb.litigation.events.v1` | LawsuitFiled, JudgmentRecorded, AuctionResult |
| S5 rwb-asset | `rwb.asset.events.v1` | AssetTakenOn, AssetSold |
| S6 rwb-debtsale | `rwb.debtsale.events.v1` | LotAwarded, AccountsTransferred |
| S7 rwb-writeoff | `rwb.writeoff.events.v1` | WriteOffApproved |
| Shared | `rwb.decision-record.v1` | DecisionRecorded |

The subject names, the registry product and the schema document format beyond JSON Schema are Not specified in the source documents (GAP-1397; ASM-2433); the event type list above is the registration backlog of the catalogue.

### 12. Contract

#### 12.1 REST operations provided

None. The registry answers its own product API for registration and validation. That API is a platform API, not a Recovery business contract: no service calls it inside a business flow, and no path in this story belongs to a service base.

#### 12.2 REST operations consumed

None. The story reads the topic catalogue and the AsyncAPI documents as files in the repository, not as a run-time call.

#### 12.3 Events published

None. The platform registers the schemas; the event types belong to the producing services.

#### 12.4 Events consumed

None. The registry validates schemas, it never reacts to an event.

#### 12.5 Workflows and activities

None. No Temporal workflow or activity is created by this story.

#### 12.6 Schedules

None. Registration happens on a commit or a release, not on a schedule.

#### 12.7 Tables owned

None. The registry is not an ACE DB table; it is a registry product that holds schema metadata only, and this story creates no table in any `rwb_*` schema.

#### 12.8 Contract fakes

None. The producer and consumer libraries point at a local registry instance in the test environment, so no WireMock fake is needed.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None | The registry API is a platform API for registration and validation, not a Recovery business contract |
| Kafka | None published or consumed by the platform | The registry serves the 20 event topics of the topic catalogue and validates the payloads the services publish on them |
| Temporal | None | No workflow, activity or task queue |
| File | None | No file is exchanged by the registry |

### 13. Solution plan

**Deliverables.** `registry/subjects.yaml` (one subject per event type of the catalogue, with its topic, producer and AsyncAPI reference), `registry/policy.yaml` (compatibility BACKWARD, access per service, the refused personal-data property list), `ci/schema-gate` (the registration and validation gate), the AsyncAPI validation job, the access policy in the registry, and the versioning and deprecation runbook.

**Pattern application.** None of the §R5.5 DP markers appears in this new platform story. It names no legacy table, no `recovery_svc` login, no old topic name, no in-process call, no scheduler and no screen of the monolith, so the DP table adds no row and no dependency. DP-09 (CloudEvents and outbox) is applied by the service stories against the schemas registered here: the outbox relay publishes a payload that this registry has validated, and the inbox dedupe is unchanged. DP-14 (topic naming) is applied by RWB-PLT-N002-INF and is read here only as the source of the subject names.

**Build steps**

1. Import the event catalogue into `registry/subjects.yaml`: one subject per event type, with its topic, its producer and its event type version.
2. Write `registry/policy.yaml`: BACKWARD as the default compatibility level, the per-service write scope, and the property list the personal-data check refuses.
3. Register version 1 of every event type of the catalogue, with the checksum and the AsyncAPI reference of its document.
4. Build `ci/schema-gate`: resolve the produced schema of a service to its subject, validate it, and fail on a missing subject or a failed compatibility check.
5. Add the AsyncAPI validation job: every message of every document must resolve to a registered subject and a matching major version.
6. Wire the producer and consumer libraries: validate against the subject before publish, cache the schema for run time, and raise the alert on a validation failure or an unreachable registry.
7. Configure the access policy: one identity per service, write only its own subjects, read the catalogue, and write every registration to the audit trail.
8. Publish the versioning and deprecation runbook, with the major-version rule, the deprecation notice and the retirement step, and hand the subject list to the service teams.

**Done when.** Every event type of the catalogue has one subject with a valid JSON Schema at BACKWARD compatibility, the gate refuses a breaking change and accepts an additive one, the AsyncAPI job is green on every document in the repository, the access policy refuses a cross-service write, and the runbook is published.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-PLT-N008-01 | A schema version is not backward compatible with the version in force | This schema cannot be registered: it is not backward compatible with the version in force. |
| MSG-PLT-N008-02 | The schema of an event has no subject in the registry | The schema of {event} is not registered. |
| MSG-PLT-N008-03 | The registry did not answer and the build stopped | The schema registry did not answer. The build stopped. |
| MSG-PLT-N008-04 | A schema declares a property that is not allowed in an event | This property is not allowed in an event schema: {property}. |

These are platform messages of the gate and the library; they carry the subject or the property name and never a business value or a personal datum.

### 15. Screens and states

None. The registry has no screen. Subject review is a pull request on `registry/subjects.yaml` and on the schema files, so the review states are those of the change request and not a workbench screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N008-INF-01 | AC1 | Contract | Every event type of the catalogue returns exactly one subject with a topic, a producer, a valid JSON Schema and the compatibility level BACKWARD |
| TC-PLT-N008-INF-02 | AC2 | Component | An added optional property is accepted; a removed required property, a renamed property, a narrowed type and an added required property are each refused and the version in force is unchanged |
| TC-PLT-N008-INF-03 | AC3 | Contract | The major version of ce_type equals the registered major version; a mismatch fails the contract check and a breaking change needs a new major version |
| TC-PLT-N008-INF-04 | AC4 | Integration | The gate fails an unregistered schema and an incompatible schema, blocks the merge, and passes a registered compatible schema; the AsyncAPI job resolves every message to a subject |
| TC-PLT-N008-INF-05 | AC5 | Component | An own-subject write is accepted and audited; an anonymous write and a cross-service write are refused and audited |
| TC-PLT-N008-INF-06 | AC6 | NFR | A scan of every registered subject finds no property that names a person, an address, an identity number or a contact point; a submitted schema with one is refused |

### 17. Guardrails

- No business value in a schema: a threshold, a band, an exclusion reason, a status list or a limit stays in the parameters, the reference data or the rule packages.
- No personal data property in any registered schema, and no personal datum in an example or a test fixture: identifiers and business facts only.
- No business data in the registry: the subjects hold schema documents, versions, checksums and references, never a payload.
- The compatibility level is never weakened without architecture approval; a breaking change is a new major version, never a relaxed subject.
- The build gate cannot be bypassed: no merge with a red schema gate, no direct write of a schema outside the pipeline.
- No secret in code or configuration: the service identities come from the platform identity store, never from a file in the repository.
- One subject per event type, one topic per service and one AsyncAPI document per topic; a duplicate subject fails the review.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| ADR-015 | Kafka with outbox, inbox and CloudEvents | One subject per event type on the topics of the catalogue, with the BACKWARD rule of the event contract | TC-PLT-N008-INF-01, TC-PLT-N008-INF-02, TC-PLT-N008-INF-04 |
| DP-09 | Outbox and inbox pattern | The payload the outbox relay publishes is validated against its subject; a failed validation keeps the record in the outbox with an alert | TC-PLT-N008-INF-02, TC-PLT-N008-INF-04 |
| DP-14 | Topic naming `rwb.<short>.events.v1` | The subject name derives from the topic and the event name of the catalogue | TC-PLT-N008-INF-01, TC-PLT-N008-INF-03 |
| Arch v5 slide 11 | JSON Schema registry, BACKWARD compatibility, AsyncAPI 3.0 per topic | The compatibility level of every subject, one subject per event type, one AsyncAPI document per topic | TC-PLT-N008-INF-01, TC-PLT-N008-INF-02, TC-PLT-N008-INF-03 |
| Arch v5 slide 22 | JSON body validated against the registry | Producer validation before publish, the cached schema at run time and the registry check point | TC-PLT-N008-INF-02, TC-PLT-N008-INF-04 |
| Arch v5 slides 42 and 43 | Schemas versioned in the registry with BACKWARD compatibility | The registration backlog per service and the version rule of the event type | TC-PLT-N008-INF-01, TC-PLT-N008-INF-03, TC-PLT-N008-INF-06 |

### 19. Out of scope

- Topic provisioning, partitions, retention, retry and dead-letter topics and topic ACLs (RWB-PLT-N002-INF).
- The AsyncAPI 3.0 documents themselves, which the service CON stories own and this story only references.
- The producer and consumer code of the services, the outbox relay and the inbox dedupe (the service stories and RWB-PLT-TE006-CON).
- The event payload design of each event type, which belongs to the producing service.
- The rule models, the DMN model registry and the rule package governance (rwb-decision, RWB-PLT-E1072-CON).
- The observability dashboards and the alerts on the event flow (RWB-PLT-N005-OPS).
- The registry product decision and its hosting, which are a platform decision recorded as Not specified in the source documents (GAP-1397; ASM-2433).
