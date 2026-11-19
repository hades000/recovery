<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 022 SMS and LINE dispatch through NSS and LINE OA v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v4.zip!RWB E2 022 SMS and LINE dispatch through NSS and LINE OA v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-022 SMS and LINE dispatch through NSS and LINE OA

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-022 |
| Epic | E2, release 31 December 2026 |
| Module | P6 Communications |
| Feature | FEAT-OCC-03 Dispatch SMS through NSS; FEAT-OCC-04 Dispatch a LINE message through LINE OA; FEAT-ILG-07 Bring dispatch outcomes into the ledger |
| Requirement IDs | REQ-OCC-004, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010 |
| BRD section | Business Requirements Epic 2, sections 3.6 and 4 |
| L3 process | 13 Manage documents and correspondence; 06 to 10 Recovery case processes |
| Decision | X6 |
| Priority | Must |
| Depends on | RWB-E1-052, RWB-E1-066 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **messages sent from approved templates through NSS and the LINE official account, with the contact rules applied before sending and the delivery status on the case**, so that **the customer is reached on the channel they use and every contact is recorded**.

## 2. Business rationale

Case owners send SMS and LINE messages outside the Workbench today, so a message can reach a customer under a contact stop or without consent, and the case has no record of it. This story sends from Legal-approved templates through the ACE notification path (INT-17, INT-18), refuses a message when a contact stop, a legal hold or missing consent applies, and writes every attempt and its delivery result to the interaction ledger. It serves REQ-OCC-004, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010, and controls CTL-16 and CTL-17.

## 3. Preconditions

- RWB-E1-052 is done; RWB-E1-046 provides Approved SMS and LINE templates (channel SMS or LINE) in TH and EN.
- RWB-E1-066 is done: the interaction ledger writer accepts entries.
- The ACE notification path to NSS and LINE OA is available in the environment (DL30).
- Contact points with consent status are loaded through COLLINS (INT-04).
- The list of deviation codes that block SMS and LINE is loaded as reference data.
- The sender holds RW-CASEOWN or another role with Case record C, and the case is in the sender's scope.

## 4. Flow

1. Case owner: on SCR-03 Case record chooses Send message, the channel (SMS or LINE), the template and the party.
2. System: checks the role (Case record C) and the scope; reads the current template for the channel and language through TemplateCatalog.
3. System: runs the conduct check: legal hold on the case, open deviation with contact stop, open deviation in the blocking list for the channel, and consent GIVEN on a verified contact point of that channel.
4. System: if the check fails, refuses, writes the decision log entry and a ledger entry with conduct check Blocked; stops.
5. System: merges the template, writes the ledger entry with conduct check Passed and delivery status Sent, and writes the send request to the outbox in the same transaction.
6. JOB-11 Outbox sender: sends the request to the ACE notification path; NSS or LINE OA returns an accepted reference, which the system stores on the ledger entry.
7. ACE notification path: returns the delivery result (NSS result code; LINE delivered and read); the system updates the ledger entry to Delivered, Read or Failed.
8. System: on Failed, adds one to the failed count of the contact point through the P1 interface.
9. Case owner: sees the message and its status on SCR-04 Case timeline.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case has an open X6 lost contact | Refused and logged | MSG-P6-001 | AC3 |
| X2 | An open deviation has the contact stop on | Refused and logged | MSG-P6-001 | AC4 |
| X3 | No consent GIVEN on the channel | Refused and logged | MSG-P6-002 | AC5 |
| X4 | The template is withdrawn | Refused | MSG-P6-003 | AC6 |
| X5 | NSS or LINE OA is unavailable | Queued and retried; after the retry limit to the exception queue | MSG-GEN-006 | AC7 |
| X6 | NSS returns a failure code | Ledger entry Failed; contact point failed count raised | None | AC8 |
| X7 | The same request with the same Idempotency-Key | One message only | None | AC9 |
| X8 | The decision log write fails on a refusal | Nothing sent; refusal not recorded; incident | MSG-P7-003 | AC10 |
| X9 | A legal hold is on the case | Refused and logged | MSG-P3-004 | AC11 |
| X10 | No channel given | Refused | MSG-GEN-001 | AC12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the template catalog and the ledger writer; the notification path is ACE's |
| Negotiable | Templates, blocking deviation codes and the retry limit are data |
| Valuable | Every SMS and LINE message is checked and recorded on the case |
| Estimable | One endpoint, one check service shared with letters, one result listener |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs with the notification path stubbed |

## 7. Acceptance criteria

```gherkin
Feature: SMS and LINE dispatch through NSS and LINE OA

  Background:
    Given template "SMS-REMIND" "TH" version 1 with channel "SMS" is Approved and current
    Given template "LINE-REMIND" "TH" version 1 with channel "LINE" is Approved and current
    Given case "RC-2026-000777" is owned by "CO-0201" with borrower party "P-0077"
    Given case "RC-2026-000777" has no legal hold and no open deviation

  Scenario: AC1 SMS sent
    Given party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN"
    When "CO-0201" sends POST /cases/RC-2026-000777/messages with channel "SMS", template "SMS-REMIND", language "TH" and party "P-0077"
    When NSS accepts the message with reference "NSS-7781" and returns result "DELIVERED"
    Then the response is status 202 with an interaction of channel "SMS", direction "OUTBOUND" and conduct check "PASSED"
    Then the interaction has delivery status "DELIVERED" and reference "NSS-7781"
    Then NSS received one message

  Scenario: AC2 LINE
    Given party "P-0077" has a verified "LINE" contact point with consent "GIVEN"
    When "CO-0201" sends a message with channel "LINE" and template "LINE-REMIND"
    When LINE OA reports the message delivered and then read
    Then the interaction has channel "LINE", conduct check "PASSED" and delivery status "READ"
    Then LINE OA received one message

  Scenario: AC3 Contact stop on lost contact
    Given case "RC-2026-000777" has an open deviation "X6" lost contact
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 409 with MSG-P6-001 naming "X6 Lost contact"
    Then the system sends nothing to NSS
    Then the system writes an interaction with conduct check "BLOCKED"
    Then one decision log entry exists with decision code "X6" and final call "contact refused"

  Scenario: AC4 Contact stop from a dispute
    Given case "RC-2026-000777" has an open deviation "X1" with contact stop on
    When "CO-0201" sends a message with channel "LINE"
    Then the response is status 409 with MSG-P6-001 naming "X1 Dispute or complaint"
    Then the system sends nothing to LINE OA
    Then the system writes an interaction with conduct check "BLOCKED"

  Scenario: AC5 No consent on the channel
    Given party "P-0077" has a "MOBILE" contact point with consent "WITHDRAWN"
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 409 with MSG-P6-002 naming "SMS"
    Then the system sends nothing to NSS
    Then the system writes an interaction with conduct check "BLOCKED"

  Scenario: AC6 Template withdrawn
    Given template "SMS-REMIND" "TH" version 1 is Withdrawn and no later version is Approved
    When "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND"
    Then the response is status 409 with MSG-P6-003 naming "SMS-REMIND"

  Scenario: AC7 NSS unavailable
    Given the ACE notification path returns "unavailable" for NSS
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 202 with MSG-GEN-006 naming "NSS"
    Then JOB-11 retries the send on its schedule
    Then after the retry limit of 5 the send is in the exception queue under rule R-UNI-34 and the interaction has delivery status "FAILED"

  Scenario: AC8 NSS failure result
    Given party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN" and failed count 0
    When NSS returns result "FAILED" for the message
    Then the interaction has delivery status "FAILED"
    Then the contact point has failed count 1

  Scenario: AC9 Repeated request
    Given "CO-0201" sent a message with Idempotency-Key "c0ffee00-0001"
    When the same request is sent again with Idempotency-Key "c0ffee00-0001"
    Then the response is the first response
    Then NSS received one message

  Scenario: AC10 Decision log write fails on a refusal
    Given case "RC-2026-000777" has an open deviation "X6"
    Given the decision log store is unavailable
    When "CO-0201" sends a message with channel "SMS"
    Then the response is status 503 with MSG-P7-003
    Then the system sends nothing to NSS
    Then the system raises an incident under rule R-UNI-39

  Scenario: AC11 Legal hold
    Given case "RC-2026-000777" has legal hold true
    When "CO-0201" sends a message with channel "LINE"
    Then the response is status 409 with MSG-P3-004
    Then the system sends nothing to LINE OA

  Scenario: AC12 Channel missing
    Given template "SMS-REMIND" "TH" is current and party "P-0077" has a verified "MOBILE" contact point
    When "CO-0201" sends POST /cases/RC-2026-000777/messages with no channel
    Then the response is status 422 with MSG-GEN-001 naming "channel"
```

## 8. Business rules

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

## 9. State transitions

None. This story does not change a case status. It sets the delivery status on the ledger entry: Sent, then Delivered, Read or Failed; and the outbox record: queued, sent, retried, exception.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Sends a message on a case in scope (Case record C) |
| RW-TEAMMGR, team manager | Reads messages on team cases (Case record R) |
| RW-CONDUCT, Conduct and QA officer | Reads blocked contacts on the ledger (Case record R) |
| RW-COMPLAIN, complaint officer | Reads the contact history of a disputed case (Case record R) |
| SY-DECLOG, decision log writer | Writes the refusal entry |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-CAS-038 | deviation | deviation_code | Read |
| DF-CAS-043 | deviation | contact_stop | Read |
| DF-CAS-044 | deviation | cleared_at | Read |
| DF-PTY-014 | contact_point | party_id | Read |
| DF-PTY-015 | contact_point | channel | Read |
| DF-PTY-016 | contact_point | value_token | Read |
| DF-PTY-018 | contact_point | consent_status | Read |
| DF-PTY-019 | contact_point | verified_at | Read |
| DF-PTY-020 | contact_point | failed_count | Write, through the P1 interface |
| DF-REF-046 | template | template_code | Read |
| DF-REF-047 | template | template_version | Read |
| DF-REF-066 | template | channel | Read |
| DF-INT-002 | interaction | case_id | Write, through the ledger writer |
| DF-INT-003 | interaction | party_id | Write, through the ledger writer |
| DF-INT-004 | interaction | occurred_at | Write, through the ledger writer |
| DF-INT-005 | interaction | channel | Write, through the ledger writer |
| DF-INT-006 | interaction | direction | Write, through the ledger writer |
| DF-INT-011 | interaction | summary | Write, through the ledger writer |
| DF-INT-012 | interaction | conduct_check | Write, through the ledger writer |
| DF-INT-013 | interaction | source_system | Write, through the ledger writer |
| DF-INT-028 | interaction | delivery_status | Write, through the ledger writer |
| DF-INT-029 | interaction | external_ref | Write, through the ledger writer |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /cases/{caseId}/messages** (new, recorded in the additions file)

| Item | Value |
|---|---|
| Request | MessageRequest: channel (SMS or LINE, required), templateCode (required), language (TH or EN, default TH), partyId (default the borrower) |
| Response | 202 Interaction: id, caseId, partyId, occurredAt, channel, direction, conductCheck, summary, sourceSystem, deliveryStatus, externalRef |
| Errors | 401 no session; 403 role lacks Case record C (MSG-P4-002); 404 case out of scope (MSG-P4-003); 409 contact stop (MSG-P6-001), no consent (MSG-P6-002), template withdrawn (MSG-P6-003), legal hold (MSG-P3-004); 422 field missing (MSG-GEN-001); 503 decision not recorded (MSG-P7-003) |
| Authorization | Case record, right C, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours |

The current GET /api/recovery/v1/cases/{caseId}/interactions (P3) returns the entries with their status.

**Job JOB-11 Outbox sender**: every minute; sends queued messages to the ACE notification path; idempotency key the interaction ID; retry limit 5, assumed; DL11; after the limit the send goes to the exception queue (R-UNI-34).

**Published interfaces**

```java
// ACE common module notification path (INT-17, INT-18)
NotificationAck NotificationPort.send(NotificationRequest request);   // channel, contactPointToken, templateRef, language, caseRef
// P6, called by the ACE notification path with each result
void MessageResultListener.onResult(String externalRef, String channel, String result, Instant at);
// Owned elsewhere
List<ContactStopView> DeviationApi.activeContactStops(UUID caseId);                    // S8
List<ContactPointView> PartyApi.contactPoints(UUID partyId, String channel);            // P1
void PartyApi.recordFailedContact(UUID contactPointId, Instant at);                    // P1
UUID InteractionLedgerApi.record(InteractionRecord record);                            // ledger writer
void InteractionLedgerApi.updateDelivery(UUID interactionId, String status, String externalRef); // ledger writer
```

## 13. Solution plan

- Package: folder `recovery/comms/messaging`, Java package `recovery.comms.messaging`; front end folder `recovery/comms/messaging`.

| Component | Type | Responsibility |
|---|---|---|
| MessageController | Controller | POST /cases/{caseId}/messages |
| MessageService | Service | Template, conduct check, merge, ledger entry and outbox write in one transaction |
| ConductCheckService | Service | From RWB-E2-021, extended with the channel blocking list and the consent check |
| MessageOutboxSender | Job | Handler of JOB-11 for message sends |
| MessageResultListener | Published interface | Maps NSS and LINE OA results to delivery status |
| SendMessageDialog | React component | Send message on SCR-03: channel, template and party, with the refusal message shown |

- Database: no new table. The outbox table of the ACE pattern holds the send requests. The ledger gets delivery_status and external_ref through the ledger writer (additions).
- Configuration and reference data: blocking deviation codes per channel, SMS and LINE: X1, X2, X3 when contact stop is on, and X6, assumed, owner Conduct and QA officer; NSS result code map to SENT, DELIVERED, FAILED and LINE OA status map to DELIVERED, READ (data steward); retry limit 5 (DL11).
- Build steps:
  1. Add MessageRequest and the Interaction fields to the OpenAPI file; generate the controller interface.
  2. Extend ConductCheckService with the blocking list and consent; unit test AC3, AC4, AC5, AC11.
  3. Build MessageService with the template check, the decision log write on refusal and the outbox write; test AC6, AC10, AC12.
  4. Build MessageOutboxSender with the retry and exception path; test AC7 with the notification path stubbed.
  5. Build MessageResultListener and the failed count call; test AC1, AC2, AC8.
  6. Add the Idempotency-Key store; test AC9.
  7. Build SendMessageDialog; browser test of a send and a refusal.
- Feature flag: `rwb.comms.sms-line`.
- Done when: the tests in section 16 pass, and the NSS and LINE OA stubs are replaced by the ACE notification path in SIT with one SMS and one LINE message to test numbers.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-001 | A contact stop applies | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | No consent for the channel | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-GEN-006 | NSS or LINE OA is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Channel or template missing | Enter {field}. |

## 15. Screens and states

SCR-03 Case record (state editable) gets the Send message action for roles with Case record C. SCR-04 Case timeline (states Loading; filtered) shows each message with channel, template, conduct check and delivery status. SCR-09 Exception queue lists sends that failed after the retry limit.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-022-01 | AC1, BR1, BR4, BR8 | System | P-0077 MOBILE consent GIVEN; NSS stub reference NSS-7781 |
| TC-E2-022-02 | AC2, BR4 | System | P-0077 LINE consent GIVEN; LINE OA stub delivered and read |
| TC-E2-022-03 | AC3, BR3 | System | Open X6 |
| TC-E2-022-04 | AC4, BR2 | System | Open X1 with contact stop |
| TC-E2-022-05 | AC5, BR4 | System | MOBILE consent WITHDRAWN |
| TC-E2-022-06 | AC6, BR8 | System | SMS-REMIND TH v1 Withdrawn |
| TC-E2-022-07 | AC7, BR6 | System | Notification path stub unavailable for 6 attempts |
| TC-E2-022-08 | AC8 | System | NSS result FAILED, failed count 0 |
| TC-E2-022-09 | AC9, BR9 | System | Same Idempotency-Key twice |
| TC-E2-022-10 | AC10, BR7 | System | Open X6; decision log stubbed unavailable |
| TC-E2-022-11 | AC11, BR5 | System | Legal hold true |
| TC-E2-022-12 | AC12 | System | No channel |
| TC-E2-022-13 | Access | Access | RW-PHONECOL sends POST /cases/{caseId}/messages; refused with MSG-P4-002 |
| TC-E2-022-14 | Principle 5 | Resilience | Decision log write forced to fail on 10 refusals; none recorded as sent |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: templates, blocking codes, result code maps and the retry limit are data.
- No personal data in logs, tests or prompts. The phone number and LINE identifier stay tokens in the Workbench; the ACE notification path detokenizes them. Test data uses synthetic tokens and test numbers only.
- No read of another module's tables. Deviations, contact points and the ledger go through their interfaces.
- No direct call to NSS or LINE OA; only the ACE notification path (REQ-DRI-006).

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-004 | SMS and LINE through the bank's channel platforms, result on the case | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | R-UNI-33, R-UNI-34, R-UNI-40 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-06, TC-E2-022-07, TC-E2-022-08, TC-E2-022-09, TC-E2-022-12, TC-E2-022-13 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-04, R-UNI-05, R-UNI-20, R-DEV-16, R-UNI-39 | TC-E2-022-03, TC-E2-022-04, TC-E2-022-10, TC-E2-022-11, TC-E2-022-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-10 | TC-E2-022-05 |
| REQ-ILG-010 | Messages dispatched write their result to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-34 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-08 |

## 19. Out of scope

- Letters through WIN (RWB-E2-021).
- Messages sent automatically by route rules, for example the offer letter of R-RES-09 (Epic 3).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
- Self-service on LINE and HOME.SCB (FEAT-COM-01 to FEAT-COM-04, Epic 4).
