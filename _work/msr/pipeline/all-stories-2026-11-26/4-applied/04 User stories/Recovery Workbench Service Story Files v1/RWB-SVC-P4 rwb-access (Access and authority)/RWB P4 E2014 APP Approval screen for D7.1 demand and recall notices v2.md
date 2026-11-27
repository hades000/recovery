# RWB-P4-E2014-APP Approval screen for D7.1 demand and recall notices

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P4-AJ |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E2014-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-APD-002, REQ-APD-006) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-014 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E2014-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer, legal counsel and head of litigation who decides a D7.1 demand or recall notice**, I want **an access answer that says whether my role carries the Litigation right to open the notice and to approve, change, refuse or return it, which version of the permission matrix and of the masking policy that answer was taken from, and an access-log entry that names the notice and the case but never the addressee's address**, so that **the first decision in the Workbench is taken by a role that may take it and is recorded as a look at that notice, and no screen opens on a notice whose address reaches a log**.

Inside `rwb-access` this is the access slice of the approval screen of legacy RWB-E2-014:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The slice delivers three answers and one record: the authorise decision for capability area `LITIGATION` with right `R` on opening a notice and right `A` on deciding it, the resolved permission answer for the caller, the masking answer for the addressee postal address `DF-PTY-016` (field `value_token` of `contact_point`, over `v_ace_contact.contact_value`), and the access-log entry written as a decision-record entry of DP-03 on every allowed read (`AC-READ`) and every refusal (`AC-DENY`).
- The slice builds no screen. The approval queue SCR-10, the decision screen SCR-11 and the notice approval panel SCR-18 are `rwb-decision`'s, served through the gateway-bff composite route; the notice itself is `rwb-comms`'s; the case facts, the case state and the case-owner task are `rwb-case`'s.
- The preparer rule of legacy BR3 and CTL-05 — a person may not approve what they prepared — is executed by `rwb-decision`. `rwb-access` supplies the letter `A` for the capability area and the holder or routed-role check, and nothing else; it never learns who the preparer is, so a slip in this slice cannot let a preparer approve, and a correct answer here cannot stop one on its own.
- The policy pack is data: permission rows under matrix version `PM-2026.12`, masking rows under masking version `MASK-SIT-01`. The load path that writes those rows is `rwb-access`'s own and is out of this story (RWB-P4-AD002-APP, RWB-P4-AD004-APP).
- The masking version in force for SIT is assumed `MASK-SIT-01` (GAP-0933; ASM-1658); no mask format for a postal address is fixed by any source, so this story names the field and the version and never a rendering (GAP-0931; ASM-1657).

The rights carried from the legacy story are unchanged: `RW-LITOFF`, `RW-LEGAL` and `RW-HEADLIT` hold Litigation `A` for a D7.1 notice they did not prepare, `RW-CASEOWN` holds Litigation `R` and receives the rejected-notice task without the right to approve, and internal audit reads with scope `ALL`.

### 2. Business rationale

A demand fee notice sent on the wrong authority is a Bank of Thailand finding, and an approval that no one can prove was authorised is the same finding one step later. The legacy story proved the decision; this slice proves the authorisation behind it. Today the right to approve a notice is spread over role documents and manual checks, and the address of the addressee is copied into working files and log lines that no one reviews. Under Architecture v5 the authorise answer and the masking answer come from `rwb-access` as data, with the matrix version and the mask version naming the policy the answer was taken from, and every look at a notice is an append-only entry in the same ledger as the decisions.

This story carries controls CTL-05 (a preparer may not decide, enforced by `rwb-decision` on the letter this slice supplies), CTL-14 (only an approved notice leaves) and the audit expectation behind NFR-042 (every read of the case store and the document store is logged). It meets REQ-APD-002 and REQ-APD-006 on the access side and supports the measure notices sent with an approval entry (target 100 percent) and the measure rule and limit changes made without a code release (target 100 percent).

The realignment changes the mechanism, not the business rule:

1. The permission rows and the masking rows of the monolith's recovery schema become `rwb-access`'s own tables in `rwb_access` (DP-01), versioned by matrix version and mask version, so a change of rights or of masking needs an approved load and no release.
2. The synchronous `RecoveryAccessGuard` call inside the monolith becomes the published authorise contract, cached, with one hop and a 2 s timeout (DP-11); the screen and the services ask `rwb-access` and hold the answer for the life of the cache entry.
3. The decision-log writer inside the monolith becomes the local decision-record library of DP-03, so an `AC-READ` or `AC-DENY` entry is hash-chained and published on `rwb.decision-record.v1` where `rwb-decision`'s ledger and the audit query already read.
4. The access event that the monolith never sent becomes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, and every holder of a cached answer — this service's own cache first — refreshes on it, so a new masking version is in force at the next call with no deployment.
5. The ACE data behind the masked field stays where it is: the address value is read through `rwb-source-data`'s contract by whoever displays it, and `rwb-access` answers only that the field is masked and under which version (DP-05).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P7-E2014-CON | The published notice and approval contract this slice is tested against: the notice `N-0201` for case `RW-2026-000123` with template `DEMAND-MTG` version 2 in language `TH` under rule `R-LIT-03` version `LIT-2026.12` and preparer `U-9211`, and the approval `A-0201` in state `WAITING` for route role `RW-LITOFF`, with its contract fakes. The request and response shape of the authorise call itself is Not specified in the source documents (GAP-0932; ASM-1656) |
| Permission matrix `PM-2026.12` `IN_FORCE` | The rows this slice answers from, loaded by the policy pack path (RWB-P4-AD002-APP, RWB-P4-AD004-APP): `LITIGATION` `A` for `RW-LITOFF`, `RW-LEGAL` and `RW-HEADLIT`, `LITIGATION` `R` for `RW-CASEOWN`, `REPORTING` and every area `R` for `RW-AUDIT` with scope `ALL`, and no `LITIGATION` row for `RW-PHONECOL` |
| Masking version `MASK-SIT-01` in force | The rows for `DF-PTY-016` covering `RW-LITOFF`, `RW-LEGAL`, `RW-HEADLIT` and `RW-CASEOWN` with `unmasked` false, so the addressee postal address is masked for every role that decides a D7.1 notice, and no row at all for a field outside the pack, which stays masked by default. The version label is assumed for SIT (GAP-0933; ASM-1658) |
| Test users in SIT | `U-9211` holds `RW-LEGAL` and prepared `N-0201`; `U-9212` and `U-9214` hold `RW-LITOFF`; `U-9213` holds `RW-HEADLIT`; `U-9215` holds `RW-CASEOWN`; `U-9216` holds `RW-AUDIT`; `U-9217` holds `RW-PHONECOL` |
| The decision-record library and its topic | `rwb.decision-record.v1` and the local library of DP-03, so an access entry is written, chained and published in one transaction with the answer |
| gateway-bff composite route | The route of DP-19 that carries the screen's authorise, permission and masking calls to this base path, with the 2 s timeout of DP-11 |

Business preconditions carried from RWB-E2-014:

- A D7.1 notice carries no amount limit, and delegation item 2.1.3 (delay of legal action) does not apply to issuing a notice; no `delegation_limit` row is read on this path.
- Templates `DEMAND-MTG`, `DEMAND-MTG-B` and `RECALL-MTG` are Approved in language `TH`; template status is `rwb-comms`'s and does not change the authorise answer.
- The input age limits are parameter rows read by `rwb-decision`; they do not change the authorise answer.
- Every refusal is answered with MSG-P4-002 naming the action and the capability area, and no notice content (FSD P4 v3 A2.4 VR-P4-004-1).

### 4. Flow

1. Litigation officer: opens SCR-10 Approval queue and selects the D7.1 item for notice `N-0201` of case `RW-2026-000123`.
2. gateway-bff composite route: on the screen open, calls `POST /api/recovery/access/v1/authorise` on this service with the caller's user reference, the roles the session resolved, capability area `LITIGATION`, right `R`, the notice and case as the object reference, and the field list the screen will render, `DF-PTY-016`.
3. `AuthoriseService`: reads the caller's permission rows for `LITIGATION` from `permission` in `rwb_access` under the matrix version in force, unions the letters of every role the caller holds, and answers `allowed` with right `R`, the roles that carry it, `matrixVersion` `PM-2026.12` and `maskingVersion` `MASK-SIT-01`.
4. `MaskingPolicyService`: reads the `masking_rule` rows for `DF-PTY-016` and the caller's roles under the mask version in force and answers masked. Where no row covers the field for any of the caller's roles the answer is masked as well, so the default is refuse rather than show (FSD P4 v3 A2.5, AC-EXC-P4-004-05). No value of the address is read, echoed or cached by this service.
5. `AccessLogWriter`, in the same transaction as the answer: writes the decision-record entry of DP-03 with decision code `AC-READ`, the actor, the notice reference, the case reference, the capability area, the right, the matrix version, the mask version and the field markers, with `DF-PTY-016` marked masked and no value; publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` through the outbox.
6. The screen draws the notice, the case facts and the rule and template versions it received from `rwb-decision`, `rwb-case` and `rwb-comms`, with the address field rendered masked; the screen itself is not this story's.
7. Litigation officer: approves, or changes the template variant and approves, or refuses with a reason. The `rwb-decision` approve or refuse call runs its own checks first and asks this service for right `A` on area `LITIGATION` for the same object and the routed role.
8. `AuthoriseService`, right `A`: answers `allowed` when a permission row of one of the caller's roles holds the letter `A` for `LITIGATION` under the matrix version in force and the role the approval routes to is one of the caller's roles; otherwise it refuses with 403 and MSG-P4-002 for the named action and area.
9. `AccessLogWriter`, on that refusal: writes `AC-DENY` with the actor, the capability area, the right, the approval reference, the matrix version and the reason code, and with no notice field, no template code, no rule version and no value; `rwb-decision` then keeps its own approval and decision entries.
10. The preparer check: `rwb-decision` compares the preparer it holds on the approval with the caller and returns 409 with MSG-P7-002. This service is not called again and records nothing, because the approval was never authorised as a decision by anyone.
11. A policy pack load by the service's own administration path commits new `permission` or `masking_rule` rows and writes the outbox row for `rwb.access.AccessPolicyChanged.v1` with the new matrix or masking version; the load itself is RWB-P4-AD002-APP and RWB-P4-AD004-APP.
12. The cache-refresh listener of this service reads that event from `rwb.access.events.v1` and replaces the cached answer for the affected roles; the next authorise call answers with the new version and a new mask answer, with no deployment and no restart, and the answer never mixes a matrix version with a mask version from a different policy load.
13. Internal audit (`RW-AUDIT`, scope `ALL`): reads the entries through `rwb-decision`'s decision-log query, where `AC-READ` and `AC-DENY` entries sit beside the approval entries of the same notice.

Every answer and its access-log entry commit in one transaction (DP-03, R-UNI-39), so a call that cannot be logged is refused rather than answered (FSD P4 v3 AC-EXC-P4-007-03), and a repeated call with the same `Idempotency-Key` returns the first answer without a second entry.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds no LITIGATION row at all | Refused with 403; one `AC-DENY` entry with area `LITIGATION` and the right asked; nothing shown | MSG-P4-002 | AC7 |
| X2 | The caller holds `LITIGATION` `R` and asks for right `A` | Refused with 403 for the named action; one `AC-DENY` entry with right `A`; the approval is unchanged | MSG-P4-002 | AC3 |
| X3 | The routed role of the approval is not one of the caller's roles | Refused with 403; one `AC-DENY` entry naming the right and the approval reference; no approval change | MSG-P4-002 | AC3 |
| X4 | No masking row covers the field for any of the caller's roles | The field is answered masked under the mask version in force; the entry marks it masked; no value is read | None | AC5 |
| X5 | The decision record of the access entry cannot be written | The call returns 503, no answer and no data; the reason is logged; the cache is unchanged | MSG-P7-003 | BR7 |
| X6 | A second call arrives with the same `Idempotency-Key` | The first answer and its entry are returned; no second entry is written | None | BR7 |
| X7 | A matrix version and a mask version arrive from two different policy loads | The cache refuses the mixed pair, keeps the versions it already holds and raises the mismatch; the caller gets the older consistent pair | None | AC6 |
| X8 | The policy event arrives before the cache is warm | The first call reads the rows directly, writes its entry and warms the cache from the same rows | None | AC6 |

An answer is never served without its entry and never without naming both policy versions; a call whose entry fails is an error, not a silent success.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published approval and notice contract RWB-P7-E2014-CON and its fake; the notice content, the case facts and the rule version arrive in the request or in the screen, never as a table read |
| Negotiable | Letters, roles, areas, masking rows, mask formats and versions are data; the story fixes the answer shape and the entry only |
| Valuable | The screen cannot open or decide a notice without a current authorise answer, and the address never leaves the owning service or enters a log |
| Estimable | Three endpoints, one cache, one masking answer, one entry writer, one index migration |
| Small | Fits one week with its tests, because the screen, the approval and the notice are other stories' |
| Testable | Every criterion below is one test case in section 16; the approval and notice facts are returned by the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Access decisions and access-log entries for D7.1 demand and recall notices

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.12" is in force and masking version "MASK-SIT-01" is in force
    Given test user "U-9211" holds RW-LEGAL, test users "U-9212" and "U-9214" hold RW-LITOFF, test user "U-9213" holds RW-HEADLIT, test user "U-9215" holds RW-CASEOWN, test user "U-9216" holds RW-AUDIT with scope "ALL" and test user "U-9217" holds RW-PHONECOL
    Given the rwb-decision contract mock returns notice "N-0201" for case "RW-2026-000123", template "DEMAND-MTG" version 2 in language "TH" under rule "R-LIT-03" version "LIT-2026.12", prepared by "U-9211"
    Given the rwb-decision contract mock returns approval "A-0201" on that notice in state "WAITING" for route role "RW-LITOFF"

  Scenario: AC1 Opening a notice for approval reads LITIGATION R and marks the address masked (new, D-RCV-60)
    Given the rwb-decision contract mock returns approval "A-0201" of notice "N-0201" for case "RW-2026-000123" waiting for role RW-LITOFF
    When "U-9212" opens the item and the composite route calls POST /api/recovery/access/v1/authorise with area "LITIGATION", right "R", notice "N-0201" and the field list "DF-PTY-016"
    Then the answer is allowed with area "LITIGATION", right "R", the role "RW-LITOFF", matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the answer marks "DF-PTY-016" masked and carries no value of the addressee address
    Then one access-log entry exists with decision code "AC-READ", actor "U-9212", notice "N-0201", case "RW-2026-000123", area "LITIGATION", matrix version "PM-2026.12" and the field marker "DF-PTY-016" as masked
    Then the entry holds no value of the addressee address and no template content

  Scenario: AC2 Approving reads LITIGATION A for the routed role (new, D-RCV-60)
    Given the rwb-decision contract mock returns approval "A-0201" of notice "N-0201" waiting for role RW-LITOFF
    When "U-9212" approves it, and the approve call asks POST /api/recovery/access/v1/authorise with area "LITIGATION", right "A", approval "A-0201", actor "U-9212" and route role "RW-LITOFF"
    Then the answer is allowed with right "A" because the permission row of RW-LITOFF in "PM-2026.12" holds the letter "A" for "LITIGATION"
    Then the answer names "RW-LITOFF" as the role that carries the item and the request's route role matches it
    Then no "AC-DENY" entry is written for that action
    Then the approval and its decision entry are "rwb-decision"'s and this service writes none

  Scenario: AC3 A role with only LITIGATION R is refused the approve action (new, D-RCV-60)
    Given the rwb-decision contract mock returns approval "A-0201" of notice "N-0201" waiting for role RW-LITOFF
    When "U-9215" calls the authorise path with area "LITIGATION", right "A", approval "A-0201" and route role "RW-LITOFF"
    Then the call is refused with status 403 and message MSG-P4-002 for the action "approve a D7.1 notice" and the area "LITIGATION"
    Then one access-log entry exists with decision code "AC-DENY", actor "U-9215", area "LITIGATION", right "A" and approval "A-0201"
    Then the answer and the entry hold no notice field, no template code, no rule version and no address value

  Scenario: AC4 Legal counsel and Head of Litigation hold LITIGATION A (new, D-RCV-60)
    Given the rwb-decision contract mock returns approval "A-0201" of notice "N-0201" escalated to route role "RW-HEADLIT" with escalation level 1
    When "U-9211" asks the authorise path for area "LITIGATION" and right "A"
    Then the answer is allowed for role "RW-LEGAL" and marks "DF-PTY-016" masked under masking version "MASK-SIT-01"
    Then the preparer rule is not applied here: rwb-decision refuses the approval of the preparer with 409 MSG-P7-002 on this letter
    When "U-9213" asks the authorise path for area "LITIGATION", right "A" and route role "RW-HEADLIT"
    Then the answer is allowed for role "RW-HEADLIT" and the request's route role matches the escalated route role
    Then neither answer carries a value of the addressee address

  Scenario: AC5 A field with no masking row is masked by default (new, D-RCV-60)
    Given no masking row in "MASK-SIT-01" covers "v_ace_customer.date_of_birth" for any role
    When "U-9212" asks GET /api/recovery/access/v1/masking-policies for that field
    Then the answer is masked under masking version "MASK-SIT-01"
    Then the answer carries no value and no format of the field

  Scenario: AC6 A policy change reaches the cached answer without a deployment (new, D-RCV-60)
    Given the cached answer for "U-9212" holds masking version "MASK-SIT-01"
    When the policy pack load commits a masking row set under a masking version later than "MASK-SIT-01" and publishes rwb.access.AccessPolicyChanged.v1
    Then the next authorise call for "U-9212" answers with the later masking version and the mask answer of that version
    Then no deployment, restart or cache flush is performed and the matrix version in the answer stays "PM-2026.12"
    Then the answer never pairs the new masking version with a matrix version from a different load

  Scenario: AC7 A role with no LITIGATION row is denied by default (new, D-RCV-60)
    Given test user "U-9217" holds RW-PHONECOL and no permission row of RW-PHONECOL names area "LITIGATION" under "PM-2026.12"
    When "U-9217" calls the authorise path with area "LITIGATION" and right "R"
    Then the call is refused with status 403 and message MSG-P4-002
    Then one access-log entry exists with decision code "AC-DENY", actor "U-9217", area "LITIGATION" and right "R"
    Then no case, notice or field data is returned

  Scenario: AC8 A refusal names the action and the area and carries no notice content (new, D-RCV-60)
    Given the rwb-decision contract mock returns approval "A-0201" of notice "N-0201" for case "RW-2026-000123" with template "DEMAND-MTG" version 2 under rule "R-LIT-03" version "LIT-2026.12"
    When "U-9215" asks the authorise path for area "LITIGATION" and right "A" on approval "A-0201"
    Then the problem response names the action "approve a D7.1 notice" and the area "LITIGATION" and its messageId is MSG-P4-002
    Then the problem response holds no notice field, no case number, no product, no total balance, no template code, no rule version and no address value
    Then the "AC-DENY" entry holds the actor, the area, the right and the approval reference only
```

The eight criteria above are the ones this story owns; the legacy AC1 to AC10 and the legacy test cases are carried by `rwb-decision` (RWB-P7-E2014-APP) and `rwb-comms` (RWB-P6-E2014-APP), and the legacy test set is kept here in section 16 against this slice's assertions.

The authorise request and response shape used above — actor, roles, area, right, object reference, route role and field list in, and allowed, roles, area, right, matrix version, masking version, field markers and messageId out — is Not specified in the source documents (GAP-0932; ASM-1656); no field of it is a business value and it is renamed at the contract review if the published contract differs.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A right is taken from the permission rows of the matrix version in force, per role and capability area, with letters C, R, U, D and A; no letter, role or area is written in code | FSD P4 v3 A2.4; BR-P4-004; TSD P4 v3 T6.1 |
| BR2 | Opening a D7.1 demand or recall notice for approval needs `LITIGATION` R; approving, changing, refusing or returning it needs `LITIGATION` A | Legacy RWB-E2-014 section 10; FSD P4 v3 A2.4; TSD P4 v3 T3.2 LOV-CAPABILITY |
| BR3 | A role with no `LITIGATION` row is denied; the authorise path refuses by default and never falls back to a broader role or to a default letter | FSD P4 v3 A2.4 AC-EXC-P4-004-06; Architecture v5 zero trust, deny by default |
| BR4 | A person may not approve what they prepared: the preparer rule is executed by `rwb-decision`, and `rwb-access` supplies the letter `A` and the holder or routed-role check only | Legacy RWB-E2-014 BR3; CTL-05; Admin and access model, section 6.2 |
| BR5 | A personal field is shown masked unless a masking row for the role and the field says unmasked, and a field with no covering row stays masked | FSD P4 v3 A2.5 AC-EXC-P4-004-05; BR-P4-005 |
| BR6 | The authorise answer depends on the rights and the policy versions only: the age of an input, the template status and the presence of a reason are `rwb-decision`'s checks and never change the access answer | FSD P4 v3 A2.4 VR-P4-004-1; legacy RWB-E2-014 BR4, BR5, BR6 |
| BR7 | Every allowed read of a notice for approval writes one `AC-READ` entry and every refusal one `AC-DENY` entry, in one transaction with the answer; a call that cannot be logged is refused | FSD P4 v3 A2.7 AC-P4-007-01, AC-EXC-P4-007-03 and AC-EXC-P4-007-04; DP-03; R-UNI-39 |
| BR8 | An answer names the matrix version and the masking version it was decided under, and a policy change reaches the cached answer through `rwb.access.AccessPolicyChanged.v1` with no deployment | FSD P4 v3 A2.4 AC-P4-004-01; Architecture v5 slide 42 cache refresh |
| BR9 | No personal data in the entry: the access-log entry carries the field ID and a masked marker, never a value, and the address value never leaves the owning service | Legacy RWB-E2-014 section 17; NFR-042; TSD P4 v3 T7 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` in `rwb_access` under the matrix version in force; the capability areas are the LOV-CAPABILITY values read through the reference-data contract of DP-07, and the Java code holds no enum of areas, roles or letters.
- BR2 and BR3 are one check on the letter of the requested right in the area `LITIGATION`, with the routed role compared against the caller's roles; a missing row is a refusal, never a default.
- BR4 is deliberately absent here: the approval carries the preparer and `rwb-decision` compares it before it calls this service for right `A`. This service never receives a preparer reference, so it cannot be the place where the rule is lost.
- BR5 is the `masking_rule` read plus the default; the mask format is the library's, because no source fixes a rendering for a postal address (GAP-0931; ASM-1657).
- BR6 is the absence of any notice field in the authorise request except the object reference: no input age, no template status and no reason code is sent, so no check here can disagree with `rwb-decision`.
- BR7 is one `RecordAndApply` transaction on the answer and the entry, with the idempotency key of DP-09.
- BR8 is the version pair in the answer and the cache refresh on the service's own `AccessPolicyChanged`.
- BR9 is a check on the entry writer: the field list it writes is the field ID and the masked flag, and a test asserts the entry text holds no digit of the address.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No cached answer | Authorise call | The policy rows are in force | Allowed or denied, with the matrix and masking versions |
| Allowed | The answer is served | The `AC-READ` entry commits | Served, with the field markers |
| Denied | The refusal is served | The `AC-DENY` entry commits | Refused with 403 and MSG-P4-002 |
| Cached under version `PM-2026.12` / `MASK-SIT-01` | `rwb.access.AccessPolicyChanged.v1` | A later policy load is in force | Cached under the new versions, served from the next call |
| Cached, mixed versions | Refresh | The event names a matrix version and a masking version from different loads | Unchanged, with the mismatch raised |

| From | Event | Condition | To |
|---|---|---|---|
| `LOADED` | The policy pack load is approved | The approver is not the loader | `APPROVED` |
| `APPROVED` | The valid-from date is reached | None | `IN_FORCE`, and `AccessPolicyChanged` is published |
| `IN_FORCE` | The next version is approved | None | `SUPERSEDED` |

The second table is the lifecycle of the rows this story reads, owned by RWB-P4-AD002-APP and RWB-P4-AD004-APP; this story reads the version in force and publishes nothing on that path itself.

Access-log entries have no lifecycle of their own: they are append-only and are read by `rwb-decision`'s decision-log query.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF Litigation officer | Opens a D7.1 notice for approval (`LITIGATION` R) and approves, changes, refuses or returns one they did not prepare (`LITIGATION` A) |
| RW-LEGAL Legal counsel | The same rights as RW-LITOFF on the same notice, from the same rows |
| RW-HEADLIT Head of Litigation | The same rights, on the item escalated to the route role RW-HEADLIT |
| RW-CASEOWN Case owner | Opens the case and the rejected-notice task (`LITIGATION` R); may not approve (`LITIGATION` A is refused) |
| RW-AUDIT Internal audit | Reads the access and decision entries with scope `ALL`, and the policy versions they were decided under |
| RW-PHONECOL and every role with no `LITIGATION` row | Refused by default, with an `AC-DENY` entry |
| SY-CASEWF, SY-DECLOG | Service identities: the case workflow's read of the case authorise answer and the decision-record library's write of the entry |

The preparer rule is not in this table: `rwb-decision` executes it before it asks this service for right `A`, and this service does not receive the preparer. The delegation of authority is not consulted either, because a D7.1 notice carries no amount limit; the holder check of a limit-based approval is another story's use of `delegation_limit`.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | role_code, role_name, role_class, default_scope | Read |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | role_code, conflicts_with, conflict_version | Read, only to report a conflicting pair to the session that asks for permissions |
| DF-PTY-016 | `contact_point` (owned by P1, read through the owner's contract of DP-05) | value_token, the addressee postal address over `v_ace_contact.contact_value` | Not read as a value: the answer names the field and the masked marker only |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` or `AC-DENY` entry: decision code, actor, object reference, area, right, versions, field markers, time | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (idempotency) | `idempotency_key` | the stored answer of an authorise call with its key | Write |

No `delegation_limit` row is read on this path: a D7.1 notice carries no amount limit and the route role, not a holder, is the check. The masked rendering of the postal address is Not specified in the source documents (GAP-0931; ASM-1657); this story names the field ID, the role and the mask version and leaves the format to the one masking library every screen uses. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. The decision is served through the operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1`, owner P4 `rwb-access`; this slice adds no path, no query parameter and no response field, and decides the following behind them:

| Method | Path | Purpose | Authorization | Errors |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The role, scope and right decision for one capability area and right, with the routed role where the action is an approval, and the field markers | The caller's own session; the answer is the decision | 401; 403 MSG-P4-002; 422; 503 MSG-P7-003 |
| GET | `/api/recovery/access/v1/me/permissions` | The caller's resolved roles, letters per capability area, scope, matrix version and masking version | None beyond the session | 401; 503 |
| GET | `/api/recovery/access/v1/masking-policies` | The masking answer for a field and a role, with the mask version | None beyond the session | 401; 503 |

Architecture v5 slide 14 names `POST /authorise`, `GET /me/permissions` and `/masking-policies`; TSD P4 v3 names `GET /me/session` (API-P4-012) for the same resolved view, so the resolved view is answered behind `GET /me/permissions` under R-PREC and the session read keeps its own story and its own shape. The request and response shape of `POST /authorise` is Not specified in the source documents (GAP-0932; ASM-1656).

#### 12.2 REST operations consumed

None. The notice, the approval and the case facts are sent in the authorise request by the composite route and by `rwb-decision`; this service calls no other service on this path, so the call stays one hop with the 2 s timeout of DP-11 and a circuit breaker.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | matrix or mask version | the policy kind, the old and new version, validFrom, the affected capability areas or fields, the load reference |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | the entry ID | the hash-chained `AC-READ` or `AC-DENY` entry of DP-03 |

CloudEvents 1.0 envelope; neither payload carries personal data. The `AccessPolicyChanged` event is written by the policy load path of this service (RWB-P4-AD002-APP, RWB-P4-AD004-APP) in the same transaction as the rows, and this story's part is the refresh it triggers; `DoaLimitChanged` belongs to the delegation path and is not published by this story.

#### 12.4 Events consumed

None from another service. The cache refresh reads this service's own `rwb.access.AccessPolicyChanged.v1` from `rwb.access.events.v1` through an internal listener, which is not a cross-service subscription; no `rwb.decision.*`, `rwb.case.*` or `rwb.comms.*` event is read. The refresh fails closed: a policy event that does not parse leaves the cache on the versions it already holds (X7).

#### 12.5 Workflows and activities

None. This story starts no workflow and registers no activity; the approval itself is `ApprovalWorkflow` in `rwb-decision`, and the case is `CaseWorkflow` in `rwb-case`.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) is a Temporal Schedule of this service and belongs to its own story; the authorise path has no clock.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The roles the caller holds and their class and default scope |
| `permission` | P4 (`rwb_access`) | The letters per capability area under the matrix version in force |
| `masking_rule` | P4 (`rwb_access`) | The unmasked flag per role and field under the mask version in force |
| `role_conflict` | P4 (`rwb_access`) | The conflicting pair reported to a session that asks for permissions |
| `delegation_limit` | P4 (`rwb_access`) | Not read here; a D7.1 notice carries no amount limit |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |

`contact_point`, `notice`, `approval`, `recovery_case` and `decision_log_entry` are other services' and are not read: the field is named, the value stays with `rwb-source-data`, and the ledger entry is written through the library (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision notice and approval WireMock | RWB-P7-E2014-CON | Notice `N-0201` for case `RW-2026-000123` with template `DEMAND-MTG` version 2 in `TH`, rule `R-LIT-03` version `LIT-2026.12` and preparer `U-9211`; approval `A-0201` `WAITING` for `RW-LITOFF`, and the escalated repeat for `RW-HEADLIT` with escalation level 1 |
| decision-record fake | RWB-PLT-E1027-CON | The entry write and the publish on `rwb.decision-record.v1`, including a forced failure for X5 |
| gateway-bff route fake | RWB-PLT-N001-CON | The composite route that carries the authorise, permission and masking calls, so the screen's own calls can be asserted |
| policy pack fixture | this story's own test data | The `PM-2026.12` permission rows, the `MASK-SIT-01` masking rows and a later masking version for AC6 |

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
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which patterns have an instance in this slice: DP-01 is the read of `permission` and `masking_rule` in `rwb_access`; DP-03 is the `AC-READ` and `AC-DENY` entry; DP-07 is the LOV-CAPABILITY area list; DP-09 is the outbox, the inbox and the idempotency key; DP-11 is the authorise contract with its mock and its 2 s timeout; DP-13 is the base path; DP-19 is the composite route. DP-05 has an instance only as an absence — this service reads no `v_ace_*` view and names the field, and the value stays with `rwb-source-data`. DP-06 and DP-10 have no instance here: no parameter row and no workflow or Schedule is this story's, and the policy rows with their versions are the data. This secondary slice adds no new build dependency of its own (metadata H = None): the platform contracts the table names are pulled by the service's baseline and by the policy pack load path (RWB-P4-AD002-APP, RWB-P4-AD004-APP), so the story is Day 1 and builds against the published contract RWB-P7-E2014-CON.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | REST controller | The three operations of 12.1, the problem responses with their message IDs, and the idempotency key |
| AuthoriseService | Service | Resolution of the caller's letters for one area and right, the routed-role check, the version pair in the answer |
| AuthoriseCache | Cache | The cached answer per user, area, right and object, with the matrix and mask versions; refresh on `AccessPolicyChanged`; fail closed on a mixed pair |
| MaskingPolicyService | Service | The `masking_rule` read per role and field, the masked default, and the mask version in the answer |
| PolicyVersionResolver | Service | The matrix version and the mask version in force, read once per refresh and held together |
| RouteRoleCheck | Service | The letter `A` plus the routed role or the holder the approval names; the preparer rule is not here |
| AccessLogWriter | Service | The `AC-READ` and `AC-DENY` entry of DP-03, with the masked field markers and no value, in the same transaction as the answer |
| PolicyChangeListener | Kafka consumer with the inbox | The service's own `AccessPolicyChanged`, deduplicated by event ID, refreshing the cache |

**Database and migrations**

- Reads `role`, `permission`, `masking_rule` and `role_conflict` in `rwb_access`; writes the decision-record entry through the library, and the inbox, outbox and idempotency rows.
- Index `ix_permission_role_area_version ON permission (role_id, capability_area, matrix_version)`, so the authorise read is one index scan in the cache-miss path.
- Index `ix_masking_field_version ON masking_rule (field_id, masking_version, role_code)`, so the mask answer for a field and a set of roles is one scan.
- No new table and no new column: the policy tables are the policy pack path's, and the access log is the decision-record entry (DP-03).
- Migration in the per-service Flyway sequence of DP-15: `V2014_1__access_authorise_indexes.sql`.

**Configuration and reference data**

- LOV-CAPABILITY, LOV-ROLE and LOV-SCOPE through the reference-data contract of DP-07 (RWB-P3-E1043-CON); the area `LITIGATION` is a value of that list, never a constant.
- The matrix version `PM-2026.12` and the masking version `MASK-SIT-01` in force are read from the rows, not configured; the SIT label is assumed (GAP-0933; ASM-1658).
- The access entry's decision codes `AC-READ` and `AC-DENY` follow the decision-code list of the ledger, and the field markers come from the request.
- No switch of this slice's own: a screen that cannot get an authorise answer must not open, so the authorise path has no off state. The legacy flag `rwb.decision.notice-approval` stays `rwb-decision`'s and is a legacy reference here.

**Build steps**

1. `AuthoriseController` and the problem responses, with the three operations and the idempotency key; tests for 401, 403 and 503 shapes.
2. `PolicyVersionResolver` and the two index reads; test that a new matrix version is served as data with no code change.
3. `AuthoriseService` for right `R` and right `A` on `LITIGATION`, with the routed-role check; tests for AC1, AC2, AC4 and AC7.
4. `MaskingPolicyService` with the masked default and the mask version in the answer; tests for AC1, AC4 and AC5.
5. `AccessLogWriter` in the same transaction as the answer, with the masked markers and the no-value assertion; tests for AC1, AC3, AC7 and AC8, and the forced failure for X5.
6. `AuthoriseCache` and `PolicyChangeListener` with the version pair and the mixed-pair refusal; test for AC6 with a fixed clock.
7. The contract-fake run against RWB-P7-E2014-CON and the gateway-bff route fake, so the story builds before `rwb-decision` and the screen exist in the environment.
8. The denial test for a role with no `LITIGATION` row through the composite route, and the audit read of the entries through `rwb-decision`.

**Done when.** The tests in section 16 pass; every open of a D7.1 notice for approval writes exactly one `AC-READ` entry naming the notice, the case, the actor and `DF-PTY-016` as masked, with no value of the address anywhere in the entry; every refusal writes one `AC-DENY` entry with its area and right; every answer names the matrix version and the masking version it was decided under; and a masking policy change is served by the cache after `AccessPolicyChanged` with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not carry the right in the area | You cannot {action} here. Your role does not include it. | This story, on the authorise path |
| MSG-P4-003 | The object is outside the caller's scope | This case is not in your scope. | This story, when the scope check fails |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the entry writer |
| MSG-GEN-004 | The cached policy was replaced while the call was in flight | Someone else changed this record. Reload it to see their change. | This story, on the version check |
| MSG-GEN-001 | A required field of the authorise request is missing | Enter {field}. | This story, on the request validation |
| MSG-P7-002 | A preparer tries to approve | You prepared this decision, so you cannot approve it. | `rwb-decision`, never this story |

The {action} value in MSG-P4-002 names the action and nothing else — for a D7.1 notice, "approve a D7.1 notice", "change a D7.1 notice", "refuse a D7.1 notice" or "open a D7.1 notice" — and the problem response carries the capability area in its `detail` beside the message ID, so a refusal is diagnosable without any notice content. Every error is an RFC 9457 problem response with `messageId` set and `instance` naming the request.

### 15. Screens and states

No screen is built here. The screens are `rwb-decision`'s and reach this service through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON):

| Screen | State | What this story supplies |
|---|---|---|
| SCR-10 Approval queue | List | The `LITIGATION` R answer per item, so the queue shows only items the caller may open, and one `AC-READ` entry per item opened |
| SCR-11 Decision screen | Ready | The `LITIGATION` A answer behind the approve, change and refuse buttons, and the field markers that keep `DF-PTY-016` masked |
| SCR-11 Decision screen | Decided | No answer of this story; the decided state is `rwb-decision`'s |
| SCR-18 Notice approval panel | Generated | The masked marker for the addressee postal address and the mask version the panel shows beside the field |
| SCR-11 Decision screen | Denied | The problem response of MSG-P4-002 with the action and the area, and the `AC-DENY` entry behind it |

The panel layout, the masked rendering and the composite route's field list are Not specified in the source documents (GAP-0931; ASM-1657); the screen stories are RWB-P7-E2014-APP and the notice API stories in `rwb-comms`, and this story changes no screen behaviour.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-014-01 | AC2, BR1, BR2 | Contract | Approver `U-9212` with `LITIGATION` `A` on approval `A-0201`; the authorise answer is the assertion, the approval is the contract fake |
| TC-E2-014-02 | AC2, BR1 | Contract | Approver `U-9212` with `A`; the variant change and its reason code stay `rwb-decision`'s |
| TC-E2-014-03 | AC2, BR2 | Contract | Approver `U-9212` with `A` on a refusal; the reason rule stays `rwb-decision`'s |
| TC-E2-014-04 | AC4, BR4 | Contract | Preparer `U-9211` holding `RW-LEGAL` with `A`; the 409 is `rwb-decision`'s and this story asserts the letter only |
| TC-E2-014-05 | AC1, BR6 | Component | Total balance from a load 3 days old; the access answer is unchanged and one `AC-READ` entry is written |
| TC-E2-014-06 | AC1, BR6 | Component | Template withdrawn after generation; the access answer is unchanged and the entry names no template |
| TC-E2-014-07 | AC2, BR2 | Contract | Refusal with an empty reason; the letter `A` is still the access assertion |
| TC-E2-014-08 | AC2, BR1 | Contract | Variant change with no reason code; the letter `A` is still the access assertion |
| TC-E2-014-09 | AC2, BR8 | Component | `U-9214` approves at 10:01 and `U-9212` at 10:02; the version pair in the answer is re-read and the 409 is `rwb-decision`'s |
| TC-E2-014-10 | AC1, AC5, BR5, BR7 | End to end | Screen open for `N-0201`; the panel shows `DF-PTY-016` masked, the entry marks it masked and no value is anywhere in the entry |
| TC-E2-014-11 | AC3, AC7, AC8, BR2, BR3 | Component | `U-9215` with `LITIGATION` `R` and `U-9217` with no `LITIGATION` row; 403 with MSG-P4-002 and one `AC-DENY` entry each |
| TC-E2-014-12 | AC1, AC6, BR7, BR9 | NFR | The decision-record write forced to fail: 503 MSG-P7-003, no answer and no data; in the same run a masking-version change published on AccessPolicyChanged reaches the next answer with no deployment |

The legacy level System maps to End to end, Access to Component and Resilience to NFR, and each case asserts only this slice's answer and entry. No case ID with the `-ITG` suffix is used here: the integration copy of the set is RWB-ITG-E2014-ITG, which proves the same facts across `rwb-access`, `rwb-decision`, `rwb-comms` and `rwb-case` with real services, and its `TC-E2-014-01-ITG` to `TC-E2-014-12-ITG` belong to that story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the letters C, R, U, D and A, the capability areas, the roles, the scopes, the masking rows and the matrix and mask versions are data rows; the Java code holds no letter, area, role or version literal (BR-P4-004, BR-P4-005).
- No personal data in logs, events, tests, workflow history or prompts: the access entry carries the actor reference, the notice and case references, the field ID and a masked marker. Workflow history is not used because this story starts no workflow.
- The addressee address never leaves the owning service: the value is read through `rwb-source-data`'s contract by whoever displays it, and this service answers the field ID and the masked flag only. A test scans the entry text for any part of the synthetic address.
- No read of another service's tables and no cross-schema read (DP-01): `notice`, `approval`, `recovery_case`, `contact_point` and `decision_log_entry` are never queried here.
- ACE data only through the owner's contract or a `v_ace_*` view of this service; this story reads no ACE view at all.
- An answer is never served without its entry, and the answer and the entry commit in one transaction (R-UNI-39).
- The cache fails closed: an unparseable or mixed policy event leaves the versions in force, and a missing policy row is a refusal, never a default allow.
- The authorise path has no off switch, because a screen that cannot be authorised must not open; the legacy approval flag stays `rwb-decision`'s.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-002 | Recommendation, reasons, inputs and limit on one screen | Epic 2, 3.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR2, BR5, BR6, BR9 | TC-E2-014-05, TC-E2-014-06, TC-E2-014-10 |
| REQ-APD-006 | Demand and recall notices approved through approval routing | Epic 2, 3.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR1, BR2, BR3, BR4, BR7, BR8 | TC-E2-014-01 to TC-E2-014-04, TC-E2-014-07 to TC-E2-014-09, TC-E2-014-11, TC-E2-014-12 |

| Legacy reference | Where it is kept |
|---|---|
| Roles RW-LITOFF, RW-LEGAL, RW-HEADLIT with Litigation A, and RW-CASEOWN with Litigation R | Metadata, sections 3, 7, 8, 10 |
| The preparer rule BR3 and CTL-05, and its execution in `rwb-decision` | Sections 1, 8, 10, 19 |
| Notice `N-0201`, case `RW-2026-000123`, approval `A-0201`, template `DEMAND-MTG` version 2, rule `R-LIT-03` version `LIT-2026.12`, preparer `U-9211` | Background, AC1 to AC4, AC8, sections 3, 12.8, 16 |
| MSG-P4-002, MSG-P4-003, MSG-P7-002, MSG-P7-003, MSG-GEN-001, MSG-GEN-004 | Section 14, exception paths |
| Masked address on the screen, and no value in the log | Sections 4, 7, 11, 17 |
| Legacy test set TC-E2-014-01 to TC-E2-014-12, and its integration copy RWB-ITG-E2014-ITG | Section 16 |
| Legacy key RWB-E2-014, story RWB-P4-E2014-APP, contract RWB-P7-E2014-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The `rwb-decision` slice of this legacy key, RWB-P7-E2014-APP with RWB-P7-E2014-CON: the approval queue SCR-10, the decision screen SCR-11, the notice approval panel SCR-18, the approve, change, refuse and return endpoints, the decision entry, and the preparer check that refuses a preparer with 409 and MSG-P7-002.
- The `rwb-comms` notice APIs: `GET /notices/{noticeId}`, the notice approve, the regenerate from another Approved variant and the hold with reason `REFUSED_BY_APPROVER`.
- The integration harness RWB-ITG-E2014-ITG and its `-ITG` copies of the test cases.
- Template authoring and the Legal approval of templates, the template status check and its withdrawn-template hold (RWB-E1-046, RWB-E1-034).
- Dispatch to WIN, proof of delivery and the notice period (RWB-E2-021).
- The policy pack load path of this service — the reference loads, their approval, verification and rollback, and the rows of `PM-2026.12` and `MASK-SIT-01` themselves (RWB-P4-AD002-APP, RWB-P4-AD004-APP).
- The delegation of authority table and its lookup for limit-based approvals (RWB-P4-E2013-APP and the `rwb-decision` slices), role, scope and sign-in administration, break-glass, and the six-monthly access review list (JOB-18).
- The case facts, the case state and the case-owner task on a rejected notice (`rwb-case`, RWB-P3-E2014-APP), and the full case record view (RWB-P3-E1023-APP).
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of the authorise path (an OPS story of this legacy key).
