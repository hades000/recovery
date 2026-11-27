# RWB-P4-E2022-APP SMS and LINE dispatch through NSS and LINE OA

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2022-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P4-AO |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E2022-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-OCC-004, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010, REQ-DRI-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-022 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E2022-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner who sends an SMS or a LINE message from SCR-03, and the access service that holds the roles, the scope and the masking policy as data**, I want **one authorise answer that says whether my role carries Case record C on a case inside my own scope, that the phone number field DF-ACE-078 and the party identifier field DF-ACE-077 are masked under the masking version in force, and one access entry for every look, every refusal and every send that names the case, the channel and the template but never a token, a number, a LINE identifier or a message text**, so that **the message is sent by a role that may send it, the phone number and the LINE identifier stay tokens inside the Workbench, and the audit trail shows who sent what on which case without holding a single personal value**.

Inside `rwb-access` this is the access slice of the legacy story RWB-E2-022:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The slice extends three operations of the service baseline and invents no path: `POST /api/recovery/access/v1/authorise`, which answers the right on a send and on a look and carries the field markers; `GET /api/recovery/access/v1/me/permissions`, which answers the caller's roles, letters, scope, matrix version and masking version; and `GET /api/recovery/access/v1/masking-policies`, which answers the mask answer for a field and a role.
- The slice delivers no business behaviour. The conduct check, the template merge, the outbox send, the retry, the NSS and LINE OA results and the ledger entries are `rwb-comms`'s (P6) in RWB-P6-E2022-APP, the case and the case timeline are `rwb-case`'s (P3), the interaction ledger and the contact point facts are `rwb-source-data`'s (P1), and the central decision ledger and its query are `rwb-decision`'s (P7). This story calls none of them: it is consumed by the gateway route and by the send route through the published contract RWB-P6-E2022-CON, one hop, 2 s timeout, and tested against that contract's fake.
- The whole legacy key is split across services: DP-05 (the contact point and the consent) is P1's data read by P6's route, DP-09 (the outbox send) and DP-10 (JOB-11) are P6's, DP-18 (the interaction ledger) is P1's, and DP-19 (SCR-03 and SCR-04) is served through the gateway-bff composite route. What remains here is the role, the right, the scope, the mask answer and the access entry.
- The policy pack is data: permission rows under matrix version `PM-2026.12`, masking rows under masking version `MASK-SIT-01`. The load path that writes those rows is the service's own and is out of this story (RWB-P4-AD002-APP, RWB-P4-AD004-APP).

The rights carried from the legacy story are unchanged: `RW-CASEOWN` holds Case record C and sends on a case in its scope; `RW-TEAMMGR`, `RW-CONDUCT` and `RW-COMPLAIN` hold Case record R and read messages on the cases they may see; `RW-PHONECOL` holds no Case record row and is refused the send. The letters per role are carried from the legacy story and are not in the TSD P4 matrix (GAP-0953; ASM-1684).

### 2. Business rationale

Case owners send SMS and LINE messages outside the Workbench today, so a message can reach a customer under a contact stop or without consent, and no one can prove afterwards who sent it. The legacy story answered the sending; this slice answers the two questions that make the sending defensible: may this role send on this case, and can the number the message goes to exist anywhere outside the owning service.

The number and the LINE identifier are the most sensitive values on the case record, and they are the values a log line, a test fixture or a prompt picks up first. Legacy RWB-E2-022 section 17 fixes the rule in one sentence: the phone number and the LINE identifier stay tokens in the Workbench and the ACE notification path detokenizes them. This story makes that rule hold in the target: the mask answer is a data row per role and per field, the ACE PII service is never called for a clear value on this path, and the access entry of a send names the case, the channel and the template and no value at all.

This story meets REQ-OCC-004, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010 on the access side — who may send, what is recorded of the send, and that the record carries no personal value — and it meets REQ-DRI-006 in the strongest form available: the slice calls no system of record, no channel platform and no PII service, so it cannot become the second path to NSS, LINE OA or ACE. It supports controls CTL-16 and CTL-17 (the contact stop and the consent) by keeping the send a right of a named role on a case in scope, and CTL-14 by letting no message leave outside that right and the current Approved template. It supports NFR-039 (party identifiers masked in use and on every screen), NFR-040 (only the personal data a screen needs), NFR-042 (every read logged) and NFR-051 (service identities under the same role checks as people).

The realignment changes the mechanism, not the business rule:

1. The role and permission rows of the monolith's recovery schema become `rwb-access`'s own tables in `rwb_access` (DP-01), versioned by matrix version, so a change of a role's right on Case record needs an approved load and no release.
2. The synchronous `RecoveryAccessGuard` call inside the monolith becomes the published authorise contract of DP-08 and DP-11, cached, one hop, 2 s timeout; the gateway route and the send route hold the answer for the life of the cache entry.
3. The masking decision that the monolith took in the view layer becomes a `masking_rule` read under the masking version in force, answered as data, so the same answer serves a screen, a list, an agent call and a preview with no second implementation.
4. The decision-log writer inside the monolith becomes the local decision-record library of DP-03: the `AC-READ` and `AC-DENY` entry of a look, a refusal and a send is hash-chained and published on `rwb.decision-record.v1`, where the central ledger and the audit query already read.
5. The access event the monolith never sent becomes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, so a new matrix or masking version reaches every cached answer at the next call with no deployment.
6. The ACE data behind the two masked fields stays where it is: `rwb-source-data` reads `v_ace_contact` and answers the contact point, `rwb-comms` sends to the token, and this service names the field and the mask version and never a value (DP-05).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P6-E2022-CON | The published send contract this slice is tested against: `POST /cases/RC-2026-000777/messages` with channel `SMS` or `LINE`, `templateCode`, `language` `TH` or `EN` and `partyId`, answering 202 with the interaction (channel, direction, conduct check, delivery status, external reference) or 409 for a contact stop, a missing consent, a withdrawn template or a legal hold. The conduct check, the merge, the outbox and the channel results are that contract's, and so is the fake |
| RWB-P4-E1037-CON (same service, its own contract story) | The authorise, me-permissions and masking-policies operations with their shape, the RFC 9457 problem responses with their message IDs, the permission and masking tables behind them, and the guard library. This slice adds no path and no field: it decides, behind those operations, what a send needs |
| RWB-PLT-E1037-CON | The guard library that carries this service's cached answer to the gateway route and to the send route (DP-08) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the access entry of a look, a refusal and a send |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): LOV-CAPABILITY with the area `CASE_RECORD`, LOV-SCOPE with `OWN`, `TEAM`, `REGION` and `ALL`, and LOV-ROLE-CLASS with `NON_HUMAN_ACTOR`, each with the version in force |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the SCR-03 open, the Send message action, the answer beside the action and the field list the screen renders |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09) |
| Permission matrix `PM-2026.12` `IN_FORCE` | The rows this slice answers from, loaded by the policy pack path (RWB-P4-AD002-APP, RWB-P4-AD004-APP): `CASE_RECORD` `C` for `RW-CASEOWN`, `CASE_RECORD` `R` for `RW-TEAMMGR`, `RW-CONDUCT` and `RW-COMPLAIN`, and no `CASE_RECORD` row for `RW-PHONECOL` |
| Masking version `MASK-SIT-01` in force | The rows for `DF-ACE-078` and `DF-ACE-077` under the mask version in force. The version label and its rows are assumed for SIT (GAP-0954; ASM-1685): no row of the pack names either field unmasked for any role on this path, so both are masked for every role |
| Test users in SIT | `CO-0201` holds `RW-CASEOWN` and owns case `RC-2026-000777`; `U-4101` holds `RW-CASEOWN` with default scope `OWN` and does not own it; `U-4103` holds `RW-TEAMMGR`; `U-4104` holds `RW-PLATADM`; `U-4106` holds `RW-PHONECOL` |

Business preconditions carried from RWB-E2-022:

- Templates `SMS-REMIND` `TH` version 1 (channel `SMS`) and `LINE-REMIND` `TH` version 1 (channel `LINE`) are Approved and current. Template status is `rwb-comms`'s and never changes the access answer (BR6).
- Case `RC-2026-000777` is owned by `CO-0201` with borrower party `P-0077`, and it has no legal hold and no open deviation at the moment of the send.
- Party `P-0077` has a verified `MOBILE` contact point and a verified `LINE` contact point, each with consent `GIVEN`. The contact point, its consent and its failed count are `rwb-source-data`'s extension rows behind its contract; this story names them and reads none of them.
- The phone number and the LINE identifier stay tokens in the Workbench, and the ACE notification path detokenizes them (legacy RWB-E2-022 section 17). No test, fixture, log line or prompt of this story holds a number or an identifier.
- The request and answer shape of the authorise call for a send, and the field list the composite route sends, are Not specified in the source documents (GAP-0955; ASM-1686).

### 4. Flow

1. Case owner (`CO-0201`): opens SCR-03 Case record on case `RC-2026-000777` through the gateway-bff composite route and reads the case, the party `P-0077` and the messages already sent.
2. gateway-bff composite route: on the screen open, calls `POST /api/recovery/access/v1/authorise` on this service with the caller's user reference, the roles the session resolved, capability area `CASE_RECORD`, right `C`, the case as the object reference, and the field list the screen will render, which holds `DF-ACE-078` and `DF-ACE-077`.
3. `AuthoriseService`: reads the caller's permission rows for `CASE_RECORD` from `permission` in `rwb_access` under the matrix version in force, unions the letters of every role the caller holds, and answers `allowed` with right `C`, the role `RW-CASEOWN`, `matrixVersion` `PM-2026.12` and `maskingVersion` `MASK-SIT-01`.
4. `ScopeResolver`: compares the owner of case `RC-2026-000777` with the caller. The default scope of `RW-CASEOWN` is `OWN` and `CO-0201` owns the case, so the case is inside the scope and no wider read is made. A case outside the scope is answered 404 with MSG-P4-003 and no case field.
5. `MaskingPolicyService`: reads the `masking_rule` rows for `DF-ACE-078` and `DF-ACE-077` and the caller's roles under the mask version in force and answers both fields masked. Where no row covers a field for any of the caller's roles the answer is masked as well, so the default is refuse rather than show (FSD P4 v3 A2.5, AC-EXC-P4-005-05). No value of either field is read, echoed or cached by this service, and no request is made to the ACE PII service for a clear value (FSD P4 v3 AC-ALT-P4-005-01).
6. The answer reaches the composite route and the screen draws the case with the phone number and the LINE identifier rendered masked, and offers Send message because right `C` is allowed. The route keeps the answer in the guard cache of DP-08 for the life of the cache entry, and the send route checks the cached answer before it calls `rwb-comms`.
7. Case owner: chooses Send message, the channel `SMS`, the template `SMS-REMIND`, the language `TH` and the party `P-0077`. A role whose cached answer does not hold `CASE_RECORD` `C` is refused here, with 403 and MSG-P4-002, and nothing is sent.
8. The send itself is `rwb-comms`'s: the send route calls `POST /cases/RC-2026-000777/messages` through RWB-P6-E2022-CON, one hop with a 2 s timeout and a circuit breaker. `rwb-comms` runs the conduct check, merges the template, writes the outbox row and answers 202 with the interaction (channel `SMS`, direction `OUTBOUND`, conduct check `PASSED`, delivery status `DELIVERED`, reference `NSS-7781`) or 409 with MSG-P6-001, MSG-P6-002, MSG-P6-003 or MSG-P3-004. This service is not on that hop and holds none of those facts.
9. The send route reports the action on the authorise operation with right `C`, the case `RC-2026-000777`, the channel `SMS`, the template code `SMS-REMIND`, the language `TH` and the conduct result the send answered. `AuthoriseService` answers the recorded decision, and `AccessLogWriter` writes one entry in the same transaction.
10. `AccessLogWriter`, `AC-READ`: decision code `AC-READ`, actor `CO-0201`, case `RC-2026-000777`, area `CASE_RECORD`, right `C`, channel `SMS`, template code `SMS-REMIND`, language `TH`, the conduct result `PASSED`, matrix version `PM-2026.12`, mask version `MASK-SIT-01`, the masked field markers `DF-ACE-078` and `DF-ACE-077`, and the time. The entry carries no token, no phone number, no LINE identifier and no message text; it publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` through the outbox.
11. A refusal — a role without Case record `C`, a case outside the scope, or a send on a case the caller may not see — is answered with its problem response and written as one `AC-DENY` entry with the actor, area `CASE_RECORD`, the right asked, the case reference and the reason code, and with no template code, no channel result and no value.
12. A policy pack load by the service's own administration path commits new `permission` or `masking_rule` rows and publishes `rwb.access.AccessPolicyChanged.v1`; the cache-refresh listener of this service reads it from `rwb.access.events.v1` and replaces the cached answer for the affected roles, so the next authorise call answers with the new version and the new mask answer, with no deployment and no restart, and never pairs a matrix version with a mask version from a different load.

Every answer and its access entry commit in one transaction (DP-03, R-UNI-39), so a call that cannot be logged is refused rather than answered (FSD P4 v3 AC-EXC-P4-007-03), and a repeated call with the same `Idempotency-Key` returns the first answer without a second entry.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller's role holds no `CASE_RECORD` row | 403, no send, nothing recorded as sent; one `AC-DENY` entry with area `CASE_RECORD` and right `C` | MSG-P4-002 | AC2, AC3 |
| X2 | The caller holds `CASE_RECORD` `R` and asks for right `C` | 403 for the named action; one `AC-DENY` entry with right `C`; the message is not sent | MSG-P4-002 | AC2 |
| X3 | The case is outside the caller's scope | 404 with no field of the case; one `AC-DENY` entry with the case reference and the reason | MSG-P4-003 | AC4 |
| X4 | No masking row covers `DF-ACE-078` or `DF-ACE-077` for any of the caller's roles | Both fields are answered masked under the mask version in force; the entry marks them masked; no value is read | None | AC5 |
| X5 | A policy version and a mask version arrive from two different loads | The cache refuses the mixed pair, keeps the versions it already holds and raises the mismatch; the caller gets the older consistent pair | None | AC1 |
| X6 | The send is blocked by the conduct check in `rwb-comms` | The access answer is unchanged and the entry records the conduct result `BLOCKED` with the case, the channel and the template only; the 409 is `rwb-comms`'s | MSG-P6-001, MSG-P6-002, MSG-P6-003, MSG-P3-004 (produced by `rwb-comms`) | AC10 |
| X7 | The decision record of the access entry cannot be written | The call returns 503, no answer and no data, and the route does not show the action as taken; the reason is logged | MSG-P7-003 | AC8 |
| X8 | A second call arrives with the same `Idempotency-Key` | The first answer and its entry are returned; no second entry is written | None | AC9 |
| X9 | The request names no channel, or names a channel the template does not carry | The send is refused by `rwb-comms` with 422 and MSG-GEN-001 naming the field, and the access answer names no channel and writes no entry of a send | MSG-GEN-001 (produced by `rwb-comms`) | AC1 |

No exception path of this story changes a case, a message or a task: this service answers and records, and the sending is `rwb-comms`'s and the case state is `rwb-case`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published send contract RWB-P6-E2022-CON and its fake; the conduct check, the merge, the outbox, the channel results and the ledger arrive in that contract and never as a table read |
| Negotiable | Letters, roles, areas, masking rows, mask versions and matrix versions are data; the story fixes the answer shape and the entry only |
| Valuable | No message leaves the Workbench for a role that may not send on that case, and the number the message goes to appears in no screen, list, preview, entry or event |
| Estimable | Three existing operations, one mask answer, one scope check, one entry writer, one cache, one contract-fake run |
| Small | Fits one week with its tests, because the send, the case, the ledger and the screens are other stories' |
| Testable | Each criterion below is one row in section 16, and the send facts are returned by the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Access decisions, masking and access-log entries for SMS and LINE dispatch

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.12" is in force and masking version "MASK-SIT-01" is in force
    Given the permission rows of "PM-2026.12" give RW-CASEOWN Case record "C", RW-TEAMMGR, RW-CONDUCT and RW-COMPLAIN Case record "R", and RW-PHONECOL no Case record row
    Given case "RC-2026-000777" is owned by "CO-0201" with borrower party "P-0077", and it has no legal hold and no open deviation
    Given test user "CO-0201" holds RW-CASEOWN, "U-4101" holds RW-CASEOWN with scope "OWN" and does not own case "RC-2026-000777", "U-4103" holds RW-TEAMMGR, "U-4104" holds RW-PLATADM and "U-4106" holds RW-PHONECOL
    Given the rwb-comms contract mock returns template "SMS-REMIND" "TH" version 1 with channel "SMS" and template "LINE-REMIND" "TH" version 1 with channel "LINE", both Approved and current

  Scenario: AC1 A case owner with Case record C sends an SMS and one entry is written (new, D-RCV-60)
    Given the rwb-comms contract mock returns an interaction for case "RC-2026-000777" with channel "SMS", direction "OUTBOUND", conduct check "PASSED", delivery status "DELIVERED" and reference "NSS-7781"
    When "CO-0201" sends with channel "SMS", template "SMS-REMIND", language "TH" and party "P-0077", and the route asks POST /api/recovery/access/v1/authorise with area "CASE_RECORD", right "C", case "RC-2026-000777", channel "SMS" and template "SMS-REMIND"
    Then the answer is allowed with area "CASE_RECORD", right "C", role "RW-CASEOWN", matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the answer marks "DF-ACE-078" and "DF-ACE-077" masked and carries no token, no phone number and no LINE identifier
    Then one access-log entry exists with decision code "AC-READ", actor "CO-0201", case "RC-2026-000777", area "CASE_RECORD", right "C", channel "SMS", template code "SMS-REMIND", language "TH", conduct result "PASSED", matrix version "PM-2026.12" and mask version "MASK-SIT-01"
    Then the entry holds no token, no number, no LINE identifier and no message text

  Scenario: AC2 A role with Case record R reads the messages and is refused the send (new, D-RCV-60)
    Given the rwb-comms contract mock returns three interactions for case "RC-2026-000777" with channel "SMS" and channel "LINE"
    When "U-4103" opens the case and asks the authorise path for area "CASE_RECORD" and right "R"
    Then the answer is allowed with right "R" for role "RW-TEAMMGR" and the screen shows the messages with their channel, template and delivery status
    Then the same answer is given for the roles "RW-CONDUCT" and "RW-COMPLAIN", whose Case record letter is "R" under "PM-2026.12"
    When "U-4103" asks the authorise path for area "CASE_RECORD" and right "C" on the same case
    Then the call is refused with status 403 and message MSG-P4-002 for the action "send a message"
    Then one access-log entry exists with decision code "AC-DENY", actor "U-4103", area "CASE_RECORD" and right "C", and it holds no template code, no channel and no message text

  Scenario: AC3 A role with no Case record row is refused the send (new, D-RCV-60)
    Given test user "U-4106" holds RW-PHONECOL and no permission row of RW-PHONECOL names area "CASE_RECORD" under "PM-2026.12"
    When "U-4106" asks the authorise path for area "CASE_RECORD", right "C" and case "RC-2026-000777"
    Then the call is refused with status 403 and message MSG-P4-002 for the action "send a message"
    Then one access-log entry exists with decision code "AC-DENY", actor "U-4106", area "CASE_RECORD" and right "C", and it names the case reference only
    Then no case field, no party reference and no template is returned

  Scenario: AC4 A case outside the caller's scope is not answered (new, D-RCV-60)
    Given test user "U-4101" holds RW-CASEOWN with default scope "OWN" and case "RC-2026-000777" is owned by "CO-0201"
    When "U-4101" asks the authorise path for area "CASE_RECORD", right "C" and case "RC-2026-000777"
    Then the call is refused with status 404 and message MSG-P4-003 for case "RC-2026-000777"
    Then the answer holds no field of the case, no product, no total balance and no party reference
    Then one access-log entry exists with decision code "AC-DENY", actor "U-4101", area "CASE_RECORD", right "C" and the case reference

  Scenario: AC5 The phone number and the party identifier are masked for every role (new, D-RCV-60)
    Given no masking row in "MASK-SIT-01" names "DF-ACE-078" or "DF-ACE-077" unmasked for any role
    When "U-4101" asks GET /api/recovery/access/v1/masking-policies for the field list "DF-ACE-078" and "DF-ACE-077", and "U-4104" asks the same for the same list
    Then both answers mark both fields masked under masking version "MASK-SIT-01"
    Then neither answer carries a value, a format or a fragment of the phone number or of the LINE identifier
    Then no request is made to the ACE PII service for a clear value

  Scenario: AC6 The message preview shows the template text and no personal value (new, D-RCV-60)
    Given the rwb-comms contract mock returns template "LINE-REMIND" "TH" version 1 with channel "LINE" and its template text
    When "CO-0201" previews the message for party "P-0077" and the route asks the authorise path for area "CASE_RECORD", right "C", case "RC-2026-000777" and the field list "DF-ACE-078" and "DF-ACE-077"
    Then the answer is allowed and marks both fields masked under masking version "MASK-SIT-01"
    Then the preview the screen draws holds the template text and the template code "LINE-REMIND" and no token, no LINE identifier and no value of party "P-0077"
    Then the entry of the preview carries the template code and no field value

  Scenario: AC7 The outbox sender runs under a service identity and the same check (new, D-RCV-60)
    Given the service identity of JOB-11 is a role of class "NON_HUMAN_ACTOR" with scope "ALL"
    When that identity calls GET /api/recovery/access/v1/me/permissions, and the authorise path is asked for area "CASE_RECORD" and right "C" under that identity
    Then the permission answer names role class "NON_HUMAN_ACTOR", scope "ALL", matrix version "PM-2026.12" and masking version "MASK-SIT-01", and its letters come from permission rows and from no constant in code
    Then the authorise answer is decided by the same operation, against the same rows, as a person's answer, and it is recorded in the same access-log shape
    Then no bypass branch, no default letter and no wider scope is answered for that identity

  Scenario: AC8 A send whose entry cannot be written is not answered (new, D-RCV-60)
    Given the decision-record store is forced to fail
    When "CO-0201" sends with channel "SMS" and template "SMS-REMIND" on case "RC-2026-000777"
    Then the authorise call returns status 503 with message MSG-P7-003 and no answer
    Then the answer holds no case field and no field marker, and the route does not show the send as taken
    Then the reason is logged with no token, no number and no message text

  Scenario: AC9 A repeated send with the same Idempotency-Key writes one entry (new, D-RCV-60)
    Given "CO-0201" sent with Idempotency-Key "c0ffee00-0001" and the first answer was allowed
    When the same request arrives again with Idempotency-Key "c0ffee00-0001"
    Then the first answer and its field markers are returned
    Then no second access-log entry is written and the decision-record chain holds one entry for the request

  Scenario: AC10 A blocked send leaves the conduct result in the entry (new, D-RCV-60)
    Given case "RC-2026-000777" has an open deviation "X6" lost contact
    Given the rwb-comms contract mock refuses the send with status 409 and message MSG-P6-001 naming "X6 Lost contact"
    When "CO-0201" sends with channel "SMS" and template "SMS-REMIND", and the route reports the send on the authorise path with right "C" and conduct result "BLOCKED"
    Then the access answer is allowed with right "C" and the field markers, because the role and the scope are unchanged
    Then one access-log entry exists with decision code "AC-READ", case "RC-2026-000777", channel "SMS", template code "SMS-REMIND" and conduct result "BLOCKED"
    Then the entry holds no token, no number, no LINE identifier and no message text, and the refusal message and the 409 are not produced here
```

The ten criteria above are the ones this story owns. The legacy criteria of RWB-E2-022 are served by the sending slices: legacy AC1 and AC2 by `rwb-comms` and by AC1 here, legacy AC3, AC4, AC5 and AC11 by `rwb-comms` and by the entry of AC10 here, legacy AC6, AC7 and AC8 by `rwb-comms`, legacy AC9 by AC9 here, legacy AC10 by AC8 here, and legacy AC12 by `rwb-comms` and by the answer of AC1 here.

The rights the JOB-11 service identity holds on `CASE_RECORD`, and the role code it runs under, are Not specified in the source documents (GAP-0956; ASM-1687); AC7 asserts that its answer comes from permission rows, that its role class is `NON_HUMAN_ACTOR`, that its scope is `ALL`, and that no bypass branch exists.

The authorise request and response shape used above — actor, roles, area `CASE_RECORD`, right, case reference, channel, template code, language, conduct result and field list in, and allowed, roles, area, right, matrix version, masking version, field markers and messageId out — is Not specified in the source documents (GAP-0955; ASM-1686); no field of it is a business value and it is renamed at the contract review if the published contract differs.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A right is taken from the permission rows of the matrix version in force, per role and capability area, with letters C, R, U, D and A; no letter, role or area is written in code | FSD P4 v3 A2.4; BR-P4-004; TSD P4 v3 T6.1 |
| BR2 | Sending an SMS or a LINE message on a case needs Case record C, and reading the messages on a case needs Case record R; the case must be inside the caller's scope | Legacy RWB-E2-022 sections 3 and 10; FSD P4 v3 A2.4, A2.14; TSD P4 v3 T3.2 LOV-CAPABILITY |
| BR3 | A role with no Case record row is denied; the authorise path refuses by default and never falls back to a broader role or to a default letter | FSD P4 v3 A2.4 AC-EXC-P4-004-06; Architecture v5 zero trust, deny by default |
| BR4 | The phone number `DF-ACE-078` and the party identifier `DF-ACE-077` are shown masked unless a masking row for the role and the field says unmasked, and a field with no covering row stays masked; a masked value is never returned clear and no ACE PII call is made for it | Legacy RWB-E2-022 section 17; FSD P4 v3 A2.5 AC-ALT-P4-005-01 and AC-EXC-P4-005-05; NFR-039 |
| BR5 | The conduct check, the template status, the consent and the delivery result are `rwb-comms`'s and never change the access answer; the entry records the conduct result it is told and computes none | FSD P4 v3 A2.4 VR-P4-004-1; legacy RWB-E2-022 BR1, BR4, BR8 |
| BR6 | Every allowed look and every allowed send writes one `AC-READ` entry, and every refusal one `AC-DENY` entry, in one transaction with the answer; a call that cannot be logged is refused | FSD P4 v3 A2.7 AC-P4-007-01, AC-EXC-P4-007-03 and AC-EXC-P4-007-04; DP-03; R-UNI-39 |
| BR7 | No token, phone number, LINE identifier or message text enters an access entry, an event or a log; the entry carries the case, the channel, the template code, the conduct result and the field IDs only | Legacy RWB-E2-022 section 17; NFR-040, NFR-042; TSD P4 v3 T7 |
| BR8 | An answer names the matrix version and the masking version it was decided under, and a policy change reaches the cached answer through `rwb.access.AccessPolicyChanged.v1` with no deployment | FSD P4 v3 A2.4 AC-P4-004-01; Architecture v5 slide 20 cache refresh |
| BR9 | A service identity passes the same role check as a person, and its rights come from permission rows like anyone else's | NFR-051; REQ-ACA-010; TSD P4 v3 T3.2 LOV-ROLE-CLASS with `NON_HUMAN_ACTOR` |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` in `rwb_access` under the matrix version in force; the capability areas are the LOV-CAPABILITY values read through the reference-data contract of DP-07, and the Java code holds no enum of areas, roles or letters.
- BR2 is one check on the letter of the requested right in the area `CASE_RECORD`, with the case owner or the case's team compared against the caller's scope; a missing row is a refusal, never a default.
- BR3 is the absence of a fallback: no default letter, no inherited area and no wildcard role.
- BR4 is the `masking_rule` read plus the masked default, and the absence of any value read: the field IDs travel in the request and the answer carries the markers, so a value of the number cannot enter this service.
- BR5 is the absence of every send fact from the decision except the conduct result the request carries: no template status, no consent, no delivery status and no external reference is a request field of a check, so no decision here can disagree with `rwb-comms`.
- BR6 is one `RecordAndApply` transaction on the answer and the entry, with the idempotency key of DP-09.
- BR7 is a check on the entry writer: the field list it writes is the field ID and the masked flag, and a test asserts the entry text holds no digit of a test number and no part of a LINE identifier.
- BR8 is the version pair in the answer and the cache refresh on the service's own `AccessPolicyChanged`.
- BR9 is the same authorise path applied to a role of class `NON_HUMAN_ACTOR`, with no bypass branch.

### 9. State transitions

This service holds no case, message or task state. The states it answers are the outcomes of an authorise call and the entries it writes.

| From | Event | Condition | To |
|---|---|---|---|
| No cached answer | Authorise call | The permission and masking rows are in force | Allowed or denied, with the matrix and masking versions |
| Allowed for a look | The answer is served | The `AC-READ` entry commits | Served, with the field markers |
| Allowed for a send | The send is reported | The `AC-READ` entry commits | Served, with the channel, the template code and the conduct result |
| Denied | The refusal is served | The `AC-DENY` entry commits | Refused with 403 and MSG-P4-002, or 404 and MSG-P4-003 for a case outside the scope |
| Cached under `PM-2026.12` and `MASK-SIT-01` | `rwb.access.AccessPolicyChanged.v1` | A later policy load is in force | Cached under the new versions, served from the next call |
| Cached, mixed versions | Refresh | The event names a matrix version and a mask version from different loads | Unchanged, with the mismatch raised |

| Command | Condition | Outcome |
|---|---|---|
| Authorise, right `R` | A `CASE_RECORD` row with `R` and a case in scope | Allowed, one entry with decision code "AC-READ" |
| Authorise, right `C` | A `CASE_RECORD` row with `C` and a case in scope | Allowed, one entry with decision code "AC-READ" and the send facts |
| Authorise, any right | No `CASE_RECORD` row, or no `C` where `C` is asked | Refused 403, MSG-P4-002, one entry with decision code "AC-DENY" |
| Authorise, any right | A case outside the caller's scope | Refused 404, MSG-P4-003, one entry with decision code "AC-DENY" |
| Authorise, any right | The entry cannot be written | 503, MSG-P7-003, nothing answered |

The case status, the task and the message delivery status move in `rwb-case`, `rwb-comms` and the interaction ledger; this story holds no copy of any of them and changes no state of theirs.

Access-log entries have no lifecycle of their own: they are append-only and are read by `rwb-decision`'s decision-log query.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN Case owner | Sends an SMS or a LINE message on a case it owns (`CASE_RECORD` `C`) and reads the messages, with the number and the identifier masked |
| RW-TEAMMGR Team manager | Reads messages on the cases its team and scope allow (`CASE_RECORD` `R`); may not send |
| RW-CONDUCT Conduct and QA officer | Reads the blocked contacts and their entries (`CASE_RECORD` `R`); may not send |
| RW-COMPLAIN Complaint officer | Reads the contact history of a disputed case (`CASE_RECORD` `R`); may not send |
| RW-PHONECOL and every role with no `CASE_RECORD` row | Refused by default, with an `AC-DENY` entry |
| RW-AUDIT Internal audit | Reads the access and decision entries with scope `ALL` through `rwb-decision`'s decision-log query; it calls no operation of this story |
| The service identity of JOB-11 | Passes the same path as a person, with role class `NON_HUMAN_ACTOR` and scope `ALL` (NFR-051). The rights it holds on `CASE_RECORD` are Not specified in the source documents (GAP-0956; ASM-1687) |
| SY-DECLOG Decision log writer | Writes the entry of DP-03 on behalf of this service; it is a library identity, not a caller |
| `rwb-access` itself | Reads `role`, `permission` and `masking_rule` in its own schema and writes no row of them in this story |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set, MSG-P4-002 for an absent right and MSG-P4-003 for a case outside the scope. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON. The conduct check, the consent and the legal hold are not in this table: `rwb-comms` executes them after this service has answered.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | role_code, role_name, role_class, default_scope | Read |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-ACE-078 | `contact_point` (owned by P1, read through the owner's contract of DP-05) | `contact_value`, the phone number and the LINE identifier behind the token | Not read as a value: the answer names the field and the masked marker only |
| DF-ACE-077 | `contact_point` (owned by P1, read through the owner's contract of DP-05) | `person_key` | Not read as a value: the answer names the field and the masked marker only |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` or `AC-DENY` entry: decision code, actor, case reference, area, right, channel, template code, language, conduct result, versions, field markers, time | Write |
| (outbox) | outbox library table in `rwb_access` | the record row and the `AccessPolicyChanged` row | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (idempotency) | `idempotency_key` | the stored answer of an authorise call with its key | Write |

The contact point extension rows `contact_point_ext.consent_given` (DF-EXT-015), `verified_at` (DF-EXT-017) and `failed_count` (DF-EXT-018) are `rwb-source-data`'s and are read by `rwb-comms` through its interface; this story names them and reads none of them. The template fields `template_code` (DF-REF-046), `template_version` (DF-REF-047) and `channel` (DF-REF-066) are `rwb-comms`'s and arrive as the template code of the request, never as a row of `rwb_comms`. The interaction fields DF-INT-002 to DF-INT-029 are written by `rwb-comms` through the ledger of `rwb-source-data` (DP-18) and are never read here. Field IDs are those in the Logical Data Model and Data Dictionary v9.

The unmask rows for `DF-ACE-078` and `DF-ACE-077` and the masking version in force are Not specified in the source documents (GAP-0954; ASM-1685); this story names the two fields, the mask version and the masked marker and leaves the rendering to the one masking library every screen uses.

### 12. Contract

#### 12.1 REST operations provided

None new. The decisions are served through the operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1`, owner P4 `rwb-access`; this slice adds no path, no query parameter and no response field, and decides the following behind them:

| Method | Path | Purpose | Authorization | Errors |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The role, scope and right decision for one capability area and right, with the case as the object, the send facts where the action is a send, and the field markers | The caller's own session; the answer is the decision | 401; 403 MSG-P4-002; 404 MSG-P4-003; 422 MSG-GEN-001; 503 MSG-P7-003 |
| GET | `/api/recovery/access/v1/me/permissions` | The caller's resolved roles, letters per capability area, scope, role class, matrix version and masking version | None beyond the session | 401; 503 |
| GET | `/api/recovery/access/v1/masking-policies` | The masking answer for a field list and a role, with the mask version | None beyond the session | 401; 503 |

Architecture v5 slide 14 names `POST /authorise`, `GET /me/permissions` and `/masking-policies` for `rwb-access`; TSD P4 v3 names `GET /me/session` (API-P4-012) for the same resolved view, so the resolved view is answered behind `GET /me/permissions` under R-PREC and the session read keeps its own story and its own shape. The request and response shape of `POST /authorise` for a send, and the field list the composite route sends, are Not specified in the source documents (GAP-0955; ASM-1686).

#### 12.2 REST operations consumed

None. The send facts, the case reference, the channel, the template code and the conduct result are sent in the authorise request by the composite route and the send route; this service calls no other service on this path, so the call stays one hop with the 2 s timeout of DP-11 and a circuit breaker. The send to `rwb-comms` is the route's call against RWB-P6-E2022-CON, not this story's.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | matrix or mask version | the policy kind, the old and new version, validFrom, the affected capability areas or fields, the load reference |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | the entry ID | the hash-chained `AC-READ` or `AC-DENY` entry of a look, a refusal or a send |

CloudEvents 1.0 envelope; neither payload carries a token, a phone number, a LINE identifier, a message text or any other personal field. The `AccessPolicyChanged` event is written by the policy load path of this service (RWB-P4-AD002-APP, RWB-P4-AD004-APP) in the same transaction as the rows, and this story's part is the refresh it triggers.

#### 12.4 Events consumed

None from another service. The cache refresh reads this service's own `rwb.access.AccessPolicyChanged.v1` from `rwb.access.events.v1` through an internal listener, which is not a cross-service subscription; no `rwb.comms.*`, `rwb.case.*` or `rwb.decision.*` event is read, and this story adds no subscription for a send or a delivery result. The refresh fails closed: a policy event that does not parse leaves the cache on the versions it already holds.

#### 12.5 Workflows and activities

None. This story starts no workflow and registers no activity on the `rwb-access` queue; `NoticeDispatchWorkflow` and the outbox relay are `rwb-comms`'s and `CaseWorkflow` is `rwb-case`'s.

#### 12.6 Schedules

None for this story. JOB-11 Outbox sender is a Schedule-task of the owning service in Architecture v5 slide 44 and runs in `rwb-comms` for this key; the six-monthly access review list (JOB-18) is a Temporal Schedule of `rwb-access` and belongs to the service's own story. The ACE shared Quartz tables are not used.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The roles the caller holds, their class and their default scope, including a role of class `NON_HUMAN_ACTOR` |
| `permission` | P4 (`rwb_access`) | The letters per capability area under the matrix version in force, with `CASE_RECORD` `C` and `R` |
| `masking_rule` | P4 (`rwb_access`) | The unmasked flag per role and field under the mask version in force, for `DF-ACE-078` and `DF-ACE-077` |
| `delegation_limit` | P4 (`rwb_access`) | Not read here: a message send carries no amount limit |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger entry is `rwb-decision`'s and the local record goes on `rwb.decision-record.v1` |

`contact_point`, `contact_point_ext`, `template`, `interaction`, `recovery_case` and `deviation` are other services' and are not read: the two fields are named, the values stay with `rwb-source-data`, the template stays with `rwb-comms`, the case and the deviation stay with `rwb-case` and `rwb-deviation`, and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-comms send WireMock | RWB-P6-E2022-CON | The send for case `RC-2026-000777`, party `P-0077`, templates `SMS-REMIND` and `LINE-REMIND` `TH` version 1, reference `NSS-7781`, conduct checks `PASSED` and `BLOCKED`, and the 409 for the open deviation `X6` with MSG-P6-001 |
| decision-record fake | RWB-PLT-E1027-CON | The entry write and the publish on `rwb.decision-record.v1`, including a forced failure for AC8 |
| guard and permission fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The cached answer behind the route's pre-check, the permission answer per role, and the refusal for a role without the right |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY with `CASE_RECORD`, LOV-SCOPE with `OWN`, `TEAM`, `REGION` and `ALL`, and LOV-ROLE-CLASS with `NON_HUMAN_ACTOR`, each with its version |
| gateway-bff route fake | RWB-PLT-N001-CON | The composite route of SCR-03, so the screen's own authorise, permission and masking calls and the field list can be asserted |
| policy pack fixture | this story's own test data | The `PM-2026.12` permission rows (`CASE_RECORD` `C` for `RW-CASEOWN`, `R` for `RW-TEAMMGR`, `RW-CONDUCT` and `RW-COMPLAIN`, no row for `RW-PHONECOL`), the `MASK-SIT-01` rows for `DF-ACE-078` and `DF-ACE-077`, and a later masking version for the refresh test |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations used), consumed 0 | The decisions are served on `/authorise`, `/me/permissions` and `/masking-policies` of RWB-P4-E1037-CON on `/api/recovery/access/v1` |
| Kafka | Published 2, consumed 0 from other services | `rwb.access.events.v1` and `rwb.decision-record.v1` published; the cache refresh reads this service's own topic |
| Temporal | 0 | No workflow, no activity, no task queue use |
| File | None | No file input or output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/authorise`, Java package `th.co.scb.ace.workbench.recovery.access.authorise`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which patterns have an instance in this slice: DP-01 is the read of `role`, `permission` and `masking_rule` in `rwb_access`; DP-03 is the `AC-READ` and `AC-DENY` entry; DP-07 is the LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS lists; DP-09 is the outbox, the inbox and the idempotency key; DP-11 is the authorise contract with its mock and its 2 s timeout; DP-13 is the base path; DP-19 is the composite route of SCR-03 and the field list it sends. DP-05 has an instance only as an absence — this service reads no `v_ace_*` view, names `DF-ACE-078` and `DF-ACE-077`, and the value stays with `rwb-source-data`. DP-10 has no instance here, because JOB-11 runs in `rwb-comms`; DP-18 has none either, because the ledger entry of a send is written by `rwb-comms` into `rwb-source-data`'s ledger.

Where the DP work of this legacy key sits:

- DP-05 (the contact points and the consent of `P-0077`) is `rwb-source-data`'s data read by `rwb-comms`'s route, and this story reads neither the rows nor the consent.
- DP-09 (the outbox send) and DP-10 (JOB-11 Outbox sender, every minute, in the owning service) are `rwb-comms`'s, with the retry limit of 5, the exception queue and rule R-UNI-34.
- DP-18 (the interaction ledger entry with its conduct check, delivery status and external reference) is `rwb-source-data`'s ledger, written by `rwb-comms` through its interface.
- DP-19 (SCR-03 Case record and SCR-04 Case timeline) is served through the gateway-bff composite route, and this story supplies the answer and the field markers that route carries.

This secondary slice adds no new build dependency of its own (metadata "Depends on (build)" is None): the libraries, the per-service Flyway baseline, the outbox and the gateway route are already build dependencies of the P4 service's own stories, in particular RWB-P4-E1037-CON and the policy pack path, and this story builds against the published contract RWB-P6-E2022-CON and its fake.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | REST controller | The three operations of 12.1, the problem responses with their message IDs, and the idempotency key |
| AuthoriseService | Service | Resolution of the caller's letters for `CASE_RECORD` and the right asked, the version pair in the answer, and the same path for a role of class `NON_HUMAN_ACTOR` |
| ScopeResolver | Service | BR2: the case owner, the team and the region against the caller's scope; 404 and MSG-P4-003 for a case outside it |
| MaskingPolicyService | Service | The `masking_rule` read per role and field for `DF-ACE-078` and `DF-ACE-077`, the masked default, and the mask version in the answer |
| PolicyVersionResolver | Service | The matrix version and the mask version in force, read once per refresh and held together |
| SendEntryAssembler | Service | BR7: the entry of a look, a send and a refusal with its case, channel, template code, language and conduct result, and with no value |
| AccessLogWriter | Service | The `AC-READ` and `AC-DENY` entry of DP-03 in the same transaction as the answer, with the outbox row (DP-09) |
| AuthoriseCache | Cache | The cached answer per user, area, right and object, with the matrix and mask versions; refresh on `AccessPolicyChanged`; fail closed on a mixed pair |
| PolicyChangeListener | Kafka consumer with the inbox | The service's own `AccessPolicyChanged`, deduplicated by event ID, refreshing the cache |

**Database and migrations**

- Reads `role`, `permission` and `masking_rule` in `rwb_access`; writes the decision-record entry through the library, and the inbox, outbox and idempotency rows.
- Index `ix_permission_role_area_version ON permission (role_id, capability_area, matrix_version)`, so the authorise read is one index scan in the cache-miss path.
- Index `ix_masking_field_version ON masking_rule (field_id, masking_version, role_code)`, so the mask answer for the two fields and a set of roles is one scan.
- No new table and no new column: the policy tables are the policy pack path's, and the access log is the decision-record entry (DP-03).
- Migration in the per-service Flyway sequence of DP-15: `V2022_1__access_send_indexes.sql`.

**Configuration and reference data**

- LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS through the reference-data contract of DP-07 (RWB-P3-E1043-CON); the area `CASE_RECORD`, the scopes and the role class `NON_HUMAN_ACTOR` are values of those lists, never constants.
- The matrix version `PM-2026.12` and the masking version `MASK-SIT-01` in force are read from the rows, not configured; the SIT masking label is assumed (GAP-0954; ASM-1685).
- The access entry's decision codes `AC-READ` and `AC-DENY` follow the decision-code list of the ledger, and the field markers come from the request; a send uses no code of its own (ASM-1688).
- The blocking deviation list, the consent state, the template status and the retry limit are `rwb-comms`'s and `rwb-source-data`'s data and are not read here.
- No switch of this slice's own: a screen or an action that cannot get an authorise answer must not proceed, so the authorise path has no off state. The legacy flag `rwb.comms.sms-line` stays `rwb-comms`'s and is a legacy reference here.

**Build steps**

1. `AuthoriseController` and the problem responses, with the three operations and the idempotency key; tests for the 401, 403, 404 and 503 shapes.
2. `PolicyVersionResolver` and the two index reads; test that a new matrix version is served as data with no code change.
3. `ScopeResolver` with the owner, team and region comparison; tests for AC4 and for the in-scope path of AC1.
4. `AuthoriseService` for right `R` and right `C` on `CASE_RECORD`, including the role with only `R` and the role with no row; tests for AC1, AC2 and AC3.
5. `MaskingPolicyService` with the masked default, the mask version in the answer and the no-value assertion; tests for AC1, AC5 and AC6.
6. `SendEntryAssembler` and `AccessLogWriter` in the same transaction as the answer; tests for AC1, AC3, AC8, AC9 and AC10, and the 503 when the record cannot be written.
7. `AuthoriseCache` and `PolicyChangeListener` with the version pair and the mixed-pair refusal; the refresh test with a fixed clock.
8. The contract-fake run against RWB-P6-E2022-CON, the gateway-bff route fake and the policy pack fixture, so the story builds before the send exists in the environment; plus the service-identity test of AC7.

**Feature switch.** The authorise path has no switch, because a screen that cannot be authorised must not open and a send that cannot be authorised must not leave. The legacy flag `rwb.comms.sms-line` and the service-level flag of RWB-P4-E1037-CON are other stories'.

**Done when.** The tests in section 16 pass; a `RW-CASEOWN` caller inside the scope of case `RC-2026-000777` is allowed right `C` with matrix version `PM-2026.12` and masking version `MASK-SIT-01` and leaves one `AC-READ` entry naming the case, the channel, the template code and the conduct result with no token, number or message text; a `RW-TEAMMGR`, `RW-CONDUCT` or `RW-COMPLAIN` caller is allowed only right `R`; `RW-PHONECOL` is refused with MSG-P4-002 and a case outside the scope with MSG-P4-003; `DF-ACE-078` and `DF-ACE-077` are masked for every role on every screen, list and preview with no ACE PII call; the JOB-11 service identity is decided by the same path; a send whose entry cannot be written returns 503 with MSG-P7-003 and is not shown as taken; and a repeated request with the same Idempotency-Key writes one entry.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not carry the right in the area | You cannot {action} here. Your role does not include it. | This story, on the authorise path |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, when the scope check fails |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the entry writer |
| MSG-GEN-001 | A required field of the authorise request is missing | Enter {field}. | This story, on the request validation; also `rwb-comms`, for a missing channel or template code |
| MSG-GEN-004 | The cached policy was replaced while the call was in flight | Someone else changed this record. Reload it to see their change. | This story, on the version check |
| MSG-P6-001 | A contact stop applies | Contact with this customer is stopped for {reason}. | `rwb-comms`, from its conduct check, not this story |
| MSG-P6-002 | No consent for the channel | The customer has not consented to {channel}. Use another channel. | `rwb-comms`, from its conduct check, not this story |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. | `rwb-comms`, not this story |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. | `rwb-comms`, from the case facts, not this story |
| MSG-GEN-006 | NSS or LINE OA is unavailable | {system} is not available. Your request is queued and will be retried. | `rwb-comms`, not this story |

The {action} value in MSG-P4-002 names the action and nothing else — for a message, "send a message" or "read the messages of this case" — and the problem response carries the capability area in its `detail` beside the message ID, so a refusal is diagnosable without any template or channel content. Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request.

### 15. Screens and states

No screen is built here. The screens are the gateway route's and `rwb-comms`'s, and they reach this service through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON):

| Screen | State | What this story supplies |
|---|---|---|
| SCR-03 Case record | Editable | The `CASE_RECORD` `C` or `R` answer behind the Send message action and the field markers that keep `DF-ACE-078` and `DF-ACE-077` masked |
| SCR-03 Case record | Send message, preview | The mask answer for the two fields in the preview, so the template text shows and no personal value does |
| SCR-04 Case timeline | Loading | The `CASE_RECORD` `R` answer per message, with the channel, the template and the delivery status supplied by the route |
| SCR-04 Case timeline | Filtered | The same answer with the scope applied, so a case outside the scope returns 404 and MSG-P4-003 |
| SCR-09 Exception queue | List | No answer of this story; the queue is `rwb-comms`'s and lists sends that failed after the retry limit |
| SCR-43 Roles and access | List | The `role`, `permission` and `masking_rule` rows this answer is taken from, with their versions (E8; by file load before) |
| SCR-03 Case record | Denied | The problem response of MSG-P4-002 or MSG-P4-003 behind it, with the `AC-DENY` entry |

The panel layout, the masked rendering and the composite route's field list are Not specified in the source documents (GAP-0955; ASM-1686); the screen stories belong to `rwb-comms` and `rwb-case`, and this story changes no screen behaviour.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-022-01 | AC1, AC4, AC5, BR1, BR4 | Contract | Party `P-0077` with a verified `MOBILE` contact point and consent `GIVEN`; `SMS-REMIND` `TH` v1; NSS stub reference `NSS-7781`; the send and the conduct check are the contract fake's, and this story asserts the answer, the scope, the field markers and the one entry |
| TC-E2-022-02 | AC1, AC6, BR4 | Contract | Party `P-0077` with a verified `LINE` contact point and consent `GIVEN`; `LINE-REMIND` `TH` v1; the LINE OA stub delivered and then read; the preview shows the template text and no personal value |
| TC-E2-022-03 | AC10, BR3 | Contract | Open deviation `X6` lost contact; the 409 and MSG-P6-001 are the contract fake's and the entry's conduct result `BLOCKED` is this story's |
| TC-E2-022-04 | AC10, BR2 | Contract | Open deviation `X1` with the contact stop on |
| TC-E2-022-05 | AC10, BR4 | Contract | `MOBILE` contact point with consent `WITHDRAWN`; MSG-P6-002 names `SMS` |
| TC-E2-022-06 | AC1, BR8 | Contract | `SMS-REMIND` `TH` v1 Withdrawn; the withdrawal is the contract fake's and the access answer names no template status |
| TC-E2-022-07 | AC1, AC8, BR6 | Contract | Notification path unavailable for six attempts; the retry is JOB-11 in `rwb-comms` and this story asserts the answer and the entry only |
| TC-E2-022-08 | AC10, BR1 | Contract | NSS result `FAILED` with failed count 0; the delivery status and the failed count are `rwb-comms`'s and `rwb-source-data`'s |
| TC-E2-022-09 | AC9, BR6 | Component | The same Idempotency-Key `c0ffee00-0001` twice |
| TC-E2-022-10 | AC8, BR7 | Component | Open deviation `X6` with the decision-record store forced to fail; 503 MSG-P7-003, no answer and no data |
| TC-E2-022-11 | AC10, BR5 | Contract | Legal hold true; the 409 and MSG-P3-004 are the contract fake's |
| TC-E2-022-12 | AC1, BR2 | Contract | No channel in the request; the 422 and MSG-GEN-001 are the contract fake's and no entry carries a channel or a template code |
| TC-E2-022-13 | AC2, AC3, AC7, BR3, BR9 | Component | `U-4106` holding `RW-PHONECOL` with no `CASE_RECORD` row, `U-4103` holding `RW-TEAMMGR` with `CASE_RECORD` `R` only, and the JOB-11 identity of class `NON_HUMAN_ACTOR` with scope `ALL`; 403 with MSG-P4-002 and one `AC-DENY` entry each |
| TC-E2-022-14 | AC8, BR7 | NFR | The decision-record write forced to fail on ten refusals; none is recorded as allowed and no answer is served |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Contract where the rule lives in the `rwb-comms` contract and to Component where the rule lives here, Access to Component and Resilience to NFR. AC4, AC6 and AC7 are this slice's own criteria; they are asserted in the rows that exercise the same answer — the scope of the send in TC-E2-022-01, the preview of the LINE template in TC-E2-022-02, and the refusal and the service identity in TC-E2-022-13 — and no separate legacy id is invented for them. The integration copy of the whole set belongs to the integration harness story of this legacy key and is not written here, so no integration-suffixed id appears in this table.

### 17. Guardrails

- No business value in code: the letters C, R, U, D and A, the capability areas, the roles, the scopes, the masking rows, the mask format and the matrix and mask versions are data rows; the Java code holds no letter, area, role or version literal (BR-P4-004, BR-P4-005). A test proves that a new role, area or masking row needs no build.
- No personal data in logs, events, tests, workflow history or prompts: no token, phone number, LINE identifier or message text enters an access entry, an event, a log line or a fixture. The entry carries the actor reference, the case reference, the channel, the template code, the conduct result, the field IDs and the masked markers. Workflow history is not used because this story starts no workflow.
- No read of another service's tables and no cross-schema read (DP-01): `contact_point`, `contact_point_ext`, `template`, `interaction`, `recovery_case`, `deviation` and `decision_log_entry` are never queried here.
- ACE data only through the owner's contract or a `v_ace_*` view of this service; this story reads no ACE view at all and calls no ACE PII service, so a clear phone number or LINE identifier cannot enter it (DP-05, REQ-DRI-006).
- The mask answer is data, not code: the field list, the role and the mask version decide it, and a field with no covering row is masked. The number and the identifier stay tokens in the Workbench and the ACE notification path detokenizes them (legacy RWB-E2-022 section 17).
- An answer is never served without its entry, and the answer and the entry commit in one transaction (R-UNI-39); a call that cannot be logged is an error, not a silent success.
- The cache fails closed: an unparseable or mixed policy event leaves the versions in force, and a missing policy row is a refusal, never a default allow.
- The authorise path has no off switch, because a screen or a send that cannot be authorised must not proceed; the legacy message flag stays `rwb-comms`'s.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-004 | SMS and LINE through the bank's channel platforms, result on the case | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | BR1, BR2, BR6, BR7; R-UNI-33, R-UNI-34, R-UNI-40 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-06, TC-E2-022-07, TC-E2-022-08, TC-E2-022-09, TC-E2-022-12, TC-E2-022-13 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | BR5, BR6, BR7; R-UNI-04, R-UNI-05, R-UNI-20, R-DEV-16, R-UNI-39 | TC-E2-022-03, TC-E2-022-04, TC-E2-022-10, TC-E2-022-11, TC-E2-022-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | BR4; R-UNI-10 | TC-E2-022-05 |
| REQ-ILG-010 | Messages dispatched write their result to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | BR6; R-UNI-34 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-08 |
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, requirement table (E1) | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | BR4, BR7 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-07 |

| Legacy reference | Where it is kept |
|---|---|
| Roles RW-CASEOWN with Case record C, and RW-TEAMMGR, RW-CONDUCT and RW-COMPLAIN with Case record R | Metadata, sections 1, 3, 7, 8, 10 |
| The refusal of RW-PHONECOL with MSG-P4-002, and the 404 of a case outside the scope with MSG-P4-003 | Sections 5, 7 (AC3, AC4), 10, 14 |
| Case `RC-2026-000777`, party `P-0077`, templates `SMS-REMIND` and `LINE-REMIND` `TH` v1, reference `NSS-7781` | Background, AC1, AC2, AC6, AC10, sections 3, 12.8, 16 |
| The phone number and the LINE identifier stay tokens (legacy section 17), and no personal value in the entry | Sections 1, 2, 4, 7 (AC5, AC6), 11, 17 |
| MSG-P6-001, MSG-P6-002, MSG-P6-003, MSG-P3-004, MSG-GEN-006 produced by `rwb-comms` | Section 14, exception paths |
| Legacy test set TC-E2-022-01 to TC-E2-022-14 | Section 16 |
| Legacy key RWB-E2-022, story RWB-P4-E2022-APP, contract RWB-P6-E2022-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The `rwb-comms` slice of this legacy key, RWB-P6-E2022-APP with RWB-P6-E2022-CON: `POST /cases/{caseId}/messages`, the conduct check, the template catalog and the merge, the outbox write, JOB-11 Outbox sender with its retry limit of 5 and the exception queue, the NSS and LINE OA results and the failed count call.
- The interaction ledger entry and its delivery status, and the contact point facts — the consent `GIVEN` and `WITHDRAWN`, the verification and the failed count — which are `rwb-source-data`'s (P1) behind its contract and written by `rwb-comms` (DP-18).
- `rwb-case` (P3): the case, its owner, its team, its legal hold, SCR-03 Case record and SCR-04 Case timeline as screens, and the deviation `X6`/`X1` facts of `rwb-deviation` (S8).
- `rwb-decision` (P7): the central decision ledger, its query and the audit read of the entries.
- The policy pack load path of this service — the reference loads, their approval, verification and rollback, and the rows of `PM-2026.12` and `MASK-SIT-01` themselves (RWB-P4-AD002-APP, RWB-P4-AD004-APP).
- The delegation of authority table and its lookup (RWB-P4-E2013-APP), role, scope and sign-in administration, break-glass, and the six-monthly access review list (JOB-18).
- The gateway-bff composite route itself, its session handling and its own Helm chart (a platform story of RWB-PLT-N001-CON), and the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of the authorise path (an OPS story of this legacy key).
- The integration harness of this legacy key and its copies of the test cases.
- Letters through WIN (RWB-E2-021), messages sent automatically by route rules (Epic 3), the breach path for a contact sent while a block is on (Epic 7), and self-service on LINE and HOME.SCB (Epic 4).
