# RWB-P4-E1054-APP Review queue for low-confidence documents

**Version 3 changes.**

- MSG-GEN-006 and MSG-P4-001 carry the English text of Error and Message Standard v6 (RD-P1-004).
SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1054-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-054 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P4-E1054-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-X |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1054-CON; RWB-P4-E1037-CON (in force) |
| Contract version | /v1 path of /api/recovery/access/v1; exact version Not specified in the source documents (DOR-RWB-P4-E1054-APP-23) |
| Contract fake published | Not specified in the source documents (DOR-RWB-P4-E1054-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DCM-005, REQ-DCM-019) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-054 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E1054-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 18 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF), case owner (RW-CASEOWN), team manager (RW-TEAMMGR), compliance and PDPA officer (RW-COE) or internal auditor (RW-AUDIT) who works the document review queue**, I want **the access service to answer, for one review item or one stored document in front of me, whether my role may read it, which scope admits it, whether my role may resolve it, and which of the fields it carries come back masked**, so that **a low-confidence document is shown only to the people entitled to work it, a correction is offered only to the role that may make it, and no OCR text and no extracted value ever leaves the document service on the strength of this answer**.

Inside `rwb-access` this is the access-side capability of legacy RWB-E1-054:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability answers four questions behind the three operations the service already publishes, `POST /authorise`, `GET /me/permissions` and `GET /masking-policies`, and it adds no operation: does the caller hold Documents right R for the item, document, its content and the queue; does the caller hold Documents right U for resolve (`SET_TYPE`, `ATTACH`, `DISCARD`), for the field confirm and correct and for the review completion; does the scope in force admit this item or this document; and which of the field IDs the caller asks about are returned masked. The queue endpoints, SCR-31 Document review queue, the intake rows, the documents, the fields, the candidates, the review outcome, the labeled set, DocumentStore and the DOCATT entry stay in `rwb-document` (P5) and are RWB-P5-E1054-APP's; this story builds no screen, stores no document and starts no job.
- The item and document facts the decision needs — the item reference, its review reason, its predicted type, its candidates, its review team and its candidate cases, and for a stored document its case, the case's team and owner and the field IDs in `REVIEW` — arrive in the authorise request, built by `rwb-document` from its own rows. The attribute set of an authorise request for a review item, including the review team of an unattached item, is Not specified in the source documents (GAP-0988; ASM-1736).
- The policy the answers come from is data in `rwb_access`: the role list, the role-to-permission matrix version in force (`PM-2026.12`), the scope rule with LOV-SCOPE, and the masking rows (`MASK-SIT-01`). The parameter `REVIEW_TEAM_UNATTACHED` belongs to `rwb-document` and is read as a value in the request: this service compares the caller's team with it and writes no copy of it. Loading and approving a policy pack is the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP and is out of scope here.
- The access log is a decision-record entry on `rwb.decision-record.v1` written through the local library of DP-03: `AC-READ` for a granted read of an item or its content with the item reference, the field IDs and their masked markers, `AC-DENY` for a refusal with the area DOCUMENTS and the right and no item fact (FEAT-ACA-07, FEAT-ACA-08).

The legacy behaviour carried into the access service is unchanged: the same scope rule of RWB-E1-054 `BR2` (an item with no case goes to the review team named by `REVIEW_TEAM_UNATTACHED` and to roles whose default scope is ALL; an item with candidate cases and a stored document go by case scope), the same refusal of a role that holds Documents R only when it tries to resolve (legacy X12, access test TC-E1-054-18), the same "not in your scope" answer with no fact for an item or a document outside the scope (legacy AC16), and the same masking of extracted values with no covering row meaning masked (legacy BR10, AC-EXC-P4-004-05).

### 2. Business rationale

A wrong type or a wrong hearing date on a court notice puts the wrong date on a case and the litigation timers run from it, which is why RWB-E1-054 routes every item the pipeline could not type, read or match to a person. That person reads OCR text and extracted values of documents that belong to customers, so the queue is a PDPA surface before it is a work list: CTL-09 and CTL-11 sit on the scope of the queue and on the masking of field values, NFR-039 and NFR-040 require masking by role at rest and in use, NFR-042 requires every read of the document store to be logged, and REQ-DCM-019 forbids any document leaving the hub silently. A queue that is readable by every role that can sign in, or that answers with a value instead of a marker, defeats all four controls at once.

This story supplies the authority slice of that queue: the two rights (Documents R for reading, Documents U for resolving), the scope rule of the queue, and the masked markers for the fields it shows, behind the three operations `rwb-access` already publishes. It meets REQ-DCM-005 and REQ-DCM-019 on the access side, and supports the measure "rule and limit changes made without a code release" at 100 percent, because the matrix, the scope values, the masking rows and their versions are data. The measure of success is that every read of a review item or a stored document is granted or refused by the policy in force, that a role holding Documents R is never granted a resolve, that a field with no masking row comes back masked, and that every granted read leaves one `AC-READ` entry naming the field IDs and their markers and nothing else.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1037-CON | The service contract of `rwb-access` already in force from wave 1: `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on base `/api/recovery/access/v1`, with the role-to-permission matrix and the masking rows as data (legacy RWB-E1-037). This story implements the decision behind those operations for the review queue; it adds no operation |
| RWB-P5-E1054-CON | The document hub contract the authorise request is built from: the intake item read with its review reason, predicted type, candidates and review team, the item content, the stored document read with its case and review status, the field IDs in `REVIEW`, and the resolve, field and completion calls. Which attributes of them an authorise request carries is Not specified in the source documents (GAP-0988; ASM-1736) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the answer |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract that carries LOV-SCOPE with the version in force (DP-07); `lov_value` stays P3's, and no scope string is written in code |
| RWB-PLT-E1047-CON | The naming library behind the topic and event names of DP-14 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence in `rwb_access` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves SCR-31 (DP-19); the route and the screen are P5's story |

Business preconditions carried from RWB-E1-054, owned by other services where they say so:

- Permission matrix version `PM-2026.12` is in force and gives DOCUMENTS right CRU to RW-LITOFF and RW-CASEOWN, right R to RW-TEAMMGR and RW-COE, right CRUA to RW-AUDIT and no right to RW-REFADM, with default_scope OWN for RW-CASEOWN, TEAM for RW-LITOFF and RW-TEAMMGR and ALL for RW-AUDIT (FSD P4 A2.4, A2.30; TSD P4 T3.2 LOV-SCOPE; legacy section 10). That these are the letters of the matrix version at the release date is assumed (GAP-0988; ASM-1737).
- Masking version `MASK-SIT-01` is in force. That this is the masking version of the SIT environment, and which review-field IDs it covers, are Not specified in the source documents (GAP-0988; ASM-1740).
- The review team of an unattached item is held as `REVIEW_TEAM_UNATTACHED` and read in the request. Its legacy assumed value is `DOC-SVC`; the production value per environment is Not specified in the source documents (GAP-0755; GAP-1010). The review team of each environment is agreed by RW-COE and loaded as a data row. The document hub keeps its own row for its screen (RWB-P5-E1054-APP); this story names the key and writes none of it (legacy section 3; ASM-1736).
- SCR-31 Document review queue and its states exist (RWB-P5-E1054-APP), and the queue endpoints `/review-items`, `/document-intake/{intakeId}`, the content read, the resolve call, the field update and `/documents/{documentId}/review` are P5's.
- The caller signed in through Entra ID with multi-factor authentication and holds at least one Recovery role; with no role the answer is 401 MSG-P4-001 (FSD P4 A2.1).
- The database login is the rwb-access login (DP-02). Its name is Not specified in the source documents (GAP-0988; ASM-1736); the story says "the rwb-access login (DP-02)" and never the shared monolith login.
- The platform contracts the DP rows name are already in place behind RWB-P4-E1037-CON in wave 1. This secondary slice adds no new build dependency of its own (metadata H = None).

### 4. Flow

1. Caller: a review user opens SCR-31. gateway-bff resolves the session; `rwb-document` reads the item or the stored document from its own rows and builds the authorise request.
2. Caller: the request names the area `DOCUMENTS`, the right — `R` for the queue read, the item read, the content read and the document read, `U` for resolve, for the field confirm and correct and for the review completion — the item reference or the document reference, the scope attributes the policy reads (the owning user reference, the review team of an unattached item, the candidate cases with their team and region, the case of a stored document with its team, region and owner) and the field IDs the screen is about to show. The full attribute set is Not specified in the source documents (GAP-0988; ASM-1736).
3. `rwb-access`: resolves the caller's roles from the session the ACE common module resolved at sign-in, and the rights from `permission` for the matrix version in force, `PM-2026.12`. `role`, `permission`, `matrix_version` and their versions are read from `rwb_access` only.
4. `rwb-access`, right check: no DOCUMENTS R for any role the caller holds gives a refusal, 403 with MSG-P4-002 naming the action, and no item fact (BR1). The refusal is written as an `AC-DENY` entry (BR7).
5. `rwb-access`, resolve check: for right `U` the caller must hold the letter `U`; a caller holding Documents R only is refused 403 with MSG-P4-002 naming the action, before any item or candidate is read (BR1; legacy X12). The refusal is an `AC-DENY` entry and the item is untouched.
6. `rwb-access`, scope check: an item with no case and no candidate case is in scope when the caller's team is the review team the request names — the `REVIEW_TEAM_UNATTACHED` value of the document hub — or when the caller's `default_scope` in force is `ALL`; an item with candidate cases and a stored document are in scope when the candidate case or the document's case satisfies the caller's `default_scope` read from LOV-SCOPE: OWN for a case the caller owns, TEAM for a case of the caller's team, REGION for a case of the caller's region, ALL for any case (BR2; legacy BR2).
7. `rwb-access`: an item or a document outside the scope is answered 404 with MSG-P4-003 and no fact, so the answer never confirms that an item or a document exists, and the refusal is written as an `AC-DENY` entry (BR3).
8. `rwb-access`, masking: for each field ID the request names, the marker is read from `masking_rule` for the roles the caller holds and the masking version in force, `MASK-SIT-01`. A field with no covering row is masked (BR5). The answer marks each field `masked` or `clear`; it never carries the value, the extracted value or the OCR text (BR5).
9. `rwb-access`: writes one `AC-READ` decision record through the library of DP-03, with the item reference or the document reference, the field IDs and their masked markers, and returns the answer to the caller inside the 2 s timeout of DP-11 (BR6; AC-READ).
10. `rwb-access`: caches the policy answer for the versions in force. A caller that asks again under the same versions is answered from the cache and reads no matrix row twice; the `AC-READ` entry is still written for that read (BR9).
11. Policy change: a new matrix version (`PM-2026.13`) or a new masking version (`MASK-SIT-02`) is approved through the load path, `rwb-access` writes the rows and publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`; every caller drops its cached answer and the next request is answered under the new version, with no deployment (BR9).
12. Document service: performs the resolve, the field confirm or correct and the review completion on its own rows and renders SCR-31 with the granted fields and their masked markers, or the "not in your scope" page for a 404 (RWB-P5-E1054-APP).

Every answer, granted or refused, is written before it is returned; when the record cannot be written nothing is returned, the call answers 503 with MSG-P7-003 and an incident is raised, so no read of a review item is ever unlogged (BR6, BR7, BR8).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The item or the document is outside the caller's scope | Not found: 404 with no item fact; one `AC-DENY` entry, no item fact | MSG-P4-003 | AC5, AC3 |
| X2 | The caller holds Documents R only and calls resolve, corrects a field or completes a review | Refused before any item fact is read: 403, no item and no candidate | MSG-P4-002 | AC4, AC7 |
| X3 | No masking rule covers a review field | The field is marked `masked` with the default marker; the read is otherwise granted | None | AC6 |
| X4 | The token carries no Recovery role, or no second factor | No answer is given: 401 before the policy is read; one refusal entry with the reason | MSG-P4-001 | AC9, BR4 |
| X5 | The decision record cannot be written | Nothing is shown: 503 with no item fact, and an incident is raised to the platform administrator queue | MSG-P7-003 | AC7, TC-E1-054-19 |
| X6 | Two roles of the caller conflict (for example RW-SECADM with a business role) | The sign-in access check refuses the session from the `role_conflict` rows this service holds; no authorise request is made | MSG-P4-006 | AC10, BR4 |
| X7 | The caller is an agent or a service identity, not a person | The same checks run under the service identity's roles; a service identity with no role is refused 401 | MSG-P4-001 | AC11, BR4, section 10 |
| X8 | The reference list of scope is not available | No answer is given rather than a guessed one: 503; the refusal is recorded | MSG-GEN-006 | AC12, BR2 |
| X9 | A new type is set on the item and extraction runs again for it | Not this story's: the re-run and its fields are P5's; the access answer is recomputed on the next read with the new field IDs | None | AC13 |

An answer that spans two masking versions in force on the same day is not specified in the source documents (GAP-0988; ASM-1737); until it is, the version whose `valid_from` is the latest on or before the business date is used, and the answer names the version it used. The legacy attach case X13 / TC-E1-054-19 is the document side of the record-before-the-answer rule: the attach transaction, its document and its DOCATT entry are P5's, and this story's record is the read and the refusal.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against RWB-P5-E1054-CON and the contract fake of the item and document facts; reads its own schema only and calls no other service at run time |
| Negotiable | The policy pack — roles, letters, scope values, masking rows and their versions — is data; the story fixes the shape of the answer, the scope rule and the refusal behaviour only |
| Valuable | The queue reaches the people entitled to work it, a correction is offered only to the role that may make it, and no value or OCR text crosses the boundary on this answer |
| Estimable | Four answers behind three existing operations, one cache, one decision-record path and two indexes |
| Small | Fits one sprint with its tests; no screen, no document, no job and no workflow |
| Testable | Every owned criterion has a test case in section 16; the document side is a published fake |

### 7. Acceptance criteria

```gherkin
Feature: Review queue for low-confidence documents

  Background:
    Given the environment is SIT
    Given the service is rwb-access with schema "rwb_access" behind the base path "/api/recovery/access/v1"
    Given permission matrix version "PM-2026.12" is in force and gives DOCUMENTS letters "CRU" to RW-LITOFF and RW-CASEOWN, "R" to RW-TEAMMGR and RW-COE, "CRUA" to RW-AUDIT and "-" to RW-REFADM
    Given the default scope in force is "OWN" for RW-CASEOWN, "TEAM" for RW-LITOFF and RW-TEAMMGR and "ALL" for RW-AUDIT
    Given the scope list LOV-SCOPE holds "OWN", "TEAM", "REGION" and "ALL" with its version in force
    Given masking version "MASK-SIT-01" is in force
    Given the rwb-document contract mock returns intake item "IN-0101" with review_reason "LOW_CONFIDENCE", predicted type "COURT_NOTICE" at 0.6200, candidates "COURT_NOTICE 0.6200" and "DEMAND_LETTER 0.2100", review team "LIT-BKK", no case and no candidate case
    Given the rwb-document contract mock returns document "DOC-0103" on case "RW-2026-000202" with review_status "PENDING" and field "black_case_no" in state "REVIEW"

  Scenario: AC1 A review officer's read of the queue is granted with field markers (new, D-RCV-60)
    Given test user "U-5101" holds RW-LITOFF with default scope "TEAM" in team "LIT-BKK"
    Given the rwb-document contract mock returns intake item "IN-0101" in review team "LIT-BKK" with field IDs DF-DOC-015 and DF-DOC-034 in state "REVIEW"
    When the caller asks POST /api/recovery/access/v1/authorise for area "DOCUMENTS", right "R", item "IN-0101", review team "LIT-BKK" and field IDs DF-DOC-015 and DF-DOC-034
    Then the answer is granted with scope "TEAM" under matrix version "PM-2026.12"
    Then the answer marks DF-DOC-015 and DF-DOC-034 "masked" under masking version "MASK-SIT-01"
    Then the answer carries no field value and no OCR text
    Then one AC-READ decision record is written with the item reference "IN-0101" and the two field IDs marked "masked"

  Scenario: AC2 An item with no case is visible to the review team and to scope ALL (new, D-RCV-60)
    Given test user "U-5101" holds RW-LITOFF in team "LIT-BKK"
    Given test user "U-5103" holds RW-AUDIT with default scope "ALL" in team "AUD-01"
    Given the rwb-document contract mock returns intake item "IN-0101" in review team "LIT-BKK" with no case and no candidate case
    When "U-5101" asks for area "DOCUMENTS", right "R" and item "IN-0101" with review team "LIT-BKK"
    Then the answer is granted with scope "TEAM"
    When "U-5103" asks for the same item with review team "LIT-BKK"
    Then the answer is granted with scope "ALL"
    When a caller holding RW-LITOFF in team "HP-NE" asks for the same item with review team "LIT-BKK"
    Then the answer is refused with status 404 and message MSG-P4-003

  Scenario: AC3 A stored document is admitted by case scope (new, D-RCV-60)
    Given test user "U-5101" holds RW-LITOFF in team "LIT-BKK"
    Given the rwb-document contract mock returns document "DOC-0103" on case "RW-2026-000202" of team "LIT-BKK" owned by "U-5101"
    When "U-5101" asks for area "DOCUMENTS", right "R", document "DOC-0103" and field ID DF-DOC-015
    Then the answer is granted with scope "TEAM"
    Then when the rwb-document contract mock returns the same document on a case of team "HP-NE" owned by another user
    Then the same request is refused with status 404 and message MSG-P4-003

  Scenario: AC4 A team manager holding Documents R is refused on resolve (new, D-RCV-60)
    Given test user "U-5102" holds RW-TEAMMGR, whose DOCUMENTS letters in "PM-2026.12" are "R"
    Given the rwb-document contract mock returns intake item "IN-0101" in review team "LIT-BKK"
    When "U-5102" asks for area "DOCUMENTS", right "U", item "IN-0101" and action "resolve the item"
    Then the answer is refused with status 403 and message MSG-P4-002 with action "resolve the item"
    Then the answer names no review team, no candidate and no field marker

  Scenario: AC5 An item outside the scope is not found (new, D-RCV-60)
    Given test user "U-5101" holds RW-LITOFF in team "LIT-BKK"
    Given the rwb-document contract mock returns intake item "IN-0110" in review team "HP-NE" with no case
    When "U-5101" asks for area "DOCUMENTS", right "R" and item "IN-0110" with review team "HP-NE"
    Then the answer is refused with status 404 and message MSG-P4-003
    Then the answer carries no item fact: no review reason, no candidate, no field marker and no case number

  Scenario: AC6 A field with no masking rule is masked (new, D-RCV-60)
    Given no masking rule in "MASK-SIT-01" covers DF-DOC-015 for any role
    Given test user "U-5101" holds RW-LITOFF in team "LIT-BKK"
    Given the rwb-document contract mock returns intake item "IN-0101" in review team "LIT-BKK" with field IDs DF-DOC-015 and DF-DOC-017 in state "REVIEW"
    When "U-5101" asks for area "DOCUMENTS", right "R", item "IN-0101" and field IDs DF-DOC-015 and DF-DOC-017
    Then the answer marks DF-DOC-015 "masked" with the default marker "XXXX-XX-XX"
    Then the answer marks DF-DOC-017 "masked"
    Then the read is otherwise granted and one AC-READ entry names both field IDs as "masked"

  Scenario: AC7 A refusal is recorded with no item fact, and a failed record answers nothing (new, D-RCV-60)
    Given test user "U-5102" holds RW-TEAMMGR, whose DOCUMENTS letters in "PM-2026.12" are "R"
    When "U-5102" asks for area "DOCUMENTS", right "U" and item "IN-0101" and the answer is refused
    Then one AC-DENY decision record is written with area "DOCUMENTS", right "U" and result "REFUSED"
    Then the record carries no item reference, no review team, no candidate case and no field marker
    Then when the decision-record library is forced to fail and "U-5101" asks for item "IN-0101" with right "R"
    Then the call answers status 503 with message MSG-P7-003 and no item fact is shown
    Then no AC-READ entry exists for that read and an incident is raised

  Scenario: AC8 A policy and masking version change reaches the answer with no deployment (new, D-RCV-60)
    Given test user "U-5101" holds RW-LITOFF in team "LIT-BKK"
    Given the rwb-document contract mock returns intake item "IN-0101" in review team "LIT-BKK"
    When "U-5101" asks for item "IN-0101" with area "DOCUMENTS" and right "R" twice under matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the second answer is served from the cached decision without a second read of the permission matrix
    Then each answer is returned inside the 2 s timeout and each granted read writes its own AC-READ entry
    Then when policy version "PM-2026.13" and masking version "MASK-SIT-02" are approved and rwb.access.AccessPolicyChanged.v1 is published for both
    Then the next ask is answered under matrix version "PM-2026.13" and masking version "MASK-SIT-02" with no deployment
    Then the earlier change from "PM-2026.11" to "PM-2026.12" reached the answer the same way

  Scenario: AC9 A caller with no Recovery role or no second factor is refused before the policy is read (new, D-RCV-60)
    Given a test user holds no Recovery role in the token
    When the caller asks POST /api/recovery/access/v1/authorise for area "DOCUMENTS", right "R" and item "IN-0101"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then no permission row is read and one AC-DENY decision record is written with the reason

  Scenario: AC10 Two conflicting roles of a caller refuse the session at sign-in (new, D-RCV-60)
    Given a test user holds RW-SECADM together with a business role
    When the test user signs in
    Then the session is refused from the role_conflict rows of rwb_access with message MSG-P4-006
    Then no authorise request is made

  Scenario: AC11 A service identity with no role is refused (new, D-RCV-60)
    Given a service identity holds no role
    When the service identity asks POST /api/recovery/access/v1/authorise for area "DOCUMENTS", right "R" and item "IN-0101"
    Then the answer is refused with status 401 and message MSG-P4-001

  Scenario: AC12 A read is not answered when the scope list is not available (new, D-RCV-60)
    Given test user "U-5101" holds RW-LITOFF in team "LIT-BKK"
    Given the scope list LOV-SCOPE is not available
    When "U-5101" asks for area "DOCUMENTS", right "R" and item "IN-0101" with review team "LIT-BKK"
    Then the answer is refused with status 503 and message MSG-GEN-006
    Then no scope is guessed and the refusal is recorded

  Scenario: AC13 A new type on an item changes the fields the next read answers (new, D-RCV-60)
    Given test user "U-5101" holds RW-LITOFF in team "LIT-BKK"
    Given the rwb-document contract mock returns intake item "IN-0101" in review team "LIT-BKK" with a new type and new field IDs after extraction runs again
    When "U-5101" asks for area "DOCUMENTS", right "R", item "IN-0101" and the new field IDs
    Then the access answer is recomputed on this read with the new field IDs and marks each one "masked"

  Scenario: AC14 A caller with no Recovery role or no second factor is refused on every operation (new, D-RCV-60)
    Given a test user holds no Recovery role in the token or no second factor
    When the caller asks POST /api/recovery/access/v1/authorise, GET /me/permissions or GET /masking-policies
    Then each answer is refused with status 401 and message MSG-P4-001
    Then no permission row is read before the refusal and one AC-DENY decision record is written with the reason
```

AC1 to AC14 are the criteria this story owns; the document-side criteria AC1 to AC17 of the legacy key are owned by RWB-P5-E1054-APP/CON and are proved against this story's answers. In AC1 the two assertions that belong to this service are the scope it names and the masked markers on the field IDs; the queue list, its order and its content are P5's. In AC2 the two callers prove that an unattached item is admitted by the review team and by scope ALL, and that a caller whose team is another team is answered 404 rather than a list. In AC3 the same document follows its case and not its reader, so a document of another team is not found. In AC4 and AC7 the refusal is proved twice for the same legacy case: as the answer the caller gets, with no item fact, and as the refusal entry the audit reads; the second half of AC7 is the record-before-the-answer rule of X13 applied to a read. In AC5 the 404 carries no review reason, no candidate and no case number, so the answer never confirms that the item exists. In AC6 the default is masked when no row covers the field, which is AC-EXC-P4-004-05 of the FSD and BR10 of the legacy key. In AC8 the cached answer is proved to change on the policy event, for both the matrix and the masking version, with no deployment.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Documents right R gates the queue read, the intake item read, its content read and the document read; Documents right U gates resolve (`SET_TYPE`, `ATTACH`, `DISCARD`), the field confirm and correct and the review completion; a caller whose roles hold no such right is refused with MSG-P4-002 naming the action and no item fact | FSD P4 A2.4 VR-P4-004-1; legacy RWB-E1-054 X12, TC-E1-054-18 and section 12 authorization rows; FEAT-ACA-04 |
| BR2 | An intake item with no case and no candidate case is in scope when the caller's team is the review team named by `REVIEW_TEAM_UNATTACHED` in the request, or when the caller's `default_scope` in force is ALL; an item with candidate cases and a stored document are in scope when the candidate case or the document's case satisfies the caller's `default_scope`: OWN, TEAM, REGION or ALL | legacy RWB-E1-054 BR2, AC14; FSD P4 A2.14 VR-P4-014-1; LOV-SCOPE; CTL-09 |
| BR3 | An item or a document outside the scope is answered 404 with MSG-P4-003 and no fact, so the answer never confirms that it exists | FSD P4 A2.14 VR-P4-014-1; legacy RWB-E1-054 X10, AC16 |
| BR4 | No Recovery role, or no second factor, is answered 401 with MSG-P4-001 before the policy is read, and one refusal entry is written with the reason | FSD P4 A2.1 VR-P4-001-1, AC-EXC-P4-001-01; TSD P4 T6.2 |
| BR5 | A review field is marked `masked` unless a `masking_rule` row for a role the caller holds and that field says unmasked true for the masking version in force; with no covering row the field is masked; the answer carries markers only, never a value, an extracted value or OCR text | FSD P4 A2.5; AC-EXC-P4-004-05; NFR-039; NFR-040; legacy RWB-E1-054 BR10 |
| BR6 | Every granted read of an intake item, its content or a stored document writes one `AC-READ` decision record with the item or document reference and the field IDs with their masked markers, before the answer is returned | FSD P4 A2.7 AC-P4-007-01, A2.8; FEAT-ACA-07; FEAT-ACA-08; NFR-042 |
| BR7 | Every refusal writes one `AC-DENY` decision record with the area DOCUMENTS and the right, and carries no item reference and no case fact | FSD P4 A2.7 AC-EXC-P4-007-04; FEAT-ACA-07 |
| BR8 | The record is written before the answer; when it cannot be written nothing is shown, the call answers 503 with MSG-P7-003 and an incident is raised | FSD P4 AC-EXC-P4-007-03; legacy RWB-E1-054 X13, TC-E1-054-19; DP-03 |
| BR9 | An answer is cached for the matrix and masking versions in force and dropped when `AccessPolicyChanged` arrives, so a policy change takes effect with no deployment | Architecture v5 slide 43; FSD P4 AC-P4-004-01; DP-11 |
| BR10 | The intake rows, the documents, the fields, the comments, the review outcome, the labeled set, DocumentStore and the DOCATT entry are `rwb-document`'s; this service holds no item, no document and no field and reads no foreign table | DP-01; ownership map (document, document_intake, document_field, document_text, document_checklist_item to P5) |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` for the caller's roles and the `matrix_version` in force; the letters C, R, U, D and A are held as the five-character field of TSD P4 T3.1, and the answer names the version it used. Documents R and Documents U are two letters of one row, so the resolve refusal of AC4 costs one read and no join.
- BR2 is the scope rule of `ScopeRule` comparing the attributes of the request with the `default_scope` value read through DP-07. The unattached-item rule is one branch of it: it compares the caller's team with the review team value the request carries, which is `REVIEW_TEAM_UNATTACHED` of the document hub, and it reads the parameter from no table of this service. The scope names OWN, TEAM, REGION and ALL are list values, never Java constants, and the attribute names of a request are Not specified in the source documents (GAP-0988; ASM-1736).
- BR3 is the same rule answering not found rather than forbidden, because a 403 on an out-of-scope item would confirm that the item exists; the refusal entry is the only place the attempt is recorded.
- BR4 is the sign-in check this service already holds the rows for; it runs before any policy read, so a caller with no role costs no query.
- BR5 is a read of `masking_rule` by `field_id`, `role_code` and `masking_version`; the answer carries markers, never values, so no personal data crosses the boundary in either direction (NFR-039, NFR-040). The OCR text and the extracted values never enter this service at all: they are P5's and are not part of any request or answer.
- BR6, BR7 and BR8 are the same `RecordAndApply` transaction as the answer: the record is written first, the answer is returned after it commits, and a failure answers 503 with MSG-P7-003 and shows nothing.
- BR9 is a cache keyed by the pair of versions in force; the `AccessPolicyChanged` entry that drops it is published by the same transaction that writes the new policy rows.
- BR10 is the reason there is no repository for an item or a document: the service holds `role`, `permission`, `masking_rule`, `role_conflict`, the decision record, the outbox and the inbox, and nothing else.

### 9. State transitions

None for a case or a document. This story changes no case status, no intake item, no document review status, no field state and no review outcome: `document_intake.review_outcome`, `document.review_status` and `document_field.state` are P5's and move on P5's calls (legacy section 9). This story runs no workflow of its own and owns no Schedule. REVIEW_TEAM_UNATTACHED is a value of the document hub read as the review team of BR2; it is not a value of LOV-SCOPE, and this story adds no value to LOV-SCOPE.

The only states this story has are the states of its answer and of its record, which it does not persist beyond the record:

| Answer state | When | What the caller gets | Record written |
|---|---|---|---|
| Granted | The caller holds the right and the item or the document is in scope, by the review-team rule or by case scope | The granted answer with the scope it used, the item or document reference, and the masked or clear marker per field ID | `AC-READ` |
| Refused, no right | No role of the caller holds Documents R, or the caller holds R only and asks for U | 403 MSG-P4-002 naming the action, no item fact | `AC-DENY` |
| Not found | The caller holds the right and the item or the document is outside the scope | 404 MSG-P4-003, no item fact | `AC-DENY` |
| Not answered | The record cannot be written, or the scope list cannot be read | 503 with MSG-P7-003 or MSG-GEN-006, nothing shown | None; the failure is raised as an incident |

The review-team rule of BR2 has no stored state: it is computed per request from the review team the request carries and the caller's team and default scope, so an item that acquires a candidate case moves from the review-team rule to the case-scope rule on the next request with no call between the services.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Documents CRU with default scope TEAM: reads the queue, an item of its review team and a document of its team's cases, and is granted resolve; the resolve itself is P5's |
| RW-CASEOWN, case owner | Documents CRU with default scope OWN: reads an item or a document of its own cases and is granted resolve on them |
| RW-TEAMMGR, team manager | Documents R with default scope TEAM: reads the queue for the team; refused 403 MSG-P4-002 on resolve, on a field correction and on a review completion |
| RW-COE, center of excellence analyst | Documents R: reads the queue and the labeled examples through the model evaluations; no resolve and no correction |
| RW-AUDIT, internal audit | Documents CRUA with default scope ALL: reads any item and any document; the field markers stay `masked` |
| RW-COMPLY, Compliance and PDPA officer | Reads which masking version is in force and which fields it covers through `GET /masking-policies`; this story writes no value on their behalf and grants no item on that basis |
| RW-REFADM and every role with no Documents right | Refused with MSG-P4-002 on every read of the queue, an item, its content or a document |
| SY-OCR, OCR and extraction pipeline | Documents CRU as a service identity: asks the same question before re-running extraction on a type change, and its roles are checked as a person's are |

No delegation-of-authority level applies to a review: a review is a read with a correction, not an approval with a limit, so the DoA table and its lookup are RWB-P4-E2013-APP's and RWB-P4-E2014-APP's and this story reads no `delegation_limit` row.

This story grants or refuses a read and, for the resolve, the right to make one; it changes no item, no document, no field and no policy row. A policy row changes only through the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and a break-glass grant, its incident reference and its four-hour ceiling stay with the wave-1 stories of the access service.

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-0988; ASM-1736); the story refers to "the rwb-access login (DP-02)".

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read (the sign-in check, X6) |
| DF-REF-027 to DF-REF-033 | `lov_value` | LOV-SCOPE values, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` and `AC-DENY` entries: code, actor, area, right, item or document reference, actions, decided at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at; used by the policy listener | Write |

The document field IDs the answer marks are identifiers only, taken from the request and never from a query:

| Field ID | Name in the document hub | Use in this story |
|---|---|---|
| DF-DOC-015 | `document_field.field_value` | Identifier only; never read by SQL |
| DF-DOC-017 | `document_field.confirmed_by` | Identifier only; never read by SQL |
| DF-DOC-034 | `document_field.extracted_value` | Identifier only; never read by SQL |
| DF-DOC-080 | `document_intake.review_reason` | Identifier only; never read by SQL |
| DF-DOC-081 | `document_intake.review_outcome` | Identifier only; never read by SQL |

The field IDs the answer marks appear in `masking_rule.field_id` and in the answer as identifiers only. Which review-field IDs the masking pack of `MASK-SIT-01` must cover is Not specified in the source documents (GAP-0988; ASM-1740), so the story answers markers for whatever field IDs a request names and writes no roster in code. No field value, no extracted value and no OCR text enters `rwb_access`, the answer, the record or the event: masking markers are the whole payload (NFR-039, NFR-040). Field IDs are those in the Logical Data Model and Data Dictionary v9.

The item and document facts of a request — the item reference, its review reason, its predicted type, its candidates, its review team, its candidate cases, the stored document's case with its team, region and owner, and the field IDs in state `REVIEW` — are read from the request and never from a table: `document`, `document_intake`, `document_field`, `document_text` and `document_checklist_item` are P5's, `recovery_case` is P3's and the `v_ace_*` views are P1's, and no foreign key and no query crosses a schema (DP-01). Which attributes a request must carry is Not specified in the source documents (GAP-0988; ASM-1736).

### 12. Contract

#### 12.1 REST operations provided

None new in this story. The operations are those of the service contract already in force from wave 1 (RWB-P4-E1037-CON), on base `/api/recovery/access/v1`, owner rwb-access (P4), unchanged in path, request, response and error shape:

| Operation | Path | What this story decides behind it |
|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The Documents right, the scope of the item or the document, and the masked or clear marker per field ID for one request. Errors 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 503 (MSG-P7-003) |
| GET | `/api/recovery/access/v1/me/permissions` | The roles, the matrix version and the default scope of the caller, as the session resolved them |
| GET | `/api/recovery/access/v1/masking-policies` | The masking version in force and the fields it covers for the caller's roles |

`GET /doa-limits` is the same service's operation and is not used here: the delegation of authority table and its routing lookup are RWB-P4-E2013-APP's.

#### 12.2 REST operations consumed

None. The item and document facts arrive in the authorise request, built by `rwb-document` from its own rows; this story calls no service at run time. The shape it expects is the one RWB-P5-E1054-CON publishes, and that contract is used as a fake in the tests (12.8) and as the alignment reference in the build.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | policy kind and version | the policy kind (permission matrix, masking), the version label, the valid-from date and the change reference |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | item or document reference where there is one, else the actor reference | the hash-chained `AC-READ` or `AC-DENY` record |

CloudEvents 1.0 envelope. Neither payload carries a personal value: the `AC-READ` record carries identifiers, field IDs and markers, the `AC-DENY` record carries the area and the right only, and the policy event carries version labels. `rwb.access.DoALimitChanged.v1` belongs to the delegation slice and is not published here.

#### 12.4 Events consumed

None. A policy change is written and published by the same service, so the cache is dropped on the commit that publishes `AccessPolicyChanged` rather than on a consumed event; the topic exists for the other services' caches (Architecture v5 slide 43: all consume it for cache refresh).

#### 12.5 Workflows and activities

None. This story runs no Temporal workflow and registers no activity on `rwb-access`. The review queue has no workflow: an item is created by the document intake job of P5 (JOB-12) and resolved by a person through P5's operations (Architecture v5 slide 44; Temporal and Drools design).

#### 12.6 Schedules

None. The document intake job (JOB-12, every 15 minutes) and the retention job (JOB-17, monthly on the first Sunday) are `rwb-document`'s under Architecture v5 slide 44; this story starts no Schedule and reads no job row. The only Schedule of this service is the six-monthly access review list (JOB-18), which is RWB-P4-AD008-APP's.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's roles and their `default_scope` |
| `permission` | P4 (`rwb_access`) | The DOCUMENTS letters and the `matrix_version` in force |
| `masking_rule` | P4 (`rwb_access`) | The masked or clear marker per role, field and masking version |
| `role_conflict` | P4 (`rwb_access`) | The conflicting role pairs the sign-in check reads |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | LOV-SCOPE, read through the contract; not owned here |
| `delegation_limit` | P4 (`rwb_access`) | Not read in this story; it is the delegation slice's |

No table of `rwb_document`, `rwb_case`, `rwb_decision` or `rwb_source_data` is read: the item, the document, the fields, the OCR text, the candidates, the review outcome and the case stay with their owners, and the only facts of them that enter this service are identifiers carried by a request (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document review WireMock | RWB-P5-E1054-CON | Intake item "IN-0101" with review_reason LOW_CONFIDENCE, predicted type COURT_NOTICE at 0.6200, candidates COURT_NOTICE 0.6200 and DEMAND_LETTER 0.2100, review team LIT-BKK, no case and no candidate case, fields DF-DOC-015 and DF-DOC-034 in state REVIEW; intake item "IN-0110" in review team HP-NE; document "DOC-0103" on case RW-2026-000202 with review_status PENDING and field black_case_no in state REVIEW; the same document moved to a case of team HP-NE for AC3 |
| decision-record fake | RWB-PLT-E1027-CON | The `AC-READ` and `AC-DENY` write and the publish on `rwb.decision-record.v1`, including the forced failure of X5 |
| policy pack fixture | RWB-P4-E1037-CON | Matrix version PM-2026.12, masking version MASK-SIT-01, the later PM-2026.13 and MASK-SIT-02 for AC8, the earlier PM-2026.11 for the change history of AC8, and the roles, scopes and masking rows of the background |
| reference-data fake | RWB-P3-E1043-CON | LOV-SCOPE with the version in force, and the unavailable list of X8 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations of RWB-P4-E1037-CON implemented), consumed 0 | Base `/api/recovery/access/v1`; the item and document facts arrive in the request |
| Kafka | Published 1 service event and 1 decision record; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-access` |
| File | None | No file input or output; the item file and its OCR text are P5's and never reach this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/review-authority`, Java package `th.co.scb.ace.workbench.recovery.access.review`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is the reason the service answers from the attributes it is given: `document`, `document_intake`, `document_field`, `document_text` and `document_checklist_item` are P5's and `recovery_case` is P3's, so the answer is built from identifiers and never from a joined query, and the OCR text and the field values never enter the service. DP-03 is the access log: an `AC-READ` and an `AC-DENY` are decision records on `rwb.decision-record.v1`, so an access question and a review decision are answered from one log. DP-07 supplies LOV-SCOPE with the version in force, because `lov_value` stays with P3 under the ownership map; the review team of an unattached item is not a list value of this service either — it is `REVIEW_TEAM_UNATTACHED` of the document hub, carried by the request, so no scope string and no team string is a Java constant. DP-09 is the outbox: the only rows this story writes to a topic are the decision record and the policy-change event, both from the transaction that answers. DP-11 is the caller-facing boundary: one hop, 2 s timeout, cached, and the answer must hold inside it. DP-13 and DP-15 are the naming and migration conventions of the service. DP-19 is the route that renders the answer: SCR-31, its list, its reviewed state and its empty state are RWB-P5-E1054-APP's, and this story supplies only the grant, the refusal and the markers.

The platform contracts the DP rows name are preconditions of the service lane already in place behind RWB-P4-E1037-CON in wave 1; this secondary slice adds no new build dependency of its own (metadata H = None; ASM-1736), and the only contract it builds against is RWB-P5-E1054-CON, which never blocks.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | Controller | The three operations of the existing contract on `/api/recovery/access/v1`; validation and problem responses |
| ReviewAuthorityService | Service | Right, scope and masking profile for one review request, in that order; one answer, one record |
| PermissionResolver | Service | Reads `permission` for the caller's roles and the `matrix_version` in force; resolves the five letters |
| ScopeRule | Service | Compares the request attributes with the `default_scope` value in force |
| ReviewTeamRule | Service | The unattached-item branch of BR2: the caller's team against the review team the request carries |
| FieldMarkerService | Service | The masked or clear marker per field ID for the caller's roles and the masking version in force; default masked |
| AccessRecordWriter | Service | The `AC-READ` and `AC-DENY` entries through the library of DP-03, and the `AccessPolicyChanged` outbox row |
| PolicyCache | Service | The cached answer per matrix and masking version, dropped on the policy change |
| PolicyChangeListener | Service | Applies a new policy version and publishes `rwb.access.AccessPolicyChanged.v1` in the same transaction |
| AccessRepository | Repository | `role`, `permission`, `masking_rule`, `role_conflict`, inbox and outbox in `rwb_access`; no foreign table |

**Database and migrations**

- No new table: `role`, `permission`, `masking_rule` and `role_conflict` exist from the wave-1 stories of this service behind RWB-P4-E1037-CON, and the policy rows are loaded by the load path stories.
- One migration in the per-service Flyway sequence of DP-15: `V1054_1__review_authority_read_path.sql` adds `ix_masking_rule_role_field` on `masking_rule (role_code, field_id, masking_version)` and `ix_permission_role_area` on `permission (role_id, capability_area, matrix_version)`. These are the only two objects the migration creates, so the two reads of an answer are index reads inside the 2 s budget of DP-11. No index is created on an item, a document or a case, because no such table is read.
- The policy rows are versioned by `matrix_version`, `masking_version` and the roles' `valid_from` and `valid_to`; this story writes none of them, and a version is never edited in place (a new version is loaded, approved and published).

**Configuration and reference data**

- The matrix version and the masking version in force are data: the latest `valid_from` on or before the business date, read from `permission.matrix_version` and `masking_rule.masking_version`. The label of the matrix and masking versions in force at the release date of 30 November 2026 is Not specified in the source documents (GAP-0988; ASM-1737); the tests use `PM-2026.12` and `MASK-SIT-01` and the answer always names the version it used.
- LOV-SCOPE (OWN, TEAM, REGION, ALL) through the reference-data contract of DP-07 (RWB-P3-E1043-CON). No other list is read.
- `REVIEW_TEAM_UNATTACHED` is a parameter of `rwb-document`, not of this service: the story names its assumed value `DOC-SVC` and compares the caller's team with the value carried by the request. No copy of it is written here, and no parameter row is read (DP-01, DP-06 not applied).
- The roster of review-field IDs that the masking pack must cover is Not specified in the source documents (GAP-0988; ASM-1740); the pack is loaded by the load path stories with the masking rows, and this story marks whatever field IDs a request names.
- No timeout constant and no role code in code: the 2 s is the platform standard of RWB-PLT-E1037-CON's client, and the cache lives for the versions in force (BR9).
- The database login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0988; ASM-1736).

**Build steps**

1. `PermissionResolver` and `ScopeRule` over `permission`, `role` and the reference list, with the matrix version named in the answer; tests for AC3 and AC5, and a test that a new scope value is accepted as data.
2. `ReviewTeamRule` with the review team and the scope ALL alternative; tests for AC2 with the review team, with scope ALL and with another team.
3. The resolve branch of BR1: Documents U required for resolve, field correction and completion; tests for AC4 with RW-TEAMMGR and with RW-LITOFF.
4. `FieldMarkerService` with the covering-row lookup and the default; tests for AC1 and AC6.
5. `AccessRecordWriter` with the `AC-READ` and `AC-DENY` entries written before the answer, and the forced failure of X5; tests for AC1, AC7 and TC-E1-054-19.
6. `PolicyCache` and `PolicyChangeListener` with the publish and the drop; test AC8 against the PM-2026.13 and MASK-SIT-02 fixture.
7. The migration of the two indexes, and a timing test that one answer stays inside the 2 s budget on a policy pack of the loaded size, with a contract-fake run of the whole capability against RWB-P5-E1054-CON and the decision-record fake.

**Feature switch.** `rwb.p4.doc-review-authority`, read from the platform feature-flag library under the R-PREC default ruling. Off: the review-team branch of BR2 is not applied, so an unattached item is admitted only by scope ALL and by case scope, while the right check, the masking profile and the access log are unchanged — an item that no case covers stays out of every team's queue, and nothing else in the service changes. The switch needs no schema rollback and blocks no read that the policy allows.

**Done when.** The tests in section 16 pass; a review officer's read of an item is granted with the scope it used and markers on every field ID; an unattached item is admitted by the review team and by scope ALL and refused to another team; a stored document follows its case; a team manager holding Documents R is refused on resolve with no item fact; an item outside the scope is answered 404 with no fact; a field with no masking row comes back masked; a refusal leaves an `AC-DENY` entry with no item and no case; a failed record answers 503 and shows nothing; and an approved matrix or masking version changes the answer with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Recovery role, or no second factor | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. | The access check before this story's answer (X4, X7) |
| MSG-P4-002 | No role of the caller holds the right in the capability area, including a caller holding Documents R only who asks for U | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR1 |
| MSG-P4-003 | The item or the document is outside the caller's scope | This case is not in your scope. | This story, on the refusal of BR3 |
| MSG-P4-006 | Two roles of the caller conflict | {role} may not be held together with {role}. | The access check, from this service's `role_conflict` rows (X6) |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer (X5) |
| MSG-GEN-006 | The scope list the answer needs is not available | {system} is not available. Try again in a few minutes. | This story, on a reference-list failure (X8) |

For MSG-P4-002 the {action} value is the action the caller attempted, for example "resolve the item" or "correct the field"; for MSG-P4-003 no item fact, no candidate and no case number is echoed, because the message must not confirm that an item or a document exists. Every error is an RFC 9457 problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10 (open decision; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 confirmed by the directive), and MSG-P4-003 keeps its wording even where the object is a review item rather than a case, so the screen and the audit read one message.

### 15. Screens and states

This story builds no screen. SCR-31 Document review queue, its file and OCR text viewer, the type chooser with candidates, the case chooser, the fields with Confirm and Correct, the Attach and Discard actions and the reviewed and empty states are RWB-P5-E1054-APP/CON through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON). The route, the page and the copy of the "not in your scope" page are P5's; the refusal text it shows is the one this story produces.

What this story decides for SCR-31 is what each state may show:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-31 Document review queue | Loading | The skeleton rows load with no item fact; the first answer arrives inside the 2 s budget and names the scope and the versions it used |
| SCR-31 Document review queue | List | Only the items and documents this story grants are rendered; a row's reason, candidates and age come from P5, and a field the answer marks masked is rendered masked even where the OCR text shows the value |
| SCR-31 Document review queue | Reviewed | After a resolve the item leaves the list; the resolve itself was granted by the U answer and performed by P5, and the read that followed it writes its own `AC-READ` entry |
| SCR-31 Document review queue | Empty (common state) | An empty list may mean no item in the team's queue or no grant for the caller; the screen shows the same empty state, and one `AC-DENY` entry exists for every refusal that produced it |
| SCR-31 Document review queue | Error | Not specified in the source documents (CG-ALL-5071) |
| SCR-31 Document review queue | No access | Not specified in the source documents (CG-ALL-5071) |

A screen that renders a field clear because a client cached it is a defect of the screen, not of the answer: the answer always names the masking version it used, and a field is clear only where a row of that version says so. A screen that renders OCR text on the strength of a read grant is P5's defect and this story's control: the grant names the field IDs, never the text.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-054-18 | AC4, AC7, BR1, BR7 | Component | RW-TEAMMGR holding Documents R calls resolve on intake item IN-0101; refused 403 with MSG-P4-002 naming "resolve the item", one AC-DENY entry with no item fact |
| TC-E1-054-19 | AC7, BR8 | NFR | The decision-record write forced to fail during a granted read of IN-0101; 503 with MSG-P7-003, nothing shown, incident raised (the attach transaction and its DOCATT entry are RWB-P5-E1054-APP's) |
| TC-E1-054-01 | AC1, BR2 — owned by RWB-P5-E1054-APP (the queue list and its order) | Component | Intake item IN-0101 classified at 0.6200 with two candidates, team LIT-BKK; the access answer grants the read with scope TEAM |
| TC-E1-054-02 | AC2, BR6 — owned by RWB-P5-E1054-APP (the correction, the attach and the labeled example) | Component | Hearing date corrected on IN-0101; the access answer grants R on the item and U on the resolve |
| TC-E1-054-03 | AC3, BR5 — owned by RWB-P5-E1054-APP (the stored document with one field in review) | Component | Document DOC-0103 on case RW-2026-000202 with black_case_no in state REVIEW; the field ID comes back marked |
| TC-E1-054-04 | owned by RWB-P5-E1054-APP (an empty correction refused) | Component | Empty value on court_name; the 422 is P5's, this story granted U |
| TC-E1-054-05 | owned by RWB-P5-E1054-APP (a type not in the list refused) | Component | Type PAYSLIP not in force; the 422 is P5's |
| TC-E1-054-06 | owned by RWB-P5-E1054-APP (a date outside the range refused) | Component | Date 2569-12-16 entered as a Gregorian year; the 422 is P5's |
| TC-E1-054-07 | owned by RWB-P5-E1054-APP (attach with a field still in review) | Component | Two fields in REVIEW, one confirmed; the 422 is P5's |
| TC-E1-054-08 | owned by RWB-P5-E1054-APP (a closed case refused) | Component | Candidate case RW-2026-000150 with status Closed; the 422 is P5's |
| TC-E1-054-09 | owned by RWB-P5-E1054-APP (two sessions on one item version) | Component | Two sessions on item version 3; the 409 is P5's |
| TC-E1-054-10 | owned by RWB-P5-E1054-APP (a type change re-runs extraction) | Component | Demand letter changed to guarantor notice; the re-run is P5's and the next read names the new field IDs |
| TC-E1-054-11 | owned by RWB-P5-E1054-APP (the same file hash already on the case) | Component | File hash H109 already on case RW-2026-000203; the link is P5's |
| TC-E1-054-12 | owned by RWB-P5-E1054-APP (discard with a reason) | Component | Unreadable item discarded with a reason; the access answer granted U and the file stays in the intake container |
| TC-E1-054-13 | owned by RWB-P5-E1054-APP (discard with an empty reason) | Component | Empty reason on IN-0112; the 422 is P5's |
| TC-E1-054-14 | AC2, BR2 | Component | Five review items across teams LIT-BKK and HP-NE; the access answer admits the team's items and the ALL reader, and refuses another team |
| TC-E1-054-15 | AC2, AC5 — owned by RWB-P5-E1054-APP (the empty queue) | Component | No review item for team LIT-BKK; the empty state is P5's and the access answer refuses the other team's items |
| TC-E1-054-16 | AC5, BR3, BR5 | Component | Document DOC-0111 on a case of team HP-NE asked for by a caller of LIT-BKK; 404 with MSG-P4-003 and no fact |
| TC-E1-054-17 | owned by RWB-P5-E1054-APP (the same PATCH sent twice) | Component | The same field confirm sent twice; the idempotent answer is P5's, the U grant is this story's |
| TC-E1-054-20 | AC6, BR2 | Component | Item IN-0101 with no case and no candidate case; review team LIT-BKK named by the request admits a caller of LIT-BKK; a caller of HP-NE with default_scope TEAM is refused 404 with MSG-P4-003 and no fact |
| TC-E1-054-21 | AC8, BR5 | Component | Request names a field ID with no covering masking_rule row under MASK-SIT-01; the field comes back masked and no value, extracted value or OCR text is returned |
| TC-E1-054-22 | §12.1 to §12.3 (operations and events; no activity) | Contract | POST /authorise, GET /me/permissions and GET /masking-policies answer as in RWB-P4-E1037-CON; rwb.access.AccessPolicyChanged.v1 and rwb.decision.DecisionRecorded.v1 carry the CloudEvents 1.0 envelope |
| TC-E1-054-23 | §12.7 tables | Component | Boundary of the §12.7 tables: a request with an unknown reference reads only role, permission, masking_rule and role_conflict; no table of rwb_document, rwb_case, rwb_decision or rwb_source_data is read |
| TC-E1-054-24 | AC6, BR5 | Component | No MASK-SIT-01 row covers DF-DOC-015 for any role; RW-LITOFF on IN-0101 with DF-DOC-015 and DF-DOC-017; DF-DOC-015 marked masked with XXXX-XX-XX, DF-DOC-017 masked, one AC-READ entry names both |
| TC-E1-054-25 | AC8, BR9 | Component | RW-LITOFF asks twice under PM-2026.12 and MASK-SIT-01; second answer served from cache; PM-2026.13 and MASK-SIT-02 approved and AccessPolicyChanged published; next ask answered under both with no deployment |
| TC-E1-054-26 | AC9, BR4 | Component | Token with no Recovery role asks for IN-0101; 401 with MSG-P4-001 before any permission read, one AC-DENY entry with the reason |
| TC-E1-054-27 | AC10, BR4 | Component | Caller holding RW-SECADM with a business role signs in; session refused from role_conflict rows with MSG-P4-006; no authorise request made |
| TC-E1-054-28 | AC11, BR4 | Component | Service identity with no role asks for IN-0101; 401 with MSG-P4-001 |
| TC-E1-054-29 | AC12, BR2 | Component | LOV-SCOPE not available during a read of IN-0101 by RW-LITOFF; 503 with MSG-GEN-006, no scope guessed, refusal recorded |
| TC-E1-054-30 | AC13, BR5 | Component | New type set on IN-0101 and extraction run again; the next read answers with the new field IDs, each marked masked |
| TC-E1-054-31 | AC14, BR4 | Component | Token with no Recovery role, or no second factor, asks POST /authorise, GET /me/permissions and GET /masking-policies; each answered 401 with MSG-P4-001 before any permission read, one AC-DENY entry with the reason |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component where the document-side assertion is stubbed by RWB-P5-E1054-CON, the level Access of TC-E1-054-18 maps to Component, and the level Resilience of TC-E1-054-19 maps to NFR because it proves the record-before-the-answer rule under a forced failure rather than a functional path. Every legacy test case of the key is listed above in the legacy order, with the Covers column rewritten to the criteria this story owns or to the slice that owns it. No `-ITG` copy sits in this story: the integration copy of this key is RWB-ITG-E1054-ITG and proves the real cross-service behaviour end to end.

### 17. Guardrails

- No business value in code: role codes, the Documents letters, scope values, field IDs, the matrix version and the masking version are data rows in `rwb_access` and list values read through DP-07; `REVIEW_TEAM_UNATTACHED` and its value are P5's data carried in the request; the switch is a platform flag (BR1, BR2, BR5, BR9).
- No personal data in logs, events, the record or the tests: the answer carries markers, the `AC-READ` entry carries identifiers and field IDs, the `AC-DENY` entry carries the area and the right, and the policy event carries version labels; OCR text and extracted values never leave the document hub, and test data is synthetic and staff appear as user references.
- ACE customer fields and OCR text only through the owner's contract and masked by role: this service stores no customer value, no field value and no document text, and answers with markers (NFR-039, NFR-040; DP-01).
- No cross-schema read (DP-01): `document`, `document_intake`, `document_field`, `document_text`, `document_checklist_item`, `recovery_case`, `decision_log_entry` and the `v_ace_*` views are never queried; the item and document facts arrive in the request and the policy is the service's own.
- One writer for the policy: only the load path stories of this service write a role, a permission or a masking row; this story reads them and publishes the change, so an answer and the policy it names cannot disagree.
- The record is written before the answer: a failure answers 503 with nothing shown and raises an incident, so no read of a review item is unlogged (BR6, BR7, BR8).
- Default deny at every boundary: no role is 401, no right is 403, out of scope is 404, no masking row is masked, and no branch of the answer is reached without a version named.
- The answer is idempotent for a policy version: the same question under the same versions returns the same answer, and the cache is dropped on the policy event rather than on a timer.
- The feature switch changes one rule and no schema: off removes the review-team branch of the scope rule and leaves every other decision as it was.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Inbound documents are classified with a confidence, and anything below the threshold goes to a review queue | Business Requirements Program, section 5.5; Business Requirements Epic 1, section 3.5 | FEAT-DCM-10, FEAT-DCM-11, FEAT-ACA-04, FEAT-ACA-05 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40; legacy BR2, BR10 | TC-E1-054-01 to TC-E1-054-31 |
| REQ-DCM-019 | Records retention runs by class, and a document reaching the end of its retention period is disposed of or extended by a recorded decision, never silently | Business Requirements Program, section 5.5 and section 6.5; Business Requirements Epic 2 | FEAT-DCM-10, FEAT-ACA-07, FEAT-ACA-08 | 13 Manage documents and correspondence | R-UNI-39; legacy BR6, BR9 | TC-E1-054-12, TC-E1-054-19 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P5-E1054-CON | CON | The contract this story builds against: the intake item and document reads, the content read, the field IDs in `REVIEW`, the resolve, field and completion calls. It is the only dependency of this story (C) and it never blocks; its fake drives every test |
| RWB-P5-E1054-APP | APP | The document-side slice of the same legacy key: the queue endpoints, SCR-31 and its states, the intake rows, the documents, the fields, the review outcome, the labeled set, DocumentStore and the DOCATT entry, and the two jobs JOB-12 and JOB-17 |
| RWB-P3-E1054-APP | APP | The case side reached through P5: the case number lookup (`CaseDirectory.findByCaseNo`), the case status, the team, the region and the owner the scope rule compares. No call is made from here; the attributes arrive in the request |
| RWB-P7-E1054-APP | APP | The central ledger that collects the `AC-READ` and `AC-DENY` records from `rwb.decision-record.v1`; this story writes the local record and publishes, and seals nothing |
| RWB-P4-E1037-CON | CON | The service contract this story implements behind: `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on `/api/recovery/access/v1`, and the policy pack fixture |
| RWB-PLT-E1037-CON | CON | The platform authorise client and guard library of DP-08, and the 2 s timeout the callers of this answer use |
| RWB-ITG-E1054-ITG | ITG | The wave-1 integration harness copy of the tests of this key, which proves the real cross-service behaviour between the document hub and this answer |

| Legacy reference | Where it is kept |
|---|---|
| The scope rule of the queue, `BR2` (the review team of an unattached item, scope ALL, case scope, and the two teams of AC14) | Sections 1, 4, 7, 8, 10, 13 |
| The refusal of a role holding Documents R only on resolve (X12, access test TC-E1-054-18) | Sections 4, 5, 7, 8, 16 |
| The not-in-scope answer with no fact (X10, AC16) | Sections 4, 5, 7, 8, 14, 16 |
| Masking of field values and the default masked (`BR10`, DF-DOC-015, AC-EXC-P4-004-05) | Sections 3, 4, 7, 8, 11 |
| The record before the answer and the failed record (X13, TC-E1-054-19) | Sections 4, 5, 7, 8, 16, 17 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-006, MSG-P7-003, MSG-GEN-006 | Section 14, exception paths |
| Rules R-UNI-39, R-UNI-40 and controls CTL-09, CTL-11 | Sections 2, 8, 18 |
| Matrix version PM-2026.12, masking version MASK-SIT-01, roles RW-LITOFF, RW-CASEOWN, RW-TEAMMGR, RW-COE, RW-AUDIT, RW-COMPLY, RW-REFADM, SY-OCR | Background, AC1 to AC8, sections 3 and 10 |
| REVIEW_TEAM_UNATTACHED and its assumed value DOC-SVC | Sections 1, 3, 7, 13 |
| Legacy key RWB-E1-054, story RWB-P4-E1054-APP, contract RWB-P5-E1054-CON | Metadata, sections 3, 12, 18 |

### 19. Out of scope

- The `rwb-document` slice of this legacy key, RWB-P5-E1054-APP and its contract RWB-P5-E1054-CON: the queue endpoints `/review-items`, `/document-intake/{intakeId}`, the content read, the resolve call, the field update and `/documents/{documentId}/review`.
- SCR-31 Document review queue, its list, its reviewed and empty states, its file and OCR text viewer and its route through gateway-bff.
- The set of review reasons (`LOW_CONFIDENCE`, `UNKNOWN_TYPE`, `MODEL_UNAVAILABLE`, `RESCAN`, `UNREADABLE_FILE`, `EXTRACTION_FAILED`, `NO_MATCH`, `MULTIPLE`, `CONFLICT`, `CASE_CLOSED`) and the `REVIEW_*` parameters of the document hub.
- The extraction re-run on a type change, and the confidence thresholds and the type list in force.
- DocumentStore, the DOCATT decision log entry, the write-once container and the document itself.
- The labeled set and the model evaluations that read it (RWB-E1-060, RWB-P10-E1060-APP).
- The case number lookup and the case status, team, region and owner (RWB-P3-E1054-APP through CaseDirectory).
- The document intake job (JOB-12) and the retention job (JOB-17), both `rwb-document`'s.
- RWB-ITG-E1054-ITG, the wave-1 integration harness copy of the tests of this key, which proves the real cross-service behaviour end to end.
- Loading, approving and rolling back the policy pack: the reference-load and approval path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and the administration screens of Epic 8.
- The delegation of authority table and its lookup (RWB-P4-E2013-APP and RWB-P4-E2014-APP), the DoA-limits operation and `rwb.access.DoALimitChanged.v1`.
- Break-glass access, its incident reference, its ceiling and its review (the wave-1 stories of this service).
- The six-monthly access review list (JOB-18, RWB-P4-AD008-APP) and every other job, workflow and Schedule of this service.
- Assigning review work to named people by queue rules (RWB-E2-011) and the case checklist on the review screen (RWB-E1-040).
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
