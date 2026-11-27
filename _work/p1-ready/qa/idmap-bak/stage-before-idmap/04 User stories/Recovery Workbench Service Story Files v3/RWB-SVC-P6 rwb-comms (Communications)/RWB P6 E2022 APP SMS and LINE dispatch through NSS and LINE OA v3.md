# RWB-P6-E2022-APP SMS and LINE dispatch through NSS and LINE OA

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2022-APP |
| Work type | APP (App development) |
| Size | Set by the squad at refinement; not specified in the source documents (DOR-RWB-P6-E2022-APP-16) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P6-A |
| Ready to start | After RWB-P6-E1052-APP |
| Depends on (build) | RWB-P6-E2022-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON, RWB-P6-E1052-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P1-E1066-CON; rwb-source-data.yaml 5.1.0 (API Specification v7) for the contact-point read, the failed-contact count and the case-scoped interaction ledger |
| Integration dependencies | None |
| Contract version | v1 (the /api/recovery/comms/v1 path); consumes rwb-source-data.yaml 5.1.0 |
| External dependencies | RWB-P6-E2022-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-010, FR-P6-017, FR-P6-018, FR-P6-020, FR-P6-022, FR-P6-023, FR-P6-024, FR-P6-025, FR-P6-026, FR-P6-027, FR-P6-028, FR-P6-029, FR-P6-030, FR-P6-031, FR-P6-036) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-041, RD-P1-064, RD-P1-070 |

**Version 3 changes.**

- The P1 operations are named from rwb-source-data.yaml 5.1.0: contact-point read, failed-contact count and the case-scoped ledger (RD-P1-005, RD-P1-007; finding 1).
- The ledger is append-only: the send, the accepted reference and each result are separate `CONTACT` entries; no interaction is updated (RD-P1-007; findings 2 to 4, 6).
- Idempotency and error answers follow the shared rules; AC9 uses a UUID key (RD-P1-001, RD-P1-004; findings 5, 7).
- AC17 to AC20 added. RD-P1-041: this story reads and writes no freshness stamp.
- Finishing pass: a failed ledger append commits nothing (RD-P1-064 rule 13), the failed contact is counted once through `processed_event` (RD-P1-070) and the append permission is settled; test case IDs of Test Cases v9 and the Error and Message Standard v6 wording applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-022 for rwb-comms in the 19-service realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E2022-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 18 cross-document, 8 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **messages sent from approved templates through NSS and the LINE official account, with the contact rules applied before sending and the delivery status on the case**, so that **the customer is reached on the channel they use and every contact is recorded**.

This story is the rwb-comms part of legacy RWB-E2-022. It builds one operation — `POST /cases/{caseId}/messages` on base `/api/recovery/comms/v1` — with the conduct check, the outbox row, the recording of the refusal in the local decision record, the mapping of the NSS and LINE OA results onto the delivery status, and the screen action behind SCR-03 and SCR-04. It builds no case state, no ledger table and no direct call to NSS or LINE OA.

### 2. Business rationale

Case owners send SMS and LINE messages outside the Workbench today, so a message can reach a customer under a contact stop or without consent, and the case has no record of it. This story sends from Legal-approved templates through the ACE notification path (INT-17, INT-18), refuses a message when a contact stop, a legal hold or missing consent applies, and records every attempt and its delivery result. It serves REQ-OCC-004, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010, and controls CTL-16 and CTL-17.

The realignment changes the path, not the business. The monolith called NSS and LINE OA from one module and wrote the interaction into its own schema. In the target, rwb-comms calls only the ACE notification path (REQ-DRI-006), the contact point, its consent and its failed count belong to rwb-source-data (DP-05, DP-18), the case and its legal hold belong to rwb-case, the deviation that carries the contact stop belongs to rwb-deviation, and the decision record is written to the local library and the shared topic `rwb.decision-record.v1` (DP-03). This story therefore calls one contract of rwb-source-data and one read of rwb-case, publishes the decision record, and writes no other service's table.

**Where the other criteria of the legacy key are owned.** This story owns AC2, AC4, AC8, AC9 and AC11. AC1, AC3, AC5, AC6, AC7, AC10 and AC12 are owned by the wave 2 integration story `RWB-ITG-E2022-ITG`, which proves the same values across rwb-comms, rwb-source-data, rwb-case, rwb-access and rwb-decision against the ACE notification path test profile; they are not copied here. The contract baseline of the operation is `RWB-P6-E2022-CON`, the deployment of its egress, retry and operator surfaces is `RWB-P6-E2022-OPS`, and the other criteria of the legacy key are answered in the same wave by the reads of RWB-P1-E2022-APP, RWB-P4-E2022-APP and RWB-P7-E2022-APP.

### 3. Preconditions

- `RWB-P6-E2022-CON` is published: the request and answer shapes of `POST /cases/{caseId}/messages`, the refusal envelope, the delivery status list, the Idempotency-Key rule, the event envelopes and the fakes (DP-11).
- `RWB-P6-E1052-APP` is delivered, so notices, templates and the template catalog of `rwb_comms` exist and a current Approved template can be resolved for a channel and a language.
- rwb-source-data.yaml 5.1.0 and its fake publish the contact-point read `GET /contact-points?personKey=&channel=`, the count `POST /contact-points/{contactPointKey}/failed-contacts` and the ledger `POST` and `GET /cases/{caseId}/interactions` with `InteractionRequest` 5.1.0 (`RWB-P1-E1066-CON`; `RWB-P1-E2022-APP`; RD-P1-005; RD-P1-007). The contract story that publishes the two contact-point operations and their fake is pending (NEW-GAP-S10-18). The permission row that gives the rwb-comms workload identity the append right (Case record C on rwb-source-data) is added by RD-P1-064 rule 2 (NEW-GAP-F10-01 closed).
- `RWB-P3-E1043-CON` is published for the reference data of LOV-CHANNEL (DP-07), so `SMS` and `LINE` are data rows and not values in code.
- The case facts the conduct check needs — the legal hold and the open deviation with the contact stop — arrive through the rwb-case case read, and the deviation facts also arrive as `DeviationRaised` and `DeviationCleared` (DP-09). The case read is not in this story's Contract dependencies and the area and right of the refusal are declared at gateway-bff, because DP-08 is not in the pattern set of this legacy key (GAP-1075; ASM-2023).
- The decision-record library and the shared topic `rwb.decision-record.v1` are live (DP-03, RWB-PLT-E1027-CON), and the outbox and inbox library is live in schema `rwb_comms` (DP-09, RWB-PLT-TE006-CON).
- The ACE notification path to NSS and LINE OA is available in the environment (legacy DL30), and its request and result shapes are carried by the stub of section 12.8 until the path publishes them (GAP-1069; ASM-2017).
- The blocking deviation codes per channel, the NSS result-code map, the LINE OA status map and the attempt limit are reference data or service configuration; the legacy names the retry limit as 5 and rule R-UNI-34 (GAP-1071; ASM-2019).
- The sender holds RW-CASEOWN or another role with Case record C, and the case is in the sender's scope; the right is declared at gateway-bff and refused with MSG-P4-002 or MSG-P4-003.
- No secret, phone number, LINE identifier or message body is written to a log, an event or a workflow input: the number and the identifier stay tokens (legacy section 17).

### 4. Flow

1. The case owner opens SCR-03 Case record through the gateway-bff composite route (DP-19) and chooses Send message, the channel (SMS or LINE), the template and the party.
2. gateway-bff declares the Case record right C, the scope and the session, and calls `POST /api/recovery/comms/v1/cases/{caseId}/messages` with an Idempotency-Key; a role without the right is refused there with MSG-P4-002.
3. rwb-comms: the idempotency store of schema `rwb_comms` is read for the key; a missing or non-UUID key is 400 MSG-PLT-N009-03; a key already answered for the same request replays the stored status and body and no second send is attempted; a key reused with another body or still in flight is 409 MSG-PLT-N009-05; an unreachable store is 503 MSG-PLT-N009-06; a stored answer is kept 24 hours.
4. rwb-comms: the case read of rwb-case is taken once (one hop, 2 s) for the legal hold and the deviation flag, and the active deviations are taken from the `DeviationRaised` and `DeviationCleared` state of the inbox when the case read degrades; a missing case answer refuses the send closed.
5. rwb-comms: the current template for the channel and the language is resolved from `template` (a current Approved version for LOV-CHANNEL `SMS` or `LINE`); a withdrawn template with no later Approved version is refused with MSG-P6-003.
6. rwb-comms: the conduct check runs — legal hold on the case, open deviation with contact stop, open deviation in the blocking list of the channel, and consent GIVEN on a verified contact point of that channel read once through the P1 contract: `GET /contact-points?personKey=&channel=` with `channel` `MOBILE` for an SMS message and `LINE` for a LINE message; a row passes only with `consentStatus` GIVEN (not WITHDRAWN or UNKNOWN) and a `verifiedAt` value.
7. rwb-comms: a failed check writes the decision record through the local library, appends the refusal to `POST /cases/{caseId}/interactions` as a `CONTACT` entry with `conductCheck` `BLOCKED` and answers 409 with MSG-P6-001, MSG-P6-002, MSG-P6-003 or MSG-P3-004; nothing is written to the outbox.
8. rwb-comms: a passed check merges the template and appends a `CONTACT` entry with `channel`, `direction` `OUTBOUND`, `conductCheck` `PASSED`, `deliveryStatus` `SENT`, the `contactKey` token and no `externalRef` to `POST /cases/{caseId}/interactions`; after the append answers 201 (or 200 for a business key already on the ledger) rwb-comms writes the send request to `outbox_event` in its own transaction (DP-09), because a REST append cannot join that transaction; the answer is 202 with the interaction.
9. The platform outbox relay (JOB-11, every minute) hands the outbox row to the P6 sender, which calls the ACE notification path with the contact point token, the template reference, the language and the case reference (INT-17 for SMS, INT-18 for LINE). No Temporal Schedule is registered by this story.
10. The ACE notification path returns an accepted reference; the sender appends a new `CONTACT` entry with that value as `externalRef` and `deliveryStatus` `SENT`, and moves the outbox row from queued to sent. The ledger is append-only: no entry is updated.
11. The ACE notification path reports the result for that reference — the NSS result code, or the LINE delivered and then read — and rwb-comms maps it to DELIVERED, READ or FAILED and appends one new `CONTACT` entry with the same `externalRef` and the later `occurredAt`; a FAILED result also posts the reference to `POST /contact-points/{contactPointKey}/failed-contacts`, which raises the failed count once for that (contact point, reference).
12. An unavailable path leaves the row queued for the next window; at the attempt limit of 5 the row moves to the exception state under R-UNI-34 and rwb-comms appends a `CONTACT` entry with `deliveryStatus` `FAILED`.
13. The case owner sees the message and its status on SCR-04 Case timeline, read from the P1 ledger entries through the case timeline route, where each entry with an `externalRef` carries `barcodeStatus`, the latest `deliveryStatus` of that reference; SCR-09 Exception queue lists the sends in the exception state.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case has an open X6 lost contact | Refused and logged | MSG-P6-001 | AC3, owned by RWB-ITG-E2022-ITG |
| X2 | An open deviation has the contact stop on | Refused and logged | MSG-P6-001 | AC4 |
| X3 | No consent GIVEN on the channel | Refused and logged | MSG-P6-002 | AC5, owned by RWB-ITG-E2022-ITG |
| X4 | The template is withdrawn | Refused | MSG-P6-003 | AC6, owned by RWB-ITG-E2022-ITG |
| X5 | NSS or LINE OA is unavailable | Queued and retried; after the attempt limit to the exception state, then the exception queue | MSG-GEN-006 | AC7, owned by RWB-ITG-E2022-ITG |
| X6 | NSS returns a failure code | Interaction FAILED; the contact point failed count raised through the P1 contract | None | AC8 |
| X7 | The same request with the same Idempotency-Key | One message only; the stored status and body are replayed | None | AC9 |
| X8 | The decision record cannot be written on a refusal | Nothing sent; the refusal is not completed; request refused; incident | MSG-P7-003 | AC10, owned by RWB-ITG-E2022-ITG |
| X9 | A legal hold is on the case | Refused and logged | MSG-P3-004 | AC11 |
| X10 | No channel given | Refused | MSG-GEN-001 | AC12, owned by RWB-ITG-E2022-ITG |
| X11 | The rwb-case case read does not answer inside the 2 s budget | The send is refused closed: no message leaves, no outbox row is written, and the caller is told the case could not be read; one entry records the degraded read | MSG-GEN-006 | AC11, ASM-2023 |
| X12 | The P1 contact point answer does not arrive inside the 2 s budget | The conduct check cannot answer PASSED, so the send is refused closed with MSG-GEN-006 and nothing leaves | MSG-GEN-006 | AC8, ASM-2018 |
| X13 | The P1 failed-count update fails after a FAILED result | The `FAILED` ledger entry stays and the count request is retried from the same delivery result with the same `Idempotency-Key` and body; the P1 operation counts one (contact point, reference) once through its `processed_event` row (RD-P1-070; NEW-GAP-S10-17 closed) and the inbox of `rwb_comms` absorbs a duplicate | None | AC8, ASM-2018 |
| X14 | The delivery result arrives for a reference rwb-comms does not know | The result is not applied and is kept for the exception count; no interaction is invented | None | AC2, GAP-1072 |
| X15 | A read of a message is asked for | There is no read operation for a message in the API specification of this module; the message and its status are read from the P1 interaction through the case timeline route | None | AC9, GAP-1070 |
| X16 | The ledger append of a passed check fails (503 MSG-P1-022) or does not answer inside the 2 s budget | The send is refused closed: no outbox row is written and nothing leaves; a retry uses the same business `idempotencyKey`, so an entry already written answers 200 | MSG-GEN-006 | AC18 |
| X17 | The ledger append of a refusal or of a delivery result fails (503 MSG-P1-022) | rwb-comms does not commit the action, or retries with the same header key and business `idempotencyKey`; no action is kept whose entry was not written. A refusal whose entry cannot be written is answered 503 and nothing is sent (RD-P1-064 rule 13, RD-P1-004) | MSG-GEN-006 | AC18 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against `RWB-P6-E2022-CON` and its fakes, the `rwb_comms` schema of RWB-P6-E1052-APP, and the two contract dependencies; the ACE notification path, the P1 contact point and the P3 case are stubs |
| Negotiable | Templates, blocking deviation codes, result-code maps and the attempt limit are data; the field names inside the P1 and path answers are settled with their owners |
| Valuable | Every SMS and LINE message is checked before it leaves, refused where a stop applies, and recorded with its delivery result |
| Estimable | One operation, one conduct check shared with letters, one outbox row, one result mapping, one screen action |
| Small | Fits one sprint with its tests, as the app slice of a legacy key split five ways |
| Testable | Each owned criterion runs with the ACE notification path, the P1 contact point and the P3 case stubbed at their documented answers |

### 7. Acceptance criteria

```gherkin
Feature: SMS and LINE dispatch through NSS and LINE OA

  Background:
    Given template "SMS-REMIND" "TH" version 1 with channel "SMS" is Approved and current
    Given template "LINE-REMIND" "TH" version 1 with channel "LINE" is Approved and current
    Given case "RC-2026-000777" is owned by "CO-0201" with borrower party "P-0077"
    Given case "RC-2026-000777" has no legal hold and no open deviation

  Scenario: AC2 LINE (legacy RWB-E2-022 AC2)
    Given party "P-0077" has a verified "LINE" contact point with consent "GIVEN"
    Given the rwb-source-data contract mock returns a verified "LINE" contact point for party "P-0077" with consent "GIVEN"
    When "CO-0201" sends a message with channel "LINE" and template "LINE-REMIND", and LINE OA reports it delivered and then read
    Then the case ledger holds separate CONTACT entries with channel "LINE" for SENT, DELIVERED and READ under one externalRef, the entry written at the check has conductCheck "PASSED", and the read answers barcodeStatus "READ"
    Then LINE OA received one message

  Scenario: AC4 Contact stop from a dispute (legacy RWB-E2-022 AC4)
    Given case "RC-2026-000777" has an open deviation "X1" with contact stop on
    Given the rwb-deviation contract mock returns the open deviation "X1" with contact stop on for case "RC-2026-000777"
    When "CO-0201" sends a message with channel "LINE"
    Then the response is status 409 with MSG-P6-001 naming "X1 Dispute or complaint"
    Then the system sends nothing to LINE OA
    Then the system appends one CONTACT entry with channel "LINE", direction "OUTBOUND" and conductCheck "BLOCKED" to POST /api/recovery/source-data/v1/cases/{caseId}/interactions
    Then one decision record is written in rwb-comms and no outbox row is written

  Scenario: AC8 NSS failure result (legacy RWB-E2-022 AC8)
    Given party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN" and failed count 0
    Given the rwb-source-data contract mock returns a verified "MOBILE" contact point for party "P-0077" with consent "GIVEN" and failed count 0
    When NSS returns result "FAILED" for the message
    Then a new CONTACT entry with deliveryStatus "FAILED" and externalRef "NSS-7781" is appended and no earlier entry is changed
    Then rwb-comms posts reference "NSS-7781", channel "SMS" and occurredAt to POST /api/recovery/source-data/v1/contact-points/{contactPointKey}/failed-contacts with a UUID Idempotency-Key
    Then the answer is 201 with failedCount 1 and counted true

  Scenario: AC9 Repeated request (legacy RWB-E2-022 AC9)
    Given the rwb-source-data contract mock returns a verified "MOBILE" contact point for party "P-0077" with consent "GIVEN"
    Given "CO-0201" sent a message with Idempotency-Key "c0ffee00-0000-4000-8000-000000000001"
    When the same request is sent again with Idempotency-Key "c0ffee00-0000-4000-8000-000000000001"
    Then the response is the stored 202 status and body of the first response
    Then NSS received one message

  Scenario: AC11 Legal hold (legacy RWB-E2-022 AC11)
    Given case "RC-2026-000777" has legal hold true
    Given the rwb-case contract mock returns case "RC-2026-000777" with legal hold true
    When "CO-0201" sends a message with channel "LINE"
    Then the response is status 409 with MSG-P3-004
    Then the system sends nothing to LINE OA

  Scenario: AC13 Rules with no criterion of their own (BR10 to BR14) (new, D-RCV-60)
    Given case "RC-2026-000777" has a route rule "R-RES-09" that raises an offer letter
    When the route rule raises the offer letter
    Then this operation sends nothing
    Then every send and result goes through the ACE notification path INT-17 and INT-18
    Then the interaction ledger and contact_point_ext are read and written only through the P1 contract
    Then each send and each refusal writes one decision record in the same transaction
    Then the REST base is "/api/recovery/comms/v1" with a 2 s timeout and an Idempotency-Key on the POST

  Scenario: AC14 Error answers 401, 403 and 404 of a provided operation (new, D-RCV-60)
    When a request without a valid credential is sent to a provided operation
    Then the response is status 401 with messageCode MSG-P4-001 as application/problem+json
    When a request by a user whose role lacks Case record C is sent to a provided operation
    Then the response is status 403 with messageCode MSG-P4-002
    When a request for a case that does not exist or is outside the caller's scope is sent to a provided operation
    Then the response is status 404 with messageCode MSG-P4-003

  Scenario: AC15 A consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-source-data contract mock does not answer the consumed call for party "P-0077"
    When "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND"
    Then the system sends nothing to NSS
    Then the response is status 503 with messageCode MSG-GEN-006 and no outbox row is written

  Scenario: AC16 A disallowed delivery status change is refused (new, D-RCV-60)
    Given the case ledger read answers barcodeStatus "DELIVERED" for externalRef "NSS-7781"
    When a delivery result "SENT" arrives for "NSS-7781"
    Then the change is refused and rwb-comms appends no entry
    Then the ledger read still answers barcodeStatus "DELIVERED"

  Scenario: AC17 A passed message is appended on the case-scoped ledger (new, RD-P1-007)
    Given the case id of "RC-2026-000777" is "c0000000-0000-4000-8000-000000000777"
    And the rwb-source-data fake returns a MOBILE contact point of party "P-0077" with consentStatus GIVEN and a verifiedAt value
    When "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND" and NSS accepts it with reference "NSS-7781"
    Then rwb-comms posts to /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000777/interactions with a UUID Idempotency-Key and eventCode "CONTACT", occurredAt, actorType "SERVICE", actorRef "rwb-comms", a sourceRef of at most 60 characters, an idempotencyKey starting "CONTACT-RC-2026-000777-", channel "SMS", direction "OUTBOUND", conductCheck "PASSED", deliveryStatus "SENT" and the contactKey token
    Then the append answers 201 before the outbox row is written, and the answer of the message request is 202
    Then the accepted reference is appended as a second entry with externalRef "NSS-7781", a new header key and a new business idempotencyKey
    Then no entry carries the message text, a mobile number or a LINE identifier

  Scenario: AC18 The ledger append fails and nothing is sent (new, RD-P1-007, RD-P1-004)
    Given the rwb-source-data fake answers the append with 503 and messageCode MSG-P1-022
    When "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND"
    Then the response is status 503 with messageCode MSG-GEN-006
    Then no outbox row is written and NSS receives no message

  Scenario: AC19 The shared idempotency answers of the message request (new, RD-P1-001)
    When the message request is sent with no Idempotency-Key header, or with a value that is not a UUID
    Then the response is status 400 with messageCode MSG-PLT-N009-03 and nothing is written
    When a key already used is sent with a different body, or while the first request is in flight
    Then the response is status 409 with messageCode MSG-PLT-N009-05 and the stored answer is unchanged
    When the idempotency store is unavailable
    Then the response is status 503 with messageCode MSG-PLT-N009-06 and nothing is sent

  Scenario: AC20 A contact point without a given consent is refused (new, RD-P1-005)
    Given the rwb-source-data fake returns the MOBILE contact point of "P-0077" with consentStatus UNKNOWN
    When "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND"
    Then the response is status 409 with MSG-P6-002
    Then a CONTACT entry with conductCheck "BLOCKED" is appended, one decision record is written and NSS receives nothing
```

AC2, AC4, AC8, AC9 and AC14 to AC16 are restated in version 3 for the append-only case-scoped ledger and the shared error and idempotency rules; AC17 to AC20 are new. TC: TC-P6-E2022-APP-05, TC-E2-022-24, TC-E2-022-25, TC-P6-E2022-APP-06, TC-P6-E2022-APP-07, TC-P6-E2022-APP-08, TC-P6-E2022-APP-09, TC-P6-E2022-APP-01, TC-P6-E2022-APP-02, TC-P6-E2022-APP-03, TC-P6-E2022-APP-04 (Test Cases v9).

The five criteria above are copied from legacy section 7 each tagged with its origin; version 3 restates the ledger assertions and the idempotency key value as the sentence above says. The cross-service line added inside a scenario is the mock of the owner's published contract with the same values the legacy line already fixed; no business value is added. AC1, AC3, AC5, AC6, AC7, AC10 and AC12 of the legacy key are owned by `RWB-ITG-E2022-ITG` and are not copied here. AC13 to AC16 are added by this story for BR10 to BR14, the error answers, a failed consumed call and a disallowed status change; they have no legacy origin.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every outbound message carries a conduct check result on its ledger entry | REQ-OCC-005; FEAT-OCC-05 |
| BR2 | No message is sent while a contact stop is in force | CTL-16; R-UNI-04, R-UNI-05 |
| BR3 | Deviation codes that block SMS and LINE are a reference list; X6 blocks both until a contact point is verified | R-DEV-16; R-UNI-12; Principle 1 |
| BR4 | Messages go only to a verified contact point with consent GIVEN for that channel | CTL-17; R-UNI-10 |
| BR5 | A legal hold stops every outbound action | R-UNI-20 |
| BR6 | A system that is unavailable queues the send and the platform retry and outbox mechanism retries it; after three retries (NFR-026; GAP-1600) it goes to the exception queue; this service names no schedule for notification retries (GAP-1601) | R-UNI-33, R-UNI-34, R-UNI-36; NFR-026; GAP-1600; GAP-1601 |
| BR7 | A refusal that cannot be written to the decision log is not completed | Principle 5; R-UNI-39 |
| BR8 | Only the current Approved template for the channel is used | R-LIT-03; CTL-14 |
| BR9 | The same request twice sends one message | R-UNI-40 |
| BR10 | A message raised automatically by a route rule — the offer letter of R-RES-09 — is sent by the rule's owning stage in Epic 3, never by this operation; this operation sends only on a person's request | R-RES-09; legacy section 19 |
| BR11 | No direct call to NSS or LINE OA: every send and every result goes through the ACE notification path (INT-17, INT-18); rwb-comms owns the call to that path for O03 and builds its own dispatch only if the ACE team confirms that no bank-wide service exists (DL30) | REQ-DRI-006; legacy section 17; DL30 |
| BR12 | The interaction ledger is rwb-source-data's (DP-18) and the contact point with its failed count is its `contact_point_ext`; rwb-comms reads and writes both only through the P1 contract and never touches `rwb_source_data`; the operations are those of rwb-source-data.yaml 5.1.0: the contact-point read, the failed-contact count and the append-only case-scoped ledger | DP-01, DP-05, DP-18 |
| BR13 | Every outbound message and every refusal writes one decision record through the local library in the same transaction, and a refusal that cannot be recorded is not completed | DP-03; R-UNI-39 |
| BR14 | One REST base per service — `/api/recovery/comms/v1` — one hop, a 2 s timeout and an Idempotency-Key on the POST; no business value, and no phone number, LINE identifier, message body or addressee, is carried in an event, a workflow input or a log | DP-11, DP-13; ADR-020; legacy section 17 |

The conduct and consent checks behind BR1, BR2 and BR4 are one versioned rule package governed in rwb-decision and evaluated by this service; the package name is Not specified in the source documents (GAP-1610).

### 9. State transitions

None in the case. This story changes no case status: the case state machine is rwb-case's and the deviation state machine is rwb-deviation's. It sets the conduct check — `PASSED` or `BLOCKED` — and the delivery status on the ledger entries it appends, and the message lifecycle on the outbox row.

| From | Event | Condition | To |
|---|---|---|---|
| no message | a send is requested on the case | the conduct check answers `PASSED` | QUEUED — the ledger entry is appended, then the outbox row is written |
| no message | a send is requested on the case | the conduct check answers `BLOCKED` | REFUSED — 409 with MSG-P6-001, MSG-P6-002, MSG-P6-003 or MSG-P3-004, no outbox row, one decision record |
| QUEUED | the platform relay hands the row to the sender | the ACE notification path accepts the request | SENT — a new ledger entry carries the accepted reference as `externalRef` |
| SENT | a result arrives for the reference | `DELIVERED` on SMS, or `DELIVERED` on LINE | DELIVERED |
| SENT | a result arrives for the reference | `READ` on LINE | READ |
| SENT | a result arrives for the reference | `FAILED` on either channel | FAILED — the contact point failed count rises by one through P1 |
| QUEUED | the retry window finds the path unavailable | the attempt count is below 5 | QUEUED — the next window retries |
| QUEUED | the retry window finds the attempt count at 5 | R-UNI-34 | EXCEPTION — the row is in the exception state and SCR-09 lists it, and a `FAILED` ledger entry is appended |

`SENT`, `DELIVERED`, `READ` and `FAILED` are the message values of this story. They are not LOV-DELIVERY, which keeps the WIN proof-of-delivery values (GAP-1076; ASM-2024).

### 10. Authority

The rights below are the Case record rights this story applies. The Case record area and right C are declared by the operation itself (API-P6-008, Case record C, scope applied); TSD P6 T6.1 is the only source used for the letters, and it declares two areas, Documents and Litigation, so the letter for each role is taken from its T6.1 row and the reconciliation of the Case record area is carried by GAP-1075.

| Who | Case record right used by this story | TSD P6 T6.1 row |
|---|---|---|
| RW-CASEOWN, case owner | C — sends a message on a case in scope | Documents CRU; Litigation R |
| RW-PHONECOL, phone collector | R only — the send is refused with MSG-P4-002 | Documents R; Litigation none |
| RW-FIELDCOL, field collector | C | Documents CR |
| RW-LITOFF, litigation officer | C (its T6.1 letters are CRUA) | Documents CRU; Litigation CRUA |
| RW-PLATADM, platform administrator | R only — the send is refused with MSG-P4-002 | Documents R; Litigation none |
| SY-DECLOG, decision record writer | Writes the refusal and the pass record through the local library; no case right, a service identity | T6.2 service identities |

The rwb-access authorise element (DP-08) is named here as the check on the composite route to SCR-03, declared at gateway-bff; no rwb-access guard library is wired in this story, and this story keeps a local guard on the refusal path that refuses closed when the right or the case answer is missing, including the legal hold and the open deviation with the contact stop (GAP-1075; ASM-2023). Refusals MSG-P4-002 and MSG-P4-003 are answered at gateway-bff. The authorise element is confirmed against RWB-P4-E1037-CON at contract review. No role in this story may grant itself a right.

### 11. Data

| BR Field ID | Entity | Field | Owner | Read or write |
|---|---|---|---|---|
| DF-REF-046, DF-REF-047, DF-REF-048, DF-REF-066, DF-REF-051 | template | template_code, template_version, language, channel, approved_by_legal | P6 (rwb_comms) | Read |
| DF-LEG-015, DF-LEG-016, DF-LEG-018 | notice | id, case_id, notice_type | P6 (rwb_comms) | Not read and not written by this story: a message produces no notice |
| DF-EXT-015 | contact_point_ext | consent_given | P1 (rwb_source_data) | Read through the P1 contract |
| DF-EXT-017 | contact_point_ext | verified_at | P1 (rwb_source_data) | Read through the P1 contract |
| DF-EXT-018 | contact_point_ext | failed_count | P1 (rwb_source_data) | Written through the P1 contract, never directly |
| DF-ACE-075, DF-ACE-077, DF-ACE-078 | contact point behind the P1 contract | contact_type, person_key, contact_value | P1 (rwb_source_data) | Read through the P1 contract as a token; the value never enters `rwb_comms` |
| DF-CAS-001, DF-CAS-020 | recovery_case | id, legal_hold | P3 (rwb_case) | Read through the P3 case read |
| DF-CAS-038, DF-CAS-043, DF-CAS-044 | deviation | deviation_code, contact_stop, cleared_at | S8 (rwb_deviation) | Read through the case read and the two deviation events |
| DF-INT-002 to DF-INT-006, DF-INT-011 to DF-INT-013, DF-INT-028, DF-INT-029 | interaction | case_id, person_key, occurred_at, channel, direction, summary, conduct_check, source_system, delivery_status, external_ref | P1 (rwb_source_data) | Written and read through the P1 contract only |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | the refusal and the pass record | P7 (rwb_decision) | Written through the local decision-record library (DP-03) |

`rwb_comms` holds no message table. The message, its template reference and its addressee are not persisted in `rwb_comms`: the interaction is rwb-source-data's and the content leaves the service inside the call to the ACE notification path. The one row this capability could write in its own schema is a `notice` row, and it writes none, because a message is not a notice. The record of a message for the case timeline is therefore the P1 interaction, which carries no template field (GAP-1077; ASM-2025). Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | API ID | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|---|
| POST | `/cases/{caseId}/messages` | API-P6-008 | `MessageRequest`: channel (SMS or LINE), template, language, party; field-level detail Not specified in the source documents (GAP-1073; ASM-2021) | 202 `Interaction`: interaction id, channel, direction, conduct check, delivery status, reference, plus the case and party identifiers | Case record C, scope applied | `Idempotency-Key` header (UUID), required; stored status and body replayed for 24 hours; 400 MSG-PLT-N009-03, 409 MSG-PLT-N009-05, 503 MSG-PLT-N009-06 |

Errors: 401 no session (message ID Not specified in the source documents (CG-ALL-6588)); 403 the role lacks Case record C (MSG-P4-002); 404 the case is outside the scope (MSG-P4-003); 409 a contact stop (MSG-P6-001), no consent (MSG-P6-002), a withdrawn template (MSG-P6-003) or a legal hold (MSG-P3-004); 422 a field is missing (MSG-GEN-001); 503 the decision record could not be written (MSG-P7-003).

There is no read operation for a message in the API specification of this module (T-A.1 lists API-P6-001 to API-P6-011 only). The message and its status are read through the P1 interaction on the case timeline route, and SCR-09 is fed by the exception state of the outbox rows (GAP-1078; ASM-2026).

#### 12.2 REST operations consumed

| Call | Owner | Use in this story |
|---|---|---|
| `GET /api/recovery/source-data/v1/contact-points?personKey=&channel=MOBILE` or `LINE` | P1 rwb-source-data | The rows `contactKey` (token), `contactType`, `consentStatus` (GIVEN, WITHDRAWN, UNKNOWN), `verifiedAt`, `failedCount`, `dataAsOf` for the conduct check; never a number or a LINE identifier; faked (rwb-source-data.yaml 5.1.0) |
| `POST /api/recovery/source-data/v1/contact-points/{contactPointKey}/failed-contacts` | P1 rwb-source-data | Body `reference`, `channel`, `occurredAt`, optional `caseId`; UUID `Idempotency-Key`; 201 with `contactKey`, `reference`, `failedCount`, `counted`; counts once for one (contact point, reference); faked |
| `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | Appends the passed, blocked and result entries as `CONTACT` entries with `InteractionRequest` 5.1.0: required `eventCode`, `occurredAt`, `actorType` SERVICE, `actorRef` `rwb-comms`, `sourceRef`, `idempotencyKey` `CONTACT-<caseNo>-<yyyyMMdd>-<actionId>`; UUID header; 201 new, 200 for an existing business key; an append writes no decision record; faked |
| `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | Reads `barcodeStatus` of an `externalRef` before a result is appended; faked |
| `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The legal hold and the deviation flag of the case; faked. Not in this story's Contract dependencies, so the fake is derived from the published P3 document (GAP-1075) |
| `GET` reference data for LOV-CHANNEL — the P3 reference-data contract of RWB-P3-E1043-CON | P3 rwb-case | `SMS` and `LINE` as data rows, never as values in code (DP-07); faked |
| `GET /api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The open deviation with its contact stop and its code, for the conduct check and for the refusal text; faked only, because the runtime path is the case read and the two deviation events (GAP-1075) |

`<actionId>` is the UUID of the rwb-comms record of that action and is the same on every retry (RD-P1-007 rule 4). Pending: which record gives it for the send, the refusal and each result, because rwb-comms holds no message table, owner solution architect (NEW-GAP-F15-3). Errors of rwb-source-data arrive as `application/problem+json` with `messageCode` (RD-P1-004).

Every row is one hop with a 2 s timeout and a breaker, and a GET is retried once with jitter (DP-11, ADR-020). The refusal's decision record is a write, not a read: it goes through the local decision-record library of the platform (DP-03, RWB-PLT-E1027-CON, owner P7 rwb-decision) in the same transaction as the refusal and is relayed as `DecisionRecorded` on `rwb.decision-record.v1` — see 12.3. This story reads no `rwb_source_data`, `rwb_case`, `rwb_deviation` or `rwb_decision` table (DP-01).

#### 12.3 Events published

| Event | Topic | Owner of the type | Payload (IDs and facts only) |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, the decision code (the deviation code on a refusal), the final call, the rule and its version where one applied, the case ID and the decided-at time; written by the local library in the same transaction and relayed by the outbox |

New `rwb.comms.*` events for this capability: None. Architecture v5 slide 17 names only `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered` on `rwb.comms.events.v1`, and a message is not a notice, so this story publishes no new comms event and adds none to the AsyncAPI document of the topic. The delivery status is carried to the timeline through the P1 interaction, not through a comms event.

#### 12.4 Events consumed

| Event | Topic | Owner | Element used |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | case ID, deviation code, raised at, the contact stop flag; keeps the blocking list of the case current when the case read degrades |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | case ID, deviation code, cleared at, outcome; releases the block |
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | case ID, previous and new state, the changed-at time; the consumer group of `rwb-comms` keeps the case projection the conduct check reads |

The three are consumed into the inbox of schema `rwb_comms` (`processed_event`), deduplicated by event ID, and each has its retry topic and its `.dlt` topic (DP-09). Their arrival is what lets the conduct check answer while the case read is degraded.

#### 12.5 Workflows and activities

None. The send is a synchronous REST request whose durability is the outbox row, and the retry is the platform relay's window; this story registers no workflow, no activity and no child workflow on task queue `rwb-comms`. The refusal is a transaction, not a workflow step.

#### 12.6 Schedules

None. JOB-11 Outbox sender is the platform's outbox relay, every minute, one owner for every service (Architecture v5 slide 44), and this story registers no Temporal Schedule, no cron entry and no job name. DP-10 is claimed because the legacy key's retry path is JOB-11 and the workflow kit is in the build dependency list; the send attempt itself is the P6 sender's code, called by the relay window. The legacy five-attempt limit and its exception-queue rule R-UNI-34 are applied inside that call (GAP-1071; ASM-2019).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| template | P6 (rwb_comms) | The current Approved version for a channel and a language |
| notice | P6 (rwb_comms) | Not written by this story: a message produces no notice |
| merge_field | P6 (rwb_comms) | The merge codes the template may use |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_comms | The send request, the inbox of the three consumed events and the stored answer of the POST |

Not owned and never written: `interaction` and `contact_point_ext` are P1's, `recovery_case` and `task` are P3's, `deviation` is S8's and `decision_log_entry` is P7's. rwb-comms holds no foreign key across services and no copy of a contact point, a case or a ledger entry (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock | rwb-source-data.yaml 5.1.0 fake: a ledger append answering 201, 200 on a repeated business key and 503 MSG-P1-022; a ledger read with `barcodeStatus`; a contact point with `consentStatus` UNKNOWN; a verified `MOBILE` contact point for `P-0077` with consent `GIVEN` and failed count 0 → 202; a `MOBILE` contact point with consent `WITHDRAWN` → the 409 path of MSG-P6-002; a verified `LINE` contact point with consent `GIVEN`; the failed-count update answering accepted, and a delayed answer beyond 2 s | AC2, AC4, AC8, AC9, AC11; the operations smoke profile |
| rwb-case WireMock | `GET /cases/{caseId}` for `RC-2026-000777` with legal hold false, then legal hold true; a case outside the scope; an answer delayed beyond 2 s | AC11 and the refusal-closed path of X11 |
| rwb-deviation WireMock | The open deviation `X1` with contact stop on for `RC-2026-000777`; the open deviation `X6`; an empty answer; a delayed answer beyond 2 s | AC4; the contract tests of RWB-P6-E2022-CON |
| decision-record library stub | A healthy chain and outbox, and a stopped chain for the 503 path of MSG-P7-003 | X8, and the contract tests |
| ACE notification path stub, NSS | An accepted reference `NSS-7781` with result `DELIVERED`, then a `FAILED` result; an `unavailable` answer for six attempts | AC8 and the exception state of section 9 |
| ACE notification path stub, LINE OA | An accepted reference, then delivered and then read (`DELIVERED`, `READ`) | AC2 |

The exact shapes of the ACE notification path are Not specified in the source documents (GAP-1069; ASM-2017); the P1 stubs follow rwb-source-data.yaml 5.1.0, the path stubs are derived from the legacy interface names, and each stub is replaced by its real owner as the wave 2 stories land.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | The send operation provided; the contact point, the failed-count update, the case read, the reference data and the deviation read consumed; one hop, 2 s |
| Kafka | 1 published, 3 consumed | `DecisionRecorded` published on the shared topic; `DeviationRaised`, `DeviationCleared` and `CaseStateChanged` consumed with retry and `.dlt` |
| Temporal | None | No workflow, no activity and no Schedule in this story; JOB-11 is the platform relay |
| File | None | Nothing is written to a file; the send is a REST call to the ACE notification path |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `messaging`, Java package `th.co.scb.ace.workbench.recovery.comms.messaging`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies as a prohibition as well as a permission: this story reads no ACE view and no ACE table, because the contact point arrives through the P1 contract as a token. DP-10 is claimed for the relay dependency only; no Schedule is registered here.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| MessageController | Controller | `POST /cases/{caseId}/messages`, validation and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| MessageService | Service | Template resolution, conduct check, merge, the ledger append to P1, then the outbox write in the local transaction |
| ConductCheckService | Service | The legal hold, the contact stop, the channel blocking list and the consent check; shared with the letter capability of RWB-P6-E2021-APP |
| TemplateResolver | Service | The current Approved template for the channel and the language from `template`, with the withdrawn case answered MSG-P6-003 |
| MessageSender | Service | The send attempt the relay window calls: the call to the ACE notification path, the accepted reference and the attempt counter |
| MessageResultMapper | Service | Maps the NSS result code and the LINE OA status onto DELIVERED, READ or FAILED and raises the failed count through P1 |
| IdempotencyStore | Repository | The stored answer of the POST under its key, in `idempotency_key` |
| ContactPointReader | Service | The P1 contract read of the contact point, its consent, its verified flag and its failed count |
| CaseFactsReader | Service | The P3 case read of the legal hold and the deviation flag, with the degraded answer refused closed |

**Database and migrations**

- Writes `outbox_event`, `processed_event` and `idempotency_key` in schema `rwb_comms`; reads `template` and `merge_field`.
- Migration in this story: `V2022_1__message_dispatch.sql` adds the index on `idempotency_key (key, created_at)` used by the stored-answer read and the index on `outbox_event (state, next_attempt_at)` used by the relay window. No table is created for a message.
- No row of `notice`, `interaction`, `contact_point_ext`, `recovery_case`, `deviation` or `decision_log_entry` is written by this story's migration, and none is written by its code except through the owners' contracts.

**Configuration and reference data**

- The blocking deviation codes per channel: X1, X2 and X3 when the contact stop is on, and X6 — data rows owned by the Conduct and QA officer, never values in code.
- The NSS result-code map to SENT, DELIVERED and FAILED, and the LINE OA status map to DELIVERED and READ — data rows owned by the data steward.
- The attempt limit of 5 and the exception-queue rule R-UNI-34 — service configuration read as data (GAP-1071; ASM-2019).
- The feature switch `rwb.comms.sms-line`, default off in DEV and on in SIT: off refuses the send closed with MSG-GEN-006 and sends nothing, and never allows a send by default.
- The login is the rwb-comms login (DP-02).

**Build steps**

1. MessageController and MessageService over the `RWB-P6-E2022-CON` document, with the idempotency store first; test AC9.
2. ConductCheckService with the legal hold, the contact stop, the blocking list and the consent check against the P1, P3 and deviation fakes; test AC4, AC11 and the refusal-closed paths of X11 and X12.
3. TemplateResolver with the current Approved rule and the withdrawn case; test the MSG-P6-003 path.
4. The refusal transaction: the decision record through the local library, then the `BLOCKED` entry appended to the P1 case-scoped ledger before the answer; test the MSG-P7-003 path.
5. MessageSender with the accepted reference, the attempt counter and the exception state at attempt 5; test the `unavailable` path against the path stub.
6. MessageResultMapper with the two maps as data the new ledger entry per result and the failed-count call through P1; test AC2, AC8 and AC16 to AC18.
7. The gateway-bff route behind SCR-03 and the timeline read of SCR-04 against the P1 fake; browser test of a send and of a refusal.
8. Contract-fake run of every cross-service answer in isolation, so the story builds before rwb-source-data, rwb-case and rwb-deviation are live in SIT.

**Feature switch.** `rwb.comms.sms-line`, read as service configuration; off refuses closed and allows nothing.

**Done when.** The tests in section 16 pass, the contract tests of `RWB-P6-E2022-CON` stay green, and a SIT week with the ACE notification path test profile shows one SMS and one LINE message to test numbers with their delivery status, every refusal message written once in the central decision ledger, and no phone number, LINE identifier or message body in a log, an event or a workflow input.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-001 | A contact stop applies | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | No consent for the channel | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P4-002 | The role lacks Case record C on the route | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Channel or template missing | Enter {field}. |
| MSG-GEN-006 | NSS or LINE OA is unavailable, or a consumed read does not answer in time | {system} is not available. Try again in a few minutes. |

The texts are copied unchanged from the legacy story; the {reason} of MSG-P6-001 is the deviation code and its name as the reference data holds them, and the {system} of MSG-GEN-006 is the name of the system that failed — `NSS`, `LINE OA` or the name of the consumed service.

### 15. Screens and states

SCR-03 Case record, states editable and Loading; empty, error and no access: Not specified in the source documents (CG-ALL-6594); the Send message action for roles with Case record C, with the channel, the template and the party, and the refusal message shown in place. SCR-04 Case timeline, states Loading and filtered; empty, error and no access: Not specified in the source documents (CG-ALL-6595): each message with its channel, its conduct check and its delivery status, read from the P1 interaction. The template is not shown until P1 adds a template reference to the interaction record. SCR-09 Exception queue, states Loading; empty, error and no access: Not specified in the source documents (CG-ALL-6596): the sends that failed after the retry limit of three (NFR-026; GAP-1600), one attempt per outbox relay window with the path's internal retries not counted, read by a P6 administrative read over the outbox rows in the exception state.

All three are gateway-bff composite routes (DP-19); this story provides the operation and the answer behind them and builds no screen of its own. No screen shows a phone number or a LINE identifier: the contact point is shown as its masked token. The template of a message is not stored anywhere in the target, so the timeline shows the channel, the conduct check and the delivery status and reads no template from a stored message (GAP-1077; ASM-2025).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-022-01 | AC1, BR1, BR4, BR8 | run by RWB-ITG-E2022-ITG | P-0077 MOBILE consent GIVEN; NSS stub reference NSS-7781 |
| TC-P6-E2022-APP-01 | AC2, BR4 | End to end | P-0077 LINE consent GIVEN; LINE OA stub delivered and read |
| TC-E2-022-03 | AC3, BR3 | run by RWB-ITG-E2022-ITG | Open X6 |
| TC-P6-E2022-APP-02 | AC4, BR2 | End to end | Open X1 with contact stop |
| TC-E2-022-05 | AC5, BR4 | run by RWB-ITG-E2022-ITG | MOBILE consent WITHDRAWN |
| TC-E2-022-06 | AC6, BR8 | run by RWB-ITG-E2022-ITG | SMS-REMIND TH v1 Withdrawn |
| TC-E2-022-07 | AC7, BR6 | run by RWB-ITG-E2022-ITG | Notification path stub unavailable for 6 attempts |
| TC-P6-E2022-APP-03 | AC8 | End to end | NSS result FAILED, failed count 0 |
| TC-P6-E2022-APP-04 | AC9, BR9 | End to end | Same Idempotency-Key twice |
| TC-E2-022-10 | AC10, BR7 | run by RWB-ITG-E2022-ITG | Open X6; decision log stubbed unavailable |
| TC-P6-E2022-APP-10 | AC11, BR5 | End to end | Legal hold true |
| TC-E2-022-12 | AC12 | run by RWB-ITG-E2022-ITG | No channel |
| TC-E2-022-13 | Access | Component | RW-PHONECOL sends POST /cases/{caseId}/messages; refused with MSG-P4-002 |
| TC-E2-022-14 | Principle 5 | NFR | Decision log write forced to fail on 10 refusals; none recorded as sent |
| TC-E2-022-15 | Section 12 operations, events and activities | Contract | Each operation, event and activity of section 12 checked against its published contract |
| TC-E2-022-16 | Section 12.7 tables | Boundary | Each table of section 12.7 written only by its owner; boundary limits Not specified in the source documents (DOR-RWB-P6-E2022-APP-12) |
| TC-E2-022-17 | BR10 | End to end | Route rule R-RES-09 raises an offer letter; this operation sends nothing |
| TC-E2-022-18 | BR11 | End to end | Every send and result goes through the ACE notification path INT-17, INT-18; no direct call to NSS or LINE OA |
| TC-E2-022-19 | BR12 | End to end | Interaction ledger and contact_point_ext read and written only through the P1 contract |
| TC-E2-022-20 | BR13 | End to end | Refusal and send each write one decision record in the same transaction; an unrecorded refusal is not completed |
| TC-E2-022-21 | BR14 | Contract | One REST base, 2 s timeout, Idempotency-Key on POST; no restricted value in an event, workflow input or log |
| TC-E2-022-22 | AC13, BR10 to BR14 | End to end | Route rule R-RES-09 raises an offer letter; ACE notification path, P1 contract, decision record and REST base checked |
| TC-P6-E2022-APP-05 | AC14 | Component | No valid credential; user without access to case RC-2026-000777; unknown caseId |
| TC-E2-022-24 | AC15 | NFR | rwb-source-data contract mock does not answer for party P-0077 |
| TC-E2-022-25 | AC16 | Component | Interaction with delivery status DELIVERED; result SENT recorded |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience to NFR. All fourteen legacy cases are kept here in their legacy order, and TC-E2-022-15 to TC-E2-022-25 are added for section 12, for BR10 to BR14 and for AC13 to AC16. Of the legacy cases, five (AC2, AC4, AC8, AC9, AC11) are owned by this story and the other seven are the same journey the integration story `RWB-ITG-E2022-ITG` proves with the `-ITG` suffix; the cases owned here run at End to end on this story's own stubs, and the `-ITG` copies are not here.

Version 3: rows that cite `TC-P6-E2022-APP-` identifiers are this story's rows of Recovery Workbench Test Cases v9. Where a shared legacy identifier now names another story's case there, this story's identifier replaces it, and cases run by one identifier are joined in one row.

### 17. Guardrails

- No business value in code: the blocking deviation codes, the result-code maps, the LINE status map, the attempt limit, the templates and the languages are data rows, reference data or service configuration read with their version.
- No personal data in events, workflow inputs, logs, tests or prompts. The mobile number, the LINE identifier, the message body and the addressee never appear in an event, a workflow input or a log: the contact point travels as a token, the ACE notification path detokenises it, and test data uses synthetic tokens and test numbers only.
- ACE data only through the owner's contract or the owner's `v_ace_*` views; this story reads no ACE table and no ACE view, because the contact point arrives through the P1 contract (DP-05).
- No cross-schema read and no cross-service write: the interaction ledger and the contact point with its failed count are P1's, the case is P3's, the deviation is S8's and the decision record is P7's; rwb-comms reaches each through its contract and holds no copy (DP-01, DP-05, DP-18).
- No direct call to NSS or LINE OA: every send and every result goes through the ACE notification path (REQ-DRI-006), and the stubs stand behind that path, never in front of it.
- The refusal and the pass record are written through the local decision-record library in the same transaction as the answer, and a refusal that cannot be recorded is not completed (R-UNI-39, DP-03).
- One REST base, one hop and a 2 s timeout: the operation is `/api/recovery/comms/v1/cases/{caseId}/messages`, the consumed calls carry the budget and a breaker, and no consumer is called twice for one decision (DP-11, DP-13, ADR-020).
- Only the current Approved template is used, and a withdrawn template with no later Approved version refuses the send; no template body is copied into code or into a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-004 | SMS and LINE through the bank's channel platforms, result on the case | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | R-UNI-33, R-UNI-34, R-UNI-40 | TC-E2-022-01, TC-P6-E2022-APP-01, TC-E2-022-06, TC-E2-022-07, TC-P6-E2022-APP-03, TC-P6-E2022-APP-04, TC-E2-022-12, TC-E2-022-13 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04, FEAT-OCC-05 | 06 to 10 Recovery case processes | R-UNI-04, R-UNI-05, R-UNI-20, R-DEV-16, R-UNI-39 | TC-E2-022-03, TC-P6-E2022-APP-02, TC-E2-022-10, TC-P6-E2022-APP-10, TC-E2-022-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-10 | TC-E2-022-05 |
| REQ-ILG-010 | Messages dispatched write their result to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-34 | TC-E2-022-01, TC-P6-E2022-APP-01, TC-P6-E2022-APP-03 |
| REQ-DRI-006 | No direct call to NSS or LINE OA; only the ACE notification path | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | No direct call to NSS or LINE OA; only the ACE notification path | TC-E2-022-01, TC-P6-E2022-APP-01, TC-E2-022-07 |
| RWB-E2-022 | The legacy key this story is split from, with AC2, AC4, AC8, AC9 and AC11 owned here and AC1, AC3, AC5, AC6, AC7, AC10 and AC12 owned by RWB-ITG-E2022-ITG | Legacy section 7 | FEAT-OCC-03, FEAT-OCC-04, FEAT-OCC-05, FEAT-OCC-06, FEAT-ILG-07 | 13 Manage documents and correspondence | BR1 to BR14 of section 8 | All fourteen legacy cases of section 16 and TC-E2-022-15 to TC-E2-022-25 |
| DP set | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 | Template and Rules §R5.5 | — | — | — | TC-E2-022-01, TC-P6-E2022-APP-03, TC-P6-E2022-APP-04 |
| ADR-013 | 19 services inside ACE, each with its own schema and login | Architecture v5 slides 20 and 41 | — | — | — | TC-E2-022-01 |
| ADR-014 | One schema and one login per service in ACE PostgreSQL | Architecture v5 slide 41 | — | — | — | TC-E2-022-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | Architecture v5 slides 22 and 42 | — | — | — | TC-P6-E2022-APP-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Template and Rules §R5.5, DP-11 | — | — | — | TC-E2-022-01, TC-E2-022-13 |

The supporting features FEAT-OCC-05 (the conduct check) and FEAT-OCC-06 (the block) are answered here only for SMS and LINE; the letter capability that shares the check is `RWB-P6-E2021-APP`.

### 19. Out of scope

- AC1, AC3, AC5, AC6, AC7, AC10 and AC12 of the legacy key, and the cross-service journey with its evidence: `RWB-ITG-E2022-ITG`.
- The contract baseline itself — the request and answer schemas, the refusal envelope, the status list, the event envelopes and the fakes as published artefacts: `RWB-P6-E2022-CON`.
- The deployment of the egress, the retry worker, the dashboards, the alerts and the runbook: `RWB-P6-E2022-OPS`.
- Notice generation and the letter capability that shares the conduct check: `RWB-P6-E1052-APP` and `RWB-P6-E2021-APP`.
- Letters through WIN, with their proof of delivery: `RWB-P6-E2021-APP` and `RWB-P6-E1055-APP`.
- The interaction ledger, the contact point, its consent and its failed count: rwb-source-data (`RWB-P1-E2022-APP`, `RWB-P1-E1066-CON`).
- The case record, its legal hold and the case timeline route: rwb-case (`RWB-P3-E1035-CON`).
- The decision ledger and its central copy: rwb-decision (`RWB-P7-E2022-APP`, `RWB-PLT-E1027-CON`).
- Messages sent automatically by route rules, for example the offer letter of R-RES-09 (Epic 3).
- The breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7).
- Self-service on LINE and HOME.SCB (FEAT-COM-01 to FEAT-COM-04, Epic 4).
- The NSS and LINE OA retries inside the ACE notification path, which are the path owner's and are proved by `RWB-ITG-E2022-ITG` (GAP-1071).

### 20. Remaining delivery steps

- Size the story: delivery lead with the squad.
- Sign off the epic design: solution architect.
- Mark RWB-P6-E2022-CON and RWB-P1-E1066-CON Done: contract owners.
- Publish the rwb-source-data.yaml 5.1.0 fake with the contact-point, count and ledger answers (NEW-GAP-S10-18): rwb-source-data contract owner.
- Load the DEV test data of case RC-2026-000777 and party P-0077: test data owner.
- Load the Case record C service-identity row of the rwb-comms workload identity (RD-P1-064 rule 2): security administrator.
- Settle the action record of the business key (NEW-GAP-F15-3): solution architect.
