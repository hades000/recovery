# RWB-PLT-N002-INF Kafka topics, retry and dead-letter topics and ACLs

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-N002-INF |
| Work type | INF (Infrastructure) |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-EVT |
| Wave | 0 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | N002 |
| Legacy disposition | New |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-EVT-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: new platform story for RWB-PLT-EVT, legacy key N002. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **infrastructure engineer**, I want **the Recovery Kafka topic set — one event topic per service, the shared decision-record topic, three retry topics and one dead-letter topic per event topic, and least-privilege ACLs — provisioned from configuration as code on the ACE Kafka platform**, so that **the 19 services publish and consume facts with per-case ordering, retry and replay from Day 1 without a new platform, a new outsourcing review or a hand-built topic**.

### 2. Business rationale

ACE already runs Kafka for its PII logging, so hosting the Recovery business events on the same bank platform means no new platform and no new outsourcing assessment (Arch v5 slide 21). What is new is a dedicated Recovery topic set with its own ACLs, quotas and subjects, separate from the ACE PII logging topics, so the Recovery traffic neither exposes personal data through the logging path nor inherits its access rules.

The topic design carries five decisions. Ordering per case comes from the record key caseId, so one case's events arrive in order across the twelve partitions of its topic. Retention and replay let a new or repurposed service rebuild its own view from history, which the reuse goal needs. One consumer group per service means many independent listeners and a producer that never changes. A retry ladder of 1 min, 10 min and 1 h followed by a dead-letter topic turns an at-least-once delivery into a recoverable failure instead of a lost fact. The fallback, Azure Event Hubs Premium through its Kafka endpoint, keeps the same producer and consumer code, so the platform choice can change without a rewrite.

The set is 20 event topics — nineteen `rwb.<short>.events.v1` topics and the shared `rwb.decision-record.v1` — with 60 retry topics and 20 dead-letter topics, 100 topics in total. Recovery volume is small, tens of thousands of events a day, so capacity is a confirmation and not a design risk. This story is a Wave 0 enabler: "Kafka topics + ACLs" is a platform item of Arch v5 slide 38, and every service story in waves 1 to 4 assumes the topics and the ACLs already exist.

### 3. Preconditions

- The Kafka hosting decision (Arch v5 slide 39, decision 1) is taken: Recovery business events on the bank Kafka platform ACE already uses, with separate topics and ACLs from PII logging, and Event Hubs Premium as the fallback.
- The ACE platform team has confirmed capacity, topic naming, the ACL model and the environment list; these are the open points of the slide 21 notes and are carried as a gap of this story.
- A network path from the AKS cluster to the brokers exists for every environment, with the cluster's workload identities able to reach it.
- The schema registry of RWB-PLT-N008-INF is available for payload validation of the event topics where the producing service registers subjects.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the topic catalogue from the Ownership Map and the event catalogue of Arch v5 slides 41, 42 and 43: one topic per service plus the shared decision-record topic.
2. Fix the settings on every event topic: 12 partitions, replication factor 3, 7-day retention, cleanup policy delete and key caseId.
3. Derive the three retry topics and the dead-letter topic of every event topic from the same configuration, with the same partition count and the retry windows of 1 min, 10 min and 1 h.
4. Write the ACLs from the consumer lists of the event catalogue: each service writes its own topic and the shared topic, and reads only the topics where the catalogue lists it as a consumer.
5. Set the authentication and the quotas: Transport Layer Security on every listener, OAUTHBEARER with the Entra identity or mutual TLS with the workload identity, and one principal per service.
6. Apply the catalogue per environment from the same files, with the environment differences held in the environment file and never by hand.
7. Verify the settings on the broker after the apply and run the ACL negative tests: a write to another service's topic, a read where the catalogue lists no consumer, an anonymous connection.
8. Publish the Event Hubs Premium fallback profile and the replay runbook, and hand the catalogue to the service stories so that the outbox relays and the consumers bind to fixed names.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The platform does not answer during an apply | The apply stops before any change, the catalogue stays as it was and the operator reruns it | MSG-PLT-N002-04 | AC1 |
| X2 | A topic already exists with different partitions or retention | The apply refuses the change and reports the difference; nothing is altered in place | MSG-PLT-N002-01 | AC1 |
| X3 | A client writes to a topic it does not own | The broker refuses the write and the attempt is audited | MSG-PLT-N002-02 | AC3 |
| X4 | A consumer fails the three retries | The record goes to the dead-letter topic, one alert is raised and the replay tool is the recovery path | MSG-PLT-N002-03 | AC2 |
| X5 | A service exhausts its quota | The producer is throttled, the outbox holds the events and nothing is lost; the relay drains when the quota frees | None | AC5 |
| X6 | The bank platform is not available at all | The Event Hubs Premium profile is applied with the same names and settings and the same code connects | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the Ownership Map and the event catalogue only |
| Negotiable | The derived retry and dead-letter names, the ACL principal model and the quota values are agreed with the ACE platform team; the topic pattern, the settings and the retry windows are fixed by the target architecture |
| Valuable | Gives every service in waves 1 to 4 a fixed, provisioned topic set on Day 1 and removes the hand-built topic from every service plan |
| Estimable | Six configuration files, one runbook, one ACL negative test suite and six acceptance criteria |
| Small | Fits one sprint with the apply, the verification and the negative tests |
| Testable | Every criterion is tested against the provisioned broker state, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Recovery Kafka topic set for the 19 services

  Background:
    Given the Kafka hosting decision on the ACE platform is taken
    Given the event catalogue of the architecture lists one producer topic per service and the shared decision-record topic

  Scenario: AC1 The topic catalogue is provisioned from configuration as code (new, D-RCV-60)
    Given the topic catalogue file of the Recovery topic set
    When it is applied to a clean environment
    Then the 19 service topics rwb.<short>.events.v1 and the shared rwb.decision-record.v1 exist
    Then every event topic has 12 partitions, replication factor 3, 7-day retention and the record key caseId
    When the same file is applied a second time
    Then no topic is created, changed or deleted

  Scenario: AC2 Every event topic has three retry topics and one dead-letter topic (new, D-RCV-60)
    Given a provisioned event topic
    When the catalogue is reviewed
    Then it has a retry topic for 1 min, a retry topic for 10 min and a retry topic for 1 h
    Then it has one dead-letter topic with the same partition count
    When a consumer fails a record three times
    Then the record walks the three retry windows in order and lands in the dead-letter topic
    Then one alert is raised and the record is replayable with the replay tool

  Scenario: AC3 The ACLs are least privilege and separate from the ACE PII topics (new, D-RCV-60)
    Given a service principal
    When it writes its own topic and the shared rwb.decision-record.v1
    Then the write succeeds
    When it writes another service's topic
    Then the write is refused
    When it reads a topic where the event catalogue does not list it as a consumer
    Then the read is refused
    Then no Recovery ACL grants access to an ACE PII logging topic

  Scenario: AC4 The topic names follow the platform rule and no legacy name is provisioned (new, D-RCV-60)
    Given the provisioned topic list
    When every name is checked against the naming rule
    Then every name is rwb.<short>.events.v1 for one of the 19 service shorts or rwb.decision-record.v1
    Then no legacy name pattern and no personal-data purpose is provisioned
    Then the retry and dead-letter names derive from the event topic name and appear in the catalogue

  Scenario: AC5 The connection is authenticated and encrypted (new, D-RCV-60)
    Given a client connection to a Recovery topic
    When it is opened without a credential
    Then the broker refuses it
    When it is opened with the workload identity
    Then the connection is over TLS and authenticated with OAUTHBEARER or mutual TLS
    Then the service principal quota caps the throughput of that service

  Scenario: AC6 The Event Hubs Premium fallback is documented and exercisable (new, D-RCV-60)
    Given the fallback profile file of this story
    When it is applied to an Event Hubs Premium namespace
    Then the same topic names and the same settings exist through the Kafka endpoint
    Then the same producer and consumer code connects with the same names and no code change
    Then the runbook states the switch-over and the switch-back steps and who performs each
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One event topic per service, `rwb.<short>.events.v1`, plus the shared `rwb.decision-record.v1`; no service publishes to another service's topic | DP-14; Arch v5 slides 41, 42 and 43 |
| BR2 | Every event topic has 12 partitions, replication factor 3, 7-day retention, key caseId and cleanup policy delete | Arch v5 slides 9 and 22 |
| BR3 | Every event topic has three retry topics (1 min, 10 min, 1 h) and then a dead-letter topic, with an alert and a replay tool | Arch v5 slides 11 and 22 |
| BR4 | One principal per service, least privilege, TLS on every listener, OAUTHBEARER with the Entra identity or mutual TLS with the workload identity | Arch v5 slides 11 and 35 |
| BR5 | Recovery topics are separate from the ACE PII logging topics; no Recovery ACL opens a PII logging topic and no PII topic is mixed into the Recovery set | Arch v5 slide 21 |
| BR6 | Events carry the CloudEvents 1.0 envelope in binary mode, IDs and facts only, and no personal data | Arch v5 slides 11 and 22 |
| BR7 | The Event Hubs Premium fallback keeps the same names and the same client code; a fallback that needs a code change is not accepted | Arch v5 slide 21 |
| BR8 | No business value lives in the catalogue: partitions, retention, quotas and the environment list are platform settings, not parameters of the business rules | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Catalogue drafted | The topic list and the settings are written in the configuration files | Reviewed |
| Reviewed | Review closed | The ACE platform team, security architecture and the service teams accept the names and the settings | Provisioned |
| Provisioned | Apply succeeds | The topics exist in the environment with the settings of the catalogue | Provisioned |
| Provisioned | ACLs bound | Every service principal resolves to its write and read lists | Access bound |
| Access bound | First producer publishes | The outbox relay of a service sends and the consumer group reads | In use |
| In use | Additive change | A partition, a retention value or a quota is raised and the change is applied from the file | Changing |
| Changing | Apply succeeds | The new settings are in force and no name changed | In use |
| In use | Topic retired | The owning service no longer publishes and the retention has elapsed | Retired |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SCB IT infrastructure | Owns this story, the catalogue files and the apply |
| ACE platform team | Owns the brokers, the quotas and the environment list; approves the naming, the ACL model and every change to a setting |
| Security architecture | Approves the ACL model, the authentication mechanism and the separation from the PII logging topics |
| Service teams | State their producer and consumer needs; they never create a topic or an ACL by hand |
| Data steward | Confirms that no topic carries a personal-data purpose and no event carries personal data |
| Release manager | Schedules the apply per environment and the fallback rehearsal |

The ACL principal model, the principal names and the quota values are Not specified in the source documents (GAP-1398; ASM-2434).

### 11. Data

| Topic | Owner | Partitions | Replication | Retention | Key |
|---|---|---|---|---|---|
| `rwb.source-data.events.v1` | P1 | 12 | 3 | 7 days | caseId |
| `rwb.integration.events.v1` | P2 | 12 | 3 | 7 days | caseId |
| `rwb.case.events.v1` | P3 | 12 | 3 | 7 days | caseId |
| `rwb.access.events.v1` | P4 | 12 | 3 | 7 days | caseId |
| `rwb.document.events.v1` | P5 | 12 | 3 | 7 days | caseId |
| `rwb.comms.events.v1` | P6 | 12 | 3 | 7 days | caseId |
| `rwb.decision.events.v1` | P7 | 12 | 3 | 7 days | caseId |
| `rwb.payment.events.v1` | P8 | 12 | 3 | 7 days | caseId |
| `rwb.reporting.events.v1` | P9 | 12 | 3 | 7 days | caseId |
| `rwb.agent.events.v1` | P10 | 12 | 3 | 7 days | caseId |
| `rwb.valuation.events.v1` | S1 | 12 | 3 | 7 days | caseId |
| `rwb.treatment.events.v1` | S2 | 12 | 3 | 7 days | caseId |
| `rwb.guarantee.events.v1` | S3 | 12 | 3 | 7 days | caseId |
| `rwb.litigation.events.v1` | S4 | 12 | 3 | 7 days | caseId |
| `rwb.asset.events.v1` | S5 | 12 | 3 | 7 days | caseId |
| `rwb.debtsale.events.v1` | S6 | 12 | 3 | 7 days | caseId |
| `rwb.writeoff.events.v1` | S7 | 12 | 3 | 7 days | caseId |
| `rwb.deviation.events.v1` | S8 | 12 | 3 | 7 days | caseId |
| `rwb.partner.events.v1` | S9 | 12 | 3 | 7 days | caseId |
| `rwb.decision-record.v1` | shared (19 producers) | 12 | 3 | 7 days | caseId |

The consumers of each topic come from the event catalogue of Arch v5 slides 42 and 43 and are the only source of the read ACLs. The shared topic carries the same catalogue settings as the service topics, because no source gives it a setting of its own. The retry and dead-letter topic names and the ACL principals are Not specified in the source documents (GAP-1398; ASM-2434). The message content is out of scope of this story: the payload schemas belong to the producing services and to the registry of RWB-PLT-N008-INF. The quota values per service are Not specified in the source documents (GAP-1398; ASM-2434).

### 12. Contract

#### 12.1 REST operations provided

None.

#### 12.2 REST operations consumed

None.

#### 12.3 Events published

None. The platform provides the topics; the event types are owned by the producing services.

#### 12.4 Events consumed

None.

#### 12.5 Workflows and activities

None.

#### 12.6 Schedules

None. The outbox relay JOB-11 runs inside each service (Arch v5 slide 44).

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

None. The tests use a throwaway Kafka broker and the ACL test harness.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| Kafka | 20 event topics provided, 60 retry topics and 20 dead-letter topics (100 topics) | One consumer group per service, CloudEvents 1.0 binary mode, key caseId |
| REST | None | The platform provides no REST surface |
| Temporal | None | No workflow and no activity in this story |
| File | None | No file in this story |

### 13. Solution plan

**Deliverables.** `platform/kafka/topics.yaml` (the 20 event topics, the 60 retry topics and the 20 dead-letter topics with their settings), `acls.yaml` (one principal per service and the write and read lists taken from the event catalogue), `quotas.yaml`, `environments.yaml`, `fallback-event-hubs.yaml` (the Event Hubs Premium profile with the same names and settings), `runbook.md` (apply, verify, replay and switch-over), and the ACL negative test suite.

**Pattern application.** None of the decoupling-pattern markers of Template and Rules §R5.5 appears in this new platform story: it introduces no legacy table, no legacy login, no legacy topic name and no legacy call, so no DP row is applied here and the metadata row "Patterns applied" reads None. The two patterns the catalogue serves are applied by the consuming stories: DP-14 (topic naming, `rwb.<short>.events.v1` instead of the legacy `rwb.p<n>.` and `rwb.casewf.` names) and DP-09 (outbox and inbox with CloudEvents) are applied by the 19 service stories against the topics this story provisions.

**Build steps**

1. `topics.yaml`: the 20 event topics of section 11 with 12 partitions, replication factor 3, 7-day retention, cleanup policy delete and key caseId.
2. Derive the retry and dead-letter topics from the same file, three retry windows and one dead-letter topic per event topic, with the derived names of the assumption row.
3. `acls.yaml`: one principal per service from its workload identity, the write list (own topic and the shared topic) and the read list from the consumer columns of the event catalogue.
4. `quotas.yaml` and the authentication settings: TLS, OAUTHBEARER with the Entra identity or mutual TLS, and the per-service quota.
5. `environments.yaml`: the environment list and the differences per environment, so that one file set applies everywhere.
6. Apply per environment and verify the broker state against the file; a difference fails the apply and is reported.
7. The ACL negative tests: write to another service's topic, read without a consumer entry, anonymous connection, quota exhaustion.
8. `fallback-event-hubs.yaml`, the runbook and the playbook rehearsal; then hand the catalogue to the service stories and to RWB-PLT-N008-INF for the subjects.

**Done when.** The 100 topics exist in every environment with the settings of section 11, a second apply changes nothing, the four ACL negative tests pass, the fallback profile has been applied once and the same code connected, and the service stories build their outbox relays against these names.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-PLT-N002-01 | A topic exists with different partitions, retention or replication | The topic {topic} already exists with different settings. The apply stopped and nothing was changed. |
| MSG-PLT-N002-02 | A client attempts an operation its ACL does not allow | The action is not authorised on the topic {topic}. |
| MSG-PLT-N002-03 | A record reached the dead-letter topic | A record reached the dead-letter topic {topic} and the alert was raised. Replay it from the runbook when the cause is fixed. |
| MSG-PLT-N002-04 | The platform did not answer during an apply | The Kafka platform did not answer. The apply stopped and the catalogue is unchanged. |

The four message IDs belong to this story; they are operator and platform messages and not business messages.

### 15. Screens and states

None. The platform has no screen; the catalogue is reviewed as code, and every state of section 9 is a pipeline or a broker state and not a screen state.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-N002-INF-01 | AC1 | Component | The catalogue applies to a clean broker; 20 event topics exist with 12 partitions, replication factor 3, 7-day retention and key caseId; a second apply reports no change |
| TC-PLT-N002-INF-02 | AC2 | Integration | A failing consumer walks the three retry windows and lands in the dead-letter topic; one alert is raised and the replay puts the record back |
| TC-PLT-N002-INF-03 | AC3 | Contract | Each service principal writes its own topic and the shared topic and is refused on another service's topic; an unlisted read is refused; no ACL names a PII logging topic |
| TC-PLT-N002-INF-04 | AC4 | Component | Every provisioned name matches the 19 service shorts or the shared topic; no legacy pattern and no personal-data purpose appears in the catalogue |
| TC-PLT-N002-INF-05 | AC5 | NFR | An anonymous connection is refused; an authenticated connection negotiates TLS and OAUTHBEARER or mutual TLS; the quota throttles the producer and the outbox keeps the events |
| TC-PLT-N002-INF-06 | AC6 | Integration | The fallback profile creates the same names on an Event Hubs Premium namespace and the unchanged producer and consumer code connects |

### 17. Guardrails

- No business value in the catalogue: partitions, retention, quotas and the environment list are platform settings and never a parameter of a business rule.
- No personal data on a topic or in an event: the topic set carries IDs and facts only, and a topic with a personal-data purpose is not provisioned.
- ACLs are least privilege and reviewed: one principal per service, the write list and the read list taken from the event catalogue, and a review on every change.
- No topic for another purpose and no PII topic mixed with the Recovery topics; the Recovery ACLs never open an ACE PII logging topic.
- Settings come from configuration as code and are never changed by hand; a manual change is corrected by the next apply and reported.
- No secret in code or in configuration: authentication uses the workload identity, and no password or key is written into a catalogue file.
- Every test payload is synthetic; no production payload is copied into a topic, a test or a runbook example.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic set, the per-case key and the CloudEvents binary mode this story provisions | TC-PLT-N002-INF-01, TC-PLT-N002-INF-04 |
| DP-09 | Outbox and inbox library | The topics the outbox relays publish to and the consumer groups that read them | TC-PLT-N002-INF-01, TC-PLT-N002-INF-02 |
| DP-14 | Topic naming `rwb.<short>.events.v1` | The 19 service topics and the shared decision-record topic of section 11 | TC-PLT-N002-INF-04 |
| Arch v5 slide 21 | Kafka hosting on the ACE platform, separate topics and ACLs from PII logging | The ACL separation rule and the Event Hubs Premium fallback profile | TC-PLT-N002-INF-03, TC-PLT-N002-INF-06 |
| Arch v5 slide 22 | The event path: outbox, topic, consumers, retry and dead-letter | The retry ladder, the dead-letter topic, the alert and the replay runbook | TC-PLT-N002-INF-02 |
| Arch v5 slide 35 | Zero trust and Kafka ACLs per service | One principal per service, TLS and OAUTHBEARER or mutual TLS | TC-PLT-N002-INF-03, TC-PLT-N002-INF-05 |

### 19. Out of scope

- The producer and consumer code and the outbox relay of each service; they belong to the 19 service stories and bind to the names this story fixes.
- The schema registry and the subjects; they belong to RWB-PLT-N008-INF.
- The Temporal namespace and its certificates; they belong to RWB-PLT-N003-INF.
- The dashboards and the alert routing beyond the dead-letter alert; they belong to RWB-PLT-N005-OPS.
- The service deployment and the Helm charts of the 19 services.
- The event payload design, which belongs to the producing services.
- The ACL model decision and any edit to the event catalogue, which are platform decisions recorded in the Ownership Map.
