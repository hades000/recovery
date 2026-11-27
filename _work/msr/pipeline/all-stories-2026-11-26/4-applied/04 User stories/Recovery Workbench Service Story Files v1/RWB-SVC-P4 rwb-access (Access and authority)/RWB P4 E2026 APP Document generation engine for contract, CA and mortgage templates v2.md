# RWB-P4-E2026-APP Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2026-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-P4-AQ |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2026-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DCM-012, REQ-OCC-002) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-026 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E2026-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer, a case owner and the case workflow identity that asks for a contract, credit approval or mortgage document**, I want **an access answer that says whether my role carries the Documents right C on that case and that treatment, which version of the permission matrix and of the masking policy the answer was taken from, and one access-log entry per generation request that names the case, the treatment and the template codes but never a single merge value**, so that **a document set is generated only for a caller and on a case that may generate it, and no borrower name, national ID number, transfer price or title deed number reaches a log, an event or an access entry**.

Inside `rwb-access` this is the access slice of the generation engine of legacy RWB-E2-026:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The slice delivers two answers and one record for one generation request: the authorise decision for capability area `DOCUMENTS` with right `C` on the case and the treatment, including the scope decision and the service-identity decision; the masking answer for the national ID field `DF-PTY-007` under the masking version in force; and the access-log entry written as a decision-record entry of DP-03 on every allowed request (`AC-READ`) and every refusal (`AC-DENY`).
- The generation itself is not here. The template selection, the merge field resolution, the value formatting, the render to PDF/A-2b, the draft store, the document rows, the `DocumentStored` event and the decision-log entry of decision code `D6.4` are `rwb-document`'s (RWB-P5-E2026-APP), reached through the published contract RWB-P5-E2026-CON and its fake, in one hop with the 2 s timeout of DP-11.
- The slice builds no screen. The screens that show the generated documents are SCR-30 Case documents and the screens of RWB-E2-017, both `rwb-document`'s; this service answers the access question behind them.
- The treatment, the case facts, the parties and the collateral are other services' and are never read here: the request carries the case reference, the treatment reference and the template codes, and it carries no merge value at all, so a value cannot leak through this service because it never receives one.
- The policy pack is data: permission rows under matrix version `PM-2026.12`, masking rows under masking version `MASK-SIT-01`. The load path that writes those rows is `rwb-access`'s own and is out of this story (RWB-P4-AD002-APP, RWB-P4-AD004-APP).

The rights carried from the legacy story are unchanged: `RW-RESTRUCT` and `RW-CASEOWN` hold Documents `C` and may request generation for a treatment in scope; `RW-TEAMMGR` holds Documents `R` and reads the generated documents but is refused generation; the service identity `SY-CASEWF` holds Documents `C` with scope `ALL` for rule-driven generation from Epic 3, under the same checks as a person (NFR-051).

### 2. Business rationale

A deed in lieu set produced for an officer who may not produce it, or on a case in another team, is an authorisation finding on top of the document finding the legacy story already closes. The legacy story proved the engine; this slice proves the authorisation and the record in front of it. Today the Documents right and the case scope are checked inside the monolith by `RecoveryAccessGuard`, and the generation engine writes its own decision entry with the merge snapshot beside it, so the question "who was allowed to generate this, under which policy version" is answered by reading application code, and the value of a field can travel with the record that describes the read.

Under Architecture v5 the authorise answer and the masking answer come from `rwb-access` as data, with the matrix version and the mask version naming the policy the answer was taken from, and every request and every refusal is an append-only entry in the same ledger as the decisions. The generation service asks this question in one hop and holds the answer for the life of its cache entry, and the entry it produces carries identifiers only.

This story carries controls CTL-11 (a national ID number is filled from the token service at render time and the clear value exists only inside the stored PDF), CTL-14 (only an approved template version leaves) on the access side, and the audit expectation behind NFR-042 (every read of the case store and the document store is logged). It meets REQ-DCM-012 and REQ-OCC-002 on the access side and supports the measure rule and limit changes made without a code release (target 100 percent) and the target of 1,000 deed in lieu cases a month in 2027 (NFR-006).

The realignment changes the mechanism, not the business rule:

1. The permission, masking and role rows of the monolith's recovery schema become `rwb-access`'s own tables in `rwb_access` (DP-01), versioned by matrix version and mask version, so a change of rights or of masking needs an approved load and no release.
2. The synchronous `RecoveryAccessGuard` call inside the monolith becomes the published authorise contract, cached, with one hop and a 2 s timeout (DP-11); `rwb-document` asks and holds the answer, and this story answers and records.
3. The decision-log writer inside the monolith becomes the local decision-record library of DP-03, so an `AC-READ` or `AC-DENY` entry is hash-chained and published on `rwb.decision-record.v1` where `rwb-decision`'s ledger and the audit query already read.
4. The access event that the monolith never sent becomes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, and every holder of a cached answer refreshes on it, so a new masking version is in force at the next call with no deployment.
5. The case facts, the party rows and the collateral rows behind the merge fields stay with their owners — `rwb-case`, `rwb-source-data` and `rwb-treatment` — and this service reads none of them; it answers which right the caller holds on the case reference it was given (DP-05).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2026-CON | The published generation contract this slice is tested against: the generation request for case `RW-2026-000301`, treatment `TRT-0301` of type `DEED_IN_LIEU` with `decision_log_id` set and no outcome, template `DIL-CONTRACT` version 2 in Thai for `MORTGAGE`, the three-template set `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1, and the request key of each call, with its contract fakes. The request and response shape of the authorise call itself is Not specified in the source documents (GAP-0938; ASM-1666) |
| Permission matrix `PM-2026.12` `IN_FORCE` | The rows this slice answers from, loaded by the policy pack path (RWB-P4-AD002-APP, RWB-P4-AD004-APP): `DOCUMENTS` `C` for `RW-RESTRUCT`, `RW-CASEOWN` and `SY-CASEWF`, `DOCUMENTS` `R` for `RW-TEAMMGR`, and no `DOCUMENTS` row for `RW-PHONECOL`. The matrix in force is the version of the load; the Documents letters per role are Not specified in the source documents (GAP-0937; ASM-1665) |
| Masking version `MASK-SIT-01` in force | The rows for `DF-PTY-007` covering `RW-RESTRUCT`, `RW-CASEOWN`, `RW-TEAMMGR` and `SY-CASEWF` with `unmasked` false, so the national ID number is masked for every role on this path, and no row at all for a field outside the pack, which stays masked by default. The version label is assumed for SIT (GAP-0940; ASM-1668) |
| Test users in SIT | `U-4101` holds `RW-CASEOWN` on case `RW-2026-000301`; `U-4103` holds `RW-TEAMMGR`; `U-4106` holds `RW-PHONECOL`; the restructuring officer of the case holds `RW-RESTRUCT`; the service identity `SY-CASEWF` holds its own role row. `U-4102` and `U-4104` hold `RW-PLATADM` and belong to the break-glass path, not to this one |
| The service identity `SY-CASEWF` | A `role` row of class `NON_HUMAN_ACTOR` with Documents `C` and default scope `ALL`, so rule-driven generation from Epic 3 passes the same check as a person (NFR-051, LOV-ROLE-CLASS). The row itself and its scope are Not specified in the source documents (GAP-0939; ASM-1667) |
| The decision-record library and its topic | `rwb.decision-record.v1` and the local library of DP-03, so an access entry is written, chained and published in one transaction with the answer |
| gateway-bff composite route | The route of DP-19 that carries the mask answer of the document screen to this base path, with the 2 s timeout of DP-11 |

Business preconditions carried from RWB-E2-026:

- The caller holds Documents `C` on the case (`RW-RESTRUCT` or `RW-CASEOWN`), or is the service identity `SY-CASEWF` (legacy section 3 and section 10).
- The treatment is of type `DEED_IN_LIEU` or `RESTRUCTURE`, approved at `D6.4` and still open; that check is `rwb-document`'s and never changes the access answer.
- Templates `DIL-CONTRACT`, `DIL-CA` and `DIL-MORTGAGE` are loaded in Thai with `approved_by_legal = true`; template status is `rwb-comms`'s and does not change the access answer (the template catalog owner is P6 under the Ownership Map).
- Every refusal is answered with MSG-P4-002 or MSG-P4-003 naming the action and, for a right, the capability area, and no case content (FSD P4 v3 A2.4 VR-P4-004-1).

### 4. Flow

1. Restructuring officer or the case workflow identity: asks `rwb-document` for generation on case `RW-2026-000301` for treatment `TRT-0301` with template codes `DIL-CONTRACT`, `DIL-CA` and `DIL-MORTGAGE`, in language `TH`, with a request key.
2. `rwb-document`: on that request, calls `POST /api/recovery/access/v1/authorise` on this service with the caller's user reference or service-identity reference, the roles the session resolved, capability area `DOCUMENTS`, right `C`, the case and treatment as the object reference, the template code list, the request key, and the field list the screen will render, `DF-PTY-007`.
3. `AuthoriseService`: reads the caller's permission rows for `DOCUMENTS` from `permission` in `rwb_access` under the matrix version in force, unions the letters of every role the caller holds, and answers `allowed` with right `C`, the roles that carry it, the scope that was applied, `matrixVersion` `PM-2026.12` and `maskingVersion` `MASK-SIT-01`.
4. `ScopeCheck`: compares the scope of the caller's roles with the team of the case reference it was given — `OWN`, `TEAM`, `REGION` or `ALL` from LOV-SCOPE, and `ALL` for `SY-CASEWF` — and refuses a case outside it. The team of the case is not read from anywhere: it arrives in the request with the object reference, because `recovery_case` is `rwb-case`'s.
5. `MaskingPolicyService`: reads the `masking_rule` rows for `DF-PTY-007` and the caller's roles under the mask version in force and answers masked. Where no row covers the field for any of the caller's roles the answer is masked as well, so the default is refuse rather than show (FSD P4 v3 A2.5, AC-EXC-P4-004-05). No value of the field is read, echoed or cached by this service.
6. `AccessLogWriter`, in the same transaction as the answer: writes the decision-record entry of DP-03 with decision code `AC-READ`, the actor, the case reference, the treatment reference, the capability area, the right, the template code list, the matrix version, the mask version and the field markers, with `DF-PTY-007` marked masked and no value; publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` through the outbox.
7. `rwb-document`: generates the set, stores the drafts, writes its own document rows, its `DocumentStored` events and its decision-log entry of decision code `D6.4` with the merge snapshot; none of that is this story's and none of it comes back here.
8. The screens of RWB-E2-017 and SCR-30 Case documents: show the generated documents, with `DF-PTY-007` rendered masked from the mask answer here; the rendering itself is the one masking library every screen uses.
9. Refusal, right: `AuthoriseService` answers 403 with MSG-P4-002 when no permission row of the caller's roles holds the letter `C` for `DOCUMENTS` under the matrix version in force — `RW-TEAMMGR` holds `R` and is refused (legacy TC-E2-026-15), and a role with no `DOCUMENTS` row is refused by default.
10. Refusal, scope: `ScopeCheck` answers 404 with MSG-P4-003 when the case is outside the caller's scope — case `RW-2026-000306` in team `HP-NE` against an officer of team `FCR-BKK` (legacy AC12) — and the case number is not echoed in the problem response.
11. `AccessLogWriter`, on either refusal: writes `AC-DENY` with the actor, the capability area, the right, the case reference, the matrix version and the reason code (`NO_RIGHT` or `OUT_OF_SCOPE`), and with no treatment detail, no template code, no merge value and no case content on the scope path.
12. A policy pack load by the service's own administration path commits new `permission` or `masking_rule` rows and writes the outbox row for `rwb.access.AccessPolicyChanged.v1` with the new matrix or masking version; the load itself is RWB-P4-AD002-APP and RWB-P4-AD004-APP, and the next authorise call answers with the new version and no deployment.

Every answer and its access entry commit in one transaction (DP-03, R-UNI-39), so a call that cannot be logged is refused rather than answered (FSD P4 v3 AC-EXC-P4-007-03), and a repeated call with the same request key returns the first answer without a second entry.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds no `DOCUMENTS` row at all | Refused with 403; one `AC-DENY` entry with area `DOCUMENTS`, right `C` and reason `NO_RIGHT`; no document is generated | MSG-P4-002 | AC2 |
| X2 | The caller holds `DOCUMENTS` `R` and asks for right `C` | Refused with 403 for the named action; one `AC-DENY` entry with right `C`; nothing is generated | MSG-P4-002 | AC2 |
| X3 | The case is outside the caller's scope | Refused with 404; one `AC-DENY` entry with reason `OUT_OF_SCOPE`; the case number is not echoed | MSG-P4-003 | AC3 |
| X4 | No masking row covers `DF-PTY-007` for any of the caller's roles | The field is answered masked under the mask version in force; the entry marks it masked; no value is read | None | AC5 |
| X5 | The service identity `SY-CASEWF` asks with no `role` row or no `DOCUMENTS` row | Refused exactly as a person would be, with 403 and one `AC-DENY` entry naming the identity | MSG-P4-002 | AC4 |
| X6 | The access entry cannot be written | The call returns 503, no answer and no data; the reason is logged; the cache is unchanged | MSG-P7-003 | AC7 |
| X7 | A second call arrives with the same request key | The first answer and its entry are returned; no second entry is written | None | AC8 |
| X8 | The matrix version and the mask version arrive from two different policy loads | The cache refuses the mixed pair, keeps the versions it already holds and raises the mismatch; the caller gets the older consistent pair | None | AC9 |
| X9 | The template set fails a check in `rwb-document` (missing merge value, unapproved or withdrawn version, treatment not approved) | Nothing happens here: the access answer stands, and the refusal is `rwb-document`'s with its own message | MSG-P5-009, MSG-P5-010, MSG-P5-011, MSG-P6-003 (all produced by `rwb-document`) | AC9 |

An answer is never served without its entry and never without naming both policy versions; a call whose entry fails is an error, not a silent success. No exception path of this story changes a document, a treatment or a case: this service answers and records.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published generation contract RWB-P5-E2026-CON and its fake; the case, the treatment, the templates and the merge values never arrive as a table read, and the merge values never arrive at all |
| Negotiable | Letters, roles, areas, scopes, masking rows, mask formats and versions are data; the story fixes the answer shape and the entry only |
| Valuable | A document set cannot be generated without a current authorise answer on the case and the treatment, and no merge value can enter a log because none enters this service |
| Estimable | Three existing endpoints, one cache, one masking answer, one scope check, one entry writer |
| Small | Fits one week with its tests, because the engine, the templates, the render and the screens are other stories' |
| Testable | Every criterion below is one test case in section 16, run against the P5 contract fake and the policy pack fixture |

### 7. Acceptance criteria

```gherkin
Feature: Access decisions and access-log entries for document generation

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.12" is in force and masking version "MASK-SIT-01" is in force
    Given test user "U-4101" holds RW-CASEOWN, test user "U-4103" holds RW-TEAMMGR and test user "U-4106" holds RW-PHONECOL
    Given the rwb-document contract mock returns a generation request for case "RW-2026-000301" and treatment "TRT-0301" of type "DEED_IN_LIEU" with decision_log_id set and no outcome
    Given the rwb-document contract mock returns template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true, and the three-template set "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE"

  Scenario: AC1 A case owner with Documents C is allowed to generate (new, D-RCV-60)
    Given test user "U-4101" holds RW-CASEOWN and its permission row in "PM-2026.12" holds the letter "C" for area "DOCUMENTS"
    When "U-4101" requests generation through the rwb-document contract for case "RW-2026-000301", treatment "TRT-0301" and template "DIL-CONTRACT", and the rwb-document call asks POST /api/recovery/access/v1/authorise with area "DOCUMENTS", right "C", the case, the treatment and the field list "DF-PTY-007"
    Then the answer is allowed with area "DOCUMENTS", right "C", the role "RW-CASEOWN", matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the answer marks "DF-PTY-007" masked and carries no value of the national ID number
    Then one access-log entry exists with decision code "AC-READ", actor "U-4101", case "RW-2026-000301", treatment "TRT-0301", template "DIL-CONTRACT" version 2, area "DOCUMENTS", matrix version "PM-2026.12" and the field marker "DF-PTY-007" as masked

  Scenario: AC2 A team manager with Documents R is refused generation (new, D-RCV-60)
    Given test user "U-4103" holds RW-TEAMMGR and its permission row in "PM-2026.12" holds the letter "R" for area "DOCUMENTS" and no letter "C"
    When "U-4103" requests generation for case "RW-2026-000301", treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the call is refused with status 403 and message MSG-P4-002 for the action "generate documents" and the area "DOCUMENTS"
    Then one access-log entry exists with decision code "AC-DENY", actor "U-4103", case "RW-2026-000301", area "DOCUMENTS", right "C" and reason "NO_RIGHT"
    Then the entry holds no treatment detail, no template code and no merge value

  Scenario: AC3 A case outside the caller's scope is refused and names no case number (new, D-RCV-60)
    Given case "RW-2026-000306" is in team "HP-NE" and the officer's scope is team "FCR-BKK"
    When the officer asks the authorise path for area "DOCUMENTS", right "C" on case "RW-2026-000306" and treatment "TRT-0301"
    Then the call is refused with status 404 and message MSG-P4-003
    Then one access-log entry exists with decision code "AC-DENY", the case reference, area "DOCUMENTS", right "C" and reason "OUT_OF_SCOPE"
    Then the problem response holds no case number, no product, no borrower name and no merge value

  Scenario: AC4 The case workflow identity passes the same checks as a person (new, D-RCV-60)
    Given the role row of "SY-CASEWF" is of class "NON_HUMAN_ACTOR" with scope "ALL", and its permission row in "PM-2026.12" holds the letter "C" for area "DOCUMENTS"
    When "SY-CASEWF" asks the authorise path for area "DOCUMENTS", right "C" on case "RW-2026-000301" and treatment "TRT-0301"
    Then the answer is allowed with right "C", role "SY-CASEWF", matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the access-log entry names "SY-CASEWF" as the actor and marks "DF-PTY-007" masked, and it holds no person reference
    When the role row of "SY-CASEWF" is removed from the pack and the same call is made
    Then the call is refused with status 403 and message MSG-P4-002, and one "AC-DENY" entry names "SY-CASEWF"

  Scenario: AC5 The national ID number is masked in every answer and in every entry (new, D-RCV-60)
    Given the case facts give transfer_price 1250000.00, title_doc_no "12345" and contract_date 2026-12-10
    Given the national ID field "DF-PTY-007" has an unmasked false row in "MASK-SIT-01" for every role on this path
    When "U-4101" is allowed for area "DOCUMENTS", right "C" with the field list "DF-PTY-007"
    Then the answer marks "DF-PTY-007" masked under masking version "MASK-SIT-01"
    Then neither the answer, nor the "AC-READ" entry, nor any event of this story holds "1250000.00", "12345", "2026-12-10" or any digit of the national ID number

  Scenario: AC6 One entry per request carries the template codes and versions and no merge value (new, D-RCV-60)
    Given the three-template set "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1 is current and approved
    When "U-4101" requests generation for treatment "TRT-0301" with the three template codes under request key "K-0301"
    Then exactly one access-log entry exists for request key "K-0301", not three
    Then the entry names the case "RW-2026-000301", the treatment "TRT-0301", the three template codes with their versions, the matrix version and the mask version
    Then the entry holds no merge value, no borrower name, no national ID number and no document ID

  Scenario: AC7 An answer that cannot be logged is refused (new, D-RCV-60)
    Given the decision-record store does not accept writes
    When "U-4101" asks the authorise path for area "DOCUMENTS", right "C" on case "RW-2026-000301" and treatment "TRT-0301"
    Then the call returns status 503 with message MSG-P7-003
    Then no allowed answer is returned and no data of the case is sent
    Then the cache of this service holds no new answer

  Scenario: AC8 A repeated request returns the first answer and writes no second entry (new, D-RCV-60)
    Given a request with request key "K-0301" was answered allowed and wrote one "AC-READ" entry
    When the same request with request key "K-0301" arrives again
    Then the first answer is returned with the same matrix version and mask version
    Then no second "AC-READ" entry is written and no new document is requested

  Scenario: AC9 A template check that fails in rwb-document does not change the access answer (new, D-RCV-60)
    Given template "DIL-CA" has only version 1 with approved_by_legal false
    Given test user "U-4101" holds Documents "C" on case "RW-2026-000301" and is in scope
    When "U-4101" requests the three-template set and the rwb-document contract mock refuses it with MSG-P5-010 naming "DIL-CA" version 1
    Then this service's answer for area "DOCUMENTS", right "C" is still allowed with matrix version "PM-2026.12"
    Then the refusal of MSG-P5-010 is not produced, reworded or repeated by this service
    Then the "AC-READ" entry names the three template codes and holds no template status and no merge value
```

The nine criteria above are the ones this story owns; the legacy AC1 to AC14 and the legacy test cases are carried by `rwb-document` (RWB-P5-E2026-APP) against the same contract, and the legacy test set is kept here in section 16 against this slice's assertions. Where a legacy criterion is served by this slice it is named in prose: the scope refusal of legacy RWB-E2-026 AC12 by AC3, the missing Documents right of legacy RWB-E2-026 X12 and TC-E2-026-15 by AC2, the national ID rule of legacy RWB-E2-026 BR11 by AC5, and the repeat with the same key of legacy RWB-E2-026 AC8 by AC8.

The authorise request and response shape used above — actor or service identity, roles, area, right, case and treatment object reference, template code list, request key and field list in, and allowed, roles, area, right, scope applied, matrix version, masking version, field markers and messageId out — is Not specified in the source documents (GAP-0938; ASM-1666); no field of it is a business value and it is renamed at the contract review if the published contract differs.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A right is taken from the permission rows of the matrix version in force, per role and capability area, with letters C, R, U, D and A; no letter, role or area is written in code | FSD P4 v3 A2.4; BR-P4-004; TSD P4 v3 T6.1 |
| BR2 | Generating a contract, credit approval or mortgage document needs Documents `C`; reading the generated documents needs Documents `R` and is not a generation right | Legacy RWB-E2-026 sections 3, 10 and 16; FSD P4 v3 A2.4; TSD P4 v3 T3.2 LOV-CAPABILITY |
| BR3 | A role with no `DOCUMENTS` row is denied; the authorise path refuses by default and never falls back to a broader role or to a default letter | FSD P4 v3 A2.4 AC-EXC-P4-004-06; Architecture v5 zero trust, deny by default |
| BR4 | A case outside the caller's scope is answered 404 with MSG-P4-003 and never 403, so a scope refusal does not confirm that the case exists | Legacy RWB-E2-026 AC12; FSD P4 v3 A2.14; TSD P4 v3 T6.2 |
| BR5 | A service identity is subject to the same role, right and scope checks as a person, and its `role_class` is `NON_HUMAN_ACTOR` | FSD P4 v3 A2.30 and REQ-ACA-010; TSD P4 v3 T7 NFR-051; legacy RWB-E2-026 section 10 |
| BR6 | A personal field is shown masked unless a masking row for the role and the field says unmasked, and a field with no covering row stays masked | FSD P4 v3 A2.5 AC-EXC-P4-004-05; BR-P4-005 |
| BR7 | The national ID number is filled at render time and exists only inside the stored PDF; the mask answer of this service names the field and the version and never a value | Legacy RWB-E2-026 BR11; DF-PTY-007; CTL-11; DL26 |
| BR8 | Every allowed generation request writes one `AC-READ` entry and every refusal one `AC-DENY` entry, in one transaction with the answer; a call that cannot be logged is refused | FSD P4 v3 A2.7 AC-P4-007-01, AC-EXC-P4-007-03 and AC-EXC-P4-007-04; DP-03; R-UNI-39 |
| BR9 | The access answer depends on the rights, the scope and the policy versions only: the template status, the treatment state, the merge values and the render are `rwb-document`'s checks and never change the access answer | Legacy RWB-E2-026 BR1, BR3, BR5; FSD P4 v3 A2.4 VR-P4-004-1 |
| BR10 | A repeat with the same request key returns the first answer and writes no second entry | Legacy RWB-E2-026 BR9; R-UNI-40 |
| BR11 | An answer names the matrix version and the masking version it was decided under, and a policy change reaches the cached answer through `rwb.access.AccessPolicyChanged.v1` with no deployment | FSD P4 v3 A2.4 AC-P4-004-01; Architecture v5 slide 42 cache refresh |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` in `rwb_access` under the matrix version in force; the capability areas are the LOV-CAPABILITY values read through the reference-data contract of DP-07 (RWB-P3-E1043-CON), and the Java code holds no enum of areas, roles or letters.
- BR2 and BR3 are one check on the letter `C` in the area `DOCUMENTS`; a missing row is a refusal, never a default.
- BR4 is the scope comparison of the case reference in the request against the scope of the caller's roles; no case row is read, so the rule cannot disagree with `rwb-case` about which team the case is in.
- BR5 is the `role_class` read of the same `role` table: the check is identical for every class, and the scope `ALL` of `SY-CASEWF` is a row of `role.default_scope`, not a branch in code.
- BR6 and BR7 are the `masking_rule` read plus the default, with the mask format left to the library, because no source fixes a rendering for a national ID number (GAP-0940; ASM-1668).
- BR8 is one `RecordAndApply` transaction on the answer and the entry, with the idempotency key of DP-09.
- BR9 is the absence of every generation input from the authorise request: no template status, no treatment state, no merge value and no override list is sent, so no check here can disagree with `rwb-document`.
- BR10 and BR11 are the stored answer and its key, and the version pair with the cache refresh on the service's own `AccessPolicyChanged`.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No cached answer | Authorise call for area `DOCUMENTS` | The policy rows are in force | Allowed or denied, with the matrix and masking versions |
| Allowed | The answer is served | The `AC-READ` entry commits | Served, with the field markers and the template code list |
| Denied | The refusal is served | The `AC-DENY` entry commits | Refused with 403 and MSG-P4-002, or 404 and MSG-P4-003 |
| Cached under version `PM-2026.12` / `MASK-SIT-01` | `rwb.access.AccessPolicyChanged.v1` | A later policy load is in force | Cached under the new versions, served from the next call |
| Cached, mixed versions | Refresh | The event names a matrix version and a masking version from different loads | Unchanged, with the mismatch raised |

| From | Event | Condition | To |
|---|---|---|---|
| `LOADED` | The policy pack load is approved | The approver is not the loader | `APPROVED` |
| `APPROVED` | The valid-from date is reached | None | `IN_FORCE`, and `AccessPolicyChanged` is published |
| `IN_FORCE` | The next version is approved | None | `SUPERSEDED` |

The second table is the lifecycle of the rows this story reads, owned by RWB-P4-AD002-APP and RWB-P4-AD004-APP; this story reads the version in force and publishes nothing on that path itself. A generated document's own state `DRAFT` is `rwb-document`'s and is not a state of this service. Access-log entries have no lifecycle of their own: they are append-only and are read by `rwb-decision`'s decision-log query.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT Restructuring officer (FCR) | Requests generation for a treatment in scope (Documents `C`) |
| RW-CASEOWN Case owner | Requests generation for a treatment in scope (Documents `C`) |
| SY-CASEWF Case workflow module | Calls for rule-driven generation from Epic 3, under its own role row of class `NON_HUMAN_ACTOR` with Documents `C` and scope `ALL`, and under the same checks as a person (R-DIL-14, R-DIL-16; NFR-051) |
| RW-TEAMMGR Team manager | Reads the generated documents (Documents `R`); generation is refused with MSG-P4-002 |
| RW-PHONECOL and every role with no `DOCUMENTS` row | Refused by default, with an `AC-DENY` entry |
| RW-AUDIT Internal audit | Reads the access and decision entries with scope `ALL` through `rwb-decision`'s decision-log query, and calls no operation of this story |
| RW-LEGAL Legal counsel | Approves template versions (Documents `CRUA`; RWB-E1-034); the approval is a precondition of `rwb-document`'s path and is not part of this story |
| SY-DECLOG Decision log writer | Writes the decision entry of the generation, which is `rwb-document`'s; this service writes the access entry only |

No approval level from the delegation of authority applies in this story, and no `delegation_limit` row is read: the treatment itself was approved at `D6.4` before generation, and the Documents right is not a limit-based approval. The refusal shape is 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002 for an absent right, and 404 with MSG-P4-003 for a case outside the scope. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | role_code, role_name, role_class, default_scope | Read |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-PTY-007 | none: the field is named, not read | the national ID number, over the party data of `rwb-source-data` | Not read as a value: the answer names the field and the masked marker only |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` or `AC-DENY` entry: decision code, actor, case and treatment reference, area, right, template codes and versions, matrix version, mask version, field markers, request key, time | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (idempotency) | `idempotency_key` | the stored answer of an authorise call with its request key | Write |

`recovery_case`, `treatment`, `party_ext`, `contact_point`, `account_ext`, `valuation_ext`, `template`, `merge_field`, `document` and `decision_log_entry` are other services' and are not read: the case and the treatment arrive as an object reference in the request, the template codes and versions arrive in the request and in the contract fake, and the ledger entry of the generation is written by `rwb-document` through its own library (DP-01). The legacy field rows DF-CAS-001 to DF-CAS-004, DF-TRT-001 to DF-TRT-013, DF-ACE-057, DF-ACE-058, DF-ACE-197, DF-REF-045 to DF-REF-051, DF-DOC-001 to DF-DOC-011, DF-DOC-032, DF-DOC-033 and DF-DEC-001 to DF-DEC-018 of legacy RWB-E2-026 section 11 belong to the P5 slice, P1's source data and P3's case, and none of them is read here. The masked rendering of the national ID number is Not specified in the source documents (GAP-0940; ASM-1668); this story names the field ID, the roles and the mask version and leaves the format to the one masking library every screen uses. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. The decision is served through the operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1`, owner P4 `rwb-access`; this slice adds no path, no query parameter and no response field, and decides the following behind them:

| Method | Path | Purpose | Authorization | Errors |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The role, scope and right decision for area `DOCUMENTS` and right `C` on a case and a treatment, with the template code list and the field markers | The caller's own session; the answer is the decision | 401; 403 MSG-P4-002; 404 MSG-P4-003; 422; 503 MSG-P7-003 |
| GET | `/api/recovery/access/v1/me/permissions` | The caller's resolved roles, letters per capability area, scope, matrix version and masking version | None beyond the session | 401; 503 |
| GET | `/api/recovery/access/v1/masking-policies` | The masking answer for `DF-PTY-007` and a role, with the mask version | None beyond the session | 401; 503 |

Architecture v5 slide 14 names `POST /authorise`, `GET /me/permissions` and `/masking-policies` for `rwb-access`; TSD P4 v3 names `GET /me/session` (API-P4-012) for the same resolved view, so the resolved view is answered behind `GET /me/permissions` under R-PREC and the session read keeps its own story and its own shape. The legacy operation of the key, `POST /cases/{caseId}/generated-documents`, is `rwb-document`'s and is not served here; Architecture v5 slide 16 names P5's own `POST /documents/generate` for the same engine. The request and response shape of `POST /authorise` is Not specified in the source documents (GAP-0938; ASM-1666).

#### 12.2 REST operations consumed

None. The case, the treatment, the template codes, the request key and the field list are sent in the authorise request by `rwb-document`; this service calls no other service on this path, so the call stays one hop with the 2 s timeout of DP-11 and a circuit breaker of the caller. The P5 contract is consumed only in this story's tests, as the fake that poses the generation request.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | matrix or mask version | the policy kind, the old and new version, validFrom, the affected capability areas or fields, the load reference |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | the entry ID | the hash-chained `AC-READ` or `AC-DENY` entry of DP-03 |

CloudEvents 1.0 envelope; neither payload carries personal data, and neither carries a merge value, a template body or a document. The `AccessPolicyChanged` event is written by the policy load path of this service (RWB-P4-AD002-APP, RWB-P4-AD004-APP) in the same transaction as the rows, and this story's part is the refresh it triggers; `DoaLimitChanged` belongs to the delegation path and is not published by this story.

#### 12.4 Events consumed

None from another service. The cache refresh reads this service's own `rwb.access.AccessPolicyChanged.v1` from `rwb.access.events.v1` through an internal listener, which is not a cross-service subscription; no `rwb.document.*`, `rwb.case.*`, `rwb.treatment.*` or `rwb.decision.*` event is read, and `DocumentStored` (EV-16) is `rwb-document`'s. The refresh fails closed: a policy event that does not parse leaves the cache on the versions it already holds (X8).

#### 12.5 Workflows and activities

None. This story starts no workflow and registers no activity; the generation is `rwb-document`'s `DocumentIntakeWorkflow` and its `generate` activity (Architecture v5 slide 16), and the case is `CaseWorkflow` in `rwb-case`. The task queue `rwb-access` exists for the service's Schedule work and is not used by this path.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) is a Temporal Schedule of this service and belongs to its own story; the authorise path has no clock.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The roles the caller holds, their class and their default scope |
| `permission` | P4 (`rwb_access`) | The letters per capability area under the matrix version in force |
| `masking_rule` | P4 (`rwb_access`) | The unmasked flag per role and field under the mask version in force |
| `delegation_limit` | P4 (`rwb_access`) | Not read here; the Documents right is not a limit-based approval |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |

`recovery_case`, `treatment`, `template`, `merge_field`, `document` and `decision_log_entry` are other services' and are not read (DP-01). This story creates no table and adds no migration of its own: `role`, `permission` and `masking_rule` and their rows are the P4 access baseline's, created in the per-service Flyway sequence of DP-15 by the service's own contract and DB stories (RWB-P4-E1037-CON, RWB-P4-AD002-APP, RWB-P4-AD004-APP), and `masking_rule` carries the `MASK-SIT-01` rows this story reads.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document generation WireMock | RWB-P5-E2026-CON | Case `RW-2026-000301` with product group `MORTGAGE`, treatment `TRT-0301` of type `DEED_IN_LIEU` with `decision_log_id` set, template `DIL-CONTRACT` version 2 in `TH`, the three-template set `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1, request key `K-0301`, and the `DIL-CA` version 1 not-approved refusal of AC9 |
| decision-record fake | RWB-PLT-E1027-CON | The entry write and the publish on `rwb.decision-record.v1`, including a forced failure for AC7 |
| guard and permission fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The permission answer behind the letter `C`, the refusal for a role without it, and the scope filter the caller's guard applies |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY with `DOCUMENTS`, LOV-SCOPE with `OWN`, `TEAM`, `REGION` and `ALL`, LOV-ROLE-CLASS with `BANK_USER`, `PARTNER_USER` and `NON_HUMAN_ACTOR` |
| parameters fake | RWB-P3-E1042-CON | The service's own parameter rows, read through the client library of DP-06; none of them changes the access answer |
| gateway-bff route fake | RWB-PLT-N001-CON | The composite route that carries the mask answer of the document screen, so the screen's own calls can be asserted |
| policy pack fixture | this story's own test data | The `PM-2026.12` permission rows for `RW-RESTRUCT`, `RW-CASEOWN`, `RW-TEAMMGR`, `RW-PHONECOL` and `SY-CASEWF`, the `MASK-SIT-01` masking rows for `DF-PTY-007`, and a later masking version for the mixed-pair refusal of X8 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations used), consumed 0 | The decisions are served on `/authorise`, `/me/permissions` and `/masking-policies` of RWB-P4-E1037-CON on `/api/recovery/access/v1` |
| Kafka | Published 2, consumed 0 from other services | `rwb.access.events.v1` and `rwb.decision-record.v1` published; the cache refresh reads this service's own topic |
| Temporal | 0 | No workflow, no activity, no task queue use |
| File | None | No file input or output; the PDF is `rwb-document`'s and never passes through this service |

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
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which patterns have an instance in this slice: DP-01 is the read of `role`, `permission` and `masking_rule` in `rwb_access`; DP-03 is the `AC-READ` and `AC-DENY` entry; DP-07 is the LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS lists; DP-09 is the outbox, the inbox and the request key; DP-11 is the authorise contract with its mock and its 2 s timeout; DP-15 is the per-service sequence the policy tables are created in, in which this story adds nothing; DP-19 is the composite route that carries the mask answer to the document screen. DP-05 and DP-06 have an instance only as an absence on the generation side: this service reads no `v_ace_*` view and no case or party row, and the only parameters it reads are its own service parameters.

The DP work of the legacy key that sits with other slices, and not here:

| DP | Which part of the legacy key it is | Whose it is |
|---|---|---|
| DP-05 | The case, party and collateral facts that fill the merge fields — `transfer_price` 1250000.00, `title_doc_no` "12345", `contract_date` 2026-12-10 and the national ID number from the token service | P1 `rwb-source-data` for the party and collateral values, and P3 `rwb-case` for the case facts |
| DP-06 | The render parameters such as the font, the idempotency hours and the ten-template ceiling | P5 `rwb-document` |
| DP-15 | The three document columns `template_code`, `template_version` and `treatment_id`, their migration and the partial unique index | P5 `rwb-document` |
| DP-09 | The `DocumentStored` event (EV-16) of each generated document | P5 `rwb-document` |

This secondary slice adds no new build dependency of its own (metadata `Depends on (build)` is None): the libraries, the Flyway baseline, the outbox and the gateway route are already build dependencies of the P4 service's own stories, in particular RWB-P4-E1037-CON and the policy pack stories RWB-P4-AD002-APP and RWB-P4-AD004-APP, so the story is Day 1 and builds against the published contract RWB-P5-E2026-CON and its fake. It needs no new migration: its rows of `masking_rule` and `permission` are carried by the P4 access baseline, in the migration that creates those tables, and this story reads them and writes none.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | REST controller | The three operations of 12.1, the problem responses with their message IDs, 404 for a scope refusal, and the request key |
| DocumentRightCheck | Service | The letter `C` in area `DOCUMENTS` under the matrix version in force, for a person or a service identity, with no branch on `role_class` |
| ScopeCheck | Service | The scope comparison of the case reference in the request against `OWN`, `TEAM`, `REGION` or `ALL`, with the refusal of BR4 |
| MaskingPolicyService | Service | The `masking_rule` read for `DF-PTY-007` per role, the masked default, and the mask version in the answer |
| PolicyVersionResolver | Service | The matrix version and the mask version in force, read once per refresh and held together |
| AuthoriseCache | Cache | The cached answer per actor, area, right and object reference, with the matrix and mask versions; refresh on `AccessPolicyChanged`; fail closed on a mixed pair |
| AccessLogWriter | Service | The `AC-READ` and `AC-DENY` entry of DP-03, with the template code list, the request key and the masked field marker, and with no value, in the same transaction as the answer |
| PolicyChangeListener | Kafka consumer with the inbox | The service's own `AccessPolicyChanged`, deduplicated by event ID, refreshing the cache |

**Database and migrations**

- Reads `role`, `permission` and `masking_rule` in `rwb_access`; writes the decision-record entry through the library, and the inbox, outbox and idempotency rows.
- Index `ix_permission_role_area_version ON permission (role_id, capability_area, matrix_version)` already belongs to the P4 access baseline, so the authorise read is one index scan in the cache-miss path; if SIT needs a further index, it is added to that baseline's migration, not to a new one here.
- Index `ix_masking_field_version ON masking_rule (field_id, masking_version, role_code)` likewise; the `DF-PTY-007` mask answer for a set of roles is one scan.
- No new table and no new column in this story: the policy tables are the policy pack path's, and the access log is the decision-record entry (DP-03). The repository of this slice has no write method on `permission` or `masking_rule`.

**Configuration and reference data**

- LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS through the reference-data contract of DP-07 (RWB-P3-E1043-CON); `DOCUMENTS`, `NON_HUMAN_ACTOR` and `ALL` are values of those lists, never constants.
- The matrix version `PM-2026.12` and the masking version `MASK-SIT-01` in force are read from the rows, not configured; the SIT label is assumed (GAP-0940; ASM-1668).
- The service parameters this slice reads are its own service parameters through DP-06 and none of them carries a right, a role or an area; the template parameters `GEN_IDEMPOTENCY_HOURS`, `GEN_MAX_TEMPLATES` and `GEN_FONT` are `rwb-document`'s.
- No switch of this slice's own: a generation call that cannot get an authorise answer must not proceed, so the authorise path has no off state. The legacy flag `rwb.dochub.generation-engine` stays `rwb-document`'s and is a legacy reference here.

**Build steps**

1. `AuthoriseController` and the problem responses, with the three operations, the 404 of the scope refusal and the request key; tests for 401, 403, 404 and 503 shapes.
2. `PolicyVersionResolver` and the two index reads; test that a new matrix version is served as data with no code change.
3. `DocumentRightCheck` for the letter `C` in `DOCUMENTS`; tests for AC1, AC2 and AC4, including the removal of the `SY-CASEWF` row.
4. `ScopeCheck` with the case reference in the request and the `ALL` scope of the service identity; tests for AC3 and AC4.
5. `MaskingPolicyService` with the masked default and the mask version in the answer; tests for AC1, AC4 and AC5, and a scan of the answer and the entry for any part of the synthetic values.
6. `AccessLogWriter` in the same transaction as the answer, with the template code list, the request key and the no-value assertion; tests for AC5, AC6, AC7 and AC8, and the forced failure for AC7.
7. `AuthoriseCache` and `PolicyChangeListener` with the version pair and the mixed-pair refusal; test for AC9's version pair with a fixed clock.
8. The contract-fake run against RWB-P5-E2026-CON, the decision-record fake and the gateway-bff route fake, so the story builds before `rwb-document` exists in the environment.

**Done when.** The tests in section 16 pass; every generation request on case `RW-2026-000301` writes exactly one `AC-READ` entry naming the case, the treatment, the template codes and versions and the request key, with `DF-PTY-007` marked masked and no value of any merge field anywhere in the entry; `RW-TEAMMGR` is refused with MSG-P4-002 and `RW-2026-000306` with MSG-P4-003; `SY-CASEWF` is allowed under its own row with scope `ALL`; every answer names the matrix version and the masking version it was decided under; and a masking policy change is served by the cache after `AccessPolicyChanged` with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not carry Documents `C` | You cannot {action} here. Your role does not include it. | This story, on the authorise path |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, on the scope check |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the entry writer |
| MSG-GEN-001 | A required field of the authorise request is missing | Enter {field}. | This story, on the request validation |
| MSG-GEN-004 | The cached policy was replaced while the call was in flight | Someone else changed this record. Reload it to see their change. | This story, on the version check |
| MSG-P5-009 | A required merge field has no value | {template} cannot be generated. {field} has no value on the case. | `rwb-document`, never this story |
| MSG-P5-010 | No current template version approved by Legal | {template} has no version approved by Legal for {product} in {language}. | `rwb-document`, never this story |
| MSG-P5-011 | The treatment is not approved or not open | Documents can be generated only for an approved {treatment} that is still open. | `rwb-document`, never this story |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. | `rwb-document`, never this story |

The {action} value in MSG-P4-002 names the action and nothing else — for this path, "generate documents" — and the problem response carries the capability area `DOCUMENTS` in its `detail` beside the message ID, so a refusal is diagnosable without any case content. The 404 of MSG-P4-003 carries no case number, no product and no team, because a scope refusal must not confirm that the case exists (BR4). Every error is an RFC 9457 problem response with `messageId` set and `instance` naming the request. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built here, and no screen state belongs to this story. The generated documents are shown by `rwb-document`'s screens, which reach this service through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON):

| Screen | State | What this story supplies |
|---|---|---|
| SCR-30 Case documents | List | The Documents `C` answer behind the generate action, and one `AC-READ` entry per generation request |
| SCR-30 Case documents | DRAFT | The mask answer that keeps `DF-PTY-007` masked beside each generated document; the document state itself is `rwb-document`'s |
| RWB-E2-017 generation screen | Ready | The Documents `C` answer as the screen's guard, so the generate action is offered only to a role that may take it |
| RWB-E2-017 generation screen | Denied | The problem response of MSG-P4-002 with the action and the area, or of MSG-P4-003 for a case out of scope, and the `AC-DENY` entry behind it |

The panel layout, the masked rendering and the composite route's field list are Not specified in the source documents (GAP-0940; ASM-1668); the screen stories are RWB-P5-E2026-APP and RWB-P5-E2017-APP, and this story changes no screen behaviour.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-026-15 | AC2, BR2, BR3 | Component | `RW-TEAMMGR` user `U-4103` with Documents `R` calls the generation path; refused with MSG-P4-002 and one `AC-DENY` entry |
| TC-E2-026-01 | AC1, AC6, BR9 | Contract | Case `RW-2026-000301`, treatment `TRT-0301`, template `DIL-CONTRACT` version 2; the access answer and the entry are the assertion, the document and its decision entry are the contract fake's |
| TC-E2-026-02 | AC5, BR6, BR7 | Contract | Case facts with transfer_price 1250000.00, title_doc_no "12345", contract_date 2026-12-10; the mask answer and the no-value entry are the assertions, MSG-P5-009 is the fake's |
| TC-E2-026-03 | AC9, BR11 | Component | Template `DIL-CONTRACT` version 3 valid from 2026-12-15; the version pair in the answer is re-read, the template choice is the fake's |
| TC-E2-026-04 | AC9, BR9 | Contract | `DIL-CA` version 1 with approved_by_legal false; this story answers allowed and the MSG-P5-010 refusal stays the fake's |
| TC-E2-026-05 | AC9, BR9 | Contract | `DIL-MORTGAGE` withdrawn; the access answer is unchanged and the entry names no template status |
| TC-E2-026-06 | AC9, BR9 | Contract | Treatment `TRT-0302` with no decision_log_id; the access answer is unchanged and MSG-P5-011 stays the fake's |
| TC-E2-026-07 | AC7, BR8 | NFR | The decision-record write forced to fail; 503 MSG-P7-003, no answer and no data, and the cache unchanged |
| TC-E2-026-08 | AC8, BR10 | Component | Request key `K-0301` sent twice; one answer and one `AC-READ` entry |
| TC-E2-026-09 | AC8, BR10 | Component | Two requests for `TRT-0301` and `DIL-CONTRACT` with different keys; two answers and two entries, one of which the fake refuses with MSG-GEN-004 |
| TC-E2-026-10 | AC1, BR9 | Contract | Damaged template body; the access answer is unchanged and MSG-GEN-006 stays the fake's |
| TC-E2-026-11 | AC9, BR1 | Contract | Hire purchase case against a mortgage-only template; the access answer is unchanged and MSG-P5-010 stays the fake's |
| TC-E2-026-12 | AC3, BR4 | Component | Case `RW-2026-000306` of team `HP-NE`, officer of team `FCR-BKK`; 404 with MSG-P4-003 and one `AC-DENY` entry with reason `OUT_OF_SCOPE` |
| TC-E2-026-13 | AC6, BR8 | Component | The three-template set `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1 in one request; exactly one entry naming the three codes and versions |
| TC-E2-026-14 | AC9, BR9 | Contract | Three templates with `DIL-CA` not approved; the access answer is allowed and the whole-set refusal stays the fake's |
| TC-E2-026-16 | AC7, BR8 | NFR | The decision-record write forced to fail during a three-template set; no answer, MSG-P7-003, and no entry survives |

The legacy level System maps to Contract where the rule lives in `rwb-document` and to Component where it lives here, Access maps to Component and Resilience to NFR, and each case asserts only this slice's answer and entry. No case ID with the `-ITG` suffix is used here: the integration copy of the set is RWB-ITG-E2026-ITG, which proves the same facts across `rwb-access`, `rwb-document`, `rwb-comms` and `rwb-treatment` with real services, and its `-ITG` copies belong to that story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the letters C, R, U, D and A, the capability areas, the roles, the scopes, the masking rows and the matrix and mask versions are data rows; the Java code holds no letter, area, role or version literal (BR-P4-004, BR-P4-005).
- No personal data in logs, events, tests, workflow history or prompts: the access entry carries the actor reference, the case and treatment references, the template code list, the field ID and a masked marker. Workflow history is not used because this story starts no workflow.
- No merge value, no national ID number and no borrower name in an entry, an event or a log: the authorise request carries no merge value at all, so none can be written; a test scans the answer and the entry text for any part of `1250000.00`, `12345`, `2026-12-10` and the synthetic national ID number.
- The national ID number exists only inside the stored PDF: this service answers that `DF-PTY-007` is masked and under which version, and the clear value is filled at render time by `rwb-document` from the token service (BR11, CTL-11).
- Service identities are subject to the same checks as people: `SY-CASEWF` holds a `role` row of class `NON_HUMAN_ACTOR` and passes the same letter, scope and masking checks, with no bypass path in code (NFR-051).
- No read of another service's tables and no cross-schema read (DP-01): `recovery_case`, `treatment`, `template`, `merge_field`, `document` and `decision_log_entry` are never queried here.
- ACE data only through the owner's contract or a `v_ace_*` view of this service; this story reads no ACE view at all, and the national ID value stays with `rwb-source-data`.
- An answer is never served without its entry, and the answer and the entry commit in one transaction (R-UNI-39).
- The cache fails closed: an unparseable or mixed policy event leaves the versions in force, and a missing policy row is a refusal, never a default allow.
- The authorise path has no off switch, because a generation call that cannot be authorised must not proceed; the legacy generation flag stays `rwb-document`'s.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-39, R-UNI-40 | TC-E2-026-15, TC-E2-026-01, TC-E2-026-02, TC-E2-026-06 to TC-E2-026-16 |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38 | TC-E2-026-03 to TC-E2-026-05, TC-E2-026-11 |

| Legacy reference | Where it is kept |
|---|---|
| Roles `RW-RESTRUCT` and `RW-CASEOWN` with Documents `C`, `RW-TEAMMGR` with Documents `R`, and the service identity `SY-CASEWF` | Metadata, sections 1, 3, 7, 10 |
| Cases `RW-2026-000301` and `RW-2026-000306`, treatment `TRT-0301` and `TRT-0302`, templates `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1, request key `K-0301` | Background, AC1 to AC3, AC6, AC8, AC9, sections 3, 12.8, 16 |
| The merge values `transfer_price` 1250000.00, `title_doc_no` "12345" and `contract_date` 2026-12-10, and the national ID rule BR11 | Sections 1, 7, 8, 11, 16, 17 |
| MSG-P4-002, MSG-P4-003, MSG-P7-003, MSG-GEN-001, MSG-GEN-004, and MSG-P5-009, MSG-P5-010, MSG-P5-011, MSG-P6-003 as `rwb-document`'s | Section 14, exception paths |
| Matrix version `PM-2026.12` and masking version `MASK-SIT-01`, and no value in the log | Sections 3, 4, 7, 11, 17 |
| Legacy test set TC-E2-026-15, TC-E2-026-01 to TC-E2-026-14 and TC-E2-026-16, and its integration copy RWB-ITG-E2026-ITG | Section 16 |
| Legacy key RWB-E2-026, story RWB-P4-E2026-APP, contract RWB-P5-E2026-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The `rwb-document` slice of this legacy key, RWB-P5-E2026-APP with RWB-P5-E2026-CON: the template selection against the current approved version, the merge field resolution through the providers of P3, S2 and P1, the value formatting, the render to PDF/A-2b, the draft store, the three document columns and their migration, the document rows, the `DocumentStored` event (EV-16), the decision-log entry of decision code `D6.4` and the errors MSG-P5-009, MSG-P5-010, MSG-P5-011, MSG-P6-003, MSG-P7-003 on the generation path.
- The generation, review and send screens of legacy RWB-E2-017 (RWB-P5-E2017-APP), SCR-30 Case documents, and the rendering of a masked field on any screen.
- The `rwb-comms` template catalog and the merge field catalog (RWB-E1-046), the template versions and their Legal approval record (RWB-E1-034), and the template-to-document-type mapping.
- The treatment record, its approval at `D6.4`, its outcome and its lifecycle (`rwb-treatment`, S2) and the case facts, the case state and the case-owner task (`rwb-case`, P3).
- Rule-driven generation when the deed in lieu route reaches `TRANSFER_PRICE_SET` (FEAT-TRT-18, Epic 3): the engine call is that story's, and this story supplies only the `SY-CASEWF` access answer behind it.
- The e-signature flow (RWB-E2-018), debt sale agreements and notices (FEAT-DBS-10, Epic 6), and the dispatch loop of RWB-E2-021.
- The policy pack load path of this service — the reference loads, their approval, verification and rollback, and the rows of `PM-2026.12` and `MASK-SIT-01` themselves (RWB-P4-AD002-APP, RWB-P4-AD004-APP), and the six-monthly access review list (JOB-18).
- The decision log of the generation and its central ledger entry (`rwb-decision`, P7), and the audit query over the access entries (legacy RWB-E1-039).
- The integration harness RWB-ITG-E2026-ITG and its `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of the authorise path (an OPS story of this legacy key).
