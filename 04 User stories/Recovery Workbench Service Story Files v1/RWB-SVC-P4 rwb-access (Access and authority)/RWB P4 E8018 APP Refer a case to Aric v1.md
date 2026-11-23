# RWB-P4-E8018-APP Refer a case to Aric

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BL |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E8018-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-018 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **fraud investigator**, I want **the Workbench to send a case to Aric where the fraud rules require it and to take the result back, so that the referral is raised once from the verdict the rules already made, carried by a record that names the rule and the rule version, and closed on the answer Aric gives**, so that **a fraud case reaches the fraud team without a re-keyed case file, recovery action is held while the referral is open, and the referral and its outcome can be shown afterwards without asking either team**.

Inside `rwb-access` this is the fraud referral of the legacy story RWB-E8-018:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Four deliverables, and nothing else: the write `POST /api/recovery/access/v1/admin/fraud-referrals`, which raises the referral; the write `POST /api/recovery/access/v1/admin/fraud-referrals/{referralId}/results`, which takes Aric's result back; and the two reads `GET /api/recovery/access/v1/admin/fraud-referrals/{referralId}` and `GET /api/recovery/access/v1/admin/fraud-referrals`, which answer one referral and a paged list by case and by state.
- The referral is a record of the local decision-record chain of DP-03 and not a table of its own: one record code for a referral, one entry per state change, hash-linked, appended in the transaction that answers the call. The record code, the state set and the field set are Not specified in the source documents (GAP-0880; ASM-1597).
- The case is P3's: `recovery_case` is `rwb-case`'s under the ownership map, and this story reads it through the P3 contract and holds no case row, no fraud flag and no case state. The trigger is the fraud rule verdict, which is P7's: the verdict for the case is read from the `rwb-decision` decision record, one hop, and the rule id, the rule version and the model version recorded on the referral are copied from that verdict.
- The parameters this story obeys are rows read through DP-06 with the version in force: the page default and maximum, the length of a referral reason and of a result note, the code of the fraud rule package whose verdict is read, the result codes that close a referral, and the client budget of the outside call. No value a business person may change is a constant in code (BR-P4-029).
- Aric is outside the bank. No service of the target owns the Aric interface, no operation of Aric is declared in the ownership map, the API specification or the Arch v5 catalogue, and its protocol, its credentials and the channel its result arrives on are Not specified in the source documents (GAP-0882; ASM-1600). This story calls it through one adapter, declares it as an external dependency in section 12.2 and 12.5, and fakes it in every test.
- The metadata of this story carries no `rwb-case` case contract dependency, no `rwb-decision` contract dependency and no `rwb-source-data` contract dependency, although the story reads a case, a verdict and a data-product freshness through those contracts; the missing C dependencies are raised at D1 and are not added to the metadata here (GAP-0880; ASM-1597).
- The referral state is carried on the SCR-03 case record panel, which is P3's and which the gateway-bff composite route of DP-19 serves; this story renders no screen of its own and holds no case panel.
- This story starts no workflow, owns no Schedule and publishes no event of its own: the referral is request-driven and event-free, and the only message it produces is `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1`.

The four states a referral carries - `SENT`, `RESULT_RECEIVED`, `CLOSED`, `FAILED` - are this story's own and are Not specified in the source documents (GAP-0880; ASM-1598). A referral is raised in `SENT`, becomes `FAILED` where the outside call cannot be completed, becomes `RESULT_RECEIVED` on the first result and `CLOSED` where the result code is one of the closing codes in force.

### 2. Business rationale

A fraud flag is not an administrative note: REQ-DVH-010 asks that a fraud flag refer the case to the fraud team and hold recovery action until it is confirmed or cleared, and it is Must. The legacy story carried the referral as one administration journey inside the monolith (FEAT-ADM-13, RWB-E8-018), where the case, the rule row and the decision log were rows of one schema and the referral was an in-process call in the same deployment. In the target the case is `rwb-case`'s (Architecture v5 slide 41), the rule verdict is `rwb-decision`'s (the central decision ledger and the DMN registry), and the fraud screening that raises the flag is `rwb-deviation`'s (S8 owns X1 to X7), so the referral is no longer a method call: it is a decision that needs a trigger it can prove, a record, and a transport to a system outside the bank.

This story is that record and that transport. It meets REQ-DVH-010 on the referral side - the case reaches the fraud team, and the referral stays open until the answer is taken back - and it supports REQ-CWC-018, because the referral runs unattended under a service identity and passes the same permission checks as a person. It carries the FSD target measure for the administration features: rule and limit changes made without a code release, 100 percent, measured monthly from the decision log and the Workbench records (FSD P4 v3 A2.29.1). The rule that decides whether a case is referred is data in a package version, the verdict is a recorded decision, and neither needs a release.

The control that makes the referral worth anything is that the trigger is not a person's opinion and not a second evaluation. The verdict is read once, from the decision record that already holds it, with its rule id and its rule version, and the referral entry copies both; so the referral can be shown, years later, to have been required by a named rule of a named version, and a rule change is answerable from the record rather than from a screen. The case itself is never written here: the fraud flag and the hold are P3's and S8's, and this story only reads the case and states the referral.

Keeping the case in P3 and the verdict in P7 is the point of the split. One writer for the case, one writer for the ledger, and one writer for the referral: this service. A single writer for the referral is what makes a duplicate referral impossible to create quietly, and an idempotent key is what makes a retry after a timeout answer the first referral rather than a second one.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8018-CON (same service, its own contract story) | The OpenAPI 3.1 document of the four operations, the `FraudReferral`, `FraudReferralResult` and `FraudReferralPage` schemas, the state set, the error envelope, the consumed-operation list, the declaration of Aric as an external dependency and the six contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of a referral and of each state change, hash-linked, written in the transaction that stores the answer |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the page bounds, the reason and note lengths, the fraud package code, the closing result codes and the client budget, as rows and not as code |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-03 Case record and calls the two reads of this story behind its referral panel, one hop each |
| The `rwb-case` case contract | The read of one case by its number, with its product group and its fraud flag in force, one hop and 2 s. It is not in this story's metadata contract-dependency list (GAP-0880; ASM-1597) |
| The `rwb-decision` decision contract | The read of the decisions recorded for a case, from which the fraud rule verdict, its rule id, its rule version and its model version are taken, one hop and 2 s. It is not in the metadata list either (GAP-0880; ASM-1597) |
| The `rwb-source-data` freshness contract | The freshness of the data product the case is read from, so that a stale product is refused with MSG-P1-001 (FSD P4 v3 A2.29 VR-P4-029-1), one hop and 2 s. It is not in the metadata list either (GAP-0880; ASM-1597) |
| The Aric interface | The outside system the referral is sent to and the result taken from. No service owns it, and its protocol, its credentials and its result channel are Not specified in the source documents (GAP-0882; ASM-1600) |

Business preconditions carried from RWB-E8-018, from the feature specification and from the technical specification:

- The rights in force are those of TSD P4 v3 T6.1: RW-FRAUD holds `R` in Rules and parameters, RW-COE holds `CRUD`, RW-RISK holds `RA`, RW-AUDIT holds `R`, and RW-PHONECOL holds a dash. The referral write authorises Rules and parameters C, the result write U and the two reads R; a caller without the letter is refused with 403 and MSG-P4-002 (BR3).
- The FSD P4 v3 A2.29.3.3 role table names no role as primary - the feature "runs unattended" - and the fraud investigator as a secondary user, while T6.1 gives RW-FRAUD `R` only. The difference is carried as an assumption and changes no metadata value (GAP-0884; ASM-1603).
- The case is `rwb-case`'s: it is read by its case number, and the fraud flag in force arrives in the P3 answer as P3 composes it. `recovery_case` carries no fraud column of its own (DF-CAS-001 to DF-CAS-023), so the field the flag arrives on is Not specified in the source documents (GAP-0881; ASM-1599).
- The verdict is the fraud rule decision recorded for the case in `rwb-decision`. The verdict's field names, the value that means "refer" and the operation that answers it are Not specified in the source documents (GAP-0880; ASM-1597).
- The legacy trigger - "a completed ACE batch, an event or a timer" (FSD P4 v3 A2.29.2 step 1) - has no counterpart in the target: `rwb-access` consumes no event for this capability (TSD P4 v3 T5.3, "Events: None") and the referral adds no Schedule, so the referral is raised by one call (GAP-0883; ASM-1601).
- The legacy endpoints and screens of RWB-E8-018 are the rule-version template's (`POST /admin/rule-versions`, SCR-39 Rules and parameters, SCR-41 Delegation of authority) and do not describe this feature; the target endpoints are fixed by RWB-P4-E8018-CON and the screen is SCR-03 (GAP-0883; ASM-1597).
- The referral reason and the result note are free text whose maximum lengths are parameter rows read through DP-06; no reason code list is used, because this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON` (GAP-0880; ASM-1597).

### 4. Flow

1. The fraud investigator opens SCR-03 Case record through the gateway-bff composite route (DP-19). The route shows the case as `rwb-case` answers it, and its referral panel calls the two reads of this story for the case.
2. The referral is raised by one call to `POST /api/recovery/access/v1/admin/fraud-referrals` on `rwb-access`, with the body `caseNo` and `referralReason` and an `Idempotency-Key` header. The caller is the signed-in user acting through the route, or the service identity of the referral path where the referral is raised unattended; both pass the same permission check (REQ-CWC-018).
3. `FraudReferralController` validates the request: `caseNo` is required and matches the case-number shape in force read through DP-06, and `referralReason` is required and within its maximum length. A missing field or a value of the wrong shape is refused with 422 and MSG-GEN-001 naming the field, a value outside its range with 422 and MSG-GEN-002, and no downstream call is made (BR11).
4. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`. A key already answered replays that first answer, stores nothing and calls nothing (BR12, AC8).
5. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Rules and parameters C. A caller without the C letter is refused with 403 and MSG-P4-002, and nothing is read, sent or recorded (BR3, AC6).
6. `FreshnessReader` reads the freshness of the data product the case is read from through `GET /api/recovery/source-data/v1/data-products/freshness`, one hop with a 2 s timeout. A product stale after a late or failed ACE batch is refused with 409 and MSG-P1-001 naming the product and its date, and no referral is raised (BR4, AC7).
7. `CaseReader` reads the case through `GET /api/recovery/case/v1/cases/{caseNo}` of `rwb-case`, one hop with a 2 s timeout and a breaker, and takes from the answer only the case reference, its product group, its status and its fraud flag in force. No customer field, no account and no balance is read or kept (BR5).
8. A case whose answer does not carry the fraud flag in force is refused with 409 and MSG-GEN-004: the referral is not raised where the case is not flagged, and the caller is asked to reload the case (BR4, AC3).
9. `FraudVerdictReader` reads the decisions recorded for the case through `GET /api/recovery/decision/v1/decisions?caseId={caseId}` of `rwb-decision`, one hop with a 2 s timeout and a breaker, and takes the fraud rule verdict with its decision reference, its rule id, its rule version and its model version (BR6).
10. A case with no fraud verdict in force, or with a verdict whose outcome is not the referral outcome in the parameter row, is refused with 409 and MSG-GEN-004: the referral is only raised where the fraud rules require it, and the refusal records nothing (BR4, AC3).
11. A referral already open for the case is refused with 409 and MSG-GEN-004; the existing referral is answered by the list read, so a second referral cannot be opened by a second key (BR7, AC8).
12. `AricReferralClient` sends the referral to Aric through the outside adapter, one call with the client budget read through DP-06, carrying the case reference, the verdict reference and the referral reason and no personal field of the customer beyond what the interface requires, and takes the external reference Aric answers (BR8, AC10).
13. Where Aric cannot be reached or does not answer inside the budget, the referral is recorded in state `FAILED` with its entry, the answer is 503 with MSG-P7-003, and a retry with the same `Idempotency-Key` re-attempts the same referral and appends the `SENT` entry when the send succeeds (BR8, AC10).
14. In one local transaction the service appends one entry to the decision-record chain of DP-03 with the record code of a fraud referral, the case id, the case number in `inputs_ref`, the verdict's decision reference, its rule id, its rule version and its model version, the state `SENT`, the external reference and the time; sets the idempotency row to the answer; and stages the outbox row of the entry (BR9, BR12).
15. The answer is 201 with `referralId`, `caseNo`, `state` `SENT`, `ruleId`, `ruleVersion`, `sentAt`, `externalReference` and the `Location` of the referral read (BR10).
16. `POST /api/recovery/access/v1/admin/fraud-referrals/{referralId}/results` takes Aric's result back: the body `resultCode`, `investigationReference` and `resultNote`, with an `Idempotency-Key`, authorised on Rules and parameters U. The service validates `resultCode` against the result codes in force read through DP-06, appends one entry, moves the referral to `RESULT_RECEIVED`, or to `CLOSED` where the code is one of the closing codes in force, and answers 200 with the referral (BR10, AC5).
17. A result on a referral that is `CLOSED` is refused with 409 and MSG-GEN-004; a result on a referral that is `FAILED` is refused with 409 and MSG-GEN-004 until the referral has been sent again (BR10, AC4).
18. `GET /api/recovery/access/v1/admin/fraud-referrals/{referralId}` answers the referral: its case number, its state, its verdict reference, its rule id and rule version, its external reference, its sent time, its result fields where a result was taken, and the number of entries that carry its state path (BR13).
19. `GET /api/recovery/access/v1/admin/fraud-referrals?caseNo=&state=&page=&size=` answers a page of referrals filtered by case and by state, ordered by the time of the latest entry then by entry id so the paging is stable, with the page default and maximum read through DP-06 (BR13).
20. A case or a state with no referral answers 200 with an empty `items` and total 0; it is never a 404 and never names a customer, so the read cannot be used to probe for a case that has not been referred (BR14).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `caseNo` or `referralReason` is empty, or `caseNo` is not of the shape in force | 422 naming the field; no downstream call, no entry, no send | MSG-GEN-001 | AC3 |
| X2 | `referralReason` or `resultNote` is longer than its parameter, or `size` is above its maximum | 422 naming the field and its bounds; no call, no entry | MSG-GEN-002 | AC3 |
| X3 | The caller holds no Rules and parameters C on the referral, U on the result, or R on the reads | 403, no case read, no verdict read, no send, no entry | MSG-P4-002 | AC6 |
| X4 | The caller's session has ended | 401, nothing read, nothing sent, nothing recorded | MSG-P4-001 | AC6 |
| X5 | The data product the case is read from is stale after a late or failed ACE batch | 409 naming the product and its date; no referral and no entry | MSG-P1-001 | AC7 |
| X6 | The case does not exist, or its answer carries no fraud flag in force | 404 for a case that does not exist; 409 and a reload action for a case not flagged; no entry | MSG-GEN-004 | AC3 |
| X7 | The case has no fraud verdict in force, or the verdict does not require a referral | 409; no entry, no send | MSG-GEN-004 | AC3 |
| X8 | A referral is already open for the case, or a result is sent for a referral that is `CLOSED` or `FAILED` | 409; the existing referral is answered by the read, nothing is appended | MSG-GEN-004 | AC4, AC8 |
| X9 | Aric cannot be reached, or does not answer inside the client budget | The referral is recorded `FAILED`, 503 and no `SENT` state; a retry with the same key re-attempts the same referral | MSG-P7-003 | AC10 |
| X10 | The local entry, the idempotency row or the outbox row cannot be written | 503 and no referral answered; nothing is recorded and the retry completes one entry | MSG-P7-003 | AC2 |
| X11 | The same referral or the same result arrives twice with the same `Idempotency-Key` | The first answer is replayed; one entry, one send | None | AC8 |
| X12 | A break-glass grant is active for the caller | The action proceeds and the answer carries the warning with the end time of the grant, and the entry carries the grant id | MSG-P4-004 | AC6 |

No exception path of this story writes a case, a case status, a fraud flag, a deviation or a task: the case belongs to `rwb-case`, the flag to the case as P3 composes it and the screening to `rwb-deviation`. The only rows this story writes of its own are the entries of its own chain and the platform library rows of the request.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8018-CON and its fakes; the case, the verdict and the freshness are read through their owners' contracts, so no case row, no decision row and no data-product row is held here |
| Negotiable | The reason and note lengths, the page bounds, the fraud package code, the closing result codes and the client budget are parameter rows; the state set and the record code are reviewed with the fraud team and the decision-record library owner |
| Valuable | One record decides that a case was referred to the fraud team by a named rule of a named version, takes the answer back and closes it, and no second referral of the same case can be opened quietly |
| Estimable | One controller, one referral service, one state reader, one outside adapter, three contract clients, one record appender, one idempotency store, six fakes and twelve test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule, no screen and no event of its own |
| Testable | Each owned criterion has a test case in section 16; the state path is provable against a seeded chain and the outside transport is provable against its fake |

### 7. Acceptance criteria

```gherkin
Feature: Refer a case to Aric

  Background:
    Given the environment is SIT
    Given the cases are held by rwb-case and rwb-access holds no case row, no fraud flag and no case state
    Given Aric is outside the bank and is unreachable from SIT, so its transport is a fake in every test (ASM-1600)
    Given test user "U-8181" holds RW-FRAUD with "R" only in "RULES_AND_PARAMETERS"
    Given test user "U-8182" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS"
    Given test user "U-8183" holds RW-PHONECOL with "-" in "RULES_AND_PARAMETERS"
    Given test user "U-8184" holds RW-AUDIT with "R" in "RULES_AND_PARAMETERS"

  Scenario: AC1 Refer a case to Aric (legacy RWB-E8-018 AC1)
    Given the rwb-case contract mock returns case "RW-2026-000123" with its fraud flag in force
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends a case to Aric where the fraud rules require it, and takes the result back
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-018 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The referral is raised on the verdict, and the record carries the rule and its version (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000123" with its fraud flag in force and product group "MORTGAGE"
    And the rwb-decision contract mock returns the fraud verdict for "RW-2026-000123" with decision reference "DL-2026-000981", ruleId "R-UNI-08", ruleVersion "FRAUD-2027-01" and modelVersion "DMN-FRAUD-3"
    And the source-data freshness mock answers that the product of "RW-2026-000123" is fresh for 2026-11-22
    And the Aric transport fake accepts the referral and answers externalReference "ARIC-2027-004417"
    When "U-8182" calls POST /api/recovery/access/v1/admin/fraud-referrals for caseNo "RW-2026-000123" and referralReason "X4 fraud confirmed by the rule package" with Idempotency-Key "k-018-1"
    Then the response is 201 with state "SENT", ruleId "R-UNI-08", ruleVersion "FRAUD-2027-01" and externalReference "ARIC-2027-004417"
    Then the referral entry carries caseNo "RW-2026-000123", decision reference "DL-2026-000981", ruleId "R-UNI-08", ruleVersion "FRAUD-2027-01" and modelVersion "DMN-FRAUD-3"
    Then the Aric transport fake records one send for "RW-2026-000123" and one referral only
    Then the referral state is read back through GET /api/recovery/access/v1/admin/fraud-referrals?caseNo=RW-2026-000123 as one item in state "SENT"

  Scenario: AC4 The referral is a record of one entry per state change, and the state path is answered (new, D-RCV-60)
    Given "U-8182" referred case "RW-2026-000123" under Idempotency-Key "k-018-1" and the referral is in state "SENT"
    When "U-8182" calls POST /api/recovery/access/v1/admin/fraud-referrals/{referralId}/results for resultCode "INVESTIGATION_OPEN" and investigationReference "ARIC-2027-004417" with Idempotency-Key "k-018-2"
    Then the response is 200 with state "RESULT_RECEIVED"
    Then a second entry is appended for the same referralId and no row of a new table is written
    When "U-8182" calls the same operation for resultCode "FRAUD_CONFIRMED" with Idempotency-Key "k-018-3"
    Then the response is 200 with state "CLOSED"
    Then GET /api/recovery/access/v1/admin/fraud-referrals/{referralId} answers the referral with state "CLOSED", three entries in its state path, its verdict reference and its rule version
    Then GET /api/recovery/access/v1/admin/fraud-referrals?state=CLOSED answers the referral and a referral of another case is not in the page
    When "U-8182" calls the result operation again for the closed referral with Idempotency-Key "k-018-4"
    Then the response is 409 with message MSG-GEN-004 and no fourth entry is appended

  Scenario: AC5 A result is taken back, recorded, and closed on the closing code in force (new, D-RCV-60)
    Given a referral of case "RW-2026-000123" is in state "SENT" with externalReference "ARIC-2027-004417"
    And the parameters in force name "FRAUD_CONFIRMED" and "FRAUD_CLEARED" as the closing result codes
    When "U-8181" holding "R" only calls POST /api/recovery/access/v1/admin/fraud-referrals/{referralId}/results for resultCode "FRAUD_CLEARED" with Idempotency-Key "k-018-5"
    Then the response is 403 with message MSG-P4-002 and no entry is appended
    When "U-8182" calls it for resultCode "FRAUD_CLEARED" and resultNote "Aric cleared the account" with Idempotency-Key "k-018-6"
    Then the response is 200 with state "CLOSED", resultCode "FRAUD_CLEARED" and investigationReference "ARIC-2027-004417"
    Then the entry carries the result code, the investigation reference, the note and the time, and no name and no account number
    When "U-8182" calls it for resultCode "NOT_A_CODE" with Idempotency-Key "k-018-7"
    Then the response is 422 with message MSG-GEN-002 naming resultCode and no entry is appended

  Scenario: AC6 A caller without the right is refused, and a role with the read right cannot refer (new, D-RCV-60)
    Given the case and verdict mocks are in place and the Aric transport fake records every call
    When "U-8183" holding a dash in "RULES_AND_PARAMETERS" calls POST /api/recovery/access/v1/admin/fraud-referrals for caseNo "RW-2026-000123" with Idempotency-Key "k-018-8"
    Then the response is 403 with message MSG-P4-002 and no referral is answered
    Then the rwb-case contract fake records no case read, the rwb-decision contract fake records no verdict read and the Aric transport fake records no send
    When "U-8181" holding "R" only calls the same operation with Idempotency-Key "k-018-9"
    Then the response is 403 with message MSG-P4-002 and no entry is appended
    When "U-8181" calls GET /api/recovery/access/v1/admin/fraud-referrals?caseNo=RW-2026-000123
    Then the response is 200 and answers the referrals of that case

  Scenario: AC7 A stale data product is refused before the referral is raised (new, D-RCV-60)
    Given the source-data freshness mock answers that the product of case "RW-2026-000123" is from 2026-11-21 and the batch of 2026-11-22 has not arrived
    When "U-8182" calls POST /api/recovery/access/v1/admin/fraud-referrals for caseNo "RW-2026-000123" with Idempotency-Key "k-018-10"
    Then the response is 409 with message MSG-P1-001 naming the product and 2026-11-21
    Then no verdict is read, the Aric transport fake records no send and no entry is appended
    Then GET /api/recovery/access/v1/admin/fraud-referrals?caseNo=RW-2026-000123 answers an empty page with total 0

  Scenario: AC8 One case, one referral, and one key answers once (new, D-RCV-60)
    Given "U-8182" referred case "RW-2026-000123" under Idempotency-Key "k-018-1" and the referral is in state "SENT"
    When "U-8182" sends the same request again with Idempotency-Key "k-018-1"
    Then the first answer is replayed with its referralId, state "SENT" and externalReference "ARIC-2027-004417"
    Then exactly one referral entry exists for the case and the Aric transport fake records one send
    When "U-8182" sends the same case with a new Idempotency-Key "k-018-11"
    Then the response is 409 with message MSG-GEN-004
    Then exactly one referral exists for the case and no second send is made

  Scenario: AC9 The entry carries references only and no personal data (new, D-RCV-60)
    Given a referral of case "RW-2026-000123" is in state "SENT"
    When "U-8184" holding Rules and parameters R calls GET /api/recovery/access/v1/admin/fraud-referrals/{referralId}
    Then the answer carries the case number, the referralId, the state, the verdict reference, the rule id, the rule version, the external reference and times
    Then the answer carries no customer name, no identification number, no account number, no balance, no e-mail address and no user reference
    Then the referral entry of the decision-record chain carries no personal field and no case data beyond the case reference and the verdict reference
    Then the published entry on rwb.decision-record.v1 carries the same references and no personal field

  Scenario: AC10 Aric is outside the bank, and a failed send leaves the referral failed (new, D-RCV-60)
    Given the Aric transport fake is switched to answer a timeout for case "RW-2026-000123"
    When "U-8182" calls POST /api/recovery/access/v1/admin/fraud-referrals for caseNo "RW-2026-000123" with Idempotency-Key "k-018-12"
    Then the response is 503 with message MSG-P7-003
    Then the referral is recorded in state "FAILED" with one entry and no external reference
    Then no request leaves the cluster and the transport fake records one attempted send
    When the fake is switched to accept and "U-8182" retries with Idempotency-Key "k-018-12"
    Then the answer is 201 with state "SENT" and the same referralId
    Then the state path carries the "FAILED" entry and then the "SENT" entry, in that order
```

AC1 and AC2 are the two criteria of RWB-E8-018, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the case mock, so the referral is provable while the `rwb-case` contract is still a fake. AC3 to AC10 are new under D-RCV-60 and test only what this story adds: the verdict as the trigger, the record and its state path, the result taken back, the three refusals, the idempotency and the outside transport.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case is referred to Aric where the fraud rules require it, and the result Aric gives is taken back and recorded with the rule version | RWB-E8-018 AC1; FSD P4 v3 A2.29; REQ-DVH-010 |
| BR2 | The referral runs unattended: it needs no screen of its own, and a caller acting for the service passes the same permission checks as a person and is recorded with the identity it used | FSD P4 v3 A2.29.3.3; REQ-CWC-018 |
| BR3 | The referral write needs Rules and parameters C, the result write U and the two reads R; a caller without the letter is refused with 403 and MSG-P4-002 and nothing is read, sent or recorded | TSD P4 v3 T6.1; legacy RWB-E8-018 permission checks |
| BR4 | The referral is raised only where the case is flagged, the verdict in force requires a referral and the data product the case is read from is fresh; each refusal records nothing and sends nothing | FSD P4 v3 A2.29 VR-P4-029-1; REQ-DVH-010 |
| BR5 | The case is `rwb-case`'s: this story reads it through the P3 contract and holds no case row, no case state, no fraud flag and no customer field | Ownership Map v1 (`recovery_case` = P3); Architecture v5 slide 41; DP-01 |
| BR6 | The trigger is the verdict `rwb-decision` already recorded: the decision reference, the rule id, the rule version and the model version on the referral are copied from that verdict and the rule is not evaluated a second time here | Architecture v5 slide 14 (P7 central decision ledger); REQ-DVH-010; DP-04 |
| BR7 | One case carries one open referral; a second referral of the same case is refused with 409 and MSG-GEN-004, and the existing referral is answered by the read | RWB-E8-018 AC1; REQ-DVH-010 |
| BR8 | The transport to Aric is outside the bank and belongs to no service; a send that cannot be completed leaves the referral `FAILED` and answers 503 with MSG-P7-003, and a retry re-attempts the same referral | FSD P4 v3 A2.29 (integration point Aric); GAP-0882; ASM-1600 |
| BR9 | Every referral and every state change appends exactly one entry to the local decision-record chain of DP-03 in the transaction that stores the answer; an answer that cannot be recorded is withheld with 503 and MSG-P7-003 | R-UNI-39; RWB-E8-018 AC2; DP-03 |
| BR10 | The state set is `SENT`, `RESULT_RECEIVED`, `CLOSED` and `FAILED`; the first result moves the referral to `RESULT_RECEIVED`, and a result code in the closing list moves it to `CLOSED`; no entry is ever updated or deleted | ASM-1598; DP-03 |
| BR11 | The reason and note lengths, the page bounds, the fraud package code, the closing result codes and the client budget are parameter rows read through DP-06 with the version in force; no such value is a constant in code | DP-06; FSD P4 v3 A2.29 BR-P4-029 |
| BR12 | One `Idempotency-Key` answers one referral or one result: a replay answers the first answer, appends no second entry and makes no second send | Architecture v5 slide 42; DP-09 |
| BR13 | The two reads answer from this service's own chain, one item per referral with its latest state, ordered by the time of the latest entry then by entry id, and they never rewrite an entry | DP-03; DP-01; BR9 |
| BR14 | A case or a state with no referral answers an empty page with total 0; the read is never a 404 and never names a customer, so it cannot be used to probe for a case that has not been referred | TSD P4 v3 T6.2; NFR-040 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1, BR3, BR4 and BR6 are one ordered gate in `FraudReferralService`: authorise, freshness, case, verdict, duplicate, send, record. Each step that refuses returns before the next one is reached, so a refused referral can never have called Aric.
- BR2 is the absence of a screen: the four operations are callable by the case record route and by the service identity of the referral path, and the entry records the identity and the role code that carried the right, never a name.
- BR5 is the absence of a case repository: the module has no table, no view and no join for `recovery_case`, and every case field arrives in the P3 answer.
- BR6 is the field set of the entry: `rule_id` (DF-DEC-004), `rule_version` (DF-DEC-005) and `model_version` (DF-DEC-006) are copied from the verdict and are never resolved here.
- BR7 is the duplicate check over the chain: an entry of the record code with the case id and a state that is not `CLOSED` is an open referral.
- BR8 is the outside adapter: one client with a budget from DP-06, no retry of its own beyond the key, and a `FAILED` entry on a failed send.
- BR9, BR10 and BR13 are the record appender and its read: the entry commits with the idempotency row, the state is the `final_call` of the latest entry, and the reads are reads over the chain with no write method.
- BR11 is the parameters reader at request time with the version in force; a changed length, bound or code is data and needs no build.
- BR12 is the `idempotency_key` row of the platform library in `rwb_access`, written with the answer.
- BR14 is the empty answer of both reads and the absence of a 404 branch on the list.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No referral | A referral is submitted | C held, the product is fresh, the case is flagged, the verdict requires a referral, no open referral, Aric accepts | `SENT`, one entry, answer 201 with the external reference |
| No referral | A referral is submitted | No C letter | Refused 403 with MSG-P4-002; no read, no send, no entry |
| No referral | A referral is submitted | The data product is stale | Refused 409 with MSG-P1-001; no verdict read, no send, no entry |
| No referral | A referral is submitted | The case is not flagged, or the verdict does not require a referral | Refused 409 with MSG-GEN-004; no send, no entry |
| No referral | A referral is submitted | Aric cannot be reached | `FAILED`, one entry, 503 with MSG-P7-003 |
| No referral | A referral is submitted | The entry cannot be written | Refused 503 with MSG-P7-003; nothing recorded and nothing sent |
| `SENT` | The same key is sent again | None | The first answer is replayed; no second entry and no second send |
| `SENT` | A second referral of the same case is submitted with a new key | An open referral exists | Refused 409 with MSG-GEN-004; one referral stays |
| `SENT` | A result is taken back | U held, the result code is in force, it is not a closing code | `RESULT_RECEIVED`, one entry |
| `SENT` | A result is taken back | U held, the result code is a closing code | `CLOSED`, one entry |
| `RESULT_RECEIVED` | A further result is taken back | U held, it is not a closing code | `RESULT_RECEIVED`, one further entry |
| `RESULT_RECEIVED` | A further result is taken back | U held, it is a closing code | `CLOSED`, one further entry |
| `CLOSED` | A result is taken back | Any code | Refused 409 with MSG-GEN-004; no entry |
| `FAILED` | The same key is retried | Aric accepts | `SENT`, one further entry with the same referralId |
| `FAILED` | A result is taken back | Any code | Refused 409 with MSG-GEN-004; the referral is not sent |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | A referral, a state change, or a refusal recorded at the service edge | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| `rwb.decision-record.v1` | An entry is appended | One `DecisionRecorded` message from the outbox of the same transaction |
| `rwb-case` | The case's fraud flag or status changes | P3's, written by P3; this story reads it at referral time and holds no copy |
| `rwb-deviation` | The X4 deviation is raised, confirmed or cleared | S8's, written by S8; this story neither reads nor writes it |

The referral state is not the case state. A referral in `CLOSED` says that Aric answered and what it answered; it moves no case, lifts no hold and closes no deviation, because the fraud flag, the hold and the deviation are P3's and S8's and are moved by the case path of FEAT-DVF-04 (BR5).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The service identity of the referral path (role class non-human actor) | Raise a referral unattended with Rules and parameters C, passing the same checks as a person and recorded with the identity and the role code it used (REQ-CWC-018; ASM-1603) |
| Center of excellence analyst (RW-COE) | Raise a referral and take a result back, holding `CRUD` in Rules and parameters (TSD P4 v3 T6.1) |
| Risk and model risk officer (RW-RISK) | Holds `RA` in Rules and parameters and may raise a referral and approve nothing here, because the referral carries no approval (TSD P4 v3 T6.1) |
| Fraud investigator (RW-FRAUD) | Reads the referrals of a case with `R` only; the write is refused with MSG-P4-002, and the difference to the FSD A2.29.3.3 role table is carried in ASM-1603 |
| Internal audit (RW-AUDIT) | Reads the referrals and their state paths with Rules and parameters R; refers nothing |
| A role with a dash in Rules and parameters (RW-PHONECOL) | Refused with 403 and MSG-P4-002 on every operation; nothing is read, sent or recorded |
| The gateway-bff route | Calls the two reads on behalf of the signed-in user, one hop each, behind the referral panel of SCR-03 |
| `rwb-access` itself | Reads `role` and `permission` in its own schema and writes only its own chain and the platform library rows of the request |
| `rwb-case` (P3) | Owns the case, its fraud flag, its status and its holds; answers the case read |
| `rwb-decision` (P7) | Owns the central decision ledger and the verdict; answers the decision read and receives this story's record events |
| `rwb-deviation` (S8) | Owns the X4 fraud screening, the deviation and its hold; this story calls it not at all |
| `rwb-source-data` (P1) | Owns the data products and their freshness; answers the freshness read |
| Aric (outside the bank) | Receives the referral and answers the result; no service of the target owns the interface (GAP-0882; ASM-1600) |

The refusal shapes are 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002 for an absent right, 401 with MSG-P4-001 for no session, 409 with MSG-GEN-004 for a state that does not allow the action and with MSG-P1-001 for a stale data product, 422 with MSG-GEN-001 for a field and MSG-GEN-002 for a value out of range, and 503 with MSG-P7-003 for a record or a send that cannot be completed. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E8018-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the role code recorded with the entry, and the non-human role class of the service identity |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the Rules and parameters C, U and R letters and the role they are held through |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the referral entry: `decision_code` DF-DEC-003 as the record code of a referral, `case_id` DF-DEC-002 as the case, `rule_id` DF-DEC-004, `rule_version` DF-DEC-005 and `model_version` DF-DEC-006 from the verdict, `inputs_ref` DF-DEC-008 with the referral id, the case number, the verdict reference, the external reference and the grant id, `final_call` DF-DEC-012 as the state, `actions` DF-DEC-014 with the target system, the send result and the times, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the two reads and for the duplicate check |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of a referral or of a result | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` | the record row of each entry | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` of `rwb_case` | case_no DF-CAS-002, product_group DF-CAS-003, status DF-CAS-005, stage_code DF-CAS-006, deviation_open DF-CAS-019, legal_hold DF-CAS-020, rule_version DF-CAS-021, and the fraud flag as P3 composes it | Returned through the P3 contract; not read |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` of `rwb_decision` | the fraud verdict: id, case_id, decision_code, rule_id, rule_version, model_version and decided_at | Returned through the P7 contract; not read |
| DF-REF-001 to DF-REF-015 | `rule_row` of `rwb_decision` | none | Not read: the rule is named by the verdict and is not resolved here |
| (data product) | `data_product` of `rwb_source_data` | the freshness of the product the case is read from | Returned through the P1 contract; not read |
| (deviation) | `deviation` of `rwb_deviation` | none | Not read: the X4 screening is S8's (ownership map) |

No row of `recovery_case`, `decision_log_entry`, `rule_row`, `data_product` or `deviation` is read or written: they are P3's, P7's, P1's and S8's under the ownership map, and their fields arrive in the contracts, not by a schema read (DP-01). No new table is created: the referral lives in the local decision-record chain of DP-03, one entry per state change, and `role` and `permission` are read only. Field IDs are those of the Logical Data Model and Data Dictionary v8 and of TSD P4 v3 T3.1.

The record code of a fraud referral, the ordered field set of the four operations, the state set, the name of the closing result codes and the shape of the verdict are Not specified in the source documents (GAP-0880; ASM-1597; ASM-1598); the schema of RWB-P4-E8018-CON fixes them and this story reads and writes them as that contract publishes them. The field on which the case answer carries the fraud flag is Not specified either: `recovery_case` has no fraud column and the flag is composed by P3 (GAP-0881; ASM-1599).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/fraud-referrals` | P4 `rwb-access` | Body: `caseNo`, `referralReason` | `referralId`, `caseNo`, `state` `SENT`, `ruleId`, `ruleVersion`, `sentAt`, `externalReference`, with `Location` of the referral read | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 (MSG-GEN-004, MSG-P1-001); 422 (MSG-GEN-001, MSG-GEN-002); 503 (MSG-P7-003) | Rules and parameters C | `Idempotency-Key` required; a replay answers the first answer and makes no second send |
| POST | `/api/recovery/access/v1/admin/fraud-referrals/{referralId}/results` | P4 `rwb-access` | Path: `referralId`. Body: `resultCode`, `investigationReference`, `resultNote` | `referralId`, `caseNo`, `state` `RESULT_RECEIVED` or `CLOSED`, `resultCode`, `investigationReference`, `receivedAt` | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 (MSG-GEN-004); 422 (MSG-GEN-001, MSG-GEN-002); 503 (MSG-P7-003) | Rules and parameters U | `Idempotency-Key` required; a replay answers the first answer and appends no second entry |
| GET | `/api/recovery/access/v1/admin/fraud-referrals/{referralId}` | P4 `rwb-access` | Path: `referralId` | `FraudReferral`: `referralId`, `caseNo`, `state`, `verdictReference`, `ruleId`, `ruleVersion`, `externalReference`, `sentAt`, `resultCode`, `investigationReference`, `receivedAt`, `entryCount` | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-GEN-004); 503 (MSG-P7-003) | Rules and parameters R, scope applied | Not applicable, read only |
| GET | `/api/recovery/access/v1/admin/fraud-referrals` | P4 `rwb-access` | Query: `caseNo`, `state`, `page`, `size` | `FraudReferralPage`: `items` of `FraudReferral`, `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001, MSG-GEN-002); 503 (MSG-P7-003) | Rules and parameters R, scope applied | Not applicable, read only |

All four operations sit on the base `/api/recovery/access/v1` of DP-13. `page` defaults to the value of its parameter row and `size` is capped by it, both read through DP-06 and never from code (BR11). The referral read answers 404 for a referral id that does not exist; the list never answers 404 (BR14).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The C, U and R checks behind the four operations, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The page bounds, the reason and note lengths, the fraud package code, the closing result codes and the client budget, with the version in force (DP-06) |
| GET | `/api/recovery/case/v1/cases/{caseNo}` | P3 `rwb-case` | The case: its reference, its product group, its status and its fraud flag in force. Declared as consumed, never as provided, and named as one of the missing C dependencies of the key (GAP-0880; ASM-1597) |
| GET | `/api/recovery/decision/v1/decisions?caseId={caseId}` | P7 `rwb-decision` | The fraud rule verdict recorded for the case: its decision reference, its rule id, its rule version, its model version and its outcome. Declared as consumed and named as one of the missing C dependencies (GAP-0880; ASM-1597) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 `rwb-source-data` | The freshness of the product the case is read from, so that a stale product is refused with MSG-P1-001 (FSD P4 v3 A2.29 VR-P4-029-1). Declared as consumed and named as one of the missing C dependencies (GAP-0880; ASM-1597) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the parameters read and the authorise answer are cached for the session or the request. No other operation of `rwb-case`, `rwb-decision`, `rwb-source-data`, `rwb-deviation` or `rwb-integration` is called.

**Aric, the outside system.** The referral leaves the bank through one adapter, not through a REST operation of a service: no operation of Aric appears in the ownership map, in the API specification or in the Arch v5 catalogue, no service owns the interface, and its protocol, its credentials and the channel its result arrives on are Not specified in the source documents (GAP-0882; ASM-1600). It is declared here as an external dependency of the contract, it is faked in every test, and no P2 integration contract is claimed for it, because this story's metadata carries no `RWB-P2-*` dependency and its pattern list no DP-16.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a referral or of a state change: the case reference, the referral id, the verdict reference, the rule id, the rule version, the model version, the state, the external reference and the time |

CloudEvents 1.0 envelope, from the outbox of the transaction that stores the answer. The payload carries references, codes and times and no name, no identification number, no account number, no balance and no e-mail address. This story publishes no `rwb.access.<Event>.v1` message: the two events of `rwb-access` are `AccessPolicyChanged` (RWB-P4-E1037-APP) and `DoaLimitChanged` (RWB-P4-E8008-APP), and a fraud referral adds neither (Architecture v5 slides 14 and 43).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 with no inbound event for this capability, and TSD P4 v3 T5.3 states "Events: None" for the module. The referral reads the case, the verdict and the freshness at request time instead of subscribing to them, so no consumer group, no `processed_event` row and no inbox is created. The legacy trigger "a completed ACE batch, an event or a timer" is read as that request path (GAP-0883; ASM-1601).

#### 12.5 Workflows and activities

None. The referral is synchronous and this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. The outside call to Aric is made by the client adapter inside the request, with the budget read through DP-06 and no durable retry: a failed send is a `FAILED` entry and a retry by the caller with the same key, not a workflow of its own (BR8). The Aric interface is the external dependency declared in section 12.2 and belongs to no service of the target.

#### 12.6 Schedules

None. The four operations are request-driven, and the only Schedule of `rwb-access` is the six-monthly access review list (JOB-18) of RWB-P4-AD008-APP. The referral adds no timer and no batch, because the verdict it reads is already recorded by the rule path that decided it (BR6).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role code recorded with the entry and the non-human role class of the service identity |
| `permission` | P4 (`rwb_access`) | Read only: the Rules and parameters C, U and R letters |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the entry of a referral and of each state change. Read: the two reads and the duplicate check |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of each entry and the idempotency row of each write; no inbox row, because no event is consumed (DP-09; ASM-0074) |
| `recovery_case` | P3 (`rwb_case`) | Not read and not written: the case is P3's and its fields arrive in the contract |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the verdict arrives in the P7 answer and the entry this story writes is its own local record |
| `deviation` | S8 (`rwb_deviation`) | Not read and not written: the X4 screening is S8's |
| `data_product` | P1 (`rwb_source_data`) | Not read and not written: the freshness arrives in the P1 answer |

No case, deviation, data-product or rule table is named as this service's and none is created here. `lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON`, so the result codes and the referral reason are parameter rows and free text, not a list of values of this service (GAP-0880; ASM-1597). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| case fake | the `rwb-case` contract (GAP-0880; ASM-1597) | `GET /cases/{caseNo}` answering "RW-2026-000123" with product group `MORTGAGE`, status `IN_PROGRESS` and its fraud flag in force; a case with no fraud flag; a case that does not exist; a 503 for X6 |
| verdict fake | the `rwb-decision` contract (GAP-0880; ASM-1597) | `GET /decisions?caseId=` answering the fraud verdict with decision reference "DL-2026-000981", ruleId "R-UNI-08", ruleVersion "FRAUD-2027-01" and modelVersion "DMN-FRAUD-3"; a case with no verdict; a verdict whose outcome is not the referral outcome; a 503 |
| freshness fake | the `rwb-source-data` contract (GAP-0880; ASM-1597) | A fresh product for 2026-11-22 and a stale product from 2026-11-21 for X5 |
| parameters fake | RWB-P3-E1042-CON | The page bounds, the reason and note lengths, the fraud package code, the closing result codes and the client budget, with the version in force |
| authorise fake | RWB-P4-E8018-CON, RWB-P4-E1037-CON | A granted answer for RW-COE with C, U and R, for RW-RISK with A, C, U and R, and for RW-AUDIT and RW-FRAUD with R, and a refused answer with MSG-P4-002 for RW-PHONECOL with a dash and for RW-FRAUD on the two writes |
| decision-record fake | RWB-PLT-E1027-CON | The append of a referral and of each state change, the hash-link check, a seeded state path of three entries, the duplicate check over an open referral, and the forced failure AC2 needs |
| Aric transport fake | the outside interface (GAP-0882; ASM-1600) | An accepted referral with externalReference "ARIC-2027-004417", a timeout for X9, a refusal with its own reason, and the same answer for a repeated `Idempotency-Key` |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-03 with the case as `rwb-case` answers it and the referral panel that calls the two reads |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 4 (the referral, the result and the two reads); consumed 5 | Base `/api/recovery/access/v1`; the own authorise operation, the `rwb-case` parameters and case reads, the `rwb-decision` decision read and the `rwb-source-data` freshness read, one hop and 2 s each |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | None | No file input and no file output; the outside call to Aric is a synchronous interface call and not a file (GAP-0882) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/fraudreferral`, Java package `th.co.scb.ace.workbench.recovery.access.fraudreferral`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module referral method and the in-module decision-log write of the monolith (DP-03: the record library and the shared topic, once per state change; DP-01 and DP-13: the case read through the P3 contract and no table read), the `casewf.config` read of the referral settings (DP-06: the parameters contract with the version in force), and the ace-web screens the legacy story named (DP-19: the SCR-03 composite route). DP-01, DP-02, DP-09 and DP-11 govern the service baseline, the idempotency store and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it. DP-04 is deliberately absent: the rule package and the Drools evaluation are `rwb-decision`'s and the verdict is read, not evaluated, so this story embeds no Drools kit and adds no `RWB-PLT-E1072-CON`. The three contract reads of section 12.2 are consumed through their owners' contracts and fakes, and the missing C dependencies are raised in the key's gap and not added to the metadata (GAP-0880; ASM-1597).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| FraudReferralController | Controller | The four operations: validation, the `Idempotency-Key` lookup, the RFC 9457 problem responses, `Location` on a created referral |
| FraudReferralService | Service | The ordered gate of BR1, BR3, BR4, BR6 and BR7: right, freshness, case, verdict, duplicate, send, record; a refusal returns before the next step |
| FraudReferralStateService | Service | The state path of BR10: the result code against the list in force, the move to `RESULT_RECEIVED` or `CLOSED`, and the refusal of a result on a closed or failed referral |
| FraudReferralReader | Service | The reads of BR13 and BR14: one referral with its latest state and its entry count, the paged list by case and by state, the stable order and the empty page |
| FraudReferralRepository | Repository | Read-only queries over the local decision-record table of DP-03 in `rwb_access` filtered by the record code, the case id and the state; no write method |
| CaseReader | Client | The `rwb-case` case read, one hop, 2 s timeout and a breaker; maps a 404 to the case refusal and a timeout to 503 |
| FraudVerdictReader | Client | The `rwb-decision` decision read, one hop, 2 s timeout and a breaker; takes the verdict and its rule and model versions |
| FreshnessReader | Client | The `rwb-source-data` freshness read, one hop, 2 s timeout; produces MSG-P1-001 with the product and its date |
| AricReferralClient | Client | The outside adapter: the referral payload, the external reference, the client budget from DP-06, and a `FAILED` outcome on a timeout or a refusal |
| DecisionRecordAppender | Service | The entry of a referral and of each state change with its outbox row, in the transaction that stores the answer (DP-03, DP-09) |
| IdempotencyStore | Service | The `Idempotency-Key` lookup and store of the platform library, written with the answer |
| PermissionReader | Service | The `role` and `permission` rows of the caller, the C, U and R letters and the role code recorded with the entry |
| ParameterReader | Service | The page bounds, the reason and note lengths, the fraud package code, the closing result codes and the client budget through DP-06, with the version in force |

**Database and migrations**

- This story creates no table of its own. `role` and `permission` are created by RWB-P4-E1037-APP, the local decision-record table by RWB-P4-E1039-APP and the platform library tables by the service's own DB story, in the per-service Flyway sequence of DP-15; this story reads and uses them.
- No case, deviation, data-product or rule table is created in `rwb_access` and no column of one is copied: a copy of the case would be a second writer of the fraud flag and would drift from `rwb-case` on the first clear (BR5).
- No write statement touches `role` or `permission`: the reader is read-only, so a referral can never grant itself a right.
- The entry, the idempotency row and the outbox row commit in one transaction; a failure rolls all three back and the answer is withheld with MSG-P7-003 (BR9).
- The referral id is the entry id of the first entry of the chain, so a referral is addressable without a table of its own and the state path is the chain filtered by that id (ASM-1597).

**Configuration and reference data**

- The page default and maximum, the referral reason and result note lengths, the fraud package code, the closing result codes and the client budget are parameter rows of `rwb-case` read through DP-06 with the version in force; no such value is a constant in code (BR11). Their names are fixed by RWB-P4-E8018-CON.
- The letters held per role are rows of `permission`; no role code and no capability area is a constant in code (BR3).
- The product group of a case is the value `rwb-case` answers and is validated against no list of this service (section 12.7).

**Build steps**

1. `FraudReferralController` and its validation; tests for X1 and X2 with no downstream call.
2. `PermissionReader` and the authorise call of step 5; test the AC6 refusals, with no case read, no verdict read, no send and an empty list afterwards.
3. `FreshnessReader` over the freshness fake; test the AC7 refusal with MSG-P1-001 and the product and date named.
4. `CaseReader` and `FraudVerdictReader` over the case and verdict fakes; tests for X6 and X7, including the case with no fraud flag and the case with no verdict.
5. `FraudReferralService` with the duplicate check; test the AC3 referral and the AC8 second referral with a new key, both with one send.
6. `AricReferralClient` over the transport fake; tests for the accepted referral of AC3 and the timeout of AC10 with the `FAILED` entry and the retry to `SENT`.
7. `DecisionRecordAppender` and `IdempotencyStore` in one transaction; test the replay of AC8 with one entry and one send, and the forced failure of AC2 with no record.
8. `FraudReferralStateService` and `FraudReferralReader` over a seeded state path of three entries; tests for AC4 and AC5, the stable order, the paging and the empty page of BR14.
9. `ParameterReader` over the parameters fake, so the story builds before `rwb-case` is in the environment; test that a changed length, bound or closing code is data and needs no build.
10. The contract-fake run of the four operations through the gateway-bff fake, so the SCR-03 referral panel can be demonstrated while the route and the three contracts are being built.

**Feature switch.** The four operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of their own. A referral path that is switched off would leave a flagged case unreferred and visible as such, which is the state the gate is meant to resolve, so this story adds no flag and removes nothing. The readiness of the Aric interface is a parameter (its client budget) and an operating condition of the environment, not a feature flag of this service.

**Done when.** The tests in section 16 pass; a flagged case "RW-2026-000123" with a fraud verdict in force is referred and answered `SENT` with the rule id, the rule version and the external reference; a stale product is refused with MSG-P1-001 and no verdict is read; a caller with a dash is refused with MSG-P4-002 and a caller with R only cannot refer; a result moves the referral to `RESULT_RECEIVED` and a closing code to `CLOSED` with one entry per change; a result on a closed referral is refused with MSG-GEN-004; the same `Idempotency-Key` replays one answer with one entry and one send and a second key on the same case is refused; a failed send leaves the referral `FAILED` and the retry succeeds; and the entries and the published record carry references and no personal data.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on all four operations |
| MSG-P4-002 | The caller holds no Rules and parameters C on the referral, no U on the result, or no R on a read | You cannot {action} here. Your role does not include it. | This story, on all four operations |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the referral and result answers, with the grant id recorded in the entry |
| MSG-GEN-001 | `caseNo` or `referralReason` is empty, or `caseNo` is not of the shape in force | Enter {field}. | This story, on the two writes and the list |
| MSG-GEN-002 | A value is outside its range: a reason or note above its maximum length, or `size` above its maximum | Not specified in the source documents (GAP-0880; ASM-1597) | This story, on the two writes and the list; the platform catalogue supplies the text and the contract carries the `messageId` only |
| MSG-GEN-004 | The case is not flagged, the verdict does not require a referral, a referral is already open, a result is sent for a closed or failed referral, or the referral id does not exist | Someone else changed this record. Reload it to see their change. | This story, on all four operations |
| MSG-P1-001 | The data product the case is read from is stale after a late or failed ACE batch | {product} is from {date}. Today's ACE batch has not arrived. | This story, on the referral, from FSD P4 v3 A2.29 VR-P4-029-1 |
| MSG-P7-003 | The local entry, the idempotency row or the outbox row cannot be written, or Aric cannot be reached inside the client budget | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on all four operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are copied unchanged from the legacy story where the message already existed: MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001 and MSG-P7-003 are the legacy texts. MSG-GEN-004 is the platform text for a state that moved. MSG-P1-001 is the P1 text and is produced here because FSD P4 v3 A2.29 VR-P4-029-1 assigns the staleness check to this feature (ASM-1602). MSG-GEN-002 is a platform message whose id the contract carries and whose text the message catalogue supplies; it is the range message of the reason length, the note length and the page size.

### 15. Screens and states

This story renders no screen of its own. It runs unattended: the referral needs no form, no panel and no confirmation of its own, and the two reads serve the referral panel of SCR-03 Case record, which is P3's screen, served through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON). The route shows the case as `rwb-case` answers it and calls the two reads of this story for the referral state of that case.

| Screen | State | What it shows |
|---|---|---|
| SCR-03 Case record (P3's screen, the referral panel) | Referral, none | An empty referral panel with total 0 and no error, also for a case no referral of which this service holds |
| SCR-03 Case record | Referral, sent | The referral with its state `SENT`, its rule id, its rule version, its external reference and its sent time |
| SCR-03 Case record | Referral, result received | The referral with its state `RESULT_RECEIVED`, its result code, its investigation reference and its received time |
| SCR-03 Case record | Referral, closed | The referral with its state `CLOSED`, the closing result code and the state path of its entries |
| SCR-03 Case record | Referral, failed | The referral with its state `FAILED`, the 503 of X9 with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |
| SCR-03 Case record | Referral, refused | The 403 of X3 with MSG-P4-002, or the 409 of X6 and X7 with MSG-GEN-004, or the 409 of X5 with MSG-P1-001 |
| SCR-03 Case record | Referral, not recorded | The 503 of X10 with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |

The legacy story named SCR-39 Rules and parameters and SCR-41 Delegation of authority in its screen table although a fraud referral sits on neither; those rows are the rule-version template's and are carried as a gap (GAP-0883). The composite route specification and the case record field list belong to RWB-PLT-N001-CON and to the P3 screen work; this story supplies the referral state only, and the fraud flag, the hold banner and the deviation section of the case record are P3's and S8's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-018-01 | AC1, BR1, BR6, BR10 | Contract | The case fake answers "RW-2026-000123" flagged; the verdict fake answers ruleId "R-UNI-08" and ruleVersion "FRAUD-2027-01"; the Aric fake accepts with "ARIC-2027-004417"; the referral is answered `SENT` and the entry carries the rule and its version |
| TC-E8-018-02 | AC2, BR9 | Component | The record store forced to fail during the referral: 503 with MSG-P7-003, no referral answered, no entry and no send; a retry with the same `Idempotency-Key` completes exactly one entry and one send |
| TC-E8-018-03 | AC6, BR3 | Component | "U-8183" with a dash in Rules and parameters refused 403 with MSG-P4-002 with no case read, no verdict read and no send; "U-8181" with R only refused on the write and answered on the read |
| TC-E8-018-04 | AC2, BR9 | NFR | The append and the outbox row forced to fail under load: every failure is a 503 with MSG-P7-003, no partial entry is ever readable, and the retry path yields one entry |
| TC-E8-018-05 | AC3, BR1, BR4, BR6 | Component | The flagged case, the verdict in force and the fresh product: 201 with `SENT`, the rule id, the rule version, the model version and the external reference; one send; the list answers one item |
| TC-E8-018-06 | AC4, BR10, BR13 | Component | A seeded state path of three entries: `SENT`, `RESULT_RECEIVED`, `CLOSED`; the referral read answers the entry count, the list filters by case and by state, and a result on the closed referral is refused 409 with MSG-GEN-004 |
| TC-E8-018-07 | AC5, BR10, BR11 | Component | The closing codes in force name "FRAUD_CONFIRMED" and "FRAUD_CLEARED": the first result answers `RESULT_RECEIVED`, the closing code answers `CLOSED`, an unknown code is refused 422 with MSG-GEN-002, and a caller with R only is refused 403 with MSG-P4-002 |
| TC-E8-018-08 | AC7, BR4 | Component | The freshness fake answers a product from 2026-11-21: 409 with MSG-P1-001 naming the product and the date, no verdict read, no send, no entry and an empty list |
| TC-E8-018-09 | AC8, BR7, BR12 | Component | The replay of `Idempotency-Key` "k-018-1" with one entry and one send; the same case with key "k-018-11" refused 409 with MSG-GEN-004 and no second send |
| TC-E8-018-10 | AC9, BR5, NFR-040 | NFR | The referral answer, the entry and the published record inspected for personal fields: references, codes and times only, and no name, identification number, account number, balance or user reference |
| TC-E8-018-11 | AC10, BR8 | Component | The Aric fake switched to timeout: 503 with MSG-P7-003 and a `FAILED` entry with no external reference; the retry with the same key answers `SENT` with the same referralId and the path carries `FAILED` then `SENT` |
| TC-E8-018-12 | AC3, BR4, BR13 | Contract | The case with no fraud flag, the case with no verdict and the verdict that does not require a referral: each refused 409 with MSG-GEN-004, no send and no entry; the referral read answers 404 for an unknown id |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows are kept: TC-E8-018-01 for AC1, TC-E8-018-02 for AC2, TC-E8-018-03 for the access refusal and TC-E8-018-04 for the forced record failure; eight rows are added for the new criteria of this story. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under §R7.2 s16. No ITG story is split from this legacy key, so no `-ITG` copy of these test cases is written here and no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the page bounds, the reason and note lengths, the fraud package code, the closing result codes and the client budget are parameter rows (BR11), the rights are rows of `permission` (BR3), and a test proves that a changed bound or a changed closing code needs no build.
- No personal data anywhere: the request, the answer, the entry and the published record carry a case number, a referral id, a verdict reference, a rule id, a rule version, a model version, a state, an external reference, a result code and times; no name, no identification number, no account number, no balance, no e-mail address and no user reference appears in the answer, the entry, the event or a test (BR10, NFR-040).
- No read of another service's tables (DP-01): `recovery_case` is P3's, `decision_log_entry` and `rule_row` are P7's, `data_product` is P1's and `deviation` is S8's, and no join crosses a schema. Every field arrives in a contract answer.
- One writer for the case: only `rwb-case` moves a case's status, its fraud flag and its holds, and only `rwb-deviation` moves the X4 deviation; this story writes neither, so a referral cannot change a case or lift a hold.
- One writer for the verdict: the rule is evaluated once, by the rule path that recorded it, and this story copies the rule id and the rule version from that verdict instead of evaluating a package (BR6).
- No referral without its record: the entry commits with the answer, and the answer is withheld with MSG-P7-003 when the entry cannot be written (BR9, R-UNI-39).
- One case, one referral, one key: an open referral blocks a second referral of the same case, and the `Idempotency-Key` is stored with the answer, so a retry after a timeout cannot create a second referral or a second send (BR7, BR12).
- The outside system stays outside: the Aric adapter is the only egress, it has no credentials in code (NFR-052), it is faked in every test, and a failed send is a recorded `FAILED` state rather than an untracked retry loop (BR8).
- The reads cannot be gamed: they answer an empty page rather than a 404 and never name a customer, so a caller cannot learn which case has not been referred (BR14).
- Every example, fixture and test payload is synthetic; no production case, customer or Aric payload is copied into a schema, a fake or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-010 | A fraud flag refers the case to the fraud team and holds recovery action until it is confirmed or cleared | Program, S8 Deviation handling | FEAT-ADM-13, FEAT-DVF-04 | All recovery processes | BR1, BR4, BR6, BR7 | TC-E8-018-01, TC-E8-018-05, TC-E8-018-12 |
| REQ-CWC-018 | A model or agent writing to a queue passes the same permission checks as a person, runs under a service identity, and its write is logged with the model or agent version | Program, Case workflow | FEAT-ADM-13 | All recovery processes | BR2, BR3, BR10 | TC-E8-018-03, TC-E8-018-05 |
| NFR-040 | Each screen and each agent receives only the personal data it needs | TSD P4 v3 T7 | FEAT-ADM-13 | All recovery processes | BR5, BR10, BR14 | TC-E8-018-10, TC-E8-018-11 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key. The BRD gives no REQ-DVF identifier for the referral; REQ-DVH-010 is the requirement the BRD actually states for it, and FEAT-DVF-04 is the S8 feature this one depends on (GAP-0883; ASM-1601).

| Legacy reference | Where it is kept |
|---|---|
| AC1 refer a case to Aric, where the fraud rules require it, and take the result back, with the rule version recorded | Sections 1, 4, 7, 8, 12.1, 12.2 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 4, 5, 7, 8, 12.1, 14 |
| The permission checks: Rules and parameters C for RW-COE and A for RW-RISK | Sections 3, 7 (AC6), 8 (BR3), 10, 12.1 |
| MSG-P4-004, MSG-P4-002, MSG-P4-001, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| The legacy data rows `recovery_case` DF-CAS-001 to DF-CAS-023, `decision_log_entry` DF-DEC-001 to DF-DEC-018, `rule_row` DF-REF-001 to DF-REF-015 and `role` DF-REF-034 to DF-REF-038 | Sections 11, 12.7 |
| TC-E8-018-01 to TC-E8-018-04 | Section 16 |
| The legacy endpoints `POST /admin/rule-versions` on the monolith base and its approve operation, and the screens SCR-39 and SCR-41 | Section 15 and section 19, carried as the rule-version template's and not as this feature's (GAP-0883) |
| The feature FEAT-ADM-13, its dependency FEAT-DVF-04 and the system Aric | Sections 1, 2, 12.2, 12.5 |
| Legacy key RWB-E8-018, story RWB-P4-E8018-APP, contract RWB-P4-E8018-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The fraud rules themselves: the fraud decision table, its package version, its approval and its evaluation are `rwb-decision`'s (P7), and the rule packages of this programme are RWB-P4-E2041-APP's and RWB-P4-E2042-APP's. This story reads the verdict and evaluates no rule.
- The X4 fraud screening, the deviation record, its hold and its return point: `rwb-deviation` (S8) and the feature FEAT-DVF-04, with its own stories.
- The case record and its fraud flag: the case, its status, its holds and the flag as P3 composes it are `rwb-case`'s (P3). This story reads the case and writes nothing of it.
- The integration file adapters, the interface configuration and the outbound items: `rwb-integration` (P2) under the ownership map. This story declares no P2 contract and builds no file path.
- The central decision ledger, the query API over `rwb_decision` and the chain verification: `rwb-decision` (P7); this story writes its own local chain and publishes it on `rwb.decision-record.v1`.
- The data products, their freshness calculation and the reconciliation that flags them: `rwb-source-data` (P1). This story reads the freshness and produces MSG-P1-001.
- The screen SCR-03 Case record, its referral panel and the composite route specification: RWB-PLT-N001-CON and the P3 screen work.
- The Aric interface itself: its protocol, its credentials, its contract and its ownership outside the bank (GAP-0882; ASM-1600). This story builds one adapter against it and fakes it.
- The integration harness and the `-ITG` copies of the test cases: no ITG story is split from this legacy key.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
