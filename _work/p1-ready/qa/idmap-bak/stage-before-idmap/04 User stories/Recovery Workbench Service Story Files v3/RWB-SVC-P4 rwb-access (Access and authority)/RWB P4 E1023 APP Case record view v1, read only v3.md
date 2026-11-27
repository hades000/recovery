# RWB-P4-E1023-APP Case record view v1, read only

**Version 3 changes.**
- caseId is the case uuid; the case number is display data (RD-P1-023; finding RWB-P4-E1023-APP#1).
- The access record carries what the ledger intake needs; the story appends nothing itself; AC23 to AC25 added (RD-P1-001, RD-P1-007, RD-P1-008, RD-P1-009; findings #2, #6).
- Contact history is read from the case-scoped ledger path of rwb-source-data 5.1.0; Problem members and contract version corrected (RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-011; findings #4, #5, #7, #8).
- RD-P1-072 rules that a read is not a decision (NEW-GAP-F09-4 closed). Open: BR12 and AC24 still publish the access records as `DecisionRecorded`; the replacing access-log write is not ruled (finding #3; NEW-GAP-G6-1).
- Finishing pass: RD-P1-072 recorded with its open point (NEW-GAP-G6-1); test case IDs of Test Cases v9 and the Error and Message Standard v6 wording applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

**Version and date.** v3, 27 November 2026.

**Change log.** D-RCV-60, 27 November 2026: applied RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-008, RD-P1-009, RD-P1-011 and RD-P1-023 and fixed the cited affected-story review findings. D-RCV-60 P1 developer readiness (RD-P1 register). Agent: F09-affected.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1023-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P4-E1023-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP18, DP19 |
| Parallel lane | L-P4-T |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1023-CON, RWB-P4-E1037-CON |
| Contract version | RWB-P4-E1037-CON at rwb-access base /api/recovery/access/v1 (rwb-access.yaml 5.1.0 does not yet publish POST /authorise; GAP-0983). Contact history is read by the case service at rwb-source-data.yaml 5.1.0 |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-008, RD-P1-009, RD-P1-011, RD-P1-023, RD-P1-072 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-006, FR-P4-014, FR-P4-015, FR-P4-016, FR-P4-017, FR-P4-018, FR-P4-019, FR-P4-023, FR-P4-024, FR-P4-025, FR-P4-026, FR-P4-027) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-023 for rwb-access, the read authority and masking behind SCR-03 Case record. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E1023-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (27 resolved, 20 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-LITOFF, RW-CONDUCT or RW-AUDIT who opens the case record view**, I want **the access service to answer, for the case in front of me, whether my role may read the case record and each of its read sections, which scope admits the case, and which personal fields come back masked**, so that **the case record view shows the case, its accounts, its parties, its contact history and its documents to the people entitled to see them, and nothing about a case to anybody else**.

Inside `rwb-access` this is the access-side capability of legacy RWB-E1-023:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability answers three questions behind the three operations the service already publishes, `POST /authorise`, `GET /me/permissions` and `GET /masking-policies`: does the caller hold Case record right R, does the scope in force admit this case, and which of the personal fields asked about are answered as `masked`. No operation is added.
- The screen SCR-03, the five read endpoints `GET /cases/{caseId}`, `GET /cases/{caseId}/accounts`, `GET /cases/{caseId}/parties`, `GET /cases/{caseId}/documents`, the contact-history section (read by the case service from `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` of rwb-source-data), the ACE view reads, the contact-history merge and the documents section are RWB-P3-E1023-APP's, with the documents section answered by RWB-P5-E1023-APP; this story builds no screen, reads no ACE view and returns no case fact of its own.
- The case facts the decision needs — the case reference, its owner, its queue, its team and its region — arrive in the authorise request one hop, built by the case service from its own rows (DP-11). The contact-history rows come from rwb-source-data's ledger contract (DP-18). No personal value and no complete copy of a case enters this service, and no table of `rwb_case`, `rwb_document` or `rwb_source_data` is named by a statement of this story (DP-01, DP-05).
- The policy the answers come from is data in `rwb_access`: the role list, the role-to-permission matrix version in force (`PM-2026.12`), the scope rule and the masking rows (`MASK-SIT-01`). Loading and approving a policy pack is the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP and is out of scope here.
- The access log is a decision-record entry on `rwb.decision-record.v1`, written through the local library of DP-03: `AC-READ` for a granted read with the case ID and the field IDs with their masked markers, `AC-DENY` for a refusal with the area and the right and no case fact (FEAT-ACA-07, FEAT-ACA-08).
- The answer decides the read; it never carries a value. For each personal field ID the caller asks about, the answer says `masked` or `clear` under the masking version in force, and the identity number is never `clear`, because the ACE view exposes `id_no_masked` and `id_no_last4` only.

The legacy behaviour carried into the access service is unchanged: the same scope answers of RWB-E1-023 section 10 (Own, Team, Region and All for internal audit), the same "not in your scope" answer that confirms no case exists, the same refusal of a role with no Case record right, and the same masking of the personal fields and the same access-log entry of the legacy AC7 and AC8, whatever the screen.

### 2. Business rationale

A programme finding is that the case record view is the screen a case owner works in all day, and the controls behind it are thin: a case outside a person's scope is answered with a page that confirms the case exists, the personal fields are hidden by whichever section the reader happens to open, and a read that cannot be written to the access log shows the data anyway. CTL-09 records the scope exposure; NFR-039 and NFR-040 require party identifiers masked at rest and in use and data minimisation per screen; and the PDPA exposure of a case record read is the reason FEAT-ACA-07 and FEAT-ACA-08 exist. Under Architecture v5 the access decision is a cached answer of `rwb-access`, each service authorises its own object against it, and every service consumes `AccessPolicyChanged` to refresh its cache, with a 2 s timeout (slides 14 and 43).

This story supplies that answer for the case record view: the matrix right, the scope rule and the masking profile behind SCR-03, in the service that holds the roles, the permissions and the masking policy as data (Architecture v5 slide 41). It meets REQ-OCC-007, REQ-RDF-009, REQ-ACA-005, REQ-ACA-006 and REQ-ACA-009 on the access side, and supports the measure rule and limit changes made without a code release at 100 percent, because the matrix, the scope values, the masking rows and their versions are data. The measure of success is that every read of a case record is granted or refused by the policy in force, that an out-of-scope case is never confirmed to exist, and that every granted read leaves one `AC-READ` entry naming the field IDs and their masked markers.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1037-CON | The service contract of `rwb-access` already in force from wave 1: `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on base `/api/recovery/access/v1`, with the role-to-permission matrix, the scope values and the masking rows as data (legacy RWB-E1-037). This story implements the decision behind those operations for the case record view; it adds no operation. Contract version built against: 5.0.0 (rwb-access.yaml, Recovery Workbench API Specification v5) |
| RWB-P3-E1023-CON | The case-record contract of the case service: the five read endpoints of SCR-03, and the case facts an authorise request is built from — the case reference, its owner, its queue, its team and its region — as the P3 slice of this legacy key publishes them. The authorise request carries the case reference, the owner, the queue, the team, the region, the action the caller is about to take and the field IDs asked about, and nothing else (GAP-0989) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the answer |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract that carries LOV-SCOPE and LOV-CAPABILITY with the version in force (DP-07); `lov_value` stays P3's, and no scope or capability string is written in code |
| RWB-PLT-E1047-CON | The naming library behind the topic and event names of DP-14 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence in `rwb_access` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves the case record view (DP-19); the route itself is P3's story |
| rwb-case, rwb-source-data, rwb-document and rwb-access consumed operations | Placeholders with owners and fakes: the case-record read of rwb-case; the account, party and contact read and the contact-history read of rwb-source-data; the document-list read of rwb-document; and the authorise, mask and AC-READ accept of rwb-access as one consumed operation. Operation names are Not specified in the source documents (GAP-3081); each answer carries dataAsOf and a freshness per product, and each placeholder is confirmed with its owner before the tag |

Business preconditions carried from RWB-E1-023, owned by other services where they say so:

- Permission matrix version `PM-2026.12` is in force and gives CASE_RECORD right R to RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-LITOFF, RW-CONDUCT and RW-AUDIT, with default_scope OWN for RW-CASEOWN, TEAM for RW-TEAMMGR and ALL for RW-AUDIT. That this is the version in force on the release date of 30 November 2026 is Not specified in the source documents (GAP-0989; ASM-1739).
- Masking version `MASK-SIT-01` is in force and covers the three field IDs of this slice for the roles of the matrix; that this is the masking version in force on the release date is Not specified in the source documents (GAP-0989; ASM-1739).
- The roster of case-record personal field IDs is DF-PTY-007 `id_no_masked` over `v_ace_customer.id_no_masked`, DF-PTY-008 `date_of_birth` and DF-PTY-016 `contact_value_masked` over `v_ace_contact.contact_value_masked`; a wider roster of case-record field IDs is Not specified in the source documents (GAP-0989; ASM-1741), and the answer accepts any field ID as data and marks it masked when no row covers it.
- The legacy flows of RWB-E1-023 hold behind the case side: cases exist with account links and party links (RWB-E1-018), the document hub lists documents by case (RWB-E1-024), the interaction ledger reads back through `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` of rwb-source-data (`InteractionPage`; RD-P1-007) and the masking rules by role are in force (RWB-E1-037).
- The caller signed in through Entra ID with multi-factor authentication and holds at least one Recovery role; with no role the answer is 401 MSG-P4-001 (FSD P4 A2.1).
- The database login is the rwb-access login of the service baseline (DP-02), created with the schema behind RWB-P4-E1037-CON; the story never names the shared monolith login.
- The platform contracts the DP rows name are already in place behind RWB-P4-E1037-CON in wave 1. This secondary slice adds no new build dependency of its own (metadata H = None).
- The section timeout `caserecord.section.timeout.ms` and the six lists of values for this page are parameters and reference data of rwb-case: no value is copied into code, and the parameter row is confirmed with the P3 owner before the tag (GAP-3084). The release stays tentative and wave 1 stays as the business-epic map gives it (GAP-3084).
- This slice serves the page as a secondary serving: the deviation block and the assembly are its own, and the case header is consumed from RWB-P3-E1023-CON. The seven platform contracts behind the DP rows (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are build prerequisites with their fakes; the metadata row keeps H = None (GAP-3082).

### 4. Flow

1. Caller: a person opens SCR-03 Case record for a case from SCR-02 Case list. gateway-bff resolves the session and calls the case service; the case service builds the authorise request from its own rows.
2. Caller: the request carries the header `Idempotency-Key` (a new uuid for each read) and `caseId`, the uuid `rwb_case.recovery_case.id`, and names the area `CASE_RECORD`, the right `R`, the case reference (the case number, display data and part of the ledger business key only), the owner, the queue, the team, the region, the action the caller is about to take ("open the case record", "read the accounts", "read the parties", "read the contact history", "read the documents") and the field IDs the screen will show. The full attribute set is Not specified in the source documents (GAP-0989; ASM-1735).
3. `rwb-access`: resolves the caller's roles from the session the ACE common module resolved at sign-in, and the rights from `permission` for the matrix version in force, `PM-2026.12`. `role`, `permission`, `masking_rule`, `matrix_version` and `masking_version` are read from `rwb_access` only.
4. `rwb-access`, role check: a token that carries no Workbench role at all is refused before the policy is read, 401 with MSG-P4-001 (BR3).
5. `rwb-access`, right check: no CASE_RECORD R for any role the caller holds gives a refusal, 403 with MSG-P4-002 naming the action, and no case fact (BR1). The refusal is written as an `AC-DENY` entry (BR7).
6. `rwb-access`, scope check: the case is in scope when the attributes of the request satisfy the caller's `default_scope` in force, read from LOV-SCOPE through the reference-data contract of DP-07: OWN for the case the caller owns, TEAM for a case of the caller's team, REGION for a case of the caller's region, ALL for any case (internal audit) (BR2). A case outside the scope is answered 404 with MSG-P4-003 and no case fact, so the answer never confirms that a case exists (BR2).
7. `rwb-access`, masking: for each personal field ID the caller asks about, the marker is read from `masking_rule` by `field_id`, `role_code` and `masking_version` for the masking version in force, `MASK-SIT-01`. A field with no covering row is marked `masked` (BR4). The answer says `masked` or `clear` and never carries the value, masked or clear (BR4, BR5).
8. `rwb-access`: writes one `AC-READ` decision record through the library of DP-03, with the case uuid as `data.caseId` and the field IDs with their masked markers, with the event attributes `ce_idempotencykey` and `ce_actor` (BR12), and returns the answer to the caller inside the 2 s timeout of DP-11 (BR6). The story appends no interaction ledger entry itself.
9. `rwb-access`: caches the answer for the policy and masking versions in force. A caller that asks again under the same versions is answered from the cache and no matrix row is read twice; the `AC-READ` entry is still written for that read (BR9).
10. Policy change: a new matrix version or a new masking version is approved through the load path, `rwb-access` writes the rows, and publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`. Every cached answer is dropped and the next call is answered under the new versions, with no deployment (BR9).
11. Case service: renders SCR-03 with the granted fields and the masked markers, or the "not in your scope" page for a 404 and the refusal page for a 403; the accounts, the parties, the contact history and the documents are its own and P5's (RWB-P3-E1023-APP, RWB-P5-E1023-APP).

Every answer, granted or refused, is written before it is returned; when the record cannot be written nothing is returned, the call answers 503 with MSG-P7-003 and an incident is raised, so no read of a case record is ever unlogged (BR6, BR7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case is outside the caller's scope | Not found: 404 with no case fact; one `AC-DENY` entry with the area and the right and no case fact | MSG-P4-003 | AC3 |
| X2 | No role of the caller holds Case record R | Refused before any case fact is read: 403 with the action named, no case fact | MSG-P4-002 | AC6, AC7 |
| X3 | The token carries no Recovery role, or no second factor | No answer is given: 401 before the policy is read; one refusal entry with the reason | MSG-P4-001 | BR3, AC10, AC16 |
| X4 | No masking rule covers a personal field | The field is marked `masked` with the default marker; the read is otherwise granted | None | AC5 |
| X5 | The caller asks for the identity number in clear | The answer marks it `masked`, because the ACE view exposes `id_no_masked` and `id_no_last4` only | None | BR5, AC11, AC17 |
| X6 | Two roles of the caller conflict (for example RW-SECADM with a business role) | The sign-in access check refuses the session from the `role_conflict` rows this service holds; no authorise request is made | MSG-P4-006 | BR10, AC12, AC18 |
| X7 | The decision record cannot be written | Nothing is returned: 503 with no personal field and no case fact, and an incident is raised to the platform administrator queue | MSG-P7-003 | AC8 |
| X8 | The reference list of scope or capability is not available | No answer is given rather than a guessed one: 503; the refusal is recorded | MSG-GEN-006 | BR10, AC13, AC19 |
| X9 | The caller is an agent or a service identity, not a person | The same checks run under the service identity's roles; a service identity with no role is refused 401 | MSG-P4-001 | BR3, AC14, AC20 |
| X10 | `caseId` is missing or is not a uuid | 400 before the policy is read; no AC-READ and no case fact | MSG-GEN-001 | AC23 |
| X11 | `Idempotency-Key` missing or not a uuid; the same key with another request or in flight; the idempotency store unavailable | 400; 409; 503; nothing is decided | MSG-PLT-N009-03; MSG-PLT-N009-05; MSG-PLT-N009-06 | AC25 |

A day that carries two masking versions in force is not specified in the source documents (GAP-0989; ASM-1739); until it is, the version whose `valid_from` is the latest on or before the business date is used, and the answer names the version it used.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against RWB-P3-E1023-CON and the contract fake of the case facts; reads its own schema only and calls no other service at run time |
| Negotiable | The policy pack — roles, permissions, scope values, masking rows and their versions — is data; the story fixes the shape of the answer and the refusal behaviour only |
| Valuable | The right people see the case and its sections; nobody else is told the case exists; the personal fields are masked by role everywhere |
| Estimable | Three answers behind existing operations, one cache, one decision-record path and two indexes |
| Small | Fits one sprint with its tests; no screen, no endpoint and no workflow |
| Testable | Every owned criterion has a test case in section 16; the case side is a published fake |

### 7. Acceptance criteria

```gherkin
Feature: Case record view v1, read only

  Background:
    Given the environment is SIT
    Given every request carries a new uuid Idempotency-Key and the case uuid as caseId; the case numbers are display data: RW-2026-000701 = 00000000-0000-4000-8000-000000000701, RW-2026-000702 = 00000000-0000-4000-8000-000000000702, RW-2026-000703 = 00000000-0000-4000-8000-000000000703
    Given the service answers on base path "/api/recovery/access/v1" and reads schema "rwb_access" only
    Given permission matrix version "PM-2026.12" is in force and gives CASE_RECORD right "R" to RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-LITOFF, RW-CONDUCT and RW-AUDIT, and no CASE_RECORD right to RW-REFADM and RW-SECADM
    Given the default scope in force is "OWN" for RW-CASEOWN, "TEAM" for RW-TEAMMGR and "ALL" for RW-AUDIT, and the scope values in force are "OWN", "TEAM", "REGION" and "ALL"
    Given masking version "MASK-SIT-01" is in force and holds unmasked "false" for DF-PTY-007, DF-PTY-008 and DF-PTY-016 for RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-LITOFF, RW-CONDUCT and RW-AUDIT
    Given the rwb-case contract mock returns case "RW-2026-000701" with product "HIRE_PURCHASE", 2 accounts, queue "TDR-BKK-CO", owner "U-81", team "TDR-BKK" and status "IN_PROGRESS"
    Given the rwb-case contract mock returns case "RW-2026-000702" in team "LIT-BKK" owned by another user

  Scenario: AC1 An owner's read is granted and answered with the field markers (new, D-RCV-60)
    Given test user "U-81" holds RW-CASEOWN with default scope "OWN" and owns case "RW-2026-000701"
    When "U-81" asks POST /api/recovery/access/v1/authorise for case "RW-2026-000701", area "CASE_RECORD", right "R", action "open the case record" and field IDs DF-PTY-007, DF-PTY-008 and DF-PTY-016
    Then the answer is granted with scope "OWN" under matrix version "PM-2026.12"
    Then the answer marks DF-PTY-007, DF-PTY-008 and DF-PTY-016 "masked" under masking version "MASK-SIT-01"
    Then the answer carries no personal value, only the three markers
    Then one AC-READ decision record is written with the case ID and the three field IDs with their masked markers

  Scenario: AC2 Team scope admits a case of the caller's team (new, D-RCV-60)
    Given a test user holds RW-TEAMMGR with default scope "TEAM" in team "TDR-BKK"
    Given the rwb-case contract mock returns case "RW-2026-000701" in team "TDR-BKK" owned by "U-81"
    When the caller asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and action "open the case record"
    Then the answer is granted with scope "TEAM"
    Then when a caller with default scope "TEAM" in team "LIT-BKK" asks for the same case
    Then the answer is refused with status 404 and message MSG-P4-003

  Scenario: AC3 A case outside the scope is not found (new, D-RCV-60)
    Given test user "U-81" holds RW-CASEOWN with default scope "OWN"
    Given the rwb-case contract mock returns case "RW-2026-000702" in team "LIT-BKK" owned by another user
    When "U-81" asks for case "RW-2026-000702", area "CASE_RECORD", right "R" and action "read the accounts"
    Then the answer is refused with status 404 and message MSG-P4-003
    Then the answer carries no case fact: no owner, no team, no queue, no status and no field marker

  Scenario: AC4 Internal audit reads any case and still receives masked fields (new, D-RCV-60)
    Given a test user holds RW-AUDIT with default scope "ALL"
    Given the rwb-case contract mock returns case "RW-2026-000702" in team "LIT-BKK" owned by another user
    When the caller asks for case "RW-2026-000702", area "CASE_RECORD", right "R" and field IDs DF-PTY-007, DF-PTY-008 and DF-PTY-016
    Then the answer is granted with scope "ALL"
    Then the three field IDs are still marked "masked" under masking version "MASK-SIT-01"
    Then the answer names the masking version it used and carries no personal value

  Scenario: AC5 A field with no masking row is masked (new, D-RCV-60)
    Given no masking rule in "MASK-SIT-01" covers DF-PTY-008 for any role
    Given test user "U-81" holds RW-CASEOWN and owns case "RW-2026-000701"
    When "U-81" asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and field IDs DF-PTY-008 and DF-PTY-016
    Then the answer marks DF-PTY-008 "masked" with the default marker "XXXX-XX-XX"
    Then the answer marks DF-PTY-016 "masked"
    Then the read is otherwise granted and one AC-READ entry names both field IDs as "masked"

  Scenario: AC6 A role without Case record R is refused (new, D-RCV-60)
    Given a test user holds RW-REFADM, which has no CASE_RECORD right in "PM-2026.12"
    When the caller asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and action "read the parties"
    Then the answer is refused with status 403 and message MSG-P4-002 with action "read the parties"
    Then no field marker and no case fact is returned

  Scenario: AC7 A refusal is recorded with no case fact (new, D-RCV-60)
    Given a test user holds RW-REFADM, which has no CASE_RECORD right in "PM-2026.12"
    When the caller asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and the answer is refused
    Then one AC-DENY decision record is written with area "CASE_RECORD", right "R" and result "REFUSED"
    Then the record and the answer carry no case ID, no owner, no team and no field marker

  Scenario: AC8 A record that cannot be written answers 503 with no personal field (new, D-RCV-60)
    Given test user "U-81" holds RW-CASEOWN and owns case "RW-2026-000701"
    Given the decision-record writer rejects every write
    When "U-81" asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and field IDs DF-PTY-007 and DF-PTY-016
    Then the answer is status 503 with message MSG-P7-003
    Then no personal field and no field marker is returned, and no case fact is shown
    Then an incident is raised to the platform administrator queue

  Scenario: AC9 A policy and masking version change reaches the answer with no deployment (new, D-RCV-60)
    Given the matrix version in force before the change is "PM-2026.11" and test user "U-81" holds RW-CASEOWN and owns case "RW-2026-000701"
    When "U-81" asks for case "RW-2026-000701" twice inside one policy version
    Then the second answer is served from the cached decision without a second read of the permission matrix
    Then each answer is returned inside the 2 s budget and each granted read writes its own AC-READ entry
    Then when matrix version "PM-2026.12" and masking version "MASK-SIT-02" are approved and rwb.access.AccessPolicyChanged.v1 is published for them
    Then the next ask is answered under matrix version "PM-2026.12" and masking version "MASK-SIT-02" with no deployment
    Then a field with no row in "MASK-SIT-02" comes back "masked"

  Scenario: AC10 A token with no Recovery role or no second factor is refused before the policy is read (new, D-RCV-60)
    Given a test user holds a token with no Recovery role or no second factor
    When the caller asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and action "open the case record"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then the permission matrix is not read for the request
    Then one refusal entry with the reason is written

  Scenario: AC11 The identity number is never clear (new, D-RCV-60)
    Given test user "U-81" holds RW-CASEOWN and owns case "RW-2026-000701"
    When "U-81" asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and asks for the identity number DF-PTY-007 in clear
    Then the answer marks DF-PTY-007 "masked" under masking version "MASK-SIT-01"
    Then the answer carries no identity number value and no clear state

  Scenario: AC12 A conflicting role pair refuses the session (new, D-RCV-60)
    Given a test user holds RW-SECADM together with a business role that conflicts with it in the role_conflict rows of this service
    When the user signs in to the Workbench
    Then the sign-in access check refuses the session with message MSG-P4-006
    Then no authorise request is made for the session

  Scenario: AC13 A reference list that is not available answers 503 and guesses nothing (new, D-RCV-60)
    Given the reference list of scope or capability is not available
    Given test user "U-81" holds RW-CASEOWN and owns case "RW-2026-000701"
    When "U-81" asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and field ID DF-PTY-007
    Then the answer is status 503 with message MSG-GEN-006
    Then no scope or capability is guessed and the refusal is recorded as one AC-DENY decision record

  Scenario: AC14 An agent or service identity is checked under its own roles (new, D-RCV-60)
    Given a service identity holds no Workbench role
    When the service identity asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and action "open the case record"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then the same checks run under the service identity's roles

  Scenario: AC15 The case facts arrive in the request and no table of another schema is read (new, D-RCV-60)
    Given test user "U-81" holds RW-CASEOWN and owns case "RW-2026-000701"
    When "U-81" asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and the request carries the case facts of the case
    Then the service reads no table of recovery_case, case_account, case_party, interaction, document or queue
    Then the answer and the decision record carry no personal value and no complete copy of the case

  Scenario: AC16 A token with no second factor is refused before the policy is read (new, D-RCV-60)
    Given a test user holds a token with a Recovery role and no second factor
    When the caller asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and action "open the case record"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then the permission matrix is not read for the request and no case fact or field marker is returned
    Then one refusal entry with the reason is written

  Scenario: AC17 An identity number asked in clear is marked and read from the masked columns only (new, D-RCV-60)
    Given test user "U-81" holds RW-CASEOWN and owns case "RW-2026-000701"
    When "U-81" asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and asks for the identity number DF-PTY-007 in clear
    Then the answer marks DF-PTY-007 "masked" and carries no identity number value
    Then the read takes its identity values from "id_no_masked" and "id_no_last4" of the ACE view only

  Scenario: AC18 A conflicting role pair is refused from the role_conflict rows (new, D-RCV-60)
    Given a test user holds RW-SECADM together with a business role that conflicts with it in the role_conflict rows of this service
    When the user signs in to the Workbench
    Then the sign-in access check reads the conflict from the role_conflict rows and refuses the session with message MSG-P4-006
    Then no role pair is written in code and no authorise request is made for the session

  Scenario: AC19 A reference list that is not available records the refusal and reads no scope (new, D-RCV-60)
    Given the reference list of scope or capability is not available
    Given test user "U-81" holds RW-CASEOWN and owns case "RW-2026-000701"
    When "U-81" asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and field ID DF-PTY-007
    Then the answer is status 503 with message MSG-GEN-006 and no scope or capability is guessed
    Then the refusal is recorded as one AC-DENY decision record and no AC-READ decision record is written

  Scenario: AC20 A service identity is checked under the roles it holds (new, D-RCV-60)
    Given a service identity holds RW-REFADM, which has no CASE_RECORD right in "PM-2026.12"
    When the service identity asks for case "RW-2026-000701", area "CASE_RECORD", right "R" and action "read the parties"
    Then the answer is refused with status 403 and message MSG-P4-002 with action "read the parties"
    Then the refusal is recorded as one AC-DENY decision record with area "CASE_RECORD" and right "R"

  Scenario: AC21 The architecture rules hold in the code and at the boundary (new, D-RCV-60)
    Given the rwb-access build is under code review and boundary test
    When the review checks the source for role codes, scope names, capability areas, field IDs and version strings, and the boundary test reads the schema and the policy event
    Then no such value is written in code and the policy pack is loaded from "rwb_access" and the reference lists
    Then no table of recovery_case, case_account, case_party, interaction, document or queue is read, a session with no Recovery role is refused before the policy is read, and a cached answer is dropped when AccessPolicyChanged arrives

  Scenario: AC22 Every provided operation answers 401 without a valid token (new, D-RCV-60)
    Given the provided operations are served on base path "/api/recovery/access/v1"
    When a request arrives to a provided operation with no valid token
    Then the answer is status 401 with message MSG-P4-001
    Then no case fact and no field marker is returned

  Scenario: AC23 A case number or a missing caseId is refused (new, RD-P1-023)
    Given test user "U-81" holds RW-CASEOWN
    When "U-81" asks POST /api/recovery/access/v1/authorise with caseId "RW-2026-000701", or with no caseId
    Then the answer is 400 application/problem+json with messageCode MSG-GEN-001, field naming caseId and a traceId
    Then no AC-READ decision record, no AC-DENY decision record and no outbox row are written

  Scenario: AC24 The access record carries the attributes the ledger intake needs (new, RD-P1-009)
    Given test user "U-81" holds RW-CASEOWN and owns case "00000000-0000-4000-8000-000000000701" with case number "RW-2026-000701"
    When "U-81" is granted a case-record read
    Then one record of type rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 with data.caseId "00000000-0000-4000-8000-000000000701"
    Then ce_actor is "USER:U-81"
    Then ce_idempotencykey has the form EV-08-RW-2026-000701-<yyyyMMdd>-<actionId>, where actionId is the uuid of this decision record, and is at most 120 characters
    Then rwb-access sends no POST to the interaction ledger of rwb-source-data

  Scenario: AC25 A replay writes no second record (new, RD-P1-001)
    Given "U-81" was granted a read with Idempotency-Key "11111111-1111-4111-8111-111111111111"
    When the identical request is sent again with the same key within 24 hours
    Then the stored status and body are replayed and no second AC-READ record and no second outbox row exist
    When the same key is sent with another caseId
    Then the answer is 409 with messageCode MSG-PLT-N009-05
    When a request has no Idempotency-Key
    Then the answer is 400 with messageCode MSG-PLT-N009-03 and nothing is decided
    When the idempotency store is unavailable
    Then the answer is 503 with messageCode MSG-PLT-N009-06
```

AC1 to AC25 are the criteria this story owns; the case-side criteria AC1 to AC10 of the legacy key are owned by RWB-P3-E1023-APP/CON and are proved against the answers of this story. In AC1 the three assertions that belong to this service are the scope it names, the masked markers and the one record; the accounts, the parties and the documents themselves are P3's and P5's. In AC2 the same case is granted to a manager of its team and refused to a manager of another team, which proves that scope is read per role and per team and not per case. In AC3 the 404 is the legacy AC5 and AC-EXC-P4-004-01, and the assertion that no case fact is echoed is the reason the answer never confirms that a case exists. In AC4 scope ALL widens the scope and changes no masking row. In AC5 the default is masked when no row covers the field, which is the exception path AC-EXC-P4-004-05 of the FSD and the legacy AC8 case. In AC6 and AC7 the refusal is proved twice: as the answer the caller gets, and as the entry the audit reads. In AC8 the read is proved to be all or nothing. In AC9 the cached answer is proved to change on the policy event and to need no deployment. AC10 and AC14 prove BR3, AC12 and AC13 prove BR10, AC15 proves BR8 and AC9 proves BR9.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The right comes from the permission matrix version in force; a caller whose roles hold no Case record R is refused with 403 MSG-P4-002 naming the action, and no case fact | FSD P4 A2.4 VR-P4-004-1; TSD P4 T6.1; FEAT-ACA-04 |
| BR2 | A case is in scope when the attributes the request carries satisfy the caller's `default_scope` in force: OWN for the case the caller owns, TEAM for a case of the caller's team, REGION for a case of the caller's region, ALL for any case; a case outside it is answered 404 with MSG-P4-003 and no case fact | FSD P4 A2.14 VR-P4-014-1; LOV-SCOPE; legacy AC5, AC-EXC-P4-004-01; REQ-ACA-009; CTL-09 |
| BR3 | A token that carries no Workbench role is refused with 401 MSG-P4-001 before the policy is read | FSD P4 A2.1; legacy AC-EXC-P4-001-01 |
| BR4 | A personal field is marked `masked` unless a `masking_rule` row for a role the caller holds and that field says unmasked true for the masking version in force; with no covering row the field is masked | FSD P4 A2.5; AC-EXC-P4-004-05; NFR-039; NFR-040; legacy AC8 |
| BR5 | The identity number is never clear: the ACE view exposes `id_no_masked` and `id_no_last4` only, and the answer carries a marker, never a value | Legacy RWB-E1-023 BR3; DF-ACE-073, DF-ACE-074; NFR-039 |
| BR6 | Every granted case-record read writes one `AC-READ` decision record with the case ID and the field IDs with their masked markers, before the answer is returned; a read whose record cannot be written answers 503 with MSG-P7-003 and shows no personal field | FSD P4 A2.7 AC-P4-007-01, AC-EXC-P4-007-03; FEAT-ACA-07, FEAT-ACA-08; legacy AC7; REQ-ACA-006 |
| BR7 | Every refusal writes one `AC-DENY` decision record with the area and the right, and the answer carries no case fact | FSD P4 A2.7 AC-EXC-P4-007-04; FEAT-ACA-07 |
| BR8 | The case facts a decision reads arrive in the request one hop, and the contact-history rows come from the ledger contract of rwb-source-data; no personal value and no complete copy of a case enters this service | DP-01, DP-05, DP-11, DP-18; ownership map (interaction to P1; case and document to P3 and P5) |
| BR9 | An answer is cached for the policy and masking versions in force and dropped when `AccessPolicyChanged` arrives, so a policy change takes effect with no deployment | Architecture v5 slide 43; FSD P4 AC-P4-004-01; DP-11 |
| BR10 | Role codes, scope values, capability areas, field IDs, matrix versions and masking versions are data read from `rwb_access` and the reference lists; no business value is written in code, and a conflicting role pair refuses the session | FSD P4 BR-P4-004, BR-P4-005; TSD P4 T3.2; principle 1 |
| BR11 | `caseId` is the case uuid; the case number is display data and is used only inside the opaque ledger business key | RD-P1-023 |
| BR12 | Each AC-READ and AC-DENY record is published as `rwb.decision.DecisionRecorded.v1` with `ce_actor` and `ce_idempotencykey` (`EV-08-<caseNo>-<yyyyMMdd>-<actionId>` where there is a case, `actionId` the decision record's uuid), through the decision-record library; `data.caseId` is the case uuid where there is one. rwb-access appends no ledger entry itself | RD-P1-007 rules 4 and 6; RD-P1-008; RD-P1-009 |
| BR13 | `POST /authorise` requires `Idempotency-Key`; a replay returns the stored status and body for 24 hours and writes no second record; refusals are `application/problem+json` with `messageCode` and `traceId` | RD-P1-001 rules 1 to 5; RD-P1-004 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` for the caller's roles and the `matrix_version` in force; the letters C, R, U, D and A are held as the five-character field of TSD P4 T3.1, and the answer names the version it used.
- BR2 is the scope rule of `ScopeRule`, comparing the attributes of the request with the `default_scope` value read through DP-07; the scope names OWN, TEAM, REGION and ALL are list values, never Java constants, and the attribute names of a request are Not specified in the source documents (GAP-0989; ASM-1735).
- BR3 is the guard in front of the answer: a session with no Recovery role never reaches the policy, so a caller with no role cannot tell an existing case from a missing one.
- BR4 is a read of `masking_rule` by `field_id`, `role_code` and `masking_version`; the answer carries markers, never values, so no personal data crosses the boundary in either direction (NFR-039).
- BR5 is the reason the identity number has no `clear` state in any answer: the only identity columns the ACE view exposes are `id_no_masked` and `id_no_last4`.
- BR6 and BR7 are the same `RecordAndApply` transaction as the answer: the record is written first, the answer is returned after it commits, and a failure answers 503 with MSG-P7-003 and changes nothing (X7).
- BR8 is the reason there is no repository for a case, an account, a party, an interaction or a document: the request carries identifiers and facts, and the ledger rows are read by the case service through P1's contract.
- BR9 is a cache keyed by the matrix and masking versions in force; the `AccessPolicyChanged` entry that drops it is published by the same transaction that writes the new policy rows.
- BR10 is visible in the code review: no role code, scope name, capability area, field ID or version string appears in a constant, and the policy pack is loaded by the stories of the load path.

### 9. State transitions

None for a case. This story changes no case status, no stage, no queue and no timer: the case, its accounts, its parties, its contact history and its documents are P3's and P5's, and the deviation flag on the case record view is RWB-S8-E1023-APP's. This story runs no workflow of its own and owns no Schedule.

The only states this story has are the states of its answer and of its record, which it does not persist beyond the record:

| Answer state | When | What the caller gets | Record written |
|---|---|---|---|
| Granted | The caller holds Case record R and the case is in scope by the scope rule | The granted answer with the scope it used, the matrix version and the masking version, and the `masked` or `clear` marker of each field ID asked about | `AC-READ` |
| Refused, no right | No role of the caller holds Case record R | 403 MSG-P4-002 naming the action, no case fact | `AC-DENY` |
| Not found | The caller holds the right and the case is outside the scope | 404 MSG-P4-003, no case fact | `AC-DENY` |
| Not answered | The record cannot be written, or the policy or a reference list cannot be read | 503, no case fact and no personal field | None; the failure is raised as an incident |

The answer has no stored state beyond the record and the cache: the scope is recomputed from the request on every call, so a case that moves queue or owner changes its answer on the next call with no message between the services.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Asks for a case it owns, with default scope OWN; the personal fields are answered with their markers, and the identity number is never clear |
| RW-TEAMMGR, team manager | Asks for a case of its team, with default scope TEAM |
| RW-PHONECOL, RW-FIELDCOL, collectors | Ask for a case in the scope their role row carries, read only, with the personal fields masked (legacy AC8; FSD P4 A2.11) |
| RW-LITOFF, litigation officer | Asks for a case in the scope its role row carries, read only |
| RW-CONDUCT, conduct and QA officer | Asks for a case in the scope its role row carries, read only |
| RW-AUDIT, internal audit | Asks for any case with default scope ALL; the personal fields stay masked |
| RW-COMPLY, Compliance and PDPA officer | Reads which masking version is in force and which fields it covers, through `GET /masking-policies`; this story writes no value on their behalf |
| RW-REFADM, reference data administrator | Holds no Case record right: refused with 403 MSG-P4-002 and no case fact |
| RW-SECADM, security administrator | Holds no Case record right: refused on a read; approves the matrix and masking versions through the load path stories, which this story reads and publishes |
| SY-CASEWF and the other service identities | Ask the same question for their own service; a service identity with no role is refused 401 MSG-P4-001 |

Reading is the whole of this story: it grants or refuses a read and writes the record of it. It changes no case, no account, no party, no interaction, no document and no policy row; a policy row changes only through the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and a break-glass grant, its incident reference and its four-hour ceiling stay with RWB-P4-E1039-APP. No DoA level applies to a read: the delegation of authority table answers approvals, not reads, and `GET /doa-limits` is not called here.

The database login is per service (DP-02): "the rwb-access login (DP-02)", created with `rwb_access` by the service baseline behind RWB-P4-E1037-CON, and never the shared monolith login.

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read (the sign-in check, X6) |
| DF-REF-027 to DF-REF-033 | `lov_value` | LOV-SCOPE and LOV-CAPABILITY values, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` and `AC-DENY` entries: code, actor, area, right, case ID, actions, decided at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at; used by the policy listener | Write |

The field IDs the answer marks — DF-PTY-007 `id_no_masked` over `v_ace_customer.id_no_masked`, DF-PTY-008 `date_of_birth` and DF-PTY-016 `contact_value_masked` over `v_ace_contact.contact_value_masked` — appear in `masking_rule.field_id` and in the answer as identifiers only. No personal value enters `rwb_access`, the answer, the record or the event: the markers are the whole payload (NFR-039, NFR-040). A wider roster of case-record field IDs is Not specified in the source documents (GAP-0989; ASM-1741); the answer accepts any field ID as data and marks it masked when no row covers it. Field IDs are those in the Logical Data Model and Data Dictionary v9. The criteria and the test data of this story read no `v_ace_*` view; the view columns named above identify the field IDs only, and the values belong to P1.

The case facts of a request — the case reference, its owner, its queue, its team and its region — and the field IDs asked about are read from the request and never from a table: `recovery_case`, `case_account`, `case_party`, `interaction`, `document` and `queue` are P3's and P1's, the `v_ace_*` views are P1's, and no foreign key and no query crosses a schema (DP-01, DP-05, DP-18). Which attributes a request must carry is Not specified in the source documents (GAP-0989; ASM-1735). No SQL statement of this story names `recovery_case`, `case_account`, `case_party`, `interaction`, `document`, `queue` or any `v_ace_*` view.

### 12. Contract

#### 12.1 REST operations provided

None new in this story. The operations are those of the service contract already in force from wave 1 (RWB-P4-E1037-CON), on base `/api/recovery/access/v1`, owner rwb-access (P4), unchanged in path, request, response and error shape:

| Operation | Path | What this story decides behind it |
|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The right, the scope and the masking markers for one area, right, case uuid and field list, with the action named; header `Idempotency-Key` required. Errors, as `application/problem+json` with `messageCode`: 400 (MSG-GEN-001, MSG-PLT-N009-03), 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 409 (MSG-PLT-N009-05), 503 (MSG-P7-003, MSG-GEN-006, MSG-PLT-N009-06) |
| GET | `/api/recovery/access/v1/me/permissions` | The roles, the matrix version and the scope of the caller, as the session resolved them |
| GET | `/api/recovery/access/v1/masking-policies` | The masking version in force and the fields it covers for the caller's roles |

`GET /doa-limits` is the same service's operation and is not used here: the delegation of authority table and its routing lookup are RWB-P4-E1038-APP's and RWB-P4-E2013-APP's.

#### 12.2 REST operations consumed

None. The case facts arrive in the authorise request, built by the caller from its own rows, and the contact-history rows are read by the caller from `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` of rwb-source-data (`InteractionPage`, rwb-source-data.yaml 5.1.0); this story calls no service at run time and appends no ledger entry. The shape it expects is the one RWB-P3-E1023-CON publishes, and that contract is used as a fake in the tests (12.8) and as the alignment reference in the build.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | policy kind and version | the policy kind (permission matrix, masking, roles), the version label, the valid-from date and the change reference |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | caseId where there is one, else the actor reference | the hash-chained `AC-READ` or `AC-DENY` record |

CloudEvents 1.0 envelope. The decision record carries `ce_actor` and `ce_idempotencykey` and, where there is a case, `data.caseId` (uuid) (BR12). rwb-source-data consumes the topic and appends a `DECISION_TAKEN` ledger entry for every record that carries `data.caseId` (RD-P1-009 row 06); RD-P1-072 rules that a read is not a decision: a case-record read is written to the access log only and publishes no `DecisionRecorded`, so it never becomes a `DECISION_TAKEN` entry (NEW-GAP-F09-4 closed). BR6, BR7, BR12 and AC24 of this story still write and publish `AC-READ` and `AC-DENY` through the decision-record library. Pending: the access-log write that replaces that publish, owner Solution architect with the rwb-access owner, tracked as NEW-GAP-G6-1; the publish of BR12 and AC24 is not built until it is ruled. Neither payload carries a personal value: the `AC-READ` record carries field IDs (identifiers classed as personal data, not values) and markers, the `AC-DENY` record carries the area and the right only, and the policy event carries version labels. `rwb.access.DoALimitChanged.v1` belongs to the delegation slice and is not published here.

#### 12.4 Events consumed

None. A policy change is written and published by the same service, so the cache is dropped on the commit that publishes `AccessPolicyChanged` rather than on a consumed event; the topic exists for the other services' caches (Architecture v5 slide 43: all consume it for cache refresh).

#### 12.5 Workflows and activities

None. This story runs no Temporal workflow and registers no activity on `rwb-access`. The case record view is a synchronous read path, and the case workflow that owns the case stays with rwb-case (Temporal and Drools design; Architecture v5 slide 42).

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is a Temporal Schedule of this service, and its story is RWB-P4-AD008-APP. This story starts no Schedule and reads no `timer` row.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's roles and their `default_scope` |
| `permission` | P4 (`rwb_access`) | The CASE_RECORD right and the `matrix_version` in force |
| `masking_rule` | P4 (`rwb_access`) | The `masked` or `clear` marker per role, field and masking version |
| `role_conflict` | P4 (`rwb_access`) | The conflicting role pairs the sign-in check reads |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | LOV-SCOPE and LOV-CAPABILITY, read through the contract; not owned here |

No table of `rwb_case`, `rwb_source_data`, `rwb_document` or `rwb_decision` is read: the case, the account, the party, the interaction, the document and the deviation stay with their owners, and the only fields of them that enter this service are identifiers and facts carried by a request (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case case-record WireMock | RWB-P3-E1023-CON | Case "RW-2026-000701" with product HIRE_PURCHASE, 2 accounts, queue TDR-BKK-CO, owner "U-81", team "TDR-BKK" and status IN_PROGRESS, with the field lists of AC1 and AC5; case "RW-2026-000702" in team LIT-BKK owned by another user, for AC3 and AC4 |
| decision-record fake | RWB-PLT-E1027-CON | The `AC-READ` and `AC-DENY` write and the publish on `rwb.decision-record.v1`, including the forced failure of X7 |
| policy pack fixture | RWB-P4-E1037-CON | Matrix versions PM-2026.11 and PM-2026.12, masking versions MASK-SIT-01 and MASK-SIT-02, and the roles, scopes and masking rows of the background |
| reference-data fake | RWB-P3-E1043-CON | LOV-SCOPE and LOV-CAPABILITY with the version in force, and the unavailable list of X8 |
| rwb-source-data contract fake | rwb-source-data.yaml 5.1.0; library path `fakes/rwb-source-data/5.1.0/` (working path, NEW-ASM-A1) | Account A-7001 at 97 days past due and THB 206,175.00 with data_as_of 2026-12-02; customer P-7001 with category RETAIL, a contact with a mobile and the EFS entries returned as `InteractionPage` items with `sourceSystem` EFS from `GET /api/recovery/source-data/v1/cases/{caseId}/interactions`; case link A-7010 with no account row, listed by REC-05 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations of RWB-P4-E1037-CON implemented), consumed 0 | Base `/api/recovery/access/v1`; the case facts arrive in the request |
| Kafka | Published 1 service event and 1 decision record; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-access` |
| File | None | No file input or output, and no export |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/caserecord`, Java package `th.co.scb.ace.workbench.recovery.access.caserecord`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read ACE data through rwb-source-data's contract only; only rwb-source-data reads `recovery.v_ace_*` (D-RCV-60) | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is the reason the answer is built from the attributes it is given: `recovery_case`, `case_account`, `case_party`, `interaction`, `document` and `queue` are P3's and P1's, so no joined query and no foreign key crosses a schema here. DP-02 is the per-service login: the service connects to `rwb_access` as the rwb-access login of the baseline, holds no privilege on `public` and none on the ACE views, so a stray read fails on a grant rather than on a code review. DP-03 is the access log: an `AC-READ` and an `AC-DENY` are decision records on `rwb.decision-record.v1` through the local library, so the access question and the decision question are answered from one log. DP-05 is the boundary of the source data: this story reads no `v_ace_*` view at all, because a personal field reaches it as a field ID and leaves it as a marker. DP-06 is recorded because the legacy key carries `caserecord.section.timeout.ms`; in the target the 2 s budget is the platform standard of the contract client, and this story reads no parameter row, so the parameters contract is a precondition of the service lane and not a call of this slice. DP-07 supplies LOV-SCOPE and LOV-CAPABILITY with the version in force, because `lov_value` stays with P3 under the ownership map, and no scope name is a Java constant. DP-08 is the guard library behind the answer: the other services authorise their objects against this service's contract, and this service applies the same guard to its own operations. DP-11 is the caller-facing boundary: one hop, 2 s timeout, cached, and the answer must hold inside it. DP-13 and DP-14 are the naming conventions of the service, on base `/api/recovery/access/v1` and topic `rwb.access.events.v1`. DP-15 is the per-service Flyway sequence that carries the two indexes. DP-18 is the ledger: the contact-history rows are rwb-source-data's under the default ruling, this story reads no ledger row, and the merge itself is the case service's. DP-19 is the route that renders the answer: SCR-03, its five sections and its states are RWB-P3-E1023-APP's, and this story supplies the grant and the markers only.

The platform contracts the DP rows name are preconditions of the service lane already in place behind RWB-P4-E1037-CON in wave 1; this secondary slice adds no new build dependency of its own (metadata H = None; ASM-1735), and the six-monthly access review list (JOB-18) is RWB-P4-AD008-APP.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseRecordAuthoriseController | Controller | The three operations of the existing contract on `/api/recovery/access/v1`; validation and problem responses |
| CaseRecordDecisionService | Service | Right, scope and masking profile for one case-record read, in that order; one answer, one record |
| PermissionResolver | Service | Reads `permission` for the caller's roles and the `matrix_version` in force; resolves the five letters |
| ScopeRule | Service | Compares the attributes of the request with the `default_scope` value in force (OWN, TEAM, REGION, ALL) |
| MaskingProfileService | Service | The `masked` or `clear` marker per field ID for the caller's roles and the masking version in force; default masked |
| RequestShapeValidator | Service | The request carries a case reference, an owner, a queue, a team, a region, a named action and the field IDs asked about |
| AccessRecordWriter | Service | The `AC-READ` and `AC-DENY` entries through the library of DP-03, and the `AccessPolicyChanged` outbox row |
| PolicyCache | Service | The cached answer per policy and masking version, dropped on the policy change |
| PolicyChangeListener | Service | Applies a new policy version and publishes `rwb.access.AccessPolicyChanged.v1` in the same transaction |
| AccessRepository | Repository | `role`, `permission`, `masking_rule`, `role_conflict`, inbox and outbox in `rwb_access`; no foreign table |

**Database and migrations**

- No new table: `role`, `permission`, `masking_rule` and `role_conflict` exist from the wave-1 stories of this service behind RWB-P4-E1037-CON, and the policy rows are loaded by the load path stories.
- One migration in the per-service Flyway sequence of DP-15: `V1023_1__case_record_read_path.sql` adds `ix_masking_rule_role_field` on `masking_rule (role_code, field_id, masking_version)` and `ix_permission_role_area` on `permission (role_id, capability_area, matrix_version)`, so the two reads of an answer are index reads inside the 2 s budget of DP-11. No other index is added by this story.
- The policy rows are versioned by `matrix_version`, `masking_version` and the roles' `valid_from` and `valid_to`; this story writes none of them, and a version is never edited in place (a new version is loaded, approved and published).

**Configuration and reference data**

- The matrix version and the masking version in force are data: the latest `valid_from` on or before the business date, read from `permission.matrix_version` and `masking_rule.masking_version`. That `PM-2026.12` and `MASK-SIT-01` are the versions in force on the release date of 30 November 2026 is Not specified in the source documents (GAP-0989; ASM-1739).
- LOV-SCOPE (OWN, TEAM, REGION, ALL) and LOV-CAPABILITY (the 14 capability areas) are read through the reference-data contract of DP-07 (RWB-P3-E1043-CON).
- No parameter row is read by this story (DP-06 is not called): the 2 s is the platform standard of the contract client behind RWB-P4-E1037-CON, and the cache lives for the versions in force (BR9).
- The field IDs the answer marks are DF-PTY-007, DF-PTY-008 and DF-PTY-016 for this slice; a wider roster is Not specified in the source documents (GAP-0989; ASM-1741).
- The database login is the rwb-access login of the service baseline (DP-02).

**Build steps**

1. `PermissionResolver` and `ScopeRule` over `permission`, `role` and the reference lists, with the matrix version named in the answer; tests for AC1, AC2 and AC4, and a test that a new scope value is accepted as data.
2. `MaskingProfileService` with the covering-row lookup, the `clear` case and the default; tests for AC1, AC4 and AC5.
3. `RequestShapeValidator` with the attribute set of the brief and the named action; a test that a request without a case reference or without an action is refused and the refusal carries no case fact.
4. `AccessRecordWriter` with the `AC-READ` and `AC-DENY` entries written before the answer, and the forced failure of X7; test TC-E1-023-07.
5. The denial path with the refusal shape and no case fact, on both the right check and the scope check; tests TC-E1-023-11 and AC6, AC7.
6. `PolicyCache` and `PolicyChangeListener` with the publish and the drop; test AC9 against the PM-2026.12 and MASK-SIT-02 fixture.
7. The migration of the two indexes, and a timing test that one answer stays inside the 2 s budget on a policy pack of the loaded size.
8. The contract-fake run of the whole capability against RWB-P3-E1023-CON and the decision-record fake, so the story builds before the case side exists in the environment.

**Feature switch.** `rwb.p4.case-record-read`, read from the platform feature-flag library under the R-PREC default ruling. Off: the answer is computed without the cache, so every call reads `permission` and `masking_rule` again and the answer is the same; the markers, the refusals and the record are unchanged, and nothing else in the service changes. The switch changes one rule and no schema, needs no rollback and blocks no case read that the policy allows.

**Done when.** The tests in section 16 pass; a case owned by the caller is answered granted with the three field markers, a case of the caller's team is granted and the same case is refused 404 to a manager of another team, an audit read with scope ALL still comes back masked, a field with no masking row comes back masked, a role without Case record R is refused with no case fact, every granted and every refused read leaves its record, a read whose record cannot be written answers 503 with no personal field, and an approved matrix or masking version changes the answer with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Recovery role, or no second factor | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. | The access check before this story's answer (X3, X9) |
| MSG-P4-002 | No role of the caller holds the right in the capability area | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR1 |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, on the refusal of BR2 |
| MSG-P4-006 | Two roles of the caller conflict | {role} may not be held together with {role}. | The access check, from this service's `role_conflict` rows (X6) |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer (X7) |
| MSG-GEN-006 | A list the answer needs is not available | {system} is not available. Try again in a few minutes. | This story, on a reference-list failure (X8) |
| MSG-GEN-001 | `caseId` missing or not a uuid | Enter {field}. | This story (X10) |
| MSG-PLT-N009-03, -05, -06 | Idempotency key missing or malformed; key conflict; store unavailable | Texts are those of RWB-PLT-N009 | Platform library (X11) |

For MSG-P4-002 the {action} value is the action the caller attempted, one of "open the case record", "read the accounts", "read the parties", "read the contact history" and "read the documents"; for MSG-P4-003 no case fact is echoed, because the message must not confirm that a case exists. Every error is an `application/problem+json` response with `type`, `title`, `status`, `traceId` and `messageCode`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10. Open decision DL10 is still open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 apply until it closes.

### 15. Screens and states

This story builds no screen. SCR-03 Case record, its five sections, its panels, its read-only state and its route are RWB-P3-E1023-APP's through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), with the documents section answered by RWB-P5-E1023-APP; the page that a case outside the scope lands on is the case service's, and the text it shows is the one this story produces.

What this story decides for SCR-03 is what each state may show:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-03 Case record | Granted | The case and the five sections are rendered; the fields this story marks masked are rendered from the masked column, and the screens hold no masking rule of their own |
| SCR-03 Case record | Masked field | A field answered `masked` has no clear value available to the screen from this service, so the screen renders the masked column or the default marker and never a value |
| SCR-03 Case record | Refused | The page shows MSG-P4-002 naming the action and no case fact, and one `AC-DENY` entry exists |
| SCR-03 Case record | Not found | The page shows MSG-P4-003 and no case fact, and one `AC-DENY` entry exists |
| SCR-03 Case record | Not available | The page shows MSG-P7-003 where the record could not be written, or MSG-GEN-006 where a list could not be read, and no case fact |
| SCR-03 Case record | Empty | Not specified in the source documents (CG-ALL-4973) |
| SCR-03 Case record | Loading | Not specified in the source documents (CG-ALL-4973) |
| SCR-03 Case record | Error | Not specified in the source documents (CG-ALL-4973) |
| SCR-03 Case record | No access | Not specified in the source documents (CG-ALL-4973) |

A screen that renders a field clear because a client cached it is a defect of the screen, not of the answer: the answer always names the masking version it used, and a field is clear only where a row of that version says so.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-023-11 | AC6, AC7, BR1, BR7 | Component | A test user holding RW-REFADM, which has no Case record right, asks for the case record of RW-2026-000701 and is refused with MSG-P4-002, with one AC-DENY entry and no case fact |
| TC-E1-023-01 | Owned by RWB-P3-E1023-APP: the load budget of SCR-03 | End to end | Case RW-2026-000701 with 50 documents and 120 contact-history entries; the budget is measured on the screen, not on this answer |
| TC-E1-023-02 | Owned by RWB-P3-E1023-APP: the account facts and the business date from ACE | End to end | Contract fake (rwb-source-data): account A-7001 at 97 days past due and THB 206,175.00 with data_as_of 2026-12-02 |
| TC-E1-023-03 | Owned by RWB-P3-E1023-APP: the customer, the contacts and the contact history | End to end | Contract fake (rwb-source-data): customer P-7001 with category RETAIL, a contact with a mobile, and the EFS entries |
| TC-E1-023-04 | Owned by RWB-P3-E1023-APP: the stale ACE batch and the banner | End to end | No COMPLETED ALS row for 2026-12-03 and data_as_of 2026-12-02 |
| TC-E1-023-05 | AC5, BR2 | Component | Case RW-2026-000702 in team LIT-BKK owned by another user, asked for by an OWN-scope owner of team TDR-BKK; 404 with MSG-P4-003 and no case fact |
| TC-E1-023-06 | Owned by RWB-P3-E1023-APP: the document hub not answering | End to end | The document hub does not answer within 3 seconds; the documents section is P5's |
| TC-E1-023-07 | AC7, BR6 | Component | The decision-record writer forced to reject every write during a granted read of RW-2026-000701; 503 with MSG-P7-003 and no personal field |
| TC-E1-023-08 | AC8, BR4, BR5 | Component | Phone collector U-82 holds RW-PHONECOL and reads RW-2026-000701 in scope OWN: DF-PTY-007 is marked "masked" from id_no_masked and DF-PTY-016 "masked" from contact_value_masked, DF-PTY-008 has no row and is masked, and the AC-READ entry names U-82, the three field IDs and their masked markers |
| TC-E1-023-09 | Owned by RWB-P3-E1023-APP: the on-hold banner and the prescription date | End to end | Case RW-2026-000701 on hold for deviation X1 with prescription date 2028-03-15 |
| TC-E1-023-10 | Owned by RWB-P3-E1023-APP: the empty documents and contact-history sections | End to end | Case RW-2026-000703 with no documents and no contact history |
| TC-E1-023-12 | Owned by RWB-P3-E1023-APP: the no-copy rule and the ACE business date | End to end | The balance of A-7001 changed by the 2026-12-03 ALS batch |
| TC-E1-023-13 | Owned by RWB-P3-E1023-APP: the account link with no ACE row | End to end | Contract fake (rwb-source-data): case link A-7010 with no account row, and REC-05 listing it |
| TC-E1-023-14 | AC2, BR2 | Component | Case RW-2026-000701 in team TDR-BKK owned by U-81: a TEAM-scope manager of TDR-BKK is granted with scope TEAM, and a TEAM-scope manager of team LIT-BKK is refused 404 with MSG-P4-003 |
| TC-E1-023-15 | AC5, BR4 | Component | No MASK-SIT-01 row covers DF-PTY-008; U-81 (RW-CASEOWN, owner of RW-2026-000701) asks for DF-PTY-008 and DF-PTY-016; DF-PTY-008 is masked with the default marker XXXX-XX-XX and one AC-READ entry names both field IDs as masked |
| TC-E1-023-16 | AC9, BR9 | Component | U-81 asks for RW-2026-000701 twice under PM-2026.11 and the second answer comes from cache with no second matrix read; PM-2026.12 and MASK-SIT-02 are approved and AccessPolicyChanged is published; the next ask runs under the new versions and a field with no MASK-SIT-02 row is masked |
| TC-E1-023-17 | AC5, BR4 | Component | No MASK-SIT-01 row covers DF-PTY-008; U-81 (RW-CASEOWN, owner of RW-2026-000701) asks for DF-PTY-008 and DF-PTY-016; DF-PTY-008 is marked masked with XXXX-XX-XX and one AC-READ entry names both field IDs as masked |
| TC-E1-023-18 | AC9, BR9 | Component | U-81 holds a cached answer for RW-2026-000701 under PM-2026.11 and MASK-SIT-01; AccessPolicyChanged is published for PM-2026.12 and MASK-SIT-02; the next ask is answered under the new versions with no deployment |
| TC-E1-023-19 | AC10, AC16, BR3 | Component | A token with a Recovery role and no second factor asks for RW-2026-000701; 401 with MSG-P4-001, the permission matrix is not read, and one refusal entry is written |
| TC-E1-023-20 | AC11, AC17, BR5 | Component | U-81 (RW-CASEOWN, owner of RW-2026-000701) asks for DF-PTY-007 in clear; DF-PTY-007 is marked masked and the identity values are read from id_no_masked and id_no_last4 only |
| TC-E1-023-21 | AC12, AC18, BR10 | Component | A test user holds RW-SECADM with a conflicting business role listed in the role_conflict rows; sign-in is refused with MSG-P4-006 and no authorise request is made |
| TC-E1-023-22 | AC13, AC19, BR10 | Component | The reference list of scope or capability is not available; U-81 asks for RW-2026-000701; 503 with MSG-GEN-006, one AC-DENY entry, and no AC-READ entry |
| TC-E1-023-23 | AC14, AC20, BR1 | Component | A service identity holding RW-REFADM asks for RW-2026-000701 with action read the parties; 403 with MSG-P4-002 and one AC-DENY entry |
| TC-E1-023-24 | AC15, AC21, BR3, BR8, BR9, BR10 | Component | Code review of rwb-access for literal role codes, scope names, capability areas, field IDs and version strings; boundary test of the schema reads, the no-role guard and the AccessPolicyChanged drop |
| TC-E1-023-25 | AC22, BR3 | Component | A request to a provided operation on /api/recovery/access/v1 with no valid token; 401 with MSG-P4-001 and no case fact |
| TC-E1-023-26 | Section 12 operations, events and activities | Contract | Not specified in the source documents (DOR-RWB-P4-E1023-APP-12) |
| TC-E1-023-27 | Section 12.7 tables (ASM-3438) | Boundary | Not specified in the source documents (DOR-RWB-P4-E1023-APP-12) |
| TC-P4-E1023-APP-01 | AC23, BR11 | Contract | Case number as caseId; missing caseId |
| TC-P4-E1023-APP-02 | AC24, BR12 | Contract | Event headers and data.caseId against the registry schema; no ledger POST |
| TC-P4-E1023-APP-03 | AC25, BR13 | Component | Replay, conflict, missing key, store outage |

The thirteen legacy TC IDs are kept in the legacy order, and each row names either the criterion of this story that the case answers or the slice that owns the legacy case. The Level column follows Template and Rules section R7.2: the legacy level Access maps to Component, and the legacy level System maps to Component where the case side is the contract mock and to End to end where the whole screen is exercised — so the four cases of the read decision are Component here, and the nine case-side cases are End to end and owned by RWB-P3-E1023-APP. In detail: TC-E1-023-11 answers the refused read, which is the one legacy Access case of the key; TC-E1-023-05 answers the out-of-scope page, which is the legacy AC5 and AC-EXC-P4-004-01; TC-E1-023-07 answers the read that cannot be logged, which is the legacy AC7 and AC-EXC-P4-007-03; and TC-E1-023-08 answers the masking by role, which is the legacy AC8 and AC-EXC-P4-004-05 with the identity number and the contact value never clear. The other cases name the case-side slice of the key they belong to: the data from ACE in TC-E1-023-02, the stale batch in TC-E1-023-04, the document hub in TC-E1-023-06, the hold banner in TC-E1-023-09, the empty sections in TC-E1-023-10, the no-copy rule in TC-E1-023-12 and the account link with no ACE row in TC-E1-023-13, all of them RWB-P3-E1023-APP's, with TC-E1-023-01 and TC-E1-023-03 belonging to RWB-P3-E1023-APP and RWB-P5-E1023-APP. No `-ITG` id sits in this story: the integration copy of this key is RWB-ITG-E1023-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: role codes, scope values, capability areas, field IDs, the matrix version and the masking version are data rows in `rwb_access` and list values read through DP-07; the switch is a platform flag (BR10).
- No personal data in logs, events, the record or the tests. The answer carries markers, the `AC-READ` entry carries field IDs and markers, the `AC-DENY` entry carries the area and the right, and the event carries version labels; test data is synthetic and staff appear as user references.
- ACE fields only as identifiers, never as values: DF-PTY-007, DF-PTY-008 and DF-PTY-016 name fields of P1's contract, this service stores no customer value, and the answer has no clear identity number to give (NFR-039, NFR-040).
- No cross-schema read (DP-01, DP-05, DP-18): `recovery_case`, `case_account`, `case_party`, `interaction`, `document`, `queue` and the `v_ace_*` views are never named by a statement of this story; the case facts arrive in the request and the policy is the service's own. Boundary rule BND-6 of RWB-P4-E1069-APP stays green on this package.
- One writer for the policy: only the load path stories of this service write a role, a permission or a masking row; this story reads them and publishes the change, so an answer and the policy it names cannot disagree.
- The record is written before the answer: a failure answers 503 with no personal field and raises an incident, so no case read is unlogged (BR6, BR7).
- Default deny: a missing role is 401, a missing right is 403 and an out-of-scope case is 404, never an allow; a field with no masking row is masked, never clear (BR2, BR4).
- The answer is idempotent for a policy version: the same question under the same matrix and masking versions returns the same answer, and the cache is dropped on the policy event rather than on a timer (BR9).
- The switch changes one rule and no schema: it removes the cache and never widens a scope, a right or a masking marker.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-007 | The case record view with the account, arrears, owner, queue, stage, status, contact history and documents — the read of it is decided here | Epic 1, 3.6; Program, 5.6 | FEAT-ACA-11 | 06 Take over and own the case | BR1, BR2, BR6, BR7 | TC-E1-023-05, TC-E1-023-07, TC-E1-023-11 |
| REQ-RDF-009 | Every data product carries a freshness stamp — the stamp and the banner are the case service's; this story answers the read of the section that carries it | Epic 1, 3.1; Program, 5.1 | FEAT-ACA-11 | 06 Take over and own the case | BR8 (no copy enters here) | None in this story; TC-E1-023-02 and TC-E1-023-04 are RWB-P3-E1023-APP's |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call — answered here as markers, never values | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-05, FEAT-ACA-11 | 06 Take over and own the case | BR4, BR5 | TC-E1-023-08 |
| REQ-ACA-006 | Every read of the case store and the document store is written to the access log | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-07, FEAT-ACA-08 | 06 Take over and own the case | BR6, BR7 | TC-E1-023-07, TC-E1-023-08, TC-E1-023-11 |
| REQ-ACA-009 | A user sees only the cases and queues their role and scope allow | Epic 1, 3.6; Program, 5.6 | FEAT-ACA-14, FEAT-ACA-11 | 06 Take over and own the case | BR2; CTL-09 | TC-E1-023-05, TC-E1-023-11 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1023-CON | Contract | C: the case-record contract that publishes the five read endpoints and the case facts an authorise request is built from, with its fake |
| RWB-P3-E1023-APP | App development | Sibling slice: the screen SCR-03, the five read endpoints, the ACE view reads, the contact-history merge and the reference and parameter reads of the case side |
| RWB-P4-E1037-CON | Contract | The service contract whose three operations this story implements for the case record view; it carries the matrix, the scope values and the masking rows as data |
| RWB-PLT-E1037-CON | Contract | The platform guard library and the authorise and masking fakes the callers of this service build against |
| RWB-P4-E1069-APP | App development | The boundary rule BND-6 this package must stay green against: no class names a `v_ace_*` view or a `public` table |
| RWB-S8-E1023-APP | App development | The deviation flag on the case record view, which is S8's and is not decided here |
| RWB-ITG-E1023-ITG | Integration | The end-to-end proof of the read across the case service, the source data, the document hub, the deviation flag and this answer |

| Legacy reference | Where it is kept |
|---|---|
| The scope answers of legacy section 10 (Own, Team, Region and All) and the on-scope case of AC5 | Sections 1, 7, 8, 10 |
| The refusal of a role with no Case record right and the not-in-scope answer that confirms no case exists | Sections 4, 5, 7, 14 |
| Masking of DF-PTY-007, DF-PTY-008 and DF-PTY-016, the identity number never clear and the default masked | Sections 3, 4, 7, 8, 11 |
| The access-log entry of AC7 and AC8 and the 503 of AC7 | Sections 4, 5, 7, 8, 14 |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-006, MSG-P7-003, MSG-GEN-006 | Section 14, exception paths |
| Matrix version PM-2026.12, masking version MASK-SIT-01, roles RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-LITOFF, RW-CONDUCT, RW-AUDIT, RW-REFADM, RW-SECADM | Background, AC1 to AC9, sections 3 and 10 |
| Legacy key RWB-E1-023, story RWB-P4-E1023-APP, contract RWB-P3-E1023-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The rwb-case slice of this legacy key, RWB-P3-E1023-APP and its contract RWB-P3-E1023-CON: the five read endpoints `GET /cases/{caseId}`, `/accounts`, `/parties`, `/interactions` and `/documents`, the case facts, the queue and the case reference.
- SCR-03 Case record and its layout, its five sections, its panels and its states, and the page a case outside the scope lands on.
- The ACE view reads, the per-section business date and the freshness banner: `v_ace_account`, `v_ace_customer`, `v_ace_contact`, `v_ace_efs_action` and `v_ace_batch_status` are P1's through rwb-source-data, and the reads themselves are P3's.
- The contact-history merge with the interaction ledger (DP-18): the ledger is rwb-source-data's and the merge is the case service's; this story reads no ledger row.
- The documents section: RWB-P5-E1023-APP and RWB-P5-E1024-APP.
- The deviation flag and the hold banner on the case record view: RWB-S8-E1023-APP.
- RWB-ITG-E1023-ITG, the integration harness copy of the tests of this key, which proves the real cross-service behaviour end to end.
- Loading, approving and rolling back the policy pack: the reference-load and approval path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and the administration screens of Epic 8.
- The delegation of authority table and its lookup (RWB-P4-E1038-APP and RWB-P4-E2013-APP), the DoA-limits operation and `rwb.access.DoALimitChanged.v1`; no DoA level applies to a read.
- Break-glass access, the access log search and export, and the access-entry writer of RWB-P4-E1039-APP and RWB-P4-AD007-APP.
- The six-monthly access review list (JOB-18, RWB-P4-AD008-APP) and every other job, workflow and Schedule of this service.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).

## Remaining delivery steps

- Size the story at refinement (squad).
- Sign the epic design for RWB-SVC-P4 (Solution architect).
- Bring RWB-P4-E1037-CON and RWB-P3-E1023-CON to Done and publish their fakes at pinned versions (contract owners).
- Publish POST /authorise in rwb-access.yaml (rwb-access service owner, GAP-0983).
- Add ce_actor and ce_idempotencykey support to the decision-record library (platform library owner).
- Rule the access-log write that replaces the published access records, then restate BR6, BR7, BR12 and AC24 (Solution architect, NEW-GAP-G6-1; RD-P1-072).
- Create the case and policy fixtures in DEV and add the new test rows in Test Cases v9 (squad; test lead).
