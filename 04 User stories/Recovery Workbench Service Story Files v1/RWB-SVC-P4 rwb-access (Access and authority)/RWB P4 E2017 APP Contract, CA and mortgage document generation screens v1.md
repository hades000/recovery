# RWB-P4-E2017-APP Contract, CA and mortgage document generation screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP11, DP13, DP19 |
| Parallel lane | L-P4-AL |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2017-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DCM-012, REQ-OCC-002, REQ-OCC-009) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-017 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer, case owner, team manager and legal counsel who works the contract, credit approval and mortgage document set of a deed in lieu treatment**, I want **an access answer that says whether my role carries the Documents right to generate, open, correct, mark reviewed and send each document of the set, whether the case of that treatment is inside my scope, which of the personal fields of the review view are masked and under which masking version the answer was taken, together with an access entry for every look and every refusal that names the case, the treatment and the document but never a merge value or a borrower detail**, so that **the document set of an approved treatment moves only through roles that may move it and every action on it is recorded as an access event, while the generation, the correction and the send themselves stay where the document engine is**.

Inside `rwb-access` this is the access and field-marker slice of the document generation screens of legacy RWB-E2-017:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The slice delivers four answers and one record behind the screens: the Documents right answer per action — `C` to generate the set, `U` to regenerate a draft with a correction, `R` to open a draft for review, `U` to mark a draft reviewed and to send the set for signature; the scope answer for the case the treatment belongs to; the field markers of the review view with the masking version; the answers' matrix version and masking version; and the access entry written as a decision-record entry of DP-03 with decision code `AC-READ` on every allowed look or action and `AC-DENY` on every refusal.
- The slice builds no screen and produces no document. SCR-14 Treatment record and SCR-30 Case documents are served by the gateway-bff composite route of DP-19; the generation engine, the template selection, the merge values, the regeneration, the write-once copy, the signature request and the document records are `rwb-document`'s, consumed through the published contract RWB-P5-E2017-CON and its fake, one hop, with the 2 s timeout of DP-11. The treatment and its approved decision are `rwb-treatment`'s, the case facts `rwb-case`'s, the merge field catalog and the template versions the template catalog's (RWB-E1-046, RWB-E1-034).
- The authority table of the legacy story is data, not code: `RW-RESTRUCT` and `RW-CASEOWN` hold Documents `CRU`, `RW-TEAMMGR` holds Documents `R`, and `RW-LEGAL` holds Documents `CRUA`, where the `A` is the template approval of RWB-E1-034 and belongs to no action of this story. This slice answers the four letters that the two screens ask for and never answers `A` on this path.
- The review view has two kinds of read-only value and this slice owns only one of them. A merge value the catalog marks locked is read-only by rule — amounts, parties, title numbers and the treatment terms — and `rwb-document` refuses a correction of it with MSG-P5-014 whatever the caller's right; the borrower's personal fields are read-only because they are masked, and that is this slice's field marker under masking version `MASK-SIT-01`, with `DF-PTY-007` among them. The answer therefore carries a masked flag per field ID and never a locked flag, because locked-ness is the catalog's and not a right.
- The policy pack is data: permission rows under matrix version `PM-2026.12`, masking rows under masking version `MASK-SIT-01`. The load path that writes those rows, and the `masking_rule` rows themselves, belong to the P4 access baseline (RWB-P4-E1037-APP, RWB-P4-AD002-APP); this story adds only the rows its capability reads and no migration of its own.

The values carried from the legacy story are unchanged: case `RW-2026-000401` with product group `MORTGAGE` in team `FCR-BKK`, treatment `TRT-0401` of type `DEED_IN_LIEU` approved at D6.4, the set `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1, the contract draft `DOC-0411`, `contract_date` `2026-12-10` corrected to `2026-12-12` with reason "Signing appointment moved by the customer", and the messages MSG-P5-011, MSG-P5-012, MSG-P5-013, MSG-P5-014, MSG-P5-002, MSG-GEN-001, MSG-GEN-004, MSG-GEN-006, MSG-P7-003, MSG-P4-002 and MSG-P4-003.

### 2. Business rationale

A deed in lieu set sent to signature on a document no one was allowed to correct is a Legal finding, and a personal field shown to a role that may not see it is a PDPA finding on the same screen. The legacy story proved that the set is generated, corrected and sent with a record; this slice proves the authorisation and the masking behind those actions. Today the right to touch a document is spread over role documents and manual checks, the borrower's details are copied into review notes, and a look at a document leaves no trace that an auditor can query beside the decision. Under Architecture v5 the right answer and the masking answer come from `rwb-access` as data, with the matrix version and the mask version naming the policy they were taken from, and every look at the set is an append-only entry in the same ledger as the decisions.

This story carries controls CTL-12 and CTL-14 on the access side (a sent document is never changed; only a reviewed set on the current template version is sent, both executed by `rwb-document`), CTL-07 (every correction keeps its old value, its new value and its reason, written by `rwb-document`) and the audit expectation behind NFR-042 (every read of the document store is logged). It meets REQ-DCM-012, REQ-OCC-002 and REQ-OCC-009 on the access side: the set is produced from approved templates, the Legal approval stays against the template version whether or not the caller may send, and the signature path a customer uses is chosen by rule and never by a right of this slice. It supports the measure rule and limit changes made without a code release (target 100 percent) and the restructure turnaround the program targets at 5 days from 23 days.

The realignment changes the mechanism, not the business rule:

1. The permission rows and the masking rows of the monolith's recovery schema become `rwb-access`'s own tables in `rwb_access` (DP-01), versioned by matrix version and mask version, so a change of rights or of masking needs an approved load and no release.
2. The synchronous `RecoveryAccessGuard` call inside the monolith becomes the published authorise contract, cached, with one hop and a 2 s timeout (DP-11); the composite route and `rwb-document` ask `rwb-access` and hold the answer for the life of the cache entry.
3. The decision-log writer inside the monolith becomes the local decision-record library of DP-03, so an `AC-READ` or `AC-DENY` entry is hash-chained and published on `rwb.decision-record.v1` where `rwb-decision`'s ledger and the audit query already read.
4. The access event that the monolith never sent becomes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, and every holder of a cached answer refreshes on it, so a new masking version is in force at the next call with no deployment.
5. The generation, the correction and the send stay in one owning service: `rwb-document` holds the document records, the versions and the write-once copy, and this slice answers only who may ask it for them (DP-11).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2017-CON | The published document contract this slice is tested against: treatment `TRT-0401` of case `RW-2026-000401` approved at D6.4 with the set `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1, the draft `DOC-0411` at doc_version 1 with `contract_date` `2026-12-10`, and the states `DRAFT`, `REVIEWED` and `SENT`, with its contract fake. The request and response shape of the authorise call itself is Not specified in the source documents (GAP-0941; ASM-1670) |
| Permission matrix `PM-2026.12` `IN_FORCE` | The rows this slice answers from, loaded by the policy pack path (RWB-P4-AD002-APP) and read under the matrix version in force: Documents `CRU` for `RW-RESTRUCT` and `RW-CASEOWN`, Documents `R` for `RW-TEAMMGR`, Documents `CRUA` for `RW-LEGAL`, and no Documents row for `RW-PHONECOL`. The TSD P4 v3 matrix carries no Documents column, so the four letters are the legacy authority table's and are assumed for the pack (GAP-0942; ASM-1671) |
| Masking version `MASK-SIT-01` in force | The rows for the personal fields of the review view, with `DF-PTY-007` and `DF-PTY-016` masked for `RW-RESTRUCT`, `RW-CASEOWN`, `RW-TEAMMGR` and `RW-LEGAL`, and no unmask row for any of them, so a borrower's personal field is masked on the review view for every role that may open it. The version label and the field list are assumed for SIT (GAP-0943; ASM-1677) |
| Test users in SIT | `U-4101` holds `RW-CASEOWN` and owns case `RW-2026-000401`; `U-4103` holds `RW-TEAMMGR`; `U-4106` holds `RW-PHONECOL`; the restructuring officer of the legacy story holds `RW-RESTRUCT` with scope team `FCR-BKK` (FSD P4 v3 A2.7 test users) |
| The decision-record library and its topic | `rwb.decision-record.v1` and the local library of DP-03, so an access entry is written, chained and published in one transaction with the answer |
| gateway-bff composite route | The route of DP-19 that carries the screen's authorise, permission and masking calls to this base path, with the 2 s timeout of DP-11 and the field list it sends for the review view |

Business preconditions carried from RWB-E2-017:

- Only an approved, open treatment can have its set generated; the treatment's approval is `rwb-treatment`'s check and never changes the access answer.
- Which merge field is overridable, and which is locked, is the merge field catalog's data owned by Legal; the catalog and its lock flags are not read by this service.
- The template set per treatment type and product, the template versions and the Legal approval against each version are the template catalog's; the `A` letter of `RW-LEGAL` on template approval is RWB-E1-034 and is not answered here.
- Every refusal is answered with MSG-P4-002 naming the action and the capability area, every out-of-scope answer with MSG-P4-003, and neither carries a document, a template or a merge value (FSD P4 v3 A2.4 VR-P4-004-1, A2.14 VR-P4-014-1).

### 4. Flow

1. Restructuring officer: opens SCR-14 Treatment record for treatment `TRT-0401` of case `RW-2026-000401` and chooses Generate documents.
2. gateway-bff composite route: on the screen open, calls `POST /api/recovery/access/v1/authorise` with the caller's user reference, the roles the session resolved, capability area `DOCUMENTS`, right `C`, case `RW-2026-000401` and treatment `TRT-0401` as the object references, the case owner and team for the scope test, and the field list the screen will render.
3. `AuthoriseService`: reads the caller's permission rows for `DOCUMENTS` from `permission` in `rwb_access` under the matrix version in force, unions the letters of every role the caller holds, and answers `allowed` with right `C`, the role `RW-RESTRUCT`, `matrixVersion` `PM-2026.12` and `maskingVersion` `MASK-SIT-01`.
4. `ScopeService`: compares the case's owner, team and region, as sent by the route from the treatment's case, with the caller's scope from `role.default_scope`; an owner scope passes on the owner, a team scope on the team `FCR-BKK`, and anything outside answers 404 with MSG-P4-003.
5. `MaskingPolicyService`: reads the `masking_rule` rows for each field ID of the request and the caller's roles under the mask version in force and answers a marker per field. A field with no covering row is answered masked as well, so the default is refuse rather than show (FSD P4 v3 A2.5, AC-EXC-P4-004-05). No value of any field is read, echoed or cached by this service.
6. `AccessLogWriter`, in the same transaction as the answer: writes the decision-record entry of DP-03 with decision code `AC-READ`, the actor, the case reference, the treatment reference, the capability area, the right, the matrix version, the mask version and the field markers with `DF-PTY-007` marked masked; publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` through the outbox.
7. The route then calls `rwb-document` to generate the set; three drafts appear in types `CONTRACT`, `CREDIT_APPROVAL` and `MORTGAGE_DOCUMENT` from template versions 2, 1 and 1, with the merge values filled. The generation, the merge rules and the drafts are `rwb-document`'s and this service is not called again.
8. Restructuring officer: opens the draft `DOC-0411` on SCR-30. The route calls the authorise path again with area `DOCUMENTS`, right `R`, case `RW-2026-000401`, treatment `TRT-0401`, document `DOC-0411` and the field list of the review view; the answer is allowed with right `R` and one `AC-READ` entry is written.
9. The review view shows the PDF beside the merge values, with the locked values read only as the catalog says and the personal fields masked as the answer says; neither the PDF nor a merge value passes through this service.
10. Restructuring officer: corrects `contract_date` from `2026-12-10` to `2026-12-12` with reason "Signing appointment moved by the customer". The route calls the authorise path with right `U` for document `DOC-0411`; the answer is allowed with right `U`, one `AC-READ` entry is written, and `rwb-document` writes its D6.4 decision entry with the old value, the new value and the reason before it regenerates the draft as doc_version 2.
11. Restructuring officer: marks each draft reviewed. Right `U` is asked per document and each allowed answer writes one `AC-READ` entry; the state change to `REVIEWED` is `rwb-document`'s.
12. Restructuring officer: chooses Send for signature. Right `U` is asked for the treatment and its set; the answer is allowed and one `AC-READ` entry names the treatment and the three documents. `rwb-document` then checks that every document is `REVIEWED` and on the current template version, copies each file to the write-once container, writes its send entry and starts the signature request; the screen shows MSG-P5-012 with count 3.
13. Legal counsel holds Documents `CRUA` on the same set from the same rows and opens the review view with right `R`; the letter `A` is not asked for and is not answered on this path.
14. The cache-refresh listener of this service reads `rwb.access.AccessPolicyChanged.v1` from `rwb.access.events.v1` and replaces the cached answer for the affected roles; the next authorise call answers with the new version and a new mask answer, with no deployment and no restart, and an answer never mixes a matrix version with a mask version from a different policy load.
15. Internal audit (`RW-AUDIT`, scope `ALL`): reads the entries through `rwb-decision`'s decision-log query, where the `AC-READ` and `AC-DENY` entries of the set sit beside the correction and send entries of the same documents.

Every answer and its access entry commit in one transaction (DP-03, R-UNI-39), so a call that cannot be logged is refused rather than answered (FSD P4 v3 AC-EXC-P4-007-03), and a repeated call with the same `Idempotency-Key` returns the first answer without a second entry.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds Documents `R` only and asks for right `U` or `C` | Refused with 403; one `AC-DENY` entry with area `DOCUMENTS` and the right asked; no document changes | MSG-P4-002 | AC5 |
| X2 | The caller holds no Documents row at all | Refused with 403; one `AC-DENY` entry with area `DOCUMENTS` and the right asked; nothing shown and nothing sent | MSG-P4-002 | AC5 |
| X3 | The case of the treatment is outside the caller's scope | Answered 404 with MSG-P4-003; one `AC-DENY` entry with the right asked and no field value | MSG-P4-003 | AC6 |
| X4 | No masking row covers a field for any of the caller's roles | The field is answered masked under the mask version in force; the entry marks it masked; no value is read | None | AC7 |
| X5 | A right `A` is asked on this path | Refused with 403 and MSG-P4-002; the letter `A` of Documents is the template approval of RWB-E1-034 and no action of these screens asks for it | MSG-P4-002 | AC8 |
| X6 | A merge value, a borrower name or a borrower ID is sent to this service | The request is refused as malformed with 422 and the value is not logged; the field list carries field IDs only | MSG-GEN-001 | AC8 |
| X7 | The access entry cannot be written | The call returns 503, no answer and no document data; the reason is logged; the cache is unchanged | MSG-P7-003 | AC10 |
| X8 | A second call arrives with the same `Idempotency-Key` | The first answer and its entry are returned; no second entry is written | None | BR7 |
| X9 | A matrix version and a mask version arrive from two different policy loads | The cache refuses the mixed pair, keeps the versions it already holds and raises the mismatch; the caller gets the older consistent pair | None | AC9 |

An answer is never served without its entry and never without naming both policy versions; a call whose entry fails is an error, not a silent success. The rule checks of P5 — an unapproved treatment (MSG-P5-011), a draft not reviewed or a stale template version (MSG-P5-013), a locked field (MSG-P5-014), an empty reason (MSG-GEN-001), a sent document (MSG-P5-002), a stale version (MSG-GEN-004) and an unavailable signature service (MSG-GEN-006) — are answered by `rwb-document` after the access answer, and none of them changes the answer of this slice.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published document contract RWB-P5-E2017-CON and its fake; the case attributes for the scope test and the field list arrive in the request, never as a table read |
| Negotiable | Letters, roles, areas, masking rows, field IDs and versions are data; the story fixes the answer shape and the entry only |
| Valuable | No screen of the set opens, corrects or sends without a current authorise answer, and a personal field of the review view is masked by policy, not by the screen |
| Estimable | Three existing endpoints, one scope answer, one masking answer, one entry writer, one cache |
| Small | Fits one week with its tests, because the generation, the correction, the send and the screens are other stories' |
| Testable | Every criterion below is one test case in section 16; the treatment, the case, the document and the template versions are returned by the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Access decisions, field markers and access-log entries for the contract, CA and mortgage document screens

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.12" is in force and masking version "MASK-SIT-01" is in force
    Given test user "U-4101" holds RW-CASEOWN and owns case "RW-2026-000401", test user "U-4103" holds RW-TEAMMGR, test user "U-4106" holds RW-PHONECOL and the restructuring officer holds RW-RESTRUCT with scope team "FCR-BKK"
    Given the rwb-document contract mock returns treatment "TRT-0401" of case "RW-2026-000401" with product group "MORTGAGE" in team "FCR-BKK", of type "DEED_IN_LIEU" and approved at D6.4
    Given the rwb-document contract mock returns the set for "DEED_IN_LIEU" as "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, all approved by Legal
    Given the rwb-document contract mock returns draft "DOC-0411" at doc_version 1 with contract date "2026-12-10"

  Scenario: AC1 Generating the set reads DOCUMENTS C and marks the borrower's field masked (new, D-RCV-60)
    Given the rwb-document contract mock returns treatment "TRT-0401" approved at D6.4 with no outcome
    When the restructuring officer chooses Generate documents on SCR-14 and the composite route calls POST /api/recovery/access/v1/authorise with area "DOCUMENTS", right "C", case "RW-2026-000401", treatment "TRT-0401" and the field list "DF-PTY-007"
    Then the answer is allowed with area "DOCUMENTS", right "C", the role "RW-RESTRUCT", matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the answer marks "DF-PTY-007" masked and carries no value of it and no merge value
    Then one access-log entry exists with decision code "AC-READ", the actor reference of the caller, case "RW-2026-000401", treatment "TRT-0401", area "DOCUMENTS" and the field marker "DF-PTY-007" as masked
    Then the entry holds no merge value, no borrower name, no borrower ID and no file name

  Scenario: AC2 Opening a draft for review reads DOCUMENTS R and keeps the locked values read only by rule (new, D-RCV-60)
    Given the rwb-document contract mock returns draft "DOC-0411" of "TRT-0401" in state "DRAFT" with transfer price 1250000.00 locked in the merge field catalog
    When the restructuring officer opens the draft on SCR-30 and the composite route calls the authorise path with area "DOCUMENTS", right "R", case "RW-2026-000401", treatment "TRT-0401", document "DOC-0411" and the field list "DF-PTY-007", "DF-PTY-016"
    Then the answer is allowed with right "R" and names no locked flag and no lock state of any merge value
    Then the answer marks "DF-PTY-007" and "DF-PTY-016" masked under masking version "MASK-SIT-01"
    Then one access-log entry exists with decision code "AC-READ", document "DOC-0411" and the two field markers as masked
    Then the read-only state of transfer price is the merge field catalog's and the screen's, not a right of this answer

  Scenario: AC3 A correction of an overridable value reads DOCUMENTS U and leaves the locked-field rule to rwb-document (new, D-RCV-60)
    Given the rwb-document contract mock returns draft "DOC-0411" at doc_version 1 with contract date "2026-12-10"
    When the restructuring officer corrects contract date to "2026-12-12" with reason "Signing appointment moved by the customer" and the composite route calls the authorise path with area "DOCUMENTS", right "U" and document "DOC-0411"
    Then the answer is allowed with right "U" and one access-log entry exists with decision code "AC-READ", document "DOC-0411" and right "U"
    Then the answer carries no old value, no new value and no reason text
    When the same officer tries to change transfer price from 1250000.00 to 1200000.00, rwb-document refuses it with 422 and MSG-P5-014, and the composite route asks the authorise path with right "U" for document "DOC-0411"
    Then that access answer is allowed as well, because the lock is the catalog's rule and not a missing right

  Scenario: AC4 Marking reviewed and sending the set read DOCUMENTS U for the treatment and its documents (new, D-RCV-60)
    Given the rwb-document contract mock returns the three drafts of "TRT-0401" in state "REVIEWED" and the send request carries Idempotency-Key "S-0401"
    When the restructuring officer chooses Send for signature and the composite route calls the authorise path with area "DOCUMENTS", right "U", treatment "TRT-0401", the three documents and case "RW-2026-000401"
    Then the answer is allowed with right "U" and one access-log entry exists with decision code "AC-READ", treatment "TRT-0401" and the three document references
    Then the answer and the entry carry no template version, no merge value and no file name
    Then the write-once copy, the signature request, the state "SENT" and MSG-P5-012 with count 3 are rwb-document's and this service writes none of them

  Scenario: AC5 A team manager with Documents R is refused the send and may still read (new, D-RCV-60)
    Given test user "U-4103" holds RW-TEAMMGR, whose Documents letters are "R" under "PM-2026.12"
    When "U-4103" calls the authorise path with area "DOCUMENTS", right "U" for treatment "TRT-0401"
    Then the call is refused with status 403 and message MSG-P4-002 for the action "send a document set for signature" and the area "DOCUMENTS"
    Then one access-log entry exists with decision code "AC-DENY", the actor "U-4103", area "DOCUMENTS" and right "U"
    Then the answer and the entry hold no document reference of the set, no merge value and no file name
    When "U-4103" calls the authorise path with area "DOCUMENTS", right "R" for document "DOC-0411"
    Then the answer is allowed with right "R" and one "AC-READ" entry is written

  Scenario: AC6 A case outside the caller's scope is refused with MSG-P4-003 (new, D-RCV-60)
    Given the rwb-document contract mock returns treatment "TRT-0401" of case "RW-2026-000401", which belongs to team "FCR-BKK" and another owner
    When "U-4101" holds RW-CASEOWN with default scope "OWN" and asks the authorise path with area "DOCUMENTS", right "U" for document "DOC-0411"
    Then the call is refused with status 404 and message MSG-P4-003
    Then one access-log entry exists with decision code "AC-DENY", area "DOCUMENTS", right "U" and reason "SCOPE"
    Then no case attribute, no merge value and no document content is returned

  Scenario: AC7 A personal field with no masking row is masked and names its version (new, D-RCV-60)
    Given no masking row in "MASK-SIT-01" holds an unmask flag for "DF-PTY-007" for any role
    When the restructuring officer asks GET /api/recovery/access/v1/masking-policies for "DF-PTY-007" on the review view
    Then the answer is masked under masking version "MASK-SIT-01"
    Then the answer carries no value and no format of the field
    Then the same answer marks "DF-PTY-016" masked under the same version

  Scenario: AC8 The field list the composite route carries holds field IDs and never a value (new, D-RCV-60)
    Given the review view of SCR-30 renders the personal fields "DF-PTY-007" and "DF-PTY-016"
    When the composite route calls the authorise path with area "DOCUMENTS", right "R", document "DOC-0411" and the field list "DF-PTY-007", "DF-PTY-016"
    Then the answer holds one marker per field ID of the request, each with its masked flag, and the masking version "MASK-SIT-01"
    Then the answer holds no value of either field and no field outside the request
    When the route sends the borrower's name in the field list instead of a field ID, the call is refused with 422 and MSG-GEN-001 and nothing of the value is logged

  Scenario: AC9 A policy change reaches the cached answer without a deployment (new, D-RCV-60)
    Given the cached answer for "U-4101" holds matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    When the policy pack load commits a mask row set under a masking version later than "MASK-SIT-01" and publishes rwb.access.AccessPolicyChanged.v1
    Then the next authorise call for "U-4101" answers with the later masking version and the mask answer of that version
    Then no deployment, restart or cache flush is performed and the matrix version in the answer stays "PM-2026.12"
    Then the answer never pairs the new masking version with a matrix version from a different load

  Scenario: AC10 An access entry that cannot be written stops the answer (new, D-RCV-60)
    Given the decision-record library refuses the write
    When the restructuring officer asks the authorise path with area "DOCUMENTS", right "U" for document "DOC-0411"
    Then the call returns status 503 with message MSG-P7-003
    Then no answer and no document data are returned and the cached answer is unchanged
    Then no entry with decision code "AC-READ" exists for that call
```

The ten criteria above are the ones this story owns and each is new under D-RCV-60. The legacy criteria of RWB-E2-017 are served across the two slices and are named here for trace: legacy RWB-E2-017 AC1 (Generate) is answered here by AC1 and by `rwb-document`; legacy AC2 (Review) by AC2 and AC3 here and by the correction and regeneration in `rwb-document`; legacy AC3 (Send) by AC4 here and by the write-once copy, the signature request and MSG-P5-012 in `rwb-document`; legacy AC4 to AC13 by the exception rules of `rwb-document`, with AC5 and AC7 of this story asserting that the access answer never changes because of them. No legacy criterion is copied as a criterion of this story.

The authorise request and response shape used above — actor, roles, area, right, case, treatment and document references, case owner and team for the scope test, and the field ID list in, and allowed, roles, area, right, matrix version, masking version, field markers, scope result and messageId out — is Not specified in the source documents (GAP-0941; ASM-1670); no field of it is a business value and it is renamed at the contract review if the published contract differs.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A right is taken from the permission rows of the matrix version in force, per role and capability area, with letters C, R, U, D and A; no letter, role, area or version is written in code | FSD P4 v3 A2.4; BR-P4-004; TSD P4 v3 T6.1 |
| BR2 | Generating the set needs Documents `C`; opening a draft for review needs Documents `R`; regenerating with a correction, marking reviewed and sending the set need Documents `U`; the letter `A` is the template approval of RWB-E1-034 and is never answered on this path | Legacy RWB-E2-017 sections 4 and 12; TSD P4 v3 T3.2 LOV-CAPABILITY |
| BR3 | A role with no Documents row is denied, and a role with Documents `R` is denied right `U` and right `C`; the authorise path refuses by default and never falls back to a broader role or to a default letter | FSD P4 v3 A2.4 AC-EXC-P4-004-06; Architecture v5 zero trust, deny by default |
| BR4 | The access answer depends on the rights, the scope and the policy versions only: the approval of the treatment, the review state of a document, the current template version, the lock of a merge field and the presence of a reason are `rwb-document`'s checks and never change the access answer | Legacy RWB-E2-017 BR2, BR3, BR6; FSD P4 v3 A2.4 VR-P4-004-1 |
| BR5 | A personal field of the review view is shown masked unless a masking row for the role and the field says unmasked, and a field with no covering row stays masked; the mask version is named in the answer | FSD P4 v3 A2.5 AC-EXC-P4-004-05, A2.7 AC-P4-007-01; BR-P4-005 |
| BR6 | The case of the treatment must be inside the caller's scope under `role.default_scope`; an out-of-scope case is answered 404 with MSG-P4-003 and never a partial document | FSD P4 v3 A2.14 VR-P4-014-1, AC-EXC-P4-004-01 |
| BR7 | Every allowed look or action writes one `AC-READ` entry and every refusal one `AC-DENY` entry, in one transaction with the answer, and a call that cannot be logged is refused; a repeat with the same `Idempotency-Key` returns the first answer without a second entry | FSD P4 v3 A2.7 AC-P4-007-01, AC-EXC-P4-007-03 and AC-EXC-P4-007-04; DP-03; R-UNI-39 |
| BR8 | An answer names the matrix version and the masking version it was decided under, and a policy change reaches the cached answer through `rwb.access.AccessPolicyChanged.v1` with no deployment | FSD P4 v3 A2.4 AC-P4-004-01; Architecture v5 slides 20 and 42 |
| BR9 | No personal data and no business value in the entry: the access-log entry carries the field ID and a masked marker, never a value, and never a merge value, a borrower name, a borrower ID or a file name | Legacy RWB-E2-017 section 17; FSD P4 v3 A2.7; NFR-042; TSD P4 v3 T7 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` in `rwb_access` under the matrix version in force; the capability areas are the LOV-CAPABILITY values read through the reference-data contract of DP-07, and the Java code holds no enum of areas, roles or letters.
- BR2 is one check on the letter of the requested right in the area `DOCUMENTS`; the four actions are told apart by the right in the request and not by an action code the service owns, and `A` is refused because no row of this path asks it.
- BR3 is a missing row, which is a refusal, never a default; the letters of two roles are unioned, so a caller holding both `RW-TEAMMGR` and `RW-RESTRUCT` reads and writes.
- BR4 is the absence of any business field in the authorise request except the object references and the case attributes of the scope test: no treatment state, no review state, no template version and no merge field value is sent, so no check here can disagree with `rwb-document`.
- BR5 is the `masking_rule` read plus the default; the mask format is the library's, because no source fixes a rendering for a personal field of this review view (GAP-0943; ASM-1677).
- BR6 is the comparison of the case owner, team and region with the scope of the caller's roles; the case attributes come from the route in the request, and this service reads no case table.
- BR7 is one `RecordAndApply` transaction on the answer and the entry, with the idempotency key of DP-09.
- BR8 is the version pair in the answer and the cache refresh on the service's own `AccessPolicyChanged`.
- BR9 is a check on the entry writer: the field list it writes is the field ID and the masked flag, and a test scans the entry text for any digit of a merge value and for any part of a borrower reference.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No cached answer | Authorise call | The policy rows are in force | Allowed or denied, with the matrix and masking versions |
| Allowed | The answer is served | The `AC-READ` entry commits | Served, with the scope result and the field markers |
| Denied | The refusal is served | The `AC-DENY` entry commits | Refused with 403 and MSG-P4-002, or 404 and MSG-P4-003 |
| Cached under version `PM-2026.12` / `MASK-SIT-01` | `rwb.access.AccessPolicyChanged.v1` | A later policy load is in force | Cached under the new versions, served from the next call |
| Cached, mixed versions | Refresh | The event names a matrix version and a masking version from different loads | Unchanged, with the mismatch raised |

| From | Event | Condition | To |
|---|---|---|---|
| `LOADED` | The policy pack load is approved | The approver is not the loader | `APPROVED` |
| `APPROVED` | The valid-from date is reached | None | `IN_FORCE`, and `AccessPolicyChanged` is published |
| `IN_FORCE` | The next version is approved | None | `SUPERSEDED` |

The second table is the lifecycle of the rows this story reads, owned by RWB-P4-AD002-APP; this story reads the version in force and publishes nothing on that path itself.

The document states of the legacy story — `DRAFT` with doc_version + 1 on a correction, `REVIEWED` on a mark, `SENT` with `write_once true` on a send — are `rwb-document`'s, are not changed by this story and are asserted here only as the object the access answer refers to. Access-log entries have no lifecycle of their own: they are append-only and are read by `rwb-decision`'s decision-log query.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT Restructuring officer (FCR) | Generates the set (Documents `C`), opens a draft (`R`), corrects an overridable value and marks reviewed (`U`), and sends the set for signature (`U`) in scope |
| RW-CASEOWN Case owner | The same rights as RW-RESTRUCT on the same set, from the same rows |
| RW-TEAMMGR Team manager | Opens the drafts and the sent documents (`R`); right `U` and right `C` are refused with MSG-P4-002 |
| RW-LEGAL Legal counsel | The same rights as RW-RESTRUCT, from Documents `CRUA`; the letter `A` is the template approval of RWB-E1-034 and no action of this story asks for it |
| RW-AUDIT Internal audit | Reads the access and decision entries with scope `ALL`, and the policy versions they were decided under |
| RW-PHONECOL and every role with no Documents row | Refused by default, with a `AC-DENY` entry |
| SY-DECLOG and the NON_HUMAN_ACTOR identities of LOV-ROLE-CLASS | Service identities: the decision-record library's write of the entry; a service identity is asked under the scope of the case it works and receives no broader answer than a person (NFR-051) |

No approval level from the delegation of authority applies: the treatment was approved at D6.4 before generation, so no `delegation_limit` row is read on this path and the holder check of a limit-based approval is RWB-P4-E2013-APP's. The lock of a merge field and the review state of a document are not in this table, because `rwb-document` executes them before and after it asks this service.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | role_code, role_name, role_class, default_scope | Read |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | role_code, conflicts_with, conflict_version | Read, only to report a conflicting pair to the session that asks for permissions |
| DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | `delegation_limit` | approval level, product and limits | Not read: no approval level applies to this path |
| DF-PTY-007 | the borrower's personal field, owned by P1 and named by the FSD P4 v3 A2.7 access entry | the field ID only | Not read as a value: the answer names the field and the masked marker only |
| DF-PTY-016 | the party contact field, owned by P1 and named by the FSD P4 v3 A2.7 access entry | the field ID only | Not read as a value: the answer names the field and the masked marker only |
| DF-DOC-001, DF-DOC-004, DF-DOC-011 | `document` (owned by P5, read through the owner's contract of DP-11) | id, document_type, doc_version | Not read: the reference arrives in the request and is copied into the entry |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` or `AC-DENY` entry: decision code, actor, object references, area, right, versions, field markers, time | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (idempotency) | `idempotency_key` | the stored answer of an authorise call with its key | Write |

The masked rendering of the review view's personal fields is Not specified in the source documents (GAP-0943; ASM-1677); this story names the field IDs, the roles and the mask version and leaves the format to the one masking library every screen uses. Field IDs are those in the Logical Data Model and Data Dictionary v8. No `masking_rule` row and no `permission` row is created by this story: the rows it reads are the policy pack's, loaded by RWB-P4-AD002-APP, and this slice adds no migration of its own.

### 12. Contract

#### 12.1 REST operations provided

None new. The answers are served through the operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1`, owner P4 `rwb-access`; this secondary slice adds no path, no query parameter and no response field, invents no path outside `/api/recovery/access/v1`, and decides the `DOCUMENTS` area and the field markers behind the three operations:

| Method | Path | Purpose | Authorization | Errors |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The Documents right for one action of the set, the scope result for the treatment's case, the mask version and the field markers | The caller's own session; the answer is the decision | 401; 403 MSG-P4-002; 404 MSG-P4-003; 422 MSG-GEN-001; 503 MSG-P7-003 |
| GET | `/api/recovery/access/v1/me/permissions` | The caller's resolved roles, letters per capability area including `DOCUMENTS`, scope, matrix version and masking version | None beyond the session | 401; 503 |
| GET | `/api/recovery/access/v1/masking-policies` | The masking answer for a field ID and a role, with the mask version | None beyond the session | 401; 503 |

Architecture v5 slide 14 names `POST /authorise`, `GET /me/permissions` and `/masking-policies` on `rwb-access`; the TSD P4 v3 appendix T-A has no authorise path, so the answer is carried on the baseline contract of RWB-P4-E1037-CON and this story extends none of its paths. The request and response shape of `POST /authorise` is Not specified in the source documents (GAP-0941; ASM-1670). `GET /doa-limits` of the same slide exists and is not used here, because no approval level applies to the document set.

#### 12.2 REST operations consumed

None. The treatment, the case reference and its owner and team, the document references and the field list are sent in the authorise request by the composite route, which composes them from the `rwb-document` contract RWB-P5-E2017-CON and the `rwb-case` case read; this service calls no other service on this path, so the call stays one hop with the 2 s timeout of DP-11 and a circuit breaker. One consequence is recorded: the scope test is made on attributes supplied by the caller, and a wrong owner or team in the request is a wrong scope answer, which is why the route takes them from the treatment's case and not from the screen (ASM-1670).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | matrix or mask version | the policy kind, the old and new version, validFrom, the affected capability areas or fields, the load reference |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | the entry ID | the hash-chained `AC-READ` or `AC-DENY` entry of DP-03 |

CloudEvents 1.0 envelope; neither payload carries personal data or a merge value. The `AccessPolicyChanged` event is written by the policy load path of this service (RWB-P4-AD002-APP) in the same transaction as the rows, and this story's part is the refresh it triggers.

#### 12.4 Events consumed

None from another service. The cache refresh reads this service's own `rwb.access.AccessPolicyChanged.v1` from `rwb.access.events.v1` through an internal listener, which is not a cross-service subscription; no `rwb.document.*`, `rwb.case.*` or `rwb.treatment.*` event is read, so the document set reaches this service only as an object reference in a request. The refresh fails closed: a policy event that does not parse leaves the cache on the versions it already holds (X9).

#### 12.5 Workflows and activities

None. This story starts no workflow and registers no activity; the document set is produced and sent inside `rwb-document`, and the case is `CaseWorkflow` in `rwb-case`.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) is a Temporal Schedule of this service and belongs to its own story; the authorise path has no clock.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The roles the caller holds, their class and default scope |
| `permission` | P4 (`rwb_access`) | The letters per capability area under the matrix version in force |
| `masking_rule` | P4 (`rwb_access`) | The unmasked flag per role and field under the mask version in force |
| `role_conflict` | P4 (`rwb_access`) | The conflicting pair reported to a session that asks for permissions |
| `delegation_limit` | P4 (`rwb_access`) | Not read here; no approval level applies to the document set |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |

`document`, `document_type`, `merge_field`, `template`, `treatment`, `recovery_case` and `decision_log_entry` are other services' and are not read: the references are named in the request and in the entry, the value stays with its owner, and the ledger entry is written through the library (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document document and treatment WireMock | RWB-P5-E2017-CON | Treatment `TRT-0401` of case `RW-2026-000401`, product group `MORTGAGE`, team `FCR-BKK`, approved at D6.4; the set `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1; draft `DOC-0411` at doc_version 1 with contract date `2026-12-10`, transfer price 1250000.00, and the states `DRAFT`, `REVIEWED` and `SENT`; the approved-but-closed treatment `TRT-0402` |
| decision-record fake | RWB-PLT-E1027-CON | The entry write and the publish on `rwb.decision-record.v1`, including a forced failure for AC10 |
| guard and permission fakes | RWB-PLT-E1037-CON and RWB-P4-E1037-CON | The guard library's call of the authorise answer and the baseline permission view, so the composite route's calls can be asserted without the screen |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY with the value `DOCUMENTS` and LOV-SCOPE with `OWN`, `TEAM`, `REGION` and `ALL` |
| gateway-bff route fake | RWB-PLT-N001-CON | The composite route that carries the authorise, permission and masking calls of SCR-14 and SCR-30, with the 2 s timeout and its field list |
| policy pack fixture | this story's own test data | The `PM-2026.12` Documents rows of `RW-RESTRUCT`, `RW-CASEOWN`, `RW-TEAMMGR`, `RW-LEGAL` and `RW-PHONECOL`, the `MASK-SIT-01` rows for `DF-PTY-007` and `DF-PTY-016`, and a later masking version for AC9 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations used), consumed 0 | The answers are served on `/authorise`, `/me/permissions` and `/masking-policies` of RWB-P4-E1037-CON on `/api/recovery/access/v1` |
| Kafka | Published 2, consumed 0 from other services | `rwb.access.events.v1` and `rwb.decision-record.v1` published; the cache refresh reads this service's own topic |
| Temporal | 0 | No workflow, no activity, no task queue use |
| File | None | No file input or output; the documents and their files never reach this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/documents`, Java package `th.co.scb.ace.workbench.recovery.access.documents`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which patterns have an instance in this slice: DP-01 is the read of `permission`, `masking_rule` and `role` in `rwb_access`; DP-03 is the `AC-READ` and `AC-DENY` entry; DP-07 is the LOV-CAPABILITY area list and the LOV-SCOPE values of the scope test; DP-11 is the published `rwb-document` contract with its fake and its 2 s timeout; DP-13 is the base path; DP-19 is the composite route of SCR-14 and SCR-30.

The DP work of the legacy key that sits with the P5 slice is named so that no one reads this story as the screen or the engine: the React components GenerateDocumentsPanel and GeneratedDocumentReview, the generation and regeneration calls, the merge-value handling, the write-once copy, the signature request and the document records are all `rwb-document`'s (RWB-P5-E2017-APP with RWB-P5-E2017-CON), and DP-19 has an instance on both slices because the route composes both services.

This secondary slice adds no H dependency of its own (metadata H = None). The libraries the table names are already build dependencies of the service's own stories: the decision-record library and the outbox come with the P4 service baseline (RWB-PLT-E1027-CON, RWB-PLT-TE006-CON), the reference-data client with DP-07 (RWB-PLT-E1043-CON, RWB-P3-E1043-CON), the Flyway baseline with the P4 DB story (RWB-PLT-E1044-CON), and the composite route with the gateway-bff contract (RWB-PLT-N001-CON). The story is therefore Day 1 and builds against the published contract RWB-P5-E2017-CON.

The `masking_rule` table, its migration and its rows belong to the P4 access baseline — RWB-P4-E1037-APP for the access service baseline and RWB-P4-AD002-APP for the policy pack load — and this story adds only the rows its capability reads: the `DOCUMENTS` permission rows of the four roles and the `MASK-SIT-01` rows of `DF-PTY-007` and `DF-PTY-016`. It creates no table, no column and no index of its own.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | REST controller | The three operations of 12.1, the problem responses with their message IDs, the idempotency key and the field-ID list of the request |
| AuthoriseService | Service | Resolution of the caller's letters for one area and right, the union across roles, the version pair in the answer |
| ScopeService | Service | The scope test of the treatment's case against `role.default_scope`, with the case attributes sent by the route |
| MaskingPolicyService | Service | The `masking_rule` read per field ID and role set, the masked default, the mask version and the markers |
| DocumentFieldMarker | Service | The field-marker list of the review view: a marker per field ID asked, a masked leaf per field, and never a value |
| AuthoriseCache | Cache | The cached answer per user, area, right and object, with the matrix and mask versions; refresh on `AccessPolicyChanged`; fail closed on a mixed pair |
| AccessLogWriter | Service | The `AC-READ` and `AC-DENY` entry of DP-03, with the object references and the masked markers and no value, in the same transaction as the answer |
| PolicyChangeListener | Kafka consumer with the inbox | The service's own `AccessPolicyChanged`, deduplicated by event ID, refreshing the cache |

**Database and migrations**

- Reads `role`, `permission`, `masking_rule` and `role_conflict` in `rwb_access`; writes the decision-record entry through the library, and the inbox, outbox and idempotency rows.
- Index `ix_permission_role_area_version ON permission (role_id, capability_area, matrix_version)`, so the authorise read is one index scan in the cache-miss path.
- Index `ix_masking_field_version ON masking_rule (field_id, masking_version, role_code)`, so the mask answer for a field and a set of roles is one scan.
- No new table and no new column: the policy tables are the access baseline's and the policy pack path's, and the access log is the decision-record entry (DP-03). This story adds no migration file; the two indexes above are additions to the baseline's own migration and are recorded in its story.

**Configuration and reference data**

- LOV-CAPABILITY, LOV-ROLE and LOV-SCOPE through the reference-data contract of DP-07 (RWB-P3-E1043-CON); the area `DOCUMENTS` is a value of that list, never a constant.
- The matrix version `PM-2026.12` and the masking version `MASK-SIT-01` in force are read from the rows, not configured; the SIT label and the field list are assumed (GAP-0943; ASM-1677).
- The access entry's decision codes `AC-READ` and `AC-DENY` follow the decision-code list of the ledger, and the field markers come from the request.
- No switch of this slice's own: a screen that cannot get an authorise answer must not open, so the authorise path has no off state. The legacy flag `rwb.dochub.generation-screens` and its send flag stay `rwb-document`'s and are a legacy reference here.

**Build steps**

1. `AuthoriseController` and the problem responses, with the three operations, the field-ID validation and the idempotency key; tests for 401, 403, 404, 422 and 503 shapes.
2. `AuthoriseService` for rights `C`, `R` and `U` on `DOCUMENTS` and the refusal of `A`; tests for AC1, AC2, AC4, AC5 and the legacy TC-E2-017-14 case.
3. `ScopeService` with the case attributes sent by the route, then test AC6 through the route fake.
4. `MaskingPolicyService` and `DocumentFieldMarker` with the masked default, the per-field marker and the mask version; tests for AC2, AC7 and AC8.
5. `AccessLogWriter` in the same transaction as the answer, with the object references and the masked markers, and the no-value, no-merge-value assertion; tests for AC1, AC3, AC5 and AC8, and the forced failure for AC10.
6. `AuthoriseCache` and `PolicyChangeListener` with the version pair and the mixed-pair refusal; test for AC9 with a fixed clock.
7. The contract-fake run against RWB-P5-E2017-CON, RWB-PLT-E1037-CON, RWB-P4-E1037-CON, RWB-P3-E1043-CON and the gateway-bff route fake, so the story builds before `rwb-document` and the screens exist in the environment.
8. The audit read of the entries through `rwb-decision` and the assertion that a correction, a refusal and a send of the same set sit beside each other in one query.

**Done when.** The tests in section 16 pass; every open of a draft and every action on the set writes exactly one `AC-READ` entry naming the case, the treatment and the document, the actor and the masked field IDs, with no merge value, no borrower name and no borrower ID anywhere in the entry; every refusal writes one `AC-DENY` entry with its area, right and reason; every answer names the matrix version and the masking version it was decided under; and a masking policy change is served by the cache after `AccessPolicyChanged` with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not carry the right in the area | You cannot {action} here. Your role does not include it. | This story, on the authorise path |
| MSG-P4-003 | The case of the treatment is outside the caller's scope | This case is not in your scope. | This story, when the scope test fails |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the entry writer |
| MSG-GEN-001 | A required field of the authorise request is missing, or a value is sent where a field ID belongs | Enter {field}. | This story, on the request validation |
| MSG-GEN-004 | The cached policy was replaced while the call was in flight | Someone else changed this record. Reload it to see their change. | This story, on the version check |
| MSG-P5-011 | The treatment is not approved or not open | Documents can be generated only for an approved {treatment} that is still open. | `rwb-document`, after the access answer |
| MSG-P5-012 | The set was sent for signature | {count} documents were sent for signature. | `rwb-document`, after the send |
| MSG-P5-013 | A document is not reviewed or not on the current template version | {document} cannot be sent yet: {reason}. | `rwb-document`, before the send |
| MSG-P5-014 | A correction to a locked merge field | {field} comes from the approved treatment and cannot be changed here. | `rwb-document`, on the correction and never this story |
| MSG-P5-002 | A change to a sent document | Legal documents cannot be changed. Add a new version instead. | `rwb-document`, on the correction |
| MSG-GEN-006 | The signature service is unavailable | {system} is not available. Your request is queued and will be retried. | `rwb-document`, on the signature request |

The {action} value in MSG-P4-002 names the action and nothing else — for this set, "generate the document set", "open a document", "correct a document", "mark a document reviewed" or "send a document set for signature" — and the problem response carries the capability area in its `detail` beside the message ID, so a refusal is diagnosable without any document content. Every error is an RFC 9457 problem response with `messageId` set and `instance` naming the request. No message of this table carries a merge value, a borrower name, a borrower ID or a file name.

### 15. Screens and states

No screen is built here. The screens are `rwb-document`'s and reach this service through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON):

| Screen | State | What this story supplies |
|---|---|---|
| SCR-14 Treatment record | Approved | The Documents `C` answer behind Generate documents and the Documents `U` answer behind Send for signature, with the scope result of the treatment's case |
| SCR-14 Treatment record | Draft, submitted | The same answers; the disabled Generate with MSG-P5-011 is `rwb-document`'s, and the access answer does not change |
| SCR-30 Case documents | List | The Documents `R` answer per document, the masked marker of each personal field with the mask version beside it, and one `AC-READ` entry per document opened |
| SCR-30 Case documents | Read only (common state) | The `R` answer for `RW-TEAMMGR`, the masked markers, and no `U` or `C` answer |
| SCR-30 Case documents | Correction | The Documents `U` answer behind the correction form, with the reason and the locked-field rules left to `rwb-document` |
| SCR-14 Treatment record | Denied | The problem response of MSG-P4-002 or MSG-P4-003 with the action and the area, and the `AC-DENY` entry behind it |

The panel layout, the masked rendering and the composite route's field list are Not specified in the source documents (GAP-0944; ASM-1678); the screen stories are RWB-P5-E2017-APP and the document engine stories in `rwb-document`, and this story changes no screen behaviour.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-017-14 | AC5, BR2, BR3 | Component | `U-4103` with `RW-TEAMMGR` (Documents `R`) calls the send and the regenerate paths; 403 with MSG-P4-002 and one `AC-DENY` entry each, and the read of `DOC-0411` allowed |
| TC-E2-017-01 | AC1, BR1, BR2 | Contract | `TRT-0401` of `RW-2026-000401` with the three approved templates; this slice asserts the Documents `C` answer and the entry, the generation is the contract fake |
| TC-E2-017-02 | AC2, AC3, BR2, BR9 | Contract | `contract_date` `2026-12-10` corrected to `2026-12-12` with reason "Signing appointment moved by the customer"; this slice asserts the `U` answer and the entry with no old value, no new value and no reason |
| TC-E2-017-03 | AC4, BR2, BR7 | Contract | Three reviewed drafts of `TRT-0401`; this slice asserts the `U` answer and one entry naming the treatment and the three documents, the send itself returns `ACCEPTED` from the contract fake |
| TC-E2-017-04 | AC1, BR4 | Contract | Treatment `TRT-0402` with no decision_log_id; the Documents `C` answer is unchanged and the refusal with MSG-P5-011 is the contract fake's |
| TC-E2-017-05 | AC3, BR4 | Contract | Correction of `contract_date` with an empty reason; the `U` answer is still allowed and MSG-GEN-001 is the contract fake's |
| TC-E2-017-06 | AC2, AC3, BR4 | Component | `transfer_price` locked in the merge field catalog at 1250000.00 and attempted at 1200000.00; the answer carries no lock flag and MSG-P5-014 is the contract fake's |
| TC-E2-017-07 | AC4, BR4 | Contract | Two drafts `REVIEWED` and `DIL-MORTGAGE` in `DRAFT`; the `U` answer is unchanged and MSG-P5-013 is the contract fake's |
| TC-E2-017-08 | AC2, AC3, BR4 | Contract | `DOC-0411` in state `SENT`; the `R` answer is allowed, the `U` answer is allowed, and the 409 with MSG-P5-002 is the contract fake's |
| TC-E2-017-09 | AC10, BR7 | NFR | The decision-record write forced to fail on a correction; 503 with MSG-P7-003, no answer, no data and the cache unchanged |
| TC-E2-017-10 | AC4, BR7, BR8 | Contract | The same send with Idempotency-Key "S-0401" twice; the first answer and its entry return and no second entry is written |
| TC-E2-017-11 | AC3, BR7 | Contract | Two officers on `DOC-0411` at version 4, the first saved so the record is at version 5; the second `U` answer is allowed and the 409 with MSG-GEN-004 is the contract fake's |
| TC-E2-017-12 | AC4, BR4 | Contract | Signature service `UNAVAILABLE`, then `ACCEPTED`; the `U` answer is unchanged, the 503 with MSG-GEN-006 is the contract fake's and the documents stay `REVIEWED` |
| TC-E2-017-13 | AC4, BR4 | Contract | `DIL-CONTRACT` version 3 current after the drafts; the `U` answer is unchanged and MSG-P5-013 with "template version 3" is the contract fake's |
| TC-E2-017-15 | AC10, BR7, BR9 | NFR | The decision-record write forced to fail on the send; 503 with MSG-P7-003, no entry, nothing sent and the documents stay `REVIEWED` |

The legacy level System maps to End to end for the `rwb-document` slice; here the business rule is `rwb-document`'s and this slice asserts the access answer and the entry against its contract fake, so those cases are Contract. Access maps to Component and Resilience to NFR. Each case asserts only this slice's answer, field markers and entry. No case ID with the `-ITG` suffix is used here: the integration copy of the set is RWB-ITG-E2017-ITG, which proves the same facts across `rwb-access`, `rwb-document` and `rwb-case` with real services, and its `-ITG` copies belong to that story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the letters C, R, U, D and A, the capability areas, the roles, the scopes, the masking rows, the field IDs and the matrix and mask versions are data rows; the Java code holds no letter, area, role, field ID or version literal (BR-P4-004, BR-P4-005).
- No personal data in logs, events, tests, workflow history or prompts: the access entry carries the actor reference, the case, treatment and document references, the field ID and a masked marker. Workflow history is not used because this story starts no workflow.
- ACE data only through the owner's contract or a `v_ace_*` view of this service; this story reads no ACE view at all, and the personal field is named, never fetched.
- No merge value, no borrower name and no borrower ID in an entry: a test scans the entry text for any digit of a merge value and for any part of a synthetic borrower reference, and the field marker list is the only field content written.
- No business value in code, second reading: which merge field is locked, which document is on which template version and whether a treatment is approved are `rwb-document`'s and the catalog's data and are absent from every request of this slice, so no check here can drift from them.
- No read of another service's tables and no cross-schema read (DP-01): `document`, `document_type`, `merge_field`, `template`, `treatment`, `recovery_case` and `decision_log_entry` are never queried here.
- An answer is never served without its entry, and the answer and the entry commit in one transaction (R-UNI-39).
- The cache fails closed: an unparseable or mixed policy event leaves the versions in force, and a missing policy row is a refusal, never a default allow.
- The authorise path has no off switch, because a screen that cannot be authorised must not open; the document flags stay `rwb-document`'s.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | BR1, BR2, BR3, BR4, BR7 | TC-E2-017-01 to TC-E2-017-04, TC-E2-017-09, TC-E2-017-10, TC-E2-017-14, TC-E2-017-15 |
| REQ-OCC-002 | Templates versioned with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | BR2, BR4, BR5 | TC-E2-017-05, TC-E2-017-06, TC-E2-017-08, TC-E2-017-13 |
| REQ-OCC-009 | A customer signs an agreement electronically where Legal permits it, and by wet ink where Legal requires it | Epic 2 requirement list; Program requirement list | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | BR2, BR4, BR7 | TC-E2-017-03, TC-E2-017-12, TC-E2-017-14 |

REQ-DCM-012 and REQ-OCC-002 take their short names from legacy RWB-E2-017 section 18, which carries those two requirements and no third; REQ-OCC-009 is carried by the same legacy story in BR8 and its short name is taken from the Epic 2 requirement list, because legacy section 18 does not repeat it. The three requirements are met here on the access side only: the generation, the template approval and the signature path are `rwb-document`'s and are asserted in RWB-P5-E2017-APP.

| Legacy reference | Where it is kept |
|---|---|
| Roles RW-RESTRUCT and RW-CASEOWN with Documents CRU, RW-TEAMMGR with Documents R, RW-LEGAL with Documents CRUA | Metadata, sections 3, 7, 8, 10 |
| Case `RW-2026-000401`, treatment `TRT-0401`, set `DIL-CONTRACT` version 2 / `DIL-CA` version 1 / `DIL-MORTGAGE` version 1, draft `DOC-0411`, contract date `2026-12-10` to `2026-12-12`, reason "Signing appointment moved by the customer" | Background, AC1 to AC5, sections 3, 12.8, 16 |
| MSG-P4-002, MSG-P4-003, MSG-P7-003, MSG-GEN-001, MSG-GEN-004, MSG-P5-002, MSG-P5-011 to MSG-P5-014, MSG-GEN-006 | Section 14, exception paths |
| Masked personal field on the review view, and no value and no merge value in the access log | Sections 4, 7, 11, 17 |
| Legacy test set TC-E2-017-14, TC-E2-017-01 to TC-E2-017-13, TC-E2-017-15, and its integration copy RWB-ITG-E2017-ITG | Section 16 |
| Legacy key RWB-E2-017, story RWB-P4-E2017-APP, contract RWB-P5-E2017-CON, matrix `PM-2026.12`, mask `MASK-SIT-01` | Metadata, sections 3, 12 |

### 19. Out of scope

- The `rwb-document` slice of this legacy key, RWB-P5-E2017-APP with RWB-P5-E2017-CON: the generation engine, the template set per treatment type, the merge values and their lock flags, the regeneration as the next doc_version, the review state, the write-once copy, the signature request, the document records and the screens SCR-14 and SCR-30.
- The generation engine of RWB-E2-026 (RWB-P5-E2026-APP) and its generated-documents operation on the `rwb-document` base path.
- Template authoring and the Legal approval of templates, and the `A` letter of Documents on that approval (RWB-E1-034, RWB-E1-046).
- The write-once container and its hash guard (RWB-TE-012), the signature path choice between e-signature and wet ink (RWB-E2-018), and the dispatch of the signed set or of a letter (RWB-E2-021, RWB-E2-022).
- The policy pack load path of this service — the reference loads, their approval, verification and rollback, and the rows of `PM-2026.12` and `MASK-SIT-01` themselves (RWB-P4-AD002-APP, RWB-P4-AD004-APP) — and the access service baseline it reads (RWB-P4-E1037-APP).
- The delegation of authority table and its lookup for limit-based approvals (RWB-P4-E2013-APP), role, scope and sign-in administration, break-glass, and the six-monthly access review list (JOB-18).
- The case facts, the case state and the task of an unapproved treatment (`rwb-case`, `rwb-treatment`), and the full case record view (RWB-P3-E1023-APP).
- The integration harness RWB-ITG-E2017-ITG and its `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of the authorise path (an OPS story of this legacy key).
