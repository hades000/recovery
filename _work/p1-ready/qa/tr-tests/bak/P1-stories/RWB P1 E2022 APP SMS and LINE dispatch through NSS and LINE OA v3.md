# RWB-P1-E2022-APP SMS and LINE dispatch through NSS and LINE OA

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2022-APP |
| Work type | APP |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | To be sized by the squad at refinement (DOR-RWB-P1-E2022-APP-16) |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P1-X |
| Ready to start | Day 1, against fakes and stubs; Done needs the ledger writer of RWB-P1-E1066-APP merged |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E2022-CON, RWB-P1-E1066-CON |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), REST base `/api/recovery/source-data/v1` |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-009, RD-P1-011, RD-P1-045, RD-P1-070 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v2.md (FR-P1-001) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- Messages are appended and read on the case-scoped ledger `/cases/{caseId}/interactions` with `InteractionRequest` 5.1.0; the flat `/interactions` family is withdrawn (RD-P1-007). Finding #1.
- The two contact-point operations are added to rwb-source-data.yaml 5.1.0; idempotency, error body and status codes follow the shared rules (RD-P1-001, RD-P1-004, RD-P1-005). Finding #1.
- Prerequisites are stated as stubs and a Done condition. Finding #2. The retry wording is aligned to GAP-1600 (finding #3).
- The delivery columns already exist, so AC9 and X7 are withdrawn.
- RD-P1-070: a counted (contact point, reference) pair is a row of `processed_event`, so a reference counts once whatever the header key (AC4; NEW-GAP-S10-17 closed). Test case IDs follow Test Cases v9; message texts follow Error and Message Standard v6.
- ACs rewritten with uuid identifiers and keys, AC14 and AC15 added, test case references corrected. Findings #4, #5 are delivery and screen items.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-022 for rwb-source-data. The legacy story read the contact points and consent, ran the conduct check, merged the template, wrote the ledger entry, sent through the ACE notification path and took the result, all in one deployable. The send, the conduct check, the template, JOB-11 and the result listener move to rwb-comms (P6), the refusal record to rwb-decision (P7) and the access right to rwb-access (P4). This story keeps the two facts those slices stand on and the ledger they append to: the contact-point read over the service's own `v_ace_contact` and `contact_point_ext`, the failed count, and the message append with its delivery result on the ledger of RWB-P1-E1066-APP, folded on `external_ref` because that ledger is append-only (DP-05, DP-13, DP-18). No NSS or LINE OA call, no template read, no conduct check, no outbox sender and no decision-log write is built here. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2022-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 32 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the contact points of a party with their consent, verification and failed count to be answered by rwb-source-data, the count of a contact point to rise by one per failed message and to answer the same count on a repeat, and every outbound SMS and LINE message with its delivery result to be entries of this service's ledger folded on their external reference**, so that **the conduct check decides from facts it does not own, a failed attempt is counted once, and the delivery state of a message is a ledger fact rather than an update of a row**.

This is the rwb-source-data slice of legacy RWB-E2-022. It delivers four things:

- **the contact-point read**: `GET /contact-points?personKey=&channel=` on base `/api/recovery/source-data/v1` (DP-13), with `channel` `MOBILE` or `LINE`, one row per contact point with `contactKey` (a token, never the number and never the LINE identifier), `contactType`, `consentStatus`, `verifiedAt`, `failedCount` and `dataAsOf`;
- **the failed-count operation**: `POST /contact-points/{contactPointKey}/failed-contacts` with an `Idempotency-Key`, which raises `contact_point_ext.failed_count` once per (contact point, reference) and answers the new count;
- **the message append and its result**: `POST /cases/{caseId}/interactions`, the message as a `CONTACT` entry with `channel` `SMS` or `LINE`, `direction` `OUTBOUND`, `conductCheck`, `deliveryStatus` and `externalRef` (for example `NSS-7781`), and the later result as a second append with the same `externalRef`, because the ledger has no update path;
- **the read-back and the migration**: `GET /cases/{caseId}/interactions` answers the appends with `barcodeStatus`, the latest `deliveryStatus` of their `externalRef` (the fold of RWB-P1-E2021-APP); the migration adds the channel index and the count check on `contact_point_ext` and the external-reference index on `interaction`.

It owns none of the twelve legacy criteria: the send and its refusals are RWB-P6-E2022-APP's, the record RWB-P7-E2022-APP's, the right RWB-P4-E2022-APP's and the cross-service proof RWB-ITG-E2022-ITG's; its own criteria are new (GAP-2183; ASM-3534). That no contact-point read and no failed-count operation exist in the P1 inventory of TSD P1 T-A.1 is a Work Package ruling, not a source statement (GAP-2183; ASM-3535).

### 2. Business rationale

Collections reaches a customer on the channel the customer uses, and the consent that allows it and the quality of the contact point are Workbench decisions, not ACE facts. ACE holds the phone, e-mail and address records (INT-04, `v_ace_contact`); the Workbench holds consent and verification in `contact_point_ext` (FSD P1 A2.1.3.2; TSD P1 T3.5). Today the legacy message path reads that row, sends, counts and updates in one deployable, so a contact point that keeps failing is visible to nobody but the message code. Under D-RCV-60 rwb-comms decides and sends, and this service answers the consent, the verification and the count and keeps the ledger the outcome is written to (DP-01, DP-05, DP-18).

A count is useful only if it counts one thing once. The legacy step added one when NSS answered a failure; over REST the same result can be redelivered or replayed, and a count that rises on every redelivery never resets. The operation therefore raises the count once per (contact point, reference), so the count is the number of messages that failed and not the number of callers (R-UNI-40). The same reasoning decides the delivery state: the legacy code updated the entry, the target ledger is append-only, so the result is a second append and the state is the latest append folded on `external_ref` (DP-18).

**What D-RCV-60 changes.** No business value: the channels, the consent rule, the contact stop, the retry limit, the references and the count keep their meaning. What changes is ownership and reach - this service's own tables and views and its own REST base, one hop with a 2 s budget, instead of an in-process call into the monolith (DP-11, DP-13). A contact point stays an ACE record; this service adds only its decision about it and never copies the number or the LINE identifier (BR-P1-001-5; legacy guardrail 2).

### 3. Preconditions

Nothing here is a build dependency: the story is Day 1 and builds against published artefacts and one contract fake.

- RWB-P1-E1001-APP has published the baseline: schema `rwb_source_data`, the per-service Flyway sequence, and `contact_point_ext` with its seven business fields and the standard record columns (DP-01).
- The ledger append and case read of RWB-P1-E1066-APP (`Idempotency-Key` handling, case check, `tr_interaction_append_only`) are used and not rebuilt. Until that story is merged the append criteria run against its contract fake; this story is Done only against the real writer. The columns `delivery_status` and `external_ref` are already on `interaction` (Physical Schema v8).
- RWB-P1-E1069-APP's view contract is published and `recovery.v_ace_contact` is readable through the `rwb_source_data` login, which holds SELECT on the views and no privilege on `public` (DP-02, DP-05; ADR-010).
- RWB-P1-E1015-APP writes `data_product_load`; the DP02 stamp of the person's business date is readable for `dataAsOf`.
- The contact-point read and the failed-count operation are added to rwb-source-data.yaml 5.1.0 and RWB-P6-E2022-CON consumes them (C).
- `processed_event`, `idempotency_key` and `outbox_event` exist in `rwb_source_data` as platform library objects; the stored response of `idempotency_key` is what a repeat answers (DP-09).
- The channel values `MOBILE`, `LINE`, `SMS` and the delivery values `SENT`, `DELIVERED`, `READ`, `FAILED` are read through the reference-data client library of DP-07 with a fixture; TSD P1 T3.8 no longer lists LOV-CHANNEL for P1 (GAP-2183; ASM-3540).
- The caller is the rwb-comms service identity of the message slice with a workload identity token; the data steward reads the count with Platform administration R (TSD P1 T6.2).
- No approval is needed to build against a Draft contract baseline.

### 4. Flow

1. rwb-comms decides to send on case "RC-2026-000777" for party "P-0077" and asks for the party's contact points on the channel, one hop with a 2 s budget (DP-11; the decision is RWB-P6-E2022-APP's).
2. `GET /api/recovery/source-data/v1/contact-points?personKey=P-0077&channel=MOBILE` reads the party's `recovery.v_ace_contact` rows and joins `contact_point_ext` on `contact_key`; a row with no extension row answers `UNKNOWN`, an empty `verifiedAt` and count 0, and is never dropped (AC1).
3. `ConsentRenderService` renders `consent_given` true as `GIVEN`, false with a `consent_at` as `WITHDRAWN`, and no row as `UNKNOWN`; `dataAsOf` is the DP02 business date (AC1).
4. rwb-comms runs its conduct check and sends through the ACE notification path; NSS accepts with reference "NSS-7781" and returns "DELIVERED" (the send is RWB-P6-E2022-APP's; REQ-DRI-006 forbids a direct NSS call here).
5. rwb-comms posts the message to `POST /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000777/interactions` with its own UUID `Idempotency-Key` and the body of section 12.1 (a `CONTACT` entry, channel "SMS", direction "OUTBOUND", conduct check "PASSED", status "DELIVERED", reference "NSS-7781"); the append answers 201 (AC2; DP-18; RD-P1-007).
6. When the result changes - LINE reported delivered and then read - rwb-comms appends the later status with the same `externalRef`, a later `occurredAt`, a new header key and a new business key; the repository has no update method (AC3).
7. `GET /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000777/interactions` answers both entries as stored, each with `barcodeStatus` of "NSS-7781": the status of the latest `occurredAt`, the higher `caseSeq` winning a tie (AC3).
8. On a failure rwb-comms posts the reference to `POST /api/recovery/source-data/v1/contact-points/{contactPointKey}/failed-contacts`; the count rises once for that (contact point, reference): the counted pair is written to `processed_event` in the transaction of the increase (RD-P1-070), a repeat of the header key answers the stored response and a new header key for a counted reference answers the unchanged count with `counted` false (AC4, AC5).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `channel` or `personKey` missing or malformed, or `channel` not `MOBILE` or `LINE` | 400; nothing answered; the field is named | MSG-GEN-001; MSG-GEN-007 for a value not in its list | AC5 |
| X2 | The contact point has no row in `contact_point_ext` and none in `v_ace_contact` | 404; nothing written, and no count invented or created on the fly | MSG-P4-003 | AC5 |
| X3 | A repeat of the same `Idempotency-Key` with the same body | The stored answer; the count unchanged and no second row | None | AC4 |
| X4 | The same `Idempotency-Key` with a different body or path, or while the first request is in flight | 409; nothing written | MSG-PLT-N009-05 | AC7 |
| X5 | A second append of a result for one `externalRef` | A new entry; the earlier one unchanged and the read folds both | None | AC3 |
| X6 | `v_ace_contact` does not answer inside 5 s or errors | 503 naming the ACE database; nothing guessed from a cache | MSG-GEN-006 | AC8, AC11 |
| X7 | Withdrawn: the delivery columns exist in the baseline (Physical Schema v8) | Not used | None | None |
| X8 | A caller without the right | 403, logged without a token or a reference value | MSG-P4-002 | AC10, AC12 |
| X9 | No valid credential | 401 | MSG-P4-001 | AC13 |
| X10 | `Idempotency-Key` missing or not a UUID; the key store unavailable | 400; 503 | MSG-PLT-N009-03; MSG-PLT-N009-06 | AC7 |
| X11 | Flag `rwb.source-data.ledger-message` is off | The contact-point read and the failed-count operation answer 404 and nothing is written | Pending: message ID of the flag-off 404 (NEW-GAP-S10-01) | AC15 |
| X12 | The ledger cannot be written | 503; no entry | MSG-P1-022 | the writer's criteria in RWB-P1-E1066-APP |

X1 to X5 are legacy X6, X7 and X10 carried onto the split; the contact stop, consent, template and legal-hold refusals of legacy X1 to X4, X8 and X9 are raised by rwb-comms and rwb-decision and never reach this service (GAP-2183; ASM-3535). The 5 s statement timeout of X6 is the server limit and the 2 s budget is the caller's, so X6 is proved at the service. Pending: alignment of the two, owner solution architect (NEW-GAP-S10-02).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E2022-CON and its fake, the baseline, the view contract and the ledger writer; needs no live rwb-comms, rwb-deviation, rwb-decision or ACE database to start |
| Negotiable | The class split, the token format and the fold are the squad's choice behind the contract; the channels, the field list, the count rule and the append-only rule are fixed |
| Valuable | rwb-comms decides from facts it does not own, a failure is counted once, and the delivery state is history instead of an overwrite |
| Estimable | Two new operations, one extension of the ledger operations, one repository over one view and one table, one migration |
| Small | Finishes inside one sprint with its tests |
| Testable | Each criterion is one call against the contract fake and two fixtures, with no second service and no live NSS or LINE OA |
| Day 1 | No build dependency; reachable on the first day of wave 2 and tested against the baseline and the fake |

### 7. Acceptance criteria

```gherkin
Feature: SMS and LINE dispatch through NSS and LINE OA

  Background:
    Given case "c0000000-0000-4000-8000-000000000777" (case number "RC-2026-000777") is owned by "CO-0201" with borrower party "P-0077"
    Given the rwb-comms contract mock returns NSS reference "NSS-7781" with result "DELIVERED" for the message of case "RC-2026-000777"
    Given the rwb-comms contract mock returns the LINE result "DELIVERED" then "READ" for the message of case "RC-2026-000777"
    Given template "SMS-REMIND" "TH" version 1 with channel "SMS" and template "LINE-REMIND" "TH" version 1 with channel "LINE" are Approved and current in rwb-comms

  Scenario: AC1 The MOBILE contact point of P-0077 answers consent "WITHDRAWN" and failed count 0 (new, D-RCV-60)
    Given party "P-0077" has a verified "MOBILE" contact point with consent "WITHDRAWN" and failed count 0
    When rwb-comms calls GET /api/recovery/source-data/v1/contact-points?personKey=P-0077&channel=MOBILE
    Then the answer holds one row with contactType "MOBILE", consentStatus "WITHDRAWN", a verifiedAt time and failedCount 0
    Then the row carries the token of the contact point as its contactKey and no mobile number
    Then the answer carries a dataAsOf date and neither a case number nor a party name

  Scenario: AC2 The outbound SMS is appended as a CONTACT entry with conduct check "PASSED" and reference "NSS-7781" (new, D-RCV-60)
    Given party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN"
    When rwb-comms posts to /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000777/interactions with Idempotency-Key "c0ffee00-0000-4000-8000-000000000001" a body with eventCode "CONTACT", occurredAt 2026-12-15T10:00:00+07:00, actorType "SERVICE", actorRef "rwb-comms", sourceRef "MSG-SYN-0001", idempotencyKey "CONTACT-RC-2026-000777-20261215-9e000000-0000-4000-8000-000000000201", channel "SMS", direction "OUTBOUND", conductCheck "PASSED", deliveryStatus "DELIVERED", externalRef "NSS-7781" and the contactKey token
    Then the answer is 201 with one interaction holding those values and sourceSystem "WORKBENCH"
    Then one row is written, no decision record and no event is written, and no operation updates the row afterwards

  Scenario: AC3 The LINE message reaches "READ" through a second append folded on "NSS-7781" (new, D-RCV-60)
    Given the CONTACT entry of the case for reference "NSS-7781" carries channel "LINE", conduct check "PASSED", status "DELIVERED" and occurredAt 2026-12-15T10:00:00+07:00
    When rwb-comms appends for "NSS-7781" the status "READ" with occurredAt 2026-12-15T10:05:00+07:00, Idempotency-Key "c0ffee00-0000-4000-8000-000000000002" and a new business key
    And rwb-comms reads GET /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000777/interactions
    Then both entries of "NSS-7781" answer barcodeStatus "READ" and their own stored deliveryStatus
    Then the first entry still carries "DELIVERED" and was not changed

  Scenario: AC4 The failed count rises to 1 once and a repeat answers 1 (new, D-RCV-60)
    Given contact point "PHONE:PH-SYN-0077" of "P-0077" has consent "GIVEN" and failed count 0
    And the rwb-comms contract mock reports the final failed attempt of reference "NSS-7781" (retry policy of rwb-comms; GAP-1600)
    When rwb-comms posts to /api/recovery/source-data/v1/contact-points/PHONE:PH-SYN-0077/failed-contacts the reference "NSS-7781", channel "SMS" and occurredAt with Idempotency-Key "c0ffee00-0000-4000-8000-000000000001"
    Then the answer is 201 with the contactKey, failedCount 1 and counted true, and the row holds 1
    When the same request is sent again with Idempotency-Key "c0ffee00-0000-4000-8000-000000000001"
    Then the stored 201 answer is replayed and the row still holds 1
    When the same reference is posted with Idempotency-Key "c0ffee00-0000-4000-8000-000000000002"
    Then the answer holds failedCount 1 and counted false and the row still holds 1
    And processed_event holds one row with consumer "rwb-source-data.failed-contacts", an idempotency_key that starts "FC:" and is 67 characters long, and a null event_id

  Scenario: AC5 A missing channel and an unknown contact point are refused with nothing written (new, D-RCV-60)
    Given party "P-0077" has one verified "MOBILE" contact point with consent "GIVEN" and failed count 0
    When rwb-comms calls GET /api/recovery/source-data/v1/contact-points?personKey=P-0077 with no channel
    Then the answer is 400 with MSG-GEN-001 naming "channel"
    When rwb-comms posts a failure for contact point "PHONE:NO-SUCH-9988" with Idempotency-Key "c0ffee00-0000-4000-8000-000000000003"
    Then the answer is 404 with MSG-P4-003 and the count of every contact point of "P-0077" stays 0
    Then no interaction entry and no counted reference exists for "PHONE:NO-SUCH-9988"

  Scenario: AC6 No mobile number and no LINE identifier is stored or returned (new, D-RCV-60)
    Given the v_ace_contact fixture holds a mobile number and the LINE identifier of party "P-0077"
    When rwb-comms reads the contact points of "P-0077" for channel "MOBILE" and for channel "LINE"
    And rwb-comms appends the message of "NSS-7781" for case "RC-2026-000777"
    Then neither answer carries the number or the identifier, and each row carries its token only
    Then the ledger entry carries the token, the reference "NSS-7781" and no number
    Then no column of contact_point_ext and none of this story's migration holds a number or a LINE identifier

  Scenario: AC7 Key conflicts and a missing key are refused with nothing written (new, D-RCV-60)
    Given the failed-contact call with Idempotency-Key "c0ffee00-0000-4000-8000-000000000001" has been answered
    When the same operation is sent with Idempotency-Key "c0ffee00-0000-4000-8000-000000000001" and a different reference
    Then the answer is 409 with MSG-PLT-N009-05 and no failed count changes
    When it is sent without the header, and with the value "c0ffee00"
    Then each answer is 400 with MSG-PLT-N009-03 and nothing is written

  Scenario: AC8 A view that does not answer inside 5 s is refused with 503 naming the ACE database and nothing is guessed from a cache (new, D-RCV-60)
    Given the v_ace_contact view of party "P-0077" does not answer inside 5 s
    When rwb-comms calls GET /api/recovery/source-data/v1/contact-points?personKey=P-0077&channel=MOBILE
    Then the answer is 503 with MSG-GEN-006 naming the ACE database
    Then no cached contact point is returned

  Scenario: AC9 Withdrawn: the delivery columns exist in the baseline, so there is no missing-column case

  Scenario: AC10 A caller without the right is refused with 403 and the log holds neither the token nor the reference value (new, D-RCV-60)
    Given a caller holds no right to append a message in rwb-access
    When the caller posts a message to POST /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000777/interactions
    Then the answer is 403 with MSG-P4-002
    Then the log line holds neither the token nor the reference value

  Scenario: AC11 The view v_ace_contact of party "P-0077" errors and is refused with 503 naming the ACE database, and nothing is guessed from a cache (new, D-RCV-60)
    Given the v_ace_contact view of party "P-0077" returns an error
    When rwb-comms calls GET /api/recovery/source-data/v1/contact-points?personKey=P-0077&channel=MOBILE
    Then the answer is 503 with MSG-GEN-006 naming the ACE database
    Then no cached contact point is returned

  Scenario: AC12 A caller without the right to read contact points is refused with 403 and the log holds neither the token nor the contact value (new, D-RCV-60)
    Given a caller holds no right to read contact points in rwb-access
    When the caller calls GET /api/recovery/source-data/v1/contact-points?personKey=P-0077&channel=MOBILE
    Then the answer is 403 with MSG-P4-002
    Then the log line holds no token and no contact value

  Scenario: AC13 A request with no credential is refused with 401 and a caller without the right is refused with 403 on each operation (new, D-RCV-60)
    Given requests to GET /api/recovery/source-data/v1/contact-points, POST /api/recovery/source-data/v1/contact-points/{contactPointKey}/failed-contacts, POST /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000777/interactions and GET /api/recovery/source-data/v1/cases/c0000000-0000-4000-8000-000000000777/interactions
    When each of the four is called without a credential, and then by a caller holding no right in rwb-access
    Then the answer is 401 with MSG-P4-001 on each and no row is returned or written
    Then a caller without the right is answered 403 with MSG-P4-002 on each

  Scenario: AC14 Two concurrent failures of one reference count once (new, D-RCV-60)
    Given contact point "PHONE:PH-SYN-0077" has failed count 0
    When two requests for reference "NSS-7781" with different Idempotency-Keys run at the same time
    Then the stored count is 1, one answer has counted true and the other counted false

  Scenario: AC15 With the flag off the contact operations are not served (new, D-RCV-60)
    Given flag "rwb.source-data.ledger-message" is off
    When the contact-point read and the failed-count operation are called
    Then each answers 404, no view is read and nothing is written

```

**Target reading.** Every assertion is new, because this story owns no legacy criterion, and each tests only the read, the count and the ledger; the legacy values are kept (case RC-2026-000777, owner CO-0201, party P-0077, templates SMS-REMIND and LINE-REMIND TH version 1, reference NSS-7781, consent GIVEN and WITHDRAWN, count 0 to 1, retry limit 5, key c0ffee00-0001, channels MOBILE, LINE and SMS, conduct check PASSED). AC1 answers the consent fact of legacy AC5 without refusing anything, which is rwb-comms' decision (REQ-OCC-006; CTL-17); the three rendered values are the reading of TSD P1 T3.5 (GAP-2183; ASM-3536). AC2 fixes the entry as `CONTACT` with the two delivery columns on the case-scoped append (GAP-2183; ASM-3538; RD-P1-007). AC3 replaces the legacy update with an append and a fold (GAP-2183; ASM-3538). AC4 counts one failed message once (R-UNI-40); its relation to the "consecutive" wording of the FSD is not settled by a source (GAP-2183; ASM-3539). AC5 fixes the refusal set of the two writes, which no source states (GAP-2183; ASM-3535). AC6 asserts the legacy guardrail instead of assuming it. The message outcome is held as an entry of the interaction ledger of RWB-P1-E1066-APP, read back through GET /cases/{caseId}/interactions; no table of rwb_comms holds a message (GAP-1599).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every outbound message carries a conduct check result on its ledger entry | REQ-OCC-005; FEAT-OCC-05 |
| BR2 | No message is sent while a contact stop is in force | CTL-16; R-UNI-04, R-UNI-05 |
| BR3 | Deviation codes that block SMS and LINE are a reference list; X6 blocks both until a contact point is verified | R-DEV-16; R-UNI-12 |
| BR4 | Messages go only to a verified contact point with consent GIVEN for that channel | CTL-17; R-UNI-10 |
| BR5 | A legal hold stops every outbound action | R-UNI-20 |
| BR6 | A system that is unavailable queues the send and retries; after the limit it goes to the exception queue | R-UNI-33, R-UNI-34, R-UNI-36 |
| BR7 | A refusal that cannot be written to the decision log is not completed | Principle 5; R-UNI-39 |
| BR8 | Only the current Approved template for the channel is used | R-LIT-03; CTL-14 |
| BR9 | The same request twice sends one message; here, one failure of one reference raises the count by one | R-UNI-40 |

**Where each rule lives.** BR1 is a field of the append: rwb-comms sends the result it computed and this story stores it; no conduct check runs here (DP-18). BR2, BR3, BR5, BR7 and BR8 belong to rwb-comms, rwb-deviation, rwb-case, rwb-decision and rwb-comms' template table. BR4 is split: this story answers `consentStatus` and `verifiedAt` as facts and the decision to send is rwb-comms' (DP-05). BR6 is the caller's retry: the limit of three retries (NFR-026; GAP-1600) sits on JOB-11, read as the platform retry and outbox mechanism of rwb-comms (GAP-1601); the limit of 5 quoted elsewhere in this story is the functional specification's wording, owned by rwb-comms, and this story counts only the failure it is told about (GAP-2183; ASM-3539). BR9 is the `Idempotency-Key` of both writes, answered from the stored response and never from a second write (DP-09).

### 9. State transitions

None in the case model: this story changes no case status, creates no case and reads no case. It changes one counter and adds ledger entries; the delivery state of a message is derived from its appends and never stored as a mutable state.

| From | Event | Condition | To |
|---|---|---|---|
| a contact point at count n | a failed-contact call | The contact point resolves and the key is new | At n+1 and the answer carries n+1 |
| a contact point at count n | a repeat of the key, or a second call for the same reference | The reference is already counted | At n and the answer carries n |
| a contact point at count n | a failed-contact call | The contact point does not resolve | Nothing written; 404 |
| a message with no entry | the first append | The case check answers and the body validates | One `CONTACT` entry with the status given |
| a message at DELIVERED | a second append with the later status | A new header and business key, the same `externalRef`, a later `occurredAt` | A second entry at READ or FAILED; the first unchanged |
| a message with two entries | the case read | The reference is folded | `barcodeStatus` is the latest status |

The four delivery values are reference data through the client library and never written in code (DP-07; legacy section 9).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-comms service identity, with a workload identity token | Reads the contact points, posts a failed contact, appends a message and its result, and reads the case ledger (Case record C or R on the case) |
| The rwb-source-data service identity | Reads `v_ace_contact` and the DP02 stamp; writes `contact_point_ext` and `interaction` in its own schema; no privilege outside it |
| RW-DATASTEW, data steward and data product owner | Reads the count answer of a contact point (Platform administration R) |
| RW-CONDUCT, Conduct and QA officer | Reads blocked-contact evidence through the rwb-comms read, not through this story |
| RW-PLATADM, platform administrator | Reads a refused call and its problem body |

No credential and no personal value appears in an answer, a log line or a test. Roles and rights are data in rwb-access (DP-01; TSD P1 T6.2). Each operation of §12 calls a rwb-access check of the caller's right before it answers; the check's name is Not specified in the source documents (DOR-RWB-P1-E2022-APP-6).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-075 | v_ace_contact | contact_type | Read (token prefix) |
| DF-ACE-076 | v_ace_contact | contact_key | Read (the token; never copied) |
| DF-ACE-077 | v_ace_contact | person_key | Read |
| DF-ACE-078 | v_ace_contact | contact_value | **Not read**; the number and the identifier stay in ACE |
| DF-ACE-080 | v_ace_contact | usage_code | Read (makes a PHONE row a MOBILE contact point) |
| DF-EXT-013 | contact_point_ext | contact_key | Read and write (the token) |
| DF-EXT-015 | contact_point_ext | consent_given | Read |
| DF-EXT-016 | contact_point_ext | consent_at | Read |
| DF-EXT-017 | contact_point_ext | verified_at | Read |
| DF-EXT-018 | contact_point_ext | failed_count | Read and write (the counter) |
| DF-OPS-002 | data_product_load | product_code | Read (the DP02 stamp) |
| DF-OPS-004 | data_product_load | business_date | Read (the DP02 stamp) |
| DF-OPS-007 | data_product_load | status | Read (the DP02 stamp) |
| DF-INT-002 | interaction | case_id | Write |
| DF-INT-003 | interaction | person_key | Write |
| DF-INT-004 | interaction | occurred_at | Write |
| DF-INT-005 | interaction | channel | Write (SMS or LINE) |
| DF-INT-006 | interaction | direction | Write (OUTBOUND) |
| DF-INT-011 | interaction | summary | Write (channel and reference only; no content) |
| DF-INT-012 | interaction | conduct_check | Write (the value rwb-comms computed) |
| DF-INT-013 | interaction | source_system | Write |
| DF-INT-014 | interaction | event_code | Write (CONTACT) |
| DF-INT-022 | interaction | contact_key | Write (the token reached) |
| DF-INT-028 | interaction | delivery_status | Write (existing column) |
| DF-INT-029 | interaction | external_ref | Write (existing column) |

Field IDs are those of the LDM and the data dictionary. `tr_interaction_append_only` is not a field and is not a row of this table; it is the database trigger of RWB-P1-E1066-APP. Every `DF-ACE-` row is read in this service's own `recovery.v_ace_contact` and never from a `public` table, and `contact_value` is not selected, so the number and the LINE identifier never leave ACE (DP-01, DP-05; BR-P1-001-5). `contact_point_ext` is this service's extension table and the only place consent and the count live (TSD P1 T3.5). The `DF-INT-` rows are the ledger this service owns (DP-18); the stored types of the two delivery columns are a target choice (GAP-2183; ASM-3538).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13). RWB-P6-E2022-CON declares the shapes the message path consumes and this story implements them.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/contact-points` | The contact points of one party on one channel: `contactKey` token, `contactType`, `consentStatus`, `verifiedAt`, `failedCount`, `dataAsOf` | The rwb-comms service identity; Platform administration R for the count | Derived from the view and the extension row on every call |
| POST | `/contact-points/{contactPointKey}/failed-contacts` | Raises `failed_count` once for one (contact point, reference) and answers the new count | The rwb-comms service identity | `Idempotency-Key` required, kept 24 hours; same key and body answers the stored count |
| POST | `/cases/{caseId}/interactions` | Appends one message as a `CONTACT` entry; 201 new, 200 for an existing business key | Case record C on the case; the rwb-comms service identity | Header `Idempotency-Key` (UUID); body `idempotencyKey` as business key |
| GET | `/cases/{caseId}/interactions` | The case ledger; each entry with an `externalRef` also carries `barcodeStatus` | Case record R on the case | Idempotent read |

The answer is `ContactPointAnswer` (`personKey`, `channel`, `asOf`, `rowCount`, `rows` of `ContactPointRow`); the failed-contact request and answer are `FailedContactRequest` (`reference`, `channel`, `occurredAt`, optional `caseId`) and `FailedContactAnswer` (`contactKey`, `reference`, `failedCount`, `counted`); the append body is `InteractionRequest` 5.1.0 (RD-P1-007 rule 3): required `eventCode` (`CONTACT`), `occurredAt`, `actorType` (`SERVICE`), `actorRef` (`rwb-comms`), `sourceRef` (the message record reference, at most 60), `idempotencyKey` (form `<code>-<caseNo>-<yyyyMMdd>-<actionId>`, `CONTACT` and the message record UUID when the action has no event); also `channel` (`SMS` or `LINE`), `direction` (`OUTBOUND`), `conductCheck`, `deliveryStatus`, `externalRef`, `contactKey` and `summary` without message content. The read answers `InteractionPage` with `barcodeStatus` (RWB-P1-E2021-APP). Property names are a target choice; the field list is fixed by section 11. The paths, the parameters and the error set are in no source document: TSD P1 T-A.1 lists API-P1-001 to API-P1-016 and none reads a contact point or counts a failed contact, and the legacy interface was an in-process method with no path and no status code (GAP-2183; ASM-3535).

Errors are `application/problem+json` with the shared `Problem` schema (RD-P1-004): 400 MSG-GEN-001, MSG-GEN-007 or MSG-PLT-N009-03; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003 for an unknown contact point and for a case out of scope; 409 MSG-PLT-N009-05; 422 MSG-GEN-001 or MSG-GEN-007 for a body member; 503 MSG-GEN-006 for the view, MSG-PLT-N009-06 for the key store, MSG-P1-022 for the ledger. Build contract: rwb-source-data.yaml 5.1.0.

#### 12.2 REST operations consumed

None at run time. The conduct check, the template, the send and the result arrive as values on the request; the case check of an append is the writer's call to rwb-case (RD-P1-007 rule 5); the channel and delivery values come through the reference-data client library of DP-07 (GAP-2183; ASM-3540). The C binding is the caller's contract RWB-P6-E2022-CON, faked for these tests.

#### 12.3 Events published

None of its own. The topic is `rwb.source-data.events.v1` with names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP. A message is a ledger entry, not an event; the events of the message path are rwb-comms' on `rwb.comms.events.v1`.

#### 12.4 Events consumed

None. rwb-comms reaches these operations over REST after it has computed the conduct check and after the notification path answered; a topic reader here would create a second reader and a second writer of the same reference (DP-09).

#### 12.5 Workflows and activities

None. The operations are synchronous REST steps with a 2 s budget. The queue `rwb-source-data` in namespace `rwb-recovery` belongs to the other P1 stories; JOB-11 is rwb-comms' (DP-10).

#### 12.6 Schedules

None. The count is raised by the caller when a result arrives and at no fixed time (DP-10).

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `contact_point_ext` | `rwb_source_data` | P1 rwb-source-data | The consent, the verification and the count; the migration adds `person_key`, `ix_contact_point_ext_person_channel (person_key, contact_type)`, the non-negative check and the default 0; no row is created for an unknown contact point |
| `interaction` | `rwb_source_data` | P1 rwb-source-data (DP-18; shape of RWB-P1-E1066-APP) | The migration adds `ix_interaction_external_ref (source_system, external_ref)` only; `delivery_status` and `external_ref` already exist; this story appends through the writer and never updates or deletes |
| `v_ace_contact` | `recovery` | ACE, through the view contract of RWB-P1-E1069-APP | SELECT only, never copied; `contact_value` is not selected (DP-05; ADR-010) |
| `v_ace_customer` | `recovery` | ACE, through the same contract | SELECT only, to resolve the party behind `personKey` |
| `data_product_load` | `rwb_source_data` | P1, written by RWB-P1-E1015-APP | Read for the DP02 business date; no row is written here |
| `processed_event`, `idempotency_key`, `outbox_event` | `rwb_source_data` | Platform library objects | The stored response of the two writes is the library's; `processed_event` also holds one row per counted (contact point, reference) under consumer `rwb-source-data.failed-contacts` (RD-P1-070); no event is published (DP-09) |

No table of another service is read and no foreign key crosses a schema (DP-01). `recovery_case`, `deviation`, `template`, `notice` and `decision_log_entry` are never named in this story's code or tests.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Provider fake of rwb-source-data.yaml 5.1.0, path `fakes/rwb-source-data/5.1.0/` | The two contact operations and the ledger append and read, for rwb-comms | One mapping per documented status; "NSS-7781" delivered for SMS, "DELIVERED" then "READ" for LINE, a counted and an uncounted failure. Pending: the P1 contract story that lists this fake (NEW-GAP-S10-18) |
| ACE contact fixture | `v_ace_contact` and `v_ace_customer` | One MOBILE contact point of P-0077 with a number, one LINE contact point with an identifier, one contact point with no extension row, one party with no contact row, the DP02 business date |
| `contact_point_ext` fixture | `rwb_source_data` | Consent GIVEN and WITHDRAWN with `consent_at`, a `verified_at`, count 0, one contact point with no row |
| Ledger fixture | `rwb_source_data` | The migration of RWB-P1-E1066-APP and this version, with the unique keys and the trigger, so AC2, AC3 and the repeat of AC4 run on the real keys |

All four are local: no live service, NSS, LINE OA or ACE database is needed for section 16.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 new operations and the ledger append and case read on `/api/recovery/source-data/v1` | rwb-case case read, by the writer | OpenAPI 3.1; one hop, 2 s, breaker per client (DP-11) |
| Kafka | None | None | The topic and both events belong to RWB-P1-E1015-APP; the message events to rwb-comms (DP-14) |
| Temporal | None | None | No workflow, activity or Schedule; JOB-11 is rwb-comms' (DP-10) |
| File | None | None | No file is read or written |
| SQL view | None | 2 views of `recovery`, SELECT only | In process, read-only login, 5 s statement timeout (DP-05; ADR-010) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `contact`, types in `...sourcedata.api`. Base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), queue `rwb-source-data` (not used here). The build starts on Day 1 against four published artefacts and no build dependency.

| Component | Type | Responsibility |
|---|---|---|
| `ContactPointController` | Controller | The read and the failed-contact operation of 12.1, the problem details and the key |
| `ContactPointReadService` | Service | One row per contact point: token, type, consent, verification, count and business date |
| `ConsentRenderService` | Service | `consent_given` and `consent_at` to `GIVEN`, `WITHDRAWN` or `UNKNOWN`, with no value in code (DP-07) |
| `FailedCountService` | Service | The raise once per (contact point, reference), the stored answer and the refusal of an unknown contact point |
| `InteractionWriteController` and writer (RWB-P1-E1066-APP) | Existing | The `CONTACT` entry with its delivery fields, the case check and the 201 |
| `BarcodeStatusFold` (RWB-P1-E2021-APP) | Existing | `barcodeStatus` of an `externalRef` on the case read |
| `ContactPointRepository`, `InteractionRepository` | Repository | SELECT over the view; read and increment of `contact_point_ext`; insert and read of `interaction`; no update and no delete method (DP-18) |

**Migration.** On this service's own Flyway sequence, after the ledger version, at the next free version at merge, in schema `rwb_source_data`; an applied version is never edited (DP-01). It carries `person_key varchar(255)` on `contact_point_ext` (a business key with no foreign key, BR-P1-001-3), `ix_contact_point_ext_person_channel (person_key, contact_type)`, `failed_count` as `NOT NULL DEFAULT 0` with `failed_count >= 0`, and on `interaction` the index `ix_interaction_external_ref (source_system, external_ref)`. The columns `delivery_status` and `external_ref` already exist (Physical Schema v8) and are not added (GAP-2183; ASM-3538). Rollback is by flag and a forward migration only (RD-P1-045). The counted references need no table and no migration: each is a row of `rwb_source_data.processed_event` with `consumer` `rwb-source-data.failed-contacts`, `idempotency_key` `FC:` followed by the lowercase hex SHA-256 of `<contactPointKey>|<reference>` (67 characters) and `event_id` null. The row and the `failed_count` increase are written in one transaction; a repeat finds the row, raises `hit_count` by 1, leaves `failed_count` unchanged and answers 201 with `counted` false (RD-P1-070; NEW-GAP-S10-17 closed).

**Configuration and reference data**

- The channel and delivery values are read through the reference-data client library with a fixture; TSD P1 T3.8 lists neither list for P1 (GAP-2183; ASM-3540).
- The channel to contact-type mapping is configuration: `MOBILE` is a `PHONE` row with a mobile `usage_code`, and `LINE` is the `PHONE` row the party uses for LINE OA, because the view has no LINE branch and `contact_type` is PHONE, EMAIL or ADDRESS (GAP-2183; ASM-3537).
- The token is `contact_type:key` of the ACE row, derived on every read (DF-ACE-076).
- The `Idempotency-Key` is kept 24 hours, the legacy value of RWB-E2-022 section 12; the 2 s budget and the 5 s statement timeout are configuration (DP-11).
- The count rule is one per (contact point, reference); the retry policy belongs to JOB-11 of rwb-comms: GAP-1600 uses the platform limit of three retries (NFR-026), to be confirmed by the solution architect, and keeps the legacy limit of 5 only as source text (GAP-2183; ASM-3539).

**Build steps**

1. The types and the fragment of 12.1 in rwb-source-data.yaml 5.1.0, with the provider fake.
2. The migration of the index and check (AC4, AC14).
3. `ContactPointRepository` and `ContactPointReadService`: the one-party, one-channel read, the join, the token and the DP02 business date (AC1, AC6).
4. `ConsentRenderService` and the reference-data client, so the values are data and not constants (AC1).
5. `FailedCountService`: the raise in one transaction, the stored answer, the 404 and the check constraint (AC4, AC5).
6. The `CONTACT` append through the writer of RWB-P1-E1066-APP (AC2, AC3).
7. The `barcodeStatus` check of both entries on the case read (AC3).
8. The error paths and an architecture test that no class updates an `interaction` row, selects `contact_value`, or names `recovery_case`, `deviation`, `template`, `notice` or `decision_log_entry` (AC3, AC6; X1, X2, X4, X6).

**Feature flag.** `rwb.source-data.ledger-message`. Off, the contact-point read and the failed-count operation answer 404 and nothing is written, so the message path has no contact facts and is held; the ledger operations behave as before this story (RD-P1-045).

**Done when.** The tests in section 16 pass; the migration is applied; the MOBILE contact point of P-0077 answers consent WITHDRAWN and count 0; the message of NSS-7781 answers 201 with conduct check PASSED and status DELIVERED; a second append folds to READ while the first keeps DELIVERED; the count reaches 1 once; a missing channel and an unknown contact point are refused with nothing written; and no answer carries a number or a LINE identifier.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required value is missing or malformed | Enter {field}. |
| MSG-P4-001 | No valid credential (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-GEN-007 | `channel` not in its list | As Error and Message Standard v6 |
| MSG-PLT-N009-03, -05, -06 | Idempotency key missing, conflicting, or the store down | As Error and Message Standard v6 |
| MSG-P1-022 | The ledger cannot be written | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P4-002 | A caller without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | An unknown contact point, or the case of an append unknown or out of scope | This case is not in your scope. |
| MSG-GEN-006 | A view does not answer inside 5 s or errors | {system} is not available. Try again in a few minutes. |

The refusals of the message path itself are rwb-comms' and never reach this service; their texts are kept unchanged: **MSG-P6-001** for a contact stop on X6 Lost contact or X1 Dispute or complaint, **MSG-P6-002** for a channel without consent, **MSG-P6-003** for a withdrawn template, **MSG-P3-004** for a legal hold, **MSG-P7-003** when a refusal cannot be recorded, and **MSG-GEN-006** when NSS or LINE OA is unavailable, after which JOB-11 retries and, after the limit of 5, the send goes to the exception queue under R-UNI-33 and R-UNI-34. This story raises MSG-GEN-006 for its own view and database failures and nothing else from that list. The 404 of an unknown contact point is MSG-P4-003 (RD-P1-004). Thai text follows DL10, which stays open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive. No message carries a name, an identity number, a phone number, a LINE identifier or an address.

### 15. Screens and states

No screen in this story. SCR-03 Case record and SCR-04 Case timeline belong to rwb-comms and rwb-case and show a message with its channel, template, conduct check and delivery status; SCR-09 Exception queue belongs to rwb-comms (DP-19). The data steward reads the count answer through the gateway-bff data-quality route. This story renders no screen and answers only the operations of 12.1. Screen states for SCR-03, SCR-04 and SCR-09: empty, loading, error and no access are Not specified in the source documents (CG-ALL-2465; CG-ALL-2466; CG-ALL-2467).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-022-01 | AC1, BR1, BR4, BR8; the send is RWB-P6-E2022-APP's | End to end | P-0077 MOBILE consent GIVEN; NSS stub reference NSS-7781 |
| TC-E2-022-02 | AC2 and AC3, BR4; the two appends and the fold | End to end | P-0077 LINE consent GIVEN; LINE OA stub delivered and read |
| TC-E2-022-03 | legacy AC3, BR3; regression, the stop is rwb-comms' | End to end | Open X6 |
| TC-E2-022-04 | legacy AC4, BR2; regression, the stop is rwb-comms' | End to end | Open X1 with contact stop |
| TC-E2-022-05 | AC1, BR4; this slice answers WITHDRAWN as data | End to end | MOBILE consent WITHDRAWN |
| TC-E2-022-06 | legacy AC6, BR8; regression, the template is rwb-comms' | End to end | SMS-REMIND TH v1 Withdrawn |
| TC-E2-022-07 | legacy AC7, BR6; regression, run by RWB-P6-E2022-APP (JOB-11 and the limit of 5 are rwb-comms') | End to end | Notification path stub unavailable for 6 attempts |
| TC-E2-022-08 | AC4, BR9; the raise to 1 and its repeat | End to end | NSS result FAILED, failed count 0 |
| TC-E2-022-09 | AC4, BR9; the repeat of the key on the count and the append | End to end | Same Idempotency-Key twice |
| TC-E2-022-10 | legacy AC10, BR7; regression, run by RWB-P7-E2022-APP (the record is RWB-P7-E2022-APP's) | End to end | Open X6; decision log stubbed unavailable |
| TC-E2-022-11 | legacy AC11, BR5; regression, run by Not specified in the source documents (CG-ALL-2462) (the hold is rwb-case's) | End to end | Legal hold true |
| TC-E2-022-12 | AC5, BR1; a missing channel with nothing written | End to end | No channel |
| TC-E2-022-13 | Access; regression, the right is RWB-P4-E2022-APP's | Component | RW-PHONECOL sends POST /api/recovery/comms/v1/cases/{caseId}/messages; refused with MSG-P4-002 |
| TC-E2-022-14 | Principle 5; regression, the proof is rwb-decision's and RWB-ITG-E2022-ITG's | NFR | Decision log write forced to fail on 10 refusals; none recorded as sent |
| TC-P1-E2022-APP-01 | AC3, BR4 | Component | Ledger fixture |
| TC-P1-E2022-APP-02 | AC6 | Component | Number and LINE identifier fixture |
| TC-E2-022-17 | AC7 | See Test Cases v9 | Key errors |
| TC-E2-022-18 | AC8 | See Test Cases v9 | View delayed past 5 s |
| TC-E2-022-20 | AC10 | See Test Cases v9 | No right on the append |
| TC-E2-022-21 | AC11 | See Test Cases v9 | View error |
| TC-E2-022-22 | AC12 | See Test Cases v9 | No right to read contact points |
| TC-E2-022-23 | AC13 | See Test Cases v9 | No credential; no right |
| TC-P1-E2022-APP-03 | AC14 | Component | Concurrent pair |
| TC-P1-E2022-APP-04 | AC15 | Component | Flag off |
| TC-E2-022-15 | Section 12 operations, contract level | Contract | rwb-source-data.yaml |
| TC-E2-022-16 | Section 12.7 tables | See Test Cases v9 | `failed_count` boundary |

The fourteen legacy IDs, their order and their Data are kept; legacy "System" maps to "End to end", "Access" to "Component" and "Resilience" to "NFR". TC-E2-022-01, 02, 05, 08, 09 and 12 are this story's own evidence on the read, the appends, the fold and the count; the others stay as regression evidence for the slices that own those criteria. The IDs are in Test Cases v9, tab Story test cases; TC-E2-022-19 is retired there with AC9.

### 17. Guardrails

- No business value in code: the channel and delivery values are reference data, the mapping and the token format are configuration, and no channel, status, template or count is written in code (DP-07; BR-P1-001).
- Personal data follows Data Classification v5. The number and the LINE identifier (`contact_value`) stay in ACE and are never selected, answered, logged or echoed. `contact_key` (DF-EXT-013) and `person_key` (DF-INT-003) are Confidential indirect identifiers: shown within the role's scope, masked in UAT, and a log carries the id of the read only, never the clear key. `external_ref` (DF-INT-029), `delivery_status` (DF-INT-028), `conduct_check` (DF-INT-012), `consent_given`, `consent_at`, `verified_at` and `failed_count` (DF-EXT-015 to DF-EXT-018) are Confidential customer data: shown within the role's scope, and a log or prompt carries a code or an id only, never the customer value. Test data is synthetic.
- No read of another service's tables: the contact value comes through this service's own view, the ledger is this service's own table, and no other service's object is named in code or tests (DP-01, DP-05, DP-18).
- No direct call to NSS or LINE OA: the only path is the ACE notification path, called by rwb-comms (REQ-DRI-006).
- No update of a ledger entry: the trigger refuses the statement, the repository has no update or delete method, and the result is a second append (DP-18).
- A count is non-negative and raised once per reference: the check refuses a negative value and the key refuses a second raise (AC4; R-UNI-40).
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates that schema only, and an applied version is never edited (DP-01, DP-02).
- One hop, 2 s, with a breaker: a slow view answers 503 instead of a partial answer (DP-11; X6).
- Every read of contact points is access logged, 100 percent (NFR-P1-009), and `personKey` and `contactPointKey` in a path or query are redacted from gateway and access logs.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-004 | SMS and LINE through the bank's channel platforms, result on the case | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | R-UNI-33, R-UNI-34, R-UNI-40 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-08, TC-E2-022-09, TC-E2-022-12 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-04, R-UNI-05, R-UNI-20, R-DEV-16, R-UNI-39 | TC-E2-022-01, TC-E2-022-03, TC-E2-022-04, TC-E2-022-10, TC-E2-022-11 |
| REQ-OCC-006 | Withdrawn consent stops the channel | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-10 | TC-E2-022-05 |
| REQ-ILG-010 | Messages dispatched write their result to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-34 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-08 |
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, section 5 | FEAT-DRI-01 | 13 Manage documents and correspondence | None | TC-E2-022-07, TC-E2-022-13 |

| Story | Relation to this story |
|---|---|
| RWB-P6-E2022-CON | C: declares the elements the message path consumes and their fakes; this story implements them |
| RWB-P6-E2022-APP | The primary slice: conduct check, template, send, JOB-11, result listener and the calls of these operations |
| RWB-P7-E2022-APP | The decision record of a refusal, which this story never writes |
| RWB-P4-E2022-APP | The access right of the message path and of these operations |
| RWB-P1-E1066-APP | Sibling: the ledger table, its writer, its case check and its append-only trigger, adopted here |
| RWB-P1-E1069-APP | Sibling: the views and the grant this story reads through |
| RWB-P1-E2021-APP | Sibling slice of the letter path, which adds `barcodeStatus` on the case read |
| RWB-ITG-E2022-ITG | Proves the whole legacy key against the live services |

### 19. Out of scope

- Sending anything: the conduct check, the template read, the merge, the send through the ACE notification path and the NSS and LINE OA calls (RWB-P6-E2022-APP).
- The outbox sender JOB-11, its retry limit of 5 and the exception queue (RWB-P6-E2022-APP; R-UNI-33, R-UNI-34).
- The result listener and the mapping of the NSS and LINE OA result codes to SENT, DELIVERED, READ and FAILED (RWB-P6-E2022-APP).
- The contact stop, the deviation facts and the consent refusal: they are decided by rwb-comms on the facts answered here.
- The decision log entry of a refusal and the incident of R-UNI-39 (RWB-P7-E2022-APP); this story writes no decision record.
- The case and its legal hold, which this story never reads; the case check is the writer's of RWB-P1-E1066-APP.
- A mutable delivery status on a row: there is none, because the ledger is append-only (GAP-2183; ASM-3538).
- The `interaction` ledger as a whole - table shape, writer, unique keys, trigger and single-entry read (RWB-P1-E1066-APP, RWB-P1-E1068-APP); this story adds one index and appends through the writer.
- The channel and delivery lists and their Thai labels (the reference-data contract of DP-07), which this story reads and never owns (GAP-2183; ASM-3540).
- The screens SCR-03, SCR-04 and SCR-09 and the gateway-bff composite routes (DP-19).
- The real cross-service proof and the NSS and LINE OA stubs replaced in SIT (RWB-ITG-E2022-ITG).

### 20. Remaining delivery steps

- Size the story (DOR-RWB-P1-E2022-APP-16): delivery lead with the squad.
- Sign off the epic design: solution architect.
- Add the `processed_event` assertion of AC4 to its test cases: test lead.
- Publish rwb-source-data.yaml 5.1.0 with the two contact operations and mark the contract Done: API contract owner.
- Publish the provider fake (NEW-GAP-S10-18): contract story owner.
- Confirm the retry limit (GAP-1600): solution architect.
- Screen states of SCR-03, SCR-04 and SCR-09 (CG-ALL-2465 to 2467): screen owners.
- Load the synthetic contact fixtures in DEV: data engineer.
