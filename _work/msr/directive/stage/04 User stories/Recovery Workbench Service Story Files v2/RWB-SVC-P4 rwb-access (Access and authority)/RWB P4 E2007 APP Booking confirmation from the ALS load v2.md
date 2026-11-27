# RWB-P4-E2007-APP Booking confirmation from the ALS load

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P4-AG |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E2007-APP-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2007-CON |
| Contract published | None. This APP story provides no contract; its operations are served through RWB-P4-E1037-CON (section 12.1). |
| Contract fake library version published | Not specified in the source documents (DOR-RWB-P4-E2007-APP-22) |
| Contract version built against | Not specified in the source documents (DOR-RWB-P4-E2007-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CHO-008) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-007 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 35 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT), a Credit Administration officer (RW-CREDITAD) and a platform administrator (RW-PLATADM)**, I want **the access decision for the booking-confirmation capability — the read of the booked terms on SCR-14 Treatment record and the completion of the booking and terms tasks that the match raises — returned by the authorise contract of rwb-access, refused with one message for a role that does not hold the right, and recorded as one access entry naming the IDs and the field IDs only**, so that **every look at the booked terms and every completion of a booking task is allowed for the role that holds the right and refused for the role that does not, with the access recorded once and no personal data in the record**.

### 2. Business rationale

The officer books restructures and settlements by hand in ALS (INT-03) and the case, the treatment and the tasks then carry the booked terms. Nothing governs who may look at those terms or who may complete the booking task: the legacy story names the roles in its authority table and records one refusal (RW-CASEOWN reruns JOB-08, MSG-P4-002) in its exception path X8 and in TC-E2-007-10, and the role model itself is data in rwb-access. rwb-access owns Recovery roles as data, scope, the masking policy, the DoA table and the access log (Architecture v5 slide 41), and every other service asks it before a read or an action (slide 14: `POST /authorise`, cached), so the decision has to be served here, once, for every screen and every agent that shows the booked terms.

This story is the rwb-access part of legacy RWB-E2-007. The match, JOB-08 and the ALS read are the rwb-integration part of the same legacy key (RWB-P2-E2007-APP and its contract RWB-P2-E2007-CON), the case move and the tasks are rwb-case (RWB-P3-E2007-APP), the treatment record and its APPROVED to BOOKED state are rwb-treatment (RWB-S2-E2007-APP), and the ACE view read is rwb-source-data (RWB-P1-E2007-APP). This slice delivers the authorise decisions and the access entries for that capability — not the case move, not the match, and no new REST path. It meets REQ-CHO-008, keeps R-UNI-39 (a decision that cannot be recorded does not proceed) and gives NFR-042 (every read logged) its entry for this capability.

The policy pack this slice answers from is the booking-confirmation slice of the matrix version in force: TREATMENT_AND_OFFER R for RW-RESTRUCT and RW-CREDITAD, CASE_RECORD R and U for RW-RESTRUCT and RW-CREDITAD, PLATFORM_ADMINISTRATION U for RW-PLATADM, no PLATFORM_ADMINISTRATION row for RW-CASEOWN, and RW-AUDIT reading with scope ALL. The pack is loaded as data by RWB-P4-AD002-APP and the matrix as a whole by RWB-P4-E1037-APP; this story reads it and applies it, and holds no role, area or letter in code.

### 3. Preconditions

- RWB-P4-E1037-CON is published: the authorise contract of rwb-access with the request and answer shapes, the error envelope and the masking read (DP-08; this story serves the read side of that contract for the booking-confirmation capability).
- RWB-P2-E2007-CON is published: the rwb-integration contract of this legacy key, with the TreatmentBooked envelope for treatment `TRT-SYN-0701` on case `RW-2026-000701` and business date `2026-12-16`, the booking-match result naming the task codes `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` and `UNMATCHED_EXCEPTION`, and its fixtures (DP-11). The exact authorise request and answer shapes are Not specified in the source documents (GAP-0922; ASM-1644).
- RWB-P4-E1001-APP creates the `rwb_access` authority tables (`role`, `permission`, `masking_rule`, `role_conflict`, `delegation_limit`); this story applies that baseline, and the local decision-record table exists before this story adds its rows and its own migration. RWB-P4-E1037-CON creates no table.
- The policy pack version `PM-2026.12` is in force in `permission` with TREATMENT_AND_OFFER R for `RW-RESTRUCT` and `RW-CREDITAD`, CASE_RECORD R and U for `RW-RESTRUCT` and `RW-CREDITAD`, PLATFORM_ADMINISTRATION U for `RW-PLATADM`, no PLATFORM_ADMINISTRATION row for `RW-CASEOWN`, and scope ALL for `RW-AUDIT` (DF-REF-042, DF-REF-043, DF-REF-044). The TSD RBAC matrix has no Case record column, so the CASE_RECORD letters are read from the pack and confirmed with the matrix owner (GAP-0923; ASM-1646).
- No `masking_rule` row is needed for this capability: the screens show case IDs, treatment IDs, amounts and dates only, and no personal field is read or shown on SCR-14 or SCR-01 by this capability (FSD P4 A2.5, A2.7).
- The caller sends the case attributes the scope test needs — the case ID, its owner, its queue and its team — inside the authorise request; rwb-access reads no `rwb_case` table, calls no rwb-case operation and reads no `v_ace_*` view (DP-01, DP-05). The attribute set and its field names are Not specified in the source documents (GAP-0922; ASM-1644).
- The decision-record library and the shared topic `rwb.decision-record.v1` are live (DP-03), and the outbox and inbox library is live in `rwb_access` (DP-09).
- The parameters contract of rwb-case and its client library are live for the decision-cache lifetime (DP-06); the value of that lifetime is Not specified in the source documents (GAP-0924; ASM-1647).
- The reference-data contract of rwb-case is live for LOV-CAPABILITY and LOV-SCOPE (DP-07).
- The login is the rwb-access login (DP-02). The per-service login name is Not specified in the source documents (GAP-0922; ASM-1645).

### 4. Flow

1. rwb-case, rwb-treatment or gateway-bff holds an action for this capability: a read of the booked terms on SCR-14 Treatment record, or a completion of `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` or `UNMATCHED_EXCEPTION` on SCR-01 My work.
2. The caller sends `POST /api/recovery/access/v1/authorise` with the caller identity from the session, the capability area, the right, the case and treatment reference, and the field IDs the screen will show.
3. rwb-access: the request is served from the decision cache when the same identity, area, right, case reference and field list is already held under the matrix version in force; otherwise it is decided.
4. rwb-access: the role set is read from `role` and `permission` at the matrix version in force (`PM-2026.12`), and the letters for the area are unioned across the roles the caller holds; no letter is written in code.
5. rwb-access: when the area and right are covered, the scope test runs — OWN compares the case owner with the caller, TEAM the case queue's team, REGION the team's region, ALL no test — on the facts read once from rwb-case.
6. rwb-access: a case that does not exist, or that sits outside the caller's scope, is answered as not found with MSG-P4-003 and no case data; an area with no letter, or no permission row at all, is refused with MSG-P4-002 (default deny).
7. rwb-access: the masking answer is read from `masking_rule` at the masking version in force for the field IDs the caller names; this capability names `DF-TRT-012` (`booked_at`) and `DF-TRT-028` (`booking_difference`) on the SCR-14 read, and neither is a personal field, so no masking row applies.
8. rwb-access: the access entry is written first, in the same transaction as the answer: decision code `AC-READ` or `AC-DENY` (FSD P4 A2.7), the actor, the case ID when the decision is on a case, the area, the right, the field IDs and the time; the `case_id` is empty only for an access event with no case (DF-DEC-002).
9. rwb-access: the local decision record is written through the decision-record library with its hash link and its outbox row; if that write fails the answer is 503 MSG-P7-003 and no case data is returned (R-UNI-39, AC in section 7 on the record path).
10. rwb-access: the outbox relay publishes `DecisionRecorded` on `rwb.decision-record.v1` for the central ledger in rwb-decision, and `AccessPolicyChanged` on `rwb.access.events.v1` when the pack version this service serves changes.
11. rwb-access: the caller receives the decision with the decision code, the matrix version, the masking answer and the scope result, and the screen shows the booked terms or completes the task.
12. When the pack version moves, the cached decision for the capability is dropped and the next call is decided on the new version, with no restart (section 7, AC7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The area holds no letter, or the role has no permission row at all | Default deny: the action is refused and nothing changes | MSG-P4-002 | AC6 |
| X2 | The case does not exist, or sits outside the caller's scope | Not found, with no case data in the answer or the entry | MSG-P4-003 | AC5 |
| X3 | RW-CASEOWN asks for PLATFORM_ADMINISTRATION U (rerun JOB-08) | Refused before the handler runs; no job starts; one entry with area PLATFORM_ADMINISTRATION, right U and result REFUSED | MSG-P4-002 | AC4 |
| X4 | The decision record cannot be written on a read | The answer is 503 and no case data is returned; an incident is raised; nothing is shown | MSG-P7-003 | AC8, TC-E2-007-11 |
| X5 | rwb-case does not answer the scope read inside the REST budget | One hop, 2 s (DP-11); the decision is not taken from a partial answer and the caller retries; no entry with a guessed scope | MSG-P4-003 | AC5 |
| X6 | The pack has no row for the area on the business date | Default deny, not a default allow; the gap is alerted to RW-PLATADM | MSG-P4-002 | AC6 |
| X7 | A cached decision outlives a pack change | The version is compared on every served decision; the entry cached under the old version is dropped on the change, with no restart | None | AC7 |
| X8 | A request names no field IDs | The entry records no field IDs; the decision itself is unchanged | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the rwb_access baseline, RWB-P4-E1037-CON and the RWB-P2-E2007-CON fixture. The rwb-case scope read, the parameters and reference-data contracts and the central ledger are contract fakes |
| Negotiable | Roles, areas, letters, scope values and the cache lifetime are data rows and parameters; the story fixes the decision path and names no role or letter in code |
| Valuable | Every read of the booked terms and every completion of a booking task is decided once, refused with one message where the right is absent, and recorded once |
| Estimable | One decision endpoint, one masking read, two versioned reads, one access-entry write and one cache |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test with a fixture; every cross-service answer is stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Booking confirmation from the ALS load — access decisions and access entries

  Background:
    Given the policy pack version "PM-2026.12" is in force with TREATMENT_AND_OFFER R and CASE_RECORD R and U for "RW-RESTRUCT" and "RW-CREDITAD", PLATFORM_ADMINISTRATION U for "RW-PLATADM", no PLATFORM_ADMINISTRATION row for "RW-CASEOWN" and scope ALL for "RW-AUDIT"
    Given the rwb-integration contract mock returns TreatmentBooked for treatment "TRT-SYN-0701" on case "RW-2026-000701" with business date 2026-12-16 and a booking-match result naming task codes "WITH_OPS_BOOKING", "WITH_OPS_SETTLEMENT" and "UNMATCHED_EXCEPTION"

  Scenario: AC1 Booked terms read allowed for the restructuring officer (new, D-RCV-60)
    Given the caller holds role "RW-RESTRUCT" with scope "OWN" and owns case "RW-2026-000701"
    When the caller asks POST /api/recovery/access/v1/authorise for capability area "TREATMENT_AND_OFFER", right "R", case "RW-2026-000701" and field IDs "DF-TRT-012" and "DF-TRT-028"
    Then the answer grants the read with decision code "AC-READ" and matrix version "PM-2026.12"
    And no masking row covers "DF-TRT-012" or "DF-TRT-028", because neither is a personal field
    And one access entry is written with decision code "AC-READ", the actor, case "RW-2026-000701", area "TREATMENT_AND_OFFER", right "R", field IDs "DF-TRT-012" and "DF-TRT-028", and decided at
    And the entry carries no amount, no account number, no name and no identity number

  Scenario: AC2 Credit Administration officer completes the terms task (new, D-RCV-60)
    Given the rwb-integration contract mock returns a booking-match result with task code "UNMATCHED_EXCEPTION" for case "RW-2026-000701"
    Given the caller holds role "RW-CREDITAD" with scope "TEAM" and case "RW-2026-000701" sits on a queue of the caller's team
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "U", case "RW-2026-000701" and no field IDs
    Then the answer grants the update and names matrix version "PM-2026.12"
    And the task "UNMATCHED_EXCEPTION" is completed on SCR-01 My work through rwb-case
    And the read of SCR-01 My work that precedes the completion is recorded once with decision code "AC-READ", area "CASE_RECORD" and the case ID, and no field IDs; the update itself is not an access event

  Scenario: AC3 Restructuring officer completes the booking tasks (new, D-RCV-60)
    Given the rwb-integration contract mock returns a booking-match result with task codes "WITH_OPS_BOOKING" and "WITH_OPS_SETTLEMENT" for case "RW-2026-000702"
    Given the caller holds role "RW-RESTRUCT" with scope "OWN" and owns case "RW-2026-000702"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "U", case "RW-2026-000702"
    Then the answer grants the update and names matrix version "PM-2026.12"
    And both task codes are completed through rwb-case and the treatment stays "APPROVED"
    And the read of SCR-01 My work that precedes each completion is recorded once with decision code "AC-READ", area "CASE_RECORD" and the case ID; the update itself is not an access event

  Scenario: AC4 Case owner refused the job rerun (new, D-RCV-60)
    Given the caller holds only role "RW-CASEOWN" and the pack holds no PLATFORM_ADMINISTRATION row for it
    When the caller asks POST /api/recovery/access/v1/authorise for area "PLATFORM_ADMINISTRATION", right "U" and the booking-confirmation job
    Then the call is refused with status 403 and message MSG-P4-002 for action "rerun the booking-confirmation job"
    And the case owner, the treatment and the tasks are unchanged and no job starts
    And one entry is written with decision code "AC-DENY", area "PLATFORM_ADMINISTRATION", right "U" and result "REFUSED"

  Scenario: AC5 Case outside the reader's scope (new, D-RCV-60)
    Given the caller holds role "RW-RESTRUCT" with scope "OWN" and does not own case "RW-2026-000999"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000999"
    Then the answer is status 404 with message MSG-P4-003 and carries no case data, no treatment ID and no booked terms
    And one entry is written with decision code "AC-DENY", area "CASE_RECORD", right "R" and the case ID
    And no booked amount and no account key is written on the entry

  Scenario: AC6 Deny by default with no permission row (new, D-RCV-60)
    Given the caller holds a role with no row in "PM-2026.12" for area "TREATMENT_AND_OFFER"
    When the caller asks POST /api/recovery/access/v1/authorise for area "TREATMENT_AND_OFFER" and right "R"
    Then the call is refused with status 403 and message MSG-P4-002
    And nothing is allowed and no screen data is returned
    And one entry is written with decision code "AC-DENY", area "TREATMENT_AND_OFFER" and right "R"

  Scenario: AC7 Cached decision refreshed on a policy change (new, D-RCV-60)
    Given "RW-CREDITAD" is refused CASE_RECORD U under "PM-2026.12" and the answer is cached
    When the pack in force moves to "PM-2026.13" with CASE_RECORD U for "RW-CREDITAD" and "AccessPolicyChanged" is published on "rwb.access.events.v1"
    Then the next POST /api/recovery/access/v1/authorise for CASE_RECORD U grants the update with decision code "AC-READ" and matrix version "PM-2026.13"
    And the service is not restarted and no answer cached under "PM-2026.12" is returned after the change

  Scenario: AC8 Access entry carries IDs and field IDs only (new, D-RCV-60)
    Given the caller holds role "RW-AUDIT" with scope "ALL" and reads case "RW-2026-000701"
    When the read of the booked terms and the difference is decided
    Then one entry is written with decision code "AC-READ", the actor, the case ID, area "TREATMENT_AND_OFFER", right "R" and field IDs "DF-TRT-012" and "DF-TRT-028"
    And the entry holds no amount, no name, no address, no identity number and no account number, only the IDs and the field IDs
    And the entry is appended through the decision-record library and relayed on "rwb.decision-record.v1", with no new Kafka event for the access log

  Scenario: AC9 Scope test and default-deny inputs read from the request and the pack only (new, D-RCV-60)
    Given the caller holds role "RW-RESTRUCT" with scope "OWN"
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000701" without the owner attribute
    Then the call is not allowed and no case data is returned
    And the scope test compares the case owner, queue team and region carried in the request against the default scope of "RW-RESTRUCT"
    And no role code, area, letter or scope value is written in code; each is read from the pack in force
    And the answer carries no masking row and no personal field
    And no DoA row is read by this call

  Scenario: AC10 Call without a valid credential answered 401 (new, D-RCV-60)
    Given the caller presents no valid credential
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R" and case "RW-2026-000701"
    Then the answer is status 401 and carries no case data
    And the message is Not specified in the source documents (NEWAC-RWB-P4-E2007-APP-AC11)

  Scenario: AC11 Replay of a write with the same idempotency key (new, D-RCV-60)
    Given the caller holds role "RW-CREDITAD" with scope "TEAM" and case "RW-2026-000701" sits on a queue of the caller's team
    When the caller completes the task "UNMATCHED_EXCEPTION" on case "RW-2026-000701" and the same request is sent again with the same idempotency key
    Then the second call returns the same answer as the first call and the task is completed once
    And no second access entry is written for the replayed update
```

The eight criteria above are new and test only this deliverable: the authorise decision, the masking read and the access entry for the booking-confirmation capability. The legacy criteria of RWB-E2-007 are owned elsewhere: AC1 to AC9 of the legacy story are carried by rwb-integration (RWB-P2-E2007-APP), rwb-case (RWB-P3-E2007-APP), rwb-treatment (RWB-S2-E2007-APP) and rwb-source-data (RWB-P1-E2007-APP); the legacy exception X8 (a role without the right reruns JOB-08, MSG-P4-002) and legacy test case TC-E2-007-10 are answered here, by AC4 and AC6.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The access decision is served only by rwb-access, on the authorise contract, from the matrix version in force; every other service and every agent asks it before a read or an action (DP-08) | Architecture v5 slides 14 and 41; DP-08 |
| BR2 | Roles, capability areas, letters, scope and the masking rows are data with their version; no role code, area, letter or scope value is written in code | FSD P4 A2.3, A2.4; BR-P4-004; TSD P4 T3.2 |
| BR3 | A capability area with no letter, and a role with no permission row, are refused (default deny), never allowed by default | FSD P4 A2.4; VR-P4-004-1 |
| BR4 | A case outside the caller's scope is answered as not found with MSG-P4-003 and returns no case data | FSD P4 A2.4 AC-EXC-P4-004-01 |
| BR5 | The scope test compares case owner, queue team and region against the role's default scope, or applies no test for ALL | FSD P4 A2.14; TSD P4 T3.2 (LOV-SCOPE) |
| BR6 | Every decision, allowed or refused, writes one access entry with decision code `AC-READ` or `AC-DENY`, the actor, the case ID when the decision is on a case, the area, the right, the field IDs and the time | FSD P4 A2.7 |
| BR7 | The access entry is a decision-record entry written through the local decision-record library and relayed on `rwb.decision-record.v1`; it is never a new Kafka event or a new topic (DP-03) | FSD P4 A2.8; Architecture v5 slide 14 (P4 events: none but the two policy events); DP-03 |
| BR8 | A read that cannot be recorded returns nothing: 503 MSG-P7-003 and no case data | FSD P4 A2.7 AC-EXC-P4-007-03; R-UNI-39 |
| BR9 | No masking row is needed for this capability: the screens show case IDs, treatment IDs, amounts and dates only, and the entry carries no personal field | FSD P4 A2.5; TSD P4 T3.1 (masking_rule) |
| BR10 | The masking answer for a named field ID is read from the masking version in force; a personal field with no masking rule is masked | FSD P4 AC-EXC-P4-004-05 |
| BR11 | The decision is cached only under the matrix version it was decided on; a change of version drops the entry and the next call is decided on the new version, with no restart | Architecture v5 slide 14 (authorise cached); DP-11 |
| BR12 | The scope test reads only the attributes carried in the request; a missing attribute never decides an allow | DP-11; Architecture v5 slide 20; FSD P4 A2.14 |
| BR13 | `AC-DENY` for a case the caller may not see still names the case ID, and `case_id` is empty only for an access event with no case | DF-DEC-002; FSD P4 A2.7 AC-EXC-P4-007-04 |
| BR14 | The DoA rows are not read by this slice; the approval router reads them through RWB-P4-E2013-APP, and this story changes no limit | Architecture v5 slide 14; TSD P4 T3.1 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| permission row in force at `PM-2026.12` | AccessPolicyChanged | A new matrix version is loaded, approved and in force | permission row in force at the new version; the cached decision under the old version is dropped |
| no letter for the area, or no permission row | an authorise request | The area and right are asked for | refused, decision code `AC-DENY`, and an entry written |
| cached decision under the version in force | an authorise request | The same identity, area, right, case reference and field list | the cached decision, served with the version it was decided on |

rwb-access holds no case state machine of its own (TSD P4 T4): the case route state, the treatment state and the task status move in rwb-case and rwb-treatment, and this story neither reads nor writes them. A policy version moves from LOADED to APPROVED to IN_FORCE to SUPERSEDED or ROLLED_BACK in the load stories (TSD P4 T3.2 LOV-VERSION-STATUS); this story only reads the version in force and answers from it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the rwb-access login, DP-02) | Serves the decision, reads the matrix and the masking rows, writes the access entry and the outbox row |
| Decision-record library identity | Writes the local access entry with its hash link and relays it on `rwb.decision-record.v1` (Decision log C, DP-03) |
| RW-RESTRUCT, restructuring officer | TREATMENT_AND_OFFER R and CASE_RECORD R and U: reads the booked terms on SCR-14 and completes `WITH_OPS_BOOKING` and `WITH_OPS_SETTLEMENT` on SCR-01 |
| RW-CREDITAD, Credit Administration officer | TREATMENT_AND_OFFER R and CASE_RECORD R and U: reads the booked terms and the difference, and completes `UNMATCHED_EXCEPTION` |
| RW-PLATADM, platform administrator | PLATFORM_ADMINISTRATION U: allowed the rerun of the booking-confirmation job; the rerun itself is rwb-integration's operation |
| RW-CASEOWN, case owner | No PLATFORM_ADMINISTRATION row: the rerun is refused with MSG-P4-002 |
| RW-AUDIT, internal audit | Reads with scope ALL, including the access entries of this capability through the access-log search of RWB-P4-E1039-APP |

The per-service login name is Not specified in the source documents (GAP-0922; ASM-1645); the story names it "the rwb-access login (DP-02)" until the platform DB story fixes it. The roles, areas and letters above are rows of the pack and are not fixed in code; no role in this story may grant itself a letter.

### 11. Data

| BR Field ID | Entity in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-038 | role | role_code, role_name, role_class, default_scope | Read |
| DF-REF-035 | role | role_code | Read |
| DF-REF-038 | role | default_scope | Read |
| DF-REF-040 to DF-REF-044 | permission | role_id, capability_area, letters, matrix_version | Read |
| DF-REF-042 | permission | capability_area | Read |
| DF-REF-043 | permission | letters | Read |
| DF-REF-044 | permission | matrix_version | Read |
| DF-REF-198 to DF-REF-204 | masking_rule | role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 | delegation_limit | decision_code, approval_level, product_group, principal_limit, loss_pct_limit, limit_version | Read |
| DF-DEC-001 to DF-DEC-018 and DF-DEC-028 to DF-DEC-031 | access entry (local decision record) | decision code, actor, case ID, actions, decided at, hash chain, idempotency key | Write |
| DF-DEC-002 | access entry (local decision record) | case_id | Write |
| DF-DEC-003 | access entry (local decision record) | decision_code | Write |
| DF-DEC-014 | access entry (local decision record) | actions (area, right, field IDs, result) | Write |
| DF-DEC-030 | access entry (local decision record) | actor_user_id | Write |
| DF-TRT-012 and DF-TRT-028 | treatment (named in the authorise request and in the entry, through the rwb-treatment contract) | booked_at, booking_difference | Not read and not written; carried as field IDs on the entry |
| DF-CAS-001 to DF-CAS-023 | case attributes in the authorise request (owned by rwb-case) | case ID, owner, queue and team for the scope test | Read from the request; nothing copied |

No treatment row, no ACE row and no case row is copied into `rwb_access`: the case attributes for the scope test arrive with the authorise request on each decision, and the booked terms stay with rwb-treatment. No account number, amount or personal field is written on the access entry; the entry holds IDs and field IDs only. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. The decision is served through the operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1`; owner rwb-access (P4). This slice adds no path, no query parameter and no response field, and decides the following behind them:

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/authorise` | Decide a role's read or action for a capability area, a case and a field list, with the masking answer and the access entry | Any authenticated caller with a Workbench role | Idempotent by identity, area, right, case reference and field list within the cache window |
| GET | `/me/permissions` | The caller's resolved roles, scope, matrix version and the letters per capability area | Authenticated caller, own record only | Not applicable |
| GET | `/masking-policies` | The masking rows in force for a role and a field list (the masking read of RWB-P4-E1037-CON) | Authenticated caller | Not applicable |

Request for `/authorise`: the caller identity from the session, the capability area, the right, the case and treatment reference and the field IDs. Answer: the decision code (`AC-READ` or `AC-DENY`), the matrix version, the masking answer per field ID, the scope result and the access-entry reference; the response field names are Not specified in the source documents (GAP-0922; ASM-1644). Errors: 401 no Workbench role (MSG-P4-001), 403 no letter for the area or right (MSG-P4-002), 404 case absent or out of scope (MSG-P4-003), 503 decision record unwritable (MSG-P7-003).

The access-log search `GET /admin/access-log`, the role read `GET /admin/roles`, the session read `GET /me/session`, the reference loads and the rule-package paths are P4 surface delivered by other P4 stories (RWB-P4-E1039-APP, RWB-P4-E1022-APP, RWB-P4-AD002-APP, RWB-P4-AD011-APP); this story adds none of them.

#### 12.2 REST operations consumed

None. The case attributes for the scope test arrive in the authorise request, and rwb-access calls no service at run time; the one hop and the 2 s budget of DP-11 apply to the inbound call.

The rwb-integration contract (RWB-P2-E2007-CON) is consumed as a fixture only: the TreatmentBooked envelope and the booking-match result name the case, the treatment and the three task codes this policy pack covers. rwb-access calls no rwb-integration operation and reads no ACE view: the parameter and reference-data values reach it through the client libraries of rwb-case (DP-06, DP-07).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | role code and area, or the matrix version | matrix version, capability area, role code, letters, valid-from date |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 | caseId, or the actor for an entry with no case | decision code, area, right, field IDs, matrix version, record reference, business date |

Both are written to the outbox in the same transaction as the answer and relayed with the CloudEvents envelope; no personal data is carried (DP-09). The access log is never published as its own event: it is the decision-record entry of this service (DP-03), and `AccessPolicyChanged` is the only access event on the topic, with `DoaLimitChanged` for the DoA rows of RWB-P4-E1038-APP.

#### 12.4 Events consumed

None. This slice consumes no topic: the decision is served from the matrix version in force on each call, and a change of the pack drops the cached entry in the transaction that writes the new version. `AccessPolicyChanged` is published for the other services' caches and for gateway-bff; this service does not consume its own outbox.

#### 12.5 Workflows and activities

None. The decision is a synchronous REST call in the caller's thread and this story runs no workflow and starts no activity (Temporal and Drools design, this story runs no workflow). The Drools kit is applied only as a read of the evaluated policy rows: the letters of a capability area are rows, not a decision table, and the routing rows R-RES-22 and R-SET-13 are evaluated in rwb-case (RWB-P3-E2007-APP), never here.

#### 12.6 Schedules

None. The booking-confirmation job (JOB-08) is a Schedule in rwb-integration, carried by the P2 slice; the access-review list (JOB-18, six-monthly) belongs to RWB-P4-AD008-APP (Architecture v5 slide 44). This story holds no Schedule of its own.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| role | P4 (rwb_access) | Recovery roles as data, with role class and default scope |
| permission | P4 (rwb_access) | Capability area, letters and matrix version per role |
| masking_rule | P4 (rwb_access) | Which role sees which personal field unmasked, by masking version; no row applies to this capability |
| role_conflict | P4 (rwb_access) | Conflicting role pairs; read by the sign-in path, not by this story |
| access entry (local decision record) | P4 rows in `rwb_access`, written through the P7 decision-record library | The access log of this capability as `AC-READ` and `AC-DENY` entries (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |

`delegation_limit` is the same service's table and is served by RWB-P4-E2013-APP; this story reads none of it.

rwb-access reads no table of another service and holds no foreign key across services (DP-01); the central ledger copy of the access entries is written in `rwb_decision` from the topic by RWB-P7-E1027-CON.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration fixture (RWB-P2-E2007-CON) | The P2 contract of this legacy key | TreatmentBooked for `TRT-SYN-0701` on case `RW-2026-000701`, business date `2026-12-16`, and the booking-match result naming `WITH_OPS_BOOKING`, `WITH_OPS_SETTLEMENT` and `UNMATCHED_EXCEPTION`; replayed twice for the cache and entry tests |
| RWB-P4-E1037-CON fake | The P4 authorise and masking contract | `/authorise` and the masking read, with a granted case and a refused case |
| decision-record library stub | DP-03 | A healthy chain and outbox, and a stopped chain for the 503 path (TC-E2-007-11) |
| parameters and reference-data fakes | DP-06, DP-07 | The decision-cache lifetime and LOV-CAPABILITY and LOV-SCOPE |
| rwb-source-data contract fake | DP-05 | Restructure flag for RW-RESTRUCT (TC-E2-007-02) and the other ACE facts this story reads |

The exact request and answer shapes of `/authorise` are stubbed from the published fixture of RWB-P4-E1037-CON; their field list is Not specified in the source documents (GAP-0922; ASM-1644).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | The decision is served on the RWB-P4-E1037-CON contract; no new path, no outbound call, and one hop within 2 s on the inbound call |
| Kafka | 2 published, 0 consumed | `rwb.access.events.v1` and `rwb.decision-record.v1` published; no topic consumed |
| Temporal | None | No workflow and no activity in this story |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `authorisation`, Java package `th.co.scb.ace.workbench.recovery.access.authorisation`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own (metadata "Depends on (build)" = None) and builds against the rwb-access baseline and its contract fake, with the platform contract libraries and the P4 contract stories already delivered by the baseline. DP-05 applies as a prohibition (no ACE view is read here), DP-10 as a statement that the job tick is not this service's (JOB-08 sits with rwb-integration and JOB-18 with RWB-P4-AD008-APP), and DP-19 as the screen route behind SCR-14 and SCR-01.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | Controller | `POST /authorise` with validation and the problem mapping for 401, 403, 404 and 503 |
| PermissionController | Controller | `GET /me/permissions` and `GET /masking-policies` |
| AuthoriseService | Service | Unions the letters across the caller's roles, applies the scope test, decides `AC-READ` or `AC-DENY` and orders the entry write before the answer |
| PolicyRepository | Repository | Reads `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` at the version in force; reads no other schema |
| ScopeEvaluator | Service | Compares the case owner, queue and team carried in the request with the role's default scope; refuses an allow when an attribute is missing |
| MaskingReader | Service | Resolves the masking answer per field ID from the masking version in force |
| AccessEntryWriter | Service | Writes the access entry through the decision-record library, first in the transaction, and its outbox row |
| PolicyCache | Cache | Holds a decision under the matrix version it was decided on and drops it on a version change |
| PolicyChangePublisher | Service | Publishes `AccessPolicyChanged` in the transaction that writes a new version in force |
| ReferenceCatalog | Service | Reads LOV-CAPABILITY and LOV-SCOPE through the reference-data contract; no area or scope value in Java |

**Database and migrations**

- Reads `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` in schema `rwb_access`; writes the access entry of the decision-record library and the outbox row.
- Migration in this story: `V2007_1__authorise_decision.sql` adds the index on `permission (capability_area, matrix_version, role_id)` used by the decision read and the index on the access entry (actor, decided_at) used by the access-log search of RWB-P4-E1039-APP. The tables arrive with the `rwb_access` baseline; no column is added for case or treatment data.
- No row of `role`, `permission`, `masking_rule`, `role_conflict` or `delegation_limit` is written by this story: the pack is loaded by RWB-P4-AD002-APP and the DoA rows by RWB-P4-E1038-APP.

**Configuration and reference data**

- The policy pack slice in force: TREATMENT_AND_OFFER R and CASE_RECORD R and U for `RW-RESTRUCT` and `RW-CREDITAD`, PLATFORM_ADMINISTRATION U for `RW-PLATADM`, absent for `RW-CASEOWN`, and scope ALL for `RW-AUDIT`, at matrix version `PM-2026.12`.
- No masking row for `DF-TRT-012` or `DF-TRT-028`: neither is a personal field.
- The decision-cache lifetime is a parameter read through the parameters contract (DP-06); its value is Not specified in the source documents (GAP-0924; ASM-1647).
- The feature switch is `rwb.access.booking-confirmation-authorise`, read as a parameter through the parameters contract: off means the decision is refused closed and the caller is told the capability is not open, never allowed by default.
- The login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0922; ASM-1645).

**Build steps**

1. PolicyRepository and PermissionController over the matrix version in force, with a test per letter set; no role or area in code.
2. AuthoriseService with the letter union and the default-deny path; tests for AC6.
3. ScopeEvaluator over the request attributes, with the not-found, the missing-attribute and the no-partial-allow tests; tests for AC5.
4. MaskingReader with the masking version and the no-row answer; test for AC1 and AC8.
5. AccessEntryWriter with the entry before the answer, the `AC-READ` and `AC-DENY` codes, and the 503 when the record cannot be written; tests for AC1 to AC5 and TC-E2-007-11.
6. PolicyCache with the version-keyed entry and the drop on a pack change; tests for AC7.
7. PolicyChangePublisher and the outbox relay for `AccessPolicyChanged` and `DecisionRecorded`; test the topic name and the payload with no personal data.
8. Contract-fake run of every cross-service answer in isolation, so the story builds before rwb-case and rwb-integration are live.

**Feature switch.** `rwb.access.booking-confirmation-authorise`, read as a parameter; off refuses closed and allows nothing.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P2-E2007-CON and RWB-P4-E1037-CON stay green, and a SIT week shows every read of the booked terms and every completion of a booking task decided with one entry, every refused action refused with MSG-P4-002 or MSG-P4-003, and no access entry carrying an amount or a personal field.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No Workbench role on the token | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | The area or the right is absent for the caller's roles | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is absent or outside the caller's scope | This case is not in your scope. |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P2-011 | Task text of `WITH_OPS_BOOKING` and `WITH_OPS_SETTLEMENT`, shown on the screen this decision guards | No booking for treatment {treatment} was found in the ALS load for {date}. Book it in ALS. Accounts not booked: {accounts}. |
| MSG-P2-012 | Task text of `UNMATCHED_EXCEPTION`, shown on the screen this decision guards | The booked {term} is {booked}. The approved {term} is {approved}. |

For MSG-P4-002 in this story, {action} names the action the caller tried — for example "rerun the booking-confirmation job" or "read the booked terms" — and never a case fact. MSG-P2-011 and MSG-P2-012 are raised and owned by the rwb-integration slice and are copied here unchanged, because the screen this decision guards shows them.

### 15. Screens and states

SCR-14 Treatment record, states approved and booked: the officer asks to see `booked_at` (DF-TRT-012) or `booking_difference` (DF-TRT-028) with each term approved and booked, and the decision for that read comes from this story. SCR-01 My work: the officer and the Credit Administration officer see their booking and terms tasks and complete them, and the decision for that update comes from this story. Both screens show case IDs, treatment IDs, amounts and dates only; no personal field is on either screen for this capability, so no masking row is read here and nothing is masked.

SCR-01 My work states: empty and loading as defined in Screen Specifications v1 section SCR-01; error and no access are Not specified in the source documents (CG-ALL-5183).

Both screens are served by the gateway-bff composite route (DP-19), which calls rwb-case for the case and the task, rwb-treatment for the booked terms and rwb-access for the decision, one hop each, and merges the answers into the screen model. The screen fields, the field-level masking of the composite route and the route specification are Not specified in the source documents (GAP-0922; ASM-1644).

SCR-14 Treatment record states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-5184). SCR-29 Posting, which shows the confirmation for all bookings, comes in Epic 4. SCR-29 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-5185).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-007-10 | AC4, AC6, BR3 | Component | RW-CASEOWN calls the authorise decision for PLATFORM_ADMINISTRATION U on the booking-confirmation job; refused with MSG-P4-002, one AC-DENY entry, no job starts |
| TC-E2-007-01 | AC1, AC8, BR1, BR6, BR7 | Contract | Synthetic settlement booked 2026-12-16 at 650,000.00 baht; TREATMENT_AND_OFFER R granted for RW-RESTRUCT on `RW-2026-000701` with field IDs DF-TRT-012 and DF-TRT-028 |
| TC-E2-007-02 | AC2, BR6, BR13 | Component | Restructure with `tdr_flag` false served by the rwb-source-data contract fake (§12.8); the `WITH_OPS_BOOKING` completion is decided AC-READ for RW-RESTRUCT |
| TC-E2-007-03 | AC3, AC8, BR6 | Component | Rate 4.5000 booked against 4.2500 approved; the `UNMATCHED_EXCEPTION` completion is decided AC-READ for RW-CREDITAD, with no amount on the entry |
| TC-E2-007-04 | AC4, BR6 | Component | Two accounts, one booked; each booking task is decided once and the read that precedes each completion is recorded once |
| TC-E2-007-05 | AC5, BR10 | Component | ACE batch failed for 2026-12-17 behind the fixture; the booked-terms read is still decided, and no personal field is named |
| TC-E2-007-06 | AC6, BR11 | Component | JOB-08 rerun for 2026-12-16; the cached decision is served under the matrix version it was decided on |
| TC-E2-007-07 | AC7, BR4 | Component | Booking missing on two batches; the case of another owner is asked for and answered 404 MSG-P4-003 with no case data |
| TC-E2-007-08 | AC8, BR8 | Contract | Decision record store stopped; the read answers 503 MSG-P7-003 and returns no case data |
| TC-E2-007-09 | AC6, AC7, BR3, BR11 | Component | No permission row in force for the area on 2026-12-17; default deny, then a new version in force and the cached refusal dropped |
| TC-E2-007-11 | AC8, BR8, BR6 | NFR | Decision record write forced to fail on the booked-terms read; nothing is returned and nothing is shown, with the entry count unchanged |
| TC-E2-007-12 | Not specified in the source documents (ASM-3438) | Component | Boundary check: reads and writes of this story are compared with the tables of §12.7; a read of any table outside that list fails the test |
| TC-E2-007-13 | AC9, BR2, BR5, BR9, BR12, BR14 | Component | RW-RESTRUCT with scope OWN asks CASE_RECORD R on `RW-2026-000701` without the owner attribute; refused, no case data, no masking row or DoA row read |
| TC-E2-007-14 | AC10 | Contract | Caller with no valid credential asks POST /api/recovery/access/v1/authorise for CASE_RECORD R on `RW-2026-000701`; answered 401 with no case data |
| TC-E2-007-15 | AC11 | Component | Not specified in the source documents (NEWAC-RWB-P4-E2007-APP-AC12) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to Component, Access to Contract and Resilience to NFR. Every legacy test case of this key is listed above with the slice of the behaviour this story answers; the -ITG copies of these cases are not here — they belong to the integration slice RWB-ITG-E2007-ITG, which proves the same values across rwb-integration, rwb-case, rwb-treatment and rwb-source-data end to end.

### 17. Guardrails

- No business value in code: roles, capability areas, letters, scope values, the masking rows, the DoA rows and the decision-cache lifetime are data rows and parameters read with the version in force. No role code, area or letter appears in Java.
- No personal data in events, logs, workflow inputs or tests. This story writes case IDs, treatment IDs, role codes and field IDs only; the access entry never carries a name, an address, an identity number, an account number or an amount. Test data uses synthetic keys (`TRT-SYN-0701`, `RW-2026-000701`).
- ACE data only through the owner's contract or the owner's `v_ace_*` views. This story reads no ACE table and no ACE view: the case attributes for the scope test arrive in the authorise request, and the group-to-role mapping of the sign-in path belongs to RWB-P4-E1022-APP and RWB-P4-AD001-APP.
- No cross-schema read: `rwb_access` holds no foreign key into another schema and no copy of a case, treatment or ACE row (DP-01). The `delegation_limit` and `masking_rule` rows are this service's own data.
- One evaluator per concern: the letters of an area are versioned rows, not a decision table, and the routing rows R-RES-22 and R-SET-13 stay in rwb-case. rwb-access holds no route table, no DRL source and no workbook (DP-04).
- The access entry is written first, in the same transaction as the answer, through the decision-record library; a failed write means the answer is 503 and no data is shown (R-UNI-39, BR8).
- Every outbound event is written to the outbox in the same transaction and carries IDs and facts only; the access log is a decision-record entry, never a new Kafka event (DP-03, DP-09).
- The decision is cached only under the matrix version it was decided on, and a missing case attribute never decides an allow (BR11, BR12).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Booking confirmed from the next day's ALS batch, with the role that may read the booked terms and complete the booking task decided by rwb-access | Program 5.3; Epic 2 3.2 | FEAT-CHO-08 | 7.3 Negotiate settlement or deed in lieu | R-RES-22, R-SET-13, R-UNI-39 | TC-E2-007-01 to TC-E2-007-09, TC-E2-007-10, TC-E2-007-11, TC-E2-007-12 |

The supporting features of the policy pack are FEAT-ACA-04 (role to permission matrix as data), FEAT-ACA-05 (mask PDPA fields by role) and FEAT-ACA-07 (every access event to the access log), which the FSD P4 module pairs with its own requirements in RWB-E1-037 and RWB-E1-039; this slice answers them only for the booking-confirmation capability and changes neither matrix nor log design. The -ITG copies of the test cases are carried by RWB-ITG-E2007-ITG.

### 19. Out of scope

- The matching run, JOB-08, the ALS read and the task texts: rwb-integration (RWB-P2-E2007-APP), with its contract in RWB-P2-E2007-CON.
- The case move from the operations-waiting route state, the timer and the task rows: rwb-case (RWB-P3-E2007-APP).
- The treatment record, its APPROVED to BOOKED state and the booking difference: rwb-treatment (RWB-S2-E2007-APP).
- The ACE account and batch read behind the match: rwb-source-data (RWB-P1-E2007-APP).
- The end-to-end proof of these values across the four services: RWB-ITG-E2007-ITG.
- Posting a settlement booking to ALS from the Workbench and the SCR-29 Posting screen: FEAT-PAY-06, Epic 4.
- Loading the policy pack and the DoA rows: RWB-P4-AD002-APP and RWB-P4-E1038-APP; the matrix as a whole and the masking design: RWB-P4-E1037-APP.
- The access-log search and export screen, the break-glass grant and the access review list: RWB-P4-AD007-APP, RWB-P4-AD006-APP and RWB-P4-AD008-APP.
- The sign-in path, the group-to-role mapping and the separation-of-duty check: RWB-P4-E1022-APP, RWB-P4-AD001-APP and RWB-P4-AD005-APP.
- The `rwb_access` schema baseline, the topic and queue provisioning, the dashboards and the runbook of this capability.
