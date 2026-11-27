# RWB-P4-E2024-APP Field app photos and bills into the document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2024-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-P4-AP |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2024-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DCM-013) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-024 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E2024-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **field collector who captures a home and a utility bill in the field app, and the case owner, restructuring officer and OCR pipeline that read those captures**, I want **an access answer that says whether my role carries the Documents right to send a capture, to read it or to mark it reviewed, whether the case is in my scope, which fields of the capture are masked for my role and under which masking version and permission matrix version that answer was taken, and an access entry for every capture, read, refusal and action that never holds a position, a file name or a photo**, so that **an inspection reaches the case the same day it is made, the position of a customer's home is answered masked to every role the policy does not name, and no coordinate reaches a log**.

Inside `rwb-access` this is the access slice of the field capture of legacy RWB-E2-024:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The slice delivers three answers and one record: the authorise decision for capability area `DOCUMENTS` with right `C` on sending the captures of a case, right `R` on reading the captures and the SCR-30 panel and right `U` on the review state and the extracted bill fields, the resolved scope answer (`OWN`, `TEAM`, `REGION`, `ALL`) with the task on the case as the `OWN` test, the masking answer for the capture fields — `captured_at` `DF-DOC-027`, `capture_latitude` `DF-DOC-028`, `capture_longitude` `DF-DOC-029`, `capture_kind` `DF-DOC-031` and the review state — and the access-log entry written as a decision-record entry of DP-03 on every allowed read (`AC-READ`) and every refusal (`AC-DENY`).
- The slice delivers no business behaviour. The manifest check, the duplicate check on `client_file_id`, the file type, the size, the capture time against the clock skew and the age limit, the malware scan, the store, the capture columns, the partial unique index, the OCR intake and the extraction are `rwb-document`'s (C dependency `RWB-P5-E2024-CON`, consumed through that contract and its fake, one hop, 2 s timeout). The `DOCATT` entry the store writes is that service's and is not this story's.
- The slice builds no screen. SCR-30 Case documents is `rwb-document`'s, served through the gateway-bff composite route of DP-19; the case facts, the case state and the field inspection task are `rwb-case`'s; the field app screens are the field app's.
- The masking rule of legacy BR9 and CTL-11 — the GPS position and the photos of a home are personal data — is executed here as data: a field is answered unmasked only where a `masking_rule` row for the role and the field says `unmasked` true under the mask version in force. The unmask is answered for the roles the policy names, `RW-CASEOWN` and `RW-RESTRUCT`, and never for `RW-PHONECOL`; a field with no covering row stays masked, so a slip in the pack cannot open a position.
- The policy pack is data: permission rows under matrix version `PM-2026.12`, masking rows under masking version `MASK-SIT-01`. The load path that writes those rows is `rwb-access`'s own and is out of this story (RWB-P4-AD002-APP, RWB-P4-AD004-APP).
- The Documents letters per role are carried from the legacy authority table — `RW-FIELDCOL` `CR`, `RW-CASEOWN` `CRU`, `RW-RESTRUCT` `CRU`, `SY-OCR` `CRU` and `RW-PHONECOL` `R` — and the TSD P4 matrix does not carry a Documents column (GAP-0949; ASM-1679). The masking version in force for SIT is assumed `MASK-SIT-01` and no mask format for a coordinate is fixed by any source (GAP-0950; ASM-1680).

The values carried from the legacy story are unchanged: case `RW-2026-000501` with entry date `2026-10-02`, field collector `FC-01`, an inspection of ten synthetic files (eight `INSPECTION_PHOTO` and two `UTILITY_BILL`) captured at `2026-12-15 14:20` at latitude `13.7563` and longitude `100.5018`, a capture made with no signal at `2026-12-14 10:05`, and case `RW-2026-000502` where `FC-01` has no task.

### 2. Business rationale

An inspection photo that cannot be shown to have been taken where and when it was claimed is evidence that fails exactly when it is questioned, and a home's position copied into a log or shown to a role that has no right to it is a PDPA finding. The legacy story proved the capture; this slice proves the authorisation, the scope and the masking behind it. Today the right to send a capture is spread over role documents and manual checks, the position is copied into working files and log lines that no one reviews, and a refusal leaves no trace of who was refused what. Under Architecture v5 the authorise answer, the scope answer and the masking answer come from `rwb-access` as data, with the matrix version and the mask version naming the policy the answer was taken from, and every look at a capture is an append-only entry in the same ledger as the decisions.

This story carries controls CTL-11 (GPS position and photos of a home masked by role and never logged), the auditionable expectation behind NFR-042 (every read of the document store is logged) and NFR-051 (a service identity is subject to the same check as a person). It meets REQ-DCM-013 on the access side, supports REQ-ACA-005, REQ-ACA-006 and REQ-ACA-007, and supports the measure rule and limit changes made without a code release (target 100 percent).

The realignment changes the mechanism, not the business rule:

1. The permission rows and the masking rows of the monolith's recovery schema become `rwb-access`'s own tables in `rwb_access` (DP-01), versioned by matrix version and mask version, so a change of rights or of masking needs an approved load and no release.
2. The synchronous access check inside the monolith becomes the published authorise contract, cached, with one hop and a 2 s timeout (DP-11); the composite route asks `rwb-access` and holds the answer for the life of the cache entry.
3. The decision-log writer inside the monolith becomes the local decision-record library of DP-03, so an `AC-READ` or `AC-DENY` entry is hash-chained and published on `rwb.decision-record.v1` where `rwb-decision`'s ledger and the audit query already read.
4. The access event that the monolith never sent becomes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, and every holder of a cached answer — this service's own cache first — refreshes on it, so a new masking version is in force at the next call with no deployment.
5. The position itself stays where it is: `capture_latitude` and `capture_longitude` are `rwb_document`'s columns, and `rwb-access` answers only that the field is masked, under which version, and for which roles — never a value and never a format.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2024-CON | The published field-capture contract this slice is tested against: case `RW-2026-000501` with entry date `2026-10-02` and a field inspection task for `FC-01`, the ten items of the inspection (eight `INSPECTION_PHOTO` and two `UTILITY_BILL`) with capture time `2026-12-15 14:20` at `13.7563` and `100.5018`, the offline capture at `2026-12-14 10:05`, the out-of-scope case `RW-2026-000502`, the two refusals of legacy AC12 and the forced entry failure of TC-E2-024-17, with its contract fake. The request and response shape of the authorise call itself is Not specified in the source documents (GAP-0952; ASM-1682) |
| Permission matrix `PM-2026.12` `IN_FORCE` | The rows this slice answers from, loaded by the policy pack path (RWB-P4-AD002-APP, RWB-P4-AD004-APP): `DOCUMENTS` `CR` for `RW-FIELDCOL`, `DOCUMENTS` `CRU` for `RW-CASEOWN`, `RW-RESTRUCT` and `SY-OCR`, `DOCUMENTS` `R` for `RW-PHONECOL`, and no `DOCUMENTS` row for a role outside the pack. The letters are carried from legacy section 10 (GAP-0949; ASM-1679) |
| Masking version `MASK-SIT-01` in force | The rows for `DF-DOC-028` and `DF-DOC-029` with `unmasked` true for `RW-CASEOWN` and `RW-RESTRUCT`, `unmasked` false for `RW-FIELDCOL` and `RW-PHONECOL`, and no row for `SY-OCR`, so the position is masked for the collector who made the capture and for the OCR path and opens only to the two roles the policy names. The version label is assumed for SIT and no mask format for a coordinate is fixed (GAP-0950; ASM-1680) |
| Test users in SIT | The FSD P4 test users `U-4101` holding `RW-CASEOWN`, `U-4103` holding `RW-TEAMMGR` and `U-4106` holding `RW-PHONECOL`, and the field collector `FC-01` holding `RW-FIELDCOL` from the legacy story. The criteria name the role `RW-RESTRUCT` and the service identity `SY-OCR` rather than a user ID, because no source fixes one |
| The decision-record library and its topic | `rwb.decision-record.v1` and the local library of DP-03, so an access entry is written, chained and published in one transaction with the answer |
| gateway-bff composite route | The route of DP-19 that carries the field-app sync and the SCR-30 panel calls to this base path, with the 2 s timeout of DP-11. Whether the field app reaches the route or this base directly is Not specified in the source documents (GAP-0951; ASM-1681) |

Business preconditions carried from RWB-E2-024:

- The field collector holds a task on the case, so the case is in `OWN` scope; a case with no task for the caller is out of scope.
- The clock skew is 5 minutes, the age limit 30 days and the file limit 50, and the document types are `INSPECTION_PHOTO`, `INSPECTION_CHECKLIST` and `UTILITY_BILL`; every one of those is `rwb_document`'s row and check and none of them changes the access answer.
- A capture with no GPS position is stored and flagged with MSG-P5-015; the flag is `rwb-document`'s and the masked answer of this slice is the same with or without a position.
- Every refusal is answered with MSG-P4-002 naming the action and the capability area, or with MSG-P4-003 for a case outside the scope, and no capture content (FSD P4 v3 A2.4 VR-P4-004-1, A2.14 VR-P4-014-1).

### 4. Flow

1. Field collector: `FC-01` captures eight photos and two bills in the field app; the app records for each file the device time, the GPS position and a client file ID.
2. Field app: when a signal is available, sends the captures for case `RW-2026-000501` through the gateway-bff composite route of DP-19.
3. gateway-bff composite route: before it forwards the sync to `rwb-document`, calls `POST /api/recovery/access/v1/authorise` on this service with the caller's user reference `FC-01`, the roles the session resolved, capability area `DOCUMENTS`, right `C`, case `RW-2026-000501` as the object reference, the activity that makes the case `OWN` (`FC-01` holds a field inspection task on it) and the field list the panel will render — `captured_at`, `capture_latitude`, `capture_longitude`, `capture_kind` and the review state.
4. `AuthoriseService`: reads the caller's permission rows for `DOCUMENTS` from `permission` in `rwb_access` under the matrix version in force, unions the letters of every role the caller holds, and answers `allowed` with right `C`, the role `RW-FIELDCOL`, scope `OWN`, `matrixVersion` `PM-2026.12` and `maskingVersion` `MASK-SIT-01`.
5. `ScopeCheck`: takes the scope from the caller's `role.default_scope` row and applies it; the `OWN` test is the task the case holds for the caller. A case with no task for the caller — `RW-2026-000502` for `FC-01` — is out of scope: the answer is 404 with MSG-P4-003, one `AC-DENY` entry is written, and the route stops before `rwb-document` is called at all.
6. `MaskingPolicyService`: reads the `masking_rule` rows for the five fields and the caller's roles under the mask version in force and answers each field's masked flag. Where no row covers a field for any of the caller's roles the answer is masked as well, so the default is refuse rather than show (FSD P4 v3 A2.5, AC-EXC-P4-004-05). No value of a position is read, echoed or cached by this service.
7. `AccessLogWriter`, in the same transaction as the answer: writes the decision-record entry of DP-03 with decision code `AC-READ`, the actor, the case reference, the capability area, the right, the scope, the matrix version, the mask version and the field markers, with `DF-DOC-028` and `DF-DOC-029` marked masked and no value and no file name; publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` through the outbox.
8. The route forwards the sync to `rwb-document`, which runs the manifest check, the duplicate check on `client_file_id`, the type, size, time and position checks, the malware scan, the store, the capture columns and the OCR intake; this service is not called again on that path, and the `DOCATT` entry the store writes is that service's.
9. Case owner: `U-4101` opens SCR-30 Case documents; the route calls the authorise path with area `DOCUMENTS`, right `R`, the same case and the same field list, and receives the masked flags of `MASK-SIT-01` — the position unmasked for `RW-CASEOWN` because the policy names that role. The panel draws the ten documents with capture time, type and review state, and MSG-P5-015 for a capture with no position; the panel and the warning are `rwb-document`'s.
10. OCR path: `SY-OCR` asks with area `DOCUMENTS` and right `U` for the review state and the extracted bill fields; the answer names role `SY-OCR`, role class `NON_HUMAN_ACTOR`, the letters `CRU`, the role's `default_scope` row and the position masked, because no row unmasks either coordinate field for it (NFR-051).
11. A policy pack load by the service's own administration path commits new `permission` or `masking_rule` rows and writes the outbox row for `rwb.access.AccessPolicyChanged.v1` with the new matrix or masking version; the load itself is RWB-P4-AD002-APP and RWB-P4-AD004-APP.
12. The cache-refresh listener of this service reads that event from `rwb.access.events.v1` and replaces the cached answer for the affected roles; the next authorise call answers with the new version and a new mask answer, with no deployment and no restart, and the answer never mixes a matrix version with a mask version from a different policy load.
13. Phone collector: `U-4106` holding `RW-PHONECOL` with the letter `R` only attempts the sync and is refused with 403 and MSG-P4-002 for the action `send a field capture`; one `AC-DENY` entry names the area and the right and holds no file name and no position.
14. Internal audit: reads the `AC-READ` and `AC-DENY` entries through `rwb-decision`'s decision-log query, where they sit beside the `DOCATT` entries of the same documents.

Every answer and its access-log entry commit in one transaction (DP-03, R-UNI-39), so a call that cannot be logged is refused rather than answered (FSD P4 v3 AC-EXC-P4-007-03), and a repeated call with the same `Idempotency-Key` returns the first answer without a second entry.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds `DOCUMENTS` `R` and asks for right `C` | Refused with 403; one `AC-DENY` entry with area `DOCUMENTS` and the right asked; nothing forwarded to `rwb-document` | MSG-P4-002 | AC2 |
| X2 | The case has no task for the caller, so it is outside `OWN` scope | Refused with 404; one `AC-DENY` entry naming the case; no document, intake item or capture row is written | MSG-P4-003 | AC3 |
| X3 | No masking row covers a field for any of the caller's roles | The field is answered masked under the mask version in force; the entry marks it masked; no value is read | None | AC5 |
| X4 | The decision record of the access entry cannot be written | The call returns 503, no answer and no accepted item; the reason is logged; the cache is unchanged | MSG-P7-003 | AC6 |
| X5 | A second call arrives with the same `Idempotency-Key` | The first answer and its entry are returned; no second entry is written | None | AC10 |
| X6 | A matrix version and a mask version arrive from two different policy loads | The cache refuses the mixed pair, keeps the versions it already holds and raises the mismatch; the caller gets the older consistent pair | None | AC7 |
| X7 | The policy event arrives before the cache is warm | The first call reads the rows directly, writes its entry and warms the cache from the same rows | None | AC7 |
| X8 | A capture carries no position | The masked answer for `DF-DOC-028` and `DF-DOC-029` is unchanged and the entry holds the field markers with no value; the MSG-P5-015 flag is `rwb-document`'s | None | AC9 |

An answer is never served without its entry and never without naming both policy versions; a call whose entry fails is an error, not a silent success.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published field-capture contract RWB-P5-E2024-CON and its fake; the case, the items, the capture times and the positions arrive in the request from the composite route, never as a table read |
| Negotiable | Letters, roles, areas, scopes, masking rows, mask formats and versions are data; the story fixes the answer shape, the field list and the entry only |
| Valuable | No capture is sent and no panel opens without a current authorise answer, the position opens only to the roles the pack names, and no coordinate reaches a log |
| Estimable | Three endpoints used, one scope check, one cache, one masking answer, one entry writer, no migration of its own |
| Small | Fits one week with its tests, because the capture, the store, the OCR intake, the extraction and the screen are other stories' |
| Testable | Every criterion below is one test case in section 16; the case, the task, the items and the positions are returned by the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Access decisions, masking answers and access-log entries for field app captures

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.12" is in force and masking version "MASK-SIT-01" is in force
    Given test user "U-4101" holds RW-CASEOWN, test user "U-4103" holds RW-TEAMMGR, test user "U-4106" holds RW-PHONECOL, the field collector "FC-01" holds RW-FIELDCOL and the service identity "SY-OCR" holds role "SY-OCR" with role class "NON_HUMAN_ACTOR"
    Given the rwb-document contract mock returns case "RW-2026-000501" with entry date 2026-10-02 and a field inspection task for field collector "FC-01"
    Given the rwb-document contract mock returns the ten items of that inspection, eight "INSPECTION_PHOTO" and two "UTILITY_BILL", with capture time 2026-12-15 14:20, latitude 13.7563 and longitude 100.5018

  Scenario: AC1 Ten captures are authorised with Documents C on a case in Own scope (new, D-RCV-60)
    Given the rwb-document contract mock returns the ten items for case "RW-2026-000501" and the field inspection task of "FC-01" on it
    When "FC-01" syncs at 2026-12-15 14:20 and the authorise path is called with area "DOCUMENTS", right "C", case "RW-2026-000501" and the field list "captured_at", "capture_latitude", "capture_longitude", "capture_kind", "review_status"
    Then the answer is allowed with area "DOCUMENTS", right "C", role "RW-FIELDCOL", matrix version "PM-2026.12" and masking version "MASK-SIT-01"
    Then the answer names scope "OWN", because "FC-01" holds a task on the case
    Then exactly one access-log entry exists for the sync with decision code "AC-READ", actor "FC-01", case "RW-2026-000501" and area "DOCUMENTS", and one item reference for each of the ten items
    Then the answer and the entry hold no latitude, no longitude, no file name and no photo

  Scenario: AC2 A role with Documents R only is refused the capture sync (new, D-RCV-60)
    Given test user "U-4106" holds RW-PHONECOL and the permission row of RW-PHONECOL in "PM-2026.12" holds the letter "R" for "DOCUMENTS"
    When "U-4106" calls the authorise path with area "DOCUMENTS", right "C" and case "RW-2026-000501"
    Then the call is refused with status 403 and message MSG-P4-002 for the action "send a field capture" and the area "DOCUMENTS"
    Then one access-log entry exists with decision code "AC-DENY", actor "U-4106", area "DOCUMENTS", right "C" and case "RW-2026-000501"
    Then the answer and the entry hold no file name, no position and no document reference
    Then the sync is not forwarded to "rwb-document" and no document is stored for it

  Scenario: AC3 A case outside the collector's scope is answered 404 and nothing is stored (new, D-RCV-60)
    Given the rwb-document contract mock returns case "RW-2026-000502" with no task for "FC-01"
    When "FC-01" sends captures for "RW-2026-000502" and the authorise path is called with area "DOCUMENTS", right "C" and case "RW-2026-000502"
    Then the answer is refused with status 404 and message MSG-P4-003
    Then one access-log entry exists with decision code "AC-DENY", actor "FC-01", case "RW-2026-000502" and area "DOCUMENTS"
    Then no document, no intake item and no capture row is written for "RW-2026-000502"

  Scenario: AC4 Reading the captures is Documents R and the position opens only to the roles policy names (new, D-RCV-60)
    Given the rwb-document contract mock returns ten documents on case "RW-2026-000501" with captured_at 2026-12-15 14:20, capture_latitude 13.7563 and capture_longitude 100.5018
    When "U-4101" opens SCR-30 and the composite route calls the authorise path with area "DOCUMENTS", right "R", case "RW-2026-000501" and the field list "captured_at", "capture_latitude", "capture_longitude", "capture_kind", "review_status"
    Then the answer is allowed with right "R" for role "RW-CASEOWN" and marks "DF-DOC-028" and "DF-DOC-029" unmasked under masking version "MASK-SIT-01"
    When the masking answer is asked through GET /api/recovery/access/v1/masking-policies for fields "DF-DOC-028" and "DF-DOC-029" and role "RW-PHONECOL"
    Then both fields are masked under "MASK-SIT-01" for "RW-PHONECOL"
    Then neither answer carries a latitude, a longitude, a mask format or a file name

  Scenario: AC5 The OCR service identity is answered with Documents CRU and the position masked (new, D-RCV-60)
    Given the permission row of "SY-OCR" in "PM-2026.12" holds the letters "CRU" for "DOCUMENTS"
    When the OCR and extraction path calls the authorise path with area "DOCUMENTS", right "U" and the document reference returned by the rwb-document contract mock
    Then the answer is allowed with right "U", role "SY-OCR", role class "NON_HUMAN_ACTOR" and the letters "CRU" for "DOCUMENTS" under "PM-2026.12"
    Then the scope in the answer is the default_scope row of role "SY-OCR" and not a value written in code
    Then "DF-DOC-028" and "DF-DOC-029" are masked for "SY-OCR" under "MASK-SIT-01", because no row unmasks either field for it
    Then the answer carries no latitude, no longitude and no extracted bill value

  Scenario: AC6 A capture whose access entry cannot be written is refused and not stored (new, D-RCV-60)
    Given the rwb-document contract mock returns three items for case "RW-2026-000501"
    Given the decision-record fake is forced to fail the entry write
    When "FC-01" syncs the three items
    Then the call returns status 503 with message MSG-P7-003 and no accepted item
    Then no document, no intake item and no capture row is written for any of the three items
    Then no access-log entry is left half written and the cached answer is unchanged
    Then an incident is raised for the failed entry

  Scenario: AC7 A masking policy change reaches the cached answer without a deployment (new, D-RCV-60)
    Given the cached answer for "U-4101" holds masking version "MASK-SIT-01"
    When the policy pack load commits a masking row set under a masking version later than "MASK-SIT-01" and publishes rwb.access.AccessPolicyChanged.v1
    Then the next authorise call for "U-4101" answers with the later masking version and the mask answer of that version
    Then no deployment, restart or cache flush is performed and the matrix version in the answer stays "PM-2026.12"
    Then the answer never pairs the new masking version with a matrix version from a different load

  Scenario: AC8 A refusal names the action and the area and carries no file name or position (new, D-RCV-60)
    Given the rwb-document contract mock returns the ten items with their file names and positions
    When "U-4106" calls the authorise path with area "DOCUMENTS", right "C" and case "RW-2026-000501"
    Then the problem response names the action "send a field capture" and the area "DOCUMENTS" and its messageId is MSG-P4-002
    Then the problem response holds no file name, no latitude, no longitude, no bill amount and no document reference
    Then the "AC-DENY" entry holds the actor, the case, the area, the right and the versions only

  Scenario: AC9 The composite route carries the field list of the field-app sync and the SCR-30 panel (new, D-RCV-60)
    Given the gateway-bff route fake carries the field-app sync and the SCR-30 panel calls to base "/api/recovery/access/v1"
    When the route calls GET /api/recovery/access/v1/masking-policies for the field list "captured_at", "capture_latitude", "capture_longitude", "capture_kind", "review_status" and role "RW-CASEOWN"
    Then the answer names each of the five fields with the masked flag of its "MASK-SIT-01" row for that role and the masking version "MASK-SIT-01"
    Then "capture_latitude" and "capture_longitude" are answered unmasked for "RW-CASEOWN" and masked for "RW-PHONECOL"
    Then the answer holds no value, no mask format and no file name of any field

  Scenario: AC10 A repeated call with the same Idempotency-Key writes no second entry (new, D-RCV-60)
    Given "FC-01" sent the ten items with Idempotency-Key "k-001" and the answer and its entry are stored
    When the field app sends the same call again with key "k-001"
    Then the first answer is returned unchanged
    Then no second access-log entry is written for that call
```

The ten criteria above are the ones this story owns. The slice serves the access part of legacy RWB-E2-024 AC1 (a capture accepted on a case in `OWN` scope), AC6 (a capture with no position accepted, where the warning is `rwb-document`'s) and AC12 (a case outside the collector's scope answered with MSG-P4-003 and nothing stored), and it carries the two access tests TC-E2-024-16 and TC-E2-024-17. Legacy AC2 to AC5, AC7 to AC11 and AC13 to AC15 are `rwb-document`'s and stay with RWB-P5-E2024-APP; no legacy criterion is copied here.

The authorise request and response shape used above — actor, roles, area, right, object reference, activity, field list and idempotency key in, and allowed, roles, area, right, scope, matrix version, masking version, field markers and messageId out — is Not specified in the source documents (GAP-0952; ASM-1682); no field of it is a business value and it is renamed at the contract review if the published contract differs.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A right is taken from the permission rows of the matrix version in force, per role and capability area, with letters C, R, U, D and A; no letter, role or area is written in code | FSD P4 v3 A2.4; BR-P4-004; TSD P4 v3 T6.1 |
| BR2 | Sending the captures of a case needs `DOCUMENTS` C, reading the captures and the SCR-30 panel needs `DOCUMENTS` R, and the OCR and extraction path needs `DOCUMENTS` U | Legacy RWB-E2-024 section 10; FSD P4 v3 A2.4; TSD P4 v3 T3.2 LOV-CAPABILITY |
| BR3 | A role with no `DOCUMENTS` row is denied; the authorise path refuses by default and never falls back to a broader role or to a default letter | FSD P4 v3 A2.4 AC-EXC-P4-004-06; Architecture v5 zero trust, deny by default |
| BR4 | The `OWN` scope test is the task the case holds for the caller; a case with no task for the caller is outside the scope, is answered 404 with MSG-P4-003 and stores nothing | Legacy RWB-E2-024 AC12 and section 3; FSD P4 v3 A2.14 VR-P4-014-1; BR-P4-014 |
| BR5 | The position `DF-DOC-028` and `DF-DOC-029` and a photo of a home are personal data: a field is answered unmasked only where a masking row for the role and the field says so, and a field with no covering row stays masked | Legacy RWB-E2-024 BR9; CTL-11; FSD P4 v3 A2.5 AC-EXC-P4-004-05; BR-P4-005 |
| BR6 | The access answer depends on the rights, the scope and the policy versions only: the capture time, the clock skew, the age limit, the file type, the size, the duplicate `client_file_id` and the malware result are `rwb-document`'s checks and never change the answer | FSD P4 v3 A2.4 VR-P4-004-1; legacy RWB-E2-024 BR1, BR2, BR3, BR4 |
| BR7 | Every allowed read of a capture writes one `AC-READ` entry and every refusal one `AC-DENY` entry, in one transaction with the answer; a call that cannot be logged is refused | FSD P4 v3 A2.7 AC-P4-007-01, AC-EXC-P4-007-03 and AC-EXC-P4-007-04; DP-03; R-UNI-39 |
| BR8 | An answer names the matrix version and the masking version it was decided under, and a policy change reaches the cached answer through `rwb.access.AccessPolicyChanged.v1` with no deployment | FSD P4 v3 A2.4 AC-P4-004-01; Architecture v5 slide 42 cache refresh |
| BR9 | No personal data in the entry or the event: the entry carries the field ID and a masked flag, never a position, a file name or a photo, and the position value stays in `rwb_document` | Legacy RWB-E2-024 section 17; NFR-039, NFR-040, NFR-042 |
| BR10 | A service identity is subject to the same role check as a person: `SY-OCR` is answered from its own role rows and its own default scope, not from a bypass | NFR-051; TSD P4 v3 T6.2; legacy RWB-E2-024 section 10 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a read of `permission` in `rwb_access` under the matrix version in force; the capability area `DOCUMENTS` is a value of LOV-CAPABILITY read through the reference-data contract of DP-07, and the Java code holds no enum of areas, roles or letters.
- BR2 and BR3 are one check on the letter of the requested right in the area `DOCUMENTS`; a missing row is a refusal, never a default.
- BR4 is the `ScopeCheck` on the role's `default_scope` row with the task on the case as the `OWN` test; the task itself is `rwb-case`'s and reaches this service as an activity in the request, never as a table read.
- BR5 is the `masking_rule` read plus the default; the mask format is the masking library's, because no source fixes a rendering for a coordinate (GAP-0950; ASM-1680).
- BR6 is the absence of any capture fact in the authorise request except the object reference, the activity and the field list: no capture time, no clock skew, no file type and no scan result is sent, so no check here can disagree with `rwb-document`.
- BR7 is one `RecordAndApply` transaction on the answer and the entry, with the idempotency key of DP-09.
- BR8 is the version pair in the answer and the cache refresh on the service's own `AccessPolicyChanged`.
- BR9 is a check on the entry writer: the field list it writes is the field ID and the masked flag, and a test asserts the entry text holds no digit of a latitude or a longitude.
- BR10 is the absence of a bypass for `role_class` `NON_HUMAN_ACTOR`: the identity is resolved to a role and answered from the same rows.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No cached answer | Authorise call | The policy rows are in force | Allowed or denied, with the scope and the two versions |
| Allowed | The answer is served | The `AC-READ` entry commits | Served, with the field markers |
| Denied | The refusal is served | The `AC-DENY` entry commits | Refused with 403 and MSG-P4-002, or 404 and MSG-P4-003 |
| Cached under version `PM-2026.12` / `MASK-SIT-01` | `rwb.access.AccessPolicyChanged.v1` | A later policy load is in force | Cached under the new versions, served from the next call |
| Cached, mixed versions | Refresh | The event names a matrix version and a masking version from different loads | Unchanged, with the mismatch raised |

| From | Event | Condition | To |
|---|---|---|---|
| `LOADED` | The policy pack load is approved | The approver is not the loader | `APPROVED` |
| `APPROVED` | The valid-from date is reached | None | `IN_FORCE`, and `AccessPolicyChanged` is published |
| `IN_FORCE` | The next version is approved | None | `SUPERSEDED` |

The second table is the lifecycle of the rows this story reads, owned by RWB-P4-AD002-APP and RWB-P4-AD004-APP; this story reads the version in force and publishes nothing on that path itself.

The captures have their own lifecycle in `rwb_document` — stored, intake item for OCR, extracted, in review — and this story changes none of it. Access-log entries have no lifecycle of their own: they are append-only and are read by `rwb-decision`'s decision-log query.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-FIELDCOL Field collector | Sends the captures of a case in `OWN` scope (`DOCUMENTS` C); the position of the captures is masked for this role |
| RW-CASEOWN Case owner | Reads the captures, the bill fields and the position on the case (`DOCUMENTS` CRU); one of the two roles the masking policy name for an unmasked position |
| RW-RESTRUCT Restructuring officer (FCR) | Reads the captures and the position on a deed in lieu case (`DOCUMENTS` CRU); the second of the two roles the policy name |
| SY-OCR OCR and extraction pipeline | Marks the review state and reads the extracted fields (`DOCUMENTS` CRU); the position stays masked for it because no row unmasks it |
| RW-PHONECOL Phone collector | Reads only (`DOCUMENTS` R); refused the sync, and the position is masked for it |
| RW-AUDIT Internal audit | Reads the `AC-READ` and `AC-DENY` entries with scope `ALL` through `rwb-decision`'s decision-log query, and the policy versions they were decided under |
| Every role with no `DOCUMENTS` row | Refused by default, with an `AC-DENY` entry |
| SY-DECLOG Decision log writer | Writes the `DOCATT` entry through the store in `rwb-document`; not a role this slice checks and not an entry this slice writes |

The scope each role carries is its `role.default_scope` row and is not a value this story fixes; only the `OWN` test — the task on the case — is asserted here. The delegation of authority is not consulted on this path: a capture carries no amount and no approval.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | role_code, role_name, role_class, default_scope | Read |
| DF-REF-040 to DF-REF-044 | `permission` | role_id, capability_area, letters, matrix_version | Read |
| DF-REF-198 to DF-REF-204 | `masking_rule` | role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read |
| DF-DOC-027, DF-DOC-028, DF-DOC-029, DF-DOC-031 | `document` (owned by P5, named only) | captured_at, capture_latitude, capture_longitude, capture_kind | Not read as values: the answer names the field and the masked flag only |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` or `AC-DENY` entry: decision code, actor, object reference, area, right, scope, versions, field markers, time | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the record row | Write |
| (idempotency) | `idempotency_key` | the stored answer of an authorise call with its key | Write |

No `document`, `document_intake`, `document_field`, `document_type` or `document_hub_parameter` row is read on this path: the capture facts arrive in the request from the composite route, and the clock skew, the age limit, the file limit and the type list are `rwb_document`'s rows behind RWB-P5-E2024-CON. No `recovery_case` row is read either: the entry date and the task on the case are `rwb-case`'s and reach this service as request facts. The masked rendering of a coordinate is Not specified in the source documents (GAP-0950; ASM-1680); this story names the field ID, the role and the mask version and leaves the format to the one masking library every screen uses. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None new. The decisions are served through the operations of RWB-P4-E1037-CON on base `/api/recovery/access/v1`, owner P4 `rwb-access`; this slice adds no path and no operation, and decides the following behind them:

| Method | Path | Purpose | Authorization | Errors |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The role, scope, right and field-marker decision for one capability area and right on one object, with the activity that makes the case `OWN` and the field list of the panel | The caller's own session; the answer is the decision | 401; 403 MSG-P4-002; 404 MSG-P4-003; 422; 503 MSG-P7-003 |
| GET | `/api/recovery/access/v1/me/permissions` | The caller's resolved roles, letters per capability area, scope, matrix version and masking version | None beyond the session | 401; 503 |
| GET | `/api/recovery/access/v1/masking-policies` | The masking answer for a field list and a role, with the mask version | None beyond the session | 401; 503 |

Architecture v5 slide 14 names `POST /authorise`, `GET /me/permissions` and `/masking-policies`; TSD P4 v3 names `GET /me/session` (API-P4-012) for the same resolved view, so the resolved view is answered behind `GET /me/permissions` under R-PREC and the session read keeps its own story and its own shape. Whether the field list travels as a repeated `fields` parameter or in the request body is Not specified in the source documents (GAP-0952; ASM-1682).

#### 12.2 REST operations consumed

None. The case, the field inspection task, the ten items and their capture facts are sent in the authorise request by the gateway-bff composite route from the answer of RWB-P5-E2024-CON; this service calls no other service on this path, so the call stays one hop with the 2 s timeout of DP-11 and a circuit breaker. No `rwb-document`, `rwb-case` or `rwb-source-data` path is called here.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | matrix or mask version | the policy kind, the old and new version, validFrom, the affected capability areas or fields, the load reference |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | the entry ID | the hash-chained `AC-READ` or `AC-DENY` entry of DP-03, with the field markers and no value |

CloudEvents 1.0 envelope; neither payload carries personal data, a position, a file name or a photo. The `AccessPolicyChanged` event is written by the policy load path of this service (RWB-P4-AD002-APP, RWB-P4-AD004-APP) in the same transaction as the rows, and this story's part is the refresh it triggers.

#### 12.4 Events consumed

None from another service. The cache refresh reads this service's own `rwb.access.AccessPolicyChanged.v1` from `rwb.access.events.v1` through an internal listener, which is not a cross-service subscription; no `rwb.document.*`, `rwb.case.*` or `rwb.decision.*` event is read. The `DocumentStored` event of the store and the OCR intake that follows it are `rwb-document`'s and are neither consumed nor published here. The refresh fails closed: a policy event that does not parse leaves the cache on the versions it already holds (X6).

#### 12.5 Workflows and activities

None. This story starts no workflow and registers no activity; the capture and the OCR intake are `DocumentIntakeWorkflow` in `rwb-document`, and the case is `CaseWorkflow` in `rwb-case`.

#### 12.6 Schedules

None for this story. The capture needs no clock: its time checks are `rwb-document`'s and its parameters are that service's rows. The six-monthly access review list (JOB-18) is a Temporal Schedule of `rwb-access` and belongs to its own story, as is the document intake Schedule of `rwb-document` (JOB-12), which is not this service's.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The roles the caller holds, their class and default scope |
| `permission` | P4 (`rwb_access`) | The letters per capability area under the matrix version in force |
| `masking_rule` | P4 (`rwb_access`) | The unmasked flag per role and field under the mask version in force |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |

`document`, `document_intake`, `document_field`, `document_type`, `document_hub_parameter`, `recovery_case`, `task` and `decision_log_entry` are other services' and are not read: the capture facts are named, the values stay with `rwb-document`, and the ledger entry is written through the library (DP-01). `role_conflict` and `delegation_limit` are this service's tables and are not read on this path.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document field-capture WireMock | RWB-P5-E2024-CON | Case `RW-2026-000501` with entry date `2026-10-02` and a field inspection task for `FC-01`; the ten items (eight `INSPECTION_PHOTO`, two `UTILITY_BILL`) with capture time `2026-12-15 14:20` at `13.7563` and `100.5018`; the offline capture at `2026-12-14 10:05`; case `RW-2026-000502` with no task for `FC-01`; a three-item sync for the forced entry failure of TC-E2-024-17 |
| decision-record fake | RWB-PLT-E1027-CON | The entry write and the publish on `rwb.decision-record.v1`, including the forced failure for AC6 |
| guard and permission fakes | RWB-PLT-E1037-CON and RWB-P4-E1037-CON | The authorise, permission and masking operations, their problem responses and the idempotency key |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS, so the area `DOCUMENTS`, the four scopes and the role classes are values and not constants |
| parameters fake | RWB-P3-E1042-CON | Listed because DP-06 is in the pattern set of the legacy key; it is not called on this path, because the capture parameters are `rwb_document`'s rows behind RWB-P5-E2024-CON |
| gateway-bff route fake | RWB-PLT-N001-CON | The composite route that carries the field-app sync and the SCR-30 panel calls with their field lists, so the calls can be asserted |
| policy pack fixture | this story's own test data | The `PM-2026.12` `DOCUMENTS` rows for the five roles, the `MASK-SIT-01` rows for `DF-DOC-028` and `DF-DOC-029`, and a later masking version for AC7 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations used), consumed 0 | The decisions are served on `/authorise`, `/me/permissions` and `/masking-policies` of RWB-P4-E1037-CON on `/api/recovery/access/v1` |
| Kafka | Published 2, consumed 0 from other services | `rwb.access.events.v1` and `rwb.decision-record.v1` published; the cache refresh reads this service's own topic |
| Temporal | 0 | No workflow, no activity, no task queue use |
| File | None | No file input and no file output: a photo, a bill and a position are never a payload of this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/authorise`, Java package `th.co.scb.ace.workbench.recovery.access.authorise`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which patterns have an instance in this slice: DP-01 is the read of `permission` and `masking_rule` in `rwb_access`; DP-03 is the `AC-READ` and `AC-DENY` entry; DP-07 is the LOV-CAPABILITY area list, the LOV-SCOPE list and the LOV-ROLE-CLASS list; DP-09 is the outbox, the inbox and the idempotency key; DP-11 is the authorise contract with its mock and its 2 s timeout; DP-19 is the composite route that carries the sync and the panel. DP-15 and DP-06 have an instance only as an absence: this story adds no table, no column and no migration, and reads no parameter row.

The work of the legacy key that sits with other slices: the capture columns `captured_at`, `capture_latitude`, `capture_longitude`, `client_file_id` and `capture_kind`, their migration `V2_5_024__field_capture.sql` in the monolith and the partial unique index `ux_document_client_file` are `rwb-document`'s DP-15 work (RWB-P5-E2024-APP), and so is every migration of the capture path. The `DocumentStored` event, its outbox row and the OCR intake the `DocumentStoredListener` starts are `rwb-document`'s DP-09 work, not this service's. DP-19 is served through the gateway route, and DP-11 is served against the published contract and its fake.

The libraries, the Flyway baseline, the outbox and the gateway route are already build dependencies of the P4 service's own stories — the access baseline and the policy pack load path pull them — so this secondary slice adds no H dependency of its own (metadata H = None), is Day 1, and builds against RWB-P5-E2024-CON. This story needs no new migration: its rows live in `role`, `permission` and `masking_rule`, which the P4 access baseline owns, and the index the mask answer uses, `ix_masking_field_version`, is created by that baseline; the `MASK-SIT-01` rows themselves are the policy pack's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | REST controller | The three operations of 12.1, the problem responses with their message IDs, and the idempotency key |
| CaptureAccessService | Service | Resolution of the caller's letters for `DOCUMENTS` and one right, the object reference and the answer shape |
| ScopeCheck | Service | The scope from the role row and the `OWN` test on the activity sent in the request; 404 with MSG-P4-003 when the case is outside it |
| MaskingPolicyService | Service | The `masking_rule` read per role and field, the masked default, and the mask version in the answer |
| FieldMarkerResolver | Service | The field list of the sync and the panel resolved to field IDs and masked flags, with no value and no format |
| PolicyVersionResolver | Service | The matrix version and the mask version in force, read once per refresh and held together |
| AuthoriseCache | Cache | The cached answer per user, area, right, object and field list, with the versions; refresh on `AccessPolicyChanged`; fail closed on a mixed pair |
| AccessLogWriter | Service | The `AC-READ` and `AC-DENY` entry of DP-03, with the masked field markers and no value, in the same transaction as the answer |
| PolicyChangeListener | Kafka consumer with the inbox | The service's own `AccessPolicyChanged`, deduplicated by event ID, refreshing the cache |

**Database and migrations**

- Reads `role`, `permission` and `masking_rule` in `rwb_access`; writes the decision-record entry through the library, and the inbox, outbox and idempotency rows.
- Uses the index `ix_masking_field_version ON masking_rule (field_id, masking_version, role_code)` and `ix_permission_role_area_version ON permission (role_id, capability_area, matrix_version)`, both created by the access baseline.
- No new table, no new column and no new migration of this story's own: the policy tables are the policy pack path's, and the access log is the decision-record entry (DP-03).

**Configuration and reference data**

- LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS through the reference-data contract of DP-07 (RWB-P3-E1043-CON); the area `DOCUMENTS` is a value of that list, never a constant.
- The matrix version `PM-2026.12` and the masking version `MASK-SIT-01` in force are read from the rows, not configured; the SIT label is assumed (GAP-0950; ASM-1680).
- The field list of the sync and of the panel is the five capture fields of section 7; the field IDs are the Data Dictionary's and are not configured.
- The access entry's decision codes `AC-READ` and `AC-DENY` follow the decision-code list of the ledger, and the field markers come from the request.
- No switch of this slice's own: a capture that cannot be authorised must not be sent, so the authorise path has no off state. The legacy flag `rwb.dochub.field-capture` stays `rwb-document`'s and is a legacy reference here.

**Build steps**

1. `AuthoriseController` and the problem responses, with the three operations and the idempotency key; tests for 401, 403, 404 and 503 shapes.
2. `PolicyVersionResolver` and the two index reads; test that a new matrix version is served as data with no code change.
3. `CaptureAccessService` for rights `C`, `R` and `U` on `DOCUMENTS`, and `ScopeCheck` for the `OWN` test on the activity; tests for AC1, AC2, AC3 and AC5.
4. `MaskingPolicyService` and `FieldMarkerResolver` with the masked default and the mask version in the answer; tests for AC4, AC5 and AC9.
5. `AccessLogWriter` in the same transaction as the answer, with the masked markers and the no-value assertion; tests for AC1, AC2, AC3, AC6 and AC8, and the forced failure for AC6.
6. `AuthoriseCache` and `PolicyChangeListener` with the version pair and the mixed-pair refusal; test for AC7 with a fixed clock.
7. The contract-fake run against RWB-P5-E2024-CON and the gateway-bff route fake, so the story builds before `rwb-document` and SCR-30 exist in the environment.
8. The denial test for `RW-PHONECOL` through the composite route, the idempotency test for AC10, and the audit read of the entries through `rwb-decision`.

**Done when.** The tests in section 16 pass; every sync of a case in `OWN` scope writes exactly one `AC-READ` entry that names the case, the actor, the area and the field markers, with no latitude, no longitude and no file name anywhere in it; every refusal writes one `AC-DENY` entry with its area, right and case, and an out-of-scope case is answered 404 with MSG-P4-003 and nothing stored; the position is answered unmasked only to `RW-CASEOWN` and `RW-RESTRUCT` under the mask version named in the answer; every answer names the matrix version and the masking version it was decided under; and a masking policy change is served by the cache after `AccessPolicyChanged` with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not carry the right in the area | You cannot {action} here. Your role does not include it. | This story, on the authorise path |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. | This story, when the scope check fails |
| MSG-P7-003 | The access entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the entry writer |
| MSG-GEN-001 | A required field of the authorise request is missing | Enter {field}. | This story, on the request validation |
| MSG-GEN-004 | The cached policy was replaced while the call was in flight | Someone else changed this record. Reload it to see their change. | This story, on the version check |
| MSG-P5-015 | Captures accepted with no GPS position | {count} files have no location. They are on the case without a position. | `rwb-document`, shown on SCR-30 beside the masked position of this story |
| MSG-GEN-002 | Capture time in the future; too many files | {field} must be between {min} and {max}. | `rwb-document`, on the item; not this story |
| MSG-GEN-003 | Capture time before the case entry date or the age limit | {field} cannot be before {other}. | `rwb-document`, on the item; not this story |
| MSG-P5-001 | File type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. | `rwb-document`, on the item; not this story |
| MSG-P5-016 | A capture with malware | This file was not stored because the malware scan found a threat. It is held in quarantine. | `rwb-document`, on the item; not this story |
| MSG-P5-017 | A capture above the size limit | This file is larger than {size} MB and cannot be stored. | `rwb-document`, on the item; not this story |
| MSG-P5-003 | A bill field needs checking | Some fields need checking. The document is in the review queue. | `rwb-document`, on the panel; not this story |

The {action} value in MSG-P4-002 names the action and nothing else — for a field capture, "send a field capture", "read the captures" or "mark a capture reviewed" — and the problem response carries the capability area in its `detail` beside the message ID, so a refusal is diagnosable without any capture content. Every error is an RFC 9457 problem response with `messageId` set and `instance` naming the request.

### 15. Screens and states

No screen is built here. SCR-30 Case documents is `rwb-document`'s and reaches this service through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON); the field app screens belong to the field app:

| Screen | State | What this story supplies |
|---|---|---|
| SCR-30 Case documents | List | The `DOCUMENTS` R answer for the case, and the masked flags of the five fields, so the panel shows capture time, type, review state and position as the policy allows and no value comes from this service |
| SCR-30 Case documents | Capture without a position | The same masked answer for `DF-DOC-028` and `DF-DOC-029`; the MSG-P5-015 warning and the empty position are `rwb-document`'s |
| SCR-30 Case documents | Bill in review | The `DOCUMENTS` U answer for the OCR path and the review state; the review queue and its message are `rwb-document`'s |
| SCR-30 Case documents | Denied | The problem response of MSG-P4-002 or MSG-P4-003 with the action and the area, and the `AC-DENY` entry behind it |
| Field app capture screen | Ready | The `DOCUMENTS` C answer and the scope answer before a capture is sent; the screen itself is the field app's |

The panel layout and the masked rendering are Not specified in the source documents (GAP-0950; ASM-1680), and the composite route's field list is Not specified in the source documents (GAP-0951; ASM-1681); the screen stories are RWB-P5-E2024-APP, and this story changes no screen behaviour.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-024-16 | AC2, AC8, BR1, BR2, BR3 | Component | `U-4106` holding `RW-PHONECOL` with `DOCUMENTS` R calls the sync; 403 with MSG-P4-002 and one `AC-DENY` entry, and the P5 fake is never called |
| TC-E2-024-17 | AC6, BR7, BR9 | NFR | Three items for case `RW-2026-000501` and the decision-record write forced to fail; 503 with MSG-P7-003, no document accepted, no entry half written, an incident raised |
| TC-E2-024-01 | AC1, AC4, BR2, BR5 | Contract | The ten synthetic files with positions in Bangkok, eight `INSPECTION_PHOTO` and two `UTILITY_BILL`, at `13.7563` and `100.5018`; the documents are the fake's, the answer and the entry are this slice's |
| TC-E2-024-02 | AC1, BR6 | Contract | A capture at `2026-12-14 10:05` synced at `2026-12-15 08:30`; the access answer is unchanged, because the capture time is not an access input |
| TC-E2-024-03 | AC1, BR6 | Contract | A synthetic utility bill; the extracted amount and due date stay `rwb-document`'s and the entry names no bill value |
| TC-E2-024-04 | AC10, BR7 | Contract | The same ten client file IDs twice with Idempotency-Key `k-001`; the duplicate result is the fake's, the single entry is this slice's |
| TC-E2-024-05 | AC10, BR7 | Contract | Six of ten items received, then all ten resent; one entry for the received sync and no second entry for the resend |
| TC-E2-024-06 | AC9, BR5 | Contract | A photo with no position; the masked answer for `DF-DOC-028` and `DF-DOC-029` is unchanged and the MSG-P5-015 flag is the fake's |
| TC-E2-024-07 | AC1, BR6 | Contract | Capture times 6 and 5 minutes after receipt; the refusal and the acceptance are `rwb-document`'s, and the access answer is the same for both |
| TC-E2-024-08 | AC3, BR4 | Contract | A capture one day before the entry date `2026-10-02`; the item refusal is the fake's, and the case stays in scope |
| TC-E2-024-09 | AC1, BR6 | Contract | Captures 31 days and 30 days before the sync; the age limit is `rwb-document`'s row and changes no access answer |
| TC-E2-024-10 | AC1, BR6 | Contract | An HEIC file; the type refusal is the fake's and the accepted items are still authorised |
| TC-E2-024-11 | AC6, BR7 | NFR | An EICAR test file in the same sync as accepted items; the quarantine is `rwb-document`'s and the entry of the accepted items is written |
| TC-E2-024-12 | AC3, BR4 | Component | Case `RW-2026-000502` with no task for `FC-01`; 404 with MSG-P4-003, one `AC-DENY` entry, and no document, intake item or capture row |
| TC-E2-024-13 | AC5, BR10 | Contract | A bill amount at confidence 0.55 and the review state asked with right `U` by `SY-OCR`; the position is masked for it and the review queue is the fake's |
| TC-E2-024-14 | AC1, BR6 | Contract | Three manifest items and two files; the 422 is `rwb-document`'s and no entry is written for a sync it refuses before it starts |
| TC-E2-024-15 | AC1, BR6 | Contract | 51 files against the limit of 50; the 413 is `rwb-document`'s and no entry is written for it |

The legacy level System maps to Contract where the rule asserted is `rwb-document`'s and the story asserts only this slice's answer and entry, and to Component where the assertion itself is this slice's; Access maps to Component and Resilience to NFR. No case ID with the integration suffix is used here: the integration copy of the set is the integration harness story of this legacy key, which proves the same facts across `rwb-access`, `rwb-document` and `rwb-case` with real services, and its own copies of these test cases belong to that story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the letters C, R, U, D and A, the capability areas, the roles, the scopes, the masking rows and the matrix and mask versions are data rows; the Java code holds no letter, area, role, scope or version literal (BR-P4-004, BR-P4-005).
- No personal data in logs, events, tests, workflow history or prompts: the access entry carries the actor reference, the case reference, the area, the right, the field ID and a masked flag. Workflow history is not used because this story starts no workflow.
- ACE data only through the owner's contract or a `v_ace_*` view of this service; this story reads no ACE view at all and no `v_ace_customer` fact.
- No position, file name or photo in an entry, an event or a log: `DF-DOC-028` and `DF-DOC-029` are answered as field IDs and flags, the coordinates stay in `rwb_document`, and no `DocumentStored` payload passes through this service. A test scans the entry text and both event payloads for any digit of `13.7563` and `100.5018`.
- The mask answer is data, not code: whether a role sees a position is one `masking_rule` row under the version in force; a field with no row is masked, and a change of the answer needs an approved load and no release.
- No read of another service's tables and no cross-schema read (DP-01): `document`, `document_intake`, `document_field`, `document_type`, `document_hub_parameter`, `recovery_case`, `task` and `decision_log_entry` are never queried here.
- An answer is never served without its entry, and the answer and the entry commit in one transaction (R-UNI-39); a call that cannot be logged is refused with MSG-P7-003.
- The cache fails closed: an unparseable or mixed policy event leaves the versions in force, and a missing policy row is a refusal or a masked field, never a default allow and never a clear value.
- The authorise path has no off switch, because a capture that cannot be authorised must not be sent; the legacy field-capture flag stays `rwb-document`'s.
- A service identity gets no bypass: `SY-OCR` is answered from its own role rows, and its scope is its `default_scope` row (NFR-051).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-21 | 13 Manage documents and correspondence | R-DIL-22, R-UNI-39, R-UNI-40 | TC-E2-024-01 to TC-E2-024-17 |

| Legacy reference | Where it is kept |
|---|---|
| Roles `RW-FIELDCOL` with Documents CR, `RW-CASEOWN` and `RW-RESTRUCT` with Documents CRU, `SY-OCR` with Documents CRU and `RW-PHONECOL` with Documents R | Metadata, sections 3, 7, 8, 10 |
| Case `RW-2026-000501`, entry date `2026-10-02`, field collector `FC-01`, ten items (eight `INSPECTION_PHOTO`, two `UTILITY_BILL`), `13.7563` and `100.5018`, capture at `2026-12-15 14:20` and `2026-12-14 10:05` | Background, AC1 to AC4, AC8, sections 3, 12.8, 16 |
| Case `RW-2026-000502` outside the collector's scope, and the 404 with MSG-P4-003 | AC3, sections 4, 5, 14, 16 (TC-E2-024-12) |
| Legacy BR9 and CTL-11 on the position and the photos of a home, and the masked default | Sections 1, 7, 8, 10, 11, 17 |
| MSG-P4-002, MSG-P4-003, MSG-P7-003, MSG-P5-015, MSG-GEN-001 to MSG-GEN-003 | Section 14, exception paths |
| Legacy test set TC-E2-024-01 to TC-E2-024-17, with the access test TC-E2-024-16 and the principle 5 test TC-E2-024-17 first, and its integration copy RWB-ITG-E2024-ITG | Section 16 |
| Legacy key RWB-E2-024, story RWB-P4-E2024-APP, contract RWB-P5-E2024-CON, feature FEAT-DCM-21 | Metadata, sections 3, 12 |

### 19. Out of scope

- The `rwb-document` slice of this legacy key, RWB-P5-E2024-APP with RWB-P5-E2024-CON: the `POST /cases/{caseId}/field-captures` endpoint, the manifest and file matching, the duplicate check on `client_file_id`, the file type and size checks, the clock skew and the age limit, the malware scan and the quarantine, the store, the capture columns, the partial unique index, the `DocumentStored` event, the OCR intake, the `UTILITY_BILL` extraction and the review queue, the SCR-30 panel and the `rwb.dochub.field-capture` flag.
- The field app itself and its offline store, and the agency field teams that reach the Workbench only through the external gateway (DL03; FEAT-PRM-15, Epic 7).
- The inspection task, the checklist rule and the asset unlock rule (`WITH_FIELD_INSPECTION`, R-DIL-22, FEAT-TRT-15, Epic 3), and the repossessed vehicle photo standard (CTL-38, Epic 7).
- The case facts, the entry date and the field inspection task (`rwb-case`), and the `DOCATT` entry the store writes (`rwb-document`).
- The integration harness RWB-ITG-E2024-ITG and its `-ITG` copies of the test cases.
- The policy pack load path of this service — the reference loads, their approval, verification and rollback, and the rows of `PM-2026.12` and `MASK-SIT-01` themselves (RWB-P4-AD002-APP, RWB-P4-AD004-APP).
- Role, scope and sign-in administration, break-glass, the access review list (JOB-18) and the access audit query (FEAT-ACA-16), which are the P4 administration stories.
- The delegation of authority table and its lookup (RWB-P4-E2013-APP), which no capture uses.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of the authorise path (an OPS story of this legacy key).
