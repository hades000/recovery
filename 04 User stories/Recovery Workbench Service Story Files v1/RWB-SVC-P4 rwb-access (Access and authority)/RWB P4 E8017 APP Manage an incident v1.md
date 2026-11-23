# RWB-P4-E8017-APP Manage an incident

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BK |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E8017-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-017 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **platform administrator, and the access service that holds the record of the incident**, I want **one incident taken through its path  -  detected, held, fixed, recorded and reported  -  as two appended entries of this service's own decision-record chain that name the capability areas and rights held while the incident is open, the fix and the report it closes with, and the parameters version in force at each step**, so that **a fault in access, limits or rules is contained while it is open and reported afterwards from the service that holds the access policy, with nothing changing while a step cannot be recorded**.

Inside `rwb-access` this is the incident-record slice of the legacy story RWB-E8-017:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Service facts of this slice: no event of its own is published, no workflow is started, no table of its own is written and no screen of its own is served  -  the legacy screen table names SCR-39 Rules and parameters and SCR-41 Delegation of authority, and the incident surface arrives through the gateway-bff composite route of DP-19.
- Three deliverables, and nothing else: the write `POST /api/recovery/access/v1/admin/incidents`, which records the detect and the hold and answers the incident in state `OPEN`; the write `POST /api/recovery/access/v1/admin/incidents/{incidentId}/closure`, which records the fix, the record and the report and answers the incident in state `CLOSED`; and the read `GET /api/recovery/access/v1/admin/incidents/{incidentId}`, which answers the incident with its five steps.
- The five step names are the five words of the legacy criterion itself  -  `DETECTED`, `HELD`, `FIXED`, `RECORDED`, `REPORTED`  -  and the first two come from the open while the last three come from the closure.
- There is no incident entity in the sources: not in TSD P4 v3 T3.1, not in the Logical Data Model and Data Dictionary v8 and not in the Physical Schema v6; and `rwb_access` owns five tables, none of them an incident. The record is therefore two entries of the local decision-record chain of DP-03, each written in the same transaction as its idempotency row, and the incident id is minted by this service and is opaque to every consumer (ASM-1594).
- The right that opens the path is `PLATFORM_ADMINISTRATION`, which TSD P4 v3 T6.1 gives RW-PLATADM as `CRUD`, RW-SECADM as `CRUDA`, RW-AUDIT as `R` and RW-COE as `R`. The legacy permission table of RWB-E8-017 names Rules and parameters C for RW-COE and A for RW-RISK, which is the rule-change right set of the same legacy chapter and not this feature's; the conflict is recorded and resolved by R-PREC, the technical specification standing above the story master (GAP-0879; ASM-1595).
- The parameters version in force is read through the parameters contract of DP-06 and carried on each entry: that is the "rule version" the legacy criterion asks the record to hold.
- The enforcement of a hold on the operations of the other services is not this story's: the guard of RWB-P4-E1037-APP authorises each call in this service's own schema, and the break-glass and access-log work is RWB-P4-E1039-APP. This story records the window those stories read and changes no permission row.
- Detection arrives as the incident reference and the detection time a person enters. TSD P4 v3 T5.1 declares no interface from P4 to Log Analytics, the FSD names Log Analytics as an integration point of the feature only, and the observability platform is RWB-PLT-OBS's (GAP-0879; ASM-1594).
- The record code a step is written under, and the field-level shape of a step inside an entry, are Not specified in the source documents (GAP-0879; ASM-1596).

### 2. Business rationale

The business owns the incident path and the FSD states its target in one measure: rule and limit changes made without a code release, 100 percent, read from the decision log and the Workbench records every month (FSD P4 v3 A2.28.1). The problem the FSD names for the module is unchanged  -  "access, limits and rules live in documents and people's heads; changes need code or manual checks" (FSD P4 v3 A2.28.1)  -  and the legacy key carries the whole path of an incident, from the detection to the report, as one administration screen against the monolith's own rule tables (RWB-E8-017; FEAT-ADM-12).

In the target the incident is not a screen state of a rule table. It is a record of the service that holds the access policy: which capability areas and which rights were held, for which scope, from when and until when, what the fix was, and which report closes it. That record is what Compliance and Internal audit read after the fact, and it is the only artefact that says an incident happened at all, because no table in any schema holds one.

The record matters more than it looks. A hold is a decision: the administrator decides that for a named area and right, inside a named scope, access is narrowed until the fix is in. R-UNI-39 says no action proceeds unlogged and the legacy criterion's second half says nothing changes where the record cannot be written; this story carries both for the incident. The same reasoning fixes the boundary: a hold that quietly edited a permission row or a delegation limit would change the matrix that the approval router and the guard read, so this story writes no value in force and proves it (BR8, AC6).

The story meets REQ-DRI-001 (every decision writes one record holding the rule and configuration versions and the actions taken), REQ-DRI-010 (a versioned parameter catalog changed without a code release) and REQ-ACA-013 (the full administration surface is available to the administrators of this module, in Epic 8). It contributes the record half of an incident and leaves the rule registry, the rule version lifecycle and the guard's enforcement to their owners.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8017-CON (same service, its own contract story) | The published OpenAPI 3.1 document of the three operations, the `Incident` and `IncidentStep` schemas, the step set and the state set, the error envelope, the consumed declarations and the contract fakes. This story implements that document and adds no path and no field |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): two entries per incident, hash-linked, each in the transaction that writes its idempotency row |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the parameters version in force, read at each write and carried on the entry. A C dependency, so it never blocks the build |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the incident surface reaches the three operations through it, one hop each |
| The legacy screen table of RWB-E8-017 | SCR-39 Rules and parameters and SCR-41 Delegation of authority, with their states Versions, load and approval. Neither screen is an incident screen and neither is built here |

Business preconditions carried from RWB-E8-017 and from the module specification:

- The rights in force are those of TSD P4 v3 T6.1: RW-PLATADM holds `CRUD` in Platform administration, RW-SECADM `CRUDA`, RW-AUDIT `R`, RW-COE `R` and the case roles hold `-`. Opening needs C, closing needs U and reading needs R (ASM-1595).
- The capability areas a hold may name are the fourteen values of LOV-CAPABILITY  -  `CASE_RECORD`, `QUEUE_AND_ALLOCATION`, `TREATMENT_AND_OFFER`, `LITIGATION`, `ASSET_AND_DISPOSAL`, `DEBT_SALE`, `WRITE_OFF_AND_POSTING`, `DOCUMENTS`, `RULES_AND_PARAMETERS`, `REFERENCE_DATA`, `DECISION_LOG`, `PARTNER_PORTAL`, `REPORTING`, `PLATFORM_ADMINISTRATION` (TSD P4 v3 T3.2).
- The rights a hold may name are the letters C, R, U, D and A, as in `permission.letters` (TSD P4 v3 T3.1, DF-REF-043).
- The scopes a held area may name are the four of LOV-SCOPE: `OWN`, `TEAM`, `REGION`, `ALL` (TSD P4 v3 T3.2).
- The parameters version in force is the data of the day of the step and is never a constant (BR-P4-028; FSD P4 v3 A2.28.3.1).
- The staff reference of the caller resolves through the session; no name and no e-mail address is read, held or returned by this story (NFR-040).

### 4. Flow

1. The platform administrator opens the administration surface through the gateway-bff composite route (DP-19), which calls the three operations of this story, one hop each.
2. A detection arrives as an incident reference and a detection time, and the administrator opens the incident: `POST /api/recovery/access/v1/admin/incidents` with the body `incidentReference`, `detectedAt`, `heldAreas` (each with `capabilityArea`, `rights` and `scope`), `reason`, and the `Idempotency-Key` of the submission.
3. `IncidentController` validates the body: `incidentReference`, `detectedAt`, at least one held area and `reason` are required and an empty one is 422 with MSG-GEN-001 naming the field; `detectedAt` that is not a timestamp is 422 with MSG-GEN-001; a `capabilityArea` outside the fourteen of LOV-CAPABILITY, a right outside C, R, U, D and A, or a scope outside LOV-SCOPE is 422 with MSG-GEN-001 naming the field path of the entry (X1).
4. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Platform administration C. A caller without the letter is refused with 403 and MSG-P4-002, and nothing is appended (BR4, AC5).
5. `IncidentReferenceCheck` looks for an incident already open under the same `incidentReference`. A second open of the same reference is refused with 409 and MSG-GEN-004 and appends nothing, so an incident is open once (BR5, AC4).
6. `ParameterReader` reads the parameters version in force on the detection date through the parameters contract of DP-06, and the version label is carried on the entry (BR7).
7. `IncidentRecorder` appends one entry to the local decision-record chain of DP-03 in the same transaction as the idempotency row: the incident id, the incident reference, the detection time, the held areas with their rights and scopes, the reason, the caller reference and the parameters version. The steps `DETECTED` and `HELD` are the steps that entry carries (BR1, BR3; ASM-1596).
8. The answer is 201 with the `Incident` in state `OPEN`: `incidentId`, `incidentReference`, `state`, `detectedAt`, `heldFrom` as the time of the entry, `heldAreas`, `reason`, `parametersVersion`, `steps` with `DETECTED` and `HELD` on that entry, `actorReference`, `recordedAt`, and the `Location` of the read (BR2).
9. The administrator fixes the fault and closes the incident: `POST /api/recovery/access/v1/admin/incidents/{incidentId}/closure` with `resolvedAt`, `fixReference`, `reportReference`, `reason` and the `Idempotency-Key`.
10. The closure is authorised for Platform administration U, validated as in step 3, and refused with 409 and MSG-GEN-004 where the incident is already `CLOSED`, so a closure is written once (BR2, AC4). An unknown `incidentId` is 404 and names the identifier only (X9).
11. `IncidentRecorder` appends one entry carrying `FIXED`, `RECORDED` and `REPORTED`, with the fix reference, the report reference, the resolution time, the reason, the caller reference and the parameters version in force on the resolution date, and answers the `Incident` in state `CLOSED` with `heldTo` as the resolution time (BR1, BR2).
12. Where an entry or its idempotency row cannot be written, the step is not taken: the call fails with 503 and MSG-P7-003, no incident id is returned on the open and no closure is written on the close, and nothing else changes (legacy AC2; R-UNI-39; BR6).
13. The same `Idempotency-Key` replayed answers the first answer, writes no second entry and mints no second incident id (BR11).
14. `GET /api/recovery/access/v1/admin/incidents/{incidentId}` reads the two entries of the incident and answers the `Incident` with `steps` as the five step rows in path order  -  `DETECTED`, `HELD`, `FIXED`, `RECORDED`, `REPORTED`  -  each with its entry id, its recorded time and its parameters version, so the report of an incident is one read with no build (BR10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is empty, `detectedAt` or `resolvedAt` is not a timestamp, or an area, a right or a scope is outside its list | 422 naming the field, no entry appended | MSG-GEN-001 | AC3 |
| X2 | The caller holds no Platform administration C on the open, or no U on the closure | 403, no entry appended; nothing about an incident is disclosed | MSG-P4-002 | AC5 |
| X3 | The caller's session has ended | 401, no entry appended | MSG-P4-001 | AC5 |
| X4 | The incident reference is already open | 409 and no second incident; the answer names the reference | MSG-GEN-004 | AC4 |
| X5 | The incident is already `CLOSED` | 409 and no second closure | MSG-GEN-004 | AC4 |
| X6 | The parameters contract does not answer inside 2 s, or the connection fails | 503 and no entry; a retry with the same `Idempotency-Key` cannot create a second entry | MSG-P7-003 | AC2 |
| X7 | An entry, or its idempotency row, cannot be written | 503; no incident id on the open and no closure on the close, and nothing is written at all | MSG-P7-003 | AC2 |
| X8 | The caller holds `-` in every area the incident holds | 404 with MSG-P4-003 and no held area, no reason and no step is returned | MSG-P4-003 | AC5 |
| X9 | The `incidentId` is unknown to this service | 404 naming the identifier only | None | AC4 |
| X10 | The same request arrives twice with the same `Idempotency-Key` | The first answer is replayed; no second entry and no second incident id | None | AC4 |

No exception path of this story writes a permission row, a masking rule, a delegation limit or a role: this service writes entries of its own chain only, and every value in force is unchanged by a refused call and by a recorded one (BR8).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8017-CON and its fakes; the parameters version is consumed through its contract and the record library is a platform dependency, so this story holds no incident table and no value in force |
| Negotiable | The step vocabulary is the legacy criterion's own five words and the state set is `OPEN` and `CLOSED`; the record code and the field shape of a step inside the entry are settled with audit and with the library owner |
| Valuable | One incident opened with its hold, closed with its fix and its report, and read back as one document with its five steps and the parameters version of each |
| Estimable | One controller, one incident service, one reference check, one parameters reader, one recorder, one reader, four fakes and eight test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule, no event of its own and no screen of its own |
| Testable | Each owned criterion has a test case in section 16; the duplicate, the second closure, the scope refusal and the unchanged matrix are provable against the fakes and its own schema |

### 7. Acceptance criteria

```gherkin
Feature: Manage an incident

  Background:
    Given the environment is SIT
    Given the run date is 15 December 2026
    Given test user "U-8201" holds RW-PLATADM with "CRUD" in "PLATFORM_ADMINISTRATION"
    Given test user "U-8202" holds RW-AUDIT with "R" in "PLATFORM_ADMINISTRATION"
    Given test user "U-8203" holds RW-PHONECOL with "-" in "PLATFORM_ADMINISTRATION"
    Given the step set is the five steps DETECTED, HELD, FIXED, RECORDED and REPORTED

  Scenario: AC1 Manage an incident (legacy RWB-E8-017 AC1)
    Given the rwb-case contract mock returns parameters version "PAR-2026.11" in force on 15 December 2026
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then runs the incident path: detect, hold, fix, record and report
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-017 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 One incident and its five steps are two entries and one read (new, D-RCV-60)
    Given the rwb-case contract mock returns parameters version "PAR-2026.11" in force on 15 December 2026
    When "U-8201" posts an incident with reference "INC0004521", detectedAt 2026-12-15T09:15:00Z, one held area "CASE_RECORD" with rights "R", "U" and scope "ALL", and a reason, with Idempotency-Key "k-e8017-1"
    Then the response is 201 in state "OPEN" with incidentId, heldFrom, the same held area and parametersVersion "PAR-2026.11"
    Then exactly one decision-record entry is appended and its steps are DETECTED and HELD
    When "U-8201" posts the closure of that incidentId with resolvedAt 2026-12-15T11:40:00Z, fixReference "CHG-4471", reportReference "IR-2026-031" and a reason
    Then the response is 200 in state "CLOSED" with heldTo 2026-12-15T11:40:00Z, fixReference "CHG-4471" and reportReference "IR-2026-031"
    Then exactly one further entry is appended and its steps are FIXED, RECORDED and REPORTED
    Then GET /api/recovery/access/v1/admin/incidents/{incidentId} answers the incident with the five steps in path order, each with its entry id and its parameters version
    Then the decision-record chain of this service holds exactly two entries for that incident and neither is updated

  Scenario: AC4 A reference is open once and a closure is written once (new, D-RCV-60)
    Given incident "INC0004521" is open
    When "U-8201" posts a second open with reference "INC0004521" and the same held area
    Then the response is 409 with message MSG-GEN-004 and no second incident exists and no entry is appended
    Given the incident is closed by "U-8201"
    When "U-8201" posts a second closure of the same incidentId with Idempotency-Key "k-e8017-2"
    Then the response is 409 with message MSG-GEN-004 and the incident keeps the state "CLOSED" it had and no third entry is appended
    When the closure is replayed with Idempotency-Key "k-e8017-1"
    Then the first closure answer is returned and no third entry is appended

  Scenario: AC5 A role without the right is refused and a hold outside the caller's areas is not disclosed (new, D-RCV-60)
    Given incident "INC0004521" is open and holds the area "CASE_RECORD" with right "U" and scope "ALL"
    When "U-8203" holding RW-PHONECOL posts an incident
    Then the response is 403 with message MSG-P4-002 and no entry is appended
    When "U-8203" reads the incident by its incidentId
    Then the response is 404 with message MSG-P4-003 and the body carries no held area, no reason and no step
    When "U-8202" holding RW-AUDIT with "R" reads the incident by its incidentId
    Then the response is 200 with the five steps and the parameters version of each
    Then the answer carries no name, no e-mail address and no personal field

  Scenario: AC6 The hold changes no value in force (new, D-RCV-60)
    Given permission matrix version "PM-2026.11" and masking version "MASK-SIT-01" are in force and the delegation limits are those of "DOA-2026.11"
    When an incident is opened holding the area "DEBT_SALE" with right "C" and scope "ALL", and then closed
    Then the permission matrix version in force is still "PM-2026.11", the masking version is still "MASK-SIT-01" and the limits are still those of "DOA-2026.11"
    Then no row of role, permission, masking_rule, role_conflict or delegation_limit is written, updated or deleted by the two calls
    Then the two entries of the incident record the held area, the right, the scope and the window, and hold nothing else
```

AC1 and AC2 are the two criteria of RWB-E8-017, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the parameters mock, so the rule version of the criterion is provable while the parameters contract is still a fake. AC3 to AC6 are new under D-RCV-60 and test only what this story adds: the five steps in two entries, the once-only reference and closure, the right and the scope refusal, and the statement that a hold writes no value in force.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An incident is a record of this service and not a table: one entry for the open and one for the closure, each appended to the local decision-record chain of DP-03 in the same transaction as its idempotency row | RWB-E8-017 AC1; DP-03; ASM-1594 |
| BR2 | The path is five steps in two entries: `DETECTED` and `HELD` on the open, `FIXED`, `RECORDED` and `REPORTED` on the closure; the states are `OPEN` and `CLOSED` and no other state exists | Legacy RWB-E8-017 AC1 (detect, hold, fix, record and report); ASM-1594 |
| BR3 | A hold names one or more capability areas of LOV-CAPABILITY, one or more rights of C, R, U, D and A, and one scope of LOV-SCOPE; anything outside those lists is refused with 422 and MSG-GEN-001 and appends nothing | TSD P4 v3 T3.1 and T3.2; FSD P4 v3 A2.28.3.1 |
| BR4 | Opening needs Platform administration C, closing needs U and reading needs R; RW-PLATADM holds `CRUD`, RW-SECADM `CRUDA`, RW-AUDIT `R` and the case roles `-`, and a caller without the letter is refused 403 with MSG-P4-002 with nothing appended | TSD P4 v3 T6.1; legacy RWB-E8-017 permission table read under R-PREC (ASM-1595) |
| BR5 | One incident per reference: a reference already open is refused 409 with MSG-GEN-004, and one closure per incident: a closed incident is refused 409 with MSG-GEN-004 | ASM-1594; FSD P4 v3 AC-EXC-P4-007-05 for the duplicate rule |
| BR6 | Every step appends exactly one entry in the same transaction as the answer; where the entry cannot be written the step is not taken and the caller sees 503 with MSG-P7-003 | R-UNI-39; legacy RWB-E8-017 AC2; DP-03 |
| BR7 | The parameters version in force is read through DP-06 at each write and carried on the entry, so the record states the rule version of the step | Legacy RWB-E8-017 AC1; REQ-DRI-010; BR-P4-028 |
| BR8 | A hold records a window and changes no value in force: this story writes no row of `role`, `permission`, `masking_rule`, `role_conflict` or `delegation_limit`, and the matrix version, the masking version and the limits are the same before and after the incident | FSD P4 v3 A2.28; DP-08; AC6 |
| BR9 | A record outside the caller's areas is not disclosed: a caller holding `-` in every held area is answered 404 with MSG-P4-003, with no held area, no reason and no step | FSD P4 v3 VR-P4-028-1 and MSG-P4-003 (AC-EXC-P4-028-01) |
| BR10 | The read answers the five steps in path order with the entry id, the recorded time and the parameters version of each, so the report of an incident needs no export and no second screen | Legacy RWB-E8-017 AC1 (report); BR2 |
| BR11 | One `Idempotency-Key` answers one step: a replay answers the first answer and appends no second entry and mints no second incident id | Architecture v5 slide 11; DP-09 |
| BR12 | The record carries references, codes, versions, dates, times, rights and scopes only: no name, no e-mail address and no personal field, and the reason is a short free-text field that a pipeline check refuses where it carries personal data | NFR-040; FSD P4 v3 A2.28.3.2 |
| BR13 | The enforcement of a hold on the operations of the other services, and the rule-version lifecycle that a fix may touch, are other stories': the guard of RWB-P4-E1037-APP, the break-glass and access-log work of RWB-P4-E1039-APP and the registry of RWB-P4-E8007-APP. This story adds no enforcement, no approval and no version state | TSD P4 v3 T6.1 and T6.2; RWB-P4-E1037-APP; RWB-P4-E1039-APP |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR6 are one recorder: the entry and the idempotency row commit in one transaction and a failure rolls both back, so an incident step can never exist without its record.
- BR2 is the one place the step vocabulary is written: the two writes declare their step set as a constant of the contract and the read concatenates the entries in append order.
- BR3 is one pass over the three lists before the parameters read, so an invalid area, right or scope costs no hop and leaves no entry.
- BR4 is the authorise call before any read of the record, so a caller without the letter learns nothing about an incident.
- BR5 is one lookup on the reference column of the chain and one read of the state of the incident from its entries, both inside the write transaction.
- BR7 is one reader: the parameters version is asked of the contract at each write and is copied onto the entry, never recomputed on a read.
- BR8 is an absence: this story has no repository for a permission row, a masking rule, a role conflict or a limit, and its only write is the chain.
- BR9 is the scope filter of the read: an incident is visible to a caller who holds at least one letter in at least one held area, and invisible as a 404 to everyone else.

### 9. State transitions

This story defines the state of an incident and observes nothing of another service. The state is derived from the entries of the chain and is never stored separately.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The open is posted | Platform administration C, a valid body and a reference not already open | Two steps appended, `OPEN` |
| (none) | The open is posted | A required field is empty, or an area, a right or a scope is outside its list | No entry, 422 with MSG-GEN-001 |
| (none) | The open is posted | The reference is already open | No entry, 409 with MSG-GEN-004 |
| `OPEN` | The closure is posted | Platform administration U and a valid body | Three further steps appended, `CLOSED` |
| `OPEN` | The closure is posted | The incident is already `CLOSED` | No entry, 409 with MSG-GEN-004 |
| `CLOSED` | A further step is posted | None | No entry, 409 with MSG-GEN-004; a closed incident is never re-opened by this story |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | A step is recorded, refused or replayed | One entry appended with its `prev_hash` and `entry_hash`, or none at all; no entry is ever updated or deleted |
| Append-only local chain | The parameters version changes | A new step carries the new version; an old entry keeps the version it was written under |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Platform administrator (RW-PLATADM) | Holds Platform administration `CRUD`: opens an incident with its hold, closes it, and reads it back. Primary actor (FSD P4 v3 A2.28.3.3; TSD P4 v3 T6.1) |
| Security administrator (RW-SECADM) | Holds Platform administration `CRUDA`: opens, closes, reads, and reads the incident beside the break-glass grants of RWB-P4-E1039-APP |
| Internal audit (RW-AUDIT) | Holds Platform administration `R`: reads an incident, its five steps and the parameters version of each as the evidence of the path |
| Tribe lead and squad members (RW-TRIBE) | Named as a secondary role by FSD P4 v3 A2.28.3.3; hold `R` and may read an incident only where that `R` is in force for the area, and are refused a write with 403 and MSG-P4-002 |
| RW-PHONECOL, RW-CASEOWN and the other case roles | Hold `-` in Platform administration: refused a write with 403 and MSG-P4-002, and answered 404 with MSG-P4-003 on a read of an incident whose areas they hold no letter in |
| The gateway-bff route | Calls the three operations on behalf of the signed-in user, one hop each, and caches nothing across users |
| `rwb-access` itself | Reads `role` and `permission` in its own schema, resolves its own session, and appends entries of its own chain and its own idempotency rows |
| `rwb-case` (P3) | Owns the parameters contract; this story reads the version in force and writes nothing there |
| `rwb-decision` (P7) | Owns the central ledger `decision_log_entry` and the query over it; this story neither reads nor writes the ledger |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002, the not-found shape of a record outside the caller's areas is 404 with MSG-P4-003, and the unauthenticated shape is 401 with MSG-P4-001. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E8017-CON together with the rest of the service's contract.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_class, default_scope | Read: the role and its class of the caller |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read: the C and U letters in `PLATFORM_ADMINISTRATION`, and the letters of the caller in the held areas |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the incident entry: `decision_code` DF-DEC-003 (the record code of a step, ASM-1596), `case_id` DF-DEC-002 empty for an incident, `inputs_ref` DF-DEC-008 with the incident id, the reference, the detection or resolution time, the held areas with their rights and scopes, the reason, the fix reference, the report reference and the parameters version, `actions` DF-DEC-014 with the steps, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the incident by its identifier |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of a step | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` (platform library table in `rwb_access`) | the record row of a step | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | `delegation_limit` of `rwb_access` | none: a hold writes no limit | Not read and not written |
| DF-REF-198 to DF-REF-204 | `masking_rule` of `rwb_access` | none: a hold writes no masking rule | Not read and not written |
| DF-REF-205 to DF-REF-211 | `role_conflict` of `rwb_access` | none: a hold writes no conflict pair | Not read and not written |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` of `rwb_decision` | none: the central ledger is P7's | Not read and not written |

No incident table exists in `rwb_access` and none is created: the record is the local chain of DP-03, and the read derives the state and the five steps from the entries of one incident id (DP-01, DP-15). The record code a step is written under, the field-level shape of a step inside `actions`, and the incident-id format are Not specified in the source documents (GAP-0879; ASM-1596); the contract of RWB-P4-E8017-CON fixes the answer, and the entry carries the same fields. Field IDs are those of the Logical Data Model and Data Dictionary v8.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/incidents` | P4 `rwb-access` | Body: `incidentReference`, `detectedAt`, `heldAreas` (`capabilityArea`, `rights[]`, `scope`), `reason` | `Incident`: `incidentId`, `incidentReference`, `state` `OPEN`, `detectedAt`, `heldFrom`, `heldAreas`, `reason`, `parametersVersion`, `steps` (`DETECTED`, `HELD`), `actorReference`, `recordedAt`, with `Location` of the read | 401 (MSG-P4-001); 403 Platform administration C (MSG-P4-002); 409 the reference is already open (MSG-GEN-004); 422 a required field empty, a time not a timestamp or a value outside its list (MSG-GEN-001); 503 the step cannot be recorded or the parameters contract is unavailable (MSG-P7-003) | Platform administration C | `Idempotency-Key` header required; the stored answer is replayed |
| POST | `/api/recovery/access/v1/admin/incidents/{incidentId}/closure` | P4 `rwb-access` | Body: `resolvedAt`, `fixReference`, `reportReference`, `reason` | The same `Incident` in state `CLOSED` with `heldTo`, `fixReference`, `reportReference` and `steps` `FIXED`, `RECORDED`, `REPORTED` | 401 (MSG-P4-001); 403 Platform administration U (MSG-P4-002); 404 unknown incident id; 409 the incident is already `CLOSED` (MSG-GEN-004); 422 (MSG-GEN-001); 503 the step cannot be recorded (MSG-P7-003) | Platform administration U | `Idempotency-Key` header required; the stored answer is replayed |
| GET | `/api/recovery/access/v1/admin/incidents/{incidentId}` | P4 `rwb-access` | None | The `Incident` with `steps` as the five step rows in path order, each with `step`, `entryId`, `recordedAt` and `parametersVersion` | 401 (MSG-P4-001); 403 caller holds no letter in any held area, answered 404 with MSG-P4-003 where the record is not in the caller's areas; 404 unknown incident id; 503 the record cannot be read (MSG-P7-003) | Platform administration R | Not applicable, read only; no Idempotency-Key |

All three operations sit under the base `/api/recovery/access/v1` of DP-13. They are this service's record of an incident; the rule-version paths the legacy story names  -  `POST /admin/rule-versions` and `POST /admin/rule-versions/{versionId}/approve`  -  are the load gate of RWB-P4-AD011-APP and the approval of RWB-P4-AD012-APP at the monolith's base, and in the target they are the rule registry's in `rwb-decision` (RWB-P4-E8007-CON). This story repeats none of them, adds no path to either and starts no rule version.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Platform administration C check of the open, the U check of the closure and the R check of the read, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The parameters version in force on the date of the step, which the entry carries; the C dependency `RWB-P3-E1042-CON` |

The authorise operation is this service's own and is declared consumed because the guard is a separate story of the same contract set (RWB-P4-E1037-CON). The parameters read is the only call that leaves the service.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a step: the incident id, the reference, the steps of the entry, the held areas with their rights and scopes, the detection or resolution time, the fix reference, the report reference and the parameters version |

CloudEvents 1.0 envelope; the payload carries references, codes, versions, dates, times, rights and scopes and no name, no e-mail address and no personal field. This story publishes no `rwb.access.<Event>.v1` message: the two events of `rwb-access` are `AccessPolicyChanged` and `DoaLimitChanged`, owned by other stories of this service, and a hold is a record and not a policy change (BR8). The rationale that a subscriber would need is stated on the pipeline of the guard and is not published as an event, because publishing a hold would put the access policy of the bank on a topic.

#### 12.4 Events consumed

None. The detection of an incident arrives as the reference and the detection time a person enters, and no source declares a feed from the observability platform to P4 (GAP-0879; ASM-1594).

#### 12.5 Workflows and activities

None. This story starts no workflow, signals none and registers no activity on the `rwb-access` queue; an incident is request-driven and its two writes are synchronous. The access review list of JOB-18 is RWB-P4-AD008-APP's.

#### 12.6 Schedules

None. Neither a detect, a hold, a fix, a record nor a report is a scheduled step.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role and class of the caller |
| `permission` | P4 (`rwb_access`) | Read only: the C, U and R letters in `PLATFORM_ADMINISTRATION`, and the letters of the caller in the held areas |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the two entries of an incident. Read: the entries by incident id |
| `idempotency_key`, `outbox_event`, `processed_event` | PLT library, created in `rwb_access` | The idempotency row and the outbox row of each entry; no inbox row is written because no event is consumed (DP-09) |
| `delegation_limit`, `masking_rule`, `role_conflict` | P4 (`rwb_access`) | Not read and not written: a hold changes no value in force (BR8) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's |

No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| parameters fake | RWB-P3-E1042-CON | `GET /api/recovery/case/v1/admin/parameters` answering the parameters version "PAR-2026.11" in force on 15 December 2026, and a second version after it for the test that a changed version needs no build |
| authorise and guard fake | RWB-P4-E8017-CON, RWB-P4-E1037-CON | A granted answer for RW-PLATADM with `CRUD` and for RW-AUDIT with `R`, and a refused answer with MSG-P4-002 for RW-PHONECOL holding `-` |
| decision-record fake | RWB-PLT-E1027-CON | The append of an entry, the hash-link check, the read of the entries of one incident id, the replay by `Idempotency-Key` and the forced write failure of AC2 |
| gateway-bff fake | RWB-PLT-N001-CON | The incident surface of the composite route: the open form with its held areas, the closure form, and the read with its five steps |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3; consumed 2 | Base `/api/recovery/access/v1`; the own authorise operation and the `rwb-case` parameters read, one hop and 2 s each |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this story |
| File | None | No file input and no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/incident`, Java package `th.co.scb.ace.workbench.recovery.access.incident`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module administration screen that ran the path in one process (DP-13 and DP-19: the service's own base, and the surface moved to the composite route) and the monolith's own decision log write (DP-03: the local chain of the library). There is no DP-01 here because no table is written at all, and no DP-09 row of its own because the outbox row is the library's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| IncidentController | Controller | The three operations: body validation, the authorise call before the record read, the RFC 9457 mapping, `Location` on a created incident |
| IncidentService | Service | The incident id, the step set of each write, and the assembly of the answer from the entries |
| HeldAreaValidator | Service | The fourteen areas of LOV-CAPABILITY, the five rights and the four scopes of LOV-SCOPE, named in the 422 |
| IncidentReferenceCheck | Service | The reference already open, inside the write transaction |
| PermissionReader | Service | The `role` and `permission` rows of the caller behind the authorise operation |
| ParameterReader | Service | The parameters version in force through the contract of DP-06 |
| IncidentRecorder | Service | The entry and its outbox and idempotency rows, in one transaction (DP-03, DP-09) |
| IncidentReader | Service | The entries of one incident id, the state derived from them, and the replay by `Idempotency-Key` |

**Database and migrations**

- This story creates no table of its own. The local decision-record table of DP-03 and the platform library objects `outbox_event`, `processed_event` and `idempotency_key` are created in `rwb_access` by the service's own DB work in the per-service Flyway sequence of DP-15, and this story only writes and reads them.
- No incident table is created and no column is added to `role`, `permission`, `masking_rule`, `role_conflict` or `delegation_limit`.
- The read of an incident needs a lookup on the reference column of the chain entries; where the SIT plan needs an index that the creating story does not have, the index is added to that story's migration and not to a new one here.
- No statement updates or deletes an entry: the chain is append-only, and the only writes of this story are one entry, one outbox row and one idempotency row per step.

**Configuration and reference data**

- The parameters version in force is read through DP-06 on the date of the step and carried on the entry; this story holds no threshold, no duration and no default, so no parameter value is a constant in code (BR7).
- The five step names, the two states and the held-area lists are contract constants published by RWB-P4-E8017-CON; a new step or a new area is a contract change and not a data change, and the areas themselves stay the list of TSD P4 v3 T3.2.
- The right of each operation  -  C, U and R in Platform administration  -  is a constant of the document and its values are rows of `permission`, so a change of who may open an incident is a permission row and needs no release (BR4).

**Build steps**

1. `HeldAreaValidator` with the three lists, and the 422 of AC3 that names the field path and makes no hop.
2. `PermissionReader` and the authorise call before the record is read; the AC5 refusal of RW-PHONECOL and the 401 of X3.
3. `IncidentRecorder` and the open, with the hash link, the replay by `Idempotency-Key` and the forced failure of AC2 (X7).
4. `IncidentReferenceCheck` and the second-open refusal of AC4 (X4).
5. The closure with its own steps and the second-closure refusal of AC4 (X5).
6. `IncidentReader` with the five step rows in path order and the scope filter of AC5 (X8).
7. `ParameterReader` over the parameters contract, and the test that a changed parameters version needs no build.
8. The composite-route run of the surface through the gateway-bff fake, so the path can be demonstrated while the guard is being built.

**Feature switch.** No switch of this slice's own: an incident path that is switched off would leave an administrator without a record of a hold they took, which is the failure the record exists to prevent. The service-level flag of the service baseline governs the administration surface, and this story adds none.

**Done when.** The tests in section 16 pass; an incident opened with one held area is answered 201 in state `OPEN` with the two steps `DETECTED` and `HELD` and leaves exactly one entry; its closure is answered in state `CLOSED` with the three further steps and leaves exactly one further entry; the read answers the five steps with their parameters versions; a second open of the same reference and a second closure are answered 409 with MSG-GEN-004; RW-PHONECOL is refused 403 with MSG-P4-002 on the write and answered 404 with MSG-P4-003 on the read; a forced record failure leaves nothing written and answers 503 with MSG-P7-003; and no value in force has changed after the two calls.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on all three operations |
| MSG-P4-002 | The caller holds no Platform administration C on the open, no U on the closure, or no R on the read | You cannot {action} here. Your role does not include it. | This story, from the authorise answer |
| MSG-P4-003 | The caller holds `-` in every area the incident holds | This case is not in your scope. | This story, on the read, as a 404 with no field of the incident |
| MSG-GEN-001 | A required field is empty, a time is not a timestamp, or an area, a right or a scope is outside its list | Enter {field}. | This story, on both writes |
| MSG-GEN-004 | The reference is already open, or the incident is already `CLOSED` | Someone else changed this record. Reload it to see their change. | This story, on both writes |
| MSG-P7-003 | A step cannot be recorded, or the parameters contract cannot be reached | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on all three operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The 422 names the field path of the refused entry, and the 409 names the reference or the state, so the surface can show the refusal without a second call. The text of MSG-P4-001 to MSG-P4-003, MSG-GEN-001 and MSG-P7-003 is the text of the legacy message table of RWB-E8-017 and of FSD P4 v3, copied unchanged; MSG-GEN-004 is the text the contract baseline of this service already publishes.

### 15. Screens and states

The incident surface arrives through the gateway-bff composite route of DP-19, which calls the three operations of this story, one hop each, and merges the answers. No source names an incident screen: the legacy screen table of RWB-E8-017 lists SCR-39 Rules and parameters and SCR-41 Delegation of authority, and neither is an incident screen, so this story serves the operations behind the surface and builds no screen of its own (GAP-0879; ASM-1594).

| Screen | State | What it shows |
|---|---|---|
| The incident surface of the composite route | Detect and hold form | The incident reference, the detection time, the held areas with their rights and scopes, and the reason, with the invalid ones marked before the call |
| The incident surface of the composite route | Open | The incident with its id, `heldFrom`, the held areas and the parameters version, and the two steps already recorded |
| The incident surface of the composite route | Already open | The 409 with MSG-GEN-004 and the reference named, with nothing appended |
| The incident surface of the composite route | Fix and close form | The resolution time, the fix reference, the report reference and the reason |
| The incident surface of the composite route | Closed | The incident with `heldTo`, the fix reference, the report reference and the three closure steps |
| The incident surface of the composite route | Report | The read: the five steps in path order with the entry id, the time and the parameters version of each |
| The incident surface of the composite route | Not in your areas | The 404 with MSG-P4-003 and no held area, no reason and no step |
| The incident surface of the composite route | Refused | The 403 with MSG-P4-002 for a role without the letter, with no form and no incident detail |

The monitor that raises the detection is not this story's surface: the observability platform of RWB-PLT-OBS holds it and TSD P4 v3 T5.1 declares no P4 interface to it, so the reference and the detection time are entered here and the alert itself stays outside this service.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-017-01 | AC1, BR1, BR7 | Contract | The parameters fake: version "PAR-2026.11" in force; an incident opened with one held area and closed with a fix and a report; two entries, each carrying the parameters version |
| TC-E8-017-02 | AC2, BR6 | Component | The record store forced to fail during the open, and again during the closure: 503, MSG-P7-003, no incident id, no closure and no entry |
| TC-E8-017-03 | AC5, BR4, BR9 | Component | RW-PHONECOL with `-`: 403 and MSG-P4-002 on the write; 404 and MSG-P4-003 on the read with no held area, no reason and no step; RW-AUDIT with `R`: 200 with the five steps |
| TC-E8-017-04 | AC2, BR6, BR11 | NFR | The record store forced to fail on a run of repeated attempts with one `Idempotency-Key`: every attempt answers 503 with MSG-P7-003, nothing is written, no partial incident exists and a later retry with the same key answers one incident |
| TC-E8-017-05 | AC3, BR2, BR10 | Component | An open with reference "INC0004521", detectedAt 2026-12-15T09:15:00Z and one held area `CASE_RECORD` with rights R and U and scope ALL: 201 `OPEN` with DETECTED and HELD; a closure at 2026-12-15T11:40:00Z with fix "CHG-4471" and report "IR-2026-031": `CLOSED` with FIXED, RECORDED and REPORTED; the read with the five steps in order |
| TC-E8-017-06 | AC4, BR5 | Component | A second open of "INC0004521" and a second closure of a closed incident: 409 with MSG-GEN-004 each time, no entry, the state kept; a replay of the closure with the first key answers the first answer |
| TC-E8-017-07 | AC6, BR8 | Component | The matrix version "PM-2026.11", the masking version "MASK-SIT-01" and the limits of "DOA-2026.11" before and after an open and a close of an area `DEBT_SALE` with right C: unchanged, with no row written in the five tables |
| TC-E8-017-08 | AC3, AC5, BR3, BR12 | Component | An area outside LOV-CAPABILITY, a right outside C, R, U, D and A, and a scope outside LOV-SCOPE: 422 with MSG-GEN-001 naming the field path and no entry; and the answer of a valid incident carrying no name, no e-mail address and no personal field |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows of RWB-E8-017 are kept: TC-E8-017-01 for AC1, TC-E8-017-02 for AC2, TC-E8-017-03 for the access refusal and TC-E8-017-04 for the forced record failure, and four rows are added for the new criteria of this story. The legacy table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, per §R7.2 s16. No ITG story is split from this legacy key, so no `-ITG` copy of these test cases is written here.

### 17. Guardrails

- No business value in code: the areas, rights and scopes are the lists of the technical specification and the parameters version is read through DP-06; a test proves that a changed parameters version needs no build (BR7).
- No personal data anywhere: an incident carries references, codes, versions, dates, times, rights and scopes, and the reason is checked for personal data before it is written, so no name, no e-mail address and no personal field appears in the answer, the entry or the tests (BR12, NFR-040).
- No read of another service's tables (DP-01): the parameters version arrives through the contract of `rwb-case`, the central ledger is `rwb-decision`'s, and no join crosses a schema.
- No incident table: the record is the append-only chain of DP-03, so a step cannot be edited after the fact and the audit reads the same entries the service does (BR1).
- A hold changes nothing in force: this story holds no repository for a permission row, a masking rule, a role conflict or a delegation limit, and a test proves the four values are the same before and after (BR8).
- No record, no step: where an entry cannot be written the call is refused with MSG-P7-003 and nothing is written, so a hold that cannot be defended is never taken (legacy AC2, R-UNI-39).
- A refused caller learns nothing: the 403 names the missing right and not the incident, and a caller with no letter in the held areas is answered a 404 with no field of the record (BR9).
- One reader and one writer: the open and the closure are the only writes and the read is the only way out, so the report of an incident is the record itself and never a copy.
- The guard, the break-glass grant, the access log and the rule registry are other stories': this story adds no enforcement, no approval and no version state (BR13).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model and agent versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome | Program | FEAT-ADM-12 | All recovery processes | BR1, BR2, BR10 | TC-E8-017-01, TC-E8-017-05 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release | Program | FEAT-ADM-12 | All recovery processes | BR7 | TC-E8-017-01, TC-E8-017-05 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Program | FEAT-ADM-12 | All recovery processes | BR4, BR9 | TC-E8-017-03, TC-E8-017-08 |

The requirement IDs are the rows this story serves, taken from the Program BRD and the FSD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this story.

| Legacy reference | Where it is kept |
|---|---|
| AC1 manage an incident: run the incident path detect, hold, fix, record and report, and write the result to the decision log with the rule version | Sections 1, 4, 7, 8, 12.1, 12.3, 14 |
| AC2 not recorded: the decision log cannot be written, nothing changes and MSG-P7-003 | Sections 1, 4, 5, 7, 8, 17 |
| The legacy endpoints `POST /admin/rule-versions` and `POST /admin/rule-versions/{versionId}/approve` | Sections 1, 12.1, 19  -  the load gate of RWB-P4-AD011-APP and the approval of RWB-P4-AD012-APP, and the registry's in `rwb-decision` |
| Permission checks: Rules and parameters C for RW-COE and A for RW-RISK | Sections 1, 3, 10, 12.1  -  read as Platform administration C, U and R under TSD P4 v3 T6.1 (GAP-0879; ASM-1595) |
| Screens SCR-39 Rules and parameters and SCR-41 Delegation of authority with their states | Sections 3, 15, 19 |
| MSG-P4-002, MSG-P4-003, MSG-P4-004, MSG-GEN-001, MSG-P7-003 | Section 14 and the exception paths; MSG-P4-004 is the break-glass banner of RWB-P4-E1039-APP and is not produced here |
| The `decision_log_entry`, `rule_row` and `role` entities of the legacy data table | Section 11  -  the record in the local chain, the rule version through DP-06 and the role and permission rows read only |
| TC-E8-017-01 to TC-E8-017-04 | Section 16 |
| Legacy key RWB-E8-017, story RWB-P4-E8017-APP, contract RWB-P4-E8017-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The monitoring that raises a detection: the observability platform of RWB-PLT-OBS, the alerts of the Log Analytics workspace and the call from it to P4, which TSD P4 v3 T5.1 does not declare.
- The enforcement of a hold on the calls of the other services: the guard of RWB-P4-E1037-APP authorises each call in its own schema, and this story defines none of it.
- The break-glass grant, the access-log search and the denial entries of a refusal: RWB-P4-E1039-APP, which reads an incident beside its grants.
- The load gate of a rule version and its approval: RWB-P4-AD011-APP and RWB-P4-AD012-APP, and the rule registry of `rwb-decision`.
- The rule-change record and the rule-change report: RWB-P4-E8007-APP and RWB-P3-E2041 (legacy RWB-E2-041).
- The move of a delegation limit and the update of the permission matrix as data: RWB-P4-E8008-APP and RWB-P4-E1037-APP. An incident records a hold and writes no row of either.
- The central ledger `decision_log_entry`, its hash chain and the query API over it: `rwb-decision` (P7).
- The incident surface itself, its panels and its composite route specification: RWB-PLT-N001-CON and the Epic 8 screen work.
- The pipeline check that refuses personal data in a free-text field: RWB-PLT-LIB, named here as a guardrail only.
- The integration harness and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
