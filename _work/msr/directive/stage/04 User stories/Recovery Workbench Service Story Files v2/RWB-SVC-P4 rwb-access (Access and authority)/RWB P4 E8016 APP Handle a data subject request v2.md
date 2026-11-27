# RWB-P4-E8016-APP Handle a data subject request

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BJ |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E8016-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Contract version | v1: REST base /api/recovery/access/v1, as fixed by RWB-P4-E8016-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Size | Set by the squad at refinement (DOR-RWB-P4-E8016-APP-16) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-016 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8016-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 10 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **compliance and PDPA officer**, I want **a PDPA access, correction or erasure request opened, worked and answered from one register that checks the right, holds the statutory due date as a parameter of the platform, records the correction and the erasure as decisions of this service, writes the masking rows an erasure needs, and answers the access evidence from the access entries of this service**, so that **every data subject request is answered inside the statutory period and the answer, its decisions and its evidence can be shown afterwards without asking another team**.

Inside `rwb-access` this is the data subject request of the legacy story RWB-E8-016:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Four operations, and nothing else: the open `POST /api/recovery/access/v1/admin/data-subject-requests`; the decision `PATCH /api/recovery/access/v1/admin/data-subject-requests/{requestId}`, which records the correction or the erasure decision and the answer under an `If-Match`; the read `GET /api/recovery/access/v1/admin/data-subject-requests/{requestId}`; and the list `GET /api/recovery/access/v1/admin/data-subject-requests`, paged.
- The register is the local decision-record chain of DP-03, not a table of its own: one entry per step of a request, written with the record code of a data subject request, hash-linked and published as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`. The service creates no new table for the register and copies no row of it.
- The statutory due date is a parameter row of `rwb-case` read through DP-06 at its version in force, and it is never a constant in code. The row's name, its value and its unit are Not specified in the source documents (GAP-0875; ASM-1590); NFR-043 states the target as "Statutory period, Not set as a working service level" and marks it "Open, DL26".
- An erasure writes `masking_rule` rows (DF-REF-198 to DF-REF-204) for **every** role with `unmasked` false from a `valid_from` and moves `masking_version` on by one, in the transaction that records the decision. The masking policy itself, which field a role may see, belongs to RWB-P4-E1037-APP; this story only executes the erasure against it.
- A correction records the field ids corrected and **no value**: the decision carries the case ids, the field ids, the person reference, the time and the role code, and the value is not read, not copied and not written here (NFR-040).
- The access evidence of an access request is answered from this service's own access entries, the `AC-READ`, `AC-EXPT` and `AC-DENY` entries of the local chain written by RWB-P4-E1039-APP, read through that capability's own read `GET /api/recovery/access/v1/admin/access-log` (API-P4-008) filtered by the case ids of the request. The workbench-wide answer across the other eighteen services is the central ledger's query and is not this story's (GAP-0877; ASM-1592).
- The request is reached from SCR-47 Personal data through the gateway-bff composite route of DP-19, which shows the register and calls the four operations; this story renders no screen of its own.
- This story starts no workflow, owns no Schedule and publishes no event of its own: opening, deciding and answering are synchronous, the due date is data and not a timer, and the only message it produces is `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1`.
- The legacy story's two endpoints (a rule-version load and a rule-version approval) and two of its three data rows are not this capability's; the split keeps the capability, the criteria, the messages and the test ids and drops the copied rule-change apparatus (GAP-0878; ASM-1593).

### 2. Business rationale

A data subject request is a statutory obligation with a clock on it. NFR-043 asks that an access, correction or erasure request be answered inside the statutory period, and REQ-S8-007 (Must) asks that the request hold automated processing on the case and route to Compliance inside the same period; R-UNI-11 is the routing rule behind it, a universal rule that moves a case to `HELD_LEGAL` when a PDPA access, correction or erasure request is received. The legacy story carried the capability as one administration journey of the monolith (FEAT-ADM-11, RWB-E8-016), where the request, the masking rows and the decision log were rows of one schema and the request was worked on a screen of the same module. In the target the masking policy is a table of `rwb-access` (P4, slide 41), the case and its hold are `rwb-case`'s and `rwb-deviation`'s, the parameters are `rwb-case`'s under DP-06, and the record of who decided what is the decision record (ADR-022). So a data subject request is no longer a single screen: it is a decision that needs an authority, a register, a due date that lives as data, and a masking write that is the erasure.

This story is that register. It meets NFR-043 on the side this service can hold: the request exists with a due date computed from the parameter row in force, every step is a recorded decision, and the answer names the evidence. It supports REQ-S8-007 on the Compliance side, while the hold on the case stays with `rwb-case` and `rwb-deviation`, which own the case state and the rule that moves it. It carries the FSD target measure of the administration features: rule and limit changes made without a code release, 100 percent, measured monthly from the decision record (FSD P4 v3 A2.27.1). The statutory period is a row, the field set of a correction is data, and neither needs a release.

The control that makes the answer worth anything is the evidence. The FSD A2.7 writes every read of the case store to the access log, and A2.5 masks a personal field by role, so "who read this person's data, and was it masked" is answerable from two tables this service already owns. An access request answered without that evidence is a letter; with it, it is a statement the bank can defend. Answering it here also keeps the request inside the service that holds the masking rules and the access entries, so no personal value has to travel to answer a question about personal data.

Keeping the register off a table is the deliberate choice of the target. A request has states, steps and a clock, and a new table would give the service a second lifecycle to migrate and a second place where a step could be lost; the decision record is append-only, hash-chained and already published to the ledger, so the register is provable and the steps cannot be rewritten. The cost is that a request is a chain of entries and not one row, and the split pays it once, in the read of section 12.1.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8016-CON (same service, its own contract story) | The OpenAPI 3.1 document of the four operations, the `DataSubjectRequest`, `DataSubjectRequestList` and `DataSubjectRequestDecision` schemas, the state set, the error envelope, the consumed-operation list and the five contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of a step, hash-linked, written in the transaction that stores the answer |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the statutory period, the page bounds and the reference shape, as rows and not as code |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-47 Personal data and calls the four operations, one hop each |
| The access-log read of RWB-P4-E1039-CON | `GET /api/recovery/access/v1/admin/access-log` (API-P4-008) over the entries of this service's own chain, filtered by case id; the filter is fixed by the contract (GAP-0877; ASM-1592) |
| RWB-P4-E1037-APP's masking table | The `masking_rule` rows (DF-REF-198 to DF-REF-204) the erasure writes and the `masking_version` it moves on; this story writes no policy and adds no column |

Business preconditions carried from RWB-E8-016, from the feature specification and from the technical specification:

- The rights in force are those of TSD P4 v3 T6.1 and of the legacy permission table: a request is opened with Rules and parameters C (RW-COE holds `CRUD`), its decision and its answer are recorded with A (RW-RISK holds `RA`), and it is read with R. A caller without the letter is refused with 403 and MSG-P4-002 (BR3).
- The FSD P4 v3 A2.27.3.3 role table names the Compliance and PDPA officer as the primary user and the Security administrator as the second. The matrix of T6.1 gives RW-COMPLY `R` only in Rules and parameters and gives RW-SECADM `CRUDA` in Platform administration, not in Rules and parameters, so the primary role of the FSD cannot open or decide a request unless a permission row carries the letter; the difference is carried as an assumption and changes no metadata value (ASM-1592).
- The legacy permission table fixes the capability area as Rules and parameters, and the legacy validation rules VR-P4-027-1 and VR-P4-027-2 fix the sign-in message and the break-glass warning of a request.
- A case hold is the case's: R-UNI-11 moves a case to `HELD_LEGAL` and routes it to Compliance, and this story neither holds nor releases a case and writes no case state (BR13).
- The statutory period, its unit and its working-day rule are Not specified in the source documents (GAP-0875; ASM-1590): the due date is computed from the parameter row in force and the calculation this story applies is calendar days from `openedAt` (ASM-1590).
- Where a corrected value is applied and where an erased field is removed are Not specified (GAP-0876; ASM-1591): this story records the decision, names the field ids and writes the masking rows of an erasure, and the execution in the owning services is out of scope.

### 4. Flow

1. The compliance and PDPA officer opens SCR-47 Personal data through the gateway-bff composite route (DP-19). The route shows the register as this service answers it and calls the four operations.
2. The officer records a request. The route calls `POST /api/recovery/access/v1/admin/data-subject-requests` on `rwb-access` with `dataSubjectRef`, `requestType` (`ACCESS`, `CORRECTION` or `ERASURE`), `caseIds`, `fieldIds` (required for `CORRECTION` and `ERASURE`), `receivedAt` and `reason`, and an `Idempotency-Key` header.
3. `DataSubjectRequestController` validates the request: every required field is present, `requestType` is one of the three, `caseIds` holds at least one case id, `fieldIds` is present for a correction and for an erasure and empty for an access request, `receivedAt` is a date, and `dataSubjectRef` matches the reference shape in force read through DP-06. An empty field or a value of the wrong shape is refused with 422 and MSG-GEN-001 naming the field, and nothing is read and nothing is written (BR4).
4. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`. A key already answered replays that first answer, stores nothing and appends no entry (BR11, AC4).
5. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Rules and parameters C. A caller without the C letter is refused with 403 and MSG-P4-002, and nothing is recorded (BR3, AC3).
6. `ParameterReader` reads the statutory-period row through `GET /api/recovery/case/v1/admin/parameters` of `rwb-case` with the version in force and computes `dueDate` as the received date plus the period the row gives. No period, unit or working-day rule is a constant in code (BR8, AC7).
7. In one local transaction the service appends one entry to the decision-record chain of DP-03 with the record code of a data subject request, the request id, the type, the person reference, the case ids, the field ids, the received date, the due date, the opening role code, no case state and no personal value; sets the idempotency row to the answer; and stages the outbox row of the entry (BR1, BR7, BR11).
8. The answer is 201 with `requestId`, `requestType`, state `OPEN`, `openedAt`, `dueDate`, `version` and the `Location` of the register read (BR6).
9. The officer works the request. Where a correction is decided, the route calls `PATCH /api/recovery/access/v1/admin/data-subject-requests/{requestId}` with `decision` `CORRECTION`, the `fieldIds`, `reason` and the `If-Match` of the version the screen holds.
10. `DataSubjectRequestService` authorises Rules and parameters A (403 with MSG-P4-002 otherwise), compares the `If-Match` with the version of the latest entry (409 with MSG-GEN-004 otherwise, the register unchanged), and refuses a decision the state does not accept (409 with MSG-GEN-004) (BR3, BR5, BR6).
11. `CorrectionRecorder` appends the decision with the field ids and no value, moves the request to `IN_PROGRESS`, and returns 200 with the new `version`; the corrected value is not read and not written here (BR7, NFR-040).
12. Where an erasure is decided, `ErasureWriterService` writes one `masking_rule` row for every role in force with `unmasked` false from the `effectiveFrom` of the decision, moves `masking_version` on by one, and appends the same decision, all in one transaction; a failure writes no masking row and appends no entry (BR7, AC5).
13. The answer to the request is recorded with `decision` `ANSWER` (or `REFUSAL` with a reason); the state moves to `ANSWERED` (or `REFUSED`) and the answer carries `answeredAt`, the number of calendar days from `openedAt`, and whether the due date was met (BR6, BR9).
14. Where the request is of type `ACCESS`, the read of step 15 answers the evidence: `AccessEvidenceReader` calls `GET /api/recovery/access/v1/admin/access-log` on its own service with the case ids of the request, one hop with a 2 s timeout, and takes the decision code, the decided time, the field ids and the mask flag of each entry. No entry of another service is read and no ledger query is made (BR9, AC6).
15. `GET /api/recovery/access/v1/admin/data-subject-requests/{requestId}` answers the request with its `steps` in entry order and its `evidence` block, and `GET /api/recovery/access/v1/admin/data-subject-requests` answers the page of requests with their state, their dates and their version, ordered by `openedAt` then by request id so the paging is stable (BR10, BR12).
16. A request with no entry answers 404 on the read by id and an empty `items` with total 0 on the list; no message carries a personal value, and no answer names a person (BR12, BR14).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is empty, `requestType` is not one of the three, `caseIds` is empty, `fieldIds` is missing for a correction or an erasure, or `receivedAt` is not a date | 422 naming the field; nothing is read and nothing is written | MSG-GEN-001 | AC1 |
| X2 | `dataSubjectRef` does not match the reference shape in force | 422 naming `dataSubjectRef`; no entry | MSG-GEN-001 | AC1 |
| X3 | The caller holds no Rules and parameters C on the open, or no A on the decision | 403, no entry, no masking row | MSG-P4-002 | AC3 |
| X4 | The caller's session has ended | 401, no entry and no masking row | MSG-P4-001 | AC3 |
| X5 | The `If-Match` of a decision is older than the request's version | 409 and the register unchanged; the screen reloads the request | MSG-GEN-004 | AC4 |
| X6 | A decision arrives for a request in `ANSWERED` or `REFUSED` | 409 and the register unchanged | MSG-GEN-004 | AC4 |
| X7 | The `rwb-case` parameters read does not answer inside 2 s, or the statutory-period row is not in force | 503 and no request opened; a retry with the same `Idempotency-Key` opens exactly one | MSG-P7-003 | AC7 |
| X8 | The access-log read does not answer inside 2 s | 503 on the read by id, the request itself unchanged and readable again later | MSG-P7-003 | AC6 |
| X9 | The decision-record entry, the masking rows, the idempotency row or the outbox row cannot be written | 503 and no answer; nothing is recorded and the retry completes one step | MSG-P7-003 | AC2 |
| X10 | The same request arrives twice with the same `Idempotency-Key` | The first answer is replayed; one entry, one masking write | None | AC4 |
| X11 | A break-glass grant is active for the caller | The step proceeds and the answer carries the warning with the end time of the grant, and the entry carries the grant id | MSG-P4-004 | AC3 |
| X12 | The request's due date has passed and the request is still open | The answer carries the overdue flag and the list shows it; no state changes and no message is produced by a timer | None | AC7 |

No exception path of this story changes a case, a task, a role, a permission or a rule: the case and its hold belong to `rwb-case` and `rwb-deviation`, the masking policy to RWB-P4-E1037-APP, and the only rows this story writes of its own are its chain entries, the masking rows of an erasure and the platform library rows of the request.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8016-CON and its fakes; the period and the page bounds are parameter rows, the access entries are read through their owner's operation, and the masking policy is another story's table |
| Negotiable | The reference shape, the page bounds and the statutory period are parameter rows; the approving letters and the state set are reviewed with Compliance and with the access-log owner |
| Valuable | One register answers whether a data subject request was worked and answered inside the statutory period, and the erasure leaves the masking rows that make it true |
| Estimable | One controller, one register service, one erasure writer, one evidence reader, one record appender, one idempotency store, five fakes and ten test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule, no screen and no event of its own |
| Testable | Each owned criterion has a test case in section 16; the due date is provable with two versions of the parameter row, and the erasure is provable against a seeded matrix |

### 7. Acceptance criteria

```gherkin
Feature: Handle a data subject request

  Background:
    Given the environment is SIT
    Given the data subject request register is held by rwb-access as decisions of its own chain and rwb-access holds no case row and no personal value
    Given test user "U-8101" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS" and opens a request
    Given test user "U-8102" holds RW-RISK with "RA" in "RULES_AND_PARAMETERS" and records the decision of a request
    Given test user "U-8110" holds RW-CASEOWN with "R" only in "RULES_AND_PARAMETERS"
    Given test user "U-8103" holds RW-AUDIT with "R" in "RULES_AND_PARAMETERS"

  Scenario: AC1 Handle a data subject request (legacy RWB-E8-016 AC1)
    Given the rwb-case contract mock returns the statutory-period parameter row at its version in force
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then works a PDPA access, correction or erasure request inside the statutory period
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-016 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A role without Rules and parameters C or A is refused (new, D-RCV-60)
    Given "U-8110" holds RW-CASEOWN with "R" only in "RULES_AND_PARAMETERS"
    When "U-8110" calls POST /api/recovery/access/v1/admin/data-subject-requests for dataSubjectRef "DS-REF-2027-000118", requestType "ERASURE" and cases "RW-2026-000123" with Idempotency-Key "k-816-1"
    Then the response is 403 with message MSG-P4-002 and no request is answered
    Then no data subject request entry is appended
    Then GET /api/recovery/access/v1/admin/data-subject-requests answers an empty items with total 0
    When "U-8101", holding C but not A, tries to record the erasure decision on "DSR-2027-000118"
    Then the response is 403 with message MSG-P4-002 and no masking row is written

  Scenario: AC4 The request moves from open to in progress to answered (new, D-RCV-60)
    Given "U-8101" opens a request of type "ERASURE" for dataSubjectRef "DS-REF-2027-000118" and cases "RW-2026-000123" on receivedAt 2027-01-04 with Idempotency-Key "k-816-2"
    Then the response is 201 with requestId "DSR-2027-000118", state "OPEN", openedAt 2027-01-04, dueDate 2027-02-18 and version "1"
    When "U-8102" records decision "ERASURE" on "DSR-2027-000118" with If-Match "1"
    Then the response is 200 with state "IN_PROGRESS" and version "2"
    When "U-8102" records decision "ANSWER" on "DSR-2027-000118" with If-Match "1"
    Then the response is 409 with message MSG-GEN-004 and the request stays "IN_PROGRESS"
    When "U-8102" records decision "ANSWER" on "DSR-2027-000118" on 2027-02-10 with If-Match "2"
    Then the response is 200 with state "ANSWERED", answeredAt 2027-02-10, version "3" and the due date met
    Then a decision "ANSWER" arrives again for the same request and the response is 409 with message MSG-GEN-004
    When "U-8101" sends the open of "DSR-2027-000118" again with Idempotency-Key "k-816-2"
    Then the first answer is replayed with requestId "DSR-2027-000118" and state "OPEN", and exactly one opening entry exists

  Scenario: AC5 An erasure writes a masking row for every role from a valid_from (new, D-RCV-60)
    Given the masking rules in force are "MASK-2027.01" and cover field "DF-PTY-016" for the roles of the matrix in force
    Given the roles in force are the rows of the permission matrix "PM-2027.01"
    When "U-8102" records decision "ERASURE" on "DSR-2027-000118" for field "DF-PTY-016" from 2027-02-01
    Then one masking_rule row is written for every role of the matrix with unmasked false and valid_from 2027-02-01
    Then masking_version moves from "MASK-2027.01" to "MASK-2027.02"
    Then the masking row carries the decision reference of the request and no value of the field
    Then no case row, no document row and no personal value is written

  Scenario: AC6 The access evidence is answered from this service's access entries (new, D-RCV-60)
    Given "U-8101" opened a request of type "ACCESS" for dataSubjectRef "DS-REF-2027-000119" and cases "RW-2026-000123" as "DSR-2027-000119"
    Given the access entries of rwb_access hold two "AC-READ" entries and one "AC-EXPT" entry for "RW-2026-000123", each with its field ids and its mask flag
    When "U-8103" calls GET /api/recovery/access/v1/admin/data-subject-requests/DSR-2027-000119
    Then the answer carries an evidence block with one item per access entry of the cases of the request, each with its case id, its decision code, its decided time, its field ids and its mask flag
    Then the answer carries no actor name, no actor user reference and no personal value
    Then the access-log read is the only read made and no ledger query and no read of another service is made

  Scenario: AC7 The statutory due date is read from the parameter row and never from code (new, D-RCV-60)
    Given the parameters fake answers the statutory-period parameter row with a period of 45 days at version "2027.1"
    When "U-8101" opens a request with receivedAt 2027-01-04
    Then the dueDate is 2027-02-18
    When the parameters fake answers the same row with a period of 60 days at version "2027.2"
    And "U-8101" opens a second request with receivedAt 2027-01-04
    Then the dueDate is 2027-03-05
    Then no period and no working-day rule is a constant in the deployed code

  Scenario: AC8 No personal value is written to the record or the answer (new, D-RCV-60)
    Given "U-8102" recorded an erasure decision for field "DF-PTY-016" on "DSR-2027-000118"
    When "U-8103" calls GET /api/recovery/access/v1/admin/data-subject-requests and GET /api/recovery/access/v1/admin/data-subject-requests/DSR-2027-000118
    Then neither answer carries a name, an e-mail address, a national identity number, a phone number, an address or a date of birth
    Then the chain entry carries dataSubjectRef, the case ids, the field ids, the decision code, the role code and the times, and no personal value
    Then the published rwb.decision.DecisionRecorded.v1 payload carries no personal value

  Scenario: AC9 A request of another type, a request with no case id and a correction with a value are refused and no case row is written (new, D-RCV-60)
    When "U-8101" opens a request with a type that is not "ACCESS", "CORRECTION" or "ERASURE" for dataSubjectRef "DS-REF-2027-000118" and cases "RW-2026-000123"
    Then the response is 422 with message MSG-GEN-001 and no entry is appended
    When "U-8101" opens a request of type "ERASURE" for dataSubjectRef "DS-REF-2027-000118" with no case id
    Then the response is 422 with message MSG-GEN-001 and no entry is appended
    When "U-8102" records decision "CORRECTION" on "DSR-2027-000118" with a corrected value in the body
    Then the response is 422 from the contract and no value is read or written
    Then no row is written in the case table of rwb_case, no case state changes and the case hold of R-UNI-11 is unchanged

  Scenario: AC10 A call with no authenticated user is answered 401 and an unknown request id is answered 404 (new, D-RCV-60)
    When a call is made to GET /api/recovery/access/v1/admin/data-subject-requests/DSR-2027-000118 with no authenticated user
    Then the response is 401 and no request is read
    When "U-8103" reads a request id that is not in the register
    Then the response is 404 and no entry is written

  Scenario: AC11 A consumed access-log read that fails or does not answer leaves the request unchanged (new, D-RCV-60)
    Given the access-log read of rwb_access does not answer in time (limit Not specified in the source documents (NEWAC-RWB-P4-E8016-APP-AC11)) for "RW-2026-000123"
    When "U-8103" calls GET /api/recovery/access/v1/admin/data-subject-requests/DSR-2027-000119
    Then the response is 503 with message MSG-P7-003 and the request is unchanged
    Then no call is made to any other service's operation
```

AC1 and AC2 are the two criteria of RWB-E8-016, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the parameters mock, so the statutory period is provable while the `rwb-case` contract is still a fake. AC3 to AC8 are new under D-RCV-60 and test only what this story adds: the two rights, the state path with its `If-Match`, the masking rows of an erasure, the access evidence, the due date from the parameter row, and the absence of a personal value.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A data subject request is one register held as decisions of this service's own chain: one entry per step, a receipt entry on the open and an outcome entry on the answer, written with the record code of a data subject request, and no new table for the register | RWB-E8-016 AC1; DP-03; ADR-022; GAP-2298 |
| BR2 | A request is opened, decided and answered through one gate per step that authorises the right, validates the fields, compares the version and records the step | RWB-E8-016 AC1; FSD P4 v3 A2.27; REQ-S8-007 |
| BR3 | A data subject request is read as the capability area PLATFORM_ADMINISTRATION: the writes (open, decision and answer) need U, and the read needs R; a caller without the letter is refused with 403 and MSG-P4-002 and nothing is recorded; the Rules and parameters letters of RW-COE and RW-RISK do not apply to this capability | TSD P4 v3 T6.1; legacy RWB-E8-016 permission checks; FSD P4 v3 A2.27.3.3; GAP-2300; ASM-1592 |
| BR4 | A request carries a type of `ACCESS`, `CORRECTION` or `ERASURE`, at least one case id, the field ids for a correction and an erasure, and a reference that matches the shape in force; a missing or malformed field is refused with 422 and MSG-GEN-001 | FSD P4 v3 A2.27.3.2; TSD P4 v3 T3.1; BR-P4-027 |
| BR5 | A decision carries the `If-Match` of the version the screen holds; a stale version is refused with 409 and MSG-GEN-004, and the register is unchanged | Architecture v5 slide 42; FSD P4 v3 A2.27.4.3 |
| BR6 | The state set is `RECEIVED`, `ANSWERED` and `REFUSED`; `RECEIVED` on the receipt entry of the open, `ANSWERED` or `REFUSED` on the outcome entry, and `ANSWERED` and `REFUSED` terminal; `late` is a flag derived from the due date and the answer time and is not a state | FSD P4 v3 A2.27.4.1; RWB-E8-016 AC1; ASM-1589; GAP-2298 |
| BR7 | An erasure writes one `masking_rule` row for every role in force with `unmasked` false from its `valid_from`, moves `masking_version` on by one, and appends the decision in the same transaction; a failure writes no row and appends no entry; the field ids of the request are the only fields covered, with no default set; the removal of a field value is done by its owning service, and a masking row does not override a retention class of P5 or the case hold of R-UNI-11, both of which stay in force | TSD P4 v3 T3.1 DF-REF-198 to DF-REF-204; FSD P4 v3 A2.5; ASM-1591; GAP-0876 |
| BR8 | A correction records the field ids corrected and no value; the corrected value is neither read nor written here, and it is applied by the owning service (`rwb-source-data` or `rwb-case`) | FSD P4 v3 A2.27; NFR-040; GAP-0876 |
| BR9 | The statutory due date is read from the parameter row in force through DP-06 and computed from the received date, and the version label of that row is recorded as the rule version of the request; no period and no working-day rule is a constant in code | NFR-043; DP-06; BR-P4-027; ASM-1590; GAP-2298 |
| BR10 | The access evidence of an access request is answered from this service's own access entries for the case ids of the request, read through the access-log operation of its owner with a case-id filter that the contract fixes; this story never reads another service's table or the central ledger, and a workbench-wide answer is the central ledger query of P7, joined to this answer by case id with no personal value copied | FSD P4 v3 A2.7; NFR-042; GAP-0877 |
| BR11 | Every step appends exactly one entry in the transaction that stores the answer; an answer that cannot be recorded is withheld with 503 and MSG-P7-003 | R-UNI-39; RWB-E8-016 AC2; DP-03 |
| BR12 | One `Idempotency-Key` answers one request: a replay answers the first answer and appends no second entry and writes no second masking row | Architecture v5 slide 42; DP-09 |
| BR13 | A request neither holds nor releases a case: the hold of R-UNI-11 and the case state are `rwb-case`'s and `rwb-deviation`'s, and this story writes no case row and no case state; the link from a recorded request to the case hold is left to `rwb-case` and raised as a dependency for D1 | R-UNI-11; REQ-S8-007; DP-01; GAP-2298 |
| BR14 | No answer, entry, event or test carries a personal value: the register names the person by a reference only (Not specified in the source documents (GAP-2298)), the cases by the case ids, the field ids, the decision code, the role code and the times, and nothing else | NFR-040; NFR-043; Principle 5; GAP-2298 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR11 are the record appender of DP-03 and its read: the entry commits with the idempotency row and with the masking rows of an erasure, and the register is a read over that chain with no update and no delete method.
- BR2 and BR3 are one ordered gate per step in `DataSubjectRequestGate`: validate, authorise, compare the version, write. Each step that refuses returns before the next one is reached, so a refused decision can never have written a masking row.
- BR4 is the schema of the contract plus the reference-shape check at request time with the version in force; a changed shape is data and needs no build.
- BR5 is the platform optimistic-lock column `version` of TSD P4 v3 T3.0 held in the latest entry, compared with the `If-Match` and answered as 409 through the platform envelope.
- BR6 is the state the register derives from its entries: the state of a request is the state of its latest entry, so no row carries a state and no step can be lost.
- BR7 is `ErasureWriterService`: one insert per role of the matrix in force, the version moved on by one, and the decision appended in the same transaction; a partial write is impossible because the transaction is one.
- BR8 is a negative rule: the decision schema has no value field, and a call that carries one is refused with 422 by the contract.
- BR9 is the parameters reader at request time, with the version in force, and the calculation in one place.
- BR10 is `AccessEvidenceReader`: one call to the access-log operation of this service with the case ids, one hop, 2 s, and the workbench-wide ledger left to P7.
- BR12 is the `idempotency_key` row of the platform library in `rwb_access`, written with the answer.
- BR13 and BR14 are the absence of a case row and of a personal value: no case table is read or written, and the person appears as a reference only.

### 9. State transitions

The register holds no state of its own; the state of a request is the state of its latest entry.

| From | Event | Condition | To |
|---|---|---|---|
| No request | `POST /admin/data-subject-requests` | C held, fields valid, the period in force read | `OPEN`, answer 201 with `openedAt` and `dueDate` |
| No request | `POST /admin/data-subject-requests` | No C letter | Refused 403 with MSG-P4-002; no entry |
| No request | `POST /admin/data-subject-requests` | The period row cannot be read | Refused 503 with MSG-P7-003; no entry |
| No request | `POST /admin/data-subject-requests` | The entry cannot be written | Refused 503 with MSG-P7-003; nothing recorded |
| `OPEN` | A correction or an erasure decision | A held, `If-Match` current, field ids present | `IN_PROGRESS`; for an erasure the masking rows are written |
| `OPEN` | A decision | No A letter | Refused 403 with MSG-P4-002; no entry |
| `OPEN` | A decision | `If-Match` stale | Refused 409 with MSG-GEN-004; no entry |
| `OPEN` | The answer without a decision | A held | `ANSWERED` or `REFUSED`; the state moves once |
| `IN_PROGRESS` | The answer | A held, `If-Match` current | `ANSWERED` or `REFUSED` |
| `ANSWERED` | A further decision | Any | Refused 409 with MSG-GEN-004; no entry |
| `REFUSED` | A further decision | Any | Refused 409 with MSG-GEN-004; no entry |
| `OPEN` or `IN_PROGRESS` | The due date passes | No step | The answer carries the overdue flag; no state changes and no message is produced by a timer |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | A step of a request | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| `masking_rule` of RWB-P4-E1037-APP | An erasure decision | One row per role in force with `unmasked` false and a `valid_from`, and `masking_version` moved on by one, in the transaction of the entry |
| `rwb.decision-record.v1` | Every entry | `rwb.decision.DecisionRecorded.v1` from the outbox of the same transaction |

A request that is answered is not reopened: a new request is opened for a new instrument, so the register keeps one instrument per request id and the history of a person's requests is the list filtered by `dataSubjectRef`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Compliance and PDPA officer (RW-COMPLY) | Works a request as the FSD A2.27.3.3 role table states; the matrix gives this role `R` in Rules and parameters, so a request is opened and decided only through a permission row that carries C or A (ASM-1592) |
| Center of excellence analyst (RW-COE) | Opens a request with `CRUD` in Rules and parameters; the C letter is the open (TSD P4 v3 T6.1) |
| Risk and model risk officer (RW-RISK) | Records the correction, the erasure decision and the answer with `RA` in Rules and parameters; the A letter is the decision |
| Internal audit (RW-AUDIT) | Reads the register and its evidence with Rules and parameters R; records nothing |
| Security administrator (RW-SECADM) | Uses the feature as the FSD role table states; holds `CRUDA` in Platform administration, so a step needs a Rules and parameters row like any other role (ASM-1592) |
| A case role without the letter (RW-CASEOWN, RW-PHONECOL) | Refused with 403 and MSG-P4-002; nothing is read and nothing is recorded |
| The gateway-bff route | Calls the four operations on behalf of the signed-in user, one hop each, and passes the `Idempotency-Key` and the `If-Match` unchanged |
| `rwb-access` itself | Reads `role` and `permission` and writes `masking_rule` in its own schema, plus its own chain and the platform library rows of the request |
| `rwb-case` (P3) | Owns the parameters and the case; answers the period and answers no case row to this story |
| `rwb-access` access log (RWB-P4-E1039-APP) | Owns the access entries and the read over them; answers the evidence |
| `rwb-decision` (P7) | Owns the central ledger and the workbench-wide query; this story calls it not at all |

The refusal shapes are 403 with an RFC 9457 problem response and `messageId` MSG-P4-002 for an absent right, 401 with MSG-P4-001 for no session, 409 with MSG-GEN-004 for a stale version or a state that does not accept the decision, 422 with MSG-GEN-001 for a field, and 503 with MSG-P7-003 for a read or a record that cannot be completed. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E8016-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the role codes the erasure writes a masking row for, and the role code of the caller recorded on the entry |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the PLATFORM_ADMINISTRATION U and R letters the step needs |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Write on an erasure: one row per role in force, `unmasked` false, `field_id` from the request, `valid_from` from the decision; and the `masking_version` moved on by one. Read: the rows in force, to know which roles are covered and which version is current |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the request entry: `decision_code` DF-DEC-003 with the record code of a data subject request, `case_id` DF-DEC-002 with the first case of the request, `rule_id` DF-DEC-004 empty, `inputs_ref` DF-DEC-008 with the request id, the type, the person reference, the case ids, the field ids, the received date, the due date and the role code, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the register and for the state of a request |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of an open | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` | the record row of a step | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | `delegation_limit` | none | Not read: a data subject request is not an approval limit |
| DF-REF-205 to DF-REF-211 | `role_conflict` | none | Not read: a request is not a role holding |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb_case` | the capability areas and the roles | Returned through the contract where needed; not read (DP-07; ASM-0071) |
| DF-PTY-007, DF-PTY-016 and the field ids of a request | the case store of `rwb_case` | none | **Not read**: the field id is a name in a decision and no value of the field is read, copied or written (NFR-040) |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` of `rwb_decision` | none | Not read and not written: the central ledger is P7's and this story reads only its own chain (DP-01) |
| (parameters) | `parameter_catalog` and `parameter_value` of `rwb_case` | the statutory period and the page bounds | Returned through the parameters contract; not read (DP-06) |
| (access entries) | the local decision-record table of RWB-P4-E1039-APP in `rwb_access` | the `AC-READ`, `AC-EXPT` and `AC-DENY` entries with their case id, decision code, time, field ids and mask flag | Read through the access-log operation of its owner, never by a query of this story |

No row of `case`, `task`, `document`, `decision_log_entry` or `parameter_catalog` is read or written: they are P3's and P7's under the ownership map and their fields arrive in a contract, not by a schema read (DP-01). The register itself is a set of entries of the local chain, so this story creates no table and names none of its own. Field IDs are those of the Logical Data Model and Data Dictionary v9 and of TSD P4 v3 T3.1.

The name and the unit of the statutory period, the record code of a data subject request, the shape of the person reference, the exact field set of a step are Not specified in the source documents (GAP-0874; ASM-1589) and (GAP-0875; ASM-1590); the schema of RWB-P4-E8016-CON fixes them, and the access-log read is filtered by case id as that contract fixes it (GAP-0877) and this story reads and writes them as that contract publishes them.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/data-subject-requests` | P4 `rwb-access` | Body: `dataSubjectRef`, `requestType` (`ACCESS`, `CORRECTION`, `ERASURE`), `caseIds`, `fieldIds`, `receivedAt`, `reason` | `requestId`, `requestType`, `state` `OPEN`, `openedAt`, `dueDate`, `version`, with `Location` of the read by id | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 (MSG-GEN-004); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters C | `Idempotency-Key` required; a replay answers the first answer |
| PATCH | `/api/recovery/access/v1/admin/data-subject-requests/{requestId}` | P4 `rwb-access` | Path: `requestId`. Header: `If-Match`. Body: `decision` (`CORRECTION`, `ERASURE`, `ANSWER`, `REFUSAL`), `fieldIds`, `effectiveFrom`, `refusalReason`, `answerSummary`, `reason` | `requestId`, `state`, `decision`, `version`, `updatedAt`, and for an erasure `maskingVersion` and `maskingRowCount` | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-GEN-004); 409 (MSG-GEN-004); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters A | `If-Match` required; the idempotency of the step is the version it moves |
| GET | `/api/recovery/access/v1/admin/data-subject-requests/{requestId}` | P4 `rwb-access` | Path: `requestId` | `DataSubjectRequest`: the request with its `steps` in entry order and, for an access request, its `evidence` block | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-GEN-004); 503 (MSG-P7-003) | Rules and parameters R, scope applied | Not applicable, read only |
| GET | `/api/recovery/access/v1/admin/data-subject-requests` | P4 `rwb-access` | Query: `state`, `requestType`, `dataSubjectRef`, `dueBefore`, `page`, `size` | `DataSubjectRequestList`: `items` of `requestId`, `requestType`, `state`, `openedAt`, `dueDate`, `overdue`, `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters R, scope applied | Not applicable, read only |

All four operations sit on the base `/api/recovery/access/v1` of DP-13. The register answers only what this service recorded, so its `state` is derived from its own entries and never from a case state. `page` defaults to the value of its parameter row and `size` is capped by it, both read through DP-06 and never from code (BR9). A request that has no entry answers 404 on the read by id and an empty `items` with total 0 on the list; the list is ordered by `openedAt` then by request id so a page cannot repeat or skip a request.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Rules and parameters C check behind the open, the A check behind a decision and the R check behind the reads, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/access/v1/admin/access-log` | P4 `rwb-access` (own service, RWB-P4-E1039-CON) | The access entries of the case ids of the request, with their decision code, time, field ids and mask flag, filtered by case id (BR10; GAP-0877; ASM-1592) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The statutory period, the person-reference shape and the page bounds, with the version in force (DP-06) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the parameters read and the authorise answer are cached for the session or the request. The access-log read is API-P4-008 of the P4 appendix T-A and is declared as consumed and never as provided by this story; its export and its search across other services are RWB-P4-AD007-APP's. No operation of `rwb-case`, `rwb-decision`, `rwb-document` or `rwb-deviation` beyond the parameters read is called.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a step of a request: the request id, the type, the person reference, the case ids, the field ids, the decision code, the role code, the received date, the due date and the time |

CloudEvents 1.0 envelope, from the outbox of the transaction that stores the answer. The payload carries references, codes and times and no name, no e-mail address and no personal value, and no case state. This story publishes no `rwb.access.<Event>.v1` message: the two events of `rwb-access` are `AccessPolicyChanged` (RWB-P4-E1037-APP) and `DoaLimitChanged` (RWB-P4-E8008-APP), and a data subject request adds neither (Architecture v5 slide 14).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 with no inbound event for this capability, and the register answers from its own chain, the parameters contract and the access-log read. No `processed_event` row is written.

#### 12.5 Workflows and activities

None. Opening, deciding and answering are synchronous, and the due date is a value and not a timer: this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. A request that passes its due date is shown as overdue by the read and is not escalated by a workflow here.

#### 12.6 Schedules

None. The register is request-driven; the six-monthly access review list (JOB-18) is the only Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role codes an erasure covers and the role code of the caller |
| `permission` | P4 (`rwb_access`) | Read only: the PLATFORM_ADMINISTRATION U and R letters |
| `masking_rule` | P4 (`rwb_access`), created by RWB-P4-E1037-APP | Write on an erasure: one row per role in force with `unmasked` false, and the `masking_version` moved on. Read: the rows in force |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: one entry per step. Read: the register, the state of a request and the evidence of an access request |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of a step and the idempotency row of an open; no inbox row, because no event is consumed (DP-09; ASM-0074) |
| `delegation_limit`, `role_conflict` | P4 (`rwb_access`) | Not read and not written: a request is neither an approval limit nor a role conflict |
| `case`, `task`, `parameter_catalog`, `lov_value` | P3 (`rwb_case`) | Not read and not written: the period and the lists arrive in the contract and no case row is read (DP-01; DP-06; DP-07) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's and the local record goes on `rwb.decision-record.v1` |
| the case store of P1 | P1 (`rwb_source_data`) | Not read and not written: no personal value is read to answer a request |

The masking policy is a table of this service and this story writes rows of it, but it defines no column, no list of fields and no policy: the field set an erasure covers is the request's, the roles are the matrix's, and the version is moved on rather than recomputed. `lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON`, so a capability area and a role are taken from the `role` and `permission` rows and from the contract, not from a list of this service (ASM-0071). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| parameters fake | RWB-P3-E1042-CON (rwb-case) | The statutory-period row at version "2027.1" with a period of 45 days, the same row at "2027.2" with 60 days, the person-reference shape, the page bounds, a version not in force for X7 and a 503 |
| authorise fake | RWB-P4-E8016-CON, RWB-P4-E1037-CON | A granted answer for RW-COE with C, for RW-RISK with A and for RW-AUDIT with R in Rules and parameters; a refused answer with MSG-P4-002 for RW-CASEOWN with R only and for RW-COE without A |
| access-log fake | RWB-P4-E1039-CON | Two `AC-READ` entries and one `AC-EXPT` entry for case "RW-2026-000123", each with its field ids and mask flag, an empty page for a case with no entry and a 503 for X8 |
| decision-record fake | RWB-PLT-E1027-CON | The append of a step, the hash-link check, the seeded chain of "DSR-2027-000118" with its opening, its erasure decision and its answer, and the forced failure AC2 needs |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-47 Personal data with the register list, the request form, the decision form and the evidence panel |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 4 (the open, the decision, the read and the list); consumed 3 | Base `/api/recovery/access/v1`; the own authorise operation, the own access-log read and the `rwb-case` parameters read, one hop and 2 s each |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | None | No file input and no file output: a request is entered on the route and the evidence is an answer, not a document |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/datasubjectrequest`, Java package `th.co.scb.ace.workbench.recovery.access.datasubjectrequest`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module request row and the in-module masking write of the monolith (DP-01 and DP-13: the case held by P3 and addressed on this service's own base), the in-process decision log (DP-03: a local library and the shared topic) and the ace-web screen that worked the request in process (DP-19: a gateway-bff composite route). DP-01, DP-02, DP-09 and DP-11 govern the service baseline and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it. A list-of-values check of the capabilities and scopes would need DP-07 and `RWB-P3-E1043-CON`, neither of which this story's metadata carries, so the roles and the capability areas come from the `role` and `permission` rows and the point is raised as an assumption in force (ASM-0071). The access-log read is consumed through its owner's contract and its fake, and the missing own contract dependency is carried in the gap row of the key (GAP-0877; ASM-1592).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DataSubjectRequestController | Controller | The four operations: validation, the `Idempotency-Key` lookup, the `If-Match` read, the RFC 9457 problem responses, `Location` on a created request |
| DataSubjectRequestGate | Service | The ordered gate of BR2 and BR3: validate, authorise, compare the version, write; a refusal returns before the next step |
| DataSubjectRequestService | Service | The state path of BR6 and the answer of BR6 and BR9: the state from the latest entry, the due date met or passed, and the step payload |
| DataSubjectRequestRegister | Repository | Read-only queries over the local decision-record table of DP-03 in `rwb_access` filtered by request id and by person reference; no update and no delete method |
| ErasureWriterService | Service | The masking rows of BR7: one row per role in force, `unmasked` false, the `valid_from` of the decision, and the `masking_version` moved on by one, in the transaction of the entry |
| CorrectionRecorder | Service | The correction of BR8: the field ids and no value, appended with the decision |
| AccessEvidenceReader | Service | The evidence of BR10: the access entries of the case ids through the owner's read, the mask flag and the field ids, and no actor name |
| ParameterReader | Service | The statutory period, the reference shape and the page bounds through the parameters contract of DP-06, with the version in force |
| PermissionReader | Service | The `role` and `permission` rows of the caller and the C, A and R letters |
| DecisionRecordAppender | Service | The step entry with its outbox row, in the transaction that stores the answer (DP-03, DP-09) |
| IdempotencyStore | Service | The `Idempotency-Key` lookup and store of the platform library, written with the answer |

**Database and migrations**

- This story creates no table of its own. `role` and `permission` and `masking_rule` are created by RWB-P4-E1037-APP, the local decision-record table by RWB-P4-E1039-APP and the platform library tables by the service's own DB story, in the per-service Flyway sequence of DP-15; this story reads and uses them.
- The register is a chain of entries and not a table: a request table would be a second lifecycle beside the chain, and a step that failed between the two would be a request the bank cannot show. No such table is created (BR1).
- No write statement touches `role` or `permission`: the reader is read-only, so a request can never grant itself a right.
- The masking rows of an erasure, the step entry, the idempotency row and the outbox row commit in one transaction; a failure rolls all of them back and the answer is withheld with MSG-P7-003 (BR7, BR11).
- No personal value is stored in a column, an index or a key: `dataSubjectRef` is a reference, and the field ids are names of fields and not their values (BR14).

**Configuration and reference data**

- The statutory period, the person-reference shape and the page default and maximum are parameter rows of `rwb-case` read through DP-06 with the version in force; no period and no bound is a constant in code (BR9). Their names are fixed by RWB-P4-E8016-CON.
- The roles an erasure covers are the rows of `role` in force and the `masking_version` of `masking_rule`; no role code and no field id is a constant in code (BR7).
- The capability area and the letters of a step are read from `permission`; no area and no letter is a constant in code (BR3).

**Build steps**

1. `DataSubjectRequestController` and its validation; tests for X1 and X2 with nothing written.
2. `PermissionReader` and the authorise call of step 5; test the AC3 refusal of a caller with R only, with no entry and an empty register afterwards, and the refusal of a C holder who tries to decide.
3. `ParameterReader` over the parameters fake; tests for AC7 with the row at "2027.1" and at "2027.2", so a changed period is data and needs no build.
4. `DecisionRecordAppender` and `IdempotencyStore` in one transaction; test the open of AC4, the replay with one entry, and the forced failure of AC2 with nothing recorded.
5. `DataSubjectRequestService` with the state path of BR6 and the `If-Match` of BR5; tests for the stale version, the terminal state and the answer inside and outside the due date.
6. `CorrectionRecorder` and the negative rule of BR8: a decision that carries a value is refused with 422 and the field ids are recorded without it.
7. `ErasureWriterService` over a seeded matrix; test AC5 with one row per role, `unmasked` false, `valid_from` and the version moved on, and the forced failure with no row and no entry.
8. `AccessEvidenceReader` over the access-log fake; tests for AC6 with the two `AC-READ` and one `AC-EXPT` entry, an empty evidence block and the 503 of X8.
9. The contract-fake run of the four operations through the gateway-bff fake, so SCR-47 can be demonstrated while the route is being built.

**Feature switch.** The four operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of their own. A register that is switched off would leave a statutory request neither recorded nor answerable, which is the state the register exists to resolve, so this story adds no flag and removes nothing.

**Done when.** The tests in section 16 pass; a request of type `ERASURE` is opened on 2027-01-04 with a due date from the parameter row and answered on 2027-02-10 inside it; a caller with R only is refused with MSG-P4-002 and nothing is recorded; a stale `If-Match` and a decision on an answered request are refused with MSG-GEN-004; an erasure writes one masking row per role and moves `masking_version` on by one; the access evidence of an access request is answered from this service's access entries with no actor name; the same `Idempotency-Key` replays one answer with one entry; a forced record failure withholds the answer with MSG-P7-003; and no answer, entry or event carries a personal value.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on all four operations |
| MSG-P4-002 | The caller holds no Rules and parameters C on the open, no A on a decision, or no R on a read | You cannot {action} here. Your role does not include it. | This story, on all four operations |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the open and on a decision, with the grant id recorded in the entry |
| MSG-GEN-001 | A required field is empty, `requestType` is not one of the three, `caseIds` is empty, `fieldIds` is missing for a correction or an erasure, `receivedAt` is not a date, or `dataSubjectRef` is not of the shape in force | Enter {field}. | This story, on the open and on a decision |
| MSG-GEN-004 | The `If-Match` is stale, the state does not accept the decision, or the request has no entry on the read by id | Someone else changed this record. Reload it to see their change. | This story, on the decision and on the read by id |
| MSG-P7-003 | The parameters read or the access-log read cannot be completed, or the entry, the masking row, the idempotency row or the outbox row cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on all four operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are copied unchanged from the legacy story where the message already existed: MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001 and MSG-P7-003 are the legacy texts of RWB-E8-016. MSG-GEN-004 is the platform conflict text and is used here for the stale version and the terminal state, a condition the legacy story did not carry; it is not a new business text.

The legacy story carries no message of its own beyond the five, and this story invents none: the due date, the overdue flag and the evidence are answer fields and not messages, so a request that is late is answered with its dates and not with a warning.

### 15. Screens and states

SCR-47 Personal data is the screen, served through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON), which holds the retention classes, the masking rules, the consent log and the data subject requests of FSD P4 v3 (screen list) and calls the four operations of this story, one hop each. This story renders no screen surface of its own.

| Screen | State | What it shows |
|---|---|---|
| SCR-47 Personal data | Loading, list | The register of requests with their type, state, received date, due date and overdue flag, paged |
| SCR-47 Personal data | Register, empty | An empty register with total 0 and no error |
| SCR-47 Personal data | Request, form | A new request with `dataSubjectRef`, `requestType`, `caseIds`, `fieldIds`, `receivedAt` and `reason`; the reference is validated against the shape in force |
| SCR-47 Personal data | Request, opened | The 201 answer with `requestId`, `requestType`, state `OPEN`, `openedAt` and `dueDate` |
| SCR-47 Personal data | Decision, form | One open request with its decision type, its field ids, its effective date and its reason, and the version the screen holds |
| SCR-47 Personal data | Decision, recorded | The 200 answer with the new state and version, and for an erasure the masking version and the number of rows |
| SCR-47 Personal data | Decision, stale | The 409 of X5 with MSG-GEN-004 and a reload action |
| SCR-47 Personal data | Request, answered | The request with its steps in order, its answer and whether the due date was met |
| SCR-47 Personal data | Evidence | For an access request, one row per access entry with its case id, decision code, time, field ids and mask flag, and no actor name |
| SCR-47 Personal data | Evidence, empty | An empty evidence block with a note that no access entry exists for the case ids, and no error |
| SCR-47 Personal data | Refused | The 403 of X3 with MSG-P4-002 for a role without the letter |
| SCR-47 Personal data | Not recorded | The 503 of X9 with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |
| SCR-47 Personal data | Error | Not specified in the source documents (CG-ALL-5627) |
| SCR-47 Personal data | No access | Not specified in the source documents (CG-ALL-5627) |

The legacy story named SCR-47 Personal data and SCR-39 Rules and parameters in its screen table; a data subject request sits on SCR-47 and not on SCR-39, and the rules and parameters surfaces are RWB-P4-E8007-APP's and RWB-P4-AD012-APP's. The composite route specification, the retention classes, the masking policy panel and the consent log belong to RWB-PLT-N001-CON, to RWB-P4-E1037-APP and to the retention work of P5; this story serves the request register and the evidence of that screen only. For SCR-39 Rules and parameters the empty, loading, error and no access states are Not specified in the source documents (CG-ALL-5626), and this story adds no SCR-39 state.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-016-01 | AC1, BR1, BR2, BR6 | Component | A request of type "ERASURE" opened on 2027-01-04 by RW-COE and answered on 2027-02-10 by RW-RISK: 201 `RECEIVED`, then 200 `ANSWERED`, two entries in order (receipt and outcome) and one `rwb.decision.DecisionRecorded.v1` per entry |
| TC-E8-016-02 | AC2, BR11 | Component | The record store forced to fail during the open and during the erasure decision: 503 with MSG-P7-003, no request answered, no entry and no masking row; a retry with the same `Idempotency-Key` completes exactly one entry |
| TC-E8-016-03 | AC3, BR3 | Component | A caller holding RW-CASEOWN with Rules and parameters R only: 403 with MSG-P4-002, no entry and an empty register; a caller holding C without A: 403 on the decision and no masking row |
| TC-E8-016-04 | AC2, BR7, BR11 | NFR | The masking write and the append forced to fail under load: every failure is a 503 with MSG-P7-003, no partial masking row and no partial entry is ever readable, and the retry path yields one row set and one entry |
| TC-E8-016-05 | AC4, BR5, BR6, BR12 | Component | The version path of "DSR-2027-000118" with `If-Match` "1", "1" again and "2": 409 with MSG-GEN-004 on the stale and the terminal step, 200 with version "2" and "3" on the others, and one opening entry for a replayed `Idempotency-Key` "k-816-2" |
| TC-E8-016-06 | AC5, BR7 | Component | The matrix "PM-2027.01" and the masking rules "MASK-2027.01": one row per role with `unmasked` false from 2027-02-01, `masking_version` "MASK-2027.02", the decision reference on every row and no value of "DF-PTY-016" |
| TC-E8-016-07 | AC6, BR10 | Component | The access-log fake with two "AC-READ" and one "AC-EXPT" entry for "RW-2026-000123": one evidence item per entry with its case id, code, time, field ids and mask flag, no actor name, and an empty evidence block for a case with no entry |
| TC-E8-016-08 | AC6, BR10 | Component | The access-log read answering 503 and the workbench-wide query absent: 503 with MSG-P7-003 on the read by id, the request unchanged and readable again, and no call to any other service's operation |
| TC-E8-016-09 | AC7, BR9 | NFR | The statutory-period row at "2027.1" with 45 days and at "2027.2" with 60 days, both opened on 2027-01-04: due dates 2027-02-18 and 2027-03-05, no period in the deployed code, and no build for the change |
| TC-E8-016-10 | AC8, BR14 | NFR | A scan of both read answers, the chain entries, the event payload and the fixtures for a name, an e-mail address, a national identity number, a phone number, an address and a date of birth: no match, and the person appears as "DS-REF-2027-000118" only |
| TC-E8-016-11 | BR2, BR4 | Contract | Each operation, event and activity of section 12 checked against the schema of RWB-P4-E8016-CON: a request and a response matching the published shape, every error code of the operation and every event name as published; an off-schema call is refused with 422 and MSG-GEN-001 |
| TC-E8-016-12 | BR7, BR10 | Component | Boundary test of each table of section 12.7 that the story reads or writes: the role set with one role and with every role in force, the permission row with the U and R letters and with no row (403), the masking_rule set before and after one erasure, and the access entries with none and with the page bound read from the parameter row in force |
| TC-E8-016-13 | BR4 | Component | A request whose type is not "ACCESS", "CORRECTION" or "ERASURE", and a request with no case id: 422 with MSG-GEN-001 both times, no entry and no masking row |
| TC-E8-016-14 | BR8 | Component | A correction whose decision body carries a corrected value: 422 from the contract, no value read or written, and the entry holds the field ids and no value |
| TC-E8-016-15 | BR13 | Component | An open and an answer on "RW-2026-000123": no row written in the case table of rwb_case, no case state changed, and the case hold of R-UNI-11 unchanged |
| TC-E8-016-16 | AC9, BR4, BR8, BR13 | Component | Not specified in the source documents (NEWAC-RWB-P4-E8016-APP-AC9) |
| TC-E8-016-17 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-P4-E8016-APP-AC10) |
| TC-E8-016-18 | AC11 | Component | Not specified in the source documents (NEWAC-RWB-P4-E8016-APP-AC11) |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows are kept: TC-E8-016-01 for AC1, TC-E8-016-02 for AC2, TC-E8-016-03 for the access refusal and TC-E8-016-04 for the forced record failure; six rows are added for the new criteria of this story. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under R7.2 s16. No ITG story is split from this legacy key, so no `-ITG` copy of these test cases is written here and no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the statutory period, the reference shape and the page bounds are parameter rows (BR9), the roles and the letters are read from `role` and `permission` (BR3, BR7), and a test proves that a changed period needs no build.
- No personal data anywhere: the register, the answer, the event and the test carry a person reference, case ids, field ids, decision codes, role codes and times; no name, no e-mail address, no national identity number, no phone number, no address and no date of birth appears in an answer, an entry or a fixture (BR14, NFR-040).
- No read of another service's tables (DP-01): `case`, `task`, `parameter_catalog` and the case store are P3's and P1's, `decision_log_entry` is P7's, and no join crosses a schema. The period arrives in the contract and the evidence arrives through the access-log operation.
- No personal value is read to answer a request: the field id of a correction and of an erasure is a name, and the value is neither read nor written here, so a request cannot become a copy of the data it is about (BR8).
- No request without its record: the entry commits with the answer and with the masking rows of an erasure, and the answer is withheld with MSG-P7-003 when they cannot be written (BR7, BR11, R-UNI-39).
- One writer for a masking policy: this service holds `masking_rule`, and this story writes rows with `unmasked` false and a `valid_from` and nothing else; it changes no policy, no field list and no other column, so the policy and the erasure cannot drift.
- The due date is data: no period, no unit and no working-day rule is a constant, so a change of the statutory period is a row and not a release (BR9).
- One key, one request, one step: the `Idempotency-Key` is stored with the answer and the `If-Match` guards the version, so a retry after a timeout cannot open a second request or write a second set of masking rows (BR12).
- The case is not touched: no case state, no task and no hold is written or released here, so the hold of R-UNI-11 stays with the service that owns the case (BR13).
- Every example, fixture and test payload is synthetic; no production personal value is copied into a schema, a fake or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S8-007 | A data subject request holds automated processing on the case and routes to Compliance inside the statutory period | Epic 8; Program, Compliance | FEAT-ADM-11 | All recovery processes | BR1, BR2, BR6, BR13 | TC-E8-016-01, TC-E8-016-05 |
| NFR-043 | A data subject access, correction or erasure request is answered inside the statutory period | Program, non-functional | FEAT-ADM-11 | All recovery processes | BR6, BR7, BR9, BR10, BR14 | TC-E8-016-01, TC-E8-016-06, TC-E8-016-07, TC-E8-016-09, TC-E8-016-10 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules R7.3; NFR-043 carries the status "Open, DL26" in TSD P4 v3 T7 and its target is "Statutory period, Not set as a working service level", which is why the period is a parameter row and its value is a gap. The Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 handle a data subject request inside the statutory period, with the result written to the decision log | Sections 1, 4, 7, 8, 12.1, 12.3 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 4, 5, 7, 8, 12.1, 14 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 3, 7 (AC3), 8 (BR3), 10, 12.1 |
| MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| The legacy validation rules VR-P4-027-1 and VR-P4-027-2 and BR-P4-027 | Sections 3, 8, 14 |
| The legacy data rows `decision_log_entry` DF-DEC-001 to DF-DEC-018, `rule_row` DF-REF-001 to DF-REF-015 and `role` DF-REF-034 to DF-REF-038 | Sections 11, 12.7: the decision row and the role row are kept, the `rule_row` is not this capability's (GAP-0878) |
| The legacy endpoints `/admin/rule-versions` and `/admin/rule-versions/{versionId}/approve` on the monolith base | Section 19 and GAP-0878: a rule-version load and approval are RWB-P4-E8007-APP's and RWB-P4-AD011-APP's, not this story's |
| The legacy screens SCR-47 Personal data and SCR-39 Rules and parameters as the story named them | Section 15, carried to SCR-47 Personal data |
| TC-E8-016-01 to TC-E8-016-04 | Section 16 |
| Legacy key RWB-E8-016, story RWB-P4-E8016-APP, contract RWB-P4-E8016-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The masking policy: which field a role may see, the field list, the masking versions and the panel of SCR-47 that administers them (RWB-P4-E1037-APP and RWB-P4-AD004-APP). This story writes the rows an erasure needs against that policy and changes no policy value.
- The access log: the writer of the access entries in every service, the break-glass grant and the search and export of the log (RWB-P4-E1039-APP, RWB-P4-AD007-APP and the DB and OPS stories of that key). This story consumes its read.
- The hold on the case and its routing to Compliance (R-UNI-11, REQ-S8-007): the case state, `HELD_LEGAL` and the task of the case are `rwb-case`'s and `rwb-deviation`'s, and no case row is written here.
- The retention classes and the retention of a request, of an access entry and of a masked field: the retention work of P5 `rwb-document` and of the P3 and S8 reference work.
- The generation and dispatch of the answer letter to a data subject (FEAT-OCC-01 and the P6 stories). This story records the answer and does not produce a letter.
- The central decision ledger, the workbench-wide access query `GET /decision-log` and the chain verification (`rwb-decision`, P7), and the integration story that proves the journey across the services.
- The screen SCR-47 Personal data itself, its retention, masking and consent panels and its composite route specification (RWB-PLT-N001-CON and RWB-P4-E1037-APP).
- The P1 dictionary, the data product catalog and the source-field lineage of a personal field (P1 `rwb-source-data`); this story reads no personal value and no dictionary row.
- The correction and the erasure in the owning services: where a corrected value is applied and where an erased field is removed are Not specified in the source documents (GAP-0876; ASM-1591) and are not this story's.
- The integration harness and the `-ITG` copies of the test cases: no ITG story is split from this legacy key.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
