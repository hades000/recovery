# RWB-ITG-E2022-ITG SMS and LINE dispatch through NSS and LINE OA

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2022-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1066-APP, RWB-P6-E2022-APP, RWB-P1-E2022-APP, RWB-P4-E2022-APP, RWB-P7-E2022-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-022 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a repeatable cross-service journey harness for SMS and LINE dispatch through the ACE notification path, with the delivery, conduct-check and decision-log evidence attached to the wave 2 release**, so that **the dispatch journey is proven end to end across rwb-comms, rwb-source-data, rwb-case, rwb-access and rwb-decision before the app stories of RWB-E2-022 are signed off**.

This story builds the harness, its contract fakes, its test data and its evidence pack. It builds no production screen, endpoint or table.

### 2. Business rationale

RWB-E2-022 splits into five app stories and this integration story. The app stories build the send request, the conduct check, the ledger entry, the refusal messages and the screens inside their own services. None of them can prove on its own that a message leaves rwb-comms, reaches the ACE notification path, comes back with an NSS or LINE OA result, updates the interaction ledger through rwb-source-data, raises the failed count on the contact point, and writes the refusal to the central decision ledger through rwb-decision. That proof is this story.

The journey is the same one the business cares about: a case owner sends a message from an approved template, the contact rules are applied before anything leaves the bank, and every attempt and its result is recorded (REQ-OCC-004, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010). The harness runs that journey against the published contracts of the five services and the ACE notification path test profile, on one business date, and produces evidence that can be re-run for any build.

The architecture changes the path, not the business. The monolith called NSS and LINE OA from one module. In the target, rwb-comms calls the ACE notification path (INT-17, INT-18) and never NSS or LINE OA directly (REQ-DRI-006); the account, contact point and consent facts come from rwb-source-data through its contract (DP-05); the interaction ledger is owned by rwb-source-data (DP-18); the decision record is written to the local library and the shared topic `rwb.decision-record.v1` (DP-03). The harness is the place where those five boundaries are exercised together, so a broken boundary is found in SIT and not by a customer who never receives a reminder.

The measure is the journey evidence: for each owned criterion, one pass or fail with the request, the response, the ledger entry, the decision entry and the delivery status captured in one report.

### 3. Preconditions

- The wave 2 harness environment (SIT) is available with the gateway route for `/api/recovery/*`, the Kafka topics of the five services and the shared topic `rwb.decision-record.v1`, and the ACE notification path test profile. The harness environment, its data seeding and its evidence format are not specified in the source documents (GAP-0405; ASM-0580).
- The five integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-P6-E2022-APP (rwb-comms), RWB-P1-E2022-APP (rwb-source-data), RWB-P4-E2022-APP (rwb-access), RWB-P7-E2022-APP (rwb-decision) and RWB-P1-E1066-APP.
- Templates "SMS-REMIND" "TH" version 1 with channel "SMS" and "LINE-REMIND" "TH" version 1 with channel "LINE" are Approved and current in the seeded data, and case "RC-2026-000777" is owned by "CO-0201" with borrower party "P-0077" (legacy section 7 Background).
- The blocking deviation codes per channel (X1, X2, X3 when the contact stop is on, and X6), the NSS result code map to SENT, DELIVERED, FAILED, the LINE OA status map to DELIVERED, READ and the retry limit 5 (DL11) are loaded as data, never in code (legacy section 13).
- The feature switch `rwb.comms.sms-line` is on in the harness profile (legacy section 13).
- The test user of role RW-CASEOWN ("CO-0201" in the legacy data) holds Case record right C on the case and the case is in that user's scope.
- Synthetic tokens and test numbers only: no real phone number, LINE identifier or customer data enters the harness or its evidence (legacy section 17).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date and the versions of the five contracts it is about to exercise.
2. Harness: seeds one case with case ID "RC-2026-000777", borrower party "P-0077", the two Approved templates and, per scenario, the deviation, legal-hold, consent and contact-point state the scenario names.
3. Harness: calls the P4 session operation for the test user and records the role, the scope and the Case record right it will exercise.
4. Harness: calls the P3 case operation and records the case state, legal hold and deviation flags the journey starts from.
5. Harness: calls `POST /api/recovery/comms/v1/cases/{caseId}/messages` with channel, template, language and party, and an Idempotency-Key per scenario; records the status and the body.
6. Harness: reads the interaction through `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` and records channel, direction, conduct check, delivery status and external reference.
7. Harness: reads the decision log through `GET /api/recovery/decision/v1/decision-log` and records whether the refusal entry exists with the decision code and the final call.
8. Harness: reads the ACE notification path stub journal for the channel and records how many messages left, with which reference, and how many retries the send went through.
9. Harness: subscribes to `rwb.decision-record.v1` for the run window and records the `DecisionRecorded` event that belongs to the case.
10. Harness: for the unavailable and failure scenarios, waits for the JOB-11 outbox sender window (every minute) and records the retry count, the delivery status and the exception-queue state.
11. Harness: writes the per-scenario evidence into one run report keyed by story key and business date, evaluates the gate and attaches the report to the wave 2 release record.
12. Harness: releases the run lock and restores the seeded data.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A contract fake or a real service answers an unexpected status for the journey | The scenario is marked failed and the report names the operation, the expected status and the answer | None | AC1, AC10 |
| X2 | The interaction is not readable after the send within the run window | The scenario is marked failed; the report names the case and the missing entry | None | AC1, AC3, AC5 |
| X3 | The decision ledger answers 503 on a refusal | The scenario passes only when the send call also answers 503 with MSG-P7-003 and nothing left for NSS | MSG-P7-003 | AC10 |
| X4 | The ACE notification path stub reports the channel unavailable | The send is queued, JOB-11 retries, and after the retry limit of 5 the send is in the exception queue with delivery status FAILED | MSG-GEN-006 | AC7 |
| X5 | The seeded data cannot be loaded (template not Approved, case not owned, consent not as the scenario states) | The run refuses to start and names the missing seed item; no scenario is reported | None | All |
| X6 | A scenario sends with no channel | The call answers 422 with MSG-GEN-001 naming "channel" and no message leaves | MSG-GEN-001 | AC12 |
| X7 | Another run holds the environment lock | The run refuses to start | None | All |
| X8 | The evidence pack cannot be attached to the release record | The run is marked failed; the local evidence file is kept for rerun | None | All |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the five published contracts or their fakes and the notification path test profile; it builds no service feature and has no build dependency |
| Negotiable | The scenarios, the seeded values and the stub result codes are data files, never code |
| Valuable | The dispatch journey is proven once across five services, before the app stories claim Done |
| Estimable | One journey runner, one fake set, one seed pack, one evidence collector, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a scenario with a fixed Given, When and Then and a recorded result |

### 7. Acceptance criteria

```gherkin
Feature: SMS and LINE dispatch through NSS and LINE OA

  Background:
    Given template "SMS-REMIND" "TH" version 1 with channel "SMS" is Approved and current
    Given template "LINE-REMIND" "TH" version 1 with channel "LINE" is Approved and current
    Given case "RC-2026-000777" is owned by "CO-0201" with borrower party "P-0077"
    Given case "RC-2026-000777" has no legal hold and no open deviation

  Scenario: AC1 SMS sent (legacy RWB-E2-022 AC1)
    Given party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN"
    When "CO-0201" sends POST /cases/RC-2026-000777/messages with channel "SMS", template "SMS-REMIND", language "TH" and party "P-0077", and NSS accepts it with reference "NSS-7781" returning result "DELIVERED"
    Then the response is status 202 with an interaction of channel "SMS", direction "OUTBOUND" and conduct check "PASSED"
    Then the interaction has delivery status "DELIVERED" and reference "NSS-7781"
    Then NSS received one message

  Scenario: AC3 Contact stop on lost contact (legacy RWB-E2-022 AC3)
    Given case "RC-2026-000777" has an open deviation "X6" lost contact
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 409 with MSG-P6-001 naming "X6 Lost contact"
    Then the system sends nothing to NSS
    Then the system writes an interaction with conduct check "BLOCKED"
    Then one decision log entry exists with decision code "X6" and final call "contact refused"

  Scenario: AC5 No consent on the channel (legacy RWB-E2-022 AC5)
    Given party "P-0077" has a "MOBILE" contact point with consent "WITHDRAWN"
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 409 with MSG-P6-002 naming "SMS"
    Then the system sends nothing to NSS
    Then the system writes an interaction with conduct check "BLOCKED"

  Scenario: AC6 Template withdrawn (legacy RWB-E2-022 AC6)
    Given template "SMS-REMIND" "TH" version 1 is Withdrawn and no later version is Approved
    When "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND"
    Then the response is status 409 with MSG-P6-003 naming "SMS-REMIND"

  Scenario: AC7 NSS unavailable (legacy RWB-E2-022 AC7)
    Given the ACE notification path returns "unavailable" for NSS
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 202 with MSG-GEN-006 naming "NSS"
    Then JOB-11 retries the send on its schedule
    Then after the retry limit of 5 the send is in the exception queue under rule R-UNI-34 and the interaction has delivery status "FAILED"

  Scenario: AC10 Decision log write fails on a refusal (legacy RWB-E2-022 AC10)
    Given case "RC-2026-000777" has an open deviation "X6"
    Given the decision log store is unavailable
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 503 with MSG-P7-003
    Then the system sends nothing to NSS
    Then the system raises an incident under rule R-UNI-39

  Scenario: AC12 Channel missing (legacy RWB-E2-022 AC12)
    Given template "SMS-REMIND" "TH" is current and party "P-0077" has a verified "MOBILE" contact point
    When "CO-0201" sends POST /cases/RC-2026-000777/messages with no channel
    Then the response is status 422 with MSG-GEN-001 naming "channel"
```

AC2, AC4, AC8, AC9 and AC11 are cited in the flow and exception table but are owned by the app stories of this legacy key (RWB-P6-E2022-APP, RWB-P1-E2022-APP, RWB-P4-E2022-APP and RWB-P7-E2022-APP); the seven criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every outbound message carries a conduct check result on its ledger entry | REQ-OCC-005; FEAT-OCC-05 |
| BR2 | No message is sent while a contact stop is in force | CTL-16; R-UNI-04, R-UNI-05 |
| BR3 | Deviation codes that block SMS and LINE are a reference list; X6 blocks both until a contact point is verified | R-DEV-16; R-UNI-12; Principle 1 |
| BR4 | Messages go only to a verified contact point with consent GIVEN for that channel | CTL-17; R-UNI-10 |
| BR5 | A legal hold stops every outbound action | R-UNI-20 |
| BR6 | A system that is unavailable queues the send and retries; after the limit it goes to the exception queue | R-UNI-33, R-UNI-34, R-UNI-36 |
| BR7 | A refusal that cannot be written to the decision log is not completed | Principle 5; R-UNI-39 |
| BR8 | Only the current Approved template for the channel is used | R-LIT-03; CTL-14 |
| BR9 | The same request twice sends one message | R-UNI-40 |

The rules are unchanged by the split; the story asserts them across the service boundaries and does not restate them in code.

### 9. State transitions

None. This story does not change a case status. It sets the delivery status on the ledger entry: Sent, then Delivered, Read or Failed; and the outbox record: queued, sent, retried, exception.

The harness adds a run state of its own only: Not started, Running, Passed, Failed, with the latest run for a build deciding the gate.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, squad members and the QA team | Run the harness, keep the fake mappings, the seed pack and the evidence, read reports |
| RW-CASEOWN, test user "CO-0201" | Makes the send request on the case with Case record right C and the case in scope |
| RW-TEAMMGR, RW-CONDUCT and RW-COMPLAIN | Read the blocked contacts and the contact history in the evidence where a scenario names them |
| SY-DECLOG, decision log writer | Supplies the refusal entry the harness asserts, through rwb-decision's contract only |
| Integration lead | Agrees the NSS and LINE OA test doubles and the result-code maps with the ACE notification path team |
| QA lead | Owns the seed pack, the evidence format and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 case operation |
| DF-CAS-020 | recovery_case | legal_hold | Read through the P3 case operation |
| DF-CAS-038 | deviation | deviation_code | Read through the P3 case operation |
| DF-CAS-043 | deviation | contact_stop | Read through the P3 case operation |
| DF-EXT-015 | contact_point_ext | consent_given | Read through the P1 contract |
| DF-EXT-017 | contact_point_ext | verified_at | Read through the P1 contract |
| DF-EXT-018 | contact_point_ext | failed_count | Read through the P1 contract; written by rwb-comms through the same contract, never by the harness |
| DF-REF-046, DF-REF-047, DF-REF-066 | template | template_code, template_version, channel | Seeded for the rwb-comms fake or the P6 story; read through the P6 contract when the real service is in the harness |
| DF-INT-002, DF-INT-003, DF-INT-004, DF-INT-005, DF-INT-006, DF-INT-011, DF-INT-012, DF-INT-013, DF-INT-028, DF-INT-029 | interaction | case_id, person_key, occurred_at, channel, direction, summary, conduct_check, source_system, delivery_status, external_ref | Read through the P1 interaction operation; written by rwb-comms through the ledger contract, never by the harness |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 decision log operation |

The harness owns no table (DP-01, DP-18). It reads and writes only through the published operations, and its own evidence holds identifiers, statuses and timestamps only, never personal data. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/comms/v1/cases/{caseId}/messages` | P6 rwb-comms | The dispatch request under test (AC1, AC3, AC5, AC6, AC7, AC10, AC12), with an Idempotency-Key per scenario |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | Reads the interaction entry, its conduct check, its delivery status and its external reference (AC1, AC3, AC5) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case state, the legal hold and the deviation flags the journey starts from |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Asserts the refusal entry (AC3) and the unavailable ledger on a refusal (AC10) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | Confirms the role, the scope and the Case record right the send runs under (TC-E2-022-13-ITG) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout and the breaker of DP-11, and every POST carries an Idempotency-Key (BR9). The publish-once access check that rwb-comms and rwb-case make inside their own process is not a path in the Ownership Map, so the harness confirms the right through the P4 session operation instead. The contact point, consent and failed-count reads and writes are rwb-source-data contract operations named in RWB-P1-E2022-APP; they are called by rwb-comms and not by the harness, and their paths are not restated here.

#### 12.3 Events published

None. The harness publishes no Kafka event; the evidence goes to the release record through its pipeline integration.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | Asserts that the decision record of a refusal reached the shared topic inside the run window (DP-03, DP-09), alongside the ledger read of 12.2 |

#### 12.5 Workflows and activities

JOB-11 Outbox sender (every minute) is exercised, not built. The harness waits for the relay window, records the retry count and the exception-queue state, and asserts the delivery status the journey ends on (AC7). It starts no workflow, adds no activity and writes no schedule; the dispatch call to the ACE notification path itself belongs to RWB-P6-E2022-APP.

Legacy section 12 has JOB-11 sending queued messages to the ACE notification path; Architecture v5 slide 44 gives JOB-11 the outbox relay to Kafka with every service as its owner, and the Ownership Map places the relay with PLT. The harness follows the higher source and treats the notification-path call as rwb-comms' own activity, so nothing in the harness depends on which side of that boundary the minute timer sits on.

#### 12.6 Schedules

None. The harness adds no workflow and no schedule; JOB-11's every-minute schedule is the platform's and is only observed.

#### 12.7 Tables owned

None. The harness owns no table in any schema (DP-01); it reads and writes through the operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-comms | `POST /api/recovery/comms/v1/cases/{caseId}/messages` | OpenAPI of P6 | 202 with the interaction, 409 with MSG-P6-001, MSG-P6-002 or MSG-P6-003, 422 with MSG-GEN-001, 503 with MSG-P7-003, per scenario; keeps the request journal for the idempotency assertion |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases/{caseId}` | OpenAPI of P3 | The case state, the legal hold and the deviation flags of the scenario |
| WireMock rwb-source-data | `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` | OpenAPI of P1 | The interaction entry with channel, direction, conduct check, delivery status and external reference |
| WireMock rwb-access | `GET /api/recovery/access/v1/me/session` | OpenAPI of P4 | The role, the scope and the Case record right, including the refusal for RW-PHONECOL (MSG-P4-002) |
| WireMock rwb-decision | `GET /api/recovery/decision/v1/decision-log` | OpenAPI of P7 | The refusal entry with decision code "X6" and final call "contact refused"; 503 for AC10 |
| ACE notification path stub, NSS | The notification call rwb-comms makes for channel SMS | The notification path contract, not in this workspace | An accepted reference and the result code from the NSS map (SENT, DELIVERED, FAILED) |
| ACE notification path stub, LINE OA | The notification call rwb-comms makes for channel LINE | The notification path contract, not in this workspace | Delivered and then read, from the LINE OA map (DELIVERED, READ) |

Each fake is replaced by the real service as its integration dependency lands, without a change to the scenarios. The NSS and LINE OA test doubles, their concrete result codes, the notification path test profile, the harness environment and the evidence format are not specified in the source documents (GAP-0405; ASM-0580).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 5 consumed, one hop on the owner's base with the 2 s timeout of DP-11 |
| Kafka | 1 event consumed on `rwb.decision-record.v1`; none published |
| Temporal | Observed only: JOB-11 Outbox sender and queue `rwb-comms`; no workflow, activity or schedule added |
| File | None |

### 13. Solution plan

**Package.** Folder `integration/recovery-notify` in the ACE repository, package `<ACE base package>.recovery.integration.notify`. Not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The harness owns no table and reads no schema; every read is an operation of 12.2 |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | The refusal entry is read through rwb-decision and the `DecisionRecorded` event is read on the shared topic |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | Consent, verified contact point and failed count are asserted only through the rwb-source-data contract |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The blocking deviation codes and the result-code maps are seeded reference data, never values in the harness code |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | The harness subscribes with its own consumer group and asserts the event, never the producer's table |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | JOB-11 is observed on its every-minute window; the harness adds no Schedule and no workflow |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | Each consumed operation is called once from the harness with a 2 s timeout and an Idempotency-Key on the POST |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 uses the owner's base, so the harness never calls a monolith base |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none | The interaction is read through rwb-source-data and never from a case table |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the real screens use, on the same bases |

The platform H dependencies in the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the five I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date |
| FakeRegistry | Configuration | WireMock mappings for the five services, one set per contract version |
| NotificationPathStub | Configuration | NSS and LINE OA doubles behind the ACE notification path profile, with the result-code maps as data |
| SeedPack | Data | Case, party, templates, consent, contact point, deviation and legal-hold states per scenario |
| LedgerAssertion | Service | Reads the interaction through rwb-source-data and compares conduct check, delivery status and reference |
| DecisionAssertion | Service | Reads the decision log and the shared topic and compares the decision code and the final call |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with request, response, ledger, decision and stub journal |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached |

**Environment and test data.** SIT, the wave 2 harness profile, one business date, synthetic tokens and test numbers only. The seeded values are the legacy section 7 Background and the state each scenario names; no other value is added. The environment, the seeding and the evidence format are not specified in the source documents (GAP-0405; ASM-0580).

**Build steps**

1. Write the SeedPack with the Background and the seven owned scenarios' states; test that a bad seed stops the run (X5).
2. Write FakeRegistry with the five WireMock mapping sets and the notification path stubs with the NSS and LINE OA result-code maps as data.
3. Write JourneyRunner for AC1 and AC5 and assert the interaction through rwb-source-data.
4. Add the refusal path for AC3 and AC6 with the decision log assertion and the stub journal assertion.
5. Add AC7 with the JOB-11 window, the retry count of 5 and the exception-queue state.
6. Add AC10 with the decision ledger unavailable and AC12 with the missing channel.
7. Write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record and rerun the seven scenarios on the release build.

**Feature switch.** `rwb.comms.sms-line` is on in the harness profile, as the legacy story sets it. The harness itself is a pipeline stage selected by the run profile, not by a business flag.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all seven owned scenarios, and each fake has been replaced by the real service where its I story has landed in SIT. The NSS and LINE OA doubles and the evidence sign-off wait for the values of GAP-0405.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-001 | A contact stop applies | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | No consent for the channel | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | NSS or LINE OA is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Channel or template missing | Enter {field}. |

The harness asserts these messages and never rewrites them. Its own report text is for the release team and is not part of the message standard.

### 15. Screens and states

SCR-03 Case record (state editable) gets the Send message action for roles with Case record C. SCR-04 Case timeline (states Loading; filtered) shows each message with channel, template, conduct check and delivery status. SCR-09 Exception queue lists sends that failed after the retry limit.

No screen is built by this story. The harness drives the operations behind those screens and asserts the states above through the contracts; the screens themselves belong to RWB-P6-E2022-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-022-01-ITG | AC1, BR1, BR4, BR8 | Integration | P-0077 MOBILE consent GIVEN; NSS stub reference NSS-7781 |
| TC-E2-022-02-ITG | AC2, BR4 | Integration | P-0077 LINE consent GIVEN; LINE OA stub delivered and read |
| TC-E2-022-03-ITG | AC3, BR3 | Integration | Open X6 |
| TC-E2-022-04-ITG | AC4, BR2 | Integration | Open X1 with contact stop |
| TC-E2-022-05-ITG | AC5, BR4 | Integration | MOBILE consent WITHDRAWN |
| TC-E2-022-06-ITG | AC6, BR8 | Integration | SMS-REMIND TH v1 Withdrawn |
| TC-E2-022-07-ITG | AC7, BR6 | Integration | Notification path stub unavailable for 6 attempts |
| TC-E2-022-08-ITG | AC8 | Integration | NSS result FAILED, failed count 0 |
| TC-E2-022-09-ITG | AC9, BR9 | Integration | Same Idempotency-Key twice |
| TC-E2-022-10-ITG | AC10, BR7 | Integration | Open X6; decision log stubbed unavailable |
| TC-E2-022-11-ITG | AC11, BR5 | Integration | Legal hold true |
| TC-E2-022-12-ITG | AC12 | Integration | No channel |
| TC-E2-022-13-ITG | Access | Component | RW-PHONECOL sends POST /cases/{caseId}/messages; refused with MSG-P4-002 |
| TC-E2-022-14-ITG | Principle 5 | NFR | Decision log write forced to fail on 10 refusals; none recorded as sent |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the app story's case, run across the five contracts and the notification path stubs. The app stories keep the unit and component copies of the same cases.

### 17. Guardrails

- No business value in code: templates, blocking codes, result code maps, retry limit and seeded state are data.
- No personal data in events, workflow inputs, logs, evidence or prompts. The phone number and the LINE identifier stay tokens; test data uses synthetic tokens and test numbers only.
- No read of another service's tables, and no schema of the harness's own: every read and write goes through the operations of 12.2 (DP-01, DP-18).
- No direct call to NSS or LINE OA; only the ACE notification path (REQ-DRI-006). The doubles stand behind that path, never in front of it.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.
- The harness never runs against UAT or production, and an exception is never added to a scenario; a value that must change changes in the seed pack through a reviewed change.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-004 | SMS and LINE through the bank's channel platforms, result on the case | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | R-UNI-33, R-UNI-34, R-UNI-40 | TC-E2-022-01-ITG, TC-E2-022-02-ITG, TC-E2-022-06-ITG, TC-E2-022-07-ITG, TC-E2-022-08-ITG, TC-E2-022-09-ITG, TC-E2-022-12-ITG, TC-E2-022-13-ITG |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-04, R-UNI-05, R-UNI-20, R-DEV-16, R-UNI-39 | TC-E2-022-03-ITG, TC-E2-022-04-ITG, TC-E2-022-10-ITG, TC-E2-022-11-ITG, TC-E2-022-14-ITG |
| REQ-OCC-006 | Withdrawn consent stops the channel | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-10 | TC-E2-022-05-ITG |
| REQ-ILG-010 | Messages dispatched write their result to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-34 | TC-E2-022-01-ITG, TC-E2-022-02-ITG, TC-E2-022-08-ITG |
| REQ-DRI-006 | No direct call to NSS or LINE OA; only the ACE notification path | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | No direct call to NSS or LINE OA; only the ACE notification path | TC-E2-022-01-ITG, TC-E2-022-02-ITG, TC-E2-022-07-ITG |

### 19. Out of scope

- Letters through WIN (RWB-E2-021).
- Messages sent automatically by route rules, for example the offer letter of R-RES-09 (Epic 3).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
- Self-service on LINE and HOME.SCB (FEAT-COM-01 to FEAT-COM-04, Epic 4).

The harness, the doubles and the evidence pack cover the four items above only as callers or consumers would see them; building any of them is out of scope for this story.
