# RWB-P4-AD010-APP Approve a reference data load

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-010 |
| Legacy disposition | Split (rework) |
| Size | Not specified in the source documents (DOR-RWB-P4-AD010-APP-16) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | L-P4-F |
| Ready to start | After RWB-P4-AD009-APP |
| Depends on (build) | RWB-P4-AD010-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P4-AD009-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Contract version | 5.0.0 (rwb-access API specification v5, rwb-access.yaml info.version) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-010 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-AD010-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 10 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **list owner holding the A letter in Reference data (RW-REFADM, RW-COE per TSD P4 v3 T6.1)**, I want **the approval gate in front of a loaded list of values — the A letter in Reference data, the four-eyes rule, the effective date and the record of the decision**, so that **no reference data changes without its owner, nobody approves a load they wrote themselves, a version takes effect from its valid-from date and never before it, and the audit trail shows which version was approved, by which approver and when**.

Inside `rwb-access` this is the approval capability of the legacy story RWB-AD-010:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- **The split, stated plainly.** Loading a list version, the file, the verification of the loaded rows and the version store are RWB-P4-AD009-APP's and `rwb-case`'s: `lov_value`, `reference_version` and `reference_row` are P3 `rwb-case` under ASM-0071, and the reference-load approve path `POST /admin/reference-loads/{loadId}/approve` is P3's under ASM-0041. This story is the **approval gate** only: the authority, the four-eyes rule, the effective date and the record. It writes no list row and no version row: it asks the owner to move the version and reads the version back.
- **Two operations provided**, and no others: `POST /api/recovery/access/v1/admin/lov-loads/{loadId}/approve`, which decides the gate and then calls the owner's approve; and `POST /api/recovery/access/v1/admin/lov-loads/{loadId}/return`, which sends the load back to its author with a coded reason.
- **Three operations consumed**: the owner's `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve`, which moves the version; the owner's `GET /api/recovery/case/v1/admin/lists/{listCode}`, which reads the version, its author, its state and its valid-from date back; and this service's own `POST /api/recovery/access/v1/authorise`, which answers the A letter in Reference data.
- **Four eyes**: the load's `author` reference is compared with the approver reference of the caller. A service-identity author may be approved by a person; a service identity may not approve; the same person may not author and approve. Both the author reference and the approver reference are recorded in the decision-record entry. The authority is the A letter in Reference data, resolved from the `role` and `permission` rows of `rwb_access`, never a hard-coded role.
- **Data**: no new list table and no write to `lov_value`. Each approve, refusal or return is one decision-record entry of the DP-03 library with decision code `REF-APPR`, `REF-DENY` or `REF-RTRN`, carrying the load, the list, the version, the effective date, the author reference and the approver reference, and no personal data.
- The screens of the legacy story SCR-39 Rules and parameters belong to the rule-version key RWB-AD-011. This story serves SCR-40 Reference data only, through the gateway-bff composite route of DP-19.
- SCR-40 states: no access shows MSG-P4-002 for an absent letter and MSG-P4-001 for an absent role; error shows 503 with MSG-P7-003 when the record cannot be written; empty and loading: Not specified in the source documents (DOR-RWB-P4-AD010-APP-10).

### 2. Business rationale

Reference data is the table a business person changes without a code release, which is exactly why it needs an owner in front of it. The legacy control was one approval endpoint and one permission row, and both were weak: the permission table said Reference data A was held by service identities only, while the legacy criterion had a person approving, and nothing said what happened when the person who loaded a version was the person asked to approve it. In the target the load and the approval are two stories on purpose: the load is a data act (RWB-P4-AD009-APP, with the store in `rwb-case`), and the approval is a governance act — who may approve, with what separation of duty, effective from when, and recorded where.

This story meets REQ-DRI-011 (a versioned table carries its valid-from and valid-to dates, its author and its approver), REQ-ACA-003 (the role-to-permission matrix is the only source of what a role may do) and REQ-ACA-013 (full administration screens for roles, permissions and delegation). It applies R-UNI-38 (a new version applies from its effective date, and open work keeps the version it was decided under) and R-UNI-39 (an action that cannot be recorded does not proceed). It follows the same approve-and-date discipline the Drools packages follow: a version is approved by a second person and takes effect on a date, not on the day it was approved. A version takes effect from its valid-from date only and never retroactively. An approval given before that date is allowed: the version reads APPROVED until the date and IN_FORCE from it, and the version it supersedes keeps valid-to set to the day before.

The approval also protects the other eighteen services. `rwb-case` holds the reference store, but a wrong list value reaches every consumer of DP-07 in one release; the gate is the one place where a person with the area right and a date can stop it.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD009-APP (same service, its own story) | A loaded version in state LOADED, with its load reference, its list code, its version label, its `author` reference and its `valid_from`; the idempotency and outbox rows of `rwb_access`; the SCR-40 load list. This story approves or returns that version and creates no load |
| RWB-P4-AD010-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the two console operations, the `LovLoadApproval` schema, the return request with its coded reason list, the error envelope and the fakes this story builds against |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the `REF-APPR`, `REF-DENY` and `REF-RTRN` entries |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the four-eyes switch and the approval-limit rows, read with the version in force |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): the list, the version, its author, its state and its effective date, and the coded return reasons |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-40 Reference data to the browser |
| RWB-P4-E1037-CON (same service, its own contract story) | The authorise operation and the permission answer behind the A letter, with the RFC 9457 refusal shape and MSG-P4-002. This story calls that operation and adds no path to it |
| RWB-P4-E1038-APP (same service, its own story) | The `role` and `permission` rows and their version, which this story reads: the matrix is data (REQ-ACA-003) |

Business preconditions carried from RWB-AD-010 and the P4 specifications:

- A list of values version is loaded and waiting for approval; the load is LOADED and its rows have passed the owner's own checks (legacy RWB-AD-009; FSD P4 v3 A2.17 BR-P4-017).
- The list owner holds the A letter in Reference data. TSD P4 v3 T6.1 gives RW-REFADM CRUD on Reference data and RW-COE CRUD, and the legacy permission row "Reference data A: Service identities only" is the row this story corrects (GAP-0817; ASM-1518).
- The approval is effective from the version's `valid_from` date; an approval given before that date is allowed and the state is APPROVED until the date (GAP-0818; ASM-1519).
- Which path the console uses for an approval is Not specified in the source documents (GAP-0816; ASM-1517): the owner's path is P3's and the console path is this story's, and the two are reconciled at contract review.
- The message id of a refused self-approval is MSG-P7-002, a message of the decision centre's catalogue, kept verbatim (GAP-0820; ASM-1521).

### 4. Flow

1. The list owner opens SCR-40 Reference data through the gateway-bff composite route of DP-19. The route calls the owner's `GET /api/recovery/case/v1/admin/lists/{listCode}` (consumed, one hop, 2 s) and shows each version with its list, label, state and valid-from date; a version in LOADED is shown as waiting, one in IN_FORCE as approved.
2. The owner picks the version waiting for approval and calls `POST /api/recovery/access/v1/admin/lov-loads/{loadId}/approve` with an `Idempotency-Key` and no body.
3. `LovLoadApprovalController` validates the call: `loadId` must be present and must be the load reference the owner's read returned; an empty one is 422 with MSG-GEN-001 naming the field. The `Idempotency-Key` is required on every POST; a repeated key answers the stored answer of the first call and writes no second record entry.
4. `PermissionReader` resolves the caller's staff reference and reads the caller's `role` and `permission` rows in `rwb_access` for the capability area REFERENCE_DATA (REQ-ACA-003; TSD P4 v3 T6.1). A caller with no role row at all is refused 403 with MSG-P4-001; a caller without the A letter in Reference data is refused 403 with MSG-P4-002 and one REF-DENY entry is written, and nothing is approved.
5. `LoadReader` reads the load through the owner's reference-data contract: the version, its list code, its `author` reference, its state and its `valid_from` (DP-07). An unknown load is 404 and nothing is written.
6. The state check: a version that is not in LOADED is refused 409 with MSG-GEN-004, because two approvers or an approval and a rollback may have raced, and the approver is told to reload. Nothing is approved and no record is written.
7. `FourEyesRule` compares the load's `author` reference with the approver reference. Where they are the same person, the call is refused 403 with MSG-P7-002 and one REF-DENY entry with decision code `REF-DENY` is written; nothing is approved. Where the author is a service identity, a person may approve, and the entry records both references (ASM-1520).
8. On pass, `LovLoadApprovalService` appends one decision-record entry of the DP-03 library with decision code `REF-APPR`, the load, the list, the version, the effective date and the approver reference, with its outbox row and in the same local transaction that stores the answer under the `Idempotency-Key`. The entry carries no name, no e-mail address and no personal field. Where the record cannot be written the call stops with 503 and MSG-P7-003 and the owner is never asked to move the version, so no reference data changes unlogged (R-UNI-39).
9. The service then calls the owner's `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve`, once, one hop, with a 2 s timeout and a breaker. The owner moves the version LOADED to APPROVED and, from its `valid_from`, to IN_FORCE, and answers the version. Where the owner does not answer inside the budget or answers 503, this service answers 503 and reports that nothing was approved; the record entry stays with outcome REQUESTED so that a retry under the same key resumes the call instead of writing a second entry.
10. The answer is 200 with the version, its state, its effective date, the approver reference and the time. A version approved before its valid-from date answers APPROVED with the future effective date, and the read on that date answers IN_FORCE; no version ever takes effect before its `valid_from` (BR5).
11. A return is the other outcome of the same gate: `POST /api/recovery/access/v1/admin/lov-loads/{loadId}/return` with a `reasonCode` from the coded reason list of the owner's contract. The same authority and the same four-eyes rule apply; the state goes back to LOADED with the version returned to its author, one REF-RTRN entry is written with the reason code, and the author is told the reason on SCR-40. An empty or unknown `reasonCode` is 422 with MSG-GEN-001 and nothing is returned.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds no A letter in Reference data | 403, nothing approved, one REF-DENY entry with the load, the list and the area | MSG-P4-002 | AC3 |
| X2 | The caller holds no role row at all in `rwb_access` | 403 and no record entry, because there is no area to record against | MSG-P4-001 | AC3 |
| X3 | The approver is the load's author | 403, nothing approved, one REF-DENY entry carrying both the author and the approver reference | MSG-P7-002 | AC2 |
| X4 | The load is not in LOADED (already approved, superseded, rolled back or refused) | 409, nothing approved, no record entry; the approver reloads SCR-40 | MSG-GEN-004 | AC1 |
| X5 | The load reference is unknown to the owner's contract | 404, nothing written | None | AC1 |
| X6 | The owner's approve operation does not answer inside the 2 s budget or answers 503 | 503 to the caller and nothing approved; the record entry keeps outcome REQUESTED and a retry under the same key resumes | None | AC1, AC4 |
| X7 | The decision-record entry cannot be written | 503 and the owner is never asked to move the version, so no reference data changes unlogged | MSG-P7-003 | AC1 |
| X8 | The approval is given before the version's valid-from date | 200 with state APPROVED and the future effective date; the read on that date answers IN_FORCE | None | AC4 |
| X9 | The same `Idempotency-Key` arrives twice | The second call answers the stored answer of the first and writes no second record entry | None | AC1 |
| X10 | A return carries an empty or unknown reason code | 422 naming `reasonCode`, nothing returned and no entry written | MSG-GEN-001 | AC5 |
| X11 | The load's author is a service identity | A person may approve; the entry records the service-identity author and the person approver | None | AC2 |
| X12 | The load's list is outside the caller's scope | 404 on the approve call and MSG-P4-003 on the read that builds SCR-40; the list is not named in the refusal | MSG-P4-003 | AC3 |

No exception path of this story writes a list row, a version row or a rule row. The only writes are the decision-record entry, its outbox row and the stored answer.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-AD010-CON and its fakes, and the owner's reference-data contract of RWB-P3-E1043-CON; the load itself is RWB-P4-AD009-APP's and `rwb-case`'s |
| Negotiable | The four-eyes switch, the approval limits and the coded reason list are parameter and reference rows; no role, reason code or limit is fixed in this story |
| Valuable | One approval gate replaces a permission row that named service identities and a separation-of-duty rule that no source had written down |
| Estimable | Two operations, one four-eyes rule, one record appender, one idempotency store, one screen route and one contract-fake run |
| Small | Fits two weeks with its tests; no table, no workflow, no event and no schema of its own |
| Testable | Each of the five criteria has a test case in section 16, and the owner's transition and the record failure are stubbed in the fakes |

### 7. Acceptance criteria

```gherkin
Feature: Approve a reference data load

  Background:
    Given the environment is SIT
    Given list "LOV-ROUTE" carries version "LOV-ROUTE 2027.01" in force from 1 January 2027
    Given test user "U-4201" holds RW-REFADM with the A letter in Reference data

  Scenario: AC1 Approve (legacy RWB-AD-010 AC1)
    Given the rwb-case contract mock returns version "LOV-ROUTE 2027.01" in state "IN_FORCE" from 1 January 2027 with approver "U-4201"
    Given a loaded version waiting for me
    When I approve it
    Then it takes effect from its valid from date and the approval is logged

  Scenario: AC2 Maker cannot approve (legacy RWB-AD-010 AC2)
    Given a version I loaded
    When I try to approve it
    Then I am refused with MSG-P7-002

  Scenario: AC3 An approver without the A letter is refused and the refusal is recorded (new, D-RCV-60)
    Given test user "U-4210" holds RW-RISK with R in Reference data and no A letter there
    When "U-4210" calls POST /api/recovery/access/v1/admin/lov-loads/{loadId}/approve for load "LD-2027-014" with Idempotency-Key "k-401"
    Then the response is 403 with message MSG-P4-002 and nothing is approved
    Then one decision-record entry is written with decision code "REF-DENY", the load, the list and the area, and no personal data

  Scenario: AC4 An approval takes effect from the valid-from date and never retroactively (new, D-RCV-60)
    Given version "LOV-ROUTE 2027.02" is loaded with valid_from 1 February 2027 and version "LOV-ROUTE 2027.01" is in force until 31 January 2027
    Given the rwb-case contract mock returns the approval of "LOV-ROUTE 2027.02" on 20 January 2027 with state "APPROVED" and effective date 1 February 2027
    When the list owner approves it on 20 January 2027
    Then the response is 200 with state "APPROVED" and effective date 1 February 2027
    Then on 1 February 2027 the version reads state "IN_FORCE" and no decision taken before that date is re-decided
    Then version "LOV-ROUTE 2027.01" keeps valid_to 31 January 2027 and stays readable

  Scenario: AC5 A return sends the load back to its author with a coded reason (new, D-RCV-60)
    Given a loaded version waiting for approval that its list owner does not accept
    When the list owner calls POST /api/recovery/access/v1/admin/lov-loads/{loadId}/return with reasonCode "REF-RSN-03"
    Then the response is 200 with state "LOADED" and the reason code
    Then one decision-record entry is written with decision code "REF-RTRN", the load, the list, the version and the reason code
    Then the author is told the reason on SCR-40 and nothing is in force
```

Scenario: AC6 The four-eyes switch and the approval limits are read as parameter rows through DP-06 with the version in force, and no switch value is written in code (new, D-RCV-60)

Scenario: AC7 A repeated approval with the same Idempotency-Key answers the first answer and writes no second entry (new, D-RCV-60)

Scenario: AC8 The service writes no row of lov_value, reference_version or reference_row (new, D-RCV-60)

Scenario: AC9 A call to POST /api/recovery/access/v1/admin/lov-loads/{loadId}/approve for an unknown load answers 404 (new, D-RCV-60)

Scenario: AC10 A consumed owner call that fails or does not answer leaves the load LOADED and reports no approval (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a caller who holds the A letter in Reference data may approve or return a load; the letter is read from the `role` and `permission` rows of `rwb_access` and never from a role name in code | REQ-ACA-003; TSD P4 v3 T6.1; legacy permission row corrected (ASM-1518) |
| BR2 | A caller with no A letter is refused with MSG-P4-002 and the refusal is recorded as one REF-DENY entry | REQ-ACA-007; FSD P4 v3 A2.17 AC-EXC-P4-017-01 |
| BR3 | The approver must not be the load's author; the same person may not author and approve, and a person may approve a load a service identity wrote | Legacy RWB-AD-010 AC2; MSG-P7-002; ASM-1520 |
| BR4 | A load is approved or returned only while it is in LOADED; any other state is 409 with MSG-GEN-004 and nothing changes | Legacy RWB-AD-010; TSD P4 v3 T4 |
| BR5 | An approved version takes effect from its `valid_from` date and never before it; an approval before that date leaves the version APPROVED until the date, and the version it supersedes keeps `valid_to` set to the day before | Legacy RWB-AD-010 AC1; TSD P4 v3 T4; R-UNI-38; ASM-1519 |
| BR6 | A return sends the load back to its author with a code from the coded reason list, leaves it LOADED and is recorded as one REF-RTRN entry | Legacy RWB-AD-010; FSD P4 v3 A2.22 (a versioned table is returned and recorded) |
| BR7 | Every approve, refusal and return appends exactly one decision-record entry of the DP-03 library, with a decision code from its decision-code list (REF-APPR, REF-DENY or REF-RTRN), carrying the package, the version label, the status change (LOADED to APPROVED, or refused), the valid-from date, the author reference, the approver reference and the outcome REQUESTED, written in the local transaction before the owner call; the entry carries no personal data | Principle 5; R-UNI-39; DP-03 |
| BR8 | No action proceeds unlogged: where the record cannot be written the call is 503 with MSG-P7-003 and the owner is never asked to move the version | R-UNI-39; FSD P4 v3 A2.17 AC-EXC-P4-017-02 |
| BR9 | The four-eyes switch and the approval limits are parameter rows read through DP-06 with the version in force; no switch value and no limit is written in code | DP-06; BR-P4-017; FSD P4 v3 A2.17 |
| BR10 | A repeated approval with the same `Idempotency-Key` answers the first answer and writes no second entry | Architecture v5 slide 11; DP-09 idempotency rule |
| BR11 | This story writes no list row and no version row: the version transition is the owner's, asked for through the reference-data contract | DP-01; ASM-0071; ASM-0041 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of two rows of the service's own schema; the REFERENCE_DATA capability area value is a reference list value, so a new area is a row and not a build.
- BR3 is one comparison of two references; it is decided before the owner is called, so a self-approval never reaches the version store and never leaves an approver on the version.
- BR4 is the state the read returned; the owner re-checks it in its own transaction, so a race answers the owner's 409 rather than a silent second approval.
- BR7 and BR8 are the record appender of DP-03 inside the local transaction that stores the answer; the owner's transaction is its own and is not held open by this service.
- BR9 is the parameters client of DP-06; a test proves that turning the four-eyes switch off is a data change with no build, and the switch is on in production.
- BR11 is the absence of any write method for `lov_value`, `reference_version` and `reference_row` in this service.

### 9. State transitions

This service holds no version state of its own; it holds the gate's outcome and the record of it. The version lifecycle is the owner's, and it is the one TSD P4 v3 T4 defines.

| From | Event | Condition | To |
|---|---|---|---|
| LOADED | Approve, approver holds A and is not the author | The valid-from date has arrived or is today | APPROVED, then IN_FORCE on the valid-from date |
| LOADED | Approve, approver holds A and is not the author | The valid-from date is in the future | APPROVED until the date, then IN_FORCE |
| LOADED | Approve, approver is the author | None | LOADED, refused with MSG-P7-002, one REF-DENY entry |
| LOADED | Approve, caller holds no A letter | None | LOADED, refused with MSG-P4-002, one REF-DENY entry |
| LOADED | Return with a coded reason | None | LOADED, returned to the author, one REF-RTRN entry |
| LOADED | Approve, the owner does not answer | None | LOADED, 503, the entry keeps outcome REQUESTED |
| APPROVED | The valid-from date arrives | None | IN_FORCE |
| IN_FORCE | The next version comes into force | None | SUPERSEDED, with `valid_to` on the day before |
| IN_FORCE | A rollback | The rollback is RWB-P4-AD009-APP's | ROLLED_BACK |

| Command | Condition | Outcome |
|---|---|---|
| Approve | A letter in Reference data, not the author, version LOADED, record written | 200, version APPROVED or IN_FORCE, one REF-APPR entry, the owner called once |
| Approve | No A letter | 403 MSG-P4-002, one REF-DENY entry, no owner call |
| Approve | Approver is the author | 403 MSG-P7-002, one REF-DENY entry, no owner call |
| Approve | Version not LOADED | 409 MSG-GEN-004, no entry, no owner call |
| Return | A letter in Reference data, version LOADED, a valid reason code | 200, version LOADED and returned, one REF-RTRN entry |
| Any | The record cannot be written | 503 MSG-P7-003, no owner call, no state change |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The list owner holding the A letter in Reference data (RW-REFADM, RW-COE per TSD P4 v3 T6.1) | Approve or return a loaded version of a list it owns |
| RW-SECADM and RW-PLATADM | Hold no A in Reference data in TSD P4 v3 T6.1, so they are refused with MSG-P4-002; a role that needs the letter gets a `permission` row, not a code change |
| Publish of a list version | Not an operation of this story: the publish is the owner's and is read as Reference data C; the approval here carries only the A letter and grants no C letter |
| Service identities (RW-REFADM's data load path) | May author and load a version; they may not approve it, and a person approves what they wrote |
| RW-AUDIT | Reads the approval record through the decision record chain; it calls no operation of this story |
| `rwb-access` itself | Reads `role` and `permission` in its own schema, reads the load through the reference-data contract, and writes no list or version row |
| The gateway-bff route | Calls this service and the owner's list read once each for SCR-40; it holds no right of its own |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set: MSG-P4-002 for an absent letter, MSG-P4-001 for an absent role, MSG-P7-002 for a self-approval. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` in `rwb_access` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` in `rwb_access` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-027 to DF-REF-033 | `lov_value` of `rwb-case` | id, lov_code, value_code, label_en, label_th, sort_order, valid_from | Read through DP-07, never written |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb-case` | the version, its state, its author, `valid_from` and `valid_to`, and the coded return reasons | Read through DP-07 |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the REF-APPR, REF-DENY and REF-RTRN entry of an approval, a refusal or a return | Write |
| (outbox) | outbox library table in `rwb_access` | the record row and its `DecisionRecorded` message | Write |
| (idempotency) | `idempotency_key` in `rwb_access` | the stored answer of each approve and return call | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No row of `lov_value`, `reference_version` or `reference_row` is written in this story: the store is P3 `rwb-case`'s under ASM-0071, and the load is RWB-P4-AD009-APP's. No row of `decision_log_entry` (P7) or of the case tables (P3) is read: the local record goes on `rwb.decision-record.v1` and the central ledger is `rwb-decision`'s (DP-01, DP-03). The approver's staff reference and group resolve through `v_ace_iam_group`, a read of the service's own ACE view, and no personal field, name or e-mail address is stored, logged or put in an event (DP-05).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/access/v1` (DP-13). Owner P4 `rwb-access`.

| Method | Path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| POST | `/admin/lov-loads/{loadId}/approve` | None | `LovLoadApproval`: `loadId`, `lovCode`, `version`, `state`, `validFrom`, `approverReference`, `approvedAt` | 401 MSG-P4-001; 403 MSG-P4-002 or MSG-P7-002; 404 unknown load; 409 MSG-GEN-004; 422 MSG-GEN-001; 503 MSG-P7-003 or owner unavailable | Reference data, right A, scope applied | `Idempotency-Key` required; a repeat answers the stored answer |
| POST | `/admin/lov-loads/{loadId}/return` | `ReturnRequest`: `reasonCode` from the coded reason list | `LovLoadApproval` with `state` LOADED and `reasonCode` | 401 MSG-P4-001; 403 MSG-P4-002 or MSG-P7-002; 404; 409 MSG-GEN-004; 422 MSG-GEN-001; 503 MSG-P7-003 | Reference data, right A, scope applied | `Idempotency-Key` required |

The legacy story named the approval path as `/admin/reference-loads/{loadId}/approve` under the single monolith base that DP-13 replaces, with the right "Reference data A"; it is TSD P4 v3 appendix T-A endpoint API-P4-006 under the per-service base of DP-13. The ownership map rules that path P3 `rwb-case`'s under ASM-0041, because the version store is the reference-data store, so this story keeps the console path under its own base and calls the owner's path as a consumer. Which path the console uses, and whether the console keeps a path of its own at all, is Not specified in the source documents (GAP-0816; ASM-1517); the contract review reconciles the two paths before either is frozen. `lov-loads` is chosen because the load, not the stored list, is what is approved.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | P3 `rwb-case` | Moves the version LOADED to APPROVED and to IN_FORCE from its valid-from date; answers the version |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case` | The version, its author reference, its state, its `valid_from` and the coded return reasons, read back for the gate and for SCR-40 |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own) | The A letter in Reference data for the caller, with the MSG-P4-002 refusal shape |

None of the three is declared as provided by this story, and no operation of another service is called twice on one approve: the authority and the load read happen before the transition, and the transition is the last call.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of an approval, a refusal or a return: decision code, load, list, version, effective date, approver reference and outcome |

Nothing is published on `rwb.access.events.v1`. This story changes no access policy and no delegation limit, so `AccessPolicyChanged` and `DoaLimitChanged` are not its events; the approval moves reference data that `rwb-case` owns, and that service's own events carry the change.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this story adds no subscription.

#### 12.5 Workflows and activities

None. The approval is one synchronous command with one downstream call; there is no long-running wait, no timer and no activity on the `rwb-access` queue.

#### 12.6 Schedules

None for this story. The six-monthly access review list is a Schedule of `rwb-access` and belongs to the service's own story.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the caller's role and class |
| `permission` | P4 (`rwb_access`) | Read only: the A letter in Reference data |
| `outbox_event`, `idempotency_key`, `processed_event` | PLT library, created in `rwb_access` | The outbox row of the record and the stored answer of each call; no inbox row is written because no event is consumed (DP-09) |
| `lov_value`, `reference_version`, `reference_row` | P3 (`rwb_case`) | Not owned and not read from the schema: read through the reference-data contract of DP-07 (ASM-0071) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is `rwb-decision`'s |

No foreign key crosses a schema and no SQL statement of this story names a table of another service (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case reference-data WireMock | RWB-P3-E1043-CON | Version "LOV-ROUTE 2027.01" in force from 1 January 2027, author "U-4101", approver "U-4201", for AC1; "LOV-ROUTE 2027.02" loaded with valid_from 1 February 2027 and its approval on 20 January 2027 in state APPROVED, for AC4; a version in LOADED with author "U-4211" waiting for approval; a version in SUPERSEDED for the 409 of X4; a 404 for an unknown load; a 503 and a timeout for X6; the coded reason list with "REF-RSN-03" |
| rwb-case approve fake | RWB-P3-E1043-CON | The owner's `POST /admin/reference-loads/{loadId}/approve` answering the moved version, and its 409 when the version is no longer LOADED |
| parameters fake | RWB-P3-E1042-CON | The four-eyes switch row on, and the approval-limit rows of the load, read with the version in force |
| decision-record fake | RWB-PLT-E1027-CON | The record append, the hash-chain check and the forced failure of X7 |
| authorise and guard fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The A letter for RW-REFADM and RW-COE, the refusal with MSG-P4-002 for RW-RISK, and the no-role answer with MSG-P4-001 |
| gateway-bff route fake | RWB-PLT-N001-CON | The SCR-40 composite route: the list read, the version list and the states waiting, approved, refused and returned |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2; consumed 3 | Two console operations on `/api/recovery/access/v1`; the owner's approve and list read, and this service's own authorise operation; one hop, 2 s timeout |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision.DecisionRecorded.v1` through the DP-03 library; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | No workflow and no timer in the gate |
| File | None | The load file is RWB-P4-AD009-APP's; this story reads no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/referenceload`, Java package `th.co.scb.ace.workbench.recovery.access.referenceload`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process approval method on the reference-data service (DP-11: a REST contract with a mock, one hop and a 2 s timeout), the direct write to `recovery.lov_value` with its `approved_by` column (DP-01 and DP-07: the store is `rwb-case`'s and the approval is a decision record), the reading of the monolith permission table (DP-05: the service's own `role` and `permission` rows plus `v_ace_iam_group` for the group mapping), the permission row "Reference data A: Service identities only" (REQ-ACA-003: the matrix is data and the list owner holds A), and the ace-web screen (DP-19: the SCR-40 composite route). DP-06 carries the four-eyes switch and the approval limits, so neither is a constant.

This story adds no dependency of its own beyond the metadata row: the libraries, the parameters and reference-data contracts, the gateway route and the load are already build dependencies of the P4 service's own stories (RWB-P4-E1037-CON, RWB-P4-E1038-APP and RWB-P4-AD009-APP), and this story builds against their published contracts and fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LovLoadApprovalController | Controller | The two operations, the `Idempotency-Key` check, the RFC 9457 error mapping and `messageId` on every refusal |
| LovLoadApprovalService | Service | The gate: authority, state, four eyes, the owner call, the answer and the record |
| PermissionReader | Service | The caller's `role` and `permission` rows in `rwb_access` and the A letter in REFERENCE_DATA |
| LoadReader | Client | The owner's list read: version, author, state, `valid_from` and the coded reasons, one hop and 2 s |
| VersionTransitionClient | Client | The owner's approve call, once per approved gate decision, with the breaker |
| FourEyesRule | Service | BR3: the author reference against the approver reference, and the service-identity case |
| DecisionRecordWriter | Service | The REF-APPR, REF-DENY and REF-RTRN entry in the transaction that stores the answer, with the outbox row |
| IdempotencyStore | Service | The stored answer per `Idempotency-Key`, so a repeat answers the first call and writes no second entry |

**Database and migrations**

- This story creates no table of its own. `role` and `permission` are created and loaded by RWB-P4-E1037-CON and RWB-P4-E1038-APP, and the outbox and idempotency rows are created in the `rwb_access` baseline by RWB-P4-AD009-APP's migration in the per-service Flyway sequence of DP-15.
- The only writes are the decision-record row, its outbox row and the `idempotency_key` row, in one local transaction. Nothing writes `lov_value`, `reference_version` or `reference_row`.
- Where SIT needs an index on `idempotency_key` beyond the baseline, the index is added to the baseline story's migration, not to a new migration here.

**Configuration and reference data**

- The four-eyes switch and the approval limits are parameter rows of `rwb-case` read through the parameters client of DP-06 with the version in force; the switch is on in production, and a test proves that turning it off is a data change with no build (BR9).
- The REFERENCE_DATA capability area and the coded return reasons are reference list values read through DP-07; no area, reason code or role name is a Java constant (BR1, BR6).
- The list, its versions and their dates belong to the owner; this story stores none of them and keeps none of them in a cache beyond the request.

**Build steps**

1. `LovLoadApprovalController` with the two paths, the `Idempotency-Key` requirement and the error envelope; contract test against RWB-P4-AD010-CON.
2. `PermissionReader` and the A letter in REFERENCE_DATA: the allowed answers for RW-REFADM and RW-COE and the refusals with MSG-P4-002 and MSG-P4-001; tests for AC3 and X2.
3. `LoadReader` over the owner's list read, with the one-hop client and the 2 s budget; tests for the 404 and for a version read in each of the four states.
4. `FourEyesRule`: the same person refused with MSG-P7-002, and a service-identity author approved by a person; tests for AC2 and X11.
5. The state check and its 409 with MSG-GEN-004 for a version already approved, superseded, rolled back or refused.
6. `DecisionRecordWriter` and `IdempotencyStore`: one entry per decision, the stored answer, the forced failure of X7 and the repeated key of X9; tests for AC1 and the NFR case.
7. `VersionTransitionClient` and the resume path: a timeout answers 503 with nothing approved, and the retry under the same key resumes without a second entry.
8. The date test of AC4 on a fixed clock: an approval before the valid-from date answers APPROVED, the read on the date answers IN_FORCE, and the superseded version keeps `valid_to`.
9. The return path with the coded reason list, the 422 for an empty or unknown code, and the REF-RTRN entry; test for AC5.
10. The SCR-40 composite route against the gateway-bff fake, with the four states waiting, approved, refused and returned.

**Feature switch.** The gate is not behind a flag: a reference-data version that could be approved without the gate would be the defect this story exists to close. The one switch that changes its behaviour is the four-eyes parameter row of DP-06, and the contract keeps the rule as an invariant so that a switch turned off is a deliberate, recorded data change.

**Done when.** The tests in section 16 pass; a list owner approves a loaded version in SIT and it takes effect from its valid-from date; the loader is refused with MSG-P7-002 and a role without the A letter with MSG-P4-002, each with one REF-DENY entry; an approval before the valid-from date never takes effect early; a return with a coded reason leaves the version LOADED with one REF-RTRN entry; a repeated key writes one entry; and a forced record failure stops the action with MSG-P7-003 and no version moves.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller holds no Recovery Workbench role row | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no A letter in Reference data | You cannot {action} here. Your role does not include it. | This story, on both operations |
| MSG-P4-003 | The load's list is outside the caller's scope | This case is not in your scope. | This story, on the read that builds SCR-40 and on the approve call |
| MSG-GEN-001 | `loadId` or `reasonCode` is empty or the code is not in its list | Enter {field}. | This story, on both operations |
| MSG-GEN-004 | The load is not in LOADED when the call arrives | Someone else changed this record. Reload it to see their change. | This story, on both operations |
| MSG-P7-002 | The approver is the load's author | You prepared this decision, so you cannot approve it. | This story, on both operations |
| MSG-P7-003 | The decision-record entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |

Every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request.

The message catalogue carries MSG-P7-002 for the decision centre, where the same separation-of-duty rule refuses an approver who prepared the decision. The legacy criterion of RWB-AD-010 uses that id word for word, so this story reuses the message rather than renumbering it: the refusal here is the same refusal in a second place, and one id for one rule is what an approver and an auditor can follow. Adding it to the P4 catalogue is the assumption recorded as ASM-1521 (GAP-0820).

### 15. Screens and states

One screen, SCR-40 Reference data, served through the gateway-bff composite route of DP-19. The route calls the owner's list read and this service's operations; the browser calls no service directly and holds no right of its own.

| Screen | State | Where it is |
|---|---|---|
| SCR-40 Reference data | Waiting: versions in LOADED with their author and valid-from date | `rwb-access` and `rwb-case` through gateway-bff; this story answers the approve and return |
| SCR-40 Reference data | Approved: the version in IN_FORCE from its valid-from date, with the approver reference and the time | Same route; the answer of the approve call |
| SCR-40 Reference data | Refused: MSG-P7-002 for a self-approval or MSG-P4-002 for a role without the letter, with nothing changed | Same route; the refusal of the approve call |
| SCR-40 Reference data | Returned: the version back in LOADED with its reason code, shown to its author | Same route; the answer of the return call |
| SCR-40 Reference data | Empty: no list loaded for the code | Same route; the owner's empty answer |
| SCR-40 Reference data | Loading: Not specified in the source documents (CG-ALL-4718) | Not specified in the source documents (CG-ALL-4718) |
| SCR-40 Reference data | Error: Not specified in the source documents (CG-ALL-4718) | Not specified in the source documents (CG-ALL-4718) |
| SCR-40 Reference data | No access: Not specified in the source documents (CG-ALL-4718) | Not specified in the source documents (CG-ALL-4718) |

SCR-39 Rules and parameters is not served by this story: the rule-version load and its approval are RWB-AD-011's. SCR-39 has no state in this story; its empty, loading, error and no-access states are Not specified in the source documents (CG-ALL-4717). The gateway-bff composite route specification, the screen field list and the masking of any field on SCR-40 are the platform story's (RWB-PLT-N001-CON); this story fixes the two console operations the route calls, the approve and the return under /api/recovery/access/v1/admin/lov-loads. The version transition stays with rwb-case and is called as a consumed contract; the approve path is reconciled with the ownership map at contract review before either is frozen. No masking-profile operation and no PII table belong to this story: the unmask read goes through the ACE Common PII logging client, and a rule's view and column resolve through the field id of the P1 field registry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-010-01 | AC1, BR5, BR7 | Component | Version "LOV-ROUTE 2027.01" loaded with author "U-4101", approved by "U-4201" holding RW-REFADM with A in Reference data; the owner fake answers IN_FORCE from 1 January 2027 and one REF-APPR entry is written |
| TC-AD-010-02 | AC2, BR3 | Component | Approver "U-4101" is the author of the load; refused with MSG-P7-002, one REF-DENY entry, and the owner is never called |
| TC-AD-010-03 | AC3, BR1, BR2 | Component | "U-4210" holds RW-RISK with R in Reference data; refused with MSG-P4-002 and one REF-DENY entry; a caller with no role row is refused with MSG-P4-001 |
| TC-AD-010-04 | AC1, BR7, BR8 | NFR | The decision-record write forced to fail during an approve and during a return; 503 with MSG-P7-003, the owner is never called and no version moves |
| TC-AD-010-05 | AC4, BR5 | Component | "LOV-ROUTE 2027.02" with valid_from 1 February 2027 approved on 20 January 2027; the answer is APPROVED, the read on 1 February 2027 is IN_FORCE, and "LOV-ROUTE 2027.01" keeps valid_to 31 January 2027 |
| TC-AD-010-06 | AC5, BR4, BR6 | Component | A return with "REF-RSN-03" leaves the version LOADED with one REF-RTRN entry; an empty code is 422 with MSG-GEN-001; a version already approved is 409 with MSG-GEN-004 |
| TC-AD-010-07 | §12 operations, events and activities | Contract | The two provided operations and the three consumed operations of section 12 checked against API Specification v5; the event rwb.decision.DecisionRecorded.v1 on topic rwb.decision-record.v1 checked against Kafka Catalog v1 |
| TC-AD-010-08 | §12.7 tables (ASM-3438) | Component | Each table of section 12.7 checked: the service reads only through its owner's path, and an SQL statement naming lov_value, reference_version, reference_row or decision_log_entry is refused |
| TC-AD-010-09 | AC6, BR9 | Component | The four-eyes switch is read from the parameter rows through DP-06; setting it off in the parameter data changes the answer with no build, and no switch value is written in code |
| TC-AD-010-10 | AC7, BR10 | Component | A repeated approve with the same Idempotency-Key answers the first answer and writes no second REF-APPR entry |
| TC-AD-010-11 | AC8, BR11 | Component | The service's write paths are checked: no write to lov_value, reference_version or reference_row, and an approve moves the version only through the owner's approve call |
| TC-AD-010-12 | AC9 | Component | An approve call on a load ID with no row answers 404; no version moves |
| TC-AD-010-13 | AC10, BR4 | Component | The owner approve call forced to fail and forced not to answer; the load stays LOADED and no approval is reported |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component, Access to Component and Principle 5 to NFR. The four legacy cases are kept as they stand because the legacy key carries them: TC-AD-010-01 and TC-AD-010-02 cover the two legacy criteria, TC-AD-010-03 the access refusal and TC-AD-010-04 the forced record failure. The integration copy of the whole set is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the capability area, the coded return reasons, the four-eyes switch and the approval limits are rows and reference list values, read with the version in force (BR1, BR9). A test proves that a new reason code and a new area need no build.
- No personal data anywhere: the load reference, the list code, the version label, the dates and the approver reference are the whole payload; the record entry, the event and every log line carry no name, no e-mail address and no personal field, and the staff reference resolves through `v_ace_iam_group` only for the authority check (DP-05).
- No read of another service's tables (DP-01): `lov_value`, `reference_version` and `reference_row` are `rwb-case`'s and are read through the reference-data contract of DP-07; `decision_log_entry` is `rwb-decision`'s and is not read.
- One writer for the version: only `rwb-case` moves it. This service has no write method for a list or a version row, so a gate decision can never change reference data by itself (BR11).
- No action without its record: the record commits before the owner is asked to move the version, and a failed write answers MSG-P7-003 with nothing approved (BR8).
- The gate is idempotent: the stored answer under the `Idempotency-Key` means a double click, a retry or a gateway repeat cannot approve two versions or write two entries (BR10).
- A refusal tells the caller what it may know and nothing more: no other version, no other list and no role name is returned, so a refusal cannot be used to map the reference data or the role matrix.
- The screen is served through the gateway-bff route of DP-19 and calls no service directly; the browser holds no token with a Reference data right of its own.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-011 | Versioned reference data with valid-from and valid-to dates, author and approver | Epic 8 administration; Program 5.4 reference data | FEAT-ADM-01, FEAT-ADM-06 | 12 Administer reference data | BR4, BR5, BR6, BR7 | TC-AD-010-01, TC-AD-010-05, TC-AD-010-06, TC-AD-010-07, TC-AD-010-08, TC-AD-010-10, TC-AD-010-11 |
| REQ-ACA-003 | The role to permission matrix is data and the only source of what a role may do | Epic 1 access; Program 5.1 access | FEAT-ACA-04 | 12 Administer reference data | BR1, BR2 | TC-AD-010-03 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation for the security administrator | Epic 8 administration | FEAT-ADM-01 | 12 Administer reference data | BR2, BR9 | TC-AD-010-03, TC-AD-010-04, TC-AD-010-09 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy criteria AC1 and AC2 of RWB-AD-010, word for word with their origin tags | Section 7, TC-AD-010-01 and TC-AD-010-02 |
| Approval effective from the valid-from date, and the approval logged | Sections 4, 7, 8, 9, 12.1 |
| The maker may not approve, refused with MSG-P7-002 | Sections 4, 5, 7, 8, 14 |
| SCR-40 Reference data with the load, and SCR-39 for the rule versions | Sections 1, 15, 19 |
| Permission checks "Rules and parameters A: RW-RISK" and "Reference data A" | Sections 8, 10, 14 (the second row corrected per ASM-1518) |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-002, MSG-P7-003 | Section 14 and the exception paths of section 5 |
| Test cases TC-AD-010-01 to TC-AD-010-04 | Section 16 |
| Rule IDs R-UNI-38 and R-UNI-39 | Sections 2, 8, 14, 17 |
| Field IDs DF-REF-027 to DF-REF-044, DF-REF-159 to DF-REF-184, DF-DEC-001 to DF-DEC-018 | Section 11 |

### 19. Out of scope

- The load itself: the file, the row checks, the verification and the version store (RWB-P4-AD009-APP with `rwb-case`). This story approves or returns a load; it never creates one and never edits one.
- The version transition and the version lifecycle states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED, which are `rwb-case`'s under ASM-0071 and ASM-0041.
- The rollback of a configuration version (FSD P4 v3 A2.22, FEAT-ADM-06), which RWB-P4-AD009-APP and the owner carry; this story reads a rolled-back version only to refuse it with MSG-GEN-004.
- The rule-version load and its approval, SCR-39 Rules and parameters and the right "Rules and parameters A: RW-RISK" (RWB-AD-011).
- The delegations of authority table and its approval path (RWB-P4-E1038-APP); the approval limits read through DP-06 are parameter rows of `rwb-case`.
- The base build of the two console paths as a service-wide contract; that is RWB-P4-AD010-CON's, and this story implements against it.
- The cross-service journey harness and its evidence; no `-ITG` story is split from this legacy key here.
- The Helm chart, the Kafka subscription values, the dashboards, the alerts and the runbook of this capability (an OPS story of this legacy key).
