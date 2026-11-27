# RWB-P4-E2036-APP Queue write interface for models and agents

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2036-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-036 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-AW |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2036-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-019, FR-P4-035) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-036 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E2036-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM), a risk and model risk officer (RW-RISK), and the model or agent that writes to a queue**, I want **the authority answer of `rwb-access` for a queue write by a non-human caller — who the writing model or agent is, which role and scope its service identity holds, which queues the write may target, whether the masking policy of the fields the write needs answers masked or clear, the refusal with its reason, and one access entry for every write** — so that **a model or an agent passes exactly the role and scope checks a person passes, an adapter gets that answer in one hop, and no queue, case, assignment or personal field is read or written outside its owner**.

Inside `rwb-access` this is the authority part of the legacy story RWB-E2-036, and nothing else:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables. First, the **placement admission** part of the service's existing `POST /api/recovery/access/v1/authorise`: the caller code, the caller type, the service identity behind it, the target queue and its team code, the case, the product group, the reason, the model or agent version and the field IDs the write needs, answered with admitted or refused, the reason code, the caller's role class, the role codes whose letters admitted the write, the scope, the matrix version, the masking version and one marker per field ID. Second, the **non-human part of `GET /api/recovery/access/v1/me/permissions`**, which answers the caller's own profile: its role codes, its role class, its scope, its letters per capability area, the matrix version in force and the queue targeting that follows from the scope.
- The placement itself is not built here. The placement record, the queue, the assignment method, the caseload cap, the overflow queue, the assignment and the refusal for a closed case, a case already in the queue or an open deviation stay in `rwb-case` (P3, RWB-P3-E2036-APP), and the caller-facing admission and forwarding operation, its replay and the approved callers list stay in `rwb-integration` (P2, RWB-P2-E2036-CON and RWB-P2-E2036-APP).
- The call is one hop: `rwb-integration` asks this service, this service answers from `rwb_access` alone, and the queue's team code, the case reference and the product group are **presented with the request** exactly as the case attributes are presented to the data-product answer of RWB-P4-E1016-APP. No operation of `rwb-case` is called and no queue, case or assignment row is read (DP-01, DP-11).
- The masking part is the same default-deny answer the service already gives: `clear` only where a `masking_rule` row for one of the caller's roles, that field ID and the masking version in force says `unmasked` true, and `masked` otherwise, including where no row exists. A placement carries no personal value, so a caller that presents no field ID receives no clear marker.
- The data-product right the write needs is the Queue and allocation letter and the masking markers; the access row on a data product that a **read** needs is that same operation's data-product part, owned by RWB-P4-E1016-APP, and this story restates neither the row nor the table, which is P1's.
- Every admission, allowed or refused, appends one access entry before the answer leaves the service, through the access-entry writer of RWB-P4-E1039-APP with decision code `AC-READ` or `AC-DENY`, carrying the caller code, the caller type, the version, the target queue, the case, the matrix version and the reason code, and no personal value (DP-03).
- The feature flag `rwb.casewf.queue-placement`, its replay window and the approved callers list are not this service's: the flag and the replay are `rwb-integration`'s (RWB-P2-E2036-CON), and the list is the `rwb-case` parameter and reference-data row under `rwb.casewf.placement.approved-callers` read by `rwb-integration` through DP-06 and DP-07. This story adds no flag of its own and answers the same whether the flag is on or off.

### 2. Business rationale

Model scores and agent findings reach the queues today through a weekly file that a person loads by hand. The legacy story removed the weekly step with one endpoint, and it wrote the one rule that makes the removal safe: a model or an agent passes **the same** access check as a person, under its own service identity, and its write is logged with its version (REQ-CWC-018; NFR-051; NFR-078; CTL-09). In the monolith that rule was a call to the common module's access check inside the placement handler; in the target the access check is `rwb-access`'s contract, and the placement handler is another service's. If the split left the check inside the handler, every caller would re-implement it, and the one thing an audit can rely on — that a non-human writer is authorised exactly as a person is — would become a property of the caller instead of a property of the platform.

This story is therefore the authority half of the legacy key and it is small on purpose: one admission answer, one profile read, one access entry. It puts three decisions in one place. **Identity**: a write by a model or an agent is resolved through the role of the service identity it runs under, and only a role of class `NON_HUMAN_ACTOR` may use it, so a person's token cannot place work through the model path. **Scope**: the legacy gives a service identity scope `All`, and this story answers the queue targeting from that one value rather than from a copy of the queue table, so `rwb-access` never needs `rwb-case`'s `queue` row. **Disclosure**: the masking markers of the fields the write needs come from the same policy that masks a screen, so a non-human caller cannot see more than the narrowest of its roles allows.

It meets REQ-CWC-017 (the write carries the case, the caller and the reason), REQ-CWC-018 (the same permission checks, a service identity, the version logged), REQ-CWC-019 (the flag is the caller's, and this answer does not depend on it) and REQ-CWC-020 (a model's work and a rule's work are one queue, so there is exactly one authority path and no model-only shortcut), and REQ-ACA-010 in full (agents run under service identities and are subject to the same role checks as people). It supports controls CTL-09 and CTL-06 and rule R-UNI-39: no admission proceeds unlogged, and an entry that cannot be written withholds the answer.

Three things no source fixes are carried as placeholders and not as invented values: the request and answer element set of the placement admission part and of the non-human profile read — Not specified in the source documents (GAP-0957; ASM-1689); the reason code vocabulary and the status each code answers with — Not specified in the source documents (GAP-0958; ASM-1690); and how a caller code is bound to a Workbench role, and to a team or region where the scope is narrower than `All` — Not specified in the source documents (GAP-0959; ASM-1691; GAP-0960; ASM-1692). The decision code of the access entry and the fields it carries are Not specified in the source documents either (GAP-0961; ASM-1693).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P2-E2036-CON | The published contract of the adapter that calls this answer: the placement on the integration base, the four legacy body fields, the Queue and allocation C expectation, the error mapping with MSG-P4-002, the replay rule, the approved callers list with the caller code and type, and the four contract fakes. That contract consumes `POST /api/recovery/access/v1/authorise` and signs off the wording of the right and the scope; it defines no part of the answer |
| RWB-P4-E1037-CON (same service, its own contract story) | The authorise contract itself: `POST /api/recovery/access/v1/authorise` and `GET /api/recovery/access/v1/me/permissions` on base `/api/recovery/access/v1`, the request and answer envelopes, the RFC 9457 problem detail shape, the guard library of DP-08 and its exemptions. This story adds a part to two existing operations and adds no path |
| RWB-P4-E1037-APP (same service, the baseline) | The `rwb_access` baseline: `role` (DF-REF-034 to DF-REF-039), `permission` (DF-REF-040 to DF-REF-044) and `masking_rule` (DF-REF-198 to DF-REF-204) exist with their dictionary rows, and the per-service login of DP-02 is in place |
| RWB-P4-E1019-APP (same service) | The role rows, the permission rows and the matrix version label in force: `PM-2026.11` at go-live and `PM-2026.12` from 1 December 2026, the role class `NON_HUMAN_ACTOR` on the service identities, and the letters of each role per capability area |
| RWB-P4-E1016-APP (same service) | The masking answer and the data-product part of `POST /authorise`: the marker per field ID at the masking version in force, the default-deny rule where no row exists, and the answer shape this story composes rather than restates |
| RWB-P4-E1039-APP (same service) | The access-entry writer: the append through the local decision-record library, the hash chain, the outbox row and the forced-failure behaviour. This story supplies the entry and the reason code and adds no second writer |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of every admission |
| RWB-PLT-E1037-CON | The guard library that carries this service's answer to the other services (DP-08), so `rwb-integration` caches the admission answer and refreshes it on `rwb.access.AccessPolicyChanged.v1` |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the contract of `rwb-case` (DP-07) for LOV-CAPABILITY, LOV-SCOPE, LOV-ROLE-CLASS and LOV-PRODUCT with the version in force; no capability area, scope value, role class or product group is a constant in code |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09) for the entry's outbox row |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15); this story adds no migration of its own |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19); no screen of this story is served through it |

Business preconditions carried from RWB-E2-036:

- The environment is SIT and matrix version `PM-SIT-02` gives the service identity `SY-AGENT` the letters `CRU` in the capability area `QUEUE_AND_ALLOCATION`, so a write is admitted on `C`. The production matrix `PM-2026.11` gives `SY-AGENT` the letter `R` only in that area, so a matrix version change by RW-SECADM is a precondition of the first live caller (legacy §3; TSD P4 v3 T6.1).
- The approved callers list holds caller `MDL-SYN-PRIORITY` of type `MODEL` for the service identity `SY-AGENT`, and it does not hold `MDL-SYN-UNLISTED`. The list is empty at go-live, an entry is requested by RW-COE and approved by RW-RISK before it is loaded, and the list is read by `rwb-integration` through DP-06 and DP-07, never by this story.
- Queue `MTG-BKK-PRI` of team `MTG-BKK` exists in `rwb-case` with method `ROUND_ROBIN`, caseload cap 150 and overflow queue `MTG-BKK-OVF`, and case `RW-2026-000501` is `NEW` with no owner and no open deviation. Every one of those values is `rwb-case`'s and arrives in the request as a presented value; this story holds none of them.
- Masking version `MASK-SIT-01` is in force in `masking_rule`. The label is the one the FSD uses for the SIT environment and no source fixes a production label.
- The two values `MODEL` and `AGENT` of the caller type are the approved callers list's, and the caller type is carried through this service and recorded; this service holds no list of caller types (GAP-0957; ASM-1689).
- Every user, caller code, case number and queue in the tests is synthetic; no production caller, case or payload is copied into a test, a fixture or a prompt, and no name of a person appears anywhere.
- No approval is required to build against a Draft contract: the baseline is Draft (realignment v1) and this part of it is frozen when the adapter's contract tests pass.

### 4. Flow

1. `rwb-integration` (P2), in its admission service, has already applied its own checks in its own order: the feature flag, the replay lookup, the field validation and the approved callers check. It calls `POST /api/recovery/access/v1/authorise` on `rwb-access` with `callerCode`, `callerType`, `targetQueueId`, `targetQueueTeamCode`, `caseId`, `productGroup`, `reason`, `modelVersion` and `fieldIds`, under its own service identity and the workload token of the caller.
2. `PlacementAuthorityController` reads the calling identity from the token and the guard library answers first: a caller without the right to ask the authorise operation is refused 403 with MSG-P4-002 before any row is read (DP-08). This is the calling service's right, not the subject's.
3. `CallerIdentityResolver` resolves the subject: the service identity presented for the caller is matched to a `role` row at the matrix version in force, and the role class is read. No role, or a role class that is not `NON_HUMAN_ACTOR`, is a refusal with reason code `CALLER_KIND` (BR4).
4. `MatrixVersionResolver` fixes the matrix version in force for the day of the call, so one answer names one version whole and never a mixture of two (BR10).
5. `PermissionReader` unions the letters of the caller's roles in the capability area `QUEUE_AND_ALLOCATION`. No `C` letter is a refusal with reason code `RIGHT_NOT_HELD`, and the answer names the area, the letter asked and the matrix version (BR2).
6. `CallerScopeService` reads the scope of the admitting role. The legacy gives a service identity scope `All`; where the scope is narrower, the queue targeting cannot be resolved from `rwb_access`, because no table binds a role to a list of teams or regions, and the refusal is `SCOPE_NOT_ALL` (BR3; GAP-0959; ASM-1691). Where the scope is `ALL`, every queue of `rwb-case` is targetable and the presented team code is recorded, not compared.
7. `PlacementAdmissionService` validates the four legacy request fields against the legacy lengths: `reason` 1 to 1,000 characters and `modelVersion` 1 to 40 characters, with `caseId`, `targetQueueId` and `callerCode` required. An empty required field is 422 with MSG-GEN-001 naming the field, a length out of range is 422 with MSG-GEN-002, and the product group is checked against LOV-PRODUCT with the version in force (BR6).
8. `MaskingAnswerService` of RWB-P4-E1016-APP resolves one marker per field ID at the masking version in force: `clear` only where a `masking_rule` row for one of the caller's roles, that field and that version says `unmasked` true, and `masked` otherwise, including where no row exists. A placement presents no field value, so a request with an empty `fieldIds` answers the masking version and no marker, and no marker is ever `clear` for a field the caller's roles do not hold an exception on (BR7).
9. The answer is 200 with `admitted` true, `callerType`, `roleClass`, `roleCodes`, `letters` for the area, `scope`, `matrixVersion`, `maskingVersion`, `productGroup` and `fieldMarkers`. The answer carries no case status, no owner, no queue method, no cap and no overflow queue: those are `rwb-case`'s and are answered by the placement (BR9).
10. A refusal answers 403 with an RFC 9457 problem detail, `messageId` MSG-P4-002, `reasonCode` and the values that make the refusal legible — the area, the letter asked, the matrix version and the scope — and nothing else. No limit, no holder, no queue list and no field value is returned in a refusal (BR11).
11. `AccessEntryWriter` of RWB-P4-E1039-APP appends one entry before the answer leaves the service: decision code `AC-READ` for an admission and `AC-DENY` for a refusal, the calling service identity, the caller code, the caller type, the model or agent version, the reason code, the target queue, the team code, the case, the product group, the matrix version, the masking version, the field IDs marked and the time. The entry carries no name, no e-mail address and no personal value (BR5).
12. Where the entry cannot be written the answer is not returned: the call fails with 503 and MSG-P7-003, because an access entry that is missing cannot be reconstructed and no admission may proceed unlogged (R-UNI-39; FSD P4 v3 A2.7 exception AC-EXC-P4-007-03).
13. `GET /api/recovery/access/v1/me/permissions` answers the same subject from the same rows: the role codes, the role class, the scope, the letters per capability area, the matrix version and the queue targeting (`ALL` with every queue targetable, or the reason that it is not). The two operations answer from one reader, so a profile read and an admission never disagree.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The calling service identity holds no right to the authorise operation | 403 before any row is read, and the refusal is the guard's | MSG-P4-002 | AC2 |
| X2 | The caller code does not resolve to a role at the matrix version in force | Refused with reason code `CALLER_KIND`; nothing is admitted and no field is answered | MSG-P4-002 | AC5 |
| X3 | The caller resolves to a role whose class is not `NON_HUMAN_ACTOR` | Refused with reason code `CALLER_KIND`: a person's token cannot place work through the model path | MSG-P4-002 | AC5 |
| X4 | The caller's roles hold no `C` letter in Queue and allocation | Refused with reason code `RIGHT_NOT_HELD`, and the area, the letter asked and the matrix version are named | MSG-P4-002 | AC2 |
| X5 | The admitting role's scope is not `ALL` | Refused with reason code `SCOPE_NOT_ALL`; no queue is named in the answer, because the queue list and the team binding are not this service's | MSG-P4-002 | AC4 |
| X6 | A required field is empty | 422 naming the field, nothing admitted and no entry beyond the refusal | MSG-GEN-001 | AC6 |
| X7 | `reason` or `modelVersion` is outside its length | 422 naming the field and the bounds | MSG-GEN-002 | AC6 |
| X8 | The presented product group is not a value of LOV-PRODUCT at the version in force | 422 naming the field, nothing admitted | MSG-GEN-001 | AC6 |
| X9 | A presented field ID has no `masking_rule` row for any of the caller's roles | The marker is `masked`: default deny, never an error and never clear | None | AC7 |
| X10 | The access entry cannot be written | 503 and no answer; the admission is not given and nothing else is written | MSG-P7-003 | AC9 |
| X11 | The same admission arrives twice with the same values | Both are answered; each writes its own entry, because an admission is a read of the policy and not a state change. The one-placement rule is `rwb-case`'s and the replay is `rwb-integration`'s | None | AC8 |
| X12 | The caller asks this service for a queue row, a case status or an assignment | There is no such answer: the operation answers policy only and names none of those values | None | AC11 |

No exception path of this story changes a case, a queue, an assignment or a task: this service answers and records, and the state machines are `rwb-case`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P2-E2036-CON and its fake, the `rwb_access` baseline of RWB-P4-E1037-APP and the masking answer of RWB-P4-E1016-APP; no queue, case or assignment row and no `rwb-case` build is needed |
| Negotiable | The matrix version, the letters, the scope, the role class, the product groups and the masking rows are data; the element names and the reason codes are fixed here and confirmed at the contract review |
| Valuable | One authority answer makes a non-human writer pass the checks a person passes, and one access entry makes every write auditable |
| Estimable | Two extended operations, one resolver, one scope rule, one masking composition and one entry appender |
| Small | Fits two weeks with its tests; there is no screen, no workflow, no table and no migration of its own |
| Testable | Every criterion in section 7 is one automated test over synthetic role, permission and masking rows, with the placement and the approved callers list stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: The authority answer for a queue write by a model or an agent

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given matrix version "PM-SIT-02" is in force on 15 December 2026 and gives the service identity "SY-AGENT" the letters "CRU" in the capability area "QUEUE_AND_ALLOCATION"
    Given the "role" row of "SY-AGENT" carries role class "NON_HUMAN_ACTOR" and default scope "ALL"
    Given masking version "MASK-SIT-01" is in force and holds no "unmasked" row for the roles of "SY-AGENT"
    Given the rwb-integration contract mock returns placement "PL-1" for queue "MTG-BKK-PRI" of team "MTG-BKK" and case "RW-2026-000501"
    Given the approved callers list behind the mock holds caller "MDL-SYN-PRIORITY" of type "MODEL" for service identity "SY-AGENT" with version "1.4.0"

  Scenario: AC1 A model caller is admitted on the Queue and allocation C right (new, D-RCV-60)
    When the rwb-integration service identity calls POST /api/recovery/access/v1/authorise for callerCode "MDL-SYN-PRIORITY", callerType "MODEL", serviceIdentity "SY-AGENT", targetQueueId "MTG-BKK-PRI", targetQueueTeamCode "MTG-BKK", caseId "RW-2026-000501", productGroup "MORTGAGE", reason "High cure score", modelVersion "1.4.0" and an empty fieldIds
    Then the response is 200 with admitted true, callerType "MODEL", roleClass "NON_HUMAN_ACTOR", roleCodes "SY-AGENT", scope "ALL" and matrixVersion "PM-SIT-02"
    Then the answer names the capability area "QUEUE_AND_ALLOCATION" and the letter "C" that admitted the write
    Then the answer carries no case status, no owner, no assignment method, no caseload cap and no overflow queue
    Then one access entry is appended with decision code "AC-READ" and the caller code, the caller type, the version and the queue before the answer is returned

  Scenario: AC2 The same permission check a person passes refuses a caller that holds R only (new, D-RCV-60)
    Given matrix version "PM-2026.11" is in force and gives the service identity "SY-AGENT" the letter "R" only in the capability area "QUEUE_AND_ALLOCATION"
    When the same placement is asked for admission under "PM-2026.11"
    Then the response is 403 with message MSG-P4-002, reasonCode "RIGHT_NOT_HELD", capabilityArea "QUEUE_AND_ALLOCATION", right "C" and matrixVersion "PM-2026.11"
    Then one access entry is appended with decision code "AC-DENY" and the reason code, and nothing is admitted
    Then the rwb-integration contract mock returns that refusal to its caller as its documented 403 with MSG-P4-002, unchanged

  Scenario: AC3 The caller's own profile names the queues the write may target (new, D-RCV-60)
    When the service identity "SY-AGENT" calls GET /api/recovery/access/v1/me/permissions
    Then the response is 200 with roleCodes "SY-AGENT", roleClass "NON_HUMAN_ACTOR", scope "ALL", matrixVersion "PM-SIT-02" and the letters of each capability area in force
    Then the queue targeting is "ALL", so every queue of rwb-case is targetable
    Then the answer names no queue row, no queue code and no team code, because the queue table is rwb-case's
    Then a caller whose role class is "BANK_USER" is answered 403 with message MSG-P4-002 and no queue targeting

  Scenario: AC4 A scope narrower than All cannot target a queue (new, D-RCV-60)
    Given the "role" row of "SY-AGENT" at the matrix version in force carries default scope "TEAM"
    When the same placement is asked for admission
    Then the response is 403 with message MSG-P4-002 and reasonCode "SCOPE_NOT_ALL"
    Then the answer names no queue, no team and no queue list, because no row of rwb_access binds a role to a list of teams or regions
    Then one access entry is appended with decision code "AC-DENY" and reasonCode "SCOPE_NOT_ALL"

  Scenario: AC5 A caller that does not resolve to a non-human role is refused (new, D-RCV-60)
    Given the rwb-integration contract mock returns a placement that presents user reference "U-5100", whose role "RW-CASEOWN" carries role class "BANK_USER"
    When the admission is asked for that caller
    Then the response is 403 with message MSG-P4-002 and reasonCode "CALLER_KIND"
    Then no letter is read, no field is answered and no queue is named
    Then an unlisted caller code such as "MDL-SYN-UNLISTED" never reaches this operation, because the approved callers list is refused by the caller's own checks, and this service holds no copy of the list

  Scenario: AC6 A required field is empty and a field is out of range (new, D-RCV-60)
    When the admission is asked with no caseId
    Then the response is 422 with message MSG-GEN-001 naming the field caseId and nothing is admitted
    Then when the admission is asked with a reason of 0 characters the response is 422 with message MSG-GEN-002 naming reason with min 1 and max 1,000
    Then when the admission is asked with a modelVersion of 41 characters the response is 422 with message MSG-GEN-002 naming modelVersion with min 1 and max 40
    Then when the admission is asked with productGroup "HIRE_PURCHASE", which LOV-PRODUCT does not hold at the version in force, the response is 422 with message MSG-GEN-001 naming productGroup

  Scenario: AC7 No personal field is answered clear for a non-human caller (new, D-RCV-60)
    Given masking version "MASK-SIT-01" holds an "unmasked" row for field "DF-PTY-016" and role "RW-TEAMMGR" only
    When the admission is asked with fieldIds "DF-PTY-007" and "DF-PTY-016"
    Then the answer carries maskingVersion "MASK-SIT-01" and a marker "masked" for both field IDs
    Then when the same call presents no field ID the answer carries the masking version and no marker at all
    Then a placement answers no clear marker for any field the caller's roles do not hold an exception on, and it answers no field value, no rendering and no last four digits

  Scenario: AC8 Every admission writes one access entry with the caller and its version (new, D-RCV-60)
    When one admission is allowed and one is refused with reasonCode "RIGHT_NOT_HELD"
    Then two entries are appended, the first with decision code "AC-READ" and the second with "AC-DENY"
    Then each entry carries the calling service identity, the caller code, the caller type, the model or agent version, the target queue, the team code, the case, the product group, the matrix version, the masking version, the reason code and the time
    Then neither entry carries a name, an e-mail address or a personal value, and each is appended before its answer leaves the service
    Then a second admission of the same case with the same values is answered and appends a second entry, because an admission is a read of the policy and not a state change

  Scenario: AC9 An admission that cannot be recorded is not given (new, D-RCV-60)
    Given the access-entry writer of RWB-P4-E1039-APP is forced to fail
    When the admission is asked for callerCode "MDL-SYN-PRIORITY" and caseId "RW-2026-000501"
    Then the response is 503 with message MSG-P7-003 and no admission answer
    Then no case, queue or assignment is touched and the rwb-integration contract mock records the failure as its own 503 with MSG-P7-003

  Scenario: AC10 The answer names the matrix version and follows a new one without a deployment (new, D-RCV-60)
    Given matrix version "PM-SIT-02" is in force on 15 December 2026
    When the admission is asked on that date the answer names "PM-SIT-02"
    Then when a version "PM-SIT-03" is loaded and takes effect on 1 January 2027 the same admission asked on 2 January 2027 names "PM-SIT-03" with no deployment
    Then a read never mixes two versions: it answers one whole, either the version in force before the effective date or the one after it

  Scenario: AC11 The authority names no table of another service (new, D-RCV-60)
    Given the target queue "MTG-BKK-PRI" exists in rwb-case and no queue row exists in rwb_access
    When the admission is asked with that queue, its team code and the case reference
    Then the answer is given on the presented values and no query of the package names recovery_case, queue, assignment or any recovery.v_ace_* view
    Then an unknown queue ID is not refused here: the queue and the case are rwb-case's, and its own 404 with MSG-P4-003 is the only place that answer exists
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A model or an agent writes to a queue only through the admission answer of `rwb-access`, under its own service identity, with the case, the caller, the reason and the version | REQ-CWC-017; REQ-CWC-018; legacy RWB-E2-036 BR1 |
| BR2 | The caller passes the same permission check a person passes: the letter `C` of the capability area `QUEUE_AND_ALLOCATION` in the matrix version in force, with no bypass for a non-engine caller | REQ-CWC-018; REQ-ACA-010; CTL-09; NFR-051; legacy BR2 |
| BR3 | The queue targeting follows the scope of the admitting role: a service identity holds scope `ALL` and may target any queue of `rwb-case`; a narrower scope is refused, because no row of `rwb_access` binds a role to a list of teams or regions | Legacy §12 authorization; REQ-ACA-009; GAP-0959; ASM-1691 |
| BR4 | Only a role of class `NON_HUMAN_ACTOR` may be the subject of this admission: a person's identity, or a role whose class is `BANK_USER` or `PARTNER_USER`, is refused | REQ-ACA-010; NFR-051; LOV-ROLE-CLASS |
| BR5 | Every admission, allowed or refused, writes one access entry with the caller, the caller type, the version, the queue, the case, the two version labels and the reason code, in the transaction that produces the answer, with no personal value | NFR-078; R-UNI-39; CTL-06; FSD P4 v3 A2.7 and A2.8 |
| BR6 | The four legacy request fields keep their legacy shape: `caseId`, `reason` (1 to 1,000 characters), `callerCode` and `modelVersion` (1 to 40 characters), with the target queue required; the product group is a value of LOV-PRODUCT at the version in force | Legacy RWB-E2-036 §12; FEAT-CWC-29 |
| BR7 | Masking is default deny: a field ID is answered `clear` only where a `masking_rule` row for one of the caller's roles, that field and the masking version in force says `unmasked` true, and `masked` otherwise, including where no row exists; no field value is ever returned | FSD P4 v3 A2.5 and AC-EXC-P4-004-05; REQ-ACA-006; NFR-040 |
| BR8 | This slice gates nothing: the feature flag `rwb.casewf.queue-placement` is the adapter's and the case service's, and the admission answer is the same whether the flag is on or off | REQ-CWC-019; legacy precondition; RWB-P2-E2036-CON §12.1 |
| BR9 | The answer carries policy only: no case status, no owner, no assignment, no assignment method, no caseload cap, no overflow queue and no queue row is read, answered or written | Arch v5 slide 41 (rwb-case owns case, queues, tasks, allocation); DP-01 |
| BR10 | One answer names one matrix version whole: the version is resolved once per call from the effective date, and a read never mixes two versions | R-UNI-38; FSD P4 v3 A2.4 |
| BR11 | A refusal names the area, the letter asked, the matrix version, the scope and the reason code, and nothing else; it returns no limit, no holder, no queue list and no field value | FSD P4 v3 VR-P4-004-1; CTL-09 |
| BR12 | No business value in code: the matrix version, the letters, the scope, the role class, the capability area, the product groups and the masking rows are data of their owners, and the reason codes are the only enumeration this story fixes | BR-P4-004; FSD P4 v3 A2.4; GAP-0958; ASM-1690 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR2 are one read of `permission` for the caller's roles at the matrix version in force, keyed on the capability area and the letter `C`; there is no second path for a model and no second path for an agent, which is also what REQ-CWC-020 asks of the platform.
- BR3 is the `role.default_scope` value alone. The queue's team code is presented with the request and recorded in the entry; it is never compared with a team list, because the only binding a source names is the single `default_scope` value of a role (GAP-0959; ASM-1691).
- BR4 is the `role.role_class` value against `LOV-ROLE-CLASS`. The caller code is recorded and not resolved: the role is the role of the service identity, and how a caller code is bound to a role is not specified by any source (GAP-0960; ASM-1692).
- BR5 is the entry appender of RWB-P4-E1039-APP inside the transaction that produces the answer; `rwb_access` holds no access-log table of its own, so the access log and the decision log are the same append-only chain (legacy FEAT-ACA-08).
- BR6 keeps the legacy lengths character for character and puts the product group in the reference-data list of DP-07 rather than in a Java enumeration.
- BR7 is the same `masking_rule` read the data-product answer uses; a placement gains nothing by asking for a field, because the default is deny.
- BR9 is the boundary rule: the package names no case, queue or assignment table and calls no `rwb-case` operation, and the boundary test of RWB-P4-E1069-APP stays green on it.
- BR12 is checked by test: a new matrix version, a new product group or a new masking row changes no build.

### 9. State transitions

This service holds no case, queue, assignment or approval state. The states it answers are the outcomes of one admission and the lifecycle of the matrix version it reads, which RWB-P4-E1019-APP writes.

| From | Event | Condition | To |
|---|---|---|---|
| No admission | Admission asked with the caller's `C` letter at the version in force and scope `ALL` | The access entry is written | `ADMITTED`, decision code `AC-READ` |
| No admission | Admission asked, no `C` letter | The entry is written | `REFUSED` 403, reasonCode `RIGHT_NOT_HELD`, decision code `AC-DENY` |
| No admission | Admission asked, scope narrower than `ALL` | The entry is written | `REFUSED` 403, reasonCode `SCOPE_NOT_ALL` |
| No admission | Admission asked, the subject is not a `NON_HUMAN_ACTOR` role | The entry is written | `REFUSED` 403, reasonCode `CALLER_KIND` |
| No admission | A required field is empty or a value is outside its list | No admission is made | 422, MSG-GEN-001 or MSG-GEN-002 |
| No admission | The entry cannot be written | None | 503, MSG-P7-003, nothing answered |
| Matrix version in force | A new version takes effect on its date | An admission is dated on or after that date | The new version answers; the older rows stay readable for their own dates |
| Admission answered | The same admission is asked again | None | The same answer, and a second entry: a read is an event, not a state change |

| Command | Condition | Outcome |
|---|---|---|
| Admission | `C` letter, scope `ALL`, role class `NON_HUMAN_ACTOR` | `ADMITTED`, one entry with `AC-READ` |
| Admission | Any of the three refusals of BR2 to BR4 | `REFUSED`, one entry with `AC-DENY` and the reason code |
| Profile read | The subject resolves to a role of class `NON_HUMAN_ACTOR` | 200 with the profile; any other class is 403 with MSG-P4-002 |

The case status, the queue, the assignment and the placement record move in `rwb-case`; this story holds no copy of them and changes no state of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The `rwb-integration` service identity | Calls the admission part of `POST /api/recovery/access/v1/authorise` and reads nothing else; its own right to call the operation is answered by the guard library of DP-08. Its login name is DP-02's and is not named here |
| The service identities of the other services | Call the same operation under their own cached permission read (DP-08); no other service places work through the model path in this release |
| `SY-AGENT` and the other `NON_HUMAN_ACTOR` roles | Are the subjects of an admission; they hold no write path of their own and read no row of `rwb_access` |
| RW-SECADM | Loads the matrix version that gives a service identity the `C` letter and a class of `NON_HUMAN_ACTOR` (RWB-P4-E1019-APP); this story gives it no write path |
| RW-RISK | Approves a caller entry before it is loaded into the approved callers list of `rwb-case`; this story holds no copy of the list |
| RW-COE | Requests a caller entry; it calls no operation of this story |
| RW-AUDIT | Reads the access entries through the decision log of `rwb-decision` and the access-log query of RWB-P4-AD007-APP; it calls no operation of this story |
| RW-PLATADM | Switches the placement flag on in `rwb-integration`; the flag is not this service's and no operation of this story reads it |
| `rwb-access` itself | Reads `role`, `permission` and `masking_rule` in `rwb_access` and writes no row of them in this story |

The refusal shape is 403 with an RFC 9457 problem response, `messageId` MSG-P4-002 and a `reasonCode`. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb-case` | LOV-CAPABILITY, LOV-SCOPE, LOV-ROLE-CLASS and LOV-PRODUCT versions in force | Read through the reference-data contract |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the access entry of an admission and of a refusal | Write |
| (outbox) | `outbox_event` in `rwb_access` | the outbox row of the entry (DP-09) | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| (idempotency) | `idempotency_key` | none: the replay is the caller's, and this story stores no answer | None |

No row of `recovery_case`, `queue`, `assignment` or `task` is read or written: those tables are `rwb-case`'s (P3), and the queue ID, the team code, the case reference and the product group arrive in the request as presented values (DP-01). No row of `data_product` or `data_product_access` is read: that access row is P1's and the data-product part of the answer is RWB-P4-E1016-APP's. No `recovery.v_ace_*` view is named. `lov_value` is reference data of `rwb-case` under the ownership ruling and is read through DP-07, not from `rwb_access`. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/access/v1`; owner P4 `rwb-access`. Both operations are the service baseline's and are published by RWB-P4-E1037-CON; this story fixes the placement admission part of the first and the non-human part of the second, and adds no path (DP-13).

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` | Body: `callerCode`, `callerType`, `serviceIdentity`, `targetQueueId`, `targetQueueTeamCode`, `caseId`, `productGroup`, `reason`, `modelVersion`, `fieldIds[]` | `admitted`, `reasonCode`, `callerType`, `roleClass`, `roleCodes[]`, `capabilityArea`, `right`, `letters`, `scope`, `matrixVersion`, `maskingVersion`, `productGroup`, `fieldMarkers[]` | 401 MSG-P4-001; 403 MSG-P4-002 with `reasonCode`; 422 MSG-GEN-001 or MSG-GEN-002; 503 MSG-P7-003 | The calling service identity's right to the operation (DP-08) and, for the subject, the `C` letter of `QUEUE_AND_ALLOCATION` | Not applicable, read only; each call writes one access entry and no Idempotency-Key is stored here |
| GET | `/api/recovery/access/v1/me/permissions` | P4 `rwb-access` | Query: `serviceIdentity`, or the session of the caller | `roleCodes[]`, `roleClass`, `scope`, `letters[]` per capability area, `matrixVersion`, `queueTargeting` | 401 MSG-P4-001; 403 MSG-P4-002; 503 MSG-P7-003 | The same guard right; the read answers the caller's own profile only | Not applicable, read only |

The operation names are Arch v5 slide 14's (`POST /authorise (role, scope, DoA)`, `GET /me/permissions`), and the base is DP-13's. Neither the legacy story nor a technical specification names the element set of either operation, and the reason codes are this story's own enumeration: the request and answer element names are Not specified in the source documents (GAP-0957; ASM-1689) and the reason code vocabulary is Not specified in the source documents (GAP-0958; ASM-1690). The contract review with the `rwb-integration` owner confirms or renames them before the part is frozen, and the adapter's 12.2 row (`POST /api/recovery/access/v1/authorise`) is the consuming side of exactly this table.

The operation changes no other operation of the service: `GET /api/recovery/access/v1/doa-limits`, the masking-policies read, the role catalogue and the access-log query keep the shapes their own stories publish.

#### 12.2 REST operations consumed

None. This story calls no REST operation. The queue ID, the team code, the case reference and the product group are presented with the request, the reference lists arrive through the client library of DP-07, and the permission rows are read in process from `rwb_access`. No call to `rwb-case` is made, so no 2 s budget and no breaker is declared on this side (DP-01, DP-11).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| None of its own | `rwb.access.events.v1` | P4 | None | This story adds no event to the service's topic. `AccessPolicyChanged` and `DoaLimitChanged` stay the load stories' |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained access entry of an admission or of a refusal, with decision code `AC-READ` or `AC-DENY` |

CloudEvents 1.0 envelope; neither payload carries a name, an e-mail address or a personal value. A placement is not a policy change, so this slice has no event of its own on `rwb.access.events.v1`: Architecture v5 slide 14 fixes the service's two events and the realignment adds none. The access entry is the decision-record entry of DP-03, so the access log and the decision log are one chain.

#### 12.4 Events consumed

None. Architecture v5 slide 14 gives `rwb-access` no inbound event ("none: reference data owner"), and this story adds no subscription and therefore writes no inbox row. The permission caches that other services refresh on `rwb.access.AccessPolicyChanged.v1` are their concern, not this story's.

#### 12.5 Workflows and activities

None. The admission is a synchronous answer of one REST request; this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. The queue `rwb-access` in namespace `rwb-recovery` exists for the service's Schedule work, and the six-monthly access review list (JOB-18) is not part of this story.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) is a Schedule of `rwb-access` and belongs to the service's own story, not to the admission answer.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role of the caller's service identity, its class and its default scope |
| `permission` | P4 (`rwb_access`) | Read only: the letters of that role in `QUEUE_AND_ALLOCATION`, at the matrix version in force |
| `masking_rule` | P4 (`rwb_access`) | Read only: the marker per field ID at the masking version in force |
| `outbox_event` | PLT library, created in `rwb_access` | The outbox row of the access entry (DP-09) |
| `processed_event` | PLT library, created in `rwb_access` | Not used: this story consumes no event |
| `idempotency_key` | PLT library, created in `rwb_access` | Not used: this story stores no answer, and the replay is the adapter's |
| `decision_record` | PLT library, created in `rwb_access` | The access entry of an admission and of a refusal, through the writer of RWB-P4-E1039-APP (DP-03) |

`recovery_case`, `queue`, `assignment`, `task`, `data_product` and `data_product_access` are never named by a query of this story, and no foreign key crosses a schema (DP-01). `lov_value` and the reference tables are read through DP-07. The column set of `decision_record` beyond the standard record columns is the library's and is Not specified in the source documents (GAP-0961; ASM-1693).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-integration placement WireMock | RWB-P2-E2036-CON | Placement "PL-1" for queue `MTG-BKK-PRI`, team `MTG-BKK` and case `RW-2026-000501`; a placement with an unknown queue ID; a placement after the approved callers refusal, so the "never reaches this operation" case of AC5 can be proved |
| rwb-integration approved callers fake | RWB-P2-E2036-CON | The list holding `MDL-SYN-PRIORITY` of type `MODEL` for `SY-AGENT` with version `1.4.0`, the list without `MDL-SYN-UNLISTED`, and the empty list at go-live |
| decision-record fake | RWB-PLT-E1027-CON, RWB-P4-E1039-APP | The entry append, the hash chain check and the forced failure of AC9 |
| authorise and guard fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The guard right to call the operation, the grant and the refusal, and the two-call cache |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY (14 areas including `QUEUE_AND_ALLOCATION`), LOV-SCOPE (`OWN`, `TEAM`, `REGION`, `ALL`), LOV-ROLE-CLASS (`BANK_USER`, `PARTNER_USER`, `NON_HUMAN_ACTOR`) and LOV-PRODUCT (`MORTGAGE`, `SSME`, without `HIRE_PURCHASE` in the version used by AC6), each with its version |
| matrix and masking fixtures | RWB-P4-E1019-APP, RWB-P4-E1016-APP | `PM-SIT-02` with `CRU` for `SY-AGENT`; `PM-2026.11` with `R` only; `PM-SIT-03` effective 1 January 2027; scope `ALL` and scope `TEAM`; `MASK-SIT-01` with the one `unmasked` row for `RW-TEAMMGR` on `DF-PTY-016` |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 (one extended operation `POST /authorise` and one extended read `GET /me/permissions`); consumed 0 | Base `/api/recovery/access/v1`; no hop to any other service |
| Kafka | Published 0 of its own, 1 published by the decision-record library; consumed 0 | `rwb.decision-record.v1`; `rwb.access.events.v1` is not extended |
| Temporal | 0 workflows, 0 activities, 0 Schedules | The service's Schedule work (JOB-18) is another story's |
| File | None | No file input and no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/placement`, Java package `th.co.scb.ace.workbench.recovery.access.placement`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the common module's access check that the placement handler called in process (DP-08: this service's own authorise contract and the guard library, so the answer is one hop and is cached) and the monolith's single `/api/recovery/v1` base (DP-13: the service base of DP-13). DP-11 is carried by the legacy key and its work sits with `rwb-integration`: the caller-facing placement is a REST contract with a mock, one hop and a 2 s timeout, and this story is the answering side of that hop. DP-14 is present for the topic name the service owns, which this slice does not extend, and DP-19 is present because the legacy key carried a placement through a screen path; no screen is served here.

This secondary slice adds no new build dependency of its own (metadata "Depends on (build)" is None): the decision-record library, the guard library, the reference-data client, the outbox and the gateway route are already build dependencies of the service's own stories, in particular RWB-P4-E1037-CON, RWB-P4-E1016-APP and RWB-P4-E1039-APP, and this story builds against the published contracts, the `rwb_access` baseline and their fakes from Day 1.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PlacementAuthorityController | Controller | The admission part of `POST /authorise` and the non-human part of `GET /me/permissions`: request validation, error mapping to RFC 9457 problem responses, the `reasonCode` of a refusal |
| CallerIdentityResolver | Service | BR4: the service identity to a `role` row at the matrix version in force, its role class and its role codes |
| PermissionReader | Service | BR2: the letters of those roles in `QUEUE_AND_ALLOCATION`, and the letter `C` that admits the write |
| CallerScopeService | Service | BR3: the `default_scope` of the admitting role and the queue targeting that follows from it; no team list exists |
| PlacementAdmissionService | Service | BR1, BR6, BR9: the order of the checks, the legacy field lengths, the product group against LOV-PRODUCT, and the answer that carries policy only |
| MaskingAnswerService | Service | BR7: composed from RWB-P4-E1016-APP; one marker per field ID at the masking version in force, default deny |
| MatrixVersionResolver | Service | BR10: the matrix version in force for the day of the call, resolved once per answer |
| CallerProfileService | Service | The `/me/permissions` answer for a non-human caller: roles, class, scope, letters, version and queue targeting |
| AccessEntryWriter | Service | BR5: the entry of an admission and of a refusal, through the writer of RWB-P4-E1039-APP, in the transaction that produces the answer (DP-03, DP-09) |
| LevelCatalog | Service | LOV-CAPABILITY, LOV-SCOPE, LOV-ROLE-CLASS and LOV-PRODUCT through the reference-data contract of DP-07; no Java enum of areas, scopes, classes or products |

**Database and migrations**

- This story creates no table and owns no Flyway version of its own. `role`, `permission` and `masking_rule` are created by the service baseline (RWB-P4-E1037-APP) in the per-service sequence of DP-15, and their rows are loaded by RWB-P4-E1019-APP and RWB-P4-E1016-APP; this story reads them through the repository.
- The read predicates are `permission.role_id`, `permission.capability_area`, `permission.matrix_version`, `role.default_scope`, `role.role_class` and the `masking_rule` keys `role_code`, `field_id` and `masking_version` with their date window. If the SIT query plan needs an index that the creating story does not have, the index is added to that story's migration, not to a new one here.
- No write statement exists in the repository for any of the three tables: the class exposes no save, update or delete, so an admission can never change a permission row.
- The entry row and its outbox row commit in one transaction with nothing else to write; a failure rolls them back and the answer is not returned.

**Configuration and reference data**

- The matrix version in force is data, resolved from the effective date of the version in `permission`; the label is never a constant. The masking version in force is data of `masking_rule` the same way.
- LOV-CAPABILITY (the 14 areas, including `QUEUE_AND_ALLOCATION`), LOV-SCOPE (`OWN`, `TEAM`, `REGION`, `ALL`), LOV-ROLE-CLASS (`BANK_USER`, `PARTNER_USER`, `NON_HUMAN_ACTOR`) and LOV-PRODUCT are read through the reference-data contract of DP-07 with the version in force; no area, scope value, role class or product group is a literal in code.
- The reason codes of BR11 are the one enumeration of this story; they are fixed in the contract document, not spread through the classes, and every refusal carries exactly one.
- The approved callers list, the placement flag and the replay window are not configuration of this service: they are `rwb-integration`'s and `rwb-case`'s, and this story holds no default for any of them.

**Build steps**

1. `CallerIdentityResolver` and `PermissionReader` over `role` and `permission`, with the version resolved once; tests for AC1, AC2 and AC10.
2. `CallerScopeService` with the `ALL` rule and the three refusal reasons; tests for AC4, and the negative test that no team list is read.
3. `PlacementAdmissionService` with the legacy lengths and the product group against LOV-PRODUCT; tests for AC6, including `HIRE_PURCHASE` and a 41-character version.
4. The masking composition with the default-deny marker; tests for AC7, including the `DF-PTY-016` exception held by another role and the empty `fieldIds` case.
5. `CallerProfileService` on `GET /me/permissions`; tests for AC3, including the `BANK_USER` refusal.
6. `AccessEntryWriter` with the entry append and the outbox row in one transaction, through RWB-P4-E1039-APP; tests for AC8 and for the 503 of AC9.
7. The boundary test: the package names no case, queue, assignment or `recovery.v_ace_*` name and calls no other service; test for AC11.
8. The contract-fake run with `RWB-P2-E2036-CON` and its four fakes, so the story builds before any `rwb-case` build exists in the environment, and the guard denial test for a calling identity without the operation right.

**Feature switch.** None of its own. The placement is switched on and off by `rwb.casewf.queue-placement` in `rwb-integration`, whose 404 with MSG-P2-025 is its first check and which never reaches this operation while the flag is off; this answer is the same in both states because authority is not a switch (BR8). The service-level kill switch and the feature flag of the service baseline are RWB-P4-E1037-CON's, and this story adds no flag and removes nothing when a matrix version is rolled back, because the admission always answers the version in force.

**Done when.** The tests in section 16 pass; the admission answers `ADMITTED` on the `C` letter of `PM-SIT-02` for `MDL-SYN-PRIORITY` under `SY-AGENT` with scope `ALL`; the `R`-only production row is refused with MSG-P4-002 and `RIGHT_NOT_HELD`; a `TEAM` scope is refused with `SCOPE_NOT_ALL` and a `BANK_USER` subject with `CALLER_KIND`; no field ID is answered `clear` without an `unmasked` row; every admission and every refusal leaves one access entry with the caller and its version; and the operation is green on the boundary test that names no table of another service.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller presents no Workbench role, or no valid session or workload token | Not specified in the source documents (GAP-0957; ASM-1689). | This story, before any row is read; the text is the service baseline's |
| MSG-P4-002 | The calling service identity holds no right to the authorise operation | You cannot {action} here. Your role does not include it. | This story, on the admission and on the profile read |
| MSG-P4-002 | The subject is not a `NON_HUMAN_ACTOR` role, the letter `C` is absent, or the scope is not `ALL` | You cannot {action} here. Your role does not include it. | This story, with `reasonCode` `CALLER_KIND`, `RIGHT_NOT_HELD` or `SCOPE_NOT_ALL` |
| MSG-GEN-001 | A required field is empty or a value is not in its list | Enter {field}. | This story, on the admission |
| MSG-GEN-002 | `reason` or `modelVersion` is outside its length | {field} must be between {min} and {max}. | This story, on the admission |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the admission and on the profile read |
| MSG-P2-025, MSG-P2-020, MSG-P2-024, MSG-P2-021, MSG-P3-005, MSG-GEN-004, MSG-P4-003 | The flag, the approved callers list, the duplicate placement, the open deviation, the closed case, the concurrent change or the unknown queue | The legacy texts, unchanged | Not produced here: `rwb-integration` and `rwb-case` produce them, and this story adds no message to them |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. A 403 also carries `reasonCode`, and the values that make the refusal legible — the capability area, the letter asked, the matrix version and the scope — and nothing else (BR11). The Thai text of each message follows decision DL10 and is the message catalogue's, not this story's.

### 15. Screens and states

No screen is built in this story. The admission and the profile read are consumed by `rwb-integration` and by the other services' guards; the screens that show their answers belong to other stories.

| Screen | State | Where it is |
|---|---|---|
| SCR-07 Team queues and SCR-02 Case list | Loading, list, empty | `rwb-case` (RWB-P3-E1019-APP and the case list stories); a placed case appears there like any other case |
| Case record view history | Entry per event | `rwb-case` and `rwb-decision`; the admission entry appears as an access entry, with the caller code and its version |
| Access audit query | List over a period | `rwb-access` (RWB-P4-AD007-APP); it reads the entries this story writes |

The gateway-bff composite route of DP-19 is not used by this story: no screen calls the admission directly, and the model or agent calls `rwb-integration`, which calls this service in one hop with a 2 s timeout and caches the answer.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-036-01 | AC1, BR1, BR2 | Contract | Approved caller `MDL-SYN-PRIORITY` of type `MODEL` under `SY-AGENT`; `PM-SIT-02` with `CRU`; queue `MTG-BKK-PRI`, team `MTG-BKK`, case `RW-2026-000501` |
| TC-E2-036-02 | AC1, BR3 | Contract | The same admission with the mock answering an owner at 150 and 149 and then both at 150 with `MTG-BKK-OVF`: the authority answer is identical and names no owner |
| TC-E2-036-03 | AC8, BR5 | Component | One admitted placement; the access entry field by field, with the caller code, the type and the version |
| TC-E2-036-04 | AC1, BR8 | Contract | The same admission with the adapter's 404 MSG-P2-025 and again with the flag on: this answer is unchanged and this operation is not reached while the flag is off |
| TC-E2-036-05 | AC5, BR4 | Contract | `MDL-SYN-UNLISTED` refused by the adapter's list and never reaching this operation; and a subject whose role class is `BANK_USER` refused here with `CALLER_KIND` |
| TC-E2-036-06 | AC6, BR6 | Component | A request with no `caseId`; a `reason` of 0 and of 1,001 characters; a `modelVersion` of 41 characters |
| TC-E2-036-07 | AC8, BR5 | Component | The same admission sent twice: two answers and two access entries; the one-placement rule is the case service's |
| TC-E2-036-08 | AC1, BR9 | Contract | A `CLOSED` case refused by the case service: the authority answer is unchanged and this operation names no case status |
| TC-E2-036-09 | AC11, BR9 | Contract | A case with an open deviation refused by the deviation service: this operation names no deviation and answers on the presented values |
| TC-E2-036-10 | AC11, BR9 | Component | A queue ID that the case service does not hold: no refusal is produced here, and the boundary test proves no queue row is read |
| TC-E2-036-11 | AC8, AC10 | Component | Two admissions commit at the same time: each writes its entry, and both answers name the one matrix version in force |
| TC-E2-036-12 | AC1, BR3 | Contract | A case with owner `U-5100` in `MTG-BKK-CO`: the authority answer is unchanged and names no owner and no queue |
| TC-E2-036-13 | AC2, AC5 | Component | `SY-AGENT` under the production matrix `PM-2026.11` with `R` only: refused with MSG-P4-002 and `RIGHT_NOT_HELD`, one `AC-DENY` entry |
| TC-E2-036-14 | AC9, BR5 | NFR | The access entry forced to fail during an admission: 503 MSG-P7-003, no admission answer, nothing written |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The whole legacy set is kept because the authority side of the key carries it; the tests whose rule lives in `rwb-integration` (the flag, the approved list, the replay) or in `rwb-case` (the cap, the overflow, the closed case, the deviation, the duplicate, the concurrency, the owner) use this story's answer and the contract fake for the rest. The ITG copy of the whole set is the wave 2 integration harness of this legacy key and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the matrix version, the letters, the scope, the role class, the capability area, the product groups and the masking rows are data of their owners, and only the reason codes are fixed here (BR12). A test proves that a new matrix version, product group or masking row needs no build.
- No personal data anywhere: the admission carries a caller code, a case reference, a product group, a reason phrase and a version; the answer, the access entry and the event payload carry no name, no e-mail address and no personal value, and no test data or prompt holds one.
- No read of another service's tables (DP-01): `recovery_case`, `queue`, `assignment` and `task` are `rwb-case`'s, `data_product` and `data_product_access` are P1's, and no foreign key crosses a schema. The queue ID, the team code and the case reference are presented values.
- ACE data only through the owner's contract or its own `v_ace_*` views: this story reads no ACE data at all, and the group-to-role mapping is the service's own concern in its own story.
- One authority path for a model, an agent and a person: there is no model-only operation, no exemption from the `C` letter and no second scope rule, which is the property REQ-CWC-020 and REQ-ACA-010 rely on.
- No answer without its entry: the access entry commits with the answer, and the answer is withheld with MSG-P7-003 when it cannot be written (BR5, R-UNI-39).
- The admission is read-only and repeatable; a retry answers the same and writes a second entry, as a read of policy must, and no answer of this story is stored as an idempotent one.
- A refused caller learns the reason code, the area, the letter and the version, and nothing else: no queue list, no field value and no other caller's data is returned in a refusal (BR11).
- The placement stays `rwb-case`'s and the flag, the list and the replay stay `rwb-integration`'s: this story answers policy, records the entry and never forwards, allocates or retries.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-017 | A queue accepts a write from a model or an agent with the case and the reason | Epic 2, 3.2 | FEAT-CWC-29 | All recovery processes | BR1, BR6 | TC-E2-036-01, TC-E2-036-06 |
| REQ-CWC-018 | A model or agent passes the same permission checks and its write is logged with its version | Epic 2, 3.2 | FEAT-CWC-29 | All recovery processes | BR2, BR5 | TC-E2-036-03, TC-E2-036-13, TC-E2-036-14 |
| REQ-CWC-019 | The queue write interface ships behind a feature flag | Epic 2, 3.2 | FEAT-CWC-29 | All recovery processes | BR8 | TC-E2-036-04, TC-E2-036-05 |
| REQ-CWC-020 | Model and rule work in the same queue, in one priority order | Epic 2, 3.2 | FEAT-CWC-29 | All recovery processes | BR1, BR9 | TC-E2-036-01, TC-E2-036-02 |
| REQ-ACA-010 | A model or agent identity passes the same role and scope checks as a person | Epic 1 | FEAT-ACA-01, FEAT-ACA-04 | All recovery processes | BR2, BR4 | TC-E2-036-05, TC-E2-036-13 |
| NFR-051 | Agents run under service identities and are subject to the same role checks as people | Non-functional, security | FEAT-ACA-04 | All recovery processes | BR2, BR4 | TC-E2-036-13 |
| NFR-078 | A model or agent write to a queue is logged with the model or agent version | Non-functional, audit | FEAT-ACA-07 | All recovery processes | BR5 | TC-E2-036-03, TC-E2-036-14 |
| R-UNI-39 | An action whose decision entry cannot be written does not proceed | Business rules, universal | FEAT-ACA-07, FEAT-ACA-08 | All recovery processes | BR5 | TC-E2-036-14 |

| Legacy reference | Where it is kept |
|---|---|
| Approved caller `MDL-SYN-PRIORITY` of type MODEL under `SY-AGENT`; the empty list at go-live and the RW-COE and RW-RISK approval | Sections 1, 3, 5, 12.2, 12.8, 19 |
| Queue and allocation C in the matrix in force; `SY-AGENT` holds R only under the production matrix | Sections 3, 7, 8, 10, 16 |
| The four request fields `caseId`, `reason`, `modelOrAgent` and `version` with their legacy lengths | Sections 4, 8, 12.1, 14 |
| The same permission check for a person, a model and an agent, under a service identity | Sections 2, 4, 8, 17 |
| Every write logged with the caller, the reason and the model or agent version | Sections 4, 7, 8, 11, 17 |
| The feature flag, the approved callers list and the replay are the adapter's | Sections 1, 3, 8, 12.2, 13, 19 |
| MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-002, MSG-P7-003 | Section 14, exception paths |
| Rule IDs R-UNI-39, R-UNI-38, CTL-06, CTL-09, NFR-051, NFR-078 | Sections 2, 8, 17, 18 |
| Legacy key RWB-E2-036, story RWB-P4-E2036-APP, contract RWB-P2-E2036-CON | Metadata, sections 3, 12 |
| Field IDs DF-REF-034 to DF-REF-044, DF-REF-198 to DF-REF-204, DF-DEC-001 to DF-DEC-018 | Section 11 |

### 19. Out of scope

- The placement itself: the placement record, the queue, the assignment method, the caseload cap, the overflow queue, the assignment, the placement decision entry and the CaseAllocated and CaseTransferred events (RWB-P3-E2036-APP and the queue engine it reuses).
- The caller-facing admission and forwarding operation, the feature flag `rwb.casewf.queue-placement`, the `Idempotency-Key` replay and the approved callers list (RWB-P2-E2036-CON and RWB-P2-E2036-APP).
- The approved callers list as a row: it is the `rwb-case` parameter and reference-data row under `rwb.casewf.placement.approved-callers`, read through DP-06 and DP-07.
- The data-product access row and the catalog entries (P1, RWB-P1-E1016-APP), and the retention class of a catalog entry (P5).
- The central decision ledger, the decision log query and the hash-chain control of `rwb-decision` (P7).
- The open deviation that refuses a placement (RWB-S8-E2036-APP) and the case status rules of `rwb-case`.
- The delegation of authority table and the approval routing of the same service (RWB-P4-E1038-APP and RWB-P4-E2013-APP): a placement moves work and approves no treatment, so no approval level applies.
- Score and priority on the placement and the queue order by priority (REQ-CWC-020): added with the first approved model consumer, in the epic that switches the flag on.
- The model or agent that calls the interface: the P10 agent runtime stories, for example the agent run and guardrail stories of RWB-SVC-P10.
- Granting a service identity the Queue and allocation `C` letter in the production matrix: a matrix version change under RWB-P4-E1019-APP.
- The real cross-service proof of the journey through gateway-bff (the wave 2 integration harness of this legacy key) and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
