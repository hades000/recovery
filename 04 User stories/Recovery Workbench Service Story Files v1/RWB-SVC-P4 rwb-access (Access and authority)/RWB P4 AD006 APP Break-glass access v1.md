# RWB-P4-AD006-APP Break-glass access

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-006 for rwb-access — the lifecycle of an incident-bound break-glass grant: its request, its security-administrator approval, its activation, the break-glass marking of every action, its own end at the end of the window, the session state it leaves and the decision-record entry of every activation and every refusal. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P4-A |
| Ready to start | After RWB-P4-E1039-APP |
| Depends on (build) | RWB-P4-AD006-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON, RWB-P4-E1039-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | RWB-P4-AD006-DB |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **platform administrator**, I want **emergency access beyond my role, tied to an open incident, ending on its own**, so that **an incident can be fixed without a permanent grant**.

This is the rwb-access slice of legacy RWB-AD-006, and it is the **lifecycle** half of that legacy key: the request with its open incident reference and its reason, the security administrator's approval, the activation, the break-glass marking of every action taken under the grant, the self-expiry at the end of the window with no action by anyone, and the state the caller's session carries while the grant is in force.

- **Service naming:** REST base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery` (not used here — this story starts no workflow), Java package `th.co.scb.ace.workbench.recovery.access`.
- **The grant:** one row of `break_glass_grant` in `rwb_access`, raised by one activation and ended by its own window. It carries the acting user reference, the open incident reference, the capability area, the right and the scope the emergency covers, the reason of at least 20 characters, the window start and end, the approver reference of the security administrator's approval, its state (`ACTIVE` or `ENDED`) and the break-glass marker the entries carry (RWB-P4-AD006-DB owns the columns).
- **The area, the right and the scope:** the capability area is one of the 14 capability areas (`DF-REF-042`, LOV-CAPABILITY), the right is one letter of `C`, `R`, `U`, `D` and `A` or a dash (`DF-REF-043`), and the scope is one of own, team, region and all (`DF-REF-038`, LOV-SCOPE). The grant raises those letters **for the one caller and for the one window**, and for nothing else.
- **The approval:** the security administrator approves the request in the bank IAM as an IAM request; the activation names that approval by its reference, so the approval is evidenced on the grant and never claimed by the activating caller (TSD P4 v3 API-P4-013: "Activate a break-glass grant approved in the bank IAM for an open incident, area, right, scope and reason").
- **The window:** the grant is in force from its activation until the end of the window, which is the earlier of the window hours from the activation and the end of the bank IAM group membership. The value in force is **4 hours** (FSD P4 v3 AC-ALT-P4-009-01: activation at 10:30, grant active until 14:30, group end 18:00); the hours are parameter data (`rwb.access.breakglass.window-hours`), never a constant in code (ASM-1492).
- **The end with no action by anyone:** the authority is the clock. A grant is in force only while its state is `ACTIVE` and `now` is before its window end, so the first call after the window end is refused with no person, no ticket and no job having done anything. The row settles to `ENDED` and writes its end entry on the next read of the grant (ASM-1496).
- **The marking:** every action taken while the grant is in force carries the grant reference and the incident reference on its record. The session exposes them (`GET /me/session`, API-P4-012, through the `breakGlass` field that RWB-P4-AD006-CON declares), the authorisation guard of this service passes them on every call, and the entry the access-log writer of RWB-P4-E1039-APP writes carries them (ASM-1495).
- **The incident:** the grant is bound to one open incident. An incident reference that is absent, that does not match the incident pattern, or that the incident register does not hold open refuses the activation and writes a refusal entry (GAP-0797; ASM-1491).
- **The record:** every activation and every refusal writes one local decision-record entry through the decision-record library of DP-03 and publishes it on the shared topic `rwb.decision-record.v1`. Where the entry cannot be written the grant is not activated and the call fails with 503 and MSG-P7-003.
- **Screens:** SCR-43 Roles and access (list; access log) is served by the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON); the banner that tells the caller the emergency access is on is MSG-P4-004 with its end time.
- **Not this story — the access log and the administration surface of legacy RWB-E1-039:** RWB-P4-E1039-APP owns the access-log writer, the access-log read and the administration screen that **lists** the break-glass grants and their entries, RWB-P4-E1039-CON owns their contract and RWB-P4-E1039-DB owns the access-log table, its partitions and the library objects. **This story is the grant lifecycle (request, approve, activate, mark, expire); RWB-P4-E1039 is the access log and the administration surface that lists the entries.** The legacy access-log endpoint (API-P4-008) belongs to that key and to the access-log search of RWB-P4-AD007-APP, not here.
- **Not this story — the search and the export of the access log:** RWB-P4-AD007-APP owns the access-log search by person, date, event and capability area and its export.
- **Not this story — the sign-in, the role catalogue and the permission matrix:** RWB-P4-E1022-APP signs a person in and resolves the groups to roles, RWB-P4-E1019-APP owns the role and permission rows as data, and RWB-P4-E1037-APP owns the role-to-permission matrix, the masking rows and the guard that this story calls.
- **Not this story — the storage:** the table, its columns, its constraints, its indexes, its retention and the per-service login grant are RWB-P4-AD006-DB's, and this story reads and writes the rows through the per-service login only (DP-02).

### 2. Business rationale

An incident is fixed at three in the morning by whoever is on call, and the person who can fix it is often not the person who holds the letter that the fix needs. Legacy RWB-AD-006 answered that with emergency access beyond the caller's role, tied to an open incident and ending on its own, so that the incident is fixed without a permanent grant and without an administrator widening a role for ever. The answer is still right, and the realignment makes it a service answer: the grant is a row with a start, an end and an incident, the window ends by the clock, and every action under it is marked.

The split of this key is fixed. **This story owns the lifecycle — the request, the approval reference, the activation, the marking and the self-expiry. RWB-P4-E1039-APP owns the access log that records the actions and the administration surface that lists the grants; RWB-P4-E1039-DB owns the access-log table, its partitions and the library objects; RWB-P4-AD007-APP owns the search and the export of the log.** The boundary matters because the two halves fail differently: this half must refuse an activation that has no open incident or no approval, and that half must be able to show afterwards who used which grant on which case. Either half alone is not a control.

Three properties are the point of the slice. The first is that **the grant expires by the clock and not by an act**: a grant whose window has ended is out of force on the first call after it, whatever the row still says, so a forgotten grant is impossible and a lost job cannot extend access. The second is that **the grant is bounded**: one incident, one area, one right, one scope, one caller, one window, and at most one active grant per caller, so the emergency access is the narrowest thing that can still fix the incident. The third is that **the grant is evidenced**: the approval is an IAM request reference, the activation and every refusal are decision-record entries, and every action under the grant carries the grant and its incident, which is what FEAT-ACA-09 and FEAT-ACA-10 and REQ-ACA-008 ask of it.

The grant is **session state and not a policy change**, and that is why this capability publishes no event of its own. Architecture v5 slide 14 gives `rwb-access` two business events, `AccessPolicyChanged` and `DoaLimitChanged`, and slide 43 publishes them to all services for a cache refresh; a grant is neither. It changes no row of the permission matrix, no scope and no delegation limit, and it expires by itself, so a consumer that refreshed a cache on a grant event would cache an entitlement that has already ended. The two readers of a grant are the authorisation guard and the session read, both inside this service and both reading `rwb_access` on the call. The only message a grant produces is the decision-record entry, and that message is the library's, on `rwb.decision-record.v1` (ASM-1495).

The negative side is the reason the refusal is a first-class path and not an error branch. Emergency access that is granted without an open incident, or without the security administrator's approval, is a privilege escalation with an audit entry attached; the legacy criterion AC2 therefore refuses the request and this story refuses it before any row is written, with the refusal recorded. The incident register's owner is fixed by no source in this read set — the incident path of FSD P4 v3 A2.28 reaches Log Analytics and the Workbench and names no store — so the check is carried by a port with a Day-1 stub and the gap is recorded rather than hidden (GAP-0797; ASM-1491).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD006-CON (same service, its own contract story) | The published grant contract: the activation, the end and the read operations, the `BreakGlassActivation` and `BreakGlassGrant` schemas, the `breakGlass` field of the session, the auto-expiry rule, the error envelope and the fakes this story builds against |
| RWB-P4-E1039-APP (same service, the H dependency) | The access-log entry and its admin surface (legacy RWB-E1-039): the writer that stamps the grant reference and the incident on every entry it records, and the screen that lists the grants. It is the consumer of the marker this story sets, and AC1's "every action is marked break-glass" is observed through it |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of every activation and of every refusal |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19), which serves SCR-43 and merges the grant read with the access-log read |
| RWB-P4-AD006-DB (external, tracked) | The table `break_glass_grant` in `rwb_access`, its constraints and its indexes, and the per-service login grant (DP-02). The table has no row in the ownership map and none in TSD P4 v3 T3.1, so its shape is this key's own working decision (GAP-0799; ASM-1493) |
| The `role` and `permission` rows in `rwb_access` | The role codes, the Platform administration letters and the capability areas and scopes the grant is expressed in (DF-REF-034 to DF-REF-044), from the service baseline of RWB-P4-E1019-APP and RWB-P4-E1037-APP. This story reads them and writes none of them |
| The guard of RWB-P4-E1037-CON | The authorisation decision that this story extends: the letters of the caller, the scope, and the break-glass state the guard passes on every call (DP-08 is RWB-P4-E1037-APP's; this story calls the guard and adds the grant) |
| The bank IAM approval | The security administrator's approval of the request as an IAM request, and the group `RWB-SIT-BREAKGLASS` that admits a caller to the emergency path (FSD P4 v3 AC-ALT-P4-009-01 and AC-EXC-P4-007-01). The IAM owns the approval workflow and this story holds only its reference (ASM-1499) |
| The incident register | The open incident the grant is bound to. Its owner, its store and its contract are **Not specified in the source documents (GAP-0797; ASM-1491)**; the story carries a port with a Day-1 stub |
| The window hours and the reason bounds | The window in force is 4 hours (FSD P4 v3 AC-ALT-P4-009-01) and the hours are parameter data; the reason is at least 20 characters (legacy AC1) and at most 1000 (FSD P4 v3 AC-EXC-P4-007-02). The parameter codes are **Not specified in the source documents (GAP-0797; ASM-1492)** for the window and **Not specified in the source documents (GAP-0797; ASM-1497)** for the reason floor |
| No human approval of this document | This story is born in Draft (realignment v1) under D-RCV-60 and builds against a Draft contract; the contract is frozen when its consumers pass their contract tests |

**Wave.** Wave 4 is taken from the W-MAP of business epic EP08 (Template and Rules §R5.6) and not from the Arch v5 wave 1 of the service, as the Work Package fixes; the release date is copied unchanged and marked tentative.

### 4. Flow

1. The platform administrator opens SCR-43 Roles and access through the gateway-bff composite route of DP-19 and asks for emergency access on an incident. The route calls the grant read of this story and the access-log read of RWB-P4-E1039-APP in parallel, one hop each.
2. The caller is authorised at the door: the activation needs the C letter of Platform administration, the read needs R, and an active role is required on both. RW-SECADM holds CRUDA in Platform administration and RW-PLATADM holds CRUD (TSD P4 v3 T6.1). A caller with no Workbench role is refused 401 with MSG-P4-001, a caller without the letter is refused 403 with MSG-P4-002, and a caller outside the bank IAM break-glass group is refused by the IAM before this service is reached (FSD P4 v3 AC-EXC-P4-007-01). Every refusal this service makes is written as a decision-record entry before the answer leaves the service.
3. The activation posts `BreakGlassActivation`: the incident reference, the IAM request reference of the security administrator's approval, the capability area, the right, the scope, the reason and the requested window hours. The `Idempotency-Key` header makes the call safe to repeat.
4. `BreakGlassChecks` run before any row is written: the incident reference is present and matches the incident pattern; the incident register answers the incident open; the IAM request reference is present and names this caller; the capability area is one of the 14 (`DF-REF-042`); the right is one letter of `C`, `R`, `U`, `D` and `A` or a dash (`DF-REF-043`); the scope is one of own, team, region and all (`DF-REF-038`); the reason is at least 20 characters and at most 1000; and the requested window is a positive number of hours not above the maximum in force. Every failed check refuses the activation with 422 and writes a refusal entry.
5. The window is computed: it starts at the activation time and ends at the earlier of the activation time plus the window hours and the end of the caller's bank IAM group membership. With the value in force, an activation at 10:30 gives a grant active until 14:30 (FSD P4 v3 AC-ALT-P4-009-01). The grant is written `ACTIVE` with its start and its end, its incident and its approval reference.
6. The decision-record entry of the activation is written in the same transaction through the library of DP-03: decision code `AC-BGON`, the actor reference, the incident, the area, the right, the scope, the window and the time, and no name and no e-mail address. The entry id becomes the grant id, so the record and the grant cannot disagree. Where the entry cannot be written the grant is not activated and the call fails with 503 and MSG-P7-003.
7. The grant is answered as `BreakGlassGrant`: the grant id, the actor reference, the incident, the area, the right, the scope, the reason, the start and the end, the state `ACTIVE`, the approver reference and the break-glass marker.
8. While the grant is in force, the caller's session answers it: `GET /me/session` (API-P4-012) carries the `breakGlass` field — the grant id, the incident, the area, the right, the scope, the start, the end and the state — and the screen shows MSG-P4-004 with the end time: "Emergency access is on until {time}. Every action is recorded." The session read is the operation of RWB-P4-E1019-APP and RWB-P4-E1037-CON; this story fills its break-glass field from the grant (ASM-1495).
9. Every call the caller makes while the grant is in force goes through the authorisation guard, which reads the grant of the caller, adds the requested area and right when the grant covers them, and passes the grant id and the incident on the call context. Every entry written for that caller until the window end carries the grant id and the incident (FSD P4 v3 AC-ALT-P4-009-01), which is what "every action is marked break-glass" means: the access-log writer of RWB-P4-E1039-APP stamps the reference this story sets, and the decision-record entries of the actions carry the same reference.
10. The window ends. The first call after it is authorised as if the grant did not exist — the caller's own letters only — and is refused with MSG-P4-002 when the caller's role does not hold the letter; no person, no ticket and no job acts for the grant to end. This is the mechanism of AC3: the authority is the clock, and a grant is in force only while its state is `ACTIVE` and `now` is before its end (ASM-1496).
11. The row settles: the first read of the grant, the first session read or the first authorised call after the window end sets its state to `ENDED`, stamps the ended time and writes the `AC-BGOFF` decision-record entry through the library, so the record shows a grant that ended when its window ended. A grant that nobody touches stays `ACTIVE` in its row and out of force by time; the guard never reads it as an entitlement (ASM-1496).
12. The platform administrator may end a grant before its window: `POST /admin/break-glass-grants/{grantId}/end` sets the state to `ENDED` from that moment, writes the `AC-BGOFF` entry and makes the next call of the caller fall back to its own letters. The end is idempotent by `Idempotency-Key`, and an ended grant cannot be reactivated; a new activation is a new grant with its own approval and its own incident.
13. A second activation while a grant of the caller is still in force is refused with 409 and MSG-GEN-004: a caller holds at most one active grant, enforced by the database constraint of RWB-P4-AD006-DB and answered as a conflict here. The same request repeated with the same `Idempotency-Key` returns the first answer and opens no second grant (FSD P4 v3 AC-EXC-P4-007-05).
14. The grant read answers one grant by its id: the actor reference, the incident, the area, the right, the scope, the reason, the window, the state, the approver reference and the entry reference of its activation. A grant that does not exist is answered 404 with the envelope, and no grant is invented.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The incident reference is absent, or it does not match the incident pattern | 422 naming the field; no row is written and a refusal entry is recorded | MSG-GEN-001 | AC2 |
| X2 | The incident register does not hold the incident open | 422 naming the field; no grant and a refusal entry with reason `NO_OPEN_INCIDENT` | MSG-GEN-001 (GAP-0797; ASM-1491) | AC2 |
| X3 | The IAM request reference is absent, does not name this caller, or names no approval | 422 naming the field; no grant and a refusal entry with reason `NO_APPROVAL` | MSG-GEN-001 | AC2 |
| X4 | The reason is shorter than 20 characters | 422 naming the field, the minimum and the maximum; nothing is written | MSG-GEN-002 | AC2 |
| X5 | The capability area, the right or the scope is not a value of its list | 422 naming the field and the value; nothing is written | MSG-GEN-001 | AC2 |
| X6 | The requested window is zero, negative or above the maximum in force | 422 naming the field; nothing is written | MSG-GEN-002 | AC2 |
| X7 | The caller holds no Platform administration C for the activation, or no R for the read | 403 before any row is read or written, one refusal entry | MSG-P4-002 | AC2 |
| X8 | The caller holds no Workbench role at all | 401 before any row is read or written, one refusal entry | MSG-P4-001 | AC2 |
| X9 | A second activation arrives while the caller's grant is in force | 409 with the envelope; the grant in force is unchanged and is answered | MSG-GEN-004 | AC2 |
| X10 | The decision-record entry cannot be written | 503, no grant row is written and the state is unchanged | MSG-P7-003 | AC2 |
| X11 | A call arrives after the window end | The grant is out of force on the clock and the caller is authorised on its own letters; refused with MSG-P4-002 where the letter is missing | MSG-P4-002 | AC3 |
| X12 | A second activation repeats the first with the same `Idempotency-Key` | The first answer is returned, no second grant and no second entry is written | None | AC1 |
| X13 | The end operation arrives on a grant already ended | The end is idempotent: the answer is the grant as it stands, and no second end entry is written | None | AC3 |
| X14 | The grant asked for does not exist | 404 with the envelope; no grant is answered and none is invented | MSG-GEN-004 | AC2 |
| X15 | The grant row settles to `ENDED` while another caller reads it | The read answers one state whole, `ACTIVE` or `ENDED`, and never a mixture | None | AC3 |

No exception path of this story changes a case, a task, an approval or a case state: emergency access widens a caller's letters for one window, and the case state machine and the approval are other services'.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the grant contract of RWB-P4-AD006-CON and its fakes, the decision-record library, the gateway-bff route and the access-log writer of RWB-P4-E1039-APP; it writes one service's own grant rows and reads the service's own role and permission rows |
| Negotiable | The window hours, the incident pattern and the reason bounds are data; the story fixes the checks, the marking, the expiry rule and the answer shapes only |
| Valuable | An incident is fixed in the window without a permanent grant, and every action under the grant is marked and recorded |
| Estimable | One migration is the DB story's; here: one check set, three operations, the guard extension, the session field, two record codes and one settle step |
| Small | Fits one sprint with its tests; the access log, the search and the screen are other stories' |
| Testable | Every criterion in section 7 is one automated test over synthetic grants, a stubbed incident register and a stubbed decision-record library; no real incident, person or entitlement is needed |

### 7. Acceptance criteria

```gherkin
Feature: Break-glass access

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given a grant is one row of "break_glass_grant" in "rwb_access" bound to one open incident
    Given a grant is in force only while its state is "ACTIVE" and now is before its window end

  Scenario: AC1 Granted with an incident (legacy RWB-AD-006 AC1)
    Given the platform library contract mock returns the decision-record entry accepted on "rwb.decision-record.v1" for the grant
    Given an open incident and a reason of at least 20 characters
    When the security administrator approves the request
    Then the system grants access for the window and every action is marked break-glass

  Scenario: AC2 Refused without an incident (legacy RWB-AD-006 AC2)
    Given no open incident
    When the request is made
    Then the system refuses it

  Scenario: AC3 Ends on its own (legacy RWB-AD-006 AC3)
    Given an active grant
    When the window ends
    Then the grant ends with no action by anyone
```

The three criteria are the legacy criteria of RWB-AD-006, copied word for word with the origin tag, and `20 characters` is kept character for character. One Given line is added and nothing else is changed: the faked answer of the decision-record library (DP-03, the H dependency RWB-PLT-E1027-CON) that accepts the entry of the grant. Every legacy value is kept as it stands.

AC1 is answered by the activation this story performs and by the marking the guard and the access-log writer of RWB-P4-E1039-APP apply; the approval it names is the security administrator's IAM approval, held by its reference on the grant, so the criterion is observed at the activation that follows it. AC2 is answered by the checks of step 4 and by the refusal entry, with the incident register stubbed because no source fixes its owner (GAP-0797; ASM-1491). AC3 is answered by the clock: the window end is a value on the row, the guard reads it on every call, and no person and no job acts for the grant to end (ASM-1496).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Emergency access is bound to one open incident and to one caller: an incident reference that is absent, malformed or not open refuses the activation, and a refusal writes no grant | Legacy RWB-AD-006 AC2; FSD P4 v3 A2.9 and AC-EXC-P4-007-02; ASM-1491 |
| BR2 | The activation names the security administrator's approval by its IAM request reference, and the grant carries the approver reference. The caller cannot approve the request it activates | Legacy RWB-AD-006 AC1; TSD P4 v3 API-P4-013; ASM-1499 |
| BR3 | The reason is at least 20 characters and at most 1000. The minimum is the legacy rule and the floor the database enforces; the maximum is the column width | Legacy RWB-AD-006 AC1; FSD P4 v3 AC-EXC-P4-007-02; GAP-0799; ASM-1497 |
| BR4 | The grant is bounded to one capability area, one right and one scope of the caller, and it raises no other letter and no other area | Legacy RWB-AD-006 AC1; TSD P4 v3 T3.1 (DF-REF-038, DF-REF-042, DF-REF-043); FSD P4 v3 AC-ALT-P4-009-01 |
| BR5 | The grant ends at the earlier of the window hours from its activation and the end of the bank IAM group membership, and the window hours are parameter data. The value in force is 4 hours | FSD P4 v3 AC-ALT-P4-009-01; ASM-1492 |
| BR6 | A grant is in force only while its state is `ACTIVE` and `now` is before its window end. The clock is the authority, so no job and no person is needed for the grant to end, and a lost settle cannot extend it | Legacy RWB-AD-006 AC3; ASM-1496 |
| BR7 | Every action taken while the grant is in force carries the grant id and the incident reference, on the session, on the authorisation call and on the entry the access-log writer records | Legacy RWB-AD-006 AC1; FSD P4 v3 AC-ALT-P4-009-01 |
| BR8 | A caller holds at most one active grant. A second activation answers 409 with MSG-GEN-004 and the same request with the same `Idempotency-Key` returns the first answer | FSD P4 v3 AC-EXC-P4-007-05; RWB-P4-AD006-DB constraint |
| BR9 | The activation needs Platform administration C and the read needs R, with an active role on every call; a missing role is 401 with MSG-P4-001 and a missing letter is 403 with MSG-P4-002 | TSD P4 v3 T6.1 and API-P4-013; FSD P4 v3 VR-P4-001-1 |
| BR10 | Every activation and every refusal writes one local decision-record entry through the library of DP-03 on `rwb.decision-record.v1`, and where the entry cannot be written the activation is not stored | DP-03; FSD P4 v3 AC-EXC-P4-007-07; MSG-P7-003 |
| BR11 | No `rwb.access.*` event is published for a grant: a grant is session state and not a policy change, and the only message is the library's decision-record entry | Architecture v5 slides 14, 20 and 43; ASM-1495 |
| BR12 | The grant is one row of `rwb_access` read and written through the per-service login, and no statement of this story names a table outside `rwb_access` or the read-only ACE views | DP-01; DP-02; ownership map |

Where each rule sits in the target: BR1 to BR3 are the check set that runs before the write, so a refused activation stores nothing. BR4 is the bound of the grant, resolved against the `permission` and `role` rows of the caller in one hop. BR5 and BR6 are the window on the row and the time predicate of the guard. BR7 is the guard's call context and the access-log writer of RWB-P4-E1039-APP. BR8 is the partial constraint of RWB-P4-AD006-DB and the idempotency store of the library. BR9 is the guard of RWB-P4-E1037-CON. BR10 is the library and the outbox of the service template. BR11 is the event rule of the architecture. BR12 is the module map and the boundary test.

### 9. State transitions

None for a case, a task or a session. The states of this story are the states of a grant.

| From | Event | Condition | To |
|---|---|---|---|
| No grant | An activation passes every check and the entry is written | An open incident, an approval reference, a valid area, right and scope, a reason of at least 20 characters and a valid window | `ACTIVE` from the activation time to the window end |
| No grant | An activation fails a check or the entry cannot be written | Any failed check, or a 503 from the record library | No row; one refusal entry |
| No grant | A second activation arrives with a different key while a grant is in force | The constraint of the database or the check of the service | No row; 409 with MSG-GEN-004 |
| `ACTIVE` | `now` reaches the window end | The clock alone; no call and no person | Out of force at once; the row settles to `ENDED` on the next read, session read or authorised call |
| `ACTIVE` | The end operation is called before the window end | The caller holds Platform administration C | `ENDED` with an ended time; the caller's next call uses its own letters |
| `ACTIVE` | The end operation repeats on the same `Idempotency-Key` | None | The first answer; no second end entry |
| `ENDED` | Any later call | None | The caller is authorised on its own letters only; the grant is never reactivated |
| `ENDED` | A new activation for a new incident | A new approval and a new window | A new grant row; the ended grant keeps its rows |

The vocabulary is `ACTIVE` and `ENDED` and no third state is stored: a refused request is a refusal entry and not a grant row, which is why a refusal cannot be mistaken for a grant that once existed. The break-glass marker is not a state: it is the `ACTIVE` grant's reference carried on the session and on every entry of the window, and it disappears when the state becomes `ENDED`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the per-service login, DP-02) | Answers the activation, the end and the read, runs the checks, computes the window, writes the entry and settles an expired grant |
| RW-SECADM, security administrator | CRUDA in Platform administration (TSD P4 v3 T6.1): approves the request in the bank IAM and activates or reads a grant. The legacy story names the security administrator as the approver |
| RW-PLATADM, platform administrator | CRUD in Platform administration: activates a grant for an incident and reads it, which is the actor of the legacy story statement; it cannot approve its own request, because the approval is the IAM's |
| RW-AUDIT, internal audit | R in Platform administration: reads the grants and their entries. Writes nothing |
| RW-COMPLY, Compliance and PDPA officer | RU in Platform administration: reads the grants and reviews their use, which is FEAT-ACA-10; a grant is not edited by Compliance, and the end of a grant is the platform administrator's |
| RW-DATASTEW, RW-COE and every other role | R in Platform administration at most: reads a grant through the read operation where its role holds R, and activates nothing |
| The bank IAM (Entra ID) | Holds the group `RWB-SIT-BREAKGLASS`, approves the request as an IAM request and ends the membership, which bounds the window. The IAM is not a role of the Workbench |
| The incident register | Owns the open state of the incident. Its owner is **Not specified in the source documents (GAP-0797; ASM-1491)** |
| No delegation of authority level applies | A grant is not a credit decision, and no limit of `delegation_limit` is read |

The legacy Permission checks table gives this story the Platform administration right R and six roles that hold it (RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM), and the legacy Endpoints table gives it `GET monolith-base/admin/access-log` with that right. Neither is the grant: the access-log read and its right are RWB-P4-E1039-APP's and RWB-P4-AD007-APP's, and the activation needs the C letter that TSD P4 v3 API-P4-013 declares, because it creates a row. The R row of the legacy table stays as the right of the read operation of this story. The two are reconciled in the gap row and the assumption (GAP-0797; ASM-1494).

The database login is the per-service login of the service baseline (DP-02), and this story adds no grant. The bank IAM's own group membership and approval workflow are outside the Workbench.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| Not specified in the source documents (GAP-0799; ASM-1493) | `break_glass_grant` | grant_id | Written on activation; read by the end and the read |
| Not specified in the source documents (GAP-0799; ASM-1493) | `break_glass_grant` | actor_user_id (USER_REF) | Written from the session; read for the guard and the read |
| Not specified in the source documents (GAP-0799; ASM-1493) | `break_glass_grant` | incident_reference | Written on activation; read by every answer and carried on the marking |
| Not specified in the source documents (GAP-0799; ASM-1493) | `break_glass_grant` | iam_request_id and the approver reference | Written on activation from the request; read by the read operation |
| DF-REF-042 | `break_glass_grant` value of `permission` | capability_area (LOV-CAPABILITY, 14 areas) | Written on activation; validated against the list |
| DF-REF-043 | `break_glass_grant` value of `permission` | right_code (one of C, R, U, D, A or a dash) | Written on activation; validated against the letters |
| DF-REF-038 | `break_glass_grant` value of `role` | scope_code (LOV-SCOPE: OWN, TEAM, REGION, ALL) | Written on activation; validated against the list |
| Not specified in the source documents (GAP-0799; ASM-1493) | `break_glass_grant` | reason (text, at least 20 and at most 1000 characters) | Written on activation; read by the read operation and by the review of RWB-P4-E1039-APP |
| Not specified in the source documents (GAP-0799; ASM-1493) | `break_glass_grant` | starts_at, ends_at and the ended time | Written on activation and on the settle or the end; read by the guard on every call |
| Not specified in the source documents (GAP-0799; ASM-1493) | `break_glass_grant` | state (`ACTIVE`, `ENDED`) | Written on activation, on the settle and on the end; read by the guard |
| DF-REF-034 to DF-REF-037, DF-REF-040, DF-REF-041, DF-REF-044 | `role`, `permission` | role_code, role_name, role_class, role_id, matrix_version | Read: the role and the Platform administration letters of the caller. Never written here |
| DF-DEC-003, DF-DEC-014, DF-DEC-016, DF-DEC-030 | the local decision record of DP-03 | decision code (`AC-BGON`, `AC-BGREF`, `AC-BGOFF`), the actions, the decided time, the actor | Written through the decision-record library; no field is invented here |
| Not specified in the source documents (GAP-0797; ASM-1491) | the incident register | the open state of the incident | Read through the incident-status port, with a Day-1 stub; no field is copied into `rwb_access` beyond the reference |

One value the sources do not fix is carried as a placeholder. The grant table has no row in the ownership map and no row in TSD P4 v3 T3.1, so it has no field ids and no physical shape in the sources — **Not specified in the source documents (GAP-0799; ASM-1493)**; the columns are those of RWB-P4-AD006-DB and its working decision. The incident register's owner and its field set are **Not specified in the source documents (GAP-0797; ASM-1491)**.

**No section of this story stores a personal value beyond the actor reference and the free-text reason.** The actor is a staff user reference, the incident is a reference, the area, the right and the scope are codes, and the reason is free text that the application bounds and the review of RWB-P4-E1039-APP reads. No name, no e-mail address and no identity number is written, logged or published.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`. `POST /admin/break-glass-grants` is API-P4-013 in TSD P4 v3 appendix T-A (right C of Platform administration, `Idempotency-Key`, errors 401, 403, 409, 422 and 503). The end and read operations have no row in the ownership map and none in TSD P4 v3 appendix T-A, so their paths, their rights and their answers are this revision's own decision — **Not specified in the source documents (GAP-0798; ASM-1494)**.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/break-glass-grants` | Activate a grant: the open incident, the IAM approval reference, the area, the right, the scope, the reason and the window. Answer `BreakGlassGrant` | Platform administration C (API-P4-013) | `Idempotency-Key` header; the same key returns the first answer |
| POST | `/api/recovery/access/v1/admin/break-glass-grants/{grantId}/end` | End a grant before its window, with the ended time and the `AC-BGOFF` entry | Platform administration C (this revision's decision) | `Idempotency-Key` header; a repeated end returns the grant as it stands |
| GET | `/api/recovery/access/v1/admin/break-glass-grants/{grantId}` | Read one grant: its actor, incident, area, right, scope, reason, window, state, approver and entry reference | Platform administration R (this revision's decision) | Not applicable, read only |

Errors for all three: 401 no session or no Workbench role (MSG-P4-001), 403 no right (MSG-P4-002), 404 unknown grant (MSG-GEN-004), 409 a second active grant or a repeated key answered differently (MSG-GEN-004), 422 a missing or invalid field (MSG-GEN-001) or a length outside its bounds (MSG-GEN-002), 503 the record entry not written (MSG-P7-003) or the incident register not answering. The three operations are the grant lifecycle; the access-log read `GET /api/recovery/access/v1/admin/access-log` (API-P4-008) is RWB-P4-E1039-APP's and RWB-P4-AD007-APP's and is not restated here.

The session read `GET /api/recovery/access/v1/me/session` (API-P4-012) is the service's own operation of RWB-P4-E1019-APP and RWB-P4-E1037-CON. This story fills its `breakGlass` field from the grant, and the field is contracted by RWB-P4-AD006-CON; the operation itself is neither restated nor changed here (ASM-1495).

#### 12.2 REST operations consumed

None. The activation, the end and the read are answered from `rwb_access` and from the incident-status port; no other service is called on the caller's thread, and the one-hop budget of DP-11 is not spent. The open-incident fact is read through `IncidentStatusPort`, whose adapter is a Day-1 stub because no source names the incident register or its contract — **Not specified in the source documents (GAP-0797; ASM-1491)**. The `v_ace_*` views are not read by this story: it needs neither a party nor an account, only the incident reference.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library, consumed by P7 | Entry id, decision code (`AC-BGON` for the activation, `AC-BGREF` for a refusal, `AC-BGOFF` for the end and for the settle), the actor reference, the incident, the area, the right, the scope, the window and the time; written by the library of DP-03, not by this story's own writer |

No `rwb.access.*` event is published for a grant, and no third event name is invented. Architecture v5 slide 14 gives `rwb-access` exactly two business events, `AccessPolicyChanged` and `DoaLimitChanged`, and slide 43 publishes them to all services for a cache refresh; **a break-glass grant is session state and not a policy change**: it changes no permission row, no scope and no delegation limit, and it ends by its own clock, so a cache that refreshed on it would cache an entitlement that has already gone. The two readers of a grant are the authorisation guard and the session read, both inside this service and both reading `rwb_access` on the call (ASM-1495).

Both messages use the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype (Architecture v5 slide 11). No message carries a name, an e-mail address, an identity number or a case fact.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), the grant state is read from `rwb_access` on each call, and this story subscribes to no topic and writes no inbox row.

#### 12.5 Workflows and activities

None. The activation, the end and the read are synchronous REST answers in the caller's thread, and the settle of an expired grant runs inside the same transaction as the read that observes it. No workflow is started, no activity is registered on the `rwb-access` queue and no signal is sent — deliberately, because the clock and not a workflow is the authority over the window (BR6).

#### 12.6 Schedules

None. No Temporal Schedule sits in this story: the window end is a value on the row, the guard applies it on every call and the settle happens on the next read, so nothing has to run on a clock. The six-monthly access review list (JOB-18, Architecture v5 slide 44) is RWB-P4-AD008-APP's, and Architecture v5 slide 14 gives `rwb-access` that one Schedule.

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| `break_glass_grant` | `rwb_access` | P4, in `rwb_access`; no row in the ownership map, this key's own working decision (GAP-0799; ASM-1493) | Writes the activation, the settle and the end; reads the guard's predicate |
| `role` | `rwb_access` | P4 | Reads the role and its default scope (DF-REF-034 to DF-REF-038); never writes |
| `permission` | `rwb_access` | P4 | Reads the caller's Platform administration letters and the capability areas (DF-REF-040 to DF-REF-044); never writes |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_access` | PLT library | Created by the service baseline; the record library writes the outbox row of an entry, and this story writes none by hand |
| `masking_rule`, `role_conflict`, `delegation_limit` | `rwb_access` | P4 | Not read and not written by this story |
| the access log of RWB-P4-E1039-DB | `rwb_access` | P4, RWB-P4-E1039-DB | **Not read and not written by this story.** The writer of RWB-P4-E1039-APP stamps the grant reference on the entry it records |
| `decision_log_entry`, `approval` | `rwb_decision` | P7 | Not read and not written; the central ledger is P7's and the local entry is the library's |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | `rwb_case` | P3 | **Never read by SQL**; the lists travel as codes and no parameter is read by this key |
| `partner_user` | `rwb_partner` | S9 | Not read and not written |

No foreign key crosses a schema and no statement in this story names a table outside `rwb_access` or a read-only ACE view. The incident reference is a value and never a key.

#### 12.8 Contract fakes

| Fake | Serves | Used for |
|---|---|---|
| Grant contract fake (RWB-P4-AD006-CON) | The three paths of 12.1 with a grant in force, an ended grant and the refusals | AC1, AC2 and AC3, and every test that activates, ends or reads a grant |
| Incident-status stub | The incident register: one incident open, one incident closed, and one reference that matches no incident | AC1 and AC2 |
| Decision-record fake (RWB-PLT-E1027-CON) | The entry append, the hash-chain check and the 503 with MSG-P7-003 | AC1, AC2 and AC3 |
| Access-log writer fake (RWB-P4-E1039-APP) | The entry of an action with the grant id and the incident reference it carries | AC1 |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 3 operations under `/api/recovery/access/v1` | 0 | OpenAPI 3.1, one hop, 2 s timeout; the incident check is a port and not a service call on this thread |
| Kafka | 1 published (the library's) | 0 | `rwb.decision-record.DecisionRecorded.v1`; no `rwb.access.*` event for a grant |
| Temporal | None | None | No workflow, activity or Schedule in this story |
| File | None | None | No file in this capability |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.breakglass`, module `breakglass`, in the service root `th.co.scb.ace.workbench.recovery.access`. Service base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1`, Temporal task queue `rwb-access` (not used here).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the entry of every activation, every refusal and every end, and the outbox row that publishes it. DP-05 is applied as a **bounded** read: this capability reads no ACE view, because it needs no party and no account, and it states that rather than leaving it open; the ACE group reference the emergency path relies on is the bank IAM's, read by the IAM and not by this service. DP-13 is the base of the three operations. DP-19 is the composite route that serves SCR-43 with the grant read and the access-log read of RWB-P4-E1039-APP.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `BreakGlassChecks` | Service | The checks of BR1 to BR4 and BR8 over a posted activation: the incident, the approval, the area, the right, the scope, the reason bounds and the window bounds |
| `BreakGlassWindow` | Service | Computes the window from the activation time and the window hours, bounded by the group end; no hour is a constant |
| `IncidentStatusPort` and its Day-1 stub adapter | Client | Answers whether the incident reference is open; the adapter is replaced when the incident register's owner is fixed (GAP-0797; ASM-1491) |
| `BreakGlassGrantRepository` | Repository | Writes the grant, reads it by id and by actor, applies the guard predicate and settles an expired row |
| `BreakGlassService` | Service | Assembles the activation, the end and the read; computes the window; settles an expired grant inside the read transaction |
| `BreakGlassGuardExtension` | Service | Extends the guard of RWB-P4-E1037-CON: reads the caller's grant, adds the area and the right it covers, and passes the grant id and the incident on the call context |
| `BreakGlassRecorder` | Service | Writes the `AC-BGON`, `AC-BGREF` and `AC-BGOFF` entries through the library of DP-03 and the outbox row that publishes them |

**Database and migrations**

- Writes `break_glass_grant` in `rwb_access` only; the table, its constraints, its indexes, its retention and its grant are RWB-P4-AD006-DB's and this story applies no migration of its own.
- The guard predicate is `state = 'ACTIVE' and now() < ends_at`, served by the index the DB story creates; the settle is one `UPDATE` of the row in the same transaction as the read that observed it.
- A grant is written once and never rewritten beyond its state and its ended time; the reason, the incident, the area, the right, the scope and the window are immutable after the activation.
- DB access uses the per-service rwb-access login of the service baseline (DP-02). No grant on `rwb_case`, on `recovery` or on `public` is added by this story.

**Configuration and reference data**

- The window hours, the incident pattern and the reason bounds are data; the value in force for the window is 4 hours (FSD P4 v3 AC-ALT-P4-009-01) and the reason floor is 20 characters (legacy AC1). The parameter codes are **Not specified in the source documents (GAP-0797; ASM-1492)** and **Not specified in the source documents (GAP-0797; ASM-1497)**.
- The capability areas, the letters and the scopes are codes of `LOV-CAPABILITY`, the letters of `permission` and `LOV-SCOPE`; no area, letter or scope is enumerated in code.
- No feature switch: the emergency path is guarded by the C letter and by the IAM approval, not by a flag.

**Build steps**

1. `IncidentStatusPort` with its Day-1 stub and the failing fixture "no open incident"; test AC2.
2. `BreakGlassChecks` with one check per rule and a failing fixture for each: an absent incident, a closed incident, an absent approval, a reason of 19 characters and one of 1001, an unknown area, an unknown letter, an unknown scope and a window of zero; test AC2.
3. `BreakGlassWindow` on a fixed clock with the value in force: activation at 10:30 gives an end at 14:30, and a group end at 18:00 does not move it; test AC1.
4. `BreakGlassGrantRepository` and `BreakGlassService` with the activation, the read and the settle; test AC1 and AC3.
5. `BreakGlassGuardExtension` over the guard of RWB-P4-E1037-CON: an action inside the window is allowed and marked, the same action one minute after the end is refused with MSG-P4-002; test AC1 and AC3.
6. `BreakGlassRecorder` with the three decision codes, the outbox row and the forced failure that answers 503 with MSG-P7-003; test AC2.
7. The end operation with its idempotency and the 409 of a second activation; test AC3 and AC2.
8. The session field: `GET /me/session` answers `breakGlass` while the grant is in force and omits it after the end; test AC1 and AC3.
9. The boundary check: no statement names a `public` table, the access-log table of RWB-P4-E1039-DB or a table of another service.

**Done when.** The tests in section 16 pass; an activation with an open incident, an approval reference and a reason of at least 20 characters answers an `ACTIVE` grant with its window and one `AC-BGON` entry; an activation with no open incident is refused with one `AC-BGREF` entry and no row; an action inside the window is allowed and carries the grant and the incident; the same action after the window end is refused with MSG-P4-002 with no action by anyone; the grant settles to `ENDED` on the next read with its `AC-BGOFF` entry; and no statement in the service names a table outside `rwb_access`.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. | The guard, on all three operations |
| MSG-P4-002 | The caller holds no Platform administration C for the activation or the end, or no R for the read; or a call arrives after the window end without the letter the action needs | You cannot {action} here. Your role does not include it. | The guard, on all three operations and on the action of a caller whose grant has ended |
| MSG-P4-004 | A grant of the caller is in force | Emergency access is on until {time}. Every action is recorded. | The session read and the banner of SCR-43 |
| MSG-GEN-001 | A required field is empty, the incident is not open, the approval reference is unknown, or the area, the right or the scope is not a value of its list | Enter {field}. | The checks of this story, as a 422 with the field and the row |
| MSG-GEN-002 | The reason is shorter than 20 or longer than 1000 characters, or the window is outside its bounds | {field} must be between {min} and {max}. | The checks of this story, as a 422 with the field and the two bounds |
| MSG-GEN-004 | A second activation arrives while a grant is in force, a repeated key is answered differently, or the grant asked for does not exist | Someone else changed this record. Reload it to see their change. | The activation and the two reads |
| MSG-P7-003 | The decision-record entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The activation, the refusals and the end, through the library of DP-03 |

Every error is an RFC 9457 problem response with `messageId` set and `detail` carrying the text with its placeholders filled. For MSG-P4-002 the {action} value names the action the caller tried — "activate emergency access", "end emergency access" or "read emergency access" — and never a case fact or another person's entitlement. For MSG-GEN-002 the {min} and {max} values are 20 and 1000 for the reason and the bounds in force for the window, so a business person can read the refusal without reading the code.

The refusal that has no legacy message of its own is the closed incident: FSD P4 v3 AC-EXC-P4-007-02 gives MSG-GEN-001 for a missing incident reference and MSG-GEN-002 for a short reason, and no source fixes the text for an incident that exists and is not open. The refusal therefore reuses the field-level answer with MSG-GEN-001 naming `incidentReference`, and the text for that condition is **Not specified in the source documents (GAP-0797; ASM-1491)**.

### 15. Screens and states

No screen is built by this story. SCR-43 Roles and access shows the roles, their permissions, the group mapping, the access log and the break-glass grants, and the platform administrator, the security administrator and internal audit read it there; it is served by the gateway-bff composite route of DP-19, which calls the grant read of this story and the access-log read of RWB-P4-E1039-APP in parallel, one hop each. The screen field list, the column order and the merge are the screen owner's, and this story returns the grant rows and the session field only.

| Screen | State | What the operator sees |
|---|---|---|
| SCR-43 Roles and access | List | The grants of the caller and of the estate that its letter reaches: grant id, incident, area, right, scope, start, end and state |
| SCR-43 Roles and access | Activate | The form of an activation: incident, IAM request, area, right, scope, reason and window, with the checks answered field by field |
| SCR-43 Roles and access | Active | MSG-P4-004 with the end time, on every screen of the caller: "Emergency access is on until {time}. Every action is recorded." |
| SCR-43 Roles and access | Activated | The written grant with its window, its state and the reference of its `AC-BGON` entry |
| SCR-43 Roles and access | Ended | The grant with its state `ENDED`, its ended time and the reference of its `AC-BGOFF` entry; MSG-P4-004 is gone |
| SCR-43 Roles and access | Refused | MSG-P4-002 or MSG-P4-001, or the field-level 422 of a check, with no grant |
| SCR-43 Roles and access | Access log | The entries of the window, each carrying the grant id and the incident, read through the access-log operation of RWB-P4-E1039-APP on the same composite route |
| SCR-43 Roles and access | Not available | MSG-P7-003 when the record cannot be written, with the retry advice of the message |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-006-01 | AC1 | End to end | Legacy test "Granted with an incident": the incident `INC0004521` is open, the IAM request `IAM-778812` is approved by the security administrator, the activation at 10:30 carries the area `CASE_RECORD`, the right `U`, the scope `ALL`, a reason of 46 characters and a window of 4 hours; the grant is `ACTIVE` until 14:30, one `AC-BGON` entry is written, an action at 14:20 is allowed and carries the grant and the incident, and MSG-P4-004 shows 14:30 |
| TC-AD-006-02 | AC2 | End to end | Legacy test "Refused without an incident": the incident register answers no open incident for the reference posted; the activation is refused with 422 and MSG-GEN-001 naming `incidentReference`, no grant row is written and one `AC-BGREF` entry with reason `NO_OPEN_INCIDENT` is on `rwb.decision-record.v1` |
| TC-AD-006-03 | AC3 | End to end | Legacy test "Ends on its own": a grant active from 10:30 to 14:30 on a fixed clock; no call is made until 14:31, when the same action is refused with MSG-P4-002 on the caller's own letters, no person or job having acted; the next read settles the row to `ENDED` with one `AC-BGOFF` entry |
| TC-AD-006-04 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002": `RW-PHONECOL` with no Platform administration letter calls the activation, the end and the read; 403 with MSG-P4-002 on each, one refusal entry each and no grant written |
| TC-AD-006-05 | Principle 5 | NFR | Legacy test "A forced decision log write failure stops the action with MSG-P7-003": the decision-record write forced to fail on an activation; 503 with MSG-P7-003, no grant row written and the state of any earlier grant unchanged |

The five legacy test cases are kept with their IDs and their legacy Covers values; the legacy test name is written in the Data column and the Level column follows Template and Rules §R7.2, where the legacy level Access maps to Component and the legacy Principle 5 row stays NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The ITG copy of the set is RWB-ITG-AD006-ITG's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the window hours, the incident pattern and the reason bounds are data, the value in force is the 4 hours of the FSD, and a test proves that a different window needs no build (BR5).
- No personal data anywhere: the actor is a staff user reference, the incident is a reference, and no test row, log, event or prompt holds a name or an e-mail address; the only free text is the reason, which the application bounds and the review reads.
- No read of another schema (DP-01): `lov_value`, the reference tables, the parameter tables, `decision_log_entry`, `partner_user` and the access-log table of RWB-P4-E1039-DB are never read by SQL.
- ACE data only through the owner's contract or the service's own `v_ace_*` view (DP-05): this capability reads no ACE view at all, and the ACE group the emergency path depends on is the bank IAM's.
- One writer for a grant: only the activation writes one, and after it only the state and the ended time change (BR6).
- Default deny on every call: a missing role resolves to 401 and a missing letter to 403 with MSG-P4-002, never to allow (BR9).
- The clock is the authority over the window: a grant out of its window is never read as an entitlement, whatever its row says, and no job or person is needed for it to end (BR6).
- One event rule: no `rwb.access.*` event for a grant, and the only message is the library's `rwb.decision-record.DecisionRecorded.v1` (BR11).
- The grant is one row of `rwb_access` under the per-service login, and no statement names a table outside the schema (BR12).

### 18. Traceability

The Work Package carries the requirement list of this key as empty, and TSD P4 v3 T8 maps REQ-ACA-008 to the sign-in story RWB-E1-022; FSD P4 v3 records REQ-ACA-008 as "A break-glass path exists for an emergency, needs its own approval, and writes to the access log", must, first in E1, with the features FEAT-ACA-09 (use break-glass access with an incident reference) and FEAT-ACA-10 (review break-glass use). This slice answers the first half of that requirement — the path and its own approval — and RWB-P4-E1039-APP answers the access log it writes to.

| Feature | Where this story answers it | Test cases |
|---|---|---|
| FEAT-ACA-09, use break-glass access with an incident reference | The activation with its open incident, its approval reference, its reason and its window (sections 1, 4, 8, 12.1) | TC-AD-006-01, TC-AD-006-02 |
| The own-approval rule of REQ-ACA-008 | The IAM request reference and the approver reference on the grant; the caller cannot approve its own request (BR2, section 10) | TC-AD-006-01 |
| The self-expiry the legacy criterion asks for | The clock as the authority and the settle on the next read (BR6, section 9) | TC-AD-006-03 |
| The default deny rule and the recorded refusal | MSG-P4-001 and MSG-P4-002 with the decision-record entry (sections 8, 14) | TC-AD-006-02, TC-AD-006-04 |
| The record-before-change rule | The entry of DP-03 written in the same transaction as the grant (BR10, section 14) | TC-AD-006-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P4-AD006-CON | Contract | H: the activation, end and read contract, the two schemas, the session field, the expiry rule and the fakes |
| RWB-P4-E1039-APP | App development | H: the access-log writer that stamps the grant and the incident, and the administration surface that lists the grants |
| RWB-P4-AD006-DB | ACE DB | X, tracked: the grant table, its constraints, its indexes, its retention and the per-service login |
| RWB-PLT-E1027-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library and the gateway-bff composite route |
| RWB-P4-E1037-CON, RWB-P4-E1037-APP, RWB-P4-E1019-APP | Contract, App development | The guard this story extends, the permission matrix, the role catalogue and the session read |
| RWB-P4-AD007-APP, RWB-P4-E1039-CON | App development, Contract | The access-log search and export, and the contract of the access log; this story neither restates nor changes them |
| RWB-P4-E1022-APP | App development | The sign-in that resolves the caller's roles and the session the grant rides on |
| RWB-ITG-AD006-ITG | Integration | The cross-service proof that a marked action reaches the access log |

| Legacy reference | Where it is kept |
|---|---|
| The story statement (emergency access beyond the role, tied to an open incident, ending on its own) | Sections 1, 2, 8 (BR1, BR6) |
| Legacy AC1, AC2 and AC3 with `20 characters` | Section 7 |
| The Data table: `role` DF-REF-034 to DF-REF-038 | Section 11 |
| The permission check Platform administration R and the six roles that hold it | Section 10 |
| The validation and messages MSG-P4-004, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| Screen SCR-43 Roles and access | Section 15 |
| Legacy test cases TC-AD-006-01 to TC-AD-006-05 | Section 16 |
| The legacy Endpoint `GET monolith-base/admin/access-log` (API-P4-008) | Section 19: it belongs to RWB-P4-E1039 and RWB-P4-AD007-APP, and this story rewrites nothing of it |

### 19. Out of scope

- The access-log writer, the access-log read and the administration screen that lists the break-glass grants: RWB-P4-E1039-APP, with its contract RWB-P4-E1039-CON and its database RWB-P4-E1039-DB.
- The access-log search by person, date, event and capability area, and its export: RWB-P4-AD007-APP and RWB-P4-AD007-CON.
- The legacy Endpoint `GET monolith-base/admin/access-log` (API-P4-008): it belongs to legacy RWB-E1-039 and therefore to RWB-P4-E1039-APP, and its search and export are RWB-P4-AD007-APP's. This story neither restates nor rewrites it, and it publishes no operation of the access log.
- The break-glass review by Compliance (FEAT-ACA-10): the review reads the grants and the entries through SCR-43 and the access-log read; no separate story of this key is created for it, and the read it needs is RWB-P4-E1039-APP's.
- The grant table, its columns, its constraints, its indexes, its retention and the per-service login: RWB-P4-AD006-DB.
- The sign-in, the group claim of the token, the multi-factor check and the separation-of-duty check: RWB-P4-E1022-APP and RWB-P4-AD005-APP.
- The role and permission rows, the masking rows, the role conflicts and the guard: RWB-P4-E1019-APP, RWB-P4-E1037-APP, RWB-P4-E1037-CON and RWB-P4-AD004-APP.
- The permission matrix and masking loads with their approval and rollback: RWB-P4-AD002-APP and RWB-P4-AD010-APP.
- The reference data itself — `lov_value`, `reference_row` and `reference_version` — and the parameter values of the estate: P3 rwb-case under the ownership map; this story consumes no parameter contract and holds no parameter row.
- The central decision ledger and its query: P7 rwb-decision; this story writes the local entry only.
- `partner_user`: S9 rwb-partner under the ownership map.
- The bank IAM's group administration, its approval workflow and the naming of `RWB-SIT-BREAKGLASS`: Entra ID and the bank IAM (INT-21), recorded in the legacy preconditions; the incident register and its open state are outside the estate until its owner is fixed (GAP-0797; ASM-1491).
- The Helm chart, the topic creation, the metrics, the alerts and the runbook of this capability: an OPS story.
- The integration harness and its evidence, and the `-ITG` copies of the test cases: RWB-ITG-AD006-ITG.
