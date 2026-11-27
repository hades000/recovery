# RWB-P1-E1066-APP Interaction ledger store and writer

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1066-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-066 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P1-P |
| Ready to start | After the E1066-CON, rwb-access and reference-data contracts are published |
| Size | Not specified; pending squad refinement |
| Depends on (build) | RWB-P1-E1001-APP, RWB-P1-E1066-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E1018-CON, RWB-P7-E1027-CON, RWB-P4-E1037-CON (rwb-access) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7), path version v1 (/api/recovery/source-data/v1) |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1066-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v2.md (FR-P1-029, FR-P1-030) |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-008, RD-P1-009, RD-P1-021, RD-P1-023, RD-P1-045, RD-P1-064 |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- One writer, one append contract: InteractionRequest 5.1.0 on the case-scoped path, caller rights and the CASE_CREATED path ruled, no decision record, business-key repeat (RD-P1-007, RD-P1-008).
- Header replay, conflict and missing-header answers (RD-P1-001); status and message codes restated from the shared table, including MSG-GEN-007 for an event code outside the list (RD-P1-004).
- Acceptance criteria rewritten and AC23 to AC26 added; AC12 withdrawn; RWB-P1-DM005-APP and RWB-P1-E2034-APP named as in-process callers (RD-P1-007, RD-P1-021).
- Findings RWB-P1-E1066-APP#1 to #27 fixed or carried as pending with a gap ID (NEW-GAP-S8-1 to S8-7, NEW-GAP-S8-12, NEW-GAP-F14-1, NEW-GAP-F14-2).
- Batch D: caller conventions, service-identity permission rows and the dispatch and delivery references are ruled (RD-P1-064; NEW-GAP-F14-1 and NEW-GAP-F14-2 closed, superseding the fourth bullet); test case IDs TC-P1-E1066-APP-11 to -14 cited.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register); applied RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-008, RD-P1-009, RD-P1-021, RD-P1-023 and RD-P1-045; findings RWB-P1-E1066-APP#1 to #27.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-066 for rwb-source-data. The in-process `InteractionLedgerWriter.append()` of the monolith becomes a REST operation of this service, `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` on base `/api/recovery/source-data/v1` (DP-11, DP-13), and the `interaction` table becomes P1's own table in schema `rwb_source_data` (DP-01, DP-18; ownership ruling of R-PREC, the Ledger owned by rwb-source-data); the per-service Flyway sequence carries the column migration and the append-only trigger (DP-15), the case check of the monolith becomes a call to the rwb-case case contract and the decision-log reference a read of the rwb-decision contract (DP-11), and the Workbench events written from the outbox stay with RWB-P1-E1067-APP, the read interface with RWB-P1-E1068-APP and the case timeline with rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P1-E1066-APP-L140, X20 RWB-P1-E1066-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 20 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the append of one ledger entry on a case to be a REST operation of rwb-source-data that refuses a missing value, orders two appends that arrive at the same moment without a gap or a repeat, and answers 404 for a case that does not exist**, so that **the history of a case is written once, in order, and is never assembled after the fact**.

This is the application slice of legacy RWB-E1-066. It owns exactly three legacy criteria:

- **AC5** — a required value is missing: the append is refused, nothing is written and the missing field is named;
- **AC6** — two entries for one case at the same moment: both are written with consecutive `case_seq`, and no `case_seq` is missing or repeated;
- **AC7** — a case that does not exist: the append is refused with 404 and nothing is written.

It also delivers the sole writer component, InteractionLedgerWriter, and the REST append operation on /api/recovery/source-data/v1. The baseline already supplies the ledger columns, nullable channel and direction, the idempotency unique key, the append-only trigger and the case-time index; this story adds the missing unique key (case_id, case_seq). The writer reads back the stored row and uses the case and decision-log contracts. Inside rwb-source-data the writer is called in process, in the caller's own transaction, by RWB-P1-E1067-APP (ledger intake), RWB-P1-E2034-APP (channel entries) and the one-off cutover load of RWB-P1-DM005-APP (RD-P1-007 rule 1; RD-P1-021). RD-P1-007's final ruling lists the first two only; adding DM005 to that list is requested from the register owner.

It does **not** claim legacy AC1, AC2, AC3, AC4 or AC8. AC1 (the ledger exists and is written to), AC2 (it is ordered and complete), AC3 (it is distinct from the decision log), AC4 (a write failure is visible) and AC8 (an entry cannot be changed) are owned by the rwb-case and rwb-integration slices of this legacy key — the recording screens and event paths that call this writer and the outbox intake that rebuilds an entry from an event — and by the cross-service proof of RWB-ITG-E1066-ITG. This story builds the writer those slices call and tests only the three paths above.

### 2. Business rationale

Today the history of a recovery case is spread across EFS, LIT, letters and team spreadsheets, and an officer rebuilds it by hand before each decision. One append-only ledger per case, written in the same transaction as the action it records, gives one ordered history with no gap. The ledger records what happened with the customer; the decision log records why the system acted; each ledger entry for a decision points to its decision log entry. A ledger write that fails stops the action and raises an incident, so the history never has a silent gap. Serves REQ-ILG-001, REQ-ILG-002, REQ-ILG-004 and REQ-ILG-008; NFR-070 and NFR-077.

In the target the writer is a service of its own. The append is a REST contract with one hop and a 2 s timeout for external callers, including screens through gateway-bff and event paths of rwb-integration. RWB-P1-E1067-APP calls InteractionLedgerWriter in process in its own transaction (DP-11, DP-13, DP-19; Architecture v5 slide 11).

The ordering rule is the part that has to survive the move. In one transaction the monolith took an advisory lock on the case ID and read the highest `case_seq`; over REST two appends for the same case may arrive on two pods at once, so the allocation stays inside one database transaction on this service's own table, and the unique key `(case_id, case_seq)` is what makes a gap or a repeat impossible rather than unlikely. That is the whole of AC6, and it is why the ledger cannot be split across two schemas.

### 3. Preconditions

- RWB-P1-E1001-APP is done: schema `rwb_source_data` exists with the base `interaction` table, its standard record columns and the dictionary rows of P1 (legacy RWB-E1-001 in the target).
- The per-service Flyway sequence of rwb-source-data exists with its own history table in schema `rwb_source_data`, and the baseline version has been applied on it (DP-15; RWB-PLT-E1044-CON).
- RWB-P1-E1066-CON is published: the OpenAPI 3.1 document of the interaction-ledger resource, the `Interaction`, `InteractionRequest` and `InteractionPage` schemas, the error envelope, the Idempotency-Key rule and the contract fakes. This story builds against that contract and never against a second draft of it.
- RWB-P3-E1018-CON is published with its fake, so the case check of the append runs from Day 1 against `GET /api/recovery/case/v1/cases/{caseId}` and a 404 is answerable without rwb-case being built (DP-11).
- RWB-P7-E1027-CON is published with its fake, so a `DECISION_TAKEN` entry is written against `GET /api/recovery/decision/v1/decision-log/{entryId}` and a missing decision entry is answerable from Day 1 (DP-03, DP-11).
- RWB-PLT-E1027-CON (the local decision-record library) is on the classpath, RWB-PLT-E1043-CON is the client library of the reference data, RWB-PLT-TE006-CON is the outbox, inbox and idempotency library, and RWB-PLT-N001-CON is the gateway-bff composite route the recording screens arrive through (DP-03, DP-07, DP-09, DP-19).
- RWB-P3-E1043-CON is published with its fake, and the list **LOV-LEDGER-EVENT** is served as data through it with its 14 values: CONTACT, LETTER, PROMISE, PAYMENT, HANDOVER, CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, CASE_ESCALATED, DOCUMENT_ATTACHED, DECISION_TAKEN, CORRECTION, PARTNER_RESULT, OFFER (DP-07; Reference Data and Lists of Values v5; the same list as the `eventCode` enum of rwb-source-data.yaml).
- A user caller holds Case record C and the case scope in its token. A service caller uses its workload identity (rwb-case, rwb-comms, rwb-integration, rwb-document, rwb-payment, rwb-treatment, rwb-partner; RD-P1-007) and holds a service-identity row Case record C on rwb-source-data in Users Roles and Permissions and the Role to System Access Matrix (RD-P1-064). The retired data-load identity SY-DATALOAD is not a caller. A call made under the rwb-case workload identity with `actorType` SERVICE skips the case-exists read, because rwb-case appends before its own commit (RD-P1-007 rule 5).
- Caller conventions (RD-P1-064), which the writer stores as sent: PROMISE when the entry records a promise to pay, CONTACT otherwise; rwb-partner appends PARTNER_RESULT with `actorType` PARTNER; a customer answer is CONTACT, INBOUND, channel PORTAL, `actorType` SERVICE and `actorRef` the receiving service; SMS and LINE notices are CONTACT entries; the delivery business key is `LETTER-<caseNo>-<yyyyMMdd>-<UUID version 5 of podKey>`; on 503 MSG-P1-022 the caller does not commit its action, or retries with the same keys. Pending: no event code identifies a complaint, owner product owner with compliance (NEW-GAP-F10-02); HOME.SCB mapped to PORTAL awaits the product owner (NEW-GAP-F16-1).
- The roles `rwb_source_data` and the login of this service exist in DEV and SIT, and the credential is held by the platform and never appears in code, a test or a runbook (DP-02; Architecture v5 slides 11 and 29).
- The append path is the case-scoped `POST /cases/{caseId}/interactions` (ASM-3528, ASM-3542 confirmed; RD-P1-007 rule 2); the flat `/interactions` family is withdrawn from every story, fake and smoke test, and ASM-0696 and ASM-0697 are superseded. `caseId` is the case UUID; the case number is never a path or query key (RD-P1-023).

### 4. Flow

1. A REST caller posts to `/api/recovery/source-data/v1/cases/{caseId}/interactions` with an `InteractionRequest` and a UUID `Idempotency-Key` header. An in-process caller of section 1 invokes `InteractionLedgerWriter` in its own transaction and does not call the REST route.
2. `InteractionWriteController` applies the platform idempotency helper (step 10) and reads the body against `InteractionRequest`: a body that cannot be parsed answers 400, a well-formed body that fails the schema answers 422 (table in 12.1).
3. `CaseScopeClient` checks Case record C from the caller's token (a role without it: 403 MSG-P4-002) and then calls `GET /api/recovery/case/v1/cases/{caseId}` once, one hop, 2 s timeout, for case existence and scope. A 404 or a 403 from rwb-case answers 404 MSG-P4-003 to a user caller. The rwb-case workload identity with `actorType` SERVICE skips this read (RD-P1-007 rule 5). The answer to another service identity whose case read finds no case is pending (NEW-GAP-S8-7).
4. `ReferenceDataClient` reads **LOV-LEDGER-EVENT** through the rwb-case reference-data client library, so an event code is data and never a constant in the code (DP-07). The behaviour when the list cannot be loaded is pending (NEW-GAP-S8-6).
5. For a `DECISION_TAKEN` entry sent over REST, `DecisionLogClient` calls `GET /api/recovery/decision/v1/decision-log/{entryId}` once (2 s) to confirm `decisionLogId` and stores the identifier only: rule, version and inputs stay in rwb-decision (DP-03, DP-11). The answers for a missing `decisionLogId`, an unknown entry and an unanswered read are pending (NEW-GAP-S8-2).
6. `InteractionLedgerWriter` validates the request (12.1 field table). A required value that is missing is refused with 422 MSG-GEN-001, a value outside its list with 422 MSG-GEN-007, a value over its length with 422 MSG-GEN-002, each naming the `field`; nothing is written (AC5, AC18). The actor is stored as the body states it. The server sets `id`, `caseId` (from the path), `caseSeq` and `sourceSystem` (`WORKBENCH`; `EFS` only when the business key starts `EFS:`). `retentionClass` is not a request property; resolving it belongs to RWB-P1-E2034-APP (ASM-3541).
7. The writer opens one transaction, takes a transaction-level advisory lock derived from the case ID, reads the highest `case_seq` of the case and allocates the next one; the first entry of a case gets 1. The unique key `uk_interaction_case_seq` `(case_id, case_seq)` decides a race; a clash is retried once and a second clash answers 503 MSG-P1-022 with nothing written (AC6, AC19).
8. `InteractionRepository` inserts the entry. No update and no delete method exists on the repository. A `CORRECTION` is a new row whose `correctsEntryId` names an entry of the same case.
9. The stored row is read back through the repository inside the same transaction (never by an HTTP call of the service to itself) and returned as `Interaction` with 201. The append writes no decision record and no outbox row; the acting service records its own decision (RD-P1-007 rule 6).
10. Two keys apply. The header `Idempotency-Key` (UUID, kept 24 hours) governs HTTP replay: the same key and body replay the stored status and body; the same key with another body or path, or while the first call is in flight, answers 409 MSG-PLT-N009-05; a missing or non-UUID header answers 400 MSG-PLT-N009-03; an unavailable key store answers 503 MSG-PLT-N009-06 (RD-P1-001). The body `idempotencyKey` is the permanent business key, form `<code>-<caseNo>-<yyyyMMdd>-<actionId>` (EFS history keeps `EFS:<efs_record_key>`): a new header key with a business key already stored answers 200 with the existing entry and no new `caseSeq`, and 409 MSG-PLT-N009-05 when the request differs from that entry (RD-P1-007 rule 4). A producer that appends and publishes one action sends the same value in `ce_idempotencykey`.
11. A database failure rolls the transaction back and answers 503 MSG-P1-022; the caller treats it as a failed action. The writer raises no incident: `LEDGER_WRITE_FAILED` is raised by the calling service for its own refused action (RWB-P3-E1066-APP for rwb-case), and by the intake of RWB-P1-E1067-APP only when its retries are exhausted (RD-P1-009 rule 6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ledger cannot be written (insert fails, or a `case_seq` clash repeats after one retry) | Transaction rolls back; 503; nothing stored; the caller treats the action as failed; a retry with the same keys is not blocked | MSG-P1-022 | AC11, AC19 |
| X2 | A required value is missing, over its length or outside its list | 422 naming the field; nothing written | MSG-GEN-001, MSG-GEN-002, MSG-GEN-007 | AC5, AC18 |
| X3 | Two entries for one case at the same moment | Both written with consecutive case_seq; no gap and no repeat | None | AC6, AC19 |
| X4 | The case does not exist or is out of scope (404 or 403 from rwb-case) | 404 to a user caller; nothing written; no decision-log call | MSG-P4-003 | AC7, AC23 |
| X5 | Any change or delete of an entry | Refused by the append-only trigger; a correction is a new entry naming the original | None | AC17; trigger proved by RWB-P1-E1066-OPS and RWB-ITG-E1066-ITG |
| X6 | The rwb-case case read does not answer inside 2 s, or answers 503 | Append refused with 503; no entry; no scope answer is guessed from a cache | MSG-P1-022 | AC9, AC23 |
| X7 | No session, or a role without Case record C | 401 or 403; nothing written; refusal logged without personal data | MSG-P4-001, MSG-P4-002 | AC10 |
| X8 | Header key missing or not a UUID; header key reused for another request | 400 or 409; nothing written | MSG-PLT-N009-03, MSG-PLT-N009-05 | AC15 |
| X9 | `DECISION_TAKEN` reference missing, unknown or not answered | Nothing written; status and message pending (NEW-GAP-S8-2) | Pending (NEW-GAP-S8-2) | AC16 |
| X10 | `rwb.dataengine.ledger-writer` is off | The append path answers 404; nothing written (EDD v6 Table 8; RD-P1-045) | Pending (NEW-GAP-S8-1) | AC22 |

X2, X3 and X4 are the legacy exception paths of RWB-E1-066 that this slice owns; X1 and X5 are kept because this story ships the rollback and relies on the trigger. X6 is the path the cross-service scope check adds: in the monolith the scope was a local join that could not time out.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published interaction-ledger contract of this key and the rwb-case and rwb-decision contracts and their fakes from Day 1; needs the `rwb_source_data` baseline and its own sequence |
| Negotiable | The internal class split, the allocator's retry count and the read-back call are the squad's choice behind the contract; the table, its keys and its trigger are fixed |
| Valuable | One writer for every recording path, one ordered history per case and a refused write that names the missing field |
| Estimable | One migration, one controller, one service, one repository, and three clients |
| Small | Fits one sprint with its tests, as the writer slice of the legacy key |
| Testable | Every criterion in section 7 is one API call, one concurrent pair of calls or one refused call, on synthetic cases |

### 7. Acceptance criteria

```gherkin
Feature: Interaction ledger store and writer

  Background:
    Given case "RW-2026-000201" has 6 entries with caseSeq 1 to 6
    Given user "u-owner-02" has Case record C on that case

  Scenario: AC5 A required field is missing
    When the append omits `eventCode`, `occurredAt`, `actorType`, `actorRef`, `sourceRef` or `idempotencyKey`
    Then it answers 422 MSG-GEN-001 with the missing `field`
    Then the case still has 6 entries and no decision record or outbox row is written

  Scenario: AC6 Concurrent appends receive consecutive caseSeq values
    Given two append requests have different header and business keys
    When both append to the case concurrently
    Then both answer 201 and receive caseSeq 7 and 8 in either order
    Then exactly two rows are added and no sequence is skipped or repeated

  Scenario: AC7 A case is unknown or outside caller scope
    Given the case contract answers 404 for the synthetic case ID
    When the caller posts a complete append
    Then the response is 404 MSG-P4-003 and no row is written
    Then the decision-log contract is not called

  Scenario: AC9 The case read exceeds its timeout
    Given the case contract does not answer within 2 s
    When a complete append is posted
    Then the response is 503 MSG-P1-022 after one case-contract call
    Then no row is written

  Scenario: AC10 Authentication and case-record rights are enforced
    When a call has no valid token
    Then it answers 401 MSG-P4-001 and writes no row
    When a RW-AUDIT caller, with Case record R but not C, posts a complete append and the case fake would answer 200
    Then it answers 403 MSG-P4-002 and writes no row
    Then the refusal is logged without the summary

  Scenario: AC11 A failed ledger insert rolls back
    Given the interaction insert is forced to fail
    When a complete append is posted
    Then it answers 503 MSG-P1-022 and no interaction row is committed
    Then the writer raises no incident and writes no decision record
    Then the same request with the same keys is accepted once the insert succeeds

  # AC12 withdrawn: not applicable, this story has no status change (review finding 7)

  Scenario: AC13 A successful append returns its stored row
    Given the case has 6 entries and the request has a new header key and business key
    When a complete CONTACT append is posted
    Then it answers 201 with the stored row at caseSeq 7 and `sourceSystem` WORKBENCH
    Then the stored values equal the request values
    Then the append writes no decision record and no outbox row

  Scenario: AC14 A repeated business key does not add a row
    Given an entry exists with business key K
    When a request with a new `Idempotency-Key` uses business key K
    Then it answers 200 with the existing entry and caseSeq
    Then no row or new sequence is added
    When a request with another new `Idempotency-Key` uses business key K and a different `eventCode`
    Then it answers 409 MSG-PLT-N009-05 and no row is added

  Scenario: AC15 Header replay and header conflict are distinct
    Given a request with header key K was accepted with 201
    When the same body is sent again with header key K within 24 hours
    Then it answers the stored 201 and body with the same id and caseSeq, and no row is added
    When a different body is sent with header key K
    Then it answers 409 MSG-PLT-N009-05 and adds no row
    When the `Idempotency-Key` header is missing or is not a UUID
    Then it answers 400 MSG-PLT-N009-03 and adds no row

  Scenario: AC16 A DECISION_TAKEN reference is checked
    Given the decision-log fake holds entry E and not entry F
    When a DECISION_TAKEN append names `decisionLogId` E
    Then it answers 201 and the stored entry carries `decisionLogId` E and no rule, version or input
    When a DECISION_TAKEN append names `decisionLogId` F, or the fake does not answer within 2 s
    Then the append is refused and no row is written
    # Pending: status and messageCode of the refusal, and of a DECISION_TAKEN request without decisionLogId; owner solution architect; NEW-GAP-S8-2.

  Scenario: AC17 A CORRECTION names an entry from the same case
    Given a CORRECTION request has no `correctsEntryId`
    When the append is posted
    Then it answers 422 MSG-GEN-001 with `field` correctsEntryId and adds no row
    Given a CORRECTION request names an unknown entry or an entry of another case
    When the append is posted
    Then it answers 422 with `field` correctsEntryId and adds no row
    Given a CORRECTION request names entry caseSeq 3 of the same case
    When the append is posted
    Then it answers 201, caseSeq 7 carries `correctsEntryId` of caseSeq 3 and entry 3 is unchanged
    # Pending: messageCode of the unknown or other-case refusal; owner solution architect; NEW-GAP-S8-4.

  Scenario: AC18 Request limits and event values are enforced
    Given `eventCode` is "FAX", which is not in LOV-LEDGER-EVENT
    When the append is posted
    Then it answers 422 MSG-GEN-007 with `field` eventCode and adds no row
    Given `summary` has 2001 characters or `idempotencyKey` has 121 characters
    When the append is posted
    Then it answers 422 MSG-GEN-002 with the `field` and adds no row
    Given each of the 14 list values and a 2000-character summary
    When the append is posted with otherwise valid fields
    Then it is accepted

  Scenario: AC19 The first sequence and parallel allocation have no gap
    Given a case has no entries
    When N appends with different keys are processed in parallel
    Then the allocated caseSeq values are exactly 1 through N

  Scenario: AC20 CASE_CREATED skips the pre-commit case read for rwb-case
    Given the case fake would answer 404 for a case that rwb-case has not committed yet
    When rwb-case appends CASE_CREATED under its workload identity with `actorType=SERVICE`
    Then the writer does not call the case read and answers 201 with caseSeq 1
    When a user token posts to the same unknown case
    Then it answers 404 MSG-P4-003 and writes no row

  Scenario: AC21 Personal fields are masked on ledger reads
    Given the rwb-access masking fake allows the caller no unmasked `interaction.summary`
    When the caller reads one entry through GET /cases/{caseId}/interactions/{entryId}
    Then `summary` is returned as "MASKED" and the stored text appears in no log, incident or event
    # Masking rows by role and record class: GAP-1475 (open).

  Scenario: AC22 The writer feature flag is off
    Given `rwb.dataengine.ledger-writer` is off
    When a valid append is posted
    Then it answers 404 and no row is written
    # Pending: messageCode of this 404; owner solution architect; NEW-GAP-S8-1.

  Scenario: AC23 The case contract refuses or is unavailable
    Given the case fake answers 503, or the connection is reset
    When a complete append is posted by a user caller
    Then it answers 503 MSG-P1-022 and writes no row
    Given the case fake answers 403 for a case outside the caller's scope
    When the append is posted
    Then it answers 404 MSG-P4-003 and writes no row

  Scenario: AC24 One entry is read under its own case only
    Given entry E belongs to case "RW-2026-000201"
    When a caller with Case record R and scope reads E under that case
    Then it answers 200 with E
    When E is read under another case in the caller's scope
    Then it answers 404 MSG-P4-003 and returns no entry value

  Scenario: AC25 The server sets the source system
    Given a service append whose `idempotencyKey` is "EFS:SYN-EFS-000001"
    When it is accepted
    Then the stored `sourceSystem` is EFS
    When a REST append with any other business key is accepted
    Then the stored `sourceSystem` is WORKBENCH

  Scenario: AC26 In-process callers use the same writer
    Given the intake, channel and cutover callers of section 1
    When one of them appends inside its own transaction and that transaction rolls back
    Then no interaction row remains
    Then an architecture test fails any write to `interaction` outside `InteractionLedgerWriter`
```

Test Cases v9 holds AC23 to AC26 as TC-P1-E1066-APP-11 to -14.

**Target reading.** In-process callers of the writer are RWB-P1-E1067-APP, RWB-P1-E2034-APP and the cutover load of RWB-P1-DM005-APP; RWB-P1-E1055-APP does not call it. The append is `POST /api/recovery/source-data/v1/cases/{caseId}/interactions`; list and entry reads are case scoped. `InteractionLedgerWriter` is the only writer of `rwb_source_data.interaction`, and it is append only. The request body `idempotencyKey` is the permanent business key; the `Idempotency-Key` UUID governs HTTP replay. A new header key with a business key already stored returns 200 with the existing entry and no new `caseSeq`. The append writes no decision record. Proof-of-delivery entries are appended by rwb-comms over REST (RWB-P6-E1055-APP); DP07 repeats use metric `rwb_source_data_win_delivery_repeat_total`. The date-wide proof-of-delivery read writes nothing. EFS history is appended per row by the P2 hand-over run over REST; this story does not fold EFS rows. The case-action link table belongs to rwb-case.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One ledger holds every interaction on a case; no other record is the authoritative history | REQ-ILG-001; case file item "Interaction ledger" (casemodel.txt) |
| BR2 | Every entry carries case, event, time, actor and source | REQ-ILG-002 |
| BR3 | An offer, promise, payment or hand-over is recorded on the interaction it was made in | REQ-ILG-004; interaction.promise_amount |
| BR4 | Entries are append only; a correction is a new entry naming an original of the same case in `correctsEntryId` | tr_interaction_append_only (Recovery Workbench Physical Schema v9, rwb_source_data.sql); R-UNI-24 |
| BR5 | A ledger write that fails stops the action and raises an incident; no entry is discarded | REQ-ILG-008; CTL-06 |
| BR6 | The ledger records what happened; the decision log records why; a decision entry links the two | FEAT-ILG-02; ADR-009 |
| BR7 | Entries of one case carry a gap-free sequence | REQ-ILG-001; interaction.case_seq |
| BR8 | Field limits: `actorRef` 64, `sourceRef` 60, `idempotencyKey` 120, `summary` 2000, `actionCode` 10, `externalRef` 60, `contactKey` 255, holder references 60 characters; `promiseAmount` numeric(18,2) | rwb-source-data.yaml 5.1.0 InteractionRequest; Physical Schema v9 |
| BR9 | A `DECISION_TAKEN` entry stores the decision-log reference only; an append writes no decision record | RD-P1-007 rule 6 |

**Where each rule lives in the target.** BR1 is now a schema rule as well as a business rule: the `interaction` table exists once, in `rwb_source_data`, and no other service's schema holds a copy, so "one ledger" is enforced by the schema boundary and not only by convention (DP-01, DP-18). BR2 and BR3 are the append's validation and its insert: the required values are checked against the published `InteractionRequest` schema and the LOV-LEDGER-EVENT list (DP-07), and the promise fields are written on the entry they belong to. BR4 is the append-only trigger on the service's own migration plus the absence of any update or delete method on the repository; a correction is a second insert with `corrects_entry_id`, and the schema still has no update path for application code (DP-15). BR5 keeps its shape but crosses a boundary: the database failure is translated into a 503 with MSG-P1-022 at this service. The incident `LEDGER_WRITE_FAILED` has one raiser per path: the calling service for its own refused action, and the intake of RWB-P1-E1067-APP after exhausted retries; this story ships the rollback and no incident hook (RD-P1-009 rule 6). BR6 becomes the split between P1's ledger entry and rwb-decision's decision-log entry, joined by `decision_log_id`: the entry carries the reference and never the rule, the version or the inputs, which are read through the rwb-decision decision-log contract (DP-03, DP-11; RWB-P7-E1027-CON). BR7 is the allocator and the unique key `(case_id, case_seq)` inside one database transaction per case.

### 9. State transitions

None in the business sense. This story does not change a case status. It adds ledger entries; an entry has no status and is never changed.

| From | Event | Condition | To |
|---|---|---|---|
| a case at case_seq n | a valid append | The case check answers and the body validates | The case is at case_seq n+1 and one entry exists |
| a case at case_seq n | a refused append | A required value is missing, or the case is unknown | The case is still at case_seq n and no entry exists |
| a case at case_seq n | a ledger write fails | The ledger cannot be written (MSG-P1-022) | The case is still at case_seq n and no entry exists |
| an applied migration version | a correction | The ledger columns or the trigger need a fix | A new Flyway version is merged; the applied version is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Records contacts and promises on own cases (Case record C, scope Own) through the recording screens and gateway-bff |
| RW-TEAMMGR, RW-PHONECOL and other case roles | Read entries only in this story (Case record R) |
| SY-CASEWF, case workflow module | Appends entries for case actions (Case record C) over the writer contract |
| rwb-integration and other service identities (rwb-comms, rwb-document, rwb-payment, rwb-treatment, rwb-partner) | Append over REST under their workload identity (RD-P1-007); the retired SY-DATALOAD identity is not used |
| RW-AUDIT, internal audit | Reads only; may not record (Case record R) |
| RW-PLATADM, platform administrator | Receives the LEDGER_WRITE_FAILED incident and reads the append series of the deployment |
| rwb-case (P3) | Owns the case, its scope and the case timeline; answers the case check this writer takes (C RWB-P3-E1018-CON) |
| rwb-decision (P7) | Owns the central decision ledger; answers the decision-log reference this writer confirms (C RWB-P7-E1027-CON) |

The append runs as the service identity of rwb-source-data (DP-02), and the caller's identity travels in the token. Case record C is checked from that token by the service's capability check; the case read of 12.2 confirms existence and scope and is not the right check (RD-P1-007 rule 5). No rwb-access authorise call is made by the append; the entry read follows the read controls of RWB-P1-E1068-APP. Pending: whether a user token's `actorRef` must equal its subject (NEW-GAP-S8-7).

**Open decisions.** DL10 (Thai texts) is worked on recommended option A: the business lead drafts per module one epic ahead and Legal and Compliance approve; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive. DL26 (retention periods) is open and does not change the append.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-INT-014 | interaction | event_code | Write |
| DF-INT-015 | interaction | actor_type | Write |
| DF-INT-016 | interaction | actor_ref | Write |
| DF-INT-017 | interaction | source_ref | Write |
| DF-INT-018 | interaction | idempotency_key | Write |
| DF-INT-019 | interaction | case_seq | Write |
| DF-INT-020 | interaction | decision_log_id | Write |
| DF-INT-021 | interaction | corrects_entry_id | Write |
| DF-INT-022 to DF-INT-029 | interaction | contact_key, from_holder_ref, to_holder_ref, treatment_id, proceeds_id, delivery_status, external_ref (written when sent); retention_class (not written by this story) | Write |
| DF-CAS-001 | recovery_case | id | Read (through the rwb-case case contract, not from the table) |
| DF-DEC-001 | decision_log_entry | id | Read (as a reference through the rwb-decision contract) |
| DF-DEC-003 | decision_log_entry | decision_code | Read (reference only) |
| DF-DEC-004 | decision_log_entry | rule_id | Read (reference only) |
| DF-DEC-005 | decision_log_entry | rule_version | Read (reference only) |
| DF-DEC-008 | decision_log_entry | inputs_ref | Read (reference only) |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read (reference only) |

Field IDs are those in the Logical Data Model and Data Dictionary.

The baseline already supplies the ledger columns event_code, actor_type, actor_ref, source_ref, idempotency_key, case_seq, decision_log_id and corrects_entry_id, nullable channel and direction, the idempotency unique key, append-only trigger and case-time index. This story adds only the missing unique key (case_id, case_seq). DF-DEC-001 to DF-DEC-010 are rwb-decision's rows in rwb_decision and are read through its contract; DF-CAS-001 stays in rwb_case and is read through the case contract. The append-only trigger is a database object, not an LDM field. actor_ref is Confidential under Data Classification v5 R234 and summary is Restricted under R229; `personKey` and `contactKey` are references and never a name, number or address. A caller with no unmasking rule receives `summary` as "MASKED" (RWB-P1-E1068-APP); masking rows by role and record class are GAP-1475. `externalRef` and the holder references are never written to a log. The contract property `documentId` (DOCUMENT_ATTACHED) has no column in Physical Schema v9: the column is pending (NEW-GAP-S8-12). Entries written before RWB-P1-E2034-APP resolves retention classes carry none and cannot be updated (NEW-GAP-S8-5). The columns and `uk_interaction_case_seq` are in Physical Schema v9.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/source-data/v1` (DP-13). The append and the read of one entry, on the interaction-ledger resource of RWB-P1-E1066-CON (rwb-source-data.yaml 5.1.0). The list read `GET /cases/{caseId}/interactions` is built by RWB-P1-E1068-APP.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/interactions` (`postCasesCaseidInteractions`) | New business key: 201 with the stored entry; business key already stored: 200 with the existing entry and no new caseSeq | Case record C; service callers by workload identity; in-process callers use the writer | UUID `Idempotency-Key` required (RD-P1-001); body `idempotencyKey` is the permanent business key |
| GET | `/cases/{caseId}/interactions/{entryId}` (`getCasesCaseidInteractionsEntryid`) | One entry of the case; 404 MSG-P4-003 when the entry is not on that case | Case record R and case scope; summary masked as in RWB-P1-E1068-APP | Idempotent read; no key |

**InteractionRequest 5.1.0.**

| Property | Required | Type and limit | Rule |
|---|---|---|---|
| `eventCode` | Yes | enum of `Interaction.eventCode` (14 values) | Outside the list: 422 MSG-GEN-007 |
| `occurredAt` | Yes | date-time with offset | A rule for future values is pending (NEW-GAP-S8-4) |
| `actorType` | Yes | USER, SERVICE, PARTNER | Stored as sent |
| `actorRef` | Yes | string, at most 64 | Stored as sent |
| `sourceRef` | Yes | string, at most 60 | Producing module and event, or interface |
| `idempotencyKey` | Yes | string, at most 120 | Business key `<code>-<caseNo>-<yyyyMMdd>-<actionId>`; `EFS:<efs_record_key>` for history |
| `channel`, `direction`, `contactResult` | No | LOV-CHANNEL, LOV-DIRECTION, LOV-CONTACT-RESULT | Empty for Workbench events; `contactResult` replaces `result` |
| `actionCode`, `summary` | No | at most 10; at most 2000, personal data | `summary` never logged |
| `promiseAmount`, `promiseDate` | No | number, numeric(18,2); date | Carried on the interaction they were made in |
| `contactKey`, `conductCheck`, `deliveryStatus`, `externalRef` | No, conditional for LETTER | at most 255; PASSED, BLOCKED, NOT_APPLICABLE; SENT, DELIVERED, READ, FAILED; at most 60 | LETTER conditions are owned by RWB-P1-E2021-APP: `conductCheck` required when `deliveryStatus` is SENT or absent, `externalRef` required when `deliveryStatus` is present. Caller values (RD-P1-064): a dispatch entry carries `conductCheck` PASSED and `externalRef` = the WIN barcode; a letter refused by the conduct check carries `conductCheck` BLOCKED with no `deliveryStatus` and no `externalRef`; a delivery entry carries `externalRef` = barcode, else notice reference, so the two pair |
| `decisionLogId`, `correctsEntryId` | No; `correctsEntryId` required for CORRECTION | uuid | AC16, AC17 |
| `fromHolderRef`, `toHolderRef`, `treatmentId`, `proceedsId`, `documentId` | No | at most 60; at most 60; uuid | `documentId` column pending (NEW-GAP-S8-12) |

The caller never sends `id`, `caseId`, `caseSeq`, `sourceSystem` or `retentionClass`. Missing a required property answers 422 MSG-GEN-001 with `field`.

**Errors** (published `Problem` body, RD-P1-004):

| Condition | Status | messageCode |
|---|---|---|
| Body not parseable | 400 | MSG-GEN-001 |
| Required value missing; value over its length; value outside its list | 422 | MSG-GEN-001; MSG-GEN-002; MSG-GEN-007 |
| `Idempotency-Key` missing or not a UUID | 400 | MSG-PLT-N009-03 |
| Header key reused or in flight; business key with a different request | 409 | MSG-PLT-N009-05 |
| Idempotency store unavailable | 503 | MSG-PLT-N009-06 |
| No session; no Case record C; case or entry missing or out of scope | 401; 403; 404 | MSG-P4-001; MSG-P4-002; MSG-P4-003 |
| Ledger cannot be written, or the case read fails or exceeds 2 s | 503 | MSG-P1-022 |

The caller's own budget is 2 s (RWB-P3-E1066-APP) and the append makes up to two reads of 2 s each; the server time budget that keeps the append inside the caller's budget is pending (NEW-GAP-S8-3).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | At most once per append (skipped for the rwb-case workload identity): case existence and scope; a 404 or 403 answers 404 MSG-P4-003 to a user caller | DP-11; C RWB-P3-E1018-CON; faked |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | Only for a `DECISION_TAKEN` entry: confirms the reference and returns nothing that is stored except the identifier | DP-03, DP-11; C RWB-P7-E1027-CON; faked |

Both calls are one hop with a 2 s timeout and a breaker per downstream (DP-11; Architecture v5 slide 11). The reference list **LOV-LEDGER-EVENT** reaches this service through the rwb-case reference-data client library and not as a run-time call of its own (DP-07; C RWB-P3-E1043-CON). No other service is called, and no table of another service is read (DP-01).

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP and are published in RWB-P1-E1015-CON (RD-P1-022). The ledger append publishes no decision record. Each acting service records its own decision through the decision-record library; the shared type is `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`.

#### 12.4 Events consumed

None. REST callers use the append; the ledger intake from business events is RWB-P1-E1067-APP, which consumes the three intake topics (RD-P1-009) and calls the writer in process.

#### 12.5 Workflows and activities

None. The append is a synchronous REST step and writes one row in one transaction. The Temporal activities `listEligibleAccounts` and `snapshot(page)` and the workflows `AceIngestCheck` and `reconciliation` of Architecture v5 slide 15 are other P1 stories; the task queue of this service is `rwb-source-data` in namespace `rwb-recovery`, and this story starts no workflow and no activity on it.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story.

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `interaction` | `rwb_source_data` | P1 rwb-source-data | The baseline already supplies the ledger columns, nullable `channel` and `direction`, `uk_interaction` (idempotency key), the append-only trigger and the case-time index. This story's migration adds `uk_interaction_case_seq (case_id, case_seq)` and uses append and read operations only |
| `processed_event` | `rwb_source_data` | PLT library, created in this service's schema | Not used by the append; it holds the intake redeliveries of RWB-P1-E1067-APP (RD-P1-001 rule 7) |
| `idempotency_key` | `rwb_source_data` | PLT library, created in this service's schema | The stored response of the append (24 hours); read and written by the library |
| `outbox_event` | `rwb_source_data` | PLT library, created in this service's schema | Not used: the append writes no decision record and no event (RD-P1-007) |

No table of another service is read and no foreign key crosses a schema (DP-01). The decision-log table `decision_log_entry` stays in `rwb_decision` and the case table `recovery_case` stays in `rwb_case`; both are reached over their contracts only.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P3-E1018-CON fake | `GET /api/recovery/case/v1/cases/{caseId}` | A case in scope, a case out of scope (403), a 404 for the synthetic case ID of AC7, a 503 and a timeout |
| RWB-P4-E1037-CON fake | rwb-access roles and masking | Token roles u-owner-02 (RW-CASEOWN, Case record C) and RW-AUDIT (R only) for AC10; a masking answer with and without unmasking for AC21 |
| RWB-P7-E1027-CON fake | `GET /api/recovery/decision/v1/decision-log/{entryId}` | A decision entry with code, rule, version and inputs reference, and a missing entry |
| RWB-P3-E1043-CON fake | The reference-data contract | The 14 values of LOV-LEDGER-EVENT, a value outside the list, and the Thai labels |
| Ledger fixture | `rwb_source_data` | A container at the baseline plus this story's migration, with the interaction table, its two unique keys and its trigger, so the concurrency test of AC6 runs on the real keys |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/source-data/v1` | `GET /api/recovery/case/v1/cases/{caseId}`, `GET /api/recovery/decision/v1/decision-log/{entryId}`; the masking read of the entry read | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11) |
| Kafka | None | None | The ledger append consumes and publishes no event and creates no decision record |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `ledger`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), Temporal task queue `rwb-source-data` in namespace `rwb-recovery` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data only through rwb-source-data's own contract or views; this story reads no ACE data | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case and the client library | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox, inbox and idempotency library in this service's schema; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/source-data/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The append writes no decision record. Each acting service records its own decision through the decision-record library; an append may store only a `decisionLogId` reference. DP-03 in the table above therefore applies to the acting service, not to this writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| V<next>__rwb_e1_066_interaction_ledger.sql (next version on the service sequence) | Migration | Adds `uk_interaction_case_seq (case_id, case_seq)`; ledger columns, nullable channel and direction, idempotency key, append-only trigger and case-time index already exist. Expand-only; never reversed (RD-P1-045) |
| `InteractionWriteController` | Controller | The two operations of 12.1; `Problem` bodies; `Idempotency-Key` helper |
| `InteractionLedgerWriter` | Service | The one write path for REST and in-process callers: validation, source-system rule, allocator, insert, read-back |
| `InteractionRepository` | Repository | Inserts and reads interaction rows; no update and no delete method exists |
| `Interaction` | Entity | Immutable mapping of the interaction table |
| `CaseScopeClient` | Client | The rwb-case case contract: one hop, 2 s timeout, 404 passed on unchanged (DP-11) |
| `DecisionLogClient` | Client | The rwb-decision decision-log contract, for the reference of a `DECISION_TAKEN` entry (DP-03) |
| `ReferenceDataClient` | Client library use | Reads LOV-LEDGER-EVENT as data; no event code in code (DP-07) |

**Migrations and sequence (DP-15).** The migration sits on rwb-source-data's own Flyway sequence after the baseline and adds the missing unique key (case_id, case_seq) in schema rwb_source_data. The baseline already supplies the ledger columns, nullable channel and direction, the idempotency unique key, append-only trigger and case-time index. The exact version number is assigned by the sequence owner at build time, and an applied version is never edited.

**Database.** This story owns one table's shape: the `interaction` table in `rwb_source_data`. It creates no table of another service, adds no foreign key across a schema, and reads `decision_log_entry` and `recovery_case` over their contracts only (DP-01).

**Configuration and reference data**

- The list LOV-LEDGER-EVENT with its 14 values and its Thai labels is reference data of rwb-case, read through the client library and never written in the code (DP-07). Behaviour when it cannot be loaded: pending (NEW-GAP-S8-6).
- The 2 s budget of the two consumed calls, the breaker and the bulkhead are configuration of the clients (DP-11).
- The flag `rwb.dataengine.ledger-writer` gates the writer at deployment (RWB-P1-E1066-OPS).
- The case-scope answer is never cached across calls: a stale answer would be a scope leak, and a call that does not answer inside 2 s refuses the append (X6).

**Build steps**

1. Add the missing unique key (case_id, case_seq) after confirming the baseline ledger columns, nullable channel and direction, idempotency unique key, append-only trigger and case-time index; verify a repeated migration changes nothing.
2. `InteractionLedgerWriter` validation against LOV-LEDGER-EVENT and the field table of 12.1, naming the field and inserting nothing on a refusal (AC5, AC17, AC18).
3. The `case_seq` allocator: a transaction-level advisory lock derived from the case ID and `max(case_seq)` plus one starting at 1, one retry on a unique-key clash then 503, and tests with two and with N parallel connections (AC6, AC19).
4. The insert and repository read-back, so a new append returns 201 with the stored entry and caseSeq.
5. The token capability check and the two clients of 12.2, each with its 2 s budget and its fake (AC7, AC9, AC10, AC16, AC20, AC23).
6. The `Idempotency-Key` handling through the platform library and the business-key repeat of the writer (AC14, AC15).
7. The failure path: the database error becomes a 503 with MSG-P1-022 and a log line with the case ID and the error class only (AC11).
8. An architecture test that no class outside the `ledger` module uses `InteractionRepository`, and that the repository has no update and no delete method.
9. Tests for AC5 to AC7, AC9 to AC11 and AC13 to AC26 with the fakes of 12.8.

**Feature flag.** `rwb.dataengine.ledger-writer`. Off, the append path answers 404 and no entry is written (EDD v6 Table 8; RD-P1-045); the messageCode of that answer, and whether the flag also gates the in-process writer, are pending (NEW-GAP-S8-1). Rollback: flag off first, previous image only if the flag does not cover the fault, no migration reversed (RD-P1-045).

**Done when.** The tests of section 16 pass, `uk_interaction_case_seq` is applied on the service sequence with the trigger in place, a valid append answers 201 against the fakes, parallel appends for one case yield consecutive case_seq with no gap, and a missing value and an unknown case are refused with nothing written.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The ledger write failed (new, see additions) | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-GEN-001 | A required value is missing, or the body cannot be parsed | Enter {field}. |
| MSG-GEN-002 | A value is over its length | {field} must be between {min} and {max}. |
| MSG-GEN-007 | A value is not in its list | {value} is not a valid value for {field}. Choose a value from the list. |
| MSG-PLT-N009-03 | `Idempotency-Key` missing or not a UUID | Platform text (Error and Message Standard v6) |
| MSG-PLT-N009-05 | Key reused with another request, or in flight | Platform text (Error and Message Standard v6) |
| MSG-PLT-N009-06 | Idempotency store unavailable | Platform text (Error and Message Standard v6) |
| MSG-P4-001 | No valid session or no Workbench role | Platform text (Error and Message Standard v6) |
| MSG-P4-002 | Role without Case record C | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case missing or out of scope | This case is not in your scope. |

Thai text for each message follows decision DL10. MSG-P4-002 and MSG-P4-003 are raised by the case check and passed on unchanged; the field name of MSG-GEN-001 is filled from the validation failure and is never a data value.

### 15. Screens and states

No screen in this story. In Epic 1 a contact is recorded through the recording screens of the rwb-case slice, which arrive through gateway-bff (DP-19; RWB-PLT-N001-CON) and call this writer; the case record view SCR-03 (Read only; its empty, loading, error and no access states: Not specified in the source documents (CG-ALL-2294)) shows ledger entries through the read interface of RWB-P1-E1068-APP. On a refused or failed append the caller sees the message of the table in 12.1 in the Error state of the recording screen; this story renders none of it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-066-05 | AC5 | End to end | Append with one required property omitted |
| TC-E1-066-06 | AC6, BR7 | End to end | Two concurrent appends on one case |
| TC-E1-066-07 | AC7 | End to end | Unknown case ID |
| TC-E1-066-12 | AC9 | End to end | rwb-case contract does not answer inside 2 s |
| TC-E1-066-13 | AC10 | End to end | No token (401); caller without Case record C (403) |
| TC-E1-066-14 | AC11 | End to end | Forced insert failure rolls back; no incident from the writer |
| TC-P1-E1066-APP-01 | AC13 | Component | Valid CONTACT append at caseSeq 7 |
| TC-P1-E1066-APP-02 | AC14 | Component | Business-key repeat, same and different request |
| TC-P1-E1066-APP-03 | AC15 | Component | Header replay, conflict, missing and non-UUID header |
| TC-P1-E1066-APP-04 | AC16 | Component | Known and unknown decision-log reference |
| TC-P1-E1066-APP-05 | AC17 | Component | CORRECTION without, with foreign and with same-case reference |
| TC-P1-E1066-APP-06 | AC18 | Component | "FAX", over-length values, the 14 list values |
| TC-P1-E1066-APP-07 | AC19 | Component | First entry and N parallel appends |
| TC-P1-E1066-APP-08 | AC20 | Component | rwb-case workload identity before commit |
| TC-P1-E1066-APP-09 | AC21 | Component | Entry read without unmasking rule |
| TC-P1-E1066-APP-10 | AC22 | Component | Writer flag off |
| TC-E1-066-11 | 12.7 boundary | Component | Duplicate (case_id, case_seq) and idempotency key; UPDATE and DELETE on an entry |
| TC-P1-E1066-APP-11 | AC23 | Component | Case fake 503, connection reset, 403 |
| TC-P1-E1066-APP-12 | AC24 | Component | Entry read under own and another case |
| TC-P1-E1066-APP-13 | AC25 | Component | EFS business key and a Workbench business key |
| TC-P1-E1066-APP-14 | AC26 | Component | In-process rollback and architecture test |

TC-E1-066-01 to -04 and -08, -09 are regression evidence of the legacy slices that own those criteria and are not run for this story. TC-E1-066-10 names the withdrawn flat entry path and TC-E1-066-15 tests the withdrawn AC12; both need correction in Test Cases v9.

### 17. Guardrails

- No business value in code: event codes are list values of LOV-LEDGER-EVENT read through the reference-data contract; channels, directions and results come from their lists; the case-scope answer and the 2 s budget are configuration.
- No personal data in logs, tests, events or prompts: a failure log names the case ID and the error class only; the summary is never logged; test summaries are synthetic; `summary` (Restricted) is masked at the read and `actorRef` (Confidential) is never put in a log message.
- No read of another service's tables: the case is read through the rwb-case case contract, the decision entry through the rwb-decision contract, and the `interaction` table is written only through this story's service and read only through its contract and the read interface (DP-01, DP-03, DP-11).
- No entry is ever updated or deleted by application code: the trigger refuses the statement and the repository has no such method.
- One login, one schema and one sequence: the release carries the `rwb_source_data` login, migrates `rwb_source_data` only, and an applied migration version is never edited (DP-02, DP-15).
- The append is one hop, 2 s, with a breaker per downstream; a slow case answer refuses the append and writes nothing (DP-11).
- The platform library objects stay the library's: `processed_event`, `idempotency_key` and `outbox_event` are created in this schema and are never redefined by this story (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-001 | One ledger holds every interaction on a case (decision RD-P1-007) | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-02 | All recovery processes | R-UNI-24 | TC-E1-066-02, TC-E1-066-06, TC-E1-066-08 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-066-01, TC-E1-066-03, TC-E1-066-05, TC-E1-066-07 |
| REQ-ILG-004 | Offer, promise, payment or hand-over recorded on its interaction | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | None | TC-E1-066-01 |
| REQ-ILG-008 | A failed ledger write raises an incident; no entry discarded | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-05 | All recovery processes | CTL-06 | TC-E1-066-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1066-CON | Contract | H build dependency: the interaction-ledger contract this story implements, its schemas, its error envelope and its fakes |
| RWB-P1-E1066-OPS | DevOps | X external dependency: the chart, the migration step, the flag, the five series and the three alerts of the writer |
| RWB-P1-E1067-APP | App development | Sibling of the same legacy key: the outbox path that turns a Workbench event into an append, and the duplicate rule |
| RWB-P1-E1068-APP | App development | Sibling of the same legacy key: the read interface and its filters |
| RWB-P3-E1018-APP | App development | Sibling: the rwb-case recording screens that call this writer, and the case timeline that reads the ledger through this contract |
| RWB-ITG-E1066-ITG | Integration | Proves AC1, AC2, AC3, AC4 and AC8 against the live contracts and the live ledger |
| RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the reference-data client library, the outbox and inbox library, the per-service Flyway sequence and the gateway-bff composite route |
| RWB-P3-E1043-CON, RWB-P3-E1018-CON, RWB-P7-E1027-CON | Contract | C: the reference-data contract, the case contract and the decision-log contract, each with its fake |

### 19. Out of scope

- Writing the Workbench events from the outbox to the ledger and duplicate rejection across event paths (RWB-P1-E1067-APP).
- The ledger read interface, its filters and its paging (RWB-P1-E1068-APP).
- The case timeline, the case record view and the recording screens of rwb-case (RWB-P3-E1018-APP); this story serves them and builds none of them.
- The append-only behaviour as a business proof and the second row of a correction (RWB-ITG-E1066-ITG); this story ships the trigger and the insert. The database deployment of the trigger, of the two unique keys and of the index is RWB-P1-E1066-OPS.
- The central decision ledger of rwb-decision, its entries, its rules and its versions (RWB-P7-E1027-CON and the P7 stories); this story reads a reference and stores the identifier.
- The decision-record library, the outbox relay and the idempotency store as platform components (RWB-PLT-E1027-CON, RWB-PLT-TE006-CON).
- The reference data itself, its values and its Thai labels (rwb-case, RWB-P3-E1043-CON).
- Contact and dispatch outcomes from EFS, WIN, SMS and LINE, partner hand-overs and the timeline view (RWB-E2-034 in the legacy set and the integration slices of this key).
- The retention class resolution for ledger entries (FEAT-ILG-10, RWB-P1-E2034-APP); this story accepts no class from a caller and writes none.
- The gateway-bff composite route and the screen rendering of a masked summary (RWB-PLT-N001-CON and the screen owners).

### Remaining delivery steps

- Size the story at refinement; owner: squad.
- Obtain epic design sign-off; owner: product owner.
- Publish the contract and matching fake; owner: contract owner.
- Add or update story tests in Test Cases v9 (W2-tests); owner: test writer.
- Run the required test data in DEV after implementation; owner: delivery team.
- Rule the masking rows by role and record class; owner data steward; GAP-1475.
- Rule the decision-log reference refusals; owner solution architect; NEW-GAP-S8-2.
- Rule the flag-off messageCode and its effect on the in-process writer; owner solution architect; NEW-GAP-S8-1.
- Rule the server time budget of the append; owner solution architect; NEW-GAP-S8-3.
- Rule the future-date rule and the correction messageCode; owner solution architect; NEW-GAP-S8-4.
- Rule the retention class of entries written before RWB-P1-E2034-APP; owner compliance (DL26); NEW-GAP-S8-5.
- Rule the behaviour when the reference list cannot be loaded; owner solution architect; NEW-GAP-S8-6.
- Rule the service-identity case 404 answer and the user actor check; owner solution architect with compliance; NEW-GAP-S8-7.
- Add the `document_id` column or withdraw `documentId`; owner data architect; NEW-GAP-S8-12.
- Add RWB-P1-DM005-APP to the in-process callers of RD-P1-007; owner register writer.
