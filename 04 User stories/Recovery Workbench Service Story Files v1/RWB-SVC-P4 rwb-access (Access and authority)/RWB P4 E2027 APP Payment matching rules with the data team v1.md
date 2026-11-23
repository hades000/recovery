# RWB-P4-E2027-APP Payment matching rules with the data team

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2027-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-AR |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P8-E2027-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CHO-009) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: created as the rwb-access slice of legacy RWB-E2-027 — the payment-matching access profile: the rights of the four roles of the legacy story held as permission rows, the session answer, the refusal and the read entries of the matching operations. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM)**, I want **the payment-matching rights of the data-team matching slice held as permission rows of the matrix version in force and answered for every caller of the matching operations — the receipt read, the exception-list read, the rule-package load and the rule-version approve — with every refusal and every exception-list read written as one access entry naming the area, the right, the matrix version and the case**, so that **a role without the right cannot see a receipt or change a matching rule, and every person who read the unmatched list can be named afterwards**.

Inside `rwb-access` this is the authority half of the legacy story RWB-E2-027:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access` (context pack P4).
- One deliverable: the `PaymentMatchAccessProfile` (the area and the right each matching operation needs), the `RightResolver` that answers ALLOW or DENY from the `permission` rows of the matrix version in force, the session and roles answers that carry those rows, and the AC-DENY and AC-READ entries the matching operations write, read through `GET /api/recovery/access/v1/admin/access-log` (DP-01, DP-03).
- The match itself stays with `rwb-payment` (P8, RWB-P8-E2027-APP): JOB-07, the `RuleEvaluator` call, the fired row, the proceeds row and the exception list. This story matches nothing, writes no proceeds row and reads no ACE view.
- The package, its versions, the parsed rows and the approval stay with `rwb-decision` (P7, RWB-P7-E2027-APP); the workbook and its Rows and Tests tabs stay with `rwb-case` (P3, RWB-P3-E2042-APP); the installment shortfall stays with `rwb-treatment` (S2). This story holds only the right that gates each of those calls.
- The rights are the legacy values unchanged: RW-CREDITAD Write-off and posting CRUA, RW-FINANCE Write-off and posting RA, RW-COE Rules and parameters C, RW-RISK Rules and parameters A (legacy section 10). The capability areas are values of LOV-CAPABILITY: `WRITE_OFF_AND_POSTING` and `RULES_AND_PARAMETERS` (TSD P4 T3.2).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-2311; ASM-3838); this story uses the phrase "the rwb-access login (DP-02)" and never the shared monolith login.
- The permission rows of the four roles are already in force in matrix version "PM-2026.11"; they are loaded and approved by the matrix stories of this service and are not rebuilt here (ASM-3836). This story serves and enforces them.

### 2. Business rationale

RWB-E2-027 makes most receipts match without a person and lists the rest, and its authority section says who may read that list and who may change the rule behind it. A matching rule that any role can load, or an exception list that any role can read without a trace, would defeat the control the story serves: CTL-41 and REQ-CHO-009 are only met if the person who reads the unmatched receipts is named, and if the person who changes a threshold is not the person who approves it.

In the monolith the check was a hard-coded role test inside the payments module, and the access trail was a single shared log. The realignment moves the rows and the answer to the owner of access (Arch v5 slides 4 and 8) and makes every other service's guard read that answer; the entry becomes an append-only decision record in the serving service's own schema. This story is the slice that holds the four role rows of the legacy story, answers them on the session, refuses the receipt read, the exception-list read and the rule-package calls of a role that lacks the right, and records each refusal and each exception-list read with the matrix version that decided it.

It serves REQ-CHO-009 on the authority side and carries the legacy control CTL-41: every match names its rule and its package version, and every read of the unmatched list names its reader. It changes no business rule of the matching itself.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P8-E2027-CON | The published rwb-payment contract: the matched and unmatched receipt read, the exception-list read and what a receipt item holds (case id, payment code, amount, date, matched flag, rule and package version). This profile serves that contract; the read is not built here. Faked, one hop, 2 s (DP-11) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): one entry per refusal and per exception-list read, written in the transaction of the action |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the rwb-case reference-data contract (DP-07): LOV-CAPABILITY, LOV-ROLE and LOV-SCOPE with the version in force |
| RWB-PLT-E1047-CON | The naming library (DP-14): the topic and event names of section 12 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the SCR-28 proceeds-matching route and the session fragment it serves |
| RWB-P4-E1037-APP, RWB-P4-AD002-APP | The `role` and `permission` tables and the matrix load that put the four roles' rows in force. Reused where they have landed and built against their published rows (ASM-3836); no build dependency of this story |
| RWB-P4-E1022-APP | `GET /api/recovery/access/v1/me/session` and the session answer that carries the roles, the letters and the matrix version; extended here, not rebuilt |

Business preconditions carried from RWB-E2-027 (legacy sections 3, 5 and 10):

- Matrix version "PM-2026.11" is in force with RW-CREDITAD Write-off and posting CRUA, RW-FINANCE Write-off and posting RA, RW-COE Rules and parameters C and RW-RISK Rules and parameters A; version "PM-2026.12" is in force from 2026-12-01 and leaves the two payment-matching areas unchanged (FSD P4 AC-P4-004-01; ASM-3832).
- Case "RC-2026-000555" has account "A-0555" and plan "T-0701" with installment amount 12,500.00 THB and next installment date 2026-12-15; the exception list of 2026-12-14 holds one unmatched payment, "PAY-91006" of 10,000.00 THB. PAYMENT_MATCH version "PM-2026.12" is in force from 2026-12-01 and version "PM-2027.01" is loaded with valid from 2027-01-01 (legacy AC3, AC5, AC6).
- Synthetic data only: role codes, matrix versions, the legacy payment codes and the case above; no real account, customer or payment (legacy section 17).

### 4. Flow

1. A caller of a matching operation presents the session token; the guard of the serving service resolves the caller's roles and letters from the session answer of `GET /api/recovery/access/v1/me/session` and asks `PaymentMatchAccessProfile` for the area and the right the operation needs.
2. `RightResolver`: reads the `permission` rows of the caller's roles for that area at the matrix version in force, takes the union of the letters over the roles held, and answers ALLOW when the right is present and DENY when it is absent. A role the caller does not hold contributes nothing, and a missing row is DENY, never ALLOW.
3. On ALLOW the guarded operation runs: the receipt read, the exception-list read, the package-version load or the rule-version approve. This story builds none of those four operations.
4. On DENY the guarded call stops with status 403 and MSG-P4-002 before the operation runs, and `RefusalRecorder` writes one AC-DENY entry with the area, the right, the result REFUSED and no payment, account or case data; the entry is committed before the 403 is returned.
5. RW-CREDITAD or RW-FINANCE: reads the matched and unmatched receipts of a case on SCR-28 through the gateway-bff route. The read is allowed from WRITE_OFF_AND_POSTING R; `ReadRecorder` writes one AC-READ entry with the actor, the case id, the filter, the row count and the matrix version in force.
6. RW-SECADM: reads the entries of a user and a period through `GET /api/recovery/access/v1/admin/access-log`, with the decision code AC-READ or AC-DENY, the area, the right, the result, the case id, the row count and the matrix version of each entry.
7. RW-SECADM: reads the roles and their permission rows through `GET /api/recovery/access/v1/admin/roles`; the answer names the role, the area, the letters and the matrix version, so the four rows of the legacy story are visible as data.
8. Nothing in this story matches a payment, evaluates a rule package, writes a proceeds row, approves a version or changes a case status.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the Write-off and posting right reads the receipts | 403 before the read runs; no receipt data; one AC-DENY entry with area WRITE_OFF_AND_POSTING and right R | MSG-P4-002 | AC2, TC-E2-027-11 |
| X2 | A role without the Rules and parameters C loads a package version | 403 before the load runs; no version is written; one AC-DENY entry with area RULES_AND_PARAMETERS and right C | MSG-P4-002 | AC3, TC-E2-027-12 |
| X3 | A role holding C but not A approves a loaded version | 403 before the approval runs; the version stays LOADED; one AC-DENY entry with right A | MSG-P4-002 | AC6 |
| X4 | No permission row exists for the role and the area of the call | DENY, not ALLOW; 403; one AC-DENY entry with the area and the right | MSG-P4-002 | AC7 |
| X5 | The session cannot be resolved, or the caller holds no Workbench role | 401 and no operation runs; one AC-DENY entry with reason NO_ROLE is written where the token identifies a user | MSG-P4-001 | TC-E2-027-11 |
| X6 | The entry of a refusal or of an exception-list read cannot be written | The refusal stands and the read returns nothing; the call answers 503; an incident is raised; no unaudited read is served | MSG-P7-003 | AC4, TC-E2-027-13 |

The entry of a refusal and the entry of a read are written before the answer leaves the service, so a read that cannot be recorded is not served (legacy BR8 and guardrail 4). A stale `permission` row at commit, matched on its `version` column, is MSG-GEN-004 and the call is retried, never applied twice.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P8-E2027-CON, the platform contracts of its DP table and the fakes; it matches no payment, evaluates no rule package and rebuilds no matrix load |
| Negotiable | The roles, the letters, the areas and the matrix versions are rows and reference data; the story fixes only the profile, the union rule, the deny-by-default rule and the entry shape |
| Valuable | A role without the right cannot read a receipt or change a matching rule, and every read of the unmatched list names its reader and its matrix version |
| Estimable | One profile, one resolver, one session assembler, one refusal recorder, one read recorder and one repository |
| Small | Fits two weeks with its tests |
| Testable | Each criterion is a session read, a roles read, a refused call or a logged read, with a fixed Given, When and Then |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching rules with the data team

  Background:
    Given the rwb-payment contract mock returns the matched and unmatched receipts of case "RC-2026-000555" for a caller holding Write-off and posting R
    Given matrix version "PM-2026.11" is in force with RW-CREDITAD Write-off and posting "CRUA", RW-FINANCE Write-off and posting "RA", RW-COE Rules and parameters "C" and RW-RISK Rules and parameters "A"
    Given case "RC-2026-000555" has account "A-0555" and running plan "T-0701" with installment amount 12,500.00 THB and next installment date 2026-12-15

  Scenario: AC1 The payment-matching rights are rows and the session answers them (new, D-RCV-60)
    Given the rwb-payment contract mock returns the exception list of 2026-12-14 with 1 unmatched payment "PAY-91006" for case "RC-2026-000555"
    When RW-CREDITAD calls GET /api/recovery/access/v1/me/session
    Then the answer holds the role "RW-CREDITAD", its scope, the matrix version "PM-2026.11" and the capability area "WRITE_OFF_AND_POSTING" with the letters "CRUA"
    And no letter comes from a role the caller does not hold
    When RW-FINANCE calls the same operation
    Then the answer holds "WRITE_OFF_AND_POSTING" with the letters "RA"
    When RW-COE calls the same operation
    Then the answer holds "RULES_AND_PARAMETERS" with the letters "C"
    And the session answer of RW-RISK holds "RULES_AND_PARAMETERS" with the letters "A"

  Scenario: AC2 A receipt read without the right is refused and recorded (new, D-RCV-60)
    Given RW-CASEOWN holds no Write-off and posting right
    When RW-CASEOWN reads the matched receipts of case "RC-2026-000555"
    Then the call is refused with status 403 and MSG-P4-002 for the action "read proceeds"
    And no call reaches the rwb-payment contract mock
    And one entry with decision code "AC-DENY", area "WRITE_OFF_AND_POSTING", right "R" and result "REFUSED" is written before the 403
    And the entry holds no payment code, no account key and no amount

  Scenario: AC3 A package-version load without the right is refused and recorded (new, D-RCV-60)
    Given RW-CASEOWN holds no Rules and parameters right
    When RW-CASEOWN calls the guarded load of a PAYMENT_MATCH package version
    Then the call is refused with status 403 and MSG-P4-002 for the action "load a rule version"
    And the load does not run and no version label is written
    And one entry with decision code "AC-DENY", area "RULES_AND_PARAMETERS" and right "C" is written and is returned by GET /api/recovery/access/v1/admin/access-log for that user

  Scenario: AC4 The exception-list read is recorded with its case and matrix version (new, D-RCV-60)
    Given the rwb-payment contract mock returns the exception list of 2026-12-14 with 1 unmatched payment "PAY-91006" of 10,000.00 THB for case "RC-2026-000555"
    When RW-CREDITAD reads the unmatched receipts of case "RC-2026-000555" on SCR-28 through the gateway-bff route
    Then the read is allowed and the answer holds the 1 unmatched item
    And one entry with decision code "AC-READ", the actor, the case id "RC-2026-000555", the filter "matched=false", the row count 1 and matrix version "PM-2026.11" is written before the answer
    And the entry holds no payment code, no account key and no amount
    And GET /api/recovery/access/v1/admin/access-log returns that entry for the actor and 2026-12-14

  Scenario: AC5 The right is a row of the matrix version in force (new, D-RCV-60)
    Given RW-CREDITAD read the matched receipts of case "RC-2026-000555" on 2026-11-30 under matrix version "PM-2026.11"
    And matrix version "PM-2026.12" is in force from 2026-12-01 with the two payment-matching areas unchanged
    When RW-CREDITAD calls GET /api/recovery/access/v1/me/session on 2026-12-01
    Then the answer holds the matrix version "PM-2026.12"
    And the entry written on 2026-11-30 keeps matrixVersion "PM-2026.11"
    And no deployment and no code change happened between the two reads
    When RW-SECADM reads GET /api/recovery/access/v1/admin/roles
    Then each of the four roles is returned with its area, its letters and its matrix version

  Scenario: AC6 The approver right is separate from the loader right (new, D-RCV-60)
    Given PAYMENT_MATCH version "PM-2027.01" is LOADED with valid from 2027-01-01
    When RW-COE, holding Rules and parameters "C" and not "A", calls the guarded approve of that version
    Then the call is refused with status 403 and MSG-P4-002 for the action "approve a rule version"
    And the version stays LOADED and no approval is recorded
    And one entry with decision code "AC-DENY", area "RULES_AND_PARAMETERS" and right "A" is written
    When RW-RISK, holding Rules and parameters "A", calls the same operation
    Then the call is allowed and the refusal is not repeated

  Scenario: AC7 A missing row is denied by default and the read fails closed (new, D-RCV-60)
    Given no permission row for RW-PHONECOL in the area "WRITE_OFF_AND_POSTING" at the matrix version in force
    When a caller holding only RW-PHONECOL reads the unmatched receipts of case "RC-2026-000555"
    Then the resolver answers DENY and the call is refused with status 403 and MSG-P4-002
    And one entry with decision code "AC-DENY", area "WRITE_OFF_AND_POSTING" and right "R" is written
    Given the decision-record library is forced to fail during the read of RW-CREDITAD
    When RW-CREDITAD reads the unmatched receipts of case "RC-2026-000555"
    Then the call answers 503 with MSG-P7-003 and returns no receipt
    And an incident is raised to the platform administrator queue
```

The seven criteria are new under D-RCV-60 and they test only the access profile, its answers and its entries. Every business value is the legacy story's: the four roles and their letters (legacy section 10), the case, the plan and the payment of 10,000.00 THB (legacy AC5) and the two package versions (legacy AC3 and AC6). The legacy criteria of RWB-E2-027 stay with the other slices of the key: the match with RWB-P8-E2027-APP, the registry with RWB-P7-E2027-APP, the workbook with RWB-P3-E2042-APP and the journey with RWB-ITG-E2027-ITG (GAP-2314; ASM-3837).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The right of a caller is the union of the letters of the roles the caller holds in the capability area of the operation, at the matrix version in force; a role not held contributes nothing | FSD P4 AC-ALT-P4-001-02; legacy section 10 |
| BR2 | No permission row for the role and the area is DENY, not ALLOW; the resolver never falls back to a default letter and never caches an allow across a matrix version | FSD P4 AC-EXC-P4-001-05; legacy section 17 |
| BR3 | The area and the right each matching operation needs are declared in one profile: receipt read and exception-list read WRITE_OFF_AND_POSTING R, package-version load RULES_AND_PARAMETERS C, rule-version approve RULES_AND_PARAMETERS A | legacy sections 10 and 12; LOV-CAPABILITY; ASM-3832 |
| BR4 | A call without the right stops with 403 and MSG-P4-002 before the operation runs, and nothing of the guarded operation is written | FSD P4 AC-EXC-P4-001-05; legacy section 14 and TC-E2-027-11, TC-E2-027-12 |
| BR5 | Every refusal writes one AC-DENY entry with the area, the right and the result, and every exception-list read writes one AC-READ entry with the case id, the filter and the row count; the entry is written before the answer | FSD P4 A2.6 and AC-P4-007-01; legacy BR8 |
| BR6 | An entry names no personal data: no name, no identity number, no phone number, no account key and no payment amount; the case id, the payment-free filter and the counts are the whole record | legacy section 17; NFR-040; FSD P4 AC-ALT-P4-005-01 |
| BR7 | The matrix version that decided a call is written on the entry and is never re-resolved afterwards; a later version changes the next call, not the record of an earlier one | FSD P4 AC-P4-004-01; legacy BR6 (earlier decisions keep their version) |
| BR8 | A read that cannot be recorded is not served, and a refusal that cannot be recorded is still a refusal: the call answers 503 and an incident is raised | legacy BR8 and section 5 X4; FSD P4 AC-EXC-P4-004-04 |
| BR9 | The letters are rows of the `permission` table and are never a constant of the code; a change of a letter is a matrix version, not a release | legacy BR10 pattern; FSD P4 BR-P4-004 |
| BR10 | The separation of duty of the rule package holds at the right: the loader holds C, the approver holds A, and no role holds both for this key | legacy section 10; TSD P4 T6.1 |

### 9. State transitions

None. This story changes no case status and no permission letter; it reads them. The two case transitions of the legacy story — `PLAN_RUNNING` on `PAYMENT_RECEIVED` under R-RES-26 and `PLAN_CURE_PERIOD` on `PAYMENT_RECEIVED_LATE` under R-RES-28 — are rwb-case's and rwb-payment's.

The only boundary this story owns is the matrix version a call is decided under:

| From | Event | Condition | To |
|---|---|---|---|
| (entry of a call) | The matrix version in force changes | A later read is made on or after the new valid-from date | The new entry carries the new version; the earlier entry keeps its version |
| (session answer) | The matrix version in force changes | The session is read on or after the new valid-from date | The session carries the new version and its letters |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration officer | Reads the matched and unmatched receipts and the exception list; every read is recorded (Write-off and posting CRUA) |
| RW-FINANCE, Finance and CFO delegate | Reads the matched receipts; every read is recorded (Write-off and posting RA) |
| RW-COE, center of excellence analyst | Loads a PAYMENT_MATCH package version; may not approve it (Rules and parameters C) |
| RW-RISK, risk and model risk officer | Approves a loaded package version; may not load it (Rules and parameters A) |
| RW-SECADM, security administrator | Reads the roles and the access entries, and owns the permission rows (Platform administration R; the matrix owner role of FSD P4 A2.4) |
| RW-CASEOWN and any role without the right of the call | Refused with 403 and MSG-P4-002 on every operation of the profile, with one AC-DENY entry |
| SY-AGENT, agent platform | Reads the exception list as the reconciliation agent under the same session check; its letters in WRITE_OFF_AND_POSTING are Not specified in the source documents (GAP-2311; ASM-3832) |
| The rwb-access service identity | Resolves the rights, writes the AC-DENY and AC-READ entries and answers the three reads of section 12.1 |
| SY-DECLOG, decision log writer | Supplies the hash-chained write of DP-03 for every entry |

Separation of duty: the analyst who loads a version does not approve it, and this story enforces the pair of rights that makes that true (BR10). No person is named anywhere; the actors are roles and service identities.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | role (P4, `rwb_access`) | id, role_code, role_name, role_class, default_scope, entra_group | Read for the session and roles answers |
| DF-REF-040 to DF-REF-044 | permission (P4, `rwb_access`) | id, role_id, capability_area, letters, matrix_version | Read; no row is written by this story |
| DF-DEC-001 to DF-DEC-031 | decision_log_entry (P4, `rwb_access`) | id, decision_code, actor_user_id, case_id, actions, outcome, decided_at, matrix version in inputs, chain_seq, prev_hash, entry_hash, idempotency_key | Write one row per refusal and per exception-list read (DP-03); read through the access log |
| DF-ACE-043 to DF-ACE-046 | v_ace_payment | payment_code, account_key, payment_date, payment_amount | Not read here: the receipts reach this story only as the item the rwb-payment contract mock returns |
| DF-FIN-002, DF-FIN-004, DF-FIN-006, DF-FIN-008 | proceeds (P8) | case_id, payment_code, amount, matched_to | Not read and not written here: `proceeds` is rwb-payment's |
| DF-TRT-001, DF-TRT-031, DF-TRT-033 | treatment (S2) | id, installment_amount, installment_shortfall | Not read here: the plan is rwb-treatment's |

`role`, `permission` and `decision_log_entry` are rwb-access's and no other service reads them (DP-01). The field IDs are those of TSD P4 T3.1 and of the Logical Data Model and Data Dictionary v8. This story adds no table and no column: it reads the two matrix tables and writes entries into the log table of RWB-P4-E1039-APP. `delegation_limit`, `masking_rule` and `role_conflict` are P4's but are not used by this key: a match is not an approval, the receipt carries no personal field and no role pair is refused by the profile.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`. The three paths are the ownership map's P4 operations, and API-P4-012, API-P4-007 and API-P4-008 of TSD P4 T-A.1 on the service base. The payment-matching profile is not a new endpoint: it is the pair (area, right) that the session answer and the entries carry.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/me/session` | The caller's resolved session: roles, the permission rows with their letters, the matrix version, the scope, the masking version and the break-glass state; 200 | None R, scope applied | Not applicable, read only |
| GET | `/admin/roles` | List the roles with their permission rows, the areas, the letters, the scope and the matrix version; 200 | Platform administration R, scope applied | Not applicable, read only |
| GET | `/admin/access-log` | Search the entries of `rwb_access`: query `user`, `from`, `to`, `event`, `capabilityArea`, `page`, `size`; AccessLogPage with `at`, `user`, `event` (AC-READ or AC-DENY), `capability`, `right`, `result`, `caseId`, `rowCount`, `matrixVersion`; 200 | Platform administration R, scope applied | Not applicable, read only |

The session answer holds `roles[]` with `roleCode`, `scope` and `permissions[]` of `capabilityArea` and `letters`, plus `matrixVersion`, `maskingVersion` and the break-glass state. Errors: 401 no session (MSG-P4-001 where the caller holds no role); 403 the role lacks the right of the admin read (MSG-P4-002); 503 the entry of the read could not be written (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set. The refused load and approve calls are not published here: they are the operations of RWB-P7-E2027-APP, stopped at their edge by the guard that reads this answer (GAP-2313; ASM-3834).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, on RWB-P3-E1043-CON | LOV-CAPABILITY with `WRITE_OFF_AND_POSTING` and `RULES_AND_PARAMETERS`, LOV-ROLE and LOV-SCOPE with the version in force, so the areas and the roles of the profile are reference data and never constants (DP-07); faked, one hop, 2 s (DP-11) |

Only one operation is consumed: the matrix tables hold the letters, so no parameter is read by this story and DP-06 adds no call (GAP-2312; ASM-3833). The rwb-payment read is not consumed: this story answers the guard that sits in front of it, and the mock of 12.8 supplies the item shape the guard protects. The platform and published contracts the DP table adds are listed in section 13 and carried in the gap of GAP-2312.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library, published by this service | entryId | the hash-chained record of a refusal or an exception-list read: decision code, the area, the right, the result, the case id, the row count, the matrix version, the actor and the decided time |

One event type, on the shared ledger topic and not on `rwb.access.events.v1`: an access entry is a decision record, not a change of access policy, and the two policy events of the service belong to RWB-P4-E1037-APP and the delegation story (ASM-3835). The row is written to the outbox in the transaction of the entry and relayed with the CloudEvents 1.0 envelope; no event carries a name, an identity number, a phone number, an account key or an amount.

#### 12.4 Events consumed

None. The two reads of the matrix are synchronous, the session and the roles answers are computed from `rwb_access`, and no subscription is needed for a right. The matching run of JOB-07 is rwb-payment's and reaches this story only as a guarded caller.

#### 12.5 Workflows and activities

None. The three operations are synchronous reads; the resolver and the two recorders run in the request; and this story starts no workflow, registers no activity and adds nothing to the `rwb-access` task queue. The matching run of the legacy story is JOB-07 of rwb-payment and is not a workflow of this story. The six-monthly access review (JOB-18) is a Schedule of rwb-access but belongs to RWB-P4-AD008-APP; this story registers none.

#### 12.6 Schedules

None. JOB-18, the six-monthly access review, runs on the `rwb-access` queue as a Temporal Schedule of RWB-P4-AD008-APP (DP-10); this story creates no Schedule, no timer and no trigger, and the matrix version reaches the service as data and not by a job.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The four role rows of the legacy story and their class and default scope, read for the session and the roles answer |
| `permission` | P4 (`rwb_access`) | The letters of a role in a capability area at a matrix version; the only source of an ALLOW |
| `decision_log_entry` | P4 (`rwb_access`) | One append-only, hash-chained entry per refusal and per exception-list read |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects the DP-03 library uses |

Not owned and not read: `proceeds` (P8), `treatment` (S2) and `v_ace_payment` (P1); `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` (P7); `lov_value`, `parameter_value` (P3). `delegation_limit`, `masking_rule` and `role_conflict` are P4's and are unused by this key. No foreign key crosses a schema and no other service reads these three tables (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-payment contract fake | RWB-P8-E2027-CON | The matched receipts of case "RC-2026-000555" for a caller holding Write-off and posting R, and the exception list of 2026-12-14 with 1 unmatched payment "PAY-91006" of 10,000.00 THB; the mock is never reached from a refused call |
| rwb-case reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY with the two areas, LOV-ROLE with the four roles and the refusal roles, and LOV-SCOPE, each with its version |
| decision-record library fake | RWB-PLT-E1027-CON | The append and the hash chain, the `DecisionRecorded` outbox row, and a forced failure for AC7 and MSG-P7-003 |
| gateway-bff route fake | RWB-PLT-N001-CON | The SCR-28 proceeds-matching route and the session fragment it serves, so the read of AC4 is exercised through one hop |

Each fake is replaced by the real contract or the real library as its story lands, without a change to the scenarios. The fakes carry the legacy role codes, matrix versions, payment codes and the synthetic case only.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 1 | The session, the roles list and the access log provided; the reference list consumed, one hop and 2 s |
| Kafka | Published 1 event type, consumed 0 | `rwb.decision-record.v1` with `DecisionRecorded`; no event on `rwb.access.events.v1` from this key |
| Temporal | None | No workflow, activity or Schedule; the matching run is JOB-07 of rwb-payment |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `accessrights/profile`, Java package `th.co.scb.ace.workbench.recovery.access.accessrights.profile`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

How this story applies the rows that carry work. **DP-01, DP-13**: the three tables and every path sit in `rwb_access` and under `/api/recovery/access/v1`; no service reads them and no monolith base appears. **DP-03**: a refusal and an exception-list read each write one local entry in the transaction and publish `DecisionRecorded` on `rwb.decision-record.v1`; an entry that cannot be written stops the read (BR8). **DP-07, DP-11**: the one consumed call reads LOV-CAPABILITY, LOV-ROLE and LOV-SCOPE once, one hop, 2 s, so the areas and the role codes are reference data; the receipt item arrives from the rwb-payment fake. **DP-15, DP-19**: no new table and no migration, and SCR-28 stays a gateway-bff composite route for which this story supplies the session fragment and the logged read. Rows that add no work: **DP-04** (nothing is evaluated — the profile holds the right that gates a load, not a rule, so no C dependency is taken), **DP-05** (no ACE view), **DP-06** (no parameter — the letters are matrix rows), **DP-10** (no job; JOB-18 is AD008's, JOB-07 is rwb-payment's), **DP-14** (no event on `rwb.access.events.v1`; the entry uses the shared ledger topic).

The platform H dependencies of the table — H RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON — and the C dependencies C RWB-P3-E1043-CON are the DP-added dependencies that are **not** in the metadata rows, which name None and RWB-P8-E2027-CON. They are recorded in GAP-2312 and ASM-3833: they are platform contracts of wave 0 and the reference-data contract of rwb-case, none blocks the build, and an APP story builds against the published set and its fake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PaymentMatchAccessProfile | Service | Declares the area and the right each matching operation needs: receipt read and exception-list read WRITE_OFF_AND_POSTING R, package-version load RULES_AND_PARAMETERS C, rule-version approve RULES_AND_PARAMETERS A |
| RightResolver | Service | Answers ALLOW or DENY from the `permission` rows of the caller's roles at the matrix version in force; a missing row is DENY and no allow is cached across a version |
| SessionAssembler | Service | Builds the session and roles answers: roles, areas, letters, scope and matrix version |
| RefusalRecorder | Service | Writes the AC-DENY entry with the area, the right and the result, and no payment, account or amount |
| ReadRecorder | Service | Writes the AC-READ entry of an exception-list read with the case id, the filter, the row count and the matrix version, and fails the read closed |
| AccessEntryRepository | Repository | Reads and writes the entries and the matrix rows of `rwb_access` only |

**Build steps**

1. Write `PaymentMatchAccessProfile` with the four operations of BR3 and unit test the pair it returns for each.
2. Build `RightResolver` over `permission`; test the union of two roles, the missing row and the version boundary of AC5.
3. Extend `SessionAssembler` so the session and the roles answers carry the letters and the matrix version; test AC1.
4. Build `RefusalRecorder` and put it before the 403 of the guarded call; test AC2, AC3 and AC6.
5. Build `ReadRecorder` for the exception-list read and assert the entry carries no personal field; test AC4 and the fail-closed half of AC7.
6. Test the deny-by-default half of AC7 with a role that has no row in the area.

**Feature flag.** `rwb.access.payment-match.profile`. Off: the four matching operations answer DENY for every caller, so a switch-off closes the path rather than opening it; the two admin reads stay on.

**Done when.** The tests in section 16 pass; the four roles answer their legacy letters on the session; a refused read, load and approve each write one AC-DENY entry with its area and right; every exception-list read writes one AC-READ entry with the case id, the row count and the matrix version, and holds no personal data; and a read that cannot be recorded returns nothing.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller's roles do not carry the right of the operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | The caller holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P7-003 | The entry of the read or of the refusal could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | A matrix or entry row changed under the call | Someone else changed this record. Reload it to see their change. |

`{action}` is the operation of the guarded call — "read proceeds", "read the exception list", "load a rule version", "approve a rule version" — and never a payment, a case or a person. Thai text follows DL10.

### 15. Screens and states

SCR-28 Proceeds matching (states Loading; matched; unmatched) shows, for each matched receipt, the rule and the package version from its decision entry, and for each unmatched receipt the reason; the read behind it is the logged read of AC4, and the refused read of AC2 shows the MSG-P4-002 problem and nothing else. SCR-43 Roles and access shows the four roles with their areas, letters and matrix version, read-only, from `GET /admin/roles` (AC5). Both screens are built by RWB-PLT-N001-APP and RWB-P8-E2027-APP; this story supplies the session fragment and the logged read behind them (ASM-3839). The session line names the caller's role and scope and is served on every screen; the access log of SCR-44 lists the AC-READ and AC-DENY entries of a user and a period.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-027-01 | AC1, BR2, BR6 — matched under the RW-CREDITAD rights of AC1 | Component | PAY-91001 12,500.00; PAYMENT_MATCH version PM-2026.12 |
| TC-E2-027-02 | AC2, BR4 — the partial match read under the same rights | Component | PAY-91002 11,875.00 |
| TC-E2-027-03 | AC3, BR6 — the rule change read under the session of the business date | Component | PM-2027.01 from 2027-01-01; PAY-91003 4 days late |
| TC-E2-027-04 | AC4, BR3, BR5 — both receipts read as the exception list records them | Component | PAY-91004 3 days late, PAY-91005 4 days late |
| TC-E2-027-05 | AC5, BR4, BR5 — the 10,000.00 unmatched item of AC1 and AC4 | Component | PAY-91006 10,000.00 |
| TC-E2-027-06 | AC6, BR7 — the load refused at the guard edge before any version check | Component | PM-2027.02 with duplicate row order and tolerance 120 |
| TC-E2-027-07 | AC7, BR8 — the refusal that cannot be recorded still refuses | Component | Decision log stubbed unavailable |
| TC-E2-027-08 | AC8, BR2 — the overpayment read under the same rights | Component | PAY-91007 13,000.00 |
| TC-E2-027-09 | AC9, BR1 — one read, one AC-READ entry | Component | PAY-91008 matched by two rows |
| TC-E2-027-10 | AC10, BR9 — the refused read when no receipt is in force on the date | Component | No PAYMENT_MATCH version in force on 2027-02-01 |
| TC-E2-027-11 | AC2, Access | Component | RW-CASEOWN calls the proceeds read; refused with MSG-P4-002 |
| TC-E2-027-12 | AC3, Access | Component | RW-CASEOWN calls the package-version load; refused with MSG-P4-002 |
| TC-E2-027-13 | AC7, Principle 5 | NFR | Decision log write forced to fail for 50 reads; no receipt returned |

The thirteen legacy test cases of RWB-E2-027 keep their IDs. This story runs them under the access profile — the rights of AC1, the refusals of AC2, AC3 and AC6 and the fail-closed read of AC7 — while the match-level assertion of TC-01 to TC-10 and the proceeds write of TC-13 are run by RWB-P8-E2027-APP. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases under the same test case ID.

### 17. Guardrails

- No business value in code: the areas, the letters and the matrix version are rows and reference data; the profile holds only the pair (area, right) each operation needs.
- No personal data in an entry, a log, an event or a payload: the case id, the filter, the row count and the matrix version are the whole record, never a name, an identity number, a phone number, an account key or an amount.
- ACE data only through the owner's contract or the `v_ace_*` views: the receipts come through RWB-P8-E2027-CON and the plan through nothing.
- Deny by default and fail closed: a missing row is DENY, and a read that cannot be recorded is not served.
- The entry is written before the answer; no refusal and no exception-list read exists without its entry.
- One resolver: every matching operation asks `RightResolver`, and no handler tests a role code itself.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list — the authority side: who reads the list and who changes the rule | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01; FEAT-ACA-04 and FEAT-ACA-07 for the rights and the log | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39, R-UNI-41 | TC-E2-027-01 to TC-E2-027-13 |

The criteria are new under D-RCV-60 and trace to the legacy key through its authority section and its two access test cases; the REQ-CHO-009 row is the legacy row of section 18, unchanged.

### 19. Out of scope

- The match, the fired row, the proceeds row, the exception list and the posting of a receipt (RWB-P8-E2027-APP).
- The PAYMENT_MATCH package, its versions, the parsed rows, the approval and the rollback (RWB-P7-E2027-APP).
- The workbook, its Rows and Tests tabs and the authoring pipeline (RWB-P3-E2042-APP, RWB-P3-E1073-APP).
- The installment shortfall passed to the plan on a partial match (S2).
- Break-glass access, the delegation of authority table and masking: none is used by a match, and each belongs to its own P4 story.
- The build of SCR-28 and SCR-43 and the composite routes behind them (RWB-PLT-N001-APP), and the access review of JOB-18 (RWB-P4-AD008-APP).
